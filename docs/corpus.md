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
the `prep` row with the fronted-modifier production dropped,
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
| rejected | 12,640 | 97.0% |
| valid | 328 | 2.5% |
| ambiguous | 57 | 0.4% |

By length, which is the shape the curve actually has:

| tokens | valid |
| --- | --- |
| 1–5 | 8.6% |
| 6–10 | 2.8% |
| 11–20 | 0.2% |
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
| `interp` | 3,208 | `-` (1,242), `,` (953), `.` (346), `–` |
| `praet` | 2,794 | the past tense: `był` (88), `była`, `było` |
| `qub` | 1,712 | particles: `nie` (545), `się` (334), `czy` |
| `adv` | 1,124 | `teraz` (62), `bardzo`, `potem` |
| `conj` | 474 | coordination: `i` (150), `ale`, `a` |
| `psubst` | 362 | nominal pronouns: `to` (104), `co`, `kto` |
| `num` | 323 | numerals: `kilka` (20), `wielu`, `wiele` |
| `pred` | 307 | `to` (183), `można`, `trzeba` |
| `ger` | 307 | gerunds: `przyjęcie`, `głosowania` |
| `prep` | 234 | `z` (75), `w` (62), `na` |

The first two are the whole answer to "why 2.5%".
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
`się` is second in the particle row at 344:
the reflexive is admitted after its verb,
and Polish puts it before one as readily.

