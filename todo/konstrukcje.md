# Konstrukcje, których gramatyka nie ma

Zdanie z łącznikiem `to` nie ma miejsca na okolicznik.
`Był to wczoraj problem.` jest odrzucone, gdzie `Był to problem w Warszawie.`
wyprowadza się, a to drugie kontrprzykładem nie jest:
wyrażenie przyimkowe dochodzi tam do rzeczownika, a nie do zdania.
Ciała tej konstrukcji pisze `grammar.rule` w `olski/subset/zdanie.py`,
a nie rozwinięcie szyku, które miejsca na okolicznik wylicza
([`docs/subset.md`](../docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
więc dziury tej nie widać po żadnym z ciał z osobna.
Ruchem jest ta sama córka, którą bierze reszta zdań składowych, wraz z pomiarem.
Do przeczytania jest przedtem, ile czytań to miejsce dokłada:
`Flaga to płat tkaniny w muzeum.` jest wieloznaczne już bez niego,
bo wyrażenie przyimkowe ma tam dwa miejsca przyłączenia, a nie jedno.

Przeczenie przy łączniku `to` nie ma ciała w zdaniu bez grupy przed łącznikiem.
`To nie kot.` jest odrzucone, gdzie `Parser to nie kompilator.` wyprowadza się
i gdzie `To nie są oczywistości.` też
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#przy-kopuli-ten-sam-łącznik-ma-trzy-szyki-a-zgodność-wybiera-podmiot)).
Ruchem jest piąte ciało tej konstrukcji wraz z pomiarem,
bo cena każdego ciała jest osobną liczbą ([CLAUDE.md](../CLAUDE.md#code)).
Do przeczytania jest przedtem rozkład zakupu na cztery ciała, które weszły:
przeczenie z grupą przed łącznikiem wzięło zdanie albo dwa nad Składnicą
i ani jednego nad prozą tego repozytorium,
więc piąte ciało wycenia się wobec tamtej liczby, a nie wobec szyku `Był to`.

Ciąg pytań zależnych nie bierze pytania z orzecznikiem jako członu pierwszego.
`Pyta, co to jest i czy to działa.` staje na `czy`,
a `Pyta, co to jest.` oraz `Pyta, kto płaci i czy to działa.` wyprowadzają się,
więc brak jest w samym złożeniu, a nie w żadnym z dwóch czół
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą)).
Do przeczytania jest `ciąg_pytajny` w `olski/subset/podrzędne.py` obok pozycji
orzecznika wysuniętego, bo pytanie jest o to, czy człon z orzecznikiem
wypuszcza cechę, której ciało ciągu żąda od członu pierwszego.
Zdanie to pisze `docs/roles.md`, a odrzucenie jest werdyktem uczciwym,
więc pozycja nie ma pilności, jaką miałby brak wydający `valid`.

Wypełnienie inne niż dopełnienie, wysunięte przed głowę, która orzeka bez podmiotu,
nie ma ani pozycji, ani ceny, bo deklaracja tej pozycji bierze samo dopełnienie
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu)).
Populacji, której to dotyczy, nie przeczytał nikt:
wiersz `imps` został po wpuszczeniu formy nieosobowej z blisko setką zdań Składnicy,
a wysunięte dopełnienie zabrało z niego część i nie wiadomo którą.
Ruchem jest przeczytanie tej resztki, a po nim wycena pozostałych wypełnień
nad obiema głowami naraz: deklaracja bierze głowę nazwą symbolu,
więc wypełnienie dopisane do niej obejmuje predykatyw i formę nieosobową razem.
Do przeczytania jest `bloker` w `olski/pokrycie.py` z tego samego powodu,
z którego czyta go wpis o resztce `praet`: nazywa on formę, a nie przyczynę.

