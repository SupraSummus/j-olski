"""Łańcuch dopełniaczy, czyli grupa imienna, w której przydawka stoi pod przydawką.

`Raport zawiera analizę wyników badań skuteczności metod leczenia pacjentów oddziału.`
każe czytelnikowi zgadywać, co do czego należy:
każda z tych form określa formę stojącą przed nią,
a która z nich określa którą, mówi dopiero rozbiór.
Naprawą jest czasownik, a nie krótszy łańcuch:
`Raport analizuje, jak skutecznie oddział leczy pacjentów.`

Reguła pyta o rozbiór, bo dopełniacz jest u Morfeusza zlany z innymi przypadkami,
a łańcuch czytany ze znaczników liczy formy zamiast przydawek:
`zdania tego jednego pliku` ma cztery formy w dopełniaczu i jedną przydawkę.
Zdanie, którego gramatyka nie wyprowadza, zostaje przez to bez wiersza,
i tym różni się ta reguła od chwytu rejestru (``olski/chwyty.py``),
który czyta się z samej morfologii.

Wiersz o łańcuchu pada obok werdyktu i tylko pod flagą ``--dopełniacze``,
bo sądów czytelnika nad cudzym tekstem ta reguła nie ma;
próg wraz z tym, co go rusza, trzyma
docs/linter.md#czwarty-wykrywacz-zgłasza-łańcuch-dopełniaczy.
"""

from __future__ import annotations

from dataclasses import dataclass

from olski.parse import Leaf, Node, Result, Tree, sklej_formy
from olski.subset import DEKLARACJA

#: Nazwa zgłoszenia, tak jak nazywa je korpus usterek (``harness/usterki.py``).
ŁAŃCUCH_DOPEŁNIACZY = "łańcuch dopełniaczy"

#: Od ilu przydawek dopełniaczowych stojących jedna pod drugą pada zgłoszenie.
#: Cztery, bo łańcuch trzech stoi w polszczyźnie, której czytelnik nie poprawia:
#: `model środka gamy Fiata`.
PRÓG = 4

#: Co autor ma z taką grupą zrobić.
NAPRAWA_ŁAŃCUCHA = "przetnij grupę i orzeknij czynność czasownikiem"


@dataclass(frozen=True)
class Łańcuch:
    """Grupa imienna wraz z liczbą przydawek, które w niej wiszą jedna pod drugą.

    Liczba idzie razem z grupą, bo to ona rozstrzyga o zgłoszeniu (:data:`PRÓG`),
    a autor odszukuje grupę w swoim zdaniu po formach.
    """

    #: Grupa tak, jak stoi w zdaniu.
    grupa: str
    #: Ile przydawek dopełniaczowych stoi w niej jedna pod drugą.
    ile: int


def łańcuchy(wynik: Result) -> tuple[Łańcuch, ...]:
    """Łańcuchy dopełniaczy tego zdania; pusta krotka jest milczeniem.

    Zdanie wieloznaczne wydaje ten łańcuch, który stoi w każdym jego czytaniu.
    Łańcucha, którego jedno czytanie nie ma, czytelnik nie musi czytać łańcuchem,
    a reguła myli się przez to w stronę milczenia,
    tak samo jak zawężenia warstwy zaimkowej (``olski/odniesienia.py``).
    Czytania idą tu tak, jak wydał je las, a on urywa je na swojej granicy
    (:data:`olski.parse.MAX_READINGS`), więc zdanie o setkach czytań
    myli się w stronę odwrotną: łańcuch zdjęty czytaniem urwanym zostaje.
    """
    if not wynik.readings:
        return ()
    pierwsze, *dalsze = [_w_czytaniu(czytanie) for czytanie in wynik.readings]
    return tuple(łańcuch for łańcuch in pierwsze if all(łańcuch in inne for inne in dalsze))


def _w_czytaniu(czytanie: Tree) -> tuple[Łańcuch, ...]:
    """Łańcuchy jednego czytania, w kolejności zdania.

    Grupa stojąca w środku grupy dłuższej własnego wiersza nie dostaje:
    jej przydawki są przydawkami tamtej, a autor czyta całą grupę naraz.
    Ceną jest milczenie o łańcuchu drugim, który stanął pod tym samym rzeczownikiem
    w wyrażeniu przyimkowym; wiersz o grupie szerszej wskazuje i jego formy.
    """
    if isinstance(czytanie, Leaf):
        return ()
    długie = [
        (grupa, ile)
        for grupa in czytanie.find(DEKLARACJA.grupa_imienna)
        if (ile := _przydawki(grupa)) >= PRÓG
    ]
    return tuple(
        Łańcuch(sklej_formy(grupa.forms()), ile)
        for grupa, ile in długie
        if not any(_wewnątrz(grupa, szersza) for szersza, _ in długie)
    )


def _wewnątrz(grupa: Node, szersza: Node) -> bool:
    return szersza.span != grupa.span and (
        szersza.span[0] <= grupa.span[0] and grupa.span[1] <= szersza.span[1]
    )


def _przydawki(grupa: Node) -> int:
    """Ile przydawek dopełniaczowych stoi pod tą grupą, jedna pod drugą."""
    ile = 0
    przydawka = _przydawka(grupa)
    while przydawka is not None:
        ile += 1
        przydawka = _przydawka(przydawka)
    return ile


def _przydawka(grupa: Node) -> Node | None:
    """Przydawka dopełniaczowa tej grupy imiennej, albo nic.

    Przydawki szuka się pod członem imiennym, a nie pod samą grupą, bo grupa
    imienna stojąca pod grupą imienną jest członem ciągu współrzędnego albo
    apozycją — `pliki i katalogi`, `Stilo, model Fiata` — i przypadek ma ten sam,
    co jej głowa. Dopełniacza żąda dopiero głowa członu (``olski/subset/grupa.py``),
    więc grupa stojąca pod członem obok jego głowy jest dopełniaczem i niczym innym.

    Schodzenie idzie po głowach, bo między grupą a członem z przydawką stoi
    tyle węzłów, ile ta grupa ma przymiotników przed rzeczownikiem:
    w `wyników wszystkich badań` przydawka wisi pod członem stojącym pod przydawką
    przymiotną, a nie pod tym, którym grupa się zaczyna.
    """
    węzeł: Tree = grupa
    while isinstance(węzeł, Node):
        if węzeł.label == DEKLARACJA.człon_imienny:
            for numer, dziecko in enumerate(węzeł.children):
                if (
                    numer != węzeł.głowa
                    and isinstance(dziecko, Node)
                    and dziecko.label == DEKLARACJA.grupa_imienna
                ):
                    return dziecko
        węzeł = węzeł.children[węzeł.głowa]
    return None
