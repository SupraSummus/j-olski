import pytest

pytest.importorskip("morfeusz2")

from skład.morfologia import paradygmat
from skład.spójniki import SPÓJNIKI

#: Same słowa, bo tyle ma świadka w słowniku: relacji Morfeusz nie zna.
SŁOWA = sorted({spójnik for spójnik, _relacja in SPÓJNIKI})


@pytest.mark.parametrize("spójnik", SŁOWA)
def test_słowo_wypisane_jako_spójnik_jest_spójnikiem_podrzędnym(spójnik: str):
    """Ten leksykon ma świadka pełniejszego niż leksykon przyimków.

    SGJP rozdziela spójnik podrzędny od współrzędnego,
    a tabela jest tabelą podrzędnych, bo tylko one wprowadzają okoliczność,
    więc ``i`` dopisane tutaj zgłasza się tu, a nie na zdaniu, które z niego wyjdzie.
    Czego ten świadek nie sprawdza, mówi ``skład/spójniki.py``:
    doboru, czyli tego, który spójnik należy się której relacji.
    """
    assert paradygmat(spójnik, "comp")
