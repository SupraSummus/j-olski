# Warstwa rozstrzygająca: co wskazuje i ile się myli

Zdanie, w którym wyrażenie przyimkowe dochodzi raz do jednego słowa, raz do innego,
olski odrzuca i oddaje czytania autorowi ([README](../README.md)).
Warstwa rozstrzygająca wskazuje przy takim zdaniu jedno z tych słów — gospodarza —
obok werdyktu i wraz z powodem wskazania.

Czemu warstwa ma kształt świadka wskazującego z powodem,
a nie kształt rankingu porządkującego cały las,
wywodzi [disambiguation.md](disambiguation.md);
stamtąd pochodzi i kolejność świadków w kodzie
([hipoteza](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza)).
Ten dokument przyjmuje tamten wywód za przesłankę i mówi, co z niego wyszło:
którzy świadkowie odpowiadają, czym każdy z nich dowodzi,
nad czym go zmierzono i jak często się myli.

## Zalążek odpowiada obok werdyktu i nazywa swoją częstość pomyłek

`olski/rozstrzyganie.py` jest tej warstwy zalążkiem
i jest w repozytorium po to, żeby kierunek dał się zmierzyć,
a nie żeby zdania rozstrzygać.
Trzy rzeczy z [wywodu o cenie](disambiguation.md) są w nim wzięte wprost,
a pod nimi opis trzech świadków, których ta warstwa ma.

**Werdykt zostaje nietknięty.**
`rozstrzygnij` bierze przyłączenia z gotowego wyniku rozbioru
i oddaje odpowiedź obok niego,
więc `valid`, `ambiguous` i `rejected` znaczą po jej dopisaniu to, co znaczyły.
`olski-check --rozstrzygaj` wypisuje ją pod werdyktem, ze znakiem zapytania na przedzie:

```sh
python3 -m olski.check --rozstrzygaj -c "Daj przepis na faworki."
```

```text
<text>: Daj przepis na faworki.
        2 odczytania, różne w roli: dopełnienie; „na faworki” → „Daj”, „przepis”
        ? „na faworki” → „przepis”: „na” przy „przepis” doszło tam w 4 z 4 wypadków banku drzew, 100%
```

**Jednostką jest świadek, a nie model.**
Świadek patrzy na jedno przyłączenie i albo wskazuje gospodarza wraz z powodem, albo milczy,
a milczenie jest odpowiedzią domyślną i pełnoprawną.
Świadkowie idą w kolejności rodzaju dowodu i pierwszy odpowiadający wygrywa,
więc dowód o tym tekście bije dowód o cudzym korpusie wszędzie tam,
gdzie oba mówią coś naraz.
Kolejność ta jest
[hipotezą wywodu o cenie](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza)
zapisaną w kodzie, a nie wynikiem porównania dwóch trafności.
Powód wraca razem ze wskazaniem, żeby wskazanie dało się sprawdzić bez zaglądania do tabeli.

**Świadkowie są trzej i jeden z nich jest tym, którego wywód o cenie wycenia najwyżej.**
Leksykon jest tańszy od rankingu i
[sekcja o leksykonie](disambiguation.md#leksykon-rozstrzyga-część-i-rozstrzyga-ją-deterministycznie)
tak go wycenia,
a `Rama` jest tym leksykonem pytanym o jedno przyłączenie.
Tożsamość czytania jest tańsza tym samym rachunkiem i tutaj jej nie ma
z powodu, który podaje
[sekcja o tożsamości](disambiguation.md#tożsamość-czytania-jest-tańsza-i-częściowo-już-stoi):
czeka ona na sąd o parze czytań, którego żaden korpus nie zapisuje.

**Świadek kontekstowy odpowiada powtórzeniem.**
`Powtórzenie` szuka w akapicie miejsca, w którym ta sama fraza stała już
przy którymś z gospodarzy, i wtedy wskazuje tego gospodarza:

```sh
python3 -m olski.check --rozstrzygaj -c "Wystąpiła awaria w systemie. Operator zgłosił awarię w systemie."
```

```text
<text>: Wystąpiła awaria w systemie.
        2 odczytania, różne w roli: podmiot; „w systemie” → „Wystąpiła”, „awaria”
<text>: Operator zgłosił awarię w systemie.
        2 odczytania, różne w roli: dopełnienie; „w systemie” → „zgłosił”, „awarię”
        ? „w systemie” → „awarię”: „w systemie” stało już przy „awaria” wyżej w tekście: „Wystąpiła awaria w systemie.”
zdań: 2; wieloznaczne: 2; bez odczytania: 0
```

Dowodem jest powtórzenie, a nie znajomość rzeczy.
Fraza, którą autor postawił przy tym gospodarzu zdanie wcześniej,
jest w tym tekście jego opisem, bo już raz nim była.
Sąsiedztwo, które rzecz tylko wprowadza, mówi mniej:
po `Mamy nowy system.` świadek milczy i zostawia to zdanie tabeli.
Reguła, która by tam odpowiadała — rzecz raz wprowadzona jest znana,
więc fraza nie identyfikuje rzeczownika i dochodzi do czasownika —
odpada na kontrprzykładzie, a nie na ostrożności:
po `Widziałem hasła.` fraza `z hasłami` dalej dochodzi do `plik`.

Zdanie tego przykładu polszczyzna naprawdę czyta dwojako:
awaria jest w systemie albo zgłoszenie w nim padło,
i oba są w rejestrze dokumentacji zwykłe.
Fraza z `z` i narzędnikiem tego nie daje i przykładu z niej tu nie ma.
`Widzę człowieka z lornetką.` jest kalką ze zdania angielskiego,
bo polskie `z` wyraża towarzyszenie, a nie narzędzie —
narzędziem widzenia jest `przez lornetkę` — więc czytelnik ma tam jedno czytanie,
a dwa, które olski nad tym zdaniem melduje, są nadprodukcją gramatyki
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)),
czyli klasą, którą trzyma
[open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma).
Świadek postawiony na takim zdaniu pokazuje mechanizm i nie pokazuje pożytku,
bo wskazuje czytanie, które polszczyzna wybrała już bez niego.

