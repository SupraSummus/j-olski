# Parser, las i koszt

Sumy kosztów drzewa nikt nie zmierzył, więc nie wiadomo, czy bije porządek dzisiejszy.
Las porządkuje ciała jednej pozycji jej kosztem, a drzewa wychodzą z niego
wyliczaniem w głąb, więc kolejność czytań jest leksykograficzna:
koszt produkcji przy korzeniu waży więcej niż każdy koszt produkcji pod nim,
choćby ich było kilka.
Koszt morfologii sumuje się już dziś i jest minimum po poddrzewie
(`koszt_morfologii` w `olski/parse/las.py`), więc pytanie o sumę stawia się teraz
o drugą połowę kosztu, a nie o cały.
Porządek po sumie kosztów całego drzewa jest inną odpowiedzią i wymaga innego wyliczania,
bo minimum globalne żąda kolejki nad lasem, a nie przejścia w głąb,
i zdejmuje leniwość, na której stoi `numer_czytania` w `olski/parse/las.py`:
wyliczanie przystaje dziś na pierwszym drzewie, które trafia, i granicy nie potrzebuje.
Ruchem jest wariant napisany w sondzie, a nie w parserze,
i jedna liczba obok tamtej: złote czytanie Składnicy pod jednym porządkiem i pod drugim.
Suma liczona po `wyprowadzenia` w `olski/parse/las.py` odpowiedzi nie da,
bo ta metoda czyta tablicę, czyli las przed unifikacją,
i minimum wypada w niej czasem na kształcie, którego unifikacja nie przepuszcza;
sumę bierze się przez to po krawędziach klas, a nie po ciałach pozycji.
Dopiero różnica mówi, czy warto płacić za kolejkę.
Trop jest jeden i jest przeciw: sesja, która wpuściła koszt morfologii, sumowała
przez pomyłkę także koszty produkcji i przestawiła wtedy nad prozą repozytorium
dwa razy więcej zdań, a przeczytane ręką wypadły gorzej — `Co pan sądzi o pomyśle
Pawła Piskorskiego?` wychodziło pierwszym czytaniem z `Co pan` w wyrażeniu
przyimkowym. Sądów jest kilkanaście i pomiarem to nie jest, więc trop mówi tyle,
że sondę warto puścić, zanim ktoś napisze kolejkę.

Przedstawiciel pozycji może stać w klasie, której żadne czytanie nie bierze.
`_przedstawiciel` w `olski/parse/las.py` bierze pierwsze drzewo pozycji bez odsiewu po
klasach żywych, a `_kształty` obok niego ten odsiew ma, więc nazwa konstytuenta
bierze się czasem z kształtu, którego werdykt nie liczy.
Rozpiętość jest w obu ta sama, więc formy różni w nich tylko podział na segmenty.
Ruchem jest `next(self._kształty(pozycja))` w miejsce tamtej pętli, a przeszkodą
pozycja bez ani jednej klasy żywej: dziś oddaje nazwę, a wtedy podniosłaby wyjątek.
Do przeczytania jest, czy nad Składnicą taka pozycja pada i czy pada z innymi formami,
bo od tego zależy, czy to usterka, czy sam porządek w kodzie.

Wykaz morfologii sumuje odczytania po ciałach jednej klasy, a klasy sąsiedniej nie widzi.
`Las._wsparte_kształtu` w `olski/parse/las.py` idzie po produkcjach spakowanych
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
Sondą jest warunek, który `tests/test_las.py` sprawdza na garści zdań —
zdanie zawężone do odczytań liści wyprowadza ten sam kształt —
puszczony nad całym README, bo w tamtej garści tej klasy nie ma.