Kopuła opuszczona ma listę o jednym lemacie, a polszczyzna opuszcza ją szerzej.
`RZECZOWNIK_ORZEKAJĄCY` w `olski/subset/słowa.py` wymienia `mowa`,
bo tego lematu zażądał rejestr ustaw,
a `brak dowodów`, `szkoda czasu` i `pora wracać` są tą samą konstrukcją:
rzeczownik w mianowniku orzeka, a czasownika nad nim nie ma.
Wypełnienia żąda przy tym każdy z tych trzech innego niż `mowa` —
dopełniacza albo bezokolicznika, a nie okolicznika —
więc lemat dopisany do listy nie wystarcza,
a wpis jest przez to o produkcję, a nie o dane.
Ruchem jest lista wyczytana z korpusu, a nie z pamięci,
a materiał do jej wyczytania daje pozycja ogólna dopisana do gramatyki:
[`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat)
nazywa dwie produkcje, które ona dopisuje,
a zdanie, które dzięki nim przechodzi, pokazuje rzeczownik w nim orzekający.
Do przeczytania jest, ile z tych zdań jest ciągiem współrzędnym grup imiennych,
bo tym była większość zakupu tamtej pozycji nad siedmioma ustawami,
a lemat dopisany za taki ciąg wraca ceną w każdym zdaniu, które ten ciąg niesie.
Cenę każdego lematu bierze potem sonda kopuły odtworzona z commita, który ją trzyma,
tak jak wzięła cenę tego jednego.

Człon lewy ciągu współrzędnego nie unosi zdania względnego.
Produkcja `grupa_imienna → człon_imienny zdanie_względne` w `olski/subset/grupa.py`
żąda członu, a produkcja koordynacji daje po lewej człon i po prawej ciąg,
więc `pliki, które rosną, i katalogi` nie ma wyprowadzenia,
a `pliki i katalogi, które rosną` ma.
Ruchem jest symbol między grupą imienną a członem imiennym, przez który idą oba człony,
i ruch ten zbudowano na próbę, więc cena jest policzona, a zakup nie.
Cena ma trzy pozycje.
Nad Składnicą pod Morfeuszem jedno zdanie traci jednoznaczność —
`Przez czynniki ekonomiczne należy rozumieć te, które kształtują rozmiary
i strukturę dochodów oraz wydatków budżetowych.` wychodzi trzema czytaniami
zamiast jednego, bo `te, które kształtują rozmiary` staje się członem ciągu —
i jest to czytanie, które polszczyzna ma, więc nie jest to usterka, tylko cena.
Pod złotą morfologią nie rusza się ani jedno zdanie.
Trzecią pozycją jest `_role` w `olski/skład/rozbiór.py`:
czyta ono kształty gramatyki po etykiecie,
więc każdy nowy poziom kosztuje tam gałąź, a obieg zamknięty bez niej pada.
Taki ciąg niosą cztery zdania Składnicy z 13035 mających drzewo wzorcowe
(`python3 -m harness.kształty`); nad ustawami nie policzył ich nikt.
Każde z tych czterech ma powyżej piętnastu słów, a jedno dwadzieścia pięć,
więc zakup jest mniejszy niż sama czwórka:
zdanie tej długości pada zwykle na czymś jeszcze,
a wpuszczona produkcja kupuje je dopiero wtedy, gdy pada wyłącznie na niej.
Kto ten wpis podnosi, nie zamknie go tą liczbą, bo cztery zdania przeciw jednemu
traconemu i gałęzi w `_role` ważą tyle samo.
Zamyka go pytanie o czytanie: to, które ten ciąg dokłada, polszczyzna ma,
więc dopisanie produkcji odbiera werdykt nieprawdziwy, a nie samą jednoznaczność,
i po tej stronie stoi
[kierunek](../docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).

Apozycji olski nie ma, więc przecinek przed wyliczeniem ma u niego jedno czytanie.
`Przyszli moi sąsiedzi, lekarz i nauczyciel.` wychodzi jednym czytaniem,
`[moi sąsiedzi], lekarz i nauczyciel`, czyli ciągiem o trzech członach,
a polszczyzna czyta to zdanie także drugim sposobem,
w którym lekarz i nauczyciel są tymi samymi sąsiadami.
Jest to jednoznaczność z braku produkcji,
czyli to, czemu zapobiega
[reguła o obu czytaniach wszędzie](../docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
tyle że tam brakująca pozycja zostawiała zdanie odrzucone, a tu przyjęte,
więc po werdykcie nie widać jej wcale.
Ruchem jest produkcja apozycji, czyli człon, przecinek i drugi człon
w tym samym przypadku, i cena jest widoczna przed pomiarem:
przecinek jest już znakiem koordynacji na pięciu poziomach
([`docs/subset.md`](../docs/subset.md#what-the-grammar-covers)),
więc apozycja dokłada czytanie każdemu ciągowi rozdzielonemu przecinkiem.
Apozycję z przecinkiem niesie 217 zdań Składnicy z 13035 mających drzewo wzorcowe
(`python3 -m harness.kształty`), i jest to największy zakup w tej sekcji.
Apozycja bez przecinka wychodzi z tego przebiegu osobno, w 1274 zdaniach,
bo jest konstrukcją inną i stoi już wśród zawyżeń
[pomiaru wieloznaczności](../docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
jako `podpis CERTYFIKAT`; ten wpis mówi o pierwszej z tych dwóch liczb.
Kształtem żadnej z nich nie policzyć, i tu wpis się mylił.
Monografia Świgry mówi, że apozycji nie rozdziela od koordynacji etykieta
(Woliński 2019, p. 2.8.2, wyliczony w [`docs/swigra.md`](../docs/swigra.md#sources)),
a wynika z tego tylko tyle, że nie rozdziela jej kategoria:
rozdziela ją nazwa reguły, którą bank drzew niesie przy każdym rozwinięciu.
Węzeł nominalny o dwóch nominalnych dzieciach jest w tym banku przydawką
dopełniaczową w 6580 zdaniach, przy 217 apozycji z przecinkiem,
więc liczba wzięta kształtem mówiłaby o przydawce, którą olski ma,
a nie o konstrukcji, której nie ma.
Zostaje sama cena: ile czytań apozycja dokłada zdaniom, w których ciąg
rozdzielony przecinkiem już się wyprowadza.

`Co innego jest tanie.` wychodzi `valid` z `Co innego` w roli okolicznika,
czyli czytaniem, którego polszczyzna nie ma,
bo Morfeusz daje formie `co` czytanie przyimka rządzącego dopełniaczem.
Przydawka za tym zaimkiem tego napisu nie odzyskała i odzyskać nie mogła
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)):
`innego` jest dopełniaczem, więc zgadza się z `co` w dopełniaczu,
a rola, w której ta grupa stoi, żąda mianownika.
Ruchem jest wykluczenie po stronie słownika, czyli ta sama droga,
którą `admissible` w `olski/segmentacja.py` odbiera czytania spoza polszczyzny
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)),
a nie kolejna produkcja.
Słownictwem projektu tego nie zrobić, choć obie jego sekcje sięgają do słownika:
`pomijane` odbiera lematowi czytania wszystkie (`olski/słownictwo.py`),
a ten rejestr pyta przez `co` zdanie po zdaniu,
więc naprawa jest kryterium na czytanie, a nie deklaracją na lemat.
Do rozstrzygnięcia jest, czy kryterium ma stać na parze `co` z przymiotnikiem,
czy na samym czytaniu przyimkowym tej formy:
`co godzinę` i `co dzień` są w polszczyźnie właśnie tym przyimkiem,
więc wykluczenie szersze zabiera zwyczajne zdania,
a wąskie jest listą, która rośnie o każdy przymiotnik.
Do przeczytania jest przedtem, ile zdań na tym czytaniu stoi:
bez tej liczby wpis jest samą ceną.
Pyta o to przebieg werdyktów, a nie bank drzew ani kolejka blokerów —
zdanie się wyprowadza, więc żadna z nich go nie pokazuje —
czyli sonda zdejmująca formie `co` czytanie przyimkowe
i licząca, którym zdaniom werdykt się przez to zmienia.

Zdanie względne bez poprzednika stoi tylko w roli podmiotu, więc `Bezokolicznik ma
dwa kształty, czyli to, kto wykonuje to, o czym mówi pozycja podrzędna.` pada, a
`Kto wchodzi w środek, poprzedniego zdania nie przeczytał.` wyprowadza się
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Ruchem jest drugie ciało dopełnienia obok tego podmiotu, i cena jest widoczna
przed pomiarem: pytanie zależne stoi w tej samej pozycji ramy, więc każde zdanie
z `kto` za czasownikiem dostanie drugie czytanie — pytanie i zdanie względne bez
poprzednika są tam jednym napisem.
Do przeczytania jest, ile takich zdań ma bank drzew: bez tej liczby wpis jest samą
ceną, a kształt do policzenia daje `zdanie_względne_bez_poprzednika`
w `olski/subset/zdanie.py`.

Zaimek pytajny stoi tylko na czele swojego zdania, więc drugie pytanie w tym samym
zdaniu nie ma pozycji: `Kto jest kim?` pada, a `Czym jest parser?` wyprowadza się
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Pozycję na miejscu odbiera zaimkowi wykluczenie z pozycji rzeczownej, a czoło jest
w zdaniu jedno, bo tyle wysuwa polszczyzna.
Ruchem jest pozycja zaimka pytajnego w roli wypełnionej na miejscu, czyli cecha
rozdzielająca zaimek stojący w pytaniu od tego, który stoi w zdaniu oznajmującym:
bez niej `Parser zapisuje co.` wyprowadza się, a polszczyzną nie jest.
Do przeczytania jest `BEZ_CZOŁA` w `olski/subset/słowa.py`, bo tą cechą gramatyka
rozdziela dziś rolę wypełnioną czołem od wypełnionej na miejscu, i pytanie jest o to,
czy druga wartość wystarczy, czy trzeba trzeciej.
Wpis ma zdanie banku drzew, które ten brak odrzuca:
`Kiedyś zapytałem kierowcę naszego gazika, kim właściwie jest mój przewodnik?`
pada pod żywą morfologią, bo `co` nie bierze poprzednika rzeczownikowego
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie)),
a pytanie zależne z orzecznikiem za przecinkiem jest jedyną rzeczą,
której temu zdaniu brakuje.

Przytoczenie samego wyrazu funkcyjnego nie ma czytania, bo `kto` i `co` nie stoją
w pozycji rzeczownej: `nikt, kto, nic, coś i ktoś mają u Morfeusza czytanie
jedno` pada, a ten sam ciąg bez `kto` w środku wyprowadza się
([`docs/konstrukcje-gramatyczne/zdanie-złożone.md`](../docs/konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).
Ruchem jest albo cudzysłów w tym zdaniu `docs/konstrukcje-gramatyczne/grupa-imienna.md`,
czyli poprawka w prozie,
albo licencja dla wyrazu przytoczonego backtickami, czyli ta sama robota, którą
trzyma wpis o angielskiej nazwie pisanej małą literą; drugie rozstrzyga o obu.

Ciąg rozdzielny przymiotników nie ma ciała przecinkowego, więc `Warstwy trzecia,
czwarta i piąta pracują.` jest odrzucone, a `Warstwy trzecia i czwarta pracują.`
wyprowadza się
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#przydawka-koordynuje-się-i-rozdziela-rzeczownik-tylko-za-nim)),
choć polszczyzna trzeci człon pisze właśnie przecinkiem.
Ruchem byłoby czwarte ciało tej rodziny, a pomiar przed nim mówi, żeby go nie pisać:
zakup jest zerowy.
Ani jedno zdanie Składnicy nie stawia między przydawkami samego przecinka
(`python3 -m harness.kształty`), a dziesięć, które stawia go w tej pozycji,
stawia go razem ze spójnikiem — `dynamiczne, ale dostosowane`,
`tak prawicowej, jak i lewicowej` — czyli w kształcie, którego to ciało nie daje.
Wpis zamyka więc albo skasowanie, albo ciało na przecinek ze spójnikiem —
a takie ciało wpuszcza konstrukcję inną niż ta z pierwszego zdania wpisu,
bo ciąg rozdzielny dzieli rzeczownik między człony, a `dynamiczne, ale
dostosowane` mówi obie rzeczy o jednym.
Zdanie `Warstwy trzecia, czwarta i piąta pracują.` zostaje przez to odrzucone
z ceną, której nikt nie zapłacił, bo rejestr banku drzew go nie pisze;
czy pisze je rejestr docelowy, mówi przebieg nad prozą tego repozytorium,
a nie ten nad Składnicą.
Zdanie tego kształtu stoi w [`docs/architecture.md`](../docs/architecture.md),
a autor odmówił tam zapłaty, bo wersja przechodząca żąda liczby pojedynczej
od trzech warstw naraz.

Człon bez czasownika stoi tylko na końcu zdania składowego, a wtrącony w środek pada:
`Skład, czyli Morfeusz, jest tani.` nie ma czytania, a `Parser jest tani, czyli
Morfeusz.` ma ([`docs/subset.md`](../docs/subset.md#what-it-does-not-cover-yet)).
Miejsce w środku zdania gramatyka ma, bo weszła nim para myślników
([`docs/konstrukcje-gramatyczne/zdanie-złożone.md`](../docs/konstrukcje-gramatyczne/zdanie-złożone.md#para-myślników-obejmuje-wtrącenie-w-środku-zdania-a-nawias-na-jego-końcu)),
więc został sam człon i to, czego on od tego miejsca żąda:
przecinka po obu stronach.
Ruchem jest przez to cecha na członie, a nie kolejne ciało w liście okoliczników:
przecinek zamykający dokłada `_zamykane` w `olski/subset/podrzędne.py` osobnym ciałem,
a dwa ciała jednego symbolu są dla produkcji nad nim jednym symbolem,
więc pozycja wpisana bez tej cechy wpuszcza w środek zdania człon niedomknięty.
Do przeczytania jest ta funkcja wraz z listą symboli, które przez nią przechodzą:
cecha dopisana tam dochodzi zarazem do zdania podrzędnego i względnego,
a cechy wypuszczanej bez czytelnika pilnuje `NIE_WYPUSZCZANE`
w `olski/subset/deklaracja.py`.
Do przeczytania jest przedtem, ile czytań ta pozycja dokłada zdaniu, które ten człon
stawia na końcu: tam da się go przyłączyć i do zdania składowego, i do miejsca
okolicznika za jego ostatnią córką, czyli dwa razy w tym samym napisie.

Spójnik skorelowany nie zaczyna się za podmiotem:
`Werdykt ani nie wnosi, ani nie zdejmuje.` pada,
gdzie `Ani werdykt nie wnosi, ani nie zdejmuje.` wyprowadza się
([`docs/konstrukcje-gramatyczne/zdanie-złożone.md`](../docs/konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-skorelowany-powtarza-się-przed-każdym-członem)).
Dwa ciała, które weszły, spinają zdania składowe i grupy imienne,
a w tym napisie ciąg zaczyna się za podmiotem, czyli spina same orzeczenia,
a takiej pozycji koordynacja olskiego nie ma na żadnym poziomie.
Zdanie to nazywa ten brak na liście w
[`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md#czego-brakuje-najbardziej).
Ruchem jest ciało spinające orzeczenia, a nie kolejny lemat ani kolejny poziom,
i cena jest widoczna przed pomiarem: orzeczenie niesie ramę czasownika,
więc ciąg musiałby powiedzieć, którą ramę wypuszcza w górę,
a dwa czasowniki o różnych ramach dzielą wtedy jedno wypełnienie.
Do przeczytania jest `wypełnienia` w `olski/subset/zdanie.py` obok
[`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#nothing-above-a-coordination-distributes-into-it),
bo zasięg koordynacji rozstrzyga się tam, gdzie stoi to, co człon zawiera.

Wolny celownik nie ma u olskiego pozycji żadnej:
`Kompilator wyprowadza psa agentowi.` pada, `Kompilator wyprowadza psa.` przechodzi,
a pierwsze jest polszczyzną
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#wolny-celownik-nie-jest-pozycją-ramy-i-nie-wchodzi-leksykonem)).
Leksykonem tego nie wpuścić, bo Walenty wypisuje pozycje żądane,
a ten celownik dochodzi do orzeczenia dowolnego czasownika,
więc ruchem jest pozycja okolicznika obok wyrażenia przyimkowego i przysłówka.
Cena jest widoczna przed pomiarem i jest wysoka:
okolicznik dochodzi do zdania i do grupy imiennej, a forma celownika żeńskiego
jest zarazem miejscownikiem, więc każde `w gramatyce` dostaje drugie czytanie.
Ceny tej zakup nie równoważy.
Celownik pod pozycją luźną, czyli ten, którego schemat czasownika nie żąda,
niesie w Składnicy 10 zdań z rzeczownikiem i 54 z zaimkiem,
na 13035 mających drzewo wzorcowe (`python3 -m harness.kształty`).
Pozycji, którą wpis proponuje, żąda pierwsza z tych liczb, a nie ich suma:
zaimek zwrotny olski ma już terminalem
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym)),
a `Rozbiłaś mi samochód!` żąda zaimka osobowego, nie grupy imiennej.
Rozdzielić te dwie liczby trzeba przy tym lematem, a nie klasą głowy,
którą bank drzew przy frazie wypisuje: `siebie` liczy on do klasy rzeczownika,
więc podział po samej klasie stawia każde `sobie` po stronie rzeczownikowej
i zawyża tam wiersz kilkakrotnie.
Zostaje `harness/konwersy.py`, bo tamto kryterium łapie ten celownik dziś jako
pomyłkę i mówi, ile go w Walentym widać z drugiej strony.

Liczebnik za rzeczownikiem nie ma pozycji, a zasłania to czytanie rzeczownikowe.
`po którym zostaje czytań kilka` wychodzi przyjęte,
bo Morfeusz zna `kilka` także rzeczownikiem,
a grupa liczebnikowa stawia liczebnik przed rzeczownikiem
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)),
czyli brak zasłania tam czytanie, którego polszczyzna nie ma
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)).
Kolejka blokerów tego nie pokazuje, bo zdanie się wyprowadza,
więc podnosi ten brak czytanie werdyktów, a nie przebieg.
Czego się po ruchu spodziewać, mówi zaimek zwrotny, czyli ten sam brak wpuszczony
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym)):
pozycja dopisana zabiera zdaniu jednoznaczność i zabiera mu zarazem werdykt
nieprawdziwy, a wybór między tymi dwiema liczbami rozstrzyga kierunek
([`docs/roadmap.md`](../docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).

Szyk `Będzie trzeba zmierzyć cenę.` nie ma ciała, a wywód i zdanie odrzucone stoją
w [`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#forma-bedzie-składa-czas-przyszły-także-z-predykatywem).
Ruchem jest drugie ciało tej samej pary produkcji wraz z pomiarem,
bo cena każdego ciała jest osobną liczbą.
Do przeczytania jest przedtem, czy ten szyk nie daje drugiego czytania zdaniu,
które dziś wychodzi jednoznaczne:
`bedzie` orzeka też samo
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony)),
a predykatyw za nim stanąłby wtedy tam, gdzie stoi orzecznik.

