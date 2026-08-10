"""Ustawa w HTML-u wchodzi, polskie zdania wychodzą.

Ustawa nie jest ciągiem zdań, tylko drzewem jednostek redakcyjnych,
i tekst większości z nich zdaniem nie jest:

    Art. 1. Ustawa określa:
      1) zadania ochrony ludności i obrony cywilnej;
      2) organy i podmioty realizujące zadania ochrony ludności i obrony cywilnej;

Zdaniem jest tu dopiero gałąź: przesłanka złożona z każdą pozycją po kolei.
Więc ten krok składa drzewo w zdania, a nie przepisuje tekst jednostka po jednostce.
Bez składania gramatyka dostałaby urywki,
a orzeczenie „to nie zdanie” mówiłoby o zapisie ustawy, a nie o polszczyźnie w niej.

Cena jest po drugiej stronie i jest jedna: przesłanka wychodzi tyle razy, ile ma pozycji.
Reguła, która liczy częstość nad tekstem, liczyłaby ją wielokrotnie,
więc ta proza idzie pod gramatykę, a nie pod pakiet reguł.
Właścicielem pozostałych cen jest docs/ustawy.md.

Wejściem jest HTML z API ELI, bo tam ustawa stoi jednostka w jednostce,
a wydawca znaczy klasą to, co jest jej tekstem, i to, co jest cytatem z innej.
Czym one są i skąd się biorą, mówi dokument wyżej;
tutaj stoi to, co z nich zostaje.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from html.parser import HTMLParser

from harness import Czytnik, Jednostka, uruchom

SUFIKS_HTML = ".html"

#: Klasa, którą wydawca znaczy jednostkę redakcyjną.
JEDNOSTKA_REDAKCYJNA = "unit"

#: Jednostki, które są pozycją wyliczenia: punkt i litera.
#: Tylko one ciągną zdanie jednostki nad sobą,
#: bo tylko wyliczenie dzieli przesłankę między pozycje,
#: a artykuł, paragraf i ustęp stoją same.
#: Zszywa ta lista, a nie jej brak,
#: więc jednostka typu, którego wydawca tu nie ma, też zostaje osobno.
POZYCJE_WYLICZENIA = frozenset({"unit_pint", "unit_lett"})

#: Atrybut, którym wydawca znaczy tekst jednostki, w odróżnieniu od jej numeru:
#: numer stoi w nagłówku, a nagłówek jest aparatem i odpada razem z nim.
TEKST = "xText"

#: Poddrzewa, które prozą tej ustawy nie są, i tyle ich jest.
#: ``cite-box`` trzyma jednostki ustawy zmienianej, a więc cudzy tekst w cudzysłowie;
#: ``xHidden`` i ``tooltip-text`` trzymają adresy publikacji i przypisy,
#: które wydawca wstawia w środek zdania, a których nikt w nim nie napisał.
#: Aparat samej strony wpisu tu nie potrzebuje: spis treści, przypisy pod ustawą
#: i nagłówki jednostek nie niosą tekstu jednostki, a tylko po niego ten krok sięga.
POMIJANE = frozenset({"cite-box", "xHidden", "tooltip-text"})

#: Odsyłacz do przypisu, czyli ``1)`` w indeksie górnym.
POMIJANE_ZNACZNIKI = frozenset({"sup"})

#: Znaczniki, które zamknięcia nie mają, więc nie otwierają też głębokości.
#: Bez tej listy znacznik pusty w środku jednostki zabrałby zamknięcie tego,
#: co go otacza, i jednostka zamknęłaby się o jeden znacznik za wcześnie.
PUSTE = frozenset({"br", "img", "hr", "meta", "link", "input", "col", "source"})

#: Ten jeden z nich renderuje się odstępem, a nie niczym,
#: więc bez niego dwa słowa złamane wierszem doszłyby do reguł sklejone w jedno.
ZŁAMANIE = "br"

#: Czym jednostka kończy tekst, gdy ciąg dalszy stoi pod nią.
#: Dwukropek otwiera wyliczenie, a średnik i przecinek zamykają jego pozycję,
#: więc każdy z nich znika w miejscu zszycia.
#: Kropka jest tam z tego samego powodu, tylko przychodzi z niższej gałęzi:
#: zdanie składa się z gałęzi już złożonych, a kropkę stawia dopiero to złożone.
SZWY = ":;,."

#: Ile spacji zostaje z tego, co w HTML-u jest wcięciem, i z twardej spacji.
BIAŁE = re.compile(r"\s+")

#: Ślady po tym, co odpadło ze środka zdania.
#: Adres publikacji stoi w nawiasie wstawionym między przecinek i przecinek,
#: więc po nim zostaje przecinek podwojony albo przecinek z odstępem przed sobą,
#: a jedno i drugie doszłoby do reguł jako znak, który ktoś wpisał.
ŚLADY = ((re.compile(r"\s+(?=[,;:.])"), ""), (re.compile(r",(\s*,)+"), ","))


@dataclass
class Przepis:
    """Jednostka redakcyjna: jej własny tekst i jednostki, które pod nią stoją.

    Jedna lista, a nie dwie, bo o zszyciu rozstrzyga kolejność:
    tekst przed pozycjami jest przesłanką,
    a tekst za nimi zakończeniem, które do każdej z nich należy tak samo:
    ``Kto`` stoi nad pozycjami, a ``podlega karze grzywny`` pod nimi.
    """

    pozycja: bool = False
    części: list[str | Przepis] = field(default_factory=list)


def zdania(przepis: Przepis) -> Iterator[str]:
    """Wypuść każdą gałąź jednostki jako jedno zdanie.

    Jednostka, pod którą nie ma wyliczenia, wypuszcza swój tekst tak, jak stoi,
    a jednostki pod nią wypuszczają swoje: artykuł nie dzieli zdania z ustępem.
    Jednostka z wyliczeniem wypuszcza każdą pozycję osobno,
    a przesłankę i zakończenie dokłada do wszystkich,
    bo pozycje są wobec siebie alternatywami, a nie ciągiem.

    Zdanie wychodzi z kropką na końcu, choćby gałąź kończyła się średnikiem.
    Jest to jedyna rzecz, którą ten krok dopisuje,
    a dopisuje ją dlatego, że gramatyka pyta o zdanie:
    bez kropki werdykt brzmiałby „to nie zdanie”
    nad każdą pozycją każdego wyliczenia w ustawie.
    """
    wyliczenie = [część for część in przepis.części if _pozycja(część)]
    if not wyliczenie:
        for część in przepis.części:
            if isinstance(część, str):
                if zdanie := _zszyj([część]):
                    yield zdanie
            else:
                yield from zdania(część)
        return
    otwarcie = next(i for i, część in enumerate(przepis.części) if _pozycja(część))
    przed = [część for część in przepis.części[:otwarcie] if isinstance(część, str)]
    po = [część for część in przepis.części[otwarcie:] if isinstance(część, str)]
    for pozycja in wyliczenie:
        for zdanie in zdania(pozycja):
            yield _zszyj([*przed, zdanie, *po])
    #  Jednostka, która ma pod sobą wyliczenie i jednostkę stojącą samą, wypuszcza
    #  tamtą osobno. Przesłanki jej nie dokładamy, bo nie po to tam stoi.
    for część in przepis.części:
        if isinstance(część, Przepis) and not _pozycja(część):
            yield from zdania(część)


def _pozycja(część: str | Przepis) -> bool:
    """Czy ta część jednostki jest pozycją wyliczenia, a więc ciągnie zdanie nad sobą."""
    return isinstance(część, Przepis) and część.pozycja


def _zszyj(części: Iterable[str]) -> str:
    """Złóż gałąź w jedno zdanie, zdejmując punktację po drodze.

    Znak zszycia idzie precz razem z ostatnim,
    bo ustawa punktuje jednostkę tym, co pod nią stoi,
    a złożone zdanie ma pod sobą już tylko koniec.
    """
    zszyte = " ".join(część.rstrip(SZWY + " ") for część in części if część.strip(SZWY + " "))
    for ślad, czym in ŚLADY:
        zszyte = ślad.sub(czym, zszyte)
    return f"{zszyte}." if zszyte else ""


class Akt(HTMLParser):
    """Drzewo jednostek jednej ustawy, złożone z tego, co wydawca znaczy klasą.

    Głębokość jest liczona, a nie zgadywana ze wcięcia:
    jednostka stoi w jednostce, poddrzewo pomijane też,
    a bez licznika koniec zagnieżdżonego odsyłacza zamykałby cały przypis.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.akt = Przepis()
        self._stos = [self.akt]
        #: Otwarte znaczniki, jeden wpis na znacznik, od najgłębszego.
        #: Wpis mówi, co zamknie jego koniec: jednostkę, tekst, poddrzewo albo nic.
        self._otwarte: list[str | None] = []
        self._tekst: list[str] | None = None
        self._pomijane = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == ZŁAMANIE:
            self.handle_data(" ")
        if tag not in PUSTE:
            atrybuty = {nazwa.lower(): (wartość or "") for nazwa, wartość in attrs}
            self._otwarte.append(self._otwiera(tag, atrybuty))

    def _otwiera(self, tag: str, atrybuty: dict[str, str]) -> str | None:
        """Co ten znacznik otwiera, czyli co zamknie jego koniec."""
        klasy = set(atrybuty.get("class", "").split())
        if klasy & POMIJANE or tag in POMIJANE_ZNACZNIKI:
            self._pomijane += 1
            return "pomijane"
        if self._pomijane:
            return None
        if atrybuty.get("data-template") == TEKST:
            self._tekst = []
            return "tekst"
        if JEDNOSTKA_REDAKCYJNA in klasy:
            jednostka = Przepis(pozycja=bool(klasy & POZYCJE_WYLICZENIA))
            self._stos[-1].części.append(jednostka)
            self._stos.append(jednostka)
            return "jednostka"
        return None

    def handle_endtag(self, tag: str) -> None:
        if tag in PUSTE:
            return
        rola = self._otwarte.pop() if self._otwarte else None
        if rola == "pomijane":
            self._pomijane -= 1
        elif rola == "tekst" and self._tekst is not None:
            self._stos[-1].części.append(BIAŁE.sub(" ", "".join(self._tekst)).strip())
            self._tekst = None
        elif rola == "jednostka":
            self._stos.pop()

    def handle_data(self, data: str) -> None:
        if self._tekst is not None and not self._pomijane:
            self._tekst.append(data)


