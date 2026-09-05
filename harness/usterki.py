"""Korpus usterek: które zgłoszenia, których autor potrzebuje, olski już wydaje.

``próba/usterki.txt`` jest kolejką roboty toru gramatycznego.
Wpis niesie zdanie z usterką, nazwę zgłoszenia, które ma nad nim paść,
i poprawkę, nad którą to zgłoszenie ma milczeć.
Sonda puszcza oba zdania przez ``olski-check`` i mówi o każdym wpisie jedno słowo:

- :data:`WYKRYTE`: zgłoszenie pada nad zdaniem i nie pada nad poprawką;
- :data:`SZUM`: zgłoszenie pada nad obojgiem, więc nie widzi usterki, tylko coś obok;
- :data:`NIECZYTANE`: zgłoszenia nie ma, a olski zdania nie czyta,
  więc o usterce nie mówi nic gramatyka, a nie wykrywacz;
- :data:`CISZA`: olski zdanie czyta i zgłoszenia nie wydaje.

Wpis czysty (``zgłoszenie: żadne``) dostaje :data:`CZYSTE`, gdy nic, co autor ma
poprawić, nad nim nie pada, a :data:`SZUM`, gdy pada cokolwiek takiego. Wiersz
o odczytaniach szumem nad nim nie jest (:data:`ODPOWIEDZI`).

Zgłoszeniem jest tu wszystko, co ``olski-check`` wypisuje nad zdaniem
z jakąkolwiek flagą: nazwy z :data:`olski.werdykt.ZGŁOSZENIA`,
nazwa chwytu spod ``--chwyty`` (``olski/chwyty.py``)
i rzecz w pozycji osoby spod ``--osoby``.
Nazwa, której olski nie wydaje wcale, jest wpisem kolejki i wychodzi ciszą
albo nieczytaniem, i to jest liczba, po którą się tę sondę puszcza.

    python3 -m harness.usterki
"""

from __future__ import annotations

import argparse
import collections
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from harness.wybory import wpisy
from olski.chwyty import chwyty
from olski.werdykt import WIELOZNACZNE, Zdanie, nad_tekstem, niespełnione_żądania

#: Korpus usterek.
USTERKI = Path(__file__).parent.parent / "próba" / "usterki.txt"

#: Zgłoszenie, które nie ma paść: wpis o zdaniu bez usterki.
ŻADNE = "żadne"

#: Nazwa zgłoszenia spod flagi, której :data:`olski.werdykt.ZGŁOSZENIA` nie liczy.
OSOBA = "rzecz w pozycji osoby"

#: Te zgłoszenia, nad którymi autor nie ma czego poprawić, więc nad wpisem czystym
#: szumem nie są: wieloznaczność jest odpowiedzią, a nie znaleziskiem
#: (docs/subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem).
ODPOWIEDZI = frozenset({WIELOZNACZNE})

KLUCZE = ("kontekst", "zdanie", "usterka", "zgłoszenie", "poprawka")

WYKRYTE = "wykryte"
SZUM = "szum"
NIECZYTANE = "nieczytane"
CISZA = "cisza"
CZYSTE = "czyste"

#: Klasy w kolejności wydruku. Krotka, a nie zbiór, bo zbiór postawiony na drodze
#: do wydruku wypisuje w każdym przebiegu co innego.
KLASY = (WYKRYTE, CISZA, NIECZYTANE, SZUM, CZYSTE)


@dataclass(frozen=True)
class Usterka:
    """Jeden wpis korpusu: zdanie, co w nim jest nie tak i co ma o tym paść."""

    kontekst: tuple[str, ...]
    zdanie: str
    usterka: str
    zgłoszenie: str
    poprawka: str | None

    @property
    def czysty(self) -> bool:
        return self.zgłoszenie == ŻADNE


@dataclass(frozen=True)
class Wynik:
    """Co olski mówi dziś o jednym wpisie."""

    wpis: Usterka
    klasa: str
    #: Wszystko, co pada nad zdaniem z usterką.
    nad_zdaniem: tuple[str, ...]
    #: Wszystko, co pada nad poprawką; pusta krotka nad wpisem czystym.
    nad_poprawką: tuple[str, ...]
    #: Wiersz werdyktu nad zdaniem z usterką.
    werdykt: str


def czytaj(path: Path = USTERKI) -> list[Usterka]:
    """Wpisy z pliku; wpis niepełny jest błędem, a nie ciszą.

    Wpis z usterką bez poprawki nie mówi, czy zgłoszenie widzi usterkę,
    czy coś obok niej, więc poprawka jest tu wymagana tak samo jak zdanie.
    """
    usterki = []
    for pola in wpisy(path, KLUCZE, ("zdanie", "zgłoszenie")):
        zgłoszenie = pola["zgłoszenie"][0]
        poprawka = pola.get("poprawka", [None])[0]
        usterka = " ".join(pola.get("usterka", ()))
        if zgłoszenie != ŻADNE and not (poprawka and usterka):
            raise ValueError(f"{path}: wpis z usterką bez poprawki albo bez usterki: {pola['zdanie'][0]}")
        if zgłoszenie == ŻADNE and (poprawka or usterka):
            raise ValueError(f"{path}: wpis czysty z poprawką albo usterką: {pola['zdanie'][0]}")
        usterki.append(
            Usterka(
                kontekst=tuple(pola.get("kontekst", ())),
                zdanie=pola["zdanie"][0],
                usterka=usterka,
                zgłoszenie=zgłoszenie,
                poprawka=poprawka,
            )
        )
    return usterki


