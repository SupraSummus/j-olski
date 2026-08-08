# The subset, as implemented

What `olski/subset.py` admits,
and the decisions that shaped it.
For the theory behind the track, see [design-notes.md](design-notes.md).

## Validity is uniqueness, not just derivability

A sentence is olski when it has **exactly one** reading.
Not at least one.

The case that settled this:

```text
Koszt samej szynki przewyższa koszt szynki z dodatkami.
```

`koszt` is nominative or accusative — the syncretism is total for m3 nouns —
and Polish permits both SVO and OVS.
So the sentence parses two ways
and says the opposite thing in each,
without a Polish reader being able to tell which was meant.

Nothing in the comparison itself does this.
Give the same verb a subject and an object whose cases do not collide
and the sentence has one reading:

```text
Chałka przewyższa zwykłą bułkę.
```

`chałka` is nominative and nothing else,
`bułkę` accusative and nothing else,
so OVS has nowhere to derive,
and the syncretism is what costs the first sentence its meaning.

Where the cases do collide, two answers were available.
Declare olski to be SVO and read the first noun phrase as the subject,
or reject the sentence.
Rejecting it wins,
because the convention would make the sentence unambiguous
only to a reader who knows the convention,
and the settled goal is that olski reads as ordinary Polish
to any Polish speaker.
A sentence nobody else can read reliably
is not a sentence olski should let through.

This also answers a question the linter track had left open.
Deep analysis is expensive because ambiguity is expensive.
Rather than pay for machinery that resolves ambiguity,
olski excludes the constructions that create it,
and every later rule inherits the exclusion.

## What counts as one reading

Two derivations are the same reading
when they have the same shape and the same parts of speech.
Feature values and lemmas are deliberately excluded.

- **Lemmas.** `zapisuje` belongs to both `zapisywać` and `zapisować`.
  Polish forms are homonymous everywhere,
  so counting that as ambiguity would reject nearly the whole language.
  Lexical ambiguity is the reader's to resolve.
- **Feature values.** Whether a phrase settled on neuter plural
  or masculine singular is not something a reader chooses between.
  Agreement has already been enforced by unification.

What does count is anything that changes the structure:
which phrase is the subject, what the object is,
where a modifier attaches,
and whether a word is being read as a noun or a gerund.

This is the distinction
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
got wrong and recorded:
counting attempts rather than outcomes
made it fall silent on lines it had understood perfectly.

## The dictionary offers readings Polish does not

Whether a word is read as a noun or as something else changes the structure,
so by the rule above it is a second reading.
One class of those is a second reading no Polish speaker has.

