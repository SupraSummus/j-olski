"""Ile kupuje i ile kosztuje interpunkcja zdaniowa, liczone zdejmowaniem jej.

Kolejka blokerów prowadzi tu wierszem ``interp``, który stoi w niej pierwszy z
trzema tysiącami zdań, czyli trzema dziesiątymi wszystkich odrzuceń, a nad prozą
tego repozytorium dwukropek stoi na jej czele (``docs/corpus.md``). Interpunkcja
zdaniowa spina zdania, które już się wyprowadzają, więc trudność nie leży w
kształcie tych produkcji, tylko w tym, z czym każdy znak w tym miejscu konkuruje.

Grupy są trzy i konkurują z czym innym, dlatego cena każdej z nich jest osobną
liczbą. Dwukropek i średnik nie konkurują z niczym: nie bierze ich żaden inny
terminal tej gramatyki, więc zdanie, w którym któryś z nich stoi, nie ma bez tej
produkcji ani jednego czytania, i zero w kolumnie ceny jest przy nich wynikiem
wyprowadzonym z gramatyki, a nie zmierzonym. Przecinek przed spójnikiem
konkuruje z koordynacją samym przecinkiem i z okolicznikiem wysuniętym przed
zdanie, bo `a` niesie w słowniku czytanie przyimkowe, więc mierzy się go po to,
żeby te dwa zobaczyć.

Cały pomiar prowadzi ``sonda/ruch.py``, wspólny sondom różnicowym tego pakietu, a
tutaj zostaje jedno pytanie: którym znakiem ta produkcja spina zdania.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.interpunkcja Składnica-frazowa-180723/
    python3 -m sonda.interpunkcja proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production
from olski.subset import DWUKROPEK, PRZECINEK, ŚREDNIK
from sonda import ruch

DWUKROPKIEM = "dwukropek"
ŚREDNIKIEM = "średnik"
PRZED_SPÓJNIKIEM = "przecinek przed spójnikiem"

#: Znaki rozdzielające zdanie, wraz z nazwą wariantu na każdy. Terminale są tu
#: wzięte z olskiego, a nie wypisane obok niego, więc nazwa lematu zmieniona w
#: gramatyce nie zostawia tej sondy mierzącej znak, którego tam już nie ma.
ZNAKI = ((DWUKROPEK, DWUKROPKIEM), (ŚREDNIK, ŚREDNIKIEM))


def znak(produkcja: Production) -> str | None:
    """Którym znakiem ta produkcja spina zdania; ``None``, gdy żadnym.

    Dwukropek i średnik odpowiadają same za siebie, bo każdy z nich bierze jeden
    terminal i żaden inny. Przecinek nie, bo polszczyzna stawia go także tam,
    gdzie nic się nie koordynuje, i tam, gdzie koordynuje sam: pozycja, o którą
    tu chodzi, jest ciągiem współrzędnym ze spójnikiem obok przecinka. Bez tego
    drugiego warunku ta sonda zdejmowałaby koordynację samym przecinkiem, którą
    mierzy ``sonda/przecinek.py``, i obie mierzyłyby jedną produkcję dwa razy.

    Znak dopisany kiedyś jako czwarty tej listy nie zgłosi się tu sam: bez wpisu
    w :data:`ZNAKI` zostaje on w każdym wariancie, więc sonda mierzy dalej trzy i
    nie mówi o tym ani słowem. Wiersz na znak jest ceną tego, że wariant nazywa
    się po polsku, a nazwy lemat nie nosi.
    """
    for terminal, nazwa in ZNAKI:
        if terminal in produkcja.body:
            return nazwa
    if PRZECINEK not in produkcja.body:
        return None
    if ruch.koordynuje(produkcja) and ruch.ze_spójnikiem(produkcja):
        return PRZED_SPÓJNIKIEM
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.interpunkcja",
    opis="Ile interpunkcja zdaniowa kupuje i ile kosztuje.",
    warianty=(
        "bez interpunkcji zdaniowej",
        DWUKROPKIEM,
        ŚREDNIKIEM,
        PRZED_SPÓJNIKIEM,
        "olski",
    ),
    grupa=znak,
    pytania=(
        "kilka znaków rusza to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
