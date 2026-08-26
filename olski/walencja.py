"""Co słowo bierze: jeden leksykon dla każdego, kto o ramę pyta.

Rama jest faktem o słowie, a nie o kierunku, w którym się tego słowa używa,
więc wszyscy, którzy o nią pytają, czytają ten sam plik.
Druga kopia tej wiedzy rozjeżdża się z pierwszą,
a rozjazd widać dopiero na zdaniu,
którego jeden kierunek nie przyjmuje, a drugi je wypuszcza;
wywód trzyma docs/design-notes.md.

Wspólny jest leksykon, a nie odpowiedź, bo pytający pytają o co innego.
Parser pyta o klasę: które lematy dzielą ramę,
bo z klasy powstaje produkcja, a nie z lematu.
Skład pyta o jeden lemat:
czy ten czasownik weźmie to, co autor postawił w drzewie.
Warstwa rozstrzygająca pyta o jeden lemat i o jedną pozycję:
czy rama tego słowa żąda tego przyimka.
Kopula pokazuje, ile ta różnica waży,
bo po stronie parsera zabiera leksykonowi swoje lematy i dostaje ramę z narzędnikiem:
kierunek dostający leksykon już po tym odjęciu
miałby ``być`` za czasownik biorący biernik
i wypuszczałby ``Program jest ustawienia.``

Wspólny jest też plik, a nie każde zdanie, które on mówi.
Biernik czytają oba kierunki, celownik i dopełniacz czyta sam parser,
a bezokolicznik oraz zdanie podrzędne czyta sam skład,
i nie jest to niezgoda o fakt, tylko różnica w tym, co on komu kupuje:
po stronie generatora jest jedyną obroną przed drzewem żądającym
bezokolicznika od czasownika, który go nie bierze,
a po stronie parsera zmierzono oba i żadne nie kupiło ani jednej jednoznaczności;
liczby trzyma docs/subset.md.
Pozycję zdania podrzędnego gramatyka podzbioru ma,
więc jest to ta sama decyzja co przy bezokoliczniku, a nie brak pozycji.

Przyimki czyta trzeci odbiorca i żadnej produkcji nie rusza:
świadek ramowy w ``olski/rozstrzyganie.py`` pyta o nie po obu stronach
spornego wyrażenia przyimkowego.
Gramatyka ich nie czyta, bo wyrażenie przyimkowe przyłącza się u olskiego
wszędzie, gdzie polszczyzna je stawia, a wybór miejsca należy do czytelnika
(docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).

Wpisy rozdziela klasa słowa, bo jeden lemat bywa kilkoma słowami naraz.
Forma z cząstką ``się`` jest innym czasownikiem —
``otwierać`` bierze dopełnienie w bierniku, a ``otwierać się`` go nie bierze,
i Morfeusz daje obu ten sam lemat —
a rzeczownik jest trzecim słowem i ma własną ramę.
Leksykon trzymany pod samym lematem zlewałby te słowa w jedno
i kłamał o każdym z nich.

Plik jest generowany z Walentego przez ``olski/walenty.py``,
który mówi, co stamtąd bierze, a czego nie,
a docs/subset.md wywodzi, czym taki leksykon jest, a czym nie jest.
"""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

LEKSYKON = Path(__file__).parent / "leksykon.txt"


#: Zdania, które leksykon o lemacie mówi, każde pod napisem, którym plik je wypisuje.
#: Nazwa jest tu tym samym zdaniem co wartość, żeby literówka nie miała gdzie się schować.
#: Stoją po stronie czytającego, bo generator jest narzędziem nad tym plikiem,
#: a plik czytają wszyscy pytający i oni nie mają po co importować narzędzia.
NIE_BIERZE_BIERNIKA = "nie_bierze_biernika"
BIERZE_BEZOKOLICZNIK = "bierze_bezokolicznik"
BIERZE_ZDANIE = "bierze_zdanie"
BIERZE_CELOWNIK = "bierze_celownik"
BIERZE_DOPEŁNIACZ = "bierze_dopełniacz"
BIERZE_CELOWNIK_PRZY_WYPEŁNIENIU = "bierze_celownik_przy_wypełnieniu"

