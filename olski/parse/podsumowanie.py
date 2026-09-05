"""Co werdykt bierze z lasu i czym o to pyta.

:class:`Deklaracja` jest pytaniem, które gramatyka wypełnia o sobie,
a :class:`Result` wraz z :class:`Przyłączenie` i :class:`Rozbieżność` odpowiedzią.
Liczy te odpowiedzi las (``olski/parse/las.py``);
typy są od niego osobno, bo czyta je warstwa, która lasu nie ogląda
(``olski/werdykt/``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from olski.parse.czytanie import Node


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
class Rozbieżność:
    """Konstytuent, który czyta się kilkoma sposobami tam, gdzie streszczenie nie zagląda.

    Streszczenie nazywa wypełnienie roli i gospodarza przyłączenia,
    więc dwa czytania różne czymkolwiek innym wychodzą z niego jednym napisem,
    a werdykt mówi wtedy samą liczbę czytań i czyta się jak usterka narzędzia.
    Poza zasięgiem streszczenia zostają dwa miejsca:
    wnętrze wypełnienia jednej roli i wnętrze zdania podrzędnego
    (:attr:`Deklaracja.podrzędne`).
    ``zainteresowana rada gminy`` jest raz przymiotnikiem przed rzeczownikiem,
    a raz rzeczownikiem z dopełniaczem po nim, i podmiotem jest w obu ten sam napis;
    ``że organ gminy wydaje przepis`` różni podmiot i dopełnienie,
    tyle że tamtego zdania, a nie tego.

    Lematu wpis nie nazywa, choć różnica bywa właśnie lematem.
    Nazwałby to, czego liczba czytań obok niego nie liczy:
    część mowy i lemat są z tożsamości czytania wyłączone rozmyślnie
    (:meth:`Node.signature`), więc dwa czytania różne samym lematem są jednym.

    Streszczenia niesie wpis dlatego, że streszczenie zdania ich nie niesie:
    rola z wnętrza zdania podrzędnego jest rolą tego zdania, a nie tego nad nim,
    więc dopiero streszczone osobno mówi, czym te czytania się różnią —
    w ``Ustawa mówi, że organ gminy wydaje przepis.``
    podmiotem jest raz ``organ gminy``, a raz ``przepis``.
    Grupa imienna roli zdania nie nosi, więc oba jej kształty streszczają się
    pustym słownikiem i po odsianiu powtórzeń zostaje z nich jedno streszczenie:
    różnicę niesie tam głowa, której streszczenie nie nazywa.
    """

    #: Formy konstytuenta, czyli to, co autor ma przepisać.
    konstytuent: str
    #: Ile czytań ten konstytuent ma, liczone tak jak :attr:`Result.ile` liczy zdanie.
    ile: int
    #: Streszczenia tych czytań, każde raz (:func:`streszczenia`).
    #: Pola bez wartości domyślnej, bo jedno streszczenie jest tu twierdzeniem
    #: o konstytuencie: znaczy, że streszczenie tej różnicy nie widzi.
    czytania: tuple[tuple[dict[str, str], ...], ...]


@dataclass(frozen=True)
class Obsada:
    """Które role czytania obsadzają pozycje ramy czasownika.

    Czyta to warstwa nad plikiem żądań (``olski/żądania.py``):
    żeby powiedzieć, czego czasownik żąda od słowa stojącego w jego pozycji,
    trzeba wiedzieć, która rola niesie ten czasownik, a która jego pozycję wypełnia.
    Rolami, bo warstwa ta ogląda gotowe czytanie, a nie gramatykę,
    a w czytaniu pozycja ramy jest właśnie etykietą roli.
    """

    #: Role, których głowa rządzi ramą zdania składowego.
    #: Jest ich kilka, bo orzeka też forma nieosobowa i predykatyw
    #: (``ORZECZENIE_BEZOSOBOWE`` w ``olski/subset/deklaracja.py``);
    #: w jednym zdaniu składowym stoi jedna z nich.
    orzeczenia: tuple[str, ...]
    #: Rola stojąca w pozycji podmiotu.
    podmiot: str
    #: Role, których pozycję nazywa przypadek wypełnienia,
    #: bo jedna nazwa roli pokrywa kilka pozycji ramy:
    #: `dopełnienie` nie mówi, w którym przypadku stoi.
    przypadkowe: tuple[str, ...]
    #: Symbole, których wnętrze obsadza ramę własnego czasownika:
    #: `dokument` w `Autor zamierzył edytować dokument.` jest dopełnieniem
    #: bezokolicznika, a nie formy osobowej nad nim.
    #: Zejście po role staje na nich, więc wiersz o tym dopełnieniu nie powstaje
    #: wcale, zamiast powstać z żądaniem cudzego czasownika.
    własna_rama: tuple[str, ...]


@dataclass(frozen=True)
class Deklaracja:
    """Co gramatyka mówi o sobie podsumowaniom werdyktu.

    Które symbole są rolami i gdzie szukać przyłączenia, wie gramatyka, a nie rozbiór,
    więc każde podsumowanie bierze to jedną wartością —
    :func:`parse`, :func:`describe` i :class:`Decyzje` pod nimi —
    a podsumowanie następne dokłada tutaj pole i nie rusza żadnej z tych sygnatur.
    Wypełnia ją gramatyka, a typ definiuje rozbiór,
    bo formalizm z ``olski/grammar.py`` niesie produkcje i o werdykcie nic nie wie.
    """

    #: Role, którymi streszcza się czytanie i o które czytania mogą się różnić.
    role: tuple[str, ...]
    #: Role, które się przyłączają,
    #: czyli te, przy których streszczenie nazywa jeszcze gospodarza.
    przyłączane: tuple[str, ...]
    #: Symbole konstytuentów, w których produkcjach przyłączenie stoi.
    gospodarze: tuple[str, ...]
    #: Ta z ról przyłączanych, której nierozstrzygniętego gospodarza werdykt liczy
    #: osobnym wierszem (:meth:`Decyzje.przyłączenia`),
    #: a warstwa za parserem zgaduje (``olski/rozstrzyganie.py``).
    #: Jest nią jedna, bo tabela skłonności i leksykon walencyjny
    #: mówią o wyrażeniu przyimkowym, a nie o każdym okoliczniku;
    #: czy wiersz werdyktu ma być szerszy od warstwy, nie rozstrzygnął nikt.
    rozstrzygany: str
    #: Symbole, których produkcje koordynują, czyli te, po których streszczenie
    #: nawiasuje człon ciągu współrzędnego.
    współrzędne: tuple[str, ...]
    #: Symbole zdań składowych, czyli członów ciągu zdań współrzędnych.
    #: Streszczeń jest tyle, ile zdanie ma składowych, po jednym na składowe,
    #: więc widać w nich całe zdanie współrzędne (:func:`describe`).
    składowe: tuple[str, ...]
    #: Symbole zdań podrzędnych, czyli tych, których wnętrze jest osobnym zdaniem.
    #: Streszczenie i :meth:`Decyzje.różniące` zatrzymują się na nich,
    #: bo rola z wnętrza takiego zdania jest jego rolą, a nie rolą zdania nad nim.
    #: Zatrzymują się na nich, a nie przed nimi: symbol stojący i tutaj, i w
    #: :attr:`role` nazywa się w streszczeniu całym sobą i wnętrza nie otwiera,
    #: czym jest okolicznik wyrażony zdaniem.
    #: Zatrzymać się muszą oba naraz, inaczej wiersz ``differing in``
    #: nazywa rolę, której lista czytań pod nim nie nazywa.
    #: Wywód, przykład i cenę trzyma
    #: docs/parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań.
    podrzędne: tuple[str, ...]
    #: Które role obsadzają pozycje ramy czasownika (:class:`Obsada`).
    obsada: Obsada
    #: Symbol konstytuenta, którym tekst nazywa rzecz.
    #: Pyta o niego warstwa szukająca tego, na co zaimek wskazuje
    #: (``olski/odniesienia.py``): kandydatem jest głowa takiego konstytuenta
    #: wziętego najszerzej, bo `duże pole maków` nazywa pole, a nie maki.
    #: Rolą ten symbol nie jest, bo rzecz nazwana stoi w każdej z ról imiennych
    #: i pod przyimkiem także, a pytanie jest o nią samą, a nie o jej pozycję.
    grupa_imienna: str


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
    #: Over a sentence that has a reading it is the sentence's last node.
    #: ``None`` says that nobody asked (:func:`podsumuj`), not that no analysis
    #: reached anywhere: the first graph node is an answer, since a sentence
    #: that stops on its own first form stops there.
    furthest: int | None = None
    #: Czy wyliczanie stanęło na :data:`MAX_READINGS`,
    #: czyli czy lista czytań jest krótsza niż :attr:`ile`.
    truncated: bool = False
    #: Role, o które czytania się różnią, o ile :func:`parse` dostał :class:`Deklaracja`.
    #: Wzięte z lasu, a nie ze streszczeń, których jest najwyżej :data:`MAX_READINGS`;
    #: dlaczego, mówi :meth:`Decyzje.różniące`.
    różniące: tuple[str, ...] = ()
    #: Przyłączenia, których czytania nie rozstrzygają,
    #: z tej samej deklaracji co :attr:`różniące`.
    #: Wpisane tu, a nie odpytywane z lasu:
    #: las jednego zdania waży tyle, ile jego tablica,
    #: a werdyktów trzyma się naraz tyle, ile dokument ma zdań.
    przyłączenia: tuple[Przyłączenie, ...] = ()
    #: Konstytuenty, w których czytania się różnią poza zasięgiem streszczenia,
    #: z tej samej deklaracji co :attr:`różniące`.
    rozbieżności: tuple[Rozbieżność, ...] = ()

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
