"""Te własności prób, na których stoją liczby wypisywane nad nimi.

Próba jest plikiem pisanym ręką, więc psuje się inaczej niż kod: literówka w
formie gospodarza nie wywraca niczego, tylko cicho robi z wpisu wieczną pomyłkę,
a wpis bez powodu jest sądem, którego nikt nie sprawdzi. Oba są tu pilnowane, bo
oba są niewidoczne w wydruku, i pilnowane są w obu plikach, bo ręka pisze oba.

Nagłówek pilnowany jest z drugiej strony: poprawiony w pliku, a nie w stałej,
wraca przy następnej budowie w wersji starszej i nadpisuje tę prawdziwą.

Ostatnia własność jest o warstwie, a nie o pliku: nad próbą losowaną z całej
populacji warstwa nie myli się ani razu. Jest to jedyne, co
``docs/disambiguation.md`` z tej próby bierze jako własność, a nie jako pomiar, i
jest to własność, którą świadek poluzowany poza swój dowód traci pierwszą. Test
jest przez to bramką rozmyślnie: świadek dopisany jutro ma nad tą próbą albo
trafiać, albo milczeć, a jeśli nie trafia, to czyta się wpis, a nie poprawia test.
Próba zawężona do odpowiedzi takiej bramki nie ma i mieć nie może, bo mierzy się
nad nią właśnie częstość pomyłek.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.wybory import (
    DO_PRZEMILCZENIA,
    NAGŁÓWEK,
    PUSTY,
    WYBORY,
    WYBORY_Z_ODPOWIEDZIĄ,
    Z_CAŁOŚCI,
    Z_ODPOWIEDZIĄ,
    czytaj,
    oceń,
)

#: Obie próby wraz ze zdaniem o losowaniu, którym każda z nich się zaczyna.
PRÓBY = ((WYBORY, Z_CAŁOŚCI), (WYBORY_Z_ODPOWIEDZIĄ, Z_ODPOWIEDZIĄ))
NAZWY = [plik.stem for plik, _ in PRÓBY]

WPISY = czytaj(WYBORY)
WSZYSTKIE = [wpis for plik, _ in PRÓBY for wpis in czytaj(plik)]


@pytest.mark.parametrize("plik", [plik for plik, _ in PRÓBY], ids=NAZWY)
def test_próba_ma_wpisy(plik):
    #  Plik pusty przechodzi każdy test niżej, bo parametryzacja nie ma wtedy
    #  czego zebrać, a sonda nad nim wypisuje same zera.
    assert czytaj(plik)


@pytest.mark.parametrize("wpis", WSZYSTKIE, ids=lambda wpis: wpis.fraza)
def test_wzorzec_jest_gospodarzem_tego_wpisu_albo_nazwaną_ciszą(wpis):
    assert wpis.wzorzec != PUSTY
    assert wpis.wzorzec in (*wpis.gospodarze, *DO_PRZEMILCZENIA)


@pytest.mark.parametrize("wpis", WSZYSTKIE, ids=lambda wpis: wpis.fraza)
def test_wzorzec_niesie_powód(wpis):
    assert wpis.powód


@pytest.mark.parametrize("wpis", WSZYSTKIE, ids=lambda wpis: wpis.fraza)
def test_fraza_stoi_w_zdaniu_tego_wpisu(wpis):
    #  Fraza poprawiona ręką bywa poprawiona w jedną stronę: wpisana z pamięci,
    #  a nie ze zdania. Wtedy świadek dostaje pytanie o wyrażenie, którego w tym
    #  tekście nie ma, i milczy z powodu, którego wydruk nie nazywa.
    assert wpis.fraza in wpis.zdanie


@pytest.mark.parametrize(("plik", "skąd"), PRÓBY, ids=NAZWY)
def test_nagłówek_pliku_jest_tym_który_wypisuje_komenda(plik, skąd):
    assert plik.read_text(encoding="utf-8").startswith(NAGŁÓWEK.format(skąd=skąd))


def test_warstwa_nie_myli_się_nad_próbą_z_całej_populacji():
    ocena = oceń(WPISY)
    assert sum(ocena.odpowiedzi.values()) == sum(ocena.trafień.values())
    assert ocena.przemilczanych == sum(ocena.do_przemilczenia.values())
