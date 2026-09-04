"""Powierzchnia: napis wraz z przecinkami, których konstytuent żąda od sąsiadów.

Kategorii ten moduł nie zna: konstytuent, który tędy przechodzi,
jest dla niego czymś, co umie się wypisać, i niczym więcej.
Pozycja dopisana do zdania nie dokłada więc tutaj gałęzi,
tylko tam, gdzie stoi kategoria, która ją niesie
(``olski/skład/składnia.py``).
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from olski.skład.kontekst import Kontekst


@dataclass(frozen=True)
class Kawałek:
    """Wypisany konstytuent wraz z przecinkami, których żąda od sąsiadów.

    Przecinek jest tu własnością kawałka, a nie znakiem w napisie,
    bo o tym, czy staje, rozstrzyga dopiero to, co obok niego stanie,
    a tego kawałek o sobie nie wie.
    Zdanie podrzędne żąda przecinka z obu stron i dostaje go z żadnej,
    gdy stoi samo; opis żąda go z jednej,
    bo przecinek otwierający stoi w środku samego opisu.
    Krawędź zdania przecinka nie stawia, i tyle wystarcza,
    żeby kropka nie stanęła po przecinku, a lista nie dostała dwóch.

    Bez tego pola przecinek jedzie wewnątrz napisu, a każde miejsce,
    które po konstytuencie coś stawia, musi o nim wiedzieć z ogona tego napisu.
    Miejsce dopisane bez tej wiedzy stawia drugi przecinek tuż za pierwszym,
    czyli wypuszcza tekst błędny i nigdzie nie zgłoszony.
    """

    napis: str
    przed: bool = False
    po: bool = False


def _rozdziela(lewy: Kawałek, prawy: Kawałek) -> str:
    """Czym stoją obok siebie dwa kawałki: przecinkiem, gdy któryś go żąda.

    Dość jednego żądania, bo polszczyzna stawia tu jeden przecinek, a nie dwa:
    zamknięcie zdania podrzędnego jest tym samym przecinkiem, co rozdzielenie listy.
    """
    return ", " if lewy.po or prawy.przed else " "


def sklej(kawałki: list[Kawałek]) -> Kawałek:
    """Kawałki jeden po drugim, wraz z żądaniami skrajnych, bo te zostają niespełnione.

    Przecinek wewnętrzny staje tutaj, a zewnętrzny czeka na to,
    co stanie obok całości, więc kawałek sklejony żąda tego samego,
    co żądały jego krańce.
    """
    napis, poprzedni = kawałki[0].napis, kawałki[0]
    for kawałek in kawałki[1:]:
        napis += _rozdziela(poprzedni, kawałek) + kawałek.napis
        poprzedni = kawałek
    return Kawałek(napis, przed=kawałki[0].przed, po=kawałki[-1].po)


def podrzędne(słowo: str, zdanie, kontekst: Kontekst) -> Kawałek:
    """Zdanie podrzędne wraz ze słowem, które je wprowadza, i przecinkami z obu stron.

    Stoi w jednym miejscu, bo zdanie podrzędne oddziela się przecinkiem z każdej
    strony, przy której coś stoi, i nie zależy to od tego, czym to zdanie jest
    w zdaniu nadrzędnym: okoliczność wyrażona zdarzeniem i treść czyjejś wiedzy
    piszą się tu identycznie i różnią się tylko słowem oraz pozycją.
    Żądanie idzie z obu stron, a krańce zdania go nie spełniają.

    Co zdanie podrzędne z tego kontekstu dziedziczy, a czego nie,
    rozstrzyga ``Kontekst.podrzędne`` i rozstrzyga to samo dla każdego z nich.
    """
    return replace(
        sklej([Kawałek(słowo), zdanie.linearyzuj(kontekst.podrzędne())]), przed=True, po=True
    )


def lista(człony: list[Kawałek]) -> Kawałek:
    """Człony przecinkami, a przed ostatnim spójnik: polska interpunkcja listy.

    Stoi ona w jednym miejscu, bo koordynacja bytów i ciąg zdarzeń
    dzielą ją co do znaku, choć łączą rzeczy różnego rodzaju.
    Przecinka żąda każdy człon od swojego poprzednika,
    więc człon, który zażądał go sam, nie dostaje drugiego.
    """
    początek = sklej([człony[0], *(replace(człon, przed=True) for człon in człony[1:-1])])
    return sklej([początek, Kawałek("i"), człony[-1]])
