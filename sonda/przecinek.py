"""Ile kupuje i ile kosztuje koordynacja przecinkiem, zmierzone nad Składnicą.

``Clause``, ``NP`` i ``AP`` mają każde produkcję ze spójnikiem i produkcję z
przecinkiem. Pytanie nie brzmi, ile zdań te trzy przyjmują, bo to policzy każdy
przebieg ``olski-corpus``. Brzmi ono, ile zdań odbierają: przecinek między
zdaniami składowymi konkuruje z przecinkiem w grupie imiennej wszędzie tam,
gdzie po przecinku stoi rzeczownik, a zdanie, które przez to wychodzi dwoma
czytaniami, olski odrzuca.

Wariantów jest pięć, bo trzy poziomy koordynacji da się zdejmować osobno i cena
każdego z nich jest osobną liczbą. Cały pomiar prowadzi ``sonda/ruch.py``, wspólny
sondom różnicowym tego pakietu, a tutaj zostaje jedno pytanie: do którego poziomu
należy produkcja.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.przecinek Składnica-frazowa-180723/
    python3 -m sonda.przecinek proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, Sym
from olski.subset import PRZECINEK
from sonda import ruch

#: Poziom koordynacji → symbol, którego produkcje go niosą. Poziom nazywa się z
#: polska, bo jest nazwą wariantu w wydruku, a symbol stoi po angielsku razem z
#: całą gramatyką.
POZIOMY = {"zdaniowy": "Clause", "imienny": "NP", "przymiotnikowy": "AP"}


def poziom(produkcja: Production) -> str | None:
    """Na którym poziomie ta produkcja wnosi przecinek; ``None``, gdy nie wnosi go wcale.

    Pytanie stawiane produkcji, a nie liście nazw obok gramatyki: przecinek
    dopisany kiedyś na czwartym poziomie odpowie tu sam, a lista obok
    przemilczałaby go i sonda mierzyłaby dalej trzy.

    Sam przecinek w ciele na to nie odpowiada, bo polszczyzna stawia go i tam,
    gdzie nic się nie koordynuje: zdanie względne otwiera nim swoją granicę.
    Ciąg współrzędny poznaje się po tym, że symbol stoi nad sobą, i tak samo
    poznaje go werdykt (``_koordynuje`` w ``olski/parse.py``). Zdjęta produkcja
    podrzędna zostawiłaby ponadto symbol bez ani jednego ciała, a gramatyka z
    symbolem nieokreślonym nie rozbiera niczego.
    """
    if PRZECINEK not in produkcja.body:
        return None
    if not any(
        isinstance(część, Sym) and część.name == produkcja.head for część in produkcja.body
    ):
        return None
    for nazwa, symbol in POZIOMY.items():
        if produkcja.head == symbol:
            return nazwa
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.przecinek",
    opis="Ile koordynacja przecinkiem kupuje i ile kosztuje.",
    warianty=("bez przecinka", *POZIOMY, "wszystkie trzy"),
    grupa=poziom,
    pytania=(
        "oba poziomy ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
