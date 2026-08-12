"""Ile pozycji rozdziela rozszczepienie po cechach, zmierzone nad dwoma korpusami.

Werdykt ma wyjść z lasu ze współdzielonymi węzłami, a wtedy liczba czytań jest
sumą iloczynów po pozycjach tablicy, a nie długością listy drzew. Suma ta liczy
jednak pary, których unifikacja nie przepuszcza, bo rodzic wskazuje pozycję, a
nie wyprowadzenie pod nią. Naprawą, którą ta sonda odrzuca, jest pozycja
rozszczepiona po cechach, które wypuszcza: rozszczepienie kosztuje pozycje, a
myli się częściej niż to, co ma naprawiać. Wywód, wybór, jaki po nim zostaje, i
liczby stąd wzięte trzyma
docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania.

Nad każdym zdaniem staje więc ta sama tablica w dwóch wariantach, a wydruk mówi
trzy rzeczy: ile pozycji przybywa od rozszczepienia, ile czytań każdy wariant
naliczył ponad wyliczone przez ``olski.parse``, i na ilu zdaniach ten nadmiar
przewraca werdykt. Wyliczenie jest tu miarą, bo środowisko cech niesie w dół
rozbioru zamiast pod pozycją, więc pary nieunifikującej się nie policzy.

Sonda nie zmienia niczego w ``olski``: tablicę buduje ``wyprowadzenia`` z
``olski.parse``, a warianty powstają z niej tutaj, tak samo jak w pozostałych
sondach tego pakietu.

    python3 -m sonda.pakowanie Składnica-frazowa-180723/
    python3 -m sonda.pakowanie Składnica-frazowa-180723/ --morphology gold
    python3 -m sonda.pakowanie proza/README.txt
"""

from __future__ import annotations

import argparse
import collections
import functools
import math
import os
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.corpus import Sentence, pliki, read
from olski.coverage import SOURCES, po_kawałkach, segments_for
from olski.morph import Segment
from olski.parse import Leaf, Node, Tree, parse, wyprowadzenia
from olski.subset import FRAGMENT, GRAMMAR, check, morphology

#: Ile zdań zachować pod każdym pytaniem. Liczba bez zdania obok mówi, że coś
#: się dzieje, i nie mówi co, a tu trzeba przeczytać, na czym nadmiar stanął.
PRZYKŁADY = 8

#: Powyżej tego zdanie nie wchodzi, tak samo jak w ``olski-corpus``: enumerator
#: nie ma na nie budżetu, a granica postawiona tu inaczej dałaby mianownik
#: nieporównywalny z tabelami ``docs/corpus.md``.
MAX_TOKENS = 40

#: Warianty tablicy w kolejności wydruku. Pierwszy pakuje po kształcie i jest
#: tym, co las daje z siebie sam; drugi rozszczepia pozycję po cechach, które
#: wypuszcza, i jest tą naprawą, którą ten pomiar odrzucił.
WARIANTY = ("spakowany", "rozszczepiony")

#: Etykieta liścia, czyli ta, której liść nie ma: czytaniem liścia jest sama
#: rozpiętość, bo części mowy ``Leaf.signature`` nie niesie. Pusta na tym miejscu
#: odróżnia klucz liścia od klucza konstytuenta bez pytania o długość krotki.
LIŚĆ = None


def _pozycja(tree: Tree, wariant: str):
    """Pozycja tablicy, w której ten konstytuent stoi."""
    if isinstance(tree, Leaf):
        return (LIŚĆ, tree.span)
    if wariant == "rozszczepiony":
        return (tree.label, tree.span, tree.features)
    return (tree.label, tree.span)


def tablica(zbudowane: Iterable[Node], wariant: str) -> dict:
    """Pozycja → jej wyprowadzenia, każde nazwane samymi pozycjami swoich córek.

    Tym pakowanie jest: dwa wyprowadzenia różne w środku, a nazwane tak samo,
    zlewają się w jedno i las przestaje rosnąć iloczynem. Nazwane tak samo znaczy
    tu „o tych samych córkach”, bo sygnatura czytania schodzi rekurencyjnie do
    sygnatur córek, a te są tym, czym pozycja córki jest.
    """
    pozycje: dict = {}
    for node in zbudowane:
        córki = tuple(_pozycja(child, wariant) for child in node.children)
        pozycje.setdefault(_pozycja(node, wariant), set()).add(córki)
    return pozycje


