import pytest

from olski.checks import CHECKS, ZASIĘG_KONTEKSTU, Abstain, Hit, count_units
from olski.document import Document
from olski.rules import Pack, RuleError

# Rules under test are declared here rather than taken from the shipped pack, so
# that a threshold change in the pack cannot quietly break a check's test.
pack = Pack(name="test", origin="tests/test_checks.py")


def over(rule, documents):
    return list(CHECKS[rule.check].run(rule, documents))


def run(rule, text):
    document = text if isinstance(text, Document) else Document(text)
    return over(rule, [document])


def hits(rule, text):
    return [outcome for outcome in run(rule, text) if isinstance(outcome, Hit)]


def corpus(*texts):
    """A corpus whose files are named after their position, so that a finding's
    document can be named in an assertion."""
    return [Document(text, path=f"{n}.txt") for n, text in enumerate(texts, start=1)]


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


rozciągnięty = pack.rule(
    id="test-unless-preceded-by-stretch",
    check="pattern",
    #  Wyjątek biegnie od skrótu aż do trafienia,
    #  bo tylko taki ma czego stracić na zasięgu:
    #  wyjątek o stałej szerokości i tak kończy się tam, gdzie trafienie się zaczyna,
    #  więc nigdy nie sięga poza okno.
    params=dict(pattern=r"\.(?=[A-Z])", unless_preceded_by=r"\bnp\b[^.]*"),
    message="run-together {match}",
    justification="a test",
)


