# The subset, as implemented

What `olski/subset.py` admits,
and the decisions that shaped it.
For the theory behind the track, see [design-notes.md](design-notes.md).

## Validity is uniqueness, not just derivability

A sentence is olski when it has **exactly one** reading.
Not at least one.

The case that settled this:

```text
Koszt samej szynki przewyższa koszt szynki z dodatkami.
```

`koszt` is nominative or accusative — the syncretism is total for m3 nouns —
and Polish permits both SVO and OVS.
So the sentence parses two ways
and says the opposite thing in each,
without a Polish reader being able to tell which was meant.

Nothing in the comparison itself does this.
Give the same verb a subject and an object whose cases do not collide
and the sentence has one reading:

```text
Chałka przewyższa zwykłą bułkę.
```

`chałka` is nominative and nothing else,
`bułkę` accusative and nothing else,
so OVS has nowhere to derive,
and the syncretism is what costs the first sentence its meaning.

Where the cases do collide, two answers were available.
Declare olski to be SVO and read the first noun phrase as the subject,
or reject the sentence.
Rejecting it wins,
because the convention would make the sentence unambiguous
only to a reader who knows the convention,
and the settled goal is that olski reads as ordinary Polish
to any Polish speaker.
A sentence nobody else can read reliably
is not a sentence olski should let through.

This also answers a question the linter track had left open.
Deep analysis is expensive because ambiguity is expensive.
Rather than pay for machinery that resolves ambiguity,
olski excludes the constructions that create it,
and every later rule inherits the exclusion.

## What counts as one reading

Two derivations are the same reading
when they have the same shape and the same parts of speech.
Feature values and lemmas are deliberately excluded.

- **Lemmas.** `zapisuje` belongs to both `zapisywać` and `zapisować`.
  Polish forms are homonymous everywhere,
  so counting that as ambiguity would reject nearly the whole language.
  Lexical ambiguity is the reader's to resolve.
- **Feature values.** Whether a phrase settled on neuter plural
  or masculine singular is not something a reader chooses between.
  Agreement has already been enforced by unification.

What does count is anything that changes the structure:
which phrase is the subject, what the object is,
where a modifier attaches,
and whether a word is being read as a noun or a gerund.

This is the distinction
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
got wrong and recorded:
counting attempts rather than outcomes
made it fall silent on lines it had understood perfectly.

## The dictionary offers readings Polish does not

Whether a word is read as a noun or as something else changes the structure,
so by the rule above it is a second reading.
One class of those is a second reading no Polish speaker has.

