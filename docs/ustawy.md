# Ustawy

Ustawa opisuje mechanikę państwa,
a pisze się ją pod regułami, które same są prawem:
„Zasady techniki prawodawczej” żądają od zdania w ustawie
w przybliżeniu tego, czego olski żąda od zdania w dokumentacji.
Rejestr, który to żądanie stawia sam sobie,
warto zmierzyć nawet wtedy, gdy olski pod niego nie powstał:
pomiar mówi wtedy coś o gramatyce, a nie tylko o rejestrze.

Mówi to, że regularność ustawy nie stoi w zdaniu.
Nad siedmioma ustawami gramatyka wyprowadza jednoznacznie przeszło setkę zdań
z blisko pięciu tysięcy, a wieloznacznych jest kilka razy więcej,
więc zdanie ustawy, które olski w ogóle czyta,
czyta on najczęściej na kilka sposobów.
Nad [Składnicą](corpus.md#the-measurement) wychodzi odwrotnie —
tam zdanie czytane w ogóle czyta się najczęściej na jeden sposób —
choć tamten bank drzew jest zbudowany z gazet i prozy.
Regularne w ustawie jest drzewo jednostek redakcyjnych,
a zdanie jest w niej długie i podrzędnie złożone,
czyli takie, jakiego olski nie ma.

## Rejestr ma własne reguły, a te reguły nie mają miary

„Zasady techniki prawodawczej” są załącznikiem do rozporządzenia
Prezesa Rady Ministrów z dnia 20 czerwca 2002 r.,
więc nie są poradnikiem, tylko obowiązują.
Trzy przepisy z nich mówią o tym samym, o czym jest to repozytorium:

- § 5: „Przepisy ustawy redaguje się zwięźle i syntetycznie,
  unikając nadmiernej szczegółowości […]”
- § 6: „Przepisy ustawy redaguje się tak, aby dokładnie i w sposób zrozumiały
  dla adresatów zawartych w nich norm wyrażały intencje prawodawcy.”
- § 7: „Zdania w ustawie redaguje się zgodnie z powszechnie przyjętymi regułami
  składni języka polskiego, unikając zdań wielokrotnie złożonych.”

§ 7 jest żądaniem podzbioru postawionym przez wykluczenie,
czyli tak, jak [wyznaczał go linter](linter.md#this-is-the-same-subset-approached-from-behind):
składnia polska wolna, a jedna konstrukcja zabroniona.
§ 6 jest kryterium jednoznaczności:
zrozumiały dla adresata jest przepis, który czyta się jednym sposobem,
i to samo mówi olski, gdy każe zdaniu mieć dokładnie jedno czytanie.
§ 55 ust. 2 żąda przy tym, żeby artykuł był w miarę możliwości jednozdaniowy,
czyli żeby jednostce redakcyjnej wystarczyło jedno zdanie.

Korekta żadnego z tych trzech nie mierzy.
Wielokrotne złożenie zdania jest własnością zdania, a nie znakiem w nim,
a jednoznaczność jest własnością wyprowadzenia,
więc spór o nią rozstrzyga sąd, czyli po uchwaleniu i po jednej sprawie naraz.
Inwentarz kandydatów na reguły tego rejestru nie obejmuje,
tak samo jak nie obejmuje prozy literackiej,
a to, co dla tego rejestru dałoby się mierzyć, zostaje niżej.

## Skąd bierze się korpus

API ELI Sejmu oddaje tekst aktu w HTML-u pod adresem ELI,
czyli pod rocznikiem i pozycją Dziennika Ustaw:

```sh
mkdir -p ustawy
for eli in 1990/95 1999/688 2001/1198 2011/112 2014/1195 2015/1485 2024/1907; do
  curl -sS -o "ustawy/DU-$(echo "$eli" | tr / -).html" \
    "https://api.sejm.gov.pl/eli/acts/DU/$eli/text.html"
done
```

Korpus mówi o sobie [pięć rzeczy](corpora.md#what-a-corpus-has-to-say-about-itself),
a akt normatywny odpowiada na każdą z nich,
i na licencję, rejestr oraz etap produkcji odpowiada tak,
jak żaden korpus tamtego przeglądu odpowiedzieć nie mógł.

**Licencja.** Żadna, w najlepszym sensie:
art. 4 pkt 1 ustawy o prawie autorskim i prawach pokrewnych
wyłącza akty normatywne z przedmiotu prawa autorskiego,
więc nie ma czego redystrybuować ani na co się zgadzać.

**Rozmiar.** Siedem ustaw wyżej to 104 062 słowa i 4921 zdań,
co starcza na czytanie trafień, a nie na rozkład.
Rozkład jest tu jednak kwestią pobrania, a nie dostępności:

```sh
curl -sS "https://api.sejm.gov.pl/eli/acts/DU/2024" | grep -o '"type":"Ustawa"' | wc -l
```

Rocznik 2024 ma 115 ustaw i API oddaje w HTML-u każdą z nich.

**Rejestr.** Jeden i zadeklarowany:
tekst pisany pod „Zasadami techniki prawodawczej”, a nie pod niczyim gustem.

**Pochodzenie.** Polszczyzna napisana po polsku,
z jednym zastrzeżeniem, którego ten pomiar nie sprawdzał:
dyrektywa transponowana jest tłumaczeniem,
a ustawa, która ją wdraża, może nieść jego składnię.
Ustawy wyżej stoją od 1990 do 2024 roku, więc rocznik nie jest tu zmienną ukrytą.

**Etap produkcji.** Trzeci, którego tamten przegląd nie ma:
tekst po redakcji i po korekcie, ogłoszony,
i przy tym nietknięty od ogłoszenia, bo zmienia go dopiero nowelizacja z własną pozycją.
Adres ELI jest przez to mocniejszym przypięciem niż commit:
akt pod nim nie może się już zmienić.
Zmienić się może HTML, w którym wydawca go podaje,
i to jest jedyne, co pod tym pomiarem może się ruszyć bez naszego udziału.

Adresy wyżej wskazują ustawy w brzmieniu ogłoszonym, a nie ujednoliconym,
bo tekst jednolity jest załącznikiem do obwieszczenia
i jego HTML niesie obwieszczenie razem z aktem.
Ustawa o samorządzie gminnym stoi tu więc taka, jaka była w 1990 roku,
i o taką, jaka jest dzisiaj, ten pomiar nie pyta.

Osobno stoją same „Zasady techniki prawodawczej”,
bo są rozporządzeniem, a nie ustawą, i o nich jest ten dokument w drugą stronę:

```sh
mkdir -p ztp
curl -sS -o ztp/DU-2016-283.html "https://api.sejm.gov.pl/eli/acts/DU/2016/283/text.html"
```

Jest to tekst jednolity z 2016 roku, czyli ostatni, który API oddaje w HTML-u;
nowszy jest ogłoszony w PDF-ie i tej ekstrakcji nie dotyczy.

## Ustawa dochodzi do gramatyki jako drzewo, nie jako tekst

Tekst jednostki redakcyjnej najczęściej nie jest zdaniem:

```text
Art. 1. Ustawa określa:
  1) zadania ochrony ludności i obrony cywilnej;
  2) organy i podmioty realizujące zadania ochrony ludności i obrony cywilnej;
```

Zdaniem jest gałąź: przesłanka złożona z każdą pozycją po kolei.
Więc `harness/ustawy.py` składa drzewo w zdania,
a nie przepisuje tekst jednostka po jednostce,
i wyliczenie o siedmiu pozycjach daje siedem zdań.
Zszywa tylko punkt i literę, bo tylko wyliczenie dzieli przesłankę między pozycje;
artykuł i ustęp stoją same.

```sh
python3 -m harness.ustawy ustawy/ --into proza/ustawy
python3 -m harness.ustawy ztp/ --into proza/ztp
```

Ten krok zmyśla trzy rzeczy, dwie zabiera,
a jedną zabrał wydawca przed nim,
i tyle razem kosztuje czytanie ustawy zdaniami.

**Zdanie, którego nikt nie napisał.**
`Ustawa określa zadania ochrony ludności i obrony cywilnej.`
stoi w ustawie w dwóch jednostkach i pod dwoma numerami.
Werdykt gramatyki dotyczy tego złożenia, a nie zapisu,
i jest to jedyna forma, w której treść ustawy jest zdaniami w ogóle.

**Przesłanka powielona.**
Wychodzi raz na pozycję, więc częstość liczona nad tą prozą liczyłaby ją wielokrotnie.
Dlatego korpus idzie pod gramatykę, która pyta o zdanie po zdaniu.

**Kropka dopisana.**
Gałąź kończy się średnikiem albo przecinkiem, a zdanie kropką.
Bez niej werdykt brzmiałby „to nie zdanie”
nad każdą pozycją każdego wyliczenia i nie mówiłby nic o polszczyźnie.

**Tekst ustawy zmienianej odjęty.**
Rozdział o zmianach w przepisach obowiązujących cytuje cudze przepisy,
a te są tekstem innej ustawy i odpadają.
Zostaje po nich przesłanka, która czyta się jak całe zdanie:
`W ustawie z dnia 14 czerwca 1960 r. - Kodeks postępowania administracyjnego
art. 221 otrzymuje brzmienie.`
Zdanie tego kształtu jest w tym korpusie odrzucone i nie jest to werdykt o polszczyźnie.

**Biały znak znormalizowany.**
Wcięcia HTML-a idą do jednej spacji,
więc odstęp podwojony i odstęp przed znakiem przestankowym
nad tą prozą nie stoją nigdzie.
To zero jest zerem ekstrakcji, nie rejestru.

**Myślnik, którego HTML nie ma.**
Ustawa ogłoszona w PDF-ie ma w nazwie kodeksu półpauzę
(`ustawa z dnia 14 czerwca 1960 r. – Kodeks postępowania administracyjnego`),
a HTML tego samego aktu ma tam dywiz i półpauzy nie ma nigdzie.
Kto liczy pauzy nad tym HTML-em, mierzy więc wydawcę, a nie prawodawcę,
i jest to ta sama usterka korpusu, którą przegląd korpusów zgłasza
[warstwie tekstowej NKJP](corpora.md#its-text-layer-has-been-character-normalized).

## Co gramatyka z tego wyprowadza

```sh
python3 -m olski.check proza/ustawy/DU-1990-95.txt
python3 -m olski.check proza/ustawy/*.txt | grep -oE ': (valid|ambiguous|rejected|fragment|unclosed) ' \
  | sort | uniq -c
```

Wiersz na akt drukuje to polecenie, więc tabeli z niego tu nie ma:
rusza ją każda dopisana produkcja,
a to, co z niej zostaje prawdą, mieści się w jednym zdaniu.
Prowadzi ustawa o samorządzie gminnym, gdzie jednoznaczne jest
blisko jedno zdanie na dziesięć, a w pozostałych sześciu aktach kilka razy mniej,
choć akty różnią się długością trzydziestokrotnie.
Same „Zasady techniki prawodawczej” stoją poza tym pomiarem, bo są rozporządzeniem:
niespełna siedemset zdań, z tego kilka jednoznacznych i kilkadziesiąt wieloznacznych.
Werdyktu „to nie zdanie” nie ma nigdzie ani razu, bo kropkę stawia ekstrakcja.

Zdania wyprowadzone jednoznacznie mają kilka kształtów.
Jeden z nich jest tym, dla którego olski powstał:

```text
Gmina posiada osobowość prawną.
Mieszkańcy gminy tworzą z mocy prawa wspólnotę samorządową.
Działalność sołtysa wspomaga rada sołecka.
Budżet oraz wysokość składek uchwala sejmik.
Ustawa zawiera przepisy merytoryczne.
Artykuł powinien być w miarę możliwości jednozdaniowy.
```

Dwa ostatnie są przepisami „Zasad techniki prawodawczej”:
zdanie, które żąda od artykułu jednozdaniowości, jest jednym zdaniem olskiego,
a definicja części ustawy z § 14 ust. 1 przechodzi przez ekstrakcję i przez gramatykę naraz.

Inny jest terminem tego rejestru z dopełniaczem pod nim, czyli tym kształtem,
[dla którego gramatyka ma pozycję](#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa):

```text
Organem wykonawczym gminy jest zarząd.
Status prawny pracowników samorządowych określa odrębna ustawa.
Podmiotami ochrony ludności są jednostki organizacyjne pomocy społecznej.
Podstawową jednostką redakcyjną ustawy jest artykuł.
```

Ostatnie jest § 54 „Zasad techniki prawodawczej”, czyli przepisem,
który nazywa artykuł podstawową jednostką redakcyjną ustawy
i nazywa go dokładnie tym kształtem.

Ile zdań przypada na który kształt, nikt po tym przeliczeniu nie policzył,
bo klasyfikacja idzie tu ręką, zdanie po zdaniu.

Nie każde z tych zdań napisał prawodawca, i widać to na dwóch klasach.
Dwa są jednym słowem: `Kalisz.` i `Przemyśl.` są pozycjami wyliczenia okręgów
wyborczych, którym ekstrakcja dopisała kropkę,
a Morfeusz czyta `kalisz` i `przemyśl` jako formy czasownika,
więc wychodzi z nich zdanie bezpodmiotowe o jednym czytaniu.
`Podmiotami ochrony ludności są Polski Czerwony Krzyż.` pokazuje drugą:
składanie przesłanki z pozycją daje tu zdanie, które nie zgadza się co do liczby,
a wyprowadza się, bo Morfeusz zna `Krzyż` także jako nazwisko nieodmienne,
czyli czytanie pasujące do liczby mnogiej i pojedynczej naraz.
W obu klasach wyprowadzenie opiera się na czytaniu, którego polszczyzna nie ma, a
[wykluczenie ze słownika](subset.md#the-dictionary-offers-readings-polish-does-not)
po nie nie sięga: wymaga ono, żeby forma miała obok czytanie z klasy zamkniętej.
Zdania przyjęte tego rejestru przeczytano wszystkie
i takich jest wśród nich kilka procent;
liczbę wraz z klasami trzyma
[subset.md](subset.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma).
Prowadzą obie klasy wyżej, czyli te, które robi ekstrakcja:
pozycja wyliczenia zamknięta kropką oraz przesłanka złożona z pozycją.

Średnie zdanie ma tu 21 słów (104 062 na 4921),
a pokrycie gramatyki [urywa się nad dziesięcioma](corpus.md#the-measurement),
więc udział zdań wyprowadzonych jest z tej długości, a nie z rejestru.
Nad README ta sama gramatyka wyprowadza garść zdań
i [tamten przebieg](corpus.md#where-the-analyses-stop) trzyma ich liczbę,
więc różnica między jednym pomiarem a drugim
jest różnicą długości zdania, a nie staranności piszącego.

## Wieloznaczność jest tu odczytem z § 6, ale nie jest zarzutem

Wieloznaczne są tu przeszło cztery zdania na pięć z tych,
którym olski daje jakiekolwiek czytanie,
a nad Składnicą, czytaną tym samym analizatorem, około połowy
([corpus.md](corpus.md#what-morphological-ambiguity-costs)).
Różnią się najczęściej podmiotem i dopełnieniem,
bo za nimi stoi jedna rzecz: przyłączenie wyrażenia przyimkowego,
którego [olski nie wybiera](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).
Najdłuższe mają czytań tyle, że liczba przestaje o czymkolwiek mówić:

```sh
python3 -m olski.check proza/ustawy/*.txt | grep -oP '\d+(?= readings)' | sort -rn | head -3
```

Kilkadziesiąt zdań ma ich więcej niż `MAX_READINGS`,
a najdłuższe idą w setki tysięcy; trzy pierwsze drukuje polecenie wyżej.
Liczby te są dokładne, bo las podaje je bez wyliczania drzew,
a `MAX_READINGS` z `olski/parse.py` sięga wypisywania czytań
i nie sięga ani liczenia ich, ani ról, o które się one różnią.

Werdykt nad takim zdaniem nazywa dwa albo trzy przyłączenia
i konstytuent czytany na kilka sposobów,
czyli wyjaśnia kilkanaście czytań z tych dziesiątek tysięcy,
a resztę zostawia bez nazwy.
Zdanie, które to pokazuje, jest wyliczeniem siedmiu grup imiennych
spiętych przecinkiem i spójnikiem —
`ministrów, sekretarzy stanu i podsekretarzy stanu, …` —
a olski bierze [współrzędność na czterech poziomach](subset.md#nothing-above-a-coordination-distributes-into-it),
więc ciąg tej długości ma sam z siebie wiele czytań o jednym znaczeniu.
Wiersza ciąg nie dostaje, bo granicę członu pokazuje nawias w napisie roli
([design-notes.md](design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)).
Ile czytań ciąg tu wnosi, nikt nie policzył,
i to jest ta wieloznaczność, o którą werdykt tego rejestru pytać nie umie.

Widać ją najczyściej tam, gdzie zostaje sama.
Garść wieloznacznych werdyktów nie mówi nic poza liczbą czytań,
i w każdym z nich jest to ciąg współrzędny stojący wewnątrz wypełnienia roli,
czyli tam, dokąd nawias nie schodzi.
`Ustawa określa zadania ochrony ludności i obrony cywilnej.`
wychodzi dwoma czytaniami:
`zadania [ochrony ludności] i [obrony cywilnej]` mówi o zadaniach dwóch rzeczy,
a `zadania ochrony [ludności i obrony cywilnej]` o zadaniach jednej.
Klasa jest ta sama nad Składnicą i tam też zostaje po werdykcie sama liczba
([disambiguation.md](disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)).

Werdykt nazywa obok tych dwóch przyłączeń dopełnienie
jako rolę, o którą czytania tego zdania się różnią,
a streszczenia, które `--readings` nad nim wypisuje,
są co do dopełnienia zgodne.
Rolę tę bierze
[z lasu](design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań),
a nie z tej listy, tak samo jak liczbę czytań obok niej.

Kształt tej wieloznaczności widać najkrócej nad zdaniami,
których w tym korpusie nie ma:
Konstytucja jest w API tylko w PDF-ie, więc ta ekstrakcja jej nie czyta,
a jej artykuły są dla tego rejestru krótkie i pisane wprost.

```sh
python3 -m olski.check -c "Władza zwierzchnia w Rzeczypospolitej Polskiej należy do Narodu."
python3 -m olski.check -c "Sejm sprawuje kontrolę nad działalnością Rady Ministrów."
```

```text
<text>: ambiguous Władza zwierzchnia w Rzeczypospolitej Polskiej należy do Narodu.
                  4 odczytania, różne w roli: podmiot; „w Rzeczypospolitej Polskiej” → „Władza”, „należy”; „Rzeczypospolitej Polskiej” ma 2 odczytania
<text>: ambiguous Sejm sprawuje kontrolę nad działalnością Rady Ministrów.
                  2 odczytania, różne w roli: dopełnienie; „nad działalnością Rady Ministrów” → „sprawuje”, „kontrolę”
```

Pierwsze niesie obok przyłączenia drugi wybór, ten słownikowy:
`Polskiej` jest i przymiotnikiem, i dopełniaczem `Polski`,
więc `Rzeczypospolitej Polskiej` czyta się dwoma sposobami,
a dwa wybory razem dają cztery czytania i tyle właśnie werdykt wyjaśnia.

Drugie z tych zdań pokazuje, dlaczego liczba wieloznacznych werdyktów
nie jest liczbą przepisów niejednoznacznych:
oba jego czytania mówią, że Sejm kontroluje działalność Rady Ministrów,
i różnią się drzewem, a nie normą.
Jest ona liczbą przepisów, w których jednoznaczność bierze się z wiedzy o świecie,
a nie ze składni,
i to jest wszystko, co pomiar tej wielkości mówi:
[wieloznaczność mierzy pewność](glr-in-practice.md#ambiguity-as-a-confidence-measure),
a nie poprawność.

Pozostałe mają w tym rejestrze wagę, której nie mają w dokumentacji.
Spór o to, do czego w przepisie dochodzi wyrażenie przyimkowe,
jest sporem o to, kogo przepis dotyczy,
i rozstrzyga go sąd, a nie autor.
Tę samą wagę ma nawiasowanie ciągu współrzędnego,
bo `zadania ochrony ludności i obrony cywilnej` wylicza raz dwie rzeczy, a raz jedną,
czyli przepis ma pod każdym czytaniem inny zakres.
Wiersza werdykt o tym nie drukuje i to jest cena milczenia opisanego wyżej:
autor dostaje liczbę czytań w miejscu, w którym potrzebuje nazwy wyboru.
Narzędzie, które autorowi pokazuje oba czytania przed uchwaleniem,
odpowiada więc na pytanie, które inaczej zadaje się dopiero w sporze,
i to jest jedyne miejsce w tym repozytorium,
gdzie werdykt „wieloznaczne” ma adresata poza autorem tekstu.

## Gdzie stają analizy w tym rejestrze

```sh
python3 -m olski.check proza/ustawy/*.txt | grep -oP 'nie bierze \K[^;]*' \
  | grep -oP '(?<=„)[^”]+(?=”)' | sort | uniq -c | sort -rn | head -20
```

Odrzucenie stoi tu w większości na formie, której żadna produkcja nie bierze,
a w reszcie na samej strukturze;
dzisiejsze liczby jednych i drugich drukuje polecenie wyżej,
bo każde dopisanie do gramatyki je rusza.
Ranking obejmuje pierwszą z tych dwóch grup i drugiej nie widzi wcale,
a największą konstrukcją, jaka w niej stoi, jest `o którym mowa`:
niesie je co siódme zdanie tych dwóch korpusów, a każda forma ma tam licencję,
więc odrzucenie stało na strukturze zdania względnego z opuszczoną kopułą.
Gramatyka je dostała i wyszedł z tego jeden werdykt przeniesiony na wieloznaczne,
czyli przeszło o dwa rzędy wielkości mniej, niż obiecywały te wystąpienia.
Różnicę tę robi ta sama klasa, która zajmuje dziewięć pierwszych miejsc niżej:
prawodawca pisze ten zwrot razem z adresem przepisu,
więc dwanaście z 851 wystąpień obywa się bez cyfry i bez skrótu.
Formy z czoła tego rankingu grupują się w trzy klasy:

| klasa | najczęstsze formy |
| --- | --- |
| aparat odsyłaczowy | `art` 717, dywiz 666, `§` 595, `r` 254, nawiasy 232 i 223, cyfry |
| cząstki | `także` 116, `również` 95 |
| imiesłowy i odsłowniki | `obejmujący` 100, `wykonywania` 88, `wniesienia` 61 |

Klasa przysłówkowa stała w tej tabeli piąta, a klasa spójników podrzędnych druga.
Obie zeszły z niej razem z produkcjami, które te formy wzięły
([subset.md](subset.md#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe),
[subset.md](subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).
Została po pierwszej klasa cząstek, którą kolejka liczyła razem z nią,
a Morfeusz rozdziela: `także` i `również` są w nim cząstkami, a nie przysłówkami,
więc produkcja przysłówka po nie nie sięga i nie miała sięgać.
Kolejka odrzuceń rusza się przy tym mocniej niż suma werdyktów:
zdanie, które stawało na spójniku albo na `który` po przecinku,
staje teraz dalej albo nie staje na żadnym słowie, a przyjęte przez to nie jest,
więc odrzuceń stojących na formie ubywa, a stojących na strukturze przybywa tyle samo.

Pierwsza klasa zajmuje dziewięć pierwszych miejsc rankingu,
i jest to jedna konstrukcja, a nie dziewięć:
odsyłacz `art. 96 ust. 1 pkt 1` w środku zdania,
dywiz z nazwy kodeksu i nawias wokół adresu publikacji.

Kolejka wychodzi więc inna niż ta,
którą [Składnica ustawiła](corpus.md#where-the-analyses-stop),
i różnica jest informacją o rejestrze.
Czas przeszły prowadził tamtą kolejkę,
a tutaj dawał kilkadziesiąt trafień
(`był`, `była`, `było`, `były`, `został`, `została`)
i do dwudziestu pierwszych miejsc nie wchodził:
ustawa mówi w czasie teraźniejszym o tym, co ma być,
a przeszły zostaje jej na przepisy przechodnie.
Na czele tej kolejki stało za to zdanie warunkowe,
czyli kształt, w którym norma jest w ogóle zapisana:
`Jeżeli` dawało kilkaset trafień na dwie pisownie.

Gramatyka dostała i jedno, i drugie, a nad tym rejestrem nie kupiła prawie nic.
Czas przeszły, przeczenie, cztery szyki podmiotu, dopełnienia i czasownika,
zdanie warunkowe oraz pytanie zależne przyjmują tu najwyżej pojedyncze zdania,
przenoszą z odrzuconych na wieloznaczne od pojedynczych do kilkudziesięciu
i pojedynczym zdaniom przyjętym wcześniej odbierają jednoznaczność.
Cena każdej z nich stoi przy konstrukcji, czyli w jej sekcji [subset.md](subset.md),
a przebieg, którym ją policzono, stoi w gicie:
pytanie „wpuszczać czy nie” pada raz, więc ten dokument nie liczy jej drugi raz.
Szyk wypada z tej listy najgorzej i wypada pod zero:
ustawa pisze zdanie w szyku, który olski miał,
więc dopisany daje jej same nowe czytania,
i tym różni się ten rejestr od prozy z banku drzew,
gdzie te same ciała kupują kilkadziesiąt zdań.
Pytanie zależne kupiło tu zdanie
`Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.`,
a drugą połowę jego wyprowadzenia daje
[pozycja z obiema przydawkami](#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa).
Zdania pytającego ten rejestr nie ma ani razu, więc ta połowa konstrukcji nie rusza tu nic.

[Grupa liczebnikowa](subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
przenosi nad tymi siedmioma aktami pojedyncze zdania,
a pojedyncze z nich przechodzą aż na przyjęte.
Zakupu nie ma tu więcej dlatego, że ten rejestr liczebnika nie pisze słowem.
Pisze go cyfrą, a cyfra stoi w tym rankingu na miejscach 3, 5, 6, 10 i 13
(`1` 612, `2` 380, `3` 319, `5` 175, `4` 166),
czyli wyżej niż cokolwiek, co gramatyka mogłaby dopisać jedną produkcją.
Cyfry olski nie bierze i dlaczego, mówi
[subset.md](subset.md#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii):
to jest ta połowa klasy, której ten rejestr używa,
i przypada ona razem z aparatem odsyłaczowym, w którym te same cyfry stoją.

Interpunkcja zdaniowa weszła trójką znaków, a rusza tu dwoma z nich.
Przecinek przed spójnikiem i średnik ruszają pojedyncze werdykty,
a średnik jest jedynym, który kupuje tu zdanie przyjęte;
jednoznaczności nie odbiera żaden z tych trzech znaków, tak samo jak nad Składnicą.
Dwukropek nie rusza ani jednego werdyktu i jego zero mówi o rejestrze,
a nie o produkcji.
Dwukropek pada w tej prozie siedemdziesiąt razy i za każdym z nich stoi wyliczenie,
a nie zdanie wyjaśniające — `W skład zarządu wchodzą: wójt albo burmistrz` —
czyli dokładnie ta połowa tej konstrukcji, której olski nie bierze
([subset.md](subset.md#what-it-does-not-cover-yet)).
Wszystkie siedemdziesiąt zdań jest odrzuconych i przed dopisaniem, i po nim,
a stają one na strukturze, na nawiasie albo na cyfrze,
więc pozycja, która tu weszła, nie ma nad tym rejestrem czego wziąć.

Przysłówek pokazuje najwyraźniej, jak mocno ta kolejka zawyża.
Dwie formy, którymi klasa przysłówkowa prowadziła w rankingu —
`odpowiednio` i `niezwłocznie` — obiecywały przeszło trzysta trafień,
a przysłówek zdjął stąd kilkadziesiąt zdań z listy odrzuconych,
więc kolejka tego rejestru zawyża mocniej niż kolejka ze Składnicy,
gdzie wiersz `adv` oddał prawie jedną trzecią tego, co obiecywał
([subset.md](subset.md#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe)).
Powód widać w tym rankingu wyżej:
trafienie liczy formę, a zdanie ustawy niesie ich kilka,
i przysłówek stoi w nim obok odsyłacza,
czyli klasy zajmującej dziewięć pierwszych miejsc,
która zdania nie wypuszcza tak czy tak.
Ta sama arytmetyka rządzi czasownikiem nieosobowym:
prawodawca pisze tę formę w ustawach 90 razy i w rozporządzeniu 35,
a zdania z nią niosą także odsyłacz, cyfrę albo wyliczenie
([subset.md](subset.md#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu)).

Grupa wysunięta razem z zaimkiem względnym rusza w każdym z dwóch tekstów
tego rejestru inną ze swoich dwóch pozycji,
a różnica ta jest informacją o dwóch tekstach, a nie o produkcji:
rozporządzenie pisze o ustawie i o akcie wykonawczym pod nią,
więc `na podstawie której` jest tam zwrotem powtarzanym przepis po przepisie,
gdzie ustawa nie ma o czym tak mówić.
Ustawa stawia za to samą grupę bez przyimka — `w okręgu wyborczym, którego wzór ustala` —
i to jest ta pozycja, którą rusza ona, a rozporządzenie nie.

Trybem przypuszczającym ten rejestr warunku nie zapisuje:
`jeżeli` pada tu przeszło trzysta razy, `gdyby` osiem, a `żeby` ani razu.
`aby` pisze prawodawca kilkadziesiąt razy, prawie zawsze z bezokolicznikiem
po `tak` albo `w taki sposób`, a zdania z nim niosą także co innego
i wychodzą odrzucone przed dopisaniem cząstki trybu i po nim
([subset.md](subset.md#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)).

Wszystkie te dopisania mówią o kolejce jedno:
wskazuje ona konstrukcje trafnie i wyceniać ich nie umie,
tak samo jak kolejka z banku drzew,
a zdanie tego rejestru jest po prostu dłuższe niż to,
co gramatyka domyka jedną konstrukcją.

## Gramatyka bierze termin z dopełniaczem, bo ten rejestr go nazywa

Ten rejestr nazywa termin rzeczownikiem z przymiotnikiem za nim —
`obrona cywilna`, `informacja publiczna`, `władza zwierzchnia`, `dobro wspólne` —
a potem dokłada mu dopełniacz i pisze
`zadania ochrony ludności`, `dobrem wspólnym wszystkich obywateli`.
`człon_imienny` w `olski/subset.py` ma osobno rzeczownik z przymiotnikiem,
osobno rzeczownik z dopełniaczem,
osobno każde z nich z wyrażeniem przyimkowym za sobą,
a obie przydawki naraz bierze pozycja dopisana dla tego rejestru:
bez niej ten kształt nie ma w olskim ani jednego wyprowadzenia.
Razem z nią wchodzi ta sama głowa z wyrażeniem przyimkowym na końcu,
której żąda [przyłączanie wyrażeń przyimkowych](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera):
bez tej drugiej wyrażenie po takim terminie
dochodzi do dopełniacza i do nikogo więcej,
czyli gramatyka wybiera przyłączenie, którego wybierać nie ma.

Zakup czyta się przejściami między werdyktami, a nie liczbą pokrycia,
bo przymiotnik za rzeczownikiem konkuruje z orzecznikiem przymiotnym,
a dopełniacz pod nim z dopełniaczem pod rzeczownikiem po lewej.
Zdejmowane są obie pozycje naraz, bo weszły razem.
Nad siedmioma ustawami kilkadziesiąt zdań przestaje być odrzuconych,
z tego mniejsza część jednoznacznie,
a w drugą stronę idą pojedyncze zdania jednoznaczne, które przechodzą na wieloznaczne;
nad „Zasadami techniki prawodawczej” przejścia pierwszego rodzaju są pojedyncze,
a nad [Składnicą](corpus.md#the-measurement) idą w tę samą stronę i są liczniejsze.
Zdanie przechodzi tu wtedy, gdy do wyprowadzenia brakuje mu samej tej pozycji,
a takich zdań jest tym więcej, im więcej gramatyka ma poza nią,
więc rusza je każda zmiana w gramatyce, a nie drukuje ich żaden przebieg:
liczy się je, zdejmując obie pozycje wymienione wyżej
i puszczając werdykt nad trzema korpusami tej sekcji.

Jednym z przechodzących jest zdanie, które ta pozycja przyjmowała kiedyś na opak.
`Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.`
wychodziło jednym czytaniem, w którym zdanie podrzędne z `które`
jest zdaniem współrzędnym po przecinku,
a polszczyzna czyta je jako podrzędne:
pozycja z dopełniaczem dokładała ostatni brakujący kawałek wyprowadzenia,
a resztę dawała koordynacja przecinkiem, którą gramatyka miała bez podrzędności.
Werdykt jednoznaczny nad zdaniem przeczytanym na opak jest najgorszym,
jaki olski wydaje, i zdjął go
[warunek na zaimek względny](subset.md#zaimek-względny-nie-jest-przymiotnikiem-przy-rzeczowniku),
po którym zdanie było odrzucone i z tą pozycją, i bez niej.
Dziś wyprowadza się raz i wyprowadza się tak, jak je czyta czytelnik,
bo gramatyka ma [pytanie zależne](subset.md#what-the-grammar-covers),
a ta pozycja dalej daje mu grupę `które zadania własne gminy`:
bez niej nie ma ono wyprowadzenia żadnego.

Po drugiej stronie stoją zdania, które przeszły na wieloznaczne,
i płacą one z dwóch różnych powodów.

```sh
python3 -m olski.check -c "Za prawidłową gospodarkę finansową gminy odpowiada zarząd."
python3 -m olski.check -c "Wynagrodzenie Szefa Krajowego Biura Wyborczego odpowiada wysokości wynagrodzenia sekretarza stanu."
python3 -m olski.check -c "Komisarz wyborczy pełni swoją funkcję niezależnie od sprawowania urzędu sędziego właściwego sądu."
python3 -m olski.check -c "Dodatkowych przedstawicieli wyznacza zainteresowana rada gminy."
```

Prawie wszystkie są wieloznaczne w polszczyźnie i olski melduje to słusznie.
Zdanie o gospodarce finansowej wychodzi trzema czytaniami,
bo dopełniacz `gminy` ma gdzie stać poza pozycją dopełnienia,
a kiedy tam stoi, `zarząd` jest i mianownikiem, i biernikiem, czyli tym synkretyzmem,
który [własność jednoznaczności](subset.md#validity-is-uniqueness-not-just-derivability) odrzuca.
Jedno czytanie miało ono nie dlatego, że jest jednoznaczne,
tylko dlatego, że gramatyka nie miała gdzie tego dopełniacza postawić.

Zdanie o wynagrodzeniu pyta, czyj jest przymiotnik:
`Szefa Krajowego Biura Wyborczego` czyta się jako szefa Krajowego Biura Wyborczego
i jako Szefa Krajowego przy Biurze Wyborczym,
a to są dwa różne stanowiska w tej samej ustawie.
Tak samo dzieli się `opiekunów prawnych tych osób` z ustawy o ochronie ludności
oraz `sędziego właściwego sądu` z Kodeksu wyborczego,
i zdania z tymi dwoma wyrażeniami stoją w tej samej klasie.
Podział przydawki jest tym samym sporem, co przy
[przyłączaniu wyrażenia przyimkowego](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera),
o jeden poziom niżej: przydawka stoi między dwoma rzeczownikami
i należy do tego po lewej albo do tego po prawej,
a rozstrzyga to wiedza o urzędach, a nie składnia.
Gramatyka bez tej pozycji przyjmuje takie zdanie z jednym z dwóch czytań
i nie mówi, że drugie istnieje.

Jedno z nich płaci za wieloznaczność słownika.
Wychodzi dwoma czytaniami o tym samym streszczeniu ról,
bo Morfeusz zna `zainteresowana` jako rzeczownik, a `rada` jako formę `rad`,
i [wykluczenie](subset.md#the-dictionary-offers-readings-polish-does-not) tam nie sięga,
bo żadne z tych dwóch czytań nie jest nieodmienne.
Werdykt nazywa nad nim konstytuent, właśnie dlatego, że streszczenia są tu jednym napisem
([design-notes.md](design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)),
i tak samo nazywa `Szefa Krajowego Biura Wyborczego` w zdaniu o wynagrodzeniu.

## Pakiet typograficzny nad tym rejestrem milczał

Pakiet jest wycofany ([linter.md](linter.md#co-zamknęło-pakiet-reguł)),
więc ten przebieg jest zapisem, a nie poleceniem do powtórzenia.
Nad 104 062 słowami nie strzeliła ani jedna reguła.
Cudzysłowów prostych i angielskich nie ma,
polskie stoją parami (116 otwierających i 116 zamykających),
pauzy nie ma żadnej, a znaki przestankowe mają po sobie odstęp wszędzie.
Dwie z tych zer są zerami ekstrakcji, jak wyżej,
a pozostałe są własnością tekstu, który złożyła Kancelaria Sejmu.

Zero mówiło tu więc o korpusie, a nie o regule,
tak samo jak [tam, gdzie reguły cudzysłowu nie miały czego znaleźć](firing-rates.md#where-the-quotation-mark-rules-had-nothing-to-find):
tekst, nad którym pakiet milczy, jest podłogą, a nie próbką.
Nad oboma korpusami, które [odczyt częstości](firing-rates.md#the-rates) trzyma,
pakiet trafienia miał,
więc był to jedyny korpus tego repozytorium, nad którym nie miał żadnego.

## Nierozstrzygnięte

Czy ten korpus wchodzi do przeglądu korpusów
([corpora.md](corpora.md#the-composition-this-argues-for))
jako polszczyzna pisana przez ludzi.
Ma licencję, rejestr i etap produkcji, których tamten przegląd nie znalazł,
a nie ma tego, czego żądała od niego reguła typograficzna:
biały znak i pauzę zjada albo ekstrakcja, albo wydawca.
Rozstrzyga to pytanie ekstrakcja z PDF-a, którego API oddaje obok HTML-a,
a dopóki jej nie ma, ten korpus mierzy gramatykę i nic poza nią.

## Źródła

- Rozporządzenie Prezesa Rady Ministrów z dnia 20 czerwca 2002 r.
  w sprawie „Zasad techniki prawodawczej”,
  tekst jednolity Dz. U. z 2016 r. poz. 283 (`DU/2016/283`)
- Ustawa z dnia 4 lutego 1994 r. o prawie autorskim i prawach pokrewnych,
  art. 4 pkt 1 (`DU/1994/83`)
- API ELI Kancelarii Sejmu, `https://api.sejm.gov.pl/eli`,
  które oddaje akt pod adresem ELI w HTML-u i w PDF-ie
- Siedem ustaw korpusu, pod adresami ELI z polecenia wyżej;
  liczby w tym dokumencie wzięto 10 sierpnia 2026
  nad tym, co API wtedy oddało
