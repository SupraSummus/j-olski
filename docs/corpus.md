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
and a linter is not a download manager.

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
| rejected | 12,626 | 96.9% |
| valid | 299 | 2.3% |
| ambiguous | 100 | 0.8% |

By length, which is the shape the curve actually has:

| tokens | valid |
| --- | --- |
| 1–5 | 8.5% |
| 6–10 | 2.3% |
| 11–20 | 0.1% |
| 21–40 | 0.0% |

So olski is a subset of short declarative Polish and nothing else,
and coverage falls off a cliff at about ten tokens.
That is the honest starting point of the curve,
and the point of recording it is that the next tier has something to beat.

## Where the analyses stop

Every rejected sentence stopped on some token,
and its part of speech names the construction
that would have to be admitted next.
Ranked, that is a work queue ordered by how much Polish each addition buys:

| stopped on | sentences | commonest forms |
| --- | --- | --- |
| `interp` | 3,259 | `-` (1,243), `,` (983), `.` (356), `–` |
| `praet` | 2,849 | the past tense: `był` (92), `była`, `było` |
| `qub` | 1,734 | particles: `nie` (552), `się` (345), `czy` |
| `adv` | 1,133 | `teraz` (62), `bardzo`, `potem` |
| `conj` | 476 | coordination: `i` (153), `ale`, `a` |
| `psubst` | 364 | nominal pronouns: `to` (104), `co`, `kto` |
| `num` | 328 | numerals: `kilka` (20), `wielu`, `wiele` |
| `ger` | 312 | gerunds: `przyjęcie`, `głosowania` |
| `pred` | 309 | `to` (185), `można`, `trzeba` |
| `comp` | 230 | subordinators: `gdy` (40), `jeśli`, `bo` |

The first two are the whole answer to "why 2.3%".
Olski has no past tense and no clause-level punctuation,
and between them they account for nearly half of the rejections
without touching the interesting questions
about discontinuity and formal power at all.
Adding the past tense costs nothing in formal power —
it is another verb form in the `Verb` rule —
which makes it the cheapest large gain available against this corpus.
What it is worth against the register olski is aimed at
is a separate question, and the run below answers it differently.

One entry says where a construction the grammar *has* stops short of Polish.
`się` is second in the particle row at 345:
the reflexive is admitted after its verb,
and Polish puts it before one as readily.

A preposition does not rank in this table at all,
and two groups of productions are why.
Drop the one that puts a modifier in front of the clause
and a `prep` row ranks third at 1,839 sentences, led by `W` (665) and `Na` (252).
Drop instead the adjunct positions
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
takes prepositional attachment to demand, and the row reads 241.
With both in place it reads 59, `z` (15) and `w` (13) in front,
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

Seven sentences of that README derive once, and two derive twice.
What stops the rest is the table above in another order:
the comma first, where the treebank's row is led by the dash,
then the Polish form Morfeusz does not know,
then adverbs, gerunds and the past tense, and numerals last.
The ranking names the token each parse stopped on
and this names every word no production takes,
which is coarser and puts the same constructions in front,
so the queue holds in a register the corpus does not contain.
One rejected sentence has no such word at all —
`Zbiór tekstów przechodzących przez wszystkie reguły jest podzbiorem
polszczyzny w jednym i w drugim przypadku.` —
which is that coarseness in the open:
every word there is one some production takes,
and what stops the sentence is the shape they are in.
The run says which is which rather than leaving it to be worked out:
a rejected sentence names the words no production takes,
or says that nothing derives it when every word is one some production does,
which is the sentence above.

That order is not the order of what an addition buys.
Both rankings count the sentences a construction stopped,
which is not the count of sentences admitting it would accept,
and here the two come apart completely.
Read the rejected sentences the run prints,
and each one carrying a construction from the list carries a second one as well,
bar a single exception:
the adverb in
`Wyznaczenie go przez wykluczanie jest nieporównanie tańsze`
stands in a sentence that also has a gerund and a relative clause,
and the past tense in
`Każdy werdykt przychodzi z tym, co go wydało`
stands in one that also has a numeral and a relative clause.
So a production for the adverb, the past tense, the numeral or the gerund,
added by itself, leaves the accepted count exactly where it stands.
What the four together come to is not read off those four,
since the sentences above carry two of them each,
and it gets measured when they are written.
The class at the top of the queue behaves the same way.
`Konwencje prozy, kodu, testów i commitów trzyma CLAUDE.md`
is the sentence it alone would unblock,
and it carries clause punctuation as well.
What the list still holds is the comma and the subordinate clause,
and [TODO.md](../TODO.md) holds the finding that over this file
those two arrive together or not at all.

That exception says what else has to arrive.
`Działają dwie rzeczy` needs the numeral and nothing else.
Admitting one would once have made the sentence ambiguous rather than accepted,
`dwie rzeczy` being nominative or accusative
and a subjectless clause taking an object,
so olski read two things as acting and as being acted upon.
[The valency lexicon](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)
says `działać` takes no accusative object and that reading is gone,
which leaves the numeral holding the sentence on its own.

