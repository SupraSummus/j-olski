# Roadmap

A high-level ordering, not a schedule.
There are no dates,
because the project is for fun
and a dated plan for a hobby is a way of making it feel like work.

Each milestone has an exit criterion,
because "when is this done" is the only part of planning
that reliably pays for itself.
The numbering is the order and it is load-bearing:
a milestone that turns out to need a later one
is a defect in the plan rather than a discovery about the work.

## What is being built

A style linter for Polish technical documentation,
used among other things
to check texts produced by language models.
See [linter.md](linter.md).

The grammar and parser work described in
[design-notes.md](design-notes.md)
is no longer the goal.
It survives as the deepest analysis tier,
reached only by rules that genuinely need it,
and as an optional track with a target of its own,
[this repository's README](#celem-toru-jest-to-readme).

## Guiding principles

**Rules are cheap to invent and worthless uncalibrated.**
Build the measurement before building the rule set.

That is also the field's own account
of why models write usable code and unreadable prose:
code came with a verifier and prose did not.
See [fiction.md](fiction.md#why-this-happens).
The account carries its own warning,
because a verifier teaches only what it checks —
[generated-polish.md](generated-polish.md#what-happened-when-the-rules-were-deleted)
records a body of Polish edited into its detectors' image.

**A rule that exists at two tiers is built at the cheaper one first.**
Nominalization density is a lemma rule in principle
and a suffix regex in practice,
and [linter.md](linter.md#suffixes-buy-more-than-expected)
argues the regex reaches most of it.
So the cheap version ships and gets its numbers,
and the version that needs an analyser
has to beat those numbers before its dependency is taken on.
The deepest milestone below applies that test to tier C;
stating it for every tier is what turns morphology
from an assumed step into an earned one.

**A measurement is allowed to come back negative.**
A milestone below the harness exits on a recorded finding
as readily as on a rule pack,
and the finding that good human technical Polish
breaks a norm a pack encodes
closes that milestone by deleting the pack.
A harness whose answer is known in advance is not measuring anything.

## Milestone 0: rule engine and the typography pack

A rule engine over plain Polish text,
plus the rules that need nothing but a tokenizer:
em dash frequency,
Polish quotation marks,
spacing artifacts.

Rules live in data, not in code,
carry an identifier, a message, a register pack,
and a recorded justification.

Markup formats are not in scope.
This is a linter for Polish, not a document-format library,
and separating prose from markup
belongs to whatever reads the markup, not here.

**Exit:** the engine runs over a plain Polish text file
and reports findings with locations,
and adding a rule requires editing data rather than code.
Met, see [rules.md](rules.md).

## Milestone 1: the calibration harness

Before the interesting rules, the thing that makes them honest.
Four deliverables.
They unblock each other in the order listed,
and they do not unblock the same rules.

**An extraction from markup to prose.**
Both halves reach the rules as plain text,
because milestone 0 keeps document formats out of olski
and that makes the extraction a step before the harness rather than part of it.
[generated-polish.md](generated-polish.md#the-apparatus-biases-a-rate-by-an-amount-the-corpus-decides)
prices skipping it:
one mark reads a quarter high over one body of Markdown
and true over another by the same writer,
so a rate measured over apparatus is not comparable
to a rate measured over prose,
nor to the next corpus's rate over its own apparatus.
`harness/markdown.py` does it for Markdown,
and [extraction.md](extraction.md) owns the account
of what it invents by doing it.

**The human half, which is the blocking one.**
Which Polish counts as the good side is **corpus sourcing** in
[open-questions.md](open-questions.md#linter-questions),
a question answered by gathering text rather than by writing code.
The rules below make specific demands of it —
a register represented in the distribution,
a baseline written in Polish rather than translated into it,
and prose whose characters nobody renormalized —
and [corpora.md](corpora.md) surveys what meets them.
Its answer is that the register is scarce enough
that the distribution gets assembled rather than chosen,
and that the rules whose hits get read
want a second corpus rather than a proportion of the first.

**The generated half, generated for the purpose and then left alone.**
[generated-polish.md](generated-polish.md#what-this-corpus-cannot-support)
is the body that was not:
its author had spent six sessions editing against detectors
for the patterns a linter measures,
so its rates are a floor rather than a sample,
and the difference is invisible in the text.
A floor is still worth measuring against as the harder case,
since a rule that fires on prose already edited against detectors
is finding something the editing did not reach.

**The report.**
A per-rule firing rate over a corpus, which `olski --format report` prints:
the command line tool reads every file into one corpus before any rule runs,
so the one-sided half of this is a way of printing the run it already does.
Ranking rules against each other needs both halves,
and [rules.md](rules.md#a-firing-rate-per-rule)
holds what the one-sided half can and cannot say.

### Two numbers, and the two questions behind them

Every rule leaves this milestone carrying two numbers:
one saying whether it can be trusted,
one saying whether it has anything to do.
Which numbers those are depends on the rule,
because reading a firing rate on human Polish as a false-positive rate
assumes an editor would have removed a real defect before publication,
and the corpus that satisfies it for one rule empties it for another.
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
owns the argument and what each kind of rule owes.

So the pack that exists exits in two pieces.
Its typographic rules exit with their hits read,
over the corpus above whose characters nobody renormalized,
and `em-dash-density` exits with two numbers of its own:
the human distribution its threshold has to sit outside,
and the share of the generated half standing beyond it.

### The two pieces are not the same size

Which piece to build first follows from the pack's composition
rather than from the order the four deliverables are listed in.
`Check.calibrated_by` in `olski/checks.py` says which of the two a check owes,
an audit of its hits or a distribution to place a threshold in,
and the pack is audit-shaped throughout but for its single rate rule,
so [the audit corpus](corpora.md#the-audit-corpus-polish-documentation-in-version-control)
unblocks nearly every rule shipped
and [the distribution corpus](corpora.md#the-distribution-corpus-edited-original-expository-polish)
unblocks one.

Their costs run the other way.
The audit corpus is [a list of repositories](audit-corpus.md)
with a clone command against each,
and it grows by admitting a repository rather than by gathering words,
so what it costs is that file and the searching to fill it.
The distribution corpus is a composition:
sources in stated proportions,
each share bounded by a defect somebody has to establish it carries,
and a recomputation with each source dropped in turn to find the thresholds
that measure a source rather than the language.

The audit piece therefore goes first,
and the argument for building the second is not the one rate rule it calibrates.
It is that [milestone 3](#milestone-3-statistical-rules) reads every threshold it owns
off the same distribution,
so two milestones pay for one corpus.

The generated half is built with the distribution corpus and not before it,
and the same two milestones pay for it:
it is the second number of that one rate rule
and of every threshold milestone 3 sets.

Which extractions this milestone owes follows from
[the repository list](audit-corpus.md#the-list)
rather than being settled apart from it.
`harness/markdown.py` reads one format,
the list records which format each member is in,
and a second extraction gets written when a repository worth admitting uses another.
So the list is chosen before the extraction is scoped, not after.
The reader of Python modules in the harness is not one of these:
it serves this repository's own prose,
which [prose-in-code.md](prose-in-code.md) says and prices.

**Exit:** every rule in the typography pack carries the two numbers its kind owes,
over a corpus anyone can fetch and a run anyone can redo,
and the pack has changed because of them —
a rule deleted, a threshold moved, or an exemption added —
with the number that caused the change recorded beside it.

Two rules could not reach that exit, and are gone.
`trailing-space` and `orphan-single-letter-word` read where a line ends,
and documentation is written in a markup format,
where a single newline is a space and no line end is one a reader sees.
So the extraction that makes such a corpus readable
takes both properties out with the markup —
[extraction.md](extraction.md#after-joining-a-line-end-rule-has-nothing-left-to-read)
holds what the step removes —
and running them over the files instead reads the format's line ends
rather than a reader's,
which [rules.md](rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives)
refuses.
Neither could therefore exit on a number,
so each exited on a decision:
either the pack claims prose laid out in lines as a register of its own,
or the two rules go, and they went.
What settled it was reading their hits across both corpora,
which turned up no instance of either defect,
and [firing-rates.md](firing-rates.md#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt)
holds those counts along with the machinery the deletion took with them.
That is the shape the exit above asks for,
a rule deleted with the number that caused it recorded beside it.

## Milestone 2: the plain-Polish pack, without an analyser

The rules with a citable Polish norm behind them,
which are also, conveniently, model tells:

- Rzeczowniki zombie, `-anie` and `-enie` and `-cie` density
- The phrases that invite them,
  `w celu`, `w razie`, `z powodu`, `na skutek`
- Impersonal `-no` and `-to`
- `można`, `trzeba`, `należy`, `warto`
- Participle chains, `będąc` and `mając` and the `-ąc` form generally
- Booster inflation matched on the stem,
  `kluczow`, `istotn`, `przełomow`

Each rule cites the plain-Polish source it comes from,
not a model it was observed in.

Two of the three nominalization endings need no morphology,
which is why the pack stands here rather than behind the analyser,
and the third one does.
[linter.md](linter.md#what-the-nominalization-endings-match) holds the measurement:
`-cie` matches the locative singular of `format` and `kontekst`
more often than it matches a nominalization,
where the other two barely match an inflected form at all,
and a stem reaches an adjective's paradigm without a lemma either way.

What the suffix route costs beyond that ending is not a class a lemma removes.
Morfeusz gives `zdanie` and `mieszkanie`, which are not zombie nouns,
the pair of readings it gives `pobranie`,
so the analyser agrees with the ending about the words the ending gets wrong,
and half of this pack's matches over the audit corpus sit in that agreement.
Whether that cost is affordable is what the two numbers are for,
and the ambiguity is where it is likeliest to prove not to be,
because it is the half no later milestone is holding a fix for.

The impersonal pair comes out of the same run the other way,
and [linter.md](linter.md#the-impersonal-endings-come-out-the-other-way)
holds it.
A tag answers what a judgement had to answer above,
so `-no` is the cleanest ending measured anywhere here
and the adverbs this milestone warns of are a twentieth of its matches,
while `-to` is one common word away from the same,
that word being the pronoun.
So the pack is three rules with three prognoses rather than one with one,
and which of the three a rule is
does not follow from all of them being suffixes.

What is left unmeasured is the boosters,
whose stems are not endings and want a match this run does not do.
[TODO.md](../TODO.md) holds them,
in front of the rules rather than after them,
a class a pattern cannot separate deciding whether a rule exists
rather than how it is tuned.

**Exit:** the pack is calibrated,
and its false discovery rate
on [the audit corpus](corpora.md#the-audit-corpus-polish-documentation-in-version-control)
is at or below the figure proselint reported for itself —
one false positive per ten true positives,
which is about nine false alarms in every hundred hits —
or the milestone records why a different bar is the right one for Polish.
[prose-linters.md](prose-linters.md#proselint-measured-what-everyone-else-asserts)
owns that figure and the corpus it was measured on.

Why that corpus and not the other follows from the shape of the number.
A false discovery rate is a share of hits a reader judged,
so it is the audit shape and it wants documentation rather than a distribution,
which leaves one candidate among the two corpora milestone 1 assembles.
What the audit corpus supplies is documentation somebody reviewed before merging,
where proselint's figure was taken over prose a copy editor worked on,
and the two are not the same pass.
The bar is quoted here against a different kind of editing,
which is one of the reasons the milestone is allowed to argue for another bar.
The other is authors:
a share measured over a corpus whose largest file is one person's habit
describes the person, and
[corpora.md](corpora.md#not-yet-decided) holds how many it takes before it stops.

## Milestone 3: statistical rules

Sentence-length variance,
paragraph-length uniformity,
three-item list frequency,
bullet density inside prose,
fact density,
connector density,
the share of sections that close on a negation,
the share of sentences opening on a fronted clause,
and the walk-on share `entity-recurrence` already computes
and no rule yet declares.

These need thresholds, not just patterns,
and a threshold is a point in the human distribution from milestone 1.

One kind of machinery is missing.
A share over units — of sections, of sentences — is a statistic
no check computes, since a rate per thousand words is not one.
[generated-polish.md](generated-polish.md#the-closing-sentence-is-measurably-different)
measures the negation share and says why such a finding
is a report about a document rather than an accusation against a sentence.

StyloMetrix from NASK extracts 195 stylometric features for Polish,
so the decision this milestone owes is
whether the features come from there or from checks written here.
The question that decides it is whether a feature arrives
with a location a finding can point at,
since a finding is a location and a feature vector is not.

**Exit:** every threshold is a stated point in the human distribution
rather than a chosen number,
with the point and the distribution recorded,
and the generated half saying for each threshold
how much of it lies beyond.

## Milestone 4: the delivery decision

Three routes:

- A standalone tool with its own rule format
- A Vale-compatible style,
  inheriting its editor and CI integration
- LanguageTool XML rules,
  inheriting an installed base and Morfologik

The decision stands here rather than at the end
because it decides whether the milestone after it exists.
A Vale style reaches tier A and stops,
since Vale's tagger ships an English model:
see [prose-linters.md](prose-linters.md#vale-is-the-architecture-to-study).
The LanguageTool route arrives with Morfologik already wired up,
so morphology becomes something the platform has
rather than something to build:
see [linter.md](linter.md#what-already-exists).
Only the standalone route leaves it as work.

Everything above is route-independent,
which is why the decision can wait this long,
and by here there is a calibrated pack to deliver,
which is why it need not wait longer.

One thing a route either supplies or leaves to be built,
waiting in [rules.md](rules.md#not-yet-decided):
a way to silence a rule on one line or one file.

**Exit:** a decision with its reasoning recorded.

## Milestone 5: morphology binding, and the rules that needed it

Lemmatization and part-of-speech tagging,
so lexical rules match inflected forms
and morphosyntactic rules become possible:

- Anglicisms and calques keyed by lemma
- `się` passives, which need the verb before the pronoun can be read
- Adjective stacking before a noun
- Comparative adjective frequency
- Lemma type-token ratio
- Echo sentences, measured as lemma overlap between neighbouring sentences

The analyser is Morfologik, decided in
[open-questions.md](open-questions.md#settled):
the grammar track needs generation and only Morfeusz does it,
which leaves this track free to take the analyser LanguageTool is built on.
How much that inheritance is worth
is what the milestone above has just settled.
The cost is a second analyser and a second tagset
in a repository whose grammar track already runs Morfeusz for analysis.

Whichever analyser is in use,
it owes its callers character offsets and not just forms,
because a finding is a location and an analysis is not:
`Segment` in `olski/morph.py` carries node numbers of a segmentation graph,
which is the shape of the problem rather than an accident of Morfeusz.

**Exit:** a lexical rule written as a lemma
catches every inflected form of it in running text,
and its findings point at the forms they matched.
Where the rule has a suffix approximation from milestone 2,
the lemma version beats it on the numbers from milestone 1;
where it does not, the approximation stays
and the analyser has not paid for itself.

## Milestone 6: deeper analysis, only where earned

Chunking or dependency parsing,
for the rules that need constructions rather than strings:
subject-predicate distance,
clause depth,
parallel-negation frames,
and fronting for gravity.

The last two are here for what is left of them
once the cheap versions have been built above.
The commonest Polish parallel-negation frame is punctuated rather than lexical,
so `em-dash-density` fires on the construction without having been aimed at it,
and tier C gets the lexical form:
[generated-polish.md](generated-polish.md#what-the-em-dashes-are-doing)
holds the rates that say which is which.
Fronting has a clause-fronted half a tier-A pattern reaches,
and a phrase-fronted half that
[linter.md](linter.md#recognizing-a-phrase-by-what-it-is-not-costs-more)
argues is beyond a better regex and beyond a lemma alike,
which makes it the candidate this milestone exists for.

**Exit:** at least one rule that could not work at tier B
working at tier C,
with the added machinery justified by that rule's calibration numbers.

## Optional track: the grammar

What the track is for is a parser that hands ambiguity back.
One reporting that a sentence has two readings, and which two,
is a different tool from one picking the likelier of them,
and it is the one whose output a writer can act on.
[subset.md](subset.md#validity-is-uniqueness-not-just-derivability)
owns the decision that makes it olski's,
and [swigra.md](swigra.md#what-it-leaves-open) is where the ground was found empty:
the closest existing parser of Polish resolves where olski would report.

The machinery is everything in [design-notes.md](design-notes.md)
about Earley, parse forests, free word order and LCFRS.

It is not on the critical path for the linter.
It remains the more interesting computational problem,
and the project is for fun,
so it stays in the repository as a track that may be picked up
whenever the linter stops being the more entertaining thing to work on.

If it is ever built,
the linter gains tier D.

### Celem toru jest to README

Plan otwiera się zdaniem, że każdy milestone ma kryterium wyjścia.
Tor gramatyczny stoi poza tą numeracją i to samo pytanie ma,
a odpowiedzią jest [README](../README.md) tego repozytorium:
tor kończy się wtedy, gdy każde jego zdanie wyprowadza się w olskim
i gdy każde ma jedno czytanie.
Kryterium mówi, co ma zajść nad zdaniem,
a nie czym ma być wyprowadzone,
więc wybór formalizmu zostaje przy cenie, a nie przy zobowiązaniu,
i trzyma go [design-notes.md](design-notes.md#formalizm-jest-środkiem-a-nie-celem).

Zdaniem jest tu to, co zamyka kropka, wykrzyknik albo pytajnik.
Nagłówek, pozycja listy i wiersz tabeli
dochodzą do olskiego jako akapity, których nic nie punktuje,
i w mianowniku kryterium nie stoją,
bo policzone jako odrzucone mierzyłyby ekstrakcję zamiast podzbioru.
Co je od zdania odróżnia i jak dużą częścią rejestru są, trzyma
[extraction.md](extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem).

Za tym plikiem przemawia to, czym on jest, a nie to, że leży pod ręką.
Stoi po polsku, w rejestrze, o który olskiemu chodzi,
i nikt go pod gramatykę nie pisał,
więc mierzy ją tak, jak zmierzyłby ją cudzy dokument.
[corpus.md](corpus.md#where-the-analyses-stop) trzyma polecenie,
które go przez olskiego przepuszcza,
i kolejność, w jakiej README ustawia to, czego gramatyce brakuje.

README stoi, a rusza się gramatyka.
Przepisanie go pod ten podzbiór kosztowałoby to, po co on jest,
a rachunek trzyma
[CLAUDE.md](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie),
więc to, co niżej, jest listą tego, co gramatyka ma dobrać.

Między tym, co ten przebieg pokazuje, a kryterium
stoją dwie rzeczy i tylko jedna z nich jest gramatyką.

**Konstrukcje.** Przecinek zdaniowy, zdanie podrzędne, czas przeszły,
liczebnik i rzeczownik odczasownikowy:
listę trzyma [subset.md](subset.md#what-it-does-not-cover-yet),
a README ustawia ją w swojej kolejności.
Zdanie podrzędne jest tu tym najdroższym,
bo README stoi na uzasadnieniach, a uzasadnienie go wymaga.
Kolejność nie jest tu harmonogramem.
Przysłówek, czas przeszły, liczebnik i rzeczownik odczasownikowy
dodane po jednym pokrycia nad tym plikiem nie podnoszą,
a ostatni z nich je obniża, co mierzy
[corpus.md](corpus.md#where-the-analyses-stop).

**Słowa, których słownik nie ma.** Morfeusz zwraca na nie `ign`,
a formy `ign` nie bierze żadna produkcja.
Klasa ma dwie połowy i olski wpuszcza jedną z nich.
Notacja tego rejestru — `docs/linter.md`, `CLAUDE.md`, `harness/markdown.py` —
dochodzi do gramatyki jako jeden rzeczownik nieodmienny
([subset.md](subset.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)),
bo rzeczownikiem nieodmiennym taka forma w polszczyźnie jest.
Zostaje polskie słowo odmienione, którego słownik nie zna:
`olski`, `lintuje`, `abstencje`, `commitów`.
Dla niego to samo czytanie byłoby nie tylko nieznane, ale fałszywe,
a [subset.md](subset.md#what-it-does-not-cover-yet) nazywa to z drugiej strony,
bo olski nie umie powiedzieć sam w sobie, czym jest.
Kolejka z banku drzew tej klasy nie ustawia,
bo tam każdy token ma rozbiór wybrany przez człowieka,
a formy, której słownik nie zna, w takim banku nie ma,
więc pokazuje ją dopiero przebieg nad dokumentacją.
Rejestr, o który tu chodzi, jest takich słów pełen,
więc jest to osobne żądanie, a nie skutek uboczny tego powyżej.

Druga połowa kryterium jest droższa od pierwszej.
Wyprowadzenie każdego zdania to pokrycie,
a jedno czytanie na zdanie to ta własność, dla której olski jest podzbiorem,
i żeby README ją miało,
przyłączanie wyrażeń przyimkowych musi przestać być otwartym problemem.
[subset.md](subset.md#the-open-problem-prepositional-attachment)
trzyma trzy wyjścia z niego
i mówi, że własność w tym brzmieniu
wyklucza dużą i zwyczajną część technicznej polszczyzny.
README jest taką polszczyzną,
więc kryterium żąda wybrania jednego z tych trzech.

**Wyjście:** każde zdanie [README](../README.md) wyprowadza się w olskim
i każde ma dokładnie jedno czytanie,
a pokazuje to polecenie, które
[corpus.md](corpus.md#where-the-analyses-stop) drukuje.

## Wish, not milestone: prose and fiction

Making language models write good Polish fiction
is an open research question,
and [linter.md](linter.md#and-fiction) records
what is lintable there,
what is not,
and the three directions that look more promising than linting:
generative constraints,
stylometric targets rather than stylometric alarms,
and the linter as a deterministic critic inside a revision loop.
[fiction.md](fiction.md) surveys the research underneath that:
the documented failure modes,
and the finding that post-training rather than prompting produces them.

Deliberately not a milestone.
Labelling a research question as a deliverable
is how hobby projects die.

## What would count as finished enough

- A rule pack for Polish technical documentation
  where every rule carries its two numbers
  and a stated justification
- Run over a real document,
  producing findings a Polish technical writer agrees with
- At least one rule deleted because the numbers said so
- Honest documentation of what the tool does not do,
  starting with the fact that it is not a detector

None of that requires the project to be useful,
and all of it would be novel for Polish.
