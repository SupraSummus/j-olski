# Notes for AI agents

This is the whole convention for working in this repository:
how prose is written, how code and tests are written,
which checks to run, the git traps this repository has actually hit,
and the review pass.
There is no separate contributor guide;
this file is the only copy.

The prose rules cover the README, everything under `docs/`,
`TODO.md`, this file,
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
Żądanie, żeby ten własny tekst był dobrze napisany,
niesie cały ten plik i nie ma pod sobą narzędzia:
sprawdza je przegląd zmian, a nie przebieg testów.
Pakiet reguł, który sprawdzał tu polską typografię, jest wycofany
([`docs/linter.md`](docs/linter.md#what-closed-the-track)),
a razem z nim lista plików, nad którymi ten check biegł.

Gramatyka checkiem tego tekstu nie jest i nie ma być.
Jej żądanie jest znacznie węższe:
zdanie z dwukropkiem, przysłówkiem albo rzeczownikiem odczasownikowym
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
a celu, pod który by rosła, ten tor nie ma:
kierunek i cenę kroku trzyma
[`docs/roadmap.md`](docs/roadmap.md#tor-gramatyczny-nie-ma-końca).

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

Nazwa w kodzie niesie znaki diakrytyczne, tak samo jak zdanie.
Tekst, który ich nie ma, nie liczy się tu jako polszczyzna:
[ekstrakcja](docs/extraction.md#which-documents-enter-the-corpus)
wyrzuca dokument, w którym diakrytyk pada rzadziej niż zadany próg,
i nie pyta, skąd ten brak się wziął.
Python przyjmuje takie identyfikatory,
a pliki repozytorium są w UTF-8 (`.editorconfig`).

Reguła nie wywodzi się z [sześciu sił](#six-forces) i nie jest od nich wyjątkiem.
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
Gdzie sekcja prozy nie trzyma, jednostką jest akapit:
sekcja `TODO.md` grupuje wpisy i własnej prozy nie ma,
więc jednostką jest tam wpis, czyli to, co jeden commit dopisuje i kasuje,
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

## Six forces

Every rule below follows from one of six forces.
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
- **Plainness.**
  A sentence is written for somebody who has to act on it,
  rather than for somebody who will admire the writing.
  Test: rewrite it in the plainest Polish you can —
  what was lost besides the impression that the author can write?
- **Checkability.**
  A claim about the world names what would settle it.
  Test: what do I show someone who asks how I know?
- **The reader's time.**
  A passage is paid for by everyone who reads past it,
  whether it was needed or not.
  Test: what does this passage buy someone who has read what stands above it?

None of the six follows from the others.
Two identical copies of a fact read perfectly from top to bottom
and rot at the first edit to one of them.
A passage answering a question nobody would ask passes the other five,
and is paid for by everyone who reads past it.
A pose passes the other five as well:
it is comprehensible in the place it stands, it copies no fact,
it names what would settle its claims,
and it can be shorter than the plain version.
Word choice comes closest and its test acquits it,
because a pose is laboured rather than automatic,
which is how a repository can produce one at volume
while breaking no rule below.
A failure mode that derives from none of the six
means either that a seventh force is missing
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
[`Not yet decided`](docs/corpora.md#not-yet-decided) in `docs/corpora.md`.
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
`docs/linter.md` does this with the abstention-against-no-coverage distinction:
it uses the conclusion and credits
[`glr-in-practice.md`](docs/glr-in-practice.md#ambiguity-as-a-confidence-measure),
which owns the argument and the numbers.

**Code owns what is implemented; documents own what code cannot show.**
Which productions the grammar has, what a lexicon entry says,
what a probe counts: the module is the truthful copy,
and a document restating it acquires a second version that goes stale silently.
Documents own provenance, rejected alternatives,
rationale that spans several modules, planned work, and open questions.
An example that illustrates a *format* earns its place,
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
  [Dlaczego biała lista, skoro czarna była tańsza](README.md#dlaczego-biała-lista-skoro-czarna-była-tańsza)
  in the README is the reference example:
  the linter framing is named, and priced, and turned down.
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
- **The contrastive frame.**
  A sentence taking its precision from what it excludes
  rather than from what it asserts:
  "X does Y, not Z", "the reading Polish does not have".
  Strike the negated half and read what is left standing.
  An exclusion somebody would actually propose survives that,
  since a subset is documented by exclusion;
  a foil invented to give the sentence a shape does not.
  Where what is left says nothing definite,
  the frame was doing the predicating and the verb under it was never chosen,
  so the repair is a sharper assertion rather than a shorter sentence.

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

These were also, in Polish, much of what the retired rule inventory was about.
The inventory is gone and the demand is not:
prose written this way reads worse, whether or not anything measures it.

## Dla kogo jest napisane zdanie

Reguła wyżej pyta, czy fraza została wybrana.
Ta reguła pyta o adresata: czy zdanie jest napisane dla kogoś,
kto ma z nim coś zrobić,
czy dla kogoś, kto ma docenić, że autor umie pisać.

Tamten test popisu nie łapie,
bo popis jest napisany starannie
i na pytanie, czy złożył się sam, odpowiada „nie”.
Test jest tu inny: przepisz zdanie najprostszą polszczyzną, jaką umiesz,
i sprawdź, co ubyło.
Jeżeli ubyło samo wrażenie, zostaje wersja prosta.

Rejestr, który się w tym repozytorium wyhodował,
to stylizacja na esejistykę inteligencką.
Powtarza się w niej kilka chwytów.

- **Peryfraza w miejscu nazwy.**
  Zdanie omawia rzecz, którą umie nazwać.
  Najbardziej szkodzi w temacie commita i w nagłówku,
  bo tam zdanie czyta się bez akapitu pod spodem.
  Naprawą jest rzeczownik, a nie skrócenie zdania.
- **Wymyślony sprawca.**
  Reguła o urzędowej frazie wyżej gubi wykonawcę,
  a tutaj wykonawcą zostaje abstrakcja:
  pomiar rusza się sam, zdanie gubi role, dokument dostaje wskazanie.
  Skutek jest ten sam co przy zgubionym wykonawcy,
  czyli nie widać, kto ma co zrobić.
  Metonimia zwykła zostaje, bo dokument mówi i reguła żąda
  bez udawania, że któreś z nich czegoś chce.
  Wykreślamy dopiero to, co rzeczy przypisuje wolę albo doznanie.
- **Czasownik domowy.**
  „Stoi”, „trzyma”, „bierze”, „kosztuje”, „schodzi”
  obsłużyły już w tych dokumentach tyle znaczeń,
  że żadnego nie znaczą osobno:
  „stoi” zastępuje jest, obowiązuje, zależy i znajduje się.
  Czyta się to jak termin i nie jest zdefiniowane nigdzie.
  Test podstawieniowy: wstaw czasownik dokładny i sprawdź, czy zdanie zyskało.
  „Sklejenie stoi przed analizą” → „Sklejenie poprzedza analizę”.
  Jest to ta sama wyblakła metafora co wyżej,
  tylko wyblakła w tym repozytorium, a nie w polszczyźnie,
  więc tamten test jej nie widzi.
- **„To” jako podmiot akapitu.**
  Zaimek odsyła do całego poprzedniego zdania, a nie do rzeczownika.
  Autor takiego zdania nie zauważy, bo wie, o czym pisał.
  Wstaw w miejsce zaimka rzeczownik.
- **Jeden rytm na wszystko.**
  Trzy zdania pod rząd o tym samym kształcie —
  teza, przecinek, człon spięty przez „a”, „bo” albo „więc”,
  podmiot odłożony za orzeczenie —
  składają się na rejestr, w którym każde zdanie brzmi jak maksyma,
  więc żadnego nie da się już wyróżnić.
  Krótkie zdanie po trzech długich robi więcej niż „warto zauważyć”.
  Test: przeczytaj trzy kolejne zdania na głos.

Nie każde takie zdanie jest usterką.
Projekt jest dla przyjemności, a materiałem jest polska proza
([README](README.md#kierunek)),
więc tekst, który się dobrze czyta, jest tu jednym z celów.
Granica biegnie tam, gdzie tekstu nie czyta się już od początku do końca.
Wywód może: README i te dokumenty, które o coś argumentują,
czyta się w jednym ciągu, i tam dobrze napisane zdanie się opłaca.
Instrukcja nie może: ten plik, tematy commitów oraz `TODO.md`
czyta się wyrywkowo, w pośpiechu i z listy,
a zdanie, które trzeba najpierw rozszyfrować,
przepada razem z tym, co miało powiedzieć.

Ten rejestr bierze się głównie z tego pliku,
bo każda sesja zaczyna od jego przeczytania i pisze potem jego głosem.
Widać to w `git log --pretty=%s`,
gdzie tematy powtarzają jeden szyk i jeden niewielki zbiór czasowników.
Regułę przyjmujemy [leniwie](#adopt-these-rules-lazily) jak resztę,
więc przebiegu porządkowego nad tym plikiem nie ma,
a sekcję przepisywaną z innego powodu
sprowadzamy przy okazji do zwykłej polszczyzny.

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
what makes two derivations one reading, say,
which the docstring of `Node.signature` in `olski/parse.py` settles.
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
every test file that reaches the analyser skips rather than failing to collect,
so the run reports the tests that stand clear of it instead of zero tests.
A green run in such an environment has not been near
the grammar, the morphology, the treebank reader or the compiler,
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
One of those tables has a fourth thing that moves it and no production in sight:
[which sentences keep the gold reading](docs/corpus.md#złote-czytanie-ocalało-w-437-z-478-zdań-wieloznacznych)
is what `Las.numer_czytania` in `olski/parse.py` answers
about the roles `PORÓWNYWANE_ROLE` in `olski/coverage.py` names,
so a change to either moves that table and leaves the rest of the run standing.
A second table sits under that same heading, saying which reading the gold one is,
and it has a mover the first one has not:
the order the forest yields readings in, which `ciała` in `olski/parse.py` fixes.
Whether a reading is in the forest does not depend on that order and its number is nothing else,
so a rewrite there can leave every verdict and every survival answer alone
and still move the second table.
The same change moves what that document says about the run over the README,
which is the other half of the same demand and needs no fetch at all:
rerun the two commands it prints and correct the sentences under them.
The README prints a run of its own, verdicts and reading counts included,
and it goes with those: a figure there is the first one a reader checks.

That count has a second thing that moves it, and it is not a change to the code.
Rewording the README moves it too, because the sentences it counts are that file's,
and the rule against writing down a figure measured over this repository's own prose
does not reach it: the figure is about the grammar and lives in another document.
So the demand lands here instead.
A commit that touches README prose reruns those same two commands
and corrects the sentences under them,
and that includes a commit whose subject is anything else —
a paragraph added about a new capability moves the count exactly as a rewrite does.

Two figures over that treebank live in `docs/subset.md` instead,
where [what prepositional attachment costs](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)
counts the productions that give it a position
and the sentences the grammar reads backwards without them.
They move with the same run and are the easiest in this list to miss,
because the document they sit in is the one a grammar change is written from
rather than the one it reports into.
A counterfactual figure of that kind also has to name the productions it drops,
or the next session cannot take it again
and has only the choice between leaving a stale number and inventing a new one.

A rewrite of the grammar that moves no verdict still moves those tables,
so "the language did not change" is not a reason to skip the rerun.
Where a rejected sentence stopped is the furthest point some analysis reached,
and that depends on which productions were tried rather than on which succeeded,
so two grammars accepting the same sentences with the same readings
rank the blockers differently.
Every figure taken behind a dropped group of productions moves for the same reason:
the grammar it was measured on is the one with the group missing,
and that one is not the same grammar twice.

The parser moves that ranking as well, and it is the easier of the two to miss,
because a change there is not a change to the language at all.
Which productions were tried is a fact about the traversal,
so a rewrite of `olski/parse.py` that leaves every verdict alone
can still rank the blockers differently,
and the rerun is what says whether it did.

A grammar change moves one more set of tables,
and they sit in the document furthest from where a grammar change is written:
[what the grammar derives from statutes](docs/ustawy.md#co-gramatyka-z-tego-wyprowadza)
is a run over acts an API serves rather than over a treebank.
A change to what `harness/ustawy.py` composes into a sentence moves them as well,
since the sentences the grammar is shown there are the ones that step produced.
That document holds a second run of the same kind and the grammar moves it too:
[where the analyses stop in that register](docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
ranks the blockers there and prices each construction's move against them,
so it is owed alongside the tables above rather than instead of them.
The fetch is a command that document prints,
and what it names is an ELI address rather than a commit,
which is the one pin in this list that cannot move:
an act is amended by another act carrying its own address,
so the text under an address stays as it was promulgated.

A run reads the code once at import,
and it lasts long enough to invite starting it and editing on.
So a run started before an edit measures the code as it was,
two runs chained behind one command need not measure the same code at all,
and neither says so anywhere in its output.
Rerun after the last edit, not alongside it.

[`docs/firing-rates.md`](docs/firing-rates.md) is the one document in this list
that no change moves, because the pack it reports on is deleted.
It is kept as the price the retirement was decided at,
it says so in its own opening, and nothing in it is to be recomputed:
a figure there that looks wrong is a figure about a program that is gone.

The rerun is owed for the figures in
[`docs/generated-polish.md`](docs/generated-polish.md#what-was-measured),
the pairs per rule and the fragment counts in
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over),
the ones over the Markdown corpus in
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken),
the sizes in
[`docs/audit-corpus.md`](docs/audit-corpus.md#the-list),
and the ending tables in
[`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match),
and what moves them is a change in what
[the extraction](docs/extraction.md) keeps.
That is why the extraction is in this list twice over:
it decides both the sizes a document reports
and which words a probe is shown,
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

One figure counts the register rather than anything this repository decides,
and three separate things move it.
[How much of the register reads two ways in Polish](docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
is taken over the audit corpus with `olski/wieloznaczność.py`,
so a change to what that module counts moves it,
and so does a change to what `admissible` in `olski/subset.py` keeps
or to the valency lexicon under it,
both of which stand between the text and the count.
The third is the extraction, as everywhere else in this list.
The figure is the ground under an open question rather than under a rule,
so a rerun that moves it moves what that question is asking about.

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
so a change to the grammar moves it
exactly as a change to `sonda/polszczyzna.py` or `sonda/wiezy.py` does,
and the session editing `olski/subset.py` has no reason to look in that document.
`tests/test_sonda.py` catches the coarse half of that drift,
a verdict that stopped agreeing, and catches nothing about the counts,
so the rerun is owed there as it is everywhere else in this list.
It is also the cheapest one to owe: the figures come from this repository's own
README and the command beside them fetches nothing.

Five sets are a difference rather than a count,
and that is what makes them easy to leave stale.
[What comma coordination costs](docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania)
is the gap between olski and olski with three productions taken out,
[what the numeral phrase costs](docs/subset.md#liczebnik-zmierzono-i-nie-odbiera-ani-jednego-zdania)
is the same gap over the two bodies that build one,
[what negation costs](docs/subset.md#negacja-zmierzona-kupuje-148-zdań-i-odbiera-jedno)
is that gap over the particle and the genitive it governs,
and [what the four word orders cost](docs/subset.md#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery)
is that gap over the fourteen bodies the four of them make,
so everything that moves the tables above moves all four,
and so does a change to the probe that names each variant's productions —
`sonda/przecinek.py`, `sonda/liczebnik.py`, `sonda/negacja.py`, `sonda/szyk.py` —
or to `sonda/ruch.py` under them, which builds the variants and counts the movement.
The fifth measures a construction the grammar does not have,
so its variants add productions where those four take them away:
[what the adverb would cost](docs/subset.md#przysłówek-zmierzono-przed-dopisaniem-i-drugi-gospodarz-odbiera-39-zdań)
is the gap between olski and olski with `sonda/przysłówek.py` written into it.
That direction moves which end of the variant list is olski and nothing else:
the denominator is olski either way,
so a grammar change moves those figures as it moves the four above.
Each of the five prints the command that produces its figures.
They share a denominator, so a construction admitted moves every one of these
tables and not only the one belonging to it.
What a test holds there is only that a probe measures this grammar
and not a copy of it, the numbers themselves having nothing to disagree with.
All five take their figures over the README as well,
so a commit that touches README prose owes those five runs
alongside the two the section above already asks of it.

One more difference prices a refusal, and it is the only figure in this list
whose two halves are moved by different things.
[What discontinuity buys and costs](docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
counts on one side the treebank sentences another grammar needed a gap for,
which moves only when the corpus release does
or when `sonda/nieciągłość.py` changes what it counts as a gap,
and on the other the uniqueness that dropping contiguity takes away,
which moves with the grammar, since its denominator is what olski accepts,
and with `sonda/polszczyzna.py` and `sonda/wiezy.py` under it.
The verdicts beside the first half move with the grammar as well,
and they are the half the refusal rests on:
a construction that stops appearing there is a construction
that has begun to buy those sentences.
A third figure there prices the refusal itself —
the sentences olski calls unambiguous while the forest holds a second,
discontinuous reading — and it is moved by both of those at once:
its population by the corpus release and by what `w_lesie` matches,
its verdicts by the grammar.
Refused stays refused when the price moves,
so what the rerun protects is the number rather than the decision.

A second refusal is priced the same way and every one of its figures
moves with the grammar, because the variant it measures is derived from it.
[What a gap buys and costs](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)
rewrites olski's own productions into a threaded feature in `sonda/luka.py`,
so a production added to the clause family arrives in the variant unasked
and moves the counts, the reading numbers quoted on single sentences,
and the production totals beside them.
The half the refusal rests on is the agreement against the gold tree,
which moves with `_role` in `olski/corpus.py` as well:
a role the treebank stops withholding from a gap
is a gap that has begun to buy those sentences.
A grammar change that gives a relative clause a body
also moves what the enumeration reaches
and with it the sentence that section names as the purchase,
which is the one figure there a rerun alone does not settle.

One set of figures is not moved by anything, for the same reason as the one above,
and it sits in a section a grammar change is otherwise read from.
[What packing decides](docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania)
prices a table the parser was given instead of the one it has,
and both the probe that took the figures
and the enumerator they were measured against are gone.
The section says so in the paragraph above them.
What a test holds there is the two sentences the argument rests on,
in `tests/test_subset.py`, where they now guard the counting itself,
and nothing about those figures.

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

**Printed output does not take its order from a set.**
String hashing is randomised at startup,
so a set walked in order to print something prints a different thing in every run,
and over a sentence truncated at `MAX_READINGS` it prints different readings.
One place fixes the order and everything downstream inherits it:
`ciała` in `olski/parse.py` does that for the forest,
and where a sort key can tie, the tiebreak is written into the key.

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
which is what `tests/test_subset.py` spends its length on:
a production that admits a phrase nothing should derive,
a segmentation graph stitched together one node out,
a lexical exclusion taking a reading the grammar needed.

## Commit messages

The subject says why, in the imperative;
the what is in the diff already.
Aim for 50 characters and treat 72 as the limit;
detail that does not fit goes in the body, in semantic line breaks.

Where the change is a name, a number, a threshold or a decision,
that word is in the subject.
A subject is read alone, in `git log --oneline` and in a list of pull requests,
so one that defers its content to the body has none:
`Nazwij po imieniu to, co tor składu robi`
announces that something was named and withholds the name,
where `Nazwij tor składu realizacją powierzchniową`
fits the same limit and says it.
Test: does the subject carry the word the body turns on?
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
- **The six forces.** Put every changed place through each of the six tests.
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
