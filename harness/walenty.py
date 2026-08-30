"""Walenty odczytany do zdań o lemacie i do kolumny przyimków.

Walenty jest słownikiem walencyjnym polszczyzny i mówi o czasowniku znacznie
więcej, niż ta gramatyka bierze: typ frazy, kontrolę, koordynację, warstwę
semantyczną. Olski ma ramę o kilku pozycjach, więc czytanie jest zejściem w dół,
a które zdania stąd wychodzą, mówi :func:`zdania`.

Zdanie o bierniku jest ujemne i mówi, że czasownik nie bierze dopełnienia w
bierniku, a zdania o bezokoliczniku twierdzące. Kierunki są przeciwne, bo
przeciwne są domyślności, od których oba odejmują: rama domyślna ma dopełnienie
w bierniku i nie ma bezokolicznika, więc milczenie o lemacie znaczy przy pierwszym
z nich, że biernik bierze, a przy drugim, że bezokolicznika nie bierze.

Zdania o bezokoliczniku są dwa i różni je kontrola. Szersze mówi, że
bezokolicznik przy tym czasowniku stoi; węższe, że wykonawcą bezokolicznika jest
podmiot tego samego schematu. Osobne są dlatego, że pytający pytają o co innego,
i po którą stronę idzie każdy z nich, mówi ``olski/walencja.py``.

Zdanie o celowniku i zdanie o dopełniaczu są twierdzące jak to o bezokoliczniku i
mówią, że czasownik bierze dopełnienie w tym przypadku. Rama domyślna przypadka
poza biernikiem nie ma, więc milczenie o lemacie odmawia mu tej pozycji, a
gramatyka wpuszcza ją tym lematom, które Walenty tu wymienia
(docs/warstwa-leksykalna.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu).

Zdanie o zdaniu podrzędnym wprowadzonym przez ``że`` jest twierdzące tak samo i
mówi, że stoi przy czasowniku to, co ktoś mówi, wie albo w co nie wierzy.
Domyślność jest ta sama co przy bezokoliczniku, bo rama domyślna takiej pozycji
nie ma, a bez tego zdania nic nie odróżnia ``wiedzieć`` od ``zamykać``: oba biorą
biernik, a zdanie podrzędne bierze jeden z nich.

Kolumna przyimków nie jest zdaniem prawda-fałsz, tylko zbiorem: pozycja
``prepnp`` mówi, którego przyimka rama tego słowa żąda.
Czyta ją warstwa rozstrzygająca, a nie gramatyka, i po obu stronach spornego
wyrażenia przyimkowego: rzeczownik wskazuje gospodarza, a czasownik odbiera
wskazanie. Dlaczego wskazuje jedna strona, a nie obie, wywodzi
docs/disambiguation.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie.

Rzeczownik wchodzi przez to obok czasownika i jest drugim plikiem wejściowym.
Katalog przymiotnikowy i przysłówkowy zostają na zewnątrz, bo nikt o nie nie
pyta: sporny wybór stawiają dwie strony, a te dwie są w tym zapisie czasownikiem
i rzeczownikiem (``strona`` w ``olski/rozstrzyganie.py``).

Ramy ten moduł nie zna: nazywa ją ``olski/subset/rama.py`` razem z resztą gramatyki, a
stąd wychodzą same słowa wraz z tym, które z tych zdań są o nich prawdziwe
i jakich przyimków żąda ich rama.

Kontrolę czytamy z Walentego, a nie z lematu, bo to ona odróżnia dwa czasowniki z
bezokolicznikiem, których polszczyzna nie składa tak samo. U ``chcieć`` etykietę
kontrolującą nosi pozycja podmiotu, czyli wykonawcą bezokolicznika jest podmiot, a
u ``kazać`` nosi ją pozycja celownikowa, czyli wykonawcą jest ten, komu kazano.
Drugiego z nich skład nie ma czym zapisać, więc lemat kontrolowany z celownika
wychodzi stąd samym zdaniem szerszym. Parser czyta właśnie je i o wykonawcę nie
pyta ani jedną produkcją; gdyby czytał węższe, ``udać się`` i ``dać się``
straciłyby bezokolicznik, bo kontroluje w nich celownik.

Narzędnika nie bierze ani jedno z tych zdań, choć Walenty zna wszystkie
przypadki, bo ``inst`` jest u olskiego pozycją orzecznika, a Walenty nie odróżnia
jej od argumentu narzędnikowego (``bawić się czymś``), więc wpis wzięty stąd
wpuszczałby orzecznik tam, gdzie polszczyzna ma dopełnienie. Kopula
zostaje przez to listą pisaną ręcznie w ``olski/subset/rama.py``, i to ta lista, a nie
ten moduł, wyłącza swoje lematy stąd.

Pliki, które to czyta, nie stoją w repozytorium: pobiera się je tak, jak bank
drzew, i docs/subset.md trzyma polecenie.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path

from olski.walencja import (
    BIERZE_BEZOKOLICZNIK,
    BIERZE_BEZOKOLICZNIK_PODMIOTU,
    BIERZE_CELOWNIK,
    BIERZE_CELOWNIK_PRZY_WYPEŁNIENIU,
    BIERZE_DOPEŁNIACZ,
    BIERZE_ZDANIE,
    CZASOWNIK,
    CZASOWNIK_ZWROTNY,
    NIE_BIERZE_BIERNIKA,
    RZECZOWNIK,
)

#: Pozycja podmiotu. Podmiot ma u olskiego własną produkcję, a nie pozycję ramy,
#: więc to czytanie go pomija i pyta tylko o to, co przy czasowniku stoi obok niego.
PODMIOT = "subj"

#: Przypadek strukturalny. Walenty pisze tak biernik dopełnienia, żeby ująć jego
#: wymianę na dopełniacz pod zaprzeczeniem, więc pozycja niepodmiotowa z ``str``
#: jest tym, czego olski szuka jako biernika. ``np(acc)`` stoi obok niego tam,
#: gdzie wymiany nie ma.
BIERNIK = ("np(str)", "np(acc)")

#: Kształt frazy bezokolicznikowej. Aspekt stoi u Walentego w nawiasie —
#: ``infp(_)`` obok ``infp(perf)`` — a olski aspektu nie żąda, więc szuka się
#: samej nazwy kształtu.
BEZOKOLICZNIK = "infp"

#: Kształt zdania podrzędnego wprowadzonego przez ``że``. Spójnik stoi u
#: Walentego w nawiasie — ``cp(int)`` obok ``cp(żeby)`` — a skład wypisuje jeden
#: i o jeden pyta, więc szuka się kształtu wraz ze spójnikiem i wraz z nawiasem
#: zamykającym: bez niego ten napis jest przedrostkiem ``cp(żeby)``. Sama nazwa
#: kształtu oddziela go od ``ncp`` oraz ``prepncp``, czyli od zdania podrzędnego
#: pod zaimkiem albo pod przyimkiem, których skład nie ma czym wypisać.
ZDANIE = "cp(że)"

#: Kształt pytania zależnego. Walenty pisze je tym samym ``cp`` co zdanie z ``że``
#: i rozdziela oba spójnikiem w nawiasie, więc szuka się kształtu wraz z nim.
PYTANIE = "cp(int)"

#: Kształty, które olski ma pozycją ramy, czyli to, co u niego wypełnia tę
#: pozycję: dopełnienie w bierniku, fraza bezokolicznikowa, zdanie podrzędne i
#: pytanie zależne. Orzecznika w tej krotce nie ma z tego samego powodu, dla
#: którego nie ma go w żadnym zdaniu tego leksykonu (docstring modułu).
WYPEŁNIENIA = (*BIERNIK, BEZOKOLICZNIK, ZDANIE, PYTANIE)

#: Kształt dopełnienia w celowniku. Wymiany na inny przypadek ta pozycja u
#: Walentego nie ma, więc kształt jest jeden, a przypadek strukturalny jej nie
#: obejmuje: ``np(str)`` jest u niego biernikiem wymieniającym się na dopełniacz.
CELOWNIK = ("np(dat)",)

#: Kształty dopełnienia w dopełniaczu. Dwa, bo Walenty rozdziela dopełniacz
#: żądany ramą od dopełniacza cząstkowego — ``potrzebować`` ma ``np(part)``,
#: a ``żądać`` ``np(gen)`` — a obie pozycje realizuje polszczyzna tą samą formą i
#: olski nie ma czym ich rozdzielić.
#:
#: Dopełniacza spod przeczenia nie ma w tej parze i mieć go nie może: tamten
#: wchodzi w miejsce biernika i stoi w gramatyce drugą produkcją tej samej pozycji
#: (docs/konstrukcje-gramatyczne.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem),
#: a Walenty pisze go tym samym ``np(str)``, co biernik.
DOPEŁNIACZ = ("np(gen)", "np(part)")

#: Etykiety, którymi Walenty zapisuje kontrolę: kto wykonuje to, o czym mówi
#: pozycja podrzędna. Pozycja kontrolowana jest tą, w której stoi bezokolicznik,
#: a kontrolującą pyta się o to, czy jest nią podmiot.
KONTROLUJĄCA = "controller"
KONTROLOWANA = "controllee"

#: Cząstka, którą Walenty pisze przy lemacie czasownika zwrotnego. Olski widzi ją
#: jako osobny token, więc leksykon trzyma ją klasą słowa, a nie częścią lematu.
SIĘ = " się"

#: Kształt pozycji przyimkowej, wraz z przyimkiem w środku. Przypadek stoi za
#: przecinkiem i to czytanie o niego nie pyta, bo ``Attachment`` w
#: ``harness/attachment.py`` niesie sam przyimek: ``prepnp(o,loc)`` i
#: ``prepnp(o,acc)`` wychodzą stąd jednym wpisem. Ile ten brak zawyża zasięg
#: świadka, mówi docs/disambiguation.md.
PRZYIMKOWA = re.compile(r"prepnp\(([^,)]+),")

#: Pozycja zleksykalizowana, czyli taka, w której Walenty żąda konkretnego słowa
#: obok przyimka: ``czekać na czas dobry``. Ramą lematu to nie jest, bo żądanie
#: dotyczy słowa stojącego w tej pozycji, więc odpada cała, a nie sam jej przyimek.
ZLEKSYKALIZOWANA = "lex("

#: Kwalifikatory pewności, pod którymi schemat wchodzi. Walenty pisze ich pięć, a
#: ``zły`` i ``archaiczny`` nazywają schemat, którego ten rejestr nie ma;
#: ``potoczny`` zostaje, bo mówi o rejestrze, a nie o poprawności schematu.
#:
#: Zwężenie do samego ``pewny`` zmierzono sondą i nie rusza ono żadnej liczby
#: o więcej niż pół punktu, więc kolumna go nie bierze;
#: docs/disambiguation.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie.
BRANE = frozenset({"pewny", "wątpliwy", "potoczny"})

#: Kwalifikator schematu niewątpliwego. Sonda ma na nim wariant, więc stała stoi
#: tu obok :data:`BRANE`, choć kolumna leksykonu bierze wszystkie trzy.
PEWNY = "pewny"


def pozycje(schemat: str) -> Iterator[tuple[str, str]]:
    """Pozycje schematu, każda jako etykieta i to, czego pozycja żąda.

    Rozbiór idzie po znakach, a nie po ``split``, bo pozycja zleksykalizowana
    trzyma własne plusy w nawiasach i rozcięta na nich przestaje być pozycją.
    Plus rozdziela pozycje tylko poza wszystkimi nawiasami.
    """
    poziom, bieżąca = 0, ""
    for znak in schemat:
        if znak in "{(":
            poziom += 1
        elif znak in "})":
            poziom -= 1
        if znak == "+" and poziom == 0:
            yield _pozycja(bieżąca)
            bieżąca = ""
        else:
            bieżąca += znak
    yield _pozycja(bieżąca)


def _pozycja(tekst: str) -> tuple[str, str]:
    etykieta, _, żądanie = tekst.partition("{")
    return etykieta.strip(), żądanie


def _pewność(schemat: str) -> str:
    """Kwalifikator pewności schematu, czyli pierwsze pole za lematem."""
    return schemat.split(":")[0].strip()


def przyimki(schematy_lematu: Sequence[str], tylko_pewne: bool = False) -> frozenset[str]:
    """Przyimki, których ten lemat żąda pozycją niepodmiotową.

    Kryterium jest jedno i czytają je dwie strony:
    kolumna leksykonu, którą wypisuje :func:`leksykon`,
    i sonda wyceniająca to kryterium nad samym Walentym (``harness/rama.py``).
    Druga kopia rozeszłaby się cicho,
    bo rozejście widać dopiero w liczbach, a nie w wydruku.

    Przyimka złożonego to czytanie nie widzi i nie ma po co:
    Walenty pisze go osobnym kształtem — ``comprepnp(na temat)`` —
    a bank drzew daje jeden token,
    więc żadna strona sporu nie ma czym się nim dopasować.
    """
    znalezione: set[str] = set()
    for schemat in schematy_lematu:
        pewność = _pewność(schemat)
        if pewność not in BRANE or (tylko_pewne and pewność != PEWNY):
            continue
        for etykieta, żądanie in pozycje(schemat):
            if PODMIOT in etykieta:
                continue
            for wariant in żądanie.split(";"):
                if ZLEKSYKALIZOWANA in wariant:
                    continue
                znalezione.update(PRZYIMKOWA.findall(wariant))
    return frozenset(znalezione)


def bierze(schematy_lematu: Sequence[str], czego: Sequence[str]) -> bool:
    """Czy któryś ze schematów ma pozycję niepodmiotową żądającą tego kształtu."""
    return any(
        any(kształt in żądanie for kształt in czego)
        for schemat in schematy_lematu
        for etykieta, żądanie in pozycje(schemat)
        if PODMIOT not in etykieta
    )


def bierze_ramą(schematy_lematu: Sequence[str], czego: Sequence[str]) -> bool:
    """To samo pytanie, zadane samym schematom, które mówią o ramie lematu.

    Rozdziela te dwa pytania kierunek zdania, które z każdego z nich wychodzi.
    Zdanie ujemne odejmuje od ramy domyślnej, więc kształt policzony za szeroko
    zostawia lemat przy tej ramie i leksykon o nim milczy. Zdanie twierdzące ramę
    poszerza, więc ta sama pomyłka wpuszcza dopełnienie tam, gdzie polszczyzna go
    nie stawia, a obietnicą podzbioru jest, że każde zdanie olskiego jest zdaniem
    polskim.

    O ramie nie mówią dwa rodzaje schematów. Schemat z pozycją zleksykalizowaną
    jest zwrotem, a pozycja stojąca w nim obok należy do tego zwrotu, a nie do
    lematu: `mieć` bierze celownik w `mieć komuś za złe` i nie bierze go poza tym,
    więc pozycja policzona osobno wpuszczałaby `Ludzie mają rozum.` z
    dopełnieniem w celowniku wszędzie tam, gdzie forma tak się czyta. Schemat
    spoza :data:`BRANE` nazywa zaś polszczyznę, której ten rejestr nie pisze.
    Odpada przez to cały schemat, a nie sama jego pozycja.
    """
    return bierze(_ramowe(schematy_lematu), czego)


def _ramowe(schematy_lematu: Sequence[str]) -> list[str]:
    """Same te schematy, które o ramie lematu mówią; odsiew wywodzi :func:`bierze_ramą`."""
    return [
        schemat
        for schemat in schematy_lematu
        if ZLEKSYKALIZOWANA not in schemat and _pewność(schemat) in BRANE
    ]


def bierze_celownik_przy_wypełnieniu(schematy_lematu: Sequence[str]) -> bool:
    """Czy któryś schemat ramowy stawia celownik obok drugiego wypełnienia.

    Pytanie idzie o jeden schemat naraz, a nie o dwa zdania leksykonu policzone
    osobno, i to jest cała różnica między tym zdaniem a koniunkcją tamtych dwóch.
    Lemat, który celownik bierze w jednym schemacie, a biernik w drugim, pary nie
    ma, a koniunkcja by mu ją dała, więc para wzięta osobno wpuszczałaby zdanie,
    którego polszczyzna nie ma, i łamała obietnicę podzbioru, o której mówi
    :func:`bierze_ramą`.

    Sąsiadem musi być wypełnienie, które olski ma pozycją ramy
    (:data:`WYPEŁNIENIA`), a nie dowolna druga pozycja schematu. Celownik obok
    wyrażenia przyimkowego — `mówić komuś o czymś` — pary nie potrzebuje, bo
    okolicznik przyłącza się u olskiego za darmo i to zdanie wychodzi już dziś.

    Które wypełnienie przy nim stoi, to zdanie przemilcza, i jest to ta sama
    zgrubność, którą ma :data:`olski.subset.RAMA_DOMYŚLNA`.
    Co każde z tych trzech zawężeń kosztuje w lematach, trzyma
    docs/warstwa-leksykalna.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia.
    """
    for schemat in _ramowe(schematy_lematu):
        stoi_celownik = stoi_wypełnienie = False
        for etykieta, żądanie in pozycje(schemat):
            if PODMIOT in etykieta:
                continue
            #  Pozycja trafiona celownikiem za sąsiada się już nie liczy, bo
            #  jedna pozycja Walentego bywa wyborem kształtów: `dziwić się` ma
            #  `{np(dat);cp(int);cp(że)}`, czyli celownik albo pytanie, a nie
            #  celownik obok pytania.
            if any(kształt in żądanie for kształt in CELOWNIK):
                stoi_celownik = True
            elif any(kształt in żądanie for kształt in WYPEŁNIENIA):
                stoi_wypełnienie = True
        if stoi_celownik and stoi_wypełnienie:
            return True
    return False


def bierze_bezokolicznik_podmiotu(schematy_lematu: Sequence[str]) -> bool:
    """Czy któryś ze schematów daje bezokolicznik, którego wykonawcą jest podmiot.

    Pytanie stawia się o cały schemat, a nie o jedną pozycję, bo kontrola jest
    relacją między dwiema: bezokolicznik stoi w pozycji kontrolowanej, a olski
    bierze ją tylko wtedy, gdy kontroluje ją podmiot tego samego schematu.
    Schemat, w którym kontroluje kto inny — ``kazać`` kontrolowane z celownika —
    daje polszczyźnie zdanie, którego ta gramatyka nie ma czym zapisać.
    """
    return any(_kontrola_podmiotu(schemat) for schemat in schematy_lematu)


def _kontrola_podmiotu(schemat: str) -> bool:
    wszystkie = list(pozycje(schemat))
    kontroluje_podmiot = any(
        PODMIOT in etykieta and KONTROLUJĄCA in etykieta for etykieta, _żądanie in wszystkie
    )
    stoi_bezokolicznik = any(
        KONTROLOWANA in etykieta and BEZOKOLICZNIK in żądanie for etykieta, żądanie in wszystkie
    )
    return kontroluje_podmiot and stoi_bezokolicznik


def schematy(path: Path | str) -> dict[str, list[str]]:
    """Schematy Walentego po lematach, prosto z wydania tekstowego.

    Wiersz jest lematem i pięcioma polami przed samym schematem, a komentarz
    zaczyna się od procentu. Pola przed schematem — pewność, kwalifikator, aspekt
    — nie zmieniają tego, czego czasownik może wziąć, więc zostają w tekście
    schematu i nikt o nie tutaj nie pyta.
    """
    zebrane: dict[str, list[str]] = {}
    with open(path, encoding="utf-8") as plik:
        for wiersz in plik:
            wiersz = wiersz.lstrip("﻿").rstrip("\n")
            if wiersz.startswith("%") or ":" not in wiersz:
                continue
            lemat, _, reszta = wiersz.partition(":")
            zebrane.setdefault(lemat.strip(), []).append(reszta)
    return zebrane


def zdania(schematy_lematu: Sequence[str]) -> tuple[str, ...]:
    """Które zdania tego leksykonu są o tym lemacie prawdziwe."""
    orzeczone = []
    if not bierze(schematy_lematu, BIERNIK):
        orzeczone.append(NIE_BIERZE_BIERNIKA)
    if bierze_ramą(schematy_lematu, CELOWNIK):
        orzeczone.append(BIERZE_CELOWNIK)
    if bierze_celownik_przy_wypełnieniu(schematy_lematu):
        orzeczone.append(BIERZE_CELOWNIK_PRZY_WYPEŁNIENIU)
    if bierze_ramą(schematy_lematu, DOPEŁNIACZ):
        orzeczone.append(BIERZE_DOPEŁNIACZ)
    if bierze_ramą(schematy_lematu, (BEZOKOLICZNIK,)):
        orzeczone.append(BIERZE_BEZOKOLICZNIK)
    if bierze_bezokolicznik_podmiotu(schematy_lematu):
        orzeczone.append(BIERZE_BEZOKOLICZNIK_PODMIOTU)
    if bierze(schematy_lematu, (ZDANIE,)):
        orzeczone.append(BIERZE_ZDANIE)
    return tuple(orzeczone)


def leksykon(
    czasowniki: Path | str, rzeczowniki: Path | str
) -> list[tuple[str, str, tuple[str, ...], frozenset[str]]]:
    """Słowa, o których ten leksykon coś mówi, każde z klasą, zdaniami i przyimkami.

    Słowo, o którym prawdziwe nie jest żadne zdanie
    i którego rama nie żąda żadnego przyimka, nie wchodzi:
    zostaje mu rama domyślna,
    a wpis, który tylko ją powtarza, niczego nie rozstrzyga.
    Warunek jest przez to sumą dwóch, a nie samymi zdaniami:
    rzeczownik żadnego zdania tego leksykonu nie orzeka,
    więc pytany o same zdania nie wszedłby ani razu.

    Kolejność jest kolejnością lematu i klasy, bo taką kolejność ma plik.
    """
    zebrane = [
        (
            lemat.removesuffix(SIĘ),
            CZASOWNIK_ZWROTNY if lemat.endswith(SIĘ) else CZASOWNIK,
            zdania(ich_schematy),
            przyimki(ich_schematy),
        )
        for lemat, ich_schematy in schematy(czasowniki).items()
    ]
    zebrane += [
        (lemat, RZECZOWNIK, (), przyimki(ich_schematy))
        for lemat, ich_schematy in schematy(rzeczowniki).items()
    ]
    return sorted(
        (lemat, klasa, orzeczone, żądane)
        for lemat, klasa, orzeczone, żądane in zebrane
        if orzeczone or żądane
    )


NAGŁÓWEK = f"""\
# Leksykon walencyjny olskiego: słowa, o których ten leksykon coś mówi. Kolumny
# to lemat, klasa słowa, zdania rozdzielone przecinkiem oraz przyimki, których
# żąda rama tego słowa, także rozdzielone przecinkiem.
#
# Klasą jest `{CZASOWNIK}`, `{CZASOWNIK_ZWROTNY}` albo `{RZECZOWNIK}`. Rozdziela
# ona wpisy o jednym lemacie, bo jeden lemat bywa kilkoma słowami naraz:
# `otwierać` bierze dopełnienie w bierniku, a `otwierać się` go nie bierze.
#
# `{NIE_BIERZE_BIERNIKA}` mówi, że czasownik nie bierze dopełnienia w bierniku.
# `{BIERZE_CELOWNIK}` i `{BIERZE_DOPEŁNIACZ}` mówią, że bierze dopełnienie w tym
# przypadku. `{BIERZE_CELOWNIK_PRZY_WYPEŁNIENIU}` mówi, że jeden schemat stawia
# ten celownik obok wypełnienia, czyli obok biernika, bezokolicznika, zdania
# podrzędnego albo pytania zależnego. `{BIERZE_BEZOKOLICZNIK}` mówi, że przy tym
# czasowniku bezokolicznik stoi, a `{BIERZE_BEZOKOLICZNIK_PODMIOTU}` — że
# wykonawcą tego bezokolicznika jest jego własny podmiot; drugie zdanie jest
# węższe od pierwszego tak samo jak celownik przy wypełnieniu od celownika.
# `{BIERZE_ZDANIE}` mówi, że bierze zdanie podrzędne wprowadzone przez `że`.
# Milczenie o lemacie zostawia mu ramę domyślną, czyli biernik, brak dopełnienia
# w przypadku innym, brak bezokolicznika i brak zdania podrzędnego. Zdania te są
# o czasowniku, więc wiersz rzeczownika ma tę kolumnę pustą.
#
# Kolumna przyimków jest zbiorem, a nie zdaniem prawda-fałsz, i pusta znaczy
# w niej dwie rzeczy naraz: że rama tego słowa nie ma pozycji przyimkowej albo
# że Walenty ramy temu słowu nie daje. Czyta ją świadek ramowy w
# `olski/rozstrzyganie.py`, a nie gramatyka.
#
# Plik jest generowany i nie pisze się go ręcznie. Powstaje z Walentego,
# słownika walencyjnego polszczyzny IPI PAN, wydanie tekstowe z 18 kwietnia
# 2016, i jest utworem zależnym od niego, więc idzie na tych samych warunkach:
# CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/
# Źródło: http://zil.ipipan.waw.pl/Walenty
#
# Wyprowadza go `harness/walenty.py`, który mówi, co stąd bierze, a czego nie;
# ramę nazywa `olski/subset/rama.py`, a docs/subset.md trzyma polecenie wraz z tym,
# skąd wziąć pliki wejściowe.
"""


def zapisz(wpisy: Sequence[tuple[str, str, tuple[str, ...], frozenset[str]]], out) -> None:
    """Wypisz wpisy w tej kolejności, w której przyszły.

    Zbiór przyimków wychodzi posortowany,
    bo kolejność zbioru jest inna w każdym przebiegu,
    a plik generowany ma się nie różnić od przebiegu do przebiegu
    (CLAUDE.md, o porządku wypisywanego wyjścia).
    """
    out.write(NAGŁÓWEK)
    for lemat, klasa, orzeczone, żądane in wpisy:
        out.write(f"{lemat}\t{klasa}\t{','.join(orzeczone)}\t{','.join(sorted(żądane))}\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.walenty",
        description="Wypisz słowa wraz z tym, co Walenty o ich ramie mówi.",
    )
    parser.add_argument("schematy", help="walenty_*_verbs_all.txt z wydania tekstowego")
    parser.add_argument(
        "--rzeczowniki",
        required=True,
        help="walenty_*_nouns_all.txt z wydania tekstowego; bez niego kolumna"
        " przyimków po stronie rzeczownika byłaby pusta, a świadek ramowy milczałby",
    )
    args = parser.parse_args(argv)
    zapisz(leksykon(args.schematy, args.rzeczowniki), sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
