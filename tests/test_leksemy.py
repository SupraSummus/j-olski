"""Który leksem stoi pod nazwą, czyli czego leksykon nazw pilnuje.

Wpis tego leksykonu jest rozstrzygnięciem autora,
więc sprawdzić da się o nim dwie rzeczy i obie stoją tu osobno.
Że wskazuje leksem, który słownik ma, widać po formie, którą ta nazwa wydaje,
i tę formę wypisują ``ŚWIADKOWIE``.
Że kompilator pyta leksykonu, a nie kolejności, w jakiej słownik wydaje formy,
widać dopiero na nazwie, której leksykon nie ma,
bo wtedy zamiast formy wychodzi zgłoszenie.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.skład import LEKSEMY, WieleLeksemów, odmień, rodzaj_rzeczownika

#: Nazwa z leksykonu wraz z żądaniem, po którym widać jej leksem, oraz formą,
#: którą ten leksem daje. Wiersz stoi tu dla każdego wpisu i tyle jest jego
#: świadkiem: identyfikator przepisany z literówką nie ma ani jednej formy, więc
#: zgłasza się tutaj, a nie na zdaniu, które z tego wpisu wyjdzie.
ŚWIADKOWIE = [
    ("Włochy", dict(case="loc", number="pl"), "Włoszech"),
    ("oko", dict(case="acc", number="pl"), "oczy"),
    ("oko_w_rosole", dict(case="nom", number="pl"), "oka"),
]


def test_każdy_wpis_leksykonu_ma_formę_po_której_go_widać():
    """Wpis bez świadka jest wpisem, którego literówki nie zgłasza nic."""
    assert sorted(nazwa for nazwa, _żądane, _forma in ŚWIADKOWIE) == sorted(LEKSEMY)


@pytest.mark.parametrize(("nazwa", "żądane", "forma"), ŚWIADKOWIE)
def test_nazwa_z_leksykonu_odmienia_się_wedle_swojego_leksemu(
    nazwa: str, żądane: dict[str, str], forma: str
):
    """Nazwa pyta o jeden leksem, więc odpowiedź nie zależy od kolejności w słowniku.

    ``Włochy`` są tu wierszem, który pokazuje, po czym leksem rozpoznać,
    bo oba leksemy tego lematu mają w miejscowniku ten sam tag
    i różni je wyłącznie identyfikator.
    Cecha nie rozstrzygnęłaby tego wiersza, a leksem rozstrzyga wszystkie trzy.
    """
    assert odmień(nazwa, "subst", **żądane) == forma


def test_leksemy_zgodne_co_do_formy_nie_żądają_rozstrzygnięcia():
    """Wybór jest tam, gdzie odpowiedzi są różne, a nie tam, gdzie leksemów jest kilka.

    ``dziób`` ma dwa leksemy i oba mają w dopełniaczu ``dzioba``,
    więc autor nie ma tu czego rozstrzygać i leksykon nie ma po co rosnąć.
    """
    assert odmień("dziób", "subst", case="gen", number="sg") == "dzioba"


def test_leksemy_niezgodne_co_do_formy_zgłaszają_się_zamiast_wybrać_w_milczeniu():
    """Aspekt jest tu ceną milczenia: forma dokonana w czasie teraźniejszym jest przyszła.

    Zgłoszenie wymienia leksemy wraz z formami, bo autor rozstrzyga między
    znaczeniami, a widzi je po tym, co z każdego wyjdzie.
    """
    with pytest.raises(WieleLeksemów) as zgłoszenie:
        odmień("stać", "fin", number="sg", person="ter")
    assert "stoi" in str(zgłoszenie.value)
    assert "stanie" in str(zgłoszenie.value)


def test_rodzaj_bierze_się_ze_zgody_leksemów_a_nie_z_kolejności_alfabetycznej():
    """Rodzaj męskozwierzęcy przyjmują oba leksemy ``potwór``, a osobowy jeden.

    Wybór alfabetyczny dałby tu osobowy, czyli rodzaj, którego drugi leksem nie ma,
    a zgodność całego zdania liczy się z tej wartości.
    """
    assert rodzaj_rzeczownika("potwór") == "m2"


def test_leksemy_niezgodne_co_do_rodzaju_zgłaszają_się_zamiast_wybrać_w_milczeniu():
    """``pilot`` jest wedle leksemu osobą, zwierzęciem albo rzeczą,
    a rodzaju, na który zgadzałyby się wszystkie trzy, nie ma.
    """
    with pytest.raises(WieleLeksemów):
        rodzaj_rzeczownika("pilot")
