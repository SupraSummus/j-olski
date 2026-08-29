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
a wtedy werdykt `valid` niczego już nie obiecuje.

Oba fotele obsadza jedna osoba i to ona wymusza równowagę
([roles.md](roles.md#rola-jest-postawą-nie-osobą)):
kto zdanie przepisuje, sam potem wycenia produkcję, która by je wpuściła,
więc kosztu nie ma komu podrzucić.
Każde zdanie ta osoba rozstrzyga przy tym osobno,
a rozstrzyga je [pytaniem](#kto-płaci-za-odrzucone-zdanie),
którego odpowiedź otwiera jeden z trzech rachunków.

Planem to nie jest.
Właścicielem ruchu jest [`TODO.md`](../TODO.md),
kolejności [`roadmap.md`](roadmap.md),
a ceny wpuszczenia konstrukcji
[`subset.md`](subset.md#what-the-grammar-covers);
tu stoi tylko materiał, którego te trzy dokumenty nie miały skąd wziąć.

## Kto płaci za odrzucone zdanie

**Pytanie brzmi: czy polszczyzna ma ten napis.**
Nie czy zdanie jest zrozumiałe i nie czy da się je poprawić.

**Za napis, którego polszczyzna nie ma, płaci autor.**
Gramatyka zapłacić nie może, bo obietnicą podzbioru jest,
że każde zdanie olskiego jest zdaniem polskim,
a produkcja wpuszczająca taki napis odbiera tę obietnicę wszystkim zdaniom naraz.
Autor dostaje za to poprawiony tekst
([niżej](#odrzucenie-bywa-poprawką)).

**Za napis, który polszczyzna ma i ten rejestr pisze, płaci gramatyka.**
Autor zapłacić nie może, bo przepisanie takiego zdania znaczy napisanie go
gorzej pod parser, a podzbiór, w którym nie da się pisać tego,
co ten rejestr mówi, mierzy sam siebie zamiast polszczyzny.
Cenę produkcji liczy autor przed dopisaniem ([README](../README.md#kierunek)).

**Za napis, który polszczyzna ma, a ten rejestr pisze rzadko, nie płaci nikt.**
Taki napis wchodzi na kolejkę, a rachunek ten jest z trzech największy:
o nim mówi cała [kolejka blokerów](corpus.md#where-the-analyses-stop).
Rozstrzyga o nim cena, czyli liczba zdań, które konstrukcja kupuje,
i po tej liczbie tamta kolejka jest ułożona, a nie po dolegliwości.

Tego pytania nie policzy żaden przebieg.
Kolejka mówi, ile razy analiza stanęła na danej formie,
a czy stanęła na polszczyźnie, czy na literówce, widać dopiero po przeczytaniu zdania.
Dlatego z tego fotela wychodzi dokument, a nie druga tabela.

## Odrzucenie bywa poprawką

Formą, na której analiza nad tą prozą staje najczęściej, jest spójnik `i`,
a częstą przyczyną tych zatrzymań jest przecinek postawiony przed `i`,
którego nie stawia tu żadna zasada.
Polska interpunkcja stawia go przed `i` tylko tam,
gdzie domyka on zdanie podrzędne albo wtrącenie,
i olski ma dokładnie te dwa miejsca
([subset.md](subset.md#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
W `architecture.md` pięć zdań miało ten przecinek bez żadnego z tych dwóch powodów.

Płaci tu autor i ten rachunek się zwraca.
Zdania te były niepoprawne przed olskim i nikt tego nie zauważył:
[reguły prozy](../CLAUDE.md#dla-kogo-jest-napisane-zdanie) o interpunkcji nie mówią,
`markdownlint` czyta Markdown, a nie polszczyznę,
a `tests/test_docs.py` sprawdza nazwy plików i sekcji.
O tym przecinku powiedział w tym repozytorium tylko werdykt `rejected`.

Odpowiada to na zarzut, że
[biała lista każe pisać pod parser](../README.md#dlaczego-biała-lista-skoro-czarna-była-tańsza).
Każe wtedy, gdy się myli, a kiedy się nie myli, każe pisać poprawną polszczyzną.
Który z tych dwóch wypadków zachodzi, rozstrzyga czytelnik i po to ten fotel jest.

Przecinek przed `i` stoi w tej prozie setki razy,
a które z tych miejsc nie domykają niczego, widać dopiero po przeczytaniu każdego;
ruch trzyma [`TODO.md`](../TODO.md).

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
([subset.md](subset.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)),
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
([subset.md](subset.md#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
Cena pozycji nie jest przez to liczbą, którą raz się zapisuje,
a dwie pozycje wpuszczone razem bywają warte więcej niż z osobna.

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

Drugie pytanie brzmi: ile jeszcze.
Jedno zatrzymanie zasłania każde następne,
bo analiza przerywa się na pierwszym i o resztę zdania nie pyta,
więc kto poprawi to jedno miejsce, dostaje zdanie odrzucone drugi raz.
Odpowiada na to `--zatrzymania`:
ta sama analiza rusza od nowa za każdym zatrzymaniem,
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
<text>: ambiguous Janek lubi piwo.
                  2 odczytania, różne w Object, Subject
                  - Subject: Janek, Object: piwo, Verb: lubi
                  - Subject: piwo, Object: Janek, Verb: lubi
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
([subset.md](subset.md#the-dictionary-offers-readings-polish-does-not)).
Autorowi zostaje więc wymiana słowa, a nie przestawienie zdania:
`Janek pije piwo.` jest wieloznaczne tak samo,
a `Chłopiec lubi piwo.` ma jedno odczytanie.
Wykaz mówi mu przy tym, którą formę wymienić,
bo odczytanie z siedmioma przypadkami widać w nim po samym znaczniku.

## Kolejka czytana po formie mówi to, czego nie mówi po części mowy

Kolejka blokerów grupuje zatrzymania po części mowy formy
([`olski/pokrycie.py`](../olski/pokrycie.py)).
Nad wierszami otwartymi — `fin`, `subst`, `prep` — mówi to dość,
a nad zamkniętymi zbiera pod jedną nazwą formy żądające każda innej konstrukcji:
wiersz `conj` prowadzą w tym rejestrze `i` oraz `a`,
a pod nimi stoją `czy`, `czyli` i `ani`
([corpus.md](corpus.md#where-the-analyses-stop) trzyma, które wiersze prowadzą).
Ruch nad tym wierszem trzyma [`TODO.md`](../TODO.md).

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

**Liczebnik w orzeczniku.**
`Tory są dwa.` pada, `Torów jest dwa.` też,
a `Działają dwie rzeczy.` przechodzi.
Grupa liczebnikowa jest wpuszczona jako podmiot i jako dopełnienie,
a zdanie, które mówi, ile czegoś jest, nie wychodzi.
Ten brak zasłania zarazem dwukropek, który wylicza:
`Tory są dwa: gramatyka i skład.` ma pozycję za dwukropkiem
([subset.md](subset.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
a nie ma czasownika przed nim.

**Apozycja z nazwą.**
`Bank drzew Składnica mierzy gramatykę.` pada,
`Składnica jest bankiem drzew.` przechodzi.
Rejestr techniczny nazywa tak każdy artefakt zewnętrzny —
korpus Składnica, słownik Morfeusz, wydanie takie a takie —
a olski żąda na to osobnego zdania.
Spójnika apozycja nie ma, więc od członu bez czasownika, który wszedł,
różni ją to, że nie ma czym wpuścić jej osobno
([subset.md](subset.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze));
cenę tej produkcji trzyma [`TODO.md`](../TODO.md).

**Cząstka `się` oddalona od swojego czasownika.**
`Rachunek się dotąd nie zwraca.` pada,
`Rachunek dotąd się nie zwraca.` przechodzi,
i tak samo pada `Nie mogłem się na niczym skupić.`,
gdzie cząstka należy do `skupić`, a odgradza ją od niego wyrażenie przyimkowe.
Obie pozycje tuż przy czasowniku gramatyka ma i ma je przy każdej jego formie
([subset.md](subset.md#cząstka-zwrotna-należy-do-swojego-czasownika)),
więc naprawą jest przysunięcie cząstki do czasownika, do którego należy.

**Cząstka `tylko` wewnątrz grupy imiennej.**
`Istnieją tylko te konstrukcje, które stoją na liście.` pada,
`Istnieją te konstrukcje, które stoją na liście.` przechodzi.
Pozycję wewnątrz grupy cząstka ma
([subset.md](subset.md#cząstka-wchodzi-obu-gospodarzami-a-w-grupie-nie-nosi-etykiety)),
a `tylko` zostaje poza listą cząstek,
bo Morfeusz czyta je także jako spójnik;
w tym rejestrze jest to cząstka określająca grupę imienną najczęściej.

**Spójnik skorelowany.**
`Werdykt ani nie wnosi, ani nie zdejmuje.` pada,
`Werdykt nie wnosi i nie zdejmuje.` przechodzi.
Polszczyzna powtarza tu spójnik przed każdym członem,
a koordynacja olskiego stawia go raz i między członami.

**Słowo pytające poza tymi trzema.**
`Pyta, czy go to dotyczy.` pada, `Pyta, który parser jest tani.` przechodzi.
Pytanie ma w gramatyce dwa kształty — zaimek przy rzeczowniku
oraz `kto` i `co` same
([subset.md](subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)) —
a `czy`, `jak`, `jaki`, `ile` i `gdzie` żądają każde innego
([subset.md](subset.md#what-it-does-not-cover-yet)).
Dokument, który opisuje rolę czytelnika, pisze te zdania zdanie po zdaniu,
bo rola pyta, a pytanie jest jej definicją.

**Bezokolicznik pod słowem, które orzeka bez podmiotu.**
`To jest stan, którego warto pilnować.` pada,
`Trzeba czytać dokumenty.` przechodzi.
Predykatyw bierze bezokolicznik na swoim miejscu,
a nie bierze go tam, gdzie zdanie względne wysunęło przed niego dopełnienie.

**Dopełnienie przed czasownikiem w zdaniu względnym.**
`Reguła, która tekst sprawdza, jest tania.` pada,
`Reguła, która sprawdza tekst, jest tania.` przechodzi,
choć `Reguła tekst sprawdza.` przechodzi też.
Zdanie główne ma wszystkie szyki podmiotu, dopełnienia i czasownika
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
a zdanie względne, którego czoło jest podmiotem, ma jeden:
ten z dopełnieniem za czasownikiem.
Ruch trzyma [`TODO.md`](../TODO.md).

**Przymiotnik w formie poprzyimkowej.**
`Reguła działa po polsku.` pada, `Reguła działa wszędzie.` przechodzi.
Morfeusz daje formie `polsku` część mowy `adjp`, której nie bierze żaden terminal,
a okoliczność wyrażoną tak polszczyzna pisze wszędzie: `po kolei`, `po cichu`.
Nazwa tego dokumentu potrzebuje przy tym dwóch napraw, a nie jednej,
bo `olsku` wraca z Morfeusza jako `ign`:
[leksykon projektu](subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)
wydaje temu słowu przymiotnik i rzeczownik, a formy poprzyimkowej nie wydaje.

**Angielska nazwa pisana małą literą.**
`README mówi o podzbiorze.` przechodzi,
a `Sekcja mówi o build w olski/subset.py.` pada na `build`.
Czytanie nieodmienne dostaje forma pisana wersalikami i nieznana słownikowi
([subset.md](subset.md#wersalik-bez-czytania-jest-tym-samym-rzeczownikiem-nieodmiennym)),
a `build`, `merge` i `yet decided` pierwszego z tych dwóch żądań nie spełniają:
pisane małą literą nie różnią się niczym od polskiego słowa,
którego słownik nie ma, a takiemu czytania nieodmiennego dać nie wolno
([subset.md](subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)).
Dokumentacja przytacza je w cudzysłowie albo w backtickach,
i te dwa sposoby olski rozdziela.
Cudzysłów licencjonuje przytoczenie, więc `Sekcja mówi o „build”.` przechodzi
([subset.md](subset.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)),
a `` `build` `` wraca z Morfeusza jednym napisem razem z backtickami.

**Drugi leksem do napisu, który słownik zna.**
`Linter sprawdza tekst.` przechodzi, `Cena lintera jest niska.` pada na `lintera`.
SGJP zna `linter` i daje mu dopełniacz `linteru`,
a ta proza odmienia go wedle drugiego leksemu.
Leksykon projektu takiego wiersza nie przyjmuje z powodu, który sam podaje,
a ruch trzyma [`TODO.md`](../TODO.md).

**Notacja z jednoliterowym członem.**
`docs/pisanie-po-olsku.md jest raportem.` przechodzi,
a `docs/pisanie-w-olskim.md jest raportem.` pada na `-`.
Wzorzec notacji nie przyjmuje członu z jednej litery i mówi, za co tak płaci
([subset.md](subset.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)),
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
i to jest ta taniość, o której README mówi na wstępie.
Nad jednym zdaniem `-c` odpowiada, zanim zdąży się przełączyć okno.

Odrzucenie z nazwaną formą naprawia się bez myślenia.
Wieloznaczność przestaje być przy tym po dwudziestu zdaniach sygnałem:
prawie każda bierze się z przyłączenia albo ze synkretyzmu,
o czym projekt rozstrzygnął
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
więc `ambiguous` czyta się jak brak werdyktu.
Nagroda `valid` bywa zaś nie za składnię, a za dobór słów:
to samo zdanie z dopełnieniem żeńskim wychodzi jednoznaczne,
a z rzeczownikiem rodzaju m3 nie.

## Cena, którą olski zostawia w prozie

Pisanie pod olskiego popycha w cztery chwyty:
zdanie krótkie, kopułę z narzędnikiem, wyrażenie przyimkowe na czele zdania
i dopełnienie w rodzaju żeńskim.
Trzy pierwsze widać w README po przepisaniu,
a [reguły prozy](../CLAUDE.md#dla-kogo-jest-napisane-zdanie) każą unikać
jednego rytmu na wszystko.
Gramatyka nagradza więc rejestr, który reguły prozy karzą.

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
