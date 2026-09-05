"""Werdykt o zdaniu: zgłoszenie wraz z tym, co autor ma przeczytać.

Werdykt mówi o zdaniu więcej niż to, do której klasy je liczy,
bo autor ma na niego zareagować.
Zdanie o dwóch odczytaniach dostaje wiersz z tymi odczytaniami,
a :meth:`Verdict.explain` pokazuje, gdzie one się rozchodzą;
znaleziskiem, czyli tym, co autor ma poprawić, jest zdanie,
które od odczytania dzieli jeden znak (:class:`Naprawa`),
a wieloznaczność nim nie jest
(docs/subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem);
zdanie odrzucone dostaje miejsce, na którym rozbiór stanął,
a :func:`zatrzymania` każde takie miejsce, bo pierwsze zasłania następne.
Skąd te odczytania się biorą, mówi ``Verdict.morfologia``:
rozchodzą się w rolach, a zaczynają w lemacie i znaczniku formy.

Kto pyta o cały tekst, dostaje :func:`nad_tekstem` i :class:`Podsumowanie`,
czyli tyle wpisów (:class:`Zdanie`), ile zdań,
oraz jedną odpowiedź policzoną z nich regułą.
Wpis niesie obok werdyktu to, czego z jednego zdania nie widać:
zdania stojące przed nim w akapicie i zaimek wskazujący na dwie rzeczy naraz.

Warstwa ta ani nie wnosi wieloznaczności, ani jej nie zdejmuje,
bo jest wypowiedzią o warstwach pod nią (docs/architecture.md).
Gramatykę czyta gotową z ``olski/subset/``,
a segmentację, po której werdykt pada, z ``olski/segmentacja.py``.

Podział na moduły jest tu decyzją i idzie za tym, o co dany moduł pyta.
``olski.werdykt.wykazy`` liczy z lasu wykaz wypisywany pod każdym odczytaniem,
``olski.werdykt.odrzucone`` płaci rozbiorem drugim za dwie odpowiedzi
o napisie, którego gramatyka nie wyprowadza,
``olski.werdykt.zdanie`` składa z tego werdykt o jednym zdaniu,
a ``olski.werdykt.tekst`` pyta o cały tekst.
Import idzie tędy w jedną stronę i żaden z tych czterech nie zawraca:
``wykazy`` i ``odrzucone`` nie wiedzą o ``zdaniu``,
a ``zdanie`` nie wie o ``tekście``.
Podkreślenie w nazwie znaczy tu prywatne dla pakietu, a nie dla modułu:
poza niego wychodzą same nazwy wyliczone w ``__all__``.
"""

from __future__ import annotations

from olski.werdykt.odrzucone import Naprawa, zatrzymania
from olski.werdykt.tekst import (
    ODNIESIENIE,
    ODNIESIENIE_W_ZDANIU,
    POPRAWKA,
    WIELOZNACZNE,
    ZGŁOSZENIA,
    ZNALEZISKA,
    Podsumowanie,
    Zdanie,
    check,
    nad_tekstem,
)
from olski.werdykt.wykazy import OdczytaniaFormy, Żądanie
from olski.werdykt.zdanie import (
    FRAGMENT,
    NIEDOMKNIĘTE,
    Verdict,
    dalsze_zatrzymania,
    niespełnione_żądania,
    werdykt,
)

__all__ = [
    "check",
    "dalsze_zatrzymania",
    "FRAGMENT",
    "nad_tekstem",
    "Naprawa",
    "NIEDOMKNIĘTE",
    "niespełnione_żądania",
    "ODNIESIENIE",
    "ODNIESIENIE_W_ZDANIU",
    "OdczytaniaFormy",
    "Podsumowanie",
    "POPRAWKA",
    "Verdict",
    "werdykt",
    "WIELOZNACZNE",
    "zatrzymania",
    "Zdanie",
    "ZGŁOSZENIA",
    "ZNALEZISKA",
    "Żądanie",
]
