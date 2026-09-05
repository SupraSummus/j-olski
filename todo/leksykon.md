# Leksykon i walencja

Leksykon gubi zwrotność, którą Walenty zapisuje pozycją, a nie lematem.
Walenty pisze `spotkać się` jako `spotkać` z pozycją `recip` w schemacie,
a `myć się` jako `myć` z pozycją `refl`, i żadnej z nich `harness/walenty.py` nie czyta,
więc `olski/leksykon.txt` mówi o 5 739 lematach zwrotnych,
a 880 lematów tych schematów nie ma w nim wcale.
Gramatyce nie odbiera to dziś nic, bo klasa domyślna leksykonu zwrotnego
wpuszcza cząstkę i bez wpisu, a odbiera świadkowi ramowemu przyimki tych schematów
(`przyimki_czasownika` w `olski/walencja.py`).
Ruchem jest zdanie leksykonu o cząstce, czytane z obu zapisów naraz,
a przed nim rozstrzygnięcie, czy pozycja `refl` odbiera ramie biernik:
`się` stoi w niej w miejscu dopełnienia, więc lemat wzięty z ramą domyślną
brałby biernik drugi raz.
Do przeczytania jest, ile ta kolumna zmienia świadkowi:
schematów z tymi pozycjami jest 2 407, a lematów 1 464.

Sprawdzian leksykonu jest skryptem pisanym od nowa przy każdej zmianie.
[Liczba, na której leksykon stoi](../docs/walencja.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)
— 615 z 616 lematów potwierdzonych bankiem drzew — bierze się ręcznie,
bo `_slot_role` w `harness/corpus.py` czyta z pola `tfw` dwie role olskiego,
a rama czasownika stoi w tym polu cała.
Ruchem jest zejście po wybranym drzewie do węzłów `zdanie`,
wzięcie lematu głowy i pozycji fraz wymaganych obok niej,
i porównanie tego z `WALENCJA` w `olski/subset/rama.py`.
Do rozstrzygnięcia jest, co taki przebieg drukuje:
sama niezgodność jest liczbą, a pożytek z niej ma dopiero ten,
kto widzi lemat, zdanie i pozycję, o którą poszło.
Do rozstrzygnięcia jest też, czy to jest flaga `harness.pomiar`,
czy komenda obok niej, bo tamta mierzy gramatykę, a ta leksykon.
Zdejmuje to zarazem pytanie, którego dziś nikt nie zadaje po zmianie w
`harness/walenty.py`: czy nowe czytanie Walentego dalej zgadza się z bankiem.

Leksykon walencyjny mówi o bierniku i o bezokoliczniku, a o przypadkach nie mówi.
Narzędnika [przekład](../docs/walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)
nie bierze, bo `inst` jest u olskiego pozycją orzecznika,
a Walenty nie odróżnia jej od argumentu narzędnikowego,
więc kopula zostaje listą pisaną ręcznie w `olski/walencja.py`.
Do przeczytania jest, czy bank drzew tę różnicę widzi:
pozycja `adjp(pred)` stoi w polu `tfw` obok `np(inst)`,
a `harness/corpus.py` czyta dziś z tego pola podmiot i dopełnienie.
Gdyby ją widział, kopula przestaje być listą, a staje się wpisem jak każdy inny,
i wtedy pytaniem jest, ile czasowników poza nią orzecznik w narzędniku bierze.