@pytest.mark.parametrize("odległość", (ZASIĘG_KONTEKSTU - 10, ZASIĘG_KONTEKSTU + 10))
def test_wyjątek_przestaje_patrzeć_wstecz_na_zasięgu(odległość):
    """Zasięg ogranicza wyjątek, który się rozciąga, a pominięcie za nim jest umyślne.

    Warto to przybić, bo nic innego nie zauważyłoby, że zasięg się ruszył.
    Przywrócenie przebiegu bez ograniczenia zostawia każdy inny test zielonym,
    a check kwadratowym względem długości dokumentu;
    zwężenie okna po cichu gubi wyjątki, na których paczka reguł stała.
    """
    #  Wypełniacz po dwa znaki,
    #  żeby skrót stał dokładnie tyle znaków przed trafieniem, ile mówi parametr.
    #  Kropki w nim nie ma:
    #  kończyłaby dopasowanie wyjątku przed trafieniem, które ten wyjątek ma zdejmować.
    tekst = "np" + " x" * ((odległość - 2) // 2) + ".Zapisz"
    assert bool(hits(rozciągnięty, tekst)) is (odległość > ZASIĘG_KONTEKSTU)


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

sparse = pack.rule(
    id="test-density-sparse",
    check="pattern-density",
    params=dict(pattern=r"\d+", unit="document", min_per_1000_words=100),
    message="{count} numerals in {words} words, {rate} per 1000, {side} {limit}",
    justification="a test",
)


#  Ten words and two dashes: 200 per 1000, over the limit of 100.
DASHY = "raz dwa trzy — cztery pięć sześć siedem — osiem dziewięć dziesięć"
#  The same two dashes, spread over enough words to come in under it.
SPREAD = DASHY + " " + " ".join(["słowo"] * 15)
#  Twenty words and not a numeral among them: 0 per 1000, under the floor of 100.
NO_NUMERALS = " ".join(["słowo"] * 20)
#  Two numerals in ten words: 200 per 1000, clear of the same floor.
NUMERALS = "3 pliki 7 stron " + " ".join(["słowo"] * 8)


@pytest.mark.parametrize(
    ("rule", "text", "side"),
    [
        (dashes, DASHY, "above"),
        (dashes, SPREAD, None),
        (sparse, NO_NUMERALS, "below"),
        (sparse, NUMERALS, None),
    ],
    ids=["ceiling-fires", "ceiling-quiet", "floor-fires", "floor-quiet"],
)
def test_one_rate_answers_a_ceiling_and_a_floor(rule, text, side):
    #  Fact density runs the other way from every rate rule the packs ship, so
    #  both halves of this table have to work without a second code path.
    assert [hit.fields["side"] for hit in hits(rule, text)] == ([side] if side else [])


def test_density_reports_the_measurement_it_used():
    found = hits(dashes, DASHY)
    assert found[0].fields["count"] == 2
    assert found[0].fields["words"] == 10
    assert found[0].fields["rate"] == "200.0"
    assert found[0].fields["limit"] == "100"


def test_density_points_at_the_first_occurrence_in_the_unit():
    assert hits(dashes, DASHY)[0].span.start == DASHY.index("—")


def test_a_cold_finding_points_at_the_scope_rather_than_at_an_occurrence():
    #  Which is also all `{match}` can show, there being no occurrence to quote.
    found = hits(sparse, NO_NUMERALS)
    assert (found[0].span.start, found[0].span.end) == (0, len(NO_NUMERALS))
    assert found[0].fields["count"] == 0
    assert found[0].fields["match"] == ""


band = pack.rule(
    id="test-density-band",
    check="pattern-density",
    params=dict(
        pattern=r"\d+",
        unit="document",
        min_per_1000_words=100,
        max_per_1000_words=300,
        min_count=3,
    ),
    message="{count} numerals, {rate} per 1000, {side} {limit}",
    justification="a test",
)


@pytest.mark.parametrize(
    ("text", "side"),
    [("3 pliki 7 stron", None), (NO_NUMERALS, "below")],
    ids=["hot-held-back", "cold-fires"],
)
def test_a_count_floor_holds_back_a_hot_reading_and_not_a_cold_one(text, side):
    #  Two numerals in two words is 1000 per 1000 and evidence of nothing, which
    #  is what min_count is for. Held against the other side it would skip the
    #  document a rate floor is looking hardest for: the one with no matches.
    assert [hit.fields["side"] for hit in hits(band, text)] == ([side] if side else [])


def test_the_count_floor_declines_a_hot_reading_rather_than_passing_over_it():
    #  Both floors are the rule refusing to answer, so both say so. Returning here
    #  instead would leave the scope in a denominator as though the rule had looked
    #  at it and found nothing.
    outcomes = run(band, "3 pliki 7 stron")
    assert [type(o) for o in outcomes] == [Abstain]
    assert outcomes[0].reason == "this document is under the 3-match floor a rate above 300 needs"


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


@pytest.mark.parametrize("text", ["raz — dwa", "raz dwa trzy"], ids=["over-the-rate", "under-it"])
def test_a_scope_under_the_word_floor_is_declined_whatever_its_rate(text):
    #  Three words either way, one carrying a dash and one not, so the first would
    #  have been reported and the second would not. The floor is tested before the
    #  bounds, so neither stays in the denominator of a rate over three words.
    outcomes = run(floored, text)
    assert [type(o) for o in outcomes] == [Abstain]
    assert outcomes[0].reason == "this document is under the 20-word floor a rate over it needs"


def test_density_abstains_on_a_scope_with_no_words_to_measure_a_rate_over():
    #  Nothing counted over nothing is a rate of zero, which a floor would
    #  otherwise report as a finding about a document with no prose to have one.
    outcomes = run(sparse, "— — —\n")
    assert [type(o) for o in outcomes] == [Abstain]
    assert "1-word floor" in outcomes[0].reason


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


corpus_sparse = pack.rule(
    id="test-corpus-sparse",
    check="pattern-density",
    params=dict(pattern=r"\d+", unit="corpus", min_per_1000_words=100),
    message="{count} numerals across the corpus, {side} {limit}",
    justification="a test",
)


def test_a_cold_corpus_finding_names_a_file_although_no_file_owns_the_answer():
    #  An abstention over a corpus belongs to no file, but a finding is a
    #  location, and a cold reading has no occurrence to take one from. The
    #  corpus starts somewhere, and that is what it points at.
    found = over(corpus_sparse, corpus(NO_NUMERALS, NO_NUMERALS))
    assert len(found) == 1
    assert found[0].document.path == "1.txt"
    assert found[0].span.start == 0


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


def test_line_end_word_matches_the_case_the_rule_listed():
    #  Folding case is what read the Roman numeral as the conjunction, and the
    #  numeral is how Polish counts a volume, a chapter and a monarch.
    assert hits(orphans, "Zaczyna się Tom I\nnowej powieści.") == []


def test_line_end_word_looks_past_trailing_punctuation():
    assert len(hits(orphans, "Wybór między a,\nb oraz c.")) == 1


def test_line_end_word_abstains_where_a_source_line_is_not_a_rendered_line():
    #  The line this would flag ends where the file wraps, not where the page
    #  does, so the letter it points at is mid-line for every reader.
    reflowed = Document(path="reflowed.md", text="Zapisano to w\npliku.\n", plain_text=False)
    outcomes = run(orphans, reflowed)
    assert [type(o) for o in outcomes] == [Abstain]
    assert outcomes[0].whole_file


def test_line_end_word_abstains_on_plain_text_that_sets_a_paragraph_on_one_line():
    #  The export a whole published corpus arrives in, where the rule fired 124
    #  times and every hit stood mid-line for every reader. The second paragraph
    #  ends on a listed word, so the refusal is what keeps it from being a finding.
    export = (
        "Zapisano to w pliku tekstowym i nic więcej się nie stało.\n\n"
        "Drugi akapit również stoi w jednej linii, jak w eksporcie, a\n\n"
        "Trzeci akapit tak samo, cały na jednej linii.\n"
    )
    outcomes = run(orphans, export)
    assert [type(o) for o in outcomes] == [Abstain]
    assert outcomes[0].whole_file


def test_line_end_word_measures_a_document_whose_paragraphs_run_past_a_line():
    #  Verse is not wrapped to a width and its line ends are line ends all the
    #  same, so what the precondition reads is where a paragraph ends and not how
    #  long a line is.
    verse = "Nie porzucaj nadzieje,\nJakoć się kolwiek dzieje: a\nbo świeci.\n"
    assert [h.fields["word"] for h in hits(orphans, verse)] == ["a"]


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
# What every check owes a document whose format olski does not read.
# --------------------------------------------------------------------------- #

#: One rule per check kind, and whether that check points at a site it can show
#: the reader or measures a scope it has to trust the whole of.
BY_SCOPE = [
    (straight_quote, True),
    (dashes, False),
    (orphans, False),
    (monotony, False),
    (walk_ons, False),
]

#: Enough of everything for every rule above to fire on it: a straight quote,
#: dashes far over the rate, three sentences of exactly one length, an entity
#: introduced and then dropped, and a single-letter word at a line end.
LOUD = (
    'Nara (fizyczka, 31) — "tak" — sprawdziła czujnik i\n'
    "wyszła.\n"
    "Rho — technik — zapisał wynik i wyszedł stąd.\n"
    "Iva — pilotka — czekała na sygnał i odeszła.\n"
)


@pytest.mark.parametrize(
    ("rule", "points_at_a_site"), BY_SCOPE, ids=[rule.check for rule, _ in BY_SCOPE]
)
def test_a_check_that_measures_a_whole_scope_declines_on_markup(rule, points_at_a_site):
    def fired(document):
        return any(isinstance(outcome, Hit) for outcome in over(rule, [document]))

    #  Without this the declining half of the test passes on any fixture,
    #  including one the rule had nothing to say about in the first place.
    assert fired(Document(LOUD, path="note.txt")), "the fixture gives this rule nothing to find"
    assert fired(Document(path="note.md", text=LOUD, plain_text=False)) == points_at_a_site


def test_every_check_kind_is_classified_by_scope():
    #  A new check that measures a rate and forgets to say so would otherwise
    #  report a number over somebody's frontmatter, and nothing would notice.
    assert {rule.check for rule, _ in BY_SCOPE} == set(CHECKS)


@pytest.mark.parametrize("rule", [rule for rule, _ in BY_SCOPE], ids=[r.check for r, _ in BY_SCOPE])
def test_every_check_counts_its_findings_over_something_a_corpus_can_be_measured_in(rule):
    #  A check naming a unit nothing counts, or reading a parameter its rules do
    #  not carry, breaks where a report is printed rather than where the check
    #  was written.
    assert count_units(CHECKS[rule.check].counted_over(rule.params), corpus(LOUD)) > 0


def test_a_mixed_corpus_is_measured_on_its_plain_files_and_declined_on_the_rest():
    mixed = [Document(LOUD, path="a.txt"), Document(LOUD, path="b.md", plain_text=False)]
    outcomes = over(dashes, mixed)
    assert [o.document.path for o in outcomes if isinstance(o, Hit)] == ["a.txt"]
    assert [o.document.path for o in outcomes if isinstance(o, Abstain)] == ["b.md"]


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


def test_what_a_density_rule_may_quote_follows_from_the_bounds_it_set():
    #  A reading above a ceiling has a first occurrence to point at, and one below
    #  a floor is the text that went by without one, so `{match}` there could only
    #  ever render empty.
    pack.rule(
        id="x14-ceiling",
        check="pattern-density",
        params=dict(pattern=r"\d+", max_per_1000_words=100),
        message="too many, such as {match}",
        justification="j",
    )
    with pytest.raises(RuleError, match="message uses match, but check 'pattern-density' reports"):
        pack.rule(
            id="x14-floor",
            check="pattern-density",
            params=dict(pattern=r"\d+", min_per_1000_words=100),
            message="too few, such as {match}",
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


@pytest.mark.parametrize(
    ("check", "params", "quantity"),
    [
        ("length-variation", dict(unit="sentence"), "variation"),
        ("pattern-density", dict(pattern="a"), "per_1000_words"),
    ],
    ids=["length-variation", "pattern-density"],
)
def test_a_bound_with_neither_side_set_is_refused(check, params, quantity):
    #  Both checks take the same pair, so a rule that names neither side has
    #  said nothing about what it would report.
    with pytest.raises(RuleError, match=f"needs 'min_{quantity}', 'max_{quantity}', or both"):
        pack.rule(
            id=f"x11-{check}",
            check=check,
            params=params,
            message="{limit}",
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
