# Warstwa leksykalna i wykluczenia

Wykluczenie słownikowe wywodzi z kształtu to, co słownik deklaruje wprost.
`admissible` w `olski/segmentacja.py` odbiera czytanie rzeczownikowe formie,
którą olski czyta jako słowo klasy zamkniętej, po kryterium nieodmienności,
a Morfeusz opatruje dokładnie te czytania kwalifikatorem dziedziny:
`do` w znaczeniu nuty niesie `muz.`, `go` w znaczeniu gry niesie `gry`,
a `at`, `cent` i `real` niosą `monet.`
Ruchem jest przeczytać, ile z tego, co `admissible` odbiera nad korpusem
audytowym, niesie taki kwalifikator, i ile niesie go czytanie, którego ono nie
odbiera — bo dopiero druga liczba mówi, czy kryterium dałoby się zastąpić listą.
Do rozstrzygnięcia jest przy tym, że lista byłaby druga i osobna od
`POZA_REJESTREM` w `olski/rejestr.py`: `muz.` i `gry` nazywają dziedzinę,
a dziedzina rejestru nie odsyła i odsyłać nie może,
bo `anat.` przy `oczy` wskazuje czytanie trafne
([`docs/formy-i-leksemy.md`](../docs/formy-i-leksemy.md#kwalifikator-mówi-o-formie-dwie-rzeczy-i-tylko-jedna-jest-rejestrem)).

`POZA_REJESTREM` w `olski/rejestr.py` nie ma nazw, które analiza nad korpusami wydaje.
Listę zebrano syntezą nad lematami, które to repozytorium ma
([`docs/formy-i-leksemy.md`](../docs/formy-i-leksemy.md#kwalifikator-mówi-o-formie-dwie-rzeczy-i-tylko-jedna-jest-rejestrem)),
a analiza nad prozą tego repozytorium i nad Składnicą wydaje obok niej
`daw._dziś_fraz.` przy `wobec`, `daw._dziś_rzad.` przy `nadziejny`
oraz `niepopr.` przy `czym` i przy `te`.
Dwie pierwsze są nazwami rejestru, więc przechodzą dziś jak nazwa dziedziny.
Trzecia jest do rozstrzygnięcia, bo `niepopr.` orzeka o normie, a nie o rejestrze,
i wpisana odsyłałaby formę, której ten rejestr używa.
Ruchem jest przebieg analizy po obu korpusach wypisujący nazwy spoza listy,
a po nim decyzja o każdej z osobna.
Do przeczytania jest przedtem, komu nazwa dopisana zmienia odpowiedź:
skład formę odesłaną zdejmuje (`olski/skład/morfologia.py`),
a analiza dokłada jej pozycję cennika i czytania nie zabiera.

Okolicznik przysłówkowy bierze całą część mowy, a Morfeusz daje czytanie `adv`
formom, których ten rejestr używa jako przyimka, spójnika albo przymiotnika:
`wobec`, `gdy`, `sam`.
Wychodzą z tego czytania, których polszczyzna w tych miejscach nie ma —
`postępować wobec innych w duchu braterstwa` dostaje trzy czytania z `wobec`
w roli okolicznika, a `Program zapisuje ustawienia, gdy linter sprawdza tekst.`
wychodzi obok czytania podrzędnego drugim, w którym `gdy` jest okolicznikiem
zdania spiętego przecinkiem.
Cena tej klasy jest przez to zmierzona i wynosi sześć zdań Składnicy:
tyle straciło jednoznaczność pod morfologią żywą, kiedy weszła podrzędność
okolicznikowa, i wszystkie sześć niesie `gdy` albo `kiedy`.
Kryterium słownikowe `admissible` w `olski/segmentacja.py` po nie nie sięga,
bo pyta o czytanie rzeczownikowe stojące obok wyrazu funkcyjnego,
a rozszerzyć go nie ma czym: kryteria zaproponowane dla tej klasy
[zmierzono i odrzucono](../docs/warstwa-leksykalna.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi),
a każde odbiera anotatorom Składnicy czytanie, które sami wybrali.
Zostaje ruch, który kryterium nie jest, a klasę nazywa.
Słownik odróżnia przysłówkowe `sam` od przymiotnikowego identyfikatorem leksemu —
`sam:D` wobec `sam:A`, `oraz:D` wobec `oraz:C`, `wszystko:D` wobec `wszystko:S` —
a `analyse` w `olski/morph.py` ten identyfikator obcina,
więc deklaracja o lemacie (`pomijane` w `olski.toml`)
sięga obu czytań naraz i żadnego z osobna
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#słownictwo-projektu-orzeka-o-lemacie-w-obie-strony)).
Do rozstrzygnięcia jest, czy deklaracja o czytaniu jest tym, czego ta klasa żąda:
wpis o `wszystko` i o `taki` zamyka nad obydwoma korpusami całą rodzinę `reg.`,
a dwa wpisy to za mało, żeby wiedzieć, czy taka lista rośnie, czy stoi.
Do przeczytania jest przedtem wpis o orzeczniku `ten sam`,
bo `sam` jest w tej klasie najczęstszy nad prozą tego repozytorium:
`Sposób jest ten sam.` zostaje po odebraniu przysłówka bez ani jednego czytania,
a wpis tamten mówi, jakiej pozycji temu zdaniu brakuje.

Rzeczownikowe czytanie przymiotnika zabiera README ostatnie zdanie
i nie widać przy nim tego, co zdjęło zaimek.
`Linter pomaga pisać dobry kod.` wychodzi dwoma czytaniami tego samego kształtu,
bo Morfeusz daje `dobry` czytanie `subst:sg:nom.acc:m3` obok przymiotnikowego,
a `kod` czytanie lematu `koda` w dopełniaczu mnogim,
więc `dobry kod` jest raz przymiotnikiem przed rzeczownikiem,
a raz rzeczownikiem z dopełniaczem po nim.
Zaimek rzeczowny zdjął z tej klasy
[warunek w produkcji](../docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
bo `to` dopełniacza nie bierze,
a `dobry` bierze: rzeczownik odprzymiotnikowy dopełniaczem rządzi
i kryterium na tę pozycję zabiera zdania Składnicy, w których rządzi,
co zmierzone stoi w
[`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi).
Zostaje więc sąsiad, nie głowa:
pary nie ma bez dopełniacza `kod`, czyli bez lematu `koda`,
którego ten rejestr nie zna,
a rzadkość formalnego znamienia nie ma.
Wykluczenia leksykalnego z tego nie będzie i to jest już rozstrzygnięte:
`dobry` w czytaniu `subst` niesie przypadek, liczbę i rodzaj,
a `admissible` odbiera czytanie, które spełnia każde żądanie,
więc z dwóch rzeczy, których ono żąda naraz, ta klasa nie ma nawet pierwszej
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi)).
Zostaje pytanie o rzadkość sąsiada i ono jest całym tym wpisem:
czy da się ją policzyć tak,
żeby liczba mówiła o polszczyźnie, a nie o korpusie, w którym się ją policzyło.
Kryterium zbyt szerokie zabiera zwyczajne polskie słowa,
co [`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)
pokazuje na `jury` i `menu`.
Zdanie to jest przy tym warunkiem pod
[kierunkiem toru](../docs/roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście),
bo czytanie, którego polszczyzna nie ma, jest dokładnie tym,
czego werdykt meldować nie powinien.

Rzeczownik `soba` zabiera kilkunastu zdaniom banku drzew jednoznaczność,
odkąd zaimek zwrotny ma pozycję
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym)).
Czytania tego polszczyzna w tych zdaniach nie ma —
`sobie` i `sobą` są w nich zaimkiem — więc jest to wieloznaczność w słowniku,
a nie w polszczyźnie, czyli dokładnie to, co odbiera `admissible`
w `olski/segmentacja.py`
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).
Kryterium tamtego wykluczenia po ten lemat nie sięga i sięgnąć nie może:
pyta ono o rzeczownik nieodmienny, a `soba` odmienia się przez przypadki.
Mechanizm już stoi — `pomijane` w sekcji `lematy` w `olski.toml`
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#słownictwo-projektu-orzeka-o-lemacie-w-obie-strony)) —
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

Nie wiadomo, czy `CLOSED_CLASS` ma zostać w kodzie.
Wykluczenie jest zakładem o rejestr, więc domyślność dostarczana z paczką jako
konfiguracja byłaby uczciwsza wobec czytelnika werdyktu: projekt nadpisuje ją
tam, gdzie chce, i widzi ją tak samo jak własną.
Ceną są dwa pliki zamiast jednego,
czyli `znajdź` w `olski/konfiguracja.py` przestający być całą regułą szukania.
Wpis czeka na ten o autorze, który nie widzi, co wykluczenie wycięło jego tekstowi,
bo o cenie rozstrzyga to, czy autor ma już skąd wiedzieć, co mu się wycina:
kiedy ma, druga droga kupuje samo nadpisywanie.

Deklaracji martwej nie pilnuje nic.
Lemat wpisany do `wpuszczane`, po który wykluczenie i tak by nie sięgnęło —
bo słownik nie daje mu czytania nieodmiennego obok klasy zamkniętej —
nie zmienia ani jednego werdyktu i nie zgłasza się,
tak samo jak lemat wpisany do `pomijane`, którego słownik nie zna wcale.
Jest to ta sama klasa, którą po stronie leksykonu łapie świadek
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)),
i tam wpis zły zgłasza się, a tutaj milczy.
Ruchem jest check pytający słownik o lemat przy czytaniu konfiguracji.
Do rozstrzygnięcia jest przedtem cena: `olski/konfiguracja.py` czyta się przy
imporcie i nie żąda dziś Morfeusza w żadnym trybie,
a check ten kazałby żądać go każdemu, kto pyta o samą konfigurację.

