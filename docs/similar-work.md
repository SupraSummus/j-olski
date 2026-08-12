# Similar work

Olski is not a new idea.
It is a new point in a space
that people have been exploring since roughly 1930,
and the field has enough measured results
that ignoring them would be a waste.

This file is the landscape.
[prior-art.md](prior-art.md) is the narrower list
of tools and resources olski might actually consume.

## The field has a name and a survey

The umbrella term is **controlled natural language**:
a subset of a natural language,
restricted in grammar and vocabulary,
to reduce or eliminate ambiguity.

The reference work is
Tobias Kuhn's *A Survey and Classification of Controlled Natural Languages*,
Computational Linguistics 40(1), 2014.
It catalogues **100 English-based controlled languages**
from 1930 to publication,
and it is the first thing to read.

Kuhn sorts them by goal into three types:

| Type | Goal | Count |
| --- | --- | --- |
| C | Comprehensibility for human readers | 45 |
| T | Translatability, usually machine-assisted | 22 |
| F | Formal representation and automated reasoning | 54 |

C and T overlap heavily.
Neither overlaps much with F.
Over 90 percent are written rather than spoken languages.

## PENS, and why it matters here

Kuhn classifies each language on four dimensions,
each with five levels:
**Precision**, **Expressiveness**, **Naturalness**, **Simplicity**.
English sits at P1E5N5S1,
propositional logic at P5E1N1S5,
and controlled languages fill the space between.

The definition of the Simplicity dimension is the interesting part.
It is the number of pages
needed to describe the language exactly and comprehensively,
such that a skilled grammar engineer
could implement a correct and complete parser from the description.
Not learnability, not Chomsky-hierarchy complexity:
implementation cost.

That means the tradeoff this project intends to make,
parser complexity against the number of represented structures,
is the S-versus-E plane of an existing, populated, measured scheme.
Olski can be given a coordinate
on the same chart as a hundred other attempts.
It should be.

### Where olski aims

This positioning describes the
[grammar track](design-notes.md),
which is the only part of the project
that would be a controlled natural language at all.
The linter is a checker, not a language,
and has no PENS class.
The S-versus-E reading below still applies to it,
because implementation cost against coverage
is the same trade under a different name.

Averaged by type, the field splits into two clusters:

| Cluster | P | E | N | S |
| --- | --- | --- | --- | --- |
| C and T | 2.0 | 4.3 to 4.8 | 4.7 to 5.0 | 1.1 to 1.2 |
| F | 4.4 | 2.3 | 3.8 | 3.2 |

The C and T languages are mostly industrial and domain-specific:
natural and expressive,
imprecise,
and impossible to describe compactly.
The F languages are mostly academic:
precise and compactly describable,
at a real cost in naturalness and expressiveness.

Only 25 of the 625 possible PENS classes are occupied at all.

Olski wants high naturalness, because it should be close to Polish,
together with high precision, because it should be deterministically checkable.
That combination is the sparse corner,
and the survey's numbers explain the sparsity:
it is paid for in Simplicity,
which is to say in implementation cost.
This is the trade the project has already chosen to make.
Choosing it knowingly, with a coordinate system to report position in,
is better than stumbling into it.

## Does it work

Kuhn's evaluation survey is the answer to
what people actually say about controlled languages,
and it is more positive than the reputation of rule-based language technology
would suggest.

For comprehensibility:
AECMA Simplified English significantly improved text comprehension,
with the largest effect on complex texts and non-native readers
(Shubert et al. 1995; Chervak, Drury, and Ouellette 1996).
Other studies pointed the same way without reaching significance
(Stewart 1998).

For translation:
MCE was reported to give a five-to-one gain in translation time
(Ruffino 1982).
PACE made post-editing three to four times faster
(Pym 1990).
CLCM reduced post-editing time by about 20 percent
(Temnikova).

For formal representation:
CLOnE's interface beat a conventional ontology editor on usability
(Funk et al. 2007),
and ACE was easier and faster to understand
than a standard ontology notation
(Kuhn 2013).
Positive usability results are also reported
for GINO, CLEF, CPL, PERMIS, and Rabbit.
Rabbit's comprehensibility results were mixed
(Hart, Johnson, and Dolbear 2008).

