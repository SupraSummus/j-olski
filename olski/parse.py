"""Parsing: every reading, not the first one.

The parser answers three questions, and the third is the one that matters most:

1. Does this sentence have a derivation at all? If not, it is not olski, and the
   furthest point reached says where the analysis died.
2. If it has exactly one, that is the reading, and the sentence means one thing.
3. If it has more than one, the sentence is ambiguous *in Polish*, and olski
   rejects it. ``Koszt samej szynki przewyższa koszt szynki z dodatkami`` parses
   two ways, because ``koszt`` is nominative or accusative and Polish permits
   both SVO and OVS, so the sentence does not say which cost is greater. A
   language whose sentences can be read two ways cannot be checked mechanically,
   and worse, cannot be read reliably by a person either.

Distinct readings, not derivations. Two derivations that describe the same
structure are one reading. The distinction is not pedantic: it is exactly the
mistake recorded in docs/glr-in-practice.md#ambiguity-as-a-confidence-measure,
where a system fell silent on lines it had understood perfectly because it
counted attempts instead of outcomes.

Implementation.
An Earley chart over the segmentation graph builds a forest with shared nodes:
one :class:`Pozycja` per constituent shape,
however many derivations stand under it,
so six undecided attachments are six positions rather than sixty-four trees.
Four summaries come off that forest and none of them needs another parser:
how many readings there are,
which of them a reader is shown,
which roles the readings disagree about,
and which attachment the sentence leaves open.
docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań
owns the argument for asking the forest rather than a list of trees,
and docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania
owns the two conditions such a forest has to meet
and the measurement behind the second.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from itertools import product

from olski.grammar import (
    EMPTY,
    Env,
    Grammar,
    Part,
    Production,
    Sym,
    Word,
    bierze,
    features_of,
    unify,
)
from olski.morph import Reading, Segment

#: Enumeration is capped,
#: because an ambiguous sentence can have very many readings
#: and the answer past the second one is always the same: too many.
#: The count itself is not capped, the forest giving it without walking the trees.
MAX_READINGS = 64

#: Cechy, z jakimi konstytuent wychodzi do rodzica, w postaci dającej się zahaszować.
#: Tyle o nim rodzic wie,
#: i dlatego tyle wystarczy, żeby liczyć czytania bez wyliczania ich.
Cechy = frozenset[tuple[str, frozenset[str]]]

#: Kształty jednej pozycji dzielą się na klasy po tym, z jakimi cechami wychodzą.
#: Klasą jest zbiór, a nie jedne cechy,
#: bo forma o kilku czytaniach daje jeden kształt i kilka sposobów, na jakie on przechodzi.
Klasa = frozenset[Cechy]


class Cykl(Exception):
    """Pozycja stoi sama pod sobą, więc czytań jest nieskończenie wiele."""


@dataclass(frozen=True)
class Pozycja:
    """Miejsce w tablicy: co się wyprowadza i skąd dokąd.

    Pakowanie polega na tym, że dwa wyprowadzenia jednego kształtu dostają jedną pozycję.
    Las rośnie wtedy z długością zdania, a nie z liczbą czytań.

    Etykieta i rozpiętość to dokładnie tyle, ile odróżnia jedno czytanie od drugiego,
    a :meth:`Node.signature` wywodzi dlaczego;
    pozycja o jeden składnik bogatsza liczyłaby wyprowadzenia zamiast czytań.
    Ile kosztuje rozdzielanie pozycji po cechach, mierzy
    docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania.

    Liść etykiety nie ma, bo czytaniem liścia jest sama rozpiętość:
    dwa czytania jednej formy są jednym liściem.
    """

    label: str | None
    span: tuple[int, int]

    @property
    def liść(self) -> bool:
        return self.label is None


@dataclass(frozen=True)
class Leaf:
    segment: Segment
    reading: Reading

    @property
    def span(self) -> tuple[int, int]:
        return (self.segment.start, self.segment.end)

    def signature(self):
        """Liść jest swoją rozpiętością i niczym więcej.

        Część mowy zeszła stąd rozmyślnie i nie ma tu wracać przez przeoczenie;
        co ją zdjęło, mówi :meth:`Node.signature`.
        """
        return self.span

    def forms(self) -> list[str]:
        return [self.segment.form]

    def forma_głowy(self) -> str:
        """Głową słowa jest ono samo, i tu schodzenie po głowach się kończy."""
        return self.segment.form


@dataclass(frozen=True)
class Node:
    label: str
    children: tuple[Leaf | Node, ...]
    #: Skąd dokąd węzeł sięga w grafie segmentów.
    #: Wpisana przy budowaniu,
    #: bo węzeł produkcji o pustym ciele nie ma dzieci, z których dałoby się ją wyliczyć,
    #: a stoi w miejscu, które zna parser.
    #: Takiej produkcji gramatyka olskiego nie ma,
    #: a żąda jej rozwinięcie szyku do warunków precedencji.
    span: tuple[int, int]
    #: Która z córek jest głową, wzięta z produkcji, która ten węzeł złożyła.
    #: Niesie ją węzeł, a nie odczytuje się jej z gramatyki,
    #: bo streszczenie czytania gramatyki nie dostaje,
    #: a węzeł powstaje tam, gdzie produkcja jest pod ręką.
    głowa: int

    def signature(self):
        """Co czyni dwa czytania jednym czytaniem.

        Czytanie jest swoim kształtem i niczym więcej: role stoją w etykietach
        węzłów, przyłączenie w rozpiętościach, a wszystko, o co olski pyta, jest
        pytaniem o drzewo. Wyłączone rozmyślnie: wartości cech, bo zgodność
        wymusiła już unifikacja; lematy, bo polskie formy są homonimiczne
        wszędzie i liczone jako dwa odrzuciłyby prawie całą polszczyznę; części
        mowy, bo tam, gdzie zmieniają strukturę, różni wyprowadzenia już
        kształt — ``do`` jako przyimek i jako nuta dalej są dwoma czytaniami.

        Ostatnią z tych trzech wywodzi docs/subset.md: co ją zdjęło, ile to
        kupuje nad bankiem drzew i czego było warunkiem.

        Pozycja lasu niesie dokładnie ten kształt,
        więc dwa drzewa wyliczone z lasu mają dwie różne sygnatury
        i nie ma tu czego odsiewać.
        """
        return (self.label, tuple(child.signature() for child in self.children))

    def forms(self) -> list[str]:
        return [form for child in self.children for form in child.forms()]

    def forma_głowy(self) -> str:
        """Forma głowy tego konstytuenta: jedno słowo, którym się go nazywa.

        Schodzi po głowach aż do liścia,
        bo głową grupy jest słowo, a nie podgrupa:
        gospodarzem przyłączenia jest ``koszt``, a nie ``koszt szynki``.
        """
        return self.children[self.głowa].forma_głowy()

    def find(self, label: str) -> list[Node]:
        """Every node with this label, this one included, outermost first."""
        found = [self] if self.label == label else []
        for child in self.children:
            if isinstance(child, Node):
                found.extend(child.find(label))
        return found


Tree = Leaf | Node


@dataclass(frozen=True)
class Przyłączenie:
    """Modyfikator, którego przyłączenie zostaje nierozstrzygnięte, i jego gospodarze.

    Werdykt nad zdaniem o kilku takich przyłączeniach ma powiedzieć autorowi, co poprawić,
    a lista czytań mówi to iloczynem:
    sześć niezależnych wyborów wychodzi z niej sześćdziesięcioma czterema wierszami.
    Stąd ta postać, czyli jeden wpis na wybór:
    wpisów jest tyle, ile decyzji, a nie ile czytań.
    """

    #: Formy modyfikatora, czyli to, co autor ma przestawić.
    modyfikator: str
    #: Konstytuenty, do których modyfikator w czytaniach dochodzi,
    #: nazwane swoją głową i ustawione tak jak w zdaniu.
    gospodarze: tuple[str, ...]


@dataclass(frozen=True)
class Deklaracja:
    """Co gramatyka mówi o sobie podsumowaniom werdyktu.

    Które symbole są rolami i gdzie szukać przyłączenia, wie gramatyka, a nie rozbiór,
    więc :func:`parse` i :func:`describe` biorą to jedną wartością:
    podsumowanie następne dokłada tutaj pole i nie rusza żadnej z dwóch sygnatur.
    Wypełnia ją gramatyka, a typ definiuje rozbiór:
    żądają go te dwie funkcje i nikt poza nimi,
    a formalizm z ``olski/grammar.py`` niesie produkcje i o werdykcie nic nie wie.
    """

    #: Role, którymi streszcza się czytanie i o które czytania mogą się różnić.
    role: tuple[str, ...]
    #: Ta z ról, która się przyłącza,
    #: czyli ta, przy której streszczenie nazywa jeszcze gospodarza.
    przyłączany: str
    #: Symbole konstytuentów, w których produkcjach to przyłączenie stoi.
    gospodarze: tuple[str, ...]


@dataclass
class Result:
    """What the parser concluded about one sentence."""

    #: Ile czytań zdanie ma, policzone po lesie i bez granicy, jakiej podlega
    #: :attr:`readings`.
    #: Liczba jest osobno od listy,
    #: bo werdykt nad zdaniem o sześciu nierozstrzygniętych przyłączeniach
    #: jest liczbą, której nikt nie chce zobaczyć wypisanej drzewo po drzewie.
    ile: int = 0
    readings: list[Node] = field(default_factory=list)
    #: The furthest graph node any partial analysis reached, which is where a
    #: rejected sentence stopped making sense.
    furthest: int = 0
    #: Czy wyliczanie stanęło na :data:`MAX_READINGS`,
    #: czyli czy lista czytań jest krótsza niż :attr:`ile`.
    truncated: bool = False
    #: Role, o które czytania się różnią, o ile :func:`parse` dostał :class:`Deklaracja`.
    #: Wzięte z lasu, a nie ze streszczeń, których jest najwyżej :data:`MAX_READINGS`;
    #: dlaczego, mówi :meth:`Las.różniące`.
    różniące: tuple[str, ...] = ()
    #: Przyłączenia, których czytania nie rozstrzygają,
    #: z tej samej deklaracji co :attr:`różniące`.
    #: Wpisane tu, a nie odpytywane z lasu:
    #: las jednego zdania waży tyle, ile jego tablica,
    #: a werdyktów trzyma się naraz tyle, ile dokument ma zdań.
    przyłączenia: tuple[Przyłączenie, ...] = ()

    @property
    def valid(self) -> bool:
        return self.ile == 1

    @property
    def ambiguous(self) -> bool:
        return self.ile > 1

    @property
    def rejected(self) -> bool:
        return self.ile == 0

    @property
    def status(self) -> str:
        """Which of the three the sentence is, as the verdict a reader is shown."""
        if self.valid:
            return "valid"
        return "ambiguous" if self.ambiguous else "rejected"


def las(grammar: Grammar, segments: list[Segment], start: str | None = None) -> Las:
    """Las tego zdania, do chodzenia po nim.

    Wywołuje ją pomiar.
    Werdykt woła :func:`parse`, która wyciąga z lasu podsumowania i las porzuca,
    bo dokument trzyma tyle werdyktów, ile ma zdań,
    a jeden las waży tyle, ile jego tablica.
    """
    return Las(_Tablica(grammar, segments, start or grammar.start))


def parse(
    grammar: Grammar,
    segments: list[Segment],
    start: str | None = None,
    deklaracja: Deklaracja | None = None,
) -> Result:
    """Rozbierz zdanie i zapytaj las, ile czytań ma, które pokazać i co zostawia otwarte.

    Bez deklaracji werdykt jest samą liczbą i listą czytań;
    co ona niesie i czemu jest jedna, mówi :class:`Deklaracja`.
    """
    zbudowany = las(grammar, segments, start)
    ile = zbudowany.ile_czytań()
    readings: list[Node] = []
    for tree in zbudowany.czytania():
        readings.append(tree)
        if len(readings) >= MAX_READINGS:
            break
    różniące, przyłączenia = (
        ((), ())
        if deklaracja is None
        else (
            zbudowany.różniące(deklaracja.role),
            tuple(zbudowany.przyłączenia(deklaracja.przyłączany, deklaracja.gospodarze)),
        )
    )
    return Result(
        ile,
        readings,
        zbudowany.najdalszy(),
        truncated=ile > len(readings),
        różniące=różniące,
        przyłączenia=przyłączenia,
    )


def _first(segments: Sequence[Segment]) -> int:
    return min((segment.start for segment in segments), default=0)


# --------------------------------------------------------------------------- #
# Tablica
# --------------------------------------------------------------------------- #

#: Stan tablicy: produkcja, ile jej ciała już przeszło, i pozycja grafu, w której się zaczęła.
#: Cech w tym nie ma rozmyślnie:
#: stan niosący środowisko cech rozdzieliłby pozycje
#: i policzyłby wyprowadzenia zamiast czytań.
#: Unifikacja przechodzi po tablicy osobno, w :meth:`Las.klasy`.
_Stan = tuple[Production, int, int]


class _Tablica:
    """Tablica Earleya nad grafem segmentów.

    Earley przyjmuje każdą gramatykę bezkontekstową,
    lewą rekursję i produkcję o pustym ciele włącznie,
    i oddaje las ze współdzielonymi węzłami sam z siebie, bez budowania automatu.
    Dla gramatyki, która się jeszcze zmienia, ten ostatni punkt jest całym argumentem
    (docs/design-notes.md#angle-one-parsing).

    Segmenty są krawędziami grafu, a nie listą, więc pozycją jest węzeł grafu:
    ``ktoś`` daje naraz jeden segment i trzy,
    a tablica nie musi wybierać między tymi podziałami przed rozbiorem.
    """

    def __init__(self, grammar: Grammar, segments: list[Segment], start: str) -> None:
        missing = grammar.undefined()
        if missing:
            raise ValueError(f"grammar refers to undefined symbols: {', '.join(sorted(missing))}")
        self.grammar = grammar
        self.segments = segments
        self.start = start
        self.krawędzie: dict[int, list[Segment]] = {}
        for segment in segments:
            self.krawędzie.setdefault(segment.start, []).append(segment)
        self.początek = _first(segments)
        self.koniec = max((segment.end for segment in segments), default=0)
        #: Pozycja grafu → stan → skąd stan tu doszedł,
        #: czyli para pozycji poprzedniej i córki, która je rozdzieliła.
        self.stany: dict[int, dict[_Stan, set[tuple[int, Pozycja]]]] = {}
        #: Pozycja grafu → symbol → stany, które na ten symbol tu czekają.
        self._oczekujące: dict[int, dict[str, list[_Stan]]] = {}
        #: Pozycja grafu → symbole, które się w niej zamknęły o zerowej rozpiętości.
        #: Bez tego produkcja o pustym ciele przepada dla stanu dopisanego po niej,
        #: bo ten nie ma już czego dokończyć.
        self._puste: dict[int, set[str]] = {}
        #: (produkcja, kropka, źródło, k) → ciała, jakie się w tym złożyły.
        self._ciała_memo: dict[tuple, set[tuple]] = {}
        #: Węzły grafu w kolejności rosnącej, bo krawędź nigdy nie idzie w tył.
        self.pozycje_grafu = sorted(
            {self.początek, self.koniec}
            | {segment.start for segment in segments}
            | {segment.end for segment in segments}
        )
        self._rozbierz()

    # -- budowanie ---------------------------------------------------------- #

    def _rozbierz(self) -> None:
        for production in self.grammar.for_head(self.start):
            self._dodaj(self.początek, (production, 0, self.początek), None)
        for k in self.pozycje_grafu:
            kolejka = list(self.stany.get(k, ()))
            i = 0
            while i < len(kolejka):
                production, kropka, źródło = kolejka[i]
                i += 1
                if kropka == len(production.body):
                    self._zamknij(k, production.head, źródło, kolejka)
                    continue
                część = production.body[kropka]
                if isinstance(część, Word):
                    self._wczytaj(k, (production, kropka, źródło), część)
                else:
                    self._przewiduj(k, (production, kropka, źródło), część, kolejka)

    def _dodaj(self, k: int, stan: _Stan, wstecz: tuple[int, Pozycja] | None) -> bool:
        """Wpisz stan i powiedz, czy jest nowy; wpis powtórzony dokłada samo wstecz."""
        w_pozycji = self.stany.setdefault(k, {})
        istniejące = w_pozycji.get(stan)
        if istniejące is None:
            w_pozycji[stan] = set() if wstecz is None else {wstecz}
            return True
        if wstecz is not None:
            istniejące.add(wstecz)
        return False

    def _przewiduj(self, k: int, stan: _Stan, część: Sym, kolejka: list[_Stan]) -> None:
        self._oczekujące.setdefault(k, {}).setdefault(część.name, []).append(stan)
        for production in self.grammar.for_head(część.name):
            if self._dodaj(k, (production, 0, k), None):
                kolejka.append((production, 0, k))
        if część.name in self._puste.get(k, ()):
            self._posuń(k, stan, k, Pozycja(część.name, (k, k)), kolejka)

    def _wczytaj(self, k: int, stan: _Stan, terminal: Word) -> None:
        """Przejdź krawędzią grafu, jeżeli terminal bierze którekolwiek jej czytanie.

        Pytanie pada z ``EMPTY``, a nie ze środowiskiem rodzeństwa,
        bo stan tablicy cech nie niesie.
        Zawężenie potrafi tylko odsiewać,
        więc na tym etapie tablica przyjmuje co najwyżej za dużo,
        a nadmiar odsiewa potem unifikacja po lesie.
        """
        production, kropka, źródło = stan
        for segment in self.krawędzie.get(k, ()):
            if not any(
                bierze(terminal, reading.tag.pos, reading.lemma, dict(reading.tag.features), EMPTY)
                is not None
                for reading in segment.readings
            ):
                continue
            self._dodaj(
                segment.end,
                (production, kropka + 1, źródło),
                (k, Pozycja(None, (k, segment.end))),
            )

    def _zamknij(self, k: int, symbol: str, źródło: int, kolejka: list[_Stan]) -> None:
        if źródło == k:
            self._puste.setdefault(k, set()).add(symbol)
        pozycja = Pozycja(symbol, (źródło, k))
        for stan in list(self._oczekujące.get(źródło, {}).get(symbol, ())):
            self._posuń(k, stan, źródło, pozycja, kolejka)

    def _posuń(
        self, k: int, stan: _Stan, j: int, dziecko: Pozycja, kolejka: list[_Stan]
    ) -> None:
        production, kropka, źródło = stan
        dalej = (production, kropka + 1, źródło)
        if self._dodaj(k, dalej, (j, dziecko)):
            kolejka.append(dalej)

    # -- czytanie ----------------------------------------------------------- #

    def zamknięte(self, production: Production, źródło: int, k: int) -> bool:
        """Czy ta produkcja doszła w tablicy do końca ciała na tej rozpiętości."""
        return (production, len(production.body), źródło) in self.stany.get(k, {})

    def ciała(self, production: Production, kropka: int, źródło: int, k: int) -> set[tuple]:
        """Ciała, jakimi ta produkcja doszła tutaj: krotki pozycji córek.

        Tablica pamięta same krawędzie wstecz, po jednej na córkę,
        więc ciało powstaje ze złożenia ich w łańcuch.
        Krotek jest tyle, na ile sposobów ta produkcja dzieli tu rozpiętość,
        czyli tyle, ile wyprowadzeń mieści jedna pozycja.
        """
        if kropka == 0:
            return {()} if źródło == k else set()
        klucz = (production, kropka, źródło, k)
        gotowe = self._ciała_memo.get(klucz)
        if gotowe is not None:
            return gotowe
        stan = (production, kropka, źródło)
        złożone: set[tuple] = set()
        for j, dziecko in self.stany.get(k, {}).get(stan, ()):
            for prefiks in self.ciała(production, kropka - 1, źródło, j):
                złożone.add((*prefiks, dziecko))
        self._ciała_memo[klucz] = złożone
        return złożone


# --------------------------------------------------------------------------- #
# Las
# --------------------------------------------------------------------------- #


class Las:
    """Las ze współdzielonymi węzłami i cztery podsumowania, jakie z niego wychodzą.

    Taki las odpowiada na pytanie olskiego pod dwoma warunkami.
    Jedną pozycję dostaje to, co jest jednym czytaniem,
    o czym rozstrzyga :class:`Pozycja`;
    liczba z jednej pozycji łączy się z liczbą z sąsiedniej tak, jak łączy je unifikacja,
    o czym rozstrzyga :meth:`klasy`.
    Wywód obu i pomiar, którym wybrano drugi, mieści
    docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania.
    """

    def __init__(self, tablica: _Tablica) -> None:
        self._tablica = tablica
        self.grammar = tablica.grammar
        self.korzeń = Pozycja(tablica.start, (tablica.początek, tablica.koniec))
        #: Rozpiętość → czytania form, jakie przez nią przechodzą,
        #: wraz z cechami gotowymi do unifikacji.
        #: Kluczem jest rozpiętość, a nie segment, bo czytaniem liścia jest sama rozpiętość.
        self._czytania_liścia: dict[
            tuple[int, int], list[tuple[Segment, Reading, dict[str, frozenset[str]]]]
        ] = {}
        for segment in tablica.segments:
            miejsce = self._czytania_liścia.setdefault((segment.start, segment.end), [])
            miejsce.extend(
                (segment, reading, dict(reading.tag.features)) for reading in segment.readings
            )
        self._wyprowadzenia: dict[Pozycja, dict[tuple[Pozycja, ...], tuple[Production, ...]]] = {}
        self._klasy: dict[Pozycja, dict[Klasa, int]] = {}
        #: (pozycja, klasa) → kombinacja klas córek → produkcja, którą przeszła.
        #: To jest las już po unifikacji:
        #: kombinacji, której ona nie przepuszcza, nie ma tu wcale,
        #: więc każda gałąź kończy się czytaniem.
        self._krawędzie: dict[tuple[Pozycja, Klasa], dict[tuple, Production]] = {}
        self._czynne: set[Pozycja] = set()
        self._żywe_pary: set[tuple[Pozycja, Klasa]] | None = None
        self._rodzice: dict[tuple[Pozycja, Klasa], set[tuple[Pozycja, Klasa]]] | None = None
        self._prefiksy: dict[tuple, frozenset[Env]] = {}
        #: (para, etykieta) → rozpiętości, jakie pierwszy węzeł tej etykiety pod nią bierze.
        self._pierwsze_role: dict[
            tuple[tuple[Pozycja, Klasa], str], frozenset[tuple[int, int] | None]
        ] = {}
        self._przedstawiciele: dict[Pozycja, Node] = {}
        self._najdalszy: int | None = None

    # -- tablica -------------------------------------------------------------#

    def wyprowadzenia(self, pozycja: Pozycja) -> dict[tuple[Pozycja, ...], tuple[Production, ...]]:
        """Wyprowadzenia pod tą pozycją: ciało → produkcje, które je złożyły.

        Kluczem jest ciało, a nie produkcja,
        bo o kształcie rozstrzygają etykiety i rozpiętości córek.
        Dwie produkcje o jednym ciele dają jedno czytanie i wchodzą tu razem;
        różni je dopiero to, co wypuszczają.

        Pytana o pozycję, której tablica nie domknęła, oddaje pusty słownik,
        więc jest to zarazem sposób zapytania lasu, czy taki konstytuent w ogóle powstał.
        """
        gotowe = self._wyprowadzenia.get(pozycja)
        if gotowe is not None:
            return gotowe
        znalezione: dict[tuple[Pozycja, ...], list[Production]] = {}
        if not pozycja.liść:
            źródło, k = pozycja.span
            for production in self.grammar.for_head(pozycja.label):
                if not self._tablica.zamknięte(production, źródło, k):
                    continue
                for ciało in self._tablica.ciała(production, len(production.body), źródło, k):
                    znalezione.setdefault(ciało, []).append(production)
        zebrane = {ciało: tuple(produkcje) for ciało, produkcje in znalezione.items()}
        self._wyprowadzenia[pozycja] = zebrane
        return zebrane

    # -- unifikacja po lesie ------------------------------------------------ #

    def klasy(self, pozycja: Pozycja) -> dict[Klasa, int]:
        """Ile kształtów stoi pod tą pozycją, w klasach po tym, co wypuszczają.

        Iloczyn liczy się tutaj po parach, które unifikacja przepuszcza,
        a nie po samych pozycjach:
        kombinacja klas córek, której żadna produkcja nie składa,
        nie wnosi ani jednego czytania.

        Klasą jest zbiór cech, a nie jedne cechy,
        bo jeden kształt przechodzi czasem na kilka sposobów:
        ``dla przyjemności`` jest jedną grupą przyimkową w dwóch liczbach.
        Rodzic widzi z córki tylko to, co ona wypuszcza,
        więc grupowanie po tym zbiorze pozwala liczyć kształty zamiast sposobów:
        dwa kształty o jednym zbiorze wpadają do jednej klasy i sumują się,
        a jeden kształt wpada do dokładnie jednej.
        """
        gotowe = self._klasy.get(pozycja)
        if gotowe is not None:
            return gotowe
        if pozycja in self._czynne:
            raise Cykl(
                f"{pozycja.label} na {pozycja.span} stoi samo pod sobą; "
                "czytań jest wtedy nieskończenie wiele"
            )
        self._czynne.add(pozycja)
        klasy: dict[Klasa, int] = {}
        try:
            for ciało, produkcje in self.wyprowadzenia(pozycja).items():
                listy = [
                    [(None, 1)] if dziecko.liść else list(self.klasy(dziecko).items())
                    for dziecko in ciało
                ]
                for kombinacja in product(*listy):
                    wybór = tuple(klasa for klasa, _ile in kombinacja)
                    wypuszczane: set[Cechy] = set()
                    przeszła = None
                    for production in produkcje:
                        cechy = self._przejdź(production, ciało, wybór)
                        if cechy:
                            wypuszczane |= cechy
                            przeszła = przeszła or production
                    if przeszła is None:
                        continue
                    klasa = frozenset(wypuszczane)
                    ile = math.prod(liczba for _klasa, liczba in kombinacja)
                    klasy[klasa] = klasy.get(klasa, 0) + ile
                    self._krawędzie.setdefault((pozycja, klasa), {}).setdefault(
                        tuple(zip(ciało, wybór, strict=True)), przeszła
                    )
        finally:
            self._czynne.discard(pozycja)
        self._klasy[pozycja] = klasy
        return klasy

    def _zawężenia(
        self, część: Part, dziecko: Pozycja, cechy: Iterable[Cechy], env: Env
    ) -> Iterator[Env]:
        """Na jakie środowiska ta córka zawęża to jedno; nic, gdy na żadne.

        Córka wchodzi tu samymi cechami, jakie wypuszcza, bo tyle o niej rodzic wie;
        liść wchodzi czytaniami, bo terminal sprawdza i część mowy, i lemat.

        Unifikacja dotyka lasu tylko w tym jednym miejscu,
        i dlatego to jedna metoda, a nie dwie:
        wołają ją i liczenie kształtów, i szukanie punktu, na którym odrzucenie stanęło.
        """
        if isinstance(część, Word):
            for _segment, reading, cechy_formy in self._czytania_liścia.get(dziecko.span, ()):
                złożone = bierze(część, reading.tag.pos, reading.lemma, cechy_formy, env)
                if złożone is not None:
                    yield złożone
            return
        for wypuszczone in cechy:
            złożone = unify(część.constraints, dict(wypuszczone), env)
            if złożone is not None:
                yield złożone

    def _dołóż(
        self,
        część: Part,
        dziecko: Pozycja,
        cechy: Iterable[Cechy],
        środowiska: Iterable[Env],
    ) -> set[Env]:
        """Środowiska po dołożeniu tej córki do tych, z jakimi ciało doszło przed nią."""
        cechy = list(cechy)
        return {
            złożone
            for env in środowiska
            for złożone in self._zawężenia(część, dziecko, cechy, env)
        }

    def _przejdź(
        self, production: Production, ciało: tuple[Pozycja, ...], wybór: tuple[Klasa | None, ...]
    ) -> set[Cechy]:
        """Cechy, z jakimi ta produkcja wychodzi nad tymi córkami; pusty zbiór, gdy z żadnymi.

        Środowisko przechodzi ciało od lewej, tak jak przechodzi je wyprowadzenie:
        zmienna wiązana przy pierwszej córce zawęża to, co wolno drugiej.
        """
        środowiska = {EMPTY}
        for część, dziecko, klasa in zip(production.body, ciało, wybór, strict=True):
            środowiska = self._dołóż(część, dziecko, klasa or (), środowiska)
            if not środowiska:
                return set()
        return {frozenset(features_of(production, env).items()) for env in środowiska}

    # -- podsumowania ------------------------------------------------------- #

    def ile_czytań(self) -> int:
        """Ile czytań ma zdanie: suma po klasach korzenia, bez wyliczania drzew."""
        return sum(self.klasy(self.korzeń).values())

    def najdalszy(self) -> int:
        """Dokąd doszła jakakolwiek analiza częściowa, czyli na czym odrzucenie stanęło.

        Liczy się przejście terminalem, bo bloker ma nazwać formę z tego miejsca zdania,
        a czym jest tu analiza częściowa, mówi :meth:`_przed_formą`.
        """
        if self._najdalszy is not None:
            return self._najdalszy
        if self.klasy(self.korzeń):
            # Czytanie sięga przez całe zdanie, więc dalej niż jego koniec nie ma gdzie.
            self._najdalszy = self._tablica.koniec
            return self._najdalszy
        najdalszy = self._tablica.początek
        for k, (production, kropka, źródło) in self._przed_formą():
            terminal = production.body[kropka]
            środowiska = self._prefiks(production, kropka, źródło, k)
            for segment in self._tablica.krawędzie.get(k, ()):
                if segment.end > najdalszy and self._przechodzi(
                    terminal, (k, segment.end), środowiska
                ):
                    najdalszy = segment.end
        self._najdalszy = najdalszy
        return najdalszy

    def _przechodzi(
        self, terminal: Word, rozpiętość: tuple[int, int], środowiska: Iterable[Env]
    ) -> bool:
        """Czy ten terminal przechodzi tę rozpiętość przy którymkolwiek z tych środowisk."""
        return any(
            bierze(terminal, reading.tag.pos, reading.lemma, cechy, env) is not None
            for env in środowiska
            for _segment, reading, cechy in self._czytania_liścia.get(rozpiętość, ())
        )

    def _przed_formą(self) -> Iterator[tuple[int, _Stan]]:
        """Analizy częściowe zatrzymane przed terminalem, pozycja po pozycji od lewej.

        Analizą częściową jest stan pod dwoma warunkami.
        Pierwszy: jego przebyte ciało unifikuje się z czymkolwiek.
        Stan bez ani jednego takiego środowiska w tablicy jest,
        bo ta pyta o cechy dopiero po lesie, a analizą nie jest.
        Drugi: przewidziała go inna analiza częściowa.
        Bez niego wystarczyłoby, że symbolu oczekuje w tym miejscu jakikolwiek stan,
        choćby sam nie był analizą,
        i odrzucenie stawałoby wtedy na formie, do której nie doszedł nikt.

        Pętla wewnętrzna dobija do punktu stałego,
        bo przewidywanie dopisuje stany do tej samej pozycji, w której je czyta.
        """
        żywe = {
            (production, self._tablica.początek)
            for production in self.grammar.for_head(self._tablica.start)
        }
        for k in self._tablica.pozycje_grafu:
            czekające: set[_Stan] = set()
            rosło = True
            while rosło:
                rosło = False
                for stan in self._tablica.stany.get(k, ()):
                    production, kropka, źródło = stan
                    if kropka == len(production.body) or (production, źródło) not in żywe:
                        continue
                    if not self._prefiks(production, kropka, źródło, k):
                        continue
                    część = production.body[kropka]
                    if not isinstance(część, Sym):
                        czekające.add(stan)
                        continue
                    for przewidziana in self.grammar.for_head(część.name):
                        rosło = rosło or (przewidziana, k) not in żywe
                        żywe.add((przewidziana, k))
            for stan in czekające:
                yield k, stan

    def _prefiks(
        self, production: Production, kropka: int, źródło: int, k: int
    ) -> frozenset[Env]:
        """Środowiska, z jakimi ta produkcja doszła tu przebytym ciałem.

        To samo pytanie co w :meth:`_przejdź`, zadane o inne miejsce w ciele:
        tam o cechy wychodzące nad ciałem domkniętym,
        a tutaj o środowisko w jego środku,
        bo terminal następujący po córce dostaje jej zawężenie.
        Córka wchodzi tu wszystkimi swoimi klasami naraz,
        bo pytanie nie dotyczy jednego kształtu.
        """
        if kropka == 0:
            return frozenset({EMPTY}) if źródło == k else frozenset()
        klucz = (production, kropka, źródło, k)
        gotowe = self._prefiksy.get(klucz)
        if gotowe is not None:
            return gotowe
        część = production.body[kropka - 1]
        środowiska: set[Env] = set()
        for j, dziecko in self._tablica.stany.get(k, {}).get((production, kropka, źródło), ()):
            cechy = [] if dziecko.liść else [c for klasa in self.klasy(dziecko) for c in klasa]
            środowiska |= self._dołóż(
                część, dziecko, cechy, self._prefiks(production, kropka - 1, źródło, j)
            )
        self._prefiksy[klucz] = frozenset(środowiska)
        return self._prefiksy[klucz]

    def czytania(self) -> Iterator[Node]:
        """Czytania jako drzewa, po jednym na kształt i w porządku, w jakim las stoi.

        Każda gałąź kończy się czytaniem,
        bo ``klasy`` odsiały już kombinacje, których unifikacja nie przepuszcza.
        Dlatego urwanie po :data:`MAX_READINGS` kosztuje tyle, ile wypisane drzewa,
        i nic ponad to.
        """
        for klasa in self.klasy(self.korzeń):
            yield from self._drzewa(self.korzeń, klasa)

    def _drzewa(self, pozycja: Pozycja, klasa: Klasa) -> Iterator[Node]:
        for kombinacja, production in self._krawędzie[(pozycja, klasa)].items():
            yield from self._z_córek(pozycja, production, kombinacja, ())

    def _z_córek(
        self, pozycja: Pozycja, production: Production, kombinacja: tuple, zebrane: tuple
    ) -> Iterator[Node]:
        """Drzewa, jakie z tych córek wychodzą, budowane od lewej i po jednym.

        Iloczyn kartezjański z biblioteki materializuje swoje wejścia,
        więc granica z :data:`MAX_READINGS` przestałaby cokolwiek ograniczać:
        zdanie o dziesiątkach tysięcy czytań wypisałoby je wszystkie,
        żeby oddać sześćdziesiąt cztery.
        Tutaj każde drzewo kosztuje osobno.
        """
        if len(zebrane) == len(kombinacja):
            yield Node(
                label=pozycja.label or "",
                children=zebrane,
                span=pozycja.span,
                głowa=production.głowa,
            )
            return
        część = production.body[len(zebrane)]
        dziecko, córka = kombinacja[len(zebrane)]
        córki = (
            [self._liść(część, dziecko)] if dziecko.liść else self._drzewa(dziecko, córka)
        )
        for drzewo in córki:
            yield from self._z_córek(pozycja, production, kombinacja, (*zebrane, drzewo))

    def _liść(self, część: Word, dziecko: Pozycja) -> Leaf:
        """Liść nazwany pierwszym czytaniem, jakie ten terminal bierze.

        Czytania jednej formy są jednym kształtem,
        więc drzewo wybiera tu przedstawiciela, a nie czytanie.
        Pytają o liść same formy, a forma jest wspólna każdemu czytaniu tej rozpiętości.
        """
        for segment, reading, cechy in self._czytania_liścia.get(dziecko.span, ()):
            if bierze(część, reading.tag.pos, reading.lemma, cechy, EMPTY) is not None:
                return Leaf(segment, reading)
        raise AssertionError(f"liść {dziecko.span} stoi w lesie bez czytania, które go bierze")

    # -- role, o które czytania się różnią ---------------------------------- #

    def różniące(self, role: Sequence[str]) -> tuple[str, ...]:
        """Te z ról, które nie mają w każdym czytaniu tego samego wypełnienia.

        Pytamy las, a nie streszczenia czytań.
        Streszczeń jest najwyżej :data:`MAX_READINGS`,
        a zdanie ustawy ma czytań dziesiątki tysięcy,
        więc rola różniąca się dopiero za tą granicą nie zostałaby nazwana,
        choć liczba obok niej granicy nie ma.

        Jednym wystąpieniem roli jest to, które nazywa :func:`describe`,
        czyli pierwsze w porządku wyprowadzenia.
        Etykieta pada w czytaniu kilka razy, bo zdanie współrzędne ma własny podmiot,
        a dwa podmioty stojące obok siebie w jednym czytaniu
        nie mówią nic o różnicy między czytaniami.

        Porównujemy rozpiętości, a nie formy:
        formy nad jedną rozpiętością są w każdym czytaniu te same,
        a różni je podział na segmenty, którego streszczenie i tak nie pokazuje.
        Rozpiętość ``None`` jest czytaniem bez tej roli,
        tak jak streszczenie bez tego klucza.
        """
        znalezione = []
        for etykieta in role:
            wystąpienia = {
                rozpiętość
                for klasa in self.klasy(self.korzeń)
                for rozpiętość in self._pierwsza_rola((self.korzeń, klasa), etykieta)
            }
            if len(wystąpienia) > 1:
                znalezione.append(etykieta)
        return tuple(znalezione)

    def _pierwsza_rola(
        self, para: tuple[Pozycja, Klasa], etykieta: str
    ) -> frozenset[tuple[int, int] | None]:
        """Czym bywa pierwszy węzeł tej etykiety pod tą parą; ``None``, gdy go nie ma.

        Ciało przechodzi się od lewej i kończy na pierwszej córce,
        która tę rolę niesie w każdym swoim czytaniu:
        dalsze córki są wtedy za pierwszym wystąpieniem i nie nazywają go.
        Wyborów córek nic nie wiąże, więc suma po nich jest tym, co dają czytania,
        a wyników jest tyle, ile rozpiętości, a nie ile drzew.
        """
        pozycja, _klasa = para
        if pozycja.label == etykieta:
            return frozenset({pozycja.span})
        gotowe = self._pierwsze_role.get((para, etykieta))
        if gotowe is not None:
            return gotowe
        znalezione: set[tuple[int, int] | None] = set()
        for kombinacja in self._krawędzie.get(para, {}):
            bez_roli = True
            for dziecko, klasa in kombinacja:
                if dziecko.liść:
                    continue
                pod_córką = self._pierwsza_rola((dziecko, klasa), etykieta)
                znalezione |= pod_córką - {None}
                if None not in pod_córką:
                    bez_roli = False
                    break
            if bez_roli:
                znalezione.add(None)
        self._pierwsze_role[(para, etykieta)] = frozenset(znalezione)
        return self._pierwsze_role[(para, etykieta)]

    # -- przyłączenia ------------------------------------------------------- #

    def przyłączenia(self, przyłączany: str, gospodarze: Sequence[str]) -> list[Przyłączenie]:
        """Modyfikatory, którym czytania dają więcej niż jednego gospodarza.

        Jeden wpis na wybór, bo tyle wyborów zdanie zostawia.
        Modyfikator występuje w każdym czytaniu raz,
        więc dwóch gospodarzy jednej pozycji to dwa czytania różniące się tym przyłączeniem,
        i zdanie o sześciu wyrażeniach przyimkowych
        daje sześć wpisów wobec sześćdziesięciu czterech czytań.

        Wyborem jest przyimek, a nie pozycja,
        i dlatego pozycje o jednym początku wchodzą tu razem.
        ``w pliku`` i ``w pliku w katalogu`` to dwie pozycje z dwóch różnych czytań,
        a decyzja pod nimi jest jedna: gdzie przyłącza się wyrażenie otwarte przez ``w``.
        Licząc po pozycjach, dostalibyśmy wpis na każdą parę przyimków,
        czyli znów kwadrat zamiast długości zdania.
        """
        u_kogo: dict[int, set[Pozycja]] = {}
        najkrótsze: dict[int, Pozycja] = {}
        for pozycja in sorted({para[0] for para in self._żywe()}, key=lambda p: p.span):
            if pozycja.label != przyłączany:
                continue
            początek = pozycja.span[0]
            najkrótsze.setdefault(początek, pozycja)
            u_kogo.setdefault(początek, set()).update(self._gospodarze(pozycja, gospodarze))
        znalezione = []
        for początek, pozycja in sorted(najkrótsze.items()):
            gospodarze_pozycji = sorted(u_kogo[początek], key=lambda p: p.span)
            if len(gospodarze_pozycji) < 2:
                continue
            # Dwie pozycje o jednej głowie są jednym wyborem,
            # bo grupa imienna dłuższa o inny modyfikator jest tą samą grupą imienną.
            nazwy = list(
                dict.fromkeys(
                    self._przedstawiciel(gospodarz).forma_głowy()
                    for gospodarz in gospodarze_pozycji
                )
            )
            if len(nazwy) < 2:
                continue
            znalezione.append(
                Przyłączenie(" ".join(self._przedstawiciel(pozycja).forms()), tuple(nazwy))
            )
        return znalezione

    def _gospodarze(self, pozycja: Pozycja, gospodarze: Sequence[str]) -> set[Pozycja]:
        """Konstytuenty z ``gospodarze``, w których ten modyfikator stoi w którymś czytaniu.

        Szukamy w górę, bo pytanie dotyczy tego, co modyfikator określa,
        a nie tego, pod czym się znalazł:
        okolicznik zdania sąsiaduje w drzewie z dopełnieniem, którego nie określa.
        Modyfikator bez żadnego z tych konstytuentów nad sobą określa całe czytanie
        i wychodzi stąd korzeniem, tak samo jak w :func:`_host`.
        """
        znalezione: set[Pozycja] = set()
        obejrzane: set[tuple[Pozycja, Klasa]] = set()
        stos = [para for para in self._żywe() if para[0] == pozycja]
        while stos:
            para = stos.pop()
            if para in obejrzane:
                continue
            obejrzane.add(para)
            rodzice = self._rodzicielskie().get(para, set())
            if not rodzice:
                znalezione.add(self.korzeń)
            for rodzic in rodzice:
                if rodzic[0].label in gospodarze:
                    znalezione.add(rodzic[0])
                else:
                    stos.append(rodzic)
        return znalezione

    def _żywe(self) -> set[tuple[Pozycja, Klasa]]:
        """Pary pozycja–klasa, które stoją w którymś czytaniu.

        Schodzimy od korzenia,
        bo tablica domyka i takie pozycje, których żadne czytanie nie przyjmuje,
        a werdykt ma mówić o czytaniach.
        """
        if self._żywe_pary is not None:
            return self._żywe_pary
        żywe: set[tuple[Pozycja, Klasa]] = set()
        rodzice: dict[tuple[Pozycja, Klasa], set[tuple[Pozycja, Klasa]]] = {}
        stos = [(self.korzeń, klasa) for klasa in self.klasy(self.korzeń)]
        while stos:
            para = stos.pop()
            if para in żywe:
                continue
            żywe.add(para)
            for kombinacja in self._krawędzie.get(para, {}):
                for dziecko, klasa in kombinacja:
                    if dziecko.liść:
                        continue
                    rodzice.setdefault((dziecko, klasa), set()).add(para)
                    stos.append((dziecko, klasa))
        self._żywe_pary = żywe
        self._rodzice = rodzice
        return żywe

    def _rodzicielskie(self) -> dict[tuple[Pozycja, Klasa], set[tuple[Pozycja, Klasa]]]:
        self._żywe()
        assert self._rodzice is not None
        return self._rodzice

    def _przedstawiciel(self, pozycja: Pozycja) -> Node:
        """Jedno z drzew tej pozycji, do nazwania jej.

        Nazwać trzeba konstytuent, a nie czytanie, a formy ma on w każdym swoim
        czytaniu te same; różni je podział na segmenty, którego nazwa i tak nie
        pokazuje. Głowa tak daleko nie sięga: ``dobry kod`` jest raz
        przymiotnikiem przed rzeczownikiem, a raz rzeczownikiem z dopełniaczem
        po nim, więc jedna rozpiętość ma tam dwie głowy, a nazwa bierze tę z
        pierwszego drzewa i tego wyboru nie ogłasza. Co z tym zrobić, jest
        otwarte w TODO.md.
        """
        gotowe = self._przedstawiciele.get(pozycja)
        if gotowe is not None:
            return gotowe
        for klasa in self.klasy(pozycja):
            for drzewo in self._drzewa(pozycja, klasa):
                self._przedstawiciele[pozycja] = drzewo
                return drzewo
        raise AssertionError(f"pozycja {pozycja} stoi w lesie bez ani jednego drzewa")


# --------------------------------------------------------------------------- #
# Streszczenie czytania
# --------------------------------------------------------------------------- #

#: Znak, którym streszczenie oddziela modyfikator od tego, do czego doszedł.
#: Bez słowa, bo słowo żądałoby przypadka od tego, co po nim następuje,
#: a następuje tam forma wzięta ze zdania i nieodmieniana.
PRZYŁĄCZONY_DO = " → "


def describe(node: Node, deklaracja: Deklaracja) -> dict[str, str]:
    """Streszczenie czytania: co stoi w której roli i do czego doszedł modyfikator.

    Dwa czytania jednego zdania gdzieś się różnią,
    a streszczenie pokazuje tę różnicę temu, kto ma zdanie poprawić.
    Same role tego nie pokazują,
    bo grupa przyimkowa dochodzi raz do jednej głowy, a raz do drugiej,
    i formy stojące nad nią zostają wtedy te same:
    ``koszt szynki z dodatkami`` jest tym samym dopełnieniem niezależnie od tego,
    czy ``z dodatkami`` doszło do ``koszt``, czy do ``szynki``.
    Rola przyłączana dostaje więc obok wypełnienia to, co modyfikator określa.

    Żąda tego jedna rola, bo jedną gramatyka zostawia nierozstrzygniętą rozmyślnie:
    podmiot i dopełnienie rozstrzyga przypadek,
    a pozycje przyłączeniowe stoją po to, żeby dać oba czytania
    (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    Dopisane jest wypełnienie, a nie pozycja obok niego,
    więc :attr:`Deklaracja.role` zostaje listą ról.

    Nazwany jest pierwszy modyfikator czytania i tylko on,
    więc dwa czytania różne miejscem drugiego wychodzą stąd jednym napisem.
    Streszczenie jest po to jedno na czytanie, a wierszy jest tyle, ile czytań;
    zdanie, którego to nie rozstrzyga, rozstrzyga :meth:`Las.przyłączenia`,
    gdzie wpisów jest tyle, ile nierozstrzygniętych wyborów.
    """
    summary = {}
    for role in deklaracja.role:
        found = node.find(role)
        if not found:
            continue
        summary[role] = " ".join(found[0].forms())
        if role == deklaracja.przyłączany:
            summary[role] += PRZYŁĄCZONY_DO + _attachment(node, found[0], deklaracja.gospodarze)
    return summary


def _attachment(root: Node, modifier: Node, hosts: tuple[str, ...]) -> str:
    """Co modyfikator określa: konstytuent, do którego doszedł, nazwany swoją głową.

    Ani węzeł, pod którym modyfikator stoi bezpośrednio,
    ani najbliższy węzeł z materiałem obok na to pytanie nie odpowiadają:
    okolicznik zdania stoi w drzewie tuż obok dopełnienia, którego nie określa.
    Odpowiada konstytuent wyliczony w :attr:`Deklaracja.gospodarze`,
    czyli ten, w którego produkcji to przyłączenie stoi.
    """
    return _host(root, modifier, hosts, root).forma_głowy()


def _host(tree: Tree, modifier: Node, hosts: tuple[str, ...], outer: Node) -> Node | None:
    """Najbliższy konstytuent z ``hosts``, w którym stoi ten modyfikator; ``None`` poza nim.

    ``outer`` jest odpowiedzią dla korzenia,
    bo modyfikator, nad którym nie stoi żaden z tych konstytuentów, określa całe czytanie.
    """
    if tree is modifier:
        return outer
    if isinstance(tree, Leaf):
        return None
    inner = tree if tree.label in hosts else outer
    for child in tree.children:
        found = _host(child, modifier, hosts, inner)
        if found is not None:
            return found
    return None
