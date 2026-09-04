"""Parsing: every reading, not the first one.

The parser answers these questions:

1. Does this sentence have a derivation at all? If not, it is not olski, and the
   furthest point reached says where the analysis died.
2. If it has exactly one, that is the reading.
3. If it has more than one, the readings and the summaries beside them
   say what the sentence leaves open.
   Why that is a finding for the author and not a rejection
   is docs/subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego.

Distinct readings, not derivations. Two derivations that describe the same
structure are one reading. The distinction is not pedantic: it is the
mistake recorded in docs/glr-in-practice.md#ambiguity-as-a-confidence-measure,
where a system fell silent on lines it had understood perfectly because it
counted attempts instead of outcomes.

Implementation.
An Earley chart over the segmentation graph builds a forest with shared nodes:
one :class:`Pozycja` per constituent shape,
however many derivations stand under it,
so six undecided attachments are six positions rather than sixty-four trees.
The summaries come off that forest, one method each,
and none of them needs another parser.
docs/parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań
owns the argument for asking the forest rather than a list of trees,
and docs/parsowanie.md#co-się-pakuje-rozstrzyga-tożsamość-czytania
owns the two conditions such a forest has to meet
and the measurement behind the second.

Podział na moduły jest tu decyzją i idzie za tym, czym każdy kawałek jest.
``olski.parse.czytanie`` definiuje typy, którymi rozbiór mówi o kształcie:
pozycję, liść i węzeł.
``olski.parse.podsumowanie`` definiuje typy, którymi rozbiór rozmawia z werdyktem:
deklarację, którą dostaje od gramatyki, i wynik, który oddaje.
``olski.parse.tablica`` rozbiera zdanie tablicą Earleya,
``olski.parse.las`` odpowiada na pytania o las, który z tej tablicy wychodzi,
``olski.parse.decyzje`` liczy z tego lasu decyzje, których czytania nie rozstrzygają,
a ``olski.parse.streszczenie`` składa napis, którym werdykt nazywa jedno czytanie.
Nazwa z podkreśleniem przechodzi tu przez granicę modułu,
bo znaczy prywatne dla pakietu, a nie dla modułu:
poza pakiet wychodzą same nazwy wyliczone w ``__all__``.

Rozcięcie między lasem a decyzjami idzie po stronie czytającej:
:class:`Decyzje` do stanu lasu nie pisze i do jego pamięci podręcznych nie sięga.
Ceną jest granica modułu, przez którą przechodzi cały odczyt lasu.
Kupuje to jedną deklarację w konstruktorze zamiast w kluczu każdej pamięci podręcznej,
którą te trzy podsumowania trzymają.

Wyliczanie drzew zostaje przy lesie:
przeplata się z jego krawędziami klasa po klasie i pisze do jego pamięci podręcznych,
więc rozcięcie dałoby tam drugi moduł sięgający do wnętrza pierwszego.

Funkcje wejściowe składają tablicę, las i podsumowania w jedną odpowiedź,
więc są tutaj, i jest to jedyne miejsce, które je składa.
"""

from __future__ import annotations

from olski.grammar import Grammar
from olski.morph import Segment
from olski.parse.czytanie import Cykl, Leaf, Node, Pozycja, Tree
from olski.parse.decyzje import Decyzje
from olski.parse.las import MAX_READINGS, Las
from olski.parse.podsumowanie import Deklaracja, Obsada, Przyłączenie, Result, Rozbieżność
from olski.parse.streszczenie import (
    OBOK,
    PRZYŁĄCZONY_DO,
    ciało_koordynuje,
    describe,
    liście,
    sklej_formy,
    streszczenia,
    streszczone,
    w_zakresie,
    zakresy,
)
from olski.parse.tablica import _Tablica


def las(grammar: Grammar, segments: list[Segment], start: str | None = None) -> Las:
    """Las tego zdania, do chodzenia po nim.

    Wywołuje ją pomiar, bo pyta las o więcej, niż werdykt z niego bierze:
    obok :func:`podsumuj` pyta jeszcze, którym z kolei czytaniem jest w tym lesie złote
    (:meth:`Las.numer_czytania`).
    Sam werdykt woła :func:`parse`, która las porzuca,
    bo dokument trzyma tyle werdyktów, ile ma zdań,
    a jeden las waży tyle, ile jego tablica.
    """
    return Las(_Tablica(grammar, segments, start or grammar.start))