Morfeusz reads `do` as the preposition and as the musical note,
and the note is indeclinable:
`subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:n:ncol` is every case at once.
Unification is the only filter olski has,
so a reading that satisfies every case demand
is one no context can rule out.
`do pliku` therefore derives twice —
as a prepositional phrase,
and as a noun with a genitive modifier —
and so does every other occurrence of `do`,
which is not a rare word:
[corpus.md](corpus.md#what-morphological-ambiguity-costs)
counts it in the treebank
and measures what excluding the note is worth and what it costs.

Olski refuses a sentence that is ambiguous in Polish.
This one is ambiguous only in the dictionary,
and a parse cannot tell those two cases apart,
so the subset excludes readings as well as constructions:
an uninflected noun reading goes
wherever the same form also reads as a function word —
a preposition, a conjunction, a particle, an interjection.
`admissible` in `olski/subset.py` is where that happens.

One exception runs the other way.
`PO`, `AA` and `UP` are organizations,
they inflect for nothing either,
and their letters spell a preposition and two interjections.
Here the noun is what the form is
and the function word is the accident,
so an all-caps form of more than one letter keeps every reading it has.
A single capital is no evidence either way,
since every sentence starts with one.

Three simpler criteria were available and none holds.
Morfeusz's own qualifiers mark the note `muz.`
and the Japanese theatre that `no` also reads as `teatr.`,
which looks like the criterion until `ku` and `ni`,
which carry no qualifier at all.
The dictionary's labels do not separate them either:
the note is a common noun, `Tam` a surname and `PO` an organization,
and the exclusion has to take the first two and leave the third.
Dropping every uninflected noun instead
would take `jury` and `menu` with it,
and those are ordinary Polish words
with no other reading to fall back on.
What makes the exclusion safe is that it asks for both at once:
the reading inflects for nothing,
and the form carries another one that is what it almost always is.

## Notacja tego rejestru jest słowem, którego słownik nie ma

Wykluczenie wyżej odbiera formie czytanie, którego Polak nie ma.
Notacja jest przypadkiem odwrotnym:
słownik nie ma tu czytania żadnego, a czytelnik ma jedno.

`docs/linter.md` jest dla Morfeusza pięcioma segmentami,
bo ukośnik i kropka są dla niego interpunkcją,
a `docs` nie jest żadnym polskim słowem, więc wraca jako `ign`,
którego nie bierze ani jedna produkcja.
Rejestr, o który olskiemu chodzi, jest takich form pełen —
ścieżka, nazwa pliku, nazwa modułu, nazwa polecenia —
i stoją one w zdaniach na miejscach rzeczownika,
bo tym w takim zdaniu są.

Olski daje więc takiej formie jedną krawędź i jedno czytanie:
rzeczownik nieodmienny, dokładnie ten tag,
który Morfeusz daje `menu` i `atelier`
(`subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:n:ncol`).
Rzeczownikiem nieodmiennym taka forma jest w polszczyźnie naprawdę,
a jedno czytanie znaczy, że nie ona daje zdaniu drugie.
Sklejenie stoi przed analizą, a nie za nią,
bo segment niesie numery węzłów grafu, a nie przesunięcia w tekście,
więc po analizie nie ma już czym zobaczyć spacji,
która ukośnik w ścieżce odróżnia od ukośnika między dwoma słowami.

Wzorzec, który to rozpoznaje, stoi w `NOTACJA` w `olski/subset.py`,
a tu stoi to, przed czym każde jego żądanie broni,
bo z samego wzorca tego nie widać.
`np.` i `r.` mają kropkę i nie są notacją,
więc kropka spaja tylko wtedy, gdy nie ma po niej spacji.
`m.in.` i `S.A.` spajają się bez spacji i notacją nie są,
więc człon musi być dłuższy niż litera —
za co płaci się ścieżką, której człon jest jednoznakowy,
i takiej olski nie sklei.
`czarno-biały` Morfeusz zna po członach
i sklejony w jedno wypadłby ze słownika razem z gramatyką,
więc łącznik spaja tylko wewnątrz ścieżki, którą trzyma już kropka:
`design-notes.md` wchodzi całe.
`2018.07.23` spaja się kropkami jak ścieżka, a rzeczownikiem nie jest,
i Morfeusz zna tę formę jako liczbę,
więc notacja musi nieść przynajmniej jedną literę.

Własność, przez którą wykluczenie wyżej istnieje, jest tu ceną.
Forma nieodmienna spełnia każde żądanie przypadku,
jakie unifikacja umie postawić,
więc notacja stoi w zdaniu wszędzie tam, gdzie stoi jakikolwiek rzeczownik.
`Cały wywód prowadzi docs/linter.md.` wychodzi z tego dwoma czytaniami,
SVO i OVS, i jest to ta sama wieloznaczność,
którą polszczyzna ma na `Koszt samej szynki przewyższa koszt szynki`:
zdanie naprawdę nie mówi, co tu prowadzi co.

To jest połowa klasy, a nie cała.
Drugą połową jest polskie słowo odmienione, którego słownik nie ma,
i tej olski nie wpuszcza;
powód trzyma [lista tego, czego gramatyka nie obejmuje](#what-it-does-not-cover-yet).

## What the grammar covers

- Clauses in SVO and OVS order, and subjectless clauses,
  both imperative (`Zapisz plik.`)
  and pro-drop indicative (`Zapisuje ustawienia.`)
- A verb before its subject, with an agreeing predicative after it or without one:
  `Są oni obdarzeni rozumem.`, `Nadchodzi druga rewolucja.`
- A predicative before the copula, which is the mirror of OVS:
  `Wejściem jest zwykły tekst polski.`
- Reflexive verbs, with `się` in the position after the verb
- An agreeing predicative, under the copula and under a verb that is not one:
  `Ludzie są wolni.`, `Ludzie rodzą się wolni.`
- A nominal predicative in the instrumental, under the copula and nowhere else:
  `Jan jest nauczycielem.`
  The copula is a closed list of lemmas
  (`być`, `zostać`, `zostawać`, `pozostać`, `pozostawać`),
  which is what keeps an instrumental adjunct from reading as a predicative
  under every other verb —
  the mistake [corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)
  counts on `Kwitnie handel paszportami.`
  What the list leaves out is the copula that takes `się`:
  `okazać się` and `stać się` govern the same case
  and the production has no place for the particle.
- The register's own notation as an indeclinable noun:
  `Zobacz docs/rules.md.`, argued above
- A modal with its infinitive.
  `powinien` inflects for gender and not for person,
  so the clause it heads agrees with its subject in gender
  and leaves person to whatever else constrains it.
- An infinitive as what any other verb takes:
  `Program pozwala zapisać ustawienia.`
  A chain of them needs no rule of its own,
  because an infinitive phrase takes complements
  and an infinitive phrase is one of them,
  so `ma pomagać pisać` comes out of the two productions already there.
- Noun phrases with an adjective before or after the noun,
  a genitive modifier, or a prepositional modifier
- Pronouns, and with them first and second person subjects.
  Person comes from the subject rather than being fixed at the third,
  so `Ja zapisuje plik.` is a disagreement
  in the way `Nowa program` is one.
- Coordination, of noun phrases, of adjective phrases and of clauses,
  joined by a conjunction
- Any number of prepositional adjuncts on one verb,
  because `postępować wobec innych w duchu braterstwa` has two
- Prepositional phrases, with the preposition governing the case
- A prepositional phrase in front of the clause,
  which modifies the clause rather than any noun in it
- An adjunct in every other position a prepositional phrase can follow
  a noun phrase in: around the verb in each of the orders,
  before the object, after a noun that already carries
  an adjective or a genitive, and after a participle.
  The positions are one decision rather than a list,
  and [Przyłączanie wyrażeń przyimkowych](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
  is where it is taken, enumerated and priced.
- Agreement throughout, as unification rather than as a separate check:
  `Nowa program zapisuje ustawienia.` has no derivation at all

Agreement being the parse rather than a check on the parse
is what makes the rejection precise.
There is no rule that says an adjective must agree with its noun.
There is only a production that shares a variable between them,
and a sentence that cannot satisfy it is not in the language.

## The bare verb-initial order keeps the predicative one honest

```text
Trwa akcja protestacyjna.
```

The adjective is attributive or it is predicated,
and Polish gives a reader both.
Admit only the verb-initial order that takes a predicative
and the second reading has nothing to compete with,
so olski calls it the one reading and is confidently wrong.
That is the failure
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance) counts,
and admitting the bare order beside it
costs the sentence its uniqueness and keeps its honesty.

The subject takes no complements of its own in either order,
which is what stops `Zapisuje program ustawienia.` deriving
and stops every SVO sentence competing with a verb-initial reading of itself.

## Nothing above a coordination distributes into it

A coordination is one **conjunct**, a conjunction, and the rest,
and the grammar's symbols are named for it:
`NPConjunct` is a noun phrase with no coordination in it,
`NP` is one that may have.
An adjective attaches inside a conjunct and never above the coordination,
so `nowe programy i pliki` is `[nowe programy] i [pliki]`
and never `nowe [programy i pliki]`.
That is a narrowing rather than a reading of Polish,
and what it buys is an agreement that can still fail.

A coordination has no gender of its own.
Polish resolves the gender of `rozum i sumienie`
by rules unification cannot state,
and a feature a phrase does not carry
is one no agreement can fail against,
so an adjective scoping over the coordination
would be an adjective agreeing with nothing
and `nowa programy i pliki` would derive.
Refusing the wider attachment is what keeps that a rejection.

## What it does not cover yet

Each of these is a sentence that gets rejected
and should not be:

- Clause-level punctuation.
  Two clauses join with a conjunction and not with a comma,
  so `Plany są niczym, ale planowanie jest wszystkim.`
  fails at the third segment, on the comma.
- The past tense, which
  [corpus.md](corpus.md#where-the-analyses-stop)
  ranks as the cheapest large gain left.
- Subordination with `że` and `który`.
- Negation and the genitive of negation.
- Numerals, which are common
  and are their own self-contained problem.
- `to` as a copula.
  `Kot to zwierzę.` is rejected where `Kot jest zwierzęciem.` derives,
  and the form heads two of the rows
  [corpus.md](corpus.md#where-the-analyses-stop) ranks,
  one of predicatives and one of nominal pronouns,
  which is the ambiguity admitting it has to survive.

Two entries are not constructions but demands every construction makes:

- **Valency.** Nothing records which complements a verb actually takes,
  so `być` accepts an accusative object,
  and any verb accepts an agreeing predicative or an infinitive.
  `On jest wolny.` is where that shows:
  `wolny` reads as an adjective and as a noun,
  so the sentence comes out ambiguous
  between the predicative a reader has and an object nobody means.
  [corpus.md](corpus.md#what-morphological-ambiguity-costs)
  found the same gap from the other side.
  The instrumental predicative is the one slot this has been taken out of,
  by the closed list of copulas above,
  and what that leaves is a lexicon rather than a list.
- **A Polish form the dictionary does not have.**
  Morfeusz is asked not to guess at one (`olski/morph.py`),
  so it comes back tagged `ign`,
  which no production takes and no agreement can rescue.
  `olski` is such a form:
  `Język polski jest podzbiorem polszczyzny.` derives
  and `Język olski jest podzbiorem polszczyzny.` does not,
  so the language cannot say in itself what it is.
  Notation is the half of this class olski does admit,
  and the reason the rest stays out is that the form is inflected:
  `lintuje` is a finite verb, `znacznikowym` an adjective in the instrumental,
  `commitów` a genitive plural,
  and reading any of them as the indeclinable noun notation gets
  would invent a reading that is not merely unknown but wrong,
  against the promise that every olski sentence is well-formed Polish.
  Gold morphology leaves a treebank no such form,
  which is why the queue in
  [corpus.md](corpus.md#where-the-analyses-stop) does not rank it
  and a run over documentation does.

## Przyłączanie wyrażeń przyimkowych: olski nie wybiera

```text
Program zapisuje ustawienia w pliku.
```

`w pliku` dochodzi do czasownika albo do dopełnienia,
a to są dwa różne zdania o tym, gdzie te ustawienia są.
Oba wyprowadzenia są polszczyzną,
więc własność jednoznaczności to zdanie odrzuca.

Konstrukcja nie jest przy tym rzadka.
Niemal każde zdanie z wyrażeniem przyimkowym po dopełnieniu
jest wieloznaczne tak samo,
więc własność w tym brzmieniu
wyklucza dużą i zwyczajną część technicznej polszczyzny.

Porównanie, którym ten dokument się otwiera, na to trafia.
`przewyższać` porównuje pod jakimś względem —
w czym jedno przewyższa drugie —
i to brak tego względu każe `Chałka przewyższa zwykłą bułkę.`
czytać sztywno,
więc kto pisze to zdanie, ten ten wzgląd nazywa:
`Chałka przewyższa zwykłą bułkę pod względem smaku.`
A to znowu są dwa czytania,
jedno, w którym wzgląd należy do porównania,
i drugie, w którym należy do bułki.

Jedna pozycja z tego wychodzi i gramatyka ją bierze:

```text
Pod względem smaku chałka przewyższa zwykłą bułkę.
```

Wyrażenie przyimkowe określa polski rzeczownik tylko zza niego,
więc przed zdaniem nie ma rzeczownika, do którego mogłoby dojść,
i czytania, w którym smak należy do bułki, nie ma —
ani dla parsera, ani dla polskiego czytelnika.
Wysunięcie nie żąda od czytelnika niczego,
bo jest pozycją, którą język ma,
a co daje jego dopuszczenie nad bankiem drzew,
liczy [corpus.md](corpus.md#where-the-analyses-stop).

Wyjścia z tego są trzy: przyjąć koszt i odrzucać takie zdania,
przyłączać zawsze do czasownika, chyba że coś wymusza inaczej,
albo uznać, że te dwa czytania mówią o jednej sytuacji
i liczyć je za jedno.
Rozstrzyga między nimi prawdziwa polszczyzna, a nie gust.

### Bank drzew nie zna domyślnego przyłączenia

Ściągnięcie korpusu opisuje [corpus.md](corpus.md#fetching-it), a potem:

```sh
python3 -m olski.attachment Składnica-frazowa-180723/
```

W wydaniu 2018 Składnicy stoi 5 837 wyrażeń przyimkowych
w pozycji, w której olski widzi dwa czytania:
tuż za grupą imienną, która się na nich kończy,
więc przyłączenie do rzeczownika jest do wzięcia.
4 517 z nich stoi w zdaniu, w którym czasownik stoi przed wyrażeniem,
czyli przyłączenie do czasownika jest do wzięcia tak samo.
Wybór anotatorów rozkłada się na nich tak:

| dokąd doszło | wyrażeń | |
| --- | --- | --- |
| do rzeczownika | 2 698 | 59.7% |
| do czasownika albo do zdania | 1 378 | 30.5% |
| gdzie indziej | 441 | 9.8% |

„Gdzie indziej” to fraza wymagana szersza niż samo wyrażenie,
fraza przymiotnikowa i drugie wyrażenie przyimkowe;
żadne z tych trzech nie jest tym wyborem, o który tu chodzi.

Tabeli nie rusza zmiana w gramatyce, bo mierzone są cudze drzewa
i żadna produkcja olskiego nic do tych liczb nie wnosi.
Rusza ją wydanie korpusu i to, co `olski/attachment.py` liczy:
które kategorie są zdaniem, a które grupą imienną, i co znaczy „po czasowniku”.

Rozkład nie zmienia się na tyle, żeby przyimek go przewidywał.
Odsetki niżej liczą się z dwóch przyłączeń, o które tu chodzi,
a nie z całej tabeli wyżej, więc porównują się do 66.2%,
czyli do tego, ile z tych dwóch bierze rzeczownik.
Nad `w` jest to 65.0% do rzeczownika, nad `na` 65.2%,
nad `do` 60.6%, a najbardziej przechylone `dla` daje 83.1%,
więc nawet leksykon przyimków myliłby się co szóste zdanie,
a nad najczęstszymi co trzecie.

### Dlatego olski przyjmuje koszt

Wyjście drugie, przyłączaj do czasownika, jest czytaniem mniejszościowym:
stawiałoby na 30% wtedy, gdy polszczyzna wybiera 60%.
Konwencja, która myli się ponad dwa razy częściej, niż trafia,
nie jest konwencją, którą czytelnik ma;
to jest ten sam zarzut, który obalił ustalenie szyku na SVO,
tyle że tutaj z liczbą pod spodem.

Wyjście trzecie musiałoby twierdzić, że te dwa czytania
mówią o jednej sytuacji.
Klasa się na to nie zgadza, i mierzy to ta sama komenda:
576 przyłączeń do czasownika to frazy, których czasownik wymaga swoim schematem,
a 214 przyłączeń do rzeczownika to frazy, których żąda sam rzeczownik.
Po żadnej z tych dwóch stron nie ma parafrazy:
przeczytanie frazy wymaganej po drugiej stronie
łamie schemat tego, kto jej żądał.
Twierdzenia o jednej sytuacji nie da się postawić nad taką klasą.

Zostaje wyjście pierwsze i olski je bierze.
Autor wysuwa wyrażenie przed zdanie albo dzieli zdanie na dwa,
a olski melduje dwa czytania i zdania nie przyjmuje.

### Przyjąć koszt to znaczy dać oba czytania wszędzie

Wyjście pierwsze wygląda na takie, które od gramatyki nie żąda niczego,
i to jest w nim mylące.
Odrzucenie jest uczciwe tylko wtedy,
gdy oba przyłączenia w ogóle mają gdzie się wyprowadzić.
Pozycja, w której gramatyka ma regułę na jedno z nich i nie ma na drugie,
nie odrzuca zdania — przyjmuje je z jednym czytaniem,
czyli wybiera przez przeoczenie to,
czego ta decyzja wybierać zabrania.

Takich pozycji jest tyle, ile zdanie ma miejsc,
w których za grupą imienną może stanąć wyrażenie przyimkowe,
i każda z nich jest zwyczajną polszczyzną:

- po podmiocie w szyku SVO, przed orzeczeniem
  (`Przybysze z najnowszej fali na ogół stronią od organizacji.`)
- po dopełnieniu i po podmiocie w szyku OVS
  (`Ustawienia w pliku zapisuje program.`)
- po podmiocie w szykach z czasownikiem na czele,
  przed orzecznikiem i za nim
  (`Trwa dochodzenie w tej sprawie.`)
- po orzeczniku wysuniętym przed kopulę i po podmiocie za nią
  (`Wejściem w tym trybie jest zwykły tekst.`)
- przed dopełnieniem, wewnątrz orzeczenia
  (`Program zapisuje w pliku ustawienia.`)
- po rzeczowniku, który już ma przy sobie przymiotnik albo dopełniacz
  (`akcja zbrojna w Strefie Gazy`),
  oraz po imiesłowie (`powiązani z interesami postkomunistów`)

Wierszy jest sześć, a produkcji dwanaście,
bo pozycja powtarza się w każdym szyku, który ją ma,
a szyk jest w tej gramatyce osobną produkcją.

Dwa z tych zdań pokazują, po czym brakującą pozycję poznać,
i nie jest to zdanie odrzucone.
`Ustawienia w pliku zapisuje program.` wygląda na pozycję,
w której zostaje samo czytanie rzeczownikowe, i nią nie jest:
gdy reguła OVS okolicznika nie bierze, wyrażenie dochodzi tylko do rzeczownika,
a zdanie wychodzi jednoznaczne tam, gdzie polski czytelnik ma oba czytania.
`Program zapisuje w pliku ustawienia.` wychodzi wtedy jednym czytaniem,
w którym `w pliku ustawienia` jest jedną frazą i dopełnienia nie ma wcale.
Oba zdania są wieloznaczne, a bez swojej pozycji każde z nich zostaje przyjęte,
i to jest ta różnica, której po samym werdykcie nie widać.

Nad Składnicą płaci się za to przyjętymi zdaniami,
a kupuje czytania, których olski nie czyta odwrotnie:
gramatyka bez tych pozycji czyta wbrew ręcznemu rozbiorowi dziewięć zdań,
a z nimi jedno, i to jedno nie jest wyborem, którego olski dokonał.
Liczby trzyma
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance).

Klasa nie jest przez to zamknięta.
Walencja zdejmuje z niej tę część, w której czasownik frazy wymaga —
576 z 4 517 wyrażeń wyżej, czyli 13% —
bo tam czytanie rzeczownikowe łamie schemat czasownika,
a nie konkuruje z nim.
To jest [etap 2](roadmap.md#etap-2-walencja), nie ten.

## Implementation

`olski/morph.py` wraps Morfeusz 2, which supplies segmentation
and every reading of every form, choosing none of them.

`olski/grammar.py` is the formalism:
productions, symbols, and feature unification.
A grammar is Python data, like the rule packs.

That formalism is tier 0 of
[the cost ladder](design-notes.md#the-cost-ladder):
every feature value is a finite set of tagset atoms,
unification is intersection,
and a variable is scoped to the production that uses it,
so the grammar underneath the features is context-free,
for the reason [design-notes.md](design-notes.md#why-a-subset-really) gives.
Reading a segmentation graph rather than a string does not reach past it,
the context-free languages being closed under intersection with a regular one.
Tier 0 is where the implementation stands and not what the track is committed to;
[design-notes.md](design-notes.md#formalizm-jest-środkiem-a-nie-celem)
owns that distinction.

`olski/parse.py` enumerates distinct readings.
It is a memoizing top-down enumerator,
which is enough for a grammar without left recursion
and reports that case rather than looping.
It builds no forest,
and that is what the verdict wants sooner than the grammar does:
a sentence with several undecided attachments
is one role name in a reading list and would be several packed nodes.
[Werdykt jest zapytaniem o las](design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)
owns that argument and the chart parser it argues for.

`olski/subset.py` is olski itself:
the grammar, what it reads as one word,
the readings it declines to consider, and the verdicts.

```sh
python3 -m olski.check -c "Zapisz plik konfiguracyjny." --readings
```
