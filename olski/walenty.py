"""Walenty przeczytany o jedno zdanie: który czasownik nie bierze biernika.

Walenty jest słownikiem walencyjnym polszczyzny i mówi o czasowniku znacznie
więcej, niż ta gramatyka umie żądać: typ frazy, kontrolę, koordynację, warstwę
semantyczną. Olski ma ramę o czterech pozycjach, więc czytanie jest zejściem w
dół i bierze stąd jedno zdanie: że czasownik nie bierze dopełnienia w bierniku.
Zdanie jest ujemne, bo wpis leksykonu tylko zawęża.

Ramy ten moduł nie zna: nazywa ją ``olski/subset.py`` razem z resztą gramatyki, a
stąd wychodzą same lematy, o których to zdanie jest prawdziwe.

Bezokolicznika to czytanie nie obejmuje, choć Walenty mówi i o nim, i jest to
wynik pomiaru, a nie przeoczenie. Leksykon odmawiający bezokolicznika tym samym
lematom, którym odmawia go Walenty, przyjmuje nad Składnicą dwa zdania mniej i
nie kupuje za to ani jednej jednoznaczności. Płaci za to cząstka ``się``, która w
polszczyźnie staje przy formie osobowej, należąc do bezokolicznika za nią:
``ma się odbyć`` jest u olskiego czasownikiem ``mieć się``, któremu Walenty
bezokolicznika nie daje.

Narzędnika też nie obejmuje, choć Walenty go zna. ``inst`` jest u olskiego
pozycją orzecznika, a Walenty nie odróżnia jej od argumentu narzędnikowego
(``bawić się czymś``), więc wpis wzięty stąd wpuszczałby orzecznik tam, gdzie
polszczyzna ma dopełnienie. Kopula zostaje przez to listą pisaną ręcznie w
``olski/subset.py``, i to ta lista, a nie ten moduł, wyłącza swoje lematy stąd.

Plik, który to czyta, nie stoi w repozytorium: pobiera się go tak, jak bank
drzew, i docs/subset.md trzyma polecenie.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path

#: Pozycja podmiotu. Podmiot ma u olskiego własną produkcję, a nie pozycję ramy,
#: więc to czytanie go pomija i pyta tylko o to, co przy czasowniku stoi obok niego.
PODMIOT = "subj"

#: Przypadek strukturalny. Walenty pisze tak biernik dopełnienia, żeby ująć jego
#: wymianę na dopełniacz pod zaprzeczeniem, więc pozycja niepodmiotowa z ``str``
#: jest tym, czego olski szuka jako biernika. ``np(acc)`` stoi obok niego tam,
#: gdzie wymiany nie ma.
BIERNIK = ("np(str)", "np(acc)")

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


def leksykon(path: Path | str) -> list[tuple[str, bool]]:
    """Lematy bez dopełnienia w bierniku, każdy ze swoją zwrotnością.

    Lemat, który biernik bierze, nie wchodzi: leksykon mówi jedno zdanie i wpis o
    lemacie, którego to zdanie nie dotyczy, niczego nie zabrania.
    """
    return sorted(
        (lemat.removesuffix(SIĘ), lemat.endswith(SIĘ))
        for lemat, ich_schematy in schematy(path).items()
        if not bierze(ich_schematy, BIERNIK)
    )


NAGŁÓWEK = """\
# Leksykon walencyjny olskiego: lematy, które nie biorą dopełnienia w bierniku,
# każdy z cząstką `się` albo z kreską w jej miejscu.
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


def zapisz(wpisy: Sequence[tuple[str, bool]], out) -> None:
    out.write(NAGŁÓWEK)
    for lemat, zwrotny in wpisy:
        out.write(f"{lemat}\t{'się' if zwrotny else '-'}\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m olski.walenty",
        description="Wypisz lematy, którym Walenty odmawia dopełnienia w bierniku.",
    )
    parser.add_argument("schematy", help="walenty_*_verbs_all.txt z wydania tekstowego")
    args = parser.parse_args(argv)
    zapisz(leksykon(args.schematy), sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
