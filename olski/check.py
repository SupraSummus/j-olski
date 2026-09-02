"""Sprawdzenie tekstu wobec gramatyki, z wiersza poleceń.

Wydruk zgłasza znaleziska i milczy o zdaniu, o którym nie ma nic do powiedzenia
(:func:`_wiersze`), a ile tego milczenia było, mówi ostatni wiersz przebiegu
(:class:`olski.werdykt.Podsumowanie`).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path

from olski.rozstrzyganie import PUSTE, Rozstrzygnięcie, domyślni, rozstrzygnij, sąsiedztwa
from olski.werdykt import (
    OdczytaniaFormy,
    Podsumowanie,
    Verdict,
    check,
    dalsze_zatrzymania,
)

#: Znak, którym wiersz morfologii oddziela dwa odczytania jednej formy.
#: Przecinka tu nie ma, bo przecinek jest formą i ma w tym wykazie własny
#: wiersz, a średnikiem rozdziela werdykt własne człony.
MIĘDZY_ODCZYTANIAMI = " | "

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


def _czytanie(streszczenie: tuple[dict[str, str], ...], wcięcie: str) -> Iterator[str]:
    """Wiersze jednego czytania: po jednym na zdanie składowe.

    Kreska otwiera czytanie, a składowe następne stoją pod nim bez niej,
    bo lista liczy czytania: kreska przy każdym składowym mówiłaby,
    że zdanie o dwóch składowych i jednym czytaniu ma czytania dwa.
    """
    for numer, składowe in enumerate(streszczenie):
        yield f"{wcięcie}- {_role(składowe)}" if numer == 0 else f"{wcięcie}  {_role(składowe)}"


def _czytania(verdict: Verdict) -> Iterator[str]:
    """Wiersze, którymi ``--readings`` mówi, co stoi w której roli.

    Za streszczeniami zdania idą streszczenia konstytuentu, którego
    wieloznaczność streszczenie zdania zostawia nienazwaną
    (``Verdict.rozbieżne`` w ``olski/werdykt.py``).
    """
    for streszczenie in verdict.readings:
        yield from _czytanie(streszczenie, "")
    for rozbieżność in verdict.rozbieżne:
        yield f"„{rozbieżność.konstytuent}” czyta się tak:"
        for streszczenie in rozbieżność.czytania:
            yield from _czytanie(streszczenie, "  ")


def _wiersz_formy(wiersz: OdczytaniaFormy, wcięcie: str) -> str:
    return f"{wcięcie}„{wiersz.forma}”: {MIĘDZY_ODCZYTANIAMI.join(wiersz.odczytania)}"


def _morfologia(verdict: Verdict) -> Iterator[str]:
    """Wiersze, którymi ``--morfologia`` mówi, czym forma w odczytaniu stoi.

    Odczytania są numerowane tak, jak je numeruje ``--readings``, bo obie flagi
    biorą tę samą listę streszczeń (``Verdict.readings`` w ``olski/werdykt.py``).
    Numeru nie ma tam, gdzie wpis jest jeden: nie ma go od czego odróżnić,
    a nad zdaniem odrzuconym nie byłby numerem odczytania
    (``Verdict.morfologia`` mówi, co taki wpis niesie).
    """
    tabele = verdict.morfologia
    numerowane = len(tabele) > 1
    for numer, tabela in enumerate(tabele, start=1):
        if numerowane:
            yield f"odczytanie {numer}:"
        for wiersz in tabela:
            yield _wiersz_formy(wiersz, "  " if numerowane else "")


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


def _wiersze(
    verdict: Verdict, args: argparse.Namespace, świadkowie, sąsiedztwo
) -> Iterator[str]:
    """Co ten przebieg ma o tym zdaniu do powiedzenia, wiersz po wierszu.

    Zdanie bez ani jednego wiersza komenda przemilcza, zamiast meldować,
    że nie ma o nim nic do powiedzenia; ile było tego milczenia,
    mówi podsumowanie całości (:class:`olski.werdykt.Podsumowanie`).
    Flaga dokłada wiersze i tym samym dokłada zdania:
    kto pyta o zatrzymania, pyta o zdania, których olski nie czyta,
    a kto pyta o czytania, pyta o każde zdanie czytane.
    """
    if verdict.znalezisko or (args.zatrzymania and not verdict.czytane):
        yield verdict.explain()
    if args.zatrzymania:
        yield from _dalsze(verdict)
    if args.readings:
        yield from _czytania(verdict)
    #  Morfologię wypisujemy za czytaniami, bo jest tym, z czego wyszły.
    if args.morfologia:
        yield from _morfologia(verdict)
    if świadkowie is not None:
        yield from _rozstrzygnięcia(verdict, świadkowie, sąsiedztwo)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="olski-check",
        description="Sprawdź zdania polskiego tekstu: zgłoś wieloznaczne, "
        "a o zdaniach, których olski nie czyta, milcz do flagi.",
    )
    parser.add_argument("paths", nargs="*", help="pliki zwykłego polskiego tekstu")
    parser.add_argument("-c", "--text", help="sprawdź ten tekst zamiast pliku")
    parser.add_argument(
        "--readings",
        action="store_true",
        help="pokaż, co stoi w której roli, raz na streszczenie odczytania",
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
            sources.append((raw, path.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError) as error:
            print(f"olski-check: nie udało się przeczytać {raw}: {error}", file=sys.stderr)
            return 2

    #  Świadkowie powstają raz na przebieg, a nie raz na zdanie: tabela skłonności
    #  wchodzi z pliku, a dokument ma tyle zdań, ile ma.
    świadkowie = domyślni() if args.rozstrzygaj else None

    wszystkie: list[Verdict] = []
    for name, text in sources:
        #  Sąsiedztwa liczą się dla całego tekstu naraz, bo akapit jest jego
        #  własnością, a nie zdania: zdanie samo nie wie, co stoi przed nim.
        werdykty = check(text)
        wszystkie += werdykty
        konteksty = sąsiedztwa(text) if świadkowie is not None else [PUSTE] * len(werdykty)
        for verdict, sąsiedztwo in zip(werdykty, konteksty, strict=True):
            wiersze = list(_wiersze(verdict, args, świadkowie, sąsiedztwo))
            if not wiersze:
                continue
            print(f"{name}: {verdict.text}")
            for wiersz in wiersze:
                print(f"{' ' * (len(name) + 2)}{wiersz}")

    podsumowanie = Podsumowanie.z_werdyktów(wszystkie)
    print(podsumowanie.explain())
    #  Kod wyjścia niesie znaleziska, a nie milczenie
    #  (docs/subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego).
    return 0 if podsumowanie.wieloznaczne == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
