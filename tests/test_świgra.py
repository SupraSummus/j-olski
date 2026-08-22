"""Ta jedna własność sondy, na której stoi jej liczba.

Sonda mierzy cudzy parser przez podstawione wejście, więc ma dwa sposoby nie
dostać liczby: Świgra może liczyć dłużej, niż wolno, albo rzucić wyjątkiem na
znaczniku, którego tłumaczenie w tej sondzie nie objęło. Pierwsze jest wynikiem
o Świgrze, drugie awarią tej sondy, a wydruk zliczający je razem podaje czas
maszyny jako czas cudzego parsera. Rozdziela je ``odczytaj`` i nic poza nim.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.świgra import odczytaj

#: Wydruk Świgry przycięty do pól, o które sonda pyta. Prolog wypisuje je przed
#: lasem, więc zdanie policzone ma je nawet wtedy, gdy wydruk lasu urwał się dalej.
POLICZONE = "info(tekst,'Zapisz plik.').\ninfo(parse_cputime,1.5).\ninfo(edges,833).\n"

#: Ten sam wydruk bez czasu, czyli tak, jak kończy zdanie, na którym gramatyka
#: rzuciła wyjątkiem: nagłówek stoi, a rozbioru nie było.
AWARIA = "info(tekst,'Zapisz plik.').\ninfo(grammar_no,1787412242).\n"


def test_awaria_prologu_nie_jest_zdaniem_ponad_budżetem():
    assert odczytaj(POLICZONE) == (1.5, 833, None)
    assert odczytaj(AWARIA) == (None, None, "awaria")
    assert odczytaj(None) == (None, None, "budżet")
