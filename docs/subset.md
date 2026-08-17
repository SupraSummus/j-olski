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

One of those exclusions bounds how far the property reaches.
A phrase has to be a contiguous stretch of text,
so a sentence whose second reading needs a discontinuous one
is let through carrying a single reading,
and the verdict says nothing about the reading it could not derive.
How many sentences that is, and what admitting them would cost instead,
is measured by
[what discontinuity buys and costs](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze).

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

- Clauses in all six orders the subject, the object and the verb stand in,
  from `Program zapisuje ustawienia.` to `Zapisuje ustawienia program.`,
  which is priced [below](#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery)
- Subjectless clauses, both imperative (`Zapisz plik.`)
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
- Negation, with the genitive it demands of an object,
  through an infinitive chain and into a fronted relative pronoun:
  `Program nie zapisuje ustawień.`, `Nie chcę czytać książki.`,
  `polszczyzna, której nikt nie napisał`
  ([below](#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem))
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
- The past tense, agreeing with the subject in gender as well as in number,
  and with the person clitic Morfeusz cuts off the form:
  `Program zapisywał ustawienia.`, `Napisałem program.`
  What it costs is [below](#czas-przeszły-żąda-rodzaju-od-każdego-szyku)
- A `że` clause as what a verb takes, which is a position in its frame
  rather than a construction beside the others:
  `Mieszkańcy grożą, że zablokują ulice.`
- A relative clause on a noun phrase, agreeing with it in number and gender,
  with the pronoun standing for the subject, for the object
  or under a fronted preposition:
  `Widoczny jest wzrost aspiracji społeczeństwa, które chce zdobywać wykształcenie.`
  Both are argued and priced
  [below](#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja)
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

## Czas przeszły żąda rodzaju od każdego szyku

W kolejce ze Składnicy czas przeszły stał na pierwszym miejscu
jako kolejna forma czasownika w produkcji `Verb`
([corpus.md](corpus.md#where-the-analyses-stop)).
O mocy formalizmu opis ten był trafny — gramatyka dalej jest bezkontekstowa —
a o jednej produkcji nie.
Forma `praet` niesie rodzaj i liczbę, a osoby nie niesie wcale,
czyli dokładnie odwrotnie niż `fin`,
więc zgodność, którą czas teraźniejszy zostawiał grupie imiennej,
przechodzi w czasie przeszłym przez orzeczenie.
Rodzaj wchodzi przez to do każdego szyku zdania,
bo `lista stała` i `wywód stał` różni sam rodzaj podmiotu,
a szyk, który rodzaju nie przepuszcza, przyjmuje `lista stał`.
Dwa symbole podmiotu zlały się przy tym w jeden:
szyk bez rodzaju przestał się różnić od szyku z rodzajem,
odkąd rodzaju żąda każdy.

Osobę pierwszą i drugą wnosi w tym czasie osobny segment.
Morfeusz odcina od formy końcówkę osobową — `napisałem` to `napisał` i `em` —
i to ona niesie liczbę oraz osobę,
więc czasownik dostaje trzy ciała zamiast jednego:
`fin` albo `impt`, samo `praet` z osobą trzecią wpisaną w produkcję,
oraz `praet` z aglutynantem.
Bez wpisanej trzeciej osoby `Ja napisał program.` wyprowadza się,
bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza.

Pod złotą morfologią czas przeszły nie odbiera Składnicy ani jednego zdania —
żadne przyjęte nie traci werdyktu i żadne nie zyskuje drugiego czytania —
a przyjętych przybywa 365 i wieloznacznych 201,
czyli 566 zdań z 2934, które na tej formie stawały.
Różnica między 566 a 2934 jest tym,
czego kolejka blokerów z zasady nie mówi:
liczy zdania, na których konstrukcja stanęła,
a nie te, które jej dopisanie przyjmuje,
i większość tamtych zdań niesie obok czasu przeszłego jeszcze coś.
Widać to po samej kolejce, która po tej zmianie stawia w tym wierszu 297:
2071 zdań przesunęło swój bloker w prawo, zamiast zejść z listy.

Nad rejestrem, o który olskiemu chodzi, zakup jest zerowy albo ujemny.
Nad [README](../README.md) kupuje jedno zdanie i jedno traci,
bo `dzieli` ma u Morfeusza czytanie `praet:pl:m1`,
którego polszczyzna w tym zdaniu nie ma
([wyżej](#the-dictionary-offers-readings-polish-does-not) trzyma tę klasę),
a nad siedmioma ustawami nie kupuje ani jednego zdania
i pięć przenosi z odrzuconych na wieloznaczne
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)).
Kolejka ze Składnicy i przebieg nad tą prozą dają więc różne odpowiedzi,
i dopiero oba pomiary razem mówią, ile ta konstrukcja jest warta.

## Negacja żąda dopełniacza i żąda go ponad bezokolicznikiem

Cząstka `nie` stoi przed formą czasownika, a przypadek dopełnienia zmienia
w całym zdaniu: `Program zapisuje ustawienia` bierze biernik,
`Program nie zapisuje ustawień` żąda dopełniacza, i żąda go obowiązkowo.
Dopełniacz negacji jest przez to drugą produkcją tej samej pozycji ramy,
a nie drugą pozycją: to samo miejsce u czasownika,
inny przypadek grupy, która je zajmuje.

Sięga on dalej, niż stoi cząstka.

```text
Program nie pozwala zapisać ustawień.
```

Przeczy tu forma osobowa, a przypadek zmienia się dopełnieniu,
które wisi pod bezokolicznikiem, i tak samo przez łańcuch dowolnej długości.
Rządzenie przechodzi więc przez konstytuent, czego zgodność nie robi nigdzie,
a mimo to jedzie kanałem cech, tym samym, którym jedzie rama.
Na jakich warunkach ten kanał je wpuścił, wywodzi
[design-notes.md](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne).

Fraza bezokolicznikowa z własną cząstką tej cechy nie wypuszcza wcale
i tym zamyka przenoszenie:
`Program ma nie zapisywać ustawień` przeczy bezokolicznikowi, a nie formie
osobowej nad nim, więc żądanie z góry ma tu nie dojść.
Nieobecność cechy jest tym samym mechanizmem, którym grupa współrzędna nie niesie
rodzaju. Ta sama droga sięga wysuniętego zaimka względnego —
`polszczyzna, której nikt nie napisał` obok `polszczyzna, którą ktoś napisał` —
i tam kosztuje najwięcej, bo przypadek zaimka rozstrzyga przeczenie stojące za
całą resztą zdania składowego, więc sześć ciał `RelativeCore` rośnie do dwunastu.

Poza biernik dopełniacz negacji nie sięga.
Orzecznik narzędnikowy stoi przy `nie jest` tak samo jak przy `jest`,
grupa pod przyimkiem zostaje w przypadku, którego przyimek żąda,
a czasownik, o którym leksykon mówi, że biernika nie bierze,
nie zyskuje przy przeczeniu nowej pozycji.

### Negacja zmierzona: kupuje przeszło sto zdań i odbiera jedno

Pełne wiersze są w [figury/negacja.txt](../figury/negacja.txt),
a wzięte nad prozą README w [figury/negacja-proza.txt](../figury/negacja-proza.txt);
polecenie i pliki, których zmiana każe je przeliczyć,
podaje każdy z tych dwóch ([`harness/figury.py`](../harness/figury.py)).

Dopełniacz bez cząstki nie kupuje ani jednego zdania i to jest o nim odczyt, a nie
przeoczenie: dopełniacza negacji nie licencjonuje nic poza czasownikiem, który
przeczy, więc bez cząstki nie ma on jak wystrzelić.
Cząstka sama kupuje dwie trzecie tego, co obie razem,
a resztę dokłada przypadek, i są to zdania, których cząstka sama nie unosi,
więc te dwie rzeczy są jedną konstrukcją mierzoną z dwóch stron.

Ani jedno ze zdań przyjętych wcześniej nie traci jednoznaczności,
i nie znaczy to, że dopełniacz z niczym nie konkuruje.
Konkuruje, i to z przydawką dopełniaczową, bo obie stawiają ten sam przypadek,
a przed czasownikiem gramatyka ma dziś oba ciała naraz.
Ta konkurencja nie wypada jednak w tym przebiegu,
bo wariant bez negacji dopełniacza w pozycji dopełnienia nie ma wcale,
więc nie ma tam czego z przydawką pomylić.
Wypada ona w sondzie, która mierzy szyk, i wynosi tam cztery zdania
([niżej](#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery)).
Zero w kolumnie zdań wieloznacznych mówi więc, że cena tego sporu należy do szyku,
a nie do negacji, i którą z dwóch produkcji zdejmuje sonda, rozstrzyga, gdzie ona
stanie.

Nad rejestrem ustaw jedno zdanie jednoznaczność traci
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
i nie robi tego dopełniacz:

```text
Sposób załatwienia petycji nie może być przedmiotem skargi.
```

Morfeusz czyta `nie` także jako biernik zaimka `on` w formie popodstawowej,
czyli tej, która stoi po przyimku — `na nie`, `za nie` — a olski warunku o tym
nie ma, więc zdanie miało czytanie z zaimkiem w roli dopełnienia,
zanim cząstka weszła, i ma je nadal obok czytania z przeczeniem.
Jest to [czytanie, którego polszczyzna nie ma](#the-dictionary-offers-readings-polish-does-not),
a kryterium słownikowe po nie nie sięga, bo wyrzuca rzeczownik, a nie zaimek.
[TODO.md](../TODO.md) trzyma ten warunek.

Nad [README](../README.md) negacja nie kupuje ani jednego zdania i żadnego nie traci,
tak samo jak czas przeszły przed nią.

### Cena stoi w trafności, a nie w liczbie czytań

Ta konstrukcja płaci nie liczbą czytań, tylko tym, które z nich wychodzi,
i jedno zdanie Składnicy olski przez nią czyta inaczej niż drzewo wzorcowe:

```text
Prezes firmy może wyrzucić każdego pracownika, premier większości nie może ruszyć.
```

Dopełnienie w dopełniaczu stoi przed swoim czasownikiem,
a tam jest także przydawką dopełniaczową grupy imiennej przed nim,
więc `premier większości` wychodzi jednym podmiotem
w zdaniu składowym, które ma podmiot i dopełnienie.
Oba czytania polszczyzna ma, a olski ma tu jedno,
bo dopełnienie należy do bezokolicznika pod czasownikiem modalnym,
a żadne ciało nie stawia go przed tą parą
([niżej](#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery)),
więc czytanie, które ma czytelnik, nie ma się czym wyprowadzić,
i zamiast dwóch czytań wychodzi jedno, pewne siebie i błędne.
Jest to ta sama pomyłka co przy [wyliczonym ciele](design-notes.md#wyliczone-ciało-myli-się-w-stronę-werdyktu),
tylko widziana od strony konstrukcji, która ją wywołała.

Dwa zdania tego samego kształtu z tej listy zeszły,
i zdjął je szyk, a nie nic w negacji:
`Apostołowie tego nie praktykowali.`
oraz `Nikt niczego nie wybiera, coś wybiera za nas.`
wychodzą dwoma czytaniami, odkąd dopełnienie ma ciało
przed formą osobową swojego czasownika.
Werdykt jest tam odmową i to jest cena zapłacona po tej zmianie w tej walucie,
w której ta sekcja liczy: czytanie czytelnika stoi na wydruku obok drugiego,
zamiast nie mieć się czym wyprowadzić.

## Szyk zmierzono: kupuje 44 zdania i odbiera cztery

Podmiot, dopełnienie i czasownik stoją w polszczyźnie w sześciu kolejnościach,
a olski miał dwie, SVO i OVS, oraz czasownik na czele bez dopełnienia.
Cztery brakujące nie były wykluczone decyzją, tylko brakiem ciała produkcji,
czego [design-notes.md](design-notes.md#angle-one-parsing) tej gramatyce
zabrania wprost: szyk spoza olskiego ma być wykluczony warunkiem,
a nie przemilczeniem.
Przeciw dopisaniu ich przemawiała jednoznaczność,
bo synkretyzm mianownika z biernikiem czyni dwuznacznym każde zdanie,
które da się przeczytać od podmiotu i od dopełnienia naraz,
a szyk dopisany daje tej dwuznaczności nowe miejsca.

Cenę tej konkurencji liczy `sonda/szyk.py` i wychodzą cztery zdania.

```sh
python3 -m sonda.szyk Składnica-frazowa-180723/
```

| wariant | przyjęte | wieloznaczne | odrzucone |
| --- | --- | --- | --- |
| bez czterech szyków | 1139 | 528 | 11 368 |
| SOV | 1151 | 533 | 11 351 |
| OSV | 1150 | 530 | 11 355 |
| VSO | 1143 | 535 | 11 357 |
| VOS | 1152 | 535 | 11 348 |
| wszystkie cztery | 1179 | 549 | 11 307 |

Mianownik jest ten sam, co w tabelach [corpus.md](corpus.md#the-measurement):
13 035 lasów Składnicy z pełnym drzewem, morfologia złota,
i wchodzą do niego wszystkie, bez granicy na długość zdania.

Czterdzieści cztery zdania przechodzą z odrzuconych na przyjęte,
siedemnaście z odrzuconych na wieloznaczne,
a cztery z przyjętych na wieloznaczne, i te cztery są całą ceną.
Zakup dzieli się między szyki na szesnaście, jedenaście, cztery i trzynaście,
czyli sumuje się dokładnie,
a sonda nie znajduje ani jednego zdania,
które rusza się pod dwoma szykami naraz.
Cztery szyki są więc czterema rozłącznymi zakupami, a nie jednym podzielonym,
i płaci za nie sam SOV: pozostałe trzy nie odbierają jednoznaczności
ani jednemu zdaniu, które ją miało.

Zakup jest przy tym zakupem, a nie samym wyprowadzeniem:
zdanie przyjęte odwrotnie niż w banku drzew nie jest zakupem dla nikogo.
Czterdzieści dwa z czterdziestu czterech zdań
mają role zgodne z drzewem wzorcowym,
a odwróconego nie ma ani jednego,
czyli szyk nie kupuje zdań przeczytanych na opak.
Dwa niezgodne sonda wypisuje obok liczby,
i żadne z nich nie jest przyłączeniem, które olski wybrał:

```text
Widzę, że ostatnia lekcja czegoś was nauczyła.
Co pan sądzi o pomyśle Pawła Piskorskiego?
```

`Nauczyć` rządzi dopełniaczem obok biernika,
a olski ma jedną pozycję dopełnienia,
więc `czegoś` nie ma gdzie stanąć i wpada do podmiotu przed nim:
podmiotem wychodzi `ostatnia lekcja czegoś` tam,
gdzie bank drzew kończy go na `lekcja`.
Jest to ta sama rozbieżność zasięgu, którą
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)
liczy nad `Policja prowadzi w tej sprawie intensywne śledztwo.`,
tylko wywołana przez pozycję dopełnienia, a nie przez okolicznik.
W drugim zdaniu olski czyta role tak, jak przeczytałby je czytelnik —
`Co` jest dopełnieniem, `pan` podmiotem —
a bank drzew dopełnienia tam nie oznacza wcale,
więc niezgodność jest po stronie porównania, tak samo jak przy
`Kampania nie przyniosła skutku.` w tamtym dokumencie.

### Dwa z tych czterech zdań są naprawą, a nie ceną

Cztery zdania tracą jednoznaczność, a dwa z nich tracą ją razem z czytaniem,
którego polszczyzna nie ma, i to jest właściwy odczyt tej kolumny.

```text
Apostołowie tego nie praktykowali.
Nikt niczego nie wybiera, coś wybiera za nas.
```

Oba są wyżej ceną, którą negacja płaciła trafnością
([wyżej](#cena-stoi-w-trafności-a-nie-w-liczbie-czytań)):
dopełniacz negacji poprzedzał swój czasownik,
brała go tam tylko przydawka dopełniaczowa,
i olski wypuszczał jedno czytanie, pewne siebie i odwrotne niż drzewo wzorcowe.
Szyk SOV daje czytaniu czytelnika ciało,
więc oba zdania wychodzą teraz dwoma czytaniami,
z których jedno jest tym, które ma bank drzew.
Werdykt `ambiguous` jest w tej gramatyce odmową,
a odmowa z dwoma czytaniami na wydruku
jest lepszym werdyktem niż jedno czytanie przeczytane na opak.

Pozostałe dwa są ceną i są tym samym sporem oglądanym bez naprawy:

```text
Kryterium wzrostu nie obowiązuje.
Janka nic nie odpowiada i zamyka drzwi.
```

Dopełniacz stojący przed czasownikiem czyta się tu i jako dopełnienie,
i jako przydawka rzeczownika przed nim,
a olski ma teraz oba ciała, więc melduje oba czytania.

Trzecie zdanie z tamtej trójki naprawy nie dostało
i pokazuje granicę tych ciał:

```text
Prezes firmy może wyrzucić każdego pracownika, premier większości nie może ruszyć.
```

Dopełnienie należy tu do bezokolicznika pod czasownikiem modalnym,
a ciała dopisane umieszczają dopełnienie przy formie osobowej i tylko przy niej,
więc `większości` dalej nie ma gdzie stanąć poza podmiotem przed sobą.
Kolejność dopełnienia wobec bezokolicznika, który je bierze,
jest osobnym zakupem i [TODO.md](../TODO.md) go trzyma.

### Nad prozą ten szyk nie rusza ani jednego zdania

```sh
python3 -m harness.markdown README.md --into proza/
python3 -m sonda.szyk proza/README.txt
```

Ani jeden werdykt nad tym plikiem się nie rusza,
pod żadnym z czterech szyków osobno i pod wszystkimi naraz.
Nad rejestrem ustaw te szyki nie kupują nic
i czynią wieloznacznymi cztery zdania,
z czego trzy przychodzą z odrzuconych, a jedno z przyjętych —
`Przebieg losowania uwzględnia się w protokole wyników wyborów.`
([ustawy.md](ustawy.md#co-gramatyka-z-tego-wyprowadza)).
Dokumentacja i ustawa szyku więc nie przestawiają,
a proza i prasa z banku drzew przestawiają,
i to jest cała różnica między tymi trzema liczbami.
Zakup tego szyku jest przez to zakupem pokrycia cudzej polszczyzny
i naprawą dwóch czytań, a nie krokiem w rejestrze, do którego olski jest kierowany.

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
`NP` is also where a relative clause attaches,
for a reason [below](#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)
that has nothing to do with coordination.
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
| bez przecinka | 1099 | 514 | 11 422 |
| zdaniowy | 1161 | 531 | 11 343 |
| imienny | 1117 | 531 | 11 387 |
| przymiotnikowy | 1099 | 514 | 11 422 |
| wszystkie trzy | 1179 | 549 | 11 307 |

Mianownik jest ten sam, co w tabelach tamtego dokumentu:
13 035 lasów Składnicy z pełnym drzewem, morfologia złota,
i wchodzą do niego wszystkie, bez granicy na długość zdania.

Ani jedno zdanie nie przechodzi z przyjętego na wieloznaczne.
Wieloznacznych przybywa trzydzieści pięć i wszystkie przychodzą z odrzuconych,
czyli z tych, których gramatyka bez przecinka nie wyprowadzała wcale.
Konkurencji między poziomami sonda nie liczy z tych sum, tylko wprost,
zdanie po zdaniu, i znajduje ją raz.
Żadnego zdania nie ruszają poziom zdaniowy i imienny naraz,
a o jednym oba naraz mówią co innego niż każdy z osobna:

```text
Stworzyła polski oddział EquiLibre, organizowała konwoje z pomocą dla byłej
Jugosławii, Kazachstanu, Czeczenii.
```

Każdy poziom z osobna to zdanie odrzuca, a oba naraz czynią je wieloznacznym,
czyli dwie produkcje dały mu czytanie, którego żadna z nich nie dała.
Argument o konkurencji ma więc nad tym korpusem dokładnie jedno zdanie,
i pojawiło się ono wraz z czasem przeszłym:
zdanie stoi w nim całe, a przed tą zmianą nie wyprowadzało się pod żadnym wariantem.

Po drugiej stronie stoi zakup: pięćdziesiąt zdań przechodzi
z odrzuconych na przyjęte, trzydzieści sześć za poziom zdaniowy
i czternaście za imienny.
Czterdzieści cztery z nich mają role zgodne z drzewem wzorcowym,
sześć nie ma w nim żadnej roli do porównania,
a odwróconych i niezgodnych nie ma ani jednego,
więc są to zdania przeczytane tak, jak przeczytali je anotatorzy.

Nowe wieloznaczności nie biorą się z przecinka, tylko z przyłączenia.
`Warszawska kuria metropolitalna ma wśród swoich licznych włości nieruchomość
w podwarszawskim Skolimowie, uzdrowiskowej dzielnicy Konstancina-Jeziorny.`
wychodzi dwoma czytaniami, bo wyrażenie przyimkowe dochodzi do rzeczownika
albo do czasownika, i tak samo różnią się czytania pozostałych.
Jest to ta sama wieloznaczność, którą olski
[oddaje czytelnikowi](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera):
koordynacja przecinkiem daje jej więcej miejsc, w których się mieści,
a nie nowy rodzaj sporu.

Poziom przymiotnikowy nie rusza ani jednego zdania w żadną stronę.
Czy jest to własność polszczyzny, czy tego korpusu, ta liczba nie mówi:
`duży, ciężki plecak` jest polszczyzną,
a nad Składnicą nie ma zdania, w którym ta produkcja byłaby ostatnią brakującą.

Nad rejestrem, o który olskiemu chodzi, przecinek kupuje trzy zdania.
To samo porównanie nad prozą wyciągniętą z README —

```sh
python3 -m harness.markdown README.md --into proza/
python3 -m sonda.przecinek proza/README.txt
```

— rusza trzy werdykty, dwa na poziomie zdaniowym i jeden na imiennym.
`Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego`
i `Co ekstrakcja po drodze zmyśla, mówi docs/extraction.md`
przechodzą z odrzucenia w wieloznaczność,
a `Czarna lista kupowała jednak co innego, niż obiecywała`
gramatyka bez przecinka odrzuca, a z nim wyprowadza jednym czytaniem.
Trzeciego z nich nie było w tym pomiarze, dopóki gramatyka nie miała czasu
przeszłego, i to on przeniósł poziom imienny z zera na jedno zdanie.
Poziom przymiotnikowy nie rusza tu nic,
bo pozostałe zdania tego pliku, które niosą przecinek,
niosą też zdanie podrzędne, przysłówek albo rzeczownik odczasownikowy.
Przecinek wszedł więc za pokrycie w cudzej polszczyźnie,
a nad tą prozą czeka na to, co w reszcie tych zdań stoi obok niego.
Podrzędność, która stała w tej kolejce pierwsza, weszła i tej liczby nie ruszyła
([niżej](#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja)),
a czas przeszły ruszył ją, nie ruszając liczby zdań przyjętych
([wyżej](#czas-przeszły-żąda-rodzaju-od-każdego-szyku)),
więc czeka ono na przysłówek i dwukropek
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
Biernik czytają oba kierunki, a bezokolicznik i zdanie podrzędne czyta sam skład,
i nie jest to niezgoda o fakt, tylko różnica w tym, co ten fakt komu kupuje.
Po stronie generatora jest bezokolicznik jedyną obroną przed drzewem,
które żąda go od czasownika, który go nie bierze,
bo bezokolicznik z niczym się nie zgadza i pomyłka nie ma jak wyjść inaczej.
Po stronie parsera został zmierzony i pomiar stoi niżej w tej sekcji.

Zdanie trzecie zmierzono po tej samej stronie i wyszło z tego to samo.
Rama domyślna ma zdanie podrzędne, a leksykon wymienia 1 926 lematów,
które je biorą, więc odjęcie reszty jest wobec Walentego prawdziwe:
`zamykać` bierze biernik, a `Kot zamyka, że mysz śpi.` polszczyzną nie jest.
Nad Składnicą to odjęcie kosztuje jedno zdanie —
`Wystarczy, że ujmiesz w swej pracy twarz i ręce.`, bo `wystarczyć` na liście
nie stoi — a jednoznaczności nie kupuje ani jednej,
pod złotą morfologią i pod Morfeuszem tak samo.
Rama zostaje więc szeroka, tak jak przy bezokoliczniku i z tego samego powodu:
zawężenie prawdziwe, które nie odbiera ani jednego drugiego czytania,
płaci pokryciem za nic.

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
bo bez niego liczebnik dopisany do gramatyki dałby temu zdaniu dwa czytania,
a nie jedno: `dwie rzeczy` jest mianownikiem i biernikiem naraz,
a zdanie bez podmiotu bierze dopełnienie.
Wpis stoi, [grupa liczebnikowa](#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
też stoi, i zdanie wychodzi jednym czytaniem.
Leksykon kupił tu więc jednoznaczność, a nie pokrycie,
i widać to dopiero z produkcją, której wtedy nie było.

## Podrzędność i koordynacja dzielą przecinek, a rozdziela je produkcja

Zdanie podrzędne otwiera w polszczyźnie ten sam znak,
którym koordynacja łączy dwa zdania składowe,
więc gramatyka, która ma przecinek i nie ma podrzędności,
nie odrzuca zdania podrzędnego — czyta je jako współrzędne.
`Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.`
wychodziło jednym czytaniem, w którym `które zadania własne gminy`
jest podmiotem drugiego zdania,
i pomiar nad rejestrem ustaw liczył to zdanie jako pokrycie
([ustawy.md](ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa)).
Jedno czytanie, pewne siebie i błędne, jest gorsze niż odmowa.

Rozdziela je miejsce przecinka w produkcji, a nie warunek obok niej.
Koordynacja ma przecinek na poziomie zdania i powtarza tam własny symbol:
`Clause → ClauseConjunct , Clause`.
Podrzędność wciąga przecinek do konstytuentu, który sama tworzy,
więc `SubordinateClause → , że Clause` jest jednym konstytuentem wraz z przecinkiem,
a `Clause` się w nim nie powtarza.
Po tym rozpoznaje ciąg współrzędny werdykt (`_koordynuje` w `olski/parse.py`)
i po tym samym rozpoznaje go sonda, która przecinek zdejmuje.

### Zdanie z `że` jest pozycją ramy, a nie konstrukcją obok niej

Czym jest zdanie podrzędne dopełnieniowe dla czasownika,
tym jest dopełnienie i bezokolicznik:
pozycją ramy, którą [leksykon walencyjny](#walencja-jest-leksykonem-o-ramie-domyślnej)
czasownikowi daje albo odbiera.
Wchodzi więc jako czwarta pozycja ramy domyślnej,
a nie jako produkcja dopisana do każdego szyku zdania z osobna,
i tak samo jak tamte trzy dochodzi do czasownika przez `Complements`.
Kosztuje to jedno słowo w `RAMA_DOMYŚLNA` i jedno ciało w `olski/subset.py`.

Spójnikiem jest `że` i nic poza nim,
choć Morfeusz daje klasę `comp` także formom `gdy`, `jeśli` i `aby`.
Tamte otwierają okolicznik zdania, a nie dopełnienie,
więc wpuszczone tą produkcją stanęłyby w pozycji, której nie zajmują,
a czasownikowi, który zdania podrzędnego nie bierze,
dałyby czytanie, w którym je bierze.

Pod złotą morfologią przebieg nad Składnicą rusza 26 zdań i wszystkie w tę samą stronę:
siedemnaście przechodzi z odrzucenia w jednoznaczność, dziewięć w wieloznaczność,
a żadne zdanie już przyjęte nie traci werdyktu ani nie zyskuje drugiego czytania.
Wśród nowo przyjętych zgodność z drzewem wzorcowym rośnie o dwanaście,
jedno zdanie wychodzi zgodne częściowo, cztery nie mają w nim roli do porównania,
a o ani jedno odwrócenie roli zgodność nie rośnie
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Liczba 26 rośnie przy tym z czasem przeszłym, a nie z podrzędnością:
zdanie podrzędne stoi w tym korpusie najczęściej przy czasowniku w tym czasie,
więc konstrukcja zmierzona przed nim była mierzona przy części swoich zdań
([wyżej](#czas-przeszły-żąda-rodzaju-od-każdego-szyku)).

```text
Mieszkańcy grożą, że zablokują ulice.
Dodaje, że zwolnienia są nieuniknione.
```

### Zaimek względny nie jest przymiotnikiem przy rzeczowniku

Morfeusz daje `który` znacznik `adj`, czyli ten sam, co `nowy` i `polski`,
i to jest cały powód, dla którego `które zadania własne gminy`
wychodziło grupą imienną.
Przymiotnikiem przy rzeczowniku ten wyraz w polszczyźnie nie bywa nigdy:
zaczyna zdanie względne albo pytanie, a przydawki nie tworzy.
Warunek jest więc taki sam jak przy [zaimku rzeczownym](#zaimek-rzeczowny-nie-rządzi-dopełniaczem)
i pada w tym samym miejscu — na terminalu, a nie w słowniku:
przydawka i orzecznik tego lematu nie biorą, a bierze go czoło zdania względnego.

Zdjęcie tego czytania jest tym, co odbiera czytanie współrzędne,
i odbiera je bez produkcji, która by go zabraniała:
`które zadania własne gminy` przestaje być grupą imienną,
więc nie ma czym być podmiotem zdania po przecinku.
Tańsza z dwóch dróg do czytania, którego polszczyzna nie ma,
prowadzi tędy, a nie przez wykluczenie w `admissible`
([roadmap.md](roadmap.md#etap-3-czytania-których-polszczyzna-nie-ma)).

Kosztuje to jedno zdanie i jest nim pytanie.
Nad Składnicą pod Morfeuszem warunek odbiera dokładnie
`Który aktor robi na tobie największe wrażenie?`,
gdzie `Który` jest zaimkiem pytajnym przy rzeczowniku.
Pytanie zależne — `określają, które zadania` — kosztuje tyle samo:
zdanie, które wychodziło błędnie, wychodzi teraz odrzucone,
a konstrukcji, która by je wyprowadzała poprawnie, ta gramatyka nie ma.
Obie należą do tego samego braku i [TODO.md](../TODO.md) trzyma je razem.

### Zdanie względne niesie liczbę i rodzaj swojego zaimka

Przypadek zaimka względnego mówi o zdaniu podrzędnym,
a liczba i rodzaj o poprzedniku:
`który` bierze przypadek z roli, którą w zdaniu podrzędnym zajmuje,
a zgadza się w liczbie i rodzaju z tym, co określa.
Zdanie względne wypuszcza więc te dwie cechy do góry,
a produkcja, która je przyłącza, żąda ich od grupy imiennej.

Kupuje to przyłączenie, którego gramatyka nie musi wybierać:

```text
Zbiór tekstów, które są polskie, jest podzbiorem.
Zbiór tekstu, który jest polski, jest podzbiorem.
```

Pierwsze ma jedno czytanie, bo `które` jest w liczbie mnogiej
i do `Zbiór` przyłączyć się nie ma jak.
Drugie ma dwa, bo `Zbiór` i `tekstu` są oba męskie i pojedyncze,
i są to dwa czytania, które ma także czytelnik.
Jest to ta sama postawa co przy
[wyrażeniu przyimkowym](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera) —
gramatyka przyłączenia nie wybiera —
z tą różnicą, że tutaj większość wyborów odbiera zgodność,
czyli to samo, czym odbiera je czytelnik.

Zdanie względne dochodzi przy tym do `NP`, a nie do `NPConjunct`,
i nie jest to wybór wygody.
Produkcja rekurencyjna na poziomie członu daje `te [konstrukcje, które stoją]`
obok `[te konstrukcje], które stoją`,
czyli dwa wyprowadzenia jednej struktury,
a tych dwóch nie ma czym odsiać:
kształty są różne, więc [są dwoma czytaniami](#co-się-liczy-jako-jedno-czytanie).
Wyżej ten wybór nie istnieje, bo `NPConjunct` bierze wszystko, co grupa niesie przed nim.
Kosztuje to symetrię w koordynacji:
człon prawy zdanie względne unieść może, a lewy nie,
więc `pliki, które rosną, i katalogi` nie ma wyprowadzenia.

Zdanie względne wypełnia trzy role, bo tylu ten rejestr używa,
a każda z nich jest tą, którą zaimek zabiera zdaniu podrzędnemu:
podmiot (`reguła, która rozstrzyga`),
dopełnienie (`polszczyzna, którą ktoś napisał`)
i wyrażenie przyimkowe (`język, o którym to repozytorium jest`).
Ostatnia sięga najdalej i jest jedną produkcją,
bo za wysuniętym wyrażeniem przyimkowym następuje zdanie składowe całe,
w każdym szyku, jaki ono ma.
Podmiot za wysuniętym dopełnieniem stoi przy tym po czasowniku i przed nim,
choć zdanie główne ma ten szyk tylko w pierwszej wersji:
`które ktoś napisał` jest w polszczyźnie zwyczajne, a `Teksty ktoś napisał` nie,
i różni je to, że zaimek względny wysuwa polszczyzna zawsze,
a dopełnienie z wyboru.

Wysunięte wyrażenie przyimkowe niesie przy tym sam zaimek i nic poza nim.
Polszczyzna wysuwa razem z nim całą grupę, w której on stoi —
`ustawy, na podstawie której jest ono wydawane` —
i takiego zdania ta gramatyka nie wyprowadza,
bo `której` jest tam dopełniaczem przy `podstawie`, a nie grupą pod przyimkiem.
Nad „Zasadami techniki prawodawczej” jest to jedyne zdanie,
które przechodzi z wieloznaczności w odrzucenie,
i przechodzi dlatego, że stało na czytaniu współrzędnym.

Zdanie względne z wysuniętym dopełnieniem żąda przy tym podmiotu,
bo każde takie ciało ma go wypisany,
więc podmiot opuszczony to zdanie odrzuca:
`Dyrektor wymienia imprezy, które zorganizował.` nie wyprowadza się,
a `Dyrektor wymienia imprezy, które on zorganizował.` wyprowadza się raz.
Polszczyzna podmiot w tej pozycji opuszcza swobodnie,
a nad Składnicą są to cztery zdania.

Wysunięte dopełnienie sięga ponadto do formy osobowej i nie dalej,
bo ciała wypisane wyżej mają w środku czasownik zdania składowego,
więc dopełnienie należące do bezokolicznika pod nim nie ma się skąd wziąć:
`Ustawa, którą organ gminy może wydać, jest tania.` jest odrzucone.
Zdania tego kształtu nie ma jednak ani jedno zdanie rejestru ustaw,
co pokazuje `grep -P 'któr\w+ [^.]*\b(może|mogą|ma|mają)\b [^.]*\w+ć'`
nad `proza/ustawy/`, więc konstrukcja ta jest wyczytana z gramatyki,
a nie z korpusu.

Po jedno i drugie sięgnęłaby cecha przeciągana, czyli luka zamiast wypisanych ciał,
a ile ona kupuje w każdym z trzech rejestrów i dlaczego nie weszła, mierzy
[design-notes.md](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze).

### Bank drzew nazywa `który` inaczej niż Morfeusz, a czytelnik to przekłada

Składnica taguje `który` jako `padj`, czyli zaimek przymiotny,
a Morfeusz jako `adj`,
więc gramatyka pisana pod tagset Morfeusza nie sięgała po ani jedno wystąpienie
w przebiegu pod złotą morfologią.
Przekłada to dzisiaj czytelnik banku drzew, razem z trzema innymi nazwami
([corpus.md](corpus.md#where-the-analyses-stop)),
i obie kolumny mierzą przez to zdanie względne tak samo.

Pod złotą morfologią zdanie z `że` wyciąga z odrzucenia 66 zdań Składnicy,
trzydzieści trzy jednoznaczne i trzydzieści trzy wieloznaczne,
a zdanie względne 36, siedem jednoznacznych i dwadzieścia dziewięć wieloznacznych.
Każdą z tych liczb bierze osobny kontrfaktyk, czyli ta gramatyka bez jednej z nich,
więc suma tych dwóch nie jest liczbą, jaką dałoby zdjęcie obu naraz.
Ani jedno zdanie przyjęte nie traci przy tym jednoznaczności,
więc jednoznaczność obie konstrukcje kosztują tu zero,
a wieloznaczności przybywa wyłącznie na zdaniach, które wcześniej odpadały.

```text
Widoczny jest wzrost aspiracji społeczeństwa, które chce zdobywać wykształcenie.
```

Rozbieżność tagsetów jest przy tym faktem o korpusie, a nie o gramatyce,
i zapisana jest tutaj dlatego, że kolumna złota mówiła bez tego przekładu
o zdaniu względnym nieprawdę:
liczba, która się nie ruszyła, czyta się jak konstrukcja, która nic nie kupuje.

## Grupa liczebnikowa zgadza się tym, czego nie ma w środku

Liczebnik przyłącza się w polszczyźnie dwoma sposobami
i który to sposób, mówi tag, a nie kontekst:
Morfeusz oznacza `dwie` jako `num:pl:nom.acc.voc:f:congr`,
a `pięć` jako `num:pl:nom.acc.voc:m2.m3.f.n:rec`,
czyli nazywa jeden zgodnym, a drugi rządzącym.
Liczebnik zgodny jest przy rzeczowniku tym, czym przymiotnik przed nim,
i zgadza się z nim w przypadku, liczbie i rodzaju:
`dwie rzeczy`, `cztery wozy`, `oba pliki`.
Liczebnik rządzący wymaga dopełniacza mnogiego,
tak jak wymaga go rzeczownik z dopełniaczem pod głową:
`pięć kobiet`, `kilka dni`, `piętnastu członków`.
Produkcje są więc dwie, a nie jedna z warunkiem w środku,
bo te dwa przyłączenia dzielą tylko nazwę części mowy.

Grupa, którą buduje liczebnik rządzący, zgadza się czymś, czego nie ma pod nią.
`Pięć kobiet przyszło.` żąda czasownika w liczbie pojedynczej i rodzaju nijakim,
choć `kobiet` jest mnogie i żeńskie,
więc liczba i rodzaj są w tej produkcji wypisane wartością,
a nie zmienną wspólną z córką.
Cecha wypisana wartością nie jest tu nowa:
[ciąg współrzędny](#nothing-above-a-coordination-distributes-into-it)
ogłasza liczbę mnogą i trzecią osobę tak samo, niezależnie od swoich członów.
Nowe jest to, czemu ta wartość przeczy.
Ciąg jest mnogi, bo dwie rzeczy są dwiema rzeczami,
a `pięć kobiet` jest pojedyncze i nijakie wbrew każdemu słowu w środku,
więc rodzaj nijaki nie opisuje tu niczego prócz zgodności, której polszczyzna żąda.
Zmienna wspólna wygląda tam poprawnie i odwraca zgodność:
przyjmuje `Pięć kobiet przyszły.`, którego polszczyzna nie ma,
i odrzuca zdanie, które ma.
Rodzaj przechodzi natomiast z liczebnika na dopełniacz,
bo rodzaj męskoosobowy ma w polszczyźnie własną formę liczebnika:
`Pięciu mężczyzn przyszło.` wyprowadza się, a `Pięć mężczyzn przyszło.` nie.
Liczebnik zbiorowy wchodzi tą samą produkcją i nie kosztuje ani jednej pozycji,
bo `dwoje` jest dla Morfeusza liczebnikiem rządzącym
i różni się od `dwa` samą wartością cechy `collectivity`.

Do drabiny [kosztów](design-notes.md#the-cost-ladder) taka cecha nic nie dokłada,
bo jest cechą skończoną jak każda inna,
więc grupa liczebnikowa mieści się na szczeblu 0 razem z resztą gramatyki.
Liczebnik płaci więc nie formalizmem, a
[drugą walutą](design-notes.md#the-second-currency-ambiguity), czyli czytaniami.
Liczebnik rządzący jest synkretyczny między mianownikiem i biernikiem,
więc zdanie z grupą liczebnikową obok drugiej grupy synkretycznej
wychodzi dwoma czytaniami: `Rada gminy liczy piętnastu członków.` czyta się
i tak, że rada liczy członków, i tak, że członkowie liczą radę.
Polszczyzna ma oba te czytania, więc olski to zdanie odrzuca i odrzuca słusznie.

### Liczebnik zmierzono i nie odbiera ani jednego zdania

Pytanie nie brzmi, ile zdań te dwa ciała przyjmują,
bo to policzy każdy przebieg `olski-corpus`.
Brzmi ono, ile zdań odbierają,
bo zdanie odrzucone przez wieloznaczność czeka na wycofanie produkcji,
a nie na dopisanie następnej.
Mierzony jest więc ruch werdyktu, zdanie po zdaniu,
a ciała zdejmują się osobno, bo cena każdego z nich jest osobną liczbą:

```sh
python3 -m sonda.liczebnik Składnica-frazowa-180723/
```

| wariant | przyjęte | wieloznaczne | odrzucone |
| --- | --- | --- | --- |
| bez liczebnika | 1105 | 499 | 11 431 |
| zgodny | 1145 | 530 | 11 360 |
| rządzący | 1137 | 517 | 11 381 |
| oba | 1179 | 549 | 11 307 |

Mianownik jest ten sam, co w tabelach [corpus.md](corpus.md#the-measurement):
13 035 lasów Składnicy z pełnym drzewem, morfologia złota,
i wchodzą do niego wszystkie, bez granicy na długość zdania.

Ani jedno zdanie nie przechodzi z przyjętego na wieloznaczne.
Siedemdziesiąt cztery przechodzą z odrzuconych na przyjęte
i pięćdziesiąt z odrzuconych na wieloznaczne,
czyli cała cena jest zapłacona zdaniami,
których gramatyka bez liczebnika nie wyprowadzała wcale.
Zakup dzieli się między ciała prawie po połowie, na czterdzieści i trzydzieści dwa,
i żadne zdanie nie rusza się pod obydwoma,
więc te dwa zbiory są rozłączne i sumują się do siedemdziesięciu dwóch.
Dwa zdania wymagają obu ciał naraz,
tak samo jak jedno z pięćdziesięciu wieloznacznych,
bo ma dwie grupy liczebnikowe i każda z nich przyłącza się inaczej:

```text
30 kilogramów falsyfikatów miało wartość 4 milionów dolarów.
```

Tak niska cena bierze się częściowo z tego, co jest jednym czytaniem.
`Tysiąc plików rośnie.` wychodzi jednym, choć `tysiąc` jest i rzeczownikiem,
i liczebnikiem rządzącym, a oba czytania stawiają pod nim dopełniacz:
kształt jest ten sam, a [część mowy jest z tożsamości czytania wyłączona](#co-się-liczy-jako-jedno-czytanie),
więc te dwa wyprowadzenia wpadają do jednej klasy.
Ta sama forma wypuszczona osobnym kształtem dałaby zdanie wieloznaczne,
i tak właśnie płaci cyfra niżej.

Role zdań nowo przyjętych zgadzają się z drzewem wzorcowym pięćdziesiąt osiem razy,
dziesięć zdań nie ma w nim roli do porównania, trzy mają ją tylko częściowo,
a niezgodne są trzy i żadne z nich nie jest wyborem, którego olski dokonał.
`W Hongkongu zmarły cztery osoby zarażone wirusem ptasiej grypy.`
czyta imiesłów jako orzecznik, gdzie bank drzew ma go w przydawce przy `osoby`,
i jest to [przydawka imiesłowowa](#what-it-does-not-cover-yet), której olski nie ma;
liczebnik tylko doprowadził analizę do miejsca, w którym ten brak widać.
`Od dwu tygodni nie mam od ciebie listu!` jest rozbieżnością zasięgu,
którą [corpus.md](corpus.md#agreement-which-matters-more-than-acceptance) liczy
razem z trzema takimi samymi: złote poddrzewo bierze w siebie wyrażenie
przyimkowe, które olski wiesza na zdaniu.
`Marzec przyniósł 6 zagranicznych delegacji.` olski czyta tak,
jak przeczytałby je czytelnik, a niezgodność jest po stronie porównania:
bank drzew daje grupie liczebnikowej w pozycji dopełnienia własne gniazdo, `np(part)`,
którego `_role` w `olski/corpus.py` nie tłumaczy na żadną rolę olskiego,
więc drzewo wzorcowe nie ma tam dopełnienia, z którym można by się zgodzić.
[TODO.md](../TODO.md) trzyma to jako usterkę porównania.

Nad rejestrem, o który olskiemu chodzi, liczebnik kupuje jedno zdanie:

```sh
python3 -m harness.markdown README.md --into proza/
python3 -m sonda.liczebnik proza/README.txt
```

`Działają dwie rzeczy.` przechodzi z odrzucenia w jedno czytanie,
i jest to zdanie, o którym [corpus.md](corpus.md#where-the-analyses-stop) mówiło,
że czeka na liczebnik i na nic więcej.
Ciało zgodne kupuje je samo, ciało rządzące nad tą prozą nie rusza nic,
a wieloznacznych nie przybywa ani jedno.
Nad rejestrem ustaw wychodzi odwrotnie:
jedno zdanie przyjęte i cztery wieloznaczne z 4921
([ustawy.md](ustawy.md#co-gramatyka-z-tego-wyprowadza)),
czyli tam przeważa cena, a nie zakup,
i powód jest ten sam, który zamyka tę sekcję: ustawa liczy cyframi.

### Cyfry olski nie bierze, bo cyfra nie niesie morfologii

Rejestr, o który olskiemu chodzi, pisze liczebnik cyfrą:
`w terminie 14 dni`, `3 szkół`, `15 członków`.
Morfeusz daje cyfrze tag `dig` i ani jednej cechy,
a cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc obie produkcje biorą cyfrę naraz i żadna nie jest w stanie jej odrzucić.
`Termin wynosi 14 dni.` wychodzi wtedy trzema czytaniami zamiast dwóch,
bo `dni` jest i dopełniaczem mnogim, i mianownikiem mnogim,
czyli jedna grupa wyprowadza się i pod produkcją rządzącą, i pod zgodną.
Dwa z tych trzech czytań mają streszczenie znak w znak to samo,
bo różni je część mowy słowa pod głową, a nie żadna rola,
i po werdykcie czyta się to jak usterka narzędzia,
a nie jak zdanie, które da się poprawić.

Odmowa jest więc rozstrzygnięciem, a nie przeoczeniem,
i cena jest po jej stronie: cyfra zostaje formą,
której żadna produkcja nie bierze, i werdykt tak o niej mówi.
Wejście żąda dwóch rzeczy, których cyfra sama nie mówi, i tylko jedną da się odczytać.
Które z dwóch przyłączeń zachodzi, mówi rzeczownik po cyfrze:
`14 dni` ma dopełniacz mnogi, więc liczebnik jest tam rządzący,
a `14 dniach` miejscownik, więc zgodny, i tak samo czyta to każdy, kto ten rejestr pisze.
Przypadka samej grupy nie mówi ani cyfra, ani ten rzeczownik:
`pięć` jest mianownikiem, biernikiem albo wołaczem, a cyfra nie jest niczym,
więc grupa bez tej wartości spełnia każde żądanie przypadka w zdaniu.
Wejście stoi na tym drugim i jest to warstwa nad morfologią, a nie produkcja,
która wchodzi tym samym kryterium, co każda inna
([design-notes.md](design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)).

## What it does not cover yet

Every one of these is a sentence that gets rejected and should not be:

- A colon opening a clause, which is how this register introduces an explanation.
  `Cena jest niska: gramatyka jest bezkontekstowa.` is rejected
  where each half of it derives once on its own,
  and of clause-level punctuation olski has the comma and nothing else,
  so it stands at the front of the queue over this repository's prose
  ([corpus.md](corpus.md#where-the-analyses-stop)).
  A colon opens a list as well, which is a second construction behind one character.
- Przysłówek, którego olski nie ma w żadnej pozycji:
  `Program szybko zapisuje ustawienia.` jest odrzucone,
  a wiersz `adv` prowadzi kolejkę blokerów zaraz za interpunkcją
  ([corpus.md](corpus.md#where-the-analyses-stop)).
  Pozycja przy czasowniku kupuje nad Składnicą 428 zdań i jest do wzięcia,
  a pozycja przy przymiotniku dopisana obok niej odbiera 39,
  więc konstrukcja wchodzi tu połową albo czeka na warunek,
  którego formalizm nie ma
  ([niżej](#przysłówek-zmierzono-przed-dopisaniem-i-drugi-gospodarz-odbiera-39-zdań)).
- A comma standing in front of a conjunction.
  Two clauses join with a conjunction or with a comma
  ([above](#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania))
  and not with both at once,
  so `Plany są niczym, ale planowanie jest wszystkim.`
  gets past the comma and fails on `ale`,
  which is how Polish punctuates that coordination.
- The subordinators past `że`, which are the ones opening an adverbial clause:
  `gdy`, `jeśli`, `aby`, `zanim`, `choć`.
  The `comp` row [corpus.md](corpus.md#where-the-analyses-stop) ranks
  is what they come to together,
  and what keeps them out is that a `że` clause is a position in a verb's frame
  while these modify a clause
  ([above](#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej)).
- `który` anywhere it is not the relative pronoun of a relative clause:
  in a question (`Który aktor robi na tobie największe wrażenie?`),
  in an indirect one (`Ustawy określają, które zadania mają charakter obowiązkowy.`),
  and under a preposition that fronted the whole phrase it stands in
  (`ustawy, na podstawie której jest ono wydawane`).
  The first two are one construction and the third another,
  and all three used to derive
  — the first as an adjective before its noun, the other two as coordination —
  so what this entry records is a rejection replacing a wrong reading.
- Liczebnik pisany cyfrą, czyli ten, którym ten rejestr liczy:
  `Termin wynosi 14 dni.` jest odrzucone,
  gdzie `Termin wynosi czternaście dni.` wyprowadza się dwoma czytaniami.
  Cenę i warunek wejścia trzyma
  [cyfry olski nie bierze](#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii),
  a liczebnik rządzący z dopełniaczem pojedynczym — `półtora roku` — stoi poza tym
  z tego samego powodu, z którego mnogi wszedł: rządzi innym przypadkiem.
- Przydawka imiesłowowa, czyli imiesłów bierny przy rzeczowniku:
  `Wymienione zadania są obowiązkowe.` jest odrzucone,
  a imiesłów w orzeczniku olski bierze.
  Wiersz `ppas` liczy w kolejce blokerów 209 zdań
  ([corpus.md](corpus.md#where-the-analyses-stop)),
  i jest to jedno z dwóch zdań, w których liczebnik doprowadził analizę
  do brakującej pozycji, zamiast na niej stanąć.
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
- po każdej z dwóch grup imiennych w czterech
  [pozostałych szykach](#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery)
  (`Program ustawienia w pliku zapisuje.`)
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
- wewnątrz zdania względnego, po obu stronach tego, co w nim zostało
  (`reguła, która w tym trybie rozstrzyga`)

Wierszy jest osiem, a produkcji czterdzieści cztery,
bo pozycja powtarza się w każdym szyku, który ją ma,
a szyk jest w tej gramatyce osobną produkcją.
Dziesięć z tych czterdziestu czterech dołożyły cztery szyki dopisane,
i tyle właśnie znaczy w tej gramatyce jeden szyk więcej.
Liczy się je tak, jak się je zdejmuje, a granica biegnie tak.
Wchodzi produkcja, w której `Adjuncts` stoi obok czegoś jeszcze,
w tym obok drugiego okolicznika,
oraz ta, w której `Modifier` dochodzi do głowy mającej już przydawkę
albo do imiesłowu, czyli `APConjunct → adj|ppas Modifier`.
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
gramatyka bez tych pozycji czyta wbrew ręcznemu rozbiorowi ponad sto zdań,
a z nimi kilkanaście, i żadne z nich nie jest przyłączeniem, które olski wybrał.
Ile ich dokładnie jest po obu stronach i czym są te trzy, trzyma
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance);
tutaj stoi rzędem wielkości, bo liczba zapisana w obu miejscach
rozeszła się już raz i nikt tego nie zauważył.

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

## Przysłówek zmierzono przed dopisaniem i drugi gospodarz odbiera 39 zdań

Wyrażenie przyimkowe ma dwóch gospodarzy i oba czytania są prawdziwe,
więc olski oddaje je czytelnikowi.
Przysłówek ma dwóch gospodarzy i drugie czytanie jest fałszywe:
`tu` w `Mam tu odmienną interpretację.`
nie określa przymiotnika `odmienną` w żadnym rozumieniu tego zdania.
Sonda wycenia więc przysłówek przed dopisaniem go do gramatyki,
a nie po nim:

```sh
python3 -m sonda.przysłówek Składnica-frazowa-180723/
python3 -m sonda.przysłówek proza/README.txt
```

Gospodarze są dwaj, więc wierszy jest cztery:
mianownik, po jednym na gospodarza i obaj naraz.
`okolicznik` wpuszcza przysłówek do listy okoliczników,
czyli tam, gdzie stoi wyrażenie przyimkowe, i przed zdanie.
`przy przymiotniku` stawia go przed przymiotnikiem,
w przydawce i w orzeczniku, licząc pozycje z produkcji olskiego.

| wariant | przyjęte | wieloznaczne | odrzucone |
| --- | --- | --- | --- |
| bez przysłówka | 1179 | 549 | 11 307 |
| okolicznik | 1607 | 707 | 10 721 |
| przy przymiotniku | 1226 | 580 | 11 229 |
| oba | 1568 | 769 | 10 698 |

Okolicznik sam kupuje 428 zdań, określenie przymiotnika samo 47,
a oba razem 389, czyli mniej niż okolicznik sam.
Drugi gospodarz dopisany do pierwszego nie kupuje nic i odbiera 39 zdań.
[Krzywa pokrycia](design-notes.md#making-the-trade-measurable)
przewidziała, że dopisanie bywa droższe od tego, co kupuje,
i jest to najciaśniejszy przypadek, jaki się tu trafił:
odbierają sobie zdania dwie połowy jednej konstrukcji,
a nie dwie konstrukcje z osobna.

Cena nie jest przy tym stratą na zdaniach, które olski przyjmuje dziś:
jednoznaczności nie traci ani jedno z tych 1179, w żadnym z trzech wariantów.
Płaci ją zakup drugiego gospodarza zakupem pierwszego,
bo zdanie, które każdy z nich osobno przyjmuje jednym czytaniem,
przy obu naraz wychodzi dwoma.

```text
Program zabawy był ściśle ustalony.
```

Pod `okolicznik` orzecznikiem jest `ustalony`, pod `przy przymiotniku`
`ściśle ustalony`, a pod `oba` te dwa czytania stoją obok siebie.
Zdań, które ruszają się pod jednym gospodarzem i pod drugim, jest 59,
a takich, o których oba naraz mówią co innego niż każdy osobno, 51.

Drugi gospodarz płaci ponadto trafnością.
Z 47 zdań, które kupuje sam, 15 olski czyta wbrew drzewu wzorcowemu,
czyli prawie co trzecie, gdzie okolicznik myli się na 13 z 428.
Powód widać na zdaniu, które ten gospodarz kupuje sam:
`Nagrali razem pierwszą płytę.` wychodzi z dopełnieniem `razem pierwszą płytę`,
bo `razem` wpada do grupy imiennej, przez którą przechodzi.
Ról odwróconych nie ma ani jednej, w żadnym wariancie.

Pierwszy gospodarz nie jest przez to darmowy, bo lista okoliczników jest płaska.
`Program zapisuje ustawienia bardzo szybko.` wychodzi pod nim jednym czytaniem,
a jego kształtem jest `Adjuncts(bardzo Adjuncts(szybko))`,
czyli dwa okoliczniki zdania obok siebie,
gdzie `bardzo` określa `szybko` i zdania nie określa wcale.
Streszczenie nie nazywa przy tym żadnego z dwóch,
bo przysłówek nie jest rolą, którą werdykt wylicza.
Zdanie przyjęte z takim drzewem jest droższe od wieloznacznego,
bo `valid` ktoś przeczyta
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
a instrument, który to liczy nad bankiem drzew, tego nie widzi:
zgodność ról porównuje podmiot i dopełnienie, a nie miejsce okolicznika.

Nad rejestrem ustaw wychodzi to samo w skali dziesięć razy mniejszej
i druga połowa odejmuje tam jedno zdanie
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
więc odejmuje w dwóch rejestrach naraz,
a nie w tym jednym, nad którym była mierzona.

Nad [README](../README.md) przysłówek nie kupuje ani jednego zdania.
Dwa zdania przenosi z odrzuconych na wieloznaczne
i jednym z nich jest to, o którym kolejka blokerów mówi,
że stoi na przysłówku i na niczym więcej
([corpus.md](corpus.md#where-the-analyses-stop)):

```text
Po to ta czarna lista tu stała i cały wywód za nią dalej stoi.
```

Wyprowadzenie dostaje, jednoznaczności nie,
bo w czytaniu, które przysłówek mu daje, `za nią` ma dwóch gospodarzy.
Kolejka mówi więc, gdzie analiza stanęła, i nie mówi, co dopisanie kupi,
także wtedy, gdy zdanie stoi na jednej klasie.

### Naprawę widać w tagsecie i nie da się jej postawić w gramatyce

Gospodarze spierają się o zdanie tylko wtedy,
gdy przysłówek stojący przed przymiotnikiem mógłby określać zdanie,
a Morfeusz tę różnicę niesie:
`tu`, `razem`, `dziś`, `teraz` i `nigdy` wychodzą jako `adv` bez stopnia,
a `bardzo`, `ściśle` i `szybko` jako `adv:pos`.
Stopień ma przysłówek odprzymiotnikowy, a pierwotny go nie ma,
i tylko pierwszy z tych dwóch określa przymiotnik.

Żądania obecności cechy formalizm nie ma.
`word("adv", degree="pos.com.sup")` bierze `tu` tak samo jak `bardzo`,
bo unifikacja pomija cechę, której konstytuent nie niesie,
i pomija ją rozmyślnie: część mowy nieodmienna
nie narusza zgodności, w której nie bierze udziału (`olski/grammar.py`).
Potrzebny tu warunek jest odwrotny do tamtego —
mówi „ta forma ma nieść stopień” — więc terminalowi brakuje go całego,
a nie wartości w nim.

Do ilu zdań ten warunek sięga, da się przeczytać bez niego,
bo zdania czytane odwrotnie sonda wypisuje:
w 10 z tych 15 przed przymiotnikiem stoi przysłówek bez stopnia —
`tu`, `razem`, `dziś`, `teraz`, `wczoraj`, `wkrótce` —
w 4 stoi tam przysłówek stopniowany, a w jednym nie ma tam żadnego
i pomyłka bierze się z czegoś innego.
Naprawa jest więc niepełna z góry:
`Oficjalnie cały Sejm RP śpi.` zostaje przy swoim czytaniu,
bo `oficjalnie` stopień niesie, a `Sejm` określać nie może.
Ile z 39 zdań odebranych ona oddaje, nie jest zmierzone, bo nie ma czym;
ruch trzyma [TODO.md](../TODO.md).

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

`olski/parse.py` builds the forest and summarizes it.
It is an Earley chart over the segmentation graph,
so one packed position stands for a constituent shape
however many derivations sit under it,
and a sentence with six undecided attachments
is six positions rather than sixty-four trees.
That is what the verdict wanted sooner than the grammar did:
the reader is shown the preposition and the heads it reaches,
one line per undecided choice.
[Werdykt jest zapytaniem o las](design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)
owns that argument,
and [tożsamość czytania](design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania)
owns what may share a position and how the counting joins two of them.

`olski/subset.py` is olski itself:
the grammar, what it reads as one word,
the readings it declines to consider, and the verdicts.

```sh
python3 -m olski.check -c "Zapisz plik konfiguracyjny." --readings
```
