# Open questions

Decisions not yet taken.
The point of writing them down
is that none of them get made by accident.

Questions are grouped by which track they block.

Decyzja, która już zapadła, stoi u właściciela swojego tematu:
rozwidlenia toru gramatycznego trzymają
[decisions taken](design-notes.md#decisions-taken)
oraz [`roadmap.md`](roadmap.md#tor-gramatyczny-nie-ma-końca),
a wycofanie toru linterowego trzyma
[`linter.md`](linter.md#what-closed-the-track).
Pytania, które blokowały wyłącznie tamten tor, zeszły razem z nim,
więc na liście niżej ich nie ma.

## Grammar-track questions

### The rest of the subset

One fork is left, and it is cheaper than the scrambling fork
[a measurement closed](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze).
Olski coordinates noun phrases, adjective phrases and clauses,
and both conjuncts have to be of one category
([subset.md](subset.md#what-the-grammar-covers)),
where Polish also coordinates unlike ones and gaps a repeated verb.
Gapping is the half already taken, and taken as ellipsis rather than as coordination:
a conjunct whose verb this register drops derives
after the conjunctions that admit one
([subset.md](subset.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).
Closeness to Polish argues for the other half,
and what it costs nobody has measured.

### Własność jednoznaczności żąda jej od zdania, które jej nie ma

`Cały wywód prowadzi docs/linter.md.` ma dwa czytania,
SVO i OVS, bo notacja jest nieodmienna, a `wywód` ma biernik równy mianownikowi.
Zdanie naprawdę nie mówi, co tu prowadzi co,
i [subset.md](subset.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)
trzyma to jako cenę przyjętą świadomie.

Dwie rzeczy, każda obroniona osobno, mówią o takim zdaniu co innego.
Zdanie jest olskie wtedy, gdy ma dokładnie jedno czytanie,
i to ta własność czyni olskiego podzbiorem
([subset.md](subset.md#validity-is-uniqueness-not-just-derivability)).
A olski wpuszcza czytania, które polszczyzna naprawdę ma, OVS wśród nich,
bo deklaracja, że pierwsza grupa imienna jest podmiotem,
czytałaby się jednoznacznie tylko temu, kto zna konwencję
(tamże).
Zdanie wieloznaczne w polszczyźnie wychodzi więc odrzucone
za wieloznaczność, którą naprawdę ma,
a autor nie ma z takim werdyktem co zrobić,
bo drugie czytanie nie jest usterką jego zdania.

Żadnemu tekstowi to żądanie przy tym nie ciąży,
bo kryterium wyjścia toru gramatycznego nie ma
([roadmap.md](roadmap.md#tor-gramatyczny-nie-ma-końca)),
więc zostaje pytanie o sam werdykt: czy taki jest dla autora użyteczny.
Wyjściem, którego to pytanie szuka, jest werdykt, który tę klasę nazywa,
czyli mówi „dwa czytania i polszczyzna ma tu dwa”, a nie samo „dwa czytania”.
Kosztem jest to, czego program nie wyda:
dla każdego zdania spornego ktoś musi powiedzieć, ile czytań ma sam.

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

Pozycję którejś z dwóch klas niesie tam 747 z 1 183 zdań, czyli 63.1%:
przyłączenie 56.0%, synkretyzm 21.0%,
a 278 zdań niesie samych przyłączeń dwa albo więcej,
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
ani jedno nie zostawia czytelnika z dwoma rozumieniami.
Zdania przyłączeniowe mają dwa drzewa i jedno rozumienie:
`kompendium wiedzy dla deweloperów` przyłącza się do rzeczownika,
bo przy czasowniku nie znaczyłoby nic innego,
i tak samo `skrót SHA-256 w Base64`.
Po stronie synkretyzmu osiem z dwunastu zdań stoi na grupie,
która podmiotem nie stanęłaby wcale:
`w odpowiedzi` i `od ostatniej wysyłki` stoją pod przyimkiem,
`Element report` jest apozycją,
a `te`, `sam` i `niż` są czytaniami, których polszczyzna w tym miejscu nie ma —
czyli tą samą klasą, którą wylicza akapit o górnym oszacowaniu niżej.
Zostają cztery, w których obie grupy naprawdę stoją do wyboru,
i w żadnej z nich czytelnik się nie waha:
`Niniejszy dokument stanowi kompendium wiedzy` czyta się raz,
bo kompendium dokumentu nie stanowi.
Jest to jedna osoba nad dwudziestoma czterema zdaniami, a nie pomiar,
i tyle z tego wynika.

Wniosek wychodzi odwrotny do tego, na co 63.1% wygląda.
Werdykt, którego to pytanie szuka, objąłby zdania rzadkie, a nie większość rejestru,
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
Podnosi ją też każde czytanie, które słownik ma, a polszczyzna nie.
Wykluczenie ze słownika sięga po nie tam, gdzie czytanie jest nieodmienne
([subset.md](subset.md#the-dictionary-offers-readings-polish-does-not)),
więc pary `go` i `gov.pl` ta liczba już nie niesie,
a `sam` czytany sklepem zostaje w niej, bo sklep odmienia się jak rzeczownik.
Osobno stoi to, co dokłada ekstrakcja:
nagłówek sklejony ze zdaniem za nim daje parę, której nikt nie napisał,
i należy to do [extraction.md](extraction.md), a nie tutaj.
Wszystkie te klasy podnoszą populację,
a wniosek wyżej idzie w tę samą stronę co one, więc żadna go nie odwraca.
Zbiera się ich przy tym najwięcej pod synkretyzmem,
więc to jego 21.0% jest z dwóch liczb tą miękką.

Dwa węższe kryteria synkretyzmu zmierzono, każde zdejmuje jedno zdanie z 250,
i zdejmują dwa różne zdania z dwóch różnych powodów.

Pierwsze żąda mianownika i biernika od jednego lematu.
Bez tego żądania mianownik wolno wziąć z jednego wpisu, a biernik z drugiego,
więc forma liczy się jako dwa słowa naraz:
`Paczka` ma mianownik od `paczka`, a biernik od nazwiska `Paczek`.
Kryterium to zdejmuje trafienie tego rodzaju i nie zdejmuje ani jednego zdania,
bo w tym zdaniu pozycja stoi jeszcze na `niż` i `MB`;
kosztuje natomiast grupowanie czytań po lemacie, którego warunek szerszy nie ma.

Drugie żąda zgody z orzeczeniem od obu czytań, a nie od mianownikowego samego.
Zgoda od mianownika samego jest tym, co stoi, i stoi na powodzie, a nie na liczbie:
podmiot wyciąga z orzeczenia formę, a dopełnienie jej nie wyciąga,
więc liczba dopełnienia nie ma z czym się nie zgodzić,
i forma o mianowniku pojedynczym i bierniku mnogim staje przy `posiada` w obu rolach.
Liczba idzie tu przy tym w drugą stronę niż powód, i warto to zapisać:
jedyne zdanie, które warunek szerszy tym zatrzymuje,
zatrzymuje przez `jeden` czytane jako rzeczownik męskozwierzęcy w mianowniku
obok liczebnika mnogiego w bierniku,
czyli przez dwa czytania, których polszczyzna w tym miejscu nie ma.
Powód zostaje, bo jest o polszczyźnie, a nie o tym korpusie,
a to jedno trafienie należy do klasy wyliczonej wyżej i tak samo jak ona liczbę podnosi.

Oba warianty mierzy się podstawieniem pod `_obojętny` w `olski/wieloznaczność.py`,
bo sondy na nie nie ma i jedno zdanie jej nie kupuje.

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
Odpowiedzi są trzy, a pierwsza jest wzięta.
Wzięta: własność jednoznaczności zostaje, jak stoi,
a kryterium wyjścia toru gramatycznego znika,
bo nad tym README nie było osiągalne
i było przez to kryterium innego rodzaju, niż je opisano
([roadmap.md](roadmap.md#tor-gramatyczny-nie-ma-końca)).
Zostaje po nim to, co ta decyzja przyznaje:
zdanie tego rejestru z pozycją przyłączeniową jest odrzucane
i nie ma po czym poznać, że kiedyś przestanie.
Druga: wraca [wyjście drugie z etapu 1](subset.md#dlatego-olski-przyjmuje-koszt),
czyli domyślne przyłączenie, odrzucone tam za to, że myli się dwa razy częściej,
niż trafia; wobec tego pomiaru trzeba by je ważyć inaczej niż wtedy,
bo po jednej stronie stoi pomyłka w drzewie, której czytelnik nie zauważa,
a po drugiej odrzucenie zdania, które przeczytał raz.
Trzecia: warstwa rozstrzygająca przyłączenie poza gramatyką,
czyli to, czego żaden etap nie planuje.
Ile taka warstwa miałaby do rozstrzygnięcia, z jaką skutecznością robią to cudze maszyny
i dlaczego reszty nie rozstrzyga nic, co stoi w zdaniu,
wycenia [disambiguation.md](disambiguation.md),
i tam też stoi zalążek, który nie rusza werdyktu.

Do przeczytania jest najpierw to, czy próbka wyżej się broni.
Dwadzieścia cztery zdania przeczytane przez jedną osobę
są podstawą wystarczającą, żeby pytanie postawić,
i za wąską, żeby na nim stanąć.

Odwrotną stronę tej pary — wieloznaczność, którą ma czytelnik, a werdykt jej nie melduje —
opisuje [disambiguation.md](disambiguation.md#wieloznaczność-której-werdykt-nie-melduje),
i to ona prowadzi do pytania niżej.

### Warstwa kontekstowa zabiera werdyktowi jednostkę

Werdykt olskiego jest o zdaniu: zdanie jest olskie, gdy ma dokładnie jedno czytanie.
Warstwa zdejmująca czytanie, któremu przeczy zdanie sąsiednie
([disambiguation.md](disambiguation.md#kontekst-rozstrzyga-wykluczeniem-a-nie-rankingiem)),
odpowiada o zdaniu na swoim miejscu, a to jest inna jednostka i inna obietnica.
Dwie rzeczy z niej wychodzą i obie widać, zanim ktokolwiek taką warstwę napisze.
`olski-check -c`, które dostaje zdanie bez sąsiedztwa,
przestaje mówić to samo, co przebieg nad plikiem, w którym to zdanie stoi.
A przestawienie akapitu rusza werdykt nad zdaniem, którego nikt nie ruszył,
czyli autor traci pewność, że odpowiedź zależy od zdania, które napisał.

Wyjścia są dwa i wzięte jest to, które niczego nie rozstrzyga.
Pierwsze zostawia jednostkę przy zdaniu, a warstwę stawia obok werdyktu,
i tak stoi `Powtórzenie` w `olski/rozstrzyganie.py`:
werdykt dalej mówi „dwa czytania”, a wiersz pod nim mówi, przy czym ta fraza już stała.
Kosztem jest zdanie, które w swoim tekście czyta się raz, a mimo to zostaje odrzucone,
i tego kosztu nie zdejmuje żaden świadek dopisany po tamtej stronie.
Drugie zmienia jednostkę i wraz z nią obietnicę parsera,
który mówi wtedy o tekście, a nie o zdaniu, i płaci obiema rzeczami wyżej.

Do przeczytania jest, czy druga cena nie jest już zapłacona po drugiej stronie.
`olski/skład/przegląd.py` mierzy napis w tym kontekście,
którym linearyzacja go składała, bo to on rozstrzyga, jakim napisem zdanie wyszło,
i zdanie mierzone osobno nazywa wprost innym zdaniem.
Jeśli po tamtej stronie jednostką jest zdanie na swoim miejscu,
to zmiana jednostki po tej wyrównuje oba kierunki, zamiast wyłamywać jeden.

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
[subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie) robi dla całego zdania.

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

Torowi gramatycznemu odpowiedź daje drugie uzasadnienie kryterium jednoznaczności
albo nie daje żadnego,
a miara po prefiksach i tak potrzebuje rozbioru,
więc pytać o nią umie tylko ten tor.

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

Co ranking nad takim lasem osiąga tam, gdzie ktoś go zbudował i zmierzył,
i dlaczego skłonność jest tu dalej „nie”,
wycenia [disambiguation.md](disambiguation.md#ranking-nie-jest-wyjściem-którego-ten-parser-potrzebuje).

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
and only the grammar track would produce one.

The scheme would let olski state its position
on the same four axes as a hundred other controlled languages.
Doing so honestly requires
an exact and comprehensive language description,
which is the Simplicity axis by definition.
Committing to that is committing to write the spec properly.
It might be the most valuable artifact the grammar track could produce,
or an obligation that kills the fun.
Undecided.

## Shared questions

**Implementation language.**
Both tracks need one, and it need not be the same one.

- The grammar track wants good algebraic data types
  and pattern matching for writing Earley and a unifier,
  and Morfeusz has usable Python and C++ bindings.
- The skład track wants the same thing for the same reasons,
  and it is written against the same analyser read backwards.
- The project is for fun,
  so enjoying the language matters more than it usually would.

**Tezaurus.**
Podmiana synonimu ([roadmap.md](roadmap.md#cele)) żąda słów bliskoznacznych,
a repozytorium nie ma ich w żadnej postaci:
Morfeusz wydaje formy i lematy, Walenty schematy,
i żadne z dwojga tezaurusem nie jest.
Kandydatem jest plWordNet, nazwany już przy pytaniu o to,
[czym rozstrzygnąć znaczenie czasownika](disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma),
i jedno źródło obsłużyłoby oba pytania albo żadnego.
Pytanie ma trzy części: czy licencja pozwala na użycie w tym repozytorium,
czy relacja synonimii wychodzi na lematy, którymi ten rejestr mówi,
i czy da się ją odsiać tym, co już czytamy —
rodzajem i aspektem z Morfeusza, schematem z Walentego, kwalifikatorem ze słownika.
Bez odpowiedzi cel nie upada, tylko czeka:
sprawdzian ma — drzewo, które po podmianie ma wrócić to samo —
a nie ma czym podmieniać.

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
