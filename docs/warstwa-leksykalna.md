# Warstwa leksykalna

Co olski bierze za słowo, których odczytań słownika nie bierze wcale
i czego czasownik żąda wedle leksykonu walencyjnego.
Każde z tych rozstrzygnięć orzeka o produkcji, której jeszcze nikt nie napisał,
więc stoi tu, a nie przy konstrukcji, którą akurat obsługuje
([konstrukcje-gramatyczne/](konstrukcje-gramatyczne/README.md)).
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

To jest połowa klasy, a nie cała.
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

## Walencja jest leksykonem o ramie domyślnej

Czasownik bierze te dopełnienia, których wymaga,
a nie te, które pasują kształtem.
`być` nie bierze dopełnienia w bierniku,
a `On jest wolny.` ma czytanie, w którym bierze:
`wolny` czyta się jako przymiotnik i jako rzeczownik,
a rzeczownikowe staje tam, gdzie produkcja czeka na biernik,
[więc są to dwa odczytania](subset.md#co-się-liczy-jako-jedno-odczytanie).
Takiego czytania nie ma żaden czytelnik tego zdania.

Ramą jest zbiór dopełnień, jakie czasownik bierze,
nazwanych przypadkiem grupy, którą bierze,
wraz z `inf` dla bezokolicznika, bo bezokolicznik przypadka nie ma.
Czasownik wypuszcza ramę z siebie jako cechę,
dopełnienie mówi, którą pozycję ramy zajmuje,
i zgadza je ta sama unifikacja, która zgadza rodzaj z liczbą.
Walencja nie jest więc sprawdzeniem doklejonym do rozbioru, tylko rozbiorem,
dokładnie tak jak [zgodność](subset.md#what-the-grammar-covers).

Leksykon jest otwarty i ma ramę domyślną.
Stoi w nim czasownik, którego rama jest inna niż domyślna —
węższa o biernik albo szersza o przypadek, którego domyślna nie ma
([niżej](#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)) —
a każdy inny bierze domyślną,
więc czasownik dopisuje się wpisem, a nie produkcją,
i nie kosztuje ani jednego przyjętego zdania, dopóki wpisu nie ma.
Ręcznie stoi w nim jeden wpis i jest nim kopula:
narzędnika rama domyślna nie ma, a biernika nie ma rama kopuli.
Reszta wpisów bierze się z Walentego i mówi o lemacie tyle,
ile któryś z kierunków ma z tego czym zapytać, o czym niżej.

Ramę wybiera forma, a nie jej pojedyncze czytanie,
bo inaczej wystarczy formie jeden lemat spoza leksykonu, żeby zawężenie ominąć.
`zapisuje` jest u Morfeusza i od `zapisywać`, i od `zapisować`;
drugiego z nich leksykon nie wymienia, więc czytanie stąd brało ramę domyślną
razem z biernikiem, i `Program zapisuje się ustawienia.` się wyprowadzało,
choć `zapisywać się` biernika nie bierze.
Klasa domyślna pyta więc o wszystkie lematy formy naraz
i wypada tam, gdzie leksykon wymienia którykolwiek z nich
(`bez_lematów_formy` w `olski/grammar.py`).
Forma o lematach niezgodnych bierze przez to ramę najwęższą z nich:
`działa` jest formą `działać`, która biernika nie bierze,
i formą `dziać`, która go bierze; jako forma biernika nie bierze.

Pod złotą morfologią pytanie nie powstaje.
Anotator wybrał po jednym czytaniu na token, więc forma ma tam jeden lemat,
i przebieg nad Składnicą nie rusza ani jednego zdania ani jednego czytania.
Cena i zysk wypadają więc pod Morfeuszem, gdzie ubywa przeszło setka czytań.
Po kilka zdań idzie tam w każdą ze stron:
jedne przechodzą z wieloznacznych na przyjęte, drugie tracą jedyne czytanie.
Rozsądza je czytanie ręką, bo pod żywą morfologią
rozpiętości złotego drzewa nie są porównywalne (`harness/pomiar.py`).
Wypadają w jedną stronę.
Ubywa czytań z dopełnieniem, którego czasownik nie bierze:
`Wszedł do starej komórki.` czytało się także z dopełnieniem `komórki`,
a `Wzrosły również obroty całego rynku.` z dopełnieniem `obroty całego rynku`.
Zdania odrzucone opierały się wszystkie na trzech formach —
`pora`, `sposób`, `cieszą` — i żadne z nich na czytaniu prawdziwym.
`Już pora.` przechodziło z `pora` jako czasownikiem,
`Wprost nie sposób!` z rozkaźnikiem od `sposobić`,
a `Z decyzji cieszą się związkowcy, którzy żądali odwołania dyrektora.`
z dopełnieniem `odwołania dyrektora` wyrwanym ze zdania względnego.
Dla dwóch pierwszych zdań olski czytania prawdziwego nie ma,
bo nie ma predykatywu `pora` ani `nie sposób` na swojej liście
(`PREDYKATYWY` w `olski/subset/słowa.py`; co z tym zrobić, notuje `todo/`),
więc odrzucenie mówi o nich prawdę, której `valid` nie mówiło
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).

Rama domyślna nie jest wygodą, tylko warunkiem, żeby żądanie było żądaniem.
Cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc rama postawiona części czasowników przechodziłaby reszcie za darmo
i „bądź kopulą” nie byłoby wtedy żądaniem.
Jest to zarazem argument, dla którego kopula osobnym symbolem gramatyki nie jest,
choć wygląda na argument za nim:
rama, którą niesie każdy czasownik, żąda tego samego,
a osobny symbol daje jednemu lematowi dwie nazwy w raporcie —
`Ludzie są wolni.` czytałoby się przez jedną, a `Jan jest nauczycielem.` przez drugą.

Rama nie zastępuje przy tym pozycji, i to jest zmierzone.
Orzecznik stoi w trzech miejscach — po czasowniku, po podmiocie w szyku
z czasownikiem na czele, i przed czasownikiem — a rama każe zapytać,
czy te trzy nie są jedną pozycją, w której orzecznik i czasownik dzielą zmienną.
Nie są, i widać to na tym, co zlanie ich w jedną przyjmuje.
Pozycja po podmiocie wpuszcza wtedy kopulę z narzędnikiem,
czyli `Jest Jan nauczycielem.`, którego olski nie ma, a polszczyzna ma,
i to jest cały zysk.
Nad Składnicą tego zdania nie ma, a są dwa inne,
i oba wychodzą przeczytane na opak.
`Na to jest zbyt wielkim tchórzem.` dostaje wtedy podmiot `zbyt`,
a `Inne wymagają ustalenia.` podmiot `ustalenia`;
to drugie przychodzi z pozycji przed czasownikiem,
kiedy wpuścić do niej czasownik, który kopulą nie jest.
Dwa zdania przyjęte więcej i dwa przeczytane na opak
to ta sama zamiana, którą [corpus.md](corpus.md#what-morphological-ambiguity-costs)
liczy w drugą stronę i tam nazywa najgorszym wyjściem tego pomiaru,
więc każda z trzech pozycji zostaje przy swoim żądaniu wobec czasownika.

Zwinięcie kopuli w ramę daje jej przy tym pozycję, do której osobny symbol nie sięga.
Rama dochodzi do bezokolicznika tą samą drogą, co do formy osobowej,
więc `mogą być interesującym materiałem` się wyprowadza,
a produkcja wypisana osobno dla formy osobowej sięga tylko jej.

Cena i zysk kopuli są zmierzone i stoją po jednej stronie morfologii.
Pod złotą morfologią przebieg nad Składnicą nie rusza się o ani jedno zdanie
ani o ani jedno czytanie,
bo anotatorzy wybrali po jednym czytaniu na token
i czytania, które rama zdejmuje, nie ma tam czego zdejmować.
Pod Morfeuszem rama zabiera te zdania,
w których `być` bierze biernik i jest to jedyne ich czytanie,
a daje jednoznaczność tym, które stoją na nim obok czytania prawdziwego;
[corpus.md](corpus.md#what-morphological-ambiguity-costs) trzyma liczby
i zdania, które za nimi stoją.

### Zdania leksykonu pochodzą z Walentego i mówią mniej niż on

Wpis pisany ręcznie kosztuje tyle, co rozstrzygnięcie o jednym czasowniku,
a rama ma obowiązywać wszędzie, więc źródłem jest słownik zrobiony po to.
[Walenty](prior-art.md) charakteryzuje 17 224 lematy czasownikowe
64 022 schematami, a obok nich 1 996 lematów rzeczownikowych 14 295 schematami,
i idzie na licencji CC BY-SA 4.0.
Mówi przy tym o czasowniku znacznie więcej, niż którykolwiek z pytających umie żądać,
więc przekład jest zejściem w dół i o każdy z tych faktów pyta osobnym zdaniem.
Zdanie o bierniku jest ujemne i mówi, że czasownik nie bierze dopełnienia w bierniku.
Zdanie o celowniku i zdanie o dopełniaczu są twierdzące i mówią,
że czasownik bierze dopełnienie w tym przypadku
([niżej](#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)).
Zdanie o celowniku przy wypełnieniu jest węższe od tamtego pierwszego i mówi,
że jeden schemat stawia ten celownik obok drugiej pozycji
([niżej](#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).
Zdania o bezokoliczniku są dwa i jedno jest węższe od drugiego, jak przy celowniku:
szersze mówi, że bezokolicznik przy tym czasowniku stoi,
a węższe — że jego wykonawcą jest podmiot tego samego schematu
([wyżej](#walencja-jest-leksykonem-o-ramie-domyślnej) mówi, komu które służy).
Zdanie o zdaniu podrzędnym mówi, że czasownik bierze zdanie wprowadzone przez `że`,
czyli że stoi przy nim to, co ktoś mówi albo wie
([kategorie-zapisu.md](kategorie-zapisu.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi)).
Kierunek zdania o bierniku jest przeciwny niż kierunek pozostałych,
bo przeciwne są domyślności, od których one odejmują:
rama domyślna ma dopełnienie w bierniku, a nie ma ani przypadka poza nim,
ani bezokolicznika, ani zdania podrzędnego.
`harness/walenty.py` jest tym przekładem i wypisuje `olski/leksykon.txt`,
czyli słowa wraz z tym, które z tych zdań są o nich prawdziwe:
zdanie o bierniku niesie 7 941 wpisów, o celowniku 7 964,
o celowniku przy wypełnieniu 4 889, o dopełniaczu 821,
o bezokoliczniku 363, o bezokoliczniku pod kontrolą podmiotu 285,
a o zdaniu podrzędnym 2 498.
Ramy ten plik nie niesie, bo rama składa się dopiero ze zdań, które on mówi.
Nazywają ją dwa moduły, po jednym na kierunek, bo każdy z nich czyta inne zdania:
`olski/subset/rama.py` wypisuje klasy walencyjne razem z domyślną,
od której je odejmuje, a `rama` w `olski/walencja.py` wydaje składowi
zbiór pozycji jednego lematu.
Czyta ten plik `olski/walencja.py`, i czyta dla wszystkich, którzy pytają,
bo rama jest faktem o słowie, a nie o kierunku, w którym się go używa;
wywód trzyma [design-notes.md](design-notes.md#the-round-trip-invariant).

Kolumna przyimków nie jest zdaniem prawda-fałsz, tylko zbiorem:
przyimki, których żąda rama tego słowa, wzięte z pozycji `prepnp` Walentego.
Kolumnę tę plik wypisuje przy czasowniku i przy rzeczowniku,
bo pyta o nią świadek ramowy warstwy rozstrzygającej i pyta po obu stronach
spornego wyrażenia:
rzeczownik wskazuje mu gospodarza, a czasownik wskazanie odbiera
([rozstrzyganie.md](rozstrzyganie.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie)).
Gramatyka jej nie czyta i nie ma po co:
wyrażenie przyimkowe przyłącza się u olskiego wszędzie, gdzie polszczyzna je stawia,
a wybór miejsca należy do czytelnika
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).

Kolumna ta niesie coś przy 12 195 wpisach,
a 3 800 z nich weszło do pliku nią samą, bez ani jednego zdania obok.
Rzeczownik wchodzi tak zawsze, bo zdania tego leksykonu są o czasowniku
i o rzeczowniku nie orzekają żadnego,
a czasownik o ramie domyślnej wchodzi wtedy, gdy jego schemat przyimka żąda.

Wspólny jest przy tym plik, a nie każde zdanie, które on mówi.
Biernik, celownik i dopełniacz czytają oba kierunki,
zdanie podrzędne sam skład,
a zdania o bezokoliczniku rozchodzą się na dwa: szersze czyta parser
przy czasowniku zwrotnym, węższe skład,
i nie jest to niezgoda o fakt, tylko różnica w tym, co ten fakt komu kupuje.
Po stronie generatora jest bezokolicznik jedyną obroną przed drzewem,
które żąda go od czasownika, który go nie bierze,
bo bezokolicznik z niczym się nie zgadza i pomyłka nie ma jak wyjść inaczej.

Zdanie o zdaniu podrzędnym zmierzono po tej samej stronie i wyszło z tego to samo.
Rama domyślna ma zdanie podrzędne, a leksykon wymienia 1 926 lematów,
które je biorą, więc odjęcie reszty jest wobec Walentego prawdziwe:
`zamykać` bierze biernik, a `Kot zamyka, że mysz śpi.` polszczyzną nie jest.
Nad Składnicą to odjęcie kosztuje jedno zdanie —
`Wystarczy, że ujmiesz w swej pracy twarz i ręce.`, bo `wystarczyć` na liście
nie stoi — a jednoznaczności nie kupuje ani jednej,
pod złotą morfologią i pod Morfeuszem tak samo.
Rama zostaje więc szeroka, tak jak przy bezokoliczniku i z tego samego powodu:
zawężenie prawdziwe, które nie odbiera ani jednego drugiego czytania,
płaci pokryciem za nic.

Klasa słowa jest drugim wymiarem klucza, a nie częścią lematu.
Morfeusz daje `otwierać` i `otwierać się` ten sam lemat,
a wziąć mogą co innego,
więc rama trzymana pod samym lematem zlewałaby te dwa czasowniki w jeden.
Rzeczownik jest z tego samego powodu klasą trzecią, a nie osobnym plikiem:
lemat go od czasownika nie rozdziela, a klucz rozdziela.
Widać to na parze zdań, w której jedno przechodzi, a drugie nie:
`Otwierają się drzwi.` wyprowadza się jednym czytaniem z podmiotem `drzwi`,
a `Otwierają drzwi.` zostaje wieloznaczne, bo tam biernik stoi w ramie.

Narzędnika przekład nie bierze, choć Walenty go zna.
`inst` jest u olskiego pozycją orzecznika,
a Walenty nie odróżnia jej od argumentu narzędnikowego — `bawić się czymś` —
więc wpis wzięty stamtąd wpuszczałby orzecznik tam, gdzie polszczyzna ma dopełnienie.
Dlatego kopula zostaje listą pisaną ręcznie.

Bezokolicznik ma u Walentego dwa kształty, a nie jeden,
i różnicę między nimi niesie kontrola, czyli to, kto wykonuje to,
o czym mówi pozycja podrzędna.
U `chcieć` etykietę kontrolującą nosi pozycja podmiotu,
więc `Córka krawca chciała zejść.` mówi, że zeszłaby ona.
U `kazać` nosi ją pozycja celownikowa,
więc `Krawiec kazał córce zejść.` mówi, że zeszłaby córka.
Zdania są przez to dwa, a nie jedno, i różni je właśnie kontrola.
Szersze mówi, że bezokolicznik przy tym czasowniku stoi,
węższe — że wykonawcą jest jego własny podmiot,
i drugie zawiera się w pierwszym tak samo jak celownik przy wypełnieniu
w celowniku ([niżej](#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).

Węższe czyta skład, bo drzewo stawiające bezokolicznik stawia i wykonawcę,
a `Krawiec kazał córce zejść.` mówi, że zeszłaby córka, i tego skład nie zapisze.
Parser czyta szersze i o kontrolę nie pyta:
bierze `córce` za dopełnienie `kazał`, bo celownik stoi obok wypełnienia,
a kto zeszedł, nie pyta ani jedna produkcja.
Zdanie węższe czytane po tej stronie odbierałoby bezokolicznik czasownikom
bezosobowym — `udać się` i `dać się` kontrolowane są z celownika —
więc `Nie udało się ustalić rasy.` przestałoby się wyprowadzać, choć polszczyzną jest.

Czyta je przy tym sama strona zwrotna, a strona zwykła zostaje przy ramie domyślnej,
i to jest wynik pomiaru.
Gramatyka odmawiająca bezokolicznika tym lematom niezwrotnym,
którym odmawia go Walenty, przyjmuje nad Składnicą dwa zdania mniej
i nie kupuje za to ani jednej jednoznaczności.
Po stronie zwrotnej to samo zawężenie kupuje jednoznaczność każdemu zdaniu,
w którym cząstka stoi między formą osobową a bezokolicznikiem
([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika)),
bo tam pozycja bezokolicznikowa jest tym, co dokłada odczytanie drugie.
Ta sama pozycja ramy kosztuje więc po jednej stronie, a po drugiej płaci,
i rozdziela je nie lemat, tylko to, czy cząstka przy nim stoi.

Bank drzew mówi o walencji sam.
Frazy wymagane niosą w Składnicy swoją pozycję,
więc każde zdanie z werdyktem `FULL` daje ramę swojego czasownika,
a 13 035 takich zdań daje 17 896 wystąpień czasownika i 2 856 lematów.
Źródłem ramy bank być nie może, bo 1 328 z tych lematów widać w nim raz,
a rama wyprowadzona z jednego zdania zabrania wszystkiego, czego to zdanie nie miało.
Sprawdzianem być może: z 616 lematów,
którym Walenty odmawia biernika i które bank drzew zna,
potwierdza 615.
Jedynym sprzecznym jest `być` z 61 wystąpieniami,
i są to zaprzeczone zdania egzystencjalne,
w których pozycja `accgen` jest dopełniaczem, a nie biernikiem,
czyli konstrukcja, [której olski nie ma](subset.md#what-it-does-not-cover-yet).
Liczby tego akapitu bierze się ręcznie nad tym samym bankiem,
tak jak te, o których mówi [corpus.md](corpus.md#fetching-it),
bo `harness/corpus.py` czyta z pola `tfw` dwie role, a nie całą ramę;
co by kosztowało polecenie, trzyma [todo/](../todo/README.md).

Cena i zysk są zmierzone nad Składnicą i idą w obie strony;
liczby niżej wzięto nad gramatyką z chwili, w której leksykon wchodził,
czyli bez przysłówka i bez czterech szyków.
Pod żywą morfologią przebieg przyjmuje 379 zdań zamiast 374,
a wieloznacznych ma 245 zamiast 267.
Odrzuconych przybywa przy tym siedemnaście,
i jest to jedna klasa: zdanie stało na dopełnieniu, którego w nim nie ma.
`Wzrośnie w tym roku dostępność studiów wyższych.`
czytało się z dopełnieniem `dostępność studiów wyższych`,
`Uczy się wykorzystania odpowiednich narzędzi.` z dopełnieniem `wykorzystania`,
które jest tam dopełniaczem liczby pojedynczej, a czytało się jako biernik mnogiej,
a `Pracujemy nad tą grupą dzień i noc.` z dopełnieniem `dzień i noc`,
które jest okolicznikiem w bierniku, a takiego okolicznika olski nie ma.
Ani jedno z tych czytań nie jest czytaniem, które ma czytelnik,
więc odrzucenie stoi tu w miejscu analizy fałszywej, a nie w miejscu trafnej.
To ostatnie zdanie jest zarazem jedynym, o które rusza się przebieg pod złotą
morfologią: jedno z 294 przyjętych zdań ubywa i nie ubywa ani jedno czytanie,
bo anotatorzy wybrali po jednym czytaniu na token.

Plik wejściowy nie stoi w repozytorium, tak samo jak bank drzew:

```sh
curl -L -o walenty.zip \
  'http://zil.ipipan.waw.pl/Walenty?action=AttachFile&do=get&target=walenty_20160418-text.zip'
unzip walenty.zip
python3 -m harness.walenty walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt \
  --rzeczowniki walenty_20160418-text/nouns/walenty_20160418_nouns_all.txt \
  > olski/leksykon.txt
```

Wpis wyprowadzony z Walentego jest utworem zależnym od niego,
więc `olski/leksykon.txt` niesie w nagłówku atrybucję i tę samą licencję.

Leksykon zamyka tyle, ile mówi, i widać to na zdaniu, które go doczekało.
`Działają dwie rzeczy.` czekało na wpis mówiący, że `działać` dopełnienia nie bierze,
bo bez niego liczebnik dopisany do gramatyki dałby temu zdaniu dwa czytania,
a nie jedno: `dwie rzeczy` jest mianownikiem i biernikiem naraz,
a zdanie bez podmiotu bierze dopełnienie.
Wpis stoi, [grupa liczebnikowa](konstrukcje-gramatyczne/grupa-imienna.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
też stoi, i zdanie wychodzi jednym czytaniem.
Leksykon kupił tu więc jednoznaczność, a nie pokrycie,
i widać to dopiero z produkcją, której wtedy nie było.

### Zawężenie orzecznika zgodnego wyceniono i decyzji nie ma

Orzecznik zgodny zgadza się z podmiotem — `Plik jest duży.` —
a narzędnikowego żąda kopula.
Stoi on w ramie domyślnej, czyli bierze go każdy czasownik,
a `Trwa akcja protestacyjna.` wychodzi przez to dwoma czytaniami:
drugie z nich orzeka `protestacyjna` o akcji i polszczyzna go nie ma
([disambiguation.md](disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca)
nazywa taką parę nadgeneracją).
Pozycję tę Walenty ma i pisze ją `adjp(pred)` kontrolowanym z podmiotu,
więc zawężenie wygląda na wpis w leksykonie.
Miarą jest schemat niezleksykalizowany, tak jak przy celowniku
(`bierze_ramą` w `harness/walenty.py`), oraz kontrola z podmiotu, tak jak przy
bezokoliczniku, bo orzecznik zgodny orzeka o podmiocie i o nikim innym;
w wydaniu z 2016 roku odpowiada temu czterdzieści lematów,
w większości podobnych kopuli.

Cena rozkłada się na trzy rzeczy i rozdziela je dopiero przeczytanie zdań.
Kilka zdań prozy tego repozytorium staje się olskimi, bo ginie im czytanie nieprawdziwe:
`Tor składu je ma` traci to, w którym `je` jest czasownikiem,
`Jedna klasa czytań przyszła` to, w którym czasownikiem jest `Jedna`,
a `Trwa akcja protestacyjna` swój orzecznik.
Przeczytano wszystkie osiem i w żadnym nie zginęło czytanie prawdziwe.
Zdań mniej niż tyle przestaje być olskimi i tam ginie czytanie czytelnika:
`Dziewczyna milknie zakłopotana`, `Grupa przechodzi cała`, `Cena wyszła zerowa`,
`Oba tory pokazują się same` — orzeczenie wtórne przy czasowniku,
którego Walenty na poziomie ramy nie wymienia,
bo wypisuje je tam, gdzie należy ono do zwrotu.
Kilkanaście zdań zmienia rodzaj odmowy, a nie odpowiedź, bo z wieloznacznych
robią się niewyprowadzalne, i te dwanaście rozpadło się przy czytaniu na pół:
w jednych ginie czytanie prawdziwe — `zdanie wraca rozstrzygnięte` —
a w innych olski czytania prawdziwego nie miał wcale,
bo `kosztuje mniej niż ona sama` czyta `sama` orzecznikiem przy `kosztuje`
i innego czytania temu zdaniu nie daje.

Zdań olskich wychodzi przez to po zawężeniu więcej, a nie mniej,
i to jest w tym pomiarze rzecz, której tabela przejść nie pokazuje:
przejście `wieloznaczne → odrzucone` liczy się jako cena
([`harness/ruch.py`](../harness/ruch.py) wywodzi, czemu),
a zdaniem olskim nie było ani przed nim, ani po nim.
Wycena nie rozstrzyga zatem tej pozycji i rozstrzygnąć jej nie może sama,
bo waży dwie rzeczy w różnych walutach:
zdanie zwyczajnej polszczyzny, które przestaje się wyprowadzać,
i zdanie, które staje się olskim.
Do przeczytania jest przedtem liczba nad Składnicą, której ten pomiar nie ma,
bo populacja stąd jest tej wielkości, że czterema zdaniami przewraca wniosek.

Tańsze od tego wyboru jest kryterium po stronie przymiotnika.
Czytania, które zawężenie miało zdjąć, różni przymiotnik, a nie czasownik:
`protestacyjna` orzekać nie może, a `zerowa` i `wypisany` mogą,
więc kryterium postawione tam zdejmuje czytania nieprawdziwe,
nie zabierając ani jednego orzeczenia wtórnego.
Różnica ta jest własnością przymiotnika odrzeczownikowego,
której tagset nie niesie, więc `niesie` po nią nie sięga
([kanał cech](parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)),
a rejestr techniczny pisze takie przymiotniki gęsto:
`plik konfiguracyjny`, `leksykon walencyjny`.
Kryterium takie mógłby dać katalog przymiotnikowy Walentego,
którego przekład nie czyta, bo nikt o niego nie pytał.

### Leksykon licencjonuje dopełnienie w celowniku i w dopełniaczu

Rama domyślna ma dopełnienie w bierniku i nie ma dopełnienia w przypadku innym,
a czasownik, któremu Walenty daje pozycję celownikową albo dopełniaczową,
dostaje ją wpisem w leksykonie.

```sh
python3 -m olski.check --readings --zatrzymania -c "Werdykt służy czytelnikowi.
Parser wyprowadza czytelnikowi.
Wpis żąda dowodu.
Sonda mierzy dowodu."
```

```text
<text>: Werdykt służy czytelnikowi.
        - podmiot: Werdykt, dopełnienie: czytelnikowi, orzeczenie: służy
<text>: Parser wyprowadza czytelnikowi.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
<text>: Wpis żąda dowodu.
        - podmiot: Wpis, dopełnienie: dowodu, orzeczenie: żąda
<text>: Sonda mierzy dowodu.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
```

Rozdziela te pary leksykon, a nie przypadek:
`służyć` i `żądać` mają w Walentym tę pozycję, a `wyprowadzać` i `mierzyć` nie mają.
Zdanie tego nie orzeka o samym przypadku przy czasowniku,
bo celownik stoi w polszczyźnie i przy czasowniku, który go w ramie nie ma:
`Kompilator wyprowadza psa agentowi.` jest polszczyzną i jest odrzucone
([niżej](#wolny-celownik-nie-jest-pozycją-ramy-i-nie-wchodzi-leksykonem)).
Zajmują przy tym tę samą pozycję ramy, co dopełnienie w bierniku,
a różni te produkcje sam przypadek grupy, która tę pozycję wypełnia,
tak samo jak różni je [dopełniacz negacji](konstrukcje-gramatyczne/orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem).

Przeczenie tych dwóch pozycji nie rusza i ruszać nie ma czego:
dopełniacz negacji wchodzi w miejsce biernika i tam kończy się jego zasięg,
a `nie służy czytelnikowi` stoi w celowniku tak samo jak `służy czytelnikowi`.
Tam, gdzie czasownik bierze dopełniacz z obu powodów naraz,
jeden napis wyprowadza się dwa razy,
a `Wpis nie żąda dowodu.` wychodzi jednym czytaniem,
bo kształt obu wyprowadzeń jest ten sam
([subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie)).

Drugiego dopełnienia obok pierwszego ta pozycja nie daje;
daje je [pozycja niżej](#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)
i wpuszcza ją osobne zdanie leksykonu.
Wyrażenia przyimkowego to nie dotyczy, bo ono jest okolicznikiem:
`Parser mówi autorowi o czytaniach.` wyprowadza się i wychodzi wieloznaczne,
bo [olski nie wybiera przyłączenia](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).

Zdanie leksykonu jest tu twierdzące, a zdanie o bierniku ujemne,
i ta różnica rozstrzyga o tym, których schematów Walentego wolno się pytać.
Zdanie ujemne odejmuje od ramy domyślnej,
więc kształt policzony za szeroko zostawia lemat przy tej ramie i nic o nim nie mówi.
Zdanie twierdzące ramę poszerza, więc ta sama pomyłka wpuszcza dopełnienie tam,
gdzie polszczyzna go przy tym czasowniku nie stawia.
Odpadają przez to dwa rodzaje schematu.
Schemat z pozycją zleksykalizowaną jest zwrotem,
a pozycja stojąca w nim obok należy do zwrotu, a nie do lematu:
celownik ma w Walentym `mieć` i ma go ze zwrotu `mieć komuś za złe`,
a policzony osobno daje `Ludzie mają rozum i sumienie.` drugie czytanie,
w którym `Ludzie` jest celownikiem od `Luda`, a ciąg współrzędny stoi w podmiocie.
Schemat spoza `BRANE` w `harness/walenty.py` nazywa zaś polszczyznę,
której ten rejestr nie pisze,
i odpada z tego samego powodu, z którego odpada w kolumnie przyimków.

#### Wolny celownik nie jest pozycją ramy i nie wchodzi leksykonem

Celownik posiadacza i tego, komu się przysłuży — `wyprowadzić komuś psa`,
`ściągnąć komuś czapkę`, `wykryć komuś raka` — nie jest pozycją, której czasownik żąda,
tylko członem dochodzącym do całego orzeczenia,
więc Walenty go nie wypisuje i wypisać nie może: stoi on przy czasowniku dowolnym
([disambiguation.md](disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma)
liczy, ile takich celowników łapie kryterium pisane pod inną pozycję).
Leksykon nie ma więc czym go wpuścić, a wpis zmyślony wpuszczałby przy jednym lemacie
to, co polszczyzna ma przy każdym.

Odrzucenie pada tu przy tym dwa razy, a nie raz.
`Kompilator wyprowadza psa agentowi.` nie ma czytania także wtedy,
gdy się celownik temu lematowi dopisze, bo dopełnienie stoi tam obok dopełnienia
([subset.md](subset.md#what-it-does-not-cover-yet)),
a wolny celownik dochodzi zawsze do orzeczenia, które ma już swoje wypełnienie.
Ruchem jest przez to pozycja okolicznika, a nie pozycja ramy,
i tym różni się ona od dwóch wpuszczonych wyżej:
okolicznik dochodzi wszędzie, więc taka pozycja bierze każdą formę czytaną celownikiem,
a te dzielą kształt z miejscownikiem w całej odmianie żeńskiej.
Ceny tego nikt nie policzył; `todo/` trzyma ten przebieg.

Cena i zakup są zmierzone nad Składnicą 180723 sondą różnicową,
która zdejmuje produkcję dopełnienia w jednym przypadku,
i wypadają po obu stronach morfologii inaczej.
Pod złotą morfologią celownik nie odbiera jednoznaczności ani jednemu zdaniu,
a daje ją kilkudziesięciu, które przedtem nie miały żadnego czytania.
Dopełniacz jednoznaczność odbiera, a daje ją przeszło dwa razy większej liczbie zdań,
niż tamtych odbiera.
Role zdań nowo przyjętych zgadzają się przy tym z drzewem wzorcowym
w przeszło czterech piątych, a odwrócone nie jest ani jedno,
czyli zdania te przychodzą z czytaniem, które ma czytelnik
([corpus.md](corpus.md#what-morphological-ambiguity-costs) mówi, ile waży odwrotne).
Pod Morfeuszem obie pozycje kosztują więcej, bo forma ma tam kilka czytań naraz,
i ruch idzie tam głównie z odrzuconych do wieloznacznych:
przyjętych przybywa kilkadziesiąt, a odrzuconych ubywa przeszło dwieście.
Obie pozycje ruszają przy tym te same kilkanaście zdań,
a zdania, o którym razem mówiłyby co innego niż każda z osobna, nie ma ani jednego.

Nad prozą tego repozytorium ta sama sonda liczby przyjętych prawie nie rusza,
choć kilkudziesięciu zdaniom zmienia werdykt,
i nie jest to sprzeczność z liczbami wyżej, tylko
[zasłanianie](pisanie-po-olsku.md#zasłanianie-działa-w-obie-strony):
zdanie o dwudziestu wyrazach ma kilka zatrzymań naraz,
więc pozycja zdejmuje jedno z nich i zostawia zdanie odrzucone, tylko dalej.
Widać ją za to nad zdaniem krótkim.

### Druga pozycja ramy jest celownikiem obok wypełnienia

`Parser pokazuje autorowi oba czytania.`, `Parser mówi autorowi, że zdanie czyta się dwojako.`
Celownik stoi tu obok wypełnienia, które pozycję ramy zajmuje, a nie w niej samej,
i tym różni się od [dopełnienia w celowniku](#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu),
które tę pozycję wypełnia samo.
Pozycja ta jest przez to faktem o wpisie leksykonu, a nie konstrukcją obok innych,
i dlatego stoi tutaj, a nie w
[konstrukcjach](konstrukcje-gramatyczne/README.md): licencji udziela jej schemat Walentego,
a nie ciało napisane ręką.

```sh
python3 -m olski.check --readings --zatrzymania -c "Parser pokazuje autorowi oba czytania.
Parser pokazuje oba czytania autorowi.
Reguła pomaga autorowi oba czytania.
Parser pokazuje autorowi autorowi."
```

```text
<text>: Parser pokazuje autorowi oba czytania.
        - podmiot: Parser, dopełnienie: autorowi + oba czytania, orzeczenie: pokazuje
<text>: Parser pokazuje oba czytania autorowi.
        - podmiot: Parser, dopełnienie: oba czytania + autorowi, orzeczenie: pokazuje
<text>: Reguła pomaga autorowi oba czytania.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
<text>: Parser pokazuje autorowi autorowi.
        brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
```

Parę wpuszcza własne zdanie leksykonu, a nie koniunkcja dwóch tamtych,
i liczy się je z jednego schematu Walentego.
Celownik z jednego schematu i biernik z drugiego pary nie dowodzą:
takich lematów jest 641, i to one dzielą `pomagać` od `pokazywać`.
Sąsiadem musi być przy tym wypełnienie, które olski ma —
dopełnienie w bierniku, bezokolicznik, zdanie podrzędne albo pytanie zależne —
bo celownik obok wyrażenia przyimkowego pary nie potrzebuje:
`mówić komuś o czymś` wychodzi okolicznikiem, który przyłącza się za darmo.
Liczony szerzej dawałby parę 2 434 lematom, które poza takim sąsiadem żadnego nie mają.

Licencję niesie cecha, a nie druga pozycja wypisana w ramie.
Ramę unifikacja przecina, więc dwie pozycje wypisane w niej byłyby alternatywą,
a żądanie jest tu koniunkcją: celownik razem z wypełnieniem, nie jedno albo drugie.
Cecha licencjonuje przez to sam celownik, a wypełnienie licencjonuje rama obok niej.

Który sąsiad przy nim stoi, zdanie leksykonu przemilcza,
i jest to ta sama zgrubność, którą ma sama rama domyślna:
skoro daje ona każdemu czasownikowi biernik, bezokolicznik, zdanie i pytanie naraz,
para rozdzielona na cztery zdania byłaby dokładniejsza od tego, do czego dochodzi.
Walenty daje celownik przy bierniku 4 611 lematom, przy zdaniu 666,
przy pytaniu 360, a przy bezokoliczniku 91.
Dopełniacza ta pozycja nie bierze, bo przy wypełnieniu daje go Walenty
kilkudziesięciu lematom, a celownik kilku tysiącom.

Cena i zakup są zmierzone nad Składnicą 180723 przebiegiem przed zmianą i po niej.
Pod złotą morfologią czytanie dostaje przeszło sto zdań, które przedtem nie miały żadnego,
a jednoznaczności nie traci ani jedno zdanie przyjęte;
czytań przybywa pojedynczym zdaniom już wieloznacznym.
Zgodność ról z drzewem wzorcowym spada o niecały punkt
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Pod Morfeuszem czytanie dostaje tyle samo zdań, a cena jest widoczna:
jednoznaczność traci kilkadziesiąt zdań przyjętych,
bo celownik dzieli formę z miejscownikiem w całej odmianie żeńskiej,
więc każde `w gramatyce` za czasownikiem z parą czyta się także jej celownikiem.
Część tych zdań na tym zyskuje, a nie traci:
`Pokazują go swoim gościom.` ma jedno czytanie i jest nim czytanie czytelnika,
bo biernik i celownik dochodzą tam do czasownika dopiero razem.

Okolicznik staje między członami pary, bo ten rejestr tak pisze —
`pokazuje autorowi w wydruku oba czytania` —
i miejsce to zmierzono osobno: kupuje kilka zdań, a jednoznaczność odbiera pojedynczemu.
Bez niego wyrażenie przyimkowe w tym miejscu ma jednego gospodarza zamiast dwóch,
czyli gramatyka wybierałaby przez przeoczenie
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).

Werdykt nazywa oba dopełnienia, rozdzielając je plusem,
bo rola o dwóch wypełnieniach czytałaby się jak dwie role:

```sh
python3 -m olski.check --readings -c "Parser pokazuje autorowi oba czytania."
```

```text
<text>: Parser pokazuje autorowi oba czytania.
        - podmiot: Parser, dopełnienie: autorowi + oba czytania, orzeczenie: pokazuje
```

## Żądanie pozycji jest osobnym plikiem, a nie kolumną leksykonu

Leksykon mówi, co czasownik bierze, a nie mówi, czego od tego żąda.
`zażądać` bierze dopełnienie w dopełniaczu,
a w podmiocie żąda człowieka,
i to drugie zdanie stoi w wydaniu TEI Walentego:
rama nazywa tam pozycję rolą i żąda od niej klasy rzeczy,
a wydanie tekstowe, z którego powstaje leksykon, tej warstwy nie niesie
([prior-art.md](prior-art.md#polish-language-resources)).
Wychodzi ono z tamtego wydania osobnym plikiem — `olski/żądania.txt` —
a nie kolumną leksykonu.

Rozstrzyga o tym to, kto który plik czyta.
Leksykon czyta gramatyka przy imporcie i bez niego nie startuje,
a żądania nie czyta ani jedna produkcja: czyta je werdykt, i to na żądanie flagi
([niżej](#werdykt-nazywa-żądanie-obsadzonej-pozycji)).
Kolumna dokładałaby przez to megabajt do pliku, od którego zależy start,
a czytałby ten megabajt ktoś, kogo na tej drodze nie ma.
Wiersz leksykonu przestałby też być zdaniem o jednym słowie:
żądanie mówi o pozycji, a jedno słowo obsadza ich kilka,
więc wiersz jest tu jeden na rolę w pozycji, a nie jeden na słowo.
Do paczki plik wchodzi tak samo jak leksykon,
bo `pyproject.toml` wpuszcza tam dane, które czyta kod paczki.

Kolumn jest pięć i mówią, czego czasownik żąda od słowa w swojej pozycji:
lemat, klasa słowa, pozycja, rola tej pozycji oraz klasy rzeczy, których żąda.
Pozycje noszą nazwy olskiego tam, gdzie olski je ma,
a `subj` i `prepnp(od)` nazwy Walentego, bo pozycji podmiotu ani przyimkowej
olski w ramie nie ma.
Klasy zbierają się po wszystkich ramach lematu, więc kolumna jest alternatywą:
`ALL` obok klasy nazwanej znaczy, że w jednym znaczeniu pozycja nie żąda niczego.

Czytanie jest złączeniem trzech warstw, a nie odczytaniem wiersza,
i tym jest droższe od przekładu obok:
argument niesie rolę wraz z żądaniem, pozycja wraz z frazą stoi w warstwie
składniowej, a wiąże je trzecia warstwa, po jednym spięciu na parę.
Co to czytanie bierze, a czego nie, mówi `harness/żądania.py`.
Wydanie TEI waży rozpakowane kilkaset megabajtów
i nie stoi w repozytorium, tak samo jak wydanie tekstowe i bank drzew:

```sh
curl -L -o walenty-tei.zip \
  'http://zil.ipipan.waw.pl/Walenty?action=AttachFile&do=get&target=walenty_20160418-TEI.zip'
unzip walenty-tei.zip
python3 -m harness.żądania walenty_20160418-TEI/walenty_20160418.xml > olski/żądania.txt
```

Wpis wyprowadzony z Walentego jest utworem zależnym od niego,
więc `olski/żądania.txt` niesie w nagłówku atrybucję i tę samą licencję,
tak samo jak leksykon.

### Przekład ma pozycje ramy, a okolicznika nie ma

Pozycję dostaje w tym pliku podmiot, dopełnienie w trzech przypadkach,
bezokolicznik, zdanie podrzędne, pytanie zależne i wyrażenie przyimkowe.
Poza plikiem zostaje argument narzędnikowy, bo `inst` jest u olskiego pozycją
orzecznika i jest to ten sam brak, który ma
[leksykon](#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on),
oraz zdanie pod zaimkiem i pozycja zleksykalizowana, których olski nie ma czym wypisać.

Największym brakiem jest okolicznik.
Walenty pisze go osobnym kształtem — `xp(locat)` jest okolicznikiem miejsca —
a olski nie ma takiej pozycji ramy,
bo wyrażenie przyimkowe przyłącza się u niego wszędzie, gdzie polszczyzna je stawia,
więc żądanie doszłoby do zdania tylko przez przyimek.
Tego przyimka ten kształt nie nazywa:
nazywa go dopiero tabela rozwinięć z tego samego wydania,
gdzie jedna pozycja miejsca rozwija się w trzydzieści przyimków,
czyli w trzydzieści wierszy mówiących jedno.
Klasy `MIEJSCE` żąda przy tym w większości właśnie pozycja okolicznikowa,
więc żądanie przestrzeni fizycznej zostaje poza tym plikiem,
a razem z nim przykład z celu o [żądaniu czasownika](roadmap.md#cele).
Ten przykład i tak by w nim nie stanął:
`stać` jest jednym z czasowników, którym Walenty ramy nie daje wcale
([prior-art.md](prior-art.md#polish-language-resources)),
więc żądanie przestrzeni fizycznej trzeba by wziąć skądinąd.

Druga połowa celu nie jest przy tym w tym pliku i nie może być.
Więcej niż co czwarty wiersz żąda klasy, której ten plik nie umie nazwać,
bo Walenty pisze ją zbiorem synsetów plWordNetu, a nie klasą nazwaną;
takie żądanie wychodzi znacznikiem, żeby zbiór klas nie kłamał milczeniem.
Czy słowo stojące w zdaniu do klasy należy, orzeka wordnet,
którego to repozytorium nie ma,
i jest to pytanie do świata
([open-questions.md](open-questions.md#shared-questions)).

### Werdykt nazywa żądanie obsadzonej pozycji

Werdykt mówi, czego czasownik żąda od tego, co w jego pozycji stanęło,
i mówi to pod flagą, obok streszczenia czytania:

```sh
python3 -m olski.check --readings --żądania -c "Autor doradza czytelnikowi poprawkę."
python3 -m olski.check --żądania -c "Program zażądał raportu."
```

```text
<text>: Autor doradza czytelnikowi poprawkę.
        - podmiot: Autor, dopełnienie: czytelnikowi + poprawkę, orzeczenie: doradza
        podmiot „Autor”: „doradza” żąda klasy PODMIOTY
        dopełnienie „czytelnikowi”: „doradza” żąda klasy LUDZIE
        dopełnienie „poprawkę”: „doradza” żąda klasy KOMUNIKAT albo SYTUACJA albo WYTWÓR
<text>: Program zażądał raportu.
        podmiot „Program”: „zażądał” żąda klasy LUDZIE albo klasy, której olski nie nazywa
        dopełnienie „raportu”: „zażądał” żąda klasy CZYNNOŚĆ albo OBIEKTY
```

Werdykt nazywa żądanie i nie pyta, czy słowo w pozycji je spełnia.
Drugie zdanie wydruku pokazuje, ile to zostawia autorowi i ile mu zabiera:
`zażądać` żąda w podmiocie ludzi, a stoi tam program,
więc czytelnik tego wiersza widzi, czego czasownik chciał,
i sam rozstrzyga, czy metafora jest tu na miejscu.
Rozstrzygnąć to za niego mógłby wordnet, którego to repozytorium nie ma
([open-questions.md](open-questions.md#shared-questions)),
a w tym zdaniu i on jest potrzebny, bo `zażądać` żąda ludzi albo klasy,
której olski nie nazywa; żądanie samych klas osobowych rozstrzyga bez niego
deklaracja projektu ([niżej](#deklaracja-projektu-rozstrzyga-żądanie-osoby)).
Wiersz idzie przez to pod flagą, a nie w samym werdykcie:
nie jest znaleziskiem, tylko materiałem do przeczytania
([subset.md](subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego)).

Adresatem tego wiersza jest reguła o wymyślonym sprawcy, a nie ta o czasowniku
domowym ([CLAUDE.md](../CLAUDE.md#dla-kogo-jest-napisane-zdanie)).
Czasownikowi domowemu tamta reguła każe podstawić czasownik dokładny,
a `stać`, `trzymać`, `brać` i `nieść` nie mają w Walentym ramy semantycznej wcale,
więc test podstawieniowy zostaje przy człowieku.
Regule sąsiedniej wiersz ma za to co powiedzieć:
`kupować` żąda w podmiocie ludzi albo podmiotów, a `rozstrzygać` bierze tam
i komunikat, więc „leksykon kupuje jednoznaczność” dostaje świadka,
a „dokument rozstrzyga” nie.

Wiersz jest jeden na obsadzoną pozycję, a nie jeden na rolę:
`dopełnienie` nie mówi, w którym przypadku stoi,
a `Autor doradza czytelnikowi poprawkę.` obsadza nim celownik i biernik naraz,
i czasownik żąda od nich czego innego.
Pozycję nazywa więc przypadek wypełnienia, a pod przeczeniem dwa naraz,
bo dopełnienie w bierniku staje tam w dopełniaczu.
Fraza bezokolicznikowa zostaje przy tym cała poza wierszem:
`dokument` w `Autor zamierzył edytować dokument.` obsadza pozycję `edytować`,
a nie tego czasownika, przy którym stoi podmiot,
więc wiersz o nim mówiłby o żądaniu cudzej ramy.

Milczenie jest odpowiedzią częstą, a kryterium trzyma `olski/żądania.py`.
Nad prozą tego repozytorium wiersz dostaje kilka procent zdań
i bierze się to głównie z zasięgu samego pliku:
`mówić`, `stać`, `brać`, `czytać` i `mieć` nie mają w tym wydaniu ramy żadnej,
a to nimi ten rejestr orzeka najczęściej.
Alternatywa nienazwana zostaje za to w wierszu — `zażądał` wyżej ma ją obok
klasy `LUDZIE` — bo wiersz o samych ludziach byłby żądaniem ostrzejszym,
niż Walenty stawia.

### Deklaracja projektu rozstrzyga żądanie osoby

Wiersz wyżej nazywa żądanie i na tym staje,
bo o przynależności do klasy orzeka wordnet.
Klasy osobowe są tą częścią pytania, która wordnetu nie żąda:
kto w rejestrze jest kimś, a co jest rzeczą, wie autor rejestru.
Mówi to sekcją `osoby` w `olski.toml`, czyli tam, gdzie mówi już,
wedle którego leksemu odmienia się słowo, którego słownik nie ma
([wyżej](#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)).
Flaga wypisuje wtedy pozycje, w których czasownik żąda kogoś, a stoi w nich rzecz.

```sh
python3 -m olski.check --osoby -c "Autor doradza czytelnikowi poprawkę.
Sonda drukuje liczby."
```

```text
<text>: Sonda drukuje liczby.
        podmiot „Sonda”: „drukuje” żąda klasy PODMIOTY, a „sonda” nikogo nie nazywa
zdań: 2; wieloznaczne: 0; bez odczytania: 0
```

Zdanie pierwsze milczy całe, bo `autor` i `czytelnik` stoją w deklaracji tego
projektu, a żądanie od obu tych pozycji wypisuje sekcja wyżej.
Osobą jest tu ten, kogo Walenty żąda klasami `LUDZIE`, `ISTOTY` i `PODMIOTY`,
czyli i człowiek, i zwierzę, i organ, który działa jak człowiek,
więc wiersz mówi, że słowo nikogo nie nazywa, a nie że nie jest człowiekiem.
Trzy klasy razem, bo pytanie deklaracji jest jedno,
a rozdzielenie ich żądałoby taksonomii, czyli znów wordnetu.
Zasięg tego pytania jest przy tym większy niż trzy klasy z dwudziestu:
6 525 wierszy o podmiocie z 10 558 nie żąda w tym pliku niczego poza kimś,
a w celowniku 1 282 z 1 821.

Alternatywa nienazwana znosi żądanie osoby w całości
i tym odpowiedź jest węższa od wiersza materiału:
`zażądać` żąda w podmiocie ludzi albo zbioru synsetów,
więc rzecz stojąca tam spełnia żądanie w tym drugim znaczeniu.
Nad prozą tego repozytorium zawężenie to odejmuje blisko połowę pozycji,
w których żądanie jest osobowe.
Wiersz jest przy tym o zdaniu, a nie o odczytaniu.
Pozycję obsadza czytanie, więc wiersz mówi, że w którymś z nich stoi rzecz tam,
gdzie czasownik żąda kogoś.
Wykaz na odczytanie kazałby przeczytać kilkanaście kopii jednego wiersza,
bo tyle czytań miewa zdanie wieloznaczne.

Deklaracja jest zamknięta: lemat spoza niej nikogo nie nazywa.
Kierunek odwrotny, czyli deklaracja rzeczy, jest kampanią bez końca,
bo rzeczowników rejestr niesie tysiące, a osób garść,
i myli się po cichu, bo słowo niezadeklarowane zostawia warstwę milczącą,
a milczenia nikt nie czyta.
Zamknięta myli się widocznie: osoba, której nikt nie zadeklarował, dostaje wiersz,
a wiersz poprawia się jednym wpisem.
Projekt bez tej sekcji nie ma nikogo,
więc wykaz wraca u niego do materiału zawężonego do klas osobowych.

Adresatem tego wykazu jest reguła o wymyślonym sprawcy
([CLAUDE.md](../CLAUDE.md#dla-kogo-jest-napisane-zdanie)) i przegląd, który ją zadaje.
Nad prozą tego repozytorium `--żądania` wypisuje przeszło dwa tysiące wierszy,
a `--osoby` przeszło sto, nad sześćdziesięcioma zdaniami, i tyle czyta się ręką.
Znaleziskiem wiersz nie jest i być nie może, bo ta sama reguła zostawia
metonimię zwykłą wprost — `dokument mówi` i `reguła żąda` są w niej polszczyzną —
a wykreśla dopiero to, co rzeczy przypisuje wolę albo doznanie.
Tego rozróżnienia nie niesie żadna klasa Walentego,
więc rozstrzyga je czytelnik, a olski podaje mu miejsca do przeczytania.
