"""Ile Świgra liczy jedno zdanie, obok tego samego zdania w olskim.

Rzeczą mierzoną jest czas, a nie pokrycie ani kształt drzewa.
Świgra rozbiera całą polszczyznę i płaci za to nawrotami,
bo swobodny szyk ma w ``sequence_of`` wyborem córki z worka,
a olski płaci raz, przy imporcie, bo szyk ma wypisany w produkcjach
(``olski/precedencja.py``).
Różnica ta jest wnioskiem z podzbioru i sonda mówi, ile ona wynosi.
Wynik czyta ``docs/swigra.md``.

**Czego ta liczba nie mówi.**
Sonda nie jest własnym potokiem Świgry,
więc czas Świgry wychodzi z niej ograniczeniem górnym, a nie jej wynikiem.
Wiązanie Morfeusza jest w pakiecie zbudowane pod SWI-Prolog 7.4 i 7.6,
więc wejście idzie tu ścieżką NKJP, czyli faktami ``input/9``,
a te powstają z Morfeusza 2 przez tłumaczenie znaczników,
którego dokładność orzeka sam ``znacznik_nkjp`` i nic poza nim.
Wejście jest przy tym szersze, niż ta ścieżka zwykle dostaje:
``gfjp2_morfologia_nkjp.pl`` kasuje interpretacje, których anotator nie wybrał,
a sonda podaje każdą, bo mierzy zdanie nierozstrzygnięte, tak jak olski.
Szukania to Świgrze nie ujmuje.
Wieloznaczność morfologiczna wchodzi wariantem na fakt,
tak jak ją zapisuje ``prepdataNKJP`` z korpusu,
a nie alternatywą, którą Świgra dostaje z Morfeusza.
Zdanie ponad budżetem wraca bez liczby, więc mediana mówi o zdaniach zmierzonych,
a zdanie ze znacznikiem, którego tłumaczenie nie objęło, wraca awarią osobno,
bo o Świgrze nie mówi nic.
Asymetria idzie przy tym na korzyść Świgry:
jej zegar mierzy sam rozbiór, a zegar olskiego całe ``check``,
czyli razem z morfologią i z werdyktem.

**Skąd wziąć parser.** ``swigra_current.zip`` ze strony projektu
(<https://zil.ipipan.waw.pl/Świgra>), rozpakowany,
a w nim gramatyka skompilowana i binarka zapisana jednym poleceniem.
Nazwa archiwum nie mówi, które to wydanie, więc mówi to odcisk pobrania,
po którym wyszły czasy w ``docs/swigra.md`` — ``sha256sum`` daje na nim
``0c87ba6ee3aa5ea5756189c13155cfd87309b48af903b8a3b59a426eb03d3513`` —
a odcisk inny znaczy, że upstream podmienił archiwum i liczba jest z innego parsera::

    sed -i s/--tradtional/--traditional/ birnam_dcg2pl
    LC_ALL=C.UTF-8 ./genparser -2

Żadna z tych dwóch poprawek nie jest wyborem.
Literówki w skrypcie SWI-Prolog 9 nie wybacza,
bo nieznaną opcję kończy wydrukiem pomocy,
a bez locale UTF-8 czyta gramatykę bajtami i wywraca się na pierwszym ogonku.
Świgra jest na GPL v3 i do drzewa tego repozytorium nie wchodzi;
katalog podaje się sondzie ścieżką.

    python3 -m harness.świgra proza/README.txt --świgra ~/swigra/parser
    python3 -m harness.świgra -c "Zapisz plik konfiguracyjny." --świgra ~/swigra/parser

Poprawka trzecia nie należy do budowania parsera, a do czytania jego lasu.
``portray('$VAR'(X)) :- format("_", [X])`` w ``gfjp_swidzinskify.pl``
podaje formatowi argument, dla którego napis nie ma dyrektywy,
na co SWI-Prolog 9 odpowiada ``format/2: Format error: too many arguments``,
więc zrzut łuków urywa się na pierwszym z nich, który niesie zmienną.
Za zrzutem drukują się ``info(trees, …)`` i ``info(useful_edges, …)``,
czyli liczba drzew i liczba łuków użytecznych, i te nie dochodzą wtedy do wydruku.
Czas przychodzi przed zrzutem, więc ta sonda mierzy dalej,
a każde zdanie kończy się wtedy błędem po stronie Prologu,
którego ``odczytaj`` nie widzi, bo pyta o ``parse_cputime``.
Kto pyta las o cokolwiek poza czasem, zamienia tamten wiersz na
``portray('$VAR'(_)) :- write('_').``
"""

