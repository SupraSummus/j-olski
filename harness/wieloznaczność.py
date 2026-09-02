"""Ile zdań rejestru czyta się dwojako w samej polszczyźnie.

Kryterium wyjścia toru gramatycznego żąda jednego czytania od zdania, które w
polszczyźnie ma dwa. Rozwidlenie, które z tego wychodzi, wraz z tym, co pomiar
stąd nad nim rozstrzygnął, trzyma docs/open-questions.md; liczbę, na której to
rozstrzygnięcie stanęło, podaje ten moduł.

To jest pomiar rejestru, a nie gramatyki, i tym różni się od harness/pomiar.py,
tak samo jak harness/attachment.py obok. Liczone są pozycje w tekście, a nie
werdykty nad nim, więc zdanie liczy się i wtedy, gdy gramatyka nie umie go
rozebrać wcale. Inaczej się nie da: takich zdań jest w tym rejestrze większość,
a to o nie właśnie pytanie idzie.

Klasy są dwie i obie stoją w tamtym pytaniu wraz ze swoim zdaniem.

Przyłączenie: wyrażenie przyimkowe stoi tuż za grupą imienną, a czasownik przed
nim, więc dochodzi do jednego albo do drugiego. Populacja jest ta sama, którą
harness/attachment.py liczy nad Składnicą, przełożona z cudzych drzew na formy:
tam grupę imienną nazywa węzeł, a tutaj część mowy.

Synkretyzm: dwie grupy imienne czytają się i w mianowniku, i w bierniku, a
czasownik przy nich bierze dopełnienie, więc SVO i OVS stoją oba do wzięcia.
Dwa warunki zdejmują z tej klasy zdanie, które polszczyzna czyta raz:
czasownika bez biernika nie liczy leksykon walencyjny, a grupy,
która z orzeczeniem nie zgadza się co do liczby i rodzaju, nie liczy sama zgoda.

Liczba jest górnym oszacowaniem i myli się w jedną stronę. Grupą imienną jest tu
ciąg form, a nie węzeł, więc przymiotnik orzecznikowy liczy się jak koniec grupy,
a zdanie złożone daje naraz pozycje z dwóch zdań składowych. Pozycja liczy się i
wtedy, gdy obaj jej gospodarze są jedną formą, czyli gdy wyboru w niej nie ma;
odsiewa taką dopiero ``pytania``, bo pyta o nią warstwa, a nie ten pomiar.
Populację zwęża
ponadto to, czego ten moduł nie widzi: wyrażenie, którego czasownik żąda swoim
schematem, stoi w tej pozycji i do wyboru nie stoi, a ile go jest, mierzy nad
Składnicą docs/subset.md. Wchodzi tu wreszcie każde czytanie, które słownik
oferuje, a polszczyzna go nie ma: liczone jest to, co zostawia ``admissible`` w
olski/segmentacja.py, a zostawia ono nazwisko nieodmienne z formy ``Nowy`` i grę z
formy ``go``. Obie te grupy są otwarte i obie mają swoje miejsce — pierwsza jest
etapem 3 z docs/roadmap.md, drugą trzyma todo/ — więc ten pomiar ruszy się,
kiedy się zamkną.

Policzona pozycja jest zarazem pytaniem i ``pytania`` oddaje ją w tej postaci,
w której warstwa rozstrzygająca pyta o gospodarza. Obie sondy nad tym rejestrem
biorą populację stamtąd, a nie każda ze swojego odczytu: gospodarze pozycji są
tym, co warstwa rozstrzyga, więc dwa odczyty rozeszłyby się przy pierwszej zmianie
w tym, co liczy się za grupę imienną.
"""

from __future__ import annotations

import argparse
import collections
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.attachment import CZASOWNIK
from harness.komenda import Komenda, uruchom
from harness.próbka import rozrzucona
from olski.document import SENTENCE_CLOSE
from olski.morph import Reading, Segment
from olski.parse import Przyłączenie

# Kryterium łańcucha, zasięg frazy i strona wyboru należą do warstwy
# rozstrzygającej i bierze się je stamtąd, żeby pozycja stąd była tym samym
# pytaniem, które warstwa dostaje od werdyktu.
from olski.rozstrzyganie import IMIENNE_LUB_NIEZNANE, STRONA_CZASOWNIKOWA, ZASIĘG_FRAZY, strona
from olski.segmentacja import morphology, sentences

