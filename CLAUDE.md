# Notes for AI agents

This is the whole convention for working in this repository:
how prose is written, how code and tests are written,
which checks to run, the git traps this repository has actually hit,
and the review pass.
There is no separate contributor guide;
this file is the only copy.

The prose rules cover the README, everything under `docs/`,
`TODO.md`, the `justification` fields of rule declarations
(see [`docs/rules.md`](docs/rules.md)),
commit messages, and pull request descriptions.

## Adopt these rules lazily

New text follows the rules below,
and so does a sentence you were editing anyway.
Old sections are left alone until a change touches them.
A section written before a rule existed is not itself a defect,
so there is no cleanup pass to run
and no reason to reflow a document nobody is otherwise changing.

Two things are not covered by that leniency,
because only the change at hand can do them:
when an item closes, its history goes in the same commit,
and when you edit a section, the stale narration inside it goes with the edit.

## Piszemy po polsku, także w kodzie

Materiałem tego projektu jest polska proza,
a taką prozę repozytorium pisze samo o sobie.
Reguły tego lintera są pisane dla polszczyzny
i nad angielskim tekstem nie mają czego mierzyć,
więc dopóki dokumenty stoją po angielsku,
żądanie, żeby własny tekst repozytorium nie potykał się o to, co linter wytyka
(zob. [gotowe frazy](#a-phrase-that-arrived-ready-made-was-not-chosen)),
zostaje deklaracją.
Po polsku da się ten tekst przepuścić przez olski,
i `tests/test_docs.py` przepuszcza każdy dokument, który po polsku stoi,
oraz każdy docstring i każdy blok komentarza, które po polsku stoją
(zob. [`docs/prose-in-code.md`](docs/prose-in-code.md)),
więc żądanie schodzi z deklaracji do checka jednostka po jednostce.

Dokument mieszany do tego checka nie wchodzi.
Wchodzące wybiera próg udziału znaków diakrytycznych w całym pliku,
a przekroczenie tego progu należy do przekładu całego dokumentu,
a nie do jednej sekcji, którą ktoś w nim właśnie napisał po polsku.
Powodem jest to, co pakiet robi nad angielskim zdaniem:
puszczony nad angielską połowę takiego pliku
zgłasza nad nią polską typografię.
Dlaczego wybór nie schodzi za to do sekcji,
mówi `polish_share` w `harness/__init__.py`.

Checkiem jest tu silnik reguł, a nie gramatyka.
Gramatyka jest drugim żądaniem i znacznie węższym:
zdanie z przecinkiem, przysłówkiem albo rzeczownikiem odczasownikowym
nie ma w olskim wyprowadzenia,
a proza tych dokumentów składa się z takich zdań prawie w całości —
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)
trzyma polecenie, które to pokazuje nad README, i kolejkę tego, czego brakuje.
Więc tych dokumentów pod gramatykę nie przepisujemy.
Przepisanie kosztowałoby to, po co README jest:
podzbiór nie ma zdania podrzędnego,
a [rama przed szczegółem](#the-reader-goes-sentence-by-sentence)
stoi na uzasadnieniach, które podrzędnego wymagają.
Kolejka rośnie od strony gramatyki, nie od strony tych plików,
a celem, do którego rośnie, jest README:
kryterium wyjścia trzyma
[`docs/roadmap.md`](docs/roadmap.md#celem-toru-jest-to-readme).

Reguła obejmuje prozę z listy na początku tego pliku,
komentarze i docstringi, które do prozy liczy
[łamanie wierszy](#semantic-line-breaks),
komunikaty, które narzędzie drukuje,
oraz nazwy, które w kodzie wybieramy:
modułów, klas, funkcji, testów, poleceń i flag.
Po angielsku zostaje to, czego nie wybieramy:
słowa kluczowe Pythona, API bibliotek, klucze konfiguracji i nazwy formatów.

Nazwy symboli gramatyki są jednym słownikiem i zostają razem.
`Subject`, `Predicative`, `NPConjunct` i reszta w `olski/subset.py`
stały po angielsku, zanim ta reguła powstała,
a jeden symbol dopisany po polsku dałby mieszaninę wewnątrz nazwy,
przed którą ta reguła broni,
więc nowy symbol idzie po angielsku razem z nimi.
Kosztem jest raport: te nazwy `olski-check` drukuje jako role czytania,
więc przekład słownika i przekład raportu są jedną zmianą, a nie dwiema.

To samo stoi za modułem, który taki słownik trzyma.
`Audit` i `Distribution` stoją w `olski/calibration.py`,
więc polska nazwa pliku dałaby tę mieszaninę w każdym imporcie,
a przekład nazwy modułu idzie razem z przekładem słownika.

Nazwa w kodzie niesie znaki diakrytyczne, tak samo jak zdanie.
Tekst, który ich nie ma, nie liczy się tu jako polszczyzna:
[ekstrakcja](docs/extraction.md#which-documents-enter-the-corpus)
wyrzuca dokument, w którym diakrytyk pada rzadziej niż zadany próg,
i nie pyta, skąd ten brak się wziął.
Python przyjmuje takie identyfikatory,
a pliki repozytorium są w UTF-8 (`.editorconfig`).

Reguła nie wywodzi się z [pięciu sił](#five-forces) i nie jest od nich wyjątkiem.
One rozstrzygają, jak zdanie jest zbudowane, a ta, w jakim jest języku,
więc stoi przed nimi, żeby zdanie „każda reguła niżej” dalej było prawdziwe.

Przyjmujemy ją [leniwie](#adopt-these-rules-lazily) jak resztę,
z jedną różnicą co do jednostki.
Reguły prozy schodzą do zdania, bo zdanie poprawia się osobno.
Język tak nisko nie schodzi,
bo mieszanina języków wewnątrz akapitu, docstringa albo nazwy
czyta się gorzej niż każda z wersji z osobna,
a przemianowana funkcja sięga wszystkich swoich wywołań.
Jednostką jest więc sekcja, docstring, komentarz, komunikat
albo nazwa wraz z wywołaniami.
Gdzie prozy nie trzyma żadna sekcja, jednostką jest akapit:
`TODO.md` ma jeden nagłówek na cały plik,
więc sekcją jest tam wszystko,
a wpisy tej listy i tak stoją po polsku po jednym.
Powód wyżej na to przystaje,
bo mieszanina, przed którą broni, jest mieszaniną wewnątrz akapitu.
Nowa powstaje po polsku, także w dokumencie, który po polsku nie jest,
a zdanie dopisane do angielskiej sekcji idzie po angielsku razem z nią,
dopóki ktoś nie przełoży całego dokumentu, co jest osobną zmianą.
Nie ma z tego przebiegu porządkowego ani wpisu w `TODO.md`,
bo tekst napisany przed regułą nie jest usterką.
[`docs/roles.md`](docs/roles.md) powstał po polsku w całości,
ta sekcja stoi po polsku w pliku, który po polsku nie jest,
i jedno, i drugie jest zgodne z regułą.

## Five forces

Every rule below follows from one of five forces.
A rule you can derive from a force needs no separate justification,
and a newly noticed failure mode has an obvious place to go —
or a reason not to be written down at all.

- **The reader.**
  A document is read once, top to bottom,
  and only what came earlier is known.
  Test: can this sentence be understood from what stands above it?
- **The next change.**
  A fact changes in one place
  and leaves no stale copy anywhere else.
  Test: when this fact changes, how many places have to move?
- **Word choice.**
  A phrase was picked rather than arriving together with the topic.
  Test: did I write this, or did it assemble itself?
- **Checkability.**
  A claim about the world names what would settle it.
  Test: what do I show someone who asks how I know?
- **The reader's time.**
  A passage is paid for by everyone who reads past it,
  whether it was needed or not.
  Test: what does this passage buy someone who has read what stands above it?

None of the five follows from the others.
Two identical copies of a fact read perfectly from top to bottom
and rot at the first edit to one of them.
A passage answering a question nobody would ask passes the other four,
and is paid for by everyone who reads past it.
A failure mode that derives from none of the five
means either that a sixth force is missing
or that the rule is not worth having.

## The reader goes sentence by sentence

The test is not whether a sentence is true or on topic,
but whether it can be understood in the place it stands.
A sentence that fails it is in the wrong place,
however well the section around it is titled.
The same few things cause the confusion:

- **A name used before it is introduced** —
  a tier, a register, a pack, an abstention, LCFRS.
  The first occurrence says what it is; later ones need not.
- **A reference with no antecedent** —
  "this difference", "those requirements", "the above".
  The reader goes back and hunts,
  and if the antecedent is further down the hunt fails.
- **A conclusion before its premise.**
  This works in the other direction too:
  a paragraph laying out numbers before saying why they are worth reading
  asks the reader to memorize them for no reason,
  so provenance and measurement belong under the conclusion they produce
  rather than above it.
- **A variant before its condition.**
  A fallback argued for before the words "this applies when"
  reads as the plan.
- **A forward pointer used as a patch.**
  A pointer says where a fact's owner lives, and nothing else.
  If a sentence makes no sense until you follow it,
  the order is wrong and the pointer hid it.

Hence frame before detail.
The README states what olski is, why it is a subset,
where it is going and what runs,
before any document explains a mechanism.
A goal that takes half a document to reach sits too low,
however well it is described once you get there.

A heading serves that order and does not substitute for it.
It announces what the following paragraphs do,
and it does not fix a paragraph placed too early.
It pays for itself where a reader would otherwise
dig through twenty lines about something else to reach their own question:
[the analysis tiers](docs/linter.md#how-deep-does-each-rule-have-to-see)
are found by the reader who came for them.

The tail of a document is fixed, because there the order follows from the role:
a `Sources` section closes a document that cites,
and the document's own list of unsettled things
sits immediately before it —
[`Not yet decided`](docs/rules.md#not-yet-decided) in `docs/rules.md`.
Such a list only enumerates;
everything that justifies its entries is already behind the reader.

The test at the end of a change:
reread from the point where you started editing,
pretending you have not seen what follows.
An author remembers what is further down and cannot see the defect unaided.

## One owner per fact; repeat narrative freely

Prose may repeat; facts may not.
Restating context so a document reads standalone is good writing,
and scope notes, per-audience retellings
and "the neighbouring document covers X" summaries are welcome.
But every fact that can change —
a decision, a status, a threshold, a measured number, a boundary —
has exactly one owning section, and that is where edits land.
A restatement elsewhere names the owner, by link or by section heading,
and stays coarser than the original:
volatile detail is not re-enumerated at full precision a second time.
If a restatement is as precise as its owner,
a reader cannot tell which copy is current,
which is how two documents come to contradict each other.
The document list in the README is the reference example —
one clause per document, no numbers, and every entry links its owner.

**Reasoning has an owner in the same way a fact does.**
A mechanism is explained once,
and other places state the conclusion in a sentence and point at it.
`docs/rules.md` does this with the abstention-against-no-coverage distinction:
it uses the conclusion and credits
[`glr-in-practice.md`](docs/glr-in-practice.md#ambiguity-as-a-confidence-measure),
which owns the argument and the numbers.

**Code owns what is implemented; documents own what code cannot show.**
Which parameters a check accepts, what a threshold is set to,
what a rule fires on: the module is the truthful copy,
and a document restating it acquires a second version that goes stale silently.
Documents own provenance, rejected alternatives,
rationale that spans several modules, planned work, and open questions.
An example that illustrates a *format* earns its place —
this is what the declaration blocks in `docs/rules.md` are for —
while a copy of behaviour does not.

## Documents describe the present; git owns the past

A document that narrates its own evolution becomes a changelog,
and git already keeps a better one:
complete, dated, and attached to the actual diffs.
The test for a sentence about the past:
**does it change what a reader working with the current state should do?**
If it only records that something happened or was once different, delete it.
If it explains why the present looks the way it does,
keep it as present-tense rationale rather than as an event.

History that earns its place, always as rationale for the current state:

- **A rejected alternative and the reason for rejecting it**,
  which saves the next person from proposing it again.
  [Dlaczego mimo wszystko jest to podzbiór polszczyzny](README.md#dlaczego-mimo-wszystko-jest-to-podzbiór-polszczyzny)
  in the README is the reference example:
  the whitelist framing is named, and priced, and turned down.
- **A deliberate reversal or renaming**, so that nobody restores it by accident.
  `docs/roadmap.md` says the grammar is no longer the goal
  and what it survives as.
- **A date that identifies an external artifact** —
  a corpus version, a published measurement,
  the observation that "stands as a testament" dates a text to 2023 or 2024.
  That is provenance and it stays.

History that is deadweight:

- **Done markers.**
  When an entry in an open list closes, delete it;
  no ~~strikethrough~~ trophies.
  If it leaves a decision behind,
  the decision moves into the section that owns it and the entry still goes.
- **Status narration** — "update (2026-07): …", "now implemented".
  Fold the current state into the sentence that owns the fact.
- **A date whose only job is to order the document's own edits.**
  Such a date means an append happened where a rewrite was needed.

A word-level tell for all of these:
temporal adverbs — "still", "already", "no longer", "not yet", "for now" —
anchor a sentence to the moment of writing
and quietly assume a future edit
("still uncalibrated" reads as "uncalibrated until someone updates this sentence").
Write the plain present instead,
or pin the claim to a dated external artifact
when the point is that the known state has not moved.
Only the temporal sense is a smell —
logical uses are fine — so a hit is a prompt to reread the sentence,
not a verdict.

**Rewrite in place; do not append amendments.**
When a decision changes, the section that owns it changes,
so that the document reads true from top to bottom.
A section announcing that the above is amended as follows
turns the document into a patch series
the reader has to apply in their head.
The one legitimate two-state case is a decision taken but not yet built,
where the document really does describe both what exists and what will:
the target gets its own section naming what it supersedes,
each superseded section gets a one-line pointer forward,
and the instruction to merge them is written into the section itself.
Executing that merge is part of the change that implements the decision.
`docs/rules.md` carries two of these,
where `calibration` reads `uncalibrated` until milestone 1
and no-coverage reporting arrives with morphology.

## A phrase that arrived ready-made was not chosen

Prose can be assembled from parts that come with the topic:
the obvious image, the word that sounds equal to the gravity of the matter,
the sentence added for the rhythm of the paragraph.
It reads smoothly and is not a choice —
nobody checked whether the image fits the thing
or whether the word predicates what it was meant to predicate.
The recurring patterns:

- **The worn metaphor.**
  An image used without a thought for its literal meaning
  stops being checked,
  and in technical prose it smuggles in mechanics nobody meant to claim.
  A fresh metaphor that does work stays.
- **The echo sentence.**
  A second sentence saying what the first said in other words,
  usually a plain version and a rhetorical one side by side.
  The better one stays, not both.
- **The intensifier with no content.**
  "Key", "crucial", "it is worth noting", "absolutely central"
  sound like information about weight and are often decoration.
  A statement of weight stays when it carries a decision
  ("the only rule that must not fire on human Polish");
  bare emphasis goes.
- **Ready-made officialese.**
  A nominalization where a verb would do,
  and a construction with no agent ("a decision was made", "it was agreed").
  Where an action has an actor, the actor is the content,
  so a sentence that drops it drops the next move along with it.
  A technical term doing its job is not decoration:
  "abstention", "false-positive rate", "type-token ratio" are precise and stay.

Each pattern is a prompt to reread, not a verdict.
The test: strike the suspect word, parenthesis or sentence
and read the place without it.
If nothing was lost, the deletion stands,
and of two versions carrying the same content the shorter one is better.

Shorter does not mean telegraphic.
The other forces spend words deliberately:
repeated context buys a document that stands on its own,
and frame before detail buys comprehension.
The cutting applies to words that buy nothing.

These are also, in Polish, much of what this project's own rule inventory is about;
see [`docs/rule-inventory.md`](docs/rule-inventory.md).
Writing them into the repository's own prose
would be a poor advertisement for the tool.

## A claim about the world says how to check it

A sentence about the world outside the repository
either names what would settle it — a register, a document, a measurement,
your own observation — or it goes.
These documents are the ground for rule justifications,
so one unsupported sentence costs the credibility of the rest.
The rule engine encodes the same demand:
a rule carries a `justification` and its `sources`,
entries in the candidate inventory are marked *cited* or left as hypotheses,
and `calibration` reads `uncalibrated` rather than implying a measurement
nobody has made.

Two patterns produce most unsupported sentences:

- **The grading or excluding judgement** —
  "the best", "the largest", "the only", "typical".
  It sounds like a fact and is often an impression added for effect.
  A judgement with its grounds beside it stays; bare amplification goes.
- **Someone else's intention** — "wants", "plans", "aims to".
  What is checkable about another project is what it did:
  its code, its documentation, its published numbers.
  An interest somebody demonstrably has can be argued as your own reasoning;
  a plan attributed to them either goes
  or becomes an entry in an open-questions list.

A measured number carries what it was measured on.
"What this number is not" in [`docs/corpus.md`](docs/corpus.md#what-this-number-is-not)
is the reference example:
the figure and the reasons it cannot mean more than it does,
in the same place.

## Semantic line breaks

All prose here follows [Semantic Line Breaks](https://sembr.org) (sembr).
Instead of hard-wrapping at a fixed column
or putting each paragraph on one long line,
break lines at boundaries of meaning.

The rules, in order of precedence:

1. A line break must not change the rendered meaning of the text.
2. Insert a line break after a sentence.
3. Insert a line break after an independent clause
   punctuated by a comma, semicolon, colon, or em dash.
4. Optionally insert a line break
   after a dependent clause,
   a long phrase,
   or a list item.

Markdown collapses a single newline into a space,
so the rendered output is identical either way.
What changes is the diff:
a reworded sentence touches only the lines that actually changed,
instead of reflowing an entire paragraph
or producing one unreadable single-line diff.

This covers Markdown and plain text files,
commit message bodies and pull request descriptions,
prose in comments and docstrings,
where the same tighter diff is the same win,
and the prose fields of a rule declaration:
`justification` is folded before use,
so it is written with semantic line breaks like everything else.
A comment that already fits on one line stays on one line.
Code itself is unaffected;
format it however the language's usual tooling says.

Two mechanical consequences:

- Do not use two trailing spaces for a hard line break.
  Trailing whitespace is stripped here (see `.editorconfig`),
  so end the line with a backslash or start a new paragraph.
- Line-length linting is off (see `.markdownlint.jsonc`),
  because sembr line lengths are meant to vary.

## Where open work goes

Something noticed while working on another topic
belongs on a list rather than in the current change,
and which list follows from who closes the entry.
A commit in this repository closes it: [`TODO.md`](TODO.md),
whose header owns that boundary, the conventions for entries,
and what an entry is worth to whoever picks it up.
The outside world closes it:
the list in the document that owns the topic,
[`docs/open-questions.md`](docs/open-questions.md)
or a document's own `Not yet decided`.
The other list may carry a one-line pointer, and nothing more.

## Splitting work across sessions

Several sessions can run at once,
and what decides whether they may is the judgment each one settles
rather than the files each one touches.
Two sessions editing one document cost a merge.
Two sessions answering one question cost the answer twice,
and the two answers need not agree,
which no merge tool reports and no test catches.

So a split names, per session, the decision that session settles —
whether falling under a rate rule's floor is a decision, say,
which the docstring of `pattern_density` in `olski/checks.py` settles.
Where two come out the same, it is one session.
This is the demand [`TODO.md`](TODO.md) makes of a single entry —
that it name the evidence it reads and not only the files it changes —
applied to a batch of them.

A session is worth starting when one decision settles several entries.
An entry that cannot be settled until another session answers
is parked rather than parallelised,
and stays on the list with the blocker named,
so that whoever picks it up next does not start it cold.
The session that answers deletes the blocker,
because nothing rereads a parked entry until somebody picks it up.

Where two sessions both correct figures in one document,
split by the kind of number rather than by the section,
since a section is a place and a number has a cause:
one moves hit counts, the other denominators,
and whoever lands second reruns the tables.
Splitting by section reads as clean and is not,
because one decision reaches wherever its number went.

## Checks

```sh
pip install -e '.[dev]'
python3 -m pytest
ruff check .
npx --yes markdownlint-cli@0.45.0 '**/*.md'
```

Morfeusz 2 is a runtime dependency and installs from PyPI,
so the editable install brings it along with pytest, ruff
and the parser the harness reads Markdown with.
Where its wheel does not build,
`tests/test_morph.py`, `tests/test_subset.py` and `tests/test_corpus.py`
skip rather than failing to collect,
so the run reports the linter-track tests instead of zero tests.
A green run in such an environment has not been near
the grammar, the morphology or the treebank reader,
and the skip count is where that shows.

[`.github/workflows/checks.yml`](.github/workflows/checks.yml)
runs the same checks on every push.
The reason to have it is that a change here
is usually verified by the session that made it and by nothing else,
and sessions do not see each other's work,
so the combination of two of them is what the workflow runs and a person does not.
Its install step is also what makes the skip above safe:
it takes Morfeusz from PyPI and fails the job when that fails,
so a branch's latest commit is never covered by a partial run alone.
The command list above and the workflow's steps are two copies,
because a runner cannot read prose,
and `tests/test_docs.py` holds them equal,
so a check added to one fails the suite until it is in the other.

The workflow carries no badge.
A standing verdict on the front page of a hobby repository
is the same way of making it feel like work
that [`docs/roadmap.md`](docs/roadmap.md) refuses dates for.

Three more checks apply where a change moves a number
that lives in a document because no test can reach it.
Each names the document, and each is part of the change rather than after it.

A change in the grammar, in the readings it is given,
or in what counts as one reading
moves the tables in [`docs/corpus.md`](docs/corpus.md),
which are the output of a run over a treebank the suite does not hold.
The third of those is the one a session can make without noticing:
`signature` in `olski/parse.py` is four lines and no production,
and it moves every verdict the other two move.
Fetch the corpus as that document says, rerun `olski-corpus`,
and correct the tables in the same commit.
The same change moves what that document says about the run over the README,
which is the other half of the same demand and needs no fetch at all:
rerun the two commands it prints and correct the sentences under them.
The README prints a run of its own, verdicts and reading counts included,
and it goes with those: a figure there is the first one a reader checks.

A run reads the code once at import,
and it lasts long enough to invite starting it and editing on.
So a run started before an edit measures the code as it was,
two runs chained behind one command need not measure the same code at all,
and neither says so anywhere in its output.
Rerun after the last edit, not alongside it.

A change in the typography pack, in a check,
or in what counts as a word, a line or a sentence
moves the tables in [`docs/firing-rates.md`](docs/firing-rates.md) the same way.
Refetch as that document says and rerun the commands it prints.
A change to a threshold or an exemption also moves what the hits *are*,
so the classes that document reports having read
are corrected along with the counts, or the audit stops describing the pack.

Deleting a rule is the one change to a pack that needs no fetch.
It takes that rule's row out of every table and moves no other row,
because a rule is measured on its own,
and what shows it is cheaper than the corpora:
run the pack before the change and after it over any corpus at hand
and read the rows that survive.
A run whose surviving rows differ is not a deletion,
and then the refetch above is owed after all.

The same holds for the figures in
[`docs/generated-polish.md`](docs/generated-polish.md#what-was-measured),
the pairs per rule and the fragment counts in
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over),
the ones over the Markdown corpus in
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken),
the sizes in
[`docs/audit-corpus.md`](docs/audit-corpus.md#the-list),
the ending tables in
[`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match),
and the audit corpus half of `docs/firing-rates.md`,
with one more thing that moves them:
a change in what [the extraction](docs/extraction.md) keeps.
That last one is why the extraction is in this list twice over:
it decides both the sizes a document reports
and which characters a rule is shown,
so a change to it moves a count and can move a class as well.
The ending tables have a second thing of their own that moves them,
since the classes a probe in `harness/endings.py` sorts into
are declared there rather than read off the corpus.
Each of them prints the commands that produce its figures,
which is the whole reason those commands are there.

One table in this list is not moved by the grammar at all,
and it is the one easiest to leave stale for that reason.
[The attachment table](docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia)
counts other people's trees,
so no production moves it and the reruns above never reach it.
What moves it is a change to what `olski/attachment.py` counts —
which categories are a clause and which a noun phrase,
what standing after a verb means —
and there the rerun is owed like any other.

One pair of figures prices something the code does not contain.
[The two exclusion criteria that were measured and refused](docs/subset.md#dwa-szersze-kryteria-zmierzono-i-żadne-nie-stoi)
count the Składnica sentences each would take,
so no production moves them and no rule above reaches them either.
What moves them is a change to what `admissible` in `olski/subset.py` keeps,
since both were measured behind it,
or a change to what `signature` in `olski/parse.py` counts as one reading,
on which the finding that one of them buys nothing rests.
A criterion refused stays refused when its price moves,
so what the rerun protects is the number and not the decision.

One file in this repository is generated, and regenerating it is part of the change.
`olski/leksykon.txt` is the valency lexicon,
which `olski/walenty.py` derives from Walenty,
so a change to what that translation takes moves the file itself
and the figures under
[the lexicon's section](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)
along with it.
That document prints the command and says where the input comes from,
as the corpora above do.
The file is not edited by hand:
an entry written into it directly is lost by the next run of the generator,
and the reason for the entry is lost with it.

One set of figures is moved by two programs rather than one.
[The comparison the sonda took](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)
counts the sentences olski and a second substrate agree about,
so a change to the grammar moves it exactly as a change to `sonda/` does,
and the session editing `olski/subset.py` has no reason to look in that document.
`tests/test_sonda.py` catches the coarse half of that drift,
a verdict that stopped agreeing, and catches nothing about the counts,
so the rerun is owed there as it is everywhere else in this list.
It is also the cheapest one to owe: the figures come from this repository's own
README and the command beside them fetches nothing.

**A figure measured over this repository's own prose is not written down.**
Every corpus above is pinned — a dated release, a repository at a commit —
so the text under a figure holds still
and only a change to the code moves it,
which is what the reruns catch.
Our own text moves with any commit that touches it,
and nothing tells the person rewording a README
that a count in another document was taken over it.
What moves the number is the line.
A claim about the code stays, because a rerun is what it waits for:
how many sentences of the README derive
moves when the grammar does, like any other figure above.
A count of the text itself stays out —
how many sentences it holds, how long its comment lines run —
because a reword moves it and no rerun rule reaches a reword.
The command stands beside the claim, as it does for a fetched corpus.

## Code

**Prefer removing a branch to adding one, and unify divergent paths.**
Where callers differ only in where an input comes from,
push the difference to the edges
and route every caller through one branch-free core.
A branch is a second path to read, test and keep in sync;
a unified flow is proven once.
The engine is built on this:
a check is one code path plus its parameters,
a rule is a declaration,
and buying precision back is `unless_preceded_by` in the data
rather than a special case in the check.

## Tests

Plain module-level `def test_*` functions with bare `assert`,
fixtures instead of setup and teardown methods,
and `pytest.mark.parametrize` instead of loops or copied cases.

A test's name says what is guaranteed,
which is why `test_every_shipped_rule_carries_what_the_roadmap_asks_for`
is worth its length.
A trivial test is worse than no test:
it costs a read, it has to be kept working,
and it demonstrates a property nobody doubted.
The tests worth writing are the ones
that would have caught a mistake somebody could plausibly make,
which is what `tests/test_checks.py` spends its length on:
an unknown check kind passing validation,
a message using a placeholder its check does not report,
a density rule measuring a rate over a document too short to have one.

## Commit messages

The subject says why, in the imperative;
the what is in the diff already.
Aim for 50 characters and treat 72 as the limit;
detail that does not fit goes in the body, in semantic line breaks.
If a change deliberately hands some information over to git history —
a deleted done-marker, a dropped section — the message says so
rather than implying nothing was lost.

## Git in remote sessions: history is truncated or stale

A Claude Code session on the web may get a shallow clone.
`.git/shallow` truncates history,
and branches outside the task are fetched shallower still and staler.
Such a clone manufactures illusions:
the main branch can look two commits long,
`git merge-base` finds no common ancestor,
and `git log main..HEAD` prints the entire history
as though the lines were disjoint.
Before drawing a conclusion from history —
about diverged branches, rewritten history, missing files —
check `git rev-parse --is-shallow-repository`
and deepen the clone with `git fetch origin --unshallow`,
which also refreshes the truncated remote refs.
Only a complete clone tells the truth about where a commit came from.

Shallowness is one of two causes, and its check reads `false` for the other.
A remote-tracking ref that has not moved since the container started
produces the same illusions against complete history,
so a `main` that looks one commit long
is not explained by `--is-shallow-repository` answering `false`.
`git fetch --all` settles both at once,
and [rewriting history](#rewriting-history) owns the trap
in the form where it costs the most.

## Rewriting history

Squashing has gone wrong here once,
in the way that is easy to miss,
so these are not general advice but the specific traps that were hit.

**`origin/main` can be stale, including in a fresh clone.**
The remote's `main` moved mid-session
while the remote-tracking ref still held the value
fetched when the container started.
Run `git fetch origin main`
before using main as a base, a diff target, or a squash point.
A fresh clone is not a guarantee that anything stayed still afterwards.

**Squash onto the parent of your own first commit,
not onto a branch name.**
Find that commit explicitly
and reset to `<your-first-commit>^`.
Resetting to `origin/main` or any other name
aims at a ref whose value you have not checked,
and if it turns out to sit further back than you thought
you will silently absorb commits somebody else wrote.

**Check what you are about to rewrite, before you rewrite it.**
`git log --oneline <base>..HEAD` should list your commits and nothing else.
If a diffstat contains files you never touched,
the base is wrong.

**Never rewrite a commit you did not author in this session.**
Its message and authorship are somebody's work.
Absorbing it into a squash destroys both,
and the loss is not visible in the resulting tree,
which is why it has to be caught before the push
rather than after.

**Verify the squash preserved the content.**
`git diff <squashed> <original-head>` must be empty.

## The review pass

Asked for a review, go through the session's changes with fresh eyes,
answer the questions below,
and make the corrections that follow from the answers:
small refactors on the spot,
larger ones written into [`TODO.md`](TODO.md) instead of started.

- **Direction.** Which concrete problem disappears with this change?
  A change that only moves text has no direction.
- **Whose path.** Which role does the change fall on,
  and does somebody in that posture still meet a text written for them?
  [`docs/roles.md`](docs/roles.md) names the roles,
  where each one enters, and what ruins its path.
- **Elegance.** Simple and closed:
  no orphaned sections, no half-finished moves.
- **The five forces.** Put every changed place through each of the five tests.
  Check reading order separately on anything you moved:
  a section lifted upward now precedes what used to introduce it,
  and that is invisible from the altitude a file is read at before editing.
- **Consistency of references.**
  `tests/test_docs.py` resolves every relative link and every anchor,
  so a renamed section fails the suite instead of rotting quietly.
  What it cannot see is prose:
  grep for the names of deleted and renamed files and sections,
  and check that an example still shows what the rule citing it claims,
  because an example rots in place —
  the section is still there and no longer illustrates anything.
  Entries in `TODO.md` name files and sections,
  so a rename has to be carried there too.
  Check what the change could have broken;
  a check that cannot come out badly proves nothing.
- **Checks.** `python3 -m pytest` and `ruff check .`.
  New tests earn their place or do not get written.
- **What opened up.** Is something now simplifiable
  that could not be touched before —
  two documents that stopped differing, a pointer with nothing left to guard?
  Small ones now, larger into `TODO.md`.
- **Closed entries.** What does this change close
  in `TODO.md` or in an open list it touches?
  Closing an entry includes deleting it,
  per [documents describe the present](#documents-describe-the-present-git-owns-the-past).
  A half-closed entry stays, rewritten to what is actually left of it.
- **Rules, applied and kept current.**
  Does the change follow the conventions above,
  semantic line breaks included?
  And in the other direction:
  does the repository now contradict one of them on purpose?
  That is a defect in the rule,
  and the correction goes into this file, the README
  or the `TODO.md` header in the same commit.
- **Honesty.** Did the change hand some information over to git history?
  Then the commit message names it,
  per [commit messages](#commit-messages).
- **Noise.** Meta-comments, parentheses and pointers
  only where they carry content.
  In code, the same question about comment characters:
  a comment restating the line above it is noise.
- **Verdict.** Further changes needed, stands as it is, or revert the lot —
  with the reasoning.
  Changes without a problem driving them are stirring the text.
