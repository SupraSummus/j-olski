"""Co rozdziela chwyt rejestru od zdania, które tak samo wygląda i chwytem nie jest.

Każda reguła ma tu własne dwa zbiory zdań (``olski/chwyty.py``): jeden ze zdaniami,
które zgłoszenie mają dostać, a drugi z tymi, które tak samo wyglądają i dostać
go nie mają. Każdy warunek reguły zdejmuje inną klasę zdań poprawnych, więc każde
zdanie z drugiego zbioru zdjęte osobno zamienia werdykt tej reguły w przeciwny.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.chwyty import (
    CZASOWNIK_PUSTY,
    PODJĘTE_ZDANIE,
    ZASTĘPCZE_ORZECZENIE,
    chwyty,
)

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
    assert (chwyt.nazwa, chwyt.forma) == (PODJĘTE_ZDANIE, "To")
    assert "wstaw w jego miejsce rzeczownik" in chwyt.naprawa


@pytest.mark.parametrize("zdanie", MILCZY_ORZECZENIE.values(), ids=MILCZY_ORZECZENIE)
def test_zwrot_który_orzeczenia_nie_zastępuje_nie_dostaje_zgłoszenia(zdanie):
    assert chwyty(zdanie) == ()


@pytest.mark.parametrize(
    ("zdanie", "zwrot"), ZGŁASZA_ORZECZENIE.values(), ids=ZGŁASZA_ORZECZENIE
)
def test_zwrot_zamykający_człon_bez_orzeczenia_dostaje_zgłoszenie(zdanie, zwrot):
    (chwyt,) = chwyty(zdanie)
    assert (chwyt.nazwa, chwyt.forma) == (ZASTĘPCZE_ORZECZENIE, zwrot)
    assert "powtórz czasownik" in chwyt.naprawa


#: Zdania, nad którymi reguła o czasowniku pustym milczy; czemu, mówi klucz.
MILCZY_PUSTY = {
    "czasownik orzeka czynność": "Zespół przeanalizował awarię, żeby ustalić jej przyczyny.",
    "rzeczownik zwykły o czytaniu odczasownikowym": (
        "Rada wykonuje zadania, o których mowa w ustawie."
    ),
    "rzeczownik odsunięty od czasownika": "Dokonano wczoraj przeprowadzenia analizy.",
    "czasownik spoza listy": "Opisano przeprowadzenie analizy.",
}

#: Zdania z czasownikiem pustym wraz z parą form, którą wykrywacz ma nazwać.
ZGŁASZA_PUSTY = {
    "forma nieosobowa": (
        "Dokonano przeprowadzenia analizy w celu ustalenia przyczyn awarii.",
        "Dokonano przeprowadzenia",
    ),
    "czynność w podmiocie": ("Nastąpiło uruchomienie systemu.", "Nastąpiło uruchomienie"),
}


@pytest.mark.parametrize("zdanie", MILCZY_PUSTY.values(), ids=MILCZY_PUSTY)
def test_czasownik_orzekający_czynność_nie_dostaje_zgłoszenia(zdanie):
    assert chwyty(zdanie) == ()


@pytest.mark.parametrize(("zdanie", "para"), ZGŁASZA_PUSTY.values(), ids=ZGŁASZA_PUSTY)
def test_czasownik_pusty_przed_rzeczownikiem_odczasownikowym_dostaje_zgłoszenie(zdanie, para):
    (chwyt,) = chwyty(zdanie)
    assert (chwyt.nazwa, chwyt.forma) == (CZASOWNIK_PUSTY, para)
    assert "orzeknij ją czasownikiem" in chwyt.naprawa


def test_zdanie_o_dwóch_chwytach_zgłasza_oba():
    """Zgłoszenia obu reguł idą jedną krotką, a nie pierwsze z nich zamiast obu."""
    formy = [chwyt.forma for chwyt in chwyty("To jest tanie, a szynka odwrotnie.")]
    assert formy == ["To", "odwrotnie"]
