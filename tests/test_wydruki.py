"""Blok wydruku wklejony do dokumentu jest tym, co komenda naprawdę drukuje.

Blok taki unieważnia każda zmiana w werdykcie, a rozjazdu nie widać nigdzie
poza puszczeniem polecenia, które nad nim stoi. Wydruk `olski-check` odtwarza
się bez korpusu, więc pilnuje go suita, a nie ręka czytającego.
Wydruku sondy nad korpusem test nie obejmuje, bo suita korpusu nie pobiera.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass
from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

from olski.check import main

ROOT = Path(__file__).resolve().parent.parent
KOMENDA = "olski.check"


@dataclass(frozen=True)
class Blok:
    """Blok ogrodzony w dokumencie wraz z wierszami, między którymi stoi."""

    rodzaj: str
    otwarcie: int
    zamknięcie: int
    treść: tuple[str, ...]


def _ogrodzone(tekst: str) -> list[Blok]:
    rodzaj, otwarcie, treść = None, 0, []
    bloki = []
    for numer, wiersz in enumerate(tekst.splitlines(), start=1):
        if rodzaj is None:
            if wiersz.startswith("```"):
                rodzaj, otwarcie, treść = wiersz.removeprefix("```").strip(), numer, []
        elif wiersz.startswith("```"):
            bloki.append(Blok(rodzaj, otwarcie, numer, tuple(treść)))
            rodzaj = None
        else:
            treść.append(wiersz)
    return bloki


def _wywołania(polecenia: tuple[str, ...]) -> list[list[str]]:
    """Argumenty każdego wywołania komendy, wzięte z bloku poleceń dokumentu.

    Jeden blok niesie czasem dwa wywołania, a jedno wywołanie czasem trzy
    wiersze, bo zdanie w cudzysłowie biegnie przez nie; oba rozdziela `shlex`.
    """
    wywołania: list[list[str]] = []
    for token in shlex.split("\n".join(polecenia)):
        if token == "python3":
            wywołania.append([])
        elif wywołania:
            wywołania[-1].append(token)
    return [w[w.index(KOMENDA) + 1 :] for w in wywołania if KOMENDA in w]


def _wydruki() -> list:
    """Wydruki komendy znalezione w drzewie, a nie wypisane tutaj ręką.

    Lista wypisana ręką pomija blok dopisany później i nie mówi o tym ani słowem.
    """
    znalezione = []
    # Rekurencyjnie, bo rejestr konstrukcji jest katalogiem i wydruki w nim ma.
    for ścieżka in [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]:
        bloki = _ogrodzone(ścieżka.read_text(encoding="utf-8"))
        # blok poleceń stoi nad wydrukiem, a rozdziela je jeden wiersz pusty
        nad = {blok.zamknięcie + 2: blok for blok in bloki if blok.rodzaj == "sh"}
        for blok in bloki:
            wydruk = blok.rodzaj == "text" and any(
                wiersz.startswith("<text>:") for wiersz in blok.treść
            )
            if not wydruk:
                continue
            skąd = f"{ścieżka.name}:{blok.otwarcie}"
            polecenia = nad[blok.otwarcie].treść if blok.otwarcie in nad else ()
            znalezione.append(pytest.param(_wywołania(polecenia), blok.treść, id=skąd))
    return znalezione


@pytest.mark.parametrize(("wywołania", "wydruk"), _wydruki())
def test_wydruk_w_dokumencie_jest_tym_co_komenda_drukuje(wywołania, wydruk, capsys):
    assert wywołania, "nad wydrukiem nie stoi blok poleceń wołający komendę"
    for argumenty in wywołania:
        main(argumenty)
    naprawdę = capsys.readouterr().out.splitlines()
    brakujące = [wiersz for wiersz in wydruk if wiersz not in naprawdę]
    assert not brakujące, f"tych wierszy komenda nie drukuje: {brakujące}"
