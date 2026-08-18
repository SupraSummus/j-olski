"""Co kupuje i co kosztuje okolicznik wyrażony zdaniem, liczone zdejmowaniem go.

Kolejka blokerów prowadzi do niego wierszem ``comp``, który stał w niej piąty z
567 zdaniami, a nad prozą tego repozytorium spójnik otwierający okolicznik stoi
zaraz za dwukropkiem (``docs/corpus.md``).

Trudność nie leży w produkcjach, bo tych są cztery. Leży w tym, że polszczyzna
otwiera ten okolicznik tym samym znakiem, którym koordynuje zdania, a część
spójników, które go wprowadzają, Morfeusz zna także jako przysłówki: ``Program
zapisuje ustawienia, gdy linter sprawdza tekst.`` czyta się jako zdanie z
okolicznikiem i jako dwa zdania spięte przecinkiem, w których ``gdy`` jest
okolicznikiem przysłówkowym. Pierwsze z tych czytań jest tym, co zdanie mówi, a
drugiego polszczyzna w tym miejscu nie ma, więc konstrukcja kupuje prawdę o
zdaniu i płaci za nią jednoznacznością tych zdań, w których stoi taki spójnik.

Grupy są dwie i każda jest jedną pozycją okolicznika. ``za zdaniem`` to pozycja z
przecinkiem przed spójnikiem, ``przed zdaniem`` ta z przecinkiem za zdaniem
podrzędnym, i cena każdej z nich jest osobną liczbą, bo pierwsza konkuruje z
koordynacją przecinkiem, a druga z okolicznikiem wysuniętym przed zdanie.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.okolicznikowe Składnica-frazowa-180723/
    python3 -m sonda.okolicznikowe proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, Sym
from olski.subset import OKOLICZNIKOWY, PRZECINEK
from sonda import ruch

ZA_ZDANIEM = "za zdaniem"
PRZED_ZDANIEM = "przed zdaniem"


def pozycja(produkcja: Production) -> str | None:
    """Po której stronie swojego zdania stawia okolicznik ta produkcja.

    Odpowiada kształt ciała, a nie lista nazw wypisana obok gramatyki: ciało
    dopisane kiedyś w którejkolwiek z dwóch pozycji trafi tu samo, gdzie lista
    postarzałaby się bez śladu.

    Kształtem odpowiada zaś przecinek, bo o to samo pyta się tu dwa razy.
    Konstytuent okolicznika trzyma go po tej stronie, po której stoi zdanie
    nadrzędne, a ciało zdania nadrzędnego stawia sam okolicznik po tej stronie,
    po której ma stać, więc obie produkcje jednej pozycji mówią o niej to samo i
    mówią to niezależnie od siebie: rozejście się ich zgłasza się tu wariantem, w
    którym symbol nie ma czym się wypełnić.
    """
    if produkcja.head == OKOLICZNIKOWY:
        return ZA_ZDANIEM if produkcja.body[0] == PRZECINEK else PRZED_ZDANIEM
    okolicznik = [
        i
        for i, część in enumerate(produkcja.body)
        if isinstance(część, Sym) and część.name == OKOLICZNIKOWY
    ]
    if not okolicznik:
        return None
    return ZA_ZDANIEM if okolicznik[0] == len(produkcja.body) - 1 else PRZED_ZDANIEM


SONDA = ruch.Sonda(
    prog="python3 -m sonda.okolicznikowe",
    opis="Ile okolicznik wyrażony zdaniem kupuje i ile kosztuje.",
    warianty=("bez okolicznika zdaniowego", ZA_ZDANIEM, PRZED_ZDANIEM, "olski"),
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
