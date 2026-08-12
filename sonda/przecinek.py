"""Ile kupuje i ile kosztuje koordynacja przecinkiem, zmierzone nad Składnicą.

``Clause``, ``NP`` i ``AP`` mają każde produkcję ze spójnikiem i produkcję z
przecinkiem. Pytanie nie brzmi, ile zdań te trzy przyjmują, bo to policzy każdy
przebieg ``olski-corpus``. Brzmi ono, ile zdań odbierają: przecinek między
zdaniami składowymi konkuruje z przecinkiem w grupie imiennej wszędzie tam,
gdzie po przecinku stoi rzeczownik, a zdanie, które przez to wychodzi dwoma
czytaniami, olski odrzuca. Zdanie odrzucone przez wieloznaczność jest droższe
niż zdanie, którego gramatyka nie wyprowadza wcale, bo tamto czeka na produkcję,
a to na jej wycofanie.

Sonda liczy więc nie stan gramatyki, tylko ruch: dla każdego zdania Składnicy
werdykt bez przecinka i werdykt z przecinkiem, i tabelę przejść między nimi.
Przejście ``przyjęte → wieloznaczne`` jest ceną, przejście
``odrzucone → przyjęte`` zakupem, a wariantów jest pięć, bo trzy poziomy
koordynacji da się zdejmować osobno i cena każdego z nich jest osobną liczbą.

Zdejmować, a nie dopisywać: mierzona jest gramatyka, która stoi, a wariantem
jest ta sama gramatyka z wyjętą produkcją. Wariant dopisywany mierzyłby produkcję
napisaną tutaj, czyli drugą deklarację tego samego, i rozszedłby się z olskim po
pierwszej zmianie, której nikt by tu nie powtórzył.

Wynik czyta ``docs/subset.md``. Sonda nie zmienia niczego w ``olski``: warianty
powstają przez przepisanie produkcji ze świeżej gramatyki z
``olski.subset.build`` do gramatyki uboższej, więc zależność biegnie w jedną
stronę tak samo jak w drugiej sondzie tego pakietu.

    python3 -m sonda.przecinek Składnica-frazowa-180723/
    python3 -m sonda.przecinek proza/README.txt
"""

from __future__ import annotations

import argparse
import collections
import functools
import os
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.corpus import Sentence, pliki, read
from olski.coverage import Outcome, po_kawałkach
from olski.grammar import Grammar, Production, Sym
from olski.parse import parse
from olski.subset import FRAGMENT, PRZECINEK, build, check

#: Ile zdań zachować pod każdym przejściem. Przejście bez przykładu jest liczbą,
#: o której nie wiadomo, co ją wywołało, a cena jest tu tym, co trzeba przeczytać.
PRZYKŁADY = 8

#: Powyżej tego zdanie nie wchodzi, tak samo jak w ``olski-corpus``: enumerator
#: nie ma na nie budżetu, a granica postawiona tu inaczej dałaby mianownik
#: nieporównywalny z tabelami ``docs/corpus.md``.
MAX_TOKENS = 40

#: Poziom koordynacji → symbol, którego produkcje go niosą. Poziom nazywa się z
#: polska, bo jest nazwą wariantu w wydruku, a symbol stoi po angielsku razem z
#: całą gramatyką.
POZIOMY = {"zdaniowy": "Clause", "imienny": "NP", "przymiotnikowy": "AP"}

#: Warianty w kolejności wydruku. Pierwszy zdejmuje przecinek zewsząd i jest
#: mianownikiem, wobec którego liczone są przejścia; ostatni nie zdejmuje nic i
#: jest gramatyką, która stoi, więc dopiero on pokazuje konkurencję między
#: poziomami, o którą w tej sondzie chodzi.
WARIANTY = ("bez", *POZIOMY, "wszystkie")


def _przecinkowa(produkcja: Production) -> bool:
    """Czy produkcja jest tą, którą przecinek wnosi jako znak koordynacji.

    Pytanie stawiane produkcji, a nie liście nazw obok gramatyki: przecinek
    dopisany kiedyś na czwartym poziomie wchodzi tu sam, a lista obok
    przemilczałaby go i sonda mierzyłaby dalej trzy.

    Sam przecinek w ciele na to nie odpowiada, bo polszczyzna stawia go i tam,
    gdzie nic się nie koordynuje: zdanie względne otwiera nim swoją granicę.
    Ciąg współrzędny poznaje się po tym, że symbol stoi nad sobą, i tak samo
    poznaje go werdykt (``_koordynuje`` w ``olski/parse.py``). Zdjęta produkcja
    podrzędna zostawiłaby ponadto symbol bez ani jednego ciała, a gramatyka z
    symbolem nieokreślonym nie rozbiera niczego.
    """
    return PRZECINEK in produkcja.body and any(
        isinstance(część, Sym) and część.name == produkcja.head for część in produkcja.body
    )


