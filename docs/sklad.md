# Skład: drzewo wchodzi, polskie zdanie wychodzi

Wchodzi drzewo tego, co ma zostać powiedziane, a wychodzi polskie zdanie,
a z kilku drzew postawionych obok siebie wychodzi tekst.
Ten dokument trzyma rozstrzygnięcia tego toru:
na jakim poziomie stoją kategorie zapisu,
co tekst wie ponad zdaniem,
i czego pod tym brakuje w leksykonie i w formach.

Etapy wraz z kryterium wyjścia trzyma
[roadmap.md](roadmap.md#tor-składu-drzewo-wchodzi-polskie-zdanie-wychodzi),
a tor gramatyczny, czyli ten sam podzbiór czytany w drugą stronę,
[design-notes.md](design-notes.md).
Dlaczego parser stoi tu świadkiem, a nie zależnością,
rozstrzyga [design-notes.md](design-notes.md#the-round-trip-invariant).

Generation inverts every difficulty in parsing.

Ambiguity is the parser's curse;
a generator never encounters it.
Agreement stops being a constraint to check
and becomes a value to compute.
Parsing `czarnego kota` means reconciling two syncretic feature bundles.
Generating it means calling `inflect(kot, acc.sg.m2)`
and getting one answer.

## Three architectures

**Correct by construction.**
The source is a typed abstract syntax tree,
with types encoding what agrees with what.
Ill-formed input fails to typecheck;
well-formed input compiles to text and cannot be wrong.
Strongest guarantee, worst ergonomics:
nobody wants to author prose as an AST.

**Write near-Polish and check it.**
The source looks like Polish and is parsed and validated.
Best ergonomics,
and it inherits every problem from the parsing angle,
plus the fact that chart parsers give famously bad error messages.
`parse failed at token 7` is not explainable.

**An unambiguous surface DSL.**
The source reads like Polish
but is designed to be parsed by something boring and deterministic,
because the notation is ours to control.
Lemmas plus explicit structural marks;
the compiler elaborates to an AST,
resolves agreement,
and linearizes.
Something in the spirit of:

```text
(zdanie
  podmiot: kot[m2]
  orzeczenie: widzieć[past]
  dopełnienie: mysz[pl])
→ Kot widział myszy.
```

The third option is the working preference among these three,
and the predictive-editor finding below partly rehabilitates the second.

What is built is none of them but a fourth,
because all three describe the sentence
where the fourth describes what the sentence is about,
and the ergonomic objection to the first therefore misses it:
[Czwarta architektura](#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
owns it.

## The predictive editor changes this

The controlled-language literature has a standard answer
to both the bad-diagnostics problem
and the habitability problem,
and it is not better error messages.
It is a **look-ahead editor**:
show the author, at each position,
which words and phrases the grammar permits next.
Then invalid text cannot be written,
so there is nothing to diagnose.

AceWiki does this for Attempto Controlled English.
For olski it would mean the checker's primary interface
is not a batch validator over a file
but an incremental one over a cursor position.
That is a substantially different program,
and it is the strongest argument found so far
for the second architecture over the third.

See [similar-work.md](similar-work.md#the-habitability-problem).

## Czwarta architektura: poziom dziedziny, a nie poziom języka

Trzy powyższe stoją na poziomie rozbioru zdania albo niżej,
i pierwsza z nich została odrzucona dokładnie za to:
prozy nikt nie chce pisać drzewem rozbioru.
Czwarta bierze drzewo, którego kategorie nie są kategoriami polszczyzny,
tylko kategoriami tego, o czym się mówi,
i zarzut wobec pierwszej jej nie dosięga.

Ten poziom jest tym, co Grammatical Framework nazywa składnią abstrakcyjną,
i tym, co ma się od niej wziąć.
Konstruktor mówi, że jedna rzecz jest określeniem drugiej,
a nie że stoi tam dopełniacz;
że czegoś jest wiele, a nie że rzeczownik ma liczbę mnogą.
Przypadek, rodzaj i formę liczy linearyzacja,
bo żadne z nich nie jest rzeczą, którą autor chce powiedzieć:
przypadek bierze się z pozycji, a rodzaj rzeczownika z leksykonu.

Jednoznaczności ten zapis nie musi sprawdzać, bo ją ma:
drzewo dobrze złożone jest jednoznaczne z definicji.
To zdejmuje przy okazji wieloznaczność, której sam worek słów nie odróżnia,
a która nad polszczyzną jest zwyczajna:
`parser podzbioru` i `podzbiór parsera` są dwoma różnymi drzewami,
choć stoją w nich te same lematy w tych samych rolach.

Buduje to `skład/`, a `skład/składnia.py` trzyma kategorie i konstruktory.
Zgodność jest tam liczona, a nie sprawdzana,
więc gramatyki podzbioru ten kierunek nie potrzebuje
([design-notes.md](design-notes.md#the-round-trip-invariant)).

Szyk to drzewo niesie, ale niesie go na jednym poziomie z dwóch.
Polszczyzna niesie szykiem temat i remat,
więc `Wejściem jest zwykły tekst polski.` i `Zwykły tekst polski jest wejściem.`
mówią to samo zdanie logiczne i co innego stawiają na czele,
a `Wyróżnienie` jest tą kategorią, z której oba wychodzą.
Kolejność słów jest z niej wnioskiem, a nie wariantem dopisanym do linearyzacji:
czasownik zostaje na miejscu, a przestawia się to, co stoi wokół niego.
Wewnątrz grupy imiennej takiej kategorii nie ma i jest to brak, a nie decyzja:
przymiotnik przed rzeczownikiem określa, a po rzeczowniku nazywa,
i dlatego README pisze `zwykły tekst polski`,
a kompilator z tego samego drzewa wypuszcza `zwykły polski tekst`.
Języki o szyku ustalonym tego wyboru nie mają,
więc biblioteka wzięta od kogoś, kto go nie miał, nie odpowie za nas.
Co ma go rozstrzygać wewnątrz grupy, nie zapadło, i trzyma to [`TODO.md`](../TODO.md).

## Tekst wie to, czego zdanie o sobie nie wie

Zdanie skompilowane osobno wypisuje każdą rzecz pełną nazwą
i stawia ją w czasie, w którym stoi samo.
Tekst wie dwie rzeczy więcej i obie zmieniają to, co wychodzi,
więc `skład.opowieść` stoi nad `skład.składnia`, a nie obok.

Pierwszą jest czas.
Opowieść mówi o tym, co się stało, i mówi tak o wszystkich swoich zdarzeniach,
więc czas przeszły jest własnością opowiadania, a nie któregokolwiek z nich.
To samo drzewo opowiedziane jako to, co się dzieje, dałoby czas teraźniejszy,
i dlatego czasu nie ma w drzewie, tylko w kontekście, w którym drzewo się wypisuje.

Drugą jest tożsamość.
Podmiot powtarzany zdanie po zdaniu czyta się źle,
a polszczyzna ma na to sposób zwykły i tani: opuszcza go,
bo osobę, liczbę i rodzaj niesie sam czasownik.
Żeby go opuścić, trzeba wiedzieć, że dwa wystąpienia lematu są tą samą rzeczą,
a tego jedno drzewo nie ma czym powiedzieć.
Niesie to `Postać`, a rozstrzyga o tym zmienna, którą jej nadano:
dwa razy napisany `R.bazyliszek` jest dwoma bazyliszkami,
a dwa razy użyta jedna `Postać` jest jednym.
Tożsamość jest więc deklaracją autora, a nie wnioskiem ze słownika synonimów,
i widać to w tej samej opowieści na drugim określeniu:
`bazyliszek` i `potwór` są dla tego kompilatora dwiema rzeczami.

Opuszczenie jest wąskie i jest wąskie z tego samego powodu,
dla którego po drugiej stronie stoi kryterium jednego czytania:
opuszczenie, po którym zdanie czyta się dwojako, nie jest oszczędnością.
Warunki trzyma `pomijalny` w `skład/składnia.py`,
a nie akapit, bo o to samo pyta ciąg zdarzeń wewnątrz jednego zdania,
i jeden z nich jest tu wart powtórzenia,
bo mówi, czym ta ostrożność się mierzy.
Po opuszczonym podmiocie zostaje forma czasownika i nic poza nią,
więc podmiot wraca stamtąd tylko wtedy,
gdy nikt inny tej samej formy z tego czasownika nie wyciąga.
Kufer stojący w piwnicy nie odbiera córce krawca niczego, bo rodzaj ma inny,
a skrzynia odbiera jej rodzaj żeński i wtedy podmiot staje wypisany.
Liczy się to tym czasownikiem, który podmiotu nie wypisze,
bo różnice, których on nie robi, nie są różnicami dla czytelnika:
czas przeszły rozdziela rodzaje, a teraźniejszy nie rozdziela żadnego.

## Zdanie podrzędne jest tu wskazaniem rzeczy

Podrzędność jest miejscem, w którym ten zapis mógł rozjechać się
z poziomem, na którym stoi.
Zdanie w zdaniu jest kategorią składni, a nie dziedziny,
i kategoria o takiej nazwie ściągnęłaby cały ten tor
na trzecią architekturę [powyżej](#three-architectures),
czyli na rozbiór zdania pisany z góry.

Kategorią, która z tego wyszła, jest wskazywanie.
`Jaki` wskazuje rzecz cechą, `Opis` w `skład/składnia.py` wskazuje ją zdarzeniem,
a pytanie jest w obu wypadkach jedno i jest pytaniem o rzecz:
o którą z nich mowa.
`kamienne postaci` i `kamienne postaci, których nikt nie liczył`
wskazują więc tak samo i różnią się tym, czym wskazują,
a nie tym, że do drugiego doczepiono zdanie.
Że wychodzi z tego przydawka zdaniowa wraz z zaimkiem względnym i dwoma przecinkami,
rozstrzyga linearyzacja, tak samo jak rozstrzyga przypadek.

Miejsce, które w zdaniu podrzędnym zostaje zaimkiem, nie jest zapisane.
Autor pisze rzecz raz i stawia tę samą zmienną w zdaniu, które ją wskazuje,
czyli robi to, co robi z `Postać` [powyżej](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie):
tam ta sama zmienna dwa razy jest jedną rzeczą w dwóch zdaniach,
a tutaj jest jedną rzeczą w zdaniu nadrzędnym i podrzędnym naraz.
Mechanizm jest ten sam co przy opuszczaniu podmiotu i stoi w jednym miejscu:
`Kontekst` niesie to, czego wypisywane drzewo o sobie nie wie,
a jedna funkcja rozstrzyga, czy rola wychodzi nazwą, czy zaimkiem.

Co ta kategoria kupuje poza rytmem, widać na przypadku tego zaimka.
`których nikt nie liczył` stoi w dopełniaczu,
bo w zdaniu podrzędnym stoi na pozycji dopełnienia czasownika zaprzeczonego,
a rodzaj i liczbę bierze z rzeczy, która stoi w zdaniu nadrzędnym.
Dopełniacz negacji sięga więc zaimka tak samo, jak sięgnąłby rzeczy postawionej tam,
i nie ma na to w kompilatorze osobnej gałęzi.
Autor nie pisze przy tym ani przypadka, ani rodzaju, ani zaimka,
ani tego, że zdanie podrzędne otwiera się nim niezależnie od roli, którą on w nim ma.

Reszta zdania złożonego wychodzi z trzech innych kategorii:
[okoliczności wyrażonej zdarzeniem](#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie),
[dopełnienia wyrażonego zdarzeniem](#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie)
oraz [następstwa](#następstwo-zdarzeń-jest-kategorią-a-spójnik-jego-wnioskiem).

Jedna granica leży przy tym w środku samej kategorii.
Wskazana rzecz musi stać w zdaniu podrzędnym na pozycji, z której wyjdzie na czoło,
czyli sama albo pod przyimkiem, a nie pod grupą imienną,
więc `kot, którego ogon goni mysz` jest zdaniem polskim, którego stąd nie ma.
Zgłasza się ono przy budowaniu drzewa, i to jest tu jedyna obrona,
bo zaimek zostawiony w środku zdania podrzędnego wyszedłby tekstem,
którego nikt nie chciał napisać.

## Okoliczność nie pyta, czy stoi pod nią rzecz, czy zdarzenie

Podrzędność, która rzeczy nie wskazuje, dochodzi do tego zapisu
kategorią, którą on już ma, a nie kategorią nową.
Okolicznik niesie relację i to, co pod nią stoi,
a stanąć może rzecz albo zdarzenie, bo pytanie stawia się jedno:
`w nocy` i `gdy zgasła świeca` odpowiadają, kiedy.

Różnica między nimi jest różnicą w polszczyźnie, a nie w drzewie,
i cała siedzi w słowie, którym relacja wychodzi na wierzch.
Przed rzeczą stoi przyimek, który rządzi przypadkiem,
i bierze go z `skład/przyimki.py`;
przed zdarzeniem stoi spójnik, który nie rządzi niczym,
bo zdanie podrzędne rozdaje przypadki własne,
więc `skład/spójniki.py` mówi o nim mniej: to, w jakiej stoi relacji.
Tyle jednak wystarcza, żeby `Kiedy.bo` się zgłosiło,
i jest to ta sama odmowa, którą tamten plik wydaje na `Skąd.do`.
Świadka ten leksykon ma przy tym pełniejszego niż tamten:
SGJP odróżnia spójnik podrzędny od współrzędnego,
więc `i` dopisane do tej tabeli zgłasza się w teście, a nie w tekście.

Słowa tego bywa zero, i nie jest to trzeci rodzaj okoliczności.
Narzędzie polszczyzna wyraża samym narzędnikiem,
a czas wyraża i tak, i tak: `wieczorem` obok `w nocy`.
Zapis idzie za tym i nie dokłada nic:
`Czym(R.lustro)` oraz `Kiedy(R.wieczór)` wołają przestrzeń nazw relacji,
a `Kiedy.w(R.noc)` sięga w niej po słowo,
więc relacja bez przyimka nie ma osobnej funkcji ani osobnej kategorii.
Wpis w `skład/przyimki.py` stoi tam mimo to, bo przypadek trzeba skądś wziąć,
a takie pary są jedynymi, których słownik nie ma czym potwierdzić:
świadkiem jest znakowanie przyimka, a przyimka tam nie ma.

Skutek jest w tym leksykonie odwrotnością przyczyny i mówi to samo,
a różni się tym, przy którym zdarzeniu stoi:
`bo` wprowadza zdanie o tym, skąd się wzięło to, przy czym stoi,
a `więc` zdanie o tym, co z niego wyszło.
Wybór między nimi jest wyborem głowy i widać go w tekście,
bo głowa wypada pierwsza:
`Wzrok potwora zamieniał ludzi w kamień, więc mieszczanie zabili okna deskami.`
opowiada zdarzenia w kolejności, w której zaszły, a to samo napisane przez `bo`
opowiada je od końca.
Nazwy pytania ta relacja przy tym nie ma i nazywa się relacją,
bo polszczyzna pytania o skutek jednym słowem nie ma;
tyle jest w tej konwencji nazw, ile jest w niej pytań.

Wysunięcie takiej okoliczności na czoło jest zwykłym `Wyróżnienie`,
więc `Gdy bazyliszek otworzył oczy, czeladnik zasłonił twarz lustrem.`
i to samo zdanie z okolicznością na końcu
są jednym drzewem z jednym znacznikiem różnicy,
a nie dwoma wariantami linearyzacji.
Wysunąć się jednak nie da wszystkiego i rozstrzyga o tym leksykon,
bo jest to fakt o słowie:
`Ponieważ zgasła świeca, córka krawca nie wróciła.` jest zdaniem polskim,
a to samo zdanie z `bo` na czele nie jest,
choć oba te spójniki stoją w jednej relacji.
Jest to jedyne miejsce w tym pakiecie, w którym leksykon mówi o kolejności,
i jedyna jego kolumna bez świadka w słowniku,
bo SGJP nie odróżnia tych dwóch słów niczym.

Przecinek zaś jest przez to własnością konstytuenta, a nie znakiem w napisie.
Zdanie podrzędne oddziela się nim z każdej strony, przy której coś stoi,
więc konstytuent nie wie o swoich przecinkach tego, co o nich rozstrzyga,
i wiedzieć nie może: rozstrzyga o nich sąsiad.
`linearyzuj` zwraca przez to `Kawałek`, czyli napis wraz z żądaniami,
a jedna funkcja te żądania spełnia i stawia jeden przecinek tam,
gdzie dwóch sąsiadów zażądało go naraz.
Krańce zdania nie spełniają żadnego, i to zdejmuje dwa warunki:
kropka nie staje po przecinku, a lista nie dostaje dwóch.
Bez tego pola przecinek jedzie w napisie, a każde miejsce,
które po konstytuencie coś stawia — a jest ich trzy — czyta go z ogona tego napisu.

## Dopełnienie nie pyta, czy stoi pod nim rzecz, czy zdarzenie

To samo, co [okolicznik](#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie)
robi z okolicznością, dopełnienie robi z uczestnikiem zdarzenia.
`Czeladnik zaczął pracę.` i `Czeladnik zaczął pracować.`
odpowiadają, co zaczął, i różnią się tym, czy zaczął rzecz, czy zdarzenie,
a nie tym, że do drugiego doczepiono zdanie.
Że wychodzi z tego raz biernik, a raz bezokolicznik bez podmiotu,
rozstrzyga linearyzacja, tak samo jak rozstrzyga przypadek.

Wykonawca jest tu tym, czego bezokolicznik o sobie nie mówi,
i dlatego stoi w drzewie, a nie w formie.
Autor pisze tę samą zmienną dwa razy, raz przy czasowniku i raz pod nim,
czyli robi to, co robi przy `Postać` i przy `Opis`,
a konstruktor zdania o czynności — `Robi` w `skład/składnia.py` —
sprawdza, że są to te same obiekty.
Zapisu na to poza zmienną nie ma i nie ma być:
znacznik postawiony przy bezokoliczniku mówiłby o zdaniu,
a to drzewo mówi o tym, kto co robi.

Podmiot nie staje przez to w takim zdaniu nigdy,
i jest to drugi powód, dla którego podmiotu w tekście bywa nie widać.
Pierwszym jest forma czasownika, z której czytelnik go odzyskuje
([wyżej](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)),
i tamten warunek mierzy się tym, co po opuszczeniu zostaje.
Tu nie zostaje nic, bo bezokolicznik nie niesie ani osoby, ani rodzaju,
więc tamten warunek odpowiada odmownie zawsze, a podmiot i tak nie staje.
Dwa powody spotykają się w jednym miejscu — `_podmiot` w `skład/składnia.py` —
i to jest wszystko, co je łączy.

Odmów jest przy tej pozycji dwie i każda broni przed czym innym.
Pierwsza jest leksykonu i broni przed czasownikiem, który bezokolicznika nie bierze.
Waży ona więcej niż ta sama odmowa przy bierniku,
bo bezokolicznik nie zgadza się z niczym:
drzewo, które postawiło go przy `zamykać`, wychodzi tekstem zgodnym gramatycznie
i nieistniejącym — `Kot zamyka spać.` —
a leksykon jest jedynym świadkiem, jakiego ta pozycja ma.
Druga jest drzewa i broni przed cudzym wykonawcą.
`Czeladnik chciał, żeby córka krawca wróciła.` jest zdaniem polskim,
którego bezokolicznik nie wyraża,
więc drzewo żądające go dla cudzego zdarzenia nie ma wyjść tekstem,
w którym wróciłby czeladnik.
Tego, że pytanie o kontrolę pada raz, nie zawdzięcza przy tym drzewo sobie:
[Walenty rozdziela kontrolę](subset.md#leksykon-mówi-dwa-zdania-na-lemat-i-bierze-je-z-walentego),
więc `chcieć` bezokolicznik dostaje, a `kazać` nie dostaje go wcale,
bo jego wykonawca stoi w celowniku, którego ta gramatyka nie ma.

Przeczenie sięga przez tę pozycję o piętro niżej i nie ma na to gałęzi.
`Nie chciał wynieść lustra.` przeczy raz, przy czasowniku osobowym,
a przypadek zmienia się przy bezokoliczniku,
więc `Kontekst` niesie przeczenie w dół tak samo, jak niesie wykonawcę.
Jest to ten sam dopełniacz negacji, który
[sięga zaimka względnego](#zdanie-podrzędne-jest-tu-wskazaniem-rzeczy),
i tam, i tu policzony w jednym miejscu.

Granica tej kategorii leży tam, gdzie granica wskazywania, i z innego powodu.
`lustro, które chciał wynieść` jest zdaniem polskim, którego stąd nie ma,
bo rzecz wskazana stoi w bezokoliczniku, czyli o dwa piętra od czoła,
a `Opis` schodzi po nią jedno.
Zgłasza się to przy budowaniu drzewa, jak każda z tych granic.

## Następstwo zdarzeń jest kategorią, a spójnik jego wnioskiem

`Ciąg` w `skład/składnia.py` bierze kilka zdarzeń i wypuszcza jedno zdanie,
a kategorią dziedziny jest w nim następstwo:
jedno stało się po drugim i jest to jedna rzecz do opowiedzenia.
Węższe to jest niż polskie `i`, które łączy także zdarzenia równoczesne,
i węższe z rozmysłu, bo kolejność zdarzeń niesie tu kolejność zapisu.

Koordynacją bytów piętro wyżej to nie jest,
i widać to na tym, czego żąda opuszczenie podmiotu.
Byty stoją w jednej roli i żaden nie ma czasownika,
a zdarzenia mają go po jednym, więc drugie z nich podmiotu nie powtarza.
Rozstrzyga o tym ten sam `pomijalny`,
który rozstrzyga o tym [między zdaniami](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie),
bo pytanie jest jedno: czy czytelnik odzyska podmiot, którego nie ma.
Wspólna zostaje im interpunkcja, bo listę obie piszą tak samo,
i stoi ona w jednym miejscu z tego właśnie powodu.

## Najpierw tekst, potem drzewo, na końcu biblioteka

Kolejność, w której powstał `opowieści/bazyliszek.py`, była odwrotna do zwykłej.
Najpierw stanął polski tekst, który miał wyjść,
potem drzewa, z których miał wyjść, a dopiero po nich to,
czego tym drzewom w bibliotece brakowało.
Kolejka konstrukcji wzięła się więc z tekstu, a nie z listy spisanej z góry,
i wyszło z niej co innego, niż wyszłoby z README:
opowieść żąda czasu przeszłego, przeczenia i okoliczników miejsca,
a README, które stoi w czasie teraźniejszym, nie żąda żadnej z tych rzeczy.

Kosztu ta kolejność ma tyle, że tekst wybrany pod kompilator
mówi o kompilatorze mniej niż tekst, którego nikt pod niego nie pisał,
i dlatego kryterium wyjścia toru zostaje przy README
([roadmap.md](roadmap.md#kryterium-wyjścia-toru-składu-to-znów-readme)).
Zysk jest za to natychmiastowy:
tekst napisany pod jedną legendę mieści się w jednym pliku i w jednej sesji,
a każda rzecz, której z niego nie dało się wypuścić,
jest brakiem pokazanym na zdaniu zamiast wyliczonym w planie.

## Lepszy tekst żąda czego innego niż dłuższy

Ta legenda przechodzi ten cykl kilka razy i za każdym nie po to,
żeby stanęło w niej więcej zdań,
tylko po to, żeby była opowieścią, a nie ciągiem zdań o jednym temacie.
Kolejkę ustawia więc to, czego opowieści brakuje jako opowieści,
i wychodzi z tego co innego, niż wyszłoby z listy konstrukcji.
Pierwszym takim żądaniem jest zakończenie, które nie mówi, o czym opowieść była,
i to żądanie stoi w [fiction.md](fiction.md#narrative) wprost,
razem z drugim, które to samo zakończenie spełnia: nie wypada ono dobrze.
Obok niego stoi powód, dla którego ktoś schodzi do piwnicy,
a ten jest rozstrzygnięciem tej opowieści, a nie pozycją z tamtego katalogu.
Najbliżej stoi tam [płaskie wnętrze postaci](fiction.md#scene-and-character),
czyli usterka o tym, czego postać nie ma, a nie o tym, czego nie robi.

Oba prowadzą do jednego, i to jest tu ustalenie:
powód i puenta, która nie podsumowuje, żądają zdania podrzędnego.
Zdanie, które nie streszcza, musi coś pokazać,
a rzecz pokazana bez podsumowania jest rzeczą, którą trzeba wskazać,
i tego jedno zdanie proste nie robi.
Wyszedł z tego `Opis` [powyżej](#zdanie-podrzędne-jest-tu-wskazaniem-rzeczy),
czyli kategoria dziedziny w miejscu, w którym
[roadmap.md](roadmap.md#etap-5-konstrukcje-których-żąda-readme) trzymała podrzędność,
i pokrywa on z niej tyle, ile podrzędność wskazuje rzecz, a nie więcej.

Drugie ustalenie jest ciekawsze, bo kolejka nie została w tej warstwie.
Zaimek względny wychodził z morfologii jako `któren`,
czyli forma, którą SGJP odsyła do gwary,
więc nowa konstrukcja składniowa zażądała kryterium wyboru formy,
stojącego pod nią o dwie warstwy niżej
([kwalifikator](#kwalifikator-mówi-o-formie-dwie-rzeczy-i-tylko-jedna-jest-rejestrem)).
Plan tego tak nie ustawia i nie ma jak ustawić:
roadmapa trzyma wybór formy jako etap 3, a podrzędność jako część etapu 5,
i wywód za tą kolejnością się nie zmienia.
Tekst nie czyta jednak numeracji i płaci od razu za wszystko,
czego wymaga zdanie, które ma z niego wyjść.

Trzecie żądanie jest o rytm i stoi w tamtym katalogu wprost.
[Jednostajność](fiction.md#sentence-and-paragraph) — zdania jednej długości,
jeden kształt zdania powtórzony przez cały tekst — jest tam usterką wymienianą
jako właściwość prozy modelowej, a opowieść złożona z samych zdań prostych ma ją całą.
Zdanie długie nie powstaje jednak z dwóch krótkich postawionych obok siebie:
potrzebne jest to, co je łączy, i stąd wzięły się
[następstwo](#następstwo-zdarzeń-jest-kategorią-a-spójnik-jego-wnioskiem)
wraz z [okolicznością wyrażoną zdarzeniem](#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie).
Bez nich `Podniosła deskę i zeszła po schodach.` rozpada się na dwa zdania,
a przyczyna, którą niesie `bo`, zostaje czytelnikowi do wyciągnięcia
z dwóch zdań postawionych obok siebie i niepołączonych niczym.

Czwarte przyszło stamtąd, gdzie pierwsze: z warstwy pod tą, którą się ruszało.
Zdanie podrzędne wstawia przed podmiot cudzy podmiot,
więc `Gdy bazyliszek otworzył oczy, zasłonił twarz lustrem.`
mówi, że twarz zasłonił bazyliszek.
Ten sam podmiot w zdaniu obok jako jedyny warunek nie wystarcza,
i pokazuje to zdanie złożone, choć nie jest to warunek o zdaniu złożonym.
Warunek, który stoi tam zamiast niego, mierzy to, co po opuszczonym podmiocie zostaje,
czyli formę czasownika ([wyżej](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)),
i sięga tak samo zdania obok:
skrzynia postawiona w piwnicy zamiast kufra odbiera córce krawca opuszczenie,
choć stoi w zdaniu podrzędnym, którego opowieść jest o czym innym.

Piąte jest po prostu tanie.
Trzy relacje okolicznikowe dopisały się bez namysłu,
bo `w nocy`, `po schodach` i `wśród kamiennych postaci` są tym,
czym opowieść odmierza czas i ruch, a nie nową kategorią.
Jedna z nich niesie przy tym coś poza sobą:
`w nocy` stoi w tym samym przypadku co `w piwnicy`,
więc jest wpisem, po którym w tekście nie zmienia się nic,
i pokazuje, że relacja nazywa to, co autor powiedział,
a nie to, w czym mu to wyjdzie.

Szóste wróciło do usterki, którą pierwsze zaczęło, i nie dało się nią załatwić.
Postać, która czegoś chce, ma wnętrze, a postać, która coś robi, ma tylko czynność,
i tego zdanie podrzędne nie kupuje:
`Opis` mówi, o którą rzecz chodzi, a nie czego ta rzecz chce.
Kupuje to [dopełnienie wyrażone zdarzeniem](#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
i legenda żąda go dwa razy w dwóch różnych rolach.
Raz jest powodem: córka krawca chce wynieść kufer,
i to zdanie stoi teraz przed świecą, bo powód wyprzedza czynność.
Raz jest kontrastem: nikt nie chce zejść do piwnicy, a czeladnik chce,
i tyle wystarcza, żeby o czeladniku nie mówić, jaki jest,
czyli żeby nie napisać zdania, którym
[fiction.md](fiction.md#sentence-and-paragraph) nazywa nazwanie emocji zamiast pokazania jej.
Poza tym echem to samo żądanie zdjęło z opowieści jedno zdanie o niczym:
zamiast `Nikt nie zszedł po schodach.` stoi w niej miasto, które stoi na ulicy.

Zapłaciło za to warstwą, którą pierwsze żądanie już raz odsłoniło,
i to jest tu ustaleniem, bo dwa razy pod rząd nie jest zbiegiem.
Bezokolicznik nie zgadza się z niczym, więc kategoria dziedziny postawiona wysoko
zażądała czytania cudzego słownika o dwie warstwy niżej,
tak jak wskazywanie rzeczy zażądało kryterium wyboru formy.
Tym razem czytanie jest o kontroli, a nie o kształcie frazy,
bo `chcieć` i `kazać` biorą w polszczyźnie ten sam bezokolicznik
i wskazują nim dwóch różnych ludzi.
Wyszło z tego coś, czego niezmiennik obiegu nie zapowiadał:
plik leksykonu jest wspólny, a zdanie, które on mówi, czyta na razie jeden kierunek.
Parser zmierzył to zawężenie i nie kupiło mu ono ani jednej jednoznaczności,
a składowi jest jedyną obroną, jaką ta pozycja ma;
liczby trzyma [subset.md](subset.md#leksykon-mówi-dwa-zdania-na-lemat-i-bierze-je-z-walentego).

Siódme jest o czasie i kosztowało jeden wpis w leksykonie przyimków.
Opowieść nie mówiła, ile go mija między zejściem dziewczyny a zejściem czeladnika,
więc miasto stało przed kamienicą w tej samej chwili, w której gasła świeca.
Trzy pory dnia zdejmują to bez żadnej kategorii nowej —
noc, ranek i wieczór — a wieczór jest tym, który zażądał czegoś od zapisu:
polszczyzna mówi `wieczorem` samym narzędnikiem, bez przyimka.
Wyszło z tego zniesienie osobnej funkcji na narzędzie:
relacja bez słowa jest wywołaniem swojej przestrzeni nazw
([wyżej](#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie)),
więc `Czym(R.lustro)` i `Kiedy(R.wieczór)` piszą się jednym kształtem,
a dwie funkcje na jedną kategorię nie powstały.

Jedno żądanie z tego przebiegu nie zostało spełnione,
a cena, którą pokazało, jest tu ustaleniem osobnym.
Opowieść wypisuje rzecz pełną nazwą tam, gdzie polszczyzna napisałaby zaimek,
i widać to na `wzroku potwora` postawionym dwa razy.
Zaimek osobowy w roli innej niż podmiot ma jednak warunek
ostrzejszy niż opuszczenie podmiotu:
zaimek niesie rodzaj i liczbę, a nie osobę,
więc blokuje go każda rzecz stojąca obok o tej samej formie zaimka,
a takich rzeczy jest w tej legendzie tyle, że pozycja zwalnia się prawie nigdzie.
Drugą połową ceny jest szyk, i to ona jest tu nowa:
`Chciał ją znaleźć.` stawia zaimek przed czasownikiem osobowym,
czyli poza zdaniem, do którego on należy,
więc zaimek i bezokolicznik są jedną zmianą, a nie dwiema stojącymi obok siebie.
Ruch trzyma [TODO.md](../TODO.md), a `jego wzrok` jest przy tym trzecią rzeczą:
zaimek dzierżawczy przestawia grupę imienną, a nie wypełnia pozycję w zdaniu.

## Checks that are cheap, deterministic, and explainable

All finite-domain, all effectively linear time,
all able to say why they failed:

- Noun-phrase-internal agreement,
  adjective and determiner against noun,
  on case, number, and gender
- Subject-verb agreement on person and number,
  and on gender in the past tense and conditional
- Verbal government:
  `używać` demands genitive,
  so `używam komputera` and not `używam komputer`
- Prepositional government,
  each preposition licensing a fixed set of cases
- Genitive of negation,
  applied as a rewrite during linearization
  so that it is automatic rather than checked
- Aspect and tense legality:
  `będę zrobił` is unconstructible,
  and perfective present is future
- Gender resolution under coordination:
  `Jan i Maria przyszli`, never `przyszły`
- Clitic and `się` placement

Every failure should report two feature bundles and their provenance,
along the lines of
*`czarna` is nom.sg.f, `kota` is acc.sg.m2,
mismatch on case and gender, from lines 3 and 4*.
That is a diagnostic a human can act on,
and it is the thing a language model structurally cannot provide:
it cannot say which rule fired,
and it will not give the same answer twice.

## Morphology generation is the underestimated piece

Analysis maps a form to tags.
Generation maps a lemma plus tags to a form.
The compiler needs the second,
and Polish inflection carries enough irregularity,
stem alternation,
and paradigm classes
that hand-writing it is a multi-year detour.

Morfeusz 2 exposes generation over SGJP,
whose 2020 edition characterizes nearly 456,000 Polish lexemes,
and both are distributed under a liberal BSD licence.
That one dependency is the difference
between a weekend-scale core and a years-scale one,
which is why the open lexicon is a settled decision.

## Leksykon projektu: SGJP nie zna słów, których używa rejestr

Słownik pod spodem nie zastępuje pisania w dwóch miejscach.
Nie ma słów, które rejestr techniczny tworzy sam — `komit`, `olski`, `lintować`
dostają `ign`, czyli nie mają czego wypuścić.
I nie ma leksemów, które ten rejestr dokłada do napisów znanych:
projekt piszący o agentach jako o programach żąda liczby mnogiej `agenty`,
a `agenty`, które SGJP wydaje, jest formą deprecjatywną leksemu osobowego,
czyli tym, czym mówi się o ludziach z góry, a nie liczbą mnogą rzeczy nieżywotnej.
Wpis takiego leksykonu nazywa więc leksem wraz z odmianą,
a nie sam napis dopisany do listy słów.

Rozróżnianie leksemów jest przy tym pytaniem, które słownik już zadaje
i na które sam odpowiada wszędzie tam, gdzie leksemy rozdzielił.
`zamek:Sm3~a` i `zamek:Sm3~u` to dwa leksemy różniące się dopełniaczem,
a `Włochy:Sn_pt~szech` i `Włochy:Sn_pt~chach` to kraj i dzielnica Warszawy,
różniące się miejscownikiem.
Ten identyfikator czyta jeden kierunek:
synteza pyta o niego przez `skład/leksemy.py`
([niżej](#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)),
a `olski/morph.py` ucina go przy analizie.
Kwalifikator słownik niesie tym samym polem, a czyta go jeden kierunek:
`POZA_REJESTREM` w `skład/morfologia.py` odsiewa nim formy przed syntezą,
a analiza wyrzuca go razem z resztą pól,
więc `projekta` oznaczone jako `daw.` ze składu nie wyjdzie, a do parsera wejdzie.
Brak słowa, rozdzielony leksem i przeczytany kwalifikator
widać naraz, nad `pl.sgjp.sgjp-2026.06.01`:

```sh
python3 -c "
import morfeusz2
morf = morfeusz2.Morfeusz()
for lemat in ('projekt', 'zamek', 'komit'):
    for forma, leksem, tag, _, kwalifikatory in morf.generate(lemat):
        if 'pl:nom' in tag or 'sg:gen' in tag or tag == 'ign':
            print(forma, leksem, tag, kwalifikatory)
"
```

Leksykon projektu jest plikiem, który czyta to repozytorium,
a nie słownikiem dołożonym Morfeuszowi, i decyduje o tym cena wejścia.
Morfeusz przyjmuje słownik własny przez `dict_path`,
ale przyjmuje go skompilowanego,
a pakiet z PyPI wydaje bibliotekę wraz z wiązaniem do Pythona i nic poza tym,
co widać po zawartości katalogu, w który się instaluje,
więc tamta droga żąda łańcucha narzędzi spoza PyPI
i zabiera to, co [`CLAUDE.md`](../CLAUDE.md#checks) ma za instalację jednym poleceniem.
Plik czytany przez oba kierunki kupuje przy tym to samo,
co kupuje [leksykon walencyjny](subset.md#walencja-jest-leksykonem-o-ramie-domyślnej):
że `komit` jest słowem raz, a nie dwa razy.

Czym wpis ma być, nie zapadło.
Wypisanie form kosztuje pisanie i nie ma jak się pomylić;
wskazanie leksemu, wedle którego wpis się odmienia,
kosztuje jedno pole i łamie się tam, gdzie temat alternuje,
bo `plik` ma w miejscowniku `pliku`, a temat zakończony na `t` bierze tam `cie`.
Trzyma to [`TODO.md`](../TODO.md).

## Kwalifikator mówi o formie dwie rzeczy i tylko jedna jest rejestrem

Kwalifikator jest jedynym kryterium wyboru formy,
które w danych stoi gotowe i nie żąda niczego poza przestaniem go wyrzucać.
Co za tym stoi, widać na dwóch słowach, których obu żąda opowieść o bazyliszku,
i widać na nich od razu, że kryterium nie jest jedno.

Bez odsiania wychodzi polszczyzna, której nikt nie pisze.
Zaimek względny rodzaju męskiego wychodził jako `któren`,
oznaczone w SGJP jako `daw._dziś_gwar.`,
a przeszła forma `zgasnąć` jako `zgasnęła`, oznaczone jako `rzad.`
Obie stoją w słowniku przed formą zwykłą,
więc kompilator brał je nie dlatego, że coś rozstrzygnął, tylko dlatego, że nie pytał.

Po odsianiu każdego kwalifikatora naraz wychodzi polszczyzna o innym znaczeniu.
SGJP rozdziela `oko` na dwa leksemy i temu o liczbie mnogiej `oczy`
daje kwalifikator `anat.`, a temu o liczbie mnogiej `oka` nie daje żadnego,
więc kryterium bez podziału zamieniłoby zdanie legendy
`Bazyliszek otworzył oczy.` na `Bazyliszek otworzył oka.`,
czyli na oczka w sieci albo w rosole.
Nazwa dziedziny nie odsyła tu formy poza rejestr, tylko mówi, w którym znaczeniu
leksem tak się odmienia, i jest to zupełnie inne zdanie o tej samej formie.

Podział jest więc rozstrzygnięciem, a nie odczytem, i stoi w `POZA_REJESTREM`.
Nazwy, które w słowniku występują, wypisuje polecenie
nad listą lematów, którą to repozytorium już ma:

```sh
python3 -c "
import collections, morfeusz2
morf = morfeusz2.Morfeusz(generate=True, expand_tags=False)
lematy = [w.split()[0] for w in open('olski/leksykon.txt') if not w.startswith('#')]
nazwy = collections.Counter(
    nazwa
    for lemat in lematy
    for *_, kwalifikatory in morf.generate(lemat)
    for napis in kwalifikatory
    for nazwa in napis.split(',')
)
for nazwa, ile in nazwy.most_common():
    print(ile, nazwa)
"
```

Zasięg tego polecenia jest zasięgiem tamtej listy, czyli czasownikami,
i to jest jedyna słabość tego wywodu:
`anat.`, `mors.` oraz `daw._dziś_gwar.` wychodzą dopiero na rzeczownikach,
więc lista nazw jest sumą dwóch przebiegów, a nie wyjściem jednego polecenia.
Nazwa, której żaden przebieg nie pokazał, przechodzi jak nazwa dziedziny,
i to ten podział kosztuje.
Odwrotny domyślny kosztowałby więcej, bo formę odsianą przez pomyłkę
widać dopiero wtedy, gdy jej brak wywali całą komórkę paradygmatu.

## Nazwę leksemu wybiera autor, bo lemat go nie wskazuje

Kwalifikator jest kryterium, które w danych stoi gotowe.
Leksem jest kryterium, którego w danych nie ma:
identyfikator słownik niesie, a które z dwóch znaczeń autor miał na myśli,
mówi tylko autor.

Że wybiera go autor, a nie cecha, widać na dwóch parach naraz.
`oko` rozdziela się na leksem zbiorowy i niezbiorowy,
a różnicę tę niesie tag, bo `oczy` mają cechę `col`, a `oka` `ncol`,
więc dałoby się je rozróżnić żądaniem cechy, tak jak żąda się przypadka.
`Włochy` rozdzielają się na kraj i dzielnicę Warszawy,
a tag obu jest w miejscowniku ten sam, `subst:pl:loc:n:pt`,
i różni je wyłącznie identyfikator.
Kryterium cechowe pokryłoby więc pierwszą parę i nie tknęłoby drugiej,
a leksem pokrywa obie.

Drugą połową ustalenia jest to, że w drzewie stoi nazwa, a nie identyfikator.
Poziomem kategorii tego pakietu jest
[dziedzina](#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka),
a kod paradygmatu jest napisem z wnętrza słownika innego projektu,
więc drzewo pisze `R.oko_w_rosole`,
a z identyfikatorem wiąże tę nazwę `skład/leksemy.py`.
Wiązanie jest wiele do jednego z założenia:
oczko w sieci i oko w rosole to jeden leksem i dwie rzeczy, o których się pisze,
więc nazw jest tyle, ile rzeczy, a nie tyle, ile leksemów.
Nazwa goła jest wpisem tego samego rodzaju:
`oko` znaczy w tym repozytorium oko, a nie oczko,
i tyle wystarcza, żeby legenda otwierała bazyliszkowi oczy
bez wpisu przy każdym użyciu.

Kiedy wpis jest potrzebny, rozstrzyga zgoda leksemów, a nie ich liczba.
`dziób` ma dwa leksemy, z których jeden słownik odsyła do żeglarstwa,
i oba mają w dopełniaczu `dzioba`,
więc pytanie o dopełniacz ma odpowiedź, pod którą oba podpisują się naraz.
`oko` w liczbie mnogiej odpowiedzi wspólnej nie ma,
i wtedy `odmień` zgłasza `WieleLeksemów` wraz z formami, które z każdego wychodzą,
bo autor rozstrzyga między znaczeniami i widzi je po tym, co z nich wyjdzie.

Najdroższy przypadek nie jest przy tym rzeczownikiem:
`stać` ma leksem niedokonany i dokonany,
a forma dokonana w czasie teraźniejszym jest w polszczyźnie przyszła,
więc milczenie wypuszczałoby stąd zdanie o tym, co będzie,
zamiast zdania o tym, co jest.

Tym samym kryterium schodzi rodzaj, który jest wartością, a nie formą:
`potwór` ma leksem zwierzęcy oraz osobowo-zwierzęcy,
więc zwierzę jest tym, pod czym podpisują się oba,
a wybór alfabetyczny dałby tu osobę.

Ceną tego kryterium jest cisza w miejscu, o które nikt nie pytał:
leksemy różniące się poza żądaną komórką przechodzą bez zgłoszenia,
bo pytanie brzmi „która forma”, a nie „który leksem”.
Otwarte zostaje to, na co to kryterium nie sięga,
i jest to słownik mówiący „albo tak, albo tak” pod jednym leksemem:
`postaci` obok `postacie` w jednej komórce
oraz `anioł` z rodzajem wypisanym dwiema wartościami w jednym tagu.
Identyfikator nie rozstrzyga ani jednego, ani drugiego, i trzyma to
[`TODO.md`](../TODO.md).

Leksykon ten jest przy tym innym plikiem niż
[leksykon projektu](#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr),
bo odpowiada na inne pytanie:
tamten dokłada leksem, którego słownik nie ma, a ten wybiera z tych, które ma.

Po stronie analizy nie zmienia się nic i jest to rozstrzygnięcie, a nie zaległość.
Identyfikatora nie potrzebuje tam nic:
`Rosół ma oka.` i `Bazyliszek ma oczy.` wyprowadzają się po jednym czytaniu,
a reguły o zbiorowość nie pytają.
Leksem wpuszczony do czytania sięgnąłby za to każdego szukania po lemacie,
czyli leksykonu walencyjnego i `KOPULA` w `olski/subset.py`,
i każde z nich musiałoby powiedzieć, którą połowę identyfikatora dopasowuje.
Wchodzi on tam wtedy, gdy będzie reguła, która tożsamości leksemu zażąda.
Kryterium, które po tamtej stronie już stoi, jest innego rodzaju i nie zastępuje tego:
[`admissible`](subset.md#the-dictionary-offers-readings-polish-does-not)
wyrzuca czytanie, którego polszczyzna nie ma,
a tutaj oba czytania polszczyzna ma i różnią się tym, o czym mówią.
