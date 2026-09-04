"""Co rozdziela chwyt rejestru od zdania, które tak samo wygląda i chwytem nie jest.

Reguły są dwie i każda ma tu własne dwa zbiory zdań (``olski/chwyty.py``).
Reguła o zaimku ma jeden warunek: rzeczownik zgodny z `to` stoi przy nim, czyli
przed orzeczeniem zdania. Reguła o domyślnym orzeczeniu ma trzy, bo każdy z nich
zdejmuje inną klasę zdań poprawnych. Każde zdanie niżej zdjęte osobno zamienia
werdykt swojej reguły w przeciwny.
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


#: Zdania, nad którymi reguła o domyślnym orzeczeniu milczy; czemu, mówi klucz.
MILCZY_ORZECZENIE = {
    "porównanie w tym samym członie": "Rolę tę bierze z lasu, tak samo jak liczbę czytań.",
    "porównanie odcięte przecinkiem": "Rusza werdykt, czyli tak samo, jak rusza go cena.",
    "forma osobowa w członie": "Tak samo przyjmujemy reguły prozy.",
    "orzeczenie bez formy osobowej": "Dowieść jej trzeba tak samo.",
    "zdanie ucięte ekstrakcją": "tak samo, a Dokument mówi, że cena jest niska.",
}

#: Zdania z takim zwrotem wraz ze zwrotem, który wykrywacz ma w nich nazwać.
ZGŁASZA_ORZECZENIE = {
    "na końcu zdania": ("Każda córka schodzi do niczego, więc ciało też.", "też"),
    "w środku zdania": (
        "Bank drzew ma wzorzec, a korpus audytowy odwrotnie, więc wzorzec czyta się ręką.",
        "odwrotnie",
    ),
    "zwrot dwuwyrazowy": (
        "Nad Składnicą nie kupuje ani jednego zdania, pod Morfeuszem tak samo.",
        "tak samo",
    ),
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


@pytest.mark.parametrize("zdanie", MILCZY_ORZECZENIE.values(), ids=MILCZY_ORZECZENIE)
def test_zwrot_który_orzeczenia_nie_zastępuje_nie_dostaje_zgłoszenia(zdanie):
    assert chwyty(zdanie) == ()


@pytest.mark.parametrize(
    ("zdanie", "zwrot"), ZGŁASZA_ORZECZENIE.values(), ids=ZGŁASZA_ORZECZENIE
)
def test_zwrot_zamykający_człon_bez_orzeczenia_dostaje_zgłoszenie(zdanie, zwrot):
    (chwyt,) = chwyty(zdanie)
    assert chwyt.forma == zwrot
    assert "powtórz czasownik" in chwyt.naprawa


def test_zdanie_o_dwóch_chwytach_zgłasza_oba():
    """Zgłoszenia obu reguł idą jedną krotką, a nie pierwsze z nich zamiast obu."""
    formy = [chwyt.forma for chwyt in chwyty("To jest tanie, a szynka odwrotnie.")]
    assert formy == ["To", "odwrotnie"]
