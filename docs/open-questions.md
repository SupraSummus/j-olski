# Open questions

Decisions not yet taken.
The point of writing them down
is that none of them get made by accident.

Questions are grouped by which track they block.
Only the first group blocks what is being built.

## Settled

- What is being built is a parser of a designed subset of Polish,
  which hands ambiguity back instead of resolving it,
  and it exits when this repository's README derives, one reading per sentence.
  See [design-notes.md](design-notes.md)
  and [roadmap.md](roadmap.md#celem-toru-jest-to-readme).
- A style linter for Polish, scoped to technical documentation,
  is the optional track beside it and keeps its own plan.
  See [linter.md](linter.md).
- Olski is as close to Polish as possible,
  and a proper subset of it.
- No rule ships without a measured false-positive rate
  on good human Polish.
- The tool is a linter, not a detector,
  and must not be described as one.
- Two morphological dictionaries for two jobs.
  The grammar track needs generation and only Morfeusz does it,
  which leaves the linter track free to take Morfologik,
  the analyser LanguageTool is built on.
  See [design-notes.md](design-notes.md#decisions-taken).

Further grammar-track decisions are recorded in
[design-notes.md](design-notes.md#decisions-taken).

## Grammar-track questions

The linter runs without any of them answered,
which is what makes it the track that can be left alone.

### The big fork: may olski scramble

Polish permits left-branch extraction that splits a noun phrase
around the rest of the clause,
as in `Jakie Jan czyta książki?`.
Admitting that means discontinuous constituents,
which means leaving the context-free tier
for LCFRS, MCFG, or TAG,
and moving from cubic parsing to sixth power at fan-out two.
Those and not the hierarchy's own type 1,
which keeps named productions
and gives up the derivation tree and the polynomial parser:
see [the ladder is not the Chomsky hierarchy](design-notes.md#the-ladder-is-not-the-chomsky-hierarchy).

This is not a difficulty gradient.
It is the one place where the cost curve jumps by an exponent.
See [the cost ladder](design-notes.md#the-cost-ladder).

Refusing it keeps everything at tier 2.
Every other decision below is cheap next to this one.
It should probably be answered by measurement rather than taste:
find out what fraction of real Polish sentences need it,
and what admitting it costs the sentences that already have one reading,
before paying for it.
[Making the trade measurable](design-notes.md#making-the-trade-measurable)
owns why that second count exists.

One parser of Polish reaches common discontinuity without paying.
Świgra threads a single gap through its free-order sequence
and forbids subjects from extracting,
which is a tier-2 answer to a tier-3 problem;
what it gives up is the measurement nobody has taken.
See [swigra.md](swigra.md#one-gap-instead-of-a-different-complexity-class).

### The rest of the subset

Each row is a real fork, not a difficulty level.
The `closeness` column notes which option
serves the settled goal of resembling Polish.

| Area | Cheap option | Expensive option | Closeness favours |
| --- | --- | --- | --- |
| Word order | Fix subject-verb-object | Dominance plus precedence constraints | Expensive |
| Subject | Require an overt noun phrase | Allow pro-drop | Expensive |
| Numerals | Exclude entirely | Full numeral agreement fictions | Expensive, but defer |
| Negation | Clause-wide `nie`, no case shift | Genitive of negation with propagation | Expensive |
| Clauses | Main clauses only | `że` and `który` subordination | Expensive |
| Coordination | Same-category only | Unlike categories, gapping | Unresolved |

Closeness to Polish argues for the expensive column nearly everywhere,
which is not a reason to build it all at once.

Numerals deserve a note:
they are extremely common in real Polish
and they are also a self-contained module,
so they are a good candidate
for being deferred rather than excluded.

### Kryterium wyjścia toru żąda jednoznaczności od zdania, które jej nie ma

`Cały wywód prowadzi docs/linter.md.` stoi w README i ma dwa czytania,
SVO i OVS, bo notacja jest nieodmienna, a `wywód` ma biernik równy mianownikowi.
Zdanie naprawdę nie mówi, co tu prowadzi co,
i [subset.md](subset.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)
trzyma to jako cenę przyjętą świadomie.

Trzy rzeczy, każda obroniona osobno, nie mogą stać razem.
Kryterium wyjścia toru żąda jednego czytania dla każdego zdania README
([roadmap.md](roadmap.md#celem-toru-jest-to-readme)).
README stoi, a rusza się gramatyka, bo przepisanie go pod podzbiór
kosztowałoby to, po co ten plik jest
([CLAUDE.md](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).
A olski wpuszcza czytania, które polszczyzna naprawdę ma, OVS wśród nich,
bo deklaracja, że pierwsza grupa imienna jest podmiotem,
czytałaby się jednoznacznie tylko temu, kto zna konwencję
([subset.md](subset.md#validity-is-uniqueness-not-just-derivability)).

Czwarte wyjście jest tym, którego szuka to pytanie:
że kryterium wyjścia ma wyjątek dla zdania wieloznacznego w polszczyźnie,
czyli mierzy nie „jedno czytanie”, a „jedno czytanie tam, gdzie czytelnik ma jedno”.
Kosztem jest werdykt, którego nie wyda program:
dla każdego zdania spornego ktoś musi powiedzieć, ile czytań ma sam,
a wtedy kryterium wyjścia przestaje być czymś, co drukuje polecenie.
Zdanie olskie ma jedno czytanie z definicji podzbioru,
więc to nie olski się tu zmienia, tylko to, co README ma o sobie dowodzić.

Rozstrzyga to jedno zdanie, a klasy są dwie.
Obie są szerokie liczone pozycjami i obie wąskie liczone czytelnikiem,
i to ta różnica jest tym, co pytanie dostaje niżej.
Synkretyzm mianownika z biernikiem ma w polszczyźnie każdy rzeczownik rodzaju m3
i nieodmienny każdy,
więc każde zdanie przechodnie o dwóch takich grupach imiennych tu wraca.
Druga klasa z tamtym zdaniem nie ma nic wspólnego i jest od niej większa:
wyrażenie przyimkowe stojące tuż za grupą imienną
dochodzi do niej albo do czasownika przed nią,
a olski nie wybiera ani jednego, ani drugiego
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
więc zdanie z taką pozycją ma dwa czytania z tego samego powodu co tamto.

Ile ich jest, pokazuje pomiar rejestru, a nie werdykt nad zdaniem.
Gramatyka odrzuca w tym rejestrze prawie każde zdanie,
więc zdanie wieloznaczne w polszczyźnie do werdyktu w ogóle nie dochodzi,
i widać je dopiero wtedy, gdy pozycje liczy się w tekście.
Klony korpusu audytowego stoją w
[audit-corpus.md](audit-corpus.md#the-list), a potem:

```sh
python3 -m harness.markdown ksef-docs --into proza/ksef
python3 -m harness.markdown rit-dokumentacja --into proza/rit
python3 -m olski.wieloznaczność proza/ksef/*.txt proza/rit/*.txt
```

Pozycję którejś z dwóch klas niesie tam 734 z 1 183 zdań, czyli 62.0%:
przyłączenie 56.1%, synkretyzm 18.0%,
a 271 zdań niesie samych przyłączeń dwa albo więcej,
czyli czytań ma po cztery i wzwyż.
To samo polecenie puszczone nad prozą tego repozytorium
daje udział niższy, bliższy połowie niż dwóm trzecim,
a README nie odstaje w nim od reszty;
liczby stąd nie stoją tu zapisane,
bo rusza je przeredagowanie zdania, a nie zmiana w kodzie.

Populacją to jest, a odpowiedzią nie, i czytanie jej zmienia wniosek.
`--przykłady 12` bierze próbkę rozrzuconą po całej liście trafień,
więc czyta się ją drugi raz po tym samym.
Dwadzieścia cztery zdania z niej, po dwanaście na klasę, wychodzą tak:
ani jedno nie zostawia czytelnika z dwoma rozumieniami,
a dwa zostawiają go z wahaniem —
`Dane te obejmują zarówno aktywne, jak i historyczne certyfikaty`,
gdzie obie grupy są mnogie i każda mogłaby obejmować drugą.
Reszta ma dwa drzewa i jedno rozumienie:
`kompendium wiedzy dla deweloperów` przyłącza się do rzeczownika,
bo przy czasowniku nie znaczyłoby nic innego,
i tak samo `skrót SHA-256 w Base64`.
Jest to jedna osoba nad dwudziestoma czterema zdaniami, a nie pomiar,
i tyle z tego wynika.

Wniosek wychodzi odwrotny do tego, na co 62.0% wygląda.
Wyjątek, którego to pytanie szuka, objąłby zdania rzadkie, a nie większość rejestru,
bo zdań, w których czytelnik naprawdę ma dwa czytania, jest w tej próbce tyle co nic.
Liczba wycenia natomiast co innego, o co nikt tu nie pytał:
jak często olski melduje wieloznaczność, której czytelnik nie ma.
Nad korpusem audytowym jest to prawie każde zdanie z pozycją przyłączeniową.

Liczba jest przy tym górnym oszacowaniem i myli się w jedną stronę.
Grupą imienną jest tam ciąg form, a nie węzeł,
więc apozycja liczy się jak dwie grupy —
`podpis CERTYFIKAT`, `Element report` — choć jest jedną,
a wyrażenia, którego czasownik żąda swoim schematem,
ten pomiar od stojącego do wyboru nie odróżnia.
Podnosi ją też każde czytanie, które słownik ma, a polszczyzna nie:
`synkretyzm [go, gov.pl]` stoi na zaimku czytanym jako gra,
czego wykluczenie ze słownika nie sięga.
Osobno stoi to, co dokłada ekstrakcja:
nagłówek sklejony ze zdaniem za nim daje parę, której nikt nie napisał,
i należy to do [extraction.md](extraction.md), a nie tutaj.
Wszystkie te klasy podnoszą populację,
a wniosek wyżej idzie w tę samą stronę co one, więc żadna go nie odwraca.
Zbiera się ich przy tym najwięcej pod synkretyzmem,
więc to jego 18.0% jest z dwóch liczb tą miękką.

### Olski melduje wieloznaczność, której czytelnik nie ma

Pytanie wyżej zostawia po sobie drugie i to ono jest droższe.
Skoro pozycja przyłączeniowa stoi w większości zdań korpusu audytowego,
a czytelnik ma nad nią jedno rozumienie,
to zdanie odrzucone przez własność jednoznaczności
płaci za dwuznaczność, której nikt poza parserem nie miał.
Liczby i próbkę trzyma pytanie wyżej, i to ono jest ich właścicielem.

Decyzji o [przyjęciu kosztu](subset.md#dlatego-olski-przyjmuje-koszt) to nie przewraca,
bo tamta stoi na czym innym.
Bank drzew mówi, że żadne przyłączenie nie jest domyślne,
czyli że wyboru między nimi nie zgadnie żadna konwencja,
a nie że czytelnik ten wybór widzi.
Obie rzeczy są prawdziwe naraz
i dopiero razem mówią, ile ta decyzja kosztuje nad rejestrem,
bo tamten pomiar wzięto nad bankiem drzew, a ten nad dokumentacją.

Wyjścia z tego nie ma w gramatyce i to jest w tym pytaniu najtrudniejsze.
Te zdania rozstrzyga znaczenie —
`kompendium wiedzy dla deweloperów` nie przyłącza się do czasownika,
bo nic by tam nie znaczyło —
a znaczenia unifikacja nie dosięga.
Zostają więc trzy odpowiedzi i żadna nie jest tania.
Pierwsza: własność jednoznaczności zostaje, jak stoi,
a kryterium wyjścia toru przestaje być osiągalne nad tym README,
co czyni je kryterium innego rodzaju, niż jest opisane.
Druga: wraca [wyjście drugie z etapu 1](subset.md#dlatego-olski-przyjmuje-koszt),
czyli domyślne przyłączenie, odrzucone tam za to, że myli się dwa razy częściej,
niż trafia; wobec tego pomiaru trzeba by je ważyć inaczej niż wtedy,
bo po jednej stronie stoi pomyłka w drzewie, której czytelnik nie zauważa,
a po drugiej odrzucenie zdania, które przeczytał raz.
Trzecia: warstwa rozstrzygająca przyłączenie poza gramatyką,
czyli to, czego olski nie ma i czego żaden etap nie planuje.

Do przeczytania jest najpierw to, czy próbka wyżej się broni.
Dwadzieścia cztery zdania przeczytane przez jedną osobę
są podstawą wystarczającą, żeby pytanie postawić,
i za wąską, żeby na nim stanąć.

### Czy jednoznaczność prefiksu mierzy czytelność

Hipoteza: tekst czyta się tym łatwiej,
im mniej rozbiorów dopuszcza każdy jego kolejny prefiks.
Czytelnik idzie słowo po słowie i nie wraca,
więc prefiks, który rozkłada się na kilka sposobów,
zostawia go z kilkoma rozbiorami naraz,
dopóki dalsze słowo ich nie unieważni.

Mierzy to co innego niż
[kryterium jednoznaczności](subset.md#validity-is-uniqueness-not-just-derivability),
i obie wielkości rozjeżdżają się w obie strony.
`Koszt samej szynki przewyższa koszt szynki z dodatkami.`
czyta się gładko i ma kilka czytań,
bo koszt płaci się przy rozumieniu, a nie przy czytaniu,
i płaci niewidocznie, skoro czytelnik nie wie, że wybrał.
Zdanie ze ścieżką ogrodową jest odwrotne:
jedno czytanie na końcu i długi prefiks, który trzymał inne.
Kryterium stoi więc na poprawności,
a hipoteza go nie podpiera i stawia obok niego drugą wielkość.

Trzy rzeczy trzeba w niej zaostrzyć, zanim da się ją zmierzyć.

Liczba rozbiorów nie jest kosztem pamięci.
Wykładniczo wiele czytań mieści się
w wielomianowym lesie ze współdzielonymi węzłami,
więc prefiks z dwudziestoma czytaniami różniącymi się jednym przyłączeniem
to jedna decyzja nierozstrzygnięta, a nie dwadzieścia.
Liczy się liczba takich decyzji,
czyli to samo rozróżnienie, które
[subset.md](subset.md#co-się-liczy-jako-jedno-czytanie) robi dla całego zdania.

Rozbiory nie są równoprawdopodobne.
Prefiks, którego jedno czytanie bierze prawie całe prawdopodobieństwo,
nie obciąża nikogo, choćby reszta była liczna.
Policzalną wersję hipotezy pole ma więc w postaci rozkładu, a nie zbioru:
*surprisal* Hale'a mierzy, ile prawdopodobieństwa traci przy kolejnym słowie
ta część rozbiorów, którą to słowo unieważnia,
i przewiduje z tego czasy czytania.
Wyjaśnienie konkurencyjne liczy pamięć wprost,
bliżej tego, jak hipoteza jest tu postawiona:
u Gibsona koszt bierze się z odległości między członami zależności,
czyli z tego, jak długo człon czeka na swoje dopełnienie.
Która z dwóch wielkości niesie tu więcej, rozstrzyga pomiar.

Kosztuje nie to, *że* prefiks był wieloznaczny,
tylko jak długo taki został
i czy rozstrzygnięcie unieważnia czytanie, które było preferowane.
Wieloznaczność ginąca na następnym słowie jest darmowa,
a to jest ten sam przypadek, który
[glr-in-practice.md](glr-in-practice.md#what-this-does-and-does-not-tell-us-about-glr-for-olski)
nazywa lokalnym i zakotwiczonym.
Gdyby hipoteza się utrzymała,
dobór kotwic przestałby być dźwignią samego kosztu parsowania.

Rozstrzygają ją czasy czytania nad polszczyzną,
zestawione z krzywą wieloznaczności prefiksu.
Sprawdzone są dwa korpusy okulograficzne i żaden nie wystarcza.
MECO nie ma polszczyzny ani w pierwszej fali, ani w drugiej.
MultiplEYE wymienia polski wśród dwudziestu siedmiu języków,
a czy wyszły jakiekolwiek dane, jest do sprawdzenia:
strona projektu nie mówi o żadnym wydaniu.

Druga przeszkoda stoi po stronie olskiego i dotyczy doboru próby.
Krzywą prefiksu umie policzyć tylko gramatyka,
a policzy ją dla tych zdań, które wyprowadza, i dla żadnych innych.
Próbą jest więc to, co gramatyka obejmuje,
a obejmuje podzbiór dobrany przez wykluczanie konstrukcji trudnych do rozebrania —
[subset.md](subset.md#what-it-does-not-cover-yet) wymienia je,
[corpus.md](corpus.md#the-measurement) mierzy, ile polszczyzny zostaje —
czyli próba jest przesiana po tej samej własności, którą hipoteza bada.

Regule linterowej odpowiedź nie da nic przed gramatyką,
bo miara po prefiksach potrzebuje rozbioru,
czyli [najgłębszego poziomu analizy](linter.md#how-deep-does-each-rule-have-to-see).
Torowi gramatycznemu daje drugie uzasadnienie kryterium jednoznaczności
albo nie daje żadnego.

### What the author writes

Three architectures, described at length in
[sklad.md](sklad.md#three-architectures).

1. A typed abstract syntax tree
2. Near-Polish text that gets parsed and validated
3. An unambiguous surface DSL that reads like Polish
   and elaborates into the AST

The working preference was the third.
The predictive-editor finding from the controlled-language literature
substantially rehabilitates the second:
with a look-ahead editor
the author writes something very close to Polish
and cannot produce an invalid sentence,
so the bad-diagnostics objection disappears.
See [sklad.md](sklad.md#the-predictive-editor-changes-this).

It decides whether the primary interface
is a batch checker over files
or an incremental one over a cursor.
Those are different programs.

### The round-trip guarantee

Restated as asymmetric:
tree to text is a function,
text to tree is a relation,
and the test is that the original tree
appears somewhere in the forest.

Still open:
whether to additionally rank the forest
and require the original tree to come out on top.
That is stronger,
and it means building a disambiguation preference,
which is where deterministic explainable systems usually stop being either.
Current inclination is not to.

A third option, cheaper than either ranking or resolving:
abstain when the forest holds more than one reading,
and treat the count itself as the confidence measure.
See [glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
for a system that does exactly this and nothing more,
including the one thing it gets wrong —
counting parses rather than *distinct* readings,
so an optional-whitespace rule
makes it abstain on lines it understood perfectly.

### How the grammar is authored

Grammar and lexicon should be one declarative source
feeding both the parser and the generator.
That source needs a format.

Open sub-questions:
a bespoke grammar file with its own parser,
an embedded DSL in the host language,
or literate prose with rules extracted from fenced blocks.
The repository already uses semantic line breaks for prose,
which makes the third option less absurd than it sounds.

Whatever the format,
[glr-in-practice.md](glr-in-practice.md#grammar-as-data-not-as-dsl)
argues the parser must accept a grammar as data,
because a precedence preprocessor generates productions
rather than writing them.

Świgra takes the first option and compiles it,
which is evidence that a bespoke file with its own compiler
can carry a grammar of Polish at full scale.
That file also carries its test cases,
a job the three options above are silent about:
see [swigra.md](swigra.md#the-grammar-carries-its-own-examples).

### What the output is

Plain text, Markdown, LaTeX, or HTML.
If a real typesetter is in the picture
then *skład* is literal
and the compiler needs a backend layer.

### Whether to publish a PENS coordinate

Applies only if the grammar track produces
an actual controlled natural language.
Kuhn's scheme classifies controlled languages,
and a linter is not one,
so this question belongs to this track alone.

The scheme would let olski state its position
on the same four axes as a hundred other controlled languages.
Doing so honestly requires
an exact and comprehensive language description,
which is the Simplicity axis by definition.
Committing to that is committing to write the spec properly.
It might be the most valuable artifact the grammar track could produce,
or an obligation that kills the fun.
Undecided.

## Linter questions

These block the optional track and nothing above it.

**Delivery route.**
Standalone tool with its own rule format,
a Vale-compatible style,
or LanguageTool XML rules over Morfologik.
The last inherits an installed base and a Polish morphology layer;
the first inherits nothing and owes nothing.
The Vale route inherits a third thing that
[the markup boundary](rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives)
turns from a convenience into a step somebody has to take:
Vale reads Markdown and AsciiDoc itself,
so a style delivered through it gets prose separated from apparatus for free
where a standalone olski asks for it in front.
What it charges for that is depth.
Vale's tagger ships an English model,
so a Vale style reaches tier A in Polish and stops:
see [prose-linters.md](prose-linters.md#vale-is-the-architecture-to-study).
So the answer decides whether the morphology work happens at all,
which is why [the roadmap](roadmap.md#milestone-4-the-delivery-decision)
puts the decision in front of that work rather than at the end.

**Rule provenance policy.**
Every rule needs a justification,
and justifications anchored to Polish style norms
outlive justifications anchored to model fingerprints.
Open question is whether fingerprint rules are admitted at all,
and if so how they are dated and retired.

**Corpus sourcing.**
Which human Polish counts as the good side of the pair.
The human side determines everything the rules learn,
and the rules impose their own constraints on the answer.
A threshold is a point in this distribution,
so the register a pack is scoped to has to be in the corpus
or the threshold is read off the wrong prose.
The rules against anglicisms and calques
need to know whether the Polish technical documentation available
was written in Polish or translated into it,
since a translated baseline licenses exactly the calques they flag.
And the good side may be two corpora rather than one:
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
argues a typographic rule measured against typeset prose
is measured against nothing,
so those rules want Polish caught at the stage a linter runs at
while the rate rules want prose somebody edited.

[corpora.md](corpora.md) surveys what is obtainable against those constraints,
and [three of its findings](corpora.md#what-the-survey-settles)
narrow the question rather than close it.
The register is nearly absent from the corpora that exist,
so a distribution over Polish technical documentation is assembled or it is nothing.
Provenance is recorded only in the translated pool,
where the file format keeps the English beside the Polish,
which makes Polish-first origin a property of how a corpus is gathered.
And the stage a typographic rule needs is not the typesetter's:
NKJP's own text layer carries more straight quotation marks than Polish ones,
so a corpus build renormalizes characters as thoroughly as typesetting does.

The survey recommends two human corpora rather than one —
documentation cloned from version control for the rules that audit their hits,
and edited original expository Polish for the rules that report a rate —
and [the composition](corpora.md#the-composition-this-argues-for)
holds the parts, the proportions and the reason each share is capped where it is.
It also recommends an answer to the generated half.
Śmigiel, the PolEval 2025 dataset, is generated for the purpose,
with no editing pass in the pipeline its authors describe,
which is what
[generated-polish.md](generated-polish.md#what-this-corpus-cannot-support)
asks of that half,
so a corpus edited against style detectors need not serve as it
and stays the harder case rather than the sample.

What is left to decide is whether to pay for the assembly,
and that is two decisions rather than one,
because the recommendation is two corpora and they cost different amounts.

The cheap alternative is to measure over Śmigiel and Polish Wikipedia as they are
and state the register assumption out loud,
which produces numbers sooner
and produces them over prose nobody claims is in the target register.
It answers for the distribution corpus and not for the audit one.
Register is what that trade concedes,
and register is the binding constraint on only one of the two:
a rule whose hits get read wants a single stage of production,
and Śmigiel's human half is thirteen sources with a stage each:
its Filmweb slice runs 5,672 straight quotation marks against 38 Polish ones
and its Wikipedia slice runs the other way,
so a share of hits taken over the whole measures the mixture.
The audit corpus has no cheap version for that reason,
and it is the cheaper of the two to assemble anyway,
being a list somebody fills rather than a distribution somebody balances.

**Whether hits get annotated.**
A false discovery rate needs a human deciding, hit by hit,
whether the rule caught a defect or a good sentence,
where a firing rate only counts.
The one published evaluation in the field rests on that reading,
and [prose-linters.md](prose-linters.md#what-beating-them-takes)
records the assumption under which a rate on human Polish stands in for it.

What is undecided is narrower than it first looks.
The assumption is vacuous for the rules a typesetter's corpus
has already been cleaned of,
so their hits have to be read whatever else is decided,
and [linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
argues they are the cheap ones to read.
The question is what happens to the rest:
whether olski pays for annotating them too,
or ships their rates as the estimate and names the assumption.

A third source is worth pricing before either is chosen.
Suppression, undecided in [rules.md](rules.md#not-yet-decided),
would have a reader marking a named rule as wrong at a named site,
which is the annotation someone else would be paid to produce.
It is not a sample, because a hit suppressed out of impatience
leaves the same mark as one suppressed for being false,
so it can feed an estimate and cannot settle one.

**Whether a measurement may need a language model.**
The README promises judgements produced as in a compiler,
not as in a language model,
and every rule shipped so far keeps that promise.
The surprise metric in
[fiction.md](fiction.md#the-evaluation-trap) does not:
it scores how unexpected a text is under a model.
It keeps the determinism —
at temperature zero the same input scores the same twice —
and it is the cheapest measurement in that survey to redo on Polish,
wanting human Polish, generated Polish and one model to score both,
with no annotators and no panel.
What it loses is the explanation.
A surprise score arrives without a rule behind it
and cannot say what to change,
which may be tolerable for a number that calibrates a rule set
and not for a finding shown to a writer.
Against it either way:
depending on a model means depending on a particular model,
which dates the way a fingerprint rule dates.

**How registers are configured.**
Rules belong to packs and packs belong to registers.
Whether a document declares its register,
or the tool guesses,
or the user picks a pack explicitly.

**Sentence-length variance in technical Polish.**
Which side of the spread is the defect is read two ways here.
[The candidate inventory](rule-inventory.md#structural-and-statistical-tier-a-with-sentence-splitting)
files low variance as the tell in technical documentation,
which asks a rule for a floor.
[fiction.md](fiction.md#what-this-means-for-olski)
reports the literature measuring the metric in both registers,
with fiction wanting range where technical documentation wants uniformity,
and a register that wants uniformity
is one where a ceiling is the flag.
Both readings hold at once if the sign never changes and only the number does:
the tell would be uniformity below a *human technical* norm,
with that norm sitting lower than a literary one.
That is a reading and not a measurement,
and a human technical baseline is what settles it.
`length-variation` takes a floor and a ceiling
so that the answer is a rule's parameter rather than a rewrite.

**Whether fiction gets a pack at all.**
Several metrics work for both registers
once the threshold is a pack's parameter rather than a check's,
which is cheap.
The rest of the fiction problem is not linting,
and is recorded as a wish rather than a plan.
See [linter.md](linter.md#and-fiction),
and [fiction.md](fiction.md#what-this-means-for-olski)
for which defects a pack could reach and which sit below any rule.

## Shared questions

**Implementation language.**
Both tracks need one, and it need not be the same one.

- The linter wants whatever makes rules-as-data pleasant
  and has a usable Morfologik binding.
  LanguageTool is Java, which matters
  only if the delivery route goes through it.
- The grammar track wants good algebraic data types
  and pattern matching for writing Earley and a unifier,
  and Morfeusz has usable Python and C++ bindings.
- The project is for fun,
  so enjoying the language matters more than it usually would.

## Sources

- <https://aclanthology.org/N01-1021/> —
  Hale, probabilistyczny parser Earleya jako model psycholingwistyczny,
  gdzie definiuje się *surprisal*
- <https://www.sciencedirect.com/science/article/abs/pii/S0010027707001436> —
  Levy, rozumienie składni oparte na oczekiwaniu
- <https://tedlab.mit.edu/tedlab_website/researchpapers/Gibson_2000_DLT.pdf> —
  Gibson, teoria lokalności zależności
- <https://www.nature.com/articles/s41597-025-05453-3> —
  druga fala korpusu MECO i trzynaście języków, które obejmuje
- <https://www.cl.uzh.ch/en/research-groups/digital-linguistics/research/MultiplEYE.html> —
  MultiplEYE i lista jego dwudziestu siedmiu języków
