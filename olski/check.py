"""Checking a text against the grammar, from the command line."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path

from olski.rozstrzyganie import PUSTE, Rozstrzygnięcie, domyślni, rozstrzygnij, sąsiedztwa
from olski.subset import Podsumowanie, Verdict, check, dalsze_zatrzymania

STATUS_WIDTH = 9

#: Znak przed wierszem warstwy rozstrzygającej. Wiersz ten nie jest werdyktem
#: i nie może się na werdykt czytać, bo werdykt mówi, co olski o zdaniu wie,
#: a ten wiersz, co osobna warstwa o nim zgaduje (``olski/rozstrzyganie.py``).
DOMYSŁ = "?"


def _rozstrzygnięcia(verdict, świadkowie, sąsiedztwo) -> list[str]:
    """Wiersze warstwy rozstrzygającej, po jednym na przyłączenie, albo żaden.

    Milczenie warstwy zostaje nienazwane, bo werdykt nad tym zdaniem nazwał już
    to przyłączenie i powiedział o nim to samo: że nierozstrzygnięte.
    """
    return [
        f"{DOMYSŁ} „{o.modyfikator}” → „{o.gospodarz}”: {o.powód}"
        for o in rozstrzygnij(verdict.result.przyłączenia, świadkowie, sąsiedztwo)
        if isinstance(o, Rozstrzygnięcie)
    ]


def _role(streszczenie: dict[str, str]) -> str:
    return ", ".join(f"{rola}: {wypełnienie}" for rola, wypełnienie in streszczenie.items())


def _czytanie(streszczenie: tuple[dict[str, str], ...], wcięcie: str) -> Iterator[str]:
    """Wiersze jednego czytania: po jednym na zdanie składowe.

    Kreska otwiera czytanie, a składowe następne stoją pod nim bez niej,
    bo lista liczy czytania: kreska przy każdym składowym mówiłaby,
    że zdanie o dwóch składowych i jednym czytaniu ma czytania dwa.
    """
    for numer, składowe in enumerate(streszczenie):
        yield f"{wcięcie}- {_role(składowe)}" if numer == 0 else f"{wcięcie}  {_role(składowe)}"


def _czytania(verdict: Verdict) -> Iterator[str]:
    """Wiersze, którymi ``--readings`` mówi, co stoi w której roli.

    Za streszczeniami zdania idą streszczenia konstytuentu, którego
    wieloznaczność streszczenie zdania zostawia nienazwaną
    (``Verdict.rozbieżne`` w ``olski/subset.py``).
    """
    for streszczenie in verdict.readings:
        yield from _czytanie(streszczenie, "")
    for rozbieżność in verdict.rozbieżne:
        yield f"„{rozbieżność.konstytuent}” czyta się tak:"
        for streszczenie in rozbieżność.czytania:
            yield from _czytanie(streszczenie, "  ")


def _dalsze(verdict: Verdict) -> str:
    """Wiersz o zatrzymaniach poza pierwszym, które nazwał już werdykt.

    Zdanie o jednym zatrzymaniu dostaje wiersz mówiący to wprost, bo milczenie
    czytałoby się tu jako flaga, która nic nie zrobiła.
    """
    dalsze = dalsze_zatrzymania(verdict)
    if not dalsze:
        return "the analysis stops nowhere else"
    formy = ", ".join(f"„{forma}”" for forma in dalsze)
    return f"the analysis stops again at {formy}"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="olski-check",
        description="Check whether each sentence of a Polish text is olski.",
    )
    parser.add_argument("paths", nargs="*", help="files of plain Polish text")
    parser.add_argument("-c", "--text", help="check this text instead of a file")
    parser.add_argument(
        "--readings",
        action="store_true",
        help="print what fills each role, once per distinct reading summary",
    )
    parser.add_argument(
        "--rozstrzygaj",
        action="store_true",
        help="obok werdyktu pokaż, co osobna warstwa mówi o przyłączeniach",
    )
    parser.add_argument(
        "--zatrzymania",
        action="store_true",
        help="pokaż każde miejsce, na którym staje analiza, a nie samo pierwsze",
    )
    args = parser.parse_args(argv)

    if not args.paths and args.text is None:
        parser.print_usage(sys.stderr)
        return 2

    sources: list[tuple[str, str]] = []
    if args.text is not None:
        sources.append(("<text>", args.text))
    for raw in args.paths:
        path = Path(raw)
        try:
            sources.append((raw, path.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError) as error:
            print(f"olski-check: could not read {raw}: {error}", file=sys.stderr)
            return 2

    #  Świadkowie powstają raz na przebieg, a nie raz na zdanie: tabela skłonności
    #  wchodzi z pliku, a dokument ma tyle zdań, ile ma.
    świadkowie = domyślni() if args.rozstrzygaj else None

    wszystkie: list[Verdict] = []
    for name, text in sources:
        #  Sąsiedztwa liczą się dla całego tekstu naraz, bo akapit jest jego
        #  własnością, a nie zdania: zdanie samo nie wie, co stoi przed nim.
        werdykty = check(text)
        wszystkie += werdykty
        konteksty = sąsiedztwa(text) if świadkowie is not None else [PUSTE] * len(werdykty)
        for verdict, sąsiedztwo in zip(werdykty, konteksty, strict=True):
            status = verdict.status
            wcięcie = f"{' ' * len(name)}  {' ' * STATUS_WIDTH}"
            print(f"{name}: {status:{STATUS_WIDTH}} {verdict.text}")
            print(f"{wcięcie} {verdict.explain()}")
            if args.zatrzymania and verdict.punktowane and verdict.result.rejected:
                print(f"{wcięcie} {_dalsze(verdict)}")
            if args.readings:
                for line in _czytania(verdict):
                    print(f"{wcięcie} {line}")
            if świadkowie is not None:
                for line in _rozstrzygnięcia(verdict, świadkowie, sąsiedztwo):
                    print(f"{wcięcie} {line}")

    podsumowanie = Podsumowanie.z_werdyktów(wszystkie)
    print(podsumowanie.explain())
    return 0 if podsumowanie.olskie == podsumowanie.zdań else 1


if __name__ == "__main__":
    raise SystemExit(main())
