"""Werdykt olskiego jako dane, czyli to, co witryna oddaje przeglądarce.

Frazę werdyktu ma na własność kod (``Verdict.explain`` w ``olski/werdykt.py``),
więc ten moduł jej nie tłumaczy i drugiej nie pisze:
przez API idzie ta sama fraza, którą drukuje ``olski-check``.
Po polsku jest przez to i werdykt, i strona wokół niego —
podpisy, przyciski, nagłówki — a co z tego czyje, mówi ``docs/witryna.md``.

Klucz JSON-a wybieramy tutaj, więc jest po polsku.
Nazwa roli w odczytaniu przychodzi z ``DEKLARACJA`` w ``olski/subset/deklaracja.py``
i zostaje taka, jaka przyszła.
"""

from __future__ import annotations

import functools
import random
from dataclasses import asdict
from typing import Any

from olski.rozstrzyganie import (
    Rozstrzygnięcie,
    Sąsiedztwo,
    Świadek,
    domyślni,
    rozstrzygnij,
    sąsiedztwa,
)
from olski.skład.makieta import losuj
from olski.werdykt import Podsumowanie, Verdict, check, dalsze_zatrzymania

#: Ile akapitów makieta wypisuje najwyżej. Losowanie akapitu jest tanie, więc
#: granica jest tu przeciw liczbie z żądania: `akapity=100000` zajęłoby workera.
NAJWIĘCEJ_AKAPITÓW = 20


@functools.cache
def _świadkowie() -> tuple[Świadek, ...]:
    """Świadkowie warstwy rozstrzygającej, raz na proces, bo tabela skłonności
    wchodzi z pliku, a proces obsługuje tyle żądań, ile ich przyjdzie."""
    return tuple(domyślni())


def zbadaj(tekst: str) -> dict[str, Any]:
    """Werdykt o każdym zdaniu tekstu wraz z podsumowaniem całości."""
    werdykty = check(tekst)
    #  Sąsiedztwa liczą się dla całego tekstu naraz, bo akapit jest jego
    #  własnością: zdanie samo nie wie, co stoi przed nim.
    konteksty = sąsiedztwa(tekst)
    podsumowanie = Podsumowanie.z_werdyktów(werdykty)
    return {
        "zdania": [
            _zdanie(verdict, sąsiedztwo)
            for verdict, sąsiedztwo in zip(werdykty, konteksty, strict=True)
        ],
        "podsumowanie": asdict(podsumowanie) | {"wyjaśnienie": podsumowanie.explain()},
    }


def makieta(ziarno: int | None, akapitów: int) -> dict[str, Any]:
    """Tekst do makiety wraz z ziarnem, którym wychodzi drugi raz.

    Ziarno wraca także wtedy, gdy przyszło, bo strona pokazuje je obok tekstu:
    bez tego tekst wylosowany raz nie da się zawołać drugi raz.
    """
    ziarno = random.randrange(10**6) if ziarno is None else ziarno
    akapitów = max(1, min(akapitów, NAJWIĘCEJ_AKAPITÓW))
    return {"ziarno": ziarno, "akapitów": akapitów, "tekst": losuj(ziarno, akapitów).kompiluj()}


def _zdanie(verdict: Verdict, sąsiedztwo: Sąsiedztwo) -> dict[str, Any]:
    """Jedno zdanie tak, jak je widzi strona: werdykt, czytania i to, co otwarte."""
    return {
        "zdanie": verdict.text,
        "status": verdict.status,
        "wyjaśnienie": verdict.explain(),
        #  Lista niesie streszczenia różne, a liczba czytań wychodzi z lasu, więc
        #  jedna z drugiej się nie wylicza. Że wyliczanie stanęło na
        #  ``MAX_READINGS`` (``olski/parse/las.py``), mówi osobne pole: po długości
        #  listy tego nie widać, bo skraca ją także samo powtórzenie napisu.
        "czytania": verdict.readings,
        "liczba_czytań": verdict.result.ile,
        "urwane": verdict.result.truncated,
        #  Konstytuenty, których wieloznaczność lista czytań zostawia
        #  nienazwaną, wraz ze streszczeniami ich kształtów.
        "rozbieżne": [
            {"konstytuent": rozbieżność.konstytuent, "czytania": list(rozbieżność.czytania)}
            for rozbieżność in verdict.rozbieżne
        ],
        "dalsze_zatrzymania": list(dalsze_zatrzymania(verdict)),
        #  Czym formy stoją w każdym odczytaniu, wpis na wpis z ``czytania``
        #  wyżej (``Verdict.morfologia`` w ``olski/werdykt.py``). Zdanie bez
        #  odczytania dostaje jeden wpis i mówi w nim, co olski w formach czyta,
        #  a rozstrzyga to werdykt, bo wydruk komendy pokazuje to samo.
        "morfologia": [
            [
                {"forma": wiersz.forma, "odczytania": list(wiersz.odczytania)}
                for wiersz in tabela
            ]
            for tabela in verdict.morfologia
        ],
        "domysły": _domysły(verdict, sąsiedztwo),
    }


def _domysły(verdict: Verdict, sąsiedztwo: Sąsiedztwo) -> list[dict[str, str]]:
    """Wskazania warstwy rozstrzygającej, po jednym na przyłączenie, albo żadne.

    Milczenie warstwy zostaje nienazwane, bo werdykt nad tym zdaniem nazwał już
    to przyłączenie i powiedział o nim to samo: że nierozstrzygnięte.
    """
    return [
        {
            "modyfikator": wskazanie.modyfikator,
            "gospodarz": wskazanie.gospodarz,
            "powód": wskazanie.powód,
            "świadek": wskazanie.świadek,
        }
        for wskazanie in rozstrzygnij(verdict.result.przyłączenia, _świadkowie(), sąsiedztwo)
        if isinstance(wskazanie, Rozstrzygnięcie)
    ]
