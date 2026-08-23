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
Cztery piąte tego, co olski odrzuca nad bankiem drzew,
zostawia dokładnie jedną decyzję: dokąd dochodzi wyrażenie przyimkowe.
Zadanie to pole mierzy od trzydziestu lat, na własnych zbiorach i z rozbiorem błędów,
a pomiar mówi dwie rzeczy naraz:
najlepsze modele podchodzą pod sufit,
a sufit leży wyraźnie poniżej stu procent,
bo część tych decyzji rozstrzyga zdanie poprzednie,
a część nie jest decyzją wcale, bo oba czytania mówią to samo.

Którą z tych cen warto zapłacić, rozstrzyga hipoteza, którą ten dokument stawia:
dobre ujednoznacznianie jest odczytaniem tego, co czytelnik ma przed sobą.
Co z niej wychodzi i co by ją obaliło, mówi
[sekcja o niej](#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza).

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
złote czytanie jest w tej kolejności pierwsze w siedmiu wypadkach na dziesięć,
licząc wobec wszystkich zdań, o które to pytanie da się zadać,
a liczbę wraz z jej mianownikiem trzyma
[corpus.md](corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).

Tyle ma do pobicia model, który miałby tu stanąć.
Liczba jest przy tym łagodniejsza dla modelu, niż wygląda,
bo mierzy zgodność dwóch ról, a nie całego drzewa
(tamże), więc mierzy mniej niż 74,0% z tabeli wyżej.
Rzędu wielkości to nie rusza:
architektura, o którą tu chodzi, startuje z dwóch trzecich zrobionych,
i to jest ta część pytania, o której najłatwiej zapomnieć.

### Cechy lekkie biją ciężkie, bo uzgodnienia sprawdziła już gramatyka

Świgra ma za sobą serię pomiarów tej warstwy i mówią one, ile model musi zobaczyć.
Model w stylu PCFG, patrzący na same nazwy jednostek nieterminalnych
i nieznający ani jednego atrybutu,
osiąga nad Składnicą 93,3% F-miary na zasięgu i nazwie wierzchołka oraz 90,2% ULAS.
Atrybuty dołożone do tego modelu nic już nie dają,
bo obserwacji przybywa wtedy szybciej niż danych, na których się je liczy.
Model maksimum entropii idzie w tę samą stronę dalej:
zestaw cech mówiących o nadrzędniku i pojedynczym podrzędniku liczy 2 070 cech
i bije zestaw wypisujący całe ciągi składników bezpośrednich, liczący ich 67 590.
Dołożenie tych ciągów do najlepszego zestawu podnosi jedną z trzech miar
o tysięczną, a liczy się trzydzieści razy dłużej;
sam ten zestaw wychodzi na 95,6% F-miary i 93,7% ULAS.
Woliński czyta to tak, że uzgodnienia zapewnia już analizator regułowy,
więc ujednoznacznianie jest innym zadaniem niż analiza
i wystarcza mu informacja wybiórcza
(Woliński 2019, p. 7.2 i 7.3, w [źródłach](#sources) na końcu).

Dla warstwy, której tu nie ma, wynika z tego tyle:
nie musiałaby ona powtarzać tego, co gramatyka już sprawdziła,
więc jej cena nie rośnie z liczbą cech, które niesie werdykt.
Drugi pomiar z tej serii mówi, gdzie leży masa decyzji, i jest gorszą wiadomością.
Usunięcie z drzew Składnicy rozróżnienia frazy wymaganej od luźnej
podniosło na starszej wersji korpusu zgodność wszystkich atrybutów
z 72,1% na 92,2%.
Tyle model nie zyskał, bo prostsze zrobiło się samo zadanie:
losowanie po tak zmienionych drzewach też trafia wyżej.
Woliński dopowiada, że rozróżnienie to jest słabo ugruntowane lingwistycznie,
choć wszechobecne w teoriach i słownikach.
Człowiek myli się na nim tak samo
([corpus.md](corpus.md#what-this-number-is-not)).
U olskiego jest to różnica dopełnienia od okolicznika, czyli klasa `rola`
z [rozbicia niżej](#czym-różnią-się-czytania-które-olski-odrzuca),
i zaniedbać jej ten parser nie może:
werdykt nazywa role, więc czytanie, które obsadza je inaczej, jest innym czytaniem.

## Czym różnią się czytania, które olski odrzuca

Zanim wiadomo, ile ranking kosztuje, trzeba wiedzieć, co miałby rozstrzygać.
Odpowiada na to sonda nad Składnicą, ściągniętą tak, jak mówi
[corpus.md](corpus.md#fetching-it):

```sh
python3 -m harness.czytania Składnica-frazowa-180723/
```

Klasy bierze z tego, co werdykt o zdaniu wypisuje,
a nie z osobnej klasyfikacji napisanej obok:
`rola` znaczy, że czytania obsadzają różnie którąś z ról,
`przyłączenie`, że gospodarz modyfikatora zostaje nierozstrzygnięty,
`konstytuent`, że różnica leży tam, gdzie streszczenie nie zagląda.
Klasę da się więc sprawdzić, czytając werdykt nad zdaniem.
Nad zdaniami, które olski odrzuca za wieloznaczność,
klasy rozkładają się tak, a ile ich jest, drukuje przebieg wyżej:

| co werdykt nazywa | ile zdań wieloznacznych |
| --- | --- |
| rola + przyłączenie | przeszło trzy czwarte |
| przyłączenie | około jednej dziesiątej |
| rola | około jednej dziesiątej |
| sama liczba czytań | kilka na sto |
| konstytuent, sam albo w parze z tamtymi | kilka na sto |

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

**Tak liczone przyłączenie jest całą decyzją w siedmiu zdaniach na dziesięć,
a w dwóch klasach, które je nazywają, w przeszło czterech piątych.**
Udział ten obniża każda konstrukcja, której dwaj gospodarze różnią czytania rolą,
a nie przyłączeniem, bo klasa `rola` rośnie wtedy, a tamta nie:
pierwszym takim dopisaniem jest przysłówek
([subset.md](subset.md#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe)),
a zdanie okolicznikowe oraz interpunkcja zdaniowa idą tą samą drogą
([subset.md](subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania),
[subset.md](subset.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
Liczba jest górnym oszacowaniem i myli się w jedną stronę,
bo dwa przyłączenia, z których jedno ma gospodarza tylko pod jednym czytaniem drugiego,
dają czytań mniej niż iloczyn;
`całe_przyłączenie` w `harness/czytania.py` mówi to o sobie samo.

Cała reszta rozkłada się na dwie rzeczy, z których żadna nie jest zadaniem dla rankingu.

Pierwsza to czytanie, którego polszczyzna nie ma.
`Trwa akcja protestacyjna.` wychodzi dwoma czytaniami,
bo `protestacyjna` czyta się raz jako przydawka, a raz jako orzecznik,
a orzecznika w tym miejscu polszczyzna nie stawia.
Nie jest to wieloznaczność do rozstrzygnięcia, tylko nadgeneracja do zdjęcia,
i tym zajmuje się [etap 3](roadmap.md#etap-3-czytania-których-polszczyzna-nie-ma),
a nie żadna warstwa za parserem.

Druga to trzy zdania, nad którymi werdykt nie mówi nic poza liczbą czytań,
a w każdym z nich czytania różni ciąg współrzędny.
Ciąg nie dostaje wiersza o konstytuencie rozmyślnie,
bo granicę członu pokazuje nawias w napisie roli;
nawias obejmuje jednak ciąg, którym jest sama rola,
a nie ciąg stojący w wypełnieniu głębiej
([design-notes.md](design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)),
i tam — w dopełnieniu albo w okoliczniku — stoją wszystkie trzy.
Najkrócej widać tę klasę na zdaniu z ustaw, bo czyta się je bez banku drzew:
`Ustawa określa zadania ochrony ludności i obrony cywilnej.`
wychodzi dwoma czytaniami, `zadania [ochrony ludności] i [obrony cywilnej]`
oraz `zadania ochrony [ludności i obrony cywilnej]`,
i werdykt milczy nad nim tak samo
([ustawy.md](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)).
Czy jest to ta sama pomyłka, którą
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
opisuje w cudzym systemie — liczenie prób zamiast wyników —
rozstrzyga się osobno nad każdym takim ciągiem:
to zdanie z ustaw znaczy pod dwoma nawiasowaniami dwie różne rzeczy,
a ciąg `równych praw kobiet i mężczyzn` z jednego ze zdań Składnicy — jedną.
Ile jest których, notuje [`TODO.md`](../TODO.md).

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

## Dobre ujednoznacznianie jest odczytaniem i jest to hipoteza

Sekcja wyżej odrzuca ranking, dwie niżej przyjmują po jednej rzeczy tańszej,
a trzecia mówi, że reszty nie rozstrzyga nic, co stoi w zdaniu.
Każda z tych czterech decyzji ma osobne uzasadnienie,
a pod wszystkimi leży jedno zdanie, którego dotąd nikt tu nie wypisał:
odpowiedź warta wzięcia jest odczytaniem tego, co czytelnik ma przed sobą,
a nie częstością zmierzoną nad czymś, czego przed sobą nie ma.

Kryterium, które z tego wychodzi, pyta o powód, a nie o trafność.
Odpowiedź przychodzi z powodem albo nie przychodzi wcale,
a powody są dwojakie.
Pierwszy nazywa coś, co leży w tym tekście albo w słowniku słowa z tego tekstu;
drugi liczbę policzoną nad korpusem, którego czytelnik nie czyta.
Pierwszy sprawdza się bez wychodzenia z akapitu.
Drugiego nie sprawdza nic, bo sprawdzianem byłaby ta sama tabela, którą przed chwilą zacytował.
Żąda tego od odpowiedzi to samo zdanie, które README stawia werdyktowi:
każdy werdykt przychodzi z czytaniem, które go wydało,
czyli parser mówi, na czym stanął ([README](../README.md)).

Hipoteza ma dwie połowy i tylko drugą da się obalić.

Pierwsza połowa jest decyzją, a nie odkryciem.
Mówi ona, że rankingowi nie pomoże dziesięć punktów trafności więcej:
model trafiający w dziewięciu wypadkach na dziesięć
dalej nie umie powiedzieć autorowi, dlaczego akurat tak,
a wyjaśnienie jest tym, co ten parser obiecuje zamiast prawdopodobieństwa.
Sekcja wyżej wycenia odrzucenie rankingu liczbą pomyłek,
a ta połowa mówi o tamtej liczbie, że jest ceną i nie jest powodem.

Druga połowa mówi coś o świecie i daje się zmierzyć.
Brzmi tak: odczytanie przenosi się między rejestrami, a częstość nie.
Tabela częstości zbudowana z banku drzew powstaje z prozy literackiej i prasowej,
a rejestrem, o który olskiemu chodzi, jest dokumentacja techniczna,
więc nad dokumentacją taka tabela ma się mylić częściej, niż mówi jej własna ocena.
Fraza powtórzona w akapicie nie ma pod sobą żadnego korpusu,
więc nie ma też skąd i dokąd się przenosić.
Obala tę połowę przebieg, w którym częstość trafia nad dokumentacją tak samo dobrze
jak nad bankiem drzew, albo taki, w którym odczytanie z akapitu myli się od niej częściej.

Kosztuje to jednak coś, czego ranking nie kosztuje.
Powód wyczytany z tekstu bywa prawdziwy i nie mówi nic.
Zdanie, w którym fraza okolicznikowa stanęła przy `być`,
dowodzi o tym czasowniku tyle, ile dowodzi o dowolnym innym,
bo przy `być` taka fraza stoi wszędzie,
i dlatego świadek kontekstowy nad powtórzeniem przy kopuli milczy
([niżej](#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Częstość zmylić się tak nie może, bo jej powód jest dokładnie tym, co zmierzyła.
Klasa pustego powodu daje się odsiać tam, gdzie da się ją nazwać lematem,
a poza tym wyłapuje ją czytelnik, bo po to właśnie powód przy odpowiedzi jest,
czyli obroną jest dokładnie to, co kryterium kupuje.

Druga połowa jest zmierzona raz i próba tej wielkości jej nie rozstrzyga.
Dwa korpusy dają po jednej połowie tego, czego pomiar żąda:
bank drzew ma wzorzec i nie ma kontekstu,
a [korpus audytowy](audit-corpus.md#the-list) odwrotnie,
więc wzorzec dla rejestru czyta się ręką, a odpowiedzi
padają nad losowaniem z całej populacji rzadziej niż milczenie.
Stopę pomyłek daje dopiero losowanie zawężone do samych odpowiedzi
([częstość nad dokumentacją](#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)),
a tabela z banku drzew myli się nad nim w 5 z 29 odpowiedzi,
czyli tyle, ile jej własna ocena dopuszcza na próbie tej wielkości.
Przenoszenie się częstości zostaje przez to pytaniem o liczbę przeczytanych odpowiedzi,
a ile ich potrzeba, mówi wpis w [`TODO.md`](../TODO.md).

Ten sam przebieg mówi o kryterium powodu coś, czego stopa pomyłek nie mówi.
Odpowiedzi z powodem leżącym w słowach zdania jest tam 23 i żadna nie jest pomyłką,
a wszystkie pięć pomyłek pada wśród sześciu, w których powodu w słowach nie ma.
Kryterium postawione po to, żeby odpowiedź miała autorowi co powiedzieć,
dzieli więc tę próbę tam, gdzie dzieli ją trafność,
i nie było pod nim żadnego pomiaru, kiedy je stawiano.

## Tożsamość czytania jest tańsza i częściowo już stoi

Drugie z trzech pytań nie potrzebuje modelu ani banku drzew.
Dwa wyprowadzenia są jednym czytaniem, kiedy mają ten sam kształt,
a co do kształtu nie wchodzi, rozstrzyga `signature` w `olski/parse.py`
i opisuje [subset.md](subset.md#co-się-liczy-jako-jedno-czytanie):
lematy, wartości cech i część mowy są wyłączone rozmyślnie.
Każde takie wyłączenie to wieloznaczność, która przestała być raportowana,
zdjęta deterministycznie i bez ani jednego wyboru między czytaniami.
Tą samą drogą idą trzy zdania z klasy „sama liczba czytań”,
bo nawiasowanie ciągu współrzędnego jest tym, o czym sygnatura grubsza nie mówi.

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

Cztery piąte odrzuceń to przyłączenie,
a części tych przyłączeń nie rozstrzyga się rankingiem, tylko słownikiem.
Nad Składnicą 576 z 4 517 spornych wyrażeń to frazy, których czasownik żąda swoim schematem,
a 214 to frazy, których żąda sam rzeczownik;
liczby te wraz z ich rozkładem trzyma
[subset.md](subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia).
Po żadnej z tych stron nie ma konkurencji między czytaniami:
przeczytanie frazy wymaganej po drugiej stronie łamie schemat tego, kto jej żądał.

Olski taki leksykon ma i sięga nim po tę klasę.
`olski/leksykon.txt` niesie kolumnę przyimków, których żąda rama słowa,
i niesie ją po obu stronach sporu: przy czasowniku i przy rzeczowniku
([subset.md](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
bo Walenty, z którego ten plik powstaje, ma ramy także dla rzeczownika.
Kolumna jest rozszerzeniem generatora, a nie nową maszyną,
i mieści się w tym, co [etap 2](roadmap.md#etap-2-walencja) obejmuje.
Rozstrzygnięcie, które z niej wychodzi, jest deterministyczne i da się wyjaśnić
jednym wierszem leksykonu, czyli jest tym rodzajem odpowiedzi,
którą ten parser obiecuje w README.

Co z tej kolumny wziąć po każdej ze stron spornego wyrażenia, rozstrzyga pomiar,
a nie to, że jedna kolumna obsługuje oba:
[sekcja niżej](#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)
wycenia to kryterium osobno dla rzeczownika i dla czasownika,
i wypada ono po tych dwóch stronach zupełnie inaczej,
więc rzeczownik wskazuje gospodarza, a czasownik odbiera wskazanie.

Ile z tych 73,7% by to zdjęło, ten dokument nie mówi.
Zasięg i trafność kryterium wycenia tamta sekcja,
a to jest pytanie o zdania, nie o wyrażenia:
790 z 4 517 to wyrażenia, a 573 z 777 to zdania,
i jedno zdanie niesie ich czasem kilka.
Pomiar, który by te dwa mianowniki złożył, jest jedną z rzeczy, których tu brakuje.

## Rama rozstrzyga po stronie rzeczownika, a po stronie czasownika nie

Świadka ramowego wyceniono przed dopisaniem go, tak jak
[przysłówek](subset.md#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe),
i pomiar rozstrzygnął go na pół.
`harness/rama.py` pyta bank drzew, dokąd wyrażenie doszło u anotatora,
i zestawia to z samym kryterium, a nie z werdyktem.
Kryterium jest jedno i ma jednego właściciela — `przyimki` w `olski/walenty.py`,
skąd bierze je i ta sonda, i kolumna leksykonu:
lemat żąda przyimka, gdy któryś jego schemat
ma pozycję niepodmiotową z `prepnp` o tym przyimku.
Odpowiedź pada w tej sondzie wtedy, gdy żąda go dokładnie jedna strona.
Liczby drukuje `python3 -m harness.rama`.

Mianownik jest tam węższy niż `4 517` wyżej i węższy o jeden warunek.
Tamta liczba obejmuje każde przyłączenie w pozycji dwuznacznej,
a ta bierze same te, które doszły do rzeczownika albo do zdania,
bo tylko o takich świadek ma co powiedzieć:
kilkaset przyłączeń dochodzi do trzeciej kategorii — `fwe`, `fpt`, `fpm`, `fps` —
i wzorca dla wyboru dwóch stron nie dają.
`Report` w `olski/attachment.py` liczy tak samo w swoim rozkładzie po przyimku,
więc oba mianowniki są tam obok siebie.

Rama odpowiada nad dwiema piątymi spornych przyłączeń
i trafia w niespełna dwie trzecie odpowiedzi.
Sama ta para mówi, że świadka takiego brać nie warto:
[kolejność lasu](#nad-składnicą-olski-ma-ranking-którego-nikt-nie-trenował)
trafia bez żadnego słownika tyle samo albo więcej.

Rozstrzyga jednak strona, a nie średnia.
Rama rzeczownika myli się rzadziej niż raz na dwadzieścia odpowiedzi,
czyli rzadziej niż tabela skłonności przy zasięgu tej samej wielkości.
Rama czasownika trafia tyle, ile rzut monetą nad wyborem dwóch stron,
a odpowiedzi wydaje dwa razy więcej niż tamta.
Średnia z obu jest przez to liczbą o niczym:
opisuje mieszaninę świadka i szumu w proporcji, którą ustala korpus.

Powód widać po tym, co bank drzew mówi o tych samych odpowiedziach.
Tam, gdzie anotator postawił nad wyrażeniem frazę — wymaganą albo luźną —
kryterium trafia w dziewięciu wypadkach na dziesięć, po obu stronach naraz.
Tam, gdzie nie postawił żadnej, trafia w połowie,
a takich odpowiedzi jest większość i prawie wszystkie padają po stronie czasownika.
Znaczy to, że kryterium myli się nie na ramie, tylko na jej braku:
czasownik żąda przyimków tak licznie, że jego schemat pasuje do okolicznika,
o którym nie mówi nic.
Widać to na lematach, które padają w pomyłkach — `być` z `na`, `być` z `z`,
`mieć` z `w`, `powodować` z `w` —
czyli na tej samej klasie, przed którą warstwa rozstrzygająca broni się już
listą `KOPULY` w `olski/rozstrzyganie.py`.

Zwężenie do schematów o kwalifikatorze `pewny` tego nie naprawia i nie stoi.
Pod `--tylko-pewne` żadna z tych liczb nie rusza się o więcej niż pół punktu,
czyli pewność nie odróżnia ramy od okolicznika.
Zwężeniem, które by to zrobiło, jest przypadek grupy pod przyimkiem:
Walenty pisze `prepnp(o,loc)` obok `prepnp(o,acc)`,
a `Attachment` w `olski/attachment.py` niesie sam przyimek,
więc żaden przebieg tej sondy dziś tego nie pyta.

Świadek, który z tego wyszedł, bierze z kryterium połowę:
`Rama` w `olski/rozstrzyganie.py` wskazuje po stronie rzeczownika,
a po stronie czasownika nie wskazuje nikogo.
Wyceniono to tak samo jak przysłówek, czyli połowa na gospodarza,
a rozstrzygnęło się inaczej: tam obie połowy weszły,
bo druga kupowała prawdę o drzewie
([subset.md](subset.md#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe)),
a tutaj druga nie ma czym odpowiedzieć.
Wypada to zgodnie z próbą nad rejestrem, wziętą nad innym korpusem i inną ręką:
tam też rozstrzyga rama rzeczownika, i to w większości tych odpowiedzi,
które w ogóle rozstrzyga jakakolwiek rama
([częstość nad dokumentacją](#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)).
Dwa korpusy mówią więc to samo o tej samej połowie.

**Nad połową banku drzew, której świadek nie widział, rama rzeczownika
dorównuje tabeli skłonności zasięgiem i bije ją trafnością.**
Odpowiada na mniej więcej co ósme sporne wyrażenie, czyli tyle, co tabela,
i myli się rzadziej niż raz na dwadzieścia odpowiedzi tam,
gdzie tabela myli się w co dziesiątej.
Jedna z tych dwóch liczb kupuje się zwykle drugą — o tym mówi krzywa progów
w tym samym wydruku — a tutaj się nie kupuje, bo świadek progu nie ma:
odpowiada wtedy i tylko wtedy, gdy słownik żąda po jednej stronie.
Rama stoi przed tabelą — dowód słownikowy bije statystyczny — i tabela odzywa się
po niej tylko tam, gdzie rama milczy, więc obaj razem odpowiadają na mniej więcej
co piąte sporne wyrażenie przy niższej stopie pomyłek, niż ma sama tabela.
Kolejność ta nie jest przy tym porównaniem dwóch trafności, tylko
[hipotezą](#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza),
i z niej wynika też, czego rama nie bije: świadek kontekstowy stoi przed nią,
bo akapit mówi o tym tekście, a leksykon o polszczyźnie.
Wszystkie te liczby drukuje `python3 -m olski.rozstrzyganie <korpus> --oceń`,
bo ten przebieg mierzy warstwę, a nie kryterium nad samym Walentym.

**Rama czasownika zostaje za to wetem, a weto kosztuje zasięg.**
Świadek milczy, gdy przyimka żąda także czasownik,
i milczy z tego samego powodu, z którego nie wskazuje czasownika:
tam, gdzie żąda go i rzeczownik, i czasownik, schematu nie łamie żadne czytanie.
Cenę weta wypisuje wariant, a nie różnica między commitami,
a wypada ona dwa razy inaczej, bo świadek i warstwa tracą co innego.
Sama rama odpowiada bez weta blisko dwa razy częściej
i myli się wtedy w co trzynastej odpowiedzi zamiast rzadziej niż w co dwudziestej.
Warstwa traci mniej, bo część tego, co weto zdejmuje, podejmuje tabela za ramą:
bez weta odpowiada ona na przeszło co czwarte sporne wyrażenie zamiast na co piąte,
a myli się w co dziesiątej odpowiedzi zamiast w co trzynastej.

Weto nie jest więc darmowe, a rozstrzyga o nim to, czym ma być wskazanie.
Rama bez weta wskazuje rzeczownik także tam, gdzie tego samego przyimka
żąda również rama czasownika, czyli tam, gdzie żadne z dwóch czytań schematu
nie łamie, a wtedy powód mówi o jednej stronie i milczy o drugiej.
Wskazanie bez powodu jest u tej warstwy rankingiem, a rankingu
[ten dokument](#ranking-nie-jest-wyjściem-którego-ten-parser-potrzebuje) tu nie chce.
Warstwa bez weta wraca zarazem do stopy pomyłek tabeli,
czyli rama przestaje być tym dowodem lepszym, dla którego stoi przed nią.

Czego ten pomiar nie mówi, to ile zdań to zdejmuje.
Mianownikiem jest tu wyrażenie, a `573 z 777` niżej liczy zdania,
i jedno zdanie niesie takich wyrażeń czasem kilka,
więc złożenie dwóch mianowników zostaje tam, gdzie było.

Nie mówi też, ile świadek odpowiada nad rejestrem docelowym.
Zasięg ogranicza mu bowiem nie kryterium, tylko słownik:
plik rzeczownikowy Walentego wylicza dwa tysiące lematów,
więc rzeczownik spoza tej listy jest dla świadka rzeczownikiem bez ramy,
a nie rzeczownikiem, którego rama tej pozycji nie ma.

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
a takich jest 162 z 777.
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
a pod nimi stoi opis trzech świadków, których ta warstwa ma.

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
Kolejność ta jest [hipotezą tego dokumentu](#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza)
zapisaną w kodzie, a nie wynikiem porównania dwóch trafności.
Powód wraca razem ze wskazaniem, żeby wskazanie dało się sprawdzić bez zaglądania do tabeli.

**Świadkowie są trzej i jeden z nich jest tym, którego ten wywód wycenia najwyżej.**
Leksykon jest tańszy od rankingu i sekcja o nim tak go wycenia,
a `Rama` jest tym leksykonem pytanym o jedno przyłączenie.
Tożsamość czytania jest tańsza tym samym rachunkiem i tutaj jej nie ma
z powodu, który tamta sekcja podaje:
czeka ona na sąd o parze czytań, którego żaden korpus nie zapisuje.

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
0 of 2 sentences are olski, and 2 have a reading
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

Jednego lematu to dopasowanie nie bierze: kopuli.
Okolicznik przyłącza się do `być` w dowolnym zdaniu,
więc dwa zdania o wspólnym lemacie `być` mają wspólne tylko orzeczenie,
a nie miejsce, do którego fraza doszła.
Bez tego warunku `Zabronione jest tworzenie opisów w 1 osobie.` dostaje gospodarza `jest`
po zdaniu `Wymaga się, aby opisy tworzone były w 3 osobie liczby pojedynczej`,
choć fraza dochodzi w nim do `tworzenie opisów`.
Lematów jest pięć, bo bierzemy listę, którą gramatyka ma dla orzecznika
(`KOPULA` w `olski/subset.py`), zamiast pisać drugą o tym samym.
Cenę całej listy wypisuje sonda niżej, a `być` odpowiada nad tym korpusem za nią całą;
czy pozostałe cztery lematy do tego kryterium należą,
pyta wpis w [`TODO.md`](../TODO.md).

Warunek dotyczy dowodu, a nie pozycji.
Kopula zostaje gospodarzem, bo okolicznik całego zdania przyłącza się do orzeczenia,
a orzeczeniem jest w takim zdaniu właśnie ona:
`w 1 osobie` czyta się i jako warunek całego zakazu, nie tylko samych opisów.
Warstwa ma więc nad taką pozycją milczeć, a nie przestać jej widzieć.
Odpada przy tym sam dowód, więc kopula obok drugiego dowodu wskazania nie blokuje:
dwóch gospodarzy, przy których świadek milknie, liczy się po odsianiu takich par.

Przy gospodarzu fraza stanęła także wtedy, gdy dzieli je łańcuch imienny.
Sąsiad bezpośredni sam nie wystarcza, bo w łańcuchu dopełniaczowym jest nim ogon grupy:
w `wymiany danych z systemami zewnętrznymi` fraza dochodzi do `wymiany`, a nie do `danych`.
Łańcuch urywa pierwsza forma bez czytania imiennego,
więc w `nadawanie i funkcjonowanie uprawnień do przeglądania` spójnik odcina `nadawanie`.
Dwóch gospodarzy w jednym łańcuchu kończy się milczeniem,
tym samym warunkiem, którym kończy się fraza powtórzona przy obu:
sąsiedztwo powtarza wtedy sporne przyłączenie, zamiast je rozstrzygać.

**Nad rejestrem, o który chodzi, świadek ten odpowiada rzadziej niż o jednej pozycji na sto.**
`harness/powtórzenie.py` przechodzi prozę zdanie po zdaniu
i pyta go o każdą pozycję przyłączeniową, jaką morfologia w tym zdaniu widzi,
a obok zasięgu reguły wypuszczanej liczy zasięg każdego wariantu wycenianego niżej.
Korpusem jest [korpus audytowy](audit-corpus.md#the-list),
czyli dokumentacja techniczna wyekstrahowana do prozy tak, jak ten dokument mówi:

```sh
python3 -m harness.powtórzenie proza/
```

Pozycje wyznacza morfologia, a nie werdykt, i to jest cała różnica między tym pytaniem
a tym, które warstwa dostaje w `olski-check`.
Gramatyka odrzuca w tym rejestrze prawie każde zdanie,
więc werdykty stawiają tu kilkadziesiąt wyborów na blisko trzy tysiące zdań,
a `olski-check --rozstrzygaj` wypisuje pod nimi garść wskazań, wszystkie skłonności.
Świadek kontekstowy nad tą populacją nie odzywa się ani razu,
i jego zero jest tam w większości liczbą o gramatyce:
żaden świadek nie odpowie częściej, niż jest pytany.
Pozycja znaleziona morfologią stoi tam, gdzie polszczyzna daje dwa czytania,
niezależnie od tego, czy olski to zdanie rozbiera,
i jest tym pytaniem, które warstwa dostanie, kiedy gramatyka po nią sięgnie
(`pytania` w `olski/wieloznaczność.py`).
Populacja jest przez to ta sama, którą ma
[wzorzec czytany ręką](#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów),
więc zasięg zmierzony tutaj i trafność zmierzona tam mówią o jednych pytaniach.

Zasięg ten ma dwa mianowniki i tylko drugi z nich jest o świadku.

Pierwszy jest o rejestrze: cztery piąte jego zdań stoi pierwsze w swoim akapicie,
więc świadek nie ma tam czego przeczytać.
Zdań pierwszych jest przy tym tyle, ile akapitów,
bo każdy akapit ma zdanie pierwsze i żaden nie stoi bez zdania,
czyli akapit tego korpusu jest niewiele dłuższy od zdania.
Długość ta bierze się z tego, co ekstrakcja liczy za akapit,
a liczy za niego osobno każdą pozycję listy,
bo zdanie nie biegnie z jednej do następnej
([extraction.md](extraction.md)).
Ile z tych akapitów wyszło właśnie z list, nie mówi ani ten przebieg, ani żaden inny,
bo ekstrakcja nie wypuszcza typu węzła, z którego akapit powstał;
tego samego braku dotyczy wpis w [`TODO.md`](../TODO.md)
o mapowaniu trafień z powrotem na konstrukcje.

Drugi jest o świadku: fraza powtarza się przy gospodarzu
rzadziej niż raz na czterdzieści pozycji,
które mają w akapicie co przeczytać.

**Siedem odpowiedzi w granicy akapitu przeczytano i wszystkie wskazują dobrze.**
Dowód pod każdą jest tego samego kształtu, czyli frazą powtórzoną przy gospodarzu:
`prawem do dalszego przekazywania` po zdaniu z `bez prawa do dalszego przekazywania`.

**Warunek na kopulę wyceniono: zdejmuje jedno wskazanie i jest nim pomyłka.**
Wariant sondy podaje świadkowi pustą listę kopul, czyli bierze za dowód i powtórzenie
przy `być`, i wtedy odpowiada raz więcej.
Tym jednym wskazaniem jest opisane wyżej `w 1 osobie` → `jest`,
więc warunek kupuje zdjęcie jednej pomyłki,
a kosztuje nad tym korpusem zero wskazań dobrych.

**Granicę akapitu wyceniono: kupuje wielokrotnie więcej odpowiedzi i dwie odbiera.**
Wariant sondy podaje świadkowi cały dokument czytany wstecz zamiast akapitu,
a dwie z tamtych siedmiu wtedy milkną.
Milkną dlatego, że dalej w dokumencie ta sama fraza stoi przy drugim gospodarzu,
a dwóch gospodarzy kończy się milczeniem —
i są to `nowa faktura z datą PermanentStorage`
oraz `uprawnień pracownikom do przeglądania`, czyli dwa wskazania dobre.

Zakup ten jest zasięgiem i o trafności nie mówi nic sam z siebie.
Dziesięć odpowiedzi rozrzuconych po tych spoza akapitu (`rozrzucona` w `olski/próbka.py`)
czyta się jako sześć wskazań dobrych i cztery słabsze,
a pomyłki co do strony wyboru nie ma wśród nich żadnej:
`atrybutów posiadanych przez obiekt w systemie źródłowym` dostaje `obiekt`,
a `przekazanie danych o obiektach turystycznych` dostaje `danych`.
Jedno ze słabszych nazywa grupę jej przymiotnikiem, a nie głową:
`wyrażenia regularne dla adresów IP` dostaje `regularne`,
bo łańcuch imienny urywa się na przymiotniku i `wyrażenia` gospodarzem nie zostaje.
Drugie stoi na pozycji, która przyłączeniem nie jest,
bo Morfeusz czyta jako przyimek samotną literę `A` z nazwy podmiotu.
Trzecie trafia w gospodarza, a pozycji pod nim nie ma:
`kontekst w ktorym jestesmy uwierzytelnieni` dostaje `kontekst`,
tyle że `w którym` otwiera zdanie względne, a nie wyrażenie przyimkowe.
Czwarte stoi tam, gdzie obaj gospodarze mówią to samo:
w `nie przesłano żadnych faktur w sesji interaktywnej` fraza nazywa tę samą sesję,
dojdzie do `faktur` czy do `przesłano`.
Granica broni się więc nie tym, że wskazania spoza niej są złe,
tylko tym, po co ją tam postawiono ([sklad.md](sklad.md)),
a policzone jest i to, co jej zdjęcie kupuje, i to, co odbiera.

**Regułę kandydata wyceniono tą samą drogą, a węższa dokłada pomyłkę na łańcuchu.**
Wariant węższy pyta o samego sąsiada frazy i odpowiada częściej od wypuszczanego,
a różnica bierze się stąd, że łańcuch pokazuje czasem dwóch gospodarzy naraz,
a dwóch kończy się milczeniem.
Kupuje to pomyłkę, którą łańcuch omija:
`Wpływa to na sposób wymiany danych z systemem RIT.` dostaje gospodarza `danych`,
gdzie fraza dochodzi do `wymiany`.
Dowodem jest tam `wymiany danych z systemami zewnętrznymi`, czyli ten sam łańcuch,
więc powtórzenie jest prawdziwe, a odczytane z niego wskazanie nie.
Reguła wypuszczana widzi w tym łańcuchu obu gospodarzy naraz i o tym zdaniu milczy.

Wariant szerszy pyta o cały prefiks zdania i odpowiada rzadziej od obu.
Kandydatów ma najwięcej i dlatego najczęściej trafia na dwóch naraz,
więc reguła szersza od wypuszczanej kupuje mniej zasięgu, a nie więcej.
Kupuje za to gospodarza stojącego daleko przed frazą, którego łańcuch nie sięga,
i bywa nim czasownik żądający tej frazy swoim schematem:
w `Rozszerzono model żądania o właściwość boolean onlyMetadata`
wskazuje `Rozszerzono`, czyli ramę `rozszerzyć coś o coś`.
Jest to ten sam dowód, którego świadek ramowy nie wypuszcza jako wskazania:
po stronie czasownika bierze go za weto, i dlaczego, mówi
[sekcja o ramie](#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie).

Częstości pomyłek ten przebieg wobec tego nie podaje.
Siedemnaście odpowiedzi przeczytanych jest odczytem, a nie stopą,
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

Dowód tego świadka jest przy tym tego samego rodzaju co dowód
[rankingu](#ranking-nie-jest-wyjściem-którego-ten-parser-potrzebuje):
częstość wyuczona z banku drzew, pytana o jedno przyłączenie zamiast o całe drzewo.
Zarzut z tamtej sekcji go nie dosięga, bo werdyktu nie rusza,
a [kryterium powodu](#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza) dosięga:
odpowiada częstością nad korpusem, którego autor zdania nie czyta.
Jest tu wobec tego jedną z dwóch stron pomiaru, który tamtą hipotezę obala albo zostawia,
a nie świadkiem, którego ta warstwa miałaby rozbudowywać.

**Świadek ramowy odpowiada schematem i stoi między tymi dwoma.**
`Rama` pyta `olski/leksykon.txt` o to, czy rama rzeczownika żąda tego przyimka,
i wskazuje go wtedy, gdy rama czasownika go nie żąda,
czyli odpowiada tą częścią klasy, o której sekcja o leksykonie mówi,
że nie konkuruje z niczym.
Za świadkiem kontekstowym, bo akapit mówi o tym tekście, a leksykon o polszczyźnie,
i przed tabelą, bo dowód słownikowy bije statystyczny.
Co ten świadek kupuje i ile kosztuje jego weto, trzyma
[sekcja o ramie](#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie).

## Werdykt pyta warstwę o inny wybór niż bank drzew

Ocena wyżej mierzy świadka na czwórkach lematów wziętych z banku drzew,
a warstwę wypuszczaną pyta `olski-check` i pyta ją czym innym.
Pytaniem jest `Przyłączenie` z werdyktu:
gospodarze są formami, a nie lematami anotatora,
form tych bywa więcej niż dwie,
i lemat wybiera dopiero Morfeusz, wybierając ich kilka naraz.
Drogę drugą mierzy `harness/wskazania.py`, pytając o wzorzec drzewo wzorcowe:

```sh
python3 -m harness.wskazania Składnica-frazowa-180723/
```

Trzy rzeczy tego przebiegu trzymają się razem i osobno każda z nich myli.

Zasięg warstwy wypuszczanej wychodzi wyższy niż w ocenie wyżej,
bo tabela wypuszczana ma pary z całej Składnicy zamiast tych z jej połowy,
a lematów formy pyta się naraz kilku, więc para znajduje się częściej.
Populacja jest przy tym inna — przyłączenia liczone tutaj to te,
przed którymi wybór postawił olski,
a nie te, przed którymi postawił go anotator —
więc dwóch zasięgów nie odejmuje się od siebie.

Trafność tego przebiegu jest mierzona na materiale, który ta tabela widziała.
`olski/skłonności.txt` powstaje z całej Składnicy, a przebieg idzie po całej Składnicy,
więc liczba ta jest górnym oszacowaniem i pomiarem trafności nie jest.
Trafnością poza próbą jest ta z oceny wyżej, o kilka punktów niższa,
a przebieg dzielący korpus tak, jak dzieli go tamta, trzyma [`TODO.md`](../TODO.md).

Gospodarzy jest więcej niż dwóch w co czwartym przyłączeniu,
czyli w tylu wypadkach ocena z czwórek mierzy wybór łatwiejszy niż ten,
przed którym warstwa staje.
Wypadki te biorą się z produkcji, a nie z rzadkości:
`Obudziłem się na podłodze w kuchni z pustą paczką po ciasteczkach w dłoniach.`
ma cztery przyłączenia, a każde następne dostaje za gospodarza rzeczownik z poprzedniego.

Wzorca nie ma dla ponad ćwierci przyłączeń i nie jest to milczenie banku drzew.
Drzewo albo nawiasuje tę frazę inaczej, niż nazywa ją werdykt,
albo przyłącza ją do czegoś, co nie jest ani grupą imienną, ani zdaniem.
Drugie ma dwie kategorie i obie wypadają z tego samego powodu.
`Auta są kradzione dla okupu.` przyłącza frazę do imiesłowu,
a `Muszę jechać do domu.` do frazy werbalnej z bezokolicznikiem,
czyli dokładnie tam, gdzie stawia ją werdykt:
odpowiedź anotatora jest tu zgodna i mimo to nie liczy się jako wzorzec,
bo `CLAUSE` w `olski/attachment.py` tej kategorii nie wylicza.
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
i losuje spośród wszystkich, a jest ich w tym korpusie ponad tysiąc
(`rozrzucona` w `olski/próbka.py`).
Wyznacza je morfologia, a nie werdykt (`pytania` w `olski/wieloznaczność.py`),
bo werdykty stawiają nad tym rejestrem 49 wyborów na 2 915 zdań
i nie ma czego z nich losować.
Jest to ta sama populacja, którą liczy
[pomiar zasięgu](#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
i to on jest jej właścicielem, bo drukuje ją obok swojego polecenia.
Ręką dopisuje się gospodarza wraz z powodem,
a poprawia się przy tym frazę i gospodarzy:
budowniczy proponuje frazę przyimkiem wraz z trzema formami za nim,
więc sięga nią dalej, niż ona idzie,
a gospodarzy proponuje całym łańcuchem imiennym,
który homonimia przedłuża czasem przez orzeczenie.

```sh
python3 -m harness.wybory próba/wybory.txt
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
Jest to jedyne miejsce, w którym jego wskazanie stoi obok wzorca:
[pomiar zasięgu](#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)
pyta go o te same pozycje i wzorca do nich nie ma, więc czyta swoje odpowiedzi ręką.
Oba dowody są tego samego kształtu, czyli frazą powtórzoną przy gospodarzu:
`z prawem do dalszego przekazywania` po zdaniu z `bez prawa do dalszego przekazywania`,
oraz `uprawnień pracownikom do przeglądania` po zdaniu z `uprawnień do przeglądania`.
Drugi z nich jest tym, czego tabela skłonności nie umie:
fraza dochodzi tam do rzeczownika oddzielonego od niej celownikiem,
a bank drzew o takim szyku nie mówi nic.

Blisko dwie trzecie wyborów zostaje nierozstrzygniętych
i to jest właściwa liczba tej próby.
Warstwa nie myli się nad nią ani razu, co pilnuje `tests/test_wybory.py`,
i nie jest to zasługa progów, tylko ich ceny:
milczenie jest tu odpowiedzią w kilkunastu wypadkach na trzydzieści.
Trzydzieści wyborów wystarcza, żeby powiedzieć, że warstwa milczy częściej, niż odpowiada,
i nie wystarcza, żeby powiedzieć, jak często się myli;
tę drugą liczbę bierze [próba zawężona do odpowiedzi](#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania).

Losowanie padło przy tym nad populacją mniejszą od dzisiejszej:
`pytania` dawało wtedy 1 058 pozycji, a gospodarza proponowało ogonem łańcucha
imiennego, gdzie dzisiejsze daje 1 113 pozycji i głowę grupy.
Ta sama komenda puszczona teraz z `--ile 30` dzieli z tym plikiem dwa zdania z trzydziestu,
więc powiększenie próby jest przerysowaniem siatki, a nie dopisaniem wpisów do niej;
co z tym zrobić, pyta wpis w [`TODO.md`](../TODO.md).
Sądów tych to nie unieważnia, bo każdy stoi przy zdaniu i przy frazie wypisanych w całości,
a gospodarzy poprawiła ręka.

## Częstość nad dokumentacją myli się tam, gdzie nie rozstrzyga żadne słowo zdania

Próba wyżej losuje spośród wszystkich pozycji rejestru,
więc mówi, jak często warstwa odpowiada, a nie mówi, jak często się myli:
odpowiedzi pada w niej pięć i jedna pomyłka przesuwałaby stopę o dwadzieścia punktów.
Częstość pomyłek żąda mianownika, którym jest odpowiedź, a nie pozycja,
a taki mianownik daje losowanie zawężone do tych pozycji, nad którymi warstwa się odzywa:
odzywa się nad 122 z 1 113 pozycji korpusu audytowego, czyli nad co dziewiątą,
i spośród tych 122 losuje się trzydzieści (`z_odpowiedzią` w `harness/wybory.py`).
`próba/wybory-z-odpowiedzią.txt` jest tym losowaniem przeczytanym ręką
i jest osobnym plikiem, a nie częścią próby wyżej,
bo jeden wydruk z dwoma mianownikami czyta się jako jeden.

Wpisy pochodzą z losowania ze 123 pozycji, czyli o jedną szerszego:
tą jedną jest wskazanie świadka kontekstowego, odebrane wraz z dowodem z kopuli.
Próby to nie przerysowuje.
Wpisy te były odpowiedziami tabeli częstości w chwili losowania,
a dziś ponad połowę z nich oddaje świadek ramowy,
bo stoi przed tabelą i bierze wybór tam, gdzie rama rzeczownika go rozstrzyga.
Przerysowania żąda ta próba przez to już teraz:
mierzy dwóch świadków w proporcji, której nikt nie wylosował,
a co z tym zrobić, pyta wpis w [`TODO.md`](../TODO.md).

```sh
python3 -m harness.wybory próba/wybory-z-odpowiedzią.txt
```

Świadek kontekstowy nie odpowiada tu ani razu i mówi to o losowaniu, a nie o świadku:
odzywa się nad tym korpusem siedem razy, więc trzydzieści wylosowanych pozycji
nie musi trafić w ani jedną z nich i nie trafiło w żadną.
Ta próba mierzy przez to nad dokumentacją świadka ramowego i tabelę częstości razem,
a więcej wskazań ma rama.
Wpisów jest trzydzieści, a odpowiedzi 29, i różnica ta jest ceną poprawiania ręką:
zawężenie pyta o frazę i gospodarzy, jakich proponuje morfologia,
a przy jednym wpisie gospodarz okazał się jeden, bo drugim był spójnik.

**Pięć pomyłek na 29 odpowiedzi nie odróżnia tego rejestru od banku drzew.**
Tabela częstości mierzona na połowie banku drzew, której nie widziała,
myli się w co dziesiątej odpowiedzi (`WSPARCIE` i `PRÓG` w `olski/rozstrzyganie.py`),
a stopa taka daje pięć pomyłek albo więcej na 29 odpowiedziach raz na sześć przebiegów.
Stopa tych 29 jest przy tym stopą dwóch świadków razem, a tamta jednego,
więc zestawienie mówi mniej, niż mówiło, gdy odpowiadała sama tabela.
Druga połowa [hipotezy](#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza)
żąda pomyłek częstszych niż tam, więc ta próba jej nie obala i nie potwierdza;
ile odpowiedzi trzeba, żeby odróżniła, mówi wpis w [`TODO.md`](../TODO.md).

**Rozstrzyga natomiast, gdzie warstwa nad tym rejestrem odpowiada dobrze.**
Wpisy dzielą się na dwoje po tym, czy wybór rozstrzyga któreś słowo tego zdania.
Podział ten przeczytała ta sama ręka, która wpisała wzorce, i przy wydruku odpowiedzi
przed sobą, więc sprawdza się go po polach `powód`, a nie po liczbie pod nim.
Powód taki niosą 23 odpowiedzi: 19 rozstrzyga rama rzeczownika
(`informacja o czymś`, `dostęp do czegoś`, `prawo do czegoś`, `wniosek o coś`),
3 dopełnienie cząstkowe liczebnika (`posiadanie jednego z kilku uprawnień`),
a jedną wyrażenie stałe `w zależności od`.
Nad żadną z tych 23 warstwa się nie myli.
Zostaje 6 odpowiedzi, w których żadne słowo zdania wyboru nie rozstrzyga,
i nad nimi warstwa myli się pięć razy.
Szósta jest trafna i pokazuje, jak wąska jest granica tego podziału:
w `wypróbować kontakty z kolejnych jej pozycji` fraza wskazuje źródło,
a świadek ramowy wskazuje `kontakty`, bo `z` jest pozycją ramy „kontakt”,
której to zdanie nie realizuje.
Powód mija się więc z relacją i mimo to wypada na właściwego gospodarza.

Trzy z tych pięciu są konstrukcjami rejestru.
`Data i czas wystąpienia błędu w UTC.` podaje strefę, w której wypisano czas,
a warstwa dołącza `w UTC` do `błędu`, bo `w` jest pozycją ramy „błąd”.
`natychmiastowej rejestracji dokumentu w KSeF` mówi, gdzie zachodzi rejestracja,
a tabela dołącza frazę do dokumentu.
`W czasie przekazywania danych do systemu RIT` ma `w czasie` za ramę czasową,
a tabela bierze `czas` za gospodarza `do systemu RIT`.
Dwie pozostałe padają nad wpisami, nad którymi trafną odpowiedzią jest milczenie:
`zapewnienie równych warunków dostępu dla wszystkich użytkowników`
i `mają zastosowanie w kontekście fakturowania` mówią to samo, dokądkolwiek fraza dojdzie,
więc tabela odpowiada tam, gdzie nie ma na co.

Ten sam podział widać po wsparciu pary, którą tabela zacytowała.
Odpowiedzi opartych na dwóch wypadkach banku drzew, czyli na najniższym wsparciu,
jakie przechodzi próg, jest 7 i cztery z nich są pomyłkami;
z 22 opartych na trzech wypadkach albo więcej pomyłką jest jedna.
Trzy trafne spod wsparcia dwóch to trzy pozycje z liczebnikiem cząstkowym,
czyli klasa, którą rozstrzyga reguła, a nie częstość.
Wsparcie podniesione o jeden zdjęłoby więc nad tą próbą cztery pomyłki z pięciu
i trzy odpowiedzi z 29, a cenę po stronie banku drzew wypisuje `--oceń`;
ruch ten trzyma wpis w [`TODO.md`](../TODO.md).

Wniosek tej próby mówi więc, co ta tabela nad tym rejestrem robiła:
w 23 odpowiedziach z 29 zastępowała leksykon, a poza nimi myliła się pięć razy na sześć.
Cena świadka ramowego jest tym policzona po stronie rejestru, a nie tylko banku drzew,
i to ona rozstrzygnęła, że świadek wchodzi po stronie rzeczownika.
Sama próba jest przy tym starsza od niego: wpisy padły wtedy, gdy tabela
odpowiadała pierwsza, więc część tych 23 odpowiedzi wydaje teraz rama,
i tego ta próba nie mierzy; [`TODO.md`](../TODO.md) trzyma wpis o jej ponownym odczycie.

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
2 of 2 sentences are olski, and 2 have a reading
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
python3 -m harness.konwersy walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt
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

Czytania to jednak nie wybiera, a klasa, nad którą miałoby wybierać, jest tu jedna.
Temat wiąże kolejność, a dwa czytania takiego zdania mają jedną kolejność:
w `Koszt szynki przewyższa koszt bułki.`
grupa `Koszt szynki` stoi pierwsza i pod SVO, i pod OVS,
więc warunek nałożony na kolejność jest spełniony po obu stronach wyboru.
Wersja, która wybiera — temat jest podmiotem — wybiera na tej parze źle:
po `Bułka jest tania.` tematem jest bułka,
więc podmiotem wypada `koszt bułki`, czyli czytanie OVS,
a czytelnik czyta SVO, bo z tamtego zdania bierze taniość, a nie rolę.
Przyłączenia ten dowód nie dotyczy wcale:
fraza stoi tam, gdzie stoi, niezależnie od tego, do czego dochodzi.

Zostaje z tego wyjście innego rodzaju i nie jest nim wybór czytania.
Temat mówi, gdzie grupa znana ma stanąć,
więc zdanie, które stawia ją gdzie indziej, da się zgłosić autorowi —
a to jest ten sam ruch, który po drugiej stronie robi już
`olski/skład/przegląd.py`, kiedy napis nie oddaje ról ([sklad.md](sklad.md)).
Pomiar niderlandzki cytowany wyżej mówi tyle, że zdanie poprzednie ten wybór czytelnikowi rozstrzyga,
i tamta para rozstrzyga go rolą, a nie kolejnością: po „pacjent wyleczył lekarza”
znany uczestnik wraca w roli, którą tamto zdanie mu dało.
Dowodem, który tak działa, jest wynikanie niżej.

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
[Próba zawężona do odpowiedzi](#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)
ma dwa takie wpisy i do tej podstawy nie dochodzi:
jej mianownikiem jest odpowiedź warstwy, a nie pozycja rejestru,
więc udział `oba` mówi w niej o tym, gdzie warstwa się odzywa, a nie o rejestrze.

Cztery rzeczy zostają wobec tego nierozstrzygnięte.

Ile z 453 zdań, w których przyłączenie jest całą decyzją,
zdjęłaby rama rzeczownika — ta połowa kryterium, którą pomiar przyjmuje.
Zasięg i trafność są wzięte nad wyrażeniem, a to pytanie jest o zdanie,
więc zostaje złożenie dwóch mianowników, a nie sam pomiar kryterium.

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
- <https://www.wuw.pl/data/include/cms/Automatyczna_analiza_skladnikowa_Wolinski_Marcin_2019.pdf> —
  Woliński, *Automatyczna analiza składnikowa języka polskiego*, 2019,
  gdzie rozdział 7 zestawia PCFG z maksimum entropii nad lasami Świgry:
  skąd liczby cech, przewaga cech lekkich
  i zysk ze zdjęcia rozróżnienia frazy wymaganej od luźnej
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
- <https://aclanthology.org/P88-1012.pdf> —
  Hobbs i Stickel, *Interpretation as Abduction*, ACL 1988,
  gdzie wieloznaczność składniową zdejmuje się tym samym wnioskowaniem co odniesienie:
  zostaje czytanie, które da się wyjaśnić najmniejszym założeniem dołożonym do wiedzy tłowej
- <https://www.cl.cam.ac.uk/~aac10/papers/mrs.pdf> —
  Copestake, Flickinger, Pollard i Sag, *Minimal Recursion Semantics: An
  Introduction*, gdzie niedookreślenie zastępuje wybór między czytaniami
- <https://aclanthology.org/2023.emnlp-main.51/> —
  Liu i inni, *We're Afraid Language Models Aren't Modeling Ambiguity*, EMNLP 2023,
  gdzie ujednoznacznienia GPT-4 uznano za poprawne w 32% wobec 90% dla zbioru
