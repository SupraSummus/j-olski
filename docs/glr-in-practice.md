# GLR in practice: a field report

[parsowanie.md](parsowanie.md#earley-wydaje-las-a-glr-zostaje-optymalizacją) argues
that GLR is the right *shape* of answer for olski
but probably the wrong specific choice,
and that Earley is the boring correct first move.
That argument is made from the algorithms' properties.
This document is the other kind of evidence:
a small system that has run a GLR parser over real Polish text since 2019,
what it did with the forest,
and what its grammar actually does
when measured against a thousand rows of its own input.
The measurements are at the end,
and one of them contradicts what the code appears to be for.

The system is a private Django project
that imports archival biographical records from CSV.
It is not a language project and has no linguistic ambitions.
That is what makes it useful here —
it shows the shape of GLR-over-Polish
when someone reaches for it to get a job done,
rather than to study parsing.

## The problem

One CSV column holds prose written by archivists,
in a dense conventional shorthand.
An invented line, in the shape of the real ones:

```text
ur. 7 III 1897 w m. Ciche k. Nowego Targu, s. Ignacego, w. rzymskokatolickie. Stolarz. Książeczka wojskowa nr 4471.
```

Each line is a run of *facts* separated by `.` or `,`:
birth date and place,
parents,
religion,
schooling,
occupation,
military unit,
military ID,
residence.
Roman numerals stand in for months,
parenthesised alternatives appear inline,
and the abbreviations are fixed by archival convention —
`ur.` born,
`s.` son of,
`m.` town,
`k.` near,
`pow.` and `gub.` administrative divisions,
`zam.` resident of,
`przyn.` attached to.

The import extracts exactly **one** field from the parse: the birth place.
Dates and names are pulled out with plain regexes elsewhere in the same class.
Every other fact type exists in the grammar
purely so the rest of the line can be consumed.
That is the whole design.
The grammar is a frame for one extraction,
not a model of the text.

This grammar covers a *register*, not a language,
which is the opposite of what olski is attempting.
Archival shorthand is already a controlled natural language,
controlled by editorial convention rather than by design,
and that is why a few hundred lines of CFG get anywhere at all.

## Grammar as data, not as DSL

The parser is [parglare](https://github.com/igordejanovic/parglare),
pinned to `0.13.*`.
parglare has its own `.pg` grammar language,
and the project does not use it.
Instead a 75-line adapter
(taken from [dhall-python](https://github.com/SupraSummus/dhall-python/blob/master/dhall/parglare_adapter.py))
turns two plain dicts into a `parglare.Grammar`:

```python
def to_parglare_grammar(productions_dict, terminals_dict, start, **kwargs):
    ...
    return parglare.Grammar(
        productions=productions,
        terminals=terminals.values(),
        start_symbol=start_non_terminal,
        **kwargs,
    ), '__start'
```

`productions_dict` maps a nonterminal to a list of alternative right-hand sides,
`terminals_dict` maps a terminal name to
`('string', literal)`,
`('regexp', pattern)`,
or `('external',)`.
The adapter builds `parglare.Terminal` objects
wrapping `StringRecognizer` or `RegExRecognizer`,
builds `parglare.NonTerminal` objects,
and prepends a synthetic `__start -> <start>` production.

This is directly relevant to olski.
Dominance and precedence are separated there
and a preprocessor expands precedence constraints into orderings
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
so the grammar handed to the parser is *generated*, not written.
A grammar-as-data interface is then the thing you need,
and a `.pg`-style concrete syntax
becomes a serialization format you have to emit and re-parse for no reason.
Whatever parser olski picks,
this is the API shape to check for.

## The grammar

Held as a class attribute, so it is constructed at import time:

```python
grammar, _ = to_parglare_grammar(
    {
        'start': [['<nil>'], ['_?', 'facts', '_?']],
        'facts': [
            [],
            ['fact'],
            ['fact', '.'],
            ['fact', 'fact_delimiter', '_', 'facts'],
        ],
        'fact': [
            ['birth_fact'], ['military_id_fact'], ['parents_fact'], ['belief_fact'],
            ['school_fact'], ['military_place_fact'], ['job_fact'], ['home_place_fact'],
        ],
        'birth_fact': [
            ['ur. ', 'w_or_we', '_', 'place'],
            ['ur. ', 'date'],
            ['ur. ', 'date', '_', 'w_or_we', '_', 'place'],
            ['ur. ', 'date', ',', '_', 'w_or_we', '_', 'place'],
            ['ur. ', 'date', ',', '_', 'place'],
        ],
        'place': [
            ['words'],
            ['m.', '_?', 'words'],
            ['words', '_', 'place_operator', '_', 'place'],
            ['m.', '_?', 'words', '_', 'place_operator', '_', 'place'],
        ],
        'place_operator': [['k.'], ['pow.'], ['gub.'], ['w']],
        'word': [['letter', 'letter', 'short_word']],
        'short_word': [['letter', 'short_word'], ['-', 'short_word'], ['letter']],
        '_?': [[], ['_']],
        ...
    },
    {
        '_': ('string', ' '),
        'letter': ('regexp', '[a-żA-Ż]'),
        'regexp_number': ('regexp', r'\d+'),
        'roman_number': ('regexp', '[IVX]+'),
        'bracket_expression': ('regexp', r'\([^\)]*\)'),
        'job_regexp': ('regexp', r'\w+(strz|nik|arz|acz|iec|ica|dent|ewc|unkt|nier|nom|iusz|ter|ant)'),
        ...
    },
    'start',
)
```

Four details are interesting beyond this project.

**No lexer.**
The parser runs with `ws=''`,
which disables parglare's whitespace skipping,
so a space is an ordinary token (`_`, with `_?` for optional).
This is forced by the terminals:
`'ur. '` and `'Książeczka wojskowa nr '`
carry their own trailing spaces,
and the difference between `m. Bystra` and `m.Bystra`
is information the grammar wants.
The price is that every single space
has to be spelled out in every production,
which is most of the visual bulk above.
Olski will face the same decision at the boundary
between a Morfeusz-style segmentation DAG and the grammar proper,
and the trade is the same one:
significant whitespace buys precision and costs legibility everywhere.

**Words are built letter by letter.**
`word -> letter letter short_word`,
with `short_word` recursing over letters and hyphens.
Not `\w+`.
This forces a minimum length of three
and keeps hyphenated names in one piece,
so stray abbreviations don't get read as words.
It also means the CFG is doing tokenizer work,
and each name in the input costs a reduction per character.
A cheap way to get a lexical constraint you couldn't otherwise state,
paid for in forest nodes.

**Occupations are recognised by suffix.**
`job_regexp` is an alternation of Polish agent-noun endings —
`-strz`, `-nik`, `-arz`, `-acz`, `-iec`, `-ica`, `-nier`, `-iusz`, `-ant`.
No dictionary, no lemmatizer;
morphology used as a classifier.
It is crude and it works,
and it is a reminder
that some of what looks like it needs SGJP
can be had from a regex over endings.

**The missing-value marker is a sentence.**
The source data writes a literal `<nil>` for an absent column,
so `<nil>` is an alternative of `start` that reduces to `None`,
rather than a special case in the calling code.
Small thing, but it is the right instinct:
if the input language contains it, the grammar should describe it.

## Semantic actions

Actions are a parallel dict of lambdas,
one list per nonterminal,
aligned **positionally** with that nonterminal's alternatives:

```python
grammar_actions = {
    'start': [pass_none, pass_inner],
    'facts': [
        lambda _, n: {},
        lambda _, n: n[0],
        lambda _, n: n[0],
        lambda _, n: {**n[0], **n[3]},
    ],
    'birth_fact': [
        lambda _, n: {'birth_place': n[1:4]},
        lambda _, n: {'birth_date': n[1]},
        lambda _, n: {'birth_date': n[1], 'birth_place': n[3:6]},
        ...
    ],
    'word': [concat_all],
    'words': concat_all,
    'place': concat_all,
}
```

Every fact reduces to a small dict;
`facts` merges them upward with `{**n[0], **n[3]}`,
so a whole line becomes one flat dict keyed by fact type.
`concat_all` recursively flattens a subtree of nested lists back into a string,
undoing the letter-by-letter `word` rule.
parglare's own `pass_none` and `pass_inner`
handle the two alternatives of `start`.

The positional alignment is a trap,
and a specific warning for olski.
Insert an alternative in the middle of a nonterminal's list
and every action after it silently shifts by one:
no exception, wrong output.
That is survivable when a human writes both dicts side by side.
It is not survivable when the productions are generated —
an ID/LP preprocessor that expands one dominance rule
into a variable number of orderings
has no stable index to attach an action to.
Actions must be keyed by an explicit label,
or attached to the dominance rule
and inherited by every permutation derived from it.

## Ambiguity as a confidence measure

Here is the part worth taking,
and the part where reading the code misleads you.

```python
def extract_birth_place(self, v):
    try:
        possible_parses = self.parser.parse(v)

        if len(possible_parses) == 1 and possible_parses[0]:
            birth_place = possible_parses[0].get('birth_place')
            if birth_place:
                return concat_all(None, birth_place)

    except parglare.exceptions.ParseError:
        return None
```

The grammar admits ambiguity rather than legislating it away.
`place`, `school_name`, and `words` overlap;
`w` is both a preposition and a `place_operator`;
the `facts` recursion can bracket a line more than one way.
An LR parser would report conflicts and force a rewrite into something worse.
GLR returns every reading instead —
and the code then uses the *cardinality of the forest* as its only signal.

One reading means the abbreviations lined up exactly one way,
so the answer is trusted.
Two or more means the line is unclear,
and the extractor declines to answer.
`ParseError` lands in the same place by a different route.
Downstream, `extract_birth_place(...) or ''` leaves the field empty
on a record that is already imported unpublished, awaiting human review.

No disambiguation rules.
No ranking.
No preference model.
Ambiguity is not resolved here;
it is a confidence measure,
and the parser is a filter separating
lines it is certain about from lines it isn't.

That is the design as written,
and it is a genuinely good idea.
It is also almost never the thing that fires.
Measured over a thousand real rows,
the abstention branch triggers **twice**;
one row in five is rejected by `ParseError` instead.
The numbers are in [Measurements](#measurements) below,
and they change what this system is evidence *of*:
not that forest cardinality is a load-bearing filter,
but that it is a cheap belt on top of a grammar
that is very nearly unambiguous on its actual input.

The two abstentions are worth looking at individually,
because they fail in opposite directions.

**One is a real save.**
`ur. 28 II 1893, przyn. Grybów, s. Józefa. Murarz.`
yields two readings.
The first reads `przyn. Grybów` correctly as a military-unit fact.
The second reads it as a *birth place* and reports it as `'przybów'` —
a string that appears nowhere in the input,
assembled from letters on either side of the abbreviation.
Because there are two readings, nothing is written.
Cardinality caught a corrupt value
that no amount of grammar review would have predicted.

**One is a false abstention.**
The line `ur. w 1895.` followed by a single trailing space
also yields two readings,
and they are *byte-identical dicts*:
`{'birth_date': ['w', ' ', '1895']}` twice.
The optional-whitespace rule `_? -> ε | _`
lets the same string be bracketed two ways with the same result.
The check counts parses, not distinct results,
so a line the grammar understood perfectly is thrown away.
Deduplicating results before counting
would be strictly better and costs one `set` of serialized readings.

So the honest summary is narrower than the code's shape suggests:
abstention-on-ambiguity is worth having,
it demonstrably prevents at least one class of silent corruption,
and half of what it caught here was its own grammar's noise.

[design-notes.md](design-notes.md#the-second-currency-ambiguity)
names mean readings per sentence as a cost to be measured.
This system says the metric has a second reading worth keeping:
per-sentence ambiguity is a cost when the consumer needs one tree,
and usable signal when the consumer is allowed to abstain.
[open-questions.md](open-questions.md) asks
whether to build a disambiguation preference over the forest.
Abstention is a third option, cheaper than ranking or resolving —
with the caveat this system supplies for free,
that it must count *distinct* readings,
or grammar artefacts will spend the budget.

## What this does and does not tell us about GLR for olski

**It does not rescue GLR.**
This grammar is nothing like an olski grammar.
Its ambiguity is *local* —
a handful of overlapping rules around place names,
inside a line whose overall structure is nailed down
by distinctive string terminals appearing every few tokens.
The graph-structured stack splits, then rejoins almost immediately.
That is precisely the mostly-unambiguous input GLR was designed to be fast on,
and it is exactly what an olski grammar will *not* be:
free word order times case syncretism gives ambiguity
that is global and pervasive rather than local and anchored.
The design-notes prediction survives.

**It does settle the nullable-rules worry, though.**
The grammar leans on empty productions —
`facts -> ε` and `_? -> ε` —
and it works.
Tomita's failure on nullable rules is a property of the 1985 algorithm,
not of GLR tooling in 2020s Python;
a maintained implementation handles them.
The project's history even records
a commit adjusting the grammar for a parglare version bump,
so the cost of depending on a GLR implementation
shows up as ordinary upgrade churn, not as a wall.
RNGLR versus BRNGLR is a question for someone implementing a parser,
not for someone using one.

**It says nothing either way about the automaton-rebuild cost.**
This was the one place a first draft of this document overreached,
so the correction is worth recording.
The grammar object is built at import time,
while the parser — and therefore the LR table — is built separately
in an `initialize_parser()` method
called at the top of the import run and explicitly by tests.
Table construction is eager, inside the `GLRParser` constructor,
which invites the reading that someone split the two to defer a real cost.
Measured, the table is 146 states and takes 29 ms to build.
That is not a cost anyone schedules around;
the split is import-time hygiene,
and probably just testability.
[parsowanie.md](parsowanie.md#earley-wydaje-las-a-glr-zostaje-optymalizacją) gives grammar churn
as a decisive reason to prefer Earley,
and that argument stands on its own.
A 146-state table is no evidence about
what a permutation-expanded free-word-order grammar would cost,
which is the case the argument is actually about.

## Smaller observations

Three defects found while reading,
all of the kind that a grammar-as-data interface invites.

**A terminal whose name and literal disagree.**
`'Student ': ('string', 'Student')` —
trailing space in the dict key, none in the recogniser.
The production is `['Student ', 'school_name']` with no `_` between them,
so that alternative matches only the space-less form.
Verified against the built parser:
`StudentSzkoły` reduces to `school_fact`,
while `Student Szkoły` does not.
The neighbouring `'Absolwent ': ('string', 'Absolwent ')` gets it right.
Using a terminal's name as documentation for its literal
invites exactly this drift,
and nothing checks it.

The consequence is milder than it looks,
for a reason that is funnier than the bug:
`Student Szkoły` still parses — as a `job_fact`.
The occupation regex ends in an alternation containing `dent`,
and *Student* ends in *-dent*,
so the suffix classifier swallows the whole phrase.
A latent bug in one rule,
hidden by an over-general regex in another.
Both would have been caught
by asserting on the parse *shape* rather than on the extracted string;
the project's two-case test only checks birth places,
so it sees neither.

**A dead terminal.**
`'w. '` is defined and referenced nowhere;
the religion rule uses `'w.'`.
An unreferenced terminal is silent —
worth a lint if olski's grammar is ever generated.

**A subclass paying for a parser it never uses.**
A variant importer for a differently-shaped source file
inherits the call to `initialize_parser()`
but hardcodes the birth place to `''`.
It builds the whole LR table on every run and never parses a byte.
All 29 ms of it, so this is tidiness rather than a performance bug.

## Measurements

Method: lift the grammar and action dicts out of the source verbatim,
build the parser with the same `ws=''` and actions the project uses,
and run it over one of the project's own CSV fixtures —
1000 rows of the free-text column.
No Django and no database involved,
so this is reproducible from the two grammar dicts alone.

Parse outcomes over 1000 rows:

| outcome | rows | share |
| --- | --- | --- |
| exactly one reading | 796 | 79.6% |
| `ParseError` | 202 | 20.2% |
| two readings (abstained) | 2 | 0.2% |
| three or more readings | 0 | 0% |

Of the 796 unambiguous parses,
473 carried a `birth_place` — 47.3% of all rows.
A twelve-row random sample of those extractions was clean:
`w Łodzi`,
`w Busku-Zdroju`,
`w m. Zimna Woda k. Jasła`,
`w m. Krzywda k. Łukowa gub. siedlecka`,
and so on,
including a correctly captured parenthetical
(`w m. Międzybrodzie Lipnickie (ob. Międzybrodzie k. Bielska-Białej)`).
So when the parser does commit, it is right;
the garbled `'przybów'` above only ever appeared
inside a reading that was discarded.

Table: 146 states, 29 ms to construct.
First parse after construction: about 1 ms.

Three things to take from this table.

**Recall, not precision, is the binding constraint.**
One row in five simply does not parse.
For an olski grammar the equivalent number
is the coverage curve [design-notes.md](design-notes.md#making-the-trade-measurable)
proposes measuring against Składnica,
and 20% rejection on a *register this narrow*,
with a grammar hand-fitted to it,
is a sobering baseline for what a designed subset of full Polish will do.

**Mean readings per sentence here is ≈ 1.003.**
That is what makes this an easy case rather than a representative one.

**A grammar can be ambiguous in principle and unambiguous in practice.**
The overlapping rules are real,
and the distinctive string terminals every few tokens
prevent them from ever compounding.
Anchoring is what buys this,
which is the same insight as a controlled language:
if the input reliably contains fixed landmarks,
the ambiguity between them stays local.
Olski gets to *choose* its landmarks.
That is a design lever worth naming.

## Takeaways

- Grammar-as-data is the interface to want
  when the grammar will be generated rather than written.
  Check for it before picking a parser.
- Bind semantic actions to labels, never to production indices.
  Index alignment cannot survive permutation expansion.
- Significant whitespace (`ws=''`) is the right call
  when terminals are abbreviations,
  and it makes every production noisier.
  Decide once, deliberately.
- Abstaining on an ambiguous parse is an underrated use of a forest.
  Cheaper than ranking, cheaper than resolving,
  and honest about what the grammar knows.
  Count *distinct* readings, though,
  or optional-whitespace rules will make you abstain on lines you understood.
- Measure the ambiguity you think you have.
  This grammar looks ambiguity-driven and averages 1.003 readings per line;
  its real filter is parse failure at 20%.
  The same gap is available to olski,
  in whichever direction.
- Modern GLR implementations handle nullable rules.
  That objection is historical.
- GLR being fine here is not evidence it is fine for olski.
  Local ambiguity anchored by distinctive terminals
  is the easy case, and olski has the hard one.
  Choosing the anchors is the lever olski has and this project didn't.