Sąsiedztwem jest akapit, a granicę tę bierzemy stąd, skąd bierze ją druga strona:
skład opuszcza podmiot wtedy, gdy o rzeczy była mowa w zdaniu obok,
a akapit jest tym, w czym „obok” się kończy
([kategorie-zapisu.md](kategorie-zapisu.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)).
Czyta się je wstecz, bo czytelnik idzie od początku do końca,
i lematami, bo `w systemach` i `w systemie` są tą samą frazą o tej samej rzeczy.
Pytanie idzie przy tym o to, co stało przed frazą, a nie o część mowy,
więc gospodarza czasownikowego ten świadek wskazuje tą samą drogą,
kiedy fraza stała wcześniej przy tym samym czasowniku.

Tą samą frazą są przy tym formy o jednym lemacie imiennym, a nie o jednym lemacie.
Morfeusz sprowadza do czasownika i odsłownik, i imiesłów przymiotnikowy,
więc bez tego warunku `żądań` i `żądającym` znaczą dla świadka jedno słowo
i zdanie o żądającym dowodzi czegoś o żądaniach.
Odsłownik zostaje, bo jest rzeczownikiem,
czyli kryterium jest częścią mowy w tagu, a nie samym lematem.
Gospodarza to zawężenie nie obejmuje, i rozmyślnie,
bo gospodarzem bywa czasownik:
`jest przetwarzany w Systemie RIT` dowodzi o gospodarzu `przetwarzania`
przez to samo zlanie, które po stronie frazy myli.

Jednego lematu to dopasowanie nie bierze: kopuli.
Okolicznik przyłącza się do `być` w dowolnym zdaniu,
więc dwa zdania o wspólnym lemacie `być` mają wspólne tylko orzeczenie,
a nie miejsce, do którego fraza doszła.
Bez tego warunku `Zabronione jest tworzenie opisów w 1 osobie.` dostaje gospodarza `jest`
po zdaniu `Wymaga się, aby opisy tworzone były w 3 osobie liczby pojedynczej`,
choć fraza dochodzi w nim do `tworzenie opisów`.
Lematy bierzemy z listy, którą gramatyka ma dla orzecznika
(`KOPULA` w `olski/walencja.py`), zamiast pisać drugą o tym samym.
Cenę całej listy wypisuje sonda niżej, a `być` odpowiada nad tym korpusem za nią całą;
czy pozostałe lematy do tego kryterium należą,
pyta wpis w `todo/`.

Warunek dotyczy dowodu, a nie pozycji.
Kopula zostaje gospodarzem, bo okolicznik całego zdania przyłącza się do orzeczenia,
a orzeczeniem jest w takim zdaniu właśnie ona:
`w 1 osobie` czyta się i jako warunek całego zakazu, nie tylko samych opisów.
Warstwa ma więc nad taką pozycją milczeć, a nie przestać jej widzieć.
Odpada przy tym sam dowód, więc kopula obok drugiego dowodu wskazania nie blokuje:
dwóch gospodarzy, przy których świadek milknie, liczy się po odsianiu takich par.

Przy gospodarzu fraza stanęła także wtedy, gdy dzieli je łańcuch imienny.
Sąsiad bezpośredni sam nie wystarcza, bo w łańcuchu dopełniaczowym jest nim ogon grupy:
w `wymiany danych z systemami zewnętrznymi` fraza dochodzi do `wymiany`, a nie do `danych`.
Łańcuch urywa pierwsza forma bez czytania imiennego,
więc w `nadawanie i funkcjonowanie uprawnień do przeglądania` spójnik odcina `nadawanie`.
Dwóch gospodarzy w jednym łańcuchu kończy się milczeniem,
tym samym warunkiem, którym kończy się fraza powtórzona przy obu:
sąsiedztwo powtarza wtedy sporne przyłączenie, zamiast je rozstrzygać.

