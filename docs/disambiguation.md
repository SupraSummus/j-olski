# Ujednoznacznianie: co miałoby rozstrzygać i za ile

Olski odrzuca zdanie, które ma więcej niż jedno czytanie,
i oddaje czytania autorowi zamiast wybierać za niego
([README](../README.md)).
Ten dokument pyta, co by się stało, gdyby jednak wybierał:
czym są wybory, które olski zostawia otwarte,
ile z nich rozstrzygnęłaby maszyna postawiona za parserem
i jaką skuteczność takie maszyny osiągają tam, gdzie ktoś je zbudował i zmierzył.

Odpowiedź krótka jest taka, że pytanie rozpada się na trzy,
a tylko jedno z nich jest o wyborze czytania.
Trzy czwarte tego, co olski odrzuca nad bankiem drzew,
zostawia dokładnie jedną decyzję: dokąd dochodzi wyrażenie przyimkowe.
Zadanie to pole mierzy od trzydziestu lat, na własnych zbiorach i z rozbiorem błędów,
a pomiar mówi dwie rzeczy naraz:
najlepsze modele podchodzą pod sufit,
a sufit leży wyraźnie poniżej stu procent,
bo część tych decyzji rozstrzyga zdanie poprzednie,
a część nie jest decyzją wcale, bo oba czytania mówią to samo.

