"""Te własności bazy sądów, bez których sonda nad nią wydaje liczbę nieprawdziwą.

Baza jest plikiem pisanym ręką, więc psuje się inaczej niż kod. Dwa zdania
wklejone do jednego wpisu wywracają mianownik po cichu, bo sonda pyta o zdanie
pierwsze i o drugim nie mówi nic. Sąd bez powodu jest zdaniem, którego nikt nie
sprawdzi, i tym samym, czym jest wzorzec bez powodu w ``tests/test_wybory.py``.

Zgodność zapisanego wiersza z dzisiejszym jest o gramatyce, a nie o pliku,
i jest bramką rozmyślnie:
sąd przeczytano przy wierszu, który werdykt wypisywał wtedy, więc wiersz ruszony
znaczy, że wpis czeka na przeczytanie na nowo. Czerwony test każe wtedy otworzyć
wpis, a nie poprawić test — dopisanie do gramatyki bywa naprawą tego zdania,
a bywa unieważnieniem sądu nad nim.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.sądy import (
    JEDNOZNACZNE,
    NAD_CZYSTYM,
    NIECZYTANE,
    POTWIERDZONE,
    PRZEOCZONE,
    WIELOZNACZNE,
    ZDJĘTE,
    Sąd,
    czytaj,
    zestaw,
)
from olski.segmentacja import sentences

WPISY = czytaj()


def test_baza_ma_wpisy():
    #  Plik pusty przechodzi każdy test niżej, bo parametryzacja nie ma wtedy
    #  czego zebrać, a sonda nad nim wypisuje same zera.
    assert WPISY


@pytest.mark.parametrize("wpis", WPISY, ids=lambda wpis: wpis.zdanie[:40])
def test_wpis_jest_jednym_zdaniem(wpis):
    assert len(sentences(wpis.zdanie)) == 1


@pytest.mark.parametrize("wpis", WPISY, ids=lambda wpis: wpis.zdanie[:40])
def test_sąd_niesie_powód(wpis):
    assert wpis.powód


@pytest.mark.parametrize("wpis", WPISY, ids=lambda wpis: wpis.zdanie[:40])
def test_zapisane_znalezisko_jest_tym_co_werdykt_wypisuje_dziś(wpis):
    #  Tym samym predykatem, którym wydruk sondy wypisuje wiersz zapisany obok
    #  dzisiejszego: dwa odczyty jednej reguły rozeszłyby się po cichu.
    assert not zestaw(wpis).rozeszło_się


#: Zdania, po jednym na klasę, wraz z tym, czym są dla olskiego dzisiaj.
#: ``Czekają nagrody.`` stoi w bazie i ma dwa odczytania; ``Chałka przewyższa
#: zwykłą bułkę.`` ma jedno, bo przypadki obu grup się nie zlewają
#: (docs/subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego);
#: ``Nowa program`` nie ma wyprowadzenia, bo formy się nie zgadzają.
ZGŁOSZONE = "Czekają nagrody."
JEDNO_ODCZYTANIE = "Chałka przewyższa zwykłą bułkę."
ODRZUCONE = "Nowa program zapisuje ustawienia."


@pytest.mark.parametrize(
    ("sąd", "zdanie", "klasa"),
    [
        (WIELOZNACZNE, ZGŁOSZONE, POTWIERDZONE),
        (JEDNOZNACZNE, ZGŁOSZONE, NAD_CZYSTYM),
        (WIELOZNACZNE, JEDNO_ODCZYTANIE, PRZEOCZONE),
        (JEDNOZNACZNE, JEDNO_ODCZYTANIE, ZDJĘTE),
        (JEDNOZNACZNE, ODRZUCONE, NIECZYTANE),
    ],
)
def test_klasa_bierze_się_z_sądu_i_z_dzisiejszego_znaleziska(sąd, zdanie, klasa):
    #  Para „przeoczone” i „zdjęte” jest tu najdroższa: obie znaczą, że
    #  znaleziska nie ma, a mówią rzecz przeciwną, więc zamienione miejscami
    #  odwracają wniosek, który sonda wydaje, i nie widać tego po wydruku.
    wpis = Sąd(plik="", zdanie=zdanie, znalezisko="", sąd=sąd, powód="powód")
    assert zestaw(wpis).klasa == klasa