@functools.cache
def gramatyka(wariant: str) -> Grammar:
    """Gramatyka olskiego bez tych produkcji z przecinkiem, których ten wariant nie ma.

    Budowana raz na proces roboczy, bo budowa jest droższa niż rozbiór jednego
    zdania, a gramatyka po zbudowaniu się nie zmienia.
    """
    if wariant not in WARIANTY:
        raise ValueError(f"nieznany wariant: {wariant}")
    zostają = {POZIOMY[wariant]} if wariant in POZIOMY else set()
    pełna = build()
    okrojona = Grammar(start=pełna.start)
    for produkcja in pełna.productions:
        if wariant != "wszystkie" and _przecinkowa(produkcja) and produkcja.head not in zostają:
            continue
        okrojona.dopisz(produkcja)
    return okrojona


@dataclass
class Raport:
    """Liczniki jednego przebiegu, wraz ze zdaniami, które je czynią czytelnymi."""

    #: Ile zdań zachować pod każdym przejściem. Stoi przy licznikach, a nie przy
    #: każdym wołaniu, bo jest tym samym przez cały przebieg i przy scalaniu.
    ile_przykładów: int = PRZYKŁADY
    #: Wariant → ile zdań wyszło którym werdyktem.
    stany: dict[str, collections.Counter] = field(default_factory=dict)
    #: Wariant → ile zdań przeszło z którego werdyktu na który.
    przejścia: dict[str, collections.Counter] = field(default_factory=dict)
    #: (wariant, przejście) → zdania, na których to przejście widać.
    przykłady: dict[tuple[str, str], list[str]] = field(default_factory=dict)
    #: Wariant → jak role zdań nowo przyjętych mają się do drzewa wzorcowego.
    #: Zdanie przyjęte odwrotnie niż w banku drzew nie jest zakupem.
    zgodność: dict[str, collections.Counter] = field(default_factory=dict)
    #: Czy poziomy koordynacji wchodzą sobie w drogę. Pytanie, po które ta sonda
    #: stoi: przecinek między zdaniami składowymi miałby konkurować z przecinkiem
    #: w grupie imiennej, a konkurencja widać po zdaniu, które oba poziomy
    #: ruszają, i po zdaniu, o którym oba naraz mówią co innego niż każdy osobno.
    konkurencja: collections.Counter = field(default_factory=collections.Counter)
    #: Zdania, których nie zmierzono, po powodzie. Wypisane, a nie odjęte po
    #: cichu, bo mianownik bez nich byłby mianownikiem zdań łatwych.
    pominięte: collections.Counter = field(default_factory=collections.Counter)

    @property
    def zmierzone(self) -> int:
        return sum(self.stany.get("bez", collections.Counter()).values())

    def zapisz(
        self,
        tekst: str,
        stany: dict[str, str],
        role: dict[str, str | None],
    ) -> None:
        """Zapisz jedno zdanie: werdykt pod każdym wariantem i role pod nowo przyjętym.

        Werdykt jest tu napisem, a nie wynikiem rozbioru, bo zdanie przychodzi z
        dwóch korpusów naraz: z banku drzew, gdzie niesie drzewo wzorcowe, i z
        prozy, gdzie nie niesie żadnego. Role przychodzą więc obok werdyktu i nad
        prozą stoją puste, zamiast rozdwajać ten licznik na dwa.
        """
        mianownik = stany["bez"]
        for wariant, stan in stany.items():
            self.stany.setdefault(wariant, collections.Counter())[stan] += 1
            if wariant == "bez" or stan == mianownik:
                continue
            przejście = f"{mianownik} → {stan}"
            self.przejścia.setdefault(wariant, collections.Counter())[przejście] += 1
            self.zanotuj((wariant, przejście), tekst)
            if stan == "valid" and wariant in role:
                zgoda = role[wariant] or "brak roli"
                self.zgodność.setdefault(wariant, collections.Counter())[zgoda] += 1
        self._konkurencja(tekst, stany, mianownik)

    def _konkurencja(self, tekst: str, stany: dict[str, str], mianownik: str) -> None:
        """Policz, czy poziomy koordynacji wchodzą sobie w drogę na tym zdaniu.

        Dwa pytania, bo konkurencja ma dwa stopnie. Zdanie, które rusza się pod
        jednym poziomem i pod drugim, jest zdaniem, o które poziomy się spierają.
        Zdanie, o którym oba naraz mówią co innego, niż mówi którykolwiek z nich
        osobno, jest zdaniem, na którym ten spór coś kosztuje: dwie produkcje
        dały mu czytanie, którego żadna z nich nie dała.
        """
        ruszone = {poziom: stany[poziom] for poziom in POZIOMY if stany[poziom] != mianownik}
        if len(ruszone) >= 2:
            self._policz("oba poziomy ruszają to samo zdanie", tekst)
        if stany["wszystkie"] not in {mianownik, *ruszone.values()}:
            self._policz("razem wychodzi co innego niż osobno", tekst)

    def _policz(self, nazwa: str, tekst: str) -> None:
        self.konkurencja[nazwa] += 1
        self.zanotuj(("konkurencja", nazwa), tekst)

    def zanotuj(self, klucz: tuple[str, str], tekst: str) -> None:
        """Zachowaj zdanie pod kluczem, dopóki mieści się w budżecie przykładów."""
        zachowane = self.przykłady.setdefault(klucz, [])
        if len(zachowane) < self.ile_przykładów:
            zachowane.append(tekst)


