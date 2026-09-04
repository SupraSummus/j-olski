"""Tekst do makiety: drzewo wylosowane zamiast napisanego.

Makieta żąda tekstu, zanim ktokolwiek ma co powiedzieć,
i dostaje zwykle łacińską sieczkę, po której nie widać polskiej kolumny:
polskie słowo jest dłuższe, odmienia się i inaczej łamie wiersz.
Losowane jest tu drzewo, a nie napis, bo gramatyczności nie ma czym naruszyć —
zgodność w tym kierunku jest policzona, a nie sprawdzona.
Odsiewa się jedno, czyli zdanie, z którego czytelnik nie odzyska ról,
i pyta o to ``olski/skład/przegląd.py``.
Po co ten moduł jest i czego zażądał od tego pakietu, mówi ``docs/po-wypisaniu.md``.

Sensu ten moduł nie pilnuje i pilnować nie ma.
`Wiadro kupiło nóż.` jest zdaniem polskim, a nie zdaniem o wiadrze,
i taki tekst do makiety pasuje, bo czytelnik ma zobaczyć kształt kolumny,
a nie zacząć czytać.
Tabele niżej dobierają więc lematy pod formę i pod rytm,
a nie pod to, kto co komu robi; o wyjątkach mówi ``Obsada``.
Fakt o polszczyźnie, który do takiej tabeli wszedł albo z niej wypadł,
jest przy tym faktem o każdym drzewie, a nie o tym jednym programie,
i mówi o tym ``docs/po-wypisaniu.md`` wraz z tym, gdzie taki fakt należy.

Rytm jest za to wyborem, bo makieta pokazuje właśnie go.
Kształty zdania wyczerpują kategorie, które niosą
``olski.skład.grupa`` oraz ``olski.skład.składnia``,
a ten sam nie wypada dwa razy pod rząd,
bo jednostajność jest usterką i wylicza ją ``docs/fiction.md``.
Obsadę akapitu niosą ``Postać``, bo dopiero one pozwalają opuścić podmiot,
a tekst, w którym każde zdanie powtarza swój podmiot, czyta się jak lista.

Warstwy nazw z ``olski/skład/słownik.py`` ten moduł nie woła i nie ma po co:
tamten zapis zamienia lemat na nazwę atrybutu dla tego, kto drzewo pisze,
a program trzymający lematy w tabeli woła konstruktory wprost.

    python3 -m olski.skład.makieta --akapity 3
    python3 -m olski.skład.makieta --ziarno 1871
"""

from __future__ import annotations

import argparse
import functools
import random
import sys
from collections.abc import Sequence
from dataclasses import dataclass

from olski.skład.grupa import Byt, Czyj, Jaki, Rzecz, byt
from olski.skład.kontekst import Kontekst
from olski.skład.morfologia import rodzaj_rzeczownika
from olski.skład.opowieść import Akapit, Opowieść, Postać
from olski.skład.przegląd import przejrzyj
from olski.skład.składnia import (
    Ciąg,
    Jest,
    Komu,
    Okolicznik,
    Opis,
    Przysłówek,
    Treść,
    Zdanie,
    nie,
    po_poprzednim,
    zdarzenie,
)
from olski.skład.spójniki import SPÓJNIKI

#: Ludzie, czyli te lematy, które w tekście robią coś komuś innemu.
#: Rodzaj rozdziela się tu z rozmysłu, bo czas przeszły go niesie
#: i to on daje zdaniu rytm, którego jedna kolumna rodzajowa nie ma.
OSOBY = (
    "aptekarz",
    "chłopiec",
    "córka",
    "czeladnik",
    "dziewczyna",
    "gospodarz",
    "kowal",
    "krawiec",
    "kucharka",
    "kupiec",
    "mieszczanin",
    "praczka",
    "sąsiad",
    "sąsiadka",
    "wdowa",
    "zegarmistrz",
)

#: Rzeczy, czyli to, co w zdaniu staje dopełnieniem, narzędziem albo podmiotem.
#: Podmiotem staje tak samo jak osoba, bo ``Postać`` człowieka nie żąda,
#: a `Świeca zgasła.` jest zdaniem, którego makieta potrzebuje.
RZECZY = (
    "beczka",
    "bochenek",
    "deska",
    "dzban",
    "klucz",
    "koszyk",
    "kufer",
    "list",
    "lustro",
    "nóż",
    "okno",
    "skrzynia",
    "sukno",
    "szal",
    "świeca",
    "wiadro",
    "zegar",
)

