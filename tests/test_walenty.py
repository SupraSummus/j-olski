"""Walenty przeczytany o te dwa zdania, które olski z niego bierze.

Słownika ten test nie potrzebuje: schematy pisane ręcznie mówią o czytaniu
wszystko, co się o nim rozstrzyga, a plik wejściowy nie stoi w repozytorium.
"""

import pytest

from olski.walencja import BIERZE_BEZOKOLICZNIK, NIE_BIERZE_BIERNIKA
from olski.walenty import (
    BIERNIK,
    bierze,
    bierze_bezokolicznik_podmiotu,
    leksykon,
    pozycje,
)


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


@pytest.mark.parametrize(
    ("schemat", "bierze_go"),
    [
        ("subj,controller{np(str)} + controllee{infp(_)}", True),
        #  Aspekt stoi u Walentego w nawiasie i olski o niego nie pyta, więc
        #  bezokolicznik dokonany jest tą samą pozycją co dowolny.
        ("subj,controller{np(str)} + controllee{np(str);infp(perf)}", True),
        #  Kontroluje celownik, czyli wykonawcą jest ten, komu kazano, i takiego
        #  zdania ta gramatyka nie ma czym zapisać.
        ("subj{np(str)} + controller{np(dat)} + controllee{infp(_)}", False),
        ("subj{np(str)} + obj{np(str)}", False),
    ],
)
def test_bezokolicznik_liczy_się_tylko_pod_kontrolą_podmiotu(schemat, bierze_go):
    assert bierze_bezokolicznik_podmiotu([schemat]) is bierze_go


def test_do_leksykonu_wchodzi_lemat_wraz_ze_zdaniami_które_są_o_nim_prawdziwe(tmp_path):
    #  Lemat, o którym prawdziwe nie jest żadne z tych zdań, nie wchodzi: zostaje mu
    #  rama domyślna, a wpis, który tylko ją powtarza, niczego nie rozstrzyga.
    #  Zwrotność schodzi z lematu do osobnego pola, bo Morfeusz jej w lemacie nie
    #  ma: cząstka jest u olskiego osobnym tokenem.
    #  Oba zdania naraz są tu wpisem jednym, a nie dwoma, bo lemat jest jeden.
    plik = tmp_path / "verbs.txt"
    plik.write_text(
        "% komentarz\n"
        "działać: pewny: _: : imperf: subj{np(str)} + {xp(locat)}\n"
        "abonować: pewny: _: : imperf: subj{np(str)} + obj{np(str)}\n"
        "bawić się: pewny: _: : imperf: subj{np(str)} + {np(inst)}\n"
        "chcieć: pewny: _: : imperf: subj,controller{np(str)} + controllee{np(str);infp(_)}\n"
        "bać się: pewny: _: : imperf: subj,controller{np(str)} + controllee{infp(_)}\n",
        encoding="utf-8",
    )
    assert leksykon(plik) == [
        ("bawić", True, (NIE_BIERZE_BIERNIKA,)),
        ("bać", True, (NIE_BIERZE_BIERNIKA, BIERZE_BEZOKOLICZNIK)),
        ("chcieć", False, (BIERZE_BEZOKOLICZNIK,)),
        ("działać", False, (NIE_BIERZE_BIERNIKA,)),
    ]