Morfeusz reads `do` as the preposition and as the musical note,
and the note is indeclinable:
`subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:n:ncol` is every case at once.
Unification is the only filter olski has,
so a reading that satisfies every case demand
is one no context can rule out.
`do pliku` therefore derives twice —
as a prepositional phrase,
and as a noun with a genitive modifier —
and so does every other occurrence of `do`,
which is not a rare word:
[corpus.md](corpus.md#what-morphological-ambiguity-costs)
counts it in the treebank
and measures what excluding the note is worth and what it costs.

Olski refuses a sentence that is ambiguous in Polish.
This one is ambiguous only in the dictionary,
and a parse cannot tell those two cases apart,
so the subset excludes readings as well as constructions:
an uninflected noun reading goes
wherever the same form also reads as a function word —
a preposition, a conjunction, a particle, an interjection.
`admissible` in `olski/subset.py` is where that happens.

One exception runs the other way.
`PO`, `AA` and `UP` are organizations,
they inflect for nothing either,
and their letters spell a preposition and two interjections.
Here the noun is what the form is
and the function word is the accident,
so an all-caps form of more than one letter keeps every reading it has.
A single capital is no evidence either way,
since every sentence starts with one.

Three simpler criteria were available and none holds.
Morfeusz's own qualifiers mark the note `muz.`
and the Japanese theatre that `no` also reads as `teatr.`,
which looks like the criterion until `ku` and `ni`,
which carry no qualifier at all.
The dictionary's labels do not separate them either:
the note is a common noun, `Tam` a surname and `PO` an organization,
and the exclusion has to take the first two and leave the third.
Dropping every uninflected noun instead
would take `jury` and `menu` with it,
and those are ordinary Polish words
with no other reading to fall back on.
What makes the exclusion safe is that it asks for both at once:
the reading inflects for nothing,
and the form carries another one that is what it almost always is.

## What the grammar covers

- Clauses in SVO and OVS order, and subjectless clauses,
  both imperative (`Zapisz plik.`)
  and pro-drop indicative (`Zapisuje ustawienia.`)
- A verb before its subject, with a predicative after it or without one:
  `Są oni obdarzeni rozumem.`, `Nadchodzi druga rewolucja.`
- A predicative before its verb, which is the mirror of OVS:
  `Wejściem jest zwykły tekst polski.`
- Reflexive verbs, with `się` in the position after the verb
- The copula, with a predicative agreeing with the subject
  or a noun phrase in the instrumental,
  and the same predicative under a verb that is not the copula:
  `Ludzie rodzą się wolni.`
- A modal with its infinitive.
  `powinien` inflects for gender and not for person,
  so the clause it heads agrees with its subject in gender
  and leaves person to whatever else constrains it.
- An infinitive as what any other verb takes:
  `Program pozwala zapisać ustawienia.`
  A chain of them needs no rule of its own,
  because an infinitive phrase takes complements
  and an infinitive phrase is one of them,
  so `ma pomagać pisać` comes out of the two productions already there.
- Noun phrases with an adjective before or after the noun,
  a genitive modifier, or a prepositional modifier
- Pronouns, and with them first and second person subjects.
  Person comes from the subject rather than being fixed at the third,
  so `Ja zapisuje plik.` is a disagreement
  in the way `Nowa program` is one.
- Coordination, of noun phrases, of adjective phrases and of clauses,
  joined by a conjunction
- Any number of prepositional adjuncts on one verb,
  because `postępować wobec innych w duchu braterstwa` has two
- Prepositional phrases, with the preposition governing the case
- A prepositional phrase in front of the clause,
  which modifies the clause rather than any noun in it
- Agreement throughout, as unification rather than as a separate check:
  `Nowa program zapisuje ustawienia.` has no derivation at all

Agreement being the parse rather than a check on the parse
is what makes the rejection precise.
There is no rule that says an adjective must agree with its noun.
There is only a production that shares a variable between them,
and a sentence that cannot satisfy it is not in the language.

## The bare verb-initial order keeps the predicative one honest

```text
Trwa akcja protestacyjna.
```

The adjective is attributive or it is predicated,
and Polish gives a reader both.
Admit only the verb-initial order that takes a predicative
and the second reading has nothing to compete with,
so olski calls it the one reading and is confidently wrong.
That is the failure
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance) counts,
and admitting the bare order beside it
costs the sentence its uniqueness and keeps its honesty.

The subject takes no complements of its own in either order,
which is what stops `Zapisuje program ustawienia.` deriving
and stops every SVO sentence competing with a verb-initial reading of itself.

## Nothing above a coordination distributes into it

A coordination is one **conjunct**, a conjunction, and the rest,
and the grammar's symbols are named for it:
`NPConjunct` is a noun phrase with no coordination in it,
`NP` is one that may have.
An adjective attaches inside a conjunct and never above the coordination,
so `nowe programy i pliki` is `[nowe programy] i [pliki]`
and never `nowe [programy i pliki]`.
That is a narrowing rather than a reading of Polish,
and what it buys is an agreement that can still fail.

A coordination has no gender of its own.
Polish resolves the gender of `rozum i sumienie`
by rules unification cannot state,
and a feature a phrase does not carry
is one no agreement can fail against,
so an adjective scoping over the coordination
would be an adjective agreeing with nothing
and `nowa programy i pliki` would derive.
Refusing the wider attachment is what keeps that a rejection.

## What it does not cover yet

Each of these is a sentence that gets rejected
and should not be:

- Clause-level punctuation.
  Two clauses join with a conjunction and not with a comma,
  so `Plany są niczym, ale planowanie jest wszystkim.`
  fails at the third segment, on the comma.
