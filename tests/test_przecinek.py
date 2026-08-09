"""Sonda przecinkowa mierzy gramatykę, która stoi, a nie swoją kopię.

Jedyne, czym sonda może skłamać po cichu: wariant pełny, który miał być olskim,
a nie jest, bo przepisanie produkcji coś po drodze zgubiło. Wtedy każda liczba w
`docs/subset.md` jest liczbą o innej gramatyce i nic tego nie widać po wydruku.
"""

from __future__ import annotations

import pytest

from olski.subset import GRAMMAR, check
from sonda.przecinek import POZIOMY, gramatyka


def test_wariant_pełny_jest_dokładnie_gramatyką_olskiego():
    assert gramatyka("wszystkie").productions == GRAMMAR.productions


@pytest.mark.parametrize(
    ("poziom", "zdanie"),
    [
        ("zdaniowy", "Wstaję, wyglądam przez okno."),
        ("imienny", "Kobiety muszą zakrywać włosy, ramiona, nogi."),
        ("przymiotnikowy", "Plik jest nowy, duży."),
    ],
)
def test_wariant_poziomu_zostawia_przecinek_na_swoim_poziomie_i_zdejmuje_go_z_reszty(
    poziom: str, zdanie: str
):
    """Zdanie, które stoi na jednym poziomie, rozstrzyga o obu stronach naraz.

    Wariant, który zdejmuje za dużo, odrzuci je mimo swojej nazwy, a wariant,
    który zdejmuje za mało, przyjmie je pod cudzą. Mianownik jest wspólny, więc
    jeden taki błąd rozjeżdża całą tabelę, a nie jeden jej wiersz.
    """
    assert [werdykt.status for werdykt in check(zdanie, gramatyka("bez"))] == ["rejected"]
    for nazwa in POZIOMY:
        oczekiwane = "valid" if nazwa == poziom else "rejected"
        assert [werdykt.status for werdykt in check(zdanie, gramatyka(nazwa))] == [oczekiwane]
