"""Co kupuje i co kosztuje grupa wysunięta razem z zaimkiem, liczone zdejmowaniem.

Polszczyzna wysuwa na czoło zdania nie tylko zaimek `który`, ale i całą grupę, w
której on stoi: `ustawy, na podstawie której jest ono wydawane` jest zdaniem „Zasad
techniki prawodawczej”, `ustawa, której przepisy obowiązują` tym samym kształtem
bez przyimka, a `W którym roku ustawa weszła?` pytaniem tego samego rejestru.
Wariant bez grupy odrzuca każde z nich, choć czytelnik ma nad nimi po jednym
czytaniu.

Grupy są trzy i każda jest jedną pozycją, bo cena każdej z nich jest osobną liczbą.
``grupa względna z przyimkiem`` to rzeczownik z zaimkiem w dopełniaczu, w obu
szykach, wysunięty razem z przyimkiem przed zdanie względne. ``grupa względna bez
przyimka`` to ta sama grupa w roli podmiotu albo dopełnienia zdania składowego,
czyli tam, gdzie przypadka żąda nie przyimek, tylko sama rola. ``grupa pytajna z
przyimkiem`` to grupa pytajna, którą pytanie stawia w podmiocie i w dopełnieniu,
wysunięta razem z przyimkiem, który nią rządzi.

Trudność leży przy pierwszej i trzeciej w tym, że przyimek z rzeczownikiem jest w
tym rejestrze zwyczajnym wyrażeniem przyimkowym, a olski przyłączenia takiego
wyrażenia nie wybiera (``docs/subset.md``): zdanie, w którym `na podstawie` daje się
przyłączyć gdzie indziej, może przez tę grupę dostać czytanie, którego przedtem nie
miało. Przy drugiej leży gdzie indziej — w zgodności, bo grupa niesie liczbę i
rodzaj dwa razy: orzeczenie zgadza się z jej głową, a poprzednik z jej zaimkiem.
Cena stoi więc tam, gdzie zdanie już przyjęte przestaje być jednoznaczne, a zakup
tam, gdzie odrzucone dostaje pierwsze czytanie.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.wysunięcie Składnica-frazowa-180723/
    python3 -m sonda.wysunięcie proza/ztp.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production
from sonda import ruch

Z_PRZYIMKIEM = "grupa względna z przyimkiem"
BEZ_PRZYIMKA = "grupa względna bez przyimka"
PYTAJNA = "grupa pytajna z przyimkiem"

#: Symbol grupy wysuniętej przed zdanie względne, symbol wyrażenia przyimkowego,
#: które ją wysuwa, i symbol tegoż wyrażenia po stronie pytania. Napisami, tak jak
#: w pozostałych sondach pytających o kształt produkcji: gramatyka nazw tych
#: symboli nie wypisuje stałą, a sonda pyta o produkcję, nie o listę obok niej.
GRUPA_WZGLĘDNA = "RelativeNP"
PRZYIMEK_WZGLĘDNY = "RelativeModifier"
PRZYIMEK_PYTANIA = "InterrogativeModifier"


def grupa(produkcja: Production) -> str | None:
    """Do której z trzech grup należy ta produkcja.

    Po stronie względnej rozstrzyga to, gdzie grupa stoi, a nie jaki ma kształt:
    gramatyka wpuszcza ją pod przyimek i w rolę zdania składowego, a kształt jest
    w obu pozycjach ten sam. Do grupy zdejmowanej należy więc ciało, które grupę
    bierze, a nie to, które ją buduje, i kształt dopisany kiedyś trafi tu sam,
    gdzie lista nazw postarzałaby się bez śladu.

    Produkcje samej grupy zostają w każdym wariancie i nie należą do żadnej z
    grup, bo obie pozycje je biorą; tak samo zostaje czoło pytania w
    ``sonda/pytanie.py``. Wariant mianownikowy zostawia je przez to bez drogi z
    góry, a symbol nieosiągalny nie wyprowadza niczego.

    Po stronie pytającej odpowiada nazwa symbolu, i wariant zdejmuje wyrażenie
    przyimkowe razem z czołem, które je bierze. Zdjęte samo zostawiłoby symbol bez
    ani jednego ciała, a taki symbol zatrzymuje rozbiór każdego zdania, nie tylko
    pytającego.
    """
    if ruch.ma_symbol(produkcja, GRUPA_WZGLĘDNA):
        return Z_PRZYIMKIEM if produkcja.head == PRZYIMEK_WZGLĘDNY else BEZ_PRZYIMKA
    if produkcja.head == PRZYIMEK_PYTANIA or ruch.ma_symbol(produkcja, PRZYIMEK_PYTANIA):
        return PYTAJNA
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.wysunięcie",
    opis="Ile kupuje i ile kosztuje grupa wysunięta razem z zaimkiem.",
    warianty=("bez grupy", Z_PRZYIMKIEM, BEZ_PRZYIMKA, PYTAJNA, "olski"),
    grupa=grupa,
    pytania=(
        "kilka grup rusza to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