from __future__ import annotations

import argparse
import os
import re
import statistics
import subprocess
import sys
import tempfile
import time
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from harness.komenda import Komenda, uruchom
from olski.morph import analyse
from olski.segmentacja import sentences
from olski.werdykt import check

#: Ile zdań pokazać pod liczbą. Sama mediana nie mówi, które zdanie zatrzymuje
#: Świgrę najdłużej, a zatrzymuje ją zdanie krótkie tak samo jak długie.
PRZYKŁADY = 5

#: Budżet na zdanie, w sekundach. Nad częścią zdań tej prozy Świgra nie kończy
#: w minutę, a sonda ma zmierzyć rozkład, a nie ogon.
BUDŻET = 45.0

#: Wartości znaczników, których NKJP nie ma, a Morfeusz 2 je wypisuje.
#: Rodzaj nijaki jest w NKJP rozdzielony na dwa, a liczebnościowe wyróżniki
#: stoją tam osobnym polem, więc schodzą.
WYRÓŻNIKI = frozenset({"col", "ncol", "pt"})

#: Pola ``info`` z wydruku Świgry, o które ta sonda pyta. Czas jest czasem
#: samego rozbioru, bo tak stawia je ``gfjp_analiza.pl``: zegar idzie między
#: ``parse`` a przetworzeniem lasu, więc nie liczy ani morfologii, ani wydruku.
POLE = re.compile(r"info\((parse_cputime|edges),([^)]+)\)")


def znacznik_nkjp(znacznik: str) -> str:
    """Znacznik Morfeusza 2 zapisany tagsetem, którego żąda gramatyka.

    Świgra czyta znaczniki NKJP i na nieznanej wartości rzuca wyjątkiem, a nie
    odrzuca zdania, więc różnica tagsetów jest tu awarią sondy, a nie wynikiem.
    Tłumaczenie jest zgrubne i o tyle właśnie liczba jest ograniczeniem górnym.
    """
    człony = [c for c in znacznik.split(":") if c not in WYRÓŻNIKI]
    return ":".join("n2" if c == "n" else c for c in człony)


@dataclass(frozen=True)
class Pomiar:
    """Jedno zdanie zmierzone po obu stronach."""

    zdanie: str
    #: Czas rozbioru Świgry w sekundach albo ``None``, gdy liczby nie oddała.
    świgra: float | None
    #: Ile łuków Świgra postawiła; ``None`` razem z czasem.
    krawędzie: int | None
    #: Czas olskiego w sekundach. Ten jest zawsze, bo olski kończy.
    olski: float
    #: Werdykt olskiego, żeby widać było, czy obie strony zdanie wzięły.
    werdykt: str
    #: Czemu czasu nie ma: ``budżet`` albo ``awaria``. ``None``, gdy jest.
    brak: str | None = None


def _doa(zdanie: str, plik: Path) -> None:
    """Zapisz zdanie jako wejście Świgry, czyli fakty ``input/9`` i ``analiza/1``.

    Morfologia wchodzi tu z ``olski.morph``, a nie z Morfeusza wprost, żeby oba
    parsery dostały ten sam graf segmentacji: sonda ma mierzyć czas, a nie
    różnicę dwóch wejść. Wariant idzie osobnym faktem, bo alternatywę
    ``nom.acc`` Świgra bierze od Morfeusza, a od korpusu jej nie dostaje.
    """
    wiersze, koniec = [], 0
    for i, segment in enumerate(analyse(zdanie)):
        koniec = max(koniec, segment.end)
        for czytanie in segment.readings:
            człony = [c.split(".") for c in znacznik_nkjp(czytanie.tag.raw).split(":")]
            for wybór in product(*człony):
                wiersze.append(
                    "input({},{},'{}','{}',{},nkjp:tak,'t{}','m{}',{}).".format(
                        segment.start,
                        segment.end,
                        segment.form.replace("'", "\\'"),
                        czytanie.lemma.replace("'", "\\'"),
                        ":".join(wybór),
                        i,
                        len(wiersze),
                        "sp" if segment.form[0].isalnum() else "nps",
                    )
                )
    tekst = zdanie.replace("'", "\\'")
    plik.write_text(
        "info(sample_id,'sonda').\n"
        "info(sent_id,'sonda/1').\n"
        f"info(startnode, 0).\ninfo(endnode, {koniec}).\n"
        f"info(tekst,'{tekst}').\ninfo(morph_ok, tak).\n"
        + "\n".join(wiersze)
        + f"\n:-analiza('{tekst}').\n",
        encoding="utf-8",
    )


