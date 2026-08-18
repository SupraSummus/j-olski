"""Co kupuje i co kosztuje pytanie, liczone zdejmowaniem obu jego pozycji.

Zaimek `który` stoi w polszczyźnie w trzech konstrukcjach, a olski miał jedną:
czoło zdania względnego. Dwie pozostałe wchodzą razem, bo dzielą kształt — na
czole zdania stoi grupa pytajna, a reszta zdania jest zdaniem bez tej roli, którą
ta grupa zajmuje — i różni je to, gdzie takie zdanie stoi: samo zamyka się
pytajnikiem, a w pozycji ramy zaczepia się przecinkiem o czasownik.

Trudność nie leży w produkcjach, bo tych są trzy. Leży w tym, że przecinek przed
pytaniem zależnym jest tym samym znakiem, którym polszczyzna koordynuje zdania,
a `które zadania` wygląda jak grupa imienna z przymiotnikiem: bez warunku
ujemnego na lemat zdanie z pytaniem zależnym wychodziło jednym czytaniem
współrzędnym, czyli werdyktem pewnym siebie i błędnym
(``docs/subset.md``). Cena stoi więc tam, gdzie zdanie już przyjęte dostaje drugie
czytanie z pytaniem, a zakup tam, gdzie odrzucone dostaje pierwsze.

Grupy są dwie i każda jest jedną pozycją. ``zdanie pytające`` to pytanie stojące
samo, ``pytanie zależne`` to pytanie w pozycji ramy, i cena każdej z nich jest
osobną liczbą, bo pierwsza konkuruje z oznajmującym zamkniętym pytajnikiem, a
druga z koordynacją przecinkiem.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.pytanie Składnica-frazowa-180723/
    python3 -m sonda.pytanie proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, Sym
from sonda import ruch

PYTAJĄCE = "zdanie pytające"
ZALEŻNE = "pytanie zależne"

#: Symbol pytania w pozycji ramy i symbol samego czoła. Napisami, tak jak w
#: pozostałych sondach pytających o kształt produkcji: gramatyka nazw tych
#: symbolów nie wypisuje stałą, a sonda pyta o produkcję, nie o listę obok niej.
PYTANIE_ZALEŻNE = "InterrogativeClause"
CZOŁO_PYTANIA = "InterrogativeCore"


def _ma_symbol(produkcja: Production, nazwa: str) -> bool:
    return any(isinstance(część, Sym) and część.name == nazwa for część in produkcja.body)


def pozycja(produkcja: Production) -> str | None:
    """W której pozycji stawia pytanie ta produkcja.

    Odpowiada kształt ciała, a nie lista nazw wypisana obok gramatyki: pozycja
    dopisana kiedyś którejkolwiek z dwóch trafi tu sama, gdzie lista postarzałaby
    się bez śladu.

    Czoło pytania zostaje w każdym wariancie i nie należy do żadnej z grup, bo
    obie je biorą. Wariant mianownikowy zostawia je przez to bez drogi z góry, a
    symbol nieosiągalny nie wyprowadza niczego, więc mianownik mówi o zdaniu to
    samo, co gramatyka przed wpuszczeniem pytania.
    """
    if produkcja.head == PYTANIE_ZALEŻNE or _ma_symbol(produkcja, PYTANIE_ZALEŻNE):
        return ZALEŻNE
    if _ma_symbol(produkcja, CZOŁO_PYTANIA):
        return PYTAJĄCE
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.pytanie",
    opis="Ile pytanie kupuje i ile kosztuje.",
    warianty=("bez pytania", PYTAJĄCE, ZALEŻNE, "olski"),
    grupa=pozycja,
    pytania=(
        "obie pozycje ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
