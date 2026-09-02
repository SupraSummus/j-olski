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
[Liczba, na której leksykon stoi](../docs/warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)
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
Narzędnika [przekład](../docs/warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)
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
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)).
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
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#przekład-ma-pozycje-ramy-a-okolicznika-nie-ma)).
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

Żądanie ma dwie strony, a tę drugą — czy słowo w pozycji do klasy należy —
mogłaby wziąć ręka, i jest to myśl luźna, nie plan.
Wordnetu ten projekt nie ma i nie ma go jak pobrać
([`docs/open-questions.md`](../docs/open-questions.md#shared-questions)),
a leksykon pisany ręką ma tu precedens:
`KOPULA` w `olski/walencja.py` jest listą wpisaną z palca,
a `olski.toml` istnieje właśnie po to, żeby odpowiadać na pytania,
na które nie odpowiada żaden korpus.
Pełnej taksonomii do tego nie trzeba.
Klas nazwanych Walenty ma dwadzieścia, a regule o wymyślonym sprawcy
([CLAUDE.md](../CLAUDE.md#dla-kogo-jest-napisane-zdanie))
wystarcza jedno rozróżnienie, bo resztę podziału niesie strona żądania:
`kupować` żąda w podmiocie człowieka, a `rozstrzygać` bierze tam i komunikat.
Miejscem takiego bitu jest `olski.toml`, a wypełniałby się przy słowie,
które i tak wchodzi tam decyzją, więc kampanii to nie żąda;
słowo nieznane zostawia warstwę milczącą, tak jak przy świadku przyłączeniowym.
Pierwsze wpisy umiałby podać przebieg, zamiast ręki:
warstwa przykładów wydania TEI wskazuje przez `sameAs` te frazy schematu,
które przykład obsadza, czyli te same identyfikatory,
po których chodzi złączenie w `harness/żądania.py`,
a przy pozycji przyimkowej przypisanie słowa do pozycji widać z samego zdania,
bo przyimek w nim stoi.
Taki przebieg proponuje, a nie orzeka, i do drzewa nie wchodzi, jak każda sonda.
Pułapki są dwie i obie stoją przed pierwszym wpisem.
Liczby z przykładów nie są definicją klasy — definiuje ją praca o tej warstwie,
zbiorami synsetów — więc plik z nich wzięty nazywa częstość, a nie przynależność,
i metonimie w nim będą, bo metonimia jest właśnie tym przypadkiem,
w którym słowo żądania nie spełnia.
Bit pisany ręką nie może zaś znaczyć „czy to może być podmiotem czasownika”,
bo ta proza metonimii używa rozmyślnie — `dokument mówi`, `reguła żąda` —
i wtedy zapala się na każdym akapicie; wąskie „czy to osoba” tego nie robi.
