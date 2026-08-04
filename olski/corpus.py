"""Składnica as test data: real Polish sentences with gold trees.

Składnica is a constituency treebank of Polish, built by parsing sentences drawn
from NKJP with Świgra — Woliński's implementation of Świdziński's GFJP — and
having annotators pick the correct tree out of the resulting forest. That
provenance is what makes it useful here and what limits it, and both halves
matter:

**Useful**, because each file is a whole forest with the gold reading marked
inside it, rather than a single tree. Olski's question is not "is this the tree"
but "does the correct reading survive, alone", and a forest with a marked answer
is exactly what that question needs. The terminals also carry disambiguated
morphology, so the grammar can be measured with the tagger's ambiguity removed
and then again with it restored, and the difference is attributable.

**Limited**, because a treebank made from one grammar's output cannot say how
much Polish a different grammar covers. It says how much of GFJP's analysed
Polish olski agrees with. See docs/corpus.md for what that does and does not
license anyone to claim.

The reader takes the gold tree seriously. A ``chosen`` attribute on a node means
the node appears in some chosen derivation, not that it is in the answer, so the
tree is collected by walking from the root along ``children`` links that are
themselves chosen. On the 2018 release the two agree, but agreeing by accident is
not the same as being right, and the walk is what the format actually specifies.

Nothing here downloads anything. The corpus is 92 MB compressed and 2.4 GB
extracted, it is under a different licence than this repository, and a linter is
not a download manager: docs/corpus.md gives the command.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections.abc import Iterator
from dataclasses import dataclass, replace
from pathlib import Path

from olski.morph import Reading, Segment, tag

#: The annotators' verdict on a forest, and the only one that carries a complete
#: gold tree. The others record why a sentence has none: no correct tree was in
#: the forest, the sentence was too hard to judge, it was not a sentence, it was
#: ungrammatical, or its morphological annotation was wrong.
FULL = "FULL"

#: Składnica names cases in Polish and in Latin interchangeably, sometimes within
#: one valency frame, so both are normalized to the Latin name Morfeusz uses.
CASES = {
    "mian": "nom",
    "dop": "gen",
    "cel": "dat",
    "bier": "acc",
    "narz": "inst",
    "miej": "loc",
    "wol": "voc",
}

#: A required phrase carries the valency slot it fills in an ``f`` of this type,
#: which is how the gold tree says which phrase is the subject. ``accgen`` is the
#: object of a transitive verb: accusative under affirmation, genitive under
#: negation.
SLOT = "tfw"


def _case(name: str) -> str:
    return CASES.get(name, name)


def _slot_role(slot: str) -> str | None:
    """The role a valency slot fills, as olski names its roles.

    Only the two roles olski has. A slot olski has no notion of is not forced
    into one: returning ``None`` keeps an unmapped construction invisible to the
    agreement check rather than silently counted as a disagreement.
    """
    if slot == "subj" or slot.startswith("subj("):
        return "Subject"
    if slot.startswith("np(") and slot.endswith(")"):
        inner = slot[3:-1]
        if _case(inner) == "acc" or inner == "accgen":
            return "Object"
    return None


@dataclass(frozen=True)
class Sentence:
    """One Składnica forest, as much of it as olski has any use for."""

    sent_id: str
    text: str
    verdict: str
    #: The gold terminals, as segments a parser can be run over. Positions are
    #: Składnica's token numbers rather than character offsets, which the parser
    #: does not care about — it treats them as nodes of a segmentation graph —
    #: and which makes spans comparable with the gold tree's.
    segments: tuple[Segment, ...] = ()
    #: Spans of the gold tree's required phrases, by the role they fill. A
    #: sentence with a subordinate clause has more than one subject.
    roles: tuple[tuple[str, int, int], ...] = ()

    @property
    def annotated(self) -> bool:
        """Whether this forest has a complete gold tree."""
        return self.verdict == FULL

    @property
    def tokens(self) -> tuple[str, ...]:
        return tuple(segment.form for segment in self.segments)

    def spans(self, role: str) -> frozenset[tuple[int, int]]:
        return frozenset((start, end) for name, start, end in self.roles if name == role)


def read(path: Path | str) -> Sentence:
    """Read one forest file."""
    path = Path(path)
    try:
        forest = ET.parse(path).getroot()
    except ET.ParseError as error:
        # ParseError carries a line and column and not the file they are in,
        # which is no help at all when the caller is walking twenty thousand
        # files and one of them is broken.
        raise ET.ParseError(f"{path}: {error}") from error
    return parse_forest(forest)


def parse_forest(forest: ET.Element) -> Sentence:
    answer = forest.find("./answer-data/base-answer")
    sentence = Sentence(
        sent_id=forest.get("sent_id", ""),
        text=(forest.findtext("text") or "").strip(),
        verdict=(answer.get("type") if answer is not None else "") or "",
    )
    nodes = {node.get("nid"): node for node in forest.findall("node") if node.get("nid")}
    gold = _gold(nodes)
    if not gold:
        return sentence

    segments = []
    roles = []
    for node in gold:
        span = _span(node)
        if span is None:
            continue
        terminal = node.find("terminal")
        if terminal is not None:
            segments.append(_segment(terminal, span))
            continue
        nonterminal = node.find("nonterminal")
        if nonterminal is None:
            continue
        slot = nonterminal.findtext(f'f[@type="{SLOT}"]')
        role = _slot_role(slot.strip()) if slot else None
        if role is not None:
            roles.append((role, *span))

    segments.sort(key=lambda segment: (segment.start, segment.end))
    return replace(sentence, segments=tuple(segments), roles=tuple(sorted(roles)))


def _gold(nodes: dict[str, ET.Element]) -> list[ET.Element]:
    """The nodes of the chosen tree, from the root down.

    Following chosen ``children`` rather than trusting a node's own ``chosen``
    attribute, which marks participation in some chosen derivation and is true of
    nodes the answer does not use.
    """
    root = _root(nodes)
    if root is None:
        return []
    found: list[ET.Element] = []
    seen: set[str] = set()
    stack = [root]
    while stack:
        node = stack.pop()
        nid = node.get("nid") or ""
        if nid in seen:
            continue
        seen.add(nid)
        found.append(node)
        for children in node.findall("children"):
            if children.get("chosen") != "true":
                continue
            for child in children.findall("child"):
                target = nodes.get(child.get("nid") or "")
                if target is not None:
                    stack.append(target)
            # One chosen expansion per node; a second would be two answers.
            break
    return found


def _root(nodes: dict[str, ET.Element]) -> ET.Element | None:
    root = nodes.get("0")
    if root is not None and root.get("chosen") == "true":
        return root
    # Fall back to the widest chosen node, so a release that numbers nodes
    # differently degrades into a slightly slower search rather than silence.
    chosen = [node for node in nodes.values() if node.get("chosen") == "true"]
    widest = None
    for node in chosen:
        span = _span(node)
        if span is None:
            continue
        if widest is None or span[1] - span[0] > widest[0]:
            widest = (span[1] - span[0], node)
    return widest[1] if widest else None


def _span(node: ET.Element) -> tuple[int, int] | None:
    start, end = node.get("from"), node.get("to")
    if start is None or end is None:
        return None
    try:
        return int(start), int(end)
    except ValueError:
        return None


def _segment(terminal: ET.Element, span: tuple[int, int]) -> Segment:
    form = terminal.findtext("orth") or ""
    lemma = terminal.findtext("base") or form
    raw = (terminal.findtext('f[@type="tag"]') or "").strip()
    return Segment(
        start=span[0],
        end=span[1],
        form=form,
        readings=(Reading(form, lemma, tag(raw)),),
    )


def walk(root: Path | str, verdicts: frozenset[str] | None = None) -> Iterator[Sentence]:
    """Read every forest under a directory, in a stable order.

    ``verdicts`` keeps only the annotators' verdicts named. The default keeps
    everything, because the rejected forests are evidence too: they say what even
    a full-scale grammar of Polish could not analyse.
    """
    for path in sorted(Path(root).rglob("*.xml")):
        sentence = read(path)
        if verdicts is None or sentence.verdict in verdicts:
            yield sentence
