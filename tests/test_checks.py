import pytest

from olski.checks import CHECKS, Abstain, Hit
from olski.document import Document, from_text
from olski.rules import Pack, RuleError

# Rules under test are declared here rather than taken from the shipped pack, so
# that a threshold change in the pack cannot quietly break a check's test.
pack = Pack(name="test", origin="tests/test_checks.py")


def over(rule, documents):
    return list(CHECKS[rule.check].run(rule, documents))


def run(rule, text):
    document = text if isinstance(text, Document) else from_text(text)
    return over(rule, [document])


def hits(rule, text):
    return [outcome for outcome in run(rule, text) if isinstance(outcome, Hit)]


def corpus(*texts):
    """A corpus whose files are named after their position, so that a finding's
    document can be named in an assertion."""
    return [from_text(text, f"{n}.txt") for n, text in enumerate(texts, start=1)]


# --------------------------------------------------------------------------- #
# pattern
# --------------------------------------------------------------------------- #

straight_quote = pack.rule(
    id="test-straight-quote",
    check="pattern",
    params=dict(pattern=r'"'),
    message="straight quote {match}",
    justification="a test",
)

boosters = pack.rule(
    id="test-unless",
    check="pattern",
    params=dict(pattern=r"kluczow\w+", unless_followed_by=r" element układanki"),
    message="booster {match}",
    justification="a test",
)


def test_pattern_reports_every_match_with_a_position():
    found = hits(straight_quote, 'Powiedział "tak" i wyszedł.')
    assert [h.span.start for h in found] == [11, 15]
    assert found[0].fields == {"match": '"'}


def test_pattern_is_quiet_on_clean_text():
    assert hits(straight_quote, "Powiedział „tak” i wyszedł.") == []


def test_unless_followed_by_exempts_a_legitimate_use():
    assert len(hits(boosters, "To kluczowy moment.")) == 1
    assert hits(boosters, "To kluczowy element układanki.") == []


abbreviated = pack.rule(
    id="test-unless-preceded-by",
    check="pattern",
    params=dict(pattern=r"\.(?=[A-Z])", unless_preceded_by=r"\b(?:np|itd)"),
    message="run-together {match}",
    justification="a test",
)


def test_unless_preceded_by_exempts_what_comes_before_the_match():
    assert len(hits(abbreviated, "Zapisz plik.Potem zamknij.")) == 1
    assert hits(abbreviated, "Sprawdź np.Zapisz w menu.") == []
    #  Anchored to the match, so the same word earlier in the text does not exempt.
    assert len(hits(abbreviated, "Sprawdź np. w menu. Zapisz plik.Potem zamknij.")) == 1


# --------------------------------------------------------------------------- #
# pattern-density
# --------------------------------------------------------------------------- #

dashes = pack.rule(
    id="test-dash-density",
    check="pattern-density",
    params=dict(pattern=r"—", unit="document", max_per_1000_words=100, min_count=2),
    message="{count} in {words} words, {rate} per 1000 over {limit}",
    justification="a test",
)

per_paragraph = pack.rule(
    id="test-paragraph-density",
    check="pattern-density",
    params=dict(pattern=r"—", unit="paragraph", max_per_1000_words=100, min_count=1),
    message="{count} dashes here",
    justification="a test",
)

floored = pack.rule(
    id="test-density-floor",
    check="pattern-density",
    params=dict(pattern=r"—", unit="document", max_per_1000_words=1, min_count=1, min_words=20),
    message="{count} dashes",
    justification="a test",
)


def test_density_fires_only_above_the_rate():
    #  Ten words, two dashes: 200 per 1000, over the limit of 100.
    over = "raz dwa trzy — cztery pięć sześć siedem — osiem dziewięć dziesięć"
    assert len(hits(dashes, over)) == 1
    # The same two dashes spread over enough words to come in under it.
    under = over + " " + " ".join(["słowo"] * 15)
    assert hits(dashes, under) == []


def test_density_reports_the_measurement_it_used():
    found = hits(dashes, "raz dwa trzy — cztery pięć sześć siedem — osiem dziewięć dziesięć")
    assert found[0].fields["count"] == 2
    assert found[0].fields["words"] == 10
    assert found[0].fields["rate"] == "200.0"
    assert found[0].fields["limit"] == "100"


def test_density_points_at_the_first_occurrence_in_the_unit():
    text = "raz dwa trzy — cztery pięć sześć siedem — osiem dziewięć dziesięć"
    assert hits(dashes, text)[0].span.start == text.index("—")


def test_min_count_keeps_a_single_occurrence_quiet():
    assert hits(dashes, "raz — dwa") == []


def test_paragraph_unit_measures_each_paragraph_separately():
    text = "raz — dwa trzy\n\n" + " ".join(["słowo"] * 40) + " — koniec"
    found = hits(per_paragraph, text)
    assert len(found) == 1
    assert found[0].span.start == text.index("—")


