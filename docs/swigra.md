# Świgra: the ground it occupies, and what it leaves open

Świgra is a constituency parser of the whole of Polish,
written by Marcin Woliński over more than two decades,
and it is the closest existing thing to olski's grammar track.
Reading its source is how to find out which ground is taken.

The useful output of that reading is the ground that is not taken,
since that is where olski's grammar track lives.
The second output is a set of mechanisms worth taking,
since a grammar of Polish that has run for twenty years
has already met the problems olski is walking into.

## What was read, and what was not

`swigra_current.zip`, fetched from the project page at
<https://zil.ipipan.waw.pl/Świgra>,
whose files carry dates up to June 2019.
The CLARIN-PL handle listed in
[similar-work.md](similar-work.md#sources) answers 404;
the wiki attachment is the live copy.

The package is roughly 66,000 lines of SWI-Prolog under GPL v3.
Two files are grammars:
`gfjp.dcg` implements Świdziński's formal grammar of Polish, the GFJP,
and `gfjp2.dcg` is a larger grammar of Woliński's own descended from it,
which the parser runs by default.
The runtime around them is called Birnam and is about 1,300 lines.
A grammar is not interpreted:
`birnam_dcg2pl` compiles the `.dcg` file into Prolog clauses,
which are then saved as a binary.
The verb and noun lexicons are generated files
carrying a header that says so,
built from the Walenty valency dictionary.
The maximum-entropy tree disambiguator ships as a separate archive.

Everything below comes from reading that source.
It was not run.
Świgra needs SWI-Prolog and a Morfeusz binding compiled against it,
and neither was installed where this reading happened,
so nothing here is a measurement —
the claims are about what the code says.

## What Świgra occupies

Świgra takes a Polish sentence and returns every constituency tree it has,
and the pipeline around it ends in a maximum-entropy component,
trained on the Składnica treebank,
that picks one of those trees.
Analysis of the whole language and resolution of the ambiguity it finds:
that is the territory, and it is held.

Three properties of it decide what is left over.

**It describes Polish rather than choosing a Polish.**
An analyser that refused a genuinely ambiguous Polish sentence
would be broken, because the sentence is Polish.
Everything Świgra does follows from having no licence to exclude.

**It resolves.**
The forest exists to be collapsed,
and the disambiguator is what collapses it.
Forests can be looked at —
there is a web demo, and TeX and PDF renderings of trees —
but nothing in the package treats the *number* of readings
as something to report about the sentence.

**It runs in one direction.**
Birnam is a bottom-up chart parser pulling input from an inflection graph.
Nothing in the package generates.

## What it leaves open

Each of these is unoccupied ground rather than a complaint,
and together they are the grammar track's reason to exist.

**Ambiguity reported to the author instead of resolved for them.**
[roadmap.md](roadmap.md#co-jest-budowane) owns that purpose,
and Świgra is where the survey found it empty:
it picks the likelier reading where olski would hand both back.
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
records the same move being made by accident
in a system with no linguistic ambitions at all,
which is evidence that it is natural rather than clever.

**A language chosen rather than described.**
Olski picks what it admits and can therefore pick its landmarks:
constructions that keep ambiguity local instead of letting it compound.
[glr-in-practice.md](glr-in-practice.md#measurements) names that lever
at the end of a grammar whose register handed it the landmarks for free,
and olski has not spent it.
Świgra has no access to it at any price.

**Generation, and the round trip.**
[design-notes.md](design-notes.md#the-round-trip-invariant)
wants one declarative source feeding both a parser and a generator,
so that a text and its structure can be checked against each other.
No part of Świgra's runtime can be that source.

**Small enough to state.**
Świgra is 66,000 lines and a book.
Kuhn's survey of controlled languages measures simplicity
in pages of description
sufficient for someone to write a correct parser,
and a subset that fits in a document
is a different artifact from a grammar that does not,
whichever admits more Polish.
See [similar-work.md](similar-work.md#pens-and-why-it-matters-here).

And the largest one, which is not about grammars at all.
[roadmap.md](roadmap.md#celem-toru-jest-to-readme)
sets the size of grammar olski needs by a document
rather than by a coverage figure:
the track exits when this repository's README derives,
one reading per sentence.
Świgra admits more Polish than that and will go on doing so,
which decides nothing here,
because the two are not measured on the same axis
and covering more is not what would make olski done.

## Why wrapping it does not get there

Worth recording so that nobody re-proposes it:
the uniqueness test could in principle run on Świgra's forest,
and four things stop it.

It counts derivations where olski counts readings.
`counttrees` in `birnam_cleanforest.pl`
multiplies subtree counts through the packed forest,
while [subset.md](subset.md#co-się-liczy-jako-jedno-czytanie)
quotients over lemmas, feature values and parts of speech
so that only structure counts,
and writing that quotient against somebody else's tree shapes
is most of the work with none of the design freedom.
Deriving everything is the wrong primitive for a subset,
so the boundary would have to be reimposed by a filter over trees,
which is a grammar written twice.
The integration is a subprocess and an XML parse:
SWI-Prolog, a binary saved by `qsave_program`,
forests serialized against `forest.xsd`,
and a Morfeusz glue library compiled against SWI-Prolog 7.4 and 7.6.
And Świgra is GPL v3,
so embedding it is a licensing decision
rather than a detail to discover afterwards.

None of which is a criticism.
If the goal were parsing arbitrary Polish this project should not exist,
and Świgra is not the competition but the measuring stick:
Składnica's trees are drawn from its output,
which is why a coverage figure against Składnica
means what [corpus.md](corpus.md#what-this-number-is-not) says and no more.

## What the code does that olski should take

### Free word order without factorial rules

`birnam_sequences.pl` defines a metanonterminal `sequence_of`
that repeatedly selects one daughter out of a bag
until the span is consumed,
so order among sisters is free by construction.
What makes it usable rather than merely permissive
is *iterated conditions*, written `^[Pred, In, Item, Out]`,
which thread an accumulator through the daughters
in whatever order they arrived:

```prolog
zdanie(...) --> s(ze1),
    ff(..., Wym, ...),
    sequence_of([ fw(W2,H2,...)  ^[oblwym_iter, Wym, W2/H2, ResztaWym],
                  fl(...)        ^[najwyżej3, 0, _, _],
                  posiłk(...) ]
                ^[obldest_iter,    Dest1, Dest2, Dest]
                ^[sprawdz_pk_iter, Pk1,   Pk2,   Pk]),
    { wymagania_zamknij(ResztaWym) }.
```

Valency saturation, comma agreement, interrogative propagation,
a ceiling of three loose phrases,
and the rule that at most one auxiliary may appear
and not directly before the finite verb
all ride on that one mechanism.
This is the tier-1 row of
[the cost ladder](design-notes.md#the-cost-ladder) —
dominance separated from precedence —
implemented in about two hundred lines,
and it is the answer to how that row is paid for in practice.
The cost it does not hide:
selecting from a bag is a backtracking choice point per daughter,
so the freedom is bought with search rather than with rules.

### Valency as a resource that gets consumed

A verb carries a `wym` term
whose last argument is a list of *alternative* schemata.
Realizing an argument keeps only the schemata
holding a position that admits it, and deletes that position;
`wyjmij` in `gfjp2_wymagania.pl` is the four-line core of it.
Coordination is `koord([Frames…])`,
and an argument must be removable from every conjunct.
At the end `wymagania_zamknij` checks that something survived.

So which frame a verb is using is never chosen in advance.
It falls out of the parse as a narrowing set,
which is both cheaper and more honest
than deciding the frame first and backtracking on it.
Valency is on the list of things
[the subset does not cover](subset.md#what-it-does-not-cover-yet),
and this is the shape to reach for when it does.

### The comma as a grammatical attribute

Every nonterminal in `gfjp2.dcg` carries `Pk`,
its *przecinkowość* — what it demands of the comma slot on each side —
combined by `oblpk` against a compatibility relation `zgodne_pk`.
Empty commas are inserted into the inflection graph beforehand,
so a comma slot exists at every position whether or not one was written.
The value lattice is the interesting part:
a comma, a forbidden comma, either,
a forced comma that may not migrate inward,
a forced absence,
a *permissible* omission,
and four more for the edges of an utterance.

This is what a comma rule looks like
when it is derived from the parse instead of matched in the text,
and it comes with a design note olski should copy outright.
The clause admitting a missing comma before a coordinator
sits under a comment saying that blocking it
backs out of a permissiveness the author calls ruinous.
One line, two severities.
A rule engine wants exactly that knob,
and here it is expressed in the grammar rather than beside it.

### One gap instead of a different complexity class

Woliński's grammar handles discontinuity with a nonterminal spelled `ξ`.
A phrase with a hole carries its own requirement,
the sequence admits **at most one** such phrase —
`wykryjξ` is a single clause, which is the whole enforcement —
and the borrowed requirement is discharged later
against the phrase that owns it.
Two limits are written into the rule itself:
subjects do not extract, and a phrase with a hole does not extract.

That is a slash feature threaded through a free-order sequence,
which puts it at tier 2 rather than tier 3.
Woliński's own list of what the grammar covers
includes common discontinuous structures,
and this is the machinery that covers them.
[The big fork](open-questions.md#the-big-fork-may-olski-scramble)
asks whether olski must leave the context-free tier to scramble,
and here is a working parser of Polish that did not have to,
having bounded the gap to one and excluded subjects from it.
Evidence, not proof: what it does not say
is what fraction of real Polish that discipline gives up.

### A full-scale grammar pays the ambiguity tax too

[The second currency](design-notes.md#the-second-currency-ambiguity)
argues that ambiguity, not formal power,
is the cost that will make the project unpleasant if ignored.
`gfjp2.dcg` contains the same argument in the form of concessions.
Genitive is blocked in loose adjunct noun phrases
under a comment naming the explosion that forced it.
The attribute tracking interrogative and relative marking
is pinned to its neutral value in one nominal rule,
because the alternative produced duplicate analyses.

Woliński had no coverage budget to respect and conceded anyway.
That is evidence the tax is real
rather than an artefact of writing a small grammar,
and it comes from a grammar of Polish
large enough for the concession to be visible.

### The grammar carries its own examples

`gfjp2.dcg` holds 437 lines beginning `%%%%`
and 53 beginning `%%%*`:
sentences that must parse and sentences that must not,
sitting directly beneath the rules that license them.

```text
%%%% Gotować mieszaninę dwie godziny.
%%%* Gotować Jan mieszaninę dwie godziny.
```

That is the convention this repository asks of tests,
applied to a grammar,
and the reason it survives decades of editing
is that the example is physically attached to the rule it exercises.
A grammar rule in olski could carry the same thing,
extracted by a test rather than read by a human.

### Failure is diagnosable, and coverage is measured against gold

An unknown word raises a distinct exception
rather than joining the general failure to derive,
so "Morfeusz did not know this form" and "the grammar did not license this"
stay separate answers.
Each analysis emits its tree count, edge count, inferences and CPU time.

The evaluation script goes further.
For each treebank sentence it walks the packed forest
counting the trees *consistent with the corpus disambiguation*.
Coverage there is not whether the parser produced something,
but whether the gold reading is in the forest
and how deeply it is buried among alternatives.

That is a better question than the one olski asks of Składnica,
and olski cannot ask it with the parser it has.
`olski/parse.py` enumerates distinct readings and builds no forest to walk,
so this measurement waits on the chart parser that
[design-notes.md](design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)
argues for and orders,
where what asks for the forest first is the verdict rather than any measurement.
This is the reason for it that comes from the measurement rather than the report.

## Sources

- <https://zil.ipipan.waw.pl/Świgra> — the parser, its licence terms and its packages
- <http://nlp.ipipan.waw.pl/Bib/woli:04.pdf> — Woliński, *Komputerowa weryfikacja gramatyki Świdzińskiego*, 2004, which documents Świgra 1 and Birnam
- <https://www.wuw.pl/data/include/cms/Automatyczna_analiza_skladnikowa_Wolinski_Marcin_2019.pdf> — Woliński, *Automatyczna analiza składnikowa języka polskiego*, 2019, which documents the second grammar
- <http://walenty.ipipan.waw.pl/> — Walenty, the valency dictionary the lexicons are generated from
