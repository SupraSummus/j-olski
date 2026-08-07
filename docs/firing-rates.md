# What the typography pack fires on

The typography pack sets its thresholds and its exemptions by judgement,
and the prose in its test suite is written to exercise the machinery.
This document is what the nine rules do when handed Polish somebody wrote:
how often each fired, over how much text,
what its hits turned out to be when they were read,
and what none of it can mean.

The text is two bodies, at the two ends of
[the argument corpora.md settles](corpora.md#what-the-survey-settles).
One is literary and expository prose from Wolne Lektury,
which reached its reader through an editor, a typesetter and a corpus build.
The other is the Polish documentation of a state IT system,
cloned from version control, which has reached nobody.
The rule against the straight ASCII quotation mark reads the difference:
`quote-straight` fires nought times in 1,940,517 words of the first
and 332 times in the running prose of the second.

That pair of numbers is
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)'s
argument measured instead of asserted.
The remaining eight rules fall out four ways.
One finds nothing anywhere, for the same reason.
Four fire, and reading their hits shows them measuring the apparatus
around the Polish rather than the Polish.
Two point at real defects, and one of those two,
handed the Markdown corpus instead, fires 748 times for a single defect.
The eighth is the pack's only rate rule,
and it comes out of this with a distribution.

## Fetching the two corpora

