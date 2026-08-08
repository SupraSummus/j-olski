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
from olski.subset import FRAGMENT, GRAMMAR, admissible, check, morphology, sentences


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
        parse(grammar, morphology("plik."))


def test_a_grammar_referring_to_a_symbol_it_never_defines_is_refused():
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("Nieznane")])
    with pytest.raises(ValueError, match="undefined symbols: Nieznane"):
        parse(grammar, morphology("plik."))


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
        #  A modifier in front of the clause, which is the position where a
        #  prepositional phrase has no noun to attach to and so stays out of the
        #  attachment ambiguity the same phrase carries after an object.
        "Pod względem smaku chałka przewyższa zwykłą bułkę.",
        #  In front of the clause whatever order the clause is in, and in front
        #  of a subjectless one too.
        "Pod względem smaku zwykłą bułkę przewyższa chałka.",
        "W pliku zapisuje ustawienia.",
        #  A reflexive verb, which is the form with się after it.
        "Program zapisuje się.",
        #  The copula, with a predicative agreeing with the subject and with a
        #  noun phrase in the instrumental.
        "Ludzie są wolni.",
        "Jan jest nauczycielem.",
        #  A predicative under a verb that is not the copula.
        "Ludzie rodzą się wolni.",
        #  Coordination, of noun phrases and of clauses.
        "Ludzie mają rozum i sumienie.",
        "Program zapisuje ustawienia i program zapisuje dane.",
        #  A modal and its infinitive, agreeing with the subject in gender
        #  because powinien inflects for one and not for person.
        "Ludzie powinni postępować.",
        #  Bezokolicznik pod zwykłym czasownikiem, i łańcuch bezokoliczników,
        #  którego żadna reguła nie opisuje: fraza bezokolicznikowa bierze
        #  dopełnienia, a jest jednym z nich.
        "Program pozwala zapisać ustawienia.",
        "To ma pomagać pisać dobrą polszczyznę.",
        #  A pronoun subject, and with it a person that is not the third.
        "Ja zapisuję plik.",
    ],
)
def test_these_are_olski(text):
    assert verdict(text).status == "valid", verdict(text).explain()


def test_the_first_article_of_the_declaration_is_olski():
    #  The sentence that drove the constructions above into the grammar: a
    #  reflexive verb, a coordinated predicative, a coordinated genitive
    #  modifier, and a quantifier, in one 13-token sentence of ordinary Polish.
    found = verdict(
        "Wszyscy ludzie rodzą się wolni i równi "
        "pod względem swej godności i swych praw."
    )
    assert found.status == "valid", found.explain()
    assert found.readings[0] == {
        "Subject": "Wszyscy ludzie",
        "Predicative": "wolni i równi",
        "Verb": "rodzą się",
        "Modifier": "pod względem swej godności i swych praw",
    }


def test_predykatyw_przed_czasownikiem_nie_jest_czytany_jako_podmiot():
    #  Lustro reguły OVS. Bez niego ten sam szyk wychodził raz tak, a raz wcale,
    #  zależnie od tego, czy po czasowniku stoi dopełnienie, czy orzecznik, a
    #  ryzykiem przy nim jest zamiana ról: podmiot stoi tu za czasownikiem.
    found = verdict("Wejściem jest zwykły tekst polski.")
    assert found.status == "valid", found.explain()
    assert found.readings[0] == {
        "Subject": "zwykły tekst polski",
        "Predicative": "Wejściem",
        "Verb": "jest",
    }


def test_a_valid_sentence_says_what_fills_each_role():
    roles = verdict("Program zapisuje ustawienia.").readings[0]
    assert roles["Subject"] == "Program"
    assert roles["Object"] == "ustawienia"
    assert roles["Verb"] == "zapisuje"


def test_a_fronted_modifier_belongs_to_the_clause_and_not_to_the_subject():
    #  Nothing but the clause rule can take it there, and the failure to guard
    #  against is the subject swallowing it: NPConjunct → subst Modifier makes
    #  the same phrase between the subject and the verb come out valid and wrong.
    roles = verdict("Pod względem smaku chałka przewyższa zwykłą bułkę.").readings[0]
    assert roles["Subject"] == "chałka"
    assert roles["Modifier"] == "Pod względem smaku"


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
        #  The predicative disagrees with the subject in gender.
        "Ludzie są wolna.",
        #  So does the modal, which inflects for gender and not for person.
        "Ludzie powinna postępować.",
        #  A first person subject with a third person verb: person comes from
        #  the subject, so this disagrees the way Nowa program does.
        "Ja zapisuje plik.",
    ],
)
def test_these_have_no_reading(text):
    assert verdict(text).status == "rejected"


