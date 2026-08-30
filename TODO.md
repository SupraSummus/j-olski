# Work to do in the repository

The running list of work inside the repository itself:
rewrites, merges, documents that have drifted apart,
dangling references, gaps, and code worth improving.
Something noticed while working on another topic goes here
instead of stretching the current change or being forgotten.
[The review pass](CLAUDE.md#przegląd-sprawdza-zmianę-wobec-całego-tego-pliku) is the other way in:
a refactor too large to do on the spot is written down rather than started,
and the review also checks whether a change deleted the entries it closes.
Read the section your work touches before starting,
because it names the problems somebody has already found there.
The list as a whole is longer than anybody reads,
which is what the sections below are for.

Lista nie przypisuje wpisów do torów i nikt nie podnosi ich po kolei,
bo wpis notuje tylko to, na co ktoś trafił przy innej robocie.
[docs/roadmap.md](docs/roadmap.md#co-jest-budowane) mówi, co jest budowane.

An entry belongs here only if a commit in this repository closes it.
A question the outside world answers is not work in the repository,
and the document that owns the topic keeps it:
[`docs/open-questions.md`](docs/open-questions.md)
or a document's own `Not yet decided`.
The next move is the tell:
waiting for somebody else's answer is an entry there,
a file to write is an entry here.

A register, not a changelog:
an entry that closes is deleted by the same commit that settles it,
which is the done-marker rule from
[`CLAUDE.md`](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
applied to this file.

One paragraph per entry, paragraphs separated by a blank line,
lines inside them broken [semantically](CLAUDE.md#semantic-line-breaks),
and no bullets or numbering,
so that adding or removing an entry gives a clean diff
and leaves its neighbours alone.
Numbering renumbers everything below an entry landing in the middle,
and a bullet indents prose that is meant to read as prose.

Podział na sekcje zachowuje ten czysty diff,
więc każdy wpis należy do jednej sekcji.
Nazwa sekcji mówi, czego wpis dotyka, a nie co jest budowane.
Wpis sięgający dwóch sekcji dopisz do tej,
która obejmuje dowód do przeczytania,
bo od dowodu zaczyna ten, kto wpis podnosi.
Sekcję bez wpisów skasuj razem z jej ostatnim wpisem,
a nową sekcję załóż dopiero wtedy, gdy masz do niej wpis.

An entry that names another one names it by what it is about.
A section name does not identify one, since a section holds many,
and a pointer saying which way to scroll is wrong
as soon as anything lands between the two.

Write so that an entry can be picked up cold,
and name the concrete next move —
what actually has to change in the text or in the code.
"Check some day" is a hope, not a move.
Name the evidence to read as well, and not only the files to change,
because two entries over disjoint files can turn on one judgment
that a file list does not show,
and what such an overlap costs is in
[splitting work across sessions](CLAUDE.md#splitting-work-across-sessions).

Wpis nie jest rozstrzygnięciem, bo autor pisał go przy innej robocie
i dał mu tyle uwagi, ile zostało.
Pewne jest w nim jedno: autor na coś trafił.
Kto wpis podnosi, dochodzi więc do ruchu sam
i traktuje nazwany ruch jako propozycję, a nie jako polecenie.
Czasem wychodzi mu ruch inny, a czasem żaden,
bo problemu nie ma albo naprawa kosztuje więcej, niż jest warta;
wtedy całą zmianą jest skasowanie wpisu, z powodem w komunikacie commita.

## Dokumenty i konwencje

Wskazania między `docs/subset.md` i `olski/subset.py` idą w obie strony,
a pilnowane są tylko w jedną.
Ćwierć wskazań z `olski/subset.py` nie ma anchora,
więc `tests/test_docs.py` sprawdza przy nich sam plik,
a kilka zdań dokumentu opiera się na nazwie w środku modułu,
której nie pilnuje nic ([CLAUDE.md](CLAUDE.md#na-czym-wolno-oprzeć-zdanie)).
Ruchem jest anchor przy każdym wskazaniu z kodu,
a po stronie dokumentu nazwa modułu w miejsce nazwy w jego środku —
tam, gdzie zdanie nadal mówi czytelnikowi, gdzie szukać.
Wskazania na `morphology`, `po_przyimku` i `po_słowie` są tu przypadkiem
najtrudniejszym, bo dokument opisuje kolejność tych trzech warstw
i nazwa modułu tego nie odda.

Komentarz w pozostałych modułach powstał pod regułą, która żądała wywodu
przy każdym ciele, a nie pytała, czy z kodu widać to samo bez niego;
[reguła dzisiejsza](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely)
zostawia komentarz tam, gdzie rozkmina jest głębsza od kodu.
Ruchem jest ten sam przebieg nad `olski/parse.py`, `olski/grammar.py`,
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
[`docs/subset.md`](docs/subset.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)
opisuje `olski/leksykon.txt`, przeliczają się z tego pliku jednym `cut`-em,
a trzy z nich rozeszły się z nim w commicie, który pisał obie strony;
znalazło je dopiero przeliczenie ręką.
`tests/test_docs.py` pilnuje nazw plików i sekcji,
`tests/test_wydruki.py` bloków stojących pod komendą,
a liczby wziętej z pliku nie pilnuje nic
([CLAUDE.md](CLAUDE.md#na-czym-wolno-oprzeć-zdanie)).
Ruchem jest check przeliczający je z tego pliku, wzorowany na tym,
czym `tests/test_docs.py` trzyma [blok checków](CLAUDE.md#checks) równy workflowowi.
Do rozstrzygnięcia jest, czy warto: klasa jest dziś tą jedną sekcją
i jedną liczbą poza nią, czyli `998 par` w
[`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
a check czytający liczbę z prozy wyrażeniem regularnym
czerwienieje po przeredagowaniu zdania, a nie po zmianie w danych.

Dawną nazwę odczytania — `czytanie` — noszą pozostałe dokumenty,
nazwy w kodzie i nazwy plików
`harness/czytania.py` oraz `tests/test_czytania.py`.
Nazwę rozstrzyga
[sekcja o tym, co się liczy jako jedno odczytanie](docs/subset.md#co-się-liczy-jako-jedno-odczytanie).
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

`docs/subset.md` jest dokumentem mieszanym.
Polskie sekcje dopisano tam do angielskiego dokumentu,
a [reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
przewiduje dla takiego pliku przekład całości, osobną zmianą.
Ruchem jest przekład reszty, jednym commitem.
Wpis ważył więcej, dopóki lista plików była zasięgiem checka;
checka nie ma, więc został sam przekład.
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
[mechanizmów](docs/swigra.md#what-the-code-does-that-olski-should-take),
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
[`docs/roadmap.md`](docs/roadmap.md#readme-jest-przyrządem-pomiarowym) zakłada,
że ten przebieg wykona każda sesja.
Ruchem jest test żądający, żeby każde odrzucenie w tej prozie było jednym z tych,
które tamta sekcja wylicza.
Ceną są dwie rzeczy: wyliczenie stoi wtedy drugi raz,
a test czerwienieje po redakcji README, a nie po zmianie w gramatyce.

Prozy tych dokumentów nikt nie przeczytał pod jednym pytaniem:
czy to zdanie przeżyje następną produkcję.
Jedna sesja znalazła trzy zdania, które go nie przeżyły,
i żadnego z nich nie łapał zakaz liczby kruchej
([`CLAUDE.md`](CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)): stosunek zgrubny w miejscu liczby,
zdanie o kierunku, w którym rusza się pokrycie,
oraz akapit liczący produkcje `olski/subset.py` za sam kod.
Ruchem jest przebieg po `docs/` z tym jednym pytaniem na zdanie,
a po nim albo granica w miejsce środka, albo wniosek ze wskaźnikiem
na właściciela w miejsce drugiej kopii.
Pytanie obejmuje przy tym zdanie obok liczby, a nie samą liczbę:
odsyłacz „czym są te trzy” przeżył akapit,
w którym trzy zdania zrobiły się dwudziestoma kilkoma.
Do przeczytania są te trzy zdania już poprawione —
dwa w [`docs/corpus.md`](docs/corpus.md#the-measurement)
i akapit pod listą pozycji przyłączeniowych w
[`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie) —
bo one, a nie liczba dokumentów, mówią, ile ten przebieg kosztuje.
Czwarte takie zdanie liczyło ciała `RelativeCore` przed przeczeniem i po nim,
a rozwinięcie szyku wypisuje ich od tamtej pory rząd wielkości więcej,
więc zostaje po nim sama krotność: przeczenie podwaja te ciała.
Cen wpuszczenia w pełnej precyzji ten wpis nie obejmuje:
właścicielem każdej z nich jest sekcja konstrukcji w `docs/subset.md`,
gdzie są przypięte do gramatyki z chwili pomiaru,
a plan etapów i dokumenty rejestrów ich nie powtarzają: cena stoi przy konstrukcji,
a przebieg, którym ją policzono, stoi w gicie
([`docs/ustawy.md`](docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)).
Czy właściciel ma trzymać ją dokładną, czy w rzędzie wielkości, nie rozstrzygnął nikt.
Jedna cena stoi poza tą regułą i stoi tak dlatego, że nie ma sekcji:
koordynację wycenia [etap 4](docs/roadmap.md#etap-4-zdanie-złożone),
bo `docs/subset.md` ma sekcję o tym, co ją dzieli od podrzędności,
a nie o tym, co jej wpuszczenie kosztowało.

Nazwa `parser` obejmuje w tych dokumentach cały tor gramatyczny,
a nazywa jedną z pięciu warstw, przez które przechodzi zdanie.
Właścicielem nazwy jest [`docs/roadmap.md`](docs/roadmap.md#co-jest-budowane),
który pisze „parser zaprojektowanego podzbioru polszczyzny”,
a używają jej README, `docs/disambiguation.md`, `docs/design-notes.md`
i `docs/subset.md`, razem w kilkudziesięciu miejscach.
Do przeczytania jest tabela warstw w
[`docs/architecture.md`](docs/architecture.md#pięć-warstw-toru-gramatycznego),
gdzie składnia jest warstwą drugą, a werdykt wypowiedzią o czterech pod nim, oraz
[`docs/design-notes.md`](docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań),
gdzie wyjściem jest zapytanie o las, a nie drzewo ani lista drzew.
Ruchem jest albo przemianowanie toru na werdykt, czyli na to, co polecenie wydaje,
albo zdanie u właściciela mówiące, że jedna warstwa nazywa tu cały tor.
Jedno i drugie idzie w jednej zmianie, bo nazwa sięga wszystkich swoich wystąpień
([`CLAUDE.md`](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).
Przeciw przemianowaniu: `olski/parse.py` i `olski-check` noszą to słowo,
a [`docs/swigra.md`](docs/swigra.md) porównuje olskiego ze Świgrą jako parser z parserem,
więc przekład nazwy rozjeżdża to porównanie z polem.

Nazwy, które werdykt wypisuje jako role odczytania, są po angielsku,
a [reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
obejmuje nazwy, które w kodzie wybieramy.
Komunikaty werdyktu są polskie, a te nazwy nie,
bo `Subject` i `Object` są zarazem symbolami gramatyki w `olski/subset.py`,
więc przekład sięga każdego wystąpienia symbolu, a nie samego wydruku.
Słownik przekłada się przy tym w całości albo wcale,
bo nazwa dopisana po polsku daje mieszaninę wewnątrz słownika.
Ruchem jest przekład jednym commitem wraz z blokami werdyktu w dokumentach,
a które to bloki, wylicza `tests/test_wydruki.py`.
Do przeczytania jest
[decyzja o gramatyce jako danych](docs/design-notes.md#decisions-taken):
symbol ma tam jedną nazwę i jest nią ta, którą drukuje werdykt,
a identyfikator jest polski, gdy symbol jest angielski.
Przekład odwraca to zdanie, więc idzie razem z nim.

Status werdyktu jest po angielsku — `valid`, `ambiguous`, `rejected`,
`unclosed`, `fragment` — i wypisują go oba wydruki:
kolumna `olski-check` oraz znaczek na stronie,
gdzie polskie zdanie stoi obok niego w legendzie (`witryna/strona.html`).
Napis ten jest zarazem klasą CSS strony (`witryna/styl.css`),
wartością pod kluczem JSON-a
oraz tym, o co pyta kilkanaście testów i sond w `harness/`,
więc przekład sięga ich wszystkich i idzie jednym commitem.
Do rozstrzygnięcia jest przy tym `Result.status` w `olski/parse.py`
obok `Verdict.status` w `olski/werdykt.py`:
nazwy właściwości zostają angielskie przy polskich wartościach,
czyli daje to mieszaninę, którą wpis wyżej odrzuca dla symboli.

Wydruk `olski-pokrycie` jest po angielsku tak samo jak tamten,
a [reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie) obejmuje oba.
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
Wpisu tego nie zamyka commit tamtego: są to dwa wydruki i dwie komendy,
a bloków w dokumentach `olski-pokrycie` nie ma,
bo `tests/test_wydruki.py` pilnuje tylko tych, które odtwarzają się bez korpusu.

Docstring modułu bywa dłuższy od sekcji dokumentu i niesie wywód sięgający kilku
modułów, którego właścicielem jest według
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely) dokument.
`olski/skład/przegląd.py` zestawia się z `harness/wieloznaczność.py` przez dwa tory,
`harness/wybory.py` wywodzi, który korpus umie ocenić którego świadka,
a `harness/walenty.py` opowiada, od jakich domyślności odejmują jego zdania.
Skreślić tego nie wolno, bo drugiej kopii nie ma,
więc ruchem jest, per docstring, albo zdanie ze wskaźnikiem na sekcję,
która ten wywód przyjmuje — `docs/sklad.md`, `docs/disambiguation.md`,
`docs/subset.md` — albo powód zapisany przy docstringu,
czemu wywód czyta się przy kodzie, a nie w dokumencie.
Do przeczytania jest ten trzeci:
czytania Walentego nie powtarza żaden dokument,
więc stoi on najbliżej granicy i on mówi, ile ten ruch jest wart.

Przecinek przed `i` stoi w tej prozie setki razy i nie wiadomo, ile z tych miejsc
jest poprawnych. Polska interpunkcja stawia go tam tylko wtedy, gdy domyka zdanie
podrzędne albo wtrącenie, a w `docs/architecture.md` pięć zdań miało go bez żadnego
z tych dwóch powodów; znalazł je werdykt `rejected`, bo o interpunkcji nie mówi tu
ani jedna reguła prozy
([`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md#odrzucenie-bywa-poprawką)).
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
([`docs/roles.md`](docs/roles.md#ktoś-kto-trafia-tu-pierwszy-raz))
dostaje nazwę, której nikt mu nie przedstawił
([`CLAUDE.md`](CLAUDE.md#the-reader-goes-sentence-by-sentence)).
To samo dotyka zdania nad listą: obiecuje ono jeden komponent,
a ostatnia pozycja mówi o składzie, czyli nie o nim.
Ruchem jest jedno zdanie we wprowadzeniu strony, które nazywa oba tory,
oraz przepisane zdanie nad listą.
Do przeczytania jest
[`docs/roadmap.md`](docs/roadmap.md#po-co-tory-są-dwa),
bo mówi, czym tory się różnią, a zdanie na stronie ma być od niego zgrubniejsze
([`docs/witryna.md`](docs/witryna.md#strona-zaczyna-od-tego-czym-olski-jest)).

Parę zdań odrzucone i przechodzące powtarza dla jednej konstrukcji kilka miejsc naraz,
a właściciela nie wyznaczył nikt.
W `docs/subset.md` wylicza je punkt listy
[czego olski nie bierze](docs/subset.md#what-it-does-not-cover-yet),
kolejka zamykająca sekcję
[o zaimkach `kto` i `co`](docs/subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)
oraz akapit sekcji
[o wolnym celowniku](docs/subset.md#wolny-celownik-nie-jest-pozycją-ramy-i-nie-wchodzi-leksykonem),
a czwarty raz, ułożone częstością zawrócenia, wylicza je
[`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md#czego-brakuje-najbardziej).
Sześć wpisów sekcji o konstrukcjach, których gramatyka nie ma,
przepisuje tę parę słowo w słowo: pięć za tamtą kolejką, jeden za tamtym akapitem.
Obydwa te miejsca kończą się przy tym zdaniem oddającym ruch do tego pliku,
więc powtórzenie nie jest kontekstem dla wpisu, tylko drugą kopią.
Ruchem jest rozstrzygnięcie, które z tych miejsc jest właścicielem pary,
a nie skrócenie sześciu wpisów po kolei:
skrócić da się je równie dobrze z drugiej strony,
czyli tam, gdzie lista ruch i tak oddaje.
Do przeczytania są te cztery wyliczenia naraz, bo każde pisze tę samą parę
dla innego czytelnika, oraz [`docs/roles.md`](docs/roles.md),
bo od roli zależy, komu ta para jest w tym miejscu potrzebna.

[`docs/linter.md`](docs/linter.md) jest dwoma dokumentami w jednym.
Sekcja [o czterech osiach](docs/linter.md#cztery-osie-każdej-reguły)
i wniosek pod tabelą poziomów mówią o linterze, który jest celem.
Reszta opisuje wycofany pakiet reguł.
Granicę między jednym a drugim niesie dziś jedno zdanie,
a nazwa dokumentu jej nie widzi.
Ruchem jest rozcięcie na dwa dokumenty:
jeden o regule, którą ktoś dopiero napisze, drugi o pakiecie, który wyszedł.
Do przeczytania jest przedtem, które sekcje idą po której stronie,
bo [`CLAUDE.md`](CLAUDE.md#the-reader-goes-sentence-by-sentence),
[`docs/prose-linters.md`](docs/prose-linters.md)
i [`docs/fiction.md`](docs/fiction.md)
linkują tabelę poziomów jako rzecz dzisiejszą,
a resztę tamtego dokumentu jako zapis.

## Komendy i sondy

`harness/pomiar.py` ma własny wiersz poleceń, choć bierze już to samo,
co bierze `harness/komenda.py`.
Stał poza nim, dopóki rozdawał ścieżki na bank drzew albo pliki prozy;
po podziale bierze sam katalog, czyli dokładnie wejście tamtego modułu,
a `--limit`, `--przykłady` i `--jobs` tamten moduł już daje.
Ruchem jest deklaracja `Komenda` zamiast tego parsera,
z `--morphology`, `--blockers` i `--examples` podanymi funkcją dopisującą argumenty.
Do rozstrzygnięcia jest przy tym język flag,
bo `harness/komenda.py` pyta o `--przykłady`, a ten przebieg o `--examples`,
i jest to ta sama decyzja, co przekład wydruku, więc oba wpisy podnosi się razem.

Kod wyjścia `olski-check` nie widzi zdania z zapomnianą kropką.
Napisu niedomkniętego nie liczy do mianownika nikt, żeby nagłówek nie psuł pomiaru
(`Verdict.punktowane` w `olski/werdykt.py`),
więc przebieg nad tekstem z jedną zapomnianą kropką kończy się zerem.
Nad prozą pisaną ręką jest to usterka do zgłoszenia,
a nad `docs/` wraz z nagłówkami — nie,
i tej różnicy komenda o sobie nie wie, bo dostaje pliki, a nie ich rodzaj.
Ruchem jest flaga, po której `unclosed` liczy się do kodu wyjścia,
albo zdanie mówiące, czemu nie liczy się nigdy.
Do przeczytania jest przebieg nad README,
bo tam ta różnica rozstrzyga o przyrządzie pomiarowym
([`docs/roadmap.md`](docs/roadmap.md#readme-jest-przyrządem-pomiarowym)).

Lista czytań mnoży odmiany zdań składowych, a mogłaby je sumować.
Wpisem na liście jest jedno czytanie, a streszczeniem czytania krotka
o słowniku na każde składowe (`describe` w `olski/parse.py`),
więc dwa składowe wieloznaczne każde na swój sposób dają tyle wpisów,
ile jest par ich odmian, po tyle wierszy każdy, ile zdanie ma składowych.
Cenę tę opisuje
[`docs/design-notes.md`](docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)
i bierze ją świadomie, więc ten wpis odwraca decyzję, a nie naprawia przeoczenie.
Ruchem jest wpis na zdanie składowe wraz z odmianami tego jednego składowego,
czyli ten sam kształt, jaki ma wiersz o konstytuencie rozbieżnym
(`Rozbieżność` w `olski/parse.py`): wpisów jest wtedy tyle, ile składowych,
a wierszy tyle, ile odmian wszystkich składowych razem.
Sam kształt jest tu łatwiejszy niż dwie decyzje, które on wymusza.
Pierwsza: czym jest to samo zdanie składowe w dwóch czytaniach,
skoro czytania rozcinają zdanie w różnych miejscach —
`Ludzie są wolni, równi i szczęśliwi.` ma czytanie o jednym składowym
i czytanie o dwóch, więc numer w krotce znaczy w nich co innego.
Druga: co liczy wtedy podpis `streszczenia odczytań` na witrynie
(`podpisOdczytań` w `witryna/skrypt.js`), bo odczytań liczyć przestaje.
Do przeczytania jest wydruk `python3 -m olski.check --readings` nad
`proza/README.txt` (`python3 -m harness.markdown README.md --into proza/`):
jedno zdanie tego pliku wychodzi tam kilkudziesięcioma streszczeniami,
a reszta pojedynczymi, więc ruch opłaca się samemu ogonowi rozkładu
i trzeba przeczytać, czy ogon jest wart osobnego kształtu listy.

Dwie sondy czytają Walentego i pytają go o różne schematy, a różnicy nie zmierzył nikt.
`harness/rama.py` odsiewa kwalifikatory `archaiczny` i `zły` przez `BRANE`,
bo schemat tak oznaczony nie należy do rejestru, o który olskiemu chodzi,
a `harness/konwersy.py` bierze wszystkie schematy lematu i o kwalifikator nie pyta wcale.
Jedna z dwóch odpowiedzi jest gorsza i nie wiadomo która:
liczba konwersów jest górnym oszacowaniem, które i tak myli się w jedną stronę
([`docs/disambiguation.md`](docs/disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma)),
więc schemat archaiczny mógł ją podnieść, a mógł nie trafić w kryterium pary.
Ruchem jest przebieg `harness/konwersy.py` z tym odsiewem i bez niego,
a potem albo `BRANE` wspólne dla obu sond, albo zapisany powód, czemu jedna go nie chce.
Do przeczytania jest `_pewność` w `harness/rama.py` oraz dwanaście par,
które tamta sonda wypisuje: jeżeli odsiew rusza liczbę, to rusza i te pary,
a wtedy należy się ich przeczytanie, a nie sama poprawiona liczba.

Zdania wklejone w prozę zmienia gramatyka, a żaden przebieg tego nie wypisuje.
Przykład przestaje wtedy pokazywać to, o czym mówi zdanie nad nim,
i widać to dopiero wtedy, gdy ktoś je puści ręką:
`tests/test_docs.py` czyta linki i anchory, a nie liczbę czytań,
a `tests/test_wydruki.py` pilnuje bloków stojących pod komendą i tych zdań nie tyka.
Wpuszczenie dopełnienia przed czasownik zdania bez podmiotu ruszyło werdykt
czternastu takich zdań, a poprawki żądały cztery, i wszystkie cztery znalazł
przebieg pisany na jedną sesję, bo w drzewie takiego nie ma.
Ruchem jest komenda wypisująca werdykt i liczbę czytań każdego zdania cytowanego
w prozie, po jednym wierszu na zdanie, żeby dwa drzewa robocze dały się porównać
diffem — tak samo jak przy zmianie, która ma tylko przyspieszyć
([`CLAUDE.md`](CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)).
Do rozstrzygnięcia jest, co jest zdaniem cytowanym:
sesja brała span kodu zaczynający się wielką literą i kończący kropką
oraz wiersze bloków `text`, i to kryterium wpuszcza nazwy plików razem ze zdaniami.
Do przeczytania jest `_ogrodzone` w `tests/test_wydruki.py`,
bo bloki czyta już ono, a różnica jest w tym, że tamto pyta komendę,
a to ma pytać gramatykę.

Polecenie powtarzające pomiar luki zlepia siedem aktów `cat`-em,
a sonda bierze je teraz osobno.
Blok w [`docs/design-notes.md`](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)
pisze `cat proza/ustawy/*.txt > proza/ustawy-razem.txt` i mierzy nad zlepkiem,
gdzie `python3 -m harness.luka proza/ustawy/*.txt` mierzy nad tymi samymi aktami
i składa z nich jeden raport.
Ruchem jest podmiana obu wierszy na jeden, a przed nią przebieg nad tym rejestrem,
bo raport scalony równa się przebiegowi nad zlepkiem tylko wtedy,
gdy każdy plik kończy się znakiem kończącym zdanie:
inaczej zlepek skleja ostatnie zdanie jednego aktu z pierwszym zdaniem drugiego,
a raport scalony tego nie robi.
Nad prozą tego repozytorium sprawdzono, że obie drogi dają wydruk co do znaku ten sam;
nad rejestrem ustaw nie sprawdził tego nikt, a bez tego podmiana rusza figury
i nic o tym nie mówi.
Wpis podnosi więc sesja, która ten rejestr ma.

`olski` chodził po katalogu, a `olski-check` bierze tylko pliki.
Widać to w poleceniu, którym
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów: stoi przed nim `find`, bo inaczej nie ma czego podać.
Komenda, która po katalogu chodziła, wyszła razem z pakietem reguł,
a chodzenia po drzewie nie ma teraz żadna z dwóch, które zostały:
`main` w `olski/check.py` i `main` w `harness/wieloznaczność.py`
czytają po prostu każdą podaną ścieżkę, więc obu rozwija się je powłoką.
Ruchem jest jedno miejsce, które schodzi po `rglob`,
bierze pliki o rozszerzeniu, które ekstrakcja pisze,
pomija katalog o nazwie zaczynającej się kropką — bo korpus stoi w repozytorium,
a jego kontrola wersji korpusem nie jest — i woła się z obu komend,
po czym `find` z tamtego polecenia znika,
a razem z nim powłoka, którą polecenia biorą tylko po to,
żeby ktoś rozwinął im glob.
Przeciw pominięciu: katalog z kropką podany wprost staje się wtedy nieosiągalny,
więc należy ono do chodzenia, a nie do testu na rozszerzenie.
Do rozstrzygnięcia jest, czy komenda mówi o plikach, które minęła:
`olski-check` ma mianownik, który tamten dokument cytuje,
więc pominięcie w ciszy zmienia figurę, o której nikt się nie dowie.
Sondy z `harness/` odpowiedziały na to pytanie odwrotnie i nie jest to niezgoda:
biorą one wiele plików prozy i rozwija im je powłoka,
bo katalog znaczy tam bank drzew i chodzenia po drzewie nie ma dla nich wolnego
(`harness/komenda.py`).
Kto ten wpis podnosi, ma więc precedens po obu stronach
i rozstrzyga, czy `olski-check` jest bliższy sondzie, czy dawnej komendzie.

Werdykt mówi jednym zdaniem trzy rzeczy, które są trzema różnymi robotami.
`no production takes „X”` pada i wtedy, gdy słownik czytania formy nie ma wcale,
i wtedy, gdy je ma, a nie sięga po nie żadna produkcja;
pierwsze naprawia wpis w `olski.toml`
([`docs/subset.md`](docs/subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)),
a drugie produkcja w `olski/subset.py`.
Trzecie jest formą, której czytania zdjęła morfologia:
`Cena niego rośnie.` wychodzi z tym komunikatem, a naprawą jest przyimek w zdaniu
([`docs/subset.md`](docs/subset.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)),
czyli ani leksykon, ani produkcja.
Ta trzecia waży najwięcej na torze pisania pod tę gramatykę
([`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md)),
bo komunikat odsyła autora do gramatyki, a poprawka stoi w jego zdaniu.
Rozdziela ją już przebieg nad korpusem: `bloker` w `olski/pokrycie.py`
daje formie opróżnionej wykluczeniem wiersz osobny od zdania bez struktury,
więc po tamtej stronie kształt jest wybrany, a werdykt mówi o tej formie
to samo, co o dwóch pozostałych.
Rozdzielenia żąda ta sama własność, którą werdykt już realizuje raz —
forma bez licencji stoi osobno od struktury bez licencji — tylko o szczebel niżej,
i ma ona właściciela w [`docs/swigra.md`](docs/swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold).
Kosztem jest wydruk, z którego jeden dokument wycina formy poleceniem:
[`docs/ustawy.md`](docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
bierze wszystko, co stoi za frazą `no production takes` do średnika,
więc drugi komunikat rozsypuje tamto polecenie, jeżeli nie da się go wyciąć tak samo.
Za tym średnikiem dopisuje się podpowiedź o cudzysłowie.
Do przeczytania jest `explain` w `olski/werdykt.py`
obok `bez_licencji` w `olski/segmentacja.py`:
formy przychodzą tam jedną krotką, więc rozdzielenie ich żąda drugiego pola
w `Verdict`, a nie samego drugiego napisu.
Ruch ten stoi przed przekładem wydruku albo za nim, ale nie razem z nim:
tamta zmiana bierze na nowo ręką każdy blok werdyktu w dokumentach.

`harness/luka.py` przepisuje z `harness/ruch.py` cały przebieg różnicowy:
liczniki, przejścia, scalanie kawałków, tryb nad prozą i tabelę,
czyli przeszło sto wierszy stojących drugi raz.
Wiersz poleceń zszedł z tej listy razem z `harness/komenda.py`,
który jest wspólny wszystkim sondom mierzącym nad korpusem,
a gramatyka wariantu zeszła z niej razem z `Sonda.gramatyki`:
wariant z luką jest dopiskiem, nie grupą zdejmowaną, i tamta sonda dopisek bierze.
Ruchem jest więc przepisanie tego pliku na tamten przebieg.
Do przeczytania są `pytania` i `Raport._konkurencja`, bo to one się nie generalizują:
warianty luki są dwiema wersjami jednego dopisku, a nie grupą na wariant,
więc pytanie o wchodzenie sobie w drogę nad nimi nie pada i pola zostają puste.
Ta sama `Sonda` zamyka drugie rozejście, które kopia zdążyła już zebrać:
oba tryby nad prozą w tym pliku wołają `check` raz na wariant,
więc segmentują ten sam tekst tyle razy, ile wariantów,
i tyle samo razy rozbierają zdanie, które olski odrzucił.
`harness/ruch.py` przestał tak robić i pomijanie zbędnych rozbiorów
ma tam jednego właściciela (`_bez_zbędnych`),
a bierze on `Sonda`, której ten plik nie ma.
Tej samej maszynerii żąda z drugiej strony wpis o porównaniu dwóch przebiegów
bez polecenia:
tam wariantem jest morfologia, a nie grupa produkcji zdjęta z olskiego,
więc ten, kto podnosi którykolwiek z dwóch, wybiera kształt dla drugiego,
i jest to jedna sesja.

`harness/konwersy.py` liczy lematy, a pytanie pod nią jest o zdania.
Wraca ona ze 144 lematami z 17 224,
czyli mówi, ilu czasowników dotyczy rama, której zdanie przechodnie samo nie wybiera,
i nie mówi, jak często taki czasownik pada bez pozycji rozstrzygającej;
[`docs/disambiguation.md`](docs/disambiguation.md#czego-brakuje-żeby-odpowiedzieć-pomiarem)
trzyma to jako czwartą rzecz nierozstrzygniętą.
Ruchem jest przebieg nad korpusem audytowym
([`docs/audit-corpus.md`](docs/audit-corpus.md#the-list)):
dla każdego zdania, które olski przyjmuje, zapytać,
czy jego czasownik jest jednym z tych lematów i czy stoi przy nim pozycja wybierająca schemat.
Do przeczytania jest przedtem cała lista par, a nie dwanaście z niej,
bo sonda sądu o parze nie wydaje, a te dwanaście mówi,
że kryterium łapie głównie celownik posiadacza (tamże),
więc przebieg nad rejestrem wart jest dokładnie tyle, ile lista, na której stanie.

Dwie sondy stoją nad jedną populacją i wołają tych samych świadków.
`harness/powtórzenie.py` i `harness/wybory.py` pytają obie o `pytania` z
`harness/wieloznaczność.py` i obie wypisują odpowiedź wraz ze zdaniem, nad którym
padła; różni je to, że pierwsza wycenia wariantem granicę akapitu i regułę
kandydata, a druga ma obok wzorzec czytany ręką
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Ruchem jest jedna sonda z flagą na wariant, bo dwa przebiegi po tym samym korpusie
rozejdą się na pierwszej zmianie w tym, co liczy się za pozycję.
Do rozstrzygnięcia jest, co się wtedy dzieje z wydrukiem: sonda pierwsza liczy
mianowniki rejestru (zdania, pierwsze w akapicie, pozycje z sąsiedztwem), a druga
liczy trafienia wobec wzorca, i jeden wydruk z obojgiem czyta się jak dwa.
Ten sam argument stoi już w drugiej sondzie po jej własnej stronie:
losowania ma ona dwa, a mianownik każdego niesie plik z wpisami,
więc scalenie dodaje trzeci tryb do dwóch, a nie drugi do jednego.
Przeciw scaleniu jest to, że wzorzec przeżyje sondę: `próba/wybory.txt` stoi poza
`harness/` właśnie dlatego, a program czytający ten plik jest najtańszą rzeczą w tej parze.

Kolejka blokerów grupuje zatrzymania po części mowy, a nad wierszami zamkniętymi
zbiera pod jedną nazwą formy żądające różnych konstrukcji: wiersz `conj` prowadzą
nad tą prozą `i` oraz `a`, a pod nimi stoją `czy`, `czyli` i `ani`
([`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md#kolejka-czytana-po-formie-mówi-to-czego-nie-mówi-po-części-mowy)).
Ruchem jest `bloker` w `olski/pokrycie.py` nazywający formę tam, gdzie każde
jej czytanie należy do klasy zamkniętej (`CLOSED_CLASS` stoi w `olski/segmentacja.py`),
a część mowy tam, gdzie nie: dla `ustawienia` przydatna jest część mowy, dla `i` napis.
Do przeczytania jest, co taki wiersz zrobi z tabelami, które ten wydruk cytują —
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop) czyta wiersze `interp`,
`conj` i `part` po nazwie — bo przemianowany wiersz żąda przeliczenia obu przebiegów
nad bankiem drzew, a nie samego dopisania zdania.
Wpis waży mniej, odkąd wiersz nazywa czytanie licencjonowane,
bo `interj` jest wierszem prawdziwych wykrzykników, a nie kryjówką dla `i`.

Sonda nad Świgrą pyta jej wydruk o czas i o łuki, a `info(trees, …)` z tego samego
wydruku pomija, więc różnicę, o którą w tym porównaniu chodzi najbardziej,
`harness/świgra.py` zostawia niezmierzoną.
Świgra liczy wyprowadzenia tam, gdzie olski liczy odczytania — `counttrees` w
`birnam_cleanforest.pl` mnoży poddrzewa, a `signature` w `olski/parse.py` kwotuje po
lematach, wartościach cech i częściach mowy — i dziś rozstrzyga to samo czytanie
źródła ([`docs/swigra.md`](docs/swigra.md#why-wrapping-it-does-not-get-there)).
Ruchem jest `trees` i `useful_edges` dopisane do `POLE`, kolumna w wydruku sondy,
a przed jednym i drugim trzecia poprawka z docstringu sondy, bez której obie te
liczby nie dochodzą do wydruku Świgry.
Decyzją, której to żąda, jest kwota: liczba drzew mówi o zapisie lasu, a nie o
wieloznaczności zdania, więc porównanie z liczbą odczytań musi powiedzieć, co nad
cudzym drzewem jest jednym kształtem — etykieta z rozpiętością czy samo nawiasowanie,
w którym łańcuchy jednoelementowe pomija się.
Druga decyzja jest o zakresie: docstring sondy deklaruje, że rzeczą mierzoną jest
czas, a nie kształt drzewa, więc ten wpis go odwraca, a nie dopracowuje.
Do przeczytania jest jedno zdanie puszczone obiema stronami: zdanie o koszcie szynki
z README wychodzi u Świgry tysiącami drzew, a u olskiego kilkoma odczytaniami,
a dopóki kwota nie jest wybrana, tych dwóch liczb nie ma jak zestawić.

Flaga `--readings` w `olski/check.py` jest po angielsku,
a stojące obok niej `--rozstrzygaj` i `--zatrzymania` po polsku,
choć [reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
obejmuje nazwy flag tak samo jak komunikaty, które komenda drukuje.
Ruchem jest `--odczytania` wraz z każdym wywołaniem w dokumentach;
bloki nad wydrukami pilnuje `tests/test_wydruki.py`, bo puszcza to, co w nich stoi,
a wystąpień w prozie nie pilnuje nic i te trzeba przejść grepem.
Do przeczytania jest przy tym
[`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md#czego-brakuje-najbardziej),
gdzie ta flaga stoi jako przykład tego, na co Morfeusz rozbiera nazwę z myślnikami.

Zmiana, która przestawia gramatykę, nie ruszając tego, co się z niej wyprowadza,
nie ma czym tego dowieść.
Odcisk z [`CLAUDE.md`](CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)
jest przebiegiem werdyktu po całej prozie:
trwa parę minut, żąda Morfeusza i mówi o zdaniach, a nie o produkcjach,
więc różnicę pokazuje dopiero na zdaniu, którego werdykt się przez nią zmienia.
Deklaracja czytana w miejsce listy wypisanej ręką nie zmienia żadnego werdyktu,
a dowodu żąda tak samo, i wtedy ostrzejszy jest odcisk samej gramatyki:
produkcje wraz z deklaracją wypisane tak,
żeby dwa drzewa robocze dały się porównać diffem.
Ruchem jest komenda, która to drukuje.
Do przeczytania jest `_wypisz` w `olski/grammar.py`:
odcisk pisany w sesji wypisał kilkadziesiąt różnic, których nie było,
bo `repr` zbioru szedł kolejnością haszy losowanych przy starcie
([`CLAUDE.md`](CLAUDE.md#code)).
To jedno miejsce jest naprawione,
a komenda ma oszczędzić następnej sesji pisania tego skryptu razem z tą pomyłką.

## Korpusy, ekstrakcja i figury

Only one of the corpora in
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken)
is counted by a program this repository holds.
`harness/markdown.py` reads Markdown,
which is what the KSeF figures there are taken with,
while NKJP is XML, Śmigiel is JSONL,
`python-docs-pl` is PO files and Wolne Lektury is plain-text exports,
so every figure over those is counted by hand.
One of the four needs no extraction at all,
since a text export is what olski reads,
and what it needs instead is a selection anybody can repeat:
the Wolne Lektury count in that document
runs over "the first forty `Epika` entries the catalogue returns",
which is not an order to rerun into.
[`docs/firing-rates.md`](docs/firing-rates.md#wolne-lektury)
already fetches the same library by naming every slug it takes,
so that half is a rewrite of one paragraph rather than a program.
The move is to decide, per corpus, whether it joins the harness
as an extraction beside the Markdown one,
as a fetch-and-select command in the document that cites it,
or not at all because the survey has already ruled the corpus out.

The corpus archives these documents send a reader to fetch
are pinned by URL and by nothing else.
[Składnica](docs/corpus.md#fetching-it)
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
name a release in the query string of a wiki attachment,
which says which release without saying which bytes.
`harness/świgra.py` is the one fetch that carries a digest,
and it needed one worst: `swigra_current.zip` names no release at all.
[The audit corpus](docs/audit-corpus.md#the-list) pins its members to a commit
and says what a pin is for:
so that a second person fetches the same bytes.
The corpus archives make that promise
and give a reader no way to hold anyone to it.
The move is `sha256sum` over Składnica and over NKJP,
with the digest beside the command that fetches it,
the way `harness/świgra.py` carries one,
which turns a substitution upstream into a failed check
rather than a figure that quietly stops reproducing.

The corpora these documents send a reader to fetch
come from hosts that gain nothing by serving them,
once per session rather than once per person,
because a Claude Code session on the web starts from an empty container.
[The Wolne Lektury run](docs/firing-rates.md#wolne-lektury)
takes 326 files at one request each from a volunteer library,
[Składnica](docs/corpus.md#fetching-it) is 92 MB
that [recomputation](CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje) makes a condition of touching the grammar,
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
is a tarball from the institute that serves Składnica.
The licences do not run in that order.
NKJP carries CC BY, which permits the redistribution a mirror is,
every Wolne Lektury file ships the library's licence in its own tail,
which that run cuts off before counting,
and Składnica is GPL,
which the fetching section raises against vendoring
and which settles nothing about mirroring,
since a mirror redistributes under Składnica's terms
whatever this repository decides about its own.
So the order of work is NKJP, Wolne Lektury, Składnica,
and the transport is the smaller half of each.
A release asset on a mirror repository holds 2 GB per file against no quota
and keeps the fetch the `curl -L` those sections print,
where git LFS asks for an install that the session clone precedes
and spends an allowance that GitHub's billing documentation puts at
1 GB stored and 1 GB of bandwidth a month, which is ten fetches of Składnica.
LFS buys that back over a binary somebody versions, and these are frozen archives.
The audit corpus needs none of it,
being clones pinned to a commit, which is what a mirror would be.
None of this starts before the entry on digests,
since a mirror nobody can check against upstream
is the second copy of a fact that
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely) warns about.

Leksykon projektu rusza liczby brane nad prozą README, bo tam zmierzono, że rusza,
a czy rusza je nad korpusem audytowym i nad rejestrem ustaw, nie sprawdził nikt,
choć oba korpusy czytają tekst tą samą drogą.
Rozstrzyga o tym jedna rzecz: czy ta proza pisze którąkolwiek formę tego leksykonu,
bo wiersz nazywa formę, której słownik nie czyta,
więc nad korpusem, który tej formy nie pisze, nie rusza on ani jednej liczby.
Ruchem jest więc grep form tego leksykonu po `proza/`,
a po nim albo przeliczenie liczb obu tych korpusów, albo zdanie mówiące,
czemu ten leksykon nad tą prozą nie rusza nic; formy wypisuje `odmiana` w
`olski/projekt.py`.

Ekstrakcja ustaw robi zdanie z pozycji wyliczenia, która jest samą nazwą,
a takie zdanie przyjmuje się na czytaniu czasownikowym:
`Kalisz.`, `Przemyśl.` i `Nowy Sącz.` są pozycjami wyliczenia okręgów wyborczych
i zajmują cztery ze 144 zdań przyjętych tego rejestru, a zdaniem żadne z nich nie jest
([`docs/subset.md`](docs/subset.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)).
Kropkę dopisuje `zdania` w `harness/ustawy.py` rozmyślnie i mówi to jej docstring:
bez niej werdyktem nad każdą pozycją każdego wyliczenia byłoby „to nie zdanie”.
Cena tej kropki jest przez to policzona po jednej stronie, a po drugiej nie:
ile pozycji wyliczenia jest zdaniem, którego czytelnik nie odrzuci, nie liczy nikt.
Ruchem jest ta druga liczba, a po niej wybór:
albo pozycja bez formy czasownikowej wychodzi bez kropki i wpada w `fragment`,
albo kropka zostaje, a cena zapisuje się przy niej.
Wykluczenie ze słownika tej klasy nie zabierze przy żadnym z dwóch wyjść,
bo czytanie czasownikowe nie jest nieodmienne
i `admissible` w `olski/segmentacja.py` po nie nie sięga.
Do przeczytania jest
[`docs/extraction.md`](docs/extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem),
bo druga ekstrakcja odpowiada na to samo pytanie odwrotnie
i werdykt `fragment` jest tam odpowiedzią wybraną.

## Gramatyka, parser i pomiar pokrycia

Trzy naprawy jednego znaku odrzucenie zgłasza trzema kształtami zamiast jednym.
`unclosed` nazywa napis, który olski czyta po domknięciu, i podaje znak
(`_domknięcie` w `olski/werdykt.py`),
cudzysłów prosty dostaje podpowiedź wpisaną osobno w `_podpowiedź` tam samo,
a brak spacji po kropce nie dostaje nic i wychodzi jako zatrzymanie na formie,
która z pomyłką autora nie ma nic wspólnego.
Świadkiem jest w każdym z trzech gramatyka — reguła strzela tam,
gdzie podmieniony znak zmienia werdykt z „no reading” na czytanie —
więc żadna nie potrzebuje kalibracji, której brak zamknął pakiet reguł
([`docs/linter.md`](docs/linter.md#co-zamknęło-pakiet-reguł)).
Ruchem jest jedna klasa napraw wraz z jednym kształtem wypowiedzi o niej,
a decyzją, którą to wymusza, czy zdanie naprawialne zostaje w `rejected`:
zostawione tam mierzy podzbiór jak dziś, a wyjęte rusza pokrycie nad korpusami.
Do przeczytania jest więc to, ile zdań Składnicy i korpusu audytowego
odrzucenie bierze za sam cudzysłów albo za brakującą spację.

Odrzucenie nie widzi małej litery na początku zdania.
`cena jest niska.` wychodzi jednym czytaniem, choć zdaniem pisanej polszczyzny nie jest.
Świadkiem jest tu norma, a nie rozbiór, bo gramatyka wyprowadza oba warianty tak samo.
Norma ma dwa wyjątki i oba trafiają w ten rejestr.
Nazwę pisaną małą literą zostawia się małą także na początku zdania,
bo granicę zdania pokazuje kropka poprzedniego
(Poradnia PWN, dr Jan Grzenia, „mała litera na początku nazwy własnej”) —
czyli to samo, co u nas rozstrzyga o `FRAGMENT`.
Pozycja wyliczenia zamknięta przecinkiem albo średnikiem zaczyna się małą literą,
bo ciągnie zdanie zaczęte przed dwukropkiem.
Blokerem jest ekstrakcja: `harness/markdown.py` zdejmuje backticki
i nie mówi nikomu, że token nimi stał,
a bez tego wyjątku pierwszego nie da się napisać —
i nie zastąpi go test na polskie słowo,
bo `odmień` i `przejrzyj` są nazwami funkcji i polskimi słowami naraz
([`CLAUDE.md`](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).
Ruchem jest więc najpierw ta informacja przeniesiona przez ekstrakcję,
a dopiero po niej kryterium, którego dowodem jest zero trafień nad prozą repozytorium:
bez wyjątków strzela ono na pierwszych zdaniach akapitów kilkadziesiąt razy
i ani razu trafnie.

`GRUPA_JEDNYM_SŁOWEM` w `olski/segmentacja.py` wypisuje części mowy,
którymi grupa imienna staje sama jednym słowem,
czyli fakt o gramatyce zapisany drugi raz obok niej.
Głowa dopisana do grupy imiennej tej listy nie ruszy,
a wtedy przytoczenie zamieni czytania napisowi, który cudzysłów bierze już jako grupę,
i napis dostanie drugie czytanie albo straci rodzaj
([`docs/subset.md`](docs/subset.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).
Rozjazdu nie widzi ani suita, ani przebieg nad prozą:
statusy ruszy dopiero napis z nową głową postawiony w cudzysłowie.
Ruchem jest pytanie gramatyki wprost, zamiast trzymania listy —
`Grammar` odpowiada dziś, czy terminal bierze czytanie
(`licencjonowane` w `olski/segmentacja.py`),
a brakuje odpowiedzi, czy bierze je terminal w produkcji grupy imiennej.
Do rozstrzygnięcia jest, czy to pytanie warto do `Grammar` dopisać,
czy taniej jest pilnować listy testem, który dla każdej głowy grupy
żąda jednego czytania od napisu w cudzysłowie.

Lista predykatywów nie ma `pora` ani `nie sposób`,
a Składnica ma zdania, które orzekają jednym z tych dwóch:
`Już pora.`, `Pora do łóżka!`, `Pora na nastolatki.`, `Wprost nie sposób!`
oraz `Nie sposób nie żywić uczucia podziwu dla odwagi pierwszych żeglarzy.`
Wszystkie przechodziły, dopóki `pora` czytała się czasownikiem `porać`,
a `sposób` rozkaźnikiem od `sposobić`;
zawężenie ramy do lematów całej formy te czytania zdjęło
([`docs/subset.md`](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
więc dziś są odrzucone i werdykt mówi o nich prawdę.
Ruchem jest dopisanie obu do `PREDYKATYWY` w `olski/subset.py`,
a czytanie `pred` obie formy u Morfeusza mają, więc terminal ma o co zapytać.
Trudność jest przy `nie sposób`:
przeczenie stoi w ciele osobno od predykatywu,
więc lemat `sposób` dopisany do listy wpuszcza też `sposób` bez przeczenia,
czego polszczyzna nie ma.
Do przeczytania jest, czy bank drzew ma zdanie z `sposób` bez przeczenia,
bo od tego zależy, czy sama lista tu wystarczy.

`olski/subset.py` grupuje po rodzaju, a nie po konstrukcji, więc jedna konstrukcja
rozkłada się w nim na cztery miejsca: rolę przy `DEKLARACJA`, ramę i listę lematów
wśród stałych, terminal wśród terminali i ciała w `build`.
Kto ją czyta albo zdejmuje, chodzi po tych czterech miejscach,
choć zmieniają się one razem i tylko razem mają sens —
sonda różnicowa grupuje właśnie po konstrukcji (`grupa` w `harness/ruch.py`).
Ruchem jest blok na konstrukcję: rama, lista, terminal i ciała pod jednym
nagłówkiem komentarza, w kolejności, w jakiej konstrukcje wchodziły.
Ceną są dwie rzeczy, które w bloku nie zmieszczą się nigdy: rola musi stać w
`DEKLARACJA`, bo werdykt czyta jedną listę ról, a ciało musi stać w `build`,
bo produkcje powstają w jednym wywołaniu.
Do przeczytania jest `build`: symbole używane przez kilka konstrukcji —
`Complements`, `Adjuncts`, zmienne zgodności — są w nim zmiennymi lokalnymi,
więc funkcja na konstrukcję bierze je argumentami,
a pytanie jest o to, czy sam blok komentarza nie kupuje tego samego taniej.
Rodzina czoła jest tu precedensem: jej cztery miejsca czytają jedną wartość
(`Rodzina` w `olski/subset.py`), a nie stoją pod jednym komentarzem.
Wprost się on jednak nie przenosi, bo rodzina wypisuje same nazwy symboli,
a konstrukcja wypisuje też ciała, a te powstają wywołaniem, nie wartością.
Miejsc bywa przy tym więcej niż cztery, i pokazuje to imiesłów przysłówkowy
([`docs/subset.md`](docs/subset.md#imiesłów-przysłówkowy-stoi-tam-gdzie-okolicznik-wyrażony-zdaniem)):
dochodzą przy nim wpis wśród gospodarzy oraz wpis w `NIE_WYPUSZCZANE`,
a ciała ma w dwóch miejscach `build`, bo głowa stoi osobno od swoich pozycji.

`NIE_WYPUSZCZANE` w `olski/subset.py` wylicza cechy, których symbol nie niesie
w górę, i żadnego z tych wpisów nie widać po werdykcie:
gramatyka bez całej listy wydaje nad prozą tego repozytorium
te same werdykty i te same liczby czytań, zdanie po zdaniu,
a poza `dostawka` o żadną z tych cech nie pyta nad swoim symbolem
ani jedna produkcja.
Lista trzyma więc deklarację przy tym, co produkcje wypisywały przed perkolacją.
Do rozstrzygnięcia jest jedno z trojga: lista zostaje jako fakt o symbolu,
znika i wszystko wychodzi z głowy,
albo odwraca się w inwentarz — symbol wylicza, co niesie —
i wtedy check porównuje inwentarz z pytaniami w obie strony,
czyli łapie także cechę wypuszczaną bez pytającego; takich są dwie
(liczba i rodzaj `InterrogativeCore`, wypisane razem z rodziną względną,
której poprzednik ich żąda).
Zdjęcie listy jest zmianą w gramatyce i pomiaru żąda osobno:
proza tego repozytorium nie rusza się wcale, a banku drzew nie zmierzył nikt.
Osobno stoi czas rozbioru, bo cechę wypuszczaną las rozdziela na klasy pozycji
(`klasy` w `olski/parse.py`), a wpisów jest kilkadziesiąt.
Do przeczytania jest `_wysunięta_rola` w `olski/subset.py` obok tej listy,
bo tamta funkcja pisze dwie rodziny czoła jedną ręką i stąd te dwie cechy.

Świadkowie w `olski/rozstrzyganie.py` pytają o `Przyłączenie`, czyli o obiekt składniowy,
choć warstwa powstała po to, żeby odpowiadać czymś ponad składnią
([`docs/architecture.md`](docs/architecture.md#warstwa-rozstrzygająca-wydaje-zawężenie-z-powodem-a-nie-znaczenie)).
Widać to na kopuli: powtórzenie frazy przy `być` nie dowodzi niczego o tym czasowniku,
więc lista kopul odbiera dowód, zamiast dać świadkowi pytanie, na które kopuła odpowiada
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Świadka pytającego o drzewo dziedziny zamiast o gospodarza zmierzono przed napisaniem
i wyszło, że nie miałby o co pytać:
warstwa znacząca tego rejestru nie dosięga,
więc pytanie padłoby nad jednym zdaniem wieloznacznym banku drzew z kilkuset,
coś, co liczy `python3 -m harness.znaczenia`.
Zostaje z tego kolejność:
pytanie ponad składnią stawia się dopiero za kategoriami, których ten zapis nie ma,
a pierwszą z nich jest wyrażenie przyimkowe pod grupą imienną,
czyli to samo przyłączenie, o które świadek miałby pytać
([`docs/sklad.md`](docs/sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma)).
Dopisanie jej jest jednak odwróceniem rozstrzygnięcia, a nie załataniem dziury,
bo okolicznik dochodzi w tym zapisie do zdarzenia, a nie do rzeczy,
więc kto ten wpis podnosi, zaczyna od tamtej sekcji, a nie od `olski/rozstrzyganie.py`.
Do przeczytania jest `Świadek` w tym samym pliku:
sygnatura jest jedna dla wszystkich świadków rozmyślnie,
więc świadek o innym wejściu albo tę sygnaturę rozszerza, albo staje się drugą listą,
a drugiej listy ten protokół unika z podanego tam powodu.

Skład składa `Skutek.więc` w napis, który olski od tej pory wyprowadza,
a obieg się na nim nie zamyka:
`_członowie` w `olski/skład/rozbiór.py` czyta ciało `ClauseConjunct , Clause`
i nie czyta tego z przecinkiem oraz spójnikiem,
więc `Program zapisuje ustawienia, więc linter sprawdza tekst.` wraca powodem,
że zdanie złożone tego kształtu nie ma tu kategorii.
Ruch nie jest dopisaniem czwartego kształtu do `_członowie`:
`więc` niesie relację, a nie następstwo,
i `SPÓJNIKI` w `olski/skład/spójniki.py` mówi o nim tyle samo, co o `bo`,
więc to zdanie ma wrócić okolicznikiem w relacji `skutek`, a nie `Ciągiem`.
Gramatyka wyprowadza je natomiast koordynacją, bo `więc` zdania nie podporządkowuje,
i to jest cała trudność tego wpisu: dwa tory nazywają jedną konstrukcję inaczej,
a obieg żąda, żeby napis wrócił tym drzewem, z którego wyszedł.
Do przeczytania jest `_okolicznikowe` w tym samym pliku,
czyli droga, którą wraca `bo`, i `test_zdanie_spoza_gramatyki_mówi_o_gramatyce_a_nie_o_brakującej_kategorii`
w `tests/test_rozbiór.py`, który stał na tym zdaniu i stoi teraz na narzędniku.

Okolicznik wyrażony zdaniem stoi w gramatyce przed swoim zdaniem i za nim,
a polszczyzna stawia go też w środku:
`Program, gdy linter sprawdza tekst, zapisuje ustawienia.` jest zdaniem odrzuconym.
Ruchem jest trzecie ciało `AdverbialClause` z przecinkiem po obu stronach
wraz z pozycją w ciele zdania składowego, czyli tam, gdzie dziś stoi podmiot,
a przed nim pomiar: pozycja ta konkuruje ze zdaniem względnym,
które przecinkami odgradza się tak samo
([`docs/subset.md`](docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
więc cena stoi w jednoznaczności zdań już przyjętych, a nie w liczbie ciał.
Do przeczytania jest cena obu pozycji, które ta konstrukcja już ma,
którą trzyma commit, który je wpuścił,
bo trzecia wraca z pytaniem tej samej postaci.
Tym samym brakiem jest okolicznik wewnątrz zdania względnego:
`Reguła, która rozstrzyga, gdy tekst jest gotowy, jest tania.` jest odrzucone,
bo obie pozycje stoją na `ClauseConjunct`,
a `RelativeCore` jest osobnym symbolem i ciała z tym symbolem w środku ma jedno.
Zdanie odrzucone jest przy tym werdyktem uczciwym, a nie czytaniem nieprawdziwym,
więc pozycja ta nie ma pilności, jaką miałby brak wydający `valid`.

Wysunięcie zdania podrzędnego jest faktem o spójniku i stoi w dwóch plikach:
`SPÓJNIKI_WYSUWANE` w `olski/subset.py` mówi to o kilkunastu lematach analizy,
a `SPÓJNIKI` w `olski/skład/spójniki.py` o kilku, których używa skład,
i obie listy zgadzają się dziś tam, gdzie się przecinają.
Rama czasownika poszła tą samą drogą i zeszła do jednego pliku,
bo jest faktem o słowie, a nie o kierunku, w którym się go używa
([`docs/roadmap.md`](docs/roadmap.md#etap-2-walencja-czytana-raz)),
a spójnik jest takim samym faktem.
Ruchem jest leksykon spójników czytany przez oba kierunki,
wzorowany na `olski/walencja.py`, i przed nim jedno rozstrzygnięcie:
skład trzyma relację obok szyku, a analiza relacji nie zna,
więc albo leksykon niesie kolumnę, której analiza nie czyta,
albo relacje dochodzą do niego dopiero z kategoriami składu,
których dziś nie ma na warunek ani na przyzwolenie.
Do przeczytania jest `olski/walencja.py` wraz z tym,
co obu kierunkom z leksykonu walencyjnego wyszło różnego
([`docs/subset.md`](docs/subset.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)).

Okolicznik przysłówkowy bierze całą część mowy, a Morfeusz daje czytanie `adv`
formom, których ten rejestr używa jako przyimka albo spójnika: `wobec`, `gdy`, `sam`.
Wychodzą z tego czytania, których polszczyzna w tych miejscach nie ma —
`postępować wobec innych w duchu braterstwa` dostaje trzy czytania z `wobec`
w roli okolicznika, a `Program zapisuje ustawienia, gdy linter sprawdza tekst.`
wychodzi obok czytania podrzędnego drugim, w którym `gdy` jest okolicznikiem
zdania spiętego przecinkiem.
Cena tej klasy jest przez to zmierzona i wynosi sześć zdań Składnicy:
tyle straciło jednoznaczność pod morfologią żywą, kiedy weszła podrzędność
okolicznikowa, i wszystkie sześć niesie `gdy` albo `kiedy`.
Kryterium słownikowe `admissible` w `olski/segmentacja.py` po nie nie sięga,
bo pyta o czytanie rzeczownikowe stojące obok wyrazu funkcyjnego.
Ruchem jest warunek na tę klasę, a dwa kandydujące są zmierzone i żaden nie jest darmowy.
Odsiew czytania przysłówkowego przy czytaniu przyimkowym kupuje nad Składnicą
pod morfologią żywą jednoznaczność dwunastu zdaniom, a jedenastu odbiera wyprowadzenie
(sześciu przyjętym i pięciu wieloznacznym); odsiew przy czytaniu spójnikowym kupuje
tyle samo i odbiera trzydziestu pięciu, bo zabiera `jak` w pytaniu.
Pod morfologią złotą oba nie ruszają niczego, bo anotator wybrał tam jedno czytanie
na token, więc pomiar tej klasy idzie po morfologii żywej i po prozie.
Do przeczytania jest lista form, które warunek dotknie: `blisko` i `naprzeciw`
niosą czytanie przysłówkowe, którego polszczyzna używa,
więc cena stoi w zdaniach, a nie w samych czytaniach.
Kandydat trzeci wyszedł z czytania zdań przyjętych i nie ma pomiaru:
czytanie przysłówkowe stojące przy czytaniu rzeczownikowym tej samej formy.
Zabiera ono `Wszystko wyżej pyta o zdanie, po którym zostaje czytań kilka.`
oraz `Czego na tej liście nie ma.`, czyli zdania przyjęte na czytaniu,
którego polszczyzna nie ma
([`docs/subset.md`](docs/subset.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)),
a dwa kandydujące wyżej po nie nie sięgają,
bo przy przysłówku stoi w nich rzeczownik, a nie przyimek ani spójnik.

Dopełnienie bezokolicznika wysunięte przed formę osobową ma szyk jeden,
a polszczyzna ma ich kilka: `Większości premier nie może ruszyć.`
oraz `Większości nie może ruszyć.` są odrzucone, gdzie
`Premier większości nie może ruszyć.` wyprowadza się
([`docs/subset.md`](docs/subset.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze)).
Wzór stoi obok: deklaracja z dopełnieniem przy formie osobowej wypisuje pięć szyków
warunkiem precedencji (`_poza_orzeczeniem` w `olski/subset.py`),
a podmiot opuszczony ma tam ciało osobne.
Ruchem jest ten warunek nad deklaracją z frazą bezokolicznikową
wraz z ciałem bez podmiotu, a przed nim pomiar:
szyk z dopełnieniem na czele konkuruje naraz z okolicznikiem wysuniętym przed zdanie
i z przydawką dopełniaczową, czyli z dwiema pozycjami,
z których żadna nie konkuruje z szykiem, który wszedł.
Cenę szyku, który wszedł, trzyma tamta sekcja i mówi ona,
od czego zaczyna każdy następny: zakupu nie ma tam żadnego,
więc szyk dopisany zaczyna od ceny, a zakup ma do policzenia.

Czoło zdania względnego sięga do formy osobowej i nie sięga do bezokolicznika pod nią,
choć dopełnienie wysunięte przed formę osobową sięga tam ciałem wypisanym
([`docs/subset.md`](docs/subset.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze)).
`Ustawa, którą organ gminy może wydać, jest tania.` jest przez to odrzucone,
a jest to jedyne zdanie, które kupuje cecha przeciągana
([`docs/design-notes.md`](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)),
więc pozycja dopisana wypisanymi ciałami zabiera luce cały jej zakup
i zamyka rozwidlenie, które tamta sekcja trzyma otwarte —
i to, a nie samo zdanie, jest tu stawką.
Ruchem jest `_wysunięta_rola` w `olski/subset.py` pisząca ten szyk także z frazą
bezokolicznikową, czyli te same córki, które wypisała deklaracja obok,
z czołem w miejscu dopełnienia.
Do rozstrzygnięcia jest, czy warto:
zdania tego kształtu nie ma ani jeden korpus, który to repozytorium czyta,
i mówi to sekcja o zdaniu względnym wraz z poleceniem,
którym sprawdzono rejestr ustaw
([`docs/subset.md`](docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
a `RelativeCore` ma kilkadziesiąt ciał i pozycja mnoży je przez klasy walencyjne.
Do przeczytania jest przy tym `harness/luka.py`:
tamten wariant zdejmuje ciała `RelativeCore` i zastępuje je luką,
więc pozycja dopisana do nich rusza każdą liczbę tamtej sekcji.

Myślnik stoi u olskiego między dwoma zdaniami i nie stoi wewnątrz zdania,
a polszczyzna stawia go wewnątrz w miejscu pominiętego orzeczenia:
`Ania lubi cydr, Janek — piwo.` jest odrzucone.
Człon bez czasownika olski ma i licencjonuje go spójnikiem
([`docs/subset.md`](docs/subset.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)),
więc `Ania lubi cydr, a nie piwo.` wyprowadza się i werdykt nazywa czasownik,
do którego ten człon dochodzi.
Różni je dwie rzeczy. Licencją jest tu sam znak, a nie spójnik, czyli ciało osobne.
Oraz `Janek — piwo` niesie dwie pozycje, a nie jedną,
więc człon musiałby zgodzić się z członem obok co do ról, których nie wypowiada,
a dzisiejsze ciało bierze jeden konstytuent i o rolach nie mówi nic.
Do rozstrzygnięcia jest przedtem granica zdania:
`Ania lubi cydr. Janek — piwo.` ma orzeczenie w zdaniu poprzednim,
a olski orzeka o zdaniu, nie o akapicie
([`docs/roadmap.md`](docs/roadmap.md#co-jest-budowane)),
więc albo konstrukcja wchodzi tylko wewnątrz jednego zdania,
albo werdykt przestaje być wypowiedzią o zdaniu.
To rozstrzygnięcie idzie pierwsze, bo od niego zależy,
czy pozostałe dwie rzeczy mają gdzie stanąć.
Wpis waży przy tym więcej, niż mówi liczba zdań, i mówi to drugie użycie tego znaku:
`Premier — większości nie może ruszyć.` nie miałoby czytania z grupą
`premier większości`, bo grupa imienna myślnika nie przechodzi,
czyli autor dostaje znak, którym rozstrzyga sam
([`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md)),
a takich pozycji ten podzbiór ma niewiele.
Ceną jest to, że znak ten spina dziś dwa zdania,
a para myślników ma wpis osobny, ten o wtrąceniu w środku zdania,
więc ciało wewnątrz zdania konkuruje z obydwoma i sesja bierze je razem.

Zamknięta lista kopul nie ma `stawać się` ani `okazywać się`,
a polszczyzna orzeka nimi narzędnik tak samo jak `zostawać`.
`Mao stał się na wiele lat przywódcą największego narodu na kuli ziemskiej.`
i `Człowiek staje się wyleniałym tygrysem.` są przez to odrzucone,
i są to dwa z 75 zdań, które zawężenie narzędnika odrzuca nad Składnicą,
a jedyne dwa, które odrzuca niesłusznie
([`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Przeszkodą nie jest lista, tylko cząstka: `KOPULA` w `olski/lematy.py` jest
warunkiem na lemat, a te dwa czasowniki są kopulami wyłącznie z `się`,
którego produkcja kopuli nie ma gdzie postawić —
[`docs/subset.md`](docs/subset.md#what-the-grammar-covers) mówi to przy liście.
Ruchem jest ramka narzędnikowa w leksykonie zwrotnym,
czyli ta sama droga, którą walencja rozdziela formę z cząstką od formy bez niej,
a do przeczytania jest, co zwrotna kopula robi z `Ludzie rodzą się wolni.`,
gdzie orzecznik zgodny stoi dziś przy czasowniku zwrotnym niebędącym kopulą.

Klasa kopuli zabiera lematowi wpis z leksykonu (`_walencja` w `olski/subset.py`),
więc kopula nie bywa naraz czasownikiem, który bierze zdanie z `że`.
Widać to na `bywać`, odkąd lemat ten stoi w `KOPULA` w `olski/lematy.py`:
`Odpowiedzią bywa decyzja.` przechodzi z odrzuconego na przyjęte,
a `bywa tak, że` zostaje bez ani jednego czytania —
jedno zdanie Składnicy i jedno zdanie `docs/subset.md`.
Ceną tą zapłacono za rolę: bez tego wpisu `Skreślenie bywa całą naprawą.`
też ma jedno czytanie, tyle że z narzędnikiem w okoliczniku, a nie w orzeczniku
([`docs/subset.md`](docs/subset.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Ruchem jest rama kopuli liczona jako suma z ramą tego lematu,
a nie jedna wartość na całą listę,
i wtedy ta sama zmiana rusza `być`, któremu Walenty daje dopełniacz,
bezokolicznik oraz zdanie podrzędne; tamtego rozszerzenia nie zmierzył nikt.
Do przeczytania przed pomiarem jest, że sondzie różnicowej tego nie zmierzyć
podmianą samej stałej: klasy walencyjne liczą się przy imporcie modułu,
a nie w `build`, więc wariant złożony po podmianie `KOPULA` jest tą samą gramatyką.

Gospodarz o dwóch kształtach ma dwie głowy, a werdykt nazywa jedną i nie mówi którą.
`Organ gminy może wyznaczyć swojego przedstawiciela do udziału w zgromadzeniu.`
daje wiersz `„do udziału” → „może”, „przedstawiciela”`,
a grupa imienna nazwana tam `przedstawiciela` jest w innym czytaniu grupą,
w której głową jest `swojego`:
przymiotnik ma czytanie rzeczownikowe, a rzeczownik dopełniaczowe,
czyli tę samą parę, o którą pyta wpis o rzeczownikowym czytaniu przymiotnika.
Wybór między tymi dwiema nazwami robi porządek, w jakim las wydaje drzewa,
bo `_przedstawiciel` w `olski/parse.py` bierze pierwsze z nich,
a porządek ten idzie po rozpiętościach córek (`ciała` w tym samym pliku)
i o tym, która głowa nazywa grupę imienną, nie mówi nic.
Formom to nie grozi, bo konstytuent ma je w każdym czytaniu te same.
Ruchem jest albo obie głowy w tym wierszu, albo pierwsza z zadeklarowanym kryterium.
Przeciw pierwszemu: wiersz przyłączenia mówi o jednym wyborze,
a `swojego` bierze się z czytania słownikowego, nie z przyłączenia,
więc wiersz zaczyna mówić o dwóch wieloznacznościach naraz;
przeciw drugiemu: kryterium na kształt grupy imiennej to gramatyka pisana drugi raz.
Do przeczytania jest, jak często rejestr ustaw taki wiersz wydaje,
bo od tego zależy, czy ten wpis jest wart ceny któregokolwiek z dwóch ruchów.

Przedstawiciel pozycji może stać w klasie, której żadne czytanie nie bierze.
`_przedstawiciel` w `olski/parse.py` bierze pierwsze drzewo pozycji bez odsiewu po
klasach żywych, a `_kształty` obok niego ten odsiew ma, więc nazwa konstytuenta
bierze się czasem z kształtu, którego werdykt nie liczy.
Rozpiętość jest w obu ta sama, więc formy różni w nich tylko podział na segmenty.
Ruchem jest `next(self._kształty(pozycja))` w miejsce tamtej pętli, a przeszkodą
pozycja bez ani jednej klasy żywej: dziś oddaje nazwę, a wtedy podniosłaby wyjątek.
Do przeczytania jest, czy nad Składnicą taka pozycja pada i czy pada z innymi formami,
bo od tego zależy, czy to usterka, czy sam porządek w kodzie.

Grupa imienna rozbieżna zostaje bez listy czytań, bo streszczenie nie ma w niej czego nazwać.
`Verdict.rozbieżne` w `olski/werdykt.py` wypuszcza konstytuent,
którego streszczenia naprawdę się różnią, czyli zdanie podrzędne, a grupy imiennej nie:
`describe` w `olski/parse.py` szuka ról zdania, a grupa imienna żadnej nie nosi,
więc oba jej kształty streszczają się pustym słownikiem.
Różnica siedzi tam w głowie — raz `rada` z przydawką `zainteresowana`,
raz `zainteresowana` z przymiotnikiem `rada` i dopełniaczem `gminy` —
więc ruchem jest drugie streszczenie, to o grupie imiennej:
głowa oraz to, czym są słowa stojące obok niej.
Tej samej nazwy żąda wpis o gospodarzu o dwóch głowach, a wydać ją raz jest taniej.
Do przeczytania jest, ile wierszy `„…” reads N ways` rejestr ustaw wydaje nad grupą
imienną, a ile nad zdaniem podrzędnym, bo pierwsza z tych liczb jest ceną milczenia.

Czas przeszły zostawił za sobą resztkę wiersza `praet`, której nikt nie przeczytał.
`praet` prowadził kolejkę blokerów,
a po dopisaniu tej formy do `Verb` w `olski/subset.py` wiersz zmalał o rząd wielkości
i to, co w nim zostało, staje na czasie przeszłym dalej.
Od tamtej pory wiersz rośnie, bo każde dopisanie przesuwa na czasownik blokery zdań,
których nie przyjęło ([`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)),
więc do przeczytania jest resztka dzisiejsza, a nie ta z chwili dopisania.
Nie wiadomo, czy stoi za tym jedna konstrukcja, czy dwadzieścia:
`Wózek zwolnił biegu i przystanął.` i `Pani Zofia była w rozpaczy.`
są w tej resztce obok siebie, a łączy je tyle, że bloker wskazał czasownik.
Ruchem jest odczytanie tej resztki i rozbicie jej na klasy,
z tego klasy nazwane w [`docs/subset.md`](docs/subset.md#what-it-does-not-cover-yet),
jeśli któraś jest konstrukcją, a nie zbiegiem okoliczności.
Do przeczytania jest sam `bloker` w `olski/pokrycie.py`:
nazywa on formę, na której rozbiór stanął,
a przy zdaniu z czasownikiem w środku bywa to forma stojąca za prawdziwą przyczyną,
więc część tej resztki może być artefaktem tego odczytu, a nie brakiem w gramatyce.

Wiersz zdań bez struktury nad całością ma nad Składnicą przeszło tysiąc zdań
i przeczytana jest z nich garść.
Nazywa on zdarzenie, a nie konstrukcję — analiza wzięła każdą formę zdania
i nie domknęła całości
([`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)) —
więc mówi, gdzie szukać, a nie czego brakuje.
Nagłówek bez czasownika, `Na próżno.` czy `Najpospolitszy.`, jest w nim mniejszością,
a większość tych zdań niesie formę czasownikową,
czyli brakuje w nich czegoś nad czasownikiem, a nie samego czasownika.
Ruchem jest odczytanie tej resztki i rozbicie jej na klasy,
z tego klasy nazwane w [`docs/subset.md`](docs/subset.md#what-it-does-not-cover-yet),
jeśli któraś jest konstrukcją, a nie zbiegiem okoliczności.
Do przeczytania jest ta resztka pod obiema morfologiami:
pod żywą wpada do niej także forma, której wykluczenie zabrało wszystkie czytania,
a tę drugą klasę trzyma wpis o wycięciu czytań bez licencji przed rozbiorem.

Aglutynant dochodzi tylko do czasownika, przy którym stoi.
`_formy_skończone` w `olski/subset.py` bierze `praet` z `aglt` po nim,
bo tak Morfeusz tnie `napisałem`,
a polszczyzna stawia tę końcówkę także przy innym słowie zdania:
`gdzieś ty był`, `myśmy przyszli`, `dlaczegoś to zrobił`.
Tym samym brakiem jest końcówka na spójniku niosącym cząstkę trybu —
`żebym napisał`, które Morfeusz tnie na `żeby` i `m`
([`docs/subset.md`](docs/subset.md#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)).
Ruchem jest aglutynant przyłączany do zdania, a nie do czasownika,
czyli cecha osoby wypuszczana w górę z miejsca, w którym końcówka stanęła.
Do rozstrzygnięcia jest, czy warto:
konstrukcja jest w rejestrze technicznym rzadka albo nieobecna,
a w prozie literackiej Składnicy nie jest.
Po stronie spójnika policzono trzydzieści zdań banku drzew —
`Żebym go chociaż mocno zranił!`,
`Nikt nas nie zmusi, abyśmy w nim partycypowali.` —
a po stronie zdania z `ty` nie policzył ich nikt.
Do przeczytania są te zdania Składnicy, w których `aglt` stoi poza `praet`,
bo od ich liczby zależy, czy ten wpis jest wart ceny ruchu.

Luka jest węzłem o pustej rozpiętości, więc rola wypełniona przez nią nie ma nazwy,
i na tym stanął pomiar cechy przeciąganej
([`docs/design-notes.md`](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
`Outcome.agreement` w `harness/pomiar.py` porównuje rozpiętości,
więc rozpiętość pusta nie trafia w żadną złotą i liczy się jako niezgodna —
tak wyszło zdanie, które luka wyciąga ze Składnicy,
choć role widoczne ma dobre.
Werdykt tej ceny nie płaci: luka stoi wewnątrz zdania względnego,
gdzie streszczenie nie zagląda,
więc o roli wypełnionej luką milczy tak samo jak o roli wypełnionej zaimkiem.
Ruchem jest luka wskazująca zaimek, który ją wiąże, a nie miejsce, w którym stoi:
etykieta roli nad zaimkiem, a nie nad pustym węzłem,
czyli to, co bank drzew robi na tych zdaniach.
Olski poza wariantem stawia tę etykietę produkcją
([`docs/subset.md`](docs/subset.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)),
więc pytanie, czy niesie ją produkcja, czy porównanie ról, ma tu odpowiedź z precedensu,
a wariant z luką tamtych ciał nie ma i musi ją postawić po swojemu:
`RelativeCore` składa tam zaimek ze zdaniem, któremu brakuje dokładnie tego, czym on jest,
więc etykieta ma stanąć nad zaimkiem w tej jednej produkcji.
Do przeczytania jest przy tym `Node.span` w `olski/parse.py`,
bo pole to wpisano pod produkcję o pustym ciele, a ta sonda jest jego pierwszym czytelnikiem.
Nie zamyka tego wpisu cała cena: warunek precedencji na lukę pilnuje pozycji w ciele,
a nie w napisie, więc zdanie zagnieżdżone dalej wychodzi dwoma kształtami.
Rozdzielenie dominacji od precedencji tej reszty nie zamknęło i zamknąć nie mogło:
rozwinięcie mówi o kolejności córek w ciele, czyli o tym samym, o czym mówi luka dziś
([`docs/subset.md`](docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
a warunek pytany o rozpiętości musiałby stanąć w lesie, gdzie `_przejdź`
w `olski/parse.py` dostaje ciało wraz z rozpiętościami córek.
Wpis jest przez to o warunek sprawdzany po rozbiorze, a nie o preprocesor przed nim.
Odbiorca takiego warunku jest przy tym jeden i mówi to pomiar, a nie przeoczenie:
tryb w ciągu współrzędnym i zagnieżdżenie liczebnika prosiły o tę samą maszynerię,
a oba okazały się cechą albo pozycją nie wartą ceny
([`docs/subset.md`](docs/subset.md#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)
oraz [tamże](docs/subset.md#liczebnik-złożony-przyłącza-się-wedle-ostatniego-członu)).
Luka jest tu ostatnia, bo cechą jej zrobić nie da się wcale,
i dlaczego, mówi
[pakowanie czytań](docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania).

Pozycja pytania zależnego stoi w ramie domyślnej i nikt nie zmierzył jej zawężenia.
`RAMA_DOMYŚLNA` w `olski/subset.py` daje `int` każdemu czasownikowi,
tak jak daje mu `comp`, a Walenty wypisuje osobno lematy z jednym i z drugim.
Zawężenie `comp` do leksykonu zmierzono i nie kupiło ani jednego czytania,
a przy `int` wynik nie musi wypaść tak samo:
pytanie zależne konkuruje z koordynacją przecinkiem i ze zdaniem względnym,
gdzie zdanie z `że` nie konkuruje z niczym, bo spójnika `że` nie bierze nic innego.
Wpis waży więcej, odkąd `co` bierze poprzednik zdaniowy: cena tamtej pozycji
stoi prawie cała na zdaniach z pytaniem zależnym, którym ono dokłada
drugie czytanie
([`docs/subset.md`](docs/subset.md#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie)),
więc zawężenie `int` do leksykonu odbiera ją tym z nich,
których czasownik pytania nie żąda.
Ruchem jest osobne zdanie leksykonu o `cp(int)`, wzięte przez `harness/walenty.py`,
i wariant gramatyki bez `int` w ramie domyślnej, zmierzony wobec olskiego.
Czym ten wariant zmierzyć, jest rozstrzygnięte:
zawężenie ramy jest zmianą danych, a nie grupą produkcji,
i takiemu wariantowi `Sonda` podaje gramatykę funkcją (`Sonda.gramatyki`).
Do przeczytania jest przy tym, czy skład ma dla tego zdania czytelnika:
`bierze_zdanie` w `olski/walencja.py` czyta ono, a pytania zależnego
`olski/skład/składnia.py` nie ma czym postawić,
więc zdanie dopisane bez tej kategorii jest danymi, których nie czyta nikt.

Lista zaimków rzeczownych nie ma źródła poza pamięcią tego, kto ją pisał.
O każdym lemacie `ZAIMEK_RZECZOWNY` w `olski/subset.py` sprawdzono w Morfeuszu,
że niesie czytanie `subst`, a czy lista jest pełna, nie sprawdził nikt
i słownikiem się tego nie sprawdzi:
czytanie zaimka niczym się nie różni od czytania rzeczownika
([`docs/subset.md`](docs/subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)).
Ruchem jest wykaz lematów, które nad korpusem stają w tej pozycji —
forma o czytaniu `subst` tuż przed formą w dopełniaczu —
uszeregowany częstością i przeczytany ręką:
zaimka nie odróżni od rzeczownika żaden test, ale odróżni go czytelnik.
Do przeczytania jest przedtem cena wpisu:
lemat dopisany odbiera czytanie i żadnego nie dodaje,
więc kandydat mylny zabiera zdanie, które gramatyka dziś wyprowadza.

`pod względem` żąda licencji od słowa, do którego się przyłącza,
a olski żąda licencji tylko od dopełnienia.
Czytelnik odrzuca `wolni pod względem swej godności` bez pomocy składni,
bo `równy` ma pozycję na wzgląd, a `wolny` jej nie ma.
Tę samą obserwację robi nad `przewyższać`
[`docs/subset.md`](docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera),
gdzie porównanie mówi, w czym jedno przewyższa drugie,
i nie ma jej dziś gdzie zapisać.
Leksykon walencyjny mówi o pozycjach ramy, które czasownik bierze albo których nie bierze
([`docs/subset.md`](docs/subset.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)),
a okolicznik pozycji ramy nie zajmuje i przyłącza się do każdego czasownika za darmo,
więc żaden wpis nie odbiera czytania,
w którym wzgląd dochodzi do `rodzą się`.
Ruchem jest zdanie leksykonu odwrócone wobec tamtych trzech:
nie „ten czasownik czegoś nie bierze”, tylko „to wyrażenie przyimkowe
przyłącza się tam, gdzie licencjonuje je leksykon”,
czyli cecha przy przyimku zleksykalizowanym, a nie przy jego gospodarzu.
Robi ono z pierwszego artykułu Deklaracji zdanie olskie:
odejmuje czytanie z `rodzą się`, bo ten czasownik wzglądu nie licencjonuje,
a zostaje czytanie z `równi`, czyli jedno.
Odejmuje też czytanie nad całym ciągiem współrzędnym,
bo `wolny` wzglądu nie licencjonuje tak samo.
Do rozstrzygnięcia jest, czy to jeszcze walencja, czy już ta warstwa,
którą [`docs/open-questions.md`](docs/open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma)
odkłada poza gramatykę jako odpowiedź trzecią;
różnicę robi to, że leksykon w gramatyce już jest, a tamta warstwa nie.
Do przeczytania jest, ile takich przyimków rejestr ma,
bo `pod względem` jest jednym z nich i nikt nie policzył, ile jest reszty,
oraz co Walenty mówi o wzglądzie:
pozycje zleksykalizowane wypisuje on w schemacie,
a przymiotnika, który licencjonuje tu wzgląd, nie ma w pliku czasownikowym,
z którego leksykon powstaje,
choć archiwum obok tego pliku niesie katalog przymiotnikowy.
Kryterium wejścia ma ten ruch to samo, co każda warstwa więzowa:
[wyprowadza się z gramatyki albo jest gramatyką pisaną drugi raz](docs/design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej),
a leksykalnie znaczy to tyle, że pozycję wypisuje słownik.
Jeśli Walenty jej nie wypisuje, ruchu nie ma i cały wpis zamyka skasowanie,
bo „brzmi nielogicznie” jest sądem o świecie, a nie faktem o słowie:
olski melduje wtedy wieloznaczność, tak samo jak melduje ją wszędzie indziej.

Wysunięte wyrażenie przyimkowe nie potrzebuje licencji od niczego,
więc `Ustawa, o której flaga to płat, obowiązuje.` wychodzi `valid`.
Wpuszcza je ciało `rodzina.rdzeń → rodzina.modyfikator ClauseConjunct`
w `olski/subset.py`, które przed dowolnym zdaniem składowym dopuszcza dowolny przyimek.
Łącznik `to` przyczyną nie jest i nie jest nią kopula pod nim opuszczona:
`Ustawa, w której flaga to płat, obowiązuje.` jest polszczyzną
i wyprowadza się tym samym ciałem,
a `Ustawa, o której flaga jest płatem, obowiązuje.` jest tą samą usterką
z kopulą wypisaną wprost.
Licencji od każdego wysunięcia żądać też nie wolno,
bo `Godzina, o której poseł śpi, mija.` jest polszczyzną,
a rama `spać` wymienia `nad` i `z`.
Fakt rozdzielający te zdania jest w `olski/leksykon.txt` —
rama rzeczownika `mowa` wymienia `o`, a `flaga` ani `płat` nie mają tam wpisu —
i czyta go sam świadek ramowy w `olski/rozstrzyganie.py`,
a czemu nie czyta go gramatyka, wywodzi `olski/walencja.py`.
Dzisiejsza unifikacja tego żądania nie zapisze,
bo licencjonuje tu którekolwiek słowo zdania składowego, a nie jego głowa:
w `o których mowa jest tam` przyimka żąda rama podmiotu, kiedy głową jest `jest`.
Cechy wychodzą z samej głowy (`_wypuszczane` w `olski/grammar.py`),
a unifikacja zbiory przecina,
więc suma przyimków licencjonowanych przez wszystkie córki nie ma czym pójść w górę.
Świadek nie ma tu z kolei czego zawężać, bo gospodarz jest jeden:
wysunięte wyrażenie stoi przed całym zdaniem składowym,
a zejście w górę zatrzymuje się na rdzeniu rodziny (`gospodarze` w `DEKLARACJA`),
więc kilku gospodarzy daje dopiero luka.
Pomiar luki tych ciał nie obejmuje:
`_wysunięty_okolicznik` w `harness/luka.py` zostawia je nieruszone,
więc liczby z
[`docs/design-notes.md`](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)
mówią o wysuniętym podmiocie i dopełnieniu, a nie o tym wyrażeniu.
Powód tamtego odrzucenia też tu nie sięga: luka dokładała tam czytania,
których czytelnik nie ma, a czytania po gospodarzach są tymi samymi,
które olski daje wyrażeniu stojącemu na swoim miejscu
([`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).
Sama pozycja zarabia na siebie i mówi to sonda różnicowa
zdejmująca ciała z `rodzina.modyfikator` w ciele, osobno dla każdego z dwóch wnętrz:
nad Składnicą pod złotą morfologią wnętrze zdaniowe wyciąga z odrzucenia
kilkadziesiąt zdań, w tym kilkanaście przyjętych jednoznacznie i zgodnych
z drzewem wzorcowym, nad korpusem ustaw kilkadziesiąt i żadnego jednoznacznie,
a jednoznaczności nie odbiera ani jednemu zdaniu w żadnym z dwóch korpusów.
Wnętrze z rzeczownikiem orzekającym nie rusza nad Składnicą ani jednego zdania
i jedno nad ustawami, czyli odpowiada rejestrowi, dla którego je wpisano.
Cena luki ma przez to górną granicę i są nią zdania,
które na tej pozycji stoją jednoznacznie, bo tylko one mają co stracić,
a sonda wypisuje je z nazwiska.

Przyimka wysuniętego wyrażenia nie widać w werdykcie, a innego przyimka widać:
`O czym poseł mówi?` streszcza się jako `Interrogative: czym`,
a `Poseł mówi o ustawie.` jako `Modifier: o ustawie → mówi`.
Rola dla tego wyrażenia nic nie kosztuje i jest to zmierzone:
`rodzina.modyfikator` dopisany do `role` i do `przyłączane`
w `DEKLARACJA` (`olski/subset.py`)
nie rusza werdyktu o ani jedno zdanie Składnicy ani korpusu ustaw.
Sama rola kosztuje najwyżej tyle samo, bo streszczenie rozszczepia wtedy
o jedno pole mniej, więc pomiaru drugi raz nie żąda.
Strzałki temu wyrażeniu dać jednak nie wolno i mówi to kryterium listy obok:
`przyłączane` bierze rolę, którą gramatyka wpuszcza w kilka miejsc,
a to wyrażenie ma miejsce jedno, więc strzałka powtarzałaby czasownik zawsze —
i za to samo stoi poza tamtą listą dopowiedzenie.
Do rozstrzygnięcia przed samą rolą jest etykieta.
Nazwą roli jest nazwa symbolu rodziny, więc jedna rzecz nosi trzy nazwy tam,
gdzie wyrażenie stojące na swoim miejscu nosi `Modifier`,
a zlanie trzech w jedną odbiera jedyną rzecz, jaką te trzy mówią:
w której rodzinie stoi czoło.
Do rozstrzygnięcia jest, czy ta rzecz ma czytelnika.

Cztery przebiegi budują nad Składnicą te same lasy, bo jeden z nich pyta las o mniej.
`zmierz_zdanie` w `harness/pomiar.py` woła `podsumuj` bez deklaracji,
więc `Outcome` nie niesie ani ról różniących, ani przyłączeń, ani rozbieżności,
a `harness/czytania.py` rozbiera przez to cały bank drzew drugi raz po to samo.
Trzeci jest `harness/wskazania.py`, który tych samych przyłączeń potrzebuje,
żeby zapytać o nie warstwę, i różni się od dwóch pozostałych tym, że czyta las
razem z cudzym drzewem — więc scalenie obejmuje go dopiero wtedy, gdy przebieg
zbiorczy umie oddać jedno i drugie.
Czwarty jest `harness/znaczenia.py` i on jeden potrzebuje samych czytań, a nie
podsumowania z nich, bo każde puszcza przez `abstrahuj`; przebieg zbiorczy albo
odda drzewa czytań przez granicę procesu, albo zrobi tę abstrakcję u siebie,
i to jest pytanie do rozstrzygnięcia przed scaleniem, a nie po nim.
Ten sam czwarty przepisuje z `harness/czytania.py` całe rusztowanie przebiegu
spisowego — `Raport`, `zanotuj`, `scal`, pulę procesów i tabelę procentową —
czyli to, czym `harness/ruch.py` jest dla sond różnicowych, a czego spisowe nie mają:
wspólny jest im wiersz poleceń z `harness/komenda.py`, a nie przebieg.
Scalenie przebiegów zdejmuje połowę tego duplikatu i dlatego idzie przed nim.
Rusztowanie to przepisuje także `harness/płaski.py`, a lasów olskiego nie buduje
wcale, bo mierzy wariant gramatyki, więc scalenie przebiegów go nie obejmie
i zostanie po nim sam duplikat rusztowania — to on mówi, ile ono jest warte
osobno.
Ruchem jest deklaracja podana tam, gdzie las i tak stoi zbudowany,
po którym tabela z
[`docs/disambiguation.md`](docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)
wychodzi z `harness.pomiar`, a sonda się kasuje.
Ceną jest to, czego dziś ten przebieg nie liczy:
`różniące`, `przyłączenia` i `rozbieżności` chodzą po lesie osobno,
a `harness.pomiar` puszcza się nad 13 035 zdaniami i pod pulą procesów.
Drugą pozycją ceny jest zatrzymanie:
sondy z tej czwórki o nie nie pytają, bo żadna go nie czyta, a `harness.pomiar` pyta,
bo z niego liczy tabelę blokerów,
i nad zdaniem odrzuconym kosztuje ono mniej więcej drugi rozbiór
(`podsumuj` w `olski/parse.py`).
Do przeczytania jest więc najpierw, ile ta trójka dokłada do przebiegu,
bo poniżej progu, przy którym to widać, ruch jest samym zdjęciem duplikatu,
a powyżej jest wyborem między dwoma przebiegami a jednym droższym.
Do przeczytania jest przy tym `Raport.record` w `olski/pokrycie.py`,
gdzie licznik klas musiałby stanąć, oraz `KAWAŁEK` w `harness/pomiar.py`,
bo przez granicę procesu idzie licznik, a nie las.

Ciąg współrzędny wewnątrz wypełnienia roli nie ma po werdykcie żadnego wiersza.
Nawias pokazuje granicę członu tylko nad ciągiem, którym jest sama rola
(`_nawiasuj` w `olski/parse.py`),
a wiersz o konstytuencie ustępuje mu miejsca nad każdym ciągiem
(`_nazwany_gdzie_indziej` tamże),
więc `Ustawa określa zadania ochrony ludności i obrony cywilnej.`
zostaje samą liczbą czytań i tak zostaje garść werdyktów rejestru ustaw
oraz pojedyncze zdania wieloznaczne Składnicy
([`docs/disambiguation.md`](docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)).
Ruchem jest zawężenie wykluczenia do ciągu, nad którym nawias naprawdę pada,
i przeszkodą jest to, że te dwa podsumowania pytają o różne rzeczy:
`_nazwany_gdzie_indziej` o pozycję w lesie, a `_nawiasuj` o węzeł jednego czytania.
Nawias potrafi przez to paść w jednym czytaniu zdania i nie paść w drugim —
`Podręczniki powinny uwzględniać zasadę równych praw kobiet i mężczyzn.`
ma pod Morfeuszem czytanie z `[zasadę równych praw kobiet] i mężczyzn`
obok czytań bez nawiasu — a werdykt streszcza las, a nie czytanie,
więc kryterium przeniesione wprost nie ma gdzie stanąć.
Do przeczytania jest przedtem, ile z tych dziesięciu zdań czyta się naprawdę dwojako,
bo ciąg trzech członów ma w tej gramatyce kilka nawiasowań o jednym znaczeniu
([`docs/subset.md`](docs/subset.md#nothing-above-a-coordination-distributes-into-it)),
a wtedy ruchem jest sygnatura czytania, a nie wiersz werdyktu.
Dwa są przeczytane i wypadły po jednym na stronę:
zdanie z ustaw znaczy pod dwoma nawiasowaniami dwie różne rzeczy,
a `równych praw kobiet i mężczyzn` jedną.
Na tej samej różnicy ten wiersz ustępuje drugi raz, a ustępuje wtedy `różniące`:
`Gdy linter sprawdza tekst, program zapisuje ustawienia.` wydaje cztery czytania,
z których dwa różni szyk wewnątrz okolicznika,
a wiersza o tym konstytuencie nie ma, bo w dwóch pozostałych `Gdy` jest przysłówkiem
i ta sama pozycja stoi w zdaniu głównym, gdzie jej role nazywa tamto podsumowanie.
Wykluczenie zdjęte na próbę oddaje temu zdaniu wiersz o wnętrzu okolicznika,
więc zawężenie ma tu tego samego adresata co przy ciągu.
Nad prozą `docs/` samą liczbą czytań zostaje kilkanaście zdań,
a ile z nich stoi na którym z tych dwóch wykluczeń, jest do przeczytania.

Wiersz werdyktu o nierozstrzygniętym przyłączeniu liczy samo wyrażenie przyimkowe,
więc `Począł myśleć gorączkowo.` tego wiersza nie ma,
choć różnicę ma tę samą co `Począł myśleć nad ranem.`, gdzie on stoi,
i `harness.czytania` liczy takie zdanie w klasie „sama liczba czytań”.
Rolę tę trzyma `rozstrzygany` w `DEKLARACJA` (`olski/subset.py`),
a czyta ją `Las.przyłączenia` wraz z warstwą rozstrzygającą.
Ruchem jest wpuszczenie do tego pola pozostałych ról z `przyłączane`,
a cena jest podwójna: warstwa nad takim przyłączeniem milczy,
bo tabela skłonności i leksykon walencyjny mówią o przyimkach,
a udziały klas w `docs/disambiguation.md` wychodzą z `harness.czytania` nad Składnicą,
więc trzeba je przeliczyć tą samą zmianą.
Do przeczytania jest, ile zdań Składnicy przechodzi przez to
z klasy „sama liczba czytań” do klasy „przyłączenie”,
bo od tej liczby zależy, czy przeliczenie tabel jest warte ruchu.
Wpuszczenie okolicznika zdaniowego nad cały ciąg współrzędny dopisało do tej klasy
garść zdań i każde z nich jest tego samego kształtu:
werdykt wypisuje im dwa różne gospodarze okolicznika,
a do tej klasy wpadają po tym, że żaden wiersz podsumowania tej różnicy nie nazywa.

Porównanie ról liczy za niezgodność i czytanie dobre, i czytanie złe,
kiedy drzewo wzorcowe nie znaczy w tym miejscu żadnego gniazda.
`Outcome.agreement` w `harness/pomiar.py` pyta o rozpiętości roli po obu stronach,
a rolę przypisaną tam, gdzie gold ma zbiór pusty, liczy jako `disagrees`,
więc `Powtarzaj je tak często, jak to jest potrzebne.` — gdzie wybrane drzewo
dopełnienia rozkaźnika nie znaczy wcale — stoi w tym wierszu obok
`Poprzednio pracodawca mógł z tym zwlekać nawet 15 lat.`,
gdzie olski czyta okolicznik czasu jako dopełnienie i myli się naprawdę
([`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Ruchem jest rola bez gniazda w gold policzona osobno,
czyli czwarty werdykt obok `agrees`, `partial` i `disagrees`,
a nie zbiór pusty czytany jak zaprzeczenie.
Do rozstrzygnięcia jest, czego ten czwarty werdykt nie ma przemilczeć:
zdanie z okolicznikiem czasu w roli dopełnienia jest pomyłką,
której wiersz niezgodnych nie powinien tracić,
więc kryterium na samą pustkę gold zabiera razem z artefaktem sprawdzianu
także jedno czytanie nieprawdziwe.
Do przeczytania są te trzy zdania wraz z gniazdami wybranego drzewa:
`nonch` przy `Co` w `Co pan sądzi o pomyśle Pawła Piskorskiego?` mówi,
że fraza stoi poza ramą, i to jest trzeci powód pustki, różny od dwóch tamtych.

Rankingu form bez licencji nad dokumentem nie wypisuje nikt.
`olski-check` mówi o zdaniu, a nie o pliku, więc formy, po które nie sięga
ani jedna produkcja, widać po jednej naraz i tylko w werdykcie, który je wypisał
(`bez_licencji` w `olski/segmentacja.py`).
Kolejka blokerów odpowiada na inne pytanie, bo grupuje po części mowy zatrzymania,
a forma bez licencji zatrzymania nie musi wywołać.
Czytelników takiego rankingu jest już dwóch:
[kolejka nad rejestrem ustaw](docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
jest wzięta potokiem z grepem, który ten dokument drukuje,
bo nie ma komendy, która by ją wypisała.
Do rozstrzygnięcia jest, czy jest to wiersz `olski-check`, czy tryb obok niej,
bo komenda ta orzeka dziś o zdaniu i ranking nad plikiem jest w niej wypowiedzią
o innym przedmiocie.
Do przeczytania jest polecenie z grepem w tamtym dokumencie:
mówi ono, czego ranking ma dostarczyć, a wycina formy z jednego komunikatu werdyktu,
więc rozdzielenie tego komunikatu na dwa rozsypuje je tak samo,
o czym mówi wpis o werdykcie nazywającym trzy różne roboty jednym zdaniem.

Comparing two runs of the whole corpus has no command,
and it is what the grammar track asks of every addition before it lands.
A point on [the coverage curve](docs/design-notes.md#making-the-trade-measurable)
is a net of what an addition buys against what it costs in uniqueness
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
so the shape wanted is two runs and what moved between them,
not one run printed twice and diffed by eye.
`harness/ruch.py` is that shape for a group of productions removed from olski,
and the declaration in `harness/płaski.py` is written against it,
while `harness/nieciągłość.py` computes its own net beside that machinery rather than on it.
What it does not take is a morphology switched off,
which is neither a group nor a production,
so the exclusion-free column and the two morphologies compared stay hand-written.
The move is a third `SOURCES` entry in `harness/pomiar.py` for the exclusion-free
morphology, and a variant in `harness/ruch.py` that is a morphology rather than
a group of productions.
What a variant is has been settled since, and a morphology is not one:
`Sonda` takes the grammar each variant measures, given as a function,
and a morphology changes the segments a variant is run over
rather than the grammar it is run with.
What to read is that field beside `SOURCES` in `harness/pomiar.py`,
because a variant of this second kind has to say where it enters.
The column is not its only caller: every criterion weighed in
[`docs/subset.md`](docs/subset.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi)
is an exclusion measured this way,
and each was measured with a probe written for the one session that priced it.

Grupa imienna mnoży ciała iloczynem, którego rozwinięcie szyku nie dosięga.
Ciała `NPConjunct` w `olski/subset.py` są iloczynem kształtów głowy
przez obecność `Modifier` po niej,
czyli mnoży je obecność oraz kolejność rodzajów przydawki,
a nie permutacja argumentów,
więc warunek precedencji nie ma tu czego powiedzieć
([`docs/subset.md`](docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Kształt głowy dopisany do tego symbolu wchodzi przez to jako dwa ciała,
bo `Modifier` musi wejść razem z nim.
Zdanie względne tego iloczynu nie ruszyło i pokazuje, którędy się go omija:
dochodzi ono do `NP`, czyli o poziom wyżej, więc jest jedną produkcją,
a nie trzecim rodzajem przydawki razy kształty głowy.
Kosztowało to symetrię w koordynacji, czyli wpis o członie lewym,
który zdania względnego nie unosi,
a `Adjuncts` w tym samym pliku się nie mnoży,
bo okoliczniki są jednego rodzaju.
Kierunek pokazywało samo zdanie względne: `Modifier` dochodzący do `NP`
zamiast do członu znosi ten iloczyn.
Zamianę tę zmierzono — cztery ciała z ośmiu zdjęte, `NP → NP Modifier` w ich
miejsce — i ona nie stoi.
Nad bankiem drzew traci jednoznaczność blisko sto zdań przyjętych,
a odzyskują ją dwa; nad prozą tego repozytorium traci ją kilka, a odzyskuje jedno.
Przyczyną nie jest piętrzenie, którego ten wpis się spodziewał
(`plik w drzewie na dysku` z obydwoma przy `plik`), tylko zasięg:
produkcja rekurencyjna przyłącza wyrażenie do każdego kształtu głowy naraz,
a cztery zdjęte ciała stoją przy głowie rzeczownikowej i odsłownikowej,
i tylko przy nich.
Czterdzieści przeczytanych zdań traci jednoznaczność na tym samym —
`Nadziałem je na haczyk i zarzuciłem.`, `Kierują go na kursy dywersji.` —
czyli na wyrażeniu przyłączonym do zaimka,
którego polszczyzna tam nie przyłącza;
jedno traci ją na grupie liczebnikowej.
Iloczyn zostaje przez to, czym był, a droga do jego zniesienia biegnie
przez cechę, która odróżnia głowę biorącą przyłączenie od zaimka,
i wtedy `NP → NP Modifier` żąda tej cechy zamiast brać wszystko.
Do przeczytania przed taką cechą jest jej cena w czasie rozbioru:
klasa cech rozdziela pozycje lasu (`klasy` w `olski/parse.py`),
a wpis o produkcjach formy `bedzie` mierzy, ile kosztuje jedna klasa więcej.
Do przeczytania jest też `_role` w `olski/skład/rozbiór.py`,
bo czyta ono kształty gramatyki po etykiecie,
więc każdy nowy poziom kosztuje tam gałąź.

`harness/polszczyzna.py` jest drugą deklaracją podzbioru,
który deklaruje `olski/subset.py`,
czyli tym drugim właścicielem faktu, przed którym broni
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely),
i pilnuje jej tylko siedem zdań z `tests/test_sonda.py`.
Te dwie deklaracje rozeszły się na koordynacji przecinkiem
— olski bierze przecinek na czterech poziomach, a sonda spójnik —
i drugi raz na podrzędności, której sonda nie ma wcale,
a nad prozą README nie widać po żadnej liczbie ani jednego z tych rozejść.
Trzecie rozejście widać i jest to grupa liczebnikowa:
`Działają dwie rzeczy` olski wyprowadza jednym czytaniem, a sonda odrzuca,
więc liczba zdań zgodnych spadła i mówi teraz o tym, czego sonda nie ma,
a nie o tym, czym się te dwa opisy różnią
([`docs/design-notes.md`](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)).
Jest to pierwsze rozejście, które ta liczba pokazuje,
i przez to pierwszy dowód, że kopia starzeje się przy każdej produkcji.
Czwarte przyszło z interpunkcją zdaniową i pokazuje się tą samą liczbą:
dwa zdania README olski wyprowadza od tej pory, a sonda odrzuca oba,
bo dwukropka ani przecinka przed spójnikiem nie ma po tamtej stronie.
Piąte przyszło z okolicznikiem narzędnikowym i zabrało tej kopii zdanie,
którym mierzyła współrzędność: `Zobacz docs/design-notes.md oraz docs/roadmap.md.`
wychodzi u olskiego wieloznaczne, bo notacja czyta się nieodmiennie
i staje przez to także w tym okoliczniku, a sonda tej pozycji nie ma
([`docs/subset.md`](docs/subset.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Póki liczby z niej cokolwiek trzymają, kopia zarabia na siebie.
Wpis czekał na to, aż szyk zejdzie do warunków precedencji,
i tamten ruch jest zrobiony
([`docs/subset.md`](docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
więc kopia trzyma odtąd samą liczbę zdań zgodnych,
czyli to, co po każdej produkcji mówi coraz mniej o różnicy dwóch formalizmów,
a coraz więcej o tym, czego sonda nie ma.
Ruchem jest wtedy `git rm harness/podłoża.py harness/polszczyzna.py harness/wiezy.py`
wraz z `tests/test_sonda.py`,
wraz z liczbami [tamtej sekcji](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą).
Zostaje z niej to, co pomiaru nie potrzebuje:
że nieciągłość jest warunkiem zdejmowanym, a nie szczeblem,
i że jednoznaczność bywa osiągana bez trafności.
Kasowanie zabiera przy tym jedyny mechanizm w repozytorium,
który wypuszcza konstytuent nieciągły:
`spójne` w `harness/wiezy.py` jest warunkiem zdejmowanym,
a produkcja z `olski/subset.py` spójności zdjąć nie umie.
Tym warunkiem zmierzono cenę nieciągłości i zamknięto
[rozwidlenie o przestawianiu](docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
a liczy ją `harness/nieciągłość.py`, czyli trzeci plik tego katalogu,
który `harness/wiezy.py` i `harness/polszczyzna.py` czyta.
Lista plików wyżej nie obejmuje więc tego, co kasowanie naprawdę zabiera,
a [sekcja o pomiarze](CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje) każe tę cenę przeliczać razem z gramatyką.
Ruch dopisuje sobie przez to jedno rozstrzygnięcie:
albo cena nieciągłości przestaje być figurą przeliczaną
i tamta sekcja mówi o niej to, co `docs/firing-rates.md` mówi o sobie,
czyli że jest ceną, przy której decyzja zapadła,
albo podłoże zostaje po to jedno, a kasowanie obejmuje samo porównanie deklaracji.
Rozstrzygnięcie to ma termin, bo liczby tamtej sekcji rozeszły się już z sondą:
werdykty nad zdaniami ze szczeliną, mianownik ceny i liczba zdań tracących
jednoznaczność są w niej inne niż w dzisiejszym przebiegu,
więc kto wpis podnosi, albo je przelicza, albo zdejmuje.

Rama mówi, co czasownik bierze, i nie mówi, ile tego bierze.
Dopełnień stoi przy czasowniku najwyżej jedno,
bo tyle stoi w ciele każdej produkcji `Complements` w `olski/subset.py`,
a nie dlatego, że rama tak mówi;
ruchem jest rama zużywana, czyli ta,
[którą pokazuje Świgra](docs/swigra.md#valency-as-a-resource-that-gets-consumed):
pozycja zajęta znika z tego, co niesie reszta grupy.
Wolno ją wyrazić cechą o dziedzinie skończonej,
bo pozycji jest w ramie skończenie wiele,
więc rozwinięcie idzie przed parsowaniem i nie rusza klasy złożoności.
Kupuje to jednak tyle, ile jest ram o dwóch pozycjach naraz,
a rama domyślna takiej nie ma:
biernik z bezokolicznikiem naraz zmierzono i nad Składnicą pod złotą morfologią
przyjmuje 289 zdań zamiast 293, a wieloznacznych ma 116 zamiast 110,
bo grupa imienna za bezokolicznikiem dochodzi wtedy i do niego, i do formy osobowej.
Pozycja, która z inną naprawdę stoi, jest już wpuszczona i jest nią celownik obok
wypełnienia ([`docs/subset.md`](docs/subset.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)),
tyle że licencji nie niesie tam rama, tylko cecha obok niej,
bo ramy unifikacja nie zużywa, a przecina.
Ruch jest przez to odwróceniem tamtej decyzji, a nie dopisaniem do niej:
rama zużywana zdejmuje tę cechę i wypowiada parę samą ramą.
Do przeczytania jest, co robi z klasami walencyjnymi:
dziś dzieli je para na dwie, a rama zużywana dzieliłaby je tym,
ile pozycji lemat bierze naraz.

Cenę pozycji, która nie rusza werdyktu, bierze ręka, bo sonda różnicowa liczy werdykty.
Etykieta roli nad wysuniętym czołem nie rusza ani jednego
([`docs/subset.md`](docs/subset.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)),
a `Raport.zapisz` w `harness/ruch.py` notuje zgodność ról pod zdaniem nowo przyjętym,
czyli dokładnie tam, gdzie werdykt się ruszył,
i `Outcome.ocalenie` nie bierze wcale.
Zakup wzięto więc dwoma przebiegami `harness.pomiar` i odjęciem wierszy ręką,
a tamta sekcja nazywa liczby oraz produkcje, które wariant zdejmuje,
żeby dało się je wziąć drugi raz.
Ruchem są dwie rzeczy naraz i żadna sama nie wystarcza.
Pierwszą jest mianownik brany ze zgodności, a nie z werdyktu:
`zapisz` ma notować zgodność i ocalenie każdego zdania, które oba warianty przyjmują,
a nie tylko tego, którego werdykt się ruszył.
Drugą jest sama gramatyka wariantu, której zdejmowaniem grupy nie da się złożyć:
etykieta jest konstytuentem nad czołem, a ciała zdania biorą ją nazwą symbolu,
więc zdjęta zostawia rodzinę względną bez córki, a nie bez etykiety.
Podać ją jest już czym (`Sonda.gramatyki`), więc zostaje napisanie tej gramatyki.

Sonda luki zastępuje ciała jednej rodziny czoła z trzech.
`ZASTĘPOWANE` w `harness/luka.py` wymienia `RelativeCore` i nic poza nim,
a `_wysunięta_rola` w `olski/subset.py` pisze tym samym kształtem
także czoło pytania oraz czoło rzeczowne, więc wariant z luką zdejmuje ciała
względne z `który`, a pytających ani rzeczownych nie zdejmuje,
choć cecha przeciągana zastąpiłaby wszystkie trzy.
Rodzina rzeczowna stoi w `DOMYKA`, żeby luka nie wychodziła nad nią w górę,
i tym różnią się te dwie stałe:
pierwsza mówi, gdzie luka się wiąże, a druga, co sonda mierzy.
Rodzina względna ma przy tym dwa czoła — sam zaimek i grupę, w której on stoi —
a wariant z luką wiąże ją tylko zaimkiem, więc grupa wysunięta z niego wypada.
Pomiar przez to zaniża i zakup, i cenę: zdanie `Które zadania wykonuje?`
jest tam odrzucone tak samo jak bez luki
([`docs/design-notes.md`](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
Ruchem jest `InterrogativeCore` oraz `NominalRelativeCore` obok `RelativeCore`
w `ZASTĘPOWANE`, a razem z nimi `InterrogativeModifier` i `NominalRelativeModifier`
obok `RelativeModifier` w `_wysunięty_okolicznik` w tym samym pliku,
bo pytanie ma dziś czoło przyimkowe tak samo jak zdanie względne
i luki pod nim nie żąda z tego samego powodu.
Wypisywać tych sześciu nazw nie trzeba: `RODZINY` w `olski/subset.py`
zbiera je rodzina po rodzinie, więc oba te miejsca biorą je stamtąd.
Przed jednym i drugim stoi rozstrzygnięcie, czym pytanie lukę wiąże:
zdanie względne wiąże ją zaimkiem, którego liczbę i rodzaj podejmuje poprzednik,
a pytanie poprzednika nie ma, więc te dwie cechy nie mają się z czym zejść.
Wpis jest winien przebiegi, których żąda ta sekcja tamtego dokumentu,
bo rusza w niej każdą liczbę.

Cząstka zwrotna nie ma pozycji wewnątrz czasu przyszłego złożonego.
`Fabryki nowej spółki będą się znajdować we Włoszech.` jest odrzucone,
bo cząstka stoi tam między `będą` i bezokolicznikiem,
czyli między dwiema częściami jednego orzeczenia,
a `SZYKI_CZĄSTKI` w `olski/subset.py` stawia ją po obu stronach całego ciała
(`_formy_skończone` tamże składa czas przyszły jednym ciałem `Verb`).
Jest to ostatnie miejsce, w którym cząstka stoi tuż przy swoim czasowniku,
a żadne ciało jej nie bierze
([docs/subset.md](docs/subset.md#cząstka-zwrotna-należy-do-swojego-czasownika)).
Ruchem jest trzecia pozycja w tym jednym ciele, między `bedzie` a głową,
a przed nim rozstrzygnięcie, czy rama ma wtedy być zwrotna:
głowa jest bezokolicznikiem, więc pytanie brzmi tak samo jak przy
`InfinitivePhrase`, tylko cząstka nie stoi po żadnej stronie tej głowy.
Do przeczytania jest odmowa kopuli przy klasie domyślnej leksykonu zwrotnego:
kosztowała ona kiedyś właśnie te zdania, a odkąd cząstkę bierze bezokolicznik,
nie kosztuje nad bankiem drzew nic, więc pozycja dopisana tutaj
wraca do niej z pytaniem, czy dalej jest po co.

Lista w [`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md#czego-brakuje-najbardziej)
jest ułożona częstością zawrócenia, a jednej pozycji ta częstość spadła
i nikt listy nie przeliczył.
Wpis o cząstce `się` obejmował dwie rzeczy — cząstkę przy bezokoliczniku
i cząstkę oddaloną — a pierwsza weszła do gramatyki,
więc został sam ogon: nad prozą tego repozytorium zawraca on jedno zdanie,
a wpis stoi w liście tam, gdzie stał z obiema.
Ruchem jest przeczytanie listy od góry z tym jednym pytaniem
i przestawienie tego wpisu; sąsiadów nikt przy tej okazji nie mierzył,
więc kto go podnosi, rozstrzyga zarazem, czym ta częstość jest mierzona,
bo dokument pisze ją z fotela autora, a nie z przebiegu.

Olski czyta cząstkę bezosobową jako czasownik zwrotny z podmiotem.
`Myśli się językowo.` wyprowadza się przez klasę domyślną leksykonu zwrotnego,
czyli tak, jakby `myśleć się` było czasownikiem,
a `Wino białe pije się inaczej.` dostaje przez to dwa czytania,
z których to z podmiotem `Wino białe` jest czytaniem, którego polszczyzna nie ma:
zdanie z tą cząstką podmiotu nie ma, a rzeczownik w nim stoi w bierniku.
Ruchu tego olski nie bierze, bo czeka on na wpis niżej o zwrotności,
którą Walenty zapisuje pozycją, a nie lematem.
Ruchem jest trzecia głowa `ImpersonalPredicate` obok predykatywu i formy
nieosobowej: forma osobowa trzeciej osoby liczby pojedynczej, w czasie przeszłym
w rodzaju nijakim, klasa walencyjna z leksykonu niezwrotnego bez orzecznika
zgodnego, cząstka w obu pozycjach.
Klasa domyślna leksykonu zwrotnego jest tą konstrukcją przeczytaną nieprawdziwie,
więc znika razem z odmową cząstki kopuli, która przy niej stoi.
Cenę przeczytano zdanie po zdaniu i zostały po tym czytaniu dwie klasy z trzech.
Klasa cząstki należącej do bezokolicznika — `Musieli się przebić.` — zeszła z tej
ceny razem z pozycją przy bezokoliczniku i jest to kilkanaście zdań banku drzew;
z reszty jedna klasa niesie `spotkać się`, czyli lemat spod wpisu niżej,
a druga zwrotność, której Walenty nie wymienia wcale.
Zakupem jest garść zdań odzyskujących jednoznaczność:
przebieg z klasą domyślną zdjętą wypuszcza dziś pojedyncze zdania z wieloznacznych
do przyjętych, czego przed tamtą pozycją nie robił ani razu.
Zgodność ról przy tym spada, bo bank drzew daje cząstce w takim zdaniu rolę podmiotu
([docs/corpus.md](docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Kto wpis podnosi, mierzy to na nowo po wpisie niżej,
bo `spotkać się` jest po nim lematem leksykonu, a nie klasy domyślnej.

Leksykon gubi zwrotność, którą Walenty zapisuje pozycją, a nie lematem.
Walenty pisze `spotkać się` jako `spotkać` z pozycją `recip` w schemacie,
a `myć się` jako `myć` z pozycją `refl`, i żadnej z nich `harness/walenty.py` nie czyta,
więc `olski/leksykon.txt` mówi o 5 739 lematach zwrotnych,
a 880 lematów tych schematów nie ma w nim wcale.
Gramatyce nie odbiera to dziś nic, bo klasa domyślna leksykonu zwrotnego
wpuszcza cząstkę i bez wpisu, a odbiera świadkowi ramowemu przyimki tych schematów
(`przyimki_czasownika` w `olski/walencja.py`).
Ruchem jest zdanie leksykonu o cząstce, czytane z obu zapisów naraz,
a przed nim rozstrzygnięcie, czy pozycja `refl` odbiera ramie biernik:
`się` stoi w niej w miejscu dopełnienia, więc lemat wzięty z ramą domyślną
brałby biernik drugi raz.
Do przeczytania jest, ile ta kolumna zmienia świadkowi:
schematów z tymi pozycjami jest 2 407, a lematów 1 464.

Klasa walencyjna mnoży produkcje formy `bedzie` przez lematy, których ta forma nie ma.
Czas przyszły idzie w `olski/subset.py` przez tę samą pętlę co reszta form osobowych,
a `bedzie` jest u Morfeusza formą jednego lematu,
więc ciało z samą tą formą powstaje raz na klasę, a wystrzelić może w jednej.
Reszta jest produkcjami, których nie dosięgnie ani jedno zdanie,
i jest ich kilkadziesiąt, czyli kilka procent całej gramatyki.
Ruchem jest to jedno ciało pisane dla tej klasy,
której warunek wpuszcza lemat `być`, i dla żadnej innej,
pytane u samej pętli klas, a nie u listy nazw obok niej
([CLAUDE.md](CLAUDE.md#code)).
Do rozstrzygnięcia jest, czy warto,
a odpowiada na to czas rozbioru mierzony
[na przemian](CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje),
bo zysk jest tu wyłącznie w nim: ani jedno zdanie werdyktu nie zmienia.
Wpis waży więcej, odkąd leksykon zwrotny czyta zdanie o bezokoliczniku:
klas walencyjnych przybyło, a klasy mnożą tę pętlę,
więc produkcji jest o jedną trzecią więcej i przebieg nad bankiem drzew
trwa o kilka procent dłużej, mierzony na przemian.
Ten sam wzrost mnoży zarazem lematy, których `bedzie` nie ma.

Sprawdzian leksykonu jest skryptem pisanym od nowa przy każdej zmianie.
[Liczba, na której leksykon stoi](docs/subset.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)
— 615 z 616 lematów potwierdzonych bankiem drzew — bierze się ręcznie,
bo `_slot_role` w `harness/corpus.py` czyta z pola `tfw` dwie role olskiego,
a rama czasownika stoi w tym polu cała.
Ruchem jest zejście po wybranym drzewie do węzłów `zdanie`,
wzięcie lematu głowy i pozycji fraz wymaganych obok niej,
i porównanie tego z `WALENCJA` w `olski/subset.py`.
Do rozstrzygnięcia jest, co taki przebieg drukuje:
sama niezgodność jest liczbą, a pożytek z niej ma dopiero ten,
kto widzi lemat, zdanie i pozycję, o którą poszło.
Do rozstrzygnięcia jest też, czy to jest flaga `harness.pomiar`,
czy komenda obok niej, bo tamta mierzy gramatykę, a ta leksykon.
Zdejmuje to zarazem pytanie, którego dziś nikt nie zadaje po zmianie w
`harness/walenty.py`: czy nowe czytanie Walentego dalej zgadza się z bankiem.

Warstwa rozstrzygająca nie dostaje pytania o synkretyzm, choć pomiar tę klasę liczy.
`pytania` w `harness/wieloznaczność.py` wypuszcza same `Przyłączenie`,
a klasa synkretyzmu zostawia `gospodarze` puste, bo wyborem nie jest tam przyłączenie,
więc `Koszt szynki i sera przewyższa koszt bułki.` nie stawia warstwie ani jednego pytania,
choć werdykt nad nim mówi `differing in Object, Subject`.
Nad korpusem audytowym pozycję tej klasy niesie 21,1% zdań
([`docs/open-questions.md`](docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)),
a ile z odrzuceń nad Składnicą zostawia ją jako całą decyzję, nie liczy nikt:
tabela klas liczy tam nazwy z werdyktu, a nie decyzje,
i osobnej kolumny na szyk nie ma
([`docs/disambiguation.md`](docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)).
Ruchem jest drugi typ pytania obok `Przyłączenie` — wybór między dwiema grupami o role —
oraz `Świadek`, który go przyjmuje, bo dzisiejszy protokół pyta o gospodarza modyfikatora.
Do rozstrzygnięcia jest, czy `próba/wybory.txt` ten typ unosi:
wpis ma pola `fraza` i `gospodarze`, a tu żadnej frazy nie ma,
więc albo dochodzi drugi plik, albo pola nazywają się szerzej.
Świadka dzisiejszego kształtu nie ma tu przy tym żadnego i nie jest to przeoczenie:
temat rozstrzyga kolejność, a nie rolę
([`docs/disambiguation.md`](docs/disambiguation.md#kontekst-rozstrzyga-wykluczeniem-a-nie-rankingiem)),
skłonność liczy przyimki, a powtórzenie przeniesione z frazy na rolę
wskazuje po `Bułka jest tania.` na `koszt bułki` jako podmiot,
czyli odwrotnie, niż czyta czytelnik.
Wpis jest więc o pytaniu, a nie o odpowiedzi:
warstwa, która pytania nie dostaje, nie umie nawet przemilczeć.

Świadek ramowy pyta o przyimek i nie pyta o przypadek grupy pod nim,
więc jego zasięg jest oszacowaniem górnym po obu stronach sporu.
Walenty pisze `prepnp(o,loc)` obok `prepnp(o,acc)`, a `Attachment`
w `harness/attachment.py` niesie sam przyimek, więc `informacja o błędzie` pasuje
do obu wpisów naraz i tak samo pasuje do nich rama czasownika,
czyli weto pada częściej, niż powinno, i częściej pada też wskazanie.
Ruchem jest przypadek wydawany przez `Attachment` wraz z kolumną leksykonu, która go
niesie, i pytanie o obie wartości naraz — w `przyimki` w `harness/walenty.py`
oraz w `Rama` w `olski/rozstrzyganie.py`, bo kryterium jest jedno.
Do przeczytania jest, ile ten zwrot zdejmuje: pod `--tylko-pewne` żadna liczba
sondy nie ruszyła się o więcej niż pół punktu, więc pewność schematu tej klasy nie
odróżnia, a przypadek jest drugim zwężeniem, jakie ten słownik daje bez czytania
schematów ręką
([`docs/disambiguation.md`](docs/disambiguation.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)).
Wpis jest winien przebiegi `harness/rama.py` oraz `--oceń`, bo rusza obie ich pary liczb.

Świadek ramowy nie widzi gospodarza imiennego, którego forma ma czytanie czasownikowe.
Stronę gospodarza nazywa `strona` w `olski/rozstrzyganie.py`, a nazywa ją po
„którymkolwiek czytaniu”, więc `opieka` trafia na stronę czasownikową przez lemat
`opiekać`, a rama `opieka`, która żąda `nad`, nie ma wtedy czego wskazać.
Odpowiedź `uzyskać` z `nad` przy `opieka` stoi wypisana wśród dwunastu, które
drukuje `harness/rama.py`, i tam trafia, bo tam stronę daje bank drzew, a nie Morfeusz.
Wskazania świadek przez to nie myli, tylko milczy, więc cena stoi w zasięgu.
Ruchem nie jest drugie kryterium obok `strona`:
o `strona` pyta także `harness/wskazania.py`, więc druga reguła rozeszłaby się z nią
cicho, a rozejście widać dopiero w liczbach.
Ruchem jest albo rodzaj konstytuentu wniesiony do `Przyłączenie` w `olski/parse.py` —
gramatyka go zna, bo `gospodarze` w `DEKLARACJA` wylicza symbole, na których
zejście się zatrzymuje, a wpis przyłączenia niesie same głowy —
albo zgoda na to, że warstwa stronę zgaduje z czytań formy, wypisana w `strona`.
Do przeczytania jest, ile ta klasa waży: liczbę daje przebieg, który pyta ramy
o gospodarza po obu stronach naraz, zamiast po tej, którą wybrała `strona`.

Nie wiadomo, ile świadek ramowy odpowiada nad rejestrem docelowym.
Zasięg ogranicza mu słownik, a nie kryterium: plik rzeczownikowy Walentego wylicza
1 996 lematów, więc rzeczownik spoza tej listy jest dla świadka rzeczownikiem bez
ramy, a nie rzeczownikiem, którego rama tej pozycji nie ma.
Liczby są dwie i bank drzew nie mówi ani o jednej:
ile pozycji spornych `harness/wieloznaczność.py` wypuszcza nad korpusem audytowym
z rzeczownikiem wypisanym w Walentym, i na ilu z nich świadek odpowiada.
Ruchem jest wiersz w `harness/wskazania.py` albo osobny przebieg nad `proza/`,
wzorowany na `harness/powtórzenie.py`, który tę populację już liczy
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Do rozstrzygnięcia jest, czy ta liczba jest wierszem tabeli świadków,
czy figurą osobną: tabela liczy odpowiedzi, a to jest pytanie o mianownik pod nimi.

Świadek kontekstowy nie ma zmierzonej trafności, a odpowiedzi do przeczytania ma siedemnaście.
`harness/powtórzenie.py` nad korpusem audytowym dostaje od niego 7 wskazań w granicy
akapitu i 127 bez niej, a przeczytane ręką jest siedem pierwszych i dziesięć
rozrzuconych po pozostałych
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)),
czyli odczyt, a nie stopa pomyłek: nad 1 126 pozycjami siedemnaście sądów nie jest częstością.
Wzorzec, przy którym byłaby, jest dwojaki i oba są cudzą robotą.
`próba/wybory.txt` daje trzydzieści sądów, a wskazania tego świadka są w nich dwa,
i losowanie go nie dosięga z żadnej strony: nad 1 126 pozycjami odzywa się siedem razy,
a próba zawężona do samych odpowiedzi warstwy wzięła trzydzieści ze 123 i nie trafiła w ani jedno
([częstość nad dokumentacją](docs/disambiguation.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)),
więc po tej stronie zostaje przeczytanie wszystkich siedmiu, a nie próba.
Drugim jest [wzorzec po drugiej stronie](docs/disambiguation.md#wzorzec-na-tę-warstwę-jest-po-drugiej-stronie),
bo tekst złożony przez `olski/skład` niesie czytanie, o które w nim chodziło,
i wtedy obrót przez parser mówi, czy warstwa zdejmuje czytanie, którego drzewo nie deklarowało.
Blokuje go ta sama własność drzewa, przez którą `przejrzyj`
zgłasza jedną klasę z dwóch: okolicznik dochodzi w nim do zdarzenia zawsze,
więc wzorzec wychodzi jednostronny i obrót niczego nie rozróżni.
Ta połowa wpisu jest przez to zaparkowana po stronie składu, a odblokuje ją dopiero
wyrażenie przyimkowe, które skład umie postawić wewnątrz grupy imiennej.

`próba/wybory-z-odpowiedzią.txt` mierzy dwóch świadków,
a wylosowano ją nad jednym.
Wpisy były odpowiedziami tabeli skłonności, a po wpuszczeniu świadka ramowego
ponad połowę z nich oddaje rama, bo stoi przed tabelą w kolejności świadków
([`docs/disambiguation.md`](docs/disambiguation.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)).
Pięć pomyłek na 29 odpowiedziach jest przez to stopą warstwy, a nie tabeli,
więc zestawienie jej z trafnością tabeli na połowie banku drzew
mierzy po dwóch stronach co innego, a dokument notuje samo to, że mówi mniej.
Do przeczytania jest wydruk `python3 -m harness.wybory próba/wybory-z-odpowiedzią.txt`
wpis po wpisie, bo powód nazywa świadka, który odpowiedział:
podział na wpisy z powodem w zdaniu i bez niego czytała ręka,
gdy odpowiadała sama tabela, a powodów ramowych jest w nim więcej
niż odpowiedzi, które rama bierze.
Ruchem jest stopa rozbita po świadkach — pole w wydruku `harness/wybory.py`
albo losowanie osobne na świadka — a nie sama poprawka zdania w dokumencie.

`ZASIĘG_FRAZY` szuka rzeczownika frazy trzy słowa za przyimkiem i nie zatrzymuje
się na przecinku, więc dopasowuje się do frazy, której w tym miejscu nie ma.
`Przypisanie atrybutów do kategorii, jest zawarte w dokumencie, zakładka:
Atrybuty kategorii.` uchodzi przez to za zdanie, w którym stała fraza
`w przypadku tych atrybutów`: rzeczownik schodzi się z `Atrybuty`,
choć fraza tego zdania jest `w dokumencie`, a między nimi stoi przecinek i dwukropek.
Wyszło to nad korpusem audytowym przy wycenie reguły kandydata, w wariancie szerszym,
gdzie takie dopasowanie kończyło się wskazaniem na `jest`
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Wskazania tego nie ma żaden wariant, bo dowód z kopuli dowodem nie jest,
a samo dopasowanie stoi: warunek na kopulę zdjął wskazanie, a nie usterkę pod nim,
i nad tym korpusem nie widać jej w żadnym przebiegu.
Ruchem jest granica frazy wzięta z interpunkcji, a nie z liczby słów:
`SŁOWO` w `olski/rozstrzyganie.py` wypuszcza dziś same znaki słowotwórcze,
więc przecinka nie ma jak zobaczyć ani `_gdzie_stała`, która frazy szuka,
ani `_łańcuch`, który tą samą drogą przechodzi przecinek w lewo.
Do przeczytania jest, ile takich dopasowań w tym korpusie w ogóle pada,
bo znane jest jedno i wyszło przez wskazanie, które warunek na kopulę zdjął;
liczbę tę daje ten sam przebieg, kiedy wypisze dopasowania, a nie same wskazania.

`_grupa` w `harness/wieloznaczność.py` przedłuża łańcuch imienny przez orzeczenie,
bo forma osobowa bywa zarazem imienna: `stanowi` jest u Morfeusza celownikiem od `stan`,
więc `dokument stanowi kompendium wiedzy dla deweloperów` proponuje gospodarzy
`wiedzy, kompendium, stanowi, dokument`, a wybór jest tam między `kompendium` i `stanowi`.
Poprawia to ręka przy wpisie próby wyborów i mówi to jej nagłówek (`próba/wybory.txt`),
a wpis o powiększeniu tej próby mnoży ten koszt przez liczbę nowych wpisów.
Gospodarza czasownikowego szuka się przy tym przed przyimkiem, a nie przed grupą,
więc orzeczenie wciągnięte do łańcucha wraca drugi raz jako on
i pozycja stawia wtedy grupę przeciw jej własnemu członowi.
Ruchem jest kryterium przedłużające łańcuch węższe od czytania imiennego,
czyli takie, które formę o czytaniu osobowym zatrzymuje —
`OSOBOWY` w tym samym pliku wylicza te czytania pod pomiar synkretyzmu.
Do przeczytania jest przedtem, ile ten warunek zabiera, bo łańcuch urwany za wcześnie
odbiera gospodarza głowie grupy, czyli to, po co ten łańcuch tam stoi;
mianownikiem jest cała populacja pozycji, którą drukuje `python3 -m harness.powtórzenie`
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Ten sam warunek czyta `_łańcuch` w `olski/rozstrzyganie.py`, bo kryterium jest jedno,
a tam urwanie łańcucha kończy się milczeniem, nie pomyłką, więc cena jest inna po obu stronach.

Lista kopul, którą `olski/rozstrzyganie.py` odejmuje od dowodu,
jest pożyczona i cztery piąte jej nie zmierzono.
Świadek kontekstowy nie bierze za dowód powtórzenia przy kopuli, a listę kopul bierze
z gramatyki, gdzie kryterium jest inne: `KOPULA` w `olski/lematy.py` wylicza czasowniki
biorące orzecznik w narzędniku, a tutaj chodzi o czasownik, przy którym okolicznik stoi
bez związku z rzeczą. Nad korpusem audytowym rozstrzyga to samo `być`, a `zostać`, `zostawać`, `pozostać`
i `pozostawać` ruszają wyłącznie wariant sondy pytający o cały prefiks zdania,
gdzie zdjęcie takiego dowodu odsłania gospodarza zasłoniętego przez kopulę.
Liczbę tę daje `Powtórzenie(kopuly=frozenset({"być"}))` puszczone przez
`przebieg` w `harness/powtórzenie.py` obok listy pełnej: wiersze wypuszczany,
bez granicy akapitu i „sąsiad bezpośredni” wychodzą wtedy identyczne,
a „cały prefiks zdania” schodzi ze 128 na 126.
Do przeczytania jest, czy dowód przy `zostać` w stronie biernej mówi coś o rzeczy:
`obiekt zostanie przyjęty do bazy RIT` niesie treść w imiesłowie, a nie w czasowniku,
więc gospodarzem bywa tam imiesłów i wtedy zdjęcie lematu `zostać` niczego nie kosztuje.
Ruchem po tym czytaniu jest albo lista własna w tym module wraz z jej uzasadnieniem,
albo zdanie w `KOPULA`, że obie strony pytają o czasownik bez własnej treści.
Rozstrzygnąć to znaczy wybrać między jedną listą o dwóch kryteriach a dwiema listami,
które rozjadą się przy pierwszym lemacie dopisanym po jednej stronie.

Trafność warstwy nad werdyktami mierzy się na materiale, który tabela widziała.
`harness/wskazania.py` puszcza świadków z `domyślni`, czyli z
`olski/skłonności.txt`, a ten plik powstaje z całej Składnicy, po której ten
przebieg idzie, więc 96,1% spod
[tabeli nad werdyktami](docs/disambiguation.md#werdykt-pyta-warstwę-o-inny-wybór-niż-bank-drzew)
jest sufitem, a nie pomiarem.
Dotyczy to samej tabeli, a nie każdego świadka:
`Rama` czyta leksykon wyprowadzony z Walentego, więc materiału tego przebiegu nie
widziała, a wiersz o niej jest pomiarem, a nie sufitem.
Ruchem jest podział taki, jaki ma już `oceń` w `harness/skłonności.py`:
tabela z połowy plików o numerze parzystym, przebieg po nieparzystych,
czyli flaga podająca sondzie świadków zbudowanych z tamtej połowy zamiast z pliku.
Do rozstrzygnięcia jest, czy zasięg liczyć wtedy na tej samej połowie:
tabela z połowy korpusu ma mniej par, więc zasięg spadnie razem z trafnością,
a te dwie liczby dziś nie pochodzą z jednego przebiegu i po tym ruchu pochodziłyby.
Do przeczytania jest przy tym `KAWAŁEK` w `harness/pomiar.py`,
bo podział na kawałki idzie po plikach i musi minąć się z podziałem na połowy.

Wzorca nie ma dla 184 z 695 przyłączeń, a dwie kategorie Składnicy to tłumaczą.
`dokąd_doszły` w `harness/wskazaniach` bierze z drzewa te wyrażenia, którym
`_dokąd_doszło` w `harness/attachment.py` daje `noun` albo `clause`, a `Auta są
kradzione dla okupu.` przyłącza frazę do węzła imiesłowowego, którego `CLAUSE`
nie wylicza, więc zdanie wypada z mianownika trafności
([tamże](docs/disambiguation.md#werdykt-pyta-warstwę-o-inny-wybór-niż-bank-drzew)).
Druga jest fraza werbalna z bezokolicznikiem: `Muszę jechać do domu.` przyłącza
frazę dokładnie tam, gdzie stawia ją werdykt, i mimo to wzorca stąd nie ma.
Ruchem jest przeczytanie, które kategorie Składnicy stoją nad imiesłowem
biernym i nad bezokolicznikiem i czy któraś z nich jest dla olskiego zdaniem —
dla werdyktu jest, bo gospodarzem jest tam forma czasownikowa.
Ceną jest to, że `CLAUSE` czyta zarazem
[tabela przyłączeń](docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia),
więc kategoria dopisana tam rusza figurę, której ten wpis nie dotyczy,
i przeliczenie obu idzie razem z tą zmianą.

Nieterminal banku drzew niesie nazwę reguły, a pyta o nią jedna sonda z pięciu.
`rule` w `Constituent` (`harness/corpus.py`) doszło tam po to, żeby policzyć
apozycję, której kategoria nie rozdziela od przydawki dopełniaczowej,
i ta sama różnica stoi pod innymi pytaniami tego katalogu:
`harness/attachment.py` rozdziela gospodarzy kategorią rodzica,
a kategoria mówi, czym rodzic jest, gdzie reguła mówi, którą konstrukcją powstał.
Ruchem jest przeczytanie, czy wzorce bez pokrycia z wpisu o 184 przyłączeniach
rozdzielają się regułą tam, gdzie kategoria je zlewa;
jeżeli tak, wpis tamten zamyka reguła, a nie kategoria dopisana do `CLAUSE`,
której ceną jest figura przeliczana razem z nią.
Do przeczytania jest przedtem, ile reguł stoi nad kategoriami, które `CLAUSE`
wylicza, bo od tej liczby zależy, czym ten ruch będzie:
garść reguł nad setkami zdań jest kryterium,
a setka reguł nad garścią zdań jest listą pisaną ręką.

Stopa pomyłek warstwy jest zmierzona na 29 odpowiedziach i tyle nie odróżnia
rejestru od banku drzew, więc
[druga połowa hipotezy](docs/disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza)
zostaje nierozstrzygnięta; liczby trzyma
[częstość nad dokumentacją](docs/disambiguation.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania).
Ruchem jest `python3 -m harness.wybory --zbuduj proza/ --z-odpowiedzią` na większe `--ile`
i przeczytanie tego, co dojdzie; pozycji z odpowiedzią jest w tym korpusie 122,
więc cała populacja mieści się w czterech takich próbach.
Kupuje to przedział, a nie liczbę, i tyle jest tu do kupienia za cztery próby czytane ręką:
przy dzisiejszej stopie wszystkie 122 odpowiedzi dają przedział od 11% do 25%,
czyli mijają co dziesiątą odpowiedź o włos.
Do rozstrzygnięcia jest przy tym, o czym mówi liczba wzięta do końca nad tym korpusem:
pozycje z odpowiedzią pochodzą z dwóch repozytoriów
([`docs/audit-corpus.md`](docs/audit-corpus.md#the-list)),
więc rejestrem, o którym stopa pomyłek wtedy mówi, są te dwa,
a nie dokumentacja techniczna w ogóle.

Wsparcie dwóch wypadków banku drzew jest nad dokumentacją progiem, przy którym
tabela skłonności myli się częściej, niż trafia:
cztery pomyłki z siedmiu odpowiedzi opartych na tym wsparciu, wobec jednej z 22 powyżej
([częstość nad dokumentacją](docs/disambiguation.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)).
Ruchem jest `WSPARCIE` w `olski/rozstrzyganie.py` podniesione do trzech,
a przed nim cena po drugiej stronie, bo próg jest punktem na krzywej i tam jest jego właściciel:
`python3 -m harness.skłonności <Składnica> --oceń` wypisuje zasięg i trafność
dla `(3, 0.85)` obok dzisiejszego `(2, 0.85)`, więc liczba jest jednym przebiegiem.
Do przeczytania jest, co robi z trzema trafnymi odpowiedziami spod wsparcia dwóch:
wszystkie trzy są liczebnikiem cząstkowym (`jednego z kilku uprawnień`),
czyli klasą, którą rozstrzyga reguła, a nie częstość,
więc próg podniesiony zabiera odpowiedzi, których tabela i tak nie powinna wydawać.
Zmiana rusza przy tym tabelę nad werdyktami banku drzew, obie próby czytane ręką
i figury w `docs/disambiguation.md`, które je cytują,
a `próbę zawężoną do odpowiedzi` przerysowuje w całości, bo losowanie idzie po odpowiedziach.

Próba wyborów jest losowaniem nad populacją, której `pytania` już nie daje.
Wpisy w `próba/wybory.txt` padły nad populacją mniejszą i przy innej propozycji gospodarza,
niż daje dzisiejsze `pytania` w `harness/wieloznaczność.py`, więc ta sama komenda z `--ile 30`
dzieli z tym plikiem dwa zdania z trzydziestu
([tamże](docs/disambiguation.md#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów)).
Sądów to nie unieważnia, bo zdanie i fraza stoją we wpisie w całości,
a psuje powiększanie: `rozrzucona` w `harness/próbka.py` bierze co którąś pozycję,
więc próba większa jest siatką przerysowaną od zera, a nie tą siatką z wpisami między nimi.
Ruchem jest jedno z dwojga: albo przerysowanie siatki wraz z przeczytaniem tych wpisów,
które na nią nie trafiły, albo `--zbuduj` z pominięciem pozycji już przeczytanych,
co daje próbę o rozkładzie zszytym z dwóch populacji i mianownik trzeba wtedy nazwać.
Do przeczytania jest, ile z trzydziestu sądów pierwsza droga każe wziąć drugi raz,
bo od tego zależy, która jest tańsza.
Tego samego rozstrzygnięcia żąda `próba/wybory-z-odpowiedzią.txt`, i ostrzej,
bo tam populację rusza każda zmiana w warstwie, a nie tylko zmiana w szukaczu pozycji.
Ruszyła ją już jedna: świadek ramowy stanął przed tabelą, więc część odpowiedzi
przeczytanych w tym pliku jako odpowiedzi tabeli wydaje teraz rama, i wniosek
[tamtej sekcji](docs/disambiguation.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)
mówi o tym, co tabela robiła, a nie o tym, co warstwa robi.

Leksykon walencyjny mówi o bierniku i o bezokoliczniku, a o przypadkach nie mówi.
Narzędnika [przekład](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)
nie bierze, bo `inst` jest u olskiego pozycją orzecznika,
a Walenty nie odróżnia jej od argumentu narzędnikowego,
więc kopula zostaje listą pisaną ręcznie w `olski/subset.py`.
Do przeczytania jest, czy bank drzew tę różnicę widzi:
pozycja `adjp(pred)` stoi w polu `tfw` obok `np(inst)`,
a `harness/corpus.py` czyta dziś z tego pola podmiot i dopełnienie.
Gdyby ją widział, kopula przestaje być listą, a staje się wpisem jak każdy inny,
i wtedy pytaniem jest, ile czasowników poza nią orzecznik w narzędniku bierze.

Rzeczownikowe czytanie przymiotnika zabiera README ostatnie zdanie
i nie widać przy nim tego, co zdjęło zaimek.
`Linter pomaga pisać dobry kod.` wychodzi dwoma czytaniami tego samego kształtu,
bo Morfeusz daje `dobry` czytanie `subst:sg:nom.acc:m3` obok przymiotnikowego,
a `kod` czytanie lematu `koda` w dopełniaczu mnogim,
więc `dobry kod` jest raz przymiotnikiem przed rzeczownikiem,
a raz rzeczownikiem z dopełniaczem po nim.
Zaimek rzeczowny zdjął z tej klasy
[warunek w produkcji](docs/subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
bo `to` dopełniacza nie bierze,
a `dobry` bierze: rzeczownik odprzymiotnikowy dopełniaczem rządzi
i kryterium na tę pozycję zabiera zdania Składnicy, w których rządzi,
co zmierzone stoi w
[`docs/subset.md`](docs/subset.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi).
Zostaje więc sąsiad, nie głowa:
pary nie ma bez dopełniacza `kod`, czyli bez lematu `koda`,
którego ten rejestr nie zna,
a rzadkość formalnego znamienia nie ma.
Do przeczytania jest, czy da się ją policzyć tak,
żeby liczba mówiła o polszczyźnie, a nie o korpusie, w którym się ją policzyło,
i pierwszym pytaniem jest, czy jakiekolwiek kryterium tu jest;
wykluczenie zbyt szerokie zabiera zwyczajne polskie słowa,
co [`docs/subset.md`](docs/subset.md#the-dictionary-offers-readings-polish-does-not)
pokazuje na `jury` i `menu`.
Ten sam sąd niesie wpis o czytaniu przysłówkowym formy,
której ten rejestr używa jako przyimka albo spójnika,
bo oba pytają, co wykluczeniu w `admissible` wolno powiedzieć,
więc rozstrzyga je jedna sesja, a nie dwie.
Zdanie to jest przy tym warunkiem pod
[kierunkiem toru](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę),
bo czytanie, którego polszczyzna nie ma, jest dokładnie tym,
czego werdykt meldować nie powinien.

Maskowanie nieciągłości zmierzono nad Składnicą, a nad rejestrem docelowym nie,
i korpus prasowy zaniża tę liczbę względem dokumentacji, zamiast ją zawyżać,
czym różni się od pozostałych liczb tamtej sekcji.
[Sekcja](docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
wywodzi tę klasę z rzeczownika,
który wybiera ten sam przyimek co rama czasownika przed nim —
`dziadek do orzechów`, `maszyna do szycia` —
a dokumentacja techniczna tak właśnie nazywa swoje narzędzia,
więc `narzędzie do podpisu` czy `moduł do fakturowania` są tam budulcem.
Ruchem jest trzecia pozycja dopisana do `harness/wieloznaczność.py`,
który dwie takie liczy nad korpusem audytowym i ma na to całą maszynerię:
rzeczownik, forma osobowa, a za nią przyimek, który ten rzeczownik bierze.
Ostatni warunek ma skąd się wziąć:
`olski/leksykon.txt` niesie przyimki ramy rzeczownika, a pyta o nie
`przyimki_rzeczownika` w `olski/walencja.py`, czyli ta sama droga, którą pyta
świadek ramowy.
Do przeczytania jest zasięg tej kolumny nad tym korpusem, bo plik rzeczownikowy
Walentego wylicza 1 996 lematów, a `narzędzie` i `moduł` są tu tymi, na których
wszystko stoi: pozycja licząca się z ramy nieobecnej liczy zero i nie mówi tego.

Figury brane nad gramatyką z wyjętą grupą produkcji
bierze każda sesja własnym skryptem, bo żadnego nie ma w repozytorium,
i dobiera do niego wariant, którego dokument nie nazywa.
Dotyczy to `docs/corpus.md` oraz pomiaru pozycji z obiema przydawkami w
[`docs/ustawy.md`](docs/ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa),
gdzie grupą są dwa ciała `NPConjunct` z przymiotnikiem i dopełniaczem pod głową,
czyli to z wyrażeniem przyimkowym na końcu i to bez niego.
Przy pozycjach przyłączeniowych granica grupy jest już wypisana
([`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)),
a przy [zdaniach, które rama zdejmuje](docs/corpus.md#what-morphological-ambiguity-costs)
nie jest: liczby odtwarza leksykon z biernikiem dopisanym kopuli,
i dokument tego nie mówi.
Wariantów jest przy tym więcej niż dwa i każdy stawia tę samą pułapkę.
Cena podrzędności żąda gramatyki bez `SubordinateClause` i bez `comp` w ramie,
a cena zdania względnego — bez produkcji względnych,
przy czym wariant zbudowany przez podmianę `ZAIMEK_PYTAJNO_WZGLĘDNY`
zdejmuje trzy naraz, bo ta stała stoi w wykluczeniu, w terminalu zaimka
i w terminalu grupy pytajnej,
więc sesja mierzy wtedy co innego, niż myśli, i nic jej o tym nie mówi.
Do przeczytania jest ta sekcja wraz z `_klasy` z `olski/subset.py`,
bo ramę zawęża ona i tylko ona.
Ruchem jest predykat nad `harness/ruch.py`, który te warianty buduje i drukuje,
wraz ze zdaniem w obu dokumentach mówiącym, że figury bierze się nim.
Pomiar zdejmuje z tych figur najdroższą pozycję:
zgadywanie, co poprzednia sesja zmierzyła.

Żadna z dwóch kolumn w
[`docs/corpus.md`](docs/corpus.md#what-morphological-ambiguity-costs)
nie pochodzi od tagera, więc nikt nie policzył, ile z ich różnicy tager odbiera.
Kandydatem jest [Concraft](docs/prior-art.md#polish-language-resources),
a rozstrzyga o nim jedna własność wyjścia:
czy wybrana interpretacja niesie jedną wartość przypadka, czy dysjunkcję.
`subst:sg:nom.acc:m3` jest w `olski/morph.py` jedną interpretacją z cechą mnogą,
więc tager, który ją wybierze i zostawi `nom.acc`, synkretyzmu nie zdejmuje,
a od synkretyzmu własność jednoznaczności się zaczyna
([`docs/subset.md`](docs/subset.md#validity-is-uniqueness-not-just-derivability)).
Ruchem jest przebieg Concrafta nad kilkoma zdaniami i odczytanie tego pola.
Trzecia kolumna dopiero po nim, bo Concraft to binarium Haskella
i model stumegabajtowy, czyli zależność pomiaru z fetchem, jak Składnica i Walenty,
a takiej nie warto zaciągać pod przebieg, który nie ruszy ani jednego zdania.
Po stronie złotej morfologii pytanie wygląda na zamknięte:
`terminal` w `tests/test_corpus.py` pisze `subst:sg:nom:m3` z jedną wartością,
a docstring tego pliku ręczy, że format przepisano z wydania z 2018.
Ręczy jedna osoba i żaden plik banku, więc gdyby Concraft wypadł ciekawie,
sprawdź to na wydaniu, zanim trzecia liczba wejdzie do dokumentu.

Warstwa rozstrzygająca tnie gospodarza inaczej niż gramatyka, kiedy jest nim notacja.
`_czytania` w `olski/rozstrzyganie.py` woła `analyse`,
więc `docs/linter.md` wraca pięcioma lematami —
`docs`, `linter`, `md` oraz kropka i ukośnik —
a `morphology` w `olski/segmentacja.py` ma tam jedną krawędź o czytaniu nieodmiennym.
Nie kończy się to milczeniem:
gospodarz `docs/linter.md` dopasowuje się do słowa `linter`
stojącego w akapicie gdziekolwiek,
a powód wypisuje wtedy to drugie słowo,
więc wskazanie samo mówi, że stoi na dowodzie o czym innym.
Ruchem jest sklejenie notacji pytane przez oba miejsca,
czyli `_segmenty` w `olski/segmentacja.py` wołane tą samą drogą,
którą oba pytają dziś o leksykon projektu.
Wpis jest winien przebieg nad korpusem audytowym,
bo dokumentacja techniczna pisze notację gęsto,
a wskazania warstwy nad tym korpusem liczy `harness/powtórzenie.py`
i cytuje je [`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek).
Do rozstrzygnięcia jest przy tym, czy warstwa ma widzieć dwa pozostałe kroki analizy:
`admissible` odbiera czytania, których polszczyzna nie ma,
a `po_przyimku` pyta o sąsiada, którego przy gospodarzu wziętym z werdyktu nie ma.

Nie wiadomo, w ilu miejscach decyzja o konstytuencie jest w olskim ta sama,
co w GFJP, a pomiar nad Składnicą tego nie powie
([`docs/swigra.md`](docs/swigra.md#którędy-gfjp-wchodzi-do-olskiego) mówi dlaczego).
Ruchem jest przejść listę konstrukcji z [`docs/subset.md`](docs/subset.md)
obok `gfjp2.dcg` ze `swigra_current.zip`
i wypisać, gdzie obie gramatyki przyłączają tak samo, a gdzie inaczej.
Nie po to, żeby różnić się celowo:
po to, żeby o każdej takiej decyzji dało się powiedzieć, czy jest wyborem.
Do przeczytania jest `gfjp2.dcg` i czyta się go inaczej, niż wygląda:
nazwy nieterminali są tam formalne — `fno`, `fw`, `fl` —
a olski nazywa symbole funkcjami, czyli `Subject` i `Object`,
więc porównanie prowadzi to, co produkcja przyjmuje, a nie nazwa symbolu.
Sesja jest osobna i nie dzieli się na pliki,
bo rozstrzyga jedno pytanie na całej liście naraz.

Przydawka imiesłowowa podniosła liczbę zdań, w których przyjęte czytanie
przeczy drzewu wzorcowemu, a przebieg, który to pokazał, nie mówi, czym te zdania są
([`docs/subset.md`](docs/subset.md#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik)).
Kierunek żąda od werdyktu prawdy o zdaniu
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
więc pozycja, która kupuje pokrycie i sprzedaje zgodność, żąda odczytania,
a nie samej liczby.
Do przeczytania jest `python3 -m harness.pomiar <korpus> --examples`
w wierszach `disagrees` oraz w tych, którym złote czytanie z lasu wypada,
i pytanie do nich jest jedno: czy pomyłki stoją na jednym kształcie.
Ciała są dwa, po jednym na imiesłów, więc kształt zdejmuje się po jednym
i przelicza obie liczby; sonda różnicowa robi to nad `harness/ruch.py`.
Gdzie pomyłki się rozchodzą, całą zmianą jest zdanie o tym w tamtej sekcji,
bo wtedy cena jest ceną przydawki, a nie jednego z dwóch imiesłowów.

Trzy przykłady w [sekcji o nieciągłości](docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
mówią o zatrzymaniach, których olski już nie ma: `Co mamy wziąć?` i `To chcę
podkreślić.` stają dziś na bezokoliczniku, a nie na zaimku rzeczownym, więc zdanie
o tym, że wszystkie trzy staną na pierwszym słowie, jest nieprawdziwe — pierwsze
z nich stawało na zaimku, którego pozycji rzeczownej nie ma
([`docs/subset.md`](docs/subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Ruchem jest przebieg nad tamtym zbiorem 323 zdań i przepisanie tych przykładów na
takie, które dziś stają tam, gdzie akapit mówi; sam akapit twierdzi rzecz szerszą —
że nieciągłość jest w tych zdaniach brakiem ostatnim — i tej ta poprawka nie tyka.
Do przeczytania jest `harness/nieciągłość.py`, bo on ten zbiór wyznacza,
oraz `bloker` w `olski/pokrycie.py`, bo stamtąd bierze się nazwa
zatrzymania.

Zdanie leksykonu o parze przemilcza, które wypełnienie przy celowniku stoi,
więc lemat z parą bierze wszystkie cztery naraz
([`docs/subset.md`](docs/subset.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).
Walenty rozdziela je i mówi to o tysiącach lematów, których rozkład trzyma
tamta sekcja: `pokazywać` ma parę z biernikiem, ze zdaniem i z pytaniem,
a z bezokolicznikiem jej nie ma, więc `Parser pokazuje autorowi zapisać ustawienia.`
wyprowadza się i polszczyzną nie jest.
Ruchem są cztery zdania leksykonu w miejsce jednego,
a wraz z nimi cztery wartości cechy `druga` w `olski/subset.py` zamiast jednej.
Do rozstrzygnięcia jest, czy warto:
rama domyślna daje każdemu czasownikowi te same cztery wypełnienia naraz,
więc para rozdzielona byłaby dokładniejsza od ramy, do której dochodzi,
a klas walencyjnych przybywa wtedy tyle, ile jest podzbiorów tej czwórki.
Do przeczytania jest cena dzisiejszej zgrubności, której nikt nie policzył:
ile zdań Składnicy przechodzi przez parę, której schemat lematu nie ma.

Dopełniacz nie ma drugiej pozycji ramy, którą ma celownik
([`docs/subset.md`](docs/subset.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).
Walenty daje go przy bierniku 15 lematom, przy pytaniu 28, a przy zdaniu 6,
i te liczby są całym powodem, dla którego pozycja weszła sama celownikiem.
Ruchem jest druga wartość cechy `druga` w `olski/subset.py`
wraz ze zdaniem leksykonu liczonym tak samo jak tamto,
a przed nim pomiar, bo cena tej pozycji jest po stronie żywej morfologii wysoka:
celownik dzieli formę z miejscownikiem, a dopełniacz z biernikiem i z mianownikiem mnogim.
Do przeczytania jest, czy zdanie z tą parą da się w ogóle odróżnić po werdykcie:
`Nauczyciel uczy dzieci matematyki.` wyprowadza się już dziś,
bo dopełniacz za grupą imienną czyta się jej przydawką,
więc brak tej pozycji nie odrzuca zdania, tylko odbiera mu drugie czytanie.

Dwie liczby w [`docs/disambiguation.md`](docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)
są wyższe od tego, co mówi przebieg.
Dokument mówi, że przyłączenie jest całą decyzją w siedmiu zdaniach na dziesięć,
a w dwóch klasach, które je nazywają, w przeszło czterech piątych,
gdy `python3 -m harness.czytania` nad Składnicą 180723 mówi dziś mniej:
przeszło trzy piąte i przeszło trzy czwarte.
Ruchem jest granica postawiona po tej stronie, po której stoi pomiar
([`CLAUDE.md`](CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)),
albo zdanie oddające obie liczby przebiegowi.
Do przeczytania jest akapit pod nimi, bo argumentuje on ich rzędem wielkości,
oraz sam wydruk, bo drugą z tych liczb przebieg drukuje osobno dla każdej z dwóch klas,
a granica trzyma się tylko pod jedną z nich.

Zawężenie orzecznika zgodnego ma wycenę nad prozą repozytorium i nie ma decyzji,
bo populacja jest tam tej wielkości, że czterema zdaniami przewraca wniosek
([`docs/subset.md`](docs/subset.md#zawężenie-orzecznika-zgodnego-wyceniono-i-decyzji-nie-ma)
trzyma cenę wraz z tym, co przy niej przeczytano).
Ruchem jest ten sam wariant puszczony nad Składnicą — rama bez pozycji `nom`
wszędzie poza kopulą — z pytaniem, ilu zdaniom ginie czytanie złote,
bo tego pytania proza postawić nie umie, nie mając anotacji.
Do przeczytania jest przy tym kryterium po stronie przymiotnika, które tamta sekcja
nazywa tańszym: jeżeli katalog przymiotnikowy Walentego je daje, wybór między
wpuszczeniem a zawężeniem po stronie czasownika przestaje być potrzebny,
a wtedy cały ten wpis zamyka wpis o przymiotniku.

Rama jest w tej gramatyce stanem, a nie zasobem, i nikt nie policzył, co to kosztuje.
Pozycji już zajętej unifikacja nie ma jak odnotować, bo zajęcie zależy od pozostałych
córek, a nie od pary głowy i zależnego, i na tym walencja wypadła z kanału cech
([`docs/design-notes.md`](docs/design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)).
Sonda więzowa płaci za to samo dwoma polami sprawdzanymi nad drzewem gotowym,
czyli `wymaga` i `zakazuje` w `harness/wiezy.py`,
i jest to jedyny znany warunek, którego przecięcie zbiorów nie umie powiedzieć,
a warstwa za parserem umiałaby.
Do przeczytania jest przedtem, czy w tej gramatyce jest w ogóle co zdejmować:
ciało produkcji wylicza córki, więc pozycja wypełniona dwa razy żąda dwóch ciał,
a jeżeli żadne takie nie stoi, cały wpis zamyka skasowanie z powodem w commicie.
Jeśli stoi, ruchem jest warunek nad czytaniem gotowym wraz z jego ceną
zmierzoną tak, jak mierzy się wpuszczenie pozycji.

Wykaz morfologii sumuje odczytania po ciałach jednej klasy, a klasy sąsiedniej nie widzi.
`Las._wsparte_kształtu` w `olski/parse.py` idzie po produkcjach spakowanych
pod jedną parą pozycji i klasy cech, więc ciało, które ten sam kształt buduje,
wypuszczając cechy z klasy obok, do sumy nie wchodzi.
Widać to na lemacie, którego leksykon walencyjny nie zna:
`Granicę pokazuje sama odpowiedź.` wypisuje `pokazywać`, a `pokazować` przemilcza,
bo `olski/leksykon.txt` ma wpis tylko dla pierwszego,
więc drugi bierze ramę domyślną i wychodzi inną klasą walencyjną.
Nad zdaniami README trafia to na trzy formy — `pokazuje`, `staje`, `zeszła` —
i na lematy, których ten rejestr nie używa: `pokazować`, `stajać`, `zniść`.
Do przeczytania jest przedtem, czy klasa jest wyborem rodzica, czy tylko kanałem cech:
suma sięgająca do klasy obok mówi, że forma stoi tu pod ramą,
której rodzic nie wziął, a suma w obrębie klasy tego nie mówi.
Wpis zamyka się też przez to, że tak zostaje, i wtedy powód idzie do
`Las._wsparte_kształtu`, bo dziś stoi tam granica bez wywodu.
Sondą jest warunek, który `tests/test_subset.py` sprawdza na garści zdań —
zdanie zawężone do odczytań liści wyprowadza ten sam kształt —
puszczony nad całym README, bo w tamtej garści tej klasy nie ma.

Produkcji, której żadne ciało nie dopasuje, nie pilnuje nic.
`Object → NP[case=inf]` stała w gramatyce tak długo, ile trwało czytanie
`DOKŁADANE` jako listy przypadków, i nie odbierała ani zdania, ani czytania:
grupa imienna przypadka `inf` nie niesie, więc ciało po prostu nie domykało się
nigdy.
Suita tego nie widzi, bo werdykty wychodzą te same,
a `nieosiągalne` w `olski/grammar.py` też nie, bo pyta o symbol,
a tu nieosiągalny jest układ cech pod symbolem osiągalnym.
Znalazła ją ręka, czytając trzy miejsca, które wypisywały jedną listę.
Ruchem jest check pytający o wartość, a nie o nazwę:
dla każdej pozycji ciała będącej `Sym` z wartością wypisaną wprost
ma istnieć produkcja tego symbolu, która tę wartość wypuszcza.
Do przeczytania jest przedtem, ile taki check kosztuje wyprowadzenia:
cecha idzie zwykle zmienną wspólną z córką, więc odpowiedź żąda punktu stałego
po całej gramatyce, a nie spojrzenia na jedną produkcję,
i to rozstrzyga, czy jest to check, czy sonda puszczana ręką.
Wynikiem pierwszego przebiegu jest lista produkcji martwych,
a każda z nich jest albo skreśleniem, albo pozycją napisaną nie tak, jak chciano.

Rzeczownik `soba` zabiera kilkunastu zdaniom banku drzew jednoznaczność,
odkąd zaimek zwrotny ma pozycję
([`docs/subset.md`](docs/subset.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym)).
Czytania tego polszczyzna w tych zdaniach nie ma —
`sobie` i `sobą` są w nich zaimkiem — więc jest to wieloznaczność w słowniku,
a nie w polszczyźnie, czyli dokładnie to, co odbiera `admissible`
w `olski/segmentacja.py`
([`docs/subset.md`](docs/subset.md#the-dictionary-offers-readings-polish-does-not)).
Kryterium tamtego wykluczenia po ten lemat nie sięga i sięgnąć nie może:
pyta ono o rzeczownik nieodmienny, a `soba` odmienia się przez przypadki.
Mechanizm już stoi — `pomijane` w sekcji `lematy` w `olski.toml`
([`docs/subset.md`](docs/subset.md#słownictwo-projektu-orzeka-o-lemacie-w-obie-strony)) —
a nie stoi w nim ani jeden lemat i to jest tu decyzja do podjęcia.
Do przeczytania jest przedtem, ile takich lematów widać nad bankiem drzew:
sonda różnicowa zaimka wypisuje zdania tracące jednoznaczność pod żywą
morfologią i tyle wystarcza, żeby powiedzieć, czy lemat jest jeden, czy jest ich wiele.
Liczba ta rozstrzyga, czy `soba` idzie do konfiguracji tego repozytorium sama,
czy razem z listą, która rośnie o każdy lemat, który ktoś zauważy.
Ten sam lemat trzyma zarazem drugą pozycję poza zasięgiem pomiaru.
Orzecznika narzędnikowego zaimek zwrotny nie ma, a `Parser jest sobą.` mimo to
wychodzi jednoznaczne, bo bierze je `soba`,
więc dopisanie tej pozycji zamieniłoby jedno czytanie na dwa,
a nie odebrałoby odrzucenia.
Wykluczenie lematu idzie przez to przed pozycją, a nie po niej:
po nim widać, ile ta pozycja naprawdę kupuje.

Autor nie ma jak zobaczyć, co wykluczenie słownikowe wycięło jego tekstowi.
Lemat, który przez nie przepadł, nie zostawia po sobie ani wiersza werdyktu:
`Go jest grą.` melduje zatrzymanie na `grą`, czyli miejsce, w którym gramatyce
zabrakło podmiotu, a nie to, w którym zabrano czytanie
([`docs/subset.md`](docs/subset.md#słownictwo-projektu-orzeka-o-lemacie-w-obie-strony)).
Kierunek `wpuszczane` umie przez to napisać ten, kto już wie, co napisać.
Ruchem jest wiersz wykazu morfologii o czytaniu zdjętym przez wykluczenie.
Do przeczytania jest przedtem `_morfologia` w `olski/check.py`,
bo wykaz ten wypisuje czytania, które do rozbioru weszły,
a odpowiedzi trzeba tu o czytanie, którego w nim nie ma.

Nie wiadomo, czy `CLOSED_CLASS` ma zostać w kodzie.
Wykluczenie jest zakładem o rejestr, więc domyślność dostarczana z paczką jako
konfiguracja byłaby uczciwsza wobec czytelnika werdyktu: projekt nadpisuje ją
tam, gdzie chce, i widzi ją tak samo jak własną.
Ceną są dwa pliki zamiast jednego,
czyli `znajdź` w `olski/konfiguracja.py` przestający być całą regułą szukania.
Wpis czeka na ten wyżej, bo o cenie rozstrzyga to, czy autor ma już skąd wiedzieć,
co mu się wycina: kiedy ma, druga droga kupuje samo nadpisywanie.

Deklaracji martwej nie pilnuje nic.
Lemat wpisany do `wpuszczane`, po który wykluczenie i tak by nie sięgnęło —
bo słownik nie daje mu czytania nieodmiennego obok klasy zamkniętej —
nie zmienia ani jednego werdyktu i nie zgłasza się,
tak samo jak lemat wpisany do `pomijane`, którego słownik nie zna wcale.
Jest to ta sama klasa, którą po stronie leksykonu łapie świadek
([`docs/subset.md`](docs/subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)),
i tam wpis zły zgłasza się, a tutaj milczy.
Ruchem jest check pytający słownik o lemat przy czytaniu konfiguracji.
Do rozstrzygnięcia jest przedtem cena: `olski/konfiguracja.py` czyta się przy
imporcie i nie żąda dziś Morfeusza w żadnym trybie,
a check ten kazałby żądać go każdemu, kto pyta o samą konfigurację.

Spójnik dzieli się w `olski/subset.py` na kilka list lematów,
a jak się one mają do siebie, nie mówi ani jedno miejsce.
Listy te odpowiadają na różne pytania o lemat — czy żąda przecinka,
czy bierze człon bez czasownika, czy stoi wewnątrz zdania,
czy powtarza się przed każdym członem, czy otwiera całe zdanie —
więc przecinają się i przecinać się mają: `natomiast` stoi w trzech.
Rozejść, których nikt nie chce, żadna z nich jednak nie widzi,
a kosztują one czytanie nieprawdziwe, którego pomiar różnicowy nie pokazuje:
lemat mający już pozycję podporządkowującą, dopisany do listy koordynacyjnej,
daje drugie wyprowadzenie zdaniu, które i bez niego jest wieloznaczne.
Tak wypadło `czy` z listy skorelowanych
([`docs/subset.md`](docs/subset.md#spójnik-skorelowany-powtarza-się-przed-każdym-członem)),
a złapała je ręka, nie przebieg; `tests/test_subset.py` pilnuje odtąd tej jednej pary.
Ruchem jest check nad wszystkimi parami naraz,
a do rozstrzygnięcia jest jego kryterium:
przecięcie samo w sobie usterką nie jest, więc check musi pytać o coś węższego,
i pierwszym kandydatem jest para, w której jedna lista podporządkowuje,
a druga koordynuje.

## Konstrukcje, których gramatyka nie ma

Łącznik `to` nie stoi przy formie osobowej ani przy przeczeniu.
`Był to nieforemny chłopak.`, `To są oczywistości.` i `Parser to nie kompilator.`
są odrzucone, gdzie `Flaga to płat tkaniny.` wyprowadza się
([`docs/subset.md`](docs/subset.md#łącznik-to-orzeka-bez-czasownika-a-podmiot-stoi-za-nim)).
Ruchy są dwa, a pierwszy jest wart więcej:
łącznik przy czasowniku prowadzi resztę wiersza `pred` kolejki blokerów
i stoi w nim setkami zdań, w obu szykach niemal po równo.
Przeczenia przy łączniku nie policzył nikt i ten wiersz o nim nie mówi,
bo takie zdanie staje na grupie za `nie`, a nie na samym łączniku.
Do przeczytania jest ten wiersz, a wycenić trzeba każdy szyk osobno,
bo pozycja pod jednym symbolem zabrałaby pomiar obu naraz
([CLAUDE.md](CLAUDE.md#code)).

Ciąg pytań zależnych nie bierze pytania z orzecznikiem jako członu pierwszego.
`Pyta, co to jest i czy to działa.` staje na `czy`,
a `Pyta, co to jest.` oraz `Pyta, kto płaci i czy to działa.` wyprowadzają się,
więc brak jest w samym złożeniu, a nie w żadnym z dwóch czół
([`docs/subset.md`](docs/subset.md#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą)).
Do przeczytania jest `InterrogativeChain` w `olski/subset.py` obok pozycji
orzecznika wysuniętego, bo pytanie jest o to, czy człon z orzecznikiem
wypuszcza cechę, której ciało ciągu żąda od członu pierwszego.
Zdanie to pisze `docs/roles.md`, a odrzucenie jest werdyktem uczciwym,
więc pozycja nie ma pilności, jaką miałby brak wydający `valid`.

Para myślników nie ma wyprowadzenia, a wtrącenie, którego żąda, stoi w środku zdania,
gdzie obie pozycje nawiasu zamykają zdanie,
więc jest to pozycja nowa, a nie drugi znak w gotowym ciele
([`docs/subset.md`](docs/subset.md#what-it-does-not-cover-yet)).
Ruchem jest para jako jedna córka w tym miejscu, które wylicza rozwinięcie szyku,
czyli tam, gdzie staje okolicznik zdania.
Do przeczytania jest ciało wtrącenia w `olski/subset.py` obok `Rozwinięcie`
w `olski/precedencja.py`, bo pytanie jest o to, ile czytań ta pozycja dokłada
zdaniu, które parę stawia na końcu: tam da się ją przyłączyć do zdania składowego
i do zdania nad nim, czyli tak samo jak drugą pozycję nawiasu wyżej.

Wypełnienie inne niż dopełnienie, wysunięte przed głowę, która orzeka bez podmiotu,
nie ma ani pozycji, ani ceny, bo deklaracja tej pozycji bierze samo dopełnienie
([`docs/subset.md`](docs/subset.md#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu)).
Populacji, której to dotyczy, nie przeczytał nikt:
wiersz `imps` został po wpuszczeniu formy nieosobowej z blisko setką zdań Składnicy,
a wysunięte dopełnienie zabrało z niego część i nie wiadomo którą.
Ruchem jest przeczytanie tej resztki, a po nim wycena pozostałych wypełnień
nad obiema głowami naraz: deklaracja bierze głowę nazwą symbolu,
więc wypełnienie dopisane do niej obejmuje predykatyw i formę nieosobową razem.
Do przeczytania jest `bloker` w `olski/pokrycie.py` z tego samego powodu,
z którego czyta go wpis o resztce `praet`: nazywa on formę, a nie przyczynę.

Kopuła opuszczona ma listę o jednym lemacie, a polszczyzna opuszcza ją szerzej.
`RZECZOWNIK_ORZEKAJĄCY` w `olski/subset.py` wymienia `mowa`,
bo tego lematu zażądał rejestr ustaw,
a `brak dowodów`, `szkoda czasu` i `pora wracać` są tą samą konstrukcją:
rzeczownik w mianowniku orzeka, a czasownika nad nim nie ma.
Wypełnienia żąda przy tym każdy z tych trzech innego niż `mowa` —
dopełniacza albo bezokolicznika, a nie okolicznika —
więc lemat dopisany do listy nie wystarcza,
a wpis jest przez to o produkcję, a nie o dane.
Ruchem jest lista wyczytana z korpusu, a nie z pamięci,
a materiał do jej wyczytania daje pozycja ogólna dopisana do gramatyki:
[`docs/subset.md`](docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną)
nazywa dwie produkcje, które ona dopisuje,
a zdanie, które dzięki nim przechodzi, pokazuje rzeczownik w nim orzekający.
Do przeczytania jest, ile z tych zdań jest ciągiem współrzędnym grup imiennych,
bo tym była większość zakupu tamtej pozycji nad siedmioma ustawami,
a lemat dopisany za taki ciąg wraca ceną w każdym zdaniu, które ten ciąg niesie.
Cenę każdego lematu bierze potem sonda kopuły odtworzona z commita, który ją trzyma,
tak jak wzięła cenę tego jednego.

Człon lewy ciągu współrzędnego nie unosi zdania względnego.
Produkcja `NP → NPConjunct RelativeClause` w `olski/subset.py`
żąda członu, a produkcja koordynacji daje po lewej człon i po prawej ciąg,
więc `pliki, które rosną, i katalogi` nie ma wyprowadzenia,
a `pliki i katalogi, które rosną` ma.
Ruchem jest symbol między `NP` a `NPConjunct`, przez który idą oba człony,
i ruch ten zbudowano na próbę, więc cena jest policzona, a zakup nie.
Cena ma trzy pozycje.
Nad Składnicą pod Morfeuszem jedno zdanie traci jednoznaczność —
`Przez czynniki ekonomiczne należy rozumieć te, które kształtują rozmiary
i strukturę dochodów oraz wydatków budżetowych.` wychodzi trzema czytaniami
zamiast jednego, bo `te, które kształtują rozmiary` staje się członem ciągu —
i jest to czytanie, które polszczyzna ma, więc nie jest to usterka, tylko cena.
Pod złotą morfologią nie rusza się ani jedno zdanie.
Trzecią pozycją jest `_role` w `olski/skład/rozbiór.py`:
czyta ono kształty gramatyki po etykiecie,
więc każdy nowy poziom kosztuje tam gałąź, a obieg zamknięty bez niej pada.
Taki ciąg niosą cztery zdania Składnicy z 13035 mających drzewo wzorcowe
(`python3 -m harness.kształty`); nad ustawami nie policzył ich nikt.
Każde z tych czterech ma powyżej piętnastu słów, a jedno dwadzieścia pięć,
więc zakup jest mniejszy niż sama czwórka:
zdanie tej długości pada zwykle na czymś jeszcze,
a wpuszczona produkcja kupuje je dopiero wtedy, gdy pada wyłącznie na niej.
Kto ten wpis podnosi, nie zamknie go tą liczbą, bo cztery zdania przeciw jednemu
traconemu i gałęzi w `_role` ważą tyle samo.
Zamyka go pytanie o czytanie: to, które ten ciąg dokłada, polszczyzna ma,
więc dopisanie produkcji odbiera werdykt nieprawdziwy, a nie samą jednoznaczność,
i po tej stronie stoi
[kierunek](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).

Apozycji olski nie ma, więc przecinek przed wyliczeniem ma u niego jedno czytanie.
`Przyszli moi sąsiedzi, lekarz i nauczyciel.` wychodzi jednym czytaniem,
`[moi sąsiedzi], lekarz i nauczyciel`, czyli ciągiem o trzech członach,
a polszczyzna czyta to zdanie także drugim sposobem,
w którym lekarz i nauczyciel są tymi samymi sąsiadami.
Jest to jednoznaczność z braku produkcji,
czyli to, czemu zapobiega
[reguła o obu czytaniach wszędzie](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
tyle że tam brakująca pozycja zostawiała zdanie odrzucone, a tu przyjęte,
więc po werdykcie nie widać jej wcale.
Ruchem jest produkcja apozycji, czyli człon, przecinek i drugi człon
w tym samym przypadku, i cena jest widoczna przed pomiarem:
przecinek jest już znakiem koordynacji na czterech poziomach
([`docs/subset.md`](docs/subset.md#what-the-grammar-covers)),
więc apozycja dokłada czytanie każdemu ciągowi rozdzielonemu przecinkiem.
Apozycję z przecinkiem niesie 217 zdań Składnicy z 13035 mających drzewo wzorcowe
(`python3 -m harness.kształty`), i jest to największy zakup w tej sekcji.
Apozycja bez przecinka wychodzi z tego przebiegu osobno, w 1274 zdaniach,
bo jest konstrukcją inną i stoi już wśród zawyżeń
[pomiaru wieloznaczności](docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
jako `podpis CERTYFIKAT`; ten wpis mówi o pierwszej z tych dwóch liczb.
Kształtem żadnej z nich nie policzyć, i tu wpis się mylił.
Monografia Świgry mówi, że apozycji nie rozdziela od koordynacji etykieta
(Woliński 2019, p. 2.8.2, wyliczony w [`docs/swigra.md`](docs/swigra.md#sources)),
a wynika z tego tylko tyle, że nie rozdziela jej kategoria:
rozdziela ją nazwa reguły, którą bank drzew niesie przy każdym rozwinięciu.
Węzeł nominalny o dwóch nominalnych dzieciach jest w tym banku przydawką
dopełniaczową w 6580 zdaniach, przy 217 apozycji z przecinkiem,
więc liczba wzięta kształtem mówiłaby o przydawce, którą olski ma,
a nie o konstrukcji, której nie ma.
Zostaje sama cena: ile czytań apozycja dokłada zdaniom, w których ciąg
rozdzielony przecinkiem już się wyprowadza.

`Co innego jest tanie.` wychodzi `valid` z `Co innego` w roli okolicznika,
czyli czytaniem, którego polszczyzna nie ma,
bo Morfeusz daje formie `co` czytanie przyimka rządzącego dopełniaczem.
Przydawka za tym zaimkiem tego napisu nie odzyskała i odzyskać nie mogła
([`docs/subset.md`](docs/subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)):
`innego` jest dopełniaczem, więc zgadza się z `co` w dopełniaczu,
a rola, w której ta grupa stoi, żąda mianownika.
Ruchem jest wykluczenie po stronie słownika, czyli ta sama droga,
którą `admissible` w `olski/segmentacja.py` odbiera czytania spoza polszczyzny
([`docs/subset.md`](docs/subset.md#the-dictionary-offers-readings-polish-does-not)),
a nie kolejna produkcja.
Słownictwem projektu tego nie zrobić, choć obie jego sekcje sięgają do słownika:
`pomijane` odbiera lematowi czytania wszystkie (`olski/słownictwo.py`),
a ten rejestr pyta przez `co` zdanie po zdaniu,
więc naprawa jest kryterium na czytanie, a nie deklaracją na lemat.
Do rozstrzygnięcia jest, czy kryterium ma stać na parze `co` z przymiotnikiem,
czy na samym czytaniu przyimkowym tej formy:
`co godzinę` i `co dzień` są w polszczyźnie właśnie tym przyimkiem,
więc wykluczenie szersze zabiera zwyczajne zdania,
a wąskie jest listą, która rośnie o każdy przymiotnik.
Do przeczytania jest przedtem, ile zdań na tym czytaniu stoi:
bez tej liczby wpis jest samą ceną.
Pyta o to przebieg werdyktów, a nie bank drzew ani kolejka blokerów —
zdanie się wyprowadza, więc żadna z nich go nie pokazuje —
czyli sonda zdejmująca formie `co` czytanie przyimkowe
i licząca, którym zdaniom werdykt się przez to zmienia.

Zdanie względne bez poprzednika stoi tylko w roli podmiotu, więc `Bezokolicznik ma
dwa kształty, czyli to, kto wykonuje to, o czym mówi pozycja podrzędna.` pada, a
`Kto wchodzi w środek, poprzedniego zdania nie przeczytał.` wyprowadza się
([`docs/subset.md`](docs/subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Ruchem jest drugie ciało dopełnienia obok tego podmiotu, i cena jest widoczna
przed pomiarem: pytanie zależne stoi w tej samej pozycji ramy, więc każde zdanie
z `kto` za czasownikiem dostanie drugie czytanie — pytanie i zdanie względne bez
poprzednika są tam jednym napisem.
Do przeczytania jest, ile takich zdań ma bank drzew: bez tej liczby wpis jest samą
ceną, a kształt do policzenia daje `FreeRelativeClause` w `olski/subset.py`.

Zaimek pytajny stoi tylko na czele swojego zdania, więc drugie pytanie w tym samym
zdaniu nie ma pozycji: `Kto jest kim?` pada, a `Czym jest parser?` wyprowadza się
([`docs/subset.md`](docs/subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Pozycję na miejscu odbiera zaimkowi wykluczenie z pozycji rzeczownej, a czoło jest
w zdaniu jedno, bo tyle wysuwa polszczyzna.
Ruchem jest pozycja zaimka pytajnego w roli wypełnionej na miejscu, czyli cecha
rozdzielająca zaimek stojący w pytaniu od tego, który stoi w zdaniu oznajmującym:
bez niej `Parser zapisuje co.` wyprowadza się, a polszczyzną nie jest.
Do przeczytania jest `BEZ_CZOŁA` w `olski/subset.py`, bo tą cechą gramatyka
rozdziela dziś rolę wypełnioną czołem od wypełnionej na miejscu, i pytanie jest o to,
czy druga wartość wystarczy, czy trzeba trzeciej.
Wpis ma zdanie banku drzew, które ten brak odrzuca:
`Kiedyś zapytałem kierowcę naszego gazika, kim właściwie jest mój przewodnik?`
pada pod żywą morfologią, bo `co` nie bierze poprzednika rzeczownikowego
([`docs/subset.md`](docs/subset.md#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie)),
a pytanie zależne z orzecznikiem za przecinkiem jest jedyną rzeczą,
której temu zdaniu brakuje.

Przytoczenie samego wyrazu funkcyjnego nie ma czytania, bo `kto` i `co` nie stoją
w pozycji rzeczownej: `nikt, kto, nic, coś i ktoś mają u Morfeusza czytanie
jedno` pada, a ten sam ciąg bez `kto` w środku wyprowadza się
([`docs/subset.md`](docs/subset.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).
Ruchem jest albo cudzysłów w tym zdaniu `docs/subset.md`, czyli poprawka w prozie,
albo licencja dla wyrazu przytoczonego backtickami, czyli ta sama robota, którą
trzyma wpis o angielskiej nazwie pisanej małą literą; drugie rozstrzyga o obu.

Ciąg rozdzielny przymiotników nie ma ciała przecinkowego, więc `Warstwy trzecia,
czwarta i piąta pracują.` jest odrzucone, a `Warstwy trzecia i czwarta pracują.`
wyprowadza się
([`docs/subset.md`](docs/subset.md#przydawka-koordynuje-się-i-rozdziela-rzeczownik-tylko-za-nim)),
choć polszczyzna trzeci człon pisze właśnie przecinkiem.
Ruchem byłoby czwarte ciało tej rodziny, a pomiar przed nim mówi, żeby go nie pisać:
zakup jest zerowy.
Ani jedno zdanie Składnicy nie stawia między przydawkami samego przecinka
(`python3 -m harness.kształty`), a dziesięć, które stawia go w tej pozycji,
stawia go razem ze spójnikiem — `dynamiczne, ale dostosowane`,
`tak prawicowej, jak i lewicowej` — czyli w kształcie, którego to ciało nie daje.
Wpis zamyka więc albo skasowanie, albo ciało na przecinek ze spójnikiem —
a takie ciało wpuszcza konstrukcję inną niż ta z pierwszego zdania wpisu,
bo ciąg rozdzielny dzieli rzeczownik między człony, a `dynamiczne, ale
dostosowane` mówi obie rzeczy o jednym.
Zdanie `Warstwy trzecia, czwarta i piąta pracują.` zostaje przez to odrzucone
z ceną, której nikt nie zapłacił, bo rejestr banku drzew go nie pisze;
czy pisze je rejestr docelowy, mówi przebieg nad prozą tego repozytorium,
a nie ten nad Składnicą.
Zdanie tego kształtu stoi w [`docs/architecture.md`](docs/architecture.md),
a autor odmówił tam zapłaty, bo wersja przechodząca żąda liczby pojedynczej
od trzech warstw naraz.

Człon bez czasownika stoi tylko na końcu zdania składowego, a wtrącony w środek pada
([`docs/subset.md`](docs/subset.md#what-it-does-not-cover-yet)).
Pozycja w środku zdania jest tą samą pozycją, której żąda para myślników,
więc oba wpisy zamyka jedna sesja, a nie dwie:
wtrącenie w środku wylicza rozwinięcie szyku, a nie osobne ciało na każdy znak.
Do przeczytania jest, ile czytań ta pozycja dokłada zdaniu, które ten człon stawia
na końcu, bo tam da się go przyłączyć do zdania składowego i do zdania nad nim.

Spójnik skorelowany nie zaczyna się za podmiotem:
`Werdykt ani nie wnosi, ani nie zdejmuje.` pada,
gdzie `Ani werdykt nie wnosi, ani nie zdejmuje.` wyprowadza się
([`docs/subset.md`](docs/subset.md#spójnik-skorelowany-powtarza-się-przed-każdym-członem)).
Dwa ciała, które weszły, spinają zdania składowe i grupy imienne,
a w tym napisie ciąg zaczyna się za podmiotem, czyli spina same orzeczenia,
a takiej pozycji koordynacja olskiego nie ma na żadnym poziomie.
Zdanie to nazywa ten brak na liście w
[`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md#czego-brakuje-najbardziej).
Ruchem jest ciało spinające orzeczenia, a nie kolejny lemat ani kolejny poziom,
i cena jest widoczna przed pomiarem: orzeczenie niesie ramę czasownika,
więc ciąg musiałby powiedzieć, którą ramę wypuszcza w górę,
a dwa czasowniki o różnych ramach dzielą wtedy jedno wypełnienie.
Do przeczytania jest `Complements` w `olski/subset.py` obok
[`docs/subset.md`](docs/subset.md#nothing-above-a-coordination-distributes-into-it),
bo zasięg koordynacji rozstrzyga się tam, gdzie stoi to, co człon zawiera.

Wolny celownik nie ma u olskiego pozycji żadnej:
`Kompilator wyprowadza psa agentowi.` pada, `Kompilator wyprowadza psa.` przechodzi,
a pierwsze jest polszczyzną
([`docs/subset.md`](docs/subset.md#wolny-celownik-nie-jest-pozycją-ramy-i-nie-wchodzi-leksykonem)).
Leksykonem tego nie wpuścić, bo Walenty wypisuje pozycje żądane,
a ten celownik dochodzi do orzeczenia dowolnego czasownika,
więc ruchem jest pozycja okolicznika obok wyrażenia przyimkowego i przysłówka.
Cena jest widoczna przed pomiarem i jest wysoka:
okolicznik dochodzi do zdania i do grupy imiennej, a forma celownika żeńskiego
jest zarazem miejscownikiem, więc każde `w gramatyce` dostaje drugie czytanie.
Ceny tej zakup nie równoważy.
Celownik pod pozycją luźną, czyli ten, którego schemat czasownika nie żąda,
niesie w Składnicy 10 zdań z rzeczownikiem i 54 z zaimkiem,
na 13035 mających drzewo wzorcowe (`python3 -m harness.kształty`).
Pozycji, którą wpis proponuje, żąda pierwsza z tych liczb, a nie ich suma:
zaimek zwrotny olski ma już terminalem
([`docs/subset.md`](docs/subset.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym)),
a `Rozbiłaś mi samochód!` żąda zaimka osobowego, nie grupy imiennej.
Rozdzielić te dwie liczby trzeba przy tym lematem, a nie klasą głowy,
którą bank drzew przy frazie wypisuje: `siebie` liczy on do klasy rzeczownika,
więc podział po samej klasie stawia każde `sobie` po stronie rzeczownikowej
i zawyża tam wiersz kilkakrotnie.
Zostaje `harness/konwersy.py`, bo tamto kryterium łapie ten celownik dziś jako
pomyłkę i mówi, ile go w Walentym widać z drugiej strony.

Liczebnik za rzeczownikiem nie ma pozycji, a zasłania to czytanie rzeczownikowe.
`po którym zostaje czytań kilka` wychodzi przyjęte,
bo Morfeusz zna `kilka` także rzeczownikiem,
a grupa liczebnikowa stawia liczebnik przed rzeczownikiem
([`docs/subset.md`](docs/subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)),
czyli brak zasłania tam czytanie, którego polszczyzna nie ma
([`docs/subset.md`](docs/subset.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)).
Kolejka blokerów tego nie pokazuje, bo zdanie się wyprowadza,
więc podnosi ten brak czytanie werdyktów, a nie przebieg.
Czego się po ruchu spodziewać, mówi zaimek zwrotny, czyli ten sam brak wpuszczony
([`docs/subset.md`](docs/subset.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym)):
pozycja dopisana zabiera zdaniu jednoznaczność i zabiera mu zarazem werdykt
nieprawdziwy, a wybór między tymi dwiema liczbami rozstrzyga kierunek
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).

Szyk `Będzie trzeba zmierzyć cenę.` nie ma ciała, a wywód i zdanie odrzucone stoją
w [`docs/subset.md`](docs/subset.md#forma-bedzie-składa-czas-przyszły-także-z-predykatywem).
Ruchem jest drugie ciało tej samej pary produkcji wraz z pomiarem,
bo cena każdego ciała jest osobną liczbą.
Do przeczytania jest przedtem, czy ten szyk nie daje drugiego czytania zdaniu,
które dziś wychodzi jednoznaczne:
`bedzie` orzeka też samo
([`docs/subset.md`](docs/subset.md#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony)),
a predykatyw za nim stanąłby wtedy tam, gdzie stoi orzecznik.

Okolicznik narzędnikowy nie ma pozycji przed zdaniem, a polszczyzna go tam stawia:
`Wieczorem wziął lustro.` pada, `Wziął lustro wieczorem.` przechodzi,
i pierwszy szyk wypisuje tor składu, więc obieg na nim nie zamyka się
(`tests/test_rozbiór.py`).
Ciało zmierzono i odrzucono, bo grupa wysunięta jest wtedy jedyną grupą przed
czasownikiem, tak samo jak w szyku od czasownika i w zdaniu o opuszczonym podmiocie
([`docs/subset.md`](docs/subset.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Ruchem nie jest więc ani samo ciało, ani znacznik na grupie:
czytania rozdziela przypadek, a nie kształt, i formy, o które idzie,
mają mianownik obok narzędnika, więc żądanie musiałoby mówić o przypadku jedynym,
a unifikacja przecina zbiory i tego powiedzieć nie umie.
Dwa obejścia, które ta gramatyka ma poza `unify`, tu nie sięgają:
oba pytają o formę — jedno odmawia lematowi, drugie formie bez cechy —
a żadne nie pyta, ile wartości ta cecha niesie
([`docs/design-notes.md`](docs/design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)).
Do przeczytania jest ta sekcja wraz z wpisem o wolnym celowniku:
tamten stoi na tej samej przeszkodzie, bo forma celownika żeńskiego
jest zarazem miejscownikiem, więc rozstrzygnięcie zapada dla obu naraz.

Liczebnik rządzący nie orzeka: `Torów jest dwa.` pada,
a `Tory są dwa.` przechodzi zgodnym
([`docs/subset.md`](docs/subset.md#liczebnik-orzeka-o-tym-ile-czegoś-jest)).
Podmiot stoi tam w dopełniaczu, a orzeczenie nie zgadza się z niczym,
więc ciało jest osobne i osobna jest jego cena, której nikt nie policzył.
Do przeczytania jest, czy nie zderzy się ono z czasownikiem nieosobowym:
tamten też orzeka bez zgodności z podmiotem
([`docs/subset.md`](docs/subset.md#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu)).

Słowa pytające `jak`, `jaki`, `ile` i `dlaczego` nie mają pozycji,
a zdania z nimi nie padają, tylko przechodzą czytaniem, którego polszczyzna nie ma:
`Pyta, ile ta gramatyka kosztuje.` wychodzi przyjęte z `ile` w okoliczniku
przysłówkowym, bo Morfeusz daje tym słowom `adv`, a `jaki` część mowy
przymiotnikową, i olski bierze te części mowy całe.
Ruch ma przez to dwie połowy i pierwsza jest zawężeniem:
czytanie okolicznikowe ma zejść, zanim wejdzie czoło, które je zastąpi
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).
Do przeczytania jest wpis o okoliczniku przysłówkowym biorącym całą część mowy,
bo wylicza on formy, które ten rejestr pisze inaczej, i te cztery słowa
są jego dalszym ciągiem.

Zaimek zwrotny nie ma pozycji orzecznika narzędnikowego,
a wywód stoi w [`docs/subset.md`](docs/subset.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym).
Ruchem jest jedno ciało wraz z pomiarem nad bankiem drzew,
bo proza tego repozytorium tej konstrukcji nie pisze.
Wpis ten jest zablokowany rzeczownikiem `soba`, o który pyta wpis w sekcji
o gramatyce i pomiarze: dopóki ten lemat bierze `sobą`, pomiar tej pozycji
liczy zamianę jednego czytania na dwa, a nie zakup.

## Skład i opowieści

`README.py` powstał drzewami przed tekstem, czyli odwrotnie, niż deklaruje
`opowieści/__init__.py`, więc mierzy, co skład powiedzieć umie, a nie co trzeba.
Ruchem jest napisać najpierw polski tekst oddający wstęp `README.md`,
potem drzewa pod niego, a różnicę między jednym a drugim przeczytać,
bo dopiero ona mówi, czego tym kategoriom brakuje.
Wtedy ten napis dostaje właściciela i wchodzi do testu tak,
jak `BAZYLISZEK` stoi w `tests/test_opowieść.py`;
dziś nie trzyma go nic i `README.py` mówi w nagłówku, dlaczego.
Kryterium wyjścia toru składu to i tak nie jest
([`docs/roadmap.md`](docs/roadmap.md#kryterium-wyjścia-toru-składu-to-znów-readme)),
bo tamto żąda znak w znak nad `README.md`, a nie treści oddanej innymi zdaniami.

Trzy pozycje, których skład nie ma, stoją każda w innym miejscu;
dwie pierwsze widać w `README.py`.
Lematu `olski` Morfeusz nie zna wcale, więc nazwa własna tego języka
nie stanie w składanym zdaniu w żadnej roli:
`olski/skład/leksemy.py` wybiera między leksemami, które SGJP ma,
i sam mówi, że leksem nieznany nie ma ani jednej formy.
Odmianę tego słowa deklaruje `olski.toml`, a skład go nie czyta,
i tym zajmuje się wpis o leksykonie projektu czytanym przez oba kierunki,
a nie ta pozycja.
Liczebnika nie ma `olski/skład/składnia.py`, więc `jedno odczytanie` z drzewa nie wyjdzie,
i jest to ta sama konstrukcja, którą gramatyka po drugiej stronie już ma
([`docs/subset.md`](docs/subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)),
czyli tor składu jest tu za nią, a nie przed.
Relacja `przyczyna` nie ma w `olski/skład/przyimki.py` wpisu pod żadnym przyimkiem,
a ma wpis w `olski/skład/spójniki.py`, więc wychodzi zdaniem i nie wychodzi frazą:
`Dlaczego.bo(zdarzenie)` składa się, a `Dlaczego.dla(rzecz)` zgłasza `PozaRamą`.
Jest to jedyna z tych trzech pozycji, przy której skład ma pół konstrukcji, a nie zero.
Do przeczytania przy niej jest ten leksykon obok
`tests/test_przyimki.py`, który świadkuje przypadkom, a nie doborowi relacji.

Komunikat werdyktu jest napisem wpisanym w kod, a repozytorium ma tor,
który polskie zdanie składa z drzewa,
więc werdykt mógłby być pierwszym konsumentem tego toru:
formę po liczebniku liczyłaby wtedy morfologia,
a nie tabela na trzy przedziały w `_odczytań` w `olski/werdykt.py`.
Wpis stoi zaparkowany za wpisem o pozycjach, których skład nie ma,
bo liczebnik jest jedną z nich,
a bez liczebnika nie wyjdzie z drzewa ani jeden wiersz tego werdyktu.
Liczebnik nie jest przy tym wszystkim, czego temu komunikatowi brakuje.
Wiersz werdyktu cytuje formę wziętą ze sprawdzanego zdania,
a drzewo składu nie ma pozycji na napis, którego się nie odmienia.
Skład zgłasza przy tym `BrakFormy` oraz `PozaRamą` nad drzewem,
którego nie umie zrealizować, a werdykt wypisuje się nad każdym zdaniem,
więc komunikat z drzewa dokłada gałąź na wypadek, którego napis nie ma.
Do przeczytania jest `explain` w `olski/werdykt.py`,
bo część jego wierszy jest polskim zdaniem, a część listą par i liczbą,
czyli rozstrzygnąć trzeba i to, ile z tego wydruku skład bierze.

Słowo, którego SGJP nie ma, mówi gramatyka i nie mówi go skład.
`olski.toml` deklaruje leksem, wedle którego takie słowo się odmienia
([`docs/subset.md`](docs/subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)),
a `olski/skład/morfologia.py` pyta o formy sam Morfeusz i tego pliku nie czyta,
więc `README.py` dalej nie wypuści zdania o olskim.
Ruchem jest `odmień` pytające o ten leksykon tam, gdzie słownik milczy,
bo `odmiana` w `olski/projekt.py` wydaje dokładnie to, co `paradygmat`
w tamtym pliku: formę wraz z cechami i leksemem.
Do przeczytania są przy tym dwa odsiewy, których leksykon projektu nie ma:
`POZA_REJESTREM` odsiewa kwalifikatorem, a wpis kwalifikatorów nie niesie,
choć wzorzec bywa nimi oznaczony,
i `WieleLeksemów`, bo wiersz wskazuje leksem wprost, czyli odpowiada już na to pytanie.
Rozstrzygnąć trzeba przy tym, czy skład bierze stąd same formy,
czy pyta jeszcze wzorzec o kwalifikatory, których wpis nie niesie.

Skład nie ma czym powiedzieć, co jest tematem wewnątrz grupy imiennej,
więc `Jaki` w `olski/skład/składnia.py` zawsze stawia przymiotnik przed rzeczownikiem,
choć polszczyzna ma oba szyki i różnią się one tym, co niosą:
przymiotnik po rzeczowniku nazywa, a przed nim określa.
Widać to bez żadnego pomiaru, na jednej frazie:
README pisze `kontrolowanych języków naturalnych`,
a to samo drzewo wypuszcza `kontrolowany naturalny język`.
Po drugiej stronie stoi to jako czytanie, które z
[obiegu](docs/sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma)
nie wraca żadnym drzewem, i trzyma to `tests/test_rozbiór.py`.
Do przeczytania jest ta para wraz z tym,
co [`docs/sklad.md`](docs/sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
mówi o tym, czego drzewo nie niesie.
Ruchem jest ta sama kategoria, którą zdanie już ma, wpuszczona do grupy imiennej:
`Wyróżnienie` stoi w `olski/skład/składnia.py` i przestawia konstytuenty zdania,
a wewnątrz grupy nie sięga niczego, bo `Cechy` w `olski/skład/słownik.py`
zwija przymiotniki, zanim spotkają rzeczownik.
Rozstrzygnięcia żąda przy tym co innego niż w zdaniu:
tam wyróżnienie przestawia to, co i tak stało osobno,
a tu przymiotnik postawiony po rzeczowniku zmienia znaczenie całej grupy,
więc nazwa `temat` na to nie przystaje.

Opowieść stawia jeden czas we wszystkich swoich orzeczeniach,
a polszczyzna liczy czas zdania podrzędnego wobec zdania nad nim,
więc `Wiedział, że pod ścianą stały postaci.` wychodzi tam,
gdzie polszczyzna napisałaby `stoją`.
Oba te zdania są polskie i mówią co innego,
czyli brakuje tu kategorii dziedziny, a nie formy do policzenia:
pyta ona o to, czy rzecz z dołu trwała wtedy, czy skończyła się przedtem.
Widać to dopiero od [treści](docs/sklad.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi),
bo okoliczność wyrażona zdarzeniem stoi obok zdarzenia nadrzędnego w czasie,
a treść stoi pod nim, i tam czas przestaje być własnością samego opowiadania.
Do przeczytania jest `CZASY` oraz `Kontekst` w `olski/skład/składnia.py`
wraz z tym, co [`docs/sklad.md`](docs/sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)
mówi o czasie jako własności tekstu,
bo ta kategoria tego zdania nie odwołuje, tylko dokłada do niego drugie:
czas opowiadania zostaje, a zdanie podrzędne dostaje go względem swojego zdania.
Ruchem jest ta kategoria przy `Treść`,
wraz z rozstrzygnięciem, czy jest ona tym samym co aspekt, czy czym innym,
bo `stoją` i `stały` różnią się tu czasem, a nie dokonaniem.
Do zmierzenia jest, ile zdań tej legendy wyszłoby wtedy inaczej,
a jest ich dziś dwa i oba stoją pod `Treść`.

Anafora sięga podmiotu i nic poza nim,
a opowieść o bazyliszku pokazuje, gdzie to boli:
`opowieści/bazyliszek.py` pisze `wzrok potwora` dwa razy,
a polszczyzna napisałaby drugi raz `jego wzrok`.
Tak samo dopełnienie: po `Bazyliszek zobaczył własne odbicie.`
legenda pisze `zamienił bazyliszka w kamień`,
a polszczyzna napisałaby `zamienił go`.
Ruchem jest zaimek osobowy w miejscu roli innej niż podmiot,
liczony z tego samego `Kontekst`.
Do przeczytania jest to, co o tej pozycji mówi
[pole generowania](docs/similar-work.md#generowanie-rozdziela-się-poziomem-wejścia),
bo ruch ten ma tam nazwę wraz z literaturą,
a warunek, który dziedziczy, jest testem na zbiór dystraktorów,
czyli tym, co tamten algorytm liczy nad opisem rzeczy.
Do przeczytania jest też `pomijalny` w `olski/skład/składnia.py`,
który trzyma warunki [wąskiego opuszczania podmiotu](docs/sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie),
bo zaimek dziedziczy stamtąd warunek, a nie tylko mechanizm,
wraz z [ceną tego ruchu](docs/sklad.md#lepszy-tekst-żąda-czego-innego-niż-dłuższy),
która trzyma cztery rzeczy czyniące go innym, niż wygląda:
ostrzejszy warunek na zaimek, szyk łączący go w jedną zmianę z
[dopełnieniem wyrażonym zdarzeniem](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
osobne miejsce zaimka dzierżawczego,
oraz podmiot zdania podrzędnego, który zaimka nie bierze wcale i stoi niżej.
Do zmierzenia jest, czy pozycja zwalnia się w tej legendzie gdziekolwiek,
a do rozstrzygnięcia, czy `swój` i `jego` są jedną kategorią, czy dwiema,
bo pierwszy odsyła do podmiotu zdania, a drugi poza nie.

Osobno stoi podmiot zdania podrzędnego, bo polszczyzna nie pisze tam zaimka,
tylko go opuszcza, a `Kontekst.podrzędne` opuszczenie w dół nie przekazuje.
Odbiera to legendzie zdanie, którego ona chce:
`Czeladnik znał córkę krawca. Nie wiedział, że stała pod ścianą.`
mówi, że on nie wiedział o niej, a nie o sobie, i mówi to samą formą,
a wersja z wypisanym podmiotem powtarza `córkę krawca` w zdaniu obok.
Pozycja jest tam wolna wedle warunku, który już stoi:
`wiedzieć` rozdziela czeladnika od córki rodzajem, i `stać` rozdziela ich tak samo,
więc oba opuszczenia mierzy dziś `pomijalny` i oba przechodzą.
Brakuje zasięgu: dziś antecedensem jest podmiot zdania poprzedniego,
a tu jest nim jego dopełnienie.
Do rozstrzygnięcia jest, czy zasięg obejmuje też okoliczność wyrażoną zdarzeniem,
i stoi za tym argument, którego treść nie ma:
zdanie z `gdy` wysunięte na czoło stoi przed swoim antecedensem,
więc opuszczenie w nim odsyłałoby wstecz do niczego,
a treść stoi za zdaniem nadrzędnym zawsze.
Do przeczytania jest `Kontekst.podrzędne` wraz z powodem,
dla którego każde pole gaśnie tam osobno,
bo ten ruch jednemu z nich ten powód odbiera.
Ruchem jest antecedens liczony z uczestników zdania poprzedniego i nadrzędnego,
a nie z samych ich podmiotów, wraz z testem na parę zdań,
w której rodzaj tych dwóch ról jest wspólny, bo tam opuszczenie ma się nie stać.

Rama czasownika, o którą pyta `Robi` w `olski/skład/składnia.py`,
odpowiada na trzy pytania z listy: o biernik, o bezokolicznik i o zdanie podrzędne,
więc rola w przypadku innym nie ma po tej stronie o co zapytać
i nie ma jak stanąć w drzewie.
Kosztuje to trzy klasy zdań, a wszystkich trzech chciała druga wersja legendy,
trzecia poprosiła o dwie z nich znowu i wszystkie trzy z niej wypadły.
`Czeladnik nie powiedział nikomu.` żąda celownika,
`Czeladnik szukał córki krawca.` żąda dopełniacza,
i oba przypadki leksykon dziś wymienia,
bo wpuściła je gramatyka podzbioru
([`docs/subset.md`](docs/subset.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu));
`Robi` o żaden z nich nie pyta i przez to odrzuca oba zdania.
`Córka krawca nie wierzyła w bazyliszka.` żąda wyrażenia przyimkowego,
którego czasownik wymaga, a nie takiego, które autor dokłada jako okoliczność,
i ta klasa jest gorsza niż brak, bo `Dokąd.w` wypuści to zdanie jako cel,
czyli powie, że ktoś w coś wierzy tak, jak mówi się, że ktoś dokądś idzie.
Czwarta wersja legendy obeszła to zdanie z drugiej strony,
bo `nie wierzyła, że w piwnicy mieszkał bazyliszek` bierze
[treść](docs/sklad.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi)
zamiast wyrażenia przyimkowego, a mówi to samo o postaci;
klasa zostaje jednak w tej samej cenie, bo wiara w rzecz zdaniem podrzędnym nie wyjdzie.
Czwarty koszt jest cichy i przez to najgorszy z nich:
`chcieć` ma u Walentego i dopełniacz, i przypadek strukturalny,
więc przechodzi tu przez pytanie o biernik i wypuszcza `Kot chce mysz.`,
czyli zdanie, którego polszczyzna woli nie mówić, a nikt tego nie zgłasza.
Jedna pozycja znaczy tu więc nie tylko odmowę tam, gdzie brakuje przypadka,
ale i wybór najgorszej z ram, które lemat ma.
Piątą klasę dokłada losowanie: `czekał na izbach` wychodzi z drzewa,
w którym `na izbach` jest okolicznością miejsca,
a czyta się przez `czekać na kogoś`, czyli przez ramę, której tu nie ma,
więc `olski/skład/makieta.py` ten czasownik pomija, zamiast wypuszczać takie zdania.
Po stronie leksykonu ta zmiana jest zrobiona:
plik niesie zdanie o celowniku i zdanie o dopełniaczu,
a czyta je sama gramatyka podzbioru
([`docs/subset.md`](docs/subset.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)),
więc zostaje strona składu i to ona jest tym wpisem.
Zdanie podrzędne dopisane po bezokoliczniku przesądziło ten wpis,
bo pokazało, ile z tej zmiany jest zrobione, a ile nie:
przekład umie wziąć trzecie zdanie, plik umie je unieść, a `Robi` umie o nie zapytać,
i mimo to każde nowe pytanie jest osobną gałęzią w konstruktorze,
a `_dopełnienie` obok rozdziela dziś trzy kształty tam, gdzie rozdzielało dwa.
Ta sama gałąź powtarza się po drugiej stronie obiegu,
bo tam każda z tych trzech pozycji jest osobnym symbolem gramatyki:
`_dopełnienia` w `olski/skład/rozbiór.py` rozdziela je tak samo
i pójdzie tą samą zmianą.
Ruchem jest rama jako zbiór pozycji, a nie lista pytań,
oraz `zdarzenie` w tym samym pliku rozdzielające argumenty po tym zbiorze,
a nie po kategorii okoliczności.

Treść bierze jeden spójnik i przez to jedną z dwóch rzeczy, które ta pozycja mówi.
`że` orzeka, że tak jest, a `żeby` — że tak ma być,
więc `Czeladnik chciał, żeby córka krawca wróciła.` z tego drzewa nie wyjdzie,
choć jest to zdanie, którym polszczyzna mówi o cudzym zdarzeniu pod czyjąś wolą.
Stoi to obok odmowy, którą `Robi` wydaje bezokolicznikowi o cudzym wykonawcy,
i te dwie rzeczy są jedną dziurą widzianą z dwóch stron:
[`docs/sklad.md`](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie)
nazywa tamto zdanie polskim, którego bezokolicznik nie wyraża,
a wyraża je dokładnie ta pozycja i ten drugi spójnik.
Do przeczytania jest `cp(żeby)` obok `cp(że)` u Walentego,
bo słownik te dwa kształty rozdziela i mówi, który lemat bierze który,
oraz `Treść` w `olski/skład/składnia.py`, gdzie spójnik stoi stałą.
Ruchem jest kategoria dziedziny na to, czy treść jest orzekana, czy żądana,
wraz z osobnym zdaniem leksykonu o `cp(żeby)`; wpis jest przez to winien
przebieg `harness/walenty.py` oraz poprawkę liczb w
[`docs/subset.md`](docs/subset.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on).

`Przysłówek` w `olski/skład/składnia.py` żąda od słownika formy przysłówkowej,
a część okoliczności polszczyzna wyraża partykułą:
`znowu` ma w SGJP sam `part`, więc `D.znowu` zgłasza `BrakFormy`.
To zdanie legenda o bazyliszku chciała postawić w zakończeniu,
gdzie miasto zabija wejście drugi raz, i postawiła je bez tego słowa.
Do przeczytania jest wyjście `paradygmat` dla `znowu`, `tam` i `wkrótce`,
bo `tam` niesie oba znakowania naraz i pokazuje,
że granica między nimi nie idzie po tym, czym słowo jest w zdaniu.
Ruchem jest rozstrzygnięcie, czy okoliczność wyrażona jednym słowem
jest jedną kategorią dziedziny niezależnie od tego, czym słownik to słowo znakuje,
bo jeśli jest, to `Przysłówek` pyta o część mowy tam,
gdzie od części mowy nie zależy ani szyk, ani zgodność, ani forma.

`przejrzyj` w `olski/skład/przegląd.py` zgłasza jedną klasę z dwóch,
bo przyłączenia zawęzić nie ma dziś czym.
Okolicznik dochodzi w drzewie do zdarzenia zawsze,
więc każde wyrażenie przyimkowe stojące za grupą imienną byłoby trafieniem,
a raport zgłaszający każde zdanie z przyimkiem nie oddziela niczego od niczego:
nad `opowieści/bazyliszek.py` trafiłby w trzynaście z dwudziestu jeden zdań,
bo tyle z nich niesie wyrażenie przyimkowe,
i żadne z tych zgłoszeń nie mówiłoby autorowi, co miałby z nim zrobić.
Do przeczytania jest, czym się różnią te miejsca,
oraz to, co [`docs/subset.md`](docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia)
mierzy nad Składnicą, bo tam ta sama klasa jest policzona nad cudzymi drzewami.
Stoi nad tym wpisem pytanie
[`docs/open-questions.md`](docs/open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma),
które pyta o to samo od strony parsera i mówi, że wyjścia nie ma w gramatyce.
Przegląd stoi wobec niego inaczej i to jest tu jedyna nadzieja:
on niczego nie odrzuca, więc pomyłka kosztuje tu wiersz raportu,
a nie zdanie, którego autor nie napisze.
Ruchem jest kryterium, które oddziela przyłączenie niosące różnicę znaczenia
od tego, przy którym oba czytania mówią to samo,
albo rozstrzygnięcie, że takiego kryterium nie ma
i że ta klasa do przeglądu nie wchodzi.

Stopnia nie ma w składzie żadnego, a jest on kategorią dziedziny.
`Jaki` w `olski/skład/składnia.py` żąda od przymiotnika stopnia równego na stałe,
`Przysłówek` obok żąda tego samego i mówi w docstringu,
że stopień wyższy „mówi co innego” i czeka na kategorię.
Bez niego nie da się powiedzieć `Koszt szynki jest wyższy niż koszt bułki.`,
czyli tego zdania, które mówi to samo co `Koszt szynki przewyższa koszt bułki.`
i mówi to bez kolizji, którą `olski/skład/przegląd.py` w drugim zgłasza.
Do przeczytania jest, czy porównanie jest kategorią osobną od cechy,
bo `wyższy` jest formą przymiotnika, a `niż koszt bułki` jest drugim uczestnikiem,
więc drzewo ma tu do postawienia relację, a nie stopień przy rzeczy.
Ruchem jest ta kategoria wraz z linearyzacją stawiającą `niż`,
a nie przełącznik wybierający między dwoma zdaniami za autora:
przegląd zgłasza, żeby autor napisał drugie drzewo,
a nie żeby kompilator podmienił mu pierwsze.

`Jest` w `olski/skład/składnia.py` umie jedną kopulę, a gramatyka bierze pięć.
`Jan zostaje nauczycielem.` wyprowadza się w olskim i stoi w `PRZYJMOWANE`
w `tests/test_subset.py`, a ze składu nie wyjdzie,
bo lemat kopuli stoi w tym konstruktorze jako stała, a nie jako pole drzewa.
Widać to dopiero od zmiany, po której rama czasownika przychodzi z leksykonu:
`KOPULA` w `olski/lematy.py` jest tą częścią walencji, której Walenty nie niesie,
i [`docs/subset.md`](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)
nazywa ją jedynym wpisem leksykonu pisanym ręcznie,
a stoi ona w gramatyce, a nie w `olski/walencja.py`, czyli tam, gdzie leksykon.
Do przeczytania jest ta sekcja wraz z wpisem o narzędniku,
bo ten sam przekład rozstrzyga, czy kopula w ogóle zostaje listą.
Ruchem jest `KOPULA` przeniesiona do `olski/walencja.py`
oraz `Jest` biorące lemat tak, jak bierze go `Robi`,
wraz z odmową dla czasownika, którego ta lista nie wymienia.
Czyta ją stamtąd także `harness/polszczyzna.py`, więc import idzie razem z nią.

`odmień` w `olski/skład/morfologia.py` bierze pierwszą z form jednego leksemu,
gdy żądaniu odpowiada ich kilka, i nie mówi o tym nigdzie.
Jest to jedyne miejsce, w którym kompilator wybiera w milczeniu,
i zostaje po dwóch kryteriach, na które ta klasa nie sięga:
kwalifikatora ta forma nie ma, a leksem ma ten sam, co forma obok niej.
Widać ją w dwóch postaciach, a przyczyna jest jedna, więc idą razem.
Pierwszą jest wariant w jednej komórce: `postaci` obok `postacie`
w mianowniku mnogim, i pierwszy z nich wypisuje `opowieści/bazyliszek.py`,
bo pierwszy z nich wydaje słownik.
Drugą jest rodzaj wypisany dwiema wartościami w jednym tagu,
z których `rodzaj_rzeczownika` w tym samym pliku bierze alfabetycznie pierwszą:
`anioł` dostaje stąd rodzaj osobowy, choć słownik nie rozstrzyga, czy jest osobowy,
a rodzaj jest tu wartością, z której liczy się zgodność całego zdania.
Do przeczytania jest to, co
[`docs/sklad.md`](docs/sklad.md#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)
mówi o kryterium, które zostało zbudowane obok tej klasy,
bo pytanie jest tu tym samym pytaniem o jedno piętro niżej:
wybór między leksemami zapada w nazwie, a ten zapada pod jednym leksemem.
Ruchem jest rozstrzygnięcie, czym ten wybór ma być, i kandydatów jest dwóch.
Zgłoszenie jak `WieleLeksemów` żąda od autora wpisu przy każdym wariancie,
także tam, gdzie oba warianty znaczą to samo, czyli przy `oczami` obok `oczyma`.
Wpis wskazujący formę, jak `olski/skład/leksemy.py` wskazuje leksem,
kosztuje wpis tylko tam, gdzie ktoś na wariant trafi,
a milczy dokładnie tak jak dziś, dopóki nikt go nie napisze.
Rozstrzyga między nimi to, ile takich wariantów rejestr naprawdę spotyka,
i tego nikt nie policzył.

`olski/skład/przyimki.py` zna przyimek w jednej postaci,
więc `we Wrocławiu`, `ze wsi` i `pode mną` z drzewa nie wyjdą,
a wyjdzie z niego `w Wrocławiu`, którego polszczyzna nie ma.
Danych do tego nie brakuje: Morfeusz znakuje obie postaci cechą `vocalicity`,
a `olski/morph.py` tę cechę czyta, więc `we` stoi w słowniku obok `w`.
Brakuje warunku, kiedy postać zgłoskotwórcza jest tą właściwą,
a jest to warunek fonologiczny nad tym, co po przyimku stoi,
czyli jedyna rzecz w tym pakiecie, której nie da się wziąć z lematu ani z pozycji.
Do przeczytania jest wyjście `paradygmat` dla `w`, `z` i `pod`
wraz z tym, co `docs/prior-art.md` mówi o tym, czego ten słownik nie niesie.
Ruchem jest ten warunek zapisany raz, w linearyzacji okolicznika,
wraz z rozstrzygnięciem, czy wpis leksykonu wymienia obie postaci,
czy jedną, a drugą liczy się z niej.

Leksem dokładany do napisu, który słownik zna, stoi poza `olski.toml`
i jest drugą połową klasy, którą ten plik obsługuje; czym się te dwie różnią,
trzyma [`docs/subset.md`](docs/subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma).
Wiersz na taki leksem — na `agent`, żeby projekt pisał o agentach `agenty` —
dokłada czytanie formie, którą słownik już czyta,
więc łamie własność, na której stoi zerowa cena tej warstwy,
a cena takiego wiersza jest przez to ceną zwykłą,
mierzoną w czytaniach zdań przyjętych.
Ruchem jest ten pomiar, a nie wiersz dopisany bez niego,
i tym różni się ta połowa od tamtej: tam cena wychodziła z własności,
a tu wychodzi z przebiegu.
Do przeczytania jest `test_żadnej_formy_leksykonu_słownik_nie_zna`
w `tests/test_projekt.py`, bo wiersz na `agent` wywraca właśnie ten test,
i rozstrzygnąć trzeba, czy test ten zostaje z wyjątkiem wypisanym obok,
czy schodzi razem z własnością.

O bezokolicznik gramatyka nie pyta wcale, a skład pyta o niego leksykon,
i te dwa zdania nie zgadzają się co do `pomagać`.
`Linter pomaga pisać dobry kod.` stoi w komentarzu `olski/subset.py`
jako przykład ciał produkcji `Complements`, olski je wyprowadza,
a `Robi` w `olski/skład/składnia.py` odmawia mu ramy,
bo `olski/leksykon.txt` mówi o tym lemacie samo `nie_bierze_biernika`.
Widać to na obiegu i nigdzie więcej, bo osobno każdy z tych kierunków
ma tylko własne zdanie i nie ma go z czym porównać;
tym różni się ten wpis od tych, które nazywają brak po jednej stronie.
Wywód trzyma
[`docs/sklad.md`](docs/sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma),
a odmowę jako powód sprawdza `tests/test_rozbiór.py`.
Do przeczytania jest, co `harness/walenty.py` bierze z Walentego przy pozycji `infp`,
bo pytanie jest o to, czy słownik tego lematu z bezokolicznikiem nie ma,
czy ma go w kształcie, którego ten przekład nie bierze,
wraz z tym, co [`docs/subset.md`](docs/subset.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)
mówi o granicach tego przekładu.
Ruchem jest jedno z dwóch, zależnie od tego, co słownik powie:
przekład biorący ten kształt, wraz z przebiegiem generatora
i poprawką liczb w tamtej sekcji,
albo zdanie przykładowe w tamtym komentarzu zamienione na takie,
które oba tory mają naraz.

Liczebnik ma produkcję w gramatyce, a w tym zapisie nie ma kategorii,
więc `Działają dwie rzeczy.` wraca powodem
`„dwie rzeczy” nie ma tu czym być w pozycji Subject`,
i tą samą drogą przepada każde zdanie z liczbą.
Do przeczytania jest `_nominalne` w `olski/skład/rozbiór.py`,
czyli lista ciał grupy imiennej, które ten kierunek mówi,
wraz z ceną liczebnika, którą trzyma commit, który go wpuścił,
bo tamta strona ma go zmierzonego od strony gramatyki.
Ruchem jest kategoria w `olski/skład/składnia.py`, a nie samo ciało w rozbiorze:
liczebnik rządzi liczbą i przypadkiem rzeczownika, którego dotyczy,
więc bez niej nie ma z czego wypisać tego, co ma wrócić.

Wybór między `w` i `na` jest faktem o rzeczowniku, a tego faktu nie ma tu nigdzie:
`olski/skład/przyimki.py` mówi, jakiego przypadka żąda przyimek w danej relacji,
i o tym, przed którym rzeczownikiem on stanie, nie mówi nic,
więc `w ulicy` oraz `na izbie` wychodzą z drzewa tak samo dobrze jak `na ulicy`.
Widać to dopiero od strony tekstu, którego nikt nie pisał zdanie po zdaniu:
autor pisze `na rynku`, nie zauważając, że wybrał,
a `olski/skład/makieta.py` wybrać musi i dlatego rozdziela `MIEJSCA_W` od `MIEJSCA_NA`,
czyli trzyma fakt o polszczyźnie w tabeli jednego programu.
Do przeczytania jest ta para tabel wraz z tym, co
[`docs/sklad.md`](docs/sklad.md#tekst-losowany-żąda-tego-czego-autor-nie-musiał-napisać)
wylicza jako fakty poza leksykonami tego pakietu,
oraz `PRZYIMKI` w `olski/skład/przyimki.py`, bo pytanie jest o kolumnę, której ten plik nie ma.
Ruchem jest ta kolumna, czyli przyimek dopisany przy rzeczowniku, a nie przy relacji,
wraz z rozstrzygnięciem, czy milczenie takiego leksykonu odmawia, jak przy przyimkach,
czy przepuszcza, jak przy ramie domyślnej czasownika;
świadka w słowniku ta wiedza nie ma, bo SGJP kolokacji nie znakuje.
Świadkiem nie jest przy tym kolumna przyimków w `olski/leksykon.txt`, choć wygląda
na niego: mówi ona, jakiego przyimka żąda rama rzeczownika — `informacja o czymś` —
a nie, którym przyimkiem mówi się o rzeczy, że coś jest przy niej.

Aspekt bezokolicznika nie jest sprawdzany, a czasownik nad nim go wybiera:
`zacząć` żąda niedokonanego, więc `Czeladnik zaczął zapłakać.`
przechodzi przez pytanie o ramę, które stawia `Robi` w `olski/skład/składnia.py`,
i wychodzi zdaniem, którego polszczyzna nie ma.
Rama jest tu sprawdzona co do pozycji i niesprawdzona co do formy,
która tę pozycję wypełnia, i jest to ta sama luka, którą ma
[dopełnienie wyrażone zdarzeniem](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
tylko o piętro niżej: tam leksykon mówi, czy bezokolicznik wolno postawić,
a tutaj nie mówi, który.
Kosztuje to dziś czasownik w tabeli `olski/skład/makieta.py`,
która `zacząć` i `przestać` pomija, żeby losowanie takiego zdania nie wypuściło.
Do przeczytania jest to, co `harness/walenty.py` bierze z Walentego,
bo słownik ten aspekt przy pozycji `infp` wypisuje,
oraz `bierze_bezokolicznik_podmiotu` w `olski/walencja.py`,
czyli zdanie, które to pytanie zadaje.
Ruchem jest czwarta kolumna leksykonu wraz z żądaniem postawionym `odmień`,
albo rozstrzygnięcie, że aspekt jest wyborem lematu i że wybiera go autor,
a wtedy ruchem jest zdanie o tym w docstringu `Robi`.

`przejrzyj` w `olski/skład/przegląd.py` uczestnika bezokolicznika z niczym nie zestawia,
więc `Zegar chciał wynieść klucz.` nie zgłasza się,
choć jest to ta sama klasa co `Koszt szynki przewyższa koszt bułki.`,
od którego ten moduł powstał:
oba rzeczowniki brzmią w mianowniku i w bierniku tak samo,
forma przeszła `chciał` rodzaju tych dwóch nie rozdziela,
i polszczyzna czyta ten ciąg zarówno jako SVO, jak i jako OVS.
Zamykają go dwa miejsca naraz:
`_zdania_pod` w `olski/skład/składnia.py` wypuszcza treść i okoliczność wyrażoną zdarzeniem,
a zdania postawionego jako dopełnienie nie wypuszcza,
i `Robi.uczestnicy` obok niego bezokolicznika za uczestnika nie liczy.
Ruchem jest uczestnik bezokolicznika zestawiony z podmiotem czasownika nad nim,
a nie ze swoim, bo bezokolicznik podmiotu nie ma;
para przechodzi więc przez piętro, czego żadna dzisiejsza para nie robi.
Do przeczytania jest to, co
[`docs/sklad.md`](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie)
mówi o tym, że podmiot w takim zdaniu nie staje nigdy,
oraz [postawa przeglądu](docs/sklad.md#drzewo-jest-jednoznaczne-a-napis-z-niego-nie-musi-być),
która o tym pomiarze mówi, że liczy się go z form, które w tekście stanęły.
Zażąda to od `_rozróżnia` czasownika z innego zdania niż uczestnik,
bo trzeci warunek pyta o formę, którą rola z czasownika wyciąga,
a bezokolicznik nie wydaje żadnej i obu rolom oddałby tę samą;
formą, która te dwie rozdziela, jest `chciał` ze zdania nadrzędnego.
Dzisiaj obie strony tego porównania biorą się z jednego zdania i tylko stamtąd.

`Jest` w `olski/skład/składnia.py` nie ma pozycji na okoliczność,
choć `Robi` obok ma ich tyle, ile autor postawi,
więc `Kot jest zwierzęciem w piwnicy.` nie wyjdzie ze składu,
a olski to zdanie czyta i czyta je dwojako.
Kosztuje to każde zdanie, które o czymś orzeka i mówi, gdzie albo kiedy,
czyli klasę, której README nie żąda, a opowieść żądałaby jej w pierwszym akapicie.
Do przeczytania jest `linearyzuj` w obu tych klasach,
bo różnią się one o tę jedną pętlę, i
[okoliczność](docs/sklad.md#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie),
która trzyma wywód o tym, że okoliczność dochodzi do zdarzenia.
Ruchem jest to samo pole na obu, wraz z rozstrzygnięciem,
czy okoliczność przy orzeczeniu imiennym mówi o byciu czymś,
czy o rzeczy, która czymś jest, bo `w piwnicy` przy `Kot jest zwierzęciem.`
czyta się i tak, i tak, a drzewo ma powiedzieć jedno.

`abstrahuj` w `olski/skład/rozbiór.py` nie ma pozycji na `LinkedPredicate`,
więc `Flaga to kawałek tkaniny.` wraca brakiem kategorii,
choć gramatyka to zdanie wyprowadza
([`docs/subset.md`](docs/subset.md#łącznik-to-orzeka-bez-czasownika-a-podmiot-stoi-za-nim)).
Rola stoi w `DEKLARACJA` w `olski/subset.py` i nie stoi w `POZYCJE`,
czyli jest to ta usterka, którą komentarz nad `POZYCJE` opisuje.
Samo dopisanie pozycji nie kupuje jednak nic i dlatego wpis jest jeden, a nie dwa:
kandydat odpada wtedy na linearyzacji, bo `Jest` wypisuje kopulę,
więc pierwsze rozstrzygnięcie jest o tym, czy łącznik niesie coś ponad nią.
Niesie — wtedy jest kategorią dziedziny obok `Wyróżnienie`,
a `Flaga to kawałek tkaniny.` i `Flaga jest kawałkiem tkaniny.` znaczą co innego.
Nie niesie — wtedy zdejmuje go `znaczenie` tak samo jak znacznik tematu,
linearyzacja przestaje być funkcją,
a niezmiennik obiegu żąda przynależności po obu stronach
([`docs/design-notes.md`](docs/design-notes.md#the-round-trip-invariant)).
Pomiar nad Składnicą daje do tego rozkład obu konstrukcji, a nie samo rozstrzygnięcie,
bo to jest osąd o polszczyźnie.

## Pakiet, instalacja i testy

`witryna/skrypt.js` jest jedynym plikiem w repozytorium, którego nic nie uruchamia.
Suita pyta o niego z zewnątrz jedno — czy strona woła trasy, które serwer ma
(`tests/test_witryna.py`) — a samego skryptu nie wykonuje,
bo w [bloku checków](CLAUDE.md#checks) nie ma node'a
i dopisanie go tam kosztuje drugie środowisko w workflowie.
Decyzja robi się potrzebna wtedy, gdy skrypt zacznie cokolwiek liczyć;
dziś rysuje dane, a po stronie Pythona jest prawie wszystko, co może być nie tak —
poza tekstem, który przycisk kopiuje do schowka
([`docs/witryna.md`](docs/witryna.md#ramy-nie-ma-bo-warstwa-http-jest-tablicą-tras)).
Ruchy są dwa i różnią się tym, co przyjmują za granicę:
albo node wchodzi do checków wraz z jednym testem strony w przeglądarce bezgłowej,
albo skrypt zostaje bez testu, a regułą staje się to,
że logika nie schodzi do przeglądarki.
Przeczytaj przed decyzją `tests/test_wydruki.py`,
bo pokazuje on, ile pilnowania da się zrobić bez drugiego środowiska.

The repository ships no licence.
`pyproject.toml` carries no `license` field and there is no `LICENSE` file,
so the terms under which any of this may be used are unstated.
The move is to pick one, add the file,
and set `license` in `pyproject.toml` to match.
Reading a GPL v3 parser of Polish is what raised it
(see [`docs/swigra.md`](docs/swigra.md#why-wrapping-it-does-not-get-there)),
and the answer decides whether olski could ever link against such a thing.

`tests/test_subset.py` ma po podziale przeszło trzy tysiące wierszy
i pyta obok podzbioru o dwa moduły niżej.
Sekcja pierwsza, pod banerem „Unification, which is where agreement lives”,
sprawdza unifikację i sprawdzenia formalizmu z `olski/grammar.py`,
las i liczbę czytań z `olski/parse.py`,
oraz to, co werdykt wypisuje o rolach, gospodarzach i konstytuentach,
czyli `explain` z `olski/werdykt.py` nad rozbieżnościami z `olski/parse.py`.
Ruchem jest przeniesienie tych grup do plików nazwanych po tamtych modułach,
tak jak swoje dostały segmentacja i werdykt,
a nazwa pliku o rozbiorze musi być inna niż `tests/test_rozbiór.py`,
bo ten pyta o pakiet składu.
Granica jest tu całą decyzją i oczywista nie jest:
test o wydruku werdyktu pyta naraz o dwie warstwy,
więc rozcięty na dwa pliki zostawia w każdym połowę zdania.
Do przeczytania jest ta sekcja od góry pliku
do banera o zdaniach przyjmowanych.

`ruff format` nie stoi w [bloku checków](CLAUDE.md#checks),
a nad kilkunastoma plikami z dziewięćdziesięciu ma zdanie inne niż to,
co w nich stoi: wypisuje je `ruff format --check .`,
a `--diff` pokazuje, że różnica jest w miejscach łamania wiersza, nie w kodzie.
Wyborem to nie jest, bo [reguła o łamaniu](CLAUDE.md#semantic-line-breaks)
oddaje kod zwykłemu narzędziu języka, a tym narzędziem jest tutaj ten formater.
Płaci za to ten, kto puści go na pliku, który akurat poprawia:
diff obejmuje wtedy wiersze, których nie tknął.
Ruchem jest jedno z dwojga — `ruff format --check .` dopisany do bloku checków
i do workflowu wraz z jednym przebiegiem po całym drzewie,
albo zdanie w `CLAUDE.md`, że formatera tu nie używamy,
a `ruff check` jest całym sprawdzeniem kodu.
Do przeczytania jest `ruff format --diff olski/parse.py`,
bo mówi, co ten przebieg zrobiłby z adnotacją typu rozbitą ręką na trzy wiersze.
