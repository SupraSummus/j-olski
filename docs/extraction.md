# Markdown in, prose out

The grammar takes plain Polish sentences,
and the bodies it is measured against
include documentation and notes kept in Markdown.
So a step before the grammar turns a corpus into files olski reads as prose:
`harness/markdown.py`, outside the `olski` package,
because reading a document format is a different job from deriving a sentence.

```sh
python3 -m harness.markdown korpus/ --into proza/
python3 -m olski.check proza/*.txt
```

An extraction is a transformation the grammar is then measured over,
so it owes an account of what it invents
exactly as a coverage figure owes its corpus.
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

## Markdown czyta parser, a nie wzorzec

Gdzie konstrukcja się zaczyna i gdzie kończy, rozstrzyga `markdown-it-py`,
a ten moduł rozstrzyga, co z nią zrobić.
Podział jest taki, że pierwsza połowa jest pytaniem o CommonMark,
na które odpowiada coś sprawdzanego wobec specyfikacji,
a druga jest decyzją tego repozytorium
i żaden renderer nie ma o niej zdania:
co jest aparatem i co konstrukcja po sobie zostawia, kiedy odpada.

Kupuje to te konstrukcje, których wzorzec nie rozstrzyga,
a dwie z nich rozstrzygał źle.
Emfaza jednoznakowa połykała następną i zostawiała po sobie znacznik,
więc `*p*, a razem z nim *p*` wychodziło jako `p*, a razem z nim *p`,
czyli dokładnie jako znak, którego nikt nie napisał.
Wstawka kodowa z trzech grawisów otwierająca wiersz
czytała się jako płotek bloku kodu,
choć CommonMark zabrania grawisu w napisie informacyjnym płotka,
i proza pod nią przepadała aż do następnego wiersza z samym płotkiem.
Obie klasy znikają razem z dopasowywaniem, i znikają razem:
parser albo składa dokument tak, jak renderer, albo nie,
więc nie ma tu usterki do poprawienia osobno.

