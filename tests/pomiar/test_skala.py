"""Rozstęp odpowiada tylko tam, gdzie suma rozstrzyga wybór.

Sonda skali czyta rozstęp jako miarę tego, ile najtańsze czytanie jest warte
(``harness/skala.py``), a zdanie o kilku najtańszych czytaniach nie zostawia
sumie żadnego wyboru. Rozstęp policzony w takim zdaniu jako zero wpisałby je do
kubełka o najwyższej trafności, bo wśród najtańszych czytań złote wtedy zwykle
stoi, i wyszłaby z tego krzywa lepsza od prawdy
(``docs/disambiguation.md#miara-porównywalna-nad-czytaniami``).
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.skala import Zdanie


@pytest.mark.parametrize(
    ("sumy", "rozstęp"),
    [((100, 200, 200), 100), ((100, 100, 200), None)],
)
def test_rozstęp_milczy_gdy_najtańszą_sumę_ma_kilka_czytań(
    sumy: tuple[int, ...], rozstęp: int | None
):
    assert Zdanie(numer=1, sumy=sumy).rozstęp == rozstęp
