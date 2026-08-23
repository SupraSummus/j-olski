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

Planem to nie jest.
Właścicielem ruchu jest [`TODO.md`](../TODO.md),
kolejności [`roadmap.md`](roadmap.md),
a ceny wpuszczenia konstrukcji
[`subset.md`](subset.md#what-the-grammar-covers);
tu stoi tylko materiał, którego te trzy dokumenty nie miały skąd wziąć.

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

## Jedna konstrukcja nie rusza liczby nad zdaniem długim

Druga sesja wpuściła do gramatyki cztery pozycje,
a jedna z nich stała najwyżej na liście niżej.
Liczba zdań wyprowadzonych w `roles.md` nie ruszyła się przez to ani o jedno,
choć nad całą polską prozą tego repozytorium przybyło ich przeszło pięćdziesiąt,
a nad bankiem drzew przeszło dwieście.
O ten rozjazd rozstrzyga długość zdania, a nie gramatyka.

Zdanie o dwudziestu wyrazach ma kilka zatrzymań naraz,
a wyprowadza się dopiero wtedy, gdy zamkną się wszystkie.
Pozycja dopisana do gramatyki zdejmuje jedno z nich
i zostawia zdanie odrzucone, tylko dalej,
więc pokrycie nad dokumentem pisanym normalną polszczyzną nie rośnie wcale,
choćby ta pozycja była tą, której temu dokumentowi brakowało najbardziej.
Krzywą pokrycia po długości zdania trzyma
[corpus.md](corpus.md#the-measurement) i mówi ona to samo od drugiej strony:
pokrycie spada z urwiska między dziesiątym a dwudziestym tokenem.
Nad prozą tego repozytorium urwisko leży w tym samym miejscu,
a `roles.md` pisze zdania długie, więc leży za nim.

To samo zasłanianie widać o szczebel wyżej, na cenie pozycji.
Sonda różnicowa wycenia pozycję, zdejmując ją z gramatyki,
więc wycenia ją wobec wszystkiego, co w gramatyce zostaje:
przecinek zamykający zdanie podrzędne kupił nad bankiem drzew kilkadziesiąt zdań
obok przydawki imiesłowowej, a bez niej kupiłby pojedyncze,
bo zdanie potrzebujące obu potyka się o tę, której nie ma
([subset.md](subset.md#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
Cena pozycji nie jest przez to liczbą, którą raz się zapisuje,
a dwie pozycje wpuszczone razem bywają warte więcej niż z osobna.

Dla kogoś, kto olskiego używa przy pisaniu, wynika z tego jedna rada.
Liczba pokrycia nad własnym dokumentem nie jest sygnałem,
dopóki zdania tego dokumentu są długie:
stoi w miejscu przy każdej poprawce w gramatyce i nic o niej nie mówi.
Sygnałem jest zatrzymanie, bo ono się rusza,
i po to `--zatrzymania` pokazuje je wszystkie nad jednym zdaniem,
a `olski.coverage` nad całym plikiem układa je w kolejkę
([corpus.md](corpus.md#the-same-queue-over-prose)).
Zdanie krótkie ma odwrotnie: jedno zatrzymanie, jedną poprawkę i widoczny skutek,
czego pierwsza sesja doświadczyła nad README, gdzie zdania są krótkie.
Która proza gdzie leży, drukuje krzywa nad plikiem.

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

**Liczebnik w orzeczniku.**
`Tory są dwa.` pada, `Torów jest dwa.` też,
a `Działają dwie rzeczy.` przechodzi.
Grupa liczebnikowa jest wpuszczona jako podmiot i jako dopełnienie,
a zdanie, które mówi, ile czegoś jest, dalej nie wychodzi.

**Apozycja z nazwą.**
`Bank drzew Składnica mierzy gramatykę.` pada,
`Składnica jest bankiem drzew.` przechodzi.
Rejestr techniczny nazywa tak każdy artefakt zewnętrzny —
korpus Składnica, słownik Morfeusz, wydanie takie a takie —
a olski żąda na to osobnego zdania.
[Dopowiedzenie z `czyli`](subset.md#what-it-does-not-cover-yet) jest tym samym brakiem
w drugiej postaci, a spójnik ten stoi już między dwoma zdaniami,
więc dopowiedzenie zostało samo.

**Człon bez czasownika po `a nie`.**
`Zgodność jest parsowaniem, a nie sprawdzeniem po nim.` pada,
`Zgodność jest parsowaniem.` przechodzi.
Brak stoi na liście i jest tam wyceniony jako jedna konstrukcja,
a w tym rejestrze jest chwytem na co drugie zdanie,
bo tak właśnie dokumentuje się podzbiór: przez to, czego w nim nie ma.
Elipsa czasownika w drugim członie — `a drugie podmiot opuszczony` — pada tak samo.

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
Gramatyka nagradza więc rejestr, który reguły prozy karzą,
i jest to napięcie do rozstrzygnięcia gdzie indziej niż tutaj.

Piąty chwyt widać dopiero z drugiego fotela i jest nim sama długość.
Zdanie za urwiskiem nie wyprowadza się prawie nigdy,
więc olski postawiony przy pisaniu popycha ku zdaniu krótkiemu
nie przez to, czego nie ma w gramatyce,
tylko przez to, że długie zdanie ma zatrzymań kilka.
Skracanie jest tu naprawą tańszą od każdej pozycji w gramatyce
i tym różni się rada dla piszącego od kolejki dla gramatyki.

## Czego ten dokument nie mówi

Sesje są dwie, rejestr jeden, a obie były sesjami agenta,
nie człowiekiem redagującym własny plik,
więc jest to raport, a nie pomiar.
Liczby z pierwszej sesji trzyma git:
zdania kandydujące stały w katalogu tymczasowym i nie weszły do repozytorium.
Liczby z drugiej mają właścicieli, bo są nad tekstem, który stoi w repozytorium:
ile zdań pliku się wyprowadza, drukuje `olski.check`,
a kolejkę blokerów i krzywą pokrycia po długości zdania — tę nad prozą i tę nad
bankiem drzew — drukuje `olski.coverage`
([corpus.md](corpus.md#the-same-queue-over-prose)).

Powtórzyć da się każdą parę zdań wyżej, przez `olski.check -c`,
i po to każda z nich stoi w tym dokumencie cała.
