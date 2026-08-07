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
The same holds for the typographic counts in
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken),
which were taken by hand for the same reason
and which `olski --format report` prints once an extraction feeds it,
so retaking them is part of this entry rather than an entry of its own.

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

`docs/corpus.md` and `docs/corpora.md` differ by two letters
and hold unrelated things:
the first measures the grammar against the Składnica treebank,
the second surveys the corpora the linter would calibrate against.
A link to either one reads the same,
and a grep for one of them finds both.
The move is to rename `docs/corpus.md` to `docs/skladnica.md`,
which says what it holds and matches `docs/swigra.md` beside it,
and to carry the rename through
`CLAUDE.md`, `README.md`, this file,
`docs/design-notes.md`, `docs/prior-art.md`, `docs/subset.md`, `docs/swigra.md`,
and the citations in `olski/corpus.py`, `olski/coverage.py`, `olski/subset.py`
and `tests/test_subset.py`.
`tests/test_docs.py` catches the Markdown links and the citations in code,
and nothing catches the plain-prose mentions,
so those are the ones to grep for.

The check table in `docs/rules.md` copies data owned by `olski/checks.py`.
Its `Reports` column restates the `fields` set each check registers,
and the `params=dict(...)` blocks restate what each validator accepts,
so both drift silently as soon as a check gains a parameter.
Either the CLI grows a `--list-checks` output that the document points at,
the way it already points readers at `--list-rules`,
or the table stays hand-written and a test asserts it against `CHECKS`,
the way `tests/test_docs.py` holds the links in the prose.
Pick one and the document stops being a second copy.

A `pattern-density` rule that sets only `min_per_1000_words`
may use `{match}` in its message and render an empty string.
`Check.fields` in `olski/checks.py` is one set per check kind,
so the placeholder check in `Rule.__post_init__` measures a message
against everything the check can ever report,
while a finding below the floor reports a strict subset of that:
there is no occurrence to quote, which is the point of such a finding.
The move is to make a check's fields a function of its validated parameters,
which `Rule.__post_init__` already holds when it checks the message.
Against it: an empty placeholder shows itself the first time a rule runs,
where the mistake this guard was built for raises `KeyError` instead,
and a callable costs more to read than a frozenset.

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
into the roadmap's guiding principles so it stops coming up.

An uncalibrated rule does not say what it owes.
`--explain` prints `calibration: uncalibrated` and stops there,
so whoever takes the first measurement has to read `calibrated_by`
in `olski/checks.py` to learn whether a rule wants its hits read
or a threshold placed in a distribution of human Polish,
which is what decides
[which corpus they need](docs/roadmap.md#milestone-1-the-calibration-harness).
The move is to make the line one function
instead of the copy `_write_text` and `_list_rules` in `olski/cli.py` each hold,
and have it name the shape the check calls for while there is nothing measured.
Against it: the shape follows from the check kind,
and `docs/rules.md` states in a sentence which kind calls for which.
