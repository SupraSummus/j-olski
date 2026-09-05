"""Kolejka blokerów i krzywa pokrycia nad własnym tekstem.

Kto pisze po olsku, dostaje od ``olski-check`` werdykt na zdanie, a od tego
programu dwie liczby o całym pliku naraz. Pierwszą jest ranking form, na których
analiza staje: forma z czoła mówi, gdzie gramatyka nad tym dokumentem zawraca
najczęściej, i tyle z wiersza wynika, bo którą konstrukcję dopisać następną i ile
ona kupi, rozstrzyga się poza tym wydrukiem (docs/roadmap.md). Drugą jest krzywa
pokrycia po długości zdania, bo pokrycie nad zdaniem krótkim i nad długim rusza
się inaczej.

Sama liczba zdań przyjętych nie jest sygnałem, dopóki zdania dokumentu są długie:
takie zdanie ma po kilka zatrzymań naraz, więc pozycja dopisana do gramatyki
zdejmuje jedno z nich i zdania nie wypuszcza. Rusza się wtedy kolejka i krzywa, a nie
suma, i dlatego stoją tu obok niej (docs/pisanie-po-olsku.md).

Ten sam licznik nad bankiem drzew mierzy gramatykę, a nie tekst, i stoi po
drugiej stronie granicy pakietu (``harness/pomiar.py``): pyta o zgodność z
cudzym drzewem wzorcowym, czego proza nie ma z czym porównać, i czyta korpus,
którego autor sprawdzający własny plik nie pobiera. Wspólne mają liczniki i
wydruk, a nie przebieg, i dlatego tamten moduł bierze :class:`Wynik` oraz
:class:`Raport` stąd, zamiast trzymać drugą parę o tych nazwach.
"""

from __future__ import annotations

import argparse
import collections
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.document import SENTENCE_CLOSE
from olski.morph import Segment
from olski.parse import Result, las, podsumuj
from olski.segmentacja import licencjonowane, morphology, na_czym_stanęło, sentences
from olski.subset import GRAMMAR
from olski.wejście import proza

#: Length buckets for the coverage curve, as upper bounds in tokens.
BUCKETS = (5, 10, 20, 40)

#: What the report says when a sentence was derivable up to its last token and
#: still had no reading covering the whole of it.
NO_STRUCTURE = "(no structure over whole sentence)"

#: What the report says when an exclusion left the stopping form without a single
#: reading. The other rows name a part of speech to admit and this form has none,
#: the work being a lexical condition rather than a production (``po_przyimku``
#: and ``bez_licencji`` in ``olski/segmentacja.py``).
NO_LICENCE = "(no reading left by an exclusion)"


def kubełek(count: int, bounds: Sequence[int]) -> str:
    """Kubełek, w który ta liczba wpada, nazwany przedziałem, jaki obejmuje.

    Jedna funkcja na obie krzywe, bo różnią się granicami i niczym poza nimi.
    """
    previous = 1
    for bound in bounds:
        if count <= bound:
            return f"{bound}" if previous == bound else f"{previous}-{bound}"
        previous = bound + 1
    return f"{previous}+"


def dolna_granica(nazwa: str) -> int:
    """Granica, od której ten kubełek się zaczyna, czyli to, co go porządkuje.

    Nazwa kubełka zaczyna się od niej, bo tak ją składa :func:`kubełek`,
    i obie krzywe sortują się nią, żeby ta zależność miała jedno miejsce.
    """
    return int(nazwa.split("-")[0].rstrip("+"))


def wiersze_tabeli(pary: Sequence[tuple[str, int]], total: int) -> list[str]:
    """Wiersze tabeli w kolejności, w jakiej przyszły.

    Kolejność wybiera wołający, bo znaczy w każdej tabeli co innego:
    licznik czyta się od najliczniejszego, a kubełek od najmniejszej granicy.
    """
    lines = []
    for name, count in pary:
        share = f"{count / total:6.1%}" if total else "     -"
        lines.append(f"  {count:7} {share}  {name}")
    return lines


def bloker(segments: Sequence[Segment], result: Result) -> str | None:
    """The part of speech the analysis stopped on, for a rejected sentence.

    Exact under gold morphology, where a terminal has one reading because the
    annotators disambiguated it. Under live morphology the form usually has
    several and the row prefers one the grammar licenses: this row names what
    to admit next, so a reading olski never takes names the wrong work
    wherever the grammar already takes the word. The criterion has one owner,
    ``licencjonowane`` in ``olski/segmentacja.py``.

    Licensing orders those readings and does not filter them, because a form
    nothing licenses is what this queue is *for*: the compound future stops
    analyses under ``bedzie``, and that row is how the construction gets named
    (roadmap.md#kolejkę-ustawia-korpus-usterek-a-nie-kolejka-blokerów).
    Between the readings left standing
    the row stays arbitrary, and picking one keeps the ranking readable.

    Which form the analysis stopped on is one criterion with one owner,
    ``na_czym_stanęło`` in ``olski/segmentacja.py``, and this row asks it rather
    than holding a second: the sentence that runs to its closing mark with
    nothing deriving the whole of it is the other event and gets
    :data:`NO_STRUCTURE`. A form an exclusion emptied is a third and gets
    :data:`NO_LICENCE`, because the analysis did stop on a form and the other
    row says it stopped on none.

    It demands the stopping point, which a verdict asks the forest for on
    request (:func:`olski.parse.podsumuj`), so a run that did not ask raises
    here rather than naming some other form.
    """
    if not result.rejected:
        return None
    if result.furthest is None:
        raise ValueError(
            "bloker nazywa formę z miejsca zatrzymania, "
            "a ten przebieg o zatrzymanie nie pytał (podsumuj w olski/parse/)"
        )
    segment = na_czym_stanęło(list(segments), result.furthest)
    if segment is None:
        return NO_STRUCTURE
    czytania = licencjonowane(segment, GRAMMAR) or segment.readings
    return czytania[0].tag.pos if czytania else NO_LICENCE


