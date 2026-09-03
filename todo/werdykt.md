# Werdykt i wydruk

Gospodarz o dwóch kształtach ma dwie głowy, a werdykt nazywa jedną i nie mówi którą.
`Organ gminy może wyznaczyć swojego przedstawiciela do udziału w zgromadzeniu.`
daje wiersz `„do udziału” → „może”, „przedstawiciela”`,
a grupa imienna nazwana tam `przedstawiciela` jest w innym czytaniu grupą,
w której głową jest `swojego`:
przymiotnik ma czytanie rzeczownikowe, a rzeczownik dopełniaczowe,
czyli tę samą parę, o którą pyta wpis o rzeczownikowym czytaniu przymiotnika.
Wybór między tymi dwiema nazwami robi porządek, w jakim las wydaje drzewa,
bo `_przedstawiciel` w `olski/parse/las.py` bierze pierwsze z nich,
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

Grupa imienna rozbieżna zostaje bez listy czytań, bo streszczenie nie ma w niej czego nazwać.
`Verdict.rozbieżne` w `olski/werdykt.py` wypuszcza konstytuent,
którego streszczenia naprawdę się różnią, czyli zdanie podrzędne, a grupy imiennej nie:
`describe` w `olski/parse/streszczenie.py` szuka ról zdania, a grupa imienna żadnej nie nosi,
więc oba jej kształty streszczają się pustym słownikiem.
Różnica siedzi tam w głowie — raz `rada` z przydawką `zainteresowana`,
raz `zainteresowana` z przymiotnikiem `rada` i dopełniaczem `gminy` —
więc ruchem jest drugie streszczenie, to o grupie imiennej:
głowa oraz to, czym są słowa stojące obok niej.
Tej samej nazwy żąda wpis o gospodarzu o dwóch głowach, a wydać ją raz jest taniej.
Do przeczytania jest, ile wierszy `„…” reads N ways` rejestr ustaw wydaje nad grupą
imienną, a ile nad zdaniem podrzędnym, bo pierwsza z tych liczb jest ceną milczenia.

Przyimka wysuniętego wyrażenia nie widać w werdykcie, a innego przyimka widać:
`O czym poseł mówi?` streszcza się jako `grupa_pytajna: czym`,
a `Poseł mówi o ustawie.` jako `wyrażenie_przyimkowe: o ustawie → mówi`.
Rola dla tego wyrażenia nic nie kosztuje i jest to zmierzone:
`rodzina.modyfikator` dopisany do `role` i do `przyłączane`
w `DEKLARACJA` (`olski/subset/deklaracja.py`)
nie rusza werdyktu o ani jedno zdanie Składnicy ani korpusu ustaw.
Sama rola kosztuje najwyżej tyle samo, bo streszczenie rozszczepia wtedy
o jedno pole mniej, więc pomiaru drugi raz nie żąda.
Strzałki temu wyrażeniu dać jednak nie wolno i mówi to kryterium listy obok:
`przyłączane` bierze rolę, którą gramatyka wpuszcza w kilka miejsc,
a to wyrażenie ma miejsce jedno, więc strzałka powtarzałaby czasownik zawsze —
i za to samo stoi poza tamtą listą dopowiedzenie.
Do rozstrzygnięcia przed samą rolą jest etykieta.
Nazwą roli jest nazwa symbolu rodziny, więc jedna rzecz nosi trzy nazwy tam,
gdzie wyrażenie stojące na swoim miejscu nosi `wyrażenie_przyimkowe`,
a zlanie trzech w jedną odbiera jedyną rzecz, jaką te trzy mówią:
w której rodzinie stoi czoło.
Do rozstrzygnięcia jest, czy ta rzecz ma czytelnika.

