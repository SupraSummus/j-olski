"""Leksykon projektu: polskie słowo odmienione, którego słownik nie ma.

Morfeusza prosi się wprost, żeby formy nieznanej nie zgadywał
(``olski/morph.py``), więc ``commitów`` wraca jako ``ign``
i nie bierze go ani jedna produkcja.
Odmianę takiego słowa deklaruje sekcja ``leksykon`` konfiguracji projektu
wpisem o trzech polach (``olski/konfiguracja.py``),
a docs/subset.md wywodzi, czemu deklaracja, czemu wskazanie leksemu
zamiast listy form i co to kosztuje.

Odmianę wydaje z takiego wpisu sam słownik.
Temat wzorca podmienia się na temat naszego słowa, a granicę między tematem
i końcówką wycina to, na czym formy wzorca przestają się zgadzać
(:func:`_granica`), więc alternację niesie wzorzec:
``bat`` ma ``bacie``, a ``commit`` bierze stamtąd i ``commitach``, i ``commicie``.
Wzorzec alternujący inaczej niż nasze słowo spełnia przy tym warunek na końcówkę
i wydaje formę fałszywą — ``pies`` dałby dla ``bies`` dopełniacz ``bsa`` —
i po to jest trzecie pole, czyli forma, którą wzorzec ma wydać:
:func:`odmiana` sprawdza ją, zamiast zostawić pomyłkę w ciszy.

Deklaracje te czyta się przy imporcie, a formy liczy się przy pierwszym pytaniu,
i różni je cena: wpisy stoją w pliku,
a formy żądają Morfeusza w trybie syntezy,
którego sama analiza tekstu nie potrzebuje do niczego.

Czytania leksykonu dochodzą do czytań słownika w :func:`z_leksykonu`
i woła ją cała analiza.
Funkcja jest jedna, bo dołożona osobno w każdym z wołających
byłaby tą samą regułą napisaną dwa razy.
Skład go nie czyta i o tym, co mu z tego zostaje, mówi ``todo/``.
"""

from __future__ import annotations

import functools
from collections.abc import Mapping
from dataclasses import replace
from typing import Any, NamedTuple

from olski.konfiguracja import LEKSYKON, ZłaKonfiguracja, sekcja
from olski.morph import Reading, Segment, generuj, tag

#: Klucz sekcji ``leksykon``, pod którym stoją wpisy.
WPISY_KLUCZ = "wpisy"

#: Część mowy, którą słownik daje skrótowi: ``tel`` stoi pod lematem ``telefon``.
#: Formą paradygmatu skrót nie jest — jest napisem uciętym — a wycina granicę
#: tematu tam, gdzie jej nie ma, więc paradygmat go nie liczy.
SKRÓT = "brev"


class ZłyWpis(Exception):
    """Wpis leksykonu, z którego nie wychodzi odmiana, którą on obiecuje.

    Wyjątek, a nie forma pominięta, bo każda przyczyna jest usterką w pliku
    pisanym ręką: leksem, którego słownik nie ma, paradygmat o dwóch tematach,
    końcówka, której nasz lemat nie ma, i świadek, którego wzorzec nie wydaje.
    Ruch po zgłoszeniu jest za każdym razem ten sam, czyli poprawiony wpis,
    i dlatego klasa jest jedna.
    """


class Wpis(NamedTuple):
    """Co leksykon mówi o jednym słowie."""

    #: Lemat słowa, którego słownik nie ma.
    lemat: str
    #: Identyfikator leksemu SGJP, wedle którego to słowo się odmienia.
    #: Leksem, a nie lemat, bo pod jednym napisem stoi ich kilka i różnią się
    #: odmianą: ``bat:Sm3~a`` ma dopełniacz ``bata``, a ``bat:Sm3~u`` ``batu``.
    wzorzec: str
    #: Forma, którą wzorzec ma wydać. Inna niż lemat, bo lemat wychodzi z każdego
    #: wzorca, który przeszedł warunek na końcówkę.
    świadek: str


