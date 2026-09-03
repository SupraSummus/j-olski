# Warstwa leksykalna

Co olski bierze za słowo i których odczytań słownika nie bierze wcale.
Każde z tych rozstrzygnięć orzeka o produkcji, której jeszcze nikt nie napisał,
więc stoi tu, a nie przy konstrukcji, którą akurat obsługuje
([konstrukcje-gramatyczne/](konstrukcje-gramatyczne/README.md)).
Które dopełnienia czasownik bierze, mówi [walencja.md](walencja.md).
Czym jest ważność i co mówi odrzucenie, wykłada [subset.md](subset.md).

## The dictionary offers readings Polish does not

A word read as a noun rather than as a function word
lands in a different shape,
so by the rule above it is a second reading.
One class of those is a second reading no Polish speaker has.

Morfeusz reads `do` as the preposition and as the musical note,
and the note is indeclinable:
its tag carries all seven cases at once.
Unification is the only filter olski has,
so a reading that satisfies every case demand
is one no context can rule out.
`do pliku` therefore derives twice —
as a prepositional phrase,
and as a noun with a genitive modifier —
and so does every other occurrence of `do`,
which is not a rare word:
[corpus.md](corpus.md#what-morphological-ambiguity-costs)
counts it in the treebank
and measures what excluding the note is worth and what it costs.

Olski refuses a sentence that is ambiguous in Polish.
This one is ambiguous only in the dictionary,
and a parse cannot tell those two cases apart,
so the subset excludes readings as well as constructions:
an uninflected noun reading goes
wherever the same form also reads as a closed-class word —
a preposition, a conjunction, a particle, an interjection, a pronoun.
`admissible` in `olski/segmentacja.py` is where that happens.

Zaimek jest na tej liście dla tej samej pary, a nie dla swojej składni.
Morfeusz czyta `go` zaimkiem i grą, `mi` zaimkiem i nutą,
a `te` zaimkiem i nazwą litery,
czyli tak samo, jak czyta `do` przyimkiem i nutą:
czytanie rzeczownikowe nie odmienia się przez nic,
a drugie z pary jest tym, czym forma w tym rejestrze prawie zawsze jest.
Ile ta pozycja kupuje i ile kosztuje, mierzy
[corpus.md](corpus.md#what-morphological-ambiguity-costs).

One exception runs the other way.
`PO`, `AA` and `UP` are organizations whose letters spell function words,
and there the noun is what the form is,
so an all-caps form keeps every reading it has.

Three simpler criteria were available and none holds.
Morfeusz's own qualifiers mark the note `muz.`
and the Japanese theatre that `no` also reads as `teatr.`,
which looks like the criterion until `ku` and `ni`,
which carry no qualifier at all.
The dictionary's labels do not separate them either:
the note is a common noun, `Tam` a surname and `PO` an organization,
and the exclusion has to take the first two and leave the third.
Dropping every uninflected noun instead
would take `jury` and `menu` with it,
and those are ordinary Polish words
with no other reading to fall back on.
What makes the exclusion safe is that it asks for both at once:
the reading inflects for nothing,
and the form carries another one that is what it almost always is.

### Każde szersze kryterium zmierzono i żadne nie stoi

Wykluczenie sięga czytania nieodmiennego stojącego przy klasie zamkniętej
i dalej nie sięga.
Kryteria, które szły dalej, mają cenę policzoną
na 13 035 lasach Składnicy z pełnym drzewem,
a miarą jest to, ile z nich traci czytanie wybrane przez anotatorów.
Każda z tych liczb jest ceną, przy której kryterium odrzucono,
i wzięto je nad gramatyką z tamtej chwili, czyli dwie pierwsze bez przysłówka:
kryterium odrzucone zostaje odrzucone, kiedy jego cena się rusza,
więc przeliczenie broniłoby liczby, a nie decyzji.
Tą samą miarą [corpus.md](corpus.md#what-morphological-ambiguity-costs)
liczy wykluczenie, które stoi, i wychodzi mu sześć.

**Wielka litera z początku zdania nie jest świadectwem nazwiska.**
Morfeusz daje formie `Celem` lemat `Cel` obok lematu `cel`,
a wielką literą zaczyna się każde zdanie,
więc na pierwszej pozycji ta litera o wyrazie nie mówi nic.
Kryterium, które kasuje tam czytanie o lemacie różniącym się od innego
czytania tej samej formy samą wielką literą,
traci 88 zdań — `Paweł`, `Niemcy`, `Bóg`, `Nowak`, `Róża` —
i nie kupuje ani jednego.
Kupić nie ma czego, bo taka para nie jest dwoma odczytaniami:
[odczytanie jest swoim kształtem](subset.md#co-się-liczy-jako-jedno-odczytanie),
a nazwisko i rzeczownik pospolity stają w tym samym miejscu tego samego drzewa.
Drugie czytanie tego zdania robił zaimek rzeczowny,
którego dopełniacza [gramatyka nie bierze](konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
i to jest ta różnica, przy której kryterium na wielką literę
mierzyło coś, czego nie było.
Klasa kosztuje więc trafność, a nie jednoznaczność,
bo czytanie nazwy własnej bywa jedynym, które coś licencjonuje,
i tak wychodzi `Tam siedzi nasz umrzyk.` z
[corpus.md](corpus.md#what-morphological-ambiguity-costs),
gdzie kosztem jest jedno czytanie zdania przeczytanego na opak.
Tam sięga wykluczenie wyżej, bo nazwisko jest w tej formie nieodmienne,
a odmienne zostaje w słowniku i tego wyprowadzenia nikt mu nie odbiera.

**Rzeczownik odprzymiotnikowy przed dopełniaczem jest zwyczajny.**
`dobry` ma obok czytania przymiotnikowego czytanie `subst`,
a `kod` czytanie lematu `koda` w dopełniaczu mnogim,
więc `Linter pomaga pisać dobry kod.` wychodzi dwoma czytaniami:
raz jest to przymiotnik przed rzeczownikiem,
a raz rzeczownik z dopełniaczem po nim.
Te dwa różnią się częścią mowy, więc są dwoma.
Kryterium, które kasuje czytanie `subst` formy znanej też jako przymiotnik,
gdy stoi ona przed rzeczownikiem z czytaniem w dopełniaczu,
traci 155 zdań, i tracą je te, w których taki rzeczownik dopełniaczem rządzi:
`przewodniczący Rady`, `ministrowi spraw`, `prawa jazdy`, `dobra kraju`.
Zostaje drugie miejsce, w którym tę parę da się rozciąć, czyli sąsiad:
`koda` jest wyrazem, którego ten rejestr nie zna,
a rzadkość formalnego znamienia nie ma,
więc kryterium na nią żąda liczby z korpusu, której olski nie ma.
[todo/](../todo/README.md) trzyma to, co z tej klasy zostaje otwarte,
wraz z pomiarem mówiącym, że nad prozą tego repozytorium
niesie ją paradygmat zaimkowy, a nie przymiotnik.

**Polszczyzna ma słowa nieodmienne, więc sama nieodmienność kryterium nie jest.**
Kryterium trzecie jest dzisiejszym bez warunku o klasie zamkniętej:
czytanie rzeczownikowe o wszystkich siedmiu przypadkach schodzi wtedy z każdej
formy, która ma obok choć jedno inne czytanie,
bo krawędzi bez czytań zostawić nie wolno.
Traci ono 122 zdania i tracą je te, w których polszczyzna naprawdę nie odmienia:
`do dziś` i `od wczoraj`, skrót `PiS` pisany nie samymi wersalikami,
zapożyczenie `jury`, `zen`, `macho`, `logo`,
nazwa obca `Mao`, `Betlejem`, `Merkel`, `Denver`,
oraz rzeczownik męski użyty o kobiecie — `panią prezes`, `pani poseł`, `dyrektor` —
który jest w takim zdaniu nieodmienny dokładnie tak jak nuta.
Od nuty odróżnia te słowa jedno: polszczyzna ich używa,
a znamienia formalnego to rozróżnienie nie ma.
Kryterium kupuje przy tym jednoznaczność 32 zdaniom banku drzew,
odbiera wyprowadzenie 65 zdaniom, z czego 15 przyjętym,
nad prozą tego repozytorium rusza sześć zdań z 6 110,
a nad korpusem audytowym ani jednego.
Płaci więc nad bankiem drzew,
a nad rejestrem, dla którego olski powstaje, nie kupuje nic.

### Kilka procent zdań przyjętych opiera się na czytaniu, którego polszczyzna nie ma

Zdanie przyjęte na takim czytaniu jest gorsze od odrzuconego,
bo pokrycie liczy je jak zdanie przeczytane.
Nad bankiem drzew, nad rejestrem ustaw i nad prozą tego repozytorium
jest ich kilka na sto zdań przyjętych.
Przyjętych, czyli tych, którym werdykt daje jedno odczytanie:
w zdaniu wieloznacznym takie czytanie odbiera jednoznaczność,
a nie przekręca tego, co werdykt o zdaniu mówi.

Liczba pochodzi z czytania ręką, bo klasy tej nie nazywa żadne pytanie do słownika.
`python3 -m olski.check <plik> --morfologia` drukuje pod zdaniem każdą formę,
którą słownik czyta więcej niż jednym sposobem,
wraz z tymi jej czytaniami, które licencjonują ją w przyjętym odczytaniu,
a czytelnik pyta o jedno: czy jest wśród nich to, które sam tej formie daje.
Przeczytano wszystkie 144 zdania przyjęte rejestru ustaw
oraz wszystkie 36 zdań przyjętych korpusu audytowego,
a ze Składnicy pod morfologią żywą i z prozy tego repozytorium
po sześćdziesiąt zdań próbką rozrzuconą po całej liście (`harness/próbka.py`).
Na czytaniu, którego polszczyzna nie ma, opiera się z tego
dziewięć zdań ustaw, jedno zdanie korpusu audytowego,
cztery zdania banku drzew i cztery zdania prozy tego repozytorium.
Korpus audytowy mówi przy tym o kierunku, a nie o udziale:
zdań przyjętych ma 36, a jedno zdanie waży przy takim mianowniku za dużo.

Klasy są trzy i jedno kryterium ich nie obejmuje.

**Nazwa własna czytana nieodmiennie.**
`Podmiotami ochrony ludności są Polski Czerwony Krzyż.` wyprowadza się,
bo nieodmienne `Krzyż` zgadza się z liczbą mnogą i pojedynczą naraz,
a `Jerzy Buzek podkreślił, że Polska jest zainteresowana koncepcją europejskiej
tożsamości obronnej.` — bo nieodmienny `Buzek` staje przydawką dopełniaczową pod imieniem.
To samo czytanie wpuszcza `wójt` i `marszałek` w wyliczeniach organów.
Kryterium na tę klasę jest zmierzone i odrzucone:
bierze ją kryterium trzecie wyżej, a razem z nią zwyczajną polszczyznę,
w której rzeczownik męski użyty o kobiecie jest nieodmienny.

**Forma imienna czytana czasownikiem.**
`Kalisz.`, `Przemyśl.` i `Nowy Sącz.` są pozycjami wyliczenia okręgów wyborczych,
którym ekstrakcja dopisała kropkę,
a `W dalsze wędrówki udaje się tylko dla zmiany ostoi.` jest zdaniem Składnicy,
w którym `ostoi` czyta się formą osobową lematu `ostać`.
`Nowy Sącz.` należy do obu klas naraz — `Nowy` jest w nim nazwą nieodmienną,
a `Sącz` rozkaźnikiem — więc klasy te nie są podziałem.
Wykluczenie ze słownika po tę klasę nie sięga z innego powodu niż po tamtą:
czytanie czasownikowe nie jest nieodmienne,
a co z nią zrobić po stronie ekstrakcji, trzyma [todo/](../todo/README.md).

**Wyraz funkcyjny albo zaimek czytany wyrazem treściowym.**
`Wszystko wyżej pyta o zdanie, po którym zostaje czytań kilka.` jest jednoznaczne,
bo `Wszystko` czyta się przysłówkiem, a `kilka` rzeczownikiem, czyli rybą.
W `Czego na tej liście nie ma.` przysłówkiem jest `czego`,
w `Wszedłem na tę stronę i zrobiłem sobie profil.` rzeczownikiem `soba` jest `sobie`,
a w `Atrybuty dzielą się na typy odzwierciedlające to jakie dane mogą przechowywać.`
spójnikiem jest `to`.
Klasa ta jest z trzech najliczniejsza i ma zdania we wszystkich czterech korpusach.
Czytanie, które daje tym formom czytelnik, jest przy tym w słowniku,
a wygrywa czytanie obok niego, bo tamtego nie licencjonuje żadna produkcja:
zaimka zwrotnego gramatyka nie ma wcale,
`co` poza pytaniem i zdaniem względnym nie ma pozycji rzeczownej
([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)),
a liczebnik za rzeczownikiem nie ma ciała,
bo grupa liczebnikowa stawia go przed nim
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)).
Widać to na tym samym zdaniu z liczebnikiem przestawionym:
`Wszystko wyżej pyta o zdanie, po którym zostaje kilka czytań.`
jest wieloznaczne i `Wszystko` jest w nim podmiotem.
Wykluczenie ze słownika zamieniłoby więc tę klasę na zdania odrzucone,
czyli werdykt nieprawdziwy na uczciwy,
a czytanie czytelnika wraca do niej dopiero z brakującą pozycją.

Liczba jest sądem jednego czytelnika i jest oszacowaniem dolnym.
Widać w niej to, co pokazuje wykaz morfologii,
więc przypadek wybrany źle wewnątrz jednego znacznika do niej nie wchodzi,
a przyłączenie postawione źle jest klasą osobną i nie liczy się tu wcale.
Część klasy pochodzi przy tym ze zdań, które zrobiła ekstrakcja —
pozycja wyliczenia z dopisaną kropką w ustawach,
urwany przykład w prozie tego repozytorium —
a nad bankiem drzew, gdzie zdania przychodzą całe, udział przez to nie spada.

## Notacja tego rejestru jest słowem, którego słownik nie ma

Wykluczenie wyżej odbiera formie czytanie, którego Polak nie ma.
Notacja jest przypadkiem odwrotnym:
słownik nie ma tu czytania żadnego, a czytelnik ma jedno.

`docs/linter.md` jest dla Morfeusza pięcioma segmentami,
bo ukośnik i kropka są dla niego interpunkcją,
a `docs` nie jest żadnym polskim słowem, więc wraca jako `ign`,
którego nie bierze ani jedna produkcja.
Rejestr, o który olskiemu chodzi, jest takich form pełen —
ścieżka, nazwa pliku, nazwa modułu, nazwa polecenia —
i stoją one w zdaniach na miejscach rzeczownika,
bo tym w takim zdaniu są.

Olski daje więc takiej formie jedną krawędź i jedno czytanie nieodmienne.
Rzeczownikiem nieodmiennym taka forma jest w polszczyźnie naprawdę,
a jedno czytanie znaczy, że nie ona daje zdaniu drugie.

Wzorzec, który to rozpoznaje, stoi w `NOTACJA` w `olski/segmentacja.py`,
a tu stoi to, przed czym każde jego żądanie broni,
bo z samego wzorca tego nie widać.
`np.` i `r.` mają kropkę i nie są notacją,
więc kropka spaja tylko wtedy, gdy nie ma po niej spacji.
`m.in.` i `S.A.` spajają się bez spacji i notacją nie są,
więc człon musi być dłuższy niż litera —
za co płaci się ścieżką, której człon jest jednoznakowy,
i takiej olski nie sklei.
`czarno-biały` Morfeusz zna po członach
i sklejony w jedno wypadłby ze słownika razem z gramatyką,
więc łącznik spaja tylko wewnątrz ścieżki, którą trzyma już kropka:
`design-notes.md` wchodzi całe.
`2018.07.23` spaja się kropkami jak ścieżka, a rzeczownikiem nie jest,
i Morfeusz zna tę formę jako liczbę,
więc notacja musi nieść przynajmniej jedną literę.

Własność, przez którą wykluczenie wyżej istnieje, jest tu ceną.
Forma nieodmienna spełnia każde żądanie przypadku,
jakie unifikacja umie postawić,
więc notacja stoi w zdaniu wszędzie tam, gdzie stoi jakikolwiek rzeczownik.
`Cały wywód prowadzi docs/linter.md.` wychodzi z tego dwoma czytaniami,
SVO i OVS, i jest to ta sama wieloznaczność,
którą polszczyzna ma na `Koszt samej szynki przewyższa koszt szynki`:
zdanie naprawdę nie mówi, co tu prowadzi co.

Czytanie nieodmienne bierze przez to połowę klasy, a nie całą.
Drugą połową jest polskie słowo odmienione, którego słownik nie ma,
i tej czytania nieodmiennego dać nie wolno;
wpuszcza ją [leksykon projektu](#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma).

## Wersalik bez czytania jest tym samym rzeczownikiem nieodmiennym

Notacja wyżej poznaje się po znaku, który ją spaja.
`README` nie niesie ani kropki, ani ukośnika,
więc wzorzec notacji go nie widzi,
a Morfeusz oddaje go jako `ign`, którego nie bierze ani jedna produkcja.
Rejestr, o który olskiemu chodzi, stawia takich form kilka na dokument —
`README`, `GLR`, `SGJP`, `LCFRS` — i stoją one na miejscach rzeczownika.

Warunek jest więc drugi i pyta o dwie rzeczy:
forma ma być pisana wersalikami i słownik ma jej nie czytać wcale.
Pierwsze pytanie zadaje już wykluczenie słownikowe,
które wersalik ze swojego zasięgu wyłącza,
bo w wersalikach forma rzeczownikiem właśnie jest
([wyżej](#the-dictionary-offers-readings-polish-does-not)).
Drugie pytanie broni polszczyzny: `NIE` i `PAN` słownik czyta,
więc czytania nieodmiennego nie dostają
i zdanie z nimi nie traci tego, które ma.
Nieodmienna taka forma jest przy tym w polszczyźnie naprawdę:
akronim odmieniony pisze się z łącznikiem i małą końcówką — `PKB-u` —
czyli już nie samymi wersalikami.

Cena jest ta sama, którą płaci notacja, i płaci się ją z tego samego powodu.
`Parser GLR jest tani.` wychodzi z tego jednym czytaniem,
w którym `GLR` jest dopełniaczem przy `parser`,
a czytelnik ma tam dopowiedzenie
([subset.md](subset.md#what-it-does-not-cover-yet) trzyma tę pozycję).
Werdykt mówi więc o tym zdaniu tyle, że się wyprowadza,
a o tym, czym w nim jest `GLR`, mówi nieprawdę.

Bank drzew tej ceny nie mierzy i nie zmierzy.
Przebieg nad Składnicą 180723 wychodzi z tym warunkiem i bez niego
tymi samymi liczbami, co do jednego zdania:
rejestr prasowy pisze wersalikiem akronim, który słownik zna,
a formy nieznanej pisanej wersalikami nie ma tam ani jednej.
Zakup jest przez to widoczny wyłącznie nad prozą tego repozytorium,
gdzie liczbę drukuje `olski.check`,
i tyle właśnie o tym warunku wiadomo.

## Leksykon projektu wpuszcza polskie słowo, którego słownik nie ma

`olski`, `commitów`, `Pythonem` — SGJP nie ma ani jednego z tych słów,
więc Morfeusz oddaje je jako `ign`, którego nie bierze ani jedna produkcja.
Czytania nieodmiennego, którym wchodzi notacja, dać im nie wolno,
i tą jedną rzeczą ta połowa klasy różni się od tamtej:
`commitów` jest dopełniaczem liczby mnogiej,
więc czytanie nieodmienne nie byłoby tu tylko nieznane, ale fałszywe,
a olski obiecuje, że każde jego zdanie jest polszczyzną.
Zgadywanie odmiany po zakończeniu wyrazu odpada z tego samego powodu:
Morfeusza prosi się wprost, żeby formy nieznanej nie zgadywał (`olski/morph.py`),
bo czytanie zgadnięte jest czytaniem, którego nikt nie zadeklarował.

Zostaje deklaracja, a zapisuje ją sekcja `leksykon` w `olski.toml`
w korzeniu repozytorium.
Plik leży tam, a nie w paczce, bo mówi o jednym projekcie:
`commit`, `Świgra` i `lintować` są słowami tego repozytorium,
a kto sprawdza własny tekst, ma własne słowa do zadeklarowania.
Olski szuka go od katalogu roboczego w górę i braku nie zgłasza,
bo projekt bez takiego pliku jest zwykłym projektem
i słowo spoza słownika wraca w nim jako `ign`.
Wpis wskazuje leksem, wedle którego słowo się odmienia, a form nie wypisuje:
`commit` odmienia się wedle `bat`, a `Python` wedle `dzban`.
Wzorzec jest przy tym faktem o odmianie, a nie o znaczeniu,
i dlatego wolno nim wskazać słowo, które z naszym nie ma nic wspólnego.
Wskazuje się leksem, a nie lemat,
bo pod jednym napisem stoi ich kilka i różnią się właśnie odmianą:
`bat:Sm3~a` ma dopełniacz `bata`, a `bat:Sm3~u` ma `batu`.
Jeden lemat ma tyle wpisów, ile leksemów mu się należy,
więc `olski` dostaje tam dwa wpisy, przymiotnik i rzeczownik,
tak samo jak `polski` ma w słowniku dwa leksemy.

Przeciw wskazaniu leksemu stała alternacja tematu,
czyli to, że `plik` ma w miejscowniku `pliku`, a temat na `t` bierze tam `cie`,
więc wzorzec dobrany byle jak wydaje formę, której polszczyzna nie ma.
Alternację niesie jednak sam wzorzec, bo granicę tematu wycina to,
na czym jego własne formy przestają się zgadzać:
`bat` ma `bacie`, więc temat schodzi do `ba`, a końcówką zostaje `t`,
i `commit`, który kończy się na `t`,
bierze stamtąd i `commitach`, i `commicie`.
Końcówka jest zarazem tym, czego wzorzec od naszego słowa żąda,
a żądania niespełnionego nie zostawia się w ciszy:
wpis dający `commitowi` wzorzec `figura` zgłasza się, zamiast wziąć temat wzorca.

Jednej pomyłki wzorzec sam nie łapie i ona jest ceną tego rozstrzygnięcia.
Wzorzec alternujący inaczej niż nasze słowo spełnia warunek na końcówkę
i wydaje formę fałszywą: `pies` daje temat `p` wraz z końcówką `ies`,
więc `bies` dostałby z niego dopełniacz `bsa`.
Trzecią kolumną wpisu jest więc świadek, czyli jedna forma, którą wzorzec ma wydać,
i on tę pomyłkę zgłasza.
Świadek ma być formą inną niż lemat, bo lemat wychodzi z każdego wzorca,
który przeszedł warunek na końcówkę,
a tam, gdzie ta proza słowo odmienia, świadkiem jest forma stojąca w niej naprawdę.

Podmiana tematu idzie tam, gdzie temat stoi, a nie na początku formy,
bo formę wolno poprzedzić przedrostkiem:
słownik trzyma `niemalowanie` w paradygmacie `malować`,
więc `lintować` bierze stamtąd `nielintowanie`.

Wpisu nie dostaje angielska nazwa przytoczona w polskim zdaniu.
`Grammatical Framework` i `Semantic Line Breaks` nie mają polskiego paradygmatu,
więc nie ma czego wskazać i żaden wpis by ich nie wpuścił;
`New Yorkera` i `Morfologik` paradygmat mieć mogłyby i wpisu nie mają,
bo README pisze je w pozycji listy, a nie w zdaniu, na które czeka jakiś werdykt.
Sekcja jest przez to rejestrem tego, co ktoś rozstrzygnął, a nie listą zamkniętą,
i słowo bez wpisu wraca jako `ign`, czyli tak samo jak przed tą sekcją.

Wpisu nie dostaje też leksem dokładany do napisu, który słownik zna,
i tym sekcja ta różni się od `olski/skład/leksemy.py`, który wybiera między leksemami
słownika ([formy-i-leksemy.md](formy-i-leksemy.md#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)).
Projekt piszący o agentach jako o programach żąda liczby mnogiej `agenty`,
a `agenty` z SGJP jest formą deprecjatywną leksemu osobowego, czyli czym innym.
Wpis na taki leksem dokłada czytanie formie, którą słownik już czyta,
więc łamie własność całej sekcji:
ani jednej jego formy słownik nie czyta,
a zdanie już przyjęte nie ma przez to jak stracić na nim jednoznaczności.
Ta połowa klasy zostaje przez to poza tą sekcją, a ruch trzyma [todo/](../todo/README.md).

Czyta ten leksykon cała analiza: `morphology` w `olski/segmentacja.py`,
czyli to samo miejsce, w którym notacja dostaje swoją krawędź,
oraz warstwa rozstrzygająca, kiedy pyta o lemat gospodarza.
Skład go nie czyta, choć tego samego pliku żąda i po swojej stronie
([formy-i-leksemy.md](formy-i-leksemy.md#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr)),
a ruch trzyma [todo/](../todo/README.md).

## Słownictwo projektu orzeka o lemacie w obie strony

[Wykluczenie słownikowe](#the-dictionary-offers-readings-polish-does-not)
mówi o sobie, że odbiera czytania, których polszczyzna nie ma.
Mówi tak o `do` czytanym jako nuta i o `mi` czytanym tak samo,
a o `go` czytanym jako gra tak nie mówi:
`Go jest grą.` jest polszczyzną, a olski tego zdania nie wyprowadza,
bo `go` traci czytanie rzeczownikowe i podmiotu nie ma z czego zbudować.
Kryterium jest więc zakładem o rejestr:
dobrym tam, gdzie o grze nikt nie pisze, i fałszywym w tekście o grze.

Zakład zostaje domyślnością, bo rejestr, dla którego olski powstaje, o grze nie pisze,
a projekt, którego rejestr wygląda inaczej, uchyla go u siebie.
Deklarację zapisuje sekcja `lematy` w `olski.toml`, czyli w tym samym pliku,
który niesie [leksykon projektu](#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma).
Plik jest jeden, bo projekt jest jedną rzeczą:
dwa żądałyby dwóch odpowiedzi na pytanie, gdzie projekt się zaczyna,
i rozjechałyby się na pierwszym, który stoi wyżej od drugiego.

Kierunki są dwa i różni je to, po której stronie wykluczenia stoją.

**`wpuszczane` uchyla wykluczenie na jednym lemacie.**
Jest to kierunek, którego żąda tekst o grze,
i sięga on jednego lematu, a nie klasy czytań:
projekt, który zadeklarował `go`, dalej traci nutę na `do`.
Kryterium pisane na część mowy albo na samą nieodmienność
uchylałoby wykluczenie całe.

Kupuje ona mniej, niż wygląda, bo zaimek pokrywa część pozycji tej gry.
`Zasady go są proste.` wyprowadza się bez deklaracji i wyprowadza raz,
bo zaimek `go` jest także dopełniaczem, więc przydawkę dopełniaczową
ta forma niesie i tak.
Deklaracji trzeba tam, gdzie gra stoi w przypadku, którego zaimek nie ma,
a jest nim przede wszystkim mianownik: `Go jest trudne.`

Płaci się za to całym czytaniem, bo uchylone jest nieodmienne:
niesie liczbę `sg.pl` i wszystkie siedem przypadków naraz,
więc żądaniu przypadka nie odmawia nigdy —
czyli ma dokładnie tę własność, dla której to wykluczenie powstało.
`Kierują go na kursy dywersji.` przestaje być przez to jednoznaczne
w projekcie, który `go` zadeklarował:
`go` staje w nim podmiotem, a takiego czytania polszczyzna nie ma,
bo zaimek `go` jest biernikiem i dopełniaczem, a mianownikiem nie bywa.
Deklaracja kupuje więc zdania o grze w mianowniku
i sprzedaje jednoznaczność zdań z zaimkiem,
a co przeważa, mówi pomiar nad tym tekstem, a nie ten dokument.

**`pomijane` odbiera lematowi czytania w całym projekcie.**
Jest to kierunek dla lematu, po który wykluczenie sięgnąć nie może:
`soba` odmienia się przez przypadki,
więc kryterium nieodmienności do niej nie dochodzi,
a `sobie` i `sobą` są w prozie technicznej zaimkiem i niczym więcej.
Znamienia formalnego, które by ją od zaimka odróżniło, nie ma,
więc nie ma tu czego wyprowadzić i zostaje deklaracja.
Krawędź wolno temu kierunkowi opróżnić,
tak samo jak wolno [formie przyimkowej zaimka](konstrukcje-gramatyczne/grupa-imienna.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą):
projekt, który mówi, że słowa nie używa, mówi to także o zdaniu,
w którym stoi ono samo, i werdykt nazywa wtedy formę bez licencji.

Oba kierunki są warunkami w `olski/segmentacja.py`, a nie produkcjami:
wykluczenie orzeka o formie, a nie o zdaniu,
i deklaracja projektu orzeka o tej samej formie.

Poza ceną, którą płaci deklarujący, mechanizm ten kosztuje osobno.

Werdykt przestaje być funkcją samego zdania.
Dwa projekty czytające ten sam napis dostają dwie odpowiedzi,
a wydruk werdyktu o pliku nie mówi.
Zaczął to leksykon projektu, który czytania dokłada,
a ta sekcja je odbiera, więc sięga zdań, które wyprowadzały się przedtem.

Liczby, które mierzą to wykluczenie —
[ile kupuje i ile kosztuje](corpus.md#what-morphological-ambiguity-costs) —
są odtąd liczbami przy deklaracji pustej.
Repozytorium to ma sekcję `lematy` pustą i po to ją ma wypisaną:
liczby te odtwarza się jego przebiegiem bez zastrzeżeń,
a projekt z deklaracją mierzy co innego i nie ma tego z czym porównać.

Lista pisana ręką rośnie o każdy lemat, który ktoś zauważy,
i tym różni się od kryterium, które broni się samo.
Cena ta jest tu jednak zapłacona świadomie:
kryterium na `soba` [zmierzono i odrzucono](#każde-szersze-kryterium-zmierzono-i-żadne-nie-stoi)
wraz z każdym innym, które szło dalej niż dzisiejsze.

Poza deklaracją zostaje warunek pytający o sąsiada.
[Forma przyimkowa zaimka](konstrukcje-gramatyczne/grupa-imienna.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)
i cząstka zwrotna tracą czytanie przez to, gdzie stoją,
a nie przez to, czym są, więc lemat o nich nie orzeka
i wiersz na `on` nie uchyliłby ani jednego z tych dwóch warunków.
