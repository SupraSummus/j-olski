"""Który kawałek cudzej prozy czyta się teraz, żeby korpus usterek rósł cudzym zdaniem.

Zdanie wchodzi do ``próba/usterki.txt`` z wycinka przeczytanego w całości, a nie
z prozy przeszukanej pod usterkę, a po co tak, mówi docs/roadmap.md#cele.
Ten moduł mówi tylko, który to wycinek: rejestr ``próba/przeczytane.txt`` niesie
przeczytane, a ``--następny`` wypisuje pierwszy wycinek, którego w nim nie ma.

Kolejność wycinków idzie odciskiem ``sha256``, a nie kolejnością plików, i z tego
samego powodu co w ``harness/sądy.py``: dziesięć wycinków wziętych po kolei
byłoby pierwszym katalogiem korpusu, a odcisk rozrzuca je po całości i daje w
każdym przebiegu tę samą kolejność.

    python3 -m harness.wycinek proza/nkjp
    python3 -m harness.wycinek --następny proza/nkjp
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from harness import pliki_prozy
from harness.wybory import wpisy
from olski.document import Document

#: Rejestr wycinków przeczytanych ręką.
PRZECZYTANE = Path(__file__).parent.parent / "próba" / "przeczytane.txt"

#: Ile zdań ma wycinek: tyle, ile ktoś przeczyta uważnie za jednym posiedzeniem.
#: Wycinek dłuższy czyta się pobieżnie, a rejestr mówi wtedy o przeczytaniu,
#: którego nie było.
CEL = 100

KLUCZE = ("od", "do")


@dataclass(frozen=True)
class Kawałek:
    """Zdania jednego pliku, numerowane od jednego, i ścieżka tego pliku.

    Wycinek jest ciągiem kawałków, a nie ciągiem zdań, bo plik jest w tym korpusie
    jednostką ciągłości: sekcje jednej próbki NKJP pochodzą z różnych miejsc
    książki (``harness/nkjp.py``), więc czytelnik dostaje granicę między nimi
    wypisaną, zamiast czytać dwa urywki jako jeden tekst.
    """

    plik: Path
    od: int
    do: int

    @property
    def ile(self) -> int:
        return self.do - self.od + 1


@dataclass(frozen=True)
class Wycinek:
    kawałki: tuple[Kawałek, ...]

    @property
    def od(self) -> str:
        return f"{self.kawałki[0].plik} {self.kawałki[0].od}"

    @property
    def do(self) -> str:
        return f"{self.kawałki[-1].plik} {self.kawałki[-1].do}"

    @property
    def ile(self) -> int:
        return sum(kawałek.ile for kawałek in self.kawałki)


def wycinki(katalog: Path, cel: int = CEL) -> list[Wycinek]:
    """Proza tego katalogu pocięta na wycinki, każdy o mniej więcej ``cel`` zdaniach.

    Plik wchodzi do wycinka w całości, dopóki się w nim mieści, bo cięcie w środku
    pliku zabiera zdaniom sprzed cięcia i zdaniom po nim kontekst, w którym się je
    czyta, a usterka bywa widoczna dopiero z niego. Plik dłuższy od całego wycinka
    tego kontekstu i tak nie ma w jednym kawałku, więc dopiero on tnie się na
    zakresy zdań. Wycinek nie przechodzi przy tym przez granicę warstwy, czyli
    katalogu najwyżej pod korzeniem korpusu: warstwa nazywa rejestr, a wycinek
    złożony z dwóch rejestrów czyta się dwoma rejestrami naraz.
    """
    gotowe: list[Wycinek] = []
    bieżące: list[Kawałek] = []
    zdań, warstwa = 0, None

    def zamknij() -> None:
        nonlocal bieżące, zdań
        if bieżące:
            gotowe.append(Wycinek(tuple(bieżące)))
            bieżące, zdań = [], 0

    for plik in pliki_prozy(katalog):
        ścieżka = plik.relative_to(katalog)
        if ścieżka.parts[0] != warstwa:
            zamknij()
            warstwa = ścieżka.parts[0]
        ile = len(Document(plik.read_text(encoding="utf-8")).sentences)
        if not ile:
            continue
        if zdań + ile > cel:
            zamknij()
        for początek in range(1, ile + 1, cel):
            koniec = min(początek + cel - 1, ile)
            bieżące.append(Kawałek(ścieżka, początek, koniec))
            zdań += koniec - początek + 1
            if zdań >= cel:
                zamknij()
    zamknij()
    return sorted(gotowe, key=lambda wycinek: hashlib.sha256(wycinek.od.encode()).hexdigest())


def przeczytane(rejestr: Path = PRZECZYTANE) -> set[str]:
    """Początki wycinków, które ktoś już przeczytał.

    Sam początek, bo to on nazywa wycinek: koniec rusza się, kiedy korpus albo
    :data:`CEL` się zmieni, a wycinek zaczynający się w tym samym miejscu jest tym
    samym kawałkiem prozy i drugi raz go nikt nie czyta.
    """
    if not rejestr.exists():
        return set()
    return {wpis["od"][0] for wpis in wpisy(rejestr, KLUCZE, KLUCZE)}


def następny(wszystkie: Sequence[Wycinek], znane: set[str]) -> Wycinek | None:
    return next((wycinek for wycinek in wszystkie if wycinek.od not in znane), None)


def wydruk(wycinek: Wycinek, katalog: Path) -> str:
    """Wycinek do przeczytania, wraz z wpisem, którym się go zapisuje do rejestru."""
    wiersze = [
        f"# {wycinek.ile} zdań w {len(wycinek.kawałki)} plikach,"
        " a wpis do próba/przeczytane.txt brzmi",
        "#",
        f"# od: {wycinek.od}",
        f"# do: {wycinek.do}",
    ]
    for kawałek in wycinek.kawałki:
        dokument = Document((katalog / kawałek.plik).read_text(encoding="utf-8"))
        zdania = dokument.sentences[kawałek.od - 1 : kawałek.do]
        wiersze.append(f"\n--- {kawałek.plik} {kawałek.od}-{kawałek.do}")
        wiersze.append(dokument.text[zdania[0].start : zdania[-1].end])
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    katalog = Path(args.katalog)
    if not katalog.is_dir():
        print(f"harness.wycinek: no such directory: {katalog}", file=sys.stderr)
        return 2
    wszystkie = wycinki(katalog)
    znane = przeczytane()
    if not args.następny:
        print(f"{len(wszystkie)} wycinków w {katalog}, przeczytanych {len(znane)}")
        return 0
    wycinek = następny(wszystkie, znane)
    if wycinek is None:
        print(f"harness.wycinek: {katalog} jest przeczytany w całości", file=sys.stderr)
        return 1
    print(wydruk(wycinek, katalog))
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="harness.wycinek",
        description="Wypisz wycinek prozy do przeczytania ręką, ten, którego nikt nie czytał.",
        epilog=__doc__.split("\n\n")[-1],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("katalog", help="katalog z prozą korpusu")
    parser.add_argument(
        "--następny",
        action="store_true",
        help="wypisz pierwszy wycinek, którego nie ma w próba/przeczytane.txt "
        "(bez tego: ile ich jest i ile przeczytano)",
    )
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
