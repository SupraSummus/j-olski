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

## Co się liczy jako jedno czytanie

Dwa wyprowadzenia są jednym czytaniem, kiedy mają ten sam kształt.
Liczy się więc to, co strukturę zmienia:
która fraza jest podmiotem, co jest dopełnieniem
i gdzie przyłącza się modyfikator.
Rozmyślnie wyłączone są trzy rzeczy, a każda z innego powodu.

- **Lematy.** `zapisuje` należy i do `zapisywać`, i do `zapisować`.
  Polskie formy są homonimiczne wszędzie,
  więc liczone jako wieloznaczność odrzuciłyby prawie całą polszczyznę.
  Wieloznaczność leksykalna jest do rozstrzygnięcia dla czytelnika.
- **Wartości cech.** To, czy fraza stanęła na nijakiej mnogiej,
  czy na męskiej pojedynczej,
  nie jest rzeczą, między którą czytelnik wybiera.
  Zgodność wymusiła już unifikacja.
- **Części mowy.** Tam, gdzie część mowy zmienia strukturę,
  różni te wyprowadzenia już kształt,
  więc `do` jako przyimek i jako nuta dalej są dwoma czytaniami.
  Zostaje przypadek, w którym kształt jest ten sam,
  i tam nie ma czym różnicy uzasadnić.

Ostatnie z tych trzech jest odwróceniem
i stoi tu po to, żeby nikt go nie przywrócił przez przeoczenie:
część mowy liczyła się obok kształtu.
Rozstrzyga odsłownik.
Morfeusz daje formie `zdanie` czytanie `subst` i czytanie `ger`,
a produkcja z odsłownikiem w głowie grupy imiennej
dawałaby każdemu takiemu zdaniu drugie wyprowadzenie tego samego kształtu,
różniące się niczym, na co czytelnik mógłby zareagować.
Nie jest to jedna forma ani klasa rzadka.
Tę parę czytań niosą rzeczowniki,
którymi ten rejestr mówi o samym sobie:

```sh
python3 -c 'import sys
from olski.morph import analyse
for forma in sys.argv[1:]:
    print(forma, sorted({r.tag.pos for r in analyse(forma)[0].readings}))' \
  zdanie czytanie wyrażenie polecenie wejście wyjście dopełnienie żądanie
```

