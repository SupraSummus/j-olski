"""Ile pozycja cennika rusza czytanie pierwsze, liczone nad prozą.

Cena porządkuje czytania i werdyktu nie rusza: czytań jest tyle samo i mówią to
samo (``olski/cennik.py``). Sonda różnicowa z ``harness/ruch.py`` jej przez to
nie zmierzy, bo porównuje werdykty, a każdy wariant wydaje tu te same.
Mierzalna jest sama kolejność, a mierzy się ją czytaniem pierwszym każdego
zdania, bo to ono stoi u góry wydruku.

Pozycji morfologii ta sonda nie wycenia: cenę czytania formy czyta
``olski/rejestr.py`` w czasie rozbioru, a nie produkcja, więc nie ma jej skąd
zdjąć (:func:`pozycje_produkcji`).

Kierunku wydruk nie podaje, bo proza drzewa wzorcowego nie niesie, więc zdanie
przestawione czyta się ręką. Co z tego wyszło i co przy tym zmierzono,
trzyma docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie.

    python3 -m harness.cena
    python3 -m harness.cena --pozycja okolicznik CLAUDE.md
"""

from __future__ import annotations

import argparse
import collections
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field, replace
from pathlib import Path

from harness import proza_repozytorium
from olski.cennik import CENNIK
from olski.check import czytanie
from olski.grammar import Grammar
from olski.segmentacja import morphology, sentences
from olski.subset import GRAMMAR, build
from olski.wejście import proza
from olski.werdykt import werdykt

#: Streszczenie jednego czytania: wpis na każde zdanie składowe, tak jak wydaje
#: je ``Verdict.readings`` w ``olski/werdykt.py``.
Czytanie = tuple[dict[str, str], ...]

#: Ile zdań pokazać pod każdą pozycją. Pozycja bez przykładu jest liczbą, o
#: której nie wiadomo, co ruszyła, a kierunku ten wydruk nie podaje, więc
#: przykład jest tu jedyną drogą do odpowiedzi, czy ruszyła w dobrą stronę.
PRZYKŁADY = 8


def pozycje_produkcji() -> tuple[str, ...]:
    """Pozycje cennika, którymi płaci choć jedna produkcja, w kolejności cennika.

    Pytamy gramatyki, a nie listy wypisanej obok cennika: pozycja dopisana do
    produkcji zgłasza się tu sama, a lista milczałaby o niej
    (``CLAUDE.md#code``). Pozycja, której nie płaci ani jedna produkcja, jest
    pozycją morfologii i tej sondy nie dotyczy (``olski/rejestr.py``).
    """
    płacone = {nazwa for produkcja in GRAMMAR.productions for nazwa in produkcja.koszty}
    return tuple(nazwa for nazwa in CENNIK if nazwa in płacone)


def bez_pozycji(pozycja: str) -> Grammar:
    """Gramatyka olskiego z tą pozycją zdjętą z rachunku każdej produkcji.

    Produkcje przepisane, a nie złożone drugi raz z części, bo składanie gubi
    głowę (``Grammar.dopisz``); tak samo składa wariant ``Zdejmowanie``
    w ``harness/ruch.py``, a różni je to, że tam produkcja wypada, a tu zostaje
    tańsza.
    """
    pełna = build()
    tańsza = Grammar(start=pełna.start)
    for produkcja in pełna.productions:
        rachunek = tuple(nazwa for nazwa in produkcja.koszty if nazwa != pozycja)
        tańsza.dopisz(replace(produkcja, koszty=rachunek))
    return tańsza


@dataclass
class Raport:
    """Liczniki jednego przebiegu wraz ze zdaniami, na których widać ruch."""

    pozycje: tuple[str, ...]
    ile_przykładów: int = PRZYKŁADY
    #: Zdania, o których werdykt orzeka; fragmentu nie ma tu ani w liczniku.
    zdań: int = 0
    #: Zdania o kilku czytaniach, czyli mianownik: pod zdaniem o jednym czytaniu
    #: cena nie ma czego przestawić.
    wieloznaczne: int = 0
    #: Pozycja → ile zdań ma pod wariantem inne czytanie pierwsze niż pod olskim.
    ruszone: collections.Counter = field(default_factory=collections.Counter)
    #: Pozycja → ile zdań zmieniło pod wariantem liczbę czytań, czyli ile razy
    #: cena zrobiła coś poza kolejnością.
    rozjechane: collections.Counter = field(default_factory=collections.Counter)
    #: Pozycja → zdania wraz z oboma czytaniami pierwszymi, olskiego i wariantu.
    przykłady: dict[str, list[tuple[str, Czytanie, Czytanie]]] = field(default_factory=dict)

    def zapisz(
        self, pozycja: str, zdanie: str, u_olskiego: Czytanie, w_wariancie: Czytanie
    ) -> None:
        self.ruszone[pozycja] += 1
        zachowane = self.przykłady.setdefault(pozycja, [])
        if len(zachowane) < self.ile_przykładów:
            zachowane.append((zdanie, u_olskiego, w_wariancie))


