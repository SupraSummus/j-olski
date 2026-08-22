"""Ile z meldowanej wieloznaczności zostaje, gdy czytania przejdą na kategorie dziedziny.

Werdykt olskiego liczy wyprowadzenia, a nie znaczenia, bo powstaje z czytań
gramatyki, a warstwa, która czytanie przenosi na drzewo dziedziny, stoi nad nim i
werdyktu nie rusza (``docs/architecture.md``). „Zdanie wieloznaczne” znaczy przez
to „ma kilka wyprowadzeń”, a czytelnik, któremu ten werdykt pokazano, pyta o
znaczenia. Sonda mierzy różnicę: puszcza czytania zdania przez ``abstrahuj`` w
``olski/skład/rozbiór.py`` i pyta, czy wracają z niego tymi samymi drzewami.

Porównywane są zbiory drzew, a nie ich liczba, i to jest tu pierwsze rozstrzygnięcie.
Jedno czytanie wraca kilkoma drzewami, bo napis milczy o relacji przyimka i o
znaczniku tematu (``docs/sklad.md``), więc suma drzew rośnie od tej ciszy tak
samo jak od wieloznaczności; pada ona natomiast pod każdym czytaniem tak samo,
więc porównanie zbiorów ją dzieli, a policzenie drzew miesza ją z odpowiedzią.

Pytanie ma przy tym warunek, który mierzy się przed nim. Zapis dziedziny
jest węższy od gramatyki, więc czytanie bywa, że nie wraca żadnym drzewem, a
zdanie, którego żadne czytanie nie wraca, nie mówi o wieloznaczności nic. Zdanie,
któremu odpadła połowa czytań, mówi o niej jeszcze mniej: wygląda na zwinięte, a
zwinęło się przez brak kategorii. Zdania dzielą się więc najpierw po zasięgu tego
zapisu, a zestawienie zbiorów pada dopiero pod tym z nich, którego każde czytanie
wróciło.

Powód, dla którego czytanie nie wraca, jest tu drugą odpowiedzią, a nie
przypisem. Zero kandydatów mówi, że kategorii nie ma i to jest miara tego, o ile
ten zapis musiałby urosnąć; kandydat, który powstał i wypisuje się innym napisem,
mówi co innego, bo kategorię ma, a oba kierunki nie zgadzają się co do jednego
zdania (``Odczyt`` w ``olski/skład/rozbiór.py``). Trzeciego rodzaju tu nie ma:
zdanie bez czytania do sondy nie wchodzi, więc pustka po werdykcie gramatyki nie
pada tu nigdy.

Zdania przyjęte liczą się obok wieloznacznych i to one są kontrolą. Zasięg
mierzony nad samymi wieloznacznymi nie mówi, czy zero wzięło się z
wieloznaczności, czy z rejestru, a zdanie jednoznaczne przechodzi tą samą drogą,
więc dwa wiersze obok siebie rozstrzygają to bez drugiego przebiegu. Drugi
kierunek liczy się przy okazji i za darmo: zdanie jednoznaczne, które wraca
kilkoma drzewami, jest miejscem, gdzie werdykt milczy, a zapis dziedziny widzi
wybór.

Morfologia złota daje po jednym czytaniu na formę, a ten rozbiór pyta krawędź o
wszystkie, więc nad bankiem drzew czyta wartości wybrane przez anotatorów. Źródło
morfologii jest przez to flagą, tak jak w ``olski-corpus``, i obie odpowiedzi mają
własną figurę: żywa daje pytaniu populację kilka razy większą od złotej i odpowiada
tak samo.

Wynik czyta ``docs/architecture.md``.

    python3 -m harness.znaczenia Składnica-frazowa-180723/
    python3 -m harness.znaczenia Składnica-frazowa-180723/ --morfologia live
    python3 -m harness.znaczenia proza/README.txt
"""

from __future__ import annotations

