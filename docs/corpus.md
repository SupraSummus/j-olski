# Measuring against Składnica

The grammar in [subset.md](subset.md) admits a subset of Polish on purpose.
This document is how much of a subset,
measured rather than asserted.

For the theory behind the measurement,
see the coverage curve in [design-notes.md](design-notes.md);
the tooling is `harness/corpus.py` and `harness/pomiar.py`.

## What Składnica is

A constituency treebank of Polish from IPI PAN.
It was built by parsing sentences drawn from NKJP with Świgra —
Woliński's implementation of Świdziński's GFJP —
and having annotators choose the correct tree out of the resulting forest.

That provenance decides what the corpus is good for.
Each file is a whole forest with the answer marked inside it,
which suits olski exactly,
because olski's question is not *is this the tree*
but *does the correct reading survive, and does it survive alone*.
The terminals also carry disambiguated tags,
so the grammar can be measured with morphological ambiguity removed
and again with it restored.

It also decides what the corpus cannot prove, which is covered below.

## Fetching it

Not vendored, and not downloaded by any code here.
The corpus is 92 MB compressed and 2.4 GB extracted,
it is distributed under the GPL while this repository carries no licence file,
and a parser is not a download manager.

```sh
curl -L -o skladnica.tar.gz \
  'https://zil.ipipan.waw.pl/Sk%C5%82adnica?action=AttachFile&do=get&target=Sk%C5%82adnica-frazowa-180723.tar.gz'
tar xzf skladnica.tar.gz
```

That is the 2018.07.23 development release,
which is the most recent one and the only one with 13,035 verified trees.
The 2011 v.½ files on the same page are older and smaller;
the dependency conversion there is older still,
and nothing here reads it.

Then:

```sh
python3 -m harness.pomiar Składnica-frazowa-180723/
python3 -m harness.pomiar Składnica-frazowa-180723/ --morphology live
```

Those two runs own every count this document is about,
which is why the document states orders of magnitude and directions instead
([CLAUDE.md](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)):
a figure copied into a paragraph here goes stale at the next production admitted,
and nothing tells the reader that it has.
So the shape of a result is written down and the size of it is run for.

What the runs do not print is the sentences behind a row —
the forms leading a blocker, the two runs' accepted sets compared,
a row read again with a group of productions dropped.
Each of those wants a per-sentence verdict rather than a total,
and half of them want two runs compared rather than one printed,
so each is a script written for one question and thrown away
([CLAUDE.md](../CLAUDE.md#code)).
Where such a reading stands in this document,
it stands as the class it found and not as the count.

The tests do not need any of this.
They use hand-written forests in `tests/test_corpus.py`,
so the suite stays offline and the licensing question stays undecided.

## What the corpus contains

22,066 forests, of which 13,035 carry a complete gold tree:

| verdict | forests | |
| --- | --- | --- |
| `FULL` | 13,035 | a complete tree was chosen |
| `NO_TREE` | 4,414 | no correct tree was in the forest |
| `TOO_DIFFICULT` | 2,922 | the annotators would not judge it |
| `NOT_SENTENCE` | 966 | not a sentence |
| `WRONG_SENTENCE` | 416 | ungrammatical |
| `MORPH` | 313 | the morphological annotation was wrong |

The 41% without a tree is itself a result worth keeping in view.
A full-scale grammar of Polish, hand-built over decades,
failed to produce an acceptable analysis for a fifth of real sentences
and the annotators declined to judge another eighth.
Whatever olski's number turns out to be,
it is not being compared against 100%.

## The measurement

Gold morphology, whole corpus, every sentence carrying a gold tree:
better than one sentence in eight comes out with a single reading,
better than one in twelve with several,
and for the rest — under four sentences in five — olski derives nothing.
All three are written as bounds rather than as figures,
because every production admitted moves them
and does not move them all one way:
a host admitted so that a reading stops being false
takes sentences out of the first count and puts them in the second
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
so uniqueness is not a number that only rises.
The run owns the counts and this document owns their order,
because a figure quoted here would be stale by the commit after it
([CLAUDE.md](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)).

The curve by length matters more than the total,
because it is the shape the coverage actually has.
Better than a third of the sentences up to five tokens come out with one reading,
better than a fifth of those up to ten,
better than one in twenty-five between eleven and twenty,
single sentences above that, and none at all above forty.
So olski is a subset of short declarative Polish and nothing else,
and coverage falls off a cliff between ten and twenty tokens.
That is the honest starting point of the curve,
and the point of recording it is that the next tier has something to beat.

The sentences above forty segments are ten in the whole treebank,
and olski rejects all ten.
They cost under a mebibyte each and a third of a second together,
against a run that takes half a minute,
so leaving them out buys nothing and the denominator is the whole annotated corpus.

What that denominator counts is a sentence the treebank hands over whole.
A gold tree's terminals have to tile it without a gap and without an overlap,
and the run asks rather than assumes it
(`Sentence.całe` in `harness/corpus.py`),
because a terminal the reader loses takes a word out of the sentence
and takes the span the role comparison stands on with it.
No `FULL` forest of the 2018 release breaks the criterion,
so it prints no row here and stands for the next release,
where a lost node comes out as a sentence not measured
rather than as a sentence measured short.

## Where the analyses stop

A rejected sentence stopped on some token,
and its part of speech names the construction
that would have to be admitted next.
Where the form reads several ways,
the row takes a reading the grammar licenses over one it does not,
because a reading no terminal reaches for names no construction to admit.
The form `i` is what that criterion is worth:
Morfeusz reads it as an interjection before it reads it as a conjunction,
and under the interjection it lands in a row naming nothing to build.
An analysis stops on it where a comma stands in front of it,
which is a string Polish does not write
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
Ranked, those parts of speech are a work queue,
and the run above prints it: a row per part of speech,
ordered by how many analyses died on one,
and one row for the sentence that stopped on no token at all.
The counts move with every production admitted, so the run owns them,
and what this document owns is which rows lead and what stands in them.
How much the ranking settles about what gets built next is another document's:
[roadmap.md](roadmap.md#kolejka-blokerów-odsiewa-a-kolejność-dopisań-ustala-tekst)
takes it as a sieve rather than as an order of work.

Punctuation leads it by a wide margin,
accounting for more than a fifth of the rejections
without touching the interesting questions
about discontinuity and formal power at all:
of clause-level punctuation olski has the comma, the colon, the semicolon
and the dash, and the form in front of that row is the hyphen,
ahead of everything else in it several times over.
The hyphen is what the dash production does not take, by a criterion of its own
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
and this corpus writes its dash with it —
as dialogue and reported speech, which newspapers and prose are full of
and technical documentation has none of.

The sentence that ran to its own end with nothing deriving the whole of it
has a row of its own, and that row is no token's part of speech.
The analysis took every form the sentence has and closed nothing over them,
so there is no stopping form to name
(`na_czym_stanęło` in `olski/segmentacja.py` is the criterion,
and a verdict over a single sentence says the same thing in a second sentence).
The row stands among the first few under either morphology,
and reading it needs the sentences rather than the row.
Most of them carry a verb form,
so the verbless headline a newspaper corpus is full of —
`Na próżno.`, `Najpospolitszy.` —
is the smaller half of it, and the rest is a sentence
whose verb the grammar has and whose structure it does not close.
Counted under the closing mark instead,
those sentences read as a defect in punctuation
and promise a construction the grammar already has.

A form an exclusion emptied of every reading has a third row of its own,
because the analysis stopped on it and not on the sentence's own end,
which is the distinction a verdict over one sentence draws
by naming the form (`bez_licencji` in `olski/segmentacja.py`).
The treebank raises none: an exclusion empties a form
where a pronoun's post-prepositional form stands without a preposition
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą))
and where a reflexive particle stands with no word in front of it
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika)),
and neither is Polish, so neither is what a press corpus is made of.

