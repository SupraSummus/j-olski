# Zdanie podrzędne i wysunięcie na czoło

Jeden plik rejestru konstrukcji, w którym sekcja przypada na konstrukcję.
Cena i zakup stoją w niej rzędem wielkości albo granicą.
Co ten rejestr obiecuje i który plik czytać, mówi [wstęp](README.md).

## Podrzędność i koordynacja dzielą przecinek, a rozdziela je produkcja

Zdanie podrzędne otwiera w polszczyźnie ten sam znak,
którym koordynacja łączy dwa zdania składowe,
więc gramatyka, która ma przecinek i nie ma podrzędności,
nie odrzuca zdania podrzędnego — czyta je jako współrzędne.
`Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.`
wychodziło jednym czytaniem, w którym `które zadania własne gminy`
jest podmiotem drugiego zdania,
i pomiar nad rejestrem ustaw liczył to zdanie jako pokrycie
([ustawy.md](../ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa)).
Jedno czytanie, pewne siebie i błędne, jest gorsze niż odmowa.

Rozdziela je miejsce przecinka w produkcji, a nie warunek obok niej.
Koordynacja ma przecinek na poziomie zdania i powtarza tam własny symbol:
`zdanie → zdanie_składowe , zdanie`.
Podrzędność wciąga przecinek do konstytuentu, który sama tworzy,
więc `zdanie_podrzędne → , że zdanie` jest jednym konstytuentem wraz z przecinkiem,
a `zdanie` się w nim nie powtarza.
Po tym rozpoznaje ciąg współrzędny werdykt (`_koordynuje` w `olski/parse/streszczenie.py`)
i po tym samym rozpoznaje go sonda, która przecinek zdejmuje.
Samo powtórzenie symbolu im nie wystarcza, bo nad ciągiem stoi jeszcze
[okolicznik zdaniowy](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania),
który do całego ciągu dochodzi i własny symbol powtarza tak samo.
Rozdziela je znak: koordynacja spina członów spójnikiem albo przecinkiem
stojącym w ciele słowem, a określenie jest grupą,
która swój przecinek niesie w sobie.

Wywód ten stoi tutaj, a nie w [subset.md](../subset.md),
bo orzeka o podrzędnościach, które ta gramatyka ma,
a nie o każdej produkcji, którą ktoś dopisze.
Każda z nich wnosi przecinek własnym ciałem,
a sekcja, której ta przesłanka jest potrzebna, powtarza ją jednym zdaniem
i wskazuje tutaj.

## Przecinek zamykający należy do zdania podrzędnego, a nie do spójnika za nim

