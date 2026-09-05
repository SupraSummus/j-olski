"""Złote znaczniki NKJP zawężają morfologię, zanim gramatyka ją zobaczy.

Podkorpus milionowy niesie obok tekstu warstwę ``ann_morphosyntax.xml``, w której
anotator wybrał każdej formie jedno odczytanie: ``nagrody`` w ``Czekają nagrody.``
stoi tam w mianowniku, a nie w bierniku. Wieloznaczność, którą olski melduje nad
tym zdaniem, jest różnicą przypadka tej jednej formy, więc anotator ją rozstrzygnął,
zanim ktokolwiek zapytał. Ta sonda pyta, nad iloma zdaniami korpusu tak jest.

Robi to tak samo jak pomiar nad Składnicą (``harness/pomiar.py``): rozbiera zdanie
raz z Morfeuszem i raz z odczytaniami zawężonymi do zgodnych ze złotym znacznikiem,
a różnica liczby czytań jest tym, co rozstrzyga anotator. Z czytania, które zostaje,
gramatyka nie widzi nic nowego; widzi mniej form, którymi wolno je zbudować.

Klas jest sześć i dzielą się po tym, ile czytań zdanie ma bez złota i ze złotem.
Nad zdaniem o jednym czytaniu złoto może mu tylko zaprzeczyć
(:data:`ZGODNE`, :data:`SPRZECZNE`), a nad wieloznacznym — rozstrzygnąć je,
zostawić wieloznaczne albo przepaść, bo żadne czytanie olskiego nie stoi na formach,
które wybrał anotator (:data:`ROZSTRZYGNIĘTE`, :data:`POZOSTAJE`, :data:`PRZEPADŁO`).
Ostatnia klasa jest wspólna z pomiarem nad Składnicą i tak samo nie mówi, kto się myli.

Złoto rozstrzyga tylko to, co jest odczytaniem formy: przypadek, liczbę, część mowy.
Przyłączenia wyrażenia przyimkowego żadna warstwa tego korpusu nie zapisuje, więc
zdanie z klasy :data:`POZOSTAJE` jest tym, nad którym sąd trzeba przeczytać ręką;
co z tego wynika dla bazy sądów, mówi docs/adnotacje.md.

    python3 -m harness.znaczniki nkjp/ --proza proza/nkjp
    python3 -m harness.znaczniki nkjp/ --sądy
"""

from __future__ import annotations

import argparse
import collections
import concurrent.futures
import hashlib
import os
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from xml.etree import ElementTree

from harness import pliki_prozy
from harness.nkjp import TEI, TEKST, XML_ID
from harness.sądy import SĄDY, Sąd, czytaj
from olski.morph import VALUES, Segment, Tag, tag
from olski.segmentacja import morphology, sentences
from olski.werdykt import WIELOZNACZNE, werdykt

#: Warstwy podkorpusu, które ta sonda czyta obok tekstu: gdzie każdy segment stoi
#: i które odczytanie wybrał mu anotator.
SEGMENTACJA = "ann_segmentation.xml"
MORFOLOGIA = "ann_morphosyntax.xml"

#: ``corresp`` segmentu: akapit, pierwszy znak i długość w tekście tego akapitu.
ZAKRES = re.compile(r"string-range\(([^,]+),(\d+),(\d+)\)")

#: Części mowy, które tagset NKJP nazywa inaczej niż Morfeusz, w kierunku Morfeusza.
#: Wartości cech obu tagsetów są te same, więc innego przekładu nie ma.
CZĘŚCI_MOWY = {"qub": "part", "numcol": "num", "xxx": "ign"}

#: Klasy zdania, po tym, ile czytań ma bez złota i ze złotem.
NIECZYTANE = "nieczytane"
ZGODNE = "zgodne"
SPRZECZNE = "sprzeczne"
ROZSTRZYGNIĘTE = "rozstrzygnięte"
POZOSTAJE = "pozostaje"
PRZEPADŁO = "przepadło"

