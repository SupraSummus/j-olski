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
Skład pyta o jeden lemat i dostaje zbiór pozycji (:func:`rama`):
które z nich ten czasownik bierze, bo tyle wystarcza,
żeby powiedzieć o drzewie, czy on weźmie to, co autor w nim postawił.
Warstwa rozstrzygająca pyta o jeden lemat i o jedną pozycję:
czy rama tego słowa żąda tego przyimka.

Wspólny jest też plik, a nie każde zdanie, które on mówi.
Biernik, celownik i dopełniacz czytają oba kierunki,
zdanie podrzędne sam skład,
a o bezokoliczniku plik mówi dwoma zdaniami i każdy czyta swoje.
Skład czyta węższe, o kontroli podmiotu, bo jest ono po tamtej stronie
jedyną obroną przed drzewem żądającym bezokolicznika od czasownika,
który go nie bierze.
Parser czyta szersze i czyta je przy czasowniku zwrotnym:
tam pozycja bezokolicznikowa dokłada odczytanie drugie zdaniu,
w którym cząstka stoi między dwoma czasownikami,
więc zawężenie kupuje jednoznaczność, zamiast kosztować zdanie.
Po stronie niezwrotnej zmierzono je i nie kupiło ani jednej;
liczby trzyma docs/subset.md.
Pozycję zdania podrzędnego gramatyka podzbioru ma,
więc jest to ta sama decyzja co przy bezokoliczniku niezwrotnym,
a nie brak pozycji.

Przyimki czyta trzeci odbiorca i żadnej produkcji nie rusza:
świadek ramowy w ``olski/rozstrzyganie.py`` pyta o nie po obu stronach
spornego wyrażenia przyimkowego.
Gramatyka ich nie czyta, bo wyrażenie przyimkowe przyłącza się u olskiego
wszędzie, gdzie polszczyzna je stawia, a wybór miejsca należy do czytelnika
(docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).

Ręcznie stoi w tym leksykonie jeden wpis i jest nim kopula (:data:`KOPULA`).
Walenty mówi o ``być`` to samo, co o każdym innym lemacie,
a rama kopuli mówi o narzędniku, którego rama domyślna nie ma,
więc kierunek biorący ten plik bez odjęcia kopuli
wypuszczałby ``Program jest ustawienia.``
Odjęcie stoi tutaj i dlatego stoi raz, a nie po jednym na kierunek;
czym rama kopuli jest dla gramatyki, mówi ``olski/subset/rama.py``.

Wpisy rozdziela klasa słowa, bo jeden lemat bywa kilkoma słowami naraz.
Forma z cząstką ``się`` jest innym czasownikiem —
``otwierać`` bierze dopełnienie w bierniku, a ``otwierać się`` go nie bierze,
i Morfeusz daje obu ten sam lemat —
a rzeczownik jest trzecim słowem i ma własną ramę.
Leksykon trzymany pod samym lematem zlewałby te słowa w jedno
i kłamał o każdym z nich.

Plik jest generowany z Walentego przez ``harness/walenty.py``,
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
BIERZE_BEZOKOLICZNIK_PODMIOTU = "bierze_bezokolicznik_podmiotu"
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

#: Kopula: czasownik, który bierze orzecznik w narzędniku, i jedyny, który go
#: bierze. Lista jest zamknięta i docs/subset.md wywodzi, czego na niej nie ma.
#: Stoi w tym pliku, bo jest tym jednym wpisem leksykonu, którego nie ma w
#: Walentym, a pytają o nią klasy walencyjne gramatyki (``olski/subset/rama.py``),
#: orzeczenie imienne składu (``olski/skład/składnia.py``) oraz świadek
#: kontekstowy, który przy tym czasowniku milczy (``olski/rozstrzyganie.py``).
KOPULA = frozenset({"być", "bywać", "zostać", "zostawać", "pozostać", "pozostawać"})

