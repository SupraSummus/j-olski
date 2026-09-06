# Parser, las i koszt

Czytanie pierwsze buduje najtańsze drzewo każdej pary, a wystarczyłby jego koszt.
`_iloczyn` w `olski/parse/las.py` żąda od każdego strumienia córek pierwszego drzewa,
zanim wyda pierwszą kombinację, więc porządek po sumie schodzi po całym lesie
i składa tam węzły, po które nikt potem nie sięgnie.
Kosztu najtańszego drzewa nie trzeba przy tym budować:
liczy się go od dołu, jedną wartością na parę.
Ruchem jest wskaźnik w kolejce wyceniany tym kosztem,
a drzewo składane dopiero przy zdjęciu z kolejki.
Nad prozą tego repozytorium czas przebiegu tego nie widać
(zmierzony naprzemiennie, 0,94–1,03× wobec kolejności sprzed sumy),
więc pomiarem, który to odwraca, jest zdanie o lesie na dziesiątki tysięcy czytań
([`docs/ustawy.md`](../docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z--6-ale-nie-jest-zarzutem)),
a nie proza.

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
Sondą jest warunek, który `tests/parser/test_las.py` sprawdza na garści zdań —
zdanie zawężone do odczytań liści wyprowadza ten sam kształt —
puszczony nad całym README, bo w tamtej garści tej klasy nie ma.

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
