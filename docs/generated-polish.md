# A body of generated Polish, measured

[linter.md](linter.md#the-thing-that-makes-or-breaks-it-calibration)
needs a paired corpus and calls the generated half the easy half.
This document reports what one already-written generated half contains.

Two shipped rules get their first datapoint,
two patterns go onto the candidate inventory,
one defect from above the phrase turns out to be countable
and gets a check written against it,
and the word *easy* loses a condition.

## What was measured

The corpus is the writing of `SupraSummus/the-agent`,
an agent that keeps its own repository and writes into it session by session.
It holds two separate bodies of Polish prose:

| | documents | prose words | sentences |
| --- | --- | --- | --- |
| Notes for an unwritten science-fiction novel | 527 | 155,413 | 14,890 |
| A philosophical memoir | 9 | 25,424 | 3,001 |

One model family, one author, and a session log
running from 2026-02 to 2026-04.

The numbers below come from two different places,
and the difference decides how much weight each carries.

**Counts over the files as they stand.**
The quotation figures are of this kind:
walk the quotation marks of every file in order
and record what closes each `„`.
Anyone with the clone can redo that and should get the same answer.

**Counts over extracted prose.**
Every rate and every positional figure needs a denominator,
so it needs the prose separated from the apparatus first:
YAML frontmatter, headings, tables, the link lists that close each note
and the question-and-answer blocks under them removed,
hard-wrapped source unwrapped before sentences are split,
and 40 of the 567 notes dropped for being written in English,
which the share of words carrying a Polish diacritic separates cleanly.
That extraction was written for this measurement and is not in this repository,
so these figures are reported rather than reproducible.
They are the ones a harness has to earn back;
[TODO.md](../TODO.md) names the next move.

The property that makes the corpus worth reading
is not its size but its git history,
which records every editorial intervention made on it
and the reasoning behind each one.
[What happened when the rules were deleted](#what-happened-when-the-rules-were-deleted)
is the part of this document that depends on that history.

## Polish closing quotation marks are absent

Of 1,995 quotations opened with the Polish `„`,
1,984 close with a straight `"` and 10 close with `”`.

| | opened `„` | closed `"` | closed `”` | never closed |
| --- | --- | --- | --- | --- |
| Notes | 1,520 | 1,509 | 10 | 1 |
| Memoir | 475 | 475 | 0 | 0 |

The two bodies were written months apart, on unrelated subjects,
and disagree by half a percent,
so this is a property of the writer rather than of one drafting session.

What the shape of the error says
is that the convention is half-known rather than unknown.
Ignorance of Polish quotation produces `"tekst"`.
This produces `„tekst"` —
the opening mark chosen correctly and deliberately,
the closing mark defaulting to the ASCII character.
The likely reason is that `„` has no other job,
while `”` competes with a `"` that means a closing quote
nearly everywhere else a model has read.

This does not argue for a new rule.
It argues that `quote-straight` is a better rule than it looks.
A straight quotation mark is usually ambiguous —
an inch mark, a fragment of code, a citation left in English —
and a rule flagging every one of them needs exemptions for all three.
Here it needs none:
the `„` a few words to the left says what the character is doing,
so the rule's hardest case is settled by the text rather than by a threshold.
That makes it cheap to calibrate,
which is the scarce property in
[the calibration problem](linter.md#the-thing-that-makes-or-breaks-it-calibration)
and a reason to measure this rule before the ones with numbers in them.

## The em dash rate has room above the threshold

`em-dash-density` allows 10 per thousand words.
The notes run at 35.9 and the memoir at 34.7.

This does not calibrate the rule.
Calibration is the firing rate on good human Polish,
and no human Polish was measured here.
What it settles is a smaller question that comes first:
whether the threshold was set so high
that generated text passes it untouched.
It was not, by a factor of three and a half,
in two independently written bodies.

## What the em dashes are doing

[fiction.md](fiction.md#word-and-phrase) records *not X; Y*
as the most recognizable sentence shape in English model fiction.
Its dominant Polish realization here is punctuated, not lexical.

Per thousand words, in the notes:

| frame | rate |
| --- | --- |
| `nie` … `—` | 8.29 |
| `nie X, ale Y` | 1.29 |
| `nie X, lecz Y` | 0.55 |
| `nie dlatego, że` | 0.43 |
| `To nie jest X. To jest Y.` | 0.16 |
| `nie tylko X, ale Y` | 0.03 |

The dashed form outruns every lexical form put together
by more than a factor of three,
and the memoir gives the same ordering at 6.10 per thousand.
Counted from the other side,
1,288 of the 5,573 em dashes in the notes
stand immediately after a negated clause,
and 155 of 881 in the memoir — 23% and 18%.
*Na Reseda-3 ćwiczenie nie jest rutyną — jest wspomnieniem*
is the frame in its pure form.

Two entries in
[the candidate inventory](linter.md#candidate-rule-inventory)
are therefore one construction:
em dash frequency, filed under typography,
and parallel-negation frames, filed under structural and statistical.
The dash carries the frame,
which puts a quarter of the corpus's dashes inside it,
so the density rule already fires on the construction
without having been aimed at it
and a rule written for the construction would take those dashes with it.
Which of the two to write is a calibration question
and not a design question,
since only a human baseline can say
whether Polish prose that is not generated
puts a dash after `nie` at a materially lower rate.

## The closing sentence is measurably different

Model fiction explaining its own theme is filed in
[fiction.md](fiction.md#narrative)
under the layer no linter reaches.
Position brings part of it back within range,
because the explanation arrives at a place a tool can point at.

Comparing the last sentence of each section against every other sentence:

| | sections | negation, non-final | negation, section-final | |
| --- | --- | --- | --- | --- |
| Notes | 1,744 | 25.0% | 38.2% | p = 4·10⁻³¹ |
| Memoir | 132 | 29.3% | 41.7% | p = 0.003 |

Sections of fewer than four sentences are left out,
because the last of three sentences is not a position.
Two independently written bodies give the same direction.
The obvious companion hypothesis fails:
section-final sentences are *longer* than the rest,
by 11.7 words against 9.8 in the notes,
so the aphorism at the end of a section
is not the short punchy sentence it is usually described as.

The limit is worth stating in the same place as the finding.
This is a shift in a rate, not a property of a sentence.
A rule firing on every negation in a final position
would be right about thirteen points of the thirty-eight
and wrong about the twenty-five it would have flagged regardless.
What the measurement supports is a document-level report —
*your sections end on a negation three times in eight* —
which is the shape
[the critic in a revision loop](linter.md#what-would-actually-help-and-is-not-linting)
already wants.

## Two entities in five are introduced and dropped

The notes set an entity up with apparatus 509 times —
a capitalized word followed by a parenthesis containing a number,
which is how this corpus introduces a person
(*Nara (fizyczka, 31, Iris, Sol)*) and a place alike.
214 of those entities, 42%,
are named fewer than three times in the note that introduced them,
the introduction counted among the three.
Such an entity is a walk-on.

The corpus's own documentation reaches the same defect by reading
rather than by counting:
its account of what makes one of its notes weak
describes characters arriving with a parenthetical CV,
performing the function the note's topic requires, and exiting.
Two methods over one corpus is weaker than two corpora,
but a defect that reading and counting both arrive at
is the kind [fiction.md](fiction.md#how-much-of-this-is-actually-established)
says to trust further than one that only one of them finds.

A single walk-on is not a defect,
which is the whole reason the figure is a share over a body of text.
Plenty of entities are named once because once is what they are worth,
and only the rate says whether a text has a habit.
`entity-recurrence` in [rules.md](rules.md#entity-recurrence) is that measurement,
and this is the number it was written against.

What the figure is a rate over is worth stating precisely.
The pattern captures one capitalized word,
so a two-word system name enters the count as its second word —
*Ceti*, *Eridani*, *Centauri* are all among the 201 distinct captures —
and a sentence-initial adverb standing before a parenthesized number
enters it as a name, which is how *Teraz* got in.
The second kind of error inflates the answer,
because a word that is not an entity is rarely repeated
and therefore counts as a walk-on,
so 42% is an upper bound on the thing it is measuring
rather than an estimate of it.
Narrowing the pattern is the obvious next move
and it needs the same human baseline everything else here needs:
a rate this loose is worth having only against another rate
measured the same loose way.

This is a count over the files as they stand,
so it belongs with the quotation marks rather than with the rates,
and anyone with the clone can redo it.
What is new is that the check is in this repository:
redoing it means running a rule rather than writing an extraction.

## What happened when the rules were deleted

The agent wrote regex detectors for its own Polish prose patterns,
ran a campaign against the counts they reported,
and then deleted the detectors.
The reasoning is recorded in the commit that removed them,
which is why this is evidence rather than an anecdote.

The stated reason for deletion was not that the tools missed defects.
It was that acting on them damaged the text:
a grounding check *pushed sensory palette homogenization*,
a social-texture check *forced social markers into technical notes*,
and a prose-quality check went with them as
*the last remaining literary-judgment check*.
No rule was tuned. The category was abandoned.

That is the failure mode
[linter.md](linter.md#the-thing-that-makes-or-breaks-it-calibration)
names as the reason for preferring precision to recall,
and it prices the preference higher than the argument there does.
The cost of a false positive was not the flag.
It was that a writer optimizing against the flag
moved the prose in the direction the flag pointed,
so the damage was done by the rule working as designed
and the removal came after it rather than before.

The principle written down afterwards is worth quoting
because it is nearly olski's and not quite:
*tools should only automate checks
with right answers independent of context.
Don't build checks that make literary judgments.*

Olski's [abstention](linter.md#abstention-is-allowed) draws the line
one step further out.
A rule whose answer depends on context does not have to be forbidden;
it has to notice the dependence and decline.
The case above is not a test of that,
because none of the deleted checks could abstain —
each returned a judgement on every input it was given.
What it does establish is the cost of getting this wrong,
which is not a rule nobody trusts
but a body of prose edited into the rule's own image
before anyone notices.

The checks that survived the deletion sort cleanly.
Contradiction, concept drift, link accuracy and isolation stayed;
every one of them is a consistency check rather than a style check.
That is the same division
[fiction.md](fiction.md#long-form) draws
between the mechanical consistency classes and everything above them,
arrived at from the other end by someone with a book to finish.

The same commit deleted a second tool aimed a layer higher,
and it failed differently.
Beside the prose detectors stood a registry of eleven genre-exhausted ideas —
the unknowable alien, the multi-generational war, the lone operator —
each with the works it comes from and a note on how to avoid leaning on it,
and a checker that detected them by keyword.
The reason recorded against it names the gap exactly:
an idea-level cliché is a matter of how an idea is treated,
not of whether certain words appear.
The registry was deleted along with the checker,
which is the part worth keeping in view:
the taxonomy was the durable half and it lived inside the disposable one.

The patterns returned.
`nikt nie`, driven down by hand-editing during the campaign,
stands in 211 of the 527 Polish notes.
The campaign's own reported counts do not reconcile —
three consecutive sessions record 94, then 82, then a reduction *from 49*
without the intervening step —
so the trajectory is documented and the endpoints are not.
Only the current rate was measured here.

## What this corpus cannot support

**It is one model family, one author and one subject.**
Phrase profiles are model-identifying,
which [fiction.md](fiction.md#what-this-means-for-olski) records,
so rates from a single writer describe that writer.

**It has no human Polish beside it.**
Every number above is one side of a comparison.

**And it is post-intervention,
which is the part that changes the assumption in
[linter.md](linter.md#the-thing-that-makes-or-breaks-it-calibration).**
The generated half of a paired corpus is easy to produce.
This one was not produced; it was found,
after its author had spent six sessions
editing against detectors for the same patterns a linter measures.
Its surface rates are a floor rather than a sample.
A corpus generated for calibration has to be generated and left alone,
and the distinction is invisible in the text itself.

## Not yet decided

- Whether a corpus edited against style detectors counts as the generated half.
  **Corpus sourcing** in
  [open-questions.md](open-questions.md#linter-questions) owns it.
- Whether the rule worth writing is
  the em dash, the negation frame, or the two in one rule.
  A human baseline decides it and nothing else can.

## Sources

- <https://github.com/SupraSummus/the-agent> —
  the repository measured, its git history, and the issues cited below
- <https://github.com/SupraSummus/the-agent/issues/457> —
  the cliché campaign, its method, and its self-reported counts
- <https://github.com/SupraSummus/the-agent/issues/530> —
  the decision to delete the detectors,
  and the design principle written down afterwards
- commit `8a3de57` in that repository —
  what was deleted, the reason recorded against each check,
  and the idea-level registry that went with them
- `book2/README.md` in that repository —
  the corpus's own account of what makes one of its notes weak
