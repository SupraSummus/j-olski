"""Measuring the grammar against Składnica.

The number this produces is the experiment docs/design-notes.md has been
promising: what fraction of real Polish olski admits, per unit of formal power.
Right now the answer is small, and it is supposed to be — olski is a deliberate
subset — so the useful part of the report is not the fraction but the three
breakdowns under it.

**Where analyses die.** A rejected sentence stopped somewhere, and the part of
speech of the token it stopped on names the construction that would have to be
admitted next. Ranked by frequency, that is a work queue ordered by how much
Polish each addition buys, which is the "principled way to say no" that
design-notes.md asks for: a construction worth thousands of sentences is worth
the formal power it costs, and one worth eleven is not.

**Gold morphology against live.** Run with the treebank's disambiguated tags and
the grammar is measured alone. Run with Morfeusz and the analyser's ambiguity
comes back, none of it resolved, because Morfeusz analyses and does not choose.
The gap between the two is what ambiguity costs olski, separated from what the
grammar cannot derive at all.

**Agreement, not just acceptance.** Accepting a sentence is worth nothing if the
reading is wrong. Olski admits every order the subject, the object and the verb
can stand in, so on every sentence it accepts
there is a real question of whether it found the same subject the annotators did,
and a wrong subject is a worse outcome than a rejection: it is a sentence olski
claims to understand backwards. Only the gold-morphology run can check this,
because only there do spans mean the same thing on both sides.
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import functools
import os
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.corpus import Sentence, pliki, read
from olski.morph import Segment
from olski.parse import MAX_READINGS, Las, Result, las, podsumuj
from olski.subset import GRAMMAR, morphology

#: Length buckets for the coverage curve, as upper bounds in tokens.
BUCKETS = (5, 10, 20, 40)

#: Kubełki, na jakie dzieli się numer złotego czytania, jako górne granice.
#: Obie granice coś znaczą, a równych odstępów nie ma tu po czym mierzyć:
#: czytanie pierwsze jest tym, które czytelnik zobaczy na górze wydruku,
#: a za :data:`MAX_READINGS` nie zobaczy go wcale.
GŁĘBOKOŚCI = (1, MAX_READINGS)

#: What the report says when a sentence was derivable up to its last token and
#: still had no reading covering the whole of it.
NO_STRUCTURE = "(no structure over whole sentence)"

#: Morphology sources. ``gold`` is the treebank's disambiguated tags, ``live`` is
#: Morfeusz on the raw text, ambiguity included.
SOURCES = ("gold", "live")

#: Role, którymi mierzy się zgodność z drzewem wzorcowym: te, które olski ma i które
#: gniazdo walencyjne w tym drzewie nazywa (``_slot_role`` w ``olski/corpus.py``).
#: Jedna lista na oba pytania, bo zgodność czytania przyjętego i ocalenie czytania
#: wśród wielu są tą samą miarą zadaną innym zbiorom zdań,
#: a rozejście się tych list zrobiłoby z nich dwie miary o jednej nazwie.
PORÓWNYWANE_ROLE = ("Subject", "Object")


@dataclass(frozen=True)
class Outcome:
    """What olski said about one corpus sentence."""

    sentence: Sentence
    result: Result
    #: What was actually parsed, which is the gold terminals only in the gold
    #: run. Under live morphology the positions are character offsets, so asking
    #: the gold segments where the analysis stopped would name the wrong token.
    segments: tuple[Segment, ...] = ()
    #: False when spans on the two sides are not comparable, which is the case
    #: whenever the morphology did not come from the gold tree.
    comparable: bool = True
    #: Czy złote czytanie ocalało wśród czytań zdania, które olski czyta kilkoma;
    #: ``None``, gdy pytanie nie powstaje.
    #: Wpisane z zewnątrz, a nie liczone tutaj jak :attr:`agreement`,
    #: bo odpowiada na nie las, a werdykt lasu nie niesie:
    #: waży on tyle, ile jego tablica, a raport przechodzi granicę procesu.
    ocalenie: str | None = None
    #: Którym z kolei czytaniem złote jest, jeżeli ocalało; ``None``, gdy nie ocalało
    #: albo gdy pytanie nie powstaje.
    #: Osobno od :attr:`ocalenie`, bo mówi, ile tamta odpowiedź jest warta,
    #: a nie powtarza jej innym typem.
    głębokość: int | None = None

    def __post_init__(self) -> None:
        if not self.segments:
            object.__setattr__(self, "segments", self.sentence.segments)

    @property
    def status(self) -> str:
        return self.result.status

    @property
    def blocker(self) -> str | None:
        """The part of speech the analysis stopped on, for a rejected sentence.

        Asked of a parse that was not asked how far it got, this raises:
        ``furthest`` is then ``None``,
        position zero would name whatever the sentence opens with,
        and the ranking would rank that.

        Exact under gold morphology, where a terminal has one reading because the
        annotators disambiguated it. Approximate under live morphology, where the
        form usually has several and this names the first one Morfeusz listed:
        the analysis stopped because *no* reading of that form could continue, so
        there is no single part of speech to name, and picking one keeps the
        ranking readable at the cost of being arbitrary between them.
        """
        if not self.result.rejected:
            return None
        if self.result.furthest is None:
            raise ValueError("bloker: rozbiór nie był pytany, dokąd doszedł")
        for segment in self.segments:
            if segment.start == self.result.furthest:
                readings = segment.readings
                return readings[0].tag.pos if readings else NO_STRUCTURE
        return NO_STRUCTURE

    @property
    def agreement(self) -> str | None:
        """Whether olski's roles match the gold tree's, on a sentence it accepts.

        ``None`` when the question does not arise: the sentence was not accepted,
        the spans are not comparable, or the gold tree marks no role to compare
        against.
        """
        if not self.result.valid or not self.comparable:
            return None
        if not self.sentence.roles:
            return None
        reading = self.result.readings[0]

        # Taken apart from the extent disagreements below, because this is the
        # failure the whole ambiguity design exists to prevent: olski admits SVO
        # and OVS, so a sentence read with the subject and object exchanged is
        # not an imprecise analysis but the opposite claim, confidently made.
        subject = frozenset(node.span for node in reading.find("Subject"))
        objects = frozenset(node.span for node in reading.find("Object"))
        if subject & self.sentence.spans("Object") or objects & self.sentence.spans("Subject"):
            return "reversed"

        # Both roles are judged before either verdict is returned. Returning on
        # the first role that is not a clean match would report a sentence that
        # is partial on its subject and wrong on its object as merely partial,
        # which is the milder of the two claims and the wrong one.
        contradicted = False
        incomplete = False
        for role in PORÓWNYWANE_ROLE:
            gold = self.sentence.spans(role)
            found = frozenset(node.span for node in reading.find(role))
            if found - gold:
                contradicted = True
            elif gold - found:
                # The gold tree marks a role olski did not assign at all. Not a
                # wrong reading, but not a confirmed one either.
                incomplete = True
        if contradicted:
            return "disagrees"
        return "partial" if incomplete else "agrees"


@dataclass
class Report:
    """Counts over a run, and the examples that make them legible."""

    source: str
    verdicts: collections.Counter = field(default_factory=collections.Counter)
    statuses: collections.Counter = field(default_factory=collections.Counter)
    blockers: collections.Counter = field(default_factory=collections.Counter)
    agreements: collections.Counter = field(default_factory=collections.Counter)
    lengths: dict[str, collections.Counter] = field(default_factory=dict)
    examples: dict[str, list[str]] = field(default_factory=dict)
    #: Annotated sentences nothing was measured on, by why not. Reported rather
    #: than dropped, because a coverage figure that quietly excluded the hard
    #: sentences would be a coverage figure of the easy ones.
    skipped: collections.Counter = field(default_factory=collections.Counter)
    #: Accepted sentences the agreement check had nothing to compare against,
    #: because the gold tree marks no subject or object — a pro-drop sentence
    #: realizes neither. Reported for the same reason: 108 of 112 reads very
    #: differently once you know 196 sentences were accepted.
    unjudged: int = 0
    #: Zdania wieloznaczne po tym, czy złote czytanie jest wśród ich czytań.
    ocalenia: collections.Counter = field(default_factory=collections.Counter)
    #: Zdania, w których złote czytanie ocalało, po jego numerze w kolejności czytań.
    #: Liczone numerem, a nie kubełkiem, bo kubełek jest sposobem opowiedzenia tej liczby
    #: i wybiera go wydruk, a najgłębszy numer trzeba mieć dokładnie.
    głębokości: collections.Counter = field(default_factory=collections.Counter)
    #: Zdania wieloznaczne, o które to pytanie nie pada, bo drzewo wzorcowe nie
    #: nazywa ani jednej roli. Osobno od licznika wyżej z tego samego powodu, dla
    #: którego :attr:`unjudged` liczy się osobno od :attr:`agreements`.
    bez_roli: int = 0

    @property
    def measured(self) -> int:
        return sum(self.statuses.values())

    def record(self, outcome: Outcome, keep_examples: int) -> None:
        status = outcome.status
        self.statuses[status] += 1
        blocker = outcome.blocker
        if blocker is not None:
            self.blockers[blocker] += 1
        agreement = outcome.agreement
        if agreement is not None:
            self.agreements[agreement] += 1
        elif outcome.comparable and outcome.result.valid:
            self.unjudged += 1
        if outcome.ocalenie is not None:
            self.ocalenia[outcome.ocalenie] += 1
        elif outcome.comparable and outcome.result.ambiguous:
            self.bez_roli += 1
        if outcome.głębokość is not None:
            self.głębokości[outcome.głębokość] += 1
        bucket = _bucket(len(outcome.sentence.segments), BUCKETS)
        self.lengths.setdefault(bucket, collections.Counter())[status] += 1
        kept = self.examples.setdefault(_example_key(outcome), [])
        if len(kept) < keep_examples:
            kept.append(outcome.sentence.text)


def _example_key(outcome: Outcome) -> str:
    if outcome.agreement in ("reversed", "disagrees", "partial"):
        return f"{outcome.status}/{outcome.agreement}"
    if outcome.ocalenie is not None:
        return f"{outcome.status}/{outcome.ocalenie}"
    return outcome.status


def _bucket(count: int, bounds: Sequence[int]) -> str:
    """Kubełek, w który ta liczba wpada, nazwany przedziałem, jaki obejmuje.

    Jedna funkcja na obie krzywe, bo różnią się granicami i niczym poza nimi.
    """
    previous = 1
    for bound in bounds:
        if count <= bound:
            return f"{bound}" if previous == bound else f"{previous}-{bound}"
        previous = bound + 1
    return f"{previous}+"


def segments_for(sentence: Sentence, source: str) -> list[Segment]:
    """The morphology to measure the grammar against.

    The live run goes through ``subset.morphology`` rather than through Morfeusz
    directly, so that the corpus is read the same way a checked document is. The
    gold run needs no equivalent: the annotators chose one reading per terminal,
    so the readings ``admissible`` drops are not there to drop.
    """
    if source == "gold":
        return list(sentence.segments)
    return morphology(sentence.text)


def _ocalenie(
    zbudowany: Las, sentence: Sentence, result: Result, comparable: bool
) -> tuple[str | None, int | None]:
    """Czy złote czytanie jest wśród czytań tego zdania i którym z nich.

    Oddaje dwie wartości ``None``, gdy pytanie nie powstaje, a nie powstaje w trzech wypadkach.
    Rozpiętości nieporównywalne: pod żywą morfologią pozycje są odstępami w napisie,
    więc złote rozpiętości nazywałyby co innego.
    Drzewo wzorcowe bez ani jednej roli: nie ma czego szukać.
    Zdanie czytane raz albo wcale: o jednym czytaniu mówi już :attr:`Outcome.agreement`
    i mówi więcej niż to pytanie, bo rozdziela czytanie zawężone od odwróconego,
    a o zdaniu odrzuconym mówić nie ma czemu.

    Zostaje więc zdanie wieloznaczne, czyli to, o którym samo odrzucenie mówi
    tyle, że jakieś czytanie się wyprowadziło.

    Werdykt i numer wracają razem, a nie jeden zamiast drugiego:
    o zdaniu, którego złote czytanie przepadło, numer nie mówi nic.
    """
    if not comparable or not result.ambiguous or not sentence.roles:
        return None, None
    złote = {rola: sentence.spans(rola) for rola in PORÓWNYWANE_ROLE}
    numer = zbudowany.numer_czytania(złote)
    return ("lost", None) if numer is None else ("survives", numer)


def zmierz_zdanie(sentence: Sentence, segments: Sequence[Segment], comparable: bool) -> Outcome:
    """Jeden las tego zdania i wszystko, co przebieg z niego bierze.

    Jedno miejsce, w którym `Outcome` powstaje z lasu, bo las waży tyle, ile jego
    tablica: pytanie zadane osobno kosztowałoby drugi rozbiór tego zdania.

    O to, dokąd analiza doszła, pyta wprost,
    bo ranking blokerów jest tym, co ten przebieg czyta z odrzucenia
    (:attr:`Outcome.blocker`).
    """
    zbudowany = las(GRAMMAR, list(segments))
    result = podsumuj(zbudowany, najdalszy=True)
    ocalenie, głębokość = _ocalenie(zbudowany, sentence, result, comparable)
    return Outcome(
        sentence=sentence,
        result=result,
        segments=tuple(segments),
        comparable=comparable,
        ocalenie=ocalenie,
        głębokość=głębokość,
    )


def measure(
    sentences: Iterable[Sentence],
    source: str = "gold",
    keep_examples: int = 0,
) -> Report:
    """Run the grammar over corpus sentences and count what came back.

    Every forest seen is counted in the composition table, including the ones
    with no gold tree, so the annotated fraction stays visible next to the
    coverage figure computed from it.

    Every annotated sentence is measured, however long, so the denominator under
    the coverage figure is the whole annotated corpus. Length needs no bound
    here: the forest counts readings by summing over root positions instead of
    walking them, so a long sentence costs one chart however many readings it
    admits. What the treebank's longest sentences cost is in
    docs/corpus.md#the-measurement, beside the row they fall in.
    """
    if source not in SOURCES:
        raise ValueError(f"unknown morphology source: {source}")
    report = Report(source=source)
    for sentence in sentences:
        report.verdicts[sentence.verdict or "?"] += 1
        if not sentence.annotated:
            continue
        segments = segments_for(sentence, source)
        if not segments:
            report.skipped["no morphology"] += 1
            continue
        report.record(zmierz_zdanie(sentence, segments, source == "gold"), keep_examples)
    return report


# --------------------------------------------------------------------------- #
# Przebiegi
# --------------------------------------------------------------------------- #

#: Ile lasów bierze jeden kawałek pracy.
#:
#: Kawałek jest tym, co proces roboczy dostaje i za co oddaje `Report`, więc przez
#: granicę procesu idzie licznik, a nie las, który go zbudował. Mniejszy kawałek
#: równa obciążenie — lasy różnią się rozmiarem o rzędy wielkości, bo długie
#: zdanie ma większy las — a częściej płaci za to przejście.
KAWAŁEK = 64


def _kawałek(ścieżki: Sequence[Path], source: str, keep_examples: int) -> Report:
    """Odcinek listy plików, przeczytany i zmierzony tam, gdzie stoi."""
    return measure((read(path) for path in ścieżki), source, keep_examples)


def po_kawałkach(ścieżki: Sequence[Path], jobs: int, praca):
    """Podziel listę lasów na kawałki i oddaj to, co każdy z nich policzył.

    Dzieli pliki, a nie zdania, bo dopiero plik daje się oddać procesowi
    roboczemu bez przenoszenia przez granicę procesu tego, co się z niego czyta.

    Jeden proces liczy na miejscu, a nie w puli o jednym pracowniku, żeby został
    ślad wyjątku i profil, które granica procesu zabiera.

    Wołający dostaje listę w kolejności kawałków i sam ją składa, bo licznik,
    który z kawałka wraca, jest jego, a nie tego podziału. Drugim wołającym jest
    `sonda/przecinek.py`, i po to ten podział stoi osobno od `scal` niżej.
    """
    kawałki = [ścieżki[start : start + KAWAŁEK] for start in range(0, len(ścieżki), KAWAŁEK)]
    if jobs == 1:
        return [praca(kawałek) for kawałek in kawałki]
    with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as pula:
        return list(pula.map(praca, kawałki))


def przebieg(
    ścieżki: Sequence[Path],
    jobs: int,
    source: str = "gold",
    keep_examples: int = 0,
) -> Report:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport."""
    praca = functools.partial(_kawałek, source=source, keep_examples=keep_examples)
    return scal(po_kawałkach(ścieżki, jobs, praca), source, keep_examples)


