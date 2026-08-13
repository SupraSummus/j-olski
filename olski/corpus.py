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
morphology, so the grammar can be measured with the analyser's ambiguity removed
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
extracted, it is under a different licence than this repository, and a parser is
not a download manager: docs/corpus.md gives the command.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
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

#: Znaczniki Składnicy są znacznikami NKJP, a gramatyka stoi nad Morfeuszem 2,
#: więc czytelnik przekłada nazwy części mowy tak samo, jak przekłada nazwy
#: przypadków wyżej i z tego samego powodu: terminal ma pytać o jedną nazwę.
#:
#: Cztery nazwy, bo tyle rozdziela te dwa zbiory nad tym korpusem. NKJP wydziela
#: zaimki jako osobne części mowy, a Morfeusz trzyma je pod rzeczownikiem,
#: przymiotnikiem i przysłówkiem — ``który`` jest tam ``adj``, a ``tym``
#: ``subst`` — i osobno nazywa kublik cząstką.
#:
#: Bez tego przekładu produkcja, która taką formę bierze, nie strzela nad złotą
#: morfologią ani razu, a wiersz blokerów nazywa nazwę znacznika tam, gdzie
#: gramatyka konstrukcję ma; docs/corpus.md mierzy, ile to było warte.
CZĘŚCI_MOWY = {
    "qub": "part",
    "psubst": "subst",
    "padj": "adj",
    "padv": "adv",
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


#: Węzeł, którego żadne wybrane wyprowadzenie nie używa.
#:
#: Plik trzyma cały las, a odpowiedź jest w nim jednym drzewem, więc budowa
#: drzewa XML idzie w większości pod węzły, których odpowiedź nie bierze, i to
#: ona, a nie gramatyka za nią, jest tym, na czym przebieg nad bankiem drzew
#: stoi — profil przebiegu to pokazuje. Tekst tych węzłów znika więc, zanim `ET`
#: go zobaczy.
#:
#: Wolno je wyciąć, bo `_gold` schodzi z korzenia po wybranych dowiązaniach
#: ``children``, a węzeł, którego ``chosen`` przeczy, nie wchodzi w żadne wybrane
#: wyprowadzenie. Tak to znaczy format, i na tym to stoi, bo nic tutaj tego nie
#: sprawdza: wydanie, które by temu przeczyło, zabrałoby zdaniu token, nie
#: mówiąc nic. Węzeł bez tej flagi zostaje — zejście idzie po dowiązaniach, a nie
#: po flagach — i Składnica takie węzły pisze.
NIEWYBRANY = re.compile(rb'<node[^>]*chosen="false"[^>]*>.*?</node>\s*', re.DOTALL)


def read(path: Path | str) -> Sentence:
    """Read one forest file."""
    return parse_forest(read_forest(path))


def read_forest(path: Path | str) -> ET.Element:
    """Jeden las, bez węzłów, których wybrane wyprowadzenie nie bierze."""
    path = Path(path)
    try:
        return ET.fromstring(NIEWYBRANY.sub(b"", path.read_bytes()))
    except ET.ParseError as error:
        # ParseError carries a line and column and not the file they are in,
        # which is no help at all when the caller is walking twenty thousand
        # files and one of them is broken.
        raise ET.ParseError(f"{path}: {error}") from error


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
    for node, _ in gold:
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


@dataclass(frozen=True)
class Constituent:
    """Nieterminal wybranego drzewa: kategoria, rozpiętość i to, pod czym stoi.

    Rodzic jest tu polem, a nie listą dzieci, bo pytanie, dla którego to jest
    czytane, biegnie w tę stronę: fraza pyta, do czego doszła.
    """

    category: str
    start: int
    end: int
    parent: Constituent | None = None


def constituents(forest: ET.Element) -> list[Constituent]:
    """Nieterminale wybranego drzewa, rodzic przed dzieckiem.

    Terminale zostają na zewnątrz: co niosą, trzyma :class:`Sentence`, a tu
    liczy się kształt drzewa nad nimi. ``olski/attachment.py`` jest tym, co o ten
    kształt pyta.
    """
    nodes = {node.get("nid"): node for node in forest.findall("node") if node.get("nid")}
    zbudowane: dict[str, Constituent] = {}
    found = []
    for node, parent in _gold(nodes):
        span = _span(node)
        nonterminal = node.find("nonterminal")
        if span is None or nonterminal is None:
            continue
        constituent = Constituent(
            category=(nonterminal.findtext("category") or "").strip(),
            start=span[0],
            end=span[1],
            parent=zbudowane.get(parent.get("nid") or "") if parent is not None else None,
        )
        zbudowane[node.get("nid") or ""] = constituent
        found.append(constituent)
    return found


def _gold(nodes: dict[str, ET.Element]) -> list[tuple[ET.Element, ET.Element | None]]:
    """The nodes of the chosen tree, from the root down, each with its parent.

    Following chosen ``children`` rather than trusting a node's own ``chosen``
    attribute, which marks participation in some chosen derivation and is true of
    nodes the answer does not use.

    Rodzic jest tym, po co drzewo się schodzi, a nie zbiera:
    ``fpm`` pod ``fno`` i ``fpm`` pod ``zdanie`` to ten sam węzeł
    i dopiero to, pod czym stoi, mówi, dokąd wyrażenie doszło.
    Wychodzi stąd w porządku, w którym rodzic stoi przed dzieckiem,
    bo zejście zaczyna się od korzenia.
    """
    root = _root(nodes)
    if root is None:
        return []
    found: list[tuple[ET.Element, ET.Element | None]] = []
    seen: set[str] = set()
    stack = [(root, None)]
    while stack:
        node, parent = stack.pop()
        nid = node.get("nid") or ""
        if nid in seen:
            continue
        seen.add(nid)
        found.append((node, parent))
        for children in node.findall("children"):
            if children.get("chosen") != "true":
                continue
            for child in children.findall("child"):
                target = nodes.get(child.get("nid") or "")
                if target is not None:
                    stack.append((target, node))
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


def _znacznik(raw: str) -> str:
    """Znacznik NKJP nazwany tak, jak nazywa tę część mowy Morfeusz.

    Przekładana jest sama nazwa części mowy, bo tylko ona się rozchodzi: wartości
    cech oba zbiory piszą tak samo. Nazwa z pliku nie zostaje obok przełożonej,
    bo znacznik pół przełożony mówiłby o formie dwie rzeczy naraz, a wydruk
    czyta ``raw``.
    """
    pos, dwukropek, reszta = raw.partition(":")
    return f"{CZĘŚCI_MOWY.get(pos, pos)}{dwukropek}{reszta}"


def _segment(terminal: ET.Element, span: tuple[int, int]) -> Segment:
    form = terminal.findtext("orth") or ""
    lemma = terminal.findtext("base") or form
    raw = _znacznik((terminal.findtext('f[@type="tag"]') or "").strip())
    return Segment(
        start=span[0],
        end=span[1],
        form=form,
        readings=(Reading(form, lemma, tag(raw)),),
    )


def pliki(root: Path | str) -> list[Path]:
    """Lasy pod katalogiem, w stałym porządku.

    Lista, a nie czytanie po kolei, bo pulę procesów w `olski/coverage.py` dzieli
    się właśnie na niej, a czyta się już w procesach roboczych. Porządek jest
    stały, bo na nim stoi to, że kawałki scalają się w wydruk jednego przebiegu.
    """
    return sorted(Path(root).rglob("*.xml"))
