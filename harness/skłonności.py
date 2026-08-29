"""Tabela skłonności przyłączeniowych: budowa z banku drzew i ocena na jego drugiej połowie.

Świadek statystyczny warstwy rozstrzygającej czyta gotową tabelę
(:class:`olski.rozstrzyganie.Skłonność`), a wypisuje ją ten program.
Rozdziela je fotel: tabelę czyta każdy, kto sprawdza własny tekst,
a buduje ją ten, kto olskiego zmienia, raz na wydanie korpusu
(``harness/__init__.py``).

Ocena stoi tu razem z budową, a nie osobno, bo mierzy tę samą tabelę
na tej samej połowie banku drzew, której budowa nie widziała.
Progi, przy których świadek odpowiada, zostają przy nim,
bo pyta o nie także werdykt.

    python3 -m harness.skłonności Składnica-frazowa-180723/ --oceń
    python3 -m harness.skłonności Składnica-frazowa-180723/ --zbuduj olski/skłonności.txt
"""

from __future__ import annotations

import argparse
import collections
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from harness.attachment import attachments
from harness.corpus import pliki, read_forest
from olski.rozstrzyganie import (
    SKŁONNOŚCI,
    STRONA_CZASOWNIKOWA,
    STRONA_IMIENNA,
    WSPARCIE,
    Licznik,
    Pytany,
    Rama,
    Skłonność,
)

#: Jeden wybór wzięty z banku drzew: przyimek, lemat rzeczownika, lemat czasownika
#: i strona, którą wybrał anotator. Tabela liczy się z tego i ocena mierzy na tym.
Wypadek = tuple[str, str, str, str]

NAGŁÓWEK = """\
# Skłonności przyłączeniowe: jak często para przyimka i gospodarza przyłączała
# się w tę stronę. Kolumny to przyimek, strona (`noun` albo `clause`), lemat
# gospodarza, przyłączeń w tę stronę i przyłączeń wszystkich.
#
# Plik jest generowany i nie pisze się go ręcznie. Powstaje ze Składnicy przez
# `python3 -m harness.skłonności <korpus> --zbuduj`, a co z niej bierze, mówi
# `harness/attachment.py`. Wpisy o wsparciu poniżej progu tu nie wchodzą, bo
# świadek i tak by na nie nie patrzył.
#
# Bank drzew jest prozą literacką i prasową, a olski celuje w dokumentację
# techniczną, więc skłonność wzięta stąd jest punktem wyjścia, a nie pomiarem
# rejestru, o który chodzi.
"""


def wypadki(paths: Iterable[Path]) -> list[Wypadek]:
    """Wybory z banku drzew, po jednym na wyrażenie, przed którym wybór w ogóle stał.

    Populacją są wyrażenia przyimkowe stojące za grupą imienną i za czasownikiem,
    czyli ta sama, którą liczy ``Report`` w ``harness/attachment.py``, zawężona do
    tych z oboma lematami. Zwężenie stoi tutaj, bo czytnik oddaje każde wyrażenie
    drzewa wraz z tym, gdzie ono stoi, i populację stawia dopiero pytający.
    """
    zebrane = []
    for path in paths:
        for a in attachments(read_forest(path)):
            if not (a.postnominal and a.postverbal):
                continue
            if a.host not in (STRONA_IMIENNA, STRONA_CZASOWNIKOWA):
                continue
            if a.prep and a.noun and a.verb:
                zebrane.append((a.prep, a.noun, a.verb, a.host))
    return zebrane


def zbuduj(wybory: Iterable[Wypadek], wsparcie: int = WSPARCIE) -> Licznik:
    """Policz pary nad wyborami z banku drzew i zostaw te, które przechodzą próg wsparcia.

    Bierze gotowe wybory, a nie ścieżki, bo ocena buduje tabelę z połowy tych
    samych wyborów, na których potem mierzy: dwa przejścia po korpusie
    rozeszłyby się na pierwszej zmianie w tym, co liczy się za wybór.
    """
    trafień: collections.Counter[tuple[str, str, str]] = collections.Counter()
    wszystkich: collections.Counter[tuple[str, str, str]] = collections.Counter()
    for przyimek, rzeczownik, czasownik, gospodarz in wybory:
        for strona, lemat in ((STRONA_IMIENNA, rzeczownik), (STRONA_CZASOWNIKOWA, czasownik)):
            wszystkich[(przyimek, strona, lemat)] += 1
            if gospodarz == strona:
                trafień[(przyimek, strona, lemat)] += 1
    return {klucz: (trafień[klucz], ile) for klucz, ile in wszystkich.items() if ile >= wsparcie}


