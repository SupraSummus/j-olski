"""Korpus w Markdownie, drzewo plików prozy na wyjściu.

Prozę jednego dokumentu wyjmuje ``olski/markdown.py``, bo o nią pyta autor
sprawdzający własny plik. Tutaj zostaje sama deklaracja komendy korpusowej:
jednostka, którą waży wybór po języku, i to, czym komenda przedstawia się w
pomocy (``uruchom`` w ``harness/__init__.py``).
"""

from __future__ import annotations

from collections.abc import Sequence

from harness import Czytnik, Jednostka, uruchom
from olski.markdown import MARKDOWN_SUFFIX, prose


def jednostki(text: str) -> list[Jednostka]:
    """Cały dokument, bo dokument jest napisany w jednym języku.

    Ekstrakcja z modułu tnie plik na docstringi i komentarze, każdy z osobna,
    a dokument tnie się na sekcje, których ten krok nie zna: sekcja jest
    nagłówkiem plus prozą pod nim, a tu nagłówki już poszły. todo/ trzyma to
    jako wpis, bo płaci za to dokument pisany w dwóch językach naraz.
    """
    return [Jednostka(1, prose(text).rstrip("\n"))]


# --------------------------------------------------------------------------- #
# The command line
# --------------------------------------------------------------------------- #

USAGE = """
  python3 -m harness.markdown notes/ --into prose/    a tree of notes
  python3 -m harness.markdown note.md --into prose/   one file
"""


CZYTNIK = Czytnik(
    komenda="harness.markdown",
    sufiks=MARKDOWN_SUFFIX,
    nazwa_jednostki="document",
    opis="Extract Polish prose from Markdown, for olski to measure.",
    użycie=USAGE,
    jednostki=jednostki,
)


def main(argv: Sequence[str] | None = None) -> int:
    return uruchom(CZYTNIK, argv)


if __name__ == "__main__":
    raise SystemExit(main())
