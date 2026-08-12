"""Walenty przeczytany o trzy zdania: co czasownik bierze, a czego nie.

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

Ramy ten moduł nie zna: nazywa ją ``olski/subset.py`` razem z resztą gramatyki, a
stąd wychodzą same lematy wraz z tym, które z tych zdań są o nich prawdziwe.

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

Plik, który to czyta, nie stoi w repozytorium: pobiera się go tak, jak bank
drzew, i docs/subset.md trzyma polecenie.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path

from olski.walencja import BIERZE_BEZOKOLICZNIK, BIERZE_ZDANIE, NIE_BIERZE_BIERNIKA

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
#: jako osobny token, więc leksykon trzyma ją jako drugi wymiar klucza, a nie
#: jako część lematu.
SIĘ = " się"


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


def leksykon(path: Path | str) -> list[tuple[str, bool, tuple[str, ...]]]:
    """Lematy, o których ten leksykon coś mówi, każdy ze zwrotnością i ze swoimi zdaniami.

    Lemat, o którym prawdziwe nie jest żadne z tych zdań, nie wchodzi: zostaje mu
    rama domyślna, a wpis, który tylko ją powtarza, niczego nie rozstrzyga.
    """
    return sorted(
        (lemat.removesuffix(SIĘ), lemat.endswith(SIĘ), orzeczone)
        for lemat, ich_schematy in schematy(path).items()
        if (orzeczone := zdania(ich_schematy))
    )


NAGŁÓWEK = f"""\
# Leksykon walencyjny olskiego: lematy, o których ten leksykon coś mówi. Kolumny
# to lemat, cząstka `się` albo kreska w jej miejscu, oraz zdania rozdzielone
# przecinkiem.
#
# `{NIE_BIERZE_BIERNIKA}` mówi, że czasownik nie bierze dopełnienia w bierniku.
# `{BIERZE_BEZOKOLICZNIK}` mówi, że bierze bezokolicznik, którego wykonawcą jest
# jego własny podmiot. `{BIERZE_ZDANIE}` mówi, że bierze zdanie podrzędne
# wprowadzone przez `że`. Milczenie o lemacie zostawia mu ramę domyślną, czyli
# biernik, brak bezokolicznika i brak zdania podrzędnego.
#
# Plik jest generowany i nie pisze się go ręcznie. Powstaje z Walentego,
# słownika walencyjnego polszczyzny IPI PAN, wydanie tekstowe z 18 kwietnia
# 2016, i jest utworem zależnym od niego, więc idzie na tych samych warunkach:
# CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/
# Źródło: http://zil.ipipan.waw.pl/Walenty
#
# Wyprowadza go `olski/walenty.py`, który mówi, co stąd bierze, a czego nie;
# ramę nazywa `olski/subset.py`, a docs/subset.md trzyma polecenie wraz z tym,
# skąd wziąć plik wejściowy.
"""


def zapisz(wpisy: Sequence[tuple[str, bool, tuple[str, ...]]], out) -> None:
    out.write(NAGŁÓWEK)
    for lemat, zwrotny, orzeczone in wpisy:
        out.write(f"{lemat}\t{'się' if zwrotny else '-'}\t{','.join(orzeczone)}\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m olski.walenty",
        description="Wypisz lematy wraz ze zdaniami, które Walenty o ich ramie mówi.",
    )
    parser.add_argument("schematy", help="walenty_*_verbs_all.txt z wydania tekstowego")
    args = parser.parse_args(argv)
    zapisz(leksykon(args.schematy), sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
