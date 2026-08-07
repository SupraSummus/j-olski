# Prior art

Things to read before writing code,
so that reimplementation is a choice rather than an accident.
Nothing here is a dependency yet.

Mostly resources for the optional
[grammar track](design-notes.md).
Tools for the linter track —
prose linters, LanguageTool, StyloMetrix —
are listed in [linter.md](linter.md#what-already-exists),
and the wider landscape in [similar-work.md](similar-work.md).

## Polish language resources

**Morfeusz 2** —
morphological analyzer *and generator* for Polish, built over SGJP.
Analysis returns a directed acyclic graph of segmentations with full tags;
generation maps a lemma plus a tag to a surface form.
The generator is the part the grammar track would lean on;
the linter needs only the analyzer,
and has a lighter option in Morfologik below.
<http://morfeusz.sgjp.pl/>

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
which makes it the likely choice for the linter track
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
and it is distributed under CC BY-SA 4.0 —
a friendlier licence than the parser
whose lexicons are generated from it.
It is what olski would need
in order to say which arguments a verb requires
rather than merely permits.
<http://walenty.ipipan.waw.pl/>

**Składnica** —
a constituency treebank of Polish, aligned with Świgra's output.
Useful as a source of test sentences
and as evidence of which constructions actually occur.
Now a dependency of the measurement, not of the package:
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