per_sentence = pack.rule(
    id="test-sentence-density",
    check="pattern-density",
    params=dict(pattern=r"—", unit="sentence", max_per_1000_words=100, min_count=1),
    message="{count} dashes in this sentence",
    justification="a test",
)


def test_sentence_unit_measures_each_sentence_separately():
    #  The first sentence is short enough for one dash to run over the rate, the
    #  second long enough for one to come in under it. A document-wide rate would
    #  average them and find nothing.
    text = "Raz — dwa trzy. " + " ".join(["Słowo"] + ["słowo"] * 40) + " — koniec."
    found = hits(per_sentence, text)
    assert len(found) == 1
    assert found[0].span.start == text.index("—")


def test_density_abstains_rather_than_measure_a_rate_over_too_few_words():
    outcomes = run(floored, "raz — dwa")
    assert [type(o) for o in outcomes] == [Abstain]
    assert "too short" in outcomes[0].reason


# --------------------------------------------------------------------------- #
# The corpus scope: rules that measure a body of text rather than a file.
# --------------------------------------------------------------------------- #

over_corpus = pack.rule(
    id="test-corpus-density",
    check="pattern-density",
    params=dict(pattern=r"—", unit="corpus", max_per_1000_words=100, min_count=2),
    message="{count} in {words} words, {rate} per 1000",
    justification="a test",
)


def test_a_corpus_rate_pools_every_document_rather_than_taking_the_first():
    #  One dash in each of two five-word files: 200 per 1000 either way, but the
    #  denominator is only right if both files were counted.
    found = over(over_corpus, corpus("raz dwa — trzy cztery", "pięć sześć — siedem osiem"))
    assert len(found) == 1
    assert found[0].fields["count"] == 2
    assert found[0].fields["words"] == 8


def test_a_corpus_rate_is_one_finding_anchored_in_the_file_it_first_occurs_in():
    found = over(over_corpus, corpus("bez znaku", "raz — dwa — trzy"))
    assert len(found) == 1
    assert found[0].document.path == "2.txt"


def test_a_per_document_rule_still_names_the_file_each_finding_is_in():
    found = over(straight_quote, corpus('pierwsze "x"', 'drugie "y"'))
    assert [h.document.path for h in found] == ["1.txt", "1.txt", "2.txt", "2.txt"]


corpus_floor = pack.rule(
    id="test-corpus-floor",
    check="pattern-density",
    params=dict(pattern=r"—", unit="corpus", max_per_1000_words=1, min_count=1, min_words=50),
    message="{count} dashes",
    justification="a test",
)


def test_a_corpus_abstention_belongs_to_no_single_file():
    outcomes = over(corpus_floor, corpus("raz — dwa", "trzy — cztery"))
    assert [type(o) for o in outcomes] == [Abstain]
    assert outcomes[0].document is None


# --------------------------------------------------------------------------- #
# entity-recurrence
# --------------------------------------------------------------------------- #

walk_ons = pack.rule(
    id="test-walk-on",
    check="entity-recurrence",
    params=dict(
        introduce=r"\b([A-ZĄĆĘŁŃÓŚŹŻ]\w+) \([^)]*\d[^)]*\)",
        min_mentions=3,
        max_walk_on_share=0.5,
    ),
    message="{walk_ons} of {introductions} ({share}, over {limit}); {entity} is named {mentions}",
    justification="a test",
)

DROPPED = "Nara (fizyczka, 31) sprawdziła czujnik.\n"
KEPT = (
    "Rho (technik, 44) sprawdził wyrzutnię.\n"
    "Rho czekał do rana.\n"
    "Potem Rho wrócił do pracy.\n"
)


def test_entity_recurrence_fires_only_above_the_share():
    #  Three walk-ons in four introductions is 75%, over the limit of 50%.
    assert len(over(walk_ons, corpus(DROPPED, DROPPED, DROPPED, KEPT))) == 1
    #  One in three comes in under it.
    assert over(walk_ons, corpus(DROPPED, KEPT, KEPT)) == []


def test_entity_recurrence_reports_the_measurement_it_used():
    found = over(walk_ons, corpus(DROPPED, DROPPED, DROPPED, KEPT))
    assert found[0].fields["walk_ons"] == 3
    assert found[0].fields["introductions"] == 4
    assert found[0].fields["share"] == "75%"
    #  Named once, and the once is the introduction.
    assert found[0].fields["entity"] == "Nara"
    assert found[0].fields["mentions"] == 1


def test_one_entity_introduced_twice_in_a_file_is_one_introduction():
    #  Counting introductions rather than entities would double the denominator,
    #  so the share would improve every time a text reintroduced someone.
    found = over(walk_ons, corpus(DROPPED + DROPPED, DROPPED, KEPT))
    assert found[0].fields["introductions"] == 3