def zmierz(
    zdania: Iterable[Sentence],
    przykłady: int = PRZYKŁADY,
    max_tokens: int | None = MAX_TOKENS,
) -> Raport:
    """Przepuść zdania przez każdy wariant i policz, co się między nimi rusza."""
    raport = Raport(przykłady)
    for zdanie in zdania:
        if not zdanie.annotated:
            continue
        if max_tokens is not None and len(zdanie.segments) > max_tokens:
            raport.pominięte[f"dłuższe niż {max_tokens} segmentów"] += 1
            continue
        segmenty = list(zdanie.segments)
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        wyniki = {
            wariant: Outcome(
                sentence=zdanie,
                result=parse(gramatyka(wariant), segmenty),
                segments=tuple(segmenty),
            )
            for wariant in WARIANTY
        }
        raport.zapisz(
            zdanie.text,
            {wariant: wynik.status for wariant, wynik in wyniki.items()},
            {wariant: wynik.agreement for wariant, wynik in wyniki.items()},
        )
    return raport


def nad_prozą(tekst: str, przykłady: int = PRZYKŁADY) -> Raport:
    """To samo porównanie nad prozą, którą olski ma czytać.

    Bank drzew rankinguje konstrukcje w rejestrze, którego olski nie ma, i mówi
    przez to, ile przecinek kupuje w cudzej polszczyźnie. Drugie pytanie jest o
    rejestr własny i pada tu: ile kupuje w dokumentacji technicznej. Ról nie ma
    czym porównać, bo drzewa wzorcowego proza nie niesie, a fragment nie jest
    zdaniem i do mianownika nie wchodzi.
    """
    raport = Raport(przykłady)
    wyniki = {wariant: check(tekst, gramatyka(wariant)) for wariant in WARIANTY}
    for kolejne in zip(*wyniki.values(), strict=True):
        werdykty = dict(zip(WARIANTY, kolejne, strict=True))
        if werdykty["bez"].status == FRAGMENT:
            raport.pominięte["fragment, a nie zdanie"] += 1
            continue
        raport.zapisz(
            werdykty["bez"].text,
            {wariant: werdykt.status for wariant, werdykt in werdykty.items()},
            {},
        )
    return raport


def _kawałek(ścieżki: Sequence[Path], przykłady: int, max_tokens: int | None) -> Raport:
    return zmierz((read(ścieżka) for ścieżka in ścieżki), przykłady, max_tokens)


def przebieg(
    ścieżki: Sequence[Path],
    jobs: int,
    przykłady: int = PRZYKŁADY,
    max_tokens: int | None = MAX_TOKENS,
) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport.

    Podział na kawałki jest ten sam, którym idzie ``olski-corpus``, i stoi tam,
    bo decyzja o jego rozmiarze jest jedna. Składanie zostaje tutaj, bo licznik,
    który z kawałka wraca, jest licznikiem tej sondy.
    """
    praca = functools.partial(_kawałek, przykłady=przykłady, max_tokens=max_tokens)
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden.

    Kawałki są odcinkami jednej posortowanej listy plików i wchodzą tu w jej
    kolejności, więc scalony raport jest tym samym raportem, co z jednego
    przebiegu nad całością, przykłady włącznie.
    """
    scalony = Raport(przykłady)
    for raport in raporty:
        for wariant, licznik in raport.stany.items():
            scalony.stany.setdefault(wariant, collections.Counter()).update(licznik)
        for wariant, licznik in raport.przejścia.items():
            scalony.przejścia.setdefault(wariant, collections.Counter()).update(licznik)
        for wariant, licznik in raport.zgodność.items():
            scalony.zgodność.setdefault(wariant, collections.Counter()).update(licznik)
        scalony.konkurencja.update(raport.konkurencja)
        scalony.pominięte.update(raport.pominięte)
        for klucz, zachowane in raport.przykłady.items():
            for tekst in zachowane:
                scalony.zanotuj(klucz, tekst)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #

