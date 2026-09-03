"""Dwie własności, bez których odcisk gramatyki mówi, że nie ruszyło się nic.

Odcisk jest przyrządem, którym dowodzi się, że zmiana przestawiająca gramatykę
niczego nie wyprowadza inaczej (``harness/odcisk.py``), więc skłamać może na dwa
sposoby i oba wyglądają jak sukces.

Pierwszy: pokazuje różnicę, której nie ma. Hasze napisów są losowane przy
starcie, a gramatyka jest pełna zbiorów, więc odcisk wzięty z dwóch drzew
roboczych wypisuje wtedy kilkadziesiąt różnic i żadna z nich nie jest zmianą.
Widać to wyłącznie między procesami, bo w jednym ziarno jest jedno, i dlatego
własność ta sprawdza się podprocesem, nad całą gramatyką naraz.

Drugi: przemilcza różnicę, która jest. ``repr`` produkcji wypisuje głowę i
ciało, a przemilcza cechy, koszty i lematy terminala, więc odcisk pisany z niego
przechodzi nad zmianą walencji tak samo jak nad zmianą żadną.
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

from harness.odcisk import wypisz
from olski.cennik import OKOLICZNIK
from olski.grammar import Production, V, Word, word

KORZEŃ = Path(__file__).resolve().parent.parent


def _odcisk(ziarno: str) -> str:
    """Wydruk komendy z procesu o tym ziarnie haszy napisów."""
    return subprocess.run(
        [sys.executable, "-m", "harness.odcisk"],
        cwd=KORZEŃ,
        env={**os.environ, "PYTHONHASHSEED": ziarno},
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def test_odcisk_wychodzi_ten_sam_pod_dwoma_ziarnami_haszy():
    assert _odcisk("0") == _odcisk("12345")


BAZA = Production(head="zdanie", body=(word("subst"), word("fin")))


def _z_terminalem(terminal: Word) -> Production:
    """Baza z podmienioną pierwszą córką, czyli różnica siedząca w terminalu."""
    return replace(BAZA, body=(terminal, *BAZA.body[1:]))


#: Produkcja różniąca się od :data:`BAZA` jednym polem, którego ``repr`` nie
#: wypisuje. Po jednej na pole, bo pominąć w odcisku da się każde z osobna,
#: a pominięte jest zmianą, o której odcisk milczy.
RÓŻNI_SIĘ_POLEM = {
    "koszty": replace(BAZA, koszty=(OKOLICZNIK,)),
    "głowa": replace(BAZA, głowa=1),
    "features": replace(BAZA, features=(("case", frozenset({"nom"})),)),
    "constraints terminala": _z_terminalem(word("subst", case=V("c"))),
    "lemmas": _z_terminalem(word("subst", lemma="plik")),
    "bez_lematów": _z_terminalem(word("subst", bez_lematu="plik")),
    "bez_lematów_formy": _z_terminalem(word("subst", bez_lematu_formy="plik")),
    "niesione": _z_terminalem(word("subst", niesie="degree")),
}


@pytest.mark.parametrize("pole", sorted(RÓŻNI_SIĘ_POLEM))
def test_odcisk_widzi_pole_którego_repr_produkcji_nie_wypisuje(pole):
    inna = RÓŻNI_SIĘ_POLEM[pole]
    assert repr(BAZA) == repr(inna), "para ma się różnić polem, którego repr nie wypisuje"
    assert wypisz(BAZA) != wypisz(inna)