The `prep` row is the one to read against the fronted-modifier production
([subset.md](subset.md#the-open-problem-prepositional-attachment)),
because that production is what keeps it small.
Drop it and the row ranks third at 1,984 sentences, led by `W` and `Na`;
keep it and the 234 that remain are `z` and `w`
in the positions no rule takes.

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

Six sentences of that README derive once, and two derive twice.
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
`Każdy werdykt przychodzi z regułą, która go wydała`
stands in one that also has a numeral and a relative clause.
So a production for the adverb, the past tense or the numeral,
added by itself, leaves the accepted count exactly where it stands,
the gerund puts it one lower,
and all four at once come out below that count rather than above it.
The class at the top of the queue behaves the same way.
`Gramatyka nie jest celem lintera; jest najgłębszym poziomem analizy`
and `Konwencje prozy, kodu, testów i commitów trzyma CLAUDE.md`
are the sentences it alone would unblock,
and each carries clause punctuation as well.
What the list still holds is the comma and the subordinate clause,
and [TODO.md](../TODO.md) holds the finding that over this file
those two arrive together or not at all.

That exception says what else has to arrive.
`Działają dwie rzeczy` needs the numeral and nothing else,
and admitting one makes the sentence ambiguous rather than accepted:
`dwie rzeczy` is nominative or accusative,
a subjectless clause takes an object,
and nothing records that `działać` takes none,
so olski reads two things as acting and as being acted upon.
That is the valency entry in
[subset.md](subset.md#what-it-does-not-cover-yet),
reached from this register rather than from the treebank.

What the gerund costs comes from the dictionary rather than from the grammar.
`wejście` carries a `ger` reading beside its `subst` one,
and a reading is told apart by the part of speech of each word
(`olski/parse.py`),
so a production admitting a gerund as the head of a noun phrase
gives `Wejściem jest zwykły tekst polski` a second reading of the same shape,
differing in nothing a reader could act on.
The run accepts that sentence, so the count falls by one.
This is the class
[subset.md](subset.md#the-dictionary-offers-readings-polish-does-not) owns,
under a criterion that section does not yet have:
the exclusion there asks for a function-word reading beside the noun,
and here both readings are nominal.

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
and three of the six sentences accepted here rest on it,
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

On the 226 accepted sentences where the gold tree marks a role to compare:

| | sentences | |
| --- | --- | --- |
| agrees | 216 | 95.6% |
| disagrees | 9 | 4.0% |
| partial | 1 | 0.4% |

The denominator is 226 and not 328
because the other 102 accepted sentences have no role to compare against:
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

One of the nine got the hard half right:
in `Juniorską reprezentację w najbliższym czasie czekają półfinały ME w Essen`
olski picked `półfinały ME w Essen` as the subject,
which is the annotators' answer and is not the first noun phrase.
The OVS rule earns its place,
and what the sentence is counted wrong for
is the extent of the object rather than which phrase fills it.

All nine are prepositional attachment,
and the corpus found it on the first run:

```text
Przybysze z najnowszej fali na ogół stronią od polonijnych organizacji społecznych.
```

Olski reads the subject as `Przybysze z najnowszej fali na ogół`,
swallowing the adverbial `na ogół` into the noun phrase,
because `NPConjunct → subst Modifier` lets any prepositional phrase attach
to a noun.
`Trwa dochodzenie w tej sprawie` and `Sen w tym wypadku jest najczulszym
instrumentem` lose their subjects the same way,
and `Prowadzę nadzór specjalistyczny do spraw chirurgii dziecięcej na Mazowszu`
loses its object to the opposite mistake,
the phrase reaching the verb where the gold tree gives it to the noun.
The subset owns the fork
([subset.md](subset.md#the-open-problem-prepositional-attachment));
this is the count of what it costs against a treebank.

A tenth kind of wrong reading is missing from the table,
because the grammar refuses the sentences it stood on outright:

```text
Kwitnie handel paszportami.
```

`paszportami` is instrumental,
a nominal predicative is a noun phrase in that case,
and nothing here records which complements a verb takes,
so the trade comes out predicated of passports rather than blooming in them.
What keeps it out is a restriction on the predicative rather than on the verb:
the instrumental one belongs to a closed list of copulas
([subset.md](subset.md#what-the-grammar-covers)).
That restriction costs four of the sentences this corpus would otherwise accept,
and the four are one mistake:
`Abakanowicz pracuje seriami.`,
`Zygmunt biegnie drugim chodnikiem.`
and `O delfinach może mówić godzinami.` beside the sentence above,
each an instrumental adjunct read as what its verb predicates.
Four fewer accepted and four fewer read backwards is the trade this section is for.

The gap they come out of is wider than the restriction.
`To są oczywistości.` below is the same missing valency from the other side,
and [subset.md](subset.md#what-it-does-not-cover-yet) holds what is left of it.

## What morphological ambiguity costs

The same run with Morfeusz on the raw text instead of the gold tags,
and with the exclusion below in force:

| | gold | live |
| --- | --- | --- |
| rejected | 12,640 | 12,411 |
| valid | 328 | 409 |
| ambiguous | 57 | 205 |

Ambiguity is where the tagger's cost lands:
148 more sentences carry more than one reading,
which is 1.1% of the 13,025 measured.
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
Leave those readings in and the live column reads 12,409, 371 and 245.
Thirty-nine of those 245 ambiguities are readings nobody can have meant,
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

Eight readings without it and four with it.
It takes the four that make `Do zwykłego koła` a noun phrase
rather than the fronted modifier the gold tree has,
and leaves four that differ over `sam`,
which Morfeusz reads as the adjective and as the self-service shop,
and over whether `sam sznurek` is the subject of a verb-initial clause
or the object of a pro-drop one.
The criterion asks for a reading that inflects for nothing
and the shop declines like any other noun,
so the sentence stays out of olski on a reading no reader of it has.

A difference between two totals is not a set of sentences,
and here an 81-sentence difference stands on 227 disagreements.
The two runs accept the same 255 sentences.
Live accepts 154 that gold rejects,
and gold accepts 73 that live does not settle on:
62 it finds ambiguous, 11 it rejects.

The 154 are the warning in the table.
At least one is accepted for a reason the annotators would reject:

```text
To są oczywistości.
```

Gold tags call `To` a `pred`, olski has no rule for one, and the sentence is
rejected.
Morfeusz also offers `subst:sg:acc:n`,
so olski reads the sentence as OVS
with `To` as the accusative object of `są`,
finds exactly one such reading, and calls it valid.
`Być` takes no accusative object,
but olski has no valency, so nothing stops it.

Two things follow.
Adding valency would remove this,
and [subset.md](subset.md#what-it-does-not-cover-yet) lists it
beside the past tense.
And the agreement check cannot see any of it:
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
and the live run has an `ign` row — 406 sentences stopped on a form
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