def ile_czytań(pozycje: dict, segmenty: Sequence[Segment], start: str) -> int:
    """Suma iloczynów po tej tablicy: ile czytań las z niej podaje.

    Korzeniem jest pozycja symbolu startowego sięgająca przez całe zdanie, a w
    wariancie rozszczepionym jest ich kilka, bo i korzeń rozdziela to, co
    wypuszcza, i czytania rozkładają się wtedy między nie.

    Cyklu ta rekurencja nie potrzebuje pilnować, bo pozycja o tym samym początku
    nie może stać sama pod sobą: gramatyka nie ma produkcji o pustym ciele, więc
    cykl w tablicy byłby lewą rekursją, a tę ``olski.parse`` wykrywa i zgłasza
    przed tym wyliczeniem.
    """
    rozpiętość = (
        min((segment.start for segment in segmenty), default=0),
        max((segment.end for segment in segmenty), default=0),
    )
    policzone: dict = {}

    def ile_pod(klucz) -> int:
        if klucz[0] is LIŚĆ:
            return 1
        if klucz in policzone:
            return policzone[klucz]
        ile = sum(math.prod(map(ile_pod, córki)) for córki in pozycje[klucz])
        policzone[klucz] = ile
        return ile

    return sum(
        ile_pod(klucz) for klucz in pozycje if klucz[0] == start and klucz[1] == rozpiętość
    )


def _stan(ile: int) -> str:
    """Werdykt, jaki taka liczba czytań daje, nazwany tak jak w ``Result.status``."""
    if ile == 1:
        return "valid"
    return "ambiguous" if ile > 1 else "rejected"


@dataclass
class Raport:
    """Liczniki jednego przebiegu, wraz ze zdaniami, które je czynią czytelnymi."""

    #: Ile zdań zachować pod każdym pytaniem. Stoi przy licznikach, a nie przy
    #: każdym wołaniu, bo jest tym samym przez cały przebieg i przy scalaniu.
    ile_przykładów: int = PRZYKŁADY
    #: Ile zdań weszło do mianownika.
    zmierzone: int = 0
    #: Wariant → ile pozycji tablice tych zdań mają razem.
    pozycje: collections.Counter = field(default_factory=collections.Counter)
    #: Na ile pozycji rozszczepienie rozdziela pozycję spakowaną → ile pozycji
    #: rozdziela się właśnie na tyle. Jest to cena rozszczepienia, a to, czy je
    #: kupić, rozstrzygają dopiero `liczby` niżej.
    rozdzielone: collections.Counter = field(default_factory=collections.Counter)
    #: Wariant → jak liczba czytań z tablicy ma się do wyliczonej.
    liczby: dict[str, collections.Counter] = field(default_factory=dict)
    #: Wariant → werdykt wyliczony i werdykt z tablicy, gdy się różnią.
    werdykty: dict[str, collections.Counter] = field(default_factory=dict)
    #: (pytanie, wariant) → zdania, na których to widać.
    przykłady: dict[tuple[str, str], list[str]] = field(default_factory=dict)
    #: Zdania, których nie zmierzono, po powodzie. Wypisane, a nie odjęte po
    #: cichu, bo mianownik bez nich byłby mianownikiem zdań łatwych.
    pominięte: collections.Counter = field(default_factory=collections.Counter)

    def zapisz(self, tekst: str, wyliczone: int, urwane: bool, z_tablicy: dict[str, int]) -> None:
        """Zapisz jedno zdanie: ile czytań wyliczono i ile podaje każdy wariant tablicy."""
        self.zmierzone += 1
        for wariant, ile in z_tablicy.items():
            liczby = self.liczby.setdefault(wariant, collections.Counter())
            if urwane:
                # Wyliczanie stanęło na ``MAX_READINGS``, więc nie ma z czym
                # porównywać: tablica liczy bez granicy, a lista czytań z granicą.
                liczby["urwane na MAX_READINGS"] += 1
            elif ile == wyliczone:
                liczby["zgadza się"] += 1
            else:
                nazwa = "liczy więcej" if ile > wyliczone else "liczy mniej"
                liczby[nazwa] += 1
                self.zanotuj((nazwa, wariant), f"{ile} zamiast {wyliczone}: {tekst}")
            stan, wyliczony = _stan(ile), _stan(wyliczone)
            if stan != wyliczony:
                przejście = f"{wyliczony} → {stan}"
                self.werdykty.setdefault(wariant, collections.Counter())[przejście] += 1
                self.zanotuj(("werdykt", wariant), f"{przejście}: {tekst}")

    def zanotuj(self, klucz: tuple[str, str], tekst: str) -> None:
        """Zachowaj zdanie pod kluczem, dopóki mieści się w budżecie przykładów."""
        zachowane = self.przykłady.setdefault(klucz, [])
        if len(zachowane) < self.ile_przykładów:
            zachowane.append(tekst)


