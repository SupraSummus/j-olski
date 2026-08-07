"""What a tally counts.

A tally is a row of a firing-rate report, and its denominator is what the corpus
held less what the rule declined. The two kinds of refusal take different amounts
with them, and getting that wrong is a wrong number rather than a missing one, so
the arithmetic is what these tests are about.
"""

from olski.document import Document, from_text
from olski.engine import lint_corpus
from olski.rules import Pack

pack = Pack(name="test", origin="tests/test_engine.py")

orphans = pack.rule(
    id="test-orphan",
    check="line-end-word",
    params=dict(words=["a", "i", "w"]),
    message="orphan {word}",
    justification="a test",
)

density = pack.rule(
    id="test-density",
    check="pattern-density",
    params=dict(pattern="—", unit="paragraph", max_per_1000_words=20, min_words=10),
    message="{rate} per 1000 words, over {limit}",
    justification="a test",
)

#  One paragraph over two lines, both of them lines a reader sees.
WRAPPED = "Zapisano to w\npliku tekstowym.\n"

#  Four paragraphs on a line each, which is what a plain-text export gives and what
#  a line-end rule declines. Seven lines with the blank ones between them.
UNWRAPPED = "\n\n".join(["Akapit stoi tu w jednej linii, jak w eksporcie."] * 4) + "\n"


def tally_of(rule, documents):
    (tally,) = lint_corpus(documents, [rule]).tally([rule])
    return tally


def test_a_declined_file_takes_all_of_its_lines_off_the_denominator():
    #  The two files hold nine lines between them and the rule reached a verdict on
    #  two of them. Counting the refusal as one line would leave six lines nobody
    #  looked at in the denominator, and the rate would be over those as well.
    documents = [from_text(WRAPPED, "wrapped.txt"), from_text(UNWRAPPED, "export.txt")]
    tally = tally_of(orphans, documents)
    assert tally.unit == "line"
    assert (tally.findings, tally.abstentions, tally.measured) == (1, 1, 2)


def test_a_rule_that_declined_every_file_reports_no_rate_rather_than_a_rate_of_nought():
    tally = tally_of(orphans, [from_text(UNWRAPPED, "export.txt")])
    assert tally.measured == 0
    assert tally.rate is None


def test_the_two_kinds_of_refusal_subtract_differently():
    #  Two paragraphs, one of them under the word floor the rule asks for, and a
    #  markup file beside them that the rule never reads. The refusals subtract
    #  differently: the file's paragraph comes off with the file, the short one
    #  comes off alone.
    text = "Krótki akapit.\n\n" + "Dłuższy akapit z myślnikiem — i dalszą treścią. " * 2
    documents = [
        from_text(text, "prose.txt"),
        Document(path="notes.md", text="Akapit w składni Markdown.\n", plain_text=False),
    ]
    tally = tally_of(density, documents)
    assert tally.unit == "paragraph"
    assert (tally.abstentions, tally.measured) == (2, 1)