#: Klasy w kolejności wydruku. Krotka, a nie zbiór, bo zbiór postawiony na drodze
#: do wydruku wypisuje w każdym przebiegu co innego.
KLASY = (NIECZYTANE, ZGODNE, SPRZECZNE, ROZSTRZYGNIĘTE, POZOSTAJE, PRZEPADŁO)

#: Klasy zdania, które olski czyta kilkoma czytaniami, czyli te, o które ta sonda pyta.
WIELOZNACZNE_KLASY = (ROZSTRZYGNIĘTE, POZOSTAJE, PRZEPADŁO)


@dataclass(frozen=True)
class Złoty:
    """Jeden segment próbki wraz z odczytaniem, które wybrał mu anotator."""

    #: ``xml:id`` akapitu i miejsce w jego tekście.
    akapit: str
    start: int
    długość: int
    forma: str
    znacznik: Tag


@dataclass(frozen=True)
class Przyłożenie:
    """Ile form zdania złoto zawęziło, a ile z jakiego powodu nie.

    Forma niezawężona zostaje ze wszystkimi odczytaniami, więc zdanie z takimi
    formami jest ze złotem mniej rozstrzygnięte, niż mogłoby być, a nie bardziej.
    """

    #: Formy, którymi Morfeusz czyta zdanie.
    form: int = 0
    #: Formy, którym złoto zabrało choć jedno odczytanie.
    zawężone: int = 0
    #: Formy, pod którymi nie stoi dokładnie jeden złoty segment: Morfeusz i
    #: anotator dzielą tam napis inaczej.
    nieprzyłożone: int = 0
    #: Formy, których żadne odczytanie Morfeusza nie zgadza się ze złotym:
    #: słownik go nie ma albo zdjęło je wykluczenie leksykalne olskiego.
    bez_odczytania: int = 0

    def __add__(self, inne: Przyłożenie) -> Przyłożenie:
        return Przyłożenie(
            self.form + inne.form,
            self.zawężone + inne.zawężone,
            self.nieprzyłożone + inne.nieprzyłożone,
            self.bez_odczytania + inne.bez_odczytania,
        )


@dataclass(frozen=True)
class Wynik:
    """Co złoto zrobiło z jednym zdaniem: liczba czytań przed i po zawężeniu."""

    plik: str
    zdanie: str
    ile: int
    #: Czytania po zawężeniu; ``None``, gdy olski zdania nie czyta i nikt nie pytał.
    ile_ze_złotem: int | None
    przyłożenie: Przyłożenie

    @property
    def klasa(self) -> str:
        if self.ile == 0:
            return NIECZYTANE
        assert self.ile_ze_złotem is not None
        if self.ile == 1:
            return ZGODNE if self.ile_ze_złotem == 1 else SPRZECZNE
        if self.ile_ze_złotem == 0:
            return PRZEPADŁO
        return ROZSTRZYGNIĘTE if self.ile_ze_złotem == 1 else POZOSTAJE

    @property
    def warstwa(self) -> str:
        return self.plik.split("/", 1)[0]

    @property
    def odcisk(self) -> str:
        return hashlib.sha256(self.zdanie.encode()).hexdigest()


# --------------------------------------------------------------------------- #
# Warstwy próbki
# --------------------------------------------------------------------------- #


def akapity(próbka: Path) -> dict[str, list[tuple[str, str]]]:
    """Sekcja → jej akapity, każdy ze swoim ``xml:id`` i tekstem, w kolejności.

    Tekst nie jest tu obcięty z białych znaków, bo miejsca złotych segmentów liczą
    się od jego pierwszego znaku; obcina go dopiero ekstrakcja (``harness/nkjp.py``),
    a zdanie i tak szuka się w akapicie po napisie.
    """
    drzewo = ElementTree.fromstring((próbka / TEKST).read_text(encoding="utf-8"))
    return {
        div.get(XML_ID) or f"div{numer}": [
            (ab.get(XML_ID) or "", "".join(ab.itertext())) for ab in div.findall(f"{TEI}ab")
        ]
        for numer, div in enumerate(drzewo.iter(f"{TEI}div"), start=1)
    }


