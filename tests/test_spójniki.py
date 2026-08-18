import pytest

pytest.importorskip("morfeusz2")

from olski.skład.morfologia import paradygmat
from olski.skład.spójniki import SPÓJNIKI
from olski.subset import SPÓJNIKI_OKOLICZNIKOWE

#: Same słowa, bo tyle ma świadka w słowniku: relacji Morfeusz nie zna.
SŁOWA = sorted({spójnik for spójnik, _relacja in SPÓJNIKI})

#: Spójniki, którymi analiza otwiera okolicznik wyrażony zdaniem, obie listy razem.
#: Świadek jest ten sam i sprawdza to samo po drugiej stronie.
OKOLICZNIKOWE = sorted(set(SPÓJNIKI_OKOLICZNIKOWE.split("|")))


@pytest.mark.parametrize("spójnik", SŁOWA)
def test_słowo_wypisane_jako_spójnik_jest_spójnikiem_podrzędnym(spójnik: str):
    """Ten leksykon ma świadka pełniejszego niż leksykon przyimków.

    SGJP rozdziela spójnik podrzędny od współrzędnego,
    a tabela jest tabelą podrzędnych, bo tylko one wprowadzają okoliczność,
    więc ``i`` dopisane tutaj zgłasza się tu, a nie na zdaniu, które z niego wyjdzie.
    Czego ten świadek nie sprawdza, mówi ``olski/skład/spójniki.py``:
    doboru, czyli tego, który spójnik należy się której relacji.
    """
    assert paradygmat(spójnik, "comp")


@pytest.mark.parametrize("spójnik", OKOLICZNIKOWE)
def test_spójnik_okolicznikowy_jest_spójnikiem_podrzędnym(spójnik: str):
    """Ta lista stoi po stronie analizy i sprawdza się tym samym świadkiem.

    Lemat dopisany tam z literówką nie zgłasza się niczym: produkcja go nie
    weźmie, bo Morfeusz takiego lematu nie wydaje, a gramatyka zbuduje się i
    wyprowadzi tyle samo zdań co przedtem. Warunku na dobór — który spójnik
    wysuwa swoje zdanie — ten świadek nie sprawdza tak samo jak wyżej,
    a liczy go ``sonda/czoło.py`` nad bankiem drzew.
    """
    assert paradygmat(spójnik, "comp")
