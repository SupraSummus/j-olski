# Prose linters

English has a working version of what olski is trying to build,
several times over, and none of it is Polish.
Two separable things can be taken from it.
One is an architecture: how a rule is written,
how deep it is allowed to see, and what it is scoped to.
The other is a measurement: what a rule has to prove before it ships.
The architecture is copied constantly and the measurement almost never,
which is where the room to do better is.

This document is the tool side of the field.
[similar-work.md](similar-work.md) is the controlled-language landscape,
[prior-art.md](prior-art.md) the Polish resources olski might consume,
and [linter.md](linter.md) the plan these tools are being compared against.

## Every engine makes the same three decisions

A rule is written as data or as code.
The analysis stops at characters, at tagged words, or at a parse.
The text arrives as plain prose or as markup with the prose scoped out of it.

| Tool | A rule is | Deepest analysis | Markup |
| --- | --- | --- | --- |
| Vale, Go | YAML, one of twelve extension points | POS tags, English only | parsed, rules scoped to elements |
| proselint, Python | a function, usually from a template | regular expressions | plain text |
| textlint, JavaScript | a plugin over a document tree | whatever the plugin loads | parsed, plugin per format |
| RedPen, Java | a validator class, or JavaScript | tokenizer per language | parsed, six formats |
| Harper, Rust | a `Linter` trait implementation | tokens and a curated dictionary | parsed, including code comments |
| LanguageTool, Java | XML over tokens, or a Java class | POS, chunks, n-gram lookup | plain text |

The interesting differences are inside those cells.

### Vale is the architecture to study

Rules are data, and the twelve extension points
are the whole vocabulary a rule author gets:
`existence`, `substitution`, `occurrence`, `repetition`, `consistency`,
`conditional`, `capitalization`, `readability`, `spelling`,
`sequence`, `metric` and `script`.
This is the same bet olski's engine makes —
a check is one code path plus its parameters,
a rule is a declaration — arrived at independently,
with the vocabulary grown to twelve where olski's `CHECKS` holds five.

Three of the twelve are worth naming,
because they go past the patterns and rates
that olski's five are made of.

