"""Reprezentacja pośrednia: kto co robi w zdaniu, bez kształtu gramatyki.

Czytanie parsera schodzi tu do zbioru krawędzi (głowa, rola, zależnik) nad słowami zdania.
Krawędź jest trójką, na której ma się uczyć model przebiegu semantycznego.
Dwa czytania o tym samym zbiorze krawędzi są jednym czytaniem,
ale na zdaniach z NKJP zdarza się to rzadko (``docs/kierunek.md``).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from olski.parse import Leaf, Node, ciało_koordynuje
from olski.subset.deklaracja import GRUPUJĄCE, OKOLICZNIK_PRZYSŁÓWKOWY
from olski.walencja import KOPULA

#: Rola członu współrzędnego przy słowie, które człony spina.
CZŁON = "człon"

ORZECZNIK = "orzecznik"

#: Części mowy orzecznika, który z łącznikiem tworzy jedno orzeczenie.
#: Orzecznik rzeczowny zostaje osobno, bo rzeczownik ma własne określenia
#: (`odpowiedź na pytanie`), a przymiotnik w orzeczeniu jest samym orzekaniem.
PRZYMIOTNE = frozenset({"adj", "ppas", "pact"})

#: Znak interpunkcyjny słowem reprezentacji nie jest, chyba że spina człony.
INTERPUNKCJA = "interp"
SPINAJĄCE = frozenset({"conj", INTERPUNKCJA})

PRZYSŁÓWEK = "adv"


@dataclass(frozen=True, order=True)
class Słowo:
    """Wystąpienie słowa w zdaniu.

    Tożsamością jest miejsce w grafie segmentacji razem z lematami,
    bo forma czytana innym leksemem jest innym słowem:
    `sobie` od `siebie` i od rzeczownika `soba` to dwa czytania, a nie jedno.
    """

    początek: int
    koniec: int
    forma: str
    lematy: tuple[str, ...]
    części_mowy: tuple[str, ...]

    def __str__(self) -> str:
        return self.forma


@dataclass(frozen=True, order=True)
class Krawędź:
    głowa: Słowo
    rola: str
    zależnik: Słowo

    def __str__(self) -> str:
        return f"{self.głowa} —{self.rola}→ {self.zależnik}"


@dataclass(frozen=True)
class Reprezentacja:
    korzeń: Słowo
    krawędzie: frozenset[Krawędź]


def _słowo(liść: Leaf) -> Słowo:
    return Słowo(
        liść.segment.start,
        liść.segment.end,
        liść.segment.form,
        tuple(sorted({odczytanie.lemma for odczytanie in liść.odczytania})),
        tuple(sorted({odczytanie.tag.pos for odczytanie in liść.odczytania})),
    )


def _etykieta(drzewo: Leaf | Node) -> str | None:
    return drzewo.label if isinstance(drzewo, Node) else None


def _spójnik(drzewo: Node) -> Leaf | None:
    """Słowo, które spina człony współrzędne, albo nic, gdy węzeł współrzędnością nie jest.

    Kryterium jest to samo co w streszczeniu, ale żąda spójnika albo przecinka,
    bo :func:`olski.parse.ciało_koordynuje` liczy ciągiem także `jak nisko`.
    W `, ale` spina `ale`, a nie przecinek.
    """
    if not ciało_koordynuje(drzewo.label, map(_etykieta, drzewo.children)):
        return None
    spinające = [
        dziecko
        for dziecko in drzewo.children
        if isinstance(dziecko, Leaf) and dziecko.reading.tag.pos in SPINAJĄCE
    ]
    return max(spinające, key=lambda liść: liść.reading.tag.pos != INTERPUNKCJA, default=None)


def _rola(dziecko: Leaf | Node) -> str:
    """Etykieta węzła albo część mowy słowa.

    Przysłówek ma jedną rolę, czy gramatyka wzięła go okolicznikiem,
    czy słowem w grupie przymiotnikowej.
    """
    if isinstance(dziecko, Node):
        return dziecko.label
    część = dziecko.reading.tag.pos
    return OKOLICZNIK_PRZYSŁÓWKOWY if część == PRZYSŁÓWEK else część


class _Budowa:
    def __init__(self) -> None:
        self.krawędzie: set[Krawędź] = set()

    def węzeł(self, drzewo: Leaf | Node) -> Słowo:
        """Słowo, którym konstytuent stoi w reprezentacji; krawędzie pod nim idą do zbioru.

        Współrzędność stoi swoim spójnikiem, bo żaden z członów nie jest głową drugiego.
        Członami są córki aż do ciągu, który powtarza etykietę węzła,
        a to, co stoi za nim, określa całą współrzędność.
        """
        if isinstance(drzewo, Leaf):
            return _słowo(drzewo)
        spójnik = _spójnik(drzewo)
        if spójnik is None:
            głowa = self.węzeł(drzewo.children[drzewo.głowa])
            for numer, dziecko in enumerate(drzewo.children):
                if numer != drzewo.głowa:
                    self.przyłącz(głowa, dziecko)
            return głowa
        głowa = _słowo(spójnik)
        ciąg = max(
            numer
            for numer, dziecko in enumerate(drzewo.children)
            if _etykieta(dziecko) == drzewo.label
        )
        for numer, dziecko in enumerate(drzewo.children):
            if numer <= ciąg and isinstance(dziecko, Node):
                self.krawędzie.add(Krawędź(głowa, CZŁON, self.węzeł(dziecko)))
            elif dziecko is not spójnik:
                self.przyłącz(głowa, dziecko)
        return głowa

    def przyłącz(self, głowa: Słowo, dziecko: Leaf | Node) -> None:
        """Krawędź od głowy do córki; córki węzła grupującego stoją przy tej samej głowie."""
        if isinstance(dziecko, Leaf) and dziecko.reading.tag.pos == INTERPUNKCJA:
            return
        if _etykieta(dziecko) in GRUPUJĄCE:
            for wnuk in dziecko.children:
                self.przyłącz(głowa, wnuk)
            return
        self.krawędzie.add(Krawędź(głowa, _rola(dziecko), self.węzeł(dziecko)))


def _scal_łącznik(krawędzie: frozenset[Krawędź]) -> frozenset[Krawędź]:
    """Łącznik z orzecznikiem przymiotnym jako jedno orzeczenie.

    `jest prowadzona od wtorku` mówi to samo, czy `od wtorku` doszło do `jest`,
    czy do `prowadzona`, więc zależniki przymiotnika przechodzą do łącznika.
    """
    scalone = {
        krawędź.zależnik: krawędź.głowa
        for krawędź in krawędzie
        if krawędź.rola == ORZECZNIK
        and KOPULA.intersection(krawędź.głowa.lematy)
        and PRZYMIOTNE.intersection(krawędź.zależnik.części_mowy)
    }
    return frozenset(
        Krawędź(scalone.get(krawędź.głowa, krawędź.głowa), krawędź.rola, krawędź.zależnik)
        for krawędź in krawędzie
    )


def obniż(czytanie: Node) -> Reprezentacja:
    budowa = _Budowa()
    korzeń = budowa.węzeł(czytanie)
    return Reprezentacja(korzeń, _scal_łącznik(frozenset(budowa.krawędzie)))


def reprezentacje(czytania: Iterable[Node]) -> list[Reprezentacja]:
    """Różne reprezentacje tych czytań, w kolejności pierwszego wystąpienia."""
    return list(dict.fromkeys(obniż(czytanie) for czytanie in czytania))
