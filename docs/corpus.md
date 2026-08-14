# Measuring against Składnica

The grammar in [subset.md](subset.md) admits a subset of Polish on purpose.
This document is how much of a subset,
measured rather than asserted.

For the theory behind the measurement,
see the coverage curve in [design-notes.md](design-notes.md);
the tooling is `olski/corpus.py` and `olski/coverage.py`.

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
olski-corpus Składnica-frazowa-180723/
olski-corpus Składnica-frazowa-180723/ --morphology live
```

Between them those two runs print most of what this document quotes
and not all of it.
The commonest forms under each blocker,
the comparison of the two runs' accepted sets,
the counts with the dictionary exclusion switched off,
the `prep`, particle and numeral rows and the disagreement row
with a group of productions dropped,
the rows those sentences land in when the productions come back,
the sentences a narrowed production stops accepting,
and the count of notation tokens in the corpus
are taken by hand against the same corpus,
and a change to the grammar moves them along with the tables.
What puts them outside the command is that each wants
a per-sentence verdict rather than a total,
and half of them want two runs compared rather than one printed;
[TODO.md](../TODO.md) holds what it would take to stop rewriting those scripts.

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

| | sentences | |
| --- | --- | --- |
| rejected | 11,307 | 86.7% |
| valid | 1,179 | 9.0% |
| ambiguous | 549 | 4.2% |

By length, which is the shape the curve actually has:

| tokens | valid |
| --- | --- |
| 1–5 | 25.9% |
| 6–10 | 11.8% |
| 11–20 | 1.5% |
| 21–40 | 0.1% |
| 41+ | 0.0% |

So olski is a subset of short declarative Polish and nothing else,
and coverage falls off a cliff between ten and twenty tokens.
That is the honest starting point of the curve,
and the point of recording it is that the next tier has something to beat.

The last row is ten sentences, which is every sentence the treebank has
above forty segments, and olski rejects all ten.
They cost under a mebibyte each and a third of a second together,
against a run that takes half a minute,
so leaving them out buys nothing and the denominator is the whole annotated corpus.

## Where the analyses stop

Every rejected sentence stopped on some token,
and its part of speech names the construction
that would have to be admitted next.
Ranked, that is a work queue ordered by how much Polish each addition buys:

| stopped on | sentences | commonest forms |
| --- | --- | --- |
| `interp` | 2,932 | `-` (1,265), `.` (775), `–` (275) |
| `adv` | 1,992 | `Jak` (72), `Teraz` (57), `bardzo` (56) |
| `part` | 1,577 | particles: `się` (142), `Czy` (115), `już` (107) |
| `conj` | 663 | coordination: `I` (141), `Ale` (130), `A` (127) |
| `ger` | 513 | gerunds: `przyjęcie` (8), `głosowania` (6), `zabranie` (5) |
| `comp` | 510 | subordinators: `że` (90), `Gdy` (39), `Jeśli` (37) |
| `pred` | 410 | `to` (134), `To` (97), `można` (37) |
| `praet` | 366 | `był` (15), `udało` (9), `były` (7) |
| `subst` | 246 | `to` (7), `skład` (3), `kto` (3) |
| `ppas` | 243 | `wymienionych` (3), `zawarte` (3), `połamanymi` (2) |

The first two rows account for two fifths of the rejections
without touching the interesting questions
about discontinuity and formal power at all:
of clause-level punctuation olski has the comma and nothing else,
and of adverbs none.

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
so two constructions the grammar *has* fire here not once.
That is what the four names are worth —
1,179 sentences accepted rather than 771,
and three rows of this table, `qub` at 2,672, `psubst` at 442 and `padj` at 378,
naming a tag where a construction is what a row is for.
Only the gold column moves with them:
the live column's tags come from Morfeusz to begin with.

What a row does not say is how much admitting its construction buys,
and negation is the measurement of that.
Drop [negation](subset.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)
and the particle row reads 2,150, led by `nie` (422) and `Nie` (308).
Putting it back takes 199 of those off the rejected list —
all of them out of this row and none out of any other —
leaves the row at 1,577 with `się` in front,
and moves the remaining 374 rightward onto another blocker without accepting them.
A sentence carries more than one missing construction,
and the row counts where an analysis stopped
rather than what admitting the construction buys.
The numeral says the same thing from the other end:
drop it and its own row reads 507 and ranks fifth,
every sentence the numeral phrase takes back comes out of that row and none out
of another, and it takes a quarter of them.
So a row does say which sentences an addition can reach —
it just does not say how many of them it will take.
What the two rankings promise against what they deliver is priced in
[roadmap.md](roadmap.md#etap-6-reszta-konstrukcji).

One entry says where a construction the grammar *has* stops short of Polish,
and it heads the particle row.
`się` leads it at 142:
the reflexive is admitted after its verb,
and Polish puts it before one as readily.

A preposition does not rank in this table at all,
and two groups of productions are why.
Drop the one that puts a modifier in front of the clause
and a `prep` row ranks second at 2,048 sentences, led by `W` (665) and `Na` (252),
capitalized because a fronted modifier opens its sentence.
Drop instead the positions that hang a prepositional phrase on a noun or on an
adjective — `Modifier` under `NPConjunct` and under `APConjunct`, which are the
attachment
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
leaves to the reader — and the row reads 425, `z` (108) and `w` (107) in front.
With both in place it reads 215, `w` (54) and `z` (53) in front,
which is a preposition standing where no rule reaches
rather than a construction the grammar lacks.

The dash at the top of the `interp` row is not a stray:
it is dialogue and reported speech,
which is what a corpus drawn from newspapers and prose is full of
and what technical documentation has none of.
That row is a reminder that the corpus is not drawn from olski's register,
and a construction frequent here is not automatically worth admitting.

The queue was ranked on a treebank,
and the register olski is aimed at can be asked whether it agrees.
Its own README is Polish documentation, so it answers:

```sh
python3 -m harness.markdown README.md --into proza/
python3 -m olski.check proza/README.txt
```

Six sentences of that README derive once, and three derive twice.
The three are one class between them, which `--readings` is what shows:
two readings olski has and a reader does not.
Two hang a prepositional phrase where either the noun or the verb could host it,
and the third reads a nominative as an accusative,
which are the two classes
[open-questions.md](open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
counts over a whole register.
What stops the rest is the table above in another order:
the colon and the adverb at the front, subordinators just behind them,
then the Polish form Morfeusz does not know,
and gerunds last.
The numeral stood between the subordinators and that form and stands there no longer,
the grammar having it
([subset.md](subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)),
and what it left behind is the digit:
`2` stops one sentence of this file, which is the half of the class that stays out.
The subordinator standing there is the one that opens an adverbial clause,
`gdy` and `zanim` rather than `że`,
the `że` clause being what a verb takes
([subset.md](subset.md#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej)).
Admitting it moved neither of the two counts above,
which is this paragraph's point taken from the other side:
every sentence of this file that stood on a `że` clause stood on something else too.
That order is read off the words the run names,
which is a classification by hand rather than a second command.
The comma, the past tense and the numeral stand in neither ranking,
the grammar having them,
and the punctuation left here is the colon that opens a clause.
The past tense left the count where it found it and changed which sentences make it:
`Czarna lista kupowała jednak co innego, niż obiecywała.` derives now,
and `Pierwsze i czwarte dzieli sam szyk,
a podmiot jednego jest dopełnieniem drugiego.` has two readings where it had one,
because Morfeusz reads `dzieli` as a past-tense plural
and a plural subject then has a verb to agree with.
The treebank ranked the construction first and this file rates it at nothing,
which is the difference between the two measurements in one sentence.
The ranking names the token each parse stopped on
and this names every word no production takes,
which is coarser and puts the same constructions in front,
so the queue holds in a register the corpus does not contain.
Six rejected sentences have no such word at all —
`Reszta repozytorium to notatki projektowe, przegląd pola,
plan i otwarte pytania.` —
which is that coarseness in the open:
every word there is one some production takes,
and what stops the sentence is the shape they are in.
The run says which is which rather than leaving it to be worked out:
a rejected sentence names the words no production takes,
or says that nothing derives it when every word is one some production does,
which is those six.

That order is not the order of what an addition buys.
Both rankings count the sentences a construction stopped,
which is not the count of sentences admitting it would accept,
and here the two come apart.
Most of the sentences the run rejects carry two classes or more:
the adverb in
`a wyznaczenie go przez wykluczanie jest nieporównanie tańsze`
stands beside two gerunds,
and a production for it, added by itself,
leaves that sentence exactly where it stands,
so what the classes together come to
is not read off the rows and gets measured when they are written.
`Każdy werdykt przychodzi z czytaniem, które go wydało,
a to samo wejście dwa razy daje tę samą odpowiedź.` is that measurement taken:
it carried the past tense and a numeral, both are admitted,
and the sentence is still rejected —
it is the sixth of the six below, stopped now on the shape its words are in
rather than on any word.

Where a sentence carries one class alone, the list still does not settle it,
because a sentence can also fail on the shape its words are in.
Six of the rejected sentences fail that way and carry no unlicensed word at all,
and one class carries two sentences of its own —
`Po to ta czarna lista tu stała i cały wywód za nią dalej stoi.`
and the sentence about what a past tense and a dropped subject come from
are stopped by an adverb and by nothing else.
That pair is measured against a grammar the adverb was written into,
and neither sentence is bought — each failing the other way.
The first derives twice, because the reading the adverb gives it
hangs `za nią` on two heads at once.
The second is left with no unlicensed word and with no derivation either,
which is how those six fail rather than how a row predicts.
A sentence standing on a single class is therefore not a sentence an addition takes,
whichever way the class is counted,
and what the whole of that measurement came to is in
[subset.md](subset.md#przysłówek-zmierzono-przed-dopisaniem-i-drugi-gospodarz-odbiera-39-zdań).

One sentence of this file did carry a single class as the whole of it, and it is the
sentence this run has bought.
`Działają dwie rzeczy` needed the numeral and nothing else,
so admitting the numeral phrase moved it from rejected to one reading,
and it is the sixth sentence in the count above.
That is the only prediction either ranking has made here that could be checked
against the addition that followed it,
and the reason it could be made at all was
[the valency lexicon](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej):
`dwie rzeczy` is nominative or accusative and a subjectless clause takes an object,
so without the entry saying `działać` takes none
the numeral would have made this sentence ambiguous rather than accepted.

What the gerund would cost is the dictionary's to decide rather than the grammar's,
and on this file it comes to nothing.
A word like `wejście` carries a `ger` reading beside its `subst` one,
so a production admitting a gerund as the head of a noun phrase
gives a sentence built on one a second derivation of the same shape,
differing in nothing a reader could act on.
Two derivations of one shape are
[one reading](subset.md#co-się-liczy-jako-jedno-czytanie),
so such a sentence is accepted either way.
That was measured on a sentence this README no longer carries,
and what it establishes is about the dictionary rather than about the sentence.

One thing in that run belongs to the register and not to the queue.
A form Morfeusz does not know stops a sentence,
and gold morphology leaves a treebank no such form to rank,
which is why [subset.md](subset.md#what-it-does-not-cover-yet) owns it.
It is a demand on the grammar that this register makes and the treebank cannot,
and it is the reason to take this run at all
rather than to read the table alone.

Half of that demand is met, and this run is what says which half is worth meeting.
The notation the register writes —
`docs/linter.md`, `CLAUDE.md`, `harness/markdown.py` —
reaches the grammar as one indeclinable noun rather than as five segments
([subset.md](subset.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)),
and two of the six sentences accepted here rest on it,
as do both of the two that derive twice.
What is left is the inflected Polish word Morfeusz lacks —
`commitów`, `Pythonem` —
which is the class the ordering above puts behind the subordinators.
That the notation had to be found here rather than in the treebank
is the register difference in one figure:
eight tokens of it occur in these 13,035 sentences,
web addresses and `10.000zł` and `II.16`,
so nothing in the live column below turns on it.

That run is the grammar track's other instrument beside this treebank.
The track has no exit criterion
([roadmap.md](roadmap.md#readme-jest-przyrządem-pomiarowym)),
so what the run prices is each addition rather than a distance to a finish.
What it counts as a sentence is what the run reports as one:
the entries of the document list arrive as paragraphs no full stop closes,
so they come back `fragment` rather than `rejected`
and stand outside the denominator.
[extraction.md](extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem)
owns that class and how much of this register it is.

## Agreement, which matters more than acceptance

Accepting a sentence proves nothing if the reading is wrong.
Olski admits every order the subject, the object and the verb can stand in
([subset.md](subset.md#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery)),
so on every sentence it accepts
there is a live question of whether it found the subject the annotators did.
The gold trees mark this directly:
a required phrase carries its valency slot,
and `subj(np(nom))` is the subject.

On the 876 accepted sentences where the gold tree marks a role to compare:

| | sentences | |
| --- | --- | --- |
| agrees | 845 | 96.5% |
| partial | 18 | 2.1% |
| disagrees | 13 | 1.5% |

The denominator is 876 and not 1,179
because the other 303 accepted sentences have no role to compare against:
a pro-drop sentence like `Wstaje.` realizes no subject,
so the gold tree marks none and there is nothing to check.
The report prints that count under the table
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
That is the third verdict the check has,
and it exists so that a reading covering less than the gold tree
is not counted as agreeing with it.

One of the thirteen *disagrees* is a reading a reader would not have,
and the other twelve are the check or the corpus rather than the grammar.
The one came in with negation:

```text
Prezes firmy może wyrzucić każdego pracownika, premier większości nie może ruszyć.
```

The genitive object stands in front of its verb,
and there it is also a genitive modifier of the noun phrase before it,
so `premier większości` comes out as one subject
where the clause has a subject and an object.
Both readings are shapes Polish has,
and only the second is a shape *olski* has:
the object belongs to the infinitive under a modal,
and the bodies that put an object in front of its verb
put it in front of a finite one
([subset.md](subset.md#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery)),
so the reading a reader takes has no body to be derived by
and the wrong one is returned alone rather than beside it.
That is the cost negation is priced at here,
and it lands in this table rather than in the ambiguity column:
[subset.md](subset.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)
holds what it buys and what it takes.

Two sentences of this shape were in this row and left it,
which is what the four word orders bought here beyond the sentences they accepted:
`Apostołowie tego nie praktykowali.`
and `Nikt niczego nie wybiera, coś wybiera za nas.`
now come out with two readings, the reader's among them,
so they are refused rather than read backwards.

Five more are the check and not a reading.
`Kampania nie przyniosła skutku.` olski reads the way a reader would,
and the gold tree gives the genitive of negation its own slot, `np(part)`,
which `_slot_role` in `olski/corpus.py` maps to no role olski has,
so olski names an object where the tree marks none.
The numeral phrase in object position lands in the same slot,
as in `Marzec przyniósł 6 zagranicznych delegacji.`,
and so does the object of `Co pan sądzi o pomyśle Pawła Piskorskiego?`,
which the four orders brought in and which olski reads
with `Co` for an object and `pan` for a subject.
[TODO.md](../TODO.md) holds that as a defect in the check
rather than in the reading, and the row carries those five until it is fixed.

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

Three more are that same requirement met from the other side:
in `Od dwu tygodni nie mam od ciebie listu!`,
`Byłam po cesarce i miałam z tym kłopoty.`
and `W swoim dawnym kształcie kapelusz nie ostał się.`
the gold span takes in a prepositional phrase olski hangs on the clause,
and the fourth is the same about a relative clause:
in `Rolę teoretyków spełniają felietoniści, którzy co tydzień fundują szkoły
i formułują programy.` the gold subject runs to the end of the sentence
where olski's stops at the first conjunct.
A fifth is the same about a second object rather than a phrase:
in `Widzę, że ostatnia lekcja czegoś was nauczyła.`
`nauczyć` governs a genitive beside its accusative,
olski has one object position,
so `czegoś` has nowhere to stand and falls into the subject in front of it.
That sentence and the one about `Co` are what the four word orders
[cost in this column](subset.md#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery),
against the two they took out of it above.
One is neither the check nor an extent:
`W Hongkongu zmarły cztery osoby zarażone wirusem ptasiej grypy.`
has the participle in the gold tree's subject and in olski's predicative,
the attributive participle being a construction olski lacks
([subset.md](subset.md#what-it-does-not-cover-yet)),
so the analysis ran as far as the next missing position.

Drop the positions
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
takes prepositional attachment to demand —
the 44 productions in which an adjunct stands beside something else,
or a modifier hangs on a phrase that already carries one or on a participle —
and this row holds 121 sentences instead of thirteen,
almost every one of them an attachment.
Accepted goes the other way, 1,426 instead of 1,179,
so those positions buy 108 fewer readings taken backwards
for 247 sentences the grammar stops accepting,
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

A second kind of wrong reading is missing from the table,
because the grammar refuses the sentences it stood on outright:

```text
Kwitnie handel paszportami.
```

`paszportami` is instrumental,
a nominal predicative is a noun phrase in that case,
so a grammar recording no valency
has the trade predicated of passports rather than blooming in them.
Two things keep it out and neither is about the predicative.
`Kwitnąć` takes no instrumental,
which is what the copula's frame says, the copula being the lexicon's hand-written entry
([subset.md](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
and the verb-initial order with a predicative takes the agreeing one alone,
which is a second refusal of the same sentence.
Dropped from the frame — every valency class gaining `inst`,
the verb-initial position left as it stands —
the restriction costs 75 sentences every reading they had,
and 73 of the 75 are one mistake:
`Zapisał nuty, przemówił do mnie szyfrem.`,
`Dwójka ratowników wyruszyła śmigłowcem na patrol.`
and `Podróżnik podzielił się ze słuchaczami wrażeniami ze swego rejsu.`
beside the sentence above,
each an instrumental adjunct read as what its verb predicates.
Seventy-five fewer accepted and seventy-three fewer read backwards
is the trade this section is for.

The other two are the price of the list rather than of the restriction:

```text
Mao stał się na wiele lat przywódcą największego narodu na kuli ziemskiej.
Człowiek staje się wyleniałym tygrysem.
```

`Stawać się` predicates an instrumental exactly as `zostawać` does,
and the closed list of copulas
([subset.md](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej))
does not carry it,
so these two are refused by a lexicon entry that is missing
rather than by a decision anybody took.
[TODO.md](../TODO.md) holds them.

The rest of the lexicon — every entry but the copula's —
moves 22 sentences here and moves them the same way.
`Zażarta walka trwała kilkadziesiąt minut.` was accepted
with `kilkadziesiąt minut` for an object,
`trwać` takes no accusative object,
and olski has no accusative adjunct to read it as instead,
so the sentence goes from read backwards to rejected.
Seventeen of the 22 lose the only reading they had,
which is the same trade again at seventeen times the count,
and the other five keep a reading beside the one the lexicon took.
The run the lexicon moves furthest is the one below.

## What morphological ambiguity costs

The same run with Morfeusz on the raw text instead of the gold tags,
and with the exclusion below in force:

| | gold | live |
| --- | --- | --- |
| rejected | 11,307 | 11,128 |
| valid | 1,179 | 1,063 |
| ambiguous | 549 | 844 |

Ambiguity is where the cost lands:
256 more sentences carry more than one reading,
which is 2.0% of the 13,035 measured.
That is the rate to watch as the grammar grows,
since every construction admitted gives the analyser's spare readings
one more place to derive something.

The live column depends on an exclusion the gold column has no use for,
the annotators having already chosen one reading per token.
Olski drops an uninflected noun reading
wherever the form also reads as a function word,
for the reasons
[subset.md](subset.md#the-dictionary-offers-readings-polish-does-not) gives.
`do` is the form that makes it worth doing:
the corpus's ninth commonest token and its fourth commonest preposition,
1,706 occurrences among 151,525,
every one of which Morfeusz also reads as the musical note.
Leave those readings in and the live column reads 11,179, 1,025 and 821.
Thirty-two of those 821 ambiguities are readings nobody can have meant,
and dropping them leaves each of those sentences with exactly one.

Across the annotated sentences the exclusion reaches 19 forms
and 1,851 tokens, all but 150 of them `do`.
Most of the rest is surnames:
`Tam`, `Tylko`, `Tym` and `Ponieważ` are each one in Morfeusz's dictionary,
indeclinable in the feminine,
so a sentence opening on any of those words
hands olski a noun it can put anywhere.

Five times in the corpus the exclusion removes the reading
the annotators themselves chose: `La` four times and `Amen` once.
That is both the shape of the mistake it can make
and the rate at which it makes it.

It also turns two confidently wrong acceptances into rejections,
and two is the whole count, which is why the sentences are quoted rather than tallied.
That outcome is the worst this measurement has, so buying off even one is worth it:

```text
Tam siedzi nasz umrzyk.
Tylko wyszła z koła dwa razy.
```

`Tam` is the adverb, but Morfeusz also offers the surname,
indeclinable exactly as the note is,
so it satisfies the accusative an object wants.
Without the exclusion olski finds that reading, finds no other,
and reports one reading of a sentence whose adverb it has read as an object.
Rejecting is what the grammar should say about a sentence it cannot analyse,
and a single reading is the one verdict a writer takes at face value.

`Tylko` is the same mistake with a different word and it arrived with the grammar
rather than with the dictionary: `dwa razy` is a noun phrase only since
[the numeral phrase](subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
was admitted, and it is what gives the surname an object position to fill.
So what this exclusion is worth grows as the grammar does,
which is the argument for it stated as a rate rather than as a count:
every construction admitted gives an uninflected noun one more place to stand.

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
([subset.md](subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)),
and without that condition thirty of these sentences carry
a second reading, four of them their only one —
`Weźmy dzieje sztuki tego okresu.`,
`Od tego momentu jest naszym pośrednikiem.` —
where `tego` is once the adjective in front of its noun
and once a pronoun governing it.
It costs two acceptances, `Wymaga to odpowiedniej polityki informacyjnej rządu.`
being one of them,
and turns two more sentences from ambiguous into rejected,
of which one is why that count is not a cost either:

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
and here a 116-sentence difference stands on 416 disagreements.
The two runs accept the same 913 sentences.
Live accepts 150 that gold rejects,
and gold accepts 266 that live does not settle on:
182 it finds ambiguous, 84 it rejects.

The 150 are the warning in the table,
and the largest single class of it is the one
[the valency lexicon](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej) refuses:

```text
To są oczywistości.
```

Gold tags call `To` a `pred`, olski has no rule for one,
and the sentence is rejected on either morphology.
What Morfeusz adds is `subst:sg:acc:n`,
which stands exactly where an accusative object stands,
so a grammar recording no valency reads the sentence as OVS,
finds one such reading, and calls it valid.
`Być` takes no accusative object,
and the frame is what says so.

Sixty-two sentences of this corpus lose a reading to that frame,
and nineteen of them lose the only one they had,
so the frame is what rejects them —
`To są oczywistości.`, `W środku nie było nic.`, `To są babskie histerie.`
Every one of them names an object no reader of the sentence has.
That is the trade `Tam siedzi nasz umrzyk.` above is quoted for,
at twenty times the count.

Fifteen more the frame settles rather than refuses,
the reading it removes being the one they are otherwise ambiguous against:
`W tobie jest niebo i piekło.`, `To jest złe myślenie.`,
`Podczas zjazdu zostały wybrane nowe władze.`
The remaining twenty stay ambiguous with fewer readings.
None of it happens under gold morphology and no verdict there moves,
the annotators having chosen one reading per token.

The agreement check cannot see any of it:
under live morphology the parser numbers positions in characters
while the gold tree numbers them in tokens,
so `olski-corpus --morphology live` reports no agreement column at all
rather than a wrong one.
The live figure is therefore the weaker of the two measurements,
and where they disagree the gold one is the one to trust.

One tagset caveat.
Składnica's tags are NKJP's and Morfeusz 2's are its own,
and the reader translates the four names they differ on
[above](#where-the-analyses-stop),
so the two blocker tables carry the same labels.
What stays asymmetric is the live run's `ign` row —
529 sentences stopped on a form Morfeusz does not know —
which the gold run cannot have.
The live blocker is also less precise than it looks:
a rejected sentence stopped because *no* reading of that form could continue,
and where the gold run has one reading to name
the live run has several and names the first.
The blocker tables are comparable in substance but not label by label.

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

It is also not a measurement of style.
The retired linter track
[wanted paired human and generated Polish](linter.md#the-thing-that-makes-or-breaks-it-calibration)
and would have measured firing rates;
this measures what the grammar derives.
The two are different numbers and neither substitutes for the other.