Drugie wyjście z tej klasy było wykluczeniem w słowniku
i stanęło na tym, że nie ma czego wykluczyć.
Olski takie wykluczenie ma i pyta ono o czytanie funkcyjne obok rzeczownikowego
([niżej](#the-dictionary-offers-readings-polish-does-not)),
a tutaj oba czytania są nominalne,
i szersze kryterium kasowałoby czytanie, które polszczyzna ma:
`zdanie` jest i rzeczą, i czynnością.
Wykluczenie odbiera formie czytanie, którego czytelnik nie ma,
a to nie jest ten przypadek.

Odwrócenie kupuje nad Składnicą 180723 sześć zdań,
które pod żywą morfologią przechodzą z wieloznacznych do przyjętych,
i ani jednego pod złotą, gdzie anotatorzy wybrali po jednym czytaniu na token;
totale obu przebiegów trzyma
[corpus.md](corpus.md#what-morphological-ambiguity-costs).
Nad prozą README nie rusza ani jednego werdyktu.

Te sześć zdań stoi na trzech parach części mowy i na dwóch mechanizmach.
Dwie pary bierze jeden terminal:
`Dziewczyna milknie zakłopotana.` stoi na `adj|ppas`,
a `Mam ogromną prośbę.` na `fin|impt`.
Trzeciej nie bierze żaden.
`Znam go.` ma `subst` obok `ppron3`,
a te dochodzą do grupy imiennej dwiema różnymi produkcjami,
z których każda robi ją z jednego słowa.

Ta trzecia jest zarazem czytaniem, którego polszczyzna nie ma,
tyle że wziętym z drugiej strony.
`go` jest grą i jest nieodmienne dokładnie tak jak nuta,
więc wykluczenie ze słownika byłoby tu na miejscu i nie sięga,
bo zaimek do klas zamkniętych nie należy.
Kształt załatwia to za darmo,
bo dopełnieniem jest tu jedno słowo tak czy tak.

Reszta tego, co się kupuje, dopiero przyjdzie:
odsłownik dopisany do gramatyki podnosi pokrycie, zamiast je obniżać,
i to jest warunek, pod którym
[roadmap.md](roadmap.md#etap-6-reszta-konstrukcji) go bierze.

To jest to rozróżnienie, na którym
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
się przewrócił i to zapisał:
liczenie prób zamiast wyników
kazało tamtemu narzędziu milczeć nad wierszami, które zrozumiało bez reszty.

## The dictionary offers readings Polish does not

A word read as a noun rather than as a function word
lands in a different shape,
so by the rule above it is a second reading.
One class of those is a second reading no Polish speaker has.

Morfeusz reads `do` as the preposition and as the musical note,
and the note is indeclinable:
its tag carries all seven cases at once.
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

### Dwa szersze kryteria zmierzono i żadne nie stoi

Wykluczenie sięga czytania nieodmiennego i dalej nie sięga.
Dwa kryteria, które szły dalej, mają cenę policzoną
na 13 035 lasach Składnicy z pełnym drzewem,
a miarą jest to, ile z nich traci czytanie wybrane przez anotatorów.
Tą samą miarą [corpus.md](corpus.md#what-morphological-ambiguity-costs)
liczy wykluczenie, które stoi, i wychodzi mu pięć.

**Wielka litera z początku zdania nie jest świadectwem nazwiska.**
Morfeusz daje formie `Celem` lemat `Cel` obok lematu `cel`,
a wielką literą zaczyna się każde zdanie,
więc na pierwszej pozycji ta litera o wyrazie nie mówi nic.
Kryterium, które kasuje tam czytanie o lemacie różniącym się od innego
czytania tej samej formy samą wielką literą,
traci 88 zdań — `Paweł`, `Niemcy`, `Bóg`, `Nowak`, `Róża` —
i nie kupuje ani jednego.
Kupić nie ma czego, bo taka para nie jest dwoma czytaniami:
[czytanie jest swoim kształtem](#co-się-liczy-jako-jedno-czytanie),
a nazwisko i rzeczownik pospolity stają w tym samym miejscu tego samego drzewa.
Drugie czytanie tego zdania robił zaimek rzeczowny,
którego dopełniacza [gramatyka nie bierze](#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
i to jest ta różnica, przy której kryterium na wielką literę
mierzyło coś, czego nie było.
Klasa kosztuje więc trafność, a nie jednoznaczność,
bo czytanie nazwy własnej bywa jedynym, które coś licencjonuje,
i tak wychodzi `Tam siedzi nasz umrzyk.` z
[corpus.md](corpus.md#what-morphological-ambiguity-costs),
gdzie kosztem jest jedno czytanie zdania przeczytanego na opak.
Tam sięga wykluczenie wyżej, bo nazwisko jest w tej formie nieodmienne,
a odmienne zostaje w słowniku i tego wyprowadzenia nikt mu nie odbiera.

**Rzeczownik odprzymiotnikowy przed dopełniaczem jest zwyczajny.**
`dobry` ma obok czytania przymiotnikowego czytanie `subst`,
a `kod` czytanie lematu `koda` w dopełniaczu mnogim,
więc `Linter pomaga pisać dobry kod.` wychodzi dwoma czytaniami:
raz jest to przymiotnik przed rzeczownikiem,
a raz rzeczownik z dopełniaczem po nim.
Te dwa różnią się częścią mowy, więc są dwoma.
Kryterium, które kasuje czytanie `subst` formy znanej też jako przymiotnik,
gdy stoi ona przed rzeczownikiem z czytaniem w dopełniaczu,
traci 155 zdań, i tracą je te, w których taki rzeczownik dopełniaczem rządzi:
`przewodniczący Rady`, `ministrowi spraw`, `prawa jazdy`, `dobra kraju`.
Zostaje drugie miejsce, w którym tę parę da się rozciąć, czyli sąsiad:
`koda` jest wyrazem, którego ten rejestr nie zna,
a rzadkość formalnego znamienia nie ma,
więc kryterium na nią żąda liczby z korpusu, której olski nie ma.
[TODO.md](../TODO.md) trzyma to, co z tej klasy zostaje otwarte,
wraz z pomiarem mówiącym, że nad prozą tego repozytorium
niesie ją paradygmat zaimkowy, a nie przymiotnik.

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
który Morfeusz daje `menu` i `atelier`.
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
  and it is closed because it is the one entry of the valency lexicon
  that is written by hand
  ([below](#walencja-jest-leksykonem-o-ramie-domyślnej)),
  which is what keeps an instrumental adjunct from reading as a predicative
  under every other verb —
  the mistake [corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)
  counts on `Kwitnie handel paszportami.`
  What the list leaves out is the copula that takes `się`:
  `okazać się` and `stać się` govern the same case
  and the production has no place for the particle.
- What a verb takes, from a lexicon rather than from a production:
  `być` takes no accusative object,
  so `On jest wolny.` loses the reading in which `wolny` is one.
- The register's own notation as an indeclinable noun:
  `Zobacz docs/subset.md.`, argued above
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
  a genitive modifier, or a prepositional modifier,
  and an adjective after the noun with a genitive under it as well:
  `dobrem wspólnym wszystkich obywateli`, which is how the register of statutes
  names a term and then says whose it is
  ([ustawy.md](ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa))
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

### Przecinek zmierzono i nie odbiera ani jednego zdania

Znakiem koordynacji jest spójnik albo przecinek, na każdym z trzech poziomów,
więc `Wstaję, wyglądam przez okno.` wyprowadza się i wyprowadza raz.
Argumentem przeciw niemu jest jednoznaczność:
przecinek między zdaniami składowymi konkuruje z przecinkiem w grupie imiennej
wszędzie tam, gdzie po przecinku stoi rzeczownik,
a zdanie, które przez to wychodzi dwoma czytaniami, olski odrzuca.
Cenę tej konkurencji liczy `sonda/przecinek.py` i wychodzi zero,
i to jest ta liczba, na której przecinek w tej gramatyce stoi.

Mierzony jest ruch werdyktu, a nie stan gramatyki:
zdanie idzie przez tę gramatykę i przez tę samą z wyjętą produkcją,
a liczy się to, na czym te dwa werdykty się różnią.
Poziomy zdejmują się osobno, bo cena każdego z nich jest osobną liczbą.

```sh
python3 -m sonda.przecinek Składnica-frazowa-180723/
```

| wariant | przyjęte | wieloznaczne | odrzucone |
| --- | --- | --- | --- |
| bez przecinka | 296 | 114 | 12 615 |
| zdaniowy | 310 | 114 | 12 601 |
| imienny | 304 | 119 | 12 602 |
| przymiotnikowy | 296 | 114 | 12 615 |
| wszystkie trzy | 318 | 119 | 12 588 |

Mianownik jest ten sam, co w tabelach tamtego dokumentu:
13 035 lasów Składnicy z pełnym drzewem, morfologia złota,
a poza pomiarem zostaje dziesięć zdań dłuższych niż czterdzieści segmentów,
na które enumerator nie ma budżetu.

Ani jedno zdanie nie przechodzi z przyjętego na wieloznaczne.
Wieloznacznych przybywa pięć i wszystkie pięć przychodzi z odrzuconych,
czyli z tych, których gramatyka bez przecinka nie wyprowadzała wcale.
Konkurencji między poziomami sonda nie liczy z tych sum, tylko wprost,
zdanie po zdaniu, i nie znajduje jej ani razu:
żadnego zdania nie ruszają poziom zdaniowy i imienny naraz,
i o żadnym oba naraz nie mówią czego innego niż każdy z osobna.
Argument o konkurencji nie ma więc nad tym korpusem czego mierzyć.

Po drugiej stronie stoi zakup: dwadzieścia dwa zdania przechodzą
z odrzuconych na przyjęte, czternaście za poziom zdaniowy i osiem za imienny.
Osiemnaście z nich ma role zgodne z drzewem wzorcowym,
cztery nie mają w nim żadnej roli do porównania,
a odwróconych i niezgodnych nie ma ani jednego,
więc są to zdania przeczytane tak, jak przeczytali je anotatorzy.

Pięć nowych wieloznaczności nie bierze się z przecinka, tylko z przyłączenia.
`Warszawska kuria metropolitalna ma wśród swoich licznych włości nieruchomość
w podwarszawskim Skolimowie, uzdrowiskowej dzielnicy Konstancina-Jeziorny.`
wychodzi dwoma czytaniami, bo wyrażenie przyimkowe dochodzi do rzeczownika
albo do czasownika, i tak samo różnią się czytania pozostałych czterech.
Jest to ta sama wieloznaczność, którą olski
[oddaje czytelnikowi](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera):
koordynacja przecinkiem daje jej więcej miejsc, w których się mieści,
a nie nowy rodzaj sporu.

Poziom przymiotnikowy nie rusza ani jednego zdania w żadną stronę.
Czy jest to własność polszczyzny, czy tego korpusu, ta liczba nie mówi:
`duży, ciężki plecak` jest polszczyzną,
a nad Składnicą nie ma zdania, w którym ta produkcja byłaby ostatnią brakującą.

Nad rejestrem, o który olskiemu chodzi, przecinek kupuje dwa zdania.
To samo porównanie nad prozą wyciągniętą z README —

```sh
python3 -m harness.markdown README.md --into proza/
python3 -m sonda.przecinek proza/README.txt
```

— rusza dwa werdykty i oba na poziomie zdaniowym.
`Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego`
gramatyka bez przecinka odrzuca, a z nim wyprowadza jednym czytaniem,
a `Co ekstrakcja po drodze zmyśla, mówi docs/extraction.md`
przechodzi z odrzucenia w wieloznaczność.
Ani poziom imienny, ani przymiotnikowy nie rusza tu nic,
bo pozostałe zdania tego pliku, które niosą przecinek,
niosą też zdanie podrzędne, przysłówek albo rzeczownik odczasownikowy.
Przecinek wszedł więc za pokrycie w cudzej polszczyźnie,
a kryterium wyjścia toru czeka na to, co w reszcie tych zdań stoi obok niego,
i pierwsza jest tam podrzędność
([roadmap.md](roadmap.md#etap-4-zdanie-złożone)).

## Zaimek rzeczowny nie rządzi dopełniaczem

Morfeusz daje formom paradygmatu `ten` czytanie rzeczownikowe obok
przymiotnikowego: `tego` jest dopełniaczem przymiotnika `ten`
i dopełniaczem zaimka `to`, a `tym` narzędnikiem jednego i drugiego.
Produkcja, która daje głowie grupy imiennej dopełniacz po niej,
bierze oba: `parser tego podzbioru` jest przymiotnikiem przy rzeczowniku,
a drugi raz zaimkiem, który rządzi rzeczownikiem.
Te dwa drzewa mają różny kształt,
więc [są dwoma czytaniami](#co-się-liczy-jako-jedno-czytanie),
a nie jednym jak para lematów.
Bez warunku niżej `Celem jest parser tego podzbioru.` wychodzi dwoma czytaniami
o identycznym streszczeniu ról.

Drugiego z nich polszczyzna nie ma.
Zaimek rzeczowny stoi za przyimkiem i przy czasowniku — `do tego`, `tego nie wiem` —
a dopełniacza po sobie nie bierze,
więc nie jest to wieloznaczność, którą czytelnik ma rozstrzygać.
Warunek obejmuje więc każdą głowę, która rządzi dopełniaczem,
i mówi tyle: taka głowa nie jest zaimkiem rzeczownym.
Produkcji z nią jest cztery, bo pod głową może stać jeszcze przymiotnik,
wyrażenie przyimkowe albo jedno i drugie.
Gdzie indziej czytanie zostaje, bo gdzie indziej jest tym, czym w polszczyźnie jest.

Jest to pierwszy warunek ujemny w tej gramatyce i lemat jest tym,
na czym wolno go postawić.
Cechy takiego warunku mieć nie mogą:
unifikacja jest przecięciem, a przecięcie negacji nie zna,
więc żądanie „nie bądź w narzędniku” nie jest żądaniem,
które da się postawić środowisku cech.
Lemat leży poza unifikacją, bo jest osobnym testem w `bierze`
z `olski/grammar.py`, więc negacja jest tam tym samym testem odwróconym.
Symetria jest zatem z `lemmas`, a nie z cechami,
i to samo rozstrzygnęło, czym jest klasa domyślna
[leksykonu walencyjnego](#walencja-jest-leksykonem-o-ramie-domyślnej):
bierze ona każdy lemat, którego leksykon nie wymienia,
i jest to drugi warunek ujemny, jaki ta gramatyka stawia.

Cena jest zerowa i jest to wynik pomiaru, a nie założenie.
Pod złotą morfologią przebieg nad Składnicą nie rusza się o ani jedno zdanie,
bo tam każda forma ma jedno czytanie wybrane przez człowieka.
Pod Morfeuszem [warunek podnosi liczbę zdań przyjętych](corpus.md#what-morphological-ambiguity-costs),
a jedyne zdanie, które odrzuca, stało na frazie, której polszczyzna nie ma.
Cała ta cena idzie na dwie z tych czterech produkcji, te bez przymiotnika:
na pozostałych dwóch warunek nie rusza ani jednego zdania żadnego z korpusów,
bo `to` z przymiotnikiem i dopełniaczem pod nim nie pojawia się w nich ani razu.
Jest tam więc z wywodu, a nie z pomiaru.

## Walencja jest leksykonem o ramie domyślnej

Czasownik bierze te dopełnienia, których wymaga,
a nie te, które pasują kształtem.
`być` nie bierze dopełnienia w bierniku,
a `On jest wolny.` ma czytanie, w którym bierze:
`wolny` czyta się jako przymiotnik i jako rzeczownik,
a rzeczownikowe staje tam, gdzie produkcja czeka na biernik,
[więc są to dwa czytania](#co-się-liczy-jako-jedno-czytanie).
Takiego czytania nie ma żaden czytelnik tego zdania.

Ramą jest zbiór dopełnień, jakie czasownik bierze,
nazwanych przypadkiem grupy, którą bierze,
wraz z `inf` dla bezokolicznika, bo bezokolicznik przypadka nie ma.
Czasownik wypuszcza ramę z siebie jako cechę,
dopełnienie mówi, którą pozycję ramy zajmuje,
i zgadza je ta sama unifikacja, która zgadza rodzaj z liczbą.
Walencja nie jest więc sprawdzeniem doklejonym do rozbioru, tylko rozbiorem,
dokładnie tak jak [zgodność](#what-the-grammar-covers).

Leksykon jest otwarty i ma ramę domyślną.
Stoi w nim czasownik, którego rama jest węższa niż domyślna,
a każdy inny bierze domyślną,
więc czasownik dopisuje się wpisem, a nie produkcją,
i nie kosztuje ani jednego przyjętego zdania, dopóki wpisu nie ma.
Ręcznie stoi w nim jeden wpis i jest nim kopula:
narzędnika rama domyślna nie ma, a biernika nie ma rama kopuli.
Reszta wpisów bierze się z Walentego i mówi o lemacie tyle,
ile któryś z kierunków ma z tego czym zapytać, o czym niżej.

Rama domyślna nie jest wygodą, tylko warunkiem, żeby żądanie było żądaniem.
Cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc rama postawiona części czasowników przechodziłaby reszcie za darmo
i „bądź kopulą” nie byłoby wtedy żądaniem.
Jest to zarazem argument, dla którego kopula osobnym symbolem gramatyki nie jest,
choć wygląda na argument za nim:
rama, którą niesie każdy czasownik, żąda tego samego,
a osobny symbol daje jednemu lematowi dwie nazwy w raporcie —
`Ludzie są wolni.` czytałoby się przez jedną, a `Jan jest nauczycielem.` przez drugą.

Rama nie zastępuje przy tym pozycji, i to jest zmierzone.
Orzecznik stoi w trzech miejscach — po czasowniku, po podmiocie w szyku
z czasownikiem na czele, i przed czasownikiem — a rama każe zapytać,
czy te trzy nie są jedną pozycją, w której orzecznik i czasownik dzielą zmienną.
Nie są, i widać to na tym, co zlanie ich w jedną przyjmuje.
Pozycja po podmiocie wpuszcza wtedy kopulę z narzędnikiem,
czyli `Jest Jan nauczycielem.`, którego olski nie ma, a polszczyzna ma,
i to jest cały zysk.
Nad Składnicą tego zdania nie ma, a są dwa inne,
i oba wychodzą przeczytane na opak.
`Na to jest zbyt wielkim tchórzem.` dostaje wtedy podmiot `zbyt`,
a `Inne wymagają ustalenia.` podmiot `ustalenia`;
to drugie przychodzi z pozycji przed czasownikiem,
kiedy wpuścić do niej czasownik, który kopulą nie jest.
Dwa zdania przyjęte więcej i dwa przeczytane na opak
to ta sama zamiana, którą [corpus.md](corpus.md#what-morphological-ambiguity-costs)
liczy w drugą stronę i tam nazywa najgorszym wyjściem tego pomiaru,
więc każda z trzech pozycji zostaje przy swoim żądaniu wobec czasownika.

Zwinięcie kopuli w ramę daje jej przy tym pozycję, do której osobny symbol nie sięga.
Rama dochodzi do bezokolicznika tą samą drogą, co do formy osobowej,
więc `mogą być interesującym materiałem` się wyprowadza,
a produkcja wypisana osobno dla formy osobowej sięga tylko jej.

Cena i zysk kopuli są zmierzone i stoją po jednej stronie morfologii.
Pod złotą morfologią przebieg nad Składnicą nie rusza się o ani jedno zdanie
ani o ani jedno czytanie,
bo anotatorzy wybrali po jednym czytaniu na token
i czytania, które rama zdejmuje, nie ma tam czego zdejmować.
Pod Morfeuszem rama zabiera te zdania,
w których `być` bierze biernik i jest to jedyne ich czytanie,
a daje jednoznaczność tym, które stoją na nim obok czytania prawdziwego;
[corpus.md](corpus.md#what-morphological-ambiguity-costs) trzyma liczby
i zdania, które za nimi stoją.

### Leksykon mówi trzy zdania na lemat i bierze je z Walentego

Wpis pisany ręcznie kosztuje tyle, co rozstrzygnięcie o jednym czasowniku,
a rama ma obowiązywać wszędzie, więc źródłem jest słownik zrobiony po to.
[Walenty](prior-art.md) charakteryzuje 17 224 lematy czasownikowe
64 022 schematami i idzie na licencji CC BY-SA 4.0.
Mówi przy tym o czasowniku znacznie więcej, niż te dwa kierunki umieją żądać,
więc przekład jest zejściem w dół i bierze z Walentego trzy zdania na lemat.
Pierwsze jest ujemne i mówi, że czasownik nie bierze dopełnienia w bierniku.
Drugie jest twierdzące i mówi, że bierze bezokolicznik,
którego wykonawcą jest jego własny podmiot.
Trzecie jest twierdzące jak drugie i mówi, że bierze zdanie podrzędne
wprowadzone przez `że`, czyli że stoi przy nim to, co ktoś mówi albo wie
([sklad.md](sklad.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi)).
Kierunek pierwszego jest przeciwny niż dwóch pozostałych,
bo przeciwne są domyślności, od których odejmują:
rama domyślna ma dopełnienie w bierniku, a nie ma ani bezokolicznika,
ani zdania podrzędnego.
`olski/walenty.py` jest tym przekładem i wypisuje `olski/leksykon.txt`,
czyli lematy wraz z tym, które z tych zdań są o nich prawdziwe;
9 525 stoi ich tam dziś, licząc formy zwrotne osobno,
z czego 7 941 niesie zdanie pierwsze, 285 drugie, a 2 498 trzecie.
Ramy ten plik nie niesie, bo rama jest słowem gramatyki, a nie słownika.
Nazywa ją `olski/subset.py` razem z domyślną, od której ją odejmuje.
Czyta go `olski/walencja.py`, i czyta dla obu kierunków naraz,
bo rama jest faktem o słowie, a nie o kierunku, w którym się go używa;
wywód trzyma [design-notes.md](design-notes.md#the-round-trip-invariant).

Wspólny jest przy tym plik, a nie każde zdanie, które on mówi.
Biernik czytają oba kierunki, a bezokolicznik czyta sam skład,
i nie jest to niezgoda o fakt, tylko różnica w tym, co ten fakt komu kupuje.
Po stronie generatora jest jedyną obroną przed drzewem,
które żąda bezokolicznika od czasownika, który go nie bierze,
bo bezokolicznik z niczym się nie zgadza i pomyłka nie ma jak wyjść inaczej.
Po stronie parsera został zmierzony i pomiar stoi niżej w tej sekcji.

Zdanie trzecie czyta sam skład i jest to inny rodzaj rozdziału niż tamten.
Bezokolicznik gramatyka ma i zmierzono, ile jej czytanie o nim kupuje;
zdania podrzędnego nie ma wcale, więc po tamtej stronie nie ma nawet pozycji,
o którą to pytanie miałoby pytać, i nie ma czego mierzyć.
Obrona jest za to po tej stronie tej samej wagi co przy bezokoliczniku:
`zamykać` bierze biernik, a `Kot zamyka, że mysz śpi.` nie jest zdaniem polskim,
i leksykon jest jedyną rzeczą, która te dwa czasowniki rozdziela.

Zwrotność jest drugim wymiarem klucza, a nie częścią lematu.
Morfeusz daje `otwierać` i `otwierać się` ten sam lemat,
a wziąć mogą co innego,
więc rama trzymana pod samym lematem zlewałaby te dwa czasowniki w jeden.
Widać to na parze zdań, w której jedno przechodzi, a drugie nie:
`Otwierają się drzwi.` wyprowadza się jednym czytaniem z podmiotem `drzwi`,
a `Otwierają drzwi.` zostaje wieloznaczne, bo tam biernik stoi w ramie.

Narzędnika przekład nie bierze, choć Walenty go zna.
`inst` jest u olskiego pozycją orzecznika,
a Walenty nie odróżnia jej od argumentu narzędnikowego — `bawić się czymś` —
więc wpis wzięty stamtąd wpuszczałby orzecznik tam, gdzie polszczyzna ma dopełnienie.
Dlatego kopula zostaje listą pisaną ręcznie.

Bezokolicznik ma u Walentego dwa kształty, a nie jeden,
i różnicę między nimi niesie kontrola, czyli to, kto wykonuje to,
o czym mówi pozycja podrzędna.
U `chcieć` etykietę kontrolującą nosi pozycja podmiotu,
więc `Córka krawca chciała zejść.` mówi, że zeszłaby ona.
U `kazać` nosi ją pozycja celownikowa,
więc `Krawiec kazał córce zejść.` mówi, że zeszłaby córka.
Przekład bierze pierwszy z tych kształtów i nie bierze drugiego,
bo celownika ta gramatyka nie ma i wykonawcy nie miałaby czym postawić.
Zdanie leksykonu jest przez to zdaniem o kontroli, a nie o samym kształcie frazy,
i tyle wystarcza, żeby skład nie musiał o kontrolę pytać drugi raz.

Czyta to zdanie na razie sam skład, a nie parser, i to jest wynik pomiaru.
Gramatyka odmawiająca bezokolicznika tym lematom, którym odmawia go Walenty,
przyjmuje nad Składnicą dwa zdania mniej
i nie kupuje za to ani jednej jednoznaczności.
Płaci za to cząstka `się`, która staje przy formie osobowej,
należąc do bezokolicznika za nią:
`Zebranie ma się odbyć.` jest u olskiego czasownikiem `mieć się`,
któremu Walenty bezokolicznika nie daje.
Pomiar mówi o odmowie, a nie o wpisie,
więc zdanie stojące w pliku i nieczytane przez parser nie kosztuje tam nic.

Bank drzew mówi o walencji sam.
Frazy wymagane niosą w Składnicy swoją pozycję,
więc każde zdanie z werdyktem `FULL` daje ramę swojego czasownika,
a 13 035 takich zdań daje 17 896 wystąpień czasownika i 2 856 lematów.
Źródłem ramy bank być nie może, bo 1 328 z tych lematów widać w nim raz,
a rama wyprowadzona z jednego zdania zabrania wszystkiego, czego to zdanie nie miało.
Sprawdzianem być może: z 616 lematów,
którym Walenty odmawia biernika i które bank drzew zna,
potwierdza 615.
Jedynym sprzecznym jest `być` z 61 wystąpieniami,
i są to zaprzeczone zdania egzystencjalne,
w których pozycja `accgen` jest dopełniaczem, a nie biernikiem,
czyli konstrukcja, [której olski nie ma](#what-it-does-not-cover-yet).
Liczby tego akapitu bierze się ręcznie nad tym samym bankiem,
tak jak te, o których mówi [corpus.md](corpus.md#fetching-it),
bo `olski/corpus.py` czyta z pola `tfw` dwie role, a nie całą ramę;
co by kosztowało polecenie, trzyma [TODO.md](../TODO.md).

Cena i zysk są zmierzone nad Składnicą i idą w obie strony.
Pod żywą morfologią przebieg przyjmuje 379 zdań zamiast 374,
a wieloznacznych ma 245 zamiast 267.
Odrzuconych przybywa przy tym siedemnaście,
i jest to jedna klasa: zdanie stało na dopełnieniu, którego w nim nie ma.
`Wzrośnie w tym roku dostępność studiów wyższych.`
czytało się z dopełnieniem `dostępność studiów wyższych`,
`Uczy się wykorzystania odpowiednich narzędzi.` z dopełnieniem `wykorzystania`,
które jest tam dopełniaczem liczby pojedynczej, a czytało się jako biernik mnogiej,
a `Pracujemy nad tą grupą dzień i noc.` z dopełnieniem `dzień i noc`,
które jest okolicznikiem w bierniku, a takiego okolicznika olski nie ma.
Ani jedno z tych czytań nie jest czytaniem, które ma czytelnik,
więc odrzucenie stoi tu w miejscu analizy fałszywej, a nie w miejscu trafnej.
To ostatnie zdanie jest zarazem jedynym, o które rusza się przebieg pod złotą
morfologią: jedno z 294 przyjętych zdań ubywa i nie ubywa ani jedno czytanie,
bo anotatorzy wybrali po jednym czytaniu na token.

Plik wejściowy nie stoi w repozytorium, tak samo jak bank drzew:

```sh
curl -L -o walenty.zip \
  'http://zil.ipipan.waw.pl/Walenty?action=AttachFile&do=get&target=walenty_20160418-text.zip'
unzip walenty.zip
python3 -m olski.walenty walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt \
  > olski/leksykon.txt
```

Wpis wyprowadzony z Walentego jest utworem zależnym od niego,
więc `olski/leksykon.txt` niesie w nagłówku atrybucję i tę samą licencję.

Leksykon zamyka tyle, ile mówi, i widać to na zdaniu, które go doczekało.
`Działają dwie rzeczy.` czekało na wpis mówiący, że `działać` dopełnienia nie bierze,
i wpis ten stoi, a zdanie dalej się nie wyprowadza:
zatrzymuje się teraz na liczebniku,
czyli na [konstrukcji, której olski nie ma](#what-it-does-not-cover-yet),
a nie na ramie.

## What it does not cover yet

Each of these is a sentence that gets rejected and should not be,
except subordination, which gets accepted and should not be:

- A comma standing in front of a conjunction.
  Two clauses join with a conjunction or with a comma
  ([above](#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania))
  and not with both at once,
  so `Plany są niczym, ale planowanie jest wszystkim.`
  gets past the comma and fails on `ale`,
  which is how Polish punctuates that coordination.
- The past tense, which
  [corpus.md](corpus.md#where-the-analyses-stop)
  ranks as the cheapest large gain left.
- Subordination with `że` and `który`, which is not merely missing.
  A `który` clause after a comma derives as a coordination of clauses,
  the comma being admitted at that level
  ([above](#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania)),
  so `Ustawy określają, które zadania gminy mają charakter obowiązkowy.`
  comes back valid with `które zadania gminy` for the subject of a second clause.
  One reading, confidently wrong, is worse than a refusal,
  and it is what admitting the comma without subordination buys:
  [ustawy.md](ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa)
  found one such sentence counted as coverage.
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

- **Valency, past the accusative.**
  The lexicon [above](#walencja-jest-leksykonem-o-ramie-domyślnej)
  records which verbs take no accusative object and nothing else,
  so an agreeing predicative and an infinitive still go to every verb,
  and so does the accusative for a lemma Walenty does not carry.
  The infinitive is the position that was measured and left alone,
  and what it waits on is `się` reaching the verb it belongs to
  rather than the one it stands beside.
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
  `Pythonem` is a noun in the instrumental and `commitów` a genitive plural,
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

Ile ta decyzja kosztuje nad rejestrem, a nie nad bankiem drzew,
jest zmierzone osobno i wychodzi wysoko:
pozycję dwuznaczną niesie większość zdań polskiej dokumentacji,
a czytelnik ma nad nią jedno rozumienie.
Decyzji to nie przewraca, bo liczby wyżej mówią o tym,
czego nie da się zgadnąć, a nie o tym, co czytelnik widzi,
i te dwie rzeczy są prawdziwe naraz.
Rachunek wraz z próbką przeczytaną ręką trzyma
[open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma).

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
- po rzeczowniku, który już ma przy sobie przymiotnik, dopełniacz albo oba
  (`akcja zbrojna w Strefie Gazy`, `zadania ochrony ludności w gminie`),
  oraz po imiesłowie (`powiązani z interesami postkomunistów`)

Wierszy jest sześć, a produkcji dwadzieścia dwie,
bo pozycja powtarza się w każdym szyku, który ją ma,
a szyk jest w tej gramatyce osobną produkcją.
Liczy się je tak, jak się je zdejmuje, a granica biegnie tak.
Wchodzi produkcja, w której `Adjuncts` stoi obok czegoś jeszcze,
w tym obok drugiego okolicznika,
oraz ta, w której `Modifier` dochodzi do głowy mającej już przydawkę
albo do imiesłowu.
Nie wchodzi `NPConjunct → subst Modifier`, czyli naga głowa z okolicznikiem:
jest to sama grupa imienna z wyrażeniem przyimkowym,
a nie drugie miejsce, w którym to wyrażenie się mieści.
Granica jest wypisana dlatego, że liczba nad nią jest zapisana w dwóch dokumentach,
a policzyć ją drugi raz można tylko wtedy, gdy wiadomo, co się liczy.

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
gramatyka bez tych pozycji czyta wbrew ręcznemu rozbiorowi dwadzieścia zdań,
a z nimi jedno, i to jedno nie jest wyborem, którego olski dokonał.
Liczby trzyma
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance).

Klasa nie jest przez to zamknięta.
Zdejmuje z niej tę część, w której czasownik frazy wymaga —
576 z 4 517 wyrażeń wyżej, czyli 13% —
[leksykon walencyjny](#walencja-jest-leksykonem-o-ramie-domyślnej),
bo tam czytanie rzeczownikowe łamie schemat czasownika,
a nie konkuruje z nim.
Leksykon nie sięga do tych 13% nigdzie,
bo mówi o bierniku, a fraza wymagana jest tu przyimkowa,
więc liczba mówi, co zdjąłby leksykon dochodzący do każdej pozycji,
a nie co zdejmuje ten.

## Implementation

`olski/morph.py` wraps Morfeusz 2, which supplies segmentation
and every reading of every form, choosing none of them.

`olski/grammar.py` is the formalism:
productions, symbols, and feature unification.
A grammar is Python data rather than a notation of its own.
It also answers whether any terminal takes a reading at all,
which is what lets a rejected sentence say what it stood on:
[więzy wyprowadzone z gramatyki](design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)
owns why that question belongs here rather than in a layer beside the grammar.

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
