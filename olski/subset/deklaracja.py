"""Nazwy ról i listy, którymi werdykt schodzi po lesie, wypisane obok produkcji.

Gramatyka wyprowadza zdanie, a nie mówi o nim nic ponadto,
więc streszczenie czytania bierze się stąd:
nazwa roli jest etykietą, którą werdykt wypisuje,
a :data:`DEKLARACJA` mówi, na których symbolach zejście po lesie staje
(``olski/parse.py``).
Ile kosztuje wpis pominięty, mówi komentarz przy każdej z tych list.
"""

from __future__ import annotations

from dataclasses import dataclass

from olski.parse import Deklaracja
from olski.subset.słowa import GRUPA_ORZECZENIA_ODWRÓCONA

#: Rola, którą gramatyka zostawia nierozstrzygniętą rozmyślnie,
#: więc streszczenie czytania nazywa przy niej i to, co ona określa:
#: bez tego dwa czytania różne samym miejscem przyłączenia wychodzą jednym napisem.
WYRAŻENIE_PRZYIMKOWE = "wyrażenie_przyimkowe"


#: Człon ciągu współrzędnego wyrażeń przyimkowych: `o bierniku` w `Leksykon mówi
#: o bierniku i o bezokoliczniku.` Rolą ta nazwa nie jest, bo rolą jest cały ciąg,
#: tak samo jak przy członie imiennym: werdykt nazywa wyrażenie przyimkowe wraz
#: z gospodarzem, do którego ono doszło, a człony ciągu dochodzą do niego razem.
CZŁON_PRZYIMKOWY = "człon_przyimkowy"


#: Ciąg współrzędny tych członów, czyli to, co stoi pod rolą i nią nie jest.
#: Symbol jest osobny od :data:`WYRAŻENIE_PRZYIMKOWE`, bo ogon ciągu pod tamtą
#: nazwą byłby drugim wyborem przyłączenia: określa on to samo, co cały ciąg,
#: a werdykt wypisałby go osobno i nazwał gospodarza, którego czytanie już nazwało.
CIĄG_PRZYIMKOWY = "ciąg_przyimkowy"


#: Rola przysłówka, czyli tego, który określa zdanie. Przysłówek określający
#: przymiotnik roli nie dostaje: stoi on wewnątrz orzecznika albo przydawki, więc
#: widać go w wypełnieniu tamtej roli, a wypisany drugi raz obok mówiłby o zdaniu,
#: że ma okolicznik, którego ono nie ma.
OKOLICZNIK_PRZYSŁÓWKOWY = "okolicznik_przysłówkowy"


#: Rola okolicznika wyrażonego zdaniem.
#: Stoi ona zarazem wśród zdań podrzędnych, bo wnętrze tego okolicznika
#: jest osobnym zdaniem, i tyle znaczy nazwanie go rolą:
#: streszczenie nazywa go całym napisem i w środek nie zagląda.
OKOLICZNIK_ZDANIOWY = "okolicznik_zdaniowy"


#: Rola grupy pytajnej:
#: `które zadania` w `Ustawy określają, które zadania mają charakter obowiązkowy.`
#: Konstytuentem jest grupa imienna,
#: więc wnętrze streszczenie nazywa całym napisem, tak samo jak wnętrze podmiotu.
GRUPA_PYTAJNA = "grupa_pytajna"


#: Rola rzeczownika, który orzeka bez czasownika:
#: `mowa` w `zadania, o których mowa w ustawie`.
#: Zdanie z tym rzeczownikiem nie ma ani podmiotu, ani czasownika,
#: więc bez tej etykiety wychodziłoby `valid` bez ani jednej roli.
#: Czemu rola stoi obok orzecznika, a nie jest nim, wywodzi
#: docs/konstrukcje-gramatyczne/podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat.
ORZECZENIE_RZECZOWNIKOWE = "orzeczenie_rzeczownikowe"