import argparse
import collections
import functools
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.komenda import Komenda, uruchom
from olski.corpus import read
from olski.coverage import SOURCES, po_kawałkach, segments_for
from olski.parse import MAX_READINGS, Node, Result, las, podsumuj
from olski.skład.rozbiór import abstrahuj, sygnatura
from olski.subset import DEKLARACJA, FRAGMENT, GRAMMAR, check

#: Ile zdań zachować pod każdym kluczem. Liczba bez zdania mówi, ile ich jest, i
#: nie mówi, czy zwinięcie, które nazywa, jest zwinięciem, które czytelnik ma.
PRZYKŁADY = 6

#: Trzy odpowiedzi o zasięgu tego zapisu nad jednym zdaniem, liczone po czytaniach.
#: ``CZĘŚĆ`` jest tu osobno od obu skrajności, bo to ono odbiera liczbie drzew
#: znaczenie: zdanie, któremu odpadła połowa czytań, zwija się przez brak.
WSZYSTKIE = "każde czytanie wraca drzewem"
CZĘŚĆ = "część czytań wraca drzewem"
ŻADNE = "żadne czytanie nie wraca drzewem"

#: Dwa rodzaje pustej odpowiedzi, rozdzielone liczbą kandydatów.
BEZ_KATEGORII = "zapis nie ma kategorii"
INNY_NAPIS = "kandydat wypisuje się innym napisem"

#: Czym są wobec siebie drzewa czytań jednego zdania, czyli ta odpowiedź, po którą
#: sonda tu jest; czemu zbiory, a nie liczba drzew, mówi nagłówek tego modułu.
#: Zbiory równe znaczą, że czytania mówią w tym zapisie jedno, więc zameldowana
#: wieloznaczność była wieloznacznością wyprowadzenia.
TE_SAME = "czytania dają te same drzewa"
CZĘŚĆ_WSPÓLNA = "drzewo wspólne stoi pod każdym czytaniem, a nie każde"
ROZŁĄCZNE = "żadne drzewo nie stoi pod każdym czytaniem"

#: Ile powodów wypisać. Powód niosący formę jest własnym wierszem, więc ogon tej
#: listy jest jednostkowy, a czoło nazywa to, czego temu zapisowi brakuje.
POWODÓW = 12


@dataclass(frozen=True)
class Odpowiedź:
    """Co ten zapis mówi o jednym zdaniu, złożone po wszystkich jego czytaniach.

    Osobno od licznika, bo o zdaniu rozstrzyga się tu dwa razy — raz zasięgiem, a
    raz zestawieniem drzew — i drugie pytanie pada tylko pod jedną odpowiedzią na
    pierwsze.
    """

    #: Które z trzech: ``WSZYSTKIE``, ``CZĘŚĆ`` albo ``ŻADNE``.
    zasięg: str
    #: Ile różnych drzew tego zapisu wróciło ze wszystkich czytań razem.
    drzewa: int
    #: Czym są wobec siebie zbiory drzew czytań; ``None``, gdy któreś nie wróciło,
    #: bo zbiór pusty jest brakiem kategorii, a nie odpowiedzią o znaczeniu.
    zestawienie: str | None
    #: Rodzaj pustej odpowiedzi, po jednym wpisie na czytanie, które nie wróciło.
    rodzaje: tuple[str, ...]
    #: Powody, każdy tyle razy, ile razy padł.
    powody: tuple[str, ...]


