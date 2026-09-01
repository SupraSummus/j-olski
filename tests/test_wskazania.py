"""Złączenie werdyktu z cudzym drzewem, czyli jedyne miejsce, gdzie ta sonda może zmilknąć.

Wzorzec dobiera się tu po formach modyfikatora, bo rozpiętości werdykt nie
niesie. Jedna strona tego napisu powstaje w ``olski/parse/las.py``, druga w sondzie,
i rozejść się mogą tak, że nikt tego nie zauważy: sonda wypisze wtedy „bez
wzorca” zamiast błędu, a mianownik trafności zejdzie do zera po cichu.

Las jest pisany ręcznie z tego samego powodu, co w ``tests/test_attachment.py``,
i jest tym samym lasem: zdanie, które olski czyta dwojako, a Składnica raz.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.corpus import parse_forest
from harness.wskazania import dokąd_doszły
from olski.parse import parse
from olski.subset import DEKLARACJA, GRAMMAR
from tests.test_attachment import zdanie


@pytest.mark.parametrize("host", ["noun", "clause"])
def test_wzorzec_znajduje_się_po_formach_którymi_werdykt_nazywa_modyfikator(host):
    las = zdanie(host)
    zdanie_wzorcowe = parse_forest(las)
    (przyłączenie,) = parse(
        GRAMMAR, list(zdanie_wzorcowe.segments), deklaracja=DEKLARACJA
    ).przyłączenia
    assert dokąd_doszły(las, zdanie_wzorcowe)[przyłączenie.modyfikator] == host