floored_recurrence = pack.rule(
    id="test-walk-on-floor",
    check="entity-recurrence",
    params=dict(
        introduce=r"\b([A-ZĄĆĘŁŃÓŚŹŻ]\w+) \([^)]*\d[^)]*\)",
        max_walk_on_share=0.1,
        min_introductions=20,
    ),
    message="{share} walk-ons",
    justification="a test",
)


def test_entity_recurrence_abstains_rather_than_share_a_handful():
    outcomes = over(floored_recurrence, corpus(DROPPED, DROPPED))
    assert [type(o) for o in outcomes] == [Abstain]
    assert "too few" in outcomes[0].reason
    assert outcomes[0].document is None


# --------------------------------------------------------------------------- #
# line-end-word
# --------------------------------------------------------------------------- #

orphans = pack.rule(
    id="test-orphan",
    check="line-end-word",
    params=dict(words=["a", "i", "w", "z"]),
    message="orphan {word}",
    justification="a test",
)


def test_line_end_word_flags_a_single_letter_at_a_line_end():
    found = hits(orphans, "Zapisano to w\npliku tekstowym.\n")
    assert [h.fields["word"] for h in found] == ["w"]


def test_line_end_word_ignores_the_same_letter_mid_line():
    assert hits(orphans, "Zapisano to w pliku\ntekstowym.\n") == []


def test_line_end_word_is_case_insensitive_by_default():
    found = hits(orphans, "Zdanie kończy się na W\nnowej linii.")
    assert [h.fields["word"] for h in found] == ["W"]


def test_line_end_word_looks_past_trailing_punctuation():
    assert len(hits(orphans, "Wybór między a,\nb oraz c.")) == 1


def test_line_end_word_abstains_when_line_breaks_are_soft():
    reflowed = Document(path="reflowed", text="Zapisano to w\npliku.\n", line_breaks="soft")
    outcomes = run(orphans, reflowed)
    assert [type(o) for o in outcomes] == [Abstain]
    assert "soft" in outcomes[0].reason


# --------------------------------------------------------------------------- #
# length-variation
# --------------------------------------------------------------------------- #

monotony = pack.rule(
    id="test-monotony",
    check="length-variation",
    params=dict(unit="sentence", min_variation=0.3),
    message="{count} {unit}s vary by {variation}, {side} {limit}",
    justification="a test",
)

erratic = pack.rule(
    id="test-erratic",
    check="length-variation",
    params=dict(unit="sentence", max_variation=0.3),
    message="{variation} is {side} {limit}",
    justification="a test",
)

floored_variation = pack.rule(
    id="test-variation-floor",
    check="length-variation",
    params=dict(unit="sentence", min_variation=0.3, min_units=4),
    message="{variation}",
    justification="a test",
)

#  Four sentences of four words each: a spread of exactly nothing.
UNIFORM = (
    "Program zapisuje twoje ustawienia. Plik zawiera cztery opcje. "
    "Katalog trzyma dwa pliki. Serwer czyta ten katalog."
)

VARIED = (
    "Zapisz plik. Program zapisuje twoje ustawienia w katalogu domowym, "
    "a potem zamyka okno i czeka na następne polecenie. Gotowe."
)


@pytest.mark.parametrize(
    ("rule", "text", "side"),
    [
        (monotony, UNIFORM, "below"),
        (monotony, VARIED, None),
        (erratic, UNIFORM, None),
        (erratic, VARIED, "above"),
    ],
    ids=["floor-fires", "floor-quiet", "ceiling-quiet", "ceiling-fires"],
)
def test_one_measurement_answers_a_floor_and_a_ceiling(rule, text, side):
    #  A pack decides which side of a spread is the defect, so both halves of
    #  this table have to work without a second code path behind them.
    assert [hit.fields["side"] for hit in hits(rule, text)] == ([side] if side else [])


def test_variation_reports_the_measurement_it_used():
    found = hits(monotony, UNIFORM)
    assert found[0].fields["count"] == 4
    assert found[0].fields["mean"] == "4.0"
    assert found[0].fields["sd"] == "0.0"
    assert found[0].fields["variation"] == "0.00"
    assert found[0].fields["limit"] == "0.3"


def test_variation_is_scale_free():
    #  Doubling every sentence leaves the shape of the document alone, so the
    #  coefficient of variation may not move. A raw standard deviation would
    #  double, and a threshold built on one would mean nothing.
    single = hits(erratic, "Raz dwa. Raz dwa trzy cztery.")
    doubled = hits(erratic, "Raz dwa raz dwa. Raz dwa trzy cztery raz dwa trzy cztery.")
    assert single[0].fields["variation"] == doubled[0].fields["variation"]


