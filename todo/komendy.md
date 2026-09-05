# Komendy i sondy

`harness/pomiar.py` ma własny wiersz poleceń, choć bierze już to samo,
co bierze `harness/komenda.py`.
Stał poza nim, dopóki rozdawał ścieżki na bank drzew albo pliki prozy;
po podziale bierze sam katalog, czyli dokładnie wejście tamtego modułu,
a `--limit`, `--przykłady` i `--jobs` tamten moduł już daje.
Ruchem jest deklaracja `Komenda` zamiast tego parsera,
z `--morphology`, `--blockers` i `--examples` podanymi funkcją dopisującą argumenty.
Do rozstrzygnięcia jest przy tym język flag,
bo `harness/komenda.py` pyta o `--przykłady`, a ten przebieg o `--examples`,
i jest to ta sama decyzja, co przekład wydruku, więc oba wpisy podnosi się razem.

Kod wyjścia `olski-check` nie widzi zdania z zapomnianą kropką.
Napisu niedomkniętego nie liczy do mianownika nikt, żeby nagłówek nie psuł pomiaru
(`Verdict.punktowane` w `olski/werdykt/zdanie.py`),
więc przebieg nad tekstem z jedną zapomnianą kropką kończy się zerem.
Nad prozą pisaną ręką jest to usterka do zgłoszenia,
a nad `docs/` wraz z nagłówkami — nie,
i tej różnicy komenda o sobie nie wie, bo dostaje pliki, a nie ich rodzaj.
Ruchem jest flaga, po której `unclosed` liczy się do kodu wyjścia,
albo zdanie mówiące, czemu nie liczy się nigdy.
Do przeczytania jest przebieg nad README,
bo tam ta różnica rozstrzyga o przyrządzie pomiarowym
([`docs/roadmap.md`](../docs/roadmap.md#readme-jest-przyrządem-pomiarowym)).

Lista czytań mnoży odmiany zdań składowych, a mogłaby je sumować.
Wpisem na liście jest jedno czytanie, a streszczeniem czytania krotka
o słowniku na każde składowe (`describe` w `olski/parse/streszczenie.py`),
więc dwa składowe wieloznaczne każde na swój sposób dają tyle wpisów,
ile jest par ich odmian, po tyle wierszy każdy, ile zdanie ma składowych.
Cenę tę opisuje
[`docs/parsowanie.md`](../docs/parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)
i bierze ją świadomie, więc ten wpis odwraca decyzję, a nie naprawia przeoczenie.
Ruchem jest wpis na zdanie składowe wraz z odmianami tego jednego składowego,
czyli ten sam kształt, jaki ma wiersz o konstytuencie rozbieżnym
(`Rozbieżność` w `olski/parse/podsumowanie.py`): wpisów jest wtedy tyle, ile składowych,
a wierszy tyle, ile odmian wszystkich składowych razem.
Sam kształt jest tu łatwiejszy niż dwie decyzje, które on wymusza.
Pierwsza: czym jest to samo zdanie składowe w dwóch czytaniach,
skoro czytania rozcinają zdanie w różnych miejscach —
`Ludzie są wolni, równi i szczęśliwi.` ma czytanie o jednym składowym
i czytanie o dwóch, więc numer w krotce znaczy w nich co innego.
Druga: co liczy wtedy podpis `streszczenia odczytań` na witrynie
(`podpisOdczytań` w `witryna/skrypt.js`), bo odczytań liczyć przestaje.
Do przeczytania jest wydruk `python3 -m olski.check --readings` nad
`proza/README.txt` (`python3 -m harness.markdown README.md --into proza/`):
jedno zdanie tego pliku wychodzi tam kilkudziesięcioma streszczeniami,
a reszta pojedynczymi, więc ruch opłaca się samemu ogonowi rozkładu
i trzeba przeczytać, czy ogon jest wart osobnego kształtu listy.

Dwie sondy czytają Walentego i pytają go o różne schematy, a różnicy nie zmierzył nikt.
`harness/rama.py` odsiewa kwalifikatory `archaiczny` i `zły` przez `BRANE`,
bo schemat tak oznaczony nie należy do rejestru, o który olskiemu chodzi,
a `harness/konwersy.py` bierze wszystkie schematy lematu i o kwalifikator nie pyta wcale.
Jedna z dwóch odpowiedzi jest gorsza i nie wiadomo która:
liczba konwersów jest górnym oszacowaniem, które i tak myli się w jedną stronę
([`docs/disambiguation.md`](../docs/disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma)),
więc schemat archaiczny mógł ją podnieść, a mógł nie trafić w kryterium pary.
Ruchem jest przebieg `harness/konwersy.py` z tym odsiewem i bez niego,
a potem albo `BRANE` wspólne dla obu sond, albo zapisany powód, czemu jedna go nie chce.
Do przeczytania jest `_pewność` w `harness/rama.py` oraz dwanaście par,
które tamta sonda wypisuje: jeżeli odsiew rusza liczbę, to rusza i te pary,
a wtedy należy się ich przeczytanie, a nie sama poprawiona liczba.

Polecenie powtarzające pomiar luki zlepia siedem aktów `cat`-em,
a sonda bierze je teraz osobno.
Blok w [`docs/design-notes.md`](../docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)
pisze `cat proza/ustawy/*.txt > proza/ustawy-razem.txt` i mierzy nad zlepkiem,
gdzie `python3 -m harness.luka proza/ustawy/*.txt` mierzy nad tymi samymi aktami
i składa z nich jeden raport.
Ruchem jest podmiana obu wierszy na jeden, a przed nią przebieg nad tym rejestrem,
bo raport scalony równa się przebiegowi nad zlepkiem tylko wtedy,
gdy każdy plik kończy się znakiem kończącym zdanie:
inaczej zlepek skleja ostatnie zdanie jednego aktu z pierwszym zdaniem drugiego,
a raport scalony tego nie robi.
Nad prozą tego repozytorium sprawdzono, że obie drogi dają wydruk co do znaku ten sam;
nad rejestrem ustaw nie sprawdził tego nikt, a bez tego podmiana rusza figury
i nic o tym nie mówi.
Wpis podnosi więc sesja, która ten rejestr ma.

Przebieg puszczony spoza korzenia mierzy olskiego bez konfiguracji projektu
i nie mówi tego w wydruku.
`znajdź` w `olski/konfiguracja.py` szuka `olski.toml` od katalogu roboczego w górę,
a nagłówek wydruku (`render` w `olski/pokrycie.py`) nazywa sam korpus i morfologię,
więc ta sama komenda puszczona z dwóch katalogów wydaje dwie różne tabele,
a różnicy nie widać po żadnej z nich.
Ruchem jest nazwa czytanego pliku w tym nagłówku, wraz z odpowiedzią o jego braku,
bo brak konfiguracji jest odpowiedzią, a nie milczeniem.
Do przeczytania jest przedtem, czy `render` jest tu właściwym miejscem:
czyta go i pomiar nad korpusem, i `olski-pokrycie` nad jednym plikiem,
a wiersz dopisany rusza każdy blok, który stoi w dokumencie pod tą komendą
(`tests/test_wydruki.py`).

`olski` chodził po katalogu, a `olski-check` bierze tylko pliki.
Widać to w poleceniu, którym
[`docs/extraction.md`](../docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów: stoi przed nim `find`, bo inaczej nie ma czego podać.
Komenda, która po katalogu chodziła, wyszła razem z pakietem reguł,
a zejście po `rglob` ma dziś jedno miejsce i nie jest nim ta komenda:
`pliki_prozy` w `harness/__init__.py` bierze pod podanym katalogiem pliki
o rozszerzeniu, które pisze ekstrakcja, i schodzi tam dla każdej sondy.
Zawołać go stamtąd `olski/check.py` nie może:
import idzie w jedną stronę, a paczka niesie samo `olski`,
i oba te powody stoją w docstringu tamtego modułu.
Ruchy są więc dwa i różnią się tym, czyim faktem jest rozszerzenie prozy.
Rozszerzenie dokumentu jest już faktem olskiego (`CZYTNIKI` w `olski/wejście.py`),
więc pierwszy z nich ma precedens.
Albo zejście przenosi się do `olski/` razem z nim,
a wtedy `.txt` przestaje być faktem o ekstrakcji i staje się faktem o tym,
co `olski-check` podnosi z katalogu;
albo ta komenda dostaje własne zejście, a rozszerzenie zostaje w dwóch kopiach.
Po którymkolwiek z nich `find` z tamtego polecenia znika,
a razem z nim powłoka, którą polecenie bierze tylko po to,
żeby ktoś rozwinął mu glob.
Do rozstrzygnięcia zostają wtedy dwie rzeczy, których tamto zejście nie ma.
Pierwszą jest katalog o nazwie zaczynającej się kropką:
korpus stoi w repozytorium, a jego kontrola wersji korpusem nie jest,
więc pominięcie należy do chodzenia, a nie do testu na rozszerzenie,
i katalog z kropką podany wprost staje się przez nie nieosiągalny.
Drugą są pliki, które komenda minęła:
`olski-check` ma mianownik, który tamten dokument cytuje,
więc pominięcie w ciszy zmienia figurę, o której nikt się nie dowie,
a sonda mianownika stamtąd nie cytuje nigdzie i milczy o tym bez ceny.

Werdykt mówi jednym zdaniem trzy rzeczy, które są trzema różnymi robotami.
`no production takes „X”` pada i wtedy, gdy słownik czytania formy nie ma wcale,
i wtedy, gdy je ma, a nie sięga po nie żadna produkcja;
pierwsze naprawia wpis w `olski.toml`
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)),
a drugie produkcja w `olski/subset/`.
Trzecie jest formą, której czytania zdjęła morfologia:
`Cena niego rośnie.` wychodzi z tym komunikatem, a naprawą jest przyimek w zdaniu
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)),
czyli ani leksykon, ani produkcja.
Ta trzecia waży najwięcej na torze pisania pod tę gramatykę
([`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md)),
bo komunikat odsyła autora do gramatyki, a poprawka stoi w jego zdaniu.
Rozdziela ją już przebieg nad korpusem: `bloker` w `olski/pokrycie.py`
daje formie opróżnionej wykluczeniem wiersz osobny od zdania bez struktury,
więc po tamtej stronie kształt jest wybrany, a werdykt mówi o tej formie
to samo, co o dwóch pozostałych.
Rozdzielenia żąda ta sama własność, którą werdykt już realizuje raz —
forma bez licencji stoi osobno od struktury bez licencji — tylko o szczebel niżej,
i ma ona właściciela w [`docs/swigra.md`](../docs/swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold).
Kosztem jest wydruk, z którego jeden dokument wycina formy poleceniem:
[`docs/ustawy.md`](../docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
bierze wszystko, co stoi za frazą `no production takes` do średnika,
więc drugi komunikat rozsypuje tamto polecenie, jeżeli nie da się go wyciąć tak samo.
Do przeczytania jest `explain` w `olski/werdykt/zdanie.py`
obok `bez_licencji` w `olski/segmentacja.py`:
formy przychodzą tam jedną krotką, więc rozdzielenie ich żąda drugiego pola
w `Verdict`, a nie samego drugiego napisu.
Ruch ten stoi przed przekładem wydruku albo za nim, ale nie razem z nim:
tamta zmiana bierze na nowo ręką każdy blok werdyktu w dokumentach.

`harness/konwersy.py` liczy lematy, a pytanie pod nią jest o zdania.
Wraca ona ze 144 lematami z 17 224,
czyli mówi, ilu czasowników dotyczy rama, której zdanie przechodnie samo nie wybiera,
i nie mówi, jak często taki czasownik pada bez pozycji rozstrzygającej;
[`docs/disambiguation.md`](../docs/disambiguation.md#czego-brakuje-żeby-odpowiedzieć-pomiarem)
trzyma to jako czwartą rzecz nierozstrzygniętą.
Ruchem jest przebieg nad korpusem audytowym
([`docs/audit-corpus.md`](../docs/audit-corpus.md#the-list)):
dla każdego zdania, które olski przyjmuje, zapytać,
czy jego czasownik jest jednym z tych lematów i czy stoi przy nim pozycja wybierająca schemat.
Do przeczytania jest przedtem cała lista par, a nie dwanaście z niej,
bo sonda sądu o parze nie wydaje, a te dwanaście mówi,
że kryterium łapie głównie celownik posiadacza (tamże),
więc przebieg nad rejestrem wart jest dokładnie tyle, ile lista, na której stanie.

Dwie sondy stoją nad jedną populacją i wołają tych samych świadków.
`harness/powtórzenie.py` i `harness/wybory.py` pytają obie o `pytania` z
`harness/wieloznaczność.py` i obie wypisują odpowiedź wraz ze zdaniem, nad którym
padła; różni je to, że pierwsza wycenia wariantem granicę akapitu i regułę
kandydata, a druga ma obok wzorzec czytany ręką
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Ruchem jest jedna sonda z flagą na wariant, bo dwa przebiegi po tym samym korpusie
rozejdą się na pierwszej zmianie w tym, co liczy się za pozycję.
Do rozstrzygnięcia jest, co się wtedy dzieje z wydrukiem: sonda pierwsza liczy
mianowniki rejestru (zdania, pierwsze w akapicie, pozycje z sąsiedztwem), a druga
liczy trafienia wobec wzorca, i jeden wydruk z obojgiem czyta się jak dwa.
Ten sam argument stoi już w drugiej sondzie po jej własnej stronie:
losowania ma ona dwa, a mianownik każdego niesie plik z wpisami,
więc scalenie dodaje trzeci tryb do dwóch, a nie drugi do jednego.
Przeciw scaleniu jest to, że wzorzec przeżyje sondę: `próba/wybory.txt` stoi poza
`harness/` właśnie dlatego, a program czytający ten plik jest najtańszą rzeczą w tej parze.

Kolejka blokerów grupuje zatrzymania po części mowy, a nad wierszami zamkniętymi
zbiera pod jedną nazwą formy żądające różnych konstrukcji: wiersz `conj` prowadzą
nad tą prozą `i` oraz `a`, a pod nimi stoją `czy`, `czyli` i `ani`
([`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md#kolejka-czytana-po-formie-mówi-to-czego-nie-mówi-po-części-mowy)).
Ruchem jest `bloker` w `olski/pokrycie.py` nazywający formę tam, gdzie każde
jej czytanie należy do klasy zamkniętej (`CLOSED_CLASS` stoi w `olski/segmentacja.py`),
a część mowy tam, gdzie nie: dla `ustawienia` przydatna jest część mowy, dla `i` napis.
Do przeczytania jest, co taki wiersz zrobi z tabelami, które ten wydruk cytują —
[`docs/corpus.md`](../docs/corpus.md#where-the-analyses-stop) czyta wiersze `conj`
i `part` po nazwie — bo przemianowany wiersz żąda przeliczenia obu przebiegów
nad bankiem drzew, a nie samego dopisania zdania.
Wpis waży mniej, odkąd wiersz nazywa czytanie licencjonowane,
bo `interj` jest wierszem prawdziwych wykrzykników, a nie kryjówką dla `i`.

Sonda nad Świgrą pyta jej wydruk o czas i o łuki, a `info(trees, …)` z tego samego
wydruku pomija, więc różnicę, o którą w tym porównaniu chodzi najbardziej,
`harness/świgra.py` zostawia niezmierzoną.
Świgra liczy wyprowadzenia tam, gdzie olski liczy odczytania — `counttrees` w
`birnam_cleanforest.pl` mnoży poddrzewa, a `signature` w `olski/parse/czytanie.py` kwotuje po
lematach, wartościach cech i częściach mowy — i dziś rozstrzyga to samo czytanie
źródła ([`docs/swigra.md`](../docs/swigra.md#why-wrapping-it-does-not-get-there)).
Ruchem jest `trees` i `useful_edges` dopisane do `POLE`, kolumna w wydruku sondy,
a przed jednym i drugim trzecia poprawka z docstringu sondy, bez której obie te
liczby nie dochodzą do wydruku Świgry.
Decyzją, której to żąda, jest kwota: liczba drzew mówi o zapisie lasu, a nie o
wieloznaczności zdania, więc porównanie z liczbą odczytań musi powiedzieć, co nad
cudzym drzewem jest jednym kształtem — etykieta z rozpiętością czy samo nawiasowanie,
w którym łańcuchy jednoelementowe pomija się.
Druga decyzja jest o zakresie: docstring sondy deklaruje, że rzeczą mierzoną jest
czas, a nie kształt drzewa, więc ten wpis go odwraca, a nie dopracowuje.
Do przeczytania jest jedno zdanie puszczone obiema stronami: zdanie o koszcie szynki
z [`docs/subset.md`](../docs/subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)
wychodzi u Świgry tysiącami drzew, a u olskiego kilkoma odczytaniami,
a dopóki kwota nie jest wybrana, tych dwóch liczb nie ma jak zestawić.

Flaga `--readings` w `olski/check.py` jest po angielsku,
a stojące obok niej `--rozstrzygaj` i `--zatrzymania` po polsku,
choć [reguła językowa](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
obejmuje nazwy flag tak samo jak komunikaty, które komenda drukuje.
Ruchem jest `--odczytania` wraz z każdym wywołaniem w dokumentach;
bloki nad wydrukami pilnuje `tests/test_wydruki.py`, bo puszcza to, co w nich stoi,
a wystąpień w prozie nie pilnuje nic i te trzeba przejść grepem.
Do przeczytania jest przy tym
[`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md#czego-brakuje-najbardziej),
gdzie ta flaga stoi jako przykład tego, na co Morfeusz rozbiera nazwę z myślnikami.

Dwa miejsca tną zdanie interpunkcją na człony, a zbiory znaków mają różne.
`GRANICE_CZŁONÓW` w `olski/chwyty.py` bierze nawias i znak kończący zdanie,
`GRANICA` w `harness/wieloznaczność.py` bierze dywiz i żadnego z tych dwóch,
a różnicy nie zmierzył nikt.
Ruchem jest jedno cięcie w `olski/`, z którego sonda bierze swoje,
bo import idzie w tę stronę, a paczka niesie samo `olski`;
zbiór znaków staje się wtedy argumentem, jeżeli obie strony chcą różnych.
Do przeczytania są oba docstringi, bo deklarują różne rzeczy:
sonda myli się świadomie w stronę mniejszej liczby członów
i dywiz w środku formy jest tam ceną tej deklaracji,
a reguła chwytu pyta tylko o człon zamknięty zwrotem, więc dywiza nie potrzebuje.
Przed podmianą trzeba puścić sondę oboma cięciami:
jej liczby cytuje
[`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
więc cięcie zmienione bez pomiaru rusza figurę i nikt tego nie zobaczy.

`olski-check` szuka `olski.toml` od katalogu roboczego, a proza,
którą sprawdza, leży zwykle gdzie indziej.
Ekstrakcja pisze pliki `--into` dowolny katalog, więc kto puszcza komendę
stamtąd, dostaje werdykty bez leksykonu projektu i nic mu o tym nie mówi:
`olski` i `konstytuenty` wychodzą wtedy jako formy, których nie bierze żadna produkcja,
a te same pliki puszczone z korzenia repozytorium przechodzą.
Braku nie zgłasza się celowo, bo projekt bez konfiguracji jest zwykłym projektem
(`znajdź` w `olski/konfiguracja.py`),
i to zostaje; różnica jest w tym, że tu konfiguracja jest, a szukano jej nie tam.
Ruchem jest jedno z dwojga: szukanie od katalogu sprawdzanego pliku,
a nie od katalogu roboczego, albo wiersz w podsumowaniu nazywający
konfigurację, którą komenda przeczytała, albo jej brak.
Pierwsze psuje przypadek prozy wyekstrahowanej poza projekt, bo tam plik
nie leży w projekcie, a leksykon jest ten sam;
drugie nie naprawia nic, tylko pokazuje, i to wystarcza,
bo błąd jest w tym, że rozjazdu nie widać.
Do przeczytania jest `Podsumowanie` w `olski/werdykt/tekst.py`,
bo wiersz o konfiguracji stanąłby obok liczby zdań,
a `tests/test_wydruki.py` puszcza każdy blok tego wydruku w dokumentach.

Wydruk `olski-check` nazywa plik, a proza modułu leży w nim kawałkami,
więc autor dostaje zdanie i szuka go potem po całym module.
Dokument tego nie stawia, bo tam proza jest jedna i idzie w kolejności pliku.
Wiersz każdego kawałka jest policzony (`jednostki` w `olski/python.py`)
i jest kandydatem na drugie pole nagłówka wydruku.
Do przeczytania jest `main` w `olski/check.py`,
gdzie nagłówek wiersza jest nazwą źródła,
a wcięcie wierszy pod nim liczy się z jej długości,
więc numer dopisany do nagłówka rusza każdy blok wydruku w dokumentach,
a te pilnuje `tests/test_wydruki.py`.
Do rozstrzygnięcia jest, czy numer idzie do nagłówka przy każdym pliku,
czy tylko tam, gdzie proza przyszła kawałkami:
`proza` w `olski/wejście.py` wydaje dziś napis i o kawałkach nie mówi nic.

Obie komendy paczki biorą ścieżki i czytają je tak samo, a odpowiadają inaczej.
Plik nie do przeczytania jest dla `olski/check.py` tym, czego „nie udało się przeczytać”,
a katalog podany zamiast pliku dla `olski/pokrycie.py` tym, czego „nie ma”;
obie kończą wtedy kodem dwa.
Samo czytanie mają wspólne, odkąd prozę wyjmuje `proza` w `olski/wejście.py`,
więc niewspólny został komunikat i to, czego każda z nich od ścieżki żąda.
Ruchem jest druga funkcja obok tamtej, biorąca ścieżki
i wracająca parami (nazwa, proza) albo kodem dwa.
Do rozstrzygnięcia jest, czy komunikat ma dalej nazywać komendę,
bo funkcja wspólna nie wie, kto ją zawołał, dopóki nie dostanie nazwy argumentem.

`olski-check` nie daje wyboru znalezisk,
więc autor cudzej prozy dostaje albo wszystkie naraz, albo żadnego.
Każda flaga tej komendy dokłada wiersze,
a kod wyjścia niesie samą obecność znalezisk (`main` w `olski/check.py`).
Pierwszego kroku żąda od tej komendy cel o czytaniu wszystkich zgłoszeń
([roadmap.md](../docs/roadmap.md#cele)).
Ruchem jest flaga wybierająca klasę znaleziska,
bo rozdziału nie trzeba wyprowadzać:
`Result` w `olski/parse/podsumowanie.py` trzyma `przyłączenia` osobno od `rozbieżności`,
a zlewa je dopiero wydruk.
Świadka, który na wieloznaczność przyłączenia odpowiada, komenda ma już dziś:
`--rozstrzygaj` odpowiada nad przyłączeniem częstością banku drzew,
a znalezisko pada obok tej odpowiedzi tak samo jak bez niej.
Do rozstrzygnięcia jest, co wtedy niesie kod wyjścia,
bo dziś niesie każde znalezisko, a po wyborze niósłby wybrane.
Do przeczytania jest `harness/wieloznaczność.py`:
sonda liczy przyłączenie osobno od synkretyzmu,
więc mówi, ile które wyciszenie zdejmie,
a bez tej liczby flaga wybiera między klasami w ciemno.

Witryna nie pokazuje żądań pozycji, choć `--żądania` je drukuje.
API oddaje przeglądarce wykaz morfologii pod własnym kluczem
(`_zdanie` w `witryna/werdykty.py`), a wiersz żądania nie idzie tam wcale,
więc czytelnik strony widzi mniej niż czytelnik wiersza poleceń
([`docs/witryna.md`](../docs/witryna.md)).
Ruchem jest klucz obok tamtego wraz ze zwojem w `witryna/skrypt.js`,
bo wykaz na odczytanie strona już rysuje i wystarczy mu drugie źródło.
Do rozstrzygnięcia jest, czy napis o klasie nienazwanej powtarza się po stronie
przeglądarki, czy idzie z API gotowy:
frazę werdyktu ma na własność kod paczki, a ten napis wybiera dziś wydruk
(`KLASA_NIENAZWANA` w `olski/check.py`), więc strona wzięłaby go drugą kopią.

`--chwyty` bierze zdanie przytoczone w grawisach za zdanie dokumentu.
Przebieg nad prozą repozytorium stoi na zerze poza kilkoma takimi napisami,
z których jednym jest `To jest tanie.`,
bo ekstrakcja zdejmuje grawisy, a kropka w środku przykładu punktuje prozę wokół niego
([`docs/extraction.md`](../docs/extraction.md#what-the-reader-sees-is-not-always-polish)).
Reguła zastępująca orzeczenie dokłada tu drugi przypadek:
wyliczenie jej własnych zwrotów trafia w samo siebie,
bo przecinek za wstawką zamyka człon zwrotem.
Proza o tej regule — sekcja `docs/linter.md` i komentarz w `olski/chwyty.py` —
nazywa przez to te zwroty zdaniem z czasownikiem,
zamiast wyliczyć je po przecinku albo przytoczyć w przykładzie.
Odpowiedź na to pytanie repozytorium już ma, tylko po drugiej stronie granicy pakietów:
`wstawki` w `harness/cytaty.py` wyjmuje treść każdej wstawki kodowej parserem,
a `cytat` obok niej orzeka, czy ta treść jest zdaniem zacytowanym.
Do przeczytania są te dwie funkcje wraz z `_inline` w `olski/markdown.py`,
gdzie treść wstawki zostaje w prozie świadomie i gdzie ta wiedza już przechodzi.
Ruchem jest przeniesienie tego pytania do pakietu, bo `olski` z harnessu nie czyta nic
(`harness/__init__.py`), i wtedy warstwa chwytów pyta o nie zamiast zgadywać z wielkiej litery.
Do rozstrzygnięcia jest, czym ekstrakcja ma o tym mówić:
dziś wydaje napis, a rozpiętości wstawek nie ma w nim jak podać,
więc albo wraca parą, albo `olski-check` czyta dokument dwa razy.
Ceną drugiego wyjścia jest to, że zdanie zacytowane liczy się wtedy nad dokumentem,
a nie nad prozą, więc nie widzi go przebieg nad plikiem `.txt`.

Co olski umie powiedzieć nad zdaniem, wyliczają dwa miejsca.
Wydruk `olski-check` stawia po jednym wierszu na flagę (`olski/check.py`),
a `zgłoszenia` w `harness/usterki.py` zbiera z tego nazwy dla korpusu usterek.
Deklaracją jest `ZGŁOSZENIA` w `olski/werdykt/tekst.py`,
a wykrywacz dopisany przez nią drugiej listy nie kosztuje:
tak weszło `imiesłów bez podmiotu` i sonda usterek policzyła je bez zmiany w sobie.
Poza tą deklaracją zostają dwa zgłoszenia — chwyt rejestru spod `--chwyty`
oraz rzecz w pozycji osoby spod `--osoby` —
i ich nazwy `harness/usterki.py` wypisuje ręką,
więc zgłoszenie dopisane obok nich sonda przemilcza,
czyli wydaje liczbę nieprawdziwą i nie widać tego po niej;
to jest ten sam powód, z którego
[`CLAUDE.md`](../CLAUDE.md#code) zakazuje drugiej deklaracji podzbioru.
Ruchem jest wciągnięcie obu do tej deklaracji: nazwa zgłoszenia wraz z funkcją,
która je nad zdaniem znajduje, a wydruk i sonda pytają o nią.
Ceną jest wydruk, bo dziś każda flaga rysuje swój wiersz inaczej.
