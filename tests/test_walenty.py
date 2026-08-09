"""Walenty przeczytany o to jedno zdanie, które olski z niego bierze.

Słownika ten test nie potrzebuje: schematy pisane ręcznie mówią o czytaniu
wszystko, co się o nim rozstrzyga, a plik wejściowy nie stoi w repozytorium.
"""

import pytest

from olski.walenty import BIERNIK, bierze, leksykon, pozycje


def test_pozycja_zleksykalizowana_nie_rozcina_się_na_swoim_plusie():
    #  Plus rozdziela pozycje, a stoi też wewnątrz pozycji zleksykalizowanej, w
    #  nawiasach. Rozbiór po samym plusie robi z jednej pozycji dwie i drugiej z
    #  nich urywa etykietę, więc pozycja podmiotu przestaje wyglądać na podmiot.
    schemat = "subj{np(str)} + {lex(np(str),sg,'czas',atr({adjp(agr)}+{np(gen)}))}"
    assert [etykieta for etykieta, _ in pozycje(schemat)] == ["subj", ""]


@pytest.mark.parametrize(
    ("schemat", "biernik"),
    [
        ("subj{np(str)} + {xp(locat)}", False),
        ("subj{np(str)} + obj{np(str)}", True),
        ("subj{np(str)} + {np(acc)}", True),
        #  Biernik bywa u Walentego pozycją bez etykiety obj i bywa schowany w
        #  pozycji zleksykalizowanej; jedno i drugie jest dopełnieniem, którego
        #  olski ma nie odbierać.
        ("subj{np(str)} + {lex(np(str),sg,'ochota',natr)}", True),
        #  Przypadek strukturalny w pozycji podmiotu jest mianownikiem, a nie
        #  biernikiem, więc sam podmiot dopełnienia nie zapowiada.
        ("subj,controller{np(str)} + controllee{infp(_)}", False),
    ],
)
def test_biernik_liczy_się_tylko_w_pozycji_niepodmiotowej(schemat, biernik):
    assert bierze([schemat], BIERNIK) is biernik


def test_do_leksykonu_wchodzi_lemat_bez_biernika_wraz_ze_swoją_zwrotnością(tmp_path):
    #  Lemat, który biernik bierze, nie wchodzi, bo leksykon mówi jedno zdanie i
    #  wpis o lemacie, którego to zdanie nie dotyczy, niczego nie zabrania.
    #  Zwrotność schodzi z lematu do osobnego pola, bo Morfeusz jej w lemacie nie
    #  ma: cząstka jest u olskiego osobnym tokenem.
    plik = tmp_path / "verbs.txt"
    plik.write_text(
        "% komentarz\n"
        "działać: pewny: _: : imperf: subj{np(str)} + {xp(locat)}\n"
        "abonować: pewny: _: : imperf: subj{np(str)} + obj{np(str)}\n"
        "bawić się: pewny: _: : imperf: subj{np(str)} + {np(inst)}\n",
        encoding="utf-8",
    )
    assert leksykon(plik) == [("bawić", True), ("działać", False)]
