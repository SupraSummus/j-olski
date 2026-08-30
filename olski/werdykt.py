"""Werdykt o zdaniu: status wraz z tym, co autor ma poprawić.

Werdykt mówi o zdaniu więcej niż sam status, bo autor ma je poprawić.
Zdanie o dwóch odczytaniach nie jest olskie
(docs/subset.md#validity-is-uniqueness-not-just-derivability),
a :meth:`Verdict.explain` pokazuje, gdzie te odczytania się rozchodzą;
zdanie odrzucone dostaje miejsce, na którym rozbiór stanął,
a :func:`zatrzymania` każde takie miejsce, bo pierwsze zasłania następne.
Skąd te odczytania się biorą, mówi ``Verdict.morfologia``:
rozchodzą się w rolach, a zaczynają w lemacie i znaczniku formy.

Kto pyta o cały tekst, dostaje :func:`check` i :class:`Podsumowanie`,
czyli tyle werdyktów, ile zdań, oraz jedną odpowiedź policzoną z nich regułą.

Warstwa ta ani nie wnosi wieloznaczności, ani jej nie zdejmuje,
bo jest wypowiedzią o warstwach pod nią (docs/architecture.md).
Gramatykę czyta gotową z ``olski/subset/``,
a segmentację, po której werdykt pada, z ``olski/segmentacja.py``.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace

from olski.document import SENTENCE_CLOSE
from olski.grammar import Grammar
from olski.lematy import (
    ZAMIENNIKI_CUDZYSŁOWU,
    ZNAK_CUDZYSŁOWU_OTWIERAJĄCY,
    ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY,
)
from olski.morph import Reading, Segment
from olski.parse import (
    PRZYŁĄCZONY_DO,
    Node,
    Przyłączenie,
    Result,
    Rozbieżność,
    liście,
    parse,
    streszczenia,
    streszczone,
)
from olski.segmentacja import bez_licencji, morphology, na_czym_stanęło, sentences
from olski.subset import (
    DEKLARACJA,
    GRAMMAR,
    NAZWY_SZKOLNE,
    ORZECZNIK_ŁĄCZNIKA,
    WYRAŻENIE_PRZYIMKOWE,
)

#: Werdykt o tym, czego nikt nie napisał jako zdania: nagłówku, pozycji listy,
#: wierszu tabeli. Odrzucone znaczy „olski tego nie wyprowadza”, a to jest inne
#: zdanie o tekście i inna robota do zrobienia; docs/extraction.md trzyma wywód i
#: mierzy, jak dużą częścią rejestru ta klasa jest.
FRAGMENT = "fragment"

#: Werdykt o napisie, którego nic nie punktuje jako zdania, a który olski czyta,
#: kiedy się go domknie. Odcięty od :data:`FRAGMENT`, bo fragment jest aparatem
#: dokumentu, a ten napis jest zdaniem bez ostatniego znaku. Czemu mówi o napisie,
#: a nie o autorze, wywodzi docs/extraction.md.
NIEDOMKNIĘTE = "unclosed"

#: Znaki, którymi :func:`_domknięcie` domyka napis, w tej kolejności. Wykrzyknika
#: nie ma, bo terminal końca zdania bierze każdy z trzech, więc kropka zamyka
#: każde czytanie, które zamknąłby on, i mówi przy tym o gramatyce, a nie o tonie
#: autora. Pytajnik jest, bo pytanie zamyka się tylko nim
#: (`KONIEC_ZDANIA` i `PYTAJNIK` w ``olski/subset/słowa.py``).
DOMKNIĘCIA = (".", "?")


@dataclass(frozen=True)
class Domknięcie:
    """Znak, który z napisu robi zdanie, wraz z liczbą czytań, jakie mu daje.

    Liczba idzie ze znakiem, bo policzona drugi raz żądałaby drugiego rozbioru
    nad napisem, który werdykt już rozebrał.
    """

    znak: str
    czytań: int


def _domknięcie(zdanie: str, grammar: Grammar, doszło_do_końca: bool) -> Domknięcie | None:
    """Domknięcie, po którym olski ten napis czyta, albo ``None``.

    Pytanie to żąda drugiego rozbioru, więc pada tylko za tanim warunkiem:
    analiza doszła do końca napisu i każda forma ma licencję. Warunek jest
    konieczny, bo czytanie nad domkniętym bierze każdą formę, więc bierze ją i
    analiza częściowa nad napisem bez znaku. Nie wystarcza: analiza dochodzi do
    końca także tam, gdzie żadnego konstytuentu nie domyka, więc werdykt stoi na
    rozbiorze, a nie na samym warunku.
    """
    if not doszło_do_końca or SENTENCE_CLOSE.search(zdanie):
        return None
    for znak in DOMKNIĘCIA:
        wynik = parse(grammar, morphology(zdanie + znak), deklaracja=DEKLARACJA)
        if not wynik.rejected:
            return Domknięcie(znak, wynik.ile)
    return None


def _nierozstrzygnięte(przyłączenie: Przyłączenie) -> str:
    """Modyfikator i głowy, do których dochodzi, jako jeden wiersz werdyktu.

    Cudzysłów jest treścią, bo modyfikator jest ciągiem wziętym ze zdania i sam
    zawiera odstępy, więc bez niego nie widać, gdzie się kończy. Głowy dostają
    go tak samo, choć każda jest jednym słowem: pierwsze, co o nich trzeba
    wiedzieć, to że stoją w zdaniu tak, jak je autor napisał.
    """
    głowy = ", ".join(f"„{głowa}”" for głowa in przyłączenie.gospodarze)
    return f"„{przyłączenie.modyfikator}”{PRZYŁĄCZONY_DO}{głowy}"


def _odczytań(ile: int) -> str:
    """Liczba odczytań w formie, której polski liczebnik żąda po sobie.

    Formę wybiera jedno miejsce, bo werdykt nazywa tę liczbę w kilku wierszach.
    Nazwą jest odczytanie, a nie czytanie, i wywodzi to
    docs/subset.md#co-się-liczy-jako-jedno-odczytanie.
    """
    if ile == 1:
        return "jedno odczytanie"
    if ile % 10 in (2, 3, 4) and ile % 100 not in (12, 13, 14):
        return f"{ile} odczytania"
    return f"{ile} odczytań"


def _rozbieżny(rozbieżność: Rozbieżność) -> str:
    """Konstytuent i liczba jego czytań, jako jeden wiersz werdyktu.

    Wiersz ten mówi, gdzie w zdaniu leży wieloznaczność, której nie widać
    w streszczeniach czytań pod nim, i tylko tyle: różnicę autor odczyta z
    konstytuenta, a nazwana byłaby lematem, którego liczba czytań nie liczy
    (:class:`Rozbieżność`).
    """
    return f"„{rozbieżność.konstytuent}” ma {_odczytań(rozbieżność.ile)}"


def _po_szkolnemu(streszczenie: dict[str, str]) -> dict[str, str]:
    """To samo streszczenie nazwami, którymi te role nazywa składnia szkolna.

    Przekłada się samo zdanie z łącznikiem i poznaje się je po obsadzonym
    :data:`ORZECZNIK_ŁĄCZNIKA`, bo `podmiot` znaczy w nim co innego niż w zdaniu
    obok. Pytać trzeba przy tym o streszczenie, a nie o zdanie: `Ty to leń.` ma
    oba naraz, bo w jednym czytaniu `Ty` stoi przed łącznikiem, a w drugim jest
    zwykłym podmiotem. Sąd wykonywany przez ten przekład stoi przy
    :data:`NAZWY_SZKOLNE`.
    """
    if ORZECZNIK_ŁĄCZNIKA not in streszczenie:
        return streszczenie
    return {NAZWY_SZKOLNE.get(rola, rola): treść for rola, treść in streszczenie.items()}


def _nazwy_szkolne(rola: str) -> tuple[str, ...]:
    """Nazwy, pod którymi ta rola wychodzi z :func:`_po_szkolnemu`.

    Rola łącznika wychodzi pod dwiema, bo przekład rozdziela ją na podmiot i
    orzecznik: czytania różne tym, co obsadza pozycję przed łącznikiem, różnią
    się po przekładzie obiema.
    """
    if rola == ORZECZNIK_ŁĄCZNIKA:
        return (NAZWY_SZKOLNE[ORZECZNIK_ŁĄCZNIKA], NAZWY_SZKOLNE["podmiot"])
    return (rola,)


def _podpowiedź(nielicencjonowane: tuple[str, ...]) -> str:
    """Znaki, którymi ten rejestr cytuje, gdy autor zacytował innymi; inaczej nic.

    Czemu podpowiedź dostaje ten znak, a nie łącznik, mówi
    docs/subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka.

    Pytanie jest o pierwszy i ostatni znak formy, bo Morfeusz scala cudzysłów
    pojedynczy ze słowem w jedną formę — ``'Zasad'`` wychodzi jednym segmentem —
    a apostrof w środku słowa nie cytuje: ``fact's`` brałby podpowiedź, gdyby
    warunek pytał o samo zawieranie.
    """
    if not any(
        forma[0] in ZAMIENNIKI_CUDZYSŁOWU or forma[-1] in ZAMIENNIKI_CUDZYSŁOWU
        for forma in nielicencjonowane
    ):
        return ""
    #  Średnik otwiera podpowiedź, bo tym znakiem wycina ją kolejka form bez
    #  licencji (docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze).
    return (
        f"; a cytat otwiera się znakiem {ZNAK_CUDZYSŁOWU_OTWIERAJĄCY}"
        f" i zamyka znakiem {ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY}"
    )


@dataclass(frozen=True)
class Verdict:
    """What olski says about one sentence."""

    #: Zdanie tak, jak stoi w tekście. Segmenty są krawędziami grafu, a nie
    #: listą, więc sklejone dają naraz każdy podział, jaki Morfeusz na formie
    #: widzi: ``ktoś`` wychodzi wtedy jako ``kto ktoś ś``.
    text: str
    result: Result
    #: Formy nie do ominięcia, którym żadna produkcja nie bierze ani jednego
    #: czytania: odrzucenie stanęło na nich, a nie na strukturze. Pola bez
    #: wartości domyślnej, bo pusta krotka jest tu twierdzeniem o zdaniu, a
    #: ``Nowa program zapisuje ustawienia.`` ma je puste i jest odrzucone.
    nielicencjonowane: tuple[str, ...]
    #: Forma, której nie wzięła ani jedna analiza częściowa, czyli miejsce, na
    #: którym odrzucenie stanęło; ``None``, gdy analiza doszła do ostatniego
    #: znaku zdania. Pola bez wartości domyślnej z tego samego powodu co wyżej:
    #: ``None`` jest tu twierdzeniem, a nie brakiem odpowiedzi.
    zatrzymanie: str | None
    #: Domknięcie, po którym olski ten napis czyta, albo ``None``. Pole, a nie
    #: właściwość, bo :func:`_domknięcie` kosztuje rozbiór, a właściwość płaciłaby
    #: tyle razy, ile razy ktoś ją przeczyta.
    domknięcie: Domknięcie | None

    @property
    def punktowane(self) -> bool:
        """Czy tekst punktuje ten napis jako zdanie.

        Mianownik pomiaru pyta o to, a nie o :attr:`status`, bo odpowiedź jest ta
        sama nad oboma werdyktami o napisie niepunktowanym i nie kosztuje rozbioru,
        którego kosztuje :attr:`domknięcie` (:class:`Podsumowanie`).
        """
        return bool(SENTENCE_CLOSE.search(self.text))

    @property
    def status(self) -> str:
        if not self.punktowane:
            return NIEDOMKNIĘTE if self.domknięcie else FRAGMENT
        return self.result.status

    @property
    def readings(self) -> list[dict[str, str]]:
        """Streszczenia odczytań, każde raz (:func:`streszczenia`).

        Lista jest po to, żeby pokazać różnicę między odczytaniami,
        a różnicę spoza zasięgu streszczenia nazywa wiersz o konstytuencie
        (:func:`_rozbieżny`), więc powtórzony napis nie zostawia jej nienazwanej.
        Liczbę odczytań podaje las (:attr:`Result.ile`),
        więc skrócenie tej listy jej nie rusza.
        """
        return [
            tuple(map(_po_szkolnemu, streszczenie))
            for streszczenie in streszczenia(self.result.readings, DEKLARACJA)
        ]

    @property
    def morfologia(self) -> list[tuple[OdczytaniaFormy, ...]]:
        """Czym formy stoją w każdym odczytaniu: wpis na streszczenie z :attr:`readings`.

        Po co ta odpowiedź autorowi, mówi
        docs/pisanie-po-olsku.md#skąd-bierze-się-odczytanie-którego-autor-nie-widzi.

        Wiersz dostaje forma czytana więcej niż jednym sposobem, a odczytania w
        nim licencjonują ją w tym kształcie (:attr:`olski.parse.Leaf.odczytania`);
        wiersze składa :func:`_pod_streszczeniem`, a nad streszczeniem, które
        zbiera kilka kształtów, bierze odczytania z każdego z nich.
        Wpisów jest tyle, ile streszczeń, więc nad zdaniem urwanym na
        :data:`olski.parse.MAX_READINGS` mówią one o odczytaniach wypisanych.

        Zdanie bez ani jednego odczytania dostaje jeden wpis, a w nim każde
        odczytanie każdej formy (:func:`_morfologia_zdania`): odsiać ich nie ma
        czym. Rozstrzyga się to tutaj, a nie w wydruku, bo wydruki są dwa
        (``olski/check.py`` i ``witryna/werdykty.py``) i rozjechałyby się po cichu.
        """
        if self.result.rejected or not self.punktowane:
            return [_morfologia_zdania(self.text)]
        return [
            _pod_streszczeniem(drzewa)
            for _streszczenie, drzewa in streszczone(self.result.readings, DEKLARACJA)
        ]

    @property
    def rozbieżne(self) -> list[Rozbieżność]:
        """Konstytuenty rozbieżne, którym streszczenia naprawdę się różnią.

        Jedno streszczenie znaczy, że streszczenie tej różnicy nie widzi
        (:class:`Rozbieżność`), a wypisane byłoby wierszem bez treści.
        Warunek stoi tu raz na oba wydruki, na wiersz poleceń i na witrynę,
        bo napisany dwa razy rozjechałby się po cichu.
        """
        return [r for r in self.result.rozbieżności if len(r.czytania) > 1]

    def explain(self) -> str:
        if self.status == NIEDOMKNIĘTE:
            return (
                f"nic tego nie domyka: „{self.domknięcie.znak}” na końcu"
                f" daje {_odczytań(self.domknięcie.czytań)}"
            )
        if self.status == FRAGMENT:
            return "to nie zdanie: nic go nie punktuje jako zdania"
        if self.result.valid:
            return _odczytań(1)
        if self.result.rejected:
            if self.nielicencjonowane:
                # Cudzysłów jest treścią: najczęstszą formą bez licencji jest
                # przecinek, a lista rozdzielana przecinkami gubi bez niego granice.
                formy = ", ".join(f"„{forma}”" for forma in self.nielicencjonowane)
                podpowiedź = _podpowiedź(self.nielicencjonowane)
                return f"brak odczytania: żadna produkcja nie bierze {formy}{podpowiedź}"
            if self.zatrzymanie is None:
                return "brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania"
            return f"brak odczytania: analiza staje na „{self.zatrzymanie}”"
        przyłączenia = self.result.przyłączenia
        # Przekład idzie i tutaj (:func:`_nazwy_szkolne`), bo wiersz ten nie ma
        # nazywać roli, której lista czytań pod nim nie nazywa.
        różne = sorted(
            {
                nazwa
                for role in self.result.różniące
                # Przyłączenie nazwane niżej mówi o tej roli więcej niż sama jej
                # nazwa, więc wypisana obok byłaby tym samym zdaniem dwa razy.
                if not (przyłączenia and role == WYRAŻENIE_PRZYIMKOWE)
                for nazwa in _nazwy_szkolne(role)
            }
        )
        # Liczba i role wychodzą z lasu, więc granica wyliczania sięga listy
        # czytań i nie sięga tego wiersza: liczba jest liczbą, a nie „64+”.
        wiersz = _odczytań(self.result.ile)
        if różne:
            # Dwukropek oddziela nazwy od zdania: bez niego „różne w dopełnienie”
            # czyta się jak rzeczownik, którego przyimek nie odmienił.
            wiersz += f", różne w {'roli' if len(różne) == 1 else 'rolach'}: {', '.join(różne)}"
        return "; ".join(
            [
                wiersz,
                *map(_nierozstrzygnięte, przyłączenia),
                *map(_rozbieżny, self.result.rozbieżności),
            ]
        )


def zatrzymania(segmenty: list[Segment], grammar: Grammar | None = None) -> tuple[str, ...]:
    """Każde zatrzymanie odrzuconego zdania, a nie samo pierwsze.

    Werdykt nazywa jedno miejsce (:func:`na_czym_stanęło`), a zdanie długie ma ich
    kilka i pierwsze zasłania resztę, więc kto pisze pod tę gramatykę, nie widzi z
    werdyktu, ile jeszcze poprawek to zdanie zabierze; po co ta odpowiedź jest,
    mówi docs/pisanie-po-olsku.md.

    Analiza rusza od nowa **za** formą zatrzymania, a nie na niej: formy, której
    nie wzięła żadna analiza częściowa, nie weźmie też analiza zaczęta od niej, a
    przebieg stałby na miejscu. Krawędź przekraczającą cięcie trzeba przy tym
    zdjąć, bo graf segmentacji rozchodzi się na kilka dróg — ``ktoś`` wychodzi
    także jako ``kto`` i ``ś`` — a takiej krawędzi nie ma z czym w kawałku złożyć.

    Cięcie nie wskazuje usterki ani granicy konstrukcji, tak samo jak jedno
    zatrzymanie jej nie wskazuje.
    """
    grammar = grammar or GRAMMAR
    formy: list[str] = []
    while segmenty:
        stanęło = na_czym_stanęło(segmenty, parse(grammar, segmenty).furthest)
        if stanęło is None:
            break
        formy.append(stanęło.form)
        segmenty = [
            replace(segment, start=segment.start - stanęło.end, end=segment.end - stanęło.end)
            for segment in segmenty
            if segment.start >= stanęło.end
        ]
    return tuple(formy)


def werdykt(zdanie: str, segmenty: list[Segment], grammar: Grammar | None = None) -> Verdict:
    """Werdykt o zdaniu już zsegmentowanym, wraz z całym podsumowaniem.

    Segmenty przychodzą argumentem, a nie powstają tutaj, bo zależą od napisu, a
    nie od gramatyki: kto pyta o jedno zdanie kilka gramatyk — sonda różnicowa
    nad prozą — segmentuje je raz i pyta tyle razy, ile ma wariantów.

    Podsumowania werdykt bierze wszystkie, także te, których wołający nie czyta,
    a ceną tego jednego wejścia jest zatrzymanie: nad zdaniem odrzuconym bierze
    ono więcej niż sam rozbiór (:func:`olski.parse.podsumuj`), i płaci je także
    ten, kto go nie drukuje.
    Sonda nad prozą oszczędza gdzie indziej — pomija rozbiory, których odpowiedź
    zna z góry, i tych oszczędza tyle, ile wariantów minus jeden
    (``_bez_zbędnych`` w ``harness/ruch.py``).
    """
    grammar = grammar or GRAMMAR
    result = parse(grammar, segmenty, deklaracja=DEKLARACJA)
    stanęło = na_czym_stanęło(segmenty, result.furthest)
    nielicencjonowane = bez_licencji(segmenty, grammar)
    return Verdict(
        text=zdanie,
        result=result,
        nielicencjonowane=nielicencjonowane,
        zatrzymanie=stanęło.form if stanęło is not None else None,
        domknięcie=_domknięcie(zdanie, grammar, stanęło is None and not nielicencjonowane),
    )


def dalsze_zatrzymania(verdict: Verdict, grammar: Grammar | None = None) -> tuple[str, ...]:
    """Zatrzymania tego zdania poza tym, które nazwał już werdykt.

    Zdanie z czytaniem nie stanęło nigdzie, więc krotka jest wtedy pusta, i tak
    samo pusta jest nad fragmentem. Segmentacja idzie tu drugi raz, bo werdykt
    segmentów nie niesie (:func:`werdykt`).
    """
    if not verdict.punktowane or not verdict.result.rejected:
        return ()
    return zatrzymania(morphology(verdict.text), grammar)[1:]


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
    (:attr:`Verdict.nielicencjonowane`).
    Odczytania odsiane leksykalnie zdejmuje :func:`olski.segmentacja.morphology`,
    więc wykaz jest tym, co weszło do rozbioru.

    Segmentacja idzie tu drugi raz, bo werdykt segmentów nie niesie
    (:func:`werdykt`), a forma dzielona przez Morfeusza jeszcze inaczej dostaje
    tyle wierszy, ile podziałów ma w grafie (:attr:`Verdict.text`).
    """
    return tuple(
        OdczytaniaFormy(segment.form, _napisy(segment, segment.readings))
        for segment in morphology(zdanie)
    )


