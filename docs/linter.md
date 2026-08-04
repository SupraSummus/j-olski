# Olski as a linter

The motivation, stated plainly:
a linter for Polish prose,
used to check texts produced by language models.
Not for syntactic errors —
models rarely make those —
but for the patterns they habitually fall into.

A linter helps write good code.
This should help write good Polish.

## The target register: technical documentation

A style linter is close to useless for accomplished prose,
where every rule it enforces is one a good writer breaks on purpose.
For technical documentation it is exactly the right instrument.

This is not a compromise, it is the field's own answer.
Every controlled language with measured results behind it
was built for technical documentation:
Simplified Technical English for aircraft maintenance manuals,
Caterpillar's languages for heavy machinery,
the whole type C and type T cluster in Kuhn's survey.
Nobody has ever usefully controlled literary prose,
and the reason is not that nobody tried.

There is a sharper version of this point in
[glr-in-practice.md](glr-in-practice.md),
which observes that the archival shorthand it parses
is *already* a controlled natural language,
controlled by editorial convention rather than by design,
and that this is the only reason
a few hundred lines of grammar get anywhere.
Technical documentation is the same kind of object:
a register that professional convention has already narrowed,
which is why rules over it can be both few and defensible.

Fixing the target register resolves the hardest calibration problem.
In technical documentation,
nominalization, impersonal constructions, hedging and uniformity
are defects by professional consensus.
In fiction the same features are instruments.
Scoping olski to expository and technical Polish
means its rules can be defended
instead of endlessly qualified.

