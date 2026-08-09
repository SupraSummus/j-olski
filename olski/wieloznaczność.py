"""Ile zdań rejestru czyta się dwojako w samej polszczyźnie.

Kryterium wyjścia toru gramatycznego żąda jednego czytania od zdania, które w
polszczyźnie ma dwa. Rozwidlenie, które z tego wychodzi, wraz z tym, co pomiar
stąd nad nim rozstrzygnął, trzyma docs/open-questions.md; brakowało mu liczby i
tę liczbę ten moduł podaje.

To jest pomiar rejestru, a nie gramatyki, i tym różni się od olski/coverage.py,
tak samo jak olski/attachment.py obok. Liczone są pozycje w tekście, a nie
werdykty nad nim, więc zdanie liczy się i wtedy, gdy gramatyka nie umie go
rozebrać wcale. Inaczej się nie da: takich zdań jest w tym rejestrze większość,
a to o nie właśnie pytanie idzie.

Klasy są dwie i obie stoją w tamtym pytaniu wraz ze swoim zdaniem.

Przyłączenie: wyrażenie przyimkowe stoi tuż za grupą imienną, a czasownik przed
nim, więc dochodzi do jednego albo do drugiego. Populacja jest ta sama, którą
olski/attachment.py liczy nad Składnicą, przełożona z cudzych drzew na formy:
tam grupę imienną nazywa węzeł, a tutaj część mowy.

Synkretyzm: dwie grupy imienne czytają się i w mianowniku, i w bierniku, a
czasownik przy nich bierze dopełnienie, więc SVO i OVS stoją oba do wzięcia.
Dwa warunki zdejmują z tej klasy zdanie, które polszczyzna czyta raz, i żaden nie
jest ozdobą: czasownika bez biernika nie liczy leksykon walencyjny, a grupy,
która z orzeczeniem nie zgadza się co do liczby i rodzaju, nie liczy sama zgoda.

Liczba jest górnym oszacowaniem i myli się w jedną stronę. Grupą imienną jest tu
ciąg form, a nie węzeł, więc przymiotnik orzecznikowy liczy się jak koniec grupy,
a zdanie złożone daje naraz pozycje z dwóch zdań składowych. Populację zwęża
ponadto to, czego ten moduł nie widzi: wyrażenie, którego czasownik żąda swoim
schematem, stoi w tej pozycji i do wyboru nie stoi, a ile go jest, mierzy nad
Składnicą docs/subset.md. Wchodzi tu wreszcie każde czytanie, które słownik
oferuje, a polszczyzna go nie ma: liczone jest to, co zostawia ``admissible`` w
olski/subset.py, a zostawia ono nazwisko nieodmienne z formy ``Nowy`` i grę z
formy ``go``. Obie klasy są otwarte i obie mają swoje miejsce — pierwsza jest
etapem 3 z docs/roadmap.md, drugą trzyma TODO.md — więc ten pomiar ruszy się,
kiedy się zamkną.
"""

from __future__ import annotations

import argparse
import collections
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.attachment import CZASOWNIK
from olski.document import SENTENCE_CLOSE
from olski.morph import Reading, Segment
from olski.subset import (
    KOPULA,
    RAMA_BEZ_BIERNIKA,
    WALENCJA,
    WALENCJA_ZWROTNA,
    morphology,
    sentences,
)

#: Części mowy, którymi grupa imienna może się skończyć. Głowa i to, co stoi za
#: nią: przymiotnik idzie w polszczyźnie i przed rzeczownikiem, i po nim.
KONIEC_NP = frozenset({"subst", "depr", "ger", "num", "numcol", "adj", "ppas", "pact"})

#: Sama głowa. Przymiotnik grupą nie jest, więc jako kandydat na podmiot albo
#: dopełnienie nie staje: policzony osobno dawałby dwie grupy tam, gdzie
#: ``nowy program`` jest jedną.
GŁOWA_NP = frozenset({"subst", "depr", "ger", "num", "numcol"})

#: Formy, przy których stoi podmiot i dopełnienie naraz, czyli te, wobec których
#: pytanie o SVO i OVS w ogóle stoi. Imiesłów i bezokolicznik są tu wyłączone,
#: choć CZASOWNIK je liczy: podmiotu przy sobie nie mają.
OSOBOWY = frozenset({"fin", "praet", "bedzie", "impt", "winien"})

#: Lematy, którym leksykon odmawia dopełnienia w bierniku, osobno dla formy z
#: cząstką ``się`` i bez niej, bo są to dwa czasowniki i biorą co innego. Kopula
#: idzie do gołych, bo to ona zabrała leksykonowi swoje lematy. Zdanie z takim
#: czasownikiem czytania OVS nie ma: nie ma dopełnienia, którym pierwsza grupa
#: miałaby stanąć.
BEZ_BIERNIKA = frozenset(WALENCJA[RAMA_BEZ_BIERNIKA].split("|") + KOPULA.split("|"))
BEZ_BIERNIKA_ZWROTNE = frozenset(WALENCJA_ZWROTNA[RAMA_BEZ_BIERNIKA].split("|"))