`metric` evaluates an arithmetic formula
over thirteen built-in counters —
words, sentences, syllables, characters, paragraphs,
lists, blockquotes, code blocks, heading levels,
and three word-complexity counts —
and fires when the result crosses a threshold.
Readability scores are one instance of it rather than a special case,
which is the same generalization `length-variation` in
[rules.md](rules.md#length-variation) makes for a different metric.

`sequence` matches a run of tokens
where each token is a regular expression **or** a part-of-speech tag,
with `skip` for gaps and `negate` for exclusions.
It is a rule format for
[tier B](linter.md#how-deep-does-each-rule-have-to-see),
where a rule needs to know what a word is,
expressed as data rather than as a check per rule.

`script` runs Tengo, a Go-like language,
against the text in the rule's scope
and appends its own matches.
It is the escape hatch that keeps the other eleven small.

The limit is where it matters most here.
Vale's tagger ships an English model,
so `sequence` is English-only.
The issue proposing to route tagging through spaCy,
which would put Polish within reach because spaCy has Polish models,
was opened in July 2021 and is open.
`spelling` takes arbitrary Hunspell dictionaries, so it is not English-bound,
and `existence`, `substitution` and `metric` are language-agnostic by construction.
A Polish Vale style is therefore possible at tier A and stops there.

### proselint measured what everyone else asserts

proselint's rules are Python functions,
usually built from one of three templates —
existence, intra-document consistency, preferred form —
and its standard for admitting a rule
is that it come with a citation to a published usage authority:
Garner, the Federal Plain Language Guidelines, Strunk and White, and others.
That is the same demand olski's `justification` and `sources` fields make.

The part worth copying is the evaluation.
The 2016 paper defines a **lint score**,
one point per true positive discounted by the false discovery rate,
`l(T, F, k) = T(1 - a)^k` where `a = F / (T + F)`,
and states the reason plainly:
the score ignores false negatives
because it is more important to be quiet and authoritative
than loud and untrustworthy.
That is [the precision argument in linter.md](linter.md#abstention-is-allowed),
with a formula attached.

It was measured against a corpus of essays
from well-edited magazines — *Harper's*, *The New Yorker*, *The Atlantic* —
chosen because a tool run over expertly edited prose
should stay almost silent.
proselint reported one false positive per ten true positives
against two per one for the best other tool they tested, Microsoft Word.

Two of the paper's own limits are the openings olski has.
The corpus is copyrighted and could not be released,
and measuring against edited prose alone,
as the authors note, says nothing about how a rule performs
where the defects actually are.
The paired corpus in [linter.md](linter.md#the-thing-that-makes-or-breaks-it-calibration)
is that missing second half: a rule that fires equally on both sides is worthless,
and a single-sided score cannot see it.

The paper also ranks usage errors by detection difficulty,
from one-to-one replacement up through regular expressions,
syntax-dependent rules, and two grades of NLP, to AI-hard.
It is [the tier table](linter.md#how-deep-does-each-rule-have-to-see) again,
cut by technique rather than by machinery,
and its top level is one olski's table does not have.

And on Polish, the paper is explicit:
they have no plans to extend to other languages,
because building a linter for a language whose creators lack fluency
would be an exercise in folly.
Nobody is coming to do this.

### Harper is the argument that this should be fast

Harper is a grammar checker in Rust:
a `Document` of tokens, a `Parser` that lexes English out of whatever it is given
(including code comments), and linters as implementations of one trait.
It ships as a language server and as WebAssembly.
The claim it makes against LanguageTool is resource cost —
milliseconds per document,
and under a fiftieth of the memory —
and against Grammarly, that nothing leaves the machine.
It is English-only, with a pull request open
that adds German and Portuguese.

The relevance is not the language.
It is that a deterministic rule engine
is small enough to run on every keystroke,
which is an argument for the whole approach
that neither olski nor the style-guide linters make out loud.

### LanguageTool's deepest mechanism stops before Polish

LanguageTool's XML rules match over tokens carrying
part-of-speech tags and chunk labels,
with a separate `disambiguation.xml` deciding
which reading of an ambiguous token survives —
a rule format that has been running against real Polish for years.
See [linter.md](linter.md#what-already-exists)
for what that means as a delivery route.

Its most advanced mechanism is not available in Polish.
Confusion pairs — words swapped for their neighbours — are decided
by looking up competing n-grams in a corpus-derived index
of roughly eight gigabytes,
and that data exists for English, German, French and Spanish only.
Polish gets the rule format and not the statistics.

## Japanese is the proof that this transfers

The evidence that this works
in a language where morphology carries the information
is not English at all.

`textlint-rule-preset-ja-technical-writing` is a rule pack
for Japanese technical documentation:
sentence length, commas per sentence,
consistency of the polite and plain registers,
doubled particles, weak phrasing, redundant expressions.
Twenty-three rules, of which five need the morphological analyser
and the rest work on characters and counts.
That is olski's tier A and tier B split,
measured on a shipped rule set,
and it comes out where [the tier table](linter.md#how-deep-does-each-rule-have-to-see)
predicts: most of the value below the morphology line.

The same authors ship `textlint-rule-preset-ai-writing`,
which is the linter track's counterpart in another language:
mechanical list formatting, hype vocabulary, mechanical bold emphasis,
colon-before-block constructions that read as translated English,
and a technical-writing guideline rule with optional document-level statistics.
One of its five rules uses morphological analysis
to decide whether the clause before a colon ends in a predicate,
which is a defensible native-Japanese judgement
rather than a list of words a model likes.
That distinction is the one
[anchoring to norms rather than fingerprints](linter.md#anchor-to-polish-norms-not-to-model-fingerprints)
is about, and Japanese got there first.

Neither preset carries a measurement
of how often it fires on human Japanese.

## The direct competitors are word lists

The English rule sets aimed at model prose specifically
are built the shallowest way available.

`vale-ai-tells` is the largest: 78 rule files in three packs,
one for prose, one for commit messages, one experimental,
citing the PNAS and excess-vocabulary studies
alongside practitioner catalogues.
A second ruleset compiles Wikipedia's *Signs of AI Writing*
into Vale rules at three severity levels.
`slop-gate` is a CLI with the em dash and some forty English tells,
plus opt-in translationese packs
for Korean, Russian, Chinese, Vietnamese and Filipino.
`awesome-slop` is the catalogue of all of it.

Three things are true of the whole group.
They are token matching, so they inherit
[the recognition problem](linter.md#recognizing-a-phrase-by-what-it-is-not-costs-more)
without a way to address it, and `vale-ai-tells` says as much:
sentence uniformity needs statistics Vale cannot express.
None of them reports a false-positive rate against human text.
And Polish appears in none of them, including the translationese packs.

The research they cite is better than the rules they produce.
The PNAS work they draw on measures constructions rather than words —
participial clauses and nominalizations at multiples of the human rate —
and those are the findings that survive translation into another language.
[What the research says](linter.md#what-the-research-says) owns the numbers.

## What beating them takes

**Take the lint score, knowing what it is not.**
The two numbers milestone 1 puts in a rule's `calibration` field
are firing rates, and a false discovery rate is not one:
a rate counts hits, and `a = F / (T + F)` needs each hit
classified as a real defect or a false alarm,
which is a human reading every one of them.
What connects the two is the assumption proselint made
when it picked expertly edited magazines —
that a hit on prose that good is a false alarm —
under which the human-side rate estimates `a`
and the lint score follows for free.
The assumption is the part to say out loud,
because a good writer's paragraph can still hold a real defect.
The pair then measures more than proselint could:
one side estimates trustworthiness, the other discrimination.
The Polish corpus can also be released,
because Wolne Lektury is public domain
and the generated half is generated,
which is the wall proselint's copyrighted corpus hit.

**Leave markup scoping alone.**
Vale, textlint and RedPen parse the markup themselves
and let a rule name the elements it applies to.
olski settled that question the other way:
formats stay outside the linter,
and a check that needs prose
[declines on a file whose format cannot give it](rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives).
The bill arrives in the delivery route,
where a Vale style would get the separation for free,
and [open-questions.md](open-questions.md#linter-questions) is where it is paid.

**Take the `sequence` shape.**
A token pattern where each position is a regular expression or a tag
buys more in Polish than in English,
because a Morfeusz tag carries case, number, gender and aspect,
not just a part of speech.
It can express agreement inside a chunk,
which is [the case](linter.md#recognizing-a-phrase-by-what-it-is-not-costs-more)
that neither a better regex nor a lemma reaches.

**Keep the two things none of them has.**
Abstention is one.
No tool surveyed here documents a third outcome,
so a threshold that was not met
and a document too short to measure a rate over
leave the same trace, which is none.
Registers are the other.
proselint's defence against the charge of homogenizing prose
is that technical writing is the register where consistency is the point,
and that defence lives in a paper:
the rule set itself does not say which register it is for.
An olski rule carries its registers as a field,
and `--list-rules` prints them beside the pack and the tier,
which is [declaring the target register](linter.md#the-target-register-technical-documentation)
rather than assuming it.

**What does not carry.**
The n-gram confusion mechanism has no Polish data.
Readability formulas are calibrated on English syllable counts;
Polish has Jasnopis.
And the word lists themselves are worth nothing in translation —
`delve` has no Polish equivalent to look up,
only a Polish equivalent to go and measure.

## Sources

- <https://docs.vale.sh/> — Vale's documentation, including the twelve extension points
- <https://docs.vale.sh/checks/sequence> — the POS-tag token-sequence check
- <https://docs.vale.sh/checks/metric> — formulas over built-in counters
- <https://docs.vale.sh/checks/script> — the Tengo escape hatch
- <https://docs.vale.sh/checks/spelling> — arbitrary Hunspell dictionaries
- <https://github.com/jdkato/prose> — the Go NLP library behind Vale's tagging, English models
- <https://github.com/errata-ai/vale/issues/356> — multilingual NLP, open
- <https://suchow.io/assets/docs/pacer2016proselint.pdf> —
  Pacer et al., *Linting science prose and the science of prose linting*, SciPy 2016:
  the lint score, the false discovery rate, the difficulty hierarchy,
  and the refusal to extend to other languages
- <https://github.com/amperser/proselint> — proselint
- <https://writewithharper.com/docs/contributors/architecture> — Harper's crates and traits
- <https://github.com/Automattic/harper> — the resource claims against LanguageTool
- <https://github.com/Automattic/harper/pull/3402> — German and Portuguese, open
- <https://dev.languagetool.org/finding-errors-using-n-gram-data.html> —
  the n-gram index, its size, and the four languages it covers
- <https://github.com/redpen-cc/redpen> — RedPen's validators and formats
- <https://github.com/textlint-ja/textlint-rule-preset-ja-technical-writing> —
  the Japanese technical-writing preset
- <https://github.com/textlint-ja/textlint-rule-preset-ai-writing> —
  the Japanese AI-writing preset
- <https://github.com/tbhb/vale-ai-tells> — 78 Vale rules for model tells
- <https://ammil.industries/signs-of-ai-writing-a-vale-ruleset/> —
  Wikipedia's catalogue compiled into Vale rules
- <https://github.com/hwajongpark/awesome-slop> —
  the catalogue of tools, word lists and research, and the languages they cover
- <https://www.pnas.org/doi/10.1073/pnas.2422455122> —
  do LLMs write like humans, with the participial and nominalization rates
- <https://arxiv.org/abs/2509.19163> — Shaib et al., *Measuring AI "Slop" in Text*
