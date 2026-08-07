# Work to do in the repository

The running list of work inside the repository itself:
rewrites, merges, documents that have drifted apart,
dangling references, gaps, and code worth improving.
Something noticed while working on another topic lands here
instead of stretching the current change or being forgotten.
The second inflow is [the review pass](CLAUDE.md#the-review-pass):
a refactor too large to do on the spot comes down to this list,
and the review also checks whether a change deleted the entries it closes.
Look here before starting new work —
the list doubles as a map of the places that sag.

An entry belongs here only if a commit in this repository closes it.
A question the outside world answers —
a measurement, which human Polish counts as the good half of the corpus,
a fork not yet taken —
is not work in the repository,
and the document that owns the topic keeps it:
[`docs/open-questions.md`](docs/open-questions.md)
or a document's own `Not yet decided`.
The next move is the tell:
waiting for somebody else's answer is an entry there,
a file to write is an entry here.

A register, not a changelog:
an entry that closes, or that turns out to have been misjudged,
is deleted by the same commit that settles it,
which is the done-marker rule from
[`CLAUDE.md`](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
applied to this file.

One paragraph per entry, paragraphs separated by a blank line,
without bullets, numbering or headings,
so that adding or removing an entry gives a clean diff
and leaves its neighbours alone.
Inside a paragraph the lines break
[semantically](CLAUDE.md#semantic-line-breaks).
Write so that the entry can be picked up cold,
and name the concrete next move —
what actually has to change in the text or in the code.
"Check some day" is a hope, not a move.

Every rate in [`docs/generated-polish.md`](docs/generated-polish.md#what-was-measured)
except the walk-on share
was produced by an extraction written once and thrown away,
so the document reports numbers this repository cannot recompute.
Milestone 1 needs the harness regardless,
and what is left of its first half is the output format:
the CLI reads every file into one corpus before any rule runs,
so a per-rule firing rate over that corpus
is a way of printing the run it already does,
not a new subsystem.
What that mode cannot do alone is rank rules by discrimination,
which needs the human half of the pair,
so it ships as a one-sided report or not at all.

Nothing in this repository turns a Markdown corpus into the prose
[the harness has to measure](docs/roadmap.md#milestone-1-the-calibration-harness),
and the checks that measure a whole file decline rather than guess,
so the corpus that [docs/generated-polish.md](docs/generated-polish.md#what-was-measured) reports on
cannot be measured here at all.
An extraction outside the `olski` package fixes that,
since milestone 0 keeps document formats out of the linter itself.
What it owes on arrival is an account of what it invents:
the two throwaway extractions both delete inline markup
and leave the space that stood in front of it,
which takes `space-before-punctuation` from 8 findings over the notes to 92,
so an unaccountable extractor trades one set of false findings for another.
The obvious first shape is the smallest one that serves the harness —
frontmatter, fenced code, headings, tables and trailing link lists dropped,
inline markup replaced by the text it wrapped rather than deleted,
hard-wrapped paragraphs joined —
and a test over a fixture carrying each of those.
It also brings that document's rates under
[the check CLAUDE.md asks of the corpus tables](CLAUDE.md#checks):
a run somebody can redo,
so a change to what counts as a word moves a number a person can correct
instead of one nothing will catch.

`pattern-density` expresses a ceiling and nothing else.
`_validate_density` in `olski/checks.py` requires `max_per_1000_words`,
and the check returns without a hit whenever the rate sits at or below it.
Fact density in
[`docs/linter.md`](docs/linter.md#candidate-rule-inventory) runs the other way:
dates, numerals and proper nouns all match at tier A,
and what the source reports is that generated text carries too few of them,
so a rule already on the inventory cannot be written with the parameters
the check accepts.
The move is a `min_per_1000_words` beside the ceiling,
both optional and at least one required,
plus a reported field naming which side fired,
because `limit` alone leaves a message unable to say
whether the text ran hot or cold.
`_bounds` and `_outside` in `olski/checks.py`
do that validation and that comparison for `length-variation`,
so what is left is calling them and settling `min_count`,
which skips a scope with too few matches
and would therefore skip what a floor rule is looking hardest for:
a document with no numerals in it at all.

`docs/corpus.md` twice points at a list that does not hold what it promises.
The past tense is "the obvious next thing to do"
and valency "belongs on the same list as the past tense",
while [what olski does not cover yet](docs/subset.md#what-it-does-not-cover-yet)
holds the copula, coordination, subordination, negation, numerals and pronouns
and neither of those two.
Either both go on that list,
which then has to say whether valency is a construction it is missing
or a gap of another kind,
or the two sentences in `docs/corpus.md` stop pointing at it.

The check table in `docs/rules.md` copies data owned by `olski/checks.py`.
Its `Reports` column restates the `fields` set each check registers,
and the `params=dict(...)` blocks restate what each validator accepts,
so both drift silently as soon as a check gains a parameter.
Either the CLI grows a `--list-checks` output that the document points at,
the way it already points readers at `--list-rules`,
or the table stays hand-written and a test asserts it against `CHECKS`,
the way `tests/test_docs.py` holds the links in the prose.
Pick one and the document stops being a second copy.

Without Morfeusz 2 installed,
`tests/test_morph.py`, `tests/test_subset.py` and `tests/test_corpus.py`
fail during collection, which aborts the entire run,
so an environment where the wheel did not build reports zero tests
rather than the linter-track tests it could have run.
`pytest.importorskip("morfeusz2")` at the top of the three modules fixes it.
The question to settle first is whether a silent skip is acceptable
while nothing but a human run notices it.

`olski-corpus` asks Składnica whether a sentence derives at all,
where the same treebank supports a sharper question.
Świgra's evaluation walks its packed forest per sentence
and counts the trees consistent with the corpus disambiguation
(see [`docs/swigra.md`](docs/swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)),
so coverage becomes whether the gold reading is among the readings
and how deeply it is buried,
rather than whether anything came out at all.
This is ordered behind the chart parser
that the implementation note in `olski/parse.py` defers,
because the enumerator builds no forest to walk
and caps enumeration at `MAX_READINGS`,
which is exactly the tail a burial-depth number would be measuring.

[`docs/roadmap.md`](docs/roadmap.md) describes the optional grammar track
as a parts list — Earley, parse forests, free word order and LCFRS —
and never says what the track is for.
The purpose is stated in
[`docs/swigra.md`](docs/swigra.md#what-it-leaves-open) instead,
which reaches it by surveying somebody else's parser:
reporting ambiguity to the author rather than resolving it for them
is the ground that survey found unoccupied.
That belongs in the roadmap section owning the track,
above its machinery,
and then `swigra.md` restates it in a clause and points there.

The repository ships no licence.
`pyproject.toml` carries no `license` field and there is no `LICENSE` file,
so the terms under which any of this may be used are unstated.
The move is to pick one, add the file,
and set `license` in `pyproject.toml` to match.
Reading a GPL v3 parser of Polish is what raised it
(see [`docs/swigra.md`](docs/swigra.md#why-wrapping-it-does-not-get-there)),
and the answer decides whether olski could ever link against such a thing.

Nothing runs `ruff check .` and `python3 -m pytest` except a person
who remembers to.
A workflow under `.github/workflows/` would run both,
plus `markdownlint` over the prose, on every push.
Against it: the project is for fun,
and a red badge on a hobby repository is a way of making it feel like work,
which is the same argument `docs/roadmap.md` uses for having no dates.
Decide it once and either add the workflow or write the decision
into the roadmap's guiding principle so it stops coming up.
