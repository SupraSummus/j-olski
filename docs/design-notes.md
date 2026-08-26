# Design notes

Decisions that have been taken are marked as such;
everything still open lives in [open-questions.md](open-questions.md).
The direction this grammar is grown in, which has no end target, is in
[roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę),
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
The track's direction names a property of a sentence and no machinery,
so a mechanism stronger than a context-free grammar,
or one standing beside the grammar rather than inside it,
is a question of price rather than of permission.
See [Formalizm jest środkiem, a nie celem](#formalizm-jest-środkiem-a-nie-celem).

**Gramatyka jest danymi, a symbol w niej napisem, nie obiektem.**
Produkcja nazywa swoją głowę napisem, a `nt` odsyła do symbolu tym samym napisem,
więc symbol ma jedną nazwę i jest nią ta, którą drukuje werdykt.
Symbol powoływany obiektem czyta się lepiej tam, gdzie pisze się produkcję,
a płaci dwiema nazwami na jeden symbol,
bo identyfikator jest w tym repozytorium polski, a symbol gramatyki angielski.
To, co miał kupić, przychodzi bez niego:
checki w `olski/grammar.py` łapią literówkę w głowie produkcji,
w nazwie cechy i w nazwie zmiennej,
a powtórzenia nie ma, bo cechy córki-głowy wychodzą z konstytuenta same
(tamże).
Pytanie wraca, jeżeli symbole zaczną przybywać regularnie
albo któryś z tych checków wyjdzie na gramatyce czerwony.

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

**Olski does not scramble.**
Discontinuous constituents stay out,
which is what keeps the whole subset context-free.
The fork was settled by measurement rather than by taste:
see [nieciągłość zmierzono](#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
for what it buys, what it costs, and what would reopen it.

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
[one reading](subset.md#co-się-liczy-jako-jedno-odczytanie).
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

The answer is no, and it came from a measurement rather than from the ladder:
[nieciągłość zmierzono](#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
holds what the yes would have bought and what it would have cost.
That section stands below
[the second currency](#the-second-currency-ambiguity)
because the cost is paid in ambiguity and not in parse time,
which is the opposite of where this section's pricing looks for it.

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

### Nieciągłość zmierzono i olski jej nie bierze

Rozwidlenie o przestawianiu zapadło z pomiaru, a nie z gustu.
Nieciągłości potrzebuje 2,5 procent zdań cudzej polszczyzny,
kupuje ona w olskim zero zdań,
a odbiera jednoznaczność prawie co trzeciemu zdaniu, które ją ma.
Sama odmowa ucisza drugie czytanie w co najwyżej dwóch zdaniach korpusu,
którym olski obiecuje jedno, a Świgra znalazła obok niego to drugie.
Olski zostaje więc na szczeblu 2 [drabiny](#the-cost-ladder)
i przestawiania nie wpuszcza.

**Potrzeba: 323 zdania z 13 035.**
Świgra, gramatyka, z której powstała Składnica,
zapisuje nieciągłość osobnym nieterminalem `ξ`:
fraza stoi przy zdaniu, a wymaga jej coś w jego środku
([swigra.md](swigra.md#one-gap-instead-of-a-different-complexity-class)).
Drzewo wzorcowe z takim węzłem jest więc zdaniem,
któremu polszczyzna kazała przestawiać,
i zdaniem, którego analizę zatwierdził człowiek, wybierając to drzewo z lasu.
Takich drzew jest 323, czyli 2,5 procent zmierzonych.
Szczelina wypada po jednej w 320 z nich i po dwie w trzech.
Granicy „najwyżej jedna w ciągu”, którą Świgra sobie postawiła,
te trzy nie przekraczają: ciągów jest w zdaniu złożonym tyle, ile zdań składowych.
Potrzeba nie jest zakupem.
Konstrukcja kupuje zdanie dopiero wtedy, gdy nic innego go nie blokuje,
więc udział zdań z nieciągłością ogranicza zakup z góry i nie równa się jemu.
Próg odmowy wynosi w tym dokumencie
[trzy procent zdań za skok z sześcianu na szósty stopień](#making-the-trade-measurable)
i mówi o różnicy zakupu i ceny,
więc 2,5 procent potrzeby wystarcza, żeby odpowiedź zapadła przed odejmowaniem.

**Zakup w olskim: zero.**
Z 323 zdań olski odrzuca 318, trzy przyjmuje bez żadnej szczeliny,
a dwa wypuszcza wieloznacznie,
więc żadne z nich nie jest zakupem dla nikogo.
Analizy odrzuconych kończą się na bezokoliczniku, na cząstce, na znaku
przestankowym, na imiesłowie biernym i na predykatywie,
czyli na słowach, których żadna produkcja nie bierze niezależnie od szyku,
a garść z nich dochodzi do końca zdania i nie domyka go wcale.
Przysłówka wśród nich nie ma: produkcja, która go stamtąd zdjęła,
nie kupiła ani jednego z tych zdań
([subset.md](subset.md#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe)).
Nieciągłość jest w tych zdaniach ostatnim brakiem, a nie pierwszym,
i widać to nawet na najkrótszych z nich.
`Co mamy wziąć?` i `To chcę podkreślić.` stają na zaimku rzeczownym,
a `Gdzie są przetrzymywani zakładnicy?` na zaimku przysłownym,
czyli wszystkie trzy na pierwszym słowie,
a więc przed wysunięciem, o które w tych zdaniach chodzi.
Nieciągłość dopisana do gramatyki nie przyjmie zdania,
którego analiza kończy się na cząstce.
Najkrótsze zdania tego zbioru są przy tym w większości pytaniami,
a cały zbiór nie: pytań jest w nim 25 z 323.

Za mową niezależną wypadła nieciągłość także u Świgry i jest to pomiar cudzy.
Składnica powstawała etapami, a w pierwszym z nich gramatyka nieciągłości nie miała,
więc dendrolog odkładał takie zdanie, wpisując powód ręką.
Woliński rozbił potem te powody na losowej próbce stu odłożonych zdań:
mowa niezależna wypadła w trzydziestu dziewięciu, cudzysłów w dwudziestu siedmiu,
myślnik w dziewiętnastu, nawias w czternastu, a nieciągłość w pięciu.
Licząc wobec całego korpusu, nieciągłość zatrzymała jeden procent zdań,
a sama mowa niezależna siedem,
i to ta próbka pokierowała rozbudową tamtej gramatyki
(Woliński 2019, p. 6.6, w [źródłach](#sources) na końcu).
Ten jeden procent jest niski częściowo dlatego,
że Świgra zdjęła sobie część nieciągłości samym wyborem struktury,
zamiast opisywać ją jako nieciągłość:
podmiot rozbijający grupę orzeczenia, spójnik inkorporacyjny
i oderwany człon formy analitycznej dostają tam drzewa ciągłe (tamże, p. 2.13 i 2.14).
Dwa pomiary pytają więc o różne rzeczy — tamten o to, co blokuje analizę
w gramatyce całej polszczyzny, a ten o to, ile zdań potrzebuje szczeliny
w drzewie już zatwierdzonym — a oba stawiają przed nieciągłością przytoczenie.
Robi to również [kolejka odrzuceń](corpus.md#where-the-analyses-stop) olskiego,
którą prowadzi interpunkcja, a zapisuje ona w tym korpusie
głównie dialog i mowę niezależną.

**Cena: 100 z 348 zdań przestaje mieć jedno czytanie.**
Cenę mierzy podłoże więzowe, czyli ten sam podzbiór powiedziany
łukami zależności zamiast produkcjami.
Nie gramatyka olskiego, bo spójność da się zdjąć tylko tam:
produkcja wyprowadza jeden odcinek tekstu i zdjąć tego nie umie,
a podłoże ma spójność jednym więzem globalnym.
Czym to podłoże jest i co jeszcze o nim wiadomo, mówi
[sonda](#podłoże-więzowe-zmierzone-sondą) niżej.
Z 1623 zdań, które olski przyjmuje jednym czytaniem,
podłoże czyta jednoznacznie 348 — deklaracja jest w nim węższa,
więc 1226 odrzuca, a 49 czyta dwojako —
i po zdjęciu spójności 100 z tych 348 przestaje mieć jedno czytanie.
Mianownik rośnie z gramatyką, a te dwie liczby rosną z nim wtedy,
gdy gramatyka dopisuje kształt, który podłoże już miało.
Grupy liczebnikowej podłoże nie ma
([subset.md](subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)),
więc każde zdanie, które ona olskiemu kupiła, odrzuca i tych liczb nie rusza;
cztery szyki ruszyły je, bo łuk podmiotu o kolejności nie mówi nic
i podłoże czytało te zdania, zanim olski dostał na nie ciała.

Płaci się przy tym nie czasem rozbioru, a określeniem,
które sięga ponad czasownik do rzeczownika po drugiej stronie.
Najkrócej widać to na zdaniu definicyjnym:

```sh
python3 -m harness.podłoża -c "Dom jest nieocieplony." --łuki --nieciągłe
```

Bez tej flagi zdanie ma jedno czytanie, z orzecznikiem przy kopuli.
Z nią dochodzi drugie, w którym `nieocieplony` jest przydawką przy `Dom`,
a podmiotem wychodzi fraza nieciągła,
więc wzorzec `X jest Y`, którym pisze się definicje, przestaje mieć jedno czytanie.
Tak samo idzie wyrażenie przyimkowe:
w `Człowiek wraca do poprzedniej wagi` przyłącza się ono po zdjęciu spójności
do `Człowiek` ponad czasownikiem.
Przyłączenie takiego wyrażenia olski oddaje czytelnikowi rozmyślnie
i pokazuje wszystkie miejsca, w które ono dochodzi
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
a spójność jest tym, co ogranicza tę listę do rzeczowników,
przy których fraza naprawdę stoi.
Nieciągłość uderza więc w dwie rzeczy naraz:
w tę listę, którą rozszerza na każdy rzeczownik zdania,
i w rozróżnienie przydawki od orzecznika, które gramatyka utrzymuje szykiem.

**Maskowanie: 128 zdań ze szczeliną odrzuconą, dwa z nich przyjęte.**
Odmowa nieciągłości ma cenę własną, o którą tamte trzy liczby nie pytają.
Zdanie, którego drugie czytanie potrzebuje frazy nieciągłej,
wychodzi olskiemu jednoznaczne, bo tego czytania nie ma czym wyprowadzić,
więc `valid` obiecuje jedno czytanie zdaniu, które ma dwa.
Odrzucenie autor zobaczy i coś z nim zrobi,
a takiej obietnicy po werdykcie nie widać.
Najkrócej widać to na rzeczowniku,
który wybiera ten sam przyimek co rama czasownika przed nim:

```sh
python3 -m harness.podłoża -c "Dziadek wraca do orzechów." --łuki --nieciągłe
```

Bez tej flagi zdanie ma jedno czytanie, z `do orzechów` przy czasowniku.
Z nią dochodzi drugie, w którym podmiotem jest nieciągłe `dziadek do orzechów`.
Samo to czytanie dochodzi w każdym takim zdaniu,
bo podłoże bez spójności przyłącza wyrażenie przyimkowe do każdego rzeczownika,
i jest to cena mierzona wyżej.
Maskowaniem czyni je dopiero czytelnik:
ma je wtedy, gdy rzeczownik z tym przyimkiem jest nazwą jednej rzeczy.
`Maszyna wraca do szycia.` idzie tak samo, więc klasa jest otwarta,
a jej granica biegnie po leksyce, nie po produkcjach.

W Składnicy są tym zdania, którym annotator wybrał drzewo ciągłe,
a Świgra znalazła obok niego analizę ze szczeliną.
Takich zdań jest 128, czyli niecały procent zmierzonych,
a olski przyjmuje z nich dwa, z których krótsze to
`W dwunastu wypadkach kandydatury wojewodów miały być uzgodnione.`
Kolejne dwa czyta wieloznacznie, więc tym niczego nie obiecuje.
Liczy je ta sama sonda, z tego samego pliku co zakup, ale nie z drzewa wybranego:
tam szczelina jest czytaniem właściwym, a tutaj drugim z dwóch.

Jest to górne oszacowanie, a nie odpowiedź.
Annotator tamte analizy odrzucił,
a korpus nie notuje, czy odrzucił je jako niemożliwe, czy jako drugie możliwe,
więc zdań, w których czytelnik naprawdę ma dwa czytania, jest wśród tych 128 mniej.
Rozstrzyga każde takie zdanie człowiek, a nie przebieg,
i jest to ta sama różnica między pozycją a czytelnikiem,
którą nad rejestrem czyta próbką
[open-questions.md](open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma).
Tamto pytanie idzie przy tym w stronę odwrotną niż to:
tam olski melduje wieloznaczność, której czytelnik nie ma, i płaci odrzuceniem,
a tutaj melduje jednoznaczność, której zdanie nie ma, i płaci obietnicą.

Czego te liczby nie mówią, jest trojakie.
Zakup jest ograniczeniem z dołu, a nie liczbą potrzeby:
zdania, którego Świgra nie rozebrała, nikt nie przeliczył,
a bez drzewa wzorcowego jest 41 procent korpusu
([corpus.md](corpus.md#what-the-corpus-contains)),
więc zdanie z dwiema szczelinami w jednym ciągu albo z wysuniętym podmiotem
siedzi wśród nich i tutaj się nie liczy.
Cena jest ceną zdjęcia spójności z deklaracji bliskiej olskiemu,
a nie z jego własnej gramatyki,
i o ile ta deklaracja jest węższa, mówi 348 wobec 1623.
Korpus jest wreszcie prozą i prasą,
a nie dokumentacją techniczną, do której olski jest kierowany.

Wraca to rozwidlenie wtedy, gdy zakup przestanie być zerem,
czyli gdy gramatyka odbierze zdaniom ze szczeliną ich dzisiejsze blokery.
Maskowanie rośnie wtedy razem z zakupem i nie ma własnego wyzwalacza:
dwójka jest mała dlatego, że olski odrzuca 121 z tych 128 zdań,
a odrzuca je na tych samych częściach mowy, tyle że w innej kolejności:
znak przestankowy, cząstka i czas przeszły
zamiast cząstki oraz znaku i bezokolicznika po równo.
Sonda liczy jedno i drugie razem z tymi blokerami po to,
żeby ten moment dało się zauważyć bez powtarzania całego pomiaru:

```sh
python3 -m harness.nieciągłość Składnica-frazowa-180723/
```

### Lukę zmierzono i olski jej nie bierze

Rozwidlenie o przestawianiu zostawiło olskiego na szczeblu 2
[drabiny](#the-cost-ladder),
a maszynerii tego szczebla olski nie używa:
cechy przeciąganej nie ma ani jedna produkcja.
Pomiar wypadł tak samo jak przy nieciągłości:
luka nie kupuje ani jednego zdania potwierdzonego bankiem drzew,
a odbiera jednoznaczność zdaniom, które ją mają.
Powodu nie ma jednak w drabinie.
Jest nim to, że luka nie ma napisu.

**Co luka miała kupić.**
Zdanie względne wypisuje się rolą po roli:
kilkadziesiąt ciał `RelativeCore` w `olski/subset.py`,
po jednym na czoło razy wysunięta rola razy szyk reszty zdania
razy miejsce na okolicznik razy przeczenie,
a role, które te ciała wypełniają, wywodzi
[subset.md](subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka).
Wysunięte dopełnienie sięga tam tylko do formy osobowej,
więc `Ustawa, którą organ gminy może wydać, jest tania.` nie wyprowadza się wcale.
Cecha przeciągana zastępuje te ciała jedną produkcją:
konstytuent ogłasza w cechach, czego mu w środku brakuje,
luka jest produkcją o pustym ciele,
a zdanie względne wiąże ją ze swoim zaimkiem.
Zdanie względne dostaje wtedy każdy szyk i każde miejsce na okolicznik,
jakie ma zdanie zwykłe, wraz z wyjęciem z głębi,
i to zdanie przechodzi jednym czytaniem.

**Luka bez napisu nie ma czego przestawiać.**
Ciało, które stawia ją między innym rodzeństwem, wydaje ten sam napis,
a kształt inny, więc [jest to drugie odczytanie](subset.md#co-się-liczy-jako-jedno-odczytanie).
`Reguła, która rozstrzyga, jest tania.` wychodzi dwoma czytaniami zamiast jednego,
bo luka podmiotu wypada raz przed czasownikiem, a raz za nim;
`Polszczyzna, którą ktoś napisał, jest trudna.` wychodzi trzema,
a `Plik, który program zapisuje, jest konfiguracyjny.` sześcioma.
Czytelnik ma w pierwszych dwóch zdaniach po jednym czytaniu, a w trzecim dwa,
więc nadmiar bierze się w całości z miejsca, w które wypada luka.

**Warunek precedencji na samą lukę odbiera większość tej ceny i nie całą.**
Luka przypięta do pozycji swojej roli —
podmiot na czele, dopełnienie tuż za czasownikiem, który je rządzi —
oddaje pierwszym dwóm zdaniom po jednym czytaniu,
a trzeciemu dwa, które polszczyzna ma:
`który` jest tam i mianownikiem, i biernikiem,
więc plik raz jest zapisywany, a raz zapisuje.
Warunek pilnuje jednak pozycji w ciele produkcji,
a pozycja w ciele przestaje być pozycją w napisie, kiedy zdanie się zagnieżdża.
`Kwiaty otrzymali nauczyciele, którzy przed laty kształcili kolejarskich
specjalistów.` wychodzi przez to dwoma czytaniami:
okolicznik raz stoi w zdaniu za luką, a raz przed całym zdaniem z luką w środku.
Streszczenia obu są znak w znak te same,
więc werdykt nie nazywa nad tym wariantem ani jednej roli
i o różnicy mówi [wierszem o konstytuencie](#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań):
`„przed laty kształcili kolejarskich specjalistów” reads 2 ways`,
czyli wskazuje zdanie względne i nie mówi, że idzie o miejsce luki w nim.

**Nie kupuje przy tym tej konstrukcji, po którą sięgano.**
Zdanie składowe bez podmiotu, czyli to, co przeciąganie dawało mimochodem,
gramatyka wypisuje sama
([subset.md](subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
więc nad 13 035 zdaniami Składnicy pod złotą morfologią
luka przypięta wyciąga z odrzucenia jedno zdanie
i jednoznaczność odbiera kilku;
tabelę przejść drukuje polecenie niżej.
Wyjęcia z głębi nie ma przy tym wśród wyciągniętych ani jedno.
Rejestr ustaw odpowiada mocniej: nad jego 4921 zdaniami
([ustawy.md](ustawy.md#co-gramatyka-z-tego-wyprowadza))
luka nie wyciąga z odrzucenia ani jednego zdania i dwa kosztuje,
a zdania o kształcie tamtej ustawy nie ma w tym rejestrze wcale
([subset.md](subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)).
Konstrukcja, dla której sięga się po szczebel 2, nie występuje więc
w żadnym korpusie, jaki to repozytorium czyta.

**Zakup jest przy tym zerem, bo bank drzew stawia tę rolę na zaimku.**
To jedno wyciągnięte zdanie olski czyta inaczej, niż czyta je drzewo wzorcowe,
i czyta tak z samego mechanizmu:
w `Myślę o tym człowieku, który mnie podglądał.`
podmiotem wychodzi u niego rozpiętość pusta, a bank drzew wskazuje `który`.
Role widoczne są przy tym dobre i o znaczeniu zdania luka nie kłamie:
rozchodzi się drzewo, a nie odczyt.
Rola wypełniona niczym nie jest jednak analizą, którą zatwierdził annotator,
a [zdanie przeczytane odwrotnie zakupem nie
jest](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).

**Na wydruku ta cena nie wypada, choć luka napisu nie ma.**
Streszczenie czytania nazywa rolę napisem wziętym ze zdania,
ale luka stoi tylko wewnątrz zdania względnego, bo domyka ją zaimek,
a tam streszczenie nie zagląda
([werdykt jest zapytaniem o las](#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)).
Roli wypełnionej luką werdykt więc nie nazywa,
tak samo jak nie nazywa roli wypełnionej zaimkiem,
i zostaje cena z akapitu wyżej: rozpiętość pusta nie trafia w żadną złotą.

**Symboli nie ubywa.**
`RelativeCore` schodzi do tych ciał, które wysuwają wyrażenie przyimkowe,
a `ClauseConjunct` rośnie za to kilkakrotnie,
bo przeciąganie żąda ciała na każdą córkę, która lukę unosi,
i cała gramatyka rośnie o kilkadziesiąt produkcji;
liczby na dziś drukuje kolumna `produkcji` w wydruku sondy.
Drabina wycenia szczebel 2 na mnożenie się symboli i wycenia trafnie,
tylko że mnożenie wypada na rodzinie zdaniowej, a nie na względnej.

Parser nie kosztował ani jednej zmiany, i tyle drabina obiecała.
Tablica Earleya przyjmuje produkcję o pustym ciele,
a `Node.span` w `olski/parse.py` jest wpisywane przy budowaniu właśnie dlatego,
że węzeł takiej produkcji nie ma dzieci, z których dałoby się rozpiętość wyliczyć.
Cena szczebla 2 nie wypada więc w tym, co liczy rozbiór,
a to jest ta sama obserwacja, którą robi
[druga waluta](#the-second-currency-ambiguity) nad całą drabiną.

Nad prozą README luka odbiera kilka jednoznaczności
i nie wyciąga z odrzucenia ani jednego zdania.
Mówi to o tym pliku, a nie o luce:
odkąd omija on konstrukcje, których olski nie wyprowadza
([README](../README.md#konwencje)),
zdanie względne stoi w nim gęściej niż w którymkolwiek korpusie,
a jednoznaczność luka odbiera właśnie takiemu zdaniu.
Bank drzew, proza README i ustawy odpowiadają więc zgodnie w kierunku ceny,
a różni je gęstość konstrukcji, po którą sięgano.

Wraca to rozwidlenie wtedy, gdy luka przestanie być węzłem o pustej rozpiętości,
a zacznie wskazywać zaimek, który ją wiąże:
zakup przestaje wtedy przeczyć bankowi drzew, a wydruk dostaje nazwę roli.
Zostaje po tym ta reszta pierwszej ceny,
której warunek precedencji nie zdjął.
Ruch trzyma [TODO.md](../TODO.md),
a zdania składowego bez podmiotu ten ruch nie dotyczy,
bo wypisuje je sama gramatyka.

Powtarzają ten pomiar te polecenia,
a rejestr ustaw ściąga się tak, jak mówi
[ustawy.md](ustawy.md#skąd-bierze-się-korpus):

```sh
python3 -m harness.luka Składnica-frazowa-180723/
python3 -m harness.luka proza/README.txt
cat proza/ustawy/*.txt > proza/ustawy-razem.txt
python3 -m harness.luka proza/ustawy-razem.txt
python3 -m harness.luka -c "Reguła, która rozstrzyga, jest tania."
```

## Formalizm jest środkiem, a nie celem

Drabina wycenia formalizmy i żadnego nie obiecuje.
Gramatyka bezkontekstowa z cechami jest tym, na czym olski stoi,
a nie tym, do czego zmierza:
kierunek tego toru mówi, co ma zajść nad zdaniem,
a nie czym ma być wyprowadzone,
i trzyma go [roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).
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

Otwartość środków jest deklaracją, dopóki nikt żadnego innego nie wyceni.
`harness/wiezy.py` wycenia jeden: ten sam podzbiór powiedziany łukami nad grafem segmentów,
gdzie zgodność jest warunkiem na parę słów,
szyk osobnym polem deklaracji,
a spójność frazy jednym warunkiem globalnym, który wolno zdjąć.
Zyski i ceny stoją niżej, a podłoża tego żąda z nich tylko nieciągłość:
szyk i przyłączenie kupuje rozdzielenie dominacji od precedencji,
czyli szczebel 1 [drabiny](#the-cost-ladder), sześcian i gramatyka bezkontekstowa.
Decyzji o przeniesieniu olskiego na to podłoże nie ma,
a ruch, który z sondy wynika, kosztuje mniej niż ona sama:
zdanie deklaruje córki, a kolejność deklaruje warunek nad nimi
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).

Powtarzają to te polecenia, a ostatnie warto puścić także bez flagi:

```sh
python3 -m harness.markdown README.md --into proza/
python3 -m harness.podłoża proza/README.txt
python3 -m harness.podłoża proza/README.txt --budżet 0.1
python3 -m harness.podłoża -c "Dobrą Jan pisze polszczyznę." --nieciągłe --łuki
python3 -m harness.podłoża -c "Zbiór tekstów przechodzących przez wszystkie reguły jest podzbiorem polszczyzny w jednym i w drugim przypadku."
```

Każde zdanie tej prozy sonda rozbiera w budżecie 10 sekund,
a każde poniżej dziesiątej części sekundy,
więc przebieg z takim budżetem kończy je tak samo —
i dlatego zamiast najwolniejszego czasu stoi tu próg,
bo zegar rusza się między przebiegami, a próg nie.
Ten sam werdykt dostaje od obu programów mniej niż co czwarte zdanie tej prozy,
a tę samą liczbę czytań jeszcze mniej,
i to drugie jest mocniejszym z dwóch odczytów:
werdykt zgadza się już wtedy, gdy jedna strona ma dwa czytania, a druga sześć,
a liczba nie, i `Koszt samej szynki przewyższa koszt szynki z dodatkami`
wychodzi po obu stronach dokładnie sześcioma —
co widać dopiero po `-c`, bo w README to zdanie stoi w bloku,
którego ekstrakcja nie wypuszcza.

Większość rozejść staje na przecinku, którego sonda nie ma do czego przyłączyć.
Granica biegnie tam, gdzie olski bierze
[przecinek jako znak koordynacji](subset.md#what-the-grammar-covers)
oraz [interpunkcję zdaniową](subset.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają),
a sonda po swojej stronie ma spójnik i nic poza nim.
Reszta rozejść nie mówi o formalizmie nic i mówi coś o samej sondzie:
liczebnika, formy z leksykonu projektu, rzeczownika odczasownikowego
ani cudzysłowu `harness/polszczyzna.py` nie ma,
a olski ma każde z nich i wyprowadza nimi zdania tego pliku.
Deklaracja stojąca obok gramatyki jest drugim zapisem tego podzbioru,
więc starzeje się po cichu przy każdym dopisaniu do olskiego,
produkcji czy wiersza leksykonu.
Czy deklaracje mają iść za produkcjami, czy sonda ma się skasować,
trzyma [`TODO.md`](../TODO.md); dopóki to nie zapadnie,
liczba zgodnych zdań spada z każdą taką zmianą i nie mówi o niej nic.

Ta liczba ma drugą przyczynę i jest nią sama proza:
README omija konstrukcje, których olski nie wyprowadza
([README](../README.md#konwencje)),
więc zdanie względne i zdanie współrzędne stoją w tym pliku gęsto,
a przecinek jest tym, czego sonda nie bierze.
Tak właśnie kosztuje figura brana nad własną prozą,
przed czym [`CLAUDE.md`](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje) ostrzega.

**Szyk i przyłączenie schodzą z produkcji na nic.**
Kilka deklaracji wypisuje zdanie olskiego,
a miejsce na okolicznik jedna reguła nad nimi
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
i dopiero rozwinięcie robi z nich kilkadziesiąt ciał `ClauseConjunct`,
które czyta parser.
Łuk podmiotu nie mówi o porządku nic,
więc wszystkie sześć szyków są po tamtej stronie jedną deklaracją,
a pozycje okolicznika, których
[subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)
liczy kilkadziesiąt, są trzema, po jednej na głowę,
i dwa czytania `Program zapisuje ustawienia w pliku`
biorą się z tego, że dozwolone są oba łuki.

Zysk pierwszy jest więc wzięty i wzięło go rozwinięcie szyku,
a nie przeniesienie olskiego na to podłoże.
Rozwinięcie nie tyka zysku drugiego ani trzeciego, bo żaden nie jest o szyk.

**Nieciągłość przestaje być szczeblem.**
`Dobrą Jan pisze polszczyznę` nie wyprowadza się w olskim wcale,
a po zdjęciu spójności wychodzi z niego czytanie,
w którym `Dobrą polszczyznę` jest jedną frazą przerwaną podmiotem i orzeczeniem.
Kosztuje to jedno pole i zero deklaracji,
bo spójność jest tu warunkiem wystawianym, a nie własnością formalizmu.
[Urwisko](#the-cliff-discontinuity) wycenia to samo na szósty stopień
i wycenia poprawnie, tylko że wycenia szczebel, a nie zjawisko:
przy tym podłożu fan-out nie jest pokrętłem, którym się cokolwiek kręci.
To jedno pole jest przy tym tym, czym zmierzono cenę nieciągłości,
i sonda tego pomiaru stoi obok
([nieciągłość zmierzono](#nieciągłość-zmierzono-i-olski-jej-nie-bierze)):
podłoże zarobiło więc na siebie rozstrzygnięciem rozwidlenia,
a nie samym porównaniem deklaracji.

**Odrzucenie zaczyna mówić, na czym stanęło.**
Słowo, do którego żaden łuk nie dochodzi, wypisuje się przy werdykcie,
i nad zdaniem o konwencjach z README wychodzą z tego dwa przecinki.
Jest to ta sama informacja, którą `olski-corpus` liczy jako bloker,
a `olski-check` mówi osobnym zdaniem werdyktu
([subset.md](subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)),
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
Dwa pierwsze zamyka deklaracja i są w `harness/polszczyzna.py` zamknięte.
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
Takim zdaniem jest to, w którym odrzucenie stoi na kształcie, a nie na słowniku,
czyli takie, w którym każda forma ma czytanie brane przez jakąś produkcję:
`Zbiór tekstów przechodzących przez wszystkie reguły jest podzbiorem
polszczyzny w jednym i w drugim przypadku`.
README tego zdania nie ma i podaje się je sondzie przez `-c`.
Sonda liczy je kilka sekund,
a każdemu zdaniu prozy README wydaje werdykt w setnych częściach sekundy,
czyli o dwa rzędy wielkości szybciej;
ten plik pisze tę samą myśl zdaniem względnym z drugim członem,
którego sonda nie przyłącza, więc dziedziny przycinają się tam wcześnie.
Ten czas trzyma warunek na lemat kopuli w deklaracji dopełnienia,
czyli walencja powiedziana po tej stronie:
bez niego to samo zdanie liczy się przeszło trzy razy dłużej
i budżetu domyślnego nie dowozi wcale,
więc przestrzeń, którą przycina jedna pozycja ramy,
jest tutaj przeszło dwiema trzecimi najgorszego przypadku.
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
  The one GLR system measured over real Polish says nothing about that cost:
  its table is 146 states.

That same system supplies a baseline worth flinching at:
20% of its input fails to parse
against a grammar hand-fitted to a register far narrower than olski.
See [glr-in-practice.md](glr-in-practice.md#measurements).

Nullable rules, which pro-drop makes unavoidable, are not an objection:
Tomita's original algorithm breaks on them and maintained implementations do not.

**Earley is the boring answer and it is what `olski/parse.py` runs.**
It handles any CFG, including left recursion and nullable rules,
with no preprocessing;
it produces a shared packed parse forest natively;
its worst case is cubic but real grammars behave far better.
Decisively for a project whose grammar is still being designed:
the grammar can change without rebuilding an automaton.
GLR stays an optimization to reach for if measurement ever demands one,
and no measurement does:
a run over the whole of Składnica takes half a minute.

For free word order specifically,
the move that keeps a CFG viable
is to separate **immediate dominance from linear precedence**,
as GPSG did.
Dominance rules say what the daughters are,
separate precedence constraints say which orders are legal,
and a preprocessor deals with the factorial.
Olski's clause is written that way,
and what it bought beyond the shorter grammar
is in [subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk).
This also keeps the subset honest:
the one permutation excluded from olski
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
Zdanie ustawy o 28 042 czytaniach pod gramatyką z tamtej chwili —
[jedno z tych, w których liczba czytań przestaje o czymkolwiek mówić](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem) —
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
[przepis o dziesiątkach tysięcy czytań](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem):
werdykt nazywa tam dopełnienie, którego wypisane czytania nie rozdzielają.
Kosztuje to jedno rozstrzygnięcie, którego lista czytań nie potrzebuje.
Etykieta roli pada w jednym czytaniu kilka razy,
bo zdanie współrzędne ma własny podmiot,
więc nad lasem trzeba powiedzieć,
które pozycje jednej etykiety są tym samym wystąpieniem.
Jest nim to, które nazywa streszczenie, czyli pierwsze.

Pierwsze w zdaniu streszczanym, a nie w zdaniu podrzędnym pod nim.
Oba podsumowania zatrzymują się na zdaniu względnym i dopełnieniowym,
bo rola z ich wnętrza należy do nich, a nie do zdania nad nimi:
`Reguła, która rozstrzyga o zdaniu, jest tania.` ma czasownik `jest`,
a bez tego zatrzymania werdykt nazywa czasownikiem `rozstrzyga`,
czyli mówi o zdaniu nieprawdę.
Zatrzymać się muszą oba naraz,
bo inaczej wiersz `differing in` nazywa rolę,
której lista czytań pod nim nie nazywa.
Zdania współrzędnego to nie obejmuje,
bo jego role należą do tego samego zdania.

Trzeci wiersz nazywa konstytuent i odpowiada tam, gdzie tamte dwa nie sięgają.
Streszczenie pokazuje wypełnienie roli oraz gospodarza przyłączenia,
więc dwa czytania różne czymkolwiek innym wychodzą z niego jednym napisem.
Miejsca takie są dwa.
`Dodatkowych przedstawicieli wyznacza zainteresowana rada gminy.`
różni czytanie słownikowe wewnątrz wypełnienia jednej roli —
`zainteresowana` jest tam i rzeczownikiem, a `rada` formą `rad` —
a `Ustawa mówi, że organ gminy wydaje przepis.` różni podmiot i dopełnienie
zdania podrzędnego, w które streszczenie nie zagląda.
Lista czytań zdania o tej różnicy milczy, bo oba czytania mają w niej jeden wpis,
więc bez tego wiersza werdykt mówi nad każdym z tych zdań samo `2 readings`,
czyli nie mówi, czym te dwa czytania się różnią.
Z nim mówi `„zainteresowana rada gminy” reads 2 ways`.

Nazwany jest konstytuent, a nie różnica pod nim,
i tę granicę stawia tożsamość czytania:
lemat i część mowy są z niej wyłączone rozmyślnie,
więc wiersz nazywający lemat mówiłby o czymś,
czego liczba czytań obok niego nie liczy.
Wpis dostaje przy tym konstytuent najwęższy:
napis obejmujący napis innego wpisu mówi o tym samym słowie i o kilku obok niego,
bo wieloznaczność wychodzi w górę.
`równych praw kobiet` czyta się dwoma sposobami przez samo `równych`,
`równych praw kobiet i mężczyzn` trzema, a naprawić trzeba jedno słowo.

Samą różnicę pokazuje pod tym wierszem lista, o ile konstytuent jest zdaniem.
Streszczenie zdania podrzędnego jest streszczeniem tego zdania,
a nie tego nad nim, więc streszczone osobno mówi to, o czym wiersz milczy:

```sh
python3 -m olski.check --readings -c "Ustawa mówi, że organ gminy wydaje przepis."
```

```text
<text>: ambiguous Ustawa mówi, że organ gminy wydaje przepis.
                  2 readings; „organ gminy wydaje przepis” reads 2 ways
                  - Subject: Ustawa, Verb: mówi
                  „organ gminy wydaje przepis” czyta się tak:
                    - Subject: organ gminy, Object: przepis, Verb: wydaje
                    - Subject: przepis, Object: organ gminy, Verb: wydaje
0 of 1 sentences are olski, and 1 have a reading
```

Granicy między konstytuentem a różnicą pod nim lista nie rusza:
rola lematem nie jest, więc lista mówi o tym, co tożsamość czytania liczy.
Wierszy przy tym nie mnoży, bo stoi pod listą czytań zdania, a nie w niej:
zdanie o takim konstytuencie i sześciu przyłączeniach dostaje kilkanaście
wierszy zdania i dwa wiersze konstytuentu, a nie ich iloczyn.
Głębiej zagnieżdżenie nie sięga, bo wpis dostaje konstytuent najwęższy,
więc dwa wpisy jednego zdania stoją obok siebie, a nie jeden w drugim.
Bez listy zostaje grupa imienna, bo roli zdania nie nosi.
Jej streszczenia wychodzą puste i sobie równe, więc zostaje z nich jedno,
a różnicę niesie tam głowa, której streszczenie nie nazywa
([`TODO.md`](../TODO.md)).

Wykluczenia są trzy i każde odpowiada jednemu wierszowi,
który werdykt drukuje bez tego podsumowania.
Ciąg współrzędny wiersza nie dostaje, bo granicę członu pokazuje nawias w napisie roli.
Konstytuent z rolą pod sobą — z tą, do której streszczenie zagląda —
nie dostaje go, bo o tej roli mówi wiersz `differing in`.
Konstytuent z nazwanym przyłączeniem pod sobą nie dostaje go,
bo o tym wyborze mówi wiersz z gospodarzami,
a ten granicy zdania podrzędnego nie zna i sięga też do jego wnętrza.
Bez ostatniego z tych trzech zdanie o dwunastu czytaniach
dostawałoby te same dwa przyłączenia po raz drugi,
raz nazwane przyimkiem, a raz konstytuentem długim na całe zdanie podrzędne.

Cena idzie na to, o czym wiersz milczy, i widać ją na jednej klasie.
Nawias obejmuje ciąg, którym jest sama rola, a nie ciąg stojący w wypełnieniu głębiej,
więc dwa czytania różne nawiasowaniem takiego ciągu wychodzą jednym napisem,
a wiersz o konstytuencie ustępuje im miejsca:
`Ustawa określa zadania ochrony ludności i obrony cywilnej.`
zostaje samą liczbą czytań, choć raz są to zadania dwóch rzeczy, a raz jednej.
Ile zdań tak zostaje, mierzy
[disambiguation.md](disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca).

Lista czytań niesie przy tym każde streszczenie raz.
Powtórzone nie mówi nic ponad to, które stoi nad nim,
a powtórzeń bywa tyle, ile czytań schodzi się pod jednym napisem:
streszczenie nazywa pierwszy modyfikator zdania i jego gospodarza,
więc zdanie o sześciu wyrażeniach przyimkowych
wychodzi kilkunastoma wierszami na swoje sześćdziesiąt cztery czytania.
Liczby czytań lista przez to nie podaje, bo tę podaje las.
Reguła obowiązuje każdą z tych list, więc i tę pod konstytuentem:
i tam dwa kształty o jednym napisie stoją jednym wpisem,
a grupa imienna zostaje przez to bez listy.

Zdanie współrzędne zatrzymania nie ma, a streszczeń dostaje tyle,
ile ma zdań składowych, po jednym na składowe:

```sh
python3 -m olski.check --readings -c "Autor działa i zapisuje ustawienia."
```

```text
<text>: valid     Autor działa i zapisuje ustawienia.
                  one reading
                  - Subject: Autor, Verb: działa
                    Object: ustawienia, Verb: zapisuje
```

Kreska otwiera czytanie, a składowe następne stoją pod nim bez niej,
i widać po tym, że dopełnienie jest z innego zdania składowego niż podmiot.
Jedno streszczenie na zdanie nazywałoby pierwsze wystąpienie każdej roli,
czyli role zdania składowego pierwszego, i o reszcie zdania milczało:
`Wciśnij klawisz wu i zapisz plik konfiguracyjny.` wychodziłoby wtedy
werdyktem `valid` i wierszem `Object: klawisz wu, Verb: Wciśnij`,
z którego czytelnik odczytuje, że parser drugiej połowy zdania nie rozebrał.
Zdanie o dwóch składowych albo więcej jest w README co trzecie
([corpus.md](corpus.md#the-same-queue-over-prose) mówi, czym się ten plik czyta),
więc milczenie to nie jest przypadkiem z brzegu.
Granicą podziału jest przy tym początek składowego następnego,
a nie koniec poprzedniego,
więc rola stojąca między składowymi wpada do tego przed nią:
dopowiedzenie za dwukropkiem stoi poza każdym zdaniem składowym
i podział po końcach zostawiłby je bez streszczenia.

Cena tego podziału jest iloczynem i bierzemy ją świadomie.
Streszczenia różne wchodzą na listę każde raz,
a dwa składowe wieloznaczne każde na swój sposób
dają streszczeń tyle, ile jest par ich odmian:
jedno zdanie README wychodzi przez to kilkudziesięcioma streszczeniami
po trzy wiersze każde, gdzie streszczenie jedno na zdanie dawało kilka wierszy.
Iloczyn ucina `MAX_READINGS`, tak jak ucina listę czytań,
a płacą go zdania odrzucone już jako wieloznaczne:
zdanie `valid` ma jedno czytanie, więc dostaje po jednym wierszu na składowe.
Wpisu na składowe zamiast wiersza na czytanie ta lista nie ma,
choć zamieniłby ten iloczyn na sumę,
tak jak zamienia go wiersz o konstytuencie rozbieżnym;
co za to płaci, mówi [`TODO.md`](../TODO.md).

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
o co [pomiar pyta bank drzew](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold).
Żadne z tych pytań nie żąda innego parsera, tylko innego podsumowania.

### Co się pakuje, rozstrzyga tożsamość czytania

Las odpowiada na pytanie olskiego pod dwoma warunkami:
pod jedną pozycję ma iść to, co jest jednym czytaniem,
a liczba z jednej pozycji ma się łączyć z liczbą z sąsiedniej tak,
jak łączy je unifikacja.
Pierwszy ma odpowiedź w gramatyce, a drugi dostał ją dopiero pomiarem.

Czytanie jest kwotowane po lematach, po wartościach cech i po częściach mowy
([subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie)),
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

Kosztuje to więzy, których nad taką pozycją nie ma jak postawić.
Rodzic widzi z córki etykietę, rozpiętość i cechy, które ona wypuszcza,
a dwa czytania różniące się wewnątrz jednej pozycji wychodzą do niego
jednym kształtem i jedną liczbą.
Warunek postawiony nad córką nie ma więc czym ich rozdzielić,
i nie jest to brak maszynerii, tylko granica tej decyzji:
pozycja, której cena ma stać na takim rozdzieleniu,
albo wypuszcza cechę, po której ją widać, albo dostaje osobny symbol.
Wpuszczenie okolicznika zdaniowego nad ciąg współrzędny poszło drogą pierwszą
([subset.md](subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)),
a tym, co żadnej z nich nie ma, jest luka: różni ją dokładnie to,
czego pozycja o sobie nie mówi.

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
Nad prozą README, która miała wtedy 43 zdania,
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
oraz ten, który [`TODO.md`](../TODO.md) stawia `harness/polszczyzna.py`.
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
python3 -m olski.check -c "Prozę w tym repozytorium łamiemy według Semantic Line Breaks, a nową piszemy po polsku."
python3 -m olski.check -c "Nowa program zapisuje ustawienia."
```

Pierwsze zdanie stoi na nazwie obcej przytoczonej po polsku i na `polsku`,
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
Porządek wyszedł do warunków precedencji:
deklaracja wymienia córki, warunek obok niej mówi, które przestawienia wchodzą,
a rozwinięcie składa jedno z drugim przed rozbiorem
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
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

Kolejność bierze się z tego, czego która rzecz potrzebuje,
i reguła, którą trzy pierwsze wyłożyły, obowiązuje czwartą.
Las szedł pierwszy, bo produkcji nie rusza,
więc dał się porównać werdykt po werdykcie z tym, co stało.
Walencja szła przed precedencją, bo kasuje czytania,
a rozwinięcie permutacji je dopisuje,
i bez lasu nie było czym przeczytać, ile ich dopisze:
dopisało cztery ciała i ani jedno nie jest permutacją
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Ruch, który czytania dopisuje, idzie więc za każdym, który je kasuje,
i to jest wszystko, co ta kolejność mówi luce.

Las przesunął przy tym granicę, za którą podłoże zostaje.
Enumerator zstępujący wołał `bierze` i `unify` w środku obchodzenia wyprowadzeń,
z środowiskiem cech niesionym w dół,
więc zgodność była wpleciona w sam rozbiór.
Tablica Earleya o cechy nie pyta wcale,
a unifikacja przechodzi po lesie osobno i w jednym miejscu:
`_sposoby` w `olski/parse.py` rozstrzyga, czy córka pasuje do rodzica,
i nikt poza nim tego nie rozstrzyga.
Warunek precedencji miał się więc gdzie wpisać —
`_przejdź` dostaje ciało wraz z rozpiętościami córek,
czyli dokładnie to, o co taki warunek pyta —
i nie żądał rozwinięcia permutacji po to, żeby zostać wypowiedzianym.
Wpisał się mimo to przed rozbiorem, a nie w lesie,
bo warunek pytany o rozpiętości odpowiada raz na wyprowadzenie,
a ten sam warunek rozwinięty odpowiada raz na gramatykę.
Rozwinięcie zostaje przez to wyborem o liczbę czytań, a nie ceną wejścia,
i drugi z dwóch odbiorców tego warunku — luka — czeka po tamtej stronie granicy:
pozycji w napisie nie pilnuje pozycja w ciele
([niżej](#lukę-zmierzono-i-olski-jej-nie-bierze)).

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
Warunek ujemny tej gramatyki płaci więc polem za to,
z czego wszystko obok niego żyje,
i płaci nim na każdy zasięg, o jaki pyta:
osobne pole ma wykluczenie czytania, osobne wykluczenie całej formy
([subset.md](subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)).

Żądanie obecności cechy ucieka temu przecięciu z drugiej strony
i stoi poza `unify` z tego samego powodu.
`niesie` w `olski/grammar.py` mówi, że forma ma cechę nieść,
a przecięcie zbiorów nie ma jak tego powiedzieć:
cecha nieobecna jest pomijana, więc wypisanie wszystkich jej wartości
znaczy dokładnie tyle, co milczenie.
Warunki poza unifikacją są przez to dwa i oba pytają o formę,
a nie o zgodność między dwiema wiązkami cech:
jeden odmawia lematowi, drugi formie, która cechy nie niesie.
Kupuje to klasę, którą tagset rozdziela, a produkcja nie umiała zażądać —
przysłówek odprzymiotnikowy niesie stopień, a pierwotny nie —
i tyle wystarcza, żeby przymiotnik brał jednego z nich
([subset.md](subset.md#naprawę-niesie-tagset-a-formalizm-ją-bierze)).

Rodzaj grupy współrzędnej nie jest symetryczny między członami,
bo polszczyzna wylicza go regułami, których unifikacja nie umie powiedzieć,
więc taka grupa nie niesie tej cechy wcale i `olski/subset.py` mówi to
przy tej produkcji.
Działa to dlatego, że `unify` pomija cechę, której konstytuent nie ma,
czyli tą samą linią, którą nieodmienna część mowy jest niewinna zgodności.
Nieobecność jest tu mechanizmem, a nie dziurą.

Negacja weszła tym kanałem, nie mając ani drugiej własności, ani trzeciej.
Rządzenie nie jest symetryczne — czasownik żąda przypadka od dopełnienia,
a dopełnienie od czasownika nie żąda niczego — i nie rozstrzyga się nad parą,
bo dopełniacz negacji sięga pod bezokolicznik przez łańcuch dowolnej długości
([subset.md](subset.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)).
Przeszła dzięki pierwszej własności, czyli tej, na której stoi unifikacja:
wartości są dwie, przecięcie tylko zawęża,
a kierunek żądania zapisuje się jednostronnie —
ciało z cząstką ogłasza `neg`, ciało bez niej `aff`,
a dopełnienie mówi, przy którym z nich stoi.
Płaci za to ścieżką, którą trzeba przeprowadzić przez każdy konstytuent,
w którym cecha nie idzie od głowy:
`Verb` ogłasza ją z cząstki stojącej obok niego,
a fraza bezokolicznikowa z własną cząstką ma jej nie wypuszczać.
Zgodność takiej ścieżki nie potrzebuje wcale, bo przypadek, liczbę i rodzaj
konstytuent bierze od swojej głowy sam (`olski/grammar.py`).
Pierwsza własność wpuszcza więc rzecz do kanału, a dwie pozostałe rozstrzygają,
czy wjedzie za darmo.

Walencja weszła tym kanałem i wypadła na lokalności.
Rama jest stanem, a nie zasobem, więc pozycji już zajętej nie ma jak odnotować,
a zajęcie zależy od pozostałych córek, a nie od samej pary głowy i zależnego.
Sonda zapłaciła za to samo dwoma polami:
`wymaga` i `zakazuje` w `harness/wiezy.py` mówią o łukach jednej głowy naraz,
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
a ostatnie jest czterema wierszami, które ruszają każdy werdykt,
choć nie ma w nich ani jednej produkcji.
Lista ciał zawęża przez to, czego w niej nie ma,
i tym się od tamtych różni: rośnie z każdą konstrukcją,
nie ma jednego miejsca, w którym da się o nią spierać, i nie mierzy jej nic.

Reszta tej drogi myli się w drugą stronę i dlatego nie waży tyle samo.
Lemat, którego leksykon nie wymienia, dostaje ramę domyślną wraz z jej biernikiem,
a cecha, której forma nie niesie, jest przez `unify` pomijana:
jedno i drugie dokłada czytania, więc zdanie wychodzi wieloznaczne,
a wieloznaczność jest werdyktem, który ktoś przeczyta.
`valid` czyta się inaczej, bo po niego ten tor jest.
Wyjątkiem jest zdanie leksykonu twierdzące — o celowniku i o dopełniaczu —
bo tam milczenie o lemacie pozycję odbiera i zdanie z nią pada
([subset.md](subset.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)).
Odrzucenie nazywa formę, na której analiza stanęła, więc czyta je ten sam ktoś,
a wpis dopisany do leksykonu jest tańszy niż produkcja.

Warunki precedencji zabrały z tej listy pozycję ostatnią,
bo miejsce zadeklarowane raz nie ma jak zostać zapomniane w jednym z ciał,
i zabrały ją z ceną, którą widać: cztery ciała, jakich gramatyka pisana ręką nie miała
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Wyceną ruchu to nie było — tę zrobiła liczba deklaracji zmierzona
[sondą](#podłoże-więzowe-zmierzone-sondą) —
tylko tym, co się przy nim kupiło poza nią.

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
and `Robi` in `olski/skład/składnia.py` asks it about the one lemma it was handed.
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
The membership test itself is `olski/skład/rozbiór.py`,
which reads a parser reading back as a tree of the abstract syntax,
and what it recovers, what it cannot,
and why one reading comes back as several trees
is owned by
[sklad.md](sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma).
The dependency also runs the other way than it first appears:
generation exposes what the grammar *over*generates,
which the parsing side sees only against a treebank.

## Known limits

**Scrambled Polish stays out, permanently.**
A sentence whose noun phrase splits around the rest of the clause
is well-formed Polish that olski will not accept,
and that is a decision rather than a gap waiting for a stage:
see [nieciągłość zmierzono](#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
for what the refusal was priced at.

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
Rule-based machine translation declined under it,
and the reasons are in
[similar-work.md](similar-work.md#the-other-tradition-engineered-wide-coverage-grammars).
Olski is not machine translation but shares the profile,
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
- <https://www.wuw.pl/data/include/cms/Automatyczna_analiza_skladnikowa_Wolinski_Marcin_2019.pdf> —
  Woliński, *Automatyczna analiza składnikowa języka polskiego*, 2019,
  skąd powody odłożenia zdania na pierwszym etapie Składnicy
  i nieciągłości, które Świgra zdejmuje wyborem struktury
