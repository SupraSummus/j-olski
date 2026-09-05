# Zdanie złożone współrzędnie: spójnik i interpunkcja

Jeden plik rejestru konstrukcji, w którym sekcja przypada na konstrukcję.
Cena i zakup stoją w niej rzędem wielkości albo granicą.
Co ten rejestr obiecuje i który plik czytać, mówi [wstęp](README.md).

## Spójnik skorelowany powtarza się przed każdym członem

`Ani parser nie rośnie, ani linter nie sprawdza.`,
`Ani parser, ani linter nie rośnie.`
Polszczyzna stawia tu spójnik dwa razy, po jednym przed każdym członem,
i przed drugim żąda przecinka,
gdzie koordynacja zwykła stawia go raz i między członami
([grupa-imienna.md](grupa-imienna.md#nothing-above-a-coordination-distributes-into-it)).
Ciało jest przez to trzecie na swoim poziomie, a nie drugą listą lematów.

Poziomy są trzy i każdy zmierzono osobno, bo cena każdego jest osobną liczbą.
Weszły dwa.
Poziom zdaniowy i imienny wyciągają razem kilka zdań banku drzew z odrzucenia,
a każde z nich zgadza się z drzewem wzorcowym;
nad prozą tego repozytorium kilka zdań dostaje czytanie, nie dostając
jednoznaczności, i są to zdania długie, wieloznaczne z innych powodów.
Jednoznaczności nie traci ani jedno zdanie w żadnym z tych dwóch przebiegów.
Poziom przymiotnikowy — `Plik jest ani nowy, ani duży.` —
nie kupuje ani jednego zdania w żadnym z nich, więc nie wchodzi.

Liczba idzie na poziomie imiennym z członu, a nie wartością `pl`,
i tym ten ciąg różni się od koordynacji zwykłej:
`Ani parser, ani linter nie rośnie.` orzeka w liczbie pojedynczej,
bo przeczenie rozdziela człony, zamiast je sumować,
a `Ani parsery, ani lintery nie rosną.` wychodzi z tego samego ciała mnogie,
bo mnogie są człony.

Z lematów zostało samo `ani`, choć polszczyzna powtarza tak również `i` oraz `czy`.
Oba zmierzono i oba wypadły, każde z innego powodu.

`i` wypada na napisie, którego polszczyzna nie ma.
Jego zakup jest sam w sobie dodatni: kilka zdań banku drzew dostaje czytanie,
a jednoznaczności nie traci żadne.
Terminal wpuszcza jednak spójnik na czoło członu, czyli wszędzie tam,
gdzie człon może się zacząć,
więc `Cena rośnie, i linter sprawdza tekst.` przestaje zatrzymywać analizę na `i`,
a przecinka przed tym spójnikiem polszczyzna nie stawia
([niżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
Zdanie zostaje odrzucone tak samo, a analiza idzie w nim dalej, niż napis pozwala,
i schodzi ono przy tym z wiersza `conj` kolejki blokerów
do wiersza zdań bez struktury nad całością
([corpus.md](../corpus.md#where-the-analyses-stop)).

`czy` wypada na drugim wyprowadzeniu jednego kształtu.
Nad bankiem drzew nie rusza ani jednego zdania,
a nad prozą tego repozytorium daje czytanie dwóm,
tyle że tym samym czytaniem, którym pytanie zależne alternatywne
staje się ciągiem dwóch zdań oznajmujących:
`Pyta, czy rośnie, czy maleje.` dostaje trzecie czytanie tam,
gdzie ciąg pytań zależnych ma już swoje
([podrzędność.md](podrzędność.md#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą)).
`ani` żadnej z tych dwóch rzeczy nie robi, bo nie licencjonuje go dziś nic.

Pary lematów gramatyka nie wymusza, bo terminal lematu nie wypuszcza,
a przy jednym lemacie na liście nie ma czego mieszać.
Lemat dopisany do niej wymusiłby parę dopiero ciałem na lemat,
czyli tyloma ciałami na poziom, ile lematów, i tej ceny nikt nie policzył.

## Interpunkcja zdaniowa spina zdania, które już się wyprowadzają

Polszczyzna łączy dwa zdania spójnikiem, przecinkiem albo jednym i drugim naraz,
dwukropkiem wprowadza wyjaśnienie, a średnikiem rozdziela to, co spina treść.
Wiersz `interp` prowadzi kolejkę blokerów i liczy w niej tysiące zdań
([corpus.md](../corpus.md#where-the-analyses-stop)).

Nowego kształtu zdania ta konstrukcja nie wymaga,
bo jej członami są zdania, które gramatyka wyprowadza i bez niej.
Wymaga natomiast trzech rozstrzygnięć, po jednym na znak.

**Dwukropek rozdziela zdanie wyżej niż przecinek.**
Przed dwukropkiem jest teza, a za nim całe jej wyjaśnienie,
więc `A, B: C.` polszczyzna czyta jako `(A, B): C`,
a produkcja należy przez to do zdania, a nie do zdania składowego.
Werdykt pokazuje ten podział streszczeniem na każde zdanie składowe,
tak samo jak przy koordynacji przecinkiem,
bo w jednym i w drugim zdanie składowe obsadza role własnym materiałem.

Jednoznaczności ta produkcja nie odbiera ani jednemu zdaniu,
a wynika to z gramatyki, nie z przebiegu:
dwukropka nie bierze żaden inny terminal.
Pilnuje tego zera `tests/test_zdanie_złożone.py`,
i pilnuje go warunkiem, a nie liczbą ciał:
symbole stojące za dwukropkiem mają być rozłączne,
więc napis wzięty jednym nie ma wyprowadzenia pozostałymi.

**Za dwukropkiem stoi zdanie, grupa imienna albo pytanie zależne.**
`Gramatyka ma dwie role: podmiot i dopełnienie.` wylicza za dwukropkiem to,
co zdanie przed nim nazwało liczbą albo terminem,
a `Sprawdzasz to jednym pytaniem: czy skreślona rzecz jest powiedziana gdzie
indziej?` stawia za nim pytanie, które zdanie przed dwukropkiem zapowiedziało.
Symbole te są rozłączne: grupa imienna zdaniem nie jest,
a zdanie składowe nie zaczyna się ani od `czy`,
ani od zaimka, który pozycji rzeczownej nie dostał
([podrzędność.md](podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Rolą jest cała ta grupa, tak samo jak przy wtrąceniu w nawiasie,
i tyle właśnie werdykt o niej mówi:
do którego składnika zdania ona się odnosi, gramatyka nie rozstrzyga,
i jest to ta sama odmowa, którą wydaje o członie bez czasownika
([niżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).

Obie pozycje kupują pojedyncze zdania tej prozy: konstrukcje są częste,
lecz zdania, które je niosą, potykają się jeszcze o co innego.
Pytanie zależne rozdziela przy tym dwa rejestry.
Nad bankiem drzew nie rusza ani jednego zdania, pod żadną z dwóch morfologii,
a nad prozą tego repozytorium przyjmuje kilka zdań i kilku dokłada czytanie:
jest to konstrukcja rejestru docelowego.
Kolejka blokerów nazwy jej nie podsuwa,
bo zdanie z takim dwukropkiem staje dopiero na swoim końcu
i wpada do wiersza zdań bez struktury nad całością,
czyli do tego jednego, który konstrukcji nie nazywa
([roadmap.md](../roadmap.md#kolejkę-ustawia-korpus-usterek-a-nie-kolejka-blokerów)).
Jedno zdanie tej prozy przechodzi przy tym z przyjętego na wieloznaczne,
i jest to zysk, a nie cena:
`Rozdziela tę tradycję jedno pytanie: co autor podaje na wejściu.`
wyprowadzało się dotąd przez przyimkowe czytanie formy `co`,
czyli czytaniem, którego nikt nie ma,
a teraz stoi obok niego to, które ma czytelnik
([podrzędność.md](podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).

**Średnik rozdziela tak samo jak dwukropek i tak samo nie kosztuje nic.**
`Program zapisuje ustawienia; cena jest niska.` wyprowadza się ciałem
`wypowiedzenie → zdanie ; zdanie .`, czyli tym samym, tylko z drugim znakiem,
a cena jest i tu zerowa z gramatyki: średnika nie bierze żaden inny terminal.

Za tym znakiem stoi rejestr, a nie polszczyzna.
Średnik stoi tam, gdzie stanąłby przecinek albo kropka,
więc produkcja nie mówi nic, czego nie mówi dwukropkowa,
a przemawia za nią to, że ten rejestr średnika używa:
zdania z nim stoją w tych dokumentach i w ustawach.

**Myślnik rozdziela tym samym ciałem, a bierze dwa znaki z trzech.**
`Cena jest niska — gramatyka jest bezkontekstowa.` wychodzi tak samo jak zdanie
z dwukropkiem, a warunek na lemat bierze pauzę i półpauzę, czyli te dwa znaki,
którymi polszczyzna myślnik pisze.
Łącznika ten warunek nie bierze, bo łącznik spaja wewnątrz wyrazu — `UTF-8`,
`16-latków` — i to jest tu cena, a nie oszczędność:
zdanie, które myślnik pisze łącznikiem, zostaje odrzucone.

Drugiego znaku rozdzielającego zdanie nie bierze — ani dwóch średników, ani
średnika razem z dwukropkiem — bo `zdanie` żadnego z nich nie ma, więc rekurencji
nie ma czym zbudować. Granica ta jest wypowiedziana, a nie przeoczona, i zostaje
[subset.md](../subset.md#what-it-does-not-cover-yet).
Dwa myślniki w jednym zdaniu są przy tym konstrukcją inną, a nie tą granicą:
para obejmuje wtrącenie, zamiast rozdzielać dwa zdania,
i ma [własną sekcję](#para-myślników-obejmuje-wtrącenie-w-środku-zdania-a-nawias-na-jego-końcu).
Zerowej ceny z gramatyki myślnik przez to nie ma,
bo stoi w czterech ciałach zamiast w jednym,
a rozdziela je liczba znaków: rozdzielające bierze jeden myślnik, para bierze dwa.
Zdanie z dwoma znakami ma stąd wyprowadzenie jedno,
bo rozdzielające żąda zdania za sobą, a zdanie drugiego myślnika nie ma.
Zero jest tu więc liczbą z pomiaru, a nie z gramatyki:
ani nad tą prozą, ani nad bankiem drzew nie traci jednoznaczności ani jedno zdanie.

**Przecinek przed spójnikiem jest faktem o słowie.**
`Plany są niczym, ale planowanie jest wszystkim.` przecinka wymaga,
a `Program zapisuje ustawienia i linter sprawdza tekst.` nie bierze go wcale,
i rozstrzyga o tym sam spójnik, a nie miejsce, w którym pada.
Spójnik zdaniowy rozdziela się przez to na dwie klasy, które się nie zachodzą.
Klasa bez przecinka wyklucza ponadto cząstkę przeczącą, i to jest to samo
wykluczenie o jeden lemat szersze: Morfeusz czyta `nie` także jako spójnik,
a gramatyka ma dla tej formy pozycję przy czasowniku,
więc bez tego warunku `Zgodności ta pozycja nie ma i mieć nie może.`
wychodzi dwoma zdaniami spiętymi przez `nie`.
Warunek zabiera pojedyncze zdania tej prozy i każde z nich wyprowadzało się
właśnie tak, czyli czytaniem, którego polszczyzna nie ma.
Klasa z przecinkiem jest zamkniętą listą.
`zaś` i `jednak` na niej nie figurują, bo czoła swojego zdania nie zajmują:
polszczyzna stawia je za pierwszym wyrazem — `linter zaś sprawdza tekst` —
i jest to ten sam warunek, którym lista spójników okolicznikowych wyklucza `bowiem`
([podrzędność.md](podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).
Te trzy lematy bierze pozycja wewnątrz zdania i ona jedna
([niżej](#spójnik-wewnątrz-zdania-ma-jedną-pozycję-i-jedno-odczytanie)).
Lemat pominięty na liście zostaje przy pozycji bez przecinka,
więc pominięcie nie odbiera ani jednego zdania.

Podział ten odbiera zarazem napisy, których polszczyzna nie ma:
`Program zapisuje ustawienia ale linter sprawdza tekst.`,
`Plik jest nowy ale duży.` i `Skład czyli Morfeusz jest tani.`
czytania nie mają, bo polszczyzna stawia przed tymi spójnikami przecinek.
W drugą stronę odbiera przecinek postawiony tam, gdzie polszczyzna go nie stawia:
`Program zapisuje ustawienia, i linter sprawdza tekst.` czytania też nie ma.
Pozycji z przecinkiem grupa imienna i przymiotnikowa nie dostają,
bo `nie polszczyzny, a dziedziny` jest w nich elipsą, a nie ciągiem współrzędnym.
Dopowiedzenia z `czyli` żadna z tych dwóch pozycji nie daje,
bo dopowiedzenie odnosi się do składnika zdania,
a koordynacja zdaniowa łączy dwa zdania;
daje je człon bez czasownika
([niżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).
Zawężenie tych dwóch poziomów nie rusza ani jednego zdania w żadnym z trzech
rejestrów — ani nad Składnicą, ani nad README, ani nad ustawami —
więc płaci za nie sam werdykt, który przedtem kłamał pewnie.

Bez trzeciego warunku ta pozycja nie kupiłaby prawie nic,
a warunek ten pada na lemat przyimka, a nie na produkcję
([niżej](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)):
Morfeusz czyta `a` także jako przyimek,
więc każde `, a` w zdaniu wychodziło okolicznikiem wysuniętym drugiego składowego.

Poza gramatyką zostaje ciąg dwóch znaków rozdzielających, zapisany
[subset.md](../subset.md#what-it-does-not-cover-yet).

## Człon bez czasownika stoi za spójnikiem, który go bierze

Ten rejestr dokumentuje podzbiór przez to, czego w nim nie ma,
więc `a nie` oraz `czyli` niosą setki zdań tej prozy,
a za tym spójnikiem stoi sam człon, bez powtórzonego czasownika:
`Milczenie obejmuje wybór, a nie zdanie.`

Konstrukcja jest elipsą, a nie koordynacją,
i rozstrzyga o tym pozycja, którą ten człon zajmuje:
żadnej. `wybór` jest dopełnieniem, a `zdanie` mówi, czym dopełnienie nie jest,
więc wpuszczone jako drugi człon ciągu imiennego wychodziłoby drugim dopełnieniem
i zdanie przyjęte mówiłoby o sobie nieprawdę.
Stoi więc obok zdania składowego, tam gdzie wtrącenie w nawiasie,
i tak samo nazywa się całym napisem
([niżej](#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).

**Czemu ten człon przeczy, gramatyka nie mówi.**
`Milczenie obejmuje wybór, a nie zdanie.` przeciwstawia dopełnieniu,
a `Wybór obejmuje milczenie, a nie zdanie.` przeciwstawia albo dopełnieniu,
albo podmiotowi, i rozstrzyga o tym znaczenie, a nie kształt.
Jest to ta sama odmowa, którą olski wydaje o przyłączeniu
([subset.md](../subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
z jedną różnicą: przyłączenie olski melduje jako wieloznaczność,
bo gramatyka ma tam kilka wyprowadzeń,
a tutaj wyprowadzenie jest jedno i milczy o tym, do czego człon się odnosi.
Werdykt nazywa więc rolę `elipsa` i wypisuje pod nią cały napis.

**Spójnik rozstrzyga, czy ten człon wchodzi, i lista jest węższa od zdaniowej.**
`a`, `ale`, `lecz`, `natomiast`, `tylko` i `czyli` biorą człon bez czasownika,
a `więc`, `zatem` i `toteż` go nie biorą,
bo `Cena jest niska, więc gramatyka.` polszczyzną nie jest.
Podział ten nie jest oszczędnością, tylko obietnicą podzbioru:
lista wzięta cała wyprowadzałaby napis, którego polszczyzna nie ma.
`czyli` stoi na liście po jednej stronie z `a nie`,
choć jedno przeczy, a drugie powtarza to samo innymi słowami:
różnicy tej gramatyka nie widzi, a rola nazywa kształt, nie funkcję.
Dopowiedzenie z `czyli` schodzi tym samym z kolejki w postaci,
w której ten rejestr pisze je najczęściej — na końcu zdania —
a postać wtrącona, `Skład, czyli Morfeusz, jest tani.`, zostaje
([subset.md](../subset.md#what-it-does-not-cover-yet)).

**Wypełnienia są trzy i każde ma cenę osobną.**
Grupa imienna, grupa przymiotnikowa i wyrażenie przyimkowe wchodzą osobnymi
ciałami, bo cena każdego z nich ma być osobną liczbą, i te liczby się rozchodzą:
nad polską prozą tego repozytorium grupa imienna kupuje kilkadziesiąt zdań,
wyrażenie przyimkowe kilkadziesiąt, a grupa przymiotnikowa poniżej dziesięciu
i zabiera przy tym pojedyncze zdania przyjęte,
bo `droga` i `tania` są u Morfeusza naraz rzeczownikiem i przymiotnikiem.
Przysłówek stał w tej pętli i wypadł: kupował pojedyncze zdania,
czyli tyle, ile nie warto czterech ciał.

Osobno stoi cząstka przecząca, bo ciało z nią i ciało bez niej są dwoma ciałami,
a nie jednym z cząstką pominiętą, i to ona kupuje najwięcej — przeszło sto zdań.
Dopełniaczem nie rządzi i nie ma czym, bo czasownika pod nią nie ma,
a przypadek członu jest przypadkiem tego, czemu on przeczy.

**Przecinek zamykający ten człon jest drugim takim przecinkiem w gramatyce.**
`Granica pakietu jest tu rozstrzygnięciem, a nie przypadkiem, i pilnuje go test.`
biegnie za tym członem dalej, tak samo jak zdanie nadrzędne biegnie dalej
za zdaniem podrzędnym, więc ciało zamknięte przecinkiem dokłada ta sama funkcja
([podrzędność.md](podrzędność.md#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
Kupuje ono kilkanaście zdań i jest zarazem tym,
co czyni przecinek przed `i` w tym rejestrze poprawnym w dwóch miejscach,
a nie w jednym.

**Zakup zależy od rejestru o rząd wielkości.**
Nad polską prozą tego repozytorium ta konstrukcja kupuje przeszło sto
czterdzieści zdań, czyli kilka procent tego, co ta proza ma,
a nad bankiem drzew kilkadziesiąt, czyli promile.
Rozjazd nie mówi nic o gramatyce i wszystko o tym, kto pisze:
podzbiór dokumentuje się przez wykluczanie, a gazeta nie.
Mierzy to za jednym razem obie kolejki, o których mówi
[corpus.md](../corpus.md#the-same-queue-over-prose).

## Spójnik wewnątrz zdania ma jedną pozycję i jedno odczytanie

`Milczenie jest zatem wartością.`, `Reguła jest bowiem tania.`,
`Linter zaś sprawdza tekst.`
Polszczyzna stawia te spójniki wewnątrz zdania, za jego pierwszym wyrazem.
Trzy lematy tej listy czoła nie zajmują wcale,
i to o nich lista spójników okolicznikowych mówi, że pozycji dla nich nie ma
([podrzędność.md](podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).

Pozycją jest lista okoliczników i nic poza nią.
Wystarcza to, bo miejsce na okolicznik wylicza się za każdą córką zdania,
a nie przed pierwszą (`olski/precedencja.py`),
czyli ta lista mówi dokładnie tyle, ile polszczyzna o tym spójniku mówi.
Czoła zdania ten symbol nie dostaje, bo spójnik za przecinkiem
bierze już koordynacja
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)):
`Cena jest niska, więc gramatyka jest tania.` wychodzi tamtą produkcją.
Cena wychodzi zatem z gramatyki, a nie z przebiegu, tak samo jak przy dwukropku,
a zakup jest zmierzony: kilkadziesiąt zdań tej prozy.

Czoło całego zdania jest pozycją osobną
i ma [własną sekcję](#spójnik-na-czele-zdania-wiąże-je-z-poprzednim).

## Spójnik na czele zdania wiąże je z poprzednim

`I nikt tego nie zauważył.`, `Zatem milczenie jest wartością.`,
`Albo inaczej.`
Spójnik nie ma tu zdania przed sobą, a wiąże swoje zdanie z poprzednim.
Spójnik współrzędny i `zatem` stoją w tym miejscu jedną pozycją,
choć koordynacja rozdziela je na dwie klasy:
przed jednym żąda przecinka, przed drugim nie,
a czoło zdania nie ma przecinka przed czym postawić.

Ciało należy do zdania, a nie do zdania składowego.
Na poziomie składowego tej pozycji nie ma jak odgraniczyć od koordynacji —
`Cena jest niska, i gramatyka jest tania.` miałoby wtedy dwa wyprowadzenia,
bo spójnik zaczynałby człon drugi i zarazem go koordynował —
a zdanie ma czoło jedno, więc na tym poziomie rozgraniczenie nic nie kosztuje.

Lematy są listą dodatnią, a nie wykluczeniem, i rozstrzyga o tym cena obu.
Wykluczenie wzięłoby każdą formę, którą Morfeusz czyta jako spójnik,
a gramatyka daje kilku z nich pozycję własną:
`czy` podporządkowuje pytanie o rozstrzygnięcie
([podrzędność.md](podrzędność.md#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą)),
`to` jest zaimkiem, a `jak` i `tymczasem` przysłówkiem.
Wpuszczone czołem, dają one drugie czytanie zdaniom,
które polszczyzna czyta raz — `Czy zmiana idzie w dobrą stronę?`,
`To samo wejście daje tę samą odpowiedź.`, `Tymczasem byk już był przy nim.` —
a klasa ta ma więcej lematów, niż widać nad jednym korpusem:
pod złotą morfologią wykluczenie nie kosztuje nic,
a pod żywą odbiera jednoznaczność kilkudziesięciu zdaniom banku drzew,
i kilkunastu nawet wtedy, gdy nazywa już trzy najczęstsze lematy,
gdzie lista dodatnia odbiera ją jednemu.
Rosłaby więc o każdy lemat, który ktoś zauważy,
i tym różni się od wykluczenia cząstki przeczącej,
które nazywa jeden lemat i jedną pozycję
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).

Lista schodzi się z trzech: spójniki, przed którymi polszczyzna stawia przecinek,
spójniki, które ten rejestr stawia wewnątrz zdania
([wyżej](#spójnik-wewnątrz-zdania-ma-jedną-pozycję-i-jedno-odczytanie)),
oraz `i` i `albo`, których żadna z tamtych nie ma.
`ani` do trzeciej nie należy, i jest to wynik, a nie przeoczenie:
bank drzew otwiera nim zdania spójnikiem skorelowanym,
a tę konstrukcję gramatyka bierze ciągiem
([wyżej](#spójnik-skorelowany-powtarza-się-przed-każdym-członem)),
więc czoło nie kupiłoby przy niej ani jednego zdania,
a odebrałoby jednoznaczność grupie `ani jedno`.
Terminal bierze przy tym obie części mowy spójnika,
bo `zatem` i `więc` na czele zdania dostają u Morfeusza `comp`,
a bank drzew nazywa je tam `conj`.

Pozycję podsunął wiersz `conj` kolejki blokerów, który prowadził ją czwarty,
a przeszło dwie trzecie jego zdań stało właśnie na czele
([corpus.md](../corpus.md#where-the-analyses-stop)).
Nad bankiem drzew wychodzi z odrzucenia przeszło sto zdań,
pod jedną morfologią i pod drugą,
a kilkadziesiąt kolejnych dostaje czytanie, nie dostając jednoznaczności.
Z tych, które mają w drzewie wzorcowym rolę do porównania,
zgadza się z nim przeszło dziewięć na dziesięć, a jedno czyta się odwrotnie.
Nad prozą tego repozytorium przybywa kilkanaście zdań przyjętych.
Jednoznaczności nie traci przy tym pod złotą morfologią i nad tą prozą
ani jedno zdanie, a pod żywą jedno, bo tej pozycji nie bierze żaden inny kształt.

## Interpunkcja obejmująca: cudzysłów wchodzi w grupę, a nawias staje obok zdania

Znak rozdzielający spina dwa zdania, a obejmujący bierze to, co stoi w środku,
i te dwie pary są w tym rejestrze dwiema różnymi konstrukcjami.
Cudzysłów obejmuje tytuł — `„Zasady techniki prawodawczej”` —
albo napis przytoczony, o którym zdanie orzeka: `„B”`, `„nie”`.
Tytuł odmienia się i jest grupą imienną, przytoczenie nie odmienia się wcale,
więc pozycje są dwie.
Nawias obejmuje dopowiedzenie obok zdania,
którym w tej prozie jest nazwa dokumentu: `(docs/subset.md)`, `(niżej)`.

**Cudzysłów przepuszcza grupę imienną całą.**
Produkcja obejmuje grupę i wypuszcza jej przypadek, liczbę oraz rodzaj bez zmiany,
bo polszczyzna odmienia to, co cudzysłów obejmuje, wedle roli, w której grupa stanęła:
`Same „Zasady techniki prawodawczej” stoją poza tą sumą.` ma w środku mianownik,
a `Ustawa jest przepisem „Zasad techniki prawodawczej”.` dopełniacz.
Napis niedomknięty wyprowadzenia nie ma.
Cudzysłowa maszynowego — `"Zasady techniki prawodawczej"` — produkcja nie bierze,
bo ten jeden znak nie jest żadnym z tych dwóch,
a za napis, którego polszczyzna nie pisze, płaci autor
([pisanie-po-olsku.md](../pisanie-po-olsku.md#kto-płaci-za-odrzucone-zdanie));
werdykt nazywa mu wtedy parę, którą ten rejestr pisze
([subset.md](../subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).
Wnętrzem tej produkcji jest sama grupa imienna,
więc `„to nie zdanie”` zostaje na zewnątrz.

**Napis przytoczony grupą imienną nie jest i dostaje czytanie nieodmienne.**
Cudzysłów obejmuje w tej prozie także `„B”`, `„nie”` i `„Daj”`,
czyli napisy, o których zdanie orzeka, a nie słowa, którymi orzeka.
Polszczyzna ich nie odmienia, więc produkcja nie ma tu czego przepuszczać,
a napis dostaje rzeczownik nieodmienny: wszystkie siedem przypadków i rodzaj nijaki.
Nieodmienność jest tu wiedzą i tym różni się przytoczenie od formy,
o której słownik milczy, a która przypadka nie niesie wcale
([warstwa-leksykalna.md](../warstwa-leksykalna.md#forma-o-której-słownik-milczy-jest-rzeczownikiem-nieoznaczonym)).
Nazwa litery zapisana słownie wyprowadza się bez tej pozycji,
bo `wu` i `ce` słownik daje jako rzeczowniki nieodmienne,
a litera zapisana znakiem jest u słownika skrótem — `B` pod lematem `bajt` —
i skrótów ta gramatyka nie ma.

Licencji udziela cudzysłów po obu stronach napisu,
tak samo jak przyimek udziela jej formie przyimkowej
([grupa-imienna.md](grupa-imienna.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)).
Napis niedomknięty nie jest więc przytoczeniem,
a wnętrze dłuższe niż jedno słowo zostaje przy grupie.

Napis z czytaniem rzeczownikowym zostaje przy grupie, choćby był jednym słowem,
i jest to warunek, a nie oszczędność:
czytanie nieodmienne spełnia każde żądanie przypadku, a niesie rodzaj nijaki,
więc `Program zapisuje „ustawienia”.` dostałoby drugie czytanie,
w którym napis jest podmiotem,
a `„Reguła” jest tania.` przestałoby się wyprowadzać.
Warunek pyta o czytania, a nie o ich użyteczność,
więc `Znam „szybko”.` pada dalej:
słownik daje tej formie wołacz rzeczownika `szybka`,
którym dopełnienia nikt nie zbuduje, a przytoczenia on już nie dopuszcza.

Cena jest ta sama, którą płaci forma, o której słownik milczy
([warstwa-leksykalna.md](../warstwa-leksykalna.md#forma-o-której-słownik-milczy-jest-rzeczownikiem-nieoznaczonym)),
a do niej dochodzi jedna osobna:
zdanie jednowyrazowe jest w cudzysłowie tym samym napisem co forma przytoczona,
więc `Znam „Płacę”.` wychodzi jednym czytaniem,
w którym mowa niezależna jest rzeczownikiem.

Nad prozą tego repozytorium pozycja nie domyka ani jednego zdania:
przytoczeń jest w niej kilkanaście, a każde zdanie z nimi niesie obok
konstrukcje, których olski nie ma, więc pozycja zdejmuje jeden powód odrzucenia,
a nie całe odrzucenie.
Zakup jest przez to odłożony, a nie zmierzony na zero,
tak samo jak przy drugiej pozycji nawiasu niżej.

**Nawias dochodzi w każdym napisie do jednego gospodarza.**
`Zdanie stoi (docs/subset.md).` wychodzi jednym czytaniem,
a nie tyloma, ile gospodarzy ma w zdaniu wyrażenie przyimkowe,
i nie jest to wybór przyłączenia, którego olski nie robi
([subset.md](../subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)).
Nawias niczego w zdaniu nie wypełnia,
więc gdziekolwiek by dochodził, role zdania są te same,
a różnicy między dwoma miejscami nie ma czym wypowiedzieć —
gdzie wyrażenie przyimkowe zmienia to, o czym zdanie mówi, a nawias nie zmienia nic.
Wtrącenie jest przy tym rolą, którą werdykt nazywa,
i jest rolą całym napisem: przysłówek w środku nawiasu nie jest okolicznikiem zdania,
więc zejście po role zatrzymuje się na wtrąceniu tak samo jak na zdaniu podrzędnym.

Wnętrzem nawiasu jest grupa imienna albo przysłówek.
Pozycje są dwie i obie stoją tam, gdzie nawias zamyka zdanie składowe
albo zdanie względne odgrodzone przecinkami:
`Reguła, która rozstrzyga (niżej), jest tania.` wychodzi jednym czytaniem.

**Druga pozycja stoi w ciele zamykanym przecinkiem i tylko w nim.**
Ciała zdania względnego są dwa, bo przecinek zamykający polszczyzna stawia wtedy,
gdy zdanie nadrzędne biegnie dalej
([podrzędność.md](podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
a w tym z przecinkiem nawias stoi przed nim,
gdzie przyłączony do zdania nadrzędnego stanąłby za nim, czyli dałby inny napis.
Ciało bez przecinka kończy się tam, gdzie kończy się zdanie nadrzędne,
i tam pozycji nie potrzeba, bo pierwsza z dwóch obsługuje ten napis w całości:
`Program zapisuje regułę, która rozstrzyga (niżej).` wychodzi jednym czytaniem,
w którym nawias dochodzi do zdania nadrzędnego.
Druga pozycja dopisana i tam nie kupiłaby ani jednego zdania,
a dołożyłaby temu napisowi czytanie,
i nierówność ciał jest przez to oszczędnością, a nie ceną.

Nad Składnicą ta pozycja nie rusza ani jednego zdania,
pod złotą morfologią ani pod żywą,
bo proza prasowa nawiasu wewnątrz zdania względnego nie pisze.
Pisze go dokumentacja tego repozytorium, i pisze kilka razy,
a przyjętego zdania ta pozycja jej nie kupiła:
zakup jest odłożony tak samo jak przy przytoczeniu wyżej.

Na zewnątrz zostaje nawias w środku grupy imiennej —
`grupa imienna (ta z dopełniaczem) stoi` —
i jest to w tej prozie mniejszość:
nawias stoi w niej zwykle przed kropką albo przecinkiem,
czyli tam, gdzie kończy się zdanie, jego składowe albo zdanie względne w nim,
co liczy `grep -oP '\)[.,]' proza/docs.txt | wc -l` wobec wszystkich nawiasów tego pliku.

## Para myślników obejmuje wtrącenie w środku zdania, a nawias na jego końcu

`Zepsute miejsce — w prozie czy w kodzie — nie potrzebuje lepszej wersji.`,
`Reszta jest prywatna — nazwa funkcji w module — i rusza ją zwykła robota.`
Para obejmuje to samo, co nawias — dopowiedzenie, które w zdaniu pozycji nie
zajmuje — a rozdziela je miejsce.
Nawias zamyka zdanie składowe albo zdanie względne w nim
([wyżej](#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)),
a para wchodzi w środek zdania, między jego składniki.

**Miejsce daje parze lista okoliczników, a nie ciało wypisane na każde z nich.**
Miejsce na okolicznik wylicza się za każdą córką zdania (`olski/precedencja.py`),
więc symbol dopisany do tej listy dostaje je wszystkie naraz:
za podmiotem, za dopełnieniem i na końcu zdania składowego.
Ciało wypisane na każde z tych miejsc byłoby drugą deklaracją szyku,
a szyk deklaruje się w tej gramatyce raz
([subset.md](../subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).

Symbol jest przy tym osobny od nawiasowego, a werdykt nazywa je dwiema rolami.
Jeden symbol na oba wpuściłby nawias w każde miejsce okolicznika,
więc `Zdanie stoi (docs/subset.md).` wychodziłoby tyloma czytaniami,
ilu gospodarzy ma w nim wyrażenie przyimkowe,
a jedno czytanie tego napisu jest tym, po co pozycja nawiasu jest jedna.
Para tej ceny nie płaci, bo miejsce, w którym stoi, wskazują dwa znaki naraz:
w `Cenę tego — pokrycie — trzyma dokument.` gospodarz jest jeden i wypisuje go werdykt.

**Wypełnienia są trzy i cena każdego z nich jest osobną liczbą.**
Grupa imienna kupuje kilka zdań tej prozy, a zdanie składowe pojedyncze.
Pierwsze wtrąca nazwę albo wyliczenie, drugie całe zdanie:
`Zdjęte jedno z nich nie odrzuca tego zdania — drugie wyprowadza je samo — tylko
oddaje je jednym czytaniem.`
Wyrażenie przyimkowe kupuje jedno zdanie i kupuje je razem z ciągiem
współrzędnym wyrażeń przyimkowych
([grupa-imienna.md](grupa-imienna.md#wyrażenie-przyimkowe-koordynuje-się-tak-jak-grupa-imienna)):
bez tamtej pozycji `— w prozie czy w kodzie —` potyka się o spójnik w środku pary,
a samo wypełnienie nie kupuje wtedy ani jednego zdania.
Dwie pozycje wpuszczone razem bywają przez to warte więcej niż z osobna
([pisanie-po-olsku.md](../pisanie-po-olsku.md#zasłanianie-działa-w-obie-strony)).
Jednoznaczności nie traci przy żadnym z tych trzech ani jedno zdanie,
a zdania nowo wyprowadzone wychodzą wieloznaczne:
są długie i niosą wieloznaczność z innego powodu.

**Zakup jest własnością rejestru, a nie gramatyki.**
Nad bankiem drzew ta konstrukcja nie rusza ani jednego zdania,
pod złotą morfologią ani pod żywą,
bo proza prasowa wtrąca nawiasem i przecinkiem, a pary myślników nie pisze.
Pisze ją dokumentacja tego repozytorium: przeszło sto zdań jej prozy niesie dwa
myślniki, licząc znaki w zdaniach wyciętych przez `harness/markdown.py`.
Rozjazd jest ten sam, co przy pytaniu zależnym za dwukropkiem
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).

Na zewnątrz zostaje para obejmująca człon bez czasownika —
`Reszta jest prywatna — a nie publiczna — i rusza ją robota.` —
oraz para, za którą stoi spójnik bez przecinka:
`Szyk jest jeden — forma przyszła przed czasownikiem — więc reszta stoi za nim.`
Pierwsza jest wypełnieniem czwartym, a druga koordynacją,
której przecinka para nie zastępuje.

## Rozdzielające `a` nie jest przyimkiem tego rejestru

Morfeusz daje formie `a` cztery czytania i jednym z nich jest przyimek rządzący
mianownikiem — ten z `dwa bilety a pięć złotych`, czyli z ceny za sztukę.
Wyrażenie przyimkowe olskiego bierze przyimek wraz z przypadkiem, którym on rządzi,
więc bez warunku niżej `a` otwiera je tak samo jak `w` albo `z`,
a grupa imienna po nim stoi w mianowniku,
czyli w tym samym przypadku, w którym stoi podmiot zdania po spójniku.
Każde `, a` w zdaniu wychodzi przez to okolicznikiem wysuniętym drugiego składowego:
`Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego.`
miało przed tym warunkiem kilka czytań i każde z nich niosło
`„a podmiot jednego” → „jest”`.

Polszczyzna tego zdania tak nie czyta.
Warunek obejmuje oba wyrażenia przyimkowe tej gramatyki — zwykłe i to,
które wysunęło zaimek względny — i mówi tyle: przyimek tego wyrażenia nie jest `a`.
Warunek ujemny postawiony na lemacie po to,
żeby odebrać czytanie, którego polszczyzna w tym miejscu nie ma,
stoi w tej gramatyce także przy
[zaimku rzeczownym](grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem).
Tańsza z dwóch dróg pyta właśnie o to, co produkcja licencjonuje,
a nie o to, co słownik oferuje
([roadmap.md](../roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).

Kryterium ogólniejsze wygląda tu na tańsze: żądanie „rządź jednym z pozostałych
sześciu przypadków” powiedziałoby to samo o każdym słowie naraz.
Nie powiedziałoby, i mówi to sam słownik.
Mianownikiem rządzą w nim także `jak`, `jako`, `niż`, `co` i `aniżeli`,
czyli wykładniki porównania,
i wszystkie pięć padają w prozie, którą to repozytorium czyta —
nad README, siedmioma ustawami i korpusem audytowym razem
`niż`, `co` i `jako` po przeszło setce razy, `jak` kilkadziesiąt,
`aniżeli` kilka, przy kilkuset formach `a`.
Kryterium na przypadek zabrałoby więc razem z rozdzielającym `a` i te pięć.

Cena jest zerowa i jest to wynik pomiaru, a nie założenie.
Pod złotą morfologią przebieg nad Składnicą nie rusza ani jednego zdania z 13 035,
bo tam każda forma ma jedno czytanie wybrane przez człowieka
i `a` nie jest w tym korpusie przyimkiem ani razu.
Pod żywą morfologią, czyli nad prozą README, warunek odbiera jedno zdanie —
to wypisane wyżej — i oddaje je z powrotem przecinek przed spójnikiem
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
i liczba czytań wychodzi ta sama przed i po.
Różnią się one tym, że tamte niosły okolicznik, którego zdanie nie ma,
a te niosą podmiot, który ono ma.