def czytaj(dane: Mapping[str, Any]) -> tuple[Wpis, ...]:
    """Leksykon jako wpisy, w kolejności, w jakiej konfiguracja je wypisuje.

    Kluczem nic tu nie jest, bo pytanie idzie o formę, a nie o lemat,
    a jeden lemat ma tyle wpisów, ile leksemów mu się należy:
    ``olski`` jest i przymiotnikiem, i rzeczownikiem, tak jak ``polski``.
    """
    wpisy = []
    for numer, wpis in enumerate(dane.get(WPISY_KLUCZ, []), start=1):
        # Liczba pól wychodzi z samej klasy, więc pole dopisane do niej nie
        # zostawia tu warunku, który przepuszcza wpis bez tego pola.
        if not isinstance(wpis, list) or len(wpis) != len(Wpis._fields):
            raise ZłaKonfiguracja(
                f"sekcja {LEKSYKON}, wpis {numer}: "
                f"wpisem jest lemat, leksem i świadek, a nie {wpis!r}"
            )
        if not all(isinstance(pole, str) for pole in wpis):
            raise ZłaKonfiguracja(f"sekcja {LEKSYKON}, wpis {numer}: pola są napisami")
        wpisy.append(Wpis(*wpis))
    return tuple(wpisy)


#: Wpisy leksykonu tego projektu, przeczytane przy imporcie.
#: Pusta krotka znaczy projekt bez tej sekcji i jest odpowiedzią zwykłą.
WPISY = czytaj(sekcja(LEKSYKON, (WPISY_KLUCZ,)))


@functools.cache
def odmiana(wpis: Wpis) -> tuple[Reading, ...]:
    """Czytania, jakie ten wpis daje słowu, po jednym na formę i tag wzorca.

    Temat wzorca podmienia się na temat naszego słowa wszędzie tam, gdzie stoi,
    a nie na samym początku formy, bo formę wolno poprzedzić przedrostkiem:
    słownik trzyma ``niemalowanie`` w paradygmacie ``malować``,
    więc ``lintować`` bierze stamtąd ``nielintowanie``.

    Kolejność jest ustalona sortowaniem, a nie kolejnością słownika,
    bo czytania wychodzą stąd do wydruku werdyktu.
    """
    formy = [
        (forma, surowy)
        for forma, leksem, surowy, _nazwy, _kwalifikatory in generuj(_lemat(wpis.wzorzec))
        if leksem == wpis.wzorzec and surowy.split(":", 1)[0] != SKRÓT
    ]
    if not formy:
        raise ZłyWpis(f"{wpis.lemat}: słownik nie ma leksemu {wpis.wzorzec}")
    temat, końcówka = _granica(wpis.wzorzec, [forma for forma, _ in formy])
    if not wpis.lemat.endswith(końcówka):
        raise ZłyWpis(
            f"{wpis.lemat}: leksem {wpis.wzorzec} odmienia się od końcówki "
            f"„{końcówka}”, której ten lemat nie ma"
        )
    nasz = wpis.lemat[: len(wpis.lemat) - len(końcówka)]
    nasze = {
        Reading(form=forma.replace(temat, nasz, 1), lemma=wpis.lemat, tag=tag(surowy))
        for forma, surowy in formy
    }
    czytania = tuple(sorted(nasze, key=lambda czytanie: (czytanie.form, czytanie.tag.raw)))
    _sprawdź_świadka(wpis, czytania)
    return czytania


def _lemat(wzorzec: str) -> str:
    """Lemat, którym pyta się słownik o leksem: identyfikator bez swojego ogona.

    Ogonem jest wszystko za dwukropkiem — ``:Sm3~a``, ``:A`` — a słownik przyjmuje
    sam lemat i leksemy wydaje wszystkie, więc wybór między nimi zapada tutaj.
    """
    return wzorzec.split(":", 1)[0]


