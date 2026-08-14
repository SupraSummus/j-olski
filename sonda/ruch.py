"""Sonda różnicowa: ile konstrukcja kupuje i ile kosztuje, liczone ruchem werdyktu.

Pytanie, które ta maszyneria obsługuje, jest jedno i stawia je każda sonda
osobno: ile zdań konstrukcja odbiera. Zdanie odrzucone przez wieloznaczność jest
droższe niż zdanie, którego gramatyka nie wyprowadza wcale, bo tamto czeka na
produkcję, a to na jej wycofanie, więc sumy z ``olski-corpus`` na to nie
odpowiadają: przejście ``przyjęte → wieloznaczne`` jest ceną, przejście
``odrzucone → przyjęte`` zakupem, a jedno i drugie widać dopiero zdanie po
zdaniu.

Wariantem jest gramatyka olskiego z wyjętą grupą produkcji, a konstrukcję, którą
olski ma, mierzy się właśnie tak, przez zdejmowanie. Dopisana mierzyłaby produkcję
napisaną w sondzie, czyli drugą deklarację tego samego, i rozeszłaby się z olskim
po pierwszej zmianie, której nikt by tu nie powtórzył.

Konstrukcji, której olski nie ma, ten powód nie dotyczy, bo nie ma tam pierwszej
deklaracji, od której miałaby się rozejść, a wycena przed dopisaniem jest tym,
po co się ją pisze. Taka sonda wypełnia :attr:`Sonda.dopisuje` i mierzy tę samą
różnicę w drugą stronę: mianownikiem zostaje wariant, który dopisku nie bierze.
Kierunek nie sięga niżej niż do tego jednego pola, bo grupa nazywana przez
:attr:`Sonda.grupa` odsiewa produkcję dopisaną tak samo, jak odsiewa własną.

Podział pracy jest przez to jednozdaniowy. Sonda odpowiada, do której grupy
produkcja należy, a wszystko pozostałe — warianty, przebieg, tabelę przejść,
konkurencję grup i wiersz poleceń — dostaje z tego pliku. Wariantów jest tyle,
ile grup da się zdjąć osobno, bo cena każdej z nich jest osobną liczbą.
"""

from __future__ import annotations

import argparse
import collections
import functools
import os
import sys
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.corpus import Sentence, pliki, read
from olski.coverage import Outcome, po_kawałkach
from olski.grammar import Grammar, Production
from olski.parse import parse
from olski.subset import FRAGMENT, build, check

#: Ile zdań zachować pod każdym przejściem. Przejście bez przykładu jest liczbą,
#: o której nie wiadomo, co ją wywołało, a cena jest tu tym, co trzeba przeczytać.
PRZYKŁADY = 8

#: Werdykty w kolejności, w jakiej stoją w tabeli.
STANY = ("valid", "ambiguous", "rejected")

#: Czym zaczyna się klucz przykładów trzymanych pod rolą, a nie pod przejściem.
#: Napisem, a nie drugim słownikiem, bo obie rodziny przykładów wchodzą do
#: jednego budżetu :attr:`Raport.ile_przykładów`, scalają się jednym :func:`scal`
#: i wychodzą jednym wydrukiem.
ROLA = "rola:"

#: Rola, pod którą przykładów nie trzymamy, bo zdanie przeczytane tak jak w banku
#: drzew nie jest tym, co z tej tabeli trzeba przeczytać. Wartość wydaje
#: ``Outcome.agreement`` i tyle o niej wie ten plik.
ZGODNE = "agrees"