## Two findings that should shape olski

### The habitability problem

A language is *habitable*
if its users can express themselves
without straying outside its boundaries.
The standing critique of controlled languages
is that for any real subject matter
the set of appropriate sentences is impossibly large,
so users cannot perceive where the fence is
and discover it only by being rejected.

This is precisely the failure mode
that "as close to Polish as possible" invites.
The closer olski gets to Polish,
the harder it becomes for an author to feel the boundary,
and the more often a perfectly good Polish sentence
gets refused for reasons that feel arbitrary.

The field's answer is the **predictive editor**.
AceWiki shows, step by step,
which words and phrases are syntactically possible
at the current position in the sentence.
That inverts the problem:
rather than writing text and receiving errors,
the author is never able to write something invalid.

It also dissolves a worry recorded in
[sklad.md](sklad.md#three-architectures),
that chart parsers give unusable diagnostics.
With look-ahead there are no diagnostics to give,
because there are no errors.
For a project whose whole claim
is cheap, deterministic, explainable checking,
this is the most important architectural idea in the literature.

### The word "subset" is usually a lie

Kuhn notes that the term is misleading:
most controlled languages are not proper subsets of their base language.
They add notation,
or deviate from natural grammar and semantics
in small ways.

Olski's framing is that it is genuinely a subset of Polish.
That is a stronger commitment than most of the field makes,
and it forbids helper notation in the surface form.
Every olski sentence must be a Polish sentence.
Worth holding deliberately rather than discovering later.

## Named languages worth knowing

**Human-oriented.**
ASD-STE100 Simplified Technical English,
descended from AECMA Simplified English,
built in the 1980s by the European aerospace industry
for aircraft maintenance manuals readable by non-native speakers,
since spread to defence, rail, automotive, oil and gas, and medical devices.
Ogden's Basic English.
Voice of America's Special English.
Caterpillar Fundamental English and Caterpillar Technical English.
Plain Language.
The spoken outliers,
SEASPEAK and ICAO phraseology,
almost all of governmental origin.

**Machine-oriented.**
Attempto Controlled English,
a subset of English translated unambiguously into first-order logic
by way of Discourse Representation Structures,
with a parser, a reasoner, a Protégé plug-in, an OWL verbaliser,
and the AceWiki predictive editor.
PENG.
Common Logic Controlled English.
For ontology authoring:
CLOnE, and Rabbit as its more expressive successor from Ordnance Survey,
and Sydney OWL Syntax.
For business rules:
SBVR Structured English, and RuleCNL.

## The other tradition: engineered wide-coverage grammars

Separate from controlled languages,
there is a large body of hand-built grammars
that aim to describe a real language rather than restrict it.
This is the honest comparison
for anything claiming to be close to Polish.

**Grammatical Framework**
provides resources for more than 40 languages
over a shared abstract syntax,
with reversible grammars,
and has explicitly scaled itself
from controlled languages toward robust pipelines.

**DELPH-IN**, the HPSG tradition:
the English Resource Grammar
parses roughly 94 percent of well-edited English
while refusing sentences impossible in English.
The Grammar Matrix is a starter kit
that produces a new language's grammar
from a typological questionnaire,
which is a striking answer to
"how do you start a precision grammar for language X".

**LFG, ParGram, and XLE**,
and for Polish specifically POLFIE,
whose c-structure derives from GFJP2,
the same grammar behind the Świgra parser,
which in turn annotated the Składnica treebank.

**Rule-based machine translation**,
Apertium and its ancestors.
Its decline is instructive:
coverage brittleness,
heavy labour cost per language pair,
and blindness to context.
It survives where the language pair is closely related.
Olski is not machine translation,
but it shares the labour profile,
and the mitigation is the same:
narrow the problem until hand-written rules are enough.

**Reversible grammar** is its own literature,
which matters because
[the round-trip invariant](design-notes.md#the-round-trip-invariant)
is not an original idea.
See Strzalkowski's *Reversible logic grammars
for natural language parsing and generation* (1990),
the 1991 ACL workshop he chaired,
and Dymetman's *Inherently Reversible Grammars*.

## Generowanie rozdziela się poziomem wejścia

Dwie tradycje wyżej czytają tekst, który ktoś napisał.
Trzecia pisze go sama, i w niej stoi tor składu,
czyli ten, który z drzewa wypuszcza polskie zdanie.
Wypuszczenie zdania z drzewa ma w polu nazwę i jest nią realizacja:
wyprowadzenie postaci powierzchniowej z reprezentacji, która pod nią stoi.
Nazwa sięga dalej niż generowanie, bo realizacją jest i głoska wyprowadzona z fonemu,
więc kto szuka literatury, ten szuka realizacji powierzchniowej,
po angielsku *surface realization*.
Rozdziela tę tradycję jedno pytanie: co autor podaje na wejściu.
Poziom wejścia rozstrzyga, co autor pisze, ile system musi wiedzieć o języku
i czego z takiego wejścia nie da się już powiedzieć.
Przegląd tego pola trzymają Gatt i Krahmer,
*Survey of the State of the Art in Natural Language Generation*, JAIR 61 (2018),
i jest on tym, co się tu czyta pierwsze.

| Poziom wejścia | Co wchodzi | Kto tak stoi |
| --- | --- | --- |
| fakty | trójki RDF, aksjomaty ontologii | WebNLG, NaturalOWL |
| dziedzina | konstruktory nazwane tym, o czym się mówi | gramatyka aplikacyjna GF, `skład` |
| kategorie językowe | zdanie, grupa imienna, grupa czasownikowa | biblioteka gramatyk GF |
| struktura głęboko-składniowa | zależności bez słów funkcyjnych | RealPro, FORGe |
| struktura funkcjonalna | f-struktura gramatyki odwracalnej | XLE wraz z POLFIE |
| drzewo lematów | szyk i odmiana do odzyskania | zadanie nad Universal Dependencies |
| specyfikacja zdania | podmiot, orzeczenie, cechy zdania | SimpleNLG wraz z portami |
| szablon | tekst wraz z miejscami do wypełnienia | RosaeNLG |
| forma | lemat wraz z tagiem | sam Morfeusz |

Dwa wiersze tej tabeli zajmuje GF, i jest to w nim podział:
gramatyka aplikacyjna ma składnię abstrakcyjną opisującą dziedzinę,
a stoi na bibliotece gramatyk, której kategorie opisują język.
Skład bierze drugi wiersz na kategorie i ostatni na formy,
a między nimi stawia trzy małe leksykony:
ramę czasownika, rekcję przyimka i relację spójnika.
Co ten wybór poziomu znaczy, trzyma
[sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka).

Poziom, który tamten dokument odrzuca jako pierwszą ze
[trzech architektur](sklad.md#three-architectures),
jest poziomem SimpleNLG, czyli realizatora,
którego API bierze podmiot, orzeczenie, dopełnienie i cechy zdania.
Inni ludzie przenieśli je na pięć języków: niemiecki, włoski, holenderski,
hiszpański i portugalski brazylijski, a polskiego wśród nich nie ma.
Zarzut, który tamten dokument stawia temu poziomowi, jest więc zarzutem o prozę:
kto wypełnia szablon raportu, ten drzewo zdania pisze bez straty,
bo zdania w raporcie nikt nie czyta dla rytmu.

Dwie rzeczy, które skład robi nad zdaniem, mają w tym polu nazwy i literaturę.
Potok Reitera i Dale'a rozdziela planowanie dokumentu, mikroplanowanie i realizację,
a mikroplanowanie obejmuje generowanie wyrażeń referencyjnych oraz agregację.
`Postać` wraz z `pomijalny` jest pierwszym z nich, a `Ciąg` drugim,
więc skład zajmuje dwa moduły tego potoku, a planowania dokumentu nie ma wcale:
o czym opowieść jest, rozstrzyga ten, kto pisze drzewa.
Granicę akapitu pisze przy tym autor, a skład ją czyta,
bo na niej kończy się to, co dla opuszczonego podmiotu jest zdaniem obok.
Czwarty warunek `pomijalny` pyta, czy tej samej formy nie wyciąga z czasownika nikt inny,
i jest to test na zbiór dystraktorów,
czyli to samo, na czym stoi przyrostowy algorytm Dale'a i Reitera (1995).
Wywód o tym warunku trzyma
[sklad.md](sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie);
ten akapit mówi tylko tyle, że nie jest on domowy.
Ten sam mechanizm poza tradycją lingwistyczną ma RosaeNLG,
gdzie wyrażenie referencyjne jest funkcją szablonu,
a Fundacja LF AI zarchiwizowała ten projekt w 2026 roku.

Sama realizacja rozkłada się na trzy części,
a podział ten ma w SimpleNLG postać potoku:
klasa `Realiser` puszcza element przez składnię, potem przez morfologię,
a na końcu przez ortografię.
Część składniowa wybiera odmianę, dostawia słowa funkcyjne i rozstrzyga szyk,
morfologiczna wylicza z tego formę,
a ortograficzna odpowiada za wielką literę, interpunkcję i formatowanie.
Dwie pierwsze mają w pakiecie `skład` po module, `skład.składnia` i `skład.morfologia`,
a trzeciej osobno nie ma i siedzi ona wewnątrz pierwszej.
Interpunkcja stoi wewnątrz linearyzacji jako pole `Kawałek`,
czyli jako żądanie konstytuenta wobec sąsiada, a nie jako znak w gotowym napisie,
i wywód o tym trzyma docstring `Kawałek` w `skład/składnia.py`;
etap puszczony po morfologii jest na to za późny.
Wielka litera wraz z kropką staje za to na końcu, w `kompiluj`.
Trójwarstwowy podział, który `skład/__init__.py` ogłasza swoją decyzją,
jest więc innym podziałem niż te trzy części, choć dwie nazwy się pokrywają:
warstwa trzecia, `skład.opowieść`, stoi nad zdaniem, a nie w nim,
i trzyma tożsamość, której żąda wyrażenie referencyjne z akapitu wyżej.

Zadanie realizacyjne nad drzewami Universal Dependencies (SR'18, SR'19, SR'20) pyta,
czy z drzewa lematów wróci szyk wraz z odmianą, i liczy to nad wieloma językami,
a jego wejście stoi o kilka wierszy niżej niż drzewo składu,
więc liczba stamtąd nie przenosi się tutaj i nie ma czego z nią porównywać.
Gramatyki odwracalne kupują za to jedno, czego ten tor nie ma:
w GF ta sama deklaracja daje linearyzację i parser, bo składnia abstrakcyjna
jest podpisem, a nie kodem,
podczas gdy konstruktor składu jest klasą Pythona wraz z metodą `linearyzuj`.
Dlaczego mimo to parser stoi tu świadkiem, a nie zależnością,
rozstrzyga [design-notes.md](design-notes.md#the-round-trip-invariant).

## Outliers

**Lojban** is the extreme of designing for parseability:
a constructed language with a formal machine grammar in YACC,
claimed to be fully syntactically unambiguous.
Instructively, it is *not* LALR(1) —
some words' grammatical function
depends on tokens that follow them,
so parsing happens in two stages,
and a PEG grammar has been proposed as the replacement baseline.
A language designed from scratch for unambiguous parsing
still could not stay inside the easy formalism.

## On the Polish side

**Plain Polish** exists as a movement:
the Pracownia Prostej Polszczyzny at the University of Wrocław,
and **Jasnopis**, from SWPS University and the Polish Academy of Sciences,
which scores text difficulty on a scale from 1 to 7,
flags hard fragments,
and since 2023 simplifies automatically.

This is readability work, not formal grammar.
It shares olski's instinct
that a restricted Polish is worth having,
and none of its machinery.

**The gap is real.**
Kuhn's hundred languages are all English-based.
Polish-language sources on controlled languages
state plainly that research on the topic is rare for Polish.
A controlled Polish
with a formal grammar,
high naturalness,
and deterministic checking
is close to unoccupied ground.

That is not evidence the idea is good.
It is evidence that nobody will hand us the answer.

## Sources

- <https://aclanthology.org/J14-1005/> — Kuhn, *A Survey and Classification of Controlled Natural Languages*
- <https://arxiv.org/abs/1507.01701> — the same survey on arXiv
- <https://en.wikipedia.org/wiki/Controlled_natural_language>
- <https://en.wikipedia.org/wiki/Simplified_Technical_English>
- <https://www.asd-ste100.org/> — ASD-STE100 specification
- <https://attempto.ifi.uzh.ch/site/pubs/papers/reasoningweb2008_fuchs.pdf> — ACE for knowledge representation
- <https://ceur-ws.org/Vol-448/paper14.pdf> — Rabbit to OWL
- <https://arxiv.org/pdf/1406.2903> — a brief state of the art for ontology authoring
- <https://arxiv.org/abs/1406.2096> — RuleCNL for business rules
- <https://direct.mit.edu/coli/article/46/2/425/93370/Abstract-Syntax-as-Interlingua-Scaling-Up-the> — GF from controlled languages to robust pipelines
- <https://journals.colorado.edu/index.php/lilt/article/view/1205> — the GF Resource Grammar Library
- <https://matrix.ling.washington.edu/> — the LinGO Grammar Matrix
- <https://delph-in.github.io/docs/home/Home/> — DELPH-IN
- <https://clarin-pl.eu/dspace/handle/11321/588> — Świgra, a parser of Polish
- <https://clarin-pl.eu/dspace/handle/11321/253> — POLFIE
- <https://aclanthology.org/W91-0100.pdf> — Reversible Grammar in Natural Language Processing, 1991 workshop
- <https://link.springer.com/article/10.1007/s10590-021-09260-6> — recent advances in Apertium
- <https://arxiv.org/abs/1703.09902> — Gatt and Krahmer, the survey of the generation field
- <https://arxiv.org/abs/cmp-lg/9605002> — Reiter and Dale on the generation pipeline
- <https://arxiv.org/abs/cmp-lg/9504020> — Dale and Reiter on referring expressions, the incremental algorithm
- <https://en.wikipedia.org/wiki/Realization_(linguistics)> — realization, the term and the three kinds of processing
- <https://aclanthology.org/W09-0613/> — SimpleNLG, a realisation engine for practical applications
- <https://github.com/simplenlg/simplenlg> — SimpleNLG itself, whose wiki lists the ports
- <https://github.com/simplenlg/simplenlg/blob/master/src/main/java/simplenlg/realiser/english/Realiser.java> — the three parts as a pipeline, syntax then morphology then orthography
- <https://aclanthology.org/W16-6630/> — adapting SimpleNLG to Italian, one of those ports
- <https://aclanthology.org/A97-1039/> — RealPro, a realizer over deep syntactic structures
- <https://aclanthology.org/S17-2158/> — FORGe, rule-based generation over meaning-text structures
- <https://aclanthology.org/2020.msr-1.1/> — the third multilingual surface realisation shared task
- <https://aclanthology.org/2020.webnlg-1.7/> — the WebNLG+ shared task, text from RDF triples
- <https://arxiv.org/abs/1405.6164> — NaturalOWL, text from OWL ontologies
- <https://github.com/RosaeNLG/rosaenlg> — RosaeNLG
- <https://lfaidata.foundation/projects/rosaenlg/> — RosaeNLG at the LF AI foundation, and its archiving
- <https://lojban.github.io/cll/21/1/> — Lojban formal grammars
- <https://mw.lojban.org/papri/PEG> — the Lojban PEG proposal
- <https://jasnopis.pl/prosty-jezyk/> — Jasnopis and plain Polish
- <https://mdpi.com/1999-4893/9/3/58/htm> — LR parsing for LCFRS