def odpowiedz(czytania: Sequence[Node]) -> Odpowiedź:
    """Puść czytania zdania przez zapis dziedziny i złóż z nich jedną odpowiedź.

    Drzewa zwijają się sygnaturą, a nie tożsamością obiektu, bo drzewa zbudowane
    z dwóch czytań nie mają jak dzielić obiektów, a pytanie jest o to, czy mówią
    to samo (``sygnatura`` w ``olski/skład/rozbiór.py``).

    Zbiór trzyma się przy tym osobno na każde czytanie i to jest cały pomiar.
    Suma odpowiada na inne pytanie, bo rośnie i od wieloznaczności, i od tego, o
    czym napis milczy, a te dwie rzeczy są tu po dwóch stronach.
    """
    zbiory: list[frozenset[tuple]] = []
    rodzaje: list[str] = []
    powody: list[str] = []
    for czytanie in czytania:
        odczyt = abstrahuj(czytanie)
        zbiory.append(frozenset(sygnatura(drzewo) for drzewo in odczyt.drzewa))
        if odczyt.drzewa:
            continue
        rodzaje.append(BEZ_KATEGORII if odczyt.kandydaci == 0 else INNY_NAPIS)
        powody.extend(odczyt.powody)
    if not zbiory:
        #  Zdanie bez czytań odrzuciła gramatyka i o tym zapisie nie mówi nic,
        #  a zbiory równe wyszłyby mu z pustego porównania.
        return Odpowiedź(ŻADNE, 0, None, (), ())
    zasięg = _zasięg_zdania(len(rodzaje), len(czytania))
    return Odpowiedź(
        zasięg,
        len(frozenset().union(*zbiory)),
        zestaw(zbiory) if zasięg == WSZYSTKIE else None,
        tuple(rodzaje),
        tuple(powody),
    )


def _zasięg_zdania(pustych: int, czytań: int) -> str:
    """Które z trzech, licząc czytania puste wobec wszystkich."""
    if not pustych:
        return WSZYSTKIE
    return ŻADNE if pustych == czytań else CZĘŚĆ


def zestaw(zbiory: Sequence[frozenset[tuple]]) -> str:
    """Czym są wobec siebie drzewa czytań tego zdania.

    Trzy odpowiedzi, bo dwie by kłamały. Zbiory równe znaczą, że czytania mówią
    w tym zapisie jedno, a zbiory bez ani jednego drzewa wspólnego, że mówią
    tyle rzeczy, ile ich jest. Między nimi stoi zdanie, którego czytania dzielą
    część drzew, i tam wieloznaczność zeszła, a nie zniknęła: nazwać ją zwinięciem
    albo przeżyciem znaczyłoby dopisać do pomiaru odpowiedź, której nie ma.

    Przecięcie liczy się po wszystkich czytaniach naraz, a nie parami, więc
    ``ROZŁĄCZNE`` mówi, że wspólnego nie ma nic ponad każdym z nich, i tyle
    właśnie stoi w jego nazwie.
    """
    if all(zbiór == zbiory[0] for zbiór in zbiory):
        return TE_SAME
    return CZĘŚĆ_WSPÓLNA if frozenset.intersection(*zbiory) else ROZŁĄCZNE


@dataclass
class Raport:
    """Co jeden przebieg naliczył."""

    ile_przykładów: int = PRZYKŁADY
    #: Zdania, o których werdykt cokolwiek mówi, czyli mianownik przebiegu.
    zmierzone: int = 0
    #: Werdykt olskiego, po jednym liczniku na trzy odpowiedzi.
    werdykty: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Zasięg zapisu dziedziny, pod kluczem werdyktu.
    zasięg: collections.Counter[tuple[str, str]] = field(default_factory=collections.Counter)
    #: Ile drzew ma zdanie, którego każde czytanie wróciło, pod kluczem werdyktu.
    drzewa: collections.Counter[tuple[str, int]] = field(default_factory=collections.Counter)
    #: Czym są wobec siebie drzewa czytań, liczone po zdaniach wieloznacznych.
    zestawienia: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Zdania o pełnym zasięgu, których lista czytań urwała się na ``MAX_READINGS``,
    #: więc o „każdym czytaniu” nie ma jak zapytać i do liczby drzew nie wchodzą.
    urwane: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Rodzaj pustej odpowiedzi, liczony po czytaniach, a nie po zdaniach.
    rodzaje: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Powody, którymi czytanie nie wróciło, liczone po czytaniach.
    powody: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Zdania zachowane pod kluczem, najkrótsze, z liczbą czytań.
    przykłady: dict[str, list[tuple[int, int, str]]] = field(default_factory=dict)
    #: Dlaczego zdanie nie weszło do żadnego licznika.
    pominięte: collections.Counter[str] = field(default_factory=collections.Counter)

    def zanotuj(self, klucz: str, przykład: tuple[int, int, str]) -> None:
        """Zachowaj zdanie pod kluczem, zostawiając najkrótsze.

        Najkrótsze, bo przykład ma być do przeczytania, a nie do przewinięcia, i
        bo wybór po długości nie zależy od kolejności, w jakiej kawałki wracają.
        """
        zachowane = self.przykłady.setdefault(klucz, [])
        zachowane.append(przykład)
        zachowane.sort()
        del zachowane[self.ile_przykładów :]