def odczytaj(wydruk: str | None) -> tuple[float | None, int | None, str | None]:
    """Czas i łuki z wydruku Świgry albo powód, dla którego ich nie ma.

    ``None`` na wejściu znaczy budżet wyczerpany.
    Wydruk bez czasu znaczy awarię po stronie Prologu,
    a najczęściej znacznik, którego gramatyka nie zna:
    Świgra rzuca wtedy wyjątkiem, a nie odrzuca zdania.
    Zdaniem drogim taki wydruk nie jest i o Świgrze nie mówi nic,
    więc powód wraca osobno, bo pomiar zliczający awarie do budżetu
    wykazałby czas maszyny na cudzym parserze.
    """
    if wydruk is None:
        return None, None, "budżet"
    pola = dict(POLE.findall(wydruk))
    if "parse_cputime" not in pola:
        return None, None, "awaria"
    return float(pola["parse_cputime"]), int(pola.get("edges", 0)), None


def zmierz(zdanie: str, parser: Path, budżet: float) -> Pomiar:
    """Puść to zdanie przez oba parsery i oddaj oba czasy.

    Czas olskiego jest tu czasem pierwszego wywołania, jeżeli jest ono pierwsze
    w procesie, bo pamięci nad znacznikami zagrzewa dopiero ono; kto woła tę
    funkcję w pętli, robi jeden przebieg na rozgrzewkę (:func:`main`).
    """
    with tempfile.TemporaryDirectory() as katalog:
        plik = Path(katalog) / "zdanie.doa"
        _doa(zdanie, plik)
        try:
            wydruk = subprocess.run(
                ["swipl", "--traditional", "-x", str(parser / "gfjp2-bin"), "-t", "halt",
                 "-g", f"['{plik}']"],
                capture_output=True,
                text=True,
                timeout=budżet,
                # Gramatyka jest w UTF-8 i bez tego Świgra czyta ją bajtami;
                # reszta środowiska zostaje, bo w nim stoi ścieżka do swipla.
                env=os.environ | {"LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"},
            ).stdout
        except subprocess.TimeoutExpired:
            wydruk = None
    świgra, krawędzie, brak = odczytaj(wydruk)
    zegar = time.perf_counter()
    werdykty = check(zdanie)
    olski = time.perf_counter() - zegar
    return Pomiar(
        zdanie=zdanie,
        świgra=świgra,
        krawędzie=krawędzie,
        olski=olski,
        werdykt=werdykty[0].status if werdykty else "—",
        brak=brak,
    )