def złote(próbka: Path) -> dict[str, list[Złoty]]:
    """Akapit → jego złote segmenty w kolejności, czyli to, co wybrał anotator.

    Segmenty bierze warstwa morfologiczna, bo tylko te, które anotator zostawił,
    mają tam odczytanie: podział odrzucony stoi w segmentacji, a tu go nie ma.
    Miejsce segmentu stoi za to tylko w segmentacji, więc czyta się obie.
    """
    miejsca = _miejsca(próbka)
    zebrane: dict[str, list[Złoty]] = {}
    drzewo = ElementTree.fromstring((próbka / MORFOLOGIA).read_text(encoding="utf-8"))
    for seg in drzewo.iter(f"{TEI}seg"):
        odczytanie = _wybrane(seg)
        if odczytanie is None:
            continue
        akapit, start, długość = miejsca[seg.get("corresp", "").split("#")[-1]]
        forma, znacznik = odczytanie
        zebrane.setdefault(akapit, []).append(Złoty(akapit, start, długość, forma, znacznik))
    return zebrane


def _miejsca(próbka: Path) -> dict[str, tuple[str, int, int]]:
    """``xml:id`` segmentu → akapit, pierwszy znak i długość."""
    drzewo = ElementTree.fromstring((próbka / SEGMENTACJA).read_text(encoding="utf-8"))
    miejsca = {}
    for seg in drzewo.iter(f"{TEI}seg"):
        zakres = ZAKRES.search(seg.get("corresp", ""))
        if zakres is not None:
            miejsca[seg.get(XML_ID)] = (zakres.group(1), int(zakres.group(2)), int(zakres.group(3)))
    return miejsca


def _wybrane(seg: ElementTree.Element) -> tuple[str, Tag] | None:
    """Forma i znacznik, które anotator wybrał temu segmentowi.

    Wybór jest wskazaniem na ``msd`` jednego z leksemów, a nie napisem, bo napis
    ``interpretation`` skleja lemat i znacznik dwukropkiem, a lemat bywa adresem
    z dwukropkiem w środku.
    """
    forma = seg.findtext(f'{TEI}fs/{TEI}f[@name="orth"]/{TEI}string')
    wybór = seg.find(f'{TEI}fs/{TEI}f[@name="disamb"]/{TEI}fs/{TEI}f[@name="choice"]')
    if forma is None or wybór is None:
        return None
    szukany = wybór.get("fVal", "").lstrip("#")
    for leksem in seg.iterfind(f'{TEI}fs/{TEI}f[@name="interps"]/{TEI}fs'):
        symbol = leksem.find(f'{TEI}f[@name="ctag"]/{TEI}symbol')
        część = symbol.get("value", "") if symbol is not None else ""
        for msd in leksem.iterfind(f'{TEI}f[@name="msd"]//{TEI}symbol'):
            if msd.get(XML_ID) == szukany:
                surowy = ":".join(kawałek for kawałek in (część, msd.get("value", "")) if kawałek)
                return forma, tag(surowy)
    return None


def próbka_i_sekcja(plik: str) -> tuple[Path, str]:
    """Z drogi pliku prozy do katalogu próbki względem archiwum i do ``xml:id`` sekcji.

    Ekstrakcja pisze ``warstwa/próbka/sekcja.txt`` (``harness/nkjp.py``), a próbka
    bywa katalogiem zagnieżdżonym, więc jest nią wszystko między warstwą a plikiem.
    """
    części = Path(plik).parts
    return Path(*części[1:-1]), Path(części[-1]).stem


# --------------------------------------------------------------------------- #
# Przyłożenie złota do zdania
# --------------------------------------------------------------------------- #


