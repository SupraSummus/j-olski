# Gramatyka i podzbiór

Lista predykatywów nie ma `pora` ani `nie sposób`,
a Składnica ma zdania, które orzekają jednym z tych dwóch:
`Już pora.`, `Pora do łóżka!`, `Pora na nastolatki.`, `Wprost nie sposób!`
oraz `Nie sposób nie żywić uczucia podziwu dla odwagi pierwszych żeglarzy.`
Wszystkie przechodziły, dopóki `pora` czytała się czasownikiem `porać`,
a `sposób` rozkaźnikiem od `sposobić`;
zawężenie ramy do lematów całej formy te czytania zdjęło
([`docs/walencja.md`](../docs/walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
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
([`docs/roadmap.md`](../docs/roadmap.md#czego-brakuje-pod-tym-kryterium)),
a spójnik jest takim samym faktem.
Ruchem jest leksykon spójników czytany przez oba kierunki,
wzorowany na `olski/walencja.py`, i przed nim jedno rozstrzygnięcie:
skład trzyma relację obok szyku, a analiza relacji nie zna,
więc albo leksykon niesie kolumnę, której analiza nie czyta,
albo relacje dochodzą do niego dopiero z kategoriami składu,
których dziś nie ma na warunek ani na przyzwolenie.
Do przeczytania jest `olski/walencja.py` wraz z tym,
co obu kierunkom z leksykonu walencyjnego wyszło różnego
([`docs/walencja.md`](../docs/walencja.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)).

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

Myślnik rozdziela u olskiego dwa zdania i obejmuje parą wtrącenie
([`docs/konstrukcje-gramatyczne/zdanie-złożone.md`](../docs/konstrukcje-gramatyczne/zdanie-złożone.md#para-myślników-obejmuje-wtrącenie-w-środku-zdania-a-nawias-na-jego-końcu)),
a pojedynczo w miejscu pominiętego orzeczenia nie stoi,
choć polszczyzna go tam stawia:
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
Ceną jest to, że znak ten ma dziś dwa ciała — rozdzielające i parę —
więc ciało pojedyncze wewnątrz zdania konkuruje z obydwoma,
a napis z dwoma myślnikami ma wtedy wyprowadzenie także jako para.

Zamknięta lista kopul nie ma `stawać się` ani `okazywać się`,
a polszczyzna orzeka nimi narzędnik tak samo jak `zostawać`.
`Mao stał się na wiele lat przywódcą największego narodu na kuli ziemskiej.`
i `Człowiek staje się wyleniałym tygrysem.` są przez to odrzucone,
i są to dwa z kilkudziesięciu zdań, które zawężenie narzędnika odrzuca nad Składnicą,
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
Ruchem jest cecha odróżniająca głowę biorącą przyłączenie od zaimka,
bo `grupa_imienna → grupa_imienna wyrażenie_przyimkowe` bez takiej cechy
[zmierzono i odrzucono](../docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
Do przeczytania przed taką cechą jest jej cena w czasie rozbioru:
klasa cech rozdziela pozycje lasu (`klasy` w `olski/parse/las.py`),
a wpis o produkcjach formy `bedzie` mierzy, ile kosztuje jedna klasa więcej.
Do przeczytania jest też `_role` w `olski/skład/rozbiór.py`,
bo czyta ono kształty gramatyki po etykiecie,
więc każdy nowy poziom kosztuje tam gałąź.

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
Ruchu tego olski nie bierze, bo czeka on na wpis o zwrotności,
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
z reszty jedna klasa niesie `spotkać się`, czyli lemat spod tamtego wpisu,
a druga zwrotność, której Walenty nie wymienia wcale.
Zakupem jest garść zdań odzyskujących jednoznaczność:
przebieg z klasą domyślną zdjętą wypuszcza dziś pojedyncze zdania z wieloznacznych
do przyjętych, czego przed tamtą pozycją nie robił ani razu.
Zgodność ról przy tym spada, bo bank drzew daje cząstce w takim zdaniu rolę podmiotu
([docs/corpus.md](../docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Kto wpis podnosi, mierzy to na nowo po tamtym wpisie,
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

Wypełnienie ramy wyrażone zdaniem nie stoi przed zdaniem nadrzędnym.
`Dlaczego parser stoi tu świadkiem, rozstrzyga design-notes.md.` jest odrzucone,
`Że cena jest niska, mówi dokument.` tak samo,
a `Dokument mówi, że cena jest niska.` wyprowadza się,
więc brak jest w szyku, a nie w żadnym z tych dwóch zdań podrzędnych.
Miejsca wypełnienia wylicza `grupa_orzeczenia` w `olski/subset/zdanie.py`,
a czasownik stoi w niej przed tym, co bierze, i jedynym ciałem z wypełnieniem
przed czasownikiem jest `grupa_orzeczenia_odwrócona`, które bierze samo dopełnienie.
Ruchem jest ciało z wypełnieniem przed czasownikiem, wraz z przecinkiem po nim,
i wraz z pomiarem: szyk wysunięty mnoży czytania,
bo wypełnień jest pięć i każde weszłoby w to miejsce.
Ciało dopisane do `zdanie_pytajne` samo nie wystarcza i zmierzono to —
nad prozą tego repozytorium nie rusza ani jednego zdania —
bo szyk zdania takiego wypełnienia na czoło nie wpuszcza.
Do przeczytania jest, ile zdań ta proza pisze tym szykiem:
garść zeszła razem z wykluczeniem przysłówka pytajnego
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#pytanie-o-okoliczność-wysuwa-przysłówek-a-zdanie-pod-nim-jest-całe)),
a wszystkie poza jednym są tego kształtu.
Tym jednym jest
`Jest nią to, dlaczego wieloznaczność jest znaleziskiem, a odrzucenie milczeniem.`,
które stawia pytanie za zaimkiem `to`,
czyli za zapowiednikiem, którego ta gramatyka nie ma,
więc wpis ten go nie zamyka.

Pytanie zależne z czołem narzędnikowym albo przyimkowym
ma dwa wyprowadzenia, które różnią się samą rolą `grupa_pytajna`.
`Pyta, czym jest witryna.` wychodzi dwoma odczytaniami
o tych samych formach i tej samej morfologii,
a `--readings` pokazuje w jednym `orzecznik: czym, grupa_pytajna: czym`,
w drugim samo `orzecznik: czym`;
tak samo `Pyta, do czego służy przycisk.` i `Mówi, po co jest ta odpowiedź.`,
gdzie `Czym jest parser?`, `Do czego służy przycisk?` i `Pyta, kim jest autor.`
wychodzą jednym odczytaniem.
Nie jest to wieloznaczność polszczyzny, tylko dwa ciała jednego napisu,
więc werdykt zgłasza znalezisko, którego zdanie nie ma.
Ruchem jest jedno ciało zamiast dwóch, a do przeczytania są ciała czoła
w `olski/subset/podrzędne.py` obok pozycji orzecznika wysuniętego,
z pytaniem, czemu drugie z nich bierze `czym`, a nie bierze `kim`:
`Pyta, kim jest autor.` wychodzi samym `orzecznik: kim`, bez roli `grupa_pytajna`.

Zdanie podrzędne z `że` stoi tylko tuż za czasownikiem, który go żąda.
`Dokument mówi, że cena jest niska.` wyprowadza się,
a `Mówi ono, że cena jest niska.`, `Mówi dokument, że cena jest niska.`
i `Mówi też, że cena jest niska.` stają na `że`,
bo podmiot odłożony za czasownik albo cząstka wchodzą między orzeczenie
i zdanie, które ono bierze.
Tym samym brakiem jest koordynacja dwóch zdań z `że`:
`Mówi, że cena jest niska i że koszt jest wysoki.` staje na drugim `że`.
Dopełnienie między nimi nie przeszkadza:
`requirements.txt mówi jej, że to jest aplikacja Pythona.` wyprowadza się.
Naprawą po stronie autora jest podmiot przed czasownikiem
i cząstka gdzie indziej, czyli szyk, którego reguły prozy nie żądają.
Ruchem jest miejsce na to wypełnienie za podmiotem odłożonym i za cząstką,
i przed nim pomiar, bo `grupa_orzeczenia` w `olski/subset/zdanie.py`
wylicza swoje szyki wprost.
Okolicznik zdaniowy dochodzi do zdania, a nie do orzeczenia,
więc `Rusza ono gramatykę, bo cena jest niska.` wyprowadza się,
a `Rusza też gramatykę, bo cena jest niska.` staje na `bo` tak samo jak tamte:
cząstka za czasownikiem zamyka zdanie przed każdym zdaniem podrzędnym,
a podmiot odłożony tylko przed wypełnieniem.
Do przeczytania są przez to dwa miejsca, szyk wypełnienia zdaniowego
i pozycja cząstki przy orzeczeniu, bo są to dwa braki pod jednym objawem.