@dataclass(frozen=True)
class Sonda:
    """Co jedna sonda różnicowa mówi o sobie wspólnemu przebiegowi.

    Warianty stoją w kolejności wydruku. Pierwszy zdejmuje wszystko i jest
    mianownikiem, wobec którego liczone są przejścia; ostatni zdejmuje zero i
    dopiero on pokazuje konkurencję między grupami, o którą sondzie chodzi.
    Między nimi stoi po jednym wariancie na grupę zdejmowaną osobno.

    Który z tych dwóch końców jest samym olskim, mówi :attr:`dopisuje`, a nie ta
    kolejność: sonda zdejmująca ma go na końcu, sonda dopisująca na początku.
    Wspólne obu jest to, że mianownik stoi pierwszy, a gramatyka wyceniana
    ostatnia.
    """

    #: Nazwa programu w wydruku pomocy i w komunikacie o błędzie ścieżki.
    prog: str
    #: O co ta sonda pyta, jednym zdaniem, do wydruku pomocy.
    opis: str
    #: Nazwy wariantów, one zaś są etykietami wiersza w tabeli, więc stoją tu
    #: pełnym napisem: `bez przecinka`, a nie `bez`. Nazwy pośrednie są przy tym
    #: nazwami grup, czyli tym, co oddaje :attr:`grupa`, i po tym wspólnym napisie
    #: wariant poznaje swoje produkcje.
    warianty: tuple[str, ...]
    #: Do której grupy należy ta produkcja; ``None``, gdy do żadnej i gdy zostaje
    #: w każdym wariancie. To jedno pytanie jest wszystkim, czym sondy różnicowe
    #: się różnią, i dlatego gramatykę wariantu składa :func:`gramatyka` niżej,
    #: jedna dla wszystkich, a nie każda sonda po swojemu.
    grupa: Callable[[Production], str | None]
    #: Dwa pytania o konkurencję grup, w kolejności wydruku, każde całym zdaniem.
    #: Całym, a nie rzeczownikiem do wstawienia w gotowy wzór: wzór żądałby od
    #: każdej sondy formy fleksyjnej, a nagłówek nad tymi dwoma wierszami nazwy
    #: grupy nie potrzebuje, bo one same ją noszą.
    #: Konkurencja ma dwa stopnie. Zdanie, które rusza się pod jedną grupą i pod
    #: drugą, jest zdaniem, o które grupy się spierają. Zdanie, o którym oba
    #: warianty naraz mówią co innego, niż mówi którykolwiek z nich osobno, jest
    #: zdaniem, na którym ten spór coś kosztuje: dwie produkcje dały mu czytanie,
    #: którego żadna z nich nie dała.
    pytania: tuple[str, str]
    #: Produkcje, których olski nie ma, dopisane do świeżej gramatyki przez tę
    #: funkcję; ``None`` u sondy, która mierzy konstrukcję stojącą w gramatyce.
    #: Dopisuje wszystkie naraz i o warianty nie pyta, bo o to, które z nich w
    #: tym wariancie zostają, pyta :attr:`grupa` — ta sama, którą sonda zdejmująca
    #: nazywa grupy własne. Stąd żądanie: każda produkcja dopisana ma mieć tam
    #: nazwę grupy, bo dopisek bez niej zostałby także w mianowniku i sonda
    #: mierzyłaby zero.
    dopisuje: Callable[[Grammar], None] | None = None

    @property
    def osobne(self) -> tuple[str, ...]:
        """Warianty zdejmujące po jednej grupie, czyli te między mianownikiem a całością."""
        return self.warianty[1:-1]

    @property
    def czysty(self) -> str:
        """Wariant, który jest dokładnie gramatyką olskiego.

        Sonda zdejmująca ma go na końcu, bo tam nie zdejmuje nic; sonda
        dopisująca na początku, bo tam odsiewa cały swój dopisek. Niezmiennik
        pilnuje ``tests/test_ruch.py``, i pilnuje go po tej właśnie własności,
        a nie po numerze wariantu.
        """
        return self.warianty[0] if self.dopisuje is not None else self.warianty[-1]


@functools.cache
def gramatyka(sonda: Sonda, wariant: str) -> Grammar:
    """Gramatyka olskiego bez tych grup produkcji, których ten wariant nie ma.

    Przepisujemy produkcje ze świeżej gramatyki, takie jakie są, bo złożona drugi
    raz z części gubiłaby głowę (``Grammar.dopisz``). Wariant pełny dostaje przez
    to wszystkie, a wariant :attr:`Sonda.czysty` dokładnie te, które olski ma, co
    pilnuje ``tests/test_ruch.py``.

    Dopisek sondy wchodzi przed odsiewem, a nie po nim, i to jest cały koszt
    drugiego kierunku: produkcja dopisana przechodzi przez to samo pytanie o
    grupę, co produkcja olskiego, więc pętla niżej nie wie, którą ma pod ręką.

    Budowana raz na proces roboczy, bo budowa jest droższa niż rozbiór jednego
    zdania, a gramatyka po zbudowaniu się nie zmienia.
    """
    if wariant not in sonda.warianty:
        raise ValueError(f"{sonda.prog}: nieznany wariant: {wariant}")
    pełna = build()
    if sonda.dopisuje is not None:
        sonda.dopisuje(pełna)
    okrojona = Grammar(start=pełna.start)
    for produkcja in pełna.productions:
        grupa = sonda.grupa(produkcja)
        if grupa is not None and wariant != sonda.warianty[-1] and grupa != wariant:
            continue
        okrojona.dopisz(produkcja)
    return okrojona