def scal(raporty: Iterable[Report], source: str, keep_examples: int = 0) -> Report:
    """Złóż raporty kawałków w jeden.

    Kawałki są ciągłymi odcinkami jednej posortowanej listy plików i wchodzą tu w
    kolejności tej listy, więc scalony raport jest tym samym raportem, co z
    jednego przebiegu nad całością. Przykłady sprawdzają to najostrzej:
    `Report.record` zachowuje pierwsze zdania, jakie dostał, więc przykład
    wybrany przez to, który proces skończył pierwszy, byłby innym wydrukiem z
    tego samego korpusu.

    Morfologię nazywa wołający, choć każdy raport swoją niesie, bo katalog bez
    lasów nie oddaje żadnego raportu, a nagłówek wydruku i tak ją drukuje.
    """
    scalony = Report(source=source)
    for raport in raporty:
        scalony.verdicts.update(raport.verdicts)
        scalony.statuses.update(raport.statuses)
        scalony.blockers.update(raport.blockers)
        scalony.agreements.update(raport.agreements)
        scalony.ocalenia.update(raport.ocalenia)
        scalony.głębokości.update(raport.głębokości)
        scalony.skipped.update(raport.skipped)
        scalony.unjudged += raport.unjudged
        scalony.bez_roli += raport.bez_roli
        for bucket, counts in raport.lengths.items():
            scalony.lengths.setdefault(bucket, collections.Counter()).update(counts)
        for key, kept in raport.examples.items():
            zebrane = scalony.examples.setdefault(key, [])
            zebrane.extend(kept)
            del zebrane[keep_examples:]
    return scalony


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #


def _rows(pary: Sequence[tuple[str, int]], total: int) -> list[str]:
    """Wiersze tabeli w kolejności, w jakiej przyszły.

    Kolejność wybiera wołający, bo znaczy w każdej tabeli co innego:
    licznik czyta się od najliczniejszego, a kubełek od najmniejszej granicy.
    """
    lines = []
    for name, count in pary:
        share = f"{count / total:6.1%}" if total else "     -"
        lines.append(f"  {count:7} {share}  {name}")
    return lines


def _dolna_granica(kubełek: str) -> int:
    """Granica, od której ten kubełek się zaczyna, czyli to, co go porządkuje.

    Nazwa kubełka zaczyna się od niej, bo tak ją składa :func:`_bucket`,
    i obie krzywe sortują się nią, żeby ta zależność miała jedno miejsce.
    """
    return int(kubełek.split("-")[0].rstrip("+"))


def _wobec_złotego(
    counter: collections.Counter, nagłówek: str, bez_roli: int, status: str
) -> list[str]:
    """Tabela porównania z drzewem wzorcowym, a pod nią zdania, których nie było z czym.

    Obie takie tabele idą tędy, bo wiersz niemierzonych ma powiedzieć w obu to samo:
    mianownik zawężony przez samo porównanie czyta się jak mianownik całego wiersza.
    """
    if not counter:
        return []
    ile = sum(counter.values())
    wiersze = ["", f"{nagłówek.format(ile=ile)}:", *_rows(counter.most_common(), ile)]
    if bez_roli:
        wiersze.append(f"  {bez_roli:7}          {status}, no gold role to compare")
    return wiersze