Zdanie leksykonu o parze przemilcza, które wypełnienie przy celowniku stoi,
więc lemat z parą bierze wszystkie cztery naraz
([`docs/walencja.md`](../docs/walencja.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).
Walenty rozdziela je i mówi to o tysiącach lematów, których rozkład trzyma
tamta sekcja: `pokazywać` ma parę z biernikiem, ze zdaniem i z pytaniem,
a z bezokolicznikiem jej nie ma, więc `Parser pokazuje autorowi zapisać ustawienia.`
wyprowadza się i polszczyzną nie jest.
Ruchem są cztery zdania leksykonu w miejsce jednego,
a wraz z nimi cztery wartości cechy `druga` w `olski/subset/rama.py` zamiast jednej.
Do rozstrzygnięcia jest, czy warto:
rama domyślna daje każdemu czasownikowi te same cztery wypełnienia naraz,
więc para rozdzielona byłaby dokładniejsza od ramy, do której dochodzi,
a klas walencyjnych przybywa wtedy tyle, ile jest podzbiorów tej czwórki.
Do przeczytania jest cena dzisiejszej zgrubności, której nikt nie policzył:
ile zdań Składnicy przechodzi przez parę, której schemat lematu nie ma.

Okolicznik nie ma w żądaniach ani jednej pozycji, a właśnie tam siedzi klasa `MIEJSCE`.
Walenty pisze go kształtem `xp(locat)`, a przyimka w tym kształcie nie nazywa;
nazywa go tabela rozwinięć z tego samego wydania — `phrase_types_expand_20160418.txt` —
gdzie pozycja miejsca rozwija się w trzydzieści przyimków
([`docs/walencja.md`](../docs/walencja.md#przekład-ma-pozycje-ramy-a-okolicznika-nie-ma)).
Tego samego brakuje kolumnie przyimków leksykonu, bo `przyimki` w `harness/walenty.py`
czyta sam `prepnp`: rama, która żąda przyimka okolicznikiem, nie daje świadkowi ramowemu nic.
Ruchem jest rozwinięcie czytane z tej tabeli, jedno dla obu przekładów, bo kryterium jest jedno.
Do przeczytania jest, ile przyimków to dokłada świadkowi ramowemu i ile wierszy plikowi żądań,
bo trzydzieści wierszy mówiących jedno na każdą pozycję miejsca jest ceną,
a alternatywą jest pozycja pod nazwą Walentego, którą czytelnik rozwija sam.

Sonda szukająca konwersów zgaduje rolę z kształtu pozycji, a rola stoi już w pliku.
`harness/konwersy.py` bierze parę schematów, z których jeden ma odbiorcę w celowniku,
a drugi źródło pod `od` albo `u`, i liczba, którą wraca, jest przez to górnym oszacowaniem
([`docs/disambiguation.md`](../docs/disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma)).
`olski/żądania.txt` rozdziela obie strony wprost:
`wynająć` ma pod `od` rolę `Initiator.Source`, a w celowniku `Initiator.Goal`.
Ruchem jest kryterium na uszczegółowienie roli w miejsce kryterium na kształt,
i wtedy sonda chodzi po tym pliku, a nie po wydaniu tekstowym.
Do przeczytania jest, ile lematów zostaje z tych, które sonda wypisuje dzisiaj,
i czy zostają te, o których tamten dokument mówi, że kryterium trafiło w nich obok:
`wykryć komuś raka` i `wykryć u kogoś raka` mówią jedno, więc rola ma je zlać.
Liczbę z tamtego dokumentu przelicza ta sama zmiana.

Deklaracja osób projektu wypełnia się ręką, a pierwsze wpisy umiałby podać przebieg.
Sekcja `osoby` w `olski.toml` odpowiada dziś za klasy osobowe żądania
([`docs/walencja.md`](../docs/walencja.md#deklaracja-projektu-rozstrzyga-żądanie-osoby)),
a warstwa przykładów wydania TEI wskazuje przez `sameAs` te frazy schematu,
które przykład obsadza, czyli te same identyfikatory,
po których chodzi złączenie w `harness/żądania.py`;
przy pozycji przyimkowej przypisanie słowa do pozycji widać z samego zdania,
bo przyimek w nim stoi.
Ruchem jest sonda wypisująca słowa, którymi przykłady obsadzają pozycje
żądające klas osobowych, i ona proponuje, a nie orzeka, jak każda sonda.
Do przeczytania jest przedtem, czy takie słowa w ogóle wchodzą do rejestru,
bo deklaracja jest o lematach, których używa ten projekt, a nie o polszczyźnie.
Pułapka stoi przed pierwszym wpisem: liczby z przykładów nie są definicją klasy —
definiuje ją praca o tej warstwie, zbiorami synsetów —
więc lista z nich wzięta nazywa częstość, a nie przynależność,
i metonimie w niej będą, bo metonimia jest właśnie tym przypadkiem,
w którym słowo żądania nie spełnia.

Klasa kopuli zabiera lematowi wpis z leksykonu (`_walencja` w `olski/subset/rama.py`),
więc kopula nie bywa naraz czasownikiem, który bierze zdanie z `że`.
Widać to na `bywać`, odkąd lemat ten stoi w `KOPULA` w `olski/walencja.py`:
`Odpowiedzią bywa decyzja.` przechodzi z odrzuconego na przyjęte,
a `bywa tak, że` zostaje bez ani jednego czytania —
jedno zdanie Składnicy i jedno zdanie `docs/subset.md`.
Ceną tą zapłacono za rolę: bez tego wpisu `Skreślenie bywa całą naprawą.`
też ma jedno czytanie, tyle że z narzędnikiem w okoliczniku, a nie w orzeczniku
([`docs/konstrukcje-gramatyczne/okolicznik.md`](../docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
Ruchem jest rama kopuli liczona jako suma z ramą tego lematu,
a nie jedna wartość na całą listę,
i wtedy ta sama zmiana rusza `być`, któremu Walenty daje dopełniacz,
bezokolicznik oraz zdanie podrzędne; tamtego rozszerzenia nie zmierzył nikt.
Do przeczytania przed pomiarem jest, że sondzie różnicowej tego nie zmierzyć
podmianą samej stałej: klasy walencyjne liczą się przy imporcie modułu,
a nie w `build`, więc wariant złożony po podmianie `KOPULA` jest tą samą gramatyką.

Pozycja pytania zależnego stoi w ramie domyślnej i nikt nie zmierzył jej zawężenia.
`RAMA_DOMYŚLNA` w `olski/subset/rama.py` daje `int` każdemu czasownikowi,
tak jak daje mu `comp`, a Walenty wypisuje osobno lematy z jednym i z drugim.
Zawężenie `comp` do leksykonu zmierzono i nie kupiło ani jednego czytania,
a przy `int` wynik nie musi wypaść tak samo:
pytanie zależne konkuruje z koordynacją przecinkiem i ze zdaniem względnym,
gdzie zdanie z `że` nie konkuruje z niczym, bo spójnika `że` nie bierze nic innego.
Wpis waży więcej, odkąd `co` bierze poprzednik zdaniowy: cena tamtej pozycji
stoi prawie cała na zdaniach z pytaniem zależnym, którym ono dokłada
drugie czytanie
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie)),
więc zawężenie `int` do leksykonu odbiera ją tym z nich,
których czasownik pytania nie żąda.
Czeka na ten wpis pytanie o miejsce.
`Gdzie są przetrzymywani zakładnicy?` zostaje odrzucone dlatego,
że `gdzie` dopisane do przysłówków pytajnych daje drugie czytanie
każdemu zdaniu, w którym ta forma otwiera okolicznik pod czasownikiem spoza
leksykonu — `Wchodzi w roadmap.md, gdzie linter sprawdza regułę.` —
a czytania tego polszczyzna nie ma
([`docs/konstrukcje-gramatyczne/podrzędność.md`](../docs/konstrukcje-gramatyczne/podrzędność.md#pytanie-o-okoliczność-wysuwa-przysłówek-a-zdanie-pod-nim-jest-całe)).
Nad prozą tego repozytorium sam lemat kosztuje w werdyktach zero
i wyciąga z odrzucenia pojedyncze zdania,
więc po zawężeniu wchodzi bez pomiaru drugiego.
Ruchem jest osobne zdanie leksykonu o `cp(int)`, wzięte przez `harness/walenty.py`,
i wariant gramatyki bez `int` w ramie domyślnej, zmierzony wobec olskiego.
Czym ten wariant zmierzyć, jest rozstrzygnięte:
zawężenie ramy jest zmianą danych, a nie grupą produkcji,
i takiemu wariantowi `Sonda` podaje gramatykę funkcją (`Sonda.gramatyki`).
Do przeczytania jest przy tym, czy skład ma dla tego zdania czytelnika:
zdanie o zdaniu podrzędnym czyta ono (`rama` w `olski/walencja.py`),
a pytania zależnego
`olski/skład/składnia.py` nie ma czym postawić,
więc zdanie dopisane bez tej kategorii jest danymi, których nie czyta nikt.

`pod względem` żąda licencji od słowa, do którego się przyłącza,
a olski żąda licencji tylko od dopełnienia.
Czytelnik odrzuca `wolni pod względem swej godności` bez pomocy składni,
bo `równy` ma pozycję na wzgląd, a `wolny` jej nie ma.
Tę samą obserwację robi nad `przewyższać`
[`docs/subset.md`](../docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera),
gdzie porównanie mówi, w czym jedno przewyższa drugie,
i nie ma jej dziś gdzie zapisać.
Leksykon walencyjny mówi o pozycjach ramy, które czasownik bierze albo których nie bierze
([`docs/walencja.md`](../docs/walencja.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)),
a okolicznik pozycji ramy nie zajmuje i przyłącza się do każdego czasownika za darmo,
więc żaden wpis nie odbiera czytania,
w którym wzgląd dochodzi do `rodzą się`.
Ruchem jest zdanie leksykonu odwrócone wobec tamtych trzech:
nie „ten czasownik czegoś nie bierze”, tylko „to wyrażenie przyimkowe
przyłącza się tam, gdzie licencjonuje je leksykon”,
czyli cecha przy przyimku zleksykalizowanym, a nie przy jego gospodarzu.
Robi ono z pierwszego artykułu Deklaracji zdanie jednoznaczne:
odejmuje czytanie z `rodzą się`, bo ten czasownik wzglądu nie licencjonuje,
a zostaje czytanie z `równi`, czyli jedno.
Odejmuje też czytanie nad całym ciągiem współrzędnym,
bo `wolny` wzglądu nie licencjonuje tak samo.
Do rozstrzygnięcia jest, czy to jeszcze walencja, czy już ta warstwa,
którą [`docs/open-questions.md`](../docs/open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma)
odkłada poza gramatykę jako odpowiedź trzecią;
różnicę robi to, że leksykon w gramatyce już jest, a tamta warstwa nie.
Do przeczytania jest, ile takich przyimków rejestr ma,
bo `pod względem` jest jednym z nich i nikt nie policzył, ile jest reszty,
oraz co Walenty mówi o wzglądzie:
pozycje zleksykalizowane wypisuje on w schemacie,
a przymiotnika, który licencjonuje tu wzgląd, nie ma w pliku czasownikowym,
z którego leksykon powstaje,
choć archiwum obok tego pliku niesie katalog przymiotnikowy.
Kryterium wejścia ma ten ruch to samo, co każda warstwa więzowa:
[wyprowadza się z gramatyki albo jest gramatyką pisaną drugi raz](../docs/parsowanie.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej),
a leksykalnie znaczy to tyle, że pozycję wypisuje słownik.
Jeśli Walenty jej nie wypisuje, ruchu nie ma i cały wpis zamyka skasowanie,
bo „brzmi nielogicznie” jest sądem o świecie, a nie faktem o słowie:
olski melduje wtedy wieloznaczność, tak samo jak melduje ją wszędzie indziej.

Rama mówi, co czasownik bierze, i nie mówi, ile tego bierze.
Dopełnień stoi przy czasowniku najwyżej jedno,
bo tyle stoi w ciele każdej produkcji `wypełnienia` w `olski/subset/zdanie.py`,
a nie dlatego, że rama tak mówi;
ruchem jest rama zużywana, czyli ta,
[którą pokazuje Świgra](../docs/swigra.md#valency-as-a-resource-that-gets-consumed):
pozycja zajęta znika z tego, co niesie reszta grupy.
Wolno ją wyrazić cechą o dziedzinie skończonej,
bo pozycji jest w ramie skończenie wiele,
więc rozwinięcie idzie przed parsowaniem i nie rusza klasy złożoności.
Kupuje to jednak tyle, ile jest ram o dwóch pozycjach naraz,
a rama domyślna takiej nie ma:
biernik z bezokolicznikiem naraz zmierzono i nad Składnicą pod złotą morfologią
przyjmuje kilka zdań mniej, a wieloznacznych ma o kilka więcej,
bo grupa imienna za bezokolicznikiem dochodzi wtedy i do niego, i do formy osobowej.
Pozycja, która z inną naprawdę stoi, jest już wpuszczona i jest nią celownik obok
wypełnienia ([`docs/walencja.md`](../docs/walencja.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)),
tyle że licencji nie niesie tam rama, tylko cecha obok niej,
bo ramy unifikacja nie zużywa, a przecina.
Ruch jest przez to odwróceniem tamtej decyzji, a nie dopisaniem do niej:
rama zużywana zdejmuje tę cechę i wypowiada parę samą ramą.
Do przeczytania jest, co robi z klasami walencyjnymi:
dziś dzieli je para na dwie, a rama zużywana dzieliłaby je tym,
ile pozycji lemat bierze naraz.

Dopełniacz nie ma drugiej pozycji ramy, którą ma celownik
([`docs/walencja.md`](../docs/walencja.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).
Walenty daje go przy bierniku 15 lematom, przy pytaniu 28, a przy zdaniu 6,
i te liczby są całym powodem, dla którego pozycja weszła sama celownikiem.
Ruchem jest druga wartość cechy `druga` w `olski/subset/rama.py`
wraz ze zdaniem leksykonu liczonym tak samo jak tamto,
a przed nim pomiar, bo cena tej pozycji jest po stronie żywej morfologii wysoka:
celownik dzieli formę z miejscownikiem, a dopełniacz z biernikiem i z mianownikiem mnogim.
Do przeczytania jest, czy zdanie z tą parą da się w ogóle odróżnić po werdykcie:
`Nauczyciel uczy dzieci matematyki.` wyprowadza się już dziś,
bo dopełniacz za grupą imienną czyta się jej przydawką,
więc brak tej pozycji nie odrzuca zdania, tylko odbiera mu drugie czytanie.

Rama jest w tej gramatyce stanem, a nie zasobem, i nikt nie policzył, co to kosztuje.
Pozycji już zajętej unifikacja nie ma jak odnotować, bo zajęcie zależy od pozostałych
córek, a nie od pary głowy i zależnego, i na tym walencja wypadła z kanału cech
([`docs/parsowanie.md`](../docs/parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)).
Sonda więzowa płaciła za to samo dwoma polami sprawdzanymi nad drzewem gotowym —
łukiem wymaganym i łukiem zakazanym
([`docs/design-notes.md`](../docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)) —
i jest to jedyny znany warunek, którego przecięcie zbiorów nie umie powiedzieć,
a warstwa za parserem umiałaby.
Do przeczytania jest przedtem, czy w tej gramatyce jest w ogóle co zdejmować:
ciało produkcji wylicza córki, więc pozycja wypełniona dwa razy żąda dwóch ciał,
a jeżeli żadne takie nie stoi, cały wpis zamyka skasowanie z powodem w commicie.
Jeśli stoi, ruchem jest warunek nad czytaniem gotowym wraz z jego ceną
zmierzoną tak, jak mierzy się wpuszczenie pozycji.

`podjąć` nie ma w `olski/żądania.txt` ani jednego wiersza,
więc `--osoby` milczy nad `Dokument podjął decyzję o wdrożeniu.`,
choć zdanie to stoi w korpusie usterek właśnie z tym zgłoszeniem
(`próba/usterki.txt`).
Leksykon walencyjny ten lemat wymienia, a plik żądań nie,
i nie jest to obcięcie wejścia, bo `podjudzić` stoi w pliku obok.
Do przeczytania jest wpis `podjąć` w wydaniu TEI Walentego.
`podjąć decyzję` jest tam frazą zleksykalizowaną,
a takiej frazy `pozycja` w `harness/żądania.py` pozycją nie nazywa;
pytanie brzmi, czy razem z nią wypada podmiot tego samego schematu,
bo podmiot jest osobną frazą i żądanie osoby stoi właśnie w nim.
Ruch zależy od odpowiedzi:
podmiot gubiony razem z frazą zleksykalizowaną jest usterką przekładu,
a lemat bez warstwy semantycznej jest brakiem zasobu
i wtedy zgłoszenie nad tym zdaniem musi wziąć coś innego niż żądanie ramy.
Ceną wejścia jest pobranie Walentego, bo ten plik powstaje przebiegiem.
