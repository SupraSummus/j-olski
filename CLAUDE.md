# Notatki dla agentów AI

Tu jest cała konwencja pracy w tym repozytorium:
jak piszemy prozę, jak piszemy kod i testy,
które checki uruchamiamy, w które pułapki gita naprawdę wpadliśmy
i jak wygląda przegląd zmian.
Osobnego przewodnika dla współpracowników nie ma;
ten plik jest jedyną kopią.

Reguły prozy obejmują README, wszystko w `docs/`,
`TODO.md`, ten plik,
komunikaty commitów i opisy pull requestów.

## Reguły przyjmujemy leniwie

Nowy tekst piszemy według reguł niżej.
Te same reguły stosujemy do zdania, które poprawiamy z innego powodu.
Starego tekstu poza tym nie ruszamy.
Sekcja napisana przed regułą nie jest przez to usterką.

Ta pobłażliwość dotyczy stylu, nie prawdy.
Zdanie, akapit i wpis z listy, które twoja zmiana unieważnia,
poprawiasz tym samym commitem, bo potem nikt nie widzi, że są nieaktualne.

## Piszemy po polsku, także w kodzie

Nowy tekst w tym repozytorium powstaje po polsku.
Reguła obejmuje prozę z listy na początku tego pliku,
komentarze i docstringi, które do prozy liczy
[łamanie wierszy](#semantic-line-breaks),
komunikaty, które drukuje narzędzie,
oraz nazwy, które w kodzie wybieramy:
modułów, klas, funkcji, testów, poleceń i flag.
Po angielsku zostaje to, czego nie wybieramy:
słowa kluczowe Pythona, API bibliotek, klucze konfiguracji i nazwy formatów.
W nazwie w kodzie piszemy znaki diakrytyczne, tak samo jak w zdaniu:
Python przyjmuje takie identyfikatory,
a pliki repozytorium są w UTF-8 (`.editorconfig`).
Nazw przy tym nie ukuwamy:
kalka czyta się jak termin, którego nikt tu nie zdefiniował,
więc gdzie polszczyzna nazwy nie ma, zdanie mówi, co się robi.

Żaden check nie pilnuje tej reguły ani żadnej innej reguły prozy:
sprawdzamy je w przeglądzie zmian, a nie w testach.
Gramatyka olskiego takim checkiem nie jest i nie ma być:
wyprowadza znacznie mniej, niż te dokumenty zawierają —
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)
podaje polecenie, które to pokazuje nad README —
i nie przepisujemy tych dokumentów tak, żeby się pod nią zmieściły.