@dataclass
class Raport:
    """Liczniki jednego przebiegu, wraz ze zdaniami, które je czynią czytelnymi."""

    sonda: Sonda
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
    #: Czy grupy produkcji wchodzą sobie w drogę; co to znaczy, mówi
    #: :attr:`Sonda.pytania`.
    konkurencja: collections.Counter = field(default_factory=collections.Counter)
    #: Zdania, których nie zmierzono, po powodzie. Wypisane, a nie odjęte po
    #: cichu, bo mianownik bez nich byłby mianownikiem zdań łatwych.
    pominięte: collections.Counter = field(default_factory=collections.Counter)

    @property
    def zmierzone(self) -> int:
        return sum(self.stany.get(self.sonda.warianty[0], collections.Counter()).values())

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
        mianownik = stany[self.sonda.warianty[0]]
        for wariant, stan in stany.items():
            self.stany.setdefault(wariant, collections.Counter())[stan] += 1
            if wariant == self.sonda.warianty[0] or stan == mianownik:
                continue
            przejście = f"{mianownik} → {stan}"
            self.przejścia.setdefault(wariant, collections.Counter())[przejście] += 1
            self.zanotuj((wariant, przejście), tekst)
            if stan == "valid" and wariant in role:
                zgoda = role[wariant] or "brak roli"
                self.zgodność.setdefault(wariant, collections.Counter())[zgoda] += 1
                #  Przejście, pod którym takie zdanie stoi, trzyma je razem z
                #  kilkudziesięcioma zgodnymi, więc pod rolą stoi drugi raz.
                if zgoda != ZGODNE:
                    self.zanotuj((wariant, f"{ROLA} {zgoda}"), tekst)
        self._konkurencja(tekst, stany, mianownik)

    def _konkurencja(self, tekst: str, stany: dict[str, str], mianownik: str) -> None:
        ruszone = {
            wariant: stany[wariant]
            for wariant in self.sonda.osobne
            if stany[wariant] != mianownik
        }
        if len(ruszone) >= 2:
            self._policz(self.sonda.pytania[0], tekst)
        if stany[self.sonda.warianty[-1]] not in {mianownik, *ruszone.values()}:
            self._policz(self.sonda.pytania[1], tekst)

    def _policz(self, nazwa: str, tekst: str) -> None:
        self.konkurencja[nazwa] += 1
        self.zanotuj(("konkurencja", nazwa), tekst)

    def zanotuj(self, klucz: tuple[str, str], tekst: str) -> None:
        """Zachowaj zdanie pod kluczem, dopóki mieści się w budżecie przykładów."""
        zachowane = self.przykłady.setdefault(klucz, [])
        if len(zachowane) < self.ile_przykładów:
            zachowane.append(tekst)


def zmierz(
    sonda: Sonda,
    zdania: Iterable[Sentence],
    przykłady: int = PRZYKŁADY,
) -> Raport:
    """Przepuść zdania banku drzew przez każdy wariant i policz, co się rusza.

    Populacja jest ta sama, co w ``olski.coverage.measure``: każde zdanie z
    drzewem wzorcowym, bez granicy na długość.
    """
    raport = Raport(sonda, przykłady)
    for zdanie in zdania:
        if not zdanie.annotated:
            continue
        segmenty = list(zdanie.segments)
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        wyniki = {
            wariant: Outcome(
                sentence=zdanie,
                result=parse(gramatyka(sonda, wariant), segmenty),
                segments=tuple(segmenty),
            )
            for wariant in sonda.warianty
        }
        raport.zapisz(
            zdanie.text,
            {wariant: wynik.status for wariant, wynik in wyniki.items()},
            {wariant: wynik.agreement for wariant, wynik in wyniki.items()},
        )
    return raport


def nad_prozą(sonda: Sonda, tekst: str, przykłady: int = PRZYKŁADY) -> Raport:
    """To samo porównanie nad prozą, którą olski ma czytać.

    Bank drzew rankinguje konstrukcje w rejestrze, którego olski nie ma, i mówi
    przez to, ile konstrukcja kupuje w cudzej polszczyźnie. Drugie pytanie jest o
    rejestr własny i pada tu. Ról nie ma czym porównać, bo drzewa wzorcowego
    proza nie niesie, a fragment nie jest zdaniem i do mianownika nie wchodzi.
    """
    raport = Raport(sonda, przykłady)
    wyniki = {wariant: check(tekst, gramatyka(sonda, wariant)) for wariant in sonda.warianty}
    for kolejne in zip(*wyniki.values(), strict=True):
        werdykty = dict(zip(sonda.warianty, kolejne, strict=True))
        pierwszy = werdykty[sonda.warianty[0]]
        if pierwszy.status == FRAGMENT:
            raport.pominięte["fragment, a nie zdanie"] += 1
            continue
        raport.zapisz(
            pierwszy.text,
            {wariant: werdykt.status for wariant, werdykt in werdykty.items()},
            {},
        )
    return raport


