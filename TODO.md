# Work to do in the repository

The running list of work inside the repository itself:
rewrites, merges, documents that have drifted apart,
dangling references, gaps, and code worth improving.
Something noticed while working on another topic lands here
instead of stretching the current change or being forgotten.
The second inflow is [the review pass](CLAUDE.md#the-review-pass):
a refactor too large to do on the spot comes down to this list,
and the review also checks whether a change deleted the entries it closes.
Look here before starting new work —
the list doubles as a map of the places that sag.

An entry belongs here only if a commit in this repository closes it.
A question the outside world answers —
a measurement, which human Polish counts as the good half of the corpus,
a fork not yet taken —
is not work in the repository,
and the document that owns the topic keeps it:
[`docs/open-questions.md`](docs/open-questions.md)
or a document's own `Not yet decided`.
The next move is the tell:
waiting for somebody else's answer is an entry there,
a file to write is an entry here.

A register, not a changelog:
an entry that closes, or that turns out to have been misjudged,
is deleted by the same commit that settles it,
which is the done-marker rule from
[`CLAUDE.md`](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
applied to this file.

One paragraph per entry, paragraphs separated by a blank line,
without bullets, numbering or headings,
so that adding or removing an entry gives a clean diff
and leaves its neighbours alone.
Inside a paragraph the lines break
[semantically](CLAUDE.md#semantic-line-breaks).
Write so that the entry can be picked up cold,
and name the concrete next move —
what actually has to change in the text or in the code.
"Check some day" is a hope, not a move.

An entry names the evidence it has to read,
and not only the files it changes.
Two entries can edit disjoint files
and still turn on one judgment about one body of text,
such as what a rule's hits over a corpus are.
A file list does not show that overlap,
so the two are picked up together
and the judgment is reached twice.

Wpis nie jest rozstrzygnięciem.
Po to ta lista jest: kto go pisał, siedział wtedy przy czymś innym,
a notatka dostała tyle uwagi, ile zostało.
Pewne jest w takim wpisie to, że autor na coś trafił,
a nie to, że dobrze zgadł, co z tym zrobić.
Kto wpis podnosi, dochodzi więc do ruchu sam:
zaczyna od dowodu, który wpis nazywa,
a nazwany ruch czyta jako propozycję, a nie jako polecenie.
Wychodzi z tego czasem ruch inny niż nazwany, a czasem żaden,
bo problemu nie ma albo naprawa kosztuje więcej niż to, co kupuje.
Wtedy całą zmianą jest skasowanie wpisu,
tak samo jak przy wpisie, który się zamknął,
z powodem w komunikacie commita,
bo skasowany wpis nie zostawia po sobie nic innego.

A one-character emphasis span swallows the next one and leaves a marker behind.
The optional tail in `INLINE` in `harness/markdown.py`,
`(?:.*?[^\s*])?` inside the emphasis alternative, is greedy,
so it prefers a body of three characters or more to a body of one,
and `*p*, a razem z nim *p*` extracts as `p*, a razem z nim *p`
where a renderer sets two emphases.
The stray marker is the failure the module was written against,
since it reaches the rules as a character somebody typed,
and the same tail sits in all five wrapping alternatives,
`**`, `__`, `~~`, `*` and `_`, each of which swallows the next span of its kind.
The move is to make those five tails lazy, `??` rather than `?`,
which leaves every span of two characters or more matching as it does now,
with a case in `tests/test_extraction.py`
for two spans of one character in one paragraph.
It is its own change because it moves what the extraction keeps,
so the figures in
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over),
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken),
[`docs/firing-rates.md`](docs/firing-rates.md#the-rates)
and [`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match)
are rerun with it.
The evidence to read is how often the pattern occurs in those corpora at all:
no document in this repository emphasizes two single characters in one paragraph,
and if the corpora hold nothing like it either the rerun returns the same tables.

A triple-backtick code span opening a line is read as a code fence,
and `harness/markdown.py` then drops the prose down to the next fence-only line.
`FENCE` in that module matches ```` ``` ```` and takes the rest of the line
as an info string,
where CommonMark forbids a backtick inside a backtick fence's info string,
so ```` ```KOD I``` zawiera link ```` is a paragraph to a renderer
and an opening fence to the extraction.
Three of the 32 `ksef-docs` files are written that way,
`kody-qr.md`, `tokeny-ksef.md` and `uwierzytelnianie.md`,
and between them they lose the better part of a thousand words
of running Polish;
[the corpus](docs/firing-rates.md#the-audit-corpus) owns how much exactly,
and reports its figures as the corpus stands.
The move is the CommonMark condition in `FENCE`,
plus the closing-fence test that goes with it,
and then rerunning the four sets of tables that hold extracted figures:
[`docs/audit-corpus.md`](docs/audit-corpus.md#the-list),
[`docs/extraction.md`](docs/extraction.md#an-inline-construct-leaves-its-text-or-takes-the-space-with-it),
[`docs/firing-rates.md`](docs/firing-rates.md#the-rates)
and [`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match).
The evidence to read is the prose the three `ksef-docs` files extract to,
since the fix is only worth the rerun if what comes back is Polish
rather than more of the code the fence was swallowing.

The line that says what a walk went past counts a repository's `.git` with it.
`_collect` in `olski/cli.py` reaches every file under a named directory,
so `olski rit-dokumentacja/` reports going past 39 files
in `.sample`, no suffix, `.md`, `.png`, `.idx`, `.pack` and `.rev`,
where the 7 Markdown files are the only ones a reader would have guessed at
and the pack and index files are git's own.
The walk always descended there and the count is what made it visible,
which is the warning working rather than a second defect.
The move is for the walk to skip a directory whose name begins with a dot,
and to say in `_collect` that a repository is the expected input
and its version control is not part of the corpus.
Against it: a dotted directory somebody names outright is then unreachable,
so the skip belongs to the walk and not to the suffix test.

Nothing in the harness says which construct a finding came out of,
so every audit of extracted prose maps its hits back by hand.
`docs/extraction.md` did it for a couple of hundred spacing findings,
and [the audit corpus's tables](docs/firing-rates.md#what-the-hits-over-the-audit-corpus-turned-out-to-be)
for more than a thousand hits,
both with a throwaway script and neither with anything reusable.
The classes that cost the most to reach are the ones a program could settle:
whether a hit stands in a table, a code span, a link's text or a raw tag.
So the move is for `prose` in `harness/markdown.py`
to record what each stretch of output came from,
and for something to print that beside a finding —
which is a second output from the extraction
and wants deciding whether it rides along with the prose files
or is a separate mode over one document.
Against it: the classes that decide whether a hit is a *defect*
are the ones needing a reader anyway,
so this halves an audit rather than removing it,
and a corpus of this size can be read by hand, as it twice already has been.

`docs/extraction.md` compares one member of the audit corpus against its files
and the corpus has two.
Its table runs the notes, the memoir and `ksef-docs` twice each,
where [`docs/firing-rates.md`](docs/firing-rates.md#the-audit-corpus)
audits `rit-dokumentacja` beside `ksef-docs`
and finds the extraction's own gaps accounting for 553 of the corpus's findings,
every one of them in that second member.
The move is a fourth column,
which means running `rit-dokumentacja` with its names changed to `.txt`
and checking the spacing findings one by one against their source
the way the section's own method demands,
since a count that agrees is not yet a hit that points at the same place.

Only one of the corpora in
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken)
reaches the rules through a program this repository holds.
`harness/markdown.py` reads Markdown,
which is what the KSeF figures there are taken with,
while NKJP is XML, Śmigiel is JSONL,
`python-docs-pl` is PO files and Wolne Lektury is plain-text exports,
so every figure over those is still counted by hand.
One of the four needs no extraction at all,
since a text export is what olski reads,
and what it needs instead is a selection anybody can repeat:
the Wolne Lektury count in that document
runs over "the first forty `Epika` entries the catalogue returns",
which is not an order to rerun into.
[`docs/firing-rates.md`](docs/firing-rates.md#wolne-lektury)
already fetches the same library by naming every slug it takes,
so that half is a rewrite of one paragraph rather than a program.
The move is to decide, per corpus, whether it joins the harness
as an extraction beside the Markdown one,
as a fetch-and-select command in the document that cites it,
or not at all because the survey has already ruled the corpus out.

Two rules read where a line ends, and the target register has no such line.
`trailing-space` and `orphan-single-letter-word` are both audit-shaped,
so each owes the share of its hits that were real defects,
and [the roadmap](docs/roadmap.md#milestone-1-the-calibration-harness)
records that neither corpus
[`docs/corpora.md`](docs/corpora.md#the-composition-this-argues-for) argues for
can supply that share.
The pack half-admits the mismatch already:
`trailing-space` justifies itself on whitespace
that changes nothing about the rendered text,
and two trailing spaces in Markdown are a line break.
So the decision comes before either fix below,
and it is whether the pack claims prose laid out in lines as a register of its own
or the two rules go.
The evidence is three readings already taken:
the audits over
[published Polish](docs/firing-rates.md#orphan-single-letter-word-reads-one-stratum-of-the-three)
and over
[the audit corpus](docs/firing-rates.md#orphan-single-letter-word-declines-all-39-files),
which between them turn up no instance of the defect in either body
and no hit at all in the one stratum where the premise held,
and [what the extraction removes](docs/extraction.md#after-joining-a-line-end-rule-has-nothing-left-to-read),
which for these two rules is every trailing space and every line end there was.
Deleting them frees machinery on one side,
which is the other half of what the decision is worth:
the `line-end-word` check kind, `needs_hard_wrap` in `olski/checks.py`,
and `hard_wrapped` and `HARD_WRAP_SHARE` in `olski/document.py`
exist for `orphan-single-letter-word` and for nothing else,
where `trailing-space` is a `pattern` rule and would leave nothing behind.
Two known misreadings of it follow the decision the other way
and are worth fixing only if the rule stays.
`_last_word` in `olski/checks.py` matches `[^\W\d_]+` of its own
where `WORD` in `olski/document.py` keeps an apostrophe inside a word,
so `Lagrange'a` ends in the word `a`,
and the move is for `_last_word` to take the last `WORD` match instead.
That leaves the class beside it standing:
`w.` for *wiek* is the word `w` and a full stop,
`ABBREVIATIONS` in `olski/document.py` does not list `w.`,
and whoever takes this settles whether the abbreviation test belongs to the check
or to the word notion both of them would then share.
The other is that a line whose end is a paragraph's end
has nothing after it for a word to be separated from,
which `Document.paragraphs` already holds the spans to skip.
No figure moves for that one,
since the rule fires nought times over the one stratum it reads,
so what it buys is the class not returning
the first time somebody points the rule at prose wrapped to a width.

A run says which files a format made a rule decline, and not which ones the text did.
`_note_markup` in `olski/cli.py` prints one line
when a whole-file rule declined on a file in a format olski does not read,
because a run over Markdown would otherwise read as a run over prose
that happened to find less.
A precondition on the text is followed by the same silence:
`olski powiesc.txt` over a paragraph-per-line export
prints no line-end finding and no notice,
and only `--format report` shows that nothing was measured.
The move is a decision about how much the default mode says —
a notice for every precondition a run tripped,
which is `--show-abstentions` in summary,
or the format notice alone,
on the grounds that a reader can see the shape of their own file
and cannot see what a suffix promised on its behalf.

`docs/corpus.md` and `docs/corpora.md` differ by two letters
and hold unrelated things:
the first measures the grammar against the Składnica treebank,
the second surveys the corpora the linter would calibrate against.
A link to either one reads the same,
and a grep for one of them finds both,
and finds `docs/audit-corpus.md` too,
which is about one of the corpora the second surveys.
The move is to rename `docs/corpus.md` to `docs/skladnica.md`,
which says what it holds and matches `docs/swigra.md` beside it,
and to carry the rename through
`CLAUDE.md`, `README.md`, this file,
`docs/design-notes.md`, `docs/prior-art.md`, `docs/subset.md`, `docs/swigra.md`,
and the citations in `olski/corpus.py`, `olski/coverage.py`, `olski/subset.py`
and `tests/test_subset.py`.
`tests/test_docs.py` catches the Markdown links and the citations in code,
and nothing catches the plain-prose mentions,
so those are the ones to grep for.
The package has the same collision twice over and the same argument settles it.
`olski/check.py` is the grammar command
and `olski/checks.py` is the linter's check kinds,
one letter apart and on opposite tracks:
[`docs/roles.md`](docs/roles.md) sends the grammar reader to the first
and [`docs/rules.md`](docs/rules.md#check-kinds) sends the rule author to the second,
and the two already stand a few lines apart in this file.
`olski-corpus` is the third: it runs `olski/coverage.py`,
where `olski/corpus.py` is the treebank reader beside it,
so the command, the module and the document
are three names for what a reader takes to be one thing.
Renaming the document alone leaves both of those in place,
which is why they are one entry:
what has to be decided is what these things are called,
and the answer for the document is the answer for the module and the command.

The check table in `docs/rules.md` copies data owned by `olski/checks.py`.
Its `Reports` column restates what each check's `fields` answers,
and the `params=dict(...)` blocks restate what each validator accepts,
so both drift silently as soon as a check gains a parameter.
`fields` is a function of a rule's validated parameters,
which the `pattern-density` row carries as a condition in prose,
so whichever move is picked reaches a check's fields through some rule's parameters.
Either the CLI grows a `--list-checks` output that the document points at,
the way it already points readers at `--list-rules`,
or the table stays hand-written and a test asserts it against `CHECKS`,
the way `tests/test_docs.py` holds the links in the prose.
Pick one and the document stops being a second copy.

`Document` computes an analysis nobody asked for
and recomputes one everybody does.
`from_text` in `olski/document.py` splits paragraphs and sentences
for every document it builds,
where a run selecting only `pattern` rules reads neither,
and `word_count` runs `WORD.finditer` afresh on every call
from the three sites in `olski/checks.py` that reach for it,
once per rule and once per scope.
Neither costs much while every analysis here is a regex pass over the text.
Both are the shape the first expensive tier arrives in:
[the roadmap](docs/roadmap.md#milestone-5-morphology-binding-and-the-rules-that-needed-it)
puts an analyser behind a lemma rule,
and a typography run paying for morphology over a corpus
is this eagerness with a number attached.
The move is to make the analyses lazy and memoized
rather than fields set at construction,
which `functools.cached_property` does on a frozen dataclass,
since freezing replaces `__setattr__`
and the descriptor writes the instance dictionary directly.
The reason to make it before the analyser rather than alongside one:
the same change made afterwards
has to be made through whatever wired the analyser in.
A second reason arrived with `hard_wrapped`,
which is a precondition computed from `paragraphs`:
a `Document` built by its constructor rather than by `from_text`
has that field empty and answers the precondition falsely,
so a rule declines a file nobody said anything wrong about.
Only tests build one that way today,
and a lazy analysis is what stops the half-built state from existing at all.

`olski-corpus` asks Składnica whether a sentence derives at all,
where the same treebank supports a sharper question.
Świgra's evaluation walks its packed forest per sentence
and counts the trees consistent with the corpus disambiguation
(see [`docs/swigra.md`](docs/swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)),
so coverage becomes whether the gold reading is among the readings
and how deeply it is buried,
rather than whether anything came out at all.
This is ordered behind the chart parser
that the implementation note in `olski/parse.py` defers,
because the enumerator builds no forest to walk
and caps enumeration at `MAX_READINGS`,
which is exactly the tail a burial-depth number would be measuring.

The archives these documents send a reader to fetch are pinned by URL and by nothing else.
[Składnica](docs/corpus.md#fetching-it)
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
name a release in the query string of a wiki attachment,
and Świgra is `swigra_current.zip`, which names none,
so [`docs/swigra.md`](docs/swigra.md#what-was-read-and-what-was-not)
dates it by the timestamps of the files inside instead.
[The audit corpus](docs/audit-corpus.md#the-list) pins its members to a commit
and says what a pin is for:
so that a second person fetches the same bytes.
The archives make that promise
and give a reader no way to hold anyone to it.
The move is `sha256sum` over each one,
with the digest beside the command that fetches it,
which turns a substitution upstream into a failed check
rather than a figure that quietly stops reproducing.

The corpora these documents send a reader to fetch
come from hosts that gain nothing by serving them,
once per session rather than once per person,
because a Claude Code session on the web starts from an empty container.
[The Wolne Lektury run](docs/firing-rates.md#wolne-lektury)
takes 326 files at one request each from a volunteer library,
[Składnica](docs/corpus.md#fetching-it) is 92 MB
that [the checks](CLAUDE.md#checks) make a condition of touching the grammar,
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
is a tarball from the institute that serves Składnica.
The licences do not run in that order.
NKJP carries CC BY, which permits the redistribution a mirror is,
every Wolne Lektury file ships the library's licence in its own tail,
which that run cuts off before counting,
and Składnica is GPL,
which the fetching section raises against vendoring
and which settles nothing about mirroring,
since a mirror redistributes under Składnica's terms
whatever this repository decides about its own.
So the order of work is NKJP, Wolne Lektury, Składnica,
and the transport is the smaller half of each.
A release asset on a mirror repository holds 2 GB per file against no quota
and keeps the fetch the `curl -L` those sections print,
where git LFS asks for an install that the session clone precedes,
so tracked files arrive as pointer files and a hook has to pull them,
and spends an allowance that GitHub's billing documentation puts at
1 GB stored and 1 GB of bandwidth a month,
which is ten fetches of Składnica.
LFS buys that back over a binary somebody versions,
and these are frozen archives.
The audit corpus needs none of it,
being clones pinned to a commit, which is what a mirror would be.
None of this starts before the entry on digests,
since a mirror nobody can check against upstream
is the second copy of a fact that
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely) warns about.

The repository ships no licence.
`pyproject.toml` carries no `license` field and there is no `LICENSE` file,
so the terms under which any of this may be used are unstated.
The move is to pick one, add the file,
and set `license` in `pyproject.toml` to match.
Reading a GPL v3 parser of Polish is what raised it
(see [`docs/swigra.md`](docs/swigra.md#why-wrapping-it-does-not-get-there)),
and the answer decides whether olski could ever link against such a thing.

[Semantic line breaks](CLAUDE.md#semantic-line-breaks) cover
"prose in comments and docstrings", and no module here writes them that way.
Every file in `olski/` and `harness/` wraps its comments to a column instead,
so the rule and the code have disagreed for as long as both have existed
and a new docstring following the rule reads as a typo beside its neighbours.
Two ways out, and the choice is a judgement about the whole package
rather than about whichever function is being edited at the time:
narrow the rule in `CLAUDE.md` to Markdown, commit messages
and the prose fields of a declaration,
which is where the tighter diff is actually collected,
or keep the rule and reflow the docstrings under
[lazy adoption](CLAUDE.md#adopt-these-rules-lazily), file by file as they are touched.
The second answer also needs saying out loud,
because the mixed state it passes through is what a reader will read as drift.

`olski-check` nie mówi, na czym zdanie stanęło, a `olski-corpus` mówi.
`Outcome.blocker` w `olski/coverage.py` nazywa część mowy tokenu,
na którym rozbiór się zatrzymał, i `Report.blockers` z tego rankuje kolejkę,
gdzie `Verdict` w `olski/subset.py` ma na odrzucenie jedno zdanie:
`no reading: nothing in olski derives this`.
Obie drogi wołają ten sam parser,
więc różnica jest w tym, co która z nich z niego wyjmuje, a nie w tym, co widzi.
Kolejność, w jakiej README ustawia braki gramatyki, z tego polecenia więc nie wychodzi:
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)
opisuje ją jako listę słów, których żadna produkcja nie bierze,
a [kryterium wyjścia toru](docs/roadmap.md#celem-toru-jest-to-readme)
każe ten sam przebieg powtarzać po każdej zmianie w gramatyce.
Ruchem jest zejście `blocker` na `Result` w `olski/parse.py`,
tak jak zeszedł tam `status`, który stał w obu klasach w dwóch kopiach,
plus segmenty, których `Verdict` nie niesie, a `blocker` ich potrzebuje,
i wypisanie rankingu przez `olski-check` nad plikiem.
Do przeczytania jest to, czy blocker liczony nad żywą morfologią
mówi cokolwiek ponad to, co mówi lista form nieznanych:
`docs/corpus.md` ostrzega, że przy wielu czytaniach formy
blocker nazywa pierwsze z nich,
a nad dokumentacją nikt czytań nie ujednoznacznia,
więc blocker jest tam zawsze tym przybliżonym.

A modifier between the subject and the verb has nowhere to go but the subject.
`Chałka pod względem smaku przewyższa zwykłą bułkę.` comes out `valid`
with the taste made part of the challah,
because `NPConjunct → subst Modifier` is the only rule
that can take a phrase in that position
and the clause rules have no slot there.
That is the narrowness
[`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)
already caught on `Przybysze z najnowszej fali na ogół`,
reached from the other side:
a fronted modifier now has a rule of its own and a preverbal one does not.
The move is a `ClauseConjunct → Subject Modifier Predicate` rule,
which turns those sentences from silently wrong into honestly ambiguous.
What has to be read before taking it is the same run both ways:
what the rule does to the accepted count
and to the four disagreements in that table,
since the sentences it costs are ones olski accepts today.

`olski` chodzi po katalogu, a `olski-check` bierze tylko pliki.
`_collect` w `olski/cli.py` schodzi po `rglob`, pyta `is_plain_text` o każdy plik
i liczy to, co minął, żeby przebieg nad katalogiem nie lintował licencji,
a `main` w `olski/check.py` czyta po prostu każdą podaną ścieżkę.
Widać to w poleceniu, którym
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów: stoi przed nim `find`, bo inaczej nie ma czego podać.
Ruchem jest wyjęcie `_collect` z `olski/cli.py` do wspólnego miejsca
i zawołanie go z obu komend, po czym `find` z tamtego polecenia znika.
Do rozstrzygnięcia jest to, co druga komenda robi z pominiętymi:
`olski` mówi o nich, bo pominięcie zmienia mianownik częstości,
a `olski-check` ma już mianownik, o który się w tej sesji rozegrało,
więc nie jest oczywiste, czy to jest ta sama notatka, czy druga obok niej.

Przecinek stoi na czele kolejki i sam nie kupuje nic.
`interp` prowadzi [tabelę blokerów](docs/corpus.md#where-the-analyses-stop),
przecinek jest w tym wierszu drugą formą po pauzie,
a pauza należy do rejestru, którego dokumentacja nie ma,
więc to przecinek jest tym, co ta tabela naprawdę stawia jako następne.
Ruchem jest koordynacja przecinkiem tam, gdzie stoi dziś spójnik:
`Clause`, `NP` i `AP` mają każde swoją produkcję ze spójnikiem
i żadne nie ma jej z przecinkiem.
Przeczytane jest to, co te trzy produkcje robią nad prozą wyciągniętą z README,
i nie robią nic:
zdanie, które niesie w tym pliku przecinek,
niesie też zdanie podrzędne, przysłówek albo rzeczownik odczasownikowy,
więc reguła sama z siebie nie wyprowadzi tam ani jednego zdania
i wchodzi razem z podrzędnym albo nie wchodzi wcale.
Jest to własność całej kolejki, a nie tej jednej reguły,
i pomiar nad czterema pozostałymi konstrukcjami trzyma
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop).
Do przeczytania zostaje cena nad Składnicą,
bo przecinek między zdaniami konkuruje z przecinkiem w grupie imiennej
wszędzie tam, gdzie po przecinku stoi rzeczownik,
a to jest ta wieloznaczność, której olski nie znosi.

Jedna forma o dwóch czytaniach nominalnych daje olskiemu dwa czytania zdania.
`wejście` ma w Morfeuszu czytanie `subst` i czytanie `ger`,
a sygnatura czytania w `olski/parse.py` rozróżnia części mowy,
więc produkcja z `ger` w głowie grupy imiennej
daje `Wejściem jest zwykły tekst polski.` drugie czytanie tego samego kształtu
i zabiera jedno z tych zdań, które olski dziś przyjmuje;
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop) mierzy ten spadek.
Rozstrzygnąć da się w dwóch miejscach i wybrać trzeba jedno.
Albo `admissible` w `olski/subset.py`,
które dziś żąda czytania funkcyjnego obok rzeczownikowego
i tej pary nie obejmuje, dostaje drugie kryterium.
Albo sygnatura przestaje liczyć część mowy tam, gdzie kształt drzewa jest ten sam,
co jest tym samym argumentem, którym już pomija lematy,
i wtedy `do` jako przyimek i jako nuta dalej są dwoma czytaniami,
bo różnią się kształtem.
Do przeczytania jest, ile takich par ten rejestr niesie:
formy z czytaniem `ger` i `subst` naraz
nad prozą wyciągniętą z dokumentów tego repozytorium,
bo jedno zdanie nie mówi, które z dwóch wyjść jest warte swojej maszynerii.
Wpis stoi przed rzeczownikiem odczasownikowym w gramatyce, a nie za nim,
bo reguła dodana pierwsza obniża pokrycie
i sesja, która ją doda, zmierzy spadek zamiast zysku.

Part of what [`docs/corpus.md`](docs/corpus.md) quotes has no command behind it.
`olski-corpus` prints the verdict tables, the length curve
and the blocker ranking by part of speech,
while the commonest forms under each blocker,
the count of sentences the two runs both accept,
and the column with `admissible` switched off
come from scripts written for one session and thrown away.
So a change to the grammar updates the tables that have a command
and silently leaves the rest stale,
which is the failure the rerun rule in
[`CLAUDE.md`](CLAUDE.md#checks) exists to prevent.
The move is in `olski/coverage.py`:
carry the blocking form beside its part of speech in `Report.blockers`,
add the exclusion-free morphology as a third `SOURCES` entry,
and let the CLI take two runs and print what they disagree about.
That last part has a second caller,
so it should not be tied to the morphology sources:
a point on [the coverage curve](docs/design-notes.md#making-the-trade-measurable)
is a net of what a tier buys against what it costs in uniqueness,
which is two grammars disagreeing rather than two morphologies.
The section that owns the reproduction path says meanwhile which figures are hand-taken,
and that sentence goes when the commands cover them.

`missing-space-after-punctuation` reads the colon of a label such as `**Exit:**`
in [`docs/roadmap.md`](docs/roadmap.md#milestone-4-the-delivery-decision)
as a missing space,
because that colon stands in front of an emphasis marker rather than a word.
Either the documents settle on a label that leaves no mark inside the emphasis,
which is what [`docs/roles.md`](docs/roles.md) does
by opening the sentence with the bold phrase itself,
or the rule gets an exemption for an emphasis marker after the mark,
which is what its own audit argues for:
markup accounts for the large majority of its hits over both corpora,
counted in
[`docs/firing-rates.md`](docs/firing-rates.md#missing-space-after-punctuation-mostly-read-an-emphasis-marker).
The exemption is the more expensive of the two,
because it moves what the rule's hits are
and so drags the rerun [`CLAUDE.md`](CLAUDE.md#checks) demands
over both corpora and over the classes that document reports having read.

The booster stems are the last pattern
[milestone 2](docs/roadmap.md#milestone-2-the-plain-polish-pack-without-an-analyser)
rests on that nothing has been run over,
and `harness/endings.py` does not reach them as it stands.
A `Probe` there matches with `endswith`,
where `kluczow` and `istotn` are what a word begins with,
so either the declaration grows a matching side beside the classes it carries,
or the boosters get a run of their own and this module stays about endings.
The choice is worth making on the classes rather than on the matching,
which is the cheaper half and the one the two probes there settle by example:
each of them turns on a tag, `ger` and `imps`,
and a booster's question is whether an adjective is doing any work,
which no tag answers and which
[the nominalization probe](docs/linter.md#what-the-nominalization-endings-match)
already shows a run can come back undecidable on.
So the run to write first is the one that says
how much of what the stems match is the adjective at all,
and it belongs in front of the rules rather than after them,
because what it decides is whether the rule exists rather than how it is tuned.

The `verb` class of `NOMINALIZATION` in `harness/endings.py`
stands before every nominal one,
which is right for `zostanie` and wrong for `dacie`.
Both carry a verb reading beside a nominal one,
and a document dating an invoice means the locative of `data`
where the order files the second person plural of `dać`,
so the inflected share quoted in
[`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match)
is a floor and not a count.
The move is either an order the corpus settles —
the nominal reading first where the verb reading is a person the register does not use —
or the floor stated wherever the share is quoted,
which is that section alone,
the roadmap having taken the same finding coarsely and quoted no number.
The evidence is 7 words: 6 `dacie` and 1 `powiecie`,
both of which the register uses as nouns.

Granica harnessu jest napisana raz, a stosuje się dwa razy inaczej.
`harness/__init__.py` mówi, że korpus w formacie znacznikowym
dochodzi do reguł tędy, a nie przez `olski`,
a `harness/endings.py` dokłada, że stoi tam,
bo o polszczyźnie niczego nie twierdzi.
Oba kryteria trafiają w `olski/corpus.py`, który czyta XML Składnicy,
i w `olski/coverage.py`, który mierzy nim gramatykę
i produkuje tabele [`docs/corpus.md`](docs/corpus.md).
Oba są liśćmi — w `olski` nikt ich nie importuje poza nimi samymi —
a mimo to instalują się z pakietem (`include = ["olski*"]` w `pyproject.toml`)
i jeden z nich ma własną komendę,
gdzie tak samo pomiarowe programy toru linterowego
nie mają ani instalacji, ani komendy.
Ruchem jest rozstrzygnięcie granicy, a nie przeniesienie plików:
albo obie idą do `harness/`, a `olski-corpus` staje się
`python3 -m harness.coverage` jak dwie pozostałe komendy pomiarowe,
co przepisuje polecenia w [`docs/corpus.md`](docs/corpus.md#fetching-it)
i w [sekcji Checks](CLAUDE.md#checks),
albo `harness/__init__.py` mówi, że jest harnessem toru linterowego,
co nie kosztuje nic i przestaje odpowiadać dwa razy.
Do przeczytania jest to, co pakiet ma dawać temu, kto go instaluje:
czytnik banku drzew i program pomiarowy są w nim dziś,
a nikt, kto lintuje tekst, ich nie woła.

`docs/linter.md` jest i wywodem, i kolejką reguł, a kod wskazuje na kolejkę.
Każda z dziewięciu reguł pakietu typograficznego ma w `sources`
`docs/linter.md#typography-tier-a`, czyli podsekcję inwentarza kandydatów,
więc `--explain` odsyła czytelnika do najdłuższego pliku w repozytorium,
a [`docs/roles.md`](docs/roles.md) posyła tam autora reguły
po następną pozycję do zrobienia.
Ruchem jest wyjęcie inwentarza do własnego dokumentu,
który README wymienia, `sources` cytują,
a `docs/linter.md` streszcza zdaniem i linkuje —
tak jak dziś streszcza [`docs/prose-linters.md`](docs/prose-linters.md)
i [`docs/fiction.md`](docs/fiction.md).
Zostaje wtedy wywód, po który reszta dokumentów naprawdę tam chodzi.
`tests/test_docs.py` łapie linki i cytowania z kodu,
więc kosztem jest przecelowanie ich, a nie znalezienie.
Do przeczytania jest, co jeszcze jest inwentarzem, a nie wywodem:
lista reguł lintowalnych w prozie literackiej
stoi poza sekcją inwentarza i jest taką samą listą kandydatów.

`docs/open-questions.md` trzyma listę decyzji zamkniętych,
a każda z nich ma właściciela gdzie indziej.
Sekcja `Settled` powtarza cel roboczy (README i [`docs/linter.md`](docs/linter.md)),
opcjonalność toru gramatycznego wraz z kryterium wyjścia
([`docs/roadmap.md`](docs/roadmap.md#celem-toru-jest-to-readme)),
bliskość polszczyzny
([`docs/design-notes.md`](docs/design-notes.md#decisions-taken)),
kalibrację
([`docs/linter.md`](docs/linter.md#the-thing-that-makes-or-breaks-it-calibration)),
to, że narzędzie nie jest detektorem
([`docs/linter.md`](docs/linter.md#limits-worth-stating-up-front)),
i dwa słowniki do dwóch zadań,
czyli tę jedną decyzję, przy której `docs/design-notes.md` pisze wprost,
że nie jest zapisana dwa razy.
Ruchem jest usunięcie sekcji na rzecz zdania mówiącego, gdzie decyzje zapadłe stoją,
czyli [zakaz znaczników zrobionego](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
zastosowany do listy otwartych pytań.
Przeciw: lista zamkniętych rozwidleń oszczędza komuś otwierania ich z powrotem.
Do przeczytania jest więc, czy któraś pozycja niesie odrzuconą alternatywę,
której jej właściciel nie trzyma — taka zostaje, a reszta idzie.

Kształty kalibracji są jednym faktem rozciętym kierunkiem importu.
`olski/checks.py` trzyma `AUDIT` i `DISTRIBUTION` jako gołe napisy,
z komentarzem, że check nie może wiedzieć, czym jest reguła,
a `olski/rules.py` mapuje te same dwie nazwy z powrotem
na klasy (`SHAPES`) i na zdania (`OWED`).
Kalibracja regułą nie jest, więc ta przeszkoda jest do zdjęcia:
osobny moduł z `Uncalibrated`, `Measurement`, `Audit`, `Distribution` i `OWED`
pozwala checkowi nazwać kształt wprost,
a `olski/rules.py` zostaje przy deklaracji reguły.
Jest to ta [rozdwojona ścieżka](CLAUDE.md#code), którą repozytorium każe scalać.
Ruch opłaca się przed milestone'em 1, a nie po nim,
bo to jest miejsce, w które ten milestone pisze:
[harness kalibracyjny](docs/roadmap.md#milestone-1-the-calibration-harness)
zastępuje `UNCALIBRATED` jedną z tych dwóch klas,
więc każda dostanie wtedy pola, których dziś nie ma.

Lista dokumentów w README miesza dwa tory, które sekcja nad nią rozdziela.
[`Co działa`](README.md#co-działa) mówi, że działają dwie rzeczy,
a lista pod nią ma dziewiętnaście pozycji bez podziału,
więc czytelnik toru gramatycznego i autor reguły
przechodzą przez cudze pozycje, zanim dojdą do swoich.
Ruchem jest pogrupowanie listy — tor linterowy, tor gramatyczny
i to, co obsługuje oba — bez ruszania linków,
czyli najtańsza zmiana, jaką ta lista przyjmie.
Przeciw katalogom w `docs/`: przepisałyby każdy link względny po to,
żeby dać indeks, którym ta lista już jest.
Do rozstrzygnięcia jest, gdzie idą pozycje graniczne,
bo [`docs/roles.md`](docs/roles.md), [`docs/roadmap.md`](docs/roadmap.md)
i [`docs/open-questions.md`](docs/open-questions.md) obsługują oba tory.
Etykiety grup nie ruszą `test_every_document_is_listed_in_the_readme`,
który czyta pozycje wzorcem `^- [docs/…]` i nie patrzy, co stoi między nimi.
