# Similar work

Olski is not a new idea.
It is a new point in a space
that people have been exploring since roughly 1930,
and the field has enough measured results
that ignoring them would be a waste.

This file is the landscape.
[prior-art.md](prior-art.md) is the narrower list
of tools and resources olski might actually consume.

## The field has a name and a survey

The umbrella term is **controlled natural language**:
a subset of a natural language,
restricted in grammar and vocabulary,
to reduce or eliminate ambiguity.

The reference work is
Tobias Kuhn's *A Survey and Classification of Controlled Natural Languages*,
Computational Linguistics 40(1), 2014.
It catalogues **100 English-based controlled languages**
from 1930 to publication,
and it is the first thing to read.

Kuhn sorts them by goal into three types:

| Type | Goal | Count |
| --- | --- | --- |
| C | Comprehensibility for human readers | 45 |
| T | Translatability, usually machine-assisted | 22 |
| F | Formal representation and automated reasoning | 54 |

C and T overlap heavily.
Neither overlaps much with F.
Over 90 percent are written rather than spoken languages.

## PENS, and why it matters here

Kuhn classifies each language on four dimensions,
each with five levels:
**Precision**, **Expressiveness**, **Naturalness**, **Simplicity**.
English sits at P1E5N5S1,
propositional logic at P5E1N1S5,
and controlled languages fill the space between.

The definition of the Simplicity dimension is the interesting part.
It is the number of pages
needed to describe the language exactly and comprehensively,
such that a skilled grammar engineer
could implement a correct and complete parser from the description.
Not learnability, not Chomsky-hierarchy complexity:
implementation cost.

That means the tradeoff this project intends to make,
parser complexity against the number of represented structures,
is the S-versus-E plane of an existing, populated, measured scheme.
Olski can be given a coordinate
on the same chart as a hundred other attempts.
It should be.

### Where olski aims

This positioning describes the
[grammar track](design-notes.md),
which is the only part of the project
that would be a controlled natural language at all.
The linter is a checker, not a language,
and has no PENS class.
The S-versus-E reading below still applies to it,
because implementation cost against coverage
is the same trade under a different name.

Averaged by type, the field splits into two clusters:

| Cluster | P | E | N | S |
| --- | --- | --- | --- | --- |
| C and T | 2.0 | 4.3 to 4.8 | 4.7 to 5.0 | 1.1 to 1.2 |
| F | 4.4 | 2.3 | 3.8 | 3.2 |

The C and T languages are mostly industrial and domain-specific:
natural and expressive,
imprecise,
and impossible to describe compactly.
The F languages are mostly academic:
precise and compactly describable,
at a real cost in naturalness and expressiveness.

Only 25 of the 625 possible PENS classes are occupied at all.

Olski wants high naturalness, because it should be close to Polish,
together with high precision, because it should be deterministically checkable.
That combination is the sparse corner,
and the survey's numbers explain the sparsity:
it is paid for in Simplicity,
which is to say in implementation cost.
This is the trade the project has already chosen to make.
Choosing it knowingly, with a coordinate system to report position in,
is better than stumbling into it.

## Does it work

Kuhn's evaluation survey is the answer to
what people actually say about controlled languages,
and it is more positive than the reputation of rule-based language technology
would suggest.

For comprehensibility:
AECMA Simplified English significantly improved text comprehension,
with the largest effect on complex texts and non-native readers
(Shubert et al. 1995; Chervak, Drury, and Ouellette 1996).
Other studies pointed the same way without reaching significance
(Stewart 1998).

For translation:
MCE was reported to give a five-to-one gain in translation time
(Ruffino 1982).
PACE made post-editing three to four times faster
(Pym 1990).
CLCM reduced post-editing time by about 20 percent
(Temnikova).

For formal representation:
CLOnE's interface beat a conventional ontology editor on usability
(Funk et al. 2007),
and ACE was easier and faster to understand
than a standard ontology notation
(Kuhn 2013).
Positive usability results are also reported
for GINO, CLEF, CPL, PERMIS, and Rabbit.
Rabbit's comprehensibility results were mixed
(Hart, Johnson, and Dolbear 2008).

## Two findings that should shape olski

### The habitability problem

A language is *habitable*
if its users can express themselves
without straying outside its boundaries.
The standing critique of controlled languages
is that for any real subject matter
the set of appropriate sentences is impossibly large,
so users cannot perceive where the fence is
and discover it only by being rejected.

This is precisely the failure mode
that "as close to Polish as possible" invites.
The closer olski gets to Polish,
the harder it becomes for an author to feel the boundary,
and the more often a perfectly good Polish sentence
gets refused for reasons that feel arbitrary.

The field's answer is the **predictive editor**.
AceWiki shows, step by step,
which words and phrases are syntactically possible
at the current position in the sentence.
That inverts the problem:
rather than writing text and receiving errors,
the author is never able to write something invalid.

