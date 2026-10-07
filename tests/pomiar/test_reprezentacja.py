"""Wskazanie świadka nałożone na reprezentacje, na którym stoi pomiar w `docs/kierunek.md`."""

import pytest

pytest.importorskip("morfeusz2")

from harness.reprezentacja import bez_gospodarzy_przyimków, sporne, zgodna
from olski.parse import Przyłączenie, las
from olski.reprezentacja import reprezentacje
from olski.segmentacja import morphology
from olski.subset import GRAMMAR


def różne(zdanie):
    return reprezentacje(las(GRAMMAR, morphology(zdanie)).czytania())


def test_wskazanie_zostawia_reprezentacje_z_tym_gospodarzem():
    #  Cztery reprezentacje to dwa przyłączenia `w Gryficach` razy dwa czytania `Michaluk`.
    wszystkie = różne("Janina Michaluk leży w szpitalu w Gryficach.")
    ((przyimek, przyłączenie),) = sporne(wszystkie).items()
    assert przyłączenie == Przyłączenie("w Gryficach", ("leży", "szpitalu"))
    zostaje = [r for r in wszystkie if zgodna(r, {przyimek: "szpitalu"})]
    assert (len(wszystkie), len(zostaje)) == (4, 2)


@pytest.mark.parametrize(
    ("zdanie", "same_przyłączenia"),
    [
        ("Spotkali się wzrokiem z Polkiem.", True),
        #  `Michaluk` jest też okolicznikiem w narzędniku, a tego przyłączenie nie rozstrzyga.
        ("Janina Michaluk leży w szpitalu w Gryficach.", False),
    ],
)
def test_sufit_liczy_zdania_różne_samym_gospodarzem_przyimka(zdanie, same_przyłączenia):
    assert (len(set(map(bez_gospodarzy_przyimków, różne(zdanie)))) == 1) is same_przyłączenia