Zatrzymanie kosztuje nad zdaniem odrzuconym więcej niż zbudowanie tablicy,
bo `najdalszy` w `olski/parse/las.py` przechodzi tablicę drugi raz
i unifikuje przy tym przebyte ciała, czego samo jej budowanie nie robi wcale.
Pomija je ten, kto go nie czyta (`werdykt` w `olski/werdykt/zdanie.py`),
więc do potanienia zostaje samo drugie przejście.
Kolejka w `_przed_formą` dostaje przy ożywieniu symbolu wszystkie jego produkcje,
a tablica ma stan dla mniejszości z nich,
więc ponad połowa par schodzi z kolejki, nie robiąc nic.
Ruchem jest kolejka symboli w miejsce kolejki par:
rozwinięty symbol brałby wtedy z tablicy same stany o tej głowie,
a produkcje czekające na pierwszą córkę wchodziłyby tak,
jak wchodzą do tablicy — przez `możliwe` tej pozycji, a nie przez przejrzenie wszystkich.
Przybliżenie tańsze od tego, czyli najdalsza pozycja o jakimkolwiek stanie tablicy,
jest zmierzone i odpada: myli się w co czwartym zdaniu, i to w obie strony,
bo tablica trzyma stan bez oglądania się na unifikację i na to,
czy analiza częściowa ten stan w ogóle przewidziała.
Do przeczytania jest `_przed_formą` wraz z `_prefiks` w `olski/parse/las.py`:
to one są tym drugim przejściem, a warunek na analizę częściową opisuje pierwsze.

Zatrzymanie stoi w module o lesie, a lasu nie pyta prawie o nic.
`najdalszy` wraz z `_przechodzi`, `_przed_formą`, `_zaczyna_się_tu` i `_prefiks`
w `olski/parse/las.py` chodzi po stanach tablicy i unifikuje przebyte ciała,
a z lasu bierze `klasy` oraz `_dołóż`, czyli samą unifikację nad córką.
Bliżej mu przez to do `olski/parse/tablica.py` niż do modułu o kształtach.
Warunkiem jest wyniesienie tej unifikacji:
`_sposoby`, `_dołóż` i `_przejdź` wraz z `_czytania_liścia`
składają się na jednego współpracownika, którego wołają i las, i zatrzymanie,
a docstring `_sposoby` mówi, że unifikacja dotyka lasu w tym jednym miejscu,
więc kawałek jest już nazwany.
Ceny nie widać z góry i to jest tu przeszkoda:
`_sposoby` leży na najgorętszej ścieżce parsera —
woła je liczenie klas, wyliczanie drzew i to drugie przejście —
więc wyniesienie ich za granicę modułu żąda pomiaru czasu, a nie samego odcisku.
Do przeczytania jest wpis o kolejce symboli w `_przed_formą`:
rusza ten sam kod, więc oba ruchy wolno zrobić jednym.

Pozycja `opuszczony podmiot` w cenniku płaci także tam,
gdzie czasownik podmiotu mieć nie może.
`brakować` żąda dopełniacza, więc `Miejsca na taki filtr nie brakuje.`
ma czytanie bez podmiotu jako jedyne poprawne,
a cennik stawia je pod czytaniem, które podmiot obsadza
([`docs/disambiguation.md`](../docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie)).
Nad prozą tego repozytorium pada jedno takie zdanie,
a pozycja przestawia czytanie pierwsze wielokrotnie częściej
i w większości przeczytanych trafnie, więc wpis jest o resztce, a nie o pozycji.
Liczbę dzisiejszą wypisuje `harness/cena.py`, pozycja po pozycji.
Ruchem jest zdjęcie tej pozycji z ciała, którego czasownik mianownika nie bierze,
czyli warunek na ramę, a nie na produkcję.
Ciała są dwa, bo pozycję tę płaci i `zdanie_składowe → dopełnienie czasownik_ramy`,
i `zdanie_składowe → grupa_orzeczenia` w `olski/subset/zdanie.py`,
a każde wchodzi jednym ciałem dla każdej ramy.
Do przeczytania jest, czy rama to mówi:
`PODMIOT` w `olski/walencja.py` nazywa pozycję podmiotu,
a leksykon walencyjny wypisuje ją przy czasowniku, który ją ma,
więc pytanie jest o to, czy czasownik bez tej pozycji da się odróżnić
przed rozbiorem, czy dopiero unifikacja to rozstrzyga.
Przedtem warto policzyć, ile takich zdań pada nad Składnicą,
bo nad tą prozą pada jedno.
