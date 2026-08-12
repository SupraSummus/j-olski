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

Implementation note. This is a memoizing top-down enumerator over the
segmentation graph, which is enough for a grammar without left recursion and
detects the case it cannot handle rather than looping. A chart parser over a
packed forest replaces it,
and what asks for that first is the verdict rather than the grammar:
several undecided attachments are several packed nodes
and one role name in a reading list.
docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań owns that
argument, the ordering it puts the move in,
and what left recursion and a forest walk add to it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from olski.grammar import EMPTY, Env, Grammar, Part, Sym, Word, bierze, features_of, unify
from olski.morph import Reading, Segment

#: Enumeration is capped, because an ambiguous sentence can have very many
#: derivations and the answer past the second one is always the same: too many.
MAX_READINGS = 64


class LeftRecursion(Exception):
    """The grammar is left-recursive, which this parser cannot handle."""


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
    features: frozenset[tuple[str, frozenset[str]]] = frozenset()

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
        """
        return (self.label, tuple(child.signature() for child in self.children))

    def forms(self) -> list[str]:
        return [form for child in self.children for form in child.forms()]

    def find(self, label: str) -> list[Node]:
        """Every node with this label, this one included, outermost first."""
        found = [self] if self.label == label else []
        for child in self.children:
            if isinstance(child, Node):
                found.extend(child.find(label))
        return found


Tree = Leaf | Node


@dataclass
class Result:
    """What the parser concluded about one sentence."""

    readings: list[Node] = field(default_factory=list)
    #: The furthest graph node any partial analysis reached, which is where a
    #: rejected sentence stopped making sense.
    furthest: int = 0
    truncated: bool = False

    @property
    def valid(self) -> bool:
        return len(self.readings) == 1

    @property
    def ambiguous(self) -> bool:
        return len(self.readings) > 1

    @property
    def rejected(self) -> bool:
        return not self.readings

    @property
    def status(self) -> str:
        """Which of the three the sentence is, as the verdict a reader is shown."""
        if self.valid:
            return "valid"
        return "ambiguous" if self.ambiguous else "rejected"


def parse(grammar: Grammar, segments: list[Segment], start: str | None = None) -> Result:
    """Enumerate the distinct readings of a segmented sentence."""
    parser = _Parser(grammar, segments)
    goal = Sym(start or grammar.start)
    end = max((segment.end for segment in segments), default=0)

    seen: dict = {}
    readings: list[Node] = []
    for tree, position, _ in parser.symbol(goal, _first(segments), EMPTY):
        if position != end or not isinstance(tree, Node):
            continue
        signature = tree.signature()
        if signature in seen:
            continue
        seen[signature] = True
        readings.append(tree)
        if len(readings) >= MAX_READINGS:
            return Result(readings, parser.furthest, truncated=True)
    return Result(readings, parser.furthest)


def wyprowadzenia(
    grammar: Grammar, segments: list[Segment], start: str | None = None
) -> list[Node]:
    """Każdy konstytuent, jaki rozbiór zbudował, także ten, którego rodzic nie wziął.

    :func:`parse` oddaje czytania, czyli to, co doszło aż do korzenia, a tablica
    pod nimi trzyma także wyprowadzenia, które unifikacja odrzuciła wyżej. Pyta o
    nią pomiar, a nie werdykt: pozycja spakowana po kształcie niesie
    wyprowadzenia różniące się cechami, których rodzic nie odróżnia, i stamtąd
    bierze się nadmiar sumy iloczynów po lesie
    (docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania).

    Korzenia ta funkcja nie wylicza, bo wyliczanie czytań tablicę czyta i niczego
    do niej nie dokłada.
    """
    parser = _Parser(grammar, segments)
    parser.analyses(start or grammar.start, _first(segments))
    return [node for found in parser._memo.values() for node, _end, _features in found]


def _first(segments: list[Segment]) -> int:
    return min((segment.start for segment in segments), default=0)


class _Parser:
    def __init__(self, grammar: Grammar, segments: list[Segment]) -> None:
        missing = grammar.undefined()
        if missing:
            raise ValueError(f"grammar refers to undefined symbols: {', '.join(sorted(missing))}")
        self.grammar = grammar
        self.edges: dict[int, list[Segment]] = {}
        for segment in segments:
            self.edges.setdefault(segment.start, []).append(segment)
        self.furthest = _first(segments)
        self._active: set[tuple[str, int]] = set()
        self._memo: dict[tuple[str, int], list[tuple[Node, int, dict]]] = {}

    def symbol(self, symbol: Sym, position: int, env: Env):
        """Yield ``(tree, end position, env)`` for every way of building it here."""
        for node, end, features in self.analyses(symbol.name, position):
            merged = unify(symbol.constraints, features, env)
            if merged is None:
                continue
            yield node, end, merged

    def analyses(self, name: str, position: int) -> list[tuple[Node, int, dict]]:
        """Every constituent of this name starting here, computed once.

        What makes the cache sound is that a production's body is enumerated
        against ``EMPTY`` rather than against the caller's bindings: what a
        symbol can build at a position does not depend on who asked for it, and
        the caller's constraints are applied afterwards, in ``symbol``. So two
        productions that begin with the same symbol — which is what a
        coordination rule and the plain rule beside it are — read one answer
        instead of computing it twice each, and a noun phrase nested n deep
        stops costing 2**n.
        """
        key = (name, position)
        cached = self._memo.get(key)
        if cached is not None:
            return cached
        if key in self._active:
            raise LeftRecursion(
                f"{name} can begin with itself at position {position}; "
                "this parser needs a grammar without left recursion"
            )
        self._active.add(key)
        found: list[tuple[Node, int, dict]] = []
        try:
            for production in self.grammar.for_head(name):
                for children, end, inner in self.body(production.body, position, EMPTY):
                    features = features_of(production, inner)
                    node = Node(
                        label=production.head,
                        children=tuple(children),
                        span=(position, end),
                        features=frozenset(features.items()),
                    )
                    found.append((node, end, features))
        finally:
            self._active.discard(key)
        self._memo[key] = found
        return found

    def body(self, parts: tuple[Part, ...], position: int, env: Env):
        if not parts:
            yield [], position, env
            return
        head, rest = parts[0], parts[1:]
        for tree, next_position, next_env in self.part(head, position, env):
            for tail, end, final in self.body(rest, next_position, next_env):
                yield [tree, *tail], end, final

    def part(self, part: Part, position: int, env: Env):
        if isinstance(part, Word):
            yield from self.terminal(part, position, env)
        else:
            yield from self.symbol(part, position, env)

    def terminal(self, terminal: Word, position: int, env: Env):
        for segment in self.edges.get(position, ()):
            for reading in segment.readings:
                merged = bierze(
                    terminal, reading.tag.pos, reading.lemma, dict(reading.tag.features), env
                )
                if merged is None:
                    continue
                self.furthest = max(self.furthest, segment.end)
                yield Leaf(segment, reading), segment.end, merged


#: Znak, którym streszczenie oddziela modyfikator od tego, do czego doszedł.
#: Bez słowa, bo słowo żądałoby przypadka od tego, co po nim stoi,
#: a stoi tam ciąg wzięty ze zdania i nieodmieniany.
PRZYŁĄCZONY_DO = " → "


def describe(
    node: Node, roles: tuple[str, ...], attaching: str, hosts: tuple[str, ...]
) -> dict[str, str]:
    """Streszczenie czytania: co stoi w której roli i do czego doszedł modyfikator.

    Dwa czytania jednego zdania gdzieś się różnią,
    a streszczenie pokazuje tę różnicę temu, kto ma zdanie poprawić.
    Same role tego nie pokazują,
    bo grupa przyimkowa dochodzi raz do jednej głowy, a raz do drugiej,
    i formy stojące nad nią zostają wtedy te same:
    ``koszt szynki z dodatkami`` jest tym samym dopełnieniem niezależnie od tego,
    czy ``z dodatkami`` doszło do ``koszt``, czy do ``szynki``.
    Rola ``attaching`` dostaje więc obok wypełnienia to, co modyfikator określa.

    Żąda tego jedna rola, bo jedną gramatyka zostawia nierozstrzygniętą rozmyślnie:
    podmiot i dopełnienie rozstrzyga przypadek,
    a pozycje przyłączeniowe stoją po to, żeby dać oba czytania
    (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    Dopisane jest wypełnienie, a nie pozycja obok niego,
    więc ``roles`` zostaje listą ról.
    ``hosts`` wylicza symbole konstytuentów, do których przyłączenie dochodzi,
    i jest deklaracją gramatyki, a nie wiedzą tego wydruku.

    Nazwany jest pierwszy modyfikator czytania i tylko on,
    więc dwa czytania różne miejscem drugiego wychodzą stąd jednym napisem.
    Nazwanie wszystkich wydłuża wiersz, a wierszy jest tyle, ile czytań,
    więc odpowiada na to werdykt nad lasem ze współdzielonymi węzłami,
    a nie ten wydruk:
    docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań.
    """
    summary = {}
    for role in roles:
        found = node.find(role)
        if not found:
            continue
        summary[role] = " ".join(found[0].forms())
        if role == attaching:
            summary[role] += PRZYŁĄCZONY_DO + _attachment(node, found[0], hosts)
    return summary


def _attachment(root: Node, modifier: Node, hosts: tuple[str, ...]) -> str:
    """Co modyfikator określa: konstytuent, do którego doszedł, nazwany tym, co w nim stoi.

    Ani węzeł, pod którym modyfikator stoi bezpośrednio,
    ani najbliższy węzeł z materiałem obok na to pytanie nie odpowiadają:
    okolicznik zdania stoi w drzewie tuż obok dopełnienia, którego nie określa.
    Odpowiada konstytuent nazwany w ``hosts``,
    czyli ten, w którego produkcji to przyłączenie stoi.

    Nazywa go to, co stoi w nim przed modyfikatorem,
    a przy modyfikatorze wysuniętym to, co stoi za nim,
    czyli ciąg wzięty ze zdania, a nie wybór z niego:
    konstytuent bez samych modyfikatorów wychodzi napisem, którego nikt nie napisał,
    bo materiał między dwoma okolicznikami do żadnego z nich nie należy.
    """
    leaves = _leaves(_host(root, modifier, hosts, root))
    start, end = modifier.span
    before = [leaf for leaf in leaves if leaf.span[1] <= start]
    after = [leaf for leaf in leaves if leaf.span[0] >= end]
    return " ".join(leaf.segment.form for leaf in before or after)


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


def _leaves(tree: Tree) -> list[Leaf]:
    """Liście tego konstytuenta, w kolejności, w jakiej stoją w zdaniu."""
    if isinstance(tree, Leaf):
        return [tree]
    return [leaf for child in tree.children for leaf in _leaves(child)]