#: Miejsca, przed którymi staje ``w``: w izbie, do izby.
#: Rozdzielone od tych z ``na``, bo wybór między tymi przyimkami jest faktem
#: o rzeczowniku, a leksykonu na to ten pakiet nie ma.
#: Lematu żądającego przyimka zgłoskotwórczego nie wymienia żadna z tych tabel,
#: bo z drzewa wyszłoby `z strychu`.
MIEJSCA_W = (
    "brama",
    "izba",
    "kamienica",
    "karczma",
    "komora",
    "kuchnia",
    "młyn",
    "ogród",
    "piwnica",
    "sień",
    "warsztat",
    "wieża",
)

#: Miejsca, przed którymi staje ``na``: na rynku, na rynek.
MIEJSCA_NA = ("dziedziniec", "most", "podwórze", "próg", "rynek", "targ", "ulica")

#: Wszystkie miejsca, bo źródło i droga biorą jedne i drugie: z rynku, z izby.
MIEJSCA = (*MIEJSCA_W, *MIEJSCA_NA)

#: Miejsca, pod którymi i przed którymi coś stanie, czyli te o zewnętrznej stronie:
#: `pod bramą` jest zdaniem o miejscu, a `pod izbą` zdaniem o piwnicy pod nią.
BUDOWLE = ("brama", "kamienica", "karczma", "most", "młyn", "wieża")

#: Pory dnia, które polszczyzna wyraża samym narzędnikiem: wieczorem, nocą.
PORY = ("ranek", "świt", "wieczór", "zmierzch")

#: Pory, przed którymi staje ``w``, a jest to jedna: `w nocy`.
#: Wpis ``("w", "czas")`` w ``olski/skład/przyimki.py`` powstał dla tego słowa
#: i dla niego jednego działa, bo `w wieczorze` zdaniem polskim nie jest,
#: więc tabela wymienia to słowo, zamiast liczyć na relację.
PORY_W_MIEJSCOWNIKU = ("noc",)

#: Przymiotniki, którymi bywa określona rzecz, miejsce albo pora.
#: `kamienny` tej tabeli nie ma, bo `kamienna kamienica` powtarza rdzeń rzeczownika,
#: a losowanie nie ma czym takiej pary zauważyć.
CECHY = (
    "ciemny",
    "cichy",
    "ciężki",
    "drewniany",
    "duży",
    "gliniany",
    "krzywy",
    "mały",
    "mokry",
    "nowy",
    "pusty",
    "stary",
    "wąski",
    "zimny",
)

#: Przymiotniki, którymi bywa określona osoba.
#: Tabela jest osobna, bo `pusta wdowa` zgadza się rodzajem, liczbą i przypadkiem,
#: a mówi o człowieku to, co mówi się o suknie.
CECHY_OSÓB = ("cichy", "duży", "mały", "młody", "stary")

#: Przysłówki, czyli okoliczność wyrażona jednym słowem.
#: Tabela wymienia te, którym SGJP daje znakowanie przysłówkowe,
#: bo ``Przysłówek`` w ``olski/skład/składnia.py`` żąda go wraz ze stopniem równym,
#: a `znowu` niesie samą partykułę i zgłosiłoby ``BrakFormy``.
#: `długo` tej tabeli nie ma, bo trwanie żąda czasownika niedokonanego,
#: a `kupił klucz długo` jest tą samą usterką co `zaczął zapłakać`.
PRZYSŁÓWKI = ("cicho", "nagle", "powoli", "późno", "prędko", "rano", "wkrótce")

#: Czasowniki ruchu, czyli te, przy których okoliczność mówi, dokąd albo skąd.
#: Część z nich biernik u Walentego bierze, więc o tym, że dopełnienia nie dostaną,
#: rozstrzyga ta tabela, a nie leksykon: `Czeladnik zszedł.` jest zdaniem,
#: którego makieta chce.
CZYNY_RUCHU = ("wrócić", "wyjść", "zejść")

#: Czasowniki, przy których nie staje ani dopełnienie, ani cel.
#: Rozdzielone od ruchu, bo relacja celu żąda czasownika, który dokądś prowadzi,
#: a `Sukno mieszkało do mostu.` wychodzi z drzewa poprawnie.
#: `czekać` tej tabeli nie ma, bo polszczyzna czeka `na kogoś`,
#: więc `czekał na izbach` czyta się przez ramę, której ta gramatyka nie niesie.
CZYNY_STANU = ("mieszkać", "milczeć", "siedzieć", "stać", "zapłakać", "zasnąć", "zniknąć")

