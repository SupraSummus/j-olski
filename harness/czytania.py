"""Czym różnią się czytania zdania, które olski odrzuca za wieloznaczność, nad Składnicą.

Odrzucenie za wieloznaczność mówi, że czytań jest więcej niż jedno, i nie mówi,
czym one się różnią. Pytanie o ujednoznacznianie zaczyna się tutaj:
maszyna, która ma taki las zwinąć, musi rozstrzygnąć konkretny wybór, a wyborów
tego rejestru jest kilka rodzajów i każdy żąda czegoś innego. Sonda liczy, ile
zdań przypada na który.

Rodzaje bierze z tego, co werdykt o zdaniu mówi, a nie z osobnej klasyfikacji
napisanej obok: ``różniące`` nazywa role, które czytania obsadzają różnie,
``przyłączenia`` modyfikatory, których gospodarz zostaje nierozstrzygnięty, a
``rozbieżności`` konstytuenty czytane kilkoma sposobami poza zasięgiem
streszczenia (``olski/parse.py``).

Wynik odpowiada na dwa pytania naraz i to jest powód, żeby liczyć je jednym
przebiegiem. Pierwsze: co musiałaby umieć maszyna, żeby zdanie z tej klasy
przestało być wieloznaczne — rozstrzygnąć przyłączenie, obsadzić role, albo
jedno i drugie. Drugie: ile z tego jest już za darmo, bo kolejność, w jakiej las
wydaje czytania, jest rankingiem, którego nikt nie trenował, a ``numer_czytania``
mówi, na którym miejscu stoi w niej czytanie wybrane przez anotatorów.

Wynik czyta ``docs/disambiguation.md``.

    python3 -m harness.czytania Składnica-frazowa-180723/
"""

from __future__ import annotations

import argparse
import collections
import functools
import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.corpus import Sentence, read
from harness.komenda import Komenda, uruchom
from harness.pomiar import PORÓWNYWANE_ROLE, po_kawałkach, segments_for
from olski.parse import Las, Result, las, podsumuj
from olski.subset import DEKLARACJA, GRAMMAR

#: Ile zdań zachować pod każdą klasą. Klasa bez przykładu jest liczbą, o której
#: nie wiadomo, jakie zdanie ją wywołało, a to właśnie zdania mówią, czy klasa
#: nazywa wybór, który czytelnik ma.
PRZYKŁADY = 8

#: Nazwa klasy, w której werdykt nie nazywa niczego poza liczbą czytań.
SAMA_LICZBA = "sama liczba czytań"


def klasa(result: Result) -> str:
    """Czym werdykt tłumaczy wieloznaczność tego zdania.

    Nazwy stoją w stałej kolejności, a nie w kolejności trafień, bo klasa jest
    kluczem tabeli: ``rola + przyłączenie`` i ``przyłączenie + rola`` byłyby
    dwoma wierszami o jednym znaczeniu.
    """
    nazwy = [
        nazwa
        for nazwa, jest in (
            ("rola", bool(result.różniące)),
            ("przyłączenie", bool(result.przyłączenia)),
            ("konstytuent", bool(result.rozbieżności)),
        )
        if jest
    ]
    return " + ".join(nazwy) if nazwy else SAMA_LICZBA


def całe_przyłączenie(result: Result) -> bool:
    """Czy przyłączenia są całą decyzją, którą to zdanie zostawia.

    Nazwa klasy tego nie mówi i mówić nie może. ``Czeka koń z furą.`` ma jedno
    przyłączenie i różni się rolą, bo podmiotem jest raz ``koń z furą``, a raz
    ``koń``: rola rusza się dlatego, że rusza się przyłączenie, więc decyzja jest
    jedna, a werdykt nazywa ją dwa razy. ``Koszt samej szynki przewyższa koszt
    szynki z dodatkami.`` ma dwie decyzje naraz, bo szyk odwraca się niezależnie
    od tego, dokąd dochodzi ``z dodatkami``.

    Rozdziela je iloczyn. Przyłączenie o dwóch gospodarzach mnoży las przez dwa,
    więc gdy iloczyn gospodarzy równa się liczbie czytań, żadna inna decyzja w
    tym lesie nie stoi, a gdy jest od niej mniejszy, stoi tam jeszcze coś.
    Zdanie bez ani jednego przyłączenia wraca stąd fałszem, bo iloczyn pusty
    wynosi jeden, a czytań jest więcej.

    Myli się w jedną stronę i myli się rzadko. Dwa przyłączenia, z których
    jedno ma gospodarza tylko pod jednym czytaniem drugiego, dają czytań mniej
    niż iloczyn, więc równość może wyjść zdaniu, które zostawia jeszcze jakąś
    decyzję, o ile ta odejmuje dokładnie tyle, ile tamta zależność. Liczba jest
    przez to górnym oszacowaniem, a nie pomiarem tego, ile decyzji tam stoi.
    """
    return math.prod(len(p.gospodarze) for p in result.przyłączenia) == result.ile


