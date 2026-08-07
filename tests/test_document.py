import time

import pytest

from olski.document import Span, from_text, is_plain_text


def test_positions_are_one_based():
    document = from_text("pierwsza\ndruga\n")
    assert document.position(0) == (1, 1)
    assert document.position(9) == (2, 1)
    assert document.position(10) == (2, 2)


def test_line_span_excludes_the_newline():
    document = from_text("ala\nma kota\n")
    assert document.slice(document.line_span(2)) == "ma kota"


def test_paragraphs_are_blank_line_separated_and_trimmed():
    document = from_text("Pierwszy akapit.\nDruga linia.\n\n\nDrugi akapit.\n")
    assert [document.slice(p) for p in document.paragraphs] == [
        "Pierwszy akapit.\nDruga linia.",
        "Drugi akapit.",
    ]


def test_a_blank_line_of_spaces_still_separates_paragraphs():
    document = from_text("Jeden.\n   \nDwa.\n")
    assert len(document.paragraphs) == 2


def test_sentences_do_not_cross_a_paragraph_boundary():
    document = from_text("Jeden. Dwa!\n\nTrzy… Cztery?\n")
    assert [document.slice(s) for s in document.sentences] == [
        "Jeden.",
        "Dwa!",
        "Trzy…",
        "Cztery?",
    ]


def test_an_unpunctuated_paragraph_is_one_sentence():
    #  A heading or a list item, which would otherwise run into the prose below.
    document = from_text("Zapisywanie pliku\n\nZapisz plik konfiguracyjny.\n")
    assert [document.slice(s) for s in document.sentences] == [
        "Zapisywanie pliku",
        "Zapisz plik konfiguracyjny.",
    ]


@pytest.mark.parametrize(
    "text",
    [
        "Ustawa z 2011 r. weszła w życie.",
        "Dotyczy to m.in. plików konfiguracyjnych.",
        "Zapisz plik, np. ustawienia użytkownika.",
        "Reguła jest w art. 12 tej ustawy.",
        "Mapa jest dostępna w serwisie zabytek.pl dla każdego.",
        "Opisał to J. Kowalski w swojej pracy.",
        "Punkt 12. tej listy mówi o czymś innym.",
    ],
)
def test_a_full_stop_inside_a_sentence_does_not_split_it(text):
    assert len(from_text(text).sentences) == 1


def test_a_closing_quotation_mark_belongs_to_the_sentence_it_closes():
    document = from_text('Napisał „plik konfiguracyjny." Potem go zapisał.')
    assert [document.slice(s) for s in document.sentences] == [
        'Napisał „plik konfiguracyjny."',
        "Potem go zapisał.",
    ]


def test_a_sentence_ending_in_an_abbreviation_runs_into_the_next():
    #  The deliberate wrong side of the choice: an abbreviation that does close a
    #  sentence merges it with the following one, which understates a count
    #  rather than inventing a sentence nobody wrote. See olski/document.py.
    document = from_text("Ustawa weszła w życie w 2011 r. Zmieniono ją później.")
    assert len(document.sentences) == 1


def test_splitting_stays_linear_in_the_length_of_a_document():
    #  Matching the token before a full stop against everything to its left is
    #  quadratic: invisible on a fixture, and a hang on a real file. Bounded, this
    #  runs in hundredths of a second; unbounded, in minutes. The budget is loose
    #  enough not to be flaky and still fails by orders of magnitude.
    text = "Program zapisuje twoje ustawienia w katalogu domowym. " * 8000
    started = time.monotonic()
    document = from_text(text)
    assert len(document.sentences) == 8000
    assert time.monotonic() - started < 5


def test_words_exclude_numbers_and_punctuation():
    #  Zażółć gęślą jaźń razy naprawdę: the numeral and the dash are not words.
    document = from_text("Zażółć gęślą jaźń, 42 razy — naprawdę.")
    assert document.word_count() == 5


def test_words_are_counted_within_a_span():
    document = from_text("jeden dwa\n\ntrzy cztery pięć")
    assert document.word_count(document.paragraphs[0]) == 2
    assert document.word_count(document.paragraphs[1]) == 3


def test_excerpt_collapses_whitespace_and_truncates():
    document = from_text("ala   ma\nkota")
    assert document.excerpt(Span(0, 13)) == "ala ma kota"
    assert document.excerpt(Span(0, 13), limit=6) == "ala m…"


def test_one_quoted_poem_does_not_make_a_novel_laid_out_in_lines():
    #  The case the threshold exists for. An export sets each paragraph on a line
    #  of its own, and a novel quoting verse has a handful that run past one, so
    #  the reading is a share and not the presence of a single multi-line
    #  paragraph. docs/firing-rates.md owns the distribution behind the number.
    export = "\n\n".join(["Akapit stoi w jednej linii."] * 9 + ["Wers pierwszy,\nwers drugi."])
    assert from_text(export).hard_wrapped is False
    verse = "\n\n".join(["Wers pierwszy,\nwers drugi."] * 2 + ["Podpis."])
    assert from_text(verse).hard_wrapped is True


@pytest.mark.parametrize(
    ("name", "plain"),
    [
        ("notatka.txt", True),
        ("notatka.TXT", True),
        ("notatka.md", False),
        #  No suffix says nothing about the contents, and the permissive guess is
        #  the one that invents findings.
        ("README", False),
    ],
)
def test_only_a_plain_text_suffix_carries_the_plain_text_guarantee(name, plain):
    assert is_plain_text(f"notes/{name}") is plain