# Lematy, którym leksykon odmawia dopełnienia w bierniku, osobno dla formy z
# cząstką ``się`` i bez niej, bo są to dwa czasowniki i biorą co innego. Zdanie z
# takim czasownikiem czytania OVS nie ma: nie ma dopełnienia, którym pierwsza
# grupa miałaby stanąć. Pytamy o nie leksykon, bo to on jest właścicielem tego
# zdania; klasa walencyjna gramatyki jest jego odczytem pod inne pytanie i
# odpowiada tu tylko dopóty, dopóki rama mówi to samo, co jedno zdanie pliku.
from olski.walencja import BEZ_BIERNIKA, BEZ_BIERNIKA_ZWROTNE

#: Części mowy, którymi grupa imienna może się skończyć. Głowa i to, co stoi za
#: nią: przymiotnik idzie w polszczyźnie i przed rzeczownikiem, i po nim.
KONIEC_NP = frozenset({"subst", "depr", "ger", "num", "numcol", "adj", "ppas", "pact"})

#: Sama głowa. Przymiotnik grupą nie jest, więc jako kandydat na podmiot albo
#: dopełnienie nie staje: policzony osobno dawałby dwie grupy tam, gdzie
#: ``nowy program`` jest jedną.
GŁOWA_NP = frozenset({"subst", "depr", "ger", "num", "numcol"})

#: Formy, przy których stoi podmiot i dopełnienie naraz, czyli te, wobec których
#: pytanie o SVO i OVS w ogóle stoi. Imiesłów i bezokolicznik są tu wyłączone,
#: choć CZASOWNIK je liczy: podmiotu przy sobie nie mają.
OSOBOWY = frozenset({"fin", "praet", "bedzie", "impt", "winien"})

#: Znaki, po których ``_człony`` tnie zdanie na składowe.
GRANICA = frozenset({",", ";", ":", "–", "—", "-"})

PRZYŁĄCZENIE = "przyłączenie"
SYNKRETYZM = "synkretyzm"
KLASY = (PRZYŁĄCZENIE, SYNKRETYZM)


@dataclass(frozen=True)
class Miejsce:
    """Jedna pozycja, w której polszczyzna daje dwa czytania."""

    klasa: str
    #: Formy, na których ta pozycja stoi: przyimek dla jednej klasy, a obie grupy
    #: imienne dla drugiej. Bez nich liczba nie ma czym się wytłumaczyć.
    formy: tuple[str, ...]
    #: Gospodarze, między którymi wybiera pozycja przyłączeniowa: formy grupy
    #: imiennej przed wyrażeniem, od najbliższej, a za nimi najbliższa forma
    #: czasownikowa przed przyimkiem. Kolejność jest ta, a nie kolejność zdania,
    #: bo pierwsza z nich stoi tuż przed przyimkiem i po niej :func:`_fraza`
    #: poznaje, o które wystąpienie przyimka chodzi. Ostatnia powtarza czasem
    #: którąś z poprzednich, bo forma bywa naraz imienna i czasownikowa; wybór
    #: zawężony do samej grupy jest wtedy węższy od prawdziwego, a nie zmyślony.
    #: Liczby stąd nie liczy nikt; niesie je :func:`pytania`, bo warstwa
    #: rozstrzygająca pyta o gospodarzy, a nie o sam przyimek. Klasa synkretyzmu
    #: zostawia je puste: tam wyborem nie jest przyłączenie.
    gospodarze: tuple[str, ...] = ()


def miejsca(zdanie: str) -> list[Miejsce]:
    """Pozycje obu klas w jednym zdaniu, tak jak stoją."""
    segments = morphology(zdanie)
    return _przyłączenia(segments) + _synkretyzm(segments)


def _przyłączenia(segments: list[Segment]) -> list[Miejsce]:
    kończy_się = {segment.end: segment for segment in segments if _ma(segment, KONIEC_NP)}
    imienne = {segment.end: segment for segment in segments if _ma(segment, IMIENNE_LUB_NIEZNANE)}
    czasowniki = {segment.start: segment.form for segment in segments if _ma(segment, CZASOWNIK)}
    znalezione = []
    for segment in segments:
        wcześniejsze = [start for start in czasowniki if start < segment.start]
        if not _ma(segment, {"prep"}) or segment.start not in kończy_się or not wcześniejsze:
            continue
        grupa = _grupa(kończy_się[segment.start], imienne)
        gospodarze = (*grupa, czasowniki[max(wcześniejsze)])
        znalezione.append(Miejsce(PRZYŁĄCZENIE, (segment.form,), gospodarze))
    return znalezione