Wiersz cząstki stoi pod znacznikami złotymi wysoko w tej kolejce,
a prowadzą go `też`, `jednak`, `czy` i `tylko`.
`się` prowadziło ten wiersz, dopóki cząstki nie brał bezokolicznik;
z tamtej pozycji został sam ogon, czyli cząstka oddalona od swojego czasownika
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika)),
i wiersz spadł przez to o rząd wielkości i o miejsce w kolejce.
Cztery formy, które go teraz prowadzą, nazywają dwie różne roboty:
`jednak`, `też` i `tylko` są cząstkami,
których zamknięta lista olskiego nie bierze
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#cząstka-ma-dwóch-gospodarzy-i-przy-jednym-dostaje-etykietę)),
a `czy` jest pytaniem o rozstrzygnięcie, którego ta gramatyka nie ma
([subset.md](subset.md#what-it-does-not-cover-yet)).
Pod Morfeuszem wiersz ten schodzi niżej,
bo przed nim staje zdanie, którego całości nic nie domyka,
spójnik otwierający zdanie, forma nieznana słownikowi i liczba.
Dalej w obu kolejkach idą czas przeszły, przyimek i bezokolicznik,
a przy samym dole stoją `pcon` oraz `siebie`, każdy z garścią zdań.
Konstrukcje, po których te dwa wiersze się nazywają, gramatyka ma
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#imiesłów-przysłówkowy-stoi-tam-gdzie-okolicznik-wyrażony-zdaniem)),
a wiersze przez to nie znikają i tym mówią o tej kolejce rzecz najważniejszą:
nazywa ona część mowy, na której analiza stanęła,
a nie konstrukcję, której zabrakło.
Ile wart jest każdy taki wiersz, mierzy się po jednym,
a nie odczytuje z jego wysokości.

Clause-level punctuation is the addition that showed
how little a row says about what admitting its construction buys.
The colon and the comma standing in front of a conjunction came in together
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
the `interp` row they belong to barely moved,
the `conj` row lost several times more sentences than that,
and the particle row *rose*.
The three forms leading the `conj` row were the same three after that addition,
all of them capitalized:
what left that row is the conjunction standing between two clauses,
and what stayed is the conjunction opening a sentence,
which is another construction and has since been admitted
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-na-czele-zdania-wiąże-je-z-poprzednim)).
So the row a construction is admitted out of is not the row that records it,
and most of what left the `conj` row
moved onto another blocker instead of being accepted.
The second addition read the row before writing anything,
which is how the two constructions turned out to be one:
the lemmas opening a sentence in this treebank are the lemmas
the two lists of clause-level conjunctions already carried, plus two.

Five constructions have left this queue outright —
the adverb, the gerund, the impersonal verb
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#czasownik-nieosobowy-rządzi-ramą-swojego-lematu)),
the future tense
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony))
and the sentence-initial conjunction
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-na-czele-zdania-wiąże-je-z-poprzednim)) —
and their rows are gone from the front of it.
The last of those emptied a row that had been fourth,
and it shows the paragraph above once more:
the rows for the particle and for a sentence with no structure over it
both rose, because most of what left the `conj` row
stopped further along rather than being accepted.
The impersonal shows the paragraph above from the other side:
its row fell to about a third of itself,
the addition accepted well under half of what fell out of it,
and the rows above it rose,
because a sentence it did not buy stopped further along instead.
The future tense is the addition that emptied its own row:
what is left of `bedzie` is a handful of sentences at the bottom of the queue,
and under half of what left it was accepted,
the rest having stopped further along.
Others took part of a row with them:
the particle, the subordinator, clause-level punctuation,
the adverbial participle, the reflexive pronoun,
and the predicative's future tense
are admitted in a shape narrower than Polish,
so their rows stay and what stands in them is what the shape leaves out.
The linker `to` is the one that left the printed queue instead.
Its verbless body took about a fifth of the `pred` row and moved that row two
places down; the orders that stand `to` beside a finite copula took what was
left of it — `Był to nieforemny chłopak.`, `To są oczywistości.`
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#przy-kopuli-ten-sam-łącznik-ma-trzy-szyki-a-zgodność-wybiera-podmiot)) —
and the row now stands below the twelve this document prints.
It fell by more than twice the sentences those bodies accept,
which is the point of the paragraph above.

