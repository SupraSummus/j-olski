"""Czy koszt czytania jest skalą, czy samym porządkiem, liczone nad bankiem drzew.

Kolejność czytań ustala dziś koszt czytany od korzenia w dół, a nie suma po
drzewie (``wyprowadzenia`` w ``olski/parse/las.py``), więc o wielkości różnicy
między dwoma czytaniami nie orzeka nic. Ta sonda pyta, ile ta wielkość jest
warta, i pyta o to trzema wydrukami, bo trzy różne rzeczy mogą ją unieważnić.

**Wariant cennika** mówi, ile pozycja kupuje: cena zmieniona, a pod nią złote
czytanie pierwsze.

**Porządek po sumie** mówi, ile kosztuje spłaszczenie hierarchii do liczby:
złote czytanie pierwsze pod sumą po całym drzewie wobec tego samego pod
porządkiem dzisiejszym.

**Rozstęp sum** mówi, co znaczy różnica: przy jakim rozstępie między najtańszą
sumą a następną najtańsze czytanie bywa złotym.

Morfologia rozstrzyga, którą rodzinę cennika ten przebieg w ogóle widzi.
Pod złotą pozycja morfologii jest zerem przy każdej formie, bo odczytanie wzięte
z drzewa kwalifikatora nie niesie, więc wycenia ją dopiero żywa.

Wywód, z którego ta sonda wynika, trzyma
docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie.

    python3 -m harness.skala Składnica-frazowa-180723/
    python3 -m harness.skala Składnica-frazowa-180723/ --cena okolicznik=0
    python3 -m harness.skala Składnica-frazowa-180723/ --morfologia żywa
"""

from __future__ import annotations

import argparse
import collections
import contextlib
import functools
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.corpus import pliki, read
from harness.pomiar import po_kawałkach, przenumerowane
from olski import cennik
from olski.parse import las, podsumuj
from olski.subset import build
from olski.werdykt.wykazy import koszty_drzewa

#: Odczytania wzięte z drzewa wzorcowego, po jednym na formę.
ZŁOTA = "złota"

#: Odczytania z Morfeusza, ponumerowane terminalami tego drzewa
#: (``przenumerowane`` w ``harness/pomiar.py``).
ŻYWA = "żywa"

#: Nazwy morfologii w kolejności wydruku pomocy.
MORFOLOGIE = (ZŁOTA, ŻYWA)

#: Role, którymi rozpoznaje się złote czytanie. Ta sama lista, którą mierzy
#: ``harness/pomiar.py``, bo rozejście się tych dwóch zrobiłoby dwie miary o
#: jednej nazwie.
ROLE = ("podmiot", "dopełnienie")

#: Ile czytań zdania wolno wyliczyć. Suma złotego czytania porównuje się tu z
#: sumami wszystkich pozostałych, więc czytania pominąć nie wolno: pominięte
#: bywa tańsze i numer wychodzi wtedy za niski. Zdanie o lesie większym od tej
#: granicy wypada więc z mianownika i wydruk je liczy osobno.
GRANICA = 3000


@contextlib.contextmanager
def ceny(nowe: dict[str, int]) -> Iterator[None]:
    """Cennik z tymi pozycjami przecenionymi, na czas budowania gramatyki.

    Cena wchodzi do produkcji przy jej powstaniu (``Production.__post_init__``
    w ``olski/grammar.py``), więc wariant robi się przeceną tabeli i ponownym
    zbudowaniem gramatyki. Drugiego uchwytu na cenę nie ma i nie ma go po co
    dokładać: podzbiór ma jedną deklarację i cennik jest jej częścią.
    """
    stare = dict(cennik.CENNIK)
    cennik.CENNIK.update(nowe)
    try:
        yield
    finally:
        cennik.CENNIK.clear()
        cennik.CENNIK.update(stare)


@functools.cache
def gramatyka(wariant: tuple[tuple[str, int], ...]):
    """Gramatyka pod tym wariantem cennika, budowana raz na proces roboczy.

    Budowa kosztuje ułamek sekundy, a przez granicę procesu idzie wtedy sam
    wariant, czyli kilka par, zamiast tysiąca kilkuset produkcji.
    """
    with ceny(dict(wariant)):
        return build()


