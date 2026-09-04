# Orzeczenie i pozycje jego ramy

Jeden plik rejestru konstrukcji, w którym sekcja przypada na konstrukcję.
Cena i zakup stoją w niej rzędem wielkości albo granicą.
Co ten rejestr obiecuje i który plik czytać, mówi [wstęp](README.md).

## Czas przeszły żąda rodzaju od każdego szyku

Czas przeszły stoi w kolejce ze Składnicy
([corpus.md](../corpus.md#where-the-analyses-stop)),
a kosztuje więcej niż jedną formę czasownika w produkcji `orzeczenie`.
Forma `praet` niesie rodzaj i liczbę, a osoby nie niesie wcale,
czyli dokładnie odwrotnie niż `fin`,
więc zgodność, którą czas teraźniejszy zostawiał grupie imiennej,
przechodzi w czasie przeszłym przez orzeczenie.
Rodzaj wchodzi przez to do każdego szyku zdania,
bo `lista stała` i `wywód stał` różni sam rodzaj podmiotu,
a szyk, który rodzaju nie przepuszcza, przyjmuje `lista stał`.
Dwa symbole podmiotu zlały się przy tym w jeden:
szyk bez rodzaju przestał się różnić od szyku z rodzajem,
odkąd rodzaju żąda każdy.

Osobę pierwszą i drugą wnosi w tym czasie osobny segment.
Morfeusz odcina od formy końcówkę osobową — `napisałem` to `napisał` i `em` —
i to ona niesie liczbę oraz osobę,
więc czasownik dostaje trzy ciała zamiast jednego:
`fin` albo `impt`, samo `praet` z osobą trzecią wpisaną w produkcję,
oraz `praet` z aglutynantem.
Tryb przypuszczający dokłada do tych trzech dwa dalsze
([niżej](#tryb-przypuszczający-jest-jedną-cząstką)).
Bez wpisanej trzeciej osoby `Ja napisał program.` wyprowadza się,
bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza.

## Tryb przypuszczający jest jedną cząstką

Morfeusz dzieli `odzyskałby` na czas przeszły i cząstkę `by`,
a `napisałbym` na czas przeszły, cząstkę i aglutynant,
więc tryb przypuszczający jest w tej gramatyce jedną cząstką
dopisaną do formy czasownika.
Ciała są dwa, po jednym na każde ciało czasu przeszłego,
i cząstkę dostaje ten czas i tylko on, bo tak stawia ją polszczyzna:
`zapisujeby` nie jest niczym.

Ceny w czytaniach ta cząstka nie ma żadnej i wynika to z gramatyki, nie z przebiegu:
formy `by` nie bierze przy czasowniku żaden inny terminal,
więc zdanie z nią albo wyprowadza się tymi dwoma ciałami, albo nie ma czytania wcale.
Niezmiennika pilnuje `tests/test_subset.py`, gdzie zdanie z tą cząstką stoi wśród
przyjmowanych: `by` dopisane do listy cząstek daje mu drugie czytanie i wywraca test.
Ciało z aglutynantem nie rusza przy tym nad prozą tego repozytorium
ani jednego werdyktu: ten rejestr pisze `odzyskałby`, a nie `odzyskałbym`.
Kolejkę form bez licencji `by` prowadziło właśnie nad tą prozą
([corpus.md](../corpus.md#where-the-analyses-stop)),
a większość jego wystąpień w niej jest angielskim przyimkiem,
co widać po tym, że stoi za formą, której słownik nie zna.

Ta sama cząstka bywa wpisana w spójnik:
`żeby` jest z `że` i `by`, `gdyby` z `gdy` i `by`,
`aby` z `a` i `by`, a `jakby` z `jak` i `by`.
Cząstka jest w zdaniu jedna, więc pod takim spójnikiem stoi forma na -ł
bez własnej cząstki: `Zażądałem, by wyszedł.`
Żeby spójnik miał czego żądać, zdanie ogłasza cechą `tryb`,
gdzie ta cząstka w nim stoi: przy czasowniku, w spójniku albo nigdzie.

Forma na -ł bez cząstki wychodzi z dwiema wartościami tej cechy naraz.
`Program zapisał ustawienia.` orzeka w trybie oznajmującym, kiedy stoi samo,
a pod spójnikiem w przypuszczającym,
i jest to ten sam synkretyzm, który ta gramatyka zna z przypadka:
jedna forma, dwie wartości, a wybiera między nimi przecięcie.
Samo zdanie żadnej z nich nie żąda,
więc zdanie w czasie przeszłym wyprowadza się tak jak przedtem.

Trzy napisy zostają przez to poza podzbiorem i każdy z innego powodu.
`żeby program zapisuje ustawienia` niesie formę osobową, która cząstki nie bierze.
`żeby linter sprawdziłby tekst` niesie cząstkę dwa razy.
`żeby napisałem plik` niesie aglutynant w miejscu,
w którym pod tym spójnikiem stoi jego własna końcówka:
polszczyzna ma `żebym napisał`.

Ceną jest ta cecha w każdej produkcji zdania.
Cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc ciało, które trybu nie przepuści, wpuszcza pod ten spójnik każdy tryb.
Niezmiennika pilnuje `tests/test_orzeczenie.py`:
ciało zdania bez tej cechy wywraca suitę,
bo pojedyncze zdanie tego nie łapie, a ciał zdania jest kilkadziesiąt.

Ciąg współrzędny wypuszcza tryb członu pierwszego i od pozostałych nie żąda niczego,
więc `żeby program zapisał ustawienia i linter sprawdza tekst` wyprowadza się,
choć polszczyzna żąda formy na -ł od obu członów.
Zmienna wspólna zabrałaby zdania już przyjęte:
`Program zapisuje ustawienia, a linter sprawdziłby tekst.`
koordynuje tryb oznajmujący z przypuszczającym.

Ile ich zabrałaby, jest zmierzone.
Zmienna wspólna na ogonie ciągu odbiera wyprowadzenie kilku zdaniom Składnicy,
pod morfologią żywą dwa razy tylu zdaniom,
a przeszło dziesięciu zdaniom prozy tego repozytorium,
bo koordynacja dwóch trybów jest w niej zwyczajna
(`Lista urywa się na MAX_READINGS, […] więc odpowiedź policzona po liście myliłaby
brak czytania z jego numerem`).
Kupuje za to czytania nieprawdziwe w kilku zdaniach banku drzew,
a jednoznaczności nie kupuje ani jednemu zdaniu:
z wieloznacznych do przyjętych nie przechodzi żadne.
Naprawa mieszcząca się w cechach jest więc droższa od usterki,
a naprawa poza cechami żąda warunku sprawdzanego po rozbiorze,
którego olski nie ma i który dla tej jednej pozycji nie zarabia na siebie.
Liczby daje wariant gramatyki z tą zmienną, puszczony przez `harness/ruch.py`.

Wypełnieniem bywa fraza bezokolicznikowa zamiast zdania —
`Odnotowuję to, żeby złagodzić wrażenie.` —
i w banku drzew pada ona pod tymi spójnikami
niemal tak samo często jak forma na -ł.
Ciało z bezokolicznikiem jest osobne, bo jego cena jest osobną liczbą.
Oba wypełnienia biorą oba miejsca okolicznika,
bo zdanie z każdym z tych spójników polszczyzna wysuwa:
`Żeby zostać rezydentem księstwa, musisz mieć oszczędności.`

Cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew,
a wynika to z gramatyki, nie z przebiegu:
`comp` z tymi lematami nie brał przedtem żaden terminal.
Zakupem jest przeszło pięćdziesiąt zdań Składnicy zdjętych z listy odrzuconych,
z czego połowa na przyjęte.
Role tych przyjętych zgadzają się z drzewem wzorcowym poza jednym zdaniem:
w `Zrodził się pomysł, by produkować klepkę.`
bank drzew przyłącza cel do rzeczownika, a olski do zdania.
Nad prozą tego repozytorium nie kupuje ani jednego zdania,
tak samo jak dopisania przed nim.

Poza podzbiorem zostaje cząstka stojąca dalej od czasownika —
`Nie ma aplikacji, która by to wszystko napędzała.` —
i jest to [nieciągłość](../design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
a nie brak pozycji.
Zostaje też aglutynant przy spójniku, czyli `żebym napisał`:
Morfeusz tnie ten napis na `żeby` i `m`,
a końcówka dochodzi w tej gramatyce do czasownika, przy którym stoi.

## Forma `bedzie` orzeka sama albo składa czas przyszły złożony

Czas przyszły stoi w kolejce ze Składnicy
([corpus.md](../corpus.md#where-the-analyses-stop)),
a niesie go tam jedna część mowy:
`bedzie` jest u Morfeusza osobną odmianą,
więc wiersz kolejki nazywa tę konstrukcję wprost.

Polszczyzna stawia tę formę w dwóch rolach i olski bierze obie.
Sama orzeka o podmiocie tak jak każda inna forma `być`:
`Cena będzie niska.`, `Testem będzie konkurs krajowy.`
Ramę bierze przy tym z leksykonu razem z resztą form tego lematu
([walencja.md](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
więc biernika nie weźmie i `Cena będzie plik.` nie ma wyprowadzenia.
Nad czasownikiem niedokonanym składa czas przyszły złożony:
`Program będzie zapisywał ustawienia.`, `Program będzie zapisywać ustawienia.`

Zgodność dzieli się w tym czasie na dwa słowa.
`bedzie` niesie liczbę i osobę, a rodzaju nie niesie, dokładnie jak `fin`.
Rodzaju żąda przez to zdanie z formą na -ł, tak samo jak czas przeszły
([wyżej](#czas-przeszły-żąda-rodzaju-od-każdego-szyku)),
więc `Lista będzie stał.` nie ma wyprowadzenia,
a zdanie z bezokolicznikiem nie żąda go wcale.
Liczby żądają oba, bo ciało z bezokolicznikiem ogłasza ją samo;
bez tego wyprowadza się `Programy będzie zapisywać ustawienia.`,
skoro cechy, której konstytuent nie niesie, unifikacja nie sprawdza.

Aspekt jest tu żądaniem wypisanym:
polszczyzna składa ten czas z czasownikiem niedokonanym i z żadnym innym,
więc `Program będzie zapisał ustawienia.` zostaje na zewnątrz.

Pozycje są dwie, a nie jedna z formą dopisaną do `fin`,
bo cena każdej z nich ma być osobną liczbą.
Obie kupują nad Składnicą po kilkanaście zdań przyjętych,
a większość tego, co zdejmują z odrzuconych, wychodzi wieloznaczna.
Pod złotą morfologią ani jedno zdanie banku drzew nie rusza się pod obiema naraz,
a pod żywą jedno, więc liczba jednej pozycji nie zależy od drugiej.
Razem oddają przeszło jedną trzecią tego, co obiecywał wiersz kolejki,
i jest to pierwszy pomiar, który oddał więcej, niż obiecywał
[przelicznik kolejki](../corpus.md#kolejka-obiecuje-więcej-niż-pozycja-oddaje).
Ani jedno nowo przyjęte zdanie nie czyta się odwrotnie niż drzewo wzorcowe.
Nad prozą tego repozytorium zdejmują z odrzuconych jedno zdanie
i wychodzi ono wieloznaczne, bo ten rejestr pisze czas teraźniejszy.

Z wiersza `bedzie` zostaje po tym garść zdań, a prowadzi ją `trzeba będzie`,
czyli czas przyszły predykatywu
([niżej](#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika)):
forma stoi tam za słowem, które orzeka,
a predykatyw pozycji na czasownik nie ma, bo orzeka bez niego.

Szyk jest jeden — forma przyszła przed czasownikiem —
więc `Zapisywał będzie ustawienia.` zostaje na zewnątrz,
choć polszczyzna ten szyk ma.
Cząstka `się` ma przy tym czasie te same dwie pozycje co przy formie osobowej,
czyli `Rachunek się będzie zwracał.` i `Rachunek będzie zwracał się.`,
a pozycji między formą przyszłą a czasownikiem nie ma,
więc `Rachunek będzie się zwracał.` zostaje na zewnątrz
razem z resztą tego, czego ta cząstka nie obejmuje
([niżej](#cząstka-zwrotna-należy-do-swojego-czasownika)).

## Cząstka zwrotna należy do swojego czasownika

Cząstka `się` jest dla leksykonu drugim wymiarem lematu, a nie określeniem:
`otwierać` bierze dopełnienie w bierniku, a `otwierać się` go nie bierze
([walencja.md](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)).
Należy przez to do czasownika, a nie do formy, w jakiej on stoi,
więc pozycję ma przy formie osobowej, przy bezokoliczniku i przy imiesłowie
czynnym, a ile ich jest przy każdej z nich, mówi polszczyzna.

Polszczyzna daje cząstce przy formie osobowej dwie pozycje,
więc gramatyka ma oba ciała:
`Rachunek zwraca się.` oraz `Rachunek się zwraca.`
W pozycji przedniej cząstka poprzedza przeczenie —
`Rachunek się nie zwraca.` — bo tam ją polszczyzna stawia,
a `Rachunek nie się zwraca.` nie jest niczym.
Ramę oba ciała biorą z leksykonu zwrotnego,
bo pozycja jest tu inna, a czasownik ten sam.

Cena wyszła zerowa nad bankiem drzew pod obiema morfologiami
oraz nad prozą tego repozytorium,
a wynika to z gramatyki, nie z przebiegu:
cząstki stojącej przed formą osobową nie brało przedtem ani jedno ciało.
Zakupem jest przeszło sześćdziesiąt zdań Składnicy zdjętych z odrzuconych,
z czego większość na przyjęte, a pod morfologią żywą tyle samo.
Role tych przyjętych nie kłócą się z drzewem wzorcowym nad ani jednym zdaniem,
a tam, gdzie odczytanie olskiego obejmuje mniej niż drzewo,
stoją zdania nieosobowe, którym bank drzew daje cząstce rolę podmiotu
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)).
Nad prozą tych dokumentów zdejmuje z odrzuconych kilkanaście zdań.

Pozycja przednia sięga początku zdania oraz miejsca tuż za znakiem,
a `Się myli.` ani `Cena rośnie, się nie liczy.` polszczyzną nie są,
więc cząstka żąda słowa przed sobą: opiera się o nie, a znak słowem nie jest.
Spójnik słowem jest i licencji udziela — `Cena rośnie, a się nie liczy.` —
bo taki napis bank drzew pisze:
`Po wielu latach sporów wiadomo już, że lądolód Grenlandii i przyrasta, i się topi`
oraz `żeby chór nie tylko istniał, ale się rozwijał`.
Warunek stoi w warstwie morfologicznej, tam gdzie warunek na formę przyimkową
zaimka ([grupa-imienna.md](grupa-imienna.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)),
i pyta o to samo: `po_słowie` w `olski/segmentacja.py` zdejmuje cząstce odczytanie tam,
gdzie w węźle otwierającym jej krawędź nie kończy się krawędź z odczytaniem,
które znakiem nie jest.
Werdykt nazywa wtedy formę bez licencji, a nie strukturę, której zdaniu brakuje,
i tyle właśnie autorowi trzeba: przez cząstkę zdanie się nie otwiera.
Pozycji tylnej ten warunek nie tyka, bo przed nią stoi jej własna forma,
więc nie zdejmuje ani jednego odczytania, które olski brał przed tym ciałem.

Te same dwie pozycje ma bezokolicznik:
`Cena zaczyna otwierać się.` i `Cena zaczyna się otwierać.` wyprowadzają się oba,
a `Trzeba się zabezpieczyć.` wyprowadza się przez predykatyw.
Imiesłów czynny bierze cząstkę jedną pozycją, za sobą —
`program otwierający się` — bo tam ją polszczyzna stawia;
bierny nie bierze jej wcale, bo strony biernej czasownik zwrotny nie ma.

Pozycja przy bezokoliczniku kupuje nad Składnicą kilkadziesiąt zdań
pod obiema morfologiami, a zgodność ról podnosi zamiast obniżać:
zdań, w których przyjęte odczytanie przeczy drzewu wzorcowemu, nie przybywa
ani jedno ([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)).
Nad prozą tych dokumentów zdejmuje z odrzuconych garść zdań —
`Komentarz mieszczący się w jednym wierszu zostaje w jednym wierszu.` —
a nad README nie rusza ani jednego werdyktu.

Ceną jest garstka odrzuceń i wszystkie stoją na jednym:
cząstka odgrodzona od swojego czasownika słowem,
czyli [nieciągłość](../design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
a nie brak pozycji.
`Rachunek się dotąd nie zwraca.` pada, `Rachunek dotąd się nie zwraca.` przechodzi,
a `Nie mogłem się na niczym skupić.` pada z tego samego powodu,
bo cząstka należy tam do `skupić`, a odgradza ją od niego wyrażenie przyimkowe.
Nad prozą tych dokumentów pada tak jedno zdanie —
`Akt pod nim nie może się już zmienić.` — gdzie odgradza ją `już`.
Odrzucenie jest w tych zdaniach werdyktem prawdziwym,
bo jedyne odczytanie, jakie by zostało, prowadzi przez formę osobową obok —
`mogłem się` — a takiego czasownika polszczyzna nie ma.
Jedno miejsce zostaje poza podzbiorem, choć cząstka stoi w nim
tuż przy swoim czasowniku: wnętrze czasu przyszłego złożonego,
czyli `Fabryki będą się znajdować we Włoszech.`
Cząstka stoi tam między dwiema częściami jednego orzeczenia
([wyżej](#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony)),
a pozycji między nimi nie ma ani jedno ciało; ruch trzyma `todo/`.

Gdzie cząstka może należeć do dwóch czasowników naraz, olski wypuszcza oba
odczytania. `Program otwierający się psuje.` czyta się i z `otwierający się`
w przydawce, i z `się psuje` w orzeczeniu, bo obie formy są w polszczyźnie
zwrotne, a wybiera między nimi znaczenie.
Tam, gdzie wybiera leksykon, wypuszcza jedno:
`Zebranie ma się odbyć.` ma odczytanie z `odbyć się`
i nie ma go z `mieć się`, bo `mieć się` bezokolicznika nie bierze
([walencja.md](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)).
Zostaje przez to konkurencja przy czasowniku zwrotnym,
któremu Walenty bezokolicznik daje: `Nie daj się schwytać.`
wychodzi dwoma odczytaniami, bo `dać się` bierze bezokolicznik
i cząstka pasuje wtedy do obu ciał.
Płaci za to [przyrząd pomiarowy](../roadmap.md#readme-jest-przyrządem-pomiarowym):
zdanie README o tym, co z prozy da się lintować, ma odtąd dwa razy tyle odczytań,
i jest to jedyne zdanie tego pliku, które ta pozycja rusza.
Ceną jest więc wieloznaczność przy kilkuset lematach, a nie przy każdym,
i tyle właśnie kupuje odjęcie bezokolicznika ramie zwrotnej.

Klasa domyślna leksykonu zwrotnego cząstki kopuli nie daje.
Leksykon ten wymienia zwrotność zleksykalizowaną i tylko ją,
a lemat, którego nie wymienia, bierze pod cząstką ramę domyślną,
bo cząstkę polszczyzna stawia przy czasowniku dowolnym: `myśli się`, `pije się`.
Kopula wchodzi tamtędy razem z nimi, a `być się` czasownikiem nie jest,
więc bez odmowy wyprowadza się `Cena się jest niska.`
Odmowa stoi przy tej klasie i wymienia lematy kopuli
(`KOPULA` w `olski/walencja.py`);
jest to jedyny czasownik, któremu ta gramatyka cząstki odmawia wprost.
Lematu `zostać` nie tyka, bo leksykon zwrotny go wymienia,
a klasa domyślna po lemat wymieniony nie sięga.
Nic to nie kosztuje: gramatyka bez tej odmowy nie rusza nad Składnicą
ani jednego werdyktu pod złotą morfologią, a jednego pod żywą.

Zamknięcie całego leksykonu zwrotnego zmierzono i olski go nie bierze.
Gramatyka odmawiająca cząstki każdemu lematowi, którego Walenty nie wymienia
jako czasownika zwrotnego, traci nad Składnicą pod obiema morfologiami
kilkadziesiąt zdań, którym olski daje dziś odczytanie,
a jednoznaczności kupuje przy tym pojedyncze zdania.
Zdania przyjęte przeczytano po kolei i większość z nich niesie polszczyznę,
a nie usterkę.
Jedna klasa niesie zwrotność, którą Walenty pisze pozycją `refl` albo `recip`
w schemacie lematu niezwrotnego, a nie osobnym lematem:
`Spotkał się ze stanowczą odmową.`
Druga niesie cząstkę bezosobową — `Myśli się językowo.`,
`Wino białe pije się inaczej.` — której Walenty nie leksykalizuje,
bo dochodzi ona do czasownika dowolnego,
a olski wyprowadza ją dziś tą samą klasą domyślną,
czytając ją czasownikiem zwrotnym z podmiotem.
Decyzję odwraca pozycja na cząstkę bezosobową, czyli zdanie bez podmiotu
z dopełnieniem w bierniku, wraz z leksykonem czytającym obie pozycje Walentego;
bez nich zamknięcie listy płaci pokryciem za czytania prawdziwe.

## Negacja żąda dopełniacza i żąda go ponad bezokolicznikiem

Cząstka `nie` stoi przed formą czasownika, a przypadek dopełnienia zmienia
w całym zdaniu: `Program zapisuje ustawienia` bierze biernik,
`Program nie zapisuje ustawień` żąda dopełniacza, i żąda go obowiązkowo.
Dopełniacz negacji jest przez to drugą produkcją tej samej pozycji ramy,
a nie drugą pozycją: to samo miejsce u czasownika,
inny przypadek grupy, która je zajmuje.

Sięga on dalej, niż stoi cząstka.

```text
Program nie pozwala zapisać ustawień.
```

Przeczy tu forma osobowa, a przypadek zmienia się dopełnieniu,
które wisi pod bezokolicznikiem, i tak samo przez łańcuch dowolnej długości.
Rządzenie przechodzi więc przez konstytuent, czego zgodność nie robi nigdzie,
a mimo to jedzie kanałem cech, tym samym, którym jedzie rama.
Na jakich warunkach ten kanał je wpuścił, wywodzi
[parsowanie.md](../parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne).

Fraza bezokolicznikowa z własną cząstką tej cechy nie wypuszcza wcale
i tym zamyka przenoszenie:
`Program ma nie zapisywać ustawień` przeczy bezokolicznikowi, a nie formie
osobowej nad nim, więc żądanie z góry ma tu nie dojść.
Nieobecność cechy jest tym samym mechanizmem, którym grupa współrzędna nie niesie
rodzaju. Ta sama droga sięga wysuniętego zaimka względnego —
`polszczyzna, której nikt nie napisał` obok `polszczyzna, którą ktoś napisał` —
i tam kosztuje najwięcej, bo przypadek zaimka rozstrzyga przeczenie stojące za
całą resztą zdania składowego, więc `rdzeń_względny` ma dwa razy tyle ciał.

Poza biernik dopełniacz negacji nie sięga.
Orzecznik narzędnikowy stoi przy `nie jest` tak samo jak przy `jest`,
grupa pod przyimkiem zostaje w przypadku, którego przyimek żąda,
a czasownik, o którym leksykon mówi, że biernika nie bierze,
nie zyskuje przy przeczeniu nowej pozycji.

## The bare verb-initial order keeps the predicative one honest

```text
Trwa akcja protestacyjna.
```

The adjective is attributive or it is predicated,
and Polish gives a reader both.
Admit only the verb-initial order that takes a predicative
and the second reading has nothing to compete with,
so olski calls it the one reading and is confidently wrong.
That is the failure
[corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance) counts,
and admitting the bare order beside it
costs the sentence its uniqueness and keeps its honesty.

The subject takes no complements of its own in either order,
which is what stops `Zapisuje program ustawienia.` deriving
and stops every SVO sentence competing with a verb-initial reading of itself.

## Łącznik `to` orzeka sam albo przy kopuli, a podmiot stoi za nim

`Flaga to płat tkaniny określonego kształtu.`, `Jedyna różnica to rozmiar.` —
zdanie ma tu dwie grupy imienne w mianowniku i nie ma czasownika,
a spina je `to`, które Morfeusz trzyma pod `pred`.
Zamknięta lista predykatywów tego lematu nie bierze
([niżej](#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika)),
bo łącznik orzeka inaczej niż tamte słowa:
ma przy sobie podmiot i ramy czasownika nie rządzi.
Wchodzi przez to osobnym ciałem.

Która grupa jest podmiotem, rozstrzyga bank drzew, a nie morfologia:
obie stoją w mianowniku, więc zgodność nie mówi o tym nic,
a polszczyzna parafrazuje to zdanie kopulą w obie strony —
`Flaga jest płatem tkaniny.` i `Rozmiar jest jedyną różnicą.`
Warianty gramatyki są przez to dwa, po jednym na stronę,
i nad Składnicą przyjmują te same zdania, różniąc się samą etykietą:
pozycja podmiotu postawiona za łącznikiem zgadza się z drzewem wzorcowym
niemal wszędzie, a postawiona przed nim jest niezgodna niemal wszędzie.
Obie klasy zdań odpowiadają tak samo, więc liczby zbiorczej nie niesie jedna z nich:
w klasie bezczasownikowej drzewo stawia tę pozycję za łącznikiem w 204 zdaniach
i przed nim w 9, a w klasie z kopulą — `Był to nieforemny chłopak.` — w 162 i w 3.
Mniejszość jest w obu i czyta się ją tak, jak przeczytałaby ją składnia szkolna:
`Sebastian to niesłychanie ciepły, pracowity i dobry człowiek.`
ma tę pozycję przed łącznikiem.
Czym różnią się te zdania od czterdziestu razy liczniejszej większości, nie wiadomo,
i tego pytania ten pomiar nie zamyka.
Pozycja podmiotu stoi więc za łącznikiem, czyli tam, gdzie stawia ją Składnica.

Nazwa, którą to wypowiada, jest przy tym nazwą banku drzew, a nie naszą.
Frazę wymaganą opatruje on typem pozycji w schemacie głowy, a jedną z nich jest `subj`,
i pozycja schematu funkcją zdaniową nie jest:
`subj` stoi w Składnicy 170 razy na cząstce `się` —
`Wszystkich podejrzewa się o rozprowadzanie narkotyków.` — gdzie podmiotu nie ma,
a bywa też bezokolicznikiem i zdaniem z `że`
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)).
Słowo `podmiot` dokłada dopiero przekład w `harness/corpus.py`,
więc zgodność zmierzono z `subj`, a nie z podmiotem.

Werdykt mówi wobec tego nazwami składni szkolnej:
w `Kot to zwierzę.` podmiotem jest `Kot`, a orzecznikiem `zwierzę`.
Słownictwo szkolne z zakresami GFJP byłoby twierdzeniem,
którego nie stawia żadna gramatyka: `subj` jest pozycją schematu,
składnia tradycyjna orzeka odwrotnie,
a analiza dająca argument podmiotowy za kopulą opisuje zdania specyfikacyjne,
nie takie, które orzekają kategorię.
Przekład wykonuje `olski/werdykt.py`, czyli warstwa za pomiarem,
więc liczby wyżej biorą się sprzed niego i żadna z nich się nie rusza;
sąd, który on wykonuje, wypisuje `NAZWY_SZKOLNE` w `olski/subset/deklaracja.py`.
Struktura zostaje ta, którą wybrał pomiar, i pilnuje jej `tests/test_orzeczenie.py`,
pytając o streszczenie sprzed przekładu.

Grupa przed łącznikiem dostaje własną rolę,
a nie rolę rzeczownika orzekającego
([podrzędność.md](podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat)):
tamten symbol czyni zdaniem każdą swoją córkę,
więc grupa imienna pod nim byłaby pozycją ogólną, którą tamta sekcja odrzuca.
Orzecznikiem zgodnym nie jest z tego samego powodu, co tamten rzeczownik:
nie ma nad sobą czasownika, więc pozycji jego ramy nie zajmuje.
Rola ta nazywa się przez to osobno, a wydruk wypisuje pod nią `podmiot`.

```sh
python3 -m olski.check -c "Flaga to płat tkaniny określonego kształtu." --readings
```

```text
<text>: Flaga to płat tkaniny określonego kształtu.
        - orzecznik: płat tkaniny określonego kształtu, podmiot: Flaga
```

Zakup wynosi nad Składnicą kilkadziesiąt zdań schodzących z odrzucenia,
w większości przyjętych jednoznacznie,
a ceny nie ma żadnej: ani jedno zdanie przyjęte wcześniej nie traci jednoznaczności.
Nad prozą tego repozytorium zakup jest zerowy — ten rejestr pisze się bez łącznika,
bo olski go nie brał — a dwa zdania schodzą z odrzucenia do wieloznaczności,
i obu wieloznaczność daje przyłączenie wewnątrz grupy, a nie sam łącznik.

`To jest tanie.` wyprowadza się przy tym bez tej produkcji,
bo `to` jest w nim rzeczownikiem w podmiocie.

### Przy kopuli ten sam łącznik ma trzy szyki, a zgodność wybiera podmiot

`Był to nieforemny chłopak.`, `To są oczywistości.`, `Kot to jest zwierzę.` —
`to` stoi tu przy czasowniku, a nie między dwiema grupami.
Czasownikiem tym jest kopula, czyli ta, która żąda narzędnika,
i każdy z trzech szyków żąda jej tak samo:
ciało napisane na czasownik dowolny dałoby `Czytał to nieforemny chłopak.`
drugie czytanie, w którym `to` nie jest dopełnieniem, a polszczyzna ma tam jedno.
Samego narzędnika przy kopuli nie ma, bo rama jest w tej gramatyce stanem,
a nie zasobem, więc pozycja niewypełniona córki nie żąda.

Zgodność rozstrzyga tu stronę, której ciało bezczasownikowe nie miało czym rozstrzygnąć.
Kopula zgadza się z grupą stojącą za łącznikiem:
`Te książki to jest skarb.` wyprowadza się, a `Te książki to są skarb.` jest odrzucone,
więc podmiotem jest `skarb`.
Wypada to na tę samą stronę, którą wybrał pomiar wobec banku drzew
[wyżej](#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim),
a wypowiada ją forma, więc czytelnik sprawdza ją bez korpusu.

```sh
python3 -m olski.check -c "Kot to jest zwierzę." --readings
```

```text
<text>: Kot to jest zwierzę.
        - orzecznik: zwierzę, orzeczenie: jest, podmiot: Kot
```

Przeczenie wchodzi tymi ciałami samo, bo cząstka stoi w tej gramatyce przy czasowniku:
`Parser to nie jest kompilator.`, `Nie jest to kompilator.` i `To nie są oczywistości.`
wyprowadzają się bez ani jednej produkcji dopisanej po temu.
Zdanie bez czasownika ma za to cząstkę wypisaną w ciele: `Parser to nie kompilator.`

Zakup wynosi nad Składnicą pod złotą morfologią kilkadziesiąt zdań schodzących z odrzucenia,
z których większość czyta się zgodnie z drzewem wzorcowym,
a ceny nie ma żadnej: ani jedno zdanie przyjęte wcześniej nie traci jednoznaczności.
Pod morfologią żywą zakup jest mniejszy, a jednoznaczność traci kilka zdań.
Nad prozą tego repozytorium przybywa kilka zdań przyjętych, a dwa tracą jednoznaczność
na `to`, które stoi zarazem przydawką przy rzeczowniku za sobą:
`Jest to górne oszacowanie.` czyta się i łącznikiem, i z `to górne oszacowanie` w podmiocie.

Rozkład tego zakupu na dopisane ciała jest nierówny.
Szyk `Był to` i szyk `To są` biorą go niemal w całości,
ciało przeczenia bierze zdanie albo dwa,
a szyk `Kot to jest` nie rusza ani jednego zdania w żadnym z trzech przebiegów.
Wchodzi mimo to, i wchodzi po to, żeby `Parser to nie jest kompilator.` miało czym wejść:
przeczenie przy kopuli stoi w tym szyku, a nie w tamtych dwóch.
Konkurencji między ciałami nie ma przy tym żadnej —
ani jedno zdanie nie rusza się pod dwoma naraz —
więc żadna z tych liczb nie zasłania drugiej.

Wiersz `pred` kolejki blokerów stał setkami zatrzymań,
a po tym dopisaniu schodzi poniżej dwunastu wierszy, które
[corpus.md](../corpus.md#where-the-analyses-stop) drukuje.
Zdań przyjętych przybyło kilkadziesiąt, czyli wiersz spadł o więcej,
niż dopisanie przyjmuje: zdanie dalej odrzucone zatrzymuje się odtąd gdzie indziej.

Poza ciałami zostaje przeczenie bez czasownika i bez grupy przed łącznikiem:
`To nie kot.` jest odrzucone, gdzie `Parser to nie kompilator.` wyprowadza się.
Jest to osobne ciało i osobna liczba, której nikt nie policzył;
`todo/` trzyma ten przebieg.

## Predykatyw orzeka bez podmiotu i rządzi ramą czasownika

`Trzeba czytać dokumenty.`, `Widać granicę w odpowiedzi.`, `Nie wiadomo.` —
Morfeusz trzyma te słowa pod `pred`, czyli w jednym wierszu kolejki blokerów
([corpus.md](../corpus.md#where-the-analyses-stop)).
Orzekają one bez podmiotu i bez czasownika,
a rządzą tym, czym rządziłby czasownik,
więc rama i `wypełnienia` są tu te same, co u niego, tylko bez orzecznika zgodnego:
dopełnienie, bezokolicznik, zdanie z `że`, pytanie zależne i okolicznik
dochodzą bez ani jednego ciała osobnego, a dopełniacz negacji tą samą cechą,
którą przechodzi przez zdanie z czasownikiem
([wyżej](#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)).

Zdaniem składowym jest predykatyw wprost, a nie orzeczeniem pod nim.
Pod symbolem `grupa_orzeczenia` stanęłoby przy nim ciało z podmiotem,
więc `Programy trzeba czytać.` wychodziłoby zdaniem o podmiocie `Programy`,
choć `programy` jest tam biernikiem;
osoby ani liczby predykatyw nie niesie, więc unifikacja tego czytania nie odbiera.
Przy [kopuli opuszczonej](podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat)
zapadł ten sam wybór: rzeczownik orzekający stoi obok orzecznika, a nie jest nim.

Lista lematów jest zamknięta, a poza nią zostaje słowo,
którego czytanie konkurujące staje na czele zdania tego samego kształtu.
`to` takie czytanie ma, i to dwa razy:
grupa imienna bierze jego czytanie rzeczownikowe,
a jako `pred` jest ono łącznikiem, czyli konstrukcją osobną i wpuszczoną osobnym ciałem
([wyżej](#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim)).
Prowadzi ono ten wiersz kolejki,
a stoją w nim szyki, których łącznik nie bierze,
więc wyłączenie `to` z tej listy nie kosztuje jej ani jednego zdania.
Poza listą stoją tak samo `brak`, `czas`, `pora`, `żal`, `sposób` i `szkoda`:
każde z nich Morfeusz zna także jako rzeczownik,
a rzeczownik w mianowniku z dopełniaczem za sobą jest grupą imienną,
którą ta gramatyka wyprowadza.
`trudno` i `łatwo` nie stoją poza listą, tylko poza częścią mowy:
Morfeusz czyta je jako przysłówki,
choć bank drzew liczy `Trudno` właśnie w tym wierszu.

Ciała są dwa, bo zakup każdego jest osobną liczbą:
predykatyw z wypełnieniem i predykatyw sam, czyli `Nie wiadomo.` albo `Można.`
Zakup wynosi nad Składnicą kilkadziesiąt zdań, w większości po stronie ciała
z wypełnieniem, a ceny w czytaniach nie ma żadnej:
ani jedno zdanie przyjęte nie staje się wieloznaczne.
Jeden kształt zdania wychodzi pod obydwoma ciałami naraz inaczej niż pod każdym
osobno — `Rozumiem, że można, a nawet trzeba piętnować wszelkie formy nawracania
pod przymusem.` — bo jeden predykatyw stoi w nim sam, drugi z wypełnieniem,
a koordynuje je spójnik.
Olski nie czyta przy tym niezgodnie z drzewem wzorcowym ani jednego zdania nowo
przyjętego, a pojedyncze czyta uboższą listą ról niż drzewo.
Nad prozą tego repozytorium zakup jest liczony w kilku zdaniach przyjętych,
a wieloznacznych przenosi więcej niż przyjmuje.
Tę parę ciał dzieli z predykatywem forma nieosobowa czasownika
([niżej](#czasownik-nieosobowy-rządzi-ramą-swojego-lematu)),
więc zdjęcie któregoś z nich zabiera obie głowy naraz.

Szyki ma ta konstrukcja dwa: predykatyw stoi przed tym, czym rządzi,
a dopełnienie przed predykatywem
([niżej](#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu)).

### Forma bedzie składa czas przyszły także z predykatywem

`Trzeba będzie zmierzyć cenę.`
Forma `bedzie` składa ten czas z predykatywem tak samo,
jak składa go z bezokolicznikiem przy czasowniku
([wyżej](#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony)),
a jedna rzecz jest tu inna: głową zostaje predykatyw, bo rama należy do niego.

Gramatyka wpisuje temu ciału liczbę i osobę, zamiast brać je zmienną.
Predykatyw nie niesie ani jednej,
a cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc bez tych dwóch wartości `Trzeba będą zmierzyć cenę.` się wyprowadza.
Trzecia osoba pojedyncza jest jedyną, w której polszczyzna to zdanie pisze.

Ciało jest jedno i stawia `bedzie` za predykatywem.
`Będzie trzeba zmierzyć cenę.` polszczyzną jest i zostaje odrzucone:
szyk odwrotny jest osobnym ciałem i osobną liczbą,
której nikt nie policzył, a wpis trzyma `todo/`.

Zakup jest liczony w pojedynczych zdaniach banku drzew
i po stronie ceny nie ma nic: ani jedno zdanie przyjęte nie staje się
wieloznaczne, pod żadną z dwóch morfologii.
Nad prozą tego repozytorium nie rusza ani jednego werdyktu,
bo ten rejestr tej formy nie pisze.
Wiersz `bedzie` w kolejce blokerów po tej konstrukcji nie pustoszeje:
zostaje w nim garść zdań, a dlaczego, mówi
[corpus.md](../corpus.md#where-the-analyses-stop).

## Czasownik nieosobowy rządzi ramą swojego lematu

`Zgłoszono usterkę.`, `Nie zrobiono nic.`, `Podano do stołu.` —
Morfeusz trzyma te formy pod `imps`, czyli w jednym wierszu kolejki blokerów
([corpus.md](../corpus.md#where-the-analyses-stop)).
Orzekają one bez podmiotu tak samo jak predykatyw wyżej,
więc rolę i oba ciała zdania biorą te same co on,
a różnica jest jedna: ta forma jest czasownikiem,
więc ramę bierze z leksykonu swojego lematu
([walencja.md](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
a nie z jednej ramy wpisanej obok zamkniętej listy słów.
Widać ją na lemacie, o którym leksykon mówi, że biernika nie bierze:
`Pomagano usterkę.` jest odrzucone tam, gdzie `Zgłoszono usterkę.` się wyprowadza.

Zamkniętej listy ta konstrukcja nie ma i nie potrzebuje jej.
Predykatyw musi ją mieć, bo `pred` niesie słowa o konkurującym czytaniu —
`to` prowadzi ten wiersz i jest zarazem łącznikiem —
a formy `imps` takiego czytania nie mają:
z 321 form tego znacznika w banku drzew jedna, `pito`, ma czytanie spoza tej
części mowy, a każde inne drugie czytanie jest znów formą `imps`,
czyli jednym czytaniem, a nie dwoma
([subset.md](../subset.md#co-się-liczy-jako-jedno-odczytanie)).

Orzecznika zgodnego nie ma ani jedna z tych dwóch ram,
bo zgadza się on z podmiotem, którego takie zdanie nie ma:
`Zgłoszono tania.` nie jest niczym, tak samo jak `Trzeba wolni.`

Rola wspólna z predykatywem kosztuje pomiar różnicowy:
zdjęcie ciała zdania zabiera obie głowy naraz,
więc cenę każdej z nich mierzy się zdjęciem jej terminali.

Zakup rozkłada się na te dwa ciała tak samo jak przy predykatywie:
ciało z wypełnieniem zdejmuje nad Składnicą z listy odrzuconych kilkadziesiąt zdań,
a ciało samej formy — `Na północy i wschodzie strzelano.` — pojedyncze.
Obie morfologie oddają tyle samo i rozkładają to inaczej,
bo pod żywą więcej z tych zdań wychodzi wieloznacznych niż przyjętych.
Jedno zdanie wychodzi pod obydwoma ciałami naraz inaczej niż pod każdym osobno —
`Załadowano się na pięć barek i o zmierzchu wyruszono.` —
bo jedna forma stoi w nim sama, druga z wypełnieniem, a koordynuje je spójnik.

Cena wyszła zerowa w trzech korpusach i pod obiema morfologiami banku drzew,
a zero jest tu własnością konstrukcji, a nie wynikiem przebiegu:
formy `imps` nie brała przedtem żadna produkcja.
Niezgodnie z drzewem wzorcowym olski nie czyta ani jednego zdania nowo przyjętego,
a pojedyncze czyta uboższą listą ról niż drzewo.
Nad rejestrem ustaw zakup jest liczony w pojedynczych zdaniach i wszystkie
wychodzą wieloznaczne, a nad rozporządzeniem nie rusza się ani jeden werdykt,
choć i ono te formy pisze: zdania z nimi stoją tam także na czym innym.
Nad prozą tego repozytorium nie kupuje ani jednego zdania:
README pisze taką formę raz, a zdanie z nią stoi na formie żartu z nazwy
([roadmap.md](../roadmap.md#readme-jest-przyrządem-pomiarowym)).

Szyki ma ta konstrukcja dwa, te same co predykatyw:
forma stoi przed tym, czym rządzi, a dopełnienie przed formą
([niżej](#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu)).
Cząstki trybu przypuszczającego ta forma nie bierze:
`Zgłoszono by usterkę.` jest odrzucone, bo cząstkę bierze forma na -ł
i tylko ona ([wyżej](#tryb-przypuszczający-jest-jedną-cząstką)).

## Dopełnienie poprzedza głowę, która orzeka bez podmiotu

`Usterkę zgłoszono.`, `Biura przeniesiono do Krakowa.`, `Nic nie widać.`
Polszczyzna wysuwa dopełnienie przed predykatyw i przed formę nieosobową
tak samo jak przed czasownik, którego podmiot opuszcza — `Cenę liczymy.` —
więc jest to jedna pozycja, a obie głowy biorą ją tak samo,
jak biorą dwa ciała zdania wyżej.

Dopełnienie stoi w niej córką zdania, a nie pod `wypełnienia`:
tamten symbol stoi w ciele za głową i tylko tam,
bo rozwinięcie szyku po nim nie chodzi
([subset.md](../subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
a córka zdania dostaje miejsce na okolicznik wyliczone,
więc `Usterkę zgłoszono wczoraj.` wychodzi z okolicznikiem za głową.

Pozycja zdejmuje nad Składnicą z listy odrzuconych kilkadziesiąt zdań,
pod obiema morfologiami tyle samo, a rozkłada je inaczej:
pod złotą większość wychodzi przyjętych,
pod żywą przyjętych i wieloznacznych po połowie.
Nad prozą tego repozytorium przyjmuje parę zdań,
a kilkanaście przenosi z odrzuconych na wieloznaczne.
Ceny w jednoznaczności nie ma żadnej:
ani jedno zdanie przyjęte nie staje się wieloznaczne,
a czytań przybywa pojedynczym zdaniom już wieloznacznym.
Zgodność ról rośnie o wszystkie nowo przyjęte zdania poza pojedynczymi
([corpus.md](../corpus.md#agreement-which-matters-more-than-acceptance)).

Wysunięte jest tu samo dopełnienie, a nie każde wypełnienie,
i tyle też po tej pozycji zostaje [subset.md](../subset.md#what-it-does-not-cover-yet).

## Dopełnienie bezokolicznika wysuwa się przed formę osobową, która go bierze

```text
Prezes firmy może wyrzucić każdego pracownika, premier większości nie może ruszyć.
```

Zdanie to jest zdaniem Składnicy, a `premier` jest w nim podmiotem,
a `większości` dopełnieniem, którego żąda `ruszyć`.
Drugie czytanie ma tu grupę imienną `premier większości`
z przydawką dopełniaczową i bez dopełnienia w zdaniu,
a polszczyzna oba te czytania ma.
Gramatyka bez tej pozycji wyprowadza samo drugie,
czyli oddaje to zdanie werdyktem `valid` i przeczytane odwrotnie,
niż czyta je czytelnik, a tego zabrania
[kierunek toru](../roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście).

Pozycję niesie osobny symbol, a nie ciało `wypełnienia`,
i nie jest to wybór między dwoma zapisami jednej rzeczy:
symbol ten stoi w orzeczeniu za swoją głową i tylko tam,
więc dopełnienie stojące przed formą osobową nie ma się gdzie w nim znaleźć.
Wysunięte przed sam bezokolicznik byłoby zaś pozycją inną —
`nie może większości ruszyć` — której ta gramatyka nie ma.
Ramę czyta w tej pozycji bezokolicznik, a nie forma osobowa nad nim,
bo pozycję, którą to dopełnienie zajmuje, ma rama `ruszyć`, a nie rama `móc`;
jak to wypowiedziano cechami, mówi `olski/subset/zdanie.py`.
Przeczenie idzie drogą odwrotną: dopełniacza żąda cząstka stojąca przy formie
osobowej i żąda go
[ponad bezokolicznikiem](#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem).

Miejsce na okolicznik jest za bezokolicznikiem i nie ma go przed nim,
bo tyle gospodarzy ma okolicznik na torze zwykłym,
gdzie `wypełnienia` bezokolicznika przed swoją głowę nie sięgają.
Bez miejsca za bezokolicznikiem ta pozycja
[wybierałaby gospodarza przez przeoczenie](../subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).

Szerokość ramy domyślnej pozycja dziedziczy i nie pogarsza.
`Córka krawca chciała zejść.` dostaje przez nią czytanie z `krawca`
w roli dopełnienia, choć `zejść` dopełnienia nie bierze,
a to samo czytanie ma już `Córka chciała zejść krawca.`,
bo biernik daje każdemu czasownikowi
[rama domyślna](../walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej).
Zawężenie postawione w tej jednej pozycji nie naprawiłoby tego,
tylko odebrałoby jeden szyk temu, co gramatyka dopuszcza w drugim,
więc naprawa jest po stronie leksykonu.

Nad Składnicą pozycja rusza pod obiema morfologiami jedno zdanie,
i jest nim to, które ta sekcja otwiera:
zdań przyjętych ubywa o nie, a wieloznacznych przybywa o nie.
Z listy odrzuconych nie zdejmuje ani jednego zdania, czyli nie kupuje żadnego,
i nad prozą tego repozytorium nie rusza ani jednego werdyktu.
Pokrycie spada więc o jedno zdanie, a werdykt przestaje o nim kłamać;
tym samym rachunkiem wchodzą
[zaimki `kto` i `co`](podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz).
Gramatyka rośnie przy tym o kilkadziesiąt produkcji,
bo ciała bezokolicznika powstają po dwa na klasę walencyjną.

Szyk jest jeden, ten wypisany, bo cena każdego jest osobną liczbą,
a głowa jedna: forma osobowa, i co po tym zostaje,
wylicza [lista braków](../subset.md#what-it-does-not-cover-yet).
Zaimka względnego pozycja ta nie dosięga,
więc `Ustawa, którą organ gminy może wydać, jest tania.` jest dalej odrzucone
([podrzędność.md](podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
i to zdanie zostaje tym jednym, które kupuje cecha przeciągana
([design-notes.md](../design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
