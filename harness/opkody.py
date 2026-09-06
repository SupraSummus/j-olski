"""Ile opkodów wykonuje rozbiór tej prozy: miernik, którego maszyna nie rusza.

Zegar rusza się między przebiegami o kilkanaście procent,
więc zmianę wartą mniej widać na nim dopiero po powtórzeniach.
Liczba wykonanych opkodów rozrzutu nie ma:
jest ta sama w każdym przebiegu i w każdym procesie,
więc dwa drzewa robocze porównuje się jednym przebiegiem każdego.

    git worktree add ../baza HEAD
    diff <(cd ../baza && python3 -m harness.opkody README.md) <(python3 -m harness.opkody README.md)

Mierzy przez to pracę maszyny wirtualnej Pythona, a nie czas: opkod tani i opkod
drogi liczą się jednakowo, więc zmiana przenosząca robotę do C wychodzi tu lepiej
niż na zegarze.

Licznik chodzi pod ``sys.settrace``, więc przebieg trwa rząd wielkości dłużej niż
zwykły; garść zdań wystarcza, bo powtarzać go nie trzeba.

Hasze napisów są losowane przy starcie, a kolejność zbioru rusza kolejność, w jakiej
rozbiór odwiedza produkcje, więc oba przebiegi żądają ``PYTHONHASHSEED=0``.
Liczy się przy tym drugi przebieg tych samych zdań: pierwszy zapełnia pamięci
podręczne, które gramatyka liczy leniwie, i wychodzi o parę procent wyższy.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from harness import proza_repozytorium
from olski.segmentacja import morphology, sentences
from olski.wejście import proza
from olski.werdykt import werdykt

#: Zmienna, którą wyłącza się losowanie haszy. Nazwa stoi tu raz,
#: bo pyta o nią i warunek, i komunikat, który go tłumaczy.
ZIARNO = "PYTHONHASHSEED"


def policz(robota: Callable[[], object]) -> int:
    """Ile opkodów wykonuje ta robota, wraz ze wszystkim, co ona woła.

    Ślad zakłada się na każdą ramkę, bo ``f_trace_opcodes`` jest własnością ramki,
    a nie przebiegu, i ramka bez niego zdarzeń o opkodach nie wydaje.
    """
    licznik = 0

    def ślad(ramka, zdarzenie, arg):
        nonlocal licznik
        ramka.f_trace_opcodes = True
        if zdarzenie == "opcode":
            licznik += 1
        return ślad

    sys.settrace(ślad)
    try:
        robota()
    finally:
        sys.settrace(None)
    return licznik


def opkody(ścieżki: Sequence[Path], ile: int) -> int:
    """Opkody rozbioru pierwszych ``ile`` zdań tej prozy, przy zapełnionych pamięciach."""
    tekst = "\n\n".join(proza(ścieżka) for ścieżka in ścieżki)
    pary = [(zdanie, morphology(zdanie)) for zdanie in list(sentences(tekst))[:ile]]

    def przebieg() -> None:
        for zdanie, segmenty in pary:
            werdykt(zdanie, segmenty)

    przebieg()
    return policz(przebieg)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.opkody",
        description="ile opkodów wykonuje rozbiór tej prozy, do porównania między drzewami",
    )
    parser.add_argument(
        "ścieżki",
        nargs="*",
        metavar="ścieżka",
        help="pliki z prozą; bez nich cała proza repozytorium",
    )
    parser.add_argument(
        "--zdań",
        type=int,
        default=100,
        help="ile pierwszych zdań rozebrać (domyślnie 100)",
    )
    args = parser.parse_args(argv)
    if os.environ.get(ZIARNO) != "0":
        print(
            f"{ZIARNO}=0 nie jest ustawione, więc liczba zależy od losowania haszy",
            file=sys.stderr,
        )
        return 2
    ścieżki = [Path(nazwa) for nazwa in args.ścieżki] or proza_repozytorium()
    print(opkody(ścieżki, args.zdań))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
