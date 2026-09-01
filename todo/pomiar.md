# Pomiar pokrycia

Kolejność czytań zmierzono nad cudzym rejestrem i tylko nad nim.
Koszt produkcji i późne domknięcie wyceniono złotym czytaniem Składnicy
([`docs/disambiguation.md`](../docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie)),
a rejestr, do którego olski celuje, nie mówi o kolejności nic,
choć to w nim czytelnik ogląda czytanie pierwsze.
Wzorzec na to jest jeden i już stoi: `próba/wybory.txt` nazywa ręką gospodarza,
o którego w danym zdaniu korpusu audytowego chodziło (`harness/wybory.py`).
Ruchem jest pytanie tamtego pliku o co innego niż warstwa rozstrzygająca:
czy czytanie pierwsze obsadza tego gospodarza, którego nazwał czytający.
Mianownik jest tam mały i to jest cena, którą ten pomiar płaci za rejestr,
a liczba mówi, czy dzisiejsze koszty są dobrane pod Składnicę,
czy pod dokumentację techniczną.

Kosztu morfologii nie widzi ani jeden pomiar nad bankiem drzew.
`harness/czytania.py` mierzy złote czytanie morfologią złotą, czyli czytaniem
wziętym z drzewa wzorcowego, a `_segment` w `harness/corpus.py` buduje je bez
kwalifikatorów, więc koszt ten wychodzi nad Składnicą zerem przy każdej formie
i cały wydruk jest ten sam co bez niego, co do wiersza.
Zielony przebieg nie mówi tam przez to nic — dokładnie tak, jak nie mówi nic
przebieg bez Morfeusza ([`CLAUDE.md`](../CLAUDE.md#checks)).
Ruchem jest `--morphology` w `harness/czytania.py`, którą ma już `harness/pomiar.py`,
a decyzją, którą to wymusza, jak dopasować drzewo wzorcowe do morfologii żywej:
pod nią parser numeruje pozycje znakami, a nie terminalami drzewa
(`Raport` w `harness/pomiar.py`), więc rola z drzewa nie trafia w rozpiętość lasu.
Na czym wycena tego kosztu stoi bez tej liczby, mówi
[`docs/disambiguation.md`](../docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie).

Wiersz zdań bez struktury nad całością ma nad Składnicą przeszło tysiąc zdań
i przeczytana jest z nich garść.
Nazywa on zdarzenie, a nie konstrukcję — analiza wzięła każdą formę zdania
i nie domknęła całości
([`docs/corpus.md`](../docs/corpus.md#where-the-analyses-stop)) —
więc mówi, gdzie szukać, a nie czego brakuje.
Nagłówek bez czasownika, `Na próżno.` czy `Najpospolitszy.`, jest w nim mniejszością,
a większość tych zdań niesie formę czasownikową,
czyli brakuje w nich czegoś nad czasownikiem, a nie samego czasownika.
Ruchem jest odczytanie tej resztki i rozbicie jej na klasy,
z tego klasy nazwane w [`docs/subset.md`](../docs/subset.md#what-it-does-not-cover-yet),
jeśli któraś jest konstrukcją, a nie zbiegiem okoliczności.
Do przeczytania jest ta resztka pod obiema morfologiami:
pod żywą wpada do niej także forma, której wykluczenie zabrało wszystkie czytania,
a tę drugą klasę trzyma wpis o wycięciu czytań bez licencji przed rozbiorem.

Luka jest węzłem o pustej rozpiętości, więc rola wypełniona przez nią nie ma nazwy,
i na tym stanął pomiar cechy przeciąganej
([`docs/design-notes.md`](../docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
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
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)),
więc pytanie, czy niesie ją produkcja, czy porównanie ról, ma tu odpowiedź z precedensu,
a wariant z luką tamtych ciał nie ma i musi ją postawić po swojemu:
`rdzeń_względny` składa tam zaimek ze zdaniem,
któremu brakuje dokładnie tego, czym on jest,
więc etykieta ma stanąć nad zaimkiem w tej jednej produkcji.
Do przeczytania jest przy tym `Node.span` w `olski/parse/czytanie.py`,
bo pole to wpisano pod produkcję o pustym ciele, a ta sonda jest jego pierwszym czytelnikiem.
Nie zamyka tego wpisu cała cena: warunek precedencji na lukę pilnuje pozycji w ciele,
a nie w napisie, więc zdanie zagnieżdżone dalej wychodzi dwoma kształtami.
Rozdzielenie dominacji od precedencji tej reszty nie zamknęło i zamknąć nie mogło:
rozwinięcie mówi o kolejności córek w ciele, czyli o tym samym, o czym mówi luka dziś
([`docs/subset.md`](../docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
a warunek pytany o rozpiętości musiałby stanąć w lesie, gdzie `_przejdź`
w `olski/parse/las.py` dostaje ciało wraz z rozpiętościami córek.
Wpis jest przez to o warunek sprawdzany po rozbiorze, a nie o preprocesor przed nim.
Odbiorca takiego warunku jest przy tym jeden i mówi to pomiar, a nie przeoczenie:
tryb w ciągu współrzędnym i zagnieżdżenie liczebnika prosiły o tę samą maszynerię,
a oba okazały się cechą albo pozycją nie wartą ceny
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#tryb-przypuszczający-jest-jedną-cząstką)
oraz [tamże](../docs/konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-złożony-przyłącza-się-wedle-ostatniego-członu)).
Luka jest tu ostatnia, bo cechą jej zrobić nie da się wcale,
i dlaczego, mówi
[pakowanie czytań](../docs/parsowanie.md#co-się-pakuje-rozstrzyga-tożsamość-czytania).

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
[`docs/disambiguation.md`](../docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)
wychodzi z `harness.pomiar`, a sonda się kasuje.
Ceną jest to, czego dziś ten przebieg nie liczy:
`różniące`, `przyłączenia` i `rozbieżności` chodzą po lesie osobno,
a `harness.pomiar` puszcza się nad 13 035 zdaniami i pod pulą procesów.
Drugą pozycją ceny jest zatrzymanie:
sondy z tej czwórki o nie nie pytają, bo żadna go nie czyta, a `harness.pomiar` pyta,
bo z niego liczy tabelę blokerów,
i nad zdaniem odrzuconym kosztuje ono mniej więcej drugi rozbiór
(`podsumuj` w `olski/parse/`).
Do przeczytania jest więc najpierw, ile ta trójka dokłada do przebiegu,
bo poniżej progu, przy którym to widać, ruch jest samym zdjęciem duplikatu,
a powyżej jest wyborem między dwoma przebiegami a jednym droższym.
Do przeczytania jest przy tym `Raport.record` w `olski/pokrycie.py`,
gdzie licznik klas musiałby stanąć, oraz `KAWAŁEK` w `harness/pomiar.py`,
bo przez granicę procesu idzie licznik, a nie las.

Porównanie ról liczy za niezgodność i czytanie dobre, i czytanie złe,
kiedy drzewo wzorcowe nie znaczy w tym miejscu żadnego gniazda.
`Outcome.agreement` w `harness/pomiar.py` pyta o rozpiętości roli po obu stronach,
a rolę przypisaną tam, gdzie gold ma zbiór pusty, liczy jako `disagrees`,
więc `Powtarzaj je tak często, jak to jest potrzebne.` — gdzie wybrane drzewo
dopełnienia rozkaźnika nie znaczy wcale — stoi w tym wierszu obok
`Poprzednio pracodawca mógł z tym zwlekać nawet 15 lat.`,
gdzie olski czyta okolicznik czasu jako dopełnienie i myli się naprawdę
([`docs/corpus.md`](../docs/corpus.md#agreement-which-matters-more-than-acceptance)).
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
Przyczynę tego jednego czytania nieprawdziwego widać przy tym bez korpusu,
na parze zdań, i jest nią brak pozycji, a nie sama nazwa roli:
`Czekał godzinę.` wychodzi z `dopełnienie: godzinę`, bo `czekać` nie ma w
`olski/leksykon.txt` wykluczenia biernika, więc okolicznik czasu wchodzi na
pozycję dopełnienia, a `Spał całą noc.` jest odrzucone, bo `spać` to wykluczenie
ma i biernikowi nie zostaje w tym zdaniu żadna pozycja.
Gramatyka nie ma więc okolicznika w bierniku wcale,
a wpuszczenie go jest osobnym ruchem wraz z pomiarem.

Rankingu form bez licencji nad dokumentem nie wypisuje nikt.
`olski-check` mówi o zdaniu, a nie o pliku, więc formy, po które nie sięga
ani jedna produkcja, widać po jednej naraz i tylko w werdykcie, który je wypisał
(`bez_licencji` w `olski/segmentacja.py`).
Kolejka blokerów odpowiada na inne pytanie, bo grupuje po części mowy zatrzymania,
a forma bez licencji zatrzymania nie musi wywołać.
Czytelników takiego rankingu jest już dwóch:
[kolejka nad rejestrem ustaw](../docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
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
A point on [the coverage curve](../docs/design-notes.md#making-the-trade-measurable)
is a net of what an addition buys against what it costs in uniqueness
([`docs/roadmap.md`](../docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
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
[`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi)
is an exclusion measured this way,
and each was measured with a probe written for the one session that priced it.

`harness/polszczyzna.py` jest drugą deklaracją podzbioru,
który deklaruje `olski/subset/`,
czyli tym drugim właścicielem faktu, przed którym broni
[`CLAUDE.md`](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely),
i pilnuje jej tylko siedem zdań z `tests/test_sonda.py`.
Te dwie deklaracje rozeszły się na koordynacji przecinkiem
— olski bierze przecinek na pięciu poziomach, a sonda spójnik —
i drugi raz na podrzędności, której sonda nie ma wcale,
a nad prozą README nie widać po żadnej liczbie ani jednego z tych rozejść.
Trzecie rozejście jest grupą liczebnikową:
`Działają dwie rzeczy.` olski wyprowadza jednym czytaniem, a sonda odrzuca.
README tego zdania nie ma, więc liczba zdań zgodnych rozejścia nie pokazuje,
a same opisy różnią się dalej
([`docs/design-notes.md`](../docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)).
Czwarte przyszło z interpunkcją zdaniową i tą samą liczbą się pokazuje,
przez co jest dowodem, że kopia starzeje się przy każdej produkcji:
dwa zdania README olski wyprowadza od tej pory, a sonda odrzuca oba,
bo dwukropka ani przecinka przed spójnikiem nie ma po tamtej stronie.
Piąte przyszło z okolicznikiem narzędnikowym i zabrało tej kopii zdanie,
którym mierzyła współrzędność: `Zobacz docs/design-notes.md oraz docs/roadmap.md.`
wychodzi u olskiego wieloznaczne, bo notacja czyta się nieodmiennie
i staje przez to także w tym okoliczniku, a sonda tej pozycji nie ma
([`docs/konstrukcje-gramatyczne/okolicznik.md`](../docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Póki liczby z niej cokolwiek trzymają, kopia zarabia na siebie.
Wpis czekał na to, aż szyk zejdzie do warunków precedencji,
i tamten ruch jest zrobiony
([`docs/subset.md`](../docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
więc kopia trzyma odtąd samą liczbę zdań zgodnych,
czyli to, co po każdej produkcji mówi coraz mniej o różnicy dwóch formalizmów,
a coraz więcej o tym, czego sonda nie ma.
Ruchem jest wtedy `git rm harness/podłoża.py harness/polszczyzna.py harness/wiezy.py`
wraz z `tests/test_sonda.py`,
wraz z liczbami [tamtej sekcji](../docs/design-notes.md#podłoże-więzowe-zmierzone-sondą).
Zostaje z niej to, co pomiaru nie potrzebuje:
że nieciągłość jest warunkiem zdejmowanym, a nie szczeblem,
i że jednoznaczność bywa osiągana bez trafności.
Kasowanie zabiera przy tym jedyny mechanizm w repozytorium,
który wypuszcza konstytuent nieciągły:
`spójne` w `harness/wiezy.py` jest warunkiem zdejmowanym,
a produkcja z `olski/subset/` spójności zdjąć nie umie.
Tym warunkiem zmierzono cenę nieciągłości i zamknięto
[rozwidlenie o przestawianiu](../docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
a liczy ją `harness/nieciągłość.py`, czyli trzeci plik tego katalogu,
który `harness/wiezy.py` i `harness/polszczyzna.py` czyta.
Lista plików wyżej nie obejmuje więc tego, co kasowanie naprawdę zabiera,
a [sekcja o pomiarze](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje) każe tę cenę przeliczać razem z gramatyką.
Ruch dopisuje sobie przez to jedno rozstrzygnięcie:
albo cena nieciągłości przestaje być figurą przeliczaną
i tamta sekcja mówi o niej to, co `docs/firing-rates.md` mówi o sobie,
czyli że jest ceną, przy której decyzja zapadła,
albo podłoże zostaje po to jedno, a kasowanie obejmuje samo porównanie deklaracji.
Rozstrzygnięcie to ma termin, bo liczby tamtej sekcji rozeszły się już z sondą:
werdykty nad zdaniami ze szczeliną, mianownik ceny i liczba zdań tracących
jednoznaczność są w niej inne niż w dzisiejszym przebiegu,
więc kto wpis podnosi, albo je przelicza, albo zdejmuje.

Cenę pozycji, która nie rusza werdyktu, bierze ręka, bo sonda różnicowa liczy werdykty.
Etykieta roli nad wysuniętym czołem nie rusza ani jednego
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)),
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
`ZASTĘPOWANE` w `harness/luka.py` wymienia sam `rdzeń_względny`,
a `_wysunięta_rola` w `olski/subset/podrzędne.py` pisze tym samym kształtem
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
([`docs/design-notes.md`](../docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
Ruchem jest dopisanie do `ZASTĘPOWANE` symboli `rdzeń_pytajny`
oraz `rdzeń_względny_rzeczowny`, a razem z nimi dopisanie
`wyrażenie_przyimkowe_pytajne` i `wyrażenie_przyimkowe_względne_rzeczowne`
do `_wysunięty_okolicznik` w tym samym pliku,
bo pytanie ma dziś czoło przyimkowe tak samo jak zdanie względne
i luki pod nim nie żąda z tego samego powodu.
Wypisywać tych sześciu nazw nie trzeba: `RODZINY` w `olski/subset/deklaracja.py`
zbiera je rodzina po rodzinie, więc oba te miejsca biorą je stamtąd.
Przed jednym i drugim stoi rozstrzygnięcie, czym pytanie lukę wiąże:
zdanie względne wiąże ją zaimkiem, którego liczbę i rodzaj podejmuje poprzednik,
a pytanie poprzednika nie ma, więc te dwie cechy nie mają się z czym zejść.
Wpis jest winien przebiegi, których żąda ta sekcja tamtego dokumentu,
bo rusza w niej każdą liczbę.

Lista w [`docs/pisanie-po-olsku.md`](../docs/pisanie-po-olsku.md#czego-brakuje-najbardziej)
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

Wzorca nie ma dla 184 z 695 przyłączeń, a dwie kategorie Składnicy to tłumaczą.
`dokąd_doszły` w `harness/wskazaniach` bierze z drzewa te wyrażenia, którym
`_dokąd_doszło` w `harness/attachment.py` daje `noun` albo `clause`, a `Auta są
kradzione dla okupu.` przyłącza frazę do węzła imiesłowowego, którego `CLAUSE`
nie wylicza, więc zdanie wypada z mianownika trafności
([tamże](../docs/rozstrzyganie.md#werdykt-pyta-warstwę-o-inny-wybór-niż-bank-drzew)).
Druga jest fraza werbalna z bezokolicznikiem: `Muszę jechać do domu.` przyłącza
frazę dokładnie tam, gdzie stawia ją werdykt, i mimo to wzorca stąd nie ma.
Ruchem jest przeczytanie, które kategorie Składnicy stoją nad imiesłowem
biernym i nad bezokolicznikiem i czy któraś z nich jest dla olskiego zdaniem —
dla werdyktu jest, bo gospodarzem jest tam forma czasownikowa.
Ceną jest to, że `CLAUSE` czyta zarazem
[tabela przyłączeń](../docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia),
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
[druga połowa hipotezy](../docs/disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza)
zostaje nierozstrzygnięta; liczby trzyma
[częstość nad dokumentacją](../docs/rozstrzyganie.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania).
Ruchem jest `python3 -m harness.wybory --zbuduj proza/ --z-odpowiedzią` na większe `--ile`
i przeczytanie tego, co dojdzie; pozycji z odpowiedzią jest w tym korpusie 122,
więc cała populacja mieści się w czterech takich próbach.
Kupuje to przedział, a nie liczbę, i tyle jest tu do kupienia za cztery próby czytane ręką:
przy dzisiejszej stopie wszystkie 122 odpowiedzi dają przedział od 11% do 25%,
czyli mijają co dziesiątą odpowiedź o włos.
Do rozstrzygnięcia jest przy tym, o czym mówi liczba wzięta do końca nad tym korpusem:
pozycje z odpowiedzią pochodzą z dwóch repozytoriów
([`docs/audit-corpus.md`](../docs/audit-corpus.md#the-list)),
więc rejestrem, o którym stopa pomyłek wtedy mówi, są te dwa,
a nie dokumentacja techniczna w ogóle.

Wsparcie dwóch wypadków banku drzew jest nad dokumentacją progiem, przy którym
tabela skłonności myli się częściej, niż trafia:
cztery pomyłki z siedmiu odpowiedzi opartych na tym wsparciu, wobec jednej z 22 powyżej
([częstość nad dokumentacją](../docs/rozstrzyganie.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)).
Ruchem jest `WSPARCIE` w `olski/rozstrzyganie.py` podniesione do trzech,
a przed nim cena po drugiej stronie, bo próg jest punktem na krzywej i tam jest jego właściciel:
`python3 -m harness.skłonności <Składnica> --oceń` wypisuje zasięg i trafność
dla `(3, 0.85)` obok dzisiejszego `(2, 0.85)`, więc liczba jest jednym przebiegiem.
Do przeczytania jest, co robi z trzema trafnymi odpowiedziami spod wsparcia dwóch:
wszystkie trzy są liczebnikiem cząstkowym (`jednego z kilku uprawnień`),
czyli klasą, którą rozstrzyga reguła, a nie częstość,
więc próg podniesiony zabiera odpowiedzi, których tabela i tak nie powinna wydawać.
Zmiana rusza przy tym tabelę nad werdyktami banku drzew, obie próby czytane ręką
i figury w `docs/rozstrzyganie.md`, które je cytują,
a `próbę zawężoną do odpowiedzi` przerysowuje w całości, bo losowanie idzie po odpowiedziach.

Próba wyborów jest losowaniem nad populacją, której `pytania` już nie daje.
Wpisy w `próba/wybory.txt` padły nad populacją mniejszą i przy innej propozycji gospodarza,
niż daje dzisiejsze `pytania` w `harness/wieloznaczność.py`, więc ta sama komenda z `--ile 30`
dzieli z tym plikiem dwa zdania z trzydziestu
([tamże](../docs/rozstrzyganie.md#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów)).
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
[tamtej sekcji](../docs/rozstrzyganie.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)
mówi o tym, co tabela robiła, a nie o tym, co warstwa robi.

Maskowanie nieciągłości zmierzono nad Składnicą, a nad rejestrem docelowym nie,
i korpus prasowy zaniża tę liczbę względem dokumentacji, zamiast ją zawyżać,
czym różni się od pozostałych liczb tamtej sekcji.
[Sekcja](../docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
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
[`docs/ustawy.md`](../docs/ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa),
gdzie grupą są dwa ciała `człon_imienny` z przymiotnikiem i dopełniaczem pod głową,
czyli to z wyrażeniem przyimkowym na końcu i to bez niego.
Przy pozycjach przyłączeniowych granica grupy jest już wypisana
([`docs/subset.md`](../docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)),
a przy [zdaniach, które rama zdejmuje](../docs/corpus.md#what-morphological-ambiguity-costs)
nie jest: liczby odtwarza leksykon z biernikiem dopisanym kopuli,
i dokument tego nie mówi.
Wariantów jest przy tym więcej niż dwa i każdy stawia tę samą pułapkę.
Cena podrzędności żąda gramatyki bez symbolu `zdanie_podrzędne` i bez `comp` w ramie,
a cena zdania względnego — bez produkcji względnych,
przy czym wariant zbudowany przez podmianę `ZAIMEK_PYTAJNO_WZGLĘDNY`
zdejmuje trzy naraz, bo ta stała stoi w wykluczeniu, w terminalu zaimka
i w terminalu grupy pytajnej,
więc sesja mierzy wtedy co innego, niż myśli, i nic jej o tym nie mówi.
Do przeczytania jest ta sekcja wraz z `_klasy` z `olski/subset/rama.py`,
bo ramę zawęża ona i tylko ona.
Ruchem jest predykat nad `harness/ruch.py`, który te warianty buduje i drukuje,
wraz ze zdaniem w obu dokumentach mówiącym, że figury bierze się nim.
Pomiar zdejmuje z tych figur najdroższą pozycję:
zgadywanie, co poprzednia sesja zmierzyła.

Żadna z dwóch kolumn w
[`docs/corpus.md`](../docs/corpus.md#what-morphological-ambiguity-costs)
nie pochodzi od tagera, więc nikt nie policzył, ile z ich różnicy tager odbiera.
Kandydatem jest [Concraft](../docs/prior-art.md#polish-language-resources),
a rozstrzyga o nim jedna własność wyjścia:
czy wybrana interpretacja niesie jedną wartość przypadka, czy dysjunkcję.
`subst:sg:nom.acc:m3` jest w `olski/morph.py` jedną interpretacją z cechą mnogą,
więc tager, który ją wybierze i zostawi `nom.acc`, synkretyzmu nie zdejmuje,
a od synkretyzmu własność jednoznaczności się zaczyna
([`docs/subset.md`](../docs/subset.md#validity-is-uniqueness-not-just-derivability)).
Ruchem jest przebieg Concrafta nad kilkoma zdaniami i odczytanie tego pola.
Trzecia kolumna dopiero po nim, bo Concraft to binarium Haskella
i model stumegabajtowy, czyli zależność pomiaru z fetchem, jak Składnica i Walenty,
a takiej nie warto zaciągać pod przebieg, który nie ruszy ani jednego zdania.
Po stronie złotej morfologii pytanie wygląda na zamknięte:
`terminal` w `tests/test_corpus.py` pisze `subst:sg:nom:m3` z jedną wartością,
a docstring tego pliku ręczy, że format przepisano z wydania z 2018.
Ręczy jedna osoba i żaden plik banku, więc gdyby Concraft wypadł ciekawie,
sprawdź to na wydaniu, zanim trzecia liczba wejdzie do dokumentu.

Nie wiadomo, w ilu miejscach decyzja o konstytuencie jest w olskim ta sama,
co w GFJP, a pomiar nad Składnicą tego nie powie
([`docs/swigra.md`](../docs/swigra.md#którędy-gfjp-wchodzi-do-olskiego) mówi dlaczego).
Ruchem jest przejść listę konstrukcji z [`docs/subset.md`](../docs/subset.md)
obok `gfjp2.dcg` ze `swigra_current.zip`
i wypisać, gdzie obie gramatyki przyłączają tak samo, a gdzie inaczej.
Nie po to, żeby różnić się celowo:
po to, żeby o każdej takiej decyzji dało się powiedzieć, czy jest wyborem.
Do przeczytania jest `gfjp2.dcg` i czyta się go inaczej, niż wygląda:
nazwy nieterminali są tam formalne — `fno`, `fw`, `fl` —
a olski nazywa symbole funkcjami, czyli `podmiot` i `dopełnienie`,
więc porównanie prowadzi to, co produkcja przyjmuje, a nie nazwa symbolu.
Sesja jest osobna i nie dzieli się na pliki,
bo rozstrzyga jedno pytanie na całej liście naraz.

Przydawka imiesłowowa podniosła liczbę zdań, w których przyjęte czytanie
przeczy drzewu wzorcowemu, a przebieg, który to pokazał, nie mówi, czym te zdania są
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik)).
Kierunek żąda od werdyktu prawdy o zdaniu
([`docs/roadmap.md`](../docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
więc pozycja, która kupuje pokrycie i sprzedaje zgodność, żąda odczytania,
a nie samej liczby.
Do przeczytania jest `python3 -m harness.pomiar <korpus> --examples`
w wierszach `disagrees` oraz w tych, którym złote czytanie z lasu wypada,
i pytanie do nich jest jedno: czy pomyłki stoją na jednym kształcie.
Ciała są dwa, po jednym na imiesłów, więc kształt zdejmuje się po jednym
i przelicza obie liczby; sonda różnicowa robi to nad `harness/ruch.py`.
Gdzie pomyłki się rozchodzą, całą zmianą jest zdanie o tym w tamtej sekcji,
bo wtedy cena jest ceną przydawki, a nie jednego z dwóch imiesłowów.

Trzy przykłady w [sekcji o nieciągłości](../docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
mówią o zatrzymaniach, których olski już nie ma: `Co mamy wziąć?` i `To chcę
podkreślić.` stają dziś na bezokoliczniku, a nie na zaimku rzeczownym, więc zdanie
o tym, że wszystkie trzy staną na pierwszym słowie, jest nieprawdziwe — pierwsze
z nich stawało na zaimku, którego pozycji rzeczownej nie ma
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Ruchem jest przebieg nad tamtym zbiorem 323 zdań i przepisanie tych przykładów na
takie, które dziś stają tam, gdzie akapit mówi; sam akapit twierdzi rzecz szerszą —
że nieciągłość jest w tych zdaniach brakiem ostatnim — i tej ta poprawka nie tyka.
Do przeczytania jest `harness/nieciągłość.py`, bo on ten zbiór wyznacza,
oraz `bloker` w `olski/pokrycie.py`, bo stamtąd bierze się nazwa
zatrzymania.

Dwie liczby w [`docs/disambiguation.md`](../docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)
są wyższe od tego, co mówi przebieg.
Dokument mówi, że przyłączenie jest całą decyzją w siedmiu zdaniach na dziesięć,
a w dwóch klasach, które je nazywają, w przeszło czterech piątych,
gdy `python3 -m harness.czytania` nad Składnicą 180723 mówi dziś mniej:
przeszło trzy piąte i przeszło trzy czwarte.
Ruchem jest granica postawiona po tej stronie, po której stoi pomiar
([`CLAUDE.md`](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)),
albo zdanie oddające obie liczby przebiegowi.
Do przeczytania jest akapit pod nimi, bo argumentuje on ich rzędem wielkości,
oraz sam wydruk, bo drugą z tych liczb przebieg drukuje osobno dla każdej z dwóch klas,
a granica trzyma się tylko pod jedną z nich.

Zawężenie orzecznika zgodnego ma wycenę nad prozą repozytorium i nie ma decyzji,
bo populacja jest tam tej wielkości, że czterema zdaniami przewraca wniosek
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#zawężenie-orzecznika-zgodnego-wyceniono-i-decyzji-nie-ma)
trzyma cenę wraz z tym, co przy niej przeczytano).
Ruchem jest ten sam wariant puszczony nad Składnicą — rama bez pozycji `nom`
wszędzie poza kopulą — z pytaniem, ilu zdaniom ginie czytanie złote,
bo tego pytania proza postawić nie umie, nie mając anotacji.
Do przeczytania jest przy tym kryterium po stronie przymiotnika, które tamta sekcja
nazywa tańszym: jeżeli katalog przymiotnikowy Walentego je daje, wybór między
wpuszczeniem a zawężeniem po stronie czasownika przestaje być potrzebny,
a wtedy cały ten wpis zamyka wpis o przymiotniku.

Zestaw ciągów odrzucanych wokół łącznika `to` stoi w `próba/łącznik-odrzucane.txt`
i nikt go jeszcze nie puścił sondą.
Materiał ten jest potrzebny dlatego, że Składnica zawiera wyłącznie zdania poprawne,
więc pomiar nad nią nie ukarze wariantu za przyjęcie ciągu,
którego wyprowadzić nie wolno, i nie rusza tego dogęszczenie banku drzew.
Sonda różnicowa widzi przy tym nadgenerację węższą — czytanie dołożone zdaniu
poprawnemu — a ciągu przyjętego, którego przyjmować nie należało, nie widzi wcale.
Ruchem jest przebieg sondy nad tym plikiem obok banku drzew,
przy wariantach zdejmujących ciała łącznika, oraz odczytanie tabeli przejść
w drugą stronę: `odrzucone → przyjęte` jest tu ceną, a nie zakupem.
Do rozstrzygnięcia jest przy tym, czy wydruk ma tę odwrotność nazywać sam,
bo dopiero to byłoby dopisaniem do `harness/ruch.py`;
uruchomienie pliku nie żąda tam ani jednej linijki.
Siedem ciągów pliku jest dziś odrzuconych i one są materiałem regresyjnym,
a nadgeneracji nie pokazuje ani jeden: `Ty to jest leń.` jest sądem niepotwierdzonym,
który rozsądza mówiony rejestr NKJP
([`docs/corpora.md`](../docs/corpora.md#the-national-corpus-of-polish)),
więc dopóki to czytanie nie padnie, teza o ślepocie pomiaru materiału nie ma.
Rosnąć ten zestaw ma o ciągi wokół tego jednego łącznika i nie dalej:
zestaw negatywny dla całej gramatyki jest osobnym przedsięwzięciem.
Kandydatami nie są `Kota to zwierzę.`, `Koty to zwierzę.` ani `Kot to są zwierzęta.`,
choć wyprowadzają się: pierwsze stoi mianownikiem osobnego leksemu
(`kota subst:sg:nom:f`), drugie tym, że ciało bezczasownikowe zgodności liczby
nie żąda i żądać nie może, a trzecie ma kształt, który polszczyzna ma —
`Rodzina to są ludzie.` — i złe jest w nim znaczenie, a nie składnia.
Asercja w `tests/test_orzeczenie.py` może stanąć obok pliku i nic nie kosztuje,
bo łapie inną awarię — ta pilnuje każdego commita, a sonda wyboru wariantu.

Sekcja zgodności ról nie pojawiła się w wydruku `harness/pomiar.py`
puszczonym nad wycinkiem Składnicy z `--limit 3000` i nikt nie wie czemu.
Jest to ten gatunek awarii, na który poszła sesja o łączniku:
pomiar, który po cichu czegoś nie mówi, czyta się jak pomiar mówiący, że jest dobrze,
więc ktoś przeczyta przebieg bez tej tabeli i uzna, że role się zgadzają.
Do przeczytania jest `Raport.wydruk` w `harness/pomiar.py` obok `agreements`:
licznik ten zapełnia się tylko nad zdaniem przyjętym, porównywalnym
i mającym w drzewie wzorcowym rolę, więc pusty bywa odpowiedzią prawdziwą,
a wydrukiem nieodróżnialną od nieodpalonej sekcji.
Ruchem jest wiersz mówiący zero tam, gdzie dziś nie ma wiersza.
