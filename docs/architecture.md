# Architektura: warstwy i typy na ich granicach

Ten dokument wylicza warstwy, przez które przechodzi zdanie w obu kierunkach,
i nazywa typ, którym jedna warstwa oddaje wynik następnej.
Uzasadnień tu nie ma.
Mechanikę toru gramatycznego opisuje [design-notes.md](design-notes.md),
poziomy kompilatora [sklad.md](sklad.md),
cenę warstwy rozstrzygającej [disambiguation.md](disambiguation.md),
a o tym, co jest budowane, mówi [roadmap.md](roadmap.md#co-jest-budowane).

Warstwy wyszły z pisania kodu, a nie z projektu spisanego przed nim,
więc granica między dwiema bywa granicą modułu, a bywa granicą pakietu.
Opisane są takie, jakie wychodzą z importów,
wraz z jednym miejscem, w którym ich kolejność przeczy temu,
po co warstwa rozstrzygająca powstała.

## Warstwa albo wnosi wieloznaczność, albo ją zdejmuje

Warstw jest pięć i porządkuje je wieloznaczność,
bo o nią jedną wolno zapytać każdą z nich osobno.
Morfologia i składnia ją wnoszą:
słownik daje czytania formie, a gramatyka daje je zdaniu.
Znaczenie i tekst ją zdejmują:
pierwsze łączy czytania, które mówią to samo,
drugie odrzuca te, którym przeczy akapit.
Werdykt ani nie wnosi, ani nie zdejmuje,
bo jest wypowiedzią o czterech warstwach pod nim.

Podział ten nie pokrywa się z podziałem na tory.
Każdy tor przechodzi wszystkie pięć warstw,
tylko w przeciwnych kierunkach,
a wspólne mają dwie z nich.

## Pięć warstw toru gramatycznego

| warstwa | gdzie | wejście | wyjście |
| --- | --- | --- | --- |
| morfologia | `olski/morph.py`, `olski/projekt.py`, `admissible` w `olski/subset.py` | napis | `Segment`, czyli krawędzie grafu segmentacji |
| składnia | `olski/grammar.py`, `olski/parse.py` | krawędzie grafu | `Node`, po jednym na czytanie |
| znaczenie | `abstrahuj` w `olski/skład/rozbiór.py` | `Node` | `Odczyt`, czyli drzewa `Zdanie` wraz z powodami |
| tekst | `olski/rozstrzyganie.py` | wybory wraz z `Sąsiedztwo` | `Rozstrzygnięcie` albo wybór z powrotem |
| werdykt | `Verdict` w `olski/subset.py` | `Result` | status, role i to, co zostało otwarte |

Nazwy trzeciej i czwartej warstwy nie są nazwami mechanizmu, a poziomu,
na którym pytanie o wieloznaczność przestaje mieć tę samą odpowiedź.
Dwa czytania różne kształtem znaczą czasem to samo,
i o tym mówi warstwa trzecia,
której kryterium tożsamości opisuje
[subset.md](subset.md#co-się-liczy-jako-jedno-czytanie).
Dwa czytania różne znaczeniem bywają rozstrzygnięte przez zdanie obok,
i o tym mówi warstwa czwarta,
a co takie zdanie rozstrzyga, wycenia
[disambiguation.md](disambiguation.md#kontekst-rozstrzyga-wykluczeniem-a-nie-rankingiem).

## Warstwa rozstrzygająca wydaje zawężenie z powodem, a nie znaczenie

Typ tej warstwy jest trudniejszy niż typy czterech pozostałych,
bo tamte wydają strukturę, a ta odpowiedź o strukturze.
Sygnatura `rozstrzygnij` w `olski/rozstrzyganie.py` odpowiada wprost:
wybór wraca zamknięty wraz z powodem albo wraca taki, jaki wszedł.
Milczenie jest zatem wartością, a nie brakiem odpowiedzi,
i żąda tego od tej warstwy
[hipoteza](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza),
pod którą odpowiedź przychodzi z powodem albo nie przychodzi wcale.

Trzy własności wychodzą z takiego typu i żadna nie wychodzi z rankingu.

Zbiór kandydatów wyłącznie maleje,
więc świadkowie składają się w dowolnej kolejności,
a świadek dopisany później nie przywraca kandydata zdjętego wcześniej.

Milczenie obejmuje wybór, a nie zdanie,
więc jedno zdanie wraca rozstrzygnięte w jednym miejscu i otwarte w drugim.

Zbiór pusty znaczyłby, że akapit przeczy każdemu czytaniu,
czyli że zdanie kłóci się z tekstem, w którym je postawiono.
Odpowiedzi tej ta warstwa nie wydaje,
bo `rozstrzygnij` wybiera jednego gospodarza na przyłączenie
i pustki nie ma jak zwrócić.
Sprzeczność zdania z akapitem jest zatem wypowiedzią,
dla której poziom tekstu ma przesłankę, a ten typ nie ma miejsca.

## Werdykt liczy wyprowadzenia, bo powstaje pod dwiema warstwami, które liczą znaczenia

`Verdict` w `olski/subset.py` powstaje z czytań gramatyki,
czyli z wyjścia warstwy drugiej,
a warstwy trzecia i czwarta pracują obok niego i werdyktu nie ruszają.
„Zdanie wieloznaczne” znaczy wobec tego „ma kilka wyprowadzeń”,
a nie „ma kilka znaczeń”.
Różnicę między jednym a drugim mierzy przebieg nad korpusem audytowym,
w którym pozycję dwuznaczną niesie większość zdań rejestru,
a czytelnik nie waha się nad żadnym z przeczytanych ręką
([open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma)).

Od strony kodu tę samą różnicę bierze `sonda/znaczenia.py`:
puszcza czytania zdania przez warstwę trzecią
i pyta, czy wracają z niej tymi samymi drzewami
(`figury/znaczenia.txt`, `figury/znaczenia-live.txt`).
Odpowiedzi są dwie i pierwsza jest o mianowniku, a nie o wieloznaczności.
Nad bankiem drzew pytanie to daje się postawić kilku zdaniom
z tysiąca z górą, które olski melduje jako wieloznaczne,
bo nad resztą nie wraca ani jedno czytanie,
a nad prozą tego repozytorium nie daje się postawić żadnemu.
Kategorią, której brakuje najczęściej,
jest wyrażenie przyimkowe pod grupą imienną,
czyli dokładnie to przyłączenie, o które w tym pytaniu chodzi.
Warstwa trzecia zameldowanej wieloznaczności zatem nie zdejmuje,
tylko jej nie dosięga.
Nad tymi zdaniami, nad którymi ją dosięga, wieloznaczność zostaje:
czytania wracają drzewami rozłącznymi w każdym z nich,
i mówią to obie morfologie, choć żywa daje pytaniu populację kilka razy większą.

Druga odpowiedź jest o tym, jak ten pomiar wolno postawić.
Zdanie o jednym czytaniu wraca z tej warstwy kilkoma drzewami, najczęściej czterema,
bo napis milczy o relacji przyimka i o znaczniku tematu
([sklad.md](sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma)),
więc liczba drzew mierzy tę ciszę tak samo jak wieloznaczność.
Rozdziela je dopiero porównanie zbiorów drzew czytania z czytaniem,
i na tym kryterium stoi ta sonda.

Kolejność warstw jest zatem tym miejscem,
w którym architektura przeczy powodowi, dla którego czwarta powstała.
Warstwa rozstrzygająca powstała po to, żeby odpowiedzieć czymś ponad składnią,
a pyta o `Przyłączenie`, czyli o obiekt składniowy,
i widać to na jednym świadku:
powtórzenie frazy przy kopuli nie dowodzi niczego o tym czasowniku,
więc świadek kontekstowy nad taką parą milczy
([disambiguation.md](disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Ruch, który z tego wychodzi, wraz z tym, co przy nim przeczytać,
opisuje wpis w [TODO.md](../TODO.md).

## Warstwa znacząca leży w pakiecie drugiego toru

`abstrahuj` w `olski/skład/rozbiór.py` przechodzi z czytania parsera
na drzewo kategorii dziedziny, czyli jest warstwą trzecią toru gramatycznego,
a leży w pakiecie toru składu i importuje z niego morfologię,
opowieść, przyimki oraz składnię.
Wzięło się to z pytania, dla którego ta funkcja powstała:
obieg zamknięty pyta, czy z napisu wraca drzewo, które ten napis wypuściło,
a nie czy zdanie ma jedno znaczenie.

Granica pakietu jest tu rozstrzygnięciem, a nie przypadkiem,
i pilnuje go `tests/test_rozbiór.py`.
Moduł czyta gramatykę, a ta buduje się przy imporcie,
więc wpisany do `olski/skład/__init__.py` kazałby ją zbudować każdemu,
kto sięga po sam kompilator,
a parser przestałby być świadkiem obiegu i stałby się jego zależnością
([design-notes.md](design-notes.md#the-round-trip-invariant)).
Wołanie `abstrahuj` z toru gramatycznego przechodzi tę granicę w drugą stronę,
więc jest przestawieniem granicy pakietu, a nie przeniesieniem funkcji.

Warstwa ta jest przy tym cząstkowa i tym różni się od czterech pozostałych.
Dziedzinę ma ograniczoną tym, co `olski/skład/składnia.py` umie powiedzieć,
a gramatyka wyprowadza więcej,
więc krotka krótsza od liczby czytań wraca stąd z dwóch różnych powodów:
dwa czytania zeszły się w jedno albo któreś nie mieści się w tym zapisie.
Powód pierwszy jest zdjętą wieloznacznością, a drugi dziurą w kompilatorze,
i rozdziela je `Odczyt`, a nie sama długość krotki:
`powody` opisuje słowami kandydata, który odpadł,
a `kandydaci` mówi, czy ten zapis w ogóle miał czym odpowiedzieć.
Werdykt liczony nad wyjściem tej warstwy odrzucałby wobec tego zdanie,
którego gramatyka nie odrzuca,
i to jest cena, którą przestawienie kolejności warstw płaci.

## Oba kierunki dzielą typ, a nie kod

Warstwy trzecia i czwarta są w obu kierunkach te same,
bo w obu chodzi o te same dwa typy:
`Zdanie` oraz `Kontekst`, oba zadeklarowane w `olski/skład/składnia.py`.
`Kontekst` leży tam, a nie w `olski/skład/opowieść.py`,
bo niesie naraz to, co o zdaniu wie tekst — czas i to, kogo wolno pominąć —
oraz to, co o nim wie drzewo nad nim.
Dwa pola tekstowe wypełnia `Akapit` w `olski/skład/opowieść.py`,
a tożsamość, której lemat nie daje, niesie stojąca tam `Postać`.
Kategorie drzewa `Zdanie` należą do dziedziny, a nie do polszczyzny,
i wywód za tym poziomem trzyma
[sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka).
Co tekst wie ponad zdaniem, dowodzi tamten dokument osobno
([sklad.md](sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)).

| warstwa | gdzie | wejście | wyjście |
| --- | --- | --- | --- |
| tekst | `olski/skład/opowieść.py` | `Akapit`, czyli ciąg drzew `Zdanie` | `Kontekst` na każde zdanie, wraz z czasem i z tym, kogo wolno pominąć |
| znaczenie | `olski/skład/składnia.py` | konstruktory, które pisze autor | `Zdanie` |
| składnia | `kompiluj` w `olski/skład/__init__.py` | `Zdanie` | formy w kolejności, wraz z policzoną zgodnością |
| morfologia | `olski/skład/morfologia.py` | lemat wraz z żądanymi cechami | napis |
| przegląd | `olski/skład/przegląd.py` | napis w swoim tekście | role, których czytelnik z napisu nie odzyska |

Warstwy pierwsza, druga i piąta różnią się między kierunkami,
a różni je to, czego jeden z nich nie ma.
Kompilator nie ma wieloznaczności, bo z jednego drzewa wychodzi jeden napis,
więc nie ma w nim czego rozstrzygać ani o czym wydawać werdykt,
a `przegląd` pyta o co innego niż `Verdict`:
nie o to, ile czytań zdanie ma, ale o to, czy niesie te role, które je wypuściły.
Parser nie ma autora, który by powiedział, o kim mowa,
więc czyta to z akapitu przez `Sąsiedztwo`,
zamiast dostać gotowe w `Kontekst`.

Zasadę tę zapisuje docstring `olski/skład/rozbiór.py`:
wspólny oba kierunki mają typ, a nie kod.
Wymuszona symetria poniżej tych dwóch warstw
dołożyłaby każdej stronie warstwę, której ta strona nie potrzebuje.

Wspólny typ kupuje przy tym wzorzec, którego bank drzew nie daje.
Drzewo, z którego skład wypuszcza napis, zna czytanie, o które chodziło,
więc obieg zamknięty mierzy warstwę czwartą bez anotatora,
i wycenia to [disambiguation.md](disambiguation.md#wzorzec-na-tę-warstwę-jest-po-drugiej-stronie).
