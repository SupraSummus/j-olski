# The subset, as implemented

What `olski/subset.py` currently admits,
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

Two answers were available.
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

## What the grammar covers

- Clauses in SVO and OVS order, and subjectless clauses,
  both imperative (`Zapisz plik.`)
  and pro-drop indicative (`Zapisuje ustawienia.`)
- Noun phrases with an adjective before or after the noun,
  a genitive modifier, or a prepositional modifier
- Prepositional phrases, with the preposition governing the case
- Agreement throughout, as unification rather than as a separate check:
  `Nowa program zapisuje ustawienia.` has no derivation at all

Agreement being the parse rather than a check on the parse
is what makes the rejection precise.
There is no rule that says an adjective must agree with its noun.
There is only a production that shares a variable between them,
and a sentence that cannot satisfy it is not in the language.

## What it does not cover yet

Each of these is a sentence that gets rejected today
and should not be:

- The copula with an instrumental predicate.
  `Plany są niczym, ale planowanie jest wszystkim.`
  fails at the third segment.
- Coordination, of clauses and of phrases.
- Subordination with `że` and `który`.
- Negation and the genitive of negation.
- Numerals, which are common
  and are their own self-contained problem.
- Pronouns, and therefore first and second person subjects.

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

Three ways out, none yet chosen:

1. **Accept the cost.** Olski is small, and this is what small means.
   The author writes `Program zapisuje w pliku ustawienia.`
   or splits the sentence.
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

`olski/parse.py` enumerates distinct readings.
It is a memoizing top-down enumerator,
which is enough for a grammar without left recursion
and reports that case rather than looping.
When the grammar outgrows it —
left recursion, or an ambiguity count large enough
that enumerating is the wrong way to count —
it becomes a chart parser over a packed forest,
which is what [design-notes.md](design-notes.md) always assumed.

`olski/subset.py` is olski itself: the grammar, and the verdicts.

```sh
python3 -m olski.check -c "Zapisz plik konfiguracyjny." --readings
```
