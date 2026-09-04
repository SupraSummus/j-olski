"""Czy znalezisko wieloznaczności zgadza się z zapisanym sądem.

Baza sądów w ``próba/nkjp-wieloznaczność.txt`` mówi przy każdym zgłoszonym
zdaniu, ile rozumień ma nad nim czytelnik. Sąd ten wydała ręka i żaden przebieg
go nie odtworzy, a werdykt nad tym samym zdaniem rusza każde dopisanie do
gramatyki, więc bez tej sondy baza cichnie: wpis mówi o znalezisku, którego już
nie ma, albo milczy o tym, że znalezisko urosło. Sonda zestawia jedno z drugim.

**Klasy odpowiadają na dwa różne pytania.** Dwie mówią o samej regule:
:data:`POTWIERDZONE` i :data:`NAD_CZYSTYM` dzielą dzisiejsze znaleziska na
trafne i fałszywe, a to jest liczba, na której opiera się pytanie o to, czy
wieloznaczność ma być zgłaszana
(docs/open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma).
Dwie następne mówią o gramatyce, która się od czasu sądu ruszyła:
:data:`PRZEOCZONE` jest zawężeniem, które zeszło za daleko, a :data:`ZDJĘTE`
trafieniem fałszywym, które zeszło samo. Wpis, którego zdania olski przestał
czytać, nie mówi o żadnym z tych dwóch i liczy się osobno (:data:`NIECZYTANE`).

**Wiersz werdyktu porównuje się w całości, a nie samą klasę.** Znalezisko urosłe
z dwóch odczytań do sześciu zostaje w tej samej klasie, a sąd nad nim
przeczytano przy dwóch, więc wydruk pokazuje oba wiersze wszędzie tam, gdzie się
rozeszły, i to jest wezwanie do przeczytania wpisu na nowo.

    python3 -m harness.sądy
    python3 -m harness.sądy próba/nkjp-wieloznaczność.txt
"""

from __future__ import annotations

import argparse
import collections
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from harness.wybory import bloki
from olski.werdykt import Verdict, nad_tekstem

#: Baza sądów o trafieniach, czyli jedyne miejsce, w którym ktoś powiedział, ile
#: rozumień ma nad zgłoszonym zdaniem czytelnik.
SĄDY = Path(__file__).parent.parent / "próba" / "nkjp-wieloznaczność.txt"

#: Czytelnik ma nad tym zdaniem jedno rozumienie, więc znalezisko jest trafieniem
#: fałszywym.
JEDNOZNACZNE = "jednoznaczne"

#: Czytelnik ma nad tym zdaniem dwa rozumienia i zdanie nie mówi, które,
#: więc znalezisko jest trafne.
WIELOZNACZNE = "wieloznaczne"

#: Wartości, które klucz ``sąd`` przyjmuje. Trzeciej nie ma: wpis bez sądu jest
#: wpisem nieprzeczytanym, a taki do bazy nie wchodzi.
WARTOŚCI_SĄDU = (JEDNOZNACZNE, WIELOZNACZNE)

#: Klucze, które wpis niesie; klucza spoza tej listy czytnik nie przemilcza,
#: bo literówka w kluczu gubi pole i nie widać tego po niczym.
KLUCZE = ("plik", "zdanie", "znalezisko", "sąd", "powód")

#: Sąd mówi ``wieloznaczne`` i znalezisko dalej pada: reguła trafiła.
POTWIERDZONE = "potwierdzone"

#: Sąd mówi ``jednoznaczne`` i znalezisko dalej pada: trafienie fałszywe.
NAD_CZYSTYM = "nad czystym"

#: Sąd mówi ``wieloznaczne``, a znaleziska nie ma, choć olski zdanie czyta:
#: zawężenie zeszło za daleko i zabrało wieloznaczność, którą czytelnik ma.
PRZEOCZONE = "przeoczone"

#: Sąd mówi ``jednoznaczne`` i znaleziska już nie ma: trafienie fałszywe zeszło.
ZDJĘTE = "zdjęte"

#: Zdania olski nie czyta, więc znaleziska nie ma z powodu, który o regule nie
#: mówi nic. Osobno od :data:`ZDJĘTE`, bo tamto jest zakupem, a to stratą.
NIECZYTANE = "nieczytane"

#: Klasy w kolejności wydruku. Krotka, a nie zbiór, bo zbiór postawiony na drodze
#: do wydruku wypisuje w każdym przebiegu co innego.
KLASY = (POTWIERDZONE, NAD_CZYSTYM, PRZEOCZONE, ZDJĘTE, NIECZYTANE)


@dataclass(frozen=True)
class Sąd:
    """Jedno zgłoszone zdanie wraz z tym, ile rozumień ma nad nim czytelnik."""

    #: Warstwa i sekcja korpusu, z której zdanie wyszło.
    plik: str
    zdanie: str
    #: Wiersz, który ``olski-check`` wypisał nad tym zdaniem w chwili czytania.
    znalezisko: str
    #: Jedna z :data:`WARTOŚCI_SĄDU`.
    sąd: str
    #: Na czym sąd stanął, bo sąd bez powodu jest zdaniem, którego nikt nie sprawdzi.
    powód: str


