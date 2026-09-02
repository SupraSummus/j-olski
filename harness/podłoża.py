"""Porównanie dwóch podłoży nad tymi samymi zdaniami.

Werdykt olskiego bierze się z ``olski/werdykt.py``, werdykt sondy z tych samych
segmentów przepuszczonych przez ``harness/wiezy.py``, a wydruk pokazuje, gdzie się
rozchodzą. Zdanie, na którym oba mówią to samo, jest tu dowodem taniości
deklaracji, a zdanie, na którym się różnią, dowodem, czego podłoże więzowe nie
ma za darmo. Jedno i drugie jest wynikiem tej sondy.

    python3 -m harness.podłoża -c "Projekt jest dla przyjemności."
    python3 -m harness.podłoża proza/README.txt
    python3 -m harness.podłoża -c "Dużą Jan kupuje książkę." --nieciągłe
"""

from __future__ import annotations

import argparse
import signal
import time
from collections.abc import Sequence
from pathlib import Path

from harness.komenda import Komenda, uruchom
from harness.polszczyzna import GRAMATYKA
from harness.wiezy import Rozbiór, rozbierz
from olski.segmentacja import morphology, sentences
from olski.werdykt import check as olski_check

#: Ile czytań zbierać. Werdykt zamyka się na drugim, a wyższy limit stoi tu po
#: to, żeby dało się porównać liczby z olskim, który zbiera do MAX_READINGS.
LIMIT = 64

#: Ile sekund dostaje jedno zdanie. Budżet stoi tu, bo przeszukiwanie więzów nie
#: ma ograniczenia, które ma parser tablicowy, i najdroższe jest tam, gdzie
#: rejestr jest najgęstszy: przy zdaniu długim, które trzeba odrzucić, a odrzucić
#: znaczy wyczerpać całą przestrzeń. Zdanie, które budżetu nie dowiozło, wchodzi do
#: podsumowania jako urwane, a nie jako odrzucone, bo to dwie różne odpowiedzi.
BUDŻET = 10.0

#: Etykiety, które raport nazywa, i nazwa, którą im daje. Dwie etykiety
#: orzecznika czytelnika nie interesują: różni je to, co się z czym zgadza, a nie
#: to, czym orzecznik w zdaniu jest.
ROLE = (
    ("podmiot", "podmiot"),
    ("dopełnienie", "dopełnienie"),
    ("orzecznik", "orzecznik"),
    ("orzecznik_narzędnikowy", "orzecznik"),
    ("wyrażenie_przyimkowe", "wyrażenie_przyimkowe"),
)


class Urwane(Exception):
    """Zdanie nie zmieściło się w budżecie."""


def _alarm(*_):
    raise Urwane()


def _argumenty(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--nieciągłe",
        action="store_true",
        dest="nieciagle",
        help="zdejmij spójność, czyli wpuść konstytuent nieciągły",
    )
    parser.add_argument(
        "--budżet",
        type=float,
        default=BUDŻET,
        dest="budzet",
        help=f"ile sekund dostaje jedno zdanie (domyślnie {BUDŻET:.0f})",
    )
    parser.add_argument(
        "--łuki",
        action="store_true",
        dest="luki",
        help="wypisz łuki każdego czytania",
    )


def przebieg(źródła: Sequence[tuple[str, str]], args: argparse.Namespace) -> str:
    """Przepuść każde zdanie przez oba podłoża i wypisz, gdzie się rozchodzą.

    Zdanie schodzi na wyjście od razu, a nie razem z podsumowaniem: przebieg nad
    prozą trwa tyle, ile najdroższe zdanie razy ich liczba, więc czytelnik ma
    widzieć, na którym stanął. Wraca stąd samo podsumowanie, czyli to, co sonda
    ma do powiedzenia o całości.
    """
    signal.signal(signal.SIGALRM, _alarm)
    zgodne = tyle_samo = doszły = zdań = 0
    najdłuższe = 0.0
    for nazwa, tekst in źródła:
        werdykty = {werdykt.text: werdykt for werdykt in olski_check(tekst)}
        for zdanie in sentences(tekst):
            werdykt = werdykty[zdanie]
            if not werdykt.punktowane:
                continue
            zdań += 1
            segmenty = morphology(zdanie)
            print(f"{nazwa}: {zdanie}")
            olskie = _ile(len(werdykt.result.readings), werdykt.result.truncated)
            print(f"  olski: {werdykt.status:9} {olskie}")
            start = time.perf_counter()
            try:
                signal.setitimer(signal.ITIMER_REAL, args.budzet)
                rozbiór = rozbierz(
                    segmenty, GRAMATYKA, limit=LIMIT, spójne=not args.nieciagle
                )
            except Urwane:
                print(f"  podłoża: {'urwane':9} nie zmieściło się w {args.budzet:.0f}s")
                continue
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
            najdłuższe = max(najdłuższe, time.perf_counter() - start)
            doszły += 1
            zgodne += _zgodne(werdykt, rozbiór)
            tyle_samo += len(rozbiór.czytania) == len(werdykt.result.readings)
            liczba = _ile(len(rozbiór.czytania), rozbiór.urwane)
            print(f"  podłoża: {rozbiór.status:9} {liczba}{_uwaga(rozbiór)}")
            for czytanie in rozbiór.czytania:
                print(f"    - {_role(czytanie)}")
                if args.luki:
                    print(f"      {_łuki(czytanie)}")

    return (
        f"{doszły} of {zdań} sentences finished inside {args.budzet:.0f}s, "
        f"the slowest in {najdłuższe:.2f}s, "
        f"and {zgodne} of those get the same verdict from both, "
        f"{tyle_samo} the same number of readings"
    )


def _proza(wejścia: Sequence[tuple[Path, str]], args: argparse.Namespace) -> str:
    return przebieg([(str(ścieżka), tekst) for ścieżka, tekst in wejścia], args)


def _zdania(tekst: str, args: argparse.Namespace) -> str:
    return przebieg([("<text>", tekst)], args)


def _zgodne(werdykt, rozbiór: Rozbiór) -> bool:
    return werdykt.status == rozbiór.status


def _ile(liczba: int, urwane: bool = False) -> str:
    if liczba == 1 and not urwane:
        return "one reading"
    return f"{liczba}{'+' if urwane else ''} readings"


def _uwaga(rozbiór: Rozbiór) -> str:
    if rozbiór.czytania or not rozbiór.bez_głowy:
        return ""
    return f", nothing attaches: {', '.join(rozbiór.bez_głowy)}"


def _role(czytanie) -> str:
    wypełnione = [(nazwa, czytanie.rola(etykieta)) for etykieta, nazwa in ROLE]
    return ", ".join(f"{nazwa}: {czym}" for nazwa, czym in wypełnione if czym) or "(brak roli)"


def _łuki(czytanie) -> str:
    return " ".join(
        f"{czytanie.formy[dziecko]}<{etykieta}-{czytanie.formy[głowa]}"
        for dziecko, głowa, etykieta in czytanie.łuki
    )


KOMENDA = Komenda(
    nazwa="harness.podłoża",
    opis="Porównaj werdykt olskiego z werdyktem podłoża więzowego.",
    proza=_proza,
    zdania=_zdania,
    argumenty=_argumenty,
)


if __name__ == "__main__":
    raise SystemExit(uruchom(KOMENDA))