What the gerund would cost is the dictionary's to decide rather than the grammar's,
and it comes to nothing.
`wejście` carries a `ger` reading beside its `subst` one,
so a production admitting a gerund as the head of a noun phrase
gives `Wejściem jest zwykły tekst polski` a second derivation of the same shape,
differing in nothing a reader could act on.
Two derivations of one shape are
[one reading](subset.md#co-się-liczy-jako-jedno-czytanie),
so the run accepts that sentence either way.

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
and three of the seven sentences accepted here rest on it,
as does one of the two that derive twice.
What is left is the inflected Polish word Morfeusz lacks —
`lintuje`, `commitów`, `znacznikowym` —
which is the class ranked second above.
That the notation had to be found here rather than in the treebank
is the register difference in one figure:
eight tokens of it occur in these 13,025 sentences,
web addresses and `10.000zł` and `II.16`,
so nothing in the live column below turns on it.

That run is also what the grammar track is aimed at.
[roadmap.md](roadmap.md#celem-toru-jest-to-readme) makes it the track's exit criterion:
every sentence of that README deriving, and deriving once.
What it counts as a sentence is what the run reports as one:
the entries of the document list arrive as paragraphs no full stop closes,
so they come back `fragment` rather than `rejected`
and stand outside the criterion's denominator.
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

On the 199 accepted sentences where the gold tree marks a role to compare:

| | sentences | |
| --- | --- | --- |
| agrees | 197 | 99.0% |
| disagrees | 1 | 0.5% |
| partial | 1 | 0.5% |

The denominator is 199 and not 299
because the other 100 accepted sentences have no role to compare against:
a pro-drop sentence like `Wstaje.` realizes no subject,
so the gold tree marks none and there is nothing to check.
The report prints that count under the table
rather than letting the check quietly narrow its own denominator.

None were *reversed* —
olski never read a subject as an object or the other way round,
which is the failure the uniqueness property exists to prevent
and the one that would have been worst to find.

The one *partial* is `Wystarczy przeanalizować wypowiedzi Adama.`
The gold tree makes the infinitive phrase the subject of `wystarczy`,
and olski reads the clause as subjectless
with the same phrase as what the verb takes,
so it assigns no subject to compare and contradicts nothing either.
That is the third verdict the check has,
and it exists so that a reading covering less than the gold tree
is not counted as agreeing with it.

The one *disagrees* is the one the treebank's own formalism produces:

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

Drop the adjunct positions
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
takes prepositional attachment to demand
and this row holds ten sentences instead of one,
every one of them an attachment.
That is what those positions buy,
at the price in accepted sentences the table above carries,
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
| rejected | 12,626 | 12,411 |
| valid | 299 | 382 |
| ambiguous | 100 | 232 |

Ambiguity is where the tagger's cost lands:
132 more sentences carry more than one reading,
which is 1.0% of the 13,025 measured.
That is the answer to a question [subset.md](subset.md) leaves open —
how much of olski's uniqueness property survives a real tagger —
and the rate to watch as the grammar grows,
since every construction admitted gives the tagger's spare readings
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
Leave those readings in and the live column reads 12,409, 369 and 247.
Fourteen of those 247 ambiguities are readings nobody can have meant,
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

It also turns one confidently wrong acceptance into a rejection,
and one is the whole count, which is why the sentence is quoted rather than tallied.
That outcome is the worst this measurement has, so buying off even one is worth it:

```text
Tam siedzi nasz umrzyk.
```

`Tam` is the adverb, but Morfeusz also offers the surname,
indeclinable exactly as the note is,
so it satisfies the accusative an object wants.
Without the exclusion olski finds that reading, finds no other,
and reports one reading of a sentence whose adverb it has read as an object.
Rejecting is what the grammar should say about a sentence it cannot analyse,
and a single reading is the one verdict a writer takes at face value.

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
and without that condition four of these sentences carry
a second reading —
`Weźmy dzieje sztuki tego okresu.`,
`Od tego momentu jest naszym pośrednikiem.` —
where `tego` is once the adjective in front of its noun
and once a pronoun governing it.
The condition turns one sentence from ambiguous into rejected,
and that sentence is why the count is not a cost:

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
and here an 83-sentence difference stands on 199 disagreements.
The two runs accept the same 241 sentences.
Live accepts 141 that gold rejects,
and gold accepts 58 that live does not settle on:
48 it finds ambiguous, 10 it rejects.

The 141 are the warning in the table,
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

Twelve sentences of this corpus stand on that reading,
and the frame takes it off all twelve.
Eleven have nothing else, so the frame is what rejects them —
`Ten syfon jest jego.`, `W tobie jest niebo i piekło.`,
`Nie jest to łatwe zadanie.` — and the twelfth stands on it twice over.
Every one of them names an object no reader of the sentence has:
`To nie` in one, `Ale` in another, `Kiedy` in a third.
That is the trade `Tam siedzi nasz umrzyk.` above is quoted for,
at eleven times the count.

Five more sentences the frame settles rather than refuses,
the reading it removes being the one they are otherwise ambiguous against:
`Powód jest prosty.`, `Jaki jest skutek?`, `To jest jedno pytanie.`
Ten stay ambiguous with fewer readings,
and one derives that otherwise derives not at all,
`Zawarte na wideokasecie wypowiedzi mogą być interesującym materiałem`,
which is the instrumental predicative reaching an infinitive
for the reason [subset.md](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej) gives.
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
and the live run has an `ign` row — 414 sentences stopped on a form
Morfeusz does not know — that the gold run cannot have.
The live blocker is also less precise than it looks:
a rejected sentence stopped because *no* reading of that form could continue,
and where the gold run has one reading to name
the live run has several and names the first.
The blocker tables are comparable in substance but not label by label.

## What this number is not

It is not coverage of Polish.
Składnica's trees are by construction drawn from Świgra's output,
so a coverage figure against it measures agreement with GFJP's analysed Polish.
It is a fair yardstick for a grammar that shares GFJP's assumptions,
it flatters any grammar that shares them more closely,
and it understates one that does not.
The 41% of forests with no gold tree is the visible edge of the same problem.

It is also not a per-rule measurement.
The calibration harness in [roadmap.md](roadmap.md) needs paired human
and generated Polish and measures firing rates;
this measures what the grammar derives.
The two are different numbers and neither substitutes for the other.
