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
`Verdict.rozbieżne` w `olski/werdykt/zdanie.py` wypuszcza konstytuent,
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

Konstytuent, którego głową jest luka, nie ma czym się nazwać,
a streszczenie pyta go o nazwę i wywraca wyjątkiem cały przebieg.
`liść_głowy` w `olski/parse/czytanie.py` schodzi po głowach do liścia,
a węzeł produkcji o pustym ciele córek nie ma,
więc `gospodarz` w `olski/parse/streszczenie.py` dostaje `IndexError`.
Gramatyka olskiego produkcji o pustym ciele nie ma,
więc wywraca się tylko wariant z luką (`harness/luka.py`):
`Jest reguła, którą ktoś zna po cichu.` wywraca się tam pod `luka wszędzie`,
bo gospodarzem okolicznika jest `wypełnienia`, a jego głową puste `dopełnienie`,
i sonda nie dochodzi przez to do końca nad znaczną częścią prozy tego repozytorium.
Przeoczeniem to nie jest: komentarze nad `Node.span` i nad `Production.głowa`
mówią już, że pustego ciała żąda luka, że nikt tego żądania nie zaspokoił
i że zero nie nazywa w takim ciele żadnej córki.
Ruchem nie jest napis zastępczy w miejsce wyjątku,
bo o nazwę pyta streszczenie po to, żeby wypisać ją czytelnikowi.
Zamyka ten wpis tamten o luce wskazującej zaimek, który ją wiąże,
a nie miejsce, w którym stoi:
etykieta roli postawiona nad zaimkiem daje głowie liść,
a przy okazji tę samą rolę, którą na tych zdaniach stawia bank drzew.
Do przeczytania jest `_host`, którego `gospodarz` woła, bo gospodarza wybiera on,
więc on mówi, czy pytanie pada tu o konstytuent, którego nazwać się nie da,
czy o cudzy konstytuent, na którym zejście miało się zatrzymać.

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
(`_nazwany_gdzie_indziej` w `olski/parse/decyzje.py`),
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
a czyta ją `Decyzje.przyłączenia` wraz z warstwą rozstrzygającą.
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
Do przeczytania jest przedtem `Verdict.morfologia` w `olski/werdykt/zdanie.py`,
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
dzisiaj `_po_szkolnemu` w `olski/werdykt/zdanie.py` rusza samo zdanie z łącznikiem,
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
([`docs/walencja.md`](../docs/walencja.md#werdykt-nazywa-żądanie-obsadzonej-pozycji)),
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
(`gospodarz` w `olski/parse/streszczenie.py` nazywa go formą głowy).
Do przeczytania jest, czy wiersz taki mówi coś, czego nie mówi wiersz obok:
żądanie pozycji przyimkowej pokrywa się z tym, co o tej parze mówi już
świadek ramowy warstwy rozstrzygającej
([`docs/rozstrzyganie.md`](../docs/rozstrzyganie.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)),
tyle że tamten mówi o przyimku, a ten o klasie rzeczy pod nim.

Zdanie bywa jednoznaczne strukturalnie i przemilcza przy tym, o kogo idzie.
`Wynajmę mieszkanie.` ma w `olski/żądania.txt` dwie pozycje wykluczające się —
`Initiator.Goal` w celowniku i `Initiator.Source` pod `od` — i żadnej nie obsadza,
więc czytelnik nie wie, czy wynajmuje się komuś, czy od kogoś.
Znaleziska są dziś dwa, poprawka jednego znaku i zaimek wskazujący na dwie rzeczy
([`docs/subset.md`](../docs/subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)),
a to byłoby trzecie i wordnetu nie żąda:
role stoją w pliku, a nieobsadzoną pozycję widzi rozbiór.
Bliskie jest ono regule o zdaniu spakowanym
([CLAUDE.md](../CLAUDE.md#katalog-chwytów-rejestru)),
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
([`docs/walencja.md`](../docs/walencja.md#werdykt-nazywa-żądanie-obsadzonej-pozycji)).
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

Jedna grupa imienna o dwóch czytaniach wydaje warstwie zaimkowej dwie rzeczy.
`Radny Mitkiewicz przyszedł na zebranie. On mówił długo.` dostaje zgłoszenie
`„On” wskazuje na „Radny” albo „Mitkiewicz”`, choć to jedna osoba:
przydawka i apozycja są dwoma czytaniami tej samej grupy, a każde z nich ma inną głowę,
więc `_głowy` w `olski/odniesienia.py` wydaje obie, a `_rzeczy` scala tylko wspólny lemat.
Wpis jest o regule dzisiejszej, a nie o rozszerzeniu za flagą,
bo zdanie obok wydaje takie pary tak samo.
Ruchem jest scalenie głów, których grupy zachodzą na siebie:
`_głowy` zna rozpiętość każdej grupy, więc dwie głowy z jednej rozpiętości
są jedną rzeczą tak samo jak dwie formy o jednym lemacie.
Do przeczytania są sądy `fałszywe` w `próba/nkjp-sądy.txt`, które ten kształt nazywają —
`radny Mitkiewicz`, `lewą nogą`, `innych ludzi` — bo mówią, ile zgłoszeń to zdejmuje.

Kandydat miejscowy wycisza zaimek także tam, gdzie polszczyzna go z nim nie łączy.
`olski/odniesienia.py` milczy nad zaimkiem, przed którym w tym samym zdaniu stoi
rzecz zgodna z nim liczbą i rodzajem, i jest to warunek bez składni:
w `Olski go nie czyta i o jego polszczyźnie milczy.` wycisza go `Olski`,
choć `go` nie może tam znaczyć `Olski` — polszczyzna żąda w tej pozycji `siebie`,
bo podmiot i dopełnienie stoją w jednej ramie.
Ruchem jest ten warunek zawężony do kandydatów spoza ramy zaimka:
role zdania składowego werdykt już nazywa (`Obsada` w `olski/parse/podsumowanie.py`),
a zaimek jest liściem o znanej rozpiętości, więc zdanie składowe obu wskazuje
`zakresy` w `olski/parse/streszczenie.py`.
Warunek zdjęty ma już swój przebieg: flaga `w_zdaniu` każe kawałkowi własnego zdania
wydać rzeczy zamiast wyciszać, a jej trafienia nad NKJP przeczytano i oceniono
([`docs/subset.md`](../docs/subset.md#rzeczy-z-tego-samego-zdania-czekają-za-flagą)).
Do zmierzenia zostaje przez to sam wariant zawężony,
bo różnica między nim a tamtym jest całą mierzoną rzeczą,
a kandydat z ramy zaimka jest jednym z kształtów, które te sądy nazywają.

Werdykt nie niesie segmentów, więc nad jednym napisem segmentacja idzie drugi raz.
`dalsze_zatrzymania` w `olski/werdykt/zdanie.py` woła `morphology` nad `Verdict.text` ponownie,
a pod `--morfologia` woła ją tam jeszcze `_morfologia_zdania`;
obie tłumaczą się z tego własnym zdaniem wskazującym na `werdykt`.
`werdykt` mówi jednak tylko, czemu segmenty przychodzą do niego argumentem,
a nie czemu u niego nie zostają,
więc fakt ten stoi w dwóch kopiach i nie ma właściciela.
Ruchem jest pole na segmenty w `Verdict`, a obok niego krawędź zatrzymania
w miejsce samej jej formy: odpadają wtedy oba wołania
oraz `na_czym_stanęło` liczone drugi raz.
Ceną jest pamięć, bo werdyktów trzyma się tyle, ile dokument ma zdań
(`nad_tekstem` w `olski/werdykt/tekst.py`), a segment niesie każde odczytanie swojej formy;
tym samym argumentem `werdykt` porzuca las.
Czasu ruch ten nie kupuje prawie wcale,
bo segmentacja jednego zdania waży drobny ułamek jego rozbioru,
więc powodem są dwa zdania tłumaczące się z jednego braku, a nie przebieg.
Do przeczytania jest, ile ta pamięć waży nad najdłuższym dokumentem repozytorium,
bo cena jest tu jedynym argumentem, a nikt jej nie zmierzył.

Kropka bez odstępu za nią jest naprawą jednego znaku i jako jedyna nie ma kształtu.
Napis niedomknięty i zdanie cytujące spoza rejestru dostają poprawkę
poświadczoną rozbiorem (`Naprawa` w `olski/werdykt/odrzucone.py`),
a `niska.Cena` wychodzi zatrzymaniem na formie,
która z pomyłką autora nie ma nic wspólnego.
Poza tę klasę wypadła przez rachubę zdań:
kropka bez odstępu nie jest granicą zdania (`SENTENCE_END` w `olski/document.py`),
więc po poprawce olski czyta dwa zdania zamiast jednego,
a werdykt o jednym zdaniu nie ma gdzie takiej odpowiedzi postawić
([`docs/subset.md`](../docs/subset.md#poprawkę-jednego-znaku-poświadcza-gramatyka)).
Ruchy są dwa i różnią się adresatem.
Albo poprawka wchodzi do podziału na zdania i mówi o niej wykrywacz nad dokumentem,
a nie werdykt o zdaniu.
Albo `Naprawa` niesie odczytania kilku zdań,
i wtedy jej wiersz przestaje mówić jedną rzecz o jednym zdaniu.
Do przeczytania przed wyborem jest
[`docs/firing-rates.md`](../docs/firing-rates.md#missing-space-after-full-stop-read-the-text-of-a-link)
wraz z sekcją o trafieniach słusznych tej samej reguły,
bo mierzy ona ten sam odstęp nad korpusem audytowym, tyle że samym znakiem.

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
Blokerem jest ekstrakcja: `olski/markdown.py` zdejmuje backticki
i nie mówi nikomu, że token nimi stał,
a bez tego wyjątku pierwszego nie da się napisać —
i nie zastąpi go test na polskie słowo,
bo `odmień` i `przejrzyj` są nazwami funkcji i polskimi słowami naraz
([`CLAUDE.md`](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)).
Ruchem jest więc najpierw ta informacja przeniesiona przez ekstrakcję,
a dopiero po niej kryterium, którego dowodem jest zero trafień nad prozą repozytorium:
bez wyjątków strzela ono na pierwszych zdaniach akapitów kilkadziesiąt razy
i ani razu trafnie.

Naprawy formy, którą wpisy o niezgodności biorą za świadka, nie robi żaden kod.
`docs/subset.md` rozstrzyga, że zgłoszenie o parze niezgodnej poświadcza odczytanie napisu,
w którym orzeczenie dostało formę, której żąda podmiot
([`docs/subset.md`](../docs/subset.md#wpis-korpusu-usterek-nazywa-kształt-zdania-a-nie-znaczenie-słowa)),
a rozbiór drugi robi dziś tylko `olski/werdykt/odrzucone.py`
i robi go dla jednego znaku, nie dla formy.
Ruchem jest ten sam rozbiór drugi nad napisem,
w którym forma osobowa dostaje liczbę i rodzaj podmiotu,
a kandydatów daje synteza tego samego lematu;
zgłoszenie nazywa parę, a nie napis do przepisania, bo naprawa bywa dwojaka.
Zacząć można od razu, bo poprawki obu wpisów o niezgodności
(`Zespół programistów spotkał się rano.`, `Lista błędów i ostrzeżeń została zapisana.`)
olski czyta, więc świadek stoi.
Uogólnienia na inne pary — przypadek dopełnienia, przypadek zaimka względnego,
liczbę przydawki — ten wpis nie obejmuje, bo ich poprawki w korpusie są dziś nieczytane
i świadka nie ma czym postawić;
ile poprawek korpusu olski czyta, mówi `python3 -m harness.usterki`,
a wpis o tych parach pisze się dopiero wtedy, gdy ich poprawki wchodzą.

Wykrywacz imiesłowu bez podmiotu trafia nad cudzym tekstem w zdania, których nikt nie poprawia:
trafienia nad NKJP przeczytano co do jednego i żadnego czytelnik nie potwierdził
([`docs/subset.md`](../docs/subset.md#imiesłów-przy-orzeczeniu-bezosobowym-czeka-za-flagą)).
Ruchem oczywistym jest zawężenie po głowie roli i ono nie wystarcza:
zdjęcie predykatywu zabiera większość trafień fałszywych, resztę zostawia,
a przy tym przeczy wpisowi korpusu usterek, który nazywa usterką `można`.
Do rozstrzygnięcia jest, czy tożsamość wykonawcy domyślnego obu orzeczeń
da się orzec z czegokolwiek, co to repozytorium ma;
jeżeli nie, ruchem jest zdjęcie reguły z kodu,
a dwa wpisy korpusu usterek wracają wtedy do ciszy.