Czytanie nieodmienne, którym wchodzi notacja i wersalik, bierze rolę okolicznika
narzędnikowego, bo spełnia każde żądanie przypadku, także narzędnika.
`Wprowadzenie streszcza README.` wychodzi czworgiem odczytań,
a dwa z nich stawiają `README` w okoliczniku narzędnikowym przy `streszcza`;
`Cały wywód prowadzi docs/linter.md.` wychodzi sześcioma,
choć [`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)
mówi o dwóch, SVO i OVS, i zdanie to jest tam nieaktualne.
Polszczyzna nie stawia nazwy pliku w narzędniku sposobu,
więc jest to czytanie, którego czytelnik nie ma, a nie cena wieloznaczności.
Ruchem jest `NIEODMIENNY` w `olski/segmentacja.py` bez narzędnika
albo warunek na okoliczniku narzędnikowym odmawiający czytaniu nieodmiennemu,
i przed nim pomiar nad prozą repozytorium, bo notacja stoi w niej gęsto
i liczba zdań, którym ubędzie odczytań, jest tym, co ten ruch kupuje.
Do przeczytania jest przedtem, czy tego samego czytania nie bierze orzecznik
narzędnikowy przy kopuli, bo `Wprowadzenie jest streszczeniem README.`
wychodzi trojgiem odczytań i jedno z nich orzeka samym `README`.

Nazwa z podkreśleniem nie jest notacją i nie ma czytania:
`Pole liczba_czytań wychodzi z lasu.` pada na `liczba_czytań`,
a `Pole urwane wychodzi z lasu.` przechodzi.
Morfeusz oddaje taki napis jednym segmentem `ign`,
a `NOTACJA` w `olski/segmentacja.py` żąda kropki albo ukośnika między członami,
więc klucz JSON-a, nazwa symbolu gramatyki i nazwa stałej pisana małymi literami
nie wchodzą, choć wersalik z podkreśleniem — `NAJWIĘCEJ_ZNAKÓW` — wchodzi
[warunkiem na wersalik](../docs/warstwa-leksykalna.md#wersalik-bez-czytania-jest-tym-samym-rzeczownikiem-nieodmiennym).
Rejestr pisze te nazwy wprost: `docs/witryna.md` nazywa klucze odpowiedzi,
a każdy dokument o gramatyce nazywa `wyrażenie_przyimkowe` i `okolicznik_zdaniowy`.
Ruchem jest podkreślenie jako trzeci znak spajający we wzorcu notacji,
a ceny po stronie polszczyzny nie ma, bo żadne polskie słowo podkreślenia nie niesie.
Do przeczytania jest komentarz nad tym wzorcem, bo wylicza on cztery żądania
i mówi, przed czym każde broni, a piąte ma powiedzieć to samo o sobie.

Nazwa własna pisana wielką literą, której słownik nie zna,
nie ma do olskiego żadnej drogi.
`Uruchamia go z tego repozytorium Scalingo.` pada na `Scalingo`,
tak samo `Flask`, `FastAPI`, `React`, `Procfile` i `PyPI`,
a `README` i `WSGI` przechodzą, bo są pisane samymi wersalikami.
Czytania nieodmiennego taka forma nie dostaje, bo warunek pyta o wersalik
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#wersalik-bez-czytania-jest-tym-samym-rzeczownikiem-nieodmiennym)),
a do leksykonu projektu nie wejdzie z dwóch powodów:
`Scalingo` polszczyzna nie odmienia, więc świadek nie może różnić się od lematu,
czego żąda `_sprawdź_świadka` w `olski/projekt.py`,
a `Flask` i `React` ta proza pisze w samym mianowniku,
więc świadka nie ma skąd wziąć.
Wpis o nazwie angielskiej pisanej małą literą tego nie obejmuje,
bo tam czytanie nieodmienne byłoby fałszywe, a tu jest jedyne prawdziwe.
Ruchem jest albo trzeci warunek obok notacji i wersalika,
czyli wielka litera na czele formy, której słownik nie czyta wcale,
a nie na czele zdania, albo wpis leksykonu bez świadka
dla słowa deklarowanego jako nieodmienne.
Zakup pierwszego jest zmierzony nad prozą tego repozytorium i jest to kilkanaście zdań,
z tego jedenaście przeczytanych ręką i wszystkie polskie —
`Opróżnia więzienie Qasr ze wszystkich kryminalistów.`
oraz `Kończy się ono przed tablicą Earleya, więc tablica dostaje ciała wypisane.` —
a ani jedno nie jest zdaniem angielskim,
bo forma angielska stoi w środku zdania małą literą.
Warunek bez wielkiej litery, czyli czytanie nieodmienne dla każdej formy nieznanej,
odpada właśnie na tym: kupuje wielokrotnie więcej zdań,
a przeczytane są w większości angielskie
i `The cutting applies to words that buy nothing.` wychodzi wtedy jednym odczytaniem.
Cena warunku z wielką literą jest widoczna bez Składnicy i jest podwójna:
`Punkty gromadzi Beenhakkera.` wyprowadza się z tą formą w podmiocie,
bo czytanie nieodmienne spełnia każde żądanie przypadku,
a `Cena Scalingo Beenhakkera Qasr rośnie.` wychodzi kilkunastoma odczytaniami,
bo nazwy nieznane przedłużają łańcuch imienny jedna za drugą.
Do przeczytania zostaje cena nad Składnicą,
bo rejestr prasowy pisze wielką literą nazwisko, którego SGJP nie ma,
i takie nazwisko dostałoby czytanie nieodmienne, choć polszczyzna je odmienia.
