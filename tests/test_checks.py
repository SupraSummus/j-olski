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


def test_empty_word_list_is_refused():
    with pytest.raises(RuleError, match="'words' must be"):
        pack.rule(
            id="x8",
            check="line-end-word",
            params=dict(words=[]),
            message="{word}",
            justification="j",
        )
