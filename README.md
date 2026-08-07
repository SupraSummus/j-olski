# j-olski

*Język olski* is *język polski* with the *p* filed off,
along with the parts of Polish that make it hard for rigid cold machines.

The working goal is a **style linter for Polish technical documentation**,
useful among other things for checking texts
that language models produced.
Not for syntactic errors, which models rarely make,
but for the patterns they habitually fall into.

A linter helps write good code.
This should help write good Polish.

Cheaply, deterministically, and explainably —
as in a compiler, not as in a language model.
Every judgement comes with the rule that produced it,
and the same input gives the same answer twice.

## Why this is still a subset of Polish

A controlled language is a whitelist:
only these constructions exist.
A linter is a blacklist:
write what you like, but these patterns get flagged.

The set of texts that pass every rule
is a subset of Polish either way.
Defining it by exclusion is enormously cheaper,
and it removes the problem
that authors cannot feel where a whitelist's boundary lies.

## Direction

**Now.** A rule engine, a calibrated rule set,
and a paired corpus of human and generated Polish
that tells us which rules discriminate
and which are merely opinions.
See [docs/linter.md](docs/linter.md).

**Optional, for its own sake.** A parser for a designed subset of Polish,
and the *skład* pun that goes with it —
*skład* is typesetting, *składnia* is syntax.
The grammar is no longer the goal;
it is the deepest analysis tier,
reached only by rules that earn it.
See [docs/design-notes.md](docs/design-notes.md).

There is no application driving any of this.
The project is for fun.

## Status

Two things run.

**A grammar for a subset of Polish**, over Morfeusz 2,
where a sentence is olski when it has exactly one reading.
Not merely one derivation: `Koszt samej szynki przewyższa koszt szynki z dodatkami.`
parses two ways and means the opposite thing in each,
so olski rejects it.

```sh
python3 -m olski.check -c "Zapisz plik konfiguracyjny." --readings
```

```text
<text>: valid     Zapisz plik konfiguracyjny .
                  one reading
                  - Object: plik konfiguracyjny, Verb: Zapisz
<text>: ambiguous Koszt samej szynki przewyższa koszt szynki z dodatkami .
                  3 readings, differing in Object, Subject
<text>: rejected  Nowa program zapisuje ustawienia .
                  no reading: nothing in olski derives this
```

Agreement is the parse rather than a check on it:
`Nowa program` has no derivation, so it is not a rule that fires but a sentence
that does not exist.
See [docs/subset.md](docs/subset.md) for what the grammar covers,
what it does not, and the open problem of prepositional attachment.

**A rule engine and the typography pack** over plain Polish text.

```sh
python3 -m olski tekst.txt
python3 -m olski tekst.txt --explain          # with each rule's reasoning
python3 -m olski --list-rules
```

```text
tekst.txt:3:42: warning: [quote-straight] Straight quotation mark; Polish takes „ opening and ” closing.
tekst.txt:3:78: warning: [orphan-single-letter-word] Single-letter word w left at the end of a line
tekst.txt: abstained: [em-dash-density] 82 words in this document is too short to measure a rate over
```

Rules of this kind earn their keep only where the judgement is about characters
rather than about structure — quotation marks, spacing, a stray dash.
Anything that needs to know what a word *is* belongs to the grammar,
which is why the plain-Polish rules are not written as patterns.
Nine rules, all tier A, all marked `uncalibrated`,
because none of them has been measured against human Polish yet
and a threshold without that measurement is an opinion with a decimal point.
Input is plain Polish text.
A file in a markup format gets the rules a character settles,
and abstentions from the rules that would otherwise measure its apparatus.
See [docs/rules.md](docs/rules.md).

The rest of the repository holds design notes, a survey of the field,
a roadmap, and open questions.

- [docs/subset.md](docs/subset.md) —
  what the grammar admits, why validity means a single reading,
  and what prepositional attachment costs
- [docs/rules.md](docs/rules.md) —
  how a rule is written, which check kinds exist,
  and the difference between abstaining and finding nothing
- [docs/corpus.md](docs/corpus.md) —
  how the grammar is measured against the Składnica treebank,
  what the first measurement says,
  and what a coverage figure against one grammar's own output cannot prove
- [docs/linter.md](docs/linter.md) —
  what the linter is for, which rules need how much analysis,
  why calibration decides everything,
  and what is and is not lintable in fiction
- [docs/fiction.md](docs/fiction.md) —
  what goes wrong in model fiction, why post-training causes it,
  why model judges rank it above the New Yorker,
  and which of it is lintable
- [docs/generated-polish.md](docs/generated-polish.md) —
  what a real body of generated Polish measures,
  which patterns it puts on the inventory,
  and why a corpus edited against detectors is a floor and not a sample
- [docs/roadmap.md](docs/roadmap.md) —
  milestones and their exit criteria
- [docs/prose-linters.md](docs/prose-linters.md) —
  the engines English and Japanese already have,
  the one that measured its own false-positive rate,
  and what beating them takes in Polish
- [docs/similar-work.md](docs/similar-work.md) —
  a hundred controlled natural languages,
  how the field classifies them,
  and which of their claims were actually measured
- [docs/design-notes.md](docs/design-notes.md) —
  the optional grammar track:
  what makes Polish hard to parse,
  the cost ladder, and the discontinuity cliff
- [docs/open-questions.md](docs/open-questions.md) —
  the forks not yet taken
- [docs/prior-art.md](docs/prior-art.md) —
  Morfeusz, Morfologik, Świgra, Grammatical Framework, and the rest
- [docs/glr-in-practice.md](docs/glr-in-practice.md) —
  a field report on a small system
  that runs a GLR parser over real Polish,
  what it does with the forest,
  and what its grammar measures at over a thousand rows

## Conventions

Prose in this repository follows
[Semantic Line Breaks](https://sembr.org).
[CLAUDE.md](CLAUDE.md) holds the conventions —
prose, code, tests and commits —
and [TODO.md](TODO.md) the open work inside the repository.
