# Design notes

Decisions that have been taken are marked as such;
everything still open lives in [open-questions.md](open-questions.md).
The direction this grammar is grown in, which has no end target, is in
[roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę),
and the linter that stands beside it, whose rule pack is retired,
is in [linter.md](linter.md#co-zamknęło-pakiet-reguł).
The other direction over the same subset —
a tree in, a Polish sentence out —
is in [sklad.md](sklad.md).
The parser, the forest, and what the verdict says over it
are in [parsowanie.md](parsowanie.md).

## What olski is

*Język olski* is *język polski* with the *p* filed off,
along with the parts of Polish that make it hard.
It is an artificial subset of Polish,
designed rather than described,
small enough that a machine can check it
cheaply, deterministically, and explainably.

Olski jest nazwą języka, a *j-olski* jest nazwą projektu wokół niego.
Projekt ma kilka celów i wylicza je [roadmap.md](roadmap.md#cele).
Wszystkie dzielą jeden podzbiór.
Każdy cel bierze zaprojektowaną część polszczyzny.
Żaden nie żąda pełnego pokrycia.
O tym, ile tej polszczyzny wchodzi, rozstrzyga cena mechanizmu.
Jest to wymiana opisana [niżej](#decisions-taken).

The goal on this track is fun and experimentation.
That is the actual goal, not a modest way of stating a real one.
There is no application driving the design,
and any construction may be cut for being boring or annoying.

The scoreboard here is internal consistency:
a grammar that contradicts itself is broken
whether or not it matches usage.
That is a narrower criterion than a linter's,
and the difference is deliberate.
A linter is judged against a corpus of real Polish
because its whole claim is about how Poles actually write,
and [not doing that](linter.md#the-thing-that-makes-or-breaks-it-calibration)
is what closed the rule pack.
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
a płaci deklaracją na każdy symbol z osobna,
w której to samo słowo jest raz identyfikatorem, a raz napisem.
Stałe w `olski/subset/` płacą ją przy symbolach z wywodem,
bo komentarz nad stałą jest jego miejscem.
To, co miał kupić, przychodzi bez niego:
checki w `olski/grammar.py` łapią literówkę w głowie produkcji,
w nazwie cechy, w nazwie zmiennej i w wartości, której więz żąda,
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
A linter needs only analysis
and would have reached for Morfologik instead.
Two dictionaries for two jobs,
and Morfeusz is the one that does both.

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

Każdy z dwóch kierunków ma własny dokument.
Właścicielem pierwszego jest [parsowanie.md](parsowanie.md),
od wyboru parsera po to, co werdykt drukuje.
Właścicielem drugiego jest [sklad.md](sklad.md),
bo rozstrzyga on poziom opisu, a nie parser,
i na żadne z jego pytań ten dokument nie odpowiada.
Ten dokument mówi, ile polszczyzny podzbiór przyjmuje i po jakiej cenie.

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
[the bare verb-initial order](konstrukcje-gramatyczne/orzeczenie.md#the-bare-verb-initial-order-keeps-the-predicative-one-honest)
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
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy)).
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
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)),
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
więc milczenie obiecuje jedno czytanie zdaniu, które ma dwa.
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
[open-questions.md](open-questions.md#znalezisko-wieloznaczności-nie-mówi-czy-ma-ją-też-czytelnik).
Tamto pytanie idzie przy tym w stronę odwrotną niż to:
tam olski melduje wieloznaczność, której czytelnik nie ma, i zgłasza ją jako znalezisko,
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
kilkadziesiąt ciał `rdzeń_względny` w `olski/subset/podrzędne.py`,
po jednym na czoło razy wysunięta rola razy szyk reszty zdania
razy miejsce na okolicznik razy przeczenie,
a role, które te ciała wypełniają, wywodzi
[konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka).
Wysunięte dopełnienie sięga tam tylko do formy osobowej,
więc `Ustawa, którą organ gminy może wydać, jest tania.` nie wyprowadza się wcale.
Cecha przeciągana zastępuje te ciała jedną produkcją:
konstytuent ogłasza w cechach, czego mu w środku brakuje,
luka jest produkcją o pustym ciele,
a zdanie względne wiąże ją ze swoim zaimkiem.
Zdanie względne dostaje wtedy każdy szyk i każde miejsce na okolicznik,
jakie ma zdanie zwykłe, wraz z wyjęciem z głębi,
więc to zdanie się wyprowadza.

**Luka bez napisu nie ma czego przestawiać.**
Ciało, które stawia ją między innym rodzeństwem, wydaje ten sam napis,
a kształt inny, więc [jest to drugie odczytanie](subset.md#co-się-liczy-jako-jedno-odczytanie).
`Reguła, która rozstrzyga, jest tania.` wychodzi dwoma czytaniami zamiast jednego,
bo luka podmiotu wypada raz przed czasownikiem, a raz za nim;
`Polszczyzna, którą ktoś napisał, jest trudna.` wychodzi trzema,
a `Plik, który program zapisuje, jest konfiguracyjny.` sześcioma.
Czytelnik ma w pierwszych dwóch zdaniach po jednym czytaniu, a w trzecim dwa,
więc nadmiar bierze się w całości z miejsca, w które wypada luka.
Nadmiar nie omija zdania, które luka kupuje:
dopełnienie bezokolicznika ma pozycję wypisaną
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze)),
więc luka wypada obok niej i `Ustawa, którą organ gminy może wydać, jest tania.`
wychodzi dwoma kształtami zamiast jednego.

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
i o różnicy mówi [wierszem o konstytuencie](parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań):
`„przed laty kształcili kolejarskich specjalistów” ma 2 odczytania`,
czyli wskazuje zdanie względne i nie mówi, że idzie o miejsce luki w nim.

**Nie kupuje przy tym tej konstrukcji, po którą sięgano.**
Zdanie składowe bez podmiotu, czyli to, co przeciąganie dawało mimochodem,
gramatyka wypisuje sama
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
więc nad 13 035 zdaniami Składnicy pod złotą morfologią
luka przypięta wyciąga z odrzucenia kilka zdań
i jednoznaczność odbiera kilku;
tabelę przejść drukuje polecenie niżej.
Wyjęcia z głębi nie ma przy tym wśród wyciągniętych ani jedno.
Rejestr ustaw odpowiada mocniej: nad jego 4921 zdaniami
([ustawy.md](ustawy.md#co-gramatyka-z-tego-wyprowadza))
luka nie wyciąga z odrzucenia ani jednego zdania i dwa kosztuje,
a zdania o kształcie tamtej ustawy nie ma w tym rejestrze wcale
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)).
Konstrukcja, dla której sięga się po szczebel 2, nie występuje więc
w żadnym korpusie, jaki to repozytorium czyta.

**Zakup jest przy tym zerem, bo bank drzew stawia tę rolę na zaimku.**
Każde z wyciągniętych zdań olski czyta inaczej, niż czyta je drzewo wzorcowe,
i mówi to sonda sama: o rolach zdań nowo przyjętych wypisuje ona `disagrees`
i nic poza tym.
Czyta tak z samego mechanizmu:
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
([werdykt jest zapytaniem o las](parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)).
Roli wypełnionej luką werdykt więc nie nazywa,
tak samo jak nie nazywa roli wypełnionej zaimkiem,
i zostaje cena z akapitu wyżej: rozpiętość pusta nie trafia w żadną złotą.

**Symboli nie ubywa.**
`rdzeń_względny` schodzi do tych ciał, które wysuwają wyrażenie przyimkowe,
a `zdanie_składowe` rośnie za to kilkakrotnie,
bo przeciąganie żąda ciała na każdą córkę, która lukę unosi,
i cała gramatyka rośnie o kilkadziesiąt produkcji;
liczby na dziś drukuje kolumna `produkcji` w wydruku sondy.
Drabina wycenia szczebel 2 na mnożenie się symboli i wycenia trafnie,
tylko że mnożenie wypada na rodzinie zdaniowej, a nie na względnej.

Parser nie kosztował ani jednej zmiany, i tyle drabina obiecała.
Tablica Earleya przyjmuje produkcję o pustym ciele,
a `Node.span` w `olski/parse/czytanie.py` jest wpisywane przy budowaniu właśnie dlatego,
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
Ruch trzyma [todo/](../todo/README.md),
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
a [parsowanie.md](parsowanie.md#earley-wydaje-las-a-glr-zostaje-optymalizacją)
mówi, co po tym przyjdzie.
W warstwie siły rusza się to, co produkcja w ogóle umie powiedzieć,
i [urwisko](#the-cliff-discontinuity) jest miejscem,
w którym ten ruch kosztuje wykładnik,
a nie miejscem, w którym coś jest zakazane.

Środek nie musi też stać na drabinie,
a repozytorium już tak pracuje, więc jest to opis, a nie obietnica.
Czytania, których żadna produkcja nie odbiera, odbiera kod obok gramatyki:
`admissible` w `olski/segmentacja.py` wyrzuca rzeczownik nieodmienny tam,
gdzie ta sama forma czyta się także jako słowo funkcyjne,
a po co, mówi [warstwa-leksykalna.md](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not).
Nieciągłość zaś ma wyjście tańsze niż szczebel, na którym stoi:
Świgra przeciąga przez ciąg o swobodnym szyku jedną lukę
([swigra.md](swigra.md#one-gap-instead-of-a-different-complexity-class)),
co jest odpowiedzią z tier 2 na problem z tier 3.
Odpowiedzią na to, co olski ma przyjmować, nie musi więc być
ani produkcja, ani wyższa klasa złożoności.

Środka nie wybiera się natomiast tam, gdzie fakt rozstrzygający nie stoi w żadnym słowniku.
Orzecznik zgodny jest tego przykładem: czytanie, które trzeba by zdjąć,
rozstrzyga własność przymiotnika, a leksykon walencyjny mówi o czasowniku,
więc ani produkcja, ani warstwa za parserem nie mają czym zapytać
([warstwa-leksykalna.md](warstwa-leksykalna.md#zawężenie-orzecznika-zgodnego-wyceniono-i-decyzji-nie-ma)).

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
Ten sam werdykt dostaje od obu programów mniej niż co trzecie zdanie tej prozy,
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
oraz [interpunkcję zdaniową](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają),
a sonda po swojej stronie ma spójnik i nic poza nim.
Reszta rozejść nie mówi o formalizmie nic i mówi coś o samej sondzie:
liczebnika, formy z leksykonu projektu, rzeczownika odczasownikowego
ani cudzysłowu `harness/polszczyzna.py` nie ma,
a olski ma każde z nich i wyprowadza nimi zdania tego pliku.
Deklaracja stojąca obok gramatyki jest drugim zapisem tego podzbioru,
więc starzeje się po cichu przy każdym dopisaniu do olskiego,
produkcji czy wiersza leksykonu.
Czy deklaracje mają iść za produkcjami, czy sonda ma się skasować,
trzyma [`todo/`](../todo/README.md); dopóki to nie zapadnie,
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
i dopiero rozwinięcie robi z nich kilkadziesiąt ciał `zdanie_składowe`,
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
Jest to ta sama informacja, którą `harness.pomiar` liczy jako bloker,
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
[Leksykon](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej) sięga do tego
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
[Walenty is that source](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej),
and `olski/walencja.py` is what each direction reads it through:
the parser turns it into the valency classes its productions need,
and `Robi` in `olski/skład/składnia.py` asks it about the one lemma it was handed.
The two ask different questions of it, which is why what they share is the
lexicon rather than an answer.

The **grammar** is not, and binding the two costs more than it buys.
Generation never meets the problem the grammar exists to solve:
agreement stops being a constraint to reconcile and becomes a value to compute,
as [sklad.md](sklad.md) says,
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
([linter.md](linter.md#co-zamknęło-pakiet-reguł)).

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
