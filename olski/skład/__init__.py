"""Skład: struktura wchodzi, polski tekst wychodzi.

Kalambur nazywa cały ten tor: skład jest łamaniem tekstu, składnia jest budową
zdania, więc łamacz sprawdzający składnię mieści się w jednym słowie.
Wywód, po co ten kierunek stoi obok parsera, trzyma
``docs/design-notes.md``.

Podział na warstwy jest tu decyzją.
Moduły niżej idą od tego, który wie najmniej, do tego, który wie najwięcej.
``olski.skład.kontekst`` trzyma to, czego wypisywane drzewo o sobie nie wie.
``olski.skład.powierzchnia`` trzyma napis wraz z przecinkami,
czyli to, czego żadna kategoria nie zna, a woła każda.
``olski.skład.morfologia`` trzyma formy, które z tego wychodzą.
``olski.skład.grupa`` trzyma kategorie niosące rzecz, czyli to,
czym wypełnia się pozycje zdania.
``olski.skład.składnia`` trzyma kategorie orzekające i ich konstruktory,
czyli zdanie wraz z tym, co w nim staje,
i nie ma w sobie ani przypadka, ani rodzaju, ani szyku.
``olski.skład.opowieść`` trzyma to, co widać dopiero nad kilkoma zdaniami naraz:
czas opowiadania i tożsamość tego, o kim mowa.
Autor pisze drzewo, a zgodność jest liczona po drodze, a nie sprawdzana po niej.
Liczona jest zgodność, a nie wszystko: rama czasownika przychodzi z leksykonu,
więc drzewo, które żąda dopełnienia od czasownika biorącego co innego,
zgłasza się przez ``PozaRamą``, zamiast powstać.
Rekcja przyimka przychodzi tak samo, z ``olski.skład.przyimki``,
a który leksem stoi pod nazwą, mówi ``olski.skład.leksemy``,
bo lemat go nie wskazuje, a od wyboru zależy znaczenie zdania.
"""

from olski.skład.grupa import (
    Byt,
    Czyj,
    Jaki,
    Koordynacja,
    Nominalne,
    Rola,
    Rzecz,
    Wyróżnienie,
    byt,
)
from olski.skład.kontekst import Kontekst
from olski.skład.leksemy import LEKSEMY, leksem
from olski.skład.morfologia import (
    BrakFormy,
    WieleLeksemów,
    odmień,
    rodzaj_rzeczownika,
)
from olski.skład.opowieść import Akapit, Opowieść, Postać
from olski.skład.powierzchnia import Kawałek
from olski.skład.przegląd import Kolizja, przejrzyj
from olski.skład.przyimki import PRZYIMKI, przypadek
from olski.skład.składnia import (
    Ciąg,
    Jest,
    Komu,
    Okolicznik,
    Opis,
    PozaRamą,
    Przysłówek,
    Robi,
    Treść,
    Zdanie,
    kompiluj,
    nie,
    po_poprzednim,
    pomijalny,
    zdarzenie,
)
from olski.skład.spójniki import SPÓJNIKI, staje_na_czele, wprowadza

__all__ = [
    "LEKSEMY",
    "PRZYIMKI",
    "Akapit",
    "BrakFormy",
    "Byt",
    "Ciąg",
    "Czyj",
    "Jaki",
    "Jest",
    "Kawałek",
    "Kolizja",
    "Komu",
    "Kontekst",
    "Koordynacja",
    "Nominalne",
    "Okolicznik",
    "Opis",
    "Opowieść",
    "Postać",
    "PozaRamą",
    "Przysłówek",
    "Robi",
    "Rola",
    "Rzecz",
    "SPÓJNIKI",
    "Treść",
    "WieleLeksemów",
    "Wyróżnienie",
    "Zdanie",
    "byt",
    "kompiluj",
    "leksem",
    "nie",
    "odmień",
    "po_poprzednim",
    "pomijalny",
    "przejrzyj",
    "przypadek",
    "rodzaj_rzeczownika",
    "staje_na_czele",
    "wprowadza",
    "zdarzenie",
]
