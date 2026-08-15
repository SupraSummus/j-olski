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
Trzy rzeczy z wywodu wyżej są w nim wzięte wprost.

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
więc dowód słownikowy bije statystyczny wszędzie tam, gdzie oba mówią coś naraz.
Powód wraca razem ze wskazaniem, żeby wskazanie dało się sprawdzić bez zaglądania do tabeli.

**Świadek dzisiaj jest jeden i jest tym, którego ten wywód wycenia najniżej.**
Tożsamość czytania i leksykon są tańsze i obie sekcje wyżej tak je wyceniają,
a nie ma ich tutaj z powodów, które te sekcje podają:
pierwsza czeka na sąd o parze czytań, którego żaden korpus nie zapisuje,
a druga na kolumnę, której `olski/leksykon.txt` nie ma.
Świadek statystyczny jest tym, który da się zbudować z tego, co w repozytorium już jest,
i stąd kolejność odwrotna do ceny.
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

Drugi świadek, który tu należy i którego nie ma, to rama walencyjna,
czyli ta część klasy, o której sekcja o leksykonie mówi, że nie konkuruje z niczym.
Byłby pierwszy w kolejności, bo jego dowód jest słownikowy,
i nie da się go dziś napisać, bo `olski/leksykon.txt` o przyimku nie mówi.
Co trzeba zmienić w `olski/walenty.py`, żeby mówił, trzyma [`TODO.md`](../TODO.md).

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

Trzy rzeczy zostają wobec tego nierozstrzygnięte.

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
