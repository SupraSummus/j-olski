"""Konkurencja liczy ciała, a nie zbiera ich nazwy.

Sonda remisu nazywa parę ciał, która odróżnia dwa najtańsze czytania
(``harness/remis.py``), a czytania odróżnia czasem sama liczba: ciąg współrzędny
dłuższy o jeden człon stoi tym samym ciałem raz więcej i niczym poza tym.
Zbiór postawiony w miejscu licznika mówi o takiej parze, że różnicy nie ma,
i chowa ją pod zdaniami, których czytania różni samo cięcie.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.remis import konkurencja
from olski.parse.czytanie import Node


def _węzeł(label: str, *dzieci: Node) -> Node:
    return Node(label=label, children=dzieci, span=(0, 1), głowa=0, koszty=())


def test_czytania_różniące_się_liczbą_tych_samych_ciał_nie_wychodzą_jednakowe():
    krótsze = _węzeł("ciąg", _węzeł("człon"), _węzeł("ciąg", _węzeł("człon")))
    dłuższe = _węzeł("ciąg", _węzeł("człon"), krótsze)
    assert konkurencja(krótsze, dłuższe) == (
        ("ciąg", ("człon", "ciąg")),
        ("człon", ()),
    )
