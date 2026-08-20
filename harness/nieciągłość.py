"""Ilu zdaniom nieciągłość jest potrzebna, ile kosztuje i co ukrywa, nad Składnicą.

Wielkie rozwidlenie pytało, czy olski wpuszcza konstytuent nieciągły, i żądało
odpowiedzi z pomiaru, a nie z gustu. Pomiar ma trzy części, bo jednoznaczność
jest tu warunkiem poprawności: konstrukcja kupuje zdania, płaci zdaniami, a
odmowa jej kosztuje osobno i w drugą stronę.

**Potrzeba.** Świgra, gramatyka, z której powstała Składnica, ma nieciągłość jako
nieterminal ``ξ``: fraza postawiona przy zdaniu, a wymagana przez coś w jego
środku. Drzewo wzorcowe z takim węzłem jest więc zdaniem, któremu polszczyzna
kazała przestawiać, i zdaniem, którego analizę zatwierdził człowiek, wybierając to
drzewo z lasu. Sonda liczy te drzewa i pyta olskiego, co o tych zdaniach mówi,
bo potrzeba zakupem nie jest: konstrukcja, która nie jest ich najbliższym
blokerem, nie kupuje ich, choćby ją dopisać.

**Cena.** Zdanie, które ma dokładnie jedno czytanie, po zdjęciu spójności ma tyle
czytań, ile miejsc, w których wolno zawiesić przymiotnik, przyimek i dopełniacz —
a wolno wszędzie, bo bez spójności między frazą a jej gospodarzem nie musi już nic
stać. Sonda przepuszcza więc zdania przyjęte przez olskiego przez podłoże więzowe
dwa razy, ze spójnością i bez niej, i liczy tabelę przejść między werdyktami.

Cena idzie po podłożu z ``harness/wiezy.py``, a nie po gramatyce olskiego, bo
spójność da się zdjąć tylko tam: produkcja wyprowadza jeden odcinek tekstu i
zdjąć tego nie umie, a podłoże ma spójność jednym więzem globalnym. Kosztuje to
tyle, że podłoże jest deklaracją węższą od gramatyki i odrzuca część zdań, które
olski przyjmuje, więc mianownikiem ceny jest przecięcie obu, wypisane w tabeli.

**Maskowanie.** Odmowa nieciągłości ma cenę własną, o którą tamte dwie liczby nie
pytają: zdanie, którego drugie czytanie potrzebuje szczeliny, wychodzi olskiemu
jednoznaczne, więc ``valid`` obiecuje jedno czytanie zdaniu, które ma dwa. Sonda
liczy takie zdania osobno od tych, którym szczelinę wybrano, bo to dwa różne
pytania nad tym samym plikiem: tam nieciągłość jest czytaniem właściwym, a tutaj
drugim z dwóch.

Wynik czyta ``docs/design-notes.md``, gdzie stoi też to, na co nie odpowiada.

    python3 -m harness.nieciągłość Składnica-frazowa-180723/
"""

from __future__ import annotations

import argparse
import collections
import functools
import os
import re
import signal
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.polszczyzna import GRAMATYKA
from harness.wiezy import rozbierz
from olski.corpus import constituents, parse_forest, pliki, read_forest
from olski.coverage import Outcome, po_kawałkach, segments_for
from olski.parse import parse
from olski.subset import GRAMMAR

#: Nieterminal, którym Świgra zapisuje frazę stojącą przy zdaniu, a wymaganą przez
#: coś w jego środku. Kategoria, a nie cecha, więc widać ją w drzewie wzorcowym.
SZCZELINA = "ξ"

#: Ta sama kategoria szukana w pliku, czyli razem z czytaniami, których annotator
#: nie wybrał. Po bajtach, bo ``read_forest`` te węzły wycina, a właśnie one są
#: tu populacją; wzorzec czyta ten format tak samo, jak czyta go ``NIEWYBRANY``
#: w ``olski/corpus.py``. Kosztuje to drugi odczyt pliku i tyle: rozbiór lasu
#: nieokrojonego jest droższy, a las okrojony na to pytanie nie odpowiada.
SZCZELINA_W_LESIE = re.compile(f"<category>{SZCZELINA}</category>".encode())

