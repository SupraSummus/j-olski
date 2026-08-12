"""Checking a text against the grammar, from the command line."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from olski.subset import FRAGMENT, check

STATUS_WIDTH = 9


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

    accepted = 0
    total = 0
    fragments = 0
    for name, text in sources:
        for verdict in check(text):
            status = verdict.status
            fragments += status == FRAGMENT
            total += status != FRAGMENT
            accepted += status == "valid"
            print(f"{name}: {status:{STATUS_WIDTH}} {verdict.text}")
            print(f"{' ' * len(name)}  {' ' * STATUS_WIDTH} {verdict.explain()}")
            if args.readings:
                for reading in verdict.readings:
                    parts = ", ".join(f"{role}: {fill}" for role, fill in reading.items())
                    print(f"{' ' * len(name)}  {' ' * STATUS_WIDTH} - {parts}")

    summary = f"{accepted} of {total} sentences are olski"
    if fragments:
        summary += f", beside {fragments} fragments that are not sentences"
    print(summary)
    return 0 if accepted == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
