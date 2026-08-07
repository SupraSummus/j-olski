"""What olski admits, and what it refuses.

The refusals matter more than the acceptances, and there are two kinds of them:
a sentence with no reading is not olski, and a sentence with more than one is not
olski either.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import EMPTY, Grammar, V, nt, unify, word
from olski.morph import analyse
from olski.parse import LeftRecursion, parse
from olski.subset import GRAMMAR, admissible, check, sentences


def verdict(text):
    found = check(text)
    assert len(found) == 1, f"expected one sentence, got {len(found)}"
    return found[0]


# --------------------------------------------------------------------------- #
# Unification, which is where agreement lives
# --------------------------------------------------------------------------- #


def test_unification_intersects_feature_values():
    env = unify(frozenset({("case", V("c"))}), {"case": frozenset({"nom", "acc"})}, EMPTY)
    assert env.get("c") == {"nom", "acc"}
    #  A second use of the same variable narrows it.
    narrowed = unify(frozenset({("case", V("c"))}), {"case": frozenset({"acc"})}, env)
    assert narrowed.get("c") == {"acc"}


def test_unification_fails_when_values_do_not_intersect():
    env = unify(frozenset({("case", V("c"))}), {"case": frozenset({"nom"})}, EMPTY)
    assert unify(frozenset({("case", V("c"))}), {"case": frozenset({"acc"})}, env) is None


def test_a_feature_a_word_does_not_have_cannot_disagree():
    #  An uninflected part of speech is not in violation of an agreement it
    #  takes no part in.
    assert unify(frozenset({("case", V("c"))}), {}, EMPTY) is not None


def test_a_left_recursive_grammar_is_reported_rather_than_looped_on():
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("A"), word("interp")])
    with pytest.raises(LeftRecursion):
        parse(grammar, sentences("plik.")[0])


def test_a_grammar_referring_to_a_symbol_it_never_defines_is_refused():
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("Nieznane")])
    with pytest.raises(ValueError, match="undefined symbols: Nieznane"):
        parse(grammar, sentences("plik.")[0])


# --------------------------------------------------------------------------- #
# Sentences olski accepts
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "text",
    [
        #  An imperative with no subject, which needs none.
        "Zapisz plik.",
        "Program zapisuje ustawienia.",
        #  Pro-drop: the subject is understood, which is ordinary Polish.
        "Zapisuje ustawienia.",
        #  An attributive adjective after its noun, as Polish terminology puts it.
        "Zapisz plik konfiguracyjny.",
        #  OVS resolved by agreement: the singular verb picks the singular noun
        #  as its subject, whatever order they come in.
        "Programy zapisuje ustawienie.",
    ],
)
def test_these_are_olski(text):
    assert verdict(text).status == "valid", verdict(text).explain()


def test_a_valid_sentence_says_what_fills_each_role():
    roles = verdict("Program zapisuje ustawienia.").readings[0]
    assert roles["Subject"] == "Program"
    assert roles["Object"] == "ustawienia"
    assert roles["Verb"] == "zapisuje"


def test_object_first_order_is_polish_and_is_read_that_way():
    #  Free word order is real: here the plural verb forces the plural noun to
    #  be the subject, so the sentence is unambiguous despite the OVS order.
    roles = verdict("Program zapisują ustawienia.").readings[0]
    assert roles["Subject"] == "ustawienia"
    assert roles["Object"] == "Program"


# --------------------------------------------------------------------------- #
# Sentences with no reading
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "text",
    [
        #  Gender disagreement between adjective and noun.
        "Nowa program zapisuje ustawienia.",
        #  The verb is plural and neither noun is.
        "Program zapisują ustawienie.",
        #  A form Morfeusz does not know cannot be given a part of speech.
        "Program zapisuje plikx.",
    ],
)
def test_these_have_no_reading(text):
    assert verdict(text).status == "rejected"


def test_a_rejection_says_how_far_the_analysis_got():
    #  A copula with an instrumental predicate, and coordination, are both
    #  outside the grammar so far, and the failure point says where it stopped.
    result = verdict("Plany są niczym, ale planowanie jest wszystkim.").result
    assert result.rejected
    assert result.furthest == 3


# --------------------------------------------------------------------------- #
# Sentences with more than one reading, which olski refuses just as firmly
# --------------------------------------------------------------------------- #


def test_case_syncretism_plus_free_word_order_makes_a_sentence_ambiguous():
    #  koszt is nominative or accusative and Polish permits both SVO and OVS,
    #  so this sentence does not say which cost is the greater one.
    found = verdict("Koszt samej szynki przewyższa koszt szynki z dodatkami.")
    assert found.status == "ambiguous"
    subjects = {reading["Subject"] for reading in found.readings}
    assert subjects == {"Koszt samej szynki", "koszt szynki z dodatkami"}
    assert "Subject" in found.explain()


@pytest.mark.parametrize(
    "text",
    [
        "Program zapisuje ustawienia w pliku.",
        "Program zapisuje ustawienia w pliku konfiguracyjnym.",
    ],
)
def test_prepositional_attachment_is_reported_as_the_ambiguity_it_is(text):
    #  w pliku attaches to the verb or to the object, and the two readings are
    #  different claims about where the settings are. Nearly every sentence with
    #  a prepositional phrase is ambiguous this way, which is the largest
    #  habitability cost the uniqueness property has run into so far.
    found = verdict(text)
    assert found.status == "ambiguous"
    assert len({reading["Object"] for reading in found.readings}) == 2


def test_readings_differing_only_in_lemma_or_feature_values_are_one_reading():
    #  zapisuje belongs to two homonymous verbs, and ustawienia has several
    #  noun readings. None of that gives a reader anything to choose between,
    #  so the sentence has one reading.
    assert len(verdict("Program zapisuje ustawienia.").result.readings) == 1


# --------------------------------------------------------------------------- #
# Readings the dictionary offers and olski does not take
# --------------------------------------------------------------------------- #


def test_a_preposition_is_not_also_read_as_the_note_of_the_same_name():
    #  Morfeusz reads do as the preposition and as the musical note. The note
    #  inflects for nothing, so unification can never rule it out, and do Włoch
    #  would derive as a noun phrase as well as a prepositional one.
    #  docs/corpus.md counts how much of the corpus that reaches.
    found = verdict("Jedziemy do Włoch.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Modifier"] == "do Włoch"


def test_an_uninflected_noun_stays_where_its_form_is_only_a_noun():
    #  The other half of the exclusion: jury inflects for nothing either, and
    #  nothing else reads it, so it is an ordinary Polish noun and stays.
    assert verdict("Jury ogłasza wyniki.").status == "valid"


def test_an_acronym_keeps_the_noun_reading_the_exclusion_would_take():
    #  PO inflects for nothing, exactly as the note does, and shares its letters
    #  with a preposition. In capitals the noun is what the form is, so this is
    #  where the exclusion has to stop.
    assert verdict("PO ogłasza wyniki.").status == "valid"


def test_excluding_a_reading_never_leaves_a_form_with_none():
    #  A segment with no readings at all is a form Morfeusz does not know, which
    #  is a different verdict and a wrong one here. What spares the segment is
    #  the function-word reading, so that one is always among the survivors.
    unfiltered = analyse("do")[0]
    assert {reading.tag.pos for reading in unfiltered.readings} == {"prep", "subst"}
    assert [reading.tag.pos for reading in admissible(unfiltered).readings] == ["prep"]


# --------------------------------------------------------------------------- #
# Splitting
# --------------------------------------------------------------------------- #


def test_text_splits_into_sentences_at_final_punctuation():
    found = sentences("Zapisz plik. Program zapisuje ustawienia.")
    assert [[segment.form for segment in group] for group in found] == [
        ["Zapisz", "plik", "."],
        ["Program", "zapisuje", "ustawienia", "."],
    ]


def test_every_sentence_of_a_text_is_checked():
    verdicts = check("Zapisz plik. Nowa program zapisuje ustawienia.")
    assert [found.status for found in verdicts] == ["valid", "rejected"]


def test_the_grammar_is_a_grammar_of_something():
    assert len(GRAMMAR) > 5
    assert GRAMMAR.undefined() == frozenset()