#: Znaki, po których ``_człony`` tnie zdanie na składowe.
GRANICA = frozenset({",", ";", ":", "–", "—", "-"})

PRZYŁĄCZENIE = "przyłączenie"
SYNKRETYZM = "synkretyzm"
KLASY = (PRZYŁĄCZENIE, SYNKRETYZM)


@dataclass(frozen=True)
class Miejsce:
    """Jedna pozycja, w której polszczyzna daje dwa czytania."""

    klasa: str
    #: Formy, na których ta pozycja stoi: przyimek dla jednej klasy, a obie grupy
    #: imienne dla drugiej. Bez nich liczba nie ma czym się wytłumaczyć.
    formy: tuple[str, ...]


def miejsca(zdanie: str) -> list[Miejsce]:
    """Pozycje obu klas w jednym zdaniu, tak jak stoją."""
    segments = morphology(zdanie)
    return _przyłączenia(segments) + _synkretyzm(segments)


def _przyłączenia(segments: list[Segment]) -> list[Miejsce]:
    kończy_się = {segment.end for segment in segments if _ma(segment, KONIEC_NP)}
    czasowniki = [segment.start for segment in segments if _ma(segment, CZASOWNIK)]
    return [
        Miejsce(PRZYŁĄCZENIE, (segment.form,))
        for segment in segments
        if _ma(segment, {"prep"})
        and segment.start in kończy_się
        and any(start < segment.start for start in czasowniki)
    ]


def _synkretyzm(segments: list[Segment]) -> list[Miejsce]:
    """Czy zdanie stawia dwie grupy, z których każda staje podmiotem i dopełnieniem.

    Dwa warunki poza samym przypadkiem, i żaden nie jest ozdobą. Zgoda:
    ``Program zapisuje ustawienia`` ma obie grupy obojętne na przypadek i jedno
    czytanie mimo to, bo orzeczenie stoi w liczbie pojedynczej, a druga grupa
    jest mnoga i podmiotem być nie może. Jeden człon: obie grupy mają stanąć przy
    tym samym orzeczeniu, bo ``Typ obiektu – liść drzewa, czyli kategoria, która
    nie posiada podkategorii`` ma je w dwóch zdaniach składowych i o wyborze
    między SVO a OVS nie mówi nic.
    """
    zwrotne = any(reading.lemma == "się" for segment in segments for reading in segment.readings)
    for człon in _człony(segments):
        for orzeczenie in (r for segment in człon for r in segment.readings):
            if orzeczenie.tag.pos not in OSOBOWY:
                continue
            odmawia = BEZ_BIERNIKA_ZWROTNE if zwrotne else BEZ_BIERNIKA
            if orzeczenie.lemma in odmawia:
                continue
            grupy = [
                segment.form
                for segment in człon
                if any(_obojętny(reading, orzeczenie) for reading in segment.readings)
            ]
            if len(grupy) >= 2:
                return [Miejsce(SYNKRETYZM, tuple(grupy))]
    return []


def _człony(segments: list[Segment]) -> list[list[Segment]]:
    """Zdanie pocięte tam, gdzie znak je punktuje.

    Cięcie idzie po interpunkcji i po niczym więcej, bo spójnik podrzędny da się
    od współrzędnego odróżnić dopiero rozbiorem, a tego ten pomiar nie ma. Myli
    się przez to w stronę mniejszej liczby: dywiz wewnątrz formy tnie tak samo
    jak myślnik między zdaniami, a człon urwany za wcześnie traci parę, której
    nie miał gdzie zestawić.
    """
    granice = sorted(segment.start for segment in segments if segment.form in GRANICA)
    człony: dict[int, list[Segment]] = {}
    for segment in segments:
        if segment.form in GRANICA:
            continue
        numer = sum(1 for granica in granice if granica < segment.start)
        człony.setdefault(numer, []).append(segment)
    return list(człony.values())


def _obojętny(reading: Reading, orzeczenie: Reading) -> bool:
    """Czy ta głowa nie odróżnia mianownika od biernika i zgadza się z orzeczeniem.

    Nieodmienne czytanie spełnia pierwsze z drugiej strony: notacja rejestru stoi
    w każdym przypadku, więc stoi i w tych dwóch. Rodzaj wchodzi do zgody tylko
    wtedy, gdy orzeczenie go niesie, bo forma osobowa czasu teraźniejszego nie
    niesie go wcale.
    """
    if reading.tag.pos not in GŁOWA_NP:
        return False
    if not {"nom", "acc"} <= reading.tag.get("case"):
        return False
    if not reading.tag.get("number") & orzeczenie.tag.get("number"):
        return False
    rodzaj = orzeczenie.tag.get("gender")
    return not rodzaj or bool(reading.tag.get("gender") & rodzaj)