#: Rola grupy imiennej, która orzeka przed łącznikiem:
#: `Flaga` w `Flaga to płat tkaniny.`
#: Symbol jest osobny od :data:`ORZECZENIE_RZECZOWNIKOWE`, bo tamten czyni zdaniem każdą swoją
#: córkę, a tutaj czyni je dopiero łącznik stojący za tą grupą; czemu grupa ta
#: stoi po tej stronie łącznika, mówi
#: docs/konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim.
ORZECZNIK_ŁĄCZNIKA = "orzecznik_łącznika"


#: Nazwy, którymi werdykt mówi o rolach zdania z łącznikiem `to`.
#:
#: Wykonywanym tu sądem jest zdanie „pozycja podmiotu przy łączniku `to` jest
#: tym, co składnia szkolna nazywa orzecznikiem”. Wewnątrz gramatyki nazwa ta
#: znaczy pozycję schematu, czyli to, co bank drzew woła `subj` i co stawia
#: także tam, gdzie podmiotu nie ma; wywód i liczby trzyma
#: docs/konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim.
#: Przekład wykonuje `olski/werdykt.py`, czyli warstwa za pomiarem, więc żadnej
#: liczby nad bankiem drzew nie rusza i ruszyć nie może.
NAZWY_SZKOLNE = {
    "podmiot": "orzecznik",
    ORZECZNIK_ŁĄCZNIKA: "podmiot",
}


#: Rola tego, co orzeka bez podmiotu. Głowy są dwie i obie rządzą ramą czasownika:
#: predykatyw — `trzeba` w `Trzeba czytać dokumenty.` — oraz forma `imps` —
#: `zgłoszono` w `Zgłoszono usterkę.`
#:
#: Rola stoi obok orzeczenia, a nie jest nim, bo żadna z tych dwóch głów zgodności nie
#: niesie: `orzeczenie: trzeba` mówiłoby o zdaniu, że ma orzeczenie zgodne z podmiotem,
#: którego ono nie ma, a `orzeczenie: zgłoszono` dałoby `Zgłoszono program.` podmiot
#: `program`, bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza.
#: Co wpuszczenie każdej z tych dwóch głów kosztuje, mierzą
#: docs/konstrukcje-gramatyczne/orzeczenie.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika oraz
#: docs/konstrukcje-gramatyczne/orzeczenie.md#czasownik-nieosobowy-rządzi-ramą-swojego-lematu.
ORZECZENIE_BEZOSOBOWE = "orzeczenie_bezosobowe"


#: Symbol imiesłowu przysłówkowego wraz z przeczeniem i cząstką zwrotną:
#: `sprawdzając` w `Program zapisuje ustawienia, sprawdzając zgodność.`
#: Rolą ta nazwa nie jest, bo rolą jest cały okolicznik (:data:`OKOLICZNIK_ZDANIOWY`),
#: który werdykt nazywa całym napisem i w środek nie zagląda.
IMIESŁÓW_PRZYSŁÓWKOWY = "imiesłów_przysłówkowy"


#: Rola cząstki stojącej przy zdaniu: `już`, `dopiero`, `także`.
#: Od przysłówka różni ją część mowy, a pozycję ma tę samą,
#: i dlatego pisze je jedna pętla.
CZĄSTKA_ZDANIA = "cząstka_zdania"


#: Rola okoliczności wyrażonej narzędnikiem bez przyimka:
#: `deskami` w `Mieszczanie zabili okna deskami.`, `Wieczorem`, `czasem`, `ręką`.
#: Symbol jest osobny od :data:`OKOLICZNIK_PRZYSŁÓWKOWY`, choć pozycję ma tę samą, bo cena
#: tej pozycji ma być osobną liczbą, a sonda mierzy zdjęciem ciał
#: (CLAUDE.md#code); pod jednym symbolem zdjęcie zabrałoby obie naraz.
#: Od orzecznika narzędnikowego różni ją to, kto jej udziela licencji:
#: orzecznika żąda ramą kopula, a okolicznik stoi przy każdym czasowniku
#: i przy żadnym nie wypełnia pozycji
#: (docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika).
OKOLICZNIK_NARZĘDNIKOWY = "okolicznik_narzędnikowy"


