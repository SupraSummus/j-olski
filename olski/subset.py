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

from olski.document import SENTENCE_CLOSE, from_text
from olski.grammar import Grammar, V, nt, word
from olski.morph import Segment, analyse
from olski.parse import Result, describe, parse

#: The roles a reading is summarized by when two of them have to be told apart.
ROLES = ("Subject", "Object", "Predicative", "Verb", "Modifier")

#: Werdykt o tym, czego nikt nie napisał jako zdania: nagłówku, pozycji listy,
#: wierszu tabeli. Odrzucone znaczy „olski tego nie wyprowadza”, a to jest inne
#: zdanie o tekście i inna robota do zrobienia; docs/extraction.md trzyma wywód i
#: mierzy, jak dużą częścią rejestru ta klasa jest.
FRAGMENT = "fragment"

#: The three features a Polish noun or adjective phrase agrees in, as the
#: variables every production sharing them uses. Spelling them out once is what
#: keeps two parts of one phrase demonstrably talking about the same agreement.
AGREE = {"case": V("c"), "number": V("n"), "gender": V("g")}


def build() -> Grammar:
    grammar = Grammar(start="Sentence")

    grammar.rule("Sentence", [nt("Clause"), word("interp", lemma=".|!|?")])

    # Coordination is one conjunct, a conjunction, and the rest, at each of the
    # three levels that have it. X → X conj X would say the same and the parser
    # refuses a left-recursive grammar. Whatever a conjunct may contain is what
    # decides where the coordination can be attached to from outside, which
    # docs/subset.md argues under "Nothing above a coordination distributes into
    # it".
    grammar.rule("Clause", [nt("ClauseConjunct")])
    grammar.rule("Clause", [nt("ClauseConjunct"), word("conj"), nt("Clause")])

    # A finite clause, in the two orders Polish actually uses, plus the
    # subjectless form: Zapisz plik has no subject and needs none, and neither
    # does Zapisuje ustawienia.
    #
    # Person comes from the subject rather than being fixed at ter, which is
    # what admits a first or second person pronoun as one. A noun phrase headed
    # by a noun says person=ter itself, so an imperative still cannot take one.
    grammar.rule(
        "ClauseConjunct",
        [
            nt("Subject", number=V("n"), gender=V("g"), person=V("p")),
            nt("Predicate", number=V("n"), gender=V("g"), person=V("p")),
        ],
    )
    grammar.rule(
        "ClauseConjunct",
        [
            nt("Object"),
            nt("Verb", number=V("n"), person=V("p")),
            nt("Subject", number=V("n"), person=V("p")),
        ],
    )
    grammar.rule("ClauseConjunct", [nt("Predicate")])

    # Verb before subject: Nadchodzi druga rewolucja, Są oni obdarzeni rozumem.
    # The subject takes no complements of its own here, so Zapisuje program
    # ustawienia does not derive and no SVO sentence competes with a
    # verb-initial reading of itself.
    grammar.rule(
        "ClauseConjunct",
        [
            nt("Verb", number=V("n"), person=V("p")),
            nt("Subject", number=V("n"), person=V("p")),
        ],
    )
    grammar.rule(
        "ClauseConjunct",
        [
            nt("Verb", number=V("n"), person=V("p")),
            nt("Subject", number=V("n"), gender=V("g"), person=V("p")),
            nt("Predicative", number=V("n"), gender=V("g")),
        ],
    )

    # Predykatyw przed swoim czasownikiem: Wejściem jest zwykły tekst polski.
    # Lustro reguły OVS, którego predykatyw nie miał, więc ten sam szyk wychodził
    # raz tak, a raz wcale, zależnie od tego, co po czasowniku stoi.
    grammar.rule(
        "ClauseConjunct",
        [
            nt("Predicative", number=V("n"), gender=V("g")),
            nt("Verb", number=V("n"), person=V("p")),
            nt("Subject", number=V("n"), gender=V("g"), person=V("p")),
        ],
    )

    # A fronted adjunct. Polish modifies a noun with a prepositional phrase only
    # from behind it, so in front of a clause there is no noun to attach to and
    # the attachment ambiguity docs/subset.md is about cannot arise.
    grammar.rule("ClauseConjunct", [nt("Modifier"), nt("ClauseConjunct")])

    grammar.rule(
        "Subject",
        [nt("NP", case="nom", number=V("n"), gender=V("g"), person=V("p"))],
        number=V("n"),
        gender=V("g"),
        person=V("p"),
    )
    grammar.rule("Object", [nt("NP", case="acc")])

    # A predicate is a verb with what it takes. What it takes is one symbol
    # rather than a list of bodies, so that the finite verb and the infinitive
    # below share it instead of each carrying its own copy.
    grammar.rule(
        "Predicate",
        [nt("Verb", number=V("n"), person=V("p"))],
        number=V("n"),
        person=V("p"),
    )
    grammar.rule(
        "Predicate",
        [
            nt("Verb", number=V("n"), person=V("p")),
            nt("Complements", number=V("n"), gender=V("g")),
        ],
        number=V("n"),
        person=V("p"),
        gender=V("g"),
    )

    # A modal and its infinitive. Powinien inflects for gender and not for
    # person, so the clause it heads agrees with its subject in gender and
    # leaves person to whatever else constrains it.
    grammar.rule(
        "Predicate",
        [word("winien", number=V("n"), gender=V("g")), nt("InfinitivePhrase")],
        number=V("n"),
        gender=V("g"),
    )
    grammar.rule("InfinitivePhrase", [word("inf")])
    grammar.rule("InfinitivePhrase", [word("inf"), nt("Complements")])

    grammar.rule("Complements", [nt("Object")])
    grammar.rule("Complements", [nt("Adjuncts")])
    grammar.rule("Complements", [nt("Object"), nt("Adjuncts")])
    grammar.rule(
        "Complements",
        [nt("Predicative", number=V("n"), gender=V("g"))],
        number=V("n"),
        gender=V("g"),
    )
    grammar.rule(
        "Complements",
        [nt("Predicative", number=V("n"), gender=V("g")), nt("Adjuncts")],
        number=V("n"),
        gender=V("g"),
    )
    # Bezokolicznik jest tym, co czasownik bierze, tak jak dopełnienie: Linter
    # pomaga pisać dobry kod. Łańcuch nie potrzebuje własnej reguły, bo
    # InfinitivePhrase → inf Complements wraca tutaj i ma pomagać pisać wychodzi
    # z tych dwóch produkcji.
    grammar.rule("Complements", [nt("InfinitivePhrase")])

    # More than one adjunct, because postępować wobec innych w duchu braterstwa
    # has two and a verb that takes one of them takes any number.
    grammar.rule("Adjuncts", [nt("Modifier")])
    grammar.rule("Adjuncts", [nt("Modifier"), nt("Adjuncts")])

    # What is predicated of the subject: an adjective phrase agreeing with it,
    # or a noun phrase in the instrumental. Both are what być takes, and the
    # first is also what rodzą się wolni i równi predicates without one.
    grammar.rule(
        "Predicative",
        [nt("AP", case="nom", number=V("n"), gender=V("g"))],
        number=V("n"),
        gender=V("g"),
    )
    grammar.rule("Predicative", [nt("NP", case="inst")])

    # Finite and imperative verbs in one production, since they differ in the
    # features their tags carry and in nothing this rule says. A reflexive verb
    # is the form with się after it: the particle can stand elsewhere in Polish,
    # and olski takes only the adjacent position.
    grammar.rule(
        "Verb",
        [word("fin|impt", number=V("n"), person=V("p"))],
        number=V("n"),
        person=V("p"),
    )
    grammar.rule(
        "Verb",
        [word("fin|impt", number=V("n"), person=V("p")), word("part", lemma="się")],
        number=V("n"),
        person=V("p"),
    )

    grammar.rule(
        "NP",
        [nt("NPConjunct", person=V("p"), **AGREE)],
        person=V("p"),
        **AGREE,
    )
    # A coordination of noun phrases is plural and third person whatever its
    # conjuncts are, and it carries no gender: Polish resolves the gender of
    # rozum i sumienie by rules unification cannot state, and a feature a phrase
    # does not carry is one no agreement can fail against.
    grammar.rule(
        "NP",
        [nt("NPConjunct", case=V("c")), word("conj"), nt("NP", case=V("c"))],
        case=V("c"),
        number="pl",
        person="ter",
    )

    # Noun phrases: a noun, an agreeing adjective before it, a genitive
    # modifier after it. Agreement is the unification, not a separate check,
    # and every one of these shares the same three variables, so they are named
    # once. A conjunct headed by a noun is third person by saying so; leaving
    # that off one of them would quietly let a first person verb take it.
    grammar.rule(
        "NPConjunct", [word("subst", **AGREE)], person="ter", **AGREE
    )
    grammar.rule(
        "NPConjunct", [word("adj", **AGREE), nt("NPConjunct", **AGREE)], person="ter", **AGREE
    )
    grammar.rule(
        "NPConjunct", [word("subst", **AGREE), nt("NP", case="gen")], person="ter", **AGREE
    )
    # Polish puts an attributive adjective after the noun in terminology:
    # plik konfiguracyjny, język polski. Both orders are the language, so both
    # are here, and where a sentence admits both readings it is ambiguous.
    grammar.rule(
        "NPConjunct", [word("subst", **AGREE), word("adj", **AGREE)], person="ter", **AGREE
    )
    grammar.rule(
        "NPConjunct", [word("subst", **AGREE), nt("Modifier")], person="ter", **AGREE
    )
    # A pronoun is the one conjunct that carries its own person, which is the
    # whole reason it is here: without one, first and second person subjects
    # have no noun phrase to be.
    grammar.rule(
        "NPConjunct",
        [word("ppron3|ppron12", person=V("p"), **AGREE)],
        person=V("p"),
        **AGREE,
    )

    # Adjective phrases, coordinated the same way and agreeing throughout, so
    # that wolni i równi is one predicative and wolna i równi is none.
    grammar.rule("AP", [nt("APConjunct", **AGREE)], **AGREE)
    grammar.rule(
        "AP", [nt("APConjunct", **AGREE), word("conj"), nt("AP", **AGREE)], **AGREE
    )
    # A passive participle is an adjective for these purposes, and it keeps the
    # complement its verb governed: obdarzeni rozumem i sumieniem.
    grammar.rule("APConjunct", [word("adj|ppas", **AGREE)], **AGREE)
    grammar.rule(
        "APConjunct", [word("adj|ppas", **AGREE), nt("NP", case="inst")], **AGREE
    )

    # A preposition governs a case, and the noun phrase has to be in it.
    grammar.rule("Modifier", [word("prep", case=V("c")), nt("NP", case=V("c"))])

    return grammar