#: Ile zdań pokazać przy liczbie. Liczba bez przykładu nie mówi, co ją wywołało,
#: a tutaj trzeba przeczytać i to, co sonda wzięła za szczelinę, i to, co za ruch.
PRZYKŁADY = 8

#: Ile czytań zbierać po każdej stronie. Dwa, bo pytanie jest o to, czy czytanie
#: jest jedno, i werdykt zamyka się na drugim. Liczba czytań ponad dwa nie wchodzi
#: do tabeli przejść, a kosztuje przeszukanie całej przestrzeni tam, gdzie
#: zdjęta spójność właśnie ją rozdmuchała.
LIMIT = 2

#: Ile sekund dostaje jedno zdanie po jednej stronie. Budżet stoi tu, bo
#: przeszukiwanie więzów nie ma ograniczenia, które ma parser tablicowy, a
#: najdroższy jest werdykt „jedno czytanie”: zamyka się dopiero po wyczerpaniu
#: przestrzeni, którą zdjęta spójność powiększa. Zdanie, które budżetu nie
#: dowiozło, wchodzi do tabeli jako urwane, a nie jako odrzucone.
BUDŻET = 10.0

#: Werdykt zdania, którego podłoże nie rozstrzygnęło w budżecie. Nie „odrzucone”,
#: bo to dwie różne odpowiedzi.
URWANE = "urwane"

#: Zdanie do pokazania przy liczbie, długością do przodu, żeby sortowanie
#: wybierało najkrótsze. Długość jest w segmentach, tak jak wszystko inne tutaj.
Przykład = tuple[int, str]


class Urwane(Exception):
    """Zdanie nie zmieściło się w budżecie."""


def _alarm(*_):
    raise Urwane()


@dataclass
class Raport:
    """Liczniki jednego przebiegu, wraz ze zdaniami, które je czynią czytelnymi."""

    #: Ile zdań zachować pod każdym kluczem. Stoi przy licznikach, a nie przy
    #: każdym wołaniu, bo jest tym samym przez cały przebieg i przy scalaniu.
    ile_przykładów: int = PRZYKŁADY
    drzewa: int = 0
    #: Ile szczelin w drzewie → ile zdań tyle ich ma. Rozkład, a nie sama suma,
    #: bo zdanie złożone ma tyle ciągów, ile zdań składowych, i dopiero rozkład
    #: mówi, czy nieciągłość wypada w zdaniu raz.
    szczeliny: collections.Counter = field(default_factory=collections.Counter)
    #: Werdykt olskiego nad zdaniami ze szczeliną.
    werdykty: collections.Counter = field(default_factory=collections.Counter)
    #: Na czym stanęła analiza tych z nich, których olski nie wyprowadza. To jest
    #: ta liczba, po której widać, czy nieciągłość jest ich najbliższym blokerem.
    blokery: collections.Counter = field(default_factory=collections.Counter)
    #: Werdykt olskiego nad zdaniami, którym szczelina wypadła poza drzewem
    #: wybranym. Werdykt, a nie sama suma, bo cała ta liczba jest o zdania
    #: przyjęte: odrzuconemu olski niczego nie obiecuje.
    maskowanie: collections.Counter = field(default_factory=collections.Counter)
    #: Na czym stanęły analizy odrzuconych z nich. Ta sama tabela, co dla zdań ze
    #: szczeliną wybraną, i porównanie obu jest tym, po czym widać, czy maskowanie
    #: ma własny wyzwalacz, czy rośnie razem z zakupem.
    blokery_maskowanych: collections.Counter = field(default_factory=collections.Counter)
    #: (werdykt ze spójnością, werdykt bez niej) → ile zdań tak przeszło. Para, a
    #: nie napis z nią w środku, bo wydruk pyta o obie strony osobno i rozklejanie
    #: napisu byłoby czytaniem tego, co ten sam moduł właśnie skleił.
    przejścia: collections.Counter = field(default_factory=collections.Counter)
    #: Klucz → najkrótsze zdania, na których to widać.
    przykłady: dict[tuple, list[Przykład]] = field(default_factory=dict)
    #: Zdania, których nie zmierzono, po powodzie. Wypisane, a nie odjęte po
    #: cichu, bo mianownik bez nich byłby mianownikiem zdań łatwych.
    pominięte: collections.Counter = field(default_factory=collections.Counter)

    @property
    def ze_szczeliną(self) -> int:
        return sum(self.szczeliny.values())

    def zanotuj(self, klucz: tuple, przykład: Przykład) -> None:
        """Zachowaj to zdanie pod kluczem, jeśli jest krótsze od już zachowanych.

        Najkrótsze, a nie pierwsze napotkane, z dwóch powodów. Krótkie zdanie
        pokazuje jedną rzecz, a długie dziesięć. I scalanie kawałków przestaje
        zależeć od kolejności, w jakiej wróciły: pierwsze napotkane są pierwszymi
        w swoim kawałku, a najkrótsze są najkrótszymi w całym przebiegu.
        """
        zachowane = self.przykłady.setdefault(klucz, [])
        zachowane.append(przykład)
        zachowane.sort()
        del zachowane[self.ile_przykładów :]


