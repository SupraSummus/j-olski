"""What an ending finds when the analyser is asked what it matched.

[Milestone 2](../docs/roadmap.md) files the plain-Polish pack at tier A on the
strength of an ending: a rule matches a suffix, so it ships before the analyser
does. What that costs is every other word the ending also ends, and the roadmap
names the cost lexically — ``zdanie`` and ``mieszkanie`` are not zombie nouns.

This is the program that reads the cost off a corpus instead of predicting it.
For every word an ending matches it asks Morfeusz what the word is, and sorts
the answer into classes.

The classes are the declaration and not the program, because an ending is a
question and different endings ask different ones. ``-anie`` asks whether a word
is a nominalization, where a gerund reading beside a nominal one is the
undecidable case; ``-no`` asks whether a word is an impersonal verb form, where
that same nominal reading is an adverb and the whole of the contamination. One
class set over both would have to name the union and would answer neither, which
is why a :class:`Probe` carries its own.

It lives here rather than in ``olski`` because it asserts nothing about Polish.
It reports what an ending matched, which is evidence for a rule that does not
exist yet, where a rule in the linter is a claim that already stands.

    python3 -m harness.endings proza/ --probe nominalization
"""

import argparse
import collections
import pathlib
import sys
from collections.abc import Callable
from dataclasses import dataclass

from olski.document import WORD, is_plain_text

#: Tags that make a reading a finite verb rather than a noun. ``ger`` is absent
#: because a gerund is what the nominalization probe is aimed at, and ``imps``
#: because it is what the impersonal one is aimed at.
FINITE = frozenset(("fin", "bedzie", "praet", "impt", "inf", "aglt", "winien"))


@dataclass(frozen=True)
class Match:
    """One matched word, with what the analyser said about it."""

    word: str
    tags: frozenset
    lemmas: frozenset

    @classmethod
    def of(cls, word, readings):
        return cls(
            word=word,
            tags=frozenset(tag.split(":")[0] for _, tag in readings),
            lemmas=frozenset(lemma.split(":")[0].lower() for lemma, _ in readings),
        )

    @property
    def unread(self) -> bool:
        return not self.tags or "ign" in self.tags

    @property
    def inflected(self) -> bool:
        """The word is a form of some other word, so a lemma would not match it."""
        return self.word.lower() not in self.lemmas


@dataclass(frozen=True)
class Class:
    name: str
    gloss: str
    holds: Callable[[Match], bool]


@dataclass(frozen=True)
class Probe:
    """An ending, and the classes the words it matches are sorted into.

    The classes are ordered and a word falls into the first that holds, so the
    order is part of the declaration. The last one holds unconditionally, which
    ``tests/test_endings.py`` requires: a word the analyser read and no class
    claimed would otherwise leave the report summing to less than its own total.
    """

    name: str
    endings: tuple
    classes: tuple

    def classify(self, match: Match) -> str:
        return next(c.name for c in self.classes if c.holds(match))


NOMINALIZATION = Probe(
    name="nominalization",
    endings=("anie", "enie", "cie"),
    classes=(
        Class("unknown", "no reading", lambda m: m.unread),
        Class(
            "verb",
            "a verb form, which a lemma alone does not settle",
            lambda m: bool(m.tags & FINITE),
        ),
        Class(
            "ambiguous",
            "gerund and ordinary noun both, which no analyser separates",
            lambda m: "ger" in m.tags and "subst" in m.tags,
        ),
        Class(
            "gerund",
            "a gerund and nothing else, the rule's intended target",
            lambda m: "ger" in m.tags,
        ),
        Class(
            "inflected",
            "an inflected form of another word, which a lemma removes",
            lambda m: m.inflected,
        ),
        Class(
            "other",
            "no verb behind it and no other lemma: an adverb, a numeral, a name",
            lambda m: True,
        ),
    ),
)

IMPERSONAL = Probe(
    name="impersonal",
    endings=("no", "to"),
    classes=(
        Class("unknown", "no reading", lambda m: m.unread),
        Class(
            "impersonal",
            "the -no or -to form the rule is aimed at",
            lambda m: "imps" in m.tags,
        ),
        Class(
            "adverb",
            "an adverb, which the ending reaches and the rule does not want",
            lambda m: "adv" in m.tags,
        ),
        Class(
            "inflected",
            "an inflected form of another word, which a lemma removes",
            lambda m: m.inflected,
        ),
        Class("other", "a word of some other part of speech", lambda m: True),
    ),
)

PROBES = {probe.name: probe for probe in (NOMINALIZATION, IMPERSONAL)}


def read(analyser, word):
    return [(a[2][1], a[2][2]) for a in analyser.analyse(word)]


def words(paths):
    """Every word of every file ``olski`` would read, tokenized as it tokenizes.

    Both halves of that are the linter's, and neither is restated here. A rate
    printed against a denominator of this program's own is not the rate its
    neighbours print, which ``harness/counts.py`` gives the general form of, and
    a walk of this program's own would reach a different set of files than the
    run whose figures this one stands beside.
    """
    for path in paths:
        for file in sorted(p for p in path.rglob("*") if p.is_file()):
            if is_plain_text(file):
                yield from WORD.findall(file.read_text(encoding="utf-8"))


def report(probe, corpus, analyser, show=6):
    """Print one row per class per ending, skipping the classes nothing reached."""
    for ending in probe.endings:
        matched = [w for w in corpus if w.lower().endswith(ending)]
        counted = collections.defaultdict(collections.Counter)
        for word in matched:
            match = Match.of(word, read(analyser, word))
            counted[probe.classify(match)][word.lower()] += 1
        rate = 1000 * len(matched) / len(corpus) if corpus else 0
        print(f"\n-{ending}: {len(matched)} matched, {rate:.1f} per 1000 words")
        for klass in probe.classes:
            counts = counted[klass.name]
            total = sum(counts.values())
            if not total:
                continue
            share = 100 * total / len(matched)
            head = ", ".join(f"{w}({n})" for w, n in counts.most_common(show))
            print(f"  {klass.name:11} {total:4}  {share:5.1f}%  {klass.gloss}")
            print(f"              {head}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="+", type=pathlib.Path)
    parser.add_argument("--probe", action="append", required=True, choices=PROBES)
    parser.add_argument(
        "--show",
        type=int,
        default=6,
        help="how many of each class's commonest words to print",
    )
    args = parser.parse_args(argv)

    # Imported here and not at the top so that the probes and their test run
    # where the Morfeusz wheel does not build, as tests/test_morph.py already
    # needs.
    import morfeusz2

    analyser = morfeusz2.Morfeusz()

    corpus = list(words(args.paths))
    print(f"{len(corpus)} words")
    for name in args.probe:
        report(PROBES[name], corpus, analyser, args.show)


if __name__ == "__main__":
    sys.exit(main())
