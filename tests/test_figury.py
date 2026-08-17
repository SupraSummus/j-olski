"""Raport o figurach odpowiada z dwóch napisów i deklaracja rdzewieje jak wskaźnik.

Odpowiedź sprawdza się tu bez pliku i bez sondy, bo ``stan`` bierze treść pliku i
odciski drzewa wprost. Reszta to rdzewienie deklaracji: plik wymieniony w
``ruszają`` da się przemianować, a raport policzy go wtedy za należność i powodu
nie nazwie; sekcję restytuującą da się przemianować jak każdy nagłówek. Jedno i
drugie zawodzi tutaj, a nie u kogoś, kto sięgnął po korpus, bo przeliczenie jest
osobną komendą właśnie po to (``harness/figury.py``).

Rozstrzyganie wskaźników bierze się z ``tests/test_docs.py``, bo slug nagłówka
jest tym samym faktem tu i tam.
"""

from dataclasses import replace

import pytest
from test_docs import ROOT, assert_resolves

from harness.figury import (
    AKTUALNA,
    FIGURY,
    KATALOG,
    NALEŻNA,
    NIEZMIERZONA,
    NIEZNANY,
    Figura,
    stan,
    zapis,
)

PRÓBNA = Figura(
    nazwa="próbna",
    polecenie=("python3", "-m", "sonda.negacja", "proza/README.txt"),
    ruszają=("olski/subset.py", "sonda/negacja.py"),
    czyta=("docs/subset.md#what-the-grammar-covers",),
)
#: Odciski drzewa, w którym nic się nie ruszyło od przebiegu figury.
TERAZ = {"olski/subset.py": "aaaaaaaaaaaa", "sonda/negacja.py": "bbbbbbbbbbbb"}


def figury():
    return [pytest.param(figura, id=figura.nazwa) for figura in FIGURY]


@pytest.mark.parametrize(
    ("pisana", "zapisane", "odpowiedź", "powody"),
    [
        pytest.param(PRÓBNA, TERAZ, AKTUALNA, [], id="nic się nie ruszyło"),
        pytest.param(
            PRÓBNA,
            {**TERAZ, "olski/subset.py": "cccccccccccc"},
            NALEŻNA,
            ["olski/subset.py"],
            id="gramatyka się ruszyła",
        ),
        pytest.param(
            PRÓBNA,
            {**TERAZ, "sonda/negacja.py": NIEZNANY},
            NIEZMIERZONA,
            ["sonda/negacja.py"],
            id="odcisk nieznany bije zgodność reszty",
        ),
        pytest.param(
            replace(PRÓBNA, ruszają=("olski/subset.py",)),
            {"olski/subset.py": "aaaaaaaaaaaa"},
            NALEŻNA,
            ["sonda/negacja.py"],
            id="ruszający dopisany po przebiegu",
        ),
        pytest.param(
            replace(PRÓBNA, polecenie=("python3", "-m", "sonda.negacja", "proza/")),
            TERAZ,
            NALEŻNA,
            ["polecenie"],
            id="przebieg czytał inny korpus",
        ),
    ],
)
def test_odpowiedź_bierze_się_z_odcisków_i_z_polecenia(
    pisana: Figura, zapisane: dict, odpowiedź: str, powody: list
):
    assert stan(PRÓBNA, zapis(pisana, zapisane, "wydruk"), TERAZ) == (odpowiedź, powody)


@pytest.mark.parametrize("figura", figury())
def test_każdy_zadeklarowany_ruszający_jest_plikiem_który_istnieje(figura: Figura):
    for plik in figura.ruszają:
        assert (ROOT / plik).exists(), f"{figura.nazwa} nazywa plik, którego nie ma: {plik}"


@pytest.mark.parametrize("figura", figury())
def test_każda_figura_nazywa_sekcję_która_ją_restytuuje(figura: Figura):
    assert figura.czyta, f"{figura.nazwa} nie nazywa sekcji, która ją restytuuje"
    for sekcja in figura.czyta:
        path, _, anchor = sekcja.partition("#")
        assert_resolves(ROOT / path, anchor, figura.nazwa)


def test_każdy_plik_w_katalogu_jest_zadeklarowany():
    assert set(KATALOG.glob("*.txt")) == {figura.plik for figura in FIGURY}