Trzecia klasa jest tą, której nikt nie zauważył: znacznik w zagnieżdżeniu.
`- > „Przyjeżdżam."` jest cytatem w pozycji listy,
a `- 1. → 3 lata` listą w liście,
i wzorzec zdejmował z takiego wiersza znacznik zewnętrzny,
a wewnętrzny zostawiał w prozie.
Wszystkie trzy klasy stoją w korpusach, a nie tylko w teorii:
zagnieżdżenie w 13 z 527 notatek,
a emfaza w jednym z dziewięciu rozdziałów wspomnienia
— [generated-polish.md](generated-polish.md#what-was-measured)
mierzy oba te ciała — gdzie zostawiała dwie osierocone gwiazdki.
Żadna reguła pakietu żadnej z nich nie zgłaszała,
bo znak aparatu nie jest tym, na co te reguły patrzą,
i dlatego trzecia klasa mogła tam siedzieć nienazwana.
Znalazło ją przeliczenie: przebieg przed zmianą i po niej
nad tym samym korpusem, plik po pliku.

Cena stoi w [`pyproject.toml`](../pyproject.toml).
Parser jest zależnością harnessu, a nie olskiego —
gramatyka czyta czysty tekst i o formacie dokumentu zdania nie ma —
więc deklaruje się tam, gdzie instalują się narzędzia do testów,
a powierzchnia zależności samego pakietu zostaje jednym wpisem, jakim była.

## What it drops and what it keeps

Frontmatter, fenced and indented code, headings, tables,
raw HTML — a block of it, an inline tag and a comment alike —
and the list of links that closes a document go.
Inline markup is replaced by the text it wrapped rather than deleted,
list and blockquote markers are dropped and their text kept,
and the lines of a paragraph are joined with single spaces,
so a line of the result is a paragraph
and where the author's editor wrapped leaves no trace in what comes out.
`harness/markdown.py` is the truthful copy of all of that;
what follows is what the code cannot show.

## An inline construct leaves its text, or takes the space with it

The rule that keeps the extraction out of the reader's way
is that a construct leaves behind the characters it wrapped.
A link leaves its text and emphasis leaves what it emphasized,
so there is no hole for the space in front of it to fall into.
The constructs that have no text to leave —
an image with no description, an HTML comment —
take that whitespace along instead.

What that buys is measurable, and it was measured with the typography pack,
which is retired ([linter.md](linter.md#co-zamknęło-pakiet-reguł)).
The instrument is gone and the property it was pointed at is what this step owes:
a mark standing where nobody typed one is a mark somebody else's text does not have,
and the sentence splitter under the grammar reads marks
([`olski/document.py`](../olski/document.py)).
So the tables here are dated rather than rerunnable,
and what they establish still holds.
Three corpora were run twice each,
once over the extracted prose
and once over the files as they stand with their names changed to `.txt`.
Each cell is the findings over the prose against the findings over the file:

| | notes | memoir | KSeF |
| --- | --- | --- | --- |
| `double-space` | 0 / 0 | 0 / 0 | 5 / 456 |
| `missing-space-after-full-stop` | 0 / 0 | 0 / 0 | 166 / 748 |
| `missing-space-after-punctuation` | 23 / 309 | 34 / 34 | 3 / 76 |
| `quote-straight` | 1,649 / 1,772 | 481 / 481 | 314 / 978 |
| `space-before-punctuation` | 1 / 9 | 2 / 2 | 4 / 45 |

No rule reports more over the prose than over the file it came from.
The notes and the memoir are the two bodies
[generated-polish.md](generated-polish.md#what-was-measured) reports on,
and KSeF is the first repository in
[the audit corpus](audit-corpus.md#the-list).
The prose half of its cells is one member of the corpus
[the typography pack was audited over](firing-rates.md#the-rates),
and the file half is that member before the step,
which is the argument for having the step.

Counting the same is not the same as pointing at the same place,
so the 238 findings of the spacing rules — the ones a deletion invents —
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
`nazwa.Pola` inside backticks reaches the grammar
as a full stop with no space after it,
and so does a source file used as a link's visible text.

Over KSeF that showed up in one rule.
[The audit](firing-rates.md#missing-space-after-full-stop-read-the-text-of-a-link)
reads all 748 of `missing-space-after-full-stop`'s hits over the files as they stand
and finds one defect among them, the rest code and links.
The extraction removes 582 of the 748,
which is the fenced code and every link target.
Of the 166 left,
157 are a source path standing as the text of a link to the file it names —
79 occurrences of 29 paths, the commonest of them ten times,
`KSeF.Client.Tests.Core\E2E\KsefToken\KsefTokenE2ETests.cs` —
6 are a dotted identifier, 2 stand inside a code span,
and the last is the defect the audit found.
The same keeping accounts for 16 of the 314 straight quotation marks
and for 3,181 words, one in eight of what a rate there is divided by.

Deleting the spans instead was tried and is worse,
though it was not worse on every rule at once.
It leaves the punctuation that separated them touching:
`(enum: A, B, C)` written with each value in a code span
extracts to `(enum:,,,)`,
which takes `missing-space-after-punctuation` over KSeF from 3 findings to 106
and puts nearly all of that rule's hits inside a parenthesis
where a reader can no longer see what stood there.
It also leaves `missing-space-after-full-stop` with the single defect and nothing else,
which is that rule's best reading anywhere in this repository,
so the choice is between one rule's noise and another's,
and it is settled by what a reader can do with a hit.
A hit a reader dismisses at a glance is the cheaper of the two,
and 157 hits on the text of a link are a document to correct
rather than a rate to discount.

## After joining, a line end is not there to be read

Joining a paragraph onto one line takes two properties out of the text
along with the markup, and both of them were ones a rule could have read.
The rules are gone and the loss is not,
because it is a property of what this step produces
and it reaches anything that would ever want a line end back.

Whitespace before a line end does not survive,
because joining strips it at every line end it consumes.
Over KSeF that is 426 findings a rule against trailing whitespace reports
over the files and cannot report over the prose,
and none of them is recoverable from it,
so a corpus is audited for trailing whitespace over its files
or not at all.

A line end a reader sees does not survive either,
the end of a paragraph becoming the only line end there is.
A rule against a one-letter word left at a line end
reports 10 findings over the notes as they stand
and declines 183 of the 527 files.
The 10 are letters standing mid-line for every reader,
because a single newline in Markdown is a space,
and the 183 are the notes that already set each paragraph on a line of its own —
which is what joining then does to the remaining 344,
so over the prose such a rule declines every file and reports nothing.

Run over the prose with that refusal taken out,
it reports 6 findings over the notes and 2 over the memoir,
none of them a word left at the end of a line:
the `a` of an apostrophe genitive (*Lagrange'a*, *hardware'u*),
the abbreviation `w.` for *wiek* (*z XXI w.*),
a shell flag (*env -i.*),
and a preposition at the end of a paragraph, which has no line to be left at.
The pack had both rules and lost them before it was itself retired,
and this step is part of the reason:
[what they turned out to fire on](firing-rates.md#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt)
reads the same classes out of them over two published corpora,
and a corpus of joined prose is one no line-end rule can be calibrated against.

## Nie każdy akapit, który stąd wychodzi, jest zdaniem

Akapitem jest tu wszystko, co parser czyta jako akapit,
więc pozycja listy i wiersz zapowiadający blok kodu wychodzą stąd jako akapity,
a podział na zdania oddaje akapit, którego nic nie punktuje,
bo inaczej zapowiedź wpadałaby w prozę pod sobą.

Regułom pakietu to nie przeszkadza:
reguła mierzy znaki i słowa i niczego od zdania nie żąda.
Gramatyce przeszkadza.
Produkcja `wypowiedzenie` w `olski/subset/wypowiedzenie.py` żąda na końcu kropki,
wykrzyknika albo pytajnika,
więc fragment, który takiego znaku nie niesie,
nie wyprowadzi się przy żadnej gramatyce,
a policzony jako odrzucony mierzyłby ten krok zamiast podzbioru.
Dlatego `olski-check` ma na niego werdykt `fragment` obok `rejected`,
i dlatego [przebieg nad prozą tego repozytorium](roadmap.md#readme-jest-przyrządem-pomiarowym)
liczy jedno osobno od drugiego.

Jedna klasa napisów bez tego znaku aparatem jednak nie jest
i dostaje werdykt `unclosed` obok tamtych dwóch:
napis, który olski czyta, kiedy się go domknie.
Werdykt ten mówi o napisie, a nie o autorze, i musi tak być,
bo nagłówek bywa zdaniem po domknięciu, a kropki mieć nie może;
skąd napis przyszedł, wie dokument, a nie napis.
Autor prozy czyta więc ten werdykt jako brakującą kropkę,
a pomiar podzbioru nie liczy takiego napisu do mianownika tak samo jak fragmentu,
bo domknięcia nie postawił nikt.

Werdykt, a nie ciche pominięcie przy podziale.
Przebieg, który zwęża sobie mianownik i nic o tym nie mówi,
jest tym, czego
[sprawdzenie ról](corpus.md#agreement-which-matters-more-than-acceptance)
odmawia po swojej stronie,
i dlatego liczba fragmentów stoi w podsumowaniu obok liczby zdań.

Klasa jest szeroka i należy do rejestru, a nie do jednego repozytorium.
Nad korpusem audytowym `olski-check` liczy 1535 zdań
i 1380 fragmentów obok nich:
1054 na 2322 nad `ksef-docs` i 326 na 593 nad `rit-dokumentacja`.
Są tam ścieżki końcówek API i zapowiedzi zakończone dwukropkiem,
a obok nich pozycje listy, które ciągną zdanie zaczęte w wierszu nad sobą
i kropkę zostawiają dopiero ostatniej z nich.

W drugą stronę ta sama granica dokłada zdanie, którego nikt nie napisał.
Zawartość spanu kodu wychodzi stąd dosłownie,
więc kropka w jego środku punktuje prozę wokół niego,
a zdanie z przykładem zamkniętym kropką
dochodzi do olskiego jako dwa, z których drugie zaczyna się małą literą.
Poprawka należy do zdania, a nie do tego kroku,
bo kropka w spanie kodu jest znakiem, który ktoś napisał,
i nic tutaj nie odgadnie, że nie kończy ona zdania.
Dlatego przykład cytowany w środku zdania stoi bez kropki,
jak `Koszt samej szynki przewyższa koszt szynki z dodatkami` w README,
a blok pod tym zdaniem pokazuje go tak, jak olski go czyta.

## Where the prose parts from the page

Two things stand in one and not in the other,
and neither is the parser failing to recognize a construct:
one is a rule about notes and one is a decision about apparatus.

- **A link list something interrupts.**
  The trailing list goes only while every item opens with a link,
  so a note whose index has a reviewer's aside or a question in the middle of it
  keeps the entries standing above the interruption.
  16 of the notes are written that way.
- **Text inside a raw HTML block.**
  A renderer shows what a `<summary>` holds and this drops it with the block,
  because a block of raw HTML is markup by the paragraph rather than by the tag
  and nothing here would tell one from the other.
  What that costs is words rather than a class of hit:
  an inline `<br>` and `<font>` drop as apparatus,
  which is what they render as.

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
python3 -m harness.markdown rit-dokumentacja --into proza/rit

python3 -m olski.check $(find proza/notes -name '*.txt')
python3 -m olski.check $(find proza/ksef -name '*.txt')
python3 -m olski.check $(find proza/rit -name '*.txt')
```

`ksef-docs` and `rit-dokumentacja` arrive by the command
[audit-corpus.md](audit-corpus.md#the-list) prints,
which pins them at the commits the columns above were measured at.
The last line of what `olski-check` prints is the count of fragments
the section above quotes,
and `find` is in front of it because that command takes files and not a tree.

The memoir is the nine chapters of `the-agent/book`:
`prolog.md`, `epilog.md` and `rozdzial-01` through `rozdzial-07`.
The comparison column is the same corpus with `.md` renamed to `.txt`.
The counts of single marks beside it — the dashes, the Polish quotation marks —
were taken with a pack of counting rules that went with the linter,
so those columns are figures this repository no longer has a command for.

Markdown is the only format this reads,
and the corpora that come in others still reach their figures by hand:
[corpora.md](corpora.md#how-the-counts-here-were-taken)
says which of them that is,
and [TODO.md](../TODO.md) holds what to do about it.
