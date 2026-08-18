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
the count of notation tokens in the corpus,
both figures about the gold role the relative pronoun carries —
the survival counts with it dropped, and the accepted sentences that have one —
and the readings the largest of the forests keeping a gold reading holds
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
| rejected | 10,710 | 82.2% |
| valid | 1,575 | 12.1% |
| ambiguous | 750 | 5.8% |

By length, which is the shape the curve actually has:

| tokens | valid |
| --- | --- |
| 1–5 | 32.0% |
| 6–10 | 16.5% |
| 11–20 | 2.6% |
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
| `interp` | 3,273 | `-` (1,280), `.` (984), `–` (276) |
| `part` | 1,811 | particles: `się` (214), `już` (123), `też` (115) |
| `conj` | 743 | coordination: `I` (141), `Ale` (130), `A` (127) |
| `ger` | 574 | gerunds: `przyjęcie` (8), `głosowania` (6), `przyjęciem` (5) |
| `comp` | 567 | subordinators: `że` (99), `Gdy` (39), `by` (38) |
| `pred` | 447 | `to` (140), `To` (97), `można` (51) |
| `praet` | 410 | `był` (15), `udało` (9), `było` (8) |
| `subst` | 314 | `to` (9), `skład` (4), `kto` (3) |
| `ppas` | 292 | `zebranych` (3), `wymienionych` (3), `prowadzone` (3) |
| `fin` | 258 | `jest` (40), `mają` (10), `ma` (7) |

The first row alone accounts for three tenths of the rejections
without touching the interesting questions
about discontinuity and formal power at all:
of clause-level punctuation olski has the comma and nothing else.

