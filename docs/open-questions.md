# Open questions

Decisions not yet taken.
The point of writing them down
is that none of them get made by accident.

Questions are grouped by which track they block.
Only the first group blocks the working goal.

## Settled

- The working goal is a style linter for Polish,
  scoped to technical documentation.
  See [linter.md](linter.md).
- The grammar and parser track is optional
  and pursued for its own sake,
  not on the linter's critical path.
  See [design-notes.md](design-notes.md).
- Olski is as close to Polish as possible,
  and a proper subset of it.
- No rule ships without a measured false-positive rate
  on good human Polish.
- The tool is a linter, not a detector,
  and must not be described as one.
- Two morphological dictionaries for two jobs:
  Morfeusz for generation on the grammar track,
  Morfologik for analysis on the linter track.

Further grammar-track decisions are recorded in
[design-notes.md](design-notes.md#decisions-taken).

## Linter questions

These block the working goal.

**Delivery route.**
Standalone tool with its own rule format,
a Vale-compatible style,
or LanguageTool XML rules over Morfologik.
The last inherits an installed base and a Polish morphology layer;
the first inherits nothing and owes nothing.

**Rule provenance policy.**
Every rule needs a justification,
and justifications anchored to Polish style norms
outlive justifications anchored to model fingerprints.
Open question is whether fingerprint rules are admitted at all,
and if so how they are dated and retired.

**Corpus sourcing.**
Which human Polish counts as the good side of the pair.
NKJP, Wolne Lektury, edited journalism, technical documentation,
and in what proportion.
The generated side is easy;
the human side determines everything the rules learn.

**How registers are configured.**
Rules belong to packs and packs belong to registers.
Whether a document declares its register,
or the tool guesses,
or the user picks a pack explicitly.

**Whether fiction gets a pack at all.**
Several metrics work for both registers with inverted thresholds,
which is cheap.
The rest of the fiction problem is not linting,
and is recorded as a wish rather than a plan.
See [linter.md](linter.md#and-fiction).

## Grammar-track questions

None of these block the linter.
They are the interesting problems,
which is a different thing.

### The big fork: may olski scramble

Polish permits left-branch extraction that splits a noun phrase
around the rest of the clause,
as in `Jakie Jan czyta książki?`.
Admitting that means discontinuous constituents,
which means leaving the context-free tier
for LCFRS, MCFG, or TAG,
and moving from cubic parsing to sixth power at fan-out two.

This is not a difficulty gradient.
It is the one place where the cost curve jumps by an exponent.
See [the cost ladder](design-notes.md#the-cost-ladder).

Refusing it keeps everything at tier 2.
Every other decision below is cheap next to this one.
It should probably be answered by measurement rather than taste:
find out what fraction of real Polish sentences need it
before paying for it.

### The rest of the subset

Each row is a real fork, not a difficulty level.
The `closeness` column notes which option
serves the settled goal of resembling Polish.

| Area | Cheap option | Expensive option | Closeness favours |
| --- | --- | --- | --- |
| Word order | Fix subject-verb-object | Dominance plus precedence constraints | Expensive |
| Subject | Require an overt noun phrase | Allow pro-drop | Expensive |
| Numerals | Exclude entirely | Full numeral agreement fictions | Expensive, but defer |
| Negation | Clause-wide `nie`, no case shift | Genitive of negation with propagation | Expensive |
| Clauses | Main clauses only | `że` and `który` subordination | Expensive |
| Coordination | Same-category only | Unlike categories, gapping | Unresolved |

Closeness to Polish argues for the expensive column nearly everywhere,
which is not a reason to build it all at once.

Numerals deserve a note:
they are extremely common in real Polish
and they are also a self-contained module,
so they are a good candidate
for being deferred rather than excluded.

### What the author writes

Three architectures, described at length in
[design-notes.md](design-notes.md#three-architectures).

1. A typed abstract syntax tree
2. Near-Polish text that gets parsed and validated
3. An unambiguous surface DSL that reads like Polish
   and elaborates into the AST

The working preference was the third.
The predictive-editor finding from the controlled-language literature
substantially rehabilitates the second:
with a look-ahead editor
the author writes something very close to Polish
and cannot produce an invalid sentence,
so the bad-diagnostics objection disappears.
See [design-notes.md](design-notes.md#the-predictive-editor-changes-this).

It decides whether the primary interface
is a batch checker over files
or an incremental one over a cursor.
Those are different programs.

### The round-trip guarantee

Restated as asymmetric:
tree to text is a function,
text to tree is a relation,
and the test is that the original tree
appears somewhere in the forest.

Still open:
whether to additionally rank the forest
and require the original tree to come out on top.
That is stronger,
and it means building a disambiguation preference,
which is where deterministic explainable systems usually stop being either.
Current inclination is not to.

A third option, cheaper than either ranking or resolving:
abstain when the forest holds more than one reading,
and treat the count itself as the confidence measure.
See [glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
for a system that does exactly this and nothing more,
including the one thing it gets wrong —
counting parses rather than *distinct* readings,
so an optional-whitespace rule
makes it abstain on lines it understood perfectly.

### How the grammar is authored

Grammar and lexicon should be one declarative source
feeding both the parser and the generator.
That source needs a format.

Open sub-questions:
a bespoke grammar file with its own parser,
an embedded DSL in the host language,
or literate prose with rules extracted from fenced blocks.
The repository already uses semantic line breaks for prose,
which makes the third option less absurd than it sounds.

Whatever the format,
[glr-in-practice.md](glr-in-practice.md#grammar-as-data-not-as-dsl)
argues the parser must accept a grammar as data,
because a precedence preprocessor generates productions
rather than writing them.

### What the output is

Plain text, Markdown, LaTeX, or HTML.
If a real typesetter is in the picture
then *skład* is literal
and the compiler needs a backend layer.

### Whether to publish a PENS coordinate

Applies only if the grammar track produces
an actual controlled natural language.
Kuhn's scheme classifies controlled languages,
and a linter is not one,
so this question belongs to this track alone.

The scheme would let olski state its position
on the same four axes as a hundred other controlled languages.
Doing so honestly requires
an exact and comprehensive language description,
which is the Simplicity axis by definition.
Committing to that is committing to write the spec properly.
It might be the most valuable artifact the grammar track could produce,
or an obligation that kills the fun.
Undecided.

## Shared questions

**Implementation language.**
Both tracks need one, and it need not be the same one.

- The linter wants whatever makes rules-as-data pleasant
  and has a usable Morfologik binding.
  LanguageTool is Java, which matters
  only if the delivery route goes through it.
- The grammar track wants good algebraic data types
  and pattern matching for writing Earley and a unifier,
  and Morfeusz has usable Python and C++ bindings.
- The project is for fun,
  so enjoying the language matters more than it usually would.