See [the fiction question](#and-fiction) for the other half of this.

## This is the same subset, approached from behind

A controlled natural language is a whitelist.
It says: only these constructions exist,
everything else is outside the language.

A linter is a blacklist.
It says: write whatever you like,
but these patterns get flagged.

The set of texts that pass every rule
is still a subset of Polish.
It is simply defined by exclusion rather than by construction,
and that turns out to be enormously cheaper.

### It dissolves the habitability problem

The single largest risk in the controlled-language framing
was habitability:
the closer olski got to Polish,
the less an author could feel where the boundary lay,
and the more often good Polish would be rejected
for reasons that felt arbitrary.
See [similar-work.md](similar-work.md#the-habitability-problem).

A linter has no boundary to feel.
There is no rejection, only advice,
and the author remains free to ignore it.
The failure mode drops from
"the tool refuses my sentence"
to "the tool nags about my sentence",
which is a category of failure every programmer already tolerates daily.

### It also removes two hard requirements

No generator is needed,
so the round-trip invariant is no longer load-bearing.
No unambiguous surface form is needed,
so the tension between closeness to Polish and round-tripping disappears.

What remains of the grammar work
is a question of *depth*:
how much analysis does each rule need in order to fire correctly.

## How deep does each rule have to see

This replaces [the cost ladder](design-notes.md#the-cost-ladder)
as the project's central tradeoff,
and it is far friendlier,
because most useful rules sit at the bottom.

| Tier | Machinery | Rules it enables |
| --- | --- | --- |
| A | Tokenizer, sentence splitter, regular expressions | Typography, literal stock phrases, connector density, sentence-length variance, list and bullet density |
| A+ | Suffix regexes over word endings | A surprising amount of tier B, without a tagger. See below |
| B | Morphological analysis and lemmatization | Lexical rules over inflected forms, nominalization density, part-of-speech ratios, impersonal and passive constructions, adjective stacking |
| C | Chunking or dependency parsing | Subject-predicate distance, clause depth, coordination length, constructions rather than strings |
| D | Full constituency parse | Very few rules genuinely need this |

### Suffixes buy more than expected

[glr-in-practice.md](glr-in-practice.md) records a working Polish system
that classifies occupations
with a single alternation over agent-noun endings —
`-strz`, `-nik`, `-arz`, `-acz`, `-iec`, `-ica`, `-nier`, `-iusz`, `-ant` —
with no dictionary and no lemmatizer.
Crude, and it works.

That matters here more than it did there.
The central plain-Polish rule,
nominalization density over `-anie`, `-enie` and `-cie`,
is a suffix pattern by definition,
so it needs no morphology at all.
The same goes for impersonal `-no` and `-to` forms.
Several of the rules filed under tier B below
are really tier A with a better regex,
which moves the morphology dependency later
and makes the first useful rule pack cheaper than it looked.

Lemma-keyed lexical rules still need real morphology.
Density metrics over endings do not.

The honest consequence:
tiers A and B probably carry most of the value,
and the Earley parser, the parse forests,
the LCFRS question and the Składnica coverage curve
all leave the critical path.
They become an optional deeper track,
not the project.

## The thing that makes or breaks it: calibration

**A rule without a measured false-positive rate on good human Polish
is a stylistic prejudice, not a linter rule.**

Good Polish writers use em dashes.
They use three-item lists.
They nominalize when nominalizing is right.
A rule set assembled from intuition
will punish exactly the human writing it claims to protect,
and there is no way to know which rules are like that
without measuring.

So the project needs a paired corpus:

- **Human Polish**, ideally across registers.
  NKJP, Wolne Lektury for literary prose,
  edited journalism, and some deliberately good expository writing.
- **Generated Polish**, from several models,
  on comparable topics and in comparable registers.
  This half is cheap, on the condition that it is generated and then left alone.
  Text that has been edited against style detectors
  reports a floor rather than a rate,
  which [generated-polish.md](generated-polish.md#what-this-corpus-cannot-support)
  measures on a corpus that had been.

Then every rule carries two numbers:
how often it fires on generated text,
and how often it fires on good human text.
A rule that fires equally on both is worthless
regardless of how strongly anyone feels about it.

This is the replacement for the coverage curve,
and it is a better experiment:
cheaper to run, and it produces a rule set
that has earned each of its rules.

### Abstention is allowed

A rule that cannot tell
whether it is looking at a defect or a legitimate choice
should decline to fire rather than guess.

This is the same instinct as the extractor in
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure),
which answers only when its parse is unambiguous
and otherwise leaves the field empty for a human.
Ambiguity there is not resolved but used as a confidence measure.

The measured version of that system sharpens the argument
and separates two things the first reading of it ran together.

Deliberate abstention is nearly free there.
It fires on 2 rows in 1000.
Silence from *lack of coverage* is what costs:
202 rows in 1000 fail to parse at all.
Both return nothing to the caller,
but only the first is the precision instinct at work;
the second is a grammar that does not reach its input,
and its linter analogue is not abstention but
*no rule matched*, which is the normal case and not a decision.

What the extracted 47.3% shows is that
when the thing does commit, it is right.
That is the property worth copying,
and the rows it stayed quiet on
were already queued for human review,
so quiet cost nothing.

One of those two abstentions is a warning.
The readings it declined to choose between
were byte-identical,
produced twice by an optional-whitespace rule,
so the check discarded a line it had understood perfectly.
A linter that abstains
must compare *distinct* outcomes rather than counting attempts,
or it will fall silent on exactly the cases it got right.

For a linter the equivalent is a bias toward precision over recall.
A missed defect costs nothing.
A false accusation against good Polish
costs the user's trust in every other rule,
and trust is the only thing that makes a linter get run twice.

## Anchor to Polish norms, not to model fingerprints

There are two ways to justify a rule.

*This is what models do* dates immediately.
Wikipedia's editors observe that
"stands as a testament" places a text in 2023 or 2024 specifically.
Tells decay as models change,
so a rule set built on fingerprints
needs continuous maintenance
and is trivially obsoleted by the next release.

*This is bad Polish style* does not date.
And it happens to catch the same texts,
because what makes model prose recognizable in Polish
is largely that it is nominal, impersonal, hedged, and uniform —
which Polish style authorities were already against.

**Prosta polszczyzna supplies a citable norm.**
The Pracownia Prostej Polszczyzny at the University of Wrocław
has spent over a decade codifying it,
and its rules are directly mechanizable:

- **Rzeczowniki zombie** — nouns in `-anie`, `-enie`, `-cie`;
  check whether a verb would do instead
- Phrases that invite them —
  `w celu`, `w razie`, `z powodu`, `na skutek`,
  especially at the start of a paragraph
- Keep subject and predicate close together
  and near the start of the sentence;
  avoid interpolations
- Write personally:
  avoid `-no` and `-to` forms, avoid `się` passives,
  avoid `można`, `trzeba`, `należy`, `warto`

Every one of those is also a model tell.
That overlap is the project's best piece of luck:
the rules can be defended on Polish stylistic grounds
and still do the job they were wanted for.

## Candidate rule inventory

Grouped by the tier they need.
Items marked *cited* come from a source in
[similar-work.md](similar-work.md) or below;
the rest are hypotheses to be calibrated, not conclusions.

### Typography, tier A

- Em dash frequency, and em dashes used where Polish would not use them *cited*
- Straight quotes where Polish takes „ and ”
- Single-letter words left at end of line
- Markdown emphasis left unreviewed in running prose *cited*
- Excess spacing and other generation artifacts *cited*

### Lexical, tier B

- Anglicisms and calques:
  `dedykowany`, `adresować` a problem, `w oparciu o`,
  `dostarczać wartość`, `holistyczny`, `synergia`
- Booster inflation:
  `kluczowy`, `istotny`, `przełomowy`, `fundamentalny`, `niezwykle`, `znacząco`
- Stock openers and closers:
  `W dzisiejszym szybko zmieniającym się świecie`,
  `Warto zauważyć, że`, `Podsumowując`
- Connector density:
  `Ponadto`, `Co więcej`, `Dodatkowo`, `Niemniej jednak`
- Repetitive evaluative vocabulary *cited*

### Morphosyntactic, tier B

- Nominalization density: `-anie`, `-enie`, `-cie` per hundred words *cited*
- Impersonal `-no` and `-to` forms, and `się` passives *cited*
- Hedges `można`, `trzeba`, `należy`, `warto` *cited*
- Adjective stacking before a noun
- Participle chains: `będąc`, `mając`
- Comparative adjective frequency *cited*

### Structural and statistical, tier A with sentence splitting

- Sentence-length uniformity, measured as low variance *cited*
- Paragraph-length uniformity
- Three-item list frequency *cited*
- Bullet density inside prose
- `nie tylko X, ale także Y` and other parallel-negation frames.
  The frame's commonest Polish form is punctuated rather than lexical,
  so this entry and the em dash above are one construction:
  see [generated-polish.md](generated-polish.md#what-the-em-dashes-are-doing)
- Lemma type-token ratio *cited*
- Fact density: dates, numerals, proper nouns; low in generated text *cited*
- Absence of inversion and other emphatic reorderings *cited*

### Discourse, tier C or D

- Promotional inflation:
  `stanowi świadectwo`, `odgrywa kluczową rolę` *cited*
- Vague attribution:
  `badania pokazują`, `eksperci twierdzą` *cited*
- Subject-predicate distance and position *cited*

### From the repository's own writing conventions

The conventions in [CLAUDE.md](../CLAUDE.md) name three patterns
the groups above do not reach.
They are defects of documentation specifically,
which is the declared target register,
and they are hypotheses in Polish like everything else here.

- **Temporal anchors** — `jeszcze`, `już`, `nadal`, `na razie`, `obecnie` —
  which pin a sentence to the moment it was written
  and let documentation rot rather than merely age.
  A word list is tier A,
  but the temporal and the logical sense share a form,
  so a rule that fires on the list alone
  will flag correct Polish more often than not.
  What has to be found first is a context test that separates the two.
- **Echo sentences** — two adjacent sentences carrying one thought,
  usually a plain version and a rhetorical one side by side.
  Lemma overlap between neighbouring sentences measures it, tier B,
  with no parse involved.
- **Ungrounded superlatives and exclusivity** —
  `naj-` forms, `jedyny`, `wyłącznie`.
  Distinct from booster inflation:
  the claim is checkable in principle and simply unchecked,
  so the flag asks for grounds rather than for a smaller word.
  The `naj-` prefix is tier A+, the rest tier B.

## What already exists

**Prose linters.**
Vale is the architecture to study:
open source, syntax-aware, extensible through a YAML rule format,
organized around the idea of a style guide,
and able to read Markdown, HTML, AsciiDoc and more.
proselint is the fixed-rule-set counterpart, in Python.
textlint is pluggable and configurable with nothing enabled by default.
The useful split is rule-based-and-configurable versus heuristic-and-fixed;
olski wants the former.

**LanguageTool is the most important existing thing.**
It is an open-source rule-based proofreading tool
with a mature Polish rule set,
described in Miłkowski's *Developing an open-source, rule-based proofreading tool*
(Software: Practice and Experience, 2010),
built on **Morfologik**,
one of the few freely licensed Polish morphological analysers,
with roughly 3.5 million forms.

That makes it either the platform to extend
or the thing to deliberately not be.
Writing olski's rules as LanguageTool XML
is a legitimate delivery route
and would come with an installed base,
an editor integration story,
and a Polish morphology layer already wired up.

**StyloMetrix**, developed at NASK,
extracts up to 195 stylometric features for Polish —
grammatical forms, lexical types,
part-of-speech frequencies, syntactic structures.
If the statistical rules need a feature extractor,
it exists and it speaks Polish.

**Wikipedia's *Signs of AI Writing***,
maintained by WikiProject AI Cleanup,
is the closest thing to the rule set olski wants:
roughly 15,000 words,
distilled from thousands of flagged articles since 2023,
explicitly descriptive rather than prescriptive.
It is English, and it is a model for how to organize such a catalogue.

**Jasnopis** remains the Polish readability tool,
scoring difficulty from 1 to 7 and simplifying automatically since 2023.
Readability is adjacent to, not the same as, style linting.

## What the research says

The strongest documented markers are lexical,
and specifically stylistic verbs and adjectives rather than content words.
In English, `delves` runs at 28 times its pre-LLM baseline,
`underscores` at 13.8,
`showcasing` at 10.7.

Across studies, measures of **lexical richness** are the most robust signal,
while most other proposed indicators
depend strongly on the particular model and text domain.
Work in PNAS finds that models
use a narrower vocabulary,
lean on auxiliary verbs,
carry fewer content words,
and fail to reproduce the stylistic variation
that distinguishes human genres from one another.

Polish work points at
repetitive sentence structures,
predictable vocabulary,
uniform sentence length,
and conspicuously textbook-correct syntax
that avoids irregular or ambiguous constructions.

**And the gap is explicit.**
The stylometric study behind those feature lists
analysed English Wikipedia introductions only,
and its authors state that the findings
do not generalize across language typologies.
Polish-targeted detectors are reported
to run at 10 to 15 percent error.
A calibrated, explainable, Polish-specific rule set
does not appear to exist.

## And fiction

The harder and more interesting wish:
some way for language models to write good Polish prose.

[fiction.md](fiction.md) is the survey behind this section:
the catalogue of documented failure modes,
the evidence that post-training rather than prompting produces them,
and the interventions that have results behind them.
What follows is the summary.

A linter cannot deliver that,
and it is worth being precise about why.
A linter removes defects.
Removing every defect from a text
produces something competent and dead,
which is already the characteristic failure of model fiction.
No amount of subtraction adds voice.

### What is nevertheless lintable in fiction

More than one might expect,
because prose craft has its own catalogue of defects,
and they are as mechanical as the technical ones:

- **Cliché** — a corpus-derived blacklist of exhausted Polish literary phrases,
  the `serce zabiło mocniej` family.
  This is the most tractable fiction rule of all,
  and it is pure tier A.
  The corpus is the trap, not the rule:
  see [fiction.md](fiction.md#what-this-means-for-olski)
  on why mining Wolne Lektury yields period marking rather than cliché.
- **Filter words** — `poczuł, że`, `zauważył, że`, `wydawało się, że`,
  constructions that hold the reader one step away from the scene
- **Adverbial dialogue tags** — `powiedział cicho`, `odparła nerwowo`
- **Repeated sentence openers**, especially subject-first every time
- **Abstraction density** — the ratio of concrete to abstract nouns,
  where model prose reliably drifts abstract

And a structural observation worth keeping:
several metrics serve both registers with **inverted thresholds**.
Technical documentation wants low sentence-length variance;
fiction wants high, and low variance is the flag.
That means one engine and one set of measurements,
with per-pack targets rather than per-pack code.

### What would actually help, and is not linting

Three directions, none of them a linter,
listed in increasing order of interest:

**Constraint instead of prohibition.**
Rules that say *you must do this*
rather than *avoid that*.
Every scene contains a physical object that recurs.
Point of view never leaves one head.
Constraints of this kind force choices a model would not default to,
which is where voice comes from.
The Oulipo understood this better than any style guide.

**Stylometric targets rather than stylometric alarms.**
StyloMetrix already extracts 195 features for Polish.
A linter uses that to measure distance from a norm and complain.
The generative move is to invert it:
name a point in that feature space —
the sentence-length distribution and lexical richness
of a particular Polish author, say —
and steer toward it.
Same instrument, opposite sign,
and far more likely to produce something with a voice
than any amount of flagging.

**The linter as a critic in a revision loop.**
This is where olski's determinism genuinely earns its place.
A model revising its own draft
against a vague instruction to write better
produces a differently bland draft.
A model revising against
*`spojrzenie` occurs eleven times in nine hundred words,
sentence lengths vary by a standard deviation of two,
and the concrete-noun ratio is half your target*
has something to actually act on.
Explainable and deterministic beats
judgement-by-another-model here,
precisely because it is the same complaint every time.

This is the best-supported of the three,
and the support is measured rather than aesthetic:
model judges rank generated fiction above New Yorker short stories,
so a revision loop with a model critic
optimizes toward the defect it was meant to remove.
See [fiction.md](fiction.md#the-evaluation-trap) for the evidence.

Honest asymmetry:
the technical-documentation linter is a project that can be finished.
Making models write good Polish fiction is an open research question.
Keeping them in that order,
with the second labelled as a wish rather than a milestone,
is what keeps this repository honest.

## Limits worth stating up front

**This cannot be a detector, and should not claim to be.**
Any linter that flags model tells
is defeated by anyone who runs the linter and fixes the flags.
That is fine — it is the same relationship
a code linter has with bad code.
The framing that survives is the one already chosen:
it helps write good Polish.
Framing it as detection would overclaim
and would age badly.

**Rules decay.**
Fingerprint rules need versioning,
a recorded date of observation,
and a policy for retiring them.
Norm-anchored rules mostly do not,
which is the second argument for anchoring to Polish style.

**False positives are the real failure mode,
and register is how they get in.**
Formal Polish written by humans — legal, academic, official —
is nominal, impersonal and hedged by convention,
and literary Polish breaks every rule deliberately.
This is why the target register is declared rather than assumed.
Rules belong to packs,
packs belong to registers,
and no rule ships without knowing which pack it is in.

## Sources

- <https://vale.sh/> — Vale, the configurable prose linter
- <https://github.com/amperser/proselint> — proselint
- <https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.971> — Miłkowski, developing an open-source rule-based proofreading tool
- <https://community.languagetool.org/?lang=pl> — LanguageTool's Polish rule community
- <https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/Guide> — WikiProject AI Cleanup guide
- <https://en.wikipedia.org/wiki/Wikipedia_talk:Signs_of_AI_writing> — discussion of the signs-of-AI-writing catalogue
- <https://www.pnas.org/doi/10.1073/pnas.2422455122> — do LLMs write like humans, variation in grammatical and rhetorical styles
- <https://www.sciencedirect.com/science/article/abs/pii/S0957417425026181> — stylometry recognizes human and LLM-generated texts in short samples
- <https://arxiv.org/pdf/2606.04177> — systematic analysis of linguistic features in AI-generated text detection
- <https://blog.humanistyka.dev/2026/03/stylometryczne-cechy-tekstow-generowanych-maszynowo> — stylometric features of machine-generated text, with StyloMetrix
- <https://blog.humanistyka.dev/2026/02/rozpoznawanie-tekstow-ai-piec-grup-cech-zamiast-jednego-wskaznika> — five groups of features
- <https://dobratresc.com/2019/02/14/rzeczowniki-zombie-i-slowa-bufony-kontra-prosta-polszczyzna/> — rzeczowniki zombie and plain Polish
- <https://mycompanypolska.pl/artykul/10-zasad-prostej-polszczyzny/16380> — ten rules of plain Polish
- <https://jasnopis.pl/prosty-jezyk/> — Jasnopis and plain Polish