def test_the_finding_is_anchored_at_the_whole_document():
    #  Anchoring it at a sentence would invite editing that sentence until the
    #  number moved, which is the failure docs/rules.md warns about.
    found = hits(monotony, UNIFORM)
    assert (found[0].span.start, found[0].span.end) == (0, len(UNIFORM))


def test_variation_abstains_rather_than_measure_a_spread_over_too_few_sentences():
    outcomes = run(floored_variation, "Program zapisuje ustawienia. Plik jest gotowy.")
    assert [type(o) for o in outcomes] == [Abstain]
    assert "too few" in outcomes[0].reason


def test_variation_abstains_on_a_document_with_no_words_to_average():
    outcomes = run(monotony, "— — —\n\n…\n")
    assert [type(o) for o in outcomes] == [Abstain]
    assert "too short" in outcomes[0].reason


# --------------------------------------------------------------------------- #
# Parameter validation, which happens when a rule is declared.
# --------------------------------------------------------------------------- #


def test_unknown_check_is_refused():
    with pytest.raises(RuleError, match="unknown check"):
        pack.rule(id="x1", check="astrology", message="m", justification="j")


def test_unknown_parameter_is_refused():
    with pytest.raises(RuleError, match="unknown parameters: patern"):
        pack.rule(
            id="x2",
            check="pattern",
            params=dict(patern="typo"),
            message="m",
            justification="j",
        )


def test_broken_regex_is_refused_with_the_rule_id():
    with pytest.raises(RuleError, match="x3.*not a valid regular expression"):
        pack.rule(
            id="x3",
            check="pattern",
            params=dict(pattern="([unclosed"),
            message="m",
            justification="j",
        )


def test_unknown_regex_flag_is_refused():
    with pytest.raises(RuleError, match="unknown regex flag"):
        pack.rule(
            id="x4",
            check="pattern",
            params=dict(pattern="a", flags=["sideways"]),
            message="m",
            justification="j",
        )


def test_message_placeholder_must_be_a_field_the_check_reports():
    with pytest.raises(RuleError, match="message uses rate, but check 'pattern' reports match"):
        pack.rule(
            id="x5",
            check="pattern",
            params=dict(pattern="a"),
            message="{rate} per 1000",
            justification="j",
        )


def test_bad_unit_is_refused():
    with pytest.raises(RuleError, match="'unit' must be"):
        pack.rule(
            id="x6",
            check="pattern-density",
            params=dict(pattern="a", unit="chapter", max_per_1000_words=1),
            message="{count}",
            justification="j",
        )


def test_negative_threshold_is_refused():
    with pytest.raises(RuleError, match="'max_per_1000_words' must be"):
        pack.rule(
            id="x7",
            check="pattern-density",
            params=dict(pattern="a", max_per_1000_words=-1),
            message="{count}",
            justification="j",
        )


def test_an_introduce_pattern_that_captures_nothing_is_refused():
    with pytest.raises(RuleError, match="exactly one group, and this one has 0"):
        pack.rule(
            id="x9",
            check="entity-recurrence",
            params=dict(introduce=r"[A-Z]\w+", max_walk_on_share=0.5),
            message="{share}",
            justification="j",
        )


def test_a_share_above_one_is_refused():
    with pytest.raises(RuleError, match="cannot exceed 1"):
        pack.rule(
            id="x10",
            check="entity-recurrence",
            params=dict(introduce=r"([A-Z]\w+)", max_walk_on_share=50),
            message="{share}",
            justification="j",
        )


def test_a_bound_with_neither_side_set_is_refused():
    with pytest.raises(RuleError, match="needs 'min_variation', 'max_variation', or both"):
        pack.rule(
            id="x11",
            check="length-variation",
            params=dict(unit="sentence"),
            message="{variation}",
            justification="j",
        )


def test_a_floor_above_its_ceiling_is_refused():
    with pytest.raises(RuleError, match="no text can pass both"):
        pack.rule(
            id="x12",
            check="length-variation",
            params=dict(min_variation=0.8, max_variation=0.2),
            message="{variation}",
            justification="j",
        )


def test_variation_over_a_corpus_is_refused():
    #  A corpus mixes documents whose lengths have no reason to agree, so it is
    #  the one unit this measurement cannot be taken over.
    with pytest.raises(RuleError, match="'unit' must be one of sentence, paragraph"):
        pack.rule(
            id="x13",
            check="length-variation",
            params=dict(unit="corpus", min_variation=0.3),
            message="{variation}",
            justification="j",
        )


def test_empty_word_list_is_refused():
    with pytest.raises(RuleError, match="'words' must be"):
        pack.rule(
            id="x8",
            check="line-end-word",
            params=dict(words=[]),
            message="{word}",
            justification="j",
        )
