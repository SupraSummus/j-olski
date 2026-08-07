# Design notes

Decisions that have been taken are marked as such;
everything still open lives in [open-questions.md](open-questions.md).

> **Scope.**
> This document describes the **grammar track**,
> which is optional and pursued for its own sake.
> The working goal of the repository is a style linter for Polish;
> see [linter.md](linter.md).
> The grammar survives here as the deepest analysis tier,
> reached only by rules that earn it,
> and as the more interesting computational problem.
> Read this second.

## What olski is

*Język olski* is *język polski* with the *p* filed off,
along with the parts of Polish that make it hard.
It is an artificial subset of Polish,
designed rather than described,
small enough that a machine can check it
cheaply, deterministically, and explainably.

The goal on this track is fun and experimentation.
That is the actual goal, not a modest way of stating a real one.
There is no application driving the design,
and any construction may be cut for being boring or annoying.

The scoreboard here is internal consistency:
a grammar that contradicts itself is broken
whether or not it matches usage.
That is a narrower criterion than the linter's,
and the difference is deliberate.
The linter is judged against a corpus of real Polish
because its whole claim is about how Poles actually write;
see [linter.md](linter.md#the-thing-that-makes-or-breaks-it-calibration).
A designed subset is judged against itself first,
and against Składnica only when it wants a coverage number.

## Decisions taken

**Olski should be as close to Polish as possible.**
Not a convenient toy subset,
but a language a Polish speaker would read as ordinary Polish.

**Closeness is traded against parser complexity, deliberately and measurably.**
Every construction admitted has a cost,
every cost buys some quantity of representable structure,
and the exchange rate is the thing worth studying.
See [the cost ladder](#the-cost-ladder) for what the currency actually is.

**Olski is a proper subset of Polish.**
Every olski sentence must be a well-formed Polish sentence.
No helper notation in the surface form,
no small deviations from Polish grammar for convenience.
Most controlled languages do not honour this;
see [similar-work.md](similar-work.md#the-word-subset-is-usually-a-lie).

**The lexicon is open, over Morfeusz 2.**
Closeness to Polish requires real inflection,
and a hand-built lexicon would make olski
close to a few hundred words of Polish rather than to Polish.
This settles what was the largest fork on this track.

Morfeusz specifically, and not Morfologik,
because this track needs **generation**:
a lemma plus a tag yielding a surface form.
The linter track needs only analysis,
and [reaches for Morfologik instead](roadmap.md#milestone-5-morphology-binding-and-the-rules-that-needed-it).
Two dictionaries for two jobs,
not one decision recorded twice.

## Two angles of the grammar track

Within this track there are two directions,
and they turned out to be one system.

**Parsing.** Polish text goes in, structure comes out.
The interesting artifact is the parser
and the question of how far a context-free grammar stretches
over Slavic morphosyntax.

**Skład.** Structure goes in, Polish text comes out.
Some source description, machine-checkable and human-authorable,
compiles into final text,
with the checks guaranteeing syntactic correctness.
Polish supplies the pun for free:
*skład* is typesetting,
*składnia* is syntax,
so a syntax-checking typesetter is one word.

The second direction is the more promising one,
because it dissolves the hardest problem in the first.
See [the round-trip invariant](#the-round-trip-invariant)
for why both survive anyway.

## Why a subset, really

The obvious justification is that natural language is not context-free,
so a CFG cannot parse Polish.
That is true in the strict sense,
but the textbook arguments are not the ones that matter here.

The real non-context-free arguments are narrow:
cross-serial dependencies in Swiss German (Shieber 1985),
unbounded reduplication in Bambara (Culy 1985).
Polish supplies neither.
The mid-1980s claims that English is not context-free
were largely dismantled by Pullum and Gazdar.

And a CFG augmented with finite-valued features
compiles down to a plain CFG.
Case, number, gender, and person are all finite,
so agreement is not a position in the Chomsky hierarchy.
It is a symbol-count problem.
A rule like `NP → Adj N` with agreement over
case (7) by number (2) by gender
(5 on the simplest analysis, more in most Polish tagsets)
is seventy instantiations at minimum:
fine for a machine, unreadable for a human,
which is why the grammar is authored with features
and expanded or unified by the toolchain.

So for a comfortable subset,
the reason to design one is **ambiguity management**, not decidability.

Committing to closeness to Polish changes that answer.
See [discontinuity](#the-cliff-discontinuity),
which is where the hierarchy stops being a technicality.

## What actually makes Polish hard

None of these are about tree shape.
Polish syntactic structure is not exotic.
The combinatorics live in the morphology-syntax interface.

**Case syncretism.**
`kobiety` is genitive singular, nominative plural, and accusative plural.
`okno` is nominative and accusative singular.
Every noun contributes several readings before parsing starts,
and the only way to narrow them
is agreement with something that may itself be syncretic.

**Free word order.**
`Jan widzi Marię`, `Marię widzi Jan`, and `Widzi Jan Marię`
are all well-formed and express the same predication.
A CFG expresses this only by enumerating permutations,
and *n* daughters means *n!* rules.

**Genitive of negation.**
`Widzę książkę` takes accusative.
`Nie widzę książki` takes genitive, obligatorily,
and the shift propagates down the object chain.

**Numeral phrases.**
`Dwie kobiety przyszły` is nominative with feminine plural agreement.
`Pięć kobiet przyszło` takes a genitive plural complement
and a neuter singular verb.
`Pięciu mężczyzn przyszło` does the same for masculine personal gender.
The numeral phrase's own case, number, and gender for agreement purposes
are a fiction distinct from anything inside it.

**Pro-drop and mobile clitics.**
`Przyszedłem` has no subject noun phrase.
`Gdzieś był?` is `Gdzie byłeś?`
with the person marker detached and clitized onto the interrogative.

## The cost ladder

"Parser complexity against represented structures"
suggests coverage can be bought incrementally.
Mostly it can.
But the price is not a smooth curve:
there is one step where it jumps by an exponent,
and knowing where that step sits
matters more than any other fact in the tradeoff.

| Tier | Buys | Cost |
| --- | --- | --- |
| 0 | CFG with finite features | Agreement, government, fixed-ish order. Earley, cubic |
| 1 | Dominance separated from precedence | Free order among sisters. Still cubic, grammar preprocessing |
| 2 | Slash and gap features | Unbounded movement, bounded discontinuity. Still context-free, symbol count multiplies |
| 3 | LCFRS, MCFG, or TAG | Genuine discontinuous constituents. Sixth power at fan-out 2 |
| 4 | Full unification, HPSG style | Everything. Undecidable in general |

Tiers 0 through 2 are the same asymptotic parser with a larger grammar.
Tier 3 is a different algorithm in a different complexity class.

### The cliff: discontinuity

Polish permits left-branch extraction
that splits a noun phrase around the rest of the clause:

```text
Jakie Jan czyta książki?
```

`jakie … książki` is one noun phrase
with the subject and verb sitting inside it.

This is not a curiosity invented for the argument.
Ross's (1967) Left Branch Condition,
which blocks exactly this in English,
fails across most of Slavic,
with Polish and Czech named as the standard exceptions:
Polish extracts wh-determiners, degree adverbs,
and attributive adjectives out of the noun phrase.
See Bošković, *On the locality of left branch extraction
and the structure of NP* (Studia Linguistica, 2005),
and for Polish specifically the empirical study in
*Extraction facts and the internal structure
of nominal constructions in Polish*
(Poznań Studies in Contemporary Linguistics, 2017).
Slavic also permits the split halves in more orders
than German does.

Discontinuous constituency is exactly what LCFRS and TAG exist for,
and it is the reason German treebank parsing
grew a whole discontinuous-parsing subfield.
Binary LCFRS with fan-out at most two
covers most cases found in real treebanks.

So the commitment to closeness to Polish
produces one concrete fork,
and it is not a difficulty gradient:
**may olski scramble across constituent boundaries?**
No keeps the project at tier 2
with a cubic parser and a large grammar.
Yes means writing an LCFRS parser.
Everything else in the subset is cheap next to this.

### The second currency: ambiguity

The ladder measures formal cost.
It misses the tax that closeness to Polish actually levies.

Free word order times case syncretism
means a six-word sentence can carry dozens of readings,
and the parser is *correct* to produce all of them.
That cost lands in forest size
and in whatever has to consume the forest,
not in the grammar's line count.

So parser complexity is two numbers:

- **Formal cost** — tier on the ladder,
  rule count after expansion,
  measured parse time
- **Ambiguity cost** — mean readings per sentence,
  forest node count

The second is the one that will make the project unpleasant if ignored,
because a grammar that admits everything
is easy to write and useless to use.

### Making the trade measurable

Kuhn's PENS scheme already defines
the axes this project wants to trade along.
Its Simplicity dimension is implementation cost,
measured in pages of description
sufficient for someone to write a correct parser;
its Expressiveness dimension is how much can be said.
Olski's cost-versus-coverage curve
is the S-versus-E plane of a scheme
that already has a hundred languages plotted on it.
See [similar-work.md](similar-work.md#pens-and-why-it-matters-here).

For the coverage side there is a ready benchmark:
Składnica holds thousands of real Polish sentences with gold trees.
For each tier of the ladder,
measure what fraction of a sample olski accepts
with a correct reading in the forest,
and plot coverage against tier.

That curve is the experiment.
How much real Polish per unit of formal power
is a question with a real answer
that nobody has computed for this grammar.
Its first point is computed:
tier 0 admits 1.5% of Składnica,
and [corpus.md](corpus.md) has the breakdown
and the reasons not to over-read the figure.
It also supplies a principled way to say no:
if scrambling buys three percent of sentences
for a jump from cubic to sixth-power parsing,
the decision makes itself.

## Angle one: parsing

Whatever parses olski must produce a **forest, not a tree**,
because genuine ambiguity is the normal case
and the useful operation is to enumerate readings and filter them.

GLR is the right shape of answer but probably the wrong specific choice:

- GLR's payoff is a precomputed table
  giving near-deterministic speed on mostly unambiguous input.
  An olski grammar will be conflict-dense throughout,
  so the graph-structured stack works hard on nearly every token
  and most of the speedup never arrives.
- Table construction over a permutation-expanded free-word-order grammar
  can blow up badly.
- Tomita's original algorithm breaks on nullable rules,
  so pro-drop would force RNGLR or BRNGLR (Scott and Johnstone).

**Earley is the boring recommendation and probably the right first move.**
It handles any CFG, including left recursion and nullable rules,
with no preprocessing;
it produces a shared packed parse forest natively;
its worst case is cubic but real grammars behave far better.
Decisively for a project whose grammar is still being designed:
the grammar can change without rebuilding an automaton.
Get the grammar right against Earley,
then treat GLR as an optimization if measurement ever demands one.

One correction to the above,
from measuring a working GLR system over real Polish:
the nullable-rules objection is historical.
Tomita's algorithm breaks on them,
maintained implementations do not.
The rest of the argument stands untouched —
that system's table is 146 states,
so it says nothing about what
a permutation-expanded grammar would cost to build.
It does supply a baseline worth flinching at:
20% of its input fails to parse
against a grammar hand-fitted to a register far narrower than olski.
See [glr-in-practice.md](glr-in-practice.md#measurements).

For free word order specifically,
the move that keeps a CFG viable
is to separate **immediate dominance from linear precedence**,
as GPSG did.
Dominance rules say what the daughters are,
separate precedence constraints say which orders are legal,
and a preprocessor deals with the factorial.
This also keeps the subset honest:
a permutation excluded from olski
is excluded by an explicit constraint rather than by omission.

## Angle two: skład

Generation inverts every difficulty in parsing.

Ambiguity is the parser's curse;
a generator never encounters it.
Agreement stops being a constraint to check
and becomes a value to compute.
Parsing `czarnego kota` means reconciling two syncretic feature bundles.
Generating it means calling `inflect(kot, acc.sg.m2)`
and getting one answer.

### Three architectures

**Correct by construction.**
The source is a typed abstract syntax tree,
with types encoding what agrees with what.
Ill-formed input fails to typecheck;
well-formed input compiles to text and cannot be wrong.
Strongest guarantee, worst ergonomics:
nobody wants to author prose as an AST.

**Write near-Polish and check it.**
The source looks like Polish and is parsed and validated.
Best ergonomics,
and it inherits every problem from the parsing angle,
plus the fact that chart parsers give famously bad error messages.
`parse failed at token 7` is not explainable.

**An unambiguous surface DSL.**
The source reads like Polish
but is designed to be parsed by something boring and deterministic,
because the notation is ours to control.
Lemmas plus explicit structural marks;
the compiler elaborates to an AST,
resolves agreement,
and linearizes.
Something in the spirit of:

```text
(zdanie
  podmiot: kot[m2]
  orzeczenie: widzieć[past]
  dopełnienie: mysz[pl])
→ Kot widział myszy.
```

The third option was the working preference.
The predictive-editor finding below
partly rehabilitates the second,
which is a better outcome than either.

### The predictive editor changes this

The controlled-language literature has a standard answer
to both the bad-diagnostics problem
and the habitability problem,
and it is not better error messages.
It is a **look-ahead editor**:
show the author, at each position,
which words and phrases the grammar permits next.
Then invalid text cannot be written,
so there is nothing to diagnose.

AceWiki does this for Attempto Controlled English.
For olski it would mean the checker's primary interface
is not a batch validator over a file
but an incremental one over a cursor position.
That is a substantially different program,
and it is the strongest argument found so far
for the second architecture over the third.

See [similar-work.md](similar-work.md#the-habitability-problem).

### Checks that are cheap, deterministic, and explainable

All finite-domain, all effectively linear time,
all able to say why they failed:

- Noun-phrase-internal agreement,
  adjective and determiner against noun,
  on case, number, and gender
- Subject-verb agreement on person and number,
  and on gender in the past tense and conditional
- Verbal government:
  `używać` demands genitive,
  so `używam komputera` and not `używam komputer`
- Prepositional government,
  each preposition licensing a fixed set of cases
- Genitive of negation,
  applied as a rewrite during linearization
  so that it is automatic rather than checked
- Aspect and tense legality:
  `będę zrobił` is unconstructible,
  and perfective present is future
- Gender resolution under coordination:
  `Jan i Maria przyszli`, never `przyszły`
- Clitic and `się` placement

Every failure should report two feature bundles and their provenance,
along the lines of
*`czarna` is nom.sg.f, `kota` is acc.sg.m2,
mismatch on case and gender, from lines 3 and 4*.
That is a diagnostic a human can act on,
and it is the thing a language model structurally cannot provide:
it cannot say which rule fired,
and it will not give the same answer twice.

### Morphology generation is the underestimated piece

Analysis maps a form to tags.
Generation maps a lemma plus tags to a form.
The compiler needs the second,
and Polish inflection carries enough irregularity,
stem alternation,
and paradigm classes
that hand-writing it is a multi-year detour.

Morfeusz 2 exposes generation over SGJP,
whose 2020 edition characterizes nearly 456,000 Polish lexemes,
and both are distributed under a liberal BSD licence.
That one dependency is the difference
between a weekend-scale core and a years-scale one,
which is why the open lexicon is a settled decision.

## The round-trip invariant

This is the load-bearing idea,
and it is what keeps both angles alive.

**Generate text from a tree,
parse the result,
and check that the original tree comes back.**

A failure is either a generator bug
or a genuine ambiguity in olski's surface form,
and *olski contains a construction that cannot be read back unambiguously*
is a language design bug worth discovering.

The idea is not original.
Reversible grammars have a literature going back to the late 1980s,
and Grammatical Framework makes reversibility structural.
See [similar-work.md](similar-work.md#the-other-tradition-engineered-wide-coverage-grammars).

### Closeness to Polish weakens it

Strict round-tripping requires unambiguous surface forms,
which is exactly what closeness to Polish gives up.
The invariant therefore needs restating,
and the honest version is asymmetric:

**Tree to text is a function.
Text to tree is a relation.**

The test becomes membership:
the original tree must appear *somewhere* in the forest.
Reading count becomes a tracked metric rather than a failure condition.
That still catches real generator bugs,
and it stops the invariant from silently forbidding
the naturalness the project is aiming for.

It follows that grammar and lexicon
should be one declarative source consumed by both directions,
rather than a parser and a generator that drift apart.
The rules should not be written twice.

## Known limits

**Grammaticality is not quality.**
A deeply nested stack of relative clauses
is exactly as well-formed as a clean sentence.
The checker will bless text no editor would accept.
That is fine,
as long as the claim stays where it belongs:
this checks syntactic correctness,
which is a real, useful, verifiable property,
and not the same thing as good Polish.

**Some correctness is usage, not structure.**
Collective numerals like `dwoje drzwi`,
the government of particular verbs,
which nouns take which prepositions:
none of that is derivable from rules.
It is lexicon.
The lexicon is therefore where the truth lives
and where the maintenance burden lands,
and it should be a first-class, reviewable, testable data file
rather than a hash map buried inside the parser.

**Rule-based language technology has a known labour profile.**
Rule-based machine translation declined
for coverage brittleness, per-language labour cost, and context-blindness.
Olski is not machine translation,
but it shares the labour profile,
and the only real mitigation is the one already chosen:
narrow the problem until hand-written rules suffice.

## The separable typographic layer

Independent of any grammar,
*skład* in the typesetting sense
has a pile of Polish rules
that are pure string manipulation and fully deterministic:

- A non-breaking space after single-letter words,
  so `w`, `z`, `i`, `a`, `o`, and `u` never end a line
- Polish quotation marks, „like this”
- The spacing of `nie`:
  separate from verbs, as in `nie ma`;
  joined to adjectives in the positive degree
  and to adjectival participles, as in `niedobry` and `niezrobiony`;
  separate from comparatives, as in `nie lepszy`
- Dash conventions and hyphenation points

This is testable, useful, and buildable
with no dependency on the grammar existing.

It is also the one part of this document
that survived the reframing unchanged,
because typographic rules are lint rules.
It ships as part of
[milestone 0](roadmap.md#milestone-0-rule-engine-and-the-typography-pack).

## Sources

- <https://sgjp.pl/o-slowniku/> — SGJP, about the dictionary
- <https://przewodnik.tmjp.pl/sgjp-2020-slownik-gramatyczny-jezyka-polskiego/> —
  the 2020 edition and its lexeme count
- <https://morfeusz.sgjp.pl/doc/about/> — Morfeusz, analysis and licensing
- <https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-9582.2005.00118.x> —
  Bošković on the locality of left branch extraction and the structure of NP
- <https://www.degruyterbrill.com/document/doi/10.1515/psicl-2017-0013/html?lang=en> —
  extraction facts and the internal structure of nominal constructions in Polish
- <https://www.ling.upenn.edu/~beatrice/syntax-textbook/lbe.html> —
  left branch extraction in Slavic, textbook summary
- <https://mdpi.com/1999-4893/9/3/58/htm> — LR parsing for LCFRS
