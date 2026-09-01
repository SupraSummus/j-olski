# Prior art

Things to read before writing code,
so that reimplementation is a choice rather than an accident.

Mostly resources for the
[grammar track](design-notes.md).
Tools for the linter —
prose linters, LanguageTool, StyloMetrix —
are listed in [linter.md](linter.md#what-already-exists),
and the wider landscape in [similar-work.md](similar-work.md).

## Polish language resources

**Morfeusz 2** —
morphological analyzer *and generator* for Polish, built over SGJP.
Analysis returns a directed acyclic graph of segmentations with full tags;
generation maps a lemma plus a tag to a surface form.
The generator is the part the grammar track leans on,
and it is why Morfologik below is not the dictionary here.
<http://morfeusz.sgjp.pl/>

**Concraft** —
a morphosyntactic tagger for Polish, built over Morfeusz 2's output.
It reads the analyser's graph of interpretations,
marks one path through it as the disambiguated one,
and by default prints a marginal probability
beside every interpretation rather than beside the chosen ones alone.
Conditional random fields underneath, Haskell above, BSD-2 licensed,
and distributed as binaries for Linux, Windows and macOS
with a model of about 100 MB
trained on NKJP1M-SGJP and dated February 2022.
It reads and writes a tab-separated graph format,
and runs as a server with a Python client as well.

Choosing is what olski declines to do before the parser sees a sentence,
so this is not a component of the analysis:
`olski/morph.py` hands every reading forward on purpose,
and a path marked upstream would settle
[what olski reports as ambiguity](subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego)
in the analyser instead of in the grammar.
What it is a candidate for is the measurement,
where [neither column](corpus.md#what-morphological-ambiguity-costs)
comes from a tagger.
The marginals are the half a measurement can take
without the analysis losing a reading,
since they weight the interpretations rather than dropping any.
<https://zil.ipipan.waw.pl/Concraft>
<https://github.com/kawu/concraft-pl>

**SGJP**, *Słownik gramatyczny języka polskiego* —
the grammatical dictionary underneath Morfeusz.
The 2020 edition characterizes nearly 456,000 Polish lexemes
with their paradigm classes,
covering both attested and potential words,
and is distributed under a liberal BSD licence together with Morfeusz.
This is the inflectional truth that would otherwise take years to rebuild.
<https://sgjp.pl/o-slowniku/>

**Morfologik** —
the other freely licensed Polish morphological dictionary,
with roughly 3.5 million forms,
and the one LanguageTool uses for Polish.
Lighter than SGJP and oriented toward analysis rather than generation,
which is why the retired rule pack would have taken it
where no surface forms need to be produced.
See [linter.md](linter.md#what-already-exists).

**GFJP** and **Świgra** —
Świdziński's *Gramatyka formalna języka polskiego*,
and Woliński's parser,
which ships both a faithful implementation of GFJP
and a larger grammar of his own descended from it.
A working constituency parser for real Polish at full scale,
built on an extended Definite Clause Grammar formalism.
Which ground it occupies, what it leaves open,
and what its source is worth taking from,
is in [swigra.md](swigra.md).

**Walenty** —
a valency dictionary of Polish,
recording for each lemma the syntactic frames it admits.
The October 2017 version bundled with Świgra
characterizes 17,820 lemmata with 97,293 schemata,
and the April 2016 text release published on its own page has 17,224 verbal lemmata
and 64,022 schemata.
It is distributed under CC BY-SA 4.0 —
a friendlier licence than the parser
whose lexicons are generated from it.
Olski's valency lexicon is derived from it,
taking the handful of facts its own frame can carry and leaving the rest,
for the reasons
[warstwa-leksykalna.md](warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on) gives.
<http://walenty.ipipan.waw.pl/>

**Składnica** —
a constituency treebank of Polish, aligned with Świgra's output.
Useful as a source of test sentences
and as evidence of which constructions actually occur.
A dependency of the measurement, not of the package:
see [corpus.md](corpus.md) for how it is fetched and what it is allowed to prove.
<https://zil.ipipan.waw.pl/Składnica>

**POLFIE** —
an LFG grammar of Polish implemented in XLE.
A second serious formal treatment,
with a different formalism and different tradeoffs.

**NKJP**, the National Corpus of Polish —
the corpus most Polish tools are trained and evaluated against.
<http://nkjp.pl/>

**UD Polish treebanks**, PDB and LFG —
Universal Dependencies conversions.
Relevant if olski ever grows a dependency representation
alongside or instead of constituency.

## Formalisms and systems

**Grammatical Framework** (Ranta) —
the strongest match to the skład angle.
A typed abstract syntax describes what can be said;
per-language concrete syntaxes linearize those trees into surface strings,
handling inflection and agreement.
Grammars are reversible,
so the same source both linearizes and parses,
which is exactly the round-trip invariant made structural.
There is a Polish concrete syntax in the Resource Grammar Library.
Read this first.

What it gives and where it stops for Polish are different answers.
The abstract syntax is the part worth taking, and
[sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
owns what taking it means here.
The morphology is the part olski is better equipped for,
and the RGL's own status table says so:
Polish carries Paradigms, Lexicon, Syntax and API,
and carries neither `Dict` nor `WordNet` nor irregular verbs.
So the words are where an application grammar stops.
`LexiconPol.gf` is the RGL test vocabulary, a few hundred entries written by hand
(`bad_A = mkRegAdj "zły" "gorszy" "źle" "gorzej"`),
the public API in `ParadigmsPol.gf` offers `mkN`, `mkA2` and `mkAdv` and no verb
constructor at all,
and `mkN` picks an inflection pattern by matching the ending
against the numbered tables in `NounMorphoPol.gf`,
whose comments record the guesser as approximate.
A verb goes in through the internal `VerbMorphoPol.gf`,
which asks for two stems and two conjugation classes per lemma.
Against that, SGJP below Morfeusz answers for nearly 456,000 lexemes
without being asked to guess,
which is the one place where this repository starts ahead.

The library stops in a second place, and words are not it:
that place is the one `Wyróżnienie`, the category carrying topic and comment,
occupies here.
`PredVP` in `SentencePol.gf` emits the subject, then the verb, then the rest,
so the neutral order is fixed in the concrete syntax
and information structure has no category to come from;
`VerbPol.gf` records topicalization as a remark about where an adverbial lands.
This is a library written for Polish declining a choice Polish has,
so it says more than
[sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
does about libraries taken from languages whose word order is fixed.
Read at commit-time state of the `master` branch;
the files are in `src/polish/`.
<https://www.grammaticalframework.org/lib/doc/status.html>
<https://github.com/GrammaticalFramework/gf-rgl>

**Attempto Controlled English** —
a controlled natural language
whose sentences map deterministically into first-order logic.
The reference point for "restricted natural language with real semantics",
and a good source of decisions about what to cut and why.

**GPSG** immediate dominance and linear precedence —
the standard technique for expressing free word order
without enumerating permutations in the grammar.

**Earley (1970)** —
chart parsing for arbitrary context-free grammars,
producing a shared packed parse forest.
The recommended starting point for the parsing angle.

**Tomita (1985, 1987)**, GLR —
LR parsing generalized to ambiguous grammars
via a graph-structured stack.
See also Scott and Johnstone on RNGLR and BRNGLR,
which fix the original algorithm's failure on nullable rules.
For what GLR over Polish looks like when someone just uses it,
see [glr-in-practice.md](glr-in-practice.md).

**parglare** —
a Python GLR implementation with a grammar-object API,
so grammars can be generated rather than written in its DSL.
The subject of the field report above,
and the closest thing to an off-the-shelf parser
for the parsing angle's first experiments.
<https://github.com/igordejanovic/parglare>

## On natural language and the Chomsky hierarchy

**Shieber (1985)** —
cross-serial dependencies in Swiss German
as an argument that natural language is not context-free.

**Culy (1985)** —
unbounded reduplication in Bambara, to the same end.

**Pullum and Gazdar** —
the dismantling of the earlier arguments that English is not context-free.
Worth reading to calibrate how much the hierarchy question
actually matters in practice, which is: less than it seems.

**Kuroda (1964)** —
the context-sensitive languages are exactly
what a linear-bounded automaton accepts,
which is where the cost of parsing them comes from.

**Vijay-Shanker, Weir and Joshi (1987)** —
LCFRS, and what structural descriptions the various formalisms produce.
One of the three that
[tier 3 of the cost ladder](design-notes.md#the-cost-ladder) names.

**Seki, Matsumura, Fujii and Kasami (1991)** —
multiple context-free grammars,
which are the same class stated differently,
with the polynomial parsing bound worked out.