Ciąg współrzędny wewnątrz wypełnienia roli nie ma po werdykcie żadnego wiersza.
Nawias pokazuje granicę członu tylko nad ciągiem, którym jest sama rola
(`_nawiasuj` w `olski/parse/streszczenie.py`),
a wiersz o konstytuencie ustępuje mu miejsca nad każdym ciągiem
(`_nazwany_gdzie_indziej` tamże),
więc `Ustawa określa zadania ochrony ludności i obrony cywilnej.`
zostaje samą liczbą czytań i tak zostaje garść werdyktów rejestru ustaw
oraz pojedyncze zdania wieloznaczne Składnicy
([`docs/disambiguation.md`](../docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)).
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
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#nothing-above-a-coordination-distributes-into-it)),
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
Rolę tę trzyma `rozstrzygany` w `DEKLARACJA` (`olski/subset/deklaracja.py`),
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

Autor nie ma jak zobaczyć, co wykluczenie słownikowe wycięło jego tekstowi.
Lemat, który przez nie przepadł, nie zostawia po sobie ani wiersza werdyktu:
`Go jest grą.` melduje zatrzymanie na `grą`, czyli miejsce, w którym gramatyce
zabrakło podmiotu, a nie to, w którym zabrano czytanie
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#słownictwo-projektu-orzeka-o-lemacie-w-obie-strony)).
Kierunek `wpuszczane` umie przez to napisać ten, kto już wie, co napisać.
Ruchem jest wiersz wykazu morfologii o czytaniu zdjętym przez wykluczenie.
Do przeczytania jest przedtem `Verdict.morfologia` w `olski/werdykt.py`,
bo wykaz ten wypisuje czytania, które do rozbioru weszły,
a odpowiedzi trzeba tu o czytanie, którego w nim nie ma.

`podmiot` znaczy w tym repozytorium dwie rzeczy i granica biegnie przez werdykt.
Przed nim jest pozycją schematu, czyli tym, co bank drzew woła `subj`
i co stawia 170 razy na cząstce `się`, gdzie podmiotu nie ma;
za nim jest funkcją zdaniową, bo `NAZWY_SZKOLNE` w `olski/subset/deklaracja.py`
przekłada role zdania z łącznikiem na nazwy składni szkolnej
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim)).
Użytkownika to nie kosztuje nic, a następnego programistę kosztuje ten sam wniosek,
od którego zaczęła się cała ta sprawa: czyta `find("podmiot")` po polsku
i bierze pozycję schematu za funkcję zdaniową.
Ruchem jest nazwa wewnętrzna brzmiąca `subj`, bo wtedy `_slot_role`
w `harness/corpus.py` schodzi do tożsamości i znika,
a porównanie idzie `subj` do `subj` bez przekładu w środku.
Żadna liczba się przez to nie rusza, bo obie strony porównania zmieniają się razem.
Zmiana jest jednak większa, niż wygląda, i to jest tu do przeczytania przed nią.
Napisów `"podmiot"` jest w kodzie 112, z czego większość stoi w testach
i część z nich pyta o wydruk, czyli ma zostać po staremu;
każde wystąpienie żąda więc osądu, po której stronie granicy stoi, a nie zamiany.
Drugą rzeczą jest to, że przekład przestaje być miejscowy:
dzisiaj `_po_szkolnemu` w `olski/werdykt.py` rusza samo zdanie z łącznikiem,
a nad nazwą `subj` musiałby przekładać każde streszczenie, bo każde ją niesie.
Trzecią jest `dopełnienie`, które przychodzi z `np(acc)` tą samą drogą:
przemianowanie samego podmiotu zostawia je słowem szkolnym o zakresie GFJP,
czyli dokładnie tą usterką, którą ta zmiana zdejmuje.
Rozstrzygnięciem przed pierwszym commitem jest więc całe słownictwo ról naraz,
a nie jedna nazwa.
Przypadkiem tej usterki nie jest natomiast `dopełnienie: godzinę`
w `Czekał godzinę.`, choć wygląda tak samo:
tam zła jest struktura, bo biernik zajmuje pozycję dopełnienia naprawdę,
a nie nazwa nad strukturą dobrą, i wpis o czwartym werdykcie porównania ról
trzyma tamto razem z jego parą.