def _ma(segment: Segment, części: Iterable[str]) -> bool:
    return any(reading.tag.pos in części for reading in segment.readings)


@dataclass
class Raport:
    """Ile zdań niesie którą klasę, i ile pozycji przypada na zdanie."""

    zdania: int = 0
    #: Nagłówek, pozycja listy i wiersz tabeli. Kryterium wyjścia ich nie liczy,
    #: więc nie liczy ich i ten pomiar, ale mówi, ile ich minął.
    fragmenty: int = 0
    zdania_z: collections.Counter = field(default_factory=collections.Counter)
    którakolwiek: int = 0
    #: Rozkład liczby przyłączeń w zdaniu: jedno zdanie bywa wieloznaczne kilka
    #: razy naraz, a wtedy czytań ma nie dwa, tylko dwa do potęgi.
    przyłączeń: collections.Counter = field(default_factory=collections.Counter)
    #: Zdania trafione, każde wraz z formami, na których stanęło.
    przykłady: dict[str, list[tuple[str, tuple[str, ...]]]] = field(default_factory=dict)

    def record(self, zdanie: str, found: Sequence[Miejsce]) -> None:
        if not SENTENCE_CLOSE.search(zdanie):
            self.fragmenty += 1
            return
        self.zdania += 1
        klasy = {miejsce.klasa for miejsce in found}
        for klasa in klasy:
            self.zdania_z[klasa] += 1
            formy = tuple(f for m in found if m.klasa == klasa for f in m.formy)
            self.przykłady.setdefault(klasa, []).append((zdanie, formy))
        self.którakolwiek += bool(klasy)
        self.przyłączeń[sum(miejsce.klasa == PRZYŁĄCZENIE for miejsce in found)] += 1


def measure(texts: Iterable[str]) -> Raport:
    report = Raport()
    for text in texts:
        for zdanie in sentences(text):
            report.record(zdanie, miejsca(zdanie))
    return report


def render(report: Raport, przykłady: int = 0) -> str:
    lines = [f"{report.zdania} zdań, obok {report.fragmenty} fragmentów, których nic nie punktuje"]
    if not report.zdania:
        return lines[0]
    lines += ["", "zdań z pozycją, w której polszczyzna daje dwa czytania:"]
    for klasa in KLASY:
        liczba = report.zdania_z[klasa]
        lines.append(f"  {liczba:6} {liczba / report.zdania:6.1%}  {klasa}")
    razem = report.którakolwiek
    lines.append(f"  {razem:6} {razem / report.zdania:6.1%}  którakolwiek")
    lines += ["", "przyłączeń nierozstrzygniętych w zdaniu:"]
    for ile, liczba in sorted(report.przyłączeń.items()):
        lines.append(f"  {ile:6} {liczba:6}")
    for klasa in KLASY:
        for zdanie, formy in _próbka(report.przykłady.get(klasa, ()), przykłady):
            lines.append(f"\n{klasa} [{', '.join(formy)}]: {zdanie}")
    return "\n".join(lines)


def _próbka(trafione: Sequence[tuple], ile: int) -> list[tuple]:
    """Rozrzut po całej liście, a nie jej głowa.

    Kto te zdania czyta, czyta je po to, żeby powiedzieć, czy polszczyzna ma tam
    dwa czytania, a głowa listy jest akapitami otwierającymi pierwszy dokument i
    o korpusie nie mówi nic. Krok jest ilorazem, więc próbka jest ta sama przy
    każdym przebiegu i daje się przeczytać drugi raz po tym samym.
    """
    if ile <= 0 or not trafione:
        return []
    if ile >= len(trafione):
        return list(trafione)
    krok = len(trafione) / ile
    return [trafione[int(i * krok)] for i in range(ile)]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m olski.wieloznaczność",
        description="Policz zdania, które czytają się dwojako w samej polszczyźnie.",
    )
    parser.add_argument("paths", nargs="+", help="pliki zwykłego tekstu")
    parser.add_argument("--przykłady", type=int, default=0, help="ile zdań wypisać na klasę")
    args = parser.parse_args(argv)

    texts = []
    for path in args.paths:
        try:
            texts.append(Path(path).read_text(encoding="utf-8"))
        except OSError as błąd:
            print(f"olski.wieloznaczność: {błąd}", file=sys.stderr)
            return 2
    print(render(measure(texts), args.przykłady))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