Okolicznik narzędnikowy nie ma pozycji przed zdaniem, a polszczyzna go tam stawia:
`Wieczorem wziął lustro.` pada, `Wziął lustro wieczorem.` przechodzi,
i pierwszy szyk wypisuje tor składu, więc obieg na nim nie zamyka się
(`tests/test_rozbiór.py`).
Ciało zmierzono i odrzucono, bo grupa wysunięta jest wtedy jedyną grupą przed
czasownikiem, tak samo jak w szyku od czasownika i w zdaniu o opuszczonym podmiocie
([`docs/konstrukcje-gramatyczne/okolicznik.md`](../docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Ruchem nie jest więc ani samo ciało, ani znacznik na grupie:
czytania rozdziela przypadek, a nie kształt, i formy, o które idzie,
mają mianownik obok narzędnika, więc żądanie musiałoby mówić o przypadku jedynym,
a unifikacja przecina zbiory i tego powiedzieć nie umie.
Dwa obejścia, które ta gramatyka ma poza `unify`, tu nie sięgają:
oba pytają o formę — jedno odmawia lematowi, drugie formie bez cechy —
a żadne nie pyta, ile wartości ta cecha niesie
([`docs/parsowanie.md`](../docs/parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)).
Do przeczytania jest ta sekcja wraz z wpisem o wolnym celowniku:
tamten stoi na tej samej przeszkodzie, bo forma celownika żeńskiego
jest zarazem miejscownikiem, więc rozstrzygnięcie zapada dla obu naraz.

Liczebnik rządzący nie orzeka: `Torów jest dwa.` pada,
a `Tory są dwa.` przechodzi zgodnym
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-orzeka-o-tym-ile-czegoś-jest)).
Podmiot stoi tam w dopełniaczu, a orzeczenie nie zgadza się z niczym,
więc ciało jest osobne i osobna jest jego cena, której nikt nie policzył.
Do przeczytania jest, czy nie zderzy się ono z czasownikiem nieosobowym:
tamten też orzeka bez zgodności z podmiotem
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#czasownik-nieosobowy-rządzi-ramą-swojego-lematu)).

