"""Co kupuje i co kosztuje grupa wysunięta razem z zaimkiem, liczone zdejmowaniem.

Polszczyzna wysuwa na czoło zdania nie tylko zaimek `który`, ale i całą grupę, w
której on stoi: `ustawy, na podstawie której jest ono wydawane` jest zdaniem „Zasad
techniki prawodawczej”, a `W którym roku ustawa weszła?` pytaniem tego samego
rejestru. Wariant mianownikowy ma czoło o jednym słowie i oba te zdania odrzuca,
choć czytelnik ma nad każdym z nich jedno czytanie.

Grupy są dwie i każda jest jedną pozycją, bo cena każdej z nich jest osobną liczbą.
``grupa względna`` to rzeczownik z zaimkiem w dopełniaczu, w obu szykach, wysunięty
razem z przyimkiem przed zdanie względne. ``grupa pytajna z przyimkiem`` to ta sama
grupa pytajna, którą pytanie stawia w podmiocie i w dopełnieniu, tylko wysunięta
razem z przyimkiem, który nią rządzi.

Trudność nie leży w liczbie produkcji, bo tych jest pięć. Leży w tym, że przyimek
z rzeczownikiem jest w tym rejestrze zwyczajnym wyrażeniem przyimkowym, a olski
przyłączenia takiego wyrażenia nie wybiera (``docs/subset.md``): zdanie, w którym
`na podstawie` daje się przyłączyć gdzie indziej, może przez tę grupę dostać
czytanie, którego przedtem nie miało. Cena stoi więc tam, gdzie zdanie już przyjęte
przestaje być jednoznaczne, a zakup tam, gdzie odrzucone dostaje pierwsze czytanie.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.wysunięcie Składnica-frazowa-180723/
    python3 -m sonda.wysunięcie proza/ztp.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, Sym
from sonda import ruch

WZGLĘDNA = "grupa względna"
PYTAJNA = "grupa pytajna z przyimkiem"

#: Symbol grupy wysuniętej przed zdanie względne i symbol wyrażenia przyimkowego,
#: którym pytanie ją wysuwa. Napisami, tak jak w pozostałych sondach pytających
#: o kształt produkcji: gramatyka nazw tych symboli nie wypisuje stałą, a sonda
#: pyta o produkcję, nie o listę obok niej.
GRUPA_WZGLĘDNA = "RelativeNP"
PRZYIMEK_PYTANIA = "InterrogativeModifier"


def _ma_symbol(produkcja: Production, nazwa: str) -> bool:
    return any(isinstance(część, Sym) and część.name == nazwa for część in produkcja.body)


def grupa(produkcja: Production) -> str | None:
    """Do której z dwóch grup należy ta produkcja.

    Po stronie względnej odpowiada długość ciała, a nie nazwa symbolu: sam zaimek
    wysuwa się także bez tej grupy, więc zdjęcie jego ciała mierzyłoby konstrukcję,
    o którą ta sonda nie pyta. Ciałem o jednej córce jest dokładnie ten zaimek, a
    każdy kolejny kształt grupy ma córek więcej, więc kształt dopisany kiedyś trafi
    tu sam, gdzie lista nazw postarzałaby się bez śladu.

    Po stronie pytającej odpowiada nazwa symbolu, i wariant zdejmuje wyrażenie
    przyimkowe razem z czołem, które je bierze. Zdjęte samo zostawiłoby symbol bez
    ani jednego ciała, a taki symbol zatrzymuje rozbiór każdego zdania, nie tylko
    pytającego.
    """
    if produkcja.head == GRUPA_WZGLĘDNA:
        return WZGLĘDNA if len(produkcja.body) > 1 else None
    if produkcja.head == PRZYIMEK_PYTANIA or _ma_symbol(produkcja, PRZYIMEK_PYTANIA):
        return PYTAJNA
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.wysunięcie",
    opis="Ile kupuje i ile kosztuje grupa wysunięta razem z zaimkiem.",
    warianty=("bez grupy", WZGLĘDNA, PYTAJNA, "olski"),
    grupa=grupa,
    pytania=(
        "obie grupy ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
