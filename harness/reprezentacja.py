"""Ile zgłoszeń wieloznaczności znika w reprezentacji pośredniej i po świadkach przyłączeń.

Zgłoszenia bierze z pliku sądów (``próba/nkjp-sądy.txt``).
Zgłoszenie znika, gdy wszystkie czytania zdania schodzą do jednej reprezentacji.
Potem wyrażenia przyimkowe o kilku gospodarzach idą do świadków
z ``olski/rozstrzyganie.py`` wraz z kontekstem z pliku sądów,
a zostają reprezentacje zgodne z ich wskazaniami.
Sufit mówi, ile zgłoszeń znikłoby, gdyby świadkowie rozstrzygali każde przyłączenie przyimkowe.
Czytania idą wprost z lasu, bo :func:`olski.parse.parse` urywa listę
na :data:`olski.parse.MAX_READINGS`.

    python3 -m harness.reprezentacja próba/nkjp-sądy.txt
    python3 -m harness.reprezentacja próba/nkjp-sądy.txt --szczegóły
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from olski.parse import Przyłączenie, las
from olski.reprezentacja import Reprezentacja, Słowo, reprezentacje
from olski.rozstrzyganie import Rozstrzygnięcie, Sąsiedztwo, rozstrzygnij
from olski.segmentacja import morphology
from olski.subset import GRAMMAR, WYRAŻENIE_PRZYIMKOWE


@dataclass(frozen=True)
class Wpis:
    zdanie: str
    kontekst: tuple[str, ...]


def wpisy(sądy: str) -> Iterator[Wpis]:
    """Zgłoszenia wieloznaczności z pliku sądów wraz ze zdaniami przed nimi."""
    for blok in sądy.split("\n\n"):
        pola = [wiersz.split(": ", 1) for wiersz in blok.splitlines() if ": " in wiersz]
        if ["znalezisko", "wieloznaczne"] in pola:
            kontekst = tuple(wartość for klucz, wartość in pola if klucz == "kontekst")
            yield Wpis(dict(pola)["zdanie"], kontekst)


def sporne(różne: list[Reprezentacja]) -> dict[Słowo, Przyłączenie]:
    """Przyimek → przyłączenie, o które reprezentacje się spierają.

    Modyfikatorem jest przyimek ze swoimi zależnikami,
    bo świadek kontekstowy szuka w kontekście rzeczownika frazy.
    Przyimek, którego dwaj gospodarze mają tę samą formę, odpada,
    bo wskazanie gospodarza jest formą.
    """
    gospodarze: dict[Słowo, set[Słowo]] = defaultdict(set)
    zależniki: dict[Słowo, set[Słowo]] = defaultdict(set)
    for reprezentacja in różne:
        for krawędź in reprezentacja.krawędzie:
            if krawędź.rola == WYRAŻENIE_PRZYIMKOWE:
                gospodarze[krawędź.zależnik].add(krawędź.głowa)
            zależniki[krawędź.głowa].add(krawędź.zależnik)
    wynik = {}
    for przyimek, kandydaci in sorted(gospodarze.items()):
        formy = [kandydat.forma for kandydat in sorted(kandydaci)]
        if len(formy) > 1 and len(set(formy)) == len(formy):
            fraza = sorted({przyimek} | zależniki[przyimek])
            wynik[przyimek] = Przyłączenie(" ".join(s.forma for s in fraza), tuple(formy))
    return wynik


def zgodna(reprezentacja: Reprezentacja, wskazania: dict[Słowo, str]) -> bool:
    return all(
        krawędź.głowa.forma == wskazania[krawędź.zależnik]
        for krawędź in reprezentacja.krawędzie
        if krawędź.rola == WYRAŻENIE_PRZYIMKOWE and krawędź.zależnik in wskazania
    )


def bez_gospodarzy_przyimków(reprezentacja: Reprezentacja) -> tuple:
    """Reprezentacja, w której wyrażenie przyimkowe nie mówi, do czego doszło."""
    krawędzie = frozenset(
        (
            None if krawędź.rola == WYRAŻENIE_PRZYIMKOWE else krawędź.głowa,
            krawędź.rola,
            krawędź.zależnik,
        )
        for krawędź in reprezentacja.krawędzie
    )
    return reprezentacja.korzeń, krawędzie


def _z_lematem(słowo: Słowo) -> str:
    return f"{słowo.forma}/{'|'.join(słowo.lematy)}"


def różnice(pierwsza: Reprezentacja, druga: Reprezentacja) -> Iterator[str]:
    """Krawędzie jednej bez drugiej i odwrotnie.

    Słowo idzie z lematem, bo reprezentacje bywają różne samym leksemem tej samej formy.
    """
    strony = [
        ("-", pierwsza.krawędzie - druga.krawędzie),
        ("+", druga.krawędzie - pierwsza.krawędzie),
    ]
    for znak, krawędzie in strony:
        for krawędź in sorted(krawędzie):
            głowa, zależnik = _z_lematem(krawędź.głowa), _z_lematem(krawędź.zależnik)
            yield f"{znak} {głowa} —{krawędź.rola}→ {zależnik}"


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.reprezentacja",
        description="Policz zgłoszenia wieloznaczności, które znikają w reprezentacji pośredniej.",
    )
    parser.add_argument("sądy", type=Path, help="plik sądów, na przykład próba/nkjp-sądy.txt")
    parser.add_argument(
        "--szczegóły",
        action="store_true",
        help="wypisz wskazania świadków i krawędzie, którymi różnią się dwie pozostałe",
    )
    args = parser.parse_args()
    liczby: Counter[str] = Counter()
    świadkowie: Counter[str] = Counter()
    for wpis in wpisy(args.sądy.read_text(encoding="utf-8")):
        czytania = list(las(GRAMMAR, morphology(wpis.zdanie)).czytania())
        różne = reprezentacje(czytania)
        spory = sporne(różne)
        odpowiedzi = rozstrzygnij(spory.values(), sąsiedztwo=Sąsiedztwo(wpis.kontekst))
        wskazane = {
            przyimek: odpowiedź
            for przyimek, odpowiedź in zip(spory, odpowiedzi, strict=True)
            if isinstance(odpowiedź, Rozstrzygnięcie)
        }
        zostaje = [r for r in różne if zgodna(r, {p: o.gospodarz for p, o in wskazane.items()})]
        print(f"{len(czytania):4d} → {len(różne):4d} → {len(zostaje):4d}  {wpis.zdanie}")
        if args.szczegóły:
            for odpowiedź in wskazane.values():
                print(
                    f"        {odpowiedź.świadek}: {odpowiedź.modyfikator} → {odpowiedź.gospodarz}"
                )
            if len(zostaje) > 1:
                for wiersz in różnice(*zostaje[:2]):
                    print(f"        {wiersz}")
        liczby.update(
            zgłoszeń=1,
            czytań=len(czytania),
            reprezentacji=len(różne),
            po_świadkach=len(zostaje),
            znika=len(różne) == 1,
            znika_po_świadkach=len(zostaje) == 1,
            sporów=len(spory),
            sufit=len(set(map(bez_gospodarzy_przyimków, różne))) == 1,
        )
        świadkowie.update(odpowiedź.świadek for odpowiedź in wskazane.values())
    print(
        f"zgłoszeń: {liczby['zgłoszeń']}; znika: {liczby['znika']}, "
        f"po świadkach: {liczby['znika_po_świadkach']}, sufit: {liczby['sufit']}; "
        f"czytań: {liczby['czytań']} → reprezentacji: {liczby['reprezentacji']} "
        f"→ po świadkach: {liczby['po_świadkach']}"
    )
    wskazań = ", ".join(f"{nazwa} {ile}" for nazwa, ile in sorted(świadkowie.items()))
    print(f"spornych przyłączeń: {liczby['sporów']}; wskazań: {wskazań or 'brak'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