It also dissolves a worry recorded in
[design-notes.md](design-notes.md#three-architectures),
that chart parsers give unusable diagnostics.
With look-ahead there are no diagnostics to give,
because there are no errors.
For a project whose whole claim
is cheap, deterministic, explainable checking,
this is the most important architectural idea in the literature.

### The word "subset" is usually a lie

Kuhn notes that the term is misleading:
most controlled languages are not proper subsets of their base language.
They add notation,
or deviate from natural grammar and semantics
in small ways.

Olski's framing is that it is genuinely a subset of Polish.
That is a stronger commitment than most of the field makes,
and it forbids helper notation in the surface form.
Every olski sentence must be a Polish sentence.
Worth holding deliberately rather than discovering later.

## Named languages worth knowing

**Human-oriented.**
ASD-STE100 Simplified Technical English,
descended from AECMA Simplified English,
built in the 1980s by the European aerospace industry
for aircraft maintenance manuals readable by non-native speakers,
since spread to defence, rail, automotive, oil and gas, and medical devices.
Ogden's Basic English.
Voice of America's Special English.
Caterpillar Fundamental English and Caterpillar Technical English.
Plain Language.
The spoken outliers,
SEASPEAK and ICAO phraseology,
almost all of governmental origin.

**Machine-oriented.**
Attempto Controlled English,
a subset of English translated unambiguously into first-order logic
by way of Discourse Representation Structures,
with a parser, a reasoner, a Protégé plug-in, an OWL verbaliser,
and the AceWiki predictive editor.
PENG.
Common Logic Controlled English.
For ontology authoring:
CLOnE, and Rabbit as its more expressive successor from Ordnance Survey,
and Sydney OWL Syntax.
For business rules:
SBVR Structured English, and RuleCNL.

## The other tradition: engineered wide-coverage grammars

Separate from controlled languages,
there is a large body of hand-built grammars
that aim to describe a real language rather than restrict it.
This is the honest comparison
for anything claiming to be close to Polish.

**Grammatical Framework**
provides resources for more than 40 languages
over a shared abstract syntax,
with reversible grammars,
and has explicitly scaled itself
from controlled languages toward robust pipelines.

**DELPH-IN**, the HPSG tradition:
the English Resource Grammar
parses roughly 94 percent of well-edited English
while refusing sentences impossible in English.
The Grammar Matrix is a starter kit
that produces a new language's grammar
from a typological questionnaire,
which is a striking answer to
"how do you start a precision grammar for language X".

**LFG, ParGram, and XLE**,
and for Polish specifically POLFIE,
whose c-structure derives from GFJP2,
the same grammar behind the Świgra parser,
which in turn annotated the Składnica treebank.

**Rule-based machine translation**,
Apertium and its ancestors.
Its decline is instructive:
coverage brittleness,
heavy labour cost per language pair,
and blindness to context.
It survives where the language pair is closely related.
Olski is not machine translation,
but it shares the labour profile,
and the mitigation is the same:
narrow the problem until hand-written rules are enough.

**Reversible grammar** is its own literature,
which matters because
[the round-trip invariant](design-notes.md#the-round-trip-invariant)
is not an original idea.
See Strzalkowski's *Reversible logic grammars
for natural language parsing and generation* (1990),
the 1991 ACL workshop he chaired,
and Dymetman's *Inherently Reversible Grammars*.

## Outliers

**Lojban** is the extreme of designing for parseability:
a constructed language with a formal machine grammar in YACC,
claimed to be fully syntactically unambiguous.
Instructively, it is *not* LALR(1) —
some words' grammatical function
depends on tokens that follow them,
so parsing happens in two stages,
and a PEG grammar has been proposed as the replacement baseline.
A language designed from scratch for unambiguous parsing
still could not stay inside the easy formalism.

## On the Polish side

**Plain Polish** exists as a movement:
the Pracownia Prostej Polszczyzny at the University of Wrocław,
and **Jasnopis**, from SWPS University and the Polish Academy of Sciences,
which scores text difficulty on a scale from 1 to 7,
flags hard fragments,
and since 2023 simplifies automatically.

This is readability work, not formal grammar.
It shares olski's instinct
that a restricted Polish is worth having,
and none of its machinery.

**The gap is real.**
Kuhn's hundred languages are all English-based.
Polish-language sources on controlled languages
state plainly that research on the topic is rare for Polish.
A controlled Polish
with a formal grammar,
high naturalness,
and deterministic checking
is close to unoccupied ground.

That is not evidence the idea is good.
It is evidence that nobody will hand us the answer.

## Sources

- <https://aclanthology.org/J14-1005/> — Kuhn, *A Survey and Classification of Controlled Natural Languages*
- <https://arxiv.org/abs/1507.01701> — the same survey on arXiv
- <https://en.wikipedia.org/wiki/Controlled_natural_language>
- <https://en.wikipedia.org/wiki/Simplified_Technical_English>
- <https://www.asd-ste100.org/> — ASD-STE100 specification
- <https://attempto.ifi.uzh.ch/site/pubs/papers/reasoningweb2008_fuchs.pdf> — ACE for knowledge representation
- <https://ceur-ws.org/Vol-448/paper14.pdf> — Rabbit to OWL
- <https://arxiv.org/pdf/1406.2903> — a brief state of the art for ontology authoring
- <https://arxiv.org/abs/1406.2096> — RuleCNL for business rules
- <https://direct.mit.edu/coli/article/46/2/425/93370/Abstract-Syntax-as-Interlingua-Scaling-Up-the> — GF from controlled languages to robust pipelines
- <https://journals.colorado.edu/index.php/lilt/article/view/1205> — the GF Resource Grammar Library
- <https://matrix.ling.washington.edu/> — the LinGO Grammar Matrix
- <https://delph-in.github.io/docs/home/Home/> — DELPH-IN
- <https://clarin-pl.eu/dspace/handle/11321/588> — Świgra, a parser of Polish
- <https://clarin-pl.eu/dspace/handle/11321/253> — POLFIE
- <https://aclanthology.org/W91-0100.pdf> — Reversible Grammar in Natural Language Processing, 1991 workshop
- <https://link.springer.com/article/10.1007/s10590-021-09260-6> — recent advances in Apertium
- <https://lojban.github.io/cll/21/1/> — Lojban formal grammars
- <https://mw.lojban.org/papri/PEG> — the Lojban PEG proposal
- <https://jasnopis.pl/prosty-jezyk/> — Jasnopis and plain Polish
- <https://mdpi.com/1999-4893/9/3/58/htm> — LR parsing for LCFRS
