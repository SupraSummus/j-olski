"""Że import nie idzie pod prąd granicy pakietu.

Granica między `olski` a `harness` jest kryterium czytanym ręką
(`harness/__init__.py`), a jedna jej konsekwencja jest mechaniczna i nikt jej
nie pilnował: paczka niesie samo `olski` (`include = ["olski*"]`), więc moduł
`olski`, który sięgnąłby po `harness` albo po `witryna`, wywraca się dopiero u
tego, kto olskiego zainstalował. Suita tego nie widzi, bo chodzi po klonie,
gdzie oba pakiety leżą obok siebie i importują się bez pudła.

Pytanie idzie o każdy import pliku, a nie o same stojące w nagłówku: import
schowany w ciele funkcji odracza wywrotkę do wywołania i tym jest gorszy, a nie
lepszy. Tym różni się to od `tests/test_zbiórka.py`, który pyta, dokąd dochodzi
sama zbiórka.

Czytane są tu drzewa składniowe, a nie moduły: import wciągnąłby analizator i
kazał pomijać ten plik tam, gdzie wheel Morfeusza się nie buduje.
"""

import ast
from pathlib import Path

import pytest

KORZEŃ = Path(__file__).resolve().parent.parent
#: Pakiety, których `olski` nie ma prawa zawołać: leżą poza paczką, każdy z
#: własnego powodu (`harness/__init__.py`, `docs/witryna.md`).
POZA_PACZKĄ = ("harness", "witryna")


def _importowane(plik: Path) -> set[str]:
    """Nazwy modułów, które ten plik importuje, gdziekolwiek w nim stoją."""
    nazwy = set()
    for węzeł in ast.walk(ast.parse(plik.read_text(encoding="utf-8"))):
        if isinstance(węzeł, ast.Import):
            nazwy |= {alias.name for alias in węzeł.names}
        elif isinstance(węzeł, ast.ImportFrom) and węzeł.module and not węzeł.level:
            nazwy.add(węzeł.module)
    return nazwy


@pytest.mark.parametrize(
    "plik", sorted((KORZEŃ / "olski").rglob("*.py")), ids=lambda plik: plik.name
)
def test_moduł_pakietu_nie_woła_niczego_spoza_paczki(plik: Path):
    zakazane = {
        nazwa
        for nazwa in _importowane(plik)
        for pakiet in POZA_PACZKĄ
        if nazwa == pakiet or nazwa.startswith(f"{pakiet}.")
    }
    assert not zakazane, f"{plik.relative_to(KORZEŃ)} woła {sorted(zakazane)}"