Dokument opisuje wobec tego cenę, a nie plan.
[roadmap.md](roadmap.md#tor-gramatyczny-nie-ma-końca) żadnego etapu na to nie ma,
a `olski/rozstrzyganie.py` jest zalążkiem stojącym obok werdyktu i nie ruszającym go:
[co on robi i ile trafia](#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
opisuje sekcja pod wywodem, z którego jego kształt wynika.

Trzy pytania niżej są o czytaniach, które las trzyma,
a zdanie niesie jeszcze wieloznaczność, która do lasu nie dochodzi:
`Wynajmę mieszkanie.` olski przyjmuje i mówi o nim „one reading”,
a wynajmuje w nim raz właściciel, raz lokator.
Klasa ta wraz z tym, co miałoby ją zdejmować, opisana jest
[niżej](#wieloznaczność-której-werdykt-nie-melduje), za wywodem o czytaniach,
bo dopiero on mówi, czego warstwie kontekstowej robić nie wolno.

## Pytanie rozpada się na trzy i tylko jedno jest o rankingu

Trzy pytania stoją pod jednym słowem, każde ma inny wynik i inną cenę.

**Które czytanie jest tym, o które autorowi chodziło.**
To jest ranking, czyli maszyna, która porządkuje las i zwraca pierwsze czytanie.
Wzorcem odpowiedzi jest drzewo wybrane przez anotatora,
więc jest to zadanie z bankiem drzew pod spodem.

**Czy dwa czytania mówią to samo.**
To jest tożsamość czytania, a nie wybór między nimi.
Wzorcem odpowiedzi jest sąd o znaczeniu,
którego żaden bank drzew nie zapisuje,
bo anotator wybierał drzewo, a nie orzekał o parze drzew.

**Czy czytelnik widzi tu wybór.**
To jest pytanie o człowieka nad zdaniem, a nie o zdanie.
Wzorca nie ma nigdzie
i [czego by trzeba, żeby powstał](#czego-brakuje-żeby-odpowiedzieć-pomiarem),
stoi na końcu tego dokumentu.

Reszta dokumentu bierze je po kolei.
Pierwsze jest drogie i zmierzone, drugie tanie i częściowo już zrobione,
a trzecie jest tym, po co olski istnieje,
więc maszyna, która by na nie odpowiadała za czytelnika, kasuje ten parser.

## Ranking zmierzono, a skuteczność spada z wielkością lasu

Ranking nad lasem gramatyki pisanej ręcznie
ma w polu dwadzieścia parę lat pomiarów, i to na tej samej architekturze,
o którą tu chodzi: gramatyka wydaje wszystkie czytania,
osobny model statystyczny wybiera jedno.

Liczbą, która mówi najwięcej, jest ta z pierwszego przebiegu nad Redwoods,
bo rozbija skuteczność po wielkości lasu, zamiast podawać średnią.
Gramatyką jest angielska ERG, modelem PCFG nad drzewami wyprowadzenia,
a trafieniem całe drzewo, nie krawędź:

| czytań w zdaniu | zdań | losowo | model |
| --- | --- | --- | --- |
| ≥ 2 | 3 824 | 25,8% | 74,0% |
| ≥ 5 | 1 789 | 9,7% | 59,6% |
| ≥ 10 | 1 027 | 5,3% | 51,6% |
| ≥ 20 | 525 | 3,0% | 45,3% |

Model dyskryminacyjny postawiony później na tym samym korpusie
podniósł średnią do około 76%,
i to jest najwyższa liczba tego rodzaju, jaką ten przegląd znalazł.
Świgra, czyli najbliższy istniejący parser polszczyzny,
ma taki komponent od dawna
([swigra.md](swigra.md#what-świgra-occupies)),
a ujednoznacznianie jej lasów sposobem bliskim PCFG
zmierzono nad Składnicą na 94,1% F-miary PARSEVAL i 92,1% ULAS.
Alpino, gramatyka niderlandzkiego z modelem maksymalnej entropii,
rozstrzyga według własnego opisu około 80% decyzji.

Dwie z tych liczb mierzą co innego niż trzy pozostałe i to jest w nich mylące.
94,1% i 92,1% liczą się po krawędziach albo po nawiasach,
czyli mówią, jaka część drzewa się zgadza.
Olski nie wydaje werdyktu o krawędzi.
Werdykt jest o zdaniu, więc miarą jest całe drzewo,
a tam liczby wyglądają jak w tabeli wyżej: od 74% w dół, wraz z lasem.
Zdania, o które olskiemu chodzi, są przy tym dokładnie tymi z dolnych wierszy,
bo o zdaniu z jednym czytaniem nie ma czego pytać.

### Nad Składnicą olski ma ranking, którego nikt nie trenował

Punktem odniesienia dla każdej takiej maszyny
jest to, co ten parser oddaje za darmo.
Las wydaje czytania w kolejności ustalonej przez `ciała` w `olski/parse.py`,
a kolejność ustalona jest rankingiem,
tyle że takim, który nie widział ani jednego drzewa wzorcowego.
Nad zdaniami, które olski odrzuca za wieloznaczność,
złote czytanie jest w tej kolejności pierwsze w 312 wypadkach,
i liczbę tę wraz z jej mianownikiem trzyma
[corpus.md](corpus.md#złote-czytanie-ocalało-w-437-z-478-zdań-wieloznacznych).
Wobec wszystkich 478 zdań, o które to pytanie da się zadać,
jest to 65,3% trafień czytaniem pierwszym.

Tyle ma do pobicia model, który miałby tu stanąć.
Liczba jest przy tym łagodniejsza dla modelu, niż wygląda,
bo mierzy zgodność dwóch ról, a nie całego drzewa
(tamże), więc mierzy mniej niż 74,0% z tabeli wyżej.
Rzędu wielkości to nie rusza:
architektura, o którą tu chodzi, startuje z dwóch trzecich zrobionych,
i to jest ta część pytania, o której najłatwiej zapomnieć.

## Czym różnią się czytania, które olski odrzuca

Zanim wiadomo, ile ranking kosztuje, trzeba wiedzieć, co miałby rozstrzygać.
Odpowiada na to sonda nad Składnicą, ściągniętą tak, jak mówi
[corpus.md](corpus.md#fetching-it):

```sh
python3 -m sonda.czytania Składnica-frazowa-180723/
```

Klasy bierze z tego, co werdykt o zdaniu wypisuje,
a nie z osobnej klasyfikacji napisanej obok:
`rola` znaczy, że czytania obsadzają różnie którąś z ról,
`przyłączenie`, że gospodarz modyfikatora zostaje nierozstrzygnięty,
`konstytuent`, że różnica leży tam, gdzie streszczenie nie zagląda.
Klasę da się więc sprawdzić, czytając werdykt nad zdaniem.
Nad 549 zdaniami, które olski odrzuca za wieloznaczność:

| co werdykt nazywa | zdań | |
| --- | --- | --- |
| rola + przyłączenie | 463 | 84,3% |
| przyłączenie | 33 | 6,0% |
| sama liczba czytań | 23 | 4,2% |
| rola | 18 | 3,3% |
| rola + przyłączenie + konstytuent | 7 | 1,3% |
| konstytuent | 5 | 0,9% |

Tabela liczy nazwy, a nie decyzje, i te dwie rzeczy się rozchodzą.
`Czeka koń z furą.` ma jedno przyłączenie i różni się rolą,
bo podmiotem jest raz `koń z furą`, a raz `koń`:
rola rusza się dlatego, że rusza się przyłączenie, więc decyzja jest jedna.
`Koszt samej szynki przewyższa koszt szynki z dodatkami.` ma dwie decyzje naraz,
bo szyk odwraca się niezależnie od tego, dokąd dochodzi `z dodatkami`.
Rozdziela je iloczyn:
przyłączenie o dwóch gospodarzach mnoży las przez dwa,
więc gdy iloczyn gospodarzy równa się liczbie czytań,
innej decyzji ten las nie zostawia.

**Tak liczone przyłączenie jest całą decyzją w 412 z 549 zdań, czyli w 75,0%.**
W klasie `rola + przyłączenie` jest to 385 z 463, a w klasie `przyłączenie` 27 z 33.
Liczba jest górnym oszacowaniem i myli się w jedną stronę,
bo dwa przyłączenia, z których jedno ma gospodarza tylko pod jednym czytaniem drugiego,
dają czytań mniej niż iloczyn;
`całe_przyłączenie` w `sonda/czytania.py` mówi to o sobie samo.

Cała reszta rozkłada się na dwie rzeczy, z których żadna nie jest zadaniem dla rankingu.

Pierwsza to czytanie, którego polszczyzna nie ma.
`Trwa akcja protestacyjna.` wychodzi dwoma czytaniami,
bo `protestacyjna` czyta się raz jako przydawka, a raz jako orzecznik,
a orzecznika w tym miejscu polszczyzna nie stawia.
Nie jest to wieloznaczność do rozstrzygnięcia, tylko nadgeneracja do zdjęcia,
i tym zajmuje się [etap 3](roadmap.md#etap-3-czytania-których-polszczyzna-nie-ma),
a nie żadna warstwa za parserem.

Druga to 23 zdania, nad którymi werdykt nie mówi nic poza liczbą czytań.
`Tata musiał pojechać do domu.` ma dwa czytania,
bo `do domu` dochodzi do formy osobowej albo do bezokolicznika za nią,
a oba czytania mówią o tym samym.
Jest to ta sama pomyłka, którą
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
opisuje w cudzym systemie —
liczenie prób zamiast wyników — tyle że w postaci węższej,
bo tu wyprowadzenia naprawdę różnią się kształtem, a nie samym nawiasowaniem.
Co dokładnie ten wiersz werdyktowi odbiera i jaki ruch go naprawia,
trzyma [`TODO.md`](../TODO.md).

## Ranking nie jest wyjściem, którego ten parser potrzebuje

Liczby wyżej mówią, że ranking nad tym lasem jest do zbudowania
i że stanie gdzieś między dwiema trzecimi a trzema czwartymi trafień.
Osobne jest pytanie, co olski dostaje, gdy go weźmie, i odpowiedź jest ujemna.

Ranking zamienia werdykt `ambiguous` na `valid` wraz z domysłem.
Zdanie, o którym parser dziś mówi „dwa czytania, oto one”,
mówiłoby wtedy „jedno czytanie”, i myliłoby się co trzecie albo co czwarte.
Własność, która czyni olskiego podzbiorem, jest właśnie tym, że tego nie robi
([subset.md](subset.md#validity-is-uniqueness-not-just-derivability)),
a odrzucenie konwencji SVO i odrzucenie domyślnego przyłączenia
stały na tym samym zarzucie z liczbą pod spodem:
konwencja, która myli się dwa razy częściej, niż trafia,
nie jest konwencją, którą czytelnik ma
([subset.md](subset.md#dlatego-olski-przyjmuje-koszt)).
Ranking trafiający w dwóch trzecich jest tym samym zarzutem złagodzonym,
a nie zdjętym.

Zostaje jedno zastosowanie, przy którym ten zarzut nie powstaje,
bo werdykt zostaje taki, jaki jest.
Czytań wypisuje się najwyżej `MAX_READINGS`,
a kolejność, w jakiej wychodzą, rozstrzyga, które autor zobaczy.
Ranking postawiony tam porządkuje listę i nie dotyka odpowiedzi,
więc kosztuje tyle, ile waży, i nie kosztuje ani jednego werdyktu.
Czy to warte modelu trenowanego na banku drzew, ten dokument nie rozstrzyga;
[open-questions.md](open-questions.md#the-round-trip-guarantee)
trzyma pytanie o ranking wraz z notowaną tam niechęcią do budowania go.

## Tożsamość czytania jest tańsza i częściowo już stoi

Drugie z trzech pytań nie potrzebuje modelu ani banku drzew.
Dwa wyprowadzenia są jednym czytaniem, kiedy mają ten sam kształt,
a co do kształtu nie wchodzi, rozstrzyga `signature` w `olski/parse.py`
i opisuje [subset.md](subset.md#co-się-liczy-jako-jedno-czytanie):
lematy, wartości cech i część mowy są wyłączone rozmyślnie.
Każde takie wyłączenie to wieloznaczność, która przestała być raportowana,
zdjęta deterministycznie i bez ani jednego wyboru między czytaniami.
Tą samą drogą idą 23 zdania z klasy „sama liczba czytań”.

Pole nazywa to samo z drugiej strony i wycenia wysoko.
W najlepszym zmierzonym modelu przyłączenia dla niemieckiego
przeczytano ręką sto błędów:
36 z nich to wypadki, w których oba przyłączenia dają to samo rozumienie,
a wzorzec zaznaczał jedno z nich.
Autorzy liczą je jako usterkę zbioru danych, a nie modelu,
i stąd bierze się ich oszacowanie sufitu zadania na około 92,6%.
Trzecia część tego, czego nie umie najlepszy model,
nie jest więc pytaniem, na które istnieje odpowiedź.

Tradycja, która na to odpowiada wprost, nazywa się niedookreśleniem:
zamiast wybierać czytanie albo je mnożyć,
buduje się jedną reprezentację, która o spornym miejscu nie mówi,
i rozstrzyga się je dopiero wtedy, gdy ktoś pyta.
Minimal Recursion Semantics jest jej najczęściej używaną postacią.
Dla olskiego znaczyłoby to grubszą sygnaturę czytania, a nie nową warstwę,
i jest to jedyny z trzech kierunków tego dokumentu,
który nie łamie niczego, na czym ten parser stoi.

Cena też jest znana i jest to cena po drugiej stronie.
Sygnatura, która zwija za dużo, każe olskiemu przyjąć zdanie,
które naprawdę ma dwa czytania,
a tego po werdykcie nie widać — dokładnie tak,
jak nie widać zdania przyjętego dlatego, że drugie czytanie żądało nieciągłości
([design-notes.md](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)).
Każde zwinięcie trzeba więc uzasadnić parą czytań, nad którą nikt nie waha się,
że mówią to samo, a nie tym, że liczba spadła.

## Leksykon rozstrzyga część i rozstrzyga ją deterministycznie

Trzy czwarte odrzuceń to przyłączenie,
a części tych przyłączeń nie rozstrzyga się rankingiem, tylko słownikiem.
Nad Składnicą 576 z 4 517 spornych wyrażeń to frazy, których czasownik żąda swoim schematem,
a 214 to frazy, których żąda sam rzeczownik;
liczby te wraz z ich rozkładem trzyma
[subset.md](subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia).
Po żadnej z tych stron nie ma konkurencji między czytaniami:
przeczytanie frazy wymaganej po drugiej stronie łamie schemat tego, kto jej żądał.

Olski taki leksykon ma i sięga nim płycej, niż ta klasa wymaga.
`olski/leksykon.txt` mówi o bierniku i o bezokoliczniku, a nie o przyimku
([subset.md](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
a Walenty, z którego ten plik powstaje, ma ramy także dla rzeczownika i przymiotnika.
Ruch jest więc jednym rozszerzeniem generatora, a nie nową maszyną,
i mieści się w tym, co [etap 2](roadmap.md#etap-2-walencja) już obejmuje.
Rozstrzygnięcie, które z niego wychodzi, jest deterministyczne i da się wyjaśnić
jednym wierszem leksykonu, czyli jest tym rodzajem odpowiedzi,
którą ten parser obiecuje w README.

Ile z tych 75% by to zdjęło, ten dokument nie mówi,
bo obie liczby wzięto nad innymi mianownikami:
790 z 4 517 to wyrażenia, a 412 z 549 to zdania,
i jedno zdanie niesie ich czasem kilka.
Pomiar, który by to złożył, jest jedną z rzeczy, których tu brakuje.

## Reszty nie rozstrzyga nic, co stoi w zdaniu

To, co zostaje po zwinięciu czytań tożsamych i po leksykonie,
nie jest zadaniem trudniejszym tego samego rodzaju.
Jest zadaniem innego rodzaju, bo informacja rozstrzygająca leży poza zdaniem.

Najczystszy dowód pochodzi z niderlandzkiego,
gdzie zdanie względne czyta się podmiotowo albo dopełnieniowo,
czyli tak samo jak polski synkretyzm mianownika z biernikiem.
`de dokter die de patiënt geneest` to „lekarz, który leczy pacjenta”
albo „lekarz, którego leczy pacjent”,
a rozstrzyga o tym zdanie postawione przed nim:
po „pacjent wyleczył lekarza” czyta się je drugim sposobem.
Praca, która to bada, pokazuje przy tym,
że parsery oparte na modelu językowym niosą w tym miejscu wyuczone przechylenie
i że kontekst zmienia ich odpowiedź trudniej, niż zmienia odpowiedź czytelnika.

Ten sam wniosek wychodzi z drugiej strony w pomiarze niemieckim:
ze stu błędów najlepszego modelu 13 wymaga analizy na poziomie tekstu,
a autorzy piszą wprost, że dopóki przyłączenie i parsowanie
są zadaniami nad zdaniem, te wypadki są nierozstrzygalne.
Trzecia liczba wycenia to samo od strony człowieka:
człowiek pokazany samą czwórką słów
— czasownik, rzeczownik, przyimek, rzeczownik —
trafia w 88,2%, a pokazany całym zdaniem w 93,2%.
Pięć punktów różnicy to jest dokładnie to, czego czwórka nie niosła,
a zdanie niesie; o tym, czego nie niesie zdanie, ten pomiar nie mówi nic,
bo nikt nie pokazywał tam akapitu.

Wniosek jest więc taki, że ujednoznacznianie na poziomie zdania ma sufit,
że sufit jest poniżej 93% na jedno przyłączenie
i że nad zdaniem z dwoma przyłączeniami spada wykładniczo —
a takich jest 123 z 549.
Powyżej sufitu nie ma modelu, jest budowanie kontekstu,
czyli zadanie, którego ten parser nie stawia i którego wykonania nie umiałby wyjaśnić.

Olski ma przy tym poziom nad zdaniem i ma go po drugiej stronie.
Opowieść w `olski/skład/` wie to, czego zdanie samo o sobie nie wie:
kiedy to było i o kim mowa była przed chwilą,
i z tego bierze czas przeszły oraz podmiot opuszczony
([sklad.md](sklad.md)).
Kierunek parsujący takiego poziomu nie ma:
`olski/document.py` dzieli tekst na zdania i każde oddaje gramatyce osobno.
Warstwa rozstrzygająca kontekstem byłaby więc drugim kompilatorem,
a nie filtrem za pierwszym, i to jest cena, której żaden z tych pomiarów nie liczy.

## Zalążek stoi obok werdyktu i nazywa swoją częstość pomyłek

`olski/rozstrzyganie.py` jest tej warstwy zalążkiem
i jest w repozytorium po to, żeby kierunek dał się zmierzyć,
a nie żeby zdania rozstrzygać.
Trzy rzeczy z wywodu wyżej są w nim wzięte wprost,
a pod nimi stoi opis dwóch świadków, których ta warstwa ma.

**Werdykt zostaje nietknięty.**
`rozstrzygnij` bierze przyłączenia z gotowego wyniku rozbioru
i oddaje odpowiedź obok niego,
więc `valid`, `ambiguous` i `rejected` znaczą po jej dopisaniu to, co znaczyły.
`olski-check --rozstrzygaj` wypisuje ją pod werdyktem, ze znakiem zapytania na przedzie:

```sh
python3 -m olski.check --rozstrzygaj -c "Daj przepis na faworki."
```

```text
<text>: ambiguous Daj przepis na faworki.
                  2 readings, differing in Object; „na faworki” → „Daj”, „przepis”
                  ? „na faworki” → „przepis”: „na” przy „przepis” doszło tam w 4 z 4 wypadków banku drzew, 100%
```

**Jednostką jest świadek, a nie model.**
Świadek patrzy na jedno przyłączenie i albo wskazuje gospodarza wraz z powodem, albo milczy,
a milczenie jest odpowiedzią domyślną i pełnoprawną.
Świadkowie idą w kolejności rodzaju dowodu i pierwszy odpowiadający wygrywa,
więc dowód o tym tekście bije dowód o cudzym korpusie wszędzie tam,
gdzie oba mówią coś naraz.
Powód wraca razem ze wskazaniem, żeby wskazanie dało się sprawdzić bez zaglądania do tabeli.

**Świadkowie są dwaj i żaden nie jest tym, którego ten wywód wycenia najwyżej.**
Tożsamość czytania i leksykon są tańsze i obie sekcje wyżej tak je wyceniają,
a nie ma ich tutaj z powodów, które te sekcje podają:
pierwsza czeka na sąd o parze czytań, którego żaden korpus nie zapisuje,
a druga na kolumnę, której `olski/leksykon.txt` nie ma.
Dwaj, którzy stoją, są tymi, których da się zbudować z tego, co w repozytorium już jest,
i stąd kolejność odwrotna do ceny.

**Świadek kontekstowy odpowiada powtórzeniem.**
`Powtórzenie` szuka w akapicie miejsca, w którym ta sama fraza stała już
przy którymś z gospodarzy, i wtedy wskazuje tego gospodarza:

```sh
python3 -m olski.check --rozstrzygaj -c "Wystąpiła awaria w systemie. Operator zgłosił awarię w systemie."
```

```text
<text>: ambiguous Wystąpiła awaria w systemie.
                  2 readings, differing in Subject; „w systemie” → „Wystąpiła”, „awaria”
<text>: ambiguous Operator zgłosił awarię w systemie.
                  2 readings, differing in Object; „w systemie” → „zgłosił”, „awarię”
                  ? „w systemie” → „awarię”: „w systemie” stało już przy „awaria” wyżej w tekście: „Wystąpiła awaria w systemie.”
0 of 2 sentences are olski
```

Dowodem jest powtórzenie, a nie znajomość rzeczy.
Fraza, którą autor postawił przy tym gospodarzu zdanie wcześniej,
jest w tym tekście jego opisem, bo już raz nim była.
Sąsiedztwo, które rzecz tylko wprowadza, mówi mniej:
po `Mamy nowy system.` świadek milczy i zostawia to zdanie tabeli.
Reguła, która by tam odpowiadała — rzecz raz wprowadzona jest znana,
więc fraza nie identyfikuje rzeczownika i dochodzi do czasownika —
odpada na kontrprzykładzie, a nie na ostrożności:
po `Widziałem hasła.` fraza `z hasłami` dalej dochodzi do `plik`.

Zdanie tego przykładu polszczyzna naprawdę czyta dwojako:
awaria jest w systemie albo zgłoszenie w nim padło,
i oba są w rejestrze dokumentacji zwykłe.
Fraza z `z` i narzędnikiem tego nie daje i przykładu z niej tu nie ma.
`Widzę człowieka z lornetką.` jest kalką ze zdania angielskiego,
bo polskie `z` wyraża towarzyszenie, a nie narzędzie —
narzędziem widzenia jest `przez lornetkę` — więc czytelnik ma tam jedno czytanie,
a dwa, które olski nad tym zdaniem melduje, są nadprodukcją gramatyki
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)),
czyli klasą, którą trzyma
[open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma).
Świadek postawiony na takim zdaniu pokazuje mechanizm i nie pokazuje pożytku,
bo wskazuje czytanie, które polszczyzna wybrała już bez niego.

Sąsiedztwem jest akapit, a granicę tę bierzemy stąd, skąd bierze ją druga strona:
skład opuszcza podmiot wtedy, gdy o rzeczy była mowa w zdaniu obok,
a akapit jest tym, w czym „obok” się kończy
([sklad.md](sklad.md)).
Czyta się je wstecz, bo czytelnik idzie od początku do końca,
i lematami, bo `w systemach` i `w systemie` są tą samą frazą o tej samej rzeczy.
Pytanie idzie przy tym o to, co stało przed frazą, a nie o część mowy,
więc gospodarza czasownikowego ten świadek wskazuje tą samą drogą,
kiedy fraza stała wcześniej przy tym samym czasowniku.

Tą samą frazą są przy tym formy o jednym lemacie imiennym, a nie o jednym lemacie.
Morfeusz sprowadza do czasownika i odsłownik, i imiesłów przymiotnikowy,
więc bez tego warunku `żądań` i `żądającym` znaczą dla świadka jedno słowo
i zdanie o żądającym dowodzi czegoś o żądaniach.
Odsłownik zostaje, bo jest rzeczownikiem,
czyli kryterium jest częścią mowy w tagu, a nie samym lematem.
Gospodarza to zawężenie nie obejmuje, i rozmyślnie,
bo gospodarzem bywa czasownik:
`jest przetwarzany w Systemie RIT` dowodzi o gospodarzu `przetwarzania`
przez to samo zlanie, które po stronie frazy myli.

Przy gospodarzu fraza stanęła także wtedy, gdy dzieli je łańcuch imienny.
Sąsiad bezpośredni sam nie wystarcza, bo w łańcuchu dopełniaczowym jest nim ogon grupy:
w `wymiany danych z systemami zewnętrznymi` fraza dochodzi do `wymiany`, a nie do `danych`.
Łańcuch urywa pierwsza forma bez czytania imiennego,
więc w `nadawanie i funkcjonowanie uprawnień do przeglądania` spójnik odcina `nadawanie`.
Dwóch gospodarzy w jednym łańcuchu kończy się milczeniem,
tym samym warunkiem, którym kończy się fraza powtórzona przy obu:
sąsiedztwo powtarza wtedy sporne przyłączenie, zamiast je rozstrzygać.

**Nad rejestrem, o który chodzi, świadek ten nie odzywa się ani razu.**
`sonda/powtórzenie.py` przechodzi prozę zdanie po zdaniu
i pyta go o każde przyłączenie, przed którym werdykt postawił wybór.
Korpusem jest [korpus audytowy](audit-corpus.md#the-list),
czyli dokumentacja techniczna wyekstrahowana do prozy tak, jak ten dokument mówi:

```sh
python3 -m sonda.powtórzenie proza/
```

```text
39 plików, 2915 zdań
  pierwszych w akapicie: 2383 (81.7%), czyli bez czego przeczytać
  przyłączeń: 38, z tego z sąsiedztwem: 13
  odpowiedzi w granicy akapitu: 0, czyli 0.0% przyłączeń
  odpowiedzi bez granicy akapitu: 2, czyli 5.3% przyłączeń
  to samo przy regule „sąsiad bezpośredni”: 3, czyli 7.9% przyłączeń
  to samo przy regule „cały prefiks zdania”: 3, czyli 7.9% przyłączeń
```

Zero ma trzy mianowniki i tylko ostatni z nich jest o świadku.

Największy jest o gramatyce.
Przyłączeń jest w całym korpusie 38, bo prawie każde zdanie tego rejestru olski odrzuca,
więc warstwa dostaje 38 pytań na 2 915 zdań,
a żaden świadek nie odpowie częściej, niż jest pytany.
Świadek statystyczny odpowiada na te same 38 siedem razy —
tyle wierszy wydaje `olski-check --rozstrzygaj` nad tymi plikami —
i tyle jest całej tej warstwy nad tym rejestrem.

Drugi jest o rejestrze: cztery piąte jego zdań stoi pierwsze w swoim akapicie,
więc świadek nie ma tam czego przeczytać.
Każdy akapit ma zdanie pierwsze, a żaden akapit tego korpusu nie stoi bez zdania,
więc liczba ta jest zarazem liczbą akapitów:
2 383 akapity na 2 915 zdań, czyli po 1,2 zdania na akapit.
Akapit tej długości bierze się z tego, co ekstrakcja liczy za akapit,
a liczy za niego osobno każdą pozycję listy,
bo zdanie nie biegnie z jednej do następnej
([extraction.md](extraction.md)).
Ile z tych 2 383 wyszło właśnie z list, nie mówi ani ten przebieg, ani żaden inny,
bo ekstrakcja nie wypuszcza typu węzła, z którego akapit powstał;
tego samego braku dotyczy wpis w [`TODO.md`](../TODO.md)
o mapowaniu trafień z powrotem na konstrukcje.

Trzeci jest o świadku i jest najmniejszy:
przyłączeń z sąsiedztwem jest 13 i przy żadnym z nich fraza wyżej nie stała.

**Granicę akapitu wyceniono i kupuje ona dwie odpowiedzi.**
Wariant sondy podaje świadkowi cały dokument czytany wstecz zamiast akapitu,
i wtedy odpowiada on 2 razy zamiast zera.
Nie jest to propozycja zdjęcia tej granicy, tylko jej cena,
a 2 odpowiedzi to za mało, żeby na nich ruszać granicę,
którą akapit dostał z drugiej strony.
Przeczytane ręką pokazują za to, jaki dowód je wydał.

Obie wskazują dobrze i dowód pod nimi mówi to samo.
`liczbę żądań do API` dostaje `żądań` po zdaniu
`Wszystkie żądania do API KSeF podlegają limitom.`,
a `informacje o sposobie przetwarzania żądań w Systemie RIT`
dostaje na `w Systemie RIT` gospodarza `przetwarzania`
po zdaniu, w którym obiekt `jest przetwarzany w Systemie RIT`.

**Regułę kandydata wyceniono tą samą drogą, a obie odrzucone dokładają pomyłkę.**
Wariant węższy pyta o samego sąsiada frazy i odpowiada 3 razy,
a odpowiedź trzecia myli się na łańcuchu dopełniaczowym:
`Wpływa to na sposób wymiany danych z systemem RIT.` dostaje gospodarza `danych`,
gdzie fraza dochodzi do `wymiany`.
Dowodem jest tam `wymiany danych z systemami zewnętrznymi`, czyli ten sam łańcuch,
więc powtórzenie jest prawdziwe, a odczytane z niego wskazanie nie.
Reguła wypuszczana widzi w tym łańcuchu obu gospodarzy naraz i o tym zdaniu milczy.

Wariant szerszy pyta o cały prefiks zdania, odpowiada również 3 razy i trafia raz.
`Sprzedawca wystawia fakturę w trybie offline.` dostaje `fakturę`,
choć dowód `faktury wystawionej w trybie offline` stawia tę frazę przy wystawieniu.
Gospodarza czasownikowego nie wskazuje tam żadna z trzech reguł,
bo `wystawiać` i `wystawić` mają u Morfeusza osobne lematy:
para aspektowa jest dla tego świadka dwoma słowami.
`System jest niewrażliwy na wielkość liter w przypadku tych atrybutów.` dostaje `jest`
po zdaniu, w którym pytana fraza nie stała wcale:
zeszła się z frazą `w dokumencie` przez `Atrybuty` stojące trzy słowa za tym przyimkiem.
Odpowiedź o `przetwarzania` wariant ten przy tym traci,
bo w prefiksie zdania dowodzącego gospodarzy jest dwóch.
Wypadek z `Atrybutami` jest usterką dopasowania frazy, a nie tej reguły —
reguła wypuszczana ma ją tak samo i nad tym korpusem tylko na nią nie trafia —
i trzyma ją [`TODO.md`](../TODO.md).

Trafności nie ma tu wobec tego wcale.
Dwie odpowiedzi wzięte z wariantu nie są częstością,
a materiał, na którym dałoby się ją policzyć, jest dwojaki:
[wzorzec po drugiej stronie](#wzorzec-na-tę-warstwę-jest-po-drugiej-stronie),
którego nie ma, oraz
[wybory przeczytane ręką](#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów),
których jest trzydzieści.

**Świadek statystyczny liczy bank drzew i nazywa własną częstość pomyłek.**
`Skłonność` liczy, jak często ta para przyimka i gospodarza
przyłączała się w banku drzew w tę stronę,
i odpowiada dopiero powyżej progu wsparcia i progu przewagi.
Tabelę buduje się i ocenia z tego samego korpusu:

```sh
python3 -m olski.rozstrzyganie Składnica-frazowa-180723/ --oceń
python3 -m olski.rozstrzyganie Składnica-frazowa-180723/ --zbuduj --wsparcie 2
```

Ocena buduje tabelę na połowie banku drzew i sprawdza ją na drugiej,
dzieląc po parzystości numeru pliku, żeby ta sama komenda dwa razy dała tę samą liczbę.
Nad 2 000 wyborami z połowy, której świadek nie widział:

| wsparcie | próg | odpowiada w | trafia w |
| --- | --- | --- | --- |
| — | — | 100,0% | 66,8% |
| 2 | 70% | 13,4% | 89,9% |
| 2 | 85% | 12,8% | 89,5% |
| 3 | 85% | 7,3% | 89,8% |
| 5 | 85% | 3,0% | 96,7% |
| 5 | 95% | 2,3% | 97,8% |

Pierwszy wiersz jest podłogą, czyli regułą „zawsze do rzeczownika”,
tą samą, którą [subset.md](subset.md#dlatego-olski-przyjmuje-koszt) odrzuciła jako konwencję.
Ustawieniem domyślnym jest wsparcie 2 i próg 85%,
czyli świadek odpowiada o jednym wyrażeniu na osiem i myli się w co dziesiątej odpowiedzi.

Cztery rzeczy o tej tabeli trzymają się razem i osobno każda z nich myli.

Trafność jest wysoka, a zasięg mały, i jest to ta sama liczba wzięta dwa razy:
świadek odpowiada tam, gdzie bank drzew ma parę policzoną,
a par jest tyle, ile ich korpus tej wielkości daje.

Trafność 89,5% nie jest trafnością zadania, tylko trafnością na wybranej ósmej części,
a najlepszy zmierzony model przyłączenia sięga 86,7% przy zasięgu pełnym,
i to on jest liczbą do pobicia, a nie podłoga.

Tabela oceniana nie jest tabelą wypuszczaną.
Ocena buduje swoją z połowy korpusu, żeby mierzyć na materiale nieoglądanym,
a `olski/skłonności.txt` powstaje z całości i ma 998 par,
więc wiersze wyżej są dla niej oszacowaniem od dołu co do zasięgu
i nie są pomiarem jej trafności wcale.
Zmierzyć ją mógłby dopiero korpus, którego ta tabela nie widziała,
a takiego drugiego banku drzew dla polszczyzny ten przegląd nie zna.

Rejestr się przy tym nie zgadza: bank drzew jest prozą literacką i prasową,
a olski celuje w dokumentację techniczną,
więc skłonność wzięta stąd jest punktem wyjścia, a nie pomiarem rejestru, o który chodzi.

Trzeci świadek, który tu należy i którego nie ma, to rama walencyjna,
czyli ta część klasy, o której sekcja o leksykonie mówi, że nie konkuruje z niczym.
Byłby pierwszy w kolejności, bo jego dowód jest słownikowy,
i nie da się go dziś napisać, bo `olski/leksykon.txt` o przyimku nie mówi.
Co trzeba zmienić w `olski/walenty.py`, żeby mówił, trzyma [`TODO.md`](../TODO.md).

## Werdykt pyta warstwę o inny wybór niż bank drzew

Ocena wyżej mierzy świadka na czwórkach lematów wziętych z banku drzew,
a warstwę wypuszczaną pyta `olski-check` i pyta ją czym innym.
Pytaniem jest `Przyłączenie` z werdyktu:
gospodarze są formami, a nie lematami anotatora,
form tych bywa więcej niż dwie,
i lemat wybiera dopiero Morfeusz, wybierając ich kilka naraz.
Drogę drugą mierzy `sonda/wskazania.py`, pytając o wzorzec drzewo wzorcowe:

```sh
python3 -m sonda.wskazania Składnica-frazowa-180723/
```

```text
  503 zdań, nad którymi werdykt zostawia przyłączenie,
  a w nich 665 przyłączeń, czyli tyle pytań warstwa dostaje

  gospodarzy na przyłączenie:
      515   77.4%  2
      115   17.3%  3
       30    4.5%  4
        5    0.8%  5

  ze wzorcem w drzewie: 511, czyli 76.8% przyłączeń

  co warstwa mówi o 511 przyłączeniach ze wzorcem:
      102   20.0% odpowiedzi,  96.1% trafień    skłonność
      511  100,0% odpowiedzi,  58.7% trafień    podłoga: zawsze do rzeczownika
```

Trzy rzeczy tej tabeli trzymają się razem i osobno każda z nich myli.

Zasięg 20% jest zasięgiem warstwy wypuszczanej i jest wyższy od 12,8% z oceny wyżej,
bo tabela wypuszczana ma 998 par zamiast tych z połowy korpusu,
a lematów formy pyta się naraz kilku, więc para znajduje się częściej.
Populacja jest przy tym inna — te 665 przyłączeń to te, przed którymi wybór postawił olski,
a nie te, przed którymi postawił go anotator — więc dwóch zasięgów nie odejmuje się od siebie.

Trafność 96,1% jest mierzona na materiale, który ta tabela widziała.
`olski/skłonności.txt` powstaje z całej Składnicy, a przebieg idzie po całej Składnicy,
więc liczba ta jest górnym oszacowaniem i pomiarem trafności nie jest.
Trafnością poza próbą jest 89,5% z oceny wyżej,
a przebieg dzielący korpus tak, jak dzieli go tamta, trzyma [`TODO.md`](../TODO.md).

Gospodarzy jest więcej niż dwóch w 22,6% przyłączeń,
czyli w tylu wypadkach ocena z czwórek mierzy wybór łatwiejszy niż ten, przed którym warstwa staje.
Wypadki te biorą się z produkcji, a nie z rzadkości:
`Obudziłem się na podłodze w kuchni z pustą paczką po ciasteczkach w dłoniach.`
ma cztery przyłączenia, a każde następne dostaje za gospodarza rzeczownik z poprzedniego.

Wzorca nie ma dla 154 z 665 przyłączeń i nie jest to milczenie banku drzew.
Drzewo albo nawiasuje tę frazę inaczej, niż nazywa ją werdykt,
albo przyłącza ją do czegoś, co nie jest ani grupą imienną, ani zdaniem —
`Auta są kradzione dla okupu.` jest tym drugim, bo fraza dochodzi tam do imiesłowu.
Złączenie idzie formami modyfikatora, bo tyle mają obie strony:
werdykt rozpiętości nie niesie.

## Wzorzec dla rejestru czyta się ręką i jest go trzydzieści wyborów

Bank drzew jest zbiorem zdań stojących osobno,
więc świadek kontekstowy nie ma nad nim czego przeczytać
i w tabeli wyżej nie odzywa się ani razu.
Nad korpusem audytowym jest odwrotnie: tekst jest ciągły, a wzorca nie ma tam żadnego.
`próba/wybory.txt` dokłada ten wzorzec i jest jedynym miejscem w tym repozytorium,
w którym sąd o zdaniu pochodzi z przeczytania, a nie z cudzego korpusu ani z przebiegu.

Zdania są przy tym cudze, a nasz jest sam sąd.
Zdanie wymyślone pod świadka mierzy autora, a nie rejestr,
więc pozycje bierze się z [korpusu audytowego](audit-corpus.md#the-list) takie, jakie tam stoją,
i losuje spośród wszystkich 1 678 (`rozrzucona` w `olski/próbka.py`).
Wyznacza je morfologia, a nie werdykt (`olski/wieloznaczność.py`),
bo werdyktów jest nad tym rejestrem 38 na 2 915 zdań i nie ma czego z nich losować.
Ręką dopisuje się gospodarza wraz z powodem,
a poprawia się przy tym frazę i gospodarzy,
bo budowniczy proponuje je z morfologii i bierze ogon łańcucha dopełniaczowego za głowę grupy.

```sh
python3 -m sonda.wybory próba/wybory.txt
```

```text
30 wyborów ze wzorcem, z tego 5 do przemilczenia
     2  oba
     3  żadne

  co warstwa odpowiedziała:
     2    6.7% odpowiedzi, 100.0% trafień    powtórzenie
     3   10.0% odpowiedzi, 100.0% trafień    skłonność
     5  100.0% wyborów do przemilczenia przemilczanych
    10   33.3% wyborów rozstrzygniętych dobrze
```

Wzorzec ma dwie odpowiedzi poza samymi gospodarzami i obie są tu po to,
żeby milczenie warstwy dało się ocenić.
`oba` znaczy, że tekst nie rozstrzyga i czytelnik też nie:
`Numer nadawany jest podczas przetwarzania faktury po stronie KSeF.`
mówi to samo, dokądkolwiek ta fraza dojdzie, bo przetwarzanie i nadanie numeru
dzieją się w jednym miejscu.
Jest to ta sama klasa, którą
[tożsamość czytania](#tożsamość-czytania-jest-tańsza-i-częściowo-już-stoi)
wycenia na trzecią część błędów najlepszego modelu przyłączenia.
`żadne` znaczy, że wyboru nie ma wcale,
bo pozycja znaleziona morfologicznie nie jest przyłączeniem:
`takich jak /auth/challenge` jest porównaniem, a nie wyrażeniem przyimkowym,
i trzy z trzydziestu wyborów są tego rodzaju.

**Świadek kontekstowy odzywa się tu dwa razy i dwa razy trafia.**
Jest to pierwsza jego odpowiedź zestawiona z wzorcem,
bo [pomiar zasięgu](#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)
nad tym samym korpusem pytał go o przyłączenia z werdyktów i dostał zero.
Oba dowody są tego samego kształtu, czyli frazą powtórzoną przy gospodarzu:
`z prawem do dalszego przekazywania` po zdaniu z `bez prawa do dalszego przekazywania`,
oraz `uprawnień pracownikom do przeglądania` po zdaniu z `uprawnień do przeglądania`.
Drugi z nich jest tym, czego tabela skłonności nie umie:
fraza dochodzi tam do rzeczownika oddzielonego od niej celownikiem,
a bank drzew o takim szyku nie mówi nic.

Dwie trzecie wyborów zostaje nierozstrzygniętych i to jest właściwa liczba tej próby.
Warstwa nie myli się nad nią ani razu, co pilnuje `tests/test_wybory.py`,
i nie jest to zasługa progów, tylko ich ceny:
milczenie jest tu odpowiedzią w dwudziestu wypadkach na trzydzieści.
Trzydzieści wyborów wystarcza, żeby powiedzieć, że warstwa milczy częściej, niż odpowiada,
i nie wystarcza, żeby powiedzieć, jak często się myli;
o ile tę próbę powiększyć, pyta wpis w [`TODO.md`](../TODO.md).

## Wieloznaczność, której werdykt nie melduje

Wszystko wyżej pyta o zdanie, po którym zostaje czytań kilka.
Bywa jednak i tak, że zostaje jedno wyprowadzenie,
a zdanie mimo to czyta się dwojako:

```sh
python3 -m olski.check --readings -c "Wynajmę mieszkanie. Znam go."
```

```text
<text>: valid     Wynajmę mieszkanie.
                  one reading
                  - Object: mieszkanie, Verb: Wynajmę
<text>: valid     Znam go.
                  one reading
                  - Object: go, Verb: Znam
2 of 2 sentences are olski
```

Pierwsze zdanie mówi raz, że wynajmuję komuś swoje mieszkanie,
a raz, że wynajmuję czyjeś dla siebie,
więc uczestnicy zamieniają się w nim rolami: jestem właścicielem albo lokatorem.
Drugie mówi raz, że wiem, kto to jest, a raz, że się z nim znam.
Streszczenie wypisuje w obu wypadkach jedno obsadzenie ról,
bo różnica nie leży ani w drzewie, ani w tym, co drzewo o rolach mówi.

Kierunek tej pomyłki jest odwrotny niż ten, o który pyta
[open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma),
i droższy o to, że nie widać go w odpowiedzi.
Zdanie odrzucone za wieloznaczność, której czytelnik nie ma,
autor czyta wraz z czytaniami i odrzucenie kwestionuje;
zdanie przyjęte wraca z jednym czytaniem i z niczym, o co dałoby się spierać.
Jest to ta sama ślepota, którą [tożsamość czytania](#tożsamość-czytania-jest-tańsza-i-częściowo-już-stoi)
wycenia po stronie sygnatury zwijającej za dużo,
z tą różnicą, że tu nie ma czego zwijać: drugiego czytania las nigdy nie miał.

## Rozstrzygnąć da się tylko to, co las trzyma

Kontekst nie wybierze czytania, którego w lesie nie ma,
więc warstwa kontekstowa jest nad tą klasą ruchem drugim, a nie pierwszym.
Pierwszym jest zadeklarowanie wyboru, czyli powiedzenie gramatyce, że czytania są dwa.
Dopiero to, co po nim zostaje, jest ujednoznacznianiem.

Pierwszy ruch jest pytaniem do leksykonu i źródło już na nie odpowiada.
Walenty, ściągnięty tak, jak mówi
[subset.md](subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego),
daje `wynająć` cztery schematy:

```text
wynająć: pewny: _: : perf: subj{np(str)} + obj{np(str)} + {np(dat)} + {prepnp(do,gen)}
wynająć: pewny: _: : perf: subj{np(str)} + obj{np(str)} + {np(dat)} + {prepnp(na,acc)}
wynająć: pewny: _: : perf: subj{np(str)} + obj{np(str)} + {prepnp(od,gen)}
wynająć: pewny: _: : perf: subj{np(str)} + obj{np(str)} + {prepnp(u,gen)}
```

Wynajmuje się komuś i wynajmuje się od kogoś,
a `Wynajmę mieszkanie.` nie obsadza ani celownika, ani frazy z `od`,
więc podchodzi pod wszystkie cztery naraz.
Rozróżnienie, którego werdykt nie ma, leży więc w słowniku, z którego olski leksykon bierze,
a trzy zdania, na które ten przekład Walentego zawęża (tamże), nie są o nim.

Cena pierwszego ruchu jest widoczna od razu:
zdania, które dziś wychodzą `valid`, wychodziłyby `ambiguous`.
Ilu lematów to dotyczy, liczy sonda nad tym samym plikiem.
Szuka ona konwersów, czyli par czytań opowiadających jedno zdarzenie z dwóch stron:

```sh
python3 -m sonda.konwersy walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt
```

Wraca 144 lematy z 17 224, każdy z parą schematów,
z których jeden ma odbiorcę w celowniku, a drugi źródło pod `od` albo `u`.
Kryterium jest zgadywaniem z kształtu pozycji, bo Walenty ról nie nazywa,
a warstwy semantycznej wydanie tekstowe z 18 kwietnia 2016 nie niesie —
własne README wylicza jego pliki i są to schematy dla czterech części mowy.
Liczba jest przez to górnym oszacowaniem, a przeczytanie mówi, jak wysokim.
Z dwunastu par, które sonda wypisuje,
dwie zostawiają zdanie przechodnie z dwoma czytaniami:
`przepisywać` — komuś na własność albo od kogoś ze ściągi — oraz `wyczarterować`.
Dziesięć pozostałych łapie celownik posiadacza albo tego, komu się przysłuży,
a `wykryć komuś raka` i `wykryć u kogoś raka` mówią wręcz to samo,
czyli kryterium bierze tam dwa sposoby powiedzenia jednej rzeczy za dwa czytania.
Dwanaście par przeczytanych jedną ręką wystarcza, żeby powiedzieć, że liczba jest za wysoka,
i nie wystarcza, żeby powiedzieć, ile wynosi.

Cenę pierwszego ruchu ta liczba wycenia przy tym po jednej stronie i tylko po jednej.
Mówi, że klasa jest w słowniku wąska — 144 lematy z 17 224 —
a nie mówi, ile zdań rejestru niesie taki czasownik,
bo `brać` i `wziąć` stoją na tej liście obok `wyczarterować`.
Drugą stronę zmierzyłby przebieg nad korpusem i trzyma go [`TODO.md`](../TODO.md).

`Znam go.` jest drugą połową tej klasy i tam leksykon walencyjny milczy.
Schematy, które `znać` u Walentego ma, różnią się kształtem dopełnienia,
a nie tym, jak się kogoś zna,
więc oba czytania mieszczą się pod tym samym.
Źródłem byłby wobec tego słownik znaczeń, a nie słownik walencyjny,
i pierwszym kandydatem jest plWordNet, o który ten przegląd nie pytał.

## Kontekst rozstrzyga wykluczeniem, a nie rankingiem

[Ranking](#ranking-nie-jest-wyjściem-którego-ten-parser-potrzebuje) odpadł na tym,
że zamienia `ambiguous` na `valid` wraz z domysłem.
Kontekst pozwala na ruch innego rodzaju:
nie wybiera czytania lepszego, tylko zdejmuje to, któremu sąsiedztwo przeczy.
Kiedy zostaje jedno, zdanie ma w tym tekście jedno czytanie, a nie czytanie zgadnięte.
Kiedy zostają dwa, werdykt wychodzi taki sam, jaki był bez tej warstwy.
Milczenie jest więc odpowiedzią domyślną, tak jak u [świadka](#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
a różnica wobec rankingu leży w tym, ile kosztuje brak odpowiedzi: nic.

Cena jest gdzie indziej i jest większa.
Werdykt przestaje być o zdaniu:
`Wynajmę mieszkanie.` ma samo dwa czytania, a w tamtym tekście jedno,
więc to samo zdanie dostaje dwie odpowiedzi zależnie od tego, co je otacza,
i przestawienie akapitu rusza werdykt bez ruszania zdania.
Czy jednoznaczność jest własnością zdania, czy zdania na swoim miejscu,
nie jest rozstrzygnięte i pyta o to
[open-questions.md](open-questions.md#warstwa-kontekstowa-zabiera-werdyktowi-jednostkę).

Dowody, na których taka warstwa mogłaby stanąć, są trzy
i idą w tej samej kolejności co u świadka, czyli od słownikowego w dół.

**Uczestnik nazwany obok.**
`Wynajmę mieszkanie. Wynajmę je od Anki.` rozstrzyga się samym leksykonem:
druga fraza obsadza pozycję, którą ma jeden ze schematów, a drugi nie.
Wersja trudniejsza — `Szukam ułożonego lokatora.` — żąda jednego kroku więcej,
bo `lokator` jest tym, kto stoi w pozycji celownikowej,
a tego, że nim jest, Walenty nie mówi;
mówi to dopiero słownik wiążący rolę ze słowem, czyli to samo źródło, którego żąda `znać`.

**Temat.**
Skład wyprowadza szyk z tego, co w zdaniu jest tematem, a co nowe
([README](../README.md)),
więc związek kolejności z tematem jest po tamtej stronie napisany.
Autor drzewa temat tam deklaruje, a parser musiałby go zgadnąć,
i krokiem, którego skład nie robi, jest zrównanie tematu z tym, o czym mowa była przed chwilą.
Po tym kroku przy synkretyzmie mianownika z biernikiem
pierwszą grupą jest ta, którą wymieniło zdanie poprzednie.
Pomiar niderlandzki cytowany wyżej mówi tyle, że zdanie poprzednie ten wybór czytelnikowi rozstrzyga,
a czy rozstrzyga go tematem, nie mówi.

**Wynikanie.**
`Znam go. Rozmawiałem z nim na imprezie u Anki.` rozstrzyga się dopiero wtedy,
gdy skądś wiadomo, że rozmowa jest kontaktem osobistym.
Takiego zapisu nie ma w tym repozytorium nic,
a rzeczą, która go ma, jest model językowy,
czyli odpowiedź, po którą ten parser nie sięga ([README](../README.md)).
Warstwa kończy się więc przed trzecim dowodem i to jest cała jej granica.

Zbudowany jest z tych trzech jeden i zbudowany węziej, niż ta sekcja opisuje.
`Powtórzenie` bierze dowód pierwszego rodzaju w postaci, która słownika ról nie żąda —
fraza powtórzona przy gospodarzu — i stosuje go do przyłączenia,
czyli do wyboru, który las już trzyma, a nie do ramy z sekcji wyżej.
Wskazuje przy tym gospodarza obok werdyktu i czytania nie zdejmuje,
bo zdejmowanie żąda rozstrzygnięcia o jednostce werdyktu, którego nie ma.
Co ten świadek robi i jaką regułę odrzuca po drodze,
mówi [sekcja o zalążku](#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek).

Jedno widać dopiero po uruchomieniu i osłabia dwa pierwsze dowody naraz.
Sąsiedztwo, które ma rozstrzygać, samo bywa nieolskie:
`Szukam ułożonego lokatora.` gramatyka odrzuca,
bo `szukać` stoi w `olski/leksykon.txt` jako czasownik, który biernika nie bierze,
a dopełniacza dopełnieniowego olski nie ma.
Warstwa czytałaby więc zdanie sąsiednie czymś słabszym niż gramatyka,
formami i lematami z Morfeusza,
tak jak nad rejestrem czyta je `olski/wieloznaczność.py`.

## Wzorzec na tę warstwę jest po drugiej stronie

Pomiar takiej warstwy wygląda na droższy niż wszystko wyżej,
bo bank drzew jest zbiorem zdań stojących osobno,
a wzorcem musiałby być tekst wraz z czytaniem, o które w nim chodziło.
Olski taki materiał wytwarza i wytwarza go za darmo.
Drzewo, z którego skład wypuszcza tekst, ma uczestników wymienionych,
tożsamość rzeczy niesie w nim `Postać`, a czas i to, o kim mowa — `Kontekst`
([sklad.md](sklad.md)),
więc odpowiedź jest znana, zanim padnie pytanie.

`olski/skład/przegląd.py` zadaje już dziś pytanie parsera z tamtej strony:
czy czytelnik odzyska z napisu to drzewo, które ten napis wypuściło.
Liczy przy tym role, a nie znaczenia, i liczy je na napisie stojącym w tekście,
bo kontekst rozstrzyga, jakim napisem zdanie wyszło.
Warstwa kontekstowa mierzy się więc obrotem:
skompiluj tekst, rozbierz go i zapytaj, czy zdejmuje ona czytanie,
którego drzewo nie deklarowało.
Anotatora w tym obrocie nie ma nigdzie.
Sam obrót jest już przedmiotem pytania
[open-questions.md](open-questions.md#the-round-trip-guarantee),
tyle że tamto pyta o gwarancję, a to o pomiar:
gwarancja żąda, żeby drzewo wyjściowe znalazło się w lesie,
a pomiar pyta, ile czytań obok niego warstwa zdejmuje.

Czego ten obrót nie mierzy, wiadomo z góry i jest tego dużo.
Rejestrem jest to, co skład umie powiedzieć, a nie dokumentacja techniczna,
więc obrót odpowiada na pytanie, czy mechanizm działa,
a nie na pytanie, jak często jest potrzebny.
Drugie żąda korpusu i zostaje w liście niżej.

## Czego brakuje, żeby odpowiedzieć pomiarem

Trzecie z trzech pytań — czy czytelnik widzi tu wybór — jest tym,
od którego zależą wszystkie decyzje wyżej, i jest jedynym bez wzorca.

Bank drzew na nie nie odpowiada i nie jest to jego usterka.
Anotator Składnicy wybierał drzewo z lasu,
więc jego odpowiedź mówi, które czytanie jest właściwe,
a nie czy drugie w ogóle było dla niego czytaniem.
Odpowiedź, której to pytanie potrzebuje, ma inną postać:
pary czytań z sądem, czy mówią to samo.
Anotacja taka jest przy tym tańsza niż wybór drzewa,
bo nie żąda od anotatora czytania drzew —
werdykt olskiego już dziś nazywa wybór słowami zdania,
`„z dodatkami” → „przewyższa”, „koszt”, „szynki”`,
i to jest materiał, który da się położyć przed kimś, kto o gramatyce nie wie nic.

Populację pod taki pomiar liczą już dwa miejsca.
Ile zdań rejestru niesie pozycję dwuznaczną, mierzy
[open-questions.md](open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma),
a ile ich niesie werdykt, mierzy tabela wyżej.
Czego brakuje między nimi, to sąd nad parą,
i dwadzieścia cztery zdania przeczytane raz jedną ręką
są za wąską podstawą, żeby na nim stanąć;
tamten dokument mówi to o swojej próbce sam.

[Wybory przeczytane ręką](#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów)
odpowiadają na to pytanie w jednym wpisie na piętnaście
i odpowiadają na nie po drodze, a nie wprost:
`oba` znaczy tam, że czytelnik wyboru nie widzi, choć pozycja go stawia.
Dwa takie wpisy z trzydziestu są tego samego rzędu co próbka wyżej,
więc podstawy nie poszerzają;
poszerzy ją dopiero ten plik, kiedy urośnie, a nie osobny pomiar obok niego.

Cztery rzeczy zostają wobec tego nierozstrzygnięte.

Ile z 412 zdań, w których przyłączenie jest całą decyzją,
zdjąłby leksykon walencyjny sięgający do przyimka —
pomiar łączący dwa mianowniki, o których mówi sekcja o leksykonie.

Czy sygnatura czytania da się zagęścić bez przyjmowania zdań,
które naprawdę mają dwa czytania —
i czym uzasadnia się każde zwinięcie, skoro spadek liczby uzasadnieniem nie jest.

Czy werdykt ma nazywać klasę, do której zdanie należy,
czyli mówić „dwa czytania i polszczyzna ma tu dwa”, a nie samo „dwa czytania”.
Pytanie to jest starsze niż ten dokument i trzyma je
[open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma);
tabela wyżej daje mu populację, a nie odpowiedź.

Ile zdań rejestru niesie ramę, której zdanie samo nie wybiera —
liczba, której sonda nad Walentym nie daje,
bo liczy lematy, a jedno pytanie jest o zdania, drugie o to,
jak często taki lemat pada bez pozycji rozstrzygającej.
Odpowiedź żąda korpusu, a ten sam korpus zmierzyłby zarazem drugą połowę klasy,
czyli zdania, w których o znaczeniu nie mówi żaden schemat.

## Sources

- <https://nlp.stanford.edu/pubs/Coling2002.pdf> —
  Oepen, Toutanova, Shieber, Manning, Flickinger i Brants,
  *The LinGO Redwoods Treebank*, COLING 2002,
  skąd tabela skuteczności rankingu wobec wielkości lasu
- <https://link.springer.com/article/10.1007/s11168-005-1288-y> —
  Toutanova, Manning, Flickinger i Oepen,
  *Stochastic HPSG Parse Disambiguation using the Redwoods Corpus*, 2005,
  gdzie model dyskryminacyjny podnosi trafność całego drzewa powyżej 76%
- <https://doi.org/10.1007/978-3-319-43808-5_12> —
  Rogozińska i Woliński,
  *Experiments in PCFG-like Disambiguation of Constituency Parse Forests for Polish*,
  LNCS 9561, 2016, skąd 94,1% PARSEVAL i 92,1% ULAS nad lasami Świgry
- <https://www.let.rug.nl/vannoord/papers/> —
  publikacje van Noorda o modelu ujednoznaczniającym Alpino,
  w tym *Using Self-Trained Bilexical Preferences to Improve Disambiguation Accuracy*, 2007
- <https://aclanthology.org/E17-2050/> —
  de Kok, Ma, Dima i Hinrichs, *PP Attachment: Where do We Stand?*, EACL 2017,
  skąd 86,7% najlepszego modelu, rozbiór stu błędów i sufit zadania na 92,6%
- <https://aclanthology.org/P94-1030/> —
  Ratnaparkhi, Reynar i Roukos, *A Maximum Entropy Model for Prepositional Phrase
  Attachment*, HLT 1994, skąd 88,2% i 93,2% trafień człowieka
- <https://arxiv.org/abs/2305.14917> —
  Wijnholds i Moortgat, *Structural Ambiguity and its Disambiguation in Language
  Model Based Parsers: the Case of Dutch Clause Relativization*, 2023
- <https://www.cl.cam.ac.uk/~aac10/papers/mrs.pdf> —
  Copestake, Flickinger, Pollard i Sag, *Minimal Recursion Semantics: An
  Introduction*, gdzie niedookreślenie zastępuje wybór między czytaniami
- <https://aclanthology.org/2023.emnlp-main.51/> —
  Liu i inni, *We're Afraid Language Models Aren't Modeling Ambiguity*, EMNLP 2023,
  gdzie ujednoznacznienia GPT-4 uznano za poprawne w 32% wobec 90% dla zbioru