def policz(raport: Raport, tekst: str, wynik: Result) -> None:
    """Nalicz jedno zdanie wraz z jego werdyktem.

    Jedno miejsce na oba rejestry, bo bank drzew i proza różnią się tym, skąd
    werdykt przychodzi, a nie tym, o co się go pyta.
    """
    raport.zmierzone += 1
    raport.werdykty[wynik.status] += 1
    if wynik.rejected:
        return
    odpowiedź = odpowiedz(wynik.readings)
    raport.zasięg[(wynik.status, odpowiedź.zasięg)] += 1
    raport.rodzaje.update(odpowiedź.rodzaje)
    raport.powody.update(odpowiedź.powody)
    if odpowiedź.zasięg != WSZYSTKIE:
        raport.zanotuj(f"{wynik.status}, {odpowiedź.zasięg}", (len(tekst), wynik.ile, tekst))
        return
    if wynik.truncated:
        raport.urwane[wynik.status] += 1
        return
    raport.drzewa[(wynik.status, odpowiedź.drzewa)] += 1
    if not wynik.ambiguous:
        #  Zdanie jednoznaczne ma jedno czytanie, więc zestawienie wychodzi mu
        #  równością zawsze i wiersz o tym mówiłby o arytmetyce, a nie o zdaniu.
        raport.zanotuj(
            f"{wynik.status}, drzew tego zapisu: {odpowiedź.drzewa}",
            (len(tekst), wynik.ile, tekst),
        )
        return
    #  Zestawienie stoi tu zawsze, bo pada pod zasięgiem pełnym, a ten jest
    #  warunkiem wejścia w te wiersze; pustki nie ma więc czego liczyć.
    raport.zestawienia[odpowiedź.zestawienie] += 1
    klucz = f"{wynik.status}, {odpowiedź.zestawienie}"
    raport.zanotuj(klucz, (len(tekst), wynik.ile, tekst))


def nad_bankiem(ścieżki: Sequence[Path], morfologia: str, przykłady: int = PRZYKŁADY) -> Raport:
    """Jeden przebieg po lasach banku drzew, bez procesów pod spodem."""
    raport = Raport(przykłady)
    for ścieżka in ścieżki:
        zdanie = read(ścieżka)
        if not zdanie.annotated:
            continue
        segmenty = segments_for(zdanie, morfologia)
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        zbudowany = las(GRAMMAR, list(segmenty))
        policz(raport, zdanie.text, podsumuj(zbudowany, DEKLARACJA, zatrzymanie=False))
    return raport


def nad_prozą(tekst: str, przykłady: int = PRZYKŁADY) -> Raport:
    """To samo pytanie nad prozą, czyli nad rejestrem, w którym oba kierunki stoją.

    Fragment nie jest zdaniem i do mianownika nie wchodzi, tak samo jak nie
    wchodzi do sond różnicowych tego pakietu (``harness/ruch.py``).
    """
    raport = Raport(przykłady)
    for werdykt in check(tekst):
        if werdykt.status == FRAGMENT:
            raport.pominięte["fragment, a nie zdanie"] += 1
            continue
        policz(raport, werdykt.text, werdykt.result)
    return raport