Wiersz żądania nazywa dwie pozycje ramy, a plik żądań ma ich osiem.
`--żądania` mówi o podmiocie i o dopełnieniu, bo tyle nazywa streszczenie
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#werdykt-nazywa-żądanie-obsadzonej-pozycji)),
a poza wierszem zostaje wyrażenie przyimkowe wraz z bezokolicznikiem,
zdaniem podrzędnym i pytaniem zależnym.
Granicę tę dziedziczy `--osoby`, więc ruch kupuje dwie flagi naraz,
a w tej drugiej dokłada pozycję przyimkową do tysiąca wierszy żądających kogoś.
Pierwsze z nich jest w pliku pozycją drugą co do wielkości, zaraz po podmiocie,
więc to ono jest tu całym ruchem, a trzy pozostałe idą przy okazji.
Przeszkodą jest przy nim gospodarz, a nie sam przekład nazwy:
wyrażenie przyimkowe przyłącza się u olskiego wszędzie, gdzie polszczyzna je stawia,
więc żądanie stoi po stronie czasownika tylko w tym czytaniu,
w którym wyrażenie doszło do niego, a nie do rzeczownika obok
(`_attachment` w `olski/parse/streszczenie.py` nazywa gospodarza formą głowy).
Do przeczytania jest, czy wiersz taki mówi coś, czego nie mówi wiersz obok:
żądanie pozycji przyimkowej pokrywa się z tym, co o tej parze mówi już
świadek ramowy warstwy rozstrzygającej
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)),
tyle że tamten mówi o przyimku, a ten o klasie rzeczy pod nim.