Regułę przyjmujemy [leniwie](#reguły-przyjmujemy-leniwie) jak resztę,
ale jednostka jest tu inna.
Jednostką reguł prozy jest pojedyncze zdanie, bo zdanie poprawia się osobno,
a jednostką języka jest sekcja, docstring, komentarz, komunikat
albo nazwa wraz z jej wywołaniami.
Gdzie sekcja nie ma własnej prozy, jednostką jest akapit:
sekcja `TODO.md` grupuje wpisy, więc jednostką jest tam wpis,
czyli to, co jeden commit dopisuje i kasuje.
Po polsku powstaje też tekst w dokumencie, który po polsku nie jest,
a zdanie dopisane do angielskiej sekcji piszemy po angielsku razem z nią,
dopóki ktoś nie przełoży całego dokumentu, co jest osobną zmianą.
Przekładu takiego dokumentu nie wpisujemy do `TODO.md`.
[`docs/roles.md`](docs/roles.md) powstał po polsku w całości,
a ta sekcja jest po polsku w pliku, który po polsku nie jest.

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

A failure mode that derives from none of the six
means either that a seventh force is missing
or that the rule is not worth having.

## Decyzja arbitralna nie dostaje wywodu

Część tego, co tu obowiązuje, jest kwestią gustu:
język, w którym piszemy, jeden plik zamiast osobnego przewodnika,
pięćdziesiąt znaków w temacie commita.
Taka decyzja mówi, co obowiązuje, i na tym koniec.
Wywód dorobiony do niej po fakcie jest oszustwem,
nawet jeżeli każde zdanie z osobna się broni:
podaje jako powód coś, co powodem nie było,
a czytelnik nie ma go czym odrzucić, bo decyzja i tak od wywodu nie zależy.
Zostaje to, co z decyzji wynika — koszt, granica stosowania, wyjątek —
a nie to, co ją rzekomo poprzedza.

## Skreślenie bywa całą naprawą

Zepsute miejsce — w prozie czy w kodzie — nie zawsze potrzebuje lepszej wersji.
Zanim napiszesz tę wersję, przeczytaj okolicę bez tego miejsca:
jeżeli reszta mówi już to samo, skreślenie jest całą zmianą.
Skreślony tekst zostaje w gicie, więc pomyłka jest odwracalna.

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

## Dla kogo jest napisane zdanie

Reguła wyżej pyta, czy fraza została wybrana.
Ta reguła pyta o adresata: czy zdanie jest napisane dla kogoś,
kto ma z nim coś zrobić,
czy dla kogoś, kto ma docenić, że autor umie pisać.

Popis jest napisany starannie, więc tamten test go nie łapie.
Test jest tu inny: przepisz zdanie najprostszą polszczyzną, jaką umiesz,
i sprawdź, co ubyło.
Jeżeli ubyło samo wrażenie, zostaje wersja prosta.

Rejestr, który przeważa w tych dokumentach,
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
- **„To” jako podmiot akapitu.**
  Zaimek odsyła do całego poprzedniego zdania, a nie do rzeczownika.
  Autor takiego zdania nie zauważy, bo wie, o czym pisał.
  Wstaw w miejsce zaimka rzeczownik.
- **Domyślne orzeczenie.**
  Zdanie pomija czasownik i każe czytelnikowi odtworzyć go z poprzedniego zdania;
  sygnałem jest „tak samo”, „też” albo „odwrotnie” w miejscu orzeczenia.
  Kto wchodzi w środek, poprzedniego zdania nie przeczytał.
  Powtórz czasownik, choćby zdanie wyszło dłuższe:
  „a zdanie, które i tak poprawiasz, tak samo” →
  „Te same reguły stosujemy do zdania, które poprawiamy z innego powodu”.
- **Jeden rytm na wszystko.**
  Trzy zdania pod rząd o tym samym kształcie —
  teza, przecinek, człon spięty przez „a”, „bo” albo „więc”,
  podmiot odłożony za orzeczenie —
  składają się na rejestr, w którym każde zdanie brzmi jak maksyma,
  więc żadnego nie da się już wyróżnić.
  Krótkie zdanie po trzech długich robi więcej niż „warto zauważyć”.
  Test: przeczytaj trzy kolejne zdania na głos.

Nie każde takie zdanie jest usterką.
Projekt jest dla przyjemności ([README](README.md#kierunek)),
więc tekst, który się dobrze czyta, jest tu jednym z celów.
Granica biegnie tam, gdzie tekstu nie czyta się już od początku do końca.
Wywód wolno tak pisać: README i te dokumenty, które o coś argumentują,
czyta się w jednym ciągu, i tam dobrze napisane zdanie się opłaca.
Instrukcji tak pisać nie wolno: ten plik, tematy commitów oraz `TODO.md`
czyta się wyrywkowo, w pośpiechu i z listy,
a zdanie, które trzeba najpierw rozszyfrować,
przepada razem z tym, co miało powiedzieć.

Rejestr bierze się głównie z tego pliku,
bo każda sesja zaczyna od jego przeczytania i pisze potem jego głosem;
widać to w `git log --pretty=%s`,
gdzie tematy powtarzają jeden szyk i jeden niewielki zbiór czasowników.
Regułę przyjmujemy [leniwie](#reguły-przyjmujemy-leniwie) jak resztę,
a sekcję przepisywaną z innego powodu
sprowadzamy przy okazji do zwykłej polszczyzny.

## A claim about the world says how to check it

A sentence about the world outside the repository
either names what would settle it — a register, a document, a measurement,
your own observation — or it goes.
These documents are the ground for rule justifications,
so one unsupported sentence costs the credibility of the rest.

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
and prose in comments and docstrings,
where the same tighter diff is the same win.
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
If a commit in this repository closes the entry, it belongs in [`TODO.md`](TODO.md),
whose header owns that boundary, the conventions for entries,
and what an entry is worth to whoever picks it up.
If the outside world closes the entry, it belongs in the list
in the document that owns the topic,
in [`docs/open-questions.md`](docs/open-questions.md)
or in a document's own `Not yet decided`.
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

Morfeusz 2 jest zależnością wykonawczą i instaluje się z PyPI,
więc instalacja edytowalna przynosi go razem z pytestem, ruffem
i parserem, którym harness czyta Markdown.
Gdzie jego wheel się nie buduje,
każdy plik testowy dochodzący do analizatora jest pomijany,
zamiast wywracać zbiórkę,
więc przebieg melduje testy stojące obok niego, a nie zero testów.
Przebieg zielony w takim środowisku nie był ani przy gramatyce,
ani przy morfologii, ani przy czytniku banku drzew, ani przy kompilatorze,
i widać to po liczbie pominięć.

[`.github/workflows/checks.yml`](.github/workflows/checks.yml)
uruchamia te same checki przy każdym pushu,
i to on sprawdza złożenie dwóch sesji, które się nie widziały.
Jego krok instalacyjny bierze Morfeusza z PyPI i wywraca zadanie, kiedy to zawiedzie,
więc ostatni commit gałęzi nie opiera się nigdy na samym przebiegu częściowym.
Lista poleceń wyżej i kroki workflowu są dwiema kopiami,
a `tests/test_docs.py` utrzymuje je równe,
więc check dopisany do jednej wywraca suitę, dopóki nie znajdzie się w drugiej.
Workflow nie nosi znaczka.

**Figura ma jednego właściciela, a właścicielem jest plik, który wypisuje przebieg.**
Figura należy do `figury/`, gdzie stoi wydruk przebiegu i nic poza nim,
a dokument, który ją czyta, powtarza ją grubiej i wskazuje ten plik:
rząd wielkości, stosunek, kierunek.
Jest to [jeden właściciel na fakt](#one-owner-per-fact-repeat-narrative-freely)
zastosowany do liczby zmierzonej, a nie osobna reguła,
i kupuje prozę, której przeliczenie nie dotyka,
bo „przeszło sto zdań” zostaje prawdą, kiedy 148 robi się 151.
Pełna precyzja w akapicie kosztuje odwrotnie:
jedno przeliczenie robi się nagłówkiem, tabelą, zdaniami pod nią
i liczbami, które ktoś z nich wyliczył ręką,
a żadna z tych rzeczy nie wywraca się, kiedy zostaje niezrobiona.

**Nagłówek nie trzyma liczby, którą przeliczenie rusza,** bo nagłówek jest adresem.
`Złote czytanie ocalało w 613 z 673 zdań wieloznacznych` był taki,
a jedna zmiana w gramatyce przemianowała go, jego anchor
i siedem plików, które go linkowały,
z `tests/test_docs.py` wywracającym się na każdym po kolei.
Rząd wielkości, stosunek i kierunek wolno tu tak samo jak w akapicie.
Stosunek ma być przy tym zgrubny, bo dokładny rusza się jak liczba:
`Złote czytanie ocalało w dziewięciu na dziesięć zdań wieloznacznych`
przestało być prawdą przy jednej zmianie w gramatyce,
więc sekcja ta nosi w nagłówku sam kierunek.
Wolno też zero: konstrukcja, która nie kosztuje nic, mówi to w nagłówku,
a zero, które przestaje być zerem, jest decyzją odwróconą, a nie liczbą ruszoną,
więc przemianowanie sekcji jest wtedy właśnie tym, o co chodzi.
Liczba powyżej zera nie ma ani jednej z tych wymówek,
a `Szyk zmierzono: kupuje kilkadziesiąt zdań i odbiera kilka`
jest tym kształtem, w którym rząd wielkości stoi poza adresem.

**Co rusza figurę, stoi w deklaracji obok niej, a nie w tym pliku.**
`FIGURY` w [`harness/figury.py`](harness/figury.py) podaje na każdy przebieg
polecenie, korpusy, bez których nie ma on czego czytać,
pliki, których zmiana rusza liczby, sekcje powtarzające figurę grubiej,
to, co po przeliczeniu zostaje ręką,
oraz to, kto ten przebieg jeszcze powtórzy,
a plik figury zapisuje odciski tych plików z chwili przebiegu.
`python3 -m harness.figury` odpowiada więc o należnościach z dwóch napisów
i nie pobiera niczego, więc odpowiada w każdym środowisku;
`python3 -m harness.figury <nazwa>` jest samym przeliczeniem
i należy do kogoś, kto ma czym je wykonać;
`python3 -m harness.figury --należne` przelicza wszystko, co raport nazywa należnym,
bo jedna zmiana w parserze czyni należnym kilkanaście figur naraz.
Nowa figura dostaje wpis w tej deklaracji, a nie akapit tutaj:
lista figur pisana prozą rośnie z każdym pomiarem,
czyta się od początku do końca i nie wywraca niczego, kiedy zardzewieje.
Figura, której nie bierze żadne polecenie — cena konstrukcji,
której gramatyka nie ma, policzona ręką na produkcjach —
nazywa w swojej sekcji produkcje, które zdejmuje,
bo inaczej nikt nie weźmie jej drugi raz
i zostaje mu wybór między liczbą nieaktualną a wymyśloną.

Trzy odpowiedzi raportu nie są ani aktualnością, ani należnością przeliczenia.
Figura zadeklarowana bez pliku stoi przed pierwszym przebiegiem,
a raport nazywa przy niej to, czego ten przebieg wymaga,
bo pierwszy przebieg nad figurą jest decyzją, a nie krokiem porządkowym.
Figura, której liczby przeniesiono z dokumentu, zamiast wziąć je przebiegiem,
ma w miejscu odcisku `nieznany`
i nie jest ani aktualna, ani należna, tylko niezmierzona tutaj.
Figura zamknięta ma w `powtórzy` napis pusty, czyli nie powtórzy jej nikt,
i przeliczenia nie jest winna nikomu:
gramatyka ruszona po tamtym przebiegu czyni jej liczbę starszą, a nie fałszywą,
więc sekcja restytuująca mówi, że pomiar jest sprzed tamtego commita.
Tu maleje aparat sond, bo sonda zamkniętej figury idzie do gita,
a commit, w którym leży, wchodzi do `w_gicie`.
Ile figur czeka na to orzeczenie, mówi ostatni wiersz raportu,
a zapada ono przy zmianie, która i tak figurę rusza,
bo przebiegu porządkowego nad wszystkimi naraz zabrania
[leniwe przyjmowanie reguł](#reguły-przyjmujemy-leniwie).
Przeliczenia nie wchodzą do bloku checków wyżej i nie uruchamiają się przy pushu:
korpusy są archiwami dziesiątek megabajtów pobieranymi raz na sesję,
a runner pobierający je przy każdym commicie płaciłby za to raz na commit.
Suita trzyma to, co jest w `tests/test_figury.py`, i nie startuje żadnej sondy:
odpowiedź, którą raport daje z odcisków i z polecenia,
oraz wiązanie pod nią — że ruszający zadeklarowany jest plikiem, który istnieje,
i że figura nazywa sekcję, która istnieje.

Przebieg czyta kod raz, przy imporcie,
a trwa dość długo, żeby zaprosić do puszczenia go i edytowania dalej.
Przebieg wystartowany przed edycją zmierzył kod z tamtej chwili,
dwa przebiegi za jedną komendą nie muszą mierzyć tego samego kodu,
a żaden z nich nie mówi tego w swoim wydruku.
Przeliczaj po ostatniej edycji, a nie obok niej.

**Blok wydruku wklejony do dokumentu jest prozą, a nie figurą.**
Rusza go to, co werdykt drukuje obok swoich liczb —
wiersz dopisany w `explain` w `olski/subset.py`
albo pole dopisane w `Deklaracja` w `olski/parse.py` —
i wtedy bloki w README,
w [`docs/ustawy.md`](docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)
i w [`docs/design-notes.md`](docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)
bierze się ręką, razem z arytmetyką pod nimi,
bo dokument mówiący, ile z czytań zdania werdykt wyjaśnia, liczy wiersze.
Żadne przeliczenie tego nie zrobi, więc figura, której blok stoi w dokumencie,
mówi to w polu `ręką`.

**Plik, który czyta sam kod, powstaje przebiegiem i nie poprawia się go ręką.**
`olski/leksykon.txt` jest leksykonem walencyjnym,
który `olski/walenty.py` wyprowadza z Walentego,
a `olski/skłonności.txt` tabelą skłonności,
którą `olski/rozstrzyganie.py` liczy nad Składnicą.
Polecenie i wejścia podaje przy pierwszym
[sekcja o leksykonie](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej),
a przy drugim
[sekcja o świadku](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek).
Wpis dopisany do takiego pliku wprost ginie przy następnym przebiegu generatora,
a razem z nim ginie powód, dla którego go dopisano.
Jedną rzeczą różnią się na tyle, żeby wiedzieć to przed skasowaniem któregoś:
gramatyka czyta leksykon przy imporcie i bez niego nie startuje,
a brak tabeli skłonności czyni tylko warstwę nad nią milczącą.

Reguła ta nie obejmuje każdych danych w `olski/`.
`olski/projekt.txt` jest leksykonem projektu i pisze się go ręką,
bo wiersz odpowiada na pytanie, na które nie odpowiada żaden korpus:
wedle którego leksemu odmienia się słowo, którego słownik nie ma
([`docs/subset.md`](docs/subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)).
Generatora ten plik nie ma i szukanie go jest szukaniem czegoś, czego nie ma;
przebiegiem wychodzą z niego formy, a nie wiersze.

**Figury nad prozą tego repozytorium nie zapisujemy.**
Każdy korpus z deklaracji jest przypięty — datowanym wydaniem, repozytorium na commicie —
więc tekst pod figurą stoi i rusza ją tylko zmiana w kodzie,
czyli to, co przeliczenia łapią.
Nasz tekst rusza się z każdym commitem, który go dotyka,
a jedyne, co o tym mówi, to figura wymieniająca ten plik wśród ruszających:
`readme` i `sonda-readme` wymieniają `README.md`,
więc przeredagowanie czyni je należnymi przeliczenia tak samo jak zmiana w gramatyce.
Twierdzenie o kodzie zostaje przez to na miejscu:
ile zdań README wyprowadza gramatyka, jest figurą jak każda wyżej.
Liczba o samym tekście — ile ma zdań, jak długie są jego wiersze komentarza —
zostaje poza dokumentem, bo mierzy prozę, a nie kod:
figura nad nią byłaby należna po każdym commicie dotykającym tekstu,
czyli mówiłaby tylko tyle, że ktoś pisał.

## Code

**Prefer removing a branch to adding one, and unify divergent paths.**
Where callers differ only in where an input comes from,
push the difference to the edges
and route every caller through one branch-free core.
A branch is a second path to read, test and keep in sync;
a unified flow is proven once.

**Sondę pisze się jak skrypt na jeden przebieg, dopóki nie okaże się, że zostaje.**
Domyślnie wychodzi z drzewa tym samym commitem,
którym wchodzi do olskiego konstrukcja, którą wyceniła,
więc nie dostaje ani własnych testów, ani dopracowanego docstringa,
ani reguł rejestru.
Poprzeczkę tego pliku płaci dopiero ta, którą ktoś nazwał w `powtórzy`
przy jej figurze, i płaci ją w commicie, w którym ta nazwa się pojawia.
Kolejność odwrotna marnuje pracę:
dopracowanie idzie wtedy w plik, o którym nie wiadomo jeszcze, czy ma czytelnika,
a większość sond go nie ma.
Dwie reguły niżej obowiązują sondę mimo to od pierwszego wiersza,
bo nie są dopracowaniem, tylko warunkiem prawdziwości pomiaru.
Kryterium wraz z odtwarzalnością przez git opisuje `sonda/__init__.py`.

**A probe asks olski's declaration and keeps no second copy of it.**
A differential probe takes productions out and reruns the verdict,
so `sonda/wysunięcie.py` is one predicate over a production
plus a `Sonda` declaration, and `sonda/ruch.py` runs the measurement for all of them.
The predicate asks the production rather than listing names beside the grammar,
because a list stays silent about a production somebody adds later
and the probe goes on measuring the ones it was given.
A probe that writes the subset out a second time
has that defect at the size of a grammar:
`sonda/polszczyzna.py` declares the subset again,
so it rejects a sentence olski derives,
and the divergence then says nothing about the two formalisms
the probe was built to compare.
It is the only probe of that shape and it is priced —
[`design-notes.md`](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)
owns what it bought, `TODO.md` whether it stays.
The shape is what makes a probe cheap to judge:
a predicate is read in a minute and a second grammar is not.

**Pozycja, której cena ma być osobną liczbą, musi być osobnym ciałem.**
Sonda różnicowa wycenia konstrukcję, zdejmując jej produkcje (`sonda/ruch.py`),
więc kształt gramatyki rozstrzyga, co da się wycenić,
a nie tylko co się wyprowadza.
Symbol obejmujący dwie pozycje naraz oszczędza kilkanaście produkcji
i odbiera pomiar, bo zdjęcie jego ciał zabiera obie pozycje, a nie jedną.
`RelativeNP` stojące obok `RelativePronoun` w `olski/subset.py` jest tym wyborem,
a [`subset.md`](docs/subset.md#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania)
podaje cenę każdej z dwóch pozycji osobno.
Gdzie o cenę osobną nikt nie pyta, wybieramy symbol wspólny, bo jest tańszy.

**Printed output does not take its order from a set.**
String hashing is randomised at startup,
so a set walked in order to print something prints a different thing in every run,
and over a sentence truncated at `MAX_READINGS` it prints different readings.
One place fixes the order and everything downstream inherits it:
`ciała` in `olski/parse.py` does that for the forest,
and where a sort key can tie, the tiebreak is written into the key.
A single value picked out of a set is the same defect wearing one value
instead of many, and it hides better:
one line of output that changes between runs
reads as a difference in the input rather than as a coin toss,
which is how it survived in `Powtórzenie` in `olski/rozstrzyganie.py`
until a probe printed the same finding twice.

## Tests

Plain module-level `def test_*` functions with bare `assert`,
fixtures instead of setup and teardown methods,
and `pytest.mark.parametrize` instead of loops or copied cases.

A test's name says what is guaranteed,
which is why `test_an_annotated_sentence_with_no_morphology_is_reported_rather_than_dropped`
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
  It reaches a renamed *file* as well, wherever prose names one
  inside an inline code span,
  which is how a document points at the code that owns a fact.
  What it cannot see is a name written without those backticks,
  and a section name, which no path spells:
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