#: Rola wtrącenia w nawiasie: `(docs/subset.md)`, `(niżej)`.
#: Rolą zdania jest samo wtrącenie, a nie to, co ono niesie,
#: bo nawias dopowiada, a nie wypełnia pozycji:
#: grupa imienna w jego środku nie jest ani podmiotem, ani dopełnieniem,
#: i streszczenie nazywa ją całym napisem.
WTRĄCENIE = "wtrącenie"


#: Rola wtrącenia w parze myślników: `— w prozie czy w kodzie —` w `Zepsute
#: miejsce — w prozie czy w kodzie — nie zawsze potrzebuje lepszej wersji.`
#:
#: Symbol jest osobny od :data:`WTRĄCENIE`, choć oba dopowiadają obok zdania, bo
#: rozdziela je miejsce: nawias staje tam, gdzie zdanie składowe się kończy, a
#: para staje wszędzie tam, gdzie okolicznik zdania. Jeden symbol na oba dałby
#: nawiasowi każde z tych miejsc, więc `Zdanie stoi (docs/subset.md).`
#: wychodziłoby tyloma czytaniami, ilu gospodarzy ma w nim wyrażenie przyimkowe,
#: a po to tamta pozycja jest jedna
#: (docs/konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania).
WTRĄCENIE_MYŚLNIKOWE = "wtrącenie_myślnikowe"


#: Rola członu, którego czasownik ten rejestr opuszcza: `a nie zdanie` w
#: `Milczenie obejmuje wybór, a nie zdanie.`, `czyli o obiekt składniowy` w
#: `Warstwa pyta o Przyłączenie, czyli o obiekt składniowy.`
#:
#: Nazwa mówi o kształcie, a nie o tym, co ten człon robi, bo jednego od drugiego
#: gramatyka nie odróżnia: `a nie` przeczy, `czyli` powtarza to samo innymi
#: słowami, a spójnik jest jedyną różnicą i o znaczeniu nie rozstrzyga. Czemu ten
#: człon przeczy, milczy tym samym prawem: `Wybór obejmuje milczenie, a nie
#: zdanie.` przeciwstawia albo dopełnieniu, albo podmiotowi.
#:
#: Rolą jest cały człon, a nie to, co on niesie, i z tego samego powodu, z
#: którego rolą jest całe wtrącenie (:data:`WTRĄCENIE`).
ELIPSA = "elipsa"


#: Symbol pary wypełnień: dopełnienie w celowniku obok wypełnienia, które zajmuje
#: pozycję ramy. Symbolem, a nie ciałami `wypełnienia`, bo inaczej
#: szyk pary mnoży się przez miejsca na okolicznik wokół niej, a tak każde z tych
#: dwóch mnoży się osobno. Rolą ta nazwa nie jest — role wylicza
#: :data:`DEKLARACJA` — bo werdykt nazywa dopełnienie dopełnieniem, a nie parą.
PARA_WYPEŁNIEŃ = "para_wypełnień"


#: Symbol frazy bezokolicznikowej, której pozycji ramy nie wypełnia nic w jej
#: środku: wypełnia ją konstytuent stojący przed formą osobową, która tę frazę
#: bierze — `większości` w `premier większości nie może ruszyć`. Rama idzie z tej
#: frazy w górę cechą `wysunięte`, bo o pozycję pyta dopełnienie stojące poza nią.
#:
#: Symbolem, a nie ciałem obok pozostałych ciał `fraza_bezokolicznikowa`, bo cena tej
#: pozycji ma być osobną liczbą, a sonda różnicowa bierze ją zdejmowaniem ciał
#: (CLAUDE.md#code): ciała dopisane tamtemu symbolowi schodziłyby razem z frazą,
#: która pozycję ramy wypełnia sama.
FRAZA_BEZOKOLICZNIKOWA_OTWARTA = "fraza_bezokolicznikowa_otwarta"


