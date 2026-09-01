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
(`Verdict.punktowane` w `olski/werdykt.py`),
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
o słowniku na każde składowe (`describe` w `olski/parse.py`),
więc dwa składowe wieloznaczne każde na swój sposób dają tyle wpisów,
ile jest par ich odmian, po tyle wierszy każdy, ile zdanie ma składowych.
Cenę tę opisuje
[`docs/design-notes.md`](../docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)
i bierze ją świadomie, więc ten wpis odwraca decyzję, a nie naprawia przeoczenie.
Ruchem jest wpis na zdanie składowe wraz z odmianami tego jednego składowego,
czyli ten sam kształt, jaki ma wiersz o konstytuencie rozbieżnym
(`Rozbieżność` w `olski/parse.py`): wpisów jest wtedy tyle, ile składowych,
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

`olski` chodził po katalogu, a `olski-check` bierze tylko pliki.
Widać to w poleceniu, którym
[`docs/extraction.md`](../docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów: stoi przed nim `find`, bo inaczej nie ma czego podać.
Komenda, która po katalogu chodziła, wyszła razem z pakietem reguł,
a chodzenia po drzewie nie ma teraz żadna z dwóch, które zostały:
`main` w `olski/check.py` i `main` w `harness/wieloznaczność.py`
czytają po prostu każdą podaną ścieżkę, więc obu rozwija się je powłoką.
Ruchem jest jedno miejsce, które schodzi po `rglob`,
bierze pliki o rozszerzeniu, które ekstrakcja pisze,
pomija katalog o nazwie zaczynającej się kropką — bo korpus stoi w repozytorium,
a jego kontrola wersji korpusem nie jest — i woła się z obu komend,
po czym `find` z tamtego polecenia znika,
a razem z nim powłoka, którą polecenia biorą tylko po to,
żeby ktoś rozwinął im glob.
Przeciw pominięciu: katalog z kropką podany wprost staje się wtedy nieosiągalny,
więc należy ono do chodzenia, a nie do testu na rozszerzenie.
Do rozstrzygnięcia jest, czy komenda mówi o plikach, które minęła:
`olski-check` ma mianownik, który tamten dokument cytuje,
więc pominięcie w ciszy zmienia figurę, o której nikt się nie dowie.
Sondy z `harness/` odpowiedziały na to pytanie odwrotnie i nie jest to niezgoda:
biorą one wiele plików prozy i rozwija im je powłoka,
bo katalog znaczy tam bank drzew i chodzenia po drzewie nie ma dla nich wolnego
(`harness/komenda.py`).
Kto ten wpis podnosi, ma więc precedens po obu stronach
i rozstrzyga, czy `olski-check` jest bliższy sondzie, czy dawnej komendzie.

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
Za tym średnikiem dopisuje się podpowiedź o cudzysłowie.
Do przeczytania jest `explain` w `olski/werdykt.py`
obok `bez_licencji` w `olski/segmentacja.py`:
formy przychodzą tam jedną krotką, więc rozdzielenie ich żąda drugiego pola
w `Verdict`, a nie samego drugiego napisu.
Ruch ten stoi przed przekładem wydruku albo za nim, ale nie razem z nim:
tamta zmiana bierze na nowo ręką każdy blok werdyktu w dokumentach.

`harness/luka.py` przepisuje z `harness/ruch.py` cały przebieg różnicowy:
liczniki, przejścia, scalanie kawałków, tryb nad prozą i tabelę,
czyli przeszło sto wierszy stojących drugi raz.
Wiersz poleceń zszedł z tej listy razem z `harness/komenda.py`,
który jest wspólny wszystkim sondom mierzącym nad korpusem,
a gramatyka wariantu zeszła z niej razem z `Sonda.gramatyki`:
wariant z luką jest dopiskiem, nie grupą zdejmowaną, i tamta sonda dopisek bierze.
Ruchem jest więc przepisanie tego pliku na tamten przebieg.
Do przeczytania są `pytania` i `Raport._konkurencja`, bo to one się nie generalizują:
warianty luki są dwiema wersjami jednego dopisku, a nie grupą na wariant,
więc pytanie o wchodzenie sobie w drogę nad nimi nie pada i pola zostają puste.
Ta sama `Sonda` zamyka drugie rozejście, które kopia zdążyła już zebrać:
oba tryby nad prozą w tym pliku wołają `check` raz na wariant,
więc segmentują ten sam tekst tyle razy, ile wariantów,
i tyle samo razy rozbierają zdanie, które olski odrzucił.
`harness/ruch.py` przestał tak robić i pomijanie zbędnych rozbiorów
ma tam jednego właściciela (`_bez_zbędnych`),
a bierze on `Sonda`, której ten plik nie ma.
Tej samej maszynerii żąda z drugiej strony wpis o porównaniu dwóch przebiegów
bez polecenia:
tam wariantem jest morfologia, a nie grupa produkcji zdjęta z olskiego,
więc ten, kto podnosi którykolwiek z dwóch, wybiera kształt dla drugiego,
i jest to jedna sesja.

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
([`docs/disambiguation.md`](../docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
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
[`docs/corpus.md`](../docs/corpus.md#where-the-analyses-stop) czyta wiersze `interp`,
`conj` i `part` po nazwie — bo przemianowany wiersz żąda przeliczenia obu przebiegów
nad bankiem drzew, a nie samego dopisania zdania.
Wpis waży mniej, odkąd wiersz nazywa czytanie licencjonowane,
bo `interj` jest wierszem prawdziwych wykrzykników, a nie kryjówką dla `i`.

Sonda nad Świgrą pyta jej wydruk o czas i o łuki, a `info(trees, …)` z tego samego
wydruku pomija, więc różnicę, o którą w tym porównaniu chodzi najbardziej,
`harness/świgra.py` zostawia niezmierzoną.
Świgra liczy wyprowadzenia tam, gdzie olski liczy odczytania — `counttrees` w
`birnam_cleanforest.pl` mnoży poddrzewa, a `signature` w `olski/parse.py` kwotuje po
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
z README wychodzi u Świgry tysiącami drzew, a u olskiego kilkoma odczytaniami,
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

[Zdanie spakowane](../CLAUDE.md#dla-kogo-jest-napisane-zdanie) wykrywa dziś tylko czytelnik,
a pierwszy z dwóch ruchów tej reguły jest policzalny:
formy osobowe w zdaniu daje Morfeusz,
a spójnik między nimi widać bez rozbioru.
Na [czterech osiach](../docs/linter.md#cztery-osie-każdej-reguły)
wypada to inaczej niż pakiet, który się zamknął:
pytanie jest o strukturę, a nie o uzus,
kształtem jest werdykt o zdaniu, a nie stopa nad tekstem,
a populacją jest nasza własna proza,
więc próg jest niepotrzebny i wszystkie trafienia i tak się czyta.
Głębokością jest morfologia, bo rozbioru nad tymi plikami nie ma:
gramatyka wyprowadza zdania README,
a `CLAUDE.md` i `docs/` pisane są bez tej ambicji.
Ruchem jest komenda nad prozą repozytorium, wzorowana na `olski/check.py`,
który już chodzi po zdaniach pliku, i na `harness/markdown.py`, który go czyta.
Drugi ruch reguły dzieli się na części o różnej cenie:
„tak samo”, „też” i „odwrotnie” w miejscu orzeczenia są listą słów,
a „napisane”, „go” i „co ją” żądają anafory, a anafory nikt tu nie zbudował.
Do rozstrzygnięcia jest, czy wpis kończy się na tej liście słów,
czy anafora dostaje własny wpis.
Do przeczytania są dwa zdania wiodące w
[sekcji o pomiarze](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje) —
o stosunku zgrubnym i o mierzeniu na przemian —
bo oba są spakowane i mówią, czego ta komenda ma nie przepuścić.