#: Klasy słowa, którymi plik rozdziela wpisy o jednym lemacie. Stoją tu z tego
#: samego powodu co zdania wyżej, a rozdzielają dlatego, że jeden lemat bywa
#: kilkoma słowami naraz i każde z nich ma własną ramę.
CZASOWNIK = "czasownik"
CZASOWNIK_ZWROTNY = "czasownik się"
RZECZOWNIK = "rzeczownik"


class Wpis(NamedTuple):
    """Co leksykon mówi o jednym słowie."""

    #: Zdania orzeczone o tym słowie, każde napisem wypisanym wyżej.
    zdania: frozenset[str]
    #: Przyimki, których żąda rama tego słowa.
    przyimki: frozenset[str]


def _czytaj(path: Path) -> dict[tuple[str, str], Wpis]:
    """Leksykon jako wpisy po lemacie i klasie słowa.

    Klasa jest częścią klucza, a nie częścią lematu,
    bo Morfeusz daje jeden lemat formie z cząstką ``się`` i bez niej,
    a bez klasy pytanie o ramę rzeczownika
    trafiałoby we wpis czasownika o tym samym lemacie.
    W wydaniu Walentego, z którego ten plik powstaje, taka para nie stoi ani raz,
    więc klucz broni przed rozejściem, a nie naprawia widoczne.
    """
    wpisy: dict[tuple[str, str], Wpis] = {}
    for wiersz in path.read_text(encoding="utf-8").splitlines():
        if wiersz.startswith("#") or not wiersz.strip():
            continue
        lemat, klasa, zdania, przyimki = wiersz.split("\t")
        wpisy[(lemat, klasa)] = Wpis(_zbiór(zdania), _zbiór(przyimki))
    return wpisy


def _zbiór(pole: str) -> frozenset[str]:
    """Pole rozdzielone przecinkiem jako zbiór; pole puste jest zbiorem pustym."""
    return frozenset(pole.split(",")) if pole else frozenset()


_WPISY = _czytaj(LEKSYKON)


def _lematy(zdanie: str, klasa: str) -> frozenset[str]:
    """Lematy tej klasy, o których leksykon orzeka to zdanie.

    Zbiorami, a nie pytaniem o lemat, bo parser buduje z nich klasy walencyjne,
    czyli pyta o to, które lematy ramę dzielą.
    Pytanie o jeden lemat, które stawia skład, czyta potem te same zbiory.
    """
    return frozenset(
        lemat
        for (lemat, jego_klasa), wpis in _WPISY.items()
        if jego_klasa == klasa and zdanie in wpis.zdania
    )


#: Lematy bez dopełnienia w bierniku, osobno dla formy bez cząstki ``się`` i z nią.
BEZ_BIERNIKA = _lematy(NIE_BIERZE_BIERNIKA, CZASOWNIK)
BEZ_BIERNIKA_ZWROTNE = _lematy(NIE_BIERZE_BIERNIKA, CZASOWNIK_ZWROTNY)

#: Lematy z dopełnieniem w celowniku i z dopełnieniem w dopełniaczu, osobno dla
#: obu klas czasownika. Kierunek jest tu przeciwny niż przy bierniku, bo przeciwna
#: jest domyślność, od której te zdania odejmują: rama domyślna ma biernik, a
#: przypadka poza nim nie ma żadnego, więc milczenie o lemacie odmawia mu pozycji.
Z_CELOWNIKIEM = _lematy(BIERZE_CELOWNIK, CZASOWNIK)
Z_CELOWNIKIEM_ZWROTNE = _lematy(BIERZE_CELOWNIK, CZASOWNIK_ZWROTNY)
Z_DOPEŁNIACZEM = _lematy(BIERZE_DOPEŁNIACZ, CZASOWNIK)
Z_DOPEŁNIACZEM_ZWROTNE = _lematy(BIERZE_DOPEŁNIACZ, CZASOWNIK_ZWROTNY)