def proza(html: str) -> str:
    """Proza jednej ustawy, jedno zdanie na akapit.

    Akapitem oddziela je to samo, co w pozostałych ekstrakcjach:
    zdanie nie biegnie z jednej gałęzi do następnej,
    a przesłanka, którą dwie gałęzie dzielą, stoi w każdej z nich osobno.
    """
    akt = Akt()
    akt.feed(html)
    ciało = "\n\n".join(zdania(akt.akt))
    return ciało + "\n" if ciało else ""


def jednostki(text: str) -> list[Jednostka]:
    """Cała ustawa, bo ustawa jest napisana w jednym języku."""
    return [Jednostka(1, proza(text).rstrip("\n"))]


# --------------------------------------------------------------------------- #
# Wiersz poleceń
# --------------------------------------------------------------------------- #

UŻYCIE = """
  python3 -m harness.ustawy ustawy/ --into proza/ustawy    drzewo ustaw
  python3 -m harness.ustawy DU-2014-1195.html --into proza/ustawy
"""


CZYTNIK = Czytnik(
    komenda="harness.ustawy",
    sufiks=SUFIKS_HTML,
    nazwa_jednostki="act",
    opis="Extract Polish sentences from a statute published by the ELI API.",
    użycie=UŻYCIE,
    jednostki=jednostki,
)


def main(argv: Sequence[str] | None = None) -> int:
    return uruchom(argv, CZYTNIK)


if __name__ == "__main__":
    raise SystemExit(main())
