# Gramatyka i podzbiór

Wykluczenie słownikowe wywodzi z kształtu to, co słownik deklaruje wprost.
`admissible` w `olski/segmentacja.py` odbiera czytanie rzeczownikowe formie,
którą olski czyta jako słowo klasy zamkniętej, po kryterium nieodmienności,
a Morfeusz opatruje dokładnie te czytania kwalifikatorem dziedziny:
`do` w znaczeniu nuty niesie `muz.`, `go` w znaczeniu gry niesie `gry`,
a `at`, `cent` i `real` niosą `monet.`
Ruchem jest przeczytać, ile z tego, co `admissible` odbiera nad korpusem
audytowym, niesie taki kwalifikator, i ile niesie go czytanie, którego ono nie
odbiera — bo dopiero druga liczba mówi, czy kryterium dałoby się zastąpić listą.
Do rozstrzygnięcia jest przy tym, że lista byłaby druga i osobna od
`POZA_REJESTREM` w `olski/rejestr.py`: `muz.` i `gry` nazywają dziedzinę,
a dziedzina rejestru nie odsyła i odsyłać nie może,
bo `anat.` przy `oczy` wskazuje czytanie trafne
([`docs/sklad.md`](../docs/sklad.md#kwalifikator-mówi-o-formie-dwie-rzeczy-i-tylko-jedna-jest-rejestrem)).

Trzy naprawy jednego znaku odrzucenie zgłasza trzema kształtami zamiast jednym.
`unclosed` nazywa napis, który olski czyta po domknięciu, i podaje znak
(`_domknięcie` w `olski/werdykt.py`),
cudzysłów prosty dostaje podpowiedź wpisaną osobno w `_podpowiedź` tam samo,
a brak spacji po kropce nie dostaje nic i wychodzi jako zatrzymanie na formie,
która z pomyłką autora nie ma nic wspólnego.
Świadkiem jest w każdym z trzech gramatyka — reguła strzela tam,
gdzie podmieniony znak zmienia werdykt z „no reading” na czytanie —
więc żadna nie potrzebuje kalibracji, której brak zamknął pakiet reguł
([`docs/linter.md`](../docs/linter.md#co-zamknęło-pakiet-reguł)).
Ruchem jest jedna klasa napraw wraz z jednym kształtem wypowiedzi o niej,
a decyzją, którą to wymusza, czy zdanie naprawialne zostaje w `rejected`:
zostawione tam mierzy podzbiór jak dziś, a wyjęte rusza pokrycie nad korpusami.
Do przeczytania jest więc to, ile zdań Składnicy i korpusu audytowego
odrzucenie bierze za sam cudzysłów albo za brakującą spację.

Odrzucenie nie widzi małej litery na początku zdania.
`cena jest niska.` wychodzi jednym czytaniem, choć zdaniem pisanej polszczyzny nie jest.
Świadkiem jest tu norma, a nie rozbiór, bo gramatyka wyprowadza oba warianty tak samo.
Norma ma dwa wyjątki i oba trafiają w ten rejestr.
Nazwę pisaną małą literą zostawia się małą także na początku zdania,
bo granicę zdania pokazuje kropka poprzedniego
(Poradnia PWN, dr Jan Grzenia, „mała litera na początku nazwy własnej”) —
czyli to samo, co u nas rozstrzyga o `FRAGMENT`.
Pozycja wyliczenia zamknięta przecinkiem albo średnikiem zaczyna się małą literą,
bo ciągnie zdanie zaczęte przed dwukropkiem.
Blokerem jest ekstrakcja: `harness/markdown.py` zdejmuje backticki
i nie mówi nikomu, że token nimi stał,
a bez tego wyjątku pierwszego nie da się napisać —
i nie zastąpi go test na polskie słowo,
bo `odmień` i `przejrzyj` są nazwami funkcji i polskimi słowami naraz
([`CLAUDE.md`](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).
Ruchem jest więc najpierw ta informacja przeniesiona przez ekstrakcję,
a dopiero po niej kryterium, którego dowodem jest zero trafień nad prozą repozytorium:
bez wyjątków strzela ono na pierwszych zdaniach akapitów kilkadziesiąt razy
i ani razu trafnie.

`GRUPA_JEDNYM_SŁOWEM` w `olski/segmentacja.py` wypisuje części mowy,
którymi grupa imienna staje sama jednym słowem,
czyli fakt o gramatyce zapisany drugi raz obok niej.
Głowa dopisana do grupy imiennej tej listy nie ruszy,
a wtedy przytoczenie zamieni czytania napisowi, który cudzysłów bierze już jako grupę,
i napis dostanie drugie czytanie albo straci rodzaj
([`docs/konstrukcje-gramatyczne/zdanie-złożone.md`](../docs/konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).
Rozjazdu nie widzi ani suita, ani przebieg nad prozą:
statusy ruszy dopiero napis z nową głową postawiony w cudzysłowie.
Ruchem jest pytanie gramatyki wprost, zamiast trzymania listy —
`Grammar` odpowiada dziś, czy terminal bierze czytanie
(`licencjonowane` w `olski/segmentacja.py`),
a brakuje odpowiedzi, czy bierze je terminal w produkcji grupy imiennej.
Do rozstrzygnięcia jest, czy to pytanie warto do `Grammar` dopisać,
czy taniej jest pilnować listy testem, który dla każdej głowy grupy
żąda jednego czytania od napisu w cudzysłowie.

Lista predykatywów nie ma `pora` ani `nie sposób`,
a Składnica ma zdania, które orzekają jednym z tych dwóch:
`Już pora.`, `Pora do łóżka!`, `Pora na nastolatki.`, `Wprost nie sposób!`
oraz `Nie sposób nie żywić uczucia podziwu dla odwagi pierwszych żeglarzy.`
Wszystkie przechodziły, dopóki `pora` czytała się czasownikiem `porać`,
a `sposób` rozkaźnikiem od `sposobić`;
zawężenie ramy do lematów całej formy te czytania zdjęło
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
więc dziś są odrzucone i werdykt mówi o nich prawdę.
Ruchem jest dopisanie obu do `PREDYKATYWY` w `olski/subset/słowa.py`,
a czytanie `pred` obie formy u Morfeusza mają, więc terminal ma o co zapytać.
Trudność jest przy `nie sposób`:
przeczenie stoi w ciele osobno od predykatywu,
więc lemat `sposób` dopisany do listy wpuszcza też `sposób` bez przeczenia,
czego polszczyzna nie ma.
Do przeczytania jest, czy bank drzew ma zdanie z `sposób` bez przeczenia,
bo od tego zależy, czy sama lista tu wystarczy.

`olski/subset/` grupuje po rodzaju, a nie po konstrukcji, więc jedna konstrukcja
rozkłada się w nim na cztery miejsca, i po podziale na moduły są to cztery pliki:
rolę bierze `olski/subset/deklaracja.py`, ramę `olski/subset/rama.py`,
listę lematów wraz z terminalem `olski/subset/słowa.py`,
a ciała moduł jej gospodarza.
Kto ją czyta albo zdejmuje, chodzi po tych czterech miejscach,
choć zmieniają się one razem i tylko razem mają sens —
sonda różnicowa grupuje właśnie po konstrukcji (`grupa` w `harness/ruch.py`).
Ruchem jest blok na konstrukcję: rama, lista, terminal i ciała pod jednym
nagłówkiem komentarza, w kolejności, w jakiej konstrukcje wchodziły.
Ceną są dwie rzeczy, które w bloku nie zmieszczą się nigdy: rola musi stać w
`DEKLARACJA`, bo werdykt czyta jedną listę ról, a ciało musi stać w module
swojego gospodarza, bo stamtąd `build` bierze produkcje.
Argumentów taki blok wziąłby przy tym niewiele, i to jest już przeczytane:
sekcje dzielą się po gospodarzu, po kilka na moduł,
a symbole, które jedna z nich wpisuje, a czyta je druga,
wylicza blok na czele `build`.
Blok na konstrukcję zmieściłby się przez to wewnątrz jednej sekcji,
zamiast ciąć ją w poprzek.
Rodzina czoła jest tu precedensem: jej cztery miejsca czytają jedną wartość
(`Rodzina` w `olski/subset/deklaracja.py`), a nie stoją pod jednym komentarzem.
Wprost się on jednak nie przenosi, bo rodzina wypisuje same nazwy symboli,
a konstrukcja wypisuje też ciała, a te powstają wywołaniem, nie wartością.
Miejsc bywa przy tym więcej niż cztery, i pokazuje to imiesłów przysłówkowy
([`docs/konstrukcje-gramatyczne/okolicznik.md`](../docs/konstrukcje-gramatyczne/okolicznik.md#imiesłów-przysłówkowy-stoi-tam-gdzie-okolicznik-wyrażony-zdaniem)):
dochodzą przy nim wpis wśród gospodarzy oraz wpis w `NIE_WYPUSZCZANE`,
a ciała ma w dwóch miejscach jednej sekcji, bo głowa stoi osobno od swoich pozycji.

`fraza_bezokolicznikowa` w `olski/subset/zdanie.py` ma ciała w dwóch sekcjach,
i jako jedyny z czterech takich symboli nie ma po temu powodu:
bezokolicznik bez wypełnienia wpisano przy grupie orzeczenia, a z wypełnieniem
przy orzeczeniu, i rozdziela je sama kolejność, w jakiej powstawały.
Ruchem jest przeniesienie tego pierwszego do drugiej sekcji.
Ceną jest pomiar: przeniesienie rusza kolejność wpisywania produkcji,
a tę widać po czytaniach (docstring `build`),
więc zmiana żąda odcisku prozy repozytorium, a nie samej zielonej suity.

`NIE_WYPUSZCZANE` w `olski/subset/deklaracja.py` wylicza cechy, których symbol nie niesie
w górę, i żadnego z tych wpisów nie widać po werdykcie:
gramatyka bez całej listy wydaje nad prozą tego repozytorium
te same werdykty i te same liczby czytań, zdanie po zdaniu,
a poza `dostawka` o żadną z tych cech nie pyta nad swoim symbolem
ani jedna produkcja.
Lista trzyma więc deklarację przy tym, co produkcje wypisywały przed perkolacją.
Do rozstrzygnięcia jest jedno z trojga: lista zostaje jako fakt o symbolu,
znika i wszystko wychodzi z głowy,
albo odwraca się w inwentarz — symbol wylicza, co niesie —
i wtedy check porównuje inwentarz z pytaniami w obie strony,
czyli łapie także cechę wypuszczaną bez pytającego; takich są dwie
(liczba i rodzaj `rdzeń_pytajny`, wypisane razem z rodziną względną,
której poprzednik ich żąda).
Zdjęcie listy jest zmianą w gramatyce i pomiaru żąda osobno:
proza tego repozytorium nie rusza się wcale, a banku drzew nie zmierzył nikt.
Osobno stoi czas rozbioru, bo cechę wypuszczaną las rozdziela na klasy pozycji
(`klasy` w `olski/parse.py`), a wpisów jest kilkadziesiąt.
Do przeczytania jest `_wysunięta_rola` w `olski/subset/podrzędne.py` obok tej listy,
bo tamta funkcja pisze dwie rodziny czoła jedną ręką i stąd te dwie cechy.

Skład składa `Skutek.więc` w napis, który olski od tej pory wyprowadza,
a obieg się na nim nie zamyka:
`_członowie` w `olski/skład/rozbiór.py` czyta ciało `zdanie_składowe , zdanie`
i nie czyta tego z przecinkiem oraz spójnikiem,
więc `Program zapisuje ustawienia, więc linter sprawdza tekst.` wraca powodem,
że zdanie złożone tego kształtu nie ma tu kategorii.
Ruch nie jest dopisaniem czwartego kształtu do `_członowie`:
`więc` niesie relację, a nie następstwo,
i `SPÓJNIKI` w `olski/skład/spójniki.py` mówi o nim tyle samo, co o `bo`,
więc to zdanie ma wrócić okolicznikiem w relacji `skutek`, a nie `Ciągiem`.
Gramatyka wyprowadza je natomiast koordynacją, bo `więc` zdania nie podporządkowuje,
i to jest cała trudność tego wpisu: dwa tory nazywają jedną konstrukcję inaczej,
a obieg żąda, żeby napis wrócił tym drzewem, z którego wyszedł.
Do przeczytania jest `_okolicznikowe` w tym samym pliku,
czyli droga, którą wraca `bo`, i `test_zdanie_spoza_gramatyki_mówi_o_gramatyce_a_nie_o_brakującej_kategorii`
w `tests/test_rozbiór.py`, który stał na tym zdaniu i stoi teraz na narzędniku.

Okolicznik wyrażony zdaniem stoi w gramatyce przed swoim zdaniem i za nim,
a polszczyzna stawia go też w środku:
`Program, gdy linter sprawdza tekst, zapisuje ustawienia.` jest zdaniem odrzuconym.
Ruchem jest trzecie ciało `okolicznik_zdaniowy` z przecinkiem po obu stronach
wraz z pozycją w ciele zdania składowego, czyli tam, gdzie dziś stoi podmiot,
a przed nim pomiar: pozycja ta konkuruje ze zdaniem względnym,
które przecinkami odgradza się tak samo
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
więc cena stoi w jednoznaczności zdań już przyjętych, a nie w liczbie ciał.
Do przeczytania jest cena obu pozycji, które ta konstrukcja już ma,
którą trzyma commit, który je wpuścił,
bo trzecia wraca z pytaniem tej samej postaci.
Tym samym brakiem jest okolicznik wewnątrz zdania względnego:
`Reguła, która rozstrzyga, gdy tekst jest gotowy, jest tania.` jest odrzucone,
bo obie pozycje stoją na symbolu `zdanie_składowe`,
a `rdzeń_względny` jest osobnym symbolem
i ciała z tym symbolem w środku ma jedno.
Zdanie odrzucone jest przy tym werdyktem uczciwym, a nie czytaniem nieprawdziwym,
więc pozycja ta nie ma pilności, jaką miałby brak wydający `valid`.

Wysunięcie zdania podrzędnego jest faktem o spójniku i stoi w dwóch plikach:
`SPÓJNIKI_WYSUWANE` w `olski/subset/słowa.py` mówi to o kilkunastu lematach analizy,
a `SPÓJNIKI` w `olski/skład/spójniki.py` o kilku, których używa skład,
i obie listy zgadzają się dziś tam, gdzie się przecinają.
Rama czasownika poszła tą samą drogą i zeszła do jednego pliku,
bo jest faktem o słowie, a nie o kierunku, w którym się go używa
([`docs/roadmap.md`](../docs/roadmap.md#etap-2-walencja-czytana-raz)),
a spójnik jest takim samym faktem.
Ruchem jest leksykon spójników czytany przez oba kierunki,
wzorowany na `olski/walencja.py`, i przed nim jedno rozstrzygnięcie:
skład trzyma relację obok szyku, a analiza relacji nie zna,
więc albo leksykon niesie kolumnę, której analiza nie czyta,
albo relacje dochodzą do niego dopiero z kategoriami składu,
których dziś nie ma na warunek ani na przyzwolenie.
Do przeczytania jest `olski/walencja.py` wraz z tym,
co obu kierunkom z leksykonu walencyjnego wyszło różnego
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)).

Okolicznik przysłówkowy bierze całą część mowy, a Morfeusz daje czytanie `adv`
formom, których ten rejestr używa jako przyimka albo spójnika: `wobec`, `gdy`, `sam`.
Wychodzą z tego czytania, których polszczyzna w tych miejscach nie ma —
`postępować wobec innych w duchu braterstwa` dostaje trzy czytania z `wobec`
w roli okolicznika, a `Program zapisuje ustawienia, gdy linter sprawdza tekst.`
wychodzi obok czytania podrzędnego drugim, w którym `gdy` jest okolicznikiem
zdania spiętego przecinkiem.
Cena tej klasy jest przez to zmierzona i wynosi sześć zdań Składnicy:
tyle straciło jednoznaczność pod morfologią żywą, kiedy weszła podrzędność
okolicznikowa, i wszystkie sześć niesie `gdy` albo `kiedy`.
Kryterium słownikowe `admissible` w `olski/segmentacja.py` po nie nie sięga,
bo pyta o czytanie rzeczownikowe stojące obok wyrazu funkcyjnego.
Ruchem jest warunek na tę klasę, a dwa kandydujące są zmierzone i żaden nie jest darmowy.
Odsiew czytania przysłówkowego przy czytaniu przyimkowym kupuje nad Składnicą
pod morfologią żywą jednoznaczność dwunastu zdaniom, a jedenastu odbiera wyprowadzenie
(sześciu przyjętym i pięciu wieloznacznym); odsiew przy czytaniu spójnikowym kupuje
tyle samo i odbiera trzydziestu pięciu, bo zabiera `jak` w pytaniu.
Pod morfologią złotą oba nie ruszają niczego, bo anotator wybrał tam jedno czytanie
na token, więc pomiar tej klasy idzie po morfologii żywej i po prozie.
Do przeczytania jest lista form, które warunek dotknie: `blisko` i `naprzeciw`
niosą czytanie przysłówkowe, którego polszczyzna używa,
więc cena stoi w zdaniach, a nie w samych czytaniach.
Kandydat trzeci wyszedł z czytania zdań przyjętych i nie ma pomiaru:
czytanie przysłówkowe stojące przy czytaniu rzeczownikowym tej samej formy.
Zabiera ono `Wszystko wyżej pyta o zdanie, po którym zostaje czytań kilka.`
oraz `Czego na tej liście nie ma.`, czyli zdania przyjęte na czytaniu,
którego polszczyzna nie ma
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)),
a dwa kandydujące wyżej po nie nie sięgają,
bo przy przysłówku stoi w nich rzeczownik, a nie przyimek ani spójnik.

Dopełnienie bezokolicznika wysunięte przed formę osobową ma szyk jeden,
a polszczyzna ma ich kilka: `Większości premier nie może ruszyć.`
oraz `Większości nie może ruszyć.` są odrzucone, gdzie
`Premier większości nie może ruszyć.` wyprowadza się
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze)).
Wzór stoi obok: deklaracja z dopełnieniem przy formie osobowej wypisuje pięć szyków
warunkiem precedencji (`_poza_orzeczeniem` w `olski/subset/rama.py`),
a podmiot opuszczony ma tam ciało osobne.
Ruchem jest ten warunek nad deklaracją z frazą bezokolicznikową
wraz z ciałem bez podmiotu, a przed nim pomiar:
szyk z dopełnieniem na czele konkuruje naraz z okolicznikiem wysuniętym przed zdanie
i z przydawką dopełniaczową, czyli z dwiema pozycjami,
z których żadna nie konkuruje z szykiem, który wszedł.
Cenę szyku, który wszedł, trzyma tamta sekcja i mówi ona,
od czego zaczyna każdy następny: zakupu nie ma tam żadnego,
więc szyk dopisany zaczyna od ceny, a zakup ma do policzenia.

Czoło zdania względnego sięga do formy osobowej i nie sięga do bezokolicznika pod nią,
choć dopełnienie wysunięte przed formę osobową sięga tam ciałem wypisanym
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze)).
`Ustawa, którą organ gminy może wydać, jest tania.` jest przez to odrzucone,
a jest to jedyne zdanie, które kupuje cecha przeciągana
([`docs/design-notes.md`](../docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)),
więc pozycja dopisana wypisanymi ciałami zabiera luce cały jej zakup
i zamyka rozwidlenie, które tamta sekcja trzyma otwarte —
i to, a nie samo zdanie, jest tu stawką.
Ruchem jest `_wysunięta_rola` w `olski/subset/podrzędne.py` pisząca ten szyk także z frazą
bezokolicznikową, czyli te same córki, które wypisała deklaracja obok,
z czołem w miejscu dopełnienia.
Do rozstrzygnięcia jest, czy warto:
zdania tego kształtu nie ma ani jeden korpus, który to repozytorium czyta,
i mówi to sekcja o zdaniu względnym wraz z poleceniem,
którym sprawdzono rejestr ustaw
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
a `rdzeń_względny` ma kilkadziesiąt ciał
i pozycja mnoży je przez klasy walencyjne.
Do przeczytania jest przy tym `harness/luka.py`:
tamten wariant zdejmuje ciała `rdzeń_względny` i zastępuje je luką,
więc pozycja dopisana do nich rusza każdą liczbę tamtej sekcji.

Myślnik stoi u olskiego między dwoma zdaniami i nie stoi wewnątrz zdania,
a polszczyzna stawia go wewnątrz w miejscu pominiętego orzeczenia:
`Ania lubi cydr, Janek — piwo.` jest odrzucone.
Człon bez czasownika olski ma i licencjonuje go spójnikiem
([`docs/konstrukcje-gramatyczne/zdanie-złożone.md`](../docs/konstrukcje-gramatyczne/zdanie-złożone.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)),
więc `Ania lubi cydr, a nie piwo.` wyprowadza się i werdykt nazywa czasownik,
do którego ten człon dochodzi.
Różni je dwie rzeczy. Licencją jest tu sam znak, a nie spójnik, czyli ciało osobne.
Oraz `Janek — piwo` niesie dwie pozycje, a nie jedną,
więc człon musiałby zgodzić się z członem obok co do ról, których nie wypowiada,
a dzisiejsze ciało bierze jeden konstytuent i o rolach nie mówi nic.
Do rozstrzygnięcia jest przedtem granica zdania:
`Ania lubi cydr. Janek — piwo.` ma orzeczenie w zdaniu poprzednim,
a olski orzeka o zdaniu, nie o akapicie
([`docs/roadmap.md`](../docs/roadmap.md#co-jest-budowane)),
więc albo konstrukcja wchodzi tylko wewnątrz jednego zdania,
albo werdykt przestaje być wypowiedzią o zdaniu.
To rozstrzygnięcie idzie pierwsze, bo od niego zależy,
czy pozostałe dwie rzeczy mają gdzie stanąć.
Wpis waży przy tym więcej, niż mówi liczba zdań, i mówi to drugie użycie tego znaku:
`Premier — większości nie może ruszyć.` nie miałoby czytania z grupą
`premier większości`, bo grupa imienna myślnika nie przechodzi,
czyli autor dostaje znak, którym rozstrzyga sam
([`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md)),
a takich pozycji ten podzbiór ma niewiele.
Ceną jest to, że znak ten spina dziś dwa zdania,
a para myślników ma wpis osobny, ten o wtrąceniu w środku zdania,
więc ciało wewnątrz zdania konkuruje z obydwoma i sesja bierze je razem.

Zamknięta lista kopul nie ma `stawać się` ani `okazywać się`,
a polszczyzna orzeka nimi narzędnik tak samo jak `zostawać`.
`Mao stał się na wiele lat przywódcą największego narodu na kuli ziemskiej.`
i `Człowiek staje się wyleniałym tygrysem.` są przez to odrzucone,
i są to dwa z 75 zdań, które zawężenie narzędnika odrzuca nad Składnicą,
a jedyne dwa, które odrzuca niesłusznie
([`docs/corpus.md`](../docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Przeszkodą nie jest lista, tylko cząstka: `KOPULA` w `olski/walencja.py` jest
warunkiem na lemat, a te dwa czasowniki są kopulami wyłącznie z `się`,
którego produkcja kopuli nie ma gdzie postawić —
[`docs/subset.md`](../docs/subset.md#what-the-grammar-covers) mówi to przy liście.
Ruchem jest ramka narzędnikowa w leksykonie zwrotnym,
czyli ta sama droga, którą walencja rozdziela formę z cząstką od formy bez niej,
a do przeczytania jest, co zwrotna kopula robi z `Ludzie rodzą się wolni.`,
gdzie orzecznik zgodny stoi dziś przy czasowniku zwrotnym niebędącym kopulą.

Klasa kopuli zabiera lematowi wpis z leksykonu (`_walencja` w `olski/subset/rama.py`),
więc kopula nie bywa naraz czasownikiem, który bierze zdanie z `że`.
Widać to na `bywać`, odkąd lemat ten stoi w `KOPULA` w `olski/walencja.py`:
`Odpowiedzią bywa decyzja.` przechodzi z odrzuconego na przyjęte,
a `bywa tak, że` zostaje bez ani jednego czytania —
jedno zdanie Składnicy i jedno zdanie `docs/subset.md`.
Ceną tą zapłacono za rolę: bez tego wpisu `Skreślenie bywa całą naprawą.`
też ma jedno czytanie, tyle że z narzędnikiem w okoliczniku, a nie w orzeczniku
([`docs/konstrukcje-gramatyczne/okolicznik.md`](../docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Ruchem jest rama kopuli liczona jako suma z ramą tego lematu,
a nie jedna wartość na całą listę,
i wtedy ta sama zmiana rusza `być`, któremu Walenty daje dopełniacz,
bezokolicznik oraz zdanie podrzędne; tamtego rozszerzenia nie zmierzył nikt.
Do przeczytania przed pomiarem jest, że sondzie różnicowej tego nie zmierzyć
podmianą samej stałej: klasy walencyjne liczą się przy imporcie modułu,
a nie w `build`, więc wariant złożony po podmianie `KOPULA` jest tą samą gramatyką.

Czas przeszły zostawił za sobą resztkę wiersza `praet`, której nikt nie przeczytał.
`praet` prowadził kolejkę blokerów,
a po dopisaniu tej formy do `orzeczenie` w `olski/subset/zdanie.py`
wiersz zmalał o rząd wielkości
i to, co w nim zostało, staje na czasie przeszłym dalej.
Od tamtej pory wiersz rośnie, bo każde dopisanie przesuwa na czasownik blokery zdań,
których nie przyjęło ([`docs/corpus.md`](../docs/corpus.md#where-the-analyses-stop)),
więc do przeczytania jest resztka dzisiejsza, a nie ta z chwili dopisania.
Nie wiadomo, czy stoi za tym jedna konstrukcja, czy dwadzieścia:
`Wózek zwolnił biegu i przystanął.` i `Pani Zofia była w rozpaczy.`
są w tej resztce obok siebie, a łączy je tyle, że bloker wskazał czasownik.
Ruchem jest odczytanie tej resztki i rozbicie jej na klasy,
z tego klasy nazwane w [`docs/subset.md`](../docs/subset.md#what-it-does-not-cover-yet),
jeśli któraś jest konstrukcją, a nie zbiegiem okoliczności.
Do przeczytania jest sam `bloker` w `olski/pokrycie.py`:
nazywa on formę, na której rozbiór stanął,
a przy zdaniu z czasownikiem w środku bywa to forma stojąca za prawdziwą przyczyną,
więc część tej resztki może być artefaktem tego odczytu, a nie brakiem w gramatyce.

Aglutynant dochodzi tylko do czasownika, przy którym stoi.
`_formy_skończone` w `olski/subset/rama.py` bierze `praet` z `aglt` po nim,
bo tak Morfeusz tnie `napisałem`,
a polszczyzna stawia tę końcówkę także przy innym słowie zdania:
`gdzieś ty był`, `myśmy przyszli`, `dlaczegoś to zrobił`.
Tym samym brakiem jest końcówka na spójniku niosącym cząstkę trybu —
`żebym napisał`, które Morfeusz tnie na `żeby` i `m`
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#tryb-przypuszczający-jest-jedną-cząstką)).
Ruchem jest aglutynant przyłączany do zdania, a nie do czasownika,
czyli cecha osoby wypuszczana w górę z miejsca, w którym końcówka stanęła.
Do rozstrzygnięcia jest, czy warto:
konstrukcja jest w rejestrze technicznym rzadka albo nieobecna,
a w prozie literackiej Składnicy nie jest.
Po stronie spójnika policzono trzydzieści zdań banku drzew —
`Żebym go chociaż mocno zranił!`,
`Nikt nas nie zmusi, abyśmy w nim partycypowali.` —
a po stronie zdania z `ty` nie policzył ich nikt.
Do przeczytania są te zdania Składnicy, w których `aglt` stoi poza `praet`,
bo od ich liczby zależy, czy ten wpis jest wart ceny ruchu.

Pozycja pytania zależnego stoi w ramie domyślnej i nikt nie zmierzył jej zawężenia.
`RAMA_DOMYŚLNA` w `olski/subset/rama.py` daje `int` każdemu czasownikowi,
tak jak daje mu `comp`, a Walenty wypisuje osobno lematy z jednym i z drugim.
Zawężenie `comp` do leksykonu zmierzono i nie kupiło ani jednego czytania,
a przy `int` wynik nie musi wypaść tak samo:
pytanie zależne konkuruje z koordynacją przecinkiem i ze zdaniem względnym,
gdzie zdanie z `że` nie konkuruje z niczym, bo spójnika `że` nie bierze nic innego.
Wpis waży więcej, odkąd `co` bierze poprzednik zdaniowy: cena tamtej pozycji
stoi prawie cała na zdaniach z pytaniem zależnym, którym ono dokłada
drugie czytanie
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie)),
więc zawężenie `int` do leksykonu odbiera ją tym z nich,
których czasownik pytania nie żąda.
Ruchem jest osobne zdanie leksykonu o `cp(int)`, wzięte przez `harness/walenty.py`,
i wariant gramatyki bez `int` w ramie domyślnej, zmierzony wobec olskiego.
Czym ten wariant zmierzyć, jest rozstrzygnięte:
zawężenie ramy jest zmianą danych, a nie grupą produkcji,
i takiemu wariantowi `Sonda` podaje gramatykę funkcją (`Sonda.gramatyki`).
Do przeczytania jest przy tym, czy skład ma dla tego zdania czytelnika:
zdanie o zdaniu podrzędnym czyta ono (`rama` w `olski/walencja.py`),
a pytania zależnego
`olski/skład/składnia.py` nie ma czym postawić,
więc zdanie dopisane bez tej kategorii jest danymi, których nie czyta nikt.

Lista zaimków rzeczownych nie ma źródła poza pamięcią tego, kto ją pisał.
O każdym lemacie `ZAIMEK_RZECZOWNY` w `olski/subset/słowa.py` sprawdzono w Morfeuszu,
że niesie czytanie `subst`, a czy lista jest pełna, nie sprawdził nikt
i słownikiem się tego nie sprawdzi:
czytanie zaimka niczym się nie różni od czytania rzeczownika
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)).
Ruchem jest wykaz lematów, które nad korpusem stają w tej pozycji —
forma o czytaniu `subst` tuż przed formą w dopełniaczu —
uszeregowany częstością i przeczytany ręką:
zaimka nie odróżni od rzeczownika żaden test, ale odróżni go czytelnik.
Do przeczytania jest przedtem cena wpisu:
lemat dopisany odbiera czytanie i żadnego nie dodaje,
więc kandydat mylny zabiera zdanie, które gramatyka dziś wyprowadza.

`pod względem` żąda licencji od słowa, do którego się przyłącza,
a olski żąda licencji tylko od dopełnienia.
Czytelnik odrzuca `wolni pod względem swej godności` bez pomocy składni,
bo `równy` ma pozycję na wzgląd, a `wolny` jej nie ma.
Tę samą obserwację robi nad `przewyższać`
[`docs/subset.md`](../docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera),
gdzie porównanie mówi, w czym jedno przewyższa drugie,
i nie ma jej dziś gdzie zapisać.
Leksykon walencyjny mówi o pozycjach ramy, które czasownik bierze albo których nie bierze
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)),
a okolicznik pozycji ramy nie zajmuje i przyłącza się do każdego czasownika za darmo,
więc żaden wpis nie odbiera czytania,
w którym wzgląd dochodzi do `rodzą się`.
Ruchem jest zdanie leksykonu odwrócone wobec tamtych trzech:
nie „ten czasownik czegoś nie bierze”, tylko „to wyrażenie przyimkowe
przyłącza się tam, gdzie licencjonuje je leksykon”,
czyli cecha przy przyimku zleksykalizowanym, a nie przy jego gospodarzu.
Robi ono z pierwszego artykułu Deklaracji zdanie olskie:
odejmuje czytanie z `rodzą się`, bo ten czasownik wzglądu nie licencjonuje,
a zostaje czytanie z `równi`, czyli jedno.
Odejmuje też czytanie nad całym ciągiem współrzędnym,
bo `wolny` wzglądu nie licencjonuje tak samo.
Do rozstrzygnięcia jest, czy to jeszcze walencja, czy już ta warstwa,
którą [`docs/open-questions.md`](../docs/open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma)
odkłada poza gramatykę jako odpowiedź trzecią;
różnicę robi to, że leksykon w gramatyce już jest, a tamta warstwa nie.
Do przeczytania jest, ile takich przyimków rejestr ma,
bo `pod względem` jest jednym z nich i nikt nie policzył, ile jest reszty,
oraz co Walenty mówi o wzglądzie:
pozycje zleksykalizowane wypisuje on w schemacie,
a przymiotnika, który licencjonuje tu wzgląd, nie ma w pliku czasownikowym,
z którego leksykon powstaje,
choć archiwum obok tego pliku niesie katalog przymiotnikowy.
Kryterium wejścia ma ten ruch to samo, co każda warstwa więzowa:
[wyprowadza się z gramatyki albo jest gramatyką pisaną drugi raz](../docs/design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej),
a leksykalnie znaczy to tyle, że pozycję wypisuje słownik.
Jeśli Walenty jej nie wypisuje, ruchu nie ma i cały wpis zamyka skasowanie,
bo „brzmi nielogicznie” jest sądem o świecie, a nie faktem o słowie:
olski melduje wtedy wieloznaczność, tak samo jak melduje ją wszędzie indziej.

Wysunięte wyrażenie przyimkowe nie potrzebuje licencji od niczego,
więc `Ustawa, o której flaga to płat, obowiązuje.` wychodzi `valid`.
Wpuszcza je ciało `rodzina.rdzeń → rodzina.modyfikator zdanie_składowe`
w `olski/subset/podrzędne.py`, które przed dowolnym zdaniem składowym dopuszcza dowolny przyimek.
Łącznik `to` przyczyną nie jest i nie jest nią kopula pod nim opuszczona:
`Ustawa, w której flaga to płat, obowiązuje.` jest polszczyzną
i wyprowadza się tym samym ciałem,
a `Ustawa, o której flaga jest płatem, obowiązuje.` jest tą samą usterką
z kopulą wypisaną wprost.
Licencji od każdego wysunięcia żądać też nie wolno,
bo `Godzina, o której poseł śpi, mija.` jest polszczyzną,
a rama `spać` wymienia `nad` i `z`.
Fakt rozdzielający te zdania jest w `olski/leksykon.txt` —
rama rzeczownika `mowa` wymienia `o`, a `flaga` ani `płat` nie mają tam wpisu —
i czyta go sam świadek ramowy w `olski/rozstrzyganie.py`,
a czemu nie czyta go gramatyka, wywodzi `olski/walencja.py`.
Dzisiejsza unifikacja tego żądania nie zapisze,
bo licencjonuje tu którekolwiek słowo zdania składowego, a nie jego głowa:
w `o których mowa jest tam` przyimka żąda rama podmiotu, kiedy głową jest `jest`.
Cechy wychodzą z samej głowy (`_wypuszczane` w `olski/grammar.py`),
a unifikacja zbiory przecina,
więc suma przyimków licencjonowanych przez wszystkie córki nie ma czym pójść w górę.
Świadek nie ma tu z kolei czego zawężać, bo gospodarz jest jeden:
wysunięte wyrażenie stoi przed całym zdaniem składowym,
a zejście w górę zatrzymuje się na rdzeniu rodziny (`gospodarze` w `DEKLARACJA`),
więc kilku gospodarzy daje dopiero luka.
Pomiar luki tych ciał nie obejmuje:
`_wysunięty_okolicznik` w `harness/luka.py` zostawia je nieruszone,
więc liczby z
[`docs/design-notes.md`](../docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)
mówią o wysuniętym podmiocie i dopełnieniu, a nie o tym wyrażeniu.
Powód tamtego odrzucenia też tu nie sięga: luka dokładała tam czytania,
których czytelnik nie ma, a czytania po gospodarzach są tymi samymi,
które olski daje wyrażeniu stojącemu na swoim miejscu
([`docs/subset.md`](../docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).
Sama pozycja zarabia na siebie i mówi to sonda różnicowa
zdejmująca ciała z `rodzina.modyfikator` w ciele, osobno dla każdego z dwóch wnętrz:
nad Składnicą pod złotą morfologią wnętrze zdaniowe wyciąga z odrzucenia
kilkadziesiąt zdań, w tym kilkanaście przyjętych jednoznacznie i zgodnych
z drzewem wzorcowym, nad korpusem ustaw kilkadziesiąt i żadnego jednoznacznie,
a jednoznaczności nie odbiera ani jednemu zdaniu w żadnym z dwóch korpusów.
Wnętrze z rzeczownikiem orzekającym nie rusza nad Składnicą ani jednego zdania
i jedno nad ustawami, czyli odpowiada rejestrowi, dla którego je wpisano.
Cena luki ma przez to górną granicę i są nią zdania,
które na tej pozycji stoją jednoznacznie, bo tylko one mają co stracić,
a sonda wypisuje je z nazwiska.

Grupa imienna mnoży ciała iloczynem, którego rozwinięcie szyku nie dosięga.
Ciała `człon_imienny` w `olski/subset/grupa.py` są iloczynem kształtów głowy
przez obecność `wyrażenie_przyimkowe` po niej,
czyli mnoży je obecność oraz kolejność rodzajów przydawki,
a nie permutacja argumentów,
więc warunek precedencji nie ma tu czego powiedzieć
([`docs/subset.md`](../docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Kształt głowy dopisany do tego symbolu wchodzi przez to jako dwa ciała,
bo `wyrażenie_przyimkowe` musi wejść razem z nim.
Zdanie względne tego iloczynu nie ruszyło i pokazuje, którędy się go omija:
dochodzi ono do symbolu `grupa_imienna`, czyli o poziom wyżej, więc jest jedną produkcją,
a nie trzecim rodzajem przydawki razy kształty głowy.
Kosztowało to symetrię w koordynacji, czyli wpis o członie lewym,
który zdania względnego nie unosi,
a `okoliczniki` w tym samym pliku się nie mnoży,
bo okoliczniki są jednego rodzaju.
Kierunek pokazywało samo zdanie względne:
`wyrażenie_przyimkowe` dochodzące do `grupa_imienna`, a nie do członu,
znosi ten iloczyn.
Zamianę tę zmierzono — cztery ciała z ośmiu zdjęte,
`grupa_imienna → grupa_imienna wyrażenie_przyimkowe` w ich
miejsce — i ona nie stoi.
Nad bankiem drzew traci jednoznaczność blisko sto zdań przyjętych,
a odzyskują ją dwa; nad prozą tego repozytorium traci ją kilka, a odzyskuje jedno.
Przyczyną nie jest piętrzenie, którego ten wpis się spodziewał
(`plik w drzewie na dysku` z obydwoma przy `plik`), tylko zasięg:
produkcja rekurencyjna przyłącza wyrażenie do każdego kształtu głowy naraz,
a cztery zdjęte ciała stoją przy głowie rzeczownikowej i odsłownikowej,
i tylko przy nich.
Czterdzieści przeczytanych zdań traci jednoznaczność na tym samym —
`Nadziałem je na haczyk i zarzuciłem.`, `Kierują go na kursy dywersji.` —
czyli na wyrażeniu przyłączonym do zaimka,
którego polszczyzna tam nie przyłącza;
jedno traci ją na grupie liczebnikowej.
Iloczyn zostaje przez to, czym był, a droga do jego zniesienia biegnie
przez cechę, która odróżnia głowę biorącą przyłączenie od zaimka,
i wtedy `grupa_imienna → grupa_imienna wyrażenie_przyimkowe`
żąda tej cechy zamiast brać wszystko.
Do przeczytania przed taką cechą jest jej cena w czasie rozbioru:
klasa cech rozdziela pozycje lasu (`klasy` w `olski/parse.py`),
a wpis o produkcjach formy `bedzie` mierzy, ile kosztuje jedna klasa więcej.
Do przeczytania jest też `_role` w `olski/skład/rozbiór.py`,
bo czyta ono kształty gramatyki po etykiecie,
więc każdy nowy poziom kosztuje tam gałąź.

Rama mówi, co czasownik bierze, i nie mówi, ile tego bierze.
Dopełnień stoi przy czasowniku najwyżej jedno,
bo tyle stoi w ciele każdej produkcji `wypełnienia` w `olski/subset/zdanie.py`,
a nie dlatego, że rama tak mówi;
ruchem jest rama zużywana, czyli ta,
[którą pokazuje Świgra](../docs/swigra.md#valency-as-a-resource-that-gets-consumed):
pozycja zajęta znika z tego, co niesie reszta grupy.
Wolno ją wyrazić cechą o dziedzinie skończonej,
bo pozycji jest w ramie skończenie wiele,
więc rozwinięcie idzie przed parsowaniem i nie rusza klasy złożoności.
Kupuje to jednak tyle, ile jest ram o dwóch pozycjach naraz,
a rama domyślna takiej nie ma:
biernik z bezokolicznikiem naraz zmierzono i nad Składnicą pod złotą morfologią
przyjmuje 289 zdań zamiast 293, a wieloznacznych ma 116 zamiast 110,
bo grupa imienna za bezokolicznikiem dochodzi wtedy i do niego, i do formy osobowej.
Pozycja, która z inną naprawdę stoi, jest już wpuszczona i jest nią celownik obok
wypełnienia ([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)),
tyle że licencji nie niesie tam rama, tylko cecha obok niej,
bo ramy unifikacja nie zużywa, a przecina.
Ruch jest przez to odwróceniem tamtej decyzji, a nie dopisaniem do niej:
rama zużywana zdejmuje tę cechę i wypowiada parę samą ramą.
Do przeczytania jest, co robi z klasami walencyjnymi:
dziś dzieli je para na dwie, a rama zużywana dzieliłaby je tym,
ile pozycji lemat bierze naraz.

Cząstka zwrotna nie ma pozycji wewnątrz czasu przyszłego złożonego.
`Fabryki nowej spółki będą się znajdować we Włoszech.` jest odrzucone,
bo cząstka stoi tam między `będą` i bezokolicznikiem,
czyli między dwiema częściami jednego orzeczenia,
a `SZYKI_CZĄSTKI` w `olski/subset/słowa.py` stawia ją po obu stronach całego ciała
(`_formy_skończone` tamże składa czas przyszły jednym ciałem `orzeczenie`).
Jest to ostatnie miejsce, w którym cząstka stoi tuż przy swoim czasowniku,
a żadne ciało jej nie bierze
([docs/konstrukcje-gramatyczne/orzeczenie.md](../docs/konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika)).
Ruchem jest trzecia pozycja w tym jednym ciele, między `bedzie` a głową,
a przed nim rozstrzygnięcie, czy rama ma wtedy być zwrotna:
głowa jest bezokolicznikiem, więc pytanie brzmi tak samo jak przy
`fraza_bezokolicznikowa`,
tylko cząstka nie stoi po żadnej stronie tej głowy.
Do przeczytania jest odmowa kopuli przy klasie domyślnej leksykonu zwrotnego:
kosztowała ona kiedyś właśnie te zdania, a odkąd cząstkę bierze bezokolicznik,
nie kosztuje nad bankiem drzew nic, więc pozycja dopisana tutaj
wraca do niej z pytaniem, czy dalej jest po co.

Olski czyta cząstkę bezosobową jako czasownik zwrotny z podmiotem.
`Myśli się językowo.` wyprowadza się przez klasę domyślną leksykonu zwrotnego,
czyli tak, jakby `myśleć się` było czasownikiem,
a `Wino białe pije się inaczej.` dostaje przez to dwa czytania,
z których to z podmiotem `Wino białe` jest czytaniem, którego polszczyzna nie ma:
zdanie z tą cząstką podmiotu nie ma, a rzeczownik w nim stoi w bierniku.
Ruchu tego olski nie bierze, bo czeka on na wpis niżej o zwrotności,
którą Walenty zapisuje pozycją, a nie lematem.
Ruchem jest trzecia głowa `orzeczenie_bezosobowe` obok predykatywu i formy
nieosobowej: forma osobowa trzeciej osoby liczby pojedynczej, w czasie przeszłym
w rodzaju nijakim, klasa walencyjna z leksykonu niezwrotnego bez orzecznika
zgodnego, cząstka w obu pozycjach.
Klasa domyślna leksykonu zwrotnego jest tą konstrukcją przeczytaną nieprawdziwie,
więc znika razem z odmową cząstki kopuli, która przy niej stoi.
Cenę przeczytano zdanie po zdaniu i zostały po tym czytaniu dwie klasy z trzech.
Klasa cząstki należącej do bezokolicznika — `Musieli się przebić.` — zeszła z tej
ceny razem z pozycją przy bezokoliczniku i jest to kilkanaście zdań banku drzew;
z reszty jedna klasa niesie `spotkać się`, czyli lemat spod wpisu niżej,
a druga zwrotność, której Walenty nie wymienia wcale.
Zakupem jest garść zdań odzyskujących jednoznaczność:
przebieg z klasą domyślną zdjętą wypuszcza dziś pojedyncze zdania z wieloznacznych
do przyjętych, czego przed tamtą pozycją nie robił ani razu.
Zgodność ról przy tym spada, bo bank drzew daje cząstce w takim zdaniu rolę podmiotu
([docs/corpus.md](../docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Kto wpis podnosi, mierzy to na nowo po wpisie niżej,
bo `spotkać się` jest po nim lematem leksykonu, a nie klasy domyślnej.

Klasa walencyjna mnoży produkcje formy `bedzie` przez lematy, których ta forma nie ma.
Czas przyszły idzie w `olski/subset/rama.py` przez tę samą pętlę co reszta form osobowych,
a `bedzie` jest u Morfeusza formą jednego lematu,
więc ciało z samą tą formą powstaje raz na klasę, a wystrzelić może w jednej.
Reszta jest produkcjami, których nie dosięgnie ani jedno zdanie,
i jest ich kilkadziesiąt, czyli kilka procent całej gramatyki.
Ruchem jest to jedno ciało pisane dla tej klasy,
której warunek wpuszcza lemat `być`, i dla żadnej innej,
pytane u samej pętli klas, a nie u listy nazw obok niej
([CLAUDE.md](../CLAUDE.md#code)).
Do rozstrzygnięcia jest, czy warto,
a odpowiada na to czas rozbioru mierzony
[na przemian](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje),
bo zysk jest tu wyłącznie w nim: ani jedno zdanie werdyktu nie zmienia.
Wpis waży więcej, odkąd leksykon zwrotny czyta zdanie o bezokoliczniku:
klas walencyjnych przybyło, a klasy mnożą tę pętlę,
więc produkcji jest o jedną trzecią więcej i przebieg nad bankiem drzew
trwa o kilka procent dłużej, mierzony na przemian.
Ten sam wzrost mnoży zarazem lematy, których `bedzie` nie ma.

Rzeczownikowe czytanie przymiotnika zabiera README ostatnie zdanie
i nie widać przy nim tego, co zdjęło zaimek.
`Linter pomaga pisać dobry kod.` wychodzi dwoma czytaniami tego samego kształtu,
bo Morfeusz daje `dobry` czytanie `subst:sg:nom.acc:m3` obok przymiotnikowego,
a `kod` czytanie lematu `koda` w dopełniaczu mnogim,
więc `dobry kod` jest raz przymiotnikiem przed rzeczownikiem,
a raz rzeczownikiem z dopełniaczem po nim.
Zaimek rzeczowny zdjął z tej klasy
[warunek w produkcji](../docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
bo `to` dopełniacza nie bierze,
a `dobry` bierze: rzeczownik odprzymiotnikowy dopełniaczem rządzi
i kryterium na tę pozycję zabiera zdania Składnicy, w których rządzi,
co zmierzone stoi w
[`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi).
Zostaje więc sąsiad, nie głowa:
pary nie ma bez dopełniacza `kod`, czyli bez lematu `koda`,
którego ten rejestr nie zna,
a rzadkość formalnego znamienia nie ma.
Do przeczytania jest, czy da się ją policzyć tak,
żeby liczba mówiła o polszczyźnie, a nie o korpusie, w którym się ją policzyło,
i pierwszym pytaniem jest, czy jakiekolwiek kryterium tu jest;
wykluczenie zbyt szerokie zabiera zwyczajne polskie słowa,
co [`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)
pokazuje na `jury` i `menu`.
Ten sam sąd niesie wpis o czytaniu przysłówkowym formy,
której ten rejestr używa jako przyimka albo spójnika,
bo oba pytają, co wykluczeniu w `admissible` wolno powiedzieć,
więc rozstrzyga je jedna sesja, a nie dwie.
Zdanie to jest przy tym warunkiem pod
[kierunkiem toru](../docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę),
bo czytanie, którego polszczyzna nie ma, jest dokładnie tym,
czego werdykt meldować nie powinien.

Dopełniacz nie ma drugiej pozycji ramy, którą ma celownik
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).
Walenty daje go przy bierniku 15 lematom, przy pytaniu 28, a przy zdaniu 6,
i te liczby są całym powodem, dla którego pozycja weszła sama celownikiem.
Ruchem jest druga wartość cechy `druga` w `olski/subset/rama.py`
wraz ze zdaniem leksykonu liczonym tak samo jak tamto,
a przed nim pomiar, bo cena tej pozycji jest po stronie żywej morfologii wysoka:
celownik dzieli formę z miejscownikiem, a dopełniacz z biernikiem i z mianownikiem mnogim.
Do przeczytania jest, czy zdanie z tą parą da się w ogóle odróżnić po werdykcie:
`Nauczyciel uczy dzieci matematyki.` wyprowadza się już dziś,
bo dopełniacz za grupą imienną czyta się jej przydawką,
więc brak tej pozycji nie odrzuca zdania, tylko odbiera mu drugie czytanie.

Rama jest w tej gramatyce stanem, a nie zasobem, i nikt nie policzył, co to kosztuje.
Pozycji już zajętej unifikacja nie ma jak odnotować, bo zajęcie zależy od pozostałych
córek, a nie od pary głowy i zależnego, i na tym walencja wypadła z kanału cech
([`docs/design-notes.md`](../docs/design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)).
Sonda więzowa płaci za to samo dwoma polami sprawdzanymi nad drzewem gotowym,
czyli `wymaga` i `zakazuje` w `harness/wiezy.py`,
i jest to jedyny znany warunek, którego przecięcie zbiorów nie umie powiedzieć,
a warstwa za parserem umiałaby.
Do przeczytania jest przedtem, czy w tej gramatyce jest w ogóle co zdejmować:
ciało produkcji wylicza córki, więc pozycja wypełniona dwa razy żąda dwóch ciał,
a jeżeli żadne takie nie stoi, cały wpis zamyka skasowanie z powodem w commicie.
Jeśli stoi, ruchem jest warunek nad czytaniem gotowym wraz z jego ceną
zmierzoną tak, jak mierzy się wpuszczenie pozycji.

Produkcji, której żadne ciało nie dopasuje, nie pilnuje nic.
`dopełnienie → grupa_imienna[case=inf]` stała w gramatyce tak długo,
ile trwało czytanie
`DOKŁADANE` jako listy przypadków, i nie odbierała ani zdania, ani czytania:
grupa imienna przypadka `inf` nie niesie, więc ciało po prostu nie domykało się
nigdy.
Suita tego nie widzi, bo werdykty wychodzą te same,
a `nieosiągalne` w `olski/grammar.py` też nie, bo pyta o symbol,
a tu nieosiągalny jest układ cech pod symbolem osiągalnym.
Znalazła ją ręka, czytając trzy miejsca, które wypisywały jedną listę.
Ruchem jest check pytający o wartość, a nie o nazwę:
dla każdej pozycji ciała będącej `Sym` z wartością wypisaną wprost
ma istnieć produkcja tego symbolu, która tę wartość wypuszcza.
Do przeczytania jest przedtem, ile taki check kosztuje wyprowadzenia:
cecha idzie zwykle zmienną wspólną z córką, więc odpowiedź żąda punktu stałego
po całej gramatyce, a nie spojrzenia na jedną produkcję,
i to rozstrzyga, czy jest to check, czy sonda puszczana ręką.
Wynikiem pierwszego przebiegu jest lista produkcji martwych,
a każda z nich jest albo skreśleniem, albo pozycją napisaną nie tak, jak chciano.

Rzeczownik `soba` zabiera kilkunastu zdaniom banku drzew jednoznaczność,
odkąd zaimek zwrotny ma pozycję
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym)).
Czytania tego polszczyzna w tych zdaniach nie ma —
`sobie` i `sobą` są w nich zaimkiem — więc jest to wieloznaczność w słowniku,
a nie w polszczyźnie, czyli dokładnie to, co odbiera `admissible`
w `olski/segmentacja.py`
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).
Kryterium tamtego wykluczenia po ten lemat nie sięga i sięgnąć nie może:
pyta ono o rzeczownik nieodmienny, a `soba` odmienia się przez przypadki.
Mechanizm już stoi — `pomijane` w sekcji `lematy` w `olski.toml`
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#słownictwo-projektu-orzeka-o-lemacie-w-obie-strony)) —
a nie stoi w nim ani jeden lemat i to jest tu decyzja do podjęcia.
Do przeczytania jest przedtem, ile takich lematów widać nad bankiem drzew:
sonda różnicowa zaimka wypisuje zdania tracące jednoznaczność pod żywą
morfologią i tyle wystarcza, żeby powiedzieć, czy lemat jest jeden, czy jest ich wiele.
Liczba ta rozstrzyga, czy `soba` idzie do konfiguracji tego repozytorium sama,
czy razem z listą, która rośnie o każdy lemat, który ktoś zauważy.
Ten sam lemat trzyma zarazem drugą pozycję poza zasięgiem pomiaru.
Orzecznika narzędnikowego zaimek zwrotny nie ma, a `Parser jest sobą.` mimo to
wychodzi jednoznaczne, bo bierze je `soba`,
więc dopisanie tej pozycji zamieniłoby jedno czytanie na dwa,
a nie odebrałoby odrzucenia.
Wykluczenie lematu idzie przez to przed pozycją, a nie po niej:
po nim widać, ile ta pozycja naprawdę kupuje.

Nie wiadomo, czy `CLOSED_CLASS` ma zostać w kodzie.
Wykluczenie jest zakładem o rejestr, więc domyślność dostarczana z paczką jako
konfiguracja byłaby uczciwsza wobec czytelnika werdyktu: projekt nadpisuje ją
tam, gdzie chce, i widzi ją tak samo jak własną.
Ceną są dwa pliki zamiast jednego,
czyli `znajdź` w `olski/konfiguracja.py` przestający być całą regułą szukania.
Wpis czeka na ten wyżej, bo o cenie rozstrzyga to, czy autor ma już skąd wiedzieć,
co mu się wycina: kiedy ma, druga droga kupuje samo nadpisywanie.

Deklaracji martwej nie pilnuje nic.
Lemat wpisany do `wpuszczane`, po który wykluczenie i tak by nie sięgnęło —
bo słownik nie daje mu czytania nieodmiennego obok klasy zamkniętej —
nie zmienia ani jednego werdyktu i nie zgłasza się,
tak samo jak lemat wpisany do `pomijane`, którego słownik nie zna wcale.
Jest to ta sama klasa, którą po stronie leksykonu łapie świadek
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)),
i tam wpis zły zgłasza się, a tutaj milczy.
Ruchem jest check pytający słownik o lemat przy czytaniu konfiguracji.
Do rozstrzygnięcia jest przedtem cena: `olski/konfiguracja.py` czyta się przy
imporcie i nie żąda dziś Morfeusza w żadnym trybie,
a check ten kazałby żądać go każdemu, kto pyta o samą konfigurację.

Spójnik dzieli się w `olski/subset/słowa.py` na kilka list lematów,
a jak się one mają do siebie, nie mówi ani jedno miejsce.
Listy te odpowiadają na różne pytania o lemat — czy żąda przecinka,
czy bierze człon bez czasownika, czy stoi wewnątrz zdania,
czy powtarza się przed każdym członem, czy otwiera całe zdanie —
więc przecinają się i przecinać się mają: `natomiast` stoi w trzech.
Rozejść, których nikt nie chce, żadna z nich jednak nie widzi,
a kosztują one czytanie nieprawdziwe, którego pomiar różnicowy nie pokazuje:
lemat mający już pozycję podporządkowującą, dopisany do listy koordynacyjnej,
daje drugie wyprowadzenie zdaniu, które i bez niego jest wieloznaczne.
Tak wypadło `czy` z listy skorelowanych
([`docs/konstrukcje-gramatyczne/zdanie-złożone.md`](../docs/konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-skorelowany-powtarza-się-przed-każdym-członem)),
a złapała je ręka, nie przebieg;
`tests/test_zdanie_złożone.py` pilnuje odtąd tej jednej pary.
Ruchem jest check nad wszystkimi parami naraz,
a do rozstrzygnięcia jest jego kryterium:
przecięcie samo w sobie usterką nie jest, więc check musi pytać o coś węższego,
i pierwszym kandydatem jest para, w której jedna lista podporządkowuje,
a druga koordynuje.

Odrzucanie `Ty to jesteś leń.` jest luką pokrycia, a nie usterką nazwy.
`My to jesteśmy szczęściarze.` stoi obok, a `Ty to jest leń.` i `My to szczęściarze.`
wyprowadzają się, więc zatrzymuje tamte dwa osoba kopuli,
a nie zaimek w grupie przed łącznikiem.
Jest to konsekwencja tego, że pozycję podmiotu wiąże grupa za łącznikiem:
`podmiot` i kopula biorą w każdym z tych ciał te same zmienne liczby, rodzaju i osoby,
a grupa przed łącznikiem wchodzi tam bez ani jednej cechy
(`_szyki_zdania_składowego` w `olski/subset/zdanie.py`),
więc zgodności z `ty` nie ma czym postawić.
Ruchem jest wypuszczenie cech w górę z grupy przed łącznikiem, wraz z pomiarem,
i jest to jedyna zmiana, którą pomiar nad bankiem drzew odradza,
bo strona podmiotu obroniła się w nim także w klasie spornej
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim)).
Do przeczytania jest przedtem, czy te zdania są w zakresie:
Składnica jest tekstem pisanym, a należą one do rejestru mówionego,
więc gramatyka celująca w tamten rejestr ma prawo ich nie brać.
Obronę tę osłabia `My to szczęściarze.`, które wyprowadza się dziś:
konstrukcja z dwiema grupami jest w zakresie, a wypada z niego dopiero forma osobowa,
i granicy biegnącej właśnie tędy nie widać czym uzasadnić.
