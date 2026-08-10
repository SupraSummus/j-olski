# Roadmap

Uporządkowanie, a nie harmonogram.
Dat tu nie ma, bo projekt jest dla przyjemności,
a datowany plan hobby jest sposobem na to, żeby zaczęło przypominać pracę.

Każdy etap ma kryterium wyjścia,
bo „kiedy to jest skończone” jest tą częścią planowania,
która regularnie na siebie zarabia.

Tory są trzy i każdy ma własną numerację.
Numeracja jest kolejnością zależności wewnątrz toru:
etap, który potrzebuje późniejszego, jest usterką planu,
a nie odkryciem na temat pracy.
Poprzez granicę torów taka zależność nie biegnie w żadną stronę,
więc numer z jednego z drugim się nie zestawia
i żaden nie mówi, na co drugi czeka.

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
żeby dało się sprawdzić liczbę, i nie twierdzi o nim nic
([rules.md](rules.md#pattern-density)).

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

Linter stylu dla polskiej dokumentacji technicznej stoi obok, na torze opcjonalnym,
i zachowuje swój plan wraz z numeracją, [niżej](#tor-opcjonalny-linter).
Odwrócenie jest zamierzone:
linter stał tu jako cel, a gramatyka jako tor obok niego,
i tamten układ nie ma wracać przez przeoczenie.

Opcjonalność jest przy tym rozstrzygnięciem o tym, przy czym się siada,
a nie oceną planu niżej:
praca idzie w oba tory wyżej,
a tor lintera czeka.
Przemawia za tym to samo, co wyżej za budowaniem parsera, czyli kształt werdyktu:
reguła nad znakami wskazuje wystąpienie i nie twierdzi o nim nic,
a wypowiedzieć się o zdaniu umie dopiero gramatyka.
Wpisy dotyczące lintera zostają w [TODO.md](../TODO.md) na tych samych prawach
co każdy inny, bo notatka o usterce nie przestaje być prawdziwa przez to,
że tor czeka.

## Celem toru jest to README

Kryterium wyjścia toru gramatycznego jest [README](../README.md) tego repozytorium:
tor kończy się wtedy, gdy każde jego zdanie wyprowadza się w olskim
i gdy każde ma jedno czytanie.
Kryterium mówi, co ma zajść nad zdaniem,
a nie czym ma być wyprowadzone,
więc wybór formalizmu zostaje przy cenie, a nie przy zobowiązaniu,
i trzyma go [design-notes.md](design-notes.md#formalizm-jest-środkiem-a-nie-celem).

Zdaniem jest tu to, co zamyka kropka, wykrzyknik albo pytajnik.
Nagłówek, pozycja listy i wiersz tabeli
dochodzą do olskiego jako akapity, których nic nie punktuje,
i w mianowniku kryterium nie stoją,
bo policzone jako odrzucone mierzyłyby ekstrakcję zamiast podzbioru.
Co je od zdania odróżnia i jak dużą częścią rejestru są, trzyma
[extraction.md](extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem).

Za tym plikiem przemawia to, czym on jest, a nie to, że leży pod ręką.
Stoi po polsku, w rejestrze, o który olskiemu chodzi,
i nikt go pod gramatykę nie pisał,
więc mierzy ją tak, jak zmierzyłby ją cudzy dokument.
[corpus.md](corpus.md#where-the-analyses-stop) trzyma polecenie,
które go przez olskiego przepuszcza,
i kolejność, w jakiej README ustawia to, czego gramatyce brakuje.

README stoi, a rusza się gramatyka.
Przepisanie go pod ten podzbiór kosztowałoby to, po co on jest,
a rachunek trzyma
[CLAUDE.md](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie).

Kryterium ma przy tym pod sobą dwa pytania bez odpowiedzi.
Zdanie wieloznaczne w samej polszczyźnie ma dwa czytania także u olskiego,
więc kryterium żąda od niego tego, czego ono nie ma,
a zdanie odwrotne jest znacznie liczniejsze:
takie, w którym dwa czytania ma olski, a czytelnik jedno.
Oba pytania wraz z pomiarem, który je wycenia, trzyma
[open-questions.md](open-questions.md#kryterium-wyjścia-toru-żąda-jednoznaczności-od-zdania-które-jej-nie-ma).

Druga połowa kryterium jest droższa od pierwszej
i to ona porządkuje etapy niżej.
Wyprowadzenie każdego zdania to pokrycie,
a jedno czytanie na zdanie to ta własność, dla której olski jest podzbiorem,
i każda konstrukcja dopisana do gramatyki wnosi jej tyle samo kłopotu, co pokrycia.
Więc to, co wieloznaczność zawęża, idzie przed tym, co pokrycie podnosi.

**Wyjście:** każde zdanie [README](../README.md) wyprowadza się w olskim
i każde ma dokładnie jedno czytanie,
a pokazuje to polecenie, które
[corpus.md](corpus.md#where-the-analyses-stop) drukuje.

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
README jest taką polszczyzną, więc kryterium żąda wybrania jednego z trzech.

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
Kryterium wyjścia toru nie ruszyła:
nad README nie zmienia ani jednego werdyktu,
bo zdanie z przecinkiem niesie tam także zdanie podrzędne.
Podrzędność jest więc tym, na czym ten etap stoi,
i wobec kryterium wyjścia pozycją najdroższą i nie do ominięcia,
bo README stoi na uzasadnieniach, a uzasadnienie wymaga zdania podrzędnego.

Interpunkcji zostaje w kolejce z banku drzew tyle, ile w niej po przecinku:
wiersz prowadzi myślnik, który jest tam dialogiem z gazety,
czego rejestr olskiego nie ma wcale
([corpus.md](corpus.md#where-the-analyses-stop)).
Bliżej stoi przecinek przed spójnikiem,
czyli `Plany są niczym, ale planowanie jest wszystkim.`,
którego ten etap nie ma
([subset.md](subset.md#what-it-does-not-cover-yet)).

**Wyjście:** zdanie łączące dwa zdania składowe spójnikiem podrzędnym
wyprowadza się i wyprowadza raz,
a pokrycie nad README idzie w górę o te zdania, które na tym stały.

## Etap 5: słowa, których słownik nie ma

Morfeusz zwraca `ign` na formę, której nie zna,
a formy `ign` nie bierze żadna produkcja.
Notację tego rejestru — `docs/linter.md`, `harness/markdown.py` —
olski wpuszcza jako rzeczownik nieodmienny,
bo rzeczownikiem nieodmiennym taka forma w polszczyźnie jest.
Zostaje polskie słowo odmienione, którego słownik nie zna:
`olski`, `lintuje`, `abstencje`, `commitów`.
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

Czas przeszły, przysłówek, `to` w roli łącznika,
negacja wraz z dopełniaczem negacji,
liczebniki i rzeczowniki odczasownikowe.
Kolejka ze Składnicy stawia je na czele:
czas przeszły nie kosztuje tam nic w mocy formalizmu
i jest najtańszym dużym zyskiem, jaki wobec tamtego korpusu został.
Wobec README podnoszą pokrycie dopiero razem,
a żaden z czterech zmierzonych dodany sam go nie rusza.
[corpus.md](corpus.md#where-the-analyses-stop) mierzy to nad czterema z nich,
a nad łącznikiem i negacją nie mierzy nic,
więc tyle samo zostaje tam do dopisania, co tutaj do zbudowania.

Ta rozbieżność jest tym, co je tutaj ustawia.
Etapy porządkuje kryterium wyjścia toru, a nie ranking z banku drzew,
i to jest cena za wybranie takiego kryterium,
a nie usterka w kolejce.

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

Etapem to nie jest, bo kryterium wyjścia toru mówi,
co ma zajść nad zdaniem, a nie czym ma być wyprowadzone.
Formalizm zostaje więc ceną płaconą tam, gdzie któryś etap jej zażąda,
a nie pozycją, którą się planuje osobno.

## Tor składu: drzewo wchodzi, polskie zdanie wychodzi

### Kryterium wyjścia toru składu to znów README

Kryterium wyjścia jest ten sam plik, którym mierzy się tor gramatyczny,
i przemawia za nim to samo, co [wyżej](#celem-toru-jest-to-readme):
stoi po polsku, w rejestrze, o który olskiemu chodzi,
i nikt go pod skład nie pisał.
Żądanie jest jednak drugie.
Tam każde zdanie ma się wyprowadzić i wyprowadzić raz;
tutaj każde ma dać się wypuścić z drzewa napisanego ręcznie,
znak w znak z tym, co w pliku stoi.
Co jest tu zdaniem, rozstrzyga tamta sekcja i rozstrzyga tak samo,
więc oba kryteria czytają jeden tekst.

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
Widać to na jednym zdaniu, bez żadnego pomiaru:
README pisze `zwykły tekst polski`, a to samo drzewo wypuszcza `zwykły polski tekst`.
Ruch wraz z tym, co do niego przeczytać, trzyma [TODO.md](../TODO.md).

Etap stoi pierwszy, bo każdy etap dokładający nowy szyk zdania
będzie tę kategorię realizował,
a drzewa napisane bez niej trzeba by przepisać razem z konstruktorami.

**Wyjście:** `zwykły tekst polski` i `zwykły polski tekst`
biorą się z dwóch różnych drzew,
tak jak biorą się z nich oba szyki orzeczenia imiennego.

### Etap 2: walencja czytana raz

Rama czasownika jest faktem o słowie, a nie o kierunku, w którym się go używa,
więc oba kierunki czytają `olski/leksykon.txt` przez `olski/walencja.py`:
parser robi z niego klasy walencyjne, bo z klasy powstaje produkcja,
a `Robi` w `skład/składnia.py` pyta o jeden lemat, bo tyle stoi w drzewie.
`V.pomagać(R.linter, A.dobry * R.kod)` zgłasza się więc zamiast wypuścić
`Linter pomaga dobry kod.`

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
README pisze `olski`, `lintuje` i `commitów`,
a żadnego z nich nie ma jak wypuścić z drzewa.

**Wyjście:** `Język olski jest podzbiorem polszczyzny.` wychodzi z drzewa,
czyli to samo zdanie, na którym tor gramatyczny ma
[etap 5](#etap-5-słowa-których-słownik-nie-ma),
a każdy wpis leksykonu projektu niesie to, skąd się w nim wziął.

### Etap 5: konstrukcje, których żąda README

Bezokolicznik po czasowniku, zaimek wskazujący i liczebnik.
Negacja wraz z dopełniaczem negacji, koordynacja bytów i zdarzeń,
wyrażenie przyimkowe, przysłówek, przydawka zdaniowa
oraz okolicznik wyrażony zdarzeniem stoją już w `skład/składnia.py`.

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
oraz zdania złożonego w obu pozostałych postaciach,
a README, stojące w czasie teraźniejszym, nie żąda żadnej z tych rzeczy.
Żadnej z nich nie wzięła przy tym za długość:
zdanie podrzędne dokłada się tam, gdzie ktoś ma powód coś zrobić,
a spójnik tam, gdzie zdania mają przestać brzmieć jednakowo
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
a jego miejsce w repozytorium rozstrzyga to,
że reguły tej warstwy stoją już w pakiecie typograficznym lintera,
czyli po stronie sprawdzania, a nie wypuszczania.

Etapem nie jest także warstwa nad zdaniem, czyli `skład/opowieść.py`,
choć stoi i choć wypuszcza czas przeszły oraz opuszczony podmiot.
Jest tak dlatego, że numeracja tego toru liczy to, czego brakuje jednemu zdaniu,
a te dwie rzeczy są własnościami tekstu i żadne zdanie ich w sobie nie ma:
zdanie nie wie, kiedy to było, ani o kim mowa była przed chwilą.
Wywód trzyma
[sklad.md](sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie).

## Tor opcjonalny: linter

Linter stylu dla polskiej dokumentacji technicznej,
przydatny między innymi do sprawdzania tekstów,
które napisały modele językowe.
Zob. [linter.md](linter.md).
Silnik reguł i pakiet typograficzny stoją, a reguły w nim stoją nieskalibrowane,
więc plan niżej jest w większości niewykonany, a nie porzucony.

Gramatyka dochodzi do tego toru jako poziom D,
najgłębszy z poziomów analizy, jakie
[linter.md](linter.md#how-deep-does-each-rule-have-to-see) wylicza,
i schodzą do niego tylko te reguły, które sobie na to zasłużą.
W drugą stronę tor ten nie sięga po nic:
milestone 5 bierze Morfologika i zostawia Morfeusza torowi gramatycznemu
([open-questions.md](open-questions.md#settled)),
więc plan niżej wykonuje się w całości przy gramatyce stojącej tam, gdzie stoi.

### Guiding principles

**Rules are cheap to invent and worthless uncalibrated.**
Build the measurement before building the rule set.

That is also the field's own account
of why models write usable code and unreadable prose:
code came with a verifier and prose did not.
See [fiction.md](fiction.md#why-this-happens).
The account carries its own warning,
because a verifier teaches only what it checks —
[generated-polish.md](generated-polish.md#what-happened-when-the-rules-were-deleted)
records a body of Polish edited into its detectors' image.

**A rule that exists at two tiers is built at the cheaper one first.**
Nominalization density is a lemma rule in principle
and a suffix regex in practice,
and [linter.md](linter.md#suffixes-buy-more-than-expected)
argues the regex reaches most of it.
So the cheap version ships and gets its numbers,
and the version that needs an analyser
has to beat those numbers before its dependency is taken on.
The deepest milestone below applies that test to tier C;
stating it for every tier is what turns morphology
from an assumed step into an earned one.

**A measurement is allowed to come back negative.**
A milestone below the harness exits on a recorded finding
as readily as on a rule pack,
and the finding that good human technical Polish
breaks a norm a pack encodes
closes that milestone by deleting the pack.
A harness whose answer is known in advance is not measuring anything.

### Milestone 0: rule engine and the typography pack

A rule engine over plain Polish text,
plus the rules that need nothing but a tokenizer:
em dash frequency,
Polish quotation marks,
spacing artifacts.

Rules live in data, not in code,
carry an identifier, a message, a register pack,
and a recorded justification.

Markup formats are not in scope.
This is a linter for Polish, not a document-format library,
and separating prose from markup
belongs to whatever reads the markup, not here.

**Exit:** the engine runs over a plain Polish text file
and reports findings with locations,
and adding a rule requires editing data rather than code.
Met, see [rules.md](rules.md).

### Milestone 1: the calibration harness

Before the interesting rules, the thing that makes them honest.
Four deliverables.
They unblock each other in the order listed,
and they do not unblock the same rules.

**An extraction from markup to prose.**
Both halves reach the rules as plain text,
because milestone 0 keeps document formats out of olski
and that makes the extraction a step before the harness rather than part of it.
[generated-polish.md](generated-polish.md#the-apparatus-biases-a-rate-by-an-amount-the-corpus-decides)
prices skipping it:
one mark reads a quarter high over one body of Markdown
and true over another by the same writer,
so a rate measured over apparatus is not comparable
to a rate measured over prose,
nor to the next corpus's rate over its own apparatus.
`harness/markdown.py` does it for Markdown,
and [extraction.md](extraction.md) owns the account
of what it invents by doing it.

**The human half, which is the blocking one.**
Which Polish counts as the good side is **corpus sourcing** in
[open-questions.md](open-questions.md#linter-questions),
a question answered by gathering text rather than by writing code.
The rules below make specific demands of it —
a register represented in the distribution,
a baseline written in Polish rather than translated into it,
and prose whose characters nobody renormalized —
and [corpora.md](corpora.md) surveys what meets them.
Its answer is that the register is scarce enough
that the distribution gets assembled rather than chosen,
and that the rules whose hits get read
want a second corpus rather than a proportion of the first.

**The generated half, generated for the purpose and then left alone.**
[generated-polish.md](generated-polish.md#what-this-corpus-cannot-support)
is the body that was not:
its author had spent six sessions editing against detectors
for the patterns a linter measures,
so its rates are a floor rather than a sample,
and the difference is invisible in the text.
A floor is still worth measuring against as the harder case,
since a rule that fires on prose already edited against detectors
is finding something the editing did not reach.

**The report.**
A per-rule firing rate over a corpus, which `olski --format report` prints:
the command line tool reads every file into one corpus before any rule runs,
so the one-sided half of this is a way of printing the run it already does.
Ranking rules against each other needs both halves,
and [rules.md](rules.md#a-firing-rate-per-rule)
holds what the one-sided half can and cannot say.

#### Two numbers, and the two questions behind them

Every rule leaves this milestone carrying two numbers:
one saying whether it can be trusted,
one saying whether it has anything to do.
Which numbers those are depends on the rule,
because reading a firing rate on human Polish as a false-positive rate
assumes an editor would have removed a real defect before publication,
and the corpus that satisfies it for one rule empties it for another.
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
owns the argument and what each kind of rule owes.

So the pack that exists exits in two pieces.
Its typographic rules exit with their hits read,
over the corpus above whose characters nobody renormalized,
and `em-dash-density` exits with two numbers of its own:
the human distribution its threshold has to sit outside,
and the share of the generated half standing beyond it.

#### The two pieces are not the same size

Which piece to build first follows from the pack's composition
rather than from the order the four deliverables are listed in.
`Check.calibrated_by` in `olski/checks.py` says which of the two a check owes,
an audit of its hits or a distribution to place a threshold in,
and the pack is audit-shaped throughout but for its single rate rule,
so [the audit corpus](corpora.md#the-audit-corpus-polish-documentation-in-version-control)
unblocks nearly every rule shipped
and [the distribution corpus](corpora.md#the-distribution-corpus-edited-original-expository-polish)
unblocks one.

Their costs run the other way.
The audit corpus is [a list of repositories](audit-corpus.md)
with a clone command against each,
and it grows by admitting a repository rather than by gathering words,
so what it costs is that file and the searching to fill it.
The distribution corpus is a composition:
sources in stated proportions,
each share bounded by a defect somebody has to establish it carries,
and a recomputation with each source dropped in turn to find the thresholds
that measure a source rather than the language.

The audit piece therefore goes first,
and the argument for building the second is not the one rate rule it calibrates.
It is that [milestone 3](#milestone-3-statistical-rules) reads every threshold it owns
off the same distribution,
so two milestones pay for one corpus.

The generated half is built with the distribution corpus and not before it,
and the same two milestones pay for it:
it is the second number of that one rate rule
and of every threshold milestone 3 sets.

Which extractions this milestone owes follows from
[the repository list](audit-corpus.md#the-list)
rather than being settled apart from it.
`harness/markdown.py` reads one format,
the list records which format each member is in,
and a second extraction gets written when a repository worth admitting uses another.
So the list is chosen before the extraction is scoped, not after.
The reader of Python modules in the harness is not one of these:
it serves this repository's own prose,
which [prose-in-code.md](prose-in-code.md) says and prices.

**Exit:** every rule in the typography pack carries the two numbers its kind owes,
over a corpus anyone can fetch and a run anyone can redo,
and the pack has changed because of them —
a rule deleted, a threshold moved, or an exemption added —
with the number that caused the change recorded beside it.

Two rules could not reach that exit, and are gone.
`trailing-space` and `orphan-single-letter-word` read where a line ends,
and documentation is written in a markup format,
where a single newline is a space and no line end is one a reader sees.
So the extraction that makes such a corpus readable
takes both properties out with the markup —
[extraction.md](extraction.md#after-joining-a-line-end-rule-has-nothing-left-to-read)
holds what the step removes —
and running them over the files instead reads the format's line ends
rather than a reader's,
which [rules.md](rules.md#a-check-may-be-asking-more-of-a-document-than-its-format-gives)
refuses.
Neither could therefore exit on a number,
so each exited on a decision:
either the pack claims prose laid out in lines as a register of its own,
or the two rules go, and they went.
What settled it was reading their hits across both corpora,
which turned up no instance of either defect,
and [firing-rates.md](firing-rates.md#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt)
holds those counts along with the machinery the deletion took with them.
That is the shape the exit above asks for,
a rule deleted with the number that caused it recorded beside it.

### Milestone 2: the plain-Polish pack, without an analyser

The rules with a citable Polish norm behind them,
which are also, conveniently, model tells:

- Rzeczowniki zombie, `-anie` and `-enie` and `-cie` density
- The phrases that invite them,
  `w celu`, `w razie`, `z powodu`, `na skutek`
- Impersonal `-no` and `-to`
- `można`, `trzeba`, `należy`, `warto`
- Participle chains, `będąc` and `mając` and the `-ąc` form generally
- Booster inflation matched on the stem,
  `kluczow`, `istotn`, `przełomow`

Each rule cites the plain-Polish source it comes from,
not a model it was observed in.

Two of the three nominalization endings need no morphology,
which is why the pack stands here rather than behind the analyser,
and the third one does.
[linter.md](linter.md#what-the-nominalization-endings-match) holds the measurement:
`-cie` matches the locative singular of `format` and `kontekst`
more often than it matches a nominalization,
where the other two barely match an inflected form at all,
and a stem reaches an adjective's paradigm without a lemma either way.

What the suffix route costs beyond that ending is not a class a lemma removes.
Morfeusz gives `zdanie` and `mieszkanie`, which are not zombie nouns,
the pair of readings it gives `pobranie`,
so the analyser agrees with the ending about the words the ending gets wrong,
and half of this pack's matches over the audit corpus sit in that agreement.
Whether that cost is affordable is what the two numbers are for,
and the ambiguity is where it is likeliest to prove not to be,
because it is the half no later milestone is holding a fix for.

The impersonal pair comes out of the same run the other way,
and [linter.md](linter.md#the-impersonal-endings-come-out-the-other-way)
holds it.
A tag answers what a judgement had to answer above,
so `-no` is the cleanest ending measured anywhere here
and the adverbs this milestone warns of are a twentieth of its matches,
while `-to` is one common word away from the same,
that word being the pronoun.
So the pack is three rules with three prognoses rather than one with one,
and which of the three a rule is
does not follow from all of them being suffixes.

What is left unmeasured is the boosters,
whose stems are not endings and want a match this run does not do.
[TODO.md](../TODO.md) holds them,
in front of the rules rather than after them,
a class a pattern cannot separate deciding whether a rule exists
rather than how it is tuned.

**Exit:** the pack is calibrated,
and its false discovery rate
on [the audit corpus](corpora.md#the-audit-corpus-polish-documentation-in-version-control)
is at or below the figure proselint reported for itself —
one false positive per ten true positives,
which is about nine false alarms in every hundred hits —
or the milestone records why a different bar is the right one for Polish.
[prose-linters.md](prose-linters.md#proselint-measured-what-everyone-else-asserts)
owns that figure and the corpus it was measured on.

Why that corpus and not the other follows from the shape of the number.
A false discovery rate is a share of hits a reader judged,
so it is the audit shape and it wants documentation rather than a distribution,
which leaves one candidate among the two corpora milestone 1 assembles.
What the audit corpus supplies is documentation somebody reviewed before merging,
where proselint's figure was taken over prose a copy editor worked on,
and the two are not the same pass.
The bar is quoted here against a different kind of editing,
which is one of the reasons the milestone is allowed to argue for another bar.
The other is authors:
a share measured over a corpus whose largest file is one person's habit
describes the person, and
[corpora.md](corpora.md#not-yet-decided) holds how many it takes before it stops.

### Milestone 3: statistical rules

Sentence-length variance,
paragraph-length uniformity,
three-item list frequency,
bullet density inside prose,
fact density,
connector density,
the share of sections that close on a negation,
the share of sentences opening on a fronted clause,
and the walk-on share `entity-recurrence` already computes
and no rule yet declares.

These need thresholds, not just patterns,
and a threshold is a point in the human distribution from milestone 1.

One kind of machinery is missing.
A share over units — of sections, of sentences — is a statistic
no check computes, since a rate per thousand words is not one.
[generated-polish.md](generated-polish.md#the-closing-sentence-is-measurably-different)
measures the negation share and says why such a finding
is a report about a document rather than an accusation against a sentence.

StyloMetrix from NASK extracts 195 stylometric features for Polish,
so the decision this milestone owes is
whether the features come from there or from checks written here.
The question that decides it is whether a feature arrives
with a location a finding can point at,
since a finding is a location and a feature vector is not.

**Exit:** every threshold is a stated point in the human distribution
rather than a chosen number,
with the point and the distribution recorded,
and the generated half saying for each threshold
how much of it lies beyond.

### Milestone 4: the delivery decision

Three routes:

- A standalone tool with its own rule format
- A Vale-compatible style,
  inheriting its editor and CI integration
- LanguageTool XML rules,
  inheriting an installed base and Morfologik

The decision stands here rather than at the end
because it decides whether the milestone after it exists.
A Vale style reaches tier A and stops,
since Vale's tagger ships an English model:
see [prose-linters.md](prose-linters.md#vale-is-the-architecture-to-study).
The LanguageTool route arrives with Morfologik already wired up,
so morphology becomes something the platform has
rather than something to build:
see [linter.md](linter.md#what-already-exists).
Only the standalone route leaves it as work.

Everything above is route-independent,
which is why the decision can wait this long,
and by here there is a calibrated pack to deliver,
which is why it need not wait longer.

One thing a route either supplies or leaves to be built,
waiting in [rules.md](rules.md#not-yet-decided):
a way to silence a rule on one line or one file.

**Exit:** a decision with its reasoning recorded.

### Milestone 5: morphology binding, and the rules that needed it

Lemmatization and part-of-speech tagging,
so lexical rules match inflected forms
and morphosyntactic rules become possible:

- Anglicisms and calques keyed by lemma
- `się` passives, which need the verb before the pronoun can be read
- Adjective stacking before a noun
- Comparative adjective frequency
- Lemma type-token ratio
- Echo sentences, measured as lemma overlap between neighbouring sentences

The analyser is Morfologik, decided in
[open-questions.md](open-questions.md#settled):
the grammar track needs generation and only Morfeusz does it,
which leaves this track free to take the analyser LanguageTool is built on.
How much that inheritance is worth
is what the milestone above has just settled.
The cost is a second analyser and a second tagset
in a repository whose grammar track already runs Morfeusz for analysis.

Whichever analyser is in use,
it owes its callers character offsets and not just forms,
because a finding is a location and an analysis is not:
`Segment` in `olski/morph.py` carries node numbers of a segmentation graph,
which is the shape of the problem rather than an accident of Morfeusz.

**Exit:** a lexical rule written as a lemma
catches every inflected form of it in running text,
and its findings point at the forms they matched.
Where the rule has a suffix approximation from milestone 2,
the lemma version beats it on the numbers from milestone 1;
where it does not, the approximation stays
and the analyser has not paid for itself.

### Milestone 6: deeper analysis, only where earned

Chunking or dependency parsing,
for the rules that need constructions rather than strings:
subject-predicate distance,
clause depth,
parallel-negation frames,
and fronting for gravity.

The last two are here for what is left of them
once the cheap versions have been built above.
The commonest Polish parallel-negation frame is punctuated rather than lexical,
so `em-dash-density` fires on the construction without having been aimed at it,
and tier C gets the lexical form:
[generated-polish.md](generated-polish.md#what-the-em-dashes-are-doing)
holds the rates that say which is which.
Fronting has a clause-fronted half a tier-A pattern reaches,
and a phrase-fronted half that
[linter.md](linter.md#recognizing-a-phrase-by-what-it-is-not-costs-more)
argues is beyond a better regex and beyond a lemma alike,
which makes it the candidate this milestone exists for.

**Exit:** at least one rule that could not work at tier B
working at tier C,
with the added machinery justified by that rule's calibration numbers.

### Wish, not milestone: prose and fiction

Making language models write good Polish fiction
is an open research question,
and [linter.md](linter.md#and-fiction) records
what is lintable there,
what is not,
and the three directions that look more promising than linting:
generative constraints,
stylometric targets rather than stylometric alarms,
and the linter as a deterministic critic inside a revision loop.
[fiction.md](fiction.md) surveys the research underneath that:
the documented failure modes,
and the finding that post-training rather than prompting produces them.

Deliberately not a milestone.
Labelling a research question as a deliverable
is how hobby projects die.

### What would count as finished enough

- A rule pack for Polish technical documentation
  where every rule carries its two numbers
  and a stated justification
- Run over a real document,
  producing findings a Polish technical writer agrees with
- At least one rule deleted because the numbers said so
- Honest documentation of what the tool does not do,
  starting with the fact that it is not a detector

None of that requires the project to be useful,
and all of it would be novel for Polish.
