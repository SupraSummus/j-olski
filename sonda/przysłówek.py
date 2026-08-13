"""Co kupuje i co kosztuje przysłówek, zmierzone przed dopisaniem go do gramatyki.

Kolejka blokerów prowadzi do przysłówka dwoma wierszami z rzędu: ``adv`` stoi w
niej druga z 1992 zdaniami, a nad prozą tego repozytorium przysłówek stoi zaraz za
dwukropkiem (``docs/corpus.md``). Gramatyka nie ma go wcale, więc
``docs/roadmap.md`` stawia go pierwszym na liście etapu 6.

Trudność nie leży w produkcjach, bo tych jest jedenaście. Leży w tym, że
przysłówek ma w polszczyźnie więcej niż jednego gospodarza i staje przy każdym z
nich w tym samym miejscu napisu: ``Plik jest bardzo duży`` czyta się z ``bardzo``
przy ``duży`` i z ``bardzo`` przy całym zdaniu, a olski odrzuca zdanie, które
wychodzi dwoma czytaniami. Jednoznaczność jest własnością, którą przysłówek atakuje
wprost, i dlatego wycena idzie przed dopisaniem, a nie po nim.

Grupy są dwie i każda jest jednym gospodarzem. ``okolicznik`` stawia przysłówek
tam, gdzie stoi okolicznik zdania, czyli w liście, którą czasownik bierze przy
sobie, i przed zdaniem, bo szyk z okolicznikiem na czele wypisany jest tylko dla
wyrażenia przyimkowego. ``przy przymiotniku`` stawia go przed przymiotnikiem — i
przydawką, i orzecznikiem — a pozycje liczy z gramatyki, a nie z listy obok niej.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.przysłówek Składnica-frazowa-180723/
    python3 -m sonda.przysłówek proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import replace

from olski.grammar import Grammar, Głowa, Part, Production, Word, nt, word
from sonda import ruch

#: Terminal przysłówka: cała część mowy i nic więcej. Stopnia nie żąda, bo
#: `Teraz` stopnia nie niesie, a `bardzo` niesie `pos`, i oba są przysłówkami tej
#: samej gramatyki.
PRZYSŁÓWEK = word("adv")

#: Części mowy, przed którymi przysłówek staje jako określenie przymiotnika. Te
#: same, które olski bierze za orzecznikowe, bo imiesłów bierny jest tam
#: przymiotnikiem i tu jest nim tak samo: `nieporównanie tańsze` i `znacznie
#: rozszerzony`.
PRZYMIOTNIKOWE = frozenset({"adj", "ppas"})

OKOLICZNIK = "okolicznik"
PRZY_PRZYMIOTNIKU = "przy przymiotniku"


def _przymiotnikowy(część: Part) -> bool:
    """Czy ta część ciała jest tym przymiotnikiem, który przysłówek określa.

    Terminal wyliczający swoje lematy nie jest: zaimek względny ma znacznik
    przymiotnika i jest nazwany lematem, a `bardzo który` polszczyzną nie jest.
    Warunek stoi więc na tym, że klasa jest otwarta, a nie na wypisanej obok
    liście symboli, których ta sonda ma nie ruszać.
    """
    return (
        isinstance(część, Word)
        and bool(część.pos & PRZYMIOTNIKOWE)
        and część.lemmas is None
    )


def _przed_przymiotnikiem(produkcja: Production) -> list[Production]:
    """Kopie tej produkcji z przysłówkiem wstawionym przed każdym przymiotnikiem.

    Pozycje wychodzą z produkcji, a nie z listy wypisanej obok: ciało dopisane
    kiedyś do grupy imiennej albo przymiotnikowej dostanie tę pozycję samo, gdzie
    lista postarzałaby się bez śladu — sonda mierzyłaby wariant węższy, niż o
    sobie mówi, i nie powiedziałaby o tym ani słowem.

    Głowa przesuwa się razem ze swoją częścią, bo jest numerem pozycji w ciele:
    bez tego określenie orzecznika nazywałoby gospodarzem przyłączenia przysłówek.
    """
    kopie = []
    for gdzie, część in enumerate(produkcja.body):
        if not _przymiotnikowy(część):
            continue
        ciało = (*produkcja.body[:gdzie], PRZYSŁÓWEK, *produkcja.body[gdzie:])
        głowa = produkcja.głowa + (1 if produkcja.głowa >= gdzie else 0)
        kopie.append(replace(produkcja, body=ciało, głowa=głowa))
    return kopie


def dopisz(grammar: Grammar) -> None:
    """Dopisz do gramatyki przysłówek u obu gospodarzy naraz.

    Okolicznik dochodzi trzema produkcjami. Dwie wpuszczają przysłówek do listy
    okoliczników, czyli tam, gdzie dochodzi wyrażenie przyimkowe, i przez tę listę
    dostaje on każdą pozycję, jaką okolicznik w zdaniu ma. Trzecia stawia go na
    czele zdania, bo czoło zdania jest w gramatyce osobnym ciałem i bierze tam samo
    wyrażenie przyimkowe. Ciało `Adjuncts` w tym miejscu dałoby wyrażeniu
    przyimkowemu drugie wyprowadzenie tego samego kształtu, więc przysłówek dostaje
    tam ciało wypisane, tak samo jak ono.

    Określenie przymiotnika liczy się z produkcji olskiego, wziętych przed
    dopiskiem: pozycję ma dostać przymiotnik gramatyki, a nie przymiotnik, który
    trafiłby kiedyś do produkcji dopisanej tutaj.
    """
    olskiego = list(grammar.productions)
    grammar.rule("Adjuncts", [PRZYSŁÓWEK])
    grammar.rule("Adjuncts", [Głowa(PRZYSŁÓWEK), nt("Adjuncts")])
    grammar.rule("ClauseConjunct", [PRZYSŁÓWEK, Głowa(nt("ClauseConjunct"))])
    for produkcja in olskiego:
        for kopia in _przed_przymiotnikiem(produkcja):
            grammar.dopisz(kopia)


def gospodarz(produkcja: Production) -> str | None:
    """Przy którym gospodarzu stawia przysłówek ta produkcja; ``None``, gdy żadnym.

    Pytanie stawiane produkcji, a nie liście nazw obok gramatyki, bo ta sama
    funkcja odsiewa produkcje olskiego, których przysłówka nie ma ani jedna.
    Odpowiada terminal, a nie symbol: określenie przymiotnika buduje `NPConjunct`
    i `APConjunct`, czyli te same symbole, które buduje każda grupa imienna i
    przymiotnikowa bez przysłówka.

    Terminal jest przy tym tym jednym, który :data:`PRZYSŁÓWEK` nazywa, a nie
    dowolnym o znaczniku `adv`: drugi terminal — na przykład zawężony do stopnia —
    wypadłby stąd bez grupy i zostałby w mianowniku, a `tests/test_ruch.py` mówi o
    tym wprost, bo dopisek bez grupy każe sondzie mierzyć zero.
    """
    if PRZYSŁÓWEK not in produkcja.body:
        return None
    if any(_przymiotnikowy(część) for część in produkcja.body):
        return PRZY_PRZYMIOTNIKU
    return OKOLICZNIK


SONDA = ruch.Sonda(
    prog="python3 -m sonda.przysłówek",
    opis="Ile przysłówek kupuje i ile kosztuje.",
    warianty=("bez przysłówka", OKOLICZNIK, PRZY_PRZYMIOTNIKU, "oba"),
    grupa=gospodarz,
    pytania=(
        "obaj gospodarze ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
    dopisuje=dopisz,
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