def wydruk(pomiary: list[Pomiar], przykłady: int, budżet: float) -> str:
    """Rozkład obu czasów, krotność między nimi, najdroższe zdania i braki.

    Braki idą dwoma wierszami, bo dwie rzeczy znaczą: budżet mówi o Świgrze,
    a awaria o tej sondzie i o tłumaczeniu znaczników w niej.
    """
    zmierzone = [p for p in pomiary if p.świgra is not None]
    wiersze = [
        f"{len(pomiary)} zdań, Świgra policzyła {len(zmierzone)} "
        f"w budżecie {budżet:g} s na zdanie"
    ]
    if not zmierzone:
        return wiersze[0]

    świgra = [p.świgra for p in zmierzone]
    olski = [p.olski for p in zmierzone]
    wiersze.append(
        f"Świgra: mediana {statistics.median(świgra):.2f} s, "
        f"najdłuższe {max(świgra):.2f} s, razem {sum(świgra):.1f} s"
    )
    wiersze.append(
        f"olski:  mediana {statistics.median(olski) * 1000:.1f} ms, "
        f"najdłuższe {max(olski) * 1000:.0f} ms, razem {sum(olski):.2f} s"
    )
    wiersze.append(
        f"krotność median {statistics.median(świgra) / statistics.median(olski):.0f}×, "
        f"krotność sum {sum(świgra) / sum(olski):.0f}×"
    )
    wiersze.append("")
    wiersze.append("najdroższe dla Świgry:")
    for p in sorted(zmierzone, key=lambda p: -p.świgra)[:przykłady]:
        wiersze.append(
            f"  {p.świgra:7.2f} s {p.krawędzie:6d} kraw. "
            f"{p.olski * 1000:6.1f} ms olski  {p.werdykt:9s} {p.zdanie}"
        )
    for powód, nagłówek in (("budżet", "ponad budżet"), ("awaria", "awaria sondy")):
        bez = [p for p in pomiary if p.brak == powód]
        if not bez:
            continue
        wiersze.append("")
        wiersze.append(f"{nagłówek} ({len(bez)}):")
        for p in bez[:przykłady]:
            wiersze.append(f"  {p.olski * 1000:6.1f} ms olski  {p.werdykt:9s} {p.zdanie}")
    return "\n".join(wiersze)


def _świgra(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--świgra",
        required=True,
        type=Path,
        help="katalog parser/ rozpakowanej Świgry, z binarką gfjp2-bin",
    )
    parser.add_argument(
        "--budżet",
        type=float,
        default=BUDŻET,
        help=f"ile sekund na zdanie (domyślnie {BUDŻET:g})",
    )


def przebieg(zdania: list[str], args: argparse.Namespace) -> str:
    """Zmierz każde zdanie i złóż z pomiarów jeden wydruk.

    Brak binarki kończy przebieg kodem 2, czyli tym samym, którym wiersz poleceń
    kończy pomyłkę w ścieżkach: jest to pomyłka tego samego rodzaju, a pyta o tę
    ścieżkę ta jedna sonda, więc i sprawdza się ją tutaj.
    """
    binarka = args.świgra / "gfjp2-bin"
    if not binarka.exists():
        print(
            f"harness.świgra: nie ma binarki {binarka}; docstring mówi, jak ją zbudować",
            file=sys.stderr,
        )
        raise SystemExit(2)

    # Pierwsze zdanie olskiego jest o rząd wielkości droższe od następnych, bo
    # dopiero ono zagrzewa pamięci nad znacznikami i nad leksykonem, i przy
    # jednym zdaniu podanym przez -c byłoby to całym pomiarem.
    check(zdania[0])

    # Przebieg nad prozą trwa godziny, bo zdanie ponad budżetem zabiera cały
    # budżet, więc każdy pomiar schodzi na bieżąco na standardowe wyjście błędów.
    # Wydruk sondy zostaje jeden i idzie na standardowe wyjście, tak jak w
    # pozostałych sondach; postęp nie jest wynikiem, a ratuje przebieg przerwany.
    pomiary = []
    for i, zdanie in enumerate(zdania, start=1):
        pomiary.append(zmierz(zdanie, args.świgra, args.budżet))
        ostatni = pomiary[-1]
        stan = ostatni.brak or f"{ostatni.świgra:.2f} s"
        print(f"{i}/{len(zdania)} {stan}", file=sys.stderr, flush=True)
    return wydruk(pomiary, args.przykłady, args.budżet)


def _proza(wejścia: Sequence[tuple[Path, str]], args: argparse.Namespace) -> str:
    return przebieg([z for _, tekst in wejścia for z in sentences(tekst)], args)


def _zdania(tekst: str, args: argparse.Namespace) -> str:
    return przebieg(sentences(tekst), args)


KOMENDA = Komenda(
    nazwa="harness.świgra",
    opis="ile Świgra liczy jedno zdanie, obok tego samego zdania w olskim",
    przykłady=PRZYKŁADY,
    proza=_proza,
    zdania=_zdania,
    argumenty=_świgra,
)


if __name__ == "__main__":
    raise SystemExit(uruchom(KOMENDA))
