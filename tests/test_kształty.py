"""Liczenie kształtów, o które pyta kolejka konstrukcji.

Lasy pisze się tu ręką z tego samego powodu, z którego pisze je
``tests/test_corpus.py``, i tamten moduł jest właścicielem ich budowania.

Sprawdzane jest to, co w tej sondzie może wypaść źle, a nie to, że liczy.
Kształt nie rozdziela apozycji od przydawki dopełniaczowej, rodzeństwo wychodzi
z zejścia w porządku odwrotnym, a bank drzew liczy zaimek zwrotny do klasy
rzeczownika: każda z tych trzech pomyłek wydaje liczbę wyglądającą tak samo
sensownie jak prawdziwa.
"""

import xml.etree.ElementTree as ET

import pytest

pytest.importorskip("morfeusz2")

from harness.kształty import APOZYCJA_BEZ_PRZECINKA, APOZYCJA_Z_PRZECINKIEM, scal, zmierz
from tests.test_corpus import forest, phrase, terminal


def _las(tmp_path, nodes, text="Przyszli moi sąsiedzi, lekarz.", nazwa="las.xml"):
    """Las zapisany na dysk, bo sonda bierze ścieżki, a nie drzewa."""
    ścieżka = tmp_path / nazwa
    ścieżka.write_bytes(ET.tostring(forest(nodes, text=text)))
    return ścieżka


def _grupa(nid, start, end, children, **cechy):
    return phrase(nid, start, end, "fno", children, **cechy)


def apozycja(rule):
    """Dwie grupy imienne pod jedną, zbudowane podaną regułą."""
    return (
        phrase(0, 0, 3, "wypowiedzenie", [1, 9])
        + _grupa(1, 0, 2, [2, 5], rule=rule, klasa="rzecz", lex="sąsiad")
        + _grupa(2, 0, 1, [3], rule="nos", klasa="rzecz", lex="sąsiad")
        + terminal(3, 0, 1, "sąsiedzi", "subst:pl:nom:m1", lemma="sąsiad")
        + _grupa(5, 1, 2, [6], rule="nos", klasa="rzecz", lex="lekarz")
        + terminal(6, 1, 2, "lekarz", "subst:sg:nom:m1", lemma="lekarz")
        + terminal(9, 2, 3, ".", "interp")
    )


def test_apozycja_liczy_się_regułą_bo_kształt_nie_odróżnia_jej_od_przydawki(tmp_path):
    """``sąsiedzi lekarz`` i ``grób męża`` mają jeden kształt i dwie reguły.

    Sonda licząca same dwie córki ``fno`` zsumowałaby apozycję z przydawką
    dopełniaczową, której bank drzew ma kilkadziesiąt razy więcej, i wydałaby
    liczbę mówiącą głównie o tej drugiej.
    """
    z_apozycją = _las(tmp_path, apozycja(APOZYCJA_BEZ_PRZECINKA), nazwa="a.xml")
    przydawka = _las(tmp_path, apozycja("noa1"), nazwa="b.xml")

    assert zmierz([z_apozycją]).zdania["apozycja bez przecinka"] == 1
    assert zmierz([przydawka]).zdania["apozycja bez przecinka"] == 0


def test_zdanie_względne_pod_członem_prawym_nie_liczy_się_jako_brak(tmp_path):
    """Olski wyprowadza ciąg z prawym członem niosącym zdanie względne.

    Rodzeństwo wychodzi z ``constituents`` w porządku odwrotnym do rozpiętości,
    więc sonda biorąca je bez sortowania czytałaby prawy człon jako lewy i
    liczyłaby zdania, których olskiemu nie brakuje.
    """
    nodes = (
        phrase(0, 0, 5, "wypowiedzenie", [1, 11])
        + _grupa(1, 0, 4, [2, 4, 5], rule="nos3", klasa="rzecz", lex="plik")
        + _grupa(2, 0, 1, [3], klasa="rzecz", lex="plik")
        + terminal(3, 0, 1, "pliki", "subst:pl:nom:m3", lemma="plik")
        + phrase(4, 1, 2, "spójnik", [7], rule="sr")
        + terminal(7, 1, 2, "i", "conj")
        + _grupa(5, 2, 4, [6, 8], klasa="rzecz", lex="katalog")
        + terminal(6, 2, 3, "katalogi", "subst:pl:nom:m3", lemma="katalog")
        + phrase(8, 3, 4, "fzd", [9], rule="zd")
        + terminal(9, 3, 4, "rosną", "fin:pl:ter:imperf", lemma="rosnąć")
        + terminal(11, 4, 5, ".", "interp")
    )
    ścieżka = _las(tmp_path, nodes, text="pliki i katalogi, które rosną.")

    assert zmierz([ścieżka]).zdania["człon lewy ciągu ze zdaniem względnym"] == 0


