# Roadmap

A high-level ordering, not a schedule.
There are no dates,
because the project is for fun
and a dated plan for a hobby is a way of making it feel like work.

Each milestone has an exit criterion,
because "when is this done" is the only part of planning
that reliably pays for itself.

## What is being built

A style linter for Polish technical documentation,
used among other things
to check texts produced by language models.
See [linter.md](linter.md).

The grammar and parser work described in
[design-notes.md](design-notes.md)
is no longer the goal.
It survives as the deepest analysis tier,
reached only by rules that genuinely need it,
and as an optional track pursued for its own sake.

## Guiding principle

Rules are cheap to invent and worthless uncalibrated.
Build the measurement before building the rule set.

That is also the field's own account
of why models write usable code and unreadable prose:
code came with a verifier and prose did not.
See [fiction.md](fiction.md#why-this-happens).
The account carries its own warning,
because a verifier teaches only what it checks —
[generated-polish.md](generated-polish.md#what-happened-when-the-rules-were-deleted)
records a body of Polish edited into its detectors' image.

## Milestone 0: rule engine and the typography pack

A rule engine over plain Polish text,
plus the rules that need nothing but a tokenizer:
em dash frequency,
Polish quotation marks,
single-letter words at line end,
spacing artifacts.

Rules live in data, not in code,
carry an identifier, a message, a register pack,
and a recorded justification.

Markup formats are not in scope.
This is a linter for Polish, not a document-format library,
and separating prose from markup
belongs to whatever reads the markup, not here.

**Exit:** the engine runs over a plain Polish text file
and reports findings with locations,
and adding a rule requires editing data rather than code.
Met, see [rules.md](rules.md).

## Milestone 1: the calibration harness

Before the interesting rules, the thing that makes them honest.

- A paired corpus:
  human Polish across registers,
  and generated Polish from several models on comparable topics
- Per-rule measurement:
  firing rate on generated text,
  firing rate on good human text
- A report that ranks rules by discrimination
  and names the ones that fire equally on both

Both halves reach the rules as plain text,
because milestone 0 keeps document formats out of olski
and that makes the extraction a step before the harness rather than part of it.
[generated-polish.md](generated-polish.md#the-apparatus-biases-a-rate-by-an-amount-the-corpus-decides)
prices skipping it:
one rule reads a quarter high over one body of Markdown
and true over another by the same writer,
so a rate measured over apparatus is not comparable
to a rate measured over prose,
nor to the next corpus's rate over its own apparatus.

**Exit:** every rule from milestone 0 carries two numbers,
and at least one rule has been deleted for failing them.

That last clause matters.
A calibration harness that never kills a rule
is not measuring anything.

## Milestone 2: morphology binding

Deferrable further than it first looked.
Nominalization density and impersonal `-no` and `-to` forms
are suffix patterns,
so much of milestone 3 can be written at tier A.
See [linter.md](linter.md#suffixes-buy-more-than-expected).
Real morphology is needed only
once lexical rules are keyed by lemma.

Lemmatization and part-of-speech tagging,
so lexical rules match inflected forms
and morphosyntactic rules become possible.

Morfologik is the likely choice over Morfeusz here:
it is what LanguageTool already uses for Polish,
it is freely licensed,
and this project needs analysis rather than generation.

Whichever analyser wins,
it owes its callers character offsets and not just forms,
because a finding is a location and an analysis is not:
`Segment` in `olski/morph.py` carries node numbers of a segmentation graph,
which is the shape of the problem rather than an accident of Morfeusz.

**Exit:** a lexical rule written as a lemma
catches every inflected form of it in running text,
and its findings point at the forms they matched.

## Milestone 3: the plain-Polish pack

The rules with a citable Polish norm behind them,
which are also, conveniently, model tells:

- Rzeczowniki zombie, `-anie` and `-enie` and `-cie` density
- The phrases that invite them,
  `w celu`, `w razie`, `z powodu`, `na skutek`
- Impersonal `-no` and `-to`, and `się` passives
- `można`, `trzeba`, `należy`, `warto`

Each rule cites the plain-Polish source it comes from,
not a model it was observed in.

**Exit:** the pack is calibrated,
and its false-positive rate on edited human technical documentation
is written down and acceptable.

## Milestone 4: statistical rules

Sentence-length variance,
paragraph-length uniformity,
lemma type-token ratio,
fact density,
three-item list frequency,
connector density.

These need thresholds, not just patterns,
and thresholds need the corpus from milestone 1.
StyloMetrix from NASK is worth evaluating here
rather than reimplementing feature extraction.

**Exit:** thresholds derived from the corpus rather than chosen,
with the derivation recorded.

## Milestone 5: the delivery decision

Three routes, decided once there is something worth delivering:

- A standalone tool with its own rule format
- A Vale-compatible style,
  inheriting its editor and CI integration
- LanguageTool XML rules,
  inheriting an installed base and Morfologik

**Exit:** a decision with its reasoning recorded.

## Milestone 6: deeper analysis, only where earned

Chunking or dependency parsing,
for the rules that need constructions rather than strings:
subject-predicate distance,
clause depth,
parallel-negation frames.

**Exit:** at least one rule that could not work at tier B
working at tier C,
with the added machinery justified by that rule's calibration numbers.

## Optional track: the grammar

Everything in [design-notes.md](design-notes.md)
about Earley, parse forests, free word order and LCFRS.

It is not on the critical path for the linter.
It remains the more interesting computational problem,
and the project is for fun,
so it stays in the repository as a track that may be picked up
whenever the linter stops being the more entertaining thing to work on.

If it is ever built,
the linter gains tier D
and the grammar gains a reason to exist.

## Wish, not milestone: prose and fiction

Making language models write good Polish fiction
is an open research question,
and [linter.md](linter.md#and-fiction) records
what is lintable there,
what is not,
and the three directions that look more promising than linting:
generative constraints,
stylometric targets rather than stylometric alarms,
and the linter as a deterministic critic inside a revision loop.
[fiction.md](fiction.md) surveys the research underneath that:
the documented failure modes,
and the finding that post-training rather than prompting produces them.

Deliberately not a milestone.
Labelling a research question as a deliverable
is how hobby projects die.

## What would count as finished enough

- A rule pack for Polish technical documentation
  where every rule has a measured discrimination
  and a stated justification
- Run over a real document,
  producing findings a Polish technical writer agrees with
- At least one rule deleted because the numbers said so
- Honest documentation of what the tool does not do,
  starting with the fact that it is not a detector

None of that requires the project to be useful,
and all of it would be novel for Polish.
