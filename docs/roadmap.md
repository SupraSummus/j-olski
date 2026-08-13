# Roadmap

Uporządkowanie, a nie harmonogram.
Dat tu nie ma, bo projekt jest dla przyjemności,
a datowany plan hobby jest sposobem na to, żeby zaczęło przypominać pracę.

Każdy etap ma kryterium wyjścia,
bo „kiedy to jest skończone” jest tą częścią planowania,
która regularnie na siebie zarabia.
Tor gramatyczny jako całość kryterium wyjścia nie ma,
a co go prowadzi zamiast tego, mówi
[sekcja niżej](#tor-gramatyczny-nie-ma-końca).
Tor składu je ma i o tym mówi
[tamta sekcja](#kryterium-wyjścia-toru-składu-to-znów-readme).

Tory są dwa i każdy ma własną numerację.
Numeracja jest kolejnością zależności wewnątrz toru:
etap, który potrzebuje późniejszego, jest usterką planu,
a nie odkryciem na temat pracy.
Poprzez granicę torów taka zależność nie biegnie w żadną stronę,
więc numer z jednego z drugim się nie zestawia
i żaden nie mówi, na co drugi czeka.
Trzeci tor tu stał i został wycofany,
o czym mówi [sekcja niżej](#tor-lintera-jest-wycofany).

## Co jest budowane

Tor gramatyczny:
parser zaprojektowanego podzbioru polszczyzny,
który wieloznaczność oddaje autorowi, zamiast rozstrzygać ją za niego.
Zdanie jest olski wtedy, gdy ma dokładnie jedno czytanie,
więc werdykt takiego parsera jest wypowiedzią o zdaniu:
mówi, że się nie wyprowadza, albo że wyprowadza się na dwa sposoby, i na jakie.
[subset.md](subset.md#validity-is-uniqueness-not-just-derivability)
trzyma decyzję, która czyni tę własność olskiego własnością,
a [swigra.md](swigra.md#what-it-leaves-open) miejsce, w którym przegląd zastał puste pole:
najbliższy istniejący parser polszczyzny rozstrzyga tam, gdzie olski by zgłaszał.
Maszyneria jest tym wszystkim, co [design-notes.md](design-notes.md)
mówi o Earleyu, lesie rozbiorów, swobodnym szyku i LCFRS.

Za budowaniem tego przemawia kształt takiego werdyktu.
Mówi on o zdaniu, które wskazuje.
Reguła mierząca stopę wzorca na tysiąc słów tego nie mówi:
jest raportem o dokumencie, a nie zarzutem wobec zdania
([generated-polish.md](generated-polish.md#the-closing-sentence-is-measurably-different)),
a wystąpienie, w które trafia, wskazuje po to,
żeby dało się sprawdzić liczbę, i nie twierdzi o nim nic.
Ten argument stał tu, zanim tor lintera został wycofany,
i to on go wycofał.

Tor składu idzie w drugą stronę:
wchodzi drzewo tego, co ma zostać powiedziane, a wychodzi polskie zdanie.
Kategorie tego drzewa są kategoriami dziedziny, a nie polszczyzny,
i to jest decyzja, która czyni ten tor tym, czym jest,
bo rozbioru zdania pisanego z góry nikt nie chce pisać
([sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)).
Zgodność jest tu liczona, a nie sprawdzana,
więc trudność, dla której olski istnieje, przy tym kierunku nie powstaje,
a gramatyka podzbioru nie jest temu torowi potrzebna do niczego:
parser stoi w nim jako świadek, a nie jako zależność
([design-notes.md](design-notes.md#the-round-trip-invariant)).

Linter stylu dla polskiej dokumentacji technicznej stał obok, na torze opcjonalnym,
i jest wycofany razem z całą analizą, która schodziła do znaku,
o czym [niżej](#tor-lintera-jest-wycofany).
Dwa odwrócenia prowadzą do tego stanu i żadne nie ma wracać przez przeoczenie:
linter stał tu najpierw jako cel, a gramatyka jako tor obok niego,
potem odwrotnie, a teraz nie stoi wcale.

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
o którym [etap 1](#etap-1-przyłączanie-wyrażeń-przyimkowych) rozstrzygnął,
że olski go nie wybiera.
Rozstrzyga o tym znaczenie, więc żadna produkcja tego nie zdejmie.
Kryterium nieosiągalne jest kryterium innego rodzaju, niż było opisane,
a to, że z trzech wyjść wybrano właśnie to, zapisuje
[open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma).

Zbiór zdań, którym się mierzyło, był przy tym w rękach tego, kto mierzy.
Każdy inny korpus tego repozytorium jest przypięty —
wydaniem, commitem albo adresem ELI — a README rusza każdy commit,
który dotyka jego prozy, i nie dogoni tego żadna reguła przeliczania
([CLAUDE.md](../CLAUDE.md#checks)).
Odległość do takiego celu skraca i dopisana produkcja, i przeredagowany akapit,
a wydruk nie mówi, które z dwojga zaszło.
Zdanie „README stoi, a rusza się gramatyka” było więc obietnicą,
a nie własnością pomiaru.

## Kierunek: werdykt ma mówić o zdaniu prawdę

Zostaje kierunek: czytania, które olski melduje,
mają być dokładnie tymi, które polszczyzna nad zdaniem ma.
Pokrycie jest skutkiem takiego kierunku i mierzy się je osobno.

Kierunek nie mówi, kiedy przestać, więc porządek robi cena kroku.
Każde dopisanie wycenia się przed wpuszczeniem w dwóch walutach,
czyli ile zdań przyjmuje i ile jednoznaczności zabiera,
a pytać o to trzeba każdy z trzech rejestrów, bo odpowiadają różnie:
bank drzew ([corpus.md](corpus.md#where-the-analyses-stop)),
prozę tego repozytorium
i ustawy ([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)).
Wycenionym przykładem jest czas przeszły z
[etapu 6](#etap-6-reszta-konstrukcji).

Kolejność etapów robi koszt przepisywania.
To, co każda późniejsza produkcja ma realizować, wchodzi przed nią,
bo dopisane potem każe przepisać je wszystkie:
tak stoją [etap 1](#etap-1-przyłączanie-wyrażeń-przyimkowych)
i [etap 2](#etap-2-walencja),
i tak samo czytanie, którego polszczyzna nie ma,
zdejmuje się przed konstrukcjami, w których by wróciło.
Formalizm miejsca w tej kolejności nie ma,
bo kierunek mówi, co ma zajść nad zdaniem, a nie czym ma być wyprowadzone
([design-notes.md](design-notes.md#formalizm-jest-środkiem-a-nie-celem)).

## README jest przyrządem pomiarowym

Przebieg nad [README](../README.md) zostaje, bo mierzy dobrze i nic nie kosztuje.
Plik stoi po polsku, w rejestrze, o który olskiemu chodzi,
nikt go pod gramatykę nie pisał,
a ściągać nie ma czego, więc ten przebieg wykona każda sesja,
czego o banku drzew ani o ustawach powiedzieć się nie da.
[corpus.md](corpus.md#where-the-analyses-stop) trzyma polecenie
i kolejność, w jakiej README ustawia to, czego gramatyce brakuje.

Zdaniem jest tu to, co zamyka kropka, wykrzyknik albo pytajnik.
Nagłówek, pozycja listy i wiersz tabeli
dochodzą do olskiego jako akapity, których nic nie punktuje,
i przebieg liczy je osobno,
bo policzone jako odrzucone mierzyłyby ekstrakcję zamiast podzbioru.
Co je od zdania odróżnia i jak dużą częścią rejestru są, trzyma
[extraction.md](extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem).

Przeredagowanie tego pliku rusza teraz same liczby,
a zakaz przepisywania tych dokumentów pod gramatykę zostaje
przy swoim własnym powodzie: proza jest tu materiałem
([CLAUDE.md](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).

## Etap 0: gramatyka, która stoi

Gramatyka podzbioru nad Morfeuszem 2,
w której poprawność zdania znaczy dokładnie jedno czytanie,
polecenie wydające werdykt zdanie po zdaniu,
i pomiar tego wszystkiego na banku drzew.

**Wyjście:** zdanie dostaje werdykt wraz z rolami,
które w każdym jego czytaniu coś wypełnia,
a pokrycie i zgodność z ręcznymi rozbiorami są zmierzone na korpusie,
który da się ściągnąć.
Zaliczone, zob. [subset.md](subset.md) i [corpus.md](corpus.md).

## Etap 1: przyłączanie wyrażeń przyimkowych

`Program zapisuje ustawienia w pliku.` ma dwa czytania i oba są polszczyzną,
więc własność jednoznaczności to zdanie odrzuca.
Konstrukcja nie jest przy tym rzadka:
[subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
trzyma trzy wyjścia z tego i mówi, że własność w tym brzmieniu
wyklucza dużą i zwyczajną część technicznej polszczyzny.
Rejestr, o który olskiemu chodzi, jest taką polszczyzną,
więc jedno z trzech trzeba wybrać.

Etap stoi pierwszy, bo te trzy wyjścia
nie żądają tego samego od produkcji pisanych później.
Drugie z nich — przyłączaj do czasownika, chyba że coś wymusza inaczej —
jest regułą, którą każda nowa produkcja z wyrażeniem przyimkowym ma realizować,
a trzecie zmienia to, co w ogóle liczy się jako dwa czytania.
Rozstrzygnięcie po napisaniu tamtych produkcji jest więc przepisaniem ich wszystkich.

**Wyjście:** jedno z trzech wyjść wybrane,
z uzasadnieniem wziętym z prawdziwej polszczyzny, a nie z gustu,
i gramatyka, o której da się powiedzieć, że je realizuje.
Zaliczone: wybrane jest pierwsze, czyli olski nie wybiera przyłączenia,
a wzięło się to z tego, że bank drzew żadnego przyłączenia nie ma za domyślne,
zob. [subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).

Ten etap płaci też za oczekiwanie, które trzeba znieść z niego na następne.
Wyjście, które od gramatyki nie żąda niczego, wyglądało tu na jedno z trzech,
a nie było nim żadne:
odrzucenie jest uczciwe dopiero wtedy, gdy oba czytania mają gdzie się wyprowadzić,
więc razem z decyzją weszły do gramatyki wszystkie pozycje okolicznika,
których brak był wyborem robionym po cichu.
Ile to kosztowało przyjętych zdań, trzyma
[corpus.md](corpus.md#the-measurement).

## Etap 2: walencja

Czego czasownik wymaga, nie mówi produkcja, i mówić to musi leksykon.
Bez niego `być` przyjmuje dopełnienie w bierniku,
a `On jest wolny.` wychodzi wieloznaczne
między orzecznikiem, który czytelnik ma,
a dopełnieniem, którego nikt nie ma na myśli.
[subset.md](subset.md#what-it-does-not-cover-yet) nazywa to żądaniem,
które stawia każda konstrukcja, a nie konstrukcją obok innych,
a [corpus.md](corpus.md#what-morphological-ambiguity-costs)
dochodzi do tej samej dziury od strony banku drzew.

Etap stoi przed konstrukcjami z tego samego powodu co poprzedni,
i powód ten jest tu arytmetyczny.
Wieloznaczność, którą wnosi brak walencji,
nie jest jedna na gramatykę, tylko jedna na czasownik
razy konstrukcje, w których ten czasownik stoi,
więc leksykon dopisany po nich sprawdza się naraz wobec wszystkich.

**Wyjście:** dopełnienia czasownika biorą się z leksykonu, a nie z produkcji,
i `On jest wolny.` traci czytanie z dopełnieniem.
Jednego czytania sama walencja temu zdaniu nie daje:
zostaje przy nim para, na którą składa się rzeczownikowe czytanie przymiotnika
wraz z nazwiskowym czytaniem, jakie Morfeusz daje formie `On`,
a jedno i drugie należy do słownika i do etapu niżej.
Zaliczone: rama czasownika jest cechą braną z leksykonu,
który ma ramę domyślną i wpis na każdy lemat węższy od niej,
zob. [subset.md](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej).

Leksykon urósł po tym etapie i urósł jednym zdaniem na lemat:
że czasownik nie bierze dopełnienia w bierniku, wzięte z Walentego.
Etap kupował mechanizm, a nie leksykon, i to widać po tym, czym urośnięcie było:
zmianą danych i jednego wymiaru klucza, a nie zmianą ani jednej produkcji.

## Etap 3: czytania, których polszczyzna nie ma

Morfeusz daje formie czytania, których czytelnik nie ma,
a każde takie czytanie jest dla olskiego drugim czytaniem całego zdania.
`admissible` w `olski/subset.py` wyklucza dziś jedną ich klasę,
czytanie nieodmienne stojące obok wyrazu funkcyjnego,
i [subset.md](subset.md#the-dictionary-offers-readings-polish-does-not)
mówi, czemu akurat te dwa warunki naraz.
README rozpada się na jednej klasie, której to kryterium nie obejmuje:
na rzeczownikowym czytaniu formy, którą Morfeusz zna też jako przymiotnik.
Stoi na niej `Linter pomaga pisać dobry kod.`,
a to, co z niej zostaje otwarte, trzyma [TODO.md](../TODO.md).

Połowa tej klasy jest zamknięta i zamknęła się nie tam, gdzie ten etap patrzy.
Formy paradygmatu `ten` niosły to czytanie licznie,
a zdejmuje je nie wykluczenie w słowniku, tylko warunek w produkcji:
zaimek rzeczowny nie rządzi dopełniaczem
([subset.md](subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)).
Czytanie, którego polszczyzna nie ma, wolno więc odebrać dwiema drogami,
i tańsza bywa ta, która pyta nie o to, co słownik oferuje,
ale o to, co produkcja licencjonuje.

Nazwiskowe czytanie rzeczownika, który zaczyna zdanie, z tej listy zeszło.
Para lematów jednej formy nie jest dwoma czytaniami
([subset.md](subset.md#co-się-liczy-jako-jedno-czytanie)),
więc jednoznaczności ta klasa nie kosztuje,
a kryterium na pozycję nie kupuje ani jednego zdania i kosztuje zdania Składnicy.

Etap stoi między tamtymi a konstrukcjami,
bo wieloznaczność zawęża, a pokrycia nie podnosi,
i jest pierwszym, przy którym nie wiadomo, czy kryterium w ogóle istnieje.
Wykluczenie zbyt szerokie zabiera zwyczajne polskie słowa,
co tamten dokument pokazuje na `jury` i `menu`,
więc odpowiedzią bywa tu decyzja, że klasy się nie da wykluczyć.
Oba kryteria, jakie na te klasy zaproponowano, są taką odpowiedzią,
a cenę każdego trzyma
[subset.md](subset.md#dwa-szersze-kryteria-zmierzono-i-żadne-nie-stoi).

**Wyjście:** klasa rozstrzygnięta kryterium
albo zapisaną decyzją, że kryterium nie ma,
a kryterium przyjęte zmierzone na Składnicy tym, ile zdań zabiera.

## Etap 4: zdanie złożone

Podrzędność z `że` i `który`, obok koordynacji przecinkiem, która już stoi.
Koordynacja weszła osobno, bo osobno się ją zmierzyło:
nie odbiera nad Składnicą ani jednego zdania już przyjętego
i dokłada dwadzieścia dwa nowe,
co wraz z tabelą i poleceniem trzyma
[subset.md](subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania).
Nad README przyjęła dwa zdania, oba na poziomie zdaniowym,
a reszta zdań z przecinkiem niesie w tym pliku także zdanie podrzędne.
Podrzędność jest więc tym, na czym ten etap stoi,
i wobec tego rejestru pozycją nie do ominięcia:
uzasadnienie wymaga zdania podrzędnego,
a proza tego repozytorium składa się z uzasadnień.

Kupuje ona ponadto coś, czego pokrycie nie mierzy,
i to jest ta połowa etapu, którą stoi zaliczyć osobno.
Zdanie podrzędne z `które` nie było odrzucane, tylko czytane jako współrzędne,
bo przecinek koordynuje zdania, a podrzędności nie było,
i wychodziło z tego jedno czytanie, które mówi co innego niż zdanie.
Zdejmuje je warunek na lemat, a nie produkcja:
zaimek względny nie jest przymiotnikiem przy rzeczowniku,
więc `które zadania własne gminy` przestaje być grupą imienną
i nie ma czym być podmiotem zdania po przecinku
([subset.md](subset.md#zaimek-względny-nie-jest-przymiotnikiem-przy-rzeczowniku)).
Nad rejestrem ustaw to jedno zdanie policzone jako przyjęte przestaje nim być
([ustawy.md](ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa)),
więc etap zdjął werdykt błędny, zanim dołożył nowe.

**Wyjście:** zdanie łączące dwa zdania składowe spójnikiem podrzędnym
wyprowadza się i wyprowadza raz,
pokrycie nad README idzie w górę o te zdania, które na tym stały,
a zdanie z `które` przestaje wychodzić czytaniem współrzędnym.

Zaliczone jest pierwsze i trzecie, a drugie nie, i drugie jest tu wynikiem.
Zdanie dopełnieniowe z `że` i zdanie względne z `który` wyprowadzają się
i pod złotą morfologią nie odbierają Składnicy ani jednego zdania przyjętego,
a zdanie z `które` wychodzi odrzucone zamiast współrzędnego;
tabelę i cenę trzyma
[subset.md](subset.md#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja).
Pokrycie nad README nie ruszyło się o ani jedno zdanie
i mówi to o pomiarze nad tym plikiem więcej niż o podrzędności:
zdania tego pliku, które na podrzędności stały, stoją także na przysłówku,
na dwukropku i na liczebniku,
czego [tamten przebieg](corpus.md#where-the-analyses-stop) nie przewidział inaczej,
niż mówiąc, że większość zdań odrzuconych niesie dwie klasy albo więcej.

Etap zostaje więc otwarty, a brakuje mu dwóch rzeczy i dzieli je to,
co każda żąda od gramatyki.
Interpunkcja zdaniowa łączy zdania, które już się wyprowadzają:
dwukropek otwierający zdanie
oraz przecinek przed spójnikiem, czyli `Plany są niczym, ale planowanie jest wszystkim.`
Stoi ona na czele kolejki nad prozą tego repozytorium
([corpus.md](corpus.md#where-the-analyses-stop)).
Reszta podrzędności żąda nowych kształtów: pytanie zależne,
spójniki podrzędne poza `że`
i zaimek wysunięty razem z grupą, w której stoi,
bo każdy kolejny kształt takiej grupy jest osobnym ciałem produkcji
([subset.md](subset.md#what-it-does-not-cover-yet)).
Co z tego dwojga jest tańsze, powie dopiero pierwsze policzone dopisanie.

## Etap 5: słowa, których słownik nie ma

Morfeusz zwraca `ign` na formę, której nie zna,
a formy `ign` nie bierze żadna produkcja.
Notację tego rejestru — `docs/subset.md`, `harness/markdown.py` —
olski wpuszcza jako rzeczownik nieodmienny,
bo rzeczownikiem nieodmiennym taka forma w polszczyźnie jest.
Zostaje polskie słowo odmienione, którego słownik nie zna:
`olski`, `commitów`, `Pythonem`.
Dla niego to samo czytanie byłoby nie tylko nieznane, ale fałszywe,
i dlatego [subset.md](subset.md#what-it-does-not-cover-yet)
trzyma tę klasę osobno od tamtej.
`Język olski jest podzbiorem polszczyzny.` się nie wyprowadza,
więc język nie umie powiedzieć sam w sobie, czym jest.

Etap nie zależy od czterech powyżej ani one od niego,
a numeracja żąda tylko tego, żeby żaden nie potrzebował późniejszego.
Stoi tutaj, bo rejestr, o który chodzi, jest takich słów pełen,
a bank drzew tej klasy nie pokazuje w ogóle:
tam każdy token ma rozbiór wybrany przez człowieka,
więc kolejki z niego ta klasa nie ustawia
i widać ją dopiero w przebiegu nad dokumentacją.

**Wyjście:** `Język olski jest podzbiorem polszczyzny.`
wyprowadza się i wyprowadza raz.

## Etap 6: reszta konstrukcji

Przysłówek, `to` w roli łącznika,
negacja wraz z dopełniaczem negacji,
liczebniki i rzeczowniki odczasownikowe.
Kolejka ze Składnicy stawia je wysoko,
bo przysłówek prowadzi w niej trzeci wiersz, a `to` dwa dalsze.
Wobec README podnoszą pokrycie dopiero razem,
a żaden z czterech zmierzonych dodany sam go nie rusza.
[corpus.md](corpus.md#where-the-analyses-stop) mierzy to nad czterema z nich,
a nad łącznikiem i negacją nie mierzy nic,
więc tyle samo zostaje tam do dopisania, co tutaj do zbudowania.

Na koniec wychodzą dlatego, że żadna z nich nie żąda niczego
od produkcji pisanych po niej,
więc [koszt przepisywania](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)
ich nie porządkuje i między sobą rozstrzyga je sama cena kroku.
Dwie kolejki, które ją wyceniają, nie zgadzają się co do kolejności,
i jest to wynik pomiaru, a nie usterka w którejś z nich.

Czas przeszły był na tej liście i z niej zszedł,
a to, jak zszedł, mówi o samej liście dwie rzeczy.
Kolejka ze Składnicy stawiała go na pierwszym miejscu
i nazywała najtańszym dużym zyskiem;
zysk wyszedł na piątą część tego, co ranking obiecywał,
a cena wypadła poza ranking, bo rodzaj wszedł do każdego szyku zdania
([subset.md](subset.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku)).
Nad README nie kupił ani jednego zdania,
bo kupił jedno i jedno stracił,
a nad rejestrem ustaw nie kupił nic i pięć zdań uczynił wieloznacznymi
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)).
Reszta tej listy pochodzi z tego samego rankingu,
więc mierzone ma być każde dopisanie z osobna, a nie sama lista na końcu.

**Wyjście:** lista w [subset.md](subset.md#what-it-does-not-cover-yet) jest pusta,
bo etap jest ostatnim, który ma z niej co brać,
a tabele w [corpus.md](corpus.md) są przeliczone tym, co ją opróżniło.

## Czego ta numeracja nie obejmuje

Czy olski może przestawiać — czyli czy wpuszcza konstytuenty nieciągłe,
jak `Jakie Jan czyta książki?` —
jest jedynym miejscem, w którym krzywa kosztu skacze o wykładnik,
bo odpowiedź na tak wyprowadza cały podzbiór poza gramatyki bezkontekstowe.
Pytanie trzyma
[open-questions.md](open-questions.md#the-big-fork-may-olski-scramble),
razem z tym, że rozstrzyga je pomiar, a nie gust.

Etapem to nie jest, bo [kierunek](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę) mówi,
co ma zajść nad zdaniem, a nie czym ma być wyprowadzone.
Formalizm zostaje więc ceną płaconą tam, gdzie któryś etap jej zażąda,
a nie pozycją, którą się planuje osobno.

## Tor składu: drzewo wchodzi, polskie zdanie wychodzi

### Kryterium wyjścia toru składu to znów README

Kryterium wyjścia jest ten sam plik, którym mierzy się tor gramatyczny,
i przemawia za nim to samo, co
[wyżej](#readme-jest-przyrządem-pomiarowym):
stoi po polsku, w rejestrze, o który olskiemu chodzi,
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
Rozstrzygnięcie jest osądem i zapisuje je etap, przy którym pada,
bo różnicy tego rodzaju nie widać z liczby.
Za samym przełącznikiem szyku dopisanym do linearyzacji nie przemawia nic:
taki parametr opisuje zdanie, a to drzewo opisuje to, o czym zdanie jest.
Drugie: przepisane zdanie README unieważnia drzewo, które je wypuszczało,
więc co tor gramatyczny płaci przy zmianie kodu, ten płaci przy zmianie prozy.
Reguły przeliczania tego rodzaju trzyma [CLAUDE.md](../CLAUDE.md#checks),
a ta dojdzie tam razem z pierwszym plikiem drzew pisanym pod README.
Drzewa, które już stoją, są opowieścią, a nie kopią README
([`opowieści/bazyliszek.py`](../opowieści/bazyliszek.py)),
i tekst, który mają wypuszczać, trzyma test, a nie inny dokument,
więc reguły przeliczania tamte drzewa nie potrzebują.

Etapy niżej porządkuje jedna zasada:
to, co zmienia drzewo, idzie przed tym, co zmienia linearyzację.
Kategoria dopisana do składni każe przepisać każde drzewo napisane wcześniej,
a poprawka wewnątrz linearyzacji sięga wszystkich drzew, nie ruszając żadnego,
więc kolejność jest tu ceną przepisywania, a nie rankingiem ważności.

**Wyjście:** każde zdanie [README](../README.md) wychodzi znak w znak
z drzewa napisanego w kategoriach `skład.składnia`,
a pokazuje to polecenie, które jedno z drugim porównuje.

### Etap 0: skład, który stoi

Drzewo kategorii dziedziny, linearyzacja licząca zgodność
i morfologia wzięta z Morfeusza czytanego w drugą stronę.

**Wyjście:** drzewo złożone z konstruktorów wypuszcza polskie zdanie,
a forma, której słownik nie ma, zgłasza się wyjątkiem, zamiast zostać zgadnięta.
Zaliczone, zob. `skład/` oraz [sklad.md](sklad.md).

### Etap 1: temat i remat

Polszczyzna niesie szykiem to, co stoi na czele,
i niesie to na dwóch poziomach naraz, z których ten zapis ma jeden.

Na poziomie zdania niesie to `Wyróżnienie`:
`Wejściem jest zwykły tekst polski.` i `Zwykły tekst polski jest wejściem.`
wychodzą z dwóch różnych drzew, a szyku nie zaszywa ani `Jest`, ani `Robi`.
Czasownik przy tym nie rusza się nigdy, więc przestawia się to, co stoi wokół niego,
i tyle wystarcza na oba szyki orzeczenia imiennego oraz na zdanie prezentujące,
czyli takie, które nową rzecz odsyła na koniec.

Wewnątrz grupy imiennej nie niesie tego nic:
`Jaki` w `skład/składnia.py` stawia przymiotnik przed rzeczownikiem zawsze,
choć przymiotnik po rzeczowniku nazywa, a przed nim określa.
Widać to na jednej frazie, bez żadnego pomiaru:
README pisze `kontrolowanych języków naturalnych`,
gdzie `kontrolowany` określa, a `naturalny` nazywa,
a to samo drzewo wypuszcza `kontrolowany naturalny język`.
Ruch wraz z tym, co do niego przeczytać, trzyma [TODO.md](../TODO.md).

Etap stoi pierwszy, bo każdy etap dokładający nowy szyk zdania
będzie tę kategorię realizował,
a drzewa napisane bez niej trzeba by przepisać razem z konstruktorami.

**Wyjście:** `kontrolowany język naturalny` i `kontrolowany naturalny język`
biorą się z dwóch różnych drzew,
tak jak biorą się z nich oba szyki orzeczenia imiennego.

### Etap 2: walencja czytana raz

Rama czasownika jest faktem o słowie, a nie o kierunku, w którym się go używa,
więc oba kierunki czytają `olski/leksykon.txt` przez `olski/walencja.py`:
parser robi z niego klasy walencyjne, bo z klasy powstaje produkcja,
a `Robi` w `skład/składnia.py` pyta o jeden lemat, bo tyle stoi w drzewie.
`V.pomagać(R.linter, A.dobry * R.kod)` zgłasza się więc zamiast wypuścić
`Linter pomaga dobry kod.`
Wspólny jest przy tym plik, a nie każde zdanie, które on mówi:
bezokolicznik czyta stąd sam skład, bo tylko jemu to zdanie coś kupuje
([subset.md](subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)).

Etap stoi przed konstrukcjami z tego samego powodu,
co [etap 2 toru gramatycznego](#etap-2-walencja):
każda konstrukcja z nową rolą zaszywałaby przypadek osobno,
a leksykon dopisany przed nimi sprawdza się naraz wobec wszystkich.

**Wyjście:** rama czasownika przychodzi z leksykonu,
a drzewo żądające dopełnienia od czasownika, który go nie bierze,
zgłasza się zamiast wypuścić zdanie, którego polszczyzna nie ma.
Zaliczone, zob. `olski/walencja.py` oraz `PozaRamą` w `skład/składnia.py`.

### Etap 3: lemat nie wskazuje formy

`odmień` w `skład/morfologia.py` bierze pierwszą z form, które żądaniu odpowiadają,
a odpowiada ich kilka z trzech różnych powodów, i tylko trzeci jest wyborem.

Pierwszym jest kwalifikator, którym słownik odsyła formę poza ten rejestr,
do dawnej polszczyzny albo do potocznej.
Kryterium na tę klasę stoi w danych i czyta je `POZA_REJESTREM` w tym samym pliku,
wraz z podziałem, którego ta klasa żąda:
nazwa dziedziny formy poza rejestr nie odsyła, więc `oczy` zostają, a `któren` nie.
Drugim jest leksem, którego lemat nie wskazuje,
bo jednym napisem odmieniają się dwie rzeczy o różnej odmianie.
Kryterium na tę klasę nie stoi w danych, bo rozstrzyga o nim autor,
więc stoi w `skład/leksemy.py`, czyli w nazwach wybranych nad identyfikatorami,
a `odmień` pyta o rozstrzygnięcie tam, gdzie leksemy dają różne formy.
Trzecim jest wybór, który po tamtych dwóch zostaje,
i dopiero on wymaga rozstrzygnięcia, czym ma być.
Klasy te wraz z poleceniem, które je pokazuje obok siebie, trzyma
[sklad.md](sklad.md#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr),
a ruch trzyma [TODO.md](../TODO.md);
kryterium po stronie analizy stoi tam, gdzie
[`admissible`](subset.md#the-dictionary-offers-readings-polish-does-not).

**Wyjście:** forma z kwalifikatorem, którego ten rejestr nie bierze, nie wychodzi,
leksem jest tym, co drzewo nazywa,
a wybór między formami, które oba kryteria zostawią, jest zapisany,
a nie brany pierwszy z brzegu.
Pierwsze dwa z tych trzech stoją, zob. `POZA_REJESTREM` oraz `WieleLeksemów`
w `skład/morfologia.py`, wraz z
[kwalifikatorem](sklad.md#kwalifikator-mówi-o-formie-dwie-rzeczy-i-tylko-jedna-jest-rejestrem)
oraz [nazwą leksemu](sklad.md#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje);
kolejność wzięła się z tekstu, a nie z tego etapu, i mówi o tym
[sklad.md](sklad.md#lepszy-tekst-żąda-czego-innego-niż-dłuższy).

### Etap 4: leksykon projektu

SGJP nie zna słów, które rejestr techniczny tworzy sam,
ani leksemów, które ten rejestr dokłada do słów znanych,
więc leksykon projektu jest tym, czego brakuje pod każdym etapem wyżej.
Czym taki plik ma być, co wpis ma nazywać
i dlaczego nie jest to słownik dołożony Morfeuszowi, trzyma
[sklad.md](sklad.md#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr).

Etapu tego nie dokłada się do kryterium, tylko kryterium go żąda:
README pisze `olski`, `commitów` i `Pythonem`,
a żadnego z nich nie ma jak wypuścić z drzewa.

**Wyjście:** `Język olski jest podzbiorem polszczyzny.` wychodzi z drzewa,
czyli to samo zdanie, na którym tor gramatyczny ma
[etap 5](#etap-5-słowa-których-słownik-nie-ma),
a każdy wpis leksykonu projektu niesie to, skąd się w nim wziął.

### Etap 5: konstrukcje, których żąda README

Zaimek wskazujący i liczebnik.
Negacja wraz z dopełniaczem negacji, koordynacja bytów i zdarzeń,
wyrażenie przyimkowe, przysłówek, przydawka zdaniowa,
okolicznik wyrażony zdarzeniem, bezokolicznik po czasowniku
oraz treść czyjegoś sądu stoją już w `skład/składnia.py`.

Kolejki nie ustawia tu żaden bank drzew,
i to jest różnica między tym torem a tamtym, a nie brak pomiaru.
Bank drzew rankinguje to, na czym staje parser,
czyli konstrukcje, które w tekście ktoś napisał;
generator staje na tym, czego nie ma czym powiedzieć,
a tego nie widać w żadnym korpusie, tylko w dokumencie, który ma wyjść.
Kolejkę ustawia więc dokument i nic poza nim,
a którym dokumentem jest, rozstrzyga to, co ten dokument mówi.
Pozycje odjęte wyżej wzięła
[legenda o bazyliszku](../opowieści/bazyliszek.py), a nie README,
bo opowieść żąda przeczenia, okoliczników miejsca, wskazania rzeczy zdarzeniem
oraz zdania złożonego w każdej z czterech pozostałych postaci,
a README, stojące w czasie teraźniejszym, nie żąda żadnej z tych rzeczy.
Żadnej z nich nie wzięła przy tym za długość:
zdanie podrzędne dokłada się tam, gdzie ktoś ma powód coś zrobić,
spójnik tam, gdzie zdania mają przestać brzmieć jednakowo,
bezokolicznik tam, gdzie postać ma czegoś chcieć,
a treść tam, gdzie ma sądzić o świecie coś, czego świat nie potwierdza
([sklad.md](sklad.md#lepszy-tekst-żąda-czego-innego-niż-dłuższy)).
Kryterium wyjścia toru zostaje przy README z powodu, który trzyma
[sklad.md](sklad.md#najpierw-tekst-potem-drzewo-na-końcu-biblioteka).

**Wyjście:** każda konstrukcja z tej listy wychodzi z drzewa,
a to, czego po nich brakuje, mówi już różnica między składem a README,
a nie lista spisana z góry.

### Czego numeracja tego toru nie obejmuje

Skład w sensie łamania tekstu — nierozdzielna spacja po wyrazie jednoliterowym,
cudzysłowy, pisownia `nie` — nie potrzebuje ani drzewa, ani gramatyki,
i stoi jako warstwa osobna w
[design-notes.md](design-notes.md#the-separable-typographic-layer).
Etapem nie jest, bo nic w tym torze na niego nie czeka,
a jego miejsce w repozytorium jest do rozstrzygnięcia,
bo reguły tej warstwy stały po stronie sprawdzania,
w pakiecie, który wyszedł razem z torem lintera.

Etapem nie jest także warstwa nad zdaniem, czyli `skład/opowieść.py`,
choć stoi i choć wypuszcza czas przeszły oraz opuszczony podmiot.
Jest tak dlatego, że numeracja tego toru liczy to, czego brakuje jednemu zdaniu,
a te dwie rzeczy są własnościami tekstu i żadne zdanie ich w sobie nie ma:
zdanie nie wie, kiedy to było, ani o kim mowa była przed chwilą.
Wywód trzyma
[sklad.md](sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie).

Etapem nie jest wreszcie `skład/makieta.py`, czyli tekst do makiety losowany z drzew,
bo kryterium tego toru mierzy zdanie napisane, a losowanie mierzy co innego:
pokazuje, których faktów o polszczyźnie nie ma tu żaden leksykon,
i pokazuje je dlatego, że autor drzewa wybiera je, nie zauważając, że wybrał.
Cztery takie fakty wyszły z niego wprost do [`TODO.md`](../TODO.md),
a wywód trzyma
[sklad.md](sklad.md#tekst-losowany-żąda-tego-czego-autor-nie-musiał-napisać).

## Tor lintera jest wycofany

Silnik reguł, pakiet typograficzny i polecenie, które je uruchamiało,
są usunięte, a razem z nimi cała analiza, która schodziła do znaku.
Decyzję i jej powody trzyma [linter.md](linter.md#what-closed-the-track),
a cenę, przy której zapadła, [firing-rates.md](firing-rates.md).

Plan tego toru stał tutaj i szedł przez sześć etapów,
od silnika reguł przez harness kalibracyjny aż po analizę głębszą niż wzorzec.
Nie ma go tu już w żadnym kształcie i git go trzyma,
bo etap, na który nikt nie czeka, nie jest planem, tylko zaległością.
Wraca za to jedna rzecz, którą ten plan ustalił i która wycofanie przeżywa:

**Reguła jest tania do wymyślenia i bezwartościowa bez kalibracji.**
Pomiar buduje się przed zestawem reguł, a nie po nim.
Zdanie to stało tutaj jako pierwsza zasada tamtego toru
i to ono go zamknęło, kiedy pomiar wreszcie przyszedł,
bo kalibracji nie doczekała się ani jedna reguła.

Tor gramatyczny czyta z tego tyle, ile mówi kształt werdyktu:
„to zdanie ma dwa czytania, oto one” jest wypowiedzią o zdaniu,
stopa wzorca na tysiąc słów nie jest,
a pierwsze nie potrzebuje kalibracji, bo niczego nie proguje.

Życzenie, które ten tor niósł obok siebie, wycofania nie dotyczy,
bo nie było etapem i nie było linterem:
o dobrą polską prozę z modelu pyta [fiction.md](fiction.md),
a co z niej dało się mierzyć, mówi [linter.md](linter.md#and-fiction).