def _jak_głęboko(głębokości: collections.Counter) -> list[str]:
    """Którym z kolei czytaniem bywa złote, w kubełkach, a pod nimi najgłębszy numer.

    Kubełki dzieli granica wypisywania, a nie równe odstępy,
    bo to ona rozstrzyga, czy czytelnik złote czytanie zobaczy
    (docs/corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).
    Najgłębszy numer idzie pod nie sam,
    bo mówi, jak blisko tej granicy przebieg podszedł, czego kubełek nie mówi.
    """
    if not głębokości:
        return []
    ile = sum(głębokości.values())
    w_kubełkach = collections.Counter()
    for numer, count in głębokości.items():
        w_kubełkach[_bucket(numer, GŁĘBOKOŚCI)] += count
    kolejne = [(nazwa, w_kubełkach[nazwa]) for nazwa in sorted(w_kubełkach, key=_dolna_granica)]
    return [
        "",
        f"which reading the gold one is, on {ile} sentences where it survives:",
        *_rows(kolejne, ile),
        f"  the deepest is reading {max(głębokości)}",
    ]


def render(report: Report, blockers: int = 12) -> str:
    total = report.measured
    lines = [
        f"Składnica, {report.source} morphology",
        "",
        f"corpus: {sum(report.verdicts.values())} forests",
        *_rows(report.verdicts.most_common(), sum(report.verdicts.values())),
        "",
        f"olski over {total} annotated sentences:",
        *_rows(report.statuses.most_common(), total),
    ]
    for reason, count in report.skipped.most_common():
        lines.append(f"  {count:7}          not measured: {reason}")

    lines += _wobec_złotego(
        report.agreements,
        "roles against the gold tree, on {ile} accepted sentences",
        report.unjudged,
        "accepted",
    )
    lines += _wobec_złotego(
        report.ocalenia,
        "the gold reading among the readings, on {ile} ambiguous sentences",
        report.bez_roli,
        "ambiguous",
    )
    lines += _jak_głęboko(report.głębokości)
    if report.lengths:
        lines += ["", "coverage by sentence length:"]
        for bucket in sorted(report.lengths, key=_dolna_granica):
            counts = report.lengths[bucket]
            seen = sum(counts.values())
            valid = counts.get("valid", 0)
            lines.append(f"  {bucket:>7} tokens: {valid:5}/{seen:<6} {valid / seen:6.1%} valid")

    if report.blockers:
        blocked = sum(report.blockers.values())
        lines += [
            "",
            f"where the {blocked} rejected sentences stopped:",
            *_rows(report.blockers.most_common(blockers), blocked),
        ]

    for key in sorted(report.examples):
        kept = report.examples[key]
        if not kept:
            continue
        lines += ["", f"{key} examples:"]
        lines += [f"  {text}" for text in kept]

    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="olski-corpus",
        description="Measure the olski grammar against the Składnica treebank.",
    )
    parser.add_argument("root", help="directory of extracted Składnica forest files")
    parser.add_argument(
        "--morphology",
        choices=SOURCES,
        default="gold",
        help="gold tags from the treebank, or Morfeusz on the raw text",
    )
    parser.add_argument("--limit", type=int, help="stop after this many forests")
    parser.add_argument("--blockers", type=int, default=12, help="how many blockers to rank")
    parser.add_argument("--examples", type=int, default=0, help="sentences to show per outcome")
    parser.add_argument(
        "--jobs",
        type=int,
        default=os.cpu_count() or 1,
        help="processes to read and measure with; 1 runs in this one",
    )
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs takes at least one process")

    root = Path(args.root)
    if not root.is_dir():
        print(f"olski-corpus: not a directory: {root}", file=sys.stderr)
        print("olski-corpus: see docs/corpus.md for how to fetch the corpus", file=sys.stderr)
        return 2

    report = przebieg(
        pliki(root)[: args.limit],
        args.jobs,
        source=args.morphology,
        keep_examples=args.examples,
    )
    print(render(report, args.blockers))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