def parse(
    grammar: Grammar,
    segments: list[Segment],
    start: str | None = None,
    deklaracja: Deklaracja | None = None,
    zatrzymanie: bool = True,
) -> Result:
    """Rozbierz zdanie i zapytaj las, ile czytań ma, które pokazać i co zostawia otwarte."""
    return podsumuj(las(grammar, segments, start), deklaracja, zatrzymanie=zatrzymanie)


def podsumuj(
    zbudowany: Las, deklaracja: Deklaracja | None = None, zatrzymanie: bool = True
) -> Result:
    """Podsumowania, jakie werdykt bierze z gotowego lasu.

    Osobno od :func:`parse`, bo pomiar buduje las sam i pyta go jeszcze o coś,
    czego werdykt nie niesie; bez tego rozbierałby zdanie drugi raz.

    Bez deklaracji werdykt jest samą liczbą i listą czytań;
    co ona niesie i czemu jest jedna, mówi :class:`Deklaracja`.

    O to, dokąd analiza doszła, pyta się na żądanie,
    bo nad zdaniem odrzuconym jest to najdroższe z podsumowań, jakie ta funkcja bierze:
    :meth:`Las.najdalszy` przechodzi wtedy tablicę drugi raz, i to drożej,
    niż kosztowało samo jej zbudowanie: przejście drugie unifikuje przebyte ciała,
    czego budowanie nie robi wcale.
    Nad zdaniem, które ma czytanie, oddaje koniec zdania bez przejścia.
    Czyta tę odpowiedź odrzucenie mówiące, gdzie stanęło
    (``explain`` w ``olski/werdykt.py``) oraz ranking blokerów (``olski/pokrycie.py``);
    przebieg, który liczy same werdykty, nie czyta jej wcale.
    Kto nie pyta, dostaje w ``Result.furthest`` stan „nikt nie pytał”.

    Warunku na samo zdanie tutaj nie ma, bo zmierzony nic nie kupił.
    Werdykt nad zdaniem, którego forma nie ma licencji, nazywa tę formę
    i zatrzymania nie czyta, a takich zdań jest większość odrzuconych,
    tyle że każde umiera wcześnie i jego tablica jest mała.
    Cena rośnie w zdaniach, które dochodzą daleko i nie domykają się,
    a tych warunek na licencję nie dotyka.
    """
    ile = zbudowany.ile_czytań()
    readings: list[Node] = []
    for tree in zbudowany.czytania():
        readings.append(tree)
        if len(readings) >= MAX_READINGS:
            break
    różniące: tuple[str, ...] = ()
    przyłączenia: tuple[Przyłączenie, ...] = ()
    rozbieżności: tuple[Rozbieżność, ...] = ()
    if deklaracja is not None:
        decyzje = Decyzje(zbudowany, deklaracja)
        różniące = decyzje.różniące()
        przyłączenia = tuple(decyzje.przyłączenia())
        rozbieżności = tuple(decyzje.rozbieżności())
    return Result(
        ile,
        readings,
        zbudowany.najdalszy() if zatrzymanie else None,
        truncated=ile > len(readings),
        różniące=różniące,
        przyłączenia=przyłączenia,
        rozbieżności=rozbieżności,
    )


__all__ = [
    "ciało_koordynuje",
    "Cykl",
    "Deklaracja",
    "describe",
    "Las",
    "las",
    "Leaf",
    "liście",
    "MAX_READINGS",
    "Node",
    "Obsada",
    "OBOK",
    "parse",
    "podsumuj",
    "Pozycja",
    "Przyłączenie",
    "PRZYŁĄCZONY_DO",
    "Result",
    "Rozbieżność",
    "sklej_formy",
    "streszczenia",
    "streszczone",
    "Tree",
    "w_zakresie",
    "zakresy",
]