def przebieg(
    ścieżki: Sequence[Path], jobs: int, morfologia: str, przykłady: int = PRZYKŁADY
) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport."""
    praca = functools.partial(nad_bankiem, morfologia=morfologia, przykłady=przykłady)
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden, przykłady włącznie."""
    scalony = Raport(przykłady)
    for raport in raporty:
        scalony.zmierzone += raport.zmierzone
        scalony.werdykty.update(raport.werdykty)
        scalony.zasięg.update(raport.zasięg)
        scalony.drzewa.update(raport.drzewa)
        scalony.zestawienia.update(raport.zestawienia)
        scalony.urwane.update(raport.urwane)
        scalony.rodzaje.update(raport.rodzaje)
        scalony.powody.update(raport.powody)
        scalony.pominięte.update(raport.pominięte)
        for klucz, zachowane in raport.przykłady.items():
            for przykład in zachowane:
                scalony.zanotuj(klucz, przykład)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


#: Kolejność werdyktów w tabelach. Stała, a nie po trafieniach, bo tabela z
#: zamienionymi wierszami czyta się jak inna tabela.
WERDYKTY = ("ambiguous", "valid")


def _wiersz(ile: int, razem: int, etykieta: object) -> str:
    """Wiersz tabeli: liczba, jej udział i to, o czym mówi."""
    return f"  {ile:>7}  {ile / razem:>6.1%}  {etykieta}"


def wydruk(raport: Raport, nagłówek: str) -> str:
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań z werdyktem",
        "",
        "  werdykt olskiego:",
        *(f"  {ile:>7}    {status}" for status, ile in raport.werdykty.most_common()),
        *(f"  {ile:>7}    niezmierzone: {powód}" for powód, ile in raport.pominięte.most_common()),
    ]
    wiersze += _zasięg(raport)
    wiersze += _zestawienia(raport)
    wiersze += _drzewa(raport)
    wiersze += _powody(raport)
    for klucz in sorted(raport.przykłady):
        wiersze += _przykłady(raport, klucz)
    return "\n".join(wiersze)


def _zasięg(raport: Raport) -> list[str]:
    """O ilu zdaniach tego rejestru zapis dziedziny w ogóle coś mówi, po werdyktach.

    Wiersz zdań jednoznacznych stoi tu po to, żeby zero w wierszu wyżej dało się
    przeczytać: zasięg jest własnością rejestru, a nie wieloznaczności, i dopiero
    różnica między dwoma wierszami mówi, czy jest inaczej.
    """
    if not raport.zasięg:
        return []
    wiersze = ["", "  ile czytań zdania wraca drzewem tego zapisu:"]
    for status in WERDYKTY:
        w_klasie = sum(ile for (klucz, _), ile in raport.zasięg.items() if klucz == status)
        if not w_klasie:
            continue
        wiersze.append(f"    {status}, {w_klasie} zdań:")
        for zasięg in (WSZYSTKIE, CZĘŚĆ, ŻADNE):
            wiersze.append(_wiersz(raport.zasięg.get((status, zasięg), 0), w_klasie, zasięg))
    return wiersze


def _zestawienia(raport: Raport) -> list[str]:
    """Co zapis dziedziny mówi o zdaniu wieloznacznym, czyli po co ta sonda jest.

    Mianownik stoi w nagłówku, bo jest nim populacja, nad którą to pytanie w
    ogóle pada: zdania wieloznaczne o pełnym zasięgu, z listą czytań nieurwaną.
    Sam ten mianownik jest tu połową odpowiedzi.
    """
    if not raport.zestawienia:
        return []
    razem = sum(raport.zestawienia.values())
    wiersze = ["", f"  czym są wobec siebie drzewa czytań, z {razem} zdań wieloznacznych:"]
    for zestawienie in (TE_SAME, CZĘŚĆ_WSPÓLNA, ROZŁĄCZNE):
        wiersze.append(_wiersz(raport.zestawienia.get(zestawienie, 0), razem, zestawienie))
    return wiersze


