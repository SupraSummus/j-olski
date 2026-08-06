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
| rejected | 12,815 | 98.4% |
| valid | 196 | 1.5% |
| ambiguous | 14 | 0.1% |

By length, which is the shape the curve actually has:

| tokens | valid |
| --- | --- |
| 1–5 | 6.3% |
| 6–10 | 1.2% |
| 11–20 | 0.1% |
| 21–40 | 0.0% |

So olski is a subset of short declarative Polish and nothing else yet,
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
| `interp` | 2,762 | `-` (1,232), `,` (643), `–`, `"` |
| `praet` | 2,214 | the past tense: `był`, `była`, `miał` |
| `prep` | 1,941 | `w`, `na`, `z`, `po` — a prepositional phrase where no rule takes one |
| `qub` | 1,430 | particles: `nie` (476), `się` (231), `czy` |
| `adv` | 981 | `teraz`, `bardzo`, `potem` |
| `conj` | 671 | coordination: `i` (306), `ale`, `a` |
| `pred` | 275 | `to` (171), `można`, `trzeba` |

The first two are the whole answer to "why 1.5%".
Olski has no past tense and no clause-level punctuation,
and between them they account for a third of the rejections
without touching the interesting questions
about discontinuity and formal power at all.
Adding the past tense costs nothing in formal power —
it is another verb form in the `Verb` rule —
which makes it the cheapest large gain available
and the obvious next thing to do.

The dash at the top of the `interp` row is not a stray:
it is dialogue and reported speech,
which is what a corpus drawn from newspapers and prose is full of
and what technical documentation has none of.
That row is a reminder that the corpus is not drawn from olski's register,
and a construction frequent here is not automatically worth admitting.

## Agreement, which matters more than acceptance

Accepting a sentence proves nothing if the reading is wrong.
Olski admits both SVO and OVS,
so on every sentence it accepts
there is a live question of whether it found the subject the annotators did.
The gold trees mark this directly:
a required phrase carries its valency slot,
and `subj(np(nom))` is the subject.

On the 112 accepted sentences where the gold tree marks a role to compare:

| | sentences | |
| --- | --- | --- |
| agrees | 108 | 96.4% |
| disagrees | 4 | 3.6% |

The denominator is 112 and not 196
because the other 84 accepted sentences have no role to compare against:
a pro-drop sentence like `Wstaje.` realizes no subject,
so the gold tree marks none and there is nothing to check.
The report prints that count under the table
rather than letting the check quietly narrow its own denominator.

None were *reversed* —
olski never read a subject as an object or the other way round,
which is the failure the uniqueness property exists to prevent
and the one that would have been worst to find.

One of the four is worth noting for what it got right:
in `Juniorską reprezentację w najbliższym czasie czekają półfinały ME w Essen`
olski picked `półfinały ME w Essen` as the subject,
which is the annotators' answer and is not the first noun phrase.
The OVS rule earns its place.

The four disagreements are all the same over-generation,
and the corpus found it on the first run:

```text
Przybysze z najnowszej fali na ogół stronią od polonijnych organizacji społecznych.
```

Olski reads the subject as `Przybysze z najnowszej fali na ogół`,
swallowing the adverbial `na ogół` into the noun phrase,
because `NP → subst Modifier` lets any prepositional phrase attach to a noun.
Worse, it reads it *unambiguously*:
the `Predicate` rules take at most one `Modifier`,
which `od polonijnych organizacji społecznych` has already used,
so the adverbial has nowhere else to go
and the wrong reading is the only reading.
The grammar's own narrowness hid the ambiguity
that would otherwise have caused the sentence to be rejected —
which is a caution about reading `valid` as `correct`
anywhere the grammar is this incomplete.

## What morphological ambiguity costs

The same run with Morfeusz on the raw text instead of the gold tags,
and with the exclusion below in force:

| | gold | live |
| --- | --- | --- |
| rejected | 12,815 | 12,726 |
| valid | 196 | 233 |
| ambiguous | 14 | 66 |

Ambiguity is where the tagger's cost lands:
52 more sentences carry more than one reading,
which is 0.4% of the 13,025 measured,
not the constant hazard the design notes worried about.
That is the answer to a question [subset.md](subset.md) leaves open —
how much of olski's uniqueness property survives a real tagger.

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
Leave those readings in and the live column reads 12,724, 200 and 101.
Thirty-five of those 101 ambiguities are readings nobody can have meant;
without them 34 of the sentences have exactly one reading and one has none.

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

It also turns two derivations into rejections,
and the gold trees say both of them were wrong:

```text
Tam siedzi nasz umrzyk.
Do zwykłego koła wystarczy sam sznurek.
```

`Tam` is the adverb, but Morfeusz also offers the surname,
indeclinable exactly as the note is,
and olski was reading it as the object of `siedzi` —
in one reading, and therefore confidently.
In the second sentence all four readings
made `Do zwykłego koła` the subject or the object,
where the gold tree has a prepositional phrase before the verb —
a construction olski does not derive at all.
Rejecting is what the grammar should say about a sentence it cannot analyse.

A difference between two totals is not a set of sentences,
and here a 37-sentence difference stands on 99 disagreements.
The two runs accept the same 165 sentences.
Live accepts 68 that gold rejects,
and gold accepts 31 that live does not settle on:
23 it finds ambiguous, 8 it rejects.

The 68 are the warning in the table.
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
and it belongs on the same list as the past tense.
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
and the live run has an `ign` row — 328 forms Morfeusz does not know —
that the gold run cannot have.
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