def zgłoszenia(zdanie: Zdanie) -> tuple[str, ...]:
    """Wszystko, co ``olski-check`` wypisuje nad tym zdaniem, z każdą flagą naraz.

    Chwyt nazywa się tu swoją regułą, a nazwa wchodzi raz, choćby ta reguła
    trafiła w zdanie dwa razy: powtórzona wypisałaby się dwa razy obok werdyktu.
    """
    nazwy = list(zdanie.zgłoszenia)
    nazwy += dict.fromkeys(chwyt.nazwa for chwyt in chwyty(zdanie.werdykt.text))
    if niespełnione_żądania(zdanie.werdykt):
        nazwy.append(OSOBA)
    return tuple(nazwy)


def ostatnie(kontekst: Sequence[str], zdanie: str) -> Zdanie:
    """Werdykt nad zdaniem czytanym za swoim kontekstem, tą drogą, którą idzie ``olski-check``."""
    zdania = nad_tekstem(" ".join((*kontekst, zdanie)))
    if not zdania or zdania[-1].werdykt.text != zdanie:
        raise ValueError(f"wpis, którego napis nie jest zdaniem swojego akapitu: {zdanie}")
    return zdania[-1]


def zbadaj(wpis: Usterka) -> Wynik:
    """Zapytaj olskiego o zdanie i o poprawkę i przyłóż odpowiedź do wpisu."""
    zdanie = ostatnie(wpis.kontekst, wpis.zdanie)
    nad_zdaniem = zgłoszenia(zdanie)
    nad_poprawką = zgłoszenia(ostatnie(wpis.kontekst, wpis.poprawka)) if wpis.poprawka else ()
    return Wynik(
        wpis=wpis,
        klasa=_klasa(wpis, nad_zdaniem, nad_poprawką, zdanie.werdykt.czytane),
        nad_zdaniem=nad_zdaniem,
        nad_poprawką=nad_poprawką,
        werdykt=zdanie.werdykt.explain(),
    )


def _klasa(
    wpis: Usterka, nad_zdaniem: Sequence[str], nad_poprawką: Sequence[str], czytane: bool
) -> str:
    if wpis.czysty:
        return SZUM if any(nazwa not in ODPOWIEDZI for nazwa in nad_zdaniem) else CZYSTE
    if wpis.zgłoszenie in nad_zdaniem:
        return SZUM if wpis.zgłoszenie in nad_poprawką else WYKRYTE
    return CISZA if czytane else NIECZYTANE


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(wyniki: Sequence[Wynik]) -> str:
    """Klasy na zgłoszenie, a pod nimi wpis po wpisie.

    Zero wypisane, a nie pominięte: zgłoszenie bez ani jednego wykrycia jest
    odpowiedzią tej sondy, a nie brakiem odpowiedzi, bo to ono jest kolejką.
    """
    z_usterką = [w for w in wyniki if not w.wpis.czysty]
    czyste = [w for w in wyniki if w.wpis.czysty]
    wiersze = [f"{len(z_usterką)} zdań z usterką, {len(czyste)} czystych"]
    nazwy = list(dict.fromkeys(w.wpis.zgłoszenie for w in z_usterką))
    for nazwa in nazwy:
        swoje = [w for w in z_usterką if w.wpis.zgłoszenie == nazwa]
        ile = collections.Counter(w.klasa for w in swoje)
        liczby = ", ".join(f"{klasa} {ile[klasa]}" for klasa in KLASY if klasa != CZYSTE)
        wiersze.append(f"  {nazwa}, {len(swoje)}: {liczby}")
    if czyste:
        ile = collections.Counter(w.klasa for w in czyste)
        wiersze.append(f"  {ŻADNE}, {len(czyste)}: {CZYSTE} {ile[CZYSTE]}, {SZUM} {ile[SZUM]}")
    szerokość = max(len(klasa) for klasa in KLASY)
    wiersze += ["", "  wpis po wpisie:"]
    wiersze += [_wypis(w, szerokość) for w in wyniki]
    return "\n".join(wiersze)


def _wypis(wynik: Wynik, szerokość: int) -> str:
    wpis = wynik.wpis
    wiersze = [f"  {wynik.klasa:>{szerokość}}  {wpis.zgłoszenie}: {wpis.zdanie}"]
    if wpis.usterka:
        wiersze.append(f"    usterka: {wpis.usterka}")
    wiersze.append(f"    dziś: {wynik.werdykt}")
    obok = [n for n in wynik.nad_zdaniem if n != wpis.zgłoszenie]
    if obok:
        wiersze.append(f"    obok: {', '.join(obok)}")
    if wynik.klasa == SZUM and wpis.poprawka:
        wiersze.append(f"    nad poprawką też: {', '.join(wynik.nad_poprawką)}")
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.usterki",
        description="Sprawdź, które zgłoszenia z korpusu usterek olski już wydaje.",
    )
    parser.add_argument(
        "ścieżka",
        nargs="?",
        help=f"korpus usterek (domyślnie {USTERKI.parent.name}/{USTERKI.name})",
    )
    args = parser.parse_args(argv)
    path = Path(args.ścieżka) if args.ścieżka else USTERKI
    if not path.is_file():
        print(f"harness.usterki: nie ma takiego pliku: {path}", file=sys.stderr)
        return 2
    print(wydruk([zbadaj(wpis) for wpis in czytaj(path)]))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
