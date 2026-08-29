"""Sonda różnicowa: ile konstrukcja kupuje i ile kosztuje, liczone ruchem werdyktu.

Pytanie, które ta maszyneria obsługuje, jest jedno i stawia je każda sonda
osobno: ile zdań konstrukcja odbiera. Zdanie odrzucone przez wieloznaczność jest
droższe niż zdanie, którego gramatyka nie wyprowadza wcale, bo tamto czeka na
produkcję, a to na jej wycofanie, więc sumy z ``harness.pomiar`` na to nie
odpowiadają: przejście ``przyjęte → wieloznaczne`` jest ceną, przejście
``odrzucone → przyjęte`` zakupem, a jedno i drugie widać dopiero zdanie po
zdaniu.

Wariantem jest zwykle gramatyka olskiego z wyjętą grupą produkcji
(:class:`Zdejmowanie`),
bo tak mierzy się konstrukcję, którą olski już ma,
a wariantów jest tyle, ile grup da się zdjąć osobno,
bo cena każdej z nich jest osobną liczbą.
Konstrukcja dopisana mierzyłaby produkcję napisaną w sondzie,
czyli drugą deklarację tego samego,
i rozeszłaby się z olskim po pierwszej zmianie, której nikt by tu nie powtórzył.

Pozycji, której olski nie ma, tak zmierzyć nie sposób,
a wyceny przed wpuszczeniem żąda ona tak samo,
więc gramatykę wariantu składa sonda i wolno jej złożyć każdą.
Ostrzeżenia wyżej pilnuje wtedy sesja:
gramatyka wariantu ma wychodzić z produkcji olskiego przepisanych,
a nie z pozycji napisanej drugi raz.

:class:`Sonda` mówi, jaką gramatykę mierzy każdy jej wariant,
a przebieg, tabelę przejść i konkurencję grup dostaje z tego pliku;
wiersz poleceń przychodzi z ``harness/komenda.py``,
wspólny także sondom, które różnicowe nie są.
"""

from __future__ import annotations

import argparse
import collections
import functools
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

from harness.corpus import Sentence, read
from harness.komenda import Komenda, nagłówek, uruchom
from harness.pomiar import SOURCES, Outcome, po_kawałkach, segments_for
from olski.grammar import Grammar, Production, Sym, Word
from olski.morph import Segment
from olski.parse import ciało_koordynuje, parse
from olski.segmentacja import morphology, sentences
from olski.subset import SPÓJNIKOWE, build
from olski.werdykt import Verdict, werdykt

#: Ile zdań zachować pod każdym przejściem. Przejście bez przykładu jest liczbą,
#: o której nie wiadomo, co ją wywołało, a cena jest tu tym, co trzeba przeczytać.
PRZYKŁADY = 8

#: Werdykty w kolejności, w jakiej stoją w tabeli.
STANY = ("valid", "ambiguous", "rejected")

#: Czym zaczyna się klucz przykładów trzymanych pod rolą, a nie pod przejściem.
#: Napisem, a nie drugim słownikiem, bo obie rodziny przykładów wchodzą do
#: jednego budżetu :attr:`Raport.ile_przykładów`, scalają się jednym :func:`scal`
#: i wychodzą jednym wydrukiem.
ROLA = "rola:"

#: Rola, pod którą przykładów nie trzymamy, bo zdanie przeczytane tak jak w banku
#: drzew nie jest tym, co z tej tabeli trzeba przeczytać. Wartość wydaje
#: ``Outcome.agreement`` i tyle o niej wie ten plik.
ZGODNE = "agrees"

#: Nazwy obu morfologii w nagłówku wydruku, bo nagłówek stoi po polsku.
#: Kluczem jest nazwa źródła z ``harness/pomiar.py``, żeby źródło dopisane tam
#: zgłosiło się tutaj brakiem nazwy, a nie wydrukiem, który milczy o tym,
#: co mierzył.
MORFOLOGIA = {"gold": "złota", "live": "żywa"}


