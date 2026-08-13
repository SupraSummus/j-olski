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
the `prep` row and the disagreement row with a group of productions dropped,
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

Gold morphology, whole corpus, every sentence of 40 tokens or fewer:

| | sentences | |
| --- | --- | --- |
| rejected | 11,921 | 91.5% |
| valid | 746 | 5.7% |
| ambiguous | 358 | 2.7% |

By length, which is the shape the curve actually has:

| tokens | valid |
| --- | --- |
| 1–5 | 17.7% |
| 6–10 | 7.1% |
| 11–20 | 0.7% |
| 21–40 | 0.1% |

So olski is a subset of short declarative Polish and nothing else,
and coverage falls off a cliff between ten and twenty tokens.
That is the honest starting point of the curve,
and the point of recording it is that the next tier has something to beat.

## Where the analyses stop

Every rejected sentence stopped on some token,
and its part of speech names the construction
that would have to be admitted next.
Ranked, that is a work queue ordered by how much Polish each addition buys:

| stopped on | sentences | commonest forms |
| --- | --- | --- |
| `interp` | 2,665 | `-` (1,253), `.` (599), `–` (274) |
| `qub` | 2,641 | particles: `się` (874), `nie` (318), `Nie` (308) |
| `adv` | 1,438 | `Teraz` (57), `bardzo` (43), `Potem` (41) |
| `conj` | 594 | coordination: `I` (141), `Ale` (130), `A` (127) |
| `psubst` | 441 | nominal pronouns: `to` (100), `tym` (45), `Co` (42) |
| `comp` | 413 | subordinators: `że` (60), `Gdy` (39), `Jeśli` (37) |
| `ger` | 413 | gerunds: `przyjęcie` (8), `głosowania` (6) |
| `padj` | 376 | adjectival pronouns: `który` (49), `które` (42) |
| `pred` | 354 | `to` (124), `To` (97), `Trzeba` (24) |
| `praet` | 331 | `był` (9), `udało` (9), `został` (5) |

The first two rows account for nearly half of the rejections
without touching the interesting questions
about discontinuity and formal power at all.
The particle row is `się` before its verb rather than after it,
and `nie`, which is the negation this grammar has no rule for;
of clause-level punctuation olski has the comma and nothing else.

The past tense headed this table at 2,934 and heads it no longer,
and the difference between those two numbers is what a row does not say.
Admitting it moved 566 of those 2,934 sentences off the rejected list,
left 297 of them stopping here,
and moved the remaining 2,071 sentences' blockers rightward without accepting them:
a sentence carries more than one missing construction,
and the row counts where an analysis stopped
rather than what admitting the construction buys.
It also cost more formal machinery than this table's ranking assumed,
which [subset.md](subset.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku) owns.
What it is worth against the register olski is aimed at
is a separate question, and the run below answers it with zero.

