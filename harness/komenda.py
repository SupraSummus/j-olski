"""Wiersz poleceń wspólny sondom, które mierzą nad korpusem.

Sondy różnią się tym, co liczą, a nie tym, jak się je woła.
Korpus przychodzi ścieżką, próbka wielkością, a pula procesów liczbą,
i o te trzy rzeczy pyta każda z nich tak samo.
Kopia parsera na sondę rozjeżdża się przy tym na samym argumencie pozycyjnym:
ta sama ścieżka nazywa się w takich kopiach ``root``, ``ścieżka`` albo ``korpus``,
choć wszystkie trzy przyjmują to samo — katalog banku drzew albo plik prozy.

Scalenie nie oddala liczby od kodu, który ją liczy,
bo parser nie liczy nic.
Przy sondzie zostaje wywołanie przebiegu i nagłówek nad wydrukiem,
czyli te dwie rzeczy, którymi sondy się różnią,
a stąd sonda otrzymuje ścieżki przyciętą listą oraz wybory z wiersza poleceń.

Sonda podaje o sobie deklarację, tak samo jak format w ``harness/__init__.py``,
i tam też stoi powód, dla którego ``argv`` idzie w obu drugie.
Pytanie własne sondy — ``--budżet``, ``--wariant``, ``--morfologia`` —
wchodzi funkcją dopisującą argumenty,
bo pomoc do niego mówi o tym, co ta jedna sonda mierzy.

Poza tym wejściem zostają programy, które korpusu lasów nie czytają — ekstrakcja
i to, co pyta Walentego — oraz dwie sondy, które czytają go innym kształtem
wejścia: ``harness/rama.py`` nie zna ani ``--limit``, ani ``--jobs``,
a ``harness/podłoża.py`` przyjmuje wiele ścieżek naraz zamiast jednej.
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
    #: Wydruk nad jednym plikiem prozy; ``None``, gdy sonda czyta sam bank drzew.
    #: Tekst i ścieżka idą osobno: plik czyta ten moduł, bo kodowanie jest jedną
    #: decyzją, a nagłówek sondy nazywa plik, po którym ta liczba wyszła.
    proza: Callable[[str, Path, argparse.Namespace], str] | None = None
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
    if args.ścieżka is None:
        parser.error("podaj ścieżkę albo -c")

    ścieżka = Path(args.ścieżka)
    if ścieżka.is_dir():
        print(komenda.korpus(pliki(ścieżka)[: args.limit], args))
        return 0
    if ścieżka.is_file() and komenda.proza is not None:
        print(komenda.proza(ścieżka.read_text(encoding="utf-8"), ścieżka, args))
        return 0

    czego = "katalogu" if komenda.proza is None else "katalogu ani pliku"
    print(f"{komenda.nazwa}: nie ma takiego {czego}: {ścieżka}", file=sys.stderr)
    print(f"{komenda.nazwa}: docs/corpus.md mówi, skąd wziąć korpus", file=sys.stderr)
    return 2


def _parser(komenda: Komenda) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=f"python3 -m {komenda.nazwa}",
        description=komenda.opis,
    )
    przyjmuje = "katalog z rozpakowaną Składnicą"
    if komenda.proza is not None:
        przyjmuje += " albo plik z prozą do przeczytania"
    parser.add_argument(
        "ścieżka",
        nargs="?" if komenda.zdania is not None else None,
        help=przyjmuje,
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
