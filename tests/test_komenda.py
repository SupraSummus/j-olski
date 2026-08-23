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


def _proza(wejścia, args: argparse.Namespace) -> str:
    """Sonda prozy, która wypisuje, co dostała."""
    return " | ".join(f"{ścieżka.name}: {tekst.strip()}" for ścieżka, tekst in wejścia) + (
        f" ({args.przykłady})"
    )


def test_plik_prozy_dochodzi_do_sondy_razem_ze_swoją_ścieżką(tmp_path, capsys):
    """Nagłówek wydruku nazywa plik, więc sonda dostaje i tekst, i ścieżkę."""
    plik = tmp_path / "proza.txt"
    plik.write_text("Program zapisuje ustawienia.\n", encoding="utf-8")

    assert uruchom(_komenda(proza=_proza), [str(plik)]) == 0
    assert capsys.readouterr().out == "proza.txt: Program zapisuje ustawienia. (6)\n"


def test_pliki_prozy_dochodzą_do_sondy_jednym_przebiegiem_w_podanej_kolejności(tmp_path, capsys):
    """Rejestr bywa wieloplikowy, a sonda ma z nich złożyć jeden raport.

    Zlepienie ich w jeden plik przed przebiegiem jest krokiem, którego dokument
    nie ma jak wydrukować obok liczby, więc pliki idą tu osobno i w tej
    kolejności, w jakiej je podano: scalony raport ma być tym samym raportem,
    co z jednego przebiegu nad całością.
    """
    for nazwa, treść in (("a.txt", "Plik jest duży."), ("b.txt", "Program zapisuje plik.")):
        (tmp_path / nazwa).write_text(treść, encoding="utf-8")

    kod = uruchom(_komenda(proza=_proza), [str(tmp_path / "b.txt"), str(tmp_path / "a.txt")])
    assert kod == 0
    assert capsys.readouterr().out == (
        "b.txt: Program zapisuje plik. | a.txt: Plik jest duży. (6)\n"
    )


def test_katalog_podany_obok_pliku_nie_uchodzi_za_prozę(tmp_path, capsys):
    """Bank drzew jest jednym katalogiem, więc kilka ścieżek może znaczyć tylko prozę.

    Katalog wpuszczony między pliki czytałby się jako proza, której nie ma, albo
    jako korpus, o który nikt nie prosił, a komunikat ma powiedzieć, co komenda
    bierze, zamiast twierdzić, że tego katalogu nie ma.
    """
    (tmp_path / "proza.txt").write_text("Plik jest duży.", encoding="utf-8")
    (tmp_path / "korpus").mkdir()

    kod = uruchom(_komenda(proza=_proza), [str(tmp_path / "proza.txt"), str(tmp_path / "korpus")])
    assert kod == 2
    błędy = capsys.readouterr().err
    assert "nie ma takiej ścieżki" not in błędy
    assert f"katalog podaje się sam, bez innych ścieżek: {tmp_path / 'korpus'}" in błędy
    assert "albo pliki z prozą do przeczytania" in błędy


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
    błędy = capsys.readouterr().err
    assert "katalog z rozpakowaną Składnicą" in błędy
    assert "prozą" not in błędy