def test_zdanie_względne_pod_członem_lewym_liczy_się_jako_brak(tmp_path):
    nodes = (
        phrase(0, 0, 5, "wypowiedzenie", [1, 11])
        + _grupa(1, 0, 4, [2, 4, 5], rule="nos3", klasa="rzecz", lex="plik")
        + _grupa(2, 0, 2, [3, 8], klasa="rzecz", lex="plik")
        + terminal(3, 0, 1, "pliki", "subst:pl:nom:m3", lemma="plik")
        + phrase(8, 1, 2, "fzd", [9], rule="zd")
        + terminal(9, 1, 2, "rosną", "fin:pl:ter:imperf", lemma="rosnąć")
        + phrase(4, 2, 3, "spójnik", [7], rule="sr")
        + terminal(7, 2, 3, "i", "conj")
        + _grupa(5, 3, 4, [6], klasa="rzecz", lex="katalog")
        + terminal(6, 3, 4, "katalogi", "subst:pl:nom:m3", lemma="katalog")
        + terminal(11, 4, 5, ".", "interp")
    )
    ścieżka = _las(tmp_path, nodes, text="pliki, które rosną, i katalogi.")

    assert zmierz([ścieżka]).zdania["człon lewy ciągu ze zdaniem względnym"] == 1


def celownik(forma, lemat):
    """Celownik pod pozycją luźną, czyli taki, którego schemat czasownika nie żąda."""
    return (
        phrase(0, 0, 3, "wypowiedzenie", [1, 9])
        + phrase(1, 0, 2, "fl", [2], rule="luz")
        + _grupa(2, 0, 2, [3], klasa="rzecz", lex=lemat, przypadek="cel")
        + terminal(3, 0, 2, forma, "subst:sg:dat:m1", lemma=lemat)
        + terminal(9, 2, 3, ".", "interp")
    )


def test_zaimek_zwrotny_nie_liczy_się_do_wolnego_celownika_rzeczownikowego(tmp_path):
    """Bank drzew liczy ``siebie`` do klasy rzeczownika, a olski ma je terminalem.

    Oba lasy niosą tu klasę ``rzecz``, więc podział po samej klasie postawiłby
    je po jednej stronie i zawyżył wiersz, o który pyta wpis kolejki.
    """
    zwrotny = _las(tmp_path, celownik("sobie", "siebie"), nazwa="a.xml")
    rzeczownik = _las(tmp_path, celownik("światu", "świat"), nazwa="b.xml")

    assert zmierz([zwrotny]).zdania["wolny celownik rzeczownikowy"] == 0
    assert zmierz([zwrotny]).zdania["wolny celownik zaimkowy"] == 1
    assert zmierz([rzeczownik]).zdania["wolny celownik rzeczownikowy"] == 1


def test_kawałki_scalone_liczą_to_samo_co_jeden_przebieg(tmp_path):
    """Pula procesów dzieli lasy na kawałki, a wydruk ma z tego nie widzieć nic.

    Przykłady są tu tym, co się psuje: liczniki składają się same, a zdania
    przechodzą przez wybór najkrótszych drugi raz, więc kawałek policzony osobno
    może wnieść zdanie, którego jeden przebieg by nie zachował, albo podnieść
    liczbę, którą już wniósł.
    """
    lasy = [
        _las(tmp_path, apozycja(APOZYCJA_Z_PRZECINKIEM), text=text, nazwa=f"{i}.xml")
        for i, text in enumerate(("Sąsiedzi, lekarz.", "Dorośli, olbrzymy i tak dalej.", "A, b."))
    ]

    razem = zmierz(lasy)
    scalone = scal([zmierz([las]) for las in lasy])

    assert scalone.zdania == razem.zdania
    assert scalone.wystąpienia == razem.wystąpienia
    assert scalone.przykłady == razem.przykłady
    assert scalone.drzewa == razem.drzewa