def zmierz(
    warianty: dict[str, Grammar],
    teksty: Iterable[str],
    przykłady: int = PRZYKŁADY,
) -> Raport:
    """Przepuść zdania tych tekstów przez każdy wariant i policz, co się przestawia.

    Mianownikiem jest olski, a wariant przychodzi gotową gramatyką, więc ta sama
    funkcja mierzy wariant tańszy i wariant droższy: sesja wyceniająca pozycję,
    której olski jeszcze nie ma, dopisuje ją do produkcji i woła to samo.
    Pozycje raportu biorą się z samych wariantów, więc tabela nie wypisze pozycji,
    której nikt nie zmierzył.

    Zdanie idzie przez warianty, a nie wariant przez cały tekst, bo segmenty
    zależą od napisu, a nie od gramatyki, i tak samo idzie ``nad_prozą``
    w ``harness/ruch.py``.
    Wariantów nie pyta się o zdanie o jednym czytaniu ani o zdanie odrzucone:
    kolejność jednego czytania jest ta sama pod każdą ceną, więc rozbiór pod
    wariantem odpowiadałby na pytanie, którego nikt nie zadał.
    """
    raport = Raport(tuple(warianty), przykłady)
    for napis in (napis for tekst in teksty for napis in sentences(tekst)):
        segmenty = morphology(napis)
        baza = werdykt(napis, segmenty, GRAMMAR, zatrzymanie=False)
        if not baza.punktowane:
            continue
        raport.zdań += 1
        if baza.result.ile < 2:
            continue
        raport.wieloznaczne += 1
        for pozycja, gramatyka in warianty.items():
            wariant = werdykt(napis, segmenty, gramatyka, zatrzymanie=False)
            if wariant.result.ile != baza.result.ile:
                raport.rozjechane[pozycja] += 1
            elif wariant.readings[0] != baza.readings[0]:
                raport.zapisz(pozycja, baza.text, baza.readings[0], wariant.readings[0])
    return raport


def przebieg(
    ścieżki: Sequence[Path],
    pozycje: Iterable[str],
    przykłady: int = PRZYKŁADY,
) -> Raport:
    """Zmierz każdą z tych pozycji nad prozą tych plików.

    Warianty składają się raz na przebieg, a nie raz na plik: budowa gramatyki
    jest droższa od rozbioru jednego zdania, a gramatyka po zbudowaniu się nie
    zmienia.
    """
    warianty = {pozycja: bez_pozycji(pozycja) for pozycja in pozycje}
    return zmierz(warianty, (proza(ścieżka) for ścieżka in ścieżki), przykłady)


def wydruk(raport: Raport, nagłówek: str) -> str:
    """Tabela ruchu, a pod nią zdania, na których go widać.

    Zero wypisane, a nie pominięte: pozycja, która nie rusza nad tą prozą
    niczego, jest odpowiedzią, a nie brakiem pomiaru, i o taką odpowiedź ta
    sonda stoi.
    """
    szerokość = max(len("pozycja"), *(len(pozycja) for pozycja in raport.pozycje))
    wiersze = [
        f"{nagłówek}, {raport.zdań} zdań, {raport.wieloznaczne} wieloznacznych",
        "",
        f"{'pozycja':>{szerokość}}  {'ruszone':>7} {'rozjechane':>10}",
    ]
    for pozycja in raport.pozycje:
        wiersze.append(
            f"{pozycja:>{szerokość}}  {raport.ruszone.get(pozycja, 0):>7}"
            f" {raport.rozjechane.get(pozycja, 0):>10}"
        )
    for pozycja in raport.pozycje:
        zachowane = raport.przykłady.get(pozycja, [])
        if not zachowane:
            continue
        wiersze += ["", f"{pozycja}, czytanie pierwsze olskiego i wariantu:"]
        for zdanie, u_olskiego, w_wariancie in zachowane:
            wiersze.append(f"  {zdanie}")
            wiersze += _para(u_olskiego, w_wariancie)
    return "\n".join(wiersze)


def _para(u_olskiego: Czytanie, w_wariancie: Czytanie) -> Iterator[str]:
    """Oba czytania pierwsze jednego zdania, każde pod swoją etykietą.

    Etykieta stoi nad czytaniem, a nie w jego wierszu, bo czytanie zdania
    złożonego ma wiersz na każde składowe (:func:`olski.check.czytanie`).
    Nazywa mianownik i wariant, a nie cenę, bo wariant bywa i droższy
    (:func:`zmierz`).
    """
    for etykieta, streszczenie in (("olski", u_olskiego), ("wariant", w_wariancie)):
        yield f"    {etykieta}:"
        yield from czytanie(streszczenie, "      ")


def main(argv: Sequence[str] | None = None) -> int:
    pozycje = pozycje_produkcji()
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.cena",
        description="ile pozycja cennika rusza czytanie pierwsze, nad prozą",
    )
    parser.add_argument(
        "ścieżki",
        nargs="*",
        metavar="ścieżka",
        help="pliki prozy albo dokumenty; bez nich cała proza repozytorium",
    )
    parser.add_argument(
        "--pozycja",
        action="append",
        choices=pozycje,
        metavar="NAZWA",
        help=f"mierz tę jedną pozycję; bez tego każdą, którą płaci produkcja "
        f"({', '.join(pozycje)})",
    )
    parser.add_argument(
        "--przykłady",
        type=int,
        default=PRZYKŁADY,
        metavar="N",
        help=f"ile zdań pokazać pod pozycją (domyślnie {PRZYKŁADY})",
    )
    args = parser.parse_args(argv)
    ścieżki = [Path(nazwa) for nazwa in args.ścieżki] or proza_repozytorium()
    raport = przebieg(ścieżki, args.pozycja or pozycje, args.przykłady)
    nazwa = ", ".join(ścieżka.name for ścieżka in ścieżki) if args.ścieżki else "cała proza"
    print(wydruk(raport, nazwa))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
