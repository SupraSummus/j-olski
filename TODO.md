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

Two documents give the same repository two counts of the same character
and one of them says they are the same count.
[`docs/firing-rates.md`](docs/firing-rates.md#the-quotation-mark-rules-had-nothing-to-find)
splits 978 hits of `quote-straight` over the KSeF Markdown into 646 in code
and 332 in running prose,
and calls that 332 the figure the survey took by hand,
where [`docs/corpora.md`](docs/corpora.md#polish-technical-documentation-original-and-translated)
now reports 312 over the same 32 files,
having stopped counting by hand when the extraction arrived.
The evidence is the same repository at the commit
[`docs/audit-corpus.md`](docs/audit-corpus.md#the-list) pins,
read twice: the raw Markdown with its code split off by a reader,
and the extracted prose, which keeps an inline code span and drops a fenced block,
so the two disagree by whatever falls in that gap.
The move is to find where the 20 marks are and say so in the sentence,
or to drop the claim that the two numbers are one number.
This reads the same hits as the entry on the audit's documentation column,
so the two are picked up together.

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
[the audit corpus](docs/audit-corpus.md#the-list) is,
and keep the as-they-stand figures only where they are the argument
for extracting at all.
That means rereading the hits, not just recounting them:
156 hits of a rule are a different audit from 748.
It also means both members rather than the first,
which is what turns the column from a repository into a corpus,
and the two do not fire alike:
`missing-space-after-full-stop` reports 156 hits over `ksef-docs` and none over
`rit-dokumentacja`, and `missing-space-after-punctuation` 10 against 195.
This reads the same hits as the entry
on the two counts of the same character, so the two are picked up together.

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

`line-end-word` reads where a file wraps and reports it as where a page wraps.
The check's docstring in `olski/checks.py` says the judgement depends on
where lines break in the output,
and takes a plain-text suffix as the evidence that they do,
which [`docs/rules.md`](docs/rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives)
prices as weaker evidence than it reads as.
[The pilot](docs/firing-rates.md#orphan-single-letter-word-fired-124-times-and-found-nothing)
is that price paid: 124 hits over a corpus of `.txt` and not one of them the defect,
because the export sets a paragraph on one line however long it runs,
and 35 of the 124 are a word ending a paragraph rather than a line.
The evidence the suffix stands in for is in the file itself:
a document wrapped to a width has its line lengths clustered under one,
where a paragraph-per-line document has a long tail.
So the move is a precondition on the document rather than an exemption in the rule,
with `line-end-word` abstaining where the lines were not wrapped to a width,
the way a rate rule abstains on a document too short to measure.
Settle first whether that reading belongs to the check or to `Document`,
since it is a property of the file
and every later rule that counts lines would ask the same of it.
This reads the same 124 hits as the entry on the Roman numeral,
so the two are picked up together.

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
Having the rule decline the pilot corpus outright,
which is where the entry on where a file wraps arrives,
removes the evidence rather than the false positive:
`Rozdział I` at the end of a line somebody wrapped to a width is still one.

`docs/corpus.md` and `docs/corpora.md` differ by two letters
and hold unrelated things:
the first measures the grammar against the Składnica treebank,
the second surveys the corpora the linter would calibrate against.
A link to either one reads the same,
and a grep for one of them finds both,
and finds `docs/audit-corpus.md` too,
which is about one of the corpora the second surveys.
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
Either option waits on the entry
that makes a check's fields a function of its validated parameters,
since both read a set that is about to become a call.

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

`Document` computes an analysis nobody asked for
and recomputes one everybody does.
`from_text` in `olski/document.py` splits paragraphs and sentences
for every document it builds,
where a run selecting only `pattern` rules reads neither,
and `word_count` runs `WORD.finditer` afresh on every call
from the three sites in `olski/checks.py` that reach for it,
once per rule and once per scope.
Neither costs much while every analysis here is a regex pass over the text.
Both are the shape the first expensive tier arrives in:
[the roadmap](docs/roadmap.md#milestone-5-morphology-binding-and-the-rules-that-needed-it)
puts an analyser behind a lemma rule,
and a typography run paying for morphology over a corpus
is this eagerness with a number attached.
The move is to make the analyses lazy and memoized
rather than fields set at construction,
which `functools.cached_property` does on a frozen dataclass,
since freezing replaces `__setattr__`
and the descriptor writes the instance dictionary directly.
The reason to make it before the analyser rather than alongside one:
the same change made afterwards
has to be made through whatever wired the analyser in.

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

The archives these documents send a reader to fetch are pinned by URL and by nothing else.
[Składnica](docs/corpus.md#fetching-it)
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
name a release in the query string of a wiki attachment,
and Świgra is `swigra_current.zip`, which names none,
so [`docs/swigra.md`](docs/swigra.md#what-was-read-and-what-was-not)
dates it by the timestamps of the files inside instead.
[The audit corpus](docs/audit-corpus.md#the-list) pins its members to a commit
and says what a pin is for:
so that a second person fetches the same bytes.
The archives make that promise
and give a reader no way to hold anyone to it.
The move is `sha256sum` over each one,
with the digest beside the command that fetches it,
which turns a substitution upstream into a failed check
rather than a figure that quietly stops reproducing.

The corpora these documents send a reader to fetch
come from hosts that gain nothing by serving them,
once per session rather than once per person,
because a Claude Code session on the web starts from an empty container.
[The Wolne Lektury run](docs/firing-rates.md#wolne-lektury)
takes 326 files at one request each from a volunteer library,
[Składnica](docs/corpus.md#fetching-it) is 92 MB
that [the checks](CLAUDE.md#checks) make a condition of touching the grammar,
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
is a tarball from the institute that serves Składnica.
The licences do not run in that order.
NKJP carries CC BY, which permits the redistribution a mirror is,
every Wolne Lektury file ships the library's licence in its own tail,
which that run cuts off before counting,
and Składnica is GPL,
which the fetching section raises against vendoring
and which settles nothing about mirroring,
since a mirror redistributes under Składnica's terms
whatever this repository decides about its own.
So the order of work is NKJP, Wolne Lektury, Składnica,
and the transport is the smaller half of each.
A release asset on a mirror repository holds 2 GB per file against no quota
and keeps the fetch the `curl -L` those sections print,
where git LFS asks for an install that the session clone precedes,
so tracked files arrive as pointer files and a hook has to pull them,
and spends an allowance that GitHub's billing documentation puts at
1 GB stored and 1 GB of bandwidth a month,
which is ten fetches of Składnica.
LFS buys that back over a binary somebody versions,
and these are frozen archives.
The audit corpus needs none of it,
being clones pinned to a commit, which is what a mirror would be.
None of this starts before the entry on digests,
since a mirror nobody can check against upstream
is the second copy of a fact that
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely) warns about.

The repository ships no licence.
`pyproject.toml` carries no `license` field and there is no `LICENSE` file,
so the terms under which any of this may be used are unstated.
The move is to pick one, add the file,
and set `license` in `pyproject.toml` to match.
Reading a GPL v3 parser of Polish is what raised it
(see [`docs/swigra.md`](docs/swigra.md#why-wrapping-it-does-not-get-there)),
and the answer decides whether olski could ever link against such a thing.

[Semantic line breaks](CLAUDE.md#semantic-line-breaks) cover
"prose in comments and docstrings", and no module here writes them that way.
Every file in `olski/` and `harness/` wraps its comments to a column instead,
a median comment line of 52 characters and a ninetieth percentile of 80,
so the rule and the code have disagreed for as long as both have existed
and a new docstring following the rule reads as a typo beside its neighbours.
Two ways out, and the choice is a judgement about the whole package
rather than about whichever function is being edited at the time:
narrow the rule in `CLAUDE.md` to Markdown, commit messages
and the prose fields of a declaration,
which is where the tighter diff is actually collected,
or keep the rule and reflow the docstrings under
[lazy adoption](CLAUDE.md#adopt-these-rules-lazily), file by file as they are touched.
The second answer also needs saying out loud,
because the mixed state it passes through is what a reader will read as drift.
