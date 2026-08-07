"""Olski itself: the subset of Polish this grammar admits.

Two properties define it, and both are exclusions rather than inventions:

**Every olski sentence is a well-formed Polish sentence.** No helper notation, no
convenient deviation. What olski leaves out, it leaves out entirely.

**Every olski sentence has exactly one reading.** This is the property doing the
real work. Polish is full of sentences that parse two ways, and a reader resolves
them from context or from knowing what the writer meant. Olski excludes them,
because a sentence with two readings has no checkable meaning and, more
importantly, no reliable one.

The grammar below admits both SVO and OVS, since Polish uses both, which is
precisely why case syncretism makes some sentences ambiguous. The alternative —
declaring that olski is SVO and reading the first noun phrase as the subject —
would make those sentences unambiguous to a reader who knows the convention and
still ambiguous to every other Polish speaker. Rejecting them keeps the promise
that olski is readable as ordinary Polish.

That property is about Polish, and a dictionary offers readings Polish does not,
so the subset excludes readings as well as constructions: see ``admissible``
below.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from olski.grammar import Grammar, V, nt, word
from olski.morph import Segment, analyse
from olski.parse import Result, describe, parse

#: The roles a reading is summarized by when two of them have to be told apart.
ROLES = ("Subject", "Object", "Verb", "Modifier")

#: Sentence-final punctuation. Olski excludes abbreviations, so a full stop is
#: always a sentence boundary and splitting is exact rather than heuristic.
TERMINATORS = frozenset({".", "!", "?"})


def build() -> Grammar:
    grammar = Grammar(start="Sentence")

    grammar.rule("Sentence", [nt("Clause"), word("interp", lemma=".|!|?")])

    # A finite clause, in the two orders Polish actually uses, plus the
    # subjectless form: Zapisz plik has no subject and needs none, and neither
    # does Zapisuje ustawienia.
    grammar.rule(
        "Clause",
        [nt("Subject", number=V("n")), nt("Predicate", number=V("n"), person="ter")],
    )
    grammar.rule(
        "Clause",
        [nt("Object"), nt("Verb", number=V("n"), person="ter"), nt("Subject", number=V("n"))],
    )
    grammar.rule("Clause", [nt("Predicate")])

    # A fronted adjunct. Polish modifies a noun with a prepositional phrase only
    # from behind it, so in front of a clause there is no noun to attach to and
    # the attachment ambiguity docs/subset.md is about cannot arise.
    grammar.rule("Clause", [nt("Modifier"), nt("Clause")])

    grammar.rule("Subject", [nt("NP", case="nom", number=V("n"))], number=V("n"))
    grammar.rule("Object", [nt("NP", case="acc")])

    # A predicate is a verb with what it takes, in the order it takes it.
    for body in ([], [nt("Object")], [nt("Modifier")], [nt("Object"), nt("Modifier")]):
        grammar.rule(
            "Predicate",
            [nt("Verb", number=V("n"), person=V("p")), *body],
            number=V("n"),
            person=V("p"),
        )

    # Finite and imperative verbs, so that a subjectless imperative is a clause
    # while a subjectless indicative is one only through pro-drop.
    grammar.rule(
        "Verb",
        [word("fin", number=V("n"), person=V("p"))],
        number=V("n"),
        person=V("p"),
    )
    grammar.rule(
        "Verb",
        [word("impt", number=V("n"), person=V("p"))],
        number=V("n"),
        person=V("p"),
    )

    # Noun phrases: a noun, an agreeing adjective before it, a genitive
    # modifier after it. Agreement is the unification, not a separate check.
    grammar.rule(
        "NP",
        [word("subst", case=V("c"), number=V("n"), gender=V("g"))],
        case=V("c"),
        number=V("n"),
        gender=V("g"),
    )
    grammar.rule(
        "NP",
        [
            word("adj", case=V("c"), number=V("n"), gender=V("g")),
            nt("NP", case=V("c"), number=V("n"), gender=V("g")),
        ],
        case=V("c"),
        number=V("n"),
        gender=V("g"),
    )
    grammar.rule(
        "NP",
        [
            word("subst", case=V("c"), number=V("n"), gender=V("g")),
            nt("NP", case="gen"),
        ],
        case=V("c"),
        number=V("n"),
        gender=V("g"),
    )
    # Polish puts an attributive adjective after the noun in terminology:
    # plik konfiguracyjny, język polski. Both orders are the language, so both
    # are here, and where a sentence admits both readings it is ambiguous.
    grammar.rule(
        "NP",
        [
            word("subst", case=V("c"), number=V("n"), gender=V("g")),
            word("adj", case=V("c"), number=V("n"), gender=V("g")),
        ],
        case=V("c"),
        number=V("n"),
        gender=V("g"),
    )
    grammar.rule(
        "NP",
        [
            word("subst", case=V("c"), number=V("n"), gender=V("g")),
            nt("Modifier"),
        ],
        case=V("c"),
        number=V("n"),
        gender=V("g"),
    )

    # A preposition governs a case, and the noun phrase has to be in it.
    grammar.rule("Modifier", [word("prep", case=V("c")), nt("NP", case=V("c"))])

    return grammar


GRAMMAR = build()


@dataclass(frozen=True)
class Verdict:
    """What olski says about one sentence."""

    text: str
    result: Result

    @property
    def status(self) -> str:
        if self.result.valid:
            return "valid"
        return "ambiguous" if self.result.ambiguous else "rejected"

    @property
    def readings(self) -> list[dict[str, str]]:
        return [describe(reading, ROLES) for reading in self.result.readings]

    def explain(self) -> str:
        if self.result.valid:
            return "one reading"
        if self.result.rejected:
            return "no reading: nothing in olski derives this"
        summaries = self.readings
        differing = sorted(
            {role for role in ROLES if len({summary.get(role) for summary in summaries}) > 1}
        )
        count = f"{len(summaries)}{'+' if self.result.truncated else ''} readings"
        if not differing:
            return count
        return f"{count}, differing in {', '.join(differing)}"


#: The closed-class parts of speech. A noun reading of a form that also reads as
#: one of these is competing with the reading the form nearly always carries.
CLOSED_CLASS = frozenset({"prep", "conj", "comp", "qub", "part", "pred", "interj"})

#: The seven cases. A noun reading carrying all of them inflects for nothing, so
#: no case demand can fail against it.
EVERY_CASE = frozenset({"nom", "gen", "dat", "acc", "inst", "loc", "voc"})


def _acronym(form: str) -> bool:
    """Whether a form is written the way Polish writes an acronym.

    ``PO``, ``AA`` and ``UP`` inflect for nothing either, and their letters spell
    function words, so the exclusion below would take exactly the reading that is
    right. In capitals the noun is what the form is. One capital says nothing,
    every sentence starting with one.
    """
    return len(form) > 1 and form.isupper()


def admissible(segment: Segment) -> Segment:
    """Drop the noun reading of a form olski reads as a function word.

    Morfeusz reads ``do`` as the preposition and as the musical note, and the
    note inflects for nothing: carrying all seven cases, it satisfies every
    demand unification can make, which is the only filter olski has. So every
    ``do`` in a text hands its sentence a second reading. That is ambiguity in
    the dictionary rather than in Polish, and no parse can tell the two apart,
    so the lexicon rules it out instead. docs/subset.md argues the criterion and
    docs/corpus.md measures what it is worth and what it costs.
    """
    if _acronym(segment.form):
        return segment
    if not any(reading.tag.pos in CLOSED_CLASS for reading in segment.readings):
        return segment
    kept = tuple(
        reading
        for reading in segment.readings
        if not (reading.tag.pos == "subst" and reading.tag.get("case") >= EVERY_CASE)
    )
    if len(kept) == len(segment.readings):
        return segment
    # A closed-class reading is not a noun reading, so the one that spared this
    # segment is itself among the survivors and the tuple is never emptied.
    return replace(segment, readings=kept)


def morphology(text: str) -> list[Segment]:
    """Analyse text as olski reads it: Morfeusz, minus the readings above."""
    return [admissible(segment) for segment in analyse(text)]


def sentences(text: str) -> list[list[Segment]]:
    """Split analysed text into sentences at final punctuation.

    Exact, because olski has no abbreviations: see the abbreviation exclusion in
    the docs. On Polish that does contain them this would be a guess, which is
    the point of excluding them.
    """
    found: list[list[Segment]] = []
    current: list[Segment] = []
    for segment in morphology(text):
        current.append(segment)
        if segment.form in TERMINATORS:
            found.append(current)
            current = []
    if current:
        found.append(current)
    return found


def check(text: str, grammar: Grammar | None = None) -> list[Verdict]:
    """Check every sentence of a text against the grammar."""
    grammar = grammar or GRAMMAR
    verdicts = []
    for segments in sentences(text):
        rendered = " ".join(segment.form for segment in segments)
        verdicts.append(Verdict(text=rendered, result=parse(grammar, segments)))
    return verdicts
