"""Skład: struktura wchodzi, polski tekst wychodzi.

Kalambur nazywa cały ten tor: skład jest łamaniem tekstu, składnia jest budową
zdania, więc łamacz sprawdzający składnię mieści się w jednym słowie.
Wywód, po co ten kierunek stoi obok parsera, trzyma
``docs/design-notes.md``.

Podział jest dwuwarstwowy i to on jest tu decyzją.
``skład.składnia`` trzyma kategorie i konstruktory, czyli to, co da się
powiedzieć, i nie ma w sobie ani przypadka, ani rodzaju, ani szyku.
``skład.morfologia`` trzyma formy, które z tego wychodzą.
Autor pisze drzewo, a zgodność jest liczona po drodze, a nie sprawdzana po niej.

Poziomem tych kategorii jest dziedzina, a nie język.
``Czyj`` mówi, co czego dotyczy, a nie że stoi tam dopełniacz,
i dlatego drzewo nie jest rozbiorem zdania zapisanym z góry.
"""

from skład.morfologia import BrakFormy, odmień, rodzaj_rzeczownika
from skład.składnia import Byt, Czyj, Jaki, Jest, Nominalne, Robi, Rzecz, byt, kompiluj

__all__ = [
    "BrakFormy",
    "Byt",
    "Czyj",
    "Jaki",
    "Jest",
    "Nominalne",
    "Robi",
    "Rzecz",
    "byt",
    "kompiluj",
    "odmień",
    "rodzaj_rzeczownika",
]
