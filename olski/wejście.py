"""Czym plik dochodzi do gramatyki, kiedy prozę niesie pod aparatem.

Komendy tej paczki biorą plik, który autor napisał (``olski/check.py``,
``olski/pokrycie.py``), więc rozszerzenie nazwy rozstrzyga, czym ten plik
przeczytać. Deklaracja jest jedna dla obu, bo druga rozeszłaby się z pierwszą na
formacie dopisanym do jednej z nich. Co ekstrakcja po drodze zmyśla, mówi
docs/extraction.md.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from olski.markdown import MARKDOWN_SUFFIX, prose


def _wprost(tekst: str) -> str:
    return tekst


#: Rozszerzenie nazwy pliku → czym wyjąć z niego prozę. Rozszerzenia, którego tu
#: nie ma, nie zgadujemy: plik zwykłego tekstu jest prozą w całości, a format
#: przeczytany na chybił trafił dochodziłby do gramatyki ze swoim aparatem.
CZYTNIKI: dict[str, Callable[[str], str]] = {MARKDOWN_SUFFIX: prose}


def proza(ścieżka: Path) -> str:
    """Proza tego pliku, wyjęta z niego w locie, jeżeli format tego żąda."""
    return CZYTNIKI.get(ścieżka.suffix, _wprost)(ścieżka.read_text(encoding="utf-8"))