#: Czasowniki, które biorą dopełnienie w bierniku.
CZYNY_Z_BIERNIKIEM = (
    "kupić",
    "naprawić",
    "otworzyć",
    "podnieść",
    "policzyć",
    "postawić",
    "przynieść",
    "rozbić",
    "schować",
    "sprzedać",
    "wynieść",
    "wziąć",
    "zamknąć",
    "zapalić",
    "zasłonić",
    "zgasić",
    "zgubić",
    "znaleźć",
    "zważyć",
)

#: Czasowniki, które biorą dopełnienie w celowniku obok tego w bierniku,
#: czyli te, przy których staje i rzecz, i ten, komu się ją daje.
#: Tabela jest osobna od biernikowej, bo celownik jest osobną pozycją ramy
#: i `Kowal zgasił sąsiadowi świecę.` mówi o celowniku, którego rama nie ma
#: (docs/walencja.md#wolny-celownik-nie-jest-pozycją-ramy-i-nie-wchodzi-leksykonem).
CZYNY_Z_CELOWNIKIEM = ("dać", "oddać", "pokazać", "przynieść", "sprzedać", "zostawić")

#: Czasowniki, które biorą bezokolicznik pod kontrolą własnego podmiotu.
#: Czasownika żądającego bezokolicznika niedokonanego ta tabela nie wymienia,
#: bo aspektu nikt tu nie sprawdza, a `zaczął zapłakać` zdaniem polskim nie jest.
CZYNY_Z_BEZOKOLICZNIKIEM = ("chcieć", "musieć", "próbować", "umieć", "woleć", "zdążyć")

#: Czasowniki, które biorą zdanie podrzędne wprowadzone przez ``że``.
CZYNY_ZE_ZDANIEM = (
    "myśleć",
    "pamiętać",
    "powiedzieć",
    "usłyszeć",
    "widzieć",
    "wiedzieć",
    "zauważyć",
)

#: Okoliczności wyrażone rzeczą: słowo, relacja i tabela, z której rzecz wychodzi.
#: Tabela idzie razem ze słowem, bo relacja o niej nie rozstrzyga:
#: `od sąsiada` i `od studni` stoją w jednej relacji, a druga z tych par
#: nie jest tym, czego szuka zdanie o tym, skąd ktoś coś wziął.
#: Para słowa z relacją ma świadka w ``olski/skład/przyimki.py``,
#: więc wiersz, który tam nie stoi, zgłasza się w ``tests/test_makieta.py``.
#: Czas stoi osobno, bo przyjmuje go każde zdarzenie, a miejsca i celu nie:
#: `wrócił wieczorem` mówi to samo przy ruchu i przy staniu.
OKOLICZNOŚCI_CZASU = (
    ("", "czas", PORY),
    ("w", "czas", PORY_W_MIEJSCOWNIKU),
)

#: Czas wraz z miejscem, czyli tabela dla zdarzenia, które nikogo nie przemieszcza.
OKOLICZNOŚCI = (
    *OKOLICZNOŚCI_CZASU,
    ("na", "miejsce", MIEJSCA_NA),
    ("pod", "miejsce", BUDOWLE),
    ("przed", "miejsce", BUDOWLE),
    ("w", "miejsce", MIEJSCA_W),
)

#: Czas wraz z celem, źródłem i drogą, czyli tabela dla czasownika ruchu.
#: Miejsca w niej nie ma, bo `zejść w karczmie` mówi o ruchu i podaje postój.
OKOLICZNOŚCI_RUCHU = (
    *OKOLICZNOŚCI_CZASU,
    ("do", "cel", MIEJSCA_W),
    ("na", "cel", MIEJSCA_NA),
    ("od", "źródło", OSOBY),
    ("po", "droga", MIEJSCA),
    ("z", "źródło", MIEJSCA),
)

#: Miejsce wraz z narzędziem, czyli tabela dla zdania o czynności.
#: Narzędzie dochodzi dopiero tutaj, bo `Zasnął nożem.` wychodzi z drzewa poprawnie,
#: a czyta się jak usterka losowania, nie jak zdanie do makiety:
#: narzędzia żąda ten, kto coś robi rzeczy, a nie ten, kto po prostu jest.
OKOLICZNOŚCI_CZYNNE = (*OKOLICZNOŚCI, ("", "narzędzie", RZECZY))