@dataclass(frozen=True)
class Sonda:
    """Co jedna sonda różnicowa mówi o sobie wspólnemu przebiegowi.

    Warianty stoją w kolejności wydruku. Pierwszy jest mianownikiem, wobec
    którego liczone są przejścia, a ostatni ma wyprowadzać najwięcej, bo na nim
    stoi pomijanie zbędnych rozbiorów (:func:`_bez_zbędnych`). Sonda zdejmująca
    grupy ma tam samego olskiego, bo grupy nie zdejmuje żadnej, po jednym
    wariancie na grupę między nim a mianownikiem, i na nim jednym widać
    konkurencję grup (:attr:`pytania`); sonda wyceniająca pozycję, której olski
    nie ma, stawia ją za olskim, a zawężenie przed nim.
    """

    #: Nazwa modułu, czyli ``harness.płaski``. Wiersz poleceń robi z niej i pomoc,
    #: i prefiks komunikatu o brakującej ścieżce (``harness/komenda.py``).
    nazwa: str
    #: O co ta sonda pyta, jednym zdaniem, do wydruku pomocy.
    opis: str
    #: Nazwy wariantów, one zaś są etykietami wiersza w tabeli, więc stoją tu
    #: pełnym napisem: `bez przecinka`, a nie `bez`.
    warianty: tuple[str, ...]
    #: Gramatyka, którą ten wariant mierzy. Sonda zdejmująca grupy składa ją
    #: :class:`Zdejmowanie`, a sonda wyceniająca pozycję, której olski nie ma —
    #: cechę dopisaną do produkcji albo samą produkcję — po swojemu, bo grupą
    #: nie jest ani jedna, ani druga. Bez tego pola sesja przepisywałaby sobie
    #: cały przebieg obok tego pliku, żeby zmierzyć jedno wpuszczenie.
    gramatyki: Callable[[str], Grammar]
    #: Dwa pytania o konkurencję grup, w kolejności wydruku, każde całym zdaniem.
    #: Całym, a nie rzeczownikiem do wstawienia w gotowy wzór: wzór żądałby od
    #: każdej sondy formy fleksyjnej, a nagłówek nad tymi dwoma wierszami nazwy
    #: grupy nie potrzebuje, bo one same ją noszą.
    #: Konkurencja ma dwa stopnie. Zdanie, które rusza się pod jedną grupą i pod
    #: drugą, jest zdaniem, o które grupy się spierają. Zdanie, o którym oba
    #: warianty naraz mówią co innego, niż mówi którykolwiek z nich osobno, jest
    #: zdaniem, na którym ten spór coś kosztuje: dwie produkcje dały mu czytanie,
    #: którego żadna z nich nie dała.
    #: Puste, kiedy grupa jest jedna: nie ma wtedy z czym konkurować, a pomiar na
    #: jednej grupie jest tym, co pisze się w sesji najczęściej.
    pytania: tuple[str, ...] = ()

    @property
    def osobne(self) -> tuple[str, ...]:
        """Warianty zdejmujące po jednej grupie, czyli te między mianownikiem a całością."""
        return self.warianty[1:-1]

    @property
    def czysty(self) -> str:
        """Wariant, który jest dokładnie gramatyką olskiego, czyli ten, co nie zdejmuje nic.

        Nazwany, a nie brany numerem, bo pyta o niego także ``harness/płaski.py``,
        która nad tą gramatyką liczy drzewa, a nie werdykty; niezmiennik pilnuje
        ``tests/test_ruch.py``.
        """
        return self.warianty[-1]


def koordynuje(produkcja: Production) -> bool:
    """Czy ta produkcja koordynuje; kryterium trzyma ``ciało_koordynuje`` w ``olski/parse.py``.

    Pytają o to sondy, które zdejmują znak koordynacji, bo sam znak w ciele na to
    nie odpowiada: polszczyzna stawia przecinek i tam, gdzie nic się nie koordynuje,
    a zdjęta produkcja podrzędna zostawiłaby symbol bez ani jednego ciała,
    a gramatyka z symbolem nieokreślonym nie rozbiera niczego.
    """
    return ciało_koordynuje(
        produkcja.head,
        (część.name if isinstance(część, Sym) else None for część in produkcja.body),
    )