def _drzewa(raport: Raport) -> list[str]:
    """Ile drzew stoi nad zdaniem, którego każde czytanie wróciło.

    Wiersz zdań jednoznacznych jest tu podłogą szumu i po to ta tabela stoi:
    zdanie o jednym czytaniu wraca kilkoma drzewami, więc liczba drzew nad
    zdaniem wieloznacznym mierzy tę ciszę tak samo jak wieloznaczność, a
    rozdziela je dopiero zestawienie wyżej.
    """
    if not raport.drzewa and not raport.urwane:
        return []
    wiersze = ["", "  ile drzew tego zapisu ma zdanie, którego każde czytanie wróciło:"]
    for status in WERDYKTY:
        w_klasie = sum(ile for (klucz, _), ile in raport.drzewa.items() if klucz == status)
        urwane = raport.urwane.get(status, 0)
        if not w_klasie and not urwane:
            continue
        wiersze.append(f"    {status}, {w_klasie} zdań, ile drzew:")
        for (klucz, drzew), ile in sorted(raport.drzewa.items()):
            if klucz == status:
                wiersze.append(_wiersz(ile, w_klasie, drzew))
        if urwane:
            wiersze.append(f"  {urwane:>7}          poza tym, urwane na {MAX_READINGS} czytaniach")
    return wiersze


def _powody(raport: Raport) -> list[str]:
    """Czemu czytanie nie wróciło: najpierw rodzaj, potem powody słowo w słowo.

    Rodzaj stoi nad powodami, bo to on rozstrzyga, czym ta liczba jest:
    brak kategorii mówi, o ile ten zapis musiałby urosnąć, a inny napis mówi, że
    kategoria stoi, a kierunki mówią o jednym zdaniu co innego.
    """
    if not raport.rodzaje:
        return []
    razem = sum(raport.rodzaje.values())
    wiersze = ["", f"  czemu czytanie nie wraca drzewem, z {razem} takich czytań:"]
    for rodzaj, ile in raport.rodzaje.most_common():
        wiersze.append(_wiersz(ile, razem, rodzaj))
    wiersze += ["", f"  najczęstsze powody, z {len(raport.powody)} różnych:"]
    for powód, ile in raport.powody.most_common(POWODÓW):
        wiersze.append(f"  {ile:>7}  {powód}")
    return wiersze


def _przykłady(raport: Raport, klucz: str) -> list[str]:
    """Najkrótsze zdania pod kluczem, z liczbą czytań, bo klucz o niej nie mówi."""
    zachowane = raport.przykłady.get(klucz)
    if not zachowane:
        return []
    return [
        "",
        f"  najkrótsze zdania: {klucz}",
        *(f"    {czytań:>3} czytań  {tekst}" for _, czytań, tekst in zachowane),
    ]


def _morfologia(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--morfologia",
        choices=SOURCES,
        default="gold",
        help="skąd brać czytania form banku drzew; prozy ten wybór nie dotyczy",
    )


def _korpus(ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    raport = przebieg(ścieżki, args.jobs, args.morfologia, przykłady=args.przykłady)
    return wydruk(raport, f"Składnica, morfologia {args.morfologia}")


def _proza(tekst: str, ścieżka: Path, args: argparse.Namespace) -> str:
    return wydruk(nad_prozą(tekst, przykłady=args.przykłady), f"{ścieżka}, morfologia live")


KOMENDA = Komenda(
    nazwa="harness.znaczenia",
    opis="Policz, ile z meldowanej wieloznaczności zostaje w kategoriach dziedziny.",
    przykłady=PRZYKŁADY,
    korpus=_korpus,
    proza=_proza,
    argumenty=_morfologia,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