#: Werdykty w kolejności, w jakiej stoją w tabeli.
STANY = ("valid", "ambiguous", "rejected")

#: Pytania o konkurencję poziomów, w kolejności wydruku i niezależnie od tego,
#: czy któreś zdanie na nie odpowiedziało.
KONKURENCJA = ("oba poziomy ruszają to samo zdanie", "razem wychodzi co innego niż osobno")


def wydruk(raport: Raport, nagłówek: str) -> str:
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań",
        "",
        f"{'wariant':>16}  {'przyjęte':>10} {'wieloznaczne':>13} {'odrzucone':>10}",
    ]
    for wariant in WARIANTY:
        licznik = raport.stany.get(wariant, collections.Counter())
        przyjęte, wieloznaczne, odrzucone = (licznik.get(stan, 0) for stan in STANY)
        wiersze.append(
            f"{wariant:>16}  {przyjęte:>10} {wieloznaczne:>13} {odrzucone:>10}"
        )
    for powód, ile in raport.pominięte.most_common():
        wiersze.append(f"{ile:>7}          niezmierzone: {powód}")

    for wariant in WARIANTY[1:]:
        przejścia = raport.przejścia.get(wariant)
        wiersze += ["", f"ruch wobec wariantu bez przecinka — {wariant}:"]
        if not przejścia:
            wiersze.append("  żadne zdanie nie zmieniło werdyktu")
            continue
        for przejście, ile in przejścia.most_common():
            wiersze.append(f"  {ile:>7}  {przejście}")
        zgodność = raport.zgodność.get(wariant)
        if zgodność:
            wiersze.append("  role zdań nowo przyjętych wobec drzewa wzorcowego:")
            for nazwa, ile in zgodność.most_common():
                wiersze.append(f"  {ile:>7}    {nazwa}")

    # Zero wypisane, a nie pominięte: liczba, której nie ma, czyta się jak
    # pomiar, którego nie było, a to jest ta liczba, po którą sonda stoi.
    wiersze += ["", "konkurencja poziomów, nad zdaniem po zdaniu:"]
    for nazwa in KONKURENCJA:
        wiersze.append(f"  {raport.konkurencja.get(nazwa, 0):>7}  {nazwa}")

    for nazwa in KONKURENCJA:
        zachowane = raport.przykłady.get(("konkurencja", nazwa), [])
        if zachowane:
            wiersze += ["", f"konkurencja, {nazwa}:"]
            wiersze += [f"  {tekst}" for tekst in zachowane]

    for wariant in WARIANTY[1:]:
        for przejście, _ in raport.przejścia.get(wariant, collections.Counter()).most_common():
            zachowane = raport.przykłady.get((wariant, przejście), [])
            if not zachowane:
                continue
            wiersze += ["", f"{wariant}, {przejście}:"]
            wiersze += [f"  {tekst}" for tekst in zachowane]

    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m sonda.przecinek",
        description="Ile koordynacja przecinkiem kupuje i ile kosztuje.",
    )
    parser.add_argument(
        "ścieżka",
        help="katalog z rozpakowaną Składnicą albo plik z prozą do przeczytania",
    )
    parser.add_argument("--limit", type=int, help="zatrzymaj się po tylu lasach")
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=MAX_TOKENS,
        help="pomiń zdania dłuższe niż tyle segmentów",
    )
    parser.add_argument(
        "--przykłady", type=int, default=PRZYKŁADY, help="ile zdań pokazać pod przejściem"
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=os.cpu_count() or 1,
        help="ile procesów czyta i mierzy; 1 liczy w tym",
    )
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs bierze co najmniej jeden proces")

    ścieżka = Path(args.ścieżka)
    if ścieżka.is_dir():
        raport = przebieg(
            pliki(ścieżka)[: args.limit],
            args.jobs,
            przykłady=args.przykłady,
            max_tokens=args.max_tokens,
        )
        print(wydruk(raport, "Składnica, morfologia złota"))
        return 0
    if ścieżka.is_file():
        print(wydruk(nad_prozą(ścieżka.read_text(), args.przykłady), f"{ścieżka.name}, proza"))
        return 0
    print(f"sonda.przecinek: nie ma takiego katalogu ani pliku: {ścieżka}", file=sys.stderr)
    print("sonda.przecinek: docs/corpus.md mówi, skąd wziąć korpus", file=sys.stderr)
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