def test_coordination_does_not_loosen_agreement_inside_a_conjunct():
    #  The failure to guard against: an adjective scoping over the whole
    #  coordination, which would let a singular feminine one head two masculine
    #  plural nouns. An adjective attaches inside a conjunct, so nowe programy i
    #  pliki is [nowe programy] i [pliki] and the disagreement below has nowhere
    #  to hide.
    assert verdict("Nowa programy i pliki mają nazwy.").status == "rejected"


def test_a_rejection_says_how_far_the_analysis_got():
    #  The copula and the coordination are both in the grammar; the comma
    #  joining two clauses is not, and the failure point is where it stands.
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


def test_the_same_comparison_is_unambiguous_when_the_cases_are_not_syncretic():
    #  Same verb in the same frame as the sentence above, but chałka is
    #  nominative only and bułkę accusative only, so OVS has nowhere to derive:
    #  what that sentence loses, it loses to the syncretism and not to the verb.
    found = verdict("Chałka przewyższa zwykłą bułkę.")
    assert found.status == "valid", found.explain()
    assert found.readings == [
        {"Subject": "Chałka", "Object": "zwykłą bułkę", "Verb": "przewyższa"}
    ]


@pytest.mark.parametrize(
    "text",
    [
        "Program zapisuje ustawienia w pliku.",
        "Program zapisuje ustawienia w pliku konfiguracyjnym.",
        #  Here the phrase cannot be dropped: przewyższać compares along a
        #  dimension, so naming it is what makes the comparison read like Polish.
        "Chałka przewyższa zwykłą bułkę pod względem smaku.",
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


def test_the_second_article_sentence_derives_and_is_still_not_olski():
    #  Everything it needs is in the grammar — verb before subject with a
    #  predicative, a participle with its instrumental complement, a modal, two
    #  coordinations — and what stops it is the attachment problem alone: w
    #  duchu braterstwa is an adjunct of postępować or a modifier of innych.
    found = verdict(
        "Są oni obdarzeni rozumem i sumieniem "
        "i powinni postępować wobec innych w duchu braterstwa."
    )
    assert found.status == "ambiguous"
    assert {reading["Modifier"] for reading in found.readings} == {
        "wobec innych",
        "wobec innych w duchu braterstwa",
    }


def test_a_predicative_that_also_reads_as_an_object_needs_valency_to_settle():
    #  wolny is an adjective and a noun, and być takes no accusative object, so
    #  the object reading is one no reader of the sentence has. Nothing in the
    #  grammar rules it out, because olski has no valency, and this is what the
    #  gap costs: a sentence with one reading in Polish has two here.
    found = verdict("On jest wolny.")
    assert found.status == "ambiguous"
    assert {frozenset(reading) for reading in found.readings} == {
        frozenset({"Subject", "Object", "Verb"}),
        frozenset({"Subject", "Predicative", "Verb"}),
    }


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


def test_tekst_dzieli_się_na_zdania_tak_jak_dzieli_go_linter():
    #  Kropka w docs/linter.md granicą nie jest, a granica akapitu jest, choć
    #  kropki tam nie ma. Jedno i drugie ma olski/document.py i żadnego nie ma
    #  cięcie na każdej kropce, którym ten podział szedł.
    assert sentences("Co działa\n\nCały wywód prowadzi docs/linter.md.") == [
        "Co działa",
        "Cały wywód prowadzi docs/linter.md.",
    ]


def test_werdykt_niesie_zdanie_tak_jak_stoi_a_nie_graf_segmentacji():
    #  Morfeusz dzieli ktoś na kto i ś obok formy całej, więc jest to zdanie,
    #  które wypisywało się jako cztery słowa, choć stoją w nim trzy.
    assert verdict("Ktoś zapisał plik.").text == "Ktoś zapisał plik."


def test_fragment_bez_znaku_zamykajacego_nie_jest_zdaniem_odrzuconym():
    #  Nagłówek i pozycja listy dochodzą do olskiego jako akapity, a produkcja
    #  Sentence żąda na końcu kropki, więc odrzucone mierzyłyby ekstrakcję.
    assert verdict("Zapisywanie pliku").status == FRAGMENT
    assert verdict("Nowa program zapisuje ustawienia.").status == "rejected"


def test_every_sentence_of_a_text_is_checked():
    verdicts = check("Zapisz plik. Nowa program zapisuje ustawienia.")
    assert [found.status for found in verdicts] == ["valid", "rejected"]


def test_the_grammar_is_a_grammar_of_something():
    assert len(GRAMMAR) > 5
    assert GRAMMAR.undefined() == frozenset()