- The past tense, which
  [corpus.md](corpus.md#where-the-analyses-stop)
  ranks as the cheapest large gain left.
- Subordination with `że` and `który`.
- Negation and the genitive of negation.
- Numerals, which are common
  and are their own self-contained problem.

Two entries are not constructions but demands every construction makes:

- **Valency.** Nothing records which complements a verb actually takes,
  so `być` accepts an accusative object,
  and any verb accepts a predicative or an infinitive.
  `On jest wolny.` is where that shows:
  `wolny` reads as an adjective and as a noun,
  so the sentence comes out ambiguous
  between the predicative a reader has and an object nobody means.
  [corpus.md](corpus.md#what-morphological-ambiguity-costs)
  found the same gap from the other side.
- **A form the dictionary does not have.**
  Morfeusz is asked not to guess at one (`olski/morph.py`),
  so it comes back tagged `ign`,
  which no production takes and no agreement can rescue.
  `olski` is such a form:
  `Język polski jest podzbiorem polszczyzny.` derives
  and `Język olski jest podzbiorem polszczyzny.` does not,
  so the language cannot say in itself what it is.
  Gold morphology leaves a treebank no such form,
  which is why the queue in
  [corpus.md](corpus.md#where-the-analyses-stop) does not rank it
  and a run over documentation does.

## The open problem: prepositional attachment

This is the largest thing found so far,
and it is not a bug.

```text
Program zapisuje ustawienia w pliku.
```

`w pliku` attaches to the verb or to the object,
and those are different claims about where the settings are.
Both derivations are real Polish,
so the uniqueness property rejects the sentence.

The trouble is that this is not a rare construction.
Nearly every sentence with a prepositional phrase after an object
is ambiguous the same way,
which means the uniqueness property as stated
excludes a large and ordinary part of technical Polish.

The comparison this document opens with runs into it.
`przewyższać` compares along a dimension —
what one thing exceeds another *in* —
and leaving the dimension out is what makes
`Chałka przewyższa zwykłą bułkę.` read stiffly,
so a person writing it names one:
`Chałka przewyższa zwykłą bułkę pod względem smaku.`
That is two readings again,
one where the dimension belongs to the comparison
and one where it belongs to the roll.

One position escapes it, and the grammar takes it:

```text
Pod względem smaku chałka przewyższa zwykłą bułkę.
```

A prepositional phrase modifies a Polish noun only from behind it,
so in front of the clause there is no noun for it to attach to
and the reading where the taste belongs to the roll does not exist —
for the parser and for a Polish reader alike.
Fronting asks nothing of the reader,
being a position the language already has,
and [corpus.md](corpus.md#where-the-analyses-stop)
counts what admitting it reaches on the treebank.

It settles one of the two readings and not the other.
The verb reading gets a position that isolates it and the noun reading gets none,
so an author who means *the settings that are in the file*
has nowhere to put the phrase where only that reading survives.
`Ustawienia w pliku zapisuje program.` looks like that position
and is not one:
the OVS rule takes no modifier of its own,
so the phrase can only reach the noun,
and olski calls the sentence unambiguous
where a Polish reader still has both readings.
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)
shows the same narrowness on the treebank,
where it accounts for every disagreement with a gold tree.

Three ways out of the reading that is left, none yet chosen:

1. **Accept the cost.** Olski is small, and this is what small means.
   The author fronts the phrase or splits the sentence.
   Moving it in front of the object instead does not work:
   `Program zapisuje w pliku ustawienia.` is accepted
   with `w pliku ustawienia` read as one phrase and no object at all,
   because no `Predicate` rule takes a modifier before its object.
2. **Attach consistently.** Declare that a prepositional phrase
   attaches to the verb unless something forces otherwise.
   Cheap, and it makes the language depend on a convention
   the reader does not know — the objection that killed
   fixing the word order.
3. **Decide it is not an ambiguity worth having.**
   The two readings may describe the same situation often enough
   that treating them as one reading is honest.
   That is a claim about Polish semantics
   and would need to be argued rather than assumed.

The question is the same shape as the word-order one
and deserves the same treatment: answered by looking at real Polish,
not by taste.

## Implementation

`olski/morph.py` wraps Morfeusz 2, which supplies segmentation
and every reading of every form, choosing none of them.

`olski/grammar.py` is the formalism:
productions, symbols, and feature unification.
A grammar is Python data, like the rule packs.

That formalism is tier 0 of
[the cost ladder](design-notes.md#the-cost-ladder):
every feature value is a finite set of tagset atoms,
unification is intersection,
and a variable is scoped to the production that uses it,
so the grammar underneath the features is context-free,
for the reason [design-notes.md](design-notes.md#why-a-subset-really) gives.
Reading a segmentation graph rather than a string does not reach past it,
the context-free languages being closed under intersection with a regular one.

`olski/parse.py` enumerates distinct readings.
It is a memoizing top-down enumerator,
which is enough for a grammar without left recursion
and reports that case rather than looping.
When the grammar outgrows it —
left recursion, or an ambiguity count large enough
that enumerating is the wrong way to count —
it becomes a chart parser over a packed forest,
which is what [design-notes.md](design-notes.md) always assumed.

`olski/subset.py` is olski itself:
the grammar, the readings it declines to consider, and the verdicts.

```sh
python3 -m olski.check -c "Zapisz plik konfiguracyjny." --readings
```