def umieść(zdania: Sequence[str], akapity: Sequence[tuple[str, str]]) -> list[tuple[str, int] | None]:
    """Gdzie każde zdanie stoi: akapit i pierwszy znak, albo ``None``, gdy go tam nie ma.

    Zdania idą w kolejności prozy, a proza jest akapitami tej sekcji po kolei, więc
    szuka się od miejsca, na którym stanęło poprzednie, i przechodzi do następnego
    akapitu, gdy w tym zdania już nie ma. Zdanie, którego nie ma w żadnym, dostaje
    ``None``, a nie błąd, bo przebieg nad korpusem ma je policzyć, a nie stanąć.
    """
    miejsca: list[tuple[str, int] | None] = []
    numer, kursor = 0, 0
    for zdanie in zdania:
        znalezione = None
        while numer < len(akapity):
            nazwa, tekst = akapity[numer]
            gdzie = tekst.find(zdanie, kursor)
            if gdzie >= 0:
                znalezione = (nazwa, gdzie)
                kursor = gdzie + len(zdanie)
                break
            numer, kursor = numer + 1, 0
        miejsca.append(znalezione)
    return miejsca


def zgodne(żywy: Tag, złoty: Tag) -> bool:
    """Czy odczytanie Morfeusza mieści złote: ta sama część mowy, a każda wspólna cecha ma wspólną wartość.

    Cecha, którą ma jedna strona, a druga nie, nie rozstrzyga: Morfeusz mówi o
    rzeczowniku nijakim, czy jest zbiorowy, a tagset NKJP tego nie mówi.
    """
    if CZĘŚCI_MOWY.get(złoty.pos, złoty.pos) != żywy.pos:
        return False
    return all(
        żywy.cechy[cecha] & wartości
        for cecha, wartości in złoty.cechy.items()
        if cecha in żywy.cechy
    )


def zawęź(żywy: Tag, złoty: Tag) -> Tag:
    """Odczytanie Morfeusza z każdą wspólną cechą zawężoną do wartości złotej.

    Samo odsianie odczytań nie starcza, bo Morfeusz pisze przypadek alternatywą:
    ``nagrody`` ma jedno odczytanie ``subst:pl:nom.acc.voc:f``, a złote mówi ``nom``,
    więc odczytanie zostaje i przypadek w nim trzeba zwęzić, inaczej gramatyka dalej
    stawia tę formę w obu rolach. Napis znacznika przepisuje się w tej samej
    kolejności, bo czyta go wydruk ``--morfologia``.
    """
    cechy = {
        cecha: (wartości & złoty.cechy[cecha]) if cecha in złoty.cechy else wartości
        for cecha, wartości in żywy.cechy.items()
    }
    kawałki = []
    for kawałek in żywy.raw.split(":")[1:]:
        kategoria = VALUES.get(kawałek.split(".")[0])
        kawałki.append(".".join(sorted(cechy[kategoria])) if kategoria in cechy else kawałek)
    return Tag(
        żywy.pos,
        frozenset((cecha, frozenset(wartości)) for cecha, wartości in cechy.items()),
        ":".join((żywy.pos, *kawałki)),
    )


def przyłóż(
    segmenty: Sequence[Segment], zdanie: str, złote: Sequence[Złoty], początek: int
) -> tuple[list[Segment], Przyłożenie]:
    """Segmenty zdania z odczytaniami zawężonymi do złotego, i ile form to zawęziło.

    Forma Morfeusza dostaje złoty segment, który zajmuje w akapicie dokładnie te
    same znaki; przy innym podziale napisu zostaje ze wszystkimi odczytaniami.
    Forma, której żadne odczytanie nie mieści złotego, też zostaje ze wszystkimi:
    zdjęcie ich wszystkich zabrałoby zdaniu każde czytanie z powodu,
    który nie jest wieloznacznością.
    """
    po_miejscu = {(z.start - początek, z.start - początek + z.długość): z for z in złote}
    miejsca = _miejsca_form(segmenty, zdanie)
    przyłożenie = Przyłożenie(form=len(segmenty))
    zawężone = []
    for segment in segmenty:
        złoty = po_miejscu.get(miejsca.get(segment))
        if złoty is None:
            przyłożenie += Przyłożenie(nieprzyłożone=1)
            zawężone.append(segment)
            continue
        odczytania = tuple(
            replace(r, tag=zawęź(r.tag, złoty.znacznik))
            for r in segment.readings
            if zgodne(r.tag, złoty.znacznik)
        )
        if not odczytania:
            przyłożenie += Przyłożenie(bez_odczytania=1)
            zawężone.append(segment)
            continue
        if odczytania != segment.readings:
            przyłożenie += Przyłożenie(zawężone=1)
        zawężone.append(replace(segment, readings=odczytania))
    return zawężone, przyłożenie