#: Spójniki, którymi okoliczność wyrażona zdarzeniem wchodzi do zdania.
#: Wychodzą one z leksykonu, a nie z drugiej tabeli tutaj,
#: bo o tym, które słowo w której relacji stoi, rozstrzyga ``olski/skład/spójniki.py``,
#: a spójnik dopisany tam ma wejść do makiety bez drugiego wpisu.
SPÓJNIKI_OKOLICZNOŚCI = tuple(SPÓJNIKI)

#: Ile najmniej i najwięcej zdań dostaje akapit.
ZDAŃ = (3, 6)

#: Ile osób oraz ile rzeczy wraca w jednym akapicie.
OSÓB = (2, 3)
RZECZY_W_OBSADZIE = (1, 2)

#: Jak często zdanie o samym zdarzeniu mówi o ruchu, a nie o stanie.
RUCH = 0.5

#: Jak często losowanie dokłada rzecz, której zdanie mieć nie musi.
#: Liczby są wyborem rytmu, a nie pomiarem: makieta ma wyglądać jak proza,
#: a proza nie określa każdej grupy imiennej i nie przeczy co drugiemu zdaniu.
CECHA = 0.4
DOPEŁNIACZ = 0.15
LICZBA_MNOGA = 0.25
PRZECZENIE = 0.15
OKOLICZNOŚĆ = 0.6
CZOŁO = 0.4


def losuj(ziarno: int, akapitów: int = 4) -> Opowieść:
    """Opowieść o niczym, ta sama za każdym razem, gdy ziarno jest to samo.

    Opowieścią, a nie tekstem o tym, co się dzieje, bo drugiego konstruktora
    ``olski/skład/opowieść.py`` nie ma, a czas przeszły niesie rodzaj,
    więc daje makiecie i rytm, i role przypięte do czasownika.
    """
    los = random.Random(ziarno)
    return Opowieść(*(_akapit(los) for _ in range(akapitów)))


@dataclass(frozen=True)
class Obsada:
    """Kto i co wraca w akapicie, rozdzielone na osoby i na rzeczy.

    Rzecz wraca w obsadzie na równi z osobą, bo ``Postać`` człowieka nie żąda,
    a `Świeca zgasła. Zniknęła w piwnicy.` opuszcza podmiot tak samo
    jak dwa zdania o czeladniku.

    Rozdzielone są dlatego, że dwie pozycje pytają, czy podmiot jest kimś.
    Wola i sąd o świecie należą do osoby, a `Beczka wiedziała, że świt zgasł.`
    czyta się jak usterka losowania, a nie jak zdanie do makiety.
    Poza tymi dwiema pozycjami sensu ten moduł nie pilnuje,
    więc rzecz podmiotem staje wszędzie tam, gdzie zdanie mówi, co się stało.
    """

    osoby: tuple[Postać, ...]
    rzeczy: tuple[Postać, ...]

    #: Lematy, które w tym akapicie już kogoś nazywają.
    #: Pytają o nie te pozycje, które mają nie nazwać drugi raz tego samego,
    #: i pytają o lematy, bo z ``Postać`` nazwy się nie wyciąga.
    lematy: frozenset[str]

    @property
    def wszyscy(self) -> tuple[Postać, ...]:
        return (*self.osoby, *self.rzeczy)


def _obsada(los: random.Random) -> Obsada:
    """Obsada akapitu: kilka osób wraz z jedną albo dwiema rzeczami."""
    osoby = _różne(los, OSOBY, los.randint(*OSÓB))
    rzeczy = _różne(los, RZECZY, los.randint(*RZECZY_W_OBSADZIE))
    return Obsada(
        osoby=tuple(Postać(Rzecz(lemat)) for lemat in osoby),
        rzeczy=tuple(Postać(Rzecz(lemat)) for lemat in rzeczy),
        lematy=frozenset((*osoby, *rzeczy)),
    )


def _akapit(los: random.Random) -> Akapit:
    """Akapit wraz z obsadą, do której wracają jego zdania.

    Obsada jest tu po to, żeby akapit czytał się jak akapit:
    ``pomijalny`` w ``olski/skład/składnia.py`` opuszcza podmiot dopiero wtedy,
    gdy dwa zdania obok siebie mówią o tej samej rzeczy,
    a tożsamość niesie sama ``Postać``, nie lemat.
    """
    obsada = _obsada(los)
    zdania: list[Zdanie] = []
    poprzedni = None
    for _ in range(los.randint(*ZDAŃ)):
        kształt = _kształt(los, poprzedni)
        zdania.append(_bez_kolizji(los, kształt, obsada, zdania[-1] if zdania else None))
        poprzedni = kształt
    return Akapit(*zdania)


