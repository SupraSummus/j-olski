"""Że sonda cen mierzy kolejność, a nie to, co się wyprowadza.

Sonda składa wariant przepisując produkcje olskiego z jedną pozycją zdjętą
z rachunku (``harness/cena.py``), i cała jej wiarygodność stoi na tym, że taki
wariant wyprowadza dokładnie to, co olski.
Pomyłka prawdopodobna jest tu jedna i cicha: dwie produkcje różniące się samym
rachunkiem zlałyby się po zdjęciu pozycji w jedną, więc zdanie dostałoby pod
wariantem inną liczbę czytań, a wydruk czytałby się jak pomiar ceny.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.cena import bez_pozycji, pozycje_produkcji, przebieg
from olski.cennik import CENNIK, OKOLICZNIK
from olski.rejestr import POZA_REJESTREM, pozycje
from olski.subset import GRAMMAR


def test_wyceniana_jest_każda_pozycja_poza_tą_której_nie_płaci_produkcja():
    """Pozycje bierze się z gramatyki, więc dopisana do produkcji wchodzi tu sama.

    Wypisane zamiast wyprowadzonych dałyby wariant, który pozycji morfologii nie
    zdejmuje, bo płaci ją rozbiór; sonda meldowałaby nad nią zero i to zero
    czytałoby się jak pomiar.
    """
    assert set(pozycje_produkcji()) == set(CENNIK) - set(pozycje(POZA_REJESTREM))


def test_wariant_ma_tyle_samo_produkcji_co_olski_bo_zdejmuje_cenę_a_nie_ciało():
    """Produkcja zostaje, a ubywa jej rachunek; zlana z drugą znaczyłaby czytanie mniej."""
    tańsza = bez_pozycji(OKOLICZNIK)
    assert len(tańsza.productions) == len(GRAMMAR.productions)
    assert not any(OKOLICZNIK in produkcja.koszty for produkcja in tańsza.productions)
    assert any(produkcja.koszty for produkcja in tańsza.productions)


def test_zdanie_któremu_cena_przestawia_czytanie_pierwsze_wchodzi_do_przykładów(tmp_path):
    """Przebieg nad plikiem prozy: mianownik, brak rozjazdu i oba czytania pierwsze.

    `Role opisuje docs/roles.md.` czyta się z nazwą pliku w podmiocie albo
    w okoliczniku narzędnikowym, a bez ceny okolicznika oba czytania kosztują
    tyle samo i przodem wychodzi to bez podmiotu.
    """
    plik = tmp_path / "proza.txt"
    plik.write_text("Role opisuje docs/roles.md.\n", encoding="utf-8")
    raport = przebieg([plik], [OKOLICZNIK])
    assert (raport.zdań, raport.wieloznaczne) == (1, 1)
    assert raport.rozjechane == {}
    (zdanie, u_olskiego, w_wariancie) = raport.przykłady[OKOLICZNIK][0]
    assert zdanie == "Role opisuje docs/roles.md."
    assert "podmiot" in u_olskiego[0]
    assert "podmiot" not in w_wariancie[0]
