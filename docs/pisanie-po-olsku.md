# Pisanie po olsku: feedback z fotela użytkownika

Dokument zbiera to, co widać z fotela użytkownika:
kogoś, kto olskiego używa przy tekście, zdanie po zdaniu,
zamiast mierzyć gramatykę nad korpusem.
Siada się w nim na dwa sposoby i każdy z nich mówi o czym innym.

Pierwsza sesja pisała *pod* gramatykę:
przepisała [README](../README.md#konwencje) na zdania, które olski wyprowadza,
i przepuściła przez `olski.check` kilkaset kandydatów na zdanie.
Druga wzięła na celownik dokument, którego nikt pod gramatykę nie pisał —
[`roles.md`](roles.md) — i próbowała podnieść w nim liczbę zdań wyprowadzonych,
dopisując gramatyce to, czego temu dokumentowi brakowało.
Pierwsza zmieniała tekst, druga gramatykę.
Trzecia siadła w obu fotelach naraz nad [`architecture.md`](architecture.md)
i przez to musiała rozstrzygnąć, czego dwie pierwsze nie rozstrzygały:
przy którym zdaniu płaci autor, a przy którym płaci gramatyka.

Planem to nie jest.
Właścicielem ruchu jest [`TODO.md`](../TODO.md),
kolejności [`roadmap.md`](roadmap.md),
a ceny wpuszczenia konstrukcji
[`subset.md`](subset.md#what-the-grammar-covers);
tu stoi tylko materiał, którego te trzy dokumenty nie miały skąd wziąć.

## Kto płaci za odrzucone zdanie

Dwa pierwsze fotele odpowiadają skrajnie.
Kto pisze pod gramatykę, płaci za każde odrzucenie sam
i kończy z rejestrem, którego nikt nie wybrał.
Kto dopisuje gramatyce każdy brak, jaki zgłosił mu jego dokument,
wpuszcza w końcu napis, którego polszczyzna nie ma,
a wtedy werdykt `valid` niczego już nie obiecuje.
Wyboru między nimi nie rozstrzyga gust.
O każdym pojedynczym zdaniu rozstrzyga jedno pytanie,
a odpowiedź na nie otwiera jeden z trzech rachunków.

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

Trzecia sesja zaczęła od rankingu form, na których staje analiza nad tą prozą,
i pierwszą z nich okazał się spójnik `i`.
Część tych zatrzymań to zdania, w których zawiodło coś przed spójnikiem,
a część to jedna rzecz: przecinek postawiony przed `i`,
którego nie stawia tu żadna zasada.
Polska interpunkcja przecinka przed `i` łączącym zdania współrzędne nie stawia,
a stawia go tam, gdzie domyka on coś, co trzeba domknąć —
zdanie podrzędne albo wtrącenie —
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
Który z tych dwóch wypadków zachodzi, rozstrzyga czytelnik, i po to ten fotel jest.

Klasa jest przy tym szersza niż jeden dokument.
Przecinek przed `i` stoi w tej prozie setki razy,
a które z tych miejsc nie domykają niczego, widać dopiero po przeczytaniu każdego.
Przebiegu tego nikt nie zrobił; wpis trzyma [`TODO.md`](../TODO.md).

## Zasłanianie działa w obie strony

Druga sesja zostawiła po sobie pomiar o tym,
że pozycja dopisana do gramatyki nie rusza liczby nad zdaniem długim:
zdanie o dwudziestu wyrazach ma kilka zatrzymań naraz,
a wyprowadza się dopiero wtedy, gdy zamkną się wszystkie,
więc dopisana pozycja zdejmuje jedno z nich
i zostawia zdanie odrzucone, tylko dalej.
Krzywą pokrycia po długości zdania trzyma
[corpus.md](corpus.md#the-measurement) i mówi ona to samo od drugiej strony:
pokrycie spada z urwiska między dziesiątym a dwudziestym tokenem.

Trzecia sesja dodaje do tego jedno zdanie: poprawka autora zasłania się tak samo.
Z pięciu poprawionych przecinków dwa wypuściły swoje zdanie z odrzuconych,
a trzy przesunęły zatrzymanie w prawo i zostawiły zdanie tam, gdzie stało,
bo za przecinkiem czekał w każdym z nich jeszcze jeden brak.
Nagroda przychodzi więc za ostatni brak, a nie za każdy,
i nie zależy od tego, kto go zdjął.

Rada dla piszącego zostaje ta sama, którą zostawiła druga sesja:
liczba pokrycia nad własnym dokumentem nie jest sygnałem,
dopóki zdania tego dokumentu są długie.
Sygnałem jest zatrzymanie, bo ono się rusza,
i po to `--zatrzymania` pokazuje je wszystkie nad jednym zdaniem,
a `olski.coverage` nad całym plikiem układa je w kolejkę
([corpus.md](corpus.md#the-same-queue-over-prose)).
Zdanie krótkie ma odwrotnie: jedno zatrzymanie, jedną poprawkę i widoczny skutek,
czego pierwsza sesja doświadczyła nad README, gdzie zdania są krótkie.
Która proza gdzie leży, drukuje krzywa nad plikiem.

To samo zasłanianie widać o szczebel wyżej, na cenie pozycji.
Sonda różnicowa wycenia pozycję, zdejmując ją z gramatyki,
więc wycenia ją wobec wszystkiego, co w gramatyce zostaje:
przecinek zamykający zdanie podrzędne kupił nad bankiem drzew kilkadziesiąt zdań
obok przydawki imiesłowowej, a bez niej kupiłby pojedyncze,
bo zdanie potrzebujące obu potyka się o tę, której nie ma
([subset.md](subset.md#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
Cena pozycji nie jest przez to liczbą, którą raz się zapisuje,
a dwie pozycje wpuszczone razem bywają warte więcej niż z osobna.

## Odrzucenie mówi, na czym stanęło, i mówi to raz

Pierwsza sesja nie miała nawet takiego werdyktu.
Na każde dziesięć odrzuceń dziewięć mówiło wtedy tyle,
że nic w olskim tego zdania nie wyprowadza.
Reszta nazwała formę — `no production takes „GLR”` — i ta reszta była łatwa,
bo naprawa jest widoczna od razu.
Metodą, która zostawała, była bisekcja ręką:
zdanie o pięciu członach dzieli się na pół, każdą połowę puszcza osobno,
potem wymienia się w podejrzanym członie jedno słowo i puszcza znowu.
Na jedno odrzucone zdanie wychodziło tak kilka do kilkunastu przebiegów,
a wiedza, która z tego zostaje, jest wiedzą o tym jednym zdaniu.

Werdykt nazywa dziś miejsce, na którym analiza stanęła,
i nazywa je dwoma zdaniami, bo zatrzymanie na formie
i zdanie, którego nic nie domyka, są dwoma zdarzeniami
([`subset.md`](subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).
Odpowiada tym na pierwsze pytanie tamtej bisekcji, czyli który człon tknąć.
Miejsce zatrzymania jest przy tym końcem przedrostka, który się analizuje,
a nie wskazaniem usterki,
więc para niezgodna rodzajem wychodzi dalej, niż stoi.

Zostawało po tym drugie pytanie bisekcji: ile jeszcze.
Jedno zatrzymanie zasłania każde następne,
bo analiza przerywa się na pierwszym i o resztę zdania nie pyta.
Kto poprawi to jedno miejsce, dostaje zdanie odrzucone drugi raz,
tylko z zatrzymaniem przesuniętym w prawo.
Odpowiada na to `--zatrzymania`:
ta sama analiza rusza od nowa za każdym zatrzymaniem,
więc wychodzi z niej zdanie pocięte na kawałki, z których każdy się analizuje,
wraz z formami, na których leżą cięcia.

```sh
python3 -m olski.check --zatrzymania -c "Dokument nazywa role, w jakich ktoś to repozytorium czyta, a dla każdej z nich: pytanie, z którym przychodzi."
```

```text
<text>: rejected  Dokument nazywa role, w jakich ktoś to repozytorium czyta, a dla każdej z nich: pytanie, z którym przychodzi.
                  no reading: the analysis stops at „repozytorium”
                  the analysis stops again at „z”, „:”
0 of 1 sentences are olski, and 0 have a reading
```

Liczba cięć mówi, ile miejsc trzeba tknąć, i tyle ta flaga odpowiada.
Cięcie nie jest granicą konstrukcji ani wskazaniem usterki:
kawałek analizuje się osobno, a zdanie nie składa się z kawałków,
które analizują się osobno.
Zastrzeżenie jest to samo co przy jednym zatrzymaniu, powtórzone tyle razy, ile cięć.

## Kolejka czytana po formie mówi to, czego nie mówi po części mowy

Kolejka blokerów grupuje zatrzymania po części mowy formy,
a nad prozą tego repozytorium część mowy bierze się z pierwszego czytania,
które dał Morfeusz, bo pod żywą morfologią forma ma ich kilka
([`olski/coverage.py`](../olski/coverage.py)).
Nad wierszami otwartymi — `fin`, `subst`, `prep` — mówi to dość,
a nad zamkniętymi rozsypuje się:
`i` wychodzi w tej kolejce jako `interj`, `a` tak samo,
więc dwie najczęstsze formy tego rejestru chowają się pod nazwą,
która o żadnej konstrukcji nie mówi nic.
Wiersz `interj` stoi w tej kolejce wysoko i przeczytać się go nie da.

Trzecia sesja zaczęła od kolejki policzonej po formie, a nie po części mowy,
i to ona ułożyła kolejność tej sesji:
`i`, `a`, dwukropek, `więc`, myślnik, `się`, `czyli`, `tylko`.
Ranking taki nie stoi w żadnym narzędziu tego repozytorium
i został napisany na jeden przebieg;
wpis o tym, czy ma stanąć obok tamtego, trzyma [`TODO.md`](../TODO.md).

Kolejka po formie odpowiada zarazem na pytanie o rachunek.
Forma nazywa słowo, a słowo da się przeczytać:
widać po nim, czy polszczyzna ma napis, w którym ono stoi.
Część mowy tego nie mówi, bo `interp` obejmuje naraz przecinek postawiony źle
i dwukropek, którego gramatyce brakuje.

## Czego brakowało najbardziej

Lista jest ułożona według tego, ile razy pozycja zawróciła zdanie,
a nie według tego, ile by kosztowało wpuszczenie.
Przy każdej stoi para zdań, z których pierwsze nie ma czytania,
a drugie się wyprowadza, bo różnica między nimi jest tu całą informacją.
O jednoznaczność ta lista nie pyta, bo pyta o pozycję, której w gramatyce nie ma.
Pozycja wpuszczona do gramatyki z tej listy schodzi
i zostaje po niej sekcja w [`subset.md`](subset.md#what-the-grammar-covers).

**Celownik.**
`Parser mówi autorowi o czytaniach.` pada, `Parser pokazuje oba czytania.` przechodzi.
Zdanie, które README stawia najwyżej — parser mówi *autorowi*, że coś jest dwojakie —
nie da się w olskim powiedzieć wcale,
więc stoi tam dziś bez adresata.
[Walencja poza biernikiem](subset.md#what-it-does-not-cover-yet) obejmuje to jako żądanie,
a nie jako pozycję, i z tego fotela jest to najdroższy pojedynczy brak.

**Grupa imienna z elipsą głowy.**
`Wszystkie obsadza jedna osoba.` pada, `Wszystkie role obsadza jedna osoba.` przechodzi.
Tak samo padają `ani jedna`, `dwa z tych czytań` i każde inne miejsce,
w którym przymiotnik albo liczebnik stoi za rzeczownik,
którego zdanie przed chwilą użyło.

**Ciąg współrzędny przymiotników przy rzeczowniku.**
`Nowy i tani parser zapisuje ustawienia.` pada,
`Nowy parser zapisuje ustawienia.` przechodzi,
i tak samo pada szyk drugi: `Warstwy trzecia i czwarta pracują.`
Koordynacja stoi w gramatyce na trzech poziomach
([subset.md](subset.md#nothing-above-a-coordination-distributes-into-it)),
a przydawka nie jest żadnym z nich: jest pojedynczym przymiotnikiem.
Szyk drugi żąda przy tym więcej niż pierwszy,
bo `warstwy` jest mnogie, a `trzecia` pojedyncza,
więc ciąg wypuszcza liczbę, której nie ma ani jeden przymiotnik w środku —
dokładnie tak, jak wypuszcza ją ciąg imienny
([subset.md](subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)).

**Liczebnik w orzeczniku.**
`Tory są dwa.` pada, `Torów jest dwa.` też,
a `Działają dwie rzeczy.` przechodzi.
Grupa liczebnikowa jest wpuszczona jako podmiot i jako dopełnienie,
a zdanie, które mówi, ile czegoś jest, dalej nie wychodzi.
Ten brak zasłania zarazem dwukropek, który wylicza:
`Tory są dwa: gramatyka i skład.` ma dziś pozycję za dwukropkiem
([subset.md](subset.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
a nie ma czasownika przed nim.

**Apozycja z nazwą.**
`Bank drzew Składnica mierzy gramatykę.` pada,
`Składnica jest bankiem drzew.` przechodzi.
Rejestr techniczny nazywa tak każdy artefakt zewnętrzny —
korpus Składnica, słownik Morfeusz, wydanie takie a takie —
a olski żąda na to osobnego zdania.
Spójnika ta postać nie ma, więc od członu bez czasownika, który wszedł,
różni ją to, że nie ma czym jej wpuścić osobno
([subset.md](subset.md#what-it-does-not-cover-yet)).

**Cząstka `się` przed swoim czasownikiem.**
`Droga tej roli mieści się w pliku.` przechodzi,
`Cała droga tej roli w jednym pliku się mieści.` pada.
Gramatyka ma tę konstrukcję i zatrzymuje się przed polszczyzną:
`się` dostało jedną pozycję, tę po czasowniku,
a polszczyzna stawia je równie chętnie przed nim.
Wiersz `part` prowadzi z tego powodu
[kolejkę blokerów](corpus.md#where-the-analyses-stop) po interpunkcji.

**Cząstka `tylko` wewnątrz grupy imiennej.**
`Istnieją tylko te konstrukcje, które stoją na liście.` pada,
`Istnieją te konstrukcje, które stoją na liście.` przechodzi.
Pozycję wewnątrz grupy cząstka dostała
([subset.md](subset.md#cząstka-wchodzi-obu-gospodarzami-a-w-grupie-nie-nosi-etykiety)),
a `tylko` zostaje poza nią razem z całą swoją listą lematów,
bo Morfeusz czyta je także jako spójnik;
w tym rejestrze jest to cząstka określająca grupę imienną najczęściej.

**Czasownik rządzący dopełniaczem.**
`Ten kierunek nie potrzebuje gramatyki.` pada, `Gramatyki skład nie czyta.` przechodzi.
To jest walencja poza biernikiem widziana od strony pisania:
`potrzebować`, `żądać` i `brakować` są w tym rejestrze codzienne.

**Spójnik skorelowany.**
`Werdykt ani nie wnosi, ani nie zdejmuje.` pada,
`Werdykt nie wnosi i nie zdejmuje.` przechodzi.
Polszczyzna powtarza tu spójnik przed każdym członem
i przed drugim stawia przecinek,
a koordynacja olskiego bierze spójnik jeden i stawia go między członami.

**Słowo pytające poza `który`.**
`Pyta, czy go to dotyczy.` pada, `Pyta, który parser jest tani.` przechodzi.
Zdanie pytające i pytanie zależne mają w gramatyce kształt grupy pytajnej,
czyli zaimka przy rzeczowniku,
a `czy`, `co`, `jak` i `gdzie` żądają każde innego kształtu
([subset.md](subset.md#what-it-does-not-cover-yet)).
Dokument, który opisuje rolę czytelnika, pisze te zdania zdanie po zdaniu,
bo rola pyta, a pytanie jest jej definicją.

**Bezokolicznik pod słowem, które orzeka bez podmiotu.**
`To jest stan, którego warto pilnować.` pada,
`Trzeba czytać dokumenty.` przechodzi.
Predykatyw bierze bezokolicznik na swoim miejscu,
a nie bierze go tam, gdzie zdanie względne wysunęło przed niego dopełnienie.

**Angielska nazwa pisana małą literą.**
`README mówi o podzbiorze.` przechodzi,
a `Sekcja mówi o build w olski/subset.py.` pada na `build`.
Wersalik dostał czytanie nieodmienne
([subset.md](subset.md#wersalik-bez-czytania-jest-tym-samym-rzeczownikiem-nieodmiennym)),
a `build`, `merge` i `yet decided` zostają poza gramatyką,
bo pisane małą literą nie różnią się niczym od polskiego słowa,
którego słownik nie ma, a któremu czytania nieodmiennego dać nie wolno
([subset.md](subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)).
Dokumentacja przytacza je w cudzysłowie albo w backtickach,
a olski widzi sam napis.

**Drugi leksem do napisu, który słownik zna.**
`Linter sprawdza tekst.` przechodzi, `Cena lintera jest niska.` pada na `lintera`.
SGJP zna `linter` i daje mu dopełniacz `linteru`,
a ta proza odmienia go wedle drugiego leksemu.
Leksykon projektu takiego wiersza nie przyjmuje z powodu, który sam podaje,
a ruch trzyma [`TODO.md`](../TODO.md).

**Notacja z jednoliterowym członem.**
`docs/pisanie-po-olsku.md jest raportem.` przechodzi,
a `docs/pisanie-w-olskim.md jest raportem.` pada na `-`.
Notację tego rejestru olski bierze jako jeden rzeczownik nieodmienny
([subset.md](subset.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)),
a wzorzec pod tym nie przyjmuje członu z jednej litery,
więc nazwy pliku z `w` albo `i` w środku nie da się w olskim wymówić.
Ten dokument nazywa się tak, jak się nazywa, właśnie dlatego.
Tak samo pada flaga: `--readings` rozpada się na `-`, `-` i słowo.

## Co działało

`--readings` ze streszczeniem było w pierwszej sesji jedynym miejscem,
w którym werdykt mówił „dlaczego”,
i działało dokładnie tak, jak README obiecuje:
strzałka `„z dodatkami” → „przewyższa”, „koszt”` mówi, co wybrać ma czytelnik,
a nazwy roli mówią, co zdanie znaczy w każdym z czytań.
Diagnoza wieloznaczności zajmuje jedno spojrzenie.

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

## Cena, którą to zostawia w prozie

Pisanie pod olskiego popycha w cztery chwyty:
zdanie krótkie, kopułę z narzędnikiem, wyrażenie przyimkowe na czele zdania
i dopełnienie w rodzaju żeńskim.
Trzy pierwsze widać w README po przepisaniu,
a [reguły prozy](../CLAUDE.md#dla-kogo-jest-napisane-zdanie) każą unikać
jednego rytmu na wszystko.
Gramatyka nagradza więc rejestr, który reguły prozy karzą.

Napięcie to jest rachunkiem trzecim:
zdanie długie jest polszczyzną i ten rejestr pisze je stale,
więc płaci gramatyka, a płaci pozycjami z kolejki wyżej.
Za urwiskiem zdanie potyka się nie o jeden brak, tylko o kilka naraz,
więc pozycja z tej kolejki kupuje takie zdanie dopiero razem z resztą.
Skracanie zostaje radą dla piszącego dzisiaj, a nie kierunkiem dla gramatyki.

## Czego ten dokument nie mówi

Sesje są trzy, rejestr jeden, a wszystkie były sesjami agenta,
nie człowiekiem redagującym własny plik,
więc jest to raport, a nie pomiar.
Liczby z pierwszej sesji trzyma git:
zdania kandydujące stały w katalogu tymczasowym i nie weszły do repozytorium.
Liczby z dwóch pozostałych mają właścicieli, bo są nad tekstem,
który stoi w repozytorium:
ile zdań pliku się wyprowadza, drukuje `olski.check`,
a kolejkę blokerów i krzywą pokrycia po długości zdania — tę nad prozą i tę nad
bankiem drzew — drukuje `olski.coverage`
([corpus.md](corpus.md#the-same-queue-over-prose)).

Rachunku po stronie autora nie mierzy nic:
liczba przecinków poprawionych w jednym dokumencie jest liczbą przeczytań,
a nie przebiegu, i tak samo będzie z każdym następnym takim znaleziskiem.

Powtórzyć da się każdą parę zdań wyżej, przez `olski.check -c`,
i po to każda z nich stoi w tym dokumencie cała.
