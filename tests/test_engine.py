"""What a tally counts.

A tally is a row of a firing-rate report, and its denominator is what the corpus
held less what the rule declined. The two kinds of refusal take different amounts
with them, and getting that wrong is a wrong number rather than a missing one, so
the arithmetic is what these tests are about.
"""

from olski.document import Document
from olski.engine import lint_corpus
from olski.rules import Pack

pack = Pack(name="test", origin="tests/test_engine.py")

density = pack.rule(
    id="test-density",
    check="pattern-density",
    params=dict(pattern="—", unit="paragraph", max_per_1000_words=20, min_words=10),
    message="{rate} per 1000 words, over {limit}",
    justification="a test",
)

#  Three paragraphs: one over the rate the rule sets, one under the word floor it
#  asks for before answering, and one it measures and finds nothing in.
PROSE = (
    "Akapit z myślnikiem — i dalszą treścią, która ciągnie się jeszcze przez chwilę.\n\n"
    "Krótki akapit.\n\n" + "słowo " * 20
)

#  The same three under a heading, in a format olski does not read, which is what a
#  rule measuring a whole scope declines: its apparatus is prose to nothing but a suffix.
MARKUP = "# Nagłówek\n\n" + PROSE


def tally_of(rule, documents):
    (tally,) = lint_corpus(documents, [rule]).tally([rule])
    return tally


def test_the_two_kinds_of_refusal_subtract_differently():
    #  The two files hold seven paragraphs and the rule answered about two of them.
    #  The markup file's four come off with the file and the short one comes off
    #  alone; counting either refusal as nothing would put paragraphs nobody looked
    #  at in the denominator, and the rate would be over those as well.
    documents = [
        Document(PROSE, path="prose.txt"),
        Document(MARKUP, path="notes.md", plain_text=False),
    ]
    tally = tally_of(density, documents)
    assert tally.unit == "paragraph"
    assert (tally.findings, tally.abstentions, tally.measured) == (1, 2, 2)


def test_a_rule_that_declined_every_file_reports_no_rate_rather_than_a_rate_of_nought():
    tally = tally_of(density, [Document(MARKUP, path="notes.md", plain_text=False)])
    assert tally.measured == 0
    assert tally.rate is None