def zapisz(licznik: Licznik, path: Path) -> None:
    wiersze = [
        f"{przyimek}\t{strona}\t{lemat}\t{trafień}\t{ile}"
        for (przyimek, strona, lemat), (trafień, ile) in sorted(licznik.items())
    ]
    path.write_text(NAGŁÓWEK + "\n".join(wiersze) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Ocena
# --------------------------------------------------------------------------- #


@dataclass
class Ocena:
    """Ile świadek odpowiada i ile z tego trafia, na materiale, którego nie widział."""

    wypadków: int = 0
    odpowiedzi: int = 0
    trafień: int = 0

    @property
    def zasięg(self) -> float:
        return self.odpowiedzi / self.wypadków if self.wypadków else 0.0

    @property
    def trafność(self) -> float:
        return self.trafień / self.odpowiedzi if self.odpowiedzi else 0.0


#: Ustawienia, które ocena przechodzi, gdy nikt nie poda swoich. Krzywa, a nie
#: punkt, bo świadka tego rodzaju wybiera się właśnie na niej: zasięg kupuje się
#: trafnością i odwrotnie, a która para jest do przyjęcia, rozstrzyga to, co
#: warstwa ma robić z odpowiedzią.
KRZYWA = ((2, 0.70), (2, 0.85), (3, 0.85), (5, 0.85), (5, 0.95))


def _kandydaci(rzeczownik: str, czasownik: str) -> list[tuple[str, str, list[str]]]:
    """Dwie strony wyboru jako kandydaci, tacy jak buduje je świadek nad werdyktem.

    Lematy idą tu wprost z banku drzew, a nie przez Morfeusza, bo anotator wybrał
    po jednym na formę. Ile wieloznaczność lematu dokłada świadkom nad żywym
    tekstem, jest osobnym pytaniem, i po stronie ramy pytaniem drugim: etykietę
    strony daje tu bank drzew, a nad werdyktem daje ją ``strona``, która czyta
    czytania formy.
    """
    return [
        (STRONA_IMIENNA, STRONA_IMIENNA, [rzeczownik]),
        (STRONA_CZASOWNIKOWA, STRONA_CZASOWNIKOWA, [czasownik]),
    ]


def _zmierz(świadkowie: Sequence[Pytany], testowe: Sequence[Wypadek]) -> Ocena:
    """Zasięg i trafność tej kolejności świadków nad tymi wypadkami.

    Kolejność, a nie jeden świadek, bo mierzy się tu warstwę, a nie tylko jej
    części: świadek postawiony przed drugim zabiera mu odpowiedzi, więc para
    trafności każdego z osobna nie mówi, co warstwa robi razem.
    Pierwszy odpowiadający wygrywa, tak samo jak w ``_pierwszy``
    w ``olski/rozstrzyganie.py``.
    """
    ocena = Ocena(wypadków=len(testowe))
    for przyimek, rzeczownik, czasownik, gospodarz in testowe:
        kandydaci = _kandydaci(rzeczownik, czasownik)
        for świadek in świadkowie:
            wybrany = świadek.wybierz(przyimek, kandydaci)
            if wybrany is not None:
                ocena.odpowiedzi += 1
                ocena.trafień += wybrany[0] == gospodarz
                break
    return ocena


def oceń(
    paths: Sequence[Path], krzywa: Sequence[tuple[int, float]] = KRZYWA
) -> tuple[list[tuple[int, float, Ocena]], list[tuple[str, Ocena]], Ocena]:
    """Zbuduj tabelę na połowie banku drzew i sprawdź na drugiej całą warstwę.

    Podział idzie po parzystości numeru pliku, a nie losowaniem, żeby ta sama
    komenda dwa razy dała tę samą liczbę. Obie połowy czyta się raz, a ustawienia
    przechodzi się po gotowych czwórkach, bo czytanie lasów jest tu całym kosztem.

    Wracają trzy rzeczy. Pierwszą jest krzywa świadka statystycznego, bo próg
    kupuje się zasięgiem i odwrotnie. Drugą są warianty świadka ramowego wraz ze
    złożeniem obu, bo świadek stojący przed drugim zabiera mu odpowiedzi i dopiero
    złożenie mówi, co warstwa robi razem. Trzecią jest ocena podłogi, czyli tego
    samego pomiaru dla reguły „zawsze do rzeczownika”: świadek, który podłogi nie
    pobija, nie kupuje niczego, bo nad tym korpusem rzeczownik bierze dwie trzecie
    wyborów (``docs/subset.md``).

    Świadka kontekstowego tu nie ma i nie jest to przeoczenie: jego dowodem jest
    akapit, a bank drzew wypadków w akapity nie układa.

    Podziału na połowy świadek ramowy nie potrzebuje, bo tabeli z banku drzew nie
    buduje, i mimo to mierzy się go na tej samej połowie: dwie liczby porównywalne
    mają pochodzić z jednego materiału.
    """
    najniższe = min(wsparcie for wsparcie, _ in krzywa)
    licznik = zbuduj(wypadki(paths[::2]), najniższe)
    testowe = wypadki(paths[1::2])

    podłoga = Ocena(wypadków=len(testowe), odpowiedzi=len(testowe))
    podłoga.trafień = sum(gospodarz == STRONA_IMIENNA for *_, gospodarz in testowe)

    krzywe = [
        (
            wsparcie,
            próg,
            _zmierz([Skłonność(licznik=licznik, wsparcie=wsparcie, próg=próg)], testowe),
        )
        for wsparcie, próg in krzywa
    ]
    tabela = Skłonność(licznik=licznik)
    #  Weto ma tu dwa wiersze, bo jego cena jest inna dla świadka i dla warstwy:
    #  sama rama traci przez nie odpowiedzi, a warstwa traci tylko te,
    #  na których tabela za ramą też milczy.
    warianty = [
        ("rama", _zmierz([Rama()], testowe)),
        ("rama bez weta", _zmierz([Rama(weto=False)], testowe)),
        ("rama, a za nią skłonność", _zmierz([Rama(), tabela], testowe)),
        ("rama bez weta, a za nią skłonność", _zmierz([Rama(weto=False), tabela], testowe)),
    ]
    return krzywe, warianty, podłoga


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.skłonności",
        description="Zbuduj albo oceń tabelę skłonności przyłączeniowych.",
    )
    parser.add_argument("root", help="katalog z rozpakowaną Składnicą")
    parser.add_argument("--zbuduj", type=Path, nargs="?", const=SKŁONNOŚCI, help="zapisz tabelę")
    parser.add_argument("--oceń", action="store_true", help="sprawdź świadka na drugiej połowie")
    parser.add_argument("--limit", type=int, help="zatrzymaj się po tylu lasach")
    parser.add_argument(
        "--wsparcie",
        type=int,
        default=WSPARCIE,
        help="ile wystąpień minimum trafia do budowanej tabeli; oceny nie rusza",
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"harness.skłonności: nie ma takiego katalogu: {root}", file=sys.stderr)
        print("harness.skłonności: skąd wziąć korpus, mówi docs/corpus.md", file=sys.stderr)
        return 2
    ścieżki = pliki(root)[: args.limit]
    if args.zbuduj:
        licznik = zbuduj(wypadki(ścieżki), args.wsparcie)
        zapisz(licznik, args.zbuduj)
        print(f"{len(licznik)} par o wsparciu co najmniej {args.wsparcie} → {args.zbuduj}")
    if args.oceń or not args.zbuduj:
        krzywe, warianty, podłoga = oceń(ścieżki)
        print(f"ocena na połowie, której świadek nie widział: {podłoga.wypadków} wyborów")
        print(f"  podłoga: zawsze do rzeczownika, trafia w {podłoga.trafność:.1%}")
        for wsparcie, próg, ocena in krzywe:
            print(
                f"  wsparcie {wsparcie}, próg {próg:.0%}: "
                f"odpowiada w {ocena.zasięg:>5.1%}, trafia w {ocena.trafność:>5.1%}"
            )
        for etykieta, ocena in warianty:
            print(
                f"  {etykieta}: "
                f"odpowiada w {ocena.zasięg:>5.1%}, trafia w {ocena.trafność:>5.1%}"
            )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
