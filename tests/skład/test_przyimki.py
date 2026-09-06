import pytest

pytest.importorskip("morfeusz2")

from olski.skład.morfologia import paradygmat
from olski.skład.przyimki import PRZYIMKI

#: Wpisy, które słownik ma czym potwierdzić. Narzędnik bez przyimka odpada stąd,
#: bo świadkiem jest znakowanie przyimka, a takiego wpisu nie ma czym znakować.
ZNAKOWANE = sorted(para for para in PRZYIMKI if para[0])


@pytest.mark.parametrize(("przyimek", "relacja"), ZNAKOWANE)
def test_przypadek_wypisany_przy_przyimku_jest_przypadkiem_który_ten_przyimek_bierze(
    przyimek: str, relacja: str
):
    """Połowa ręcznego leksykonu ma świadka w słowniku, więc ta połowa jest checkiem.

    Morfeusz znakuje przyimek przypadkami, którymi ten przyimek rządzi,
    więc literówka w tabeli zgłasza się tutaj, a nie na zdaniu, które z niej wyjdzie.
    Czego ten świadek nie sprawdza, mówi ``olski/skład/przyimki.py``:
    doboru, czyli tego, który przypadek należy się której relacji.
    """
    bierze = {
        wartość
        for _forma, cechy, _leksem in paradygmat(przyimek, "prep")
        for nazwa, wartości in cechy
        if nazwa == "case"
        for wartość in wartości
    }
    assert PRZYIMKI[przyimek, relacja] in bierze
