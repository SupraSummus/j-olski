"""Te własności próby, na których stoi liczba wypisywana nad nią.

Próba jest plikiem pisanym ręką, więc psuje się inaczej niż kod: literówka w
formie gospodarza nie wywraca niczego, tylko cicho robi z wpisu wieczną pomyłkę,
a wpis bez powodu jest sądem, którego nikt nie sprawdzi. Oba są tu pilnowane, bo
oba są niewidoczne w wydruku.

Trzecia własność jest o warstwie, a nie o pliku: nad tą próbą warstwa nie myli
się ani razu. Jest to jedyne, co ``docs/disambiguation.md`` z tej próby bierze
jako własność, a nie jako pomiar, i jest to własność, którą świadek poluzowany
poza swój dowód traci pierwszą. Test jest przez to bramką rozmyślnie: świadek
dopisany jutro ma nad tą próbą albo trafiać, albo milczeć, a jeśli nie trafia,
to czyta się wpis, a nie poprawia test.
"""

import pytest

pytest.importorskip("morfeusz2")

from sonda.wybory import DO_PRZEMILCZENIA, PUSTY, WYBORY, czytaj, oceń

WPISY = czytaj(WYBORY)


def test_próba_ma_wpisy():
    #  Plik pusty przechodzi każdy test niżej, bo parametryzacja nie ma wtedy
    #  czego zebrać, a sonda nad nim wypisuje same zera.
    assert WPISY


@pytest.mark.parametrize("wpis", WPISY, ids=lambda wpis: wpis.fraza)
def test_wzorzec_jest_gospodarzem_tego_wpisu_albo_nazwaną_ciszą(wpis):
    assert wpis.wzorzec != PUSTY
    assert wpis.wzorzec in (*wpis.gospodarze, *DO_PRZEMILCZENIA)


@pytest.mark.parametrize("wpis", WPISY, ids=lambda wpis: wpis.fraza)
def test_wzorzec_niesie_powód(wpis):
    assert wpis.powód


@pytest.mark.parametrize("wpis", WPISY, ids=lambda wpis: wpis.fraza)
def test_fraza_stoi_w_zdaniu_tego_wpisu(wpis):
    #  Fraza poprawiona ręką bywa poprawiona w jedną stronę: wpisana z pamięci,
    #  a nie ze zdania. Wtedy świadek dostaje pytanie o wyrażenie, którego w tym
    #  tekście nie ma, i milczy z powodu, którego wydruk nie nazywa.
    assert wpis.fraza in wpis.zdanie


def test_warstwa_nie_myli_się_nad_tą_próbą():
    ocena = oceń(WPISY)
    assert sum(ocena.odpowiedzi.values()) == sum(ocena.trafień.values())
    assert ocena.przemilczanych == sum(ocena.do_przemilczenia.values())