def _różne(los: random.Random, tabela: Sequence, ile: int) -> list:
    """Tyle członów tabeli, ile zażądano, i każdy inny.

    Losowane pojedynczo, a nie próbką, bo próbka wybiera algorytmem,
    który wolno zmienić między wydaniami Pythona,
    a ten sam tekst z tego samego ziarna jest tu żądaniem.
    """
    wybrane: list = []
    while len(wybrane) < ile:
        człon = los.choice(tabela)
        if człon not in wybrane:
            wybrane.append(człon)
    return wybrane


def _bez_kolizji(los: random.Random, kształt, obsada: Obsada, poprzednie: Zdanie | None) -> Zdanie:
    """Zdanie tego kształtu, które czyta się jednym sposobem.

    Odsiewa ``olski/skład/przegląd.py``, czyli to samo zgłoszenie, które autorowi
    mówi, że jego napis nie oddaje ról z drzewa.
    Autor dostaje je jako raport i sam rozstrzyga, a losowanie nie ma czego
    rozstrzygać, więc pyta o ten sam werdykt i losuje jeszcze raz.

    Pytane jest o zdanie stojące za poprzednim, a nie o zdanie stojące samo,
    bo akapit opuszcza podmiot i wtedy pytanie ma inną odpowiedź:
    po `Kowal zasnął.` zdanie o tym samym kowalu wychodzi samym `Wziął nóż.`,
    a tam nie widać już, czy nóż jest podmiotem, czy dopełnieniem.
    Kontekst liczy więc ``po_poprzednim``, czyli to samo, co zapyta akapit,
    składając z tych zdań tekst.

    Pętla się domyka, bo każde kolejne losowanie bierze role od nowa.
    Podmiot wypisany kolizji nie zrobi, gdy jest nim osoba:
    biernik rzeczownika osobowego równa się dopełniaczowi, a nie mianownikowi,
    więc czytelnik wie, która rola jest którą, choćby dopełnienie brzmiało tak samo.
    Podmiot opuszczony tej obrony nie ma, bo żadnej swojej formy nie pokazuje,
    a zwalnia go forma dopełnienia albo podmiot wylosowany inny niż w zdaniu obok,
    po którym opuszczenia nie ma wcale.
    """
    kontekst = Kontekst(czas=Opowieść.CZAS)
    while True:
        zdanie = kształt(los, obsada)
        if not przejrzyj(zdanie, po_poprzednim(zdanie, poprzednie, kontekst)):
            return zdanie


def _kształt(los: random.Random, poprzedni):
    """Kształt zdania inny niż ten, który wypadł przed nim.

    Powtórzenie odsiewa się tu, a nie w tabeli kształtów,
    bo jednostajność jest własnością sąsiedztwa, a nie listy:
    dwa zdania jednego kształtu obok siebie czyta się jak jedno powtórzone,
    a rozdzielone trzecim już nie.
    """
    while True:
        kształt = los.choice(KSZTAŁTY)
        if kształt is not poprzedni:
            return kształt


def _bez_dopełnienia(los: random.Random) -> tuple[str, tuple]:
    """Czasownik bez dopełnienia wraz z tabelą okoliczności, którą on przyjmuje.

    Jedna funkcja, a nie dwa losowania w każdym kształcie zdania,
    bo czasownik i tabela są tu jedną decyzją: relacja celu żąda ruchu,
    a stan żąda miejsca.
    """
    if los.random() < RUCH:
        return los.choice(CZYNY_RUCHU), OKOLICZNOŚCI_RUCHU
    return los.choice(CZYNY_STANU), OKOLICZNOŚCI


def _cechy(tabela: Sequence[str]) -> tuple[str, ...]:
    """Przymiotniki, którymi wolno określić rzecz z tej tabeli."""
    return CECHY_OSÓB if tabela is OSOBY else CECHY


def _grupa(
    los: random.Random,
    tabela: Sequence[str],
    *,
    goła: bool = False,
    cechy: Sequence[str] | None = None,
) -> Byt:
    """Grupa imienna zbudowana nad rzeczą wylosowaną z tej tabeli."""
    przymiotniki = _cechy(tabela) if cechy is None else cechy
    return _rola(los, Rzecz(los.choice(tabela)), goła=goła, cechy=przymiotniki)


