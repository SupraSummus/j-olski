"""Osoby projektu: lematy, którymi ten rejestr nazywa kogoś.

Plik żądań mówi, czego czasownik żąda od słowa stojącego w jego pozycji,
i nie mówi, czy słowo to żądanie spełnia (``olski/żądania.py``).
Dla klas osobowych odpowiada ta deklaracja, a dla pozostałych wordnet,
którego to repozytorium nie ma.
Deklaracja jest zamknięta, czyli lemat spoza niej nikogo nie nazywa,
a wywód tego kierunku wraz z jego ceną trzyma
docs/walencja.md#deklaracja-projektu-rozstrzyga-żądanie-osoby.

Sekcję czyta ten moduł, a jej strukturę ``olski/konfiguracja.py``,
tak samo jak przy słownictwie projektu (``olski/słownictwo.py``).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from olski.konfiguracja import OSOBY, napisy, sekcja

#: Klucz, pod którym stoją lematy nazywające kogoś.
LEMATY = "lematy"


@dataclass(frozen=True)
class Osoby:
    """Lematy, którymi ten projekt nazywa kogoś.

    Wartość domyślna jest projektem bez tej sekcji i wchodzi argumentem
    domyślnym tam, gdzie się o nią pyta, tak samo jak słownictwo projektu:
    kto czyta jedno zdanie dwiema deklaracjami, podaje swoją zamiast
    podmieniać stałą.
    """

    lematy: frozenset[str] = frozenset()

    def nazywają(self, lematy: Iterable[str]) -> bool:
        """Czy któryś z tych lematów nazywa kogoś.

        Któryś, a nie każdy, bo forma bywa dwoma słowami naraz
        i czytanie nie mówi, którym z nich stoi
        (:meth:`olski.parse.Node.signature`),
        więc wątpliwość milczy tu tak samo jak po stronie żądania
        (:func:`olski.żądania.żądane`).
        """
        return any(lemat in self.lematy for lemat in lematy)


#: Osoby tego projektu, przeczytane przy imporcie.
OSOBY_PROJEKTU = Osoby(napisy(OSOBY, LEMATY, sekcja(OSOBY, (LEMATY,))))
