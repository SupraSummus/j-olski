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
a `olski/rozstrzyganie.py` jest zalążkiem odpowiadającym obok werdyktu i nie ruszającym go.
Co ten zalążek wskazuje i ile się myli, mówi
[rozstrzyganie.md](rozstrzyganie.md), a kształt tamtej warstwy wynika z wywodu niżej.

Trzy pytania niżej są o czytaniach, które las trzyma,
a zdanie niesie jeszcze wieloznaczność, która do lasu nie dochodzi:
`Wynajmę mieszkanie.` olski przyjmuje i mówi o nim „jedno odczytanie”,
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
Las wydaje czytania w kolejności, którą ustala
`wyprowadzenia` w `olski/parse/las.py` ([sekcja niżej](#kolejność-czytań-ustala-koszt-i-późne-domknięcie)),
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

### Kolejność czytań ustala koszt i późne domknięcie

Kolejność, którą mierzy sekcja wyżej, jest deklaracją.
Las porządkuje ciała jednej pozycji trzema rzeczami po kolei
(`wyprowadzenia` w `olski/parse/las.py`):
kosztem, potem miejscem cięcia, a na końcu etykietą córki.
Werdyktu żadna z nich nie rusza — czytań jest tyle samo i mówią to samo —
więc rozstrzygają one o tym, co czytelnik widzi u góry wydruku
i co mieści się w czytaniach wypisywanych przed granicą wyliczania.

Koszt jest liczbą całkowitą i mówią o nim dwie rzeczy naraz:
produkcja, którą ciało złożono, oraz morfologia, na której ono stoi.
Całkowitą, bo jest deklaracją, a nie wagą wyuczoną:
koszt ułamkowy byłby logarytmem prawdopodobieństwa,
czyli tym modelem, którego [ten dokument nie chce](#ranking-nie-jest-wyjściem-którego-ten-parser-potrzebuje).

Kosztu produkcji nie sposób wypisywać przy każdej,
bo jest ich tysiąc kilkaset, z czego blisko połowa to samo `orzeczenie`,
a wypisuje je rozwinięcie z jednej deklaracji.
Liczby są przez to trzy i wszystkie mówią to samo:
ciało wypisane w deklaracji jest tym podstawowym.
Dwie wyliczają koszt z deklaracji (`olski/precedencja.py`) —
konstytuent bierze okolicznik, a jego córki stoją w innym szyku niż wypisany —
a trzecia mówi o jednej rodzinie produkcji, że jest konstrukcją nacechowaną,
i jest nią orzecznik wysunięty przed kopulę (`olski/subset/zdanie.py`).

Czwarta liczba wycenia morfologię i orzeka o słowniku, a nie o gramatyce:
czytanie oparte na formie, którą SGJP opatrzył kwalifikatorem odsyłającym ją
poza ten rejestr, schodzi niżej od czytania, które na takiej formie się nie opiera
(`olski/rejestr.py`).
Częstością liczba ta nie jest i być nie może, bo słownik częstości nie zna:
niesie on przy czytaniu nazwy i kwalifikatory, a licznika nie niesie żadnego.
Kwalifikator mówi przy tym o formie więcej niż jedną rzecz i tylko jedna z nich
jest rejestrem, więc odsyłające wypisuje lista, a nie wzorzec;
wywód tego podziału wraz z ceną trzyma
[formy-i-leksemy.md](formy-i-leksemy.md#kwalifikator-mówi-o-formie-dwie-rzeczy-i-tylko-jedna-jest-rejestrem),
a tę samą listę czyta synteza, która formę odesłaną zdejmuje zamiast liczyć ją kosztem.

Koszt morfologii idzie w górę, a koszt produkcji zostaje przy swoim ciele,
i jest to ten sam warunek czytany dwa razy:
koszt rozstrzyga między ciałami jednej pozycji,
więc zostaje tam, gdzie konkurencja jest, a idzie wyżej, gdy jej nie ma.
Ciała córki rozstrzygnęła sama córka,
a czytania formy nie rozstrzyga nikt, bo liść ciał nie ma:
dwa czytania jednej formy są jednym liściem (`Pozycja` w `olski/parse/czytanie.py`).
Koszt morfologii liczony na miejscu nie ruszyłby przez to ani jednego zdania.

Cięcie rozstrzyga ciała jednego kosztu i idzie rozpiętością malejąco,
czyli przepuszcza przodem to czytanie, w którym wyrażenie dołączyło
do konstytuentu stojącego tuż przed nim, a nie do tego wyżej.
Nazywa się to domknięciem późnym, a kierunek wybrano pomiarem,
bo argumentu z góry na niego nie było.

Zmierzono nad Składnicą każdą z tych rzeczy osobno
i pomiar mówi jedno: rozstrzyga cięcie, a koszty niemal nie.
Cięcie odwrócone na rosnące traci co dziesiąte trafienie w złote czytanie,
czyli spada z niespełna sześciu na dziesięć poniżej pięciu.
Koszty przy dobrym cięciu ruszają kilka zdań na dwa tysiące,
a wyjątkiem jest sam znak kosztu okolicznika:
czytanie z okolicznikiem postawione przed czytaniem bez niego
traci prawie tyle, co odwrócone cięcie.

Zostały mimo to i jest to decyzja, a nie odczyt.
Rozstrzygają zdania, o których ten korpus nie ma zdania:
bez kosztu szyku `Janek lubi piwo.`, a bez kosztu wysunięcia `On jest wolny.`
wychodzą pierwszym czytaniem odwróconym,
bo ciała o córkach tej samej rozpiętości rozstrzyga wtedy alfabet etykiet.
Bank drzew ma oba szyki i koszt wygrywa nad nim tyle zdań, ile traci,
więc pomiar milczy i rozstrzyga sama deklaracja:
szyk wypisany w niej jest podstawowy, a wysunięcie jest nacechowane.
Czwarty koszt produkcji nie został: odsunięcie okolicznika od końca konstytuenta
wyceniano tak samo i nie rusza ono ani jednego zdania,
bo miejsca okolicznika różnią się rozpiętością córek, a o tych mówi już cięcie.

**Kosztu morfologii ten pomiar nie widzi wcale i jest to brak w przyrządzie.**
Bank drzew mierzy się morfologią złotą, czyli czytaniem wziętym z drzewa
wzorcowego, a takie czytanie kwalifikatora nie niesie
([corpus.md](corpus.md#what-the-corpus-contains)),
więc nad Składnicą koszt ten jest zerem przy każdej formie i cały wydruk
wychodzi ten sam co bez niego, co do wiersza.
Co mierzy, widać przez to nad prozą tego repozytorium, a mierzy niewiele:
przestawia pierwsze czytanie kilkunastu zdań na blisko siedem tysięcy,
werdyktu nie ruszając w żadnym.
Kilka z nich przestawia w stronę czytania trafnego —
`Wszystko jest podmiotem.` wychodziło pierwszym czytaniem z `Wszystko`
w okoliczniku, bo przysłówek `wszystko` jest u Morfeusza regionalizmem —
a większość przestawia w obrębie zdań, których gramatyka i tak nie czyta dobrze.
To jedno zdanie trzyma `tests/test_kolejność.py`, bo nad Składnicą nie ma czego
trzymać; co zrobić, żeby pomiar zobaczył resztę, mówi [`todo/`](../todo/README.md).

Kolejności dopisań nie widać w żadnej z tych trzech rzeczy i to jest cel.
Przestawiona zmieniałaby pierwsze czytanie mniej więcej w połowie zdań
wieloznacznych README, a werdyktu nie ruszała w żadnym;
że dziś nie zmienia żadnego, pilnuje `tests/test_kolejność.py`.
Sama liczba trafień na tym nie zyskała, bo kolejność dopisań trafiała podobnie,
i nie to było pytaniem: liczba z sekcji wyżej wisiała na czymś,
czego nikt nie zadeklarował, więc ruszało ją każde przestawienie produkcji
i nie było tego widać w przeglądzie.

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
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy)),
a zdanie okolicznikowe oraz interpunkcja zdaniowa idą tą samą drogą
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania),
[konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
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
a zdejmuje się ją słownikiem albo produkcją
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)),
a nie warstwą za parserem.

Druga to trzy zdania, nad którymi werdykt nie mówi nic poza liczbą czytań,
a w każdym z nich czytania różni ciąg współrzędny.
Ciąg nie dostaje wiersza o konstytuencie rozmyślnie,
bo granicę członu pokazuje nawias w napisie roli;
nawias obejmuje jednak ciąg, którym jest sama rola,
a nie ciąg stojący w wypełnieniu głębiej
([parsowanie.md](parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)),
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
Ile jest których, notuje [`todo/`](../todo/README.md).

## Ranking nie jest wyjściem, którego ten parser potrzebuje

Liczby wyżej mówią, że ranking nad tym lasem jest do zbudowania
i że stanie gdzieś między dwiema trzecimi a trzema czwartymi trafień.
Osobne jest pytanie, co olski dostaje, gdy go weźmie, i odpowiedź jest ujemna.

Ranking zamienia werdykt `ambiguous` na `valid` wraz z domysłem.
Zdanie, o którym parser dziś mówi „dwa czytania, oto one”,
mówiłoby wtedy „jedno czytanie”, i myliłoby się co trzecie albo co czwarte.
Werdykt olskiego jest właśnie tym, że tego nie robi
([subset.md](subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego)),
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
([rozstrzyganie.md](rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
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
([częstość nad dokumentacją](rozstrzyganie.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)),
a tabela z banku drzew myli się nad tą próbą tyle,
ile jej własna ocena dopuszcza na próbie tej wielkości.
Przenoszenie się częstości zostaje przez to pytaniem o liczbę przeczytanych odpowiedzi,
a ile ich potrzeba, mówi wpis w [`todo/`](../todo/README.md).

Ten sam przebieg mówi o kryterium powodu coś, czego stopa pomyłek nie mówi.
Odpowiedzi z powodem leżącym w słowach zdania jest tam większość i żadna nie jest pomyłką,
a wszystkie pomyłki padają wśród tych kilku, w których powodu w słowach nie ma.
Kryterium postawione po to, żeby odpowiedź miała autorowi co powiedzieć,
dzieli więc tę próbę tam, gdzie dzieli ją trafność,
i nie było pod nim żadnego pomiaru, kiedy je stawiano.

## Tożsamość czytania jest tańsza i częściowo już stoi

Drugie z trzech pytań nie potrzebuje modelu ani banku drzew.
Dwa wyprowadzenia są jednym czytaniem, kiedy mają ten sam kształt,
a co do kształtu nie wchodzi, rozstrzyga `signature` w `olski/parse/czytanie.py`
i opisuje [subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie):
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
Nad Składnicą przeszło co ósme sporne wyrażenie jest frazą,
której czasownik żąda swoim schematem,
a blisko co dwudzieste jest frazą, której żąda sam rzeczownik;
liczby te wraz z ich rozkładem trzyma
[subset.md](subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia).
Po żadnej z tych stron nie ma konkurencji między czytaniami:
przeczytanie frazy wymaganej po drugiej stronie łamie schemat tego, kto jej żądał.

Olski taki leksykon ma i sięga nim po tę klasę.
`olski/leksykon.txt` niesie kolumnę przyimków, których żąda rama słowa,
i niesie ją po obu stronach sporu: przy czasowniku i przy rzeczowniku
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
bo Walenty, z którego ten plik powstaje, ma ramy także dla rzeczownika.
Kolumna jest rozszerzeniem generatora, a nie nową maszyną.
Rozstrzygnięcie, które z niej wychodzi, jest deterministyczne i da się wyjaśnić
jednym wierszem leksykonu, czyli jest tym rodzajem odpowiedzi,
którą ten parser obiecuje w README.

Co z tej kolumny wziąć po każdej ze stron spornego wyrażenia, rozstrzyga pomiar,
a nie to, że jedna kolumna obsługuje oba:
[sekcja o ramie](rozstrzyganie.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)
wycenia to kryterium osobno dla rzeczownika i dla czasownika,
i wypada ono po tych dwóch stronach zupełnie inaczej,
więc rzeczownik wskazuje gospodarza, a czasownik odbiera wskazanie.

Ile odrzuceń za przyłączenie by to zdjęło, ten dokument nie mówi.
Zasięg i trafność kryterium wycenia tamta sekcja,
a to jest pytanie o zdania, nie o wyrażenia:
obie klasy wyżej liczą wyrażenia,
a [rozbicie klas](#czym-różnią-się-czytania-które-olski-odrzuca) liczy zdania,
a jedno zdanie niesie wyrażeń czasem kilka.
Pomiar, który by te dwa mianowniki złożył, jest jedną z rzeczy, których tu brakuje.

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
a zdanie takie jest przeszło co piątym z tych, które sporne przyłączenie niosą.
Powyżej sufitu nie ma modelu, jest budowanie kontekstu,
czyli zadanie, którego ten parser nie stawia i którego wykonania nie umiałby wyjaśnić.

Olski ma przy tym poziom nad zdaniem i ma go po drugiej stronie.
Opowieść w `olski/skład/` wie to, czego zdanie samo o sobie nie wie:
kiedy to było i o kim mowa była przed chwilą,
i z tego bierze czas przeszły oraz podmiot opuszczony
([kategorie-zapisu.md](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)).
Kierunek parsujący takiego poziomu nie ma:
`olski/document.py` dzieli tekst na zdania i każde oddaje gramatyce osobno.
Warstwa rozstrzygająca kontekstem byłaby więc drugim kompilatorem,
a nie filtrem za pierwszym, i to jest cena, której żaden z tych pomiarów nie liczy.

## Wieloznaczność, której werdykt nie melduje

Wszystko wyżej pyta o zdanie, po którym zostaje czytań kilka.
Bywa jednak i tak, że zostaje jedno wyprowadzenie,
a zdanie mimo to czyta się dwojako:

```sh
python3 -m olski.check --readings -c "Wynajmę mieszkanie. Znam go."
```

```text
<text>: Wynajmę mieszkanie.
        - dopełnienie: mieszkanie, orzeczenie: Wynajmę
<text>: Znam go.
        - dopełnienie: go, orzeczenie: Znam
zdań: 2; wieloznaczne: 0; bez odczytania: 0
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
[warstwa-leksykalna.md](warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on),
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
a zdania, na które ten przekład Walentego zawęża (tamże), nie są o nim.

Deklaracji nie trzeba przy tym wymyślać, bo wydanie TEI z tej samej daty ma ją gotową:
`wynająć` dostaje tam cztery nazwane znaczenia, `ktoś komuś` i `od kogoś` wśród nich,
a osobna warstwa wiąże argument ramy z pozycją schematu
([prior-art.md](prior-art.md#polish-language-resources)).
Warstwę tę mają dwie piąte lematów tego słownika,
więc ruch pierwszy ma źródło dla części czasowników, a nie dla wszystkich.

Cena pierwszego ruchu jest widoczna od razu:
zdania, które dziś wychodzą `valid`, wychodziłyby `ambiguous`.
Ilu lematów to dotyczy, liczy sonda nad tym samym plikiem.
Szuka ona konwersów, czyli par czytań opowiadających jedno zdarzenie z dwóch stron:

```sh
python3 -m harness.konwersy walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt
```

Wraca 144 lematy z 17 224, każdy z parą schematów,
z których jeden ma odbiorcę w celowniku, a drugi źródło pod `od` albo `u`.
Kryterium jest zgadywaniem z kształtu pozycji, bo role nazywa wydanie TEI,
a sonda chodzi po wydaniu tekstowym z 18 kwietnia 2016,
którego README wylicza jego pliki i są to schematy dla czterech części mowy.
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
Drugą stronę zmierzyłby przebieg nad korpusem i trzyma go [`todo/`](../todo/README.md).

`Znam go.` jest drugą połową tej klasy i tam leksykon walencyjny milczy.
Schematy, które `znać` u Walentego ma, różnią się kształtem dopełnienia,
a nie tym, jak się kogoś zna,
więc oba czytania mieszczą się pod tym samym.
Milczy tam i warstwa semantyczna wydania TEI, bo `znać` nie ma w niej ani jednej ramy.
Źródłem byłby wobec tego słownik znaczeń, a nie słownik walencyjny,
i pierwszym kandydatem zostaje plWordNet,
na którym waży już nie licencja, tylko pobranie
([prior-art.md](prior-art.md#polish-language-resources)).

## Kontekst rozstrzyga wykluczeniem, a nie rankingiem

[Ranking](#ranking-nie-jest-wyjściem-którego-ten-parser-potrzebuje) odpadł na tym,
że zamienia `ambiguous` na `valid` wraz z domysłem.
Kontekst pozwala na ruch innego rodzaju:
nie wybiera czytania lepszego, tylko zdejmuje to, któremu sąsiedztwo przeczy.
Kiedy zostaje jedno, zdanie ma w tym tekście jedno czytanie, a nie czytanie zgadnięte.
Kiedy zostają dwa, werdykt wychodzi taki sam, jaki był bez tej warstwy.
Milczenie jest więc odpowiedzią domyślną, tak jak u [świadka](rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
a różnica wobec rankingu leży w tym, ile kosztuje brak odpowiedzi: nic.

Cena jest gdzie indziej i jest większa.
Werdykt przestaje być o zdaniu:
`Wynajmę mieszkanie.` ma samo dwa czytania, a w tamtym tekście jedno,
więc to samo zdanie dostaje dwie odpowiedzi zależnie od tego, co je otacza,
i przestawienie akapitu rusza werdykt bez ruszania zdania.
Jednoznaczność jest własnością zdania na swoim miejscu, a nie zdania samego,
bo jednostką sprawdzaną jest tekst
([roadmap.md](roadmap.md#podzbiór-jest-umową-a-nie-zasięgiem)),
i tę właśnie cenę ta decyzja przyjęła.

Dowody, na których taka warstwa mogłaby stanąć, są trzy
i idą w tej samej kolejności co u świadka, czyli od słownikowego w dół.

**Uczestnik nazwany obok.**
`Wynajmę mieszkanie. Wynajmę je od Anki.` rozstrzyga się samym leksykonem:
druga fraza obsadza pozycję, którą ma jeden ze schematów, a drugi nie.
Wersja trudniejsza — `Szukam ułożonego lokatora.` — żąda jednego kroku więcej,
bo `lokator` jest tym, kto stoi w pozycji celownikowej,
a tego, że nim jest, Walenty nie mówi;
mówi to dopiero słownik wiążący rolę ze słowem, czyli to samo źródło, którego żąda `znać`.

Połowa tego kroku jest zrobiona i leży w `olski/żądania.txt`:
pozycja schematu niesie tam rolę wraz z klasą rzeczy, której żąda,
przełożoną z warstwy semantycznej wydania TEI
([warstwa-leksykalna.md](warstwa-leksykalna.md#żądanie-pozycji-jest-osobnym-plikiem-a-nie-kolumną-leksykonu)).
Połowy drugiej — czy słowo stojące w tej pozycji do tej klasy należy —
morfologia nie zastępuje.
Świadkiem osoby jest w niej rodzaj męskoosobowy i nic poza nim,
bo `Anna` ma ten sam znacznik co `szafa`.
Filtr zdejmujący czytanie, w którym podmiot pozycji żądającej człowieka
jest rzeczownikiem męskim nieosobowym,
zdejmuje nad prozą tego repozytorium coś w czterech zdaniach,
przeczytanych potem co do jednego,
a dwóm z nich zabiera wszystkie czytania.
Te dwa są polszczyzną — `Odpadają przez to dwa rodzaje schematu.`
oraz zdanie, w którym `zażąda` czegoś `któryś etap` —
czyli filtr trafia w metonimię, którą
[CLAUDE.md](../CLAUDE.md#dla-kogo-jest-napisane-zdanie) zostawia w prozie wprost.
Ten sam pomiar odrzuca zarazem
[świadka odpowiadającego obok werdyktu](rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
bo pomyłką są dwa trafienia z czterech, a świadek ma nazywać swoją częstość pomyłek.
Miejsca na taki filtr nie brakuje, bo czytania tej prozy
spierają się o głowę podmiotu często;
brakuje słownika, bo ram nie mają czasowniki najczęstsze (tamże).

Żądanie człowieka trafia przy tym w tę klasę i trafia w niej źle,
a powód jest mechaniczny.
Synkretyzm mianownika z biernikiem żąda formy synkretycznej po obu stronach sporu,
a mają ją rzeczownik męski nieosobowy, nijaki oraz żeński na spółgłoskę.
Nie-człowiekiem filtr czyta pierwszy z tych trzech rodzajów,
czyli strzela w środek tej klasy, a nie obok niej.
`Anna zapisuje plik.` ma przez to jedno czytanie, bo biernikiem jest `Annę`,
a `Program zapisuje plik.` ma dwa.
Filtr żądający człowieka zdejmuje więc czytania tam, gdzie ta klasa jest,
a tam, gdzie jej nie ma, nie zdejmuje żadnego —
i widać to po tym, w co trafił, bo `któryś etap` i `dwa rodzaje schematu`
są rzeczownikami tej właśnie odmiany.
Czego ta klasa żąda od wordnetu, mówią dwa zdania, a żądanie nad nimi olski już czyta.
`Program drukuje werdykt.` ma dwa czytania,
a `drukować` żąda w podmiocie klasy `PODMIOTY`, a w dopełnieniu `KOMUNIKAT`,
więc jedno pytanie — czy `werdykt` do pierwszej z nich należy — zdejmuje czytanie drugie.
`Dokument opisuje pomiar.` ma dwa czytania i żądanie ich nie dzieli:
`opisywać` bierze w podmiocie pięć klas, a w dopełnieniu jedenaście,
i obie grupy mieszczą się po obu stronach.
Drugie z tych zdań jest przykładem negatywnym i jest mocniejsze
niż zdanie, którego czasownik żądania nie ma:
żądanie tu jest, zostało przeczytane i nie wystarczyło,
więc warstwa, która to zdanie rozstrzygnie, ma na nim pomyłkę, a nie zasięg.

Zdanie celu wybiera się przy tym z lematów tego pliku, a nie z prozy repozytorium.
`olski/żądania.txt` niesie przeszło sześć tysięcy lematów,
a nie ma wśród nich `gonić`, `zapisywać`, `sprawdzać` ani `zasłaniać`,
więc `Mysz goni ogon.` i `Kufer zasłania lustro.` są dla tej warstwy niewidzialne.
Jest to ta sama luka, którą prior-art nazywa przy `być`, `mieć` i `czytać`:
ramy nie mają czasowniki najczęstsze, a rejestr stoi właśnie na nich.

Miarę osoby ta warstwa dostała lepszą, a czytania zdejmuje dalej tak samo, czyli wcale.
Deklaracja osób projektu orzeka o klasach osobowych bez wordnetu
([warstwa-leksykalna.md](warstwa-leksykalna.md#deklaracja-projektu-rozstrzyga-żądanie-osoby)),
więc `któryś etap` przestaje być nie-człowiekiem przez samą swoją odmianę:
orzeka o nim to, czy autor wpisał go między osoby.
Przesłanki filtra to jednak nie naprawia, bo zła była w nim nie miara,
tylko założenie, że rzecz w pozycji osoby jest usterką.
Ta proza pisze `reguła żąda` rozmyślnie,
więc czytanie zdjęte na żądaniu osoby ginęłoby i tam, gdzie autor je napisał,
i tak właśnie zginęły czytania zdaniom, które pomiar wyżej wypisał.
Deklaracja wypisuje przez to pozycję i zostawia sąd czytelnikowi.

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
`olski/skład/przegląd.py`, kiedy napis nie oddaje ról
([po-wypisaniu.md](po-wypisaniu.md#drzewo-jest-jednoznaczne-a-napis-z-niego-nie-musi-być)).
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
mówi [sekcja o zalążku](rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek).

Jedno widać dopiero po uruchomieniu i osłabia dwa pierwsze dowody naraz.
Sąsiedztwo, które ma rozstrzygać, samo bywa nieolskie:
`Szukam ułożonego lokatora.` gramatyka odrzuca,
bo `szukać` stoi w `olski/leksykon.txt` jako czasownik, który biernika nie bierze,
a dopełniacza dopełnieniowego olski nie ma.
Warstwa czytałaby więc zdanie sąsiednie czymś słabszym niż gramatyka,
formami i lematami z Morfeusza,
tak jak nad rejestrem czyta je `harness/wieloznaczność.py`.

## Wzorzec na tę warstwę jest po drugiej stronie

Pomiar takiej warstwy wygląda na droższy niż wszystko wyżej,
bo bank drzew jest zbiorem zdań stojących osobno,
a wzorcem musiałby być tekst wraz z czytaniem, o które w nim chodziło.
Olski taki materiał wytwarza i wytwarza go za darmo.
Drzewo, z którego skład wypuszcza tekst, ma uczestników wymienionych,
tożsamość rzeczy niesie w nim `Postać`, a czas i to, o kim mowa — `Kontekst`
([kategorie-zapisu.md](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)),
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
[open-questions.md](open-questions.md#znalezisko-wieloznaczności-nie-mówi-czy-ma-ją-też-czytelnik),
a ile ich niesie werdykt, mierzy tabela wyżej.
Czego brakuje między nimi, to sąd nad parą,
i dwadzieścia cztery zdania przeczytane raz jedną ręką
są za wąską podstawą, żeby na nim stanąć;
tamten dokument mówi to o swojej próbce sam.

[Wybory przeczytane ręką](rozstrzyganie.md#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów)
odpowiadają na to pytanie w jednym wpisie na piętnaście
i odpowiadają na nie po drodze, a nie wprost:
`oba` znaczy tam, że czytelnik wyboru nie widzi, choć pozycja go stawia.
Dwa takie wpisy z trzydziestu są tego samego rzędu co próbka wyżej,
więc podstawy nie poszerzają;
poszerzy ją dopiero ten plik, kiedy urośnie, a nie osobny pomiar obok niego.
[Próba zawężona do odpowiedzi](rozstrzyganie.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)
ma dwa takie wpisy i do tej podstawy nie dochodzi:
jej mianownikiem jest odpowiedź warstwy, a nie pozycja rejestru,
więc udział `oba` mówi w niej o tym, gdzie warstwa się odzywa, a nie o rejestrze.

Cztery rzeczy zostają wobec tego nierozstrzygnięte.

Ile z 453 zdań, w których przyłączenie jest całą decyzją, zdjęłaby
[rama rzeczownika](rozstrzyganie.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie) —
ta połowa kryterium, którą pomiar przyjmuje.
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
  skąd rozbiór stu błędów i sufit zadania na 92,6%
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
