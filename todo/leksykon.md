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
