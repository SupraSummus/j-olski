"""Walenty przeczytany o trzy zdania i o jedną pozycję ramy.

Walenty jest słownikiem walencyjnym polszczyzny i mówi o czasowniku znacznie
więcej, niż ta gramatyka bierze: typ frazy, kontrolę, koordynację, warstwę
semantyczną. Olski ma ramę o kilku pozycjach, więc czytanie jest zejściem w dół i
bierze stąd trzy zdania na lemat.

Pierwsze jest ujemne i mówi, że czasownik nie bierze dopełnienia w bierniku.
Drugie jest twierdzące i mówi, że bierze bezokolicznik, którego wykonawcą jest
jego własny podmiot. Kierunki są przeciwne, bo przeciwne są domyślności, od
których oba odejmują: rama domyślna ma dopełnienie w bierniku i nie ma
bezokolicznika, więc milczenie o lemacie znaczy przy pierwszym zdaniu, że biernik
bierze, a przy drugim, że bezokolicznika nie bierze.

Trzecie jest twierdzące jak drugie i mówi, że czasownik bierze zdanie
podrzędne wprowadzone przez ``że``, czyli że stoi przy nim to, co ktoś mówi,
wie albo w co nie wierzy. Domyślność jest ta sama co przy bezokoliczniku, bo
rama domyślna takiej pozycji nie ma, a bez tego zdania nic nie odróżnia
``wiedzieć`` od ``zamykać``: oba biorą biernik, a zdanie podrzędne bierze
jeden z nich.

Czwarte czytanie nie jest zdaniem prawda-fałsz, tylko zbiorem, i wychodzi z niego
kolumna przyimków: pozycja ``prepnp`` mówi, którego przyimka rama tego słowa żąda.
Czyta ją warstwa rozstrzygająca, a nie gramatyka, i po obu stronach spornego
wyrażenia przyimkowego: rzeczownik wskazuje gospodarza, a czasownik odbiera
wskazanie. Dlaczego wskazuje jedna strona, a nie obie, wywodzi
docs/disambiguation.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie.

Rzeczownik wchodzi przez to obok czasownika i jest drugim plikiem wejściowym.
Katalog przymiotnikowy i przysłówkowy zostają na zewnątrz, bo nikt o nie nie
pyta: sporny wybór stawiają dwie strony, a te dwie są w tym zapisie czasownikiem
i rzeczownikiem (``strona`` w ``olski/rozstrzyganie.py``).

Ramy ten moduł nie zna: nazywa ją ``olski/subset.py`` razem z resztą gramatyki, a
stąd wychodzą same słowa wraz z tym, które z tych zdań są o nich prawdziwe
i jakich przyimków żąda ich rama.

Kontrolę czytamy z Walentego, a nie z lematu, bo to ona odróżnia dwa czasowniki z
bezokolicznikiem, których polszczyzna nie składa tak samo. U ``chcieć`` etykietę
kontrolującą nosi pozycja podmiotu, czyli wykonawcą bezokolicznika jest podmiot, a
u ``kazać`` nosi ją pozycja celownikowa, czyli wykonawcą jest ten, komu kazano.
Celownika ta gramatyka nie ma, więc drugiego z nich nie ma jak zapisać, i lemat
kontrolowany z celownika stąd nie wychodzi.

Czytanie ujemne obejmuje sam biernik, choć Walenty zna wszystkie przypadki.
Narzędnika nie bierze, bo ``inst`` jest u olskiego pozycją orzecznika, a Walenty
nie odróżnia jej od argumentu narzędnikowego (``bawić się czymś``), więc wpis
wzięty stąd wpuszczałby orzecznik tam, gdzie polszczyzna ma dopełnienie. Kopula
zostaje przez to listą pisaną ręcznie w ``olski/subset.py``, i to ta lista, a nie
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
#: ``olski/attachment.py`` niesie sam przyimek: ``prepnp(o,loc)`` i
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
    if bierze_bezokolicznik_podmiotu(schematy_lematu):
        orzeczone.append(BIERZE_BEZOKOLICZNIK)
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
# `{BIERZE_BEZOKOLICZNIK}` mówi, że bierze bezokolicznik, którego wykonawcą jest
# jego własny podmiot. `{BIERZE_ZDANIE}` mówi, że bierze zdanie podrzędne
# wprowadzone przez `że`. Milczenie o lemacie zostawia mu ramę domyślną, czyli
# biernik, brak bezokolicznika i brak zdania podrzędnego. Zdania te są o
# czasowniku, więc wiersz rzeczownika ma tę kolumnę pustą.
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
# Wyprowadza go `olski/walenty.py`, który mówi, co stąd bierze, a czego nie;
# ramę nazywa `olski/subset.py`, a docs/subset.md trzyma polecenie wraz z tym,
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
        prog="python3 -m olski.walenty",
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