#: Rola spójnika, który stoi wewnątrz swojego zdania: `zatem` w `Milczenie jest
#: zatem wartością.` Od cząstki różni ją to, co to słowo robi: cząstka określa
#: zdanie, a ten spójnik wiąże je z tym, co stoi przed nim.
SPÓJNIK = "spójnik"


#: Rola grupy imiennej, którą ten rejestr wylicza za dwukropkiem: `Zdanie oraz
#: Kontekst` w `Warstwa pyta o dwa typy: Zdanie oraz Kontekst.` Rolą jest cała
#: grupa, z tego samego powodu co przy :data:`WTRĄCENIE`.
#:
#: Rola stoi osobno od :data:`ELIPSA`, choć `, czyli Morfeusz` i `: Morfeusz`
#: dopowiadają to samo, bo rozdziela je kształt: tamten człon stoi za spójnikiem
#: i w zdaniu składowym, a ten za dwukropkiem i w zdaniu całym, gdzie dwukropek
#: musi stać (:data:`DWUKROPEK`). Jedna rola na oba żądałaby cechy, która by te
#: dwa poziomy rozdzieliła, czyli maszynerii droższej niż druga nazwa.
DOPOWIEDZENIE = "dopowiedzenie"


@dataclass(frozen=True)
class Rodzina:
    """Zdanie z jedną rolą wysuniętą na czoło, wraz z symbolami wokół niego.

    Nazwy jednej rodziny czytają cztery miejsca: :func:`_wysunięta_rola` pisze
    nimi ciała, :data:`NIE_WYPUSZCZANE` zatrzymuje na nich cechy, a `gospodarze`
    i `podrzędne` w :data:`DEKLARACJA` zatrzymują na nich dwa zejścia werdyktu.
    Rodzina jest tu jedną wartością dlatego, że wpis pominięty w którymkolwiek
    z tych miejsc nie wywraca żadnego testu: odbiera wiersz werdyktu albo każe
    cesze kosztować rozbiór, po cichu.
    """

    #: Zdanie z wysuniętą rolą, czyli to, co czoło ma pod sobą.
    rdzeń: str
    #: Wyrażenie przyimkowe wysunięte razem z czołem. Przypadka nie wypuszcza,
    #: bo ustala go przyimek nad nim, a nie zdanie pod czołem.
    modyfikator: str
    #: Czoła tej rodziny; każde wchodzi w obie pozycje wysunięte i pod przyimek.
    czoła: tuple[str, ...]
    #: Symbole, którymi to zdanie staje przy zdaniu nad nim, czyli te, na których
    #: zatrzymuje się streszczenie (`podrzędne` w :data:`DEKLARACJA`).
    opakowujące: tuple[str, ...]


#: Symbole opakowujące są dwa tam, gdzie zdanie z poprzednikiem i zdanie bez
#: niego stają przy zdaniu nad nim inaczej.
RODZINY = (
    Rodzina(
        rdzeń="rdzeń_względny",
        modyfikator="wyrażenie_przyimkowe_względne",
        czoła=("zaimek_względny", "grupa_imienna_względna"),
        opakowujące=("zdanie_względne",),
    ),
    Rodzina(
        rdzeń="rdzeń_względny_rzeczowny",
        modyfikator="wyrażenie_przyimkowe_względne_rzeczowne",
        czoła=("zaimek_względny_rzeczowny",),
        opakowujące=("zdanie_względne_rzeczowne", "zdanie_względne_bez_poprzednika"),
    ),
    Rodzina(
        rdzeń="rdzeń_pytajny",
        modyfikator="wyrażenie_przyimkowe_pytajne",
        czoła=(GRUPA_PYTAJNA,),
        opakowujące=("zdanie_pytajne",),
    ),
)


