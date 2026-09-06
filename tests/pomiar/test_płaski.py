"""Kryterium, którym sonda liczy płaskie czytania, i jego dwie granice.

Pytanie jest jedno: czy przysłówek stopniowany wisi wprost pod listą okoliczników
i czy zaraz po nim padł przymiotnik albo drugi przysłówek. Bez żądania stopnia
kryterium liczy przysłówek pierwotny, który zdanie określa zgodnie z prawdą, a bez
żądania „wprost” liczy czytanie drugiego gospodarza, czyli to, o którym mówi, że
go brakuje. Jedno i drugie podnosi liczbę, nie ruszając wydruku.
"""

import pytest

pytest.importorskip("morfeusz2")


from harness.płaski import (
    OKOLICZNIK,
    PRZED_PRZYMIOTNIKIEM,
    PRZED_PRZYSŁÓWKIEM,
    PRZY_PRZYMIOTNIKU,
    płaskie,
    wariant,
)
from olski.werdykt import check


def _czytanie(zdanie: str, nazwa: str = OKOLICZNIK):
    werdykty = check(zdanie, wariant(nazwa))
    assert len(werdykty) == 1
    [drzewo] = werdykty[0].result.readings
    return drzewo


@pytest.mark.parametrize(
    ("zdanie", "klasy"),
    [
        ("Plik jest bardzo duży.", [PRZED_PRZYMIOTNIKIEM]),
        ("Program zapisuje ustawienia bardzo szybko.", [PRZED_PRZYSŁÓWKIEM]),
        #  Przysłówek pierwotny przymiotnika nie określa, więc przed nim stoi
        #  zgodnie z prawdą i pomyłką nie jest.
        ("Teraz nowa ustawa wchodzi w życie.", []),
        #  Przysłówek stopniowany przy czasowniku, czyli pozycja, po którą ta
        #  połowa konstrukcji weszła.
        ("Bardzo lubię pliki.", []),
    ],
)
def test_płaskie_liczy_przysłówek_stopniowany_i_tylko_przed_niższym_gospodarzem(
    zdanie: str, klasy: list[str]
):
    assert [klasa for klasa, _ in płaskie(_czytanie(zdanie))] == klasy


def test_czytanie_drugiego_gospodarza_nie_jest_płaskie_choć_ma_te_same_formy():
    """Ten sam napis pod dwiema gramatykami, bo o pomyłce rozstrzyga drzewo.

    Kryterium liczące sam napis powiedziałoby o obu czytaniach to samo, a jedno z
    nich jest tym, którego brak sonda wycenia: pod drugim gospodarzem `bardzo`
    stoi pod grupą przymiotnikową i drzewo mówi o nim prawdę.
    """
    zdanie = "Program zabawy był ściśle ustalony."
    assert [klasa for klasa, _ in płaskie(_czytanie(zdanie))] == [PRZED_PRZYMIOTNIKIEM]
    pod_drugim = _czytanie(zdanie, PRZY_PRZYMIOTNIKU)
    assert płaskie(pod_drugim) == []
