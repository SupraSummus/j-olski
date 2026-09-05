# Roadmap

Uporządkowanie, a nie harmonogram.
Dat tu nie ma, bo nikt na żaden etap nie czeka,
a plan z datami zamienia tę robotę w pracę.

Plik odpowiada na trzy pytania.
Co olski obiecuje autorowi, mówi [umowa](#podzbiór-jest-umową-a-nie-zasięgiem).
Po czym poznać, że obietnica jest spełniona, mówi [lista celów](#cele).
Czego olski nie obiecuje, mówią [dwie sekcje](#czego-olski-nie-robi)
[o tym](#czego-ten-tor-nie-obejmuje), po jednej na tor.

Numerowanych etapów ten plan nie ma i nie ma ich świadomie,
więc nikt nie przywraca ich przez przeoczenie.
Etap dostawał kryterium wyjścia, bo „kiedy to jest skończone”
jest tą częścią planowania, która regularnie na siebie zarabia.
Tor gramatyczny końca nie ma, więc jego odcinki dostawały kryteria wyjścia
dla czegoś, co się nie kończy, a numeracja obiecywała kolejność zależności,
której dwa z tych odcinków u siebie zaprzeczały.
Co z nich zostało, rozeszło się do właścicieli:
otwarta robota do `todo/`,
wiedza o cenie pozycji do
[corpus.md](corpus.md#kolejka-obiecuje-więcej-niż-pozycja-oddaje),
a wywód o konstrukcji do jej sekcji w [subset.md](subset.md).
Tor składu zachowuje kryterium wyjścia, bo tor ten się kończy,
i mówi o tym [jego sekcja](#kryterium-wyjścia-toru-składu-to-znów-readme).

## Co jest budowane

Sprawdzacz polskiego tekstu dla autora, który pisze po polsku
i chce znaleźć w tekście usterki głębsze niż literówka i błąd składni:
zaimek, którego nie da się rozwiązać, imiesłów bez podmiotu,
orzeczenie, które nie nazywa wykonawcy.
Autorem bywa człowiek, a bywa agent AI,
i dla tego drugiego narzędzie jest sposobem na dobrą polszczyznę,
choćby kosztowało go więcej pracy nad zdaniem.
Werdykt jest deterministyczny i wyjaśnialny,
bo autor ma wiedzieć, czemu zdanie dostało zgłoszenie, i ma móc to dostroić.
Dlatego pod spodem jest gramatyka pisana ręką, a nie model,
którego parametrów nikt nie przeczyta.
Jakich zgłoszeń autor potrzebuje, wylicza korpus usterek
([niżej](#kolejkę-ustawia-korpus-usterek-a-nie-kolejka-blokerów)).

Tor gramatyczny:
parser zaprojektowanego podzbioru polszczyzny,
który zwraca wszystkie odczytania zdania i zostawia wybór autorowi,
oraz narzędzie nad nim, które sprawdza polski tekst i zgłasza znaleziska.
Wieloznaczność jest odpowiedzią, a nie znaleziskiem:
werdykt mówi, że zdanie wyprowadza się na kilka sposobów, i na jakie,
a kodu wyjścia tym nie rusza.
Zdanie, którego gramatyka nie wyprowadza, jest znaleziskiem tylko wtedy,
gdy dzieli je od czytania jeden znak;
poza tym werdykt mówi o nim tyle, dokąd analiza doszła.
[subset.md](subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)
jest właścicielem obu tych decyzji,
a [swigra.md](swigra.md#what-it-leaves-open) opisuje puste pole, które zastał przegląd:
najbliższy istniejący parser polszczyzny rozstrzyga tam, gdzie olski zgłasza.
Maszyneria jest tym wszystkim, co [parsowanie.md](parsowanie.md)
mówi o Earleyu, lesie rozbiorów i swobodnym szyku,
oraz tym, co [design-notes.md](design-notes.md) mówi o LCFRS.

Za budowaniem tego przemawia kształt takiego werdyktu.
Mówi on o zdaniu, które wskazuje.
Reguła mierząca stopę wzorca na tysiąc słów tego nie mówi:
jest raportem o dokumencie, a nie zarzutem wobec zdania
([generated-polish.md](generated-polish.md#the-closing-sentence-is-measurably-different)),
a wystąpienie, w które trafia, wskazuje po to,
żeby dało się sprawdzić liczbę, i nie twierdzi o nim nic.

Tor składu idzie w drugą stronę:
wchodzi drzewo tego, co ma zostać powiedziane, a wychodzi polskie zdanie.
Kategorie tego drzewa są kategoriami dziedziny, a nie polszczyzny,
i to jest decyzja, która czyni ten tor tym, czym jest,
bo rozbioru zdania pisanego z góry nikt nie chce pisać
([sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)).
Zgodność jest tu liczona, a nie sprawdzana,
więc trudność, dla której olski istnieje, przy tym kierunku nie powstaje,
a gramatyka podzbioru nie jest temu torowi potrzebna do niczego
([design-notes.md](design-notes.md#the-round-trip-invariant)).

Ten tor ma jednak drugą robotę, i przez nią oba tory się widzą.
Propozycja, którą narzędzie podaje autorowi, jest napisem,
a napis z drzewa wypuszcza linearyzacja i nic poza nią,
więc [cel o uproszczeniu](#cele) stoi na składzie tak samo jak na parserze.
Parser zostaje w tamtym niezmienniku świadkiem,
a w tym celu jest połową maszyny.

Linter stylu dla polskiej dokumentacji technicznej stał obok, na torze opcjonalnym.
Jego pakiet reguł jest wycofany, o czym [niżej](#wycofany-jest-pakiet-reguł).
Sam linter został celem.
[Lista celów](#cele) nazywa go wykrywaczem wzorców prozy.
Cztery odwrócenia prowadzą do tego stanu i żadne nie ma wracać przez przeoczenie:
linter stał tu najpierw jako cel, a gramatyka jako tor obok niego,
potem gramatyka stała jako cel, a linter jako tor,
potem narzędzie nad gramatyką zgłaszało znaleziska,
wśród których wieloznaczność była jednym, a nie definicją olskiego,
a na końcu wieloznaczność przestała być znaleziskiem,
bo baza sądów nie potwierdziła ani jednego jej zgłoszenia
([subset.md](subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)).

## Podzbiór jest umową, a nie zasięgiem

Olski oznaczy zdania poprawne po polsku i ma je oznaczać.
Umowa z autorem brzmi tak: albo pisze po polsku i odpowiada za jakość sam,
albo rezygnuje z części polszczyzny, a wtedy olski pomaga mu tej jakości pilnować.
Podzbiór jest tym, z czego autor rezygnuje, czyli ceną, którą za tę pomoc płaci.

Zasięgiem podzbiór nie jest, i zmienia to, czego od niego chcemy.
Zasięg ma rosnąć, aż obejmie polszczyznę.
Umowa ma być warta podpisania, a to jest inny warunek:
lista tego, [czego olski nie bierze](subset.md#what-it-does-not-cover-yet),
nie ma być pusta — ma być tania.
Ile autor traci, wchodząc w środek, wycenia
[pisanie-po-olsku.md](pisanie-po-olsku.md#kto-płaci-za-odrzucone-zdanie).
Rachunek ma tam trzy strony, bo autor jest zarazem tym, kto dopisuje produkcje.
Autor, który olskiego tylko używa, tego drugiego ruchu nie ma
i zostaje mu jeden: przepisać zdanie albo odpowiadać za nie sam.

**Jednostką umowy jest tekst, bo jednostką sprawdzaną jest tekst.**
Czy zdanie dostanie zgłoszenie, rozstrzyga zdanie przed nim.
`Są one czerwone.` jest zdaniem dobrym po `Widzimy pole maków.`
i wieloznacznym po `Maki rosną w garnkach.`,
bo `one` zgadza się tam z dwiema grupami imiennymi naraz,
a przed pierwszym zdaniem tekstu nie ma czym rozwiązać `one` w ogóle.
Zgłoszenie to olski wydaje i jest ono drugim z jego znalezisk;
zaimki, które bierze, i granicę sąsiedztwa trzyma
[subset.md](subset.md#zaimek-wskazujący-na-dwie-rzeczy-jest-drugim-znaleziskiem).
Rachunek prowadzi zgodność, a nie znaczenie:
`one` niesie liczbę mnogą i rodzaj niemęskoosobowy,
więc kandydatów wylicza morfologia, a wybór między dwoma zostaje przy autorze,
tak jak zostaje przy nim wybór między czytaniami jednego zdania.
Że `czerwone` orzeka się o makach, a nie o garnkach, rozstrzyga znaczenie,
i tego olski nie rozstrzyga.

Umowa na pojedyncze zdanie nie stoi właśnie z tego powodu.
Zdanie zostawione poza podzbiorem jest w tym rachunku dziurą,
więc psuje zgłoszenia w zdaniach po sobie, a autor nie ma jak tego zobaczyć.
Umowę podpisuje się przez to na cały tekst.

Zmiana jednostki ma dwie ceny i obie były znane, zanim zapadła.
`olski.check -c`, które dostaje zdanie bez sąsiedztwa,
przestaje mówić to samo, co przebieg nad plikiem, w którym to zdanie stoi.
A przestawienie akapitu rusza werdykt nad zdaniem, którego nikt nie ruszył,
czyli autor traci pewność, że odpowiedź zależy od zdania, które napisał.
Za nie kupujemy zgłoszenia, których w jednym zdaniu nie widać wcale,
oraz zgodność obu kierunków:
`olski/skład/przegląd.py` mierzy napis w tym kontekście,
którym linearyzacja go składała,
więc po tamtej stronie jednostką jest zdanie na swoim miejscu już dziś.

**Jedna granica stoi ponad umową: czy polszczyzna ma dany napis.**
Napisu, którego polszczyzna nie ma, gramatyka nie bierze za żadną cenę,
bo obietnicą podzbioru jest, że każde zdanie olskiego jest zdaniem polskim,
a produkcja wpuszczająca taki napis odbiera tę obietnicę wszystkim zdaniom naraz
([pisanie-po-olsku.md](pisanie-po-olsku.md#ruchy-są-dwa-i-spotykają-się-w-punkcie-kompromisu)).
Odrzucenie jest przy tym uczciwe dopiero wtedy,
gdy oba czytania mają gdzie się wyprowadzić.
Zdanie odrzucone za wieloznaczność, której gramatyka nie umie pokazać,
mówi o brakującej pozycji, a nie o polszczyźnie,
i dlatego razem z decyzją o przyłączaniu wyrażeń przyimkowych
weszły do gramatyki wszystkie pozycje okolicznika
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)).

**Drobny druk umowy jest zmierzony i mówi, że w jednym miejscu olski jakość obniża.**
Pisanie pod tę gramatykę popycha w pięć chwytów,
a zdanie zanegowane wychodzi tańsze o jedno czytanie niż to samo twierdzenie,
czyli gramatyka nagradza rejestr, który reguły prozy karzą
([pisanie-po-olsku.md](pisanie-po-olsku.md#cena-którą-olski-zostawia-w-prozie)).
Umowa musi ten druk nieść, bo obiecuje jakość,
a w tym jednym miejscu wydaje jeden rytm na wszystko.

## Po co tory są dwa

Tory są dwa, a robota jedna: oba kończą się jakością zdania, które ktoś przeczyta.
Różni je moment.
Skład rozstrzyga o tej jakości przed zdaniem,
bo drzewo wchodzi jednoznaczne i zgodność się w nim liczy
([wyżej](#co-jest-budowane)).
Gramatyka rozstrzyga po zdaniu,
bo werdykt liczy odczytania, które napisane zdanie już ma.

Paralela z programowaniem nazywa ten moment.
Kompilator wypuszcza program z zapisu wyższego poziomu,
a linter czyta zapis pisany ręką,
i tak dzielą się tory: skład jest tym pierwszym, a parser tym drugim.
Dalej paralela nie prowadzi, bo kod źródłowy i program są dwiema rzeczami,
a nad polszczyzną rzeczą jest samo zdanie.
Drzewo istnieje wtedy, gdy ktoś je napisał,
więc nad tekstem napisanym po polsku nie istnieje żadne.
Pytanie „czym jest ten tekst” nie ma zatem odpowiedzi,
a ma ją pytanie o autora: na jakim poziomie pisze.
Pisze nad zdaniem, czyli drzewem, albo w zdaniu, czyli po polsku.
Poziomy, między którymi ten wybór przebiega, wylicza
[sklad.md](sklad.md#three-architectures).

Autorowi, który pisze w zdaniu, wycofanie tamtego pakietu zostawia edytor pokazujący,
co gramatyka dopuszcza na następnej pozycji:
zdania spoza podzbioru nie da się wtedy napisać, więc nie ma czego diagnozować
([sklad.md](sklad.md#the-predictive-editor-changes-this)).
Ten edytor podpisuje [umowę](#podzbiór-jest-umową-a-nie-zasięgiem) z góry,
zamiast przedstawiać ją autorowi nad zdaniem już napisanym.

Oba końce spina niezmiennik obiegu:
zdanie wychodzi ze składu i wchodzi do parsera,
a rozjazd wskazuje usterkę składu
albo konstrukcję olskiego, której nie da się przeczytać z powrotem jednoznacznie
([design-notes.md](design-notes.md#the-round-trip-invariant)).
Paralela tego nie ma, bo binarki nikt nie rozbiera, żeby sprawdzić kompilator.

Celem to nie jest, bo nie mówi, czym by się to sprawdziło,
a tego [lista celów](#cele) żąda od każdej swojej pozycji.
Mówi, po co tory są dwa, i o to pyta się celu kandydującego:
czy poprawia zdanie przed napisaniem, czy mierzy je po napisaniu,
czy zamyka obieg między jednym a drugim.

## Tor gramatyczny nie ma końca

Kryterium wyjścia tego toru było [README](../README.md) tego repozytorium:
każde jego zdanie miało się wyprowadzić i wyprowadzić raz.
Nie ma go z dwóch powodów.

Jedno czytanie na zdanie jest nad tym plikiem nieosiągalne,
i nie dlatego, że jest daleko.
Zdania README, które wychodzą wieloznaczne, są wszystkie tej samej klasy —
olski widzi w nich dwa czytania, a czytelnik jedno
([corpus.md](corpus.md#where-the-analyses-stop)) —
a w większości robi to przyłączenie wyrażenia przyimkowego,
o którym olski nie wybiera
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)).
Rozstrzyga o tym znaczenie, więc żadna produkcja tego nie zdejmie.
Kryterium nieosiągalne jest kryterium innego rodzaju, niż było opisane,
a to, że z trzech wyjść wybrano właśnie to, zapisuje
[open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma).

Zbiór zdań, którym się mierzyło, był przy tym w rękach tego, kto mierzy.
Każdy inny korpus tego repozytorium jest przypięty —
wydaniem, commitem albo adresem ELI — a README rusza każdy commit,
który dotyka jego prozy, i nie dogoni tego żadna reguła przeliczania.
Odległość do takiego celu skraca i dopisana produkcja, i przeredagowany akapit,
a wydruk nie mówi, które z dwojga zaszło.
Zdanie „README stoi, a rusza się gramatyka” było więc obietnicą,
a nie własnością pomiaru.

## Kierunek: werdykt ma mówić prawdę o tekście

Zostaje kierunek: czytania, które olski melduje,
mają być dokładnie tymi, które polszczyzna nad tym tekstem ma.
Pokrycie jest skutkiem takiego kierunku i mierzy się je osobno.

Prawda o zdaniu jest połową tego żądania i jest połową starszą.
Cztery szyki podmiotu, dopełnienia i czasownika są jej przykładem.
Nie ma ich w żadnej kolejce blokerów, bo szyk nie jest formą,
na której analiza staje, i żaden korpus o nie nie prosił.
Prosił o nie werdykt: dopełniacz negacji stojący przed swoim czasownikiem
nie miał ciała, więc olski czytał pięć zdań Składnicy odwrotnie,
niż czyta je czytelnik, i mówił to jednym czytaniem.
Dopisane, kupują kilkadziesiąt zdań banku drzew, kosztują sześć produkcji
i cztery z tych sześciu są tamtą naprawą.
Pokrycie wyszło więc skutkiem, dokładnie tak, jak ten kierunek mówi, że wyjdzie.

Zaimki `kto` i `co` są pierwszym dopisaniem, po którym pokrycie spadło,
i mówią o tym kierunku to, czego tamten przykład nie mówi
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Zdania z nimi wyprowadzały się przedtem ciągiem współrzędnym,
czyli czytaniem, którego polszczyzna nie ma,
a pokrycie liczyło każde z nich jako sukces.
Odebranie tym zaimkom pozycji rzeczownej zabiera to czytanie wszystkim naraz,
więc nad bankiem drzew zdań przyjętych ubywa kilkanaście,
a nad prozą tego repozytorium przybywa ich kilka.
Wybór między tymi dwiema liczbami rozstrzyga kierunek, a nie ich suma:
werdykt, który stoi na czytaniu nieprawdziwym,
jest miejscem, gdzie pokrycie i prawda mówią co innego,
i wtedy jedno z dwojga trzeba wybrać.

**Czytanie, którego polszczyzna nie ma, wolno odebrać dwiema drogami.**
Pierwsza pyta, co słownik oferuje, i tą drogą chodzi
`admissible` w `olski/segmentacja.py`
([warstwa-leksykalna.md](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).
Druga pyta, co produkcja licencjonuje,
i tańsza bywa właśnie ona: formy paradygmatu `ten` niosły czytanie rzeczownikowe
licznie, a zdjął je warunek mówiący, że zaimek rzeczowny nie rządzi dopełniaczem
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)).
Która droga jest tańsza, rozstrzyga się osobno przy każdej klasie,
a każde kryterium szersze, jakie na te klasy zaproponowano, zmierzono
i żadne nie stoi
([warstwa-leksykalna.md](warstwa-leksykalna.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi)).
Decyzja, że klasy się nie da wykluczyć, jest tu odpowiedzią, a nie porażką:
wykluczenie zbyt szerokie zabiera zwyczajne polskie słowa.

Prawda o tekście jest połową nowszą i jej żąda
[jednostka umowy](#podzbiór-jest-umową-a-nie-zasięgiem).
Zaimek bez antecedensu, orzeczenie wzięte ze zdania obok
i odesłanie do całego poprzedniego zdania
są czytaniami, o których jedno zdanie nie mówi nic,
bo zdanie nie wie, o kim mowa była przed chwilą
([kategorie-zapisu.md](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)).

Kolejność dopisań robi koszt przepisywania.
To, co każda późniejsza produkcja ma realizować, wchodzi przed nią,
bo dopisane potem każe przepisać je wszystkie.
Tak weszła decyzja o przyłączaniu wyrażeń przyimkowych przed produkcjami,
które ją realizują, i tak weszła walencja przed konstrukcjami,
w których każdy czasownik stoi:
wieloznaczność, którą wnosi jej brak, nie jest jedna na gramatykę,
tylko jedna na czasownik razy konstrukcje, w których ten czasownik stoi
([walencja.md](walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)).
Tak samo czytanie, którego polszczyzna nie ma,
zdejmuje się przed konstrukcjami, w których by wróciło.
Formalizm tej kolejności nie ma,
bo kierunek mówi, co ma zajść nad tekstem, a nie czym ma być wyprowadzone
([design-notes.md](design-notes.md#formalizm-jest-środkiem-a-nie-celem)).

## Cele

Kierunek prowadzi tor, a cel mówi, po co to wszystko jest.
Cel wolno mieć nieosiągnięty, dopóki mówi, co by go osiągnęło.
Lista jest zbiorem, a nie kolejnością, i żaden z celów nie czeka na inny.
Żaden z nich nie kończy przy tym toru gramatycznego:
cel nieosiągalny nie jest kryterium, a osiągnięty nie zamyka toru.

Dwa powody, dla których README przestało być kryterium
([wyżej](#tor-gramatyczny-nie-ma-końca)), dają dwie zasady,
które cel z tej listy ma wytrzymać.
Pierwsza: cel nazywa, czym się go sprawdza.
Nieosiągalny cel jest dopuszczalny, niesprawdzalny nie.
Druga: cel nad tekstem, który sami piszemy, mierzy zdolność, a nie udział,
bo udział skraca też przeredagowany akapit.
Trzecia zasada przychodzi z wycofanego pakietu ([niżej](#wycofany-jest-pakiet-reguł)),
gdzie etap, na który nikt nie czeka, okazał się zaległością, a nie planem:
cel, którego nikt nie podnosi, kasuje się razem z pracą, którą niósł.

Pierwszy cel pyta o cały korpus usterek.
Dwa następne pyta się o jedno zdanie, a dwa ostatnie o tekst.
Podział ten idzie za [jednostką umowy](#podzbiór-jest-umową-a-nie-zasięgiem)
i mówi, ile każdy cel potrzebuje zobaczyć, a nie który jest ważniejszy.

**Każde zgłoszenie z korpusu usterek jest wykryte, a wpis czysty nie ma szumu.**
`próba/usterki.txt` wylicza zdania z usterką, którą czytelnik by poprawił,
wraz z poprawką, nad którą zgłoszenie ma milczeć,
i zdania czyste, nad którymi ma milczeć wszystko, co autor ma poprawić.
Wiersz o odczytaniach nie jest tam szumem, bo poprawiać nad nim nie ma czego
([subset.md](subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)).
Widać to na `Operator ustala priorytet.`, które stoi w korpusie wpisem czystym:
czytelnik ma nad nim jedno czytanie, a olski dwa, i tak ma zostać
([wyżej](#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).
Sprawdza go `python3 -m harness.usterki`,
a cel jest osiągnięty, gdy każdy wpis wychodzi wykryty albo czysty.
Ten sam przebieg ustawia kolejkę roboty
([niżej](#kolejkę-ustawia-korpus-usterek-a-nie-kolejka-blokerów)):
wpis nieczytany żąda produkcji, wpis w ciszy żąda wykrywacza,
a szum żąda zawężenia tego, co już pada.
Cel mierzy zdolność, a nie udział,
bo zdania korpusu nikt nie przepisuje pod gramatykę:
przepisać wolno poprawkę, a zdanie z usterką ma zostać usterką.
Korpus rośnie zdaniem, które autor chciał zgłoszone, a olski przemilczał,
i nie rośnie zdaniem dopisanym pod wykrywacz, który już stoi.

**Wzorzec prozy ma wykrywacz, a repozytorium jest od niego czyste.**
Wzorce, których w prozie nie chcemy — zdanie echo, wzmacniacz bez treści,
peryfrazę, czasownik domowy — wylicza
katalog chwytów w `CLAUDE.md`,
a sprawdza je przegląd zmian, czyli człowiek czytający zdanie po zdaniu.
Cel żąda, żeby wzorzec raz nazwany dostał wykrywacz,
a wykrywacz przeszedł po całej prozie repozytorium i stanął na zerze.
Sprawdza go przebieg, a nie udział, więc przeredagowanie akapitu jest tu robotą.
Ten cel jest linterem tego repozytorium.
Wycofanego pakietu nie wskrzesza, a różni je populacja:
tamten zestaw reguł strzelał nad cudzą polszczyzną i żądał kalibracji,
której się nie doczekał,
a ten chodzi po tekście, za który odpowiadamy,
więc trafienia czyta się wszystkie, zamiast progować ich stopę.
Tę różnicę rozkłada na osie
[linter.md](linter.md#cztery-osie-każdej-reguły),
a jak dobrać i wycenić następną regułę, mówi
[ten sam plik](linter.md#kolejna-reguła-zaczyna-się-od-zdania-z-usterką-a-kalibracja-przychodzi-przed-awansem).
Milczenie kosztuje przy tym zero:
zdanie, którego olski nie wyprowadza, zostaje przy przeglądzie,
czyli przy tym, co je dziś sprawdza,
więc cel nie żąda od tych dokumentów, żeby zmieściły się pod gramatykę.
Osiągnięty, unieważni zdanie z `CLAUDE.md`,
że treści reguł prozy nie pilnuje żaden check, a pilnuje jej przegląd;
póki nie jest osiągnięty, zdanie to obowiązuje.
Wykrywacz mają już pierwsze wzorce i przebieg nad nimi stoi na zerze
([linter.md](linter.md#wykrywacz-chwytu-zgłasza-to-bez-rzeczownika-przy-sobie)).
Populacją są przy tym i dokumenty, i moduły,
bo docstring oraz blok komentarza są prozą tych samych reguł,
a `olski-check` czyta jedno i drugie
([extraction.md](extraction.md#w-module-jednostką-jest-docstring-a-rest-czyta-wzorzec)).

**Olski proponuje zdanie o tym samym drzewie i mniejszej liczbie czytań.**
Autor pyta olskiego, czy da się to zdanie napisać prościej,
a prościej znaczy tu: tym samym drzewem, a mniejszą liczbą odczytań.
Miara jest własna, bo liczbę odczytań olski już drukuje.
Maszyna też stoi w obu połowach: tekst w drzewo rozbiera
`olski/skład/rozbiór.py`, a drzewo w tekst wypuszcza linearyzacja.
Rankingu nad lasem cel nie żąda, i tym różni się od
[gwarancji obiegu](open-questions.md#the-round-trip-guarantee),
która żąda zdania wracającego znak w znak, więc żąda jednego drzewa z kilku.
Propozycji może być kilka i wybór zostaje przy autorze,
czyli tam, gdzie zostaje wybór między czytaniami.
Filtr w środku jest parametrem przebiegu, a nie osobnym celem:
„użyj formy przestarzałej, jeżeli słownik ją ma” odwraca odsiew,
który robi `poza_rejestrem` w `olski/rejestr.py`,
a „nie używaj tej konstrukcji” jest tym, co pomiar różnicowy robi już dziś,
zdejmując produkcje i porównując werdykty (`harness/ruch.py`).
Sprawdzianem tańszym niż każdy, jaki dziś mamy, jest podmiana synonimu:
zamień słowo na bliskoznaczne, wypisz zdanie na nowo i rozbierz je,
a drzewo ma wrócić to samo, bo zdania, w których nie wraca,
nazywają miejsce, w którym wycieka rodzaj albo walencja.
Ta połowa czeka na tezaurus, którego to repozytorium nie ma w żadnej postaci,
a że jest to pytanie do świata, zapisuje je
[open-questions.md](open-questions.md#shared-questions).
Że przeżyje znaczenie, cel nie obiecuje, bo na to testu nie ma,
i nie odwraca to decyzji, że tożsamość rzeczy jest deklaracją autora,
a nie wnioskiem ze słownika synonimów
([kategorie-zapisu.md](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)).

**Olski mówi, czego czasownik żąda od swojej pozycji, a czego zdanie tam nie podaje.**
Test podstawieniowy z reguły o czasowniku domowym ma dwa kroki,
a cel o propozycji kupuje pierwszy, mechaniczny.
Drugi krok — czy zdanie po podstawieniu zyskało —
dostaje w przeglądzie odpowiedź w rodzaju
„«stać» nie jest tu dobrym czasownikiem, bo żąda przestrzeni fizycznej,
a nic w tym zdaniu na przestrzeń fizyczną nie wskazuje”.
Mówi ją człowiek.
Cel żąda, żeby powiedział ją werdykt.
Do tego samego celu należy zdanie spakowane, czyli drugi rodzaj skrótu,
w którym autor wyrzuca to, co czytelnik ma odtworzyć.
Sygnał jest tu strukturalny i `CLAUDE.md` nazywa go wprost:
w instrukcji ma być jedno twierdzenie na zdanie,
a znakiem ostrzegawczym są dwa człony spięte przez „a”, „więc” albo „i”,
każdy z innym podmiotem.
Liczbę twierdzeń i podmiot każdego członu czyta się z drzewa,
więc ta połowa nie potrzebuje żadnego zasobu.
Żądanie pozycji werdykt już nazywa.
Czego czasownik żąda poza przypadkiem, nazywa warstwa semantyczna wydania TEI Walentego,
i nazywa to klasą rzeczy — `MIEJSCE` jest tam tą przestrzenią fizyczną —
a wydanie tekstowe, z którego powstaje leksykon, tej warstwy nie niesie
([prior-art.md](prior-art.md#polish-language-resources)).
Przekład tej warstwy stoi w `olski/żądania.txt`,
a `--żądania` mówi obok streszczenia, czego czasownik żąda od tego,
co w jego pozycji stanęło
([walencja.md](walencja.md#werdykt-nazywa-żądanie-obsadzonej-pozycji)).
Druga połowa pytania — czy słowo stojące w pozycji żądanie spełnia —
jest zamknięta dla klas osobowych, bo tam odpowiada deklaracja projektu,
a `--osoby` wypisuje pozycje, w których czasownik żąda kogoś, a stoi tam rzecz
([walencja.md](walencja.md#deklaracja-projektu-rozstrzyga-żądanie-osoby)).
Czeka więc na dwie rzeczy, i obie zostają z tamtej połowy.
Na wordnet, bo o klasach poza osobowymi — `MIEJSCE` jest jedną z nich —
nie orzeka żaden zasób, który to repozytorium ma,
i jest to pytanie do świata
([open-questions.md](open-questions.md#shared-questions)).
Oraz na samo żądanie miejsca, którego w tym przekładzie nie ma,
bo nie ma w nim pozycji okolicznikowej
([walencja.md](walencja.md#przekład-ma-pozycje-ramy-a-okolicznika-nie-ma)):
przykład z tego celu przechodzi przez nią i przez czasownik,
któremu Walenty nie daje ramy żadnej.
Czy „stać” żąda przestrzeni fizycznej, czy żąda jej tylko w tym domu,
rozstrzyga się razem z tamtym pytaniem:
metafora wystygła jest w polszczyźnie zwykłym użyciem,
a próg między nią a usterką stawia
`CLAUDE.md`.
Wiersz żądania idzie przy tym obok streszczenia, a nie w odrzuceniu:
zdanie odrzucone nie obsadza żadnej pozycji, więc mówi dalej,
dokąd analiza doszła
([subset.md](subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).

**Olski nazywa zaimek, którego tekst nie pozwala rozwiązać.**
`Są one czerwone.` ma tylu kandydatów na antecedens,
ile grup imiennych w zdaniu obok zgadza się z `one` liczbą i rodzajem
([wyżej](#podzbiór-jest-umową-a-nie-zasięgiem)).
Kilku jest zgłoszeniem wraz z ich listą, a jeden jest ciszą,
i to zgłoszenie olski wydaje: jest ono drugim z jego znalezisk
([subset.md](subset.md#zaimek-wskazujący-na-dwie-rzeczy-jest-drugim-znaleziskiem)).
Zera kandydatów nie zgłasza, choć odesłanie bez antecedensu jest usterką,
bo zdanie obok, którego gramatyka nie wyprowadza, kandydata nie podaje żadnego,
więc zero znaczy tam co innego niż w tekście przeczytanym w całości (tamże).
Ta połowa celu wraca razem z pokryciem, a nie osobnym pomysłem.
Nieosiągnięty zostaje sprawdzian, czyli garść tekstów przeczytana ręką:
nad każdym zgłoszonym zaimkiem czytelnik mówi, ilu kandydatów widzi sam,
a cel jest osiągnięty, gdy zgłoszenie pada tylko tam, gdzie nie ma ich dokładnie jednego.
Dwa wzorce z tej listy zeszły, bo zgodność nie ma nad nimi czego liczyć,
i zgłasza je warstwa obok, innym kształtem.
„To” w miejscu podmiotu akapitu zeszło, bo zdanie podjęte rzeczą nie jest
([linter.md](linter.md#wykrywacz-chwytu-zgłasza-to-bez-rzeczownika-przy-sobie)),
a orzeczenie domyślne, bo zaimkiem nie jest wcale
([tamże](linter.md#drugi-wykrywacz-zgłasza-zwrot-zastępujący-orzeczenie-członu)).
Czego zgodność nie rozstrzygnie, cel nie obiecuje:
przy dwóch kandydatach zgodnych wybiera znaczenie,
a olski melduje obu i oddaje wybór autorowi.

**Warunek na każdy cel z tej listy: zgłoszenia czyta się wszystkie.**
Autor przychodzi z prozą, której nie pisał pod tę gramatykę,
a każde zgłoszenie fałszywe kosztuje go zdanie przepisane bez powodu.
Zdanie prawdziwie wieloznaczne i zdanie, którego drugie czytanie
czytelnik odrzuca bez namysłu, dostają ten sam wiersz o odczytaniach:
`Koszt samej szynki przewyższa koszt szynki z dodatkami.`
oraz `Operator ustala priorytet.` wychodzą oba
jako `różne w rolach: dopełnienie, podmiot`.
Drugie jest zwykłym zdaniem SVO o podmiocie osobowym i rzeczowym dopełnieniu,
a czytania OVS polszczyzna naprawdę ma,
więc zdjąć go nie wolno i zostawia je
[kierunek](#kierunek-werdykt-ma-mówić-prawdę-o-tekście).
Ten warunek zdjął wieloznaczność ze znalezisk:
baza sądów nad NKJP nie potwierdziła ani jednego jej zgłoszenia
([subset.md](subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)).
Sprawdza go garść zdań przeczytana ręką,
nad korpusem audytowym ([audit-corpus.md](audit-corpus.md#the-list))
i nad NKJP ([corpora.md](corpora.md#baza-sądów-ocenia-znaleziska-a-ocenione-nie-wracają)):
nad każdym zgłoszonym zdaniem czytelnik mówi, czy poprawiłby to, co zgłoszenie wskazuje,
a warunek jest spełniony, gdy zgłoszenie pada tylko tam, gdzie poprawiłby.
Rejestr jest przypięty, a sąd czytelnika nad zdaniem raz przeczytanym
nie starzeje się, więc dopisanie produkcji każe doczytać zdania nowo zgłoszone,
a nie przeczytać rejestr od nowa.

Czego na tej liście nie ma.
Kierunku, bo prowadzi on tor, zamiast stać na jego końcu,
i ma [własną sekcję](#kierunek-werdykt-ma-mówić-prawdę-o-tekście).
Kryterium toru składu, bo jest kryterium, a zapisuje je
[jego własna sekcja](#kryterium-wyjścia-toru-składu-to-znów-readme).
Tego, po co tory są dwa, bo cele wybiera się pod tym,
i ma [własną sekcję](#po-co-tory-są-dwa).
Nie ma też sparsowanej prozy tego repozytorium,
która była pierwszym brzmieniem celu o wykrywaczu i upadła na drugiej zasadzie:
udział zdań wyprowadzonych z naszego tekstu skraca przeredagowany akapit,
a wykrywacz, który ma stać na zerze, skraca tylko poprawione zdanie.
Nie ma wreszcie jednoznaczności zdania polskiej dokumentacji technicznej,
która stała tu jako cel nad korpusem przypiętym i straciła adresata:
autor pilnujący własnej prozy nie pyta, jaki udział ustawy olski wyprowadza,
a jednoznaczność jest [znaleziskiem](#co-jest-budowane), czyli wyjściem narzędzia.
Liczbę nad rejestrem przypiętym zachowujemy jako pomiar,
i są jej właścicielami [ustawy.md](ustawy.md) oraz [corpus.md](corpus.md).

## Kolejkę ustawia korpus usterek, a nie kolejka blokerów

Co robić następne, mówi przebieg `python3 -m harness.usterki`
nad `próba/usterki.txt`, a nie liczba pokrycia.
Wpis nieczytany nazywa zdanie, którego gramatyka nie wyprowadza,
a którego autor potrzebuje przeczytanego, bo stoi w nim usterka do zgłoszenia;
produkcja, która je wpuszcza, ma pierwszeństwo przed produkcją,
która kupuje kilkadziesiąt zdań banku drzew bez ani jednej usterki.
Wpis w ciszy nazywa wykrywacz do napisania.
Szum nazywa zgłoszenie, które pada obok usterki, a nie na nią, i żąda zawężenia.
Pokrycie zostaje skutkiem, tak jak mówi
[kierunek](#kierunek-werdykt-ma-mówić-prawdę-o-tekście):
zdanie z usterką bywa długie, więc produkcja, która je wpuszcza,
wpuszcza razem z nim zdania bez usterki.

Kolejka blokerów nad bankiem drzew zostaje pomiarem i przestaje być planem.
Kolejka ta nazywa kandydatów i tyle o niej wiadomo z pomiaru.
Wiersz nazywa część mowy, na której analiza stanęła
([corpus.md](corpus.md#where-the-analyses-stop)),
więc liczy czasem kilka konstrukcji naraz,
a ile z jego obietnicy zostaje po dopisaniu, mierzy się parami wziętymi po kolei
([corpus.md](corpus.md#kolejka-obiecuje-więcej-niż-pozycja-oddaje)).
Braku, który jest kształtem zdania, a nie formą — szyku, wtrącenia,
członu bez czasownika — kolejka nie nazywa,
bo zdanie staje wtedy na cudzym wierszu albo na tym jednym,
który nie nazywa żadnej konstrukcji
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
a takich pozycji weszło do gramatyki kilka,
wśród nich cztery szyki podmiotu, dopełnienia i czasownika
([wyżej](#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).
Zostaje z niej sito.
Wiersz mówi z grubsza, ile pozycja obiecuje w tym rejestrze,
i nie mówi, że jest następna, ani wtedy, gdy stoi na czele.

Listę tego, [czego olski nie bierze](subset.md#what-it-does-not-cover-yet),
zapełniają przez to cztery źródła, a kolejka blokerów jest tylko jednym z nich.
Pierwszym jest korpus usterek, o czym wyżej.
Drugim jest przebieg nad prozą, która ten rejestr pisze:
człon bez czasownika wtrącony w środek zdania
oraz nazwa postawiona przy rzeczowniku bez spójnika
weszły na nią jako zdania odrzucone, a nie jako wiersz częstości.
Czwartym jest tor składu: wysunięty narzędnik jest na tej liście dlatego,
że legenda o bazyliszku go wypisuje, a gramatyka go nie bierze
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Wszystkie te pozycje są kształtem, a nie formą,
więc kolejka blokerów nie widzi ich w ogóle, i tym różnią się tamte źródła od niej:
pokazują pozycje, których ona nie stawia.

Kolejność dopisań ustala tekst, który ma się wyprowadzić,
a rozstrzyga o niej to, komu wolno się ruszyć.
Tekstu, który wolno przepisać bez straty, gramatyka brać nie musi:
zatrzymanie zdejmuje wtedy autor i płaci zdaniem napisanym inaczej,
a rachunki te rozdziela
[pisanie-po-olsku.md](pisanie-po-olsku.md#kto-płaci-za-odrzucone-zdanie).
Tekst, którego przepisać nie wolno, bo przepisany powiedziałby mniej,
zostawia zatrzymanie gramatyce, i dopiero to jest robota, a nie kandydat.
Tak wyszła kolejka konstrukcji legendy,
którą wypisuje tor składu (`opowieści/bazyliszek.py`),
i wyszło z niej co innego, niż wyszłoby z listy spisanej z góry
([kategorie-zapisu.md](kategorie-zapisu.md#najpierw-tekst-potem-drzewo-na-końcu-biblioteka)).

Uznaniowy zostaje wybór tekstu i jest to cena tego kryterium.
Tekst pisany pod gramatykę żądania nie postawi,
bo omija konstrukcje, których olski nie wyprowadza,
i dlatego kolejki nie ustawia już [README](#readme-jest-przyrządem-pomiarowym).
Stawia je dopiero tekst, który powstałby i bez olskiego:
korpus przypięty wydaniem albo adresem, cudza dokumentacja,
opowieść, która ma być opowieścią.

Bank drzew zostaje przy tym przyrządem weryfikacji.
Drzewa Składnicy pochodzą z wyjścia Świgry,
czyli parsera cudzej gramatyki formalnej polszczyzny,
więc pomiar nad tym bankiem nie odrzuci decyzji zgodnej z tamtą gramatyką,
a wywód o tym prowadzi
[swigra.md](swigra.md#którędy-gfjp-wchodzi-do-olskiego).
Kolejka ustawiona nad tym bankiem przenosi to skrzywienie z pomiaru na plan,
gdzie nie zostawia po sobie liczby:
konstrukcja, której Świgra nie rozebrała, nie ma w kolejce ani jednego wiersza,
więc plan z niej nie mówi o niej nic i nie mówi też, że milczy.
Skrzywienie to jest jednak w obu przebiegach naraz,
więc zgodności, która ubyła, nie podrabia:
czy dopisanie zepsuło rozbiór, który gramatyka miała przedtem,
bank drzew rozstrzyga.
Zgodności przybyłej nie potwierdza tak samo,
bo decyzję zbliżoną do tamtej gramatyki nagrodzi i w różnicy, i w poziomie,
a to jest ta jedna rzecz, o którą nad tym bankiem pytać nie wolno.

## README jest przyrządem pomiarowym

Przebieg nad [README](../README.md) zostaje, bo nic nie kosztuje:
plik jest po polsku, w rejestrze, o który olskiemu chodzi,
a ściągać nie ma czego, więc ten przebieg wykona każda sesja,
czego o banku drzew ani o ustawach powiedzieć się nie da.
[corpus.md](corpus.md#where-the-analyses-stop) jest właścicielem polecenia
i tego, co przebieg mówi dzisiaj.

**Plik jest odtąd pisany pod gramatykę i to zmienia, co przebieg mierzy.**
Zdania omijają w nim konstrukcje, których olski nie wyprowadza
([README](../README.md#konwencje), `CLAUDE.md`),
więc pokrycie nad tym plikiem mierzy pisanie tak samo jak gramatykę,
a wydruk nie mówi, które z dwojga je ruszyło.
Jest to ta sama cena, którą płacił cel nad tekstem pisanym u siebie
([wyżej](#tor-gramatyczny-nie-ma-końca)), wzięta świadomie.
Zostaje z przebiegu to, czego przeredagowanie nie podrabia:
werdykt mówi, jakie czytania olski zdaniu daje,
czyli mierzy [kierunek](#kierunek-werdykt-ma-mówić-prawdę-o-tekście), a nie udział.
O polszczyźnie, której nikt pod olskiego nie pisał,
mówią odtąd bank drzew i ustawy, i tylko one.
Liczby wzięte nad tym plikiem przed przepisaniem są w gicie,
a dzisiejsze drukuje przebieg.

**Redakcja README ma pierwszeństwo przed pomiarem, który jego prozę cytuje.**
Plik wprowadza kogoś, kto trafia tu pierwszy raz
([roles.md](roles.md#ktoś-kto-trafia-tu-pierwszy-raz)),
a zdanie skasowane albo przepisane zabiera przy okazji przykład dokumentowi,
który to zdanie cytował jako pozycję przebiegu.
Ustępuje wtedy dokument: zdanie służy w nim dalej za przykład,
traci wskazanie na tę prozę, a liczbę nad nią przelicza polecenie.
Odwrotnie nie wolno, bo README pisane pod cudzy cytat przestaje wprowadzać.

Zdaniem jest tu to, co zamyka kropka, wykrzyknik albo pytajnik.
Nagłówek, pozycja listy i wiersz tabeli
dochodzą do olskiego jako akapity, których nic nie punktuje,
i przebieg liczy je osobno,
bo policzone jako odrzucone mierzyłyby ekstrakcję zamiast podzbioru.
Ten plik nie ma ani jednej takiej pozycji,
bo nie ma w nim ani listy, ani tabeli.
Co je od zdania odróżnia i jak dużą częścią rejestru są, wycenia
[extraction.md](extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem).

Kolejki form bez licencji ten plik już nie ustawia,
bo odrzuceń została w nim garść i każde stoi na czymś pojedynczym:
na formie żartu z nazwy, na cyfrze, na przytoczonej niezgodności,
na angielskim tytule i na słowie, którym ten plik pyta poza `który`
([pisanie-po-olsku.md](pisanie-po-olsku.md#czego-brakuje-najbardziej)).

## Czego olski nie robi

Przestawiania — czyli konstytuentu nieciągłego, jak w `Jakie Jan czyta książki?` —
olski nie wpuszcza.
Jest to jedyne miejsce, w którym krzywa kosztu skacze o wykładnik,
i rozstrzygnął je pomiar, a co on pokazał, mówi
[design-notes.md](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze).
Formalizm jest przez to ceną płaconą tam, gdzie kierunek jej zażąda,
a nie pozycją, którą się planuje osobno.

Warstwy rozstrzygającej wieloznaczność za parserem olski też nie ma,
i z powodu przeciwnego niż przy przestawianiu:
tamto olski wyklucza, a to jest tym, co olski oddaje autorowi zamiast rozstrzygać.
Ile taka warstwa miałaby do rozstrzygnięcia i za ile,
wycenia [disambiguation.md](disambiguation.md),
a `olski/rozstrzyganie.py` jest jej zalążkiem, który werdyktu nie rusza
([rozstrzyganie.md](rozstrzyganie.md)).

Wykluczenie dotyczy przy tym rankingu, a nie każdej odpowiedzi takiej warstwy,
a granicę między jednym a drugim wyznacza
[hipoteza tamtego dokumentu](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza).
Frazy przyimkowej, której rzeczownik żąda swoim schematem,
nie rozstrzyga maszyna za parserem, tylko kolumna `olski/leksykon.txt`,
którą wypisuje `harness/walenty.py`
([disambiguation.md](disambiguation.md#leksykon-rozstrzyga-część-i-rozstrzyga-ją-deterministycznie)).
Odpowiedź wyczytana ze słownika jest częścią leksykonu, a nie warstwą nad nim.

Rozbioru rozmytego, czyli takiego, który zdanie z usterką wciąga i naprawia,
olski też nie ma, i tu powodem jest znów pomiar.
Naprawa jednego znaku wchodzi do werdyktu dlatego, że kandydat jest w niej jeden,
a naprawa całego słowa daje ich kilku nad jednym zdaniem
([subset.md](subset.md#naprawa-całego-słowa-nie-jest-jednoznaczna)).

## Tor składu: drzewo wchodzi, polskie zdanie wychodzi

### Kryterium wyjścia toru składu to znów README

Kryterium wyjścia jest ten sam plik, którym mierzy się tor gramatyczny,
i przemawia za nim to samo, co
[wyżej](#readme-jest-przyrządem-pomiarowym):
jest po polsku, w rejestrze, o który olskiemu chodzi,
i nikt go pod skład nie pisał.
Kryterium tu zostaje, a na tamtym torze go nie ma,
i różni te dwa tory samo żądanie.
Tam każde zdanie miało się wyprowadzić i wyprowadzić raz,
czyli o zdanie wieloznaczne w polszczyźnie potykało się kryterium;
tutaj każde ma dać się wypuścić z drzewa napisanego ręcznie,
znak w znak z tym, co w pliku stoi,
a napisu wieloznacznego nie ma, bo napis albo się zgadza, albo nie.
Przeredagowanie README kosztuje tu robotę, zamiast ją zaliczać.
Co jest tu zdaniem, rozstrzyga tamta sekcja i rozstrzyga tak samo,
więc oba tory czytają jeden tekst.

Kryterium mierzy przy tym coś węższego niż to, po co ten tor jest.
Linearyzacja wypuszcza napis, więc jest połową maszyny,
której żąda [cel o propozycji](#cele),
a README mierzy, ile polszczyzny ta połowa umie wypuścić.
Sam cel mierzy się inaczej, bo pyta o zdanie autora, a nie o zdanie z tego pliku.

Znak w znak, bo słabszego porównania nie ma czym zrobić.
Sprawdzanie wyjścia parserem oddałoby kryterium gramatyce,
a ta [temu torowi zależnością nie jest](design-notes.md#the-round-trip-invariant)
i nad zdaniem spoza podzbioru nie ma czego powiedzieć.
Zostaje tekst i tekst, a różnica między nimi jest tym, co ten tor czyta.

Drzewa są przy tym pisane w kategoriach składni,
a nie dobierane pod zdanie, które ma wyjść.
Zdanie trafione konstruktorem napisanym dla niego jednego
nie mówi o składzie nic i kryterium nie zalicza.

Kryterium ma pod sobą dwa pytania, na które odpowiada dopiero rozbieżność.
Pierwsze: gdzie skład nie trafia w zdanie README,
brakuje kategorii, którą warto dopisać, czy stoi tam wariant, który nic nie niesie?
Rozstrzygnięcie jest osądem i zapisuje je ta zmiana, przy której pada,
bo różnicy tego rodzaju nie widać z liczby.
Za samym przełącznikiem szyku dopisanym do linearyzacji nie przemawia nic:
taki parametr opisuje zdanie, a to drzewo opisuje to, o czym zdanie jest.
Drugie: przepisane zdanie README unieważnia drzewo, które je wypuszczało,
więc co tor gramatyczny płaci przy zmianie kodu, ten płaci przy zmianie prozy.
Reguły przeliczania tego rodzaju są w `CLAUDE.md`,
a ta dojdzie tam razem z pierwszym plikiem drzew pisanym pod README.
Drzewa, które już stoją, są opowieścią, a nie kopią README
([`opowieści/bazyliszek.py`](../opowieści/bazyliszek.py)),
i tekst, który mają wypuszczać, pilnuje test, a nie inny dokument,
więc reguły przeliczania tamte drzewa nie potrzebują.

**Wyjście:** każde zdanie [README](../README.md) wychodzi znak w znak
z drzewa napisanego w kategoriach `olski.skład`,
a pokazuje to polecenie, które jedno z drugim porównuje.

### Czego brakuje pod tym kryterium

Trzy braki dzielą kryterium od wyjścia i każdy ma wpis w
`todo/`, gdzie stoi razem z dowodem do przeczytania.
Porządkuje je jedna zasada: to, co zmienia drzewo,
idzie przed tym, co zmienia linearyzację.
Kategoria dopisana do składni każe przepisać każde drzewo napisane wcześniej,
a poprawka wewnątrz linearyzacji sięga wszystkich drzew, nie ruszając żadnego,
więc kolejność jest tu ceną przepisywania, a nie rankingiem ważności.

Szyku wewnątrz grupy imiennej nie niesie nic.
`Jaki` w `olski/skład/grupa.py` stawia przymiotnik przed rzeczownikiem zawsze,
choć przymiotnik po rzeczowniku nazywa, a przed nim określa.
Widać to na jednej frazie, bez żadnego pomiaru:
README pisze `kontrolowanych języków naturalnych`,
gdzie `kontrolowany` określa, a `naturalny` nazywa,
a to samo drzewo wypuszcza `kontrolowany naturalny język`.
Na poziomie zdania szyk niesie `Wyróżnienie`, więc dziura jest tu jedna, a nie dwie.

Lemat nie wskazuje formy, więc `odmień` w `olski/skład/morfologia.py`
bierze pierwszą z tych, które żądaniu odpowiadają.
Odpowiada ich kilka z trzech powodów i dwa są rozstrzygnięte:
kwalifikator odsyłający formę poza ten rejestr czyta `POZA_REJESTREM`
w `olski/rejestr.py`, a leksem, którego lemat nie wskazuje, nazywa
`olski/skład/leksemy.py`, a `WieleLeksemów` pyta o rozstrzygnięcie tam,
gdzie leksemy dają różne formy.
Wybór, który po tych dwóch zostaje, ma być zapisany, a nie brany pierwszy z brzegu
([formy-i-leksemy.md](formy-i-leksemy.md#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr)).

Leksykonu projektu nie ma, a kryterium go żąda:
README pisze `olski`, `commitów` i `Pythonem`,
a żadnego z nich nie ma jak wypuścić z drzewa.
SGJP nie zna słów, które rejestr techniczny tworzy sam,
ani leksemów, które ten rejestr dokłada do słów znanych,
więc ten brak jest pod dwoma powyższymi
([formy-i-leksemy.md](formy-i-leksemy.md#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr)).
Po stronie analizy to samo słowo już przechodzi,
bo odmianę deklaruje `olski.toml`
([warstwa-leksykalna.md](warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)),
i `Język olski jest podzbiorem polszczyzny.` jest zdaniem,
na którym oba tory spotykają ten brak.

Kolejki nie ustawia tu żaden bank drzew,
i to jest różnica między tym torem a tamtym, a nie brak pomiaru.
Bank drzew rankinguje to, na czym staje parser,
czyli konstrukcje, które w tekście ktoś napisał;
generator staje na tym, czego nie ma czym powiedzieć,
a tego nie widać w żadnym korpusie, tylko w dokumencie, który ma wyjść.
Kolejkę ustawia więc dokument i nic poza nim.
Zaimek wskazujący, liczebnik, negacja wraz z dopełniaczem negacji,
koordynacja bytów i zdarzeń, wyrażenie przyimkowe, przysłówek,
przydawka zdaniowa, okolicznik wyrażony zdarzeniem,
bezokolicznik po czasowniku oraz treść czyjegoś sądu wyszły z drzewa dlatego,
że zażądała ich [legenda o bazyliszku](../opowieści/bazyliszek.py), a nie README,
które stoi w czasie teraźniejszym i nie żąda żadnej z tych rzeczy.
Żadnej z nich nie wzięła przy tym za długość:
zdanie podrzędne dokłada się tam, gdzie ktoś ma powód coś zrobić,
spójnik tam, gdzie zdania mają przestać brzmieć jednakowo,
bezokolicznik tam, gdzie postać ma czegoś chcieć,
a treść tam, gdzie ma sądzić o świecie coś, czego świat nie potwierdza
([kategorie-zapisu.md](kategorie-zapisu.md#lepszy-tekst-żąda-czego-innego-niż-dłuższy)).

Rama czasownika jest przy tym faktem o słowie, a nie o kierunku,
w którym się go używa,
więc oba kierunki czytają `olski/leksykon.txt` przez `olski/walencja.py`:
parser robi z niego klasy walencyjne, bo z klasy powstaje produkcja,
a `Robi` w `olski/skład/składnia.py` pyta o jeden lemat, bo tyle jest w drzewie.
`V.pomagać(R.linter, A.dobry * R.kod)` zgłasza się więc zamiast wypuścić
`Linter pomaga dobry kod.`
Wspólny jest przy tym plik, a nie każde zdanie, które on mówi:
bezokolicznik czyta stąd sam skład, bo tylko jemu to zdanie coś kupuje
([walencja.md](walencja.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)).

### Czego ten tor nie obejmuje

Skład w sensie łamania tekstu — nierozdzielna spacja po wyrazie jednoliterowym,
cudzysłowy, pisownia `nie` — nie potrzebuje ani drzewa, ani gramatyki,
i jest warstwą osobną w
[design-notes.md](design-notes.md#the-separable-typographic-layer).
Miejsce tej warstwy w repozytorium jest do rozstrzygnięcia,
bo jej reguły stały po stronie sprawdzania,
w pakiecie, który wyszedł razem z silnikiem reguł.

Poza kryterium jest także warstwa nad zdaniem, czyli `olski/skład/opowieść.py`,
choć stoi i choć wypuszcza czas przeszły oraz opuszczony podmiot.
Jest tak dlatego, że kryterium liczy to, czego brakuje jednemu zdaniu,
a te dwie rzeczy są własnościami tekstu i żadne zdanie ich w sobie nie ma:
zdanie nie wie, kiedy to było, ani o kim mowa była przed chwilą.
Wywód prowadzi
[kategorie-zapisu.md](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie).
Warstwa ta jest przy tym tym samym rachunkiem,
którego [cel o zaimku](#cele) żąda po stronie analizy.

Poza kryterium jest wreszcie `olski/skład/makieta.py`, czyli tekst do makiety losowany
z drzew, bo kryterium mierzy zdanie napisane, a losowanie mierzy co innego:
pokazuje, których faktów o polszczyźnie nie ma tu żaden leksykon,
i pokazuje je dlatego, że autor drzewa wybiera je, nie zauważając, że wybrał.
Cztery takie fakty wyszły z niego wprost do `todo/`,
a wywód prowadzi
[po-wypisaniu.md](po-wypisaniu.md#tekst-losowany-żąda-tego-czego-autor-nie-musiał-napisać).

## Wycofany jest pakiet reguł

Silnik reguł, pakiet typograficzny i polecenie, które je uruchamiało,
są usunięte, a razem z nimi cała analiza, która schodziła do znaku.
Linter nie jest wycofany.
Nazywa go [lista celów](#cele) wyżej.
Decyzję i jej powody zapisuje [linter.md](linter.md#co-zamknęło-pakiet-reguł),
a cenę, przy której zapadła, [firing-rates.md](firing-rates.md).

Plan tego toru stał tutaj i git go trzyma,
bo etap, na który nikt nie czeka, nie jest planem, tylko zaległością.
Wraca za to jedna rzecz, którą ten plan ustalił i która wycofanie przeżywa:

**Reguła jest tania do wymyślenia i bez kalibracji nie wchodzi do wydruku domyślnego.**
Zdanie to stało tutaj jako pierwsza zasada tamtego toru,
w brzmieniu „bezwartościowa bez kalibracji”,
i to ono go zamknęło, kiedy pomiar wreszcie przyszedł,
bo kalibracji nie doczekała się ani jedna reguła.
Brzmienie dzisiejsze jest słabsze i jest tak celowo:
tamto żądało pomiaru przed napisaniem reguły i przez to reguły nie powstawały,
a to żąda go przed awansem do znalezisk i pozwala wykrywaczowi stać za flagą,
dopóki sądy czytelnika go nie potwierdzą albo nie zdejmą
([linter.md](linter.md#kolejna-reguła-zaczyna-się-od-zdania-z-usterką-a-kalibracja-przychodzi-przed-awansem)).
Tak samo wieloznaczność zeszła ze znalezisk na kilkudziesięciu sądach,
zamiast czekać na setki.

Tor gramatyczny czyta z tego tyle, ile mówi kształt werdyktu:
„to zdanie ma dwa czytania, oto one” jest wypowiedzią o zdaniu,
stopa wzorca na tysiąc słów nie jest,
a pierwsze nie potrzebuje kalibracji, bo niczego nie proguje.
Kształt jest jedną z [czterech osi](linter.md#cztery-osie-każdej-reguły).
Wycofanie dotyczy trzech z nich.

Życzenie, które ten tor niósł obok siebie, wycofania nie dotyczy,
bo nie było etapem i nie było linterem:
o dobrą polską prozę z modelu pyta [fiction.md](fiction.md),
a co z niej dało się mierzyć, mówi [linter.md](linter.md#and-fiction).
