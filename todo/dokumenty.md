# Dokumenty i konwencje

Wskazania między `docs/konstrukcje-gramatyczne/` i `olski/subset/`
idą w obie strony,
a pilnowane są tylko w jedną.
Ćwierć wskazań z `olski/subset/` nie ma anchora,
więc `tests/test_docs.py` sprawdza przy nich sam plik,
a kilka zdań dokumentu opiera się na nazwie w środku modułu,
której nie pilnuje nic ([CLAUDE.md](../CLAUDE.md#na-czym-wolno-oprzeć-zdanie)).
Ruchem jest anchor przy każdym wskazaniu z kodu,
a po stronie dokumentu nazwa modułu w miejsce nazwy w jego środku —
tam, gdzie zdanie nadal mówi czytelnikowi, gdzie szukać.
Wskazania na `morphology`, `po_przyimku` i `po_słowie` są tu przypadkiem
najtrudniejszym, bo dokument opisuje kolejność tych trzech warstw
i nazwa modułu tego nie odda.

Komentarz w pozostałych modułach powstał pod regułą, która żądała wywodu
przy każdym ciele, a nie pytała, czy z kodu widać to samo bez niego;
[reguła dzisiejsza](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely)
zostawia komentarz tam, gdzie rozkmina jest głębsza od kodu.
Ruchem jest ten sam przebieg nad `olski/parse/`, `olski/grammar.py`,
`olski/rozstrzyganie.py` i `olski/skład/`, po jednym module na commit,
bo skreślenie wmieszane w cudzy moduł ginie w przeglądzie.
Do przeczytania jest przy każdym module jedno pytanie:
czy zdanie komentarza mówi to, co widać z nazwy symbolu i z kształtu ciała.
Pułapkę tego przebiegu pokazał ten nad gramatyką:
skrócone zdanie zabiera czasem jedyną kopię przesłanki,
a zdanie obok zostaje wtedy bez poprzednika,
i żadnego z tych dwóch nie łapie suita, tylko grep po skreślonej frazie.

Liczba przepisana z pliku danych do dokumentu rozjeżdża się z nim po cichu.
Liczby, którymi
[`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)
opisuje `olski/leksykon.txt`, przeliczają się z tego pliku jednym `cut`-em,
a trzy z nich rozeszły się z nim w commicie, który pisał obie strony;
znalazło je dopiero przeliczenie ręką.
`tests/test_docs.py` pilnuje nazw plików i sekcji,
`tests/test_wydruki.py` bloków stojących pod komendą,
a liczby wziętej z pliku nie pilnuje nic
([CLAUDE.md](../CLAUDE.md#na-czym-wolno-oprzeć-zdanie)).
Ruchem jest check przeliczający je z tego pliku, wzorowany na tym,
czym `tests/test_docs.py` trzyma [blok checków](../CLAUDE.md#checks) równy workflowowi.
Do rozstrzygnięcia jest, czy warto: klasa jest dziś tą jedną sekcją
i jedną liczbą poza nią, czyli `998 par` w
[`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
a check czytający liczbę z prozy wyrażeniem regularnym
czerwienieje po przeredagowaniu zdania, a nie po zmianie w danych.

Dwanaście nagłówków rejestru ma w orzeczeniu czasownik domowy —
„stoi”, „wchodzi”, „niesie”, „bierze” — którego nagłówek znosi najgorzej
([CLAUDE.md](../CLAUDE.md#dla-kogo-jest-napisane-zdanie)),
a sześć bierze precyzję z tego, co wyklucza
([CLAUDE.md](../CLAUDE.md#a-phrase-that-arrived-ready-made-was-not-chosen));
`Czoło niesie etykietę roli, którą zajmuje, a werdyktu nie rusza`
jest w obu tych zbiorach.
Najtrudniejszy jest `Zaimki kto i co wchodzą wszystkimi pozycjami naraz`,
bo „naraz” niesie tam tezę o pomiarze:
pozycja wpuszczona sama obniża pokrycie.
Ruchem jest przejście nagłówków `docs/konstrukcje-gramatyczne/`
testem podstawieniowym, po kilka na commit,
bo każde przemianowanie rusza kotwicę i wszystkie wskazania na nią.
Do przeczytania jest pierwszy akapit sekcji, bo teza skreślona z nagłówka
ma tam stać, a zwykle już stoi.

`Czoło` jest w `docs/konstrukcje-gramatyczne/podrzędność.md` terminem,
a nie ma w tym rejestrze zdania, które by je wprowadzało:
pierwszy raz pada w sekcji o zaimku względnym jako nazwa znana,
a sekcja `Czoło niesie etykietę roli, którą zajmuje, a werdyktu nie rusza`
mówi, co czoło robi, nie mówiąc, czym ono jest.
Kto wchodzi po kotwicy `#dopełniacz-z-ramy-wysuwa-się-na-czoło-a-celownik-nie`,
czyta przez to nazwę nigdzie tu nie zdefiniowaną
([CLAUDE.md](../CLAUDE.md#the-reader-goes-sentence-by-sentence)).
Ruchem jest jedno zdanie przy pierwszym wystąpieniu.
Do przeczytania są dwie rodziny czół w `olski/subset/podrzędne.py`,
bo to zdanie ma powiedzieć, co rozdziela cecha `czoło`,
a nie tylko że konstytuent stoi wysunięty.

Dawną nazwę odczytania — `czytanie` — noszą pozostałe dokumenty,
nazwy w kodzie i nazwy plików
`harness/czytania.py` oraz `tests/test_czytania.py`.
Nazwę rozstrzyga
[sekcja o tym, co się liczy jako jedno odczytanie](../docs/subset.md#co-się-liczy-jako-jedno-odczytanie).
Ruchem jest poprawianie reszty w miejscu ruszanym z innego powodu,
a nie przebieg sedem po całym repozytorium:
ten przemianowałby też formę `czytanie` cytowaną w bloku tamtej sekcji,
gdzie jest ona przykładem rzeczownika o dwóch częściach mowy, a nie terminem.
Wpis zamyka commit, po którym `czytanie` w znaczeniu wyniku nie zostaje nigdzie.

`docs/corpus.md` and `docs/corpora.md` differ by two letters
and hold unrelated things:
the first measures the grammar against the Składnica treebank,
the second surveys the corpora of human Polish this repository can obtain.
A link to either one reads the same,
and a grep for one of them finds both,
and finds `docs/audit-corpus.md` too,
which is about one of the corpora the second surveys.
The move is to rename `docs/corpus.md` to `docs/skladnica.md`,
which says what it holds and matches `docs/swigra.md` beside it,
and to carry the rename through every file that names it.
`tests/test_docs.py` catches the Markdown links and the citations in code,
and nothing catches the plain-prose mentions,
so those are the ones to grep for.
That name lands beside `docs/sklad.md`, which is the compiler and not the treebank,
so a grep for `sklad` finds both,
and the pair this entry is about becomes that one.
The package no longer collides with either name,
the coverage run over prose having become `olski-pokrycie`
and the run over the treebank `python3 -m harness.pomiar`,
so `corpus` names the treebank reader and this document and nothing else.
That leaves the document alone to rename, and its neighbour is the reason to:
a reader who greps for one of the two corpora documents finds both.

Trzy dokumenty podzbioru są mieszane.
Polskie sekcje dopisywano do angielskiego dokumentu, zanim go rozcięto,
a [reguła językowa](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
przewiduje dla takiego pliku przekład całości, osobną zmianą.
Ruchem jest przekład, po jednym commicie na dokument,
i najcięższy jest przy `docs/subset.md`, gdzie angielska jest połowa sekcji
wraz z obiema listami; w dwóch pozostałych zostały po dwie.
Przekład kurczy się przy tym sam, bo akapit nowy powstaje po polsku,
a przepisywany przekłada się razem z przepisaniem.

`docs/swigra.md` wylicza mechanizmy warte wzięcia i wyliczył je z kodu,
a monografia Świgry opisuje trzy, których kod pokazuje jako zapis, a nie jako wybór.
Pierwszym jest wartość `req(Neg)`: fraza bezokolicznikowa z podrzędnikiem
wymuszającym negację niesie w górę żądanie zamiast wartości,
a unifikuje je dopiero reguła czasownika nadrzędnego (Woliński 2019, p. 4.4.2).
Drugim jest przecinkowość, czyli para wartości na obu końcach frazy
i czteroklauzulowy warunek zgodności sąsiadów,
w którym surowość gramatyki wobec pominiętych przecinków
ustawia się włączaniem klauzul (tamże, p. 4.4.5).
Trzecim jest `sequence_of` z warunkami iterowanymi, czyli reguła o zmiennej
liczbie składników, w której warunek zawodzący w kroku ucina budowę reszty
sekwencji (tamże, p. 4.2.2 i 4.2.3, gdzie stoi też cena: komplikacja zapisu reguł).
Ruchem jest dopisanie ich do
[mechanizmów](../docs/swigra.md#what-the-code-does-that-olski-should-take),
a do przeczytania jest przy każdym `gfjp2.dcg` obok książki,
bo tamta sekcja powstała z kodu
i dopisanie do niej z książki może dać drugą kopię tego, co już tam stoi.
Rozstrzygnąć trzeba też, czy każdy z tych trzech jest mechanizmem:
przecinkowość Woliński sam nazywa ceną formalizmu,
więc może chcieć innego miejsca niż dwa pozostałe.

Przebieg nad prozą README nic nie kosztuje, a zdanie spoza podzbioru
przeżyło w tym pliku pięćdziesiąt kilka commitów:
`Czytania szynki dzieli szyk oraz gospodarz frazy` miało liczbę pojedynczą
przy podmiocie z dwóch członów.
[`docs/roadmap.md`](../docs/roadmap.md#readme-jest-przyrządem-pomiarowym) zakłada,
że ten przebieg wykona każda sesja.
Ruchem jest test żądający, żeby każde odrzucenie w tej prozie było jednym z tych,
które tamta sekcja wylicza.
Ceną są dwie rzeczy: wyliczenie stoi wtedy drugi raz,
a test czerwienieje po redakcji README, a nie po zmianie w gramatyce.

Zdanie `nad README nie rusza ani jednego werdyktu` w
[`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika)
zmierzono nad tekstem sprzed redakcji,
czyli nad plikiem, który miał jeszcze sekcję o dwóch listach i spis dokumentów.
Ruchem jest sonda różnicowa nad prozą dzisiejszą
(`python3 -m harness.markdown README.md --into proza/`)
i poprawka tego zdania, o ile przebieg zastanie je nieprawdziwym.
Predykat sondy do drzewa nie wchodzi, więc pisze się go na nowo
([`CLAUDE.md`](../CLAUDE.md#code)).
Wpis waży tyle, ile waży to jedno zdanie:
zdania skreślone werdyktu mu nie odbiorą,
więc ruszyć je może tylko zdanie dopisane po pomiarze.

Orzekanie przez zaprzeczenie stoi w prozie tego repozytorium setki razy.
Zdanie tej klasy niesie predykację w członie zanegowanym,
a po skreśleniu tego członu nie mówi nic:
`Cięcie nie jest granicą konstrukcji.` w README stoi tak dalej,
a sam zwrot „a nie” pada w `docs/konstrukcje-gramatyczne/` przeszło sto razy.
Ruchem jest przebieg z jednym pytaniem na zdanie —
co zostaje po skreśleniu członu zanegowanego —
i zdanie twierdzące tam, gdzie nie zostaje nic;
wykluczenie, które ktoś naprawdę by zaproponował, zostaje
([`CLAUDE.md`](../CLAUDE.md#a-phrase-that-arrived-ready-made-was-not-chosen)).
Do przeczytania jest cena po stronie gramatyki:
zdanie zanegowane wychodzi jednoznaczne przez dopełniacz,
więc taki przebieg kupuje czytelność kosztem jednoznaczności
([`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md#cena-którą-olski-zostawia-w-prozie)).
Kto podnosi ten wpis, rozstrzyga też, czy klasa jest robotą ręczną,
czy pierwszym wzorcem dla wykrywacza z [listy celów](../docs/roadmap.md#cele).

Prozy tych dokumentów nikt nie przeczytał pod jednym pytaniem:
czy to zdanie przeżyje następną produkcję.
Jedna sesja znalazła trzy zdania, które go nie przeżyły,
i żadnego z nich nie łapał zakaz liczby kruchej
([`CLAUDE.md`](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)): stosunek zgrubny w miejscu liczby,
zdanie o kierunku, w którym rusza się pokrycie,
oraz akapit liczący produkcje `olski/subset/` za sam kod.
Ruchem jest przebieg po `docs/` z tym jednym pytaniem na zdanie,
a po nim albo granica w miejsce środka, albo wniosek ze wskaźnikiem
na właściciela w miejsce drugiej kopii.
Pytanie obejmuje przy tym zdanie obok liczby, a nie samą liczbę:
odsyłacz „czym są te trzy” przeżył akapit,
w którym trzy zdania zrobiły się dwudziestoma kilkoma.
Do przeczytania są te trzy zdania już poprawione —
dwa w [`docs/corpus.md`](../docs/corpus.md#the-measurement)
i akapit pod listą pozycji przyłączeniowych w
[`docs/subset.md`](../docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie) —
bo one, a nie liczba dokumentów, mówią, ile ten przebieg kosztuje.
Czwarte takie zdanie liczyło ciała `rdzeń_względny` przed przeczeniem i po nim,
a rozwinięcie szyku wypisuje ich od tamtej pory rząd wielkości więcej,
więc zostaje po nim sama krotność: przeczenie podwaja te ciała.
Cen wpuszczenia ten wpis nie obejmuje:
właścicielem każdej z nich jest sekcja konstrukcji
w `docs/konstrukcje-gramatyczne/`,
a plan etapów i dokumenty rejestrów ich nie powtarzają: cena stoi przy konstrukcji,
a przebieg, którym ją policzono, stoi w gicie
([`docs/ustawy.md`](../docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)).
Właściciel trzyma ją w rzędzie wielkości albo granicą, a nie w pełnej precyzji,
i mówi to [jego wstęp](../docs/konstrukcje-gramatyczne/README.md).
Jedna cena stoi poza tą regułą i stoi tak dlatego, że nie ma sekcji:
koordynację wycenia [etap 4](../docs/roadmap.md#etap-4-zdanie-złożone),
bo `docs/konstrukcje-gramatyczne/podrzędność.md` ma sekcję o tym,
co ją dzieli od podrzędności,
a nie o tym, co jej wpuszczenie kosztowało.

Nazwa `parser` obejmuje w tych dokumentach cały tor gramatyczny,
a nazywa jedną z pięciu warstw, przez które przechodzi zdanie.
Właścicielem nazwy jest [`docs/roadmap.md`](../docs/roadmap.md#co-jest-budowane),
który pisze „parser zaprojektowanego podzbioru polszczyzny”,
a używają jej README, `docs/disambiguation.md`, `docs/design-notes.md`
oraz trzy dokumenty podzbioru, razem w kilkudziesięciu miejscach.
`docs/parsowanie.md` ma to słowo w nazwie i obejmuje nim cały kierunek.
Przemianowanie toru sięga więc i tego pliku.
Do przeczytania jest tabela warstw w
[`docs/architecture.md`](../docs/architecture.md#pięć-warstw-toru-gramatycznego),
gdzie składnia jest warstwą drugą, a werdykt wypowiedzią o czterech pod nim, oraz
[`docs/parsowanie.md`](../docs/parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań),
gdzie wyjściem jest zapytanie o las, a nie drzewo ani lista drzew.
Ruchem jest albo przemianowanie toru na werdykt, czyli na to, co polecenie wydaje,
albo zdanie u właściciela mówiące, że jedna warstwa nazywa tu cały tor.
Jedno i drugie idzie w jednej zmianie, bo nazwa sięga wszystkich swoich wystąpień
([`CLAUDE.md`](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).
Przeciw przemianowaniu: `olski/parse/` i `olski-check` noszą to słowo,
a [`docs/swigra.md`](../docs/swigra.md) porównuje olskiego ze Świgrą jako parser z parserem,
więc przekład nazwy rozjeżdża to porównanie z polem.

Status werdyktu jest po angielsku — `valid`, `ambiguous`, `rejected`,
`unclosed`, `fragment` — a wydruk komendy go nie ma.
Zostaje znaczek na stronie, gdzie polskie zdanie stoi obok niego w legendzie
(`witryna/strona.html`), oraz słowo, którym pomiar nazywa swoją klasę.
Napis ten jest zarazem klasą CSS strony (`witryna/styl.css`),
wartością pod kluczem JSON-a, słowem tabeli `olski-pokrycie`
oraz tym, o co pyta kilkanaście testów i sond w `harness/`,
więc przekład sięga ich wszystkich i idzie jednym commitem.
Powód przekładu zeszedł przez to do samego znaczka:
reguła językowa obejmuje wydruk narzędzia,
a nie słowo, po którym pomiar nazywa swoją kolumnę.
Do rozstrzygnięcia jest przy tym `Result.status` w `olski/parse/podsumowanie.py`
obok `Verdict.status` w `olski/werdykt.py`:
nazwy właściwości zostają angielskie przy polskich wartościach,
czyli daje to mieszaninę, której nazwy symboli nie mają
(`DEKLARACJA` w `olski/subset/deklaracja.py`).

Wydruk `olski-pokrycie` jest po angielsku tak samo jak tamten,
a [reguła językowa](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie) obejmuje oba.
Przekłada się go w całości albo wcale, bo etykieta dopisana po polsku daje
mieszaninę wewnątrz jednej tabeli: `NO_STRUCTURE` i `NO_LICENCE`
w `olski/pokrycie.py` stoją w kolejce blokerów parą i czyta się je obok siebie.
Nazwy części mowy w tej samej kolejce zostają, bo są nazwami tagsetu,
czyli tym, czego się tu nie wybiera.
Ten sam wydruk drukuje `harness/pomiar.py` nad bankiem drzew,
więc przekład obejmuje obie komendy naraz.
Do przeczytania jest `render` w tym pliku, bo wierszy jest tam więcej niż ta para —
nagłówki tabel, powody pominięcia, wiersze krzywej pokrycia —
i to one mówią, ile ten przekład kosztuje.
Wpisu tego nie zamyka commit tamtego: tamten przekłada jedno słowo,
a ten cały wydruk innej komendy,
a bloków w dokumentach `olski-pokrycie` nie ma,
bo `tests/test_wydruki.py` pilnuje tylko tych, które odtwarzają się bez korpusu.

Docstring modułu bywa dłuższy od sekcji dokumentu i niesie wywód sięgający kilku
modułów, którego właścicielem jest według
[`CLAUDE.md`](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely) dokument.
`olski/skład/przegląd.py` zestawia się z `harness/wieloznaczność.py` przez dwa tory,
`harness/wybory.py` wywodzi, który korpus umie ocenić którego świadka,
a `harness/walenty.py` opowiada, od jakich domyślności odejmują jego zdania.
Skreślić tego nie wolno, bo drugiej kopii nie ma,
więc ruchem jest, per docstring, albo zdanie ze wskaźnikiem na sekcję,
która ten wywód przyjmuje — `docs/sklad.md`, `docs/rozstrzyganie.md`,
`docs/warstwa-leksykalna.md` — albo powód zapisany przy docstringu,
czemu wywód czyta się przy kodzie, a nie w dokumencie.
Do przeczytania jest ten trzeci:
czytania Walentego nie powtarza żaden dokument,
więc stoi on najbliżej granicy i on mówi, ile ten ruch jest wart.

Przecinek przed `i` stoi w tej prozie setki razy i nie wiadomo, ile z tych miejsc
jest poprawnych. Polska interpunkcja stawia go tam tylko wtedy, gdy domyka zdanie
podrzędne albo wtrącenie, a w `docs/architecture.md` pięć zdań miało go bez żadnego
z tych dwóch powodów; znalazł je werdykt `rejected`, bo o interpunkcji nie mówi tu
ani jedna reguła prozy
([`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md#odrzucenie-bywa-poprawką)).
Ruchem jest przejść wystąpienia `, i` w prozie polskiej tego repozytorium i skasować
te, które niczego nie domykają.
Do przeczytania jest samo zdanie przy każdym z nich, bo tego nie policzy żaden
przebieg: olski odrzuca zarazem zdania, w których ten przecinek jest na miejscu,
a zawodzi coś innego, więc werdykt sam wystąpień nie rozdziela.
Sesja dzieli się po plikach, bo każde wystąpienie rozstrzyga się osobno.
Wpis jest mniejszy, niż mówi liczba wystąpień:
w `docs/design-notes.md` i w `docs/roadmap.md` większość domyka zdanie podrzędne
albo powtarza spójnik, a z garści, która zostaje, część żąda przepisania zdania:
`a liczba nie, i` bez przecinka zestawia przeczenie ze spójnikiem.

Strona nie przedstawia drugiego toru, a nazywa go dwa razy:
w ostatniej pozycji listy zastosowań i w akapicie nad makietą
(`witryna/strona.html`).
Wprowadzenie mówi o samym parserze, więc czytelnik z zewnątrz
([`docs/roles.md`](../docs/roles.md#ktoś-kto-trafia-tu-pierwszy-raz))
dostaje nazwę, której nikt mu nie przedstawił
([`CLAUDE.md`](../CLAUDE.md#the-reader-goes-sentence-by-sentence)).
To samo dotyka zdania nad listą: obiecuje ono jeden komponent,
a ostatnia pozycja mówi o składzie, czyli nie o nim.
Ruchem jest jedno zdanie we wprowadzeniu strony, które nazywa oba tory,
oraz przepisane zdanie nad listą.
Do przeczytania jest
[`docs/roadmap.md`](../docs/roadmap.md#po-co-tory-są-dwa),
bo mówi, czym tory się różnią, a zdanie na stronie ma być od niego zgrubniejsze
([`docs/witryna.md`](../docs/witryna.md#strona-zaczyna-od-tego-czym-olski-jest)).

Parę zdań odrzucone i przechodzące powtarza dla jednej konstrukcji kilka miejsc naraz,
a właściciela nie wyznaczył nikt.
W `docs/subset.md` wylicza je punkt listy
[czego olski nie bierze](../docs/subset.md#what-it-does-not-cover-yet),
kolejka zamykająca sekcję
[o zaimkach `kto` i `co`](../docs/konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)
oraz akapit sekcji
[o wolnym celowniku](../docs/warstwa-leksykalna.md#wolny-celownik-nie-jest-pozycją-ramy-i-nie-wchodzi-leksykonem),
a czwarty raz, ułożone częstością zawrócenia, wylicza je
[`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md#czego-brakuje-najbardziej).
Sześć wpisów sekcji o konstrukcjach, których gramatyka nie ma,
przepisuje tę parę słowo w słowo: pięć za tamtą kolejką, jeden za tamtym akapitem.
Obydwa te miejsca kończą się przy tym zdaniem oddającym ruch do tego pliku,
więc powtórzenie nie jest kontekstem dla wpisu, tylko drugą kopią.
Ruchem jest rozstrzygnięcie, które z tych miejsc jest właścicielem pary,
a nie skrócenie sześciu wpisów po kolei:
skrócić da się je równie dobrze z drugiej strony,
czyli tam, gdzie lista ruch i tak oddaje.
Do przeczytania są te cztery wyliczenia naraz, bo każde pisze tę samą parę
dla innego czytelnika, oraz [`docs/roles.md`](../docs/roles.md),
bo od roli zależy, komu ta para jest w tym miejscu potrzebna.

[`docs/linter.md`](../docs/linter.md) jest dwoma dokumentami w jednym.
Sekcja [o czterech osiach](../docs/linter.md#cztery-osie-każdej-reguły)
i wniosek pod tabelą poziomów mówią o linterze, który jest celem.
Reszta opisuje wycofany pakiet reguł.
Granicę między jednym a drugim niesie dziś jedno zdanie,
a nazwa dokumentu jej nie widzi.
Ruchem jest rozcięcie na dwa dokumenty:
jeden o regule, którą ktoś dopiero napisze, drugi o pakiecie, który wyszedł.
Do przeczytania jest przedtem, które sekcje idą po której stronie,
bo [`CLAUDE.md`](../CLAUDE.md#the-reader-goes-sentence-by-sentence),
[`docs/prose-linters.md`](../docs/prose-linters.md)
i [`docs/fiction.md`](../docs/fiction.md)
linkują tabelę poziomów jako rzecz dzisiejszą,
a resztę tamtego dokumentu jako zapis.

Bloki Markdowna czyta w tym repozytorium jeden program wzorcem, a drugi parserem.
`_ogrodzone` w `tests/test_wydruki.py` szuka ogrodzeń po wierszach,
bo `_wydruki` obok potrzebuje numeru wiersza:
paruje blok poleceń z wydrukiem stojącym pod nim.
`wstawki` w `harness/cytaty.py` pyta o to samo `markdown_it`,
czyli tak, jak granicę między parserem a decyzją stawia `harness/markdown.py`.
Różnica nie jest kosmetyczna: wzorzec po wierszach czyta ciąg backticków
otwierający blok tak samo jak wstawkę i nie schodzi do pozycji listy.
Ruchem jest przepisanie tamtego czytnika na tokeny,
bo `markdown_it` daje pod `map` zakres wierszy, którego to parowanie potrzebuje.
Do przeczytania jest `_wydruki`, a nie sam `_ogrodzone`, bo to ono liczy na numery.
Zbiór plików wypisują przy tym trzy miejsca i nie jest on w nich ten sam:
`DOCUMENTS` w `tests/test_docs.py` oraz `domyślne` w `harness/cytaty.py`
biorą korzeń wraz z `docs/` i `todo/`, a `_wydruki` pomija `CLAUDE.md` i `todo/`,
więc bloku wydruku wklejonego do tych dwóch nie pilnuje nic.

Dwie sekcje `CLAUDE.md` opisują jedną rodzinę usterek rejestru
i odsyłają do siebie nawzajem:
[fraza gotowa](../CLAUDE.md#a-phrase-that-arrived-ready-made-was-not-chosen)
pyta, czy słowo zostało wybrane,
a [adresat](../CLAUDE.md#dla-kogo-jest-napisane-zdanie) pyta, dla kogo zdanie napisano.
Razem zajmują siódmą część pliku, który każda sesja czyta w całości.
Ruchem jest jeden katalog chwytów zamiast dwóch,
zamknięty jednym akapitem, bo oba akapity zamykające mówią dziś to samo:
że trafienie jest wezwaniem do przeczytania zdania, a nie werdyktem.
Do przeczytania jest, które pary chwytów są tą samą usterką —
urzędowa fraza gubi wykonawcę, a wymyślony sprawca wstawia w jego miejsce abstrakcję —
oraz czy zwinięcie zachowa granicę między wywodem a instrukcją,
bo ona rozstrzyga, gdzie te chwyty wolno zostawić.

[Splitting work across sessions](../CLAUDE.md#splitting-work-across-sessions)
odpowiada planiście dzielącemu partię wpisów,
a `CLAUDE.md` pisany jest pod sesję, która podział dostaje już zrobiony
([docs/roles.md](../docs/roles.md#sesja-agenta)).
Każda sesja czyta przez to kilkadziesiąt wierszy,
a potrzebuje ich tylko ta, która taką partię układa.
Ruchem jest przeniesienie sekcji do właściciela i zdanie z linkiem w jej miejscu,
bo [sesja agenta](../docs/roles.md#sesja-agenta) wskazuje ją
jako jedną z trzech rzeczy, które robią tej roli całą drogę.
Do rozstrzygnięcia jest właściciel, a dwaj kandydaci różnią się ceną.
[Planista](../docs/roles.md#planista) już nazywa tę postawę,
a do `docs/roles.md` wchodzi tylko ten, kto po niego przyszedł.
Nagłówek tego pliku mówi, czym jest pojedynczy wpis,
a sekcja mówi, co robi się z partią wpisów — tylko że
[sesja agenta](../docs/roles.md#sesja-agenta) czyta i ten plik w całości,
więc przeniesienie tam zostawia te wiersze w każdej sesji.

Dwa zdania [`docs/corpus.md`](../docs/corpus.md#where-the-analyses-stop) wskazują
[listę braków](../docs/subset.md#what-it-does-not-cover-yet), a nazywają konstrukcje wpuszczone.
Zdanie o `czy` przy wierszu `qub` mówi, że pytania o rozstrzygnięcie ta gramatyka nie ma,
a `Czy to działa?` i `Pyta, czy to działa.` wyprowadzają się
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą)).
Zdanie o spójnikach, pod którymi stoi tryb przypuszczający, przy wierszu `comp`
mówi to samo o nich, a `Gdyby ustawa obowiązywała, cena byłaby niska.`
i `Poseł mówi, żeby ustawa obowiązywała.` wyprowadzają się.
Wiersz nazywa część mowy, a nie konstrukcję, więc po wpuszczeniu zostaje
i mówi odtąd o tym, czego wpuszczony kształt nie obejmuje —
akapit wyżej mówi to o czterech innych wierszach, a przy tych dwóch tego zdania brakuje.
Ruchem jest w każdym z nich zdanie mówiące, na czym te zatrzymania stoją dzisiaj,
a do przeczytania są same zatrzymania obu wierszy nad Składnicą,
bo bez nich zostaje samo skreślenie wskazania.

Zdanie [`docs/corpus.md`](../docs/corpus.md#what-morphological-ambiguity-costs)
o klasie, którą morfologia żywa przyjmuje sama, mówi „a large part of them”
i jest to oszacowanie bez pomiaru pod spodem.
Klasę mierzono, zanim łącznik `to` dostał ciała przy kopuli,
a te zabrały jej członków: `To są oczywistości.` przyjmują odtąd obie morfologie.
Ruchem jest porównanie zbiorów zdań przyjętych pod obiema morfologiami,
po którym zdanie dostaje z powrotem stopień albo traci go na dobre.
Polecenia na to porównanie nie ma i jest to ten sam brak,
o którym mówi wpis o dwóch przebiegach całego korpusu.

Drabina głębokości w [`docs/linter.md`](../docs/linter.md#how-deep-does-each-rule-have-to-see)
kończy się na pełnym rozbiorze, a cel o żądaniu czasownika
([`docs/roadmap.md`](../docs/roadmap.md#cele)) nie mieści się na niej:
reguła mówiąca, czego czasownik żąda od swojej pozycji,
potrzebuje słownika znaczeń ponad rozbiorem, a takiego wiersza tabela nie ma.
Ruchem jest piąty wiersz albo zdanie pod tabelą,
że drabina kończy się tam, gdzie zaczyna się słownik znaczeń.
Do przeczytania jest sekcja o czterech osiach z tego samego dokumentu:
głębokość jest tam osią każdej reguły, więc dopisany wiersz rusza i ją.
Reguł to nie dotyczy ani jednej:
każda, która weszła do wycofanego pakietu, rozstrzygała się na znaku.
