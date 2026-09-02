# Co widać dopiero na napisie

Przegląd pyta, czy czytelnik odzyska z napisu role.
Obieg pyta, czy z napisu wraca to drzewo, które go wypuściło.
Makieta czyta własne wyjście i mówi, czego ten pakiet o polszczyźnie nie wie.
Chwyt mają wspólny i daje im go kierunek generowania:
formy nie zgaduje się z drzewa, tylko wypisuje się ją i porównuje napisy.

Co do linearyzacji wchodzi, trzyma
[kategorie-zapisu.md](kategorie-zapisu.md),
a niezmiennik obiegu [design-notes.md](design-notes.md#the-round-trip-invariant).

## Drzewo jest jednoznaczne, a napis z niego nie musi być

Drzewo dobrze złożone jest jednoznaczne z definicji,
i [sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
trzyma to jako własność zapisu, którą ten tor dostaje za darmo.
Napis jednoznaczny nie jest, bo przez linearyzację ta własność się nie przenosi:
`Koszt szynki przewyższa koszt bułki.` wychodzi z drzewa, które mówi, co jest większe,
a samo nie mówi tego wcale.
Nie jest to wybór szyku, bo szyk jest tu SVO i innego nie ma —
obie role stoją w formie równej mianownikowi i biernikowi naraz,
a polszczyzna czyta taki ciąg i jako SVO, i jako OVS.
Zgłasza to `olski/skład/przegląd.py`, a ta sekcja mówi, na czym on stoi.

**Liczone jest to z form, a nie z czytań.**
Rola wraca czytelnikowi z dwóch rzeczy: z własnej formy i z czasownika,
więc pyta się o jedno i o drugie.
Czy podmiot brzmi w bierniku tak samo jak w mianowniku,
czy dopełnienie brzmi w mianowniku tak samo jak tam, gdzie stoi,
i czy te dwie role wyciągają z czasownika tę samą formę.
Kiedy wszystkie trzy odpowiedzi są twierdzące, zamiana ról nie zmienia napisu,
i wtedy zdanie nie mówi, która rola jest którą.
Odpowiedzi biorą się z linearyzacji, bo wszystkie trzy są formami,
a form skład nie zgaduje: wypisuje rolę drugi raz i porównuje napisy.

**Z form, które w tekście stanęły**, a nie z tych, które to zdanie miałoby samo.
Jedno drzewo wychodzi dwoma napisami, zależnie od miejsca, w którym się je wypisuje,
a rozstrzyga o tym `Kontekst`: zdanie o tej samej postaci co zdanie obok
podmiotu nie wypisuje, a zdanie wskazujące rzecz mówi o niej zaimkiem.
Zdanie dostaje więc do pomiaru ten kontekst, którym linearyzacja je składała,
i liczy się go tą samą drogą, bo druga mierzyłaby tekst,
którego ten kompilator nie wypuścił.
Zmienia to obie odpowiedzi i w obie strony.
`Czeladnik zasłania sień, którą klucz zamyka.` ról nie miesza,
bo `którą` różni się od `która`, choć `sień` od siebie samej się nie różni,
a policzone z samej grupy imiennej dałoby tu zgłoszenie o wadzie,
której w napisie nie ma.
`Zamykała sień.` postawione po zdaniu o córce krawca ról nie oddaje,
choć to samo zdanie napisane osobno oddaje je swoim podmiotem.

Pytań zostaje wtedy dwa, bo pierwsze z trzech wyżej dotyczy formy podmiotu,
a podmiot opuszczony żadnej swojej formy czytelnikowi nie pokazuje.
Oba, które zostają, mierzą to, co widać: formę, którą uczestnik stanął,
oraz formę czasownika, bo z niej właśnie czytelnik opuszczony podmiot odzyskuje.
Zgłoszenie niesie przez to jeden napis zamiast dwóch —
podmiot dopisany do niego byłby formą wziętą z drzewa,
czyli dokładnie tym, czego ten przegląd nie mierzy.

To jest ten sam pomiar, który stoi w `pomijalny`, i warto to nazwać.
Tamten pyta, czy podmiot wróci czytelnikowi z formy czasownika,
i liczy to, wypisując tę formę dla każdego, kto mógłby ją z niego wyciągnąć.
Tutaj pytanie jest o rolę zamiast o podmiot, a sposób jest ten sam.
Kierunek generowania oddaje to za darmo, jak zapowiada początek tego dokumentu:
parser widzi formy i musi z nich odgadnąć strukturę,
a skład ma strukturę i formy liczy z niej.

**Zgłasza, a nie odmawia**, i przesądza o tym rodzaj porażki.
Skład rozdziela dziś trzy.
Drzewa, którego nie ma, nie da się zbudować i mówi o tym `PozaRamą`;
formy, której nie ma, nie da się wypisać i mówi o tym `BrakFormy`;
a tu drzewo jest dobre i forma jest dobra, tylko czytelnik nie odzyska ról.
`pomijalny` jest tu starszym przykładem tego trzeciego rodzaju
i on wyznacza posturę: kiedy podmiotu nie da się odzyskać, wypisuje podmiot,
zamiast cokolwiek odrzucać.
Tam, gdzie bezpieczną powierzchnię da się policzyć, liczy ją linearyzacja,
a przegląd bierze te miejsca, dla których polszczyzna wyjścia nie ma.

Za zgłoszeniem zamiast odmowy stoi drugi powód i jest on mocniejszy.
Czytań policzonych nad zdaniem czytelnik nie ma tyle samo,
a `Program zapisuje plik.` czyta on raz, choć formalnie stoją tam dwa:
o tym, co się z czym rozjeżdża, mówi
[jednoznaczność prefiksu](open-questions.md#czy-jednoznaczność-prefiksu-mierzy-czytelność),
i to ona jest właścicielem tego wywodu.
Odmowa odbierałaby więc autorowi zdania, których nikt poza pomiarem nie czyta dwojako,
a raport zostawia mu je wraz z powodem.

**Gramatyki przegląd nie woła i nie potrzebuje.**
Parser jest tu [świadkiem, a nie zależnością](design-notes.md#the-round-trip-invariant),
a check postawiony na liczbie czytań milczałby tam, gdzie kończy się podzbiór:
legenda o bazyliszku ma zdania, których gramatyka nie wyprowadza,
więc to pokrycie olskiego rozstrzygałoby, o których zdaniach przegląd się wypowie.
Nie woła też `harness/wieloznaczność.py`, który tę samą klasę liczy nad tekstem,
i to jest różnica warta zapisania, bo pokazuje, co ten kierunek daje.
Tamten moduł musi zgadywać z form to, co tutaj wiadomo z drzewa:
gdzie kończy się grupa imienna, co jest uczestnikiem, a co stoi pod przyimkiem,
i przy którym orzeczeniu para stanęła — i sam nazywa przez to swoją liczbę
górnym oszacowaniem.
Tutaj żadne z tych pytań nie pada.

Poprawiło to raz tamten pomiar, i tak wygląda ta wymiana w praktyce.
`Mysz goni ogon.` czyta się dwojako,
a synkretyzm liczony z jednego czytania słownika tej pary nie widzi,
bo `mysz` niesie mianownik i biernik dwoma osobnymi wpisami,
podczas gdy `ogon` niesie oba jednym.
Porównanie napisów o wpisy nie pyta i widzi ją bez żadnego warunku,
więc `_obojętny` w tamtym module pyta dziś o segment, a nie o czytanie.
Że obie strony widzą tę parę, sprawdza `tests/test_przegląd.py`.
Skład jest tu zatem świadkiem dla parsera, a nie odwrotnie,
co jest tą samą wymianą, którą zapowiada
[niezmiennik obiegu](design-notes.md#the-round-trip-invariant):
generowanie pokazuje, czego druga strona nie widzi.

Ile przegląd zgłasza, widać na tekście, którego nikt pod niego nie pisał:
nad legendą o bazyliszku nie zgłasza nic,
a przyczyną jest czas, w którym ta opowieść stoi.
Czas przeszły niesie w polszczyźnie rodzaj, a teraźniejszy nie niesie żadnego,
więc `Kufer zasłaniał lustro.` ma role przypięte,
a `Kufer zasłania lustro.` nie ma ich wcale.
Rodzaj przypina je także tam, gdzie podmiot z tekstu wypadł,
i to on jest powodem, dla którego opuszczenia tej legendy nic nie kosztują.
Trzyma to `tests/test_przegląd.py` i trzyma mimo swojej zerowej liczby,
bo liczba ta jest tu odpowiedzią, a nie brakiem przypadków.

Klasa jest jedna z dwóch, które ta wieloznaczność ma nad polszczyzną.
Przyłączenia przegląd nie zgłasza,
bo o wyrażeniu przyimkowym drzewo mówi to, czego przy rolach nie mówi:
okolicznik dochodzi w nim do zdarzenia zawsze,
więc każde takie miejsce byłoby trafieniem,
a raport zgłaszający każde zdanie z przyimkiem nie oddziela niczego od niczego.
Czym to zawęzić, trzyma [`todo/`](../todo/README.md).

## Czytanie parsera wraca drzewem, a jedno czytanie kilkoma

Niezmiennik obiegu żąda, żeby drzewo puszczone w tekst wróciło z tekstu drzewem,
a [design-notes.md](design-notes.md#the-round-trip-invariant) trzyma jego postać:
drzewo do napisu jest funkcją, napis do drzewa relacją,
więc żąda się przynależności, a nie równości.
Robi to `olski/skład/rozbiór.py`, a ta sekcja mówi, na czym on stoi.

Odwrotnością linearyzacji ten kierunek nie jest, bo oba tory stoją na dwóch poziomach.
Parser wydaje wyprowadzenie nad symbolami gramatyki wraz z formami i ich cechami,
a autor pisze kategorie dziedziny, w których przypadka nie ma,
bo bierze się on z pozycji.
Wspólny mają więc typ, a nie kod, i jest to druga funkcja,
a nie ta sama przebiegnięta wstecz.
Stoi ona w `olski/skład/`, bo zależność biegnie tu w jedną stronę:
skład czyta olskiego, a linter o kompilatorze nie wie nic i nie ma wiedzieć.

**Rozstrzyga o tym linearyzacja, a nie rozbiór.**
Drzewo wychodzi stamtąd tylko wtedy, gdy wypisane daje te formy,
z których je przeczytano, więc mówi napisem to, co przeczytano, i nie ma jak skłamać.
Zdejmuje to z tego pliku drugą kopię tego, co kompilator wie o szyku i o formach,
a płaci wypisaniem kandydatów, czyli tym, co skład i tak robi.
Jest to ten sam chwyt, którym mierzy
[przegląd](#drzewo-jest-jednoznaczne-a-napis-z-niego-nie-musi-być):
formy nie zgaduje się z drzewa, tylko wypisuje się je i porównuje.

**Jedno czytanie wraca kilkoma drzewami**, a mnoży je to, o czym napis milczy.
Relacja okolicznika jest kategorią dziedziny, a w napisie stoi przyimek,
więc `w piwnicy` wraca i relacją miejsca, i relacją czasu,
a relacją celu nie wraca, bo ta żąda biernika, którego w napisie nie ma.
Znacznik tematu jest drugą taką rzeczą: postawiony tam,
gdzie konstytuent i tak stoi, nie przestawia niczego,
a jest tym, co autor napisał.
Trzecią jest pozycja, którą grupa imienna zajmuje w ramie:
gramatyka nazywa dopełnieniem i biernik, i celownik,
a przypadka rozbiór nie czyta, więc jedna grupa wraca w obu pozycjach naraz
i odsiewa je dopiero wypisanie.
Odpowiedzią jest więc lista drzew, a nie wybór między nimi,
bo wybierać musiałby ranking, a czy go budować,
trzyma [`open-questions.md`](open-questions.md#the-round-trip-guarantee)
jako pytanie otwarte.

**Wartości bierze się z formy, a nie z wyprowadzenia, które zostało**,
i żąda tego czytanie samo.
Czytanie parsera jest swoim kształtem, a lematy i wartości cech
są z niego wyłączone rozmyślnie, o czym mówi `signature` w `olski/parse/czytanie.py`,
więc dwa wyprowadzenia różniące się lematem są jednym czytaniem
i to, które z nich w nim stoi, rozstrzygnęła kolejność.
`Kot mieszka w piwnicy.` pokazuje cenę, jaką by to miało:
w czytaniu, które zostaje, `Kot` jest nazwiskiem rodzaju żeńskiego,
więc rozbiór czytający lemat z liścia wydałby drzewo o kimś innym,
a liczby nie wydałby wcale.
Pytana jest zatem krawędź grafu segmentacji, czyli wszystkie czytania formy,
a zdanie to wraca oboma drzewami.
Jest to jedno miejsce, w którym pojęcie jednego czytania po tamtej stronie
jest grubsze niż to, czego ten zapis potrzebuje,
i płaci się za to wyliczaniem, a nie zmianą tamtego pojęcia:
lemat wpuszczony do sygnatury czytania odrzuciłby prawie całą polszczyznę,
i mówi to tamten docstring wprost.

Przeczenie napis niesie osobnym słowem, a to słowo zajmuje pozycję czasownika,
więc pozycję tę czyta się całym ciałem:
gramatyka stawia `nie` przed formą, a lemat, o który tu chodzi, idzie za nim.
Dopełniacza negacji nie ma przy tym czego czytać, bo rozstrzyga o nim linearyzacja:
przypadka ten plik nie czyta wcale, więc `Kot nie widzi myszy.`
wraca drzewem, które ten przypadek liczy dopiero przy wypisaniu.

Zdanie wypełniające pozycję ramy wraca dwiema drogami, a dzieli je podmiot.
Treść ma go wypisanego, więc wraca z samego napisu jak każdy inny konstytuent.
Bezokolicznik nie ma go wcale i nie ma skąd wziąć,
bo ani osoby, ani rodzaju ta forma nie niesie,
więc zdanie pod tą pozycją powstaje po podmiocie zdania nad nim, a nie przed nim.
Jest to ta sama droga, którą wraca podmiot opuszczony w następstwie zdarzeń.

Rozjazd między kierunkami widać przy tym na obiegu i nigdzie więcej,
bo osobno każdy z nich ma tylko własne zdanie i nie ma go z czym porównać.
O bezokolicznik gramatyka nie pyta wcale, bo pozycję na niego niesie
każda klasa walencyjna prócz kopuli, a skład pyta o niego leksykon;
`olski/walencja.py` nazywa to zdaniem leksykonu czytanym przez jeden kierunek.
`Linter pomaga pisać dobry kod.` stoi przez to w komentarzu `olski/subset/zdanie.py`
jako przykład ciał produkcji `wypełnienia` i ze składu nie wychodzi wcale,
bo `pomagać` bezokolicznika w tym leksykonie nie bierze.
Który z dwóch mówi tu prawdę, pyta [`todo/`](../todo/README.md).

Odpowiedź pusta jest odpowiedzią i ma trzy przyczyny, z których jedna jest brakiem.
Zaimka, orzecznika przymiotnego, zdania bez podmiotu,
cząstki, spójnika na czele zdania,
okoliczności przy orzeczeniu imiennym
oraz wyrażenia przyimkowego pod grupą imienną ten zapis nie ma czym powiedzieć.
Przymiotnik po rzeczowniku kategorię ma, a wraca z niej inny szyk,
bo `Jaki` stawia go przed rzeczownikiem zawsze,
i to jest ta [dziura wewnątrz grupy imiennej](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
zmierzona z drugiej strony: `zwykły tekst polski` z README nie wraca niczym.
Leksem jest trzecią, bo nazwa w drzewie jest nazwą, którą wybrał autor,
a rozbiór stawia lemat, więc `Rosół ma oka.` nie wraca:
goła nazwa `oko` znaczy w tym repozytorium oko.

Jak często który z tych braków pada, mierzy `harness/znaczenia.py` nad rejestrem.
Nad bankiem drzew zdanie, które olski melduje jako wieloznaczne,
nie wraca żadnym drzewem prawie zawsze,
a przed pozostałymi brakami stoi wyrażenie przyimkowe pod grupą imienną,
czyli ten jeden, który jest tu rozstrzygnięciem, a nie dziurą.
Po co ten pomiar wzięto i co mówi o warstwach, mówi
[architecture.md](architecture.md#werdykt-liczy-wyprowadzenia-bo-powstaje-pod-dwiema-warstwami-które-liczą-znaczenia).

Pustą odpowiedzią jest tak samo kształt ciała, dla którego kategorii nie ma,
i jest to żądanie postawione temu plikowi, a nie własność, którą ma za darmo.
Gramatyka dopisuje ciała symbolom, które rozbiór czyta,
a ciało rozpakowane do zmiennych, których nie opisuje,
kończy się wyjątkiem Pythona, czyli brakiem kategorii udającym usterkę rozbioru.
Dlatego grupa imienna i zdanie złożone dopasowują całe ciało,
tak samo jak robi to `_nominalne`,
a zdanie względne pod grupą imienną jest tym ciałem, na którym to widać.
Pozycja bez ani jednego kandydata żąda tego samego z drugiej strony:
zdanie w rozkaźniku nie ma czasownika, którego ten zapis wypisuje,
więc bez zgłoszenia wygaszałoby iloczyn kandydatów i wracało samą pustką.

Która z tych przyczyn zadziałała, mówi sama odpowiedź, a nie ta lista.
`Odczyt` w `olski/skład/rozbiór.py` wraca z drzewami i z powodami tego,
co po drodze odpadło, a powód powstaje tam, gdzie kandydat odpada:
zgłoszeniem, gdy brakuje kategorii, komunikatem morfologii, gdy brakuje formy,
odmową ramy, gdy leksykon nie daje czasownikowi pozycji, którą kandydat zajął,
i napisem, który wyszedł, gdy wyszedł inny.
Pyta o to samo, co `explain` w `olski/werdykt.py` po tamtej stronie,
i jest potrzebne z tego samego powodu:
lista wylicza przyczyny, a nie mówi, na którą trafiło to jedno zdanie.
Rozdziela ona przy tym dwie pustki, których nazwać inaczej nie ma czym,
i o to rozdzielenie prosi też `tests/test_rozbiór.py`,
stawiając werdykt gramatyki obok każdego zdania, którego ten kierunek nie mówi:
zdanie bez czytań wraca powodem o olskim, a nie o brakującej tu kategorii.

Tożsamość wraca stamtąd, gdzie napis ją niesie, i tylko stamtąd.
Niesie ją opuszczony podmiot, czyli to, czego w zdaniu nie ma,
więc wewnątrz jednego zdania rozbiór wie, że dwa zdarzenia mówią o jednej rzeczy,
i wypuszcza `Postać`, żeby ten sam napis z tego drzewa wyszedł.
Między zdaniami nie niesie jej nic i wtedy dwa wystąpienia lematu
wracają jako dwie rzeczy, co jest tą samą granicą,
którą [`Postać`](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)
zapisuje po drugiej stronie:
tożsamość deklaruje autor.
Dlatego porównanie stoi na `sygnatura`, a nie na równości drzew,
i jest ono odpowiednikiem `signature` z `olski/parse/czytanie.py`,
czyli mówi, co czyni dwa drzewa tego zapisu jednym drzewem.
Różnica jest jedna i jest nią właśnie tożsamość:
wychodzi ona numerem nadanym po kolei, a nie obiektem,
bo drzewo zbudowane z napisu nie ma jak dzielić obiektów z tym,
z którego ten napis wyszedł.

Kryteria tożsamości są przy tym dwa, bo pytania są dwa.
Obok `sygnatura` stoi `znaczenie`, które pyta o jedno zdanie logiczne,
a nie o jedno drzewo, i zdejmuje w tym celu znacznik tematu:
`Celem jest parser.` i `Parser jest celem.` wychodzą pod nim równe.
Obieg zostaje przy sygnaturze, bo żąda z powrotem tego drzewa,
które napis wypuściło, a nie tego samego zdania logicznego.
Czy łącznik `to` schodzi tą samą drogą co znacznik,
nie rozstrzygnięto, i trzyma to [`todo/`](../todo/README.md).

`harness/znaczenia.py` zostaje przy sygnaturze i jest to pomiar, a nie przeoczenie.
Przestawiona na drugie kryterium nie rusza ani jednego werdyktu,
i mówią to wszystkie zdania, którym pytanie to daje się dziś postawić,
pod obiema morfologiami banku drzew i nad prozą tego repozytorium.
Znacznik tematu pada bowiem pod każdym czytaniem tak samo,
więc zbiory drzew dzielą go i bez tego kryterium.

Przyłączenie widać na tym obiegu tak, jak je ten zapis rozstrzyga.
`Program zapisuje ustawienia w repozytorium.` czyta się w olskim dwojako,
bo wyrażenie przyimkowe dochodzi i do zdarzenia, i do rzeczy,
a wraca z tego jedno czytanie, bo do rzeczy nie ma tu czym dojść.
Jest to ta sama własność drzewa, na której stoi
[przegląd](#drzewo-jest-jednoznaczne-a-napis-z-niego-nie-musi-być),
kiedy przyłączenia nie zgłasza.

## Tekst losowany żąda tego, czego autor nie musiał napisać

Makieta żąda tekstu, zanim ktokolwiek ma co powiedzieć,
i dostaje zwykle łacińską sieczkę, po której nie widać, jak wygląda polska kolumna:
polskie słowo jest dłuższe, odmienia się i przez to inaczej łamie wiersz.
Ten kierunek wypuszcza taki tekst za darmo i dlatego `olski/skład/makieta.py` powstał:
gramatyczności nie ma czym naruszyć, bo zgodność jest tu policzona, a nie sprawdzona,
więc losuje się drzewo, a nie napis, i nie ma czego odsiewać po fakcie.
Generator postawiony nad parserem musiałby wypuścić zdanie, przeczytać je i odrzucić,
czyli oprzeć się na werdykcie, którego olski nad polszczyzną spoza podzbioru nie wydaje.

Odsianie jest jedno i pyta o nie [przegląd](#drzewo-jest-jednoznaczne-a-napis-z-niego-nie-musi-być),
czyli to samo zgłoszenie, które autorowi zostawia decyzję.
Losowanie decyzji nie ma czym podjąć, więc zdanie zgłoszone wraca do puli.
Kosztuje to niewiele i mówi o polszczyźnie coś, czego legenda nie pokazała:
osoba podmiotem stojąca kolizji nie zrobi,
bo biernik rzeczownika osobowego równa się dopełniaczowi, a nie mianownikowi.
Wraca ta klasa wraz z rzeczą postawioną w tej roli — `Zegar zasłonił kufer.` —
a rzecz w obsadzie jest, bo `Świeca zgasła.` jest zdaniem, którego makieta potrzebuje.

Pyta się przy tym o zdanie stojące za poprzednim, a nie o zdanie stojące samo,
i tego żąda opuszczanie podmiotu, którego makieta używa dla rytmu.
Po `Kowal zasnął.` zdanie o tym samym kowalu wychodzi samym `Wziął nóż.`,
gdzie nie widać już, czy nóż jest podmiotem, czy dopełnieniem,
a osoba, którą obrona wyżej się tłumaczy, żadnej swojej formy tam nie pokazuje.
Odsiew pyta więc o to, co akapit z tego zdania złoży,
i o opuszczenie pyta ten sam `pomijalny`, którego zapyta za chwilę akapit,
bo dwa warunki na jedno opuszczenie odsiewałyby jeden tekst, a składały drugi.

Ustaleniem tej sekcji jest jednak co innego,
i wychodzi ono z różnicy między tekstem losowanym a napisanym.
Autor pisze `w izbie` i `na rynku`, nie zauważając, że wybrał,
bo wybór ten robi za niego polszczyzna, którą zna;
losowanie musi ten wybór podjąć i dopiero wtedy widać,
że w tym pakiecie nie ma go z czego wziąć.
Wyszła z tego lista faktów o polszczyźnie, których nie niesie tu żaden leksykon,
a każdy z nich wypuszcza z drzewa napis poprawny gramatycznie i nieistniejący.

Przyimek miejsca zależy od rzeczownika, a nie od relacji:
`w izbie` obok `na rynku`, więc `w ulicy` i `na izbie` wychodzą stąd tak samo dobrze.
Aspekt bezokolicznika zależy od czasownika nad nim,
więc `zaczął zapłakać` przechodzi przez ramę, której `zacząć` żąda, i zdaniem nie jest.
Postać zgłoskotwórcza przyimka zależy od tego, co po nim stoi,
więc `z strychu` wychodzi tam, gdzie polszczyzna mówi `ze strychu`.
Przymiotnik dzieli się na te, którymi opisuje się rzecz, i te, którymi opisuje się człowieka,
więc `pusta wdowa` zgadza się rodzajem, liczbą i przypadkiem, a mówi o człowieku to,
co mówi się o suknie.
Rama czasownika sięga dalej niż pozycje, o które pyta `Robi`,
bo wyrażenia przyimkowego nie ma wśród nich ani jednego,
więc `czekał na izbach` czyta się przez `czekać na kogoś`,
a nie jako okoliczność miejsca, którą autor drzewa tam postawił.

Rozstrzygają je wszystkie tabele `olski/skład/makieta.py`, przez wpis albo przez pominięcie,
czyli miejsce, które leksykonem nie jest i nim nie będzie:
tabela wymienia lematy, których ten jeden program używa,
a fakt o przyimku dotyczy każdego drzewa, jakie ktokolwiek napisze.
Każdy z nich prócz jednego ma przez to wpis w [`todo/`](../todo/README.md),
a przymiotnik go nie ma i nie ma mieć:
o tym, którym przymiotnikiem opisuje się człowieka, nie rozstrzyga ani forma,
ani rama, ani czytanie, więc nie ma go gdzie zapisać jako faktu o polszczyźnie.
Losowanie jest przez to tanią sondą nad tym, czego ten pakiet o polszczyźnie nie wie:
wystarcza jej przeczytać własne wyjście.

Rytm jest w tej makiecie wyborem, bo makieta pokazuje właśnie go.
Tekst złożony ze zdań jednego kształtu ma usterkę,
którą [fiction.md](fiction.md#sentence-and-paragraph) wylicza jako jednostajność,
więc kształt zdania jest losowany razem z lematami
i ten sam nie wypada dwa razy pod rząd.
Kształty te wyczerpują przy tym kategorie, które ten zapis niesie,
i to jest drugie żądanie, osobne od rytmu:
makieta pokazuje, co kompilator umie, więc kategoria pominięta w niej jest długiem.
Trzyma to `tests/test_makieta.py`, bo po samym tekście takiego długu nie widać —
tak wypadł dopełniacz, którego nie wystawiał żaden kształt,
choć `Czyj` w składni jest od początku.
Obsadę akapitu niosą `Postać`, bo dopiero one pozwalają opuścić podmiot,
i to jest ta sama rzecz, którą
[tekst wie ponad zdaniem](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie),
widziana od strony programu:
zdania powstają tu osobno i nic o sobie nie wiedzą,
a tekst wychodzi z nich akapitem, bo tożsamość jest zadeklarowana raz, przed nimi.