def check(text: str, grammar: Grammar | None = None) -> list[Verdict]:
    """Check every sentence of a text against the grammar."""
    return [werdykt(zdanie, morphology(zdanie), grammar) for zdanie in sentences(text)]


@dataclass(frozen=True)
class Podsumowanie:
    """Ile zdań tekstu jest olskich, dla tego, kto pyta o cały tekst.

    Liczby te wychodzą z werdyktów jedną regułą — fragment nie jest zdaniem, więc
    nie wchodzi do mianownika, a zdanie odrzucone nie ma czytania — i pyta o nie
    więcej niż jeden wołający, więc policzone u każdego z nich rozjeżdżają się po
    cichu: mianownik mniejszy o fragment czyta się jak pomiar, a nie jak pomyłka.
    """

    #: Zdania, którym gramatyka daje dokładnie jedno czytanie, czyli zdania olskie.
    olskie: int
    #: Zdania, czyli to, o czym werdykt orzeka: fragmentów nie ma tu ani w liczniku.
    zdań: int
    #: Zdania, którym gramatyka daje przynajmniej jedno czytanie.
    z_czytaniem: int
    #: Napisy, których nic nie interpunkuje jako zdania. Liczba jest jedna na oba
    #: werdykty o takim napisie, :data:`FRAGMENT` i :data:`NIEDOMKNIĘTE`, bo o
    #: mianowniku rozstrzyga jedno i to samo: domknięcia nie postawił nikt.
    fragmentów: int

    @classmethod
    def z_werdyktów(cls, werdykty: Sequence[Verdict]) -> Podsumowanie:
        zdania = [verdict for verdict in werdykty if verdict.punktowane]
        return cls(
            olskie=sum(verdict.result.valid for verdict in zdania),
            zdań=len(zdania),
            z_czytaniem=sum(not verdict.result.rejected for verdict in zdania),
            fragmentów=len(werdykty) - len(zdania),
        )

    def explain(self) -> str:
        #  Wiersz jest listą par, a nie zdaniem: liczba na końcu członu nie żąda
        #  zgody od słowa przed sobą, więc odmienia się tu jedno słowo, a nie każde.
        zdań = "zdania" if self.zdań == 1 else "zdań"
        podsumowanie = (
            f"olskie: {self.olskie} z {self.zdań} {zdań}; z odczytaniem: {self.z_czytaniem}"
        )
        if self.fragmentów:
            #  Nie „fragmenty, które nie są zdaniami”: napis niedomknięty jest w tej
            #  liczbie, a werdykt nad nim mówi, że olski to zdanie czyta.
            podsumowanie += f"; fragmenty, których nic nie punktuje jako zdania: {self.fragmentów}"
        return podsumowanie