@dataclass(frozen=True, kw_only=True)
class Zdanie:
    """Jedno zdanie banku drzew zmierzone pod jednym wariantem."""

    #: Numer złotego czytania w kolejności dzisiejszej, licząc od jednego.
    numer: int
    #: Suma cennika każdego czytania, w tej samej kolejności.
    sumy: tuple[int, ...]

    @property
    def złota(self) -> int:
        return self.sumy[self.numer - 1]

    @property
    def pierwsze_dziś(self) -> bool:
        return self.numer == 1

    @property
    def pierwsze_pod_sumą(self) -> bool:
        """Czy złote czytanie wyszłoby pierwsze, gdyby porządkowała suma.

        Remis rozstrzyga kolejność dzisiejsza, więc czytanie o tej samej sumie
        stojące dziś wcześniej wyprzedza złote i tutaj.
        """
        tańsze = any(suma < self.złota for suma in self.sumy)
        równe_przed = any(suma == self.złota for suma in self.sumy[: self.numer - 1])
        return not tańsze and not równe_przed

    @property
    def rozstęp(self) -> int | None:
        """O ile najtańsza suma jest tańsza od następnej; ``None``, gdy nie jest jedna.

        Zdanie, którego najtańszą sumę ma kilka czytań, rozstępu nie ma i suma
        nie rozstrzyga w nim wyboru, więc trafności takiego zdania nie liczy się
        razem z resztą. Wartość następna zawsze tu jest: zdanie jest wieloznaczne,
        więc jedna wartość sumy znaczy kilka czytań pod nią i wychodzi warunkiem
        wyżej.
        """
        ile = collections.Counter(self.sumy)
        wartości = sorted(ile)
        if ile[wartości[0]] > 1:
            return None
        return wartości[1] - wartości[0]

    @property
    def najtańsze_złote(self) -> bool:
        return self.złota == min(self.sumy)


@dataclass
class Raport:
    """Co przebieg policzył: zdania zmierzone i te, które wypadły z mianownika."""

    zdania: list[Zdanie] = field(default_factory=list)
    #: Zdania wieloznaczne o lesie większym od :data:`GRANICA`.
    za_duże: int = 0
    #: Zdania wieloznaczne, w których złote czytanie przepadło.
    bez_złotego: int = 0
    #: Zdania, które morfologia żywa dzieli inaczej niż drzewo wzorcowe
    #: (:func:`harness.pomiar.przenumerowane`). Pod morfologią złotą zero.
    inna_segmentacja: int = 0

    def dołóż(self, inny: Raport) -> None:
        self.zdania.extend(inny.zdania)
        self.za_duże += inny.za_duże
        self.bez_złotego += inny.bez_złotego
        self.inna_segmentacja += inny.inna_segmentacja


def zmierz(
    ścieżki: Sequence[Path], wariant: tuple[tuple[str, int], ...], morfologia: str = ZŁOTA
) -> Raport:
    """Przeczytaj te lasy i zmierz w nich złote czytanie pod tym wariantem.

    Przecena obejmuje cały przebieg, a nie samo budowanie gramatyki, bo cenę
    czyta się tu dwa razy: raz przy produkcji, która ustala kolejność, i raz w
    :func:`olski.cennik.suma` nad wyliczonym drzewem. Przecena zdjęta po budowie
    dawała kolejność wariantu pod sumami cennika dzisiejszego, czyli dwie
    połowy wydruku spod dwóch różnych tabel.
    """
    raport = Raport()
    with ceny(dict(wariant)):
        gramatyka_wariantu = gramatyka(wariant)
        for ścieżka in ścieżki:
            zdanie = read(ścieżka)
            if not zdanie.annotated or not zdanie.całe or not zdanie.roles:
                continue
            segmenty = list(zdanie.segments) if morfologia == ZŁOTA else przenumerowane(zdanie)
            if segmenty is None:
                raport.inna_segmentacja += 1
                continue
            if not segmenty:
                continue
            zbudowany = las(gramatyka_wariantu, segmenty)
            wynik = podsumuj(zbudowany)
            if not wynik.ambiguous:
                continue
            # Granica przed pytaniem o numer, bo numer kosztuje wyliczanie, a pod
            # wariantem, który złote czytanie spycha w dół, kosztuje cały las.
            if wynik.ile > GRANICA:
                raport.za_duże += 1
                continue
            numer = zbudowany.numer_czytania({rola: zdanie.spans(rola) for rola in ROLE})
            if numer is None:
                raport.bez_złotego += 1
                continue
            sumy = tuple(cennik.suma(koszty_drzewa(drzewo)) for drzewo in zbudowany.czytania())
            raport.zdania.append(Zdanie(numer=numer, sumy=sumy))
    return raport


