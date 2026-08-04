from olski.document import Span, from_text


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
