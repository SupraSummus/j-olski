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

A triple-backtick code span opening a line is read as a code fence,
and `harness/markdown.py` then drops the prose down to the next fence-only line.
`FENCE` in that module matches ```` ``` ```` and takes the rest of the line
as an info string,
where CommonMark forbids a backtick inside a backtick fence's info string,
so ```` ```KOD I``` zawiera link ```` is a paragraph to a renderer
and an opening fence to the extraction.
Three of the 32 `ksef-docs` files are written that way,
`kody-qr.md`, `tokeny-ksef.md` and `uwierzytelnianie.md`,
and between them they lose the better part of a thousand words
of running Polish;
[the corpus](docs/firing-rates.md#the-audit-corpus) owns how much exactly,
and reports its figures as the corpus stands.
The move is the CommonMark condition in `FENCE`,
plus the closing-fence test that goes with it,
and then rerunning the three sets of tables that hold extracted figures:
[`docs/audit-corpus.md`](docs/audit-corpus.md#the-list),
[`docs/extraction.md`](docs/extraction.md#an-inline-construct-leaves-its-text-or-takes-the-space-with-it)
and [`docs/firing-rates.md`](docs/firing-rates.md#the-rates).
The evidence to read is the prose the three `ksef-docs` files extract to,
since the fix is only worth the rerun if what comes back is Polish
rather than more of the code the fence was swallowing.

The line that says what a walk went past counts a repository's `.git` with it.
`_collect` in `olski/cli.py` reaches every file under a named directory,
so `olski rit-dokumentacja/` reports going past 39 files
in `.sample`, no suffix, `.md`, `.png`, `.idx`, `.pack` and `.rev`,
where the 7 Markdown files are the only ones a reader would have guessed at
and the pack and index files are git's own.
The walk always descended there and the count is what made it visible,
which is the warning working rather than a second defect.
The move is for the walk to skip a directory whose name begins with a dot,
and to say in `_collect` that a repository is the expected input
and its version control is not part of the corpus.
Against it: a dotted directory somebody names outright is then unreachable,
so the skip belongs to the walk and not to the suffix test.

Nothing in the harness says which construct a finding came out of,
so every audit of extracted prose maps its hits back by hand.
`docs/extraction.md` did it for a couple of hundred spacing findings,
and [the audit corpus's tables](docs/firing-rates.md#what-the-hits-over-the-audit-corpus-turned-out-to-be)
for more than a thousand hits,
both with a throwaway script and neither with anything reusable.
The classes that cost the most to reach are the ones a program could settle:
whether a hit stands in a table, a code span, a link's text or a raw tag.
So the move is for `prose` in `harness/markdown.py`
to record what each stretch of output came from,
and for something to print that beside a finding —
which is a second output from the extraction
and wants deciding whether it rides along with the prose files
or is a separate mode over one document.
Against it: the classes that decide whether a hit is a *defect*
are the ones needing a reader anyway,
so this halves an audit rather than removing it,
and a corpus of this size can be read by hand, as it twice already has been.

`docs/extraction.md` compares one member of the audit corpus against its files
and the corpus has two.
Its table runs the notes, the memoir and `ksef-docs` twice each,
where [`docs/firing-rates.md`](docs/firing-rates.md#the-audit-corpus)
audits `rit-dokumentacja` beside `ksef-docs`
and finds the extraction's own gaps accounting for 553 of the corpus's findings,
every one of them in that second member.
The move is a fourth column,
which means running `rit-dokumentacja` with its names changed to `.txt`
and checking the spacing findings one by one against their source
the way the section's own method demands,
since a count that agrees is not yet a hit that points at the same place.

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

The engine tells a declined file from a declined scope by comparing a reason string.
`_tally` in `olski/engine.py` subtracts the two differently,
since a rule that declined a file never saw the scopes in it
where one that declined a scope saw that scope and no other,
and what it tells them apart with
is whether the reason equals `NOT_PLAIN_TEXT`.
Every abstention the checks can raise is classified right by that test,
so this is about the next one rather than about a wrong number in a report:
a rule declining a whole document for any other reason
counts as having declined a single scope.
Give `line-end-word` the wrap precondition
the entry on where a file wraps asks for,
and declining a 50-line file leaves 49 of its lines in the denominator.
The move is to make the width part of the outcome instead of reading it off the prose,
with an `Abstain` saying whether it refuses a scope or the whole file,
which also relieves `NOT_PLAIN_TEXT` of doubling as a tag,
a job `olski/checks.py` documents it as having.
That entry is what makes this reachable,
so whoever picks it up needs this as well.

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
Its `Reports` column restates what each check's `fields` answers,
and the `params=dict(...)` blocks restate what each validator accepts,
so both drift silently as soon as a check gains a parameter.
`fields` is a function of a rule's validated parameters,
which the `pattern-density` row carries as a condition in prose,
so whichever move is picked reaches a check's fields through some rule's parameters.
Either the CLI grows a `--list-checks` output that the document points at,
the way it already points readers at `--list-rules`,
or the table stays hand-written and a test asserts it against `CHECKS`,
the way `tests/test_docs.py` holds the links in the prose.
Pick one and the document stops being a second copy.
Either option waits on the entry
that makes a check's fields a function of its validated parameters,
since both read a set that is about to become a call.

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
