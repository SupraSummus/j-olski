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
czy ten czasownik weźmie to, co autor postawił w drzewie.
Kopula pokazuje, ile ta różnica waży,
bo po stronie parsera zabiera leksykonowi swoje lematy i dostaje ramę z narzędnikiem:
kierunek dostający leksykon już po tym odjęciu
miałby ``być`` za czasownik biorący biernik
i wypuszczałby ``Program jest ustawienia.``

Wspólny jest też plik, a nie każde zdanie, które on mówi.
Biernik czytają oba kierunki, a bezokolicznik oraz zdanie podrzędne
czyta sam skład,
i nie jest to niezgoda o fakt, tylko różnica w tym, co on komu kupuje:
po stronie generatora jest jedyną obroną przed drzewem żądającym
bezokolicznika od czasownika, który go nie bierze,
a po stronie parsera zmierzono oba i żadne nie kupiło ani jednej jednoznaczności;
liczby trzyma docs/subset.md.
Pozycję zdania podrzędnego gramatyka podzbioru już ma,
więc jest to teraz ta sama decyzja co przy bezokoliczniku, a nie brak pozycji.

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


#: Zdania, które leksykon o lemacie mówi, każde pod napisem, którym plik je wypisuje.
#: Nazwa jest tu tym samym zdaniem co wartość, żeby literówka nie miała gdzie się schować.
#: Stoją po stronie czytającego, bo generator jest narzędziem nad tym plikiem,
#: a plik czytają oba kierunki i one nie mają po co importować narzędzia.
NIE_BIERZE_BIERNIKA = "nie_bierze_biernika"
BIERZE_BEZOKOLICZNIK = "bierze_bezokolicznik"
BIERZE_ZDANIE = "bierze_zdanie"


def _czytaj(path: Path) -> dict[str, dict[bool, frozenset[str]]]:
    """Leksykon jako zdania po lemacie, osobno dla formy bez cząstki ``się`` i z nią.

    Zwrotność jest kluczem, a nie częścią lematu, bo Morfeusz daje obu formom
    lemat ten sam, a wziąć mogą co innego.
    """
    wpisy: dict[str, dict[bool, frozenset[str]]] = {}
    for wiersz in path.read_text(encoding="utf-8").splitlines():
        if wiersz.startswith("#") or not wiersz.strip():
            continue
        lemat, cząstka, orzeczone = wiersz.split("\t")
        wpisy.setdefault(lemat, {})[cząstka == "się"] = frozenset(orzeczone.split(","))
    return wpisy


_WPISY = _czytaj(LEKSYKON)


def _lematy(zdanie: str, *, zwrotny: bool) -> frozenset[str]:
    """Lematy, o których leksykon orzeka to zdanie.

    Zbiorami, a nie pytaniem o lemat, bo parser buduje z nich klasy walencyjne,
    czyli pyta o to, które lematy ramę dzielą.
    Pytanie o jeden lemat, które stawia skład, czyta potem te same zbiory.
    """
    return frozenset(
        lemat for lemat, wedle_cząstki in _WPISY.items() if zdanie in wedle_cząstki.get(zwrotny, ())
    )


#: Lematy bez dopełnienia w bierniku, osobno dla formy bez cząstki ``się`` i z nią.
BEZ_BIERNIKA = _lematy(NIE_BIERZE_BIERNIKA, zwrotny=False)
BEZ_BIERNIKA_ZWROTNE = _lematy(NIE_BIERZE_BIERNIKA, zwrotny=True)

#: Lematy z bezokolicznikiem pod kontrolą podmiotu. Zbiór zwrotny stąd nie wychodzi,
#: bo cząstki ``się`` nie ma czym zapisać po tej stronie, a parser tego zdania nie czyta.
Z_BEZOKOLICZNIKIEM = _lematy(BIERZE_BEZOKOLICZNIK, zwrotny=False)

#: Lematy ze zdaniem podrzędnym wprowadzonym przez ``że``. Formy zwrotnej ta strona
#: nie ma czym zapisać, tak samo jak przy bezokoliczniku, więc zbiór jest jeden.
ZE_ZDANIEM = _lematy(BIERZE_ZDANIE, zwrotny=False)


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


def bierze_bezokolicznik(lemat: str) -> bool:
    """Czy czasownik weźmie bezokolicznik, którego wykonawcą jest jego podmiot.

    Odpowiedź przecząca należy się lematowi, którego leksykon nie wymienia,
    czyli odwrotnie niż przy bierniku, i odwrotność ta jest w domyślności,
    a nie w sposobie czytania: rama domyślna ma dopełnienie w bierniku
    i nie ma bezokolicznika, więc jedno zdanie odejmuje, a drugie dokłada.

    Kontrolę leksykon już rozstrzygnął, więc to pytanie o nią nie pyta:
    ``kazać`` bierze w polszczyźnie bezokolicznik, a wykonawcą jest ten,
    komu kazano, i takiego zdania ta gramatyka nie ma czym zapisać,
    bo celownika w niej nie ma.
    """
    return lemat in Z_BEZOKOLICZNIKIEM


def bierze_zdanie(lemat: str) -> bool:
    """Czy czasownik weźmie zdanie podrzędne wprowadzone przez ``że``.

    Domyślność jest ta sama co przy bezokoliczniku i z tego samego powodu:
    drzewo składu takiej pozycji nie stawia, dopóki ktoś jej nie postawi,
    więc milczenie o lemacie odmawia.
    Gramatyka podzbioru czyta to inaczej i pyta o to innym pytaniem:
    tam pozycja stoi w ramie domyślnej i to zawężenie zmierzono,
    o czym mówi ``RAMA_DOMYŚLNA`` w ``olski/subset.py``.

    O kontrolę to pytanie nie pyta i pytać nie ma czego:
    zdanie podrzędne niesie własny podmiot, więc nie ma tu nikogo,
    kogo czasownik nad nim musiałby wskazać.
    """
    return lemat in ZE_ZDANIEM
