"""Co kupuje i co kosztuje rzeczownik odczasownikowy, liczone zdejmowaniem go.

Kolejka nad prozą tego repozytorium prowadzi tu wprost: po leksykonie projektu
rzeczowniki odczasownikowe stoją na jej czele (``docs/corpus.md``), a wiersz
``ger`` stoi w kolejce ze Składnicy czwarty. Formy `ger` nie brał przedtem żaden
terminal, więc zdanie z nią nie miało ani jednego czytania.

Trudność nie leży w kształcie tych produkcji, bo rzeczownik odczasownikowy stoi w
grupie imiennej tam, gdzie każdy inny rzeczownik. Leży w tym, z czym konkuruje:
`czytanie` jest u Morfeusza i rzeczownikiem, i formą odczasownikową `czytać`, a
dwa wyprowadzenia jednego kształtu są jednym czytaniem (``olski/parse.py``), więc
tam, gdzie słownik ma oba, ta konstrukcja nie ma jak odebrać jednoznaczności.
Płaci dopiero forma, której słownik rzeczownikiem nie zna — `przyłączenie`,
`sięgnięciu` — bo dopiero ona wnosi kształt, którego zdanie przedtem nie miało.

Grupy są dwie i każda jest jedną pozycją, bo cena każdej z nich jest osobną
liczbą. ``głowa`` to rzeczownik odczasownikowy jako głowa grupy imiennej, sam albo
z przymiotnikiem i wyrażeniem przyimkowym przy sobie. ``z dopełniaczem`` to ta sama
głowa rządząca dopełniaczem: `przyłączenie wyrażenia przyimkowego`. Druga jest ta,
o którą chodzi w tym rejestrze, i ta, która może odebrać jednoznaczność, bo
dopełniacz pod głową konkuruje z przyłączeniem, którego olski nie wybiera.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.odczasownikowy Składnica-frazowa-180723/
    python3 -m sonda.odczasownikowy proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, Word
from sonda import ruch

GŁOWA = "głowa"
Z_DOPEŁNIACZEM = "z dopełniaczem"

#: Część mowy, którą Morfeusz daje rzeczownikowi odczasownikowemu.
ODCZASOWNIKOWY = "ger"

#: Symbol grupy imiennej, czyli tej, którą taka głowa rządzi w dopełniaczu.
GRUPA_IMIENNA = "NP"


def grupa(produkcja: Production) -> str | None:
    """Do której z dwóch grup należy ta produkcja; ``None``, gdy do żadnej.

    Odpowiada terminal stojący w ciele, a nie lista nazw wypisana obok gramatyki:
    ciało dopisane kiedyś tej głowie trafi tu samo, gdzie lista postarzałaby się
    bez śladu i sonda mierzyłaby wariant węższy, niż o sobie mówi.

    Warunek pyta, czy część mowy stoi w terminalu, a nie czy jest nim całym, bo
    terminal wzięty razem z rzeczownikiem zdejmowałby przy tym rzeczownik, czyli
    mierzyłby coś innego niż konstrukcję. Takiego terminala gramatyka nie ma i po
    to nie ma, więc ten warunek zgłasza go pomiarem, który wywróci się widocznie:
    wariant mianownikowy nie wyprowadzi wtedy ani jednego zdania.
    """
    if not any(
        isinstance(część, Word) and ODCZASOWNIKOWY in część.pos for część in produkcja.body
    ):
        return None
    return Z_DOPEŁNIACZEM if ruch.ma_symbol(produkcja, GRUPA_IMIENNA) else GŁOWA


SONDA = ruch.Sonda(
    prog="python3 -m sonda.odczasownikowy",
    opis="Ile kupuje i ile kosztuje rzeczownik odczasownikowy.",
    warianty=("bez rzeczownika odczasownikowego", GŁOWA, Z_DOPEŁNIACZEM, "olski"),
    grupa=grupa,
    pytania=(
        "obie pozycje ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