#: Pozycje ramy, każda pod napisem, którym morfologia nazywa to, czego ta pozycja
#: żąda: przypadek grupy imiennej, formę czasownika, część mowy spójnika. Napisu
#: tego ten plik nie dobiera i nie ma po co: pozycja przypadkowa oddaje go wprost
#: do ``odmień`` w ``olski/skład/morfologia.py``, bo przypadek jest dokładnie tym,
#: czego ona od roli żąda.
BIERNIK = "acc"
CELOWNIK = "dat"
DOPEŁNIACZ = "gen"
ORZECZNIK = "inst"
BEZOKOLICZNIK = "inf"
ZDANIE_PODRZĘDNE = "comp"


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
#: ``harness/walenty.py``.
Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU = _lematy(BIERZE_CELOWNIK_PRZY_WYPEŁNIENIU, CZASOWNIK)
Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU_ZWROTNE = _lematy(
    BIERZE_CELOWNIK_PRZY_WYPEŁNIENIU, CZASOWNIK_ZWROTNY
)

#: Zbiory różnią się zdaniem, a nie klasą słowa, i po to stoją tu oba naraz:
#: pierwszy mówi, że przy formie z cząstką ``się`` bezokolicznik stoi, a drugi,
#: że przy formie bez cząstki wykonawcą bezokolicznika jest jej własny podmiot.
#: Zdanie węższe zawiera się w szerszym tak samo jak celownik przy wypełnieniu
#: w celowniku, a komu które służy, mówi docstring tego modułu.
Z_BEZOKOLICZNIKIEM_ZWROTNE = _lematy(BIERZE_BEZOKOLICZNIK, CZASOWNIK_ZWROTNY)
Z_BEZOKOLICZNIKIEM_PODMIOTU = _lematy(BIERZE_BEZOKOLICZNIK_PODMIOTU, CZASOWNIK)

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


#: Rama kopuli: orzecznik w narzędniku i nic poza nim. Biernika nie ma, bo
#: `Program jest ustawienia.` nie jest zdaniem; pozycji, które leksykon dokłada,
#: nie ma z tego samego powodu, a Walenty daje kopuli je wszystkie.
RAMA_KOPULI = frozenset({ORZECZNIK})

#: Pozycje, które leksykon do ramy dokłada, każda wraz z lematami, które ją mają.
#: Zdania te są twierdzące, a zdanie o bierniku ujemne, i odwrotność ta jest w
#: domyślności, od której każde odejmuje: rama domyślna ma biernik i nie ma
#: pozycji żadnej z tych czterech.
POZYCJE_LEKSYKONU = (
    (CELOWNIK, Z_CELOWNIKIEM),
    (DOPEŁNIACZ, Z_DOPEŁNIACZEM),
    (BEZOKOLICZNIK, Z_BEZOKOLICZNIKIEM_PODMIOTU),
    (ZDANIE_PODRZĘDNE, ZE_ZDANIEM),
)


def rama(lemat: str) -> frozenset[str]:
    """Pozycje, które ten czasownik bierze, czyli rama widziana przez skład.

    Zbiorem, a nie pytaniem na pozycję, bo drzewo żąda tylu pozycji, ile w nim
    stanęło: pytań byłoby po jednym na pozycję, a każde z nich stoi u pytającego
    osobną gałęzią, więc lista rośnie wtedy w dwóch miejscach naraz.
    Zbiór porównuje się raz i tak go czyta ``Robi`` w ``olski/skład/składnia.py``.

    Pyta się o formę bez cząstki ``się``, bo taką stawia składnia; formy z cząstką
    nie ma ona czym zapisać, więc zbiory zwrotne czyta po tej stronie nikt.

    Kopula ma ramę wypisaną (:data:`RAMA_KOPULI`), a nie liczoną z pliku, i mówi o
    tym docstring tego modułu. Odjęcie to jest przy tym całą odmową, jaką skład
    kopuli wydaje: czasownik, który orzeka orzecznikiem, nie orzeka czynnością.

    Bezokolicznik wchodzi tu zdaniem węższym, o kontroli podmiotu, bo drzewo
    wykonawcę stawia i musi wiedzieć, czy jest nim ten sam, o kim orzeka czasownik
    nad nim: ``kazać`` bierze w polszczyźnie bezokolicznik, a wykonawcą jest ten,
    komu kazano, i tego ten zapis nie ma czym powiedzieć.
    """
    if lemat in KOPULA:
        return RAMA_KOPULI
    domyślna = frozenset() if lemat in BEZ_BIERNIKA else {BIERNIK}
    return frozenset(domyślna) | {
        pozycja for pozycja, lematy in POZYCJE_LEKSYKONU if lemat in lematy
    }
