"""Wykazy, które werdykt wypisuje pod odczytaniem: formy, rachunek i żądania ramy.

Wykaz jest jeden na streszczenie odczytania
(``Verdict.readings`` w ``olski/werdykt/zdanie.py``),
więc wszystkie trzy drukuje jeden wydruk (``_wykaz`` w ``olski/check.py``).
Liczy się każdy z lasu, a nie z werdyktu, więc moduł ten o werdykcie nie wie.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field, replace

from olski import cennik, rejestr
from olski.lematy import LEMAT_PRZECZENIA, LEMAT_ZWROTNY
from olski.morph import Reading, Segment
from olski.parse import Leaf, Node, Tree, liście, sklej_formy, w_zakresie, zakresy
from olski.segmentacja import morphology
from olski.subset import DEKLARACJA
from olski.walencja import BIERNIK, CZASOWNIK, CZASOWNIK_ZWROTNY, DOPEŁNIACZ, PODMIOT
from olski.żądania import NIENAZWANE, PRZYPADKI, żądane

#: Symbole, na których staje zejście po role wiersza żądania: zdanie podrzędne
#: oraz konstytuent obsadzający ramę własnego czasownika
#: (:class:`olski.parse.Obsada`). Streszczenie staje na pierwszej z tych list,
#: a nie na drugiej, bo nazywa rolę wraz z wypełnieniem i nie pyta, czyja ona jest.
_STOP = (*DEKLARACJA.podrzędne, *DEKLARACJA.obsada.własna_rama)


@dataclass(frozen=True)
class OdczytaniaFormy:
    """Forma zdania wraz z odczytaniami, którymi tam stać może, każde napisem.

    Odczytanie jest napisem, a nie parą lematu i znacznika, bo oba wydruki
    wypisują je razem, a rozdzielone kazałyby każdemu z nich składać ten napis
    osobno.
    """

    forma: str
    odczytania: tuple[str, ...]


def _napisy(segment: Segment, odczytania: Iterable[Reading]) -> tuple[str, ...]:
    """Te odczytania jako napisy, każdy raz i w kolejności odczytań segmentu.

    Raz, bo lemat traci przy analizie indeks homonimu (:func:`olski.morph.analyse`),
    więc `Zamek` wychodzi z Morfeusza dwoma odczytaniami o jednym lemacie i jednym
    znaczniku, a wypisane oba czytają się jak pomyłka wydruku.

    Kolejność jest kolejnością segmentu, bo odczytania przychodzą tu zbiorem,
    z liści kilku drzew (:func:`_pod_streszczeniem`).
    """
    wybrane = set(odczytania)
    napisy: list[str] = []
    for czytanie in segment.readings:
        napis = f"{czytanie.lemma} {czytanie.tag}"
        if czytanie in wybrane and napis not in napisy:
            napisy.append(napis)
    return tuple(napisy)


def _pod_streszczeniem(drzewa: Iterable[Node]) -> tuple[OdczytaniaFormy, ...]:
    """Czym formy stoją pod tym streszczeniem: wiersz na formę, w porządku zdania.

    Rozpiętość liścia jest kluczem, bo forma powtórzona w zdaniu stoi w dwóch
    miejscach i każde bierze swoje odczytania: `koszt` przed dopełniaczem czyta
    się inaczej niż `koszt` w dopełnieniu.
    Zbiór wystarcza, bo kolejność wiersza bierze segment (:func:`_napisy`).
    """
    zebrane: dict[tuple[int, int], tuple[Segment, set[Reading]]] = {}
    for drzewo in drzewa:
        for liść in liście(drzewo):
            _segment, odczytania = zebrane.setdefault(liść.span, (liść.segment, set()))
            odczytania.update(liść.odczytania)
    return tuple(
        OdczytaniaFormy(segment.form, _napisy(segment, odczytania))
        for _span, (segment, odczytania) in sorted(zebrane.items())
        if len(segment.readings) > 1
    )


def _morfologia_zdania(zdanie: str) -> tuple[OdczytaniaFormy, ...]:
    """Formy zdania wraz z każdym odczytaniem, jakie olski w nich czyta.

    Odsiewu gramatyką nie ma: wchodzi tu i odczytanie, po które nie sięga żaden
    terminal, a formę, której gramatyka nie bierze wcale, nazywa werdykt
    (:attr:`olski.werdykt.zdanie.Verdict.nielicencjonowane`).
    Odczytania odsiane leksykalnie zdejmuje :func:`olski.segmentacja.morphology`,
    więc wykaz jest tym, co weszło do rozbioru.

    Segmentacja idzie tu drugi raz, bo werdykt segmentów nie niesie
    (``werdykt`` w ``olski/werdykt/zdanie.py``),
    a forma dzielona przez Morfeusza jeszcze inaczej dostaje tyle wierszy,
    ile podziałów ma w grafie (:attr:`olski.werdykt.zdanie.Verdict.text`).
    """
    return tuple(
        OdczytaniaFormy(segment.form, _napisy(segment, segment.readings))
        for segment in morphology(zdanie)
    )


def _koszty_drzewa(drzewo: Tree) -> Iterator[str]:
    """Pozycje cennika, którymi płaci to drzewo: węzeł swoją produkcją, liść swoją formą.

    Liść płaci najtańszym ze swoich odczytań, bo tak liczy go las
    (:meth:`olski.parse.Las.koszt_morfologii`): forma, którą ten kształt bierze
    i w rejestrze, i poza nim, nie płaci nic.
    """
    if isinstance(drzewo, Leaf):
        yield from min(
            (rejestr.pozycje(czytanie.kwalifikatory) for czytanie in drzewo.odczytania),
            key=cennik.suma,
            default=(),
        )
        return
    yield from drzewo.koszty
    for dziecko in drzewo.children:
        yield from _koszty_drzewa(dziecko)


@dataclass(frozen=True)
class Żądanie:
    """Czego czasownik zdania żąda od tego, co w jego pozycji stanęło.

    Wiersz jest jeden na obsadzoną pozycję, a nie jeden na rolę, bo jedna rola
    obsadza czasem dwie pozycje naraz: `Autor doradza czytelnikowi poprawkę.`
    ma dopełnienie w celowniku obok dopełnienia w bierniku, a czasownik żąda
    od nich czego innego.
    """

    #: Rola, którą streszczenie nazywa to wypełnienie.
    rola: str
    #: Formy wypełnienia i forma czasownika, tak jak stoją w zdaniu.
    wypełnienie: str
    czasownik: str
    #: Żądane klasy jako alternatywa, nazwane przed nienazwanymi
    #: (:data:`olski.żądania.NIENAZWANE`), a w każdej z tych grup alfabetycznie.
    klasy: tuple[str, ...]
    #: Lematy głowy wypełnienia, czyli słowa, którymi ta pozycja stoi. O nie pyta
    #: deklaracja osób (``olski/osoby.py``), bo deklaruje się lemat, a nie formę.
    #: Poza porównaniem, bo wiersz jest o pozycji, a nie o głowie, i dwa kształty
    #: dają czasem tę samą pozycję o dwóch głowach (:func:`_zwinięte`).
    lematy: frozenset[str] = field(compare=False)


@dataclass(frozen=True)
class _Czasownik:
    """Czasownik zdania składowego: słowa, którymi bywa, jego forma i przeczenie."""

    #: Pary lematu i klasy słowa, czyli klucze, którymi pyta się pliku żądań.
    #: Jest ich kilka tam, gdzie formę licencjonuje w tym kształcie kilka odczytań.
    słowa: frozenset[tuple[str, str]]
    forma: str
    #: Czy przy tym czasowniku stoi przeczenie (:data:`olski.lematy.LEMAT_PRZECZENIA`).
    przeczony: bool


def _zwinięte(żądania: Iterable[Żądanie]) -> tuple[Żądanie, ...]:
    """Te żądania bez powtórzeń, z lematami zebranymi po wszystkich kształtach.

    Wiersz mówi o pozycji, a nie o głowie wypełnienia,
    więc pozycja, którą dwa kształty nazywają dwiema głowami, wychodzi stąd raz:
    podmiotem w `Wszystko to deklaruje REUSE.toml.` jest `wszystko` z określeniem
    `to` albo `to` z określeniem `wszystko`, a żądanie stoi w obu to samo.
    Lematy zbierają się wtedy tak, jak zbiera je żądanie po słowach czasownika
    (:func:`olski.żądania.żądane`), i deklaracja pyta o zbiór cały
    (:meth:`olski.osoby.Osoby.nazywają`).
    """
    zebrane: dict[Żądanie, frozenset[str]] = {}
    for żądanie in żądania:
        zebrane[żądanie] = zebrane.get(żądanie, frozenset()) | żądanie.lematy
    return tuple(replace(żądanie, lematy=lematy) for żądanie, lematy in zebrane.items())


def _żądania_streszczenia(drzewa: Iterable[Node]) -> tuple[Żądanie, ...]:
    """Żądania obsadzonych pozycji tych czytań, każde raz i rolami po kolei.

    Drzew jest kilka z tego samego powodu co w :func:`_pod_streszczeniem`:
    jedno streszczenie zbiera czasem kilka kształtów, a wiersz powtórzony nie
    mówi nic ponad ten nad sobą.

    Zdanie składowe pyta o swój czasownik osobno, tak samo jak osobno się
    streszcza, a zdania podrzędnego ta warstwa nie otwiera i z tego samego
    powodu: pozycje tamtego zdania są ramą tamtego czasownika
    (:attr:`olski.parse.Deklaracja.podrzędne`).
    """
    return _zwinięte(
        żądanie
        for drzewo in drzewa
        for zakres in zakresy(drzewo, DEKLARACJA.składowe)
        for żądanie in _żądania_składowego(drzewo, zakres)
    )


def _żądania_składowego(drzewo: Node, zakres: tuple[int, int]) -> Iterator[Żądanie]:
    """Żądania jednego zdania składowego, po jednym na obsadzoną pozycję."""
    obsada = DEKLARACJA.obsada
    czasownik = _czasownik(drzewo, zakres)
    if czasownik is None:
        return
    for rola in (obsada.podmiot, *obsada.przypadkowe):
        for węzeł in w_zakresie(drzewo, rola, _STOP, zakres):
            klasy = _żądane_od(węzeł, rola, czasownik)
            if klasy:
                głowa = węzeł.liść_głowy()
                yield Żądanie(
                    rola,
                    sklej_formy(węzeł.forms()),
                    czasownik.forma,
                    klasy,
                    frozenset(czytanie.lemma for czytanie in głowa.odczytania),
                )


def _czasownik(drzewo: Node, zakres: tuple[int, int]) -> _Czasownik | None:
    """Czasownik, który rządzi ramą tego zdania składowego, albo ``None``.

    ``None`` znaczy, że zdanie orzeka bez czasownika: orzeczeniem rzeczownikowym
    albo orzecznikiem przy kopuli, i ramy nie ma wtedy o co pytać.

    Cząstka zwrotna i przeczenie stoją w tym samym konstytuencie co czasownik —
    ``orzeczenie → się otwiera`` — więc obie widać po jego liściach.
    Pierwsza z nich czyni z niego inne słowo, więc wchodzi do klucza pliku żądań,
    a druga zostaje osobno, bo mówi o przypadku dopełnienia, a nie o słowie.
    """
    for rola in DEKLARACJA.obsada.orzeczenia:
        for węzeł in w_zakresie(drzewo, rola, _STOP, zakres):
            lematy = {czytanie.lemma for liść in liście(węzeł) for czytanie in liść.odczytania}
            klasa = CZASOWNIK_ZWROTNY if LEMAT_ZWROTNY in lematy else CZASOWNIK
            głowa = węzeł.liść_głowy()
            return _Czasownik(
                słowa=frozenset((czytanie.lemma, klasa) for czytanie in głowa.odczytania),
                forma=głowa.segment.form,
                przeczony=LEMAT_PRZECZENIA in lematy,
            )
    return None


def _żądane_od(węzeł: Node, rola: str, czasownik: _Czasownik) -> tuple[str, ...]:
    """Klasy, których czasownik żąda od tego wypełnienia; krotka pusta jest milczeniem.

    Pozycji kandydujących bywa kilka (:func:`_pozycje`), a wiersz wychodzi stąd
    dopiero wtedy, gdy żąda dokładnie jedna z nich: przy dwóch żądających nie
    widać, które z tych żądań autor ma przeczytać.
    """
    żądające = [
        klasy
        for pozycja in _pozycje(węzeł, rola, czasownik)
        if (klasy := żądane(czasownik.słowa, pozycja))
    ]
    if len(żądające) != 1:
        return ()
    return tuple(sorted(żądające[0], key=lambda klasa: (klasa in NIENAZWANE, klasa)))


def _pozycje(węzeł: Node, rola: str, czasownik: _Czasownik) -> tuple[str, ...]:
    """Pozycje ramy, w których to wypełnienie stać może.

    Podmiot nazywa swoją pozycję sam, a rola przypadkowa nazywa ją przypadkiem
    głowy wypełnienia: `ustawienia` w bierniku obsadza pozycję ``acc``.
    Przypadek bierze się z odczytań licencjonujących ten kształt, a nie z jednego
    z nich, bo forma bywa dwoma słowami naraz — `ustawienia` jest rzeczownikiem
    i odsłownikiem — i pozycję obsadza w obu tak samo.

    Pozycje są dwie tam, gdzie przy czasowniku stoi przeczenie: dopełnienie
    w bierniku staje pod nim w dopełniaczu
    (docs/konstrukcje-gramatyczne/orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem),
    więc dopełniacz nazywa tam obie pozycje naraz.
    """
    if rola == DEKLARACJA.obsada.podmiot:
        return (PODMIOT,)
    przypadki = frozenset.intersection(
        *(czytanie.tag.get("case") for czytanie in węzeł.liść_głowy().odczytania)
    )
    kandydaci = set(przypadki) & set(PRZYPADKI)
    if czasownik.przeczony and DOPEŁNIACZ in kandydaci:
        kandydaci.add(BIERNIK)
    return tuple(sorted(kandydaci))
