"""Pomiar gramatyki nad bankiem drzew: ile Składnicy olski przyjmuje i czy tak samo ją czyta.

Liczba stąd jest eksperymentem, który obiecuje docs/design-notes.md: jaką część
prawdziwej polszczyzny olski wpuszcza za jednostkę mocy formalnej. Odpowiedź jest
mała i ma taka być — olski jest podzbiorem z wyboru — więc czyta się nie sam
ułamek, a rozbicia pod nim.

**Gdzie umiera analiza.** Kolejka blokerów uszeregowana częstością mówi, ile
polszczyzny każde dopisanie obiecuje, a ile z tej obietnicy zostaje, widać dopiero
po dopisaniu (docs/roadmap.md). Jest to ta sama kolejka, którą autor czyta nad
własnym plikiem, więc liczy ją ``olski/pokrycie.py`` i stamtąd bierze się tu
:class:`Wynik` wraz z nią.

**Morfologia złota wobec żywej.** Z odczytaniami anotatora mierzy się samą
gramatykę. Z Morfeuszem wraca wieloznaczność analizatora, nierozstrzygnięta,
bo Morfeusz analizuje i nie wybiera. Różnica między jednym a drugim jest ceną
wieloznaczności, oddzieloną od tego, czego gramatyka nie wyprowadza wcale.

**Zgodność, a nie samo przyjęcie.** Przyjęcie zdania nie jest warte nic, jeżeli
czytanie jest złe. Olski wpuszcza każdy szyk, w jakim podmiot, dopełnienie i
czasownik mogą stanąć, więc nad każdym zdaniem przyjętym stoi pytanie, czy
znalazł ten sam podmiot co anotatorzy, a podmiot odwrócony jest gorszy od
odrzucenia: to zdanie, które olski twierdzi, że rozumie na odwrót. Sprawdzić to
umie sam przebieg nad morfologią złotą, bo tylko tam rozpiętości znaczą po obu
stronach to samo.

Cały ten moduł stoi po stronie harnessu, bo pyta o cudze drzewa wzorcowe i czyta
korpus, którego nikt sprawdzający własny tekst nie pobiera (``harness/__init__.py``).

    python3 -m harness.pomiar Składnica-frazowa-180723/ --morphology live
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

from harness.corpus import Sentence, pliki, read
from olski.morph import Segment
from olski.parse import MAX_READINGS, Las, Result, las, podsumuj
from olski.pokrycie import (
    Raport,
    Wynik,
    dolna_granica,
    kubełek,
    render,
    wiersze_tabeli,
)
from olski.segmentacja import morphology
from olski.subset import GRAMMAR

#: Morphology sources. ``gold`` is the treebank's disambiguated tags, ``live`` is
#: Morfeusz on the raw text, ambiguity included.
SOURCES = ("gold", "live")

#: Kubełki, na jakie dzieli się numer złotego czytania, jako górne granice.
#: Obie granice coś znaczą, a równych odstępów nie ma tu po czym mierzyć:
#: czytanie pierwsze jest tym, które czytelnik zobaczy na górze wydruku,
#: a za :data:`MAX_READINGS` nie zobaczy go wcale.
GŁĘBOKOŚCI = (1, MAX_READINGS)

#: Role, którymi mierzy się zgodność z drzewem wzorcowym: te, które olski ma i które
#: gniazdo walencyjne w tym drzewie nazywa (``_slot_role`` w ``harness/corpus.py``).
#: Jedna lista na oba pytania, bo zgodność czytania przyjętego i ocalenie czytania
#: wśród wielu są tą samą miarą zadaną innym zbiorom zdań,
#: a rozejście się tych list zrobiłoby z nich dwie miary o jednej nazwie.
PORÓWNYWANE_ROLE = ("podmiot", "dopełnienie")


@dataclass(frozen=True, kw_only=True)
class Outcome(Wynik):
    """Co olski powiedział o jednym zdaniu banku drzew, wraz z tym, co mówi drzewo.

    Kolejka blokerów, status i krzywa długości są tu tym samym, czym nad prozą,
    i biorą się z :class:`olski.pokrycie.Wynik`. Dochodzi to, czego proza nie ma:
    drzewo wzorcowe, wobec którego mierzy się czytanie.
    """

    #: Zdanie banku drzew wraz z drzewem wzorcowym nad nim.
    sentence: Sentence
    #: False when spans on the two sides are not comparable, which is the case
    #: whenever the morphology did not come from the gold tree: under live
    #: morphology the parser numbers positions in characters and the gold tree
    #: numbers them in tokens.
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
        if not self.tekst:
            object.__setattr__(self, "tekst", self.sentence.text)

    @property
    def długość(self) -> int:
        """Terminale drzewa wzorcowego, a nie te, po których szedł rozbiór.

        Pod żywą morfologią te dwie listy są różne, a krzywa ma dzielić zdania
        tak samo w obu przebiegach, bo różnica między nimi jest właśnie tym,
        co ta krzywa pokazuje.
        """
        return len(self.sentence.segments)

    @property
    def klucz(self) -> str:
        if self.agreement in ("reversed", "disagrees", "partial"):
            return f"{self.status}/{self.agreement}"
        if self.ocalenie is not None:
            return f"{self.status}/{self.ocalenie}"
        return self.status

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
        subject = frozenset(node.span for node in reading.find("podmiot"))
        objects = frozenset(node.span for node in reading.find("dopełnienie"))
        if subject & self.sentence.spans("dopełnienie") or objects & self.sentence.spans("podmiot"):
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
class RaportZłoty(Raport):
    """Liczniki prozy wraz z tymi, na które odpowiada samo drzewo wzorcowe."""

    #: Werdykty anotatorów nad lasami, czyli skład korpusu. Liczony także tam,
    #: gdzie drzewa wzorcowego nie ma, żeby ułamek zanotowanych stał obok
    #: pokrycia policzonego z niego.
    verdicts: collections.Counter = field(default_factory=collections.Counter)
    agreements: collections.Counter = field(default_factory=collections.Counter)
    #: Accepted sentences the agreement check had nothing to compare against,
    #: because the gold tree marks no subject or object — a pro-drop sentence
    #: realizes neither. Reported for the same reason ``skipped`` is: 108 of 112
    #: reads very differently once you know 196 sentences were accepted.
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

    def record(self, wynik: Outcome) -> None:
        super().record(wynik)
        agreement = wynik.agreement
        if agreement is not None:
            self.agreements[agreement] += 1
        elif wynik.comparable and wynik.result.valid:
            self.unjudged += 1
        if wynik.ocalenie is not None:
            self.ocalenia[wynik.ocalenie] += 1
        elif wynik.comparable and wynik.result.ambiguous:
            self.bez_roli += 1
        if wynik.głębokość is not None:
            self.głębokości[wynik.głębokość] += 1

    def dołóż(self, inny: RaportZłoty) -> None:
        super().dołóż(inny)
        self.verdicts.update(inny.verdicts)
        self.agreements.update(inny.agreements)
        self.ocalenia.update(inny.ocalenia)
        self.głębokości.update(inny.głębokości)
        self.unjudged += inny.unjudged
        self.bez_roli += inny.bez_roli

    def wiersze(self, blockers: int) -> list[str]:
        return [
            *self.skład(),
            *self.statusy(),
            *self.wobec_złotego(),
            *self.krzywa(),
            *self.blokery(blockers),
            *self.próbka(),
        ]

    def skład(self) -> list[str]:
        lasy = sum(self.verdicts.values())
        if not lasy:
            return []
        return [f"corpus: {lasy} forests", *wiersze_tabeli(self.verdicts.most_common(), lasy), ""]

    def wobec_złotego(self) -> list[str]:
        return [
            *_tabela_wzorca(
                self.agreements,
                "roles against the gold tree, on {ile} accepted sentences",
                self.unjudged,
                "accepted",
            ),
            *_tabela_wzorca(
                self.ocalenia,
                "the gold reading among the readings, on {ile} ambiguous sentences",
                self.bez_roli,
                "ambiguous",
            ),
            *_jak_głęboko(self.głębokości),
        ]


def _tabela_wzorca(
    counter: collections.Counter, nagłówek: str, bez_roli: int, status: str
) -> list[str]:
    """Tabela porównania z drzewem wzorcowym, a pod nią zdania, których nie było z czym.

    Obie takie tabele idą tędy, bo wiersz niemierzonych ma powiedzieć w obu to samo:
    mianownik zawężony przez samo porównanie czyta się jak mianownik całego wiersza.
    """
    if not counter:
        return []
    ile = sum(counter.values())
    wiersze = ["", f"{nagłówek.format(ile=ile)}:", *wiersze_tabeli(counter.most_common(), ile)]
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
    w_kubełkach: collections.Counter = collections.Counter()
    for numer, count in głębokości.items():
        w_kubełkach[kubełek(numer, GŁĘBOKOŚCI)] += count
    kolejne = [(nazwa, w_kubełkach[nazwa]) for nazwa in sorted(w_kubełkach, key=dolna_granica)]
    return [
        "",
        f"which reading the gold one is, on {ile} sentences where it survives:",
        *wiersze_tabeli(kolejne, ile),
        f"  the deepest is reading {max(głębokości)}",
    ]


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
    """
    zbudowany = las(GRAMMAR, list(segments))
    result = podsumuj(zbudowany)
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
) -> RaportZłoty:
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
    report = RaportZłoty(source=source, przykładów=keep_examples)
    for sentence in sentences:
        report.verdicts[sentence.verdict or "?"] += 1
        if not sentence.annotated:
            continue
        segments = segments_for(sentence, source)
        if not segments:
            report.skipped["no morphology"] += 1
            continue
        # Po morfologii, bo las bez ani jednego czytelnego węzła nie ma terminali
        # i przeczy temu kryterium tak samo jak las z dziurą w środku, a te dwie
        # odpowiedzi są dwiema różnymi robotami do zrobienia.
        if not sentence.całe:
            report.skipped["gold terminals do not tile the sentence"] += 1
            continue
        report.record(zmierz_zdanie(sentence, segments, source == "gold"))
    return report