def ma_symbol(produkcja: Production, nazwa: str) -> bool:
    """Czy w ciele tej produkcji stoi ten symbol.

    Pytają o to sondy grupujące produkcje po tym, co produkcja bierze, a nie po
    tym, co definiuje. Pozycję konstrukcji stawia bowiem ciało, więc to ciało
    należy do grupy zdejmowanej, a symbol, który w nim stoi, zostaje.
    """
    return any(isinstance(część, Sym) and część.name == nazwa for część in produkcja.body)


def ze_spójnikiem(produkcja: Production) -> bool:
    """Czy w ciele tej produkcji stoi spójnik (:data:`SPÓJNIKOWE`).

    Rozdziela to dwa znaki koordynacji, które polszczyzna stawia przed zdaniem
    składowym, a sondy mierzą osobno: sam przecinek i przecinek przed spójnikiem.
    """
    return any(isinstance(część, Word) and część.pos & SPÓJNIKOWE for część in produkcja.body)


@functools.cache
def gramatyka(sonda: Sonda, wariant: str) -> Grammar:
    """Gramatyka, którą ten wariant mierzy; składa ją sama sonda.

    Nazwę wariantu sprawdzamy tutaj, bo literówka w niej daje inaczej gramatykę
    cudzego wariantu, i budujemy raz na proces roboczy, bo budowa jest droższa
    niż rozbiór jednego zdania, a gramatyka po zbudowaniu się nie zmienia.
    """
    if wariant not in sonda.warianty:
        raise ValueError(f"{sonda.nazwa}: nieznany wariant: {wariant}")
    return sonda.gramatyki(wariant)


@dataclass(frozen=True)
class Zdejmowanie:
    """Gramatyka wariantu składana zdejmowaniem grup produkcji, po nazwie wariantu.

    :attr:`grupa` odpowiada, do której grupy należy produkcja, a ``None`` znaczy,
    że do żadnej i że zostaje w każdym wariancie. Wariant ostatni dostaje
    wszystkie, czyli jest dokładnie olskim, i tego pilnuje ``tests/test_ruch.py``.

    Klasą, a nie funkcją zwracającą domknięcie, bo :func:`przebieg` posyła sondę
    do procesu roboczego, a domknięcia posłać nie sposób. Pilnuje tego
    ``tests/test_ruch.py``, bo w jednym procesie sonda z domknięciem liczy to samo
    i o tej granicy nie mówi.
    """

    grupa: Callable[[Production], str | None]
    #: Krotką, a nie listą, bo :func:`gramatyka` haszuje sondę wraz z tym polem.
    warianty: tuple[str, ...]

    def __call__(self, wariant: str) -> Grammar:
        """Produkcje przepisane ze świeżej gramatyki, takie jakie są.

        Złożona drugi raz z części gubiłaby głowę (``Grammar.dopisz``).
        """
        pełna = build()
        okrojona = Grammar(start=pełna.start)
        for produkcja in pełna.productions:
            należy = self.grupa(produkcja)
            if należy is not None and wariant != self.warianty[-1] and należy != wariant:
                continue
            okrojona.dopisz(produkcja)
        return okrojona


