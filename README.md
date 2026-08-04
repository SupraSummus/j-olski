# j-olski

*Język olski* is *język polski* with the *p* filed off,
along with the parts of Polish that make it hard.

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

Nothing is implemented.
The repository holds design notes, a survey of the field,
a roadmap, and open questions.

- [docs/linter.md](docs/linter.md) —
  what the linter is for, which rules need how much analysis,
  why calibration decides everything,
  and what is and is not lintable in fiction
- [docs/roadmap.md](docs/roadmap.md) —
  milestones and their exit criteria
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
See [CONTRIBUTING.md](CONTRIBUTING.md) before editing Markdown.