def nad_zdaniem(raport: Raport, tekst: str, segmenty: list[Segment]) -> None:
    """Zbuduj tablicę tego zdania w obu wariantach i dopisz, co je różni.

    Wyliczenie idzie osobno od tablicy, choć jedno i drugie rozbiera to samo
    zdanie. Tablica jest tu mierzona, więc liczba, wobec której się ją mierzy,
    nie może z niej pochodzić.
    """
    zbudowane = wyprowadzenia(GRAMMAR, segmenty)
    tablice = {wariant: tablica(zbudowane, wariant) for wariant in WARIANTY}

    rozdział: collections.Counter = collections.Counter()
    for etykieta, rozpiętość, _cechy in tablice["rozszczepiony"]:
        rozdział[(etykieta, rozpiętość)] += 1
    for wariant, pozycje in tablice.items():
        raport.pozycje[wariant] += len(pozycje)
    for spakowana in tablice["spakowany"]:
        raport.rozdzielone[rozdział[spakowana]] += 1

    wynik = parse(GRAMMAR, segmenty)
    raport.zapisz(
        tekst,
        len(wynik.readings),
        wynik.truncated,
        {
            wariant: ile_czytań(pozycje, segmenty, GRAMMAR.start)
            for wariant, pozycje in tablice.items()
        },
    )


def zmierz(
    zdania: Iterable[Sentence],
    source: str = "live",
    przykłady: int = PRZYKŁADY,
    max_tokens: int | None = MAX_TOKENS,
) -> Raport:
    """Przepuść zdania banku drzew przez obie tablice i policz, co je różni.

    Morfologia domyślna jest tu inna niż w ``olski-corpus``, i to nie jest
    niedopatrzenie. Nadmiar, o który sonda pyta, bierze się z formy, której
    słownik daje kilka czytań, a złota morfologia takiej formy nie ma:
    anotatorzy wybrali po jednym czytaniu na terminal, więc pod nią pozycja
    rozszczepia się prawie nigdzie i pomiar mówiłby o anotacji, a nie o
    gramatyce. Wariant złoty zostaje osiągalny flagą, bo ta różnica jest sama w
    sobie liczbą wartą wydrukowania.
    """
    if source not in SOURCES:
        raise ValueError(f"nieznane źródło morfologii: {source}")
    raport = Raport(przykłady)
    for zdanie in zdania:
        if not zdanie.annotated:
            continue
        if max_tokens is not None and len(zdanie.segments) > max_tokens:
            raport.pominięte[f"dłuższe niż {max_tokens} segmentów"] += 1
            continue
        segmenty = segments_for(zdanie, source)
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        nad_zdaniem(raport, zdanie.text, segmenty)
    return raport


def nad_prozą(tekst: str, przykłady: int = PRZYKŁADY) -> Raport:
    """To samo nad prozą, którą olski ma czytać.

    Bank drzew mierzy tablicę nad cudzą polszczyzną, a rejestr własny mierzy
    dopiero to: nadmiar bierze się z formy, której słownik daje dwa czytania, a
    tych form dokumentacja techniczna ma inne niż gazeta. Fragment nie jest
    zdaniem i do mianownika nie wchodzi.
    """
    raport = Raport(przykłady)
    for werdykt in check(tekst):
        if werdykt.status == FRAGMENT:
            raport.pominięte["fragment, a nie zdanie"] += 1
            continue
        nad_zdaniem(raport, werdykt.text, morphology(werdykt.text))
    return raport


def _kawałek(
    ścieżki: Sequence[Path], source: str, przykłady: int, max_tokens: int | None
) -> Raport:
    return zmierz((read(ścieżka) for ścieżka in ścieżki), source, przykłady, max_tokens)


def przebieg(
    ścieżki: Sequence[Path],
    jobs: int,
    source: str = "live",
    przykłady: int = PRZYKŁADY,
    max_tokens: int | None = MAX_TOKENS,
) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport."""
    praca = functools.partial(
        _kawałek, source=source, przykłady=przykłady, max_tokens=max_tokens
    )
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden.

    Kawałki są odcinkami jednej posortowanej listy plików i wchodzą tu w jej
    kolejności, więc scalony raport jest tym samym raportem, co z jednego
    przebiegu nad całością, przykłady włącznie.
    """
    scalony = Raport(przykłady)
    for raport in raporty:
        scalony.zmierzone += raport.zmierzone
        scalony.pozycje.update(raport.pozycje)
        scalony.rozdzielone.update(raport.rozdzielone)
        scalony.pominięte.update(raport.pominięte)
        for wariant, licznik in raport.liczby.items():
            scalony.liczby.setdefault(wariant, collections.Counter()).update(licznik)
        for wariant, licznik in raport.werdykty.items():
            scalony.werdykty.setdefault(wariant, collections.Counter()).update(licznik)
        for klucz, zachowane in raport.przykłady.items():
            for tekst in zachowane:
                scalony.zanotuj(klucz, tekst)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #

#: Pytania o nadmiar w kolejności wydruku i niezależnie od tego, czy któreś
#: zdanie na nie odpowiedziało. Zero wypisane, a nie pominięte: liczba, której
#: nie ma, czyta się jak pomiar, którego nie było.
#:
#: „Liczy mniej” zera nigdy nie opuszcza i stoi tu jako sprawdzian samej sondy:
#: każde czytanie ma w tablicy wyprowadzenie, więc suma iloczynów jest
#: oszacowaniem od góry i wiersz niezerowy znaczy, że to sonda się myli.
NADMIAR = ("liczy więcej", "liczy mniej", "zgadza się", "urwane na MAX_READINGS")


def wydruk(raport: Raport, nagłówek: str) -> str:
    spakowane = raport.pozycje.get("spakowany", 0)
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań",
        "",
        "pozycje tablicy, zsumowane po zdaniach:",
    ]
    for wariant in WARIANTY:
        ile = raport.pozycje.get(wariant, 0)
        mierzony = spakowane and wariant != "spakowany"  # mianownik przy sobie samym nic nie mówi
        krotność = f"  ({ile / spakowane:.2f}× spakowanej)" if mierzony else ""
        wiersze.append(f"  {ile:>9}  {wariant}{krotność}")
    for powód, ile in raport.pominięte.most_common():
        wiersze.append(f"  {ile:>9}  niezmierzone: {powód}")

    wiersze += ["", "na ile pozycji rozszczepienie rozdziela pozycję spakowaną:"]
    for na_ile in sorted(raport.rozdzielone):
        ile = raport.rozdzielone[na_ile]
        udział = f"  ({ile / spakowane:.4f})" if spakowane else ""
        wiersze.append(f"  {ile:>9}  na {na_ile}{udział}")

    for wariant in WARIANTY:
        wiersze += ["", f"liczba czytań z tablicy wobec wyliczonej — {wariant}:"]
        licznik = raport.liczby.get(wariant, collections.Counter())
        for nazwa in NADMIAR:
            wiersze.append(f"  {licznik.get(nazwa, 0):>9}  {nazwa}")
        przejścia = raport.werdykty.get(wariant)
        wiersze.append(f"  {sum(przejścia.values()) if przejścia else 0:>9}  werdykt inny")
        for przejście, ile in sorted((przejścia or {}).items()):
            wiersze.append(f"  {ile:>9}    {przejście}")

    # Nagłówki brane z tego, co się zachowało, a nie z listy obok: lista byłaby
    # drugim wyliczeniem pytań, które zadaje `Raport.zapisz`.
    for (pytanie, wariant), zachowane in sorted(raport.przykłady.items()):
        wiersze += ["", f"{wariant}, {pytanie}:"]
        wiersze += [f"  {tekst}" for tekst in zachowane]
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="sonda.pakowanie",
        description="Zmierz, ile pozycji tablicy rozdziela rozszczepienie po cechach.",
    )
    parser.add_argument("ścieżki", nargs="+", help="katalog Składnicy albo pliki polskiej prozy")
    parser.add_argument(
        "--jobs",
        type=int,
        default=os.cpu_count() or 1,
        help="ile procesów liczy bank drzew (domyślnie tyle, ile rdzeni)",
    )
    parser.add_argument(
        "--przykłady",
        type=int,
        default=PRZYKŁADY,
        dest="przyklady",
        help=f"ile zdań pokazać pod każdym pytaniem (domyślnie {PRZYKŁADY})",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=MAX_TOKENS,
        help=f"powyżej tylu segmentów zdanie nie wchodzi (domyślnie {MAX_TOKENS})",
    )
    parser.add_argument(
        "--morphology",
        choices=SOURCES,
        default="live",
        help="czytania, jakie bank drzew dostaje: własne albo złote",
    )
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs bierze co najmniej jeden proces")

    for surowa in args.ścieżki:
        ścieżka = Path(surowa)
        if ścieżka.is_dir():
            raport = przebieg(
                pliki(ścieżka), args.jobs, args.morphology, args.przyklady, args.max_tokens
            )
            nagłówek = f"{surowa} — morfologia {args.morphology}"
        else:
            raport = nad_prozą(ścieżka.read_text(encoding="utf-8"), args.przyklady)
            nagłówek = surowa
        print(wydruk(raport, nagłówek))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
