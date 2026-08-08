"""Porównanie dwóch podłoży nad tymi samymi zdaniami.

Werdykt olskiego bierze się z ``olski/subset.py``, werdykt sondy z tych samych
segmentów przepuszczonych przez ``sonda/wiezy.py``, a wydruk pokazuje, gdzie się
rozchodzą. Zdanie, na którym oba mówią to samo, jest tu dowodem taniości
deklaracji, a zdanie, na którym się różnią, dowodem, czego podłoże więzowe nie
ma za darmo. Jedno i drugie jest wynikiem tej sondy.

    python3 -m sonda -c "Projekt jest dla przyjemności."
    python3 -m sonda proza/README.txt
    python3 -m sonda -c "Dużą Jan kupuje książkę." --nieciągłe
"""

from __future__ import annotations

import argparse
import signal
import sys
import time
from collections.abc import Sequence
from pathlib import Path

from olski.subset import FRAGMENT, morphology, sentences
from olski.subset import check as olski_check
from sonda.polszczyzna import GRAMATYKA
from sonda.wiezy import Rozbiór, rozbierz

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
    ("Subject", "Subject"),
    ("Object", "Object"),
    ("Predicative", "Predicative"),
    ("PredInst", "Predicative"),
    ("Modifier", "Modifier"),
)


class Urwane(Exception):
    """Zdanie nie zmieściło się w budżecie."""


def _alarm(*_):
    raise Urwane()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sonda",
        description="Porównaj werdykt olskiego z werdyktem podłoża więzowego.",
    )
    parser.add_argument("paths", nargs="*", help="pliki zwykłego tekstu polskiego")
    parser.add_argument("-c", "--text", help="sprawdź ten tekst zamiast pliku")
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
    args = parser.parse_args(argv)

    if not args.paths and args.text is None:
        parser.print_usage(sys.stderr)
        return 2

    źródła: list[tuple[str, str]] = []
    if args.text is not None:
        źródła.append(("<text>", args.text))
    for surowa in args.paths:
        try:
            źródła.append((surowa, Path(surowa).read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError) as błąd:
            print(f"sonda: nie da się przeczytać {surowa}: {błąd}", file=sys.stderr)
            return 2

    signal.signal(signal.SIGALRM, _alarm)
    zgodne = tyle_samo = doszły = zdań = 0
    najdłuższe = 0.0
    for nazwa, tekst in źródła:
        werdykty = {werdykt.text: werdykt for werdykt in olski_check(tekst)}
        for zdanie in sentences(tekst):
            werdykt = werdykty[zdanie]
            if werdykt.status == FRAGMENT:
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
                print(f"  sonda: {'urwane':9} nie zmieściło się w {args.budzet:.0f}s")
                continue
            finally:
                signal.setitimer(signal.ITIMER_REAL, 0)
            najdłuższe = max(najdłuższe, time.perf_counter() - start)
            doszły += 1
            zgodne += _zgodne(werdykt, rozbiór)
            tyle_samo += len(rozbiór.czytania) == len(werdykt.result.readings)
            liczba = _ile(len(rozbiór.czytania), rozbiór.urwane)
            print(f"  sonda: {rozbiór.status:9} {liczba}{_uwaga(rozbiór)}")
            for czytanie in rozbiór.czytania:
                print(f"    - {_role(czytanie)}")
                if args.luki:
                    print(f"      {_łuki(czytanie)}")

    print(
        f"{doszły} of {zdań} sentences finished inside {args.budzet:.0f}s, "
        f"the slowest in {najdłuższe:.2f}s, "
        f"and {zgodne} of those get the same verdict from both, "
        f"{tyle_samo} the same number of readings"
    )
    return 0 if zgodne == zdań else 1


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


if __name__ == "__main__":
    raise SystemExit(main())