def _rola(
    los: random.Random, rzecz: Rzecz, *, goła: bool = False, cechy: Sequence[str] = CECHY
) -> Byt:
    """Rzecz jako rola: wraz z liczbą i z określeniami albo bez nich.

    Pełna grupa bierze liczbę, przymiotnik oraz określenie w dopełniaczu,
    a każde z nich osobnym losem, i te dwa określenia składają się ze sobą,
    bo ``Jaki`` bierze pod siebie ``Czyj``: `stary klucz kucharki`.
    Właściciel jest zwykłą rzeczą, a nie ``Postać``, tak jak `wzrok potwora` w legendzie:
    określenie mówi, o który klucz chodzi, i nie wprowadza nikogo,
    o kim czytelnik miałby pamiętać w zdaniu obok.

    Goła bierze jedną rzecz i najwyżej przymiotnik, a żądają jej dwie pozycje.
    Pora dnia, bo `w nocach` nie jest polszczyzną,
    a `w nocy chłopca` mówi, czyja to była noc.
    Orzecznik, bo podmiotem jest tam jedna osoba,
    a `kowalem kucharki` orzeka o dwóch naraz.
    """
    nominalne = Jaki(los.choice(cechy), rzecz) if cechy and los.random() < CECHA else rzecz
    if not goła and los.random() < DOPEŁNIACZ:
        nominalne = Czyj(nominalne, byt(Rzecz(los.choice(OSOBY))))
    return Byt(nominalne, "pl" if not goła and los.random() < LICZBA_MNOGA else "sg")


def _zdarzenie(los: random.Random, kto, czyn: str, *reszta):
    """Zdarzenie, czasem zaprzeczone, bo przeczenie jest cechą zdania, a nie kategorią."""
    zdanie = zdarzenie(kto, czyn, *reszta)
    return nie(zdanie) if los.random() < PRZECZENIE else zdanie


def _okoliczności(los: random.Random, tabela=OKOLICZNOŚCI, *, wysuwalne: bool = True) -> tuple:
    """Zero albo jedna okoliczność, czasem wysunięta na czoło zdania.

    Jedna, a nie ile wypadnie, bo dwie okoliczności obok siebie —
    `milczał wieczorem cicho` — czytają się jak zdanie, któremu ktoś przerwał.

    Wysunięcia nie dostaje zdanie bez podmiotu, czyli bezokolicznik:
    czołem jest tam miejsce przed samym czasownikiem,
    więc `wolał do studni zapłakać` przestawia okoliczność w środek zdania nadrzędnego,
    zamiast powiedzieć, o czym zdanie podrzędne jest.
    """
    if los.random() >= OKOLICZNOŚĆ:
        return ()
    okoliczność = _okoliczność(los, tabela)
    na_czele = wysuwalne and los.random() < CZOŁO
    return (okoliczność.temat if na_czele else okoliczność,)


def _okoliczność(los: random.Random, tabela):
    """Okoliczność wyrażona rzeczą albo jednym słowem.

    Pora dnia wychodzi grupą gołą i mówi o tym ``_rola``,
    a przysłówek wypada tak często jak jeden wiersz tabeli,
    bo jest jedną z możliwości, a nie osobnym rejestrem rytmu.
    """
    if los.random() < 1 / (len(tabela) + 1):
        return Przysłówek(los.choice(PRZYSŁÓWKI))
    słowo, relacja, rzeczowniki = los.choice(tabela)
    pora = relacja == "czas"
    grupa = _grupa(los, rzeczowniki, goła=pora, cechy=() if pora else None)
    return Okolicznik(słowo, relacja, grupa)


def _czynność(los: random.Random, obsada: Obsada) -> Zdanie:
    """Ktoś albo coś zrobiło coś, czego nikomu nie robi: `Świeca zniknęła w izbie.`"""
    czyn, tabela = _bez_dopełnienia(los)
    return _zdarzenie(los, los.choice(obsada.wszyscy), czyn, *_okoliczności(los, tabela))


def _praca(los: random.Random, obsada: Obsada) -> Zdanie:
    """Ktoś zrobił coś rzeczy: `Kucharka zamknęła stary kufer.`"""
    return _zdarzenie(
        los,
        los.choice(obsada.wszyscy),
        los.choice(CZYNY_Z_BIERNIKIEM),
        _grupa(los, RZECZY),
        *_okoliczności(los, OKOLICZNOŚCI_CZYNNE),
    )