def szczeliny(forest) -> int:
    """Ile szczelin ma drzewo wzorcowe tego lasu.

    Liczone po drzewie wybranym, a nie po pliku: las trzyma także węzły, których
    odpowiedź nie bierze, i szczelina stoi wśród nich częściej niż w samej
    odpowiedzi, bo to ona jest tym, co annotator odrzucał. Grep po pliku liczy
    więc kilka razy za dużo i nie mówi o polszczyźnie nic.
    """
    return sum(1 for fraza in constituents(forest) if fraza.category == SZCZELINA)


def w_lesie(ścieżka: Path) -> bool:
    """Czy plik ma szczelinę gdziekolwiek, czyli także wśród czytań odrzuconych.

    Pytanie odwrotne do tego, na które odpowiada ``szczeliny`` obok, i wołane
    dopiero wtedy, gdy tamto odpowiedziało zero: zdanie, któremu szczelinę
    wybrano, jest potrzebą, a zdanie, któremu ją odrzucono, jest maskowaniem.
    """
    return bool(SZCZELINA_W_LESIE.search(ścieżka.read_bytes()))


def podłoże(segmenty: list, spójne: bool, budżet: float) -> str:
    """Werdykt podłoża nad tym zdaniem, albo ``urwane``, gdy nie zmieścił się w budżecie."""
    # Uchwyt ustawiany przy każdym wołaniu, bo przebieg idzie po procesach
    # roboczych, a żaden z nich nie zaczyna od `main`, gdzie stanąłby raz.
    signal.signal(signal.SIGALRM, _alarm)
    try:
        signal.setitimer(signal.ITIMER_REAL, budżet)
        return rozbierz(segmenty, GRAMATYKA, limit=LIMIT, spójne=spójne).status
    except Urwane:
        return URWANE
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def zmierz(
    ścieżki: Iterable[Path],
    przykłady: int = PRZYKŁADY,
    budżet: float = BUDŻET,
) -> Raport:
    """Policz obie połowy pomiaru nad tymi lasami.

    Jeden przebieg na obie, bo obie czytają to samo drzewo wzorcowe i ta sama
    morfologia złota wchodzi do obu. Zdanie ze szczeliną i zdanie przyjęte przez
    olskiego są przy tym dwiema populacjami, a nie jedną: pierwsza mówi, ile
    nieciągłość kupuje, druga, ile kosztuje.

    Populacja jest ta sama, co w ``olski.coverage.measure``: każde zdanie z
    drzewem wzorcowym, bez granicy na długość. Podłoże więzowe zostaje przy tym
    pod :data:`BUDŻET`, bo ograniczenia parsera tablicowego nie ma, a zdanie,
    które budżetu nie dowiozło, wchodzi do tabeli jako urwane.
    """
    raport = Raport(przykłady)
    for ścieżka in ścieżki:
        forest = read_forest(ścieżka)
        zdanie = parse_forest(forest)
        if not zdanie.annotated:
            continue
        segmenty = segments_for(zdanie, "gold")
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        raport.drzewa += 1

        wynik = Outcome(
            sentence=zdanie,
            result=parse(GRAMMAR, segmenty, najdalszy=True),
            segments=tuple(segmenty),
            comparable=True,
        )
        przykład = (len(segmenty), zdanie.text)
        ile = szczeliny(forest)
        if ile:
            raport.szczeliny[ile] += 1
            raport.werdykty[wynik.status] += 1
            raport.zanotuj(("szczelina", wynik.status), przykład)
            if wynik.blocker:
                raport.blokery[wynik.blocker] += 1
        elif w_lesie(ścieżka):
            raport.maskowanie[wynik.status] += 1
            raport.zanotuj(("maskowanie", wynik.status), przykład)
            if wynik.blocker:
                raport.blokery_maskowanych[wynik.blocker] += 1
        if wynik.status != "valid":
            continue

        przejście = (
            podłoże(list(segmenty), True, budżet),
            podłoże(list(segmenty), False, budżet),
        )
        raport.przejścia[przejście] += 1
        raport.zanotuj(("przejście", *przejście), przykład)
    return raport


