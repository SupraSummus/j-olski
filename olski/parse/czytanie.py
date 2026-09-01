"""Czytanie i jego kawałki: pozycja lasu, liść i węzeł.

Typy, którymi mówią do siebie warstwy rozbioru i którymi parser odpowiada na zewnątrz.
Co czyni dwa wyprowadzenia jednym czytaniem, rozstrzyga :meth:`Node.signature`.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from olski.morph import Reading, Segment


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
    docs/parsowanie.md#co-się-pakuje-rozstrzyga-tożsamość-czytania.

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
    """Forma pod terminalem i czytania, którymi ją ten kształt bierze."""

    segment: Segment
    #: Odczytania licencjonujące ten liść w kształcie, w jakim stoi, a nie
    #: dowolne odczytania formy: `lubi` pod orzeczeniem ma tu samo `lubić`, choć
    #: Morfeusz czyta tę formę również jako rzeczownik i jako przymiotnik.
    #: Jest ich kilka tam, gdzie kształtu nie rozstrzygają — `Janek` w podmiocie
    #: stoi i jako `subst:sg:nom:m1`, i jako nazwisko nieodmienne —
    #: i wtedy wybór między nimi nie należy do gramatyki
    #: (:meth:`Node.signature` mówi, dlaczego odczytania kształt nie liczy).
    #: Kolejność jest kolejnością odczytań w segmencie, żeby dwa przebiegi
    #: wypisywały to samo.
    odczytania: tuple[Reading, ...]

    @property
    def reading(self) -> Reading:
        """Pierwsze z odczytań licencjonujących, dla tego, kto pyta o jedno.

        Kto pyta o lemat, tym wyborem wiązać się nie powinien:
        ``olski/skład/rozbiór.py`` pyta o lemat krawędź grafu i mówi, po co.
        """
        return self.odczytania[0]

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
    #: Takiej produkcji gramatyka olskiego nie ma i nie żąda jej rozwinięcie szyku:
    #: miejsce na okolicznik wychodzi z niego osobnym ciałem, a nie córką o pustej rozpiętości,
    #: bo córka taka stałaby w każdym miejscu każdego zdania i mnożyła wyprowadzenia.
    #: Pustego ciała żąda natomiast luka, i tego żądania nikt nie zaspokoił.
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

        Wyliczone drzewo niesie za to więcej niż sygnaturę,
        bo na liściach stoją czytania, a tych kształt nie liczy.
        Klasa czytania zbiera wyprowadzenia różne samą morfologią,
        więc nie rozstrzyga, które z nich w drzewie stoi;
        rozstrzyga, że czytanie spoza niej jest w nim błędem,
        i tyle drzewo dostaje (:meth:`Las._wybierz`).
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

    def find(self, label: str, skip: Sequence[str] = ()) -> list[Node]:
        """Every node with this label, this one included, outermost first.

        A subtree labelled with one of ``skip`` is named where it stands and not
        entered, which is how the summary asks for the roles of the clause it
        summarises rather than for the roles of a clause subordinate to it
        (:attr:`Deklaracja.podrzędne`). Named, because a subordinate clause is
        sometimes a role itself: an adverbial clause is one of the roles readings
        differ in, and its inside is a separate sentence all the same.
        The coverage check passes nothing, because the gold tree marks a role
        wherever a clause has one.
        """
        found = [self] if self.label == label else []
        if self.label in skip:
            return found
        for child in self.children:
            if isinstance(child, Node):
                found.extend(child.find(label, skip))
        return found


Tree = Leaf | Node
