"""Co rozdziela zaimek podejmujący zdanie od zaimka stojącego przy rzeczowniku.

Reguła ma jeden warunek: rzeczownik zgodny z `to` stoi przy nim, czyli przed
orzeczeniem zdania (``olski/chwyty.py``). Zdania niżej są tymi, na których ten
warunek się rozstrzyga, i każde z nich zdjęte osobno zamienia werdykt reguły w
przeciwny.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.chwyty import chwyty

#: Zdania, nad którymi reguła milczy, każde z innego powodu: rzeczownik przy
#: zaimku, rzeczownik odczasownikowy w tej roli, łącznik i zapowiedź
#: podrzędnego.
MILCZY = {
    "przy rzeczowniku": "To zdanie ma dwa czytania.",
    "przy rzeczowniku odczasownikowym": "To przeliczenie rusza werdykt.",
    "łącznik": "Flaga to kawałek tkaniny.",
    "zapowiedź podrzędnego": "To, czy fraza stanęła na nijakiej, nie jest rzeczą.",
}

#: Zdania, w których zaimek podejmuje całe zdanie obok. Ostatnie z nich jest
#: powodem, dla którego zgodności szuka się przed orzeczeniem, a nie w całym
#: zdaniu: `miejsce` zgadza się z `to` w każdej cesze i zaimka nie określa.
ZGŁASZA = {
    "orzecznik przymiotny": "To jest tanie.",
    "orzeczenie bez orzecznika": "To kosztuje.",
    "rzeczownik nijaki za orzeczeniem": "To jest miejsce, gdzie olski milczy.",
}


@pytest.mark.parametrize("zdanie", MILCZY.values(), ids=MILCZY)
def test_zaimek_stojący_przy_swoim_rzeczowniku_nie_jest_chwytem(zdanie):
    """Zgłoszenie chybione kosztuje zdanie przepisane bez powodu, a milczenie zero."""
    assert chwyty(zdanie) == ()


@pytest.mark.parametrize("zdanie", ZGŁASZA.values(), ids=ZGŁASZA)
def test_zaimek_bez_rzeczownika_przy_sobie_dostaje_zgłoszenie(zdanie):
    (chwyt,) = chwyty(zdanie)
    assert chwyt.forma == "To"
    assert "wstaw w jego miejsce rzeczownik" in chwyt.naprawa
