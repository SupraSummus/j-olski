"""Kolejność czytań stoi na deklaracji, a nie na kolejności dopisań do gramatyki.

Czym ta kolejność jest i po co, mówi
docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie.
"""

import random

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import Grammar, Głowa, nt, word
from olski.parse import parse
from olski.segmentacja import morphology
from olski.subset import build
from olski.werdykt import check

#: Zdania wieloznaczne, każde inną decyzją: przyłączenie wyrażenia przyimkowego,
#: szyk podmiotu i dopełnienia oraz oba naraz. Kolejność czytań rozstrzyga się
#: w każdym z nich gdzie indziej, więc jedno zdanie nie starczy na tę własność.
ZDANIA = [
    "Program zapisuje ustawienia w pliku.",
    "Ustawienia zapisuje program.",
    "Nowy program zapisuje ustawienia użytkownika w pliku.",
]


def _czytania(grammar: Grammar) -> list[list[str]]:
    """Czytania każdego z tych zdań, w kolejności, w jakiej widzi je czytelnik."""
    werdykty = check("\n\n".join(ZDANIA), grammar)
    assert all(werdykt.readings for werdykt in werdykty), "zdanie bez czytań nic tu nie mierzy"
    return [[str(streszczenie) for streszczenie in werdykt.readings] for werdykt in werdykty]


def _potasowana(seed: int) -> Grammar:
    """Te same produkcje dopisane do gramatyki w innej kolejności."""
    wzór = build()
    produkcje = list(wzór.productions)
    random.Random(seed).shuffle(produkcje)
    grammar = Grammar(start=wzór.start, nie_wypuszczane=wzór.nie_wypuszczane)
    for production in produkcje:
        grammar.dopisz(production)
    return grammar


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_kolejność_czytań_nie_zależy_od_kolejności_dopisania_produkcji(seed: int):
    assert _czytania(_potasowana(seed)) == _czytania(build())


def test_produkcja_tańsza_wydaje_swoje_czytanie_wcześniej():
    """Koszt rozstrzyga przed cięciem, więc tańsze ciało wychodzi z lasu pierwsze.

    Gramatyka jest napisana pod tę jedną własność: dwa ciała o córkach tej samej
    rozpiętości zostawiają kosztowi całą decyzję, a nad zdaniem olskiego
    rozstrzygnęłoby ją zwykle cięcie i test nie mierzyłby kosztu.
    """
    kolejność = []
    for koszt_lewego in (0, 1):
        grammar = Grammar(start="zdanie")
        grammar.rule("zdanie", [Głowa(nt("lewe"))], koszt=koszt_lewego)
        grammar.rule("zdanie", [Głowa(nt("prawe"))], koszt=1 - koszt_lewego)
        grammar.rule("lewe", [Głowa(word("subst")), word("interp")])
        grammar.rule("prawe", [Głowa(word("subst")), word("interp")])
        czytania = parse(grammar, morphology("plik.")).readings
        kolejność.append([drzewo.children[0].label for drzewo in czytania])
    assert kolejność == [["lewe", "prawe"], ["prawe", "lewe"]]


def test_koszt_produkcji_nie_sumuje_się_do_kosztu_rodzica():
    """Ciała córki rozstrzygnęła córka, więc jej koszt nie waży już nad rodzicem.

    Gramatyka jest napisana pod tę jedną własność: `lewe` i `prawe` mają córki
    tej samej rozpiętości i kosztują tyle samo, więc o kolejności rozstrzyga
    alfabet etykiet, a koszt zsumowany po poddrzewie wpuszczałby przodem `prawe`.
    Sumowanie jest tu pomyłką prawdopodobną, bo tak właśnie sumuje się koszt
    morfologii, a widać ją tylko po kolejności: czytań nie ubywa.
    """
    grammar = Grammar(start="zdanie")
    grammar.rule("zdanie", [Głowa(nt("lewe"))])
    grammar.rule("zdanie", [Głowa(nt("prawe"))])
    grammar.rule("lewe", [Głowa(word("subst")), word("interp")], koszt=5)
    grammar.rule("prawe", [Głowa(word("subst")), word("interp")])
    czytania = parse(grammar, morphology("plik.")).readings
    assert [drzewo.children[0].label for drzewo in czytania] == ["lewe", "prawe"]


def test_czytanie_oparte_na_formie_spoza_rejestru_wychodzi_z_lasu_później():
    """Koszt morfologii idzie w górę, aż trafi na ciała, które się nim różnią.

    `Wszystko` jest u Morfeusza i rzeczownikiem, i przysłówkiem regionalnym
    (``olski/rejestr.py``), a czytania te różnią się dopiero pod `zdanie_składowe`.
    Koszt liczony na miejscu nie ruszyłby więc żadnego z nich.
    Czytań przy tym nie ubywa i werdykt zostaje ten sam.
    """
    (werdykt,) = check("Wszystko jest podmiotem.")
    assert [sorted(zdanie) for (zdanie,) in werdykt.readings] == [
        ["orzeczenie", "orzecznik", "podmiot"],
        ["okolicznik_przysłówkowy", "orzeczenie", "orzecznik"],
    ]
