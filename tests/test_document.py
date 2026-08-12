import time

import pytest

from olski.document import Document


def test_paragraphs_are_blank_line_separated_and_trimmed():
    document = Document("Pierwszy akapit.\nDruga linia.\n\n\nDrugi akapit.\n")
    assert [document.slice(p) for p in document.paragraphs] == [
        "Pierwszy akapit.\nDruga linia.",
        "Drugi akapit.",
    ]


def test_a_blank_line_of_spaces_still_separates_paragraphs():
    document = Document("Jeden.\n   \nDwa.\n")
    assert len(document.paragraphs) == 2


def test_sentences_do_not_cross_a_paragraph_boundary():
    document = Document("Jeden. Dwa!\n\nTrzy… Cztery?\n")
    assert [document.slice(s) for s in document.sentences] == [
        "Jeden.",
        "Dwa!",
        "Trzy…",
        "Cztery?",
    ]


def test_an_unpunctuated_paragraph_is_one_sentence():
    #  A heading or a list item, which would otherwise run into the prose below.
    document = Document("Zapisywanie pliku\n\nZapisz plik konfiguracyjny.\n")
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
    assert len(Document(text).sentences) == 1


def test_a_closing_quotation_mark_belongs_to_the_sentence_it_closes():
    document = Document('Napisał „plik konfiguracyjny." Potem go zapisał.')
    assert [document.slice(s) for s in document.sentences] == [
        'Napisał „plik konfiguracyjny."',
        "Potem go zapisał.",
    ]


def test_a_sentence_ending_in_an_abbreviation_runs_into_the_next():
    #  The deliberate wrong side of the choice: an abbreviation that does close a
    #  sentence merges it with the following one, which understates a count
    #  rather than inventing a sentence nobody wrote. See olski/document.py.
    document = Document("Ustawa weszła w życie w 2011 r. Zmieniono ją później.")
    assert len(document.sentences) == 1


def test_splitting_stays_linear_in_the_length_of_a_document():
    #  Matching the token before a full stop against everything to its left is
    #  quadratic: invisible on a fixture, and a hang on a real file. Bounded, this
    #  runs in hundredths of a second; unbounded, in minutes. The budget is loose
    #  enough not to be flaky and still fails by orders of magnitude.
    text = "Program zapisuje twoje ustawienia w katalogu domowym. " * 8000
    started = time.monotonic()
    document = Document(text)
    assert len(document.sentences) == 8000
    assert time.monotonic() - started < 5