@dataclass
class Raport:
    """Liczniki jednego przebiegu, wraz ze zdaniami, które je czynią czytelnymi."""

    sonda: Sonda
    #: Ile zdań zachować pod każdym przejściem. Stoi przy licznikach, a nie przy
    #: każdym wołaniu, bo jest tym samym przez cały przebieg i przy scalaniu.
    ile_przykładów: int = PRZYKŁADY
    #: Wariant → ile zdań wyszło którym werdyktem.
    stany: dict[str, collections.Counter] = field(default_factory=dict)
    #: Wariant → ile zdań przeszło z którego werdyktu na który.
    przejścia: dict[str, collections.Counter] = field(default_factory=dict)
    #: (wariant, przejście) → zdania, na których to przejście widać.
    przykłady: dict[tuple[str, str], list[str]] = field(default_factory=dict)
    #: Wariant → jak role zdań nowo przyjętych mają się do drzewa wzorcowego.
    #: Zdanie przyjęte odwrotnie niż w banku drzew nie jest zakupem.
    zgodność: dict[str, collections.Counter] = field(default_factory=dict)
    #: Czy grupy produkcji wchodzą sobie w drogę; co to znaczy, mówi
    #: :attr:`Sonda.pytania`.
    konkurencja: collections.Counter = field(default_factory=collections.Counter)
    #: Zdania, których nie zmierzono, po powodzie. Wypisane, a nie odjęte po
    #: cichu, bo mianownik bez nich byłby mianownikiem zdań łatwych.
    pominięte: collections.Counter = field(default_factory=collections.Counter)

    @property
    def zmierzone(self) -> int:
        return sum(self.stany.get(self.sonda.warianty[0], collections.Counter()).values())

    def zapisz(
        self,
        tekst: str,
        stany: dict[str, str],
        role: dict[str, str | None],
    ) -> None:
        """Zapisz jedno zdanie: werdykt pod każdym wariantem i role pod nowo przyjętym.

        Werdykt jest tu napisem, a nie wynikiem rozbioru, bo zdanie przychodzi z
        dwóch korpusów naraz: z banku drzew, gdzie niesie drzewo wzorcowe, i z
        prozy, gdzie nie niesie żadnego. Role przychodzą więc obok werdyktu i nad
        prozą stoją puste, zamiast rozdwajać ten licznik na dwa.
        """
        mianownik = stany[self.sonda.warianty[0]]
        for wariant, stan in stany.items():
            self.stany.setdefault(wariant, collections.Counter())[stan] += 1
            if wariant == self.sonda.warianty[0] or stan == mianownik:
                continue
            przejście = f"{mianownik} → {stan}"
            self.przejścia.setdefault(wariant, collections.Counter())[przejście] += 1
            self.zanotuj((wariant, przejście), tekst)
            if stan == "valid" and wariant in role:
                zgoda = role[wariant] or "brak roli"
                self.zgodność.setdefault(wariant, collections.Counter())[zgoda] += 1
                #  Przejście, pod którym takie zdanie stoi, trzyma je razem z
                #  kilkudziesięcioma zgodnymi, więc pod rolą stoi drugi raz.
                if zgoda != ZGODNE:
                    self.zanotuj((wariant, f"{ROLA} {zgoda}"), tekst)
        self._konkurencja(tekst, stany, mianownik)

    def _konkurencja(self, tekst: str, stany: dict[str, str], mianownik: str) -> None:
        ruszone = {
            wariant: stany[wariant]
            for wariant in self.sonda.osobne
            if stany[wariant] != mianownik
        }
        if len(self.sonda.pytania) < 2:
            return
        if len(ruszone) >= 2:
            self._policz(self.sonda.pytania[0], tekst)
        if stany[self.sonda.warianty[-1]] not in {mianownik, *ruszone.values()}:
            self._policz(self.sonda.pytania[1], tekst)

    def _policz(self, nazwa: str, tekst: str) -> None:
        self.konkurencja[nazwa] += 1
        self.zanotuj(("konkurencja", nazwa), tekst)

    def zanotuj(self, klucz: tuple[str, str], tekst: str) -> None:
        """Zachowaj zdanie pod kluczem, dopóki mieści się w budżecie przykładów."""
        zachowane = self.przykłady.setdefault(klucz, [])
        if len(zachowane) < self.ile_przykładów:
            zachowane.append(tekst)


#: Wynik jednego wariantu: :class:`Outcome` nad bankiem drzew, :class:`Verdict`
#: nad prozą. Pomijaniu zbędnych rozbiorów te dwa nie różnią się niczym, bo czyta
#: ono jedno pole, które oba niosą; wypisane są z nazwy, żeby trzeci zgłosił się
#: tutaj, a nie w wydruku, który milczy o tym, co pominął.
Wynik = TypeVar("Wynik", Outcome, Verdict)


