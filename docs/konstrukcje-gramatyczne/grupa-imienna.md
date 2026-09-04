# Grupa imienna, liczebnikowa i przymiotnikowa

Jeden plik rejestru konstrukcji, w którym sekcja przypada na konstrukcję.
Cena i zakup stoją w niej rzędem wielkości albo granicą.
Co ten rejestr obiecuje i który plik czytać, mówi [wstęp](README.md).

## Nothing above a coordination distributes into it

A coordination is one **conjunct**, a conjunction, and the rest,
and the grammar's symbols are named for it:
`człon_imienny` is a noun phrase with no coordination in it,
`grupa_imienna` is one that may have.
`grupa_imienna` is also where a relative clause attaches,
for a reason that has nothing to do with coordination
([podrzędność.md](podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)).
An adjective attaches inside a conjunct and never above the coordination,
so `nowe programy i pliki` is `[nowe programy] i [pliki]`
and never `nowe [programy i pliki]`.
That is a narrowing rather than a reading of Polish,
and what it buys is an agreement that can still fail.

A coordination has no gender of its own,
so an adjective scoping over the coordination
would be an adjective agreeing with nothing
and `nowa programy i pliki` would derive.
Refusing the wider attachment is what keeps that a rejection.

Wywód ten obowiązuje tam, gdzie obowiązuje zgodność.
Okolicznik wyrażony zdaniem dochodzi do całego ciągu zdań składowych,
bo nie zgadza się z niczym ani pod członem, ani nad ciągiem,
więc brak rodzaju u ciągu nic mu nie odbiera,
a czytania są dwa i oba polszczyzna ma
([podrzędność.md](podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).
Zawężenie zostaje przez to przy przydawce, czyli przy tym, co je uzasadnia.
Wyrażenie przyimkowe przyłącza się do całego ciągu z tego samego powodu,
z którego przyłącza się do niego okolicznik:
`pliki i katalogi w tym drzewie` mówi o obu członach,
gdzie to samo wyrażenie pod członem ostatnim mówi o samych katalogach,
a polszczyzna ma oba czytania, więc gramatyka ma oba ciała
([subset.md](../subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).
Ciąg przymiotnikowy dostaje tę pozycję tak samo,
choć zgodność niesie przez cały siebie:
wyrażenie przyimkowe żadnej cechy nie zmienia, więc zasięg zostaje dwojaki.

Pozycję tę zapisuje ciało ze spójnikiem,
a nie produkcja `grupa_imienna → grupa_imienna wyrażenie_przyimkowe`.
O zasięgu obie mówiłyby to samo.
Różni je liczba czytań: produkcja rekurencyjna dokłada drugie wyprowadzenie
każdej grupie bez koordynacji, a werdykt nie ma czym go odróżnić od pierwszego,
bo obu daje tego samego gospodarza.
Spójnik w ciele jest tym, co jedno od drugiego odróżnia,
więc ciała są dwa, po jednym na spójnik i na przecinek,
i tak samo dwa są nad ciągiem przymiotnikowym.

Ciąg dłuższy niż dwuczłonowy ma tę pozycję na każdym swoim poziomie,
bo ogonem ciągu jest `grupa_imienna`:
`A i B i C w drzewie` czyta wyrażenie przy samym `C`, przy `B i C`
oraz przy całej trójce, po jednym wyprowadzeniu na zasięg i bez nawiasowań ponad to.

Pozycja ta kosztowała mniej, niż zapowiadał precedens okolicznika zdaniowego.
Nad bankiem drzew nie rusza ani jednego werdyktu,
i tak samo pod morfologią złotą, jak pod żywą:
zdań przyjętych nie ubywa i nie przybywa.
Przebieg pod morfologią złotą mówi ponadto to, czego tamten nie liczy:
zgodność z drzewem wzorcowym zostaje ta sama,
a złote czytanie ocala się w tylu zdaniach wieloznacznych, w ilu ocalało przedtem.
Rusza się w nim jedno zdanie i nie werdyktem, tylko głębokością:
złote czytanie schodzi w nim poniżej granicy z `MAX_READINGS`.
Nad prozą tego repozytorium pozycja dokłada czytanie kilku zdaniom
już wieloznacznym i nie odbiera jednoznaczności żadnemu,
a czytania te są tymi, które polszczyzna nad nimi ma:
`Braki w leksykonie i braki w formach wylicza docs/roadmap.md.`
czyta odtąd `w formach` także przy obu brakach.
Kto chce liczby dzisiejszej, puszcza polecenia z
[corpus.md](../corpus.md#fetching-it).

Dwa symbole zamiast jednego wybrano dla liczby czytań, a nie dla parsera.
Tablica Earleya bierze rekursję lewostronną,
co pilnuje test w `tests/test_gramatyka.py`,
więc `grupa_imienna → grupa_imienna conj grupa_imienna`
dałoby się tu wpisać jedną produkcją w miejsce dwóch.
Powiedziałoby ono o zasięgu dokładnie to samo, bo zawężenie wyżej stoi na rodzaju,
którego ciąg nie ma, a nie na kształcie produkcji —
i wypuszczałoby ciąg tyloma wyprowadzeniami, ilu on nawiasowań dopuszcza:
ciąg trzech członów dwoma, czterech pięcioma, a siedmiu stu trzydziestoma dwoma,
gdzie te dwa symbole wypuszczają każdy z nich raz.
Są to wyprowadzenia jednej struktury, więc gramatyka płaciłaby tu tym,
czym płaci [gramatyka kategorialna](../parsowanie.md#kierunek-produkcja-się-rozwarstwia-a-podłoże-zostaje):
wieloznacznością pozorną, którą trzeba potem kwotować postacią normalną.
Ciąg siedmiu członów nie jest przy tym przypadkiem z brzegu:
tyle ma wyliczenie z rejestru ustaw, nad którym olski liczy czytań najwięcej
([ustawy.md](../ustawy.md#wieloznaczność-jest-tu-odczytem-z--6-ale-nie-jest-zarzutem)),
i tamta liczba mówi, ile taki mnożnik znaczy przy zdaniu,
które wieloznaczność ma już z innego powodu.

## Przydawka koordynuje się i rozdziela rzeczownik tylko za nim

Przymiotniki przy jednym rzeczowniku polszczyzna spina spójnikiem i przecinkiem,
a wychodzą z tego dwie różne rzeczy.
Ciąg zgodny orzeka o jednej rzeczy kilka cech naraz:
`warstwy nowe i tanie` są warstwami, które są nowe i zarazem tanie.
Ciąg rozdzielny dzieli rzeczownik między swoje człony:
`warstwy trzecia i czwarta` są dwiema warstwami, a nie jedną.
Pierwszy stoi w obu szykach przydawki, drugi tylko za rzeczownikiem.

```sh
python3 -m olski.check --readings --zatrzymania -c "Nowy i tani parser zapisuje ustawienia.
Warstwy trzecia i czwarta pracują.
Warstwy trzecia, czwarta i piąta pracują.
Nowy i tania parser zapisuje ustawienia."
```

```text
<text>: Nowy i tani parser zapisuje ustawienia.
        - podmiot: Nowy i tani parser, dopełnienie: ustawienia, orzeczenie: zapisuje
<text>: Warstwy trzecia i czwarta pracują.
        - podmiot: Warstwy trzecia i czwarta, orzeczenie: pracują
<text>: Warstwy trzecia, czwarta i piąta pracują.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
<text>: Nowy i tania parser zapisuje ustawienia.
        brak odczytania: analiza staje na „zapisuje”
```

Para symboli jest tu ta sama, którą ma grupa imienna i przymiotnikowa:
`przydawka` jest ciągiem, a `człon_przydawki` jednym członem,
i wybrano ją dla liczby czytań, tak samo jak tam
([wyżej](#nothing-above-a-coordination-distributes-into-it)).

Ciąg rozdzielny wypuszcza liczbę mnogą wartością, a nie zmienną wspólną z członem,
bo mnogi jest ciąg, a każdy przymiotnik w nim pojedynczy;
tym samym chwytem stoi koordynacja imienna i grupa liczebnikowa
([niżej](#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)).
Z ciągiem zgodnym się nie miesza, bo `warstwy nowe i trzecia i czwarta`
łączyłoby przydawkę orzekającą o wszystkich warstwach z dwiema, które je dzielą.

Przed rzeczownikiem ciąg rozdzielny nie staje, bo polszczyzna go tam nie stawia:
`trzecia i czwarta warstwy` nią nie jest, choć `warstwy trzecia i czwarta` jest.
Zatrzymuje go cecha, bo oba ciała są jednym symbolem.
Warunek nie rusza werdyktu ani jednego zdania Składnicy 180723
pod żadną z dwóch morfologii, a odbiera `Trzecia i czwarta warstwy pracują.`
czytanie, którego polszczyzna nie ma;
samego zdania nie odrzuca, bo wyprowadza się ono ciągiem imiennym.

Ciała są trzy — po jednym na znak koordynacji i trzecie na rozdział —
a cena każdego z nich jest osobną liczbą, wziętą sondą różnicową (`harness/ruch.py`).
Nad tym bankiem pod złotą morfologią czytanie dostaje kilkadziesiąt zdań,
z których blisko połowa wychodzi jednoznaczna,
a jednoznaczność traci kilka zdań przyjętych;
pod Morfeuszem zakup jest tego samego rzędu, a cena o zdanie wyższa.
Nad prozą tego repozytorium czytanie dostaje garść zdań, jedno traci jednoznaczność,
a nad README nie rusza się ani jedno
([roadmap.md](../roadmap.md#readme-jest-przyrządem-pomiarowym)).
Ciało spójnikowe i przecinkowe kupują po kilkadziesiąt zdań,
a rozdzielne pojedyncze i nie odbiera jednoznaczności żadnemu.
Zgodność ról sprzedaje ciało przecinkowe i ono jedno:
nie mniej niż co piąte zdanie nowo przez nie przyjęte
olski czyta inaczej, niż czyta je bank drzew
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)),
a zdania nowo przyjęte przez ciało spójnikowe zgadzają się z bankiem co do jednego.

Ciała przecinkowego rodzina rozdzielna nie ma, bo jej ogonem jest ciąg zgodny
w liczbie pojedynczej i rozdział pada w takim ciągu raz,
więc `Warstwy trzecia, czwarta i piąta pracują.` jest odrzucone,
choć polszczyzna trzeci człon pisze właśnie przecinkiem;
ile to ciało kosztuje, trzyma `todo/`.

## Wyrażenie przyimkowe koordynuje się tak jak grupa imienna

`Leksykon mówi o bierniku i o bezokoliczniku.`,
`Program zapisuje ustawienia w pliku i w katalogu.`
Poziom jest piąty, obok zdania, grupy imiennej, grupy przymiotnikowej i przydawki.
Bez tego poziomu przyimek pada w takim napisie raz — `o bierniku i bezokoliczniku` —
a jest to jedno wyrażenie z ciągiem imiennym w środku,
czyli inna konstrukcja i inny napis.

Symbole są tu trzy, a nie dwa jak na poziomach obok.
Człon i ciąg nad nim wybrano dla liczby czytań, tak samo jak przy grupie imiennej
([wyżej](#nothing-above-a-coordination-distributes-into-it)).
Trzeci jest rolą i stoi nad ciągiem, bo rolą jest cały napis:
ogon ciągu pod nazwą roli wychodziłby w werdykcie drugim wyborem przyłączenia,
a wybór jest tu jeden i czytanie już go nazwało.

Przypadka ciąg nie wypuszcza, bo rządzi nim przyimek stojący w każdym członie
z osobna, więc człony pod różnymi przyimkami stoją w jednym ciągu —
`w Belgii i na Malcie` — i tym ten poziom różni się od czterech pozostałych,
które zgodności właśnie żądają.

Przyłączenie zostaje przy tym wyborem czytelnika, tak samo jak przy wyrażeniu
pojedynczym: `Program zapisuje ustawienia w pliku i w katalogu.` ma dwa czytania,
bo cały ciąg dochodzi i do czasownika, i do dopełnienia
([subset.md](../subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)).

**Spinacze są dwa i rozchodzą się rejestrem.**
Nad polską prozą tego repozytorium spójnik wyciąga z odrzucenia kilkanaście zdań,
a przecinek jedno; nad bankiem drzew jest odwrotnie,
a zakup obu razem jest tam kilkakrotnie większy.
Jednoznaczności nie traci nad tą prozą ani jedno zdanie,
a nad bankiem drzew jedno, i odbiera mu ją przecinek.
Z tych, które przecinek nowo przyjmuje pod złotą morfologią,
przeszło dwie trzecie czyta role tak, jak czyta je drzewo wzorcowe,
a reszta nie ma tam roli do porównania albo ma ją częściowo.
Jedno zdanie olski czyta inaczej niż bank drzew i przyjmuje je spójnik:
`W Tokio, Sydney i w Londynie rekordy spodziewane są dopiero dzisiaj.`

Przecinek bierze zarazem zawężenie: `Działa w Polsce, w okolicach Kielc.`
mówi o jednym miejscu, a nie o dwóch, i jest to apozycja, której olski nie ma.
Zamiana ta nie jest tu nowa i nie jest tu do naprawienia:
ciąg imienny robi ją tak samo, a wpis o apozycji trzyma
`todo/`.

**Skład tego poziomu nie ma i mówi to wprost.**
`olski/skład/rozbiór.py` schodzi przez ciąg i człon do przyimka,
a ciąg o kilku członach zgłasza brakiem kategorii,
bo okoliczność mówi w tamtym zapisie o jednej relacji i o jednej rzeczy
([kategorie-zapisu.md](../kategorie-zapisu.md#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie)).
Gałąź ta jest ceną, którą tamten kierunek płaci za każdy nowy poziom gramatyki,
i płaci ją niezależnie od tego, czy sam ten poziom umie powiedzieć.

## Zaimek rzeczowny nie rządzi dopełniaczem

Morfeusz daje formom paradygmatu `ten` czytanie rzeczownikowe obok
przymiotnikowego: `tego` jest dopełniaczem przymiotnika `ten`
i dopełniaczem zaimka `to`, a `tym` narzędnikiem jednego i drugiego.
Produkcja, która daje głowie grupy imiennej dopełniacz po niej,
bierze oba: `parser tego podzbioru` jest przymiotnikiem przy rzeczowniku,
a drugi raz zaimkiem, który rządzi rzeczownikiem.
Te dwa drzewa mają różny kształt,
więc [są dwoma odczytaniami](../subset.md#co-się-liczy-jako-jedno-odczytanie),
a nie jednym jak para lematów.
Bez warunku niżej `Celem jest parser tego podzbioru.` wychodzi dwoma czytaniami
o identycznym streszczeniu ról.

Drugiego z nich polszczyzna nie ma.
Zaimek rzeczowny stoi za przyimkiem i przy czasowniku — `do tego`, `tego nie wiem` —
a dopełniacza po sobie nie bierze.
Warunek obejmuje więc każdą głowę, która rządzi dopełniaczem,
i mówi tyle: taka głowa nie jest zaimkiem rzeczownym.
W grupie imiennej produkcji z nią jest cztery,
bo pod głową może stać jeszcze przymiotnik, wyrażenie przyimkowe albo jedno i drugie.
Dwie następne są w [grupie, którą polszczyzna wysuwa przed zdanie względne
razem z zaimkiem](podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka):
przydawką dopełniaczową jest tam sam zaimek względny,
więc bez warunku `Polszczyzna, której nikt nie napisał, jest podzbiorem.`
wychodzi drugim czytaniem, w którym `której nikt` jest taką grupą.
Gdzie indziej czytanie zostaje, bo gdzie indziej jest tym, czym w polszczyźnie jest.

Paradygmat `ten` jest częścią tej klasy, a nie całą klasą.
`nikt`, `kto`, `nic`, `coś` i `ktoś` mają u Morfeusza czytanie jedno
i jest ono rzeczownikowe,
więc pod nimi nie stoją dwa czytania tej samej formy,
a mimo to produkcja z dopełniaczem po głowie bierze je za głowę:
bez warunku `Wtedy nikt nas nie zauważy.` wychodzi drugim czytaniem,
w którym `nikt nas` jest grupą imienną.
Przy paradygmacie `ten` takie czytanie zdejmuje także złota morfologia,
bo anotator wybiera jedno czytanie formy.
Tutaj wybierać nie ma z czego, więc czytanie zostaje po obu morfologiach,
a warunek jest jedynym miejscem, w którym ono ginie.

Wpisem na tej liście jest lemat, bo zaimka od rzeczownika nie rozdziela w słowniku
ani znacznik, ani cecha, ani kwalifikator.
Lista jest przez to zamknięta i starzeje się o każdy zaimek,
którego nikt do niej nie dopisze.
Starzenie kosztuje wieloznaczność, a nie zdanie odrzucone:
lemat dopisany odbiera czytanie i żadnego nie dodaje.

Jest to pierwszy warunek ujemny w tej gramatyce i lemat jest tym,
na czym wolno go postawić.
Cechy takiego warunku mieć nie mogą:
unifikacja jest przecięciem, a przecięcie negacji nie zna,
więc żądanie „nie bądź w narzędniku” nie jest żądaniem,
które da się postawić środowisku cech.
Lemat leży poza unifikacją, bo jest osobnym testem w `bierze`
z `olski/grammar.py`, więc negacja jest tam tym samym testem odwróconym.
Symetria jest zatem z `lemmas`, a nie z cechami,
i to samo rozstrzygnęło, czym jest klasa domyślna
[leksykonu walencyjnego](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej):
bierze ona każdą formę, której lematów leksykon nie wymienia,
i jest to drugi warunek ujemny, jaki ta gramatyka stawia.

Te dwa warunki różnią się zasięgiem.
Wykluczenie zaimka mówi „tym słowem nie bądź”, więc pyta o jedno czytanie formy;
klasa domyślna mówi „tą formą nie bądź”, więc pyta o wszystkie jej lematy naraz.
Klasa domyślna bez tego zasięgu przepuszcza formę, którą miała zatrzymać,
a co jej tą drogą przeszło, mówi
[sekcja o leksykonie](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej).
Wykluczenia leksykalne zostają przy czytaniu, bo o czytaniu mówią.
Czytanie i forma nie są tym samym słowem:
`nie` jest u Morfeusza cząstką `nie` i formą `on`,
`lecz` spójnikiem i rozkaźnikiem od `leczyć`,
a `pnie` grupą imienną od `pień` obok formy od `piąć`.
Pomiar tej różnicy nie widzi:
zamiana ich wszystkich na zasięg formy
nie rusza nad Składnicą ani jednego zdania pod żadną morfologią.
Zobaczy ją pierwsze wykluczenie, które taką formę trafi,
bo zasięg formy odbierze jej czytanie, o którym to wykluczenie nic nie mówi.

Warunek i kupuje, i płaci, a pomiar mówi ile.
Nad Składnicą pod Morfeuszem
[podnosi on liczbę zdań przyjętych](../corpus.md#what-morphological-ambiguity-costs)
o kilkadziesiąt, a odrzuca kilka.
Pod złotą morfologią widać obie strony tej wymiany:
kilka zdań przechodzi z wieloznacznych na przyjęte i każde z nich zgadza się
z drzewem wzorcowym, a kilku warunek zabiera jedyne czytanie, jakie miały,
i były to czytania, którym drzewo wzorcowe przeczyło albo których nie potwierdzało.
Każde z tych zdań stało na jednej frazie, której polszczyzna nie ma —
`to` z dopełniaczem pod sobą tam, gdzie tym dopełniaczem rządzi czasownik —
i tamten dokument jedno z nich cytuje.
Liczby dzisiejsze wydają dwa przebiegi `harness.pomiar`, z warunkiem i bez niego:
sonda różnicowa zdejmuje produkcje, a to jest warunek w terminalu.

Rozłożona na produkcje cena wypada po obu stronach inaczej.
W grupie imiennej warunek coś znaczy w każdym z czterech ciał:
zdjęty z dwóch, pod których głową stoi jeszcze przymiotnik,
oddaje pod morfologią żywą wieloznaczność
`Wprowadźmy do tego trupiego świata poprawkę.`
i podwaja liczbę czytań kilku dłuższym zdaniom banku drzew,
a pod złotą nie rusza tam nic.
W dwóch produkcjach wysunięcia nie rusza nad Składnicą liczby czytań
ani jednego zdania pod żadną z dwóch morfologii,
więc jest w nich z wywodu, a wywód jest ten sam:
przydawka dopełniaczowa jest w obu miejscach tą samą przydawką.

## Grupa liczebnikowa zgadza się tym, czego nie ma w środku

Liczebnik przyłącza się w polszczyźnie dwoma sposobami
i który to sposób, mówi tag, a nie kontekst:
Morfeusz oznacza `dwie` jako `num:pl:nom.acc.voc:f:congr`,
a `pięć` jako `num:pl:nom.acc.voc:m2.m3.f.n:rec`,
czyli nazywa jeden zgodnym, a drugi rządzącym.
Liczebnik zgodny jest przy rzeczowniku tym, czym przymiotnik przed nim,
i zgadza się z nim w przypadku, liczbie i rodzaju:
`dwie rzeczy`, `cztery wozy`, `oba pliki`.
Liczebnik rządzący wymaga dopełniacza mnogiego,
tak jak wymaga go rzeczownik z dopełniaczem pod głową:
`pięć kobiet`, `kilka dni`, `piętnastu członków`.
Produkcje są więc dwie, a nie jedna z warunkiem w środku,
bo te dwa przyłączenia dzielą tylko nazwę części mowy.

Grupa, którą buduje liczebnik rządzący, zgadza się czymś, czego nie ma pod nią:
`Pięć kobiet przyszło.` żąda czasownika w liczbie pojedynczej i rodzaju nijakim,
choć `kobiet` jest mnogie i żeńskie,
więc liczba i rodzaj są w tej produkcji wypisane wartością.
Cecha wypisana wartością nie jest tu nowa:
[ciąg współrzędny](#nothing-above-a-coordination-distributes-into-it)
ogłasza liczbę mnogą i trzecią osobę tak samo, niezależnie od swoich członów.
Nowe jest to, czemu ta wartość przeczy.
Ciąg jest mnogi, bo dwie rzeczy są dwiema rzeczami,
a `pięć kobiet` jest pojedyncze i nijakie wbrew każdemu słowu w środku,
więc rodzaj nijaki nie opisuje tu niczego prócz zgodności, której polszczyzna żąda.
Rodzaj przechodzi natomiast z liczebnika na dopełniacz,
bo rodzaj męskoosobowy ma w polszczyźnie własną formę liczebnika:
`Pięciu mężczyzn przyszło.` wyprowadza się, a `Pięć mężczyzn przyszło.` nie.
Liczebnik zbiorowy wchodzi tą samą produkcją i nie kosztuje ani jednej pozycji,
bo `dwoje` jest dla Morfeusza liczebnikiem rządzącym
i różni się od `dwa` samą wartością cechy `collectivity`.

Do drabiny [kosztów](../design-notes.md#the-cost-ladder) taka cecha nic nie dokłada,
bo jest cechą skończoną jak każda inna,
więc grupa liczebnikowa mieści się na szczeblu 0 razem z resztą gramatyki.
Liczebnik płaci więc nie formalizmem, a
[drugą walutą](../design-notes.md#the-second-currency-ambiguity), czyli czytaniami.
Liczebnik rządzący jest synkretyczny między mianownikiem i biernikiem,
więc zdanie z grupą liczebnikową obok drugiej grupy synkretycznej
wychodzi dwoma czytaniami: `Rada gminy liczy piętnastu członków.` czyta się
i tak, że rada liczy członków, i tak, że członkowie liczą radę.
Polszczyzna ma oba te czytania, więc olski to zdanie odrzuca i odrzuca słusznie.
Drugą taką parę czytań daje sam słownik:
`więcej` i `najwięcej` Morfeusz zna jako liczebniki obok przysłówka `dużo`,
więc `otrzymał więcej głosów` wychodzi i grupą liczebnikową, i okolicznikiem,
a te dwa czytania polszczyzna ma tak samo.

### Liczebnik złożony przyłącza się wedle ostatniego członu

`Dwadzieścia dwa chleby leżą.` odmienia się wedle `dwa`,
a `Dwadzieścia siedem chlebów leży.` wedle `siedem`,
czyli wedle tego z dwóch przyłączeń wyżej, które niesie człon skrajnie prawy.
Dwa liczebniki obok siebie są więc łańcuchem o głowie po prawej,
a nie trzecim przyłączeniem ani warunkiem w środku tamtych dwóch:
symbol `Liczebnik` bierze `accommodability` od swojej głowy,
a oba tamte ciała pytają go tym samym, czym pytały terminala.
Łańcuch jest osobnym ciałem, bo sonda wycenia go zdejmowaniem ciał.

Przypadek, liczba i rodzaj są w łańcuchu wspólne wszystkim członom,
bo polszczyzna odmienia każdy z nich:
`Dwudziestu dwóch mężczyzn przyszło.` stawia w mianowniku oba człony,
a `dwadzieścia dwóch` nie jest niczym.
Łańcuch wiąże w prawo, więc `sto dwadzieścia dwa` ma jedno nawiasowanie.

Ostatniego członu `jeden` łańcuch nie bierze.
`Dwadzieścia jeden chlebów` żąda dopełniacza mnogiego,
choć `jeden chleb` żąda zgodności,
czyli ten człon rządzi w łańcuchu inaczej, niż rządzi sam.
Osobne ciało na `jeden` po liczebniku kupiłoby liczby zakończone na jeden,
więc wejdzie dopiero wtedy, gdy takich zdań naliczy się więcej niż garść.

Płaci łańcuch drugą walutą i płaci w dwóch miejscach.
Pierwsze z nich zdejmuje warunek ujemny.
Morfeusz daje `pięć` drugie czytanie — dopełniacz mnogi rzeczownika
odczasownikowego od `piąć` — a rzeczownik odczasownikowy jest
[głową grupy imiennej](#rzeczownik-odczasownikowy-jest-głową-grupy-imiennej-a-nie-pozycją-przy-czasowniku),
więc bez warunku `Dwadzieścia pięć chlebów leży.` wychodzi dwoma czytaniami:
łańcuchem oraz `dwadzieścia` nad grupą, której głową jest `pięć`.
Drugiego polszczyzna nie ma, a kolizja bierze co dziesiątą liczbę pisaną słowem,
bo tyle kończy się na pięć,
więc terminal rzeczownika odczasownikowego tego lematu nie bierze.
Jest to znowu warunek ujemny na lemacie, ten sam ruch co
[przy rozdzielającym `a`](zdanie-złożone.md#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru).
Zabiera on cały leksem, bo negacji unifikacja nie zna,
więc `Pięcie jest trudne.` przestaje się wyprowadzać,
a skreślenie jednego argumentu oddaje to zdanie z powrotem.

Drugie miejsce zostaje i jest nim zagnieżdżenie.
Grupa, którą buduje liczebnik zgodny, jest dopełniaczem mnogim tak samo jak sam
rzeczownik — `brakuje dwóch mężczyzn` — więc ciało rządzące bierze ją nad sobą
i `Dwudziestu dwóch mężczyzn przyszło.` czyta się dwojako:
o dwudziestu dwóch oraz o dwudziestu z dwóch.
Drugie czytanie polszczyzna pisze przyimkiem, którego w tym zdaniu nie ma,
a cechy dzisiejsze tych dwóch nie odróżniają:
liczebnik zgodny wypuszcza grupę o cechach samego rzeczownika,
więc różni je sam kształt.

Zagnieżdżenie zachodzi tam, gdzie pierwszy człon jest synkretyczny
między rządzącym i zgodnym, czyli w formach męskoosobowych i przypadkach zależnych.
`Dwadzieścia dwa chleby leżą.` wychodzi jednym czytaniem.
Przed tą pozycją zdanie o dwudziestu dwóch przechodziło pod samym zagnieżdżeniem,
więc łańcuch zamienia tu werdykt nieprawdziwy na odmowę
([roadmap.md](../roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).

Odróżnia te dwa czytania cecha dopisana, czyli znacznik taki jak
[`ciąg`](podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania):
grupa zbudowana przez liczebnik zgodny ogłasza się nim,
ciało rządzące żąda od tego, co pod nim stoi, wartości przeciwnej,
a `Dwudziestu dwóch mężczyzn przyszło.` wychodzi wtedy jednym czytaniem, tym właściwym.
Drugiej kopii pozycji grupy imiennej znacznik nie żąda;
żąda tej cechy w każdej produkcji `grupa_imienna` i `człon_imienny`,
bo żądanie jest dodatnie, a cechy nieobecnej unifikacja nie sprawdza.
Czytanie zostaje mimo to, bo naprawa nie kupuje niczego, co dałoby się zmierzyć.
Zdań stawiających obok siebie dwie formy o czytaniu liczebnikowym
ma Składnica 180723 dziesięć,
znacznik nie rusza liczby czytań ani nad jednym z nich pod żadną z dwóch morfologii
ani nad prozą tego repozytorium,
a rejestr docelowy pisze liczebnik złożony
[cyfrą](#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii), której olski nie bierze.
Liczbę pierwszą daje przejście po złotej morfologii banku drzew,
a pozostałe wariant gramatyki z tą cechą, puszczony przez `harness/ruch.py`.

### Cząstkę przybliżającą przyłącza liczebnik, a nie grupa imienna

`przeszło sto zdań`, `przeszło trzy tysiące lematów` —
tak ten rejestr pisze granicę zamiast liczby dokładnej,
bo liczby kruchej
nie wpisuje do dokumentu, a granicę od dołu nazywa właśnie `przeszło`.
Bez tej pozycji całe takie zdanie jest odrzucone, a odrzucenie staje na tym słowie.

Ciało wchodzi w łańcuch liczebnika, a nie przed grupę imienną,
choć drugiego gospodarza cząstka
[już ma](okolicznik.md#cząstka-ma-dwóch-gospodarzy-i-przy-jednym-dostaje-etykietę).
Ciało dopisane tam obejmowałoby oba przyłączenia liczebnika naraz,
więc lemat postawiony na obu listach dawałby `niemal sto zdań`
dwa wyprowadzenia jednego kształtu, i dlatego listy są rozłączne.

Lista ma jeden lemat, a kryterium na wejście jest to samo co przy cząstce zdania:
czytanie konkurujące.
Odpowiada ono tutaj inaczej, bo pozycja jest węższa.
`przeszło` czyta się jeszcze formą czasownika `przejść`,
a w łańcuchu liczebnika tego czytania nie bierze nic,
więc o samo miejsce cząstka z nikim nie konkuruje.
Zdaniu czytanie czasownikowe zostaje:
`Przeszło dwadzieścia dwa chleby leżą.` wychodzi i cząstką, i z `Przeszło`
w orzeczeniu, bo to drugie czytanie zdanie miało już przedtem.
Ani bank drzew, ani ta proza zdania tego kształtu nie mają.

`ponad`, `blisko` i `około` mają w tym samym miejscu przyimek albo przysłówek:
`Kupuje ponad sto zdań.` wyprowadza się dziś wyrażeniem przyimkowym,
a `Kupuje blisko sto zdań.` z `blisko` w okoliczniku przysłówkowym,
czyli czytaniami, których polszczyzna w tych zdaniach nie ma.
Wpuszczenie tych trzech postawiłoby drugie wyprowadzenie obok nieprawdziwego,
zamiast je zdjąć, a zdejmuje się je wykluczeniem po stronie słownika;
`todo/` trzyma tę połowę osobno.

Rzeczownika nazywającego wielkość ta pozycja nie obejmuje:
`przeszło setkę zdań` odpada, bo `setka` jest rzeczownikiem, a ciało żąda liczebnika.
Odpada też `przeszło trzy razy dłużej`,
a odpada bez udziału cząstki: `trzy razy dłużej` nie wyprowadza się i bez niej.

Nad bankiem drzew pod złotą morfologią wychodzą z odrzucenia pojedyncze zdania,
złote czytanie ma każde z nich,
a jednoznaczności nie traci ani jedno zdanie przyjęte.
Pod żywą morfologią nie zmienia się werdykt ani jednego zdania
i przesuwa się sam bloker: odrzucenie staje dalej niż na `przeszło`.
Nad prozą tego repozytorium nie staje na tym słowie ani jedno odrzucenie,
a bez tej pozycji staje ich tam przeszło dwadzieścia;
czytanie dostaje z nich kilka, jednoznaczności nie traci żadne zdanie,
a reszta pada dalej, na przecinku albo na spójniku.
Liczby daje przejście po banku drzew pod obiema morfologiami
([corpus.md](../corpus.md#fetching-it) trzyma polecenia) oraz przebieg `olski-check`
nad prozą, oba porównane między dwoma drzewami roboczymi.

Liczba czytań maleje przy tym tam, gdzie forma za cząstką
czyta się także rzeczownikiem.
`Wiersz ma tysiąc zdań.` wychodzi i grupą liczebnikową, i rzeczownikiem `tysiąc`
z dopełniaczem pod sobą, a `Wiersz ma przeszło tysiąc zdań.` samą pierwszą z tych dwóch,
bo ciało żąda liczebnika i czytanie rzeczownikowe pod cząstkę nie wchodzi.

### Cyfry olski nie bierze, bo cyfra nie niesie morfologii

Rejestr, o który olskiemu chodzi, pisze liczebnik cyfrą:
`w terminie 14 dni`, `3 szkół`, `15 członków`.
Morfeusz daje cyfrze tag `dig` i ani jednej cechy,
a cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc obie produkcje biorą cyfrę naraz.
Odrzucić ją umie żądanie obecności cechy
([parsowanie.md](../parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)),
tyle że odrzuca wtedy każdą cyfrę i wpuszczenia nie kupuje.
`Termin wynosi 14 dni.` wychodzi wtedy o jedno czytanie więcej,
bo `dni` jest i dopełniaczem mnogim, i mianownikiem mnogim,
czyli jedna grupa wyprowadza się i pod produkcją rządzącą, i pod zgodną.
Dwa z tych czytań mają streszczenie znak w znak to samo,
bo różni je część mowy słowa pod głową, a nie żadna rola,
i po werdykcie czyta się to jak usterka narzędzia,
a nie jak zdanie, które da się poprawić.

Odmowa jest więc rozstrzygnięciem, a nie przeoczeniem,
i cena jest po jej stronie: cyfra zostaje formą,
której żadna produkcja nie bierze, i werdykt tak o niej mówi.
Wejście żąda dwóch rzeczy, których cyfra sama nie mówi, i tylko jedną da się odczytać.
Które z dwóch przyłączeń zachodzi, mówi rzeczownik po cyfrze:
`14 dni` ma dopełniacz mnogi, więc liczebnik jest tam rządzący,
a `14 dniach` miejscownik, więc zgodny, i tak samo czyta to każdy, kto ten rejestr pisze.
Przypadka samej grupy nie mówi ani cyfra, ani ten rzeczownik:
`pięć` jest mianownikiem, biernikiem albo wołaczem, a cyfra nie jest niczym,
więc grupa bez tej wartości spełnia każde żądanie przypadka w zdaniu.
Wejście stoi na tym drugim i jest to warstwa nad morfologią, a nie produkcja,
która wchodzi tym samym kryterium, co każda inna
([parsowanie.md](../parsowanie.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)).

## Liczebnik orzeka o tym, ile czegoś jest

`Tory są dwa.` mówi, ile torów jest, i orzeka to samym liczebnikiem,
a nie rzeczownikiem ani przymiotnikiem.
Pozycja jest orzecznikiem zgodnym, czyli tym samym miejscem, w którym stoi
`Ludzie są wolni.`, bo liczebnik zgadza się tu z podmiotem tak samo jak przymiotnik:
`Warstwy są dwie.` żąda formy żeńskiej, a `Tory są dwa.` męskorzeczowej.
Ciało jest przez to jedno i wypisuje samą parę cech, tak jak orzecznik przymiotnikowy.

Ciało jest osobne, a nie liczebnikiem wpuszczonym do symbolu grupy przymiotnikowej,
bo tamten symbol jest zarazem przydawką,
a liczebnik ma przy rzeczowniku
[własne przyłączenia](#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
i własne ciała; wpuszczony tam dałby `dwie rzeczy` drugie wyprowadzenie.

Pozycję tę bierze liczebnik zgodny i on jeden.
`Torów jest dwa.` mówi to samo rządzącym i zostaje na zewnątrz:
podmiot stoi tam w dopełniaczu, a orzeczenie nie zgadza się z niczym,
więc jest to osobne ciało i osobna liczba, której nikt nie policzył.

Nad bankiem drzew to ciało wyciąga z odrzucenia dwa zdania —
`Roześmieliśmy się obaj.` i `Ona płakała, a za chwilę płakałyśmy już obie.` —
a jednoznaczności nie odbiera ani jednemu zdaniu przyjętemu wcześniej.
Liczba jest mała, bo mierzy prozę prasową i literacką.
Rejestr, o który olskiemu chodzi, liczy tory i konstrukcje zdanie po zdaniu,
i to on postawił tę pozycję.
Kolejka blokerów jej nie widzi, bo każda forma tych zdań licencję ma,
a odrzucenie stoi na strukturze.

## Przydawka imiesłowowa stoi tam, gdzie przymiotnik

`Wymienione zadania są obowiązkowe.` i `Reguła sięgająca znaku jest tania.`
niosą jedną konstrukcję i jest nią przydawka,
a nie dwie pozycje przy dwóch częściach mowy.

Imiesłów przy rzeczowniku zgadza się z nim przypadkiem, liczbą i rodzajem,
czyli tym samym, czym zgadza się przymiotnik,
i stoi w tych samych dwóch szykach.
Dochodzi więc ciałem symbolu przymiotnikowego, a nie własnym symbolem:
osobny żądałby drugiej kopii każdej pozycji, w której przydawka stoi —
a stoi ich w gramatyce kilkanaście —
i nie kupowałby za to niczego, czego polszczyzna w tych pozycjach rozdziela.
Dopełniacz, którego imiesłów czynny żąda od swojego dopełnienia,
przychodzi przez to za darmo:
ciało z przydawką i dopełniaczem pod głową stało w gramatyce przed nim.

Ciała są dwa, po jednym na imiesłów, bo cena każdego jest osobną liczbą.
Orzecznik bierze przy tym biernego i nie bierze czynnego:
`Dziewczyna milknie zakłopotana.` jest polszczyzną,
a `Reguła jest sięgająca.` nie jest zdaniem, które ten rejestr pisze.

Cena stoi po stronie zgodności z drzewem wzorcowym, a nie po stronie pokrycia.
Przebieg nad Składnicą 180723 wypuszcza z odrzuconych przeszło dwieście zdań
i dokłada kilkadziesiąt przyjętych,
a podnosi przy tym dwie liczby, które mówią o werdykcie, że kłamie:
zdania, w których przyjęte czytanie przeczy drzewu wzorcowemu,
oraz zdania wieloznaczne, którym złote czytanie z lasu wypada.
Werdykt mówi więc o zdaniu nieprawdę częściej niż przed tą pozycją,
a kierunek ten trzyma
[roadmap.md](../roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście);
czym te zdania są, ten przebieg nie mówi, a wpis trzyma `todo/`.
Obie liczby drukuje `harness.pomiar`, a te sprzed tej pozycji trzyma git.

## Rzeczownik odczasownikowy jest głową grupy imiennej, a nie pozycją przy czasowniku

`Przyłączenie`, `wykluczanie`, `sięgnięciu` — Morfeusz daje takiej formie tag
`ger` wraz z liczbą, przypadkiem i rodzajem,
czyli z tym wszystkim, czego gramatyka od głowy grupy imiennej żąda.
Rodzaj jest przy tym zawsze nijaki, a niesie go tag, więc nie żąda go tu nic.

Rejestr, o który olskiemu chodzi, mówi tą formą o czynnościach,
bo dokumentacja opisuje to, co program robi:
`przyłączenie wyrażenia przyimkowego`, `wyznaczenie granicy`,
`sięgnięcie po mocniejszy mechanizm`.
Kolejka nad prozą tego repozytorium postawiła tę klasę na czele
zaraz po [leksykonie projektu](../warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma),
a kolejka ze Składnicy trzyma ją w czwartym wierszu
([corpus.md](../corpus.md#where-the-analyses-stop)).

Wchodzi ona jako głowa grupy imiennej, a nie jako pozycja przy czasowniku,
i tyle mówi o niej polszczyzna:
dopełnienia żąda w dopełniaczu — `przyłączenie wyrażenia`, a nie `przyłączenie
wyrażenie` — czyli tak, jak żąda go rzeczownik z dopełniaczem pod głową.
Rama czasownika zostaje przez to nietknięta,
a grupa z taką głową stoi w każdej roli, w której stoi każda inna grupa imienna.

Ta głowa dostaje tyle pozycji, ile ma rzeczownik, i dostaje je jednym zapisem:
pętla w `olski/subset/grupa.py` wypisuje każde ciało grupy imiennej dwa razy,
raz z rzeczownikiem i raz z formą odczasownikową.

Jedno wykluczenie stoi po stronie rzeczownika i nie dotyczy tej głowy.
Głowa rządząca dopełniaczem nie jest [zaimkiem rzeczownym](#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
a żaden z tych zaimków nie jest rzeczownikiem odczasownikowym,
więc po tej stronie nie ma czego wykluczać.

Jednej pozycji ta głowa nie ma i jest nią grupa wysunięta przed zdanie względne:
`którego przyłączenia` nie ma wyprowadzenia, gdzie `którego wyrażenia` ma.
Czoło zdania względnego bierze rzeczownik, a tej głowy nie bierze,
i wpuszczenie jej tam trzyma `todo/`.

## Forma przyimkowa zaimka żąda przyimka przed sobą

[Wykluczenie](../warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not) pyta o samą formę,
a jedna klasa czytań, których polszczyzna nie ma, żąda pytania o sąsiada.

Morfeusz czyta `nie` jako biernik zaimka `on`,
a `niego` wyłącznie jako dopełniacz i biernik tegoż,
i polszczyzna stawia te formy jedynie po przyimku: `na nie`, `bez niego`.
Tagset mówi to sam.
Cecha `post_prepositionality` ma wartość `praep` przy formie stojącej po przyimku
i `npraep` przy tej, która stoi bez niego,
a `nim` niesie obie naraz, tak samo jak `niej` i `nich` w miejscowniku,
bo te formy stoją i pod przyimkiem, i bez niego.

Bez warunku na tę cechę wychodzą czytania, których polszczyzna nie ma,
i bywa tak, że takie czytanie zostaje jedynym.
Jedno czytanie zdania przeczytanego na opak jest werdyktem najgorszym,
jaki ten pomiar wydaje
([corpus.md](../corpus.md#what-morphological-ambiguity-costs)),
bo milczenie czytelnik przyjmuje bez sprawdzania.

Warunek stoi przez to w warstwie morfologicznej i przed rozbiorem,
a nie na terminalu zaimka;
pyta on graf segmentacji, a jak, mówi `po_przyimku` w `olski/segmentacja.py`.

Licencji udziela sam przyimek tej gramatyki,
więc wykluczenie rozdzielającego `a` stoi i tutaj, nie tylko na terminalu
([zdanie-złożone.md](zdanie-złożone.md#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)).
Zdanie po zdaniu widać ten warunek dopiero razem z członem bez czasownika
([zdanie-złożone.md](zdanie-złożone.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)),
bo dopiero on daje `, a` cokolwiek za sobą.
Kosztuje ten warunek pojedyncze zdania tej prozy i oba czytania, które zdjął,
były nieprawdziwe: `a nie` wychodziło w nich spójnikiem i zaimkiem
w zdaniu, którego dalsza część potyka się o co innego.

Dwie drogi obok tej odpadły, każda na czym innym.
Terminal wypowiada warunek o parze wiązek cech,
a przyimek stoi nad zaimkiem przez całą grupę imienną,
więc żądanie postawione na terminalu musiałoby zejść przez każde jej ciało osobno —
tą samą drogą, którą przeszła
[negacja](../parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne),
i za tę samą cenę.
Ciało, które by cechy nie przepuściło, przepuściłoby za to każdą formę,
a takiego przeoczenia nie łapie żaden test.
Warunek sprawdzany po rozbiorze musiałby z kolei znać kształt grupy imiennej
i wyrażenia przyimkowego, czyli być gramatyką napisaną drugi raz,
a to jest właśnie kryterium, po którym warstwa więzowa
[wchodzi albo nie wchodzi](../parsowanie.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej).
Cecha na terminalu zostaje tam, gdzie warunek jest o parę:
zaimek dzierżawczy żąda `npraep` od formy przed rzeczownikiem
([niżej](#zaimek-dzierżawczy-jest-dopełniaczem-przed-rzeczownikiem)),
i pod przyimkiem to żądanie zostaje jedynym, które `bez niego zapisu` odrzuca.

Cena nad Składnicą wychodzi zerowa i mówi to przebieg pod morfologią żywą.
Jednoznaczność zyskuje kilkanaście zdań,
a wyprowadzenie tracą te i tylko te:

```text
Ale nie tylko same ulice irytują.
Po drugiej stronie też nie ma nic.
Posłowie opozycji winią nie tylko Żochowskiego.
W tym roku Zagłębie też nie płaci.
```

Każde z nich było przyjęte na czytaniu, w którym `nie` jest dopełnieniem,
więc odrzucenie jest przy każdym werdyktem uczciwym.
Pod złotą morfologią warunek nie rusza niczego,
bo anotatorzy wybrali tam jedno czytanie na token,
tak samo jak przy wykluczeniu wyżej.

Na zewnątrz zostaje ciąg współrzędny pod jednym przyimkiem.
`dla niego i niej` ma przyimek nad obydwoma członami,
a przed drugim z nich nie ma go wcale,
więc `Program zapisuje ustawienia dla niego i niej.` traci wyprowadzenie,
gdzie `bez nich i plików` je zachowuje,
bo tam forma przyimkowa jest członem pierwszym.
Nad Składnicą nie kosztuje to ani jednego zdania,
a zdanie odrzucone stoi wśród tego,
[czego olski nie bierze](../subset.md#what-it-does-not-cover-yet).

Forma, której to wykluczenie zabiera wszystkie czytania — `niego` innych nie ma —
jest dla werdyktu formą bez licencji,
więc `Cena niego rośnie.` wychodzi odrzucone z `niego` wypisanym.
Przebieg nad korpusem czyta ją inaczej i liczy takie zdanie
jako zdanie bez struktury nad całością,
bo `bloker` w `olski/pokrycie.py` nazywa część mowy pierwszego czytania,
a tu nie ma ani jednego.
Rozejście to jest zapowiedziane
([parsowanie.md](../parsowanie.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)),
a naprawę trzyma `todo/` razem z wycięciem czytań bez licencji,
które daje tę samą krawędź bez czytań na całej klasie form.

## Zaimek dzierżawczy jest dopełniaczem przed rzeczownikiem

`Jego skutki są znane.`, `Jej cena jest niska.`, `Ich liczba rośnie.`
Posiadanie trzeciej osoby polszczyzna wyraża dopełniaczem zaimka osobowego,
a nie osobnym przymiotnikiem, i tym różni się `jego` od `mój`, `nasz` i `swój`:
te trzy Morfeusz zna jako przymiotniki,
więc bierze je pozycja przymiotnika przy rzeczowniku,
a `jego`, `jej` oraz `ich` czyta jako formy lematu `on`,
więc brakowało trzeciej osoby i tylko jej.

Pozycja jest jedna i stoi przed grupą imienną, bo tam ją polszczyzna stawia.
Dopełniacz po rzeczowniku bierze inna produkcja,
więc `skutki jego` wychodzi tak samo jak `skutki wyboru`
([subset.md](../subset.md#what-the-grammar-covers)), i ciało jest dlatego jedno, a nie dwa.

Zgodności ta pozycja nie ma i mieć nie może,
bo zaimek zgadza się ze swoim poprzednikiem, a ten stoi w zdaniu obok:
`Jego skutki` ma zaimek pojedynczy przy rzeczowniku mnogim,
a `Ich cena` ma zaimek mnogi przy rzeczowniku pojedynczym.
Zmienna wspólna — ta, którą wypuszcza przymiotnik i liczebnik zgodny obok —
wygląda tu poprawnie i odbiera polszczyźnie prawie każdą taką parę;
niezmiennik pilnuje test w `tests/test_grupa_imienna.py`.

Formę zawężają dwa warunki na cechę, a nie lista lematów:
lematem każdej z tych form jest `on`, więc lista wpuszczałaby je wszystkie naraz.
Pierwszy żąda formy akcentowanej, czyli zostawia poza pozycją `go`:
`Znam go cenę.` nie jest polszczyzną, bo forma nieakcentowana stoi
przy czasowniku, a nie przy rzeczowniku.
Drugi żąda formy nieprzyimkowej, czyli zostawia poza pozycją `niego`, `niej` i `nich`:
`Znam niego cenę.` nie jest polszczyzną tak samo,
a `Bez niego cena rośnie.` jest, bo tam ta forma stoi po przyimku.
Warunek drugi zarabia na siebie właśnie pod przyimkiem, i tylko tam.
Poza nim formę przyimkową odsiewa już morfologia
([wyżej](#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)),
a `bez niego zapisu` ma tę formę po przyimku,
więc odrzuca ją to jedno żądanie i nic poza nim.

Pozycji tej nie ustawiła ani kolejka blokerów
([corpus.md](../corpus.md#where-the-analyses-stop)),
ani ranking form bez licencji.
Odrzucenie stało na strukturze, a nie na żadnej z tych form,
bo grupa imienna o jednym zaimku bierze każdą z nich,
więc analiza zatrzymywała się dopiero za zaimkiem:
`Jego skutki są znane.` stawało na `znane`.
Wskazała ją sesja pisząca pod tę gramatykę zdanie po zdaniu.
Ze wszystkiego, co tam zawracało zdanie, ta pozycja zawracała je najczęściej
([pisanie-po-olsku.md](../pisanie-po-olsku.md)).

## Zaimek zwrotny jest terminalem, bo nie zgadza się z niczym

`Widzę siebie.`, `Osie są od siebie niezależne.`
Morfeusz trzyma ten zaimek pod częścią mowy tej jednej formy — `siebie:gen`,
`sobie:dat`, `sobą:inst` — a przypadek jest jedyną cechą, jaką ta część mowy niesie.

Rozstrzyga o tym brak liczby i rodzaju.
Grupa imienna niesie obie, bo zgadza się nimi z przydawką i ze zdaniem względnym,
a ciało grupy bez nich wpuszczałoby ten zaimek wszędzie tam,
gdzie zgodności żąda ktoś inny:
cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc `Widzę siebie, która stoi.` dostawałoby wyprowadzenie.
Ceną terminalu jest to, że przydawki ani dopełniacza ten zaimek pod sobą nie bierze,
a polszczyzna nie daje mu ani jednego, ani drugiego.

Pozycje są dwie: dopełnienie oraz grupa pod przyimkiem.
Dopełnienie powtarza ciała grupy imiennej —
biernik, dopełniacz negacji oraz celownik i dopełniacz z leksykonu
([walencja.md](../walencja.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)) —
a stoją one wypisane, bo z listy leksykonu wchodzą tu dwie pozycje z trzech:
bezokolicznik przypadkiem nie jest.
Mianownika ta część mowy nie ma i mieć nie może,
skoro zaimek ten odsyła do podmiotu, więc podmiotem nie bywa
i produkcji na to nie ma.
Orzecznika narzędnikowego ten zaimek nie dostał,
a zdanie z nim mimo to się wyprowadza:
`Parser jest sobą.` wychodzi jednoznaczne na rzeczowniku `soba` w narzędniku.
Pozycja i ten lemat schodzą się przez to w jedno pytanie, a wpis trzyma
`todo/`.

Zakup jest tu kilkudziesięcioma zdaniami banku drzew wyciągniętymi z odrzucenia,
w większości przyjętymi, i po stronie ceny nie ma pod złotą morfologią nic:
ani jedno zdanie przyjęte wcześniej nie staje się wieloznaczne.
Pod żywą płaci ten sam lemat `soba`, którego Morfeusz zna w celowniku,
miejscowniku i narzędniku: jednoznaczności traci kilkanaście zdań z `sobie`
i `sobą`, a `siebie` żadnego.
Każde z nich wychodziło bez tej pozycji jednoznaczne właśnie na rzeczowniku,
czyli na czytaniu, którego polszczyzna tam nie ma
([warstwa-leksykalna.md](../warstwa-leksykalna.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)),
więc razem z jednoznacznością ubywa werdyktów nieprawdziwych.
Wykluczenie ze słownika po ten lemat nie sięga, bo jest to rzeczownik odmienny
([warstwa-leksykalna.md](../warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).
Nad prozą tego repozytorium zakup jest liczony w pojedynczych zdaniach,
a ceny nie ma żadnej.
Z drzewem wzorcowym olski nie zgadza się nad pojedynczymi zdaniami nowo przyjętymi,
a garść czyta bez roli, którą dałoby się z tym drzewem porównać:
podmiot jest w nich opuszczony, a zaimek stoi pod przyimkiem.