Przecinek zamykający stawia polszczyzna wtedy, gdy zdanie nadrzędne biegnie dalej,
a biegnie ono dalej także spójnikiem:
`Dokument mówi, że cena jest niska, i liczy cenę.`
Parę ciał — jedno zamknięte przecinkiem, drugie nie —
ma przez to każde zdanie podrzędne tej gramatyki.
Przecinek stoi w obu wewnątrz konstytuentu, a nie obok niego,
bo tym podrzędność różni się od koordynacji
([wyżej](#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja)).

`A, i B` dalej się nie wyprowadza i to jest tu cała ostrożność.
Przecinek przed `i` nie jest w polszczyźnie znakiem koordynacji zdaniowej
i lista spójników przecinkowych go nie obejmuje
([zdanie-złożone.md](zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
więc pozycja dochodzi zdaniu podrzędnemu, a nie spójnikowi:
znak wchodzi tam, gdzie polszczyzna go stawia, i nigdzie poza tym.

Kupuje to nad bankiem drzew kilkadziesiąt zdań, a nad prozą tego repozytorium kilka.
Liczba ta zależy jednak od tego, co jeszcze w gramatyce stoi, i to jest tu ciekawsze
od niej samej: zdjęta z gramatyki bez przydawki imiesłowowej ta sama pozycja
kupowała pojedyncze zdania, bo zdanie, które jej potrzebuje, potykało się wtedy
o imiesłów.
Cena pozycji pojedynczej jest więc różnicą wobec gramatyki dzisiejszej,
a nie stałą, którą raz się zapisuje
([pisanie-po-olsku.md](../pisanie-po-olsku.md#zasłanianie-działa-w-obie-strony)).

## Zdanie z `że` jest pozycją ramy, a nie konstrukcją obok niej

Czym jest zdanie podrzędne dopełnieniowe dla czasownika,
tym jest dopełnienie i bezokolicznik:
pozycją ramy, którą [leksykon walencyjny](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)
czasownikowi daje albo odbiera.
Wchodzi więc jako czwarta pozycja ramy domyślnej,
a nie jako produkcja dopisana do każdego szyku zdania z osobna,
i tak samo jak tamte trzy dochodzi do czasownika przez `wypełnienia`.
Kosztuje to jedno słowo w `RAMA_DOMYŚLNA` i jedno ciało w `olski/subset/zdanie.py`.

Spójnikiem jest `że` i nic poza nim,
choć Morfeusz daje klasę `comp` także formom `gdy`, `jeśli` i `aby`.
Tamte otwierają okolicznik zdania, a nie dopełnienie,
więc wpuszczone tą produkcją stanęłyby w pozycji, której nie zajmują,
a czasownikowi, który zdania podrzędnego nie bierze,
dałyby czytanie, w którym je bierze.
Własną pozycję dostały [niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)
i jest nią okolicznik zdania, czyli dokładnie ta, którą zajmują.

Pod złotą morfologią przebieg nad Składnicą rusza kilkadziesiąt zdań
i wszystkie w tę samą stronę:
większość przechodzi z odrzucenia w jednoznaczność, reszta w wieloznaczność,
a żadne zdanie już przyjęte nie traci werdyktu ani nie zyskuje drugiego czytania.
Wśród nowo przyjętych większość zgadza się z drzewem wzorcowym,
jedno zdanie wychodzi zgodne częściowo, garść nie ma w nim roli do porównania,
a o ani jedno odwrócenie roli zgodność nie rośnie
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)).
Zakup ten rośnie przy tym z czasem przeszłym, a nie z podrzędnością:
zdanie podrzędne stoi w tym korpusie najczęściej przy czasowniku w tym czasie,
więc konstrukcja zmierzona przed nim była mierzona przy części swoich zdań
([orzeczenie.md](orzeczenie.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku)).

```text
Mieszkańcy grożą, że zablokują ulice.
Dodaje, że zwolnienia są nieuniknione.
```

## Okolicznik wyrażony zdaniem nie jest pozycją ramy i dochodzi do zdania

Zdania z `że` żąda czasownik, a zdania z `gdy` nie bierze żaden.

```text
Program zapisuje ustawienia, gdy linter sprawdza tekst.
Gdy linter sprawdza tekst, program zapisuje ustawienia.
```

Zdanie z `gdy` mówi, kiedy zachodzi to, o czym mówi zdanie obok niego,
i mówi to o całym tym zdaniu, a nie o jego orzeczeniu,
więc dochodzi tam, gdzie dochodzi wyrażenie przyimkowe wysunięte przed zdanie:
do zdania składowego, a nie do symbolu `wypełnienia`.
Dochodzi zarazem do całego ciągu współrzędnego, a nie do samego składowego w nim,
i te dwa czytania są dwoma zdaniami:
`Dwoisz się i troisz, aby rozwiązać problemy.` mówi o obu członach naraz,
a `Mieszkał z ojcem i nie chciał, żeby ktoś wiedział.` o samym drugim.
Bez pozycji nad ciągiem gramatyka ma samo czytanie drugie,
czyli wybiera przez przeoczenie
([subset.md](../subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)),
a nad zdaniami takimi jak pierwsze wybiera odwrotnie, niż czyta czytelnik.

Ciąg jest tu żądany cechą, bo nad zdaniem o jednym członie
oba ciała dają ten sam napis dwoma kształtami.
Cena stoi przez to w jednoznaczności, a nie w pokryciu:
nad Składnicą traci ją garść zdań przyjętych,
nad prozą tego repozytorium pojedyncze zdanie,
a z odrzuconych do przyjętych nie przechodzi ani jedno.
Bez żądania ciągu cena jest kilkakrotnie wyższa,
bo dochodzi do niej każde zdanie o jednym członie.
Bank drzew tego wyboru nie rozstrzyga:
oba czytania mają rolę okolicznika o tej samej rozpiętości,
a porównanie ról pyta o rozpiętości
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)),
więc różnicę widać w werdykcie po nazwie gospodarza i nie widać jej w pomiarze.
Tym jednym różni się ta konstrukcja od [zdania z `że`](#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej),
a reszta jest w obu ta sama: przecinek należy do konstytuentu, który spójnik tworzy,
a nie do produkcji nad nim.

Przecinek stoi przy tym po tej stronie, po której stoi zdanie nadrzędne,
więc ciała są dwa, a wiąże je z pozycją cecha.

Spójnik jest warunkiem na lemat i lista jest zamknięta.
Poza nią zostaje `bowiem`, bo polszczyzna stawia je za pierwszym wyrazem zdania,
oraz `więc`, bo zdania nie podporządkowuje, tylko dokłada skutek:
`Program zapisuje ustawienia, więc linter sprawdza tekst.`
jest dwoma zdaniami spiętymi spójnikiem po przecinku
([zdanie-złożone.md](zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
Zdanie pod spójnikiem z tej listy stoi w trybie oznajmującym,
a `aby`, `żeby`, `by`, `gdyby` i `jakby` żądają przypuszczającego
i biorą przez to ciała osobne
([orzeczenie.md](orzeczenie.md#tryb-przypuszczający-jest-jedną-cząstką)).

Listy są przez to dwie, a nie jedna, bo wysunięcie jest faktem o słowie:
`Zostaję w domu, bo pada.` jest polszczyzną, a `Bo pada, zostaję w domu.` nie jest,
i tak samo dzieli się `gdyż` od `ponieważ`, choć oba mówią o przyczynie.
Fakt ten skład trzyma o dwóch z tych lematów
(`olski/skład/spójniki.py`),
i `todo/` trzyma ruch, którym oba kierunki czytałyby jeden leksykon,
tak jak czytają jeden leksykon walencyjny.
Sam podział ma przy tym świadka zmierzonego:
nad Składnicą `gdyż` nie otwiera ani jednego zdania,
tak samo jak `bowiem`, którego gramatyka nie bierze wcale,
a `gdy` i `jeśli` otwierają dwie piąte swoich wystąpień i ponad połowę.
Liczby dla `bo` i dla `albowiem` mierzą co innego niż tamte
i sonda mówi to o sobie sama:
zdanie zaczynające się od tych spójników odsyła w tym korpusie do zdania przed nim,
zamiast być zdaniem podrzędnym wysuniętym przed swoje nadrzędne.
Dwa wpisy listy wysuwanej nie mają w tym korpusie świadka wcale:
`dopóki` i `póki` stoją w nim raz albo dwa i ani razu na czele zdania,
więc na tej liście stoją z samego znaczenia, a nie z pomiaru.

Okolicznik ten jest rolą, którą werdykt nazywa, tak samo jak przysłówek
([okolicznik.md](okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy)),
i jest zarazem zdaniem podrzędnym, czym żadna inna rola nie jest.
Symbol stojący i wśród ról, i wśród zdań podrzędnych
rozstrzyga o dwóch rzeczach naraz, i rozstrzyga je przeciwnie:
streszczenie nazywa ten okolicznik całym napisem, bo jest on rolą,
a w środek jego nie zagląda, bo podmiot spod spójnika jest podmiotem tamtego zdania.
Zejście po role zatrzymuje się więc na takim węźle, a nie przed nim
(`Node.find` w `olski/parse/czytanie.py`
oraz `_pierwsza_rola` w `olski/parse/las.py`),
a kosztuje to jeden warunek w obu zejściach po role.

Widać po tym, do którego zdania okolicznik doszedł:

```text
Pomiar mówi, że autor pisze, ponieważ tekst jest gotowy.
```

Czytania są dwa i oba polszczyzna nad tym zdaniem ma,
a streszczenie rozdziela je nazwaniem tej roli albo przemilczeniem jej:
okolicznik doszedł do zdania streszczanego albo do tego, które stoi pod `że`.

## Przysłówek względny otwiera okolicznik i nie określa zdania

Okolicznik wyrażony zdaniem
([wyżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania))
otwiera także `gdzie`, a Morfeusz daje tej formie `adv`, a nie `comp`,
więc pozycji spójnika nie dosięga i bierze osobne ciało.

```text
Wchodzi w roadmap.md, gdzie każdy etap ma kryterium wyjścia.
Gdzie cząstka może należeć do dwóch czasowników, olski wypuszcza oba odczytania.
```

Miejsca są dwa, tak samo jak przy spójniku wysuwanym,
i o drugim z nich rozstrzyga pomiar, a nie wywód:
zdanie wysunięte znaczy tu `wszędzie tam, gdzie` i o miejsce nie pyta,
więc wygląda na kształt, którego ta proza nie pisze, a pisze go.
Ciało samo za zdaniem odbiera przez to czytanie napisom, które w niej stoją.

**Okolicznikiem zdania oznajmującego ta forma nie bywa i pozycji tej nie ma.**
Wpuszczona tam daje każdemu zdaniu z `gdzie` czytanie ciągu współrzędnego,
w którym przysłówek określa człon drugi,
i jest to nad `Program zapisuje ustawienia, gdzie linter sprawdza tekst.`
czytanie jedyne, a polszczyzna go nie ma.
Wykluczenie stoi więc na terminalu okolicznika i weszło razem z tym ciałem,
tak samo jak wykluczenie zaimka rzeczownego weszło razem ze swoimi czołami
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).

Cena tego wykluczenia jest wypisana, bo mierzy się ją osobno:
bez niego nad prozą tego repozytorium zdań przyjętych jednoznacznie
jest o kilka mniej, a wieloznacznych o kilkanaście więcej.
Zabiera ono za to `gdzie indziej`, czyli parę, w której ta forma określa
drugi przysłówek, więc para ta dostaje własne ciało
i bez niego wykluczenie odbierałoby zdania, które ta proza pisze.
Pytania o miejsce to wykluczenie zabiera i zdania takiego olski nie ma:
rolą wysuniętą jest tam okolicznik, a czoła pytań wysuwają podmiot,
dopełnienie albo orzecznik, więc pytanie o miejsce zostaje
[subset.md](../subset.md#what-it-does-not-cover-yet).

## Zaimek względny nie jest przymiotnikiem przy rzeczowniku

Morfeusz daje `który` znacznik `adj`, czyli ten sam, co `nowy` i `polski`,
i to jest cały powód, dla którego `które zadania własne gminy`
wychodziło grupą imienną.
Przymiotnikiem przy rzeczowniku ten wyraz w polszczyźnie nie bywa nigdy:
zaczyna zdanie względne albo pytanie, a przydawki nie tworzy.
Warunek jest więc taki sam jak przy [zaimku rzeczownym](grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)
i pada w tym samym miejscu — na terminalu, a nie w słowniku:
przydawka i orzecznik tego lematu nie biorą, a bierze go czoło zdania względnego.

Zdjęcie tego czytania jest tym, co odbiera czytanie współrzędne,
i odbiera je bez produkcji, która by go zabraniała:
`które zadania własne gminy` przestaje być grupą imienną,
więc nie ma czym być podmiotem zdania po przecinku.
Tańsza z dwóch dróg do czytania, którego polszczyzna nie ma,
prowadzi tędy, a nie przez wykluczenie w `admissible`
([roadmap.md](../roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).

Cena była ceną pozycji, której gramatyka nie miała, a którą ten warunek nazwał.
Pozycję tę stawia pytanie, więc `Który aktor robi na tobie największe wrażenie?`
oraz pytanie zależne `określają, które zadania` wyprowadzają się, każde raz.

## Zdanie względne niesie liczbę i rodzaj swojego zaimka

Przypadek zaimka względnego mówi o zdaniu podrzędnym,
a liczba i rodzaj o poprzedniku:
`który` bierze przypadek z roli, którą w zdaniu podrzędnym zajmuje,
a zgadza się w liczbie i rodzaju z tym, co określa.
Zdanie względne wypuszcza więc te dwie cechy do góry,
a produkcja, która je przyłącza, żąda ich od grupy imiennej.

Kupuje to przyłączenie, którego gramatyka nie musi wybierać:

```text
Zbiór tekstów, które są polskie, jest podzbiorem.
Zbiór tekstu, który jest polski, jest podzbiorem.
```

Pierwsze ma jedno czytanie, bo `które` jest w liczbie mnogiej
i do `Zbiór` przyłączyć się nie ma jak.
Drugie ma dwa, bo `Zbiór` i `tekstu` są oba męskie i pojedyncze,
i są to dwa czytania, które ma także czytelnik.
Jest to ta sama postawa co przy
[wyrażeniu przyimkowym](../subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera) —
gramatyka przyłączenia nie wybiera —
z tą różnicą, że tutaj większość wyborów odbiera zgodność,
czyli to samo, czym odbiera je czytelnik.

Zdanie względne dochodzi przy tym do symbolu `grupa_imienna`, a nie `człon_imienny`,
bo na poziomie członu produkcja rekurencyjna dałaby jednej strukturze
dwa wyprowadzenia, a te [są dwoma odczytaniami](../subset.md#co-się-liczy-jako-jedno-odczytanie).
Wyżej ten wybór nie istnieje,
bo `człon_imienny` bierze wszystko, co grupa niesie przed nim.
Kosztuje to symetrię w koordynacji:
człon prawy zdanie względne unieść może, a lewy nie,
więc `pliki, które rosną, i katalogi` nie ma wyprowadzenia.

Zdanie względne wypełnia trzy role, bo tylu ten rejestr używa,
a każda z nich jest tą, którą zaimek zabiera zdaniu podrzędnemu:
podmiot (`reguła, która rozstrzyga`),
dopełnienie (`polszczyzna, którą ktoś napisał`)
i wyrażenie przyimkowe (`język, o którym to repozytorium jest`).
Ostatnia sięga najdalej i jest jedną produkcją,
bo za wysuniętym wyrażeniem przyimkowym stoi zdanie składowe całe.
Podmiot za wysuniętym dopełnieniem stoi przy tym po czasowniku i przed nim,
choć zdanie główne ma ten szyk tylko w pierwszej wersji:
`które ktoś napisał` jest w polszczyźnie zwyczajne, a `Teksty ktoś napisał` nie,
i różni je to, że zaimek względny wysuwa polszczyzna zawsze,
a dopełnienie z wyboru.

**Dopełnienie stoi przed czasownikiem także tam, gdzie czołem jest podmiot.**
`reguła, która tekst sprawdza` i `ktoś, kto go nie używa` są w tym rejestrze
tak samo zwyczajne jak szyk z dopełnieniem za czasownikiem,
a zdanie główne ma oba od początku,
więc gramatyka bez tego ciała mówiła o szyku rzecz nieprawdziwą:
że zależy on od tego, czy któraś rola stoi wysunięta.

Ciało jest drugie i bierze osobny symbol orzeczenia,
a nie szyk dopisany do córek zdania.
Rozstrzyga o tym duplikat: córki zdania głównego przestawia
[deklaracja szyku](../subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk),
więc szyk dopisany tam dałby `Reguła tekst sprawdza.` drugie wyprowadzenie
tego samego kształtu, czyli [drugie odczytanie](../subset.md#co-się-liczy-jako-jedno-odczytanie).
Przed czasownik wychodzi przy tym samo dopełnienie, a nie całe wypełnienie ramy,
i to też jest warunek, a nie oszczędność:
wypełnienie niesie okolicznik w swoich ciałach, a okolicznik stawia przed
czasownikiem także deklaracja szyku, więc `którzy na niej stoją`
miałoby dwa wyprowadzenia jednego kształtu.

Nad prozą tego repozytorium ciało to daje czytanie kilkunastu zdaniom,
a jednoznacznych przybywa wśród nich kilka.
Ceną jest para zdań tracących jednoznaczność,
czyli takich, w których grupa imienna przed czasownikiem
konkuruje wewnątrz zdania względnego z przydawką albo z podmiotem.
Ani jedno zdanie nie traci przy tym czytania,
bo szyku tego nie bierze żaden inny kształt.

Wysunięte na czoło jest przy tym nie sam zaimek,
ale cała grupa, w której on stoi.
Pozycje ma ona dwie i obie niesie rejestr ustaw.
Pod przyimkiem niesie ją `ustawy, na podstawie której jest ono wydawane`,
zdanie „Zasad techniki prawodawczej”,
gdzie `której` jest dopełniaczem przy `podstawie`.
Bez przyimka grupa stoi w podmiocie i w dopełnieniu zdania składowego:
`ustawa, której przepisy obowiązują`.

Grupa niesie liczbę i rodzaj dwa razy, i to jest cała jej trudność.
Przypadka żąda od niej przyimek albo rola, w której stanęła,
a wypuszcza go jej rzeczownik.
Ten sam rzeczownik wypuszcza liczbę i rodzaj,
bo z głową grupy zgadza się orzeczenie zdania składowego.
Zaimek wypuszcza tę samą parę drugi raz i osobno,
bo w niej zgadza się z nim poprzednik zdania względnego.
Jedna para na obie zgodności wygląda poprawnie i odwraca każdą z nich:
`w wyniku której` ma głowę męską przy żeńskim poprzedniku,
a `której autorzy piszą` mnogą przy pojedynczym.
Para wzięta z zaimka przyjmuje przez to `Ustawa, której autorzy pisze`,
a para wzięta z głowy `Ustawy, której autorzy piszą` —
w obie strony werdykt pewny siebie i błędny.

Kształty grupy są dwa: rzeczownik z zaimkiem za sobą (`na podstawie której`)
i ten sam rzeczownik z zaimkiem przed sobą (`o którego zdaniu`).
Sam zaimek (`o którym`, `która rozstrzyga`) jest obok tych dwóch
czołem drugim, w tych samych dwóch pozycjach.
Czoła są dwa, a nie jedno obejmujące oba kształty,
i rozstrzyga o tym pomiar, a nie polszczyzna:
pod jednym czołem cena pozycji bez przyimka nie byłaby osobną liczbą,
a wywód stoi w `olski/subset/podrzędne.py` przy czołach obu rodzin.

Podmiotu zdanie z wysuniętym dopełnieniem nie żąda,
bo deklaracje są dwie — z podmiotem i bez niego —
tak samo jak ma je zdanie główne.
Jedno czytanie ma przez to `Dyrektor wymienia imprezy, które zorganizował.`
i jedno `Dyrektor wymienia imprezy, które on zorganizował.`.
Ciała pisze obu rodzinom czół jedna funkcja, więc to samo dostało pytanie:
`Które zadania wykonuje?` wyprowadza się obok `Które zadania gmina wykonuje?`.

Zakupem jest pod obiema morfologiami garść zdań Składnicy wyjętych z odrzucenia
i pojedyncze, które przechodzą z niego w wieloznaczność.
Role nowo przyjętych zgadzają się z drzewem wzorcowym poza jednym zdaniem,
a to jedno — `Złodzieje kradną drogi sprzęt, który potem sprzedają w cenie złomu.` —
olski czyta z okolicznikiem przy zdaniu nadrzędnym zamiast przy względnym,
bo miejsce na okolicznik jest w ciele jedno,
a to zdanie stawia okolicznik po obu stronach czasownika.

Płacą za to zdania, w których zaimek jest zarazem mianownikiem i biernikiem,
a czasownik biernik bierze, bo daje mu go rama domyślna:
`Wywód, który za nią stał, stoi dalej.` jest takim zdaniem,
a nad Składnicą pod żywą morfologią traci jednoznaczność jedno.
Pod złotą morfologią nie traci jej ani jedno,
bo anotator wybrał tam jedno czytanie na token,
a nad rejestrem ustaw nie rusza się ani cena, ani zakup.
Tą samą drogą wyprowadza się `Ustawa, której przepisy obowiązuje`,
i dlatego parę cech czoła pokazuje wyżej głowa męskoosobowa,
której mianownik różni się od biernika.

Pod żywą morfologią jedno z tych zdań wchodzi przy tym
nie tym czytaniem, o które szło.
`Myślę o tym człowieku, który mnie podglądał.` wychodzi
pytaniem zależnym w pozycji, którą każdemu czasownikowi daje
[rama domyślna](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej),
a nie zdaniem względnym:
zdanie względne z wysuniętym podmiotem stawia dopełnienie za czasownikiem,
więc `mnie podglądał` nie ma w nim gdzie stanąć.

Wysunięte dopełnienie sięga ponadto do formy osobowej i nie dalej,
bo ciała wypisane wyżej mają w środku czasownik zdania składowego,
więc dopełnienie należące do bezokolicznika pod nim nie ma się skąd wziąć:
`Ustawa, którą organ gminy może wydać, jest tania.` jest odrzucone.
Zdania tego kształtu nie ma jednak ani jedno zdanie rejestru ustaw,
co pokazuje `grep -P 'któr\w+ [^.]*\b(może|mogą|ma|mają)\b [^.]*\w+ć'`
nad `proza/ustawy/`, więc konstrukcja ta jest wyczytana z gramatyki,
a nie z korpusu.

Po ten brak sięgnęłaby cecha przeciągana, czyli luka zamiast wypisanych ciał,
a ile ona kupuje i dlaczego nie weszła, mierzy
[design-notes.md](../design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze).

### Bank drzew nazywa `który` inaczej niż Morfeusz, a czytelnik to przekłada

Składnica taguje `który` jako `padj`, czyli zaimek przymiotny,
a Morfeusz jako `adj`,
więc gramatyka pisana pod tagset Morfeusza nie sięgała po ani jedno wystąpienie
w przebiegu pod złotą morfologią.
Przekłada to dzisiaj czytelnik banku drzew, razem z trzema innymi nazwami
([corpus.md](../corpus.md#where-the-analyses-stop)),
i obie kolumny mierzą przez to zdanie względne tak samo.

Pod złotą morfologią zdanie z `że` wyciąga z odrzucenia kilkadziesiąt zdań Składnicy
i połowę z nich przyjmuje jednoznacznie,
a zdanie względne wyciąga mniej i jednoznacznie przyjmuje z nich garść.
Każdy z tych dwóch zakupów bierze osobny kontrfaktyk,
czyli tę gramatykę bez jednej z tych konstrukcji,
więc suma tych dwóch nie jest liczbą, jaką dałoby zdjęcie obu naraz.
Ani jedno zdanie przyjęte nie traci przy tym jednoznaczności,
więc jednoznaczność obie konstrukcje kosztują tu zero,
a wieloznaczności przybywa wyłącznie na zdaniach, które wcześniej odpadały.

```text
Widoczny jest wzrost aspiracji społeczeństwa, które chce zdobywać wykształcenie.
```

Rozbieżność tagsetów jest przy tym faktem o korpusie, a nie o gramatyce,
i zapisana jest tutaj dlatego, że kolumna złota mówiła bez tego przekładu
o zdaniu względnym nieprawdę:
liczba, która się nie ruszyła, czyta się jak konstrukcja, która nic nie kupuje.

## Dopełniacz z ramy wysuwa się na czoło, a celownik nie

Czoło dopełnienia brało dopełniacz przy przeczeniu i tylko przy nim,
bo tam rządzi nim negacja.
Dopełniaczem rządzi jednak i rama, więc zdanie względne o czasowniku,
który go żąda, nie miało czytania:

```text
Cena, której żądamy, jest niska.
Pozycja, której brakuje, jest droga.
Kogo dotyczy zmiana?
```

Pozycja jest trzecim ciałem tej samej trójki szyków,
a różni ją od dwóch pozostałych to, że przeczenia nie ogłasza.
Nie ma czego: dopełniacz negacji wchodzi w miejsce biernika
i tam kończy się jego zasięg
([orzeczenie.md](orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)),
a `nie brakuje ceny` stoi w dopełniaczu tak samo jak `brakuje ceny`.
Tam, gdzie czasownik bierze oba dopełniacze, jeden napis dostaje przez to
dwa wyprowadzenia i jedno czytanie, bo kształt mają ten sam
([subset.md](../subset.md#co-się-liczy-jako-jedno-odczytanie)).

Zakupem nad bankiem drzew jest pod złotą morfologią jedno zdanie
wyjęte z odrzucenia, a jest nim `Nie wiem, czego się obawia.`
Złote czytanie w nim ocalało.
Jednoznaczności nie traci pod tą morfologią ani jedno zdanie.
Pod żywą traci ją to samo zdanie
wraz z `Zadałem sobie pytanie, ile mogę zaryzykować, czego najbardziej się boję.`,
i jest to ta sama zamiana, którą liczy
[corpus.md](../corpus.md#what-morphological-ambiguity-costs):
oba stały tam na `czego` przeczytanym jako przysłówek,
czyli na czytaniu, którego polszczyzna w tym zdaniu nie ma,
a teraz stoją obok czytania prawdziwego.

Nad prozą tego repozytorium konstrukcja przyjmuje kilka zdań
i kilku dalszym daje pierwsze czytanie.
Jednoznaczność traci przy tym `jest zdaniem, którego makieta potrzebuje.`,
bo zdanie to miało czytanie z grupą `którego makieta` w podmiocie,
a dostaje obok niego czytanie z dopełnieniem `którego`.
Polszczyzna ma oba, więc wieloznaczność jest tu prawdziwa.

Celownika ta pozycja nie bierze i rozstrzyga o tym pomiar.
Nad bankiem drzew nie kupuje on ani jednego zdania w żadnej z dwóch morfologii,
a pod żywą odbiera jednoznaczność jednemu ponad te dwa wyżej.
Nad prozą tego repozytorium daje czytanie jednemu zdaniu
i jest to czytanie nieprawdziwe:
`szew, którym to zdanie wychodzi poza podzbiór` z tego dokumentu
niesie narzędnik, którego olski bez przyimka nie bierze
([subset.md](../subset.md#what-it-does-not-cover-yet)),
a celownik na czole czyta ten napis jako dopełnienie `wychodzić`.
Bezokolicznik z tej samej listy
([walencja.md](../walencja.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu))
zostaje na zewnątrz z powodu ogólniejszego:
wypełnienie inne niż dopełnienie na czoło się nie wysuwa.

## Pytanie o rozstrzygnięcie podporządkowuje spójnikiem, a nie rolą

Pytanie o rolę wysuwa tę rolę na czoło, a pytanie o rozstrzygnięcie
nie wysuwa niczego: podporządkowuje je spójnik, a zdanie pod nim jest całe.

```text
Czy program zapisuje ustawienia?
Pyta, czy go to dotyczy.
Pyta, kto płaci i czy program działa.
```

Czoło jest przez to osobnym ciałem, a nie lematem dopisanym do listy zaimków,
i nie przechodzi przez funkcję wypisującą szyki reszty zdania.
Pozycję ramy niesie ono tak samo jak pozostałe czoła,
więc ciąg pytań pod jednym czasownikiem miesza te dwa kształty bez osobnej pozycji.

Ten sam lemat bierze zarazem koordynacja bez przecinka,
gdzie `czy` znaczy `albo`, a rozdziela te dwa użycia materiał pod spójnikiem:
koordynacja stawia po nim człon, a to ciało zdanie.
Napisu wspólnego oba nie mają, więc drugiego czytania to ciało nie dokłada nikomu,
i tym różni się ono od czół zaimkowych,
które weszły razem z wykluczeniem
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).

## Czoło niesie etykietę roli, którą zajmuje, a werdyktu nie rusza

Wysunięty konstytuent zajmuje w zdaniu składowym rolę:
`która` w `reguła, która rozstrzyga` jest podmiotem,
a `którą` w `polszczyzna, którą napisał autor` dopełnieniem.
`_wysunięta_rola` w `olski/subset/podrzędne.py` stawia nad nim `podmiot` albo `dopełnienie`,
czyli tę samą etykietę, którą nosi rola wypełniona na swoim miejscu.

Bez tej etykiety olski wyprowadza te zdania dokładnie tak, jak czyta je bank drzew,
a rozdanie ról wychodzi z nich o jedną rolę uboższe,
więc porównanie ról nie ma go z czym zestawić;
ile zdań na tym stało, liczy
[corpus.md](../corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).

Etykieta jest osobnym konstytuentem nad czołem, a nie cechą na nim,
bo rolę czyta się z etykiety węzła (`Node.find` w `olski/parse/czytanie.py`),
i stąd bierze się trudność tej pozycji.
Symbol wpisany do ciała wpuszcza tam wszystkie swoje produkcje,
a `podmiot → grupa_imienna` wpuszcza w to miejsce każdą grupę imienną w mianowniku:
`reguła, ta reguła rozstrzyga` byłoby wtedy zdaniem względnym,
a `Który aktor robi wrażenie.` zdaniem oznajmującym o takim podmiocie,
czyli wróciłoby czytanie, które zdjął
[warunek na lemat](#zaimek-względny-nie-jest-przymiotnikiem-przy-rzeczowniku).

Rozdziela obie rodziny produkcji cecha `czoło` (`BEZ_CZOŁA` w `olski/subset/słowa.py`),
a niosą ją wszystkie produkcje obu symboli,
bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc rodzina milcząca przechodziłaby przez to żądanie za darmo.
Wartością jest nazwa symbolu, a nie jedno „wysunięte”,
bo każde czoło należy do jednej rodziny.
Wspólna wartość zlałaby te rodziny, więc `ustawa, który przepis obowiązuje`
wychodziłoby zdaniem względnym z grupą pytajną na czole,
a `Który zapisuje ustawienia?` pytaniem o sam zaimek.
Tę samą robotę wykonuje przy orzeczniku cecha `valency`:
rozdziela orzecznik zgodny od narzędnikowego, a kopula żąda drugiego z nich.
Cechę `czoło` niesie `orzecznik` obok tamtej i z tego samego powodu co podmiot:
orzecznik wysunięty na czoło jest tam trzecią rolą, którą czoło wypełnia
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).

Cena wyszła zerowa i wynika z kształtu tej zmiany, a nie z przebiegu.
Etykieta nie zmienia tego, co się wyprowadza, tylko to, jak się nazywa,
więc żaden werdykt ruszyć się nie może;
przebiegi nad bankiem drzew pod obiema morfologiami
oraz nad trzema korpusami prozy wydają to samo, zdanie po zdaniu.
Rusza się w nich sama kolejka blokerów, i o kilka zdań:
bloker mówi, dokąd rozbiór doszedł, a nie co się udało,
więc produkcja dopisana przesuwa go tam, gdzie tablica sięga dalej
(`bloker` w `olski/pokrycie.py`).

Zakup liczy się przez to w innej walucie i widać go w dwóch porównaniach ról
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)).
Pod złotą morfologią kilkadziesiąt zdań wieloznacznych przechodzi
z `lost` na `survives`, a garść przyjętych z `partial` na `agrees`;
`disagrees` nie rośnie o ani jedno.

Tych dwóch przejść nie liczy żadne polecenie i liczy je ręka,
bo sonda różnicowa liczy przejścia werdyktu (`harness/ruch.py`),
a ta pozycja nie rusza ani jednego.
Wariantem jest gramatyka bez produkcji, które `_wysunięta_rola` pisze nad czołem:
`podmiot → czoło` po jednej na czoło, `dopełnienie → czoło` po dwóch,
bo tam rozdziela je przeczenie, oraz `orzecznik → czoło` po jednej,
a wraz z nimi wychodzi cecha `czoło` z ról, które ją niosą.
`python3 -m harness.pomiar Składnica-frazowa-180723/` puszczony nad taką gramatyką
wydaje obie tabele bez etykiety, a różnica wierszy jest tymi dwoma przejściami.
Czego brakuje, żeby wzięło je polecenie, trzyma `todo/`.

Grupa pytajna niesie dwie etykiety naraz i obie są potrzebne.
`grupa_pytajna` mówi, o co zdanie pyta,
i bez niej pytanie przyjęte nie mówiłoby tego wcale
(`GRUPA_PYTAJNA` w `olski/subset/deklaracja.py`),
a `podmiot` albo `dopełnienie` mówi, czym ta grupa w zdaniu jest,
i tego żąda bank drzew, bo grupy pytajnej nie zna
i obsadza `Który aktor` podmiotem.
Streszczenie wypisuje przez to jedną rozpiętość dwa razy,
i tyle ta pozycja kosztuje w wydruku.

## Pytanie o okoliczność wysuwa przysłówek, a zdanie pod nim jest całe

Pytanie o rolę wysuwa tę rolę i zostawia po niej lukę
([wyżej](#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)),
a pytanie o okoliczność luki nie zostawia:
przysłówek stoi przed zdaniem, a zdanie pod nim ma wszystkie swoje role.

```text
Dlaczego gramatyka rośnie?
Pyta, dlaczego gramatyka rośnie.
```

Ciało ma przez to kształt wysuniętego wyrażenia przyimkowego, a nie kształt czoła:
rozwinięcie szyku wypisuje zdanie, któremu jednej roli brakuje,
a temu zdaniu nie brakuje żadnej.
Pary poprzednika ciało nie niesie, bo pytanie poprzednika nie ma.

Etykieta nad przysłówkiem jest osobną rolą.
Od grupy pytajnej różni ją to, o co zdanie pyta —
tamta nazywa rzecz, a ta okoliczność —
a od okolicznika przysłówkowego to,
że gospodarza nie ma i mieć go nie może:
przysłówek stoi przed całym zdaniem, a nie w którymś jego miejscu.
Bez tej etykiety pytanie wychodzi `valid` i o pytaniu nie mówi nic.

**Wykluczenie z pozycji okolicznika wchodzi razem z tym ciałem,**
tak samo jak wykluczenie zaimka rzeczownego weszło razem ze swoimi czołami
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Bez niego `Pyta, dlaczego gramatyka rośnie.` wychodzi ciągiem dwóch zdań
współrzędnych, w którym `dlaczego` określa czasownik członu drugiego,
a pytania zależnego nie ma w tym zdaniu wcale.
Czytania tego polszczyzna nie ma, a olski wydaje na nim `valid`,
czyli werdykt, który ten pomiar liczy jako najgorszy
([corpus.md](../corpus.md#what-morphological-ambiguity-costs)).

**Lematy wchodzą tu pojedynczo, bo rozdziela je reszta czytań, które mają.**
`dlaczego` ma u Morfeusza czytanie jedno i tylko ono weszło.
`jak` jest zarazem spójnikiem porównania — `tak samo jak reguła` —
a to czytanie gramatyka bierze,
więc lemat dopisany tutaj odbierałby zdania, które ta proza pisze.
`jaki` jest przymiotnikiem i żąda kształtu grupy pytajnej, a nie tego,
a `ile` liczebnikiem, który rządzi dopełniaczem.
Każdy z tych trzech jest przez to osobną robotą,
a nie lematem dopisanym do zbioru.

**`gdzie` zmierzono i zostaje na zewnątrz, dopóki nie zawęzi się rama domyślna.**
Pytanie o miejsce nad prozą tego repozytorium nic nie kosztuje w werdyktach —
pojedyncze zdania wychodzą z odrzucenia, a nie traci ani jedno —
a kosztuje czytaniem nieprawdziwym, którego po werdykcie nie widać:
`Wchodzi w roadmap.md, gdzie linter sprawdza regułę.` dostaje drugie czytanie,
w którym zdanie z `gdzie` jest pytaniem zależnym pod `wchodzi`.
Bierze się ono stąd, że pytanie zależne stoi w ramie domyślnej,
czyli dostaje je każdy czasownik spoza leksykonu
([walencja.md](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
a `wchodzić` pytania zależnego nie bierze.
Lemat ten wraca więc razem z zawężeniem tamtej pozycji do leksykonu;
`todo/` trzyma ten przebieg.

**Zostaje po tym pytanie zależne wysunięte przed zdanie nadrzędne.**
`Dlaczego parser stoi tu świadkiem, rozstrzyga design-notes.md.`
wyprowadzało się przedtem tym samym czytaniem nieprawdziwym,
a po wykluczeniu nie wyprowadza się wcale.
Pozycji tej nie ma przy tym żadne wypełnienie ramy:
`Że cena jest niska, mówi dokument.` jest odrzucone tak samo,
więc jest to jedna konstrukcja, a nie osobna dla pytania.
Zdań tego kształtu ta proza pisze garść i wszystkie zeszły razem;
`todo/` trzyma ruch i cenę, którą ten szyk sam ma.

## Kopułę opuszczoną wpuszcza wpis na lemat

Rejestr ustaw odsyła zwrotem `o którym mowa`:
`Rada wykonuje zadania, o których mowa w ustawie.` znaczy `o których jest mowa`,
a `jest` nie pisze tam nikt.
Morfeusz zna formę `mowa` wyłącznie jako `subst:sg:nom:f`,
więc zdanie względne tego zwrotu obywa się bez czasownika,
a zdanie składowe bez czasownika wyprowadza w tej gramatyce sama ta konstrukcja.
Zwrot ten jest najczęstszym zdaniem względnym rejestru ustaw —
niesie go co siódme zdanie dwóch jego korpusów
([ustawy.md](../ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)) —
więc konstrukcja ta odpowiada na kolejkę tamtego rejestru,
a nie na kolejkę ze Składnicy.

Wpuszczają ją dwa ciała, a rozdziela je to, skąd bierze się wyrażenie,
o którym ten rzeczownik orzeka.
Kopuła opuszczona takiego wyrażenia żąda, więc `Mowa o zadaniach.` jest polszczyzną,
a `Mowa.` nie jest.
Zdanie względne bierze to wyrażenie skądinąd:
`o których` leży poza zdaniem składowym, bo wysuwa je `wyrażenie_przyimkowe_względne`,
więc ciało czoła bierze ten rzeczownik wprost i zdania składowego nie ma pod sobą wcale.
Czoło pytania bierze go tym samym ciałem, więc `O którym akcie mowa?`
wyprowadza się razem z `o których mowa`.

Terminal tego rzeczownika żąda lematu, i to żądanie jest decyzją,
bo polszczyzna opuszcza kopułę szerzej niż w tym jednym zwrocie.
Wyjścia były dwa.
Pozycja ogólna czyni zdaniem składowym każdą grupę imienną w mianowniku,
czyli dopisuje `zdanie_składowe → podmiot` obok `zdanie_składowe → podmiot okoliczniki`.
Wpis leksykalny kupuje ten jeden zwrot i nic poza nim,
tak samo jak spójnik, którym zaczepia się
[zdanie z `że`](#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej).

Pozycję ogólną zmierzono, dopisując te dwie produkcje do gramatyki
i porównując werdykty z werdyktami olskiego.
Nad siedmioma ustawami wyciąga ona z odrzucenia setki zdań,
połowę z nich przyjmuje jednoznacznie,
a jednoznaczność odbiera garści zdań przyjętych wcześniej;
nad „Zasadami techniki prawodawczej” i nad prozą tego repozytorium
odbiera ją po jednym zdaniu.
Zakup nie jest jednak zakupem, i widać to po tym, co ona przyjmuje:

```text
Wrocław.
Siedziba Okręgowej Komisji Wyborczej: LEGNICA.
```

Nazwa miasta stoi w akcie w tabeli, a nie w zdaniu,
i olski melduje o niej `valid`.
Reszta zakupu jest tą samą usterką w środku zdania,
bo przecinek i spójnik koordynują u olskiego zdania:
`Kierownikiem urzędu jest wójt lub burmistrz.` wychodzi wtedy dwoma zdaniami
składowymi, z których drugim jest `burmistrz`,
a `Statut związku powinien określać uczestników i czas trwania związku.`
dostaje drugie czytanie, w którym zdaniem składowym jest `czas trwania związku`.
Drugie z tych zdań jest jednym z tych, którym ta pozycja odbiera jednoznaczność,
a dwa dalsze — `Przemyśl.` i `Kalisz.` — olski przyjmuje jako rozkaźnik
i pozycja ogólna daje im drugie czytanie, w którym są nazwą miasta.
Cena tej pozycji nie kończy się więc na tej garści zdań:
psuje ona każdy ciąg współrzędny grup imiennych,
a takich ciągów ten rejestr niesie zdanie po zdaniu.

Etykietę roli stawia temu rzeczownikowi produkcja, tak samo jak przy
[czole zdania względnego](#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza),
a czego bez niej brakuje werdyktowi, mówi `olski/subset/deklaracja.py` przy tej roli.

```sh
python3 -m olski.check -c "Mowa o zadaniach." --readings
```

```text
<text>: Mowa o zadaniach.
        - orzeczenie_rzeczownikowe: Mowa, wyrażenie_przyimkowe: o zadaniach → Mowa
```

Rola ta stoi obok orzecznika, a nie jest nim, i rozdziela je rama czasownika.
Orzecznik jest pozycją ramy: rzeczownikowy stoi w narzędniku pod kopulą,
a przymiotnikowy w mianowniku pod czasownikiem, którego rama go ma.
Rzeczownik orzekający nie ma nad sobą czasownika, więc pozycji ramy nie zajmuje,
a wpuszczony do orzecznika stanąłby tam, gdzie orzecznik ramy nie ogłasza:
w szyku z orzecznikiem przed kopulą (`olski/subset/zdanie.py`).
Przyjąłby wtedy `Mowa jest ustawa.`, czyli zdanie,
w którym olski czyta rzeczownikowy orzecznik w mianowniku.

Oba ciała są przy tym potrzebne, i rozstrzyga o tym przyłączenie:
`w ustawie` dochodzi w `Rada wykonuje zadania, o których mowa w ustawie.`
i do `mowa`, i do `wykonuje`, a pierwsze z tych czytań daje ciało zdania składowego,
drugie ciało czoła.
Zdjęte jedno z nich nie odrzuca tego zdania — drugie wyprowadza je samo —
tylko oddaje je jednym czytaniem,
czyli tak, jak wygląda zdanie, o którym gramatyka wybrała przyłączenie
([subset.md](../subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).
Wieloznaczność tego zdania jest więc tym przyłączeniem,
a nie czymkolwiek, co wnosi kopuła opuszczona.

## Zaimki `kto` i `co` wchodzą wszystkimi pozycjami naraz

Morfeusz trzyma te dwa zaimki pod rzeczownikiem,
a przecinek koordynuje w tej gramatyce zdania,
więc bez wykluczenia każde ich użycie ma jeden i ten sam kształt:
zaimek jest podmiotem albo dopełnieniem zdania po przecinku.
`Pyta, kto płaci.` wychodzi wtedy `valid` z czytaniem,
które jest ciągiem dwóch zdań współrzędnych,
czyli którego polszczyzna nie ma.
Jedno czytanie zdania przeczytanego na opak jest werdyktem najgorszym,
jaki ten pomiar wydaje
([corpus.md](../corpus.md#what-morphological-ambiguity-costs)).

Pozycji rzeczownej te dwa lematy dlatego nie mają.
Z tą pozycją jeden napis dostaje dwa wyprowadzenia:
`Kto płaci?` wyprowadza się i pytaniem, i zdaniem oznajmującym
zamkniętym pytajnikiem, a role obu są te same.
Wykluczenie stoi na terminalu głowy grupy imiennej,
a nie w `admissible`, bo czytanie `subst` jest tym,
o które pytają czoła niżej;
tym różni się ono od wykluczenia ze słownika
([warstwa-leksykalna.md](../warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).

Wykluczenie to odbiera pozycję wszystkim użyciom tych zaimków naraz,
a użycie jest w tym rejestrze niejedno.
Dlatego pozycje niżej stoją w gramatyce razem, a nie jedna po drugiej:
pozycja wpuszczona sama zostawia pozostałe bez ani jednego czytania,
a pomiar mówi wtedy o zmianie, że obniża pokrycie,
choć obniża je przez to, że pierwsza pozycja zabiera pozostałym czytanie
nieprawdziwe i nie daje im nic w zamian.

- **Czoło pytania o jednym słowie.**
  `Kto płaci?`, `Pyta, kto płaci.` Grupa pytajna ma dwa ciała:
  zaimek `który` przy rzeczowniku i te dwa zaimki same,
  bo rzeczownika przy sobie nie mają.
  Wyrażenie przyimkowe bierze to czoło osobnym ciałem —
  `Kto z posłów zapisuje ustawienia?` — bo grupy imiennej,
  która by je wzięła, w środku nie ma.
  Przyłączenia tego olski nie wybiera, tak samo jak wszędzie
  ([subset.md](../subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)).
  Przymiotnik za zaimkiem jest ciałem trzecim:
  `Kto pierwszy wstaje od stołu?`, `Kto inny zapisuje ustawienia?`
  Zaimek zgadza się z nim sam, bo rzeczownika przy sobie nie ma.
  Ciało bierze terminal, a nie symbol przydawki, i wyklucza zaimek wskazujący:
  Morfeusz czyta `to` także jako przymiotnik od `ten`,
  więc bez wykluczenia `co to` wychodzi grupą pytajną,
  gdzie polszczyzna ma dwa zaimki obok siebie,
  a `Co to jest?` dostaje drugie czytanie.
  Zakupem jest jedno zdanie banku drzew, ceną zero pod obiema morfologiami,
  a szersze ciało kupowałoby więcej i kupowałoby właśnie tamtym czytaniem,
  więc rozstrzyga tu
  [kierunek](../roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście), a nie pokrycie.
- **Zaimek względny o poprzedniku zaimkowym.**
  `To, co mogło się zepsuć, jest tanie.`,
  `Program zapisuje wszystko, co widzi.`
  Czoło jest osobnym symbolem, a nie drugim ciałem czoła z `który`,
  i rozstrzyga o tym poprzednik: `który` bierze rzeczownik,
  a te dwa zaimka albo całe zdanie
  ([niżej](#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie)).
- **Zdanie względne o poprzedniku zdaniowym.**
  `Cena jest niska, co przekreśla sens działań.`,
  `Bierzemy ostry zakręt, dzięki czemu unikamy zderzenia.`
  Poprzednikiem jest tu zdanie, więc zgodności nie ma z czym sprawdzać,
  a pozycja bierze `co` i nie bierze `kto`, bo tamten jest męskoosobowy.
- **Zdanie względne bez poprzednika w roli podmiotu.**
  `Kto wchodzi w środek, poprzedniego zdania nie przeczytał.`
  Przecinek zamyka ją tak samo jak każde zdanie względne,
  a role jej wnętrza nie są rolami zdania nad nią.
- **Ciąg pytań zależnych pod jednym czasownikiem.**
  `Drzewo mówi, co jest tematem, a co jest nowe.`
  Drugie wypełnienie bierze przy czasowniku sam celownik
  ([walencja.md](../walencja.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)),
  więc pozycję ramy zajmuje ciąg cały,
  a znakiem tego ciągu jest spójnik, a nie sam przecinek
  ([wyżej](#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja)).
- **Orzecznik wysunięty na czoło.** `Czym jest parser?`, `to, czym jest GLR.`
  Rola jest w tych dwóch rodzinach trzecia obok podmiotu i dopełnienia,
  a pozycję ma jedną, bo narzędnika żąda sama kopuła.

Zakup i cena są różnicą wobec gramatyki bez tych pozycji,
a między rejestrami rozchodzą się w tę stronę,
którą [kierunek](../roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście) przewiduje.
Nad prozą tego repozytorium przybywa zdań przyjętych jednoznacznie,
a każde z nich ma w tamtej gramatyce także czytanie ciągu współrzędnego;
kilka zdań dostaje czytanie tam, gdzie tamta nie daje żadnego,
a kilkanaście przechodzi na odrzucone — i tym, co je tam wyprowadza,
jest właśnie ten ciąg; konstrukcję, której im brakuje, nazywa kolejka niżej.
Nad bankiem drzew zakup jest mniejszy, a cena większa,
i tak wychodzi pod jedną morfologią i pod drugą:
kilka zdań, których tamta gramatyka nie wyprowadza, wychodzi przyjętych,
a kilkanaście, które w niej czytanie mają, przechodzi na odrzucone,
więc suma przyjętych spada.
Rozdziela te dwa rejestry poprzednik, a nie częstość:
`, co` niesie tu częściej niż co dwudzieste zdanie,
a w banku drzew rzadziej niż co setne,
tylko że tutaj stoi przed tym zaimkiem `to`, `wszystko` albo `niczego`,
a tam zdanie całe — i to drugie jest tym, czemu wykluczenie zabiera czytanie.

Wykluczenie zostawia po sobie kolejkę konstrukcji, a nie pustą listę,
i stoją na niej te użycia, których czoła nie obejmują:
zaimek stojący nie na czele, czyli drugie pytanie w tym samym zdaniu
(`Kto jest kim?`),
zdanie względne bez poprzednika w roli innej niż podmiot,
oraz przytoczenie samego wyrazu, którym ten rejestr o sobie mówi
(`nikt, kto, nic, coś i ktoś mają u Morfeusza czytanie jedno`).
`todo/` trzyma je wszystkie.

Jedno użycie zostaje na tej kolejce mimo ciała trzeciego i zostaje osobno:
`Co innego jest tanie.` wychodzi przyjęte z `Co innego` w okoliczniku,
bo Morfeusz czyta `co` także jako przyimek,
a przymiotnik za zaimkiem tego czytania nie zdejmuje:
`innego` jest dopełniaczem, więc zgadza się z `co` w dopełniaczu,
a rola, w której to stoi, żąda mianownika.
Przydawka i ten napis są więc dwiema robotami, a nie jedną,
i drugą z nich zamyka wykluczenie po stronie słownika, a nie produkcja.

## Poprzednikiem zaimka `co` jest zaimek albo zdanie

Zaimek `który` zastępuje rzeczownik, a `co` zaimek rzeczowny albo całe zdanie,
i są to trzy różne poprzedniki, nie dwa użycia jednego.
Dopóki oba zaimki miały jedno czoło, rzeczownik dostawał zdanie względne z `co`
wszędzie, gdzie parę cech miał przypadkiem —
`Sejm zaaprobował przekroczenie budżetowe, co przekreśliło sens dalszych działań
Trybunału Stanu.` wychodziło `valid` z jednym czytaniem,
w którym `co` jest przydawką przy `przekroczenie`,
a całe zdanie podrzędne wpada w dopełnienie.
Poprzednikiem jest tam zdanie, więc było to czytanie,
którego polszczyzna nie ma,
a werdykt podawał je z pewnością jednego odczytania.
Nad bankiem drzew wychodziło to w jednym wierszu `disagrees` i nigdzie poza nim,
bo zdanie takie olski przyjmuje, a pokrycie liczy je jak przeczytane
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)).

Czoła są przez to dwa, każde osobnym symbolem,
i nie jest to podział na lematy, tylko na poprzedniki:
czoło z `który` wchodzi pod rzeczownik,
a czoło z `kto` i `co` pod zaimek rzeczowny oraz pod zdanie.
Zdanie względne bez poprzednika idzie tą drugą drogą,
bo tam stoją zaimki, którymi ono się zaczyna;
`który` wyprowadzenia w tej pozycji nie miał i bez tego podziału,
więc przeniesienie jej nic nie zabiera i nic nie kupuje —
gramatyka mówi po nim to, co i przedtem było prawdą.
Poprzednik zaimkowy stoi przy tym w ciele członu grupy imiennej,
a nie nad grupą całą, bo zaimek rzeczowny dopełniacza nie bierze
([grupa-imienna.md](grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)),
więc przydawki przed sobą nie ma i grupy z niego nie ma po co składać.

Zgodności ta pozycja nie sprawdza,
bo poprzednikiem jest zdanie, które liczby ani rodzaju nie ma.
Wypisuje je więc sama, i są to liczba pojedyncza i rodzaj nijaki,
czyli to, co niesie `co`.
Rozdziela to `co` od `kto` bez osobnej cechy —
`kto` jest męskoosobowy, więc tej pozycji nie dosięga,
a `Cena jest niska, kto przekreśla sens.` zostaje odrzucone.
Przyimek przed zaimkiem wchodzi tą samą drogą co przy poprzedniku zaimkowym,
bo niesie go czoło, a nie ta pozycja, więc `dzięki czemu`, `przez co`, `po czym`
i `wobec czego` wychodzą razem z `co` samym.
Pozycje są dwie — nad zdaniem składowym i nad całym ciągiem współrzędnym —
bo poprzednikiem bywa jedno i drugie,
i są to te same dwie pozycje, które ma okolicznik wyrażony zdaniem
([wyżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).

Zakup i cena są nad bankiem drzew tego samego rzędu pod obiema morfologiami,
a cena jest o włos większa.
Zakupem jest garść zdań przechodzących z odrzuconych:
`Bierzemy ostry zakręt, dzięki czemu unikamy zderzenia z ciemnoczerwoną ścianą.`
oraz `Podopieczni Leo Beenhakkera w obecnym sezonie nadzwyczaj skutecznie
gromadzą punkty, dzięki czemu ich przewaga nad rywalami nie podlega dyskusji.`
Ceną jest garść zdań tracących jednoznaczność,
a przeczytane po kolei mówią, skąd ona się bierze:
poza jednym wszystkie są pytaniem zależnym — `Wiem, co zrobię.`,
`Sprawdziłeś, o co cię prosiłem?`, `Wiedzą, co robią.` —
któremu ta pozycja dokłada drugie czytanie,
bo `, co` z pytaniem zależnym dzieli napis co do znaku.
Właścicielem tej ceny nie jest ta pozycja, tylko rama domyślna:
pozycję pytania zależnego daje ona każdemu czasownikowi
([walencja.md](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
więc drugie czytanie wychodzi i tam, gdzie czasownik pytania nie żąda.
Zawężenie tej pozycji do leksykonu trzyma `todo/`,
i ten pomiar jest argumentem za nim.

Drugie czoło kosztuje w produkcjach:
`_wysunięta_rola` wypisuje dla niego wszystkie szyki reszty zdania,
więc gramatyka rośnie o kilka procent,
a liczbę na dziś drukuje kolumna `produkcji` w wydruku sondy luki
([design-notes.md](../design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
Kosztu tego dałoby się uniknąć jednym czołem i cechą przy nim,
mówiącą, który zaimek to czoło niesie,
a odrzuca tę wersję pomiar, nie liczba produkcji:
sonda wycenia pozycję zdjęciem produkcji, więc cena osobna żąda symbolu osobnego.
Pod jednym czołem zdjęcie ciał zabrałoby razem z `co` także `który`,
czyli tę pozycję dałoby się wpuścić, a nie dałoby się jej wycenić.
Odwraca ten wybór jedno: gdy o cenę tej pozycji nikt już nie pyta,
tańsze jest czoło wspólne.

Pod złotą morfologią, czyli tam, gdzie pomiar sięga po drzewo wzorcowe,
złotego czytania nie traci ani jedno zdanie,
a zdanie o przekroczeniu budżetowym, od którego ta sekcja się zaczyna,
przechodzi z wiersza niezgodnych do zgodnych.
Ani jedno zdanie nie traci też tam wyprowadzenia;
pod żywą traci je jedno, i jest to odrzucenie prawdziwsze od trzech czytań:
`Kiedyś zapytałem kierowcę naszego gazika, kim właściwie jest mój przewodnik?`
wyprowadzało się wyłącznie przez `kim` w przydawce przy `kierowcę`,
a pytania z orzecznikiem wysuniętym za przecinkiem ten podzbiór nie ma,
więc jedyne, czego temu zdaniu brakuje, jest tą pozycją, a nie przydawką
([wyżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)
wylicza ją wśród konstrukcji, które zostają w kolejce).
