"""Czego suma cennika nie rozstrzyga, czyli które ciała konkurują za darmo.

Kolejność czytań ustala suma cennika po całym drzewie, a nad przeszło połową
zdań wieloznacznych nie ustala jej wcale: najtańszą sumę ma tam kilka czytań i
o pierwszym miejscu rozstrzyga dopiero cięcie. ``harness/skala.py`` liczy, jak
często to pada; ta sonda mówi, między czym, i pyta się jej przed dopisaniem
pozycji do cennika.

Wydruk czyta się parami ciał, a nie liczbą pod nimi: nie każda konkurencja
czeka na cenę, bo część z nich olski rozmyślnie zostawia czytelnikowi, a cena
postawiona nad taką parą odwraca decyzję, zamiast zapełniać dziurę. Które to
pary i czemu licznik produkcji nieopłaconych na to pytanie nie odpowiada, mówi
docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie.

Ciało nazywa tu symbol wraz z etykietami córek, bez rozpiętości i bez cech: dwa
czytania jednego napisu różnią się czasem samym miejscem cięcia, a wtedy para
ciał wychodzi pusta i takie zdania stoją w wydruku pod osobną liczbą.

    python3 -m harness.remis Składnica-frazowa-180723/
    python3 -m harness.remis README.md
"""

from __future__ import annotations

import argparse
import collections
import functools
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.corpus import read
from harness.komenda import Komenda, uruchom
from harness.pomiar import po_kawałkach
from olski import cennik
from olski.morph import Segment
from olski.parse import las, podsumuj
from olski.parse.czytanie import Leaf, Node
from olski.segmentacja import morphology, sentences
from olski.subset import GRAMMAR
from olski.wejście import proza
from olski.werdykt.wykazy import koszty_drzewa

#: Ile zdań pokazać pod każdą konkurencją. Para ciał mówi, co z czym stanęło, i
#: nie mówi, o jaki napis poszło, a bez napisu nie da się rozstrzygnąć, czy ta
#: para czeka na cenę, czy jest odmową wyboru.
PRZYKŁADY = 2

#: Ile konkurencji wypisać. Ogon jest długi i pojedynczy, bo ciała schodzą się w
#: nim po kilka naraz, a decyzję podejmuje się nad czołem tabeli.
KONKURENCJE = 20

#: Czym jest w wydruku córka będąca słowem. Terminal etykiety nie ma, a bez
#: znaku ciało dwuczłonowe wyglądałoby jak jednoczłonowe.
SŁOWO = "·"

#: Symbol i etykiety jego córek, czyli ciało bez rozpiętości i bez cech.
Ciało = tuple[str, tuple[str, ...]]

#: Ciała, którymi dwa czytania się różnią, w kolejności alfabetycznej.
Konkurencja = tuple[Ciało, ...]

#: Zdanie gotowe do rozbioru: napis wraz z segmentami, którymi je podzielono.
#: Bank drzew i proza różnią się tym i tylko tym (:func:`zmierz`).
Zdanie = tuple[str, Sequence[Segment]]


def ciała(drzewo: Node) -> collections.Counter[Ciało]:
    """Ciała, którymi to drzewo stoi, każde wraz z liczbą wystąpień.

    Licznikiem, a nie zbiorem, bo czytanie bywa tym samym ciałem postawionym
    raz więcej: ciąg współrzędny dłuższy o jeden człon różni się od krótszego
    samą liczbą, a zbiór powiedziałby, że nie różnią się niczym.
    """
    ile: collections.Counter[Ciało] = collections.Counter()
    do_obejścia: list[Node] = [drzewo]
    while do_obejścia:
        węzeł = do_obejścia.pop()
        ile[(węzeł.label, tuple(_etykieta(córka) for córka in węzeł.children))] += 1
        do_obejścia.extend(córka for córka in węzeł.children if isinstance(córka, Node))
    return ile


def _etykieta(córka: Leaf | Node) -> str:
    return SŁOWO if isinstance(córka, Leaf) else córka.label


def konkurencja(pierwsze: Node, drugie: Node) -> Konkurencja:
    """Ciała, które stoją w jednym z tych czytań i nie stoją w drugim.

    Kolejność jest alfabetyczna, a nie kolejnością obejścia drzewa: para służy
    tu za klucz licznika, więc dwa zdania o tej samej parze mają dać ten sam
    klucz, choćby ciała stały w nich w innej kolejności.
    """
    tu, tam = ciała(pierwsze), ciała(drugie)
    return tuple(sorted(set((tu - tam).elements()) | set((tam - tu).elements())))


