# Parsowanie

Tor gramatyczny ma dwa kierunki, a ten dokument mówi o pierwszym:
polski tekst wchodzi, struktura wychodzi.
Kierunek drugi opisuje [sklad.md](sklad.md),
a ramę obu daje
[design-notes.md](design-notes.md#two-angles-of-the-grammar-track).
Ten sam dokument mówi, ile kosztuje bliskość polszczyzny:
[drabina kosztów](design-notes.md#the-cost-ladder)
i [urwisko nieciągłości](design-notes.md#the-cliff-discontinuity).
Co gramatyka wpuszcza, mówi [subset.md](subset.md),
a co warstwa za parserem ma rozstrzygnąć, mówi
[disambiguation.md](disambiguation.md).

## Earley wydaje las, a GLR zostaje optymalizacją

Whatever parses olski must produce a **forest, not a tree**,
because genuine ambiguity is the normal case
and the useful operation is to enumerate readings and filter them.

GLR is the right shape of answer but probably the wrong specific choice:

- GLR's payoff is a precomputed table
  giving near-deterministic speed on mostly unambiguous input.
  An olski grammar will be conflict-dense throughout,
  so the graph-structured stack works hard on nearly every token
  and most of the speedup never arrives.
- Table construction over a permutation-expanded free-word-order grammar
  can blow up badly.
  The one GLR system measured over real Polish says nothing about that cost:
  its table is 146 states.

That same system supplies a baseline worth flinching at:
20% of its input fails to parse
against a grammar hand-fitted to a register far narrower than olski.
See [glr-in-practice.md](glr-in-practice.md#measurements).

Nullable rules, which pro-drop makes unavoidable, are not an objection:
Tomita's original algorithm breaks on them and maintained implementations do not.

**Earley is the boring answer and it is what `olski/parse/tablica.py` runs.**
It handles any CFG, including left recursion and nullable rules,
with no preprocessing;
it produces a shared packed parse forest natively;
its worst case is cubic but real grammars behave far better.
Decisively for a project whose grammar is still being designed:
the grammar can change without rebuilding an automaton.
GLR stays an optimization to reach for if measurement ever demands one,
and no measurement does:
a run over the whole of Składnica takes half a minute.

For free word order specifically,
the move that keeps a CFG viable
is to separate **immediate dominance from linear precedence**,
as GPSG did.
Dominance rules say what the daughters are,
separate precedence constraints say which orders are legal,
and a preprocessor deals with the factorial.
Olski's clause is written that way,
and what it bought beyond the shorter grammar
is in [subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk).
This also keeps the subset honest:
the one permutation excluded from olski
is excluded by an explicit constraint rather than by omission.

## Werdykt jest zapytaniem o las, a nie listą czytań

Werdykt wychodzi z lasu ze współdzielonymi węzłami, a nie z listy drzew,
i po co, widać na dwóch poleceniach:

```sh
python3 -m olski.check -c "Program zapisuje ustawienia w pliku w katalogu."
python3 -m olski.check -c "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci w firmie w kraju."
```

Każde doklejone wyrażenie przyimkowe podwaja liczbę czytań,
bo dochodzi do czasownika albo do rzeczownika przed nim,
a te wybory są od siebie niezależne.
Drugie z tych zdań ma więc sześćdziesiąt cztery czytania
i sześć nierozstrzygniętych decyzji, po jednej na wyrażenie,
a werdykt wypisuje sześć wierszy:
przyimek wraz z dwiema głowami, do których dochodzi.
Wierszy jest tyle, ile decyzji,
więc przybywa ich z długością zdania, a nie z liczbą czytań,
i o tę różnicę krotności szło.
Tę samą wielkość nazywa
[pytanie o czytelność prefiksu](open-questions.md#czy-jednoznaczność-prefiksu-mierzy-czytelność),
więc jedno pytanie i drugie stoją na tym samym prymitywie.
Liczba czytań jest przy tym liczbą, a nie napisem `64+`:
las podaje ją sumą po pozycjach korzenia,
i granica z `MAX_READINGS` sięga wypisywania drzew, a nie liczenia ich.

Lista czytań tego nie dowozi, i nie dowiozą jej dwie poprawki,
które wyglądają na tańsze wyjście:
streszczenie nazywające wszystkie węzły roli zamiast pierwszego,
wraz ze zdjętą granicą wyliczania.
Stoją tu zapisane, żeby nikt ich nie proponował drugi raz.
Streszczenie czytania nazywa pierwszy węzeł roli,
więc dwa czytania różne miejscem drugiego modyfikatora
wychodzą z niego jednym napisem,
a nazwanie wszystkich
daje nad drugim z tych zdań sześćdziesiąt cztery wiersze do porównania ręką:
wydruk rośnie wtedy wykładniczo,
a nazwać trzeba liczbę decyzji.

Trzecie tańsze wyjście brzmi najmocniej i mierzy się najgorzej:
zostawić enumerator i powiedzieć, że zdanie o więcej niż `MAX_READINGS` czytaniach
jest po prostu za wieloznaczne, żeby je czytać.
Werdykt „poddaję się” jest tu w porządku i nie o niego idzie.
Idzie o to, że enumerator zstępujący nie umiał go wydać tanio.
`analyses` przed tą zmianą (commit `9456a22`, wtedy jeden moduł)
wyliczał pod pozycją każde wyprowadzenie, zanim oddał pierwsze,
więc granica ucinała wydruk, a nie pracę.
Zdanie ustawy o 28 042 czytaniach pod gramatyką z tamtej chwili —
[jedno z tych, w których liczba czytań przestaje o czymkolwiek mówić](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem) —
kosztowało go 76 s, żeby oddać sześćdziesiąt cztery drzewa i napis `64+`.
Las podaje nad nim liczbę dokładną w 0,05 s.
Sekundy zależą od maszyny, a krotność jest trzema rzędami wielkości,
i to o nią tu idzie.
Obie liczby bierze to samo polecenie,
raz nad plikiem z tamtego commita, a raz nad tym, który stoi:

```sh
git show 9456a22:olski/parse.py > /tmp/stary/parse.py
PYTHONPATH=/tmp/stary python3 -c 'import time, sys
from olski.subset import GRAMMAR, morphology
parse = __import__(sys.argv[1]).parse
s = morphology(open("zdanie.txt", encoding="utf-8").read().strip())
t = time.time(); w = parse(GRAMMAR, s)
print(len(w.readings), getattr(w, "ile", "—"), f"{time.time() - t:.2f}s")' parse
```

Enumerator pisany leniwie zmieściłby się w tej granicy,
bo urwałby wyliczanie na sześćdziesiątym czwartym drzewie,
i to jest jedyna uczciwa obrona tamtego wyjścia.
Liczby nie podałby przy tym żadnym kosztem,
a pamięć podręczna pod pozycją, czyli to, co go trzyma poniżej wykładniczej,
z leniwym wyliczaniem sama się nie składa.

Role, o które czytania się różnią, wychodzą z lasu tą samą drogą.
Streszczeń jest najwyżej `MAX_READINGS`,
więc rola, którą rozdziela dopiero sześćdziesiąte piąte czytanie,
nie zostałaby z nich nazwana,
a liczba obok niej granicy nie ma i tej niezgody po sobie nie pokazuje.
Tak stoi
[przepis o dziesiątkach tysięcy czytań](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem):
werdykt nazywa tam dopełnienie, którego wypisane czytania nie rozdzielają.
Kosztuje to jedno rozstrzygnięcie, którego lista czytań nie potrzebuje.
Etykieta roli pada w jednym czytaniu kilka razy,
bo zdanie współrzędne ma własny podmiot,
więc nad lasem trzeba powiedzieć,
które pozycje jednej etykiety są tym samym wystąpieniem.
Jest nim to, które nazywa streszczenie, czyli pierwsze.

Pierwsze w zdaniu streszczanym, a nie w zdaniu podrzędnym pod nim.
Oba podsumowania zatrzymują się na zdaniu względnym i dopełnieniowym,
bo rola z ich wnętrza należy do nich, a nie do zdania nad nimi:
`Reguła, która rozstrzyga o zdaniu, jest tania.` ma czasownik `jest`,
a bez tego zatrzymania werdykt nazywa czasownikiem `rozstrzyga`,
czyli mówi o zdaniu nieprawdę.
Zatrzymać się muszą oba naraz,
bo inaczej wiersz `differing in` nazywa rolę,
której lista czytań pod nim nie nazywa.
Zdania współrzędnego to nie obejmuje,
bo jego role należą do tego samego zdania.

Trzeci wiersz nazywa konstytuent i odpowiada tam, gdzie tamte dwa nie sięgają.
Streszczenie pokazuje wypełnienie roli oraz gospodarza przyłączenia,
więc dwa czytania różne czymkolwiek innym wychodzą z niego jednym napisem.
Miejsca takie są dwa.
`Dodatkowych przedstawicieli wyznacza zainteresowana rada gminy.`
różni czytanie słownikowe wewnątrz wypełnienia jednej roli —
`zainteresowana` jest tam i rzeczownikiem, a `rada` formą `rad` —
a `Ustawa mówi, że organ gminy wydaje przepis.` różni podmiot i dopełnienie
zdania podrzędnego, w które streszczenie nie zagląda.
Lista czytań zdania o tej różnicy milczy, bo oba czytania mają w niej jeden wpis,
więc bez tego wiersza werdykt mówi nad każdym z tych zdań samo `2 odczytania`,
czyli nie mówi, czym te dwa czytania się różnią.
Z nim mówi `„zainteresowana rada gminy” ma 2 odczytania`.

Nazwany jest konstytuent, a nie różnica pod nim,
i tę granicę stawia tożsamość czytania:
lemat i część mowy są z niej wyłączone rozmyślnie,
więc wiersz nazywający lemat mówiłby o czymś,
czego liczba czytań obok niego nie liczy.
Wpis dostaje przy tym konstytuent najwęższy:
napis obejmujący napis innego wpisu mówi o tym samym słowie i o kilku obok niego,
bo wieloznaczność wychodzi w górę.
`równych praw kobiet` czyta się dwoma sposobami przez samo `równych`,
`równych praw kobiet i mężczyzn` trzema, a naprawić trzeba jedno słowo.

Samą różnicę pokazuje pod tym wierszem lista, o ile konstytuent jest zdaniem.
Streszczenie zdania podrzędnego jest streszczeniem tego zdania,
a nie tego nad nim, więc streszczone osobno mówi to, o czym wiersz milczy:

```sh
python3 -m olski.check --readings -c "Ustawa mówi, że organ gminy wydaje przepis."
```

```text
<text>: Ustawa mówi, że organ gminy wydaje przepis.
        2 odczytania; „organ gminy wydaje przepis” ma 2 odczytania
        - podmiot: Ustawa, orzeczenie: mówi
        „organ gminy wydaje przepis” czyta się tak:
          - podmiot: organ gminy, dopełnienie: przepis, orzeczenie: wydaje
          - podmiot: przepis, dopełnienie: organ gminy, orzeczenie: wydaje
zdań: 1; wieloznaczne: 1; bez odczytania: 0
```

Granicy między konstytuentem a różnicą pod nim lista nie rusza:
rola lematem nie jest, więc lista mówi o tym, co tożsamość czytania liczy.
Wierszy przy tym nie mnoży, bo stoi pod listą czytań zdania, a nie w niej:
zdanie o takim konstytuencie i sześciu przyłączeniach dostaje kilkanaście
wierszy zdania i dwa wiersze konstytuentu, a nie ich iloczyn.
Głębiej zagnieżdżenie nie sięga, bo wpis dostaje konstytuent najwęższy,
więc dwa wpisy jednego zdania stoją obok siebie, a nie jeden w drugim.
Bez listy zostaje grupa imienna, bo roli zdania nie nosi.
Jej streszczenia wychodzą puste i sobie równe, więc zostaje z nich jedno,
a różnicę niesie tam głowa, której streszczenie nie nazywa
([`todo/`](../todo/README.md)).

Wykluczenia są trzy i każde odpowiada jednemu wierszowi,
który werdykt drukuje bez tego podsumowania.
Ciąg współrzędny wiersza nie dostaje, bo granicę członu pokazuje nawias w napisie roli.
Konstytuent z rolą pod sobą — z tą, do której streszczenie zagląda —
nie dostaje go, bo o tej roli mówi wiersz `differing in`.
Konstytuent z nazwanym przyłączeniem pod sobą nie dostaje go,
bo o tym wyborze mówi wiersz z gospodarzami,
a ten granicy zdania podrzędnego nie zna i sięga też do jego wnętrza.
Bez ostatniego z tych trzech zdanie o dwunastu czytaniach
dostawałoby te same dwa przyłączenia po raz drugi,
raz nazwane przyimkiem, a raz konstytuentem długim na całe zdanie podrzędne.

Cena idzie na to, o czym wiersz milczy, i widać ją na jednej klasie.
Nawias obejmuje ciąg, którym jest sama rola, a nie ciąg stojący w wypełnieniu głębiej,
więc dwa czytania różne nawiasowaniem takiego ciągu wychodzą jednym napisem,
a wiersz o konstytuencie ustępuje im miejsca:
`Ustawa określa zadania ochrony ludności i obrony cywilnej.`
zostaje samą liczbą czytań, choć raz są to zadania dwóch rzeczy, a raz jednej.
Ile zdań tak zostaje, mierzy
[disambiguation.md](disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca).

Lista czytań niesie przy tym każde streszczenie raz.
Powtórzone nie mówi nic ponad to, które stoi nad nim,
a powtórzeń bywa tyle, ile czytań schodzi się pod jednym napisem:
streszczenie nazywa pierwszy modyfikator zdania i jego gospodarza,
więc zdanie o sześciu wyrażeniach przyimkowych
wychodzi kilkunastoma wierszami na swoje sześćdziesiąt cztery czytania.
Liczby czytań lista przez to nie podaje, bo tę podaje las.
Reguła obowiązuje każdą z tych list, więc i tę pod konstytuentem:
i tam dwa kształty o jednym napisie stoją jednym wpisem,
a grupa imienna zostaje przez to bez listy.

Zdanie współrzędne zatrzymania nie ma, a streszczeń dostaje tyle,
ile ma zdań składowych, po jednym na składowe:

```sh
python3 -m olski.check --readings -c "Autor działa i zapisuje ustawienia."
```

```text
<text>: Autor działa i zapisuje ustawienia.
        - podmiot: Autor, orzeczenie: działa
          dopełnienie: ustawienia, orzeczenie: zapisuje
```

Kreska otwiera czytanie, a składowe następne stoją pod nim bez niej,
i widać po tym, że dopełnienie jest z innego zdania składowego niż podmiot.
Jedno streszczenie na zdanie nazywałoby pierwsze wystąpienie każdej roli,
czyli role zdania składowego pierwszego, i o reszcie zdania milczało:
`Wciśnij klawisz wu i zapisz plik konfiguracyjny.` wychodziłoby wtedy
jednym wierszem `dopełnienie: klawisz wu, orzeczenie: Wciśnij`,
z którego czytelnik odczytuje, że parser drugiej połowy zdania nie rozebrał.
Zdanie o dwóch składowych albo więcej jest w README co trzecie
([corpus.md](corpus.md#the-same-queue-over-prose) mówi, czym się ten plik czyta),
więc milczenie to nie jest przypadkiem z brzegu.
Granicą podziału jest przy tym początek składowego następnego,
a nie koniec poprzedniego,
więc rola stojąca między składowymi wpada do tego przed nią:
dopowiedzenie za dwukropkiem stoi poza każdym zdaniem składowym
i podział po końcach zostawiłby je bez streszczenia.

Cena tego podziału jest iloczynem i bierzemy ją świadomie.
Streszczenia różne wchodzą na listę każde raz,
a dwa składowe wieloznaczne każde na swój sposób
dają streszczeń tyle, ile jest par ich odmian:
jedno zdanie README wychodzi przez to kilkudziesięcioma streszczeniami
po trzy wiersze każde, gdzie streszczenie jedno na zdanie dawało kilka wierszy.
Iloczyn ucina `MAX_READINGS`, tak jak ucina listę czytań,
a płacą go zdania odrzucone już jako wieloznaczne:
zdanie `valid` ma jedno czytanie, więc dostaje po jednym wierszu na składowe.
Wpisu na składowe zamiast wiersza na czytanie ta lista nie ma,
choć zamieniłby ten iloczyn na sumę,
tak jak zamienia go wiersz o konstytuencie rozbieżnym;
co za to płaci, mówi [`todo/`](../todo/README.md).

Gospodarza nazywa jego głowa, czyli jedno słowo.
`w Rzeczypospolitej Polskiej` dochodzi do `Władza` albo do `należy`,
a `z dodatkami` do `szynki`, do `koszt` albo do `przewyższa`,
i po każdej z tych nazw widać, którą poprawkę autor ma rozważyć.
Nazwa wzięta z materiału poprzedzającego modyfikator tego nie daje,
i to jest powód, dla którego produkcja swoją głowę wyróżnia:
grupa imienna otwierająca zdanie dzieli ten materiał z całym zdaniem,
więc obaj gospodarze wychodzą jednym napisem,
a rozdziela je dopiero dopisany symbol konstytuenta —
`Władza zwierzchnia (grupa_imienna)` obok `Władza zwierzchnia (zdanie_składowe)` —
po którym wybór jest widoczny, a nie nazwany po imieniu.

Głowę wyróżnia znacznik `Głowa` wewnątrz ciała, a nie numer pozycji obok niego.
Numer myli się bez śladu: przestawione ciało zostawia go niezmienionym
i nikt tego nie zauważy, a znacznik przesuwa się razem ze swoją częścią.
Ciało o kilku częściach bez znacznika nie powstaje wcale,
więc produkcja dopisana bez głowy przerywa budowanie gramatyki na swoim wierszu,
zamiast nazwać gospodarza pierwszą córką, którąkolwiek by ona była.
Odmowę sprawdza `tests/test_gramatyka.py`,
a oba zdania z tymi werdyktami `tests/test_las.py`.

Las jest przy tym jeden, a werdykty są nad nim różnymi podsumowaniami:
czy cokolwiek się wyprowadza, ile się wyprowadza, czy najwyżej dwa,
i czy złote czytanie jest wśród czytań oraz jak głęboko,
o co [pomiar pyta bank drzew](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold).
Żadne z tych pytań nie żąda innego parsera, tylko innego podsumowania.

## Co się pakuje, rozstrzyga tożsamość czytania

Las odpowiada na pytanie olskiego pod dwoma warunkami:
pod jedną pozycję ma iść to, co jest jednym czytaniem,
a liczba z jednej pozycji ma się łączyć z liczbą z sąsiedniej tak,
jak łączy je unifikacja.
Pierwszy ma odpowiedź w gramatyce, a drugi dostał ją dopiero pomiarem.

Czytanie jest kwotowane po lematach, po wartościach cech i po częściach mowy
([subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie)),
więc pozycja tablicy trzymana osobno dla każdego środowiska cech
nie spakuje niczego i policzy wyprowadzenia zamiast czytań.
Jest to dokładnie ten błąd, który zapisuje
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure),
i ten, przez który
[obudowanie Świgry](swigra.md#why-wrapping-it-does-not-get-there)
jest pisaniem gramatyki po raz drugi.
Pozycja niesie więc etykietę i rozpiętość, i nic ponad to,
czyli dokładnie tyle, ile niesie sygnatura czytania.
Zarabia to na siebie na tym samym kwotowaniu:
`zapisuje` ma dwa lematy, a lemat do sygnatury nie wchodzi,
więc `Program zapisuje ustawienia.` wyprowadza się dwa razy na jedną pozycję,
i mnożyłoby się to przez każde następne słowo, któremu słownik daje dwa lematy.

Kosztuje to więzy, których nad taką pozycją nie ma jak postawić.
Rodzic widzi z córki etykietę, rozpiętość i cechy, które ona wypuszcza,
a dwa czytania różniące się wewnątrz jednej pozycji wychodzą do niego
jednym kształtem i jedną liczbą.
Warunek postawiony nad córką nie ma więc czym ich rozdzielić,
i nie jest to brak maszynerii, tylko granica tej decyzji:
pozycja, której cena ma stać na takim rozdzieleniu,
albo wypuszcza cechę, po której ją widać, albo dostaje osobny symbol.
Wpuszczenie okolicznika zdaniowego nad ciąg współrzędny poszło drogą pierwszą
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)),
a tym, co żadnej z nich nie ma, jest luka, czyli produkcja o pustym ciele
([design-notes.md](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)):
różni ją dokładnie to, czego pozycja o sobie nie mówi.

Na czym drugi warunek się rozchodzi, pokazuje zdanie, które olski przyjmuje:

```sh
python3 -m olski.check -c "Zobacz docs/subset.md."
```

Suma iloczynów po samych pozycjach liczy nad nim o jedno czytanie więcej,
niż ma ich to zdanie.
`wypełnienia` nad `docs/subset.md` budują się trzema produkcjami
z `olski/subset/zdanie.py` — przez `dopełnienie`, przez `orzecznik`
i przez okolicznik narzędnikowy —
bo [notacja rejestru](warstwa-leksykalna.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)
dostaje czytanie nieodmienne i stoi przez to w każdym przypadku.
Czytania są z tego dwa, bo okolicznik narzędnikowy dochodzi tu do czasownika
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)),
a orzecznik ginie u rodzica.
Obie są czytaniami tej rozpiętości, więc pakowanie stawia je pod jedną pozycją
i robi z nimi to, czego pierwszy warunek żąda.
Rozchodzi się dopiero to, czym pozycja jest dla rodzica:
`grupa_orzeczenia → orzeczenie wypełnienia` wiąże jedną wspólną zmienną
ramę czasownika z pozycją, którą dopełnienie zajmuje,
a `zobacz` ma ramę domyślną, w której narzędnika nie ma.
Rodzic wskazuje pozycję, a nie wariant,
więc liczy wszystkie trzy, choć unifikacja przepuściła dwa.

Nadmiar jest więc wzięty z przeciwnej strony niż ten wyżej:
tamten bierze się z rozdzielenia pozycji, a ten ze sklejenia.
Cena jest przy tym inna, bo olski pyta o liczbę czytań, a nie o czytania:
zdanie przyjęte wychodzi z takiego lasu dwuznaczne,
czyli przewraca się werdykt, a nie sama liczba obok niego.

Wyjścia są z tego dwa i tańsze jest drugie, bo pierwsze zmierzono i liczy gorzej.
Pierwszym jest pozycja rozszczepiona po cechach, które wypuszcza:
dwa warianty `wypełnienia` z tego zdania stoją wtedy w tablicy osobno,
para nieunifikująca się nie powstaje wcale i to zdanie wychodzi z jednym czytaniem.
Rozszczepienie idzie po cechach wypuszczanych, a nie po całym środowisku,
więc jest węższe od tego, przed którym broni pierwszy warunek wyżej —
ale nie dość węższe, i widać to na zdaniu, które olski przyjmuje tak samo:

```sh
python3 -m olski.check -c "Projekt jest dla przyjemności."
```

`przyjemności` ma pięć czytań, więc `grupa_imienna` nad nim rozszczepia się na pięć pozycji,
a `dla` przepuszcza z nich dwie, obie w dopełniaczu i różne liczbą.
`wyrażenie_przyimkowe` nad tym przypadka ani liczby nie wypuszcza,
więc obie wracają pod jedną pozycję jako dwa wyprowadzenia jednego kształtu,
i suma iloczynów liczy nad tym zdaniem dwa czytania zamiast jednego.
Nadmiar wychodzi więc rozszczepieniu tam,
gdzie cecha, która pozycje rozdzieliła, ginie u rodzica,
a stamtąd ten iloczyn idzie w górę aż do korzenia.

Stoi więc wyjście drugie: iloczyn liczony po parach, które unifikacja przepuszcza,
co zostawia tablicę spakowaną i przenosi koszt z pakowania do liczenia.
Tak liczy `Las.klasy` w `olski/parse/las.py`:
kształty jednej pozycji stoją w klasach po tym, jakie cechy wypuszczają,
i kombinacja klas, której produkcja nie składa, nie wnosi ani jednego czytania.
Miarą, wobec której oba warianty zmierzono, był enumerator zstępujący,
który tę tablicę zastąpiła —
on środowisko cech niósł w dół rozbioru zamiast pod pozycją,
więc pary nieunifikującej się nie liczył.

Zmierzono je trzema przebiegami nad dwoma korpusami,
bo pozycje rozdziela dopiero forma stojąca w zdaniu.
Liczby niżej są ceną, za jaką odrzucono rozszczepienie,
i nie ma ich po co przeliczać:
sonda, która je wzięła, poszła razem z enumeratorem będącym jej miarą,
a wariant, który mierzyła, nie stoi w kodzie i nie ma jak się zmienić.
Zdania, na których widać oba nadmiary, trzyma `tests/test_las.py`,
więc podstawa tego wywodu nie zniknie po cichu.

Nad 13025 zdaniami Składnicy pod morfologią własną
rozszczepienie rozdziela 31.6% pozycji, czyli 126814 rośnie do 189880,
a najdalej rozdzielona pozycja idzie na dziesięć.
Tablica spakowana liczy nad 56 zdaniami więcej czytań, niż zdanie ma,
i przewraca przy tym 12 werdyktów, wszystkie z `valid` na `ambiguous`;
tablica rozszczepiona myli się nad 224 zdaniami i przewraca 85.
Trzy zdania z tego mianownika nie mają się z czym porównać,
bo wyliczanie stanęło na nich na `MAX_READINGS`, a tablica granicy nie ma.
Nad prozą README, która miała wtedy 43 zdania,
pozycji przybywa w tej samej krotności — 811 rośnie do 1218 —
a każdy wariant myli się nad dwoma zdaniami.
Rozszczepienie kosztuje więc półtorej tablicy,
a zdań liczy źle cztery razy tyle, co tablica, którą ma naprawiać.

Trzeci przebieg mówi, skąd tych liczb nie brać.
Pod złotą morfologią rozdziela się 71 pozycji z 71877
i żaden wariant nie myli się ani na jednym zdaniu,
bo anotatorzy wybrali po jednym czytaniu na terminal,
a nadmiar bierze się z formy, której słownik daje ich kilka.
Liczba stamtąd byłaby liczbą o anotacji, a nie o gramatyce.

## Więzy wchodzą wyprowadzone z gramatyki, a nie napisane obok niej

Sonda więzowa, czyli ten sam podzbiór powiedziany łukami zamiast produkcjami
([design-notes.md](design-notes.md#podłoże-więzowe-zmierzone-sondą)),
pokazała dwie rzeczy, które więzy robią taniej niż produkcja:
przycinanie dziedzin przed szukaniem drzewa
i powiedzenie, na czym odrzucenie stanęło.

Kryterium, po którym taka warstwa wchodzi, jest jedno:
musi się wyprowadzać z gramatyki.
Napisana obok niej jest gramatyką napisaną dwa razy,
czyli tym drugim właścicielem faktu, przed którym broni
[`CLAUDE.md`](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely),
i jest to ten sam zarzut, który przewraca obudowanie Świgry
oraz ten, który [`todo/`](../todo/README.md) stawia `harness/polszczyzna.py`.
Wyprowadzona nie kosztuje ani jednej deklaracji.

Najtańszym kawałkiem takiej warstwy jest licencja terminala,
czyli pytanie, czy czytanie formy bierze jakikolwiek `Word` w gramatyce.
`licencjonuje` w `olski/grammar.py` stawia je wobec `EMPTY`,
i wolno tak, bo unifikacja tylko zawęża:
czytanie, którego bez środowiska nie bierze żaden terminal,
nie przejdzie przy żadnym.
Warunek na czytanie stoi przy tym raz, w `bierze` obok niej,
i pytają o niego rozbiór i licencja,
bo dwie kopie tego warunku byłyby dwoma właścicielami tego samego faktu
tak samo jak warstwa napisana obok gramatyki.

Drugi z dwóch zysków wychodzi z tego prawie wprost.
Forma, której w ten sposób nie zostaje ani jedno czytanie,
jest tym, na czym odrzucenie stanęło, i werdykt ją wypisuje:

```sh
python3 -m olski.check -c "Prozę w tym repozytorium łamiemy według Semantic Line Breaks, a nową piszemy po polsku."
python3 -m olski.check -c "Nowa program zapisuje ustawienia."
```

Pierwsze zdanie stoi na nazwie obcej przytoczonej bez cudzysłowu,
a drugie ma każdą formę wziętą i stoi na zgodności rodzaju.
Są to dwie różne odpowiedzi i dwie różne roboty do zrobienia,
i dlatego werdykt je rozdziela, tak jak
[rozdziela je Świgra](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold).

Owo „prawie” jest jedną rzeczą i bierze się stąd, że segmenty są krawędziami
grafu, a nie listą.
Morfeusz dzieli `Ktoś` na `Kto` i `ś` obok formy całej,
a `ś` nie ma ani jednego czytania, które bierze jakakolwiek produkcja,
i nie jest przy tym słowem, które ktokolwiek napisał.
Werdykt nazywa więc nie każdą pustą dziedzinę,
tylko krawędź, bez której nie ma drogi przez zdanie,
i `Ktoś zna docs/subset.md.` wychodzi przez to przyjęte, nie mówiąc o `ś` nic.
Zdanie, które ma czytanie, nie zgłasza tym samym żadnej formy,
i nie zgłasza jej z dowodu, a nie z przybliżenia:
ścieżka, którą to czytanie się wyprowadza, omija każdą krawędź, której nie wzięła.
Sonda tego pytania nie miała, bo
[zdania o rozchodzącym się grafie nie rozbiera wcale](design-notes.md#podłoże-więzowe-zmierzone-sondą).

Pierwszego zysku nie ma, a cena za niego stoi poza parserem.
Czytanie bez licencji nie zmienia dziś żadnego werdyktu,
bo `terminal` w `olski/parse/tablica.py` odrzuca je tak samo,
ani nie rusza `furthest`, który idzie w górę wyłącznie po dopasowaniu udanym,
więc wycięcie takiego czytania przed rozbiorem oddaje ten sam `Result`, tylko szybciej.
Rusza się co innego: `bloker` w `olski/pokrycie.py`
nazywa część mowy pierwszego czytania formy,
więc formie wyciętej do zera nazwałby brak struktury zamiast braku licencji,
a na tym odczycie stoi kolejka z [corpus.md](corpus.md#where-the-analyses-stop).
Wycięcie jest więc zmianą w kolejce, a nie w parserze,
i [`todo/`](../todo/README.md) trzyma je razem z przebiegiem, który jest winne.

## Kierunek: produkcja się rozwarstwia, a podłoże zostaje

Wychodzi z tego kierunek i nie jest nim zmiana podłoża.
Produkcja zlewa w jedno trzy rzeczy,
i te trzy [sonda](design-notes.md#podłoże-więzowe-zmierzone-sondą) rozdziela:
zgodność, porządek i to, że konstytuent jest jednym odcinkiem tekstu.
Każda z nich ma wyjście, które zostaje przy szczeblu 2
[drabiny](design-notes.md#the-cost-ladder).
Zgodność wyszła do cech, zanim to pytanie stanęło.
Porządek wyszedł do warunków precedencji:
deklaracja wymienia córki, warunek obok niej mówi, które przestawienia wchodzą,
a rozwinięcie składa jedno z drugim przed rozbiorem
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Spójność wychodzi do luki przeciąganej przez ciąg o swobodnym szyku,
więc [urwisko](design-notes.md#the-cliff-discontinuity) wycenia szczebel, a nie zjawisko.
Zostaje w produkcji to jedno, czego z niczym nie zlewa:
z czego konstytuent się składa.

Walencji produkcja nie mówi wcale, i jest to brak innego rodzaju niż tamte trzy.
Nie ma jej skąd wyprowadzić, bo stoi w leksykonie,
a dopisana produkcjami mnoży je przez czasowniki,
co [etap 2](roadmap.md#etap-2-walencja) liczy jako powód swojej kolejności.
Wchodzi więc cechą, którą czasownik niesie z leksykonu,
a to, co przy nim stoi, żąda w niej swojej pozycji
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)).
Mówi przez to, co czasownik bierze, i nie mówi, ile tego bierze:
liczba dopełnień zostaje w produkcjach,
a rama, która się zużywa, jest tym, czego olski nie ma i co pokazuje
[Świgra](swigra.md#valency-as-a-resource-that-gets-consumed).

Między dwoma wyjściami z nieciągłości rozstrzyga wydruk.
Sonda zdejmuje spójność jednym warunkiem globalnym
i traci nazwanie podmiotu napisem,
bo poddrzewo bez spójności jest zbiorem słów, a nie odcinkiem tekstu.
Luka oddaje pożyczone żądanie frazie, która je pożyczyła,
więc rozpiętość zostaje odcinkiem tekstu,
a werdykt olskiego wypełnioną rolę nazywa napisem.
Ile polszczyzny oddaje dyscyplina jednej luki, nie mówi żadne z dwóch wyjść,
i [Świgra tego też nie mówi](swigra.md#one-gap-instead-of-a-different-complexity-class);
a to jest ten pomiar, który cały ten kierunek by przewrócił.

Kolejność bierze się z tego, czego która rzecz potrzebuje,
i reguła, którą trzy pierwsze wyłożyły, obowiązuje czwartą.
Las szedł pierwszy, bo produkcji nie rusza,
więc dał się porównać werdykt po werdykcie z tym, co stało.
Walencja szła przed precedencją, bo kasuje czytania,
a rozwinięcie permutacji je dopisuje,
i bez lasu nie było czym przeczytać, ile ich dopisze:
dopisało cztery ciała i ani jedno nie jest permutacją
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Ruch, który czytania dopisuje, idzie więc za każdym, który je kasuje,
i to jest wszystko, co ta kolejność mówi luce.

Las przesunął przy tym granicę, za którą podłoże zostaje.
Enumerator zstępujący wołał `bierze` i `unify` w środku obchodzenia wyprowadzeń,
z środowiskiem cech niesionym w dół,
więc zgodność była wpleciona w sam rozbiór.
Tablica Earleya o cechy nie pyta wcale,
a unifikacja przechodzi po lesie osobno i w jednym miejscu:
`_sposoby` w `olski/parse/las.py` rozstrzyga, czy córka pasuje do rodzica,
i nikt poza nim tego nie rozstrzyga.
Warunek precedencji miał się więc gdzie wpisać —
`_przejdź` dostaje ciało wraz z rozpiętościami córek,
czyli dokładnie to, o co taki warunek pyta —
i nie żądał rozwinięcia permutacji po to, żeby zostać wypowiedzianym.
Wpisał się mimo to przed rozbiorem, a nie w lesie,
bo warunek pytany o rozpiętości odpowiada raz na wyprowadzenie,
a ten sam warunek rozwinięty odpowiada raz na gramatykę.
Rozwinięcie zostaje przez to wyborem o liczbę czytań, a nie ceną wejścia,
i drugi z dwóch odbiorców tego warunku — luka — czeka po tamtej stronie granicy:
pozycji w napisie nie pilnuje pozycja w ciele
([lukę zmierzono](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).

Urwiska to nie dotyka i nie ma udawać, że dotyka.
Pozycja lasu jest jednym odcinkiem tekstu,
a luka przeciągana przez ciąg żąda zbioru odcinków,
więc tam przerabia się tablicę, a nie warstwę nad nią,
i szczebel zostaje wyceniony tak, jak wycenia go
[urwisko](design-notes.md#the-cliff-discontinuity).

Zostaje droga trzecia, czyli formalizm leksykalizowany,
i odpada ona na tym samym kwotowaniu.
Gramatyka kategorialna kupuje swobodny szyk kompozycją,
a płaci wieloznacznością pozorną:
jedna struktura zależności ma w niej wiele wyprowadzeń.
Kwotowanie po niej nazywa się postacią normalną i trzeba je utrzymywać,
czyli jest to ta sama robota, którą wycenia
[tożsamość czytania](#co-się-pakuje-rozstrzyga-tożsamość-czytania),
tylko wniesiona do własnej gramatyki zamiast napotkanej w cudzej.

## Cechy biorą to, co zawęża, jest symetryczne i lokalne

Zgodność zeszła z produkcji do cech,
a warto powiedzieć, co ją tam wpuściło,
bo to samo pytanie stoi przed każdą następną rzeczą,
którą ktoś zechce z produkcji wyprowadzić.
Unifikacja wzięła zgodność, bo zgodność ma trzy własności naraz:
przecięcie zbiorów tylko zawęża,
zgodność jest symetryczna między dwoma wiązkami cech,
a rozstrzyga się nad samą tą parą, bez oglądania się na resztę zdania.
Rzecz, która ma te trzy, kosztuje jedną zmienną.
Rzecz, której którejś brakuje, kanału cech nie dostaje,
i w tym repozytorium widać każdą taką wychodzącą bokiem.

Wykluczenie lematu nie zawęża, więc stoi poza `unify`.
`bez_lematów` w `olski/grammar.py` jest osobnym polem i osobnym testem,
bo przecięcie zbiorów nie ma jak powiedzieć „nie” o lemacie.
Monotoniczność, spod której ten warunek ucieka, jest przy tym nośna:
`licencjonuje` pyta wobec `EMPTY` i odpowiada poprawnie tylko dlatego,
że unifikacja nigdy nie poszerza,
co [więzy wyprowadzone z gramatyki](#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)
biorą za darmo.
Wykluczenie płaci więc polem za to,
z czego wszystko obok niego żyje,
i płaci nim na każdy zasięg, o jaki pyta:
osobne pole ma wykluczenie czytania, osobne wykluczenie całej formy
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)).

Żądanie obecności cechy ucieka temu przecięciu z drugiej strony
i stoi poza `unify` z tego samego powodu.
`niesie` w `olski/grammar.py` mówi, że forma ma cechę nieść,
a przecięcie zbiorów nie ma jak tego powiedzieć:
cecha nieobecna jest pomijana, więc wypisanie wszystkich jej wartości
znaczy dokładnie tyle, co milczenie.
Warunki poza unifikacją są przez to dwa i oba pytają o formę,
a nie o zgodność między dwiema wiązkami cech:
jeden odmawia lematowi, drugi formie, która cechy nie niesie.
Kupuje to klasę, którą tagset rozdziela, a produkcja nie umiała zażądać —
przysłówek odprzymiotnikowy niesie stopień, a pierwotny nie —
i tyle wystarcza, żeby przymiotnik brał jednego z nich
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#naprawę-niesie-tagset-a-formalizm-ją-bierze)).

Żądanie odwrotne — że część tej cechy nie niesie — pola nie potrzebuje,
bo jest dolnym krańcem żądania wartości, które unifikacja ma.
Więz na zbiór wpuszcza konstytuent niosący którąś z wypisanych wartości,
a obok niego ten, który cechy nie niesie wcale i przez to się z nią nie kłóci.
Więz na zbiór pusty wpuszcza więc tego drugiego i tylko jego
(`NIE_NIESIE` w `olski/grammar.py`).
Żąda tak gramatyka gospodarza bez dostawki
oraz wypełnienia bez drugiej pozycji ramy,
czyli tam, gdzie cechę niesie jedna strona, a druga o niej milczy.

Powiedzieć to samo wartością, której nikt nie wypuszcza, też się da,
i jest to alternatywa odrzucona.
Płaci się za nią sprawdzeniem martwych więzów:
taka wartość wygląda dokładnie tak jak literówka w wartości,
więc sprawdzenie musi wtedy milczeć o każdym więzie na cechę,
o której choć jedna produkcja gospodarza milczy
(`więzy_niespełnialne` w `olski/grammar.py`).
Rozdzielone mówią po jednej rzeczy,
a sprawdzenie orzeka o każdym więzie na wartość, nie tylko o części z nich;
że nie pomija żadnego, wypisuje `więzy_nierozstrzygnięte` obok niego.

Rodzaj grupy współrzędnej nie jest symetryczny między członami,
bo polszczyzna wylicza go regułami, których unifikacja nie umie powiedzieć,
więc taka grupa nie niesie tej cechy wcale i `olski/subset/grupa.py` mówi to
przy tej produkcji.
Działa to dlatego, że `unify` pomija cechę, której konstytuent nie ma,
czyli tą samą linią, którą nieodmienna część mowy jest niewinna zgodności.
Nieobecność jest tu mechanizmem, a nie dziurą.

Negacja weszła tym kanałem, nie mając ani drugiej własności, ani trzeciej.
Rządzenie nie jest symetryczne — czasownik żąda przypadka od dopełnienia,
a dopełnienie od czasownika nie żąda niczego — i nie rozstrzyga się nad parą,
bo dopełniacz negacji sięga pod bezokolicznik przez łańcuch dowolnej długości
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)).
Przeszła dzięki pierwszej własności, czyli tej, na której stoi unifikacja:
wartości są dwie, przecięcie tylko zawęża,
a kierunek żądania zapisuje się jednostronnie —
ciało z cząstką ogłasza `neg`, ciało bez niej `aff`,
a dopełnienie mówi, przy którym z nich stoi.
Płaci za to ścieżką, którą trzeba przeprowadzić przez każdy konstytuent,
w którym cecha nie idzie od głowy:
`orzeczenie` ogłasza ją z cząstki stojącej obok niego,
a fraza bezokolicznikowa z własną cząstką ma jej nie wypuszczać.
Zgodność takiej ścieżki nie potrzebuje wcale, bo przypadek, liczbę i rodzaj
konstytuent bierze od swojej głowy sam (`olski/grammar.py`).
Pierwsza własność wpuszcza więc rzecz do kanału, a dwie pozostałe rozstrzygają,
czy wjedzie za darmo.

Walencja weszła tym kanałem i wypadła na lokalności.
Rama jest stanem, a nie zasobem, więc pozycji już zajętej nie ma jak odnotować,
a zajęcie zależy od pozostałych córek, a nie od samej pary głowy i zależnego.
Sonda zapłaciła za to samo dwoma polami:
`wymaga` i `zakazuje` w `harness/wiezy.py` mówią o łukach jednej głowy naraz,
więc sprawdza je `_dopuszczalne`, gdy drzewo stoi już całe,
a nie tablica licencji, która stoi policzona przed szukaniem.
Co z tego zostaje po stronie produkcji,
mówi [kierunek](#kierunek-produkcja-się-rozwarstwia-a-podłoże-zostaje) wyżej.

## Wyliczone ciało myli się w stronę werdyktu

Pozycja, której gramatyka nie ma, zdania nie odrzuca:
wypuszcza je jednym czytaniem, czyli wybiera przez przeoczenie.
Wywód wraz z listą takich pozycji i z ceną nad Składnicą trzyma
[subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
Zostaje do tego dopisać kierunek, w którym ta pomyłka idzie,
bo on mówi, ile ona waży.

Zawężanie liczby czytań ma tu właścicieli wyłożonych i jednego niewyłożonego.
`admissible` w `olski/segmentacja.py` odbiera czytanie, którego polszczyzna nie ma,
warunek na [zaimek rzeczowny](konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)
odbiera grupie imiennej drugie czytanie tego samego kształtu,
a `signature` w `olski/parse/czytanie.py` liczy dwa wyprowadzenia jako jedno czytanie.
Każde z tych trzech jest pojedynczą decyzją z wywodem i z ceną:
pierwsze wykłada [kryterium słownikowe](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not),
a ostatnie jest czterema wierszami, które ruszają każdy werdykt,
choć nie ma w nich ani jednej produkcji.
Lista ciał zawęża przez to, czego w niej nie ma,
i tym się od tamtych różni: rośnie z każdą konstrukcją,
nie ma jednego miejsca, w którym da się o nią spierać, i nie mierzy jej nic.

Reszta tej drogi myli się w drugą stronę i dlatego nie waży tyle samo.
Lemat, którego leksykon nie wymienia, dostaje ramę domyślną wraz z jej biernikiem,
a cecha, której forma nie niesie, jest przez `unify` pomijana:
jedno i drugie dokłada czytania, więc zdanie wychodzi wieloznaczne,
a wieloznaczność jest werdyktem, który ktoś przeczyta.
Zdanie przyjęte czyta się inaczej, bo po nie ten tor jest.
Wyjątkiem jest zdanie leksykonu twierdzące — o celowniku i o dopełniaczu —
bo tam milczenie o lemacie pozycję odbiera i zdanie z nią pada
([warstwa-leksykalna.md](warstwa-leksykalna.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)).
Odrzucenie nazywa formę, na której analiza stanęła, więc czyta je ten sam ktoś,
a wpis dopisany do leksykonu jest tańszy niż produkcja.

Warunki precedencji zabrały z tej listy pozycję ostatnią,
bo miejsce zadeklarowane raz nie ma jak zostać zapomniane w jednym z ciał,
i zabrały ją z ceną, którą widać: cztery ciała, jakich gramatyka pisana ręką nie miała
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)).
Wyceną ruchu to nie było — tę zrobiła liczba deklaracji zmierzona
[sondą](design-notes.md#podłoże-więzowe-zmierzone-sondą) —
tylko tym, co się przy nim kupiło poza nią.
