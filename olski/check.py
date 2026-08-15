"""Checking a text against the grammar, from the command line."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from olski.rozstrzyganie import Rozstrzygnięcie, domyślni, rozstrzygnij
from olski.subset import FRAGMENT, check

STATUS_WIDTH = 9

#: Znak przed wierszem warstwy rozstrzygającej. Wiersz ten nie jest werdyktem
#: i nie może się na werdykt czytać, bo werdykt mówi, co olski o zdaniu wie,
#: a ten wiersz, co osobna warstwa o nim zgaduje (``olski/rozstrzyganie.py``).
DOMYSŁ = "?"


def _rozstrzygnięcia(verdict, świadkowie) -> list[str]:
    """Wiersze warstwy rozstrzygającej, po jednym na przyłączenie, albo żaden.

    Milczenie warstwy zostaje nienazwane, bo werdykt nad tym zdaniem nazwał już
    to przyłączenie i powiedział o nim to samo: że nierozstrzygnięte.
    """
    return [
        f"{DOMYSŁ} „{o.modyfikator}” → „{o.gospodarz}”: {o.powód}"
        for o in rozstrzygnij(verdict.result.przyłączenia, świadkowie)
        if isinstance(o, Rozstrzygnięcie)
    ]


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
        help="print what fills each role in every reading",
    )
    parser.add_argument(
        "--rozstrzygaj",
        action="store_true",
        help="obok werdyktu pokaż, co osobna warstwa mówi o przyłączeniach",
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

    accepted = 0
    total = 0
    fragments = 0
    for name, text in sources:
        for verdict in check(text):
            status = verdict.status
            fragments += status == FRAGMENT
            total += status != FRAGMENT
            accepted += status == "valid"
            wcięcie = f"{' ' * len(name)}  {' ' * STATUS_WIDTH}"
            print(f"{name}: {status:{STATUS_WIDTH}} {verdict.text}")
            print(f"{wcięcie} {verdict.explain()}")
            if args.readings:
                for reading in verdict.readings:
                    parts = ", ".join(f"{role}: {fill}" for role, fill in reading.items())
                    print(f"{wcięcie} - {parts}")
            if świadkowie is not None:
                for line in _rozstrzygnięcia(verdict, świadkowie):
                    print(f"{wcięcie} {line}")

    summary = f"{accepted} of {total} sentences are olski"
    if fragments:
        summary += f", beside {fragments} fragments that are not sentences"
    print(summary)
    return 0 if accepted == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
