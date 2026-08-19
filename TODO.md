# Work to do in the repository

The running list of work inside the repository itself:
rewrites, merges, documents that have drifted apart,
dangling references, gaps, and code worth improving.
Something noticed while working on another topic goes here
instead of stretching the current change or being forgotten.
[The review pass](CLAUDE.md#the-review-pass) is the other way in:
a refactor too large to do on the spot is written down rather than started,
and the review also checks whether a change deleted the entries it closes.
Read the list before starting new work,
because it names the problems somebody has already found.

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
The package has the same collision and the same argument settles it.
`olski-corpus` runs `olski/coverage.py`,
where `olski/corpus.py` is the treebank reader beside it,
so the command, the module and the document
are three names for what a reader takes to be one thing.
Renaming the document alone leaves the module and the command as they are,
which is why they are one entry:
what has to be decided is what these things are called,
and the answer for the document is the answer for the other two.
The entry about the harness boundary reaches the third of them on its own grounds,
since one of the two answers it offers moves the treebank reader to `harness/`
and takes the command along as `python3 -m harness.coverage`,
which leaves nothing there to rename,
so whichever entry is picked up first is answering for the other.

`docs/subset.md` jest dokumentem mieszanym.
Polskie sekcje dopisano tam do angielskiego dokumentu,
a [reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
przewiduje dla takiego pliku przekład całości, osobną zmianą.
Ruchem jest przekład reszty, jednym commitem,
bo dopóki go nie ma, każde nowe zdanie w angielskiej sekcji idzie po angielsku,
co ta reguła mówi wprost.
Wpis ważył więcej, dopóki lista plików była zasięgiem checka;
checka nie ma, więc został sam przekład.

`docs/open-questions.md` trzyma listę decyzji zamkniętych,
a każda z nich ma właściciela gdzie indziej.
Sekcja `Settled` powtarza to, co jest budowane, wraz z kierunkiem toru
([`docs/roadmap.md`](docs/roadmap.md#tor-gramatyczny-nie-ma-końca)),
wycofanie toru linterowego ([`docs/linter.md`](docs/linter.md#what-closed-the-track)),
bliskość polszczyzny
([`docs/design-notes.md`](docs/design-notes.md#decisions-taken)),
i słownik morfologiczny,
czyli tę jedną decyzję, przy której `docs/design-notes.md` pisze wprost,
że nie jest zapisana dwa razy.
Ruchem jest usunięcie sekcji na rzecz zdania mówiącego, gdzie decyzje zapadłe stoją,
czyli [zakaz znaczników zrobionego](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
zastosowany do listy otwartych pytań.
Przeciw: lista zamkniętych rozwidleń oszczędza komuś otwierania ich z powrotem.
Do przeczytania jest więc, czy któraś pozycja niesie odrzuconą alternatywę,
której jej właściciel nie trzyma — taka zostaje, a reszta idzie.

Lista dokumentów w README miesza dwa tory, które sekcja nad nią rozdziela.
[`Co działa`](README.md#co-działa) mówi, że działają dwie rzeczy,
a lista pod nią biegnie bez podziału i rośnie z każdym dokumentem,
więc czytelnik toru gramatycznego i czytelnik toru składu
przechodzą przez cudze pozycje, zanim dojdą do swoich.
Ruchem jest pogrupowanie listy — tor gramatyczny, tor składu,
to, co obsługuje oba, i zapis toru wycofanego — bez ruszania linków,
czyli najtańsza zmiana, jaką ta lista przyjmie.
Przeciw katalogom w `docs/`: przepisałyby każdy link względny po to,
żeby dać indeks, którym ta lista już jest.
Do rozstrzygnięcia jest, gdzie idą pozycje graniczne,
bo [`docs/roles.md`](docs/roles.md), [`docs/roadmap.md`](docs/roadmap.md)
i [`docs/open-questions.md`](docs/open-questions.md) obsługują oba tory.
Etykiety grup nie ruszą `test_every_document_is_listed_in_the_readme`,
który czyta pozycje wzorcem `^- [docs/…]` i nie patrzy, co stoi między nimi.

`docs/firing-rates.md` wyprowadza drugi raz to, co należy do
[listy korpusu audytowego](docs/audit-corpus.md#the-list):
dlaczego `rit-dokumentacja` traci na ekstrakcji tyle, ile traci,
czyli że jej tabele API stoją bez wiodących kresek
i że takie tabele są większością jej dokumentów.
Przyczyna stoi w obu miejscach w pełnej precyzji,
a jeden właściciel rozumowania żąda tam zdania ze wskaźnikiem.
Wniosek, po który `firing-rates.md` po nią sięga, zostaje:
różnica formatu jest większością tego, czym trafienia niżej nie są.
Wpis waży mniej, odkąd tamten dokument jest zapisem, którego nic nie rusza:
zostaje z niego czytelnik trafiający na to samo wyprowadzenie dwa razy,
a nie dwie kopie, które się rozjadą.

`docs/prose-linters.md` mówi o wycofanym pakiecie w czasie teraźniejszym.
Przeglądowi cudzych silników w tym dokumencie nic nie brakuje,
ale własne odniesienia wskazują kod, którego nie ma:
otwarcie pisze „what olski is trying to build",
`Vale is the architecture to study` liczy pięć reguł w `CHECKS`,
a `proselint measured what everyone else asserts` mówi, że pola `justification`
i `sources` deklaracji reguły żądają tego samego, co standard proselinta.
W kodzie nie ma żadnej deklaracji reguły, więc nie ma i tych pól,
a `CHECKS` nie występuje w żadnym `.py`.
Do przeczytania jest, jak mówią o sobie dwa pozostałe dokumenty tego toru:
[`docs/linter.md`](docs/linter.md#what-closed-the-track) pisze
„What follows is the design as it stood",
a [`docs/firing-rates.md`](docs/firing-rates.md) nazywa pakiet wycofanym
w drugim akapicie i mówi tam też, że żadnego przebiegu z niego nie da się powtórzyć.
Ruchem jest albo takie zdanie w otwarciu tego dokumentu,
albo czas przeszły przy każdym własnym odniesieniu osobno.
Za drugim ruchem przemawia to, że zdanie w otwarciu zamroziłoby także
przegląd cudzych silników, którego wycofanie toru nie dotyczy
i po który ktoś do tego dokumentu wraca.
Pozycja tego dokumentu na liście w README jest już w czasie przeszłym,
więc rozstrzygnięcie dotyczy samego dokumentu, a nie tamtej listy.

Liczby wzięte nad własnym README stoją w dwóch dokumentach w pełnej precyzji,
a właściciela mają: figury `readme` i `sonda-readme` wymieniają `README.md`
wśród ruszających, więc przeredagowanie czyni je należnymi przeliczenia
i `python3 -m harness.figury` mówi to temu, kto przeredagowuje.
Zostaje zejść z pełnej precyzji tym czterem:
mianownikowi i dwóm zgodnościom w
[`docs/design-notes.md`](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)
oraz licznikowi klasy zdań w
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop),
bo jedno przeredagowanie rusza te cztery liczby naraz,
a przeliczenie poprawia wtedy cztery zdania zamiast wskazać plik.
Do przeczytania są oba te akapity: pierwszy z nich opiera się na zdaniu,
którego README nie ma — o czym mówi wpis o `Cenie trzeciej` w sekcji o komendach —
więc samo przeliczenie go nie naprawia.

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

Wydruk `olski-check` jest po angielsku,
a [reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
obejmuje komunikaty, które drukuje narzędzie.
Nieprzełożone są tam dwie rzeczy naraz:
komunikaty z `explain` w `olski/subset.py`
i nazwy symboli, które ten sam wiersz wypisuje jako role czytania.
Ruchem jest przekład jednym commitem,
bo nazwa sięga wszystkich swoich wystąpień, a wydruk stoi w dokumentach.
Słownik symboli przekłada się przy tym w całości albo wcale,
bo nazwa dopisana po polsku daje mieszaninę wewnątrz słownika.
Do przeczytania są bloki werdyktu cytowane w README, `docs/subset.md`
i `docs/design-notes.md`: przekład bierze je na nowo ręką,
i to one, a nie liczba nazw, mówią, ile ta zmiana kosztuje.

## Komendy i sondy

Dwie sondy czytają Walentego i pytają go o różne schematy, a różnicy nie zmierzył nikt.
`sonda/rama.py` odsiewa kwalifikatory `archaiczny` i `zły` przez `BRANE`,
bo schemat tak oznaczony nie należy do rejestru, o który olskiemu chodzi,
a `sonda/konwersy.py` bierze wszystkie schematy lematu i o kwalifikator nie pyta wcale.
Jedna z dwóch odpowiedzi jest gorsza i nie wiadomo która:
liczba konwersów jest górnym oszacowaniem, które i tak myli się w jedną stronę
([`docs/disambiguation.md`](docs/disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma)),
więc schemat archaiczny mógł ją podnieść, a mógł nie trafić w kryterium pary.
Ruchem jest przebieg `sonda/konwersy.py` z tym odsiewem i bez niego,
a potem albo `BRANE` wspólne dla obu sond, albo zapisany powód, czemu jedna go nie chce.
Do przeczytania jest `_pewność` w `sonda/rama.py` oraz dwanaście par,
które tamta sonda wypisuje: jeżeli odsiew rusza liczbę, to rusza i te pary,
a wtedy należy się ich przeczytanie, a nie sama poprawiona liczba.

Sonda różnicowa nad prozą bierze jeden plik, a rejestr ustaw to siedem plików.
`main` w `sonda/ruch.py` rozgałęzia się na katalog, który czyta jako Składnicę,
i na plik, który czyta jako prozę, więc siedmiu aktów nie ma jak podać:
figury nad tym rejestrem trzeba wziąć po zlepieniu ich w jeden plik,
i to zlepienie jest krokiem, którego dokument nie ma jak wydrukować obok liczby,
a [`docs/ustawy.md`](docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
cytuje ruch każdej konstrukcji nad tym rejestrem osobno.
Ruchem jest wiele ścieżek prozy w jednym przebiegu, złożonych jednym raportem,
czyli to, co `przebieg` już robi nad lasami banku drzew:
`nad_prozą` bierze napis, a nie ścieżkę, więc scalanie jest w tym pliku gotowe.
Do rozstrzygnięcia zostaje, co robi ścieżka katalogu z prozą w środku:
Składnica też jest katalogiem, a rozpoznawanie po rozszerzeniu plików w środku
byłoby trzecim znaczeniem jednego argumentu.

`olski` chodził po katalogu, a `olski-check` bierze tylko pliki.
Widać to w poleceniu, którym
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów: stoi przed nim `find`, bo inaczej nie ma czego podać.
Komenda, która po katalogu chodziła, wyszła razem z torem lintera,
a chodzenia po drzewie nie ma teraz żadna z dwóch, które zostały:
`main` w `olski/check.py` i `main` w `olski/wieloznaczność.py`
czytają po prostu każdą podaną ścieżkę, więc obu rozwija się je powłoką.
Ruchem jest jedno miejsce, które schodzi po `rglob`,
bierze pliki o rozszerzeniu, które ekstrakcja pisze,
pomija katalog o nazwie zaczynającej się kropką — bo korpus stoi w repozytorium,
a jego kontrola wersji korpusem nie jest — i woła się z obu komend,
po czym `find` z tamtego polecenia znika,
a razem z nim powłoka z czterech figur w [`harness/figury.py`](harness/figury.py),
które biorą `sh -c` tylko po to, żeby ktoś rozwinął im glob.
Przeciw pominięciu: katalog z kropką podany wprost staje się wtedy nieosiągalny,
więc należy ono do chodzenia, a nie do testu na rozszerzenie.
Do rozstrzygnięcia jest, czy komenda mówi o plikach, które minęła:
`olski-check` ma mianownik, który tamten dokument cytuje,
więc pominięcie w ciszy zmienia figurę, o której nikt się nie dowie.

`olski-check` daje dokumentowi liczbę, której nie sprawdza żaden test.
Samą komendę woła `tests/test_rozstrzyganie.py` — `main` z listą argumentów
i wydruk czytany przez `capsys`, czyli tym wzorem, o który ten wpis prosił —
ale pyta ją wyłącznie o wiersz warstwy rozstrzygającej
i o sąsiedztwo, które ta warstwa dostaje po zdaniu.
Niesprawdzone zostają trzy kody wyjścia
(2 bez argumentów i nad ścieżką, której nie da się przeczytać,
1 wtedy, gdy nie każde zdanie przeszło)
oraz podsumowanie, w którym fragmenty liczą się obok zdań.
Podsumowanie jest tym, po co dokument tę komendę woła:
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów nad korpusem audytowym z ostatniego wiersza wydruku,
więc figura w dokumencie opiera się na formacie, którego nic nie pilnuje.
Testem nie jest wydruk przepisany wiersz po wierszu:
kosztuje przy każdej zmianie układu
i nie broni niczego, czego by czytelnik nie zobaczył.
Warte pisania są właśnie te dwie rzeczy: podsumowanie, bo cytuje je dokument,
i kody wyjścia, bo widzi je tylko ten, kto komendę wpina w potok.

`sonda/luka.py` przepisuje z `sonda/ruch.py` cały przebieg różnicowy:
liczniki, przejścia, scalanie kawałków, tryb nad prozą, tabelę i wiersz poleceń,
czyli około stu osiemdziesięciu wierszy stojących drugi raz.
Połowa powodu, dla którego nie dało się ich wziąć stamtąd, zeszła
i wróciła w innej postaci.
Wariant bogatszy od mianownika ta maszyneria umiała, dopóki miała `Sonda.dopisuje`,
a odsiew grup działał nad dopiskiem tak samo jak nad produkcjami olskiego;
pole to wyszło razem z przysłówkiem, czyli z jedyną sondą, która je wypełniała,
bo konstrukcja wpuszczona do gramatyki mierzy się już zdejmowaniem.
Zostaje to, że warianty luki są dwiema wersjami jednego dopisku,
a nie jednym wariantem na grupę zdejmowaną osobno:
wariant ostatni nie jest wtedy „obie naraz”,
więc `pytania` i `Raport._konkurencja` — dwa wiersze o tym,
czy grupy wchodzą sobie w drogę — nad nimi nie znaczą nic.
Ruchem jest `Sonda` biorąca gramatykę wariantu wprost, funkcją zamiast grupy,
wraz z konkurencją zepchniętą do sond, które grupy zdejmują.
Do przeczytania są właśnie te dwa pola, bo to one się nie generalizują,
oraz `gramatyka` w `ruch.py`, która jest jedynym miejscem
wiążącym wariant z grupą produkcji.
Tej samej maszynerii żąda z drugiej strony wpis o figurach
`docs/corpus.md` bez polecenia:
tam wariantem jest morfologia, a nie grupa produkcji zdjęta z olskiego,
więc ten, kto podnosi którykolwiek z dwóch, wybiera kształt dla drugiego,
i jest to jedna sesja.

Klasa `verb` w `NOMINALIZATION` z `harness/endings.py`
stoi przed każdą nominalną,
co jest słuszne dla `zostanie` i niesłuszne dla `dacie`.
Oba niosą czytanie czasownikowe obok nominalnego,
a dokument datujący fakturę ma na myśli miejscownik od `data`
tam, gdzie ta kolejność wpisuje drugą osobę liczby mnogiej od `dać`,
więc udział form odmienionych cytowany w
[`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match)
jest podłogą, a nie liczbą.
Ruchem jest albo kolejność, którą rozstrzyga korpus —
czytanie nominalne przed czasownikowym tam, gdzie czasownikowe jest osobą,
której rejestr nie używa — albo podłoga wypisana tam, gdzie udział jest cytowany,
czyli w tamtej sekcji i nigdzie indziej.
Dowodem jest 7 słów: 6 razy `dacie` i raz `powiecie`,
a rejestr obu używa jako rzeczowników.
Waga wpisu spadła razem z torem, który tę sondę zamawiał:
figura, którą on prostuje, jest teraz częścią zapisu o czymś wycofanym,
a nie liczbą, na której coś stoi.

`Cena trzecia` w
[`docs/design-notes.md`](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)
opiera się na zdaniu, którego README nie ma.
Cytuje `Zbiór tekstów przechodzących przez wszystkie reguły
jest podzbiorem polszczyzny w jednym i w drugim przypadku`
i liczy je ponad sześć sekund,
a README niesie to zdanie z drugim członem,
`a wyznaczenie go przez wykluczanie jest nieporównanie tańsze`,
którego słów sonda nie przyłącza:
dziedziny przycinają się wcześnie
i cały plik kończy się najwolniejszym czasem poniżej dziesiątej części sekundy.
Sam cytat podany przez `-c` liczy się ponad osiem sekund,
więc zjawisko zostaje, a przykład z tego pliku wyszedł.
Rozjeżdża się razem z nim drugie zdanie tamtego akapitu:
mówi ono o `dokładnie jednym` zdaniu odrzuconym bez ani jednej formy spoza produkcji,
gdzie [`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop) liczy takich pięć.
Do przeczytania jest ten akapit obok `python3 -m sonda proza/README.txt`
i tego samego zdania podanego przez `-c`.
Ruchem jest albo zdanie, które README naprawdę ma i które ten czas pokazuje,
albo powiedzenie tej ceny bez zdania z tego pliku.
Liczby w tamtym akapicie zostały nieprzeliczone razem z resztą,
bo przeliczenie jednej z nich w wywodzie bez dowodu czyta się jak uzgodnienie.
Widać to teraz po samej sekcji: mówi ona wyżej o 48 zdaniach prozy README,
a ten akapit o pozostałych 42, i różnicy nie tłumaczy w niej nic.
Wpisu o figurach nad własną prozą to nie zamyka:
tamten pyta, czy mianownik w ogóle zapisywać.

`sonda/konwersy.py` liczy lematy, a pytanie pod nią jest o zdania.
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
`sonda/powtórzenie.py` i `sonda/wybory.py` pytają obie o `pytania` z
`olski/wieloznaczność.py` i obie wypisują odpowiedź wraz ze zdaniem, nad którym
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
`sonda/` właśnie dlatego, a program czytający ten plik jest najtańszą rzeczą w tej parze.

`CZASOWNIK` znaczy w trzech miejscach trzy rzeczy i jeden plik importuje dwie.
`olski/attachment.py` nazywa tak zbiór części mowy, `olski/rozstrzyganie.py` stronę
wyboru (`"clause"`), a `sonda/polszczyzna.py` wzorzec `fin|impt|inf`.
Nazwę drugą wzięto stamtąd, gdzie pierwsza już stała: komentarz przy niej mówi
„tak jak nazywa je `olski/attachment.py`”, a tamten plik ma pod tą nazwą co innego.
`olski/wieloznaczność.py` potrzebuje obu naraz, więc importuje jedną pod
`STRONA_CZASOWNIKOWA` i tłumaczy to komentarzem, czyli płaci za kolizję,
której nie zrobił.
Ruchem jest nazwa dla strony wyboru mówiąca, że jest stroną — `STRONA_IMIENNA`
i `STRONA_CZASOWNIKOWA` w miejsce `RZECZOWNIK` i `CZASOWNIK` — bo zbiór części mowy
pod tą nazwą stoi w dwóch plikach, a strona w jednym.
Czytelników strony jest sześciu i wszyscy są nazwani z imienia:
`strona`, `wypadki`, `zbuduj`, `oceń` i `Skłonność.wybierz` w tamtym module
oraz `sonda/wskazania.py`.
`olski/skłonności.txt` zmiana nie rusza, bo wartości `noun` i `clause` zostają
te same; przemianowana jest nazwa stałej, a nie napis, który ona trzyma.

`sonda/ruch.py` pomija zbędne rozbiory nad bankiem drzew, a nad prozą nie.
`_warianty` rozbiera zdanie olskim i odrzuceniem zamyka pozostałe warianty,
bo ich czytania są podzbiorem czytań olskiego,
a `nad_prozą` obok woła `check` raz na wariant,
więc segmentuje ten sam tekst i rozbiera to samo zdanie tyle razy, ile wariantów.
Kosztuje to sekundy, czyli mało,
ale dwie funkcje jednego pliku odpowiadają na to samo pytanie inaczej,
i nic w nich nie mówi, że jedna z tych odpowiedzi jest przeoczeniem.
Ruchem jest funkcja w `olski/subset.py` biorąca zdanie już zsegmentowane,
przez którą idą i `check`, i `nad_prozą`,
bo segmenty zależą od napisu, a nie od gramatyki.
Do przeczytania jest `check`: liczy jeszcze `bez_licencji` i całą `DEKLARACJA`,
których `nad_prozą` nie czyta ani razu,
więc razem z tym ruchem rozstrzyga się, czy wspólna funkcja liczy je zawsze.

Dziewięć sond różnicowych rozbiera nad Składnicą tę samą gramatykę olskiego.
Wariant `czysty` jest w każdej z nich dokładnie olskim,
a `_warianty` rozbiera nim każde zdanie jako pierwsze,
więc rozbiór trzynastu tysięcy zdań powtarza się dziewięć razy,
raz na proces, który `harness.figury` uruchamia po kolei.
Ruchem jest przebieg czytający bank drzew raz i puszczający sondy razem,
z rozbiorem olskiego liczonym raz na zdanie.
Ceną jest to, na czym stoi `harness/figury.py`:
figura deklaruje polecenie słowo po słowie, a jej plik to polecenie zapisuje,
więc figura wzięta przebiegiem zbiorczym traci polecenie,
którym da się ją powtórzyć osobno.
Rozstrzygnąć trzeba więc najpierw, czy deklaracja umie nazwać jedno i drugie,
a nie jak scalić przebiegi.
Wpis o czterech przebiegach budujących nad Składnicą te same lasy
pyta o to samo od strony pomiaru i podnosi się razem z tym.

## Korpusy, ekstrakcja i figury

Osiemnaście figur ma deklarację w `harness/figury.py` i nie ma pliku,
bo pierwszego przebiegu nie zrobił nikt: `python3 -m harness.figury` wypisuje je
pod odpowiedzią `bez pliku` wraz z tym, czego każda z nich wymaga.
Podnosi je ten, kto ma korpus albo prozę z niego wyjętą, po jednej,
a każda kosztuje dwie rzeczy: sam przebieg
oraz prozę, z której po nim schodzi pełna precyzja, nagłówek z cyfrą włącznie.
Drugie jest droższe, bo akapit wylicza dziś liczby jedną z drugiej
(„cząstka kupuje 99, obie 148, czyli przypadek dokłada 49”),
a restytucja mówi to stosunkiem, więc jest przepisaniem zdania, a nie podmianą liczby.
Wzorcem jest negacja: deklaracja, wydruk w `figury/`,
a w [`docs/subset.md`](docs/subset.md#negacja-zmierzona-kupuje-przeszło-sto-zdań-i-nie-płaci-dopełniaczem)
restytucja grubsza od niego i wskaźnik.
Figura, której nikt nie rusza, czeka na miejscu,
bo tekst napisany przed regułą nie jest usterką.

`python3 -m harness.endings proza` liczy, co w `proza/` stoi, a nie korpus audytowy.
Figura `końcówki` deklaruje `proza/ksef` i `proza/rit`,
bo tabele w [`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match)
są nad tymi dwoma,
a polecenie, które ta sekcja drukuje, przechodzi całe drzewo `proza/`,
więc sesja, która wyjęła wcześniej prozę z README
tak, jak każe [`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop),
dostaje z tego samego polecenia liczby nad korpusem audytowym plus README
i nic tego nie mówi w wydruku.
Ruchem jest ścieżki liczone przez sondę wziąć z argumentów zamiast z jednego drzewa,
czyli w tej sekcji i w tej figurze wymienić oba katalogi.
Do przeczytania jest `main` w `harness/endings.py`,
bo od tego zależy, czy druga ścieżka nie żąda zmiany w tym, co sonda przechodzi.

Sekcja o cenie negacji mówi o jednym zdaniu, a figura wypisuje ich osiem.
[`docs/subset.md`](docs/subset.md#cena-stoi-w-trafności-a-nie-w-liczbie-czytań)
liczy cenę tej konstrukcji trafnością i nazywa jedno zdanie czytane inaczej niż bank drzew,
a wiersz `disagrees` w `figury/negacja.txt` ma ich osiem
i tylko jedno z nich jest tym, o którym ta sekcja mówi:
dopełniaczem stojącym przed swoim czasownikiem.
Reszta to rozbieżności zasięgu, które
[`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)
liczy osobno i nazywa czym innym niż czytaniem odwróconym.
Ruchem jest zdanie mówiące, ile z tych ośmiu należy do klasy, o którą tej sekcji chodzi,
a przed nim odczyt ręczny tych ośmiu, bo `agreement` w `olski/coverage.py`
oddziela odwrócenie roli od sprzeczności zasięgu, a nie zasięg od zasięgu.
Do przeczytania jest przy tym `figury/szyk.txt`,
bo cztery zdania tej klasy zeszły z tamtej listy razem z czterema szykami
i [tamta sekcja](docs/subset.md#większość-tych-zdań-jest-naprawą-a-nie-ceną) je wypisuje.

Sekcje restytuujące potrafią zardzewieć w pliku figury i raport tego nie widzi.
`stan` w `harness/figury.py` porównuje polecenie oraz odciski, a `czyta` zapisuje
z deklaracji tylko `zapis`, więc sekcja dopisana do deklaracji zostawia w pliku
listę krótszą, a figura wychodzi z raportu jako aktualna.
Trafiło się to przy przysłówku, gdzie sekcji jest trzy, i zeszło przeliczeniem,
którego nie zamawiał żaden ruszony plik.
Ruchem jest test na tę parę, a nie `czyta` wśród rzeczy porównywanych przez `stan`:
tamto policzyłoby figurę za należną przeliczenia nad korpusem po to,
żeby przepisać jej nagłówek, choć liczby stoją.
Do przeczytania jest `nagłówek` obok `zapis`, bo czyta ono dziś polecenie
i odciski, a sekcji nie zwraca, więc test bez tego nie ma czego porównać.

Restytucji nikt nie pilnuje i wpisanie do niej pełnej precyzji z powrotem nic nie
kosztuje, choć jest to dokładnie ta usterka, przed którą właściciel figury broni.
Ruchem jest pytanie zadawane przez `harness/figury.py` sekcji z `czyta`:
liczba, która pada w niej tak samo, jak pada w pliku figury,
jest kopią właściciela, a nie restytucją grubszą od niego.
Do rozstrzygnięcia jest, ile taki test myli się na liczbach, których nie wziął
żaden przebieg — rozmiar korpusu, numer paragrafu, rok wydania —
i czy odsiew po samych cyfrach wystarczy, żeby nie liczyć słowa „jedno” za figurę.
Wart jest tyle, ile figur ma właściciela, więc rośnie z każdą konwersją.

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

Figury, które [`docs/corpus.md`](docs/corpus.md#the-measurement) bierze ręcznie,
są w większości sondami różnicowymi i nie ma ich czym puścić.
Wiersz `prep` z jedną grupą produkcji zdjętą, ten sam z drugą, trzydzieści pozycji
przyłączeniowych zdjętych naraz oraz kolumna najczęstszych form przy każdym blokerze
powstają dziś skryptem pisanym na jeden przebieg i kasowanym po nim,
a sekcja o nich wskazuje ten plik jako miejsce, gdzie stoi, co by je uwolniło.
`sonda/ruch.py` jest tym kształtem od tej strony, której brakowało:
sonda deklaruje, do której grupy należy produkcja, a przebieg, warianty i tabelę
dostaje gotowe, więc dwie pierwsze figury są predykatem i sześcioma wierszami deklaracji.
Brakuje temu przebiegowi jednej rzeczy, której te figury żądają, a przecinek i liczebnik nie:
liczy on przejścia werdyktu, a nie blokery, więc wiersz `prep` nie ma skąd wyjść.
Ruchem jest licznik blokerów na wariant w `Raport`, wzorowany na `Report.blockers`
z `olski/coverage.py`, i dwie sondy na te dwie grupy produkcji.
Nie obejmuje to jednej figury z tamtej listy: kolumna bez wykluczenia słownikowego
jest wariantem morfologii, a nie grupy produkcji, i pod ten kształt nie podchodzi.
Do rozstrzygnięcia jest przy tym, czy sonda na figurę, którą czyta jeden dokument,
zarabia na siebie, czy taniej jest wpisać kryterium obok liczby,
co [tamta sekcja](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)
robi dla trzydziestu pozycji i co pozwoliło wziąć tę liczbę drugi raz.
Przysłówek wpuszczony do gramatyki był próbą tego drugiego i wypadła ona po jego stronie:
kryterium wypisane obok liczby dało się wziąć skryptem po latach — czterdzieści cztery
produkcje przyłączeniowe policzyły się drugi raz na tę samą liczbę — a wariant opisany
luźniej („pozycje, których przyłączenie żąda”) nie dał się powtórzyć wcale
i zdanie o nim trzeba było napisać od nowa nad wariantem nazwanym wprost.
Skrypt i tak powstał na jeden przebieg i został skasowany, więc ruch wyżej stoi.

The archives these documents send a reader to fetch are pinned by URL and by nothing else.
[Składnica](docs/corpus.md#fetching-it)
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
name a release in the query string of a wiki attachment,
and Świgra is `swigra_current.zip`, which names none,
so [`docs/swigra.md`](docs/swigra.md#what-was-read-and-what-was-not)
dates it by the timestamps of the files inside instead.
[The audit corpus](docs/audit-corpus.md#the-list) pins its members to a commit
and says what a pin is for:
so that a second person fetches the same bytes.
The archives make that promise
and give a reader no way to hold anyone to it.
The move is `sha256sum` over each one,
with the digest beside the command that fetches it,
which turns a substitution upstream into a failed check
rather than a figure that quietly stops reproducing.

The corpora these documents send a reader to fetch
come from hosts that gain nothing by serving them,
once per session rather than once per person,
because a Claude Code session on the web starts from an empty container.
[The Wolne Lektury run](docs/firing-rates.md#wolne-lektury)
takes 326 files at one request each from a volunteer library,
[Składnica](docs/corpus.md#fetching-it) is 92 MB
that [the checks](CLAUDE.md#checks) make a condition of touching the grammar,
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

## Gramatyka, parser i pomiar pokrycia

Świadkowie w `olski/rozstrzyganie.py` pytają o `Przyłączenie`, czyli o obiekt składniowy,
choć warstwa powstała po to, żeby odpowiadać czymś ponad składnią
([`docs/architecture.md`](docs/architecture.md#warstwa-rozstrzygająca-wydaje-zawężenie-z-powodem-a-nie-znaczenie)).
Widać to na kopuli: powtórzenie frazy przy `być` nie dowodzi niczego o tym czasowniku,
więc `KOPULY` odbiera dowód, zamiast dać świadkowi pytanie, na które kopuła odpowiada
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Świadka pytającego o drzewo dziedziny zamiast o gospodarza zmierzono przed napisaniem
i wyszło, że nie miałby o co pytać:
warstwa znacząca tego rejestru nie dosięga,
więc pytanie padłoby nad jednym zdaniem wieloznacznym banku drzew z kilkuset
(`figury/znaczenia.txt`).
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

Terminal wypisuje zbiór wartości napisem rozdzielonym kreską —
`word("fin|impt")`, `word("interp", lemma=".|!|?")`, `KOPULA`, `SPÓJNIKI_PRZECINKOWE` —
i `word` rozcina go na krawędzi, wewnątrz zostaje `frozenset`.
Notacja jest przez to jedna dla części mowy, lematu, warunku ujemnego i żądanej cechy,
a `SPÓJNIKI_OKOLICZNIKOWE` składa dwie takie listy przez interpolację napisu,
czyli wolno jej złożyć listę, której żaden test nie sprawdzi po jednym elemencie.
Ruchem jest `word` przyjmujący krotkę albo `frozenset` obok napisu,
a wtedy jedna rzecz ma dwie pisownie obok siebie,
albo `word` przyjmujący samą krotkę, a wtedy zmiana sięga każdego terminala
w `olski/subset.py` i w sondach, które terminale pisują same
(`sonda/polszczyzna.py`, `sonda/luka.py`).
Werdyktu nie rusza ani jedno, ani drugie, więc figury po tym nie chodzą,
i dlatego ten wpis jest tu, a nie w zmianie, która o niego potrącała.
Do przeczytania jest `bierze` w `olski/grammar.py`:
lemat, warunek ujemny i żądana cecha są tam trzema osobnymi testami przed unifikacją,
więc typ wejścia rozstrzyga się dla nich razem, a nie dla każdego osobno.

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
Do przeczytania jest cena obu pozycji, które ta konstrukcja już ma
([`docs/subset.md`](docs/subset.md#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie)),
bo trzecia wraca z pytaniem tej samej postaci.
Tym samym brakiem jest okolicznik wewnątrz zdania względnego:
`Reguła, która rozstrzyga, gdy tekst jest gotowy, jest tania.` jest odrzucone,
bo obie pozycje stoją na `ClauseConjunct`,
a `RelativeCore` jest osobnym symbolem i ciała z tym symbolem w środku ma jedno.
Zdanie odrzucone jest przy tym werdyktem uczciwym, a nie czytaniem nieprawdziwym,
więc pozycja ta nie ma pilności, jaką miałby brak wydający `valid`.

Okolicznik wyrażony zdaniem dochodzi do zdania składowego, przy którym stoi,
a nie do ciągu współrzędnego, w którym to zdanie stoi,
więc `Program zapisuje ustawienia i linter sprawdza tekst, ponieważ tekst jest
gotowy.` wychodzi jednym czytaniem tam, gdzie polszczyzna ma dwa.
Jest to ta sama granica, którą trzyma zasięg koordynacji
([`docs/subset.md`](docs/subset.md#nothing-above-a-coordination-distributes-into-it)),
i ten sam kształt, jaki ma dziś okolicznik wysunięty przed zdanie,
więc jedna decyzja obejmuje oba.
Ruchem jest ciało `Clause → Clause AdverbialClause` obok tego na `ClauseConjunct`,
a przed nim odpowiedź na to, co ono wnosi:
nad zdaniem o jednym składowym oba ciała dają ten sam napis dwoma kształtami,
czyli drugie czytanie, którego nie ma czym odsiać,
więc pozycja żąda albo warunku na ciąg, albo innego miejsca.

Wysunięcie zdania podrzędnego jest faktem o spójniku i stoi w dwóch plikach:
`SPÓJNIKI_WYSUWANE` w `olski/subset.py` mówi to o szesnastu lematach analizy,
a `SPÓJNIKI` w `olski/skład/spójniki.py` o sześciu, których używa skład,
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
([`docs/subset.md`](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)).

Przysłówek ma w gramatyce dwóch gospodarzy, a polszczyzna daje mu trzeciego:
przysłówek przed przysłówkiem, jak `bardzo szybko`, nie dochodzi do niczego,
więc `Program zapisuje ustawienia bardzo szybko.` wychodzi jednym czytaniem,
w którym `bardzo` jest okolicznikiem zdania na równi z `szybko`.
Takich czytań zostaje jedno na sto pięćdziesiąt zdań przyjętych, wszystkie tej klasy
([`docs/subset.md`](docs/subset.md#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę)).
Ruchem jest symbol przysłówka rekurencyjny po stronie stopnia —
`Adverb → adv:degree Adverb` obok `Adverb → adv` — czyli ta sama pozycja,
którą przymiotnik dostał od `Adjective`, a przed nią pomiar.
Do przeczytania jest cena drugiego gospodarza, bo trzeci wraca z pytaniem tej samej
postaci: kupuje prawdę o drzewie i płaci jednoznacznością zdań, które dziś przechodzą,
a nad Składnicą drugi zapłacił za nią trzydziestoma dwoma zdaniami
([`docs/subset.md`](docs/subset.md#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe)).
Kto to podnosi, płaci przeliczenie wszystkich figur nad gramatyką
([`CLAUDE.md`](CLAUDE.md#checks)),
a korpusy trzeba mieć wszystkie trzy naraz, bo znak ceny zależy od rejestru.

Okolicznik przysłówkowy bierze całą część mowy, a Morfeusz daje czytanie `adv`
formom, których ten rejestr używa jako przyimka albo spójnika: `wobec`, `gdy`, `sam`.
Wychodzą z tego czytania, których polszczyzna w tych miejscach nie ma —
`postępować wobec innych w duchu braterstwa` dostaje trzy czytania z `wobec`
w roli okolicznika, a `Program zapisuje ustawienia, gdy linter sprawdza tekst.`
wychodzi obok czytania podrzędnego drugim, w którym `gdy` jest okolicznikiem
zdania spiętego przecinkiem.
Cena tej klasy jest przez to zmierzona i wynosi sześć zdań Składnicy:
tyle straciło jednoznaczność pod morfologią żywą, kiedy weszła podrzędność
okolicznikowa, i wszystkie sześć niesie `gdy` albo `kiedy`
([`docs/subset.md`](docs/subset.md#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie)).
Kryterium słownikowe `admissible` w `olski/subset.py` po nie nie sięga,
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

Dopełnienie stoi przed swoim czasownikiem w czterech szykach dopisanych,
a przed bezokolicznikiem, który je bierze, nie stoi w żadnym.
Ciała biorą `Verb`, czyli formę osobową, więc `premier większości nie może
ruszyć` dalej wychodzi z jednym podmiotem i bez dopełnienia,
i jest to jedno zdanie Składnicy, które olski czyta odwrotnie, niż czyta je
czytelnik
([`docs/subset.md`](docs/subset.md#cena-stoi-w-trafności-a-nie-w-liczbie-czytań)),
a pomyłka jest droższa od wieloznaczności, bo werdykt `valid` ktoś przeczyta.
Do przeczytania jest, ile ta pozycja zabiera poza tym jednym zdaniem:
dopełnienie przed łańcuchem `może ruszyć` konkuruje z przydawką dopełniaczową
tam, gdzie cztery szyki już konkurują z nią przed formą osobową,
i cenę tamtych czterech zna
[`sonda/szyk.py`](sonda/szyk.py) — sześć zdań —
więc ta pozycja ma z czym się porównać, zanim zapadnie decyzja.
Ruchem jest ciało `Complements`, a nie piąty szyk:
pozycję ramy niesie fraza bezokolicznikowa
([`docs/subset.md`](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
więc dopełnienie przed nią stoi wewnątrz orzeczenia,
a nie w kolejności podmiotu wobec czasownika.
Sonda różnicowa nad tym jednym ciałem, wzorowana na `sonda/szyk.py`,
idzie przed decyzją.

Forma `nie` ma u Morfeusza czytanie zaimkowe, którego polszczyzna w tym miejscu
nie ma: jest to biernik `on` w postaci popodstawowej, czyli tej, która stoi
wyłącznie po przyimku (`na nie`, `za nie`).
Grupa imienna bierze `ppron3` bez warunku, więc to czytanie stoi w każdej
pozycji dopełnienia, i to ono odbiera jednoznaczność jedynemu zdaniu,
które ją nad trzema rejestrami straciło przy wpuszczeniu negacji
([`docs/subset.md`](docs/subset.md#negacja-zmierzona-kupuje-przeszło-sto-zdań-i-nie-płaci-dopełniaczem)).
Kryterium słownikowe `admissible` w `olski/subset.py` po nie nie sięga,
bo wyrzuca rzeczownik nieodmienny, a tu chodzi o zaimek,
i cecha, po której to czytanie widać, jest inna: `praep` w tagu.
Ruchem jest warunek `npraep` na terminalu zaimka w grupie imiennej wraz z drogą
dla grupy pod przyimkiem, która `praep` brać musi, a przed nim pomiar,
ile czytań ten warunek zdejmuje nad Składnicą:
tagów `praep` jest w niej więcej niż samo `nie`.

Zamknięta lista kopul nie ma `stawać się` ani `okazywać się`,
a polszczyzna orzeka nimi narzędnik tak samo jak `zostawać`.
`Mao stał się na wiele lat przywódcą największego narodu na kuli ziemskiej.`
i `Człowiek staje się wyleniałym tygrysem.` są przez to odrzucone,
i są to dwa z 75 zdań, które zawężenie narzędnika odrzuca nad Składnicą,
a jedyne dwa, które odrzuca niesłusznie
([`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Przeszkodą nie jest lista, tylko cząstka: `KOPULA` w `olski/subset.py` jest
warunkiem na lemat, a te dwa czasowniki są kopulami wyłącznie z `się`,
którego produkcja kopuli nie ma gdzie postawić —
[`docs/subset.md`](docs/subset.md#what-the-grammar-covers) mówi to przy liście.
Ruchem jest ramka narzędnikowa w leksykonie zwrotnym,
czyli ta sama droga, którą walencja rozdziela formę z cząstką od formy bez niej,
a do przeczytania jest, co zwrotna kopula robi z `Ludzie rodzą się wolni.`,
gdzie orzecznik zgodny stoi dziś przy czasowniku zwrotnym niebędącym kopulą.

Współrzędność wypisuje się trzema produkcjami, a mogłaby jedną, lewostronnie rekurencyjną.
`X → X conj X` powiedziałoby o zasięgu to samo co trzy poziomy z `build`
w `olski/subset.py`, bo zawężenie zasięgu stoi na rodzaju,
którego koordynacja nie ma
([`docs/subset.md`](docs/subset.md#nothing-above-a-coordination-distributes-into-it)),
a nie na kształcie produkcji.
Przeciw takiej produkcji był parser i już go nie ma:
tablica Earleya bierze lewą rekursję, co pilnuje `tests/test_subset.py`.
Różni te dwa zapisy liczba czytań ciągu współrzędnego,
bo wyprowadzeń tego samego ciągu jest pod nimi inaczej wiele,
i to jest jedyne, co tu jest do zmierzenia.
Do przeczytania są figury, które nad tymi poziomami bierze
[`sonda/przecinek.py`](docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania),
bo zmiana rusza je razem z werdyktami.
Ruchem jest jedna produkcja w miejsce trzech, o ile pomiar pokaże,
że czytań nie przybywa; przy przeciwnym wyniku ruchem jest samo zdanie w tej sekcji
mówiące, że wybór padł na trzy poziomy dla liczby czytań, a nie dla parsera.
Widać na czym mierzyć: zdanie ustawy o siedmiu członach ma dziś 28 042 czytania
([`docs/ustawy.md`](docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)),
i nie jest policzone, ile z tej liczby bierze sama współrzędność.

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

Czas przeszły zostawił za sobą 297 zdań Składnicy, których nikt nie przeczytał.
`praet` prowadził kolejkę blokerów z 2934 zdaniami,
a po dopisaniu tej formy do `Verb` w `olski/subset.py` wiersz ten czytał 297,
i są to zdania, które na czasie przeszłym stawały i dalej na nim stają.
Wiersz czyta dziś 331 ([`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)),
a 34 dołożył liczebnik, przesuwając na czasownik blokery zdań, których nie przyjął,
więc do przeczytania jest cała ta resztka, a nie tamte 297.
Nie wiadomo, czy stoi za tym jedna konstrukcja, czy dwadzieścia:
`Wózek zwolnił biegu i przystanął.` i `Pani Zofia była w rozpaczy.`
są w tej resztce obok siebie, a łączy je tyle, że bloker wskazał czasownik.
Ruchem jest odczytanie tej resztki i rozbicie jej na klasy,
z tego klasy nazwane w [`docs/subset.md`](docs/subset.md#what-it-does-not-cover-yet),
jeśli któraś jest konstrukcją, a nie zbiegiem okoliczności.
Do przeczytania jest sam `blocker` w `olski/coverage.py`:
nazywa on formę, na której rozbiór stanął,
a przy zdaniu z czasownikiem w środku bywa to forma stojąca za prawdziwą przyczyną,
więc część tej resztki może być artefaktem tego odczytu, a nie brakiem w gramatyce.

Aglutynant dochodzi tylko do czasownika, przy którym stoi.
`_formy_skończone` w `olski/subset.py` bierze `praet` z `aglt` po nim,
bo tak Morfeusz tnie `napisałem`,
a polszczyzna stawia tę końcówkę także przy innym słowie zdania:
`gdzieś ty był`, `myśmy przyszli`, `dlaczegoś to zrobił`.
Ruchem jest aglutynant przyłączany do zdania, a nie do czasownika,
czyli cecha osoby wypuszczana w górę z miejsca, w którym końcówka stanęła.
Do rozstrzygnięcia jest, czy warto:
konstrukcja jest w rejestrze technicznym rzadka albo nieobecna,
a w prozie literackiej Składnicy nie jest, i nikt nie policzył, ile jej tam.
Do przeczytania są zdania Składnicy, w których `aglt` stoi poza `praet`,
bo od ich liczby zależy, czy ten wpis jest wart ceny ruchu.

Zdanie względne z wysuniętym dopełnieniem żąda podmiotu, a polszczyzna go tam opuszcza.
Każde ciało z dopełnieniem, jakie pisze `_wysunięta_rola`
w `olski/subset.py`, ma wypisany podmiot,
więc `Dyrektor wymienia imprezy, które zorganizował.` nie wyprowadza się wcale,
a `Dyrektor wymienia imprezy, które on zorganizował.` raz.
Funkcja pisze te ciała dla obu rodzin czół, więc ruch dotyka i pytania:
`Które zadania gmina wykonuje?` ma podmiot, a `Które zadania wykonuje?` go nie ma
i przez to nie wyprowadza się wcale.
Nad Składnicą są to cztery zdania i wyszły one z
[pomiaru luki](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze),
który je kupił mimochodem, mierząc co innego:
cechy przeciąganej te cztery zdania do kupienia nie potrzebują.
Ruchem jest deklaracja bez podmiotu obok tej z podmiotem,
czyli to samo, co zdanie główne ma w `ClauseConjunct → Predicate`,
a ile ciał ona napisze, rozstrzyga rozwinięcie szyku, a nie ręka
([`docs/subset.md`](docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Do przeczytania jest, ile ta pozycja dokłada wieloznaczności:
zdanie względne bez podmiotu konkuruje z czytaniem, w którym podmiotem jest zaimek,
a rodzina ta liczy siedemnaście ciał.
Cenę i zakup bierze się sondą różnicową, tak jak przy każdym dopisaniu
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
a wpis jest winien przebiegi, których żąda [sekcja Checks](CLAUDE.md#checks).

Luka jest węzłem o pustej rozpiętości, więc rola wypełniona przez nią nie ma nazwy,
i na tym stanął pomiar cechy przeciąganej
([`docs/design-notes.md`](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
`agreement` w `olski/coverage.py` porównuje rozpiętości,
więc rozpiętość pusta nie trafia w żadną złotą i liczy się jako niezgodna —
wszystkie cztery zdania, jakie luka wyciągnęła ze Składnicy, wyszły tak,
choć role widoczne mają dobre.
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

Pozycja pytania zależnego stoi w ramie domyślnej i nikt nie zmierzył jej zawężenia.
`RAMA_DOMYŚLNA` w `olski/subset.py` daje `int` każdemu czasownikowi,
tak jak daje mu `comp`, a Walenty wypisuje osobno lematy z jednym i z drugim
([`docs/subset.md`](docs/subset.md#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał)).
Zawężenie `comp` do leksykonu zmierzono i nie kupiło ani jednego czytania,
a przy `int` wynik nie musi wypaść tak samo:
pytanie zależne konkuruje z koordynacją przecinkiem i ze zdaniem względnym,
gdzie zdanie z `że` nie konkuruje z niczym, bo spójnika `że` nie bierze nic innego.
Ruchem jest czwarte zdanie leksykonu, wzięte z `cp(int)` przez `olski/walenty.py`,
i wariant gramatyki bez `int` w ramie domyślnej, zmierzony wobec olskiego.
Do rozstrzygnięcia jest, czym ten wariant zmierzyć:
`sonda/ruch.py` zdejmuje grupy produkcji, a zawężenie ramy jest zmianą danych,
więc albo maszyneria bierze gramatykę wariantu funkcją — o co prosi też `sonda/luka.py` —
albo przebieg staje obok niej i wtedy jest drugą deklaracją tego samego.
Do przeczytania jest przy tym, czy skład ma dla tego zdania czytelnika:
`bierze_zdanie` w `olski/walencja.py` czyta ono, a pytania zależnego
`olski/skład/składnia.py` nie ma czym postawić,
więc zdanie dopisane bez tej kategorii jest danymi, których nie czyta nikt.

`o którym mowa` nie ma wyprowadzenia, a jest najczęstszym zdaniem względnym ustaw.
Zwrot ten niesie 851 zdań siedmiu ustaw i „Zasad techniki prawodawczej”
z 5620, jakie te dwa korpusy mają —
`grep -cP 'o (którym|której|których) mowa' proza/ustawy.txt proza/ztp.txt` je liczy —
a `mowa` jest u Morfeusza `subst:sg:nom:f` i orzeczeniem zdania względnego,
w którym kopuła jest opuszczona: `o których [jest] mowa w ust. 1`.
Zdania składowego bez czasownika gramatyka nie ma, więc żadne z tych zdań nie przechodzi.
Do rozstrzygnięcia jest, czy kopuła opuszczona wchodzi jako pozycja `ClauseConjunct`,
czy jako wpis leksykalny na lemat `mowa`, wzorowany na `KOPULA` w `olski/subset.py`.
Pozycja ogólna jest droga po stronie wieloznaczności, bo czyni zdaniem każdą grupę
imienną w mianowniku, a wpis na lemat kupuje ten jeden zwrot i nic poza nim,
czyli jest zamkniętą listą, jakich ta gramatyka ma dwie i obie wyceniła.
Do przeczytania jest `Predicative` w tym samym pliku:
orzecznik rzeczownikowy stoi tam w narzędniku i pod kopułą, a nie w mianowniku,
więc kopuła opuszczona żąda drugiej pozycji orzecznika, a nie tej samej bez czasownika.
Zakup jest niepoliczony i nie jest nim te 851 zdań:
zdanie ustawy niesie zwykle kilka konstrukcji odrzucających naraz,
a ile z nich stoi na samym tym zwrocie, wyda dopiero sonda różnicowa
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).

Zaimek rzeczowny nie rządzi dopełniaczem, a kryterium na to nazywa jeden lemat.
`ZAIMEK_RZECZOWNY` w `olski/subset.py` wyklucza `to` z głowy, która bierze
dopełniacz pod sobą, a Morfeusz znakuje jako `subst` całą klasę takich zaimków:
`nikt`, `kto`, `nic`, `coś`, `ktoś`.
Żaden z nich dopełniacza przy sobie nie bierze, więc każdy daje drugie czytanie
tam, gdzie stoi po dopełniaczu albo przed nim,
a `Polszczyzna, której nikt nie napisał, jest podzbiorem.` traci przez to jednoznaczność,
bo `której nikt` wychodzi grupą wysuniętą
([`docs/subset.md`](docs/subset.md#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania)).
Ruchem jest lista lematów w miejsce jednego, a przed nim rozstrzygnięcie,
czy klasę tę nazywa lemat, czy coś, o co da się zapytać czytanie:
lista zamknięta postarza się o każdy zaimek, którego nikt do niej nie dopisał.
Do przeczytania jest cena tamtego kryterium
([`docs/subset.md`](docs/subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)),
bo rozszerzenie płaci tą samą walutą, tylko na kilku lematach naraz.
Cena jest niepoliczona i sonda różnicowa jej nie policzy,
bo `sonda/ruch.py` zdejmuje produkcje, a to jest zmiana warunku w terminalu;
liczbę wydaje przebieg nad korpusem z warunkiem i bez niego, czytany ręką,
tak samo jak przy tamtym kryterium.

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
Do policzenia zostaje zakup, czyli ile zdań z takim ciągiem rejestr ma;
nad Składnicą i nad ustawami nie policzył ich nikt.
Dopóki tej liczby nie ma, wpis stoi po stronie ceny,
bo jednoznaczność płacona za pokrycie niepoliczone
idzie wbrew cenie kroku, której żąda
[`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).

Wyrażenie przyimkowe przyłącza się do ostatniego członu ciągu współrzędnego
albo do zdania, a do całego ciągu nie przyłącza się wcale.
`Pliki i katalogi w tym drzewie rosną.` wychodzi dwoma czytaniami —
`Pliki i [katalogi w tym drzewie]` oraz `w tym drzewie` przy `rosną` —
a czytania, w którym w tym drzewie są i pliki, i katalogi, nie ma,
choć polszczyzna je ma.
Powodem są produkcje przyjmujące `Modifier`:
`NPConjunct` i `APConjunct` w `olski/subset.py` mają go pod głową członu,
a produkcje koordynacji nie mają go wcale.
[Zawężenie o przydawce](docs/subset.md#nothing-above-a-coordination-distributes-into-it)
tej pozycji nie uzasadnia, bo wywodzi się z braku rodzaju u ciągu:
przymiotnik nad ciągiem zgadzałby się z niczym,
a wyrażenie przyimkowe nie zgadza się z niczym również pod członem.
Ruch przepisuje tamtą sekcję, bo tytuł mówi tam o wszystkim,
co nad ciągiem stoi, a wywód pod nim o samej przydawce.
Żąda jej natomiast
[reguła o obu czytaniach wszędzie](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
bo pozycja z produkcją na jedno przyłączenie i bez produkcji na drugie
wybiera przez przeoczenie.
Ruchem są dwa ciała `NP` i dwa `AP`, po jednym na spójnik i na przecinek,
z `Modifier` za całym ciągiem.
`NP → NP Modifier` tym ruchem nie jest:
dałoby drugie wyprowadzenie każdej grupie bez koordynacji,
czyli czytanie, którego polszczyzna tam nie ma.
Do przeczytania jest
`test_pierwszy_artykuł_deklaracji_stoi_na_przyłączeniu_wyrażenia_przyimkowego`
w `tests/test_subset.py`, bo wylicza dwa czytania pierwszego artykułu Deklaracji,
a ruch dopisuje im trzecie.
Wpis jest winien przebiegi, których [sekcja Checks](CLAUDE.md#checks)
żąda od zmiany w gramatyce,
wraz z listą pozycji przyłączeniowych w
[`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
która rośnie o tę jedną.
Te same produkcje przepisuje wpis o współrzędności wypisanej trzema poziomami
zamiast jedną produkcją lewostronnie rekurencyjną,
więc ten z dwóch, który wejdzie pierwszy, wybiera kształt dla drugiego.

`pod względem` żąda licencji od słowa, do którego się przyłącza,
a olski żąda licencji tylko od dopełnienia.
Czytelnik odrzuca `wolni pod względem swej godności` bez pomocy składni,
bo `równy` ma pozycję na wzgląd, a `wolny` jej nie ma.
Tę samą obserwację robi nad `przewyższać`
[`docs/subset.md`](docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera),
gdzie porównanie mówi, w czym jedno przewyższa drugie,
i nie ma jej dziś gdzie zapisać.
Leksykon walencyjny mówi trzy zdania i wszystkie trzy zawężają ramę dopełnienia
([`docs/subset.md`](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)),
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
kiedy dopisze je wpis o wyrażeniu przyimkowym przyłączanym do ciągu,
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
przecinek jest już znakiem koordynacji na trzech poziomach
([`docs/subset.md`](docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania)),
więc apozycja dokłada czytanie każdemu ciągowi rozdzielonemu przecinkiem.
Do przeczytania jest, ile apozycji rejestr ma, bo bez tej liczby wpis jest samą ceną,
a gotowej nie ma gdzie wziąć:
[pomiar wieloznaczności](docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
wymienia apozycję wśród swoich zawyżeń, ale tę bez przecinka — `podpis CERTYFIKAT` —
czyli konstrukcję inną niż ta.
Pierwszym pytaniem jest więc, czy bank drzew rozdziela apozycję od koordynacji
etykietą, po której da się ją policzyć.

Cztery przebiegi budują nad Składnicą te same lasy, bo jeden z nich pyta las o mniej.
`zmierz_zdanie` w `olski/coverage.py` woła `podsumuj` bez deklaracji,
więc `Outcome` nie niesie ani ról różniących, ani przyłączeń, ani rozbieżności,
a `sonda/czytania.py` rozbiera przez to cały bank drzew drugi raz po to samo.
Trzeci jest `sonda/wskazania.py`, który tych samych przyłączeń potrzebuje,
żeby zapytać o nie warstwę, i różni się od dwóch pozostałych tym, że czyta las
razem z cudzym drzewem — więc scalenie obejmuje go dopiero wtedy, gdy przebieg
zbiorczy umie oddać jedno i drugie.
Czwarty jest `sonda/znaczenia.py` i on jeden potrzebuje samych czytań, a nie
podsumowania z nich, bo każde puszcza przez `abstrahuj`; przebieg zbiorczy albo
odda drzewa czytań przez granicę procesu, albo zrobi tę abstrakcję u siebie,
i to jest pytanie do rozstrzygnięcia przed scaleniem, a nie po nim.
Ten sam czwarty przepisuje z `sonda/czytania.py` całe rusztowanie przebiegu
spisowego — `Raport`, `zanotuj`, `scal`, pulę procesów i tabelę procentową —
czyli to, czym `sonda/ruch.py` jest dla sond różnicowych, a czego spisowe nie mają;
scalenie przebiegów zdejmuje połowę tego duplikatu i dlatego idzie przed nim.
Rusztowanie to przepisuje także `sonda/płaski.py`, a lasów olskiego nie buduje
wcale, bo mierzy wariant gramatyki, więc scalenie przebiegów go nie obejmie
i zostanie po nim sam duplikat rusztowania — to on mówi, ile ono jest warte
osobno.
Ruchem jest deklaracja podana tam, gdzie las i tak stoi zbudowany,
po którym tabela z
[`docs/disambiguation.md`](docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)
wychodzi z `olski-corpus`, a sonda się kasuje.
Ceną jest to, czego dziś ten przebieg nie liczy:
`różniące`, `przyłączenia` i `rozbieżności` chodzą po lesie osobno,
a `olski-corpus` puszcza się nad 13 035 zdaniami i pod pulą procesów.
Do przeczytania jest więc najpierw, ile ta trójka dokłada do przebiegu,
bo poniżej progu, przy którym to widać, ruch jest samym zdjęciem duplikatu,
a powyżej jest wyborem między dwoma przebiegami a jednym droższym.
Do przeczytania jest przy tym `Report.record` w `olski/coverage.py`,
gdzie licznik klas musiałby stanąć, i `KAWAŁEK` obok,
bo przez granicę procesu idzie licznik, a nie las.

Ciąg współrzędny wewnątrz wypełnienia roli nie ma po werdykcie żadnego wiersza.
Nawias pokazuje granicę członu tylko nad ciągiem, którym jest sama rola
(`_nawiasuj` w `olski/parse.py`),
a wiersz o konstytuencie ustępuje mu miejsca nad każdym ciągiem
(`_nazwany_gdzie_indziej` tamże),
więc `Ustawa określa zadania ochrony ludności i obrony cywilnej.`
zostaje samą liczbą czytań i tak zostaje siedem z 272 werdyktów rejestru ustaw
oraz trzy z 549 zdań wieloznacznych Składnicy
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

Grupa liczebnikowa w pozycji dopełnienia ma w banku drzew gniazdo,
którego porównanie ról nie czyta, więc dobre czytanie liczy się jako niezgodne.
`Marzec przyniósł 6 zagranicznych delegacji.` olski czyta tak, jak czyta je czytelnik,
a drzewo wzorcowe daje temu dopełnieniu `np(part)`,
czyli przypadek strukturalny, którym polszczyzna oznacza właśnie tę frazę,
i `_role` w `olski/corpus.py` nie tłumaczy tego gniazda na żadną rolę olskiego.
Gold nie ma wtedy dopełnienia, z którym można by się zgodzić,
a `agreement` w `olski/coverage.py` liczy rolę przypisaną poza gniazdem jako `disagrees`,
więc wiersz niezgodnych z [`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)
jest o jedno zdanie za długi i będzie rósł razem z liczebnikiem.
Ruchem jest `np(part)` odwzorowane na `Object` obok `np(acc)` i `np(accgen)`.
Do rozstrzygnięcia jest, czy to gniazdo jest dopełnieniem zawsze:
`Napiłem się wody` ma w nim dopełniacz partytywny, który dopełnieniem jest,
a olski go nie bierze, więc odwzorowanie nie zmieni na nim niczego,
i pytanie brzmi, czy bank drzew stawia tam kiedykolwiek coś, co dopełnieniem nie jest.
Do przeczytania są zdania Składnicy z tym gniazdem
wraz z werdyktem, jaki nad nimi wydaje `olski-corpus --morphology gold`,
bo tylko one mogą tę zmianę cokolwiek kosztować.
Ruch jest winien przebiegi, których [sekcja Checks](CLAUDE.md#checks)
żąda od zmiany w tabeli zgodności, i rusza ją w obu kolumnach.

Werdykt nad zdaniem mówi, na czym odrzucenie stanęło, a przebieg nad korpusem zgaduje.
`blocker` w `olski/coverage.py` nazywa część mowy pierwszego czytania formy
i sam w docstringu mówi, że między czytaniami wybiera dowolnie,
więc kolejka z [`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)
jest rankingiem stojącym na tym wyborze,
choć ten dokument opisuje ją jako listę słów, których żadna produkcja nie bierze.
Ruchem jest wycięcie czytań bez licencji przed rozbiorem,
po którym forma bez ani jednego czytania jest dla `blockera` brakiem licencji,
a nie brakiem struktury, którym ją dziś nazwie,
i wywód wraz z ceną tego wycięcia trzyma
[`docs/design-notes.md`](docs/design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej).
Rusza ono kolejkę, więc wpis jest winien przebiegi,
których [sekcja Checks](CLAUDE.md#checks) żąda od zmiany w czytaniach,
jakie gramatyka dostaje.
Do przeczytania jest, ile ta kolejka na tym się zmienia,
i tę różnicę trzeba przeczytać przed wybraniem korpusu:
złota morfologia zostawia bank drzew bez ani jednej formy nieznanej,
więc tam wycięcie nie rozdzieli niczego,
a nad prozą README brak w słowniku stoi w tej kolejce zaraz za przecinkiem.
Zostaje przy tym pytanie, którego werdykt nad zdaniem nie zadaje:
`olski-check` mówi o zdaniu, a nie o pliku,
więc rankingu form bez licencji nad dokumentem nie wypisuje nikt,
i do rozstrzygnięcia jest, czy jest to wiersz tej komendy, czy tryb obok niej.
Czytelników takiego rankingu jest już dwóch:
[kolejka nad rejestrem ustaw](docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
jest wzięta potokiem z grepem, który ten dokument drukuje,
bo nie ma komendy, która by ją wypisała.

Part of what [`docs/corpus.md`](docs/corpus.md) quotes has no command behind it.
`olski-corpus` prints the verdict tables, the length curve
and the blocker ranking by part of speech,
while the commonest forms under each blocker,
the count of sentences the two runs both accept,
and the column with `admissible` switched off
come from scripts written for one session and thrown away.
So a change to the grammar updates the tables that have a command
and silently leaves the rest stale,
which is the failure the rerun rule in
[`CLAUDE.md`](CLAUDE.md#checks) exists to prevent.
The move is in `olski/coverage.py`:
carry the blocking form beside its part of speech in `Report.blockers`,
add the exclusion-free morphology as a third `SOURCES` entry,
and let the CLI take two runs and print what they disagree about.
That last part has a second caller,
so it should not be tied to the morphology sources:
a point on [the coverage curve](docs/design-notes.md#making-the-trade-measurable)
is a net of what a tier buys against what it costs in uniqueness,
which is two grammars disagreeing rather than two morphologies.
That net is what the grammar track now asks of every addition before it lands
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
so this part of the entry carries a rule rather than a convenience.
The third of those moves exists, and for that second caller rather than for this one.
`sonda/ruch.py` runs olski against a variant and prints what moved between them,
and five probes are written as declarations against it, `przecinek.py` among them,
while `nieciągłość.py` computes its own net beside that machinery rather than on it.
What the machinery takes is a group of productions removed from olski,
and a morphology switched off is neither a group nor a production,
so the two runs this entry wants compared have no command.
The entry about hand-taken figures being differential probes says as much
from its own side, handing the `admissible`-off column back here.
The entry about cutting unlicensed readings before the parse
moves what `blocker` reads off a form,
so whichever of the two is taken first decides what the blocking form is,
and they are one session.
The section that owns the reproduction path says meanwhile which figures are hand-taken,
and that sentence goes when the commands cover them.

Six of those figures were left stale by the change that admitted
[four word orders](docs/subset.md#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka),
and they are named here so that the next session does not have to find them.
Each counts sentences and each moved with the accepted set, and none has a command:
what the past tense bought, in
[`docs/subset.md`](docs/subset.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku),
whose `praet` row the blocker table has contradicted since negation and the numeral
landed; and five in
[`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)
and the section after it — the instrumental dropped from every valency class,
the rest of the valency lexicon, the condition that the substantival pronoun
governs no genitive, the live totals with the dictionary exclusion switched off,
and what the frame settles under live morphology.
The values are in those documents and not repeated here,
because a value copied into this list is stale twice over once somebody retakes it.
Taking them by hand is the work this entry is about not doing twice,
so the general version above is the move, and retaking them meanwhile is the fallback.

Okolicznik nie staje między czasownikiem a tym, co przy nim stoi, i nikt tego nie wycenił.
`czasownikowe` w deklaracji zdania w `olski/subset.py` wymienia `Verb` i `Predicate`,
więc miejsce na okolicznik staje po córce, która jest grupą, i po czasowniku nie staje
([`docs/subset.md`](docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Polszczyzna tę pozycję ma i olski płaci za jej brak w obu walutach naraz:
`Trwa w tej sprawie dochodzenie.` jest odrzucone,
a `Zapisuje w pliku program ustawienia.` wychodzi jednym czytaniem,
w którym `program ustawienia` jest dopełnieniem,
i nie wychodzi tym, w którym `program` zapisuje `ustawienia`.
Drugie jest cięższe, bo `valid` mówiący o zdaniu nieprawdę ktoś przeczyta
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).
Zawężenie to jest starsze od rozwinięcia szyku i weszło brakiem ciała,
a rozwinięcie zrobiło z niego jeden argument, więc dopiero teraz je widać.
Ruchem jest zdjęcie `Verb` z tej krotki, a przed nim pomiar:
dziesięć produkcji więcej, a cena stoi w rolach, nie w przyłączeniu,
bo pozycja ta daje zdaniu czasownikowemu drugie czytanie z podmiotem,
gdzie pozostałe pozycje okolicznika dają drugie przyłączenie.
Jest to więc inne pytanie niż to, na które odpowiada
[reguła o obu czytaniach](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
i sondą je bierze `sonda/ruch.py` tak samo jak każdą inną grupę produkcji.
Do przeczytania jest cena czterech szyków dopisanych
([`docs/subset.md`](docs/subset.md#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka)),
bo one też kupowały czytania z podmiotem i wróciły z ceną siedmiu zdań.
Zamknięcie wpisu kasuje wiersz `Trwa w tej sprawie dochodzenie.`
z `test_these_have_no_reading` w `tests/test_subset.py`.

Grupa imienna mnoży ciała iloczynem, którego rozwinięcie szyku nie dosięga.
`NPConjunct` w `olski/subset.py` ma dwanaście ciał,
z czego osiem jest iloczynem czterech kształtów głowy
przez obecność `Modifier` po niej,
i mnoży to obecność oraz kolejność rodzajów przydawki,
a nie permutacja argumentów,
więc warunek precedencji nie ma tu czego powiedzieć
([`docs/subset.md`](docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Czwarty kształt głowy, czyli przymiotnik z dopełniaczem naraz,
wszedł jako dwa ciała, bo `Modifier` musiał wejść razem z nim,
i tyle samo zażąda każdy następny.
Zdanie względne tego iloczynu nie ruszyło i pokazuje, którędy się go omija:
dochodzi ono do `NP`, czyli o poziom wyżej, więc jest jedną produkcją,
a nie trzecim rodzajem przydawki razy cztery kształty głowy.
Kosztowało to symetrię w koordynacji i osobny wpis wyżej,
a `Adjuncts` w tym samym pliku się nie mnoży,
bo okoliczniki są jednego rodzaju.
Kierunek pokazuje więc samo zdanie względne: przydawka dochodząca do `NP`
zamiast do członu znosi ten iloczyn,
a przy okazji zmienia zasięg, bo daje przydawkę całemu ciągowi współrzędnemu,
czego przydawka pod członem nie daje.
Jest to ta sama pozycja, o którą prosi wpis o wyrażeniu przyimkowym nad ciągiem,
więc kto podnosi jeden z tych dwóch wpisów, rozstrzyga i drugi.
Do przeczytania jest `_role` w `olski/skład/rozbiór.py`,
bo czyta ono kształty gramatyki po etykiecie,
więc każdy nowy poziom kosztuje tam gałąź.

`sonda/polszczyzna.py` jest drugą deklaracją podzbioru,
który deklaruje `olski/subset.py`,
czyli tym drugim właścicielem faktu, przed którym broni
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely),
i pilnuje jej tylko siedem zdań z `tests/test_sonda.py`.
Te dwie deklaracje rozeszły się na koordynacji przecinkiem
— olski bierze przecinek na trzech poziomach, a sonda spójnik —
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
Póki liczby z niej cokolwiek trzymają, kopia zarabia na siebie.
Wpis czekał na to, aż szyk zejdzie do warunków precedencji,
i tamten ruch jest zrobiony
([`docs/subset.md`](docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
więc kopia trzyma odtąd samą liczbę zdań zgodnych,
czyli to, co po każdej produkcji mówi coraz mniej o różnicy dwóch formalizmów,
a coraz więcej o tym, czego sonda nie ma.
Ruchem jest wtedy `git rm sonda/__main__.py sonda/polszczyzna.py sonda/wiezy.py`
wraz z `tests/test_sonda.py`,
z figurami [tamtej sekcji](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)
oraz z figurą `sonda-readme` w [`harness/figury.py`](harness/figury.py)
i jej wydrukiem w `figury/`.
Katalog zostaje, bo `sonda/przecinek.py` jest osobną sondą wokół osobnej decyzji,
i zostaje z nim nazwa `sonda` w `SOURCES` z `tests/test_docs.py`.
Zostaje z sekcji to, co figur nie potrzebuje:
że nieciągłość jest warunkiem zdejmowanym, a nie szczeblem,
i że jednoznaczność bywa osiągana bez trafności.
Kasowanie zabiera przy tym jedyny mechanizm w repozytorium,
który wypuszcza konstytuent nieciągły:
`spójne` w `sonda/wiezy.py` jest warunkiem zdejmowanym,
a produkcja z `olski/subset.py` spójności zdjąć nie umie.
Tym warunkiem zmierzono cenę nieciągłości i zamknięto
[rozwidlenie o przestawianiu](docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
a liczy ją `sonda/nieciągłość.py`, czyli trzeci plik tego katalogu,
który `sonda/wiezy.py` i `sonda/polszczyzna.py` czyta.
Lista plików wyżej nie obejmuje więc tego, co kasowanie naprawdę zabiera,
a [sekcja Checks](CLAUDE.md#checks) każe tę cenę przeliczać razem z gramatyką.
Ruch dopisuje sobie przez to jedno rozstrzygnięcie:
albo cena nieciągłości przestaje być figurą przeliczaną
i tamta sekcja mówi o niej to, co `docs/firing-rates.md` mówi o sobie,
czyli że jest ceną, przy której decyzja zapadła,
albo podłoże zostaje po to jedno, a kasowanie obejmuje samo porównanie deklaracji.

Liczba pozycji na `Modifier` w `sonda/polszczyzna.py` nie ma wyprowadzenia.
Komentarz przy więzach okolicznika mówi „trzy deklaracje zamiast jedenastu pozycji”,
a jedenastu nie daje żaden sposób liczenia produkcji `build` w `olski/subset.py`,
jakim udało się tę liczbę odtworzyć:
córkę `Adjuncts` albo `Modifier` ma sześćdziesiąt pięć produkcji,
samo `Modifier` stoi w ośmiu z nich,
a produkcji `ClauseConjunct` z okolicznikiem jest dziewiętnaście.
Regułę liczenia rozstrzygnęła po swojej stronie
[`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
która liczy produkcje i mówi, które z nich zdejmuje.
Ruchem jest przepisanie komentarza na regułę i liczbę,
przy czym sonda liczy miejsca w zdaniu, a tamten dokument produkcje,
więc albo przejmuje tę regułę, albo mówi, czemu liczy co innego.
Bez reguły żadna zmiana w gramatyce nie umie tej liczby ponieść,
a [sekcja Checks](CLAUDE.md#checks) każe ponieść figury sondy razem z gramatyką.
Zamyka ten wpis także wycofanie sondy,
bo komentarz stoi w pliku, który wtedy znika.

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
Kupuje to jednak dokładnie tyle, ile jest ram o dwóch pozycjach naraz, a takich nie ma:
biernik z bezokolicznikiem naraz zmierzono i nad Składnicą pod złotą morfologią
przyjmuje 289 zdań zamiast 293, a wieloznacznych ma 116 zamiast 110,
bo grupa imienna za bezokolicznikiem dochodzi wtedy i do niego, i do formy osobowej.
Wpis czeka więc na pozycję, która z inną naprawdę stoi,
czyli na dopełnienie w celowniku obok biernika — `dać uczniowi książkę` —
którego produkcji olski dziś nie ma;
bez niej mechanizm rozwija się na jedną pozycję i nie liczy niczego.

Czytelnik Składnicy gubi węzeł bez słowa w dwóch miejscach,
a gubi go z drzewa, na którym stoi zgodność ról, a nie samo przyjęcie zdania.
`_gold` w `olski/corpus.py` pomija dziecko, którego `nid` do niczego nie prowadzi,
a `NIEWYBRANY` wycina węzły, którym `chosen` przeczy,
i stoi na tym, że format tak to znaczy, a nie na sprawdzeniu.
Łapie oba jedno kryterium: terminale wybranego drzewa
mają pokrywać rozpiętość korzenia bez dziur i bez zakładek.
Nad wydaniem 2018 żaden las z werdyktem `FULL` mu nie przeczy,
a lasy bez werdyktu przeczą mu masowo,
bo tam `_root` schodzi do najszerszego wybranego węzła i znajduje fragment,
więc kryterium obejmuje `annotated` i nic poza tym.
Do rozstrzygnięcia zostaje, co ma się stać z lasem, który mu przeczy:
przerwać przebieg czy wejść do niemierzonych obok zdań bez morfologii,
i to drugie żąda wiersza w wydruku, którego pierwsze nie żąda.
Sprawdzianem do napisania obok jest las, który kryterium łamie,
bo `tests/test_corpus.py` pisze lasy ręcznie i taki też napisze.

Cenę pozycji, która nie rusza werdyktu, bierze ręka, bo sonda różnicowa liczy werdykty.
Etykieta roli nad wysuniętym czołem nie rusza ani jednego
([`docs/subset.md`](docs/subset.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)),
a `Raport.zapisz` w `sonda/ruch.py` notuje zgodność ról pod zdaniem nowo przyjętym,
czyli dokładnie tam, gdzie werdykt się ruszył,
i `Outcome.ocalenie` nie bierze wcale.
Zakup wzięto więc dwoma przebiegami `olski-corpus` i odjęciem wierszy ręką,
a tamta sekcja nazywa liczby oraz produkcje, które wariant zdejmuje,
żeby dało się je wziąć drugi raz.
Ruchem są dwie rzeczy naraz i żadna sama nie wystarcza.
Pierwszą jest mianownik brany ze zgodności, a nie z werdyktu:
`zapisz` ma notować zgodność i ocalenie każdego zdania, które oba warianty przyjmują,
a nie tylko tego, którego werdykt się ruszył.
Drugą jest gramatyka wariantu brana funkcją, a nie zdejmowaniem grupy produkcji:
etykieta jest konstytuentem nad czołem, a ciała zdania biorą ją nazwą symbolu,
więc zdjęta zostawia rodzinę względną bez córki, a nie bez etykiety.
Tego samego żąda od tej maszynerii `sonda/luka.py`.

Sonda luki domyka lukę w rodzinie względnej i nie domyka jej w pytaniu.
`DOMYKA` w `sonda/luka.py` wymienia `RelativeCore` i nic poza nim,
a `_wysunięta_rola` w `olski/subset.py` pisze tym samym kształtem
także czoło pytania, więc wariant z luką zdejmuje ciała względne,
a pytających nie zdejmuje, choć cecha przeciągana zastąpiłaby jedne i drugie.
Rodzina względna ma przy tym dwa czoła — sam zaimek i grupę, w której on stoi —
a wariant z luką wiąże ją tylko zaimkiem, więc grupa wysunięta z niego wypada.
Pomiar przez to zaniża i zakup, i cenę: zdanie `Które zadania wykonuje?`
jest tam odrzucone tak samo jak bez luki
([`docs/design-notes.md`](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
Ruchem jest `InterrogativeCore` obok `RelativeCore` w tej stałej,
a razem z nim `InterrogativeModifier` obok `RelativeModifier`
w `_wysunięty_okolicznik` w tym samym pliku,
bo pytanie ma dziś czoło przyimkowe tak samo jak zdanie względne
i luki pod nim nie żąda z tego samego powodu.
Przed jednym i drugim stoi rozstrzygnięcie, czym pytanie lukę wiąże:
zdanie względne wiąże ją zaimkiem, którego liczbę i rodzaj podejmuje poprzednik,
a pytanie poprzednika nie ma, więc te dwie cechy nie mają się z czym zejść.
Wpis jest winien przebiegi, których żąda ta sekcja tamtego dokumentu,
bo rusza w niej każdą liczbę.

Cząstka `się` stoi przy formie osobowej, a należy do bezokolicznika za nią.
`Zebranie ma się odbyć.` jest u olskiego czasownikiem `mieć się`,
bo produkcja `Verb` w `olski/subset.py` skleja cząstkę z formą osobową
i tylko z nią, a polszczyzna kładzie ją tam także wtedy,
gdy zwrotny jest bezokolicznik.
Płaci za to [gramatyka](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego):
zawężenie o bezokolicznik jest wobec Walentego prawdziwe,
a nad Składnicą kosztuje dwa zdania i nie kupuje żadnej jednoznaczności,
więc parser tego zdania leksykonu nie czyta, choć skład je czyta,
i mówi w `olski/walenty.py`, dlaczego.
Ruchem jest cząstka licencjonowana przez czasownik, do którego należy,
a nie przez ten, przy którym stoi.
Do rozstrzygnięcia jest, czy da się to postawić bez czytania,
w którym oba czasowniki biorą ją naraz,
bo takie czytanie jest drugim czytaniem tego samego zdania.
Zamierzone jest po tym powtórzenie tamtego pomiaru,
bo zawężenie o bezokolicznik wraca wtedy do rozważenia.

Sprawdzian leksykonu jest skryptem pisanym od nowa przy każdej zmianie.
[Liczba, na której leksykon stoi](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)
— 615 z 616 lematów potwierdzonych bankiem drzew — bierze się ręcznie,
bo `_slot_role` w `olski/corpus.py` czyta z pola `tfw` dwie role olskiego,
a rama czasownika stoi w tym polu cała.
Ruchem jest zejście po wybranym drzewie do węzłów `zdanie`,
wzięcie lematu głowy i pozycji fraz wymaganych obok niej,
i porównanie tego z `WALENCJA` w `olski/subset.py`.
Do rozstrzygnięcia jest, co taki przebieg drukuje:
sama niezgodność jest liczbą, a pożytek z niej ma dopiero ten,
kto widzi lemat, zdanie i pozycję, o którą poszło.
Do rozstrzygnięcia jest też, czy to jest flaga `olski-corpus`,
czy komenda obok niej, bo tamta mierzy gramatykę, a ta leksykon.
Zdejmuje to zarazem pytanie, którego dziś nikt nie zadaje po zmianie w
`olski/walenty.py`: czy nowe czytanie Walentego dalej zgadza się z bankiem.

Warstwa rozstrzygająca nie dostaje pytania o synkretyzm, choć pomiar tę klasę liczy.
`pytania` w `olski/wieloznaczność.py` wypuszcza same `Przyłączenie`,
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

Świadek ramowy jest wyceniony i wchodzi połową: rzeczownikiem, a nie czasownikiem.
`olski/rozstrzyganie.py` obiecuje w docstringu świadka, który wskazuje gospodarza wtedy,
gdy schemat jednej ze stron tej frazy żąda, i jest to obietnica niedotrzymana,
bo `olski/leksykon.txt` mówi o bierniku i o bezokoliczniku, a fraza sporna jest przyimkowa.
`sonda/rama.py` mierzy to kryterium nad Walentym i bankiem drzew, nie ruszając leksykonu,
a rozstrzyga o ruchu strona: rama rzeczownika myli się rzadziej niż raz na dwadzieścia
odpowiedzi, a rama czasownika tyle, ile rzut monetą, przy dwa razy większym zasięgu
([`docs/disambiguation.md`](docs/disambiguation.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)).
Ruchem jest wobec tego `olski/walenty.py` czytający pozycje `prepnp`
z pliku rzeczownikowego Walentego i wypisujący je do leksykonu kolumną,
której ten plik jeszcze nie ma, a potem świadek pytający o samego gospodarza imiennego
i postawiony przed `Skłonność` w `domyślni`, bo dowód słownikowy bije statystyczny.
Do rozstrzygnięcia jest, czym ma być kolumna dla lematu, którego rama żąda dwóch przyimków,
bo dotychczasowe kolumny są zdaniami prawda-fałsz, a ta jest zbiorem.
Do przeczytania jest `zdania` w `olski/walenty.py`, czyli miejsce, w którym wpis
o samej ramie domyślnej nie wchodzi do pliku,
oraz dwanaście odpowiedzi, które ta sonda wypisuje:
trafność wzięta nad bankiem drzew nie mówi, czy powód da się pokazać autorowi.
`przyimki` w `sonda/rama.py` jest przy tym tym samym pytaniem, które generator zada,
i stoi w sondzie tylko dlatego, że sonda jest dziś jedynym pytającym,
więc razem z kolumną przenosi się do `olski/walenty.py`, obok `pozycje` i `schematy`,
skąd ta sonda bierze już resztę. Dwie kopie tego kryterium rozeszłyby się cicho,
bo rozejście widać dopiero w liczbach, a nie w wydruku.
Regeneracja leksykonu i przeliczenie
[tabeli świadka](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)
idą razem z tym wpisem.
Po stronie czasownika ruchu nie ma i odmowa jest wyceniona:
kryterium myli się tam na braku ramy, a nie na ramie,
bo schemat czasownika pasuje do okolicznika, o którym nie mówi nic.
Zwężeniem, które warto przy tym zmierzyć, jest przypadek grupy pod przyimkiem —
`prepnp(o,loc)` obok `prepnp(o,acc)` — czego `Attachment` w `olski/attachment.py` nie wydaje,
więc sonda pyta dziś o sam przyimek i jej zasięg jest oszacowaniem górnym.

Świadek kontekstowy nie ma zmierzonej trafności, a odpowiedzi do przeczytania ma siedemnaście.
`sonda/powtórzenie.py` nad korpusem audytowym dostaje od niego 7 wskazań w granicy
akapitu i 130 bez niej, a przeczytane ręką jest siedem pierwszych i dziesięć
rozrzuconych po pozostałych
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)),
czyli odczyt, a nie stopa pomyłek: nad 1 113 pozycjami siedemnaście sądów nie jest częstością.
Wzorzec, przy którym byłaby, jest dwojaki i oba są cudzą robotą.
`próba/wybory.txt` daje trzydzieści sądów, a wskazania tego świadka są w nich dwa,
i losowanie go nie dosięga z żadnej strony: nad 1 113 pozycjami odzywa się siedem razy,
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

`_grupa` w `olski/wieloznaczność.py` przedłuża łańcuch imienny przez orzeczenie,
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
mianownikiem jest cała populacja pozycji, którą drukuje `python3 -m sonda.powtórzenie`
([`docs/disambiguation.md`](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)).
Ten sam warunek czyta `_łańcuch` w `olski/rozstrzyganie.py`, bo kryterium jest jedno,
a tam urwanie łańcucha kończy się milczeniem, nie pomyłką, więc cena jest inna po obu stronach.

`KOPULY` w `olski/rozstrzyganie.py` jest listą pożyczoną i cztery piąte jej nie zmierzono.
Świadek kontekstowy nie bierze za dowód powtórzenia przy kopuli, a listę kopul bierze
z gramatyki, gdzie kryterium jest inne: `KOPULA` w `olski/subset.py` wylicza czasowniki
biorące orzecznik w narzędniku, a tutaj chodzi o czasownik, przy którym okolicznik stoi
bez związku z rzeczą. Nad korpusem audytowym rozstrzyga to samo `być`, a `zostać`, `zostawać`, `pozostać`
i `pozostawać` ruszają wyłącznie wariant sondy pytający o cały prefiks zdania,
gdzie zdjęcie takiego dowodu odsłania gospodarza zasłoniętego przez kopulę.
Liczbę tę daje `Powtórzenie(kopuly=frozenset({"być"}))` puszczone przez
`przebieg` w `sonda/powtórzenie.py` obok listy pełnej: wiersze wypuszczany,
bez granicy akapitu i „sąsiad bezpośredni” wychodzą wtedy identyczne,
a „cały prefiks zdania” schodzi ze 126 na 124.
Do przeczytania jest, czy dowód przy `zostać` w stronie biernej mówi coś o rzeczy:
`obiekt zostanie przyjęty do bazy RIT` niesie treść w imiesłowie, a nie w czasowniku,
więc gospodarzem bywa tam imiesłów i wtedy zdjęcie lematu `zostać` niczego nie kosztuje.
Ruchem po tym czytaniu jest albo lista własna w tym module wraz z jej uzasadnieniem,
albo zdanie w `KOPULA`, że obie strony pytają o czasownik bez własnej treści.
Rozstrzygnąć to znaczy wybrać między jedną listą o dwóch kryteriach a dwiema listami,
które rozjadą się przy pierwszym lemacie dopisanym po jednej stronie.

Trafność warstwy nad werdyktami mierzy się na materiale, który tabela widziała.
`sonda/wskazania.py` puszcza świadków z `domyślni`, czyli z
`olski/skłonności.txt`, a ten plik powstaje z całej Składnicy, po której ten
przebieg idzie, więc 96,1% spod
[tabeli nad werdyktami](docs/disambiguation.md#werdykt-pyta-warstwę-o-inny-wybór-niż-bank-drzew)
jest sufitem, a nie pomiarem.
Ruchem jest podział taki, jaki ma już `oceń` w `olski/rozstrzyganie.py`:
tabela z połowy plików o numerze parzystym, przebieg po nieparzystych,
czyli flaga podająca sondzie świadków zbudowanych z tamtej połowy zamiast z pliku.
Do rozstrzygnięcia jest, czy zasięg liczyć wtedy na tej samej połowie:
tabela z połowy korpusu ma mniej par, więc zasięg spadnie razem z trafnością,
a te dwie liczby dziś nie pochodzą z jednego przebiegu i po tym ruchu pochodziłyby.
Do przeczytania jest przy tym `KAWAŁEK` w `olski/coverage.py`,
bo podział na kawałki idzie po plikach i musi minąć się z podziałem na połowy.

Wzorca nie ma dla 184 z 695 przyłączeń, a dwie kategorie Składnicy to tłumaczą.
`dokąd_doszły` w `sonda/wskazaniach` bierze z drzewa te wyrażenia, którym
`_dokąd_doszło` w `olski/attachment.py` daje `noun` albo `clause`, a `Auta są
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

Stopa pomyłek warstwy jest zmierzona na 29 odpowiedziach i tyle nie odróżnia
rejestru od banku drzew, więc
[druga połowa hipotezy](docs/disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza)
zostaje nierozstrzygnięta; liczby trzyma
[częstość nad dokumentacją](docs/disambiguation.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania).
Ruchem jest `python3 -m sonda.wybory --zbuduj proza/ --z-odpowiedzią` na większe `--ile`
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
`python3 -m olski.rozstrzyganie <Składnica> --oceń` wypisuje zasięg i trafność
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
niż daje dzisiejsze `pytania` w `olski/wieloznaczność.py`, więc ta sama komenda z `--ile 30`
dzieli z tym plikiem dwa zdania z trzydziestu
([tamże](docs/disambiguation.md#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów)).
Sądów to nie unieważnia, bo zdanie i fraza stoją we wpisie w całości,
a psuje powiększanie: `rozrzucona` w `olski/próbka.py` bierze co którąś pozycję,
więc próba większa jest siatką przerysowaną od zera, a nie tą siatką z wpisami między nimi.
Ruchem jest jedno z dwojga: albo przerysowanie siatki wraz z przeczytaniem tych wpisów,
które na nią nie trafiły, albo `--zbuduj` z pominięciem pozycji już przeczytanych,
co daje próbę o rozkładzie zszytym z dwóch populacji i mianownik trzeba wtedy nazwać.
Do przeczytania jest, ile z trzydziestu sądów pierwsza droga każe wziąć drugi raz,
bo od tego zależy, która jest tańsza.
Tego samego rozstrzygnięcia żąda `próba/wybory-z-odpowiedzią.txt`, i ostrzej,
bo tam populację rusza każda zmiana w warstwie, a nie tylko zmiana w szukaczu pozycji.

Leksykon walencyjny mówi o bierniku i o bezokoliczniku, a o przypadkach nie mówi.
Narzędnika [przekład](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)
nie bierze, bo `inst` jest u olskiego pozycją orzecznika,
a Walenty nie odróżnia jej od argumentu narzędnikowego,
więc kopula zostaje listą pisaną ręcznie w `olski/subset.py`.
Do przeczytania jest, czy bank drzew tę różnicę widzi:
pozycja `adjp(pred)` stoi w polu `tfw` obok `np(inst)`,
a `olski/corpus.py` czyta dziś z tego pola podmiot i dopełnienie.
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
[`docs/subset.md`](docs/subset.md#dwa-szersze-kryteria-zmierzono-i-żadne-nie-stoi).
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
Ten sam sąd niesie wpis o zaimku wykluczonym ze słownika,
bo oba pytają, co wykluczeniu w `admissible` wolno powiedzieć,
więc rozstrzyga je jedna sesja, a nie dwie.
Zdanie to jest przy tym warunkiem pod
[kierunkiem toru](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę),
bo czytanie, którego polszczyzna nie ma, jest dokładnie tym,
czego werdykt meldować nie powinien.

Wykluczenie ze słownika nie sięga po zaimek, a `go` jest grą.
`CLOSED_CLASS` w `olski/subset.py` wylicza siedem klas zamkniętych,
od przyimka po wykrzyknik, a zaimka wśród nich nie ma,
więc `admissible` zostawia formie `go` czytanie `subst` obok `ppron3`,
choć jest ono nieodmienne dokładnie tak jak nuta,
której to samo wykluczenie odmawia
([`docs/subset.md`](docs/subset.md#the-dictionary-offers-readings-polish-does-not)).
Tam, gdzie oba czytania dają jeden kształt, nie kosztuje to nic,
bo [czytanie jest kształtem](docs/subset.md#co-się-liczy-jako-jedno-czytanie),
i tak wychodzą trzy z sześciu zdań, które tamta sekcja liczy.
Zostaje to, gdzie kształty się różnią,
czyli produkcja dająca głowie grupy imiennej dopełniacz po niej:
zaimka jako głowy ta produkcja nie bierze, a rzeczownik bierze.
Kosztuje to już jedną figurę i to jest tańsza połowa dowodu.
`olski/wieloznaczność.py` liczy nad korpusem audytowym to, co zostawia
`admissible`, więc para `go` i `gov.pl` wychodzi tam dwiema grupami imiennymi,
a udział, który stąd rośnie, cytuje
[`docs/open-questions.md`](docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
jako miękką z dwóch swoich liczb.
Do przeczytania zostaje to, czy takie zdanie kosztuje także werdykt,
bo dopiero ono mówi, czy jest tu co naprawiać w gramatyce;
przebieg nad Składnicą, który to pokaże, jest tym samym,
którym mierzy się cenę
[dwóch szerszych kryteriów](docs/subset.md#dwa-szersze-kryteria-zmierzono-i-żadne-nie-stoi),
czyli liczbą lasów tracących czytanie wybrane przez anotatorów.
Ruchem, gdyby było, jest `ppron3` i `ppron12` dopisane do `CLOSED_CLASS`.
Przeciw: zaimek nie jest wyrazem funkcyjnym w tym sensie, w którym są nim tamte,
a kryterium rozszerzone na niego przestaje mówić to, co mówi dziś.

Maskowanie nieciągłości zmierzono nad Składnicą, a nad rejestrem docelowym nie,
i korpus prasowy zaniża tę liczbę względem dokumentacji, zamiast ją zawyżać,
czym różni się od pozostałych liczb tamtej sekcji.
[Sekcja](docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
wywodzi tę klasę z rzeczownika,
który wybiera ten sam przyimek co rama czasownika przed nim —
`dziadek do orzechów`, `maszyna do szycia` —
a dokumentacja techniczna tak właśnie nazywa swoje narzędzia,
więc `narzędzie do podpisu` czy `moduł do fakturowania` są tam budulcem.
Ruchem jest trzecia pozycja dopisana do `olski/wieloznaczność.py`,
który dwie takie liczy nad korpusem audytowym i ma na to całą maszynerię:
rzeczownik, forma osobowa, a za nią przyimek, który ten rzeczownik bierze.
Do przeczytania jest najpierw to, skąd wziąć ostatni warunek,
bo `olski/leksykon.txt` ma ramy czasowników i nic o przyimku przy rzeczowniku,
a `olski/walenty.py` bierze z Walentego tylko je.
Bez tego pozycja liczy się z listy pisanej ręcznie
i jest warta tyle, co ta lista,
czyli mniej niż dwie pozycje, obok których by stanęła.

Nie wiadomo, ile zdań przyjętych opiera się na czytaniu,
którego polszczyzna nie ma.
Nad rejestrem ustaw widać dwa takie z 69 na jednej klasie i jedno na drugiej
([`docs/ustawy.md`](docs/ustawy.md#co-gramatyka-z-tego-wyprowadza)),
a przeczytano je okiem, nie policzono:
`Kalisz.` wyprowadza się jako czasownik, a `Polski Czerwony Krzyż` jako nazwisko
nieodmienne, czyli forma zgodna z każdą liczbą naraz.
Zdanie przyjęte na takim czytaniu jest gorsze niż odrzucone,
bo pokrycie liczy je jak zdanie przeczytane, a
[wykluczenie ze słownika](docs/subset.md#the-dictionary-offers-readings-polish-does-not)
po nie nie sięga: żąda ono, żeby forma miała obok czytanie z klasy zamkniętej.
Do przeczytania jest `admissible` w `olski/subset.py` wraz z tym wykluczeniem
i z [pomiarem jego ceny](docs/corpus.md#what-morphological-ambiguity-costs),
bo to on mówi, co dzisiejsze kryterium zdejmuje i za ile.
Ruchem jest liczba: ile zdań przyjętych każdego korpusu traci czytanie,
gdy zdjąć czytania nieodmienne wszędzie, a nie tylko przy klasie zamkniętej.
Dopóki jej nie ma, nie wiadomo, czy szersze kryterium jest zakupem, czy stratą,
bo [dwa szersze zmierzono i oba brały za dużo](docs/subset.md#dwa-szersze-kryteria-zmierzono-i-żadne-nie-stoi).

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
Ruchem jest sonda obok `sonda/przecinek.py`, która te warianty buduje i drukuje,
wraz ze zdaniem w obu dokumentach mówiącym, że figury bierze się nią.
Sonda zdejmuje z tych figur najdroższą pozycję:
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

Trzy pozycje, których `README.py` zażądał i nie dostał, stoją każda w innym miejscu.
Lematu `olski` Morfeusz nie zna wcale i czyta go jako `ign`,
więc nazwa własna tego języka nie stanie w zdaniu w żadnej roli,
a obejść tego nie ma czym: `olski/skład/leksemy.py` wybiera między leksemami,
które SGJP ma, i sam mówi, że leksem nieznany nie ma ani jednej formy.
Liczebnika nie ma `olski/skład/składnia.py`, więc `jedno czytanie` z drzewa nie wyjdzie,
i jest to ta sama konstrukcja, którą gramatyka po drugiej stronie już ma
([`docs/subset.md`](docs/subset.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)),
czyli tor składu jest tu za nią, a nie przed.
Relacja `przyczyna` nie ma w `olski/skład/przyimki.py` wpisu pod żadnym przyimkiem,
a ma wpis w `olski/skład/spójniki.py`, więc wychodzi zdaniem i nie wychodzi frazą:
`Dlaczego.bo(zdarzenie)` składa się, a `Dlaczego.dla(rzecz)` zgłasza `PozaRamą`.
Jest to jedyna z tych trzech pozycji, przy której skład ma pół konstrukcji, a nie zero.
Do przeczytania przy niej jest ten leksykon obok
`tests/test_przyimki.py`, który świadkuje przypadkom, a nie doborowi relacji.

Słownika własnego nie ma w tym repozytorium ani jeden kierunek,
więc słowa, którego SGJP nie ma, nie powie ani skład, ani gramatyka.
`olski/skład/leksemy.py` wybiera między leksemami, które słownik ma,
a `olski/morph.py` prosi Morfeusza wprost, żeby nieznanej formy nie zgadywał.
Mechanizm ma sam Morfeusz i jest nim `dict_name` albo `dict_path`,
czyli słownik skompilowany jego własnym narzędziem obok tego, który przychodzi z paczki.
Rozstrzygnąć trzeba jednak nie to, jak, a czy:
słownik dopisany po tej stronie czyni repozytorium drugim źródłem prawdy o polszczyźnie,
a po tamtej jest zmianą w języku, bo zdanie z nowym słowem zaczyna się wyprowadzać,
i wtedy wchodzi jej cena w werdyktach, tak samo jak przy dopisanej produkcji.
Rozdzielić te dwie strony wolno: skład potrzebuje samej syntezy nazwy własnej,
a gramatyka nie potrzebuje jej wcale, więc wpis po jednej stronie
nie żąda wpisu po drugiej, i to jest pierwsza rzecz do przeczytania.
Do przeczytania jest przy tym, czym `dict_path` płaci przy instalacji:
paczka bierze Morfeusza z PyPI ([`CLAUDE.md`](CLAUDE.md#checks)),
a kompilator słownika nie jest tym, co ta paczka niesie.

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

`Zdanie.podmioty` w `olski/skład/składnia.py` schodzi pod konstytuent na dwa poziomy,
czyli tam, gdzie sięga `_wskazany`, a zdanie podrzędne stoi czasem głębiej:
`Mysz goniła ogon myszy, która spała.` ma dwa podmioty, a widać stąd jeden.
Kosztuje to opuszczenie postawione tam, gdzie czytelnik trafia na dwie rzeczy
wyciągające z czasownika jedną formę, czyli dokładnie to, przed czym ten warunek broni.
Do przeczytania jest `_zdania_pod` wraz z `_wskazany` w tym samym pliku,
bo schodzą tak samo głęboko i tylko jednej z nich to wystarcza:
tamta pyta, skąd zaimek wyjdzie na czoło, a ta, na kogo czytelnik trafi.
Ruchem jest zejście po całym drzewie roli zamiast po dwóch jego poziomach,
i jest ono tańsze niż tamto, bo nie ma z niego nic do wyprowadzenia.

Rama czasownika, o którą pyta `Robi` w `olski/skład/składnia.py`,
odpowiada na trzy pytania z listy: o biernik, o bezokolicznik i o zdanie podrzędne,
więc rola w przypadku innym nie ma po tej stronie o co zapytać
i nie ma jak stanąć w drzewie.
Kosztuje to trzy klasy zdań, a wszystkich trzech chciała druga wersja legendy,
trzecia poprosiła o dwie z nich znowu i wszystkie trzy z niej wypadły.
`Czeladnik nie powiedział nikomu.` żąda celownika,
`Czeladnik szukał córki krawca.` żąda dopełniacza,
i to drugie `Robi` odrzuca, bo leksykon `szukać` wymienia jako czasownik bez biernika,
czyli mówi o nim prawdę i mówi ją w jedyny sposób, jaki ma.
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
Do przeczytania jest `olski/walenty.py` wraz z tym,
co [`docs/subset.md`](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)
mówi o tym, co ten przekład z Walentego bierze, a czego nie,
bo Walenty niesie wszystkie te ramy i jest to jedna zmiana po obu stronach.
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
wraz z czwartym zdaniem leksykonu; wpis jest przez to winien
przebieg `olski/walenty.py` oraz poprawkę liczb w
[`docs/subset.md`](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego).

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
`KOPULA` w `olski/subset.py` jest tą częścią walencji, której Walenty nie niesie,
i [`docs/subset.md`](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)
nazywa ją jedynym wpisem leksykonu pisanym ręcznie,
a stoi ona w gramatyce, a nie w `olski/walencja.py`, czyli tam, gdzie leksykon.
Do przeczytania jest ta sekcja wraz z wpisem o narzędniku,
bo ten sam przekład rozstrzyga, czy kopula w ogóle zostaje listą.
Ruchem jest `KOPULA` przeniesiona do `olski/walencja.py`
oraz `Jest` biorące lemat tak, jak bierze go `Robi`,
wraz z odmową dla czasownika, którego ta lista nie wymienia.
Czyta ją stamtąd także `sonda/polszczyzna.py`, więc import idzie razem z nią.

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

Leksykonu projektu nie ma, a rejestr, w którym się pisze, żąda go od obu kierunków:
`komit`, `olski` i `lintować` dostają z SGJP `ign`,
więc synteza nie ma czego wypuścić, a analiza czyta formę, której nie zna.
Osobno stoi leksem, którego słownik nie ma, choć napis zna:
projekt piszący o agentach jako o programach żąda liczby mnogiej `agenty`,
a `agenty` z SGJP jest formą deprecjatywną leksemu osobowego,
czyli czym innym niż liczba mnoga rzeczy nieżywotnej.
Do przeczytania jest to, co
[`docs/sklad.md`](docs/sklad.md#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr)
mówi o cenie słownika dołożonego Morfeuszowi i o tym, co wpis ma nazywać,
wraz z `olski/leksykon.txt` i `olski/skład/leksemy.py`, czyli dwoma leksykonami,
które już stoją, a żaden z nich na to pytanie nie odpowiada.
Ruchem jest rozstrzygnięcie, czy wpis wypisuje formy,
czy wskazuje leksem, wedle którego się odmienia,
a po nim plik z wpisami na te słowa, których to repozytorium używa o sobie.
Drugą z tych dróg widać już na `olski/skład/leksemy.py`, ale tylko połowę:
wpis wskazuje tam leksem, który słownik ma,
a tutaj trzeba wskazać leksem, wedle którego odmienia się słowo,
którego słownik nie ma wcale.

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
Do przeczytania jest, co `olski/walenty.py` bierze z Walentego przy pozycji `infp`,
bo pytanie jest o to, czy słownik tego lematu z bezokolicznikiem nie ma,
czy ma go w kształcie, którego ten przekład nie bierze,
wraz z tym, co [`docs/subset.md`](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)
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
wraz z [ceną liczebnika](docs/subset.md#liczebnik-zmierzono-i-nie-odbiera-ani-jednego-zdania),
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
Do przeczytania jest to, co `olski/walenty.py` bierze z Walentego,
bo słownik ten aspekt przy pozycji `infp` wypisuje,
oraz `bierze_bezokolicznik` w `olski/walencja.py`, czyli zdanie, które to pytanie zadaje.
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

## Pakiet, instalacja i testy

The repository ships no licence.
`pyproject.toml` carries no `license` field and there is no `LICENSE` file,
so the terms under which any of this may be used are unstated.
The move is to pick one, add the file,
and set `license` in `pyproject.toml` to match.
Reading a GPL v3 parser of Polish is what raised it
(see [`docs/swigra.md`](docs/swigra.md#why-wrapping-it-does-not-get-there)),
and the answer decides whether olski could ever link against such a thing.

Granica harnessu jest napisana raz, a stosuje się dwa razy inaczej.
`harness/__init__.py` mówi, że korpus w formacie znacznikowym
dochodzi do gramatyki tędy, a nie przez `olski`,
a `harness/endings.py` dokłada, że stoi tam,
bo o polszczyźnie niczego nie twierdzi.
Oba kryteria trafiają w `olski/corpus.py`, który czyta XML Składnicy,
w `olski/coverage.py`, który mierzy nim gramatykę
i produkuje tabele [`docs/corpus.md`](docs/corpus.md),
oraz w `olski/attachment.py`, który mierzy nim sam korpus
i produkuje tabelę
[`docs/subset.md`](docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia).
Trzeci z nich jest przy tym przypadkiem najostrzejszym,
bo o gramatyce nie mówi nic, tak samo jak `harness/endings.py`.
Czwarty pokazuje, że samo kryterium jest za grube:
`olski/wieloznaczność.py` też o gramatyce nie mówi nic
i mimo to do `harness/` nie pójdzie,
bo liczy przez `admissible` i przez leksykon walencyjny,
czyli przez dwie decyzje toru gramatycznego naraz.
Trzy z tych czterech są liśćmi,
a czwarty odbiera `olski/attachment.py` bycie liściem, importując go,
i wszystkie instalują się z pakietem
(`include = ["olski*"]` w `pyproject.toml`),
a jeden ma własną komendę,
gdzie tak samo pomiarowe programy w `harness/`
nie mają ani instalacji, ani komendy.
Ruchem jest rozstrzygnięcie granicy, a nie przeniesienie plików:
albo obie idą do `harness/`, a `olski-corpus` staje się
`python3 -m harness.coverage` jak dwie pozostałe komendy pomiarowe,
co przepisuje polecenia w [`docs/corpus.md`](docs/corpus.md#fetching-it)
oraz w figurach `korpus` i `korpus-żywa` w [`harness/figury.py`](harness/figury.py),
a wraz z nimi wydruki, które te figury zapisały,
albo `harness/__init__.py` mówi, czym granica jest,
co nie kosztuje nic i przestaje odpowiadać dwa razy.
Do przeczytania jest to, co pakiet ma dawać temu, kto go instaluje:
czytnik banku drzew i trzy programy pomiarowe są w nim,
a kto sprawdza zdanie gramatyką, żadnego z nich nie woła.

Pomijania testów bez Morfeusza nie pilnuje nic, a raz już się rozeszło.
[Sekcja Checks](CLAUDE.md#checks) mówi, że plik testowy sięgający analizatora
pomija się zamiast wywracać zbiórkę,
a sięgnąć go można nie wypisując go ani razu:
`olski/subset.py` ciągnie `olski/morph.py`,
gdzie `import morfeusz2` stoi na górze pliku.
Linię tę mają dziś wszystkie pliki, które tam dochodzą,
a własności, którą ona przywraca, nie pilnuje nic:
przebieg z Morfeuszem przechodzi tak samo z nią i bez niej,
więc rozejście widać wyłącznie w tym stanie, w który wchodzi się bokiem,
a opisuje go wpis o `morfeusz2` w `dependencies`.
Ruchem jest test czytający pliki z `tests/`:
ten, którego import dochodzi do `olski/morph.py`,
ma nad tym importem `pytest.importorskip("morfeusz2")`.
Do rozstrzygnięcia jest, czy liczyć import wypisany w pliku,
czy to, dokąd on dochodzi:
`tests/test_ruch.py` sięga analizatora przez dwa moduły i ani razu go nie nazywa,
a `tests/test_endings.py` nie sięga go wcale,
choć nazywa `harness/endings.py`, który woła `morfeusz2` dopiero w `main`.