Zdanie bywa jednoznaczne strukturalnie i przemilcza przy tym, o kogo idzie.
`Wynajmę mieszkanie.` ma w `olski/żądania.txt` dwie pozycje wykluczające się —
`Initiator.Goal` w celowniku i `Initiator.Source` pod `od` — i żadnej nie obsadza,
więc czytelnik nie wie, czy wynajmuje się komuś, czy od kogoś.
Znaleziska są dziś dwa, wieloznaczność i poprawka jednego znaku
([`docs/subset.md`](../docs/subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego)),
a to byłoby trzecie i wordnetu nie żąda:
role stoją w pliku, a nieobsadzoną pozycję widzi rozbiór.
Bliskie jest ono regule o zdaniu spakowanym
([CLAUDE.md](../CLAUDE.md#dla-kogo-jest-napisane-zdanie)),
z tą różnicą, że tamta mówi o słowie wyrzuconym ze zdania,
a to o uczestniku, którego zdanie nie nazwało.
Zawężenie jest tu całą robotą, bo wersja naiwna zapala się wszędzie:
pozycji nieobsadzonych ma każde zdanie i większość z nich niczego nie przemilcza.
Kandydatem na kryterium jest para pozycji, które różni samo uszczegółowienie roli,
czyli dwie strony jednego zdarzenia,
a policzone nad plikiem bierze ono 2 171 lematów z 8 556, czyli co czwarty,
bo `Theme.Goal` obok `Theme.Source` jest w nim parą najczęstszą i mówi o kierunku,
a nie o dwóch stronach.
Zawężone do roli `Initiator` bierze 83 lematy,
a do jednej pozycji niosącej oba uszczegółowienia naraz — 19,
i są to `wynająć`, `wypożyczyć`, `dzierżawić`, `czarterować` wraz z resztą tej klasy.
Ani jeden z nich nie stoi w rejestrze, o który olski pyta,
więc znalezisko wychodzi poprawne i bezczynne, i to jest tu cena.
Czy zdania z tymi lematami naprawdę czyta się dwojako, zostaje do przeczytania —
sonda konwersów mierzyła to kształtem pozycji i wyszła jej liczba za wysoka
([`docs/disambiguation.md`](../docs/disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma)).

Fraza bezokolicznikowa nie dostaje wiersza żądania, choć ma własną ramę.
Zejście po role staje na niej (`własna_rama` w `DEKLARACJA`), żeby dopełnienie
`edytować` nie dostało żądania czasownika stojącego nad nim, więc `Autor zamierzył
edytować dokument.` milczy o dopełnieniu w ogóle
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#werdykt-nazywa-żądanie-obsadzonej-pozycji)).
Ruchem jest ta fraza czytana jak zdanie składowe: jej głowa rządzi ramą,
a jej rozpiętość jest zakresem, w którym szuka się wypełnień.
Przeszkodą jest to, gdzie stoi zespół czasownikowy tej frazy:
przy formie osobowej zamyka go symbol `orzeczenie`, więc cząstkę zwrotną i
przeczenie widać po jego liściach, a bezokolicznik stoi liściem wprost pod frazą,
obok swoich wypełnień, więc pytanie o liście tej frazy odpowiada o całym zdaniu.
Do rozstrzygnięcia jest, czy tańszy jest symbol nad tym zespołem w gramatyce,
czy warunek na liście stojące przed pierwszym konstytuentem frazy.

Wiersz `--osoby` o zaimku i o liczebniku nie mówi czytelnikowi nic.
`to`, `wszystko`, `nic`, `pierwsza` i `pięć` dostają go tak samo jak `pomiar`,
a nie nazywają nikogo z innego powodu niż `pomiar`:
nie nazywają one same z siebie ani kogoś, ani czegoś,
bo to, czym są, stoi w zdaniu obok nich albo w zdaniu przed nimi.
Nad prozą tego repozytorium jest to mniej więcej co dziesiąty wiersz tej flagi.
Ruchem jest warunek na część mowy głowy wypełnienia,
czyli pytanie o znacznik odczytań liścia zamiast o sam lemat,
i wtedy zaimek milczy tak jak słowo spoza pliku żądań.
Do rozstrzygnięcia jest, gdzie postawić granicę:
`ktoś` deklaracja osób już wypisuje i wypisywać musi, bo kogoś nazywa,
a liczebnik w podmiocie bierze rzecz z dopełniacza obok siebie,
więc żądanie mówi tam o tej rzeczy, a nie o liczbie.
Do przeczytania są wiersze tej flagi nad `docs/`, bo klasa jest tam cała.

Werdykt nie mówi o zaimku, którego tekst nie pozwala rozwiązać,
a [cel](../docs/roadmap.md#cele) tego żąda, i jednostką tego żądania jest tekst
([`docs/roadmap.md`](../docs/roadmap.md#podzbiór-jest-umową-a-nie-zasięgiem)).
`Są one czerwone.` przechodzi dziś samo, bez żadnego zdania przed sobą,
bo `olski.check` liczy czytania jednego zdania i o sąsiedztwo nie pyta.
Kandydatów na antecedens wylicza zgodność, a nie znaczenie:
`one` żąda liczby mnogiej i rodzaju niemęskoosobowego,
więc kandydatem jest każda grupa imienna przed nim, która jedno i drugie niesie.
Ruchem jest przebieg po zdaniach jednego pliku,
który zbiera grupy imienne przyjętych czytań i przy każdym zaimku liczy kandydatów,
a zgłasza zero oraz więcej niż jednego, wypisując przy drugim ich listę;
zgłoszenie idzie przy zaimku, bo drugie czytanie całego tekstu
mnożyłoby się przez każdy zaimek w nim.
Do przeczytania jest `pomijalny` w `olski/skład/składnia.py` wraz z `Kontekst`,
bo skład prowadzi ten rachunek w drugą stronę
i ma już warunek na rodzaj rozdzielający uczestników zdania obok
([`docs/kategorie-zapisu.md`](../docs/kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)),
a wpis o zasięgu antecedensu przy opuszczonym podmiocie zdania podrzędnego
mówi, czego ten warunek nie obejmuje.
Do rozstrzygnięcia jest, czy zaimek bez ani jednego kandydata
jest zgłoszeniem tej samej nazwy co zaimek o dwóch,
bo pierwszy mówi, że tekst czegoś nie podaje, a drugi, że podaje dwie rzeczy.
