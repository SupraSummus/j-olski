# Design notes

Decisions that have been taken are marked as such;
everything still open lives in [open-questions.md](open-questions.md).
The target this grammar is grown towards is in
[roadmap.md](roadmap.md#celem-toru-jest-to-readme),
and the linter track that stood beside it, now retired,
is in [linter.md](linter.md#what-closed-the-track).
The other direction over the same subset —
a tree in, a Polish sentence out —
is in [sklad.md](sklad.md).

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
That is a narrower criterion than the retired linter's,
and the difference is deliberate.
A linter is judged against a corpus of real Polish
because its whole claim is about how Poles actually write,
and [not doing that](linter.md#the-thing-that-makes-or-breaks-it-calibration)
is what closed the track.
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
The retired linter track needed only analysis
and would have reached for Morfologik instead.
Two dictionaries for two jobs,
and only one of the two jobs is left.

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

What follows is the first direction.
The second has its own document, [sklad.md](sklad.md),
because what it decides is a level of description rather than a parser,
and nothing it settles is answerable from this one.

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

Proza README ma 45 zdań.
Wszystkie sonda rozbiera w budżecie 10 sekund na zdanie,
a każde poniżej dziesiątej części sekundy,
więc przebieg z takim budżetem kończy je tak samo —
i dlatego zamiast najwolniejszego czasu stoi tu próg,
bo zegar rusza się między przebiegami, a próg nie.
Ten sam werdykt i tę samą liczbę czytań dostają od obu programów 42 z nich,
a to drugie jest mocniejszym z dwóch odczytów:
werdykt zgadza się już wtedy, gdy jedna strona ma dwa czytania, a druga sześć,
a liczba nie, i `Koszt samej szynki przewyższa koszt szynki z dodatkami`
wychodzi po obu stronach dokładnie sześcioma —
co widać dopiero po `-c`, bo w README to zdanie stoi w bloku,
którego ekstrakcja nie wypuszcza.

Pozostałe trzy rozchodzą się na przecinku.
`Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego`
wychodzi w olskim dwoma czytaniami,
`Co ekstrakcja po drodze zmyśla, mówi docs/extraction.md` czterema,
`Czarna lista kupowała jednak co innego, niż obiecywała` jednym,
a sonda odrzuca wszystkie trzy, bo przecinka nie ma do czego przyłączyć.
Granica biegnie więc tam, gdzie olski bierze
[przecinek jako znak koordynacji](subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania),
a sonda po swojej stronie ma spójnik.

Ten pomiar mówi mniej, niż mówił, i nie dlatego, że któryś program się zmienił.
Zdanie, którego rozbiór zajmował ponad pięć sekund,
oraz dwa, o które oba programy się spierały,
stały w tej połowie README, którą zdjęło wycofanie toru linterowego,
a te dwa, które spór przywróciły, dopisała zmiana w tej samej prozie.
Trzecie dołożył czas przeszły, czyli tym razem zmiana w gramatyce,
i o tyle jest to spór mocniejszy od tamtych dwóch.
Tak właśnie kosztuje figura brana nad własną prozą,
przed czym [`CLAUDE.md`](../CLAUDE.md#checks) ostrzega,
a [`TODO.md`](../TODO.md) trzyma wpis o tym, co z tym zrobić.

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

**Earley was the boring recommendation and it is what `olski/parse.py` runs.**
It handles any CFG, including left recursion and nullable rules,
with no preprocessing;
it produces a shared packed parse forest natively;
its worst case is cubic but real grammars behave far better.
Decisively for a project whose grammar is still being designed:
the grammar can change without rebuilding an automaton.
GLR stays an optimization to reach for if measurement ever demands one,
and no measurement does:
a run over the whole of Składnica takes half a minute.

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

Werdykt wychodzi z lasu ze współdzielonymi węzłami, a nie z listy drzew,
i po co, widać na dwóch poleceniach:

```sh
python3 -m olski.check -c "Program zapisuje ustawienia w pliku w katalogu."
python3 -m olski.check -c "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci w firmie w kraju."
```

Każde doklejone wyrażenie przyimkowe podwaja liczbę czytań,
bo dochodzi do czasownika albo do rzeczownika przed nim,
a te wybory są od siebie niezależne.
Drugie z tych zdań ma więc sześćdziesiąt cztery czytania
i sześć nierozstrzygniętych decyzji, po jednej na wyrażenie,
a werdykt wypisuje sześć wierszy:
przyimek wraz z dwiema głowami, do których dochodzi.
Wierszy jest tyle, ile decyzji,
więc przybywa ich z długością zdania, a nie z liczbą czytań,
i o tę różnicę krotności szło.
Tę samą wielkość nazywa
[pytanie o czytelność prefiksu](open-questions.md#czy-jednoznaczność-prefiksu-mierzy-czytelność),
więc jedno pytanie i drugie stoją na tym samym prymitywie.
Liczba czytań jest przy tym liczbą, a nie napisem `64+`:
las podaje ją sumą po pozycjach korzenia,
i granica z `MAX_READINGS` sięga wypisywania drzew, a nie liczenia ich.

Lista czytań tego nie dowozi, i nie dowiozą jej dwie poprawki,
które wyglądają na tańsze wyjście:
streszczenie nazywające wszystkie węzły roli zamiast pierwszego,
wraz ze zdjętą granicą wyliczania.
Stoją tu zapisane, żeby nikt ich nie proponował drugi raz.
Streszczenie czytania nazywa pierwszy węzeł roli,
więc dwa czytania różne miejscem drugiego modyfikatora
wychodzą z niego jednym napisem,
a nazwanie wszystkich
daje nad drugim z tych zdań sześćdziesiąt cztery wiersze do porównania ręką:
wydruk rośnie wtedy wykładniczo,
a nazwać trzeba liczbę decyzji.

Trzecie tańsze wyjście brzmi najmocniej i mierzy się najgorzej:
zostawić enumerator i powiedzieć, że zdanie o więcej niż `MAX_READINGS` czytaniach
jest po prostu za wieloznaczne, żeby je czytać.
Werdykt „poddaję się” jest tu w porządku i nie o niego idzie.
Idzie o to, że enumerator zstępujący nie umiał go wydać tanio.
`analyses` w `olski/parse.py` przed tą zmianą (commit `9456a22`)
wyliczał pod pozycją każde wyprowadzenie, zanim oddał pierwsze,
więc granica ucinała wydruk, a nie pracę.
Zdanie ustawy o 28 042 czytaniach —
[najdłuższe z tego rejestru](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem) —
kosztowało go 76 s, żeby oddać sześćdziesiąt cztery drzewa i napis `64+`.
Las podaje nad nim liczbę dokładną w 0,05 s.
Sekundy zależą od maszyny, a krotność jest trzema rzędami wielkości,
i to o nią tu idzie.
Obie liczby bierze to samo polecenie,
raz nad plikiem z tamtego commita, a raz nad tym, który stoi:

```sh
git show 9456a22:olski/parse.py > /tmp/stary/parse.py
PYTHONPATH=/tmp/stary python3 -c 'import time, sys
from olski.subset import GRAMMAR, morphology
parse = __import__(sys.argv[1]).parse
s = morphology(open("zdanie.txt", encoding="utf-8").read().strip())
t = time.time(); w = parse(GRAMMAR, s)
print(len(w.readings), getattr(w, "ile", "—"), f"{time.time() - t:.2f}s")' parse
```

Enumerator pisany leniwie zmieściłby się w tej granicy,
bo urwałby wyliczanie na sześćdziesiątym czwartym drzewie,
i to jest jedyna uczciwa obrona tamtego wyjścia.
Liczby nie podałby przy tym żadnym kosztem,
a pamięć podręczna pod pozycją, czyli to, co go trzyma poniżej wykładniczej,
z leniwym wyliczaniem sama się nie składa.

Role, o które czytania się różnią, wychodzą z lasu tą samą drogą.
Streszczeń jest najwyżej `MAX_READINGS`,
więc rola, którą rozdziela dopiero sześćdziesiąte piąte czytanie,
nie zostałaby z nich nazwana,
a liczba obok niej granicy nie ma i tej niezgody po sobie nie pokazuje.
Tak stoi
[przepis o 28 042 czytaniach](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem):
werdykt nazywa tam dopełnienie, którego wypisane czytania nie rozdzielają.
Kosztuje to jedno rozstrzygnięcie, którego lista czytań nie potrzebuje.
Etykieta roli pada w jednym czytaniu kilka razy,
bo zdanie współrzędne ma własny podmiot,
więc nad lasem trzeba powiedzieć,
które pozycje jednej etykiety są tym samym wystąpieniem.
Jest nim to, które nazywa streszczenie, czyli pierwsze.

Gospodarza nazywa jego głowa, czyli jedno słowo.
`w Rzeczypospolitej Polskiej` dochodzi do `Władza` albo do `należy`,
a `z dodatkami` do `szynki`, do `koszt` albo do `przewyższa`,
i po każdej z tych nazw widać, którą poprawkę autor ma rozważyć.
Nazwa wzięta z materiału poprzedzającego modyfikator tego nie daje,
i to jest powód, dla którego produkcja swoją głowę wyróżnia:
grupa imienna otwierająca zdanie dzieli ten materiał z całym zdaniem,
więc obaj gospodarze wychodzą jednym napisem,
a rozdziela je dopiero dopisany symbol konstytuenta —
`Władza zwierzchnia (NP)` obok `Władza zwierzchnia (ClauseConjunct)` —
po którym wybór jest widoczny, a nie nazwany po imieniu.

Głowę wyróżnia znacznik `Głowa` wewnątrz ciała, a nie numer pozycji obok niego.
Numer myli się bez śladu: przestawione ciało zostawia go niezmienionym
i nikt tego nie zauważy, a znacznik przesuwa się razem ze swoją częścią.
Ciało o kilku częściach bez znacznika nie powstaje wcale,
więc produkcja dopisana bez głowy przerywa budowanie gramatyki na swoim wierszu,
zamiast nazwać gospodarza pierwszą córką, którąkolwiek by ona była.
Odmowę i oba zdania z tymi werdyktami sprawdza `tests/test_subset.py`.

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
Pierwszy ma odpowiedź w gramatyce, a drugi dostał ją dopiero pomiarem.

Czytanie jest kwotowane po lematach, po wartościach cech i po częściach mowy
([subset.md](subset.md#co-się-liczy-jako-jedno-czytanie)),
więc pozycja tablicy trzymana osobno dla każdego środowiska cech
nie spakuje niczego i policzy wyprowadzenia zamiast czytań.
Jest to dokładnie ten błąd, który zapisuje
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure),
i ten, przez który
[obudowanie Świgry](swigra.md#why-wrapping-it-does-not-get-there)
jest pisaniem gramatyki po raz drugi.
Pozycja niesie więc etykietę i rozpiętość, i nic ponad to,
czyli dokładnie tyle, ile niesie sygnatura czytania.
Zarabia to na siebie na tym samym kwotowaniu:
`zapisuje` ma dwa lematy, a lemat do sygnatury nie wchodzi,
więc `Program zapisuje ustawienia.` wyprowadza się dwa razy na jedną pozycję,
i mnożyłoby się to przez każde następne słowo, któremu słownik daje dwa lematy.

Na czym drugi warunek się rozchodzi, pokazuje zdanie, które olski przyjmuje:

```sh
python3 -m olski.check -c "Zobacz docs/subset.md."
```

Czytanie ma jedno, a suma iloczynów po samych pozycjach liczy nad nim dwa.
`Complements` nad `docs/subset.md` buduje się dwiema produkcjami
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

Wyjścia są z tego dwa i tańsze jest drugie, bo pierwsze zmierzono i liczy gorzej.
Pierwszym jest pozycja rozszczepiona po cechach, które wypuszcza:
dwa warianty `Complements` z tego zdania stoją wtedy w tablicy osobno,
para nieunifikująca się nie powstaje wcale i to zdanie wychodzi z jednym czytaniem.
Rozszczepienie idzie po cechach wypuszczanych, a nie po całym środowisku,
więc jest węższe od tego, przed którym broni pierwszy warunek wyżej —
ale nie dość węższe, i widać to na zdaniu, które olski przyjmuje tak samo:

```sh
python3 -m olski.check -c "Projekt jest dla przyjemności."
```

`przyjemności` ma pięć czytań, więc `NP` nad nim rozszczepia się na pięć pozycji,
a `dla` przepuszcza z nich dwie, obie w dopełniaczu i różne liczbą.
`Modifier` nad tym przypadka ani liczby nie wypuszcza,
więc obie wracają pod jedną pozycję jako dwa wyprowadzenia jednego kształtu,
i suma iloczynów liczy nad tym zdaniem dwa czytania zamiast jednego.
Nadmiar wychodzi więc rozszczepieniu tam,
gdzie cecha, która pozycje rozdzieliła, ginie u rodzica,
a stamtąd ten iloczyn idzie w górę aż do korzenia.

Stoi więc wyjście drugie: iloczyn liczony po parach, które unifikacja przepuszcza,
co zostawia tablicę spakowaną i przenosi koszt z pakowania do liczenia.
Tak liczy `Las.klasy` w `olski/parse.py`:
kształty jednej pozycji stoją w klasach po tym, jakie cechy wypuszczają,
i kombinacja klas, której produkcja nie składa, nie wnosi ani jednego czytania.
Miarą, wobec której oba warianty zmierzono, był enumerator zstępujący,
który tę tablicę zastąpiła —
on środowisko cech niósł w dół rozbioru zamiast pod pozycją,
więc pary nieunifikującej się nie liczył.

Zmierzono je trzema przebiegami nad dwoma korpusami,
bo pozycje rozdziela dopiero forma stojąca w zdaniu.
Liczby niżej są ceną, za jaką odrzucono rozszczepienie,
i nie ma ich po co przeliczać:
sonda, która je wzięła, poszła razem z enumeratorem będącym jej miarą,
a wariant, który mierzyła, nie stoi w kodzie i nie ma jak się zmienić.
Zdania, na których widać oba nadmiary, trzyma `tests/test_subset.py`,
więc podstawa tego wywodu nie zniknie po cichu.

Nad 13025 zdaniami Składnicy pod morfologią własną
rozszczepienie rozdziela 31.6% pozycji, czyli 126814 rośnie do 189880,
a najdalej rozdzielona pozycja idzie na dziesięć.
Tablica spakowana liczy nad 56 zdaniami więcej czytań, niż zdanie ma,
i przewraca przy tym 12 werdyktów, wszystkie z `valid` na `ambiguous`;
tablica rozszczepiona myli się nad 224 zdaniami i przewraca 85.
Trzy zdania z tego mianownika nie mają się z czym porównać,
bo wyliczanie stanęło na nich na `MAX_READINGS`, a tablica granicy nie ma.
Nad prozą README, gdzie zdań jest 43,
pozycji przybywa w tej samej krotności — 811 rośnie do 1218 —
a każdy wariant myli się nad dwoma zdaniami.
Rozszczepienie kosztuje więc półtorej tablicy,
a zdań liczy źle cztery razy tyle, co tablica, którą ma naprawiać.

Trzeci przebieg mówi, skąd tych liczb nie brać.
Pod złotą morfologią rozdziela się 71 pozycji z 71877
i żaden wariant nie myli się ani na jednym zdaniu,
bo anotatorzy wybrali po jednym czytaniu na terminal,
a nadmiar bierze się z formy, której słownik daje ich kilka.
Liczba stamtąd byłaby liczbą o anotacji, a nie o gramatyce.

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
i `Ktoś zna docs/subset.md.` wychodzi przez to przyjęte, nie mówiąc o `ś` nic.
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

Las, już zbudowany, przesunął przy tym granicę, za którą podłoże zostaje.
Enumerator zstępujący wołał `bierze` i `unify` w środku obchodzenia wyprowadzeń,
z środowiskiem cech niesionym w dół,
więc zgodność była wpleciona w sam rozbiór.
Tablica Earleya o cechy nie pyta wcale,
a unifikacja przechodzi po lesie osobno i w jednym miejscu:
`_zawężenia` w `olski/parse.py` rozstrzyga, czy córka pasuje do rodzica,
i nikt poza nim tego nie rozstrzyga.
Warunek precedencji ma się więc gdzie wpisać —
`_przejdź` dostaje ciało wraz z rozpiętościami córek,
czyli dokładnie to, o co taki warunek pyta —
i nie żąda rozwinięcia permutacji po to, żeby zostać wypowiedzianym.
Rozwinięcie zostaje wyborem o liczbę czytań, a nie ceną wejścia.

Urwiska to nie dotyka i nie ma udawać, że dotyka.
Pozycja lasu jest jednym odcinkiem tekstu,
a luka przeciągana przez ciąg żąda zbioru odcinków,
więc tam przerabia się tablicę, a nie warstwę nad nią,
i szczebel zostaje wyceniony tak, jak wycenia go
[urwisko](#the-cliff-discontinuity).

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
The membership test itself is `skład/rozbiór.py`,
which reads a parser reading back as a tree of the abstract syntax,
and what it recovers, what it cannot,
and why one reading comes back as several trees
is owned by
[sklad.md](sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma).
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

This is testable and buildable
with no dependency on the grammar existing.
Whether it is useful is a separate question,
and it is a list of candidates rather than a queue:
the single-letter-word rule was built and deleted,
the register that keeps such a rule honest being text somebody typesets
rather than documentation, which is what this pack is scoped to.
[firing-rates.md](firing-rates.md#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt)
holds the reading that settled it.

Typographic rules were lint rules,
so it shipped with the pack and went with it
([linter.md](linter.md#what-closed-the-track)).

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