@dataclass
class Raport:
    """Co jeden przebieg naliczył."""

    ile_przykładów: int = PRZYKŁADY
    #: Zdania z pełnym drzewem wzorcowym, czyli mianownik werdyktów.
    zmierzone: int = 0
    #: Werdykt olskiego, po jednym liczniku na trzy odpowiedzi.
    werdykty: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Klasa wieloznaczności, liczona po zdaniach wieloznacznych.
    klasy: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Ile nierozstrzygniętych przyłączeń niesie zdanie wieloznaczne.
    przyłączenia: collections.Counter[int] = field(default_factory=collections.Counter)
    #: Zdania, w których przyłączenia są całą decyzją, pod kluczem klasy.
    całe: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Czy złote czytanie ocalało, pod kluczem klasy.
    ocalenie: collections.Counter[tuple[str, str]] = field(default_factory=collections.Counter)
    #: Którym z kolei jest złote czytanie, pod kluczem klasy.
    numery: collections.Counter[tuple[str, int]] = field(default_factory=collections.Counter)
    #: Zdania zachowane pod klasą, najkrótsze, z liczbą czytań.
    przykłady: dict[str, list[tuple[int, int, str]]] = field(default_factory=dict)
    #: Dlaczego zdanie nie weszło do żadnego licznika.
    pominięte: collections.Counter[str] = field(default_factory=collections.Counter)

    def zanotuj(self, klucz: str, przykład: tuple[int, int, str]) -> None:
        """Zachowaj zdanie pod klasą, zostawiając najkrótsze.

        Najkrótsze, bo przykład ma być do przeczytania, a nie do przewinięcia,
        i bo wybór po długości nie zależy od kolejności, w jakiej kawałki wracają.
        """
        zachowane = self.przykłady.setdefault(klucz, [])
        zachowane.append(przykład)
        zachowane.sort()
        del zachowane[self.ile_przykładów :]


def zmierz(ścieżki: Sequence[Path], przykłady: int = PRZYKŁADY) -> Raport:
    """Jeden przebieg po lasach, bez procesów pod spodem."""
    raport = Raport(przykłady)
    for ścieżka in ścieżki:
        zdanie = read(ścieżka)
        if not zdanie.annotated:
            continue
        segmenty = segments_for(zdanie, "gold")
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        raport.zmierzone += 1
        zbudowany = las(GRAMMAR, list(segmenty))
        result = podsumuj(zbudowany, DEKLARACJA, zatrzymanie=False)
        raport.werdykty[result.status] += 1
        if result.ambiguous:
            _wieloznaczne(raport, zdanie, zbudowany, result)
    return raport


def _wieloznaczne(raport: Raport, zdanie: Sentence, zbudowany: Las, result: Result) -> None:
    """Naliczenia, które powstają tylko nad zdaniem odrzuconym za wieloznaczność."""
    nazwa = klasa(result)
    raport.klasy[nazwa] += 1
    raport.przyłączenia[len(result.przyłączenia)] += 1
    if całe_przyłączenie(result):
        raport.całe[nazwa] += 1
    raport.zanotuj(nazwa, (len(zdanie.tokens), result.ile, zdanie.text))
    if not zdanie.roles:
        return
    #  Pytanie o złote czytanie jest tym samym pytaniem, które zadaje
    #  docs/corpus.md, i idzie tą samą drogą: rolami, bo nawiasowania dwie
    #  gramatyki nie dzielą, i przez las, bo lista czytań urywa się na
    #  MAX_READINGS właśnie na tych zdaniach.
    złote = {rola: zdanie.spans(rola) for rola in PORÓWNYWANE_ROLE}
    numer = zbudowany.numer_czytania(złote)
    raport.ocalenie[(nazwa, "lost" if numer is None else "survives")] += 1
    if numer is not None:
        raport.numery[(nazwa, numer)] += 1


def _kawałek(ścieżki: Sequence[Path], przykłady: int) -> Raport:
    return zmierz(ścieżki, przykłady)


