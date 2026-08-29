# Świgra: the ground it occupies, and what it leaves open

Świgra is a constituency parser of the whole of Polish,
written by Marcin Woliński over more than two decades,
and it is the closest existing thing to olski's grammar track.
Reading its source is how to find out which ground is taken.

The useful output of that reading is the ground that is not taken,
since that is where olski's grammar track lives.
The second output is a set of mechanisms worth taking,
since a grammar of Polish that has run for twenty years
has already met the problems olski is walking into.

## What was read, and what was run

`swigra_current.zip`, fetched from the project page at
<https://zil.ipipan.waw.pl/Świgra>,
whose files carry dates up to June 2019.
The name says nothing about which release it is,
so the digest of the copy read here sits in `harness/świgra.py`
beside the command that fetches it.
The CLARIN-PL handle listed in
[similar-work.md](similar-work.md#sources) answers 404;
the wiki attachment is the live copy.

The package is roughly 66,000 lines of SWI-Prolog under GPL v3.
Two files are grammars:
`gfjp.dcg` implements Świdziński's formal grammar of Polish, the GFJP,
and `gfjp2.dcg` is a larger grammar of Woliński's own descended from it,
which the parser runs by default.
The runtime around them is called Birnam and is about 1,300 lines.
A grammar is not interpreted:
`birnam_dcg2pl` compiles the `.dcg` file into Prolog clauses,
which are then saved as a binary.
The verb and noun lexicons are generated files
carrying a header that says so,
built from the Walenty valency dictionary.
The maximum-entropy tree disambiguator ships as a separate archive.

Most of what follows comes from reading that source.
The parser also runs, and one claim below is a measurement:
`harness/świgra.py` feeds the compiled binary one sentence at a time,
owns the number that comes back,
and names both what the comparison flatters
and what the package needs patched to build under SWI-Prolog 9 at all.
The package decided how it is fed.
Its Morfeusz glue library is built against SWI-Prolog 7.4 and 7.6,
so input goes in as the NKJP facts the parser also accepts
rather than through Morfeusz;
and NKJP tags are not Morfeusz 2's,
so the probe translates between them and is coarse where it does.
Everything here that is not that number is about what the code says.

The monograph under [Sources](#sources) was read as well,
and what it holds is decisions and measurements rather than mechanisms,
so it lands in the documents that own those and not in this one:
what stopped the treebank's own grammar before discontinuity did
([design-notes.md](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)),
what the verified trees still get wrong
([corpus.md](corpus.md#what-this-number-is-not)),
how much a disambiguating layer has to see
([disambiguation.md](disambiguation.md#cechy-lekkie-biją-ciężkie-bo-uzgodnienia-sprawdziła-już-gramatyka)),
and which word orders Polish prose actually uses
([sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)).

## What Świgra occupies

Świgra takes a Polish sentence and returns every constituency tree it has,
and the pipeline around it ends in a maximum-entropy component,
trained on the Składnica treebank,
that picks one of those trees.
Analysis of the whole language and resolution of the ambiguity it finds:
that is the territory, and it is held.

What is left over follows from the properties below.

**It describes Polish rather than choosing a Polish.**
An analyser that refused a genuinely ambiguous Polish sentence
would be broken, because the sentence is Polish.
Everything Świgra does follows from having no licence to exclude.

**It resolves.**
The forest exists to be collapsed,
and the disambiguator is what collapses it.
Forests can be looked at —
there is a web demo, and TeX and PDF renderings of trees —
but nothing in the package treats the *number* of readings
as something to report about the sentence.

**It runs in one direction.**
Birnam is a bottom-up chart parser pulling input from an inflection graph.
Nothing in the package generates.

**It answers in seconds, where a subset answers in milliseconds.**
Free word order is bought with search rather than with rules
([`sequence_of`](#free-word-order-without-factorial-rules) below),
and describing all of Polish means paying that on every sentence.
Over the prose of this repository's README,
`harness/świgra.py` has Świgra spend seconds on sentences of ten words
and run past a forty-five second budget on some of them,
where olski takes milliseconds a sentence
and finishes the whole file before Świgra finishes one of those.
This is a consequence of describing Polish rather than a defect,
and it decides what each parser can be used for, not which is better:
a treebank is built once, so seconds a sentence is a night of compute,
and a checker that answers while a sentence is being typed is not on that ground.
Where those numbers come from is the probe's own subject,
including the part of it that flatters Świgra.

## What it leaves open

Each of these is unoccupied ground rather than a complaint,
and together they are the grammar track's reason to exist.

**Ambiguity reported to the author instead of resolved for them.**
[roadmap.md](roadmap.md#co-jest-budowane) owns that purpose,
and Świgra is where the survey found it empty:
it picks the likelier reading where olski would hand both back.
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
records the same move being made by accident
in a system with no linguistic ambitions at all,
which is evidence that it is natural rather than clever.

**A language chosen rather than described.**
Olski picks what it admits and can therefore pick its landmarks:
constructions that keep ambiguity local instead of letting it compound.
[glr-in-practice.md](glr-in-practice.md#measurements) names that lever
at the end of a grammar whose register handed it the landmarks for free,
and olski has not spent it.
Świgra has no access to it at any price.

**Generation, and the round trip.**
[design-notes.md](design-notes.md#the-round-trip-invariant)
wants one declarative source feeding both a parser and a generator,
so that a text and its structure can be checked against each other.
No part of Świgra's runtime can be that source.

**Small enough to state.**
Świgra is 66,000 lines and a book.
Kuhn's survey of controlled languages measures simplicity
in pages of description
sufficient for someone to write a correct parser,
and a subset that fits in a document
is a different artifact from a grammar that does not,
whichever admits more Polish.
See [similar-work.md](similar-work.md#pens-and-why-it-matters-here).

And the largest one, which is not about grammars at all.
[roadmap.md](roadmap.md#tor-gramatyczny-nie-ma-końca)
gives the track no size to reach and no coverage figure to hit:
what it grows towards is a verdict that says something true about one sentence,
and every addition is priced rather than counted off against a target.
Świgra admits more Polish and will go on doing so,
which decides nothing here,
because the two are not measured on the same axis
and there is no amount of covering that would make olski done.

## Why wrapping it does not get there

Worth recording so that nobody re-proposes it:
the uniqueness test could in principle run on Świgra's forest,
and every obstacle below stops it on its own.

It counts derivations where olski counts readings.
`counttrees` in `birnam_cleanforest.pl`
multiplies subtree counts through the packed forest,
while [subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie)
quotients over lemmas, feature values and parts of speech
so that only structure counts,
and writing that quotient against somebody else's tree shapes
is most of the work with none of the design freedom.
Deriving everything is the wrong primitive for a subset,
so the boundary would have to be reimposed by a filter over trees,
which is a grammar written twice.
The integration is a subprocess and an XML parse:
SWI-Prolog, a binary saved by `qsave_program`,
forests serialized against `forest.xsd`,
and a Morfeusz glue library compiled against SWI-Prolog 7.4 and 7.6.
A wrapper inherits the seconds a sentence as well,
which is the whole of what a checker in an editor has to spend.
And Świgra is GPL v3,
so embedding it is a licensing decision
rather than a detail to discover afterwards.

None of which is a criticism.
If the goal were parsing arbitrary Polish this project should not exist,
and Świgra is not the competition but the measuring stick:
Składnica's trees are drawn from its output,
which is why a coverage figure against Składnica
means what [corpus.md](corpus.md#what-this-number-is-not) says and no more.

## What the code does that olski should take

### Free word order without factorial rules

`birnam_sequences.pl` defines a metanonterminal `sequence_of`
that repeatedly selects one daughter out of a bag
until the span is consumed,
so order among sisters is free by construction.
What makes it usable rather than merely permissive
is *iterated conditions*, written `^[Pred, In, Item, Out]`,
which thread an accumulator through the daughters
in whatever order they arrived:

```prolog
zdanie(...) --> s(ze1),
    ff(..., Wym, ...),
    sequence_of([ fw(W2,H2,...)  ^[oblwym_iter, Wym, W2/H2, ResztaWym],
                  fl(...)        ^[najwyżej3, 0, _, _],
                  posiłk(...) ]
                ^[obldest_iter,    Dest1, Dest2, Dest]
                ^[sprawdz_pk_iter, Pk1,   Pk2,   Pk]),
    { wymagania_zamknij(ResztaWym) }.
```

Valency saturation, comma agreement, interrogative propagation,
a ceiling of three loose phrases,
and the rule that at most one auxiliary may appear
and not directly before the finite verb
all ride on that one mechanism.
This is the tier-1 row of
[the cost ladder](design-notes.md#the-cost-ladder) —
dominance separated from precedence —
implemented in about two hundred lines,
and it is the answer to how that row is paid for in practice.
The cost it does not hide:
selecting from a bag is a backtracking choice point per daughter,
so the freedom is bought with search rather than with rules.

### Valency as a resource that gets consumed

A verb carries a `wym` term
whose last argument is a list of *alternative* schemata.
Realizing an argument keeps only the schemata
holding a position that admits it, and deletes that position;
`wyjmij` in `gfjp2_wymagania.pl` is the four-line core of it.
Coordination is `koord([Frames…])`,
and an argument must be removable from every conjunct.
At the end `wymagania_zamknij` checks that something survived.

So which frame a verb is using is never chosen in advance.
It falls out of the parse as a narrowing set,
which is both cheaper and more honest
than deciding the frame first and backtracking on it.
Valency is on the list of things
[the subset does not cover](subset.md#what-it-does-not-cover-yet),
and this is the shape to reach for when it does.

### Fraza luźna jest pozycją, której nikt nie żąda

Córki zdania dzielą się w GFJP na dwa rodzaje.
Frazy wymaganej żąda rama walencyjna czasownika
(`fw`, [wyżej](#valency-as-a-resource-that-gets-consumed)),
a fraza luźna — u Świdzińskiego przyzdanie — dochodzi do zdania bez żądania (`fl`).
Pod jedną pozycję wchodzi przez to wszystko, czego rama nie wymienia,
i `gfjp2.dcg` mówi to przykładami wpisanymi nad regułami `fl`:

```text
Wymknął się po angielsku.
Znam go od dawna.
Czytałaś, dziewczyno.
Wchodziliśmy do domu, depcząc trawnik.
Umrze przeczytawszy książkę kucharską.
```

Okolicznik, wyrażenie przyimkowe, wołacz i dwa imiesłowy są jedną pozycją,
a nie pięcioma; te same reguły biorą tam zdanie okolicznikowe
i gołą grupę imienną mówiącą jak długo —
`dwie godziny` w `Gotować mieszaninę dwie godziny.` dochodzi luźno,
a zdanie to jest w gramatyce przykładem obowiązkowym.
Kolejność jest wolna, a sufit jeden — `najwyżej3` w warunku iterowanym tego samego
`sequence_of` ([wyżej](#free-word-order-without-factorial-rules)) —
więc konstrukcje, które inaczej wchodziłyby po jednej, wchodzą tu jednym symbolem.

Cena wychodzi z tego samego, z czego pożytek.
Pozycja luźna przyjmuje frazę każdego typu i wchodzi w zdanie w każdym miejscu,
więc grupa, której nie chce żadna pozycja ramy, ma gdzie wpaść —
i wpada tam w każdej kombinacji z pozostałymi, bo kolejność jest wolna.
Woliński płaci to ustępstwami wpisanymi w gramatykę,
a jedno z nich dotyczy właśnie grupy luźnej
([niżej](#a-full-scale-grammar-pays-the-ambiguity-tax-too)).

Olski tej pozycji nie ma i nie jest to przeoczenie.
Każda fraza czytania obsadza u niego rolę, którą werdykt nazywa:
modyfikator dostaje nazwanego gospodarza,
okolicznik wyrażony zdaniem dochodzi do zdania składowego
([subset.md](subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)),
a przysłówki dostają wspólną listę.
Frazy bez roli streszczenie nie ma czym nazwać,
więc analiza dochodzi do końca zdania i nic go nie zamyka:

```sh
python3 -m olski.check -c "Czytałaś, dziewczyno.
Gotuj mieszaninę dwie godziny."
```

```text
<text>: rejected  Czytałaś, dziewczyno.
                  brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
<text>: rejected  Gotuj mieszaninę dwie godziny.
                  brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
olskie: 0 z 2 zdań; z odczytaniem: 0
```

Do wzięcia jest z tego mechanizmu sufit, a nie sama pozycja.
Wpuszczenie pozycji bez roli odwracałoby dwie rzeczy naraz:
werdykt, który role nazywa, i wieloznaczność, którą taka pozycja mnoży.
Konstrukcje z listy wyżej wchodzą więc do olskiego pojedynczo, każda ze swoją rolą,
a to, co ta pozycja robi z liczbą czytań, olski ma już u siebie o rozmiar mniejsze:
płaska lista przysłówków daje zdaniu kształt, który mówi o nim nieprawdę
([subset.md](subset.md#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę)).

### The comma as a grammatical attribute

Every nonterminal in `gfjp2.dcg` carries `Pk`,
its *przecinkowość* — what it demands of the comma slot on each side —
combined by `oblpk` against a compatibility relation `zgodne_pk`.
Empty commas are inserted into the inflection graph beforehand,
so a comma slot exists at every position whether or not one was written.
The value lattice is the interesting part:
a comma, a forbidden comma, either,
a forced comma that may not migrate inward,
a forced absence,
a *permissible* omission,
and four more for the edges of an utterance.

This is what a comma rule looks like
when it is derived from the parse instead of matched in the text,
and it comes with a design note olski should copy outright.
The clause admitting a missing comma before a coordinator
sits under a comment saying that blocking it
backs out of a permissiveness the author calls ruinous.
One line, two severities.
A rule engine wants exactly that knob,
and here it is expressed in the grammar rather than beside it.

### One gap instead of a different complexity class

Woliński's grammar handles discontinuity with a nonterminal spelled `ξ`.
A phrase with a hole carries its own requirement,
the sequence admits **at most one** such phrase —
`wykryjξ` is a single clause, which is the whole enforcement —
and the borrowed requirement is discharged later
against the phrase that owns it.
Two limits are written into the rule itself:
subjects do not extract, and a phrase with a hole does not extract.

That is a slash feature threaded through a free-order sequence,
which puts it at tier 2 rather than tier 3.
Woliński's own list of what the grammar covers
includes common discontinuous structures,
and this is the machinery that covers them.
Whether olski had to leave the context-free tier to scramble was a real fork,
and here is a working parser of Polish that did not have to,
having bounded the gap to one and excluded subjects from it.
The same machinery is what made that fork answerable,
because `ξ` stands in the treebank on the phrases the gap was needed for,
so they can be counted:
[design-notes.md](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
holds the count, the refusal it produced, and the price beside it.
What the count does not say is the other direction,
namely what fraction of real Polish the discipline gives up,
since a sentence this grammar could not analyse carries no gold tree to count.

### A full-scale grammar pays the ambiguity tax too

[The second currency](design-notes.md#the-second-currency-ambiguity)
argues that ambiguity, not formal power,
is the cost that will make the project unpleasant if ignored.
`gfjp2.dcg` contains the same argument in the form of concessions.
Genitive is blocked in loose adjunct noun phrases
under a comment naming the explosion that forced it.
The attribute tracking interrogative and relative marking
is pinned to its neutral value in one nominal rule,
because the alternative produced duplicate analyses.

Woliński had no coverage budget to respect and conceded anyway.
That is evidence the tax is real
rather than an artefact of writing a small grammar,
and it comes from a grammar of Polish
large enough for the concession to be visible.

### The grammar carries its own examples

`gfjp2.dcg` holds 437 lines beginning `%%%%`
and 53 beginning `%%%*`:
sentences that must parse and sentences that must not,
sitting directly beneath the rules that license them.

```text
%%%% Gotować mieszaninę dwie godziny.
%%%* Gotować Jan mieszaninę dwie godziny.
```

That is the convention this repository asks of tests,
applied to a grammar,
and the reason it survives decades of editing
is that the example is physically attached to the rule it exercises.
A grammar rule in olski could carry the same thing,
extracted by a test rather than read by a human.

### Failure is diagnosable, and coverage is measured against gold

An unknown word raises a distinct exception
rather than joining the general failure to derive,
so "Morfeusz did not know this form" and "the grammar did not license this"
stay separate answers.
Each analysis emits its tree count, edge count, inferences and CPU time.

The evaluation script goes further.
For each treebank sentence it walks the packed forest
counting the trees *consistent with the corpus disambiguation*.
Coverage there is not whether the parser produced something,
but whether the gold reading is in the forest
and how deeply it is buried among alternatives.

Olski asks both halves, in that order.
`Las.numer_czytania` in `olski/parse.py` walks the packed positions
for a reading assigning the roles the gold tree assigns,
so a gold reading past the enumeration cap comes back found rather than missing;
only then does it walk the enumeration to the tree carrying that reading,
and the depth is where that walk stopped.
[corpus.md](corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym)
holds what both answers say about the sentences olski refuses for ambiguity.
Where the gold tree meets a packed position is settled there by the roles:
a position stands for a shape rather than for a tree,
and two grammars share no bracketing to compare shape by shape.
The verdict is what asked for the forest first
([design-notes.md](design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)),
and this is the reason for it that comes from the measurement instead.

## Którędy GFJP wchodzi do olskiego

Mechanizmy [warte wzięcia](#what-the-code-does-that-olski-should-take)
są kanałem świadomym i cały ten dokument nim jest.
Poza nim GFJP dochodzi tutaj kanałami, których nikt nie wybierał,
bo zasoby, na których olski się opiera, napisał Woliński:
Morfeusz 2 ustala znaczniki,
Walenty ustala leksykon walencyjny,
a Składnica ustala, na czym mierzy się pokrycie.

Składnica kosztuje z nich najwięcej i mówi o tym
[corpus.md](corpus.md#what-this-number-is-not):
drzewa Składnicy pochodzą z wyjścia Świgry,
więc pomiar nad nią nie odrzuci decyzji zgodnej z GFJP.
Architektury to nie dotyczy,
bo dwa formalizmy da się położyć obok siebie i różnica jest widoczna —
inaczej nie powstałby ten dokument.
Dotyczy pojedynczej decyzji o konstytuencie:
który gospodarz przyjmuje frazę, gdzie kończy się grupa.
Tam jedyny przyrząd, jaki olski ma,
przyzna GFJP rację niezależnie od tego, skąd ta decyzja przyszła.

Składnica sięga przy tym dalej niż liczba pokrycia.
Warstwa statystyczna za parserem zajmuje w olskim to samo miejsce potoku,
co komponent Świgry, i liczy się nad tym samym bankiem drzew:
`olski/skłonności.txt` wychodzi ze Składnicy tak samo, jak wyszedł z niej tamten.
Nowe jest nie to miejsce, a typ odpowiedzi —
świadek zawęża z powodem albo milczy, a ranker odpowiada zawsze —
i o tym mówi
[disambiguation.md](disambiguation.md#kontekst-rozstrzyga-wykluczeniem-a-nie-rankingiem).
Zbieżności tej nie wymusza sam problem,
tylko to, że bank drzew polszczyzny jest jeden.

Kolejka blokerów jest kanałem osobnym od pomiaru,
choć drukuje ją ten sam przebieg:
ustawia ona olskiemu porządek robót.
Nazywa część mowy, na której analiza stanęła
([corpus.md](corpus.md#where-the-analyses-stop)),
a wpuszczenia powołują się na jej wiersze wprost:
czas przyszły wszedł stamtąd
([subset.md](subset.md#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony)).
Wiersz liczy jednak tylko zdania z drzewem wzorcowym, bo tyle mierzy przebieg,
a drzewa nie ma tam, gdzie Świgra dobrego nie znalazła
([corpus.md](corpus.md#what-the-corpus-contains)),
więc konstrukcja potrzebna w takim zdaniu nie staje w kolejce wcale:
zdania, którego nikt nie rozebrał, nikt też nie przeliczył
([design-notes.md](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)).
Pomiar mówi przez to, jak oceniono gramatykę dzisiejszą,
a kolejka mówi, która konstrukcja powstanie następna.
Odpowiedzią na to jest ta sama kolejka policzona nad własnym dokumentem
([corpus.md](corpus.md#the-same-queue-over-prose)).

Kanał, którego nie ma jak sprawdzić, został tu nazwany właśnie dlatego.
Prozę i kod tego repozytorium pisze sesja modelu językowego,
a Świgra jest publiczna od dwóch dekad razem z monografiami, które ją opisują,
więc decyzja może dotrzeć do olskiego już w kształcie, który nadała jej GFJP,
a introspekcja modelu tego nie rozstrzygnie.
Rozstrzyga porównanie kodu z kodem,
i o tyle właśnie czytanie źródła jest tu warte więcej niż zapewnienie.

## Sources

- <https://zil.ipipan.waw.pl/Świgra> — the parser, its licence terms and its packages
- <http://nlp.ipipan.waw.pl/Bib/woli:04.pdf> — Woliński, *Komputerowa weryfikacja gramatyki Świdzińskiego*, 2004, which documents Świgra 1 and Birnam
- <https://www.wuw.pl/data/include/cms/Automatyczna_analiza_skladnikowa_Wolinski_Marcin_2019.pdf> — Woliński, *Automatyczna analiza składnikowa języka polskiego*, 2019, which documents the second grammar
- <http://walenty.ipipan.waw.pl/> — Walenty, the valency dictionary the lexicons are generated from
