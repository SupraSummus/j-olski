"""Rama czasownika: klasy walencyjne i formy skończone, które z nich wychodzą.

Walencja jedzie kanałem cech, tak jak zgodność: czasownik wypuszcza swoją ramę,
dopełnienie mówi, którą pozycję zajmuje, a przecina jedno z drugim unifikacja.
Ramę czasownika podaje leksykon (``olski/leksykon.txt``),
a ramę domyślną — tę, którą dostaje czasownik spoza leksykonu — deklaruje ten moduł;
wywód, czemu leksykon ma ramę domyślną nad sobą, trzyma
docs/warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej.
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Głowa, Part, V, Var, word
from olski.segmentacja import EVERY_CASE
from olski.subset.słowa import (
    CZĄSTKA_TRYBU,
    TRYB_FORMY_NA_Ł,
    TRYB_OZNAJMUJĄCY,
    TRYB_PRZYPUSZCZAJĄCY,
)
from olski.walencja import (
    BEZ_BIERNIKA,
    BEZ_BIERNIKA_ZWROTNE,
    KOPULA,
    RAMA_KOPULI,
    Z_BEZOKOLICZNIKIEM_ZWROTNE,
    Z_CELOWNIKIEM,
    Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU,
    Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU_ZWROTNE,
    Z_CELOWNIKIEM_ZWROTNE,
    Z_DOPEŁNIACZEM,
    Z_DOPEŁNIACZEM_ZWROTNE,
)

#: Rama czasownika spoza leksykonu: dopełnienie w bierniku, orzecznik zgodny,
#: bezokolicznik, zdanie podrzędne i pytanie zależne. Zabrania ona dwóch rzeczy.
#: Narzędnika w niej nie ma, bo orzecznik narzędnikowy bierze kopula i nikt poza
#: nią, a celownika ani dopełniacza nie ma, bo dopełnienie w tych przypadkach
#: wpuszcza wpis w leksykonie (:data:`DOKŁADANE`). Zdanie podrzędne stoi w niej mimo
#: tego, że leksykon wylicza lematy, które je biorą: zawężenie zmierzono i nie
#: odbiera ono ani jednego drugiego czytania, a kosztuje zdanie; docs/subset.md
#: trzyma pomiar.
#:
#: Pytanie zależne jest pozycją osobną od zdania z `że`, a nie tym samym `comp`,
#: bo Walenty rozdziela je kształtem i mówi to o kilkuset lematach; wywód i
#: polecenie trzyma docs/subset.md. Stoi ono w ramie domyślnej tak samo jak `comp`,
#: a zawężenia tej pozycji do leksykonu nikt nie zmierzył — todo/ trzyma ten
#: przebieg.
RAMA_DOMYŚLNA = frozenset({"nom", "acc", "inf", "comp", "int"})


#: Rama lematu, o którym leksykon mówi, że biernika nie bierze.
#:
#: Ramy węższe odejmują od domyślnej, a nie stoją wypisane obok niej, żeby
#: pozycję dopisaną tam widziała każda z nich.
RAMA_BEZ_BIERNIKA = RAMA_DOMYŚLNA - {"acc"}


#: Rama czasownika zwrotnego spoza leksykonu: domyślna bez bezokolicznika.
#:
#: Odjęcie to jest zdaniem o cząstce, a nie o czasowniku. Cząstka stoi po obu
#: stronach swojej formy osobowej i po obu stronach bezokolicznika pod nią, więc w
#: `ma się odbyć` jeden napis pasuje do dwóch ciał naraz: `[ma się] [odbyć]` oraz
#: `[ma] [się odbyć]`. Polszczyzna ma tam jedno czytanie, a rozstrzyga o nim
#: leksykon: `mieć się` bezokolicznika nie bierze, a `starać się` bierze
#: (:data:`Z_BEZOKOLICZNIKIEM_ZWROTNE`). Bez tego odjęcia pozycja przy
#: bezokoliczniku dokłada drugie wyprowadzenie każdemu zdaniu tego kształtu,
#: zamiast odbierać nieprawdziwe.
#:
#: Po stronie niezwrotnej pozycja ta zostaje w ramie domyślnej, bo tam konkurencji
#: nie ma i zawężenie zmierzono: nie kupiło ani jednego drugiego czytania
#: (:data:`RAMA_DOMYŚLNA`). Cenę odjęcia zwrotnego trzyma
#: docs/konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika.
RAMA_DOMYŚLNA_ZWROTNA = RAMA_DOMYŚLNA - {"inf"}


#: Pozycja, której rama domyślna tej klasy słowa nie ma, a leksykon ją lematowi
#: daje: nazwa pozycji wraz ze zbiorami lematów, osobno dla formy bez cząstki
#: ``się`` i z nią.
#:
#: Zdanie leksykonu jest tu twierdzące, a przy bierniku ujemne, i przeciwne są
#: domyślności, od których oba odejmują: biernik stoi w ramie domyślnej, a
#: przypadek poza nim nie stoi w niej wcale. Bezokolicznik odejmuje w jedną stronę
#: i dokłada w drugą, bo domyślności są tu dwie: rama zwykła go ma, a zwrotna nie
#: (:data:`RAMA_DOMYŚLNA_ZWROTNA`), więc zbiór zwykły jest pusty.
DOKŁADANE = (
    ("dat", Z_CELOWNIKIEM, Z_CELOWNIKIEM_ZWROTNE),
    ("gen", Z_DOPEŁNIACZEM, Z_DOPEŁNIACZEM_ZWROTNE),
    ("inf", frozenset(), Z_BEZOKOLICZNIKIEM_ZWROTNE),
)


#: Te pozycje dokładane, które są przypadkiem, czyli te, które wypełnia grupa
#: imienna (:data:`DOKŁADANE`). Bezokolicznik odpada, bo wypełnia go
#: ``fraza_bezokolicznikowa``.
#:
#: Warunek pyta o listę przypadków (:data:`EVERY_CASE`), a nie wylicza pozycji,
#: których na niej nie ma. Cała lista czytana jako przypadki wypuszczała
#: ``dopełnienie → grupa_imienna[case=inf]`` — ciało, którego nie dopasuje żadna grupa imienna —
#: i nie widziała go ani suita, ani :meth:`Grammar.nieosiągalne`, bo nieosiągalny
#: jest tu układ cech, a nie symbol. Pozycja dopisana do leksykonu poza
#: przypadkami wpadłaby w to samo, gdyby warunek nazywał wyjątki.
DOKŁADANE_PRZYPADKI = tuple(
    nazwa for nazwa, _zwykli, _zwrotni in DOKŁADANE if nazwa in EVERY_CASE
)


def _dokładane(zwrotne: bool) -> list[tuple[str, frozenset[str]]]:
    """Pozycje dokładane wraz z lematami tej klasy słowa (:data:`DOKŁADANE`)."""
    return [(nazwa, zwrotni if zwrotne else zwykli) for nazwa, zwykli, zwrotni in DOKŁADANE]


#: Druga pozycja ramy, czyli dopełnienie dokładane stojące obok wypełnienia:
#: `Parser pokazuje autorowi oba czytania.` Wartość nazywa przypadek tego
#: dopełnienia, a :data:`BEZ_DRUGIEJ` mówi, że lemat pary nie ma.
#:
#: Cechą osobną, a nie pozycją ramy, bo rama jest zbiorem, którego unifikacja
#: przecina, więc żądanie dwóch pozycji naraz wypisane w niej byłoby ich
#: alternatywą: ta cecha licencjonuje celownik, a rama równolegle wypełnienie,
#: obok którego on stoi.
#:
#: Wartość jest jedna, bo jeden przypadek ma tę parę zmierzoną: dopełniacz obok
#: wypełnienia bierze u Walentego kilkadziesiąt lematów, a celownik kilka tysięcy;
#: liczby trzyma docs/warstwa-leksykalna.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia.
DRUGA_CELOWNIK = "dat"


BEZ_DRUGIEJ = "bez"


def _rama(
    lemat: str,
    domyślna: frozenset[str],
    bez_biernika: frozenset[str],
    dokładane: Sequence[tuple[str, frozenset]],
) -> frozenset[str]:
    """Rama tego lematu: domyślna bez tego, czego leksykon mu odmawia, i z tym, co mu daje.

    ``domyślna`` jest domyślną jego klasy słowa, bo klasy te mają dwie różne
    (:data:`RAMA_DOMYŚLNA_ZWROTNA`).
    """
    odjęta = domyślna - {"acc"} if lemat in bez_biernika else domyślna
    return odjęta | {nazwa for nazwa, lematy in dokładane if lemat in lematy}


def _klasy_walencyjne(
    domyślna: frozenset[str],
    bez_biernika: frozenset[str],
    dokładane: Sequence[tuple[str, frozenset]],
    poza: frozenset[str] = frozenset(),
) -> dict[frozenset[str], frozenset[str]]:
    """Lematy leksykonu zebrane w klasy po ramie, którą leksykon każdemu z nich daje.

    ``poza`` zabiera lematy, które mają ramę wypisaną ręcznie: klasy mają się nie
    zachodzić, a lemat wzięty dwiema byłby dwoma czytaniami tego samego kształtu.

    Klucz sortowania jest wypisany, bo rama jest zbiorem, a ``<`` na zbiorach
    porównuje zawieraniem: ``sorted`` bez klucza oddaje kolejność wejścia i nie
    wywraca się przy tym. Kolejność klas ustala kolejność produkcji, a ta
    kolejność, w jakiej las wydaje czytania (CLAUDE.md#code).
    """
    klasy: dict[frozenset[str], set[str]] = {}
    for lemat in bez_biernika.union(*(lematy for _nazwa, lematy in dokładane)) - poza:
        klasy.setdefault(_rama(lemat, domyślna, bez_biernika, dokładane), set()).add(lemat)
    return {
        rama: frozenset(lematy)
        for rama, lematy in sorted(klasy.items(), key=lambda para: sorted(para[0]))
    }


def _walencja() -> tuple[
    dict[frozenset[str], frozenset[str]], dict[frozenset[str], frozenset[str]]
]:
    """Leksykon jako klasy walencyjne, osobno dla formy z cząstką ``się`` i bez niej.

    Zwrotność jest drugim wymiarem klucza, a nie częścią lematu, i dlaczego,
    mówi ``olski/walencja.py``, czyli ten, który leksykon czyta dla obu
    kierunków. Tutaj zostaje to, co jest zdaniem samej gramatyki.

    Kluczem klasy jest rama, a nie lemat, bo tak wychodzi produkcja: powstaje raz
    na ramę, a nie raz na lemat. Kopula zabiera leksykonowi swoje lematy, zamiast
    stanąć obok nich, bo klasy mają się nie zachodzić: Walenty mówi o niej to samo
    co leksykon o każdym innym lemacie, a rama kopuli mówi ponadto o narzędniku.
    Sam narzędnik przychodzi z ``olski/walencja.py`` (:data:`RAMA_KOPULI`), bo
    odjęcie kopuli od leksykonu robią po tej zmianie oba kierunki; podmiot dokłada
    ta produkcja, bo pozycji podmiotu tamten plik nie ma.

    Zdania leksykonu są tu cztery — o bierniku, o celowniku, o dopełniaczu i o
    bezokoliczniku — a plik mówi pięć. Bezokolicznik czyta sama strona zwrotna;
    co zdejmuje go po drugiej i co zdejmuje piąte zdanie, mówi :data:`RAMA_DOMYŚLNA`.
    """
    return (
        {
            **_klasy_walencyjne(RAMA_DOMYŚLNA, BEZ_BIERNIKA, _dokładane(False), KOPULA),
            frozenset({"nom", *RAMA_KOPULI}): KOPULA,
        },
        _klasy_walencyjne(RAMA_DOMYŚLNA_ZWROTNA, BEZ_BIERNIKA_ZWROTNE, _dokładane(True)),
    )


#: Walencja: co czasownik bierze, wypisane lematami, a nie produkcjami.
#: Leksykon jest otwarty i ma ramę domyślną, więc czasownik dopisuje się wpisem, a
#: nie produkcją; czym taki leksykon jest, a czym nie jest, wywodzi
#: docs/warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej.
WALENCJA, WALENCJA_ZWROTNA = _walencja()


def _bez_orzecznika(rama: frozenset[str]) -> frozenset[str]:
    """Ta rama bez orzecznika zgodnego, czyli rama zdania, które podmiotu nie ma.

    Orzecznik zgodny zgadza się z podmiotem, więc zdanie bez podmiotu nie ma go z
    czym zgodzić: `Trzeba wolni.` nie jest niczym i `Zgłoszono tania.` też nie.
    Pytają o to obie głowy roli :data:`ORZECZENIE_BEZOSOBOWE`, a każda o inną ramę —
    predykatyw o domyślną (:data:`RAMA_BEZOSOBOWA`), forma nieosobowa o ramę
    swojego lematu — więc odejmowanie jest funkcją, a nie drugą stałą obok nich.
    """
    return rama - {"nom"}


#: Rama predykatywu (:data:`PREDYKATYWY`): domyślna bez orzecznika zgodnego.
#: Wyliczona z domyślnej z tego samego powodu, z którego wylicza się z niej
#: :data:`RAMA_BEZ_BIERNIKA`.
RAMA_BEZOSOBOWA = _bez_orzecznika(RAMA_DOMYŚLNA)


def _klasy(zwrotne: bool) -> list[tuple[dict[str, frozenset[str]], frozenset[str], str]]:
    """Klasy walencyjne: warunek na lemat, rama i druga pozycja, którą warunek wpuszcza.

    Ostatnia jest klasa domyślna, i jest nią warunek ujemny na wszystkie lematy
    leksykonu naraz, bo klasy mają się nie zachodzić: forma wzięta dwiema klasami
    byłaby dwoma czytaniami tego samego kształtu.

    Pyta on o formę, a nie o jedno jej czytanie, bo rama jest własnością formy:
    zapytany o czytanie rozdziela lematy zamiast form i wpuszcza ramę domyślną
    formie, której lemat leksykon wymienia. Reprodukcję, cenę i zysk trzyma
    docs/warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej.

    Forma z cząstką ``się`` pyta o swój leksykon, bo jest innym czasownikiem;
    lemat, którego tamten leksykon nie wymienia, bierze ramę domyślną tak samo
    jak każdy inny nieznany, bo cząstkę stawia polszczyzna przy czasowniku
    dowolnym, a Walenty wymienia z niej samą zwrotność zleksykalizowaną.
    Domyślne są przy tym dwie i różni je bezokolicznik, o czym mówi
    :data:`RAMA_DOMYŚLNA_ZWROTNA`.

    Klasa domyślna leksykonu zwrotnego odmawia przy tym kopuli (:data:`KOPULA`), i
    jest to jedyny czasownik, któremu ta gramatyka cząstki odmawia wprost: bez tego
    ``Cena się jest niska.`` się wyprowadza, a ``być się`` czasownikiem nie jest.
    Lematu ``zostać`` odmowa ta nie tyka, bo leksykon zwrotny go wymienia i klasa
    domyślna po niego nie sięga. Cenę i odrzuconą alternatywę trzyma
    docs/konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika.

    Klasa ramy dzieli się na dwie tam, gdzie leksykon daje części jej lematów
    drugą pozycję (:data:`DRUGA_CELOWNIK`), a klasa domyślna drugiej pozycji nie
    ma: zdanie o parze mówi o celowniku, więc lemat, który je niesie, stoi w
    leksykonie i tej klasy nie dosięga.
    """
    leksykon = WALENCJA_ZWROTNA if zwrotne else WALENCJA
    z_parą = Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU_ZWROTNE if zwrotne else Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU
    klasy = [
        ({"lemma": wybrane}, rama, druga)
        for rama, lematy in leksykon.items()
        for druga, wybrane in _po_drugiej(lematy, z_parą)
        if wybrane
    ]
    poza_domyślną = (KOPULA if zwrotne else frozenset()).union(*leksykon.values())
    domyślna = RAMA_DOMYŚLNA_ZWROTNA if zwrotne else RAMA_DOMYŚLNA
    return [*klasy, ({"bez_lematu_formy": poza_domyślną}, domyślna, BEZ_DRUGIEJ)]


def _po_drugiej(
    lematy: frozenset[str], z_parą: frozenset[str]
) -> list[tuple[str, frozenset[str]]]:
    """Lematy klasy rozdzielone na te z drugą pozycją i te bez niej."""
    return [(DRUGA_CELOWNIK, lematy & z_parą), (BEZ_DRUGIEJ, lematy - z_parą)]


def _formy_skończone(
    warunek: dict[str, str],
) -> list[tuple[list[Part | Głowa], dict[str, Var | str]]]:
    """Ciała czasownika w formie skończonej, każde wraz z cechami, które ogłasza.

    Czas teraźniejszy i przeszły dzielą trzy ciała, bo osobę niosą inaczej. ``fin``
    niesie osobę i liczbę, a rodzaju nie ma; ``praet`` odwrotnie, więc osoba trzecia
    jest w nim wpisana tutaj, a bez tego ``Ja napisał program.`` się wyprowadza:
    cechy, której konstytuent nie niesie, unifikacja nie sprawdza. Osobę pierwszą
    i drugą wnosi aglutynant, czyli końcówkę, którą Morfeusz odcina od formy —
    ``napisałem`` wchodzi tu jako ``napisał`` i ``em`` — i która liczbę ma tę samą
    co czasownik przy niej.

    Tryb przypuszczający ma dwa ciała i różnią się one od dwóch przeszłych jedną
    cząstką (:data:`CZĄSTKA_TRYBU`): ``odzyskałby`` i ``odzyskałbym``. Dostaje ją
    czas przeszły i on jeden, bo tak stawia tę cząstkę polszczyzna: ``zapisujeby``
    nie jest niczym. Ciała są dwa, a nie jedno z cząstką pominiętą, bo cena trybu
    ma być osobną liczbą, a sonda różnicowa bierze ją zdejmowaniem ciał.

    Tryb wychodzi stąd wartością cechy, bo pyta o niego spójnik, który cząstkę
    niesie sam (:data:`SPÓJNIKI_TRYBU`). Forma na -ł bez cząstki wychodzi z obiema
    wartościami naraz (:data:`TRYB_FORMY_NA_Ł`), a ta sama forma z aglutynantem już
    nie: aglutynant zajmuje miejsce, które pod takim spójnikiem zajmuje jego własna
    końcówka, więc polszczyzna ma ``żebym wiedział``, a nie ``żeby wiedziałem``.

    Czas przyszły ma trzy ciała.
    Forma ``bedzie`` stoi w nich osobno od ``fin``, choć liczbę i osobę niesie
    tak samo, z tego samego powodu, z którego osobno stoi tryb.
    Bezokolicznik nie niesie ani liczby, ani rodzaju,
    więc liczbę ogłasza to ciało samo — bez tego
    ``Programy będzie zapisywać ustawienia.`` się wyprowadza —
    a rodzaju nie żąda nikt.
    Głową jest czasownik, a nie ``bedzie``, bo rama należy do czasownika
    i po nim werdykt nazywa gospodarza przyłączenia.
    Polszczyznę i cenę trzyma
    docs/konstrukcje-gramatyczne/orzeczenie.md#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony.

    Głowa stoi w każdym ciele, także w tym o jednej części: ciało wychodzi
    stąd do produkcji zwrotnej, która dopisuje mu cząstkę ``się``, a ciało o
    dwóch częściach bez głowy nie powstaje.
    """
    czasownik = word("praet", number=V("n"), gender=V("g"), **warunek)
    aglutynant = word("aglt", number=V("n"), person=V("p"))
    forma_przyszła = word("bedzie", number=V("n"), person=V("p"))
    niedokonany = {"aspect": "imperf"}
    return [
        (
            [Głowa(word({"fin", "impt"}, number=V("n"), person=V("p"), **warunek))],
            {"person": V("p"), "tryb": TRYB_OZNAJMUJĄCY},
        ),
        ([Głowa(czasownik)], {"person": "ter", "tryb": TRYB_FORMY_NA_Ł}),
        ([Głowa(czasownik), aglutynant], {"person": V("p"), "tryb": TRYB_OZNAJMUJĄCY}),
        (
            [Głowa(czasownik), CZĄSTKA_TRYBU],
            {"person": "ter", "tryb": TRYB_PRZYPUSZCZAJĄCY},
        ),
        (
            [Głowa(czasownik), CZĄSTKA_TRYBU, aglutynant],
            {"person": V("p"), "tryb": TRYB_PRZYPUSZCZAJĄCY},
        ),
        (
            [Głowa(word("bedzie", number=V("n"), person=V("p"), **warunek))],
            {"person": V("p"), "tryb": TRYB_OZNAJMUJĄCY},
        ),
        (
            [
                forma_przyszła,
                Głowa(word("praet", number=V("n"), gender=V("g"), **niedokonany, **warunek)),
            ],
            {"person": V("p"), "tryb": TRYB_OZNAJMUJĄCY},
        ),
        (
            [forma_przyszła, Głowa(word("inf", **niedokonany, **warunek))],
            {"person": V("p"), "number": V("n"), "tryb": TRYB_OZNAJMUJĄCY},
        ),
    ]


def _poza_orzeczeniem(szyk: tuple[str, ...]) -> bool:
    """Czy tego szyku zdania nie składa już podmiot z orzeczeniem.

    ``grupa_orzeczenia`` jest czasownikiem wraz z tym, co on bierze, a stoi za podmiotem,
    więc zdanie o szyku podmiot-czasownik-dopełnienie ma wyprowadzenie tamtędy.
    Wypisane płasko drugi raz dałoby jednemu napisowi dwa wyprowadzenia.
    Pozostałych pięciu szyków ``grupa_orzeczenia`` nie składa, bo albo podmiot nie stoi w
    nich pierwszy, albo między nim a czasownikiem coś stoi.
    """
    return szyk[:2] != ("podmiot", "orzeczenie")