def _kawałek(ścieżki: Sequence[Path], przykłady: int, budżet: float):
    return zmierz(ścieżki, przykłady, budżet)


def przebieg(
    ścieżki: Sequence[Path],
    jobs: int,
    przykłady: int = PRZYKŁADY,
    budżet: float = BUDŻET,
) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport.

    Podział na kawałki jest ten sam, którym idzie ``olski-corpus``, i stoi tam,
    bo decyzja o jego rozmiarze jest jedna. Składanie zostaje tutaj, bo licznik,
    który z kawałka wraca, jest licznikiem tej sondy.
    """
    praca = functools.partial(_kawałek, przykłady=przykłady, budżet=budżet)
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden.

    Scalony raport jest tym samym raportem, co z jednego przebiegu nad całością,
    przykłady włącznie, i nie zależy przy tym od kolejności kawałków: liczniki
    się dodają, a przykłady wybiera długość zdania.
    """
    scalony = Raport(przykłady)
    for raport in raporty:
        scalony.drzewa += raport.drzewa
        scalony.szczeliny.update(raport.szczeliny)
        scalony.werdykty.update(raport.werdykty)
        scalony.blokery.update(raport.blokery)
        scalony.maskowanie.update(raport.maskowanie)
        scalony.blokery_maskowanych.update(raport.blokery_maskowanych)
        scalony.przejścia.update(raport.przejścia)
        scalony.pominięte.update(raport.pominięte)
        for klucz, zachowane in raport.przykłady.items():
            for przykład in zachowane:
                scalony.zanotuj(klucz, przykład)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(raport: Raport, nagłówek: str, blokery: int = 10) -> str:
    udział = raport.ze_szczeliną / raport.drzewa if raport.drzewa else 0.0
    wiersze = [
        f"{nagłówek}, {raport.drzewa} drzew wzorcowych",
        "",
        f"potrzeba: {raport.ze_szczeliną} zdań ze szczeliną, {udział:.1%} drzew",
    ]
    for ile, zdań in sorted(raport.szczeliny.items()):
        wiersze.append(f"  {zdań:>7}  szczelin w drzewie: {ile}")
    for powód, zdań in raport.pominięte.most_common():
        wiersze.append(f"  {zdań:>7}  niezmierzone: {powód}")
    wiersze += _tabela("werdykt olskiego nad tymi zdaniami:", raport.werdykty)
    # Bloker jest tym, po czym widać, czy szczelina jest tym, czego brakuje
    # najbliżej. Konstrukcja, która nie stoi w tej tabeli ani raz, nie kupuje
    # ani jednego z tych zdań, choćby ją dopisać.
    wiersze += _tabela("na czym stanęły analizy odrzuconych:", raport.blokery, blokery)
    wiersze += _przykłady(raport, ("szczelina", "rejected"), "najkrótsze odrzucone")
    wiersze += _przykłady(raport, ("szczelina", "valid"), "najkrótsze przyjęte")

    maskowane = sum(raport.maskowanie.values())
    wiersze += ["", f"maskowanie: {maskowane} zdań ze szczeliną poza drzewem wybranym"]
    wiersze += _tabela("werdykt olskiego nad tymi zdaniami:", raport.maskowanie)
    wiersze += _tabela("na czym stanęły analizy odrzuconych:", raport.blokery_maskowanych, blokery)
    wiersze += _przykłady(raport, ("maskowanie", "valid"), "najkrótsze przyjęte")

    zmierzone = sum(raport.przejścia.values())
    wiersze += ["", f"cena: {zmierzone} zdań, które olski przyjmuje jednym czytaniem"]
    # Werdykty w tej tabeli są podłoża, a nie olskiego, i wiersz to mówi: olski
    # wydał je wszystkie wyżej, przyjmując te zdania, więc czytelnik, który tego
    # nie widzi, czyta pierwszy wiersz jako sprzeczność.
    wiersze.append("  werdykt podłoża więzowego, ze spójnością → bez niej:")
    for (przed, po), zdań in raport.przejścia.most_common():
        wiersze.append(f"  {zdań:>7}    {przed} → {po}")
    for przed, po in raport.przejścia:
        if przed != po:
            wiersze += _przykłady(raport, ("przejście", przed, po), f"najkrótsze {przed} → {po}")
    return "\n".join(wiersze)