DEKLARACJA = Deklaracja(
    # Konstrukcja, na którą nie ma tu etykiety,
    # wychodzi `valid` bez słowa o tym, co olski w niej przyjął.
    role=(
        "podmiot",
        "dopełnienie",
        "orzecznik",
        "orzeczenie",
        ORZECZENIE_RZECZOWNIKOWE,
        ORZECZNIK_ŁĄCZNIKA,
        ORZECZENIE_BEZOSOBOWE,
        OKOLICZNIK_PRZYSŁÓWKOWY,
        CZĄSTKA_ZDANIA,
        OKOLICZNIK_NARZĘDNIKOWY,
        SPÓJNIK,
        OKOLICZNIK_ZDANIOWY,
        GRUPA_PYTAJNA,
        WTRĄCENIE,
        WTRĄCENIE_MYŚLNIKOWE,
        ELIPSA,
        DOPOWIEDZENIE,
        WYRAŻENIE_PRZYIMKOWE,
    ),
    # Tu stoi każda rola, którą gramatyka wpuszcza w kilka miejsc:
    # bez nazwy gospodarza dwa czytania różne samym miejscem
    # wychodzą z werdyktu jednym wierszem powtórzonym dwa razy.
    # W `Począł myśleć gorączkowo.` czytania różni tylko to,
    # czy `gorączkowo` doszło do bezokolicznika, czy do formy osobowej nad nim.
    # Kryterium bierzemy z kształtu gramatyki i płacimy strzałką,
    # która powtarza czasownik zdania tam, gdzie gospodarz jest jeden.
    # Strzałka stawiana dopiero tam, gdzie gospodarz się rusza, byłaby tańsza,
    # a zabrałaby ją zdaniu o jednym czytaniu, gdzie nie rusza się nigdy,
    # choć mówi jedyną rzecz, jakiej o tym czytaniu nie widać po rolach.
    # Dopowiedzenie zostaje przez to poza listą,
    # bo gramatyka daje mu jedno miejsce (`wypowiedzenie` w ``olski/subset/wypowiedzenie.py``),
    # więc jego strzałka powtarzałaby czasownik zawsze.
    przyłączane=(
        WYRAŻENIE_PRZYIMKOWE,
        OKOLICZNIK_PRZYSŁÓWKOWY,
        CZĄSTKA_ZDANIA,
        OKOLICZNIK_NARZĘDNIKOWY,
        SPÓJNIK,
        OKOLICZNIK_ZDANIOWY,
        WTRĄCENIE,
        WTRĄCENIE_MYŚLNIKOWE,
        ELIPSA,
    ),
    rozstrzygany=WYRAŻENIE_PRZYIMKOWE,
    # Konstytuenty, na których zatrzymuje się zejście w górę od modyfikatora
    # (``_gospodarze`` w ``olski/parse.py``).
    # Streszczenie nazywa ten z nich, który stoi najbliżej, bo tam przyłączenie zapadło,
    # a okolicznik zdania nie ma nad sobą ani grupy imiennej, ani przymiotnikowej
    # i zostaje przy zdaniu.
    # Pominięty wpis nie odbiera zdania, tylko przekłamuje streszczenie:
    # okolicznik wychodzi z takiego konstytuentu w górę,
    # a werdykt nazywa gospodarza stojącego nad nim
    # — bez wpisu ``rdzeń_względny`` poprzednik zamiast orzeczenia zdania względnego —
    # albo streszcza oba czytania jednym napisem, jak bez wpisu ``fraza_bezokolicznikowa``.
    # :data:`GRUPA_PYTAJNA` stoi tu, choć jest zarazem rolą, bo wyrażenie przyimkowe
    # ma pod zaimkiem pytajnym własne ciało: `Kto z posłów zapisuje ustawienia?`.
    # :data:`OKOLICZNIK_ZDANIOWY` stoi tu z tego samego powodu i tylko dla jednej ze
    # swoich dwóch głów: okolicznik wyrażony zdaniem ma pod sobą zdanie, a więc
    # i `zdanie_składowe`, na którym zejście staje wcześniej, a imiesłów
    # przysłówkowy nie ma pod sobą żadnego innego gospodarza, więc bez tego wpisu
    # `sprawdzając zgodność z dokumentem` nazywa gospodarzem orzeczenie zdania
    # nadrzędnego i dwa czytania wychodzą jednym napisem.
    gospodarze=(
        "grupa_imienna",
        "grupa_przymiotnikowa",
        "zdanie_składowe",
        "fraza_bezokolicznikowa",
        FRAZA_BEZOKOLICZNIKOWA_OTWARTA,
        GRUPA_PYTAJNA,
        OKOLICZNIK_ZDANIOWY,
        *(rodzina.rdzeń for rodzina in RODZINY),
    ),
    # Symbole, których ciąg nawiasuje napis roli: grupa imienna, grupa
    # przymiotnikowa i zdanie.
    # Człon nazywa tu produkcja spójnikowa i przecinkowa każdego z nich,
    # a nie symbol członu — ``człon_imienny``, ``człon_przymiotnikowy``,
    # ``zdanie_składowe`` — który jest jednym członem, a nie ciągiem.
    # Przydawka koordynuje się tak samo i tutaj nie stoi:
    # nawias schodzi do ciągu przez węzły o jednej córce (``_nawiasuj`` w ``olski/parse.py``),
    # a przydawka stoi pod rzeczownikiem, czyli w ciele o kilku córkach,
    # więc wpisana tu odbierałaby wiersz o konstytuencie, nie dając w zamian nawiasu.
    współrzędne=("grupa_imienna", "grupa_przymiotnikowa", "zdanie"),
    # Streszczenie pyta o rozpiętość jednego zdania, a nie o ciąg, w którym ono stoi,
    # więc symbolem jest tu człon, a nie ciąg nad nim.
    # Czoło pytania członem tego ciągu nie bywa, więc dopisane tutaj
    # nie rozdzieliłoby ani jednego streszczenia.
    składowe=("zdanie_składowe",),
    # Lista zatrzymuje zejście po role wszędzie, gdzie konstytuent nazywa się
    # całym napisem, a nie tylko przy zdaniu podrzędnym: wywody trzymają
    # :data:`OKOLICZNIK_ZDANIOWY`, :data:`WTRĄCENIE`, :data:`ELIPSA` i :data:`DOPOWIEDZENIE`.
    # Zdania podrzędne stoją tu symbolem opakowującym, a nie samym `zdanie`,
    # bo `zdanie` koordynuje — jest wypisane wyżej wśród współrzędnych —
    # więc zatrzymanie na nim objęłoby także zdanie współrzędne,
    # którego role są rolami tego samego zdania.
    podrzędne=(
        *(symbol for rodzina in RODZINY for symbol in rodzina.opakowujące),
        "zdanie_podrzędne",
        OKOLICZNIK_ZDANIOWY,
        WTRĄCENIE,
        WTRĄCENIE_MYŚLNIKOWE,
        ELIPSA,
        DOPOWIEDZENIE,
    ),
)