def _kawałek(ścieżki: Sequence[Path], sonda: Sonda, przykłady: int):
    return zmierz(sonda, (read(ścieżka) for ścieżka in ścieżki), przykłady)


def przebieg(
    sonda: Sonda,
    ścieżki: Sequence[Path],
    jobs: int,
    przykłady: int = PRZYKŁADY,
) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport.

    Podział na kawałki jest ten sam, którym idzie ``olski-corpus``, i stoi tam,
    bo decyzja o jego rozmiarze jest jedna. Składanie zostaje tutaj, bo licznik,
    który z kawałka wraca, jest licznikiem sondy.
    """
    praca = functools.partial(_kawałek, sonda=sonda, przykłady=przykłady)
    return scal(sonda, po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(sonda: Sonda, raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden.

    Kawałki są odcinkami jednej posortowanej listy plików i wchodzą tu w jej
    kolejności, więc scalony raport jest tym samym raportem, co z jednego
    przebiegu nad całością, przykłady włącznie.
    """
    scalony = Raport(sonda, przykłady)
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


def wydruk(raport: Raport, nagłówek: str) -> str:
    sonda = raport.sonda
    szerokość = max(len("wariant"), *(len(wariant) for wariant in sonda.warianty))
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań",
        "",
        f"{'wariant':>{szerokość}}  {'przyjęte':>10} {'wieloznaczne':>13} {'odrzucone':>10}",
    ]
    for wariant in sonda.warianty:
        licznik = raport.stany.get(wariant, collections.Counter())
        przyjęte, wieloznaczne, odrzucone = (licznik.get(stan, 0) for stan in STANY)
        wiersze.append(
            f"{wariant:>{szerokość}}  {przyjęte:>10} {wieloznaczne:>13} {odrzucone:>10}"
        )
    for powód, ile in raport.pominięte.most_common():
        wiersze.append(f"{ile:>7}          niezmierzone: {powód}")

    for wariant in sonda.warianty[1:]:
        przejścia = raport.przejścia.get(wariant)
        wiersze += ["", f"ruch wobec wariantu „{sonda.warianty[0]}” — {wariant}:"]
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
                for tekst in raport.przykłady.get((wariant, f"{ROLA} {nazwa}"), []):
                    wiersze.append(f"             {tekst}")

    # Zero wypisane, a nie pominięte: liczba, której nie ma, czyta się jak
    # pomiar, którego nie było, a to jest ta liczba, po którą sonda stoi.
    wiersze += ["", "konkurencja, nad zdaniem po zdaniu:"]
    for nazwa in sonda.pytania:
        wiersze.append(f"  {raport.konkurencja.get(nazwa, 0):>7}  {nazwa}")

    for nazwa in sonda.pytania:
        zachowane = raport.przykłady.get(("konkurencja", nazwa), [])
        if zachowane:
            wiersze += ["", f"konkurencja, {nazwa}:"]
            wiersze += [f"  {tekst}" for tekst in zachowane]

    for wariant in sonda.warianty[1:]:
        for przejście, _ in raport.przejścia.get(wariant, collections.Counter()).most_common():
            zachowane = raport.przykłady.get((wariant, przejście), [])
            if not zachowane:
                continue
            wiersze += ["", f"{wariant}, {przejście}:"]
            wiersze += [f"  {tekst}" for tekst in zachowane]

    return "\n".join(wiersze)


def main(sonda: Sonda, argv: Sequence[str] | None = None) -> int:
    """Wiersz poleceń wspólny sondom różnicowym: katalog banku drzew albo plik prozy."""
    parser = argparse.ArgumentParser(prog=sonda.prog, description=sonda.opis)
    parser.add_argument(
        "ścieżka",
        help="katalog z rozpakowaną Składnicą albo plik z prozą do przeczytania",
    )
    parser.add_argument("--limit", type=int, help="zatrzymaj się po tylu lasach")
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
            sonda,
            pliki(ścieżka)[: args.limit],
            args.jobs,
            przykłady=args.przykłady,
        )
        print(wydruk(raport, "Składnica, morfologia złota"))
        return 0
    if ścieżka.is_file():
        raport = nad_prozą(sonda, ścieżka.read_text(), args.przykłady)
        print(wydruk(raport, f"{ścieżka.name}, proza"))
        return 0
    print(f"{sonda.prog}: nie ma takiego katalogu ani pliku: {ścieżka}", file=sys.stderr)
    print(f"{sonda.prog}: docs/corpus.md mówi, skąd wziąć korpus", file=sys.stderr)
    return 2
