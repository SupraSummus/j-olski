"""Wiersz poleceń wspólny sondom, które mierzą nad korpusem.

Sondy różnią się tym, co liczą, a nie tym, jak się je woła.
Korpus przychodzi ścieżkami, próbka wielkością, a pula procesów liczbą,
i o te trzy rzeczy pyta każda z nich tak samo.
Kopia parsera na sondę rozjeżdża się przy tym na samym argumencie pozycyjnym:
ta sama ścieżka nazywa się w takiej kopii ``root`` albo ``korpus``,
choć przyjmuje to samo — katalog banku drzew albo pliki prozy.

Bank drzew jest jednym katalogiem, więc kilka ścieżek naraz może znaczyć tylko
prozę, i na tym stoi rozdanie wejścia.
Prozy bierze się tyle plików, ile ich podano, bo rejestr bywa wieloplikowy —
siedem aktów ustaw — a zlepienie go w jeden plik jest krokiem,
którego dokument nie ma jak wydrukować obok liczby;
jeden raport składa z nich ``scal`` po stronie sondy.
Katalog podany sondzie, która banku drzew nie czyta, jest katalogiem z prozą:
trzeciego rodzaju wejścia rozdanie nie ma, bo to deklaracja sondy mówi,
czym jest dla niej katalog, i korpus audytowy przychodzi drzewem plików.

Przy sondzie zostaje wywołanie przebiegu i nagłówek nad wydrukiem,
czyli te dwie rzeczy, którymi sondy się różnią,
a stąd sonda otrzymuje ścieżki przyciętą listą oraz wybory z wiersza poleceń.

O flagę pyta ta sonda, której przebieg ją czyta.
``--limit`` ucina listę lasów, a ``--jobs`` dzieli ją na procesy,
więc obu nie ma sonda, która banku drzew nie czyta,
a ``--jobs`` nie ma także ta, która lasy przechodzi jednym procesem;
``--przykłady`` nie ma ta, która przykładów pod liczbą nie pokazuje.
Flaga wypisana mimo to obiecuje w pomocy przebieg, którego nie ma.

Sonda podaje o sobie deklarację, tak samo jak format w ``harness/__init__.py``,
i tam też stoi powód, dla którego ``argv`` idzie w obu drugie.
Pytanie własne sondy — ``--budżet``, ``--wariant``, ``--morfologia`` —
wchodzi funkcją dopisującą argumenty,
bo pomoc do niego mówi o tym, co ta jedna sonda mierzy.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from harness import PROSE_SUFFIX, pliki_prozy
from harness.corpus import BANK_DRZEW, PLIKI_PROZY, POMYŁKA, pliki, rozdaj


@dataclass(frozen=True)
class Komenda:
    """Co jedna sonda mówi o sobie wspólnemu wierszowi poleceń."""

    #: Nazwa modułu, czyli ``harness.czytania``. Jedna na dwa użytki: pomoc
    #: przedstawia się przez ``python3 -m``, a komunikat o brakującej ścieżce samą
    #: nazwą. Dwa napisy na to rozjeżdżają się, bo nikt ich nie czyta obok siebie.
    nazwa: str
    #: O co ta sonda pyta, jednym zdaniem, do wydruku pomocy.
    opis: str
    #: Wydruk nad bankiem drzew. Ścieżki przychodzą przycięte przez ``--limit``,
    #: a wybory z wiersza poleceń całą przestrzenią nazw, bo sonda pyta o swoje.
    #: ``None``, gdy sonda banku drzew nie czyta (wyżej).
    korpus: Callable[[Sequence[Path], argparse.Namespace], str] | None = None
    #: Wydruk nad plikami prozy; ``None``, gdy sonda czyta sam bank drzew.
    #: Plików jest tyle, ile ich podano (wyżej), a sonda składa z nich jeden raport.
    #: Tekst i ścieżka idą parą: pliki czyta ten moduł, bo kodowanie jest jedną
    #: decyzją, a nagłówek sondy nazywa to, po czym ta liczba wyszła.
    proza: Callable[[Sequence[tuple[Path, str]], argparse.Namespace], str] | None = None
    #: Wydruk nad zdaniami podanymi wprost przez ``-c``, czyli bez korpusu.
    zdania: Callable[[str, argparse.Namespace], str] | None = None
    #: Domyślna wielkość próbki pod wydrukiem. Sondy mają ją różną, bo różnie
    #: dużo trzeba przeczytać, żeby uwierzyć liczbie, którą ta sonda drukuje;
    #: ``None`` znaczy, że przykładów nie pokazuje (wyżej).
    przykłady: int | None = None
    #: Czy przebieg tej sondy dzieli lasy na pulę procesów. Z banku drzew tego nie
    #: widać: część sond czyta go jednym procesem, mając go do przeczytania w całości.
    pula: bool = False
    #: Argumenty, o które pyta ta jedna sonda.
    argumenty: Callable[[argparse.ArgumentParser], None] | None = None


def uruchom(komenda: Komenda, argv: Sequence[str] | None = None) -> int:
    """Mierzy to, co nazwano w wierszu poleceń, i wypisuje wydruk sondy."""
    parser = _parser(komenda)
    args = parser.parse_args(argv)
    if komenda.pula and args.jobs < 1:
        parser.error("--jobs bierze co najmniej jeden proces")

    if komenda.zdania is not None and args.zdania:
        print(komenda.zdania(args.zdania, args))
        return 0
    if not args.ścieżki:
        parser.error("podaj ścieżkę albo -c")

    podane = [Path(nazwa) for nazwa in args.ścieżki]
    rozdanie = rozdaj(podane)
    if rozdanie == BANK_DRZEW and komenda.korpus is not None:
        print(komenda.korpus(pliki(podane[0])[: args.limit], args))
        return 0

    ścieżki = podane
    if rozdanie == BANK_DRZEW:
        ścieżki = pliki_prozy(podane[0])
        rozdanie = PLIKI_PROZY if ścieżki else POMYŁKA
    if rozdanie == PLIKI_PROZY and komenda.proza is not None:
        wejścia = [(ścieżka, ścieżka.read_text(encoding="utf-8")) for ścieżka in ścieżki]
        print(komenda.proza(wejścia, args))
        return 0
    return _pomyłka(komenda, podane)


def _pomyłka(komenda: Komenda, ścieżki: Sequence[Path]) -> int:
    """Czemu z tych ścieżek nic nie wyszło, a potem co ta sonda w ogóle bierze."""
    for ścieżka in ścieżki:
        if not ścieżka.exists():
            print(f"{komenda.nazwa}: nie ma takiej ścieżki: {ścieżka}", file=sys.stderr)
        elif ścieżka.is_dir() and len(ścieżki) > 1:
            print(
                f"{komenda.nazwa}: katalog podaje się sam, bez innych ścieżek: {ścieżka}",
                file=sys.stderr,
            )
        elif ścieżka.is_dir():
            print(
                f"{komenda.nazwa}: nie ma tu prozy: {ścieżka}/*{PROSE_SUFFIX}",
                file=sys.stderr,
            )
    print(f"{komenda.nazwa}: {_przyjmuje(komenda)}", file=sys.stderr)
    print(f"{komenda.nazwa}: {_skąd(komenda)}", file=sys.stderr)
    return 2


def _skąd(komenda: Komenda) -> str:
    """Który dokument mówi, skąd wziąć to, czego tej sondzie zabrakło."""
    if komenda.korpus is not None:
        return "docs/corpus.md mówi, skąd wziąć korpus"
    return "docs/audit-corpus.md mówi, skąd wziąć prozę"


def nagłówek(wejścia: Sequence[tuple[Path, str]]) -> str:
    """Nazwy plików, po których wyszła liczba, do nagłówka wydruku sondy.

    Jeden plik daje samą swoją nazwę, a kilka nazwy po przecinku, bo rejestr
    wieloplikowy poznaje się po tym, które akty w nim stoją.
    """
    return ", ".join(ścieżka.name for ścieżka, _ in wejścia)


def _przyjmuje(komenda: Komenda) -> str:
    """Co ta sonda bierze na wejściu, jednym zdaniem.

    Jedno na dwa użytki: pomoc mówi to przed przebiegiem, a komunikat o pomyłce
    po nim, i obiecywać mają tyle samo.
    """
    z_prozą = "pliki z prozą do przeczytania"
    if komenda.korpus is None:
        return f"katalog z prozą albo {z_prozą}"
    katalog = "katalog z rozpakowaną Składnicą"
    if komenda.proza is None:
        return katalog
    return f"{katalog} albo {z_prozą}"


def _parser(komenda: Komenda) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=f"python3 -m {komenda.nazwa}",
        description=komenda.opis,
    )
    parser.add_argument(
        "ścieżki",
        nargs="*" if komenda.zdania is not None else "+",
        metavar="ścieżka",
        help=_przyjmuje(komenda),
    )
    if komenda.zdania is not None:
        parser.add_argument("-c", dest="zdania", help="zmierz te zdania zamiast korpusu")
    if komenda.korpus is not None:
        parser.add_argument("--limit", type=int, help="zatrzymaj się po tylu lasach")
    if komenda.przykłady is not None:
        parser.add_argument(
            "--przykłady",
            type=int,
            default=komenda.przykłady,
            help=f"ile zdań pokazać pod liczbą (domyślnie {komenda.przykłady})",
        )
    if komenda.argumenty is not None:
        komenda.argumenty(parser)
    if komenda.pula:
        parser.add_argument(
            "--jobs",
            type=int,
            default=os.cpu_count() or 1,
            help="ile procesów czyta i mierzy; 1 liczy w tym",
        )
    return parser
