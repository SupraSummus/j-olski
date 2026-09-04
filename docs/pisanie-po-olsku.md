# Pisanie po olsku: feedback z fotela użytkownika

Dokument zbiera to, co widać z fotela użytkownika:
kogoś, kto olskiego używa przy tekście, zdanie po zdaniu,
zamiast mierzyć gramatykę nad korpusem.

Fotele są dwa i żądają rzeczy przeciwnych.
Kto pisze, nie chce przepisywać niczego:
zdanie ma przechodzić takie, jakie je napisał.
Kto gramatykę rozwija, chce odwrotnie —
żeby pisano wewnątrz tego, co gramatyka już ma,
bo konstrukcja dopisana dokłada czytania każdemu zdaniu, które ją niesie,
a zdanie o dwóch czytaniach olski odrzuca
([roles.md](roles.md#autor-produkcji)).
Osobno żadnego z tych dwóch żądań przyjąć nie można.
Autor, który pisze pod gramatykę, płaci za każde odrzucenie sam
i kończy z rejestrem, którego nikt nie wybrał.
Kto gramatyce dopisuje każdy brak zgłoszony mu przez jeden dokument,
wpuszcza w końcu napis, którego polszczyzna nie ma,
a wtedy milczenie werdyktu niczego już nie obiecuje.

Oba fotele obsadza jedna osoba i to ona wymusza równowagę
([roles.md](roles.md#rola-jest-postawą-nie-osobą)):
kto zdanie przepisuje, sam potem wycenia produkcję, która by je wpuściła,
więc kosztu nie ma komu podrzucić.
Każde zdanie ta osoba rozstrzyga przy tym osobno,
a rozstrzyga je tak, że rusza obie strony naraz
i zatrzymuje się w [punkcie kompromisu](#ruchy-są-dwa-i-spotykają-się-w-punkcie-kompromisu).

Planem to nie jest.
Właścicielem ruchu jest `todo/`,
kolejności [`roadmap.md`](roadmap.md),
a ceny wpuszczenia konstrukcji
[`subset.md`](subset.md#what-the-grammar-covers);
tu stoi tylko materiał, którego te trzy dokumenty nie miały skąd wziąć.

## Ruchy są dwa i spotykają się w punkcie kompromisu

Odrzucone zdanie rusza dwie rzeczy naraz i obie wolno ruszyć.
Autor przepisuje zdanie tak, żeby olski je wziął.
Developer dopisuje produkcję tak, żeby olski wziął zdanie bez zmiany.
Ruchy te nie wykluczają się i najczęściej wchodzą razem:
autor skraca zdanie, nowy napis dalej nie przechodzi,
a developer dopisuje pozycję, której ten nowy napis żąda.

**Punkt spotkania nie leży w połowie i nie ma leżeć.**
Wybiera go za każdym razem to, co która strona traci.
Autor traci wtedy, gdy zdanie po przepisaniu mówi mniej albo mówi gorzej;
gramatyka traci wtedy, gdy produkcja dokłada czytanie każdemu zdaniu,
które ją niesie ([roles.md](roles.md#autor-produkcji)).
Gdzie autor traci mało, a produkcja kosztowałaby dużo, rusza się zdanie.
Gdzie zdanie po przepisaniu byłoby gorszą polszczyzną, rusza się gramatyka.
Obie te straty widzi jedna osoba, i po to
[fotele obsadza jedna osoba](roles.md#rola-jest-postawą-nie-osobą).

**Jedna granica stoi ponad tym wyborem: czy polszczyzna ma ten napis.**
Napisu, którego polszczyzna nie ma, gramatyka nie bierze za żadną cenę,
bo obietnicą podzbioru jest, że każde zdanie olskiego jest zdaniem polskim,
a produkcja wpuszczająca taki napis odbiera tę obietnicę wszystkim zdaniom naraz.
Tam ruch jest jeden i robi go autor, a dostaje za to poprawiony tekst
([niżej](#odrzucenie-bywa-poprawką)).
Poza tą granicą wybór jest otwarty i rozstrzyga go cena obu stron.

Tego pytania nie policzy żaden przebieg.
Kolejka mówi, ile razy analiza stanęła na danej formie,
a czy stanęła na polszczyźnie, czy na literówce, widać dopiero po przeczytaniu zdania.
Dlatego z tego fotela wychodzi dokument, a nie druga tabela.

## Kto płaci za odrzucone zdanie

Rachunki są trzy i mówią, ile która strona ma do stracenia
w [punkcie kompromisu](#ruchy-są-dwa-i-spotykają-się-w-punkcie-kompromisu).

**Za napis, którego polszczyzna nie ma, płaci autor.**
Jest to ta jedna granica, za którą wyboru nie ma.

**Za napis, który polszczyzna ma i ten rejestr pisze, płaci głównie gramatyka.**
Autor zapłaciłby tu najwięcej, bo przepisanie takiego zdania znaczy napisanie go
gorzej pod parser, a podzbiór, w którym nie da się pisać tego,
co ten rejestr mówi, mierzy sam siebie zamiast polszczyzny.
Cenę produkcji liczy autor przed dopisaniem ([README](../README.md#kierunek)).
Zdania wolno przy tym dotknąć, gdy nic ono na tym nie traci:
zdanie długie ma kilka zatrzymań naraz i rozbite na dwa
zdejmuje developerowi część roboty, nie mówiąc przez to mniej.

**Za napis, który polszczyzna ma, a ten rejestr pisze rzadko, płaci autor.**
Produkcja czeka wtedy na kolejce, a nie na tę jedną sesję:
o niej mówi cała [kolejka blokerów](corpus.md#where-the-analyses-stop).
Rozstrzyga o niej cena, czyli liczba zdań, które konstrukcja kupuje,
i po tej liczbie tamta kolejka jest ułożona, a nie po dolegliwości.

## Odrzucenie bywa poprawką

Formą, na której analiza nad tą prozą staje najczęściej, jest spójnik `i`,
a częstą przyczyną tych zatrzymań jest przecinek postawiony przed `i`,
którego nie stawia tu żadna zasada.
Polska interpunkcja stawia go przed `i` tylko tam,
gdzie domyka on zdanie podrzędne albo wtrącenie,
i olski ma dokładnie te dwa miejsca
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
W `architecture.md` pięć zdań miało ten przecinek bez żadnego z tych dwóch powodów.

Płaci tu autor i ten rachunek się zwraca.
Zdania te były niepoprawne przed olskim i nikt tego nie zauważył:
reguły prozy o interpunkcji nie mówią,
`markdownlint` czyta Markdown, a nie polszczyznę,
a `tests/test_docs.py` sprawdza nazwy plików i sekcji.
O tym przecinku powiedział w tym repozytorium tylko werdykt `rejected`.

Odpowiada to na zarzut, że
[biała lista każe pisać pod parser](linter.md#it-dissolves-the-habitability-problem).
Każe wtedy, gdy się myli, a kiedy się nie myli, każe pisać poprawną polszczyzną.
Który z tych dwóch wypadków zachodzi, rozstrzyga czytelnik i po to ten fotel jest.

Przecinek przed `i` stoi w tej prozie setki razy,
a które z tych miejsc nie domykają niczego, widać dopiero po przeczytaniu każdego;
ruch trzyma `todo/`.

## Zasłanianie działa w obie strony

Pozycja dopisana do gramatyki nie rusza liczby nad zdaniem długim.
Zdanie o dwudziestu wyrazach ma kilka zatrzymań naraz,
a wyprowadza się dopiero wtedy, gdy zamkną się wszystkie,
więc dopisana pozycja zdejmuje jedno z nich
i zostawia zdanie odrzucone, tylko dalej.
Krzywą pokrycia po długości zdania trzyma
[corpus.md](corpus.md#the-measurement) i mówi ona to samo od drugiej strony:
pokrycie spada z urwiska między dziesiątym a dwudziestym tokenem.

Poprawka autora zasłania się tak samo.
Z pięciu poprawionych przecinków dwa wypuściły swoje zdanie z odrzuconych,
a trzy przesunęły zatrzymanie w prawo i zostawiły zdanie tam, gdzie stało,
bo za przecinkiem czekał w każdym z nich jeszcze jeden brak.
Nagroda przychodzi więc za ostatni brak, a nie za każdy,
i nie zależy od tego, kto go zdjął.

Zasłanianie widać najlepiej na pozycji, którą zmierzono z obu stron naraz.
Dopełnienie w celowniku i w dopełniaczu jest taką pozycją.
Nad bankiem drzew kupuje przeszło sto zdań
([walencja.md](walencja.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)),
a nad prozą tego repozytorium podnosi liczbę zdań przyjętych o pojedyncze sztuki,
choć z tego fotela była brakiem najdroższym.
Zdania tej prozy mają po kilka zatrzymań naraz,
więc pozycja zdejmuje jedno zatrzymanie i rzadko kiedy domyka zdanie.

Rada dla piszącego wychodzi z tego jedna:
liczba pokrycia nad własnym dokumentem nie jest sygnałem,
dopóki zdania tego dokumentu są długie.
Sygnałem jest zatrzymanie, bo ono się rusza,
i po to `--zatrzymania` pokazuje je wszystkie nad jednym zdaniem,
a `olski-pokrycie` nad całym plikiem układa je w kolejkę
([corpus.md](corpus.md#the-same-queue-over-prose)).
Nad zdaniem krótkim jest odwrotnie:
jedno zatrzymanie, jedna poprawka i widoczny skutek,
czego doświadcza każdy, kto pisze README
([README](../README.md#konwencje)).
Która proza gdzie leży, drukuje krzywa nad plikiem.

To samo zasłanianie widać o szczebel wyżej, na cenie pozycji.
Sonda różnicowa wycenia pozycję, zdejmując ją z gramatyki,
więc wycenia ją wobec wszystkiego, co w gramatyce zostaje,
a pozycja wpuszczona samotnie mierzy się przez to blisko zera,
choć obok pozycji, o którą jej zdania i tak się potykają, kupuje wielokrotnie więcej
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
Cena pozycji nie jest przez to liczbą, którą raz się zapisuje,
a dwie pozycje wpuszczone razem bywają warte więcej niż z osobna.

## Przebieg po całym dokumencie kupuje zdania szykiem, a nie produkcją

Jedno zdanie poprawia się w minutę, a jeden dokument przechodzi się w jednej sesji,
i te dwie roboty dają różne odpowiedzi.
`architecture.md` przeszedł taką sesję zdanie po zdaniu, oba fotele naraz.
Czytanie miało przed nią niespełna trzy zdania z dziesięciu, a po niej ma prawie każde;
przyjętych była garść, a jest ich kilkadziesiąt.
Liczbę dzisiejszą drukuje `olski.check` nad tym plikiem.

Ruch, który kupił najwięcej, jest jeden i nie jest to wymiana słowa:
zdanie długie rozbite na dwa albo trzy krótkie.
Odpowiada to [zasłanianiu](#zasłanianie-działa-w-obie-strony) od drugiej strony.
Zatrzymań w zdaniu długim jest kilka i nagroda przychodzi za ostatnie,
a rozbicie zdania dzieli te zatrzymania między dwa zdania,
więc każda połowa domyka się osobno i osobno wchodzi do liczby.

Trzy ruchy dalsze kupują mniej, a każdy ma swoją cenę po stronie prozy.
Rzeczownik powtórzony w miejscu elipsy głowy wydłuża zdanie
i to jest cała jego cena.
Słowo wymienione na takie, które Morfeusz czyta jak trzeba — `niekiedy` za `czasem`,
`identyczne` za `te same` — rusza rejestr, a nie treść.
Nazwa funkcji zdjęta na rzecz nazwy modułu nie kosztuje nic
i jest to jedyny z czterech ruchów, którego
reguły prozy chciały i bez olskiego.

Zdania odrzucone zostają i zostać muszą,
a granica przebiega przez nie dwiema drogami.
Jedne niosą po kilka zatrzymań naraz i rozbite na krótsze straciłyby wywód.
Drugie przeszłyby, gdyby powiedzieć w nich mniej, i te nazywają granicę wprost.
Zdanie o warstwie pierwszej, drugiej i piątej żąda liczby mnogiej,
a ciągu rozdzielnego przydawek gramatyka nie ma
i wpis o nim trzyma `todo/`.
Zdanie o populacji kilka razy większej przechodzi bez `kilka razy`,
tylko że wtedy rzędu wielkości nie mówi,
a rząd wielkości jest tu tym, po co ono stoi.
Granicę tę stawia `CLAUDE.md`,
i to ona rozstrzyga, kiedy przebieg po dokumencie się kończy.

## Odrzucenie mówi, na czym stanęło, i mówi to raz

Gdyby odrzucenie miejsca nie nazywało, autorowi zostawałaby bisekcja ręką:
dzieli zdanie na pół, puszcza każdą połowę osobno,
potem wymienia w podejrzanym członie jedno słowo i puszcza znowu.
Na jedno zdanie wychodzi tak kilka do kilkunastu przebiegów,
a wiedza, która z nich zostaje, jest wiedzą o tym jednym zdaniu.
Bisekcja pyta o dwie rzeczy, a olski odpowiada na obie.

Pierwsze pytanie brzmi: który człon tknąć.
Odpowiada na nie nazwane miejsce zatrzymania,
a werdykt nazywa je dwoma zdaniami, bo zatrzymanie na formie
i zdanie, którego nic nie domyka, są dwoma zdarzeniami
([`subset.md`](subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).
Oba te zdania wypisuje flaga `--zatrzymania`,
bo odrzucenie, którego nie zdejmuje jeden znak, znaleziskiem nie jest
i wydruk sam z siebie o nim milczy
([`subset.md`](subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego)),
więc kto pisze pod tę gramatykę, trzyma tę flagę włączoną.

Drugie pytanie brzmi: ile jeszcze.
Jedno zatrzymanie zasłania każde następne,
bo analiza przerywa się na pierwszym i o resztę zdania nie pyta,
więc kto poprawi to jedno miejsce, dostaje zdanie odrzucone drugi raz.
Odpowiada na to ta sama flaga:
pod nią ta sama analiza rusza od nowa za każdym zatrzymaniem,
więc wychodzi z niej zdanie pocięte na kawałki, z których każdy się analizuje,
wraz z formami, na których leżą cięcia.
Liczba cięć mówi, ile miejsc trzeba tknąć, i tyle ta flaga odpowiada.
Wydruk stoi w [README](../README.md#co-działa) razem z zastrzeżeniem o cięciu.

## Skąd bierze się odczytanie, którego autor nie widzi

Werdykt nad zdaniem wieloznacznym nazywa role, w których odczytania się różnią,
a nie mówi, czemu forma może w tej roli stanąć.
`Janek lubi piwo.` dostaje dwa odczytania i w drugim `Janek` jest dopełnieniem,
choć polszczyzna ma tam biernik `Janka`.
Autor czyta wtedy własne zdanie jak pomyłkę parsera i nie ma czym jej sprawdzić.

Odpowiada na to `--morfologia`, czyli wykaz form
wraz z odczytaniami, którymi w tym odczytaniu zdania stać mogą:

```sh
python3 -m olski.check --readings --morfologia -c "Janek lubi piwo."
```

```text
<text>: Janek lubi piwo.
        2 odczytania, różne w rolach: dopełnienie, podmiot
        - podmiot: Janek, dopełnienie: piwo, orzeczenie: lubi
        - podmiot: piwo, dopełnienie: Janek, orzeczenie: lubi
        odczytanie 1:
          „Janek”: Janek subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:f | Janek subst:sg:nom:m1
          „lubi”: lubić fin:sg:ter:imperf
        odczytanie 2:
          „Janek”: Janek subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:f
          „lubi”: lubić fin:sg:ter:imperf
```

Odpowiada odczytanie drugie, czyli to z dopełnieniem `Janek`:
zostaje w nim jedno odczytanie tej formy i jest to rzeczownik żeński
nieodmienny, czyli nazwisko, a nieodmienne niesie wszystkie przypadki naraz.
Biernik jest wśród nich i innego biernika ta forma nie ma,
więc dopełnieniem czyni `Janek` właśnie to jedno odczytanie.
W odczytaniu pierwszym `Janek` jest podmiotem i stoi tam obok mianownika `m1`,
bo podmiot bierze oba.

Wykaz nie wypisuje przy tym odczytań, których to odczytanie zdania nie bierze:
`lubi` ma tu samo `lubić`, choć Morfeusz czyta tę formę również
jako rzeczownik i jako przymiotnik `luby`.
Nie ma też wiersza o formie czytanej jednym sposobem —
`piwo` i kropka — bo o niej wiersz nie mówiłby nic ponad zdanie samo.
Zdanie odrzucone odczytania nie ma, więc odsiać go nie ma czym,
i tam ten sam wykaz wypisuje każde odczytanie każdej formy.

Odczytania nieodmiennego polszczyzna w tym zdaniu nie ma i nikt go nie zdejmuje:
wykluczenie sięga odczytania nieodmiennego stojącego obok czytania z klasy zamkniętej,
a szersze zabrałoby `jury` i `menu`, czyli zwyczajne polskie słowa
([warstwa-leksykalna.md](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).
Autorowi zostaje więc wymiana słowa, a nie przestawienie zdania:
`Janek pije piwo.` jest wieloznaczne tak samo,
a `Chłopiec lubi piwo.` ma jedno odczytanie.
Wykaz mówi mu przy tym, którą formę wymienić,
bo odczytanie z siedmioma przypadkami widać w nim po samym znaczniku.

Pytanie sąsiednie zadaje `--żądania`:
czego czasownik żąda od słowa, które autor postawił w jego pozycji.
Czy to słowo żądanie spełnia, ten wykaz nie mówi
([walencja.md](walencja.md#werdykt-nazywa-żądanie-obsadzonej-pozycji)).

## Kolejka czytana po formie mówi to, czego nie mówi po części mowy

Kolejka blokerów grupuje zatrzymania po części mowy formy
([`olski/pokrycie.py`](../olski/pokrycie.py)).
Nad wierszami otwartymi — `fin`, `subst`, `prep` — mówi to dość,
a nad zamkniętymi zbiera pod jedną nazwą formy żądające każda innej konstrukcji:
wiersz `conj` prowadzą w tym rejestrze `i` oraz `a`,
a pod nimi stoją `czy`, `czyli` i `ani`
([corpus.md](corpus.md#where-the-analyses-stop) trzyma, które wiersze prowadzą).
Ruch nad tym wierszem trzyma `todo/`.

Kolejka policzona po samej formie odpowiada zarazem na pytanie o rachunek.
Forma nazywa słowo, a słowo da się przeczytać:
widać po nim, czy polszczyzna ma napis, w którym ono stoi.
Część mowy tego nie mówi, bo `interp` obejmuje naraz przecinek postawiony źle
i dwukropek, którego gramatyce brakuje.
Kolejkę tę drukuje jedno polecenie nad werdyktami, więc puszcza ją każda sesja
([subset.md](subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).

## Czego brakuje najbardziej

Lista jest ułożona według tego, ile razy pozycja zawróciła zdanie,
a nie według tego, ile by kosztowało wpuszczenie.
Przy każdej pozycji stoi para zdań, z których pierwsze nie ma czytania,
a drugie się wyprowadza, bo różnica między nimi jest tu całą informacją.
O jednoznaczność ta lista nie pyta, bo pyta o pozycję, której w gramatyce nie ma.
Pozycja wpuszczona do gramatyki z tej listy schodzi
i zostaje po niej sekcja w [`subset.md`](subset.md#what-the-grammar-covers).

**Grupa imienna z elipsą głowy.**
`Wszystkie obsadza jedna osoba.` pada, `Wszystkie role obsadza jedna osoba.` przechodzi.
Tak samo padają `ani jedna`, `dwa z tych czytań` i każde inne miejsce,
w którym przymiotnik albo liczebnik stoi za rzeczownik,
którego zdanie przed chwilą użyło.
Pozycja ta stoi tu inaczej niż pozostałe, bo jest już zmierzona:
jedno ciało wyciąga zdania z odrzucenia,
a jednoznaczność odbiera większej liczbie zdań, niż wyciąga,
i wypada tak w każdym z trzech przebiegów
([subset.md](subset.md#what-it-does-not-cover-yet) trzyma liczby).
Płaci więc za nią autor i będzie płacił, a wpis zostaje na liście po to,
żeby nikt nie liczył jej drugi raz.

**Okolicznik narzędnikowy wysunięty przed zdanie.**
`Czasem granica jest granicą modułu.` pada,
`Granica jest czasem granicą modułu.` przechodzi.
Narzędnik bez przyimka gramatyka bierze i bierze go na każdym miejscu okolicznika
poza tym jednym ([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)),
bo przed zdaniem stoi już orzecznik wysunięty przed kopulę.
Naprawą jest tu przestawienie okolicznika za czasownik.

**Liczebnik rządzący w orzeczniku.**
`Torów jest dwa.` pada, `Tory są dwa.` przechodzi.
Zgodny orzeka i orzeka razem z dwukropkiem, który wylicza —
`Tory są dwa: gramatyka i skład.` —
a rządzący stawia podmiot w dopełniaczu i nie zgadza orzeczenia z niczym
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-orzeka-o-tym-ile-czegoś-jest)).
Naprawą jest tu wymiana szyku na zgodny.

**Apozycja z nazwą.**
`Bank drzew Składnica mierzy gramatykę.` pada,
`Składnica jest bankiem drzew.` przechodzi.
Rejestr techniczny nazywa tak każdy artefakt zewnętrzny —
korpus Składnica, słownik Morfeusz, wydanie takie a takie —
a olski żąda na to osobnego zdania.
Tą samą drogą pada zdanie, które cytuje inne zdanie,
więc [README](../README.md#co-działa) nie zapowiada przykładu jego słowami,
tylko blokiem pod spodem.
Spójnika apozycja nie ma, więc od członu bez czasownika, który wszedł,
różni ją to, że nie ma czym wpuścić jej osobno
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze));
cenę tej produkcji trzyma `todo/`.

**Cząstka `się` oddalona od swojego czasownika.**
`Rachunek się dotąd nie zwraca.` pada,
`Rachunek dotąd się nie zwraca.` przechodzi,
i tak samo pada `Nie mogłem się na niczym skupić.`,
gdzie cząstka należy do `skupić`, a odgradza ją od niego wyrażenie przyimkowe.
Obie pozycje tuż przy czasowniku gramatyka ma i ma je przy każdej jego formie
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika)),
więc naprawą jest przysunięcie cząstki do czasownika, do którego należy.

**Cząstka `tylko` wewnątrz grupy imiennej.**
`Istnieją tylko te konstrukcje, które stoją na liście.` pada,
`Istnieją te konstrukcje, które stoją na liście.` przechodzi.
Pozycję wewnątrz grupy cząstka ma
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#cząstka-ma-dwóch-gospodarzy-i-przy-jednym-dostaje-etykietę)),
a `tylko` zostaje poza listą cząstek,
bo Morfeusz czyta je także jako spójnik;
w tym rejestrze jest to cząstka określająca grupę imienną najczęściej.

**Spójnik skorelowany zaczynający się za podmiotem.**
`Werdykt ani nie wnosi, ani nie zdejmuje.` pada,
`Ani werdykt nie wnosi, ani nie zdejmuje.` przechodzi.
Spójnik powtórzony przed każdym członem gramatyka ma
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-skorelowany-powtarza-się-przed-każdym-członem)),
a te dwa zdania rozdziela miejsce, w którym ciąg się zaczyna:
w drugim otwiera on zdanie składowe, w pierwszym stoi za jego podmiotem,
czyli spina same orzeczenia, a takiej pozycji koordynacja nie ma.
Polszczyzna pisze oba szyki, a autor płaci tu przestawieniem podmiotu
przed pierwszy spójnik.

**Słowo pytające poza tymi pięcioma.**
Pozycja ta stoi tu inaczej niż pozostałe, bo zdania z nią nie padają:
`Pyta, ile ta gramatyka kosztuje.` i `Pyta, jak to działa.`
wychodzą przyjęte, a wychodzą na czytaniu, którego polszczyzna nie ma.
Morfeusz daje `ile` i `jak` część mowy `adv`, a `jaki` przymiotnikową,
i olski bierze te części mowy całe, więc słowo pytające staje okolicznikiem
albo przydawką, a pytania zależnego w tym zdaniu nie ma wcale.
Autor nie ma po czym poznać, że napisał zdanie poza olskim,
i dlatego pozycja ta jest droższa od tych, które zawracają.
Dopisane słowo pytające ma to czytanie zdjąć, a nie stanąć obok niego;
`todo/` trzyma ruch.
Pytanie ma w gramatyce cztery kształty — zaimek przy rzeczowniku,
`kto` i `co` same
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)),
`czy` nad całym zdaniem
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą))
oraz `dlaczego` przed zdaniem całym
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#pytanie-o-okoliczność-wysuwa-przysłówek-a-zdanie-pod-nim-jest-całe)) —
a `jak`, `jaki` i `ile` żądają każde innego
([subset.md](subset.md#what-it-does-not-cover-yet)).
Dokument, który opisuje rolę czytelnika, pisze te zdania zdanie po zdaniu,
bo rola pyta, a pytanie jest jej definicją.

**Pytanie o miejsce.**
`Gdzie są przetrzymywani zakładnicy?` pada,
a `Wchodzi w roadmap.md, gdzie każdy etap ma kryterium wyjścia.` przechodzi.
Okolicznik z `gdzie` gramatyka ma
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#przysłówek-względny-otwiera-okolicznik-i-nie-określa-zdania)),
a kształt pytania o okoliczność ma od `dlaczego`,
więc zostaje tu sam lemat i wraca on razem z zawężeniem ramy domyślnej:
dopisany dziś daje drugie czytanie każdemu zdaniu z okolicznikiem tego kształtu
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#pytanie-o-okoliczność-wysuwa-przysłówek-a-zdanie-pod-nim-jest-całe)).
Naprawą jest tu na razie zdanie oznajmujące o tym samym.

**Bezokolicznik pod słowem, które orzeka bez podmiotu.**
`To jest stan, którego warto pilnować.` pada,
`Trzeba czytać dokumenty.` przechodzi.
Predykatyw bierze bezokolicznik na swoim miejscu,
a nie bierze go tam, gdzie zdanie względne wysunęło przed niego dopełnienie.

**Angielska nazwa pisana małą literą.**
`README mówi o podzbiorze.` przechodzi,
a `Sekcja mówi o build w olski/subset/__init__.py.` pada na `build`.
Czytanie nieodmienne dostaje forma pisana wersalikami i nieznana słownikowi
([warstwa-leksykalna.md](warstwa-leksykalna.md#wersalik-bez-czytania-jest-tym-samym-rzeczownikiem-nieodmiennym)),
a `build`, `merge` i `yet decided` pierwszego z tych dwóch żądań nie spełniają:
pisane małą literą nie różnią się niczym od polskiego słowa,
którego słownik nie ma, a takiemu czytania nieodmiennego dać nie wolno
([warstwa-leksykalna.md](warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)).
Dokumentacja przytacza je w cudzysłowie albo w backtickach,
i te dwa sposoby olski rozdziela.
Cudzysłów licencjonuje przytoczenie, więc `Sekcja mówi o „build”.` przechodzi
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)),
a `` `build` `` wraca z Morfeusza jednym napisem razem z backtickami.

**Drugi leksem do napisu, który słownik zna.**
`Linter sprawdza tekst.` przechodzi, `Cena lintera jest niska.` pada na `lintera`.
SGJP zna `linter` i daje mu dopełniacz `linteru`,
a ta proza odmienia go wedle drugiego leksemu.
Leksykon projektu takiego wiersza nie przyjmuje z powodu, który sam podaje,
a ruch trzyma `todo/`.

**Notacja z jednoliterowym członem.**
`docs/pisanie-po-olsku.md jest raportem.` przechodzi,
a `docs/pisanie-w-olskim.md jest raportem.` pada na `-`.
Wzorzec notacji nie przyjmuje członu z jednej litery i mówi, za co tak płaci
([warstwa-leksykalna.md](warstwa-leksykalna.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)),
więc nazwy pliku z `w` albo `i` w środku nie da się w olskim wymówić.
Ten dokument nazywa się tak, jak się nazywa, właśnie dlatego.
Tak samo pada flaga: `--readings` rozpada się na `-`, `-` i słowo.

## Co w tym fotelu działa

Streszczenie czytań diagnozuje wieloznaczność jednym spojrzeniem:
strzałka mówi, co czytelnik ma wybrać,
a nazwy roli mówią, co zdanie znaczy w każdym z czytań
([README](../README.md#co-działa)).

Przebieg nad całym plikiem trwa poniżej sekundy,
więc pętla „popraw i sprawdź” nie ma tarcia,
a taniość rozbioru mierzy się właśnie tą liczbą.
Nad jednym zdaniem `-c` odpowiada, zanim zdąży się przełączyć okno.

Odrzucenie z nazwaną formą naprawia się bez myślenia.
Wieloznaczność przestaje być przy tym po dwudziestu zdaniach sygnałem:
prawie każda bierze się z przyłączenia albo ze synkretyzmu,
o czym projekt rozstrzygnął
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
więc znalezisko czyta się jak brak werdyktu.
Nagrodą jest zaś milczenie, które bywa nie za składnię, a za dobór słów:
to samo zdanie z dopełnieniem żeńskim wychodzi jednoznaczne,
a z rzeczownikiem rodzaju m3 nie.

## Cena, którą olski zostawia w prozie

Pisanie pod olskiego popycha w pięć chwytów:
zdanie krótkie, kopułę z narzędnikiem, wyrażenie przyimkowe na czele zdania,
dopełnienie w rodzaju żeńskim i orzekanie przez zaprzeczenie.
Trzy pierwsze widać w README po przepisaniu,
a reguły prozy każą unikać
jednego rytmu na wszystko.
Gramatyka nagradza więc rejestr, który reguły prozy karzą.

Chwyt piąty wychodzi na jaw dopiero przy przepisywaniu zdania na twierdzące.
Polszczyzna stawia dopełnienie po przeczeniu w dopełniaczu,
a dopełniacz zdejmuje synkretyzm mianownika z biernikiem,
przez który olski daje zdaniu dwa czytania:
`Pokrycia gramatyki skład nie dziedziczy.` wychodzi jednoznaczne,
a `Skład dziedziczy pokrycie gramatyki.` wieloznaczne.
Zdanie zanegowane jest przez to tańsze o jedno czytanie od tego samego twierdzenia,
a kontrastowa rama
jest tym, co reguły prozy wykreślają.

Płaci tu gramatyka, bo zdanie długie jest polszczyzną
i ten rejestr pisze je stale,
a płaci pozycjami z kolejki wyżej.
Za urwiskiem zdanie potyka się nie o jeden brak, tylko o kilka naraz,
więc pozycja z tej kolejki kupuje takie zdanie dopiero razem z resztą.
Skracanie zostaje radą dla piszącego dzisiaj, a nie kierunkiem dla gramatyki.

## Czego ten dokument nie mówi

Materiał wyszedł z sesji agenta nad prozą tego repozytorium —
[README](../README.md#konwencje), [`roles.md`](roles.md),
[`architecture.md`](architecture.md) oraz kolejka po formie nad całym `docs/` —
a fotel bywał w nich jeden, drugi albo oba naraz.
Nad `architecture.md` sesje były dwie i różni je jednostka:
pierwsza szła za jedną formą przez cały katalog,
a druga rozstrzygnęła każde zdanie tego jednego dokumentu po kolei
([wyżej](#przebieg-po-całym-dokumencie-kupuje-zdania-szykiem-a-nie-produkcją)).
Rejestr jest przy tym jeden, a człowiek redagujący własny plik
nie siedział w żadnej z tych sesji, więc jest to raport, a nie pomiar.

Liczby mają właścicieli tam, gdzie stoją nad tekstem z repozytorium:
ile zdań pliku się wyprowadza, drukuje `olski.check`,
a kolejkę blokerów i krzywą pokrycia po długości zdania nad prozą
drukuje `olski-pokrycie`, i te same tabele nad bankiem drzew `harness.pomiar`
([corpus.md](corpus.md#the-same-queue-over-prose)).
Zdania kandydujące z pierwszej sesji stały w katalogu tymczasowym
i do repozytorium nie weszły, więc jej liczby zostały w gicie.

Rachunku po stronie autora nie mierzy nic:
liczba przecinków poprawionych w jednym dokumencie jest liczbą przeczytań,
a nie przebiegu, i tak samo będzie z każdym następnym takim znaleziskiem.

Powtórzyć da się każdą parę zdań wyżej, przez `olski.check -c`,
i po to każda z nich stoi w tym dokumencie cała.
