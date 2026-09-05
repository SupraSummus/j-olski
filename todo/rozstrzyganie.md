# Rozstrzyganie i świadkowie

Świadkowie w `olski/rozstrzyganie.py` pytają o `Przyłączenie`, czyli o obiekt składniowy,
choć warstwa powstała po to, żeby odpowiadać czymś ponad składnią
([`docs/architecture.md`](../docs/architecture.md#warstwa-rozstrzygająca-wydaje-zawężenie-z-powodem-a-nie-znaczenie)).
Widać to na kopuli: powtórzenie frazy przy `być` nie dowodzi niczego o tym czasowniku,
więc lista kopul odbiera dowód, zamiast dać świadkowi pytanie, na które kopuła odpowiada
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Świadka pytającego o drzewo dziedziny zamiast o gospodarza zmierzono przed napisaniem
i wyszło, że nie miałby o co pytać:
warstwa znacząca tego rejestru nie dosięga,
więc pytanie padłoby nad jednym zdaniem wieloznacznym banku drzew z kilkuset,
coś, co liczy `python3 -m harness.znaczenia`.
Zostaje z tego kolejność:
pytanie ponad składnią stawia się dopiero za kategoriami, których ten zapis nie ma,
a pierwszą z nich jest wyrażenie przyimkowe pod grupą imienną,
czyli to samo przyłączenie, o które świadek miałby pytać
([`docs/po-wypisaniu.md`](../docs/po-wypisaniu.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma)).
Dopisanie jej jest jednak odwróceniem rozstrzygnięcia, a nie załataniem dziury,
bo okolicznik dochodzi w tym zapisie do zdarzenia, a nie do rzeczy,
więc kto ten wpis podnosi, zaczyna od tamtej sekcji, a nie od `olski/rozstrzyganie.py`.
Do przeczytania jest `Świadek` w tym samym pliku:
sygnatura jest jedna dla wszystkich świadków rozmyślnie,
więc świadek o innym wejściu albo tę sygnaturę rozszerza, albo staje się drugą listą,
a drugiej listy ten protokół unika z podanego tam powodu.

Warstwa rozstrzygająca nie dostaje pytania o synkretyzm, choć pomiar tę klasę liczy.
`pytania` w `harness/wieloznaczność.py` wypuszcza same `Przyłączenie`,
a klasa synkretyzmu zostawia `gospodarze` puste, bo wyborem nie jest tam przyłączenie,
więc `Koszt szynki i sera przewyższa koszt bułki.` nie stawia warstwie ani jednego pytania,
choć werdykt nad nim mówi `różne w rolach: dopełnienie, podmiot`.
Nad korpusem audytowym pozycję tej klasy niesie 21,1% zdań
([`docs/open-questions.md`](../docs/open-questions.md#odpowiedź-o-wieloznaczności-nie-mówi-czy-ma-ją-też-czytelnik)),
a ile z odrzuceń nad Składnicą zostawia ją jako całą decyzję, nie liczy nikt:
tabela klas liczy tam nazwy z werdyktu, a nie decyzje,
i osobnej kolumny na szyk nie ma
([`docs/disambiguation.md`](../docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)).
Ruchem jest drugi typ pytania obok `Przyłączenie` — wybór między dwiema grupami o role —
oraz `Świadek`, który go przyjmuje, bo dzisiejszy protokół pyta o gospodarza modyfikatora.
Do rozstrzygnięcia jest, czy `próba/wybory.txt` ten typ unosi:
wpis ma pola `fraza` i `gospodarze`, a tu żadnej frazy nie ma,
więc albo dochodzi drugi plik, albo pola nazywają się szerzej.
Świadka dzisiejszego kształtu nie ma tu przy tym żadnego i nie jest to przeoczenie:
temat rozstrzyga kolejność, a nie rolę
([`docs/disambiguation.md`](../docs/disambiguation.md#kontekst-rozstrzyga-wykluczeniem-a-nie-rankingiem)),
skłonność liczy przyimki, a powtórzenie przeniesione z frazy na rolę
wskazuje po `Bułka jest tania.` na `koszt bułki` jako podmiot,
czyli odwrotnie, niż czyta czytelnik.
Wpis jest więc o pytaniu, a nie o odpowiedzi:
warstwa, która pytania nie dostaje, nie umie nawet przemilczeć.
Wzorzec ma przy tym dwa wiersze gotowe do przeczytania:
`Program drukuje werdykt.` rozstrzyga się jednym pytaniem o klasę,
a `Dokument opisuje pomiar.` nie rozstrzyga się nią wcale,
choć żądanie stoi nad obydwoma
([`docs/disambiguation.md`](../docs/disambiguation.md#kontekst-rozstrzyga-wykluczeniem-a-nie-rankingiem)).
Zdania celu bierze się z lematów `olski/żądania.txt`,
bo nad czasownikiem, którego ten plik nie ma, warstwa milczy z drugiego powodu,
a pomiar tych dwóch powodów nie rozdzieli.

Świadek ramowy pyta o przyimek i nie pyta o przypadek grupy pod nim,
więc jego zasięg jest oszacowaniem górnym po obu stronach sporu.
Walenty pisze `prepnp(o,loc)` obok `prepnp(o,acc)`, a `Attachment`
w `harness/attachment.py` niesie sam przyimek, więc `informacja o błędzie` pasuje
do obu wpisów naraz i tak samo pasuje do nich rama czasownika,
czyli weto pada częściej, niż powinno, i częściej pada też wskazanie.
Ruchem jest przypadek wydawany przez `Attachment` wraz z kolumną leksykonu, która go
niesie, i pytanie o obie wartości naraz — w `przyimki` w `harness/walenty.py`
oraz w `Rama` w `olski/rozstrzyganie.py`, bo kryterium jest jedno.
Do przeczytania jest, ile ten zwrot zdejmuje: pod `--tylko-pewne` żadna liczba
sondy nie ruszyła się o więcej niż pół punktu, więc pewność schematu tej klasy nie
odróżnia, a przypadek jest drugim zwężeniem, jakie ten słownik daje bez czytania
schematów ręką
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)).
Wpis jest winien przebiegi `harness/rama.py` oraz `--oceń`, bo rusza obie ich pary liczb.

Świadek ramowy nie widzi gospodarza imiennego, którego forma ma czytanie czasownikowe.
Stronę gospodarza nazywa `strona` w `olski/rozstrzyganie.py`, a nazywa ją po
„którymkolwiek czytaniu”, więc `opieka` trafia na stronę czasownikową przez lemat
`opiekać`, a rama `opieka`, która żąda `nad`, nie ma wtedy czego wskazać.
Odpowiedź `uzyskać` z `nad` przy `opieka` stoi wypisana wśród dwunastu, które
drukuje `harness/rama.py`, i tam trafia, bo tam stronę daje bank drzew, a nie Morfeusz.
Wskazania świadek przez to nie myli, tylko milczy, więc cena stoi w zasięgu.
Ruchem nie jest drugie kryterium obok `strona`:
o `strona` pyta także `harness/wskazania.py`, więc druga reguła rozeszłaby się z nią
cicho, a rozejście widać dopiero w liczbach.
Ruchem jest albo rodzaj konstytuentu wniesiony do `Przyłączenie` w `olski/parse/podsumowanie.py` —
gramatyka go zna, bo `gospodarze` w `DEKLARACJA` wylicza symbole, na których
zejście się zatrzymuje, a wpis przyłączenia niesie same głowy —
albo zgoda na to, że warstwa stronę zgaduje z czytań formy, wypisana w `strona`.
Do przeczytania jest, ile ta klasa waży: liczbę daje przebieg, który pyta ramy
o gospodarza po obu stronach naraz, zamiast po tej, którą wybrała `strona`.

Nie wiadomo, ile świadek ramowy odpowiada nad rejestrem docelowym.
Zasięg ogranicza mu słownik, a nie kryterium: plik rzeczownikowy Walentego wylicza
1 996 lematów, więc rzeczownik spoza tej listy jest dla świadka rzeczownikiem bez
ramy, a nie rzeczownikiem, którego rama tej pozycji nie ma.
Liczby są dwie i bank drzew nie mówi ani o jednej:
ile pozycji spornych `harness/wieloznaczność.py` wypuszcza nad korpusem audytowym
z rzeczownikiem wypisanym w Walentym, i na ilu z nich świadek odpowiada.
Ruchem jest wiersz w `harness/wskazania.py` albo osobny przebieg nad `proza/`,
wzorowany na `harness/powtórzenie.py`, który tę populację już liczy
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Do rozstrzygnięcia jest, czy ta liczba jest wierszem tabeli świadków,
czy figurą osobną: tabela liczy odpowiedzi, a to jest pytanie o mianownik pod nimi.

Świadek kontekstowy nie ma zmierzonej trafności, a odpowiedzi do przeczytania ma siedemnaście.
`harness/powtórzenie.py` nad korpusem audytowym dostaje od niego 7 wskazań w granicy
akapitu i 127 bez niej, a przeczytane ręką jest siedem pierwszych i dziesięć
rozrzuconych po pozostałych
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)),
czyli odczyt, a nie stopa pomyłek: nad 1 126 pozycjami siedemnaście sądów nie jest częstością.
Wzorzec, przy którym byłaby, jest dwojaki i oba są cudzą robotą.
`próba/wybory.txt` daje trzydzieści sądów, a wskazania tego świadka są w nich dwa,
i losowanie go nie dosięga z żadnej strony: nad 1 126 pozycjami odzywa się siedem razy,
a próba zawężona do samych odpowiedzi warstwy wzięła trzydzieści ze 123 i nie trafiła w ani jedno
([częstość nad dokumentacją](../docs/rozstrzyganie.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)),
więc po tej stronie zostaje przeczytanie wszystkich siedmiu, a nie próba.
Drugim jest [wzorzec po drugiej stronie](../docs/disambiguation.md#wzorzec-na-tę-warstwę-jest-po-drugiej-stronie),
bo tekst złożony przez `olski/skład` niesie czytanie, o które w nim chodziło,
i wtedy obrót przez parser mówi, czy warstwa zdejmuje czytanie, którego drzewo nie deklarowało.
Blokuje go ta sama własność drzewa, przez którą `przejrzyj`
zgłasza jedną klasę z dwóch: okolicznik dochodzi w nim do zdarzenia zawsze,
więc wzorzec wychodzi jednostronny i obrót niczego nie rozróżni.
Ta połowa wpisu jest przez to zaparkowana po stronie składu, a odblokuje ją dopiero
wyrażenie przyimkowe, które skład umie postawić wewnątrz grupy imiennej.

`próba/wybory-z-odpowiedzią.txt` mierzy dwóch świadków,
a wylosowano ją nad jednym.
Wpisy były odpowiedziami tabeli skłonności, a po wpuszczeniu świadka ramowego
ponad połowę z nich oddaje rama, bo stoi przed tabelą w kolejności świadków
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)).
Pięć pomyłek na 29 odpowiedziach jest przez to stopą warstwy, a nie tabeli,
więc zestawienie jej z trafnością tabeli na połowie banku drzew
mierzy po dwóch stronach co innego, a dokument notuje samo to, że mówi mniej.
Do przeczytania jest wydruk `python3 -m harness.wybory próba/wybory-z-odpowiedzią.txt`
wpis po wpisie, bo powód nazywa świadka, który odpowiedział:
podział na wpisy z powodem w zdaniu i bez niego czytała ręka,
gdy odpowiadała sama tabela, a powodów ramowych jest w nim więcej
niż odpowiedzi, które rama bierze.
Ruchem jest stopa rozbita po świadkach — pole w wydruku `harness/wybory.py`
albo losowanie osobne na świadka — a nie sama poprawka zdania w dokumencie.

`ZASIĘG_FRAZY` szuka rzeczownika frazy trzy słowa za przyimkiem i nie zatrzymuje
się na przecinku, więc dopasowuje się do frazy, której w tym miejscu nie ma.
`Przypisanie atrybutów do kategorii, jest zawarte w dokumencie, zakładka:
Atrybuty kategorii.` uchodzi przez to za zdanie, w którym stała fraza
`w przypadku tych atrybutów`: rzeczownik schodzi się z `Atrybuty`,
choć fraza tego zdania jest `w dokumencie`, a między nimi stoi przecinek i dwukropek.
Wyszło to nad korpusem audytowym przy wycenie reguły kandydata, w wariancie szerszym,
gdzie takie dopasowanie kończyło się wskazaniem na `jest`
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Wskazania tego nie ma żaden wariant, bo dowód z kopuli dowodem nie jest,
a samo dopasowanie stoi: warunek na kopulę zdjął wskazanie, a nie usterkę pod nim,
i nad tym korpusem nie widać jej w żadnym przebiegu.
Ruchem jest granica frazy wzięta z interpunkcji, a nie z liczby słów:
`SŁOWO` w `olski/rozstrzyganie.py` wypuszcza dziś same znaki słowotwórcze,
więc przecinka nie ma jak zobaczyć ani `_gdzie_stała`, która frazy szuka,
ani `_łańcuch`, który tą samą drogą przechodzi przecinek w lewo.
Do przeczytania jest, ile takich dopasowań w tym korpusie w ogóle pada,
bo znane jest jedno i wyszło przez wskazanie, które warunek na kopulę zdjął;
liczbę tę daje ten sam przebieg, kiedy wypisze dopasowania, a nie same wskazania.

`_grupa` w `harness/wieloznaczność.py` przedłuża łańcuch imienny przez orzeczenie,
bo forma osobowa bywa zarazem imienna: `stanowi` jest u Morfeusza celownikiem od `stan`,
więc `dokument stanowi kompendium wiedzy dla deweloperów` proponuje gospodarzy
`wiedzy, kompendium, stanowi, dokument`, a wybór jest tam między `kompendium` i `stanowi`.
Poprawia to ręka przy wpisie próby wyborów i mówi to jej nagłówek (`próba/wybory.txt`),
a wpis o powiększeniu tej próby mnoży ten koszt przez liczbę nowych wpisów.
Gospodarza czasownikowego szuka się przy tym przed przyimkiem, a nie przed grupą,
więc orzeczenie wciągnięte do łańcucha wraca drugi raz jako on
i pozycja stawia wtedy grupę przeciw jej własnemu członowi.
Ruchem jest kryterium przedłużające łańcuch węższe od czytania imiennego,
czyli takie, które formę o czytaniu osobowym zatrzymuje —
`OSOBOWY` w tym samym pliku wylicza te czytania pod pomiar synkretyzmu.
Do przeczytania jest przedtem, ile ten warunek zabiera, bo łańcuch urwany za wcześnie
odbiera gospodarza głowie grupy, czyli to, po co ten łańcuch tam stoi;
mianownikiem jest cała populacja pozycji, którą drukuje `python3 -m harness.powtórzenie`
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Ten sam warunek czyta `_łańcuch` w `olski/rozstrzyganie.py`, bo kryterium jest jedno,
a tam urwanie łańcucha kończy się milczeniem, nie pomyłką, więc cena jest inna po obu stronach.

Lista kopul, którą `olski/rozstrzyganie.py` odejmuje od dowodu,
jest pożyczona i cztery piąte jej nie zmierzono.
Świadek kontekstowy nie bierze za dowód powtórzenia przy kopuli, a listę kopul bierze
z gramatyki, gdzie kryterium jest inne: `KOPULA` w `olski/walencja.py` wylicza czasowniki
biorące orzecznik w narzędniku, a tutaj chodzi o czasownik, przy którym okolicznik stoi
bez związku z rzeczą. Nad korpusem audytowym rozstrzyga to samo `być`, a `zostać`, `zostawać`, `pozostać`
i `pozostawać` ruszają wyłącznie wariant sondy pytający o cały prefiks zdania,
gdzie zdjęcie takiego dowodu odsłania gospodarza zasłoniętego przez kopulę.
Liczbę tę daje `Powtórzenie(kopuly=frozenset({"być"}))` puszczone przez
`przebieg` w `harness/powtórzenie.py` obok listy pełnej: wiersze wypuszczany,
bez granicy akapitu i „sąsiad bezpośredni” wychodzą wtedy identyczne,
a „cały prefiks zdania” schodzi ze 128 na 126.
Do przeczytania jest, czy dowód przy `zostać` w stronie biernej mówi coś o rzeczy:
`obiekt zostanie przyjęty do bazy RIT` niesie treść w imiesłowie, a nie w czasowniku,
więc gospodarzem bywa tam imiesłów i wtedy zdjęcie lematu `zostać` niczego nie kosztuje.
Ruchem po tym czytaniu jest albo lista własna w tym module wraz z jej uzasadnieniem,
albo zdanie w `KOPULA`, że obie strony pytają o czasownik bez własnej treści.
Rozstrzygnąć to znaczy wybrać między jedną listą o dwóch kryteriach a dwiema listami,
które rozjadą się przy pierwszym lemacie dopisanym po jednej stronie.

Trafność warstwy nad werdyktami mierzy się na materiale, który tabela widziała.
`harness/wskazania.py` puszcza świadków z `domyślni`, czyli z
`olski/skłonności.txt`, a ten plik powstaje z całej Składnicy, po której ten
przebieg idzie, więc 96,1% spod
[tabeli nad werdyktami](../docs/rozstrzyganie.md#werdykt-pyta-warstwę-o-inny-wybór-niż-bank-drzew)
jest sufitem, a nie pomiarem.
Dotyczy to samej tabeli, a nie każdego świadka:
`Rama` czyta leksykon wyprowadzony z Walentego, więc materiału tego przebiegu nie
widziała, a wiersz o niej jest pomiarem, a nie sufitem.
Ruchem jest podział taki, jaki ma już `oceń` w `harness/skłonności.py`:
tabela z połowy plików o numerze parzystym, przebieg po nieparzystych,
czyli flaga podająca sondzie świadków zbudowanych z tamtej połowy zamiast z pliku.
Do rozstrzygnięcia jest, czy zasięg liczyć wtedy na tej samej połowie:
tabela z połowy korpusu ma mniej par, więc zasięg spadnie razem z trafnością,
a te dwie liczby dziś nie pochodzą z jednego przebiegu i po tym ruchu pochodziłyby.
Do przeczytania jest przy tym `KAWAŁEK` w `harness/pomiar.py`,
bo podział na kawałki idzie po plikach i musi minąć się z podziałem na połowy.

Warstwa rozstrzygająca tnie gospodarza inaczej niż gramatyka, kiedy jest nim notacja.
`_czytania` w `olski/rozstrzyganie.py` woła `analyse`,
więc `docs/linter.md` wraca pięcioma lematami —
`docs`, `linter`, `md` oraz kropka i ukośnik —
a `morphology` w `olski/segmentacja.py` ma tam jedną krawędź o czytaniu nieodmiennym.
Nie kończy się to milczeniem:
gospodarz `docs/linter.md` dopasowuje się do słowa `linter`
stojącego w akapicie gdziekolwiek,
a powód wypisuje wtedy to drugie słowo,
więc wskazanie samo mówi, że stoi na dowodzie o czym innym.
Ruchem jest sklejenie notacji pytane przez oba miejsca,
czyli `_segmenty` w `olski/segmentacja.py` wołane tą samą drogą,
którą oba pytają dziś o leksykon projektu.
Wpis jest winien przebieg nad korpusem audytowym,
bo dokumentacja techniczna pisze notację gęsto,
a wskazania warstwy nad tym korpusem liczy `harness/powtórzenie.py`
i cytuje je [`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek).
Do rozstrzygnięcia jest przy tym, czy warstwa ma widzieć dwa pozostałe kroki analizy:
`admissible` odbiera czytania, których polszczyzna nie ma,
a `po_przyimku` pyta o sąsiada, którego przy gospodarzu wziętym z werdyktu nie ma.

Ile wyborów werdykty stawiają nad korpusem audytowym, mówią trzy miejsca w dwóch
wartościach: `docs/rozstrzyganie.md` pisze przy losowaniu wzorca 49 wyborów na 2 915 zdań,
a `harness/wieloznaczność.py` i `tests/test_powtórzenie.py` piszą 38 na tyle samo zdań.
Jedna z nich jest sprzed zmiany w gramatyce albo w szukaczu pozycji
i nie widać której, bo żadna nie mówi, którym przebiegiem padła.
Dowodem do przeczytania jest liczba dzisiejsza:
`olski-check --rozstrzygaj` nad prozą [korpusu audytowego](../docs/audit-corpus.md#the-list)
wypisuje werdykty, a wyborem jest ten, który nazywa przyłączenie.
Ruchem tańszym od przeliczenia jest zejście obu komentarzy do rzędu wielkości,
bo obie liczby są tam przesłanką jednego zdania o populacji morfologicznej,
a właścicielem liczby jest dokument
([`CLAUDE.md`](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)).
