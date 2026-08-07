# Writing rules

The engine holds no rules.
Rules live in packs,
packs are Python modules that declare data,
and adding one does not touch the engine.

This document is the reference for that format.
For what the rules are *for*, see [linter.md](linter.md);
for the order things get built in, see [roadmap.md](roadmap.md).

## What exists

Milestone 0.
The engine, the typography pack, and the command line tool are in `olski/`.

These rules are the character-level half of the project.
Anything whose judgement depends on what a word *is* —
a gerund against a noun, a subject against an object —
belongs to the grammar in [subset.md](subset.md),
because a pattern cannot tell those apart
and a rule that guesses is worse than no rule.

Input is plain Polish text, and only that.
Markup formats are out of scope:
this is a linter for Polish,
and reading a document format is a different job
that belongs to whatever produced the document.
What happens when a file arrives in one anyway
is [a question of what each check needs](#a-check-may-be-asking-more-of-a-document-than-its-format-gives).

## A rule

```python
from olski.rules import Pack

pack = Pack(name="typography", registers=("technical",))

pack.rule(
    id="quote-straight",
    check="pattern",
    params=dict(pattern=r'"'),
    message="Straight quotation mark; Polish takes „ opening and ” closing.",
    justification="""
    Polish typography uses „ for the opening quotation mark
    and ” for the closing one.
    A straight ASCII quote is a keyboard artifact rather than a Polish mark.
    """,
    sources=("docs/linter.md#typography-tier-a",),
)
```

| Field | Required | What it is |
| --- | --- | --- |
| `id` | yes | Stable identifier, used to select and to suppress the rule |
| `check` | yes | Name of a check kind, from the table below |
| `message` | yes | What the reader is told, as a format template, [in Polish](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie) |
| `justification` | yes | Why the rule exists, in prose |
| `params` | per check | Parameters for the named check |
| `sources` | no | Where the justification comes from |
| `pack` | from pack | Which pack the rule belongs to |
| `registers` | from pack | Which registers it is defensible in |
| `tier` | from pack | How deep an analysis it needs, `A` to `D` |
| `severity` | from pack | `note`, `warning` or `error` |
| `calibration` | from pack | What is known about its discrimination |

Anything a rule does not set is taken from its pack,
so a pack states the register once
and only the rules that differ say so.

Prose fields are folded before use,
so a `justification` may be written
with [semantic line breaks](https://sembr.org) like the rest of the repository.

A declaration is validated when its module is imported.
An unknown check, an unknown parameter, a broken pattern,
a message placeholder the check does not report:
each fails immediately, naming the rule.

### Two fields that are not decoration

**`justification`** is required because a rule without one
is a stylistic prejudice that happens to be executable.
Anchor it to a Polish style norm where one exists.
A rule justified by *this is what models do* dates;
a rule justified by *this is bad Polish style* does not.

**`calibration`** records what has been measured, as data rather than as prose.
Every rule ships `UNCALIBRATED`,
which is honest and also the reason
the thresholds in the typography pack are lenient:
a threshold with no number behind it is an opinion with a decimal point.

The milestone 1 harness replaces that with one of two shapes.
[What a rate on human Polish means](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
owns the argument:
a rule pointing at a site owes its hits, read,
while a rule comparing a measurement to a threshold
owes the human distribution that threshold has to sit outside.
Which of the two a check is doing is the check's own business,
so the shape is the check's to call for rather than the rule's to choose,
and a rule carrying the other one is refused when its pack is imported.

A rule whose hits were read carries how many there were
and how many of them were real defects:

```python
from olski.rules import Audit

calibration=Audit(
    hits=83,
    defects=79,
    corpus="drafts, characters as typed",
    taken="2026-08-07",
)
```

A rule with a threshold carries where edited Polish sits
on the statistic it measures, `median`,
and the share of that prose its threshold fires on, `accused`,
over however many scopes the distribution was taken across:

```python
from olski.rules import Distribution

calibration=Distribution(
    median=2.1,
    accused=0.03,
    scopes=812,
    corpus="expository NKJP",
    taken="2026-08-07",
)
```

`corpus` names prose somebody else can fetch and `taken` the date it was measured,
because what a number can mean is decided by the body of text it came from.
The threshold itself stays in `params`,
so moving a threshold moves one number and not two.

Both shapes answer the first of
[the two questions milestone 1 asks](roadmap.md#two-numbers-and-the-two-questions-behind-them),
whether the rule can be trusted.
Whether it has anything to do is [the report](#a-firing-rate-per-rule)'s number,
which a run recomputes over whatever corpus it is pointed at,
and what a declaration records is what no run reproduces:
hits a person read, and a distribution over a corpus that may not be at hand.

## A rule may be asking about the corpus

Every check sees all the files a run covers, not one file at a time.
One file is a corpus of one,
so a rule about a quotation mark is unaffected
and is written as though the corpus did not exist.

The scope exists because some defects are not properties of any one file.
A phrase is a tic because it recurs,
and an ending is a formula because the other endings are the same.
Each instance is a legitimate choice on its own,
and no per-file view can tell a choice from a habit,
because the evidence is in the files it is not looking at.

**A corpus rule reports one finding, anchored at one example.**
It does not raise the measurement against every site that fed it.
A rate is a property of the body of text and not of any sentence in it,
so a list of every site would be an invitation
to edit the sites until the number moves,
which leaves the prose worse and the measurement meaningless.
That is not a hypothetical:
[generated-polish.md](generated-polish.md#what-happened-when-the-rules-were-deleted)
records a body of prose edited into its detectors' image,
and the detectors deleted afterwards rather than before.
The anchor is there so the number can be checked.

A share measured over five introductions is not a share,
so a corpus rule that cannot see enough text
declines to answer and says why rather than report one.
Such an [abstention](#abstention-is-not-silence) belongs to no file,
since no file owns the answer.

## A check may be asking more of a document than its format gives

Plain text carries two guarantees at once:
every character in it is prose,
and every newline in it is a newline on the page.
A markup format carries neither.
Its frontmatter, headings, tables and link lists — its apparatus —
are text like any other,
and a single newline in it is whitespace the renderer collapses.

Which guarantee a check needs follows from how much of a document it looks at.
A check pointing at a site is answerable on a file of any format,
because the reader can look at the site and judge it:
a straight quotation mark inside a code span
is one a reader dismisses at a glance,
and a rate over the wrong denominator is not something anyone can dismiss.
A check measuring a whole scope is measuring the apparatus along with the prose,
and a check reading a line end is reading where the file wraps
rather than where the page does.
Those two decline, and name the file they declined on.

So `olski notatka.md` reports the quotation marks and the spacing
and abstains on the rates.
Refusing the file outright would throw away the half that is correct,
and measuring it anyway is the failure this is written against:
[generated-polish.md](generated-polish.md#the-apparatus-biases-a-rate-by-an-amount-the-corpus-decides)
measures one rule running a quarter high over one body of Markdown
and true over another by the same writer,
so the error cannot be discounted in general.

Separating prose from apparatus is a job for whatever reads the format,
which is where [milestone 0](roadmap.md#milestone-0-rule-engine-and-the-typography-pack)
puts it,
and [extraction.md](extraction.md) is the step that does it for Markdown.
What belongs to olski is knowing the job has not been done.
A file's suffix is the whole of the evidence available about its characters,
and one olski does not recognize is read as text it cannot vouch for.

Recognizing a suffix is weaker evidence than it reads as,
because a guarantee belongs to a format and a suffix is not one.
[firing-rates.md](firing-rates.md#what-the-hits-over-published-polish-turned-out-to-be)
measures both guarantees failing across a corpus of `.txt`:
a table laid out with runs of spaces and emphasis written as `*`
are apparatus in a file that answered for prose,
and a paragraph set on one line however long it runs
puts a newline where the page has a paragraph break rather than a line end.

The two are not evidenced alike, so they are not asked for alike.
Whether a character is prose or apparatus is a question about a format,
and a suffix is the only thing that answers it at all.
Whether a newline is a line break is a question about the text,
and the text answers it:
a document that broke its own lines has paragraphs running past one,
where an export has a paragraph to a line.
So the second guarantee is measured rather than taken on the suffix's word,
and `Document.hard_wrapped` is what a check asks for it with.
That audit is the price of having asked the suffix instead,
and every finding in it stood in a file
whose own lines said it was not laid out in them.

## Check kinds

A check is the machinery; a rule is the decision to use it.
Adding a rule is a declaration.
Adding a check kind is code, in `olski/checks.py`,
and is meant to be the rarer event.

| Check | Fires on | Reports |
| --- | --- | --- |
| `pattern` | Each match of a regular expression | `{match}` |
| `pattern-density` | A scope whose matches per 1000 words run over a rate, or under one | `{count}`, `{words}`, `{rate}`, `{limit}`, `{side}`, and `{match}` where the rule set a ceiling |
| `length-variation` | A document whose units are too alike in length, or too unlike | `{unit}`, `{count}`, `{words}`, `{mean}`, `{sd}`, `{variation}`, `{limit}`, `{side}` |
| `line-end-word` | A listed word left at the end of a line | `{word}` |
| `entity-recurrence` | A corpus that introduces entities and drops them | `{entity}`, `{mentions}`, `{walk_ons}`, `{introductions}`, `{share}`, `{limit}` |

A message may only use the placeholders its check reports.
Using another one is an error at import time, not a surprise at runtime.
What a check reports is read off the rule's parameters,
which is why the `pattern-density` row carries a condition:
a rule that set no ceiling can only ever report a reading below its floor,
and such a reading has no occurrence to quote,
so `{match}` there is refused rather than left to render an empty string.

### `pattern`

```python
params=dict(
    pattern=r"(?<=[ \t])[,.;:!?…]",
    unless_followed_by=r"\w",
    flags=["ignorecase"],
)
```

`unless_preceded_by` and `unless_followed_by` are how precision is bought back.
Either one matching the context around a match
means the match is a legitimate use and the rule stays quiet.
`unless_preceded_by` is anchored to the match,
so a pattern that matches earlier in the text does not exempt anything.

Each exemption is a deliberate miss.
That is the trade the project has chosen:
a missed defect costs nothing,
and a false accusation against correct Polish
costs the reader's trust in every other rule.

### `pattern-density`

```python
params=dict(
    pattern=r"[—–]",
    unit="document",        # or "sentence", "paragraph", "corpus"
    max_per_1000_words=10,  # or min_per_1000_words, or both
    min_count=3,
    min_words=150,
)
```

`min_per_1000_words` and `max_per_1000_words` are a floor and a ceiling,
and a rule sets either or both, but not neither.
A ceiling reports a text that overuses something,
which is what the em dash rule is for.
A floor reports one that underuses it,
which is what fact density on
[the candidate inventory](linter.md#candidate-rule-inventory) needs:
what the source there reports of generated text
is too few dates, numerals and proper nouns rather than too many.
`{side}` says which of the two fired,
because a number alone leaves a message unable to tell a writer
whether the text ran hot or cold.

`min_count` and `min_words` bound the evidence rather than the rate,
and falling under either one is the rule declining rather than the rule finding nothing.
`min_words` is the denominator:
a rate over a short scope is noise,
since one dash in nine words is 111 per 1000 and means nothing.
It is tested before the bounds,
so a scope under it abstains whatever that scope turned out to hold,
and the scopes the rule could never have judged
come off the denominator [the report](#a-firing-rate-per-rule) divides by.

`min_count` is the evidence a reading above the ceiling needs,
and it does not stand under the floor,
where too few matches is the finding rather than a reason to doubt one.
Running it against both sides would skip
what a floor rule is looking hardest for:
the document with no numerals in it at all.
So it is tested where the side is known,
and there the rule abstains as it does under the word floor.

Both abstentions name the floor they refused on rather than what the scope held,
because the floor is the number a writer can act on,
and because a reason carrying a per-scope measurement is a distinct reason per scope,
which turns `--show-abstentions` from a count of causes into a line per file.

A finding above the ceiling points at the first occurrence in the scope,
so that the number can be checked against the text.
One below the floor has no occurrence to point at —
what it found is the text that went by without one —
so it points at the scope it measured, and `{match}` is empty.
A rule that set no ceiling has no other kind of finding to make,
which is why `{match}` is not among the placeholders it may use at all.

`unit="corpus"` pools every file the run covers into one rate.
See [what a corpus scope is for](#a-rule-may-be-asking-about-the-corpus).

`unit="sentence"` is the narrowest scope
and the only one that is inferred rather than read off the text.
A blank line is a paragraph boundary and a file is a file,
while a full stop in Polish is a sentence boundary only sometimes:
`m.in.`, `w 2011 r.`, `art. 6`, `12. dzień` and a bare `zabytek.pl`
all put one in the middle of a sentence.
`olski/document.py` owns the abbreviation list that settles it,
and with it the choice of which way to be wrong:
an abbreviation that does close a sentence merges it with the next,
so the splitter loses a boundary rather than inventing one.
A rate measured per sentence carries that error,
which is worth knowing before a rule reports a number it did not compute alone.

### `length-variation`

```python
params=dict(
    unit="sentence",        # or "paragraph"
    min_variation=0.35,
    min_units=8,
)
```

Uniformity is what this check is for.
Sentence length varying less than in human prose
is among the most robust of the documented differences,
which [what the research says](linter.md#what-the-research-says) owns,
and it is a property of the document and of no sentence in it,
so the finding is anchored at the whole document.
Anchoring it at a sentence would invite editing that sentence
until the number moved,
which is the failure
[a corpus rule avoids the same way](#a-rule-may-be-asking-about-the-corpus).

The statistic is the coefficient of variation:
the standard deviation of the units' word counts, over their mean.
Dividing by the mean is what lets one threshold serve every document,
since a spread of four words means one thing among nine-word sentences
and another among thirty-word ones.

`min_variation` and `max_variation` are the floor and ceiling pair
that [`pattern-density`](#pattern-density) describes,
set here over a spread rather than over a rate,
and `{side}` names which of the two fired.
A measurement's defective side belongs to the pack rather than to the check,
which is what buys one engine for two registers:
see [the fiction section of linter.md](linter.md#what-is-nevertheless-lintable-in-fiction),
and note that which side a *technical* pack sets
is one of the open questions it points at.

`min_units` is the same kind of floor as `min_words` above,
and it is the one that matters here:
three sentences have a standard deviation and not a distribution.
Below it the rule abstains.

No rule in this repository declares this check.
The numbers above illustrate the format,
and a threshold that means anything comes from
[milestone 3](roadmap.md#milestone-3-statistical-rules)
and the corpus behind it.

### `line-end-word`

```python
params=dict(words=["a", "i", "o", "u", "w", "z"])
```

Only meaningful where a line break in the source
is a line break in the output,
which takes a format olski reads
and a document that used its newlines to break lines:
[the two are asked for separately](#a-check-may-be-asking-more-of-a-document-than-its-format-gives),
and failing either one the rule abstains,
because a source line says nothing about a rendered line
and guessing would flag correct text.

Words are matched as written rather than folded,
so a list carries the forms it means.
The fold is what read `Tom I` as a conjunction,
and [firing-rates.md](firing-rates.md#orphan-single-letter-word-reads-one-stratum-of-the-three)
holds what it cost and what leaving it out costs in return.

### `entity-recurrence`

```python
params=dict(
    introduce=r"\b([A-ZĄĆĘŁŃÓŚŹŻ]\w+) \([^)]*\d[^)]*\)",
    min_mentions=3,
    min_introductions=50,
    max_walk_on_share=0.25,
)
```

`introduce` matches the place a text sets an entity up with apparatus —
a name with a parenthesis after it, a term with its expansion —
and captures the entity's name in its one group.
An entity named fewer than `min_mentions` times
in the file that introduced it is a walk-on,
the introduction counted among the mentions,
and the finding is the share of walk-ons across the corpus.

A single walk-on is not a defect.
Plenty of things are named once because once is what they are worth,
which is why this reports a share and not a site,
and why no shipped pack declares a rule against it:
the share that separates a text from a habit
is exactly what [milestone 1](roadmap.md#milestone-1-the-calibration-harness) is for.
The check exists because the measurement has to come first.

## Abstention is not silence

Three different things look like nothing happening,
and the engine keeps them apart:

- **No match.** The normal case. Not a decision, and not reported.
- **Abstention.** The rule could have fired and declined,
  because it cannot tell a defect from a legitimate choice here.
  Reported by `--show-abstentions`, with the reason.
- **No coverage.** A rule that cannot analyze this input at all.
  Does not arise yet, because every check here is tier A
  and a regular expression reaches all of its input.
  It arrives with morphology and with parsing,
  and when it does it needs reporting,
  because silence from lack of coverage
  reads exactly like a clean document.

That distinction comes from
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure),
where deliberate abstention cost 2 rows in 1000
and lack of coverage cost 202.

The middle case is stated as *could have fired* and is sometimes weaker.
A rule declining because a file's format is one olski does not read
has counted nothing,
so it does not know whether there was anything to count.
A rate rule under one of [its floors](#pattern-density) has counted,
and found either the scope too short to divide by
or the count too small to stand behind.
Neither of the two could have fired,
and what each reports is that it did not measure.
That is the honest claim,
and it is the useful one,
because the alternative is a number nobody can tell from a measurement.

## A firing rate per rule

`olski --format report` prints one row per rule
instead of one line per finding:
how often the rule fired, how often it abstained,
how much text it measured,
and what the firing comes to over that much.
Every selected rule gets a row, the ones that never fired included,
since whether a rule has anything to do
is half of what the rate is being asked.

**The denominator is what a check can fire at most once per.**
A check reporting on a whole scope raises one finding about it,
so its findings are counted against the scopes it was given
and reported as a share of them;
a rule against a word left at a line end is counted in lines the same way.
A check with no such bound is counted against the quantity of prose instead,
since a pattern can match twenty times in a paragraph,
and reported per thousand words.
Which of the two a check is, and in what unit,
is the check's own business and `olski/checks.py` owns it.

**What a rule declined comes off the denominator.**
[Abstention is not silence](#abstention-is-not-silence),
and it is not a firing rate of zero either:
a rule that declined on every file measured nothing,
so it reports no rate at all rather than a rate of zero,
which would say it had looked.
The abstentions have a column of their own beside the findings,
so a rule that stayed quiet can be told from one that never looked.

**A scope a rule could not have judged is a scope it declined.**
A rate rule under [either of its floors](#pattern-density) has refused to answer,
so it abstains and the scope leaves the denominator with every other refusal.
The alternative is to pass over such a scope in silence
and have the report take it out afterwards,
by asking each check which of the scopes it was handed it could reach:
a second protocol beside the one that reports outcomes,
and one that leaves `--show-abstentions` nothing to print,
where the reason is what tells a reader
that a corpus was the wrong shape for the rule
rather than that the rule looked and found nothing.
[firing-rates.md](firing-rates.md#what-the-report-mode-did-when-rules-declined)
is the choice measured:
one stratum's denominator falls from 295 documents
to the 8 the rule was in a position to report on.

**The report is one side of a pair.**
A firing rate says whether a rule has anything to do.
Whether it can be trusted is the other number
[milestone 1](roadmap.md#milestone-1-the-calibration-harness) asks for,
and ranking rules by what they discriminate
needs a human half to compare against,
which no run over one body of text can supply.

## A project's own pack

Any importable module or `.py` file that declares a module-level `pack` works:

```sh
olski text.txt --packs mypack.py
```

That replaces the shipped packs rather than adding to them.
Pass the shipped pack too if you want both:

```sh
olski text.txt --packs olski.packs.typography --packs mypack.py
```

## Why Python and not YAML

The configuration is already a program's data structure.
Writing it in Python means
a declaration is validated the moment its module is imported,
the error names the rule and the file,
patterns are ordinary raw strings
rather than strings inside a quoting convention inside a schema,
and there is no second language to learn or to validate against.

The cost is that a pack is executable,
which is the same bargain a test configuration or a build file makes.
The rules stay declarative by convention:
a pack declares data and calls nothing but `pack.rule`.

## Not yet decided

- **Suppression.** No way yet to silence a rule on one line or one file.
- **Delivery route.** Whether this stays a standalone tool,
  becomes a Vale style, or becomes LanguageTool XML.
  See [open-questions.md](open-questions.md).
