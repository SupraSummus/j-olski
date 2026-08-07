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
| `message` | yes | What the reader is told, as a format template |
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

**`calibration`** records what has been measured.
Every rule shipped so far reads `uncalibrated`,
which is honest and also the reason
the thresholds in the typography pack are lenient.
Milestone 1 replaces that string with two numbers.
Until then a threshold is an opinion with a decimal point.

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
puts it.
What belongs to olski is knowing the job has not been done.
A file's suffix is the whole of the evidence available,
and one olski does not recognize is read as text it cannot vouch for.

## Check kinds

A check is the machinery; a rule is the decision to use it.
Adding a rule is a declaration.
Adding a check kind is code, in `olski/checks.py`,
and is meant to be the rarer event.

| Check | Fires on | Reports |
| --- | --- | --- |
| `pattern` | Each match of a regular expression | `{match}` |
| `pattern-density` | A scope whose matches per 1000 words run over a rate, or under one | `{count}`, `{words}`, `{rate}`, `{limit}`, `{side}`, `{match}` |
| `length-variation` | A document whose units are too alike in length, or too unlike | `{unit}`, `{count}`, `{words}`, `{mean}`, `{sd}`, `{variation}`, `{limit}`, `{side}` |
| `line-end-word` | A listed word left at the end of a line | `{word}` |
| `entity-recurrence` | A corpus that introduces entities and drops them | `{entity}`, `{mentions}`, `{walk_ons}`, `{introductions}`, `{share}`, `{limit}` |

A message may only use the placeholders its check reports.
Using another one is an error at import time, not a surprise at runtime.

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

`min_count` and `min_words` bound the evidence rather than the rate.
`min_words` is the denominator:
a rate over a short scope is noise,
since one dash in nine words is 111 per 1000 and means nothing,
so below it the rule abstains and says so.
It abstains where it would otherwise have reported and nowhere else,
because a scope a rule had nothing to say about
is not a scope it declined to judge.

`min_count` is the evidence a reading above the ceiling needs,
and it does not stand under the floor,
where too few matches is the finding rather than a reason to doubt one.
Running it against both sides would skip
what a floor rule is looking hardest for:
the document with no numerals in it at all.

A finding above the ceiling points at the first occurrence in the scope,
so that the number can be checked against the text.
One below the floor has no occurrence to point at —
what it found is the text that went by without one —
so it points at the scope it measured, and `{match}` is empty.

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
`{side}` says which of the two fired,
because a number alone leaves a message unable to tell a writer
whether the text ran hot or cold.

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
params=dict(words=["a", "i", "o", "u", "w", "z"], case_sensitive=False)
```

Only meaningful where a line break in the source
is a line break in the output,
which is one of the two things
[plain text guarantees and a markup format does not](#a-check-may-be-asking-more-of-a-document-than-its-format-gives).
Elsewhere the rule abstains,
because a source line says nothing about a rendered line
and guessing would flag correct text.

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
is exactly what [milestone 1](roadmap.md#milestone-1-the-calibration-harness)
is for, and a threshold chosen before then
is an opinion with a decimal point.
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
so it does not know whether there was anything to count;
what it reports is that it did not measure.
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
so how much of a rule's silence was a decision stays visible.

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

- **Message language.** Messages are English while the documentation is.
  A linter for Polish authors should probably speak Polish,
  and that is a localization decision, not a rule decision.
- **Suppression.** No way yet to silence a rule on one line or one file.
- **Delivery route.** Whether this stays a standalone tool,
  becomes a Vale style, or becomes LanguageTool XML.
  See [open-questions.md](open-questions.md).
