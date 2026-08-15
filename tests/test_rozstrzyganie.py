"""Te własności warstwy rozstrzygającej, na których stoi jej prawo do istnienia.

Warstwa jest zalążkiem i większość tego, co mówi, mówi tabelą przeliczaną z banku
drzew, której nikt tu nie pilnuje. Trzy rzeczy są inne, bo bez nich zalążek jest
nie tyle niedokończony, co szkodliwy: że milczy, kiedy nie ma na czym stanąć, że
wskazanie przychodzi z liczbami, i że werdykt zostaje nietknięty.

Czwarta jest o kolejności świadków, bo na niej stoi obietnica z docstringa
``olski/rozstrzyganie.py``: dowód słownikowy bije statystyczny, a nie odwrotnie.

Świadka każdy test buduje sam, z licznika wypisanego na miejscu, zamiast czytać
``olski/skłonności.txt``. Plik ten jest generowany, więc test na nim oparty
pilnowałby banku drzew, a nie warstwy, i milkłby razem z nim.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.parse import Przyłączenie
from olski.rozstrzyganie import Rozstrzygnięcie, Skłonność, rozstrzygnij
from olski.subset import check

#: Przyłączenie, jakie werdykt wydaje nad ``Daj przepis na faworki.``
FAWORKI = Przyłączenie(modyfikator="na faworki", gospodarze=("Daj", "przepis"))

#: Licznik, przy którym świadek odpowiada: cztery wystąpienia, wszystkie w jedną stronę.
JEDNOZNACZNY = {("na", "noun", "przepis"): (4, 4)}


@pytest.mark.parametrize(
    ("licznik", "dlaczego"),
    [
        ({}, "bez tabeli, czyli po świeżej instalacji"),
        ({("na", "noun", "przepis"): (1, 1)}, "poniżej progu wsparcia"),
        ({("na", "noun", "przepis"): (5, 10)}, "gdy bank drzew przyłącza i tak, i tak"),
    ],
    ids=["bez tabeli", "poniżej wsparcia", "bez przewagi"],
)
def test_świadek_milczy_zamiast_zgadywać(licznik: dict, dlaczego: str):
    """Milczenie jest odpowiedzią domyślną, więc każdy jego powód działa osobno."""
    assert rozstrzygnij([FAWORKI], [Skłonność(licznik=licznik)]) == [FAWORKI], dlaczego


def test_wskazanie_przychodzi_z_liczbami_które_je_wydały():
    """Wskazanie bez powodu nie da się sprawdzić bez zaglądania do tabeli."""
    (odpowiedź,) = rozstrzygnij([FAWORKI], [Skłonność(licznik=JEDNOZNACZNY)])
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == "przepis"
    assert "4 z 4" in odpowiedź.powód


def test_odpowiedź_niesie_imię_świadka_który_ją_wydał():
    """Podpisuje ją warstwa, więc świadek nie ma jak podpisać się cudzym imieniem."""
    (odpowiedź,) = rozstrzygnij([FAWORKI], [Skłonność(licznik=JEDNOZNACZNY, nazwa="inny")])
    assert odpowiedź.świadek == "inny"


def test_pierwszy_świadek_z_odpowiedzią_wygrywa_z_dalszymi():
    """Kolejność jest kolejnością rodzaju dowodu, więc musi być kolejnością, a nie zbiorem."""

    class Rama:
        nazwa = "rama"

        def __call__(self, przyłączenie):
            return Rozstrzygnięcie(przyłączenie.modyfikator, "Daj", "bo tak")

    (odpowiedź,) = rozstrzygnij([FAWORKI], [Rama(), Skłonność(licznik=JEDNOZNACZNY)])
    assert (odpowiedź.świadek, odpowiedź.gospodarz) == ("rama", "Daj")


def test_warstwa_nie_rusza_werdyktu():
    """Zdanie rozstrzygnięte przez warstwę zostaje dla olskiego wieloznaczne.

    To jest cała różnica między tą warstwą a rankingiem wstawionym w werdykt,
    i jest to różnica, którą ``docs/disambiguation.md`` wywodzi z pomiaru.
    """
    (werdykt,) = check("Daj przepis na faworki.")
    przed = werdykt.status, werdykt.result.ile, werdykt.explain()
    odpowiedzi = rozstrzygnij(werdykt.result.przyłączenia, [Skłonność(licznik=JEDNOZNACZNY)])
    assert any(isinstance(o, Rozstrzygnięcie) for o in odpowiedzi), "świadek nic nie powiedział"
    assert (werdykt.status, werdykt.result.ile, werdykt.explain()) == przed
    assert werdykt.status == "ambiguous"
