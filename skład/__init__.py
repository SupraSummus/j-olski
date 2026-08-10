"""Skład: struktura wchodzi, polski tekst wychodzi.

Kalambur nazywa cały ten tor: skład jest łamaniem tekstu, składnia jest budową
zdania, więc łamacz sprawdzający składnię mieści się w jednym słowie.
Wywód, po co ten kierunek stoi obok parsera, trzyma
``docs/design-notes.md``.

Podział jest trójwarstwowy i to on jest tu decyzją.
``skład.składnia`` trzyma kategorie i konstruktory, czyli to, co da się
powiedzieć, i nie ma w sobie ani przypadka, ani rodzaju, ani szyku.
``skład.morfologia`` trzyma formy, które z tego wychodzą.
``skład.opowieść`` trzyma to, co widać dopiero nad kilkoma zdaniami naraz:
czas opowiadania i tożsamość tego, o kim mowa.
Autor pisze drzewo, a zgodność jest liczona po drodze, a nie sprawdzana po niej.
Liczona jest zgodność, a nie wszystko: rama czasownika przychodzi z leksykonu,
więc drzewo, które żąda dopełnienia od czasownika biorącego co innego,
zgłasza się przez ``PozaRamą``, zamiast powstać.
Rekcja przyimka przychodzi tak samo, z ``skład.przyimki``,
a który leksem stoi pod nazwą, mówi ``skład.leksemy``,
bo lemat go nie wskazuje, a od wyboru zależy znaczenie zdania.

Poziomem tych kategorii jest dziedzina, a nie język.
``Czyj`` mówi, co czego dotyczy, a nie że stoi tam dopełniacz,
``Dokąd`` mówi, że coś jest celem, a nie że stoi tam biernik,
i dlatego drzewo nie jest rozbiorem zdania zapisanym z góry.
"""

from skład.leksemy import LEKSEMY, leksem
from skład.morfologia import (
    BrakFormy,
    WieleLeksemów,
    odmień,
    rodzaj_rzeczownika,
)
from skład.opowieść import Akapit, Opowieść, Postać
from skład.przyimki import PRZYIMKI, przypadek
from skład.składnia import (
    Byt,
    Ciąg,
    Czyj,
    Jaki,
    Jest,
    Kawałek,
    Kontekst,
    Koordynacja,
    Nominalne,
    Okolicznik,
    Opis,
    PozaRamą,
    Przysłówek,
    Robi,
    Rola,
    Rzecz,
    Wyróżnienie,
    Zdanie,
    byt,
    kompiluj,
    nie,
    pomijalny,
    zdarzenie,
)
from skład.spójniki import SPÓJNIKI, staje_na_czele, wprowadza

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
    "WieleLeksemów",
    "Wyróżnienie",
    "Zdanie",
    "byt",
    "kompiluj",
    "leksem",
    "nie",
    "odmień",
    "pomijalny",
    "przypadek",
    "rodzaj_rzeczownika",
    "staje_na_czele",
    "wprowadza",
    "zdarzenie",
]
