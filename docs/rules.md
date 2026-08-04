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

## Check kinds

A check is the machinery; a rule is the decision to use it.
Adding a rule is a declaration.
Adding a check kind is code, in `olski/checks.py`,
and is meant to be the rarer event.

| Check | Fires on | Reports |
| --- | --- | --- |
| `pattern` | Each match of a regular expression | `{match}` |
| `pattern-density` | A unit where matches exceed a rate per 1000 words | `{count}`, `{words}`, `{rate}`, `{limit}`, `{match}` |
| `line-end-word` | A listed word left at the end of a line | `{word}` |

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
    unit="document",        # or "paragraph"
    max_per_1000_words=10,
    min_count=3,
    min_words=150,
)
```

`min_count` and `min_words` are floors, and they are not optional in spirit.
A rate computed over a short unit is noise:
one dash in nine words is 111 per 1000 and means nothing.
Below `min_words` the rule abstains and says so.
Below `min_count` it simply does not match,
which is a different thing.

### `line-end-word`

```python
params=dict(words=["a", "i", "o", "u", "w", "z"], case_sensitive=False)
```

Only meaningful where a line break in the source
is a line break in the output.
On a document whose breaks are soft the rule abstains,
because a source line says nothing about a rendered line
and guessing would flag correct text.

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