@dataclass
class Raport:
    """Co przebieg policzył, wraz ze zdaniami, na których widać konkurencję."""

    ile_przykładów: int = PRZYKŁADY
    #: Zdania, które olski czyta; zdanie odrzucone nie ma czytań do porównania.
    czytane: int = 0
    #: Zdania o kilku czytaniach, czyli mianownik.
    wieloznaczne: int = 0
    #: Zdania, w których dwa najtańsze czytania mają jedną sumę.
    remis: int = 0
    #: Zdania remisu, których czytania różnią się samym miejscem cięcia, więc
    #: para ciał wychodzi pusta.
    samo_cięcie: int = 0
    #: Konkurencja → ile zdań ją ma.
    konkurencje: collections.Counter[Konkurencja] = field(default_factory=collections.Counter)
    #: Konkurencja → zdania, na których ją widać.
    przykłady: dict[Konkurencja, list[str]] = field(default_factory=dict)

    def zapisz(self, tekst: str, czytania: Sequence[Node]) -> None:
        """Dopisz jedno zdanie wraz z jego czytaniami, od najtańszego."""
        self.czytane += 1
        if len(czytania) < 2:
            return
        self.wieloznaczne += 1
        pierwsze, drugie = czytania[0], czytania[1]
        if cennik.suma(koszty_drzewa(pierwsze)) != cennik.suma(koszty_drzewa(drugie)):
            return
        self.remis += 1
        para = konkurencja(pierwsze, drugie)
        if not para:
            self.samo_cięcie += 1
            return
        self.konkurencje[para] += 1
        zachowane = self.przykłady.setdefault(para, [])
        if len(zachowane) < self.ile_przykładów:
            zachowane.append(tekst)

    def dołóż(self, inny: Raport) -> None:
        self.czytane += inny.czytane
        self.wieloznaczne += inny.wieloznaczne
        self.remis += inny.remis
        self.samo_cięcie += inny.samo_cięcie
        self.konkurencje.update(inny.konkurencje)
        for para, zdania in inny.przykłady.items():
            zachowane = self.przykłady.setdefault(para, [])
            zachowane.extend(zdania[: self.ile_przykładów - len(zachowane)])


def zmierz(zdania: Iterable[Zdanie], przykłady: int = PRZYKŁADY) -> Raport:
    """Rozbierz te zdania i policz, czego suma w nich nie rozstrzyga.

    Wieloznaczność zdania czyta się tu z listy czytań, a nie z ``Result.ile``:
    sonda pyta o dwa najtańsze, a lista urywa się na ``MAX_READINGS``, więc
    zdanie o lesie większym od tej granicy nie kosztuje tu nic ponad zdanie
    o dwóch czytaniach.
    """
    raport = Raport(przykłady)
    for tekst, segmenty in zdania:
        wynik = podsumuj(las(GRAMMAR, segmenty), zatrzymanie=False)
        if wynik.readings:
            raport.zapisz(tekst, wynik.readings)
    return raport


def z_banku(ścieżki: Sequence[Path]) -> Iterator[Zdanie]:
    """Zdania tych lasów pod morfologią wzorcową.

    Wzorcową, bo pozycja morfologii jest pod nią zerem przy każdej formie
    (``olski/rejestr.py``), więc remis mówi tu o samej gramatyce, wyjętej spod
    wieloznaczności analizatora.
    """
    for ścieżka in ścieżki:
        zdanie = read(ścieżka)
        if zdanie.annotated and zdanie.całe and zdanie.segments:
            yield zdanie.text, list(zdanie.segments)


def z_prozy(teksty: Iterable[str]) -> Iterator[Zdanie]:
    """Zdania tych tekstów pod morfologią żywą."""
    for tekst in teksty:
        for napis in sentences(tekst):
            yield napis, morphology(napis)


def przebieg(ścieżki: Sequence[Path], jobs: int, przykłady: int = PRZYKŁADY) -> Raport:
    """Zmierz bank drzew w puli procesów i złóż jeden raport."""
    scalony = Raport(przykłady)
    praca = functools.partial(_kawałek, przykłady=przykłady)
    for kawałek in po_kawałkach(ścieżki, jobs, praca):
        scalony.dołóż(kawałek)
    return scalony


def _kawałek(ścieżki: Sequence[Path], przykłady: int) -> Raport:
    return zmierz(z_banku(ścieżki), przykłady)


def wydruk(raport: Raport, nagłówek: str, konkurencji: int = KONKURENCJE) -> str:
    """Ile razy suma nie rozstrzyga, a pod tym między czym."""
    wiersze = [
        nagłówek,
        "",
        f"zdań czytanych: {raport.czytane}, wieloznacznych: {raport.wieloznaczne}",
        f"suma nie rozstrzyga: {raport.remis}",
        f"  różni je samo cięcie: {raport.samo_cięcie}",
    ]
    for para, ile in _po_kolei(raport.konkurencje, konkurencji):
        wiersze += ["", f"  {ile}×"]
        wiersze += [f"      {symbol} → {' '.join(córki)}" for symbol, córki in para]
        wiersze += [f"    · {zdanie}" for zdanie in raport.przykłady.get(para, ())]
    return "\n".join(wiersze)


def _po_kolei(
    ile: collections.Counter[Konkurencja], konkurencji: int
) -> list[tuple[Konkurencja, int]]:
    """Konkurencje od najczęstszej; remis liczby rozstrzyga sama para.

    Bez tego rozstrzygnięcia dwa przebiegi wypisują konkurencje o równej liczbie
    w kolejności, w jakiej trafiły do licznika, czyli w kolejności plików.
    """
    return sorted(ile.items(), key=lambda wpis: (-wpis[1], wpis[0]))[:konkurencji]


def _korpus(ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    return wydruk(przebieg(ścieżki, args.jobs, args.przykłady), "Składnica")


def _proza(wejścia: Sequence[tuple[Path, str]], args: argparse.Namespace) -> str:
    raport = zmierz(z_prozy(proza(ścieżka) for ścieżka, _ in wejścia), args.przykłady)
    return wydruk(raport, ", ".join(ścieżka.name for ścieżka, _ in wejścia))


KOMENDA = Komenda(
    nazwa="harness.remis",
    opis="Wypisz ciała, które konkurują tam, gdzie suma cennika nie rozstrzyga.",
    przykłady=PRZYKŁADY,
    korpus=_korpus,
    proza=_proza,
    pula=True,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