def _para(los: random.Random, obsada: Obsada) -> Zdanie:
    """Dwie rzeczy w jednej roli: `Kowal wyniósł dzban i wiadro.`

    Lematy są różne, bo `dzban i dzban` mówi o dwóch rzeczach jednym słowem,
    a koordynacja jest tu po to, żeby role dostały dwa człony, a nie dwie kopie.
    """
    jeden, drugi = _różne(los, RZECZY, 2)
    return _zdarzenie(
        los,
        los.choice(obsada.wszyscy),
        los.choice(CZYNY_Z_BIERNIKIEM),
        _rola(los, Rzecz(jeden)) & _rola(los, Rzecz(drugi)),
    )


def _przysługa(los: random.Random, obsada: Obsada) -> Zdanie:
    """Ktoś dał komuś rzecz: `Kowal sprzedał sąsiadowi stary dzban.`

    Dający i biorący są różnymi osobami, bo `Kowal oddał kowalowi klucz.`
    wypisuje jedną rzecz dwa razy w dwóch rolach, a nie mówi o dwóch ludziach.
    Biorący jest osobą, bo celownik tych czasowników nazywa tego,
    komu się rzecz daje, a `Kowal sprzedał dzbanowi klucz.` nie mówi nic.
    """
    kto, biorący = _różne(los, obsada.osoby, 2)
    return _zdarzenie(
        los,
        kto,
        los.choice(CZYNY_Z_CELOWNIKIEM),
        Komu(biorący),
        _grupa(los, RZECZY),
    )


def _ciąg(los: random.Random, obsada: Obsada) -> Zdanie:
    """Dwa zdarzenia jednym zdaniem, o tej samej rzeczy, więc z podmiotem raz.

    Podmiot wypada w tekście jeden, bo o tym rozstrzyga ``Ciąg``,
    a nie ten, kto zdarzenia losuje.
    """
    kto = los.choice(obsada.wszyscy)
    czyn, tabela = _bez_dopełnienia(los)
    return Ciąg(
        (
            _zdarzenie(los, kto, los.choice(CZYNY_Z_BIERNIKIEM), _grupa(los, RZECZY)),
            _zdarzenie(los, kto, czyn, *_okoliczności(los, tabela, wysuwalne=False)),
        )
    )


def _powód(los: random.Random, obsada: Obsada) -> Zdanie:
    """Zdarzenie wraz z drugim, które mówi, kiedy albo dlaczego.

    Wysunięcie na czoło pyta o leksykon, a nie o los:
    zdanie z ``więc`` na przodzie nie jest zdaniem o innym szyku,
    tylko zdaniem, którego polszczyzna nie ma.
    """
    słowo, relacja = los.choice(SPÓJNIKI_OKOLICZNOŚCI)
    kto, drugi = _różne(los, obsada.wszyscy, 2)
    czyn, tabela = _bez_dopełnienia(los)
    podrzędne = _zdarzenie(los, drugi, czyn, *_okoliczności(los, tabela, wysuwalne=False))
    okoliczność = Okolicznik(słowo, relacja, podrzędne)
    na_czele = okoliczność.wysuwalna and los.random() < CZOŁO
    return _zdarzenie(
        los,
        kto,
        los.choice(CZYNY_Z_BIERNIKIEM),
        _grupa(los, RZECZY),
        okoliczność.temat if na_czele else okoliczność,
    )


def _wola(los: random.Random, obsada: Obsada) -> Zdanie:
    """Osoba wraz z tym, co chciała zrobić: `Kowal nie chciał zejść do piwnicy.`

    Wykonawca jest tą samą ``Postać`` dwa razy, bo tyle sprawdza ``Robi``:
    bezokolicznik podmiotu nie ma i bierze go z czasownika nad sobą.
    """
    kto = los.choice(obsada.osoby)
    czyn, tabela = _bez_dopełnienia(los)
    return _zdarzenie(
        los,
        kto,
        los.choice(CZYNY_Z_BEZOKOLICZNIKIEM),
        zdarzenie(kto, czyn, *_okoliczności(los, tabela, wysuwalne=False)),
    )


def _sąd(los: random.Random, obsada: Obsada) -> Zdanie:
    """Zdarzenie, o którym osoba coś orzeka: `Kowal wiedział, że świeca zgasła.`

    Sądzący i ten, o kim on sądzi, są różni, bo `Córka pamiętała, że córka zasnęła.`
    wypisuje jedną rzecz dwa razy tam, gdzie polszczyzna opuszcza podmiot,
    a opuszczenia w zdaniu podrzędnym ``Kontekst.podrzędne`` nie przekazuje.
    """
    kto = los.choice(obsada.osoby)
    (drugi,) = _różne(los, [x for x in obsada.wszyscy if x is not kto], 1)
    czyn, tabela = _bez_dopełnienia(los)
    return _zdarzenie(
        los,
        kto,
        los.choice(CZYNY_ZE_ZDANIEM),
        Treść(_zdarzenie(los, drugi, czyn, *_okoliczności(los, tabela, wysuwalne=False))),
    )


