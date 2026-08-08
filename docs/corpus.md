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
and the counts with the dictionary exclusion switched off
are taken by hand against the same corpus,
and a change to the grammar moves them along with the tables.

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
| rejected | 12,680 | 97.4% |
| valid | 295 | 2.3% |
| ambiguous | 50 | 0.4% |

By length, which is the shape the curve actually has:

| tokens | valid |
| --- | --- |
| 1–5 | 8.3% |
| 6–10 | 2.4% |
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
| `interp` | 3,116 | `-` (1,242), `,` (896), `.`, `–` |
| `praet` | 2,770 | the past tense: `był`, `była`, `było` |
| `qub` | 1,679 | particles: `nie` (542), `się` (327), `czy` |
| `adv` | 1,106 | `teraz`, `bardzo`, `potem` |
| `conj` | 484 | coordination: `i` (158), `ale`, `a` |
| `psubst` | 360 | nominal pronouns: `to`, `co`, `kto` |
| `num` | 321 | numerals: `kilka`, `wielu`, `dwa` |
| `pred` | 307 | `to` (183), `można`, `trzeba` |
| `ger` | 291 | gerunds: `przyjęcie`, `głosowania` |
| `fin` | 230 | `jest` (70), `są` (14), `może` |

The first two are the whole answer to "why 2.3%".
Olski has no past tense and no clause-level punctuation,
and between them they account for nearly half of the rejections
without touching the interesting questions
about discontinuity and formal power at all.
Adding the past tense costs nothing in formal power —
it is another verb form in the `Verb` rule —
which makes it the cheapest large gain available
and the obvious next thing to do.

Two entries say where a construction the grammar *has* stops short of Polish.
`się` is second in the particle row at 327:
the reflexive is admitted after its verb,
and Polish puts it before one as readily.
A finite verb blocks 230 sentences and `jest` is 70 of them,
39 of which carry a nominative or instrumental adjective or noun
immediately in front of the copula:
`Dużą trudnością jest udowodnienie molestowania.`
That is the predicative before its verb,
the order olski has for an object and not for a predicative.

No `prep` row is in that table,
and the rule for a phrase in front of the clause
([subset.md](subset.md#the-open-problem-prepositional-attachment)) is why.
Drop that one production and the row ranks third at 1,954 sentences;
keep it and 192 are left,
`z` and `w` in the positions no rule takes.

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

One sentence of that README derives.
What stops the rest is the table above in another order:
the comma first, where the treebank's row is led by the dash,
then adverbs, the past tense, numerals and gerunds.
The ranking names the token each parse stopped on
and this names every word no production takes,
which is coarser and puts the same constructions in front,
so the queue holds in a register the corpus does not contain.

Two things in that run belong to the register and not to the queue.
A form Morfeusz does not know stops a sentence,
and gold morphology leaves a treebank no such form to rank,
which is why [subset.md](subset.md#what-it-does-not-cover-yet) owns it.
And the command splits that README into more sentences
than the splitter in `olski/document.py` does:
a full stop inside `docs/linter.md` is a boundary for one and not for the other.
That is the splitter rather than the grammar,
and [TODO.md](../TODO.md) holds it.

That run is also what the grammar track is aimed at.
[roadmap.md](roadmap.md#celem-toru-jest-to-readme) makes it the track's exit criterion —
every sentence of that README deriving, and deriving once —
which puts the splitter above in front of the grammar rather than beside it,
a number taken over a bad split measuring the apparatus instead.
The unknown form is the other way round:
it is a demand on the grammar that this register makes and the treebank cannot.

## Agreement, which matters more than acceptance

Accepting a sentence proves nothing if the reading is wrong.
Olski admits both SVO and OVS,
so on every sentence it accepts
there is a live question of whether it found the subject the annotators did.
The gold trees mark this directly:
a required phrase carries its valency slot,
and `subj(np(nom))` is the subject.

On the 200 accepted sentences where the gold tree marks a role to compare:

| | sentences | |
| --- | --- | --- |
| agrees | 191 | 95.5% |
| disagrees | 9 | 4.5% |

The denominator is 200 and not 295
because the other 95 accepted sentences have no role to compare against:
a pro-drop sentence like `Wstaje.` realizes no subject,
so the gold tree marks none and there is nothing to check.
The report prints that count under the table
rather than letting the check quietly narrow its own denominator.

None were *reversed* —
olski never read a subject as an object or the other way round,
which is the failure the uniqueness property exists to prevent
and the one that would have been worst to find.

One of the nine got the hard half right:
in `Juniorską reprezentację w najbliższym czasie czekają półfinały ME w Essen`
olski picked `półfinały ME w Essen` as the subject,
which is the annotators' answer and is not the first noun phrase.
The OVS rule earns its place,
and what the sentence is counted wrong for
is the extent of the object rather than which phrase fills it.

Eight of the nine are prepositional attachment,
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

The ninth is valency:

```text
Kwitnie handel paszportami.
```

`paszportami` is instrumental, a predicative is a noun phrase in that case,
and no rule says `kwitnąć` does not take one,
so olski reads the trade as being predicated of rather than being *in*
passports.
That is the same gap `To są oczywistości.` shows below,
and [subset.md](subset.md#what-it-does-not-cover-yet) lists it as one.

## What morphological ambiguity costs

The same run with Morfeusz on the raw text instead of the gold tags,
and with the exclusion below in force:

| | gold | live |
| --- | --- | --- |
| rejected | 12,680 | 12,453 |
| valid | 295 | 377 |
| ambiguous | 50 | 195 |

Ambiguity is where the tagger's cost lands:
145 more sentences carry more than one reading,
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
Leave those readings in and the live column reads 12,451, 342 and 232.
Thirty-six of those 232 ambiguities are readings nobody can have meant,
and dropping them leaves each of those sentences with exactly one.

Across the annotated sentences the exclusion reaches 19 forms
and 1,854 tokens, all but 150 of them `do`.
Most of the rest is surnames:
`Tam`, `Tylko`, `Tym` and `Ponieważ` are each one in Morfeusz's dictionary,
indeclinable in the feminine,
so a sentence opening on any of those words
hands olski a noun it can put anywhere.

Five times in the corpus the exclusion removes the reading
the annotators themselves chose: `La` four times and `Amen` once.
That is both the shape of the mistake it can make
and the rate at which it makes it.

It also turns one derivation into a rejection,
and the gold tree says that derivation was wrong:

```text
Tam siedzi nasz umrzyk.
```

`Tam` is the adverb, but Morfeusz also offers the surname,
indeclinable exactly as the note is,
and that reading makes it the object of `siedzi` —
the only reading, and so a confident one.
Rejecting is what the grammar should say about a sentence it cannot analyse.

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
and here an 82-sentence difference stands on 210 disagreements.
The two runs accept the same 231 sentences.
Live accepts 146 that gold rejects,
and gold accepts 64 that live does not settle on:
56 it finds ambiguous, 8 it rejects.

The 146 are the warning in the table.
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
and the live run has an `ign` row — 404 sentences stopped on a form
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