# --------------------------------------------------------------------------- #
# Przebiegi
# --------------------------------------------------------------------------- #

#: Ile lasów bierze jeden kawałek pracy.
#:
#: Kawałek jest tym, co proces roboczy dostaje i za co oddaje `Raport`, więc przez
#: granicę procesu idzie licznik, a nie las, który go zbudował. Mniejszy kawałek
#: równa obciążenie — lasy różnią się rozmiarem o rzędy wielkości, bo długie
#: zdanie ma większy las — a częściej płaci za to przejście.
KAWAŁEK = 64


def _kawałek(ścieżki: Sequence[Path], source: str, keep_examples: int) -> RaportZłoty:
    """Odcinek listy plików, przeczytany i zmierzony tam, gdzie stoi."""
    return measure((read(path) for path in ścieżki), source, keep_examples)


def po_kawałkach(ścieżki: Sequence[Path], jobs: int, praca):
    """Podziel listę lasów na kawałki i oddaj to, co każdy z nich policzył.

    Dzieli pliki, a nie zdania, bo dopiero plik daje się oddać procesowi
    roboczemu bez przenoszenia przez granicę procesu tego, co się z niego czyta.

    Jeden proces liczy na miejscu, a nie w puli o jednym pracowniku, żeby został
    ślad wyjątku i profil, które granica procesu zabiera.

    Wołający dostaje listę w kolejności kawałków i sam ją składa, bo licznik,
    który z kawałka wraca, jest jego, a nie tego podziału. Sondy w tym pakiecie
    są drugim wołającym, i po to ten podział stoi osobno od scalania.
    """
    kawałki = [ścieżki[start : start + KAWAŁEK] for start in range(0, len(ścieżki), KAWAŁEK)]
    if jobs == 1:
        return [praca(kawałek) for kawałek in kawałki]
    with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as pula:
        return list(pula.map(praca, kawałki))