def _grupa(sąsiad: Segment, imienne: dict[int, Segment]) -> tuple[str, ...]:
    """Formy grupy imiennej kończącej się tym segmentem, od prawej do lewej.

    Tą samą drogą schodzi ``_łańcuch`` w ``olski/rozstrzyganie.py`` i tam stoi
    wywód: co przedłuża łańcuch imienny, po co sąsiad wchodzi bez warunku i czym
    grozi łańcuch wzięty za daleko. Świadek kontekstowy szuka nim gospodarza w
    zdaniu wcześniejszym, a tu szuka się go w zdaniu spornym, więc kryterium jest
    jedno (:data:`~olski.rozstrzyganie.IMIENNE_LUB_NIEZNANE`).

    Cena wychodzi jednak inna niż tam. ``stanowi`` jest u Morfeusza i formą
    osobową, i celownikiem od ``stan``, więc w ``dokument stanowi kompendium
    wiedzy dla deweloperów`` łańcuch przechodzi przez orzeczenie: świadek płaci za
    to milczeniem, a pozycja stąd traci gospodarza czasownikowego, bo orzeczenie
    stoi wtedy po obu stronach wyboru. Wpis o zawężeniu kryterium trzyma todo/.
    """
    grupa = [sąsiad]
    while _ma(grupa[-1], IMIENNE_LUB_NIEZNANE) and grupa[-1].start in imienne:
        grupa.append(imienne[grupa[-1].start])
    return tuple(człon.form for człon in grupa)


def _synkretyzm(segments: list[Segment]) -> list[Miejsce]:
    """Czy zdanie stawia dwie grupy, z których każda staje podmiotem i dopełnieniem.

    Dwa warunki poza samym przypadkiem, i żaden nie jest ozdobą. Zgoda:
    ``Program zapisuje ustawienia`` ma obie grupy obojętne na przypadek i jedno
    czytanie mimo to, bo orzeczenie stoi w liczbie pojedynczej, a druga grupa
    jest mnoga i podmiotem być nie może. Jeden człon: obie grupy mają stanąć przy
    tym samym orzeczeniu, bo ``Typ obiektu – liść drzewa, czyli kategoria, która
    nie posiada podkategorii`` ma je w dwóch zdaniach składowych i o wyborze
    między SVO a OVS nie mówi nic.
    """
    zwrotne = any(reading.lemma == "się" for segment in segments for reading in segment.readings)
    for człon in _człony(segments):
        for orzeczenie in (r for segment in człon for r in segment.readings):
            if orzeczenie.tag.pos not in OSOBOWY:
                continue
            odmawia = BEZ_BIERNIKA_ZWROTNE if zwrotne else BEZ_BIERNIKA
            if orzeczenie.lemma in odmawia:
                continue
            grupy = [segment.form for segment in człon if _obojętny(segment, orzeczenie)]
            if len(grupy) >= 2:
                return [Miejsce(SYNKRETYZM, tuple(grupy))]
    return []


def _człony(segments: list[Segment]) -> list[list[Segment]]:
    """Zdanie pocięte tam, gdzie znak je punktuje.

    Cięcie idzie po interpunkcji i po niczym więcej, bo spójnik podrzędny da się
    od współrzędnego odróżnić dopiero rozbiorem, a tego ten pomiar nie ma. Myli
    się przez to w stronę mniejszej liczby: dywiz wewnątrz formy tnie tak samo
    jak myślnik między zdaniami, a człon urwany za wcześnie traci parę, której
    nie miał gdzie zestawić.
    """
    granice = sorted(segment.start for segment in segments if segment.form in GRANICA)
    człony: dict[int, list[Segment]] = {}
    for segment in segments:
        if segment.form in GRANICA:
            continue
        numer = sum(1 for granica in granice if granica < segment.start)
        człony.setdefault(numer, []).append(segment)
    return list(człony.values())