def przebieg(ścieżki: Sequence[Path], jobs: int, przykłady: int = PRZYKŁADY) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport."""
    praca = functools.partial(_kawałek, przykłady=przykłady)
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden, przykłady włącznie."""
    scalony = Raport(przykłady)
    for raport in raporty:
        scalony.zmierzone += raport.zmierzone
        scalony.werdykty.update(raport.werdykty)
        scalony.klasy.update(raport.klasy)
        scalony.przyłączenia.update(raport.przyłączenia)
        scalony.całe.update(raport.całe)
        scalony.ocalenie.update(raport.ocalenie)
        scalony.numery.update(raport.numery)
        scalony.pominięte.update(raport.pominięte)
        for klucz, zachowane in raport.przykłady.items():
            for przykład in zachowane:
                scalony.zanotuj(klucz, przykład)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(raport: Raport, nagłówek: str) -> str:
    wieloznaczne = sum(raport.klasy.values())
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań z drzewem wzorcowym",
        "",
        "  werdykt olskiego:",
        *(f"  {ile:>7}    {status}" for status, ile in raport.werdykty.most_common()),
        *(f"  {ile:>7}    niezmierzone: {powód}" for powód, ile in raport.pominięte.most_common()),
    ]
    if not wieloznaczne:
        return "\n".join(wiersze)

    wiersze += ["", f"co werdykt nazywa nad {wieloznaczne} zdaniami wieloznacznymi:"]
    for nazwa, ile in raport.klasy.most_common():
        wiersze.append(f"  {ile:>7}  {ile / wieloznaczne:>6.1%}  {nazwa}")
    wiersze += ["", "  nierozstrzygniętych przyłączeń na zdanie:"]
    for ile_przyłączeń, zdań in sorted(raport.przyłączenia.items()):
        wiersze.append(f"  {zdań:>7}  {ile_przyłączeń:>6}")

    #  Maszyna rozstrzygająca przyłączenia wyprowadza zdanie z wieloznaczności
    #  dokładnie wtedy, gdy innej decyzji ten las nie zostawia, i to liczy
    #  `całe_przyłączenie`, a nie nazwa klasy: rola, która rusza się razem z
    #  przyłączeniem, jest tą samą decyzją nazwaną drugi raz.
    całe = sum(raport.całe.values())
    udział = całe / wieloznaczne
    wiersze += ["", f"przyłączenie jest całą decyzją w {całe} z {wieloznaczne} zdań, {udział:.1%}:"]
    for nazwa, _ in raport.klasy.most_common():
        ile = raport.całe.get(nazwa, 0)
        w_klasie = raport.klasy[nazwa]
        wiersze.append(f"  {ile:>7} z {w_klasie:<7} {ile / w_klasie:>6.1%}  {nazwa}")

    wiersze += _złote(raport)
    for nazwa, _ in raport.klasy.most_common():
        wiersze += _przykłady(raport, nazwa)
    return "\n".join(wiersze)


def _złote(raport: Raport) -> list[str]:
    """Ocalenie złotego czytania i jego numer, po klasach i razem.

    Numer stoi obok ocalenia, bo bez niego wiersz nie mówi tego, po co tu jest:
    czytanie pierwsze jest odpowiedzią rankingu, którego nikt nie trenował,
    a czytanie czterdzieste pierwsze odpowiedzią, której nikt nie zobaczy.
    """
    pytane = sum(raport.ocalenie.values())
    if not pytane:
        return []
    nagłówek = f"złote czytanie wśród czytań, nad {pytane} zdaniami z rolą w drzewie wzorcowym:"
    wiersze = ["", nagłówek]
    for nazwa in [*(klucz for klucz, _ in raport.klasy.most_common()), None]:
        ocalałe = _ile(raport.ocalenie, nazwa, "survives")
        wszystkie = ocalałe + _ile(raport.ocalenie, nazwa, "lost")
        if not wszystkie:
            continue
        pierwsze = sum(
            ile for (klucz, numer), ile in raport.numery.items() if numer == 1 and _ta(nazwa, klucz)
        )
        wiersze.append(
            f"  {ocalałe:>7} z {wszystkie:<7} {ocalałe / wszystkie:>6.1%} ocalało, "
            f"{pierwsze / wszystkie:>6.1%} czytaniem pierwszym    {nazwa or 'razem'}"
        )
    return wiersze


def _ta(nazwa: str | None, klucz: str) -> bool:
    """Czy wiersz o tej klasie liczy ten klucz; ``None`` jest wierszem zbiorczym."""
    return nazwa is None or nazwa == klucz


def _ile(licznik: collections.Counter[tuple[str, str]], nazwa: str | None, werdykt: str) -> int:
    return sum(ile for (klucz, kt), ile in licznik.items() if kt == werdykt and _ta(nazwa, klucz))


def _przykłady(raport: Raport, nazwa: str) -> list[str]:
    """Najkrótsze zdania klasy, z liczbą czytań, bo klasa o niej nie mówi."""
    zachowane = raport.przykłady.get(nazwa)
    if not zachowane:
        return []
    return [
        "",
        f"  najkrótsze zdania klasy „{nazwa}”:",
        *(f"    {ile:>3} czytań  {tekst}" for _, ile, tekst in zachowane),
    ]


def _korpus(ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    raport = przebieg(ścieżki, args.jobs, przykłady=args.przykłady)
    return wydruk(raport, "Składnica, morfologia złota")


KOMENDA = Komenda(
    nazwa="harness.czytania",
    opis="Policz, czym różnią się czytania zdań odrzuconych za wieloznaczność.",
    przykłady=PRZYKŁADY,
    korpus=_korpus,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
