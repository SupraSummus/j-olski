"""Sonda pakowania mierzy dwa nadmiary, a każdy widać na innym zdaniu.

Wywód, który z tych zdań korzysta, stoi w
`docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania`, a liczby pod
nim wzięto tą sondą. Zdanie, które przestało pokazywać swój nadmiar, zabiera
temu wywodowi podstawę i nie widać tego po żadnej liczbie w wydruku: obie
tablice zgodziłyby się wtedy z wyliczeniem i sonda wypisałaby same zera.
"""

from __future__ import annotations

import dataclasses

import pytest

pytest.importorskip("morfeusz2")

from olski.parse import parse, wyprowadzenia
from olski.subset import GRAMMAR, morphology
from sonda.pakowanie import WARIANTY, Raport, ile_czytań, nad_prozą, scal, tablica


def policz(zdanie: str) -> dict[str, int]:
    """Ile czytań podaje każdy wariant tablicy, i ile ich naprawdę jest."""
    segmenty = morphology(zdanie)
    zbudowane = wyprowadzenia(GRAMMAR, segmenty)
    ile = {
        wariant: ile_czytań(tablica(zbudowane, wariant), segmenty, GRAMMAR.start)
        for wariant in WARIANTY
    }
    return {"wyliczone": len(parse(GRAMMAR, segmenty).readings), **ile}


def test_tablica_spakowana_liczy_parę_której_unifikacja_nie_przepuszcza():
    #  `Complements` buduje się nad notacją rejestru raz przez `Object`, raz przez
    #  `Predicative`, a rodzic wskazuje pozycję, a nie wariant pod nią.
    assert policz("Zobacz docs/subset.md.")["spakowany"] == 2


def test_tablica_rozszczepiona_liczy_wyprowadzenia_tam_gdzie_cecha_ginie():
    #  `przyjemności` ma pięć czytań, więc `NP` rozszczepia się po przypadku, a
    #  `Modifier` nad nim przypadka nie wypuszcza i zbiera je z powrotem w jedną
    #  pozycję o dwóch wyprowadzeniach jednego kształtu.
    assert policz("Projekt jest dla przyjemności.")["rozszczepiony"] == 2


@pytest.mark.parametrize(
    ("zdanie", "wariant"),
    [
        ("Zobacz docs/subset.md.", "rozszczepiony"),
        ("Projekt jest dla przyjemności.", "spakowany"),
    ],
)
def test_nadmiar_jednej_tablicy_nie_jest_nadmiarem_drugiej(zdanie: str, wariant: str):
    """Dwa nadmiary są z przeciwnych stron, i to jest ta różnica, którą sonda wycenia.

    Zdanie liczone źle przez oba warianty niczego między nimi nie rozstrzyga, bo
    wybór jest tu między sklejeniem a rozdzieleniem, a nie między tablicą dobrą a
    złą.
    """
    liczby = policz(zdanie)
    assert liczby[wariant] == liczby["wyliczone"] == 1


def test_scalanie_nie_gubi_ani_jednego_licznika():
    """Licznik pominięty w `scal` znika dopiero przy `--jobs` większym od jednego.

    Przebieg na jednym procesie scalania nie woła, więc rozbieżność wychodzi
    tylko tam, gdzie nikt jej nie ma z czym porównać: liczba spada, a wydruk
    wygląda tak samo.
    """
    raport = nad_prozą("# Nagłówek\n\nProjekt jest dla przyjemności.\n")
    assert all(getattr(raport, pole.name) for pole in dataclasses.fields(Raport)), (
        "zdanie próbne przestało wypełniać każdy licznik, więc test niczego nie pilnuje"
    )
    assert scal([raport]) == raport