def _miejsca_form(segmenty: Sequence[Segment], zdanie: str) -> dict[Segment, tuple[int, int]]:
    """Segment → jego znaki w zdaniu.

    Segmenty są krawędziami grafu, a nie listą, więc miejsce liczy się po węzłach:
    węzeł końcowy krawędzi stoi tam, gdzie kończy się jej forma, a dwie krawędzie
    z jednego węzła zaczynają się w tym samym znaku. Forma, której nie ma w zdaniu
    od swojego węzła, miejsca nie dostaje i zostaje nieprzyłożona.
    """
    węzły = {min(s.start for s in segmenty): 0} if segmenty else {}
    miejsca = {}
    for segment in sorted(segmenty, key=lambda s: (s.start, s.end)):
        skąd = węzły.get(segment.start)
        if skąd is None:
            continue
        gdzie = zdanie.find(segment.form, skąd)
        if gdzie < 0 or zdanie[skąd:gdzie].strip():
            continue
        miejsca[segment] = (gdzie, gdzie + len(segment.form))
        węzły.setdefault(segment.end, gdzie + len(segment.form))
    return miejsca


def zmierz(plik: str, zdanie: str, złote_akapitu: Sequence[Złoty], początek: int) -> Wynik:
    """Rozbierz zdanie bez złota i ze złotem.

    Ze złotem tylko wtedy, gdy bez złota ma czytanie: zawężenie odczytań czytania
    nie dodaje, więc nad zdaniem odrzuconym drugi rozbiór nie powie nic nowego.
    Zatrzymania żaden z rozbiorów nie liczy, bo pyta się o liczbę czytań.
    """
    segmenty = morphology(zdanie)
    ile = werdykt(zdanie, segmenty, zatrzymanie=False).result.ile
    zawężone, przyłożenie = przyłóż(segmenty, zdanie, złote_akapitu, początek)
    ile_ze_złotem = None
    if ile:
        ile_ze_złotem = werdykt(zdanie, zawężone, zatrzymanie=False).result.ile
    return Wynik(plik, zdanie, ile, ile_ze_złotem, przyłożenie)


def nad_sekcją(archiwum: Path, plik: str, proza: str) -> tuple[list[Wynik], int]:
    """Wyniki nad zdaniami jednego pliku prozy, i ile zdań nie stało w żadnym akapicie."""
    próbka, sekcja = próbka_i_sekcja(plik)
    złote_próbki = złote(archiwum / próbka)
    akapity_sekcji = akapity(archiwum / próbka)[sekcja]
    zdania = sentences(proza)
    wyniki, nieumieszczone = [], 0
    for zdanie, miejsce in zip(zdania, umieść(zdania, akapity_sekcji), strict=True):
        if miejsce is None:
            nieumieszczone += 1
            continue
        akapit, początek = miejsce
        wyniki.append(zmierz(plik, zdanie, złote_próbki.get(akapit, ()), początek))
    return wyniki, nieumieszczone


# --------------------------------------------------------------------------- #
# Przebieg nad korpusem
# --------------------------------------------------------------------------- #


def _nad_plikiem(zadanie: tuple[Path, Path, Path]) -> tuple[list[Wynik], int]:
    archiwum, korzeń, ścieżka = zadanie
    plik = ścieżka.relative_to(korzeń).as_posix()
    return nad_sekcją(archiwum, plik, ścieżka.read_text(encoding="utf-8"))


