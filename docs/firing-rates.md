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
The other is [the audit corpus](audit-corpus.md):
the documentation of two Polish state IT systems,
cloned from version control and extracted to prose,
which has reached nobody.
The rule against the straight ASCII quotation mark reads the difference:
`quote-straight` fires nought times in 1,940,517 words of the first
and 750 times in 38,937 words of the second.

That pair of numbers is
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)'s
argument measured instead of asserted.
The remaining eight rules come out of the two bodies ranked differently,
which is the reason for reading both.
`quote-english` finds nothing in either,
for the reason `quote-straight` finds nothing in the first.
`orphan-single-letter-word` reads 295 of the 365 files and fires nought times,
having declined the other 70 as text whose line ends are not a page's,
and `trailing-space` finds a table in the first body
and cannot fire at all in the second.
Four rules do point at the defect they name somewhere,
at shares running from nothing in 205 hits to eleven in eleven,
and which of the two bodies a rule is right about
is not the same from rule to rule.
The eighth is the pack's only rate rule,
and it comes out of both bodies with a distribution
and out of neither with a threshold.

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
and the notices report 12 straight quotation marks
and 12 runs of two or more spaces over 64,468 words,
which is what the trim keeps out of every number below.
The line-end rule declines all 326 of them,
each notice being a set of paragraphs on a line apiece.

The files are CRLF throughout, and no rule sees it,
because `Path.read_text` translates line endings before a document is built.
Anyone checking `trailing-space` against the raw bytes will find the report
disagreeing with a count of runs of spaces before a line end,
and the report is the one describing what olski was shown.

### The audit corpus

