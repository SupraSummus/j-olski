"""Że warstwa morfologiczna stoi poniżej gramatyki, a nie tylko tak o sobie mówi."""

import subprocess
import sys

import pytest

pytest.importorskip("morfeusz2")


@pytest.mark.parametrize("moduł", ["olski.segmentacja", "olski.lematy"])
def test_import_warstwy_pod_gramatyką_nie_buduje_gramatyki(moduł):
    """Docstringi obu modułów obiecują to zdanie, a nie pilnowało go nic.

    Jeden import dopisany do tamtych modułów oddaje koszt gramatyki każdemu,
    kto pyta o samą segmentację, a ``olski/wieloznaczność.py`` jest takim pytającym.
    Zapłacono za to zdanie osobnym modułem na lematy dwóch warstw
    (``olski/lematy.py`` mówi, czym ten koszt jest),
    a wraca ono po cichu: suita przechodzi tak samo z takim importem i bez niego.

    Liczone jest to w osobnym procesie, tak samo jak granica pakietu składu
    (``tests/test_rozbiór.py``), bo w tym gramatykę zaimportowały testy stojące obok.
    """
    kod = f"import {moduł}, sys; print('olski.subset' in sys.modules)"
    przebieg = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True)
    assert przebieg.stdout.strip() == "False", przebieg.stderr
