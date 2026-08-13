"""Ile kupuje i ile kosztuje grupa liczebnikowa, zmierzone nad Składnicą.

Liczebnik przyłącza się w polszczyźnie dwoma sposobami i Morfeusz rozdziela je
cechą ``accommodability``. Zgodny zgadza się z rzeczownikiem jak przymiotnik
(`dwie rzeczy`), a rządzący wymaga dopełniacza mnogiego i wypuszcza grupę, której
liczba i rodzaj nie są liczbą ani rodzajem żadnego słowa pod nią (`Pięć kobiet
przyszło`). Produkcje są więc dwie i każdą da się zdjąć osobno, bo cena każdej
jest osobną liczbą.

Pytanie jest to samo, co w drugiej sondzie różnicowej tego pakietu, i po to obie
stoją na ``sonda/ruch.py``: nie ile zdań te dwie produkcje przyjmują, bo to
policzy każdy przebieg ``olski-corpus``, tylko ile zdań odbierają. Grupa
liczebnikowa w mianowniku i w bierniku jest synkretyczna, bo taki jest liczebnik
rządzący, więc zdanie z nią obok drugiej grupy synkretycznej wychodzi dwoma
czytaniami — i to jest ta cena, której suma nie pokazuje.

Odpowiedź nad tym korpusem brzmi zero i wynik czyta ``docs/subset.md``.

    python3 -m sonda.liczebnik Składnica-frazowa-180723/
    python3 -m sonda.liczebnik proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, Word
from sonda import ruch

#: Przyłączenie → wartość ``accommodability``, którą jego liczebnik nosi.
#: Przyłączenie nazywa się z polska, bo jest nazwą wariantu w wydruku, a wartość
#: cechy jest napisem z tagsetu Morfeusza i zostaje taka, jaka tam stoi.
PRZYŁĄCZENIA = {"zgodny": "congr", "rządzący": "rec"}


def przyłączenie(produkcja: Production) -> str | None:
    """Które przyłączenie liczebnika niesie ta produkcja; ``None``, gdy żadne.

    Pytanie stawiane produkcji, a nie liście nazw obok gramatyki: produkcja
    dopisana kiedyś dla trzeciego przyłączenia odpowie tu sama, a lista obok
    przemilczałaby ją i sonda mierzyłaby dalej dwa.

    Odpowiada terminal, a nie symbol nad nim: obie produkcje budują ``NPConjunct``,
    czyli ten sam symbol, którym jest każda grupa imienna bez liczebnika, więc po
    głowie produkcji nie da się ich odróżnić od reszty.
    """
    for część in produkcja.body:
        if not (isinstance(część, Word) and "num" in część.pos):
            continue
        wartości = dict(część.constraints).get("accommodability") or ()
        for nazwa, wartość in PRZYŁĄCZENIA.items():
            if wartość in wartości:
                return nazwa
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.liczebnik",
    opis="Ile grupa liczebnikowa kupuje i ile kosztuje.",
    warianty=("bez liczebnika", *PRZYŁĄCZENIA, "oba"),
    grupa=przyłączenie,
    pytania=(
        "oba przyłączenia ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
