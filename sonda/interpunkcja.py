"""Ile kupuje i ile kosztuje interpunkcja zdaniowa, liczone zdejmowaniem jej.

Kolejka blokerów prowadzi tu wierszem ``interp``, który stoi w niej pierwszy z
trzema tysiącami zdań, czyli trzema dziesiątymi wszystkich odrzuceń, a nad prozą
tego repozytorium dwukropek stoi na jej czele (``docs/corpus.md``). Interpunkcja
zdaniowa spina zdania, które już się wyprowadzają, więc trudność nie leży w
kształcie tych produkcji, tylko w tym, z czym każdy znak w tym miejscu konkuruje.

Grupy są dwie i konkurują z czym innym, dlatego cena każdej z nich jest osobną
liczbą. Dwukropek nie konkuruje z niczym: nie bierze go żaden inny terminal tej
gramatyki, więc zdanie, w którym on stoi, nie ma bez tej produkcji ani jednego
czytania, i zero w kolumnie ceny jest tu wynikiem wyprowadzonym z gramatyki, a nie
zmierzonym. Przecinek przed spójnikiem konkuruje z koordynacją samym przecinkiem
i z okolicznikiem wysuniętym przed zdanie, bo `a` niesie w słowniku czytanie
przyimkowe, więc mierzy się go po to, żeby te dwa zobaczyć.

Cały pomiar prowadzi ``sonda/ruch.py``, wspólny sondom różnicowym tego pakietu, a
tutaj zostaje jedno pytanie: którym znakiem ta produkcja spina zdania.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.interpunkcja Składnica-frazowa-180723/
    python3 -m sonda.interpunkcja proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production
from olski.subset import DWUKROPEK, PRZECINEK
from sonda import ruch

DWUKROPKIEM = "dwukropek"
PRZED_SPÓJNIKIEM = "przecinek przed spójnikiem"


def znak(produkcja: Production) -> str | None:
    """Którym znakiem ta produkcja spina zdania; ``None``, gdy żadnym.

    Pytanie stawiane produkcji, a nie liście nazw obok gramatyki: średnik dopisany
    kiedyś jako trzeci znak zgłosi się tu sam brakującą nazwą wariantu, gdzie lista
    przemilczałaby go i sonda mierzyłaby dalej dwa.

    Dwukropek odpowiada sam za siebie, bo bierze go jeden terminal. Przecinek nie,
    bo polszczyzna stawia go także tam, gdzie nic się nie koordynuje, i tam, gdzie
    koordynuje sam: pozycja, o którą tu chodzi, jest ciągiem współrzędnym ze
    spójnikiem obok przecinka. Bez tego drugiego warunku ta sonda zdejmowałaby
    koordynację samym przecinkiem, którą mierzy ``sonda/przecinek.py``,
    i obie mierzyłyby jedną produkcję dwa razy.
    """
    if DWUKROPEK in produkcja.body:
        return DWUKROPKIEM
    if PRZECINEK not in produkcja.body:
        return None
    if ruch.koordynuje(produkcja) and ruch.ze_spójnikiem(produkcja):
        return PRZED_SPÓJNIKIEM
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.interpunkcja",
    opis="Ile interpunkcja zdaniowa kupuje i ile kosztuje.",
    warianty=("bez interpunkcji zdaniowej", DWUKROPKIEM, PRZED_SPÓJNIKIEM, "olski"),
    grupa=znak,
    pytania=(
        "oba znaki ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
