# Kategorie zapisu: co autor pisze w drzewie

Rejestr kategorii, w których pisze się drzewo toru składu:
co każda z nich mówi, czego odmawia i co kosztowała.
Rejestru nie czyta się od góry — czytelnik przebiega go do swojego wpisu.
Na jakim poziomie te kategorie stoją i czemu nie są kategoriami polszczyzny,
rozstrzyga [sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka).
Deklarują je `olski/skład/składnia.py` oraz `olski/skład/opowieść.py`.

Dwie sekcje ostatnie mówią, skąd wzięła się kolejka,
w której te kategorie powstawały.

## Tekst wie to, czego zdanie o sobie nie wie

Zdanie skompilowane osobno wypisuje każdą rzecz pełną nazwą
i stawia ją w czasie, w którym stoi samo.
Tekst wie dwie rzeczy więcej i obie zmieniają to, co wychodzi,
więc `olski.skład.opowieść` stoi nad `olski.skład.składnia`, a nie obok.

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
Warunki trzyma `pomijalny` w `olski/skład/składnia.py`,
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
na [trzecią architekturę](sklad.md#three-architectures),
czyli na rozbiór zdania pisany z góry.

Kategorią, która z tego wyszła, jest wskazywanie.
`Jaki` wskazuje rzecz cechą, `Opis` w `olski/skład/składnia.py` wskazuje ją zdarzeniem,
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

Reszta zdania złożonego wychodzi z czterech innych kategorii:
[okoliczności wyrażonej zdarzeniem](#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie),
[dopełnienia wyrażonego zdarzeniem](#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
[treści](#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi)
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
Z tego samego powodu dochodzi ona jednakowo do zdania o czynności
i do orzeczenia imiennego: `Kot jest zwierzęciem w piwnicy.`
mówi, gdzie, i pytanie o to nie zależy od tego, czym zdanie orzeka.
Pod orzecznikiem taka okoliczność nie stoi i jest to rozstrzygnięcie:
`w piwnicy` czyta się w tym zdaniu i o byciu, i o zwierzęciu,
a drzewo mówi jedno, bo okolicznik dochodzi w nim do orzekania,
tak jak dochodzi do zdarzenia, a do rzeczy nie dochodzi nigdzie.

Różnica między nimi jest różnicą w polszczyźnie, a nie w drzewie,
i cała siedzi w słowie, którym relacja wychodzi na wierzch.
Przed rzeczą stoi przyimek, który rządzi przypadkiem,
i bierze go z `olski/skład/przyimki.py`;
przed zdarzeniem stoi spójnik, który nie rządzi niczym,
bo zdanie podrzędne rozdaje przypadki własne,
więc `olski/skład/spójniki.py` mówi o nim mniej: to, w jakiej stoi relacji.
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
Wpis w `olski/skład/przyimki.py` stoi tam mimo to, bo przypadek trzeba skądś wziąć,
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
Świadka daje jej za to bank drzew:
`gdyż` nie otwiera w nim ani jednego zdania, a `gdy` dwie piąte swoich wystąpień
i to samo rozstrzygnięcie stoi po stronie analizy, w dwóch listach lematów
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)),
bo jest to fakt o słowie, a nie o kierunku, w którym się go używa.

Okoliczność wyrażoną zdarzeniem gramatyka od niedawna wyprowadza,
więc obieg zamyka się i na niej:
`Program zapisuje ustawienia, bo linter sprawdza tekst.`
wraca z napisu tym drzewem, z którego wyszło,
a relację czyta rozbiór z tego samego leksykonu, tyle że wspak
(`RELACJE_SPÓJNIKÓW` w `olski/skład/rozbiór.py`).
Skutek jest jedynym wpisem tej tabeli, który stąd nie wraca,
bo `więc` spina dwa zdania przecinkiem i spójnikiem naraz,
a gramatyka bierze zdania spięte jednym z tych znaków albo drugim
([subset.md](subset.md#what-it-does-not-cover-yet)),
i to jest ta różnica między kierunkami, którą widać dopiero na obiegu.

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

Przypadek tej pozycji przychodzi z ramy, a nie z drzewa,
i jest to ta sama zasada, którą niesie cały ten zapis:
przypadek bierze się z pozycji, a nie z tego, co autor napisał.
`Czeladnik szukał córki krawca.` i `Czeladnik zasłonił twarz.`
wychodzą przez to z drzew jednego kształtu i stoją w dwóch przypadkach,
bo `szukać` biernika nie bierze i dopełniacz jest tym, co jego rama ma.
Widać na tej parze i to, dokąd sięga przeczenie:
dopełniacz negacji wchodzi w miejsce biernika i dopełniacza z leksykonu nie rusza,
bo nie ma tam czego zmienić.
Rama wychodzi przy tym z leksykonu zbiorem pozycji (`rama` w `olski/walencja.py`),
więc pytanie pada tu raz na pozycję postawioną w drzewie,
a nie raz na pozycję, którą ta kategoria zna,
i pozycja dopisana do leksykonu nie dokłada gałęzi w konstruktorze.

Wykonawca jest tu tym, czego bezokolicznik o sobie nie mówi,
i dlatego stoi w drzewie, a nie w formie.
Autor pisze tę samą zmienną dwa razy, raz przy czasowniku i raz pod nim,
czyli robi to, co robi przy `Postać` i przy `Opis`,
a konstruktor zdania o czynności — `Robi` w `olski/skład/składnia.py` —
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
Dwa powody spotykają się w jednym miejscu — `_podmiot` w `olski/skład/składnia.py` —
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
[Walenty rozdziela kontrolę](warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on),
więc `chcieć` bezokolicznik dostaje, a `kazać` nie dostaje go wcale,
bo jego wykonawca stoi w celowniku,
a celownik obok bezokolicznika jest drugą pozycją ramy,
której gramatyka podzbioru nie ma
([subset.md](subset.md#what-it-does-not-cover-yet)).

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

## Kopulę wybiera autor, bo bycie i stawanie się są dwiema rzeczami

`Jan jest nauczycielem.` i `Jan zostaje nauczycielem.` orzekają o tym samym
i różnią się tym, czy mówią o zmianie,
a różnica ta jest kategorią dziedziny, a nie formą do policzenia.
Kopula stoi więc w drzewie polem, tak samo jak czynność,
i wybiera ją autor, a nie kompilator.

Wybór ogranicza leksykon i jest to ta sama odmowa, którą dostaje czynność:
orzecznik w narzędniku bierze kopula i nikt poza nią,
więc `zapisywać` postawione w tym miejscu zgłasza się.
Odmowa idzie i w drugą stronę: czasownik, który orzeka orzecznikiem,
nie orzeka czynnością, więc `Parser jest.` nie wychodzi ze składu tak samo,
jak nie wyprowadza się z olskiego.
Jest to jedyny wpis tego leksykonu pisany ręką,
bo Walenty mówi o `być` to samo, co o każdym innym lemacie,
i dlatego odjęcie kopuli stoi w jednym miejscu na oba kierunki
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)).

## Uczestników bywa dwóch i rozdziela ich kategoria, a nie kolejność

`Parser pokazuje autorowi czytania.` ma poza działającym dwóch uczestników
i nie są oni wymienni:
ten, komu się rzecz pokazuje, jest kimś innym niż to, co się pokazuje.
Drzewo ma więc powiedzieć, który jest który, a ma na to dwa sposoby:
kolejność argumentów albo kategorię.

Kolejność odpada, bo ten zapis nie mówi kolejnością nic nigdzie indziej.
Role czyta się w nim z nazw i rozstrzyga o tym
[`olski/skład/słownik.py`](../olski/skład/słownik.py),
a argument dopisany w środku zmieniałby wtedy zdanie
bez żadnego śladu w miejscu, w którym go dopisano.
Kategorią jest `Komu`, a nazwą jest w niej pytanie —
tak samo jak przy relacjach okolicznikowych — bo polszczyzna nie ma na tego
uczestnika jednego słowa:
`dawać` stawia tam odbiorcę, `pomagać` tego, komu się pomaga,
a `dziękować` tego, komu się dziękuje.

Że wychodzi z tego celownik, rozstrzyga rama, i jest to ta sama droga,
którą przypadek dostaje
[dopełnienie](#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie).
Rama wychodzi z leksykonu zbiorem pozycji, a nie odpowiedzią na jedno pytanie,
i widać to na parze czasowników:
`pokazywać` ma w niej biernik obok celownika, a `pomagać` ma sam celownik,
więc `Linter pomaga autorowi.` wychodzi ze składu,
a to samo drzewo z rzeczą w miejscu dopełnienia zgłasza się.

## Treść jest zdarzeniem, o którym ktoś coś sądzi

Ta sama pozycja bierze rzecz, zdarzenie wykonywane
i zdarzenie, o którym podmiot tylko coś orzeka,
a trzecie z nich jest osobną kategorią, bo pytanie przy nim jest inne.
`Czeladnik chciał zejść.` mówi, co czeladnik zrobi,
a `Czeladnik wiedział, że postaci stały pod ścianą.` mówi, co on o świecie sądzi.
Nosi tę kategorię `Treść` w `olski/skład/składnia.py`,
i tam też stoi powód, dla którego jest zawinięciem, a nie wnioskiem z drzewa:
to samo zdarzenie stoi pod `chcieć` i pod `wiedzieć`, a mówi dwie różne rzeczy,
więc różnicy nie ma z czego policzyć.
Rozstrzyga o niej przez to autor, a nie kompilator zgadujący z podmiotów,
i jest to ta sama postawa, którą trzyma
[przegląd](po-wypisaniu.md#drzewo-jest-jednoznaczne-a-napis-z-niego-nie-musi-być):
zgłaszać albo pytać, a nie podmieniać drzewo za autora.

Jest to jedyna rzecz, którą ten zapis ma na wnętrze postaci, i po to tu jest.
Jedno zdanie o tym, w co postać nie wierzy, mówi o niej więcej
niż zdanie o tym, jaka ona jest, i mówi to bez nazywania emocji,
czyli bez usterki, którą [fiction.md](fiction.md#sentence-and-paragraph) wylicza.
Legenda o bazyliszku stoi na tym całym akapitem pierwszym:
każde z trzech zdań, które on orzeka, wraca potem w innym akapicie,
a dwa z nich wracają jako to, co postać o świecie sądzi,
przy czym jedna sądzi przecząco i przez to schodzi do piwnicy.

Od bezokolicznika w tej samej pozycji różni ją podmiot,
który stoi w drzewie, zamiast przychodzić z góry,
i z tego jednego idą trzy rzeczy, z których żadna nie ma osobnej gałęzi.
Kontroli nie ma tu czego pytać.
Dopełniacz negacji nie sięga w dół, bo zdanie podrzędne rozdaje przypadki własne,
więc `Nie wierzył, że wyniosła kufer.` przeczy jednemu czasownikowi,
a drugi zostaje przy swoim bierniku.
Podmiot wypisuje się w takim zdaniu zawsze, także gdy jest tym samym,
o którym orzeka czasownik nad nim, bo opuszczenie w zdaniu podrzędnym
odsyłałoby czytelnika o piętro wyżej.

W drugą stronę ten podmiot sięga jednak zdania obok
i jest to jedyne miejsce, w którym treść zmienia coś poza sobą.
`Wiedział, że skrzynia stała w piwnicy.` odbiera zdaniu następnemu opuszczenie
dokładnie tak, jak odbiera je to samo zdarzenie postawione pod `bo`,
bo warunek mierzy to, na kogo czytelnik trafia, a nie to, czym ten ktoś jest
w zdaniu ([wyżej](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)).
Widać to w samej legendzie: `Czeladnik wiedział, że pod ścianą stały postaci.`
podmiot opuszcza, bo postaci wyciągają z tego czasownika formę mnogą,
a to samo zdanie o bazyliszku wypisałoby czeladnika,
bo w czasie przeszłym obaj wyciągają z niego `wiedział`.

Spójnik jest tu jeden i stoi w klasie, a nie w leksykonie,
czyli odwrotnie niż przy okoliczności, gdzie autor wybiera między `bo` i `ponieważ`.
Polszczyzna wybiera go tu za autora: `że` mówi, że tak jest, a `żeby`, że tak ma być,
i to drugie jest inną kategorią dziedziny, której to drzewo nie ma.
Odsłoniła ta pozycja jeszcze jedną, i jest nią czas zdania podrzędnego;
obie trzyma [`todo/`](../todo/README.md), a co pokazały,
mówi [czego nie spełniono](#czego-nie-spełniono).

## Następstwo zdarzeń jest kategorią, a spójnik jego wnioskiem

`Ciąg` w `olski/skład/składnia.py` bierze kilka zdarzeń i wypuszcza jedno zdanie,
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

Żądania te rozdzielają się warstwą, która za nie zapłaciła,
i to ona jest tu porządkiem, bo kolejność, w której padły, nie niesie nic:
nie jest ani czasem, ani wagą.
Jedne zostały w składni i wyszły z nich nowe kategorie.
Jedne zeszły o warstwę niżej, do wyboru formy i do czytania cudzego słownika,
i to jest ustalenie tej sekcji, bo raz nie jest zbiegiem, a trzy razy nie jest.
Jedno zapłaciło samym zapisem, nie ruszając ani kategorii, ani formy.
A dwa nie zostały spełnione i to one pokazały ceny,
których nikt przed nimi nie wycenił.

### Co zostało w składni

Pierwszym żądaniem jest zakończenie, które nie mówi, o czym opowieść była,
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
[roadmap.md](roadmap.md#czego-brakuje-pod-tym-kryterium) trzymała podrzędność,
i pokrywa on z niej tyle, ile podrzędność wskazuje rzecz, a nie więcej.

Drugie żądanie jest o rytm i stoi w tamtym katalogu wprost.
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

Trzecie wróciło do usterki, którą pierwsze zaczęło, i nie dało się nią załatwić.
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

Czwarte poszło dalej tą samą usterką i doszło tam, gdzie wola nie dochodzi.
Postać, która czegoś chce, ma wnętrze płaskie,
bo chcieć czegoś to znaczy zmierzać do rzeczy, którą opowieść i tak pokaże;
postać, która sądzi o świecie coś, czego świat nie potwierdza, ma je własne.
Legenda stoi na tym akapitem pierwszym: orzeka on trzy rzeczy,
a każda z nich wraca potem w innym akapicie.
Córka krawca nie wierzy w bazyliszka i dlatego schodzi po kufer,
czyli jej powód jest teraz pomyłką, a nie odwagą;
czeladnik wie o kamiennych postaciach i dlatego bierze lustro;
a trzecie zdanie, o wzroku potwora, wraca na końcu przeciw temu, do kogo należał.
Wyszła z tego [treść](#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi),
a wraz z nią jedno zdanie mniej o tym, jaka postać jest,
bo tego zdania w tej legendzie nie ma ani jednego.

Piąte jest po prostu tanie.
Trzy relacje okolicznikowe dopisały się bez namysłu,
bo `w nocy`, `po schodach` i `wśród kamiennych postaci` są tym,
czym opowieść odmierza czas i ruch, a nie nową kategorią.
Jedna z nich niesie przy tym coś poza sobą:
`w nocy` stoi w tym samym przypadku co `w piwnicy`,
więc jest wpisem, po którym w tekście nie zmienia się nic,
i pokazuje, że relacja nazywa to, co autor powiedział,
a nie to, w czym mu to wyjdzie.

### Co zeszło warstwę niżej

Pierwsze zejście wyszło z tego samego żądania, co `Opis` powyżej,
i jest ciekawsze niż ono, bo kolejka nie została w tej warstwie.
Zaimek względny wychodził z morfologii jako `któren`,
czyli forma, którą SGJP odsyła do gwary,
więc nowa konstrukcja składniowa zażądała kryterium wyboru formy,
stojącego pod nią o dwie warstwy niżej
([kwalifikator](formy-i-leksemy.md#kwalifikator-mówi-o-formie-dwie-rzeczy-i-tylko-jedna-jest-rejestrem)).
Plan tego tak nie ustawia i nie ma jak ustawić:
roadmapa trzyma wybór formy jako etap 3, a podrzędność jako część etapu 5,
i wywód za tą kolejnością się nie zmienia.
Tekst nie czyta jednak numeracji i płaci od razu za wszystko,
czego wymaga zdanie, które ma z niego wyjść.

Drugie zejście przyszło stamtąd, gdzie pierwsze,
i dotknęło opuszczania podmiotu, czyli tego, co widać dopiero nad tekstem.
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

Trzecie i czwarte zeszły do cudzego słownika, oba z pozycji dopełnienia,
i to one czynią z tej pary ustalenie, bo dwa razy pod rząd nie jest zbiegiem.
Bezokolicznik nie zgadza się z niczym, więc kategoria dziedziny postawiona wysoko
zażądała czytania Walentego o dwie warstwy niżej,
tak jak wskazywanie rzeczy zażądało kryterium wyboru formy.
Czytanie jest przy tym o kontroli, a nie o kształcie frazy,
bo `chcieć` i `kazać` biorą w polszczyźnie ten sam bezokolicznik
i wskazują nim dwóch różnych ludzi.
Treść zażądała trzeciego zdania z tego samego słownika i o kontrolę nie pyta,
bo zdanie podrzędne niesie podmiot własny;
pyta o samą pozycję, i pyta o nią tym mocniej,
że `zamykać` bierze biernik, a `Kot zamyka, że mysz śpi.` nie jest zdaniem polskim.
Wyszło z tego coś, czego niezmiennik obiegu nie zapowiadał:
plik leksykonu jest wspólny, a dwa z trzech zdań, które on mówi, czyta jeden kierunek.
Bezokolicznik parser zmierzył i nie kupiło mu to zawężenie ani jednej jednoznaczności,
a zdania podrzędnego tamta gramatyka nie ma wcale, więc nie ma tam czego mierzyć;
liczby trzyma [warstwa-leksykalna.md](warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on).

### Co zapłaciło samym zapisem

Jedno żądanie jest o czasie i kosztowało jeden wpis w leksykonie przyimków.
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

### Czego nie spełniono

Anafora spełniona nie została,
a cena, którą pokazała, jest tu ustaleniem osobnym.
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
Ruch trzyma [todo/](../todo/README.md), a `jego wzrok` jest przy tym trzecią rzeczą:
zaimek dzierżawczy przestawia grupę imienną, a nie wypełnia pozycję w zdaniu.
Czwartą odsłoniła treść i jest z tych czterech najtańsza,
bo polszczyzna nie pisze tam zaimka wcale, tylko opuszcza podmiot:
legenda chce zdania `Czeladnik znał córkę krawca. Nie wiedział, że stała pod ścianą.`,
a warunek na to opuszczenie stoi i tę parę przepuszcza —
brakuje zasięgu, bo antecedensem jest dziś podmiot zdania obok,
a tu jest nim jego dopełnienie.

Czas zdania podrzędnego odsłoniła ta sama pozycja i bez niej nie było go widać,
bo dotąd każde orzeczenie tej opowieści stało obok innych, a nie pod nimi.
Czas jest [własnością opowiadania](#tekst-wie-to-czego-zdanie-o-sobie-nie-wie),
więc opowieść stawia jeden czas wszędzie,
a polszczyzna liczy czas zdania podrzędnego wobec zdania nad nim:
`Wiedział, że pod ścianą stały postaci.` mówi co innego niż to samo ze `stoją`.
Oba te zdania są polskie, więc jest to kategoria dziedziny, a nie forma do policzenia,
i pyta ona o to, czy rzecz z dołu trwała wtedy, czy skończyła się przedtem.
Trzyma to [todo/](../todo/README.md), a legenda stoi na razie na wersji przeszłej.