def _bez_zbędnych(sonda: Sonda, wynik: Callable[[str], Wynik]) -> dict[str, Wynik]:
    """Wynik każdego wariantu, bez rozbiorów, których odpowiedź jest już znana.

    Wariant ostatni wyprowadza najwięcej, a każdy inny wyprowadza podzbiór tego,
    co on, więc zdanie odrzucone przez niego jest odrzucone pod wszystkimi.
    Jego rozbiór idzie przez to pierwszy, a odrzucenie zamyka pozostałe warianty
    jedną odpowiedzią, bo o zdaniu odrzuconym mówią one to samo.
    Olski odrzuca większość zdań banku drzew, co drukuje ``harness.pomiar``,
    więc z przebiegu wypada przeszło połowa rozbiorów.

    Kolejność tę deklaruje sonda i odpowiada za nią sama (:class:`Sonda`):
    wariant rozszerzający postawiony przed ostatnim dostałby wiersz o zdaniach,
    których nikt nie rozebrał, a wydruk milczałby o tym.
    U sondy zdejmującej grupy wariantem ostatnim jest sam olski
    i tego pilnuje ``tests/test_ruch.py``.

    Pytanie to jest jedno dla obu korpusów, więc i odpowiedź stoi tu jedna: bank
    drzew i proza różnią się tym, co wariant nad zdaniem wydaje, a nie tym, które
    rozbiory są zbędne.
    """
    czysty = wynik(sonda.czysty)
    if czysty.result.rejected:
        return dict.fromkeys(sonda.warianty, czysty)
    wyniki = {wariant: wynik(wariant) for wariant in sonda.warianty[:-1]}
    wyniki[sonda.czysty] = czysty
    return wyniki


def _warianty(
    sonda: Sonda,
    zdanie: Sentence,
    segmenty: list[Segment],
    comparable: bool,
) -> dict[str, Outcome]:
    """Wynik każdego wariantu nad jednym zdaniem banku drzew."""

    def wynik(wariant: str) -> Outcome:
        return Outcome(
            sentence=zdanie,
            result=parse(gramatyka(sonda, wariant), segmenty, zatrzymanie=False),
            segments=tuple(segmenty),
            comparable=comparable,
        )

    return _bez_zbędnych(sonda, wynik)


def _werdykty(sonda: Sonda, zdanie: str, segmenty: list[Segment]) -> dict[str, Verdict]:
    """Werdykt każdego wariantu nad jednym zdaniem prozy."""

    def wynik(wariant: str) -> Verdict:
        return werdykt(zdanie, segmenty, gramatyka(sonda, wariant))

    return _bez_zbędnych(sonda, wynik)


def zmierz(
    sonda: Sonda,
    zdania: Iterable[Sentence],
    przykłady: int = PRZYKŁADY,
    źródło: str = "gold",
) -> Raport:
    """Przepuść zdania banku drzew przez każdy wariant i policz, co się rusza.

    Populacja jest ta sama, co w ``harness.pomiar.measure``: każde zdanie z
    drzewem wzorcowym, bez granicy na długość.

    Morfologia jest dwojaka i konstrukcja bywa taka, że pod jedną z nich nie
    kosztuje nic. Anotator wybrał w banku drzew jedno czytanie na token, więc
    konstrukcja konkurująca z czytaniem, którego on nie wybrał, wychodzi pod złotą
    morfologią darmowa, a płaci dopiero tam, gdzie czytania są wszystkie —
    czyli w tekście, który olski dostaje do sprawdzenia.
    Ról pod żywą morfologią nie porównujemy, bo rozpiętości nie są wtedy
    rozpiętościami drzewa wzorcowego (``Outcome.comparable``),
    i tym ten przebieg jest podobny do przebiegu nad prozą niżej.
    """
    raport = Raport(sonda, przykłady)
    for zdanie in zdania:
        if not zdanie.annotated:
            continue
        segmenty = segments_for(zdanie, źródło)
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        wyniki = _warianty(sonda, zdanie, segmenty, comparable=źródło == "gold")
        raport.zapisz(
            zdanie.text,
            {wariant: wynik.status for wariant, wynik in wyniki.items()},
            {wariant: wynik.agreement for wariant, wynik in wyniki.items()}
            if źródło == "gold"
            else {},
        )
    return raport


