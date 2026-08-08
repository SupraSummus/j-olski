"""What the harness does to a document and to a module, and what it must not invent.

The fixture beside this file carries one instance of every construct each
extraction handles, and the prose beside it is the whole answer: a change in
what the extraction keeps shows up as a diff a reader can judge. Its tail is
the constructs the parser and the enabled rules settle rather than this
repository — a table written without leading pipes, a code span of three
backticks opening a line, two one-character emphases in a row — so a preset
narrowed to plain CommonMark, or widened, moves the fixture. The other
tests here are the mistakes that would not show up that way — an extraction
that quietly drops prose, and one that leaves findings behind where markup
stood, which is the failure docs/extraction.md was written against — and the
counting pack, which no other test reaches and two documents cite.
"""

from pathlib import Path

import pytest

from harness import PROSE_SUFFIX, markdown, python
from olski.checks import get_check
from olski.engine import lint_string
from olski.rules import load_packs

HARNESS = Path(__file__).parent.parent / "harness"
FIXTURES = Path(__file__).parent / "fixtures"

#: A list that closes a document, in the two shapes that decide whether it is an
#: index or the last thing the author had to say.
CLOSING_LIST = "Wnioski:\n\n- {first}\n- {second}\n"


def test_the_markdown_fixture_extracts_to_the_prose_beside_it():
    source = (FIXTURES / "extraction.md").read_text(encoding="utf-8")
    expected = (FIXTURES / f"extraction{PROSE_SUFFIX}").read_text(encoding="utf-8")
    assert markdown.prose(source) == expected


def test_the_markdown_extraction_invents_no_typographic_finding():
    """The fixture's prose is clean, so every finding over it would be the extractor's.

    Both extractions written before this one deleted inline markup and left the
    space in front of it, which is a ``space-before-punctuation`` finding per
    link and a ``double-space`` finding per span in the middle of a sentence.
    The fixture stands a link before a question mark and an image with no
    description mid-paragraph for exactly that reason.
    """
    extracted = markdown.prose((FIXTURES / "extraction.md").read_text(encoding="utf-8"))
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
    extracted = markdown.prose(CLOSING_LIST.format(first=first, second=second))
    assert ("wniosek" in extracted) is survives
    assert "Wnioski:" in extracted


def test_a_document_in_another_language_is_left_out_of_a_polish_corpus(tmp_path, capsys):
    """A rate over Polish must not have another language in its denominator."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "pl.md").write_text(
        "Zdanie po polsku, w którym słowa mają ogonki.\n", encoding="utf-8"
    )
    (tmp_path / "src" / "en.md").write_text("A sentence in English.\n", encoding="utf-8")
    markdown.main([str(tmp_path / "src"), "--into", str(tmp_path / "out"), "--polish", "0.05"])
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
    assert markdown.main([str(tmp_path / "notes"), "--into", str(tmp_path / "prose")]) == 0
    assert "2 files" in capsys.readouterr().out
    assert (tmp_path / "prose" / f"one{PROSE_SUFFIX}").read_text(encoding="utf-8") == "Zdanie.\n"
    assert (tmp_path / "prose" / "deep" / f"two{PROSE_SUFFIX}").read_text(
        encoding="utf-8"
    ) == "Drugie zdanie.\n"


#: Moduł pisany w dwóch językach, czyli tak, jak pisany jest każdy moduł tego
#: repozytorium, plus komentarz za krótki, żeby udział diakrytyków cokolwiek
#: nad nim znaczył.
MODUŁ = '''\
"""A module mixes two languages by design, so the selection has to go below the
file to see which of its parts are Polish and which of them are not."""

#  Komentarz po polsku, dostatecznie długi, żeby udział znaków diakrytycznych
#  cokolwiek nad nim znaczył, bo nad ośmioma słowami nie znaczy on nic ponad
#  to, ile ich jest.

#  Zdanie za krótkie.
STAŁA = 1
'''


def test_moduł_próbny_wychodzi_prozą_która_stoi_obok_niego():
    source = (FIXTURES / "moduł.py").read_text(encoding="utf-8")
    expected = (FIXTURES / f"moduł{PROSE_SUFFIX}").read_text(encoding="utf-8")
    assert python.prose(source) == expected


def test_ekstrakcja_z_modułu_nie_wymyśla_znaleziska_typograficznego():
    """Proza fixture'u jest czysta, więc każde znalezisko nad nią jest ekstrakcji.

    Konstrukcja skasowana tak, że odstęp przed nią zostaje, jest znaleziskiem
    dwóch reguł na sztukę, i po to fixture stawia pytajnik tuż za rolą Sphinksa
    oraz cztery znaczniki w jednym zdaniu.
    """
    wyszło = python.prose((FIXTURES / "moduł.py").read_text(encoding="utf-8"))
    raport = lint_string(wyszło, f"moduł{PROSE_SUFFIX}")
    assert [(f.rule.id, f.message) for f in raport.findings] == []


@pytest.fixture
def proza_modułu(tmp_path):
    (tmp_path / "pakiet").mkdir()
    (tmp_path / "pakiet" / "moduł.py").write_text(MODUŁ, encoding="utf-8")
    python.main(
        [
            str(tmp_path / "pakiet"),
            "--into",
            str(tmp_path / "proza"),
            "--polish",
            "0.12",
            "--min-words",
            "20",
        ]
    )
    return (tmp_path / "proza" / f"moduł{PROSE_SUFFIX}").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("fragment", "zostaje"),
    [
        ("Komentarz po polsku", True),
        ("A module mixes two languages", False),
        ("Zdanie za krótkie", False),
    ],
    ids=["polski", "angielski", "krótszy niż podłoga"],
)
def test_wybór_po_języku_schodzi_do_jednostki_i_ma_podłogę(proza_modułu, fragment, zostaje):
    """Nad plikiem ten wybór nie ma nad czym stanąć, a nad ośmioma słowami nie ma czym mierzyć.

    Docstring po angielsku jest dłuższy niż podłoga, a komentarz za krótki jest
    polski na tyle, na ile trzy słowa mogą być, więc każdy z nich wypada z
    innego powodu i żaden nie wypada przez ten drugi.
    """
    assert (fragment in proza_modułu) is zostaje
