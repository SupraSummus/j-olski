# Markdown in, prose out

The rules that measure a whole file
[decline on anything but plain text](rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives),
and the bodies
[milestone 1](roadmap.md#milestone-1-the-calibration-harness) calibrates against
include documentation and notes kept in Markdown.
So a step before the harness turns a corpus into files olski reads as prose:
`harness/markdown.py`, outside the `olski` package,
because milestone 0 keeps document formats out of the linter itself.

```sh
python3 -m harness.markdown korpus/ --into proza/
python3 -m olski proza/ --format report
```

An extraction is a transformation the rules then fire on,
so it owes an account of what it invents
exactly as a rule owes a false-positive rate.
That account is this document.

What makes it worth having is the two extractions written before this one.
Both deleted inline markup and left the space that stood in front of it,
which took `space-before-punctuation` over a body of notes
from 8 findings to 92,
and `double-space` over a memoir from none to 40.
A reader would have read either as the writer's typing.
Neither extraction is in this repository,
so those two figures are quoted from the runs that produced them
and are the last numbers here that cannot be redone.

## What it drops and what it keeps

Frontmatter, fenced code, headings, tables, HTML comments
and the list of links that closes a document go.
Inline markup is replaced by the text it wrapped rather than deleted,
list and blockquote markers are dropped and their text kept,
and the lines of a paragraph are joined with single spaces,
so a line of the result is a paragraph
and a rule about where a line ends
measures where the prose ends rather than where the author's editor wrapped.
`harness/markdown.py` is the truthful copy of all of that;
what follows is what the code cannot show.

## An inline construct leaves its text, or takes the space with it

The rule that keeps the extraction out of the rules' way
is that a construct leaves behind the characters it wrapped.
A link leaves its text and emphasis leaves what it emphasized,
so there is no hole for the space in front of it to fall into.
The constructs that have no text to leave —
an image with no description, an HTML comment —
take that whitespace along instead.

What that buys is measurable.
Three corpora were run twice each,
once over the extracted prose
and once over the files as they stand with their names changed to `.txt`,
which is how you assert a guarantee olski cannot check for itself.
Each cell below is the findings over the prose against the findings over the file:

| | notes | memoir | KSeF |
| --- | --- | --- | --- |
| `double-space` | 0 / 0 | 0 / 0 | 4 / 456 |
| `missing-space-after-full-stop` | 0 / 0 | 0 / 0 | 156 / 748 |
| `missing-space-after-punctuation` | 23 / 309 | 34 / 34 | 10 / 76 |
| `orphan-single-letter-word` | 23 / 32 | 2 / 24 | 4 / 12 |
| `quote-straight` | 1,649 / 1,772 | 481 / 481 | 312 / 978 |
| `space-before-punctuation` | 1 / 9 | 2 / 2 | 4 / 45 |
| `trailing-space` | 0 / 0 | 0 / 0 | 0 / 426 |

No rule reports more over the prose than over the file it came from.
The notes and the memoir are the two bodies
[generated-polish.md](generated-polish.md#what-was-measured) reports on,
and KSeF is the first repository in
[the audit corpus](audit-corpus.md#the-list).
Its file column is [the pilot run](firing-rates.md#the-rates) rerun,
and it differs from that run in one place:
naming the files `.txt` is what lets `orphan-single-letter-word` measure them
rather than decline.

Counting the same is not the same as pointing at the same place,
so the 234 findings of the spacing rules — the ones a deletion invents —
were checked one by one against the source they came from:
for every one of them, the five characters around the mark
stand in the Markdown file as well,
once the markup characters are taken out
and a line break is read as the space it renders as.

That is a measurement rather than a guarantee.
Joining two lines puts a mark next to a word it did not stand next to,
so an extraction of this shape *can* invent a finding,
and on these three corpora it did not.

## What the reader sees is not always Polish

A code span and a link both leave their text behind,
and in documentation that text is often an identifier or a path.
`nazwa.Pola` inside backticks reaches the rules
as a full stop with no space after it,
and so does a source file used as a link's visible text.

Over KSeF that shows up in one rule.
[The audit of the same files as they stand](firing-rates.md#two-rules-pointed-at-real-defects)
reads all 748 of `missing-space-after-full-stop`'s hits
and finds one defect among them, the rest code and links.
The extraction removes 592 of the 748,
which is the fenced code and every link target.
Of the 156 left, 8 stand inside a code span,
147 are a source path standing as the text of a link to the file it names —
142 of them the same path,
`KSeF.Client.Tests.Core\E2E\Invoice\InvoiceE2ETests.cs` —
and the last is the defect the audit found.
The same keeping accounts for 34 of the 312 straight quotation marks
and for 1,888 words, one in thirteen of what a rate there is divided by.

Deleting the spans instead was tried and is worse.
It leaves the punctuation that separated them touching:
`(enum: A, B, C)` written with each value in a code span
extracts to `(enum:,,,)`,
which took `missing-space-after-punctuation` over KSeF from 10 findings to 102
and put nine tenths of that rule's hits inside a parenthesis
where a reader can no longer see what stood there.
A hit a reader dismisses at a glance is the cheaper of the two,
and 147 hits on the text of a link are a document to correct
rather than a rate to discount.

## After joining, a line-end rule measures a different line

Two rules read where a line ends,
and both of them measure something else once a paragraph is one line.

`trailing-space` cannot fire at all:
joining strips the whitespace at every line end it consumes.
Over KSeF that is 426 findings the extraction removes,
and none of them is recoverable from the prose,
so a corpus is audited for trailing whitespace over its files
or not at all.

`orphan-single-letter-word` starts measuring the right thing instead.
Over the notes as they stand it reports 32 findings,
every one of them a letter that stands mid-line for every reader,
because a single newline in Markdown is a space.
Over the prose it reports 23,
each at the end of a paragraph,
and reading them gives the rule's own false-positive class
rather than the format's:
a designator (*sekcja A*), a unit (*10¹⁸ W*),
an abbreviation (*z XXI w.*), and the label *Q&A:*.
Those are the classes
[the audit over published Polish](firing-rates.md#orphan-single-letter-word-fired-124-times-and-found-nothing)
reads out of the rule as well.
That is the number a calibration can use.

## What it does not recognize

Four things reach the prose that a renderer would not have shown,
and each is worth revisiting when a corpus that leans on it arrives:

- **A table written without leading pipes.**
  A row is recognized by the `|` that opens it.
- **An indented code block.**
  Only fenced code is dropped.
- **A raw HTML block.**
  Comments go; a `<details>` or a `<br>` stays as the characters it is written with.
- **A link list something interrupts.**
  The trailing list goes only while every item opens with a link,
  so a note whose index has a reviewer's aside or a question in the middle of it
  keeps the entries standing above the interruption.
  16 of the notes are written that way.

A label above a link list — a line reading *Powiązane:* — survives the same way,
since it is a paragraph rather than an item of the list,
and arrives as a one-word paragraph of prose.

## Which documents enter the corpus

Selecting them is the same step's business,
because a rate over Polish must not have another language in its denominator.
`--polish SHARE` leaves out a document
whose words carry a Polish diacritic less often than the share given.
The two populations separate rather than shade into each other:
of the 567 notes, the 40 written in English top out at 2.8%
and the lowest of the remaining 527 sits at 13.1%,
so any threshold between the two picks the same documents.
Words are counted as olski counts them,
so the share and the rates it selects for are measured over the same tokens.

## What the numbers here were run over

```sh
git clone --depth 1 https://github.com/SupraSummus/the-agent

python3 -m harness.markdown the-agent/book2/notes --into proza/notes --polish 0.05
python3 -m harness.markdown ksef-docs --into proza/ksef

python3 -m olski proza/notes --format report
```

`ksef-docs` arrives by the command
[audit-corpus.md](audit-corpus.md#the-list) prints,
which pins it at the commit the KSeF column above was measured at.

The memoir is the nine chapters of `the-agent/book`:
`prolog.md`, `epilog.md` and `rozdzial-01` through `rozdzial-07`.
The comparison column is the same corpus with `.md` renamed to `.txt`,
and a count of a mark no rule reports a rate for —
the dashes, the Polish quotation marks — comes from
`--packs harness/counts.py`, which counts rather than judges.

Markdown is the only format this reads,
and the corpora that come in others still reach their figures by hand:
[corpora.md](corpora.md#how-the-counts-here-were-taken)
says which of them that is,
and [TODO.md](../TODO.md) holds what to do about it.