#: Konstytuenty, które zejście w górę od modyfikatora mija,
#: choć rola przyłączana stoi w którymś ich ciele.
#:
#: Dopełnienie listy gospodarzy, potrzebne dlatego, że sama ta lista milczy
#: o symbolu dopisanym później; ile takie milczenie kosztuje, mówi komentarz
#: przy `gospodarze` wyżej.
#: Obie strony razem mają pokrywać to, co gramatyka niesie, i pilnuje tego check
#: w ``tests/test_subset.py``, gdzie stoi powód, dla którego podział jest
#: wypisany, a nie wyprowadzony.
MIJANE = (
    # Sam ciąg ról przyłączanych oraz ciąg przysłówków w nim:
    # zejście zaczyna się w środku, więc nie ma tu czego zatrzymywać.
    "okoliczniki",
    OKOLICZNIK_PRZYSŁÓWKOWY,
    # Człon ciągu współrzędnego, którego gospodarzem jest cały ciąg
    # (`współrzędne` wyżej): głowa członu wychodzi w górę razem z nim,
    # więc streszczenie nazywa ją i tak.
    "człon_imienny",
    "człon_przymiotnikowy",
    # Konstytuent, w którym okolicznik nie określa jego samego: w wypełnieniu
    # roli określa czasownik stojący nad nim, a nad ciągiem zdań współrzędnych
    # nie ma gospodarza i zostaje przy całym czytaniu.
    "wypełnienia",
    PARA_WYPEŁNIEŃ,
    "zdanie",
    # Symbol, który streszczenie nazywa całym sobą (`podrzędne` wyżej),
    # więc rola z jego wnętrza gospodarza nie dostaje.
    ELIPSA,
    WTRĄCENIE_MYŚLNIKOWE,
    "zdanie_względne",
)


