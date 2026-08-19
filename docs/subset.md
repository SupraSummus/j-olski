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
Obie liczby są ceną, przy której kryterium odrzucono,
i wzięto je nad gramatyką z tamtej chwili, czyli bez przysłówka:
kryterium odrzucone zostaje odrzucone, kiedy jego cena się rusza,
więc przeliczenie broniłoby liczby, a nie decyzji.
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
  which is priced [below](#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka)
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
  joined by a conjunction or by a comma.
  The conjunction is the one Polish writes without a comma in front of it,
  on all three levels, so `Plik jest nowy ale duży.` has no derivation
- Two clauses joined by a comma and a conjunction at once,
  which is how Polish punctuates the conjunctions it puts a comma in front of:
  `Plany są niczym, ale planowanie jest wszystkim.`
  Those conjunctions are a closed list and the rest keep the position without the
  comma, so the two classes do not overlap and neither `A ale B` nor `A, i B`
  derives; the pair is priced
  [below](#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego)
- A colon opening a clause, which is how this register introduces an explanation:
  `Cena jest niska: gramatyka jest bezkontekstowa.`
  It stands above coordination rather than in it,
  so `A, B: C.` reads as `(A, B): C`,
  and what it does not take is the colon that opens an enumeration
  ([below](#what-it-does-not-cover-yet))
- The past tense, agreeing with the subject in gender as well as in number,
  and with the person clitic Morfeusz cuts off the form:
  `Program zapisywał ustawienia.`, `Napisałem program.`
  What it costs is [below](#czas-przeszły-żąda-rodzaju-od-każdego-szyku)
- A `że` clause as what a verb takes, which is a position in its frame
  rather than a construction beside the others:
  `Mieszkańcy grożą, że zablokują ulice.`
- Okolicznik wyrażony zdaniem, przed swoim zdaniem i za nim:
  `Program zapisuje ustawienia, gdy linter sprawdza tekst.`
  Pozycją ramy nie jest, bo żaden czasownik go nie żąda,
  więc dochodzi do zdania, a nie do orzeczenia;
  spójnik jest zamkniętą listą lematów, a konstrukcję wraz z ceną trzyma
  [poniżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)
- A relative clause on a noun phrase, agreeing with it in number and gender,
  with the pronoun standing for the subject, for the object,
  or under a fronted preposition together with the group it stands in:
  `Widoczny jest wzrost aspiracji społeczeństwa, które chce zdobywać wykształcenie.`,
  `ustawy, na podstawie której jest ono wydawane`
  The group carries the number and gender of the pronoun rather than of its own head,
  because it is the pronoun that agrees with the antecedent;
  the construction is argued and priced
  [below](#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja)
- Zdanie pytające o grupie imiennej na czole,
  w pozycji podmiotu, dopełnienia i wyrażenia przyimkowego:
  `Który aktor robi na tobie największe wrażenie?`, `Które zadania gmina wykonuje?`,
  `W którym roku ustawa weszła?`
  Grupą pytajną jest zaimek przy rzeczowniku, a nie sam zaimek,
  i jest ona rolą, którą werdykt nazywa, bo mówi, o co zdanie pyta.
  Pod przyimkiem stoi ta sama grupa, więc pozycja trzecia jest drugim czołem,
  a nie trzecim kształtem grupy.
- Pytanie zależne jako to, co czasownik bierze,
  czyli pozycja ramy osobna od pozycji zdania z `że`:
  `Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.`
  Spójnika ono nie ma, bo podporządkowuje sam zaimek,
  a jedno i drugie wraz z ceną trzyma
  [poniżej](#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał)
- Kopuła opuszczona przy jednym rzeczowniku, czyli zdanie składowe bez czasownika:
  `Przepisy, o których mowa, obowiązują.`, `Mowa o zadaniach.`
  Rzeczownik ten orzeka sam i niesie rolę, którą werdykt nazywa,
  bo zdanie z nim nie ma ani podmiotu, ani czasownika,
  a lematem jest `mowa` i nic poza nim;
  wywód i cenę trzyma
  [poniżej](#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną)
- Przysłówek u dwóch gospodarzy: jako okolicznik zdania, w każdej pozycji, którą
  okolicznik ma (`Program zapisuje ustawienia szybko.`, `Teraz program zapisuje
  ustawienia.`), i jako określenie przymiotnika, gdzie stoi sam przysłówek
  stopniowany (`Koszt bardzo dużego pliku jest niski.`).
  Okolicznik przysłówkowy jest przy tym rolą, którą werdykt nazywa,
  a określenie przymiotnika stoi w wypełnieniu roli nad nim;
  parę gospodarzy wraz z ceną trzyma
  [poniżej](#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)
- Any number of prepositional adjuncts on one verb,
  because `postępować wobec innych w duchu braterstwa` has two
- Prepositional phrases, with the preposition governing the case.
  One lemma stays out, by name: Morfeusz reads `a` as the preposition
  of `dwa bilety a pięć złotych`, which this register does not have
  ([below](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru))
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
Para ta jest ceną, przy której konstrukcja wchodziła,
i tak samo jak pary pozostałych konstrukcji jest wzięta nad gramatyką z tamtej chwili
([roadmap.md](roadmap.md#etap-6-reszta-konstrukcji)):
obietnicą jest wiersz kolejki liczony wtedy, gdy konstrukcji jeszcze nie ma,
więc dopisanie następnej rusza i wiersz, i to, ile z niego zostaje do wzięcia.
Różnica między 566 a 2934 jest tym,
czego kolejka blokerów z zasady nie mówi:
liczy zdania, na których konstrukcja stanęła,
a nie te, które jej dopisanie przyjmuje,
i większość tamtych zdań niesie obok czasu przeszłego jeszcze coś.
Widać to po samej kolejce, która po tej zmianie stawia w tym wierszu 297:
2071 zdań przesunęło swój bloker w prawo, zamiast zejść z listy.

Nad rejestrem, o który olskiemu chodzi, zakup jest zerowy albo ujemny:
nad siedmioma ustawami nie kupuje ani jednego zdania
i pięć przenosi z odrzuconych na wieloznaczne
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)).
Kolejka ze Składnicy i przebieg nad ustawami dają więc różne odpowiedzi,
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

### Negacja zmierzona: kupuje przeszło sto zdań i nie płaci dopełniaczem

Pełne wiersze są w [figury/negacja.txt](../figury/negacja.txt),
a polecenie i pliki, których zmiana każe je przeliczyć,
podaje ta figura ([`harness/figury.py`](../harness/figury.py)).

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
Wypada ona w sondzie, która mierzy szyk, i wynosi tam sześć zdań
([niżej](#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka)).
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
([niżej](#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka)),
więc czytanie, które ma czytelnik, nie ma się czym wyprowadzić,
i zamiast dwóch czytań wychodzi jedno, pewne siebie i błędne.
Jest to ta sama pomyłka co przy [wyliczonym ciele](design-notes.md#wyliczone-ciało-myli-się-w-stronę-werdyktu),
tylko widziana od strony konstrukcji, która ją wywołała.

Cztery zdania tego samego kształtu z tej listy zeszły,
i zdjął je szyk, a nie nic w negacji:
dopełnienie ma dziś ciało przed formą osobową swojego czasownika,
więc każde z nich wychodzi wieloznaczne
([niżej](#większość-tych-zdań-jest-naprawą-a-nie-ceną)).
Werdykt jest tam odmową i to jest cena zapłacona po tej zmianie w tej walucie,
w której ta sekcja liczy: czytanie czytelnika stoi na wydruku obok drugiego,
zamiast nie mieć się czym wyprowadzić.

## Szyk zmierzono: kupuje kilkadziesiąt zdań i odbiera kilka

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

Cenę tej konkurencji liczy `sonda/szyk.py` i wychodzi siedem zdań.

Pełne wiersze są w [figury/szyk.txt](../figury/szyk.txt),
a polecenie i pliki, których zmiana każe je przeliczyć, podaje ta figura
([`harness/figury.py`](../harness/figury.py)).
Mianownik jest w niej ten sam, co w tabelach [corpus.md](corpus.md#the-measurement):
13 035 lasów Składnicy z pełnym drzewem, morfologia złota,
i wchodzą do niego wszystkie, bez granicy na długość zdania.

Kilkadziesiąt zdań przechodzi z odrzuconych na przyjęte,
połowa tylu z odrzuconych na wieloznaczne,
a siedem z przyjętych na wieloznaczne, i tyle właśnie liczy kolumna ceny.
Zakup dzieli się między szyki nierówno — najwięcej bierze VOS, najmniej VSO —
a sumuje się dokładnie,
bo sonda nie znajduje ani jednego zdania,
które rusza się pod dwoma szykami naraz.
Cztery szyki są więc czterema rozłącznymi zakupami, a nie jednym podzielonym,
i płaci za nie sam SOV: pozostałe trzy nie odbierają jednoznaczności
ani jednemu zdaniu, które ją miało.

Zakup jest przy tym zakupem, a nie samym wyprowadzeniem:
zdanie przyjęte odwrotnie niż w banku drzew nie jest zakupem dla nikogo.
Wszystkie te zdania poza dwoma mają role zgodne z drzewem wzorcowym,
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

### Większość tych zdań jest naprawą, a nie ceną

Siedem zdań traci jednoznaczność, a pięć z nich traci ją razem z czytaniem,
którego polszczyzna nie ma, i to jest właściwy odczyt tej kolumny.

```text
Apostołowie tego nie praktykowali.
Nikt niczego nie wybiera, coś wybiera za nas.
Nikt go tu nie zapraszał!
Wtedy nikt nas nie zauważy.
Kuba tego nie pamięta, ale wie od mamy.
```

Rozstrzyga o tym drzewo wzorcowe:
pod gramatyką bez tych czterech szyków czytanie każdego z nich
nie zgadzało się z bankiem drzew, a czytanie pozostałych dwóch zgadzało.
Piąte z nich przyszło do tej kolumny razem z
[interpunkcją zdaniową](#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego),
bo bez przecinka przed spójnikiem olski tego zdania nie wyprowadzał wcale,
i pokazuje o tej kolumnie to, czego cztery pierwsze nie pokazują:
naprawa rośnie razem z pokryciem, bo zdanie przyjęte odwrotnie niż w banku drzew
trafia tu dopiero wtedy, gdy w ogóle się wyprowadza.
Wszystkie pięć są wyżej ceną, którą negacja płaciła trafnością
([wyżej](#cena-stoi-w-trafności-a-nie-w-liczbie-czytań)):
dopełniacz negacji poprzedzał swój czasownik,
brała go tam tylko przydawka dopełniaczowa,
i olski wypuszczał jedno czytanie, pewne siebie i odwrotne niż drzewo wzorcowe.
Szyk SOV daje czytaniu czytelnika ciało,
więc każde z nich wychodzi teraz wieloznaczne,
a wśród czytań stoi to, które ma bank drzew.
Werdykt `ambiguous` jest w tej gramatyce odmową,
a odmowa, która wypisuje czytania,
jest lepszym werdyktem niż jedno czytanie przeczytane na opak.

Pozostałe dwa są ceną i są tym samym sporem oglądanym bez naprawy:

```text
Kryterium wzrostu nie obowiązuje.
Janka nic nie odpowiada i zamyka drzwi.
```

Dopełniacz stojący przed czasownikiem czyta się tu i jako dopełnienie,
i jako przydawka rzeczownika przed nim,
a olski ma teraz oba ciała, więc melduje oba czytania.

Piąte zdanie tego kształtu naprawy nie dostało
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
i naprawą czterech czytań, a nie krokiem w rejestrze, do którego olski jest kierowany.

## Zdanie deklaruje córki, a warunek deklaruje szyk

Produkcja mówi naraz dwie rzeczy: z czego zdanie się składa
i w jakiej kolejności te córki stoją.
Rozdzielone, te dwie rzeczy mieszczą się w sześciu deklaracjach,
z których rozwinięcie pisze dwadzieścia osiem ciał `ClauseConjunct`.
Deklaracja wymienia same córki,
warunek precedencji obok niej mówi, które ich przestawienia wchodzą,
a rozwinięcie składa jedno z drugim przed rozbiorem
(`olski/precedencja.py`).
Kończy się ono przed tablicą Earleya, więc tablica dostaje ciała wypisane.
Olski zajmuje przez to szczebel 1 [drabiny](design-notes.md#the-cost-ladder)
i płaci dokładnie tym, czym ten szczebel każe płacić:
preprocesorem gramatyki, a nie innym parserem.

Warunek wyklucza jeden szyk i mówi który, zamiast go przemilczeć.
Jedna deklaracja wymienia podmiot, dopełnienie i czasownik,
a warunek pod nią odmawia temu przestawieniu,
w którym podmiot stoi pierwszy, a czasownik zaraz za nim:
zdanie tego szyku składa się z podmiotu i orzeczenia,
więc wypisane płasko drugi raz dałoby jednemu napisowi dwa wyprowadzenia.
Pozostałych pięciu szyków orzeczenie nie składa,
bo albo podmiot nie stoi w nich pierwszy, albo między nim a czasownikiem coś stoi.
Tego żąda od tej gramatyki decyzja o szyku wyżej —
szyk spoza olskiego ma być wykluczony warunkiem, a nie brakiem ciała —
i żąda tego samego od każdego szyku dopisanego później.

Miejsce na okolicznik wylicza to samo rozwinięcie
i przez to nie ma go jak zapomnieć w jednym ciele z trzech.
Reguła jest jedna: okolicznik staje po każdej córce, która jest grupą,
oraz na końcu zdania, którego nie zamyka orzeczenie —
to bierze swój okolicznik samo, przez `Complements`.
Pierwsza połowa tej reguły jest odpowiedzią na przyłączenie oddawane czytelnikowi
([niżej](#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)):
gdzie grupa imienna bierze wyrażenie przyimkowe za sobą,
tam musi umieć wziąć je też zdanie.

Po córce czasownikowej okolicznik nie staje, i jest to zawężenie,
a nie wniosek z tamtej reguły.
Polszczyzna tę pozycję ma, a olski jej nie ma i nikt nie policzył, ile to kosztuje:
`Trwa w tej sprawie dochodzenie.` jest przez nią zdaniem odrzuconym,
a `Zapisuje w pliku program ustawienia.` wychodzi jednym czytaniem,
w którym `program ustawienia` jest dopełnieniem,
i nie wychodzi tym, w którym `program` zapisuje `ustawienia`.
Drugie z tych dwóch jest tą samą pomyłką,
przed którą broni [reguła o obu czytaniach](#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
Rozwinięcie tego nie naprawia i nie po to jest.
Zmienia jedno: zawężenie mieści się po nim w jednym argumencie deklaracji,
a nie w trzydziestu dwóch ciałach, z których żadne go nie wypowiadało,
więc jest co wycenić, a wycenę trzyma `TODO.md`.

Cztery ciała gramatyka ma dlatego, że regułę liczy rozwinięcie, a nie ręka.
Zdanie względne i pytanie mają za wysuniętą rolą trzy miejsca,
a ciała z podmiotem przed czasownikiem miały dwa z nich,
dopóki każde miejsce wypisywało osobne ciało.
Bez trzeciego `Ustawa, którą organ w tym trybie wydaje, jest tania.`
wychodzi jednym czytaniem, w którym `w tym trybie` dochodzi do `organ`,
a czytania z okolicznikiem przy `wydaje` nie ma skąd wziąć —
czyli werdykt `valid` nad zdaniem, które czytelnik czyta dwojako.
Ciała są cztery, a nie dwa, bo przypadek wysuniętego dopełnienia rozstrzyga przeczenie
([wyżej](#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)),
więc każda z dwóch rodzin ma tę deklarację w dwóch wersjach.

Mnożenia się ciał rozwinięcie nie zdejmuje całego, bo część mnoży cecha.
`RelativeCore` ma dwie deklaracje z dopełnieniem zamiast jednej,
bo przypadek czoła zależy od tego, czy czasownik za nim przeczy,
a `NPConjunct` mnoży kształt głowy przez obecność przydawki za nią;
ani jedno, ani drugie nie jest kolejnością,
więc warunek precedencji nie ma tam czego powiedzieć.

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

Pełne wiersze są w [figury/przecinek.txt](../figury/przecinek.txt),
a polecenie i pliki, których zmiana każe je przeliczyć, podaje ta figura
([`harness/figury.py`](../harness/figury.py)).
Mianownik jest w niej ten sam, co w tabelach tamtego dokumentu:
13 035 lasów Składnicy z pełnym drzewem, morfologia złota,
i wchodzą do niego wszystkie, bez granicy na długość zdania.

Ani jedno zdanie nie przechodzi z przyjętego na wieloznaczne.
Wieloznacznych przybywa kilkadziesiąt i wszystkie przychodzą z odrzuconych,
czyli z tych, których gramatyka bez przecinka nie wyprowadzała wcale.
Konkurencji między poziomami sonda nie liczy z tych sum, tylko wprost,
zdanie po zdaniu, i znajduje ją dwa razy.
Żadnego zdania nie ruszają poziom zdaniowy i imienny naraz,
a o dwóch wszystkie trzy naraz mówią co innego niż każdy z osobna:

```text
Stworzyła polski oddział EquiLibre, organizowała konwoje z pomocą dla byłej
Jugosławii, Kazachstanu, Czeczenii.
```

Każdy poziom z osobna to zdanie odrzuca, a wszystkie naraz czynią je wieloznacznym,
czyli dwie produkcje dały mu czytanie, którego żadna z nich nie dała.
Argument o konkurencji ma więc nad tym korpusem dwa zdania,
i oba przyszły z konstrukcjami dopisanymi po tym pomiarze:
pierwsze z czasem przeszłym, a drugie ze zdaniem okolicznikowym
([niżej](#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie)):
`kiedy` jest w banku drzew spójnikiem, więc bez tamtej produkcji
zdanie, w którym stoi, nie ma pod złotą morfologią ani jednego czytania
i do tej pary wejść nie mogło.

Po drugiej stronie stoi zakup: przeszło sto zdań przechodzi
z odrzuconych na przyjęte, a bierze je w większości poziom zdaniowy;
resztę dokłada imienny, a przymiotnikowy trzy.
Role zgodne z drzewem wzorcowym ma z nich cztery piąte,
a reszcie bank drzew albo nie daje roli do porównania,
albo daje rolę, której olski nie obsadził;
niezgodne są trzy i żadne z nich nie jest rolą odwróconą.
Jedno niesie dopełniacz negacji przed czasownikiem, drugie przysłówek w podmiocie,
i obie te ceny mają właściciela gdzie indziej
([wyżej](#cena-stoi-w-trafności-a-nie-w-liczbie-czytań),
[niżej](#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe));
trzecie — `Powtarzaj je tak często, jak to jest potrzebne.` —
czyta `jak to` jako wyrażenie przyimkowe tam, gdzie bank drzew ma zdanie porównawcze,
czyli konstrukcję, której olski nie ma.

Nowe wieloznaczności nie biorą się z przecinka, tylko z przyłączenia.
`Warszawska kuria metropolitalna ma wśród swoich licznych włości nieruchomość
w podwarszawskim Skolimowie, uzdrowiskowej dzielnicy Konstancina-Jeziorny.`
wychodzi dwoma czytaniami, bo wyrażenie przyimkowe dochodzi do rzeczownika
albo do czasownika, i tak samo różnią się czytania pozostałych.
Jest to ta sama wieloznaczność, którą olski
[oddaje czytelnikowi](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera):
koordynacja przecinkiem daje jej więcej miejsc, w których się mieści,
a nie nowy rodzaj sporu.

Poziom przymiotnikowy ruszał kiedyś zero zdań i rusza dziś sześć,
z czego trzy przyjmuje: `duży, ciężki plecak` jest polszczyzną,
a zdania, w których ta produkcja jest ostatnią brakującą,
przyszły razem z przysłówkiem, bo to on zdjął z nich blokera przed nią.

Nad rejestrem, o który olskiemu chodzi, przecinek kupuje trzy zdania.
To samo porównanie nad prozą wyciągniętą z README
rusza cztery werdykty, trzy na poziomie zdaniowym i jeden na imiennym.
`Co ekstrakcja po drodze zmyśla, mówi docs/extraction.md`
i dwa zdania, które przyszły tu razem z
[interpunkcją zdaniową](#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego),
przechodzą z odrzucenia w wieloznaczność,
a `Czarna lista kupowała jednak co innego, niż obiecywała`
gramatyka bez przecinka odrzuca, a z nim wyprowadza jednym czytaniem.
Ostatniego z nich nie było w tym pomiarze, dopóki gramatyka nie miała czasu
przeszłego, i to on przeniósł poziom imienny z zera na jedno zdanie.
`Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego`
stało w tej trójce i zeszło z niej, nie zmieniając werdyktu:
przecinek sam już go nie wyprowadza, bo stoi w nim przed spójnikiem,
i rusza go odtąd tamta produkcja, a nie ta.
Poziom przymiotnikowy nie rusza tu nic,
bo pozostałe zdania tego pliku, które niosą przecinek,
niosą też zdanie podrzędne, przysłówek albo rzeczownik odczasownikowy.
Przecinek wszedł więc za pokrycie w cudzej polszczyźnie,
a nad tą prozą czeka na to, co w reszcie tych zdań stoi obok niego.
Podrzędność, która stała w tej kolejce pierwsza, weszła i tej liczby nie ruszyła
([niżej](#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja)),
a czas przeszły ruszył ją, nie ruszając liczby zdań przyjętych
([wyżej](#czas-przeszły-żąda-rodzaju-od-każdego-szyku)).
Przysłówek wszedł po nich i tej liczby też nie ruszył,
choć nad Składnicą przeniósł zakup przecinka o połowę w górę.
Dwukropek stał w tej kolejce następny i wszedł
([niżej](#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego)),
też nie ruszając tej liczby,
więc nad tą prozą czeka ona na rzeczownik odczasownikowy
i na polską formę, której słownik nie zna
([roadmap.md](roadmap.md#etap-5-słowa-których-słownik-nie-ma)).

## Interpunkcja zdaniowa spina zdania, które już się wyprowadzają

Polszczyzna łączy dwa zdania spójnikiem, przecinkiem albo jednym i drugim naraz,
a dwukropkiem wprowadza wyjaśnienie.
Olski wyprowadzał z tego dwa pierwsze sposoby
([wyżej](#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania)),
a do reszty prowadził wiersz `interp`,
pierwszy w kolejce blokerów z trzema tysiącami zdań
([corpus.md](corpus.md#where-the-analyses-stop)).

Nowego kształtu zdania ta konstrukcja nie wymaga,
bo jej członami są zdania, które gramatyka wyprowadza i bez niej.
Wymaga natomiast dwóch rozstrzygnięć, po jednym na znak.

**Dwukropek rozdziela zdanie wyżej niż przecinek.**
Produkcja należy przez to do zdania, a nie do zdania składowego:
`Sentence → Clause : Clause .`
Dwukropek wpuszczony tam, gdzie przecinek, czyli do `Clause`,
byłby prawostronnie rekurencyjny razem z nim
i `A, B: C.` wyprowadzałby jako `A, (B: C)`,
gdzie polszczyzna czyta `(A, B): C`:
przed dwukropkiem jest teza, a za nim całe jej wyjaśnienie.
Werdykt pokazuje ten podział znakiem `…` przy roli,
tak samo jak przy koordynacji przecinkiem,
bo w jednym i w drugim po którejś ze stron roli zdanie ma jeszcze jedno składowe.

Jednoznaczności ta produkcja nie odbiera ani jednemu zdaniu,
a wynika to z gramatyki, nie z przebiegu.
Dwukropek wchodzi w jedno ciało i nie bierze go żaden inny terminal,
więc zdanie z dwukropkiem albo wyprowadza się tą produkcją, albo nie ma czytania wcale,
a zdania bez dwukropka ta produkcja nie dotyczy.
Zero w kolumnie ceny jest przez to wyprowadzone, a nie zmierzone,
i pilnuje tego `tests/test_subset.py`:
dwukropek bierze dokładnie jedna produkcja,
a druga zamieniłaby to zero w liczbę, którą trzeba by policzyć.

**Przecinek przed spójnikiem jest faktem o słowie.**
`Plany są niczym, ale planowanie jest wszystkim.` przecinka wymaga,
a `Program zapisuje ustawienia i linter sprawdza tekst.` nie bierze go wcale,
i rozstrzyga o tym sam spójnik, a nie miejsce, w którym pada.
Spójnik zdaniowy rozdziela się przez to na dwie klasy,
a drugą wyznacza warunek ujemny na pierwszą, bo klasy nie mają się zachodzić:
lemat wzięty obiema pozycjami dałby polszczyźnie dwa napisy tam, gdzie ma ona jeden.
Klasa z przecinkiem jest zamkniętą listą —
`ale`, `a`, `lecz`, `natomiast`, `więc`, `zatem`, `toteż` —
i obejmuje dwie części mowy naraz,
bo Morfeusz zna `więc` jako `comp`, a `ale` jako `conj`,
a o interpunkcji przed nimi ten podział nie mówi nic.
`zaś` i `jednak` na tej liście nie figurują, bo czoła swojego zdania nie zajmują:
polszczyzna stawia je za pierwszym wyrazem — `linter zaś sprawdza tekst` —
i jest to ten sam warunek, którym lista spójników okolicznikowych wyklucza `bowiem`
([niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).
Lemat pominięty na liście zostaje przy pozycji bez przecinka,
więc pominięcie nie odbiera ani jednego zdania.

Podział ten odbiera zarazem napisy, których polszczyzna nie ma.
`Program zapisuje ustawienia ale linter sprawdza tekst.` wyprowadzało się,
dopóki jedno ciało brało całą klasę `conj`,
a klasa bez przecinka dochodzi do wszystkich trzech poziomów koordynacji,
więc `Plik jest nowy ale duży.` przestaje wychodzić jednym czytaniem.
Pozycji z przecinkiem grupa imienna i przymiotnikowa nie dostają,
bo `nie polszczyzny, a dziedziny` jest w nich elipsą, a nie ciągiem współrzędnym.
Zawężenie tych dwóch poziomów nie rusza ani jednego zdania w żadnym z trzech
rejestrów — ani nad Składnicą, ani nad README, ani nad ustawami —
więc płaci za nie sam werdykt, który przedtem kłamał pewnie.

Bez trzeciego warunku ta pozycja nie kupiłaby prawie nic,
a warunek ten pada na lemat przyimka, a nie na produkcję
([niżej](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)):
Morfeusz czyta `a` także jako przyimek,
więc każde `, a` w zdaniu wychodziło okolicznikiem wysuniętym drugiego składowego.

Poza gramatyką zostają dwie rzeczy, obie zapisane
[niżej](#what-it-does-not-cover-yet):
dwukropek otwierający wyliczenie i średnik.

### Interpunkcja zdaniowa zmierzona: kupuje kilkadziesiąt zdań i nie odbiera żadnego

Mierzony jest ruch werdyktu, a nie stan gramatyki:
zdanie idzie przez tę gramatykę i przez tę samą z wyjętą produkcją,
a liczy się to, na czym te dwa werdykty się różnią.
Znaki zdejmują się osobno, bo konkurują z czym innym i cena każdego jest osobną liczbą.

Pełne wiersze są w [figury/interpunkcja.txt](../figury/interpunkcja.txt),
a polecenie i pliki, których zmiana każe je przeliczyć, podaje ta figura
([`harness/figury.py`](../harness/figury.py)).
Mianownik jest w niej ten sam, co w tabelach tamtego dokumentu:
13 035 lasów Składnicy z pełnym drzewem, morfologia złota,
i wchodzą do niego wszystkie, bez granicy na długość zdania.

Czterdzieści osiem zdań przechodzi z odrzuconych, dwadzieścia sześć na przyjęte
i dwadzieścia dwa na wieloznaczne, a z przyjętego na wieloznaczne — ani jedno.
Dwukropek daje z tego pięć zdań, a przecinek przed spójnikiem czterdzieści trzy,
i suma wychodzi dokładnie z tych dwóch:
konkurencji między znakami sonda nie znajduje nad tym korpusem ani razu,
ani zdania, które rusza się pod jednym i pod drugim,
ani takiego, o którym oba naraz mówią co innego niż każdy osobno.

Role zdań nowo przyjętych zgadzają się z drzewem wzorcowym w dwudziestu jednym
przypadku na dwadzieścia sześć, a niezgodnych nie ma ani jednego:
trzem bank drzew nie daje roli do porównania, a dwóm daje ją częściowo.
Liczba zdań niezgodnych z drzewem wzorcowym nie rusza się przy tym w całym przebiegu
i zostaje na dwudziestu jednym
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)),
więc ta konstrukcja nie wydaje ani jednego werdyktu wbrew drzewu.

Nad prozą, o którą olskiemu chodzi, interpunkcja zdaniowa nie kupuje
ani jednego zdania przyjętego, tak samo jak pięć dopisań przed nią,
a trzy zdania przenosi z odrzuconych na wieloznaczne.
Jednym z tych trzech jest zdanie, które warunek na przyimek stąd odebrał
([niżej](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)),
więc wobec gramatyki przed tą zmianą wieloznacznych przybywa dwa, a nie trzy.
Jest to o kolejce nad tym plikiem odczyt, a nie o konstrukcji:
zdania README, które stały na dwukropku, stoją teraz na rzeczowniku
odczasownikowym, na formie, której słownik nie zna, na `dopiero` albo na strukturze,
czego [tamten przebieg](corpus.md#where-the-analyses-stop) nie przewidział inaczej,
niż mówiąc, że większość zdań odrzuconych niesie dwie klasy albo więcej.
Nad rejestrem ustaw wypada ta para najskromniej z trzech:
dwukropek nie rusza tam ani jednego werdyktu, bo za każdym dwukropkiem tej prozy
stoi wyliczenie, a przecinek przed spójnikiem rusza jeden werdykt i nic nie odbiera
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)).

Z listy form bez licencji nad prozą README zeszły natomiast oba znaki:
dziewiętnaście zdań README niosło na niej dwukropek albo `więc`,
dziewięć z nich staje teraz na strukturze, a nie na znaku,
jedno wychodzi wieloznaczne,
a dziewięć stoi dalej na innej formie, którą werdykt nazywa.
Dopiero to mówi, czego w tych zdaniach brakuje.

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

## Rozdzielające `a` nie jest przyimkiem tego rejestru

Morfeusz daje formie `a` cztery czytania i jednym z nich jest przyimek rządzący
mianownikiem — ten z `dwa bilety a pięć złotych`, czyli z ceny za sztukę.
Wyrażenie przyimkowe olskiego bierze przyimek wraz z przypadkiem, którym on rządzi,
więc bez warunku niżej `a` otwiera je tak samo jak `w` albo `z`,
a grupa imienna po nim stoi w mianowniku,
czyli w tym samym przypadku, w którym stoi podmiot zdania po spójniku.
Każde `, a` w zdaniu wychodzi przez to okolicznikiem wysuniętym drugiego składowego:
`Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego.`
miało przed tym warunkiem trzy czytania i każde z nich niosło
`„a podmiot jednego” → „jest”`.

Polszczyzna tego zdania tak nie czyta.
Warunek obejmuje oba wyrażenia przyimkowe tej gramatyki — zwykłe i to,
które wysunęło zaimek względny — i mówi tyle: przyimek tego wyrażenia nie jest `a`.
Jest to trzeci warunek ujemny w tej gramatyce
i drugi postawiony na lemacie po to,
żeby odebrać czytanie, którego polszczyzna w tym miejscu nie ma
([wyżej](#zaimek-rzeczowny-nie-rządzi-dopełniaczem)).
Tańsza z dwóch dróg pyta właśnie o to, co produkcja licencjonuje,
a nie o to, co słownik oferuje
([roadmap.md](roadmap.md#etap-3-czytania-których-polszczyzna-nie-ma)).

Kryterium ogólniejsze wygląda tu na tańsze: żądanie „rządź jednym z pozostałych
sześciu przypadków” powiedziałoby to samo o każdym słowie naraz.
Nie powiedziałoby, i mówi to sam słownik.
Mianownikiem rządzą w nim także `jak`, `jako`, `niż`, `co` i `aniżeli`,
czyli wykładniki porównania,
i wszystkie pięć padają w prozie, którą to repozytorium czyta —
nad README, siedmioma ustawami i korpusem audytowym razem `niż` 194 razy,
`co` 186, `jako` 117, `jak` 71, `aniżeli` 5, przy 333 formach `a`.
Kryterium na przypadek zabrałoby więc razem z rozdzielającym `a` i te pięć.

Cena jest zerowa i jest to wynik pomiaru, a nie założenie.
Pod złotą morfologią przebieg nad Składnicą nie rusza ani jednego zdania z 13 035,
bo tam każda forma ma jedno czytanie wybrane przez człowieka
i `a` nie jest w tym korpusie przyimkiem ani razu.
Pod żywą morfologią, czyli nad prozą README, warunek odbiera jedno zdanie —
to wypisane wyżej — i oddaje je z powrotem przecinek przed spójnikiem
([wyżej](#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego)),
z trzema czytaniami w miejsce trzech.
Liczba czytań wychodzi więc ta sama przed i po,
a różnią się one tym, że tamte trzy niosły okolicznik, którego zdanie nie ma,
a te trzy niosą podmiot, który ono ma.
Cena i zakup nie dają się tu policzyć w żadnej z dwóch walut,
którymi mierzy się dopisanie, i jest to drugi taki przypadek
([wyżej](#cena-stoi-w-trafności-a-nie-w-liczbie-czytań)).

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
64 022 schematami, a obok nich 1 996 lematów rzeczownikowych 14 295 schematami,
i idzie na licencji CC BY-SA 4.0.
Mówi przy tym o czasowniku znacznie więcej, niż którykolwiek z pytających umie żądać,
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
czyli słowa wraz z tym, które z tych zdań są o nich prawdziwe:
zdanie pierwsze niesie 7 941 wpisów, drugie 285, a trzecie 2 498.
Ramy ten plik nie niesie, bo rama jest słowem gramatyki, a nie słownika.
Nazywa ją `olski/subset.py` razem z domyślną, od której ją odejmuje.
Czyta go `olski/walencja.py`, i czyta dla wszystkich, którzy pytają,
bo rama jest faktem o słowie, a nie o kierunku, w którym się go używa;
wywód trzyma [design-notes.md](design-notes.md#the-round-trip-invariant).

Czwarte zdanie tego pliku nie jest zdaniem prawda-fałsz, tylko zbiorem:
przyimki, których żąda rama tego słowa, wzięte z pozycji `prepnp` Walentego.
Kolumnę tę plik wypisuje przy czasowniku i przy rzeczowniku,
bo pyta o nią świadek ramowy warstwy rozstrzygającej i pyta po obu stronach
spornego wyrażenia:
rzeczownik wskazuje mu gospodarza, a czasownik wskazanie odbiera
([disambiguation.md](disambiguation.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)).
Gramatyka jej nie czyta i nie ma po co:
wyrażenie przyimkowe przyłącza się u olskiego wszędzie, gdzie polszczyzna je stawia,
a wybór miejsca należy do czytelnika
([wyżej](#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).

Kolumna ta niesie coś przy 12 195 wpisach,
a 6 179 z nich weszło do pliku nią samą, bez ani jednego z trzech zdań.
Rzeczownik wchodzi tak zawsze, bo zdania tego leksykonu są o czasowniku
i o rzeczowniku nie orzekają żadnego,
a czasownik o ramie domyślnej wchodzi wtedy, gdy jego schemat przyimka żąda.

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

Klasa słowa jest drugim wymiarem klucza, a nie częścią lematu.
Morfeusz daje `otwierać` i `otwierać się` ten sam lemat,
a wziąć mogą co innego,
więc rama trzymana pod samym lematem zlewałaby te dwa czasowniki w jeden.
Rzeczownik jest z tego samego powodu klasą trzecią, a nie osobnym plikiem:
lemat go od czasownika nie rozdziela, a klucz rozdziela.
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

Cena i zysk są zmierzone nad Składnicą i idą w obie strony;
liczby niżej wzięto nad gramatyką z chwili, w której leksykon wchodził,
czyli bez przysłówka i bez czterech szyków.
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
  --rzeczowniki walenty_20160418-text/nouns/walenty_20160418_nouns_all.txt \
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
Własną pozycję dostały [niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)
i jest nią okolicznik zdania, czyli dokładnie ta, którą zajmują.

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

### Okolicznik wyrażony zdaniem nie jest pozycją ramy i dochodzi do zdania

Zdania z `że` żąda czasownik, a zdania z `gdy` nie bierze żaden.

```text
Program zapisuje ustawienia, gdy linter sprawdza tekst.
Gdy linter sprawdza tekst, program zapisuje ustawienia.
```

Zdanie z `gdy` mówi, kiedy zachodzi to, o czym mówi zdanie obok niego,
i mówi to o całym tym zdaniu, a nie o jego orzeczeniu,
więc dochodzi tam, gdzie dochodzi wyrażenie przyimkowe wysunięte przed zdanie:
do zdania składowego, a nie do `Complements`.
Tym jednym różni się ta konstrukcja od [zdania z `że`](#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej),
a reszta jest w obu ta sama: przecinek należy do konstytuentu, który spójnik tworzy,
a nie do produkcji nad nim.

Przecinek stoi przy tym po tej stronie, po której stoi zdanie nadrzędne,
więc ciała są dwa, a wiąże je z pozycją cecha.
Bez niej ciało z przecinkiem z przodu staje na czele zdania,
a olski wyprowadza napis zaczynający się przecinkiem, którego nikt nie napisał.

Spójnik jest warunkiem na lemat i lista jest zamknięta,
bo klasa `comp` niesie także takie spójniki, których ta produkcja wziąć nie może.
Spójnik ma stać na czele swojego zdania, czego `bowiem` nie robi:
polszczyzna stawia je za pierwszym wyrazem zdania.
Zdanie pod spójnikiem ma być oznajmujące, czyli takie, jakie ta gramatyka wyprowadza,
a `aby`, `żeby`, `by`, `gdyby` i `jakby` żądają trybu przypuszczającego.
Olski nie odróżnia go od czasu przeszłego, bo cząstki `by` nie bierze żadna produkcja,
więc wpuszczone wyprowadzałyby `aby program zapisuje ustawienia`,
czego polszczyzna nie ma,
a obietnicą podzbioru jest, że każde zdanie olskiego jest zdaniem polskim.
`więc` Morfeusz znakuje tak samo i nie ma go na liście z trzeciego powodu:
zdania nie podporządkowuje, tylko dokłada skutek,
więc `Program zapisuje ustawienia, więc linter sprawdza tekst.`
jest dwoma zdaniami spiętymi spójnikiem po przecinku,
czyli tą konstrukcją, którą ten dokument trzyma
[wśród nieobjętych](#what-it-does-not-cover-yet).

Listy są przez to dwie, a nie jedna, bo wysunięcie jest faktem o słowie.
Ciało z okolicznikiem za zdaniem bierze każdy spójnik z listy,
a ciało z okolicznikiem przed zdaniem tylko te,
których zdanie polszczyzna wysuwa:
`Zostaję w domu, bo pada.` jest polszczyzną, a `Bo pada, zostaję w domu.` nie jest,
i tak samo dzieli się `gdyż` od `ponieważ`, choć oba mówią o przyczynie.
Fakt ten skład trzyma o dwóch z tych lematów
(`staje_na_czele` w `olski/skład/spójniki.py`),
bo jest to fakt o słowie, a nie o kierunku, w którym się go używa,
i [TODO.md](../TODO.md) trzyma ruch, którym oba kierunki czytałyby jeden leksykon,
tak jak czytają jeden leksykon walencyjny.
Sam podział ma przy tym świadka w [figury/czoło.txt](../figury/czoło.txt):
nad Składnicą `gdyż` nie otwiera ani jednego zdania,
tak samo jak `bowiem`, którego gramatyka nie bierze wcale,
a `gdy` i `jeśli` otwierają dwie piąte swoich wystąpień i ponad połowę.
Liczby dla `bo` i dla `albowiem` mierzą co innego niż tamte
i sonda mówi to o sobie sama:
zdanie zaczynające się od tych spójników odsyła w tym korpusie do zdania przed nim,
zamiast być zdaniem podrzędnym wysuniętym przed swoje nadrzędne.
Dwa wpisy listy wysuwanej nie mają w tym korpusie świadka wcale:
`dopóki` i `póki` stoją w nim raz albo dwa i ani razu na czele zdania,
więc na tej liście stoją z samego znaczenia, a nie z pomiaru.

Okolicznik ten jest rolą, którą werdykt nazywa, tak samo jak przysłówek
([niżej](#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)),
i jest zarazem zdaniem podrzędnym, czym żadna inna rola nie jest.
Symbol stojący i wśród ról, i wśród zdań podrzędnych
rozstrzyga o dwóch rzeczach naraz, i rozstrzyga je przeciwnie:
streszczenie nazywa ten okolicznik całym napisem, bo jest on rolą,
a w środek jego nie zagląda, bo podmiot spod spójnika jest podmiotem tamtego zdania.
Zejście po role zatrzymuje się więc na takim węźle, a nie przed nim
(`Node.find` oraz `_pierwsza_rola` w `olski/parse.py`),
a kosztuje to jeden warunek w obu zejściach po role.

Widać po tym, do którego zdania okolicznik doszedł:

```text
Pomiar mówi, że linter działa, ponieważ tekst jest gotowy.
```

Czytania są dwa i oba polszczyzna nad tym zdaniem ma,
a streszczenie rozdziela je nazwaniem tej roli albo przemilczeniem jej:
okolicznik doszedł do zdania streszczanego albo do tego, które stoi pod `że`.

### Zdanie okolicznikowe zmierzono: pod złotą morfologią jest darmowe, a pod żywą nie

Pełne wiersze są w [figury/okolicznikowe.txt](../figury/okolicznikowe.txt),
a te spod morfologii żywej w [figury/okolicznikowe-żywa.txt](../figury/okolicznikowe-żywa.txt);
polecenie i pliki, których zmiana każe je przeliczyć, podaje każda z tych dwóch
([`harness/figury.py`](../harness/figury.py)).

Nad Składnicą pod złotą morfologią konstrukcja zdejmuje z listy odrzuconych
blisko pięćdziesiąt zdań, z tego niespełna połowę jednoznacznie,
i nie odbiera jednoznaczności ani jednemu zdaniu przyjętemu wcześniej.
Wśród nowo przyjętych zgodność z drzewem wzorcowym rośnie o każde,
które ma w nim rolę do porównania,
a o ani jedno odwrócenie roli nie rośnie
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)),
więc konstrukcja nie wydaje przy tym ani jednego werdyktu wbrew drzewu.
Pozycja za zdaniem zdejmuje z tej listy dwa razy tyle zdań, co pozycja przed nim,
a nie spierają się one o ani jedno:
zdanie ma spójnik po przecinku albo przed nim, i nigdy jedno i drugie naraz,
więc obie pozycje mierzą się osobno i sumują się bez reszty.

Cenę widać dopiero pod morfologią żywą, i widać tam, o co ta konstrukcja konkuruje.
Sześć zdań traci jednoznaczność i wszystkie niosą `gdy` albo `kiedy`,
czyli spójnik, któremu Morfeusz daje obok czytanie przysłówkowe:

```text
Nie lubię, gdy ktoś jest natarczywy.
```

Zdanie to wychodziło przedtem jednym czytaniem i było ono nieprawdziwe —
dwa zdania spięte przecinkiem, w których `gdy` jest okolicznikiem przysłówkowym —
a teraz stoi obok czytania, które to zdanie ma.
Konstrukcja kupuje więc prawdę o zdaniu i płaci za nią jednoznacznością,
czyli robi to samo, co drugi gospodarz przysłówka,
i rozstrzyga o niej [ten sam kierunek](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę):
`valid` mówiący o zdaniu nieprawdę czyta się jak twierdzenie.
Jednoznaczność wraca tu warunkiem słownikowym, a nie produkcją —
czytanie przysłówkowe stojące przy czytaniu spójnikowym —
a cenę tego warunku, zmierzoną osobno, zapisuje [TODO.md](../TODO.md).

Nad rejestrem ustaw nie kupuje ani jednego zdania jednoznacznie
i przenosi pięć z odrzuconych na wieloznaczne
([ustawy.md](ustawy.md#co-gramatyka-z-tego-wyprowadza)),
czyli zachowuje się tam tak jak czas przeszły, tyle że niczego nie odbiera.

Poza konstrukcją zostają dwie rzeczy, obie widoczne dopiero po niej.
Okolicznik wstawiony w środek swojego zdania — `Program, gdy linter sprawdza tekst,
zapisuje ustawienia.` — nie ma ciała i jest zdaniem odrzuconym.
Okolicznik za ciągiem współrzędnym dochodzi zaś do zdania składowego,
przy którym stoi, a nie do całego ciągu,
więc `Program zapisuje ustawienia i linter sprawdza tekst, ponieważ tekst jest gotowy.`
wychodzi jednym czytaniem tam, gdzie polszczyzna ma dwa.
Jest to ta sama granica, którą trzyma [zasięg koordynacji](#nothing-above-a-coordination-distributes-into-it),
widziana od strony okolicznika, a oba te ruchy zapisuje [TODO.md](../TODO.md).

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

Kosztowało to jedno zdanie Składnicy i było nim pytanie:
`Który aktor robi na tobie największe wrażenie?`,
gdzie `Który` jest zaimkiem pytajnym przy rzeczowniku.
Pytanie zależne — `określają, które zadania` — kosztowało tyle samo w rejestrze
ustaw: zdanie, które wychodziło błędnie, wychodziło po nim odrzucone.
Cena była ceną pozycji, której gramatyka wtedy nie miała, a którą ten warunek nazwał;
stawia ją [pytanie](#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał),
więc oba te zdania wyprowadzają się dziś, każde raz.

### Pytanie zmierzono: nie odbiera żadnego zdania i oddaje to, które warunek zabrał

Pełne wiersze są w [figury/pytanie.txt](../figury/pytanie.txt),
a te spod morfologii żywej w [figury/pytanie-żywa.txt](../figury/pytanie-żywa.txt);
polecenie i pliki, których zmiana każe je przeliczyć, podaje każda z tych dwóch
([`harness/figury.py`](../harness/figury.py)).

Konstrukcje są dwie i dzielą kształt ze zdaniem względnym.
Zdanie pytające stoi samo i zamyka się pytajnikiem,
pytanie zależne zaczepia się o czasownik przecinkiem,
a w obu na czole zdania stoi grupa pytajna
i za nią zdanie bez tej roli, którą ta grupa zajmuje.
Deklaracje pisze jedna funkcja i dla nich, i dla zdania względnego
(`_wysunięta_rola` w `olski/subset.py`),
bo te dwie rodziny różni samo czoło:
zaimek pytajny przy rzeczowniku albo zaimek względny, sam lub przy rzeczowniku.
Role są dwie — podmiot i dopełnienie — i są to te same,
które zdanie względne wysuwa bez przyimka.

```text
Który aktor robi na tobie największe wrażenie?
Które zadania gmina wykonuje?
Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.
```

Cena wyszła zerowa w obu korpusach i pod obiema morfologiami banku drzew:
ani jedno zdanie przyjęte wcześniej nie traci jednoznaczności ani wyprowadzenia,
i nie rusza się ani jeden werdykt poza tymi, które ta konstrukcja kupuje.
Nad Składnicą zdanie pytające zdejmuje z listy odrzuconych jedno zdanie
i jest nim dokładnie to, które zabrał
[warunek na lemat](#zaimek-względny-nie-jest-przymiotnikiem-przy-rzeczowniku),
a pytanie zależne przenosi jedno zdanie z odrzuconych na wieloznaczne.
Nad rejestrem ustaw pytanie zależne kupuje jedno zdanie jednoznacznie
([ustawy.md](ustawy.md#co-gramatyka-z-tego-wyprowadza)),
a zdanie pytające nie kupuje niczego.
Obie pozycje nie spierają się przy tym o ani jedno zdanie,
bo pytanie zamyka się pytajnikiem albo stoi za przecinkiem, i nigdy jedno i drugie.

Zakup wynosi po jednym zdaniu na korpus, a liczba ta mówi o rejestrze,
a nie o produkcjach.
Pytań jest w Składnicy 881 na 13 035 zdań z drzewem wzorcowym,
czyli jedno na piętnaście,
a lemat, na którym grupa pytajna stoi, otwiera dwa z nich
([figury/pytajne.txt](../figury/pytajne.txt)).
Reszta pyta czym innym i każde z tych słów żąda innego kształtu:
`czy` otwiera pytanie o rozstrzygnięcie i nie zajmuje ani podmiotu, ani dopełnienia,
`kto` i `co` stoją same, bez rzeczownika przy sobie,
a `jak`, `dlaczego` i `gdzie` są przysłówkami.
Kolejka z tej tabeli jest więc kolejką kształtów, a nie lematów:
lemat dopisany do `ZAIMEK_PYTAJNO_WZGLĘDNY` nie kupuje ani jednego z tych zdań.

Drugie z tych dwóch pytań Składnicy nie wyprowadza się i nie staje na pytaniu:
`Które łóżko było Panka?` ma orzecznik w dopełniaczu,
którego ta gramatyka nie ma,
więc grupa pytajna dosięga w tym korpusie jednego zdania z dwóch.

Zdanie nowo przyjęte wychodzi zgodne z drzewem wzorcowym,
bo grupa pytajna niesie obok swojej etykiety etykietę roli, którą zajmuje
([niżej](#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)):
bank drzew nazywa `Który aktor` podmiotem i olski nazywa tę rozpiętość tak samo,
a grupa pytajna stoi obok tego i mówi, o co zdanie pyta.
Nad pytaniem zależnym żadna z tych dwóch etykiet nie pada w streszczeniu
i werdykt mówi tam tyle, co nad zdaniem z `że`, czyli nic:
oba są zdaniami podrzędnymi, a streszczenie w nie nie zagląda.

Pozycja ramy jest przy tym osobna od pozycji zdania z `że`, a nie tym samym `comp`.
Walenty rozdziela je kształtem — `cp(int)` stoi w nim obok `cp(że)` —
a lematów, które biorą pierwszy i nie biorą drugiego, jest 220:

```sh
python3 - <<'EOF'
from olski.walenty import bierze, schematy
wedle_lematu = schematy("walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt")
print(sum(
    1
    for jego in wedle_lematu.values()
    if bierze(jego, ("cp(int)",)) and not bierze(jego, ("cp(że)",))
))
EOF
```

`analizować`, `badać` i `doglądać` są w tej liczbie,
więc czasownik biorący pytanie i nie biorący zdania z `że` istnieje,
a pozycja wzięta jako jedna nie miałaby czym tego zapisać.
Samego zawężenia tej pozycji do leksykonu nikt nie zmierzył,
więc stoi ona w [ramie domyślnej](#walencja-jest-leksykonem-o-ramie-domyślnej)
tak samo jak `comp`,
a przebieg, który by je wycenił, zapisuje [TODO.md](../TODO.md).

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

Wysunięte na czoło jest przy tym nie sam zaimek,
ale cała grupa, w której on stoi.
Pozycje ma ona dwie i obie niesie rejestr ustaw.
Pod przyimkiem niesie ją `ustawy, na podstawie której jest ono wydawane`,
zdanie „Zasad techniki prawodawczej”,
gdzie `której` jest dopełniaczem przy `podstawie`.
Bez przyimka grupa stoi w podmiocie i w dopełnieniu zdania składowego:
`ustawa, której przepisy obowiązują`.

Grupa niesie liczbę i rodzaj dwa razy, i to jest cała jej trudność.
Przypadka żąda od niej przyimek albo rola, w której stanęła,
a wypuszcza go jej rzeczownik.
Ten sam rzeczownik wypuszcza liczbę i rodzaj,
bo z głową grupy zgadza się orzeczenie zdania składowego.
Zaimek wypuszcza tę samą parę drugi raz i osobno,
bo w niej zgadza się z nim poprzednik zdania względnego.
Jedna para na obie zgodności wygląda poprawnie i odwraca każdą z nich:
`w wyniku której` ma głowę męską przy żeńskim poprzedniku,
a `której przepisy obowiązują` mnogą przy pojedynczym.
Para wzięta z zaimka przyjmuje przez to `Ustawa, której przepisy obowiązuje`,
a para wzięta z głowy `Ustawy, której przepisy obowiązują` —
w obie strony werdykt pewny siebie i błędny.

Kształty grupy są dwa: rzeczownik z zaimkiem za sobą (`na podstawie której`)
i ten sam rzeczownik z zaimkiem przed sobą (`o którego zdaniu`).
Każdy jest osobnym ciałem produkcji,
bo cechy nie przechodzą przez grupę imienną same,
więc głowa z przydawką pod sobą wysunięcia nie ma.
Sam zaimek (`o którym`, `która rozstrzyga`) jest obok tych dwóch
czołem drugim, w tych samych dwóch pozycjach.
Czoła są dwa, a nie jedno obejmujące oba kształty,
i rozstrzyga o tym pomiar, a nie polszczyzna.
Cenę każdej z dwóch pozycji bierze się osobno, zdejmując produkcje,
a pod jednym czołem pozycja bez przyimka nie jest żadną produkcją osobno:
te same ciała bierze wtedy sam zaimek, więc nie ma czego zdjąć.
Ile ta grupa kupuje i ile kosztuje w każdej z dwóch pozycji, mierzy
[grupę wysuniętą zmierzono](#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania).

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
a ile ona kupuje i dlaczego nie weszła, mierzy
[design-notes.md](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze).

### Grupę wysuniętą zmierzono: nie kosztuje nic i kupuje pojedyncze zdania

Pełne wiersze są w [figury/wysunięcie.txt](../figury/wysunięcie.txt),
te spod morfologii żywej w [figury/wysunięcie-żywa.txt](../figury/wysunięcie-żywa.txt),
a te nad rejestrem ustaw w [figury/wysunięcie-ustawy.txt](../figury/wysunięcie-ustawy.txt)
oraz w [figury/wysunięcie-ztp.txt](../figury/wysunięcie-ztp.txt);
polecenie i pliki, których zmiana każe je przeliczyć, podaje każda z tych czterech
([`harness/figury.py`](../harness/figury.py)).

Grupy są trzy i zdejmuje się je osobno, bo cena każdej z nich jest osobną liczbą.
Grupa względna z przyimkiem jest rzeczownikiem z zaimkiem w dopełniaczu, w obu szykach,
wysuniętym przed zdanie względne razem z przyimkiem.
Grupa względna bez przyimka jest tą samą grupą w podmiocie i w dopełnieniu
zdania składowego, czyli tam, gdzie przypadka żąda nie przyimek, tylko sama rola.
Grupa pytajna z przyimkiem jest tą samą grupą pytajną,
którą pytanie stawia w podmiocie i w dopełnieniu
([wyżej](#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał)),
tylko wysuniętą razem z przyimkiem, który nią rządzi.
Pytanie żąda przez to własnego czoła, a nie trzeciego kształtu grupy,
i tym różni się od dwóch pozycji względnych,
które ten sam kształt dzielą.

Z dwóch szyków grupy względnej rejestr niesie jeden — zaimek za głową:
`na podstawie której`, `w interesie którego`, `w następstwie którego`,
`na terytorium których`.
Szyku odwrotnego, czyli `o którego zdaniu`, nie ma w nim ani razu:

```sh
grep -ohP '\b(?:na|w|o|z|do|przez|od|dla|pod|nad|przy|po|za|wobec|bez)\s+któr\w+\s+\w+' \
  proza/ztp/*.txt proza/ustawy/*.txt | sort | uniq -c | sort -rn
```

Cztery piąte z 1208 trafień jest zwrotem `o którym mowa`,
gdzie `mowa` jest orzeczeniem zdania względnego, a nie głową grupy pod przyimkiem,
a w pozostałych zaimek zgadza się z przyimkiem i głowy przy sobie nie ma.
Szyk z zaimkiem przed głową jest więc wyczytany z polszczyzny, a nie z korpusu,
tak samo jak pytanie o tę grupę niżej.
Sam ten zwrot jest przy tym najczęstszym zdaniem względnym rejestru ustaw,
a wyprowadzenie daje mu
[kopuła opuszczona](#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną):
pod przyimkiem stoi w nim goły zaimek, bo `mowa` orzeka za całe zdanie składowe.

```text
Rozporządzenie powinno wchodzić w życie w dniu wejścia w życie ustawy, na podstawie
której jest ono wydawane.
W nocy biolodzy z Zakładu Badań Ssaków PAN obserwowali watahę, w której skład
wchodził uwięziony wilk.
Czterech gości, których stan był najcięższy, trafiło do szpitala.
W którym roku ustawa weszła?
```

Cena wyszła zerowa w każdym z trzech korpusów i pod obiema morfologiami banku drzew:
ani jedno zdanie przyjęte wcześniej nie traci jednoznaczności ani wyprowadzenia,
i nie zmienia się ani jeden werdykt poza tymi, które ta konstrukcja kupuje.
Grupy nie spierają się przy tym o ani jedno zdanie,
choć `z którego pliku` spełnia żądanie obu naraz:
zaimek jest tam i dopełniaczem, i zgodny z rzeczownikiem po sobie.
Rozdziela je nie kształt grupy, ale to, co ją bierze —
zdanie względne wisi na grupie imiennej, a pytanie zamyka pytajnik
albo stoi w ramie czasownika — więc zdanie sporne musiałoby dopuszczać
jedno i drugie w tym samym miejscu.
Dwie pozycje względne rozdziela przy tym sam przyimek,
bo grupa albo stoi pod nim, albo nie stoi.

Zera po stronie ceny nikt tu nie przewidział, i przy każdej pozycji z innego powodu.
Grupa pod przyimkiem następuje po nim,
a przyłączenia wyrażenia przyimkowego olski
[nie wybiera](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera),
więc zdanie przyjęte z `o której` mogło od tej grupy dostać drugie czytanie,
w którym rzeczownik za zaimkiem przechodzi na głowę grupy.
Nie dostało go ani jedno, bo grupa żąda dwóch przypadków naraz:
dopełniacza od zaimka i przypadka przyimka od swojej głowy.
`Reguła, o której ustawa mówi, jest tania.` wyprowadza się przez to raz,
bo `ustawa` jest mianownikiem, a `o` mianownika nie rządzi.

Grupa bez przyimka konkuruje z czymś innym, bo staje tam,
gdzie stoi wysunięty sam zaimek: rzeczownik zaraz za zaimkiem
jest raz głową grupy, a raz podmiotem zdania składowego,
i `polszczyzna, której autor nie napisał` czyta się przez to na oba te sposoby.
Oba czytania ma tam także czytelnik, więc jest to cena należna.

Zero po stronie ceny nie znaczy przy tym,
że ta pozycja nie bierze czytań, których polszczyzna nie ma.
Głową grupy wolno tu stanąć zaimkowi rzeczownemu,
a taki zaimek dopełniaczem przy sobie nie rządzi:
`polszczyzna, której nikt nie napisał` dostaje przez to drugie czytanie,
w którym `której nikt` jest grupą.
Kryterium na tę klasę gramatyka ma i stawia je gdzie indziej —
[zaimek rzeczowny nie rządzi dopełniaczem](#zaimek-rzeczowny-nie-rządzi-dopełniaczem) —
a nazywa lematem jeden zaimek, nie klasę,
więc nad tą pozycją nie strzela; [TODO.md](../TODO.md) trzyma jego rozszerzenie.
Żadne zdanie tych korpusów na to nie trafiło,
więc cena tej klasy jest wyczytana z gramatyki, a nie z przebiegu.

Zakup jest drobny i cały należy do dwóch grup względnych.
Grupa bez przyimka kupuje jedyne zdanie, jakie ta konstrukcja przyjmuje:
`Czterech gości, których stan był najcięższy, trafiło do szpitala.`
wychodzi jednym czytaniem pod obiema morfologiami banku drzew,
a obok niego dwa zdania Składnicy i jedno rejestru ustaw
przechodzą z odrzuconych na wieloznaczne.
Grupa z przyimkiem nie kupuje nad Składnicą nic pod złotą morfologią
i jedno zdanie pod żywą,
a nad „Zasadami techniki prawodawczej” dwa,
jednym z nich jest to zdanie o rozporządzeniu wyżej.
Pod złotą morfologią tamto jedno zostaje poza gramatyką jeszcze jedną formą:
`uwięziony` dostało od anotatora sam imiesłów bierny,
a przydawka przed rzeczownikiem przyjmuje przymiotnik i nic poza nim,
bo imiesłów wpuszcza w tej gramatyce `PredicativeAdjective`, i tylko on.

Rejestry odpowiadają przez to na dwie pozycje różnie.
Zdania, które rusza pierwsza, stoją tylko w „Zasadach techniki prawodawczej”,
bo `na podstawie której` jest w nich zwrotem powtarzanym przepis po przepisie;
zdania drugiej tylko w siedmiu ustawach, a bank drzew daje jedne i drugie.
Odczyt jest to o rejestrach, a nie o produkcjach: kształt grupy jest w obu pozycjach ten sam.

Grupa pytajna z przyimkiem nie kupuje ani jednego zdania w żadnym z tych korpusów,
i jest to odczyt o rejestrze, a nie o produkcjach.
Pytań stawia Składnica jedno na piętnaście zdań,
a lemat, na którym ta grupa stoi, otwiera dwa z nich
([figury/pytajne.txt](../figury/pytajne.txt)),
więc pytanie o wyrażenie przyimkowe nie ma tam ani jednego wystąpienia do kupienia.
Konstrukcja ta jest przez to wyczytana z gramatyki, a nie z korpusu:
`W którym roku ustawa weszła?` napisała ta sekcja, a nie prawodawca,
i tyle wolno o tej połowie powiedzieć.

### Czoło niesie etykietę roli, którą zajmuje, a werdyktu nie rusza

Wysunięty konstytuent zajmuje w zdaniu składowym rolę:
`która` w `reguła, która rozstrzyga` jest podmiotem,
a `którą` w `polszczyzna, którą napisał autor` dopełnieniem.
`_wysunięta_rola` w `olski/subset.py` stawia nad nim `Subject` albo `Object`,
czyli tę samą etykietę, którą nosi rola wypełniona na swoim miejscu.

Bez tej etykiety olski wyprowadza te zdania dokładnie tak, jak czyta je bank drzew,
a rozdanie ról wychodzi z nich o jedną rolę uboższe,
więc porównanie ról nie ma go z czym zestawić;
ile zdań na tym stało, liczy
[corpus.md](corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).

Etykieta jest osobnym konstytuentem nad czołem, a nie cechą na nim,
bo rolę czyta się z etykiety węzła (`Node.find` w `olski/parse.py`),
i stąd bierze się trudność tej pozycji.
Symbol wpisany do ciała wpuszcza tam wszystkie swoje produkcje,
a `Subject → NP` wpuszcza w to miejsce każdą grupę imienną w mianowniku:
`reguła, ta reguła rozstrzyga` byłoby wtedy zdaniem względnym,
a `Który aktor robi wrażenie.` zdaniem oznajmującym o takim podmiocie,
czyli wróciłoby czytanie, które zdjął
[warunek na lemat](#zaimek-względny-nie-jest-przymiotnikiem-przy-rzeczowniku).

Rozdziela obie rodziny produkcji cecha `czoło` (`BEZ_CZOŁA` w `olski/subset.py`),
a niosą ją wszystkie produkcje obu symboli,
bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc rodzina milcząca przechodziłaby przez to żądanie za darmo.
Rola na swoim miejscu ogłasza, że czoła nie ma;
rola wysunięta ogłasza nazwę czoła, którym ją wypełniono.
Wartością jest nazwa symbolu, a nie jedno „wysunięte”,
bo czoła są trzy i każde należy do jednej rodziny:
sam zaimek i grupa, w której on stoi, są czołami zdania względnego,
a grupa pytajna czołem pytania.
Wspólna wartość zlałaby te rodziny, więc `ustawa, który przepis obowiązuje`
wychodziłoby zdaniem względnym z grupą pytajną na czole,
a `Który zapisuje ustawienia?` pytaniem o sam zaimek.
Tę samą robotę wykonuje przy `Predicative` cecha `valency`:
rozdziela orzecznik zgodny od narzędnikowego, a kopula żąda drugiego z nich.

Cena wyszła zerowa i wynika z kształtu tej zmiany, a nie z przebiegu.
Etykieta nie zmienia tego, co się wyprowadza, tylko to, jak się nazywa,
więc żaden werdykt ruszyć się nie może;
przebiegi nad bankiem drzew pod obiema morfologiami
oraz nad trzema korpusami prozy wydają to samo, zdanie po zdaniu.
Rusza się w nich sama kolejka blokerów, i o kilka zdań:
bloker mówi, dokąd rozbiór doszedł, a nie co się udało,
więc produkcja dopisana przesuwa go tam, gdzie tablica sięga dalej
(`Outcome.blocker` w `olski/coverage.py`).

Zakup liczy się przez to w innej walucie i widać go w dwóch tabelach porównania ról
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Pod złotą morfologią 34 zdania wieloznaczne przechodzą z `lost` na `survives`,
a 10 zdań przyjętych z `partial` na `agrees`;
`disagrees` nie rośnie o ani jedno.

Tych dwóch liczb nie bierze żadne polecenie i bierze je ręka,
bo sonda różnicowa liczy przejścia werdyktu (`sonda/ruch.py`),
a ta pozycja nie rusza ani jednego.
Wariantem jest gramatyka bez produkcji, które `_wysunięta_rola` pisze nad czołem:
`Subject → czoło` po jednej na czoło, `Object → czoło` po dwóch,
bo tam rozdziela je przeczenie,
a wraz z nimi wychodzi cecha `czoło` z ról, które ją niosą.
`olski-corpus Składnica-frazowa-180723/` puszczony nad taką gramatyką
wydaje obie tabele bez etykiety, a różnica wierszy jest tymi liczbami.
Czego brakuje, żeby wzięło je polecenie, trzyma [TODO.md](../TODO.md).

Grupa pytajna niesie dwie etykiety naraz i obie są potrzebne.
`Interrogative` mówi, o co zdanie pyta,
i bez niej pytanie przyjęte nie mówiłoby tego wcale
(`PYTAJNY` w `olski/subset.py`),
a `Subject` albo `Object` mówi, czym ta grupa w zdaniu jest,
i tego żąda bank drzew, bo grupy pytajnej nie zna
i obsadza `Który aktor` podmiotem.
Streszczenie wypisuje przez to jedną rozpiętość dwa razy,
i tyle ta pozycja kosztuje w wydruku.

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

### Kopuła opuszczona jest wpisem na lemat, a nie pozycją ogólną

Rejestr ustaw odsyła zwrotem `o którym mowa`:
`Rada wykonuje zadania, o których mowa w ustawie.` znaczy `o których jest mowa`,
a `jest` nie pisze tam nikt.
Morfeusz zna formę `mowa` wyłącznie jako `subst:sg:nom:f`,
więc zdanie względne tego zwrotu obywa się bez czasownika,
a zdanie składowe bez czasownika wyprowadza w tej gramatyce sama ta konstrukcja.
Zwrot ten jest najczęstszym zdaniem względnym rejestru ustaw —
niesie go co siódme zdanie dwóch jego korpusów
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)) —
więc konstrukcja ta odpowiada na kolejkę tamtego rejestru,
a nie na kolejkę ze Składnicy.

Wpuszczają ją dwa ciała, a rozdziela je to, skąd bierze się wyrażenie,
o którym ten rzeczownik orzeka.
Kopuła opuszczona takiego wyrażenia żąda, więc `Mowa o zadaniach.` jest polszczyzną,
a `Mowa.` nie jest, i stąd okolicznik stoi w zdaniu składowym córką żądaną,
a nie miejscem, które dokłada
[rozwinięcie szyku](#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk).
Zdanie względne bierze to wyrażenie skądinąd:
`o których` leży poza zdaniem składowym, bo wysuwa je `RelativeModifier`,
więc ciało czoła bierze ten rzeczownik wprost i zdania składowego nie ma pod sobą wcale.
Czoło pytania bierze go tym samym ciałem, więc `O którym akcie mowa?`
wyprowadza się razem z `o których mowa`.

Terminal tego rzeczownika żąda lematu, i to żądanie jest decyzją,
bo polszczyzna opuszcza kopułę szerzej niż w tym jednym zwrocie.
Wyjścia były dwa.
Pozycja ogólna czyni zdaniem składowym każdą grupę imienną w mianowniku,
czyli dopisuje `ClauseConjunct → Subject` obok `ClauseConjunct → Subject Adjuncts`.
Wpis leksykalny kupuje ten jeden zwrot i nic poza nim,
tak samo jak spójnik, którym zaczepia się
[zdanie z `że`](#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej).

Pozycję ogólną zmierzono, dopisując te dwie produkcje do gramatyki
i porównując werdykty z werdyktami olskiego.
Nad siedmioma ustawami wyciąga ona z odrzucenia 231 zdań,
116 z nich przyjmuje jednoznacznie,
a jednoznaczność odbiera siedmiu zdaniom przyjętym wcześniej;
nad „Zasadami techniki prawodawczej” i nad prozą tego repozytorium
odbiera ją po jednym zdaniu.
Zakup nie jest jednak zakupem, i widać to po tym, co ona przyjmuje:

```text
Wrocław.
Siedziba Okręgowej Komisji Wyborczej: LEGNICA.
```

Nazwa miasta stoi w akcie w tabeli, a nie w zdaniu,
i olski melduje o niej `valid`.
Reszta zakupu jest tą samą usterką w środku zdania,
bo przecinek i spójnik koordynują u olskiego zdania:
`Kierownikiem urzędu jest wójt lub burmistrz.` wychodzi wtedy dwoma zdaniami
składowymi, z których drugim jest `burmistrz`,
a `Statut związku powinien określać uczestników i czas trwania związku.`
dostaje drugie czytanie, w którym zdaniem składowym jest `czas trwania związku`.
Drugie z tych zdań jest jednym z siedmiu, którym ta pozycja odbiera jednoznaczność,
a dwa dalsze — `Przemyśl.` i `Kalisz.` — olski przyjmuje jako rozkaźnik
i pozycja ogólna daje im drugie czytanie, w którym są nazwą miasta.
Cena tej pozycji nie kończy się więc na tych siedmiu zdaniach:
psuje ona każdy ciąg współrzędny grup imiennych,
a takich ciągów ten rejestr niesie zdanie po zdaniu.

Rzeczownik orzekający niesie etykietę roli, bo zdanie to nie ma żadnej innej:
ani podmiotu, ani czasownika.
Przyjęte bez etykiety wychodziłoby `valid` bez ani jednej roli,
czyli bez słowa o tym, co olski w nim przyjął,
a etykietę stawia produkcja, tak samo jak przy
[czole zdania względnego](#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza).

```text
$ olski-check -c 'Mowa o zadaniach.' --readings
<text>: valid     Mowa o zadaniach.
                  one reading
                  - NominalPredicate: Mowa, Modifier: o zadaniach → Mowa
```

Rola ta stoi obok `Predicative`, a nie jest nim, i rozdziela je rama czasownika.
Orzecznik jest pozycją ramy: rzeczownikowy stoi w narzędniku pod kopulą,
a przymiotnikowy w mianowniku pod czasownikiem, którego rama go ma.
Rzeczownik orzekający nie ma nad sobą czasownika, więc pozycji ramy nie zajmuje,
a wpuszczony do `Predicative` stanąłby tam, gdzie orzecznik ramy nie ogłasza:
w szyku z orzecznikiem przed kopulą (`olski/subset.py`).
Przyjąłby wtedy `Mowa jest ustawa.`, czyli zdanie,
w którym olski czyta rzeczownikowy orzecznik w mianowniku.

Oba ciała są przy tym potrzebne, i rozstrzyga o tym przyłączenie:
`w ustawie` dochodzi w `Rada wykonuje zadania, o których mowa w ustawie.`
i do `mowa`, i do `wykonuje`, a pierwsze z tych czytań daje ciało zdania składowego,
drugie ciało czoła.
Zdjęte jedno z nich nie odrzuca tego zdania — drugie wyprowadza je samo —
tylko oddaje je jednym czytaniem,
czyli tak, jak wygląda zdanie, o którym gramatyka wybrała przyłączenie
([niżej](#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).
Wieloznaczność tego zdania jest więc tym przyłączeniem,
a nie czymkolwiek, co wnosi kopuła opuszczona.

### Kopułę opuszczoną zmierzono: nie kosztuje nic i kupuje mniej, niż obiecywała jej częstość

Pełne wiersze są w [figury/kopuła.txt](../figury/kopuła.txt),
te spod morfologii żywej w [figury/kopuła-żywa.txt](../figury/kopuła-żywa.txt),
a te nad rejestrem ustaw w [figury/kopuła-ustawy.txt](../figury/kopuła-ustawy.txt)
oraz w [figury/kopuła-ztp.txt](../figury/kopuła-ztp.txt);
polecenie i pliki, których zmiana każe je przeliczyć, podaje każda z tych czterech
([`harness/figury.py`](../harness/figury.py)).

Grupy są dwie i zdejmuje się je osobno, bo cena każdej z nich jest osobną liczbą.
`rzeczownik pod czołem` jest ciałem czoła, w którym wysunięte wyrażenie przyimkowe
bierze ten rzeczownik wprost,
a `rzeczownik z okolicznikiem` zdaniem składowym, w którym rzeczownik
bierze okolicznik sam.

Cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew:
ani jedno zdanie przyjęte wcześniej nie traci jednoznaczności ani wyprowadzenia.
Zera tego nikt tu nie przewidział, bo rzeczownik w mianowniku jest w każdym innym
miejscu tej gramatyki podmiotem albo orzecznikiem.
Broni go warunek na jedną formę: drugie czytanie dostaje wyłącznie zdanie,
w którym `mowa` stoi, a poza tym zwrotem te korpusy piszą ją razem z jej kopułą:

```sh
grep -hoP '.{40}\bmowa\b' proza/ustawy.txt proza/ztp.txt proza/README.txt \
  | grep -vP 'o (którym|której|których) mowa'
```

`ilekroć w niniejszej ustawie jest mowa o` oraz `o kim mowa była przed chwilą`
niosą czasownik wypisany, więc zdanie składowe bez niego nie ma tam czym stanąć.

Zakupem jest jedno zdanie i całe leży w rejestrze ustaw:

```text
Termin rozpatrzenia petycji wielokrotnej liczy się od dnia upływu okresu, o którym
mowa w zdaniu poprzednim.
```

Przechodzi ono z odrzuconych na wieloznaczne, a oba ciała ruszają je osobno,
bo `w zdaniu poprzednim` przyłącza się i do `mowa`, i wyżej.
Nad Składnicą nie rusza się ani jeden werdykt pod żadną z dwóch morfologii,
a nad „Zasadami techniki prawodawczej” i nad prozą tego repozytorium
nie rusza się także ani jeden.

Jedno zdanie wobec 851 wystąpień zwrotu jest odczytem o rejestrze,
a nie o tej konstrukcji.
Zwrot ten odsyła, więc prawodawca pisze go razem z adresem przepisu:

```sh
grep -hoP 'o (którym|której|których) mowa[^,.;]{0,30}' proza/ustawy.txt proza/ztp.txt \
  | sed 's/[0-9][0-9]*/N/g' | sort | uniq -c | sort -rn | head
grep -hcP 'o (którym|której|których) mowa(?![^,.;]*(art|ust|pkt|lit|§|[0-9]))' \
  proza/ustawy.txt proza/ztp.txt
```

Bez cyfry, bez znaku `§` i bez skrótu `art.`, `ust.`, `pkt` albo `lit.`
obywa się dwanaście z tych wystąpień, wszystkie w siedmiu ustawach,
a [cyfry olski nie bierze](#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii).
Aparat odsyłaczowy zajmuje w kolejce blokerów tego rejestru dziewięć pierwszych miejsc
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
więc zdanie z tym zwrotem staje na nim, a nie na kopuli.
Częstość zwrotu obiecała tu przeszło dwa rzędy wielkości więcej, niż on kupił,
i myli się przez to tak samo jak tamta kolejka, choć powstała inaczej:
konstrukcję znalazł grep, a nie ranking form bez licencji,
bo każda forma tego zwrotu licencję ma.

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

Pełne wiersze są w [figury/liczebnik.txt](../figury/liczebnik.txt),
a polecenie i pliki, których zmiana każe je przeliczyć, podaje ta figura
([`harness/figury.py`](../harness/figury.py)).
Mianownik jest w niej ten sam, co w tabelach [corpus.md](corpus.md#the-measurement):
13 035 lasów Składnicy z pełnym drzewem, morfologia złota,
i wchodzą do niego wszystkie, bez granicy na długość zdania.

Ani jedno zdanie nie przechodzi z przyjętego na wieloznaczne.
Blisko sto przechodzi z odrzuconych na przyjęte
i przeszło dwie trzecie tylu z odrzuconych na wieloznaczne,
czyli cała cena jest zapłacona zdaniami,
których gramatyka bez liczebnika nie wyprowadzała wcale.
Zakup dzieli się między ciała prawie po połowie
i żadne zdanie nie rusza się pod obydwoma,
więc te dwa zbiory są rozłączne.
Dwa zdania zostają poza nimi i wymagają obu ciał naraz,
tak samo jak dwa spośród wieloznacznych,
bo mają dwie grupy liczebnikowe i każda z nich przyłącza się inaczej:

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

Role zdań nowo przyjętych zgadzają się z drzewem wzorcowym w czterech piątych,
kilkunastu bank drzew nie daje roli do porównania albo daje ją tylko częściowo,
a niezgodne są cztery i żadne z nich nie jest wyborem, którego olski dokonał.
`W Hongkongu zmarły cztery osoby zarażone wirusem ptasiej grypy.`
czyta imiesłów jako orzecznik, gdzie bank drzew ma go w przydawce przy `osoby`,
i jest to [przydawka imiesłowowa](#what-it-does-not-cover-yet), której olski nie ma;
liczebnik tylko doprowadził analizę do miejsca, w którym ten brak widać.
`Od dwu tygodni nie mam od ciebie listu!` jest rozbieżnością zasięgu,
którą [corpus.md](corpus.md#agreement-which-matters-more-than-acceptance) liczy
razem z trzema takimi samymi: złote poddrzewo bierze w siebie wyrażenie
przyimkowe, które olski wiesza na zdaniu.
`Mieszkańcy miasta mówią, że od 20 lat rzeka nie miała tak wysokiego poziomu.`
przyszło tu razem z przysłówkiem i jest rozbieżnością tego samego rodzaju:
złote dopełnienie obejmuje `tak wysokiego poziomu`, a olski zostawia `tak` zdaniu,
bo przysłówek bez stopnia do przymiotnika nie dochodzi
([niżej](#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)).
`Marzec przyniósł 6 zagranicznych delegacji.` olski czyta tak,
jak przeczytałby je czytelnik, a niezgodność jest po stronie porównania:
bank drzew daje grupie liczebnikowej w pozycji dopełnienia własne gniazdo, `np(part)`,
którego `_role` w `olski/corpus.py` nie tłumaczy na żadną rolę olskiego,
więc drzewo wzorcowe nie ma tam dopełnienia, z którym można by się zgodzić.
[TODO.md](../TODO.md) trzyma to jako usterkę porównania.

Nad rejestrem, o który olskiemu chodzi, liczebnik kupuje jedno zdanie.
`Działają dwie rzeczy.` przechodzi z odrzucenia w jedno czytanie,
i jest to zdanie, o którym [corpus.md](corpus.md#where-the-analyses-stop) mówiło,
że czeka na liczebnik i na nic więcej.
Ciało zgodne kupuje je samo, ciało rządzące nad tą prozą nie rusza nic,
a wieloznacznych nie przybywa ani jedno.
Nad rejestrem ustaw wychodzi odwrotnie:
dwa zdania przyjęte i siedem wieloznacznych z 4921
([ustawy.md](ustawy.md#co-gramatyka-z-tego-wyprowadza)),
czyli tam przeważa cena, a nie zakup,
i powód jest ten sam, który zamyka tę sekcję: ustawa liczy cyframi.

### Cyfry olski nie bierze, bo cyfra nie niesie morfologii

Rejestr, o który olskiemu chodzi, pisze liczebnik cyfrą:
`w terminie 14 dni`, `3 szkół`, `15 członków`.
Morfeusz daje cyfrze tag `dig` i ani jednej cechy,
a cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc obie produkcje biorą cyfrę naraz.
Odrzucić ją umie żądanie obecności cechy
([design-notes.md](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)),
tyle że odrzuca wtedy każdą cyfrę i wpuszczenia nie kupuje.
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

- A colon opening an enumeration, which is the second construction behind that
  character: `Tory są dwa: gramatyka i skład.` is rejected
  where `Cena jest niska: gramatyka jest bezkontekstowa.` derives
  ([above](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
  What separates the two is not the sign but what stands after it.
  An explanatory clause needs no relation to anything inside the clause before it,
  the way a coordinated clause needs none,
  while an enumeration is an apposition to something in that clause —
  to `dwa` here — and a production at the sentence level has no way of saying to what.
- A semicolon joining two clauses.
  `Program zapisuje ustawienia; linter sprawdza tekst.` is rejected
  where the same two clauses joined by a colon derive,
  so what olski has of clause-level punctuation
  is now the comma, the colon and nothing else.
  The semicolon is the cheapest entry on this list to admit
  and the hardest to argue for:
  Polish puts it where either a comma or a full stop would also stand,
  so the production would say nothing the colon's does not.
- Przysłówek przed drugim przysłówkiem, czyli trzeci gospodarz tej konstrukcji:
  `Program zapisuje ustawienia bardzo szybko.` nie jest odrzucone i to jest z nim
  gorzej, bo wychodzi jednym czytaniem, w którym `bardzo` określa zdanie
  ([niżej](#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę)).
  Stoi tu, bo jest to jedyna pozycja przysłówka, której olski nie ma,
  a nie jest to zdanie odrzucone, które być nim nie powinno.
- A conjunction opening a sentence, which is what leads the `conj` row
  [corpus.md](corpus.md#where-the-analyses-stop) ranks:
  `I nikt tego nie zauważył.` is rejected
  where the same conjunction between two clauses derives.
  Every one of the three forms leading that row is capitalized,
  and that is the whole of what is left of the row for this construction:
  the comma in front of a conjunction took the lowercase ones
  ([above](#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego)).
- The subordinators the conditional stands under: `aby`, `żeby`, `by`, `gdyby`.
  A clause with one of them has its verb in the past tense and the particle `by`
  fused into the subordinator or standing beside it,
  which no production takes,
  so the [adverbial clause](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)
  leaves them out rather than deriving `aby program zapisuje ustawienia`.
  They come back with the particle and not before it,
  and two of them stand second and third in the `comp` row
  [corpus.md](corpus.md#where-the-analyses-stop) ranks, behind `że` itself.
- Słowa, którymi ten rejestr pyta poza tym jednym zaimkiem:
  `czy`, `kto`, `co`, `jak`, `dlaczego`, `gdzie`.
  `Czy program zapisuje ustawienia?` jest odrzucone,
  gdzie `Który program zapisuje ustawienia?` wyprowadza się,
  a każde z tych słów żąda innego kształtu niż grupa pytajna,
  więc jest to kolejka konstrukcji, a nie jedna pozycja;
  waży ją [pytanie zmierzono](#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał).
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
  Wiersz `ppas` liczy w kolejce blokerów 300 zdań
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
  [pozostałych szykach](#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka)
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
- wewnątrz zdania względnego, wokół tego, co w nim zostało:
  po zaimku, między podmiotem a czasownikiem i na końcu
  (`reguła, która w tym trybie rozstrzyga`,
  `polszczyzna, którą ktoś w tym trybie napisał`)
- wewnątrz pytania, w tych samych trzech miejscach za grupą pytajną
  (`Który program w tym trybie zapisuje ustawienia?`)

Wierszy jest dziewięć, a produkcji sześćdziesiąt jeden,
bo pozycja powtarza się w każdym szyku, który ją ma,
a szyk jest w tej gramatyce osobną produkcją.
Dziesięć z tych sześćdziesięciu jeden dołożyły cztery szyki dopisane,
i tyle właśnie znaczy w tej gramatyce jeden szyk więcej;
jedna jest z przysłówka, bo lista okoliczników bierze go tak samo
jak wyrażenie przyimkowe
([niżej](#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)),
a czternaście z pytania: jedenaście wewnątrz jego czoła
i trzy w orzeczeniu, które bierze pytanie zależne
([wyżej](#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał)).
Cztery dołożyło [rozwinięcie szyku](#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk),
po dwa w zdaniu względnym i w pytaniu,
i jest to jedna pozycja w dwóch konstrukcjach z listy wyżej,
którą gramatyka pisana ręką miała w dwóch ciałach z trzech.
Liczy się je tak, jak się je zdejmuje, a granica biegnie tak.
Wchodzi produkcja, w której `Adjuncts` stoi obok czegoś jeszcze,
w tym obok drugiego okolicznika,
oraz ta, w której `Modifier` dochodzi do głowy mającej już przydawkę
albo do imiesłowu, czyli `APConjunct → adj|ppas Modifier`.
Nie wchodzi `NPConjunct → subst Modifier`, czyli naga głowa z okolicznikiem:
jest to sama grupa imienna z wyrażeniem przyimkowym,
a nie drugie miejsce, w którym to wyrażenie się mieści.
Nie wchodzi z tego samego powodu `ClauseConjunct → NominalPredicate Adjuncts`,
czyli [kopuła opuszczona](#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną)
z okolicznikiem: rzeczownik orzekający grupą imienną nie jest,
więc temu wyrażeniu nie ma tam do czego dojść poza zdaniem składowym.
Granica jest wypisana dlatego, że liczba nad nią jest zapisana w dwóch dokumentach,
a policzyć ją drugi raz można tylko wtedy, gdy wiadomo, co się liczy.
Rusza tę liczbę każda produkcja dająca modyfikatorowi pozycję,
a policzenie jej na nowo jest odliczeniem ręką według granicy wyżej,
bo żaden przebieg jej nie drukuje i nie ma jej w `FIGURY` w `harness/figury.py`.

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
gramatyka bez pozycji przy grupie imiennej i przymiotnikowej
czyta wbrew ręcznemu rozbiorowi ponad dwieście zdań,
a z nimi dwadzieścia kilka, i żadne z nich nie jest przyłączeniem, które olski wybrał.
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

## Przysłówek wchodzi obu gospodarzami, bo drugi zdejmuje czytania nieprawdziwe

Wyrażenie przyimkowe ma dwóch gospodarzy i oba czytania są prawdziwe,
więc olski oddaje je czytelnikowi.
Przysłówek ma dwóch gospodarzy, a nad jednym zdaniem prawdziwy jest jeden z nich:
`bardzo` w `Plik jest bardzo duży.` określa przymiotnik i zdania nie określa,
a `tu` w `Mam tu odmienną interpretację.` określa zdanie i przymiotnika nie określa.
Wybór między gospodarzami jest więc rozstrzygnięciem,
a nie wieloznacznością do zgłoszenia,
i dlatego sonda wyceniła każdego z nich osobno, zanim któryś wszedł do gramatyki.

Weszli obaj: drugi gospodarz kosztuje zdania, a kupuje prawdę o drzewie,
i po tym kursie olski go przyjmuje.

Pełne wiersze są w [figury/przysłówek.txt](../figury/przysłówek.txt),
a polecenie i pliki, których zmiana każe je przeliczyć,
podaje ta figura ([`harness/figury.py`](../harness/figury.py)).

Gospodarze są dwaj, więc wariantów jest cztery:
gramatyka bez przysłówka, po jednym na gospodarza i sam olski, w którym stoją obaj.
`okolicznik` wpuszcza przysłówek do listy okoliczników,
czyli tam, gdzie stoi wyrażenie przyimkowe, i przed zdanie.
`przy przymiotniku` stawia go pod symbolem przymiotnika,
a bierze tam sam przysłówek stopniowany
([niżej](#naprawę-niesie-tagset-a-formalizm-ją-bierze)).

Okolicznik kupuje nad Składnicą kilkaset zdań,
czyli podnosi liczbę przyjętych o ponad jedną trzecią,
a określenie przymiotnika kilkanaście razy mniej.
Obaj razem kupują mniej niż okolicznik sam,
więc drugi gospodarz dopisany do pierwszego nie kupuje nic i odbiera mu zdania.
[Krzywa pokrycia](design-notes.md#making-the-trade-measurable)
przewidziała, że dopisanie bywa droższe od tego, co kupuje,
i jest to najciaśniejszy przypadek, jaki się tu trafił:
odbierają sobie zdania dwie połowy jednej konstrukcji,
a nie dwie konstrukcje z osobna.

Cena nie jest przy tym stratą na zdaniach, które olski przyjmował przed przysłówkiem:
jednoznaczności nie traci ani jedno z nich, w żadnym z trzech wariantów.
Płaci się ją zakupem pierwszego gospodarza:
zdanie, które każdy z nich osobno przyjmuje jednym czytaniem,
przy obu naraz wychodzi dwoma.

```text
Program zabawy był ściśle ustalony.
```

Pod `okolicznik` orzecznikiem jest `ustalony`, pod `przy przymiotniku`
`ściśle ustalony`, a pod olskim te dwa czytania stoją obok siebie.

Zakupem drugiego gospodarza jest prawda o zdaniach, które zostają.
Pierwszy gospodarz sam wypuszcza jedno na czterdzieści zdań przyjętych
z czytaniem, w którym przysłówek jest okolicznikiem zdania,
choć stoi przed przymiotnikiem i ten przymiotnik określa;
przy obu gospodarzach takich czytań jest jedno na sto pięćdziesiąt
i ani jedno z nich nie pada przed przymiotnikiem
([niżej](#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę)).
Zdanie przyjęte z takim drzewem jest droższe od wieloznacznego,
bo `valid` ktoś przeczyta
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
więc para gospodarzy zamienia werdykt fałszywy na werdykt o dwóch czytaniach.
Kurs wychodzi przez to bliski jednemu do jednego:
zdań przyjętych ubywa mniej więcej tyle, ile ubywa czytań nieprawdziwych.

W tę samą stronę idzie zgodność z drzewem wzorcowym.
Okolicznik sam czyta wbrew niemu jedno zdanie na trzydzieści z tych, które kupuje,
a obaj gospodarze jedno na pięćdziesiąt,
więc pomyłek jest po dopisaniu drugiego mniej nie tylko w udziale, ale i w liczbie,
choć zdań przyjętych jest mniej.
Drugi gospodarz sam myli się przy tym najczęściej z trzech wariantów,
bo czyta wbrew drzewu jedno zdanie na dziesięć z tych, które kupuje sam:
zostają mu pomyłki na przysłówku odprzymiotnikowym,
który określa i zdanie, więc stopień nie rozdziela niczego —
`Oficjalnie cały Sejm RP śpi.` wychodzi z podmiotem `Oficjalnie cały Sejm RP`.
Ról odwróconych nie ma ani jednej, w żadnym wariancie.

Werdykt nazywa tę parę wprost, bo okolicznik przysłówkowy jest w nim rolą:

```sh
python3 -m olski.check --readings -c "Plik jest bardzo duży."
```

```text
<text>: ambiguous Plik jest bardzo duży.
                  2 readings, differing in Adverb, Predicative
                  - Subject: Plik, Predicative: bardzo duży, Verb: jest
                  - Subject: Plik, Predicative: duży, Verb: jest, Adverb: bardzo
0 of 1 sentences are olski
```

Rolę niesie jeden z dwóch gospodarzy, i jest to decyzja, a nie przeoczenie.
Przysłówek określający przymiotnik stoi wewnątrz orzecznika albo przydawki,
więc widać go w wypełnieniu tamtej roli,
a wypisany drugi raz obok mówiłby o zdaniu, że ma okolicznik, którego ono nie ma.
Dwa czytania rozdziela przez to sama lista ról,
zamiast czekać na to, że czytelnik porówna dwa napisy orzecznika.

Nad rejestrem ustaw okolicznik kupuje w skali dziesięć razy mniejszej,
a drugi gospodarz dokłada tam zdanie, zamiast odejmować
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
więc znak tej ceny zależy od rejestru,
a nie od samej pary gospodarzy.

Nad [README](../README.md) przysłówek nie kupuje ani jednego zdania,
a przenosi na wieloznaczne te, które na nim stały.
Jednym z nich jest to, o którym kolejka blokerów mówiła,
że stoi na przysłówku i na niczym więcej
([corpus.md](corpus.md#where-the-analyses-stop)):

```text
Po to ta czarna lista tu stała i cały wywód za nią dalej stoi.
```

Wyprowadzenie dostaje, jednoznaczności nie,
bo w czytaniu, które przysłówek mu daje, `za nią` ma dwóch gospodarzy.
Kolejka mówi więc, gdzie analiza stanęła, i nie mówi, co dopisanie kupi,
także wtedy, gdy zdanie stoi na jednej klasie.

Jedna klasa czytań przyszła razem z tą konstrukcją i nie jest przyłączeniem.
Morfeusz daje czytanie przysłówkowe formom, które ten rejestr pisze
jako przyimek albo spójnik — `wobec`, `gdy`, `jak` —
a okolicznik zdania bierze całą część mowy,
więc `Są oni obdarzeni rozumem i sumieniem i powinni postępować wobec innych
w duchu braterstwa.` ma trzy czytania z `wobec` w roli okolicznika,
w których `innych` jest dopełnieniem,
a `Program zapisuje ustawienia, gdy linter sprawdza tekst.` wyprowadza się
jako dwa zdania spięte przecinkiem, choć zdanie po przecinku jest podrzędne.
Jest to [czytanie, którego polszczyzna nie ma](#the-dictionary-offers-readings-polish-does-not),
a `admissible` po nie nie sięga, bo pyta o czytanie rzeczownikowe.
Kryterium na tę klasę nie jest przy tym oczywiste:
`blisko` i `jak` niosą czytanie przysłówkowe, którego polszczyzna używa,
więc warunek odsiewający przysłówek przy czytaniu przyimkowym zabrałby i je.
[TODO.md](../TODO.md) trzyma ruch wraz z ceną obu kryteriów, które mu się nasuwają.

### Naprawę niesie tagset, a formalizm ją bierze

Gospodarze spierają się o zdanie tylko wtedy,
gdy przysłówek stojący przed przymiotnikiem mógłby określać zdanie,
a Morfeusz tę różnicę niesie:
`tu`, `razem`, `dziś`, `teraz` i `nigdy` wychodzą jako `adv` bez stopnia,
a `bardzo`, `ściśle` i `szybko` jako `adv:pos`.
Stopień ma przysłówek odprzymiotnikowy, a pierwotny go nie ma,
i tylko pierwszy z tych dwóch określa przymiotnik.

Formalizm ma na to warunek i jest nim `niesie`:
`word("adv", niesie="degree")` bierze `bardzo`, a `tu` nie.
Wypisanie wszystkich wartości cechy tego nie mówi,
bo `word("adv", degree="pos.com.sup")` bierze `tu` tak samo jak `bardzo`.
Dlaczego warunek nie mieszka w unifikacji i co jeszcze jest obok niej,
wywodzi [kanał cech](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne).

Naprawa jest z góry niepełna i taka wypadła.
Warunek oddaje pierwszemu gospodarzowi niespełna piątą część zdań,
które drugi mu bez niego odbiera,
a resztę drugi gospodarz odbiera nadal:
o te zdania spierają się przysłówki stopniowane i żadna cecha ich nie rozdziela.
Zmienia natomiast to, ile drugi gospodarz kupuje i jak często się myli:
kupuje o dwie piąte mniej zdań i myli się na nich trzy razy rzadziej,
bo dwie trzecie jego pomyłek pada bez niego na przysłówku bez stopnia.
Te trzy liczby wzięto nad gramatyką, w której przysłówka jeszcze nie było,
i żaden przebieg ich dziś nie powtarza:
wariant bez tego warunku nie jest grupą produkcji, tylko innym terminalem w tej samej,
więc sonda różnicowa nie ma go czym zdjąć,
a gramatyki wariantu branej funkcją żąda od tej maszynerii [TODO.md](../TODO.md).
Są przez to ceną, przy której warunek zapadł, a nie figurą o dzisiejszej gramatyce.

### Płaska lista okoliczników mówi o zdaniu nieprawdę

Pierwszy gospodarz nie jest darmowy, bo lista okoliczników jest płaska.
`Program zapisuje ustawienia bardzo szybko.` wychodzi jednym czytaniem,
a jego kształtem jest `Adjuncts(bardzo Adjuncts(szybko))`,
czyli dwa okoliczniki zdania obok siebie,
gdzie `bardzo` określa `szybko` i zdania nie określa wcale.
Streszczenie nazywa przy tym pierwszy z nich,
bo rola przysłówka nazywa okolicznik pierwszy tak samo jak rola przyłączana,
więc drugi widać dopiero w napisie zdania.
Zdanie przyjęte z takim drzewem jest droższe od wieloznacznego,
bo `valid` ktoś przeczyta
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
a instrument, który liczy zgodność nad bankiem drzew, tego nie widzi:
porównuje podmiot i dopełnienie, a nie miejsce okolicznika.

Liczy to osobna sonda, bo pyta o co innego niż figura wyżej:
tamta o werdykt, a ta o drzewo, którym werdykt wypadł.
Pełne wiersze są w [figury/płaski.txt](../figury/płaski.txt),
a przed dopisaniem drugiego gospodarza w
[figury/płaski-okolicznik.txt](../figury/płaski-okolicznik.txt).
Populacją są zdania przyjęte jednym czytaniem,
bo tam odpowiedź jest dokładna, a listę czytań zdania wieloznacznego
ucina granica wyliczania.

Klasy są dwie i różni je to, czy brakującą pozycję ma drugi gospodarz.
Przysłówek stopniowany przed przymiotnikiem dochodzi do niego,
a przed drugim przysłówkiem nie dochodzi do nikogo.
Pierwsza klasa jest w olskim pusta, i to jest zakup drugiego gospodarza
wypisany osobno: przy nim samym pierwszym gospodarzu przypada na nią
trzy czwarte płaskich czytań.
Zostaje klasa druga, czyli jedno płaskie czytanie na sto pięćdziesiąt zdań
przyjętych, i wszystkie są przysłówkiem przed przysłówkiem, jak `bardzo szybko`.
Trzeci gospodarz jest tym, co ją zdejmuje, i jest on ruchem, a nie dziurą:
[TODO.md](../TODO.md) trzyma pytanie, czy wraca on z tą samą ceną co drugi.

Liczba jest przy tym górnym oszacowaniem,
bo przysłówek stopniowany bywa okolicznikiem zdania
i stoi wtedy przed przymiotnikiem, którego nie określa,
jak w `Ostatecznie nowa ustawa wchodzi w życie.`
Które formy to wywołują, wypisuje każda z tych figur, i prowadzi w nich `bardzo`.
Oszacowanie sięga teraz i przysłówka na czele zdania,
bo pod symbolem przysłówka stoi każdy okolicznik przysłówkowy,
a czoło zdania jest osobnym ciałem produkcji:
`Oficjalnie cały Sejm RP śpi.` liczy się przez to razem z resztą,
i to jest jedna z rzeczy, o które ta figura urosła.
Nad rejestrem ustaw ani jedno zdanie przyjęte płaskiego czytania nie dostaje
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
więc konstrukcja jest tu droga w rejestrze,
który olskiemu ustawia kolejkę, a nie w tym, o który mu chodzi.

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
