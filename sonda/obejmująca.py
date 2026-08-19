"""Co kupuje interpunkcja obejmująca, czyli cudzysłów i nawias, liczone zdejmowaniem.

Znak rozdzielający spina dwa zdania, a te dwa obejmują to, co stoi w środku:
cudzysłów tytuł albo termin cytowany — `„Zasady techniki prawodawczej”` —
a nawias dopowiedzenie obok zdania, którym w tym rejestrze jest nazwa dokumentu:
`(docs/subset.md)`, `(niżej)`. Wiersz ``interp`` prowadzi kolejkę blokerów
ze Składnicy, a nad prozą tego repozytorium te dwa znaki stoją w niej za
średnikiem (``docs/corpus.md``).

Cena obu jest zerowa i wynika z gramatyki, a nie z przebiegu: żadnego z czterech
znaków nie brał przedtem ani jeden terminal, więc zdanie z nim nie miało czytania,
z którego dałoby się je wytrącić. Mierzy się tu więc sam zakup, i mierzy się go
osobno na znak, bo osobno się o niego pyta: cudzysłów wchodzi w grupę imienną,
a nawias staje obok zdania składowego.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.obejmująca Składnica-frazowa-180723/
    python3 -m sonda.obejmująca proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production
from olski.subset import (
    CUDZYSŁÓW_OTWIERAJĄCY,
    CUDZYSŁÓW_ZAMYKAJĄCY,
    NAWIAS_OTWIERAJĄCY,
    NAWIAS_ZAMYKAJĄCY,
    WTRĄCONY,
)
from sonda import ruch

CUDZYSŁOWEM = "cudzysłów"
NAWIASEM = "nawias"

#: Terminale każdego znaku wraz z nazwą wariantu. Wzięte z olskiego, a nie
#: wypisane obok niego, więc lemat zmieniony w gramatyce nie zostawia tej sondy
#: mierzącej znak, którego tam już nie ma.
ZNAKI = (
    ((CUDZYSŁÓW_OTWIERAJĄCY, CUDZYSŁÓW_ZAMYKAJĄCY), CUDZYSŁOWEM),
    ((NAWIAS_OTWIERAJĄCY, NAWIAS_ZAMYKAJĄCY), NAWIASEM),
)


def grupa(produkcja: Production) -> str | None:
    """Który znak ta produkcja bierze; ``None``, gdy żadnego.

    Produkcja wpuszczająca wtrącenie do zdania składowego należy do nawiasu, choć
    sama nawiasu nie bierze: bez niej symbol wtrącenia zostaje bez drogi z góry, a
    zdejmowanie samego ciała z nawiasami zostawiałoby w gramatyce symbol
    nieosiągalny — tak samo jak przy grupie wysuniętej w ``sonda/wysunięcie.py``.
    """
    for terminale, nazwa in ZNAKI:
        if any(terminal in produkcja.body for terminal in terminale):
            return nazwa
    if ruch.ma_symbol(produkcja, WTRĄCONY):
        return NAWIASEM
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.obejmująca",
    opis="Ile kupuje cudzysłów i ile kupuje nawias.",
    warianty=("bez interpunkcji obejmującej", CUDZYSŁOWEM, NAWIASEM, "olski"),
    grupa=grupa,
    pytania=(
        "oba znaki ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
