"""Czy zdanie z tym spójnikiem staje na czele, policzone nad Składnicą.

Okolicznik wyrażony zdaniem ma w polszczyźnie dwie pozycje i nie każdy spójnik
bierze obie: `Zostaję w domu, bo pada.` jest polszczyzną, a `Bo pada, zostaję w
domu.` nie jest. Fakt ten rozstrzyga o jednym ciele produkcji
(``SPÓJNIKI_WYSUWANE`` w ``olski/subset.py``), a rozstrzygać go z pamięci nie ma
po co, skoro korpus stoi obok.

Miara jest zgrubna i jest taka rozmyślnie. Liczymy, ile razy forma otwiera
zdanie, wobec tego, ile razy stoi w nim w ogóle, i o zdanie podrzędne nie pytamy,
bo pytanie o nie żądałoby drzewa, a drzewo jest tu odpowiedzią wzorcową, nie
pytaniem. Miara ta myli się w jedną stronę i widać to na `bo`: zdanie
zaczynające się od tego spójnika odsyła w tym korpusie do zdania przed nim,
zamiast być zdaniem podrzędnym wysuniętym przed swoje nadrzędne. Rozdziela
natomiast czysto te spójniki, które nie otwierają zdania nigdy, i po to tu stoi.

Znacznik bierzemy z morfologii złotej, czyli z tego czytania, które wybrał
anotator, bo pytanie jest o spójnik, a nie o formę, która bywa też czym innym.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.czoło Składnica-frazowa-180723/
"""

from __future__ import annotations

import argparse
import collections
import os
import sys
from collections.abc import Sequence
from pathlib import Path

from olski.corpus import pliki, read
from olski.coverage import po_kawałkach
from olski.subset import SPÓJNIKI_PO_ZDANIU, SPÓJNIKI_WYSUWANE

#: Spójniki, których okolicznik nie bierze, a które są tu miarą dla tamtych.
#: `bowiem` nie otwiera swojego zdania, bo polszczyzna stawia je za pierwszym
#: wyrazem, a `że` otwiera zdanie, którego się nie wysuwa, bo jest ono pozycją
#: ramy czasownika, więc oba mówią, jak wygląda w tej mierze spójnik niewysuwany.
POZA_OKOLICZNIKIEM = ("bowiem", "że")

#: Do której listy należy spójnik, czyli co ta sonda ma potwierdzić albo obalić.
LISTY = {
    **{lemat: "wysuwany" for lemat in SPÓJNIKI_WYSUWANE.split("|")},
    **{lemat: "po zdaniu" for lemat in SPÓJNIKI_PO_ZDANIU.split("|")},
    **{lemat: "poza okolicznikiem" for lemat in POZA_OKOLICZNIKIEM},
}


def _kawałek(ścieżki: Sequence[Path]) -> tuple[collections.Counter, collections.Counter]:
    czoło: collections.Counter = collections.Counter()
    razem: collections.Counter = collections.Counter()
    for ścieżka in ścieżki:
        zdanie = read(ścieżka)
        if not zdanie.annotated:
            continue
        for numer, segment in enumerate(zdanie.segments):
            lematy = {
                czytanie.lemma for czytanie in segment.readings if czytanie.tag.pos == "comp"
            }
            for lemat in lematy & set(LISTY):
                razem[lemat] += 1
                if numer == 0:
                    czoło[lemat] += 1
    return czoło, razem


def wydruk(czoło: collections.Counter, razem: collections.Counter) -> str:
    wiersze = [
        "Składnica, morfologia złota: ile razy spójnik otwiera zdanie",
        "",
        f"{'spójnik':>10}  {'na czele':>9} {'wystąpień':>10}  lista",
    ]
    for lemat in sorted(razem, key=lambda lemat: (-razem[lemat], lemat)):
        wiersze.append(
            f"{lemat:>10}  {czoło[lemat]:>9} {razem[lemat]:>10}  {LISTY[lemat]}"
        )
    for lemat in sorted(set(LISTY) - set(razem)):
        wiersze.append(f"{lemat:>10}  {'—':>9} {'—':>10}  {LISTY[lemat]}, w korpusie nieobecny")
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m sonda.czoło",
        description="Ile razy spójnik podrzędny otwiera zdanie w banku drzew.",
    )
    parser.add_argument("ścieżka", help="katalog z rozpakowaną Składnicą")
    parser.add_argument(
        "--jobs",
        type=int,
        default=os.cpu_count() or 1,
        help="ile procesów czyta i liczy; 1 liczy w tym",
    )
    args = parser.parse_args(argv)

    ścieżka = Path(args.ścieżka)
    if not ścieżka.is_dir():
        print(f"sonda.czoło: nie ma takiego katalogu: {ścieżka}", file=sys.stderr)
        print("sonda.czoło: docs/corpus.md mówi, skąd wziąć korpus", file=sys.stderr)
        return 2

    czoło: collections.Counter = collections.Counter()
    razem: collections.Counter = collections.Counter()
    for część, wszystkie in po_kawałkach(pliki(ścieżka), args.jobs, _kawałek):
        czoło.update(część)
        razem.update(wszystkie)
    print(wydruk(czoło, razem))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
