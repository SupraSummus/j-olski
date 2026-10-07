"""Które czytania reprezentacja pośrednia skleja, a które zostawia osobno."""

import pytest

pytest.importorskip("morfeusz2")

from olski.parse import las
from olski.reprezentacja import reprezentacje
from olski.segmentacja import morphology
from olski.subset import GRAMMAR


def trójki(zdanie):
    """Zbiory krawędzi wszystkich czytań, bez miejsc w zdaniu."""
    return [
        {
            (krawędź.głowa.forma.casefold(), krawędź.rola, krawędź.zależnik.forma.casefold())
            for krawędź in reprezentacja.krawędzie
        }
        for reprezentacja in reprezentacje(las(GRAMMAR, morphology(zdanie)).czytania())
    ]


@pytest.mark.parametrize("zdanie", ["Kot śpi w piwnicy.", "W piwnicy kot śpi."])
def test_okolicznik_stoi_przy_orzeczeniu_w_każdym_szyku(zdanie):
    #  Gramatyka bierze okolicznik przed orzeczeniem i za nim innymi produkcjami.
    assert {
        ("śpi", "podmiot", "kot"),
        ("śpi", "wyrażenie_przyimkowe", "w"),
        ("w", "grupa_imienna", "piwnicy"),
    } in trójki(zdanie)


@pytest.mark.parametrize(
    ("zdanie", "spójnik", "człony"),
    [
        ("Kot i pies śpią.", "i", {"kot", "pies"}),
        ("Kot śpi, a pies szczeka.", "a", {"śpi", "szczeka"}),
    ],
)
def test_współrzędność_stoi_spójnikiem(zdanie, spójnik, człony):
    (krawędzie,) = trójki(zdanie)
    assert {zależnik for głowa, rola, zależnik in krawędzie if głowa == spójnik} == człony


@pytest.mark.parametrize(
    "zdanie",
    ["Akcja zbierania podpisów jest prowadzona od wtorku.", "Jan jest bardzo zmęczony."],
)
def test_łącznik_z_przymiotnikiem_jest_jednym_orzeczeniem(zdanie):
    #  Czytania różni tylko to, czy okolicznik doszedł do łącznika, czy do przymiotnika.
    assert len(trójki(zdanie)) == 1


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Rzeczownik w orzeczeniu ma własne określenia: lekarz w szpitalu.
        "Janek jest lekarzem w szpitalu.",
        #  `z Polkiem` przy `Spotkali` albo przy `wzrokiem`.
        "Spotkali się wzrokiem z Polkiem.",
        #  Te same krawędzie, inny leksem: `sobie` od `siebie` albo od rzeczownika `soba`.
        "teraz sobie przypominam.",
    ],
)
def test_czytania_różne_strukturą_albo_leksemem_zostają_osobno(zdanie):
    assert len(trójki(zdanie)) == 2