@dataclass(frozen=True, kw_only=True)
class Wynik:
    """Co olski powiedział o jednym zdaniu.

    Pola są słowami kluczowymi, bo klasa ta ma podklasę o polach wymaganych
    (``Outcome`` w ``harness/pomiar.py``), a te stałyby po polach z wartością
    domyślną i bez tego by się nie zbudowały.
    """

    result: Result
    #: To, po czym rozbiór naprawdę szedł, bo to na tym stanął.
    #: Pod morfologią złotą i pod żywą są to dwie różne listy i pyta o nie
    #: ``Outcome`` w ``harness/pomiar.py``.
    segments: tuple[Segment, ...] = ()
    #: Zdanie takie, jak stoi w tekście, czyli to, co idzie do próbki pod wydrukiem.
    tekst: str = ""

    @property
    def status(self) -> str:
        return self.result.status

    @property
    def blocker(self) -> str | None:
        return bloker(self.segments, self.result)

    @property
    def długość(self) -> int:
        """Ile form liczy się temu zdaniu do krzywej pokrycia."""
        return len(self.segments)

    @property
    def klucz(self) -> str:
        """Pod jakim nagłówkiem stoi to zdanie w próbce pod wydrukiem."""
        return self.status


@dataclass
class Raport:
    """Counts over a run, and the examples that make them legible."""

    source: str = "live"
    #: Ile zdań zachować pod każdym nagłówkiem próbki. Pole, a nie argument
    #: zapisu i scalania naraz, bo obie te drogi muszą przyciąć tak samo,
    #: a dwie kopie liczby rozjeżdżają się na wywołaniu, które ją pominie.
    przykładów: int = 0
    statuses: collections.Counter = field(default_factory=collections.Counter)
    blockers: collections.Counter = field(default_factory=collections.Counter)
    lengths: dict[str, collections.Counter] = field(default_factory=dict)
    examples: dict[str, list[str]] = field(default_factory=dict)
    #: Sentences nothing was measured on, by why not. Reported rather than
    #: dropped, because a coverage figure that quietly excluded the hard
    #: sentences would be a coverage figure of the easy ones.
    skipped: collections.Counter = field(default_factory=collections.Counter)

    @property
    def measured(self) -> int:
        return sum(self.statuses.values())

    def record(self, wynik: Wynik) -> None:
        self.statuses[wynik.status] += 1
        blocker = wynik.blocker
        if blocker is not None:
            self.blockers[blocker] += 1
        self.lengths.setdefault(kubełek(wynik.długość, BUCKETS), collections.Counter())[
            wynik.status
        ] += 1
        kept = self.examples.setdefault(wynik.klucz, [])
        if len(kept) < self.przykładów:
            kept.append(wynik.tekst)

    def dołóż(self, inny: Raport) -> None:
        """Dołóż do tego raportu liczniki drugiego.

        Scalany raport wchodzi tu w kolejności, w jakiej mierzono, więc raport
        złożony jest tym samym raportem, co z jednego przebiegu nad całością.
        Przykłady sprawdzają to najostrzej: :meth:`record` zachowuje pierwsze
        zdania, jakie dostał, więc przykład wybrany przez to, który proces
        skończył pierwszy, byłby innym wydrukiem z tego samego korpusu.
        """
        self.statuses.update(inny.statuses)
        self.blockers.update(inny.blockers)
        self.skipped.update(inny.skipped)
        for nazwa, counts in inny.lengths.items():
            self.lengths.setdefault(nazwa, collections.Counter()).update(counts)
        for key, kept in inny.examples.items():
            zebrane = self.examples.setdefault(key, [])
            zebrane.extend(kept)
            del zebrane[self.przykładów :]

    # ----------------------------------------------------------------------- #
    # Wydruk
    # ----------------------------------------------------------------------- #

    def wiersze(self, blockers: int) -> list[str]:
        """Ciało wydruku, tabela po tabeli, w kolejności, w jakiej się je czyta.

        Kolejność jest tu wypisana, a nie wyprowadzona z tego, które liczniki są
        niepuste, bo podklasa wsuwa między te tabele swoje
        (``RaportZłoty`` w ``harness/pomiar.py``) i wtedy widać, gdzie stają.
        """
        return [
            *self.statusy(),
            *self.krzywa(),
            *self.blokery(blockers),
            *self.próbka(),
        ]

    def statusy(self) -> list[str]:
        wiersze = [
            f"olski over {self.measured} measured sentences:",
            *wiersze_tabeli(self.statuses.most_common(), self.measured),
        ]
        for reason, count in self.skipped.most_common():
            wiersze.append(f"  {count:7}          not measured: {reason}")
        return wiersze

    def krzywa(self) -> list[str]:
        if not self.lengths:
            return []
        wiersze = ["", "coverage by sentence length:"]
        for nazwa in sorted(self.lengths, key=dolna_granica):
            counts = self.lengths[nazwa]
            seen = sum(counts.values())
            valid = counts.get("valid", 0)
            #  Dwie liczby, bo pytają o nie dwa fotele: pokrycie jest tym, co
            #  olski obiecuje, a wyprowadzalność tym, co rusza się przy pozycji
            #  dopisanej do gramatyki.
            wyprowadzone = seen - counts.get("rejected", 0)
            wiersze.append(
                f"  {nazwa:>7} tokens: {valid:5}/{seen:<6} {valid / seen:6.1%} valid,"
                f" {wyprowadzone / seen:6.1%} with a reading"
            )
        return wiersze

    def blokery(self, ile: int) -> list[str]:
        if not self.blockers:
            return []
        blocked = sum(self.blockers.values())
        return [
            "",
            f"where the {blocked} rejected sentences stopped:",
            *wiersze_tabeli(self.blockers.most_common(ile), blocked),
        ]

    def próbka(self) -> list[str]:
        wiersze = []
        for key in sorted(self.examples):
            kept = self.examples[key]
            if not kept:
                continue
            wiersze += ["", f"{key} examples:"]
            wiersze += [f"  {text}" for text in kept]
        return wiersze


