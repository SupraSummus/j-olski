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

## Odrzucenie mówi, dokąd analiza doszła, a nie gdzie stoi usterka

Odrzucenie ma trzy przyczyny i werdykt rozdziela je trzema zdaniami,
bo za każdą stoi inna robota do zrobienia.
Pierwszą jest forma, po którą nie sięga ani jedna produkcja,
i tę werdykt nazywa wprost, bo widać ją przed rozbiorem;
[Świgra](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)
trzyma ją osobno tak samo.
Dwie pozostałe są strukturą,
a rozdziela je to, dokąd doszła analiza częściowa
(`Las.najdalszy` w `olski/parse.py`).

Analiza staje wewnątrz zdania, przed formą, której nie wzięła żadna analiza częściowa.

```sh
python3 -m olski.check -c "Tory są dwa: gramatyka i skład."
```

Werdykt nazywa tam dwukropek,
czyli szew, którym to zdanie wychodzi poza podzbiór.
Albo analiza bierze każdą formę zdania i nie domyka całości:
`Gramatyka jest tania, a nie droga.` dochodzi do kropki,
bo drugi człon nie ma czasownika,
i werdykt mówi wtedy, że zdania nic nie zamyka.
Znak kończący nazwany jako zatrzymanie kazałby autorowi poprawić kropkę,
więc te dwa zdarzenia dostają dwa zdania.
Zatrzymanie wewnątrz zdania jest z tych dwóch częstsze:
nad prozą tych dokumentów pada tak przeszło osiem odrzuceń na dziesięć,
a kolejkę form, na których staje, drukuje sam werdykt.

```sh
python3 -m harness.markdown docs/ --into proza/
python3 -m olski.check proza/*.txt | grep -oP 'stops at „\K[^”]+' | sort | uniq -c | sort -rn
```

