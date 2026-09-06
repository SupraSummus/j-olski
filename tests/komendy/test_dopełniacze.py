"""Co rozdziela łańcuch dopełniaczy od zdania, które ma dopełniaczy tyle samo.

Reguła liczy przydawki dopełniaczowe wiszące jedna pod drugą, a nie formy
w dopełniaczu (``olski/dopełniacze.py``), więc sądem nietrywialnym jest tu każde
milczenie: zdania niżej mają po kilka dopełniaczy i łańcucha nie mają.
Zgłoszenie pada dopiero od progu, więc łańcuch krótszy od niego stoi tu osobno.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.dopełniacze import PRÓG, łańcuchy
from olski.werdykt import nad_tekstem

#: Zdanie z korpusu usterek wraz z poprawką, nad którą reguła ma milczeć
#: (``próba/usterki.txt``).
Z_USTERKĄ = "Raport zawiera analizę wyników badań skuteczności metod leczenia pacjentów oddziału."
POPRAWKA = "Raport analizuje, jak skutecznie oddział leczy pacjentów."

#: Zdania, nad którymi reguła milczy; czemu, mówi klucz.
MILCZY = {
    "poprawka zdania z korpusu": POPRAWKA,
    "łańcuch krótszy od progu": "Raport zawiera analizę wyników badań skuteczności.",
    "trzy dopełniacze pod rzeczownikiem": "Widzieliśmy dom ojca mojego przyjaciela.",
    "dopełniacze rozdzielone przyimkiem i przeczeniem": (
        "Bez zgody autora nie ma opisu badań ani metod leczenia."
    ),
    "zdanie, którego olski nie czyta": (
        "Analiza wyników badań skuteczności metod leczenia pacjentów oddziału bez raportu wobec."
    ),
}


def znalezione(zdanie: str):
    """Łańcuchy nad jednym zdaniem, tą drogą, którą idzie ``olski-check``."""
    (wpis,) = nad_tekstem(zdanie)
    return łańcuchy(wpis.werdykt.result)


def test_łańcuch_przydawek_dopełniaczowych_dostaje_zgłoszenie():
    (łańcuch,) = znalezione(Z_USTERKĄ)
    assert łańcuch.grupa == "analizę wyników badań skuteczności metod leczenia pacjentów oddziału"
    assert łańcuch.ile >= PRÓG


@pytest.mark.parametrize("zdanie", MILCZY.values(), ids=MILCZY)
def test_dopełniacze_bez_łańcucha_nie_dostają_zgłoszenia(zdanie):
    """Zgłoszenie chybione kosztuje zdanie przepisane bez powodu, a milczenie zero."""
    assert znalezione(zdanie) == ()
