# Walencja

Które dopełnienia czasownik bierze i czego żąda od słowa, które w nich stanie.
Każde z tych rozstrzygnięć orzeka o produkcji, której jeszcze nikt nie napisał,
więc stoi tu, a nie przy konstrukcji, którą akurat obsługuje
([konstrukcje-gramatyczne/](konstrukcje-gramatyczne/README.md)).
Co olski bierze za słowo, mówi [warstwa-leksykalna.md](warstwa-leksykalna.md).
Czym jest ważność i co mówi odrzucenie, wykłada [subset.md](subset.md).

## Walencja jest leksykonem o ramie domyślnej

Czasownik bierze te dopełnienia, których wymaga,
a nie te, które pasują kształtem.
`być` nie bierze dopełnienia w bierniku,
a `On jest wolny.` ma czytanie, w którym bierze:
`wolny` czyta się jako przymiotnik i jako rzeczownik,
a rzeczownikowe staje tam, gdzie produkcja czeka na biernik,
[więc są to dwa odczytania](subset.md#co-się-liczy-jako-jedno-odczytanie).
Takiego czytania nie ma żaden czytelnik tego zdania.

Ramą jest zbiór dopełnień, jakie czasownik bierze,
nazwanych przypadkiem grupy, którą bierze,
wraz z `inf` dla bezokolicznika, bo bezokolicznik przypadka nie ma.
Czasownik wypuszcza ramę z siebie jako cechę,
dopełnienie mówi, którą pozycję ramy zajmuje,
i zgadza je ta sama unifikacja, która zgadza rodzaj z liczbą.
Walencja nie jest więc sprawdzeniem doklejonym do rozbioru, tylko rozbiorem,
dokładnie tak jak [zgodność](subset.md#what-the-grammar-covers).

Leksykon jest otwarty i ma ramę domyślną.
Stoi w nim czasownik, którego rama jest inna niż domyślna —
węższa o biernik albo szersza o przypadek, którego domyślna nie ma
([niżej](#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)) —
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
rozpiętości złotego drzewa nie są porównywalne (`harness/pomiar.py`).
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
(`PREDYKATYWY` w `olski/subset/słowa.py`; co z tym zrobić, notuje `todo/`),
więc odrzucenie mówi o nich prawdę, której `valid` nie mówiło
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).

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

### Zdania leksykonu pochodzą z Walentego i mówią mniej niż on

Wpis pisany ręcznie kosztuje tyle, co rozstrzygnięcie o jednym czasowniku,
a rama ma obowiązywać wszędzie, więc źródłem jest słownik zrobiony po to.
[Walenty](prior-art.md) charakteryzuje 17 224 lematy czasownikowe
64 022 schematami, a obok nich 1 996 lematów rzeczownikowych 14 295 schematami,
i idzie na licencji CC BY-SA 4.0.
Mówi przy tym o czasowniku znacznie więcej, niż którykolwiek z pytających umie żądać,
więc przekład jest zejściem w dół i o każdy z tych faktów pyta osobnym zdaniem.
Zdanie o bierniku jest ujemne i mówi, że czasownik nie bierze dopełnienia w bierniku.
Zdanie o celowniku i zdanie o dopełniaczu są twierdzące i mówią,
że czasownik bierze dopełnienie w tym przypadku
([niżej](#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)).
Zdanie o celowniku przy wypełnieniu jest węższe od tamtego pierwszego i mówi,
że jeden schemat stawia ten celownik obok drugiej pozycji
([niżej](#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).
Zdania o bezokoliczniku są dwa i jedno jest węższe od drugiego, jak przy celowniku:
szersze mówi, że bezokolicznik przy tym czasowniku stoi,
a węższe — że jego wykonawcą jest podmiot tego samego schematu
([wyżej](#walencja-jest-leksykonem-o-ramie-domyślnej) mówi, komu które służy).
Zdanie o zdaniu podrzędnym mówi, że czasownik bierze zdanie wprowadzone przez `że`,
czyli że stoi przy nim to, co ktoś mówi albo wie
([kategorie-zapisu.md](kategorie-zapisu.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi)).
Kierunek zdania o bierniku jest przeciwny niż kierunek pozostałych,
bo przeciwne są domyślności, od których one odejmują:
rama domyślna ma dopełnienie w bierniku, a nie ma ani przypadka poza nim,
ani bezokolicznika, ani zdania podrzędnego.
`harness/walenty.py` jest tym przekładem i wypisuje `olski/leksykon.txt`,
czyli słowa wraz z tym, które z tych zdań są o nich prawdziwe:
zdanie o bierniku niesie 7 941 wpisów, o celowniku 7 964,
o celowniku przy wypełnieniu 4 889, o dopełniaczu 821,
o bezokoliczniku 363, o bezokoliczniku pod kontrolą podmiotu 285,
a o zdaniu podrzędnym 2 498.
Ramy ten plik nie niesie, bo rama składa się dopiero ze zdań, które on mówi.
Nazywają ją dwa moduły, po jednym na kierunek, bo każdy z nich czyta inne zdania:
`olski/subset/rama.py` wypisuje klasy walencyjne razem z domyślną,
od której je odejmuje, a `rama` w `olski/walencja.py` wydaje składowi
zbiór pozycji jednego lematu.
Czyta ten plik `olski/walencja.py`, i czyta dla wszystkich, którzy pytają,
bo rama jest faktem o słowie, a nie o kierunku, w którym się go używa;
wywód trzyma [design-notes.md](design-notes.md#the-round-trip-invariant).

Kolumna przyimków nie jest zdaniem prawda-fałsz, tylko zbiorem:
przyimki, których żąda rama tego słowa, wzięte z pozycji `prepnp` Walentego.
Kolumnę tę plik wypisuje przy czasowniku i przy rzeczowniku,
bo pyta o nią świadek ramowy warstwy rozstrzygającej i pyta po obu stronach
spornego wyrażenia:
rzeczownik wskazuje mu gospodarza, a czasownik wskazanie odbiera
([rozstrzyganie.md](rozstrzyganie.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)).
Gramatyka jej nie czyta i nie ma po co:
wyrażenie przyimkowe przyłącza się u olskiego wszędzie, gdzie polszczyzna je stawia,
a wybór miejsca należy do czytelnika
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).

Kolumna ta niesie coś przy 12 195 wpisach,
a 3 800 z nich weszło do pliku nią samą, bez ani jednego zdania obok.
Rzeczownik wchodzi tak zawsze, bo zdania tego leksykonu są o czasowniku
i o rzeczowniku nie orzekają żadnego,
a czasownik o ramie domyślnej wchodzi wtedy, gdy jego schemat przyimka żąda.

Wspólny jest przy tym plik, a nie każde zdanie, które on mówi.
Biernik, celownik i dopełniacz czytają oba kierunki,
zdanie podrzędne sam skład,
a zdania o bezokoliczniku rozchodzą się na dwa: szersze czyta parser
przy czasowniku zwrotnym, węższe skład,
i nie jest to niezgoda o fakt, tylko różnica w tym, co ten fakt komu kupuje.
Po stronie generatora jest bezokolicznik jedyną obroną przed drzewem,
które żąda go od czasownika, który go nie bierze,
bo bezokolicznik z niczym się nie zgadza i pomyłka nie ma jak wyjść inaczej.

Zdanie o zdaniu podrzędnym zmierzono po tej samej stronie i wyszło z tego to samo.
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
Zdania są przez to dwa, a nie jedno, i różni je właśnie kontrola.
Szersze mówi, że bezokolicznik przy tym czasowniku stoi,
węższe — że wykonawcą jest jego własny podmiot,
i drugie zawiera się w pierwszym tak samo jak celownik przy wypełnieniu
w celowniku ([niżej](#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).

Węższe czyta skład, bo drzewo stawiające bezokolicznik stawia i wykonawcę,
a `Krawiec kazał córce zejść.` mówi, że zeszłaby córka, i tego skład nie zapisze.
Parser czyta szersze i o kontrolę nie pyta:
bierze `córce` za dopełnienie `kazał`, bo celownik stoi obok wypełnienia,
a kto zeszedł, nie pyta ani jedna produkcja.
Zdanie węższe czytane po tej stronie odbierałoby bezokolicznik czasownikom
bezosobowym — `udać się` i `dać się` kontrolowane są z celownika —
więc `Nie udało się ustalić rasy.` przestałoby się wyprowadzać, choć polszczyzną jest.

Czyta je przy tym sama strona zwrotna, a strona zwykła zostaje przy ramie domyślnej,
i to jest wynik pomiaru.
Gramatyka odmawiająca bezokolicznika tym lematom niezwrotnym,
którym odmawia go Walenty, przyjmuje nad Składnicą dwa zdania mniej
i nie kupuje za to ani jednej jednoznaczności.
Po stronie zwrotnej to samo zawężenie kupuje jednoznaczność każdemu zdaniu,
w którym cząstka stoi między formą osobową a bezokolicznikiem
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika)),
bo tam pozycja bezokolicznikowa jest tym, co dokłada odczytanie drugie.
Ta sama pozycja ramy kosztuje więc po jednej stronie, a po drugiej płaci,
i rozdziela je nie lemat, tylko to, czy cząstka przy nim stoi.

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
czyli konstrukcja, [której olski nie ma](subset.md#what-it-does-not-cover-yet).
Liczby tego akapitu bierze się ręcznie nad tym samym bankiem,
tak jak te, o których mówi [corpus.md](corpus.md#fetching-it),
bo `harness/corpus.py` czyta z pola `tfw` dwie role, a nie całą ramę;
co by kosztowało polecenie, trzyma `todo/`.

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
python3 -m harness.walenty walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt \
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
Wpis stoi, [grupa liczebnikowa](konstrukcje-gramatyczne/grupa-imienna.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
też stoi, i zdanie wychodzi jednym czytaniem.
Leksykon kupił tu więc jednoznaczność, a nie pokrycie,
i widać to dopiero z produkcją, której wtedy nie było.

### Zawężenie orzecznika zgodnego wyceniono i decyzji nie ma

Orzecznik zgodny zgadza się z podmiotem — `Plik jest duży.` —
a narzędnikowego żąda kopula.
Stoi on w ramie domyślnej, czyli bierze go każdy czasownik,
a `Trwa akcja protestacyjna.` wychodzi przez to dwoma czytaniami:
drugie z nich orzeka `protestacyjna` o akcji i polszczyzna go nie ma
([disambiguation.md](disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)
nazywa taką parę nadgeneracją).
Pozycję tę Walenty ma i pisze ją `adjp(pred)` kontrolowanym z podmiotu,
więc zawężenie wygląda na wpis w leksykonie.
Miarą jest schemat niezleksykalizowany, tak jak przy celowniku
(`bierze_ramą` w `harness/walenty.py`), oraz kontrola z podmiotu, tak jak przy
bezokoliczniku, bo orzecznik zgodny orzeka o podmiocie i o nikim innym;
w wydaniu z 2016 roku odpowiada temu czterdzieści lematów,
w większości podobnych kopuli.

Cena rozkłada się na trzy rzeczy i rozdziela je dopiero przeczytanie zdań.
Kilka zdań prozy tego repozytorium staje się olskimi, bo ginie im czytanie nieprawdziwe:
`Tor składu je ma` traci to, w którym `je` jest czasownikiem,
`Jedna klasa czytań przyszła` to, w którym czasownikiem jest `Jedna`,
a `Trwa akcja protestacyjna` swój orzecznik.
Przeczytano wszystkie osiem i w żadnym nie zginęło czytanie prawdziwe.
Zdań mniej niż tyle przestaje być olskimi i tam ginie czytanie czytelnika:
`Dziewczyna milknie zakłopotana`, `Grupa przechodzi cała`, `Cena wyszła zerowa`,
`Oba tory pokazują się same` — orzeczenie wtórne przy czasowniku,
którego Walenty na poziomie ramy nie wymienia,
bo wypisuje je tam, gdzie należy ono do zwrotu.
Kilkanaście zdań zmienia rodzaj odmowy, a nie odpowiedź, bo z wieloznacznych
robią się niewyprowadzalne, i te dwanaście rozpadło się przy czytaniu na pół:
w jednych ginie czytanie prawdziwe — `zdanie wraca rozstrzygnięte` —
a w innych olski czytania prawdziwego nie miał wcale,
bo `kosztuje mniej niż ona sama` czyta `sama` orzecznikiem przy `kosztuje`
i innego czytania temu zdaniu nie daje.

Zdań olskich wychodzi przez to po zawężeniu więcej, a nie mniej,
i to jest w tym pomiarze rzecz, której tabela przejść nie pokazuje:
przejście `wieloznaczne → odrzucone` liczy się jako cena
([`harness/ruch.py`](../harness/ruch.py) wywodzi, czemu),
a zdaniem olskim nie było ani przed nim, ani po nim.
Wycena nie rozstrzyga zatem tej pozycji i rozstrzygnąć jej nie może sama,
bo waży dwie rzeczy w różnych walutach:
zdanie zwyczajnej polszczyzny, które przestaje się wyprowadzać,
i zdanie, które staje się olskim.
Do przeczytania jest przedtem liczba nad Składnicą, której ten pomiar nie ma,
bo populacja stąd jest tej wielkości, że czterema zdaniami przewraca wniosek.

Tańsze od tego wyboru jest kryterium po stronie przymiotnika.
Czytania, które zawężenie miało zdjąć, różni przymiotnik, a nie czasownik:
`protestacyjna` orzekać nie może, a `zerowa` i `wypisany` mogą,
więc kryterium postawione tam zdejmuje czytania nieprawdziwe,
nie zabierając ani jednego orzeczenia wtórnego.
Różnica ta jest własnością przymiotnika odrzeczownikowego,
której tagset nie niesie, więc `niesie` po nią nie sięga
([kanał cech](parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)),
a rejestr techniczny pisze takie przymiotniki gęsto:
`plik konfiguracyjny`, `leksykon walencyjny`.
Kryterium takie mógłby dać katalog przymiotnikowy Walentego,
którego przekład nie czyta, bo nikt o niego nie pytał.

### Leksykon licencjonuje dopełnienie w celowniku i w dopełniaczu

Rama domyślna ma dopełnienie w bierniku i nie ma dopełnienia w przypadku innym,
a czasownik, któremu Walenty daje pozycję celownikową albo dopełniaczową,
dostaje ją wpisem w leksykonie.

```sh
python3 -m olski.check --readings --zatrzymania -c "Werdykt służy czytelnikowi.
Parser wyprowadza czytelnikowi.
Wpis żąda dowodu.
Sonda mierzy dowodu."
```

```text
<text>: Werdykt służy czytelnikowi.
        - podmiot: Werdykt, dopełnienie: czytelnikowi, orzeczenie: służy
<text>: Parser wyprowadza czytelnikowi.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
<text>: Wpis żąda dowodu.
        - podmiot: Wpis, dopełnienie: dowodu, orzeczenie: żąda
<text>: Sonda mierzy dowodu.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
```

Rozdziela te pary leksykon, a nie przypadek:
`służyć` i `żądać` mają w Walentym tę pozycję, a `wyprowadzać` i `mierzyć` nie mają.
Zdanie tego nie orzeka o samym przypadku przy czasowniku,
bo celownik stoi w polszczyźnie i przy czasowniku, który go w ramie nie ma:
`Kompilator wyprowadza psa agentowi.` jest polszczyzną i jest odrzucone
([niżej](#wolny-celownik-nie-jest-pozycją-ramy-i-nie-wchodzi-leksykonem)).
Zajmują przy tym tę samą pozycję ramy, co dopełnienie w bierniku,
a różni te produkcje sam przypadek grupy, która tę pozycję wypełnia,
tak samo jak różni je [dopełniacz negacji](konstrukcje-gramatyczne/orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem).

Przeczenie tych dwóch pozycji nie rusza i ruszać nie ma czego:
dopełniacz negacji wchodzi w miejsce biernika i tam kończy się jego zasięg,
a `nie służy czytelnikowi` stoi w celowniku tak samo jak `służy czytelnikowi`.
Tam, gdzie czasownik bierze dopełniacz z obu powodów naraz,
jeden napis wyprowadza się dwa razy,
a `Wpis nie żąda dowodu.` wychodzi jednym czytaniem,
bo kształt obu wyprowadzeń jest ten sam
([subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie)).

Drugiego dopełnienia obok pierwszego ta pozycja nie daje;
daje je [pozycja niżej](#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)
i wpuszcza ją osobne zdanie leksykonu.
Wyrażenia przyimkowego to nie dotyczy, bo ono jest okolicznikiem:
`Parser mówi autorowi o czytaniach.` wyprowadza się i wychodzi wieloznaczne,
bo [olski nie wybiera przyłączenia](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).

Zdanie leksykonu jest tu twierdzące, a zdanie o bierniku ujemne,
i ta różnica rozstrzyga o tym, których schematów Walentego wolno się pytać.
Zdanie ujemne odejmuje od ramy domyślnej,
więc kształt policzony za szeroko zostawia lemat przy tej ramie i nic o nim nie mówi.
Zdanie twierdzące ramę poszerza, więc ta sama pomyłka wpuszcza dopełnienie tam,
gdzie polszczyzna go przy tym czasowniku nie stawia.
Odpadają przez to dwa rodzaje schematu.
Schemat z pozycją zleksykalizowaną jest zwrotem,
a pozycja stojąca w nim obok należy do zwrotu, a nie do lematu:
celownik ma w Walentym `mieć` i ma go ze zwrotu `mieć komuś za złe`,
a policzony osobno daje `Ludzie mają rozum i sumienie.` drugie czytanie,
w którym `Ludzie` jest celownikiem od `Luda`, a ciąg współrzędny stoi w podmiocie.
Schemat spoza `BRANE` w `harness/walenty.py` nazywa zaś polszczyznę,
której ten rejestr nie pisze,
i odpada z tego samego powodu, z którego odpada w kolumnie przyimków.

#### Wolny celownik nie jest pozycją ramy i nie wchodzi leksykonem

Celownik posiadacza i tego, komu się przysłuży — `wyprowadzić komuś psa`,
`ściągnąć komuś czapkę`, `wykryć komuś raka` — nie jest pozycją, której czasownik żąda,
tylko członem dochodzącym do całego orzeczenia,
więc Walenty go nie wypisuje i wypisać nie może: stoi on przy czasowniku dowolnym
([disambiguation.md](disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma)
liczy, ile takich celowników łapie kryterium pisane pod inną pozycję).
Leksykon nie ma więc czym go wpuścić, a wpis zmyślony wpuszczałby przy jednym lemacie
to, co polszczyzna ma przy każdym.

Odrzucenie pada tu przy tym dwa razy, a nie raz.
`Kompilator wyprowadza psa agentowi.` nie ma czytania także wtedy,
gdy się celownik temu lematowi dopisze, bo dopełnienie stoi tam obok dopełnienia
([subset.md](subset.md#what-it-does-not-cover-yet)),
a wolny celownik dochodzi zawsze do orzeczenia, które ma już swoje wypełnienie.
Ruchem jest przez to pozycja okolicznika, a nie pozycja ramy,
i tym różni się ona od dwóch wpuszczonych wyżej:
okolicznik dochodzi wszędzie, więc taka pozycja bierze każdą formę czytaną celownikiem,
a te dzielą kształt z miejscownikiem w całej odmianie żeńskiej.
Ceny tego nikt nie policzył; `todo/` trzyma ten przebieg.

Cena i zakup są zmierzone nad Składnicą 180723 sondą różnicową,
która zdejmuje produkcję dopełnienia w jednym przypadku,
i wypadają po obu stronach morfologii inaczej.
Pod złotą morfologią celownik nie odbiera jednoznaczności ani jednemu zdaniu,
a daje ją kilkudziesięciu, które przedtem nie miały żadnego czytania.
Dopełniacz jednoznaczność odbiera, a daje ją przeszło dwa razy większej liczbie zdań,
niż tamtych odbiera.
Role zdań nowo przyjętych zgadzają się przy tym z drzewem wzorcowym
w przeszło czterech piątych, a odwrócone nie jest ani jedno,
czyli zdania te przychodzą z czytaniem, które ma czytelnik
([corpus.md](corpus.md#what-morphological-ambiguity-costs) mówi, ile waży odwrotne).
Pod Morfeuszem obie pozycje kosztują więcej, bo forma ma tam kilka czytań naraz,
i ruch idzie tam głównie z odrzuconych do wieloznacznych:
przyjętych przybywa kilkadziesiąt, a odrzuconych ubywa przeszło dwieście.
Obie pozycje ruszają przy tym te same kilkanaście zdań,
a zdania, o którym razem mówiłyby co innego niż każda z osobna, nie ma ani jednego.

Nad prozą tego repozytorium ta sama sonda liczby przyjętych prawie nie rusza,
choć kilkudziesięciu zdaniom zmienia werdykt,
i nie jest to sprzeczność z liczbami wyżej, tylko
[zasłanianie](pisanie-po-olsku.md#zasłanianie-działa-w-obie-strony):
zdanie o dwudziestu wyrazach ma kilka zatrzymań naraz,
więc pozycja zdejmuje jedno z nich i zostawia zdanie odrzucone, tylko dalej.
Widać ją za to nad zdaniem krótkim.

### Druga pozycja ramy jest celownikiem obok wypełnienia

`Parser pokazuje autorowi oba czytania.`, `Parser mówi autorowi, że zdanie czyta się dwojako.`
Celownik stoi tu obok wypełnienia, które pozycję ramy zajmuje, a nie w niej samej,
i tym różni się od [dopełnienia w celowniku](#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu),
które tę pozycję wypełnia samo.
Pozycja ta jest przez to faktem o wpisie leksykonu, a nie konstrukcją obok innych,
i dlatego stoi tutaj, a nie w
[konstrukcjach](konstrukcje-gramatyczne/README.md): licencji udziela jej schemat Walentego,
a nie ciało napisane ręką.

```sh
python3 -m olski.check --readings --zatrzymania -c "Parser pokazuje autorowi oba czytania.
Parser pokazuje oba czytania autorowi.
Reguła pomaga autorowi oba czytania.
Parser pokazuje autorowi autorowi."
```

```text
<text>: Parser pokazuje autorowi oba czytania.
        - podmiot: Parser, dopełnienie: autorowi + oba czytania, orzeczenie: pokazuje
<text>: Parser pokazuje oba czytania autorowi.
        - podmiot: Parser, dopełnienie: oba czytania + autorowi, orzeczenie: pokazuje
<text>: Reguła pomaga autorowi oba czytania.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
<text>: Parser pokazuje autorowi autorowi.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
```

Parę wpuszcza własne zdanie leksykonu, a nie koniunkcja dwóch tamtych,
i liczy się je z jednego schematu Walentego.
Celownik z jednego schematu i biernik z drugiego pary nie dowodzą:
takich lematów jest 641, i to one dzielą `pomagać` od `pokazywać`.
Sąsiadem musi być przy tym wypełnienie, które olski ma —
dopełnienie w bierniku, bezokolicznik, zdanie podrzędne albo pytanie zależne —
bo celownik obok wyrażenia przyimkowego pary nie potrzebuje:
`mówić komuś o czymś` wychodzi okolicznikiem, który przyłącza się za darmo.
Liczony szerzej dawałby parę 2 434 lematom, które poza takim sąsiadem żadnego nie mają.

Licencję niesie cecha, a nie druga pozycja wypisana w ramie.
Ramę unifikacja przecina, więc dwie pozycje wypisane w niej byłyby alternatywą,
a żądanie jest tu koniunkcją: celownik razem z wypełnieniem, nie jedno albo drugie.
Cecha licencjonuje przez to sam celownik, a wypełnienie licencjonuje rama obok niej.

Który sąsiad przy nim stoi, zdanie leksykonu przemilcza,
i jest to ta sama zgrubność, którą ma sama rama domyślna:
skoro daje ona każdemu czasownikowi biernik, bezokolicznik, zdanie i pytanie naraz,
para rozdzielona na cztery zdania byłaby dokładniejsza od tego, do czego dochodzi.
Walenty daje celownik przy bierniku 4 611 lematom, przy zdaniu 666,
przy pytaniu 360, a przy bezokoliczniku 91.
Dopełniacza ta pozycja nie bierze, bo przy wypełnieniu daje go Walenty
kilkudziesięciu lematom, a celownik kilku tysiącom.

Cena i zakup są zmierzone nad Składnicą 180723 przebiegiem przed zmianą i po niej.
Pod złotą morfologią czytanie dostaje przeszło sto zdań, które przedtem nie miały żadnego,
a jednoznaczności nie traci ani jedno zdanie przyjęte;
czytań przybywa pojedynczym zdaniom już wieloznacznym.
Zgodność ról z drzewem wzorcowym spada o niecały punkt
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Pod Morfeuszem czytanie dostaje tyle samo zdań, a cena jest widoczna:
jednoznaczność traci kilkadziesiąt zdań przyjętych,
bo celownik dzieli formę z miejscownikiem w całej odmianie żeńskiej,
więc każde `w gramatyce` za czasownikiem z parą czyta się także jej celownikiem.
Część tych zdań na tym zyskuje, a nie traci:
`Pokazują go swoim gościom.` ma jedno czytanie i jest nim czytanie czytelnika,
bo biernik i celownik dochodzą tam do czasownika dopiero razem.

Okolicznik staje między członami pary, bo ten rejestr tak pisze —
`pokazuje autorowi w wydruku oba czytania` —
i miejsce to zmierzono osobno: kupuje kilka zdań, a jednoznaczność odbiera pojedynczemu.
Bez niego wyrażenie przyimkowe w tym miejscu ma jednego gospodarza zamiast dwóch,
czyli gramatyka wybierałaby przez przeoczenie
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).

Werdykt nazywa oba dopełnienia, rozdzielając je plusem,
bo rola o dwóch wypełnieniach czytałaby się jak dwie role:

```sh
python3 -m olski.check --readings -c "Parser pokazuje autorowi oba czytania."
```

```text
<text>: Parser pokazuje autorowi oba czytania.
        - podmiot: Parser, dopełnienie: autorowi + oba czytania, orzeczenie: pokazuje
```

## Żądanie pozycji jest osobnym plikiem, a nie kolumną leksykonu

Leksykon mówi, co czasownik bierze, a nie mówi, czego od tego żąda.
`zażądać` bierze dopełnienie w dopełniaczu,
a w podmiocie żąda człowieka,
i to drugie zdanie stoi w wydaniu TEI Walentego:
rama nazywa tam pozycję rolą i żąda od niej klasy rzeczy,
a wydanie tekstowe, z którego powstaje leksykon, tej warstwy nie niesie
([prior-art.md](prior-art.md#polish-language-resources)).
Wychodzi ono z tamtego wydania osobnym plikiem — `olski/żądania.txt` —
a nie kolumną leksykonu.

Rozstrzyga o tym to, kto który plik czyta.
Leksykon czyta gramatyka przy imporcie i bez niego nie startuje,
a żądania nie czyta ani jedna produkcja: czyta je werdykt, i to na żądanie flagi
([niżej](#werdykt-nazywa-żądanie-obsadzonej-pozycji)).
Kolumna dokładałaby przez to megabajt do pliku, od którego zależy start,
a czytałby ten megabajt ktoś, kogo na tej drodze nie ma.
Wiersz leksykonu przestałby też być zdaniem o jednym słowie:
żądanie mówi o pozycji, a jedno słowo obsadza ich kilka,
więc wiersz jest tu jeden na rolę w pozycji, a nie jeden na słowo.
Do paczki plik wchodzi tak samo jak leksykon,
bo `pyproject.toml` wpuszcza tam dane, które czyta kod paczki.

Kolumn jest pięć i mówią, czego czasownik żąda od słowa w swojej pozycji:
lemat, klasa słowa, pozycja, rola tej pozycji oraz klasy rzeczy, których żąda.
Pozycje noszą nazwy olskiego tam, gdzie olski je ma,
a `subj` i `prepnp(od)` nazwy Walentego, bo pozycji podmiotu ani przyimkowej
olski w ramie nie ma.
Klasy zbierają się po wszystkich ramach lematu, więc kolumna jest alternatywą:
`ALL` obok klasy nazwanej znaczy, że w jednym znaczeniu pozycja nie żąda niczego.

Czytanie jest złączeniem trzech warstw, a nie odczytaniem wiersza,
i tym jest droższe od przekładu obok:
argument niesie rolę wraz z żądaniem, pozycja wraz z frazą stoi w warstwie
składniowej, a wiąże je trzecia warstwa, po jednym spięciu na parę.
Co to czytanie bierze, a czego nie, mówi `harness/żądania.py`.
Wydanie TEI waży rozpakowane kilkaset megabajtów
i nie stoi w repozytorium, tak samo jak wydanie tekstowe i bank drzew:

```sh
curl -L -o walenty-tei.zip \
  'http://zil.ipipan.waw.pl/Walenty?action=AttachFile&do=get&target=walenty_20160418-TEI.zip'
unzip walenty-tei.zip
python3 -m harness.żądania walenty_20160418-TEI/walenty_20160418.xml > olski/żądania.txt
```

Wpis wyprowadzony z Walentego jest utworem zależnym od niego,
więc `olski/żądania.txt` niesie w nagłówku atrybucję i tę samą licencję,
tak samo jak leksykon.

### Przekład ma pozycje ramy, a okolicznika nie ma

Pozycję dostaje w tym pliku podmiot, dopełnienie w trzech przypadkach,
bezokolicznik, zdanie podrzędne, pytanie zależne i wyrażenie przyimkowe.
Poza plikiem zostaje argument narzędnikowy, bo `inst` jest u olskiego pozycją
orzecznika i jest to ten sam brak, który ma
[leksykon](#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on),
oraz zdanie pod zaimkiem i pozycja zleksykalizowana, których olski nie ma czym wypisać.

Największym brakiem jest okolicznik.
Walenty pisze go osobnym kształtem — `xp(locat)` jest okolicznikiem miejsca —
a olski nie ma takiej pozycji ramy,
bo wyrażenie przyimkowe przyłącza się u niego wszędzie, gdzie polszczyzna je stawia,
więc żądanie doszłoby do zdania tylko przez przyimek.
Tego przyimka ten kształt nie nazywa:
nazywa go dopiero tabela rozwinięć z tego samego wydania,
gdzie jedna pozycja miejsca rozwija się w trzydzieści przyimków,
czyli w trzydzieści wierszy mówiących jedno.
Klasy `MIEJSCE` żąda przy tym w większości właśnie pozycja okolicznikowa,
więc żądanie przestrzeni fizycznej zostaje poza tym plikiem,
a razem z nim przykład z celu o [żądaniu czasownika](roadmap.md#cele).
Ten przykład i tak by w nim nie stanął:
`stać` jest jednym z czasowników, którym Walenty ramy nie daje wcale
([prior-art.md](prior-art.md#polish-language-resources)),
więc żądanie przestrzeni fizycznej trzeba by wziąć skądinąd.

Druga połowa celu nie jest przy tym w tym pliku i nie może być.
Więcej niż co czwarty wiersz żąda klasy, której ten plik nie umie nazwać,
bo Walenty pisze ją zbiorem synsetów plWordNetu, a nie klasą nazwaną;
takie żądanie wychodzi znacznikiem, żeby zbiór klas nie kłamał milczeniem.
Czy słowo stojące w zdaniu do klasy należy, orzeka wordnet,
którego to repozytorium nie ma,
i jest to pytanie do świata
([open-questions.md](open-questions.md#shared-questions)).

### Werdykt nazywa żądanie obsadzonej pozycji

Werdykt mówi, czego czasownik żąda od tego, co w jego pozycji stanęło,
i mówi to pod flagą, obok streszczenia czytania:

```sh
python3 -m olski.check --readings --żądania -c "Autor doradza czytelnikowi poprawkę."
python3 -m olski.check --żądania -c "Program zażądał raportu."
```

```text
<text>: Autor doradza czytelnikowi poprawkę.
        - podmiot: Autor, dopełnienie: czytelnikowi + poprawkę, orzeczenie: doradza
        podmiot „Autor”: „doradza” żąda klasy PODMIOTY
        dopełnienie „czytelnikowi”: „doradza” żąda klasy LUDZIE
        dopełnienie „poprawkę”: „doradza” żąda klasy KOMUNIKAT albo SYTUACJA albo WYTWÓR
<text>: Program zażądał raportu.
        podmiot „Program”: „zażądał” żąda klasy LUDZIE albo klasy, której olski nie nazywa
        dopełnienie „raportu”: „zażądał” żąda klasy CZYNNOŚĆ albo OBIEKTY
```

Werdykt nazywa żądanie i nie pyta, czy słowo w pozycji je spełnia.
Drugie zdanie wydruku pokazuje, ile to zostawia autorowi i ile mu zabiera:
`zażądać` żąda w podmiocie ludzi, a stoi tam program,
więc czytelnik tego wiersza widzi, czego czasownik chciał,
i sam rozstrzyga, czy metafora jest tu na miejscu.
Rozstrzygnąć to za niego mógłby wordnet, którego to repozytorium nie ma
([open-questions.md](open-questions.md#shared-questions)),
a w tym zdaniu i on jest potrzebny, bo `zażądać` żąda ludzi albo klasy,
której olski nie nazywa; żądanie samych klas osobowych rozstrzyga bez niego
deklaracja projektu ([niżej](#deklaracja-projektu-rozstrzyga-żądanie-osoby)).
Wiersz idzie przez to pod flagą, a nie w samym werdykcie:
nie jest znaleziskiem, tylko materiałem do przeczytania
([subset.md](subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego)).

Adresatem tego wiersza jest reguła o frazie urzędowej bez wykonawcy,
a nie ta o czasowniku domowym.
Czasownikowi domowemu tamta reguła każe podstawić czasownik dokładny,
a `stać`, `trzymać`, `brać` i `nieść` nie mają w Walentym ramy semantycznej wcale,
więc test podstawieniowy zostaje przy człowieku.
Regule sąsiedniej wiersz ma za to co powiedzieć:
`kupować` żąda w podmiocie ludzi albo podmiotów, a `rozstrzygać` bierze tam
i komunikat, więc „leksykon kupuje jednoznaczność” dostaje świadka,
a „dokument rozstrzyga” nie.

Wiersz jest jeden na obsadzoną pozycję, a nie jeden na rolę:
`dopełnienie` nie mówi, w którym przypadku stoi,
a `Autor doradza czytelnikowi poprawkę.` obsadza nim celownik i biernik naraz,
i czasownik żąda od nich czego innego.
Pozycję nazywa więc przypadek wypełnienia, a pod przeczeniem dwa naraz,
bo dopełnienie w bierniku staje tam w dopełniaczu.
Fraza bezokolicznikowa zostaje przy tym cała poza wierszem:
`dokument` w `Autor zamierzył edytować dokument.` obsadza pozycję `edytować`,
a nie tego czasownika, przy którym stoi podmiot,
więc wiersz o nim mówiłby o żądaniu cudzej ramy.

Milczenie jest odpowiedzią częstą, a kryterium trzyma `olski/żądania.py`.
Nad prozą tego repozytorium wiersz dostaje kilka procent zdań
i bierze się to głównie z zasięgu samego pliku:
`mówić`, `stać`, `brać`, `czytać` i `mieć` nie mają w tym wydaniu ramy żadnej,
a to nimi ten rejestr orzeka najczęściej.
Alternatywa nienazwana zostaje za to w wierszu — `zażądał` wyżej ma ją obok
klasy `LUDZIE` — bo wiersz o samych ludziach byłby żądaniem ostrzejszym,
niż Walenty stawia.

### Deklaracja projektu rozstrzyga żądanie osoby

Wiersz wyżej nazywa żądanie i na tym staje,
bo o przynależności do klasy orzeka wordnet.
Klasy osobowe są tą częścią pytania, która wordnetu nie żąda:
kto w rejestrze jest kimś, a co jest rzeczą, wie autor rejestru.
Mówi to sekcją `osoby` w `olski.toml`, czyli tam, gdzie mówi już,
wedle którego leksemu odmienia się słowo, którego słownik nie ma
([warstwa-leksykalna.md](warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)).
Flaga wypisuje wtedy pozycje, w których czasownik żąda kogoś, a stoi w nich rzecz.

```sh
python3 -m olski.check --osoby -c "Autor doradza czytelnikowi poprawkę.
Sonda drukuje liczby."
```

```text
<text>: Sonda drukuje liczby.
        podmiot „Sonda”: „drukuje” żąda klasy PODMIOTY, a „sonda” nikogo nie nazywa
zdań: 2; wieloznaczne: 0; bez odczytania: 0
```

Zdanie pierwsze milczy całe, bo `autor` i `czytelnik` stoją w deklaracji tego
projektu, a żądanie od obu tych pozycji wypisuje sekcja wyżej.
Osobą jest tu ten, kogo Walenty żąda klasami `LUDZIE`, `ISTOTY` i `PODMIOTY`,
czyli i człowiek, i zwierzę, i organ, który działa jak człowiek,
więc wiersz mówi, że słowo nikogo nie nazywa, a nie że nie jest człowiekiem.
Trzy klasy razem, bo pytanie deklaracji jest jedno,
a rozdzielenie ich żądałoby taksonomii, czyli znów wordnetu.
Zasięg tego pytania jest przy tym większy niż trzy klasy z dwudziestu:
6 525 wierszy o podmiocie z 10 558 nie żąda w tym pliku niczego poza kimś,
a w celowniku 1 282 z 1 821.

Alternatywa nienazwana znosi żądanie osoby w całości
i tym odpowiedź jest węższa od wiersza materiału:
`zażądać` żąda w podmiocie ludzi albo zbioru synsetów,
więc rzecz stojąca tam spełnia żądanie w tym drugim znaczeniu.
Nad prozą tego repozytorium zawężenie to odejmuje blisko połowę pozycji,
w których żądanie jest osobowe.
Wiersz jest przy tym o zdaniu, a nie o odczytaniu.
Pozycję obsadza czytanie, więc wiersz mówi, że w którymś z nich stoi rzecz tam,
gdzie czasownik żąda kogoś.
Wykaz na odczytanie kazałby przeczytać kilkanaście kopii jednego wiersza,
bo tyle czytań miewa zdanie wieloznaczne.

Deklaracja jest zamknięta: lemat spoza niej nikogo nie nazywa.
Kierunek odwrotny, czyli deklaracja rzeczy, jest kampanią bez końca,
bo rzeczowników rejestr niesie tysiące, a osób garść,
i myli się po cichu, bo słowo niezadeklarowane zostawia warstwę milczącą,
a milczenia nikt nie czyta.
Zamknięta myli się widocznie: osoba, której nikt nie zadeklarował, dostaje wiersz,
a wiersz poprawia się jednym wpisem.
Projekt bez tej sekcji nie ma nikogo,
więc wykaz wraca u niego do materiału zawężonego do klas osobowych.

Adresatem tego wykazu jest reguła o frazie urzędowej bez wykonawcy
i przegląd, który ją zadaje.
Nad prozą tego repozytorium `--żądania` wypisuje przeszło dwa tysiące wierszy,
a `--osoby` przeszło sto, nad sześćdziesięcioma zdaniami, i tyle czyta się ręką.
Znaleziskiem wiersz nie jest i być nie może, bo ta sama reguła zostawia
metonimię zwykłą wprost — `dokument mówi` i `reguła żąda` są w niej polszczyzną —
a wykreśla dopiero to, co rzeczy przypisuje wolę albo doznanie.
Tego rozróżnienia nie niesie żadna klasa Walentego,
więc rozstrzyga je czytelnik, a olski podaje mu miejsca do przeczytania.