#: Lematy, przy których celownik stoi obok drugiego wypełnienia, osobno dla obu
#: klas czasownika. Zbiór zawarty w tym wyżej; czemu para potrzebuje własnego
#: zdania, zamiast wychodzić z dwóch policzonych osobno, wywodzi
#: ``olski/walenty.py``.
Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU = _lematy(BIERZE_CELOWNIK_PRZY_WYPEŁNIENIU, CZASOWNIK)
Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU_ZWROTNE = _lematy(
    BIERZE_CELOWNIK_PRZY_WYPEŁNIENIU, CZASOWNIK_ZWROTNY
)

#: Lematy z bezokolicznikiem pod kontrolą podmiotu. Zbiór zwrotny stąd nie wychodzi,
#: bo cząstki ``się`` nie ma czym zapisać po tej stronie, a parser tego zdania nie czyta.
Z_BEZOKOLICZNIKIEM = _lematy(BIERZE_BEZOKOLICZNIK, CZASOWNIK)

#: Lematy ze zdaniem podrzędnym wprowadzonym przez ``że``. Formy zwrotnej ta strona
#: nie ma czym zapisać, tak samo jak przy bezokoliczniku, więc zbiór jest jeden.
ZE_ZDANIEM = _lematy(BIERZE_ZDANIE, CZASOWNIK)


def przyimki_rzeczownika(lemat: str) -> frozenset[str]:
    """Przyimki, których żąda rama rzeczownika o tym lemacie.

    Zbiór pusty znaczy dwie rzeczy naraz,
    a świadek ramowy obu daje tę samą odpowiedź, czyli milczenie:
    albo Walenty daje temu rzeczownikowi ramę bez pozycji przyimkowej,
    albo nie daje mu ramy wcale.
    Plik rzeczownikowy Walentego wylicza dwa tysiące lematów,
    więc drugie zdarza się częściej,
    i to ono ogranicza zasięg tego świadka;
    docs/disambiguation.md liczy, ile z tego wychodzi.
    """
    return _przyimki(lemat, RZECZOWNIK)


def przyimki_czasownika(lemat: str) -> frozenset[str]:
    """Przyimki, których żąda rama czasownika o tym lemacie, z cząstką ``się`` i bez niej.

    Obie klasy naraz, bo pytający ma formę czasownikową,
    a nie zdanie o tym, czy cząstka przy niej stoi:
    ``Przyłączenie`` w ``olski/parse.py`` niesie same głowy gospodarzy.
    Suma jest tu stroną bezpieczną, bo tego zbioru świadek ramowy używa jako weta:
    przyimek żądany przez którekolwiek z tych dwóch słów
    kończy się milczeniem, a nie wskazaniem.
    """
    return _przyimki(lemat, CZASOWNIK) | _przyimki(lemat, CZASOWNIK_ZWROTNY)


def _przyimki(lemat: str, klasa: str) -> frozenset[str]:
    wpis = _WPISY.get((lemat, klasa))
    return wpis.przyimki if wpis is not None else frozenset()


def bierze_biernik(lemat: str) -> bool:
    """Czy czasownik bez cząstki ``się`` weźmie dopełnienie w bierniku.

    Pyta o formę bez cząstki, bo o taką pyta ``Robi`` w ``olski/skład/składnia.py``,
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
    komu kazano, i tego skład nie ma czym zapisać.
    Parser bierze `córce` za dopełnienie `kazał`, bo celownik stoi obok
    wypełnienia, a kto ten bezokolicznik wykonuje, nie pyta ani jedna produkcja.
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