def _obojętny(segment: Segment, orzeczenie: Reading) -> bool:
    """Czy ta forma staje przy tym orzeczeniu i podmiotem, i dopełnieniem.

    **Pytanie idzie o segment, a nie o czytanie**, bo słownik rozdziela te dwa
    przypadki na wpisy tam, gdzie forma ich nie rozdziela: ``mysz`` wychodzi z
    Morfeusza jako ``subst:sg:nom:f`` i ``subst:sg:acc:f`` osobno, a ``ogon``
    jako jedno ``subst:sg:nom.acc:m3``. Warunek pytany o czytanie mijał więc
    ``Mysz goni ogon.``, czyli mylił się w stronę mniejszą tam, gdzie ten pomiar
    nazywa swoją liczbę górnym oszacowaniem. Zgłosił to skład, który tę samą
    klasę liczy porównaniem napisów (``docs/sklad.md``).

    Dwa węższe warianty tego warunku są zmierzone i po jednym zdaniu każdy;
    ceny i wnioski trzyma ``docs/open-questions.md``.

    Nieodmienne czytanie spełnia oba warunki naraz: notacja rejestru stoi w
    każdym przypadku, więc stoi i w tych dwóch.
    """
    głowy = [reading for reading in segment.readings if reading.tag.pos in GŁOWA_NP]
    podmiotem = any(
        "nom" in reading.tag.get("case") and _zgodny(reading, orzeczenie) for reading in głowy
    )
    dopełnieniem = any("acc" in reading.tag.get("case") for reading in głowy)
    return podmiotem and dopełnieniem


def _zgodny(reading: Reading, orzeczenie: Reading) -> bool:
    """Czy ta głowa zgadza się z orzeczeniem tak, jak zgadza się z nim podmiot.

    Żąda się tego od czytania mianownikowego i od niego jednego: podmiot
    wyciąga z orzeczenia formę, a dopełnienie nie, więc liczba i rodzaj
    dopełnienia nie mają z czym się nie zgodzić. Rodzaj wchodzi do zgody tylko
    wtedy, gdy orzeczenie go niesie, bo forma osobowa czasu teraźniejszego nie
    niesie go wcale.
    """
    if not reading.tag.get("number") & orzeczenie.tag.get("number"):
        return False
    rodzaj = orzeczenie.tag.get("gender")
    return not rodzaj or bool(reading.tag.get("gender") & rodzaj)


def _ma(segment: Segment, części: Iterable[str]) -> bool:
    return any(reading.tag.pos in części for reading in segment.readings)


def pytania(zdanie: str) -> list[Przyłączenie]:
    """Pozycje przyłączeniowe tego zdania jako pytania do warstwy rozstrzygającej.

    **Populacja warstwy nad żywym tekstem jest morfologiczna, a nie z werdyktów,
    i to jest powód, po który sięgają tu obie sondy.** Gramatyka odrzuca w
    rejestrze dokumentacji prawie każde zdanie, więc werdykty stawiają nad
    korpusem audytowym 38 wyborów na 2 915 zdań (``docs/rozstrzyganie.md``), a
    liczba zmierzona na nich mówi o gramatyce, nie o warstwie. Pozycja znaleziona
    morfologią stoi tam, gdzie polszczyzna daje dwa czytania, niezależnie od tego,
    czy olski to zdanie rozbiera.

    Typ jest ten sam, którym pyta werdykt (``Przyłączenie`` w ``olski/parse/podsumowanie.py``),
    więc pytanie stąd i pytanie z rozbioru są jednym kształtem. Tyle samo nie
    znaczą: fraza jest tu propozycją, bo gdzie wyrażenie przyimkowe się kończy,
    mówi dopiero rozbiór, którego nad tym rejestrem w większości nie ma.

    Pozycja o jednym gospodarzu wyboru nie stawia i wypada: imiesłów kończy grupę
    imienną i jest zarazem formą czasownikową, więc w ``obiekt jest przetwarzany w
    Systemie RIT`` obie strony są jednym słowem. Grupy dłuższej warunek ten nie
    tyka, choćby orzeczenie powtarzało którąś z jej form, bo łańcuch pokazuje
    wtedy gospodarza, którego sąsiad sam nie pokazał.
    """
    zebrane = []
    for miejsce in miejsca(zdanie):
        if miejsce.klasa != PRZYŁĄCZENIE or len(set(miejsce.gospodarze)) < 2:
            continue
        fraza = _fraza(zdanie, miejsce.formy[0], miejsce.gospodarze[0])
        zebrane.append(Przyłączenie(modyfikator=fraza, gospodarze=miejsce.gospodarze))
    return zebrane


