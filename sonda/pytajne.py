"""Czym ten rejestr pyta, policzone nad Składnicą.

Grupa pytajna olskiego stoi na jednym lemacie — tym, który niesie zarazem zdanie
względne (``ZAIMEK_PYTAJNO_WZGLĘDNY`` w ``olski/subset.py``) — a polszczyzna pyta
kilkunastoma słowami i każde z nich żąda innego kształtu: cząstka otwiera pytanie
o rozstrzygnięcie, zaimek rzeczowny stoi sam, a przysłówek pytajny nie zajmuje
ani podmiotu, ani dopełnienia. Ile każde z nich w tym rejestrze waży, rozstrzyga
o kolejności, w jakiej te kształty warto dopisywać, i z pamięci tego rozstrzygać
nie ma po co, skoro korpus stoi obok.

Miara jest zgrubna i jest taka rozmyślnie. Pytaniem jest zdanie zamknięte
pytajnikiem, a jego czołem pierwszy segment, który nie jest samą interpunkcją, bo
w tym korpusie kwestię dialogu otwiera myślnik. O to, czy zdanie jest pytaniem
zależnym, nie pytamy wcale: pytanie o nie żądałoby drzewa, a drzewo jest tu
odpowiedzią wzorcową, nie pytaniem, i pytania zależnego pytajnik nie zamyka.

Wiersz nazywa lemat, który pytanie otwiera, a nie słowo pytajne: pytanie o
rozstrzygnięcie stawiane bez cząstki otwiera czasownik albo przeczenie, i te
wiersze są w tej tabeli tak samo prawdziwe jak tamte. Forma o kilku lematach
wchodzi pod pierwszy z nich alfabetycznie, więc wiersz o jednym wystąpieniu mówi
mniej niż wiersz o pięćdziesięciu. Liczba nad tabelą pyta natomiast o formę, a nie
o wiersz: wchodzi do niej każde pytanie, którego czoło ma lemat olskiego wśród
swoich, także wtedy, gdy w tabeli stoi pod lematem innym.

Znacznik i lemat bierzemy z morfologii złotej, czyli z czytania, które wybrał
anotator, bo pytanie jest o słowo, a nie o formę, która bywa też czym innym.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.pytajne Składnica-frazowa-180723/
"""

from __future__ import annotations

import argparse
import collections
import os
import sys
from collections.abc import Sequence
from pathlib import Path

from olski.corpus import Sentence, pliki, read
from olski.coverage import po_kawałkach
from olski.subset import ZAIMEK_PYTAJNO_WZGLĘDNY

#: Znak, którym polszczyzna zamyka pytanie.
PYTAJNIK = "?"

#: Ile wierszy tabeli wypisać. Ogon jest długi i jest nim po jednym wystąpieniu na
#: lemat, czyli ta część rozkładu, o której miara wyżej mówi najmniej.
WIERSZY = 20

#: Lematy, na których stoi grupa pytajna olskiego. Wzięte z gramatyki, a nie
#: wypisane tutaj, bo lemat dopisany tam ma zgłosić się w tej kolumnie sam.
U_OLSKIEGO = frozenset(ZAIMEK_PYTAJNO_WZGLĘDNY.split("|"))


def _czoło(zdanie: Sentence) -> frozenset[str]:
    """Lematy pierwszego segmentu zdania, który nie jest samą interpunkcją."""
    for segment in zdanie.segments:
        if all(czytanie.tag.pos == "interp" for czytanie in segment.readings):
            continue
        return frozenset(czytanie.lemma.lower() for czytanie in segment.readings)
    return frozenset()


def _kawałek(ścieżki: Sequence[Path]) -> tuple[collections.Counter, collections.Counter]:
    czoła: collections.Counter = collections.Counter()
    ile: collections.Counter = collections.Counter()
    for ścieżka in ścieżki:
        zdanie = read(ścieżka)
        if not zdanie.annotated:
            continue
        ile["zdań"] += 1
        if not zdanie.text.rstrip().endswith(PYTAJNIK):
            continue
        ile["pytań"] += 1
        lematy = _czoło(zdanie)
        if not lematy:
            continue
        czoła[sorted(lematy)[0]] += 1
        if lematy & U_OLSKIEGO:
            ile["czołem u olskiego"] += 1
    return czoła, ile


def wydruk(czoła: collections.Counter, ile: collections.Counter) -> str:
    wiersze = [
        "Składnica, morfologia złota: czym otwiera się pytanie",
        "",
        f"{ile['zdań']:>7}  zdań z drzewem wzorcowym",
        f"{ile['pytań']:>7}  zamkniętych pytajnikiem",
        f"{ile['czołem u olskiego']:>7}  otwartych lematem, który grupa pytajna olskiego bierze",
        "",
        f"{'lemat':>10}  {'pytań':>7}  u olskiego",
    ]
    for lemat, razem in czoła.most_common(WIERSZY):
        ma = "tak" if lemat in U_OLSKIEGO else "nie"
        wiersze.append(f"{lemat:>10}  {razem:>7}  {ma}")
    ogon = sum(czoła.values()) - sum(razem for _lemat, razem in czoła.most_common(WIERSZY))
    wiersze.append(f"{'reszta':>10}  {ogon:>7}  lematów: {max(len(czoła) - WIERSZY, 0)}")
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m sonda.pytajne",
        description="Czym otwiera się pytanie w banku drzew.",
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
        print(f"sonda.pytajne: nie ma takiego katalogu: {ścieżka}", file=sys.stderr)
        print("sonda.pytajne: docs/corpus.md mówi, skąd wziąć korpus", file=sys.stderr)
        return 2

    czoła: collections.Counter = collections.Counter()
    ile: collections.Counter = collections.Counter()
    for część, liczniki in po_kawałkach(pliki(ścieżka), args.jobs, _kawałek):
        czoła.update(część)
        ile.update(liczniki)
    print(wydruk(czoła, ile))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
