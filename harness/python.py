"""Pakiet w Pythonie, drzewo plików prozy na wyjściu.

Prozę jednego modułu wyjmuje ``olski/python.py``, bo o nią pyta autor
sprawdzający własny plik. Tutaj zostaje sama deklaracja komendy korpusowej:
jednostka, którą waży wybór po języku, i to, czym komenda przedstawia się w
pomocy (``uruchom`` w ``harness/__init__.py``).

Jednostek jest tu tyle, ile moduł ma docstringów i bloków komentarza, a nie
jedna na plik jak w ``harness/markdown.py``, i dlatego ta komenda ma nad czym
stanąć: moduł miesza dwa języki z założenia (``olski/python.py``).
"""

from __future__ import annotations

from collections.abc import Sequence

from harness import Czytnik, Jednostka, uruchom
from olski.python import PYTHON_SUFFIX
from olski.python import jednostki as kawałki


def jednostki(text: str) -> list[Jednostka]:
    """Docstring i blok komentarza, każdy osobno, wraz z wierszem, w którym stoi."""
    return [Jednostka(wiersz, tekst) for wiersz, tekst in kawałki(text)]


# --------------------------------------------------------------------------- #
# The command line
# --------------------------------------------------------------------------- #

USAGE = """
  python3 -m harness.python olski/ --into prose/            a package
  python3 -m harness.python olski/werdykt.py --into prose/  one module
"""


CZYTNIK = Czytnik(
    komenda="harness.python",
    sufiks=PYTHON_SUFFIX,
    nazwa_jednostki="comment or docstring",
    opis="Extract Polish prose from Python comments and docstrings.",
    użycie=USAGE,
    jednostki=jednostki,
)


def main(argv: Sequence[str] | None = None) -> int:
    return uruchom(CZYTNIK, argv)


if __name__ == "__main__":
    raise SystemExit(main())