def scal(
    raporty: Iterable[RaportZłoty], source: str = "gold", keep_examples: int = 0
) -> RaportZłoty:
    """Złóż raporty kawałków w jeden.

    Morfologię nazywa wołający, choć każdy raport swoją niesie, bo katalog bez
    lasów nie oddaje żadnego raportu, a nagłówek wydruku i tak ją drukuje.
    """
    scalony = RaportZłoty(source=source, przykładów=keep_examples)
    for raport in raporty:
        scalony.dołóż(raport)
    return scalony


def przebieg(
    ścieżki: Sequence[Path],
    jobs: int,
    source: str = "gold",
    keep_examples: int = 0,
) -> RaportZłoty:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport."""
    praca = functools.partial(_kawałek, source=source, keep_examples=keep_examples)
    return scal(po_kawałkach(ścieżki, jobs, praca), source, keep_examples)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.pomiar",
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
        print(f"harness.pomiar: no such directory: {root}", file=sys.stderr)
        print("harness.pomiar: see docs/corpus.md for how to fetch the corpus", file=sys.stderr)
        return 2

    report = przebieg(
        pliki(root)[: args.limit],
        args.jobs,
        source=args.morphology,
        keep_examples=args.examples,
    )
    print(render(report, "Składnica", args.blockers))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