def _tabela(nazwa: str, licznik: collections.Counter, ile: int | None = None) -> list[str]:
    """Licznik pod nagłówkiem, od najczęstszego, albo nic, gdy nie ma czego liczyć.

    Cztery tabele tego wydruku różnią się tym, co liczą, a nagłówek jest jedynym
    miejscem, gdzie to mówią, więc kształt jest jeden i stoi tutaj.
    """
    if not licznik:
        return []
    return [f"  {nazwa}", *(f"  {ilu:>7}    {klucz}" for klucz, ilu in licznik.most_common(ile))]


def _przykłady(raport: Raport, klucz: tuple, nazwa: str) -> list[str]:
    """Zdania zachowane pod kluczem, z długością, bo po niej je wybrano.

    Zdania stoją tu po to, żeby liczba nad nimi dała się sprawdzić:
    to one, a nie liczba, mówią, co sonda uznała za szczelinę i za ruch.
    """
    zachowane = raport.przykłady.get(klucz)
    if not zachowane:
        return []
    return [f"  {nazwa}:", *(f"    {ile:>3}  {tekst}" for ile, tekst in zachowane)]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.nieciągłość",
        description="Policz, ile nieciągłość kupuje zdań i ile ich kosztuje.",
    )
    parser.add_argument("root", help="katalog z rozpakowaną Składnicą")
    parser.add_argument("--limit", type=int, help="zatrzymaj się po tylu lasach")
    parser.add_argument(
        "--przykłady", type=int, default=PRZYKŁADY, dest="przykłady", help="ile zdań pokazać"
    )
    parser.add_argument(
        "--budżet",
        type=float,
        default=BUDŻET,
        dest="budżet",
        help=f"ile sekund dostaje jedno zdanie po jednej stronie (domyślnie {BUDŻET:.0f})",
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

    root = Path(args.root)
    if not root.is_dir():
        print(f"harness.nieciągłość: nie ma takiego katalogu: {root}", file=sys.stderr)
        print("harness.nieciągłość: skąd wziąć korpus, mówi docs/corpus.md", file=sys.stderr)
        return 2
    raport = przebieg(
        pliki(root)[: args.limit],
        args.jobs,
        przykłady=args.przykłady,
        budżet=args.budżet,
    )
    print(wydruk(raport, "Składnica, morfologia złota"))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
