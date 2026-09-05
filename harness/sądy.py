"""Ocena znalezisk olskiego nad korpusem: ocenione nie wracają, a baza rośnie.

``--nowe`` wypisuje znaleziska nad prozą korpusu, których baza w
``próba/nkjp-sądy.txt`` jeszcze nie ma; ktoś ocenia każde jako trafne albo
fałszywe i dopisuje do bazy, a następny przebieg tych znalezisk już nie wypisuje.
Bez flag sonda zestawia bazę z dzisiejszym werdyktem, bo werdykt rusza każde
dopisanie do gramatyki, a sąd nie. Po co ta baza jest i co jest w niej sądem,
mówi docs/corpora.md#baza-sądów-ocenia-znaleziska-a-ocenione-nie-wracają.

Jednostką jest znalezisko nad zdaniem, nazwane słowem z
:data:`olski.werdykt.ZGŁOSZENIA`, więc zgłoszenie dopisane do olskiego wchodzi
tu bez zmiany w tym module. Baza ocenia zgłoszenia, a nie same znaleziska,
bo to ona rozstrzyga, które zgłoszenie znaleziskiem zostaje. Zdanie o dwu znaleziskach stoi w bazie dwa razy.

Sonda pyta przy tym o zgłoszenia wraz z tymi, których wydruk domyślny nie ma:
``w_zdaniu`` niżej włącza rozszerzenie warstwy zaimkowej stojące za flagą
(``olski/odniesienia.py``). Bez tego reguła czekająca na awans nie miałaby jak go
dostać, bo awansują ją sądy z tej bazy, a wpisy do niej wypisuje ten przebieg.
Zgłoszenie spod flagi ma własną nazwę, więc obie reguły liczą się tu osobno.

Klas jest pięć, bo mówią o dwu rzeczach naraz: :data:`POTWIERDZONE` i
:data:`NAD_CZYSTYM` o regule, :data:`PRZEOCZONE` i :data:`ZDJĘTE` o gramatyce,
która od czasu sądu znalezisko zabrała — pierwsze jest stratą, drugie zakupem,
a obie liczby wychodzą z jednej zmiany — i :data:`NIECZYTANE` o zdaniu, którego
olski przestał czytać, bo ono o regule nie mówi nic.

Nowe idą w porządku ``sha256`` zdania, a nie po plikach: pierwszych ``--ile`` po
plikach byłoby pierwszym plikiem korpusu, a odcisk daje próbę rozrzuconą po
całości, tę samą w każdym przebiegu, z której ocenione wypadają same.

    python3 -m harness.sądy
    python3 -m harness.sądy --nowe proza/nkjp --ile 40 > nowe.txt
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import hashlib
import os
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from harness import pliki_prozy
from harness.wybory import wpisy
from olski.subset.deklaracja import WYRAŻENIE_PRZYIMKOWE
from olski.werdykt import WIELOZNACZNE, ZGŁOSZENIA, Verdict, Zdanie, nad_tekstem

#: Baza sądów, czyli jedyne miejsce, w którym ktoś ocenił znalezisko olskiego.
SĄDY = Path(__file__).parent.parent / "próba" / "nkjp-sądy.txt"

#: Czytelnik poprawiłby to, co znalezisko wskazuje.
TRAFNE = "trafne"

#: Czytelnik nie poprawiłby nic: znalezisko jest trafieniem fałszywym.
FAŁSZYWE = "fałszywe"

#: Sąd jeszcze niewydany. Wpis z nim czeka na przeczytanie, nie wchodzi do
#: żadnej liczby i nie zdejmuje znaleziska z następnego przebiegu.
PUSTY = "?"

#: Wartości, które klucz ``sąd`` przyjmuje.
WARTOŚCI_SĄDU = (TRAFNE, FAŁSZYWE, PUSTY)

#: Klucze, które wpis niesie; klucza spoza tej listy czytnik nie przemilcza,
#: bo literówka w kluczu gubi pole i nie widać tego po niczym.
#: ``kontekst`` bywa kilkoma wierszami, bo akapit bywa kilkoma zdaniami.
KLUCZE = ("plik", "kontekst", "zdanie", "znalezisko", "werdykt", "sąd", "powód")

#: Sąd mówi ``trafne`` i znalezisko dalej pada: reguła trafiła.
POTWIERDZONE = "potwierdzone"

#: Sąd mówi ``fałszywe`` i znalezisko dalej pada: trafienie fałszywe.
NAD_CZYSTYM = "nad czystym"

#: Sąd mówi ``trafne``, a znaleziska nie ma, choć olski zdanie czyta:
#: zmiana w gramatyce zabrała znalezisko, które czytelnik potwierdził.
PRZEOCZONE = "przeoczone"

#: Sąd mówi ``fałszywe`` i znaleziska już nie ma: trafienie fałszywe zeszło.
ZDJĘTE = "zdjęte"

#: Zdania olski nie czyta, więc znaleziska nie ma z powodu, który o regule nie
#: mówi nic. Osobno od :data:`ZDJĘTE`, bo tamto jest zakupem, a to stratą.
NIECZYTANE = "nieczytane"

#: Klasy w kolejności wydruku. Krotka, a nie zbiór, bo zbiór postawiony na drodze
#: do wydruku wypisuje w każdym przebiegu co innego.
KLASY = (POTWIERDZONE, NAD_CZYSTYM, PRZEOCZONE, ZDJĘTE, NIECZYTANE)

#: Kształty wieloznaczności, czyli to, czym czytania się różnią. Zdanie niesie
#: czasem kilka naraz i wtedy kształtem jest ich złożenie, ``przyłączenie+role``.
PRZYŁĄCZENIE = "przyłączenie"
ROLE = "role"
BUDOWA = "budowa"


@dataclass(frozen=True)
class Sąd:
    """Jedno znalezisko nad jednym zdaniem wraz z tym, co o nim powiedział czytelnik."""

    #: Warstwa i sekcja korpusu, z której zdanie wyszło.
    plik: str
    #: Zdania tego akapitu stojące przed zdaniem, w kolejności.
    kontekst: tuple[str, ...]
    zdanie: str
    #: Nazwa zgłoszenia z :data:`olski.werdykt.ZGŁOSZENIA`.
    znalezisko: str
    #: Wiersz, który ``olski-check`` wypisał nad tym zdaniem w chwili oceny.
    werdykt: str
    #: Jedna z :data:`WARTOŚCI_SĄDU`.
    sąd: str
    #: Na czym sąd stanął, bo sąd bez powodu jest zdaniem, którego nikt nie sprawdzi.
    powód: str

    @property
    def przeczytany(self) -> bool:
        return self.sąd != PUSTY

    @property
    def klucz(self) -> tuple[str, str]:
        """To, po czym następny przebieg poznaje znalezisko już ocenione."""
        return (self.zdanie, self.znalezisko)


@dataclass(frozen=True)
class Zestawienie:
    """Co dzisiejszy werdykt mówi o jednym zapisanym sądzie."""

    sąd: Sąd
    klasa: str
    #: Dzisiejszy wiersz werdyktu nad tym zdaniem.
    dzisiejsze: str
    #: Kształt dzisiejszej wieloznaczności, albo pusty napis, gdy jej nie ma.
    kształt: str

    @property
    def rozeszło_się(self) -> bool:
        """Czy werdykt ruszył się od chwili, w której ten sąd wydano."""
        return self.dzisiejsze != self.sąd.werdykt


def czytaj(path: Path = SĄDY) -> list[Sąd]:
    """Wpisy z pliku; wpis niepełny jest błędem, a nie ciszą.

    Wartości sądu i nazwy znaleziska pilnuje się tutaj, bo literówka w nich nie
    wywraca niczego, tylko cicho wypycha wpis z mianownika albo wpuszcza
    znalezisko z powrotem do przebiegu.
    """
    sądy = []
    for pola in wpisy(path, KLUCZE, ("zdanie", "znalezisko", "werdykt", "sąd")):
        znalezisko = pola["znalezisko"][0]
        if znalezisko not in ZGŁOSZENIA:
            raise ValueError(
                f"{path}: znalezisko {znalezisko!r} nie jest jednym z {', '.join(ZGŁOSZENIA)}"
            )
        sąd = pola["sąd"][0] or PUSTY
        if sąd not in WARTOŚCI_SĄDU:
            raise ValueError(f"{path}: sąd {sąd!r} nie jest jednym z {', '.join(WARTOŚCI_SĄDU)}")
        sądy.append(
            Sąd(
                plik=" ".join(pola.get("plik", ())),
                kontekst=tuple(pola.get("kontekst", ())),
                zdanie=pola["zdanie"][0],
                znalezisko=znalezisko,
                werdykt=pola["werdykt"][0],
                sąd=sąd,
                powód=" ".join(pola.get("powód", ())),
            )
        )
    return sądy


def werdykt_wpisu(sąd: Sąd) -> Zdanie:
    """Co olski mówi o zdaniu tego wpisu, czytanym za jego akapitem.

    Werdykt bierze się przez ``nad_tekstem``, czyli tą samą drogą, którą idzie
    ``olski-check``, bo zapisany ``werdykt`` jest wierszem tamtej komendy i druga
    droga do niego rozeszłaby się z nią po cichu. Akapit idzie przed zdaniem, bo
    znalezisko odniesieniowe czyta zdanie obok, a wpis je niesie.
    """
    zdania = nad_tekstem(" ".join((*sąd.kontekst, sąd.zdanie)), w_zdaniu=True)
    if not zdania or zdania[-1].werdykt.text != sąd.zdanie:
        raise ValueError(f"wpis, którego napis nie jest zdaniem swojego akapitu: {sąd.zdanie}")
    return zdania[-1]


def zestaw(sąd: Sąd) -> Zestawienie:
    """Zapytaj olskiego o zdanie tego wpisu i przyłóż odpowiedź do sądu."""
    zdanie = werdykt_wpisu(sąd)
    return Zestawienie(
        sąd=sąd,
        klasa=_klasa(sąd, sąd.znalezisko in zdanie.zgłoszenia, zdanie.werdykt.czytane),
        dzisiejsze=zdanie.werdykt.explain(),
        kształt=kształt(zdanie.werdykt) if sąd.znalezisko == WIELOZNACZNE else "",
    )


def _klasa(sąd: Sąd, pada: bool, czytane: bool) -> str:
    if pada:
        return POTWIERDZONE if sąd.sąd == TRAFNE else NAD_CZYSTYM
    if not czytane:
        return NIECZYTANE
    return PRZEOCZONE if sąd.sąd == TRAFNE else ZDJĘTE


def kształt(verdict: Verdict) -> str:
    """Czym różnią się czytania zdania wieloznacznego, tak jak nazywa to werdykt.

    Trzy składniki idą za trzema wierszami ``explain`` w ``olski/werdykt/zdanie.py``:
    przyłączenie nierozstrzygnięte, rola obsadzona inaczej i konstytuent o kilku
    czytaniach, ten ostatni z każdej rozbieżności, którą werdykt wypisuje, a nie
    tylko z tych, którym różnią się streszczenia. Rola wyrażenia przyimkowego nie
    liczy się osobno tam, gdzie nazywa ją przyłączenie, z tego samego powodu, dla
    którego tamten wiersz jej tam nie wypisuje.
    """
    if not (verdict.punktowane and verdict.result.ambiguous):
        return ""
    result = verdict.result
    składniki = []
    if result.przyłączenia:
        składniki.append(PRZYŁĄCZENIE)
    if any(
        not (result.przyłączenia and rola == WYRAŻENIE_PRZYIMKOWE) for rola in result.różniące
    ):
        składniki.append(ROLE)
    if result.rozbieżności:
        składniki.append(BUDOWA)
    return "+".join(składniki) or "inne"


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(zestawienia: Sequence[Zestawienie], czekające: int = 0) -> str:
    """Klasy na znalezisko, kształty wieloznaczności, a pod nimi wpis po wpisie.

    Zero wypisane, a nie pominięte: klasa, do której nie wpadł ani jeden wpis,
    jest odpowiedzią o tej bazie, a nie brakiem odpowiedzi. Znalezisko bez ani
    jednego sądu nie dostaje tabeli, bo tabela z samych zer mówi tylko tyle,
    że nikt jeszcze nie czytał.
    """
    szerokość = max(len(klasa) for klasa in KLASY)
    wiersze = [f"{len(zestawienia)} sądów o znaleziskach"]
    if czekające:
        wiersze[0] += f", a {czekające} wpisów czeka na sąd i nie wchodzi do liczb"
    for nazwa in ZGŁOSZENIA:
        swoje = [z for z in zestawienia if z.sąd.znalezisko == nazwa]
        if not swoje:
            continue
        ile = collections.Counter(z.klasa for z in swoje)
        wiersze += ["", f"  {nazwa}, {len(swoje)} sądów:"]
        wiersze += [f"  {ile[klasa]:>4}  {klasa}" for klasa in KLASY]

    kształty = sorted({z.kształt for z in zestawienia if z.kształt})
    if kształty:
        wiersze += ["", f"  {WIELOZNACZNE} po kształcie, potwierdzone / nad czystym:"]
        for k in kształty:
            klasy = [z.klasa for z in zestawienia if z.kształt == k]
            wiersze.append(
                f"  {klasy.count(POTWIERDZONE):>4} / {klasy.count(NAD_CZYSTYM):<4} {k}"
            )

    wiersze += ["", "  wpis po wpisie:"]
    wiersze += [_wypis(z, szerokość) for z in zestawienia]
    return "\n".join(wiersze)


def _wypis(zestawienie: Zestawienie, szerokość: int) -> str:
    """Wpis wraz z jego powodem, a wiersz werdyktu raz albo dwa razy.

    Dwa razy tam, gdzie werdykt ruszył się od chwili oceny: sąd wydano przy
    wierszu zapisanym i to on mówi, czego ten sąd dotyczył.
    """
    sąd = zestawienie.sąd
    wiersze = [f"  {zestawienie.klasa:>{szerokość}}  {sąd.znalezisko}: {sąd.zdanie}"]
    if zestawienie.rozeszło_się:
        wiersze.append(f"    zapisane: {sąd.werdykt}")
        wiersze.append(f"    dzisiaj:  {zestawienie.dzisiejsze}")
    else:
        wiersze.append(f"    {zestawienie.dzisiejsze}")
    if sąd.powód:
        wiersze.append(f"    {sąd.powód}")
    return "\n".join(wiersze)


# --------------------------------------------------------------------------- #
# Nowe znaleziska
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Znalezisko:
    """Jedno znalezisko olskiego nad zdaniem korpusu, wraz z akapitem i werdyktem."""

    plik: str
    kontekst: tuple[str, ...]
    zdanie: str
    znalezisko: str
    werdykt: str

    @property
    def klucz(self) -> tuple[str, str]:
        return (self.zdanie, self.znalezisko)

    @property
    def odcisk(self) -> str:
        return hashlib.sha256(f"{self.znalezisko}\n{self.zdanie}".encode()).hexdigest()


def _znaleziska_pliku(para: tuple[Path, Path]) -> list[Znalezisko]:
    korzeń, path = para
    return [
        Znalezisko(
            plik=str(path.relative_to(korzeń)),
            kontekst=zdanie.sąsiedztwo.zdania,
            zdanie=zdanie.werdykt.text,
            znalezisko=nazwa,
            werdykt=zdanie.werdykt.explain(),
        )
        for zdanie in nad_tekstem(path.read_text(encoding="utf-8"), w_zdaniu=True)
        for nazwa in zdanie.zgłoszenia
    ]


def znaleziska(korzeń: Path, jobs: int = 1) -> list[Znalezisko]:
    """Każde znalezisko olskiego pod tym katalogiem, w porządku odcisku.

    Akapit idzie z tej samej funkcji, która podaje go świadkowi w ``olski-check``,
    więc oceniający widzi to, co narzędzie.
    """
    pliki = [(korzeń, path) for path in pliki_prozy(korzeń)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as pula:
        listy = pula.map(_znaleziska_pliku, pliki, chunksize=8)
    return sorted((z for lista in listy for z in lista), key=lambda z: z.odcisk)


def nowe(
    znaleziska: Iterable[Znalezisko], ocenione: Iterable[tuple[str, str]]
) -> list[Znalezisko]:
    """Znaleziska, których baza jeszcze nie ma, w porządku podanym.

    To samo zdanie stoi w korpusie czasem w dwu sekcjach, a ocenia się je raz:
    drugie wystąpienie tego samego klucza nie wychodzi, bo wpis w bazie ma być
    jeden na znalezisko i sonda liczyłaby jeden sąd dwa razy.
    """
    widziane = set(ocenione)
    wybrane = []
    for z in znaleziska:
        if z.klucz not in widziane:
            widziane.add(z.klucz)
            wybrane.append(z)
    return wybrane


NAGŁÓWEK_NOWYCH = """\
# Znaleziska olskiego nad {korzeń}, których baza sądów jeszcze nie ma:
# {wypisane} z {nowych} nieocenionych, w porządku odcisku; ocenionych jest {ocenionych}.
# Wpisz `sąd` (trafne albo fałszywe) i `powód` i przenieś wpisy do próba/nkjp-sądy.txt.
"""


def zapisz(znaleziska: Sequence[Znalezisko], nagłówek: str = "") -> str:
    """Wpisy jako tekst pliku, z werdyktem i pustym sądem."""
    bloki = []
    for z in znaleziska:
        wiersze = [f"plik: {z.plik}"]
        wiersze += [f"kontekst: {zdanie}" for zdanie in z.kontekst]
        wiersze += [
            f"zdanie: {z.zdanie}",
            f"znalezisko: {z.znalezisko}",
            f"werdykt: {z.werdykt}",
            f"sąd: {PUSTY}",
            "powód:",
        ]
        bloki.append("\n".join(wiersze))
    return nagłówek + "\n" + "\n\n".join(bloki) + "\n"


# --------------------------------------------------------------------------- #
# Wiersz poleceń
# --------------------------------------------------------------------------- #


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.sądy",
        description="Zestaw dzisiejsze znaleziska olskiego z sądami przeczytanymi ręką.",
    )
    parser.add_argument(
        "ścieżka",
        nargs="?",
        help=f"baza sądów (domyślnie {SĄDY.parent.name}/{SĄDY.name}); "
        "przy --nowe katalog z prozą",
    )
    parser.add_argument(
        "--nowe",
        action="store_true",
        help="wypisz znaleziska nad prozą, których baza jeszcze nie ocenia",
    )
    parser.add_argument("--ile", type=int, default=40, help="ile znalezisk (domyślnie 40)")
    parser.add_argument(
        "--jobs",
        type=int,
        default=os.cpu_count() or 1,
        help="na ile procesów podzielić rozbiór przy --nowe",
    )
    args = parser.parse_args(argv)

    if args.nowe:
        if not args.ścieżka or not Path(args.ścieżka).is_dir():
            print("harness.sądy: --nowe żąda katalogu z prozą", file=sys.stderr)
            return 2
        korzeń = Path(args.ścieżka)
        ocenione = {sąd.klucz for sąd in czytaj()}
        wszystkie = znaleziska(korzeń, args.jobs)
        nieocenione = nowe(wszystkie, ocenione)
        wybrane = nieocenione[: args.ile]
        nagłówek = NAGŁÓWEK_NOWYCH.format(
            korzeń=korzeń,
            wypisane=len(wybrane),
            nowych=len(nieocenione),
            ocenionych=len(wszystkie) - len(nieocenione),
        )
        print(zapisz(wybrane, nagłówek), end="")
        return 0

    path = Path(args.ścieżka) if args.ścieżka else SĄDY
    if not path.is_file():
        print(f"harness.sądy: nie ma takiego pliku: {path}", file=sys.stderr)
        return 2
    sądy = czytaj(path)
    przeczytane = [sąd for sąd in sądy if sąd.przeczytany]
    print(wydruk([zestaw(sąd) for sąd in przeczytane], len(sądy) - len(przeczytane)))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
