"""Wiersz poleceń wspólny sondom, które mierzą nad korpusem.

Sondy różnią się tym, co liczą, a nie tym, jak się je woła.
Korpus przychodzi ścieżkami, próbka wielkością, a pula procesów liczbą,
i o te trzy rzeczy pyta każda z nich tak samo.
Kopia parsera na sondę rozjeżdża się przy tym na samym argumencie pozycyjnym:
ta sama ścieżka nazywa się w takich kopiach ``root``, ``ścieżka`` albo ``korpus``,
choć wszystkie trzy przyjmują to samo — katalog banku drzew albo pliki prozy.

Bank drzew jest jednym katalogiem, więc kilka ścieżek naraz może znaczyć tylko
prozę, i na tym stoi rozdanie wejścia.
Prozy bierze się tyle plików, ile ich podano, bo rejestr bywa wieloplikowy —
siedem aktów ustaw — a zlepienie go w jeden plik jest krokiem,
którego dokument nie ma jak wydrukować obok liczby;
jeden raport składa z nich ``scal`` po stronie sondy.

Scalenie wiersza poleceń nie oddala liczby od kodu, który ją liczy,
bo parser nie liczy nic.
Przy sondzie zostaje wywołanie przebiegu i nagłówek nad wydrukiem,
czyli te dwie rzeczy, którymi sondy się różnią,
a stąd sonda otrzymuje ścieżki przyciętą listą oraz wybory z wiersza poleceń.

Sonda podaje o sobie deklarację, tak samo jak format w ``harness/__init__.py``,
i tam też stoi powód, dla którego ``argv`` idzie w obu drugie.
Pytanie własne sondy — ``--budżet``, ``--wariant``, ``--morfologia`` —
wchodzi funkcją dopisującą argumenty,
bo pomoc do niego mówi o tym, co ta jedna sonda mierzy.

Poza tym wejściem zostają programy, które korpusu lasów nie czytają — ekstrakcja,
to, co pyta Walentego, oraz ``harness/podłoża.py``, który czyta samą prozę i
katalogu nie bierze wcale — a także ``harness/rama.py``, który bank drzew czyta
innym kształtem wejścia: nie zna ani ``--limit``, ani ``--jobs``.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from olski.corpus import pliki


@dataclass(frozen=True)
class Komenda:
    """Co jedna sonda mówi o sobie wspólnemu wierszowi poleceń."""

    #: Nazwa modułu, czyli ``harness.czytania``. Jedna na dwa użytki: pomoc
    #: przedstawia się przez ``python3 -m``, a komunikat o brakującej ścieżce samą
    #: nazwą. Dwa napisy na to rozjeżdżają się, bo nikt ich nie czyta obok siebie.
    nazwa: str
    #: O co ta sonda pyta, jednym zdaniem, do wydruku pomocy.
    opis: str
    #: Domyślna wielkość próbki pod wydrukiem. Sondy mają ją różną, bo różnie
    #: dużo trzeba przeczytać, żeby uwierzyć liczbie, którą ta sonda drukuje.
    przykłady: int
    #: Wydruk nad bankiem drzew. Ścieżki przychodzą przycięte przez ``--limit``,
    #: a wybory z wiersza poleceń całą przestrzenią nazw, bo sonda pyta o swoje.
    korpus: Callable[[Sequence[Path], argparse.Namespace], str]
    #: Wydruk nad plikami prozy; ``None``, gdy sonda czyta sam bank drzew.
    #: Plików jest tyle, ile ich podano (wyżej), a sonda składa z nich jeden raport.
    #: Tekst i ścieżka idą parą: pliki czyta ten moduł, bo kodowanie jest jedną
    #: decyzją, a nagłówek sondy nazywa to, po czym ta liczba wyszła.
    proza: Callable[[Sequence[tuple[Path, str]], argparse.Namespace], str] | None = None
    #: Wydruk nad zdaniami podanymi wprost przez ``-c``, czyli bez korpusu.
    zdania: Callable[[str], str] | None = None
    #: Argumenty, o które pyta ta jedna sonda.
    argumenty: Callable[[argparse.ArgumentParser], None] | None = None


def uruchom(komenda: Komenda, argv: Sequence[str] | None = None) -> int:
    """Mierzy to, co nazwano w wierszu poleceń, i wypisuje wydruk sondy."""
    parser = _parser(komenda)
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs bierze co najmniej jeden proces")

    if komenda.zdania is not None and args.zdania:
        print(komenda.zdania(args.zdania))
        return 0
    if not args.ścieżki:
        parser.error("podaj ścieżkę albo -c")

    ścieżki = [Path(nazwa) for nazwa in args.ścieżki]
    if len(ścieżki) == 1 and ścieżki[0].is_dir():
        print(komenda.korpus(pliki(ścieżki[0])[: args.limit], args))
        return 0
    if komenda.proza is not None and all(ścieżka.is_file() for ścieżka in ścieżki):
        wejścia = [(ścieżka, ścieżka.read_text(encoding="utf-8")) for ścieżka in ścieżki]
        print(komenda.proza(wejścia, args))
        return 0

    for ścieżka in ścieżki:
        if not ścieżka.exists():
            print(f"{komenda.nazwa}: nie ma takiej ścieżki: {ścieżka}", file=sys.stderr)
        elif ścieżka.is_dir():
            print(
                f"{komenda.nazwa}: katalog podaje się sam, bez innych ścieżek: {ścieżka}",
                file=sys.stderr,
            )
    print(f"{komenda.nazwa}: {_przyjmuje(komenda)}", file=sys.stderr)
    print(f"{komenda.nazwa}: docs/corpus.md mówi, skąd wziąć korpus", file=sys.stderr)
    return 2


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
    katalog = "katalog z rozpakowaną Składnicą"
    if komenda.proza is None:
        return katalog
    return f"{katalog} albo pliki z prozą do przeczytania"


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
    parser.add_argument("--limit", type=int, help="zatrzymaj się po tylu lasach")
    parser.add_argument(
        "--przykłady",
        type=int,
        default=komenda.przykłady,
        help=f"ile zdań pokazać pod liczbą (domyślnie {komenda.przykłady})",
    )
    if komenda.argumenty is not None:
        komenda.argumenty(parser)
    parser.add_argument(
        "--jobs",
        type=int,
        default=os.cpu_count() or 1,
        help="ile procesów czyta i mierzy; 1 liczy w tym",
    )
    return parser
