# Architektura: warstwy i typy na ich granicach

Ten dokument wylicza warstwy, przez które przechodzi zdanie w obu kierunkach.
Nazywa przy tym typ wyniku, który jedna warstwa przekazuje dalej.
Uzasadnień tu nie ma.
Mechanikę toru gramatycznego opisuje [parsowanie.md](parsowanie.md),
a cenę tego toru opisuje [design-notes.md](design-notes.md).
Poziomy kompilatora opisuje [sklad.md](sklad.md).
Cenę warstwy rozstrzygającej liczy [disambiguation.md](disambiguation.md),
a jej zalążek opisuje [rozstrzyganie.md](rozstrzyganie.md).
O tym, co jest budowane, mówi [roadmap.md](roadmap.md#co-jest-budowane).

Warstwy wyszły z pisania kodu, a nie z projektu spisanego przed nim.
Granice między warstwami są granicami modułu albo granicami pakietu.
Kolejność warstw wychodzi tu z importów.
Jedno miejsce przeczy w niej temu, po co warstwa rozstrzygająca powstała.

## Warstwa albo wnosi wieloznaczność, albo ją zdejmuje

Wieloznaczność porządkuje pięć warstw,
bo o samą wieloznaczność wolno zapytać każdą warstwę osobno.
Morfologia i składnia ją wnoszą:
słownik daje czytania formie, a gramatyka daje je zdaniu.
Znaczenie i tekst ją zdejmują:
znaczenie łączy czytania, które mówią to samo,
a tekst odrzuca czytania sprzeczne z akapitem.
Werdykt nie wnosi wieloznaczności i nie zdejmuje jej,
bo jest wypowiedzią o czterech warstwach pod nim.

Podział ten nie pokrywa się z podziałem na tory.
Każdy tor przechodzi wszystkie pięć warstw w przeciwnym kierunku.
Dwie warstwy powtarzają się w obu torach.

## Pięć warstw toru gramatycznego

| warstwa | gdzie | wejście | wyjście |
| --- | --- | --- | --- |
| morfologia | `olski/morph.py`, `olski/projekt.py`, `olski/słownictwo.py`, `olski/segmentacja.py` | napis | `Segment`, czyli krawędzie grafu segmentacji |
| składnia | `olski/grammar.py`, `olski/parse/` | krawędzie grafu | `Node`, po jednym na czytanie |
| znaczenie | `abstrahuj` w `olski/skład/rozbiór.py` | `Node` | `Odczyt`, czyli drzewa `Zdanie` wraz z powodami |
| tekst | `olski/rozstrzyganie.py` | wybory wraz z `Sąsiedztwo` | `Rozstrzygnięcie` albo wybór z powrotem |
| werdykt | `Verdict` w `olski/werdykt.py` | `Result` | status, role i to, co zostało otwarte |

Nazwy trzeciej i czwartej warstwy nie są nazwami mechanizmu, a poziomu,
na którym pytanie o wieloznaczność przestaje mieć tę samą odpowiedź.
Dwa czytania o różnym kształcie znaczą niekiedy to samo
i o tym mówi warstwa trzecia,
której kryterium tożsamości opisuje
[subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie).
Niekiedy dwa czytania o różnym znaczeniu rozstrzyga zdanie obok.
Mówi o tym warstwa czwarta.
Co takie zdanie rozstrzyga, wycenia
[disambiguation.md](disambiguation.md#kontekst-rozstrzyga-wykluczeniem-a-nie-rankingiem).

## Warstwa rozstrzygająca wydaje zawężenie z powodem, a nie znaczenie

Typ tej warstwy jest trudniejszy od typów czterech warstw pozostałych,
bo tamte warstwy wydają strukturę, a ta warstwa wydaje odpowiedź o strukturze.
Sygnatura tej warstwy w `olski/rozstrzyganie.py` odpowiada wprost:
wybór wraca zamknięty wraz z powodem albo wraca otwarty.
Milczenie jest zatem wartością, a nie brakiem odpowiedzi,
i żąda tego od tej warstwy
[hipoteza](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza),
pod którą odpowiedź przychodzi z powodem albo nie przychodzi wcale.

Trzy własności wychodzą z takiego typu, a nie z rankingu.

Zbiór kandydatów wyłącznie maleje,
więc świadkowie składają się w dowolnej kolejności,
a świadek dopisany później nie przywraca kandydata zdjętego wcześniej.

Milczenie obejmuje wybór, a nie zdanie,
więc jedno zdanie wraca rozstrzygnięte w jednym miejscu i otwarte w drugim.

Zbiór pusty mówiłby, że akapit przeczy każdemu czytaniu.
Zdanie kłóciłoby się wtedy z tekstem, w którym je postawiono.
Odpowiedzi tej ta warstwa nie wydaje,
bo wybiera jednego gospodarza na przyłączenie i nie umie zwrócić pustki.
Sprzeczność zdania z akapitem jest zatem wypowiedzią,
dla której poziom tekstu ma przesłankę, a ten typ nie ma miejsca.

## Werdykt liczy wyprowadzenia, bo powstaje pod dwiema warstwami, które liczą znaczenia

Werdykt powstaje z czytań gramatyki, czyli z wyjścia warstwy drugiej,
a warstwy trzecia i czwarta pracują obok niego i werdyktu nie ruszają.
„Zdanie wieloznaczne” znaczy wobec tego „ma kilka wyprowadzeń”,
a nie „ma kilka znaczeń”.
Tę różnicę mierzy przebieg nad korpusem audytowym.
Pozycję dwuznaczną niesie tam większość zdań rejestru,
a czytelnik nie waha się nad żadnym przeczytanym zdaniem
([open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma)).

Od strony kodu tę samą różnicę bierze `harness/znaczenia.py`:
puszcza czytania zdania przez warstwę trzecią
i pyta, czy wracają z niej w tych samych drzewach.
Pytanie stawia się pod obiema morfologiami.

```sh
python3 -m harness.znaczenia Składnica-frazowa-180723/
python3 -m harness.znaczenia Składnica-frazowa-180723/ --morfologia live
```

Ten przebieg daje dwie odpowiedzi.
Pierwsza odpowiedź jest o mianowniku, a nie o wieloznaczności.
Pytanie to daje się postawić najwyżej kilku zdaniom na tysiąc
spośród tych, które olski melduje jako wieloznaczne,
bo nad resztą nie wraca ani jedno czytanie,
i mówi to tak samo bank drzew, jak i proza tego repozytorium.
Kategorią, której brakuje najczęściej,
jest wyrażenie przyimkowe pod grupą imienną,
czyli dokładnie to przyłączenie, o które w tym pytaniu chodzi.
Warstwa trzecia zameldowanej wieloznaczności zatem nie zdejmuje,
bo jej nie dosięga.
Nad tymi zdaniami, nad którymi ją dosięga, wieloznaczność zostaje:
czytania wracają w tych zdaniach w drzewach rozłącznych, i to bez wyjątku.
Mówią to obie morfologie i mówi to proza,
choć morfologia żywa daje pytaniu populację kilka razy większą niż złota.

Druga odpowiedź jest o tym, jak ten pomiar wolno postawić.
Zdanie o jednym czytaniu ma w tej warstwie kilka drzew.
Najczęściej ma cztery drzewa,
bo napis milczy o relacji przyimka i o znaczniku tematu
([po-wypisaniu.md](po-wypisaniu.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma)),
więc liczba drzew mierzy tę ciszę tak samo jak wieloznaczność.
Rozdziela je dopiero porównanie zbiorów drzew czytania z czytaniem
i na tym kryterium stoi ta sonda.

Kolejność warstw jest zatem tym miejscem,
w którym architektura przeczy powodowi, dla którego czwarta powstała.
Warstwa rozstrzygająca powstała po to, żeby odpowiedzieć ponad składnią.
Warstwa ta pyta jednak o `Przyłączenie`, czyli o obiekt składniowy.
Widać to na jednym świadku:
powtórzenie frazy przy kopuli nie dowodzi niczego o tym czasowniku,
więc świadek kontekstowy nad taką parą milczy
([rozstrzyganie.md](rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Ruch, który z tego wychodzi, opisuje wpis o świadkach pytających o obiekt składniowy
w [todo/rozstrzyganie.md](../todo/rozstrzyganie.md).

## Warstwa znacząca leży w pakiecie drugiego toru

Warstwa trzecia toru gramatycznego przechodzi z czytania parsera
na drzewo kategorii dziedziny.
Wypuszcza ją `olski/skład/rozbiór.py`, czyli moduł z pakietu toru składu,
i importuje z tego pakietu morfologię, opowieść, przyimki oraz składnię.
Wzięło się to z pytania, dla którego ta warstwa powstała:
obieg zamknięty pyta, czy z napisu wraca drzewo, które ten napis wypuściło.
O jedno znaczenie zdania obieg nie pyta.

Granica pakietu jest tu rozstrzygnięciem, a nie przypadkiem,
i pilnuje go `tests/test_rozbiór.py`.
Moduł czyta gramatykę, a gramatyka buduje się przy imporcie.
Po wpisaniu tego modułu do `olski/skład/__init__.py`
gramatykę budowałby każdy import samego kompilatora.
Parser przestałby wtedy być świadkiem obiegu i byłby jego zależnością
([design-notes.md](design-notes.md#the-round-trip-invariant)).
Wołanie z toru gramatycznego przechodzi tę granicę w drugą stronę,
więc jest przestawieniem granicy pakietu, a nie przeniesieniem funkcji.

Warstwa ta jest przy tym cząstkowa, a cztery warstwy pozostałe nie są cząstkowe.
Ogranicza jej dziedzinę to, co `olski/skład/składnia.py` umie powiedzieć,
a gramatyka wyprowadza więcej.
Krotka krótsza od liczby czytań wraca stąd z dwóch różnych powodów:
dwa czytania zeszły się w jedno albo któreś czytanie nie mieści się w tym zapisie.
Powód pierwszy jest zdjętą wieloznacznością, a powód drugi jest dziurą w kompilatorze.
Rozdziela je `Odczyt`, a nie sama długość krotki:
`powody` opisuje słowami kandydata, który odpadł,
a `kandydaci` mówi, czy ten zapis w ogóle miał czym odpowiedzieć.
Werdykt liczony nad wyjściem tej warstwy odrzucałby wobec tego zdanie,
którego gramatyka nie odrzuca.
Tę cenę płaci przestawienie kolejności warstw.

## Oba kierunki dzielą typ, a nie kod

Warstwy trzecia i czwarta są w obu kierunkach identyczne,
bo w obu kierunkach chodzi o te same dwa typy.
Typami tymi są `Zdanie` oraz `Kontekst`, a deklaruje je `olski/skład/składnia.py`.
`Kontekst` leży tam, a nie w `olski/skład/opowieść.py`,
bo niesie naraz to, co o zdaniu wie tekst, oraz to, co wie o nim drzewo nad nim.
Tekst wie czas zdarzenia i podmiot do pominięcia.
Dwa pola tekstowe wypełnia `Akapit` w `olski/skład/opowieść.py`,
a tożsamość, której lemat nie daje, niesie stojąca tam `Postać`.
Kategorie tego drzewa należą do dziedziny, a nie do polszczyzny.
Wywód za tym poziomem trzyma
[sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka).
Co tekst wie ponad zdaniem, dowodzi tamten dokument osobno
([kategorie-zapisu.md](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)).

| warstwa | gdzie | wejście | wyjście |
| --- | --- | --- | --- |
| tekst | `olski/skład/opowieść.py` | `Akapit`, czyli ciąg drzew `Zdanie` | `Kontekst` na każde zdanie, wraz z czasem i z tym, kogo wolno pominąć |
| znaczenie | `olski/skład/składnia.py` | konstruktory, które pisze autor | `Zdanie` |
| składnia | `kompiluj` w `olski/skład/__init__.py` | `Zdanie` | formy w kolejności, wraz z policzoną zgodnością |
| morfologia | `olski/skład/morfologia.py` | lemat wraz z żądanymi cechami | napis |
| przegląd | `olski/skład/przegląd.py` | napis w swoim tekście | role, których czytelnik z napisu nie odzyska |

Warstwy pierwsza, druga i piąta nie powtarzają się w obu torach,
a różni je to, czego jeden z kierunków nie ma.
Kompilator nie ma wieloznaczności, bo z jednego drzewa wychodzi jeden napis.
Nie ma w nim czego rozstrzygać, a werdykt nie ma czego liczyć.
Przegląd pyta o inną rzecz niż werdykt:
nie pyta o liczbę czytań zdania, a o role, które to zdanie wypuściły.
Parser nie ma autora, więc nie wie, o kim mowa.
Czyta to z akapitu przez `Sąsiedztwo`, a nie dostaje odpowiedzi w `Kontekst`.

Zasadę tę zapisuje `olski/skład/rozbiór.py`:
oba kierunki mają wspólny typ, a nie wspólny kod.
Wymuszona symetria poniżej tych dwóch warstw
dałaby każdej stronie warstwę, której ta strona nie potrzebuje.

Wspólny typ kupuje przy tym wzorzec, którego bank drzew nie daje.
Drzewo, z którego skład wypuszcza napis, zna czytanie, o które chodziło,
więc obieg zamknięty mierzy warstwę czwartą bez anotatora
i wycenia to [disambiguation.md](disambiguation.md#wzorzec-na-tę-warstwę-jest-po-drugiej-stronie).