Kolejka ta stawia na czele `i`, `a`, `więc`, przecinek, dwukropek i `czyli`,
czyli spójnik i znak, którym zdanie tego rejestru dokłada człon.
Jest to inna kolejka niż ta ze Składnicy,
która rankinguje część mowy, a nie formę
([corpus.md](corpus.md#where-the-analyses-stop)).
Ściągać do niej nie ma czego, więc puszcza ją każda sesja.

Nazwane miejsce jest końcem najdłuższego przedrostka, który się analizuje,
i nie jest wskazaniem usterki.
Widać tę różnicę na zdaniu, którym [README](../README.md#co-działa) pokazuje odrzucenie:
`Nowa program zapisuje ustawienia.` staje na `ustawienia`,
choć niezgodna para stoi na czele zdania.
Przedrostek ten analizuje się swobodnym szykiem:
`Nowa` jest mianownikiem, a `program` biernikiem,
więc `Nowa program zapisuje` przechodzi jako podmiot, dopełnienie i orzeczenie
w tej właśnie kolejności, a `ustawienia` nie ma już czym być.
Werdykt mówi o analizie prawdę, a wskazania usterki nie obiecuje.

Czego gramatyka w tym miejscu oczekiwała, werdykt nie podaje,
i nie podaje dlatego, że na formę nie czeka tam nic.
Analiza częściowa, która na formę czeka i tę formę bierze,
przesuwa zatrzymanie za nią,
więc przejście po `_przed_formą` w `olski/parse.py` oddaje w miejscu zatrzymania
zbiór pusty nad każdym zdaniem tej prozy odrzuconym na strukturze.
Wydruk oczekiwań milczałby zatem dokładnie tam, gdzie autor jest zgubiony.

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

## Forma przyimkowa zaimka żąda przyimka przed sobą

Wykluczenie wyżej pyta o samą formę,
a jedna klasa czytań, których polszczyzna nie ma, żąda pytania o sąsiada.

Morfeusz czyta `nie` jako biernik zaimka `on`,
a `niego` wyłącznie jako dopełniacz i biernik tegoż,
i polszczyzna stawia te formy jedynie po przyimku: `na nie`, `bez niego`.
Tagset mówi to sam.
Cecha `post_prepositionality` ma wartość `praep` przy formie stojącej po przyimku
i `npraep` przy tej, która stoi bez niego,
a `nim` niesie obie naraz, tak samo jak `niej` i `nich` w miejscowniku,
bo te formy stoją i pod przyimkiem, i bez niego.

Grupa imienna bierze zaimek w każdej swojej pozycji,
więc bez warunku na tę cechę `Cena niego rośnie.` się wyprowadza,
a `nie` staje dopełnieniem w zdaniu, które przeczy:
`Zagłębie nie płaci.` wychodzi wtedy dwoma czytaniami, gdzie polszczyzna ma jedno.
Bywa i tak, że takie czytanie zostaje jedynym.
Jedno czytanie zdania przeczytanego na opak jest werdyktem najgorszym,
jaki ten pomiar wydaje
([corpus.md](corpus.md#what-morphological-ambiguity-costs)),
bo `valid` czytelnik przyjmuje bez sprawdzania.

Warunek stoi przez to w warstwie morfologicznej i przed rozbiorem,
a nie na terminalu zaimka.
`po_przyimku` w `olski/subset.py` pyta graf segmentacji:
czytanie o samym `praep` zostaje tam,
gdzie w węźle otwierającym tę krawędź kończy się krawędź z czytaniem przyimkowym,
a poza tym schodzi.

Licencji udziela przy tym przyimek, który ta gramatyka bierze,
a nie każda forma z czytaniem przyimkowym,
więc wykluczenie rozdzielającego `a` stoi i tutaj, nie tylko na terminalu
([niżej](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)).
Bez tego warunku `Cena jest niska, a nie.` się wyprowadza:
Morfeusz czyta `a` jako przyimek, więc licencjonuje `nie` stojące za nim,
a wyrażenia przyimkowego z tego `a` nie ma jak zbudować,
czyli licencji udzielała pozycja, której nikt nie zajmuje.
Zdanie po zdaniu widać to dopiero razem z członem bez czasownika
([wyżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)),
bo dopiero on daje `, a` cokolwiek za sobą.
Kosztuje ten warunek pojedyncze zdania tej prozy i oba czytania, które zdjął,
były nieprawdziwe: `a nie` wychodziło w nich spójnikiem i zaimkiem
w zdaniu, którego dalsza część potyka się o co innego.

Dwie drogi obok tej odpadły, każda na czym innym.
Terminal wypowiada warunek o parze wiązek cech,
a przyimek stoi nad zaimkiem przez całą grupę imienną,
więc żądanie postawione na terminalu musiałoby zejść przez każde jej ciało osobno —
tą samą drogą, którą przeszła
[negacja](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne),
i za tę samą cenę.
Ciało, które by cechy nie przepuściło, przepuściłoby za to każdą formę,
a takiego przeoczenia nie łapie żaden test.
Warunek sprawdzany po rozbiorze musiałby z kolei znać kształt grupy imiennej
i wyrażenia przyimkowego, czyli być gramatyką napisaną drugi raz,
a to jest właśnie kryterium, po którym warstwa więzowa
[wchodzi albo nie wchodzi](design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej).
Cecha na terminalu zostaje tam, gdzie warunek jest o parę:
zaimek dzierżawczy żąda `npraep` od formy przed rzeczownikiem
([niżej](#zaimek-dzierżawczy-jest-dopełniaczem-przed-rzeczownikiem)),
i pod przyimkiem to żądanie zostaje jedynym, które `bez niego zapisu` odrzuca.

Cena nad Składnicą wychodzi zerowa i mówi to przebieg pod morfologią żywą.
Jednoznaczność zyskuje kilkanaście zdań,
a wyprowadzenie tracą te i tylko te:

```text
Ale nie tylko same ulice irytują.
Po drugiej stronie też nie ma nic.
Posłowie opozycji winią nie tylko Żochowskiego.
W tym roku Zagłębie też nie płaci.
```

Każde z nich było przyjęte na czytaniu, w którym `nie` jest dopełnieniem,
więc odrzucenie jest przy każdym werdyktem uczciwym.
Pod złotą morfologią warunek nie rusza niczego,
bo anotatorzy wybrali tam jedno czytanie na token,
tak samo jak przy wykluczeniu wyżej.

Na zewnątrz zostaje ciąg współrzędny pod jednym przyimkiem.
`dla niego i niej` ma przyimek nad obydwoma członami,
a przed drugim z nich nie ma go wcale,
więc `Program zapisuje ustawienia dla niego i niej.` traci wyprowadzenie,
gdzie `bez nich i plików` je zachowuje,
bo tam forma przyimkowa jest członem pierwszym.
Nad Składnicą nie kosztuje to ani jednego zdania,
a zdanie odrzucone stoi wśród tego,
[czego olski nie bierze](#what-it-does-not-cover-yet).

Forma, której to wykluczenie zabiera wszystkie czytania — `niego` innych nie ma —
jest dla werdyktu formą bez licencji,
więc `Cena niego rośnie.` wychodzi odrzucone z `niego` wypisanym.
Przebieg nad korpusem czyta ją inaczej i liczy takie zdanie
jako zdanie bez struktury nad całością,
bo `blocker` w `olski/coverage.py` nazywa część mowy pierwszego czytania,
a tu nie ma ani jednego.
Rozejście to jest zapowiedziane
([design-notes.md](design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)),
a naprawę trzyma [TODO.md](../TODO.md) razem z wycięciem czytań bez licencji,
które daje tę samą krawędź bez czytań na całej klasie form.

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
i tej czytania nieodmiennego dać nie wolno;
wpuszcza ją [leksykon projektu](#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma).

## Wersalik bez czytania jest tym samym rzeczownikiem nieodmiennym

Notacja wyżej poznaje się po znaku, który ją spaja.
`README` nie niesie ani kropki, ani ukośnika,
więc wzorzec notacji go nie widzi,
a Morfeusz oddaje go jako `ign`, którego nie bierze ani jedna produkcja.
Rejestr, o który olskiemu chodzi, stawia takich form kilka na dokument —
`README`, `GLR`, `SGJP`, `LCFRS` — i stoją one na miejscach rzeczownika.

Warunek jest więc drugi i pyta o dwie rzeczy:
forma ma być pisana wersalikami i słownik ma jej nie czytać wcale.
Pierwsze pytanie zadaje już wykluczenie słownikowe,
które wersalik ze swojego zasięgu wyłącza,
bo w wersalikach forma rzeczownikiem właśnie jest
([wyżej](#the-dictionary-offers-readings-polish-does-not)),
a tutaj stoi drugie zdanie tej samej myśli.
Drugie pytanie broni polszczyzny: `NIE` i `PAN` słownik czyta,
więc czytania nieodmiennego nie dostają
i zdanie z nimi nie traci tego, które ma.
Nieodmienna taka forma jest przy tym w polszczyźnie naprawdę:
akronim odmieniony pisze się z łącznikiem i małą końcówką — `PKB-u` —
czyli już nie samymi wersalikami.

Cena jest ta sama, którą płaci notacja, i płaci się ją z tego samego powodu:
forma nieodmienna spełnia każde żądanie przypadku,
jakie unifikacja umie postawić.
`Parser GLR jest tani.` wychodzi z tego jednym czytaniem,
w którym `GLR` jest dopełniaczem przy `parser`,
a czytelnik ma tam dopowiedzenie
([niżej](#what-it-does-not-cover-yet) trzyma tę pozycję).
Werdykt mówi więc o tym zdaniu tyle, że się wyprowadza,
a o tym, czym w nim jest `GLR`, mówi nieprawdę.

Bank drzew tej ceny nie mierzy i nie zmierzy.
Przebieg nad Składnicą 180723 wychodzi z tym warunkiem i bez niego
tymi samymi liczbami, co do jednego zdania:
rejestr prasowy pisze wersalikiem akronim, który słownik zna,
a formy nieznanej pisanej wersalikami nie ma tam ani jednej.
Zakup jest przez to widoczny wyłącznie nad prozą tego repozytorium,
gdzie liczbę drukuje `olski.check`,
i tyle właśnie o tym warunku wiadomo.

## Leksykon projektu wpuszcza polskie słowo, którego słownik nie ma

`olski`, `commitów`, `Pythonem` — SGJP nie ma ani jednego z tych słów,
więc Morfeusz oddaje je jako `ign`, którego nie bierze ani jedna produkcja.
Czytania nieodmiennego, którym wchodzi notacja, dać im nie wolno,
i tą jedną rzeczą ta połowa klasy różni się od tamtej:
`commitów` jest dopełniaczem liczby mnogiej,
więc czytanie nieodmienne nie byłoby tu tylko nieznane, ale fałszywe,
a olski obiecuje, że każde jego zdanie jest polszczyzną.
Zgadywanie odmiany po zakończeniu wyrazu odpada z tego samego powodu:
Morfeusza prosi się wprost, żeby formy nieznanej nie zgadywał (`olski/morph.py`),
bo czytanie zgadnięte jest czytaniem, którego nikt nie zadeklarował.

Zostaje deklaracja, a zapisuje ją `olski/projekt.txt`.
Wpis wskazuje leksem, wedle którego słowo się odmienia, a form nie wypisuje:
`commit` odmienia się wedle `bat`, a `Python` wedle `dzban`.
Wzorzec jest przy tym faktem o odmianie, a nie o znaczeniu,
i dlatego wolno nim wskazać słowo, które z naszym nie ma nic wspólnego.
Wskazuje się leksem, a nie lemat,
bo pod jednym napisem stoi ich kilka i różnią się właśnie odmianą:
`bat:Sm3~a` ma dopełniacz `bata`, a `bat:Sm3~u` ma `batu`.
Jeden lemat ma tyle wierszy, ile leksemów mu się należy,
więc `olski` dostaje tam dwa wiersze, przymiotnik i rzeczownik,
tak samo jak `polski` ma w słowniku dwa leksemy.

Przeciw wskazaniu leksemu stała alternacja tematu,
czyli to, że `plik` ma w miejscowniku `pliku`, a temat na `t` bierze tam `cie`,
więc wzorzec dobrany byle jak wydaje formę, której polszczyzna nie ma.
Alternację niesie jednak sam wzorzec, bo granicę tematu wycina to,
na czym jego własne formy przestają się zgadzać:
`bat` ma `bacie`, więc temat schodzi do `ba`, a końcówką zostaje `t`,
i `commit`, który kończy się na `t`,
bierze stamtąd i `commitach`, i `commicie`.
Końcówka jest zarazem tym, czego wzorzec od naszego słowa żąda,
a żądania niespełnionego nie zostawia się w ciszy:
wpis dający `commitowi` wzorzec `figura` zgłasza się, zamiast wziąć temat wzorca.

Jednej pomyłki wzorzec sam nie łapie i ona jest ceną tego rozstrzygnięcia.
Wzorzec alternujący inaczej niż nasze słowo spełnia warunek na końcówkę
i wydaje formę fałszywą: `pies` daje temat `p` wraz z końcówką `ies`,
więc `bies` dostałby z niego dopełniacz `bsa`.
Trzecią kolumną wpisu jest więc świadek, czyli jedna forma, którą wzorzec ma wydać,
i on tę pomyłkę zgłasza.
Świadek ma być formą inną niż lemat, bo lemat wychodzi z każdego wzorca,
który przeszedł warunek na końcówkę,
a tam, gdzie ta proza słowo odmienia, świadkiem jest forma stojąca w niej naprawdę.

Podmiana tematu idzie tam, gdzie temat stoi, a nie na początku formy,
bo formę wolno poprzedzić przedrostkiem:
słownik trzyma `niemalowanie` w paradygmacie `malować`,
więc `lintować` bierze stamtąd `nielintowanie`.

Wiersza nie dostaje angielska nazwa przytoczona w polskim zdaniu.
`Grammatical Framework` i `Semantic Line Breaks` nie mają polskiego paradygmatu,
więc nie ma czego wskazać i żaden wiersz by ich nie wpuścił;
`New Yorkera` i `Morfologik` paradygmat mieć mogłyby i wiersza nie mają,
bo README pisze je w pozycji listy, a nie w zdaniu, na które czeka jakiś werdykt.
Plik jest przez to rejestrem tego, co ktoś rozstrzygnął, a nie listą zamkniętą,
i słowo bez wiersza wraca jako `ign`, czyli tak samo jak przed tym plikiem.

Wiersza nie dostaje też leksem dokładany do napisu, który słownik zna,
i tym plik ten różni się od `olski/skład/leksemy.py`, który wybiera między leksemami
słownika ([sklad.md](sklad.md#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)).
Projekt piszący o agentach jako o programach żąda liczby mnogiej `agenty`,
a `agenty` z SGJP jest formą deprecjatywną leksemu osobowego, czyli czym innym.
Wiersz na taki leksem dokłada czytanie formie, którą słownik już czyta,
więc łamie własność całego pliku:
ani jednej jego formy słownik nie czyta,
a zdanie już przyjęte nie ma przez to jak stracić na nim jednoznaczności.
Ta połowa klasy zostaje przez to poza tym plikiem, a ruch trzyma [TODO.md](../TODO.md).

Czyta ten leksykon cała analiza: `morphology` w `olski/subset.py`,
czyli to samo miejsce, w którym notacja dostaje swoją krawędź,
oraz warstwa rozstrzygająca, kiedy pyta o lemat gospodarza.
Skład go nie czyta, choć tego samego pliku żąda i po swojej stronie
([sklad.md](sklad.md#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr)),
a ruch trzyma [TODO.md](../TODO.md).

## What the grammar covers

- Clauses in all six orders the subject, the object and the verb stand in,
  from `Program zapisuje ustawienia.` to `Zapisuje ustawienia program.`
- Subjectless clauses, both imperative (`Zapisz plik.`)
  and pro-drop indicative (`Zapisuje ustawienia.`),
  with the object in front of the verb as well: `Cenę liczymy.`,
  the order [CLAUDE.md](../CLAUDE.md#reguły-przyjmujemy-leniwie)
  writes its own rules in
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
- Forma pisana wersalikami, której słownik nie czyta wcale,
  jako ten sam rzeczownik nieodmienny: `README mówi o podzbiorze.`, `Parser GLR
  jest tani.`
  Warunek pyta o milczenie słownika, a nie o samo pismo formy, i wywód wraz z ceną
  trzyma [poniżej](#wersalik-bez-czytania-jest-tym-samym-rzeczownikiem-nieodmiennym)
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
- Przydawka imiesłowowa, czyli imiesłów przy rzeczowniku, w obu szykach przydawki
  i wraz z dopełniaczem, którego jego czasownik żąda:
  `Wymienione zadania są obowiązkowe.`, `Reguła sięgająca znaku jest tania.`
  Bierny i czynny dochodzą osobnymi ciałami tego samego symbolu,
  a orzecznik bierze biernego i nie bierze czynnego;
  wywód wraz z ceną trzyma
  [poniżej](#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik)
- Rzeczownik odczasownikowy jako głowa grupy imiennej, w każdej pozycji, którą
  ma rzeczownik: `Przyłączenie jest tanie.`, `Wyznaczenie granicy jest tańsze.`
  Pozycją przy czasowniku ta głowa nie jest, bo dopełnienia żąda w dopełniaczu,
  a nie w bierniku; wywód trzyma
  [poniżej](#rzeczownik-odczasownikowy-jest-głową-grupy-imiennej-a-nie-pozycją-przy-czasowniku)
- Pronouns, and with them first and second person subjects.
  Person comes from the subject rather than being fixed at the third,
  so `Ja zapisuje plik.` is a disagreement
  in the way `Nowa program` is one.
- Zaimek dzierżawczy przed rzeczownikiem, czyli `jego`, `jej` i `ich`:
  `Jego skutki są znane.`, `Ich cena jest niska.`
  Zgodności ta pozycja nie ma, bo zaimek zgadza się ze swoim poprzednikiem,
  a nie z rzeczownikiem, przy którym stoi;
  warunek na formę trzyma
  [poniżej](#zaimek-dzierżawczy-jest-dopełniaczem-przed-rzeczownikiem)
- Coordination, of noun phrases, of adjective phrases and of clauses,
  joined by a conjunction or by a comma.
  The conjunction is the one Polish writes without a comma in front of it,
  on all three levels, so `Plik jest nowy ale duży.` has no derivation
- Two clauses joined by a comma and a conjunction at once,
  which is how Polish punctuates the conjunctions it puts a comma in front of:
  `Plany są niczym, ale planowanie jest wszystkim.`
  Those conjunctions are a closed list and the rest keep the position without the
  comma, so the two classes do not overlap and neither `A ale B` nor `A, i B`
  derives
- Przecinek zamykający zdanie podrzędne przed spójnikiem bez przecinka:
  `Dokument mówi, że cena jest niska, i liczy cenę.`
  Znak ten należy do zdania podrzędnego, a nie do koordynacji nad nim;
  wywód trzyma
  [poniżej](#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)
- Człon, którego czasownik ten rejestr opuszcza:
  `Milczenie obejmuje wybór, a nie zdanie.`,
  `Warstwa pyta o Przyłączenie, czyli o obiekt składniowy.`
  Rolą jest cały ten człon, a czemu on przeczy albo co powtarza,
  gramatyka nie mówi; wywód i cenę trzyma
  [poniżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)
- Spójnik stojący wewnątrz swojego zdania, a nie na jego czele:
  `Milczenie jest zatem wartością.`, `Reguła jest bowiem tania.`
  Trzy lematy tej listy — `bowiem`, `zaś` i `jednak` — czoła nie zajmują wcale,
  więc dopiero ta pozycja wpuszcza je do gramatyki; wywód trzyma
  [poniżej](#spójnik-wewnątrz-zdania-nie-dostaje-czoła-i-tym-stoi-przy-jednym-czytaniu)
- A colon opening a clause, which is how this register introduces an explanation:
  `Cena jest niska: gramatyka jest bezkontekstowa.`
  It stands above coordination rather than in it,
  so `A, B: C.` reads as `(A, B): C`.
  A noun phrase stands there as readily as a clause —
  `Gramatyka ma dwie role: podmiot i dopełnienie.` —
  and it is a second body rather than a wider symbol.
  The semicolon and the dash separate at that same level and by that same body,
  and the dash takes two of the three characters Polish writes it with,
  the hyphen having a job of its own inside a word
  ([below](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają))
- Tryb przypuszczający, czyli czas przeszły z cząstką `by` za sobą:
  `Czytelnik nie odzyskałby ról.`, `Napisałbym program.`
  Cząstka stoi przy czasowniku albo w spójniku nad zdaniem —
  `Zażądałem, by wyszedł.` — a zdanie ogłasza cechą, gdzie stoi;
  wywód trzyma
  [poniżej](#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)
- Predykatyw, czyli słowo, które orzeka bez podmiotu i bez czasownika:
  `Trzeba czytać dokumenty.`, `Widać granicę w odpowiedzi.`, `Nie wiadomo.`
  Rządzi tym, czym rządziłby czasownik, bo idzie tą samą ramą,
  a rolę ma osobną, bo czasownikiem nie jest;
  lematy są zamkniętą listą, a wywód trzyma
  [poniżej](#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika)
- Cząstka przy zdaniu i wewnątrz grupy imiennej:
  `Program już zapisuje ustawienia.`, `Już program zapisuje ustawienia.`,
  `Nawet ptaki przestały śpiewać.`
  Lematy są zamkniętą listą, a warunek na wejście jest jeden:
  cząstka bez czytania, które gramatyka bierze gdzie indziej.
  Przy zdaniu ma rolę osobną od przysłówka, którym nie jest,
  a w grupie nie ma jej wcale, i jedno i drugie trzyma
  [poniżej](#cząstka-wchodzi-obu-gospodarzami-a-w-grupie-nie-nosi-etykiety)
- Cudzysłów obejmujący grupę imienną, czyli tytuł albo termin cytowany:
  `Same „Zasady techniki prawodawczej” stoją poza tą sumą.`
  Grupa przechodzi przez niego cała, więc odmienia się wedle roli, w której stanęła
- Nawias obok zdania składowego, czyli wtrącenie, którym ten rejestr dopowiada:
  `Zdanie stoi (docs/subset.md).`, `Cena jest niska (niżej).`
  Wtrącenie jest rolą, którą werdykt nazywa,
  a dochodzi do jednego miejsca, bo w zdaniu niczego nie wypełnia;
  jedno i drugie trzyma
  [poniżej](#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)
- The past tense, agreeing with the subject in gender as well as in number,
  and with the person clitic Morfeusz cuts off the form:
  `Program zapisywał ustawienia.`, `Napisałem program.`
  What the form does to agreement is [below](#czas-przeszły-żąda-rodzaju-od-każdego-szyku)
- A `że` clause as what a verb takes, which is a position in its frame
  rather than a construction beside the others:
  `Mieszkańcy grożą, że zablokują ulice.`
- Okolicznik wyrażony zdaniem, przed swoim zdaniem i za nim:
  `Program zapisuje ustawienia, gdy linter sprawdza tekst.`
  Pozycją ramy nie jest, bo żaden czasownik go nie żąda,
  więc dochodzi do zdania, a nie do orzeczenia;
  spójnik jest zamkniętą listą lematów, a konstrukcję trzyma
  [poniżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)
- A relative clause on a noun phrase, agreeing with it in number and gender,
  with the pronoun standing for the subject, for the object,
  or under a fronted preposition together with the group it stands in:
  `Widoczny jest wzrost aspiracji społeczeństwa, które chce zdobywać wykształcenie.`,
  `ustawy, na podstawie której jest ono wydawane`
  The group carries the number and gender of the pronoun rather than of its own head,
  because it is the pronoun that agrees with the antecedent;
  the construction is argued
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
  Spójnika ono nie ma, bo podporządkowuje sam zaimek
- Kopuła opuszczona przy jednym rzeczowniku, czyli zdanie składowe bez czasownika:
  `Przepisy, o których mowa, obowiązują.`, `Mowa o zadaniach.`
  Rzeczownik ten orzeka sam i niesie rolę, którą werdykt nazywa,
  bo zdanie z nim nie ma ani podmiotu, ani czasownika,
  a lematem jest `mowa` i nic poza nim;
  wywód trzyma
  [poniżej](#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną)
- Przysłówek u trzech gospodarzy: jako okolicznik zdania, w każdej pozycji, którą
  okolicznik ma (`Program zapisuje ustawienia szybko.`, `Teraz program zapisuje
  ustawienia.`), oraz jako określenie przymiotnika i drugiego przysłówka, gdzie
  stoi sam przysłówek stopniowany (`Koszt bardzo dużego pliku jest niski.`,
  `Program zapisuje ustawienia bardzo szybko.`).
  Okolicznik przysłówkowy jest przy tym rolą, którą werdykt nazywa,
  a określenie przymiotnika stoi w wypełnieniu roli nad nim;
  gospodarzy trzyma
  [poniżej](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe)
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
Tryb przypuszczający dokłada do tych trzech dwa dalsze
([niżej](#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)).
Bez wpisanej trzeciej osoby `Ja napisał program.` wyprowadza się,
bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza.

## Cząstka trybu stoi przy czasowniku albo w spójniku

Morfeusz dzieli `odzyskałby` na czas przeszły i cząstkę `by`,
a `napisałbym` na czas przeszły, cząstkę i aglutynant,
więc tryb przypuszczający jest w tej gramatyce jedną cząstką
dopisaną do formy czasownika.
Ciała są dwa, po jednym na każde ciało czasu przeszłego,
i cząstkę dostaje ten czas i tylko on, bo tak stawia ją polszczyzna:
`zapisujeby` nie jest niczym.

Ceny w czytaniach ta cząstka nie ma żadnej i wynika to z gramatyki, nie z przebiegu:
formy `by` nie bierze przy czasowniku żaden inny terminal,
więc zdanie z nią albo wyprowadza się tymi dwoma ciałami,
albo nie ma czytania wcale — tak samo jak zdanie z dwukropkiem
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
Niezmiennika pilnuje `tests/test_subset.py`, gdzie zdanie z tą cząstką stoi wśród
przyjmowanych: `by` dopisane do listy cząstek daje mu drugie czytanie i wywraca test.
Ciało z aglutynantem nie rusza przy tym nad prozą tego repozytorium
ani jednego werdyktu: ten rejestr pisze `odzyskałby`, a nie `odzyskałbym`.
Kolejkę form bez licencji `by` prowadziło właśnie nad tą prozą
([corpus.md](corpus.md#where-the-analyses-stop)),
a większość jego wystąpień w niej jest angielskim przyimkiem,
co widać po tym, że stoi za formą, której słownik nie zna.

Ta sama cząstka bywa wpisana w spójnik:
`żeby` jest z `że` i `by`, `gdyby` z `gdy` i `by`,
`aby` z `a` i `by`, a `jakby` z `jak` i `by`.
Cząstka jest w zdaniu jedna, więc pod takim spójnikiem stoi forma na -ł
bez własnej cząstki: `Zażądałem, by wyszedł.`
Żeby spójnik miał czego żądać, zdanie ogłasza cechą `tryb`,
gdzie ta cząstka w nim stoi: przy czasowniku, w spójniku albo nigdzie.

Forma na -ł bez cząstki wychodzi z dwiema wartościami tej cechy naraz.
`Program zapisał ustawienia.` orzeka w trybie oznajmującym, kiedy stoi samo,
a pod spójnikiem w przypuszczającym,
i jest to ten sam synkretyzm, który ta gramatyka zna z przypadka:
jedna forma, dwie wartości, a wybiera między nimi przecięcie.
Samo zdanie żadnej z nich nie żąda,
więc zdanie w czasie przeszłym wyprowadza się tak jak przedtem.

Trzy napisy zostają przez to poza podzbiorem i każdy z innego powodu.
`żeby program zapisuje ustawienia` niesie formę osobową, która cząstki nie bierze.
`żeby linter sprawdziłby tekst` niesie cząstkę dwa razy.
`żeby napisałem plik` niesie aglutynant w miejscu,
w którym pod tym spójnikiem stoi jego własna końcówka:
polszczyzna ma `żebym napisał`.

Ceną jest ta cecha w każdej produkcji zdania.
Cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc ciało, które trybu nie przepuści, wpuszcza pod ten spójnik każdy tryb.
Niezmiennika pilnuje `tests/test_subset.py`:
ciało zdania bez tej cechy wywraca suitę,
bo pojedyncze zdanie tego nie łapie, a ciał zdania jest kilkadziesiąt.

Ciąg współrzędny wypuszcza tryb członu pierwszego i od pozostałych nie żąda niczego,
więc `żeby program zapisał ustawienia i linter sprawdza tekst` wyprowadza się,
choć polszczyzna żąda formy na -ł od obu członów.
Zmienna wspólna zabrałaby zdania już przyjęte:
`Program zapisuje ustawienia, a linter sprawdziłby tekst.`
koordynuje tryb oznajmujący z przypuszczającym.

Ile ich zabrałaby, jest zmierzone.
Zmienna wspólna na ogonie ciągu odbiera wyprowadzenie kilku zdaniom Składnicy,
pod morfologią żywą dwa razy tylu zdaniom,
a przeszło dziesięciu zdaniom prozy tego repozytorium,
bo koordynacja dwóch trybów jest w niej zwyczajna
(`Lista urywa się na MAX_READINGS, […] więc odpowiedź policzona po liście myliłaby
brak czytania z jego numerem`).
Kupuje za to czytania nieprawdziwe w kilku zdaniach banku drzew,
a jednoznaczności nie kupuje ani jednemu zdaniu:
z wieloznacznych do przyjętych nie przechodzi żadne.
Naprawa mieszcząca się w cechach jest więc droższa od usterki,
a naprawa poza cechami żąda warunku sprawdzanego po rozbiorze,
którego olski nie ma i który dla tej jednej pozycji nie zarabia na siebie.
Liczby daje wariant gramatyki z tą zmienną, puszczony przez `harness/ruch.py`.

Wypełnieniem bywa fraza bezokolicznikowa zamiast zdania —
`Odnotowuję to, żeby złagodzić wrażenie.` —
i w banku drzew pada ona pod tymi spójnikami
niemal tak samo często jak forma na -ł.
Bezokolicznik podmiotu nie ma i trybu nie niesie, więc ciało z nim o tryb nie pyta,
a osobne jest dlatego, że jego cena jest osobną liczbą.
Oba wypełnienia biorą oba miejsca okolicznika,
bo zdanie z każdym z tych spójników polszczyzna wysuwa:
`Żeby zostać rezydentem księstwa, musisz mieć oszczędności.`

Cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew,
a wynika to z gramatyki, nie z przebiegu:
`comp` z tymi lematami nie brał przedtem żaden terminal,
więc zdanie z takim spójnikiem nie miało czytania,
z którego dałoby się je wytrącić.
Zakupem jest przeszło pięćdziesiąt zdań Składnicy zdjętych z listy odrzuconych,
z czego połowa na przyjęte.
Role tych przyjętych zgadzają się z drzewem wzorcowym poza jednym zdaniem:
w `Zrodził się pomysł, by produkować klepkę.`
bank drzew przyłącza cel do rzeczownika, a olski do zdania.
Nad prozą tego repozytorium nie kupuje ani jednego zdania,
tak samo jak dopisania przed nim.

Poza podzbiorem zostaje cząstka stojąca dalej od czasownika —
`Nie ma aplikacji, która by to wszystko napędzała.` —
i jest to [nieciągłość](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
a nie brak pozycji.
Zostaje też aglutynant przy spójniku, czyli `żebym napisał`:
Morfeusz tnie ten napis na `żeby` i `m`,
a końcówka dochodzi w tej gramatyce do czasownika, przy którym stoi
([TODO.md](../TODO.md)).

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

## Zdanie deklaruje córki, a warunek deklaruje szyk

Produkcja mówi naraz dwie rzeczy: z czego zdanie się składa
i w jakiej kolejności te córki stoją.
Rozdzielone, te dwie rzeczy mieszczą się w siedmiu deklaracjach,
z których rozwinięcie pisze kilkadziesiąt ciał `ClauseConjunct`.
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

Reguła obejmuje przy tym córkę czasownikową,
bo polszczyzna okolicznik między czasownikiem a podmiotem stawia.
Bez tej pozycji płaci się w obu walutach naraz:
`Trwa w tej sprawie dochodzenie.` nie wyprowadza się wcale,
a `Zapisuje w pliku program ustawienia.` wychodzi jednym czytaniem,
w którym `program ustawienia` jest dopełnieniem,
i nie wychodzi tym, w którym `program` zapisuje `ustawienia`.
Drugie z tych dwóch jest tą samą pomyłką,
przed którą broni [reguła o obu czytaniach](#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
a po werdykcie jej nie widać, bo werdykt brzmi wtedy `valid`.
Zawężenie takiego kształtu mieści się po rozwinięciu w jednym argumencie
deklaracji, a nie w kilkudziesięciu ciałach, z których żadne go nie wypowiada,
i dopiero wtedy da się je wycenić jednym przebiegiem.

Wyjęte zostaje orzeczenie, bo okolicznik bierze ono samo, przez `Complements`,
więc miejsce obok niego byłoby drugim wyprowadzeniem jednego napisu.
Dotyczy to obu miejsc, które ta córka ma, czyli tego za nią i tego na końcu zdania,
więc pyta o nie jeden zbiór, a nie dwa.

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

Wywód ten obowiązuje tam, gdzie obowiązuje zgodność.
Okolicznik wyrażony zdaniem dochodzi do całego ciągu zdań składowych,
bo nie zgadza się z niczym ani pod członem, ani nad ciągiem,
więc brak rodzaju u ciągu nic mu nie odbiera,
a czytania są dwa i oba polszczyzna ma
([wyżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).
Zawężenie zostaje przez to przy przydawce, czyli przy tym, co je uzasadnia,
a [TODO.md](../TODO.md) trzyma pozycję trzecią, czyli wyrażenie przyimkowe nad ciągiem,
którego zawężenie nie uzasadnia z tego samego powodu.

Dwa symbole zamiast jednego wybrano dla liczby czytań, a nie dla parsera.
Tablica Earleya bierze rekursję lewostronną,
co pilnuje test w `tests/test_subset.py`,
więc `NP → NP conj NP` dałoby się tu wpisać jedną produkcją w miejsce dwóch.
Powiedziałoby ono o zasięgu dokładnie to samo, bo zawężenie wyżej stoi na rodzaju,
którego ciąg nie ma, a nie na kształcie produkcji —
i wypuszczałoby ciąg tyloma wyprowadzeniami, ilu on nawiasowań dopuszcza:
ciąg trzech członów dwoma, czterech pięcioma, a siedmiu stu trzydziestoma dwoma,
gdzie te dwa symbole wypuszczają każdy z nich raz.
Są to wyprowadzenia jednej struktury, więc gramatyka płaciłaby tu tym,
czym płaci [gramatyka kategorialna](design-notes.md#kierunek-produkcja-się-rozwarstwia-a-podłoże-zostaje):
wieloznacznością pozorną, którą trzeba potem kwotować postacią normalną.
Ciąg siedmiu członów nie jest przy tym przypadkiem z brzegu:
tyle ma wyliczenie z rejestru ustaw, nad którym olski liczy czytań najwięcej
([ustawy.md](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)),
i tamta liczba mówi, ile taki mnożnik znaczy przy zdaniu,
które wieloznaczność ma już z innego powodu.

## Interpunkcja zdaniowa spina zdania, które już się wyprowadzają

Polszczyzna łączy dwa zdania spójnikiem, przecinkiem albo jednym i drugim naraz,
dwukropkiem wprowadza wyjaśnienie, a średnikiem rozdziela to, co spina treść.
Olski wyprowadzał z tego dwa pierwsze sposoby,
a resztę zostawiał wierszowi `interp`,
który kolejkę blokerów prowadzi i liczy w niej tysiące zdań
([corpus.md](corpus.md#where-the-analyses-stop)).

Nowego kształtu zdania ta konstrukcja nie wymaga,
bo jej członami są zdania, które gramatyka wyprowadza i bez niej.
Wymaga natomiast trzech rozstrzygnięć, po jednym na znak.

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
Dwukropek wchodzi w dwa ciała i nie bierze go żaden inny terminal,
a te dwa żądają za nim symboli rozłącznych: jedno zdania, drugie grupy imiennej.
Grupa imienna zdaniem nie jest, więc napis wzięty jednym z tych ciał
nie ma wyprowadzenia drugim, a zdania bez dwukropka żadne z nich nie dotyczy.
Zero po stronie ceny jest przez to wyprowadzone, a nie zmierzone,
i pilnuje tego `tests/test_subset.py`:
za dwukropkiem stoją dokładnie te dwa symbole,
a trzeci zamieniłby to zero w liczbę, którą trzeba by policzyć.

**Za dwukropkiem stoi zdanie albo grupa imienna.**
`Gramatyka ma dwie role: podmiot i dopełnienie.` wylicza to,
co zdanie przed dwukropkiem nazwało liczbą albo terminem,
a wylicza jednym ciągiem współrzędnym, więc grupa bierze tę pozycję cała.
Ciało jest osobne od zdaniowego, bo cena każdego z nich jest osobną liczbą,
a kupuje ono pojedyncze zdania tej prozy: konstrukcja jest częsta,
lecz zdania, które ją niosą, potykają się jeszcze o co innego.
Rolą jest cała ta grupa, tak samo jak przy wtrąceniu w nawiasie,
i tyle właśnie werdykt o niej mówi:
do którego składnika zdania ona się odnosi, gramatyka nie rozstrzyga,
i jest to ta sama odmowa, którą wydaje o członie bez czasownika
([wyżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).

**Średnik rozdziela tak samo jak dwukropek i tak samo nie kosztuje nic.**
`Program zapisuje ustawienia; cena jest niska.` wyprowadza się ciałem
`Sentence → Clause ; Clause .`, czyli tym samym, tylko z drugim znakiem,
a cena jest i tu zerowa z gramatyki: średnika nie bierze żaden inny terminal.
Ciała są mimo to dwa, a nie jedno biorące oba znaki naraz,
bo zakup każdego z nich jest osobną liczbą i sonda bierze ją zdejmowaniem ciał.

Za tym znakiem stoi rejestr, a nie polszczyzna.
Średnik stoi tam, gdzie stanąłby przecinek albo kropka,
więc produkcja nie mówi nic, czego nie mówi dwukropkowa,
a przemawia za nią to, że ten rejestr średnika używa:
zdania z nim stoją w tych dokumentach i w ustawach.

**Myślnik rozdziela tym samym ciałem, a bierze dwa znaki z trzech.**
`Cena jest niska — gramatyka jest bezkontekstowa.` wychodzi tak samo jak zdanie
z dwukropkiem, a warunek na lemat bierze pauzę i półpauzę, czyli te dwa znaki,
którymi polszczyzna myślnik pisze.
Łącznika ten warunek nie bierze, bo łącznik spaja wewnątrz wyrazu — `UTF-8`,
`16-latków` — i to jest tu cena, a nie oszczędność:
zdanie, które myślnik pisze łącznikiem, zostaje odrzucone.

Drugiego znaku rozdzielającego zdanie nie bierze — ani dwóch średników, ani
średnika razem z dwukropkiem — bo `Clause` żadnego z nich nie ma, więc rekurencji
nie ma czym zbudować. Granica ta jest wypowiedziana, a nie przeoczona, i zostaje
[niżej](#what-it-does-not-cover-yet).
Najwięcej kosztuje ona przy myślniku, bo ten rejestr stawia go parą częściej
niż pojedynczo, a para obejmuje wtrącenie w środku zdania,
zamiast rozdzielać dwa zdania.

**Przecinek przed spójnikiem jest faktem o słowie.**
`Plany są niczym, ale planowanie jest wszystkim.` przecinka wymaga,
a `Program zapisuje ustawienia i linter sprawdza tekst.` nie bierze go wcale,
i rozstrzyga o tym sam spójnik, a nie miejsce, w którym pada.
Spójnik zdaniowy rozdziela się przez to na dwie klasy,
a drugą wyznacza warunek ujemny na pierwszą, bo klasy nie mają się zachodzić:
lemat wzięty obiema pozycjami dałby polszczyźnie dwa napisy tam, gdzie ma ona jeden.
Klasa bez przecinka wyklucza ponadto cząstkę przeczącą, i to jest to samo
wykluczenie o jeden lemat szersze: Morfeusz czyta `nie` także jako spójnik,
a gramatyka ma dla tej formy pozycję przy czasowniku,
więc bez tego warunku `Zgodności ta pozycja nie ma i mieć nie może.`
wychodzi dwoma zdaniami spiętymi przez `nie`.
Warunek zabiera pojedyncze zdania tej prozy i każde z nich wyprowadzało się
właśnie tak, czyli czytaniem, którego polszczyzna nie ma.
Klasa z przecinkiem jest zamkniętą listą —
`ale`, `a`, `lecz`, `natomiast`, `więc`, `zatem`, `toteż`, `czyli` —
i obejmuje dwie części mowy naraz,
bo Morfeusz zna `więc` jako `comp`, a `ale` jako `conj`,
a o interpunkcji przed nimi ten podział nie mówi nic.
`zaś` i `jednak` na tej liście nie figurują, bo czoła swojego zdania nie zajmują:
polszczyzna stawia je za pierwszym wyrazem — `linter zaś sprawdza tekst` —
i jest to ten sam warunek, którym lista spójników okolicznikowych wyklucza `bowiem`
([niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).
Te trzy lematy bierze pozycja wewnątrz zdania i ona jedna
([wyżej](#spójnik-wewnątrz-zdania-nie-dostaje-czoła-i-tym-stoi-przy-jednym-czytaniu)).
Lemat pominięty na liście zostaje przy pozycji bez przecinka,
więc pominięcie nie odbiera ani jednego zdania.

Podział ten odbiera zarazem napisy, których polszczyzna nie ma.
`Program zapisuje ustawienia ale linter sprawdza tekst.` wyprowadzało się,
dopóki jedno ciało brało całą klasę `conj`,
a klasa bez przecinka dochodzi do wszystkich trzech poziomów koordynacji,
więc `Plik jest nowy ale duży.` przestaje wychodzić jednym czytaniem.
Pozycji z przecinkiem grupa imienna i przymiotnikowa nie dostają,
bo `nie polszczyzny, a dziedziny` jest w nich elipsą, a nie ciągiem współrzędnym.
Lemat dopisany do listy odbiera przez to napis bez przecinka:
`Skład czyli Morfeusz jest tani.` wyprowadzało się, dopóki `czyli` stało w klasie
bez przecinka, a polszczyzna ten znak przed nim stawia.
Dopowiedzenia z `czyli` żadna z tych dwóch pozycji nie daje,
bo dopowiedzenie odnosi się do składnika zdania,
a koordynacja zdaniowa łączy dwa zdania;
daje je człon bez czasownika
([wyżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).
Zawężenie tych dwóch poziomów nie rusza ani jednego zdania w żadnym z trzech
rejestrów — ani nad Składnicą, ani nad README, ani nad ustawami —
więc płaci za nie sam werdykt, który przedtem kłamał pewnie.

Bez trzeciego warunku ta pozycja nie kupiłaby prawie nic,
a warunek ten pada na lemat przyimka, a nie na produkcję
([niżej](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)):
Morfeusz czyta `a` także jako przyimek,
więc każde `, a` w zdaniu wychodziło okolicznikiem wysuniętym drugiego składowego.

Poza gramatyką zostaje ciąg dwóch znaków rozdzielających, zapisany
[niżej](#what-it-does-not-cover-yet).

## Człon bez czasownika stoi za spójnikiem, który go bierze

Ten rejestr dokumentuje podzbiór przez to, czego w nim nie ma,
więc `a nie` oraz `czyli` niosą setki zdań tej prozy,
a za tym spójnikiem stoi sam człon, bez powtórzonego czasownika:
`Milczenie obejmuje wybór, a nie zdanie.`
Olski żądał tam zdania współrzędnego i dlatego takie zdanie odrzucał,
choć `Milczenie obejmuje wybór.` przyjmował.

Konstrukcja jest elipsą, a nie koordynacją,
i rozstrzyga o tym pozycja, którą ten człon zajmuje:
żadnej. `wybór` jest dopełnieniem, a `zdanie` mówi, czym dopełnienie nie jest,
więc wpuszczone jako drugi człon ciągu imiennego wychodziłoby drugim dopełnieniem
i zdanie przyjęte mówiłoby o sobie nieprawdę.
Stoi więc obok zdania składowego, tam gdzie wtrącenie w nawiasie,
i tak samo nazywa się całym napisem
([niżej](#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).

**Czemu ten człon przeczy, gramatyka nie mówi.**
`Milczenie obejmuje wybór, a nie zdanie.` przeciwstawia dopełnieniu,
a `Wybór obejmuje milczenie, a nie zdanie.` przeciwstawia albo dopełnieniu,
albo podmiotowi, i rozstrzyga o tym znaczenie, a nie kształt.
Jest to ta sama odmowa, którą olski wydaje o przyłączeniu
([niżej](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
z jedną różnicą: przyłączenie olski melduje jako wieloznaczność,
bo gramatyka ma tam kilka wyprowadzeń,
a tutaj wyprowadzenie jest jedno i milczy o tym, do czego człon się odnosi.
Werdykt nazywa więc rolę `Ellipsis` i wypisuje pod nią cały napis.

**Spójnik rozstrzyga, czy ten człon wchodzi, i lista jest węższa od zdaniowej.**
`a`, `ale`, `lecz`, `natomiast`, `tylko` i `czyli` biorą człon bez czasownika,
a `więc`, `zatem` i `toteż` go nie biorą,
bo `Cena jest niska, więc gramatyka.` polszczyzną nie jest.
Podział ten nie jest oszczędnością, tylko obietnicą podzbioru:
lista wzięta cała wyprowadzałaby napis, którego polszczyzna nie ma.
`czyli` stoi na liście po jednej stronie z `a nie`,
choć jedno przeczy, a drugie powtarza to samo innymi słowami:
różnicy tej gramatyka nie widzi, a rola nazywa kształt, nie funkcję.
Dopowiedzenie z `czyli` schodzi tym samym z kolejki w postaci,
w której ten rejestr pisze je najczęściej — na końcu zdania —
a postać wtrącona, `Skład, czyli Morfeusz, jest tani.`, zostaje
([niżej](#what-it-does-not-cover-yet)).

**Wypełnienia są trzy i każde ma cenę osobną.**
Grupa imienna, grupa przymiotnikowa i wyrażenie przyimkowe wchodzą osobnymi
ciałami, bo cena każdego z nich ma być osobną liczbą, i te liczby się rozchodzą:
nad polską prozą tego repozytorium grupa imienna kupuje kilkadziesiąt zdań,
wyrażenie przyimkowe kilkadziesiąt, a grupa przymiotnikowa poniżej dziesięciu
i zabiera przy tym pojedyncze zdania przyjęte,
bo `droga` i `tania` są u Morfeusza naraz rzeczownikiem i przymiotnikiem.
Przysłówek stał w tej pętli i wypadł: kupował pojedyncze zdania,
czyli tyle, ile nie warto czterech ciał.

Osobno stoi cząstka przecząca, bo ciało z nią i ciało bez niej są dwoma ciałami,
a nie jednym z cząstką pominiętą, i to ona kupuje najwięcej — przeszło sto zdań.
Dopełniaczem nie rządzi i nie ma czym: czasownika pod nią nie ma,
a przypadek członu jest przypadkiem tego, czemu on przeczy,
więc cechy `negacja` to ciało nie niesie.

**Przecinek zamykający ten człon jest drugim takim przecinkiem w gramatyce.**
`Granica pakietu jest tu rozstrzygnięciem, a nie przypadkiem, i pilnuje go test.`
biegnie za tym członem dalej, tak samo jak zdanie nadrzędne biegnie dalej
za zdaniem podrzędnym, więc ciało zamknięte przecinkiem dokłada ta sama funkcja
([niżej](#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
Kupuje ono kilkanaście zdań i jest zarazem tym,
co czyni przecinek przed `i` w tym rejestrze poprawnym w dwóch miejscach,
a nie w jednym.

**Zakup zależy od rejestru o rząd wielkości.**
Nad polską prozą tego repozytorium ta konstrukcja kupuje przeszło sto
czterdzieści zdań, czyli kilka procent tego, co ta proza ma,
a nad bankiem drzew kilkadziesiąt, czyli promile.
Rozjazd nie mówi nic o gramatyce i wszystko o tym, kto pisze:
podzbiór dokumentuje się przez wykluczanie, a gazeta nie.
Mierzy to za jednym razem obie kolejki, o których mówi
[corpus.md](corpus.md#the-same-queue-over-prose).

## Spójnik wewnątrz zdania nie dostaje czoła i tym stoi przy jednym czytaniu

`Milczenie jest zatem wartością.`, `Reguła jest bowiem tania.`,
`Linter zaś sprawdza tekst.`
Polszczyzna stawia te spójniki wewnątrz zdania, za jego pierwszym wyrazem,
a olski miał dla nich jedno miejsce — czoło drugiego zdania po przecinku —
więc zdanie z takim spójnikiem w środku nie miało czytania.
Trzy lematy tej listy czoła nie zajmują wcale,
i to o nich lista spójników okolicznikowych mówiła, że pozycji dla nich nie ma
([niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).

Pozycją jest lista okoliczników i nic poza nią.
Wystarcza to, bo miejsce na okolicznik wylicza się za każdą córką zdania,
a nie przed pierwszą (`olski/precedencja.py`),
czyli ta lista mówi dokładnie tyle, ile polszczyzna o tym spójniku mówi.
Czoła zdania ten symbol nie dostaje, i to trzyma jeden napis przy jednym czytaniu:
`Cena jest niska, więc gramatyka jest tania.` ma spójnik za przecinkiem,
więc bierze go koordynacja
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
a czoło dałoby temu napisowi drugie wyprowadzenie tego samego kształtu.
Cena wychodzi zatem z gramatyki, a nie z przebiegu, tak samo jak przy dwukropku,
a zakup jest zmierzony: kilkadziesiąt zdań tej prozy.

Rola jest osobna od cząstki, bo osobna jest część mowy:
cząstka określa zdanie, a ten spójnik wiąże je z tym, co stoi przed nim,
więc `Particle: zatem` mówiłoby o zdaniu, że ma określenie, którego nie ma.
Jest to ten sam podział, którym cząstka stoi osobno od przysłówka
([niżej](#cząstka-wchodzi-obu-gospodarzami-a-w-grupie-nie-nosi-etykiety)).

Poza gramatyką zostaje `zatem` na czele swojego zdania —
`Zatem milczenie jest wartością.` — czyli ta pozycja, którą trzy z tych lematów
mają, a której koordynacja nie daje, bo żąda przecinka przed sobą.
Ruch trzyma [`TODO.md`](../TODO.md).

## Cząstka wchodzi obu gospodarzami, a w grupie nie nosi etykiety

`Program już zapisuje ustawienia.`, `Reguła obowiązuje także wtedy.`,
`Już program zapisuje ustawienia.` —
cząstka stoi w zdaniu tam, gdzie okolicznik przysłówkowy,
i tę pozycję gramatyka ma, odkąd ma
[przysłówek](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe).
Produkcje są przez to dwie i pisze je ta sama pętla, co tamte:
cząstka w liście okoliczników i cząstka na czele zdania składowego.

Przy zdaniu cząstka dostaje rolę osobną od przysłówka, choć pozycję ma tę samą,
bo werdykt nazywa rolę etykietą węzła:
`Adverb: już` mówiłoby o zdaniu, że ma okolicznik przysłówkowy, którego ono nie ma.

Drugim gospodarzem jest grupa imienna,
bo tam polszczyzna cząstkę stawia tak samo:
`Nawet ptaki przestały śpiewać.` mówi o ptakach, a nie o przestawaniu,
i widać to po zasięgu podmiotu, a nie po żadnej roli.
Ciałem jest `NPConjunct → part NPConjunct`, a osobę przepuszcza ono,
bo cząstka staje i przed zaimkiem: `Nawet ja zapisuję ustawienia.`

W grupie cząstka etykiety nie nosi, bo widać ją w napisie roli,
którą ta grupa zajmuje: podmiotem jest `Nawet ptaki`.
Rolę niesie przez to gospodarz jeden, tym samym prawem,
którym niesie ją [jeden gospodarz przysłówka](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe).

Wybór gospodarza nie jest tu jednak rozstrzygnięciem, i tym cząstka różni się
od przysłówka. Przysłówkowych gospodarzy rozdziela stopień, czyli cecha,
którą niesie tagset, a cząstki nie rozdziela ani cecha, ani lemat:
bank drzew stawia wewnątrz grupy każdy lemat tej listy, który w nim pada,
i ten sam lemat stawia przy zdaniu.
Udział wystąpień w grupie idzie od jednego na jedenaście przy `dopiero`
do co drugiego przy `niemal`,
a lematu, który stałby wyłącznie w grupie albo wyłącznie przy zdaniu, nie ma;
trzy lematy stoją tam wyłącznie przy zdaniu i każdy pada mniej niż dziesięć razy.
Podział listy po lemacie jest więc wariantem odrzuconym:
bank drzew go nie potwierdza, a kryterium na tę pozycję nie jest leksykalne.
Zostaje wieloznaczność oddana czytelnikowi,
tak samo jak przy [wyrażeniu przyimkowym](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).

Cena wypada przez to inaczej niż przy przysłówku.
Nad Składnicą kilkadziesiąt zdań schodzi z przyjętych na wieloznaczne
pod jedną morfologią i pod drugą, a wyprowadzenie zyskuje kilka.
Zakupem jest prawda o zdaniu, a nie pokrycie:
wiersz zdań czytanych wbrew drzewu wzorcowemu maleje o blisko połowę
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)),
złote czytanie wraca kilku zdaniom wieloznacznym,
a zdania czytanego przy tym gospodarzu wbrew drzewu, a bez niego zgodnie z nim,
nie ma ani jednego.
Nad rejestrem ustaw jedno zdanie traci jednoznaczność,
nad korpusem audytowym jedno zyskuje wyprowadzenie,
a nad prozą tego repozytorium nie rusza się ani jedno.

Trudność nie leży przy tym w żadnej z tych pozycji, tylko w liście lematów.
Morfeusz trzyma pod `part` całą klasę cząstek naraz,
a w niej cztery słowa, które olski bierze albo wyklucza osobno:
`nie` przeczy, `się` stoi przy czasowniku zwrotnym,
`czy` otwiera pytanie o rozstrzygnięcie,
a `by` żąda trybu przypuszczającego, którego ta gramatyka nie ma
([niżej](#what-it-does-not-cover-yet)).
Lista jest więc zamknięta, a kryterium na wejście jedno:
cząstka ma nie mieć czytania, które gramatyka bierze już gdzie indziej.
`tylko` je ma, bo Morfeusz czyta je także jako spójnik, a spójnik bierze koordynacja,
więc wpuszczone tutaj dałoby jednemu napisowi dwa wyprowadzenia;
tym samym warunkiem stoją obok siebie dwie klasy
[spójnika zdaniowego](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają).
Poza listą zostaje przez to `tylko`, `też`, `bo` i `to`,
a `to` ma ponadto własną pozycję, której olski nie ma
([niżej](#what-it-does-not-cover-yet)).

## Interpunkcja obejmująca: cudzysłów wchodzi w grupę, a nawias staje obok zdania

Znak rozdzielający spina dwa zdania, a obejmujący bierze to, co stoi w środku,
i te dwie pary są w tym rejestrze dwiema różnymi konstrukcjami.
Cudzysłów obejmuje tytuł albo termin cytowany — `„Zasady techniki prawodawczej”` —
a nawias dopowiedzenie obok zdania, którym w tej prozie jest nazwa dokumentu:
`(docs/subset.md)`, `(niżej)`.

**Cudzysłów przepuszcza grupę imienną całą.**
Produkcja obejmuje grupę i wypuszcza jej przypadek, liczbę oraz rodzaj bez zmiany,
bo polszczyzna odmienia to, co cudzysłów obejmuje, wedle roli, w której grupa stanęła:
`Same „Zasady techniki prawodawczej” stoją poza tą sumą.` ma w środku mianownik,
a `Ustawa jest przepisem „Zasad techniki prawodawczej”.` dopełniacz.
Znaki są dwa i są różne, bo polszczyzna otwiera cudzysłów innym znakiem,
niż go zamyka, więc napis niedomknięty nie ma wyprowadzenia.
Wnętrzem jest sama grupa imienna, więc `„to nie zdanie”` zostaje na zewnątrz:
w cudzysłowie stoi tam zdanie, a nie grupa.

**Nawias dochodzi w każdym napisie do jednego gospodarza.**
`Zdanie stoi (docs/subset.md).` wychodzi jednym czytaniem,
a nie tyloma, ile gospodarzy ma w zdaniu wyrażenie przyimkowe,
i nie jest to wybór przyłączenia, którego olski nie robi
([niżej](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)).
Nawias niczego w zdaniu nie wypełnia,
więc gdziekolwiek by dochodził, role zdania są te same,
a różnicy między dwoma miejscami nie ma czym wypowiedzieć —
gdzie wyrażenie przyimkowe zmienia to, o czym zdanie mówi, a nawias nie zmienia nic.
Wtrącenie jest przy tym rolą, którą werdykt nazywa,
i jest rolą całym napisem: przysłówek w środku nawiasu nie jest okolicznikiem zdania,
więc zejście po role zatrzymuje się na wtrąceniu tak samo jak na zdaniu podrzędnym.

Wnętrzem nawiasu jest grupa imienna albo przysłówek, bo tym są te dopowiedzenia:
nazwą dokumentu i wskazaniem, gdzie szukać.
Pozycje są dwie i obie stoją tam, gdzie nawias zamyka zdanie składowe
albo zdanie względne odgrodzone przecinkami:
`Reguła, która rozstrzyga (niżej), jest tania.` wychodzi jednym czytaniem.

**Druga pozycja stoi w ciele zamykanym przecinkiem i tylko w nim.**
Ciała zdania względnego są dwa, bo przecinek zamykający polszczyzna stawia wtedy,
gdy zdanie nadrzędne biegnie dalej
([niżej](#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
a w tym z przecinkiem nawias stoi przed nim,
gdzie przyłączony do zdania nadrzędnego stanąłby za nim, czyli dałby inny napis.
Ciało bez przecinka kończy się tam, gdzie kończy się zdanie nadrzędne,
i tam pozycji nie potrzeba, bo pierwsza z dwóch obsługuje ten napis w całości:
`Program zapisuje regułę, która rozstrzyga (niżej).` wychodzi jednym czytaniem,
w którym nawias dochodzi do zdania nadrzędnego.
Druga pozycja dopisana i tam nie kupiłaby ani jednego zdania,
a dołożyłaby temu napisowi czytanie,
i nierówność ciał jest przez to oszczędnością, a nie ceną.

Nad Składnicą ta pozycja nie rusza ani jednego zdania,
pod złotą morfologią ani pod żywą,
bo proza prasowa nawiasu wewnątrz zdania względnego nie pisze.
Pisze go dokumentacja tego repozytorium, i pisze kilka razy,
a przyjętego zdania ta pozycja jej dotąd nie kupiła:
zdania te niosą obok tego nawiasu inne konstrukcje, których olski nie ma,
więc pozycja zdejmuje jeden powód odrzucenia, a nie całe odrzucenie.
Zakup jest przez to odłożony, a nie zmierzony na zero,
i tym różni się ta pozycja od tych, które wchodzą z przejściami między werdyktami.

Na zewnątrz zostaje nawias w środku grupy imiennej —
`grupa imienna (ta z dopełniaczem) stoi` —
i jest to w tej prozie mniejszość:
nawias stoi w niej zwykle przed kropką albo przecinkiem,
czyli tam, gdzie kończy się zdanie, jego składowe albo zdanie względne w nim,
co liczy `grep -oP '\)[.,]' proza/docs.txt | wc -l` wobec wszystkich nawiasów tego pliku.

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
W grupie imiennej produkcji z nią jest cztery,
bo pod głową może stać jeszcze przymiotnik, wyrażenie przyimkowe albo jedno i drugie.
Dwie następne są w [grupie, którą polszczyzna wysuwa przed zdanie względne
razem z zaimkiem](#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka):
przydawką dopełniaczową jest tam sam zaimek względny,
więc bez warunku `Polszczyzna, której nikt nie napisał, jest podzbiorem.`
wychodzi drugim czytaniem, w którym `której nikt` jest taką grupą.
Gdzie indziej czytanie zostaje, bo gdzie indziej jest tym, czym w polszczyźnie jest.

Paradygmat `ten` jest częścią tej klasy, a nie całą klasą.
`nikt`, `kto`, `nic`, `coś` i `ktoś` mają u Morfeusza czytanie jedno
i jest ono rzeczownikowe,
więc pod nimi nie stoją dwa czytania tej samej formy,
a mimo to produkcja z dopełniaczem po głowie bierze je za głowę:
bez warunku `Wtedy nikt nas nie zauważy.` wychodzi drugim czytaniem,
w którym `nikt nas` jest grupą imienną.
Przy paradygmacie `ten` takie czytanie zdejmuje także złota morfologia,
bo anotator wybiera jedno czytanie formy.
Tutaj wybierać nie ma z czego, więc czytanie zostaje po obu morfologiach,
a warunek jest jedynym miejscem, w którym ono ginie.

Wpisem na tej liście jest lemat, bo słownik nie daje nic innego,
o co dałoby się zapytać:
`nikt` jest `subst:sg:nom:m1` tak samo, jak `parser` jest `subst:sg:nom:m3`,
a zaimka od rzeczownika nie rozdziela w nim
ani znacznik, ani cecha, ani kwalifikator.
Lista jest przez to zamknięta i starzeje się o każdy zaimek,
którego nikt do niej nie dopisze.
Starzenie kosztuje wieloznaczność, a nie zdanie odrzucone:
lemat dopisany odbiera czytanie i żadnego nie dodaje.

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
bierze ona każdą formę, której lematów leksykon nie wymienia,
i jest to drugi warunek ujemny, jaki ta gramatyka stawia.

Te dwa warunki różnią się zasięgiem.
Wykluczenie zaimka mówi „tym słowem nie bądź”, więc pyta o jedno czytanie formy;
klasa domyślna mówi „tą formą nie bądź”, więc pyta o wszystkie jej lematy naraz.
Klasa domyślna bez tego zasięgu przepuszcza formę, którą miała zatrzymać,
a co jej tą drogą przeszło, mówi
[sekcja o leksykonie](#walencja-jest-leksykonem-o-ramie-domyślnej).
Wykluczenia leksykalne zostają przy czytaniu, bo o czytaniu mówią.
Czytanie i forma nie są tym samym słowem:
`nie` jest u Morfeusza cząstką `nie` i formą `on`,
`lecz` spójnikiem i rozkaźnikiem od `leczyć`,
a `pnie` grupą imienną od `pień` obok formy od `piąć`.
Pomiar tej różnicy nie widzi:
zamiana ich wszystkich na zasięg formy
nie rusza nad Składnicą ani jednego zdania pod żadną morfologią.
Zobaczy ją pierwsze wykluczenie, które taką formę trafi,
bo zasięg formy odbierze jej czytanie, o którym to wykluczenie nic nie mówi.

Warunek i kupuje, i płaci, a pomiar mówi ile.
Nad Składnicą pod Morfeuszem
[podnosi on liczbę zdań przyjętych](corpus.md#what-morphological-ambiguity-costs)
o kilkadziesiąt, a odrzuca kilka.
Pod złotą morfologią widać obie strony tej wymiany:
kilka zdań przechodzi z wieloznacznych na przyjęte i każde z nich zgadza się
z drzewem wzorcowym, a kilku warunek zabiera jedyne czytanie, jakie miały,
i były to czytania, którym drzewo wzorcowe przeczyło albo których nie potwierdzało.
Każde z tych zdań stało na jednej frazie, której polszczyzna nie ma —
`to` z dopełniaczem pod sobą tam, gdzie tym dopełniaczem rządzi czasownik —
i tamten dokument jedno z nich cytuje.
Liczby dzisiejsze wydają dwa przebiegi `olski-corpus`, z warunkiem i bez niego:
sonda różnicowa zdejmuje produkcje, a to jest warunek w terminalu.

Rozłożona na produkcje cena wypada po obu stronach inaczej.
W grupie imiennej warunek coś znaczy w każdym z czterech ciał:
zdjęty z dwóch, pod których głową stoi jeszcze przymiotnik,
oddaje pod morfologią żywą wieloznaczność
`Wprowadźmy do tego trupiego świata poprawkę.`
i podwaja liczbę czytań kilku dłuższym zdaniom banku drzew,
a pod złotą nie rusza tam nic.
W dwóch produkcjach wysunięcia nie rusza nad Składnicą liczby czytań
ani jednego zdania pod żadną z dwóch morfologii,
więc jest w nich z wywodu, a wywód jest ten sam:
przydawka dopełniaczowa jest w obu miejscach tą samą przydawką.

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
nad README, siedmioma ustawami i korpusem audytowym razem
`niż`, `co` i `jako` po przeszło setce razy, `jak` kilkadziesiąt,
`aniżeli` kilka, przy kilkuset formach `a`.
Kryterium na przypadek zabrałoby więc razem z rozdzielającym `a` i te pięć.

Cena jest zerowa i jest to wynik pomiaru, a nie założenie.
Pod złotą morfologią przebieg nad Składnicą nie rusza ani jednego zdania z 13 035,
bo tam każda forma ma jedno czytanie wybrane przez człowieka
i `a` nie jest w tym korpusie przyimkiem ani razu.
Pod żywą morfologią, czyli nad prozą README, warunek odbiera jedno zdanie —
to wypisane wyżej — i oddaje je z powrotem przecinek przed spójnikiem
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
z trzema czytaniami w miejsce trzech.
Liczba czytań wychodzi więc ta sama przed i po,
a różnią się one tym, że tamte trzy niosły okolicznik, którego zdanie nie ma,
a te trzy niosą podmiot, który ono ma.

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

Ramę wybiera forma, a nie jej pojedyncze czytanie,
bo inaczej wystarczy formie jeden lemat spoza leksykonu, żeby zawężenie ominąć.
`zapisuje` jest u Morfeusza i od `zapisywać`, i od `zapisować`;
drugiego z nich leksykon nie wymienia, więc czytanie stąd brało ramę domyślną
razem z biernikiem, i `Program zapisuje się ustawienia.` się wyprowadzało,
choć `zapisywać się` biernika nie bierze.
Klasa domyślna pyta więc o wszystkie lematy formy naraz
i wypada tam, gdzie leksykon wymienia którykolwiek z nich
(`bez_lematów_formy` w `olski/grammar.py`).
Forma o lematach niezgodnych bierze przez to ramę najwęższą z nich:
`działa` jest formą `działać`, która biernika nie bierze,
i formą `dziać`, która go bierze; jako forma biernika nie bierze.

Pod złotą morfologią pytanie nie powstaje.
Anotator wybrał po jednym czytaniu na token, więc forma ma tam jeden lemat,
i przebieg nad Składnicą nie rusza ani jednego zdania ani jednego czytania.
Cena i zysk wypadają więc pod Morfeuszem, gdzie ubywa przeszło setka czytań.
Po kilka zdań idzie tam w każdą ze stron:
jedne przechodzą z wieloznacznych na przyjęte, drugie tracą jedyne czytanie.
Rozsądza je czytanie ręką, bo pod żywą morfologią
rozpiętości złotego drzewa nie są porównywalne (`olski/coverage.py`).
Wypadają w jedną stronę.
Ubywa czytań z dopełnieniem, którego czasownik nie bierze:
`Wszedł do starej komórki.` czytało się także z dopełnieniem `komórki`,
a `Wzrosły również obroty całego rynku.` z dopełnieniem `obroty całego rynku`.
Zdania odrzucone opierały się wszystkie na trzech formach —
`pora`, `sposób`, `cieszą` — i żadne z nich na czytaniu prawdziwym.
`Już pora.` przechodziło z `pora` jako czasownikiem,
`Wprost nie sposób!` z rozkaźnikiem od `sposobić`,
a `Z decyzji cieszą się związkowcy, którzy żądali odwołania dyrektora.`
z dopełnieniem `odwołania dyrektora` wyrwanym ze zdania względnego.
Dla dwóch pierwszych zdań olski czytania prawdziwego nie ma,
bo nie ma predykatywu `pora` ani `nie sposób` na swojej liście
(`PREDYKATYWY` w `olski/subset.py`; co z tym zrobić, notuje `TODO.md`),
więc odrzucenie mówi o nich prawdę, której `valid` nie mówiło
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).

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
Samo powtórzenie symbolu im nie wystarcza, bo nad ciągiem stoi jeszcze
[okolicznik zdaniowy](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania),
który do całego ciągu dochodzi i własny symbol powtarza tak samo.
Rozdziela je znak: koordynacja spina członów spójnikiem albo przecinkiem
stojącym w ciele słowem, a określenie jest grupą,
która swój przecinek niesie w sobie.

### Przecinek zamykający należy do zdania podrzędnego, a nie do spójnika za nim

Przecinek zamykający stawia polszczyzna wtedy, gdy zdanie nadrzędne biegnie dalej,
a biegnie ono dalej także spójnikiem:
`Dokument mówi, że cena jest niska, i liczy cenę.`
Zdanie względne miało na to parę ciał — jedno zamknięte przecinkiem, drugie nie —
a pozostałe trzy zdania podrzędne miały samo ciało otwarte,
więc przecinek przed `i` dochodził do koordynacji,
która spójnika przed sobą nie bierze, i zdanie nie miało ani jednego czytania.
Parę ciał ma przez to każde z czterech.

`A, i B` dalej się nie wyprowadza i to jest tu cała ostrożność.
Przecinek przed `i` nie jest w polszczyźnie znakiem koordynacji zdaniowej
i lista spójników przecinkowych go nie obejmuje
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
więc pozycja dochodzi zdaniu podrzędnemu, a nie spójnikowi:
znak wchodzi tam, gdzie polszczyzna go stawia, i nigdzie poza tym.

Kupuje to nad bankiem drzew kilkadziesiąt zdań, a nad prozą tego repozytorium kilka.
Liczba ta zależy jednak od tego, co jeszcze w gramatyce stoi, i to jest tu ciekawsze
od niej samej: zdjęta z gramatyki bez przydawki imiesłowowej ta sama pozycja
kupowała pojedyncze zdania, bo zdanie, które jej potrzebuje, potykało się wtedy
o imiesłów.
Cena pozycji pojedynczej jest więc różnicą wobec gramatyki dzisiejszej,
a nie stałą, którą raz się zapisuje
([pisanie-po-olsku.md](pisanie-po-olsku.md#zasłanianie-działa-w-obie-strony)).

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
Dochodzi zarazem do całego ciągu współrzędnego, a nie do samego składowego w nim,
i te dwa czytania są dwoma zdaniami:
`Dwoisz się i troisz, aby rozwiązać problemy.` mówi o obu członach naraz,
a `Mieszkał z ojcem i nie chciał, żeby ktoś wiedział.` o samym drugim.
Bez pozycji nad ciągiem gramatyka ma samo czytanie drugie,
czyli wybiera przez przeoczenie
([niżej](#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)),
a nad zdaniami takimi jak pierwsze wybiera odwrotnie, niż czyta czytelnik.

Ciąg jest tu żądany cechą, bo nad zdaniem o jednym członie
oba ciała dają ten sam napis dwoma kształtami.
Cena stoi przez to w jednoznaczności, a nie w pokryciu:
nad Składnicą traci ją garść zdań przyjętych,
nad prozą tego repozytorium pojedyncze zdanie,
a z odrzuconych do przyjętych nie przechodzi ani jedno.
Bez żądania ciągu cena jest kilkakrotnie wyższa,
bo dochodzi do niej każde zdanie o jednym członie.
Bank drzew tego wyboru nie rozstrzyga:
oba czytania mają rolę okolicznika o tej samej rozpiętości,
a porównanie ról pyta o rozpiętości
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)),
więc różnicę widać w werdykcie po nazwie gospodarza i nie widać jej w pomiarze.
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
Zdanie pod spójnikiem z tej listy stoi w trybie oznajmującym,
a `aby`, `żeby`, `by`, `gdyby` i `jakby` żądają przypuszczającego
i biorą przez to ciała osobne
([niżej](#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)).
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
Sam podział ma przy tym świadka zmierzonego:
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
([niżej](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe)),
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
Pomiar mówi, że autor pisze, ponieważ tekst jest gotowy.
```

Czytania są dwa i oba polszczyzna nad tym zdaniem ma,
a streszczenie rozdziela je nazwaniem tej roli albo przemilczeniem jej:
okolicznik doszedł do zdania streszczanego albo do tego, które stoi pod `że`.

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
pozycję tę stawia pytanie, więc oba te zdania wyprowadzają się, każde raz.

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
a `której autorzy piszą` mnogą przy pojedynczym.
Para wzięta z zaimka przyjmuje przez to `Ustawa, której autorzy pisze`,
a para wzięta z głowy `Ustawy, której autorzy piszą` —
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

Podmiotu zdanie z wysuniętym dopełnieniem nie żąda,
bo deklaracje są dwie — z podmiotem i bez niego —
tak samo jak ma je zdanie główne.
Jedno czytanie ma przez to `Dyrektor wymienia imprezy, które zorganizował.`
i jedno `Dyrektor wymienia imprezy, które on zorganizował.`.
Ciała pisze obu rodzinom czół jedna funkcja, więc to samo dostało pytanie:
`Które zadania wykonuje?` wyprowadza się obok `Które zadania gmina wykonuje?`.

Zakupem są pod złotą morfologią cztery zdania Składnicy wyjęte z odrzucenia
i piąte, które z odrzucenia przechodzi w wieloznaczność;
pod żywą jest ich odpowiednio trzy i dwa.
Role trzech z tych czterech zgadzają się z drzewem wzorcowym,
a czwarte — `Złodzieje kradną drogi sprzęt, który potem sprzedają w cenie złomu.` —
olski czyta z okolicznikiem przy zdaniu nadrzędnym zamiast przy względnym,
bo miejsce na okolicznik jest w ciele jedno,
a to zdanie stawia okolicznik po obu stronach czasownika.

Płacą za to zdania, w których zaimek jest zarazem mianownikiem i biernikiem,
a czasownik biernik bierze, bo daje mu go rama domyślna:
`Wywód, który za nią stał, stoi dalej.` z prozy README jest takim zdaniem,
a nad Składnicą pod żywą morfologią traci jednoznaczność jedno.
Pod złotą morfologią nie traci jej ani jedno,
bo anotator wybrał tam jedno czytanie na token,
a nad rejestrem ustaw nie rusza się ani cena, ani zakup.
Tą samą drogą wyprowadza się `Ustawa, której przepisy obowiązuje`,
i dlatego parę cech czoła pokazuje wyżej głowa męskoosobowa,
której mianownik różni się od biernika.

Pod żywą morfologią jedno z tych zdań wchodzi przy tym
nie tym czytaniem, o które szło.
`Myślę o tym człowieku, który mnie podglądał.` wychodzi
pytaniem zależnym w pozycji, którą każdemu czasownikowi daje
[rama domyślna](#walencja-jest-leksykonem-o-ramie-domyślnej),
a nie zdaniem względnym:
zdanie względne z wysuniętym podmiotem stawia dopełnienie za czasownikiem,
więc `mnie podglądał` nie ma w nim gdzie stanąć.

Wysunięte dopełnienie sięga ponadto do formy osobowej i nie dalej,
bo ciała wypisane wyżej mają w środku czasownik zdania składowego,
więc dopełnienie należące do bezokolicznika pod nim nie ma się skąd wziąć:
`Ustawa, którą organ gminy może wydać, jest tania.` jest odrzucone.
Zdania tego kształtu nie ma jednak ani jedno zdanie rejestru ustaw,
co pokazuje `grep -P 'któr\w+ [^.]*\b(może|mogą|ma|mają)\b [^.]*\w+ć'`
nad `proza/ustawy/`, więc konstrukcja ta jest wyczytana z gramatyki,
a nie z korpusu.

Po ten brak sięgnęłaby cecha przeciągana, czyli luka zamiast wypisanych ciał,
a ile ona kupuje i dlaczego nie weszła, mierzy
[design-notes.md](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze).

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

Zakup liczy się przez to w innej walucie i widać go w dwóch porównaniach ról
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Pod złotą morfologią 34 zdania wieloznaczne przechodzą z `lost` na `survives`,
a 10 zdań przyjętych z `partial` na `agrees`;
`disagrees` nie rośnie o ani jedno.

Tych dwóch liczb nie bierze żadne polecenie i bierze je ręka,
bo sonda różnicowa liczy przejścia werdyktu (`harness/ruch.py`),
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

```sh
python3 -m olski.check -c "Mowa o zadaniach." --readings
```

```text
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

## Określenie przed zdaniem wchodzi pod to, które stoi za nim

Zdanie składowe bierze określenie z obu stron i bierze je jednym symbolem.
Przed nim stoi wyrażenie przyimkowe, przysłówek albo cząstka,
a za nim wtrącenie w nawiasie, człon bez czasownika
albo [okolicznik wyrażony zdaniem](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania).
Cały ciąg współrzędny bierze z obu stron ten jeden okolicznik
i żąda tego samego, i z tego samego powodu.
Żadna z tych produkcji nie mówi, która dochodzi pierwsza,
więc same z siebie dają jednemu napisowi dwa kształty:

```text
Na stole leży sto dwadzieścia chlebów, bo piekarz je tam położył.
```

`Na stole` wchodzi w jednym kształcie pod okolicznik, a w drugim nad niego,
i to jest cała różnica między nimi.
Streszczenie nie różni ich ani jednym znakiem,
bo gospodarzem tego modyfikatora jest w obu ten sam czasownik,
więc werdykt liczy dwa czytania
i nie ma czym pokazać, czym się różnią.
Czytelnik nie ma tu przy tym czego rozstrzygać:
określenie przed zdaniem nie mówi nic o tym, co stoi za zdaniem,
a określenie za zdaniem nie mówi nic o tym, co stoi przed nim.
[Czytaniem jest kształt](#co-się-liczy-jako-jedno-czytanie),
więc dwa kształty na jedno czytanie są usterką tej gramatyki,
a nie faktem o polszczyźnie.

Kształt zdejmuje gramatyka, choć oba znaczą to samo,
bo ani tożsamość czytania, ani warstwa znacząca tu nie sięgają.
Zwinięcie po stronie tożsamości żąda postaci normalnej nad zagnieżdżeniem określeń,
zostawia oba wyprowadzenia w lesie,
a sygnatura grubsza obowiązuje każde zdanie naraz, nie tylko tę parę
([disambiguation.md](disambiguation.md#tożsamość-czytania-jest-tańsza-i-częściowo-już-stoi)).
Warstwa znacząca dziedzinę ma węższą niż gramatyka i tych zdań nie dosięga
([architecture.md](architecture.md#werdykt-liczy-wyprowadzenia-bo-powstaje-pod-dwiema-warstwami-które-liczą-znaczenia)).
Warunek w gramatyce kosztuje za to jedną cechę, a las po nim maleje.

Porządek jest zapisany cechą (`dostawka` w `olski/subset.py`):
określenie stojące za zdaniem ją wypuszcza,
a określenie wysunięte przed zdanie żąda gospodarza, który jej nie niesie.
Wysunięte wchodzi więc pod to, co stoi za zdaniem, i nigdy nad nie.
Który z dwóch kształtów zostaje, nie rozstrzyga niczego poza sobą:
werdykt nad takim zdaniem wychodzi z obu ten sam.

Zdanie określone z jednej strony ma kształt jeden i warunek tego kształtu nie rusza,
więc nie odbiera on wyprowadzenia ani jednemu zdaniu:
nad Składnicą 180723 odrzuconych zdań jest z nim tyle samo, ile bez niego,
pod złotą morfologią i pod żywą.
Zdanie określone z obu stron ma za to czytań co najmniej o połowę mniej,
bo bez warunku mnoży je każde wysunięcie z każdym określeniem za zdaniem,
a kilkanaście zdań tego banku drzew przechodzi z wieloznacznych do przyjętych,
żadne nie tracąc złotego czytania.
Nad prozą tego repozytorium przechodzi ich kilka
([corpus.md](corpus.md#where-the-analyses-stop) trzyma polecenie).

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

### Liczebnik złożony przyłącza się wedle ostatniego członu

`Dwadzieścia dwa chleby leżą.` odmienia się wedle `dwa`,
a `Dwadzieścia siedem chlebów leży.` wedle `siedem`,
czyli wedle tego z dwóch przyłączeń wyżej, które niesie człon skrajnie prawy.
Dwa liczebniki obok siebie są więc łańcuchem o głowie po prawej,
a nie trzecim przyłączeniem ani warunkiem w środku tamtych dwóch:
symbol `Liczebnik` bierze `accommodability` od swojej głowy,
a oba tamte ciała pytają go tym samym, czym pytały terminala.
Łańcuch jest osobnym ciałem, bo sonda wycenia go zdejmowaniem ciał.

Przypadek, liczba i rodzaj są w łańcuchu wspólne wszystkim członom,
bo polszczyzna odmienia każdy z nich:
`Dwudziestu dwóch mężczyzn przyszło.` stawia w mianowniku oba człony,
a `dwadzieścia dwóch` nie jest niczym.
Łańcuch wiąże w prawo, więc `sto dwadzieścia dwa` ma jedno nawiasowanie.

Ostatniego członu `jeden` łańcuch nie bierze.
`Dwadzieścia jeden chlebów` żąda dopełniacza mnogiego,
choć `jeden chleb` żąda zgodności,
czyli ten człon rządzi w łańcuchu inaczej, niż rządzi sam.
Osobne ciało na `jeden` po liczebniku kupiłoby liczby zakończone na jeden,
więc wejdzie dopiero wtedy, gdy takich zdań naliczy się więcej niż garść.

Płaci łańcuch drugą walutą i płaci w dwóch miejscach.
Pierwsze z nich zdejmuje warunek ujemny.
Morfeusz daje `pięć` drugie czytanie — dopełniacz mnogi rzeczownika
odczasownikowego od `piąć` — a rzeczownik odczasownikowy jest
[głową grupy imiennej](#rzeczownik-odczasownikowy-jest-głową-grupy-imiennej-a-nie-pozycją-przy-czasowniku),
więc bez warunku `Dwadzieścia pięć chlebów leży.` wychodzi dwoma czytaniami:
łańcuchem oraz `dwadzieścia` nad grupą, której głową jest `pięć`.
Drugiego polszczyzna nie ma, a kolizja bierze co dziesiątą liczbę pisaną słowem,
bo tyle kończy się na pięć,
więc terminal rzeczownika odczasownikowego tego lematu nie bierze.
Jest to czwarty warunek ujemny w tej gramatyce
i trzeci postawiony na lemacie po to, żeby odebrać czytanie,
którego polszczyzna w tym miejscu nie ma
([wyżej](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)).
Zabiera on cały leksem, bo negacji unifikacja nie zna,
więc `Pięcie jest trudne.` przestaje się wyprowadzać,
a skreślenie jednego argumentu oddaje to zdanie z powrotem.

Drugie miejsce zostaje i jest nim zagnieżdżenie.
Grupa, którą buduje liczebnik zgodny, jest dopełniaczem mnogim tak samo jak sam
rzeczownik — `brakuje dwóch mężczyzn` — więc ciało rządzące bierze ją nad sobą
i `Dwudziestu dwóch mężczyzn przyszło.` czyta się dwojako:
o dwudziestu dwóch oraz o dwudziestu z dwóch.
Drugie czytanie polszczyzna pisze przyimkiem, którego w tym zdaniu nie ma,
a cechy dzisiejsze tych dwóch nie odróżniają:
liczebnik zgodny wypuszcza grupę o cechach samego rzeczownika,
więc różni je sam kształt.

Zagnieżdżenie zachodzi tam, gdzie pierwszy człon jest synkretyczny
między rządzącym i zgodnym, czyli w formach męskoosobowych i przypadkach zależnych.
`Dwadzieścia dwa chleby leżą.` wychodzi jednym czytaniem.
Przed tą pozycją zdanie o dwudziestu dwóch przechodziło pod samym zagnieżdżeniem,
więc łańcuch zamienia tu werdykt nieprawdziwy na odmowę
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).

Odróżnia te dwa czytania cecha dopisana, czyli znacznik taki jak
[`ciąg`](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania):
grupa zbudowana przez liczebnik zgodny ogłasza się nim,
ciało rządzące żąda od tego, co pod nim stoi, wartości przeciwnej,
a `Dwudziestu dwóch mężczyzn przyszło.` wychodzi wtedy jednym czytaniem, tym właściwym.
Drugiej kopii pozycji grupy imiennej znacznik nie żąda;
żąda tej cechy w każdej produkcji `NP` i `NPConjunct`,
bo żądanie jest dodatnie, a cechy nieobecnej unifikacja nie sprawdza.
Czytanie zostaje mimo to, bo naprawa nie kupuje niczego, co dałoby się zmierzyć.
Zdań stawiających obok siebie dwie formy o czytaniu liczebnikowym
ma Składnica 180723 dziesięć,
znacznik nie rusza liczby czytań ani nad jednym z nich pod żadną z dwóch morfologii
ani nad prozą tego repozytorium,
a rejestr docelowy pisze liczebnik złożony
[cyfrą](#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii), której olski nie bierze.
Liczbę pierwszą daje przejście po złotej morfologii banku drzew,
a pozostałe wariant gramatyki z tą cechą, puszczony przez `harness/ruch.py`.

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

## Przydawka imiesłowowa stoi tam, gdzie przymiotnik

`Wymienione zadania są obowiązkowe.` i `Reguła sięgająca znaku jest tania.`
różniły się w gramatyce tym, na czym stawała analiza:
pierwsze na kształcie grupy imiennej, drugie na samym słowie,
bo formy `pact` nie brał żaden terminal.
Konstrukcja jest jednak jedna i jest nią przydawka,
a nie dwie pozycje przy dwóch częściach mowy.

Imiesłów przy rzeczowniku zgadza się z nim przypadkiem, liczbą i rodzajem,
czyli tym samym, czym zgadza się przymiotnik,
i stoi w tych samych dwóch szykach.
Dochodzi więc ciałem symbolu przymiotnikowego, a nie własnym symbolem:
osobny żądałby drugiej kopii każdej pozycji, w której przydawka stoi —
a stoi ich w gramatyce kilkanaście —
i nie kupowałby za to niczego, czego polszczyzna w tych pozycjach rozdziela.
Dopełniacz, którego imiesłów czynny żąda od swojego dopełnienia,
przychodzi przez to za darmo:
ciało z przydawką i dopełniaczem pod głową stało w gramatyce przed nim.

Ciała są dwa, po jednym na imiesłów, bo cena każdego jest osobną liczbą.
Orzecznik bierze przy tym biernego i nie bierze czynnego:
`Dziewczyna milknie zakłopotana.` jest polszczyzną,
a `Reguła jest sięgająca.` nie jest zdaniem, które ten rejestr pisze.

Cena stoi po stronie zgodności z drzewem wzorcowym, a nie po stronie pokrycia.
Przebieg nad Składnicą 180723 wypuszcza z odrzuconych przeszło dwieście zdań
i dokłada kilkadziesiąt przyjętych,
a podnosi przy tym dwie liczby, które mówią o werdykcie, że kłamie:
zdania, w których przyjęte czytanie przeczy drzewu wzorcowemu,
oraz zdania wieloznaczne, którym złote czytanie z lasu wypada.
Werdykt mówi więc o zdaniu nieprawdę częściej niż przed tą pozycją,
a kierunek ten trzyma
[roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę);
czym te zdania są, ten przebieg nie mówi, a wpis trzyma [TODO.md](../TODO.md).
Obie liczby drukuje `olski.coverage`, a te sprzed tej pozycji trzyma git.

## Rzeczownik odczasownikowy jest głową grupy imiennej, a nie pozycją przy czasowniku

`Przyłączenie`, `wykluczanie`, `sięgnięciu` — Morfeusz daje takiej formie tag
`ger` wraz z liczbą, przypadkiem i rodzajem,
czyli z tym wszystkim, czego gramatyka od głowy grupy imiennej żąda.
Rodzaj jest przy tym zawsze nijaki, a niesie go tag, więc nie żąda go tu nic.

Rejestr, o który olskiemu chodzi, mówi tą formą o czynnościach,
bo dokumentacja opisuje to, co program robi:
`przyłączenie wyrażenia przyimkowego`, `wyznaczenie granicy`,
`sięgnięcie po mocniejszy mechanizm`.
Kolejka nad prozą tego repozytorium postawiła tę klasę na czele
zaraz po [leksykonie projektu](#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma),
a kolejka ze Składnicy trzyma ją w czwartym wierszu
([corpus.md](corpus.md#where-the-analyses-stop)).

Wchodzi ona jako głowa grupy imiennej, a nie jako pozycja przy czasowniku,
i tyle mówi o niej polszczyzna:
dopełnienia żąda w dopełniaczu — `przyłączenie wyrażenia`, a nie `przyłączenie
wyrażenie` — czyli tak, jak żąda go rzeczownik z dopełniaczem pod głową.
Rama czasownika zostaje przez to nietknięta,
a grupa z taką głową stoi w każdej roli, w której stoi każda inna grupa imienna.

Ta głowa dostaje tyle pozycji, ile ma rzeczownik, i dostaje je jednym zapisem:
pętla w `olski/subset.py` wypisuje każde ciało grupy imiennej dwa razy,
raz z rzeczownikiem i raz z formą odczasownikową.
Terminala o dwóch częściach mowy naraz w tym miejscu nie ma
i nie jest to wybór wygody:
cena tej głowy ma być osobną liczbą, a sonda różnicowa wycenia ją zdejmowaniem ciał
([CLAUDE.md](../CLAUDE.md#code)),
więc pozycja zlana w jeden terminal nie byłaby żadnym ciałem osobno.
Pętla kupuje zarazem to, czego dwa komplety ciał wypisane obok siebie nie dają:
pozycja dopisana kiedyś rzeczownikowi dochodzi tą samą deklaracją i drugiej głowie.

Jedno wykluczenie stoi po stronie rzeczownika i nie dotyczy tej głowy.
Głowa rządząca dopełniaczem nie jest [zaimkiem rzeczownym](#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
a żaden z tych zaimków nie jest rzeczownikiem odczasownikowym,
więc po tej stronie nie ma czego wykluczać i warunek stoi w deklaracji pary,
a nie w każdym ciele osobno.

Jednej pozycji ta głowa nie ma i jest nią grupa wysunięta przed zdanie względne:
`którego przyłączenia` nie ma wyprowadzenia, gdzie `którego wyrażenia` ma.
Czoło zdania względnego bierze rzeczownik, a tej głowy nie bierze,
i wpuszczenie jej tam trzyma [TODO.md](../TODO.md).

## Predykatyw orzeka bez podmiotu i rządzi ramą czasownika

`Trzeba czytać dokumenty.`, `Widać granicę w odpowiedzi.`, `Nie wiadomo.` —
Morfeusz trzyma te słowa pod `pred`, czyli w jednym wierszu kolejki blokerów
([corpus.md](corpus.md#where-the-analyses-stop)).
Orzekają one bez podmiotu i bez czasownika,
a rządzą tym, czym rządziłby czasownik,
więc rama i `Complements` są tu te same, co u niego, tylko bez orzecznika zgodnego:
dopełnienie, bezokolicznik, zdanie z `że`, pytanie zależne i okolicznik
dochodzą bez ani jednego ciała osobnego, a dopełniacz negacji tą samą cechą,
którą przechodzi przez zdanie z czasownikiem
([wyżej](#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)).

Zdaniem składowym jest predykatyw wprost, a nie orzeczeniem pod nim.
Pod `Predicate` stanęłoby przy nim ciało z podmiotem,
więc `Programy trzeba czytać.` wychodziłoby zdaniem o podmiocie `Programy`,
choć `programy` jest tam biernikiem;
osoby ani liczby predykatyw nie niesie, więc unifikacja tego czytania nie odbiera.
Przy [kopuli opuszczonej](#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną)
zapadł ten sam wybór: rzeczownik orzekający stoi obok `Predicative`, a nie jest nim.
Rolę ma predykatyw osobną od `Verb`, bo zgodności nie niesie:
`Verb: trzeba` mówiłoby o zdaniu, że ma orzeczenie zgodne z podmiotem,
którego ono nie ma.

Lista lematów jest zamknięta, bo `pred` niesie całą klasę naraz,
a kryterium na wejście jest jedno:
czytanie konkurujące nie może stanąć na czele zdania tego samego kształtu.
`to` takie czytanie ma, i to dwa razy:
grupa imienna bierze jego czytanie rzeczownikowe,
a jako `pred` jest ono łącznikiem, czyli konstrukcją osobną i niewpuszczoną
([niżej](#what-it-does-not-cover-yet)).
Prowadzi ono zarazem ten wiersz kolejki, więc wyłączenie `to` jest ceną tej listy.
Poza listą stoją tak samo `brak`, `czas`, `pora`, `żal`, `sposób` i `szkoda`:
każde z nich Morfeusz zna także jako rzeczownik,
a rzeczownik w mianowniku z dopełniaczem za sobą jest grupą imienną,
którą ta gramatyka wyprowadza.
`trudno` i `łatwo` nie stoją poza listą, tylko poza częścią mowy:
Morfeusz czyta je jako przysłówki,
choć bank drzew liczy `Trudno` właśnie w tym wierszu.

Ciała są dwa, bo zakup każdego jest osobną liczbą:
predykatyw z wypełnieniem i predykatyw sam, czyli `Nie wiadomo.` albo `Można.`
Zakup wynosi nad Składnicą kilkadziesiąt zdań, w większości po stronie ciała
z wypełnieniem, a ceny w czytaniach nie ma żadnej:
ani jedno zdanie przyjęte nie staje się wieloznaczne.
Jeden kształt zdania wychodzi pod obydwoma ciałami naraz inaczej niż pod każdym
osobno — `Rozumiem, że można, a nawet trzeba piętnować wszelkie formy nawracania
pod przymusem.` — bo jeden predykatyw stoi w nim sam, drugi z wypełnieniem,
a koordynuje je spójnik.
Olski nie czyta przy tym niezgodnie z drzewem wzorcowym ani jednego zdania nowo
przyjętego, a pojedyncze czyta uboższą listą ról niż drzewo.
Nad prozą tego repozytorium zakup jest liczony w kilku zdaniach przyjętych,
a wieloznacznych przenosi więcej niż przyjmuje.
Tę parę ciał dzieli z predykatywem forma nieosobowa czasownika
([niżej](#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu)),
więc zdjęcie któregoś z nich zabiera obie głowy naraz.

Ta konstrukcja ma jeden szyk — predykatyw stoi przed tym, czym rządzi —
i tyle też po niej zostaje [niżej](#what-it-does-not-cover-yet).

## Czasownik nieosobowy orzeka bez podmiotu i rządzi ramą swojego lematu

`Zgłoszono usterkę.`, `Nie zrobiono nic.`, `Podano do stołu.` —
Morfeusz trzyma te formy pod `imps`, czyli w jednym wierszu kolejki blokerów
([corpus.md](corpus.md#where-the-analyses-stop)).
Orzekają one bez podmiotu tak samo jak predykatyw wyżej,
więc rolę i oba ciała zdania biorą te same co on,
a różnica jest jedna: ta forma jest czasownikiem,
więc ramę bierze z leksykonu swojego lematu
([wyżej](#walencja-jest-leksykonem-o-ramie-domyślnej)),
a nie z jednej ramy wpisanej obok zamkniętej listy słów.
Widać ją na lemacie, o którym leksykon mówi, że biernika nie bierze:
`Pomagano usterkę.` jest odrzucone tam, gdzie `Zgłoszono usterkę.` się wyprowadza.

Zamkniętej listy ta konstrukcja nie ma i nie potrzebuje jej.
Predykatyw musi ją mieć, bo `pred` niesie słowa o konkurującym czytaniu —
`to` prowadzi ten wiersz i jest zarazem łącznikiem —
a formy `imps` takiego czytania nie mają:
z 321 form tego znacznika w banku drzew jedna, `pito`, ma czytanie spoza tej
części mowy, a każde inne drugie czytanie jest znów formą `imps`,
czyli jednym czytaniem, a nie dwoma
([wyżej](#co-się-liczy-jako-jedno-czytanie)).
Cząstka `się` stoi przy tej formie tak samo jak przy osobowej
i pyta o ten sam leksykon zwrotny, bo `zajmowano się sprawą`
jest tym samym czasownikiem co `zajmuje się sprawą`.

Orzecznika zgodnego nie ma ani jedna z tych dwóch ram,
bo zgadza się on z podmiotem, którego takie zdanie nie ma:
`Zgłoszono tania.` nie jest niczym, tak samo jak `Trzeba wolni.`
Osobna od `Verb` jest ta rola także dla tej formy i decyduje o tym gramatyka:
zgodności ta forma nie niesie żadnej,
a cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc pod symbolem czasownika `Zgłoszono program.` wychodziłoby zdaniem
o podmiocie `program`, choć `program` jest tam biernikiem.
Symbol wspólny kosztuje przy tym pomiar różnicowy:
zdjęcie ciała zdania zabiera obie głowy naraz,
więc cenę każdej z nich mierzy się zdjęciem jej terminali
([CLAUDE.md](../CLAUDE.md#code)).

Zakup rozkłada się na te dwa ciała tak samo jak przy predykatywie:
ciało z wypełnieniem zdejmuje nad Składnicą z listy odrzuconych kilkadziesiąt zdań,
a ciało samej formy — `Na północy i wschodzie strzelano.` — pojedyncze.
Obie morfologie oddają tyle samo i rozkładają to inaczej,
bo pod żywą więcej z tych zdań wychodzi wieloznacznych niż przyjętych.
Jedno zdanie wychodzi pod obydwoma ciałami naraz inaczej niż pod każdym osobno —
`Załadowano się na pięć barek i o zmierzchu wyruszono.` —
bo jedna forma stoi w nim sama, druga z wypełnieniem, a koordynuje je spójnik.

Cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew,
a zero jest tu własnością konstrukcji, a nie wynikiem przebiegu:
formy `imps` nie brała przedtem żadna produkcja,
więc żadne zdanie przyjęte jej nie niosło.
Niezgodnie z drzewem wzorcowym olski nie czyta ani jednego zdania nowo przyjętego,
a pojedyncze czyta uboższą listą ról niż drzewo.
Nad rejestrem ustaw zakup jest liczony w pojedynczych zdaniach i wszystkie
wychodzą wieloznaczne, a nad rozporządzeniem nie rusza się ani jeden werdykt,
choć i ono te formy pisze: zdania z nimi stoją tam także na czym innym.
Nad prozą tego repozytorium nie kupuje ani jednego zdania:
README pisze taką formę raz, a zdanie z nią stoi na formie żartu z nazwy
([roadmap.md](roadmap.md#readme-jest-przyrządem-pomiarowym)).

Szyk ma ta konstrukcja jeden, ten sam co predykatyw — forma stoi przed tym,
czym rządzi — więc wypełnienie wysunięte przed nią zostaje
[niżej](#what-it-does-not-cover-yet) razem z wypełnieniem predykatywu.
Cząstki trybu przypuszczającego ta forma nie bierze:
`Zgłoszono by usterkę.` jest odrzucone, bo cząstkę bierze forma na -ł
i tylko ona ([wyżej](#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)).

## Zaimek dzierżawczy jest dopełniaczem przed rzeczownikiem

`Jego skutki są znane.`, `Jej cena jest niska.`, `Ich liczba rośnie.`
Posiadanie trzeciej osoby polszczyzna wyraża dopełniaczem zaimka osobowego,
a nie osobnym przymiotnikiem, i tym różni się `jego` od `mój`, `nasz` i `swój`:
te trzy Morfeusz zna jako przymiotniki,
więc bierze je pozycja przymiotnika przy rzeczowniku,
a `jego`, `jej` oraz `ich` czyta jako formy lematu `on`,
więc brakowało trzeciej osoby i tylko jej.

Pozycja jest jedna i stoi przed grupą imienną, bo tam ją polszczyzna stawia.
Dopełniacz po rzeczowniku bierze inna produkcja,
więc `skutki jego` wychodzi tak samo jak `skutki wyboru`
([wyżej](#what-the-grammar-covers)), i ciało jest dlatego jedno, a nie dwa.

Zgodności ta pozycja nie ma i mieć nie może.
Zaimek zgadza się liczbą i rodzajem ze swoim poprzednikiem,
a poprzednik stoi w zdaniu obok, a nie w tej grupie,
więc cechy grupy są cechami głowy, a zaimek nie wnosi do nich nic:
`Jego skutki` ma zaimek pojedynczy przy rzeczowniku mnogim, a `Ich cena` odwrotnie.
Zmienna wspólna — ta, którą wypuszcza przymiotnik i liczebnik zgodny obok —
wygląda tu poprawnie i odbiera polszczyźnie prawie każdą taką parę;
niezmiennik pilnuje test w `tests/test_subset.py`.

Formę zawężają dwa warunki na cechę, a nie lista lematów:
lematem każdej z tych form jest `on`, więc lista wpuszczałaby je wszystkie naraz.
Pierwszy żąda formy akcentowanej, czyli zostawia poza pozycją `go`:
`Znam go cenę.` nie jest polszczyzną, bo forma nieakcentowana stoi
przy czasowniku, a nie przy rzeczowniku.
Drugi żąda formy nieprzyimkowej, czyli zostawia poza pozycją `niego`, `niej` i `nich`:
`Znam niego cenę.` nie jest polszczyzną tak samo,
a `Bez niego cena rośnie.` jest, bo tam ta forma stoi po przyimku.
Warunek drugi zarabia na siebie właśnie pod przyimkiem, i tylko tam.
Poza nim formę przyimkową odsiewa już morfologia
([wyżej](#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)),
a `bez niego zapisu` ma tę formę po przyimku,
więc odrzuca ją to jedno żądanie i nic poza nim.

Pozycji tej nie ustawiła ani kolejka blokerów
([corpus.md](corpus.md#where-the-analyses-stop)),
ani ranking form bez licencji.
Odrzucenie stało na strukturze, a nie na żadnej z tych form,
bo grupa imienna o jednym zaimku bierze każdą z nich,
więc analiza zatrzymywała się dopiero za zaimkiem:
`Jego skutki są znane.` stawało na `znane`.
Wskazała ją sesja pisząca pod tę gramatykę zdanie po zdaniu.
Ze wszystkiego, co tam zawracało zdanie, ta pozycja zawracała je najczęściej
([pisanie-po-olsku.md](pisanie-po-olsku.md)).

## What it does not cover yet

Every one of these is a sentence that gets rejected and should not be:

- Nawias stojący w środku grupy imiennej:
  `Grupa imienna (ta z dopełniaczem) stoi tu.` jest odrzucone,
  gdzie `Grupa imienna stoi tu (niżej).` wyprowadza się
  i gdzie `Grupa imienna, która stoi (niżej), jest tania.` też,
  bo pozycje nawiasu są dwie i obie zamykają zdanie
  ([wyżej](#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).
- Forma przyimkowa zaimka w drugim członie ciągu pod jednym przyimkiem:
  `Program zapisuje ustawienia dla niego i niej.` jest odrzucone,
  gdzie `Program zapisuje ustawienia dla niego.` wyprowadza się,
  bo licencji udziela tej formie przyimek stojący przed nią
  ([wyżej](#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)).
- Two separating signs in one sentence, whether the same one twice or one of each.
  `Cena jest niska; gramatyka jest bezkontekstowa; parser jest tani.` is rejected
  where either half of it derives,
  and so is a sentence carrying a colon and a semicolon at once.
  Both signs stand at the level of the sentence
  ([above](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
  and `Clause` carries neither, so there is nothing to recurse through.
  What such a production would have to settle is what the second sign separates:
  `(A; B); C` and `A; (B; C)` are the same string
  and a right-recursive body would give it two derivations,
  where the enumeration this register writes with semicolons is one flat list.
- A conjunction opening a sentence, which is what leads the `conj` row
  [corpus.md](corpus.md#where-the-analyses-stop) ranks:
  `I nikt tego nie zauważył.` is rejected
  where the same conjunction between two clauses derives.
  Every one of the three forms leading that row is capitalized,
  and that is the whole of what is left of the row for this construction:
  the comma in front of a conjunction took the lowercase ones
  ([above](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
- Para myślników, czyli wtrącenie w środku zdania:
  `Zepsute miejsce — w prozie czy w kodzie — nie zawsze potrzebuje lepszej wersji.`
  jest odrzucone, gdzie ten sam znak pojedynczy rozdziela dwa zdania
  ([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
  Ten rejestr pisze parę częściej niż znak pojedynczy,
  a pozycja, której ona żąda, jest wtrąceniem w środku zdania składowego,
  gdzie nawias stoi na jego końcu
  ([wyżej](#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).
- Wypełnienie wysunięte przed to, co orzeka bez podmiotu:
  `Programy trzeba czytać.` jest odrzucone,
  gdzie `Trzeba czytać programy.` wyprowadza się,
  i tak samo `Usterkę zgłoszono.` obok `Zgłoszono usterkę.`
  Szyk ma tam sześć wariantów, bo czasownik i podmiot mają je wszystkie,
  a predykatyw stoi w jednym
  ([wyżej](#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika))
  i czasownik nieosobowy w tym samym
  ([wyżej](#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu)).
- Słowa, którymi ten rejestr pyta poza tym jednym zaimkiem:
  `czy`, `kto`, `co`, `jak`, `dlaczego`, `gdzie`.
  `Czy program zapisuje ustawienia?` jest odrzucone,
  gdzie `Który program zapisuje ustawienia?` wyprowadza się,
  a każde z tych słów żąda innego kształtu niż grupa pytajna,
  więc jest to kolejka konstrukcji, a nie jedna pozycja.
  Dwa z tych słów wypadają z tej sekcji, bo nie są odrzucane:
  `Pyta, kto płaci.` wychodzi `valid`, a `Mówi, co robi parser.` wieloznacznie,
  i w obu wypadkach czytanie jest nieprawdziwe.
  Morfeusz czyta `kto` i `co` jako zaimki rzeczowne, a przecinek koordynuje zdania,
  więc pytanie zależne wychodzi ciągiem dwóch zdań współrzędnych,
  w którym zaimek jest podmiotem drugiego.
  Jedno czytanie zdania przeczytanego na opak jest werdyktem najgorszym,
  jaki ten pomiar wydaje
  ([corpus.md](corpus.md#what-morphological-ambiguity-costs)),
  więc te dwa słowa są robotą pilniejszą niż cztery pozostałe;
  `TODO.md` trzyma ruch.
- Liczebnik pisany cyfrą, czyli ten, którym ten rejestr liczy:
  `Termin wynosi 14 dni.` jest odrzucone,
  gdzie `Termin wynosi czternaście dni.` wyprowadza się dwoma czytaniami.
  Cenę i warunek wejścia trzyma
  [cyfry olski nie bierze](#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii),
  a liczebnik rządzący z dopełniaczem pojedynczym — `półtora roku` — stoi poza tym
  z tego samego powodu, z którego mnogi wszedł: rządzi innym przypadkiem.
- `to` as a copula.
  `Kot to zwierzę.` is rejected where `Kot jest zwierzęciem.` derives,
  and the form heads two of the rows
  [corpus.md](corpus.md#where-the-analyses-stop) ranks,
  one of predicatives and one of nominal pronouns,
  which is the ambiguity admitting it has to survive.
- Narzędnik bez przyimka jako pozycja przy czasowniku:
  `Parser mierzy gramatykę sondą.` jest odrzucone,
  gdzie `Parser mierzy gramatykę.` wyprowadza się,
  a `Werdykt przychodzi z czytaniem.` wyprowadza się z przyimkiem przed sobą.
  Olski bierze więc ten przypadek pod przyimkiem i nie bierze go bez niego.
  Jest to ta sama potrzeba, którą nazywa jedyny wpis tej sekcji
  niebędący konstrukcją: pozycja poza biernikiem.
- Człon bez czasownika wtrącony w środek zdania, a nie postawiony na jego końcu:
  `Skład, czyli Morfeusz, jest tani.` jest odrzucone,
  gdzie `Parser jest tani, czyli Morfeusz.` wyprowadza się
  ([wyżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).
  Pozycja jest jedna i stoi na końcu zdania składowego, tak samo jak pozycja
  nawiasu, a wtrącenie w środku jest osobnym ciałem i osobną liczbą,
  której nikt nie policzył; `TODO.md` trzyma ten przebieg.
- Nazwa postawiona przy rzeczowniku bez spójnika:
  `Bank drzew Składnica mierzy gramatykę.` jest odrzucone,
  gdzie `Składnica jest bankiem drzew.` wyprowadza się.
  Ten rejestr nazywa tak każdy artefakt zewnętrzny — korpus Składnica,
  słownik Morfeusz — a od członu bez czasownika różni tę konstrukcję to,
  że spójnika nie ma, więc nie ma czym jej wpuścić bez wpuszczenia zarazem
  dwóch rzeczowników postawionych obok siebie przez pomyłkę.

- Czas przyszły złożony: `Program będzie zapisywał ustawienia.`
  i `Program będzie zapisywać ustawienia.` są odrzucone,
  gdzie `Program zapisuje ustawienia.` wyprowadza się.
  Formy `bedzie` nie bierze żaden terminal,
  a stoi ona nad bezokolicznikiem albo nad formą na `-ł`,
  czyli nad dwiema pozycjami, które gramatyka ma osobno.
- Imiesłów przysłówkowy: `Program zapisuje ustawienia, sprawdzając zgodność.`
  jest odrzucone.
  Jest to trzeci imiesłów obok dwóch, które stoją w
  [przydawce](#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik),
  i różni się od nich gospodarzem: dochodzi do zdania, a nie do rzeczownika.
- Zaimek `siebie`, który słownik trzyma pod częścią mowy tej jednej formy:
  `Reguły odsyłają do siebie.` jest odrzucone,
  gdzie `Reguły odsyłają do dokumentu.` wyprowadza się.
  Stoi on w tej prozie i w banku drzew, a odrzucenie pada w obu na samej formie.

Te trzy wpisy stawia kolejka blokerów
([corpus.md](corpus.md#where-the-analyses-stop)),
a nie przebieg nad prozą ani ranking form bez licencji.
Widać je dlatego, że kolejkę czyta się tu po części mowy, a nie po formie:
`bedzie` niesie jedną konstrukcję na cały wiersz,
więc wiersz nazywa ją wprost,
gdzie `interp` albo `part` grupuje po kilka.

One entry is not a construction but a demand every construction makes:

- **Valency, past the accusative.**
  The lexicon [above](#walencja-jest-leksykonem-o-ramie-domyślnej)
  records which verbs take no accusative object and nothing else,
  so an agreeing predicative and an infinitive still go to every verb,
  and so does the accusative for a lemma Walenty does not carry.
  The infinitive is the position that was measured and left alone,
  and what it waits on is `się` reaching the verb it belongs to
  rather than the one it stands beside.

Słowo, którego słownik nie ma, było tu drugim takim żądaniem i zeszło:
odmianę takiego słowa deklaruje
[leksykon projektu](#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma),
a `Język olski jest podzbiorem polszczyzny.` wyprowadza się i wyprowadza raz.
Słowo bez wpisu wraca dalej jako `ign`,
i jest to wtedy brak wiersza w jednym pliku, a nie brak pozycji w gramatyce.

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
- po każdej z dwóch grup imiennych w czterech pozostałych szykach
  (`Program ustawienia w pliku zapisuje.`)
- po podmiocie w szykach z czasownikiem na czele,
  przed orzecznikiem i za nim
  (`Trwa dochodzenie w tej sprawie.`)
- po orzeczniku wysuniętym przed kopulę i po podmiocie za nią
  (`Wejściem w tym trybie jest zwykły tekst.`)
- przed dopełnieniem, wewnątrz orzeczenia
  (`Program zapisuje w pliku ustawienia.`)
- po czasowniku w szykach z czasownikiem na czele
  (`Trwa w tej sprawie dochodzenie.`, `Zapisuje w pliku program ustawienia.`)
- po rzeczowniku, który już ma przy sobie przymiotnik, dopełniacz albo oba
  (`akcja zbrojna w Strefie Gazy`, `zadania ochrony ludności w gminie`),
  oraz po imiesłowie (`powiązani z interesami postkomunistów`)
- wewnątrz zdania względnego, wokół tego, co w nim zostało:
  po zaimku, między podmiotem a czasownikiem i na końcu
  (`reguła, która w tym trybie rozstrzyga`,
  `polszczyzna, którą ktoś w tym trybie napisał`)
- wewnątrz pytania, w tych samych trzech miejscach za grupą pytajną
  (`Który program w tym trybie zapisuje ustawienia?`)

Wierszy jest dziesięć, a produkcji kilkadziesiąt,
bo pozycja powtarza się w każdym szyku, który ją ma,
a szyk jest w tej gramatyce osobną produkcją.
Ile ich jest dzisiaj, mówi `olski/subset.py`, a nie ten akapit:
rusza je każde dopisanie do gramatyki,
a liczy się je tak, jak się je zdejmuje.
Wiersz kosztuje przez to tym więcej ciał, im więcej szyków go ma,
i to jest w tej gramatyce cena jednego szyku więcej.
Przysłówek dostaje każdą pozycję listy okoliczników za darmo,
bo lista bierze go tak samo jak wyrażenie przyimkowe
([niżej](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe)),
a pytanie kosztuje najwięcej, bo ma własne czoło i własne orzeczenie.
Wiersz ostatni, czyli okolicznik po czasowniku,
ma pozycję w każdym szyku, w którym czasownik stoi przed grupą imienną.
Pozycję wewnątrz zdania względnego i wewnątrz pytania pisze
[rozwinięcie szyku](#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk), a nie ręka,
i jest to jedna pozycja w dwóch konstrukcjach z listy wyżej,
którą gramatyka pisana ręką miała w dwóch ciałach z trzech.
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
bo żaden przebieg jej nie drukuje.

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

## Przysłówek wchodzi każdym gospodarzem, bo dalszy zdejmuje czytania nieprawdziwe

Wyrażenie przyimkowe ma dwóch gospodarzy i oba czytania są prawdziwe,
więc olski oddaje je czytelnikowi.
Przysłówek ma trzech gospodarzy, a nad jednym zdaniem prawdziwy jest jeden z nich:
`bardzo` w `Plik jest bardzo duży.` określa przymiotnik i zdania nie określa,
a `tu` w `Mam tu odmienną interpretację.` określa zdanie i przymiotnika nie określa.
Wybór między gospodarzami jest więc rozstrzygnięciem,
a nie wieloznacznością do zgłoszenia,
i dlatego sonda wyceniła każdego z nich osobno, zanim któryś wszedł do gramatyki.

Weszli wszyscy trzej: gospodarz dalszy kosztuje zdania, a kupuje prawdę o drzewie,
i po tym kursie olski przyjmuje każdego.

Gospodarze są trzej, a wariantów cztery:
gramatyka bez przysłówka, po jednym na gospodarza wycenianego osobno i sam olski.
`okolicznik` wpuszcza przysłówek do listy okoliczników,
czyli tam, gdzie stoi wyrażenie przyimkowe, i przed zdanie.
`przy przymiotniku` stawia go pod symbolem przymiotnika,
a bierze tam sam przysłówek stopniowany
([niżej](#naprawę-niesie-tagset-a-formalizm-ją-bierze)).
Gospodarz trzeci osobnego wariantu nie ma,
bo bez listy okoliczników nie wyprowadza niczego,
więc jego cena nie jest osobną liczbą.

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
jednoznaczności nie traci ani jedno z nich, w żadnym wariancie.
Płaci się ją zakupem pierwszego gospodarza:
zdanie, które każdy z nich osobno przyjmuje jednym czytaniem,
przy obu naraz wychodzi dwoma.

```text
Program zabawy był ściśle ustalony.
```

Pod `okolicznik` orzecznikiem jest `ustalony`, pod `przy przymiotniku`
`ściśle ustalony`, a pod olskim te dwa czytania stoją obok siebie.

Zakupem gospodarza dalszego jest prawda o zdaniach, które zostają.
Pierwszy gospodarz sam wypuszcza jedno na czterdzieści zdań przyjętych
z czytaniem, w którym przysłówek jest okolicznikiem zdania,
choć określa słowo stojące zaraz za nim.
Drugi gospodarz zdejmuje z tych czytań te przed przymiotnikiem,
a trzeci resztę, czyli te przed przysłówkiem,
i po nim nie zostaje ani jedno
([niżej](#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę)).
Zdanie przyjęte z takim drzewem jest droższe od wieloznacznego,
bo `valid` ktoś przeczyta
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
więc każdy gospodarz dalszy zamienia werdykt fałszywy
na werdykt o dwóch czytaniach.
Kurs wychodzi przez to bliski jednemu do jednego:
zdań przyjętych ubywa mniej więcej tyle, ile ubywa czytań nieprawdziwych,
a przy gospodarzu trzecim ubyło jednych i drugich dokładnie tyle samo.

W tę samą stronę idzie zgodność z drzewem wzorcowym.
Okolicznik sam czyta wbrew niemu jedno zdanie na kilkadziesiąt z tych, które kupuje,
a przy gospodarzach dalszych takich zdań jest mniej,
nie tylko w udziale, ale i w liczbie.
Gospodarz trzeci nie rusza przy tym ani jednego z nich:
odbiera jednoznaczność zdaniom czytanym zgodnie z drzewem wzorcowym,
a zdania czytanego wbrew niemu ani nie zabiera, ani nie dokłada.
Drugi gospodarz sam myli się przy tym najczęściej ze wszystkich,
bo czyta wbrew drzewu jedno zdanie na osiem z tych, które kupuje sam:
zostają mu pomyłki na przysłówku odprzymiotnikowym,
który określa i zdanie, więc stopień nie rozdziela niczego —
`Oficjalnie cały Sejm RP śpi.` wychodzi z podmiotem `Oficjalnie cały Sejm RP`.
Ról odwróconych nie ma ani jednej, w żadnym wariancie.

Werdykt nazywa gospodarzy wprost, bo okolicznik przysłówkowy jest w nim rolą:

```sh
python3 -m olski.check --readings -c "Plik jest bardzo duży."
```

```text
<text>: ambiguous Plik jest bardzo duży.
                  2 readings, differing in Adverb, Predicative
                  - Subject: Plik, Predicative: bardzo duży, Verb: jest
                  - Subject: Plik, Predicative: duży, Verb: jest, Adverb: bardzo → jest
0 of 1 sentences are olski, and 1 have a reading
```

Rolę niesie jeden z gospodarzy, i jest to decyzja, a nie przeoczenie.
Przysłówek określający przymiotnik stoi wewnątrz orzecznika albo przydawki,
więc widać go w wypełnieniu tamtej roli,
a wypisany drugi raz obok mówiłby o zdaniu, że ma okolicznik, którego ono nie ma.
Dwa czytania rozdziela przez to sama lista ról,
zamiast czekać na to, że czytelnik porówna dwa napisy orzecznika.

Nad rejestrem ustaw okolicznik kupuje w skali dziesięć razy mniejszej,
a drugi gospodarz dokłada tam zdanie, zamiast odejmować
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
więc znak tej ceny zależy od rejestru,
a nie od samych gospodarzy.
Trzeci nie rusza tam ani jednego werdyktu, tak samo jak nad korpusem audytowym:
przysłówek przed przysłówkiem jest konstrukcją prozy prasowej,
a rejestr, o który olskiemu chodzi, nie pisze jej wcale.

Nad prozą tego repozytorium przysłówek daje wyprowadzenie,
a jednoznaczności nie daje.
Takim zdaniem jest to, o którym kolejka blokerów mówiła,
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
Sam wypuszcza `Program zapisuje ustawienia bardzo szybko.` jednym czytaniem,
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

Liczy to osobne narzędzie, bo pyta o co innego niż pomiar wyżej:
tamten o werdykt, a ten o drzewo, którym werdykt wypadł.
Pełne wiersze drukuje `python3 -m harness.płaski`,
a te sprzed dopisania gospodarzy dalszych — ono z `--wariant okolicznik`.
Populacją są zdania przyjęte jednym czytaniem,
bo tam odpowiedź jest dokładna, a listę czytań zdania wieloznacznego
ucina granica wyliczania.

Klasy są dwie i różni je to, który gospodarz ma brakującą pozycję.
Przysłówek stopniowany przed przymiotnikiem dochodzi do drugiego,
a przed drugim przysłówkiem do trzeciego.
W olskim obie są przez to puste, i to jest zakup tych dwóch gospodarzy
wypisany osobno: przy samym pierwszym przypada na klasę pierwszą
trzy czwarte płaskich czytań, a na drugą reszta.

Liczba wariantu jest przy tym górnym oszacowaniem,
bo przysłówek stopniowany bywa okolicznikiem zdania
i stoi wtedy przed przymiotnikiem, którego nie określa,
jak w `Ostatecznie nowa ustawa wchodzi w życie.`
Które formy to wywołują, wypisuje każda z tych figur, i prowadzi w nich `bardzo`.
Oszacowanie sięga teraz i przysłówka na czele zdania,
bo pod symbolem przysłówka stoi każdy okolicznik przysłówkowy,
a czoło zdania jest osobnym ciałem produkcji:
`Oficjalnie cały Sejm RP śpi.` liczy się przez to razem z resztą,
i to jest jedna z rzeczy, o które ta liczba urosła.
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
