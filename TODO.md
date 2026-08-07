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

An entry names the evidence it has to read,
and not only the files it changes.
Two entries can edit disjoint files
and still turn on one judgment about one body of text,
such as what a rule's hits over a corpus are.
A file list does not show that overlap,
so the two are picked up together
and the judgment is reached twice.

Only one of the corpora in
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken)
reaches the rules through a program this repository holds.
`harness/markdown.py` reads Markdown,
which is what the KSeF figures there are taken with,
while NKJP is XML, Śmigiel is JSONL,
`python-docs-pl` is PO files and Wolne Lektury is plain-text exports,
so every figure over those is still counted by hand.
One of the four needs no extraction at all,
since a text export is what olski reads,
and what it needs instead is a selection anybody can repeat:
the Wolne Lektury count in that document
runs over "the first forty `Epika` entries the catalogue returns",
which is not an order to rerun into.
[`docs/firing-rates.md`](docs/firing-rates.md#wolne-lektury)
already fetches the same library by naming every slug it takes,
so that half is a rewrite of one paragraph rather than a program.
The move is to decide, per corpus, whether it joins the harness
as an extraction beside the Markdown one,
as a fetch-and-select command in the document that cites it,
or not at all because the survey has already ruled the corpus out.

The documentation half of [`docs/firing-rates.md`](docs/firing-rates.md#the-rates)
audits the pack over apparatus that the harness can now take away.
Its KSeF column is the 32 Markdown files as they stand,
where `missing-space-after-full-stop` fires 748 times for one defect
and `trailing-space` 426 times for none,
and [`docs/extraction.md`](docs/extraction.md#an-inline-construct-leaves-its-text-or-takes-the-space-with-it)
holds what the same rules report over the extracted prose.
Two readings of one corpus in two documents is one too many.
The move is to make the audit's documentation column the extracted one,
since that is the corpus
[the audit corpus](docs/corpora.md#the-audit-corpus-polish-documentation-in-version-control)
will actually be,
and keep the as-they-stand figures only where they are the argument
for extracting at all.
That means rereading the hits, not just recounting them:
156 hits of a rule are a different audit from 748.

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

A rate rule's denominator counts scopes the rule could never have judged.
`pattern_density` in `olski/checks.py` tests its bounds before its two floors,
so a scope reaches `min_words` only when it was about to be reported,
and `min_count` turns away a scope above the ceiling by returning rather than abstaining.
[The pilot run](docs/firing-rates.md#what-the-report-mode-did-when-rules-declined)
gives both halves a number:
283 of the 291 documents in one denominator
hold fewer words than `em-dash-density` needs to answer at all,
and of 38 scopes over the threshold that went unjudged, 34 left no record.
Settle first whether falling under a floor is a decision.
If it is, `min_count` abstains as `min_words` does,
and the floors are tested before the bounds so that every scope failing one says so.
If it is not, `measured` subtracts the scopes that fail a floor,
so that a share is taken over what the rule could reach.
The present code does neither, and reports a denominator
that describes the corpus rather than the rule.

`orphan-single-letter-word` reads the Roman numeral `I` as the conjunction `i`.
Folding case is right for `A` and `W` opening a sentence
and wrong for the numeral Polish numbers its chapters and its monarchs with:
70 of the 124 hits over
[the pilot corpus](docs/firing-rates.md#orphan-single-letter-word-fired-124-times-and-found-nothing)
are `Tom I`, `Rozdział I` and `Mieszko I`.
The rule cannot fix this by itself,
because `case_sensitive` is one flag for the whole word list
and the list needs `i` folded and `I` not.
So either that parameter becomes a per-word one,
or `line-end-word` grows the exemption `pattern` already carries
in `unless_preceded_by` and `unless_followed_by`,
which is the smaller change and buys precision back the way the pack does elsewhere.

A directory walk that skips files says nothing about having skipped them.
`_collect` in `olski/cli.py` takes `.txt` and `.text` out of a directory
and passes over everything else without a word,
so `olski ksef-docs/` over a repository of 32 Markdown files
lints its `LICENSE.txt` and prints a nine-row report over 169 words of English.
`_note_markup` beside it has the shape the fix wants:
one line to stderr, counted off the run rather than off the input,
saying how many files the walk passed by
and that naming them on the command line is what reaches them.
Settle first whether that line names the suffixes it skipped,
which is what tells a reader to reach for a converter
rather than for a different directory.

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
