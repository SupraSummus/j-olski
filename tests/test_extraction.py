"""What the harness does to a Markdown document, and what it must not invent.

The fixture beside this file carries one instance of every construct the
extraction handles, and the prose beside it is the whole answer: a change in
what the extraction keeps shows up as a diff a reader can judge. The other
tests here are the mistakes that would not show up that way — an extraction
that quietly drops prose, and one that leaves findings behind where markup
stood, which is the failure docs/extraction.md was written against — and the
counting pack, which no other test reaches and two documents cite.
"""

from pathlib import Path

import pytest

from harness.markdown import PROSE_SUFFIX, main, prose
from olski.checks import get_check
from olski.cli import lint_string
from olski.rules import load_packs

HARNESS = Path(__file__).parent.parent / "harness"
FIXTURES = Path(__file__).parent / "fixtures"

#: A list that closes a document, in the two shapes that decide whether it is an
#: index or the last thing the author had to say.
CLOSING_LIST = "Wnioski:\n\n- {first}\n- {second}\n"


def test_the_fixture_extracts_to_the_prose_beside_it():
    source = (FIXTURES / "extraction.md").read_text(encoding="utf-8")
    assert prose(source) == (FIXTURES / f"extraction{PROSE_SUFFIX}").read_text(encoding="utf-8")


def test_the_extraction_invents_no_typographic_finding():
    """The fixture's prose is clean, so every finding over it would be the extractor's.

    Both extractions written before this one deleted inline markup and left the
    space in front of it, which is a ``space-before-punctuation`` finding per
    link and a ``double-space`` finding per span in the middle of a sentence.
    The fixture stands a link before a question mark and an image with no
    description mid-paragraph for exactly that reason.
    """
    extracted = prose((FIXTURES / "extraction.md").read_text(encoding="utf-8"))
    report = lint_string(extracted, "extraction.txt")
    assert [(f.rule.id, f.message) for f in report.findings] == []


@pytest.mark.parametrize(
    ("first", "second", "survives"),
    [
        ("Pierwszy wniosek.", "Drugi wniosek.", True),
        ("[prom](prom.md) — Rin i promy", "[tlen](tlen.md) — atmosfera", False),
    ],
    ids=["sentences", "links"],
)
def test_a_list_closing_a_document_goes_only_when_its_items_are_links(first, second, survives):
    extracted = prose(CLOSING_LIST.format(first=first, second=second))
    assert ("wniosek" in extracted) is survives
    assert "Wnioski:" in extracted


def test_a_document_in_another_language_is_left_out_of_a_polish_corpus(tmp_path, capsys):
    """A rate over Polish must not have another language in its denominator."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "pl.md").write_text(
        "Zdanie po polsku, w którym słowa mają ogonki.\n", encoding="utf-8"
    )
    (tmp_path / "src" / "en.md").write_text("A sentence in English.\n", encoding="utf-8")
    main([str(tmp_path / "src"), "--into", str(tmp_path / "out"), "--polish", "0.05"])
    assert "1 files into" in capsys.readouterr().out
    assert [path.stem for path in (tmp_path / "out").iterdir()] == ["pl"]


def test_every_counter_reports_a_rate_per_thousand_words():
    """The rates docs/corpora.md and docs/generated-polish.md cite come out of these.

    A counter is a rule declaration like any other, so a change to what a rule
    must carry breaks the pack where nothing else looks, and the two documents
    go on citing numbers nobody can produce. The unit is the other half: read
    over anything but words, the same row would be a share of documents.
    """
    counters = load_packs([str(HARNESS / "counts.py")])
    assert {rule.id for rule in counters} == {"em-dash", "en-dash", "quote-open", "quote-close"}
    assert {get_check(rule.check, rule.id).counted_over(rule.params) for rule in counters} == {
        "word"
    }


def test_the_command_mirrors_a_tree_into_files_olski_reads_as_prose(tmp_path, capsys):
    (tmp_path / "notes" / "deep").mkdir(parents=True)
    (tmp_path / "notes" / "one.md").write_text("# Tytuł\n\nZdanie.\n", encoding="utf-8")
    (tmp_path / "notes" / "deep" / "two.md").write_text("Drugie\nzdanie.\n", encoding="utf-8")
    assert main([str(tmp_path / "notes"), "--into", str(tmp_path / "prose")]) == 0
    assert "2 files" in capsys.readouterr().out
    assert (tmp_path / "prose" / f"one{PROSE_SUFFIX}").read_text(encoding="utf-8") == "Zdanie.\n"
    assert (tmp_path / "prose" / "deep" / f"two{PROSE_SUFFIX}").read_text(
        encoding="utf-8"
    ) == "Drugie zdanie.\n"
