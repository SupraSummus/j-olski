# Okolicznik: przysłówek, cząstka, narzędnik i imiesłów

Jeden plik rejestru konstrukcji, w którym sekcja przypada na konstrukcję.
Cena i zakup stoją w niej rzędem wielkości albo granicą.
Co ten rejestr obiecuje i który plik czytać, mówi [wstęp](README.md).

## Cząstka ma dwóch gospodarzy i przy jednym dostaje etykietę

`Program już zapisuje ustawienia.`, `Reguła obowiązuje także wtedy.`,
`Już program zapisuje ustawienia.` —
cząstka stoi w zdaniu tam, gdzie okolicznik przysłówkowy,
i tę pozycję gramatyka ma, odkąd ma
[przysłówek](#przysłówek-dostaje-wszystkich-trzech-gospodarzy).
Produkcje są przez to dwie i pisze je ta sama pętla, co tamte:
cząstka w liście okoliczników i cząstka na czele zdania składowego.

Przy zdaniu cząstka dostaje rolę osobną od przysłówka, choć pozycję ma tę samą,
bo werdykt nazywa rolę etykietą węzła:
`okolicznik_przysłówkowy: już` mówiłoby o zdaniu,
że ma okolicznik przysłówkowy, którego ono nie ma.

Drugim gospodarzem jest grupa imienna,
bo tam polszczyzna cząstkę stawia tak samo:
`Nawet ptaki przestały śpiewać.` mówi o ptakach, a nie o przestawaniu,
i widać to po zasięgu podmiotu, a nie po żadnej roli.
Ciałem jest `człon_imienny → part człon_imienny`, a osobę przepuszcza ono,
bo cząstka staje i przed zaimkiem: `Nawet ja zapisuję ustawienia.`

W grupie cząstka etykiety nie nosi, bo widać ją w napisie roli,
którą ta grupa zajmuje: podmiotem jest `Nawet ptaki`.
Rolę niesie przez to gospodarz jeden, tym samym prawem,
którym niesie ją [jeden gospodarz przysłówka](#przysłówek-dostaje-wszystkich-trzech-gospodarzy).

Wybór gospodarza nie jest tu jednak rozstrzygnięciem, i tym cząstka różni się
od przysłówka. Przysłówkowych gospodarzy rozdziela stopień, czyli cecha,
którą niesie tagset, a cząstki nie rozdziela ani cecha, ani lemat:
bank drzew stawia wewnątrz grupy każdy lemat tej listy, który w nim pada,
i ten sam lemat stawia przy zdaniu.
Udział wystąpień w grupie idzie od jednego na jedenaście przy `dopiero`
do co drugiego przy `niemal`,
a lematu stojącego wyłącznie w grupie nie ma ani jednego;
wyłącznie przy zdaniu stoją trzy i każdy pada mniej niż dziesięć razy.
Podział listy po lemacie jest więc wariantem odrzuconym:
bank drzew go nie potwierdza, a kryterium na tę pozycję nie jest leksykalne.
Zostaje wieloznaczność oddana czytelnikowi,
tak samo jak przy [wyrażeniu przyimkowym](../subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).

Cena wypada przez to inaczej niż przy przysłówku.
Nad Składnicą kilkadziesiąt zdań schodzi z przyjętych na wieloznaczne
pod jedną morfologią i pod drugą, a wyprowadzenie zyskuje kilka.
Zakupem jest prawda o zdaniu, a nie pokrycie:
wiersz zdań czytanych wbrew drzewu wzorcowemu maleje o blisko połowę
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)),
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
([subset.md](../subset.md#what-it-does-not-cover-yet)).
Lista jest więc zamknięta, a kryterium na wejście jedno:
cząstka ma nie mieć czytania, które gramatyka bierze już gdzie indziej,
i tym samym warunkiem stoją obok siebie dwie klasy
[spójnika zdaniowego](zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają).
Poza listą zostaje przez to `to`, które ma ponadto własną pozycję,
a tej olski nie ma ([subset.md](../subset.md#what-it-does-not-cover-yet)).

## Określenie przed zdaniem wchodzi pod to, które stoi za nim

Zdanie składowe bierze określenie z obu stron i bierze je jednym symbolem.
Przed nim stoi wyrażenie przyimkowe, przysłówek albo cząstka,
a za nim wtrącenie w nawiasie, człon bez czasownika
albo [okolicznik wyrażony zdaniem](podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania).
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
[Odczytaniem jest kształt](../subset.md#co-się-liczy-jako-jedno-odczytanie),
więc dwa kształty na jedno odczytanie są usterką tej gramatyki,
a nie faktem o polszczyźnie.

Kształt zdejmuje gramatyka, choć oba znaczą to samo,
bo ani tożsamość czytania, ani warstwa znacząca tu nie sięgają.
Zwinięcie po stronie tożsamości żąda postaci normalnej nad zagnieżdżeniem określeń,
zostawia oba wyprowadzenia w lesie,
a sygnatura grubsza obowiązuje każde zdanie naraz, nie tylko tę parę
([disambiguation.md](../disambiguation.md#tożsamość-czytania-jest-tańsza-i-częściowo-już-stoi)).
Warstwa znacząca dziedzinę ma węższą niż gramatyka i tych zdań nie dosięga
([architecture.md](../architecture.md#werdykt-liczy-wyprowadzenia-bo-powstaje-pod-dwiema-warstwami-które-liczą-znaczenia)).
Warunek w gramatyce kosztuje za to jedną cechę, a las po nim maleje.

Porządek jest zapisany cechą (`dostawka` w `olski/subset/słowa.py`):
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
([corpus.md](../corpus.md#where-the-analyses-stop) trzyma polecenie).

## Imiesłów przysłówkowy stoi tam, gdzie okolicznik wyrażony zdaniem

`Program zapisuje ustawienia, sprawdzając zgodność.`
Konstrukcja ta jest okolicznikiem i zajmuje miejsce,
które okolicznik wyrażony zdaniem w tej gramatyce już ma
([podrzędność.md](podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)),
więc dochodzi jego ciałami, a nie własnym symbolem.
Przemawia za tym to samo, co przy [przydawce
imiesłowowej](grupa-imienna.md#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik):
symbol osobny żądałby drugiej kopii obu pozycji okolicznika
oraz obu ciał nad ciągiem współrzędnym,
a nie kupowałby za to niczego, czego polszczyzna w tych miejscach rozdziela.

Spójnika te ciała nie mają i mieć nie mogą,
bo imiesłów podporządkowuje sam: formą osobową nie jest.
Przecinek zostaje, bo to on tę konstrukcję w zdaniu odgranicza.

Wypełnienie bierze imiesłów ramą swojego lematu,
tak samo jak forma nieosobowa czasownika
([orzeczenie.md](orzeczenie.md#czasownik-nieosobowy-rządzi-ramą-swojego-lematu)),
i tak samo bez orzecznika zgodnego:
podmiot tego imiesłowu stoi w zdaniu nadrzędnym,
więc pod nim nie ma z czym zgodzić ani orzecznika, ani niczego innego.
Widać to na lemacie, o którym leksykon mówi, że biernika nie bierze:
`Program zapisuje ustawienia, pomagając zgodność.` jest odrzucone,
gdzie `pomagając linterowi` się wyprowadza.
Polszczyzna żąda przy tym od tego imiesłowu tożsamości podmiotu,
a nie zgodności form, więc gramatyka nie ma tego czym złamać:
`pcon` nie niesie ani liczby, ani rodzaju, ani osoby.

Ciała są dwa na każdą pozycję, bo zakup imiesłowu samego —
`Program zapisuje ustawienia, milcząc.` — jest osobną liczbą.
Cząstka zwrotna stoi przy nim po obu stronach, tak samo jak przy formie osobowej.

Przez tę konstrukcję symbol okolicznika wchodzi między gospodarzy przyłączenia,
i jest to jedyna jego głowa, która tego wpisu potrzebuje.
Pod okolicznikiem wyrażonym zdaniem stoi zdanie składowe,
na którym zejście po gospodarza staje wcześniej,
a pod imiesłowem nie stoi żaden inny gospodarz,
więc bez tego wpisu `sprawdzając zgodność z dokumentem`
nazywałoby gospodarzem orzeczenie zdania nadrzędnego
i dwa czytania wychodziłyby z werdyktu jednym napisem
([subset.md](../subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).

Zakup jest tu kilkudziesięcioma zdaniami banku drzew wyciągniętymi z odrzucenia,
w większości wieloznacznymi, a ceny nie ma żadnej pod żadną z dwóch morfologii:
ani jedno zdanie przyjęte wcześniej nie staje się wieloznaczne.
Niezgodnie z drzewem wzorcowym olski nie czyta ani jednego zdania nowo przyjętego.
Nad prozą tego repozytorium zakup jest liczony w pojedynczych zdaniach,
bo ten rejestr pisze tę formę rzadko.

## Narzędnik bez przyimka jest okolicznikiem obok orzecznika

`Mieszczanie zabili okna deskami.` mówi, czym zabili,
a `Wziął lustro wieczorem.` mówi, kiedy wziął,
i polszczyzna wyraża jedno i drugie samym narzędnikiem, bez przyimka.
Olski brał ten przypadek pod przyimkiem i nie brał go bez niego,
bo `inst` było u niego pozycją orzecznika i niczym więcej
([warstwa-leksykalna.md](../warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)).

Pozycja jest okolicznikiem, czyli stoi tam, gdzie stoi wyrażenie przyimkowe
i przysłówek, i wchodzi tą samą listą co one.
Symbol ma własny, choć pozycję dzieli z przysłówkiem,
bo cena każdej z nich ma być osobną liczbą, a sonda bierze ją zdejmowaniem ciał
([CLAUDE.md](../../CLAUDE.md#code)).

Od orzecznika różni ten okolicznik to, kto mu udziela licencji.
Orzecznika żąda ramą kopula i nikt poza nią,
a okolicznik stoi przy każdym czasowniku i nie wypełnia przy żadnym pozycji ramy.
Zdanie, w którym kopula stoi przy grupie w narzędniku, ma przez to dwa czytania,
i dlatego kopula wypada z dwóch ciał, w których orzecznika przy niej nie ma:
`Parser jest.` przestaje się wyprowadzać,
a `Parser jest narzędziem.` zostaje przy jednym czytaniu, tym prawdziwym.
Zawężenie to kupuje jednoznaczność także zdaniu złożonemu:
bez niego `Pomiar mówi, że gramatyka jest podzbiorem.` czyta się i tak,
że zdanie podrzędne kończy się na `jest`,
a `podzbiorem` jest okolicznikiem przy `mówi`.
Cena jest jedna i nazwana: zdania orzekającego samym istnieniem — `Bóg jest.` —
olski nie bierze, a ten rejestr go nie pisze.

Zakup liczy się w setkach zdań i jest mniejszy niż ten, którym płacił
[przysłówek](#przysłówek-dostaje-wszystkich-trzech-gospodarzy).
Nad Składnicą pod złotą morfologią przeszło sto zdań wychodzi z odrzucenia
z jednym czytaniem, a drugie tyle z kilkoma,
i jest to więcej niż jedno zdanie odrzucone na trzydzieści.
Cena jest kilkunastokrotnie mniejsza:
jednoznaczność traci kilkanaście zdań przyjętych wcześniej.

Ważniejsze od tych dwóch liczb jest to, co werdykt mówi o zdaniach nowo przyjętych.
Z rolami drzewa wzorcowego zgadza się ponad cztery piąte z nich,
a niezgodne jest co dziewiąte.
Wśród niezgodnych stoi `Kwitnie handel paszportami.`,
czyli to samo zdanie, którym
[corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)
mierzył, ile kosztuje orzecznik wpuszczony pod każdy czasownik:
olski czyta je teraz tak, jak czyta je czytelnik — handel kwitnie w paszportach —
a drzewo wzorcowe znaczy tam co innego.
Odrzucenie zamieniło się więc na czytanie prawdziwe, a nie na zgodność
([roadmap.md](../roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).

Pod żywą morfologią rachunek jest inny i cała różnica jest w słowniku.
Zdań z odczytaniem przybywa tam podobnie wiele, a przyjętych ubywa kilkanaście:
forma czytana w kilku przypadkach naraz staje odtąd i w tym okoliczniku,
więc drugie czytanie dostaje każde zdanie, w którym taka forma zajmuje rolę.
Nazwa własna i nazwa urzędu mają to po Morfeuszu — `Jan`, `minister` i `redaktor`
niosą czytanie żeńskie nieodmienne obok męskiego — a w tym rejestrze mają to
[notacja](../warstwa-leksykalna.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)
oraz [napis przytoczony](zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania),
bo czytanie nieodmienne spełnia każde żądanie przypadku i spełnia też to.
`Zobacz docs/subset.md.` traci przez to jednoznaczność,
a `tests/test_subset.py` trzyma tę cenę wypisaną zdaniami.
Nad prozą tego repozytorium ubywa przez to kilku zdań przyjętych,
a odrzuconych nie ubywa ani jedno.

**Wysunięcia przed zdanie ta pozycja nie dostaje i jest to pomiar odmowny.**
`Wieczorem wziął lustro.` zostaje przez to na zewnątrz,
choć polszczyzna ten szyk pisze, a tor składu go wypisuje
(`tests/test_rozbiór.py`).

Zderza się on z dwoma kształtami zdania, które gramatyka ma:
z [szykiem od czasownika](orzeczenie.md#the-bare-verb-initial-order-keeps-the-predicative-one-honest)
oraz ze zdaniem o opuszczonym podmiocie.
W obu grupa wysunięta jest jedyną grupą przed czasownikiem,
więc `Wejściem jest zwykły tekst polski.` czyta się i tak, że wejście jest
orzecznikiem, i tak, że tekst jest wejściem, a `Jan jest nauczycielem.` dostaje
czytanie mówiące, że ktoś jest nauczycielem przy pomocy Jana.
Rozdziela te czytania morfologia, a nie struktura:
pierwsze żąda mianownika, drugie narzędnika, a formy, o które idzie, mają oba.
Produkcja nie ma więc czego zażądać,
bo unifikacja przecina zbiory i nie umie zażądać przypadku jedynego
([parsowanie.md](../parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)).

Sonda mówi to samo liczbą: ciało to wyciąga z odrzucenia jeszcze kilkadziesiąt zdań,
a jednoznaczność odbiera niemal tylu, ilu ją daje,
więc płaci się za nie zdaniem tego rejestru, a dostaje zdania banku drzew.
Liczby te trzyma commit, który to ciało odrzucił.

## Przysłówek dostaje wszystkich trzech gospodarzy

Wyrażenie przyimkowe ma dwóch gospodarzy i oba czytania są prawdziwe,
więc olski [oddaje je czytelnikowi](../subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).
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
[Krzywa pokrycia](../design-notes.md#making-the-trade-measurable)
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
Pierwszy gospodarz sam wypuszcza nie mniej niż jedno na pięćdziesiąt
zdań przyjętych z czytaniem, w którym przysłówek jest okolicznikiem zdania,
choć określa słowo stojące zaraz za nim.
Drugi gospodarz zdejmuje z tych czytań te przed przymiotnikiem,
a trzeci resztę, czyli te przed przysłówkiem,
i po nim nie zostaje ani jedno
([niżej](#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę)).
Zdanie przyjęte z takim drzewem jest droższe od wieloznacznego,
bo narzędzie o nim milczy
([roadmap.md](../roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
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
bo czyta wbrew drzewu nie mniej niż jedno zdanie na dziesięć z tych,
które kupuje sam:
zostają mu pomyłki na przysłówku odprzymiotnikowym,
który określa i zdanie, więc stopień nie rozdziela niczego —
`Oficjalnie cały Sejm RP śpi.` wychodzi z podmiotem `Oficjalnie cały Sejm RP`.
Ról odwróconych nie ma ani jednej, w żadnym wariancie.

Werdykt nazywa gospodarzy wprost, bo okolicznik przysłówkowy jest w nim rolą:

```sh
python3 -m olski.check --readings -c "Plik jest bardzo duży."
```

```text
<text>: Plik jest bardzo duży.
        2 odczytania, różne w rolach: okolicznik_przysłówkowy, orzecznik
        - podmiot: Plik, orzecznik: bardzo duży, orzeczenie: jest
        - podmiot: Plik, orzecznik: duży, orzeczenie: jest, okolicznik_przysłówkowy: bardzo → jest
zdań: 1; wieloznaczne: 1; bez odczytania: 0
```

Rolę niesie jeden z gospodarzy, i jest to decyzja, a nie przeoczenie.
Dwa czytania rozdziela przez to sama lista ról,
zamiast czekać na to, że czytelnik porówna dwa napisy orzecznika.

Nad rejestrem ustaw okolicznik kupuje w skali dziesięć razy mniejszej,
a drugi gospodarz dokłada tam zdanie, zamiast odejmować,
więc znak tej ceny zależy od rejestru,
a nie od samych gospodarzy.
Trzeci nie rusza tam ani jednego werdyktu, tak samo jak nad korpusem audytowym:
przysłówek przed przysłówkiem jest konstrukcją prozy prasowej,
a rejestr, o który olskiemu chodzi, nie pisze jej wcale.

Nad prozą tego repozytorium przysłówek daje wyprowadzenie,
a jednoznaczności nie daje.
Widać to na zdaniu, które staje na przysłówku i na niczym więcej:

```text
Po to ta czarna lista tu stała i cały wywód za nią dalej stoi.
```

Wyprowadzenie dostaje, jednoznaczności nie,
bo w czytaniu, które przysłówek mu daje, `za nią` ma dwóch gospodarzy.
Kolejka mówi więc, gdzie analiza stanęła, i nie mówi, co dopisanie kupi,
także wtedy, gdy zdanie stoi na jednej klasie
([corpus.md](../corpus.md#where-the-analyses-stop)).

Jedna klasa czytań przyszła razem z tą konstrukcją i nie jest przyłączeniem.
Morfeusz daje czytanie przysłówkowe formom, które ten rejestr pisze
jako przyimek albo spójnik — `wobec`, `gdy`, `jak` —
a okolicznik zdania bierze całą część mowy,
więc `Są oni obdarzeni rozumem i sumieniem i powinni postępować wobec innych
w duchu braterstwa.` ma trzy czytania z `wobec` w roli okolicznika,
w których `innych` jest dopełnieniem,
a `Program zapisuje ustawienia, gdy linter sprawdza tekst.` wyprowadza się
jako dwa zdania spięte przecinkiem, choć zdanie po przecinku jest podrzędne.
Jest to [czytanie, którego polszczyzna nie ma](../warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not),
a `admissible` po nie nie sięga, bo pyta o czytanie rzeczownikowe.
Kryterium na tę klasę nie jest przy tym oczywiste:
`blisko` i `jak` niosą czytanie przysłówkowe, którego polszczyzna używa,
więc warunek odsiewający przysłówek przy czytaniu przyimkowym zabrałby i je.
[todo/](../../todo/README.md) trzyma ruch wraz z ceną obu kryteriów, które mu się nasuwają.

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
bo `word("adv", degree={"pos", "com", "sup"})` bierze `tu` tak samo jak `bardzo`.
Dlaczego warunek nie mieszka w unifikacji i co jeszcze jest obok niej,
wywodzi [kanał cech](../parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne).

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
a gramatyki wariantu branej funkcją żąda od tej maszynerii [todo/](../../todo/README.md).
Są przez to ceną, przy której warunek zapadł, a nie figurą o dzisiejszej gramatyce.

### Płaska lista okoliczników mówi o zdaniu nieprawdę

Pierwszy gospodarz nie jest darmowy, bo lista okoliczników jest płaska.
Sam wypuszcza `Program zapisuje ustawienia bardzo szybko.` jednym czytaniem,
a jego kształtem jest `okoliczniki(bardzo okoliczniki(szybko))`,
czyli dwa okoliczniki zdania obok siebie,
gdzie `bardzo` określa `szybko` i zdania nie określa wcale.
Streszczenie nazywa przy tym pierwszy z nich,
bo rola przysłówka nazywa okolicznik pierwszy tak samo jak rola przyłączana,
więc drugi widać dopiero w napisie zdania.
Instrument, który liczy zgodność nad bankiem drzew, tego nie widzi:
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
Oszacowanie sięga i przysłówka na czele zdania,
bo pod symbolem przysłówka stoi każdy okolicznik przysłówkowy,
a czoło zdania jest osobnym ciałem produkcji:
`Oficjalnie cały Sejm RP śpi.` liczy się przez to razem z resztą.
Nad rejestrem ustaw ani jedno zdanie przyjęte płaskiego czytania nie dostaje,
więc konstrukcja jest tu droga w rejestrze,
który olskiemu ustawia kolejkę, a nie w tym, o który mu chodzi.

## Przymiotnik w formie poprzyimkowej jest okolicznikiem, a nie wyrażeniem przyimkowym

`Reguła działa po polsku.` wyprowadza się, a `Reguła działa polsku.` nie:
Morfeusz daje takiej formie część mowy `adjp`, czyli formę, która poza przyimkiem nie stoi,
i osobno nie bierze jej żaden terminal, więc para wchodzi jednym ciałem.

Okolicznikiem, a nie wyrażeniem przyimkowym, bo pytanie, na które ta para odpowiada,
jest pytaniem przysłówka: `po cichu` odpowiada tam, gdzie odpowiada `cicho`.
Formalizm mówi to samo, bo `adjp` nie niesie przypadka i przyimek nie ma tu czym rządzić;
ciało wraz z powodem, dla którego głową jest forma, stoi w `olski/subset/grupa.py`.

Przyimka lista nie zawęża, i jest to cena wzięta świadomie.
`w polsku` wyprowadza się przez to tak samo jak `po polsku`,
choć polszczyzna pisze samo drugie.
Która forma `adjp` staje po którym przyimku, jest faktem o leksemie, a nie o gramatyce,
a lista pisana ręką odsiewałaby razem z tym `z bliska` i `od dawna`.
Jednoznaczności to nie kosztuje:
pary, której nikt nie pisze, nie ma w żadnym zdaniu, więc nie dokłada ona czytania żadnemu.

Nad prozą tego repozytorium wiersz `adjp`
[kolejki blokerów](../pisanie-po-olsku.md#kolejka-czytana-po-formie-mówi-to-czego-nie-mówi-po-części-mowy)
obiecywał kilkanaście zdań,
a pozycja wyciąga z odrzucenia przeszło połowę z nich;
reszta staje po niej na blokerze następnym, bo zdanie odrzucone niesie zwykle kilka.
Wyciągnięte wychodzą prawie wszystkie wieloznaczne, a jednoznaczne wychodzi jedno,
i tym ta pozycja jest podobna do okolicznika w ogóle: kupuje czytanie, a nie zdanie jednoznaczne.

Cena liczona werdyktem wyszła zerowa:
sonda różnicowa nie znalazła nad tą prozą ani jednego zdania,
które traciłoby jednoznaczność, ani żadnego przejścia poza tymi dwoma w górę.
Miejsce, w którym cena mogłaby paść, jednak istnieje,
i jest nim forma niosąca obok `adjp` czytanie przymiotnikowe — `bliska`, `dawna`, `rzadka` —
bo tamto czytanie produkcje brały już przedtem.
Sonda liczy werdykty, więc czytanie dołożone zdaniu i tak wieloznacznemu
stoi poza jej zasięgiem, a `todo/` trzyma ten brak;
nad zdaniami cytowanymi w tej prozie, gdzie liczbę czytań widać zdanie po zdaniu
(`harness/cytaty.py`), nie przybyło ono ani jednemu.
