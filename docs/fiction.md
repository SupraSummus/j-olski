# Fiction: what goes wrong, and what is known to help

[linter.md](linter.md#and-fiction) files fiction as a wish rather than a milestone,
and keeps it there deliberately.
This document is the survey behind that decision.

It is a catalogue of failure modes,
an account of where they come from,
and a short list of interventions that have evidence behind them.

It is deliberately qualitative.
The literature is full of percentages,
and almost all of them are properties of a particular model generation
measured on a particular corpus.
The observations outlive the numbers,
so the observations are what is recorded here.

Everything below is English-language research
unless marked otherwise.
See [the honesty section](#how-much-of-this-is-actually-established)
for what that costs.

## The failure modes, by the depth needed to see them

This reuses [the tier ladder](linter.md#how-deep-does-each-rule-have-to-see),
because the same question decides everything:
how much analysis does a defect require before a tool can name it.

The catalogue sorts almost too neatly.
The defects that are easy to see are the ones that matter least,
and the defects that make model fiction unreadable
sit at a depth no linter reaches.
That is the finding, not an accident of presentation.

### Word and phrase

The most documented layer, and the shallowest.

**Over-represented phrasing.**
The *Antislop* work treats this as an inventory problem:
profile a model's output against a human baseline,
and collect the words, phrases and n-grams
that come out disproportionately often.
The resulting lists run to thousands of entries per model.
Sam Paech's *slop-forensics* pushes the same data further
and builds a similarity tree over models from their phrase profiles alone,
treating each phrase as a trait and each model as a species.
Models are identifiable from their verbal tics,
which is a strong statement about how narrow the tics are.

**Abstract-noun frames.**
The expert-edit study behind the LAMP corpus
found models reaching repeatedly for a small set of nominal frames
that professional writers do not use at that rate —
*the weight of*, *a sense of*, *a mix of X and Y* —
and for particular words, *unspoken* chief among them,
at frequencies with no human counterpart.
These are not clichés in the usual sense.
They are grammatical habits that produce clichés.

**Negation-substitution.**
*It was not a current. It was a summons.*
The *not X; Y* frame is near-universal in model fiction
and is the single most recognizable sentence shape in the corpus.
It is also trivially detectable and trivially removable,
which is why it will be the first thing to disappear.

**Triples.**
Three-item lists, especially escalating ones,
used as the default rhythm rather than as an effect.

**Metaphor density without occasion.**
Sensory comparisons clustered thickly
where nothing in the scene called for them.

One caution that generalizes:
the em dash was the canonical tell for years,
and newer models have largely stopped —
while keeping the sentence structures the em dash used to punctuate,
now joined by semicolons and commas.
The fingerprint moved down a layer rather than going away.
Rules anchored to the character
died while the defect they were proxying for survived.
This is the concrete case for
[anchoring rules to norms rather than to fingerprints](linter.md#anchor-to-polish-norms-not-to-model-fingerprints).

### Sentence and paragraph

**Uniformity.**
Sentence length, paragraph length and sentence opener
all vary less than in human prose.
Human writers break rhythm constantly and mostly unconsciously;
models hold a cadence.

**Inability to leave a local minimum.**
The observation from the web-fiction community is that
a human writer who notices a rut instinctively breaks it,
and a model settles into one and stays,
producing what one reader calls droning.
The tell is not any individual sentence but the consistency across a long passage.

**Blockiness.**
Text separating into visibly demarcated zones:
a block of dialogue, a block of exposition, a block of narration,
rather than the three interleaving as they do in worked prose.

**Purple prose alternating with plain cliché.**
Ornate vocabulary and exhausted phrasing sitting next to each other.
The alternation itself is the signal —
a human stylist committing to ornament stays ornate.

**Craft defects with names already.**
Filter words that hold the reader a step back from the scene,
adverbial dialogue tags,
emotion named instead of shown,
abstraction where a concrete detail belongs.
Creative-writing pedagogy has been cataloguing these for a century,
and model prose commits all of them at once.
The LAMP editors' categories are the same list arrived at independently:
awkward phrasing, poor sentence structure,
redundant exposition, cliché, purple prose,
lack of specificity, tense drift.

### Scene and character

Past what a rule can reach, and where readers actually give up.

**Undifferentiated dialogue.**
Every character speaks in the same register.
Nobody has an idiolect, so nobody has a personality
beyond the one or two traits the prose has latched onto and keeps restating.

**Curt or artificially clipped exchanges,**
ending on manufactured beats.

**Shallow interiority.**
Emotion and motive rendered formulaically rather than convincingly.
Expert readers in the style-imitation study,
asked what they were actually keying on,
named narrative voice and character interiority first —
not the surface tics that detection research concentrates on.

### Narrative

The layer the discourse-level studies below measure,
and the one no linter touches.

**Over-explanation of theme.**
*StoryScope*, which analyses discourse-level narrative features
rather than surface style,
finds that AI stories explain their own meaning.
The story tells you what it was about.

**Tidy single-track plots.**
The same work finds AI narratives favour clean single lines of causation,
frame protagonists' choices as morally unambiguous,
and carry much less temporal complexity than human stories.
Human-written stories occupy a far wider region of narrative space;
model output clusters.

**Positivity bias and arc collapse.**
Work on discourse-level narrative structure finds models
strongly over-producing recovery arcs
and almost never producing arcs that end badly.
The tragic shapes are effectively absent.

**Premature resolution.**
The same line of work finds models placing early turning points correctly
and then rushing the setback and the climax,
so tension collapses well before the end.
Affective intensity stays flat where human stories widen their range.

**Flattened emotional range.**
High-intensity emotion gives way to neutrality.

### Long-form

Defects that only appear at length, and are mostly mechanical.

*ConStory-Bench* organizes them as consistency classes:
character, plot, world, temporal, and coreference.
The community reports on generated novels add the cruder ones:
paragraphs and whole scene-introductions recurring verbatim across chapters,
a model abandoning an outline it wrote itself
(killing characters the plan required to survive, or the reverse),
and chapters that simply stop mid-sentence.

These are the most fixable failures in the catalogue
and the least interesting,
because none of them is a prose problem.

## Why this happens

An absence sits underneath both mechanisms below.
Reinforcement learning against a verifier
produced the jumps in code and mathematics,
where a rule-based checker returns a binary signal for free.
Writing has no such checker,
so the only signal available at scale is human preference,
and what that preference contains decides everything downstream.
The same literature names the limit inside code as well:
what the verifier does not check —
maintainability, and the later consequences of a design —
goes unlearned there too.

Two mechanisms have real evidence, and they point the same way.

**Typicality bias in preference data.**
The *Verbalized Sampling* work argues that human annotators,
with correctness held constant,
systematically prefer the more predictable of two responses.
Once that preference enters a reward model,
optimizing against it sharpens the output distribution —
mathematically like lowering temperature.
Where a task has one right answer this costs nothing.
Where many answers are equally valid, which is the definition of creative work,
typicality becomes the tiebreaker
and the distribution collapses onto the most ordinary option.

**Post-training compresses narrative variation.**
The *narrative flattening* study is the cleanest experiment in this literature.
It takes four checkpoints of one model — base, SFT, DPO, RLVR —
sharing architecture, scale, tokenizer and pretraining,
so the only variable is post-training.
Thematic movement, affective range and stylistic diversity
all compress progressively along that chain.
The effect is largest against professional literary fiction as a baseline
and smallest against ordinary online story-platform prose,
which is to say:
the better the human writing you compare against,
the wider the gap.
And the post-trained endpoints converge with each other
regardless of which kind of fiction they were asked to continue,
which means alignment produces a single continuation manner
insensitive to what it is continuing.

The consequence for this repository is direct.
These defects are not prompting mistakes and not model-specific quirks.
They are produced by the alignment stack,
they are systematic, and they are stable across models.

That is bad news for fiction and good news for a linter.
A defect that appears because of how models are trained
is exactly the kind of defect a fixed rule set can be calibrated against —
unlike a vocabulary tic, which is a property of one release.

## The evaluation trap

This is the part that most changes what olski should try to be.

**Model judges get fiction backwards.**
On the leading creative-writing benchmark,
LLM judges scoring against a rubric
rank zero-shot AI stories *above* New Yorker short stories.
Not close to them. Above them.

**And the reason is legible.**
The *Style over Story* work finds that when models choose between narratives,
they weight surface polish over narrative substance,
preferring the better-groomed passage
even when the alternative is the more coherent story.

**A metric that does not have this failure exists,**
and it works by not asking for a judgement.
The *100-Endings* approach measures tension
by repeatedly predicting how the story ends
and treating prediction failure as evidence of tension.
It ranks New Yorker stories far above model output,
which is the ordering the rubric judges inverted.

**A second metric of the same kind measures surprise directly.**
Human continuations are markedly less predictable to a model
than the model's own,
the gap is wider for creative writing than for news or essays,
and instruction-tuned and reasoning variants widen it further —
the flattening experiment above, arrived at through a different instrument.
Its shape matters as much as its direction.
Quality against unpredictability is an inverted U,
peaking high but short of the extreme,
so the quantity has an optimum rather than a maximum.
Its cost is that computing it takes a language model,
which this repository does not use for anything
and which the retired linter track declined to take on.

Three things follow.

You cannot bootstrap fiction quality with a model judge.
Any revision loop whose critic is a model asked *is this good writing*
will optimize toward the polish the judge rewards,
which is the defect.

Measurement that commits to something specific and checkable
beats holistic judgement,
even when the specific thing is a proxy.

And this is the strongest available argument
for [the critic-in-a-revision-loop idea](linter.md#what-would-actually-help-and-is-not-linting).
Not because a deterministic critic is clever,
but because the obvious alternative has been measured and is broken.

## What is known to help

Roughly in order of how well supported each is.

**Fine-tuning on a real body of prose, rather than prompting with it.**
The strongest single result in this literature.
Given the task of writing in a named author's style,
models prompted with excerpts and a style description
lose badly to human writers in expert judgement.
The same task, with a model fine-tuned on that author's actual books,
flips the expert preference the other way —
on both quality and fidelity.
The MFA-trained judges who could reliably spot the prompted output
could not spot the fine-tuned output.
What disappears is precisely the surface layer of this catalogue:
the tics, the awkward phrasing, the ornamental excess.
Style is apparently in the weights or nowhere;
a context window of examples does not transfer it.

This is also the result with the ugliest implications,
since the training data is somebody's copyrighted body of work.
The Polish-language commentary on it treats that as the main point,
and it is a reasonable reading.

**Narratological structure imposed from outside.**
Giving the generator an explicit plan
in the vocabulary narrative theory already has —
turning points, arc shape, where the setback goes —
measurably improves suspense and diversity
over asking for a story and hoping.
Making the model generate its own turning points first
works better than supplying them.
The generic *write an outline first* does less;
what helps is a plan in terms the theory has named.

**Distribution-level prompting.**
Asking for several candidates with their probabilities,
rather than asking for the answer,
recovers a large part of the pre-training diversity
that post-training compressed.
Same model, same weights, different question.
The mechanism follows from the typicality-bias account:
an instance-level prompt collapses to the single most typical item,
a distribution-level prompt collapses to a spread.
The gains grow with model capability,
which is not what you would expect
if this were a trick that better models would outgrow.

**Editing, with limits.**
Expert edits of model paragraphs improve them,
and readers prefer edited text to unedited by a wide margin.
Automated editing against the same taxonomy captures some of that gain.
But expert-edited beats machine-edited,
identifying which span is defective is much easier
than agreeing on what is wrong with it,
and no amount of editing produced text
that experts preferred to human originals.
Subtraction works and then stops working,
which is the same conclusion linter.md reaches from the other direction.

**Suppression at the right granularity.**
The *Antislop* result worth keeping is architectural.
Banning tokens outright breaks down early —
the vocabulary is load-bearing and you run out of room.
Banning *strings*, with backtracking when one appears,
scales to thousands of patterns without damaging fluency,
and the same targets distilled into a token-level fine-tune
hold up without hurting reasoning benchmarks.
The generalizable point:
the unit of suppression should be the phrase, not the word,
and it needs the ability to retract.

**What does not help.**
Prompting a model to write better, without a specification.
Rubric-based model judging, for the reasons above.
Longer context windows, for consistency —
the outline-abandonment and verbatim-repetition failures
happen well inside the advertised window.

## What this means for olski

**The inverted thresholds have measurements behind them.**
Sentence-length variance, lexical richness, abstraction ratio and affective range
are all measured in both directions in this literature:
where technical documentation wants uniformity, fiction wants range.
That is the evidence under
[one engine with per-pack targets](linter.md#and-fiction).

**The tractable Polish fiction rules are the shallow ones,**
and they are worth building because they are cheap, not because they are important:
the negation-substitution frame,
triples used as default rhythm,
repeated sentence openers,
filter constructions,
adverbial dialogue tags,
sentence-length variance below a literary norm,
concrete-to-abstract noun ratio.
Every one of these is tier A or A+ in Polish
and none of them requires the grammar.

**The cliché blacklist has a corpus trap in it.**
linter.md calls a corpus-derived Polish cliché list
the most tractable fiction rule of all.
It is tractable, but the obvious corpus is a hazard.
Wolne Lektury is overwhelmingly pre-war,
so phrases mined from it are period-marked rather than exhausted,
and a rule set built on it would flag
contemporary Polish prose for not sounding like Prus.
A cliché list needs a contemporary human baseline
and a contemporary generated comparison,
which is the same paired corpus the technical rules need.

**The slop lists cannot be imported.**
They are English, they are per-model, and they date.
What transfers is the *pipeline*:
generate Polish on matched prompts, profile against human Polish,
keep what is over-represented.
That is a method, and it is the same method
the technical rule pack's calibration already requires.
Building it once serves both packs.
Note also that the phrase profiles are model-identifying,
which means a Polish profile will be per-model too,
and a rule pack built from one model's profile
is a rule pack about that model.

**The critic-in-a-revision-loop direction rests on this evidence,**
rather than on a preference for determinism.
Model judgement on fiction inverts the ordering it was meant to reproduce,
while committing to a specific checkable quantity does not.
That is what this survey contributes to
[the direction linter.md favours](linter.md#what-would-actually-help-and-is-not-linting).

**And the ceiling is worth stating precisely.**
Nothing at any tier reaches
theme over-explanation, premature climax, arc monotony,
undifferentiated dialogue, or shallow interiority.
Those are the defects that make model fiction unreadable.

**Four of those five look like one defect.**
Each is a failure to hold several models of a mind apart across a text:
the characters' and the reader's.
Nobody has an idiolect because nobody is a separate mind,
interiority stays shallow because there is no mind there to render,
the theme gets explained because nothing tracks what the reader has inferred,
and tension collapses early because nothing tracks
what the reader has been made to expect.
Arc monotony is the loose one
and groups with the positivity bias above instead.
Read this way the ceiling is a prediction rather than a policy:
the four move when mind-modelling moves,
and not for a better rule, a better prompt or a longer context.
The reading is this document's rather than the literature's,
and [the honesty section](#how-much-of-this-is-actually-established)
says what would settle it.

A tool that removes every defect it *can* see
produces prose with no tells and no voice,
which is the failure linter.md already names,
with this document as its evidence.

## How much of this is actually established

**It is almost entirely English.**
Every study cited here works on English text.
Polish contributes a narratological reading of AI-generated short stories —
Lutostański's argument in *Forum Poetyki* that model output
simulates the formal properties of narrative
without doing what fiction does —
and some commentary on style extraction.
No Polish equivalent of the phrase profiles,
the discourse-feature work, or the flattening experiment exists.
The gap noted in linter.md for technical Polish
is wider for literary Polish.
[generated-polish.md](generated-polish.md) narrows one corner of it,
by measuring two of the failure modes catalogued here
on a body of Polish that one model wrote.

**Much of it is detection research wearing a critic's hat.**
StoryScope and the stylometric work select features for *separability*.
A feature that distinguishes AI from human prose
is not thereby a feature that distinguishes good prose from bad.
The overlap is real but it is an overlap, not an identity,
and reading detection features as a style guide
is how a linter ends up punishing human writing.
The catalogue above is more trustworthy where independent lines converge —
expert editors, detection features and reader anecdote
all naming the same defect — and thinner where only one does.

**The single-cause reading of the ceiling is this document's.**
The studies catalogue those defects separately and do not connect them,
and whether models model minds at all is contested in both directions:
they reach adult scores on higher-order false-belief tasks,
those scores fall apart under small perturbations of the task,
and contamination is plausible either way,
because the tasks are decades old and published.
The reading asks for less than that debate settles.
What would test it is whether dialogue differentiation and interiority
move together with a measure of mental-state tracking maintained over a text,
which nobody has built.

**The corpora are short stories.**
The narrative-structure findings mostly rest on synopses and short fiction.
Novel-length claims come from consistency benchmarks
and from readers reporting on generated novels,
which is weaker evidence and reads like it.

**And every quantity in this literature is a moving target.**
Which is the reason this document does not quote them.

## Sources

Research:

- <https://arxiv.org/abs/2604.03136> —
  StoryScope, discourse-level narrative features,
  over-explained themes and single-track plots
- <https://arxiv.org/abs/2605.27878> —
  narrative flattening across base, SFT, DPO and RLVR checkpoints
- <https://arxiv.org/abs/2604.09854> —
  narrative forecasting as a tension metric,
  and rubric judges ranking AI fiction above New Yorker fiction
- <https://arxiv.org/abs/2602.16162> —
  the surprise gap between human and model continuations,
  and quality as an inverted U over unpredictability
- <https://aclanthology.org/2024.emnlp-main.978/> —
  story arcs, turning points and affective range in LLM narratives
- <https://arxiv.org/abs/2409.14509> —
  the LAMP corpus, expert edits of model paragraphs, and the edit taxonomy
- <https://arxiv.org/abs/2510.15061> —
  Antislop: the backtracking sampler, the profiling pipeline, and FTPO
- <https://arxiv.org/abs/2510.01171> —
  Verbalized Sampling, typicality bias, and distribution-level prompting
- <https://arxiv.org/abs/2506.00103> —
  why writing gets no verifier,
  and what a verifier leaves unlearned inside code
- <https://arxiv.org/abs/2510.02025> —
  Style over Story: model judges weighting polish over narrative substance
- <https://arxiv.org/abs/2601.18353> —
  fine-tuning on authors' books versus prompting with excerpts
- <https://arxiv.org/abs/2603.05890> —
  ConStory-Bench and the consistency-bug classes in long generation
- <https://arxiv.org/abs/2412.13575> —
  dynamic hierarchical outlining for long-form stories
- <https://arxiv.org/abs/2507.00769> —
  LitBench, on evaluating creative-writing verifiers
- <https://www.pnas.org/doi/10.1073/pnas.2405460121> —
  models at or above adult scores on false-belief tasks
- <https://arxiv.org/abs/2310.19619> —
  theory of mind across situated tasks, finding none coherent

Tools and lists:

- <https://github.com/sam-paech/slop-forensics> —
  phrase profiling, and model lineage inferred from slop profiles
- <https://github.com/sam-paech/auto-antislop> —
  the profile-and-suppress pipeline, as a method to copy
- <https://eqbench.com/creative_writing.html> —
  the creative-writing leaderboard, with slop and repetition components
- <https://eqbench.com/slop-score.html> —
  how the slop score is computed

Polish:

- <https://pressto.amu.edu.pl/index.php/fp/article/view/55214> —
  Lutostański, *Poza fikcjonalnością*, Forum Poetyki 2026:
  simulated narrative form without fictional intent
- <https://blog.humanistyka.dev/2026/07/skuteczna-maszynowa-ekstrakcja-stylu-to-powazne-wyzwanie-dla-literatury> —
  machine style extraction and what it means for authors
- <https://wszystkoconajwazniejsze.pl/pepites/ai-i-jezyk-polski-czy-polszczyzna-przetrwa-epoke-modeli/> —
  why thin Polish training data produces calques and flat style

Practitioner accounts, useful for the craft layer and weaker as evidence:

- <https://recordcrash.substack.com/p/how-to-identify-ai-written-web-fiction> —
  negation-substitution, triples, blockiness, droning,
  and the em dash migrating rather than disappearing
- <https://coyotetracks.org/blog/ai-writing/> —
  generated novels: repeated scenes, abandoned outlines,
  told-not-shown openings