Nothing is vendored and no code here downloads it,
for the reasons [corpus.md](corpus.md#fetching-it) gives about Składnica.
Both fetches were taken on 2026-08-07.

### Wolne Lektury

Three strata, because a rule is scoped to a register
and one stratum cannot show what a register does to a rate.
`proza` is narrative prose and `wyklad` is essays and treatises.
`wiersze` is Kochanowski's *Fraszki*, one file per fraszka,
and it earns its place twice over.
Its documents are the only ones short enough to reach a rate rule's floor.
And the export sets a prose paragraph on a single line however long it runs —
1,346 characters for the longest in the first volume of *Lalka* —
so a verse line is the only line break in the corpus
that falls where a line ends on a page.

```sh
PROZA='lalka-tom-pierwszy lalka-tom-drugi faraon-tom-pierwszy faraon-tom-drugi
faraon-tom-trzeci nad-niemnem-tom-pierwszy nad-niemnem-tom-drugi
nad-niemnem-tom-trzeci chlopi-czesc-pierwsza-jesien popioly-tom-pierwszy
quo-vadis'

WYKLAD='sklodowska-badanie-cial-radioaktywnych gliscinski-dyskursy-prawa-autorskiego
o-filozofii-sredniowiecznej legenda-mlodej-polski mitologia-slowianska
bruckner-starozytna-litwa krzewiciele-zdziczenia patryotyzm-i-kosmopolityzm
o-wplywie-nauki-na-rozwoj-milosierdzia kilka-slow-o-kobietach
walewska-kobieta-polska-w-nauce wyka-modernizm-polski wyka-rzecz-wyobrazni
prawidla-zycia obrachunki-fredrowskie pieklo-kobiet
uwagi-z-powodu-listu-polaka-do-ministra-rosyjskiego zulawski-miasta-umarle
o-literaturze-rosyjskiej-i-naszym-do-niej-stosunku-dzis-i-lat-temu-trzysta
elegie-i-inne-pisma-literackie-i-spoleczne'

WIERSZE=$(curl -fsS 'https://wolnelektury.pl/api/authors/jan-kochanowski/books/' |
  python3 -c 'import json,sys
for b in json.load(sys.stdin):
    if b["slug"].startswith("fraszki-ksiegi-") and b["slug"].count("-") > 2:
        print(b["slug"])')

get() {
  mkdir -p "polszczyzna/$1"
  for slug in $2; do
    curl -fsS -o "polszczyzna/$1/$slug.txt" \
      "https://wolnelektury.pl/media/book/txt/$slug.txt"
  done
}

get proza "$PROZA"
get wyklad "$WYKLAD"
get wiersze "$WIERSZE"
```

That is 11, 20 and 295 files by 17 authors.
Where a file states the edition it was made from, the edition is dated 1873 to 1988;
one of the twenty expository texts,
Gliściński on the discourses of copyright,
is a contemporary academic monograph the catalogue files under `Współczesność`.

Every file ends with the library's licence and provenance notice,
about two hundred words of it,
opened by a line holding five hyphens and nothing else.
Cutting there is the only thing done to the download,
and it deletes a suffix rather than rewriting anything:

```sh
python3 -c '
import pathlib, re
for f in pathlib.Path("polszczyzna").rglob("*.txt"):
    f.write_bytes(re.split(rb"(?m)^-----\r?$", f.read_bytes(), maxsplit=1)[0])'
```

The delimiter occurs exactly once in each of the 326 files,
so the cut is settled rather than guessed at,
and what it removes is worth a number rather than a shrug.
Write the second half of the same split to a second tree and lint that,
and the notices report 12 straight quotation marks,
12 runs of two or more spaces and 7 line-end orphans over 64,468 words,
which is what the trim keeps out of every number below.

The files are CRLF throughout, and no rule sees it,
because `Path.read_text` translates line endings before a document is built.
Anyone checking `trailing-space` against the raw bytes will find the report
disagreeing with a count of runs of spaces before a line end,
and the report is the one describing what olski was shown.

### Polish documentation in version control

The repository
[corpora.md](corpora.md#polish-technical-documentation-original-and-translated)
names as the first member of the audit corpus:

```sh
git clone --depth 1 https://github.com/CIRFMF/ksef-docs
```

32 Markdown files, 36,550 words as olski counts them over the files as they stand.
That is apparatus and prose together,
which is the point here and is why the figure
[corpora.md](corpora.md#polish-technical-documentation-original-and-translated)
gives for the same repository is a third smaller.

## What ran

```sh
python3 -m olski polszczyzna --format report --show-abstentions
python3 -m olski polszczyzna/proza --format report
python3 -m olski $(find ksef-docs -name '*.md' | sort) --format report --show-abstentions
```

The `find` is not decoration.
A directory walk collects `.txt` and `.text` and nothing else,
so `olski ksef-docs/` reaches one file —
`LICENSE.txt`, the MIT licence, in English, 169 words —
and prints a nine-row table over it without saying what it passed by.

## The rates

Over all 326 files of Wolne Lektury:

```text
326 files, 1940517 words, 9 rules

rule                             fired  abstained       measured          rate
double-space                       139          0  1940517 words  0.1 per 1000
em-dash-density                     21          4  322 documents          6.5%
missing-space-after-full-stop       11          0  1940517 words  0.0 per 1000
missing-space-after-punctuation     31          0  1940517 words  0.0 per 1000
orphan-single-letter-word          124          0   107280 lines          0.1%
quote-english                        0          0  1940517 words  0.0 per 1000
quote-straight                       0          0  1940517 words  0.0 per 1000
space-before-punctuation            67          0  1940517 words  0.0 per 1000
trailing-space                     110          0  1940517 words  0.1 per 1000
```

Over the 32 Markdown files of KSeF:

```text
32 files, 36550 words, 9 rules

rule                             fired  abstained     measured           rate
double-space                       456          0  36550 words  12.5 per 1000
em-dash-density                      0         32  0 documents              —
missing-space-after-full-stop      748          0  36550 words  20.5 per 1000
missing-space-after-punctuation     76          0  36550 words   2.1 per 1000
orphan-single-letter-word            0         32      0 lines              —
quote-english                        0          0  36550 words   0.0 per 1000
quote-straight                     978          0  36550 words  26.8 per 1000
space-before-punctuation            45          0  36550 words   1.2 per 1000
trailing-space                     426          0  36550 words  11.7 per 1000
```

Findings by stratum, so that a register can be told from a rule:

| rule | proza | wykład | wiersze | notices | KSeF |
| --- | --- | --- | --- | --- | --- |
| words | 912,377 | 1,011,472 | 16,668 | 64,468 | 36,550 |
| `double-space` | 0 | 139 | 0 | 12 | 456 |
| `em-dash-density` | 11 of 11 | 10 of 20 | 0 | 0 | declined |
| `missing-space-after-full-stop` | 3 | 8 | 0 | 1 | 748 |
| `missing-space-after-punctuation` | 0 | 31 | 0 | 0 | 76 |
| `orphan-single-letter-word` | 35 | 89 | 0 | 7 | declined |
| `quote-english` | 0 | 0 | 0 | 0 | 0 |
| `quote-straight` | 0 | 0 | 0 | 12 | 978 |
| `space-before-punctuation` | 10 | 57 | 0 | 0 | 45 |
| `trailing-space` | 0 | 110 | 0 | 2 | 426 |

## The quotation mark rules had nothing to find

`quote-straight` and `quote-english` fire nought times
in 1,940,517 words of published Polish.
The corpus is not quiet about quotation:
it carries 8,891 `„` and 8,845 `”`.
What it carries none of is the mark either rule looks for,
and the twelve exceptions in the whole download
sit in a notice the library appends rather than in anybody's Polish.

`quote-straight` over the KSeF documentation fires 978 times.
646 of those are inside fenced or inline code,
where a straight quotation mark is a straight quotation mark in JSON and correct.
The remaining 332 are around Polish phrases in running prose.
That 332 is the figure
[corpora.md](corpora.md#polish-technical-documentation-original-and-translated)
took by hand over the same repository,
which is worth saying because that document notes of all its counts
that the program which took them is not in this repository.
Here the program is `olski --format report`,
plus a split of code from prose that no code in this repository performs,
so the agreement checks the survey rather than closing the gap it names.

A rate of nought over 1.9 million words is not a false-positive rate near zero.
It is a corpus that could not have held what the rule looks for,
which is what
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
predicts of exactly these two rules.

## What the hits turned out to be

A rule whose answer depends on the site owes an audit rather than a rate.
All 482 site-anchored hits over Wolne Lektury were classified,
and each class read.

### `orphan-single-letter-word` fired 124 times and found nothing

Not one of the 124 is a one-letter word left at the end of a line,
because nothing that lays out a page broke a line in this corpus.

| hits | | what it is |
| --- | --- | --- |
| 70 | 56% | the Roman numeral `I`, in `Tom I`, `Rozdział I`, `Mieszko I` |
| 35 | 28% | a one-letter word ending a paragraph: `— A!… a!…`, `Jadłaś, Justynko, a?` |
| 11 | 9% | the `a` of an apostrophe genitive: `Locke'a`, `Farrère'a`, `Lafayette'a` |
| 5 | 4% | a line of verse quoted inside criticism, broken where the poet broke it |
| 3 | 2% | the abbreviation `w.` for *wiek* |

The largest class is a parameter meeting Polish:
`case_sensitive=False` folds `I` into the listed `i`,
and Polish numbers its chapters in Roman.
The second is the rule's premise failing rather than the rule misreading anything —
a word at the end of a paragraph has nothing after it to be separated from,
so there is no orphan whatever the measure of the line.
The third and fifth are a tokenizer question:
neither the `a` after an apostrophe nor the `w` of `w.` is a word.

The `wiersze` stratum is where the premise holds,
its 5,481 lines being lines a poet wrote as lines,
and there the rule fires nought times.
The rule found nothing wherever it could have been right
and 124 things wherever it could not.

### `double-space` and `trailing-space` measured two tables

All 139 `double-space` hits are in two of the 326 files,
and 96 of the 110 `trailing-space` hits are in the same two.
Both carry tables laid out with runs of spaces:
Skłodowska-Curie's measurements of the radioactivity of uranium compounds,
and Walewska's counts of women enrolled at Polish universities.

```text
Tlenek uranu czarny, U2O4,    2,6
Tlenek uranu zielony, U2O4    1,80
```

Neither rule is wrong about the characters in front of it.
Both are measuring a table rather than a sentence,
which is the failure
[rules.md](rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives)
attributes to markup formats,
happening inside a file whose format promised it would not.

### `missing-space-after-punctuation` mostly read an emphasis marker

22 of its 31 hits are a comma or a colon followed by `*`:

```text
*Adwokat dr Kazimierz Sterling,*
```

Wolne Lektury's text export marks emphasis with asterisks,
so a `.txt` file from it carries inline markup like any document format does.
Of the other 9, eight are the defect —
`Zważmy ,że`, `niezabudki;W łanach`, `tłumaczą:.` —
and the ninth is the ratio `stosunek e:m` in Skłodowska-Curie's thesis.

### Two rules pointed at real defects

`space-before-punctuation` fired 67 times.
15 of those are one line of `legenda-mlodej-polski.txt`,
a row of spaced full stops standing for an elision in a quoted poem,
which is one site rather than fifteen.
The remaining 52 are a stray space before a mark,
in prose where nothing else accounts for it:

```text
Zwycięzcami świata stać się mają lub niczym .
```

`missing-space-after-full-stop` fired 11 times and all 11 are the defect,
ten of them a sentence running straight into the next
and one an initial running into a surname, `Pan J. St.Mill`.

Over KSeF the same rule fires 748 times, and one of the 748 is the defect.
429 are inside a fenced or inline code span and 291 inside a link;
of the 28 a crude split leaves over, 27 are code the split missed,
and the odd one out is `części paczki.Po upływie`.
That is the rule's own false positive — a dotted identifier quoted bare —
arriving at a rate its justification does not anticipate,
because the justification assumes the linter is not shown the code spans
and this run showed it 32 files of them.
Showing it the prose instead leaves 156 of the 748,
and [extraction.md](extraction.md#what-the-reader-sees-is-not-always-polish)
reads those.

## `em-dash-density` has a distribution now

The threshold is 10 per 1000 words and was chosen to be lenient.
Per document, over the scopes long enough for the rule to believe its own number:

| stratum | documents | lowest | median | highest | over the threshold |
| --- | --- | --- | --- | --- | --- |
| proza | 11 | 20.2 | 43.1 | 52.0 | 11 |
| wykład | 20 | 1.8 | 10.0 | 18.8 | 10 |
| wiersze | 8 | 0.0 | 0.0 | 8.2 | 0 |

The narrative half sits entirely above the threshold
and its median at four times it,
because Polish opens a line of dialogue with a dash.
That is the reason [corpora.md](corpora.md#wolne-lektury) gives
for a literary corpus measuring dialogue punctuation on this statistic
rather than the construction the rule is aimed at,
and the pack agrees in advance:
`em-dash-density` is the one rule scoped to the `technical` register alone.

The expository half is the one worth looking at,
being the nearest register to the pack's target that could be fetched,
and its median falls on the threshold.
Ten of twenty edited Polish essays and treatises stand above a limit
set with no measurement behind it,
and the spread runs an order of magnitude, from 1.8 to 18.8.

A threshold does not come out of this,
for a reason [the last section](#what-these-numbers-are-not) holds
and for one that belongs here:
these authors published between 1873 and 1988,
so a dash rate among them is a period style as much as a register one.
What the run does establish is that the pack and the harness together
produce a distribution when they are handed prose,
and that this one is wide enough for the threshold's position in it to matter.

## What the report mode did when rules declined

Three of the report's decisions turn on what a rule declined,
and a corpus that makes rules decline is what shows whether they hold.

**Declines come off the denominator rather than folding into zero.**
Over KSeF both whole-file rules decline on all 32 files,
`measured` reads `0 documents` and `0 lines`,
and the rate column reads `—`.
That is the intended answer,
and it is a different answer from the `0.0%`
the same rule prints over the `wiersze` stratum.
The two remaining decisions are about how much that `0.0%` is worth.

**A rate rule is counted over the scopes it was given.**
The `wiersze` stratum shows what that denominator holds.
Of its 295 documents, 4 abstain and 291 are counted as measured,
and 8 of the 295 hold the 150 words the rule needs.
So 283 of the 291 are documents the rule could not have reported on
whatever they contained, and the row says nothing of it.
The share is honest about what the rule did
and silent about what it was in a position to do.

**Two floors mean the same thing and only one of them is recorded.**
`min_words` abstains and names the reason.
`min_count`, the evidence a reading above the ceiling needs, returns silently.
Across the corpus 21 documents were reported,
4 abstained on `min_words`,
and 34 stood above the ceiling and were turned away by `min_count` without a word.
So the abstention column accounts for 4 of the 38 scopes
that stood over the threshold and went unjudged,
and whether the other 34 are declining or simply not finding anything
is a question this run raises rather than settles.

The `orphan-single-letter-word` row shows a denominator going wrong the other way.
Its denominator of 107,280 lines is 101,799 lines of the prose strata,
where a line is a paragraph or the blank between two,
and 5,481 lines of verse.
Only the second kind is a line in the sense the rule means.
The unit is right about what the check can fire at most once per
and wrong about what the rule is asking.

## What these numbers are not

**They are not a calibration of any rule,
and no rule here should carry one because of this run.**
A hit count beside a defect count is the shape of an
[`Audit`](rules.md#two-fields-that-are-not-decoration),
and this document reports several: 124 hits and no defects, 11 hits and 11.
What an `Audit` also carries is the corpus,
and that field is where these pairs fail rather than in the counting.
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
asks a site-answering rule for the share of its hits that were real defects,
over prose caught at the stage the linter runs at.
Wolne Lektury is not that stage,
and the audit above says so through the composition of the hits
rather than through their number:
the one rule that came out of it clean, `missing-space-after-full-stop`,
was read over 11 hits, which is a quantity of evidence and not a rate.
The same passage asks a rate rule for a distribution over prose somebody edited,
and twenty documents from one library's public-domain holdings
are a shape rather than a norm,
however wide the spread `em-dash-density` turns out to have.

**They are not a measurement of Polish.**
Every property reported here belongs to a corpus,
and several belong to a corpus *build*:
the CRLF endings, the asterisk emphasis, the space-aligned tables
and the licence notice were all put there by whoever made the text export.
[corpora.md](corpora.md#what-the-survey-settles) states the general form of this,
having measured it on corpora that announce themselves as builds.
What this run adds is that a plain-text file carries the same freight,
which is why
[rules.md](rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives)
reads a recognized suffix as a promise the format makes
rather than as a fact about the file.

**They do not answer corpus sourcing.**
Neither body here is one of the two that
[corpora.md](corpora.md#the-composition-this-argues-for) argues for.
Wolne Lektury is in neither of them, on register, provenance and period at once,
and KSeF is one repository by a handful of authors
where that document asks for a list of them.
This is what could be fetched and run in an afternoon:
enough to exercise the harness, and not enough to calibrate a rule.
