import pytest

from harness.endings import PROBES, Match

# One word per class of each probe, with its readings as Morfeusz returns them.
# Taking them as data rather than calling the analyser keeps this test running
# where the Morfeusz wheel does not build, and puts the readings the classes
# turn on in front of the reader: `zostanie` carries a gerund beside the verb,
# `kontekście` a lemma that is not the word, and `to` a lemma that is.
EXAMPLES = {
    "nominalization": {
        "unknown": ("ostylowanie", [("ostylowanie", "ign")]),
        "verb": (
            "zostanie",
            [("zostać", "fin:sg:ter:perf"), ("zostać", "ger:sg:nom.acc:n:perf:aff")],
        ),
        "ambiguous": (
            "pobranie",
            [
                ("pobranie", "subst:sg:nom.acc:n"),
                ("pobrać", "ger:sg:nom.acc:n:perf:aff"),
            ],
        ),
        "gerund": ("sprawdzenie", [("sprawdzić", "ger:sg:nom.acc:n:perf:aff")]),
        "inflected": (
            "kontekście",
            [("kontekst", "subst:sg:loc:m3"), ("kontekst", "subst:sg:voc:m3")],
        ),
        "other": ("oczywiście", [("oczywiście", "adv:pos")]),
    },
    "impersonal": {
        "unknown": ("page_no", []),
        "impersonal": ("dodano", [("dodać", "imps:perf")]),
        "adverb": ("zarówno", [("zarówno", "adv"), ("zarówno", "conj")]),
        "inflected": ("powinno", [("powinien", "winien:sg:n:imperf")]),
        "other": ("to", [("ten", "adj:sg:nom:n:pos"), ("to", "subst:sg:nom:n")]),
    },
}


@pytest.mark.parametrize(
    "probe, expected",
    [(probe, name) for probe, classes in EXAMPLES.items() for name in classes],
)
def test_each_class_is_reached_by_the_word_that_defines_it(probe, expected):
    word, readings = EXAMPLES[probe][expected]
    assert PROBES[probe].classify(Match.of(word, readings)) == expected


def test_every_class_a_probe_declares_is_one_some_word_reaches():
    """A class an earlier one shadows is dead, and the report cannot say so.

    It prints no row where nothing reached a class, which is also what a class
    that is doing its job looks like on a corpus that happens to hold none of it.
    """
    assert {name: {c.name for c in probe.classes} for name, probe in PROBES.items()} == {
        name: set(classes) for name, classes in EXAMPLES.items()
    }


@pytest.mark.parametrize("probe", PROBES.values(), ids=lambda probe: probe.name)
def test_a_probe_answers_for_a_word_none_of_its_classes_names(probe):
    """The last class holds unconditionally, and nothing but this says so.

    A probe declared without one classifies most of a corpus and then raises on
    the first word that surprises it, halfway through a run over a corpus.
    """
    assert probe.classify(Match.of("cokolwiek", [("cokolwiek", "qub")]))


def test_a_verb_read_as_a_gerund_too_is_filed_as_a_verb():
    """The branch order is the finding, so it is what this pins.

    Testing for the gerund first would file every `zostanie` as the
    nominalization the rule is aimed at, and the totals would not show it.
    """
    word, readings = EXAMPLES["nominalization"]["verb"]
    assert "ger" in {tag.split(":")[0] for _, tag in readings}
    assert PROBES["nominalization"].classify(Match.of(word, readings)) == "verb"
