"""Konfiguracja projektu, czyli jeden plik pisany ręką i jego usterki.

Plik ten odbiera zdaniom czytania i dokłada je, więc usterka w nim rusza werdykt
o cudzym tekście. Pilnowane jest przez to jedno: że każda usterka zgłasza się i
nazywa miejsce, zamiast wejść w analizę po cichu.

Co znaczy przeczytana deklaracja, pilnują ``tests/test_projekt.py`` oraz
``tests/test_słownictwo.py``: struktura jest tutaj, znaczenie tam.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.konfiguracja import LEKSYKON, LEMATY, NAZWA, ZłaKonfiguracja, czytaj, sekcja, znajdź
from olski.projekt import WPISY_KLUCZ
from olski.projekt import czytaj as wpisy
from olski.słownictwo import KLUCZE, POMIJANE, WPUSZCZANE
from olski.słownictwo import czytaj as słownictwo


def plik(tmp_path, treść):
    kandydat = tmp_path / NAZWA
    kandydat.write_text(treść, encoding="utf-8")
    return kandydat


def test_konfiguracja_znajduje_się_z_podkatalogu_projektu(tmp_path):
    #  Projekt ma podkatalogi, więc szukanie w samym katalogu roboczym gubiłoby
    #  deklarację każdemu, kto woła olskiego spod `docs/` albo spod `src/`.
    #  Szuka się w górę, tak jak szuka się `.editorconfig`.
    plik(tmp_path, f"[{LEMATY}]\n{POMIJANE} = ['soba']\n")
    głęboko = tmp_path / "docs" / "wewnątrz"
    głęboko.mkdir(parents=True)
    assert znajdź(głęboko) == tmp_path / NAZWA


def test_projekt_bez_konfiguracji_nie_zgłasza_braku(tmp_path):
    #  Brak jest stanem zwykłym: kto sprawdza cudzy tekst, tego pliku nie ma, a
    #  wyjątek zamiast tego wywracałby import całego olskiego.
    assert znajdź(tmp_path) is None


def test_sekcja_nazwana_inaczej_zgłasza_się_zamiast_zostać_przemilczana(tmp_path):
    #  Deklaracja, której nikt nie przeczytał, jest gorsza od jej braku: autor
    #  widzi plik, w którym coś napisał, a werdykty ma takie jak bez niego.
    with pytest.raises(ZłaKonfiguracja, match="sekcjami"):
        czytaj(plik(tmp_path, "[slowa]\nwpisy = []\n"))


def test_klucz_nazwany_inaczej_zgłasza_się_z_tego_samego_powodu(tmp_path):
    #  Literówka w kluczu jest usterką tego samego rodzaju co literówka w nazwie
    #  sekcji, więc dostaje ten sam komunikat i pada w tym samym miejscu.
    wczytane = czytaj(plik(tmp_path, f"[{LEMATY}]\nwpuszczone = ['go']\n"))
    with pytest.raises(ZłaKonfiguracja, match="kluczami"):
        sekcja(LEMATY, KLUCZE, wczytane)


@pytest.mark.parametrize(
    "treść, urywek",
    [
        #  Wpis o dwóch polach jest wpisem, któremu ktoś nie dopisał świadka, a
        #  bez świadka wzorzec dobrany źle wydaje formę, której polszczyzna nie ma.
        ("wpisy = [['commit', 'bat:Sm3~a']]", "lemat, leksem i świadek"),
        #  Napis w miejscu wpisu jest wierszem starego formatu wklejonym tutaj.
        ("wpisy = ['commit\tbat:Sm3~a\tcommita']", "lemat, leksem i świadek"),
    ],
)
def test_zły_wpis_leksykonu_zgłasza_się_zamiast_wejść_w_analizę(tmp_path, treść, urywek):
    wczytane = czytaj(plik(tmp_path, f"[{LEKSYKON}]\n{treść}\n"))
    with pytest.raises(ZłaKonfiguracja, match=urywek):
        wpisy(sekcja(LEKSYKON, (WPISY_KLUCZ,), wczytane))


def test_lemat_w_obu_kierunkach_zgłasza_się_zamiast_dać_jednemu_wygrać(tmp_path):
    #  Dwie takie deklaracje znoszą się nawzajem i żadna nie mówi, która miała
    #  wygrać, a rozstrzygnięcie po cichu byłoby regułą, której nikt nie
    #  zadeklarował.
    treść = f"[{LEMATY}]\n{WPUSZCZANE} = ['go']\n{POMIJANE} = ['go']\n"
    wczytane = czytaj(plik(tmp_path, treść))
    with pytest.raises(ZłaKonfiguracja, match="w obu kierunkach"):
        słownictwo(sekcja(LEMATY, KLUCZE, wczytane))


def test_lista_lematów_jest_listą_napisów(tmp_path):
    #  Napis w miejscu listy przeszedłby jako zbiór swoich liter, więc projekt
    #  deklarujący `go` pomijałby lematy `g` i `o`.
    wczytane = czytaj(plik(tmp_path, f"[{LEMATY}]\n{POMIJANE} = 'soba'\n"))
    with pytest.raises(ZłaKonfiguracja, match="listą napisów"):
        słownictwo(sekcja(LEMATY, KLUCZE, wczytane))
