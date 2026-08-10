# Design notes

Decisions that have been taken are marked as such;
everything still open lives in [open-questions.md](open-questions.md).
The target this grammar is grown towards is in
[roadmap.md](roadmap.md#celem-toru-jest-to-readme),
and the optional linter track beside it,
which reaches this grammar as its deepest analysis tier,
is in [linter.md](linter.md).

## What olski is

*Język olski* is *język polski* with the *p* filed off,
along with the parts of Polish that make it hard.
It is an artificial subset of Polish,
designed rather than described,
small enough that a machine can check it
cheaply, deterministically, and explainably.

The goal on this track is fun and experimentation.
That is the actual goal, not a modest way of stating a real one.
There is no application driving the design,
and any construction may be cut for being boring or annoying.

The scoreboard here is internal consistency:
a grammar that contradicts itself is broken
whether or not it matches usage.
That is a narrower criterion than the linter's,
and the difference is deliberate.
The linter is judged against a corpus of real Polish
because its whole claim is about how Poles actually write;
see [linter.md](linter.md#the-thing-that-makes-or-breaks-it-calibration).
A designed subset is judged against itself first,
and against Składnica only when it wants a coverage number.

## Decisions taken

**Olski should be as close to Polish as possible.**
Not a convenient toy subset,
but a language a Polish speaker would read as ordinary Polish.

**Closeness is traded against parser complexity, deliberately and measurably.**
Every construction admitted has a cost,
every cost buys some quantity of representable structure,
and the exchange rate is the thing worth studying.
See [the cost ladder](#the-cost-ladder) for what the currency actually is.

**No formalism is committed to.**
The track's target names a property of a sentence and no machinery,
so a mechanism stronger than a context-free grammar,
or one standing beside the grammar rather than inside it,
is a question of price rather than of permission.
See [Formalizm jest środkiem, a nie celem](#formalizm-jest-środkiem-a-nie-celem).

**Olski is a proper subset of Polish.**
Every olski sentence must be a well-formed Polish sentence.
No helper notation in the surface form,
no small deviations from Polish grammar for convenience.
Most controlled languages do not honour this;
see [similar-work.md](similar-work.md#the-word-subset-is-usually-a-lie).

**The lexicon is open, over Morfeusz 2.**
Closeness to Polish requires real inflection,
and a hand-built lexicon would make olski
close to a few hundred words of Polish rather than to Polish.
This settles what was the largest fork on this track.

Morfeusz specifically, and not Morfologik,
because this track needs **generation**:
a lemma plus a tag yielding a surface form.
The linter track needs only analysis,
and [reaches for Morfologik instead](roadmap.md#milestone-5-morphology-binding-and-the-rules-that-needed-it).
Two dictionaries for two jobs,
not one decision recorded twice.

## Two angles of the grammar track

Within this track there are two directions,
and they turned out to be one system.

**Parsing.** Polish text goes in, structure comes out.
The interesting artifact is the parser
and the question of how far a context-free grammar stretches
over Slavic morphosyntax.

**Skład.** Structure goes in, Polish text comes out.
Some source description, machine-checkable and human-authorable,
compiles into final text,
with the checks guaranteeing syntactic correctness.
Polish supplies the pun for free:
*skład* is typesetting,
*składnia* is syntax,
so a syntax-checking typesetter is one word.

The second direction is the more promising one,
because it dissolves the hardest problem in the first.
See [the round-trip invariant](#the-round-trip-invariant)
for why both survive anyway.

## Why a subset, really

The obvious justification is that natural language is not context-free,
so a CFG cannot parse Polish.
That is true in the strict sense,
but the textbook arguments are not the ones that matter here.

The real non-context-free arguments are narrow:
cross-serial dependencies in Swiss German (Shieber 1985),
unbounded reduplication in Bambara (Culy 1985).
Polish supplies neither.
The mid-1980s claims that English is not context-free
were largely dismantled by Pullum and Gazdar.

And a CFG augmented with finite-valued features
compiles down to a plain CFG.
Case, number, gender, and person are all finite,
so agreement is not a position in the Chomsky hierarchy.
It is a symbol-count problem.
A rule like `NP → Adj N` with agreement over
case (7) by number (2) by gender
(5 on the simplest analysis, more in most Polish tagsets)
is seventy instantiations at minimum:
fine for a machine, unreadable for a human,
which is why the grammar is authored with features
and expanded or unified by the toolchain.

So for a comfortable subset,
the reason to design one is **ambiguity management**, not decidability.

Committing to closeness to Polish changes that answer.
See [discontinuity](#the-cliff-discontinuity),
which is where the hierarchy stops being a technicality.

## What actually makes Polish hard

None of these are about tree shape.
Polish syntactic structure is not exotic.
The combinatorics live in the morphology-syntax interface.

**Case syncretism.**
`kobiety` is genitive singular, nominative plural, and accusative plural.
`okno` is nominative and accusative singular.
Every noun contributes several readings before parsing starts,
and the only way to narrow them
is agreement with something that may itself be syncretic.

**Free word order.**
`Jan widzi Marię`, `Marię widzi Jan`, and `Widzi Jan Marię`
are all well-formed and express the same predication.
A CFG expresses this only by enumerating permutations,
and *n* daughters means *n!* rules.

**Genitive of negation.**
`Widzę książkę` takes accusative.
`Nie widzę książki` takes genitive, obligatorily,
and the shift propagates down the object chain.

**Numeral phrases.**
`Dwie kobiety przyszły` is nominative with feminine plural agreement.
`Pięć kobiet przyszło` takes a genitive plural complement
and a neuter singular verb.
`Pięciu mężczyzn przyszło` does the same for masculine personal gender.
The numeral phrase's own case, number, and gender for agreement purposes
are a fiction distinct from anything inside it.

**Pro-drop and mobile clitics.**
`Przyszedłem` has no subject noun phrase.
`Gdzieś był?` is `Gdzie byłeś?`
with the person marker detached and clitized onto the interrogative.

## The cost ladder

"Parser complexity against represented structures"
suggests coverage can be bought incrementally.
Mostly it can.
But the price is not a smooth curve:
there is one step where it jumps by an exponent,
and knowing where that step sits
matters more than any other fact in the tradeoff.

| Tier | Buys | Cost |
| --- | --- | --- |
| 0 | CFG with finite features | Agreement, government, fixed-ish order. Earley, cubic |
| 1 | Dominance separated from precedence | Free order among sisters. Still cubic, grammar preprocessing |
| 2 | Slash and gap features | Unbounded movement, bounded discontinuity. Still context-free, symbol count multiplies |
| 3 | LCFRS, MCFG, or TAG | Genuine discontinuous constituents. Sixth power at fan-out 2 |
| 4 | Full unification, HPSG style | Everything. Undecidable in general |

Tiers 0 through 2 are the same asymptotic parser with a larger grammar.
Tier 3 is a different algorithm in a different complexity class.

### The ladder is not the Chomsky hierarchy

The ladder's rungs are chosen by what a formalism buys over Polish
and by what parsing one costs,
so the hierarchy's own next class does not appear on it.
A context-sensitive grammar in the type-1 sense writes `αAβ → αγβ`:
one non-terminal on the left,
productions named the way a CFG's are.
It is still the wrong thing to reach for.

Deciding whether a sentence is in the language of a type-1 grammar
is PSPACE-complete,
the class being exactly what a linear-bounded automaton accepts
(Kuroda 1964),
which ends parsing rather than making it expensive.
And a type-1 derivation is a sequence of rewrites and not a tree,
where every question olski asks is a question about a tree:
which phrase is the subject,
where a modifier attached,
and whether two derivations are
[one reading](subset.md#co-się-liczy-jako-jedno-czytanie).
Nor is the surplus one Polish has a use for.
Type 1 adds copying and counting,
which is the direction the Swiss German and Bambara arguments run in
and the direction Polish does not go.

Where Polish does exceed context-free is discontinuity,
and named productions reach it without any of the above.
An MCFG production is written and named like a CFG's,
and what changes is that a non-terminal spans a tuple of intervals
rather than a single one:

```text
A(x1 y1, x2 y2) → B(x1, x2) C(y1, y2)
```

`A` there has **fan-out** two — its yield arrives in two pieces —
and the production says how its daughters' pieces interleave,
which is a discontinuous constituent stated as a named rule.
So the quantity to trade against is fan-out
rather than a position in the hierarchy,
and [the cliff](#the-cliff-discontinuity) is what fan-out two would buy.

### The cliff: discontinuity

Polish permits left-branch extraction
that splits a noun phrase around the rest of the clause:

```text
Jakie Jan czyta książki?
```

`jakie … książki` is one noun phrase
with the subject and verb sitting inside it.

This is not a curiosity invented for the argument.
Ross's (1967) Left Branch Condition,
which blocks exactly this in English,
fails across most of Slavic,
with Polish and Czech named as the standard exceptions:
Polish extracts wh-determiners, degree adverbs,
and attributive adjectives out of the noun phrase.
See Bošković, *On the locality of left branch extraction
and the structure of NP* (Studia Linguistica, 2005),
and for Polish specifically the empirical study in
*Extraction facts and the internal structure
of nominal constructions in Polish*
(Poznań Studies in Contemporary Linguistics, 2017).
Slavic also permits the split halves in more orders
than German does.

Discontinuous constituency is exactly what LCFRS and TAG exist for,
and it is the reason German treebank parsing
grew a whole discontinuous-parsing subfield.
Binary LCFRS with fan-out at most two
covers most cases found in real treebanks.

So the commitment to closeness to Polish
produces one concrete fork,
and it is not a difficulty gradient:
**may olski scramble across constituent boundaries?**
No keeps the project at tier 2
with a cubic parser and a large grammar.
Yes means paying for discontinuity,
which the ladder prices at tier 3.
A bounded gap buys the common cases from tier 2 instead,
giving up a fraction of Polish nobody has measured:
[swigra.md](swigra.md#one-gap-instead-of-a-different-complexity-class)
holds a parser of Polish that takes that route.
Everything else in the subset is cheap next to this.

### The second currency: ambiguity

The ladder measures formal cost.
It misses the tax that closeness to Polish actually levies.

Free word order times case syncretism
means a six-word sentence can carry dozens of readings,
and the parser is *correct* to produce all of them.
That cost lands in forest size
and in whatever has to consume the forest,
not in the grammar's line count.

So parser complexity is two numbers:

- **Formal cost** — tier on the ladder,
  rule count after expansion,
  measured parse time
- **Ambiguity cost** — mean readings per sentence,
  forest node count

The second is the one that will make the project unpleasant if ignored,
because a grammar that admits everything
is easy to write and useless to use.

### Making the trade measurable

Kuhn's PENS scheme already defines
the axes this project wants to trade along.
Its Simplicity dimension is implementation cost,
measured in pages of description
sufficient for someone to write a correct parser;
its Expressiveness dimension is how much can be said.
Olski's cost-versus-coverage curve
is the S-versus-E plane of a scheme
that already has a hundred languages plotted on it.
See [similar-work.md](similar-work.md#pens-and-why-it-matters-here).

For the coverage side there is a ready benchmark:
Składnica holds thousands of real Polish sentences with gold trees.
For each tier of the ladder,
measure what fraction of a sample olski accepts —
one reading, and the gold one —
and plot that against tier.

That curve is the experiment.
How much real Polish per unit of formal power
is a question with a real answer
that nobody has computed for this grammar.
Its first point is computed,
and [corpus.md](corpus.md) holds it,
with the breakdown and the reasons not to over-read the figure.

The curve does not only rise,
because what olski accepts is uniqueness rather than derivability.
Admitting a construction only ever adds derivations,
so a tier buys the sentences it makes derivable
and charges for the ones that had a single reading and now have two.
Each point is a net of those two counts,
and a tier can cost more sentences than it buys.
Tier 0 already spends that way on purpose in one place:
[the bare verb-initial order](subset.md#the-bare-verb-initial-order-keeps-the-predicative-one-honest)
was admitted knowing it takes a sentence's uniqueness with it,
and [corpus.md](corpus.md#what-morphological-ambiguity-costs)
watches the same exchange arriving from the morphology instead.

The curve also supplies a principled way to say no:
a tier whose net comes to three percent of sentences
for a jump from cubic to sixth-power parsing
decides itself.

## Formalizm jest środkiem, a nie celem

Drabina wycenia formalizmy i żadnego nie obiecuje.
Gramatyka bezkontekstowa z cechami jest tym, na czym olski stoi,
a nie tym, do czego zmierza:
kryterium, po którym poznać koniec tego toru,
mówi, co ma zajść nad zdaniem, a nie czym ma być wyprowadzone,
i trzyma je [roadmap.md](roadmap.md#celem-toru-jest-to-readme).
Wybór szczebla jest więc rachunkiem, a nie deklaracją.

Ruszyć wolno obie warstwy.
W warstwie implementacji ruszają się parser i sposób liczenia czytań:
[subset.md](subset.md#implementation) mówi, co stoi dzisiaj,
a [sekcja niżej](#angle-one-parsing) mówi, co po tym przyjdzie.
W warstwie siły rusza się to, co produkcja w ogóle umie powiedzieć,
i [urwisko](#the-cliff-discontinuity) jest miejscem,
w którym ten ruch kosztuje wykładnik,
a nie miejscem, w którym coś jest zakazane.

Środek nie musi też stać na drabinie,
a repozytorium już tak pracuje, więc jest to opis, a nie obietnica.
Czytania, których żadna produkcja nie odbiera, odbiera kod obok gramatyki:
`admissible` w `olski/subset.py` wyrzuca rzeczownik nieodmienny tam,
gdzie ta sama forma czyta się także jako słowo funkcyjne,
a po co, mówi [subset.md](subset.md#the-dictionary-offers-readings-polish-does-not).
Nieciągłość zaś ma wyjście tańsze niż szczebel, na którym stoi:
Świgra przeciąga przez ciąg o swobodnym szyku jedną lukę
([swigra.md](swigra.md#one-gap-instead-of-a-different-complexity-class)),
co jest odpowiedzią z tier 2 na problem z tier 3.
Odpowiedzią na to, co olski ma przyjmować, nie musi więc być
ani produkcja, ani wyższa klasa złożoności.

Otwarte są środki, a nie własności.
Wiąże to, [czym olski jest](#what-olski-is):
sprawdzalny tanio, deterministycznie i z wyjaśnieniem.
Wiąże to, co [rozstrzygnięto](#decisions-taken):
olski zostaje podzbiorem polszczyzny bez notacji pomocniczej.
Wiąże wreszcie to, czym czytanie jest, czyli drzewo,
i to jest powodem, dla którego typ 1 hierarchii odpada mimo swojej siły
([drabina to nie hierarchia](#the-ladder-is-not-the-chomsky-hierarchy)).
Mechanizm, który którąś z tych własności łamie, odpada przez nią,
a nie przez to, że stoi wyżej niż gramatyka bezkontekstowa.

### Podłoże więzowe zmierzone sondą

Otwartość środków była deklaracją, dopóki nikt żadnego innego nie wycenił.
`sonda/` wycenia jeden: ten sam podzbiór powiedziany łukami nad grafem segmentów,
gdzie zgodność jest warunkiem na parę słów,
szyk osobnym polem deklaracji,
a spójność frazy jednym warunkiem globalnym, który wolno zdjąć.
Wyszło z tego, że oba opisy mówią nad prozą README prawie to samo,
że szyk i przyłączenie nie kosztują po tej stronie ani jednej deklaracji,
a nieciągłość jest jedną wartością logiczną,
i że cena stoi w trzech miejscach wymienionych niżej.
Wyszło z tego także to, czego nikt nie szukał:
dwa z trzech zysków nie żądają tego podłoża wcale.
Szyk i przyłączenie kupuje rozdzielenie dominacji od precedencji,
czyli szczebel 1 [drabiny](#the-cost-ladder), sześcian i gramatyka bezkontekstowa,
i tylko nieciągłość zostaje przy podłożu, którego olski nie ma.
Decyzji o przeniesieniu olskiego na to podłoże nie ma,
a ruch, który z sondy wynika, jest tańszy niż ona sama
i trzyma go [TODO.md](../TODO.md).

Powtarzają to te polecenia, a ostatnie warto puścić także bez flagi:

```sh
python3 -m harness.markdown README.md --into proza/
python3 -m sonda proza/README.txt
python3 -m sonda proza/README.txt --budżet 0.1
python3 -m sonda -c "Dobrą Jan pisze polszczyznę." --nieciągłe --łuki
```

Proza README ma 56 zdań.
Wszystkie sonda rozbiera w budżecie 10 sekund na zdanie,
a jednemu z nich zajmuje to ponad pięć sekund, czyli więcej niż cała reszta razem,
i widać to po przebiegu z budżetem dziesiątej części sekundy: kończy go 55 z nich.
54 z tych 56 dostaje od obu programów ten sam werdykt,
a 53 tę samą liczbę czytań,
i to drugie jest mocniejszym z dwóch odczytów:
werdykt zgadza się już wtedy, gdy jedna strona ma dwa czytania, a druga sześć,
a liczba nie, i `Koszt samej szynki przewyższa koszt szynki z dodatkami`
wychodzi po obu stronach dokładnie sześcioma.

**Szyk i przyłączenie schodzą z produkcji na nic.**
`olski/subset.py` ma kilkanaście produkcji `ClauseConjunct`,
bo każdy szyk wypisuje się osobno, a każdy z nich jeszcze raz w tylu wersjach,
ile ma miejsc na okolicznik.
Łuk podmiotu nie mówi o porządku nic,
więc SVO i OVS są tam jedną deklaracją,
a jedenaście pozycji na okolicznik jest trzema, po jednej na głowę,
i dwa czytania `Program zapisuje ustawienia w pliku`
biorą się z tego, że dozwolone są oba łuki.

**Nieciągłość przestaje być szczeblem.**
`Dobrą Jan pisze polszczyznę` nie wyprowadza się w olskim wcale,
a po zdjęciu spójności wychodzi z niego czytanie,
w którym `Dobrą polszczyznę` jest jedną frazą przerwaną podmiotem i orzeczeniem.
Kosztuje to jedno pole i zero deklaracji,
bo spójność jest tu warunkiem wystawianym, a nie własnością formalizmu.
[Urwisko](#the-cliff-discontinuity) wycenia to samo na szósty stopień
i wycenia poprawnie, tylko że wycenia szczebel, a nie zjawisko:
przy tym podłożu fan-out nie jest pokrętłem, którym się cokolwiek kręci.

**Odrzucenie zaczyna mówić, na czym stanęło.**
Słowo, do którego żaden łuk nie dochodzi, wypisuje się przy werdykcie,
i nad zdaniem o konwencjach z README wychodzą z tego trzy przecinki i `commitów`.
Jest to ta sama informacja, którą `olski-corpus` liczy jako bloker
i której `olski-check` nie podaje wcale,
tylko wzięta nie z najdalszego osiągniętego punktu, a z pustej dziedziny.
Podłoże daje ją przy tym za darmo, bo licencja łuku i tak stoi policzona.

**Cena pierwsza: cztery rodzaje deklaracji ponad licencję łuku.**
Każdy z nich nazywa coś, co produkcja ma darmo,
i każdy znalazł się nie przy pisaniu, tylko przy pierwszej rozbieżności.
Zgodność orzecznika z podmiotem idzie w produkcji przez wspólną matkę,
a między parą słów nie przechodzi,
bo forma osobowa rodzaju nie niesie.
Przyimek bez swojej grupy imiennej jest dozwolonym okolicznikiem,
dopóki nikt nie napisze, że grupy brakować nie może.
Dwa rzeczowniki obok siebie są członami współrzędnymi bez spójnika,
dopóki łuk członu nie zażąda spójnika i odwrotnie.
Czasownik bierze naraz dopełnienie i orzecznik,
dopóki nie napisze się, że tych dwóch razem nie bierze.

**Cena druga: jednoznaczność olskiego stoi częściowo na braku produkcji.**
Trzy razy sonda pokazała czytanie,
którego gramatyka bezkontekstowa nie ma nie dlatego, że je wyklucza,
tylko dlatego, że nikt odpowiedniego ciała nie wypisał:
dopełnienie przed czasownikiem bez podmiotu,
dwa dopełniacze przy jednym rzeczowniku,
i dopełnienie doczepione do dalszego bezokolicznika w łańcuchu
`ma pomagać pisać`.
Dwa pierwsze zamyka deklaracja i są w `sonda/polszczyzna.py` zamknięte.
Trzeciego nie zamyka nic poza leksykonem walencyjnym,
i to jest ta jedna rozbieżność, która nad próbką została:
`To ma pomagać pisać dobrą polszczyznę` wychodzi w olskim jednoznaczne,
a w sondzie trzema czytaniami różniącymi się tym, który czasownik bierze biernik.
[Leksykon](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej) sięga do tego
po stronie olskiego, bo mówi, że `pomagać` biernika nie bierze,
a sonda ma po swojej stronie warunek na sam lemat kopuli,
więc rozbieżność jest tym, o ile leksykon wyprzedził tamtą deklarację.
Wpisem, a nie produkcją: to jest to, co ten etap kupił.

**Cena trzecia: nie ma ograniczenia, które ma parser tablicowy,
i widać to na jednym zdaniu.**
Earley jest sześcianem w najgorszym przypadku, a przeszukiwanie więzów nie jest
niczym, i najdroższe jest tam, gdzie żadne słowo nie wypada lokalnie,
bo wtedy przycinanie dziedzin nie ma czego uciąć,
a policzenie czytań każe przejść całą przestrzeń.
Takim zdaniem jest w README dokładnie jedno,
to samo, które [corpus.md](corpus.md#where-the-analyses-stop) wskazuje
jako jedyne odrzucone bez ani jednej formy, której jakaś produkcja nie bierze,
czyli stojące na kształcie, a nie na słowniku:
`Zbiór tekstów przechodzących przez wszystkie reguły jest podzbiorem
polszczyzny w jednym i w drugim przypadku`.
Sonda liczy je ponad sześć sekund,
gdzie każdemu z pozostałych 42 zdań wydaje werdykt
poniżej trzech setnych sekundy, czyli o dwa rzędy wielkości szybciej.
Trzyma tę liczbę warunek na lemat kopuli w deklaracji dopełnienia,
czyli walencja powiedziana po tej stronie:
bez niego to samo zdanie liczy się ponad dwadzieścia sekund
i budżetu nie dowozi wcale,
więc przestrzeń, którą przycina jedna pozycja ramy,
jest tutaj trzema czwartymi najgorszego przypadku.
Tej różnicy nie zdejmie lepsze przycinanie,
bo tu nie ma czego przyciąć:
każdy łuk tego zdania jest dozwolony,
a wykluczanie zostaje na kształcie całego drzewa.
Pytanie „czy czytanie jest jedno” tego nie ratuje,
choć wygląda, jakby miało:
werdykt „dwa czytania” zamyka się na drugim modelu i wychodzi tanio,
a werdykt „jedno czytanie” wymaga przeszukania wszystkiego i nie tanieje wcale.

To samo zdanie mówi jeszcze coś, czego sonda nie miała mierzyć.
Wychodzi z niej jednym czytaniem, którego olski nie ma wcale,
a to czytanie nie jest tym, które ma czytelnik:
`w jednym i w drugim przypadku` wychodzi tam współrzędnością rzeczowników
zamiast dwoma wyrażeniami przyimkowymi.
Jednoznaczność bez trafności jest więc osiągalna,
i to jest ten argument, dla którego pomiar pokrycia
chce wiedzieć, czy złote czytanie jest wśród czytań,
a nie tylko ile ich jest
([swigra.md](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)).

Zostaje przy tym poza pomiarem to,
czego sonda nie umie i o czym nie da się przez to powiedzieć nic.
Współrzędność wisi w niej pierwszym członem,
więc liczba całej grupy jest liczbą pierwszego członu,
a `rozum i sumienie` w roli podmiotu mnogiego przez parę słów nie przechodzi.
Zdania, którego graf segmentacji się rozchodzi, sonda nie rozbiera wcale.
I trzecia rzecz, ta najbliższa temu, po co olski jest:
raport nazywa podmiot napisem tylko dopóki spójność stoi,
bo poddrzewo bez niej jest zbiorem słów, a nie odcinkiem tekstu.
Nieciągłość kupuje się więc na parserze, a płaci na wydruku.

## Angle one: parsing

Whatever parses olski must produce a **forest, not a tree**,
because genuine ambiguity is the normal case
and the useful operation is to enumerate readings and filter them.

GLR is the right shape of answer but probably the wrong specific choice:

- GLR's payoff is a precomputed table
  giving near-deterministic speed on mostly unambiguous input.
  An olski grammar will be conflict-dense throughout,
  so the graph-structured stack works hard on nearly every token
  and most of the speedup never arrives.
- Table construction over a permutation-expanded free-word-order grammar
  can blow up badly.
- Tomita's original algorithm breaks on nullable rules,
  so pro-drop would force RNGLR or BRNGLR (Scott and Johnstone).

**Earley is the boring recommendation and probably the right first move.**
It handles any CFG, including left recursion and nullable rules,
with no preprocessing;
it produces a shared packed parse forest natively;
its worst case is cubic but real grammars behave far better.
Decisively for a project whose grammar is still being designed:
the grammar can change without rebuilding an automaton.
Get the grammar right against Earley,
then treat GLR as an optimization if measurement ever demands one.

One correction to the above,
from measuring a working GLR system over real Polish:
the nullable-rules objection is historical.
Tomita's algorithm breaks on them,
maintained implementations do not.
The rest of the argument stands untouched —
that system's table is 146 states,
so it says nothing about what
a permutation-expanded grammar would cost to build.
It does supply a baseline worth flinching at:
20% of its input fails to parse
against a grammar hand-fitted to a register far narrower than olski.
See [glr-in-practice.md](glr-in-practice.md#measurements).

For free word order specifically,
the move that keeps a CFG viable
is to separate **immediate dominance from linear precedence**,
as GPSG did.
Dominance rules say what the daughters are,
separate precedence constraints say which orders are legal,
and a preprocessor deals with the factorial.
This also keeps the subset honest:
a permutation excluded from olski
is excluded by an explicit constraint rather than by omission.

### Werdykt jest zapytaniem o las, a nie listą czytań

Earley oddaje las ze współdzielonymi węzłami sam z siebie,
a nota w `olski/parse.py` odkłada go na moment,
w którym wymusi go lewa rekursja albo cena wyliczania.
Wymusza go wcześniej to, co werdykt ma powiedzieć autorowi,
i pokazują to dwa polecenia:

```sh
python3 -m olski.check -c "Program zapisuje ustawienia w pliku w katalogu." --readings
python3 -m olski.check -c "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci w firmie w kraju."
```

Każde doklejone wyrażenie przyimkowe podwaja liczbę czytań,
bo dochodzi do czasownika albo do rzeczownika przed nim,
a te wybory są od siebie niezależne.
Werdykt przestaje przy tym mówić cokolwiek nowego już przy drugim wyrażeniu.
`explain` w `olski/subset.py` nazywa te role, które się między czytaniami różnią,
i nad czterema czytaniami pierwszego zdania wypisuje `Modifier, Object`,
a nad sześćdziesięcioma czterema czytaniami drugiego wypisuje to samo,
bo `describe` w `olski/parse.py` bierze pierwszy węzeł roli, a nie wszystkie.
Liczba przestaje przy tym być liczbą,
bo `MAX_READINGS` ucina ją i werdykt czyta `64+`.
README obiecuje, że parser mówi, *jak* zdanie czyta się dwojako,
a lista czytań tej obietnicy nie dowozi nad zdaniem,
którego rejestr olskiego jest pełen.
Oba te napisy trzyma `tests/test_subset.py`,
więc sekcja nie rozjedzie się z kodem po cichu.

Wyliczanie nie jest tu drogie i nie o cenę idzie.
Nierozstrzygniętych decyzji stoi w drugim z tych zdań sześć,
po jednej na wyrażenie, a czytań sześćdziesiąt cztery,
i las ze współdzielonymi węzłami trzyma sześć węzłów spakowanych
zamiast sześćdziesięciu czterech drzew.
Werdykt wychodzący z takiego lasu wskazuje przyimek i dwie głowy,
do których dochodzi, czyli mówi to, co autor ma poprawić.
Tę samą wielkość nazywa już
[pytanie o czytelność prefiksu](open-questions.md#czy-jednoznaczność-prefiksu-mierzy-czytelność):
liczy się liczba nierozstrzygniętych decyzji, a nie liczba czytań.
Jedno pytanie i drugie żądają więc tego samego prymitywu.

Tańsze wyjście wygląda na dwie poprawki w kodzie i nim nie jest,
więc stoi tu zapisane, żeby nikt go nie proponował drugi raz.
`describe` nazywające wszystkie węzły roli zamiast pierwszego,
przy zdjętym `MAX_READINGS`,
daje nad drugim z tych zdań sześćdziesiąt cztery wiersze do porównania ręką.
Wydruk rośnie wtedy z liczbą czytań, czyli wykładniczo,
a nazwać trzeba liczbę decyzji, która rośnie z długością zdania.

Las jest przy tym jeden, a werdykty są nad nim różnymi podsumowaniami:
czy cokolwiek się wyprowadza, ile się wyprowadza, czy najwyżej dwa,
i czy złote czytanie jest wśród czytań oraz jak głęboko,
o co [pomiar chce pytać bank drzew](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold).
Żadne z tych pytań nie żąda innego parsera, tylko innego podsumowania.

### Co się pakuje, rozstrzyga tożsamość czytania

Las odpowiada na pytanie olskiego pod dwoma warunkami:
pod jedną pozycję ma iść to, co jest jednym czytaniem,
a liczba z jednej pozycji ma się łączyć z liczbą z sąsiedniej tak,
jak łączy je unifikacja.
Pierwszy ma odpowiedź, drugi jej nie ma.

Czytanie jest kwotowane po lematach, po wartościach cech i po częściach mowy
([subset.md](subset.md#co-się-liczy-jako-jedno-czytanie)),
więc pozycja tablicy trzymana osobno dla każdego środowiska cech
nie spakuje niczego i policzy wyprowadzenia zamiast czytań.
Jest to dokładnie ten błąd, który zapisuje
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure),
i ten, przez który
[obudowanie Świgry](swigra.md#why-wrapping-it-does-not-get-there)
jest pisaniem gramatyki po raz drugi.

Dzisiejszy enumerator tę dyscyplinę ma,
i dlatego zamiana nie jest przepisaniem:
`analyses` w `olski/parse.py` pamięta wynik pod `(nazwa, pozycja)`
i wylicza ciało wobec `EMPTY`, a żądania wołającego stosuje po fakcie,
więc tożsamość pozycji cech nie niesie.
Brakuje samego spakowania,
czyli wyprowadzeń grupowanych po sygnaturze,
gdzie sygnatura niesie zbiór środowisk cech, z którymi przechodzi.
Nadmiar, który to zdejmuje, bierze się z tego samego kwotowania:
`zapisuje` ma dwa lematy, a lemat do sygnatury nie wchodzi,
więc `Program zapisuje ustawienia.` wyprowadza się dwa razy na jedną sygnaturę,
i mnoży się to przez każde następne słowo, któremu słownik daje dwa lematy.

Na czym drugi warunek się rozchodzi, pokazuje zdanie, które olski przyjmuje:

```sh
python3 -m olski.check -c "Zobacz docs/rules.md."
```

Czytanie ma jedno, a suma iloczynów po lesie liczy nad nim dwa.
`Complements` nad `docs/rules.md` buduje się dwiema produkcjami
z `build` w `olski/subset.py`, raz przez `Object`, raz przez `Predicative`,
bo [notacja rejestru](subset.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)
dostaje czytanie nieodmienne i stoi przez to w każdym przypadku.
Obie są czytaniami tej rozpiętości, więc pakowanie stawia je pod jedną pozycją
i robi z nimi to, czego pierwszy warunek żąda.
Rozchodzi się dopiero to, czym pozycja jest dla rodzica:
`Predicate → Verb Complements` wiąże jedną wspólną zmienną
ramę czasownika z pozycją, którą dopełnienie zajmuje,
a `zobacz` ma ramę domyślną, w której narzędnika nie ma.
Rodzic wskazuje pozycję, a nie wariant,
więc liczy oba, choć unifikacja przepuściła jeden.

Nadmiar jest więc wzięty z przeciwnej strony niż ten wyżej:
tamten bierze się z rozdzielenia pozycji, a ten ze sklejenia.
Cena jest przy tym inna, bo olski pyta o liczbę czytań, a nie o czytania:
zdanie przyjęte wychodzi z takiego lasu dwuznaczne,
czyli przewraca się werdykt, a nie sama liczba obok niego.
Na czym liczba ma stanąć zamiast iloczynu, trzyma [`TODO.md`](../TODO.md).

### Więzy wchodzą wyprowadzone z gramatyki, a nie napisane obok niej

Sonda pokazała dwie rzeczy, które więzy robią taniej niż produkcja:
przycinanie dziedzin przed szukaniem drzewa
i powiedzenie, na czym odrzucenie stanęło.

Kryterium, po którym taka warstwa wchodzi, jest jedno:
musi się wyprowadzać z gramatyki.
Napisana obok niej jest gramatyką napisaną dwa razy,
czyli tym drugim właścicielem faktu, przed którym broni
[`CLAUDE.md`](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely),
i jest to ten sam zarzut, który przewraca obudowanie Świgry
oraz ten, który [`TODO.md`](../TODO.md) stawia `sonda/polszczyzna.py`.
Wyprowadzona nie kosztuje ani jednej deklaracji.

Najtańszym kawałkiem takiej warstwy jest licencja terminala,
czyli pytanie, czy czytanie formy bierze jakikolwiek `Word` w gramatyce.
`licencjonuje` w `olski/grammar.py` stawia je wobec `EMPTY`,
i wolno tak, bo unifikacja tylko zawęża:
czytanie, którego bez środowiska nie bierze żaden terminal,
nie przejdzie przy żadnym.
Warunek na czytanie stoi przy tym raz, w `bierze` obok niej,
i pytają o niego rozbiór i licencja,
bo dwie kopie tego warunku byłyby dwoma właścicielami tego samego faktu
tak samo jak warstwa napisana obok gramatyki.

Drugi z dwóch zysków wychodzi z tego prawie wprost.
Forma, której w ten sposób nie zostaje ani jedno czytanie,
jest tym, na czym odrzucenie stanęło, i werdykt ją wypisuje:

```sh
python3 -m olski.check -c "Konwencje prozy, kodu, testów i commitów trzyma CLAUDE.md."
python3 -m olski.check -c "Nowa program zapisuje ustawienia."
```

Pierwsze zdanie stoi na przecinku i na polskiej formie, której słownik nie zna,
a drugie ma każdą formę wziętą i stoi na zgodności rodzaju.
Są to dwie różne odpowiedzi i dwie różne roboty do zrobienia,
i dlatego werdykt je rozdziela, tak jak
[rozdziela je Świgra](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold).

Owo „prawie” jest jedną rzeczą i bierze się stąd, że segmenty są krawędziami
grafu, a nie listą.
Morfeusz dzieli `Ktoś` na `Kto` i `ś` obok formy całej,
a `ś` nie ma ani jednego czytania, które bierze jakakolwiek produkcja,
i nie jest przy tym słowem, które ktokolwiek napisał.
Werdykt nazywa więc nie każdą pustą dziedzinę,
tylko krawędź, bez której nie ma drogi przez zdanie,
i `Ktoś zna docs/rules.md.` wychodzi przez to przyjęte, nie mówiąc o `ś` nic.
Zdanie, które ma czytanie, nie zgłasza tym samym żadnej formy,
i nie zgłasza jej z dowodu, a nie z przybliżenia:
ścieżka, którą to czytanie się wyprowadza, omija każdą krawędź, której nie wzięła.
Sonda tego pytania nie miała, bo
[zdania o rozchodzącym się grafie nie rozbiera wcale](#podłoże-więzowe-zmierzone-sondą).

Pierwszego zysku nie ma, a cena za niego stoi poza parserem.
Czytanie bez licencji nie zmienia dziś żadnego werdyktu,
bo `terminal` w `olski/parse.py` odrzuca je tak samo,
ani nie rusza `furthest`, który idzie w górę wyłącznie po dopasowaniu udanym,
więc wycięcie takiego czytania przed rozbiorem oddaje ten sam `Result`, tylko szybciej.
Rusza się co innego: `blocker` w `olski/coverage.py`
nazywa część mowy pierwszego czytania formy,
więc formie wyciętej do zera nazwałby brak struktury zamiast braku licencji,
a na tym odczycie stoi kolejka z [corpus.md](corpus.md#where-the-analyses-stop).
Wycięcie jest więc zmianą w kolejce, a nie w parserze,
i [`TODO.md`](../TODO.md) trzyma je razem z przebiegiem, który jest winne.

### Kierunek: produkcja się rozwarstwia, a podłoże zostaje

Wychodzi z tego kierunek i nie jest nim zmiana podłoża.
Produkcja zlewa w jedno trzy rzeczy,
i te trzy [sonda](#podłoże-więzowe-zmierzone-sondą) rozdziela:
zgodność, porządek i to, że konstytuent jest jednym odcinkiem tekstu.
Każda z nich ma wyjście, które zostaje przy szczeblu 2
[drabiny](#the-cost-ladder).
Zgodność wyszła do cech, zanim to pytanie stanęło.
Porządek wychodzi do warunków precedencji i ten ruch trzyma
[`TODO.md`](../TODO.md).
Spójność wychodzi do luki przeciąganej przez ciąg o swobodnym szyku,
więc [urwisko](#the-cliff-discontinuity) wycenia szczebel, a nie zjawisko.
Zostaje w produkcji to jedno, czego z niczym nie zlewa:
z czego konstytuent się składa.

Walencji produkcja nie mówi wcale, i jest to brak innego rodzaju niż tamte trzy.
Nie ma jej skąd wyprowadzić, bo stoi w leksykonie,
a dopisana produkcjami mnoży je przez czasowniki,
co [etap 2](roadmap.md#etap-2-walencja) liczy jako powód swojej kolejności.
Wchodzi więc cechą, którą czasownik niesie z leksykonu,
a to, co przy nim stoi, żąda w niej swojej pozycji
([subset.md](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)).
Mówi przez to, co czasownik bierze, i nie mówi, ile tego bierze:
liczba dopełnień zostaje w produkcjach,
a rama, która się zużywa, jest tym, czego olski nie ma i co pokazuje
[Świgra](swigra.md#valency-as-a-resource-that-gets-consumed).

Między dwoma wyjściami z nieciągłości rozstrzyga wydruk.
Sonda zdejmuje spójność jednym warunkiem globalnym
i traci nazwanie podmiotu napisem,
bo poddrzewo bez spójności jest zbiorem słów, a nie odcinkiem tekstu.
Luka oddaje pożyczone żądanie frazie, która je pożyczyła,
więc rozpiętość zostaje odcinkiem tekstu,
a werdykt olskiego wypełnioną rolę nazywa napisem.
Ile polszczyzny oddaje dyscyplina jednej luki, nie mówi żadne z dwóch wyjść,
i [Świgra tego też nie mówi](swigra.md#one-gap-instead-of-a-different-complexity-class);
a to jest ten pomiar, który cały ten kierunek by przewrócił.

Kolejność bierze się z tego, czego która rzecz potrzebuje.
Las idzie pierwszy, bo nie rusza ani jednej produkcji,
więc da się go porównać werdykt po werdykcie z tym, co stoi.
Walencja idzie przed precedencją, bo kasuje czytania,
a rozwinięcie permutacji je dopisuje,
i [`TODO.md`](../TODO.md) pyta wprost,
co preprocesor precedencji robi z ich liczbą,
czego bez lasu nie ma czym przeczytać.

Zostaje droga trzecia, czyli formalizm leksykalizowany,
i odpada ona na tym samym kwotowaniu.
Gramatyka kategorialna kupuje swobodny szyk kompozycją,
a płaci wieloznacznością pozorną:
jedna struktura zależności ma w niej wiele wyprowadzeń.
Kwotowanie po niej nazywa się postacią normalną i trzeba je utrzymywać,
czyli jest to ta sama robota, którą wycenia
[tożsamość czytania](#co-się-pakuje-rozstrzyga-tożsamość-czytania),
tylko wniesiona do własnej gramatyki zamiast napotkanej w cudzej.

### Cechy biorą to, co zawęża, jest symetryczne i lokalne

Zgodność zeszła z produkcji do cech,
a warto powiedzieć, co ją tam wpuściło,
bo to samo pytanie stoi przed każdą następną rzeczą,
którą ktoś zechce z produkcji wyprowadzić.
Unifikacja wzięła zgodność, bo zgodność ma trzy własności naraz:
przecięcie zbiorów tylko zawęża,
zgodność jest symetryczna między dwoma wiązkami cech,
a rozstrzyga się nad samą tą parą, bez oglądania się na resztę zdania.
Rzecz, która ma te trzy, kosztuje jedną zmienną.
Rzecz, której którejś brakuje, kanału cech nie dostaje,
i w tym repozytorium widać każdą taką wychodzącą bokiem.

Warunek ujemny nie zawęża, więc stoi poza `unify`.
`bez_lematów` w `olski/grammar.py` jest osobnym polem i osobnym testem,
bo przecięcie zbiorów nie ma jak powiedzieć „nie”.
Monotoniczność, spod której ten warunek ucieka, jest przy tym nośna:
`licencjonuje` pyta wobec `EMPTY` i odpowiada poprawnie tylko dlatego,
że unifikacja nigdy nie poszerza,
co [więzy wyprowadzone z gramatyki](#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)
biorą za darmo.
Jedyny warunek ujemny tej gramatyki płaci więc polem za to,
z czego wszystko obok niego żyje.

Rodzaj grupy współrzędnej nie jest symetryczny między członami,
bo polszczyzna wylicza go regułami, których unifikacja nie umie powiedzieć,
więc taka grupa nie niesie tej cechy wcale i `olski/subset.py` mówi to
przy tej produkcji.
Działa to dlatego, że `unify` pomija cechę, której konstytuent nie ma,
czyli tą samą linią, którą nieodmienna część mowy jest niewinna zgodności.
Nieobecność jest tu mechanizmem, a nie dziurą.

Walencja weszła tym kanałem i wypadła na lokalności.
Rama jest stanem, a nie zasobem, więc pozycji już zajętej nie ma jak odnotować,
a zajęcie zależy od pozostałych córek, a nie od samej pary głowy i zależnego.
Sonda zapłaciła za to samo dwoma polami:
`wymaga` i `zakazuje` w `sonda/wiezy.py` mówią o łukach jednej głowy naraz,
więc sprawdza je `_dopuszczalne`, gdy drzewo stoi już całe,
a nie tablica licencji, która stoi policzona przed szukaniem.
Co z tego zostaje po stronie produkcji,
mówi [kierunek](#kierunek-produkcja-się-rozwarstwia-a-podłoże-zostaje) wyżej.

### Wyliczone ciało myli się w stronę werdyktu

Pozycja, której gramatyka nie ma, zdania nie odrzuca:
wypuszcza je jednym czytaniem, czyli wybiera przez przeoczenie.
Wywód wraz z listą takich pozycji i z ceną nad Składnicą trzyma
[subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
Zostaje do tego dopisać kierunek, w którym ta pomyłka idzie,
bo on mówi, ile ona waży.

Zawężanie liczby czytań ma tu właścicieli wyłożonych i jednego niewyłożonego.
`admissible` w `olski/subset.py` odbiera czytanie, którego polszczyzna nie ma,
warunek na [zaimek rzeczowny](subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)
odbiera grupie imiennej drugie czytanie tego samego kształtu,
a `signature` w `olski/parse.py` liczy dwa wyprowadzenia jako jedno czytanie.
Każde z tych trzech jest pojedynczą decyzją z wywodem i z ceną:
pierwsze wykłada [kryterium słownikowe](subset.md#the-dictionary-offers-readings-polish-does-not),
a ostatnie jest czterema wierszami, które
[sekcja Checks](../CLAUDE.md#checks) wymienia z nazwy właśnie dlatego,
że ruszają każdy werdykt.
Lista ciał zawęża przez to, czego w niej nie ma,
i tym się od tamtych różni: rośnie z każdą konstrukcją,
nie ma jednego miejsca, w którym da się o nią spierać, i nie mierzy jej nic.

Reszta tej drogi myli się w drugą stronę i dlatego nie waży tyle samo.
Lemat, którego leksykon nie wymienia, dostaje ramę domyślną, czyli szerszą,
a cecha, której forma nie niesie, jest przez `unify` pomijana:
jedno i drugie dokłada czytania, więc zdanie wychodzi wieloznaczne,
a wieloznaczność jest werdyktem, który ktoś przeczyta.
`valid` czyta się inaczej, bo po niego ten tor jest.

Warunki precedencji zabierają z tej listy pozycję ostatnią,
bo miejsce zadeklarowane raz nie ma jak zostać zapomniane w jednym z ciał.
Wyceny ruchu to nie jest — tę robi liczba deklaracji zmierzona
[sondą](#podłoże-więzowe-zmierzone-sondą) —
tylko to, co się przy nim kupuje poza nią.

## Angle two: skład

Generation inverts every difficulty in parsing.

Ambiguity is the parser's curse;
a generator never encounters it.
Agreement stops being a constraint to check
and becomes a value to compute.
Parsing `czarnego kota` means reconciling two syncretic feature bundles.
Generating it means calling `inflect(kot, acc.sg.m2)`
and getting one answer.

### Three architectures

**Correct by construction.**
The source is a typed abstract syntax tree,
with types encoding what agrees with what.
Ill-formed input fails to typecheck;
well-formed input compiles to text and cannot be wrong.
Strongest guarantee, worst ergonomics:
nobody wants to author prose as an AST.

**Write near-Polish and check it.**
The source looks like Polish and is parsed and validated.
Best ergonomics,
and it inherits every problem from the parsing angle,
plus the fact that chart parsers give famously bad error messages.
`parse failed at token 7` is not explainable.

**An unambiguous surface DSL.**
The source reads like Polish
but is designed to be parsed by something boring and deterministic,
because the notation is ours to control.
Lemmas plus explicit structural marks;
the compiler elaborates to an AST,
resolves agreement,
and linearizes.
Something in the spirit of:

```text
(zdanie
  podmiot: kot[m2]
  orzeczenie: widzieć[past]
  dopełnienie: mysz[pl])
→ Kot widział myszy.
```

The third option is the working preference among these three,
and the predictive-editor finding below partly rehabilitates the second.

What is built is none of them but a fourth,
because all three describe the sentence
where the fourth describes what the sentence is about,
and the ergonomic objection to the first therefore misses it:
[Czwarta architektura](#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
owns it.

### The predictive editor changes this

The controlled-language literature has a standard answer
to both the bad-diagnostics problem
and the habitability problem,
and it is not better error messages.
It is a **look-ahead editor**:
show the author, at each position,
which words and phrases the grammar permits next.
Then invalid text cannot be written,
so there is nothing to diagnose.

AceWiki does this for Attempto Controlled English.
For olski it would mean the checker's primary interface
is not a batch validator over a file
but an incremental one over a cursor position.
That is a substantially different program,
and it is the strongest argument found so far
for the second architecture over the third.

See [similar-work.md](similar-work.md#the-habitability-problem).

### Czwarta architektura: poziom dziedziny, a nie poziom języka

Trzy powyższe stoją na poziomie rozbioru zdania albo niżej,
i pierwsza z nich została odrzucona dokładnie za to:
prozy nikt nie chce pisać drzewem rozbioru.
Czwarta bierze drzewo, którego kategorie nie są kategoriami polszczyzny,
tylko kategoriami tego, o czym się mówi,
i zarzut wobec pierwszej jej nie dosięga.

Ten poziom jest tym, co Grammatical Framework nazywa składnią abstrakcyjną,
i tym, co ma się od niej wziąć.
Konstruktor mówi, że jedna rzecz jest określeniem drugiej,
a nie że stoi tam dopełniacz;
że czegoś jest wiele, a nie że rzeczownik ma liczbę mnogą.
Przypadek, rodzaj i formę liczy linearyzacja,
bo żadne z nich nie jest rzeczą, którą autor chce powiedzieć:
przypadek bierze się z pozycji, a rodzaj rzeczownika z leksykonu.

Jednoznaczności ten zapis nie musi sprawdzać, bo ją ma:
drzewo dobrze złożone jest jednoznaczne z definicji.
To zdejmuje przy okazji wieloznaczność, której sam worek słów nie odróżnia,
a która nad polszczyzną jest zwyczajna:
`parser podzbioru` i `podzbiór parsera` są dwoma różnymi drzewami,
choć stoją w nich te same lematy w tych samych rolach.

Buduje to `skład/`, a `skład/składnia.py` trzyma kategorie i konstruktory.
Zgodność jest tam liczona, a nie sprawdzana,
więc gramatyki podzbioru ten kierunek nie potrzebuje
([niżej](#the-round-trip-invariant)).

Szyk to drzewo niesie, ale niesie go na jednym poziomie z dwóch.
Polszczyzna niesie szykiem temat i remat,
więc `Wejściem jest zwykły tekst polski.` i `Zwykły tekst polski jest wejściem.`
mówią to samo zdanie logiczne i co innego stawiają na czele,
a `Wyróżnienie` jest tą kategorią, z której oba wychodzą.
Kolejność słów jest z niej wnioskiem, a nie wariantem dopisanym do linearyzacji:
czasownik zostaje na miejscu, a przestawia się to, co stoi wokół niego.
Wewnątrz grupy imiennej takiej kategorii nie ma i jest to brak, a nie decyzja:
przymiotnik przed rzeczownikiem określa, a po rzeczowniku nazywa,
i dlatego README pisze `zwykły tekst polski`,
a kompilator z tego samego drzewa wypuszcza `zwykły polski tekst`.
Języki o szyku ustalonym tego wyboru nie mają,
więc biblioteka wzięta od kogoś, kto go nie miał, nie odpowie za nas.
Co ma go rozstrzygać wewnątrz grupy, nie zapadło, i trzyma to [`TODO.md`](../TODO.md).

### Tekst wie to, czego zdanie o sobie nie wie

Zdanie skompilowane osobno wypisuje każdą rzecz pełną nazwą
i stawia ją w czasie, w którym stoi samo.
Tekst wie dwie rzeczy więcej i obie zmieniają to, co wychodzi,
więc `skład.opowieść` stoi nad `skład.składnia`, a nie obok.

Pierwszą jest czas.
Opowieść mówi o tym, co się stało, i mówi tak o wszystkich swoich zdarzeniach,
więc czas przeszły jest własnością opowiadania, a nie któregokolwiek z nich.
To samo drzewo opowiedziane jako to, co się dzieje, dałoby czas teraźniejszy,
i dlatego czasu nie ma w drzewie, tylko w kontekście, w którym drzewo się wypisuje.

Drugą jest tożsamość.
Podmiot powtarzany zdanie po zdaniu czyta się źle,
a polszczyzna ma na to sposób zwykły i tani: opuszcza go,
bo osobę, liczbę i rodzaj niesie sam czasownik.
Żeby go opuścić, trzeba wiedzieć, że dwa wystąpienia lematu są tą samą rzeczą,
a tego jedno drzewo nie ma czym powiedzieć.
Niesie to `Postać`, a rozstrzyga o tym zmienna, którą jej nadano:
dwa razy napisany `R.bazyliszek` jest dwoma bazyliszkami,
a dwa razy użyta jedna `Postać` jest jednym.
Tożsamość jest więc deklaracją autora, a nie wnioskiem ze słownika synonimów,
i widać to w tej samej opowieści na drugim określeniu:
`bazyliszek` i `potwór` są dla tego kompilatora dwiema rzeczami.

Opuszczenie jest wąskie i jest wąskie z tego samego powodu,
dla którego po drugiej stronie stoi kryterium jednego czytania:
opuszczenie, po którym zdanie czyta się dwojako, nie jest oszczędnością.
Warunki trzyma `pomijalny` w `skład/składnia.py`,
a nie akapit, bo o to samo pyta ciąg zdarzeń wewnątrz jednego zdania,
i jeden z nich jest tu wart powtórzenia,
bo mówi, czym ta ostrożność się mierzy.
Po opuszczonym podmiocie zostaje forma czasownika i nic poza nią,
więc podmiot wraca stamtąd tylko wtedy,
gdy nikt inny tej samej formy z tego czasownika nie wyciąga.
Kufer stojący w piwnicy nie odbiera córce krawca niczego, bo rodzaj ma inny,
a skrzynia odbiera jej rodzaj żeński i wtedy podmiot staje wypisany.
Liczy się to tym czasownikiem, który podmiotu nie wypisze,
bo różnice, których on nie robi, nie są różnicami dla czytelnika:
czas przeszły rozdziela rodzaje, a teraźniejszy nie rozdziela żadnego.

### Zdanie podrzędne jest tu wskazaniem rzeczy

Podrzędność jest miejscem, w którym ten zapis mógł rozjechać się
z poziomem, na którym stoi.
Zdanie w zdaniu jest kategorią składni, a nie dziedziny,
i kategoria o takiej nazwie ściągnęłaby cały ten tor
na trzecią architekturę [powyżej](#three-architectures),
czyli na rozbiór zdania pisany z góry.

Kategorią, która z tego wyszła, jest wskazywanie.
`Jaki` wskazuje rzecz cechą, `Opis` w `skład/składnia.py` wskazuje ją zdarzeniem,
a pytanie jest w obu wypadkach jedno i jest pytaniem o rzecz:
o którą z nich mowa.
`kamienne postaci` i `kamienne postaci, których nikt nie liczył`
wskazują więc tak samo i różnią się tym, czym wskazują,
a nie tym, że do drugiego doczepiono zdanie.
Że wychodzi z tego przydawka zdaniowa wraz z zaimkiem względnym i dwoma przecinkami,
rozstrzyga linearyzacja, tak samo jak rozstrzyga przypadek.

Miejsce, które w zdaniu podrzędnym zostaje zaimkiem, nie jest zapisane.
Autor pisze rzecz raz i stawia tę samą zmienną w zdaniu, które ją wskazuje,
czyli robi to, co robi z `Postać` [powyżej](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie):
tam ta sama zmienna dwa razy jest jedną rzeczą w dwóch zdaniach,
a tutaj jest jedną rzeczą w zdaniu nadrzędnym i podrzędnym naraz.
Mechanizm jest ten sam co przy opuszczaniu podmiotu i stoi w jednym miejscu:
`Kontekst` niesie to, czego wypisywane drzewo o sobie nie wie,
a jedna funkcja rozstrzyga, czy rola wychodzi nazwą, czy zaimkiem.

Co ta kategoria kupuje poza rytmem, widać na przypadku tego zaimka.
`których nikt nie liczył` stoi w dopełniaczu,
bo w zdaniu podrzędnym stoi na pozycji dopełnienia czasownika zaprzeczonego,
a rodzaj i liczbę bierze z rzeczy, która stoi w zdaniu nadrzędnym.
Dopełniacz negacji sięga więc zaimka tak samo, jak sięgnąłby rzeczy postawionej tam,
i nie ma na to w kompilatorze osobnej gałęzi.
Autor nie pisze przy tym ani przypadka, ani rodzaju, ani zaimka,
ani tego, że zdanie podrzędne otwiera się nim niezależnie od roli, którą on w nim ma.

Reszta zdania złożonego wychodzi z dwóch innych kategorii:
[okoliczności wyrażonej zdarzeniem](#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie)
oraz [następstwa](#następstwo-zdarzeń-jest-kategorią-a-spójnik-jego-wnioskiem).

Jedna granica leży przy tym w środku samej kategorii.
Wskazana rzecz musi stać w zdaniu podrzędnym na pozycji, z której wyjdzie na czoło,
czyli sama albo pod przyimkiem, a nie pod grupą imienną,
więc `kot, którego ogon goni mysz` jest zdaniem polskim, którego stąd nie ma.
Zgłasza się ono przy budowaniu drzewa, i to jest tu jedyna obrona,
bo zaimek zostawiony w środku zdania podrzędnego wyszedłby tekstem,
którego nikt nie chciał napisać.

### Okoliczność nie pyta, czy stoi pod nią rzecz, czy zdarzenie

Podrzędność, która rzeczy nie wskazuje, dochodzi do tego zapisu
kategorią, którą on już ma, a nie kategorią nową.
Okolicznik niesie relację i to, co pod nią stoi,
a stanąć może rzecz albo zdarzenie, bo pytanie stawia się jedno:
`w nocy` i `gdy zgasła świeca` odpowiadają, kiedy.

Różnica między nimi jest różnicą w polszczyźnie, a nie w drzewie,
i cała siedzi w słowie, którym relacja wychodzi na wierzch.
Przed rzeczą stoi przyimek, który rządzi przypadkiem,
i bierze go z `skład/przyimki.py`;
przed zdarzeniem stoi spójnik, który nie rządzi niczym,
bo zdanie podrzędne rozdaje przypadki własne,
więc `skład/spójniki.py` mówi o nim mniej: to, w jakiej stoi relacji.
Tyle jednak wystarcza, żeby `Kiedy.bo` się zgłosiło,
i jest to ta sama odmowa, którą tamten plik wydaje na `Skąd.do`.
Świadka ten leksykon ma przy tym pełniejszego niż tamten:
SGJP odróżnia spójnik podrzędny od współrzędnego,
więc `i` dopisane do tej tabeli zgłasza się w teście, a nie w tekście.

Skutek jest w tym leksykonie odwrotnością przyczyny i mówi to samo,
a różni się tym, przy którym zdarzeniu stoi:
`bo` wprowadza zdanie o tym, skąd się wzięło to, przy czym stoi,
a `więc` zdanie o tym, co z niego wyszło.
Wybór między nimi jest wyborem głowy i widać go w tekście,
bo głowa wypada pierwsza:
`Wzrok potwora zamieniał ludzi w kamień, więc mieszczanie zabili okna deskami.`
opowiada zdarzenia w kolejności, w której zaszły, a to samo napisane przez `bo`
opowiada je od końca.
Nazwy pytania ta relacja przy tym nie ma i nazywa się relacją,
bo polszczyzna pytania o skutek jednym słowem nie ma;
tyle jest w tej konwencji nazw, ile jest w niej pytań.

Wysunięcie takiej okoliczności na czoło jest zwykłym `Wyróżnienie`,
więc `Gdy bazyliszek otworzył oczy, czeladnik zasłonił twarz lustrem.`
i to samo zdanie z okolicznością na końcu
są jednym drzewem z jednym znacznikiem różnicy,
a nie dwoma wariantami linearyzacji.
Wysunąć się jednak nie da wszystkiego i rozstrzyga o tym leksykon,
bo jest to fakt o słowie:
`Ponieważ zgasła świeca, córka krawca nie wróciła.` jest zdaniem polskim,
a to samo zdanie z `bo` na czele nie jest,
choć oba te spójniki stoją w jednej relacji.
Jest to jedyne miejsce w tym pakiecie, w którym leksykon mówi o kolejności,
i jedyna jego kolumna bez świadka w słowniku,
bo SGJP nie odróżnia tych dwóch słów niczym.

Przecinek zaś jest przez to własnością konstytuenta, a nie znakiem w napisie.
Zdanie podrzędne oddziela się nim z każdej strony, przy której coś stoi,
więc konstytuent nie wie o swoich przecinkach tego, co o nich rozstrzyga,
i wiedzieć nie może: rozstrzyga o nich sąsiad.
`linearyzuj` zwraca przez to `Kawałek`, czyli napis wraz z żądaniami,
a jedna funkcja te żądania spełnia i stawia jeden przecinek tam,
gdzie dwóch sąsiadów zażądało go naraz.
Krańce zdania nie spełniają żadnego, i to zdejmuje dwa warunki:
kropka nie staje po przecinku, a lista nie dostaje dwóch.
Bez tego pola przecinek jedzie w napisie, a każde miejsce,
które po konstytuencie coś stawia — a jest ich trzy — czyta go z ogona tego napisu.

### Następstwo zdarzeń jest kategorią, a spójnik jego wnioskiem

`Ciąg` w `skład/składnia.py` bierze kilka zdarzeń i wypuszcza jedno zdanie,
a kategorią dziedziny jest w nim następstwo:
jedno stało się po drugim i jest to jedna rzecz do opowiedzenia.
Węższe to jest niż polskie `i`, które łączy także zdarzenia równoczesne,
i węższe z rozmysłu, bo kolejność zdarzeń niesie tu kolejność zapisu.

Koordynacją bytów piętro wyżej to nie jest,
i widać to na tym, czego żąda opuszczenie podmiotu.
Byty stoją w jednej roli i żaden nie ma czasownika,
a zdarzenia mają go po jednym, więc drugie z nich podmiotu nie powtarza.
Rozstrzyga o tym ten sam `pomijalny`,
który rozstrzyga o tym [między zdaniami](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie),
bo pytanie jest jedno: czy czytelnik odzyska podmiot, którego nie ma.
Wspólna zostaje im interpunkcja, bo listę obie piszą tak samo,
i stoi ona w jednym miejscu z tego właśnie powodu.

### Najpierw tekst, potem drzewo, na końcu biblioteka

Kolejność, w której powstał `opowieści/bazyliszek.py`, była odwrotna do zwykłej.
Najpierw stanął polski tekst, który miał wyjść,
potem drzewa, z których miał wyjść, a dopiero po nich to,
czego tym drzewom w bibliotece brakowało.
Kolejka konstrukcji wzięła się więc z tekstu, a nie z listy spisanej z góry,
i wyszło z niej co innego, niż wyszłoby z README:
opowieść żąda czasu przeszłego, przeczenia i okoliczników miejsca,
a README, które stoi w czasie teraźniejszym, nie żąda żadnej z tych rzeczy.

Kosztu ta kolejność ma tyle, że tekst wybrany pod kompilator
mówi o kompilatorze mniej niż tekst, którego nikt pod niego nie pisał,
i dlatego kryterium wyjścia toru zostaje przy README
([roadmap.md](roadmap.md#kryterium-wyjścia-toru-składu-to-znów-readme)).
Zysk jest za to natychmiastowy:
tekst napisany pod jedną legendę mieści się w jednym pliku i w jednej sesji,
a każda rzecz, której z niego nie dało się wypuścić,
jest brakiem pokazanym na zdaniu zamiast wyliczonym w planie.

### Lepszy tekst żąda czego innego niż dłuższy

Ta legenda przechodzi ten cykl kilka razy i za każdym nie po to,
żeby stanęło w niej więcej zdań,
tylko po to, żeby była opowieścią, a nie ciągiem zdań o jednym temacie.
Kolejkę ustawia więc to, czego opowieści brakuje jako opowieści,
i wychodzi z tego co innego, niż wyszłoby z listy konstrukcji.
Pierwszym takim żądaniem jest zakończenie, które nie mówi, o czym opowieść była,
i to żądanie stoi w [fiction.md](fiction.md#narrative) wprost,
razem z drugim, które to samo zakończenie spełnia: nie wypada ono dobrze.
Obok niego stoi powód, dla którego ktoś schodzi do piwnicy,
a ten jest rozstrzygnięciem tej opowieści, a nie pozycją z tamtego katalogu.
Najbliżej stoi tam [płaskie wnętrze postaci](fiction.md#scene-and-character),
czyli usterka o tym, czego postać nie ma, a nie o tym, czego nie robi.

Oba prowadzą do jednego, i to jest tu ustalenie:
powód i puenta, która nie podsumowuje, żądają zdania podrzędnego.
Zdanie, które nie streszcza, musi coś pokazać,
a rzecz pokazana bez podsumowania jest rzeczą, którą trzeba wskazać,
i tego jedno zdanie proste nie robi.
Wyszedł z tego `Opis` [powyżej](#zdanie-podrzędne-jest-tu-wskazaniem-rzeczy),
czyli kategoria dziedziny w miejscu, w którym
[roadmap.md](roadmap.md#etap-5-konstrukcje-których-żąda-readme) trzymała podrzędność,
i pokrywa on z niej tyle, ile podrzędność wskazuje rzecz, a nie więcej.

Drugie ustalenie jest ciekawsze, bo kolejka nie została w tej warstwie.
Zaimek względny wychodził z morfologii jako `któren`,
czyli forma, którą SGJP odsyła do gwary,
więc nowa konstrukcja składniowa zażądała kryterium wyboru formy,
stojącego pod nią o dwie warstwy niżej
([kwalifikator](#kwalifikator-mówi-o-formie-dwie-rzeczy-i-tylko-jedna-jest-rejestrem)).
Plan tego tak nie ustawia i nie ma jak ustawić:
roadmapa trzyma wybór formy jako etap 3, a podrzędność jako część etapu 5,
i wywód za tą kolejnością się nie zmienia.
Tekst nie czyta jednak numeracji i płaci od razu za wszystko,
czego wymaga zdanie, które ma z niego wyjść.

Trzecie żądanie jest o rytm i stoi w tamtym katalogu wprost.
[Jednostajność](fiction.md#sentence-and-paragraph) — zdania jednej długości,
jeden kształt zdania powtórzony przez cały tekst — jest tam usterką wymienianą
jako właściwość prozy modelowej, a opowieść złożona z samych zdań prostych ma ją całą.
Zdanie długie nie powstaje jednak z dwóch krótkich postawionych obok siebie:
potrzebne jest to, co je łączy, i stąd wzięły się
[następstwo](#następstwo-zdarzeń-jest-kategorią-a-spójnik-jego-wnioskiem)
wraz z [okolicznością wyrażoną zdarzeniem](#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie).
Bez nich `Podniosła deskę i zeszła po schodach.` rozpada się na dwa zdania,
a przyczyna, którą niesie `bo`, zostaje czytelnikowi do wyciągnięcia
z dwóch zdań postawionych obok siebie i niepołączonych niczym.

Czwarte przyszło stamtąd, gdzie pierwsze: z warstwy pod tą, którą się ruszało.
Zdanie podrzędne wstawia przed podmiot cudzy podmiot,
więc `Gdy bazyliszek otworzył oczy, zasłonił twarz lustrem.`
mówi, że twarz zasłonił bazyliszek.
Ten sam podmiot w zdaniu obok jako jedyny warunek nie wystarcza,
i pokazuje to zdanie złożone, choć nie jest to warunek o zdaniu złożonym.
Warunek, który stoi tam zamiast niego, mierzy to, co po opuszczonym podmiocie zostaje,
czyli formę czasownika ([wyżej](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)),
i sięga tak samo zdania obok:
skrzynia postawiona w piwnicy zamiast kufra odbiera córce krawca opuszczenie,
choć stoi w zdaniu podrzędnym, którego opowieść jest o czym innym.

Ostatnie jest po prostu tanie.
Trzy relacje okolicznikowe dopisały się bez namysłu,
bo `w nocy`, `po schodach` i `wśród kamiennych postaci` są tym,
czym opowieść odmierza czas i ruch, a nie nową kategorią.
Jedna z nich niesie przy tym coś poza sobą:
`w nocy` stoi w tym samym przypadku co `w piwnicy`,
więc jest wpisem, po którym w tekście nie zmienia się nic,
i pokazuje, że relacja nazywa to, co autor powiedział,
a nie to, w czym mu to wyjdzie.

### Checks that are cheap, deterministic, and explainable

All finite-domain, all effectively linear time,
all able to say why they failed:

- Noun-phrase-internal agreement,
  adjective and determiner against noun,
  on case, number, and gender
- Subject-verb agreement on person and number,
  and on gender in the past tense and conditional
- Verbal government:
  `używać` demands genitive,
  so `używam komputera` and not `używam komputer`
- Prepositional government,
  each preposition licensing a fixed set of cases
- Genitive of negation,
  applied as a rewrite during linearization
  so that it is automatic rather than checked
- Aspect and tense legality:
  `będę zrobił` is unconstructible,
  and perfective present is future
- Gender resolution under coordination:
  `Jan i Maria przyszli`, never `przyszły`
- Clitic and `się` placement

Every failure should report two feature bundles and their provenance,
along the lines of
*`czarna` is nom.sg.f, `kota` is acc.sg.m2,
mismatch on case and gender, from lines 3 and 4*.
That is a diagnostic a human can act on,
and it is the thing a language model structurally cannot provide:
it cannot say which rule fired,
and it will not give the same answer twice.

### Morphology generation is the underestimated piece

Analysis maps a form to tags.
Generation maps a lemma plus tags to a form.
The compiler needs the second,
and Polish inflection carries enough irregularity,
stem alternation,
and paradigm classes
that hand-writing it is a multi-year detour.

Morfeusz 2 exposes generation over SGJP,
whose 2020 edition characterizes nearly 456,000 Polish lexemes,
and both are distributed under a liberal BSD licence.
That one dependency is the difference
between a weekend-scale core and a years-scale one,
which is why the open lexicon is a settled decision.

### Leksykon projektu: SGJP nie zna słów, których używa rejestr

Słownik pod spodem nie zastępuje pisania w dwóch miejscach.
Nie ma słów, które rejestr techniczny tworzy sam — `komit`, `olski`, `lintować`
dostają `ign`, czyli nie mają czego wypuścić.
I nie ma leksemów, które ten rejestr dokłada do napisów znanych:
projekt piszący o agentach jako o programach żąda liczby mnogiej `agenty`,
a `agenty`, które SGJP wydaje, jest formą deprecjatywną leksemu osobowego,
czyli tym, czym mówi się o ludziach z góry, a nie liczbą mnogą rzeczy nieżywotnej.
Wpis takiego leksykonu nazywa więc leksem wraz z odmianą,
a nie sam napis dopisany do listy słów.

Rozróżnianie leksemów jest przy tym pytaniem, które słownik już zadaje
i na które sam odpowiada wszędzie tam, gdzie leksemy rozdzielił.
`zamek:Sm3~a` i `zamek:Sm3~u` to dwa leksemy różniące się dopełniaczem,
a `Włochy:Sn_pt~szech` i `Włochy:Sn_pt~chach` to kraj i dzielnica Warszawy,
różniące się miejscownikiem.
Ten identyfikator czyta jeden kierunek:
synteza pyta o niego przez `skład/leksemy.py`
([niżej](#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)),
a `olski/morph.py` ucina go przy analizie.
Kwalifikator słownik niesie tym samym polem, a czyta go jeden kierunek:
`POZA_REJESTREM` w `skład/morfologia.py` odsiewa nim formy przed syntezą,
a analiza wyrzuca go razem z resztą pól,
więc `projekta` oznaczone jako `daw.` ze składu nie wyjdzie, a do parsera wejdzie.
Brak słowa, rozdzielony leksem i przeczytany kwalifikator
widać naraz, nad `pl.sgjp.sgjp-2026.06.01`:

```sh
python3 -c "
import morfeusz2
morf = morfeusz2.Morfeusz()
for lemat in ('projekt', 'zamek', 'komit'):
    for forma, leksem, tag, _, kwalifikatory in morf.generate(lemat):
        if 'pl:nom' in tag or 'sg:gen' in tag or tag == 'ign':
            print(forma, leksem, tag, kwalifikatory)
"
```

Leksykon projektu jest plikiem, który czyta to repozytorium,
a nie słownikiem dołożonym Morfeuszowi, i decyduje o tym cena wejścia.
Morfeusz przyjmuje słownik własny przez `dict_path`,
ale przyjmuje go skompilowanego,
a pakiet z PyPI wydaje bibliotekę wraz z wiązaniem do Pythona i nic poza tym,
co widać po zawartości katalogu, w który się instaluje,
więc tamta droga żąda łańcucha narzędzi spoza PyPI
i zabiera to, co [`CLAUDE.md`](../CLAUDE.md#checks) ma za instalację jednym poleceniem.
Plik czytany przez oba kierunki kupuje przy tym to samo,
co kupuje [leksykon walencyjny](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej):
że `komit` jest słowem raz, a nie dwa razy.

Czym wpis ma być, nie zapadło.
Wypisanie form kosztuje pisanie i nie ma jak się pomylić;
wskazanie leksemu, wedle którego wpis się odmienia,
kosztuje jedno pole i łamie się tam, gdzie temat alternuje,
bo `plik` ma w miejscowniku `pliku`, a temat zakończony na `t` bierze tam `cie`.
Trzyma to [`TODO.md`](../TODO.md).

### Kwalifikator mówi o formie dwie rzeczy i tylko jedna jest rejestrem

Kwalifikator jest jedynym kryterium wyboru formy,
które w danych stoi gotowe i nie żąda niczego poza przestaniem go wyrzucać.
Co za tym stoi, widać na dwóch słowach, których obu żąda opowieść o bazyliszku,
i widać na nich od razu, że kryterium nie jest jedno.

Bez odsiania wychodzi polszczyzna, której nikt nie pisze.
Zaimek względny rodzaju męskiego wychodził jako `któren`,
oznaczone w SGJP jako `daw._dziś_gwar.`,
a przeszła forma `zgasnąć` jako `zgasnęła`, oznaczone jako `rzad.`
Obie stoją w słowniku przed formą zwykłą,
więc kompilator brał je nie dlatego, że coś rozstrzygnął, tylko dlatego, że nie pytał.

Po odsianiu każdego kwalifikatora naraz wychodzi polszczyzna o innym znaczeniu.
SGJP rozdziela `oko` na dwa leksemy i temu o liczbie mnogiej `oczy`
daje kwalifikator `anat.`, a temu o liczbie mnogiej `oka` nie daje żadnego,
więc kryterium bez podziału zamieniłoby zdanie legendy
`Bazyliszek otworzył oczy.` na `Bazyliszek otworzył oka.`,
czyli na oczka w sieci albo w rosole.
Nazwa dziedziny nie odsyła tu formy poza rejestr, tylko mówi, w którym znaczeniu
leksem tak się odmienia, i jest to zupełnie inne zdanie o tej samej formie.

Podział jest więc rozstrzygnięciem, a nie odczytem, i stoi w `POZA_REJESTREM`.
Nazwy, które w słowniku występują, wypisuje polecenie
nad listą lematów, którą to repozytorium już ma:

```sh
python3 -c "
import collections, morfeusz2
morf = morfeusz2.Morfeusz(generate=True, expand_tags=False)
lematy = [w.split()[0] for w in open('olski/leksykon.txt') if not w.startswith('#')]
nazwy = collections.Counter(
    nazwa
    for lemat in lematy
    for *_, kwalifikatory in morf.generate(lemat)
    for napis in kwalifikatory
    for nazwa in napis.split(',')
)
for nazwa, ile in nazwy.most_common():
    print(ile, nazwa)
"
```

Zasięg tego polecenia jest zasięgiem tamtej listy, czyli czasownikami,
i to jest jedyna słabość tego wywodu:
`anat.`, `mors.` oraz `daw._dziś_gwar.` wychodzą dopiero na rzeczownikach,
więc lista nazw jest sumą dwóch przebiegów, a nie wyjściem jednego polecenia.
Nazwa, której żaden przebieg nie pokazał, przechodzi jak nazwa dziedziny,
i to ten podział kosztuje.
Odwrotny domyślny kosztowałby więcej, bo formę odsianą przez pomyłkę
widać dopiero wtedy, gdy jej brak wywali całą komórkę paradygmatu.

### Nazwę leksemu wybiera autor, bo lemat go nie wskazuje

Kwalifikator jest kryterium, które w danych stoi gotowe.
Leksem jest kryterium, którego w danych nie ma:
identyfikator słownik niesie, a które z dwóch znaczeń autor miał na myśli,
mówi tylko autor.

Że wybiera go autor, a nie cecha, widać na dwóch parach naraz.
`oko` rozdziela się na leksem zbiorowy i niezbiorowy,
a różnicę tę niesie tag, bo `oczy` mają cechę `col`, a `oka` `ncol`,
więc dałoby się je rozróżnić żądaniem cechy, tak jak żąda się przypadka.
`Włochy` rozdzielają się na kraj i dzielnicę Warszawy,
a tag obu jest w miejscowniku ten sam, `subst:pl:loc:n:pt`,
i różni je wyłącznie identyfikator.
Kryterium cechowe pokryłoby więc pierwszą parę i nie tknęłoby drugiej,
a leksem pokrywa obie.

Drugą połową ustalenia jest to, że w drzewie stoi nazwa, a nie identyfikator.
Poziomem kategorii tego pakietu jest
[dziedzina](#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka),
a kod paradygmatu jest napisem z wnętrza słownika innego projektu,
więc drzewo pisze `R.oko_w_rosole`,
a z identyfikatorem wiąże tę nazwę `skład/leksemy.py`.
Wiązanie jest wiele do jednego z założenia:
oczko w sieci i oko w rosole to jeden leksem i dwie rzeczy, o których się pisze,
więc nazw jest tyle, ile rzeczy, a nie tyle, ile leksemów.
Nazwa goła jest wpisem tego samego rodzaju:
`oko` znaczy w tym repozytorium oko, a nie oczko,
i tyle wystarcza, żeby legenda otwierała bazyliszkowi oczy
bez wpisu przy każdym użyciu.

Kiedy wpis jest potrzebny, rozstrzyga zgoda leksemów, a nie ich liczba.
`dziób` ma dwa leksemy, z których jeden słownik odsyła do żeglarstwa,
i oba mają w dopełniaczu `dzioba`,
więc pytanie o dopełniacz ma odpowiedź, pod którą oba podpisują się naraz.
`oko` w liczbie mnogiej odpowiedzi wspólnej nie ma,
i wtedy `odmień` zgłasza `WieleLeksemów` wraz z formami, które z każdego wychodzą,
bo autor rozstrzyga między znaczeniami i widzi je po tym, co z nich wyjdzie.

Najdroższy przypadek nie jest przy tym rzeczownikiem:
`stać` ma leksem niedokonany i dokonany,
a forma dokonana w czasie teraźniejszym jest w polszczyźnie przyszła,
więc milczenie wypuszczałoby stąd zdanie o tym, co będzie,
zamiast zdania o tym, co jest.

Tym samym kryterium schodzi rodzaj, który jest wartością, a nie formą:
`potwór` ma leksem zwierzęcy oraz osobowo-zwierzęcy,
więc zwierzę jest tym, pod czym podpisują się oba,
a wybór alfabetyczny dałby tu osobę.

Ceną tego kryterium jest cisza w miejscu, o które nikt nie pytał:
leksemy różniące się poza żądaną komórką przechodzą bez zgłoszenia,
bo pytanie brzmi „która forma”, a nie „który leksem”.
Otwarte zostaje to, na co to kryterium nie sięga,
i jest to słownik mówiący „albo tak, albo tak” pod jednym leksemem:
`postaci` obok `postacie` w jednej komórce
oraz `anioł` z rodzajem wypisanym dwiema wartościami w jednym tagu.
Identyfikator nie rozstrzyga ani jednego, ani drugiego, i trzyma to
[`TODO.md`](../TODO.md).

Leksykon ten jest przy tym innym plikiem niż
[leksykon projektu](#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr),
bo odpowiada na inne pytanie:
tamten dokłada leksem, którego słownik nie ma, a ten wybiera z tych, które ma.

Po stronie analizy nie zmienia się nic i jest to rozstrzygnięcie, a nie zaległość.
Identyfikatora nie potrzebuje tam nic:
`Rosół ma oka.` i `Bazyliszek ma oczy.` wyprowadzają się po jednym czytaniu,
a reguły o zbiorowość nie pytają.
Leksem wpuszczony do czytania sięgnąłby za to każdego szukania po lemacie,
czyli leksykonu walencyjnego i `KOPULA` w `olski/subset.py`,
i każde z nich musiałoby powiedzieć, którą połowę identyfikatora dopasowuje.
Wchodzi on tam wtedy, gdy będzie reguła, która tożsamości leksemu zażąda.
Kryterium, które po tamtej stronie już stoi, jest innego rodzaju i nie zastępuje tego:
[`admissible`](subset.md#the-dictionary-offers-readings-polish-does-not)
wyrzuca czytanie, którego polszczyzna nie ma,
a tutaj oba czytania polszczyzna ma i różnią się tym, o czym mówią.

## The round-trip invariant

This is the load-bearing idea,
and it is what keeps both angles alive.

**Generate text from a tree,
parse the result,
and check that the original tree comes back.**

A failure is either a generator bug
or a genuine ambiguity in olski's surface form,
and *olski contains a construction that cannot be read back unambiguously*
is a language design bug worth discovering.

The idea is not original.
Reversible grammars have a literature going back to the late 1980s,
and Grammatical Framework makes reversibility structural.
See [similar-work.md](similar-work.md#the-other-tradition-engineered-wide-coverage-grammars).

### Closeness to Polish weakens it

Strict round-tripping requires unambiguous surface forms,
which is exactly what closeness to Polish gives up.
The invariant therefore needs restating,
and the honest version is asymmetric:

**Tree to text is a function.
Text to tree is a relation.**

The test becomes membership:
the original tree must appear *somewhere* in the forest.
Reading count becomes a tracked metric rather than a failure condition.
That still catches real generator bugs,
and it stops the invariant from silently forbidding
the naturalness the project is aiming for.

It follows that the **lexicon** is one declarative source read in both
directions: what `używać` governs is a fact about a word,
and a second copy of it drifts.
[Walenty is that source](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej),
and `olski/walencja.py` is what each direction reads it through:
the parser turns it into the valency classes its productions need,
and `Robi` in `skład/składnia.py` asks it about the one lemma it was handed.
The two ask different questions of it, which is why what they share is the
lexicon rather than an answer.

The **grammar** is not, and binding the two costs more than it buys.
Generation never meets the problem the grammar exists to solve:
agreement stops being a constraint to reconcile and becomes a value to compute,
as the section above says,
so linearization needs no productions at all.
What it would inherit instead is the parser's coverage,
which over the [README](../README.md) is a handful of its sentences
([corpus.md](corpus.md#where-the-analyses-stop) counts them),
so a compiler restricted to the grammar could not produce that document.

So the parser stays a witness rather than a dependency.
Where a generated sentence happens to fall inside the subset,
the round trip tests it and reports whichever way it reads;
outside, it has nothing to say and the compiler is unaffected.
`tests/test_skład.py` uses it in exactly that posture.
The dependency also runs the other way than it first appears:
generation exposes what the grammar *over*generates,
which the parsing side sees only against a treebank.

## Known limits

**Grammaticality is not quality.**
A deeply nested stack of relative clauses
is exactly as well-formed as a clean sentence.
The checker will bless text no editor would accept.
That is fine,
as long as the claim stays where it belongs:
this checks syntactic correctness,
which is a real, useful, verifiable property,
and not the same thing as good Polish.

**Some correctness is usage, not structure.**
Collective numerals like `dwoje drzwi`,
the government of particular verbs,
which nouns take which prepositions:
none of that is derivable from rules.
It is lexicon.
The lexicon is therefore where the truth lives
and where the maintenance burden lands,
and it should be a first-class, reviewable, testable data file
rather than a hash map buried inside the parser.

**Rule-based language technology has a known labour profile.**
Rule-based machine translation declined
for coverage brittleness, per-language labour cost, and context-blindness.
Olski is not machine translation,
but it shares the labour profile,
and the only real mitigation is the one already chosen:
narrow the problem until hand-written rules suffice.

## The separable typographic layer

Independent of any grammar,
*skład* in the typesetting sense
has a pile of Polish rules
that are pure string manipulation and fully deterministic:

- A non-breaking space after single-letter words,
  so `w`, `z`, `i`, `a`, `o`, and `u` never end a line
- Polish quotation marks, „like this”
- The spacing of `nie`:
  separate from verbs, as in `nie ma`;
  joined to adjectives in the positive degree
  and to adjectival participles, as in `niedobry` and `niezrobiony`;
  separate from comparatives, as in `nie lepszy`
- Dash conventions and hyphenation points

This is testable, useful, and buildable
with no dependency on the grammar existing.

It is also the one part of this document
that survived the reframing unchanged,
because typographic rules are lint rules.
It ships as part of
[milestone 0](roadmap.md#milestone-0-rule-engine-and-the-typography-pack).

## Sources

- <https://sgjp.pl/o-slowniku/> — SGJP, about the dictionary
- <https://przewodnik.tmjp.pl/sgjp-2020-slownik-gramatyczny-jezyka-polskiego/> —
  the 2020 edition and its lexeme count
- <https://morfeusz.sgjp.pl/doc/about/> — Morfeusz, analysis and licensing
- <https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-9582.2005.00118.x> —
  Bošković on the locality of left branch extraction and the structure of NP
- <https://www.degruyterbrill.com/document/doi/10.1515/psicl-2017-0013/html?lang=en> —
  extraction facts and the internal structure of nominal constructions in Polish
- <https://www.ling.upenn.edu/~beatrice/syntax-textbook/lbe.html> —
  left branch extraction in Slavic, textbook summary
- <https://mdpi.com/1999-4893/9/3/58/htm> — LR parsing for LCFRS