def przebieg(
    ścieżki: Sequence[Path],
    jobs: int,
    wariant: tuple[tuple[str, int], ...],
    morfologia: str = ZŁOTA,
) -> Raport:
    """Zmierz wszystkie lasy na tylu procesach, ile podano, i złóż jeden raport."""
    scalony = Raport()
    praca = functools.partial(zmierz, wariant=wariant, morfologia=morfologia)
    for kawałek in po_kawałkach(ścieżki, jobs, praca):
        scalony.dołóż(kawałek)
    return scalony


def _tabela_rozstępu(zdania: Sequence[Zdanie]) -> list[str]:
    """Rozstęp sum wobec tego, jak często najtańsze czytanie jest złotym."""
    kubełki: dict[int | None, list[int]] = collections.defaultdict(lambda: [0, 0])
    for zdanie in zdania:
        kubełek = kubełki[zdanie.rozstęp]
        kubełek[0] += zdanie.najtańsze_złote
        kubełek[1] += 1
    wiersze = ["", "rozstęp sum, a pod nim złote czytanie wśród najtańszych:"]
    for rozstęp in sorted(kubełki, key=lambda r: (r is None, r)):
        trafione, wszystkie = kubełki[rozstęp]
        nazwa = "suma nie rozstrzyga" if rozstęp is None else f"rozstęp {rozstęp}"
        wiersze.append(f"  {nazwa:>22}: {trafione:>5} / {wszystkie:<5} {trafione / wszystkie:6.1%}")
    return wiersze


def wydruk(raport: Raport, nagłówek: str) -> str:
    """Trzy odpowiedzi tej sondy, w kolejności, w jakiej się je czyta."""
    zdania = raport.zdania
    dziś = sum(zdanie.pierwsze_dziś for zdanie in zdania)
    pod_sumą = sum(zdanie.pierwsze_pod_sumą for zdanie in zdania)
    wartości = collections.Counter(len(set(zdanie.sumy)) for zdanie in zdania)
    wiersze = [
        nagłówek,
        "",
        f"zdań wieloznacznych ze złotym czytaniem: {len(zdania)}",
        f"  wypadło za granicą {GRANICA} czytań: {raport.za_duże}",
        f"  złote czytanie przepadło: {raport.bez_złotego}",
        f"  segmentacja rozeszła się z terminalami: {raport.inna_segmentacja}",
        "",
        f"złote czytanie pierwsze, porządek dzisiejszy: {dziś}",
        f"złote czytanie pierwsze, porządek po sumie:   {pod_sumą}",
        "",
        "ile różnych sum ma zdanie:",
        *(f"  {ile:>3}: {zdań}" for ile, zdań in sorted(wartości.items())),
        *_tabela_rozstępu(zdania),
    ]
    return "\n".join(wiersze)


def _cena(wpis: str) -> tuple[str, int]:
    """``pozycja=liczba`` rozłożone na parę, z nazwą sprawdzoną w cenniku."""
    nazwa, _, wartość = wpis.partition("=")
    if nazwa not in cennik.CENNIK:
        raise argparse.ArgumentTypeError(f"cennik nie ma pozycji o nazwie {nazwa!r}")
    try:
        return nazwa, int(wartość)
    except ValueError:
        raise argparse.ArgumentTypeError(f"cena {wartość!r} nie jest liczbą") from None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.skala",
        description="Czy koszt czytania jest skalą, czy samym porządkiem.",
    )
    parser.add_argument("root", help="katalog z rozpakowaną Składnicą")
    parser.add_argument(
        "--cena",
        action="append",
        type=_cena,
        default=[],
        metavar="POZYCJA=LICZBA",
        help="przecena pozycji cennika na czas przebiegu; wolno podać kilka razy",
    )
    parser.add_argument(
        "--morfologia",
        choices=MORFOLOGIE,
        default=ZŁOTA,
        help="odczytania anotatora albo Morfeusza; pozycję morfologii wycenia tylko żywa",
    )
    parser.add_argument("--jobs", type=int, default=1, help="ile procesów liczy")
    args = parser.parse_args(argv)
    if args.jobs < 1:
        parser.error("--jobs takes at least one process")
    wariant = tuple(args.cena)
    przecena = ", ".join(f"{nazwa} = {wartość}" for nazwa, wartość in wariant)
    raport = przebieg(pliki(args.root), args.jobs, wariant, args.morfologia)
    nagłówek = f"{przecena or 'cennik dzisiejszy'}, morfologia {args.morfologia}"
    print(wydruk(raport, nagłówek))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