GRAMMAR = build()


@dataclass(frozen=True)
class Verdict:
    """What olski says about one sentence."""

    #: Zdanie tak, jak stoi w tekście. Segmenty są krawędziami grafu, a nie
    #: listą, więc sklejone dają naraz każdy podział, jaki Morfeusz na formie
    #: widzi: ``ktoś`` wychodzi wtedy jako ``kto ktoś ś``.
    text: str
    result: Result

    @property
    def status(self) -> str:
        if not SENTENCE_CLOSE.search(self.text):
            return FRAGMENT
        return self.result.status

    @property
    def readings(self) -> list[dict[str, str]]:
        return [describe(reading, ROLES) for reading in self.result.readings]

    def explain(self) -> str:
        if self.status == FRAGMENT:
            return "not a sentence: nothing punctuates it as one"
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


def sentences(text: str) -> list[str]:
    """Tnie tekst na zdania i oddaje je tak, jak stoją.

    Podział jest ten, którym idzie linter, czyli :mod:`olski.document`: żąda po
    kropce białego znaku i zna skróty. Sam olski skrótów nie ma, więc nad nim
    cięcie na każdej kropce byłoby dokładne. Wejściem jest jednak dokumentacja,
    gdzie ``docs/linter.md`` jest jednym słowem, a cięcie na kropce w jego środku
    wymyśla dwa zdania, których nikt nie napisał.

    Cięcie stoi więc przed analizą, a nie po niej. Morfeusz jest wołany z
    ``SKIP_WHITESPACES``, a segment niesie numery węzłów grafu zamiast przesunięć
    w tekście, więc po analizie nie ma już czym zobaczyć spacji, która odróżnia
    granicę zdania od nazwy pliku.
    """
    document = from_text(text)
    return [document.slice(span) for span in document.sentences]


def check(text: str, grammar: Grammar | None = None) -> list[Verdict]:
    """Check every sentence of a text against the grammar."""
    grammar = grammar or GRAMMAR
    return [
        Verdict(text=sentence, result=parse(grammar, morphology(sentence)))
        for sentence in sentences(text)
    ]