def nad_korpusem(archiwum: Path, korzeń: Path, jobs: int = 1) -> tuple[list[Wynik], int]:
    """Wyniki nad całą prozą pod tym katalogiem, w porządku plików."""
    zadania = [(archiwum, korzeń, ścieżka) for ścieżka in pliki_prozy(korzeń)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as pula:
        części = list(pula.map(_nad_plikiem, zadania, chunksize=8))
    return [w for wyniki, _ in części for w in wyniki], sum(n for _, n in części)


def wydruk(wyniki: Sequence[Wynik], nieumieszczone: int, przykłady: int) -> str:
    """Klasy nad całością, klasy wieloznaczne po warstwach, przyłożenie, a pod tym przykłady.

    Udział klasy liczy się od zdań, o których ona mówi: zgodne i sprzeczne od zdań
    o jednym czytaniu, trzy klasy wieloznaczne od wieloznacznych, bo o zdaniu
    nieczytanym złoto nie mówi nic, a zdanie o jednym czytaniu nie ma czego rozstrzygać.
    Przykłady idą w porządku odcisku zdania, żeby były próbą z całego korpusu,
    a nie z jego pierwszego pliku (``harness/sądy.py`` mówi, czemu tak).
    """
    ile = collections.Counter(w.klasa for w in wyniki)
    jednoznaczne = ile[ZGODNE] + ile[SPRZECZNE]
    wieloznaczne = sum(ile[klasa] for klasa in WIELOZNACZNE_KLASY)
    wiersze = [
        f"{len(wyniki)} zdań, z tego {jednoznaczne} olski czyta jednym czytaniem, "
        f"a {wieloznaczne} kilkoma"
    ]
    if nieumieszczone:
        wiersze[0] += f"; {nieumieszczone} zdań nie stało w żadnym akapicie i nie wchodzi do liczb"
    for klasa in KLASY:
        mianownik = wieloznaczne if klasa in WIELOZNACZNE_KLASY else jednoznaczne
        udział = f"{ile[klasa] / mianownik:>6.1%}" if mianownik and klasa != NIECZYTANE else "      "
        wiersze.append(f"  {ile[klasa]:>6}  {udział}  {klasa}")

    wiersze += ["", "  zdania wieloznaczne po warstwach: rozstrzygnięte / pozostaje / przepadło"]
    po_warstwie = collections.defaultdict(collections.Counter)
    for w in wyniki:
        if w.klasa in WIELOZNACZNE_KLASY:
            po_warstwie[w.warstwa][w.klasa] += 1
    for warstwa in sorted(po_warstwie):
        licznik = po_warstwie[warstwa]
        razem = sum(licznik.values())
        wiersze.append(
            f"  {licznik[ROZSTRZYGNIĘTE]:>5} / {licznik[POZOSTAJE]:<5} / {licznik[PRZEPADŁO]:<5}"
            f"  {licznik[ROZSTRZYGNIĘTE] / razem:>6.1%} rozstrzygniętych  {warstwa}"
        )

    razem = sum((w.przyłożenie for w in wyniki if w.ile), Przyłożenie())
    wiersze += [
        "",
        f"  {razem.form} form w zdaniach czytanych: {razem.zawężone} zawężonych, "
        f"{razem.nieprzyłożone} podzielonych inaczej niż u anotatora, "
        f"{razem.bez_odczytania} bez odczytania zgodnego ze złotym",
    ]

    for klasa in (SPRZECZNE, *WIELOZNACZNE_KLASY):
        swoje = sorted((w for w in wyniki if w.klasa == klasa), key=lambda w: w.odcisk)[:przykłady]
        if swoje:
            wiersze += ["", f"  {klasa}:"]
            wiersze += [f"  {w.ile:>4} → {w.ile_ze_złotem:<4} {w.zdanie}" for w in swoje]
    return "\n".join(wiersze)


# --------------------------------------------------------------------------- #
# Baza sądów
# --------------------------------------------------------------------------- #


def nad_sądami(archiwum: Path, sądy: Iterable[Sąd]) -> list[tuple[Sąd, Wynik | None]]:
    """Każdy sąd o wieloznaczności wraz z tym, co złoto mówi o jego zdaniu.

    ``None`` przy sądzie, którego zdania nie ma w nazwanej sekcji: wpis bez ``plik``
    nie ma czym wskazać próbki, a zdanie przeredagowane nie stoi w żadnym akapicie.
    """
    zestawienia = []
    for sąd in sądy:
        if sąd.znalezisko != WIELOZNACZNE or not sąd.plik:
            continue
        próbka, sekcja = próbka_i_sekcja(sąd.plik)
        akapity_sekcji = akapity(archiwum / próbka).get(sekcja, [])
        (miejsce,) = umieść([sąd.zdanie], akapity_sekcji)
        if miejsce is None:
            zestawienia.append((sąd, None))
            continue
        akapit, początek = miejsce
        złote_akapitu = złote(archiwum / próbka).get(akapit, ())
        zestawienia.append((sąd, zmierz(sąd.plik, sąd.zdanie, złote_akapitu, początek)))
    return zestawienia


def wydruk_sądów(zestawienia: Sequence[tuple[Sąd, Wynik | None]]) -> str:
    """Sąd czytelnika obok klasy złota, wpis po wpisie, a nad tym ich zestawienie.

    Dwie odpowiedzi mówią o czym innym i nie mają się zgadzać: sąd mówi, czy
    czytelnik by coś poprawił, a złoto — czy anotator musiał wybrać przypadek.
    Zestawienie mówi więc, ile sądów fałszywych złoto rozstrzyga samo, czyli ile
    z nich nie musiał wydawać nikt.
    """
    ile = collections.Counter((sąd.sąd, wynik.klasa if wynik else "nieumieszczone") for sąd, wynik in zestawienia)
    wiersze = [f"{len(zestawienia)} sądów o wieloznaczności wobec złotych znaczników"]
    for (sąd, klasa), n in sorted(ile.items()):
        wiersze.append(f"  {n:>4}  {sąd} / {klasa}")
    wiersze += ["", "  wpis po wpisie:"]
    for sąd, wynik in zestawienia:
        if wynik is None:
            wiersze.append(f"  {'nieumieszczone':>14}  {sąd.sąd}: {sąd.zdanie}")
        else:
            wiersze.append(
                f"  {wynik.klasa:>14}  {sąd.sąd}, {wynik.ile} → {wynik.ile_ze_złotem}: {sąd.zdanie}"
            )
    return "\n".join(wiersze)


# --------------------------------------------------------------------------- #
# Wiersz poleceń
# --------------------------------------------------------------------------- #


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.znaczniki",
        description="Zawęź odczytania złotymi znacznikami NKJP i policz, co to rozstrzyga.",
    )
    parser.add_argument("archiwum", help="rozpakowany podkorpus milionowy NKJP")
    co = parser.add_mutually_exclusive_group(required=True)
    co.add_argument("--proza", metavar="DIR", help="proza z harness.nkjp, cała albo jej warstwa")
    co.add_argument(
        "--sądy",
        nargs="?",
        const=str(SĄDY),
        metavar="PLIK",
        help=f"zestaw złoto z sądami bazy (domyślnie {SĄDY.parent.name}/{SĄDY.name})",
    )
    parser.add_argument("--przykłady", type=int, default=5, help="ile zdań pokazać na klasę")
    parser.add_argument(
        "--jobs", type=int, default=os.cpu_count() or 1, help="na ile procesów podzielić rozbiór"
    )
    args = parser.parse_args(argv)

    archiwum = Path(args.archiwum)
    if not archiwum.is_dir():
        print(f"harness.znaczniki: nie ma takiego katalogu: {archiwum}", file=sys.stderr)
        print("harness.znaczniki: skąd wziąć podkorpus, mówi docs/corpora.md", file=sys.stderr)
        return 2
    if args.sądy is not None:
        print(wydruk_sądów(nad_sądami(archiwum, czytaj(Path(args.sądy)))))
        return 0
    korzeń = Path(args.proza)
    if not pliki_prozy(korzeń):
        print(f"harness.znaczniki: nie ma tu prozy: {korzeń}", file=sys.stderr)
        return 2
    wyniki, nieumieszczone = nad_korpusem(archiwum, korzeń, args.jobs)
    print(wydruk(wyniki, nieumieszczone, args.przykłady))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