**Nad rejestrem, o który chodzi, świadek ten odpowiada rzadziej niż o jednej pozycji na sto.**
`harness/powtórzenie.py` przechodzi prozę zdanie po zdaniu
i pyta go o każdą pozycję przyłączeniową, jaką morfologia w tym zdaniu widzi,
a obok zasięgu reguły wypuszczanej liczy zasięg każdego wariantu wycenianego niżej.
Korpusem jest [korpus audytowy](audit-corpus.md#the-list),
czyli dokumentacja techniczna wyekstrahowana do prozy ([extraction.md](extraction.md)):

```sh
python3 -m harness.powtórzenie proza/
```

Pozycje wyznacza morfologia, a nie werdykt, i to jest cała różnica między tym pytaniem
a tym, które warstwa dostaje w `olski-check`.
Gramatyka odrzuca w tym rejestrze prawie każde zdanie,
więc werdykty stawiają tu kilkadziesiąt wyborów na blisko trzy tysiące zdań,
a `olski-check --rozstrzygaj` wypisuje pod nimi garść wskazań, wszystkie skłonności.
Świadek kontekstowy nad tą populacją nie odzywa się ani razu,
i jego zero jest tam w większości liczbą o gramatyce:
żaden świadek nie odpowie częściej, niż jest pytany.
Pozycja znaleziona morfologią stoi tam, gdzie polszczyzna daje dwa czytania,
niezależnie od tego, czy olski to zdanie rozbiera,
i jest tym pytaniem, które warstwa dostanie, kiedy gramatyka po nią sięgnie
(`pytania` w `harness/wieloznaczność.py`).
Populacja jest przez to ta sama, którą ma
[wzorzec czytany ręką](#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów),
więc zasięg zmierzony tutaj i trafność zmierzona tam mówią o jednych pytaniach.

Zasięg ten ma dwa mianowniki i tylko drugi z nich jest o świadku.

Pierwszy jest o rejestrze: cztery piąte jego zdań stoi pierwsze w swoim akapicie,
więc świadek nie ma tam czego przeczytać.
Zdań pierwszych jest przy tym tyle, ile akapitów,
bo każdy akapit ma zdanie pierwsze i żaden nie stoi bez zdania,
czyli akapit tego korpusu jest niewiele dłuższy od zdania.
Długość ta bierze się z tego, co ekstrakcja liczy za akapit,
a liczy za niego osobno każdą pozycję listy,
bo zdanie nie biegnie z jednej do następnej
([extraction.md](extraction.md)).
Ile z tych akapitów wyszło właśnie z list, nie mówi ani ten przebieg, ani żaden inny,
bo ekstrakcja nie wypuszcza typu węzła, z którego akapit powstał;
tego samego braku dotyczy wpis w `todo/`
o mapowaniu trafień z powrotem na konstrukcje.

Drugi jest o świadku: fraza powtarza się przy gospodarzu
rzadziej niż raz na czterdzieści pozycji,
które mają w akapicie co przeczytać.

**Siedem odpowiedzi w granicy akapitu przeczytano i wszystkie wskazują dobrze.**
Dowód pod każdą jest tego samego kształtu, czyli frazą powtórzoną przy gospodarzu:
`prawem do dalszego przekazywania` po zdaniu z `bez prawa do dalszego przekazywania`.

**Warunek na kopulę wyceniono: zdejmuje jedno wskazanie i jest nim pomyłka.**
Wariant sondy podaje świadkowi pustą listę kopul, czyli bierze za dowód i powtórzenie
przy `być`, i wtedy odpowiada raz więcej.
Tym jednym wskazaniem jest opisane wyżej `w 1 osobie` → `jest`,
więc warunek kupuje zdjęcie jednej pomyłki,
a kosztuje nad tym korpusem zero wskazań dobrych.

**Granicę akapitu wyceniono: kupuje wielokrotnie więcej odpowiedzi i dwie odbiera.**
Wariant sondy podaje świadkowi cały dokument czytany wstecz zamiast akapitu,
a dwie z tamtych siedmiu wtedy milkną.
Milkną dlatego, że dalej w dokumencie ta sama fraza stoi przy drugim gospodarzu,
a dwóch gospodarzy kończy się milczeniem —
i są to `nowa faktura z datą PermanentStorage`
oraz `uprawnień pracownikom do przeglądania`, czyli dwa wskazania dobre.

Zakup ten jest zasięgiem i o trafności nie mówi nic sam z siebie.
Dziesięć odpowiedzi rozrzuconych po tych spoza akapitu (`rozrzucona` w `harness/próbka.py`)
czyta się jako sześć wskazań dobrych i cztery słabsze,
a pomyłki co do strony wyboru nie ma wśród nich żadnej:
`atrybutów posiadanych przez obiekt w systemie źródłowym` dostaje `obiekt`,
a `przekazanie danych o obiektach turystycznych` dostaje `danych`.
Jedno ze słabszych nazywa grupę jej przymiotnikiem, a nie głową:
`wyrażenia regularne dla adresów IP` dostaje `regularne`,
bo łańcuch imienny urywa się na przymiotniku i `wyrażenia` gospodarzem nie zostaje.
Drugie stoi na pozycji, która przyłączeniem nie jest,
bo Morfeusz czyta jako przyimek samotną literę `A` z nazwy podmiotu.
Trzecie trafia w gospodarza, a pozycji pod nim nie ma:
`kontekst w ktorym jestesmy uwierzytelnieni` dostaje `kontekst`,
tyle że `w którym` otwiera zdanie względne, a nie wyrażenie przyimkowe.
Czwarte stoi tam, gdzie obaj gospodarze mówią to samo:
w `nie przesłano żadnych faktur w sesji interaktywnej` fraza nazywa tę samą sesję,
dojdzie do `faktur` czy do `przesłano`.
Granica broni się więc nie tym, że wskazania spoza niej są złe,
tylko tym, po co ją tam postawiono ([sklad.md](sklad.md)),
a policzone jest i to, co jej zdjęcie kupuje, i to, co odbiera.

**Regułę kandydata wyceniono tą samą drogą, a węższa dokłada pomyłkę na łańcuchu.**
Wariant węższy pyta o samego sąsiada frazy i odpowiada częściej od wypuszczanego,
a różnica bierze się stąd, że łańcuch pokazuje czasem dwóch gospodarzy naraz,
a dwóch kończy się milczeniem.
Kupuje to pomyłkę, którą łańcuch omija:
`Wpływa to na sposób wymiany danych z systemem RIT.` dostaje gospodarza `danych`,
gdzie fraza dochodzi do `wymiany`.
Dowodem jest tam `wymiany danych z systemami zewnętrznymi`, czyli ten sam łańcuch,
więc powtórzenie jest prawdziwe, a odczytane z niego wskazanie nie.
Reguła wypuszczana widzi w tym łańcuchu obu gospodarzy naraz i o tym zdaniu milczy.

Wariant szerszy pyta o cały prefiks zdania i odpowiada rzadziej od obu.
Kandydatów ma najwięcej i dlatego najczęściej trafia na dwóch naraz,
więc reguła szersza od wypuszczanej kupuje mniej zasięgu, a nie więcej.
Kupuje za to gospodarza stojącego daleko przed frazą, którego łańcuch nie sięga,
i bywa nim czasownik żądający tej frazy swoim schematem:
w `Rozszerzono model żądania o właściwość boolean onlyMetadata`
wskazuje `Rozszerzono`, czyli ramę `rozszerzyć coś o coś`.
Jest to ten sam dowód, którego świadek ramowy nie wypuszcza jako wskazania:
po stronie czasownika bierze go za weto, i dlaczego, mówi
[sekcja o ramie](#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie).

Częstości pomyłek ten przebieg wobec tego nie podaje.
Siedemnaście odpowiedzi przeczytanych jest odczytem, a nie stopą,
a materiał, na którym dałoby się ją policzyć, jest dwojaki:
[wzorzec po drugiej stronie](disambiguation.md#wzorzec-na-tę-warstwę-jest-po-drugiej-stronie),
którego nie ma, oraz
[wybory przeczytane ręką](#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów),
których jest trzydzieści.

**Świadek statystyczny liczy bank drzew i nazywa własną częstość pomyłek.**
`Skłonność` liczy, jak często ta para przyimka i gospodarza
przyłączała się w banku drzew w tę stronę,
i odpowiada dopiero powyżej progu wsparcia i progu przewagi.
Tabelę buduje się i ocenia z tego samego korpusu:

```sh
python3 -m harness.skłonności Składnica-frazowa-180723/ --oceń
python3 -m harness.skłonności Składnica-frazowa-180723/ --zbuduj --wsparcie 2
```

Tabela zbudowana tą komendą podlega warunkom banku drzew, czyli GPL v3,
i tak jest zadeklarowana ([README.md](../README.md#licencja)).

Ocena buduje tabelę na połowie banku drzew i sprawdza ją na drugiej,
dzieląc po parzystości numeru pliku, żeby ta sama komenda dwa razy dała tę samą liczbę.
Nad 2 000 wyborami z połowy, której świadek nie widział:

| wsparcie | próg | odpowiada w | trafia w |
| --- | --- | --- | --- |
| — | — | 100,0% | 66,8% |
| 2 | 70% | 13,4% | 89,9% |
| 2 | 85% | 12,8% | 89,5% |
| 3 | 85% | 7,3% | 89,8% |
| 5 | 85% | 3,0% | 96,7% |
| 5 | 95% | 2,3% | 97,8% |

Pierwszy wiersz jest podłogą, czyli regułą „zawsze do rzeczownika”,
tą samą, którą [subset.md](subset.md#dlatego-olski-przyjmuje-koszt) odrzuciła jako konwencję.
Ustawieniem domyślnym jest wsparcie 2 i próg 85%,
czyli świadek odpowiada o jednym wyrażeniu na osiem i myli się w co dziesiątej odpowiedzi.

Cztery rzeczy o tej tabeli trzymają się razem i osobno każda z nich myli.

Trafność jest wysoka, a zasięg mały, i jest to ta sama liczba wzięta dwa razy:
świadek odpowiada tam, gdzie bank drzew ma parę policzoną,
a par jest tyle, ile ich korpus tej wielkości daje.

Trafność 89,5% nie jest trafnością zadania, tylko trafnością na wybranej ósmej części,
a najlepszy zmierzony model przyłączenia sięga 86,7% przy zasięgu pełnym,
i to on jest liczbą do pobicia, a nie podłoga.

Tabela oceniana nie jest tabelą wypuszczaną.
Ocena buduje swoją z połowy korpusu, żeby mierzyć na materiale nieoglądanym,
a `olski/skłonności.txt` powstaje z całości i ma 998 par,
więc wiersze wyżej są dla niej oszacowaniem od dołu co do zasięgu
i nie są pomiarem jej trafności wcale.
Zmierzyć ją mógłby dopiero korpus, którego ta tabela nie widziała,
a takiego drugiego banku drzew dla polszczyzny ten przegląd nie zna.

Rejestr się przy tym nie zgadza: bank drzew jest prozą literacką i prasową,
a olski celuje w dokumentację techniczną,
więc skłonność wzięta stąd jest punktem wyjścia, a nie pomiarem rejestru, o który chodzi.

Dowód tego świadka jest przy tym tego samego rodzaju co dowód
[rankingu](disambiguation.md#ranking-nie-jest-wyjściem-którego-ten-parser-potrzebuje):
częstość wyuczona z banku drzew, pytana o jedno przyłączenie zamiast o całe drzewo.
Zarzut z tamtej sekcji go nie dosięga, bo werdyktu nie rusza,
a [kryterium powodu](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza) dosięga:
odpowiada częstością nad korpusem, którego autor zdania nie czyta.
Jest tu wobec tego jedną z dwóch stron pomiaru, który tamtą hipotezę obala albo zostawia,
a nie świadkiem, którego ta warstwa miałaby rozbudowywać.

**Świadek ramowy odpowiada schematem i stoi między tymi dwoma.**
`Rama` pyta `olski/leksykon.txt` o to, czy rama rzeczownika żąda tego przyimka,
i wskazuje go wtedy, gdy rama czasownika go nie żąda,
czyli odpowiada tą częścią klasy, o której
[sekcja o leksykonie](disambiguation.md#leksykon-rozstrzyga-część-i-rozstrzyga-ją-deterministycznie) mówi,
że nie konkuruje z niczym.
Za świadkiem kontekstowym, bo akapit mówi o tym tekście, a leksykon o polszczyźnie,
i przed tabelą, bo dowód słownikowy bije statystyczny.
Co ten świadek kupuje i ile kosztuje jego weto, trzyma
[sekcja o ramie](#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie).

## Rama rozstrzyga po stronie rzeczownika, a po stronie czasownika nie

Świadka ramowego wyceniono przed dopisaniem go, tak jak
[przysłówek](konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy),
i pomiar rozstrzygnął go na pół.
`harness/rama.py` pyta bank drzew, dokąd wyrażenie doszło u anotatora,
i zestawia to z samym kryterium, a nie z werdyktem.
Kryterium jest jedno i ma jednego właściciela — `przyimki` w `harness/walenty.py`,
skąd bierze je i ta sonda, i kolumna leksykonu:
lemat żąda przyimka, gdy któryś jego schemat
ma pozycję niepodmiotową z `prepnp` o tym przyimku.
Odpowiedź pada w tej sondzie wtedy, gdy żąda go dokładnie jedna strona.
Liczby drukuje `python3 -m harness.rama`.

Mianownik jest tam węższy niż mianownik, którym liczy
[sekcja o leksykonie](disambiguation.md#leksykon-rozstrzyga-część-i-rozstrzyga-ją-deterministycznie),
i węższy o jeden warunek.
Tamten obejmuje każde przyłączenie w pozycji dwuznacznej,
a ten bierze same te, które doszły do rzeczownika albo do zdania,
bo tylko o takich świadek ma co powiedzieć:
kilkaset przyłączeń dochodzi do trzeciej kategorii — `fwe`, `fpt`, `fpm`, `fps` —
i wzorca dla wyboru dwóch stron nie dają.
`Report` w `harness/attachment.py` liczy tak samo w swoim rozkładzie po przyimku,
więc oba mianowniki są tam obok siebie.

Rama odpowiada nad dwiema piątymi spornych przyłączeń
i trafia w niespełna dwie trzecie odpowiedzi.
Sama ta para mówi, że świadka takiego brać nie warto:
[kolejność lasu](disambiguation.md#nad-składnicą-olski-ma-ranking-którego-nikt-nie-trenował)
trafia bez żadnego słownika tyle samo albo więcej.

Rozstrzyga jednak strona, a nie średnia.
Rama rzeczownika myli się rzadziej niż raz na dwadzieścia odpowiedzi,
czyli rzadziej niż tabela skłonności przy zasięgu tej samej wielkości.
Rama czasownika trafia tyle, ile rzut monetą nad wyborem dwóch stron,
a odpowiedzi wydaje dwa razy więcej niż tamta.
Średnia z obu jest przez to liczbą o niczym:
opisuje mieszaninę świadka i szumu w proporcji, którą ustala korpus.

Powód widać po tym, co bank drzew mówi o tych samych odpowiedziach.
Tam, gdzie anotator postawił nad wyrażeniem frazę — wymaganą albo luźną —
kryterium trafia w dziewięciu wypadkach na dziesięć, po obu stronach naraz.
Tam, gdzie nie postawił żadnej, trafia w połowie,
a takich odpowiedzi jest większość i prawie wszystkie padają po stronie czasownika.
Znaczy to, że kryterium myli się nie na ramie, tylko na jej braku:
czasownik żąda przyimków tak licznie, że jego schemat pasuje do okolicznika,
o którym nie mówi nic.
Widać to na lematach, które padają w pomyłkach — `być` z `na`, `być` z `z`,
`mieć` z `w`, `powodować` z `w` —
czyli na tej samej klasie, przed którą warstwa rozstrzygająca broni się już
listą kopul odejmowaną od dowodu w `olski/rozstrzyganie.py`.

Zwężenie do schematów o kwalifikatorze `pewny` tego nie naprawia i nie stoi.
Pod `--tylko-pewne` żadna z tych liczb nie rusza się o więcej niż pół punktu,
czyli pewność nie odróżnia ramy od okolicznika.
Zwężeniem, które by to zrobiło, jest przypadek grupy pod przyimkiem:
Walenty pisze `prepnp(o,loc)` obok `prepnp(o,acc)`,
a `Attachment` w `harness/attachment.py` niesie sam przyimek,
więc żaden przebieg tej sondy dziś tego nie pyta.

Świadek, który z tego wyszedł, bierze z kryterium połowę:
`Rama` w `olski/rozstrzyganie.py` wskazuje po stronie rzeczownika,
a po stronie czasownika nie wskazuje nikogo.
Wyceniono to tak samo jak przysłówek, czyli połowa na gospodarza,
a rozstrzygnęło się inaczej: tam obie połowy weszły,
bo druga kupowała prawdę o drzewie
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy)),
a tutaj druga nie ma czym odpowiedzieć.
Wypada to zgodnie z próbą nad rejestrem, wziętą nad innym korpusem i inną ręką:
tam też rozstrzyga rama rzeczownika, i to w większości tych odpowiedzi,
które w ogóle rozstrzyga jakakolwiek rama
([częstość nad dokumentacją](#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania)).
Dwa korpusy mówią więc to samo o tej samej połowie.

**Nad połową banku drzew, której świadek nie widział, rama rzeczownika
dorównuje tabeli skłonności zasięgiem i bije ją trafnością.**
Odpowiada na mniej więcej co ósme sporne wyrażenie, czyli tyle, co tabela,
i myli się rzadziej niż raz na dwadzieścia odpowiedzi tam,
gdzie tabela myli się w co dziesiątej.
Jedna z tych dwóch liczb kupuje się zwykle drugą — o tym mówi krzywa progów
w tym samym wydruku — a tutaj się nie kupuje, bo świadek progu nie ma:
odpowiada wtedy i tylko wtedy, gdy słownik żąda po jednej stronie.
Rama stoi przed tabelą — dowód słownikowy bije statystyczny — i tabela odzywa się
po niej tylko tam, gdzie rama milczy, więc obaj razem odpowiadają na mniej więcej
co piąte sporne wyrażenie przy niższej stopie pomyłek, niż ma sama tabela.
Kolejność ta nie jest przy tym porównaniem dwóch trafności, tylko
[hipotezą](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza),
i z niej wynika też, czego rama nie bije: świadek kontekstowy stoi przed nią,
bo akapit mówi o tym tekście, a leksykon o polszczyźnie.
Wszystkie te liczby drukuje `python3 -m harness.skłonności <korpus> --oceń`,
bo ten przebieg mierzy warstwę, a nie kryterium nad samym Walentym.

**Rama czasownika zostaje za to wetem, a weto kosztuje zasięg.**
Świadek milczy, gdy przyimka żąda także czasownik,
i milczy z tego samego powodu, z którego nie wskazuje czasownika:
tam, gdzie żąda go i rzeczownik, i czasownik, schematu nie łamie żadne czytanie.
Cenę weta wypisuje wariant, a nie różnica między commitami,
a wypada ona dwa razy inaczej, bo świadek i warstwa tracą co innego.
Sama rama odpowiada bez weta blisko dwa razy częściej
i myli się wtedy w co trzynastej odpowiedzi zamiast rzadziej niż w co dwudziestej.
Warstwa traci mniej, bo część tego, co weto zdejmuje, podejmuje tabela za ramą:
bez weta odpowiada ona na przeszło co czwarte sporne wyrażenie zamiast na co piąte,
a myli się w co dziesiątej odpowiedzi zamiast w co trzynastej.

Weto nie jest więc darmowe, a rozstrzyga o nim to, czym ma być wskazanie.
Rama bez weta wskazuje rzeczownik także tam, gdzie tego samego przyimka
żąda również rama czasownika, czyli tam, gdzie żadne z dwóch czytań schematu
nie łamie, a wtedy powód mówi o jednej stronie i milczy o drugiej.
Wskazanie bez powodu jest u tej warstwy rankingiem, a rankingu
[wywód o cenie](disambiguation.md#ranking-nie-jest-wyjściem-którego-ten-parser-potrzebuje) tu nie chce.
Warstwa bez weta wraca zarazem do stopy pomyłek tabeli,
czyli rama przestaje być tym dowodem lepszym, dla którego stoi przed nią.

Czego ten pomiar nie mówi, to ile zdań to zdejmuje.
Mianownikiem jest tu wyrażenie, a pomiar zdań ma mianownik własny,
i jedno zdanie niesie takich wyrażeń czasem kilka,
więc złożenie dwóch mianowników zostaje tam, gdzie było.

Nie mówi też, ile świadek odpowiada nad rejestrem docelowym.
Zasięg ogranicza mu bowiem nie kryterium, tylko słownik:
plik rzeczownikowy Walentego wylicza dwa tysiące lematów,
więc rzeczownik spoza tej listy jest dla świadka rzeczownikiem bez ramy,
a nie rzeczownikiem, którego rama tej pozycji nie ma.

## Werdykt pyta warstwę o inny wybór niż bank drzew

Ocena wyżej mierzy świadka na czwórkach lematów wziętych z banku drzew,
a warstwę wypuszczaną pyta `olski-check` i pyta ją czym innym.
Pytaniem jest `Przyłączenie` z werdyktu:
gospodarze są formami, a nie lematami anotatora,
form tych bywa więcej niż dwie,
i lemat wybiera dopiero Morfeusz, wybierając ich kilka naraz.
Drogę drugą mierzy `harness/wskazania.py`, pytając o wzorzec drzewo wzorcowe:

```sh
python3 -m harness.wskazania Składnica-frazowa-180723/
```

Trzy rzeczy tego przebiegu trzymają się razem i osobno każda z nich myli.

Zasięg warstwy wypuszczanej wychodzi wyższy niż w ocenie wyżej,
bo tabela wypuszczana ma pary z całej Składnicy zamiast tych z jej połowy,
a lematów formy pyta się naraz kilku, więc para znajduje się częściej.
Populacja jest przy tym inna — przyłączenia liczone tutaj to te,
przed którymi wybór postawił olski,
a nie te, przed którymi postawił go anotator —
więc dwóch zasięgów nie odejmuje się od siebie.

Trafność tego przebiegu jest mierzona na materiale, który ta tabela widziała.
`olski/skłonności.txt` powstaje z całej Składnicy, a przebieg idzie po całej Składnicy,
więc liczba ta jest górnym oszacowaniem i pomiarem trafności nie jest.
Trafnością poza próbą jest ta z oceny wyżej, o kilka punktów niższa,
a przebieg dzielący korpus tak, jak dzieli go tamta, trzyma `todo/`.

Gospodarzy jest więcej niż dwóch w co czwartym przyłączeniu,
czyli w tylu wypadkach ocena z czwórek mierzy wybór łatwiejszy niż ten,
przed którym warstwa staje.
Wypadki te biorą się z produkcji, a nie z rzadkości:
`Obudziłem się na podłodze w kuchni z pustą paczką po ciasteczkach w dłoniach.`
ma cztery przyłączenia, a każde następne dostaje za gospodarza rzeczownik z poprzedniego.

Wzorca nie ma dla ponad ćwierci przyłączeń i nie jest to milczenie banku drzew.
Drzewo albo nawiasuje tę frazę inaczej, niż nazywa ją werdykt,
albo przyłącza ją do czegoś, co nie jest ani grupą imienną, ani zdaniem.
Drugie ma dwie kategorie i obie wypadają z tego samego powodu.
`Auta są kradzione dla okupu.` przyłącza frazę do imiesłowu,
a `Muszę jechać do domu.` do frazy werbalnej z bezokolicznikiem,
czyli dokładnie tam, gdzie stawia ją werdykt:
odpowiedź anotatora jest tu zgodna i mimo to nie liczy się jako wzorzec,
bo `CLAUSE` w `harness/attachment.py` tej kategorii nie wylicza.
Złączenie idzie formami modyfikatora, bo tyle mają obie strony:
werdykt rozpiętości nie niesie.

## Wzorzec dla rejestru czyta się ręką i jest go trzydzieści wyborów

Bank drzew jest zbiorem zdań stojących osobno,
więc świadek kontekstowy nie ma nad nim czego przeczytać
i w tabeli wyżej nie odzywa się ani razu.
Nad korpusem audytowym jest odwrotnie: tekst jest ciągły, a wzorca nie ma tam żadnego.
`próba/wybory.txt` dokłada ten wzorzec i jest jedynym miejscem w tym repozytorium,
w którym sąd o zdaniu pochodzi z przeczytania, a nie z cudzego korpusu ani z przebiegu.
O kolejność czytań pyta ten sam plik `harness/kolejność.py`
([disambiguation.md](disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie)),
więc przerysowanie którejś z prób rusza dwie liczby, a nie jedną.

Zdania są przy tym cudze, a nasz jest sam sąd.
Zdanie wymyślone pod świadka mierzy autora, a nie rejestr,
więc pozycje bierze się z [korpusu audytowego](audit-corpus.md#the-list) takie, jakie tam stoją,
i losuje spośród wszystkich, a jest ich w tym korpusie ponad tysiąc
(`rozrzucona` w `harness/próbka.py`).
Wyznacza je morfologia, a nie werdykt (`pytania` w `harness/wieloznaczność.py`),
bo werdykty stawiają nad tym rejestrem 49 wyborów na 2 915 zdań
i nie ma czego z nich losować.
Jest to ta sama populacja, którą liczy
[pomiar zasięgu](#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek),
i to on jest jej właścicielem, bo drukuje ją obok swojego polecenia.
Ręką dopisuje się gospodarza wraz z powodem,
a poprawia się przy tym frazę i gospodarzy:
budowniczy proponuje frazę przyimkiem wraz z trzema formami za nim,
więc sięga nią dalej, niż ona idzie,
a gospodarzy proponuje całym łańcuchem imiennym,
który homonimia przedłuża czasem przez orzeczenie.

```sh
python3 -m harness.wybory próba/wybory.txt
```

Wzorzec ma dwie odpowiedzi poza samymi gospodarzami i obie są tu po to,
żeby milczenie warstwy dało się ocenić.
`oba` znaczy, że tekst nie rozstrzyga i czytelnik też nie:
`Numer nadawany jest podczas przetwarzania faktury po stronie KSeF.`
mówi to samo, dokądkolwiek ta fraza dojdzie, bo przetwarzanie i nadanie numeru
dzieją się w jednym miejscu.
Jest to ta sama klasa, którą
[tożsamość czytania](disambiguation.md#tożsamość-czytania-jest-tańsza-i-częściowo-już-stoi)
wycenia na trzecią część błędów najlepszego modelu przyłączenia.
`żadne` znaczy, że wyboru nie ma wcale,
bo pozycja znaleziona morfologicznie nie jest przyłączeniem:
`takich jak /auth/challenge` jest porównaniem, a nie wyrażeniem przyimkowym,
i trzy z trzydziestu wyborów są tego rodzaju.

**Świadek kontekstowy odzywa się tu dwa razy i dwa razy trafia.**
Jest to jedyne miejsce, w którym jego wskazanie stoi obok wzorca:
[pomiar zasięgu](#zalążek-odpowiada-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek)
pyta go o te same pozycje i wzorca do nich nie ma, więc czyta swoje odpowiedzi ręką.
Oba dowody są tego samego kształtu, czyli frazą powtórzoną przy gospodarzu:
`z prawem do dalszego przekazywania` po zdaniu z `bez prawa do dalszego przekazywania`,
oraz `uprawnień pracownikom do przeglądania` po zdaniu z `uprawnień do przeglądania`.
Drugi z nich jest tym, czego tabela skłonności nie umie:
fraza dochodzi tam do rzeczownika oddzielonego od niej celownikiem,
a bank drzew o takim szyku nie mówi nic.

Blisko dwie trzecie wyborów zostaje nierozstrzygniętych
i to jest właściwa liczba tej próby.
Warstwa nie myli się nad nią ani razu, co pilnuje `tests/test_wybory.py`,
i nie jest to zasługa progów, tylko ich ceny:
milczenie jest tu odpowiedzią w kilkunastu wypadkach na trzydzieści.
Trzydzieści wyborów wystarcza, żeby powiedzieć, że warstwa milczy częściej, niż odpowiada,
i nie wystarcza, żeby powiedzieć, jak często się myli;
tę drugą liczbę bierze [próba zawężona do odpowiedzi](#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania).

Losowanie padło przy tym nad populacją mniejszą od dzisiejszej:
`pytania` dawało wtedy 1 058 pozycji, a gospodarza proponowało ogonem łańcucha
imiennego, gdzie dzisiejsze daje 1 126 pozycji i głowę grupy.
Ta sama komenda puszczona teraz z `--ile 30` dzieli z tym plikiem dwa zdania z trzydziestu,
więc powiększenie próby jest przerysowaniem siatki, a nie dopisaniem wpisów do niej;
co z tym zrobić, pyta wpis w `todo/`.
Sądów tych to nie unieważnia, bo każdy stoi przy zdaniu i przy frazie wypisanych w całości,
a gospodarzy poprawiła ręka.

## Częstość nad dokumentacją myli się tam, gdzie nie rozstrzyga żadne słowo zdania

Próba wyżej losuje spośród wszystkich pozycji rejestru,
więc mówi, jak często warstwa odpowiada, a nie mówi, jak często się myli:
odpowiedzi pada w niej pięć i jedna pomyłka przesuwałaby stopę o dwadzieścia punktów.
Częstość pomyłek żąda mianownika, którym jest odpowiedź, a nie pozycja,
a taki mianownik daje losowanie zawężone do tych pozycji, nad którymi warstwa się odzywa:
odzywa się nad 212 z 1 126 pozycji korpusu audytowego, czyli nad co piątą,
i spośród nich losuje się trzydzieści (`z_odpowiedzią` w `harness/wybory.py`).
`próba/wybory-z-odpowiedzią.txt` jest tym losowaniem przeczytanym ręką
i jest osobnym plikiem, a nie częścią próby wyżej,
bo jeden wydruk z dwoma mianownikami czyta się jako jeden.

Wpisy pochodzą z losowania ze 123 pozycji, bo tyle warstwa dawała odpowiedzi wtedy,
kiedy dawała je sama tabela częstości;
jedną z tych 123 było wskazanie świadka kontekstowego,
odebrane wraz z dowodem z kopuli, i próby to nie przerysowuje.
Wpisy te były odpowiedziami tabeli częstości w chwili losowania,
a dziś ponad połowę z nich oddaje świadek ramowy,
bo stoi przed tabelą i bierze wybór tam, gdzie rama rzeczownika go rozstrzyga.
Przerysowania żąda ta próba przez to już teraz:
mierzy dwóch świadków w proporcji, której nikt nie wylosował,
a co z tym zrobić, pyta wpis w `todo/`.

```sh
python3 -m harness.wybory próba/wybory-z-odpowiedzią.txt
```

Świadek kontekstowy nie odpowiada tu ani razu i mówi to o losowaniu, a nie o świadku:
odzywa się nad tym korpusem siedem razy, więc trzydzieści wylosowanych pozycji
nie musi trafić w ani jedną z nich i nie trafiło w żadną.
Ta próba mierzy przez to nad dokumentacją świadka ramowego i tabelę częstości razem,
a więcej wskazań ma rama.
Wpisów jest trzydzieści, a odpowiedzi 29, i różnica ta jest ceną poprawiania ręką:
zawężenie pyta o frazę i gospodarzy, jakich proponuje morfologia,
a przy jednym wpisie gospodarz okazał się jeden, bo drugim był spójnik.

**Pięć pomyłek na 29 odpowiedzi nie odróżnia tego rejestru od banku drzew.**
Tabela częstości mierzona na połowie banku drzew, której nie widziała,
myli się w co dziesiątej odpowiedzi (`WSPARCIE` i `PRÓG` w `olski/rozstrzyganie.py`),
a stopa taka daje pięć pomyłek albo więcej na 29 odpowiedziach raz na sześć przebiegów.
Stopa tych 29 jest przy tym stopą dwóch świadków razem, a tamta jednego,
więc zestawienie mówi mniej, niż mówiło, gdy odpowiadała sama tabela.
Druga połowa [hipotezy](disambiguation.md#dobre-ujednoznacznianie-jest-odczytaniem-i-jest-to-hipoteza)
żąda pomyłek częstszych niż tam, więc ta próba jej nie obala i nie potwierdza;
ile odpowiedzi trzeba, żeby odróżniła, mówi wpis w `todo/`.

**Rozstrzyga natomiast, gdzie warstwa nad tym rejestrem odpowiada dobrze.**
Wpisy dzielą się na dwoje po tym, czy wybór rozstrzyga któreś słowo tego zdania.
Podział ten przeczytała ta sama ręka, która wpisała wzorce, i przy wydruku odpowiedzi
przed sobą, więc sprawdza się go po polach `powód`, a nie po liczbie pod nim.
Powód taki niosą 23 odpowiedzi: 19 rozstrzyga rama rzeczownika
(`informacja o czymś`, `dostęp do czegoś`, `prawo do czegoś`, `wniosek o coś`),
3 dopełnienie cząstkowe liczebnika (`posiadanie jednego z kilku uprawnień`),
a jedną wyrażenie stałe `w zależności od`.
Nad żadną z tych 23 warstwa się nie myli.
Zostaje 6 odpowiedzi, w których żadne słowo zdania wyboru nie rozstrzyga,
i nad nimi warstwa myli się pięć razy.
Szósta jest trafna i pokazuje, jak wąska jest granica tego podziału:
w `wypróbować kontakty z kolejnych jej pozycji` fraza wskazuje źródło,
a świadek ramowy wskazuje `kontakty`, bo `z` jest pozycją ramy „kontakt”,
której to zdanie nie realizuje.
Powód mija się więc z relacją i mimo to wypada na właściwego gospodarza.

Trzy z tych pięciu są konstrukcjami rejestru.
`Data i czas wystąpienia błędu w UTC.` podaje strefę, w której wypisano czas,
a warstwa dołącza `w UTC` do `błędu`, bo `w` jest pozycją ramy „błąd”.
`natychmiastowej rejestracji dokumentu w KSeF` mówi, gdzie zachodzi rejestracja,
a tabela dołącza frazę do dokumentu.
`W czasie przekazywania danych do systemu RIT` ma `w czasie` za ramę czasową,
a tabela bierze `czas` za gospodarza `do systemu RIT`.
Dwie pozostałe padają nad wpisami, nad którymi trafną odpowiedzią jest milczenie:
`zapewnienie równych warunków dostępu dla wszystkich użytkowników`
i `mają zastosowanie w kontekście fakturowania` mówią to samo, dokądkolwiek fraza dojdzie,
więc tabela odpowiada tam, gdzie nie ma na co.

Ten sam podział widać po wsparciu pary, którą tabela zacytowała.
Odpowiedzi opartych na dwóch wypadkach banku drzew, czyli na najniższym wsparciu,
jakie przechodzi próg, jest 7 i cztery z nich są pomyłkami;
z 22 opartych na trzech wypadkach albo więcej pomyłką jest jedna.
Trzy trafne spod wsparcia dwóch to trzy pozycje z liczebnikiem cząstkowym,
czyli klasa, którą rozstrzyga reguła, a nie częstość.
Wsparcie podniesione o jeden zdjęłoby więc nad tą próbą cztery pomyłki z pięciu
i trzy odpowiedzi z 29, a cenę po stronie banku drzew wypisuje `--oceń`;
ruch ten trzyma wpis w `todo/`.

Wniosek tej próby mówi więc, co ta tabela nad tym rejestrem robiła:
w 23 odpowiedziach z 29 zastępowała leksykon, a poza nimi myliła się pięć razy na sześć.
Cena świadka ramowego jest tym policzona po stronie rejestru, a nie tylko banku drzew,
i to ona rozstrzygnęła, że świadek wchodzi po stronie rzeczownika.
Sama próba jest przy tym starsza od niego: wpisy padły wtedy, gdy tabela
odpowiadała pierwsza, więc część tych 23 odpowiedzi wydaje teraz rama,
i tego ta próba nie mierzy; `todo/` trzyma wpis o jej ponownym odczycie.

## Sources

- <https://aclanthology.org/E17-2050/> —
  de Kok, Ma, Dima i Hinrichs, *PP Attachment: Where do We Stand?*, EACL 2017,
  skąd 86,7% najlepszego modelu przyłączenia przy zasięgu pełnym
