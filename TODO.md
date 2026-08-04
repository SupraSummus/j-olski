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
was produced by an extraction written once and thrown away,
so the document reports numbers this repository cannot recompute.
Milestone 1 needs the harness regardless,
and the first half of it is small:
the CLI already walks a directory and already builds a `Report`,
so a per-rule firing rate over a corpus
is an output format over the run it already does,
not a new subsystem.
What that mode cannot do alone is rank rules by discrimination,
which needs the human half of the pair,
so it ships as a one-sided report or not at all.
Note also that `TEXT_SUFFIXES` keeps Markdown out on purpose,
and the corpus that prompted this is Markdown:
either the extraction lives outside olski and the document says where,
or the markup boundary in `olski/cli.py` gets revisited deliberately.

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

Nothing runs `ruff check .` and `python3 -m pytest` except a person
who remembers to.
A workflow under `.github/workflows/` would run both,
plus `markdownlint` over the prose, on every push.
Against it: the project is for fun,
and a red badge on a hobby repository is a way of making it feel like work,
which is the same argument `docs/roadmap.md` uses for having no dates.
Decide it once and either add the workflow or write the decision
into the roadmap's guiding principle so it stops coming up.
