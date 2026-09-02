"""Te dwie własności sondy o znaczeniach, na których stoi jej tabela.

Sonda pyta, czy wieloznaczność zameldowana przez werdykt zostaje po przejściu
czytań na kategorie dziedziny, a odpowiada porównaniem zbiorów drzew, a nie ich
liczbą. Zbiory dzielą się na trzy przypadki i dwa z nich nie padają nad żadnym z
rejestrów tego repozytorium, więc partycję sprawdza się tu zbiorami pisanymi
ręką, a to, co pada, zdaniami.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.znaczenia import CZĘŚĆ, CZĘŚĆ_WSPÓLNA, ROZŁĄCZNE, TE_SAME, WSZYSTKIE, odpowiedz, zestaw
from olski.werdykt import check


@pytest.mark.parametrize(
    ("zbiory", "zestawienie"),
    [
        ((frozenset("ab"), frozenset("ab")), TE_SAME),
        ((frozenset("ab"), frozenset("bc")), CZĘŚĆ_WSPÓLNA),
        ((frozenset("a"), frozenset("b")), ROZŁĄCZNE),
        ((frozenset("ab"), frozenset("bc"), frozenset("ca")), ROZŁĄCZNE),
    ],
)
def test_zestawienie_pyta_o_drzewo_wspólne_wszystkim_a_nie_parom(zbiory, zestawienie):
    """Trzy czytania parami zachodzące na siebie nie mają drzewa wspólnego wszystkim.

    Przypadek ostatni jest tym, po który ta partycja tu stoi: przecięcie liczy
    się po wszystkich czytaniach naraz, więc zdanie, którego czytania dzielą
    drzewa parami, wychodzi rozłączne, a nie częściowo wspólne. Odczytać to
    inaczej znaczy powiedzieć o zdaniu, że jedno drzewo mówi je całe.
    """
    assert zestaw(zbiory) == zestawienie


def test_wieloznaczność_ról_wychodzi_rozłączna_choć_drzew_jest_więcej_niż_czytań():
    """Zdanie, o którym oba kierunki mówią to samo: kto kogo widzi, zostaje wyborem.

    Obie formy są tu i mianownikiem, i biernikiem, więc czytania obsadzają role
    odwrotnie, a zapis dziedziny ma czym powiedzieć jedno i drugie. Drzew w sumie
    jest przy tym więcej niż czytań, bo napis milczy o znaczniku tematu, i to jest
    podłoga szumu, pod którą liczba drzew nie odpowiada na nic: odpowiedzią jest
    rozłączność zbiorów, a nie ich rozmiar.
    """
    werdykt = check("Dziecko widzi zwierzę.")[0]
    assert werdykt.result.ambiguous
    odpowiedź = odpowiedz(werdykt.result.readings)
    assert odpowiedź.zasięg == WSZYSTKIE
    assert odpowiedź.zestawienie == ROZŁĄCZNE
    assert odpowiedź.drzewa > werdykt.result.ile


def test_zwinięcie_przez_brak_kategorii_nie_wchodzi_do_zestawienia():
    """Zdanie, którym `docs/po-wypisaniu.md` pokazuje przyłączenie rozstrzygnięte w drzewie.

    Wyrażenie przyimkowe dochodzi w olskim i do zdarzenia, i do rzeczy, a do
    rzeczy ten zapis nie ma czym dojść, więc jedno z dwóch czytań nie wraca
    niczym. Zdanie takie wygląda jak zwinięte i zwinięte nie jest,
    bo drugiego czytania nie zdjęło znaczenie, tylko brak kategorii,
    i dlatego zestawienia nie dostaje wcale.
    """
    werdykt = check("Program zapisuje ustawienia w repozytorium.")[0]
    assert werdykt.result.ambiguous
    odpowiedź = odpowiedz(werdykt.result.readings)
    assert odpowiedź.zasięg == CZĘŚĆ
    assert odpowiedź.zestawienie is None