Both repositories are cloned at the commits
[the list](audit-corpus.md#the-list) pins
and extracted to prose by the run that document prints.
The prose is what this document measures:
39 files and 38,937 words,
23,825 of them `ksef-docs` and 15,112 `rit-dokumentacja`.

The same 39 files as they stand are 53,814 words,
and the difference is the argument for having an extraction step at all.
`missing-space-after-full-stop` fires 748 times over the files
and 156 times over the prose, for the same one defect either way,
and `trailing-space` fires 431 times over the files
and cannot fire over the prose at all.
[extraction.md](extraction.md#an-inline-construct-leaves-its-text-or-takes-the-space-with-it)
holds the pair per rule for `ksef-docs`, and what the step costs to buy them.

One thing the extraction gets wrong belongs to the corpus rather than to a rule,
and the figures below are the corpus as it stands.
A line opening with a triple-backtick code span, as `` ```KOD I``` `` does,
is read as a code fence,
and the block it opens then runs to the next line that is nothing but a fence,
so three of the 32 `ksef-docs` files lose the prose between the two.
Reading the fence as CommonMark does,
where a backtick fence's info string may not contain a backtick,
adds 919 words to that member and takes `quote-straight` over it from 312 to 338.
[TODO.md](../TODO.md) holds the fix.

## What ran

```sh
python3 -m olski polszczyzna --format report --show-abstentions
python3 -m olski polszczyzna/proza --format report
python3 -m olski proza --format report --show-abstentions
python3 -m olski proza/ksef --format report
python3 -m olski proza/rit --format report
python3 -m olski $(find ksef-docs rit-dokumentacja -name '*.md' | sort) --format report
```

The `find` in the last line is not decoration.
A directory walk collects `.txt` and `.text` and nothing else,
so `olski ksef-docs/` reaches one file —
`LICENSE.txt`, the MIT licence, in English, 169 words —
and prints a nine-row table over it.
The run says on stderr how many files it went past and in which formats,
which warns and does not reach them:
naming the files is what the `find` is for.
The same walk over `rit-dokumentacja/` reaches no file at all,
and prints nine rows of noughts with the warning standing above them.

## The rates

Over all 326 files of Wolne Lektury:

```text
326 files, 1940517 words, 135192 sentences, 9 rules

rule                             fired  abstained       measured          rate
double-space                       139          0  1940517 words  0.1 per 1000
em-dash-density                     21        287   39 documents         53.8%
missing-space-after-full-stop       11          0  1940517 words  0.0 per 1000
missing-space-after-punctuation     31          0  1940517 words  0.0 per 1000
orphan-single-letter-word            0         31     5481 lines          0.0%
quote-english                        0          0  1940517 words  0.0 per 1000
quote-straight                       0          0  1940517 words  0.0 per 1000
space-before-punctuation            67          0  1940517 words  0.0 per 1000
trailing-space                     110          0  1940517 words  0.1 per 1000
```

Over the prose extracted from the audit corpus:

```text
39 files, 38937 words, 3391 sentences, 9 rules

rule                             fired  abstained      measured           rate
double-space                        88          0   38937 words   2.3 per 1000
em-dash-density                      7          9  30 documents          23.3%
missing-space-after-full-stop      156          0   38937 words   4.0 per 1000
missing-space-after-punctuation    205          0   38937 words   5.3 per 1000
orphan-single-letter-word            0         39       0 lines              —
quote-english                        0          0   38937 words   0.0 per 1000
quote-straight                     750          0   38937 words  19.3 per 1000
space-before-punctuation             7          0   38937 words   0.2 per 1000
trailing-space                       0          0   38937 words   0.0 per 1000
```

Findings by stratum and by repository,
so that a register can be told from a rule
and one writer's habit from the corpus:

| rule | proza | wykład | wiersze | notices | `ksef-docs` | `rit-dokumentacja` |
| --- | --- | --- | --- | --- | --- | --- |
| words | 912,377 | 1,011,472 | 16,668 | 64,468 | 23,825 | 15,112 |
| `double-space` | 0 | 139 | 0 | 12 | 4 | 84 |
| `em-dash-density` | 11 of 11 | 10 of 20 | 0 of 8 | 0 of 326 | 5 of 24 | 2 of 6 |
| `missing-space-after-full-stop` | 3 | 8 | 0 | 1 | 156 | 0 |
| `missing-space-after-punctuation` | 0 | 31 | 0 | 0 | 10 | 195 |
| `orphan-single-letter-word` | declined | declined | 0 | declined | declined | declined |
| `quote-english` | 0 | 0 | 0 | 0 | 0 | 0 |
| `quote-straight` | 0 | 0 | 0 | 12 | 312 | 438 |
| `space-before-punctuation` | 10 | 57 | 0 | 0 | 4 | 3 |
| `trailing-space` | 0 | 110 | 0 | 2 | 0 | 0 |

The two members disagree as sharply as the two bodies do.
`missing-space-after-full-stop` fires 156 times over the first
and not once over the second, and `missing-space-after-punctuation` 10 against 195,
which is what admitting a second repository is for:
a share read over one of them is one project's convention
until a second one either repeats it or does not.

## Where the quotation mark rules had nothing to find

`quote-straight` and `quote-english` fire nought times
in 1,940,517 words of published Polish.
The corpus is not quiet about quotation:
it carries 8,891 `„` and 8,845 `”`.
What it carries none of is the mark either rule looks for,
and the twelve exceptions in the whole download
sit in a notice the library appends rather than in anybody's Polish.

A rate of nought over 1.9 million words is not a false-positive rate near zero.
It is a corpus that could not have held what the rule looks for,
which is what
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
predicts of exactly these two rules.

Half of that reading holds over the audit corpus too.
`quote-english` fires nought times there as well,
and this time it is the intended answer rather than the empty one:
a body carrying 750 straight marks
carries not one English opening `“` to be confused with them.
What `quote-straight` does with its 750
is [the last of the readings below](#quote-straight-fired-750-times-and-was-right-about-316).

## What the hits over published Polish turned out to be

A rule whose answer depends on the site owes an audit rather than a rate.
All 358 site-anchored hits over Wolne Lektury were classified,
and each class read.

### `orphan-single-letter-word` reads one stratum of the three

The rule measures the 5,481 lines of `wiersze`,
which are lines a poet wrote as lines,
and fires nought times over them.
It declines the 31 files of `proza` and `wykład`,
where the export sets a paragraph on a line however long it runs,
so that a newline there is a paragraph break
and the premise the rule needs is absent.

Both of those come out of an audit,
and the audit is the reason to believe them.
With case folded and no precondition on the document,
the rule fires 124 times over all 326 files,
and not one of the 124 is a one-letter word left at the end of a line.

| hits | | what it is |
| --- | --- | --- |
| 70 | 56% | the Roman numeral `I`, in `Tom I`, `Rozdział I`, `Mieszko I` |
| 35 | 28% | a one-letter word ending a paragraph: `— A!… a!…`, `Jadłaś, Justynko, a?` |
| 11 | 9% | the `a` of an apostrophe genitive: `Locke'a`, `Farrère'a`, `Lafayette'a` |
| 5 | 4% | a line of verse quoted inside criticism, broken where the poet broke it |
| 3 | 2% | the abbreviation `w.` for *wiek* |

The largest class is a fold meeting Polish:
folding case reads the listed `i` into the numeral
Polish counts its chapters and its monarchs in.
So the rule's list is lower case,
and what that costs is the sentence opening on `A` or `W`
at the very end of a line.
The second class is the premise failing rather than the rule misreading anything —
a word at the end of a paragraph has nothing after it to be separated from,
so there is no orphan whatever the measure of the line.
The fourth is the premise holding
in the one place in these two strata where it does,
and it is inside a file of prose that is declined around it,
which is what a per-file precondition costs:
`wyka-rzecz-wyobrazni` quotes the verse it discusses,
and one answer for the file has to be the careful one.
The third and fifth are a tokenizer question:
neither the `a` after an apostrophe nor the `w` of `w.` is a word,
and [TODO.md](../TODO.md) holds them.

What tells the strata apart is how many of a file's paragraphs run past one line:

```sh
python3 -c '
import pathlib, statistics
from olski.document import Document
for name in ("proza", "wyklad", "wiersze"):
    shares = []
    for f in sorted(pathlib.Path("polszczyzna", name).glob("*.txt")):
        d = Document(f.read_text(encoding="utf-8"))
        shares.append(sum("\n" in d.slice(p) for p in d.paragraphs) / len(d.paragraphs))
    print(name, f"{min(shares):.2f}", f"{statistics.median(shares):.2f}", f"{max(shares):.2f}")'
```

`proza` runs from 0.00 to 0.02 and `wykład` from 0.00 to 0.24,
against 0.50 to 0.93 for `wiersze`,
and `HARD_WRAP_SHARE` in `olski/document.py` sits at 0.3.
It sits at the low end of that gap because the same files as downloaded
put `wiersze` at 0.36,
the library's notice being a run of one-line paragraphs
appended to a short poem.

So the rule found nothing wherever it could have been right,
and 124 things wherever it could not,
and it declines the second kind of place instead of reporting from it.
What that leaves is a rule with a firing rate over one stratum of verse
and no false-positive rate over prose at all,
because no body of prose in either corpus is laid out in lines.

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

### `space-before-punctuation` and `missing-space-after-full-stop` pointed at real defects

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

## What the hits over the audit corpus turned out to be

All 1,206 site-anchored hits over the audit corpus were classified as well.
One class runs through four of the rules and is named once here.

**A table written without leading pipes reaches the prose whole.**
The extraction recognizes a row by the `|` that opens it,
which [extraction.md](extraction.md#what-it-does-not-recognize) records as a gap,
and `rit-dokumentacja` writes its API tables in the style the gap lets through:
a header, a `--- | ---` separator and one line per parameter,
none of them opening with a pipe.
Four of that member's seven documents carry such a table,
and each row arrives as part of one long line holding the cells,
the tabs between them, the `<br>` tags inside them
and the JSON examples the cells quote.
553 of the corpus's 1,206 site-anchored findings stand inside those four files,
which is one gap in one extraction
producing more hits than every rule's real defects put together.

### `orphan-single-letter-word` declines all 39 files

Joining a paragraph onto one line
leaves the end of a paragraph as the only line end there is,
so every file here fails the precondition
and the rule measures none of them.

Run without it, the rule fires 12 times and finds no defect:

| hits | | what it is |
| --- | --- | --- |
| 7 | 58% | a one-letter word ending a paragraph, five of them a preposition introducing the list below it: `złożony z:`, `chodzi więc o:` |
| 5 | 42% | a designator or an abbreviation: `XAdES-A`, `w kontekście podmiotu A.`, `Betacom S.A.` |

Neither class is new,
and between them they are the two things the rule now does differently.
The first is the premise failing, as it does over Wolne Lektury.
The second is a capital `A`, which a lower-case list does not match,
and it is the class
[extraction.md](extraction.md#after-joining-a-line-end-rule-has-nothing-left-to-read)
reads out of the rule over a body of notes as well.
136 hits across the two corpora produced no instance of the defect,
and the one stratum where the premise held produced no hits.

### `missing-space-after-punctuation` read a table and a raw tag

Not one of the 205 is the defect.

| hits | | what it is |
| --- | --- | --- |
| 106 | 52% | a JSON example quoted inside a cell of such a table: `{"cat_attributes":[],"id":77,"name":"Root"}` |
| 81 | 40% | a comma or a colon against the `<br>` that ends a line inside such a cell: `wartości:<br>SHORT_TEXT` |
| 8 | 4% | a colon inside a quoted value: `"xml:lang"`, `"HH:MM"` |
| 7 | 3% | the same `<br>`, or a `</font>`, standing outside a table: `podmiotu:<br/>`, `<font color="red">Uwaga:</font>` |
| 3 | 1% | the axis separator of an XPath expression: `ancestor-or-self::ds:Signature` |

The second and fourth classes are one gap seen with and without a table around it:
`<br>` is a raw HTML tag, and
[extraction.md](extraction.md#what-it-does-not-recognize)
keeps one as the characters it is written with,
so the punctuation that closed the line before it arrives touching a tag.
The third and fifth are the rule's own false positive,
a colon separating the parts of an identifier rather than a clause from a clause.
Over published Polish the same rule read an emphasis marker for 22 of its 31 hits;
over documentation 194 of its 205 are markup,
and the 11 that are not are that colon.

### `missing-space-after-full-stop` read the text of a link

156 hits, one of them the defect.

| hits | | what it is |
| --- | --- | --- |
| 149 | 96% | a source path standing as the visible text of a link to the file it names: `KSeF.Client.Tests.Core\E2E\Certificates\CertificatesE2ETests.cs` |
| 6 | 4% | a dotted identifier: `InvoiceQueryFormType.RR`, `securitySchemes.Bearer`, `operation.Status` |
| 1 | 0.6% | the defect: `części paczki.Po upływie` |

The extraction is doing what it promised and the cost is visible here.
A link leaves its text behind so that the space in front of it has somewhere to go,
and in this repository that text is 149 full stops inside a path.
[extraction.md](extraction.md#what-the-reader-sees-is-not-always-polish)
prices the alternative, which is worse,
and splits the same 156 by the construct each arrives through
rather than by what the token is.

Over the same files as they stand the rule fires 748 times
for the identical single defect,
because the justification assumes the linter is not shown the code spans
and such a run shows it 32 files of them.
That is the number to compare 156 against:
the extraction removes four fifths of a rule's hits
and none of its evidence.

### `double-space` and `space-before-punctuation` pointed at real defects

`double-space` fired 88 times, and 34 of those are the defect:
a run of two or more spaces somebody typed in running Polish prose.

| hits | | what it is |
| --- | --- | --- |
| 54 | 61% | space used to lay out a table written without leading pipes |
| 34 | 39% | the defect: `zostanie/powinien zostać  zignorowany`, `z obiektów  InvoiceMetadataSeller`, `o  którym mowa w  art.  47 ust. 1` |

30 of the 34 are in `rit-dokumentacja`,
and they are the first defects this rule has found
over any body measured in this repository.
Over Wolne Lektury this rule fired 139 times and found no defect at all,
every hit being a table laid out with spaces in a file that claimed to be prose,
and the difference between the two readings is not the rule:
it is that one corpus reached its reader through a typesetter and the other did not.
One of the four hits in `ksef-docs` is worth naming for where it sits.
The run is inside an image's description, `QR  Certyfikat`,
which the extraction keeps as prose because a reader can be shown it,
so the defect is in text nobody proofreads.

`space-before-punctuation` fired 7 times and 4 are the defect:
`na format : Schemat_{systemCode}`, `IsTruncated = false , kolejne`,
`przykładowe implementacje .`, and `na adres URL tego dokumentu, .`
Of the other three, two are an empty cell in one of those tables,
arriving as `, ,`,
and the third is an ellipsis standing for text left out,
`Authorization: Bearer ...)`,
which is the class the same rule's row of spaced full stops
falls into over published Polish.

### `quote-straight` fired 750 times and was right about 316

318 of the 750 are the defect,
more than the eight other rules turned up between them
over both bodies together:

| hits | | what it is |
| --- | --- | --- |
| 316 | 42% | a word, a phrase or a whole sentence in straight quotes |
| 310 | 41% | a cell of a table written without leading pipes |
| 122 | 16% | a name or a value the system uses, quoted where a code span belongs |
| 2 | 0.3% | a straight mark closing a quotation that opened with `„` |

The first class is the defect the rule names,
and in `ksef-docs` it is one document's habit:
`api-changelog.md` quotes API error messages and OpenAPI field descriptions
release by release — *"Uwierzytelnianie zakończone niepowodzeniem z powodu
błędnego tokenu"*, *"Certyfikat zawieszony"* —
and holds nine tenths of that member's hits by itself.
[The list](audit-corpus.md#what-a-second-repository-buys)
owns that share and what a second repository does to it.

The third class is a straight mark that is right as a character
and wrong as markup: `"status"`, `"InvoiceRead"`, `"en-GB"`, `"image/jpeg"`,
`"2015-05-01"`, and the attribute in `<font color="red">`.
A JSON field name carries a straight mark in the JSON,
so what the writer owed here was a code span rather than a Polish quotation,
and no rule reading characters can tell the two apart.

The last class is two hits.
*„Nieprawidłowy skrót pliku"* and *„moment zakończenia"*
open in Polish and close in ASCII,
which is the justification's claim that the mark
carries no information about which end of the quotation it is,
arriving as a defect somebody made rather than as an argument somebody wrote.

## `em-dash-density` has a distribution

The threshold is 10 per 1000 words and was chosen to be lenient.
Per document, over the scopes long enough for the rule to believe its own number:

| stratum | documents | lowest | median | highest | over the threshold |
| --- | --- | --- | --- | --- | --- |
| proza | 11 | 20.2 | 43.1 | 52.0 | 11 |
| wykład | 20 | 1.8 | 10.0 | 18.8 | 10 |
| wiersze | 8 | 0.0 | 0.0 | 8.2 | 0 |
| `ksef-docs` | 25 | 0.0 | 7.8 | 59.6 | 6 |
| `rit-dokumentacja` | 6 | 0.0 | 7.5 | 18.6 | 2 |

The narrative half of Wolne Lektury sits entirely above the threshold
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

The audit corpus is the target register itself, and its two medians land under it.
Its `ksef-docs` row is where this table and
[the row over the same member](#the-rates) part by one document:
six documents run above the threshold and five are reported,
because a rate exists wherever the words do
and reporting one takes the evidence `min_count` asks for as well.
Reading the dashes then gives the literary corpus's failure a second time,
with a different convention doing it.
Of the 118 dashes in the seven documents that fire,
105 separate a term from its gloss, one item to a line or a cell:
`SHORT_TEXT – krótki tekst`, `east – długość geograficzna wschodnia`,
`RRRRMMDD – data przyjęcia faktury`.
Four are a numeric or alphabetic range, `[0–9 A–F]`,
which the rule counts because its pattern takes the en dash alongside the em dash.
Nine are the parenthetical aside the rule was built to count:
`Przy wysyłce faktury – zarówno w trybie interaktywnym, jak i wsadowym – należy`.
So the highest rate in the table, 59.6 over the 151 words of `numer-ksef.md`,
is a document defining the parts of an identifier,
and the two `rit-dokumentacja` documents above the threshold
are dashes inside the tables the extraction did not recognize.
A dash rate over documentation measures the definition list
the way a dash rate over fiction measures the dialogue.

A threshold does not come out of any of this,
for a reason [the last section](#what-these-numbers-are-not) holds
and for one that belongs here:
the Wolne Lektury authors published between 1873 and 1988,
so a dash rate among them is a period style as much as a register one,
and the audit corpus answers with a convention rather than with a norm.
What the runs do establish is that the pack and the harness together
produce a distribution when they are handed prose,
and that the spread is wide enough for the threshold's position in it to matter.

## What the report mode did when rules declined

Three of the report's decisions turn on what a rule declined,
and a corpus that makes rules decline is what shows whether they hold.

**Declines come off the denominator rather than folding into zero.**
Over the audit corpus's 39 files as they stand
both whole-file rules decline on every one of them,
`measured` reads `0 documents` and `0 lines`,
and the rate column reads `—`.
That is the intended answer,
and it is a different answer from the `0.0%`
the same rule prints over the `wiersze` stratum.
What the extraction then does is answer for one of the two and not the other:
over the prose `em-dash-density` reaches 30 of the documents,
where the line-end rule declines all 39 a second time,
joining having left it one paragraph to a line.
What the next two decisions settle is what that `0.0%` is a share of.

**The denominator is what the rule could reach rather than what the corpus held.**
The `wiersze` stratum is where that decision is worth a number.
287 of its 295 fraszki hold fewer than the 150 words `em-dash-density` needs,
so the rule abstains on each of them
and `measured` reads 8 documents rather than 295.
The share is then taken over the documents the rule could have reported on,
which is why that 8 is also the `wiersze` count in
[the distribution](#em-dash-density-has-a-distribution):
where nothing trips the second floor,
the denominator of the row and the population of the table are one number.
Over all 326 files the same accounting reads 21 findings over 39 documents:
a rate of 53.8%, where the run was handed 326 documents
and a share taken over those would have been a share of the download.

**Both floors record the decision, and here one of them had nothing to record.**
`min_words` and `min_count` are each the rule refusing to answer,
so each abstains and names the floor it refused on.
`min_words` is tested first, and that is what leaves the second silent:
of the 39 documents standing over the word floor,
not one runs above the ceiling on fewer than the 3 dashes `min_count` asks for,
so all 287 abstentions are the word floor
and the count floor turns nothing away in the whole download.
A corpus where it does is in
[generated-polish.md](generated-polish.md#the-apparatus-biases-a-rate-by-an-amount-the-corpus-decides).
The 18 documents that are in neither the 21 nor the 287
are documents the rule measured and found within its ceiling,
which is the one silence a firing rate is entitled to.

The audit corpus is nearer than that, and records on the count floor once.
The rule reaches 30 of its documents and abstains on 9,
eight of them under the word floor.
The ninth is one `ksef-docs` file
standing at 10.2 dashes per 1000 words on 2 of them:
a reading above the ceiling
with less evidence behind it than `min_count` asks for.
That one file is the only place in either body
where the report tells the two floors apart.

The `orphan-single-letter-word` row is the other half of the same point:
a unit can be right about the check and wrong about the rule.
The unit counts what the check can fire at most once per, which is a line,
and 101,799 of this corpus's 107,280 lines
are paragraphs of the prose strata or the blanks between them.
Only the remaining 5,481 are lines in the sense the rule means.
What keeps the others out of the rate is not the unit but the refusal:
the rule declines those 31 files whole,
and a file declined whole takes its lines with it.

## What these numbers are not

**They are not a calibration of any rule,
and no rule here should carry one because of these runs.**
A hit count beside a defect count is the shape of an
[`Audit`](rules.md#two-fields-that-are-not-decoration),
and this document reports several:
124 hits and no defects, 11 hits and 11, 750 hits and 316.
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
The audit corpus is that stage and fails the other half of the demand.
It is two repositories where
[corpora.md](corpora.md#the-composition-this-argues-for) asks for a list of them,
one of its files supplies nine tenths of one member's quotation marks,
and 553 of its 1,206 findings come from a single gap in the extraction
rather than from anything a writer did.
The same passage asks a rate rule for a distribution over prose somebody edited,
and twenty documents from one library's public-domain holdings
are a shape rather than a norm,
however wide the spread `em-dash-density` turns out to have.

**They are not a measurement of Polish.**
Every property reported here belongs to a corpus,
and several belong to a corpus *build* or to an extraction:
the CRLF endings, the asterisk emphasis, the space-aligned tables
and the licence notice were all put there by whoever made the text export,
and the pipe-less tables and the surviving `<br>`
are what `harness/markdown.py` does not recognize.
[corpora.md](corpora.md#what-the-survey-settles) states the general form of this,
having measured it on corpora that announce themselves as builds.
What these runs add is that a plain-text file carries the same freight,
which is why
[rules.md](rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives)
reads a recognized suffix as a promise the format makes
rather than as a fact about the file,
and that an extraction acquires freight of its own,
which is why [extraction.md](extraction.md) owes the account it gives.

**They do not answer corpus sourcing.**
Wolne Lektury is in neither of the two corpora
[corpora.md](corpora.md#the-composition-this-argues-for) argues for,
on register, provenance and period at once.
The audit corpus is the first of the two, at the size of its first two members,
and [the list](audit-corpus.md#what-a-second-repository-buys)
holds what the third one has to move.
This is what could be fetched and run in an afternoon:
enough to exercise the harness, and not enough to calibrate a rule.