#: Cechy, których symbol nie niesie w górę, choć żąda ich od swojej głowy.
#: Reszta wychodzi z głowy sama (``olski/grammar.py``),
#: więc zgodności nie wypisuje drugi raz żadna produkcja,
#: a wpis tutaj mówi o symbolu to, czego z jego ciał nie widać.
#:
#: Powody są trzy. Zdanie nie niesie liczby, rodzaju, osoby, ramy ani przeczenia
#: swojego czasownika, bo nad zdaniem nie ma z czym ich zgadzać;
#: tak samo czasownik nie niesie aspektu, o który pyta jedno jego ciało
#: (:func:`_formy_skończone`).
#: Rola nie niesie przypadka, bo sama go ustala.
#: Cecha o kształcie wewnątrz konstytuenta — `czoło` wypełnienia,
#: `accommodability` liczebnika, `dostawka` zdania — kończy się na nim.
#:
#: Żadnego z tych wpisów nie widać po werdykcie i nie jest to przypadek:
#: o cechę, którą wpis zatrzymuje, nie pyta nad tym symbolem ani jedna produkcja
#: poza `dostawka`, a nad prozą tego repozytorium gramatyka bez tych wpisów
#: wydaje werdykt i liczbę czytań co do zdania te same.
#: Wpisy zostają, bo cechę wypuszczaną rozdziela las na klasy pozycji
#: (`klasy` w ``olski/parse.py``), więc niesiona bez czytelnika kosztuje rozbiór;
#: zdjęcie ich jest zmianą w gramatyce i pomiaru żąda osobno (todo/).
NIE_WYPUSZCZANE = {
    "zdanie_składowe": ("number", "gender", "person", "valency", "negacja", "druga", "dostawka"),
    "zdanie": ("dostawka",),
    "orzeczenie": ("aspect",),
    "grupa_orzeczenia": ("valency", "negacja", "druga", "kopula"),
    GRUPA_ORZECZENIA_ODWRÓCONA: ("valency", "negacja", "druga"),
    **{rodzina.rdzeń: ("person", "valency", "negacja") for rodzina in RODZINY},
    OKOLICZNIK_ZDANIOWY: ("tryb", "valency", "negacja", "druga"),
    ORZECZENIE_RZECZOWNIKOWE: ("case", "number"),
    "podmiot": ("case",),
    "dopełnienie": ("case",),
    "orzecznik": ("case",),
    CZŁON_PRZYIMKOWY: ("case",),
    **{rodzina.modyfikator: ("case",) for rodzina in RODZINY},
    "wypełnienia": ("czoło", "kopula"),
    "człon_imienny": ("accommodability",),
}