def _granica(wzorzec: str, formy: list[str]) -> tuple[str, str]:
    """Temat wzorca wraz z końcówką, której nasze słowo ma się trzymać.

    Tematem jest najdłuższy początek lematu wzorca stojący w każdej jego formie,
    a końcówką resztą tego lematu. Warunek na „w każdej formie” jest tym, co
    wpuszcza alternację: ``bacie`` nie zawiera ``bat``, więc temat schodzi do
    ``ba``, a końcówka ``t`` staje się tym, czego wzorzec żąda od naszego słowa.
    Tam, gdzie temat nie alternuje, końcówka jest pusta i wzorzec nie żąda niczego,
    bo temat wychodzi wtedy na cały lemat.
    """
    lemat = _lemat(wzorzec)
    for długość in range(len(lemat), 0, -1):
        temat = lemat[:długość]
        if all(temat in forma for forma in formy):
            return temat, lemat[długość:]
    raise ZłyWpis(f"{wzorzec}: formy tego leksemu nie mają wspólnego tematu z jego lematem")


def _sprawdź_świadka(wpis: Wpis, czytania: tuple[Reading, ...]) -> None:
    if wpis.świadek == wpis.lemat:
        raise ZłyWpis(f"{wpis.lemat}: świadkiem ma być forma inna niż lemat")
    formy = {czytanie.form for czytanie in czytania}
    if wpis.świadek not in formy:
        raise ZłyWpis(
            f"{wpis.lemat}: leksem {wpis.wzorzec} nie wydaje formy „{wpis.świadek}”, "
            f"tylko {', '.join(sorted(formy))}"
        )


@functools.lru_cache(maxsize=1)
def _wedle_formy() -> dict[str, tuple[Reading, ...]]:
    """Czytania leksykonu po formie, złożone z wszystkich wpisów.

    Forma jest kluczem złożonym z małych liter, bo słownik czyta ją tak samo:
    ``warszawa`` wraca z niego jako miasto, a ``Program`` jako ``program``.
    Czytania powtórzone schodzą, bo dwa wpisy jednego lematu różnią się jedną
    komórką: ``konstytuentu`` i ``konstytuenta`` są dwoma dopełniaczami, a
    ``konstytuentem`` jednym narzędnikiem, choćby stało w obu paradygmatach.
    """
    wedle: dict[str, list[Reading]] = {}
    for wpis in WPISY:
        for czytanie in odmiana(wpis):
            znane = wedle.setdefault(czytanie.form.casefold(), [])
            if czytanie not in znane:
                znane.append(czytanie)
    return {forma: tuple(czytania) for forma, czytania in wedle.items()}


def czytania(forma: str) -> tuple[Reading, ...]:
    """Czytania, jakie leksykon projektu daje tej formie, albo nic.

    Forma wraca w czytaniu taka, jak stoi w tekście, a nie taka, jak ją wydał
    słownik, bo tym samym oddaje ją Morfeusz: ``Program`` wraca od niego z
    lematem ``program`` i z formą ``Program``.
    """
    znalezione = _wedle_formy().get(forma.casefold(), ())
    return tuple(replace(czytanie, form=forma) for czytanie in znalezione)


def z_leksykonu(segment: Segment) -> Segment:
    """Krawędź wraz z czytaniami, jakie leksykon projektu daje jej formie.

    Czytania leksykonu dochodzą do tych, które ma słownik, a nie zastępują ich,
    bo leksykon orzeka o formie, a nie łata milczenie Morfeusza: forma, którą
    słownik zna, a leksykon o niej mówi, ma czytania jednego i drugiego, i tyle
    właśnie czytań ma wtedy w polszczyźnie.

    Czytanie ``ign`` stąd schodzi, bo mówi ono, że słowa nie zna nikt, a
    leksykon właśnie je nazwał. Krawędź bez czytań z tego nie wyjdzie: znika ono
    tylko tam, gdzie leksykon coś dołożył.
    """
    czytania_leksykonu = czytania(segment.form)
    if not czytania_leksykonu:
        return segment
    znane = tuple(reading for reading in segment.readings if reading.tag.known)
    return replace(segment, readings=znane + czytania_leksykonu)
