"""Werdykt każdego zdania cytowanego w prozie, po jednym wierszu na zdanie.

Zdanie wklejone w dokument jako przykład zmienia się razem z gramatyką, a nie
zmienia się razem z nim akapit nad nim: przykład przestaje wtedy pokazywać to, o
czym tamten akapit mówi, i nie widzi tego żaden przebieg. ``tests/test_docs.py``
czyta linki i anchory, a ``tests/test_wydruki.py`` bloki stojące pod komendą,
czyli te, które komenda odtwarza; zdania w backtickach nie stoją pod żadną
komendą i nie pilnuje ich nic.

Wpuszczenie dopełnienia przed czasownik zdania bez podmiotu ruszyło werdykt
czternastu takich zdań, poprawki żądały cztery, i wszystkie cztery znalazł
skrypt pisany na jedną sesję.

Cytatem jest tu wstawka kodowa albo wiersz bloku ``text``, który zaczyna się
wielką literą i kończy znakiem kończącym zdanie. Kryterium jest szerokie i ma
takie być: nazwa, która pod nie podpadnie, dostaje w obu drzewach roboczych ten
sam wiersz, więc kosztuje wiersz wydruku, a nie fałszywy sygnał, gdzie zdanie
pominięte kosztuje dokładnie tę zmianę, dla której ta komenda powstała.

Wiersze idą posortowane zdaniem, a nie kolejnością dokumentu, bo pytanie jest o
to, co gramatyka o zdaniu mówi, a nie gdzie ono stoi: przeniesiony akapit
pokazywałby inaczej różnicę, której nie ma. Z tego samego powodu nie ma tu
numeru wiersza.

    python3 -m harness.cytaty
    git worktree add ../baza HEAD
    diff <(cd ../baza && python3 -m harness.cytaty) <(python3 -m harness.cytaty)
"""

from __future__ import annotations

import argparse
from collections.abc import Iterator, Sequence
from pathlib import Path

from harness.markdown import PARSER
from olski.werdykt import check

KORZEŃ = Path(__file__).resolve().parent.parent

#: Znaki, którymi ta proza kończy zdanie; te same, po których tnie
#: ``sentences`` w ``olski/segmentacja.py``.
KOŃCZY_ZDANIE = (".", "?", "!")


def domyślne() -> list[Path]:
    """Cała proza repozytorium, czyli to, co obejmują reguły pisania (CLAUDE.md).

    Katalogami, a nie listą nazw, żeby dokument dopisany do korzenia, do
    ``docs/`` albo do ``todo/`` wszedł tu sam; ten sam zbiór bierze
    ``tests/test_docs.py``.
    Rejestr konstrukcji jest katalogiem w ``docs/``, więc zejście tam jest
    rekurencyjne: bez tego odcisk minąłby cały ten rejestr.
    """
    return (
        sorted(KORZEŃ.glob("*.md"))
        + sorted((KORZEŃ / "docs").rglob("*.md"))
        + sorted((KORZEŃ / "todo").glob("*.md"))
    )


def wstawki(tekst: str) -> Iterator[str]:
    """Treść każdej wstawki kodowej i każdy wiersz bloku ``text``.

    Gdzie stoi wstawka, mówi parser, a nie wzorzec w tym pliku, z tego samego
    powodu, dla którego mówi to w ``harness/markdown.py``: ciąg backticków bywa
    otwarciem bloku, a bywa wstawką, i rozstrzyga to specyfikacja.
    """
    for token in PARSER.parse(tekst):
        if token.type == "fence" and token.info.strip() == "text":
            yield from token.content.splitlines()
        elif token.type == "inline":
            for dziecko in token.children or ():
                if dziecko.type == "code_inline":
                    yield dziecko.content


def cytat(napis: str) -> bool:
    """Czy ten napis jest zdaniem zacytowanym, a nie nazwą ani wydrukiem.

    Wielka litera na początku odsiewa nazwę pisaną małą literą i wiersz wydruku,
    który zaczyna się od ``<text>:``, a znak kończący zdanie odsiewa nazwę pliku
    i flagę. Zdanie bez takiego znaku odsiewa się samo i nie jest to strata:
    werdykt nad napisem niedomkniętym jest ``unclosed`` i o gramatyce nie mówi nic.
    """
    napis = napis.strip()
    return bool(napis) and napis[0].isupper() and napis.endswith(KOŃCZY_ZDANIE)


def wiersze(ścieżka: Path, tekst: str) -> list[str]:
    """Werdykty cytatów tego pliku, po jednym wierszu na zdanie, w porządku wyżej.

    Zdanie jest kluczem, więc cytat powtórzony w pliku daje jeden wiersz: drugi
    niósłby ten sam werdykt i tę samą liczbę czytań.
    """
    znalezione: dict[str, str] = {}
    for napis in wstawki(tekst):
        zdanie = napis.strip()
        if not cytat(zdanie):
            continue
        for werdykt in check(zdanie):
            znalezione[werdykt.text] = (
                f"{ścieżka.name:<24} {werdykt.status:<9} {werdykt.result.ile:>4}  {werdykt.text}"
            )
    return [znalezione[zdanie] for zdanie in sorted(znalezione)]


def wydruk(ścieżki: Sequence[Path]) -> str:
    return "\n".join(
        wiersz
        for ścieżka in ścieżki
        for wiersz in wiersze(ścieżka, ścieżka.read_text(encoding="utf-8"))
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.cytaty",
        description="werdykt każdego zdania cytowanego w prozie, do porównania diffem",
    )
    parser.add_argument(
        "ścieżki",
        nargs="*",
        metavar="ścieżka",
        help="pliki Markdown; bez nich cała proza repozytorium",
    )
    args = parser.parse_args(argv)
    ścieżki = [Path(nazwa) for nazwa in args.ścieżki] or domyślne()
    print(wydruk(ścieżki))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