The subordinator row is where that shows on today's queue.
`że` leads it, and the grammar has `że`:
those sentences hang the clause on a noun or on a predicative —
`nadzieja, że odzyska syna`, `Możliwe, że miałam zostać królikiem` —
and the grammar has that position in a verb's frame and nowhere else.
Behind it stand the subordinators the conditional stands under,
which are left out for a reason of their own
([subset.md](subset.md#what-it-does-not-cover-yet)).

The rows are named as Morfeusz names a part of speech,
and the treebank names four of them otherwise.
Składnica's tags are NKJP's,
which calls the particle `qub`
and gives pronouns three parts of speech of their own —
`psubst`, `padj`, `padv` — where Morfeusz files them
under the noun, the adjective and the adverb.
The reader translates those four names, as it translates the case names beside
them. Without the translation the grammar is shown a tagset it does not speak:
a terminal asking for `part` matches no `się` in this corpus
and one asking for `adj` matches no `który`,
so two constructions the grammar *has* fire here not once,
and a thousand sentences and more come out rejected
for a difference between two tagsets rather than for anything in the grammar.
The untranslated run also ranks three rows by a tag
where a row is for a construction.
Only the gold column moves with the translation:
the live column's tags come from Morfeusz to begin with.

What a row does not say is how much admitting its construction buys.
Negation is the measurement of that, and the numeral is the same measurement
from the other end: dropping negation puts hundreds of sentences back
into the particle row, and putting it back takes a fraction of them
off the rejected list, the rest moving rightward onto another blocker,
where every sentence the numeral phrase reaches comes out of the numeral's own row
and it takes a fifth of them.
A sentence carries more than one missing construction,
and the row counts where an analysis stopped
rather than what admitting the construction buys.
So a row does say which sentences an addition can reach —
it just does not say how many of them it will take.
What the two rankings promise against what they deliver is priced in
[roadmap.md](roadmap.md#etap-6-reszta-konstrukcji).

A preposition does not rank near the top of this queue at all,
and two groups of productions are why.
Drop the one that puts a modifier in front of the clause
and the `prep` row rises by an order of magnitude, into the first few,
led by capitalized forms, because a fronted modifier opens its sentence.
Drop instead the positions that hang a prepositional phrase on a noun or on an
adjective — `wyrażenie_przyimkowe` under `człon_imienny`
and under `człon_przymiotnikowy`, which are the
attachment
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
leaves to the reader — and the row doubles.
With both in place what is left of it is a preposition
standing where no rule reaches
rather than a construction the grammar lacks.

So a construction frequent here is not automatically worth admitting,
which is the reason the register gets a run of its own below.

The queue was ranked on a treebank,
and the register olski is aimed at can be asked whether it agrees.
Its own README is Polish documentation, so it answers:

```sh
python3 -m harness.markdown README.md --into proza/
python3 -m olski.check proza/README.txt
```

Better than a quarter of that README's sentences derive once,
most of the rest derive more than once,
and a handful are rejected.
The file is written that way rather than found that way:
it omits the constructions olski does not derive
([README](../README.md#konwencje)),
so the count says as much about the prose as about the grammar,
and [roadmap.md](roadmap.md#readme-jest-przyrządem-pomiarowym)
owns what is left of the run as an instrument.
The ambiguous ones are almost all one of two classes:
a prepositional phrase either the noun or the verb could host,
and a nominative read as an accusative,
which are the two classes
[open-questions.md](open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
counts over a whole register;
`--readings` is what shows them, as readings olski has and a reader does not.
A sentence carrying both at once, once in each of its clauses,
comes out with over a hundred readings,
and that is the multiplication rather than any single construction going wrong.

A third class sits beside those two and belongs to the dictionary.
Morfeusz reads `sam` as an adverb beside the adjective,
so `Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem
drugiego.` has a reading in which `sam` is an adjunct of the clause.
That is a dictionary reading Polish does not have here,
the class this register shows the same way the treebank shows it on `wobec`.

What stops each of those is named.
This file used to rank the forms no production takes,
and construction after construction took that ranking apart —
the gerund, the adverb, the numeral written as a word,
clause-level punctuation, the wrapping kind beside it, the project lexicon,
each argued in the section of [subset.md](subset.md#what-the-grammar-covers)
that admitted it.
What is left of the ranking is single occurrences:
the bare letter *p* that the title's joke turns on,
the digit in `Morfeusz 2`,
and the English title this file cites beside the form `polsku`.
One rejection stands on the shape its words are in rather than on a word,
and it is the quoted `Nowa program`,
whose disagreement is the whole of what the example shows:
every word is one some production takes,
and nothing derives the two together.
The run says which is which rather than leaving it to be worked out:
a rejected sentence names the words no production takes,
or, where every word is one some production does take,
names the place its analysis stopped at
([subset.md](subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).

The two rankings agree on which constructions lead
and disagree on what admitting one is worth.
Most sentences either run rejects carry two missing classes or more,
so a production added by itself leaves them where they stand,
and the row the treebank ranks first rates at nothing here.
A prediction made before an addition can be checked against one sentence,
and `Działają dwie rzeczy.` is the sentence it was checked on:
it needed the numeral phrase and nothing else.
The reason the prediction could be made at all was
[the valency lexicon](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej) —
`dwie rzeczy` is nominative or accusative and a subjectless clause takes an object,
so without the entry saying `działać` takes none
the numeral would have made this sentence ambiguous rather than accepted.

One thing in that run belongs to the register and not to the queue.
A form Morfeusz does not know stops a sentence,
and gold morphology leaves a treebank no such form to rank,
which is why [warstwa-leksykalna.md](warstwa-leksykalna.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)
and [the lexicon beside it](warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)
own it.
It is a demand on the grammar that this register makes and the treebank cannot,
and it is the reason to take this run at all
rather than to read the queue alone.
Both halves of it are met, and this run is what said which half to meet first.
The notation the register writes —
`docs/linter.md`, `CLAUDE.md`, `harness/markdown.py` —
reaches the grammar as one indeclinable noun rather than as five segments,
and the inflected Polish word Morfeusz lacks — `commitów`, `Pythonem` —
is declared word by word instead,
because an indeclinable reading would be wrong for it rather than merely unknown.
The treebank could not have raised the first of those:
notation occurs in these 13,035 sentences a handful of times,
web addresses and `10.000zł` and `II.16`,
so nothing in the live column below turns on it.

That run is the grammar track's other instrument beside this treebank.
The track has no exit criterion
([roadmap.md](roadmap.md#readme-jest-przyrządem-pomiarowym)),
so what the run prices is each addition rather than a distance to a finish.
What it counts as a sentence is what the run reports as one,
and nothing in this file comes back `fragment` and stands outside the denominator.
[extraction.md](extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem)
owns that class and how much of this register it is.

### The same queue over prose

The queue, the length curve and the status table are computed by
`olski/pokrycie.py`, which the run here extends with the gold-tree tables,
so the same three tables come off a file of prose under a command of their own:

```sh
python3 -m harness.markdown docs/roles.md --into proza/
olski-pokrycie proza/roles.txt
```

Whoever raises coverage over a document of their own needs this ranking
over that document rather than over a newspaper treebank,
because the two registers put different constructions in front:
the hyphen leads the punctuation row here and technical documentation has none of it,
while notation and the all-caps name lead a document in this repository
and occur in these 13,035 sentences a handful of times.
The number to read there is the curve rather than the total,
because a construction admitted moves the stopping point of a long sentence
without moving its verdict,
so the total can stand still while the run bought exactly what it was meant to
([pisanie-po-olsku.md](pisanie-po-olsku.md#zasłanianie-działa-w-obie-strony)).

Morphology is live and has to be:
prose carries no disambiguated tags, so the gold column has no meaning over it,
and the queue is approximate for the reason the gold column exists —
the row names the first reading Morfeusz listed for the form
where the analysis stopped because no reading of it could continue.

## Agreement, which matters more than acceptance

Accepting a sentence proves nothing if the reading is wrong.
Olski admits every order the subject, the object and the verb can stand in
([subset.md](subset.md#what-the-grammar-covers)),
so on every sentence it accepts
there is a live question of whether it found the subject the annotators did.
The gold trees mark this directly:
a required phrase carries its valency slot,
and `subj(np(nom))` is the subject.

On the accepted sentences where the gold tree marks a role to compare,
the roles agree in better than nine out of ten,
and the rest split between a *partial* verdict and a *disagreement*.
The run prints all three,
and it prints beside them the accepted sentences with no role to compare against:
a pro-drop sentence like `Wstaje.` realizes no subject,
so the gold tree marks none and there is nothing to check.
That count stands under the table
rather than letting the check quietly narrow its own denominator.

None were *reversed* —
olski never read a subject as an object or the other way round,
which is the failure the uniqueness property exists to prevent
and the one that would have been worst to find.

The *partials* are the gold tree naming a subject
where olski reads the phrase as what the verb takes.
In `Wystarczy przeanalizować wypowiedzi Adama.`
the gold tree makes the infinitive phrase the subject of `wystarczy`,
in `Wystarczy, że ujmiesz w swej pracy twarz i ręce.` it makes the `że` clause one,
and in `Mieszka z nimi sama.` it makes `sama` the subject,
which olski reads as the predicative of a subjectless clause.
A fourth is the same shape as the second and arrived with the numeral phrase:
in `Wyszło z tych badań, że identyfikacja ma dwa poziomy.`
the gold tree makes the `że` clause the subject of `Wyszło`.
The fifth is neither, and it is in this list because the check found it
rather than because anything was added:
`Dochodzi 5-ta i zaległa cisza.` has two clauses in the gold tree and two subjects,
where olski reads one clause and finds the second subject alone.
None of the five assigns a subject olski contradicts.
Most of the rest are `się`, which the gold tree gives a subject slot
and olski gives no role at all,
and they are the same class the section on the gold reading below counts.
That is the third verdict the check has,
and it exists so that a reading covering less than the gold tree
is not counted as agreeing with it.

Where the gold tree puts a role on a fronted `który`,
olski puts one there too:
the fronted constituent carries the label of the role it fills
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)).
A relative clause or a question reaches this row
on whatever else its reading says, and not on that one label.
The label weighs more in that section than it does here.

The *disagreements* are mostly one class, with a short tail behind it.
The corpus's own notion of a constituent leads them,
and behind it stand a few the check produces rather than the grammar.
No reading a reader would not have stands in this row.
Which classes those are is what this document owns;
how many sentences stand in each is what the run prints.
A particle standing inside a noun phrase does not reach this row,
because the grammar has that position and returns both readings
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#cząstka-ma-dwóch-gospodarzy-i-przy-jednym-dostaje-etykietę)),
where this row is for a reading olski returns alone
and the treebank contradicts.
The shape such a reading takes is a genitive object standing in front of its verb,
and it comes with negation:

```text
Prezes firmy może wyrzucić każdego pracownika, premier większości nie może ruszyć.
```

There the object is also a genitive modifier of the noun phrase before it,
so `premier większości` reads as one subject
where the clause has a subject and an object.
Both readings are shapes Polish has, and both are shapes olski has:
the object belongs to the infinitive under a modal,
and it has a body in front of the finite verb
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze)),
so the sentence is refused for its ambiguity
rather than accepted on the reading a reader does not take.
That body accepts no sentence at all, so this row is all it bought,
and the section it is linked to prices it.

Three sentences of this shape stand outside this row:
this one on that body, and two on the four word orders,
which is what those bought here beyond the sentences they accepted.
`Apostołowie tego nie praktykowali.` now comes out with two readings,
the reader's among them, so it is refused rather than read backwards.
`Nikt niczego nie wybiera, coś wybiera za nas.` went further:
the substantival pronoun takes no genitive after it
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)),
which leaves the second reading nowhere to stand,
and the one left agrees with the gold tree.

A few are the check and not a reading, and what makes them one
is the gold tree marking no slot at all where olski names a role.
`Powtarzaj je tak często, jak to jest potrzebne.` is one:
the chosen tree leaves the imperative's object unmarked,
so olski names an object the tree neither confirms nor contradicts.
`Co pan sądzi o pomyśle Pawła Piskorskiego?` is the same shape with a reason:
the tree marks `Co` as `nonch`, which is a phrase outside the frame,
and olski reads it for an object.
What the row cannot do is tell either of those
from `Poprzednio pracodawca mógł z tym zwlekać nawet 15 lat.`,
where olski reads a duration as an object and is simply wrong.

The rest are extents, and the first is the one the treebank's own formalism
produces:

```text
Policja prowadzi w tej sprawie intensywne śledztwo.
```

Olski reads `w tej sprawie` as an adjunct of the verb
and the object as `intensywne śledztwo`.
The gold tree makes the object span the phrase and the noun together.
The annotators read the phrase as belonging to the investigation,
and GFJP builds constituents out of adjacent material,
so a phrase read that way from in front of its noun
has nowhere to sit but inside the object.
Polish modifies a noun with a prepositional phrase only from behind it
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
so the span the tree records is not a phrase olski could offer,
and what separates the two here is the corpus's constituency requirement
rather than an attachment olski chose.

Several more are that same requirement met from the other side:
in `Od dwu tygodni nie mam od ciebie listu!`,
`Byłam po cesarce i miałam z tym kłopoty.`
and `W swoim dawnym kształcie kapelusz nie ostał się.`
the gold span takes in a prepositional phrase olski hangs on the clause,
and another is the same about a relative clause:
in `Rolę teoretyków spełniają felietoniści, którzy co tydzień fundują szkoły
i formułują programy.` the gold subject runs to the end of the sentence
where olski's stops at the first conjunct.
One more is the same about a second object rather than a phrase:
in `Widzę, że ostatnia lekcja czegoś was nauczyła.`
`nauczyć` governs a genitive beside its accusative,
olski has one object position,
so `czegoś` has nowhere to stand and falls into the subject in front of it.
That sentence and the one about `Co` are what the four word orders
cost in this column, against the two they took out of it above.

Two are neither the check nor an extent, and both stand on a participle:
`W Hongkongu zmarły cztery osoby zarażone wirusem ptasiej grypy.`
has the participle in the gold tree's subject and in olski's predicative,
the attributive participle being a construction olski lacks
([subset.md](subset.md#what-it-does-not-cover-yet)),
so the analysis ran as far as the next missing position.

Drugie stoi na szyku i przyszło razem z ciągiem współrzędnym wyrażeń przyimkowych
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#wyrażenie-przyimkowe-koordynuje-się-tak-jak-grupa-imienna)):
w `W Tokio, Sydney i w Londynie rekordy spodziewane są dopiero dzisiaj.`
drzewo wzorcowe orzeka imiesłowem o rekordach,
a olski czyta go przydawką za rzeczownikiem i bierze `rekordy spodziewane` za podmiot.
Czytania, które ma czytelnik, gramatyka nie ma czym wydać:
orzecznika przed jego kopulą nie bierze, więc `Rekordy spodziewane są.`
nie ma wyprowadzenia, a czytanie przydawkowe zostaje w tym zdaniu samo.
Jest to ten sam brak, o którym mówi
[przyjąć koszt](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
widziany od strony zgodności, a nie od strony liczby czytań;
ruch trzyma [todo/](../todo/README.md).

Drop the positions that hang a prepositional phrase on a noun or on an adjective —
`wyrażenie_przyimkowe` under `człon_imienny` and under `człon_przymiotnikowy`,
and the bodies that put it
over a whole coordination
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#nothing-above-a-coordination-distributes-into-it)),
which together are the attachment
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
leaves to the reader —
and this row grows by an order of magnitude,
almost every one of them an attachment.
Acceptance goes the other way and grows by hundreds of sentences,
most of them ones olski reports as ambiguous with those positions in place,
so the positions trade several hundred sentences the grammar stops accepting
for a couple of hundred readings not taken backwards,
and the sentence the corpus caught the problem on first shows how:

```text
Przybysze z najnowszej fali na ogół stronią od polonijnych organizacji społecznych.
```

Four readings, differing in the subject and in what the modifier is.
The subject that swallows the adverbial `na ogół` is among them,
and it is what a grammar with one attachment position returns alone.
Beside the reading that leaves the adverbial to the clause
it is a report the writer can act on
rather than an analysis handed over with confidence.

A second kind of wrong reading is what the valency restriction keeps out,
and this sentence is where it was read:

```text
Kwitnie handel paszportami.
```

`paszportami` is instrumental,
a nominal predicative is a noun phrase in that case,
so a grammar recording no valency
has the trade predicated of passports rather than blooming in them.
Two things keep that reading out and neither is about the predicative.
`Kwitnąć` takes no instrumental,
which is what the copula's frame says, the copula being the lexicon's hand-written entry
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
and the verb-initial order with a predicative takes the agreeing one alone,
which is a second refusal of the same reading.
The sentence itself now derives, and derives the way a reader reads it:
the instrumental is an adjunct, admitted as a position of its own
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)),
so what the restriction refuses is the predicative and not the sentence.
Dropped from the frame — every valency class gaining `inst`,
the verb-initial position left as it stands —
the restriction costs dozens of sentences every reading they had
and about half as many again their second,
and most of the first group are one mistake:
`Zapisał nuty, przemówił do mnie szyfrem.`,
`W minionym tygodniu miastem wstrząsnęło tragiczne wydarzenie.`
and `Wieczorem ruszyły tramwaje.` beside the sentence above,
each an instrumental adjunct read as what its verb predicates.
The rest carry a copula the closed list does not have —
`stawać się` and `okazywać się`, which the two sentences below name —
and how they divide between the two classes is a reading of them
rather than a count this run takes:
the gold roles it compares are the subject and the object,
and a predicative read where an adjunct stands moves neither.
Dozens fewer accepted and most of them no longer read backwards
is the trade this section is for.

That second class is the price of the list rather than of the restriction:

```text
Mao stał się na wiele lat przywódcą największego narodu na kuli ziemskiej.
Człowiek staje się wyleniałym tygrysem.
```

`Stawać się` predicates an instrumental exactly as `zostawać` does,
and the closed list of copulas
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej))
does not carry it,
so a sentence with either verb is refused by a lexicon entry that is missing
rather than by a decision anybody took.
[todo/](../todo/README.md) holds them.

The rest of the lexicon — every entry but the copula's —
moves dozens of sentences here and moves them the same way.
`Zażarta walka trwała kilkadziesiąt minut.` was accepted
with `kilkadziesiąt minut` for an object,
`trwać` takes no accusative object,
and olski has no accusative adjunct to read it as instead,
so the sentence goes from read backwards to rejected.
About half of them lose the only reading they had,
which is the same trade again at many times the count,
a quarter go from ambiguous to rejected,
and the rest keep a reading beside the one the lexicon took.
The run the lexicon moves furthest is the live one,
under [what morphological ambiguity costs](#what-morphological-ambiguity-costs).

## Złote czytanie ocalało w niemal każdym zdaniu wieloznacznym

Zdanie wieloznaczne olski odrzuca,
a samo odrzucenie nie mówi, czy wśród czytań jest to, którego chce czytelnik.
Ten sam bank drzew odpowiada na to ostrzejsze pytanie
i takie zadaje ewaluacja Świgry
([swigra.md](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)):
czy wśród czytań jest to, które wybrali anotatorzy.
Odpowiada na nie las, a nie lista czytań.
Lista urywa się na `MAX_READINGS`,
a wieloznaczne są dokładnie te zdania, na których ta granica pada,
więc odpowiedź policzona po liście myliłaby brak czytania z jego numerem;
`Las.ma_czytanie` w `olski/parse/las.py` pyta o to las.

Miarą są role, czyli to, czym mierzy zgodność sekcja wyżej.
Nawiasowanie miarą być nie może, bo dwie gramatyki grupują materiał każda po swojemu
i sekcja wyżej pokazuje, na czym:
fraza przyimkowa przed rzeczownikiem siedzi w tym banku wewnątrz dopełnienia,
bo konstytuent buduje się tam z sąsiadów.
Rola jest natomiast tym, co obie gramatyki orzekają o zdaniu, a nie o sobie.
Pytanie brzmi więc: czy któreś czytanie obsadza podmiot i dopełnienie tak,
jak obsadza je drzewo wzorcowe, i czy obsadza oba naraz —
czytanie z dobrym podmiotem i cudzym dopełnieniem złotym czytaniem nie jest.

Nad zdaniami wieloznacznymi, którym drzewo wzorcowe nazywa choć jedną rolę,
złote czytanie ocalało w przeszło czterech na pięć,
a przepada w mniej niż co piątym.
Zdania wieloznaczne, którym drzewo wzorcowe nie nazywa ani jednej roli,
przebieg liczy osobno pod tym wierszem z tego samego powodu,
dla którego liczy tam zdania przyjęte bez roli do porównania.

Odrzucenie za wieloznaczność jest więc odrzuceniem wobec liczby czytań,
a nie wobec tego, co w nich stoi.
Sekcja wyżej mówi to samo o jednym zdaniu i mówi to z ręki:
`Apostołowie tego nie praktykowali.`
wychodzi dwoma czytaniami, a czytanie czytelnika jest wśród nich.
Przebieg mówi to o wszystkich naraz i przelicza się razem z gramatyką.

Ile odpowiedź `survives` jest warta, mówi dopiero numer czytania obok niej.
Czytanie drugie z dwóch i czytanie tysięczne z dwudziestu ośmiu tysięcy
wchodzą do tego wiersza jednakowo, a wypisanych czytań jest `MAX_READINGS`,
więc numer rozstrzyga, czy czytelnik złote czytanie w ogóle zobaczy.
Ocalenie i numer liczy razem ewaluacja Świgry
([swigra.md](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)).
Numerem jest miejsce w kolejności, w jakiej las wydaje drzewa,
i nadaje go samo wyliczanie (`Las.numer_czytania` w `olski/parse/las.py`),
bo numer policzony obok byłby tą kolejnością wypisaną drugi raz.

Tam, gdzie złote czytanie ocalało, jest nim w trzech wypadkach na cztery
czytanie pierwsze, czyli to, które czytelnik widzi na górze wydruku,
a reszta stoi niżej.
Jedno jedyne wypada poza wypisywane czytania i wypada głęboko:
stoi kilkakrotnie dalej niż granica wydruku, więc na wydruku go nie ma.
Numer jest zarazem ceną, bo wyliczanie buduje tyle drzew, ile on wynosi:
rusza dopiero po odpowiedzi lasu, że takie czytanie tam jest,
i przystaje na pierwszym takim drzewie.
Zdanie z wiersza `lost` nie buduje więc ani jednego drzewa,
a granica z `MAX_READINGS` nie jest wyliczaniu potrzebna.
Numer nie rośnie przy tym z wielkością lasu:
złote czytanie największego z tych lasów jest w nim pierwsze.

Drzewo wzorcowe obsadza zaimkiem `który` podmiot albo dopełnienie zdania względnego,
a olski wyprowadza te zdania dokładnie tak, jak czyta je bank drzew,
i tak samo je nazywa, bo czoło niesie etykietę roli, którą zajmuje
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)).
Bez tej etykiety rozdanie ról wychodziłoby o tę jedną rolę uboższe
i złotemu nie równałoby się nigdy, a wiersz `lost` liczyłby kilkadziesiąt zdań więcej —
i byłby to odczyt o mierze, a nie o gramatyce,
bo etykieta nie zmienia ani jednego czytania ani jednego z tych zdań.
Tą samą miarą płacą zdania z gniazdem `np(part)` w wierszu `disagrees` wyżej,
i [todo/](../todo/README.md) trzyma tamto.

To, co po złotym czytaniu zostaje, rozkłada się na cztery klasy,
a dwie z nich wiersze zgodności wyżej już opisują.
Pierwsza to zdanie albo bezokolicznik w miejscu podmiotu,
czyli to samo, co daje tam `partial`:
w `Zdaje się, że w tym miejscu jaskinia uchodzi w nieskończoność.`
podmiotem `zdaje się` jest w drzewie wzorcowym całe zdanie z `że`,
a w `Wystarczy wpłacić pieniądze na specjalne konto.` — fraza bezokolicznikowa.
Druga to rozpiętość, czyli to samo, co daje tam `disagrees`:
w `Spojrzałem na kobietę i stwierdziłem, że po raz pierwszy jej twarz zasługiwała na uwagę.`
złoty podmiot obejmuje `jej twarz`, a olski zatrzymuje go na `twarz`,
i w tę samą stronę idzie `Stali wśród namiotów, w których krzątali się nadwołżańscy
Niemcy, zruszczeni po wiekach.`, gdzie złoty podmiot sięga apozycji.
Trzecia to cząstka `się`, której bank drzew daje rolę podmiotu,
a olski nie daje jej żadnej: `Docelowo myśli się o rozbudowie tego systemu`
jest w tym zapisie zdaniem bez podmiotu.
Reszta to rola obsadzona po jednej stronie i pusta po drugiej.
`chwilę` w `Szli chwilę w milczeniu i Helena spostrzegła, że kierują się w stronę
plebanii.` i `7 dni` w `Produkcja idzie 7 dni w tygodniu.`
są biernikiem czasu, którego olski nie ma czym czytać poza dopełnieniem
([subset.md](subset.md#what-it-does-not-cover-yet)).
`Opróżnia więzienie Qasr ze wszystkich kryminalistów.` rozcina na dwie role frazę,
której polszczyzna tam nie rozcina: `więzienie` wychodzi w dopełnieniu,
a `Qasr ze wszystkich kryminalistów` w podmiocie,
bo apozycji olski nie ma i `więzienie Qasr` nie ma się czym wyprowadzić w całości.

Przysłówek dołożył do tej listy klasę własną i jest ona jedną z rozpiętości:
`Dlatego właśnie przed laty do Monako przenosili się masowo szwedzcy tenisiści.`
wychodzi z podmiotem `masowo szwedzcy tenisiści`,
bo przysłówek stopniowany dochodzi do przymiotnika, a bank drzew zostawia go zdaniu
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy)).

Miara porównuje przy tym dwie role i nic poza nimi.
Czytanie, które je obsadza tak jak drzewo wzorcowe,
może się od niego różnić okolicznikiem, przydawką albo granicą członu,
a wiersz `survives` policzy je razem z tymi, które zgadzają się w całości.
Zawyżenie jest więc możliwe i nie jest zmierzone —
ile go jest, powiedziałaby dopiero miara nad kształtem,
a tej dwie gramatyki nie mają na czym oprzeć.

## What morphological ambiguity costs

The second run is the same measurement with Morfeusz on the raw text
instead of the gold tags, and with the exclusion below in force.
Ambiguity is where the cost lands.
Rejection barely moves between the two runs
and acceptance falls by a couple of hundred sentences,
where several hundred more come out with more than one reading —
a few per cent of the 13,035 measured, and the run prints the three counts.
That share is the rate to watch as the grammar grows,
since every construction admitted gives the analyser's spare readings
one more place to derive something.

The live column depends on two exclusions the gold column has no use for,
the annotators having already chosen one reading per token.
The second of them drops the post-prepositional form of a pronoun
wherever no preposition stands in front of it,
and what it is worth is measured where it is argued
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)).
The first is the one this section is about.
Olski drops an uninflected noun reading
wherever the form also reads as a closed-class word,
for the reasons
[warstwa-leksykalna.md](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not) gives.
`do` is the form that makes it worth doing:
the corpus's ninth commonest token and its fourth commonest preposition,
1,706 occurrences among 151,525,
every one of which Morfeusz also reads as the musical note.
Leave those readings in and the live column loses acceptances to ambiguity:
dozens of those ambiguities are readings nobody can have meant,
and dropping them leaves each of those sentences with exactly one.

Nad zdaniami anotowanymi wykluczenie sięga 22 form i 2 298 tokenów,
licząc `do` i `Do` za jedną formę.
Prawie cała ta liczba to dwie pozycje:
`do` z 1 704 tokenami i zaimek — `go`, `mi`, `te` — z 443.
Reszta jest w większości nazwiskami.
`Tam`, `Tylko`, `Tym` i `Ponieważ` Morfeusz zna każde jako nazwisko,
nieodmienne w rodzaju żeńskim,
więc zdanie zaczynające się którymkolwiek z tych słów
dostaje rzeczownik, który stanie w nim gdziekolwiek.

Zaimek kupuje nad tym korpusem jednoznaczność kilkudziesięciu zdaniom wieloznacznym
i zabiera wyprowadzenie kilkunastu, z czego dwóm przyjętym.
Zabrane stały na czytaniu, które ta pozycja zdejmuje —
`Nie było go wtedy w domu.` wychodziło dwoma czytaniami,
a w obu gra `go` była podmiotem albo orzecznikiem —
więc odrzucenie jest nad nimi werdyktem prawdziwym,
czyli tym, czego [kierunek toru](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)
żąda od werdyktu.

Six times in the corpus the exclusion removes the reading
the annotators themselves chose:
`La` four times, `Amen` once, and `Go` once in the name of a festival.
That is both the shape of the mistake it can make
and the rate at which it makes it.

It also turns a confidently wrong acceptance into a rejection,
and one is the whole count, which is why the sentence is quoted rather than tallied.
That outcome is the worst this measurement has, so buying off even one is worth it:

```text
Tylko wyszła z koła dwa razy.
```

`Tylko` is the adverb, but Morfeusz also offers the surname,
indeclinable exactly as the note is,
so it satisfies the accusative an object wants.
Without the exclusion olski finds that reading, finds no other,
and reports one reading of a sentence whose adverb it has read as an object.
Rejecting is what the grammar should say about a sentence it cannot analyse,
and a single reading is the one verdict a writer takes at face value.

`Tylko` arrived with the grammar rather than with the dictionary:
`dwa razy` is a noun phrase only since
[the numeral phrase](konstrukcje-gramatyczne/grupa-imienna.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
was admitted, and it is what gives the surname an object position to fill.
So what this exclusion is worth grows as the grammar does,
which is the argument for it stated as a rate rather than as a count:
every construction admitted gives an uninflected noun one more place to stand.
Two sentences left this count the other way, each when the grammar
gave it a second reading:
`Tam siedzi nasz umrzyk.`, where the surname reading no longer stands alone,
and `To państwo Kaczyńscy wiedzą i rządu do dymisji nie podadzą.`,
which stood on `do` itself read as the object of `podadzą`
until `rządu do dymisji nie podadzą` came out
as an object in front of a subjectless clause
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Without the exclusion each of them comes out ambiguous rather than
confidently wrong, so the exclusion buys it the reading a reader has
instead of buying a rejection.

Where the exclusion does not reach is a competing noun that inflects:

```text
Do zwykłego koła wystarczy sam sznurek.
```

Two readings with it and the same two without it,
so the exclusion reaches nothing here.
They agree that `Do zwykłego koła` is the fronted modifier the gold tree has
and that `sam sznurek` is the subject,
and differ over `sam` alone,
which Morfeusz reads as the adjective and as the self-service shop.
The criterion asks for a reading that inflects for nothing
and the shop declines like any other noun,
so the sentence stays out of olski on a reading no reader of it has.

One reading Polish does not have is refused by the grammar and not by the lexicon,
and the live column is the run with that refusal in force.
The substantival pronoun takes no genitive after it
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)),
and without that condition dozens of these sentences carry
a second reading, a few of them their only one —
`Weźmy dzieje sztuki tego okresu.`,
`Od tego momentu jest naszym pośrednikiem.` —
where `tego` is once the adjective in front of its noun
and once a pronoun governing it.
It costs a few sentences their acceptance,
`Wymaga to odpowiedniej polityki informacyjnej rządu.` being one of them,
and turns a couple more from ambiguous into rejected,
of which one is why that price is not a cost either:

```text
Dotyczy to wszystkich kategorii zawodowych.
```

Two readings without the condition,
and both read `to wszystkich kategorii zawodowych` as one noun phrase.
Polish has `to` as the subject
and the genitive as what `dotyczyć` governs,
which is a production olski does not have,
so both stood on a phrase nobody wrote,
and rejecting is what the grammar should say about a sentence it cannot analyse.

A difference between two totals is not a set of sentences,
and here a difference of a couple of hundred stands
on several hundred disagreements in both directions.
Most of what either run accepts the other accepts too.
Beyond that, live accepts a hundred and more sentences that gold does not,
and gold accepts several times as many that live leaves unsettled,
finding most of them ambiguous and rejecting the rest.

The sentences live accepts alone are the warning in that comparison,
and a large part of them turn on the reading
[the valency lexicon](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej) refuses:

```text
To są oczywistości.
```

Gold tags call `To` a `pred`, which olski reads as the linker,
and the sentence derives on either morphology
by the order standing the linker in front of a finite copula
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#przy-kopuli-ten-sam-łącznik-ma-trzy-szyki-a-zgodność-wybiera-podmiot)).
What Morfeusz adds is `subst:sg:acc:n`,
which stands exactly where an accusative object stands,
so a grammar recording no valency reads the sentence as OVS as well
and hands back two readings where the frame leaves one.
`Być` takes no accusative object,
and the frame is what says so.

Give the copula the frame every other verb has
and dozens of sentences change verdict, which is what they lose to it.
Most of them lose a reading the frame rejects —
`To są oczywistości.`, `Jest to ciekawy umysł, niepopularny umysł.` —
whether it was the only one they had or the second beside it,
and every one names an object no reader of the sentence has.
That is the trade `Tam siedzi nasz umrzyk.` above is quoted for,
at many times the count.

The rest it settles rather than refuses,
the reading it removes being the one they are otherwise ambiguous against:
`W tobie jest niebo i piekło.`, `W środku nie było nic.`, `Gdzie jest kierownik?`
None of it happens under gold morphology and no verdict there moves,
the annotators having chosen one reading per token.

The agreement check cannot see any of it:
under live morphology the parser numbers positions in characters
while the gold tree numbers them in tokens,
so `harness.pomiar --morphology live` reports no agreement column at all
rather than a wrong one.
The live figure is therefore the weaker of the two measurements,
and where they disagree the gold one is the one to trust.

One tagset caveat.
Składnica's tags are NKJP's and Morfeusz 2's are its own,
and the reader translates the four names they differ on
[above](#where-the-analyses-stop),
so the two blocker rankings carry the same labels.
What stays asymmetric is the live run's `ign` row —
hundreds of sentences stopped on a form Morfeusz does not know —
which the gold run cannot have.
The live blocker is also less precise than it looks:
a rejected sentence stopped because *no* reading of that form could continue,
and where the gold run has one reading to name
the live run has several and names the first.
The two rankings are comparable in substance but not label by label.

Neither column comes from a tagger.
Morfeusz analyses and does not choose,
so the live column holds its readings minus the exclusion above,
and the gold column holds an annotator's answer rather than a program's.
How much of the gold column a tagger recovers is a third figure neither run has,
and it is the one that says what
[the uniqueness property](subset.md#validity-is-uniqueness-not-just-derivability)
costs outside a treebank.
[Concraft](prior-art.md#polish-language-resources) is the candidate for taking it.

## What this number is not

It is not coverage of Polish.
Składnica's trees are by construction drawn from Świgra's output,
so a coverage figure against it measures agreement with GFJP's analysed Polish.
It is a fair yardstick for a grammar that shares GFJP's assumptions,
it flatters any grammar that shares them more closely,
and it understates one that does not.
The 41% of forests with no gold tree is the visible edge of the same problem.

It is not measured against an error-free gold tree.
Every forest was verified by two annotators independently
with a third settling the disagreements, and the two agreed on 88% of utterances.
Woliński then sampled 100 verified trees and found errors in 18,
several of them carrying more than one:
six attached a subordinate somewhere evidently wrong,
eight called a required phrase loose or the other way round,
four carried a plainly wrong structure, and the remainder were single cases.
He read the two leading classes as the ones to expect,
prepositional phrases attaching in several places
and the required-versus-loose call being unclear or arbitrary,
which is the pair that names
[the classes olski's own ambiguity falls into](disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca).
The sample dates from the first stage of the corpus,
so it fixes a rate at a moment rather than describing this release.
The source is Woliński,
*Automatyczna analiza składnikowa języka polskiego*, 2019, §6.6,
which [swigra.md](swigra.md#sources) lists.

What that costs a figure here is bounded by what the figure reads.
These runs compare two roles and ignore the rest of the tree,
so a wrong modifier host cannot move them and a wrong subject can,
and the required-versus-loose call reaches them
wherever it decides which phrase is the object.
The direction is not knowable from the rate either:
a wrong gold tree can cost olski a match it deserved
or hand it one it did not.

It is not a check on where a constituent decision came from either.
An analysis agreeing with GFJP scores the same here
whether it was derived or inherited,
so this number cannot tell those apart,
and [swigra.md](swigra.md#którędy-gfjp-wchodzi-do-olskiego)
owns what follows for a grammar written beside GFJP's own resources.

It is also not a measurement of style.
The retired rule pack
[wanted paired human and generated Polish](linter.md#the-thing-that-makes-or-breaks-it-calibration)
and would have measured firing rates;
this measures what the grammar derives.
The two are different numbers and neither substitutes for the other.
