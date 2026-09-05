# Cechy, więzy i pytania do gramatyki

`GRUPA_JEDNYM_SŁOWEM` w `olski/segmentacja.py` wypisuje części mowy,
którymi grupa imienna staje sama jednym słowem,
czyli fakt o gramatyce zapisany drugi raz obok niej.
Głowa dopisana do grupy imiennej tej listy nie ruszy,
a wtedy przytoczenie zamieni czytania napisowi, który cudzysłów bierze już jako grupę,
i napis dostanie drugie czytanie albo straci rodzaj
([`docs/konstrukcje-gramatyczne/zdanie-złożone.md`](../docs/konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).
Rozjazdu nie widzi ani suita, ani przebieg nad prozą:
statusy ruszy dopiero napis z nową głową postawiony w cudzysłowie.
Ruchem jest pytanie gramatyki wprost, zamiast trzymania listy —
`Grammar` odpowiada dziś, czy terminal bierze czytanie
(`licencjonowane` w `olski/segmentacja.py`),
a brakuje odpowiedzi, czy bierze je terminal w produkcji grupy imiennej.
Do rozstrzygnięcia jest, czy to pytanie warto do `Grammar` dopisać,
czy taniej jest pilnować listy testem, który dla każdej głowy grupy
żąda jednego czytania od napisu w cudzysłowie.

`NIE_WYPUSZCZANE` w `olski/subset/deklaracja.py` wylicza cechy, których symbol nie niesie
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
(liczba i rodzaj `rdzeń_pytajny`, wypisane razem z rodziną względną,
której poprzednik ich żąda).
Zdjęcie listy jest zmianą w gramatyce i pomiaru żąda osobno:
proza tego repozytorium nie rusza się wcale, a banku drzew nie zmierzył nikt.
Osobno stoi czas rozbioru, bo cechę wypuszczaną las rozdziela na klasy pozycji
(`klasy` w `olski/parse/las.py`), a wpisów jest kilkadziesiąt.
Do przeczytania jest `_wysunięta_rola` w `olski/subset/podrzędne.py` obok tej listy,
bo tamta funkcja pisze dwie rodziny czoła jedną ręką i stąd te dwie cechy.

Gramatyka umie powiedzieć, że symbol cechę wypuszcza, a nie umie, że wypuszcza ją zawsze.
Produkcja, w której dwie córki wiążą jedną zmienną do zbiorów rozłącznych,
nie domyka się tak samo jak ta z więzem martwym, a dziś nie widzi jej nic,
bo `wiązanie` w `olski/grammar.py` sumuje wtedy córki, zamiast je przecinać,
i sumuje rozmyślnie: córka milcząca o cesze zmiennej nie zawęża.
Przeciąć wolno dopiero te córki, które cechę niosą w każdym swoim wyprowadzeniu,
więc sprawdzenie żąda drugiego punktu stałego, po tym, co część niesie na pewno,
wraz z inwentarzem cech, które dana część mowy niesie zawsze —
ten wychodzi z tagsetu Morfeusza, przecięciem cech tagów jednej części mowy,
i podaje się go tą samą drogą co inwentarz wartości.
Punkt stały liczy się przy tym po zaprzeczeniu, czyli po tym,
że jakieś wyprowadzenie części tej cechy nie niesie:
liczony wprost nie potwierdza symbolu, który stoi we własnym ciele,
a stoją tam `grupa_imienna` i `zdanie_składowe`, czyli gospodarze większości więzów.
Do przeczytania jest, ile ta klasa jest warta:
nad dzisiejszą gramatyką pada zero, więc jest to zabezpieczenie, a nie naprawa.
Zabezpiecza przy tym drugą rzecz, i tę wnosi dopiero żądanie ujemne pisane pustym
zbiorem (`NIE_NIESIE` w `olski/grammar.py`): zbiór policzony i pusty przez pomyłkę
czyta się odtąd jako to żądanie, a nie jako więz martwy.
Połowę takich pomyłek łapie `więzy_niesprawdzane`, bo pyta o samą nazwę cechy,
a drugiej — pustego żądania na cesze, którą część niesie zawsze — nie łapie nic.
Więzów na wartość ten ruch nie kupuje żadnych:
`więzy_nierozstrzygnięte` w `olski/grammar.py` wypisuje dziś pustkę,
czyli `więzy_niespełnialne` orzeka o każdym z nich i bez tego punktu stałego.

Wartość, która mówi samo „nie”, bywa do zdjęcia, odkąd żąda się milczenia wprost.
`BEZ_KOPULI`, `BEZ_CIĄGU` i `BEZ_ROZDZIELNEJ` w `olski/subset/słowa.py`
stoją w parze z wartością dodatnią dlatego, że żądania ujemnego nie było jak napisać
inaczej niż wartością, a pustym więzem jest ono jednym znakiem
(`NIE_NIESIE` w `olski/grammar.py`).
Ruchem jest para po parze: produkcja o cesze przemilcza,
a ta, która żądała wartości ujemnej, żąda milczenia.
Do przeczytania jest przy każdej parze, kto tę cechę czyta i po co:
`czoło` jest tu przypadkiem osobnym, bo wartość niesie tam etykietę roli,
a nie samo „nie”
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza)).
Pułapką jest kanał zmienny: strona, która przemilczy, przestaje zmienną wiązać,
a druga wiąże ją wtedy, czym chce.
Tak stoi `druga` w `olski/subset/rama.py` i dlatego czasownik ogłasza `BEZ_DRUGIEJ`
wartością, choć wypełnienie żąda po drugiej stronie milczenia.
Ceną jest pomiar: cechę wypuszczaną las rozdziela na klasy pozycji
(`klasy` w `olski/parse/las.py`), więc zdjęcie wartości rusza czas rozbioru,
a werdyktów ruszyć nie ma prawa i dowodzi się tego odciskiem prozy
(`harness/cytaty.py`).

O kształt produkcji pyta jedenaście plików i każdy pisze własną pętlę.
Po `GRAMMAR.productions` chodzą `harness/ruch.py`, `harness/luka.py`,
`harness/cena.py` i `harness/odcisk.py` oraz siedem plików testowych,
a każdy z nich sam rozstrzyga, co liczy jako ciało koordynujące
albo jako parę ciał okalających.
Kryterium jest przez to napisane kilka razy, a rozjazdu nie łapie żaden check,
bo każda kopia odpowiada nad swoim wycinkiem produkcji.
Ruchem są pytania w `olski/grammar.py` — o ciała danego symbolu,
o ciała koordynujące, o głowę ciała — zadawane zamiast pętli;
tak samo pyta się dziś o nazwy pozycji, których `olski/skład/rozbiór.py`
nie przepisuje, tylko bierze z `olski/subset/deklaracja.py`.
Drugą połową ruchu jest sześć nazw, którymi gramatyka odpowiada o własnych usterkach
(`undefined`, `nieosiągalne` i cztery o więzach w `olski/grammar.py`):
odpowiadają w trzech różnych kształtach,
a zależności między dwiema z nich, którą nazywa wpis o drugim punkcie stałym,
nie widać w żadnej z tych sygnatur.
Do przeczytania jest przedtem, czy te kopie pytają o to samo:
predykat sondy odsiewa produkcje po to, żeby je zdjąć,
a test podzbioru po to, żeby o nie zapytać,
więc wspólne pytanie opłaca się dopiero wtedy, gdy kryterium jest jedno.
Nie jest to druga deklaracja podzbioru:
pytanie odpowiada także za produkcję dopisaną po nim, a lista nazw nie odpowiada.
