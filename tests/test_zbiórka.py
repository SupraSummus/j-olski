"""Że zbiórka testów przechodzi tam, gdzie wheel Morfeusza się nie buduje.

[Sekcja Checks](CLAUDE.md#checks) obiecuje, że w takim środowisku plik testowy
dochodzący do analizatora pomija się sam, a przebieg melduje testy stojące obok
niego, a nie zero testów. Obietnicy tej nie pilnowało nic i raz już się
rozeszła, bo przebieg z Morfeuszem przechodzi tak samo z pominięciem i bez
niego: rozejście widać wyłącznie w środowisku bez wheela.

Liczy się to, dokąd import dochodzi, a nie to, co plik wypisuje.
``import morfeusz2`` stoi na górze ``olski/morph.py``, a dochodzi się tam przez
gramatykę albo przez czytnik banku drzew, więc ``tests/test_ruch.py`` sięga
analizatora dwoma modułami i ani razu go nie nazywa. Import stojący w ciele
funkcji nie dochodzi nigdzie, bo zbiórka go nie wykonuje, i dlatego
``tests/test_endings.py`` analizatora nie sięga, choć nazywa
``harness/endings.py``, który woła ``morfeusz2`` w ``main``.

Pominięcia zbędnego ten plik nie zgłasza, choć zabiera ono przebiegowi testy,
które przeszłyby bez analizatora: plik dochodzący do niego dopiero w ciele testu
jest z tego zejścia nie do odróżnienia od pliku, który nie dochodzi wcale.

Czytane są tu same drzewa składniowe. Import któregokolwiek modułu
repozytorium wywracałby zbiórkę, o którą ten plik pyta.
"""

import ast
import functools
from pathlib import Path

import pytest

KORZEŃ = Path(__file__).resolve().parent.parent
#: Pakiety, po których idzie zejście. Import spoza nich jest biblioteką i nie ma
#: pod sobą pliku, do którego dałoby się zejść.
PAKIETY = ("olski", "harness", "opowieści", "witryna", "tests")
ANALIZATOR = "morfeusz2"
POMINIĘCIE = "importorskip"


@functools.cache
def _drzewo(plik: Path) -> ast.Module:
    return ast.parse(plik.read_text(encoding="utf-8"))


def _nazwy(węzeł: ast.AST) -> set[str]:
    """Moduły, które ten węzeł importuje, albo nic, gdy importem nie jest.

    ``from olski import projekt`` wypisuje moduł i nazwę osobno, a która z nich
    jest modułem, rozstrzyga dopiero plik na dysku, więc wychodzą stąd oba
    kandydaci i odsiewa je :func:`_moduły`.
    """
    if isinstance(węzeł, ast.Import):
        return {alias.name for alias in węzeł.names}
    if isinstance(węzeł, ast.ImportFrom) and węzeł.module and not węzeł.level:
        return {węzeł.module} | {f"{węzeł.module}.{alias.name}" for alias in węzeł.names}
    return set()


def _importy(plik: Path) -> set[str]:
    """Co plik wciąga przy imporcie, czyli co stoi na poziomie modułu."""
    return {nazwa for węzeł in _drzewo(plik).body for nazwa in _nazwy(węzeł)}


def _moduły() -> dict[str, Path]:
    """Nazwa modułu → jego plik, dla każdego pliku tych pakietów.

    ``__init__.py`` nosi nazwę swojego katalogu, bo pod tą nazwą go importują,
    i przez nią dochodzi się do wszystkiego, co on sam wciąga.
    """
    znalezione = {}
    for pakiet in PAKIETY:
        for plik in (KORZEŃ / pakiet).rglob("*.py"):
            części = plik.relative_to(KORZEŃ).with_suffix("").parts
            nazwa = ".".join(części[:-1] if części[-1] == "__init__" else części)
            znalezione[nazwa] = plik
    return znalezione


def _dochodzące(moduły: dict[str, Path]) -> frozenset[str]:
    """Moduły, których import wykonuje ``import morfeusz2``, wprost albo przez inne."""
    doszłe = {nazwa for nazwa, plik in moduły.items() if ANALIZATOR in _importy(plik)}
    rosło = True
    while rosło:
        rosło = False
        for nazwa, plik in moduły.items():
            if nazwa not in doszłe and _importy(plik) & doszłe:
                doszłe.add(nazwa)
                rosło = True
    return frozenset(doszłe)


MODUŁY = _moduły()
DOCHODZĄCE = _dochodzące(MODUŁY)
PLIKI_TESTOWE = sorted(plik for nazwa, plik in MODUŁY.items() if nazwa.startswith("tests."))


def _wiersz_pominięcia(plik: Path) -> int | None:
    """Wiersz, w którym plik pomija się bez analizatora, albo nic.

    Liczy się pominięcie stojące na poziomie modułu i tylko ono,
    bo zbiórki nie zatrzyma to, które czeka w ciele testu.
    """
    for węzeł in _drzewo(plik).body:
        if not isinstance(węzeł, ast.Expr) or not isinstance(węzeł.value, ast.Call):
            continue
        wołanie = węzeł.value
        nazwa = wołanie.func.attr if isinstance(wołanie.func, ast.Attribute) else None
        argumenty = [a.value for a in wołanie.args if isinstance(a, ast.Constant)]
        if nazwa == POMINIĘCIE and ANALIZATOR in argumenty:
            return węzeł.lineno
    return None


def _wiersz_dojścia(plik: Path) -> int | None:
    """Wiersz pierwszego importu, którym plik dochodzi do analizatora, albo nic."""
    wiersze = [
        węzeł.lineno for węzeł in _drzewo(plik).body if _nazwy(węzeł) & (DOCHODZĄCE | {ANALIZATOR})
    ]
    return min(wiersze, default=None)


@pytest.mark.parametrize("plik", PLIKI_TESTOWE, ids=lambda plik: plik.name)
def test_plik_dochodzący_do_analizatora_pomija_się_przed_tym_importem(plik: Path):
    dojście = _wiersz_dojścia(plik)
    if dojście is None:
        return
    pominięcie = _wiersz_pominięcia(plik)
    assert pominięcie is not None, "bez analizatora ten plik wywraca zbiórkę"
    assert pominięcie < dojście, "pominięcie stoi pod importem, który je uprzedza"