Słowa pytające `jak`, `jaki` i `ile` nie mają pozycji,
a zdania z nimi nie padają, tylko przechodzą czytaniem, którego polszczyzna nie ma:
`Pyta, ile ta gramatyka kosztuje.` wychodzi przyjęte z `ile` w okoliczniku
przysłówkowym, bo Morfeusz daje `jak` oraz `ile` część mowy `adv`, a `jaki`
przymiotnikową, i olski bierze te części mowy całe.
Ruch ma przez to dwie połowy i pierwsza jest zawężeniem:
czytanie okolicznikowe ma zejść, zanim wejdzie czoło, które je zastąpi
([`docs/roadmap.md`](../docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).
Czwarte z tych słów, `dlaczego`, weszło i zostawiło po sobie kształt,
w który `jak` wchodzi wprost, bo pyta tak samo o okoliczność
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#pytanie-o-okoliczność-wysuwa-przysłówek-a-zdanie-pod-nim-jest-całe)),
a `ile` i `jaki` żądają każde innego: pierwsze rządzi dopełniaczem,
a drugie zgadza się z rzeczownikiem i jest tym samym kształtem co `który`.
Do przeczytania jest przy `jak` to, co ta gramatyka bierze z jego czytania
spójnikowego — `tak samo jak reguła` — bo zawężenie odbiera zdania,
które ta proza pisze, a wpuszczenie samego czytania przysłówkowego ich nie odbiera
i wtedy jeden napis dostaje dwa wyprowadzenia.
Do przeczytania jest też wpis o okoliczniku przysłówkowym biorącym całą część mowy,
bo wylicza on formy, które ten rejestr pisze inaczej, i te trzy słowa
są jego dalszym ciągiem.

Zaimek zwrotny nie ma pozycji orzecznika narzędnikowego,
a wywód stoi w [`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym).
Ruchem jest jedno ciało wraz z pomiarem nad bankiem drzew,
bo proza tego repozytorium tej konstrukcji nie pisze.
Wpis ten jest zablokowany rzeczownikiem `soba`, o który pyta wpis w sekcji
o gramatyce i pomiarze: dopóki ten lemat bierze `sobą`, pomiar tej pozycji
liczy zamianę jednego czytania na dwa, a nie zakup.

Para wypełnień nie rozdziela się szykiem, więc żaden jej człon nie wychodzi
przed podmiot: `Autorowi parser pokazuje czytania.` jest odrzucone
i `Czytania parser pokazuje autorowi.` tak samo,
choć oba zdania polszczyzna ma, a `Autorowi linter pomaga.` wyprowadza się,
bo sam celownik idzie zwykłym szykiem dopełnienia.
Ciała pary wylicza `PARA_WYPEŁNIEŃ` w `olski/subset/zdanie.py`
i wszystkie stawiają oba człony w grupie orzeczenia,
czyli za podmiotem, a szyki zdania o parze nie wiedzą.
Skład tę dziurę odsłania, odkąd celownik jest w nim pozycją:
`Komu` w `olski/skład/składnia.py` bierze znacznik tematu jak każdy konstytuent,
więc drzewo z celownikiem na czele wychodzi napisem i z obiegu nie wraca.
Do przeczytania jest rozwinięcie szyku
([`docs/subset.md`](../docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
bo para jest symbolem, a nie dwiema córkami zdania, i to ono rozstrzyga,
czy ruchem jest szyk dopisany parze, czy para rozpisana na córki.
Ruch żąda pomiaru, bo szyk wysunięty jest w tej gramatyce kosztowny
i mnoży czytania tam, gdzie grupy są synkretyczne.

Orzecznik nie stoi między podmiotem a swoją kopulą, więc `Rekordy spodziewane są.`
nie ma wyprowadzenia, a `Rekordy są spodziewane.` ma i `Spodziewane są rekordy.` też.
Jest to ta sama usterka, o której mówi
[`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#the-bare-verb-initial-order-keeps-the-predicative-one-honest),
tyle że o jeden szyk dalej: przymiotnik jest przydawką albo orzeka,
a gramatyka mająca jeden z tych dwóch szyków wydaje drugie czytanie sama.
Brak ten nie odrzuca zdania, tylko zostawia w nim czytanie nieprawdziwe:
imiesłów przed kopulą czyta się przydawką za rzeczownikiem,
więc `W Tokio, Sydney i w Londynie rekordy spodziewane są dopiero dzisiaj.`
wychodzi z podmiotem `rekordy spodziewane`, a bank drzew orzeka tym imiesłowem
([`docs/corpus.md`](../docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Ruchem jest ciało z tym szykiem wraz z pomiarem, a cena jest widoczna przed nim:
przydawka za rzeczownikiem zostaje, więc każde takie zdanie dostanie drugie czytanie
zamiast pierwszego prawdziwego, czyli zamieni werdykt nieprawdziwy na wieloznaczność
([`docs/roadmap.md`](../docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).
Do przeczytania jest przedtem, ile zdań banku drzew stoi na tym czytaniu:
wpis znalazło jedno, które przyszło do wiersza niezgodnych razem z ciągiem
współrzędnym wyrażeń przyimkowych, a przebiegu po całym wierszu nikt nie zrobił.