The `praet` row reads 331 rather than those 297,
and the 34 between them are sentences another addition pushed onto it,
which is the same effect seen from the other end:
a row moves when a construction it does not name is admitted.
The numeral is what moved it, and the numeral left this table altogether.
Its row held 453 sentences, ranked fifth, and led on `dwa` (14) and `Kilka` (14);
admitting [the numeral phrase](subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
moved 91 of them off the rejected list, 56 to one reading and 35 to several,
and moved the remaining 362 rightward onto `interp`, `qub` and `praet`
without accepting them.
Every one of the 91 came out of this row and none out of another,
so a row does say which sentences an addition can reach —
it just does not say how many of them it will take.
What the two rankings promise against what they deliver is priced in
[roadmap.md](roadmap.md#etap-6-reszta-konstrukcji).

One entry says where a construction the grammar *has* stops short of Polish,
and it heads the particle row.
`się` leads it at 874:
the reflexive is admitted after its verb,
and Polish puts it before one as readily.

A preposition does not rank in this table at all,
and two groups of productions are why.
Drop the one that puts a modifier in front of the clause
and a `prep` row ranks third at 1,971 sentences, led by `W` (665) and `Na` (252),
capitalized because a fronted modifier opens its sentence.
Drop instead the positions that hang a prepositional phrase on a noun or on an
adjective — `Modifier` under `NPConjunct` and under `APConjunct`, which are the
attachment
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
leaves to the reader — and the row reads 370, `w` (94) and `z` (94) in front.
With both in place it reads 155, `z` (39) and `w` (38) in front,
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
eight tokens of it occur in these 13,025 sentences,
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
Olski admits both SVO and OVS,
so on every sentence it accepts
there is a live question of whether it found the subject the annotators did.
The gold trees mark this directly:
a required phrase carries its valency slot,
and `subj(np(nom))` is the subject.

On the 549 accepted sentences where the gold tree marks a role to compare:

| | sentences | |
| --- | --- | --- |
| agrees | 541 | 98.5% |
| partial | 5 | 0.9% |
| disagrees | 3 | 0.5% |

The denominator is 549 and not 746
because the other 197 accepted sentences have no role to compare against:
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

None of the three *disagrees* is an attachment olski chose, and each fails differently.
The first is the one the treebank's own formalism produces:

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

The other two arrived with the numeral phrase and neither is about the numeral.
`W Hongkongu zmarły cztery osoby zarażone wirusem ptasiej grypy.`
has the participle in the gold tree's subject and in olski's predicative,
the attributive participle being a construction olski lacks
([subset.md](subset.md#what-it-does-not-cover-yet)),
so the numeral carried the analysis as far as the next missing position.
`Marzec przyniósł 6 zagranicznych delegacji.` olski reads the way a reader would,
and the disagreement is in the comparison:
the gold tree gives a numeral phrase in object position its own slot, `np(part)`,
which `_role` in `olski/corpus.py` maps to no role olski has,
so there is no gold object to agree with.
[TODO.md](../TODO.md) holds that as a defect in the check
rather than in the reading, and the row reads three until it is fixed.

Drop the positions
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
takes prepositional attachment to demand —
the 30 productions in which an adjunct stands beside something else,
or a modifier hangs on a phrase that already carries one or on a participle —
and this row holds 82 sentences instead of three,
every one of them an attachment.
Accepted goes the other way, 909 instead of 746,
so those positions buy 79 fewer readings taken backwards
for 163 sentences the grammar stops accepting,
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
Dropped wherever it stands, the restriction costs four of the sentences
this corpus would otherwise accept, and the four are one mistake:
`Abakanowicz pracuje seriami.`,
`Zygmunt biegnie drugim chodnikiem.`
and `O delfinach może mówić godzinami.` beside the sentence above,
each an instrumental adjunct read as what its verb predicates.
Three of the four are the frame's alone, the sentence above being the position's.
Four fewer accepted and four fewer read backwards is the trade this section is for.

The rest of the lexicon moves one sentence here and it moves it the same way.
`Pracujemy nad tą grupą dzień i noc.` was accepted with `dzień i noc` for an object,
`pracować` takes no accusative object,
and olski has no accusative adjunct to read it as instead,
so the sentence goes from read backwards to rejected.
One fewer accepted and one fewer read backwards is the same trade again,
and it is the whole of what the lexicon moves under gold morphology:
no sentence loses a reading it had beside a true one,
because the annotators chose one reading per token.
The run the lexicon moves is the one below.

## What morphological ambiguity costs

The same run with Morfeusz on the raw text instead of the gold tags,
and with the exclusion below in force:

| | gold | live |
| --- | --- | --- |
| rejected | 11,921 | 11,388 |
| valid | 746 | 925 |
| ambiguous | 358 | 712 |

Ambiguity is where the cost lands:
354 more sentences carry more than one reading,
which is 2.7% of the 13,025 measured.
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
Leave those readings in and the live column reads 11,382, 895 and 748.
Thirty-two of those 748 ambiguities are readings nobody can have meant,
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
and without that condition six of these sentences carry
a second reading —
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
and here a 193-sentence difference stands on 473 disagreements.
The two runs accept the same 550 sentences.
Live accepts 333 that gold rejects,
and gold accepts 140 that live does not settle on:
105 it finds ambiguous, 35 it rejects.

The 333 are the warning in the table,
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

Fifty-five sentences of this corpus lose a reading to that frame,
and twenty of them lose the only one they had,
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
Składnica's tags are NKJP's, Morfeusz 2's are its own,
and they differ on names olski's report shows:
`qub` in the gold run is `part` in the live one,
and the live run has an `ign` row — 510 sentences stopped on a form
Morfeusz does not know — that the gold run cannot have.
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
