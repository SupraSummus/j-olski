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
structure with the same word readings are one reading. The distinction is not
pedantic: it is exactly the mistake recorded in
docs/glr-in-practice.md#ambiguity-as-a-confidence-measure, where a system fell
silent on lines it had understood perfectly because it counted attempts instead
of outcomes.

Implementation note. This is a memoizing top-down enumerator over the
segmentation graph, which is enough for a grammar without left recursion and
detects the case it cannot handle rather than looping. When the grammar needs
left recursion — or when enumerating readings costs more than counting them — it
gets replaced by a chart parser with a packed forest, which is what
docs/design-notes.md has always assumed.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from olski.grammar import EMPTY, Env, Grammar, Part, Sym, Word, features_of, unify
from olski.morph import Reading, Segment

#: Enumeration is capped, because an ambiguous sentence can have very many
#: derivations and the answer past the second one is always the same: too many.
MAX_READINGS = 64

#: What makes two readings the same reading.
#:
#: Olski's uniqueness property is about structure: who is the subject, what the
#: object is, where a modifier attaches, and what part of speech each word is
#: being taken as. All of that shows up in the tree — role assignment in the node
#: labels, attachment in the spans — so a reading is identified by its shape and
#: its parts of speech, and by nothing else.
#:
#: Deliberately excluded: feature values and lemmas. Agreement has already been
#: enforced by unification, so whether a phrase settled on neuter plural or
#: masculine singular does not give a reader two things to choose between. And a
#: form that belongs to two homonymous lemmas is one sentence, not two: Polish
#: forms are homonymous everywhere, so counting those would reject nearly all of
#: it. Lexical ambiguity is the reader's to resolve; structural ambiguity is what
#: leaves a sentence saying two things at once.


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
        return (self.segment.start, self.segment.end, self.reading.tag.pos)

    def forms(self) -> list[str]:
        return [self.segment.form]


@dataclass(frozen=True)
class Node:
    label: str
    children: tuple[Leaf | Node, ...]
    features: frozenset[tuple[str, frozenset[str]]] = frozenset()

    @property
    def span(self) -> tuple[int, int]:
        return (self.children[0].span[0], self.children[-1].span[1])

    def signature(self):
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


def parse(grammar: Grammar, segments: list[Segment], start: str | None = None) -> Result:
    """Enumerate the distinct readings of a segmented sentence."""
    missing = grammar.undefined()
    if missing:
        raise ValueError(f"grammar refers to undefined symbols: {', '.join(sorted(missing))}")

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


def _first(segments: list[Segment]) -> int:
    return min((segment.start for segment in segments), default=0)


class _Parser:
    def __init__(self, grammar: Grammar, segments: list[Segment]) -> None:
        self.grammar = grammar
        self.edges: dict[int, list[Segment]] = {}
        for segment in segments:
            self.edges.setdefault(segment.start, []).append(segment)
        self.furthest = _first(segments)
        self._active: set[tuple[str, int]] = set()

    def symbol(self, symbol: Sym, position: int, env: Env):
        """Yield ``(tree, end position, env)`` for every way of building it here."""
        key = (symbol.name, position)
        if key in self._active:
            raise LeftRecursion(
                f"{symbol.name} can begin with itself at position {position}; "
                "this parser needs a grammar without left recursion"
            )
        self._active.add(key)
        try:
            for production in self.grammar.for_head(symbol.name):
                for children, end, inner in self.body(production.body, position, EMPTY):
                    features = features_of(production, inner)
                    merged = unify(symbol.constraints, features, env)
                    if merged is None:
                        continue
                    node = Node(
                        label=production.head,
                        children=tuple(children),
                        features=frozenset(features.items()),
                    )
                    yield node, end, merged
        finally:
            self._active.discard(key)

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
                if reading.tag.pos not in terminal.pos:
                    continue
                if terminal.lemmas is not None and reading.lemma not in terminal.lemmas:
                    continue
                features = {name: values for name, values in reading.tag.features}
                merged = unify(terminal.constraints, features, env)
                if merged is None:
                    continue
                self.furthest = max(self.furthest, segment.end)
                yield Leaf(segment, reading), segment.end, merged


def describe(node: Node, roles: tuple[str, ...]) -> dict[str, str]:
    """Summarize a reading by what fills each named role, for reporting.

    Two readings of the same sentence differ somewhere, and this is how the
    difference gets shown to whoever has to fix it.
    """
    summary = {}
    for role in roles:
        found = node.find(role)
        if found:
            summary[role] = " ".join(found[0].forms())
    return summary
