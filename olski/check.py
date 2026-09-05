"""Sprawdzenie tekstu wobec gramatyki, z wiersza poleceń.

Komenda bierze plik, który autor napisał, i prozę wyjmuje z niego sama
(:func:`olski.wejście.proza`), więc dokumentu nikt nie przepisuje wcześniej na
zwykły tekst.

Wydruk zgłasza znaleziska i milczy o zdaniu, o którym nie ma nic do powiedzenia
(:func:`_wiersze`), a ile tego milczenia było, mówi ostatni wiersz przebiegu
(:class:`olski.werdykt.Podsumowanie`).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from typing import TypeVar

from olski.cennik import cena
from olski.chwyty import chwyty
from olski.imiesłowy import Imiesłów
from olski.odniesienia import Niezwrotny, Odniesienie
from olski.rozstrzyganie import Rozstrzygnięcie, domyślni, rozstrzygnij
from olski.wejście import proza
from olski.werdykt import (
    OdczytaniaFormy,
    Podsumowanie,
    Verdict,
    Zdanie,
    Żądanie,
    dalsze_zatrzymania,
    nad_tekstem,
    niespełnione_żądania,
)
from olski.żądania import NIENAZWANE

#: Wpis wykazu drukowanego na odczytanie (:func:`_wykaz`).
T = TypeVar("T")

#: Znak, którym wiersz morfologii oddziela dwa odczytania jednej formy.
#: Przecinka tu nie ma, bo przecinek jest formą i ma w tym wykazie własny
#: wiersz, a średnikiem rozdziela werdykt własne człony.
MIĘDZY_ODCZYTANIAMI = " | "

#: Słowo, którym wiersz żądania oddziela dwie klasy. Przecinka tu nie ma, bo
#: klasy stoją w alternatywie: czasownik żąda jednej z nich, a nie obu naraz.
ALBO = " albo "

#: Napis, którym wiersz żądania nazywa klasę, której plik żądań nie nazywa
#: (:data:`olski.żądania.NIENAZWANE`). Stoi w alternatywie obok klas nazwanych,
#: bo przemilczana czytałaby się jak żądanie ostrzejsze, niż Walenty stawia.
KLASA_NIENAZWANA = "klasy, której olski nie nazywa"

#: Znak przed wierszem o chwycie rejestru. Werdyktem ten wiersz nie jest tak
#: samo jak :data:`DOMYSŁ`, a z innego powodu: werdykt mówi o polszczyźnie
#: zdania, a chwyt o rejestrze, w którym je napisano (``olski/chwyty.py``).
CHWYT = "~"

#: Znak przed wierszem warstwy rozstrzygającej. Wiersz ten nie jest werdyktem
#: i nie może się na werdykt czytać, bo werdykt mówi, co olski o zdaniu wie,
#: a ten wiersz, co osobna warstwa o nim zgaduje (``olski/rozstrzyganie.py``).
DOMYSŁ = "?"


def _rozstrzygnięcia(verdict, świadkowie, sąsiedztwo) -> list[str]:
    """Wiersze warstwy rozstrzygającej, po jednym na przyłączenie, albo żaden.

    Milczenie warstwy zostaje nienazwane, bo werdykt nad tym zdaniem nazwał już
    to przyłączenie i powiedział o nim to samo: że nierozstrzygnięte.
    """
    return [
        f"{DOMYSŁ} „{o.modyfikator}” → „{o.gospodarz}”: {o.powód}"
        for o in rozstrzygnij(verdict.result.przyłączenia, świadkowie, sąsiedztwo)
        if isinstance(o, Rozstrzygnięcie)
    ]


def _role(streszczenie: dict[str, str]) -> str:
    return ", ".join(f"{rola}: {wypełnienie}" for rola, wypełnienie in streszczenie.items())


def czytanie(streszczenie: tuple[dict[str, str], ...], wcięcie: str = "") -> Iterator[str]:
    """Wiersze jednego czytania: po jednym na zdanie składowe.

    Kreska otwiera czytanie, a składowe następne stoją pod nim bez niej,
    bo lista liczy czytania: kreska przy każdym składowym mówiłaby,
    że zdanie o dwóch składowych i jednym czytaniu ma czytania dwa.

    Publiczna, bo czytanie pierwsze wypisuje obok tej komendy sonda cen
    (``harness/cena.py``), a dwa wydruki jednego czytania nie dałyby się porównać.
    """
    for numer, składowe in enumerate(streszczenie):
        yield f"{wcięcie}- {_role(składowe)}" if numer == 0 else f"{wcięcie}  {_role(składowe)}"


def _czytania(verdict: Verdict) -> Iterator[str]:
    """Wiersze, którymi ``--readings`` mówi, co stoi w której roli.

    Za streszczeniami zdania idą streszczenia konstytuentu, którego
    wieloznaczność streszczenie zdania zostawia nienazwaną
    (``Verdict.rozbieżne`` w ``olski/werdykt/zdanie.py``).
    """
    for streszczenie in verdict.readings:
        yield from czytanie(streszczenie)
    for rozbieżność in verdict.rozbieżne:
        yield f"„{rozbieżność.konstytuent}” czyta się tak:"
        for streszczenie in rozbieżność.czytania:
            yield from czytanie(streszczenie, "  ")


def _wiersz_formy(wiersz: OdczytaniaFormy, wcięcie: str) -> str:
    return f"{wcięcie}„{wiersz.forma}”: {MIĘDZY_ODCZYTANIAMI.join(wiersz.odczytania)}"


def _wiersz_żądania(wiersz: Żądanie, wcięcie: str) -> str:
    """Żądanie jednej pozycji jako wiersz wydruku.

    Rola i wypełnienie otwierają wiersz tak, jak je nazywa streszczenie, bo obok
    niego się go czyta; cudzysłów jest treścią, bo wypełnienie jest ciągiem
    wziętym ze zdania i samo zawiera odstępy.
    """
    klasy = ALBO.join(
        KLASA_NIENAZWANA if klasa in NIENAZWANE else klasa for klasa in wiersz.klasy
    )
    return f"{wcięcie}{wiersz.rola} „{wiersz.wypełnienie}”: „{wiersz.czasownik}” żąda klasy {klasy}"


def _wiersz_pozycji(wpis: tuple[str, int], wcięcie: str) -> str:
    """Jedna pozycja rachunku: za co to odczytanie płaci, ile razy i ile to razem.

    Liczba stoi przy każdej, bo pozycje kosztują różnie i to o nią w tym wydruku
    chodzi (``olski/cennik.py``).
    """
    nazwa, ile = wpis
    razy = f" ×{ile}" if ile > 1 else ""
    return f"{wcięcie}{nazwa}{razy}: {cena(nazwa) * ile}"


def _wiersz_osoby(wiersz: Żądanie) -> str:
    """Żądanie osoby, którego wypełnienie nie spełnia, jako wiersz wydruku.

    Wiersz nazywa klasę tak jak :func:`_wiersz_żądania`, bo bez niej nie da się
    go sprawdzić w Walentym, a kończy się lematem, bo deklaracja projektu jest
    o lemacie, a nie o formie stojącej w zdaniu (``olski/osoby.py``).

    Klasy nienazwanej ten wiersz nie ma czym wypisać i nie ma po co:
    alternatywa z nią nie jest żądaniem osoby
    (:func:`olski.żądania.żąda_osoby`), więc tutaj taka klasa nie dochodzi.
    Lematy idą alfabetycznie, bo stoją w zbiorze
    (:func:`olski.werdykt.wykazy._zwinięte`), a wydruk kolejności ze zbioru nie bierze.
    """
    lematy = ALBO.join(f"„{lemat}”" for lemat in sorted(wiersz.lematy))
    return (
        f"{wiersz.rola} „{wiersz.wypełnienie}”: „{wiersz.czasownik}” żąda klasy "
        f"{ALBO.join(wiersz.klasy)}, a {lematy} nikogo nie nazywa"
    )


def _wiersz_imiesłowu(wiersz: Imiesłów) -> str:
    """Imiesłów i orzeczenie, które podmiotu nie ma, jako wiersz wydruku.

    Oba nazwane formą, bo autor odszuka je w zdaniu właśnie w tej formie, i oba
    w cudzysłowie z tego samego powodu, z którego dostaje go gospodarz
    przyłączenia (:func:`_nierozstrzygnięte` w ``olski/werdykt/zdanie.py``).
    """
    return f"„{wiersz.imiesłów}” określa „{wiersz.orzeczenie}”, które podmiotu nie ma"


def _wiersz_niezwrotnego(wiersz: Niezwrotny) -> str:
    """Zaimek dzierżawczy, rzecz i podmiot, którego on nie bierze, jako wiersz wydruku.

    Wiersz kończy się formą, którą autor napisałby o rzeczy podmiotu, bo to ona
    jest poprawką; rodzaju i przypadka wiersz jej nie odmienia, bo `swój` odmienia
    się za rzeczą, a nie za zaimkiem, którego on zastępuje.
    Formy w cudzysłowie z tego samego powodu co przy :func:`_wiersz_imiesłowu`.
    """
    return (
        f"„{wiersz.zaimek}” określa „{wiersz.rzecz}”, a o rzeczy podmiotu "
        f"„{wiersz.podmiot}” mówi się „swój”"
    )


def _wykaz(tabele: Sequence[Sequence[T]], wiersz: Callable[[T, str], str]) -> Iterator[str]:
    """Wykaz na odczytanie, numerowany tak, jak ``--readings`` numeruje odczytania.

    Każda flaga, która ten wykaz drukuje, bierze tę samą listę streszczeń
    (``Verdict.readings`` w ``olski/werdykt/zdanie.py``), więc numer znaczy w nich to
    samo, a wypisany osobno w każdej rozjechałby się po cichu.
    Numeru nie ma tam, gdzie wpis jest jeden: nie ma go od czego odróżnić,
    a nad zdaniem odrzuconym nie byłby numerem odczytania
    (``Verdict.morfologia`` mówi, co taki wpis niesie).
    Wpis pusty nie dostaje nawet numeru, bo nagłówek bez wierszy pod sobą
    zapowiada wykaz, którego nie ma.
    """
    numerowane = len(tabele) > 1
    for numer, tabela in enumerate(tabele, start=1):
        if not tabela:
            continue
        if numerowane:
            yield f"odczytanie {numer}:"
        for wpis in tabela:
            yield wiersz(wpis, "  " if numerowane else "")


def _dalsze(verdict: Verdict) -> Iterator[str]:
    """Wiersz o zatrzymaniach poza pierwszym, które nazwał już werdykt, albo żaden.

    Zdanie o jednym zatrzymaniu wiersza nie dostaje, bo flaga zrobiła nad nim
    to, co widać: wypisała zdanie, które bez niej byłoby przemilczane.
    Tak samo milczy o tym strona (``witryna/skrypt.js``).
    O zdanie odrzucone pyta samo :func:`olski.werdykt.dalsze_zatrzymania`,
    więc warunku na nie tutaj nie ma.
    """
    dalsze = dalsze_zatrzymania(verdict)
    if dalsze:
        formy = ", ".join(f"„{forma}”" for forma in dalsze)
        yield f"analiza staje też na {formy}"


def _odniesienia(zgłoszenia: Sequence[Odniesienie]) -> Iterator[str]:
    """Wiersze o zaimkach wskazujących na dwie rzeczy naraz, po jednym na zaimek.

    Wiersz nazywa rzeczy formami, w których stoją w zdaniu obok, bo tam autor je
    odszuka; czemu wypisane są wszystkie, a nie sama ich liczba, mówi
    ``olski/odniesienia.py``.
    """
    for zgłoszenie in zgłoszenia:
        rzeczy = ALBO.join(f"„{rzecz}”" for rzecz in zgłoszenie.rzeczy)
        yield f"„{zgłoszenie.zaimek}” wskazuje na {rzeczy}"


def _wiersze(zdanie: Zdanie, args: argparse.Namespace, świadkowie) -> Iterator[str]:
    """Co ten przebieg ma o tym zdaniu do powiedzenia, wiersz po wierszu.

    Zdanie bez ani jednego wiersza komenda przemilcza, zamiast meldować,
    że nie ma o nim nic do powiedzenia; ile było tego milczenia,
    mówi podsumowanie całości (:class:`olski.werdykt.Podsumowanie`).
    Flaga dokłada wiersze i tym samym dokłada zdania:
    kto pyta o zatrzymania, pyta o zdania, których olski nie czyta,
    a kto pyta o czytania, pyta o każde zdanie czytane.
    """
    verdict = zdanie.werdykt
    if verdict.zgłoszenie or (args.zatrzymania and not verdict.czytane):
        yield verdict.explain()
    #  Zaraz za werdyktem, bo jest zgłoszeniem tak samo jak on, a nie odpowiedzią
    #  warstwy obok (:func:`_rozstrzygnięcia`); flagi go nie chowają z tego samego
    #  powodu, dla którego nie chowają wieloznaczności.
    yield from _odniesienia(zdanie.odniesienia)
    if args.zatrzymania:
        yield from _dalsze(verdict)
    if args.readings:
        yield from _czytania(verdict)
    #  Rachunek zaraz za czytaniami, bo mówi o kolejności, w jakiej one stoją.
    if args.koszt:
        yield from _wykaz(verdict.rachunki, _wiersz_pozycji)
    #  Morfologię wypisujemy za czytaniami, bo jest tym, z czego wyszły.
    if args.morfologia:
        yield from _wykaz(verdict.morfologia, _wiersz_formy)
    #  Żądania za morfologią, bo mówią o pozycji, którą czytanie już obsadziło.
    if args.żądania:
        yield from _wykaz(verdict.żądania, _wiersz_żądania)
    #  Osoby za żądaniami, bo są tymi żądaniami, na które projekt odpowiedział.
    if args.osoby:
        yield from map(_wiersz_osoby, niespełnione_żądania(verdict))
    #  Imiesłowy za osobami, bo obie flagi pytają o zdanie, a nie o odczytanie,
    #  i obie o to, czego zdaniu brakuje: tam wykonawcy w pozycji, tu podmiotu.
    if args.imiesłowy:
        yield from map(_wiersz_imiesłowu, verdict.imiesłowy)
    #  Zaimki dzierżawcze za imiesłowami, bo pytają o to samo co warstwa zaimkowa
    #  nad werdyktem, a czekają za flagą tak jak imiesłów nad nimi.
    if args.dzierżawcze:
        yield from map(_wiersz_niezwrotnego, verdict.niezwrotne)
    if świadkowie is not None:
        yield from _rozstrzygnięcia(verdict, świadkowie, zdanie.sąsiedztwo)
    #  Chwyt na końcu, bo o polszczyźnie tego zdania nie mówi nic.
    if args.chwyty:
        yield from (
            f"{CHWYT} „{chwyt.forma}” {chwyt.naprawa}" for chwyt in chwyty(verdict.text)
        )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="olski-check",
        description="Sprawdź zdania polskiego tekstu: zgłoś znaleziska, "
        "wypisz odczytania zdań wieloznacznych, "
        "a o zdaniach, których olski nie czyta, milcz do flagi.",
    )
    parser.add_argument("paths", nargs="*", help="pliki polskiego tekstu albo dokumenty")
    parser.add_argument("-c", "--text", help="sprawdź ten tekst zamiast pliku")
    parser.add_argument(
        "--readings",
        action="store_true",
        help="pokaż, co stoi w której roli, raz na streszczenie odczytania",
    )
    parser.add_argument(
        "--koszt",
        action="store_true",
        help="pokaż, czym każde odczytanie jest nacechowane i ile to kosztuje",
    )
    parser.add_argument(
        "--rozstrzygaj",
        action="store_true",
        help="obok werdyktu pokaż, co osobna warstwa mówi o przyłączeniach",
    )
    parser.add_argument(
        "--morfologia",
        action="store_true",
        help="pokaż lemat i znacznik form, czyli czym stoją w odczytaniu",
    )
    parser.add_argument(
        "--żądania",
        action="store_true",
        help="pokaż, czego czasownik żąda od słowa stojącego w jego pozycji",
    )
    parser.add_argument(
        "--osoby",
        action="store_true",
        help="pokaż pozycje, w których czasownik żąda kogoś, a stoi w nich rzecz",
    )
    parser.add_argument(
        "--imiesłowy",
        action="store_true",
        help="pokaż imiesłowy przysłówkowe stojące przy orzeczeniu, które podmiotu nie ma",
    )
    parser.add_argument(
        "--dzierżawcze",
        action="store_true",
        help="pokaż zaimki dzierżawcze nazywające rzecz podmiotu, o której mówi się „swój”",
    )
    parser.add_argument(
        "--chwyty",
        action="store_true",
        help="pokaż chwyty rejestru, których w prozie tego repozytorium nie chcemy",
    )
    parser.add_argument(
        "--zatrzymania",
        action="store_true",
        help="pokaż zdania, których olski nie czyta, wraz z każdym miejscem, "
        "na którym staje analiza",
    )
    args = parser.parse_args(argv)

    if not args.paths and args.text is None:
        parser.print_usage(sys.stderr)
        return 2

    sources: list[tuple[str, str]] = []
    if args.text is not None:
        sources.append(("<text>", args.text))
    for raw in args.paths:
        path = Path(raw)
        try:
            sources.append((raw, proza(path)))
        except (OSError, UnicodeDecodeError) as error:
            print(f"olski-check: nie udało się przeczytać {raw}: {error}", file=sys.stderr)
            return 2

    #  Świadkowie powstają raz na przebieg, a nie raz na zdanie: tabela skłonności
    #  wchodzi z pliku, a dokument ma tyle zdań, ile ma.
    świadkowie = domyślni() if args.rozstrzygaj else None

    wszystkie: list[Zdanie] = []
    for name, text in sources:
        zdania = nad_tekstem(text)
        wszystkie += zdania
        for zdanie in zdania:
            wiersze = list(_wiersze(zdanie, args, świadkowie))
            if not wiersze:
                continue
            print(f"{name}: {zdanie.werdykt.text}")
            for wiersz in wiersze:
                print(f"{' ' * (len(name) + 2)}{wiersz}")

    podsumowanie = Podsumowanie.ze_zdań(wszystkie)
    print(podsumowanie.explain())
    #  Kod wyjścia niesie znaleziska, a nie milczenie ani wieloznaczność
    #  (docs/subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem).
    return 0 if podsumowanie.znalezisk == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
