# What the typography pack fired on

The typography pack set its thresholds and its exemptions by judgement,
and the prose in its test suite was written to exercise the machinery.
This document is what the seven rules did when handed Polish somebody wrote:
how often each fired, over how much text,
what its hits turned out to be when they were read,
and what none of it can mean.
Two more rules were run over the same two bodies and left the pack before it,
which [the reading that removed them](#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt)
holds along with their numbers.

The pack is retired and so is the engine that ran it,
and [linter.md](linter.md#co-zamknęło-pakiet-reguł) holds that decision.
This document survives it because it is the price the decision was taken at:
a reader who thinks the idea deserves another try
should start from these numbers rather than from the intuition that produced them.
No run reported here can be taken again.
The commands below are what produced the figures, recorded rather than offered,
and the code they name is in git.

The text is two bodies, at the two ends of
[the argument corpora.md settles](corpora.md#what-the-survey-settles).
One is literary and expository prose from Wolne Lektury,
which reached its reader through an editor, a typesetter and a corpus build.
The other is [the audit corpus](audit-corpus.md):
the documentation of two Polish state IT systems,
cloned from version control and extracted to prose,
which has reached nobody.
The rule against the straight ASCII quotation mark reads the difference:
`quote-straight` fired nought times in 1,940,517 words of the first
and 442 times in 31,417 words of the second.

That pair of numbers is
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)'s
argument measured instead of asserted.
The remaining six rules come out of the two bodies ranked differently,
which is the reason for reading both.
`quote-english` finds nothing in either,
for the reason `quote-straight` finds nothing in the first.
Four rules do point at the defect they name somewhere,
at shares running from one in 166 hits to thirty-five in thirty-five,
and which of the two bodies a rule is right about
is not the same from rule to rule.
The sixth is the pack's only rate rule,
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
and its documents are the only ones short enough to reach a rate rule's floor.
It is also the one stratum that stands in lines,
the export setting a prose paragraph on a single line however long it runs —
1,346 characters for the longest in the first volume of *Lalka* —
so a verse line is the only line break in the corpus
that falls where a line ends on a page,
which is what let
[the two rules that read a line end](#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt)
be read at all.

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

### The audit corpus

Both repositories are cloned at the commits
[the list](audit-corpus.md#the-list) pins
and extracted to prose by the run that document prints.
The prose is what this document measures:
39 files and 31,417 words,
24,663 of them `ksef-docs` and 6,754 `rit-dokumentacja`.

The same 39 files as they stand are 53,814 words,
and the difference is the argument for having an extraction step at all.
`missing-space-after-full-stop` fires 748 times over the files
and 166 times over the prose, for the same one defect either way.
[extraction.md](extraction.md#an-inline-construct-leaves-its-text-or-takes-the-space-with-it)
holds the pair per rule for `ksef-docs`, and what the step costs to buy them.

The two members lose different amounts to that step, and the reason is a format
that [the list](audit-corpus.md#the-list) names, with the counts:
`rit-dokumentacja` writes API tables where `ksef-docs` writes prose,
and a table is apparatus.
That is the corpus the figures below are over,
and the same difference is most of what the hits below are not.

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
and prints a seven-row table over it.
The run says on stderr how many files it went past and in which formats,
which warns and does not reach them:
naming the files is what the `find` is for.
The same walk over `rit-dokumentacja/` reaches no file at all,
and prints seven rows of noughts with the warning standing above them.

## The rates

Over all 326 files of Wolne Lektury:

```text
326 files, 1940517 words, 135192 sentences, 7 rules

rule                             fired  abstained       measured          rate
double-space                       139          0  1940517 words  0.1 per 1000
em-dash-density                     21        287   39 documents         53.8%
missing-space-after-full-stop       11          0  1940517 words  0.0 per 1000
missing-space-after-punctuation     31          0  1940517 words  0.0 per 1000
quote-english                        0          0  1940517 words  0.0 per 1000
quote-straight                       0          0  1940517 words  0.0 per 1000
space-before-punctuation            67          0  1940517 words  0.0 per 1000
```

Over the prose extracted from the audit corpus:

```text
39 files, 31417 words, 2915 sentences, 7 rules

rule                             fired  abstained      measured           rate
double-space                        35          0   31417 words   1.1 per 1000
em-dash-density                      7         10  29 documents          24.1%
missing-space-after-full-stop      166          0   31417 words   5.3 per 1000
missing-space-after-punctuation     11          0   31417 words   0.4 per 1000
quote-english                        0          0   31417 words   0.0 per 1000
quote-straight                     442          0   31417 words  14.1 per 1000
space-before-punctuation             5          0   31417 words   0.2 per 1000
```

Findings by stratum and by repository,
so that a register can be told from a rule
and one writer's habit from the corpus:

| rule | proza | wykład | wiersze | notices | `ksef-docs` | `rit-dokumentacja` |
| --- | --- | --- | --- | --- | --- | --- |
| words | 912,377 | 1,011,472 | 16,668 | 64,468 | 24,663 | 6,754 |
| `double-space` | 0 | 139 | 0 | 12 | 5 | 30 |
| `em-dash-density` | 11 of 11 | 10 of 20 | 0 of 8 | 0 of 326 | 6 of 25 | 1 of 4 |
| `missing-space-after-full-stop` | 3 | 8 | 0 | 1 | 166 | 0 |
| `missing-space-after-punctuation` | 0 | 31 | 0 | 0 | 3 | 8 |
| `quote-english` | 0 | 0 | 0 | 0 | 0 | 0 |
| `quote-straight` | 0 | 0 | 0 | 12 | 314 | 128 |
| `space-before-punctuation` | 10 | 57 | 0 | 0 | 4 | 1 |

The two members disagree as sharply as the two bodies do.
`missing-space-after-full-stop` fires 166 times over the first
and not once over the second, and `double-space` 5 against 30
over a quarter of the words,
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
a body carrying 442 straight marks
carries not one English opening `“` to be confused with them.
What `quote-straight` does with its 442
is [the last of the readings below](#quote-straight-fired-442-times-and-was-right-about-296).

## What the hits over published Polish turned out to be

A rule whose answer depends on the site owes an audit rather than a rate.
All 248 site-anchored hits over Wolne Lektury were classified,
and each class read.

### `double-space` measured two tables

All 139 of its hits are in two of the 326 files,
both of which carry tables laid out with runs of spaces:
Skłodowska-Curie's measurements of the radioactivity of uranium compounds,
and Walewska's counts of women enrolled at Polish universities.

```text
Tlenek uranu czarny, U2O4,    2,6
Tlenek uranu zielony, U2O4    1,80
```

The rule is not wrong about the characters in front of it.
It is measuring a table rather than a sentence,
which is the failure the engine attributed to markup formats
and declined to run a whole-file check over,
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

All 659 site-anchored hits over the audit corpus were classified as well,
each by what stands around it:
a source path, a quoted identifier, a colon inside a name,
a run of two spaces in running Polish.

### `missing-space-after-punctuation` read a colon inside an identifier

Not one of the 11 is the defect, and all 11 are one class:

| hits | | what it is |
| --- | --- | --- |
| 8 | 73% | a colon inside a quoted value: `"xml:lang"`, `"HH:MM"` |
| 3 | 27% | the axis separator of an XPath expression: `ancestor-or-self::ds:Signature` |

Both are the rule's own false positive,
a colon separating the parts of an identifier rather than a clause from a clause,
and the rule has no way to tell that colon from the one it is looking for.
Over published Polish the same rule read an emphasis marker for 22 of its 31 hits,
which is the corpus supplying the noise;
here the corpus supplies none and the rule supplies all of it.

### `missing-space-after-full-stop` read the text of a link

166 hits, one of them the defect.

| hits | | what it is |
| --- | --- | --- |
| 157 | 95% | a source path standing as the visible text of a link to the file it names: `KSeF.Client.Tests.Core\E2E\Certificates\CertificatesE2ETests.cs` |
| 6 | 4% | a dotted identifier: `InvoiceQueryFormType.RR`, `securitySchemes.Bearer`, `operation.Status` |
| 2 | 1% | a project name inside a code span inside such a link: `KSeF.Client.Tests.CertTestApp` |
| 1 | 0.6% | the defect: `części paczki.Po upływie` |

The extraction is doing what it promised and the cost is visible here.
A link leaves its text behind so that the space in front of it has somewhere to go,
and in this repository that text is 157 full stops inside a path.
[extraction.md](extraction.md#what-the-reader-sees-is-not-always-polish)
prices the alternative, which is worse on the pack and better on this rule,
and splits the same 166 by the construct each arrives through
rather than by what the token is.

Over the same files as they stand the rule fires 748 times
for the identical single defect,
because the justification assumes the linter is not shown the code spans
and such a run shows it 32 files of them.
That is the number to compare 166 against:
the extraction removes more than three quarters of a rule's hits
and none of its evidence.

### `double-space` and `space-before-punctuation` pointed at real defects

`double-space` fired 35 times and every one of them is the defect:
a run of two or more spaces somebody typed in running Polish prose —
`zostanie/powinien zostać  zignorowany`, `z obiektów  InvoiceMetadataSeller`,
`o  którym mowa w  art.  47 ust. 1`.
Every hit was traced back to the file it came from,
because a run of spaces is the finding an extraction is likeliest to invent:
the two spaces stand in the Markdown for all 35.

30 of the 35 are in `rit-dokumentacja`,
and they are the first defects this rule has found
over any body measured in this repository.
Over Wolne Lektury this rule fired 139 times and found no defect at all,
every hit being a table laid out with spaces in a file that claimed to be prose,
and the difference between the two readings is not the rule:
it is that one corpus reached its reader through a typesetter and the other did not.
One of the five hits in `ksef-docs` is worth naming for where it sits.
The run is inside an image's description, `QR  Certyfikat`,
which the extraction keeps as prose because a reader can be shown it,
so the defect is in text nobody proofreads.

`space-before-punctuation` fired 5 times and 4 are the defect:
`na format : Schemat_{systemCode}`, `IsTruncated = false , kolejne`,
`przykładowe implementacje .`, and `na adres URL tego dokumentu, .`
The fifth is an ellipsis standing for text left out,
`Authorization: Bearer ...)`,
which is the class the same rule's row of spaced full stops
falls into over published Polish.

### `quote-straight` fired 442 times and was right about 296

296 of the 442 are the defect,
more than the eight other rules turned up between them
over both bodies together:

| hits | | what it is |
| --- | --- | --- |
| 296 | 67% | a word, a phrase or a whole sentence in straight quotes |
| 144 | 33% | a name or a value the system uses, quoted where a code span belongs |
| 2 | 0.5% | a straight mark closing a quotation that opened with `„` |

The first class is the defect the rule names,
and in `ksef-docs` it is one document's habit:
`api-changelog.md` quotes API error messages and OpenAPI field descriptions
release by release — *"Uwierzytelnianie zakończone niepowodzeniem z powodu
błędnego tokenu"*, *"Certyfikat zawieszony"* —
and holds four fifths of that member's hits by itself.
[The list](audit-corpus.md#what-a-second-repository-buys)
owns that share and what a second repository does to it.

The second class is a straight mark that is right as a character
and wrong as markup: `"status"`, `"InvoiceRead"`, `"en-GB"`, `"image/jpeg"`,
`"2015-05-01"`, `"xml:lang"`.
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
| `ksef-docs` | 25 | 0.0 | 5.7 | 59.6 | 6 |
| `rit-dokumentacja` | 4 | 0.0 | 3.3 | 13.5 | 1 |

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
seven documents run above the threshold and six are reported,
because a rate exists wherever the words do
and reporting one takes the evidence `min_count` asks for as well.
Reading the dashes then gives the literary corpus's failure a second time,
with a different convention doing it.
Of the 70 dashes in the seven documents that fire,
47 separate a term from its gloss, one item to a line:
`SHORT_TEXT – krótki tekst`, `TO_ARCHIVE – przeniesienie do archiwum`,
`RRRRMMDD – data przyjęcia faktury`.
Four are a numeric or alphabetic range, `[0–9 A–F]`,
which the rule counts because its pattern takes the en dash alongside the em dash.
The remaining 19 stand in running prose, where the rule is aimed,
and only two of them are the paired aside —
`Przy wysyłce faktury – zarówno w trybie interaktywnym, jak i wsadowym – należy` —
the rest being a single dash where a colon or a comma would do:
`nie ma odpowiednika w systemie RIT – w takiej sytuacji należy`.
So the highest rate in the table, 59.6 over the 151 words of `numer-ksef.md`,
is a document defining the parts of an identifier.
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
the pack's one whole-file rule declines on every one of them,
`measured` reads `0 documents`
and the rate column reads `—`.
That is the intended answer,
and it is a different answer from the `0.0%`
the same rule prints over the `wiersze` stratum,
where it measured 8 documents and found nothing in them.
The extraction is what turns the first into the second:
over the prose `em-dash-density` reaches 29 of the 39.
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
The rule reaches 29 of its documents and abstains on 10,
nine of them under the word floor.
The tenth is one `ksef-docs` file
standing at 10.2 dashes per 1000 words on 2 of them:
a reading above the ceiling
with less evidence behind it than `min_count` asks for.
That one file is the only place in either body
where the report tells the two floors apart.

## Dwie reguły wyszły z pakietu, i to jest ich odczyt

`orphan-single-letter-word` i `trailing-space` czytały koniec wiersza,
a rejestr, o który temu pakietowi chodzi, takiego końca nie ma.
Dokumentacja stoi w formacie znacznikowym,
gdzie pojedynczy koniec wiersza jest spacją;
[ekstrakcja](extraction.md#after-joining-a-line-end-is-not-there-to-be-read)
skleja akapit w jeden wiersz i zabiera po drodze każdą spację, która stała na końcu;
a przebieg nad plikami zamiast nad prozą czyta łamanie formatu, nie czytelnika,
czego silnik odmawiał każdemu checkowi mierzącemu cały plik.
Obie reguły są kształtu audytowego,
więc każda jest winna udział trafień, które były usterkami,
i żaden z korpusów, o które prosi
[corpora.md](corpora.md#the-composition-this-argues-for),
tego udziału im nie da.
Wyjściem jest więc rozstrzygnięcie zamiast liczby,
a rozstrzygnięciem — usunięcie obu.
Liczby niżej pochodzą z tych samych dwóch przebiegów, co reszta dokumentu,
z pakietu w kształcie sprzed usunięcia.

### `orphan-single-letter-word`: 133 trafienia i ani jedna usterka

Nad Wolnymi Lekturami reguła mierzyła 5481 wierszy warstwy `wiersze`,
które poeta napisał jako wiersze, i nie strzeliła nad nimi ani razu.
Pozostałe 31 plików `prozy` i `wykładu` odmówiła,
bo eksport stawia tam akapit w jednym wierszu, jakkolwiek długi by był,
więc koniec wiersza jest tam końcem akapitu i przesłanki reguły nie ma.
Nad korpusem audytowym odmówiła wszystkich 39 plików z tego samego powodu.

Co reguła zgłosiłaby bez tej odmowy, pokazuje przebieg ze zdjętą przesłanką.
Ze złożoną wielkością liter i bez warunku na dokumencie
strzelała 124 razy nad wszystkimi 326 plikami Wolnych Lektur,
a nad korpusem audytowym 9 razy, i ani jedno z tych 133 trafień
nie było jednoliterowym słowem zostawionym na końcu wiersza:

| trafienia | | czym są |
| --- | --- | --- |
| 70 | 53% | liczebnik rzymski `I`, w `Tom I`, `Rozdział I`, `Mieszko I` |
| 44 | 33% | jednoliterowe słowo kończące akapit: `— A!… a!…`, `złożony z:`, `chodzi więc o:` |
| 11 | 8% | `a` dopełniacza po apostrofie: `Locke'a`, `Farrère'a`, `Lafayette'a` |
| 5 | 4% | wiersz poezji cytowany w krytyce, złamany tam, gdzie złamał go poeta |
| 3 | 2% | skrót `w.` od *wiek* |

Największa klasa to złożona wielkość liter spotykająca polszczyznę:
złożone `i` czyta się jako liczebnik, którym polszczyzna liczy rozdziały i władców,
więc lista reguły stała po małej literze,
a kosztowało to zdanie otwierające się na `A` albo `W` na samym końcu wiersza.
Druga klasa to przesłanka, która nie zachodzi, a nie reguła, która się myli:
słowo na końcu akapitu nie ma za sobą niczego, od czego miałoby być odcięte,
i nad korpusem audytowym jest to całe dziewięć tamtejszych trafień,
osiem z nich przyimkiem zapowiadającym listę pod sobą.
Czwarta to przesłanka, która zachodzi,
w jedynym miejscu tych dwóch warstw, gdzie zachodzi,
i stoi w pliku prozy odmówionym dokoła niej:
`wyka-rzecz-wyobrazni` cytuje wiersze, o których pisze,
a jedna odpowiedź na plik musi być tą ostrożną.
Trzecia i piąta są pytaniem o tokenizator,
bo ani `a` po apostrofie, ani `w` skrótu `w.` nie jest słowem.

Co dzieli warstwy, widać po tym, ile akapitów pliku wychodzi poza jeden wiersz:

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

`proza` biegnie od 0,00 do 0,02, a `wykład` od 0,00 do 0,24,
wobec 0,50 do 0,93 dla `wierszy`.
Reguła nie znalazła więc niczego tam, gdzie mogła mieć rację,
i znalazła 124 rzeczy tam, gdzie racji mieć nie mogła,
bo żadna proza w żadnym z tych dwóch korpusów nie stoi w wierszach.

### `trailing-space`: tabela, a w rejestrze docelowym nic

Nad Wolnymi Lekturami reguła strzelała 110 razy,
a 96 z tych trafień stoi w tych samych dwóch plikach, co wszystkie trafienia
`double-space`: w tabelach ułożonych ciągami spacji.
Nad prozą korpusu audytowego nie mogła strzelić w ogóle,
a nad tymi samymi plikami przed ekstrakcją strzelała 431 razy,
co jest liczbą o formacie plików, a nie o polszczyźnie w nich.

Uzasadnienie tej reguły mówiło, że biała spacja na końcu wiersza
nie zmienia niczego w tekście, który widzi czytelnik.
W Markdownie dwie spacje na końcu wiersza są złamaniem wiersza,
więc zdanie to jest fałszywe dokładnie tam, gdzie stoi rejestr docelowy,
a to, co z reguły zostaje, jest sprawą dla `.editorconfig`,
a nie twierdzeniem o polszczyźnie.

### Co usunięcie zabrało ze sobą

`trailing-space` była regułą rodzaju `pattern` i nie zostawiła po sobie nic.
Za `orphan-single-letter-word` stała maszyneria, która nie miała innego wołającego:
rodzaj checku `line-end-word` i `needs_hard_wrap` w `olski/checks.py`,
`hard_wrapped` i `HARD_WRAP_SHARE` w `olski/document.py`
oraz jednostka `line`, w której liczyło się jedynie to, co ta reguła zgłaszała.
Dokument nie odpowiada już na pytanie, gdzie kończy się wiersz,
bo nikt go o to nie pyta.

Rejestrem, którego te dwie reguły chcą, jest tekst, który ktoś złoży,
a nie każdy tekst stojący w wierszach.
Komentarz w pliku źródłowym stoi w wierszach, które czytelnik widzi,
i jest najbliższym kandydatem, jaki to repozytorium ma;
ekstrakcja z modułu sklejała jednak i te wiersze, z tego samego powodu:
regułą, która by tam strzeliła, byłoby żądanie twardej spacji w kodzie źródłowym.

## What these numbers are not

**They are not a calibration of any rule,
and no rule here should carry one because of these runs.**
A hit count beside a defect count is the shape of an audit,
which is one of the two shapes a rule's calibration field could take,
and this document reports several:
139 hits and no defects, 11 hits and 11, 442 hits and 296.
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
one of its files supplies four fifths of one member's quotation marks,
and one of the two members supplies six sevenths of another rule's hits
on a quarter of the words.
The same passage asks a rate rule for a distribution over prose somebody edited,
and twenty documents from one library's public-domain holdings
are a shape rather than a norm,
however wide the spread `em-dash-density` turns out to have.

**They are not a measurement of Polish.**
Every property reported here belongs to a corpus,
and several belong to a corpus *build* or to an extraction:
the CRLF endings, the asterisk emphasis, the space-aligned tables
and the licence notice were all put there by whoever made the text export,
and a path standing where a reader sees a link's text
is what `harness/markdown.py` keeps on purpose.
[corpora.md](corpora.md#what-the-survey-settles) states the general form of this,
having measured it on corpora that announce themselves as builds.
What these runs add is that a plain-text file carries the same freight,
which is why the engine read a recognized suffix as a promise the format makes
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