def _wskazanie(los: random.Random, obsada: Obsada) -> Zdanie:
    """Rzecz wskazana zdarzeniem: `Praczka znalazła klucz, który zgubił kowal.`

    Wskazywana rzecz wchodzi do obu zdań jednym obiektem,
    bo o tym, które miejsce zostaje zaimkiem, rozstrzyga tożsamość, a nie znacznik.
    Podmioty obu zdań są różne, bo `nóż, który sąsiad podniósł` po sąsiedzie
    wypisuje go drugi raz, a wskazanie ma powiedzieć, o którą rzecz chodzi.
    """
    kto, drugi = _różne(los, obsada.wszyscy, 2)
    czyn, wskazujący = _różne(los, CZYNY_Z_BIERNIKIEM, 2)
    rzecz = Rzecz(los.choice(RZECZY))
    wskazujące = _zdarzenie(los, drugi, wskazujący, byt(rzecz))
    return _zdarzenie(los, kto, czyn, Opis(byt(rzecz), wskazujące))


@functools.cache
def _osoby_rodzaju(rodzaj: str) -> tuple[str, ...]:
    """Osoby, które niosą ten rodzaj, wzięte z SGJP, a nie z drugiej tabeli.

    Pyta o to orzecznik, bo `Córka była gospodarzem.` jest zdaniem poprawnym,
    które czyta się jak pomyłka losowania:
    zgodności rodzaju kopula nie żąda, a czytelnik jej oczekuje,
    bo o jednej osobie mówią tu dwa rzeczowniki naraz.
    """
    return tuple(lemat for lemat in OSOBY if rodzaj_rzeczownika(lemat) == rodzaj)


def _orzecznik(los: random.Random, obsada: Obsada) -> Zdanie:
    """Osoba wraz z tym, kim była: `Sąsiad był starym kowalem.`

    Orzecznik wychodzi w liczbie pojedynczej, bo podmiotem jest jedna osoba,
    a `Sąsiad był kowalami.` liczby nie zgadza z niczym.
    Orzecznikiem nie staje przy tym nikt z obsady, i to jest szerszy warunek
    niż sam podmiot: `Sąsiad był sąsiadem.` nie mówi nic,
    a `Mieszczanin był kowalem.` w akapicie, w którym kowal już chodzi,
    czyta się jak zdanie o dwóch postaciach, które są jedną.
    """
    kto = los.choice(obsada.osoby)
    wolne = (lemat for lemat in _osoby_rodzaju(kto.rodzaj) if lemat not in obsada.lematy)
    czym = tuple(wolne)
    zdanie = Jest(co=kto, czym=_grupa(los, czym, goła=True, cechy=CECHY_OSÓB))
    return nie(zdanie) if los.random() < PRZECZENIE else zdanie


#: Kształty zdań, z których losuje się akapit.
#: Każdy z nich jest innym drzewem, a nie innym zestawem słów w jednym drzewie,
#: bo makieta pokazuje rytm, a rytm niesie budowa zdania.
#: Lista jest przez to tym, czym jest rytm makiety:
#: kształt dopisany do niej zmienia tekst każdego ziarna, a nie tylko tego,
#: w którym wypadł.
KSZTAŁTY = (
    _czynność,
    _praca,
    _przysługa,
    _para,
    _ciąg,
    _powód,
    _wola,
    _sąd,
    _wskazanie,
    _orzecznik,
)


def main(argv: Sequence[str] | None = None) -> int:
    """Wydruk makiety wraz z ziarnem, którym da się ją wywołać drugi raz.

    Ziarno idzie na wyjście błędów, a tekst na wyjście zwykłe,
    bo makietę się przekierowuje do pliku, a ziarno się czyta.
    """
    parser = argparse.ArgumentParser(description="Tekst do makiety, po polsku, z drzew.")
    parser.add_argument("--ziarno", type=int, help="ziarno losowania; bez niego losowe")
    parser.add_argument("--akapity", type=int, default=4, help="ile akapitów wypisać")
    argumenty = parser.parse_args(argv)
    ziarno = random.randrange(10**6) if argumenty.ziarno is None else argumenty.ziarno
    print(f"ziarno: {ziarno}", file=sys.stderr)
    print(losuj(ziarno, argumenty.akapity).kompiluj())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