def scal(raporty: Iterable[Raport], przykładów: int = 0) -> Raport:
    """Złóż raporty plików w jeden."""
    scalony = Raport(przykładów=przykładów)
    for raport in raporty:
        scalony.dołóż(raport)
    return scalony


def nad_prozą(text: str, przykładów: int = 0) -> Raport:
    """Przebieg nad jednym tekstem, czyli nad prozą bez drzew wzorcowych.

    Fragment, którego nic nie punktuje jako zdania, wchodzi do wiersza
    niemierzonych, a nie do odrzuconych: nagłówek i pozycja listy dochodzą tu
    akapitem tak samo jak zdanie (``olski/markdown.py``), a policzone jako
    odrzucone mierzyłyby ekstrakcję zamiast podzbioru.
    """
    report = Raport(przykładów=przykładów)
    for zdanie in sentences(text):
        if not SENTENCE_CLOSE.search(zdanie):
            report.skipped["nic nie punktuje tego jako zdania"] += 1
            continue
        segmenty = morphology(zdanie)
        if not segmenty:
            report.skipped["no morphology"] += 1
            continue
        report.record(
            Wynik(
                result=podsumuj(las(GRAMMAR, list(segmenty))),
                segments=tuple(segmenty),
                tekst=zdanie,
            )
        )
    return report


def render(raport: Raport, nad: str, blockers: int = 12) -> str:
    """Wydruk raportu, wraz z nazwą tego, co przebieg czytał.

    Nazwa jest parametrem bez wartości domyślnej, a nie polem raportu: liczniki
    są nad plikiem i nad bankiem drzew te same, a różni je to, co stoi w
    nagłówku. Żadna nazwa nie jest przy tym dobra dla obu wołających, więc
    domyślna kłamałaby jednemu z nich w pierwszym wierszu wydruku.
    """
    return "\n".join([f"{nad}, {raport.source} morphology", "", *raport.wiersze(blockers)])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="olski-pokrycie",
        description="Zmierz pokrycie gramatyki nad plikami polskiej prozy.",
    )
    parser.add_argument(
        "ścieżki", nargs="+", metavar="ścieżka", help="pliki polskiej prozy albo dokumenty"
    )
    parser.add_argument("--blockers", type=int, default=12, help="how many blockers to rank")
    parser.add_argument("--examples", type=int, default=0, help="sentences to show per outcome")
    args = parser.parse_args(argv)

    ścieżki = [Path(nazwa) for nazwa in args.ścieżki]
    brakujące = [ścieżka for ścieżka in ścieżki if not ścieżka.is_file()]
    if brakujące:
        for ścieżka in brakujące:
            print(f"olski-pokrycie: nie ma takiego pliku: {ścieżka}", file=sys.stderr)
        return 2

    raporty = [
        nad_prozą(proza(ścieżka), args.examples) for ścieżka in ścieżki
    ]
    nad = ", ".join(ścieżka.name for ścieżka in ścieżki)
    print(render(scal(raporty, args.examples), nad, args.blockers))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