@dataclass(frozen=True)
class Zestawienie:
    """Co dzisiejszy werdykt mówi o jednym zapisanym sądzie."""

    sąd: Sąd
    klasa: str
    #: Dzisiejszy wiersz werdyktu nad tym zdaniem.
    dzisiejsze: str

    @property
    def rozeszło_się(self) -> bool:
        """Czy werdykt ruszył się od chwili, w której ten sąd przeczytano."""
        return self.dzisiejsze != self.sąd.znalezisko


def czytaj(path: Path = SĄDY) -> list[Sąd]:
    """Wpisy z pliku; wpis niepełny jest błędem, a nie ciszą.

    Umowa jest ta sama, którą czyta ``czytaj`` w ``harness/wybory.py``, i podział
    na wpisy bierze się stamtąd (``bloki``). Wartości sądu pilnuje się tutaj, bo
    literówka w niej nie wywraca niczego, tylko cicho wypycha wpis z mianownika.
    """
    sądy = []
    for numer, blok in bloki(path.read_text(encoding="utf-8")):
        pola: dict[str, list[str]] = {}
        for wiersz in blok:
            klucz, _, wartość = wiersz.partition(":")
            if klucz not in KLUCZE:
                raise ValueError(f"{path}:{numer}: nieznany klucz {klucz!r}")
            pola.setdefault(klucz, []).append(wartość.strip())
        brakujące = {"zdanie", "znalezisko", "sąd"} - pola.keys()
        if brakujące:
            raise ValueError(f"{path}:{numer}: wpis bez {', '.join(sorted(brakujące))}")
        sąd = pola["sąd"][0]
        if sąd not in WARTOŚCI_SĄDU:
            raise ValueError(
                f"{path}:{numer}: sąd {sąd!r} nie jest jednym z {', '.join(WARTOŚCI_SĄDU)}"
            )
        sądy.append(
            Sąd(
                plik=" ".join(pola.get("plik", ())),
                zdanie=pola["zdanie"][0],
                znalezisko=pola["znalezisko"][0],
                sąd=sąd,
                powód=" ".join(pola.get("powód", ())),
            )
        )
    return sądy


def zestaw(sąd: Sąd) -> Zestawienie:
    """Zapytaj olskiego o zdanie tego wpisu i przyłóż odpowiedź do sądu.

    Werdykt bierze się przez ``nad_tekstem``, czyli tą samą drogą, którą idzie
    ``olski-check``, bo zapisane ``znalezisko`` jest wierszem tamtej komendy i
    druga droga do niego rozeszłaby się z nią po cichu.
    """
    zdania = nad_tekstem(sąd.zdanie)
    if not zdania:
        raise ValueError(f"wpis, którego napis nie jest zdaniem: {sąd.zdanie}")
    verdict = zdania[0].werdykt
    return Zestawienie(sąd=sąd, klasa=_klasa(sąd, verdict), dzisiejsze=verdict.explain())


def _klasa(sąd: Sąd, verdict: Verdict) -> str:
    if verdict.punktowane and verdict.result.ambiguous:
        return POTWIERDZONE if sąd.sąd == WIELOZNACZNE else NAD_CZYSTYM
    if not verdict.czytane:
        return NIECZYTANE
    return PRZEOCZONE if sąd.sąd == WIELOZNACZNE else ZDJĘTE


def wydruk(zestawienia: Sequence[Zestawienie]) -> str:
    """Liczby klas, a pod nimi wpis po wpisie, bo kierunek czyta człowiek.

    Zero wypisane, a nie pominięte: klasa, do której nie wpadł ani jeden wpis,
    jest odpowiedzią o tej bazie, a nie brakiem odpowiedzi.
    """
    ile = collections.Counter(z.klasa for z in zestawienia)
    szerokość = max(len(klasa) for klasa in KLASY)
    wiersze = [f"{len(zestawienia)} sądów o znalezisku wieloznaczności", ""]
    wiersze += [f"  {ile[klasa]:>4}  {klasa}" for klasa in KLASY]
    wiersze += ["", "  wpis po wpisie:"]
    wiersze += [_wypis(z, szerokość) for z in zestawienia]
    return "\n".join(wiersze)


def _wypis(zestawienie: Zestawienie, szerokość: int) -> str:
    """Wpis wraz z jego powodem, a wiersz werdyktu raz albo dwa razy.

    Dwa razy tam, gdzie werdykt ruszył się od chwili czytania: sąd przeczytano
    przy wierszu zapisanym i to on mówi, czego ten sąd dotyczył.
    """
    sąd = zestawienie.sąd
    wiersze = [f"  {zestawienie.klasa:>{szerokość}}  {sąd.zdanie}"]
    if zestawienie.rozeszło_się:
        wiersze.append(f"    zapisane: {sąd.znalezisko}")
        wiersze.append(f"    dzisiaj:  {zestawienie.dzisiejsze}")
    else:
        wiersze.append(f"    {zestawienie.dzisiejsze}")
    if sąd.powód:
        wiersze.append(f"    {sąd.powód}")
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.sądy",
        description="Zestaw dzisiejsze znaleziska wieloznaczności z sądami przeczytanymi ręką.",
    )
    parser.add_argument(
        "plik",
        nargs="?",
        help=f"baza sądów (domyślnie {SĄDY.parent.name}/{SĄDY.name})",
    )
    args = parser.parse_args(argv)
    path = Path(args.plik) if args.plik else SĄDY
    if not path.is_file():
        print(f"harness.sądy: nie ma takiego pliku: {path}", file=sys.stderr)
        return 2
    print(wydruk([zestaw(sąd) for sąd in czytaj(path)]))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
