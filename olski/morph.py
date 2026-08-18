"""Morphology, over Morfeusz 2.

Morfeusz answers two questions olski needs and a regular expression cannot:
what are this form's possible readings, and what are the features of each. It
also segments, and it segments into a graph rather than a list, because Polish
does not always agree with itself about where one word ends.

Two things about the output matter more than the API:

**A form usually has several readings.** ``ustawienia`` is the genitive singular
or nominative plural of the noun ``ustawienie``, and also two forms of the
gerund of ``ustawić``. Nothing here picks between them. Choosing is the parser's
job, and where the parser cannot choose either, the ambiguity is the answer.

**A tag is a set of feature values, not a string.** ``subst:sg:nom.acc:m3`` says
singular, nominative *or* accusative, inanimate masculine. The dot is a
disjunction, so a feature holds a set and agreement is set intersection. That is
what makes unification the right operation later.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass

import morfeusz2

#: Feature categories, keyed by the values that identify them. Morfeusz tags are
#: positional per part of speech, but every value is unambiguous on its own, so
#: reading them by value avoids a table of positions for each of forty tagsets.
VALUES: dict[str, str] = {}


def _category(name: str, values: str) -> None:
    for value in values.split():
        VALUES[value] = name


_category("number", "sg pl")
_category("case", "nom gen dat acc inst loc voc")
_category("gender", "m1 m2 m3 f n n1 n2 p1 p2 p3")
_category("person", "pri sec ter")
_category("degree", "pos com sup")
_category("aspect", "imperf perf")
_category("negation", "aff neg")
_category("accommodability", "congr rec")
_category("accentability", "akc nakc")
_category("post_prepositionality", "praep npraep")
_category("agglutination", "agl nagl")
_category("vocalicity", "wok nwok")
_category("fullstoppedness", "pun npun")
_category("collectivity", "col ncol pt")

#: The tag Morfeusz gives a form it does not know.
UNKNOWN = "ign"


@dataclass(frozen=True)
class Tag:
    """A part of speech and its features, each feature holding a set of values."""

    pos: str
    features: frozenset[tuple[str, frozenset[str]]] = frozenset()
    raw: str = ""

    @property
    def known(self) -> bool:
        return self.pos != UNKNOWN

    def get(self, feature: str) -> frozenset[str]:
        """Return the values of a feature, or the empty set if it has none."""
        for name, values in self.features:
            if name == feature:
                return values
        return frozenset()

    def has(self, feature: str, value: str) -> bool:
        return value in self.get(feature)

    def __str__(self) -> str:
        return self.raw or self.pos


@dataclass(frozen=True)
class Reading:
    """One way of reading a form: its lemma and its tag."""

    form: str
    lemma: str
    tag: Tag

    def __str__(self) -> str:
        return f"{self.form}:{self.lemma}:{self.tag}"


@dataclass(frozen=True)
class Segment:
    """An edge of the segmentation graph, with every reading of its form.

    ``start`` and ``end`` are node numbers in that graph. A text whose
    segmentation is unambiguous — most of them — produces edges where each
    ``end`` is the next ``start``, and then the graph is a chain.

    They are positions in the graph and not offsets into the text, so nothing
    here can say where in a file a form was found. Morfeusz emits the gaps as
    ``sp`` edges under ``KEEP_WHITESPACES``, which is what walking a path and
    summing form lengths would need; this asks for ``SKIP_WHITESPACES`` because
    the parser wants words.
    """

    start: int
    end: int
    form: str
    readings: tuple[Reading, ...]

    @property
    def known(self) -> bool:
        return any(reading.tag.known for reading in self.readings)

    def with_pos(self, pos: str) -> tuple[Reading, ...]:
        return tuple(r for r in self.readings if r.tag.pos == pos)


def tag(raw: str) -> Tag:
    """Parse a Morfeusz tag string into a part of speech and its features."""
    chunks = raw.split(":")
    pos, rest = chunks[0], chunks[1:]
    features: dict[str, frozenset[str]] = {}
    for chunk in rest:
        if not chunk:
            continue
        values = chunk.split(".")
        category = VALUES.get(values[0])
        if category is None:
            # An unrecognized chunk is kept rather than dropped, under its own
            # name, so that a tagset olski has not met yet stays visible.
            category = f"other:{chunk}"
            features[category] = frozenset({chunk})
            continue
        # Repeated categories are intersected, which is what a tag like
        # nom.acc:acc would mean if Morfeusz ever emitted one.
        merged = frozenset(values)
        if category in features:
            merged = features[category] & merged
        features[category] = merged
    return Tag(pos=pos, features=frozenset(features.items()), raw=raw)


@functools.lru_cache(maxsize=1)
def _analyser() -> morfeusz2.Morfeusz:
    # Morfeusz keeps its dictionary in memory, so one instance is reused. It is
    # asked not to guess at unknown forms: a form olski does not know should
    # come back as ign and be reported, not silently invented.
    return morfeusz2.Morfeusz(
        generate=False, expand_tags=False, whitespace=morfeusz2.SKIP_WHITESPACES
    )


def analyse(text: str) -> list[Segment]:
    """Segment and analyse text, returning the edges of its segmentation graph."""
    edges: dict[tuple[int, int, str], list[Reading]] = {}
    for start, end, interpretation, *_ in _analyser().analyse(text):
        form, lemma, raw = interpretation[0], interpretation[1], interpretation[2]
        # Morfeusz appends a homonym index to some lemmas, as in bieg:s1. The
        # index is appended to a lemma, so what stands in front of the colon is
        # the lemma — except where the lemma is a colon and nothing stands in
        # front of it, and then the whole form is the lemma.
        lemma = lemma.split(":", 1)[0] or lemma
        edges.setdefault((start, end, form), []).append(Reading(form, lemma, tag(raw)))
    return [
        Segment(start=start, end=end, form=form, readings=tuple(readings))
        for (start, end, form), readings in sorted(edges.items())
    ]


def unknown(segments: list[Segment]) -> list[Segment]:
    """Return the segments Morfeusz could not recognize at all."""
    return [segment for segment in segments if not segment.known]
