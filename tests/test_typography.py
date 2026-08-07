"""What the shipped pack does to real Polish sentences.

These are the tests that would notice a threshold or a pattern changing, and
they are written as sentences rather than as fixtures so that a false positive
is visible as text.
"""

import pytest

from olski.engine import lint_text
from olski.rules import load_packs, select

RULES = load_packs()


def fired(text, rule_id):
    rules = select(RULES, ids=[rule_id])
    assert rules, f"no such rule: {rule_id}"
    return [f.message for f in lint_text(text, rules).findings]


CLEAN = "Program zapisuje ustawienia w pliku konfiguracyjnym.\nDomyślnie jest to plik lokalny."


@pytest.mark.parametrize("rule", [r.id for r in RULES])
def test_no_rule_fires_on_a_clean_Polish_paragraph(rule):
    assert fired(CLEAN, rule) == []


@pytest.mark.parametrize(
    "text",
    [
        'Kliknij przycisk "Zapisz".',
        'Ustaw wartość na "true".',
    ],
)
def test_straight_quotes_are_flagged(text):
    assert len(fired(text, "quote-straight")) == 2


def test_polish_quotes_are_not_flagged():
    assert fired("Kliknij przycisk „Zapisz”.", "quote-straight") == []
    assert fired("Kliknij przycisk „Zapisz”.", "quote-english") == []


def test_only_the_english_opening_quote_is_flagged():
    #  ” is the Polish closing mark as well as the English one, so only the
    #  opening mark can be judged from the character alone.
    assert len(fired("Kliknij przycisk “Zapisz”.", "quote-english")) == 1


def test_dash_density_fires_on_a_dash_heavy_document():
    heavy = " ".join(
        f"Konfiguracja jest prosta — wystarczy jeden plik — i nic więcej numer {n}."
        for n in range(20)
    )
    assert len(fired(heavy, "em-dash-density")) == 1


def test_dash_density_is_quiet_on_occasional_dashes():
    sparse = (
        " ".join(f"Zdanie numer {n} opisuje jedną rzecz i nic więcej." for n in range(80))
        + " Jeden wyjątek — ten właśnie — i drugi wyjątek — koniec."
    )
    assert fired(sparse, "em-dash-density") == []


def test_dash_density_reports_nothing_about_a_text_under_its_word_floor():
    #  Four words carrying three dashes is 750 per 1000 and evidence of nothing,
    #  which is the number min_words=150 is in the pack to keep out of a report.
    assert fired("Raz — dwa — trzy — cztery.", "em-dash-density") == []


def test_orphan_single_letter_word_is_flagged_at_a_line_end():
    text = "Ustawienia zapisujemy w\npliku konfiguracyjnym.\n"
    assert len(fired(text, "orphan-single-letter-word")) == 1


def test_a_longer_word_at_a_line_end_is_fine():
    text = "Ustawienia zapisujemy do\npliku konfiguracyjnym.\n"
    assert fired(text, "orphan-single-letter-word") == []


def test_double_space_is_flagged_but_a_single_one_is_not():
    assert len(fired("Program  zapisuje ustawienia.", "double-space")) == 1
    assert fired("Program zapisuje ustawienia.", "double-space") == []


def test_indentation_is_not_a_double_space():
    assert fired("Akapit.\n    Wcięty wiersz ciągu dalszego.\n", "double-space") == []


def test_trailing_space_is_flagged_on_the_line_that_has_it():
    assert len(fired("Pierwsza linia.   \nDruga linia.\n", "trailing-space")) == 1


def test_space_before_punctuation_is_flagged():
    assert len(fired("Program zapisuje ustawienia .", "space-before-punctuation")) == 1
    assert len(fired("Czy to działa ?", "space-before-punctuation")) == 1


def test_space_before_a_dash_is_not_punctuation_tightening():
    assert fired("Konfiguracja jest prosta — jeden plik.", "space-before-punctuation") == []


@pytest.mark.parametrize(
    "text",
    [
        "Plik leży w katalogu .config w katalogu domowym.",
        "Zainstaluj wersję .NET podaną w wymaganiach.",
    ],
)
def test_a_leading_dot_in_a_name_is_not_a_loose_full_stop(text):
    assert fired(text, "space-before-punctuation") == []


def test_the_flagged_position_is_the_mark_not_the_space_before_it():
    report = lint_text("Zapisz zmiany .", select(RULES, ids=["space-before-punctuation"]))
    finding = report.sorted()[0]
    assert finding.column == 15
    assert "Space before ." in finding.message


def test_missing_space_after_punctuation_is_flagged():
    assert len(fired("Zapisz plik,potem go zamknij.", "missing-space-after-punctuation")) == 1


@pytest.mark.parametrize(
    "text",
    [
        "Wartość wynosi 1,5 metra.",
        "Spotkanie o 10:30 w sali.",
        "Zobacz https://example.org/strona w przeglądarce.",
        "Lista zawiera: pierwszy, drugi, trzeci.",
    ],
)
def test_missing_space_after_punctuation_leaves_numbers_and_urls_alone(text):
    assert fired(text, "missing-space-after-punctuation") == []


@pytest.mark.parametrize(
    "text",
    [
        "Zapisz plik.Potem go zamknij.",
        #  A space is required after an abbreviation period too, so this is
        #  malformed whichever reading you take, and the rule need not choose.
        "Sprawdź np.Zapisz w menu.",
        "Spotkanie o godz.Dziesiątej się zaczyna.",
        "Ustawienia są w pliku „config.toml”.Plik leży w katalogu domowym.",
    ],
)
def test_a_full_stop_with_no_space_after_it_is_flagged(text):
    assert len(fired(text, "missing-space-after-full-stop")) == 1


@pytest.mark.parametrize(
    "text",
    [
        "Wersja 2.0 jest gotowa.",
        "Skrót m.in. oznacza między innymi.",
        "Spotkanie odbędzie się 10.05.2026 w Warszawie.",
        "Sprawdź np. Zapisz w menu.",
    ],
)
def test_a_full_stop_that_needs_no_space_is_left_alone(text):
    #  An abbreviation period followed by a lower-case letter, a decimal point
    #  and a date separator all set tight in Polish, and none of them is flagged.
    assert fired(text, "missing-space-after-full-stop") == []


def test_findings_carry_a_location_and_the_rule_that_produced_them():
    report = lint_text('Pierwsza linia.\nDruga "linia".\n', select(RULES, ids=["quote-straight"]))
    first = report.sorted()[0]
    assert (first.line, first.column) == (2, 7)
    assert first.rule.id == "quote-straight"
    assert first.rule.justification


def test_the_same_input_gives_the_same_answer_twice():
    text = 'Zapisz plik,potem  go zamknij .\nUstaw wartość na "true" w\npliku.\n'
    first = lint_text(text, RULES)
    second = lint_text(text, RULES)
    assert [(f.location, f.rule.id, f.message) for f in first.sorted()] == [
        (f.location, f.rule.id, f.message) for f in second.sorted()
    ]