The adverb led the second row with 1,992 sentences and the row is gone,
the grammar having the construction at both of its hosts
([subset.md](subset.md#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)).
It is the largest single move this table has recorded:
597 sentences left the rejected list,
which is what the rows below have moved up by.

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
1,575 sentences accepted rather than 999,
and three rows of this table, `qub` at 2,959, `psubst` at 484 and `padj` at 433,
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
and a `prep` row ranks second at 2,205 sentences, led by `W` (665) and `Na` (252),
capitalized because a fronted modifier opens its sentence.
Drop instead the positions that hang a prepositional phrase on a noun or on an
adjective — `Modifier` under `NPConjunct` and under `APConjunct`, which are the
attachment
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
leaves to the reader — and the row reads 509, `w` (127) and `z` (125) in front.
With both in place it reads 243, `w` (62) and `z` (57) in front,
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

Six sentences of that README derive once, and five derive more than once.
Four of the five hang a prepositional phrase
where either the noun or the verb could host it,
and one reads a nominative as an accusative,
which are the two classes
[open-questions.md](open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
counts over a whole register;
`--readings` is what shows them, as readings olski has and a reader does not.
One sentence carries both at once and eight readings with them,
the attachment multiplied by the case read twice over,
once in each of its two clauses.
Two of the five arrived with the adverb,
which took them off the rejected list and gave them a second reading
rather than one
([subset.md](subset.md#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)),
and one of those two carries a third class of its own:
Morfeusz reads `sam` as an adverb beside the adjective,
so `Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem
drugiego.` has a reading in which `sam` is an adjunct of the clause.
That is a dictionary reading Polish does not have here,
the class this register shows the same way the treebank shows it on `wobec`.
What stops the rest is the table above in another order:
the colon at the front, subordinators just behind it,
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
The comma, the past tense, the numeral and the adverb stand in neither ranking,
the grammar having them,
and the punctuation left here is the colon that opens a clause.
The past tense left the count where it found it and changed which sentences make it:
`Czarna lista kupowała jednak co innego, niż obiecywała.` derives now,
and `Pierwsze i czwarte dzieli sam szyk,
a podmiot jednego jest dopełnieniem drugiego.` has readings where it had one,
because Morfeusz reads `dzieli` as a past-tense plural
and a plural subject then has a verb to agree with.
The treebank ranked the construction first and this file rates it at nothing,
which is the difference between the two measurements in one sentence.
The ranking names the token each parse stopped on
and this names every word no production takes,
which is coarser and puts the same constructions in front,
so the queue holds in a register the corpus does not contain.
Eight rejected sentences have no such word at all —
`Reszta repozytorium to notatki projektowe, przegląd pola,
plan i otwarte pytania.` —
which is that coarseness in the open:
every word there is one some production takes,
and what stops the sentence is the shape they are in.
The run says which is which rather than leaving it to be worked out:
a rejected sentence names the words no production takes,
or says that nothing derives it when every word is one some production does,
which is those eight.

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
[subset.md](subset.md#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe).

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
([subset.md](subset.md#szyk-zmierzono-kupuje-55-zdań-i-odbiera-sześć)),
so on every sentence it accepts
there is a live question of whether it found the subject the annotators did.
The gold trees mark this directly:
a required phrase carries its valency slot,
and `subj(np(nom))` is the subject.

On the 1,162 accepted sentences where the gold tree marks a role to compare:

| | sentences | |
| --- | --- | --- |
| agrees | 1,117 | 96.1% |
| partial | 24 | 2.1% |
| disagrees | 21 | 1.8% |

The denominator is 1,162 and not 1,575
because the other 413 accepted sentences have no role to compare against:
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

One of the twenty-one *disagrees* is a reading a reader would not have,
eight arrived with the adverb and four of those eight are about it,
and the rest are the check or the corpus rather than the grammar.
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
([subset.md](subset.md#szyk-zmierzono-kupuje-55-zdań-i-odbiera-sześć)),
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
[cost in this column](subset.md#szyk-zmierzono-kupuje-55-zdań-i-odbiera-sześć),
against the two they took out of it above.
One is neither the check nor an extent:
`W Hongkongu zmarły cztery osoby zarażone wirusem ptasiej grypy.`
has the participle in the gold tree's subject and in olski's predicative,
the attributive participle being a construction olski lacks
([subset.md](subset.md#what-it-does-not-cover-yet)),
so the analysis ran as far as the next missing position.

Drop the positions that hang a prepositional phrase on a noun or on an adjective —
`Modifier` under `NPConjunct` and under `APConjunct`, which are the attachment
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
leaves to the reader —
and this row holds 211 sentences instead of 21,
almost every one of them an attachment.
Accepted goes the other way, 2,072 instead of 1,575,
five hundred of them sentences olski reports as ambiguous,
so those positions buy 190 fewer readings taken backwards
for 497 sentences the grammar stops accepting,
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
the restriction costs 46 sentences every reading they had
and 13 more their second,
and 42 of the 46 are one mistake:
`Zapisał nuty, przemówił do mnie szyfrem.`,
`W minionym tygodniu miastem wstrząsnęło tragiczne wydarzenie.`
and `Wieczorem ruszyły tramwaje.` beside the sentence above,
each an instrumental adjunct read as what its verb predicates.
Forty-six fewer accepted and forty-two fewer read backwards
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
moves 34 sentences here and moves them the same way.
`Zażarta walka trwała kilkadziesiąt minut.` was accepted
with `kilkadziesiąt minut` for an object,
`trwać` takes no accusative object,
and olski has no accusative adjunct to read it as instead,
so the sentence goes from read backwards to rejected.
Nineteen of the 34 lose the only reading they had,
which is the same trade again at nineteen times the count,
six go from ambiguous to rejected,
and the other nine keep a reading beside the one the lexicon took.
The run the lexicon moves furthest is the live one,
under [what morphological ambiguity costs](#what-morphological-ambiguity-costs).

## Złote czytanie ocalało w 592 z 650 zdań wieloznacznych

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
`Las.ma_czytanie` w `olski/parse.py` pyta o to las.

Miarą są role, czyli to, czym mierzy zgodność sekcja wyżej.
Nawiasowanie miarą być nie może, bo dwie gramatyki grupują materiał każda po swojemu
i sekcja wyżej pokazuje, na czym:
fraza przyimkowa przed rzeczownikiem siedzi w tym banku wewnątrz dopełnienia,
bo konstytuent buduje się tam z sąsiadów.
Rola jest natomiast tym, co obie gramatyki orzekają o zdaniu, a nie o sobie.
Pytanie brzmi więc: czy któreś czytanie obsadza podmiot i dopełnienie tak,
jak obsadza je drzewo wzorcowe, i czy obsadza oba naraz —
czytanie z dobrym podmiotem i cudzym dopełnieniem złotym czytaniem nie jest.

Nad 650 zdaniami wieloznacznymi, którym drzewo wzorcowe nazywa choć jedną rolę:

| | zdania | |
| --- | --- | --- |
| `survives` | 592 | 91,1% |
| `lost` | 58 | 8,9% |

Pozostałe 100 zdań wieloznacznych drzewo wzorcowe zostawia bez ani jednej roli,
i przebieg liczy je pod tabelą z tego samego powodu,
dla którego liczy tam 413 zdań przyjętych.

Odrzucenie za wieloznaczność jest więc odrzuceniem wobec liczby czytań,
a nie wobec tego, co w nich stoi.
Sekcja wyżej mówi to samo o dwóch zdaniach i mówi to z ręki:
`Apostołowie tego nie praktykowali.`
i `Nikt niczego nie wybiera, coś wybiera za nas.`
wychodzą dwoma czytaniami, a czytanie czytelnika jest wśród nich.
Tabela mówi to o wszystkich naraz i przelicza się razem z gramatyką.

Ile odpowiedź `survives` jest warta, mówi dopiero numer czytania obok niej.
Czytanie drugie z dwóch i czytanie tysięczne z dwudziestu ośmiu tysięcy
wchodzą do tego wiersza jednakowo, a wypisanych czytań jest `MAX_READINGS`,
więc numer rozstrzyga, czy czytelnik złote czytanie w ogóle zobaczy.
Ocalenie i numer liczy razem ewaluacja Świgry
([swigra.md](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)).
Numerem jest miejsce w kolejności, w jakiej las wydaje drzewa,
i nadaje go samo wyliczanie (`Las.numer_czytania` w `olski/parse.py`),
bo numer policzony obok byłby tą kolejnością wypisaną drugi raz.

Nad 592 zdaniami, w których złote czytanie ocalało:

| | zdania | |
| --- | --- | --- |
| czytanie 1 | 434 | 73,3% |
| czytania 2-64 | 158 | 26,7% |

Żadne z nich nie wypada poza wypisywane czytania,
a najgłębsze jest czterdziestym pierwszym.
Tyle też wynosi cena, bo wyliczanie buduje tyle drzew, ile numer:
rusza dopiero po odpowiedzi lasu, że takie czytanie tam jest,
i przystaje na pierwszym takim drzewie.
Zdanie z wiersza `lost` nie buduje więc ani jednego drzewa,
a granica z `MAX_READINGS` nie jest wyliczaniu potrzebna.
Numer nie rośnie przy tym z wielkością lasu:
złote czytanie największego z tych lasów jest w nim pierwsze.

Trzydzieści dwa z 58 przepadło na roli, której olski nie nadaje nikomu.
Drzewo wzorcowe obsadza zaimkiem `który` podmiot albo dopełnienie zdania względnego,
a `RelativeCore` w `olski/subset.py` wysuniętemu zaimkowi etykiety roli nie daje:
wyprowadza on te zdania tak, jak czyta je bank drzew,
i rozdanie wychodzi z niego o tę jedną rolę uboższe, więc złotemu nie równa się nigdy.
Zdejmij tę rolę ze strony złotej, a 27 z tych 32 ocaleje —
wiersz `lost` liczy wtedy 31, a `survives` 619 z 650, czyli 95,2%.
Pozostałych pięć ma obok niej drugą różnicę i zostaje.
Jest to brak etykiety, a nie błąd czytania,
tak samo jak pięć zdań z gniazdem `np(part)` w wierszu `disagrees` wyżej,
i [TODO.md](../TODO.md) trzyma jedno i drugie.
Ta sama luka dochodzi do zdań przyjętych i waży tam mniej.

Trzydzieści jeden, które zostaje, rozkłada się na cztery klasy,
a dwie z nich wiersze zgodności wyżej już opisują.
Siedem to zdanie albo bezokolicznik w miejscu podmiotu,
czyli to samo, co daje tam `partial`:
w `Zdaje się, że w tym miejscu jaskinia uchodzi w nieskończoność.`
podmiotem `zdaje się` jest w drzewie wzorcowym całe zdanie z `że`,
a w `Wystarczy wpłacić pieniądze na specjalne konto.` — fraza bezokolicznikowa.
Sześć to rozpiętość, czyli to samo, co daje tam `disagrees`:
w `Spojrzałem na kobietę i stwierdziłem, że po raz pierwszy jej twarz zasługiwała na uwagę.`
złoty podmiot obejmuje `jej twarz`, a olski zatrzymuje go na `twarz`,
i w tę samą stronę idzie `Stali wśród namiotów, w których krzątali się nadwołżańscy
Niemcy, zruszczeni po wiekach.`, gdzie złoty podmiot sięga apozycji.
Pięć to cząstka `się`, której bank drzew daje rolę podmiotu,
a olski nie daje jej żadnej: `Docelowo myśli się o rozbudowie tego systemu`
jest w tym zapisie zdaniem bez podmiotu.
Reszta to rola obsadzona po jednej stronie i pusta po drugiej.
`chwilę` w `Szli chwilę w milczeniu i Helena spostrzegła, że kierują się w stronę
plebanii.` i `7 dni` w `Produkcja idzie 7 dni w tygodniu.`
są biernikiem czasu, którego olski nie ma czym czytać poza dopełnieniem
([subset.md](subset.md#what-it-does-not-cover-yet)),
a w `W kratkach z cyframi skarbów nie ma.` idzie to w drugą stronę:
dopełnieniem jest tam `skarbów`, czyli dopełniacz negacji, a olski dopełnienia nie obsadza.
`Opróżnia więzienie Qasr ze wszystkich kryminalistów.` rozcina na dwie role frazę,
której polszczyzna tam nie rozcina: `więzienie` wychodzi w dopełnieniu,
a `Qasr ze wszystkich kryminalistów` w podmiocie,
bo apozycji olski nie ma i `więzienie Qasr` nie ma się czym wyprowadzić w całości.

Przysłówek dołożył do tej listy klasę własną i jest ona jedną z rozpiętości:
`Dlatego właśnie przed laty do Monako przenosili się masowo szwedzcy tenisiści.`
wychodzi z podmiotem `masowo szwedzcy tenisiści`,
bo przysłówek stopniowany dochodzi do przymiotnika, a bank drzew zostawia go zdaniu
([subset.md](subset.md#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)).

Miara porównuje przy tym dwie role i nic poza nimi.
Czytanie, które je obsadza tak jak drzewo wzorcowe,
może się od niego różnić okolicznikiem, przydawką albo granicą członu,
a wiersz `survives` policzy je razem z tymi, które zgadzają się w całości.
Zawyżenie jest więc możliwe i nie jest zmierzone —
ile go jest, powiedziałaby dopiero miara nad kształtem,
a tej dwie gramatyki nie mają na czym oprzeć.

## What morphological ambiguity costs

The same run with Morfeusz on the raw text instead of the gold tags,
and with the exclusion below in force:

| | gold | live |
| --- | --- | --- |
| rejected | 10,710 | 10,482 |
| valid | 1,575 | 1,371 |
| ambiguous | 750 | 1,182 |

Ambiguity is where the cost lands:
432 more sentences carry more than one reading,
which is 3.3% of the 13,035 measured.
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
Leave those readings in and the live column reads 10,473, 1,331 and 1,231.
Forty of those ambiguities are readings nobody can have meant,
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
and without that condition 46 of these sentences carry
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
and here a 204-sentence difference stands on 572 disagreements.
The two runs accept the same 1,187 sentences.
Live accepts 184 that gold rejects,
and gold accepts 388 that live does not settle on:
269 it finds ambiguous, 119 it rejects.

The 184 are the warning in the table,
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

Give the copula the frame every other verb has and 63 sentences of this corpus
change verdict, which is what they lose to it.
Twenty-six lose the only reading they had, so the frame is what rejects them —
`To są oczywistości.`, `Jest to ciekawy umysł, niepopularny umysł.` —
and twelve more it takes from ambiguous to rejected.
Every one of them names an object no reader of the sentence has.
That is the trade `Tam siedzi nasz umrzyk.` above is quoted for,
at twenty times the count.

Twenty-five it settles rather than refuses,
the reading it removes being the one they are otherwise ambiguous against:
`W tobie jest niebo i piekło.`, `W środku nie było nic.`, `Gdzie jest kierownik?`
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
598 sentences stopped on a form Morfeusz does not know —
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