def nad_prozą(sonda: Sonda, tekst: str, przykłady: int = PRZYKŁADY) -> Raport:
    """To samo porównanie nad prozą, którą olski ma czytać.

    Bank drzew rankinguje konstrukcje w rejestrze, którego olski nie ma, i mówi
    przez to, ile konstrukcja kupuje w cudzej polszczyźnie. Drugie pytanie jest o
    rejestr własny i pada tu. Ról nie ma czym porównać, bo drzewa wzorcowego
    proza nie niesie, a fragment nie jest zdaniem i do mianownika nie wchodzi.

    Zdanie idzie tu przez warianty, a nie wariant przez cały tekst, bo segmenty
    zależą od napisu, a nie od gramatyki (``werdykt`` w ``olski/werdykt.py``):
    inaczej ten sam tekst segmentuje się tyle razy, ile jest wariantów, i tyle
    samo razy rozbiera się zdanie, które olski odrzucił.
    """
    raport = Raport(sonda, przykłady)
    for zdanie in sentences(tekst):
        werdykty = _werdykty(sonda, zdanie, morphology(zdanie))
        pierwszy = werdykty[sonda.warianty[0]]
        if not pierwszy.punktowane:
            raport.pominięte["fragment, a nie zdanie"] += 1
            continue
        raport.zapisz(
            pierwszy.text,
            {wariant: wynik.status for wariant, wynik in werdykty.items()},
            {},
        )
    return raport


def _kawałek(ścieżki: Sequence[Path], sonda: Sonda, przykłady: int, źródło: str):
    return zmierz(sonda, (read(ścieżka) for ścieżka in ścieżki), przykłady, źródło)