def _fraza(zdanie: str, przyimek: str, sąsiad: str) -> str:
    """Przyimek wraz z formami stojącymi za nim, do :data:`ZASIĘG_FRAZY`.

    Zasięg jest ten, którym świadek kontekstowy szuka rzeczownika frazy, bo
    propozycja ma trafiać w to, o co on i tak zapyta.

    Wystąpienie wybiera gospodarz stojący przed przyimkiem, a nie kolejność:
    zdanie z dwoma takimi samymi przyimkami ma dwie pozycje, a propozycja opisana
    z pierwszej z nich mówiłaby o innej niż ta, do której dobrano gospodarzy.
    Kończy się na formie czasownikowej i na słowie, za którym stoi znak: fraza
    przez żadne z nich nie przechodzi, a propozycja sięgająca dalej kosztuje
    czytającego skreślenie zamiast przeczytania. Dalej jej nie zwężamy, bo
    granicę frazy zna dopiero rozbiór, a lista słów pisana tutaj byłaby
    zgadywaniem, które czytający i tak poprawia.
    """
    słowa = zdanie.split()
    for i, słowo in enumerate(słowa):
        if _goły(słowo).lower() != przyimek.lower():
            continue
        #  Przyimek stojący pierwszy w zdaniu nie ma przed sobą grupy imiennej,
        #  więc nie jest tą pozycją, choćby jego forma się zgadzała.
        if i == 0 or _goły(słowa[i - 1]) != sąsiad:
            continue
        fraza = [_goły(słowo)]
        for dalsze in słowa[i + 1 : i + 1 + ZASIĘG_FRAZY]:
            if strona(_goły(dalsze)) == STRONA_CZASOWNIKOWA:
                break
            fraza.append(_goły(dalsze))
            if _goły(dalsze) != dalsze:
                break
        return " ".join(fraza)
    return przyimek


def _goły(słowo: str) -> str:
    return słowo.strip(",.;:()„”\"'")


@dataclass
class Raport:
    """Ile zdań niesie którą klasę, i ile pozycji przypada na zdanie."""

    zdania: int = 0
    #: Nagłówek, pozycja listy i wiersz tabeli. Kryterium wyjścia ich nie liczy,
    #: więc nie liczy ich i ten pomiar, ale mówi, ile ich minął.
    fragmenty: int = 0
    zdania_z: collections.Counter = field(default_factory=collections.Counter)
    którakolwiek: int = 0
    #: Rozkład liczby przyłączeń w zdaniu: jedno zdanie bywa wieloznaczne kilka
    #: razy naraz, a wtedy czytań ma nie dwa, tylko dwa do potęgi.
    przyłączeń: collections.Counter = field(default_factory=collections.Counter)
    #: Zdania trafione, każde wraz z formami, na których stanęło.
    przykłady: dict[str, list[tuple[str, tuple[str, ...]]]] = field(default_factory=dict)

    def record(self, zdanie: str, found: Sequence[Miejsce]) -> None:
        if not SENTENCE_CLOSE.search(zdanie):
            self.fragmenty += 1
            return
        self.zdania += 1
        klasy = {miejsce.klasa for miejsce in found}
        for klasa in klasy:
            self.zdania_z[klasa] += 1
            formy = tuple(f for m in found if m.klasa == klasa for f in m.formy)
            self.przykłady.setdefault(klasa, []).append((zdanie, formy))
        self.którakolwiek += bool(klasy)
        self.przyłączeń[sum(miejsce.klasa == PRZYŁĄCZENIE for miejsce in found)] += 1


def measure(texts: Iterable[str]) -> Raport:
    report = Raport()
    for text in texts:
        for zdanie in sentences(text):
            report.record(zdanie, miejsca(zdanie))
    return report


def render(report: Raport, przykłady: int = 0) -> str:
    lines = [f"{report.zdania} zdań, obok {report.fragmenty} fragmentów, których nic nie punktuje"]
    if not report.zdania:
        return lines[0]
    lines += ["", "zdań z pozycją, w której polszczyzna daje dwa czytania:"]
    for klasa in KLASY:
        liczba = report.zdania_z[klasa]
        lines.append(f"  {liczba:6} {liczba / report.zdania:6.1%}  {klasa}")
    razem = report.którakolwiek
    lines.append(f"  {razem:6} {razem / report.zdania:6.1%}  którakolwiek")
    lines += ["", "przyłączeń nierozstrzygniętych w zdaniu:"]
    for ile, liczba in sorted(report.przyłączeń.items()):
        lines.append(f"  {ile:6} {liczba:6}")
    for klasa in KLASY:
        for zdanie, formy in rozrzucona(report.przykłady.get(klasa, ()), przykłady):
            lines.append(f"\n{klasa} [{', '.join(formy)}]: {zdanie}")
    return "\n".join(lines)


def _proza(wejścia: Sequence[tuple[Path, str]], args: argparse.Namespace) -> str:
    return render(measure(tekst for _, tekst in wejścia), args.przykłady)


KOMENDA = Komenda(
    nazwa="harness.wieloznaczność",
    opis="Policz zdania, które czytają się dwojako w samej polszczyźnie.",
    przykłady=0,
    proza=_proza,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
