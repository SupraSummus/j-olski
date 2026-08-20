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

Cel jest trzecią rzeczą obok kryterium i kierunku, i ma [własną sekcję](#cele).
Mówi, czego chcemy od narzędzia, a nie kiedy praca się kończy,
więc wolno mu zostać nieosiągniętym.

Tory są dwa i każdy ma własną numerację.
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
żeby dało się sprawdzić liczbę, i nie twierdzi o nim nic.

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

Cztery szyki podmiotu, dopełnienia i czasownika są przykładem samego kierunku,
a nie któregoś etapu.
Nie ma ich w żadnej kolejce blokerów, bo szyk nie jest formą,
na której analiza staje, i żaden korpus o nie nie prosił.
Prosił o nie werdykt: dopełniacz negacji stojący przed swoim czasownikiem
nie miał ciała, więc olski czytał pięć zdań Składnicy odwrotnie,
niż czyta je czytelnik, i mówił to jednym czytaniem.
Dopisane, kupują kilkadziesiąt zdań banku drzew, kosztują sześć
i cztery z tych sześciu są tamtą naprawą
([subset.md](subset.md#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka)).
Pokrycie wyszło więc skutkiem, dokładnie tak, jak ten kierunek mówi,
że wyjdzie.

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

Przeredagowanie tego pliku rusza same liczby,
a nie zakaz przepisywania tych dokumentów pod gramatykę
([CLAUDE.md](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).

Kolejki form bez licencji ten plik już nie ustawia,
bo prawie każde jego odrzucenie stoi na strukturze,
a formy, które zostały, są pojedynczymi wystąpieniami.
Czego gramatyce brakuje wobec tego pliku, mówi więc odtąd samo zatrzymanie analizy,
a nie część mowy, na której ono padło,
i tego zatrzymania werdykt jeszcze nie nazywa ([TODO.md](../TODO.md)).

## Cele

Etap ma kryterium wyjścia, tor gramatyczny ma kierunek,
a cel mówi, po co to wszystko jest.
Cel kryterium nie zastępuje:
niespełnione kryterium jest robotą do zrobienia,
a cel wolno mieć nieosiągnięty, dopóki mówi, co by go osiągnęło.
Lista jest zbiorem, a nie kolejnością, i żaden z celów nie czeka na inny.
Żaden z nich nie kończy przy tym toru gramatycznego:
cel nieosiągalny nie jest kryterium, a osiągnięty nie zamyka toru.

Dwa powody, dla których README przestało być kryterium
([wyżej](#tor-gramatyczny-nie-ma-końca)), dają dwie zasady,
które cel z tej listy ma wytrzymać.
Pierwsza: cel nazywa, czym się go sprawdza.
Nieosiągalny cel jest dopuszczalny, niesprawdzalny nie.
Druga: cel nad tekstem, który sami piszemy, mierzy zdolność, a nie udział,
bo udział skraca przeredagowany akapit tak samo jak dopisana produkcja,
a wydruk nie mówi, które z dwojga zaszło.
Trzecia zasada przychodzi z toru lintera ([niżej](#tor-lintera-jest-wycofany)),
gdzie etap, na który nikt nie czeka, okazał się zaległością, a nie planem:
cel, którego nikt nie podnosi, kasuje się razem z pracą, którą niósł.

**Wzorzec prozy ma wykrywacz, a repozytorium jest od niego czyste.**
CLAUDE.md wylicza wzorce, których w prozie nie chcemy —
zdanie echo i wzmacniacz bez treści wśród
[fraz gotowych](../CLAUDE.md#a-phrase-that-arrived-ready-made-was-not-chosen),
peryfrazę i czasownik domowy wśród tego,
[dla kogo zdanie jest napisane](../CLAUDE.md#dla-kogo-jest-napisane-zdanie) —
a sprawdza je przegląd zmian, czyli człowiek czytający zdanie po zdaniu.
Cel żąda, żeby wzorzec raz nazwany dostał wykrywacz,
a wykrywacz przeszedł po całej prozie repozytorium i stanął na zerze.
Sprawdza go przebieg, a nie udział, więc przeredagowanie akapitu jest tu robotą.
Wycofanego toru cel ten nie wskrzesza, choć wygląda podobnie,
a różni je populacja:
tamten zestaw reguł strzelał nad cudzą polszczyzną i żądał kalibracji,
której się nie doczekał,
a ten chodzi po tekście, który sami napisaliśmy,
więc trafienia czyta się wszystkie, zamiast progować ich stopę.
Milczenie kosztuje przy tym zero:
zdanie, którego olski nie wyprowadza, zostaje przy przeglądzie,
czyli przy tym, co je dziś sprawdza,
więc cel nie żąda od tych dokumentów, żeby zmieściły się pod gramatykę
([CLAUDE.md](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).
Osiągnięty, unieważni zdanie z CLAUDE.md,
że reguł prozy nie pilnuje żaden check, a pilnuje ich przegląd;
póki nie jest osiągnięty, zdanie to obowiązuje.
Czeka na czytnik prozy z modułów, bo docstring i blok komentarza
są prozą tych samych reguł:
taki czytnik wyszedł razem z torem lintera i trzyma go git,
więc wraca poleceniem `git show f5f5561^:harness/python.py`,
zamiast powstawać od nowa.

**Zdanie polskiej dokumentacji technicznej wyprowadza się i wyprowadza raz.**
Jest to żądanie, które upadło nad README,
postawione tym razem nad korpusem przypiętym,
czyli takim, którego nasz commit nie rusza.
Rejestr ten ma dziś zmierzoną ustawę —
gramatyka wyprowadza tam jednoznacznie kilkadziesiąt zdań z kilku tysięcy
([ustawy.md](ustawy.md)) —
a dokumentacja formatu, czyli tekst najbliższy temu, po co olski jest,
przeszła przez olskiego po to, żeby zmierzyć ekstrakcję
([extraction.md](extraction.md#what-the-numbers-here-were-run-over)),
i werdyktów nad nią nikt nie policzył.
Osiągnięty w całości nie będzie, bo rejestr niesie zdania,
których żaden podzbiór nie weźmie,
więc sprawdza go liczba nad korpusem przypiętym i to, w którą stronę idzie.

**Zdanie wraca z drzewa tym samym zdaniem.**
Obieg jest dziś zamknięty w jedną stronę — drzewo w tekst, tekst w drzewo —
niezmiennik trzyma [design-notes.md](design-notes.md#the-round-trip-invariant),
a robi to `olski/skład/rozbiór.py`.
Cel żąda drugiej strony: zdanie rozebrane, zrozumiane i wypisane z powrotem,
znak w znak.
Filtr w środku jest parametrem tego przebiegu, a nie osobnym celem:
„użyj formy przestarzałej, jeżeli słownik ją ma” odwraca odsiew,
który robi `_w_rejestrze` w `olski/skład/morfologia.py`,
a „nie używaj tej konstrukcji” jest tym, co pomiar różnicowy robi już dziś,
zdejmując produkcje i porównując werdykty (`harness/ruch.py`).
Blokuje ten cel pytanie otwarte, a nie brak kodu:
jedno czytanie wraca kilkoma drzewami
([sklad.md](sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma)),
a wypisać trzeba jedno,
więc cel jest tym, co każe odpowiedzieć na
[pytanie o ranking nad lasem](open-questions.md#the-round-trip-guarantee).
Dokument skłania się tam dziś ku „nie”, i jeżeli przy tym zostanie,
celu w tym brzmieniu nie ma jak osiągnąć — co jest odpowiedzią, a nie porażką.

**Podmiana synonimu zostawia to samo drzewo.**
Wariant powyższego, osobny dlatego, że sprawdza się czym innym:
zamień słowo na bliskoznaczne, wypisz zdanie na nowo i rozbierz je,
a drzewo ma wrócić to samo.
Zdania, w których nie wraca, nazywają miejsce,
w którym wycieka rodzaj albo walencja,
więc jest to sprawdzian obiegu tańszy niż każdy, jaki dziś mamy.
Że przeżyje znaczenie, cel nie obiecuje, bo na to testu nie ma,
i nie odwraca to decyzji, że tożsamość rzeczy jest deklaracją autora,
a nie wnioskiem ze słownika synonimów
([sklad.md](sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)).
Kupuje przy tym mechaniczną połowę reguły, która już obowiązuje:
przy czasowniku domowym [CLAUDE.md](../CLAUDE.md#dla-kogo-jest-napisane-zdanie)
każe podstawić czasownik dokładny i sprawdzić, czy zdanie zyskało.
Czeka na tezaurus, którego to repozytorium nie ma w żadnej postaci,
a że jest to pytanie do świata, zapisuje je
[open-questions.md](open-questions.md#shared-questions).

Czego na tej liście nie ma.
Kierunku, bo prowadzi on tor, zamiast stać na jego końcu,
i ma [własną sekcję](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).
Kryterium toru składu, bo jest kryterium, a zapisuje je
[jego własna sekcja](#kryterium-wyjścia-toru-składu-to-znów-readme).
Nie ma też sparsowanej prozy tego repozytorium,
która była pierwszym brzmieniem celu o wykrywaczu i upadła na drugiej zasadzie:
udział zdań wyprowadzonych z naszego tekstu skraca przeredagowany akapit,
a wykrywacz, który ma stać na zerze, skraca tylko poprawione zdanie.

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

Leksykon urósł po tym etapie i urósł zdaniami na lemat oraz kolumną przyimków,
którą czyta warstwa rozstrzygająca, a nie gramatyka.
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

Dwie pozycje podrzędności, których gramatyce brakowało,
odsłoniło właśnie to dopisanie,
a każda z nich wchodzi niżej razem ze swoim pomiarem.

Okolicznik wyrażony zdaniem wchodzi obiema pozycjami, przed swoim zdaniem i za nim,
i jest pierwszym policzonym dopisaniem tego etapu.
Zdejmuje on z listy odrzuconych blisko pięćdziesiąt zdań Składnicy,
a jednoznaczności nie odbiera pod złotą morfologią ani jednemu zdaniu
i sześciu pod żywą
([subset.md](subset.md#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie)).
Płaci się tu za to samo, co przy przysłówku:
te sześć zdań wychodziło przedtem jednym czytaniem, którego polszczyzna nie ma,
bo `gdy` stoi w nich jako okolicznik przysłówkowy po przecinku koordynacji.
Nad prozą tego repozytorium nie kupuje ani jednego zdania,
tak samo jak cztery dopisania przed nim,
i jest to o tamtej kolejce odczyt, a nie o konstrukcji:
zdanie tego pliku, które stało na spójniku, stoi także na rzeczowniku
odczasownikowym albo na średniku.
Zostają z tej listy spójniki trybu przypuszczającego, czyli `aby` i `żeby`
([subset.md](subset.md#tryb-przypuszczający-jest-cząstką-przy-czasowniku-a-nie-cechą-zdania)).

Interpunkcja zdaniowa jest drugim policzonym dopisaniem tego etapu
i jest zarazem najtańszym, jakie ta gramatyka dotąd przyjęła:
dwukropek otwierający zdanie, średnik oraz przecinek przed spójnikiem
zdejmują z listy odrzuconych sześćdziesiąt pięć zdań Składnicy,
a jednoznaczności nie odbierają ani jednemu zdaniu pod żadną z dwóch morfologii
([subset.md](subset.md#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego)).
Zero po stronie ceny nie jest przy dwukropku ani przy średniku wynikiem przebiegu:
żadnego z tych znaków nie brała przedtem produkcja,
więc zdanie z nim nie miało czytania, z którego dałoby się je wytrącić.
Kolejka nad prozą tego repozytorium stawiała dwukropek na czele
([corpus.md](corpus.md#where-the-analyses-stop))
i nad tym plikiem nie kupuje ta trójka żadnego zdania przyjętego,
tak samo jak dopisania przed nią,
za to zdejmuje z listy form bez licencji wszystkie trzy znaki naraz,
więc osiemnaście zdań README staje odtąd na strukturze, a nie na znaku.
Nad rejestrem ustaw kupuje jedno zdanie i nic nie odbiera
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
więc trzeci rejestr odpowiedział tu tak samo jak drugi, tylko ciszej.

Średnik wszedł do tej trójki później niż dwukropek i wszedł za sam rejestr:
argumentu o polszczyźnie nie ma, bo znak ten stoi tam, gdzie stanąłby przecinek
albo kropka, a zdanie README, które go niesie, jest tym, co za nim przemawia.
Zakup wypadł przy nim na dwa zdania Składnicy i jedno zdanie ustawy,
czyli o rząd wielkości mniej niż przy przecinku przed spójnikiem.

Płaci za tę parę osobny warunek, i nie płaci ani w zdaniach, ani w czytaniach:
przecinek przed spójnikiem nie kupowałby prawie nic,
dopóki `a` czyta się jako przyimek rządzący mianownikiem,
a warunek, który to czytanie odbiera, sam odbiera zdanie README —
i to samo zdanie wraca z tą parą, z trzema czytaniami w miejsce trzech,
tylko że prawdziwymi
([subset.md](subset.md#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)).
Cena wypadła więc trzeci raz poza obie waluty, którymi ten kierunek mierzy,
i wypadła po stronie zakupu.

Pytanie jest trzecim policzonym dopisaniem tego etapu
i jest z nich wszystkich najtańsze: cena wyszła zerowa w obu korpusach,
pod obiema morfologiami banku drzew
([subset.md](subset.md#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał)).
Zdanie pytające i pytanie zależne weszły razem, bo dzielą kształt ze zdaniem względnym,
a zakup wyszedł na jedno zdanie w banku drzew i jedno w ustawach.
Jedno z nich jest zarazem tym zdaniem, które ten etap wcześniej zabrał:
warunek na lemat, którym etap zdjął czytanie współrzędne, nazwał zarazem pozycję,
której gramatyce brakowało, i pytanie ją stawia.

Zakup jednym zdaniem na korpus jest odczytem o rejestrze, a nie o produkcjach:
pytań jest w Składnicy jedno na piętnaście zdań,
a otwiera je `czy`, `kto`, `co`, `jak` albo `dlaczego`,
czyli słowa żądające każde innego kształtu niż grupa imienna na czole zdania.
Kolejka po tym dopisaniu jest więc kolejką kształtów pytania,
a nie listą lematów do dopisania obok jednego, który olski ma.

Grupa wysunięta razem z zaimkiem pod przyimkiem
jest czwartym policzonym dopisaniem tego etapu.
Polszczyzna wysuwa na czoło nie tylko zaimek `który`, ale i grupę, w której on stoi,
a grupa ta rozchodzi cechy na dwie strony:
przypadek do przyimka nad sobą, a liczbę i rodzaj do poprzednika
([subset.md](subset.md#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania)).
Cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew,
a zakup drobny: dwa zdania „Zasad techniki prawodawczej” i jedno Składnicy.
Zera po stronie ceny nikt tu nie przewidział,
bo grupa następuje po przyimku, którego przyłączenia olski nie wybiera.
Nie kosztuje ona dlatego, że żąda dwóch przypadków naraz:
dopełniacza od zaimka i przypadka przyimka od swojej głowy.

Pytanie o tę grupę weszło razem z nią i nie kupiło ani jednego zdania nigdzie,
co jest o rejestrze odczytem, a nie o produkcji:
`W którym roku ustawa weszła?` napisała ta dokumentacja, a nie żaden korpus.
Zdanie względne żądało tu kształtu grupy, a pytanie drugiego czoła,
i te dwie połowy zostały przez to policzone osobno.

Ta sama grupa wysunięta bez przyimka jest piątym policzonym dopisaniem
i pierwszym, którego przeszkodą jest zgodność.
Grupa niesie liczbę i rodzaj dwa razy, bo orzeczenie zgadza się z jej głową,
a poprzednik z jej zaimkiem, więc para jedna wydaje werdykt pewny siebie i błędny —
raz przyjmując `Ustawa, której przepisy obowiązuje`,
a raz `Ustawy, której przepisy obowiązują`
([subset.md](subset.md#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania)).
Cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew,
tak samo jak przy pozycji pod przyimkiem,
a zakup jest pierwszym, jaki ta konstrukcja robi nad bankiem drzew
pod złotą morfologią: jedno zdanie przyjęte i trzy wyciągnięte z odrzucenia.
Rejestry odpowiadają przy tym na obie pozycje różnie:
rozporządzenie rusza tylko pierwsza, siedem ustaw tylko druga, a bank drzew obie,
i to jest odczyt o rejestrach, bo kształt grupy jest w obu pozycjach ten sam.
Nad prozą tego repozytorium nie kupuje ani jednego zdania,
tak samo jak dopisania przed nią.

Kopuła opuszczona jest szóstym policzonym dopisaniem tego etapu,
czyli zdaniem względnym, które obywa się bez czasownika: `o którym mowa`.
Pozycji tej nie ustawiła ani kolejka ze Składnicy, ani ranking form bez licencji,
bo każda forma tego zwrotu licencję ma, a odrzucenie stało na strukturze;
znalazł ją grep, którym mierzono szyki grupy wysuniętej.
Gramatyka wpuszcza ją wpisem na jeden lemat, a nie pozycją ogólną,
bo pozycja ogólna czyni zdaniem składowym każdą grupę imienną w mianowniku,
czyli psuje każdy ciąg współrzędny takich grup
([subset.md](subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną)).
Cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew,
a zakupem jest jedno zdanie rejestru ustaw,
czyli przeszło o dwa rzędy wielkości mniej, niż obiecywało 851 wystąpień tego zwrotu:
prawodawca pisze go razem z adresem przepisu, a cyfry olski nie bierze
([subset.md](subset.md#kopułę-opuszczoną-zmierzono-nie-kosztuje-nic-i-kupuje-mniej-niż-obiecywała-jej-częstość)).

Lista pozycji tego etapu jest przez to pusta,
a otwarte zostaje samo jego wyjście drugie, czyli pokrycie nad README.
Brak tego pokrycia jest odczytem o pomiarze nad tym plikiem, a nie o podrzędności,
i akapit wyżej nazywa formy, na których stoją zdania stojące przedtem na spójniku.

## Etap 5: słowa, których słownik nie ma

Morfeusz zwraca `ign` na formę, której nie zna,
a formy `ign` nie bierze żadna produkcja.
Notację tego rejestru — `docs/subset.md`, `harness/markdown.py` —
olski wpuszcza jako rzeczownik nieodmienny,
bo rzeczownikiem nieodmiennym taka forma w polszczyźnie jest.
Drugą połową klasy jest polskie słowo odmienione, którego słownik nie zna:
`olski`, `commitów`, `Pythonem`.
Dla niego to samo czytanie byłoby nie tylko nieznane, ale fałszywe,
i dlatego [subset.md](subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)
trzyma tę połowę osobno od tamtej.

Etap nie zależy od czterech powyżej ani one od niego,
a numeracja żąda tylko tego, żeby żaden nie potrzebował późniejszego.
Stoi tutaj, bo rejestr, o który chodzi, jest takich słów pełen,
a bank drzew tej klasy nie pokazuje w ogóle:
tam każdy token ma rozbiór wybrany przez człowieka,
więc kolejki z niego ta klasa nie ustawia
i widać ją dopiero w przebiegu nad dokumentacją.

**Wyjście:** `Język olski jest podzbiorem polszczyzny.`
wyprowadza się i wyprowadza raz.
Zaliczone: odmianę takiego słowa deklaruje `olski/projekt.txt`,
wskazując leksem, wedle którego się ono odmienia, wraz z formą, którą ten leksem
ma wydać, zob.
[subset.md](subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma).
Etap kupił mechanizm, a nie listę słów, i widać to po cenie:
ani jednej formy tego leksykonu słownik nie czyta,
więc zdanie, które się wyprowadza, nie ma jak stracić przez niego jednoznaczności
([subset.md](subset.md#leksykon-projektu-zmierzono-nie-odbiera-ani-jednego-zdania-bo-tych-form-słownik-nie-czyta)).
Zdania przyjętego nie kupuje przy tym nad README ani jednego,
tak samo jak dopisania przed nim,
a klasa, która stała w tamtej kolejce na czele, z niej schodzi.
Słowo bez wpisu wraca dalej jako `ign`,
i jest to odtąd brak wiersza w jednym pliku, a nie brak pozycji w gramatyce.

## Etap 6: reszta konstrukcji

`to` w roli łącznika i liczebnik pisany cyfrą.
Kolejka ze Składnicy stawia oba wysoko, bo `to` prowadzi w niej dwa wiersze.
Wobec README podnoszą pokrycie dopiero razem,
a żaden z pięciu zmierzonych dodany sam go nie rusza.
[corpus.md](corpus.md#where-the-analyses-stop) mierzy to nad czterema z nich,
a nad łącznikiem nie mierzy nic,
więc tyle samo zostaje tam do dopisania, co tutaj do zbudowania.

Lista, którą ten etap ma opróżnić, ma jednak dwa źródła
i drugim z nich nie jest kolejka.
Narzędnik bez przyimka, koordynacja `a nie`, dopowiedzenie z `czyli`
i imiesłów czynny przy rzeczowniku weszły na nią z przebiegu nad prozą,
która ten rejestr pisze, czyli jako zdania odrzucone, a nie jako wiersz częstości.
Trzy z tych czterech są przy tym kształtem, a nie formą,
więc kolejka blokerów nie widzi ich w ogóle
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
i tym różni się to źródło od tamtego: pokazuje pozycje, których tamto nie stawia.

Cztery pozycje stoją na tej liście z kolejki czytanej po części mowy,
a nie po formie, i nie stawia ich ani jedno z tych dwóch źródeł:
czasownik nieosobowy, czas przyszły złożony, imiesłów przysłówkowy
i zaimek `siebie`
([subset.md](subset.md#what-it-does-not-cover-yet)).
Dwa pierwsze stoją w kolejce wysoko i niosą po jednej konstrukcji na cały wiersz,
więc wiersz nazywa je wprost,
gdzie wiersze przed nimi grupują po kilka konstrukcji naraz
i dopiero czytanie form mówi, o które idzie.
Zmierzona nie jest z nich żadna,
a kolejność między nimi rozstrzyga cena,
tak samo jak przy pozostałych pozycjach tej listy.

Na koniec wychodzą dlatego, że żadna z nich nie żąda niczego
od produkcji pisanych po niej,
więc [koszt przepisywania](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)
ich nie porządkuje, a między sobą rozstrzyga je sama cena.
Dwie kolejki, które ją wyceniają, nie zgadzają się co do kolejności,
i jest to wynik pomiaru, a nie usterka w którejś z nich.

Liczebnik pisany słowem był na tej liście i zszedł z niej cały,
a cyfra została i jest osobną pozycją, a nie resztą tej samej.
Kupił on 56 zdań Składnicy przy 35 uczynionych wieloznacznymi,
jedno zdanie README i jedno zdanie ustawy,
a jednoznaczności nie odebrał ani jednemu zdaniu przyjętemu wcześniej,
w żadnym z tych trzech korpusów
([subset.md](subset.md#liczebnik-zmierzono-i-nie-odbiera-ani-jednego-zdania)).
Tym różni się od czasu przeszłego, który nad ustawami zabrał pięć.
Sam ranking wypadł natomiast tak samo jak przy nim:
wiersz `num` obiecywał 453 zdania i oddał 91,
gdzie `praet` obiecywał 2934 i oddał 566, czyli oba po jednej piątej.
Cyfrę zdejmie z tej listy warstwa nad morfologią, a nie produkcja,
bo `dig` nie niesie ani przypadka, ani liczby
([subset.md](subset.md#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii)),
i tym różni się ta pozycja od pozostałych czterech.

Negacja była na tej liście i zeszła z niej cała, razem z dopełniaczem negacji,
bo cząstka bez tego przypadka kupuje dwie trzecie tego, co obie razem.
Kupiła 146 zdań Składnicy przy 45 uczynionych wieloznacznymi
i cztery zdania ustawy przy trzydziestu,
a jednoznaczność odebrała jednemu zdaniu przyjętemu wcześniej —
i nie odebrał jej dopełniacz, tylko czytanie zaimka, które słownik daje formie
`nie` ([subset.md](subset.md#negacja-zmierzona-kupuje-przeszło-sto-zdań-i-nie-płaci-dopełniaczem)).
Ranking wypadł przy niej lepiej niż przy tamtych dwóch:
wiersz `qub` obiecywał 710 zdań na samym `nie` i oddał 191, czyli ponad jedną
czwartą, gdzie tamte oddawały po jednej piątej.
Płaci za to gdzie indziej: trzy zdania olski czyta po tej zmianie odwrotnie,
niż czyta je czytelnik, bo dopełniacz stojący przed czasownikiem
wpada do grupy imiennej przed nim, a szyku, który by go stamtąd wyjął,
gramatyka nie ma
([subset.md](subset.md#cena-stoi-w-trafności-a-nie-w-liczbie-czytań)).
Cena konstrukcji nie musi więc dać się policzyć w żadnej z dwóch walut,
które ta sekcja zna.

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

Przysłówek zszedł z tej listy cały, czyli obu swoimi gospodarzami,
i jest największym dopisaniem, jakie ta lista dotąd oddała:
zdań przyjętych nad Składnicą jest po nim o ponad jedną trzecią więcej
([corpus.md](corpus.md#the-measurement)).
Wybór był między dwiema cenami w różnych walutach —
zdaniami, którym drugi gospodarz odbiera jednoznaczność,
przeciw werdyktom, które pierwszy sam wydaje wbrew drzewu —
i rozstrzygnął go [kierunek](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę):
za każde zdanie oddane drugiemu gospodarzowi ubywa jedno czytanie nieprawdziwe,
a `valid` mówiący o zdaniu nieprawdę czyta się jak twierdzenie
([subset.md](subset.md#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)).
Nad README nie kupuje ani jednego zdania, tak samo jak cztery dopisania przed nim,
a cztery zdania przenosi z odrzuconych na wieloznaczne;
dwa z tych czterech przyszły tam po nim, razem z interpunkcją zdaniową.
Ranking wypadł przy nim lepiej niż przy każdym z tamtych czterech:
wiersz `adv` obiecywał 1992 zdania i oddał prawie jedną trzecią tego.

Cząstka na tej liście nie stała i weszła prosto z przebiegu nad prozą,
czyli z tego samego źródła, z którego weszły na nią cztery pozycje wyżej.
Kupiła dziewięćdziesiąt jeden zdań Składnicy przy siedemdziesięciu dziewięciu
uczynionych wieloznacznymi, a jednoznaczności nie odebrała ani jednemu zdaniu
([subset.md](subset.md#cząstkę-zmierzono-kupuje-kilkadziesiąt-zdań-a-płaci-zasięgiem-podmiotu)).
Cena wypadła i tu poza obie waluty tego etapu, a wypadła w zasięgu:
dziewięć zdań nowo przyjętych olski czyta ciaśniej, niż czyta je bank drzew,
bo cząstka stoi tam wewnątrz grupy imiennej, a tu przy zdaniu.
Drugi gospodarz, który by to zdjął, jest tym samym wyborem, co przy przysłówku,
i [TODO.md](../TODO.md) trzyma go razem z jego ceną.
Pary do przelicznika niżej to dopisanie nie dokłada z tego samego powodu,
z którego nie dokłada jej rzeczownik odczasownikowy.

Interpunkcja obejmująca — cudzysłów i nawias — weszła tą samą drogą,
a różni ją to, czym za nią przemawia proza:
w prozie ustaw i w prasie te znaki stoją, ale zdania z nimi stoją także na czym innym,
więc zakup jest tam liczony w pojedynczych zdaniach
([subset.md](subset.md#interpunkcję-obejmującą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania)).
Cena wyszła zerowa z gramatyki, bo żadnego z czterech znaków nie brał przedtem terminal.
Nad prozą, dla której to weszło, zakupu nie mierzy żadna figura i mierzyć nie będzie:
byłaby należna przeliczenia po każdym commicie dotykającym tekstu
([CLAUDE.md](../CLAUDE.md#checks)),
a nawias nie ma nad README ani jednego zdania do wzięcia,
bo ten plik pisze odsyłacz odnośnikiem, a nie w nawiasie.

Rzeczownik odczasownikowy zszedł z tej listy cały:
cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew,
a zakupem jest sześćdziesiąt jeden zdań Składnicy i dwadzieścia zdań ustawy
([subset.md](subset.md#rzeczownik-odczasownikowy-zmierzono-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego)).
Zero po stronie ceny wychodzi tu z tego, co jest jednym czytaniem:
`czytanie` jest u Morfeusza i rzeczownikiem, i formą odczasownikową,
a dwa wyprowadzenia jednego kształtu są jednym czytaniem,
więc zdanie już przyjęte nie ma jak stracić jednoznaczności na tej głowie.
Nad prozą tego repozytorium nie kupuje ani jednego zdania,
tak samo jak dopisania przed nim,
za to zdejmuje z listy form bez licencji nad nią całą swoją klasę,
i kolejkę nad tym plikiem prowadzi odtąd cząstka.
Pary do przelicznika niżej to dopisanie nie dokłada,
bo obietnicą jest wiersz `ger` liczony wtedy, gdy konstrukcji jeszcze nie ma,
a tabeli, która ten wiersz trzyma, nikt tu od tamtej pory nie przeliczył.

Tryb przypuszczający zszedł z tej listy w połowie:
weszła cząstka przy czasowniku, a spójniki, które tego trybu żądają, zostały
([subset.md](subset.md#tryb-przypuszczający-jest-cząstką-przy-czasowniku-a-nie-cechą-zdania)).
Kupuje kilkanaście zdań Składnicy i pojedyncze zdania tej prozy,
a jednoznaczności nie odbiera ani jednemu zdaniu w żadnym z tych dwóch korpusów.
Cechę trybu, po której wracają tamte spójniki, trzyma [TODO.md](../TODO.md).

Predykatyw na tej liście nie stał i wszedł prosto z kolejki blokerów,
z wiersza `pred`, którego olski nie ruszał dotąd wcale
([subset.md](subset.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika)).
Kupuje kilkadziesiąt zdań Składnicy i kilka zdań tej prozy przy zerowej cenie
w czytaniach, a wiersz, z którego wchodzi, prowadzi `to`,
czyli łącznik, którego lista lematów nie bierze:
połowa tamtego wiersza zostaje przez to po jego stronie.

Myślnik dołożył interpunkcji zdaniowej trzeci znak rozdzielający
i jest z tych trzech najskromniejszy: nad bankiem drzew nie rusza ani jednego
werdyktu, a nad tą prozą kupuje pojedyncze zdania
([subset.md](subset.md#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego)).
Zakupem jest przy tym coś, czego żadna z tych dwóch liczb nie liczy:
znak ten schodzi z listy form bez licencji nad tą prozą,
więc dopiero teraz widać, czego brakuje zdaniom, które go niosą.
Parę myślników trzyma [TODO.md](../TODO.md).

Nad samym README żadne z tych trzech dopisań nie rusza ani jednego werdyktu,
tak samo jak dopisania przed nimi.
Myślnika ten plik nie pisze ani razu,
a zdania, które niosą dwie pozostałe konstrukcje, stoją w nim także na czym innym.

Zmierzone są tym samym cztery wiersze tej kolejki: `num`, `praet`, `qub` i `adv`.
Trzy pierwsze oddały jedną piątą albo jedną czwartą tego, co obiecywały,
a `adv` niemal jedną trzecią,
więc przelicznik wychodzi trzy- do pięciokrotnego i żaden pomiar z niego nie wypadł.
Każda z tych par jest przy tym wzięta nad gramatyką z chwili, w której konstrukcja wchodziła,
bo obietnicą jest wiersz kolejki liczony wtedy, gdy konstrukcji jeszcze nie ma,
i dlatego pary z siebie nie wynikają:
dopisanie kolejnej konstrukcji zmienia i wiersz, i to, ile z niego zostaje do wzięcia.
Cztery pary to zresztą cztery, a nie rozkład,
więc kolejność w kolejce dalej rozstrzyga się pomiarem, a nie tym przelicznikiem.

Piątą parę zmierzył [etap 4](#etap-4-zdanie-złożone) i wypadła ona poza ten przelicznik:
wiersz `comp` obiecywał 567 zdań, a okolicznik wyrażony zdaniem oddał z niego
niecałą dziesiątą część.
Wiersz ten liczy jednak trzy konstrukcje naraz — zdanie z `że`, które gramatyka ma,
spójniki trybu przypuszczającego, których nie bierze, i okolicznik, który wszedł —
i tym różni się od tamtych czterech, z których każdy stał za jedną.
Obietnicą wiersza jest więc tyle, ile konstrukcji on liczy,
a tego kolejka o sobie nie mówi i mówić nie może:
nazywa ona część mowy, na której analiza stanęła, a nie konstrukcję, której zabrakło.

Została po nim jedna pozycja przysłówka, której olski nie ma, i nie jest to zdanie odrzucone:
przysłówek przed drugim przysłówkiem wychodzi jednym czytaniem, w którym oba określają zdanie.
Trzeci gospodarz jest tym, co ją zdejmuje, i [TODO.md](../TODO.md) trzyma pytanie,
czy wraca on z tą samą ceną co drugi.

**Wyjście:** lista w [subset.md](subset.md#what-it-does-not-cover-yet) jest pusta,
bo etap jest ostatnim, który ma z niej co brać,
a tabele w [corpus.md](corpus.md) są przeliczone tym, co ją opróżniło.

## Czego ta numeracja nie obejmuje

Przestawiania — czyli konstytuentu nieciągłego, jak w `Jakie Jan czyta książki?` —
żaden etap nie dopisuje, bo olski go nie wpuszcza.
Jest to jedyne miejsce, w którym krzywa kosztu skacze o wykładnik,
i rozstrzygnął je pomiar, a co on pokazał, mówi
[design-notes.md](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze).

Etapem to nie jest, bo [kierunek](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę) mówi,
co ma zajść nad zdaniem, a nie czym ma być wyprowadzone.
Formalizm zostaje więc ceną płaconą tam, gdzie któryś etap jej zażąda,
a nie pozycją, którą się planuje osobno.

Warstwy rozstrzygającej wieloznaczność za parserem też żaden etap nie dopisuje,
i z powodu przeciwnego niż przy przestawianiu:
tamto olski wyklucza, a to jest tym, co olski oddaje czytelnikowi zamiast rozstrzygać.
Ile taka warstwa miałaby do rozstrzygnięcia i za ile,
wycenia [disambiguation.md](disambiguation.md),
a `olski/rozstrzyganie.py` jest jej zalążkiem stojącym obok werdyktu i nie ruszającym go.

Wykluczenie dotyczy przy tym rankingu, a nie każdej odpowiedzi takiej warstwy,
a granicę między jednym a drugim wyznacza
[hipoteza tamtego dokumentu](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza).
Frazy przyimkowej, której rzeczownik żąda swoim schematem,
nie rozstrzyga maszyna za parserem, tylko kolumna `olski/leksykon.txt`,
którą wypisuje `olski/walenty.py`,
czyli generator zbudowany na [etapie 2](#etap-2-walencja)
([disambiguation.md](disambiguation.md#leksykon-rozstrzyga-część-i-rozstrzyga-ją-deterministycznie)).
Odpowiedź wyczytana ze słownika nie potrzebuje więc etapu i etapem nie jest.

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
z drzewa napisanego w kategoriach `olski.skład.składnia`,
a pokazuje to polecenie, które jedno z drugim porównuje.

### Etap 0: skład, który stoi

Drzewo kategorii dziedziny, linearyzacja licząca zgodność
i morfologia wzięta z Morfeusza czytanego w drugą stronę.

**Wyjście:** drzewo złożone z konstruktorów wypuszcza polskie zdanie,
a forma, której słownik nie ma, zgłasza się wyjątkiem, zamiast zostać zgadnięta.
Zaliczone, zob. `olski/skład/` oraz [sklad.md](sklad.md).

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
`Jaki` w `olski/skład/składnia.py` stawia przymiotnik przed rzeczownikiem zawsze,
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
a `Robi` w `olski/skład/składnia.py` pyta o jeden lemat, bo tyle stoi w drzewie.
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
Zaliczone, zob. `olski/walencja.py` oraz `PozaRamą` w `olski/skład/składnia.py`.

### Etap 3: lemat nie wskazuje formy

`odmień` w `olski/skład/morfologia.py` bierze pierwszą z form, które żądaniu odpowiadają,
a odpowiada ich kilka z trzech różnych powodów, i tylko trzeci jest wyborem.

Pierwszym jest kwalifikator, którym słownik odsyła formę poza ten rejestr,
do dawnej polszczyzny albo do potocznej.
Kryterium na tę klasę stoi w danych i czyta je `POZA_REJESTREM` w tym samym pliku,
wraz z podziałem, którego ta klasa żąda:
nazwa dziedziny formy poza rejestr nie odsyła, więc `oczy` zostają, a `któren` nie.
Drugim jest leksem, którego lemat nie wskazuje,
bo jednym napisem odmieniają się dwie rzeczy o różnej odmianie.
Kryterium na tę klasę nie stoi w danych, bo rozstrzyga o nim autor,
więc stoi w `olski/skład/leksemy.py`, czyli w nazwach wybranych nad identyfikatorami,
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
w `olski/skład/morfologia.py`, wraz z
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
oraz treść czyjegoś sądu stoją już w `olski/skład/składnia.py`.

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

Etapem nie jest także warstwa nad zdaniem, czyli `olski/skład/opowieść.py`,
choć stoi i choć wypuszcza czas przeszły oraz opuszczony podmiot.
Jest tak dlatego, że numeracja tego toru liczy to, czego brakuje jednemu zdaniu,
a te dwie rzeczy są własnościami tekstu i żadne zdanie ich w sobie nie ma:
zdanie nie wie, kiedy to było, ani o kim mowa była przed chwilą.
Wywód trzyma
[sklad.md](sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie).

Etapem nie jest wreszcie `olski/skład/makieta.py`, czyli tekst do makiety losowany z drzew,
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

Wykrywacza wzorców prozy, którego żąda [cel](#cele), wycofanie to nie odwraca,
a czym się różni od tamtego zestawu reguł, mówi tamta sekcja.

Życzenie, które ten tor niósł obok siebie, wycofania nie dotyczy,
bo nie było etapem i nie było linterem:
o dobrą polską prozę z modelu pyta [fiction.md](fiction.md),
a co z niej dało się mierzyć, mówi [linter.md](linter.md#and-fiction).