def przebieg(
    sonda: Sonda,
    ścieżki: Sequence[Path],
    jobs: int,
    przykłady: int = PRZYKŁADY,
    źródło: str = "gold",
) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport.

    Podział na kawałki jest ten sam, którym idzie ``harness.pomiar``, i stoi tam,
    bo decyzja o jego rozmiarze jest jedna. Składanie zostaje tutaj, bo licznik,
    który z kawałka wraca, jest licznikiem sondy.
    """
    praca = functools.partial(_kawałek, sonda=sonda, przykłady=przykłady, źródło=źródło)
    return scal(sonda, po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(sonda: Sonda, raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden.

    Kawałki są odcinkami jednej posortowanej listy plików i wchodzą tu w jej
    kolejności, więc scalony raport jest tym samym raportem, co z jednego
    przebiegu nad całością, przykłady włącznie.
    """
    scalony = Raport(sonda, przykłady)
    for raport in raporty:
        for wariant, licznik in raport.stany.items():
            scalony.stany.setdefault(wariant, collections.Counter()).update(licznik)
        for wariant, licznik in raport.przejścia.items():
            scalony.przejścia.setdefault(wariant, collections.Counter()).update(licznik)
        for wariant, licznik in raport.zgodność.items():
            scalony.zgodność.setdefault(wariant, collections.Counter()).update(licznik)
        scalony.konkurencja.update(raport.konkurencja)
        scalony.pominięte.update(raport.pominięte)
        for klucz, zachowane in raport.przykłady.items():
            for tekst in zachowane:
                scalony.zanotuj(klucz, tekst)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(raport: Raport, nagłówek: str) -> str:
    """Tabela werdyktów, a przed nią to, ile produkcji ma każdy wariant.

    Kolumna produkcji stoi tu z tego samego powodu, dla którego stoi w
    ``harness/luka.py``: wariant, który nie zdjął ani jednej produkcji, drukuje
    tabelę bez ani jednego przejścia, czyli wydruk nie do rozróżnienia od
    konstrukcji, która nic nie kosztuje. Sonda pisana pod jedną decyzję dostaje
    nazwy wariantów ręką, więc pomylić je z nazwą grupy jest łatwo.
    """
    sonda = raport.sonda
    szerokość = max(len("wariant"), *(len(wariant) for wariant in sonda.warianty))
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań",
        "",
        f"{'wariant':>{szerokość}}  {'produkcji':>9} {'przyjęte':>10}"
        f" {'wieloznaczne':>13} {'odrzucone':>10}",
    ]
    for wariant in sonda.warianty:
        licznik = raport.stany.get(wariant, collections.Counter())
        przyjęte, wieloznaczne, odrzucone = (licznik.get(stan, 0) for stan in STANY)
        wiersze.append(
            f"{wariant:>{szerokość}}  {len(gramatyka(sonda, wariant).productions):>9}"
            f" {przyjęte:>10} {wieloznaczne:>13} {odrzucone:>10}"
        )
    for powód, ile in raport.pominięte.most_common():
        wiersze.append(f"{ile:>7}          niezmierzone: {powód}")

    for wariant in sonda.warianty[1:]:
        przejścia = raport.przejścia.get(wariant)
        wiersze += ["", f"ruch wobec wariantu „{sonda.warianty[0]}” — {wariant}:"]
        if not przejścia:
            wiersze.append("  żadne zdanie nie zmieniło werdyktu")
            continue
        for przejście, ile in przejścia.most_common():
            wiersze.append(f"  {ile:>7}  {przejście}")
        zgodność = raport.zgodność.get(wariant)
        if zgodność:
            wiersze.append("  role zdań nowo przyjętych wobec drzewa wzorcowego:")
            for nazwa, ile in zgodność.most_common():
                wiersze.append(f"  {ile:>7}    {nazwa}")
                for tekst in raport.przykłady.get((wariant, f"{ROLA} {nazwa}"), []):
                    wiersze.append(f"             {tekst}")

    # Zero wypisane, a nie pominięte: liczba, której nie ma, czyta się jak
    # pomiar, którego nie było, a to jest ta liczba, po którą sonda stoi.
    wiersze += ["", "konkurencja, nad zdaniem po zdaniu:"]
    for nazwa in sonda.pytania:
        wiersze.append(f"  {raport.konkurencja.get(nazwa, 0):>7}  {nazwa}")

    for nazwa in sonda.pytania:
        zachowane = raport.przykłady.get(("konkurencja", nazwa), [])
        if zachowane:
            wiersze += ["", f"konkurencja, {nazwa}:"]
            wiersze += [f"  {tekst}" for tekst in zachowane]

    for wariant in sonda.warianty[1:]:
        for przejście, _ in raport.przejścia.get(wariant, collections.Counter()).most_common():
            zachowane = raport.przykłady.get((wariant, przejście), [])
            if not zachowane:
                continue
            wiersze += ["", f"{wariant}, {przejście}:"]
            wiersze += [f"  {tekst}" for tekst in zachowane]

    return "\n".join(wiersze)


def _morfologia(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--morfologia",
        choices=SOURCES,
        default="gold",
        help="czytania banku drzew: wybrane przez anotatora czy wszystkie, jakie ma Morfeusz",
    )


def _korpus(sonda: Sonda, ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    raport = przebieg(sonda, ścieżki, args.jobs, przykłady=args.przykłady, źródło=args.morfologia)
    return wydruk(raport, f"Składnica, morfologia {MORFOLOGIA[args.morfologia]}")


def _proza(sonda: Sonda, wejścia: Sequence[tuple[Path, str]], args: argparse.Namespace) -> str:
    raporty = (nad_prozą(sonda, tekst, args.przykłady) for _, tekst in wejścia)
    return wydruk(scal(sonda, raporty, args.przykłady), f"{nagłówek(wejścia)}, proza")


def main(sonda: Sonda, argv: Sequence[str] | None = None) -> int:
    """Puszcza sondę różnicową nad bankiem drzew albo nad plikiem prozy.

    Sonda pisana pod jedną decyzję woła to jednym wierszem,
    bo od sond wpisanych do drzewa różni się tym, co zdejmuje,
    a nie tym, o co pyta w wierszu poleceń (``CLAUDE.md#code``).
    """
    return uruchom(
        Komenda(
            nazwa=sonda.nazwa,
            opis=sonda.opis,
            przykłady=PRZYKŁADY,
            korpus=functools.partial(_korpus, sonda),
            proza=functools.partial(_proza, sonda),
            argumenty=_morfologia,
        ),
        argv,
    )
