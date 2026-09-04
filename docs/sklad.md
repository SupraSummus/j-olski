# Skład: drzewo wchodzi, polskie zdanie wychodzi

Wchodzi drzewo tego, co ma zostać powiedziane, a wychodzi polskie zdanie,
a z kilku drzew postawionych obok siebie wychodzi tekst.
Ten dokument rozstrzyga jedno: na jakim poziomie stoją kategorie tego drzewa.
Resztę toru trzymają trzy dokumenty obok.

Etapy wraz z kryterium wyjścia trzyma
[roadmap.md](roadmap.md#tor-składu-drzewo-wchodzi-polskie-zdanie-wychodzi),
a tor gramatyczny, czyli ten sam podzbiór czytany w drugą stronę,
[design-notes.md](design-notes.md).
Dlaczego parser stoi tu świadkiem, a nie zależnością,
rozstrzyga [design-notes.md](design-notes.md#the-round-trip-invariant).
Jak pole nazywa tę operację i na jakie trzy części ją rozkłada,
trzyma [similar-work.md](similar-work.md#generowanie-rozdziela-się-poziomem-wejścia).

Generation inverts every difficulty in parsing.

Ambiguity is the parser's curse;
a generator never encounters it.
Agreement stops being a constraint to check
and becomes a value to compute.
Parsing `czarnego kota` means reconciling two syncretic feature bundles.
Generating it means calling `inflect(kot, acc.sg.m2)`
and getting one answer.

## Który plik czytać

Poziom zapisu jest wywodem i czyta się go od góry, czyli dalej w tym pliku.
Trzy dokumenty obok czyta się do swojego wpisu.

- [kategorie-zapisu.md](kategorie-zapisu.md) — kategorie,
  w których autor pisze drzewo.
- [po-wypisaniu.md](po-wypisaniu.md) — przegląd ról, obieg zamknięty i makieta,
  czyli to, czego nie widać, dopóki napis nie zostanie wypisany.
- [formy-i-leksemy.md](formy-i-leksemy.md) — zgodność, morfologia i dwa leksykony,
  czyli warstwa pod kategoriami.

## Three architectures

**Correct by construction.**
The source is a typed abstract syntax tree,
with types encoding what agrees with what.
Ill-formed input fails to typecheck;
well-formed input compiles to text and cannot be wrong.
Strongest guarantee, and the ergonomics depend on what is being written:
SimpleNLG, a realizer whose API takes a subject, a verb and features,
offers exactly this level,
and other people have ported it to five languages,
so the objection is to authoring prose this way rather than to the level
([similar-work.md](similar-work.md#generowanie-rozdziela-się-poziomem-wejścia)).

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

## The predictive editor changes this

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

## Czwarta architektura: poziom dziedziny, a nie poziom języka

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
Jednoznaczność ta zdejmuje przy okazji wieloznaczność, której sam worek słów nie odróżnia,
a która nad polszczyzną jest zwyczajna:
`parser podzbioru` i `podzbiór parsera` są dwoma różnymi drzewami,
choć stoją w nich te same lematy w tych samych rolach.

Buduje to `olski/skład/`: `olski/skład/grupa.py` trzyma kategorie niosące rzecz,
a `olski/skład/składnia.py` te, które orzekają o niej zdaniem.
Zgodność jest tam liczona, a nie sprawdzana,
więc gramatyki podzbioru ten kierunek nie potrzebuje
([design-notes.md](design-notes.md#the-round-trip-invariant)).

Szyk to drzewo niesie, ale niesie go na jednym poziomie z dwóch.
Polszczyzna niesie szykiem temat i remat,
więc `Wejściem jest zwykły tekst polski.` i `Zwykły tekst polski jest wejściem.`
mówią to samo zdanie logiczne i co innego stawiają na czele,
a `Wyróżnienie` jest tą kategorią, z której oba wychodzą.
Kolejność słów jest z niej wnioskiem, a nie wariantem dopisanym do linearyzacji:
czasownik zostaje na miejscu, a przestawia się to, co stoi wokół niego.
Wewnątrz grupy imiennej takiej kategorii nie ma i jest to brak, a nie decyzja:
przymiotnik przed rzeczownikiem określa, a po rzeczowniku nazywa,
i dlatego README pisze `kontrolowanych języków naturalnych`,
a kompilator z tego samego drzewa wypuszcza `kontrolowany naturalny język`.
Języki o szyku ustalonym tego wyboru nie mają,
więc biblioteka wzięta od kogoś, kto go nie miał, nie odpowie za nas.
Co ma go rozstrzygać wewnątrz grupy, nie zapadło, i trzyma to `todo/`.

Szyk, który z tego drzewa wychodzi, ma z czym się porównać,
bo rozkład szyków polszczyzny ktoś policzył.
Woliński przeliczył szyk 16 019 zdań elementarnych Składnicy
i powtórzył tym samym wcześniejsze liczenie Derwojedowej,
zrobione ręką na korpusie mniejszym i inaczej dobranym;
osiem najczęstszych wariantów wyszło w obu badaniach to samo.
Pierwszy jest wariant VO z 24,5% zdań, drugi SVO z 22,5%, a trzeci OVS z 7,3%
(Woliński, *Automatyczna analiza składnikowa języka polskiego*, 2019, p. 6.9,
a wylicza tę pracę [swigra.md](swigra.md#sources)).
Wiersz pierwszy liczy zdania, w których podmiot nie został wypisany,
choć zdania z podmiotem są razem liczniejsze niż te bez niego,
a opuszczanie podmiotu jest dokładnie tym, co ten kompilator już umie.
Drugi i trzeci wiersz różni sam szyk przy tym samym komplecie ról,
czyli ten wybór, który tutaj wychodzi z tematu i rematu.
Korpus jest jednak prozą i prasą, a nie rejestrem, do którego skład celuje,
więc rozkład ten jest miarą porównawczą, a nie celem do trafienia.
