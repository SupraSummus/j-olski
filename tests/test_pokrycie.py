"""Kolejka blokerów i krzywa pokrycia nad plikiem prozy.

Liczba pokrycia nad własnym dokumentem stoi w miejscu, dopóki zdania są długie,
a rusza się kolejka pod nią, więc te dwie tabele są tym, po co ktoś tu sięga
(docs/pisanie-po-olsku.md). Testy pytają o wiersz, który ta kolejka nazywa,
bo nazwa formy jest tym, co czytelnik z niej bierze.

Nad bankiem drzew liczy te same tabele ``harness/pomiar.py`` i tam stoją
pytania o drzewo wzorcowe, których proza nie ma z czym porównać.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.pokrycie import NO_LICENCE, NO_STRUCTURE, main, nad_prozą, render


def test_przebieg_nad_prozą_liczy_kolejkę_blokerów_i_krzywą_długości():
    #  Kolejka i krzywa są tym, po co ktoś sięga nad własnym dokumentem.
    raport = nad_prozą(
        "Zapisz plik konfiguracyjny. Nowa program zapisuje ustawienia w pliku konfiguracyjnym."
    )
    assert raport.statuses == {"valid": 1, "rejected": 1}
    #  Analiza dochodzi tu do końca i nie domyka zdania, bo tablica domyka pozycję
    #  po samym kształcie ciała, a o cechy pyta dopiero unifikacja po lesie
    #  (tests/test_subset.py stoi na tej samej różnicy),
    #  więc wiersz jest tym jednym, który nie nazywa żadnej formy.
    assert raport.blockers == {NO_STRUCTURE: 1}
    assert raport.lengths == {"1-5": {"valid": 1}, "6-10": {"rejected": 1}}


def test_wiersz_kolejki_nazywa_czytanie_po_które_gramatyka_sięga():
    #  Morfeusz czyta `i` najpierw jako wykrzyknik, a olski bierze pod tą formą
    #  spójnik, więc wiersz nazwany czytaniem pierwszym obiecywałby konstrukcję,
    #  której nikt nie zbuduje, a ta chowałaby się pod nim. Zdanie stawia przed
    #  spójnikiem przecinek, którego polszczyzna tam nie stawia (docs/subset.md),
    #  więc analiza staje właśnie na tej formie.
    assert nad_prozą("Cena rośnie, i linter sprawdza tekst.").blockers == {"conj": 1}


def test_forma_bez_czytań_po_wykluczeniu_nie_wpada_do_wiersza_zdania_bez_struktury():
    #  `po_przyimku` zdejmuje `niego` wszystkie czytania, bo przyimka przed nim nie
    #  ma, więc analiza staje na tej formie, a nie na końcu zdania. Liczone razem,
    #  oba zdarzenia obiecują konstrukcję domykającą całość, choć werdykt nad tym
    #  zdaniem wypisuje samą formę (`bez_licencji` w `olski/segmentacja.py`).
    assert nad_prozą("Cena niego rośnie.").blockers == {NO_LICENCE: 1}


def test_proza_nie_dostaje_wierszy_o_zgodności_z_drzewem_wzorcowym():
    #  Usterka, którą to łapie: wiersz o zgodności ról stojący nad zdaniem, o
    #  którym nikt nie wie, gdzie ma podmiot. Liczników na to ten raport nie ma
    #  wcale, bo niosą je drzewa wzorcowe (``RaportZłoty`` w ``harness/pomiar.py``),
    #  a wydruk jest tym, przez co usterka by wyszła.
    assert "gold tree" not in render(nad_prozą("Zapisz plik konfiguracyjny."), "proza.txt")


def test_fragment_prozy_wchodzi_do_niemierzonych_a_nie_do_odrzuconych():
    #  Nagłówek i pozycja listy dochodzą tu akapitem tak samo jak zdanie, a
    #  policzone jako odrzucone mierzyłyby ekstrakcję zamiast podzbioru.
    raport = nad_prozą("Nagłówek bez kropki\n\nZapisz plik konfiguracyjny.")
    assert raport.statuses == {"valid": 1}
    assert sum(raport.skipped.values()) == 1


def test_przebieg_nad_prozą_nazywa_pliki_a_nie_bank_drzew(tmp_path, capsys):
    #  Nagłówek wydruku mówi, po czym wyszła liczba, i nad prozą nie ma prawa
    #  powiedzieć „Składnica”; tabeli składu korpusu ten raport nie ma wcale.
    ścieżka = tmp_path / "proza.txt"
    ścieżka.write_text("Zapisz plik konfiguracyjny.", encoding="utf-8")
    assert main([str(ścieżka)]) == 0
    wydruk = capsys.readouterr().out
    assert wydruk.startswith("proza.txt, live morphology")
    assert "forests" not in wydruk


def test_katalog_podany_obok_pliku_jest_odmówiony_a_nie_czytany(tmp_path, capsys):
    #  Ten przebieg czyta pliki prozy i nic poza nimi, więc katalog jest tu
    #  pomyłką, której nie wolno przeczytać jako pliku. Bank drzew chodzi osobną
    #  komendą (``harness/pomiar.py``).
    (tmp_path / "proza.txt").write_text("Zapisz plik.", encoding="utf-8")
    assert main([str(tmp_path / "proza.txt"), str(tmp_path)]) == 2
    assert "nie ma takiego pliku" in capsys.readouterr().err


