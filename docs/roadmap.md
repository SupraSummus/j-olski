# Roadmap

Uporządkowanie, a nie harmonogram.
Dat tu nie ma, bo nikt na żaden etap nie czeka,
a plan z datami zamienia tę robotę w pracę.

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

Linter stylu dla polskiej dokumentacji technicznej stał obok, na torze opcjonalnym.
Jego pakiet reguł jest wycofany, o czym [niżej](#wycofany-jest-pakiet-reguł).
Sam linter został celem.
[Lista celów](#cele) nazywa go wykrywaczem wzorców prozy.
Dwa odwrócenia prowadzą do tego stanu i żadne nie ma wracać przez przeoczenie:
linter stał tu najpierw jako cel, a gramatyka jako tor obok niego,
a potem odwrotnie.

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
Zestaw reguł chodzący po tym samym tekście został zmierzony i wycofany
([niżej](#wycofany-jest-pakiet-reguł)).

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
([CLAUDE.md](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)).
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
i cztery z tych sześciu są tamtą naprawą.
Pokrycie wyszło więc skutkiem, dokładnie tak, jak ten kierunek mówi,
że wyjdzie.

Zaimki `kto` i `co` są pierwszym dopisaniem, po którym pokrycie spadło,
i mówią o tym kierunku to, czego tamten przykład nie mówi
([subset.md](subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
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

## Kolejka blokerów odsiewa, a kolejność dopisań ustala tekst

Kolejka blokerów nazywa kandydatów i tyle o niej wiadomo z pomiaru.
Wiersz nazywa część mowy, na której analiza stanęła
([corpus.md](corpus.md#where-the-analyses-stop)),
więc liczy czasem kilka konstrukcji naraz,
a ile z jego obietnicy zostaje po dopisaniu i czym pozycja płaci poza nim,
mierzy [etap 6](#etap-6-reszta-konstrukcji) parami wziętymi po kolei.
Braku, który jest kształtem zdania, a nie formą — szyku, wtrącenia,
członu bez czasownika — kolejka nie nazywa,
bo zdanie staje wtedy na cudzym wierszu albo na tym jednym,
który nie nazywa żadnej konstrukcji
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
a takich pozycji weszło do gramatyki kilka,
wśród nich cztery szyki podmiotu, dopełnienia i czasownika
([wyżej](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).
Zostaje z niej sito.
Wiersz mówi z grubsza, ile pozycja obiecuje w tym rejestrze,
i nie mówi, że jest następna, ani wtedy, gdy stoi na czele.

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
([sklad.md](sklad.md#najpierw-tekst-potem-drzewo-na-końcu-biblioteka)).

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
a wywód o tym trzyma
[swigra.md](swigra.md#którędy-gfjp-wchodzi-do-olskiego).
Kolejka ustawiona nad tym bankiem przenosi to skrzywienie z pomiaru na plan,
gdzie nie zostawia po sobie liczby:
konstrukcja, której Świgra nie rozebrała, nie ma w kolejce ani jednego wiersza,
więc plan z niej nie mówi o niej nic i nie mówi też, że milczy.
Skrzywienie to stoi jednak w obu przebiegach naraz,
więc zgodności, która ubyła, nie podrabia:
czy dopisanie zepsuło rozbiór, który gramatyka miała przedtem,
bank drzew rozstrzyga.
Zgodności przybyłej nie potwierdza tak samo,
bo decyzję zbliżoną do tamtej gramatyki nagrodzi i w różnicy, i w poziomie,
a to jest ta jedna rzecz, o którą nad tym bankiem pytać nie wolno.

## README jest przyrządem pomiarowym

Przebieg nad [README](../README.md) zostaje, bo nic nie kosztuje:
plik stoi po polsku, w rejestrze, o który olskiemu chodzi,
a ściągać nie ma czego, więc ten przebieg wykona każda sesja,
czego o banku drzew ani o ustawach powiedzieć się nie da.
[corpus.md](corpus.md#where-the-analyses-stop) trzyma polecenie
i to, co przebieg mówi dzisiaj.

**Plik jest odtąd pisany pod gramatykę i to zmienia, co przebieg mierzy.**
Zdania omijają w nim konstrukcje, których olski nie wyprowadza
([README](../README.md#konwencje), [CLAUDE.md](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)),
więc pokrycie nad tym plikiem mierzy pisanie tak samo jak gramatykę,
a wydruk nie mówi, które z dwojga je ruszyło.
Jest to ta sama cena, którą płacił cel nad tekstem pisanym u siebie
([wyżej](#tor-gramatyczny-nie-ma-końca)), wzięta świadomie.
Zostaje z przebiegu to, czego przeredagowanie nie podrabia:
werdykt mówi, jakie czytania olski zdaniu daje,
czyli mierzy [kierunek](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę), a nie udział.
O polszczyźnie, której nikt pod olskiego nie pisał,
mówią odtąd bank drzew i ustawy, i tylko one.
Liczby wzięte nad tym plikiem przed przepisaniem trzyma git,
a dzisiejsze drukuje przebieg.

Zdaniem jest tu to, co zamyka kropka, wykrzyknik albo pytajnik.
Nagłówek, pozycja listy i wiersz tabeli
dochodzą do olskiego jako akapity, których nic nie punktuje,
i przebieg liczy je osobno,
bo policzone jako odrzucone mierzyłyby ekstrakcję zamiast podzbioru.
Ten plik nie ma już ani jednej takiej pozycji,
bo lista dokumentów stoi w nim zdaniami.
Co je od zdania odróżnia i jak dużą częścią rejestru są, trzyma
[extraction.md](extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem).

Kolejki form bez licencji ten plik już nie ustawia,
bo odrzuceń została w nim garść i każde stoi na czymś pojedynczym:
na formie żartu z nazwy, na cyfrze, na przytoczonej niezgodności,
na angielskim tytule i na słowie, którym ten plik pyta poza `który`
([pisanie-po-olsku.md](pisanie-po-olsku.md#czego-brakuje-najbardziej)).

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
bo udział skraca też przeredagowany akapit.
Trzecia zasada przychodzi z wycofanego pakietu ([niżej](#wycofany-jest-pakiet-reguł)),
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
Ten cel jest linterem tego repozytorium.
Wycofanego pakietu nie wskrzesza, a różni je populacja:
tamten zestaw reguł strzelał nad cudzą polszczyzną i żądał kalibracji,
której się nie doczekał,
a ten chodzi po tekście, który sami napisaliśmy,
więc trafienia czyta się wszystkie, zamiast progować ich stopę.
Tę różnicę rozkłada na osie
[linter.md](linter.md#cztery-osie-każdej-reguły).
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
taki czytnik wyszedł razem z pakietem reguł i trzyma go git,
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
który robi `poza_rejestrem` w `olski/rejestr.py`,
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
Tego, po co tory są dwa, bo cele wybiera się pod tym,
i ma [własną sekcję](#po-co-tory-są-dwa).
Nie ma też sparsowanej prozy tego repozytorium,
która była pierwszym brzmieniem celu o wykrywaczu i upadła na drugiej zasadzie:
udział zdań wyprowadzonych z naszego tekstu skraca przeredagowany akapit,
a wykrywacz, który ma stać na zerze, skraca tylko poprawione zdanie.

## Etap 0: gramatyka, która stoi

Gramatyka podzbioru nad Morfeuszem 2,
w której zdanie jest olskie dopiero przy jednym odczytaniu,
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
Żądanie to stawia każda konstrukcja z osobna, a konstrukcją obok innych nie jest,
i [corpus.md](corpus.md#what-morphological-ambiguity-costs)
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
`admissible` w `olski/segmentacja.py` wyklucza dziś jedną ich klasę,
czytanie nieodmienne stojące obok czytania z klasy zamkniętej,
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

Jedna klasa ma wycenę i nie ma decyzji.
Orzecznik zgodny bierze u olskiego każdy czasownik,
więc `Trwa akcja protestacyjna.` orzeka `protestacyjna` o akcji,
a zawężenie tej pozycji do leksykonu daje zdań olskich więcej
i zabiera przy tym orzeczenie wtórne, czyli zwyczajną polszczyznę
([subset.md](subset.md#zawężenie-orzecznika-zgodnego-wyceniono-i-decyzji-nie-ma)).

Nazwiskowe czytanie rzeczownika na czele zdania do tego etapu nie należy:
para lematów jednej formy nie jest dwoma czytaniami
([subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie)),
a kryterium pisane pod tę klasę zmierzono i ono nie stoi
([subset.md](subset.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi)).

Ile ta klasa waży, jest przeczytane ręką:
nad bankiem drzew, nad rejestrem ustaw i nad prozą tego repozytorium
opiera się na takim czytaniu kilka procent zdań przyjętych
([subset.md](subset.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)).
Część tej klasy nie należy przy tym do tego etapu.
Gdzie czytanie czytelnika jest w słowniku, a nie licencjonuje go żadna produkcja —
zaimek zwrotny, liczebnik za rzeczownikiem — wykluczenie zamienia zdanie przyjęte
na odrzucone, czyli werdykt nieprawdziwy na uczciwy,
a czytanie właściwe wraca do zdania dopiero z pozycją,
czyli z [etapem 6](#etap-6-reszta-konstrukcji).

Etap stoi między tamtymi a konstrukcjami,
bo wieloznaczność zawęża, a pokrycia nie podnosi,
i jest pierwszym, przy którym nie wiadomo, czy kryterium w ogóle istnieje.
Wykluczenie zbyt szerokie zabiera zwyczajne polskie słowa,
co tamten dokument pokazuje na `jury` i `menu`,
więc odpowiedzią bywa tu decyzja, że klasy się nie da wykluczyć.
Każde kryterium, jakie na te klasy zaproponowano, jest taką odpowiedzią,
a cenę każdego trzyma
[subset.md](subset.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi).

**Wyjście:** klasa rozstrzygnięta kryterium
albo zapisaną decyzją, że kryterium nie ma,
a kryterium przyjęte zmierzone na Składnicy tym, ile zdań zabiera.

## Etap 4: zdanie złożone

Podrzędność z `że` i `który`, obok koordynacji przecinkiem, która już stoi.
Koordynacja weszła osobno, bo osobno się ją zmierzyło:
nie odbiera nad Składnicą ani jednego zdania już przyjętego
i dokłada dwadzieścia kilka nowych.
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
wywód trzyma
[subset.md](subset.md#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja).
Pokrycie nad README nie ruszyło się o ani jedno zdanie
i mówi to o pomiarze nad tym plikiem więcej niż o podrzędności:
zdania tego pliku, które na podrzędności stały, stoją także na przysłówku,
na dwukropku i na liczebniku,
czego [tamten przebieg](corpus.md#where-the-analyses-stop) nie przewidział inaczej,
niż mówiąc, że większość zdań odrzuconych niesie dwie klasy albo więcej.

Dwie pozycje podrzędności, których gramatyce brakowało,
odsłoniło właśnie to dopisanie: okolicznik wyrażony zdaniem, przed swoim zdaniem
i za nim, oraz kopuła opuszczona.
Weszły razem z interpunkcją zdaniową — dwukropkiem, średnikiem i przecinkiem
przed spójnikiem — z pytaniem, z grupą wysuniętą pod przyimkiem i bez niego,
ze spójnikiem, który cząstkę trybu niesie sam,
oraz z podmiotem opuszczonym w zdaniu z wysuniętym dopełnieniem.
Wywód i cenę każdej z tych konstrukcji trzyma jej sekcja w
[subset.md](subset.md), a przebiegi, którymi je policzono, są w gicie.
Lista pozycji tego etapu jest przez to pusta,
a otwarte zostaje samo jego wyjście drugie, czyli pokrycie nad README.

Pomiary tego etapu mówią przy tym coś o samym planowaniu.

Zero po stronie ceny bywa własnością gramatyki, a nie wynikiem przebiegu.
Dwukropka ani średnika nie brała przedtem żadna produkcja,
więc zdanie z takim znakiem nie miało czytania,
z którego dałoby się je wytrącić.
Cena zerowa nie mówi wtedy, że konstrukcja niczego nie psuje,
tylko że nie miała czego zepsuć.

Zakup bywa poza obiema walutami, którymi mierzy
[kierunek](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).
Przecinek przed spójnikiem nie kupowałby prawie nic,
dopóki `a` czyta się jako przyimek rządzący mianownikiem,
a warunek, który to czytanie odbiera, sam odbiera zdanie README —
i to samo zdanie wraca z tą parą, z trzema czytaniami w miejsce trzech,
tylko że prawdziwymi
([subset.md](subset.md#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)).
Para ta kupuje więc prawdę o zdaniu,
a prawdy nie liczy ani pokrycie, ani lista zdań wieloznacznych.

Zakup liczony pojedynczymi zdaniami na korpus jest odczytem o rejestrze,
a nie o produkcjach.
Pytań jest w Składnicy jedno na piętnaście zdań,
a otwiera je `czy`, `kto`, `co`, `jak` albo `dlaczego`,
czyli słowa żądające każde innego kształtu niż grupa imienna na czole zdania,
więc kolejka po tym dopisaniu jest kolejką kształtów pytania,
a nie listą lematów do dopisania obok jednego, który olski ma.
Tak samo `o którym mowa` obiecuje w rejestrze ustaw 851 wystąpień,
a oddaje przeszło o dwa rzędy wielkości mniej,
bo prawodawca pisze ten zwrot razem z adresem przepisu,
a cyfry olski nie bierze
([subset.md](subset.md#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii)).
Rejestr rozstrzyga zarazem, którą pozycję konstrukcji pomiar w ogóle zobaczy.
Grupa wysunięta ma dwie, pod przyimkiem i bez niego,
a rozporządzenie odpowiada tylko na pierwszą, siedem ustaw tylko na drugą,
a bank drzew na obie, choć kształt grupy jest w obu ten sam.

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
Zaliczone: odmianę takiego słowa deklaruje `olski.toml`,
wskazując leksem, wedle którego się ono odmienia, wraz z formą, którą ten leksem
ma wydać, zob.
[subset.md](subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma).
Etap kupił mechanizm, a nie listę słów, i widać to po cenie:
ani jednej formy tego leksykonu słownik nie czyta,
więc zdanie, które się wyprowadza, nie ma jak stracić przez niego jednoznaczności.
Zdania przyjętego nie kupuje przy tym nad README ani jednego,
tak samo jak dopisania przed nim,
a klasa, która stała w tamtej kolejce na czele, z niej schodzi.
Słowo bez wpisu wraca dalej jako `ign`,
i jest to odtąd brak wiersza w jednym pliku, a nie brak pozycji w gramatyce.

## Etap 6: reszta konstrukcji

Etap ma opróżnić listę tego,
[czego olski nie bierze](subset.md#what-it-does-not-cover-yet).
Konstrukcje, które olski już bierze, mają wywód i cenę
w swoich sekcjach [subset.md](subset.md#what-the-grammar-covers),
a przebiegi, którymi je policzono, są w gicie.
Kolejka ze Składnicy stawia najwyżej jedną pozycję tej listy,
czyli liczebnik pisany cyfrą.
Co dopisanie konstrukcji robi z wierszami tej kolejki, opisuje
[corpus.md](corpus.md#where-the-analyses-stop).

Cyfra jest przy tym osobną pozycją, a nie resztą liczebnika:
zdejmie ją warstwa nad morfologią, a nie produkcja,
bo `dig` nie niesie ani przypadka, ani liczby
([subset.md](subset.md#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii)).

Lista ta ma trzy źródła i pierwszym z nich nie jest kolejka.
Człon bez czasownika wtrącony w środek zdania
i nazwa postawiona przy rzeczowniku bez spójnika weszły na nią z przebiegu nad prozą,
która ten rejestr pisze, czyli jako zdania odrzucone, a nie jako wiersz częstości.
Trzecim jest tor składu: wysunięty narzędnik stoi na tej liście dlatego,
że legenda o bazyliszku go wypisuje, a gramatyka go nie bierze
([subset.md](subset.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Wszystkie trzy pozycje są przy tym kształtem, a nie formą,
więc kolejka blokerów nie widzi ich w ogóle
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)),
i tym różnią się te dwa źródła od tamtego: pokazują pozycje, których tamto nie stawia.

Kolejkę tę czyta się przy tym dwojako i tylko jedno z dwóch czytań stawia dziś
pozycje na tej liście.
Po formie widać zdanie, na którym analiza stanęła.
Po części mowy widać konstrukcję, ale tylko tam, gdzie cały wiersz niesie ją jedną —
tak stoją `pcon` oraz `siebie` — bo wiersz taki jak `interp` albo `part`
grupuje po kilka i dopiero czytanie form mówi, o którą idzie.
Czytanie po części mowy nie stawia na tej liście nic,
bo wpuszczone są wszystkie trzy pozycje, które nazwało:
[imiesłów przysłówkowy](subset.md#imiesłów-przysłówkowy-stoi-tam-gdzie-okolicznik-wyrażony-zdaniem),
[zaimek `siebie`](subset.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym)
oraz [czas przyszły predykatywu](subset.md#forma-bedzie-składa-czas-przyszły-także-z-predykatywem),
czyli resztka wiersza, którego czas przyszły nie opróżnił do końca.
Wiersze tych trzech w kolejce zostają
([corpus.md](corpus.md#where-the-analyses-stop)),
i mówi to o niej to samo, co wiersz `comp` wyżej:
nazywa ona część mowy, a nie konstrukcję.

Trzy konstrukcje weszły przy tym poza wszystkimi tymi źródłami.
Zaimek dzierżawczy postawiła sesja pisząca pod tę gramatykę zdanie po zdaniu
([pisanie-po-olsku.md](pisanie-po-olsku.md)),
podmiot opuszczony postawił pomiar luki, który kupował go mimochodem
([design-notes.md](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)),
a miejsce na okolicznik po czasowniku postawiło zawężenie stojące obok reguły,
która te miejsca wylicza
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Żadnej z tych trzech kolejka blokerów nie widzi,
bo każda forma tych zdań licencję ma, a odrzucenie stoi na strukturze.

Pozycje tej listy wychodzą na koniec dlatego, że żadna nie żąda niczego
od produkcji pisanych po niej,
więc [koszt przepisywania](#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)
ich nie porządkuje, a między sobą rozstrzyga je sama cena.
Dwie kolejki, które ją wyceniają, nie zgadzają się co do kolejności,
i jest to wynik pomiaru, a nie usterka w którejś z nich.

Mierzy się przy tym każde dopisanie z osobna, a nie samą listę na końcu,
bo kolejka wycenia pozycję, zanim się ją napisze:
zysk wypada na ułamek tego, co obiecywała, a cena bywa poza nią.
Czas przeszły stał w tej kolejce pierwszy, a kolejka nazywała go
najtańszym dużym zyskiem;
zapłacił on rodzajem wchodzącym do każdego szyku zdania
([subset.md](subset.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku)),
czego kolejka nie widziała i widzieć nie mogła.

Zmierzone są tym samym wiersze tej kolejki:
`num`, `praet`, `qub`, `adv`, `imps` i `bedzie`.
Trzy pierwsze oddały jedną piątą albo jedną czwartą tego, co obiecywały,
a `adv` oraz `imps` niemal jedną trzecią,
więc przelicznik wychodzi trzy- do pięciokrotnego.
Wypadł z niego dopiero `bedzie` i wypadł w drugą stronę niż `comp` niżej:
czas przyszły oddał więcej, niż przelicznik obiecywał
([subset.md](subset.md#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony)).
Żadne z tych dopisań nie rusza osobno pokrycia nad README.
Każda z tych par jest przy tym wzięta nad gramatyką z chwili, w której konstrukcja wchodziła,
bo obietnicą jest wiersz kolejki liczony wtedy, gdy konstrukcji jeszcze nie ma,
i dlatego pary z siebie nie wynikają:
dopisanie kolejnej konstrukcji zmienia i wiersz, i to, ile z niego zostaje do wzięcia.
Par tych jest garść, a nie rozkład,
więc kolejność w kolejce dalej rozstrzyga się pomiarem, a nie tym przelicznikiem.

Jeszcze jedną parę zmierzył [etap 4](#etap-4-zdanie-złożone)
i wypadła ona poza ten przelicznik:
wiersz `comp` obiecywał 567 zdań, a okolicznik wyrażony zdaniem oddał z niego
niecałą dziesiątą część.
Wiersz ten liczy jednak trzy konstrukcje naraz — zdanie z `że`, okolicznik, który wszedł,
i spójniki trybu przypuszczającego, które weszły po nim —
i tym różni się od tamtych, z których każdy stał za jedną.
Obietnicą wiersza jest więc tyle, ile konstrukcji on liczy,
a tego kolejka o sobie nie mówi i mówić nie może:
nazywa ona część mowy, na której analiza stanęła, a nie konstrukcję, której zabrakło.

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
którą wypisuje `harness/walenty.py`,
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
Reguły przeliczania tego rodzaju trzyma [CLAUDE.md](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje),
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
([subset.md](subset.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)).

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
Kryterium na tę klasę stoi w danych i czyta je `POZA_REJESTREM` w `olski/rejestr.py`,
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
Pierwsze dwa z tych trzech stoją, zob. `POZA_REJESTREM` w `olski/rejestr.py`
oraz `WieleLeksemów` w `olski/skład/morfologia.py`, wraz z
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
w pakiecie, który wyszedł razem z silnikiem reguł.

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

## Wycofany jest pakiet reguł

Silnik reguł, pakiet typograficzny i polecenie, które je uruchamiało,
są usunięte, a razem z nimi cała analiza, która schodziła do znaku.
Linter nie jest wycofany.
Nazywa go [lista celów](#cele) wyżej.
Decyzję i jej powody trzyma [linter.md](linter.md#co-zamknęło-pakiet-reguł),
a cenę, przy której zapadła, [firing-rates.md](firing-rates.md).

Plan tego toru stał tutaj i git go trzyma,
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
Kształt jest jedną z [czterech osi](linter.md#cztery-osie-każdej-reguły).
Wycofanie dotyczy trzech z nich.

Życzenie, które ten tor niósł obok siebie, wycofania nie dotyczy,
bo nie było etapem i nie było linterem:
o dobrą polską prozę z modelu pyta [fiction.md](fiction.md),
a co z niej dało się mierzyć, mówi [linter.md](linter.md#and-fiction).
