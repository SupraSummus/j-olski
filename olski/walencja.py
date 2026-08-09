"""Co czasownik bierze: jeden leksykon czytany w obie strony.

Rama jest faktem o słowie, a nie o kierunku, w którym się tego słowa używa,
więc parser i skład czytają ten sam plik.
Druga kopia tej wiedzy rozjeżdża się z pierwszą,
a rozjazd widać dopiero na zdaniu,
którego jeden kierunek nie przyjmuje, a drugi je wypuszcza;
wywód trzyma docs/design-notes.md.

Wspólny jest leksykon, a nie odpowiedź, bo kierunki pytają o co innego.
Parser pyta o klasę: które lematy dzielą ramę,
bo z klasy powstaje produkcja, a nie z lematu.
Skład pyta o jeden lemat:
czy ten czasownik weźmie dopełnienie, które autor postawił w drzewie.
Kopula pokazuje, ile ta różnica waży,
bo po stronie parsera zabiera leksykonowi swoje lematy i dostaje ramę z narzędnikiem:
kierunek dostający leksykon już po tym odjęciu
miałby ``być`` za czasownik biorący biernik
i wypuszczałby ``Program jest ustawienia.``

Zbiory są dwa, bo forma z cząstką ``się`` jest innym czasownikiem:
``otwierać`` bierze dopełnienie w bierniku, a ``otwierać się`` go nie bierze,
i Morfeusz daje obu ten sam lemat.
Leksykon trzymany pod samym lematem zlewałby te dwa czasowniki w jeden
i kłamał o obu.

Plik jest generowany z Walentego przez ``olski/walenty.py``,
który mówi, co stamtąd bierze, a czego nie,
a docs/subset.md wywodzi, czym taki leksykon jest, a czym nie jest.
"""

from __future__ import annotations

from pathlib import Path

LEKSYKON = Path(__file__).parent / "leksykon.txt"


def _czytaj(path: Path) -> tuple[frozenset[str], frozenset[str]]:
    """Leksykon jako dwa zbiory lematów: bez cząstki ``się`` i z nią."""
    gołe: set[str] = set()
    zwrotne: set[str] = set()
    for wiersz in path.read_text(encoding="utf-8").splitlines():
        if wiersz.startswith("#") or not wiersz.strip():
            continue
        lemat, cząstka = wiersz.split("\t")
        (zwrotne if cząstka == "się" else gołe).add(lemat)
    return frozenset(gołe), frozenset(zwrotne)


#: Lematy o ramie węższej niż domyślna, osobno dla formy bez cząstki ``się``
#: i z nią.
BEZ_BIERNIKA, BEZ_BIERNIKA_ZWROTNE = _czytaj(LEKSYKON)


def bierze_biernik(lemat: str) -> bool:
    """Czy czasownik bez cząstki ``się`` weźmie dopełnienie w bierniku.

    Pyta o formę bez cząstki, bo o taką pyta ``Robi`` w ``skład/składnia.py``,
    czyli jedyny konstruktor, który dopełnienie stawia.
    Formy z cząstką składnia nie ma czym zapisać,
    więc drugi zbiór czyta po tej stronie nikt, a po tamtej czyta go gramatyka.

    Odpowiedź twierdząca należy się także lematowi, którego ten leksykon nie wymienia,
    i to jest rama domyślna, a nie brak wiedzy:
    plik wylicza czasowniki o ramie węższej,
    więc milczenie o czasowniku jest tu zdaniem o nim.
    """
    return lemat not in BEZ_BIERNIKA
