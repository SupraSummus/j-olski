"""Rozdanie wejścia, na którym stoi każda sonda mierząca nad korpusem.

Wiersz poleceń jest w `harness/komenda.py` jeden, więc pomyłka w rozdaniu wejścia
psuje wszystkie sondy naraz, a żadna z nich nie ma testu nad swoim wydrukiem: to,
co drukują, czyta człowiek. Tu stoi więc to jedno, co da się sprawdzić bez
korpusu — który tryb dostaje zdanie i co sonda widzi, kiedy ścieżki nie ma.
"""

from __future__ import annotations

import argparse
import importlib
import pkgutil
from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

import harness
from harness.komenda import Komenda, uruchom


def _komenda(**pola) -> Komenda:
    """Sonda, która wypisuje, co dostała, żeby test miał co przeczytać."""
    return Komenda(
        nazwa="harness.próba",
        opis="Sonda do testu.",
        przykłady=6,
        korpus=lambda ścieżki, args: f"korpus: {[p.name for p in ścieżki]}",
        **pola,
    )


def _sondy() -> list:
    """Moduły, które deklarują tu swój wiersz poleceń, znalezione, a nie wypisane.

    Lista wypisana ręką pomija sondę dopisaną później i nie mówi o tym ani słowem,
    a niezmiennik niżej ma obowiązywać każdą.
    """
    znalezione = []
    for info in pkgutil.iter_modules(harness.__path__):
        moduł = importlib.import_module(f"harness.{info.name}")
        if hasattr(moduł, "KOMENDA"):
            znalezione.append(moduł)
    return znalezione


@pytest.mark.parametrize("sonda", _sondy(), ids=lambda sonda: sonda.__name__)
def test_deklaracja_nazywa_moduł_w_którym_stoi(sonda):
    """Z nazwy powstaje i pomoc, i prefiks komunikatu, więc pomyłka w niej kłamie."""
    assert sonda.KOMENDA.nazwa == sonda.__name__


def test_zdania_podane_wprost_nie_żądają_ścieżki(capsys):
    """Tryb `-c` mierzy to, co podano, więc argument pozycyjny jest przy nim wolny."""
    kod = uruchom(_komenda(zdania=lambda tekst: f"zdania: {tekst}"), ["-c", "Plik jest duży."])
    assert kod == 0
    assert capsys.readouterr().out == "zdania: Plik jest duży.\n"


def test_bez_ścieżki_i_bez_zdań_wiersz_poleceń_kończy_użyciem():
    with pytest.raises(SystemExit) as podniesione:
        uruchom(_komenda(zdania=lambda tekst: tekst), [])
    assert podniesione.value.code == 2


def test_plik_prozy_dochodzi_do_sondy_razem_ze_swoją_ścieżką(tmp_path, capsys):
    """Nagłówek wydruku nazywa plik, więc sonda dostaje i tekst, i ścieżkę."""
    plik = tmp_path / "proza.txt"
    plik.write_text("Program zapisuje ustawienia.\n", encoding="utf-8")

    def proza(tekst: str, ścieżka: Path, args: argparse.Namespace) -> str:
        return f"{ścieżka.name}: {tekst.strip()} ({args.przykłady})"

    assert uruchom(_komenda(proza=proza), [str(plik)]) == 0
    assert capsys.readouterr().out == "proza.txt: Program zapisuje ustawienia. (6)\n"


def test_limit_ucina_listę_lasów_przed_sondą(tmp_path, capsys):
    for nazwa in ("a.xml", "b.xml"):
        (tmp_path / nazwa).touch()
    assert uruchom(_komenda(), [str(tmp_path), "--limit", "1"]) == 0
    assert capsys.readouterr().out == "korpus: ['a.xml']\n"


def test_sonda_bez_trybu_prozy_nie_bierze_pliku(tmp_path, capsys):
    """Komunikat obiecuje tyle, ile ta sonda przyjmuje, a plikiem się nie zajmuje."""
    plik = tmp_path / "proza.txt"
    plik.touch()
    assert uruchom(_komenda(), [str(plik)]) == 2
    assert "nie ma takiego katalogu:" in capsys.readouterr().err
