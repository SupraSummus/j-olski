"""Słownictwo projektu: lematy, o których projekt orzeka sam.

Wykluczenie słownikowe (``admissible`` w ``olski/segmentacja.py``) jest zakładem
o rejestr, a nie zdaniem o polszczyźnie: `Go jest grą.` polszczyzna ma.
Zakład zostaje domyślnością, a sekcja ``lematy`` konfiguracji projektu
(``olski/konfiguracja.py``) uchyla go na jednym lemacie (:data:`WPUSZCZANE`)
albo odbiera lematowi czytania tam, gdzie tamto kryterium sięgnąć nie może
(:data:`POMIJANE`).

Wywód obu kierunków wraz z ich ceną trzyma
docs/subset.md#słownictwo-projektu-orzeka-o-lemacie-w-obie-strony.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from olski.konfiguracja import LEMATY, ZłaKonfiguracja, napisy, sekcja

#: Klucz, pod którym stoją lematy używane mimo wykluczenia słownikowego.
WPUSZCZANE = "wpuszczane"

#: Klucz, pod którym stoją lematy, których projekt nie używa wcale.
POMIJANE = "pomijane"

KLUCZE = (WPUSZCZANE, POMIJANE)


@dataclass(frozen=True)
class Słownictwo:
    """Co projekt orzeka o lematach, w obu kierunkach naraz.

    Wartość domyślna jest projektem bez tej sekcji i wchodzi argumentem
    domyślnym do warunków w ``olski/segmentacja.py``, więc kto czyta jedno
    zdanie dwiema deklaracjami, podaje swoją zamiast podmieniać stałą.
    """

    #: Lematy, których projekt używa mimo wykluczenia słownikowego.
    wpuszczane: frozenset[str] = frozenset()
    #: Lematy, których projekt nie używa wcale.
    pomijane: frozenset[str] = frozenset()


def czytaj(dane: Mapping[str, Any]) -> Słownictwo:
    """Słownictwo z sekcji konfiguracji.

    Lemat stojący w obu kierunkach naraz zgłasza się,
    bo dwie takie deklaracje znoszą się nawzajem,
    a rozstrzygnięcie po cichu byłoby regułą, której nikt nie zadeklarował.
    """
    wpuszczane = napisy(LEMATY, WPUSZCZANE, dane)
    pomijane = napisy(LEMATY, POMIJANE, dane)
    obydwa = wpuszczane & pomijane
    if obydwa:
        raise ZłaKonfiguracja(
            f"sekcja {LEMATY}: lemat stoi w obu kierunkach naraz: {', '.join(sorted(obydwa))}"
        )
    return Słownictwo(wpuszczane=wpuszczane, pomijane=pomijane)


#: Słownictwo tego projektu, przeczytane przy imporcie.
SŁOWNICTWO = czytaj(sekcja(LEMATY, KLUCZE))
