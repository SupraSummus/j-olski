# Konstrukcje gramatyczne

Sekcja na konstrukcję: co gramatyka wpuszcza, jakim ciałem i ile to kosztowało.
Dokumentu nie czyta się od góry — czytelnik przebiega go do swojego wpisu.
Wylicza te konstrukcje [lista pokrycia](subset.md#what-the-grammar-covers),
a czym jest ważność i co mówi odrzucenie, wykłada [subset.md](subset.md).

## Czas przeszły żąda rodzaju od każdego szyku

Czas przeszły stoi w kolejce ze Składnicy
([corpus.md](corpus.md#where-the-analyses-stop)),
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
([niżej](#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)).
Bez wpisanej trzeciej osoby `Ja napisał program.` wyprowadza się,
bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza.

## Cząstka trybu stoi przy czasowniku albo w spójniku

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
([corpus.md](corpus.md#where-the-analyses-stop)),
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
Niezmiennika pilnuje `tests/test_subset.py`:
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
i jest to [nieciągłość](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
a nie brak pozycji.
Zostaje też aglutynant przy spójniku, czyli `żebym napisał`:
Morfeusz tnie ten napis na `żeby` i `m`,
a końcówka dochodzi w tej gramatyce do czasownika, przy którym stoi
([TODO.md](../TODO.md)).

## Forma `bedzie` orzeka sama albo składa czas przyszły złożony

Czas przyszły stoi w kolejce ze Składnicy
([corpus.md](corpus.md#where-the-analyses-stop)),
a niesie go tam jedna część mowy:
`bedzie` jest u Morfeusza osobną odmianą,
więc wiersz kolejki nazywa tę konstrukcję wprost.

Polszczyzna stawia tę formę w dwóch rolach i olski bierze obie.
Sama orzeka o podmiocie tak jak każda inna forma `być`:
`Cena będzie niska.`, `Testem będzie konkurs krajowy.`
Ramę bierze przy tym z leksykonu razem z resztą form tego lematu
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
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
bo cena każdej z nich ma być osobną liczbą
([CLAUDE.md](../CLAUDE.md#code)).
Obie kupują nad Składnicą po kilkanaście zdań przyjętych,
a większość tego, co zdejmują z odrzuconych, wychodzi wieloznaczna.
Pod złotą morfologią ani jedno zdanie banku drzew nie rusza się pod obiema naraz,
a pod żywą jedno, więc liczba jednej pozycji nie zależy od drugiej.
Razem oddają przeszło jedną trzecią tego, co obiecywał wiersz kolejki,
i jest to pierwszy pomiar, który oddał więcej, niż obiecywał przelicznik
[etapu 6](roadmap.md#etap-6-reszta-konstrukcji).
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
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)).
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
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Nad prozą tych dokumentów zdejmuje z odrzuconych kilkanaście zdań.

Pozycja przednia sięga początku zdania oraz miejsca tuż za znakiem,
a `Się myli.` ani `Cena rośnie, się nie liczy.` polszczyzną nie są,
więc cząstka żąda słowa przed sobą: opiera się o nie, a znak słowem nie jest.
Spójnik słowem jest i licencji udziela — `Cena rośnie, a się nie liczy.` —
bo taki napis bank drzew pisze:
`Po wielu latach sporów wiadomo już, że lądolód Grenlandii i przyrasta, i się topi`
oraz `żeby chór nie tylko istniał, ale się rozwijał`.
Warunek stoi w warstwie morfologicznej, tam gdzie warunek na formę przyimkową
zaimka ([niżej](#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)),
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
ani jedno ([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Nad prozą tych dokumentów zdejmuje z odrzuconych garść zdań —
`Komentarz mieszczący się w jednym wierszu zostaje w jednym wierszu.` —
a nad README nie rusza ani jednego werdyktu.

Ceną jest garstka odrzuceń i wszystkie stoją na jednym:
cząstka odgrodzona od swojego czasownika słowem,
czyli [nieciągłość](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
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
a pozycji między nimi nie ma ani jedno ciało; ruch trzyma [TODO.md](../TODO.md).

Gdzie cząstka może należeć do dwóch czasowników naraz, olski wypuszcza oba
odczytania. `Program otwierający się psuje.` czyta się i z `otwierający się`
w przydawce, i z `się psuje` w orzeczeniu, bo obie formy są w polszczyźnie
zwrotne, a wybiera między nimi znaczenie.
Tam, gdzie wybiera leksykon, wypuszcza jedno:
`Zebranie ma się odbyć.` ma odczytanie z `odbyć się`
i nie ma go z `mieć się`, bo `mieć się` bezokolicznika nie bierze
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)).
Zostaje przez to konkurencja przy czasowniku zwrotnym,
któremu Walenty bezokolicznik daje: `Nie daj się schwytać.`
wychodzi dwoma odczytaniami, bo `dać się` bierze bezokolicznik
i cząstka pasuje wtedy do obu ciał.
Płaci za to [przyrząd pomiarowy](roadmap.md#readme-jest-przyrządem-pomiarowym):
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
(`KOPULA` w `olski/lematy.py`);
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
[design-notes.md](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne).

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
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance) counts,
and admitting the bare order beside it
costs the sentence its uniqueness and keeps its honesty.

The subject takes no complements of its own in either order,
which is what stops `Zapisuje program ustawienia.` deriving
and stops every SVO sentence competing with a verb-initial reading of itself.

## Nothing above a coordination distributes into it

A coordination is one **conjunct**, a conjunction, and the rest,
and the grammar's symbols are named for it:
`człon_imienny` is a noun phrase with no coordination in it,
`grupa_imienna` is one that may have.
`grupa_imienna` is also where a relative clause attaches,
for a reason [below](#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)
that has nothing to do with coordination.
An adjective attaches inside a conjunct and never above the coordination,
so `nowe programy i pliki` is `[nowe programy] i [pliki]`
and never `nowe [programy i pliki]`.
That is a narrowing rather than a reading of Polish,
and what it buys is an agreement that can still fail.

A coordination has no gender of its own,
so an adjective scoping over the coordination
would be an adjective agreeing with nothing
and `nowa programy i pliki` would derive.
Refusing the wider attachment is what keeps that a rejection.

Wywód ten obowiązuje tam, gdzie obowiązuje zgodność.
Okolicznik wyrażony zdaniem dochodzi do całego ciągu zdań składowych,
bo nie zgadza się z niczym ani pod członem, ani nad ciągiem,
więc brak rodzaju u ciągu nic mu nie odbiera,
a czytania są dwa i oba polszczyzna ma
([niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).
Zawężenie zostaje przez to przy przydawce, czyli przy tym, co je uzasadnia.
Wyrażenie przyimkowe przyłącza się do całego ciągu z tego samego powodu,
z którego przyłącza się do niego okolicznik:
`pliki i katalogi w tym drzewie` mówi o obu członach,
gdzie to samo wyrażenie pod członem ostatnim mówi o samych katalogach,
a polszczyzna ma oba czytania, więc gramatyka ma oba ciała
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).
Ciąg przymiotnikowy dostaje tę pozycję tak samo,
choć zgodność niesie przez cały siebie:
wyrażenie przyimkowe żadnej cechy nie zmienia, więc zasięg zostaje dwojaki.

Pozycję tę zapisuje ciało ze spójnikiem,
a nie produkcja `grupa_imienna → grupa_imienna wyrażenie_przyimkowe`.
O zasięgu obie mówiłyby to samo.
Różni je liczba czytań: produkcja rekurencyjna dokłada drugie wyprowadzenie
każdej grupie bez koordynacji, a werdykt nie ma czym go odróżnić od pierwszego,
bo obu daje tego samego gospodarza.
Spójnik w ciele jest tym, co jedno od drugiego odróżnia,
więc ciała są dwa, po jednym na spójnik i na przecinek,
i tak samo dwa są nad ciągiem przymiotnikowym.

Ciąg dłuższy niż dwuczłonowy ma tę pozycję na każdym swoim poziomie,
bo ogonem ciągu jest `grupa_imienna`:
`A i B i C w drzewie` czyta wyrażenie przy samym `C`, przy `B i C`
oraz przy całej trójce, po jednym wyprowadzeniu na zasięg i bez nawiasowań ponad to.

Pozycja ta kosztowała mniej, niż zapowiadał precedens okolicznika zdaniowego.
Nad bankiem drzew nie rusza ani jednego werdyktu,
i tak samo pod morfologią złotą, jak pod żywą:
zdań przyjętych nie ubywa i nie przybywa.
Przebieg pod morfologią złotą mówi ponadto to, czego tamten nie liczy:
zgodność z drzewem wzorcowym zostaje ta sama,
a złote czytanie ocala się w tylu zdaniach wieloznacznych, w ilu ocalało przedtem.
Rusza się w nim jedno zdanie i nie werdyktem, tylko głębokością:
złote czytanie schodzi w nim poniżej granicy z `MAX_READINGS`.
Nad prozą tego repozytorium pozycja dokłada czytanie kilku zdaniom
już wieloznacznym i nie odbiera jednoznaczności żadnemu,
a czytania te są tymi, które polszczyzna nad nimi ma:
`Braki w leksykonie i braki w formach wylicza docs/roadmap.md.`
czyta odtąd `w formach` także przy obu brakach.
Kto chce liczby dzisiejszej, puszcza polecenia z
[corpus.md](corpus.md#fetching-it).

Dwa symbole zamiast jednego wybrano dla liczby czytań, a nie dla parsera.
Tablica Earleya bierze rekursję lewostronną,
co pilnuje test w `tests/test_subset.py`,
więc `grupa_imienna → grupa_imienna conj grupa_imienna`
dałoby się tu wpisać jedną produkcją w miejsce dwóch.
Powiedziałoby ono o zasięgu dokładnie to samo, bo zawężenie wyżej stoi na rodzaju,
którego ciąg nie ma, a nie na kształcie produkcji —
i wypuszczałoby ciąg tyloma wyprowadzeniami, ilu on nawiasowań dopuszcza:
ciąg trzech członów dwoma, czterech pięcioma, a siedmiu stu trzydziestoma dwoma,
gdzie te dwa symbole wypuszczają każdy z nich raz.
Są to wyprowadzenia jednej struktury, więc gramatyka płaciłaby tu tym,
czym płaci [gramatyka kategorialna](design-notes.md#kierunek-produkcja-się-rozwarstwia-a-podłoże-zostaje):
wieloznacznością pozorną, którą trzeba potem kwotować postacią normalną.
Ciąg siedmiu członów nie jest przy tym przypadkiem z brzegu:
tyle ma wyliczenie z rejestru ustaw, nad którym olski liczy czytań najwięcej
([ustawy.md](ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)),
i tamta liczba mówi, ile taki mnożnik znaczy przy zdaniu,
które wieloznaczność ma już z innego powodu.

## Spójnik skorelowany powtarza się przed każdym członem

`Ani parser nie rośnie, ani linter nie sprawdza.`,
`Ani parser, ani linter nie rośnie.`
Polszczyzna stawia tu spójnik dwa razy, po jednym przed każdym członem,
i przed drugim żąda przecinka,
gdzie koordynacja wyżej stawia go raz i między członami.
Ciało jest przez to trzecie na swoim poziomie, a nie drugą listą lematów.

Poziomy są trzy i każdy zmierzono osobno, bo cena każdego jest osobną liczbą.
Weszły dwa.
Poziom zdaniowy i imienny wyciągają razem kilka zdań banku drzew z odrzucenia,
a każde z nich zgadza się z drzewem wzorcowym;
nad prozą tego repozytorium kilka zdań dostaje czytanie, nie dostając
jednoznaczności, i są to zdania długie, wieloznaczne z innych powodów.
Jednoznaczności nie traci ani jedno zdanie w żadnym z tych dwóch przebiegów.
Poziom przymiotnikowy — `Plik jest ani nowy, ani duży.` —
nie kupuje ani jednego zdania w żadnym z nich, więc nie wchodzi.

Liczba idzie na poziomie imiennym z członu, a nie wartością `pl`,
i tym ten ciąg różni się od koordynacji zwykłej:
`Ani parser, ani linter nie rośnie.` orzeka w liczbie pojedynczej,
bo przeczenie rozdziela człony, zamiast je sumować,
a `Ani parsery, ani lintery nie rosną.` wychodzi z tego samego ciała mnogie,
bo mnogie są człony.

Z lematów zostało samo `ani`, choć polszczyzna powtarza tak również `i` oraz `czy`.
Oba zmierzono i oba wypadły, każde z innego powodu.

`i` wypada na napisie, którego polszczyzna nie ma.
Jego zakup jest sam w sobie dodatni: kilka zdań banku drzew dostaje czytanie,
a jednoznaczności nie traci żadne.
Terminal wpuszcza jednak spójnik na czoło członu, czyli wszędzie tam,
gdzie człon może się zacząć,
więc `Cena rośnie, i linter sprawdza tekst.` przestaje zatrzymywać analizę na `i`,
a przecinka przed tym spójnikiem polszczyzna nie stawia
([niżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
Zdanie zostaje odrzucone tak samo, a analiza idzie w nim dalej, niż napis pozwala,
i schodzi ono przy tym z wiersza `conj` kolejki blokerów
do wiersza zdań bez struktury nad całością
([corpus.md](corpus.md#where-the-analyses-stop)).

`czy` wypada na drugim wyprowadzeniu jednego kształtu.
Nad bankiem drzew nie rusza ani jednego zdania,
a nad prozą tego repozytorium daje czytanie dwóm,
tyle że tym samym czytaniem, którym pytanie zależne alternatywne
staje się ciągiem dwóch zdań oznajmujących:
`Pyta, czy rośnie, czy maleje.` dostaje trzecie czytanie tam,
gdzie ciąg pytań zależnych ma już swoje
([niżej](#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą)).
`ani` żadnej z tych dwóch rzeczy nie robi, bo nie licencjonuje go dziś nic.

Pary lematów gramatyka nie wymusza, bo terminal lematu nie wypuszcza,
a przy jednym lemacie na liście nie ma czego mieszać.
Lemat dopisany do niej wymusiłby parę dopiero ciałem na lemat,
czyli tyloma ciałami na poziom, ile lematów, i tej ceny nikt nie policzył.

## Przydawka koordynuje się i rozdziela rzeczownik tylko za nim

Przymiotniki przy jednym rzeczowniku polszczyzna spina spójnikiem i przecinkiem,
a wychodzą z tego dwie różne rzeczy.
Ciąg zgodny orzeka o jednej rzeczy kilka cech naraz:
`warstwy nowe i tanie` są warstwami, które są nowe i zarazem tanie.
Ciąg rozdzielny dzieli rzeczownik między swoje człony:
`warstwy trzecia i czwarta` są dwiema warstwami, a nie jedną.
Pierwszy stoi w obu szykach przydawki, drugi tylko za rzeczownikiem.

```sh
python3 -m olski.check -c "Nowy i tani parser zapisuje ustawienia.
Warstwy trzecia i czwarta pracują.
Warstwy trzecia, czwarta i piąta pracują.
Nowy i tania parser zapisuje ustawienia."
```

```text
<text>: valid     Nowy i tani parser zapisuje ustawienia.
                  jedno odczytanie
<text>: valid     Warstwy trzecia i czwarta pracują.
                  jedno odczytanie
<text>: rejected  Warstwy trzecia, czwarta i piąta pracują.
                  brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
<text>: rejected  Nowy i tania parser zapisuje ustawienia.
                  brak odczytania: analiza staje na „zapisuje”
```

Para symboli jest tu ta sama, którą ma grupa imienna i przymiotnikowa:
`przydawka` jest ciągiem, a `człon_przydawki` jednym członem,
i wybrano ją dla liczby czytań, tak samo jak tam
([wyżej](#nothing-above-a-coordination-distributes-into-it)).

Ciąg rozdzielny wypuszcza liczbę mnogą wartością, a nie zmienną wspólną z członem,
bo mnogi jest ciąg, a każdy przymiotnik w nim pojedynczy;
tym samym chwytem stoi koordynacja imienna i grupa liczebnikowa
([niżej](#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)).
Z ciągiem zgodnym się nie miesza, bo `warstwy nowe i trzecia i czwarta`
łączyłoby przydawkę orzekającą o wszystkich warstwach z dwiema, które je dzielą.

Przed rzeczownikiem ciąg rozdzielny nie staje, bo polszczyzna go tam nie stawia:
`trzecia i czwarta warstwy` nią nie jest, choć `warstwy trzecia i czwarta` jest.
Zatrzymuje go cecha, bo oba ciała są jednym symbolem.
Warunek nie rusza werdyktu ani jednego zdania Składnicy 180723
pod żadną z dwóch morfologii, a odbiera `Trzecia i czwarta warstwy pracują.`
czytanie, którego polszczyzna nie ma;
samego zdania nie odrzuca, bo wyprowadza się ono ciągiem imiennym.

Ciała są trzy — po jednym na znak koordynacji i trzecie na rozdział —
a cena każdego z nich jest osobną liczbą, wziętą sondą różnicową (`harness/ruch.py`).
Nad tym bankiem pod złotą morfologią czytanie dostaje kilkadziesiąt zdań,
z których blisko połowa wychodzi jednoznaczna,
a jednoznaczność traci kilka zdań przyjętych;
pod Morfeuszem zakup jest tego samego rzędu, a cena o zdanie wyższa.
Nad prozą tego repozytorium czytanie dostaje garść zdań, jedno traci jednoznaczność,
a nad README nie rusza się ani jedno
([roadmap.md](roadmap.md#readme-jest-przyrządem-pomiarowym)).
Ciało spójnikowe i przecinkowe kupują po kilkadziesiąt zdań,
a rozdzielne pojedyncze i nie odbiera jednoznaczności żadnemu.
Zgodność ról sprzedaje ciało przecinkowe i ono jedno:
nie mniej niż co piąte zdanie nowo przez nie przyjęte
olski czyta inaczej, niż czyta je bank drzew
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)),
a zdania nowo przyjęte przez ciało spójnikowe zgadzają się z bankiem co do jednego.

Ciała przecinkowego rodzina rozdzielna nie ma, bo jej ogonem jest ciąg zgodny
w liczbie pojedynczej i rozdział pada w takim ciągu raz,
więc `Warstwy trzecia, czwarta i piąta pracują.` jest odrzucone,
choć polszczyzna trzeci człon pisze właśnie przecinkiem;
ile to ciało kosztuje, trzyma [TODO.md](../TODO.md).

## Interpunkcja zdaniowa spina zdania, które już się wyprowadzają

Polszczyzna łączy dwa zdania spójnikiem, przecinkiem albo jednym i drugim naraz,
dwukropkiem wprowadza wyjaśnienie, a średnikiem rozdziela to, co spina treść.
Wiersz `interp` prowadzi kolejkę blokerów i liczy w niej tysiące zdań
([corpus.md](corpus.md#where-the-analyses-stop)).

Nowego kształtu zdania ta konstrukcja nie wymaga,
bo jej członami są zdania, które gramatyka wyprowadza i bez niej.
Wymaga natomiast trzech rozstrzygnięć, po jednym na znak.

**Dwukropek rozdziela zdanie wyżej niż przecinek.**
Przed dwukropkiem jest teza, a za nim całe jej wyjaśnienie,
więc `A, B: C.` polszczyzna czyta jako `(A, B): C`,
a produkcja należy przez to do zdania, a nie do zdania składowego.
Werdykt pokazuje ten podział streszczeniem na każde zdanie składowe,
tak samo jak przy koordynacji przecinkiem,
bo w jednym i w drugim zdanie składowe obsadza role własnym materiałem.

Jednoznaczności ta produkcja nie odbiera ani jednemu zdaniu,
a wynika to z gramatyki, nie z przebiegu:
dwukropka nie bierze żaden inny terminal.
Pilnuje tego zera `tests/test_subset.py`,
i pilnuje go warunkiem, a nie liczbą ciał:
symbole stojące za dwukropkiem mają być rozłączne,
więc napis wzięty jednym nie ma wyprowadzenia pozostałymi.

**Za dwukropkiem stoi zdanie, grupa imienna albo pytanie zależne.**
`Gramatyka ma dwie role: podmiot i dopełnienie.` wylicza za dwukropkiem to,
co zdanie przed nim nazwało liczbą albo terminem,
a `Sprawdzasz to jednym pytaniem: czy skreślona rzecz jest powiedziana gdzie
indziej?` stawia za nim pytanie, które zdanie przed dwukropkiem zapowiedziało.
Symbole te są rozłączne: grupa imienna zdaniem nie jest,
a zdanie składowe nie zaczyna się ani od `czy`,
ani od zaimka, który pozycji rzeczownej nie dostał
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).
Rolą jest cała ta grupa, tak samo jak przy wtrąceniu w nawiasie,
i tyle właśnie werdykt o niej mówi:
do którego składnika zdania ona się odnosi, gramatyka nie rozstrzyga,
i jest to ta sama odmowa, którą wydaje o członie bez czasownika
([niżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).

Obie pozycje kupują pojedyncze zdania tej prozy: konstrukcje są częste,
lecz zdania, które je niosą, potykają się jeszcze o co innego.
Pytanie zależne rozdziela przy tym dwa rejestry.
Nad bankiem drzew nie rusza ani jednego zdania, pod żadną z dwóch morfologii,
a nad prozą tego repozytorium przyjmuje kilka zdań i kilku dokłada czytanie:
jest to konstrukcja rejestru docelowego.
Kolejka blokerów nazwy jej nie podsuwa,
bo zdanie z takim dwukropkiem staje dopiero na swoim końcu
i wpada do wiersza zdań bez struktury nad całością,
czyli do tego jednego, który konstrukcji nie nazywa
([roadmap.md](roadmap.md#kolejka-blokerów-odsiewa-a-kolejność-dopisań-ustala-tekst)).
Jedno zdanie tej prozy przechodzi przy tym z przyjętego na wieloznaczne,
i jest to zysk, a nie cena:
`Rozdziela tę tradycję jedno pytanie: co autor podaje na wejściu.`
wyprowadzało się dotąd przez przyimkowe czytanie formy `co`,
czyli czytaniem, którego nikt nie ma,
a teraz stoi obok niego to, które ma czytelnik
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).

**Średnik rozdziela tak samo jak dwukropek i tak samo nie kosztuje nic.**
`Program zapisuje ustawienia; cena jest niska.` wyprowadza się ciałem
`wypowiedzenie → zdanie ; zdanie .`, czyli tym samym, tylko z drugim znakiem,
a cena jest i tu zerowa z gramatyki: średnika nie bierze żaden inny terminal.

Za tym znakiem stoi rejestr, a nie polszczyzna.
Średnik stoi tam, gdzie stanąłby przecinek albo kropka,
więc produkcja nie mówi nic, czego nie mówi dwukropkowa,
a przemawia za nią to, że ten rejestr średnika używa:
zdania z nim stoją w tych dokumentach i w ustawach.

**Myślnik rozdziela tym samym ciałem, a bierze dwa znaki z trzech.**
`Cena jest niska — gramatyka jest bezkontekstowa.` wychodzi tak samo jak zdanie
z dwukropkiem, a warunek na lemat bierze pauzę i półpauzę, czyli te dwa znaki,
którymi polszczyzna myślnik pisze.
Łącznika ten warunek nie bierze, bo łącznik spaja wewnątrz wyrazu — `UTF-8`,
`16-latków` — i to jest tu cena, a nie oszczędność:
zdanie, które myślnik pisze łącznikiem, zostaje odrzucone.

Drugiego znaku rozdzielającego zdanie nie bierze — ani dwóch średników, ani
średnika razem z dwukropkiem — bo `zdanie` żadnego z nich nie ma, więc rekurencji
nie ma czym zbudować. Granica ta jest wypowiedziana, a nie przeoczona, i zostaje
[subset.md](subset.md#what-it-does-not-cover-yet).
Najwięcej kosztuje ona przy myślniku, bo ten rejestr stawia go parą częściej
niż pojedynczo, a para obejmuje wtrącenie w środku zdania,
zamiast rozdzielać dwa zdania.

**Przecinek przed spójnikiem jest faktem o słowie.**
`Plany są niczym, ale planowanie jest wszystkim.` przecinka wymaga,
a `Program zapisuje ustawienia i linter sprawdza tekst.` nie bierze go wcale,
i rozstrzyga o tym sam spójnik, a nie miejsce, w którym pada.
Spójnik zdaniowy rozdziela się przez to na dwie klasy, które się nie zachodzą.
Klasa bez przecinka wyklucza ponadto cząstkę przeczącą, i to jest to samo
wykluczenie o jeden lemat szersze: Morfeusz czyta `nie` także jako spójnik,
a gramatyka ma dla tej formy pozycję przy czasowniku,
więc bez tego warunku `Zgodności ta pozycja nie ma i mieć nie może.`
wychodzi dwoma zdaniami spiętymi przez `nie`.
Warunek zabiera pojedyncze zdania tej prozy i każde z nich wyprowadzało się
właśnie tak, czyli czytaniem, którego polszczyzna nie ma.
Klasa z przecinkiem jest zamkniętą listą.
`zaś` i `jednak` na niej nie figurują, bo czoła swojego zdania nie zajmują:
polszczyzna stawia je za pierwszym wyrazem — `linter zaś sprawdza tekst` —
i jest to ten sam warunek, którym lista spójników okolicznikowych wyklucza `bowiem`
([niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).
Te trzy lematy bierze pozycja wewnątrz zdania i ona jedna
([niżej](#spójnik-wewnątrz-zdania-nie-dostaje-czoła-i-tym-stoi-przy-jednym-czytaniu)).
Lemat pominięty na liście zostaje przy pozycji bez przecinka,
więc pominięcie nie odbiera ani jednego zdania.

Podział ten odbiera zarazem napisy, których polszczyzna nie ma:
`Program zapisuje ustawienia ale linter sprawdza tekst.`,
`Plik jest nowy ale duży.` i `Skład czyli Morfeusz jest tani.`
czytania nie mają, bo polszczyzna stawia przed tymi spójnikami przecinek.
W drugą stronę odbiera przecinek postawiony tam, gdzie polszczyzna go nie stawia:
`Program zapisuje ustawienia, i linter sprawdza tekst.` czytania też nie ma.
Pozycji z przecinkiem grupa imienna i przymiotnikowa nie dostają,
bo `nie polszczyzny, a dziedziny` jest w nich elipsą, a nie ciągiem współrzędnym.
Dopowiedzenia z `czyli` żadna z tych dwóch pozycji nie daje,
bo dopowiedzenie odnosi się do składnika zdania,
a koordynacja zdaniowa łączy dwa zdania;
daje je człon bez czasownika
([niżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).
Zawężenie tych dwóch poziomów nie rusza ani jednego zdania w żadnym z trzech
rejestrów — ani nad Składnicą, ani nad README, ani nad ustawami —
więc płaci za nie sam werdykt, który przedtem kłamał pewnie.

Bez trzeciego warunku ta pozycja nie kupiłaby prawie nic,
a warunek ten pada na lemat przyimka, a nie na produkcję
([niżej](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)):
Morfeusz czyta `a` także jako przyimek,
więc każde `, a` w zdaniu wychodziło okolicznikiem wysuniętym drugiego składowego.

Poza gramatyką zostaje ciąg dwóch znaków rozdzielających, zapisany
[subset.md](subset.md#what-it-does-not-cover-yet).

## Człon bez czasownika stoi za spójnikiem, który go bierze

Ten rejestr dokumentuje podzbiór przez to, czego w nim nie ma,
więc `a nie` oraz `czyli` niosą setki zdań tej prozy,
a za tym spójnikiem stoi sam człon, bez powtórzonego czasownika:
`Milczenie obejmuje wybór, a nie zdanie.`

Konstrukcja jest elipsą, a nie koordynacją,
i rozstrzyga o tym pozycja, którą ten człon zajmuje:
żadnej. `wybór` jest dopełnieniem, a `zdanie` mówi, czym dopełnienie nie jest,
więc wpuszczone jako drugi człon ciągu imiennego wychodziłoby drugim dopełnieniem
i zdanie przyjęte mówiłoby o sobie nieprawdę.
Stoi więc obok zdania składowego, tam gdzie wtrącenie w nawiasie,
i tak samo nazywa się całym napisem
([niżej](#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).

**Czemu ten człon przeczy, gramatyka nie mówi.**
`Milczenie obejmuje wybór, a nie zdanie.` przeciwstawia dopełnieniu,
a `Wybór obejmuje milczenie, a nie zdanie.` przeciwstawia albo dopełnieniu,
albo podmiotowi, i rozstrzyga o tym znaczenie, a nie kształt.
Jest to ta sama odmowa, którą olski wydaje o przyłączeniu
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
z jedną różnicą: przyłączenie olski melduje jako wieloznaczność,
bo gramatyka ma tam kilka wyprowadzeń,
a tutaj wyprowadzenie jest jedno i milczy o tym, do czego człon się odnosi.
Werdykt nazywa więc rolę `elipsa` i wypisuje pod nią cały napis.

**Spójnik rozstrzyga, czy ten człon wchodzi, i lista jest węższa od zdaniowej.**
`a`, `ale`, `lecz`, `natomiast`, `tylko` i `czyli` biorą człon bez czasownika,
a `więc`, `zatem` i `toteż` go nie biorą,
bo `Cena jest niska, więc gramatyka.` polszczyzną nie jest.
Podział ten nie jest oszczędnością, tylko obietnicą podzbioru:
lista wzięta cała wyprowadzałaby napis, którego polszczyzna nie ma.
`czyli` stoi na liście po jednej stronie z `a nie`,
choć jedno przeczy, a drugie powtarza to samo innymi słowami:
różnicy tej gramatyka nie widzi, a rola nazywa kształt, nie funkcję.
Dopowiedzenie z `czyli` schodzi tym samym z kolejki w postaci,
w której ten rejestr pisze je najczęściej — na końcu zdania —
a postać wtrącona, `Skład, czyli Morfeusz, jest tani.`, zostaje
([subset.md](subset.md#what-it-does-not-cover-yet)).

**Wypełnienia są trzy i każde ma cenę osobną.**
Grupa imienna, grupa przymiotnikowa i wyrażenie przyimkowe wchodzą osobnymi
ciałami, bo cena każdego z nich ma być osobną liczbą, i te liczby się rozchodzą:
nad polską prozą tego repozytorium grupa imienna kupuje kilkadziesiąt zdań,
wyrażenie przyimkowe kilkadziesiąt, a grupa przymiotnikowa poniżej dziesięciu
i zabiera przy tym pojedyncze zdania przyjęte,
bo `droga` i `tania` są u Morfeusza naraz rzeczownikiem i przymiotnikiem.
Przysłówek stał w tej pętli i wypadł: kupował pojedyncze zdania,
czyli tyle, ile nie warto czterech ciał.

Osobno stoi cząstka przecząca, bo ciało z nią i ciało bez niej są dwoma ciałami,
a nie jednym z cząstką pominiętą, i to ona kupuje najwięcej — przeszło sto zdań.
Dopełniaczem nie rządzi i nie ma czym, bo czasownika pod nią nie ma,
a przypadek członu jest przypadkiem tego, czemu on przeczy.

**Przecinek zamykający ten człon jest drugim takim przecinkiem w gramatyce.**
`Granica pakietu jest tu rozstrzygnięciem, a nie przypadkiem, i pilnuje go test.`
biegnie za tym członem dalej, tak samo jak zdanie nadrzędne biegnie dalej
za zdaniem podrzędnym, więc ciało zamknięte przecinkiem dokłada ta sama funkcja
([niżej](#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim)).
Kupuje ono kilkanaście zdań i jest zarazem tym,
co czyni przecinek przed `i` w tym rejestrze poprawnym w dwóch miejscach,
a nie w jednym.

**Zakup zależy od rejestru o rząd wielkości.**
Nad polską prozą tego repozytorium ta konstrukcja kupuje przeszło sto
czterdzieści zdań, czyli kilka procent tego, co ta proza ma,
a nad bankiem drzew kilkadziesiąt, czyli promile.
Rozjazd nie mówi nic o gramatyce i wszystko o tym, kto pisze:
podzbiór dokumentuje się przez wykluczanie, a gazeta nie.
Mierzy to za jednym razem obie kolejki, o których mówi
[corpus.md](corpus.md#the-same-queue-over-prose).

## Spójnik wewnątrz zdania nie dostaje czoła i tym stoi przy jednym czytaniu

`Milczenie jest zatem wartością.`, `Reguła jest bowiem tania.`,
`Linter zaś sprawdza tekst.`
Polszczyzna stawia te spójniki wewnątrz zdania, za jego pierwszym wyrazem.
Trzy lematy tej listy czoła nie zajmują wcale,
i to o nich lista spójników okolicznikowych mówi, że pozycji dla nich nie ma
([niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).

Pozycją jest lista okoliczników i nic poza nią.
Wystarcza to, bo miejsce na okolicznik wylicza się za każdą córką zdania,
a nie przed pierwszą (`olski/precedencja.py`),
czyli ta lista mówi dokładnie tyle, ile polszczyzna o tym spójniku mówi.
Czoła zdania ten symbol nie dostaje, bo spójnik za przecinkiem
bierze już koordynacja
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)):
`Cena jest niska, więc gramatyka jest tania.` wychodzi tamtą produkcją.
Cena wychodzi zatem z gramatyki, a nie z przebiegu, tak samo jak przy dwukropku,
a zakup jest zmierzony: kilkadziesiąt zdań tej prozy.

Czoło całego zdania jest pozycją osobną
i ma [własną sekcję](#spójnik-na-czele-zdania-wiąże-je-z-poprzednim).

## Spójnik na czele zdania wiąże je z poprzednim

`I nikt tego nie zauważył.`, `Zatem milczenie jest wartością.`,
`Albo inaczej.`
Spójnik nie ma tu zdania przed sobą, a wiąże swoje zdanie z poprzednim.
Spójnik współrzędny i `zatem` stoją w tym miejscu jedną pozycją,
choć koordynacja rozdziela je na dwie klasy:
przed jednym żąda przecinka, przed drugim nie,
a czoło zdania nie ma przecinka przed czym postawić.

Ciało należy do zdania, a nie do zdania składowego.
Na poziomie składowego tej pozycji nie ma jak odgraniczyć od koordynacji —
`Cena jest niska, i gramatyka jest tania.` miałoby wtedy dwa wyprowadzenia,
bo spójnik zaczynałby człon drugi i zarazem go koordynował —
a zdanie ma czoło jedno, więc na tym poziomie rozgraniczenie nic nie kosztuje.

Lematy są listą dodatnią, a nie wykluczeniem, i rozstrzyga o tym cena obu.
Wykluczenie wzięłoby każdą formę, którą Morfeusz czyta jako spójnik,
a gramatyka daje kilku z nich pozycję własną:
`czy` podporządkowuje pytanie o rozstrzygnięcie
([niżej](#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą)),
`to` jest zaimkiem, a `jak` i `tymczasem` przysłówkiem.
Wpuszczone czołem, dają one drugie czytanie zdaniom,
które polszczyzna czyta raz — `Czy zmiana idzie w dobrą stronę?`,
`To samo wejście daje tę samą odpowiedź.`, `Tymczasem byk już był przy nim.` —
a klasa ta ma więcej lematów, niż widać nad jednym korpusem:
pod złotą morfologią wykluczenie nie kosztuje nic,
a pod żywą odbiera jednoznaczność kilkudziesięciu zdaniom banku drzew,
i kilkunastu nawet wtedy, gdy nazywa już trzy najczęstsze lematy,
gdzie lista dodatnia odbiera ją jednemu.
Rosłaby więc o każdy lemat, który ktoś zauważy,
i tym różni się od wykluczenia cząstki przeczącej,
które nazywa jeden lemat i jedną pozycję
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).

Lista schodzi się z trzech: spójniki, przed którymi polszczyzna stawia przecinek,
spójniki, które ten rejestr stawia wewnątrz zdania
([wyżej](#spójnik-wewnątrz-zdania-nie-dostaje-czoła-i-tym-stoi-przy-jednym-czytaniu)),
oraz `i` i `albo`, których żadna z tamtych nie ma.
`ani` do trzeciej nie należy, i jest to wynik, a nie przeoczenie:
bank drzew otwiera nim zdania spójnikiem skorelowanym,
a tę konstrukcję gramatyka bierze ciągiem
([wyżej](#spójnik-skorelowany-powtarza-się-przed-każdym-członem)),
więc czoło nie kupiłoby przy niej ani jednego zdania,
a odebrałoby jednoznaczność grupie `ani jedno`.
Terminal bierze przy tym obie części mowy spójnika,
bo `zatem` i `więc` na czele zdania dostają u Morfeusza `comp`,
a bank drzew nazywa je tam `conj`.

Pozycję podsunął wiersz `conj` kolejki blokerów, który prowadził ją czwarty,
a przeszło dwie trzecie jego zdań stało właśnie na czele
([corpus.md](corpus.md#where-the-analyses-stop)).
Nad bankiem drzew wychodzi z odrzucenia przeszło sto zdań,
pod jedną morfologią i pod drugą,
a kilkadziesiąt kolejnych dostaje czytanie, nie dostając jednoznaczności.
Z tych, które mają w drzewie wzorcowym rolę do porównania,
zgadza się z nim przeszło dziewięć na dziesięć, a jedno czyta się odwrotnie.
Nad prozą tego repozytorium przybywa kilkanaście zdań przyjętych.
Jednoznaczności nie traci przy tym pod złotą morfologią i nad tą prozą
ani jedno zdanie, a pod żywą jedno, bo tej pozycji nie bierze żaden inny kształt.

## Cząstka wchodzi obu gospodarzami, a w grupie nie nosi etykiety

`Program już zapisuje ustawienia.`, `Reguła obowiązuje także wtedy.`,
`Już program zapisuje ustawienia.` —
cząstka stoi w zdaniu tam, gdzie okolicznik przysłówkowy,
i tę pozycję gramatyka ma, odkąd ma
[przysłówek](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe).
Produkcje są przez to dwie i pisze je ta sama pętla, co tamte:
cząstka w liście okoliczników i cząstka na czele zdania składowego.

Przy zdaniu cząstka dostaje rolę osobną od przysłówka, choć pozycję ma tę samą,
bo werdykt nazywa rolę etykietą węzła:
`okolicznik_przysłówkowy: już` mówiłoby o zdaniu,
że ma okolicznik przysłówkowy, którego ono nie ma.

Drugim gospodarzem jest grupa imienna,
bo tam polszczyzna cząstkę stawia tak samo:
`Nawet ptaki przestały śpiewać.` mówi o ptakach, a nie o przestawaniu,
i widać to po zasięgu podmiotu, a nie po żadnej roli.
Ciałem jest `człon_imienny → part człon_imienny`, a osobę przepuszcza ono,
bo cząstka staje i przed zaimkiem: `Nawet ja zapisuję ustawienia.`

W grupie cząstka etykiety nie nosi, bo widać ją w napisie roli,
którą ta grupa zajmuje: podmiotem jest `Nawet ptaki`.
Rolę niesie przez to gospodarz jeden, tym samym prawem,
którym niesie ją [jeden gospodarz przysłówka](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe).

Wybór gospodarza nie jest tu jednak rozstrzygnięciem, i tym cząstka różni się
od przysłówka. Przysłówkowych gospodarzy rozdziela stopień, czyli cecha,
którą niesie tagset, a cząstki nie rozdziela ani cecha, ani lemat:
bank drzew stawia wewnątrz grupy każdy lemat tej listy, który w nim pada,
i ten sam lemat stawia przy zdaniu.
Udział wystąpień w grupie idzie od jednego na jedenaście przy `dopiero`
do co drugiego przy `niemal`,
a lematu stojącego wyłącznie w grupie nie ma ani jednego;
wyłącznie przy zdaniu stoją trzy i każdy pada mniej niż dziesięć razy.
Podział listy po lemacie jest więc wariantem odrzuconym:
bank drzew go nie potwierdza, a kryterium na tę pozycję nie jest leksykalne.
Zostaje wieloznaczność oddana czytelnikowi,
tak samo jak przy [wyrażeniu przyimkowym](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).

Cena wypada przez to inaczej niż przy przysłówku.
Nad Składnicą kilkadziesiąt zdań schodzi z przyjętych na wieloznaczne
pod jedną morfologią i pod drugą, a wyprowadzenie zyskuje kilka.
Zakupem jest prawda o zdaniu, a nie pokrycie:
wiersz zdań czytanych wbrew drzewu wzorcowemu maleje o blisko połowę
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)),
złote czytanie wraca kilku zdaniom wieloznacznym,
a zdania czytanego przy tym gospodarzu wbrew drzewu, a bez niego zgodnie z nim,
nie ma ani jednego.
Nad rejestrem ustaw jedno zdanie traci jednoznaczność,
nad korpusem audytowym jedno zyskuje wyprowadzenie,
a nad prozą tego repozytorium nie rusza się ani jedno.

Trudność nie leży przy tym w żadnej z tych pozycji, tylko w liście lematów.
Morfeusz trzyma pod `part` całą klasę cząstek naraz,
a w niej cztery słowa, które olski bierze albo wyklucza osobno:
`nie` przeczy, `się` stoi przy czasowniku zwrotnym,
`czy` otwiera pytanie o rozstrzygnięcie,
a `by` żąda trybu przypuszczającego, którego ta gramatyka nie ma
([subset.md](subset.md#what-it-does-not-cover-yet)).
Lista jest więc zamknięta, a kryterium na wejście jedno:
cząstka ma nie mieć czytania, które gramatyka bierze już gdzie indziej,
i tym samym warunkiem stoją obok siebie dwie klasy
[spójnika zdaniowego](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają).
Poza listą zostaje przez to `to`, które ma ponadto własną pozycję,
a tej olski nie ma ([subset.md](subset.md#what-it-does-not-cover-yet)).

## Interpunkcja obejmująca: cudzysłów wchodzi w grupę, a nawias staje obok zdania

Znak rozdzielający spina dwa zdania, a obejmujący bierze to, co stoi w środku,
i te dwie pary są w tym rejestrze dwiema różnymi konstrukcjami.
Cudzysłów obejmuje tytuł — `„Zasady techniki prawodawczej”` —
albo napis przytoczony, o którym zdanie orzeka: `„B”`, `„nie”`.
Tytuł odmienia się i jest grupą imienną, przytoczenie nie odmienia się wcale,
więc pozycje są dwie.
Nawias obejmuje dopowiedzenie obok zdania,
którym w tej prozie jest nazwa dokumentu: `(docs/subset.md)`, `(niżej)`.

**Cudzysłów przepuszcza grupę imienną całą.**
Produkcja obejmuje grupę i wypuszcza jej przypadek, liczbę oraz rodzaj bez zmiany,
bo polszczyzna odmienia to, co cudzysłów obejmuje, wedle roli, w której grupa stanęła:
`Same „Zasady techniki prawodawczej” stoją poza tą sumą.` ma w środku mianownik,
a `Ustawa jest przepisem „Zasad techniki prawodawczej”.` dopełniacz.
Napis niedomknięty wyprowadzenia nie ma.
Cudzysłowa maszynowego — `"Zasady techniki prawodawczej"` — produkcja nie bierze,
bo ten jeden znak nie jest żadnym z tych dwóch,
a za napis, którego polszczyzna nie pisze, płaci autor
([pisanie-po-olsku.md](pisanie-po-olsku.md#kto-płaci-za-odrzucone-zdanie));
werdykt nazywa mu wtedy parę, którą ten rejestr pisze
([subset.md](subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).
Wnętrzem tej produkcji jest sama grupa imienna,
więc `„to nie zdanie”` zostaje na zewnątrz.

**Napis przytoczony grupą imienną nie jest i dostaje czytanie nieodmienne.**
Cudzysłów obejmuje w tej prozie także `„B”`, `„nie”` i `„Daj”`,
czyli napisy, o których zdanie orzeka, a nie słowa, którymi orzeka.
Polszczyzna ich nie odmienia, więc produkcja nie ma tu czego przepuszczać,
a napis dostaje rzeczownik nieodmienny, ten sam, który dostaje wersalik
([warstwa-leksykalna.md](warstwa-leksykalna.md#wersalik-bez-czytania-jest-tym-samym-rzeczownikiem-nieodmiennym)).
Nazwa litery zapisana słownie wyprowadza się bez tej pozycji,
bo `wu` i `ce` słownik daje jako rzeczowniki nieodmienne,
a litera zapisana znakiem jest u słownika skrótem — `B` pod lematem `bajt` —
i skrótów ta gramatyka nie ma.

Licencji udziela cudzysłów po obu stronach napisu,
tak samo jak przyimek udziela jej formie przyimkowej
([niżej](#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)).
Napis niedomknięty nie jest więc przytoczeniem,
a wnętrze dłuższe niż jedno słowo zostaje przy grupie.

Napis z czytaniem rzeczownikowym zostaje przy grupie, choćby był jednym słowem,
i jest to warunek, a nie oszczędność:
czytanie nieodmienne spełnia każde żądanie przypadku, a niesie rodzaj nijaki,
więc `Program zapisuje „ustawienia”.` dostałoby drugie czytanie,
w którym napis jest podmiotem,
a `„Reguła” jest tania.` przestałoby się wyprowadzać.
Warunek pyta o czytania, a nie o ich użyteczność,
więc `Znam „szybko”.` pada dalej:
słownik daje tej formie wołacz rzeczownika `szybka`,
którym dopełnienia nikt nie zbuduje, a przytoczenia on już nie dopuszcza.

Cena jest ta sama, którą płaci wersalik, a do niej dochodzi jedna osobna:
zdanie jednowyrazowe jest w cudzysłowie tym samym napisem co forma przytoczona,
więc `Znam „Płacę”.` wychodzi jednym czytaniem,
w którym mowa niezależna jest rzeczownikiem.

Nad prozą tego repozytorium pozycja nie domyka ani jednego zdania:
przytoczeń jest w niej kilkanaście, a każde zdanie z nimi niesie obok
konstrukcje, których olski nie ma, więc pozycja zdejmuje jeden powód odrzucenia,
a nie całe odrzucenie.
Zakup jest przez to odłożony, a nie zmierzony na zero,
tak samo jak przy drugiej pozycji nawiasu niżej.

**Nawias dochodzi w każdym napisie do jednego gospodarza.**
`Zdanie stoi (docs/subset.md).` wychodzi jednym czytaniem,
a nie tyloma, ile gospodarzy ma w zdaniu wyrażenie przyimkowe,
i nie jest to wybór przyłączenia, którego olski nie robi
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)).
Nawias niczego w zdaniu nie wypełnia,
więc gdziekolwiek by dochodził, role zdania są te same,
a różnicy między dwoma miejscami nie ma czym wypowiedzieć —
gdzie wyrażenie przyimkowe zmienia to, o czym zdanie mówi, a nawias nie zmienia nic.
Wtrącenie jest przy tym rolą, którą werdykt nazywa,
i jest rolą całym napisem: przysłówek w środku nawiasu nie jest okolicznikiem zdania,
więc zejście po role zatrzymuje się na wtrąceniu tak samo jak na zdaniu podrzędnym.

Wnętrzem nawiasu jest grupa imienna albo przysłówek.
Pozycje są dwie i obie stoją tam, gdzie nawias zamyka zdanie składowe
albo zdanie względne odgrodzone przecinkami:
`Reguła, która rozstrzyga (niżej), jest tania.` wychodzi jednym czytaniem.

**Druga pozycja stoi w ciele zamykanym przecinkiem i tylko w nim.**
Ciała zdania względnego są dwa, bo przecinek zamykający polszczyzna stawia wtedy,
gdy zdanie nadrzędne biegnie dalej
([niżej](#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
a w tym z przecinkiem nawias stoi przed nim,
gdzie przyłączony do zdania nadrzędnego stanąłby za nim, czyli dałby inny napis.
Ciało bez przecinka kończy się tam, gdzie kończy się zdanie nadrzędne,
i tam pozycji nie potrzeba, bo pierwsza z dwóch obsługuje ten napis w całości:
`Program zapisuje regułę, która rozstrzyga (niżej).` wychodzi jednym czytaniem,
w którym nawias dochodzi do zdania nadrzędnego.
Druga pozycja dopisana i tam nie kupiłaby ani jednego zdania,
a dołożyłaby temu napisowi czytanie,
i nierówność ciał jest przez to oszczędnością, a nie ceną.

Nad Składnicą ta pozycja nie rusza ani jednego zdania,
pod złotą morfologią ani pod żywą,
bo proza prasowa nawiasu wewnątrz zdania względnego nie pisze.
Pisze go dokumentacja tego repozytorium, i pisze kilka razy,
a przyjętego zdania ta pozycja jej nie kupiła:
zakup jest odłożony tak samo jak przy przytoczeniu wyżej.

Na zewnątrz zostaje nawias w środku grupy imiennej —
`grupa imienna (ta z dopełniaczem) stoi` —
i jest to w tej prozie mniejszość:
nawias stoi w niej zwykle przed kropką albo przecinkiem,
czyli tam, gdzie kończy się zdanie, jego składowe albo zdanie względne w nim,
co liczy `grep -oP '\)[.,]' proza/docs.txt | wc -l` wobec wszystkich nawiasów tego pliku.

## Zaimek rzeczowny nie rządzi dopełniaczem

Morfeusz daje formom paradygmatu `ten` czytanie rzeczownikowe obok
przymiotnikowego: `tego` jest dopełniaczem przymiotnika `ten`
i dopełniaczem zaimka `to`, a `tym` narzędnikiem jednego i drugiego.
Produkcja, która daje głowie grupy imiennej dopełniacz po niej,
bierze oba: `parser tego podzbioru` jest przymiotnikiem przy rzeczowniku,
a drugi raz zaimkiem, który rządzi rzeczownikiem.
Te dwa drzewa mają różny kształt,
więc [są dwoma odczytaniami](subset.md#co-się-liczy-jako-jedno-odczytanie),
a nie jednym jak para lematów.
Bez warunku niżej `Celem jest parser tego podzbioru.` wychodzi dwoma czytaniami
o identycznym streszczeniu ról.

Drugiego z nich polszczyzna nie ma.
Zaimek rzeczowny stoi za przyimkiem i przy czasowniku — `do tego`, `tego nie wiem` —
a dopełniacza po sobie nie bierze.
Warunek obejmuje więc każdą głowę, która rządzi dopełniaczem,
i mówi tyle: taka głowa nie jest zaimkiem rzeczownym.
W grupie imiennej produkcji z nią jest cztery,
bo pod głową może stać jeszcze przymiotnik, wyrażenie przyimkowe albo jedno i drugie.
Dwie następne są w [grupie, którą polszczyzna wysuwa przed zdanie względne
razem z zaimkiem](#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka):
przydawką dopełniaczową jest tam sam zaimek względny,
więc bez warunku `Polszczyzna, której nikt nie napisał, jest podzbiorem.`
wychodzi drugim czytaniem, w którym `której nikt` jest taką grupą.
Gdzie indziej czytanie zostaje, bo gdzie indziej jest tym, czym w polszczyźnie jest.

Paradygmat `ten` jest częścią tej klasy, a nie całą klasą.
`nikt`, `kto`, `nic`, `coś` i `ktoś` mają u Morfeusza czytanie jedno
i jest ono rzeczownikowe,
więc pod nimi nie stoją dwa czytania tej samej formy,
a mimo to produkcja z dopełniaczem po głowie bierze je za głowę:
bez warunku `Wtedy nikt nas nie zauważy.` wychodzi drugim czytaniem,
w którym `nikt nas` jest grupą imienną.
Przy paradygmacie `ten` takie czytanie zdejmuje także złota morfologia,
bo anotator wybiera jedno czytanie formy.
Tutaj wybierać nie ma z czego, więc czytanie zostaje po obu morfologiach,
a warunek jest jedynym miejscem, w którym ono ginie.

Wpisem na tej liście jest lemat, bo zaimka od rzeczownika nie rozdziela w słowniku
ani znacznik, ani cecha, ani kwalifikator.
Lista jest przez to zamknięta i starzeje się o każdy zaimek,
którego nikt do niej nie dopisze.
Starzenie kosztuje wieloznaczność, a nie zdanie odrzucone:
lemat dopisany odbiera czytanie i żadnego nie dodaje.

Jest to pierwszy warunek ujemny w tej gramatyce i lemat jest tym,
na czym wolno go postawić.
Cechy takiego warunku mieć nie mogą:
unifikacja jest przecięciem, a przecięcie negacji nie zna,
więc żądanie „nie bądź w narzędniku” nie jest żądaniem,
które da się postawić środowisku cech.
Lemat leży poza unifikacją, bo jest osobnym testem w `bierze`
z `olski/grammar.py`, więc negacja jest tam tym samym testem odwróconym.
Symetria jest zatem z `lemmas`, a nie z cechami,
i to samo rozstrzygnęło, czym jest klasa domyślna
[leksykonu walencyjnego](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej):
bierze ona każdą formę, której lematów leksykon nie wymienia,
i jest to drugi warunek ujemny, jaki ta gramatyka stawia.

Te dwa warunki różnią się zasięgiem.
Wykluczenie zaimka mówi „tym słowem nie bądź”, więc pyta o jedno czytanie formy;
klasa domyślna mówi „tą formą nie bądź”, więc pyta o wszystkie jej lematy naraz.
Klasa domyślna bez tego zasięgu przepuszcza formę, którą miała zatrzymać,
a co jej tą drogą przeszło, mówi
[sekcja o leksykonie](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej).
Wykluczenia leksykalne zostają przy czytaniu, bo o czytaniu mówią.
Czytanie i forma nie są tym samym słowem:
`nie` jest u Morfeusza cząstką `nie` i formą `on`,
`lecz` spójnikiem i rozkaźnikiem od `leczyć`,
a `pnie` grupą imienną od `pień` obok formy od `piąć`.
Pomiar tej różnicy nie widzi:
zamiana ich wszystkich na zasięg formy
nie rusza nad Składnicą ani jednego zdania pod żadną morfologią.
Zobaczy ją pierwsze wykluczenie, które taką formę trafi,
bo zasięg formy odbierze jej czytanie, o którym to wykluczenie nic nie mówi.

Warunek i kupuje, i płaci, a pomiar mówi ile.
Nad Składnicą pod Morfeuszem
[podnosi on liczbę zdań przyjętych](corpus.md#what-morphological-ambiguity-costs)
o kilkadziesiąt, a odrzuca kilka.
Pod złotą morfologią widać obie strony tej wymiany:
kilka zdań przechodzi z wieloznacznych na przyjęte i każde z nich zgadza się
z drzewem wzorcowym, a kilku warunek zabiera jedyne czytanie, jakie miały,
i były to czytania, którym drzewo wzorcowe przeczyło albo których nie potwierdzało.
Każde z tych zdań stało na jednej frazie, której polszczyzna nie ma —
`to` z dopełniaczem pod sobą tam, gdzie tym dopełniaczem rządzi czasownik —
i tamten dokument jedno z nich cytuje.
Liczby dzisiejsze wydają dwa przebiegi `harness.pomiar`, z warunkiem i bez niego:
sonda różnicowa zdejmuje produkcje, a to jest warunek w terminalu.

Rozłożona na produkcje cena wypada po obu stronach inaczej.
W grupie imiennej warunek coś znaczy w każdym z czterech ciał:
zdjęty z dwóch, pod których głową stoi jeszcze przymiotnik,
oddaje pod morfologią żywą wieloznaczność
`Wprowadźmy do tego trupiego świata poprawkę.`
i podwaja liczbę czytań kilku dłuższym zdaniom banku drzew,
a pod złotą nie rusza tam nic.
W dwóch produkcjach wysunięcia nie rusza nad Składnicą liczby czytań
ani jednego zdania pod żadną z dwóch morfologii,
więc jest w nich z wywodu, a wywód jest ten sam:
przydawka dopełniaczowa jest w obu miejscach tą samą przydawką.

## Rozdzielające `a` nie jest przyimkiem tego rejestru

Morfeusz daje formie `a` cztery czytania i jednym z nich jest przyimek rządzący
mianownikiem — ten z `dwa bilety a pięć złotych`, czyli z ceny za sztukę.
Wyrażenie przyimkowe olskiego bierze przyimek wraz z przypadkiem, którym on rządzi,
więc bez warunku niżej `a` otwiera je tak samo jak `w` albo `z`,
a grupa imienna po nim stoi w mianowniku,
czyli w tym samym przypadku, w którym stoi podmiot zdania po spójniku.
Każde `, a` w zdaniu wychodzi przez to okolicznikiem wysuniętym drugiego składowego:
`Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego.`
miało przed tym warunkiem trzy czytania i każde z nich niosło
`„a podmiot jednego” → „jest”`.

Polszczyzna tego zdania tak nie czyta.
Warunek obejmuje oba wyrażenia przyimkowe tej gramatyki — zwykłe i to,
które wysunęło zaimek względny — i mówi tyle: przyimek tego wyrażenia nie jest `a`.
Warunek ujemny postawiony na lemacie po to,
żeby odebrać czytanie, którego polszczyzna w tym miejscu nie ma,
stoi w tej gramatyce także wyżej
([zaimek rzeczowny](#zaimek-rzeczowny-nie-rządzi-dopełniaczem)).
Tańsza z dwóch dróg pyta właśnie o to, co produkcja licencjonuje,
a nie o to, co słownik oferuje
([roadmap.md](roadmap.md#etap-3-czytania-których-polszczyzna-nie-ma)).

Kryterium ogólniejsze wygląda tu na tańsze: żądanie „rządź jednym z pozostałych
sześciu przypadków” powiedziałoby to samo o każdym słowie naraz.
Nie powiedziałoby, i mówi to sam słownik.
Mianownikiem rządzą w nim także `jak`, `jako`, `niż`, `co` i `aniżeli`,
czyli wykładniki porównania,
i wszystkie pięć padają w prozie, którą to repozytorium czyta —
nad README, siedmioma ustawami i korpusem audytowym razem
`niż`, `co` i `jako` po przeszło setce razy, `jak` kilkadziesiąt,
`aniżeli` kilka, przy kilkuset formach `a`.
Kryterium na przypadek zabrałoby więc razem z rozdzielającym `a` i te pięć.

Cena jest zerowa i jest to wynik pomiaru, a nie założenie.
Pod złotą morfologią przebieg nad Składnicą nie rusza ani jednego zdania z 13 035,
bo tam każda forma ma jedno czytanie wybrane przez człowieka
i `a` nie jest w tym korpusie przyimkiem ani razu.
Pod żywą morfologią, czyli nad prozą README, warunek odbiera jedno zdanie —
to wypisane wyżej — i oddaje je z powrotem przecinek przed spójnikiem
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
z trzema czytaniami w miejsce trzech.
Liczba czytań wychodzi więc ta sama przed i po,
a różnią się one tym, że tamte trzy niosły okolicznik, którego zdanie nie ma,
a te trzy niosą podmiot, który ono ma.

## Podrzędność i koordynacja dzielą przecinek, a rozdziela je produkcja

Zdanie podrzędne otwiera w polszczyźnie ten sam znak,
którym koordynacja łączy dwa zdania składowe,
więc gramatyka, która ma przecinek i nie ma podrzędności,
nie odrzuca zdania podrzędnego — czyta je jako współrzędne.
`Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.`
wychodziło jednym czytaniem, w którym `które zadania własne gminy`
jest podmiotem drugiego zdania,
i pomiar nad rejestrem ustaw liczył to zdanie jako pokrycie
([ustawy.md](ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa)).
Jedno czytanie, pewne siebie i błędne, jest gorsze niż odmowa.

Rozdziela je miejsce przecinka w produkcji, a nie warunek obok niej.
Koordynacja ma przecinek na poziomie zdania i powtarza tam własny symbol:
`zdanie → zdanie_składowe , zdanie`.
Podrzędność wciąga przecinek do konstytuentu, który sama tworzy,
więc `zdanie_podrzędne → , że zdanie` jest jednym konstytuentem wraz z przecinkiem,
a `zdanie` się w nim nie powtarza.
Po tym rozpoznaje ciąg współrzędny werdykt (`_koordynuje` w `olski/parse.py`)
i po tym samym rozpoznaje go sonda, która przecinek zdejmuje.
Samo powtórzenie symbolu im nie wystarcza, bo nad ciągiem stoi jeszcze
[okolicznik zdaniowy](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania),
który do całego ciągu dochodzi i własny symbol powtarza tak samo.
Rozdziela je znak: koordynacja spina członów spójnikiem albo przecinkiem
stojącym w ciele słowem, a określenie jest grupą,
która swój przecinek niesie w sobie.

Wywód ten stoi tutaj, a nie w [subset.md](subset.md), bo orzeka o konstrukcjach
pod sobą, a nie o każdej produkcji, którą ktoś dopisze:
przecinek dzielą te podrzędności, które ta sekcja wylicza,
i każda z nich wnosi go własnym ciałem.

### Przecinek zamykający należy do zdania podrzędnego, a nie do spójnika za nim

Przecinek zamykający stawia polszczyzna wtedy, gdy zdanie nadrzędne biegnie dalej,
a biegnie ono dalej także spójnikiem:
`Dokument mówi, że cena jest niska, i liczy cenę.`
Parę ciał — jedno zamknięte przecinkiem, drugie nie —
ma przez to każde zdanie podrzędne tej gramatyki.

`A, i B` dalej się nie wyprowadza i to jest tu cała ostrożność.
Przecinek przed `i` nie jest w polszczyźnie znakiem koordynacji zdaniowej
i lista spójników przecinkowych go nie obejmuje
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
więc pozycja dochodzi zdaniu podrzędnemu, a nie spójnikowi:
znak wchodzi tam, gdzie polszczyzna go stawia, i nigdzie poza tym.

Kupuje to nad bankiem drzew kilkadziesiąt zdań, a nad prozą tego repozytorium kilka.
Liczba ta zależy jednak od tego, co jeszcze w gramatyce stoi, i to jest tu ciekawsze
od niej samej: zdjęta z gramatyki bez przydawki imiesłowowej ta sama pozycja
kupowała pojedyncze zdania, bo zdanie, które jej potrzebuje, potykało się wtedy
o imiesłów.
Cena pozycji pojedynczej jest więc różnicą wobec gramatyki dzisiejszej,
a nie stałą, którą raz się zapisuje
([pisanie-po-olsku.md](pisanie-po-olsku.md#zasłanianie-działa-w-obie-strony)).

### Zdanie z `że` jest pozycją ramy, a nie konstrukcją obok niej

Czym jest zdanie podrzędne dopełnieniowe dla czasownika,
tym jest dopełnienie i bezokolicznik:
pozycją ramy, którą [leksykon walencyjny](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)
czasownikowi daje albo odbiera.
Wchodzi więc jako czwarta pozycja ramy domyślnej,
a nie jako produkcja dopisana do każdego szyku zdania z osobna,
i tak samo jak tamte trzy dochodzi do czasownika przez `wypełnienia`.
Kosztuje to jedno słowo w `RAMA_DOMYŚLNA` i jedno ciało w `olski/subset/zdanie.py`.

Spójnikiem jest `że` i nic poza nim,
choć Morfeusz daje klasę `comp` także formom `gdy`, `jeśli` i `aby`.
Tamte otwierają okolicznik zdania, a nie dopełnienie,
więc wpuszczone tą produkcją stanęłyby w pozycji, której nie zajmują,
a czasownikowi, który zdania podrzędnego nie bierze,
dałyby czytanie, w którym je bierze.
Własną pozycję dostały [niżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)
i jest nią okolicznik zdania, czyli dokładnie ta, którą zajmują.

Pod złotą morfologią przebieg nad Składnicą rusza 26 zdań i wszystkie w tę samą stronę:
siedemnaście przechodzi z odrzucenia w jednoznaczność, dziewięć w wieloznaczność,
a żadne zdanie już przyjęte nie traci werdyktu ani nie zyskuje drugiego czytania.
Wśród nowo przyjętych zgodność z drzewem wzorcowym rośnie o dwanaście,
jedno zdanie wychodzi zgodne częściowo, cztery nie mają w nim roli do porównania,
a o ani jedno odwrócenie roli zgodność nie rośnie
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Liczba 26 rośnie przy tym z czasem przeszłym, a nie z podrzędnością:
zdanie podrzędne stoi w tym korpusie najczęściej przy czasowniku w tym czasie,
więc konstrukcja zmierzona przed nim była mierzona przy części swoich zdań
([wyżej](#czas-przeszły-żąda-rodzaju-od-każdego-szyku)).

```text
Mieszkańcy grożą, że zablokują ulice.
Dodaje, że zwolnienia są nieuniknione.
```

### Okolicznik wyrażony zdaniem nie jest pozycją ramy i dochodzi do zdania

Zdania z `że` żąda czasownik, a zdania z `gdy` nie bierze żaden.

```text
Program zapisuje ustawienia, gdy linter sprawdza tekst.
Gdy linter sprawdza tekst, program zapisuje ustawienia.
```

Zdanie z `gdy` mówi, kiedy zachodzi to, o czym mówi zdanie obok niego,
i mówi to o całym tym zdaniu, a nie o jego orzeczeniu,
więc dochodzi tam, gdzie dochodzi wyrażenie przyimkowe wysunięte przed zdanie:
do zdania składowego, a nie do symbolu `wypełnienia`.
Dochodzi zarazem do całego ciągu współrzędnego, a nie do samego składowego w nim,
i te dwa czytania są dwoma zdaniami:
`Dwoisz się i troisz, aby rozwiązać problemy.` mówi o obu członach naraz,
a `Mieszkał z ojcem i nie chciał, żeby ktoś wiedział.` o samym drugim.
Bez pozycji nad ciągiem gramatyka ma samo czytanie drugie,
czyli wybiera przez przeoczenie
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)),
a nad zdaniami takimi jak pierwsze wybiera odwrotnie, niż czyta czytelnik.

Ciąg jest tu żądany cechą, bo nad zdaniem o jednym członie
oba ciała dają ten sam napis dwoma kształtami.
Cena stoi przez to w jednoznaczności, a nie w pokryciu:
nad Składnicą traci ją garść zdań przyjętych,
nad prozą tego repozytorium pojedyncze zdanie,
a z odrzuconych do przyjętych nie przechodzi ani jedno.
Bez żądania ciągu cena jest kilkakrotnie wyższa,
bo dochodzi do niej każde zdanie o jednym członie.
Bank drzew tego wyboru nie rozstrzyga:
oba czytania mają rolę okolicznika o tej samej rozpiętości,
a porównanie ról pyta o rozpiętości
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)),
więc różnicę widać w werdykcie po nazwie gospodarza i nie widać jej w pomiarze.
Tym jednym różni się ta konstrukcja od [zdania z `że`](#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej),
a reszta jest w obu ta sama: przecinek należy do konstytuentu, który spójnik tworzy,
a nie do produkcji nad nim.

Przecinek stoi przy tym po tej stronie, po której stoi zdanie nadrzędne,
więc ciała są dwa, a wiąże je z pozycją cecha.

Spójnik jest warunkiem na lemat i lista jest zamknięta.
Poza nią zostaje `bowiem`, bo polszczyzna stawia je za pierwszym wyrazem zdania,
oraz `więc`, bo zdania nie podporządkowuje, tylko dokłada skutek:
`Program zapisuje ustawienia, więc linter sprawdza tekst.`
jest dwoma zdaniami spiętymi spójnikiem po przecinku
([wyżej](#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)).
Zdanie pod spójnikiem z tej listy stoi w trybie oznajmującym,
a `aby`, `żeby`, `by`, `gdyby` i `jakby` żądają przypuszczającego
i biorą przez to ciała osobne
([wyżej](#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)).

Listy są przez to dwie, a nie jedna, bo wysunięcie jest faktem o słowie:
`Zostaję w domu, bo pada.` jest polszczyzną, a `Bo pada, zostaję w domu.` nie jest,
i tak samo dzieli się `gdyż` od `ponieważ`, choć oba mówią o przyczynie.
Fakt ten skład trzyma o dwóch z tych lematów
(`olski/skład/spójniki.py`),
i [TODO.md](../TODO.md) trzyma ruch, którym oba kierunki czytałyby jeden leksykon,
tak jak czytają jeden leksykon walencyjny.
Sam podział ma przy tym świadka zmierzonego:
nad Składnicą `gdyż` nie otwiera ani jednego zdania,
tak samo jak `bowiem`, którego gramatyka nie bierze wcale,
a `gdy` i `jeśli` otwierają dwie piąte swoich wystąpień i ponad połowę.
Liczby dla `bo` i dla `albowiem` mierzą co innego niż tamte
i sonda mówi to o sobie sama:
zdanie zaczynające się od tych spójników odsyła w tym korpusie do zdania przed nim,
zamiast być zdaniem podrzędnym wysuniętym przed swoje nadrzędne.
Dwa wpisy listy wysuwanej nie mają w tym korpusie świadka wcale:
`dopóki` i `póki` stoją w nim raz albo dwa i ani razu na czele zdania,
więc na tej liście stoją z samego znaczenia, a nie z pomiaru.

Okolicznik ten jest rolą, którą werdykt nazywa, tak samo jak przysłówek
([niżej](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe)),
i jest zarazem zdaniem podrzędnym, czym żadna inna rola nie jest.
Symbol stojący i wśród ról, i wśród zdań podrzędnych
rozstrzyga o dwóch rzeczach naraz, i rozstrzyga je przeciwnie:
streszczenie nazywa ten okolicznik całym napisem, bo jest on rolą,
a w środek jego nie zagląda, bo podmiot spod spójnika jest podmiotem tamtego zdania.
Zejście po role zatrzymuje się więc na takim węźle, a nie przed nim
(`Node.find` oraz `_pierwsza_rola` w `olski/parse.py`),
a kosztuje to jeden warunek w obu zejściach po role.

Widać po tym, do którego zdania okolicznik doszedł:

```text
Pomiar mówi, że autor pisze, ponieważ tekst jest gotowy.
```

Czytania są dwa i oba polszczyzna nad tym zdaniem ma,
a streszczenie rozdziela je nazwaniem tej roli albo przemilczeniem jej:
okolicznik doszedł do zdania streszczanego albo do tego, które stoi pod `że`.

### Przysłówek względny otwiera okolicznik i nie określa zdania

Ten sam okolicznik otwiera `gdzie`, a Morfeusz daje mu `adv`, a nie `comp`,
więc pozycji spójnika nie dosięga i bierze osobne ciało.

```text
Wchodzi w roadmap.md, gdzie każdy etap ma kryterium wyjścia.
Gdzie cząstka może należeć do dwóch czasowników, olski wypuszcza oba odczytania.
```

Miejsca są dwa, tak samo jak przy spójniku wysuwanym,
i o drugim z nich rozstrzyga pomiar, a nie wywód:
zdanie wysunięte znaczy tu `wszędzie tam, gdzie` i o miejsce nie pyta,
więc wygląda na kształt, którego ta proza nie pisze, a pisze go.
Ciało samo za zdaniem odbiera przez to czytanie napisom, które w niej stoją.

**Okolicznikiem zdania oznajmującego ta forma nie bywa i pozycji tej nie ma.**
Wpuszczona tam daje każdemu zdaniu z `gdzie` czytanie ciągu współrzędnego,
w którym przysłówek określa człon drugi,
i jest to nad `Program zapisuje ustawienia, gdzie linter sprawdza tekst.`
czytanie jedyne, a polszczyzna go nie ma.
Wykluczenie stoi więc na terminalu okolicznika i weszło razem z tym ciałem,
tak samo jak wykluczenie zaimka rzeczownego weszło razem ze swoimi czołami
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).

Cena tego wykluczenia jest wypisana, bo mierzy się ją osobno:
bez niego nad prozą tego repozytorium zdań przyjętych jednoznacznie
jest o kilka mniej, a wieloznacznych o kilkanaście więcej.
Zabiera ono za to `gdzie indziej`, czyli parę, w której ta forma określa
drugi przysłówek, więc para ta dostaje własne ciało
i bez niego wykluczenie odbierałoby zdania, które ta proza pisze.
Pytania o miejsce to wykluczenie zabiera i zdania takiego olski nie ma:
rolą wysuniętą jest tam okolicznik, a czoła pytań wysuwają podmiot,
dopełnienie albo orzecznik, więc pytanie o miejsce zostaje
[subset.md](subset.md#what-it-does-not-cover-yet).

### Zaimek względny nie jest przymiotnikiem przy rzeczowniku

Morfeusz daje `który` znacznik `adj`, czyli ten sam, co `nowy` i `polski`,
i to jest cały powód, dla którego `które zadania własne gminy`
wychodziło grupą imienną.
Przymiotnikiem przy rzeczowniku ten wyraz w polszczyźnie nie bywa nigdy:
zaczyna zdanie względne albo pytanie, a przydawki nie tworzy.
Warunek jest więc taki sam jak przy [zaimku rzeczownym](#zaimek-rzeczowny-nie-rządzi-dopełniaczem)
i pada w tym samym miejscu — na terminalu, a nie w słowniku:
przydawka i orzecznik tego lematu nie biorą, a bierze go czoło zdania względnego.

Zdjęcie tego czytania jest tym, co odbiera czytanie współrzędne,
i odbiera je bez produkcji, która by go zabraniała:
`które zadania własne gminy` przestaje być grupą imienną,
więc nie ma czym być podmiotem zdania po przecinku.
Tańsza z dwóch dróg do czytania, którego polszczyzna nie ma,
prowadzi tędy, a nie przez wykluczenie w `admissible`
([roadmap.md](roadmap.md#etap-3-czytania-których-polszczyzna-nie-ma)).

Cena była ceną pozycji, której gramatyka nie miała, a którą ten warunek nazwał.
Pozycję tę stawia pytanie, więc `Który aktor robi na tobie największe wrażenie?`
oraz pytanie zależne `określają, które zadania` wyprowadzają się, każde raz.

### Zdanie względne niesie liczbę i rodzaj swojego zaimka

Przypadek zaimka względnego mówi o zdaniu podrzędnym,
a liczba i rodzaj o poprzedniku:
`który` bierze przypadek z roli, którą w zdaniu podrzędnym zajmuje,
a zgadza się w liczbie i rodzaju z tym, co określa.
Zdanie względne wypuszcza więc te dwie cechy do góry,
a produkcja, która je przyłącza, żąda ich od grupy imiennej.

Kupuje to przyłączenie, którego gramatyka nie musi wybierać:

```text
Zbiór tekstów, które są polskie, jest podzbiorem.
Zbiór tekstu, który jest polski, jest podzbiorem.
```

Pierwsze ma jedno czytanie, bo `które` jest w liczbie mnogiej
i do `Zbiór` przyłączyć się nie ma jak.
Drugie ma dwa, bo `Zbiór` i `tekstu` są oba męskie i pojedyncze,
i są to dwa czytania, które ma także czytelnik.
Jest to ta sama postawa co przy
[wyrażeniu przyimkowym](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera) —
gramatyka przyłączenia nie wybiera —
z tą różnicą, że tutaj większość wyborów odbiera zgodność,
czyli to samo, czym odbiera je czytelnik.

Zdanie względne dochodzi przy tym do symbolu `grupa_imienna`, a nie `człon_imienny`,
bo na poziomie członu produkcja rekurencyjna dałaby jednej strukturze
dwa wyprowadzenia, a te [są dwoma odczytaniami](subset.md#co-się-liczy-jako-jedno-odczytanie).
Wyżej ten wybór nie istnieje,
bo `człon_imienny` bierze wszystko, co grupa niesie przed nim.
Kosztuje to symetrię w koordynacji:
człon prawy zdanie względne unieść może, a lewy nie,
więc `pliki, które rosną, i katalogi` nie ma wyprowadzenia.

Zdanie względne wypełnia trzy role, bo tylu ten rejestr używa,
a każda z nich jest tą, którą zaimek zabiera zdaniu podrzędnemu:
podmiot (`reguła, która rozstrzyga`),
dopełnienie (`polszczyzna, którą ktoś napisał`)
i wyrażenie przyimkowe (`język, o którym to repozytorium jest`).
Ostatnia sięga najdalej i jest jedną produkcją,
bo za wysuniętym wyrażeniem przyimkowym stoi zdanie składowe całe.
Podmiot za wysuniętym dopełnieniem stoi przy tym po czasowniku i przed nim,
choć zdanie główne ma ten szyk tylko w pierwszej wersji:
`które ktoś napisał` jest w polszczyźnie zwyczajne, a `Teksty ktoś napisał` nie,
i różni je to, że zaimek względny wysuwa polszczyzna zawsze,
a dopełnienie z wyboru.

**Dopełnienie stoi przed czasownikiem także tam, gdzie czołem jest podmiot.**
`reguła, która tekst sprawdza` i `ktoś, kto go nie używa` są w tym rejestrze
tak samo zwyczajne jak szyk z dopełnieniem za czasownikiem,
a zdanie główne ma oba od początku,
więc gramatyka bez tego ciała mówiła o szyku rzecz nieprawdziwą:
że zależy on od tego, czy któraś rola stoi wysunięta.

Ciało jest drugie i bierze osobny symbol orzeczenia,
a nie szyk dopisany do córek zdania.
Rozstrzyga o tym duplikat: córki zdania głównego przestawia
[deklaracja szyku](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk),
więc szyk dopisany tam dałby `Reguła tekst sprawdza.` drugie wyprowadzenie
tego samego kształtu, czyli [drugie odczytanie](subset.md#co-się-liczy-jako-jedno-odczytanie).
Przed czasownik wychodzi przy tym samo dopełnienie, a nie całe wypełnienie ramy,
i to też jest warunek, a nie oszczędność:
wypełnienie niesie okolicznik w swoich ciałach, a okolicznik stawia przed
czasownikiem także deklaracja szyku, więc `którzy na niej stoją`
miałoby dwa wyprowadzenia jednego kształtu.

Nad prozą tego repozytorium ciało to daje czytanie kilkunastu zdaniom,
a jednoznacznych przybywa wśród nich kilka.
Ceną jest para zdań tracących jednoznaczność,
czyli takich, w których grupa imienna przed czasownikiem
konkuruje wewnątrz zdania względnego z przydawką albo z podmiotem.
Ani jedno zdanie nie traci przy tym czytania,
bo szyku tego nie bierze żaden inny kształt.

Wysunięte na czoło jest przy tym nie sam zaimek,
ale cała grupa, w której on stoi.
Pozycje ma ona dwie i obie niesie rejestr ustaw.
Pod przyimkiem niesie ją `ustawy, na podstawie której jest ono wydawane`,
zdanie „Zasad techniki prawodawczej”,
gdzie `której` jest dopełniaczem przy `podstawie`.
Bez przyimka grupa stoi w podmiocie i w dopełnieniu zdania składowego:
`ustawa, której przepisy obowiązują`.

Grupa niesie liczbę i rodzaj dwa razy, i to jest cała jej trudność.
Przypadka żąda od niej przyimek albo rola, w której stanęła,
a wypuszcza go jej rzeczownik.
Ten sam rzeczownik wypuszcza liczbę i rodzaj,
bo z głową grupy zgadza się orzeczenie zdania składowego.
Zaimek wypuszcza tę samą parę drugi raz i osobno,
bo w niej zgadza się z nim poprzednik zdania względnego.
Jedna para na obie zgodności wygląda poprawnie i odwraca każdą z nich:
`w wyniku której` ma głowę męską przy żeńskim poprzedniku,
a `której autorzy piszą` mnogą przy pojedynczym.
Para wzięta z zaimka przyjmuje przez to `Ustawa, której autorzy pisze`,
a para wzięta z głowy `Ustawy, której autorzy piszą` —
w obie strony werdykt pewny siebie i błędny.

Kształty grupy są dwa: rzeczownik z zaimkiem za sobą (`na podstawie której`)
i ten sam rzeczownik z zaimkiem przed sobą (`o którego zdaniu`).
Sam zaimek (`o którym`, `która rozstrzyga`) jest obok tych dwóch
czołem drugim, w tych samych dwóch pozycjach.
Czoła są dwa, a nie jedno obejmujące oba kształty,
i rozstrzyga o tym pomiar, a nie polszczyzna:
pod jednym czołem cena pozycji bez przyimka nie byłaby osobną liczbą,
a wywód stoi w `olski/subset/podrzędne.py` przy czołach obu rodzin.

Podmiotu zdanie z wysuniętym dopełnieniem nie żąda,
bo deklaracje są dwie — z podmiotem i bez niego —
tak samo jak ma je zdanie główne.
Jedno czytanie ma przez to `Dyrektor wymienia imprezy, które zorganizował.`
i jedno `Dyrektor wymienia imprezy, które on zorganizował.`.
Ciała pisze obu rodzinom czół jedna funkcja, więc to samo dostało pytanie:
`Które zadania wykonuje?` wyprowadza się obok `Które zadania gmina wykonuje?`.

Zakupem są pod złotą morfologią cztery zdania Składnicy wyjęte z odrzucenia
i piąte, które z odrzucenia przechodzi w wieloznaczność;
pod żywą jest ich odpowiednio trzy i dwa.
Role trzech z tych czterech zgadzają się z drzewem wzorcowym,
a czwarte — `Złodzieje kradną drogi sprzęt, który potem sprzedają w cenie złomu.` —
olski czyta z okolicznikiem przy zdaniu nadrzędnym zamiast przy względnym,
bo miejsce na okolicznik jest w ciele jedno,
a to zdanie stawia okolicznik po obu stronach czasownika.

Płacą za to zdania, w których zaimek jest zarazem mianownikiem i biernikiem,
a czasownik biernik bierze, bo daje mu go rama domyślna:
`Wywód, który za nią stał, stoi dalej.` z prozy README jest takim zdaniem,
a nad Składnicą pod żywą morfologią traci jednoznaczność jedno.
Pod złotą morfologią nie traci jej ani jedno,
bo anotator wybrał tam jedno czytanie na token,
a nad rejestrem ustaw nie rusza się ani cena, ani zakup.
Tą samą drogą wyprowadza się `Ustawa, której przepisy obowiązuje`,
i dlatego parę cech czoła pokazuje wyżej głowa męskoosobowa,
której mianownik różni się od biernika.

Pod żywą morfologią jedno z tych zdań wchodzi przy tym
nie tym czytaniem, o które szło.
`Myślę o tym człowieku, który mnie podglądał.` wychodzi
pytaniem zależnym w pozycji, którą każdemu czasownikowi daje
[rama domyślna](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej),
a nie zdaniem względnym:
zdanie względne z wysuniętym podmiotem stawia dopełnienie za czasownikiem,
więc `mnie podglądał` nie ma w nim gdzie stanąć.

Wysunięte dopełnienie sięga ponadto do formy osobowej i nie dalej,
bo ciała wypisane wyżej mają w środku czasownik zdania składowego,
więc dopełnienie należące do bezokolicznika pod nim nie ma się skąd wziąć:
`Ustawa, którą organ gminy może wydać, jest tania.` jest odrzucone.
Zdania tego kształtu nie ma jednak ani jedno zdanie rejestru ustaw,
co pokazuje `grep -P 'któr\w+ [^.]*\b(może|mogą|ma|mają)\b [^.]*\w+ć'`
nad `proza/ustawy/`, więc konstrukcja ta jest wyczytana z gramatyki,
a nie z korpusu.

Po ten brak sięgnęłaby cecha przeciągana, czyli luka zamiast wypisanych ciał,
a ile ona kupuje i dlaczego nie weszła, mierzy
[design-notes.md](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze).

### Dopełniacz z ramy wysuwa się na czoło, a celownik nie

Czoło dopełnienia brało dopełniacz przy przeczeniu i tylko przy nim,
bo tam rządzi nim negacja.
Dopełniaczem rządzi jednak i rama, więc zdanie względne o czasowniku,
który go żąda, nie miało czytania:

```text
Cena, której żądamy, jest niska.
Pozycja, której brakuje, jest droga.
Kogo dotyczy zmiana?
```

Pozycja jest trzecim ciałem tej samej trójki szyków,
a różni ją od dwóch pozostałych to, że przeczenia nie ogłasza.
Nie ma czego: dopełniacz negacji wchodzi w miejsce biernika
i tam kończy się jego zasięg
([wyżej](#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)),
a `nie brakuje ceny` stoi w dopełniaczu tak samo jak `brakuje ceny`.
Tam, gdzie czasownik bierze oba dopełniacze, jeden napis dostaje przez to
dwa wyprowadzenia i jedno czytanie, bo kształt mają ten sam
([subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie)).

Zakupem nad bankiem drzew jest pod złotą morfologią jedno zdanie
wyjęte z odrzucenia, a jest nim `Nie wiem, czego się obawia.`
Złote czytanie w nim ocalało.
Jednoznaczności nie traci pod tą morfologią ani jedno zdanie.
Pod żywą traci ją to samo zdanie
wraz z `Zadałem sobie pytanie, ile mogę zaryzykować, czego najbardziej się boję.`,
i jest to ta sama zamiana, którą liczy
[corpus.md](corpus.md#what-morphological-ambiguity-costs):
oba stały tam na `czego` przeczytanym jako przysłówek,
czyli na czytaniu, którego polszczyzna w tym zdaniu nie ma,
a teraz stoją obok czytania prawdziwego.

Nad prozą tego repozytorium konstrukcja przyjmuje kilka zdań
i kilku dalszym daje pierwsze czytanie.
Jednoznaczność traci przy tym `jest zdaniem, którego makieta potrzebuje.`,
bo zdanie to miało czytanie z grupą `którego makieta` w podmiocie,
a dostaje obok niego czytanie z dopełnieniem `którego`.
Polszczyzna ma oba, więc wieloznaczność jest tu prawdziwa.

Celownika ta pozycja nie bierze i rozstrzyga o tym pomiar.
Nad bankiem drzew nie kupuje on ani jednego zdania w żadnej z dwóch morfologii,
a pod żywą odbiera jednoznaczność jednemu ponad te dwa wyżej.
Nad prozą tego repozytorium daje czytanie jednemu zdaniu
i jest to czytanie nieprawdziwe:
`szew, którym to zdanie wychodzi poza podzbiór` z tego dokumentu
niesie narzędnik, którego olski bez przyimka nie bierze
([subset.md](subset.md#what-it-does-not-cover-yet)),
a celownik na czole czyta ten napis jako dopełnienie `wychodzić`.
Bezokolicznik z tej samej listy
([warstwa-leksykalna.md](warstwa-leksykalna.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu))
zostaje na zewnątrz z powodu ogólniejszego:
wypełnienie inne niż dopełnienie na czoło się nie wysuwa.

### Pytanie o rozstrzygnięcie podporządkowuje spójnikiem, a nie rolą

Pytanie o rolę wysuwa tę rolę na czoło, a pytanie o rozstrzygnięcie
nie wysuwa niczego: podporządkowuje je spójnik, a zdanie pod nim jest całe.

```text
Czy program zapisuje ustawienia?
Pyta, czy go to dotyczy.
Pyta, kto płaci i czy to działa.
```

Czoło jest przez to osobnym ciałem, a nie lematem dopisanym do listy zaimków,
i nie przechodzi przez funkcję wypisującą szyki reszty zdania.
Pozycję ramy niesie ono tak samo jak pozostałe czoła,
więc ciąg pytań pod jednym czasownikiem miesza te dwa kształty bez osobnej pozycji.

Ten sam lemat bierze zarazem koordynacja bez przecinka,
gdzie `czy` znaczy `albo`, a rozdziela te dwa użycia materiał pod spójnikiem:
koordynacja stawia po nim człon, a to ciało zdanie.
Napisu wspólnego oba nie mają, więc drugiego czytania to ciało nie dokłada nikomu,
i tym różni się ono od czół zaimkowych,
które weszły razem z wykluczeniem
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).

### Czoło niesie etykietę roli, którą zajmuje, a werdyktu nie rusza

Wysunięty konstytuent zajmuje w zdaniu składowym rolę:
`która` w `reguła, która rozstrzyga` jest podmiotem,
a `którą` w `polszczyzna, którą napisał autor` dopełnieniem.
`_wysunięta_rola` w `olski/subset/podrzędne.py` stawia nad nim `podmiot` albo `dopełnienie`,
czyli tę samą etykietę, którą nosi rola wypełniona na swoim miejscu.

Bez tej etykiety olski wyprowadza te zdania dokładnie tak, jak czyta je bank drzew,
a rozdanie ról wychodzi z nich o jedną rolę uboższe,
więc porównanie ról nie ma go z czym zestawić;
ile zdań na tym stało, liczy
[corpus.md](corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).

Etykieta jest osobnym konstytuentem nad czołem, a nie cechą na nim,
bo rolę czyta się z etykiety węzła (`Node.find` w `olski/parse.py`),
i stąd bierze się trudność tej pozycji.
Symbol wpisany do ciała wpuszcza tam wszystkie swoje produkcje,
a `podmiot → grupa_imienna` wpuszcza w to miejsce każdą grupę imienną w mianowniku:
`reguła, ta reguła rozstrzyga` byłoby wtedy zdaniem względnym,
a `Który aktor robi wrażenie.` zdaniem oznajmującym o takim podmiocie,
czyli wróciłoby czytanie, które zdjął
[warunek na lemat](#zaimek-względny-nie-jest-przymiotnikiem-przy-rzeczowniku).

Rozdziela obie rodziny produkcji cecha `czoło` (`BEZ_CZOŁA` w `olski/subset/słowa.py`),
a niosą ją wszystkie produkcje obu symboli,
bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc rodzina milcząca przechodziłaby przez to żądanie za darmo.
Wartością jest nazwa symbolu, a nie jedno „wysunięte”,
bo każde czoło należy do jednej rodziny.
Wspólna wartość zlałaby te rodziny, więc `ustawa, który przepis obowiązuje`
wychodziłoby zdaniem względnym z grupą pytajną na czole,
a `Który zapisuje ustawienia?` pytaniem o sam zaimek.
Tę samą robotę wykonuje przy orzeczniku cecha `valency`:
rozdziela orzecznik zgodny od narzędnikowego, a kopula żąda drugiego z nich.
Cechę `czoło` niesie `orzecznik` obok tamtej i z tego samego powodu co podmiot:
orzecznik wysunięty na czoło jest tam trzecią rolą, którą czoło wypełnia
([niżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)).

Cena wyszła zerowa i wynika z kształtu tej zmiany, a nie z przebiegu.
Etykieta nie zmienia tego, co się wyprowadza, tylko to, jak się nazywa,
więc żaden werdykt ruszyć się nie może;
przebiegi nad bankiem drzew pod obiema morfologiami
oraz nad trzema korpusami prozy wydają to samo, zdanie po zdaniu.
Rusza się w nich sama kolejka blokerów, i o kilka zdań:
bloker mówi, dokąd rozbiór doszedł, a nie co się udało,
więc produkcja dopisana przesuwa go tam, gdzie tablica sięga dalej
(`bloker` w `olski/pokrycie.py`).

Zakup liczy się przez to w innej walucie i widać go w dwóch porównaniach ról
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).
Pod złotą morfologią 34 zdania wieloznaczne przechodzą z `lost` na `survives`,
a 10 zdań przyjętych z `partial` na `agrees`;
`disagrees` nie rośnie o ani jedno.

Tych dwóch liczb nie bierze żadne polecenie i bierze je ręka,
bo sonda różnicowa liczy przejścia werdyktu (`harness/ruch.py`),
a ta pozycja nie rusza ani jednego.
Wariantem jest gramatyka bez produkcji, które `_wysunięta_rola` pisze nad czołem:
`podmiot → czoło` po jednej na czoło, `dopełnienie → czoło` po dwóch,
bo tam rozdziela je przeczenie, oraz `orzecznik → czoło` po jednej,
a wraz z nimi wychodzi cecha `czoło` z ról, które ją niosą.
`python3 -m harness.pomiar Składnica-frazowa-180723/` puszczony nad taką gramatyką
wydaje obie tabele bez etykiety, a różnica wierszy jest tymi liczbami.
Czego brakuje, żeby wzięło je polecenie, trzyma [TODO.md](../TODO.md).

Grupa pytajna niesie dwie etykiety naraz i obie są potrzebne.
`grupa_pytajna` mówi, o co zdanie pyta,
i bez niej pytanie przyjęte nie mówiłoby tego wcale
(`GRUPA_PYTAJNA` w `olski/subset/deklaracja.py`),
a `podmiot` albo `dopełnienie` mówi, czym ta grupa w zdaniu jest,
i tego żąda bank drzew, bo grupy pytajnej nie zna
i obsadza `Który aktor` podmiotem.
Streszczenie wypisuje przez to jedną rozpiętość dwa razy,
i tyle ta pozycja kosztuje w wydruku.

### Bank drzew nazywa `który` inaczej niż Morfeusz, a czytelnik to przekłada

Składnica taguje `który` jako `padj`, czyli zaimek przymiotny,
a Morfeusz jako `adj`,
więc gramatyka pisana pod tagset Morfeusza nie sięgała po ani jedno wystąpienie
w przebiegu pod złotą morfologią.
Przekłada to dzisiaj czytelnik banku drzew, razem z trzema innymi nazwami
([corpus.md](corpus.md#where-the-analyses-stop)),
i obie kolumny mierzą przez to zdanie względne tak samo.

Pod złotą morfologią zdanie z `że` wyciąga z odrzucenia 66 zdań Składnicy,
trzydzieści trzy jednoznaczne i trzydzieści trzy wieloznaczne,
a zdanie względne 36, siedem jednoznacznych i dwadzieścia dziewięć wieloznacznych.
Każdą z tych liczb bierze osobny kontrfaktyk, czyli ta gramatyka bez jednej z nich,
więc suma tych dwóch nie jest liczbą, jaką dałoby zdjęcie obu naraz.
Ani jedno zdanie przyjęte nie traci przy tym jednoznaczności,
więc jednoznaczność obie konstrukcje kosztują tu zero,
a wieloznaczności przybywa wyłącznie na zdaniach, które wcześniej odpadały.

```text
Widoczny jest wzrost aspiracji społeczeństwa, które chce zdobywać wykształcenie.
```

Rozbieżność tagsetów jest przy tym faktem o korpusie, a nie o gramatyce,
i zapisana jest tutaj dlatego, że kolumna złota mówiła bez tego przekładu
o zdaniu względnym nieprawdę:
liczba, która się nie ruszyła, czyta się jak konstrukcja, która nic nie kupuje.

### Kopuła opuszczona jest wpisem na lemat, a nie pozycją ogólną

Rejestr ustaw odsyła zwrotem `o którym mowa`:
`Rada wykonuje zadania, o których mowa w ustawie.` znaczy `o których jest mowa`,
a `jest` nie pisze tam nikt.
Morfeusz zna formę `mowa` wyłącznie jako `subst:sg:nom:f`,
więc zdanie względne tego zwrotu obywa się bez czasownika,
a zdanie składowe bez czasownika wyprowadza w tej gramatyce sama ta konstrukcja.
Zwrot ten jest najczęstszym zdaniem względnym rejestru ustaw —
niesie go co siódme zdanie dwóch jego korpusów
([ustawy.md](ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)) —
więc konstrukcja ta odpowiada na kolejkę tamtego rejestru,
a nie na kolejkę ze Składnicy.

Wpuszczają ją dwa ciała, a rozdziela je to, skąd bierze się wyrażenie,
o którym ten rzeczownik orzeka.
Kopuła opuszczona takiego wyrażenia żąda, więc `Mowa o zadaniach.` jest polszczyzną,
a `Mowa.` nie jest.
Zdanie względne bierze to wyrażenie skądinąd:
`o których` leży poza zdaniem składowym, bo wysuwa je `wyrażenie_przyimkowe_względne`,
więc ciało czoła bierze ten rzeczownik wprost i zdania składowego nie ma pod sobą wcale.
Czoło pytania bierze go tym samym ciałem, więc `O którym akcie mowa?`
wyprowadza się razem z `o których mowa`.

Terminal tego rzeczownika żąda lematu, i to żądanie jest decyzją,
bo polszczyzna opuszcza kopułę szerzej niż w tym jednym zwrocie.
Wyjścia były dwa.
Pozycja ogólna czyni zdaniem składowym każdą grupę imienną w mianowniku,
czyli dopisuje `zdanie_składowe → podmiot` obok `zdanie_składowe → podmiot okoliczniki`.
Wpis leksykalny kupuje ten jeden zwrot i nic poza nim,
tak samo jak spójnik, którym zaczepia się
[zdanie z `że`](#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej).

Pozycję ogólną zmierzono, dopisując te dwie produkcje do gramatyki
i porównując werdykty z werdyktami olskiego.
Nad siedmioma ustawami wyciąga ona z odrzucenia 231 zdań,
116 z nich przyjmuje jednoznacznie,
a jednoznaczność odbiera siedmiu zdaniom przyjętym wcześniej;
nad „Zasadami techniki prawodawczej” i nad prozą tego repozytorium
odbiera ją po jednym zdaniu.
Zakup nie jest jednak zakupem, i widać to po tym, co ona przyjmuje:

```text
Wrocław.
Siedziba Okręgowej Komisji Wyborczej: LEGNICA.
```

Nazwa miasta stoi w akcie w tabeli, a nie w zdaniu,
i olski melduje o niej `valid`.
Reszta zakupu jest tą samą usterką w środku zdania,
bo przecinek i spójnik koordynują u olskiego zdania:
`Kierownikiem urzędu jest wójt lub burmistrz.` wychodzi wtedy dwoma zdaniami
składowymi, z których drugim jest `burmistrz`,
a `Statut związku powinien określać uczestników i czas trwania związku.`
dostaje drugie czytanie, w którym zdaniem składowym jest `czas trwania związku`.
Drugie z tych zdań jest jednym z siedmiu, którym ta pozycja odbiera jednoznaczność,
a dwa dalsze — `Przemyśl.` i `Kalisz.` — olski przyjmuje jako rozkaźnik
i pozycja ogólna daje im drugie czytanie, w którym są nazwą miasta.
Cena tej pozycji nie kończy się więc na tych siedmiu zdaniach:
psuje ona każdy ciąg współrzędny grup imiennych,
a takich ciągów ten rejestr niesie zdanie po zdaniu.

Etykietę roli stawia temu rzeczownikowi produkcja, tak samo jak przy
[czole zdania względnego](#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza),
a czego bez niej brakuje werdyktowi, mówi `olski/subset/deklaracja.py` przy tej roli.

```sh
python3 -m olski.check -c "Mowa o zadaniach." --readings
```

```text
<text>: valid     Mowa o zadaniach.
                  jedno odczytanie
                  - orzeczenie_rzeczownikowe: Mowa, wyrażenie_przyimkowe: o zadaniach → Mowa
```

Rola ta stoi obok orzecznika, a nie jest nim, i rozdziela je rama czasownika.
Orzecznik jest pozycją ramy: rzeczownikowy stoi w narzędniku pod kopulą,
a przymiotnikowy w mianowniku pod czasownikiem, którego rama go ma.
Rzeczownik orzekający nie ma nad sobą czasownika, więc pozycji ramy nie zajmuje,
a wpuszczony do orzecznika stanąłby tam, gdzie orzecznik ramy nie ogłasza:
w szyku z orzecznikiem przed kopulą (`olski/subset/zdanie.py`).
Przyjąłby wtedy `Mowa jest ustawa.`, czyli zdanie,
w którym olski czyta rzeczownikowy orzecznik w mianowniku.

Oba ciała są przy tym potrzebne, i rozstrzyga o tym przyłączenie:
`w ustawie` dochodzi w `Rada wykonuje zadania, o których mowa w ustawie.`
i do `mowa`, i do `wykonuje`, a pierwsze z tych czytań daje ciało zdania składowego,
drugie ciało czoła.
Zdjęte jedno z nich nie odrzuca tego zdania — drugie wyprowadza je samo —
tylko oddaje je jednym czytaniem,
czyli tak, jak wygląda zdanie, o którym gramatyka wybrała przyłączenie
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).
Wieloznaczność tego zdania jest więc tym przyłączeniem,
a nie czymkolwiek, co wnosi kopuła opuszczona.

## Określenie przed zdaniem wchodzi pod to, które stoi za nim

Zdanie składowe bierze określenie z obu stron i bierze je jednym symbolem.
Przed nim stoi wyrażenie przyimkowe, przysłówek albo cząstka,
a za nim wtrącenie w nawiasie, człon bez czasownika
albo [okolicznik wyrażony zdaniem](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania).
Cały ciąg współrzędny bierze z obu stron ten jeden okolicznik
i żąda tego samego, i z tego samego powodu.
Żadna z tych produkcji nie mówi, która dochodzi pierwsza,
więc same z siebie dają jednemu napisowi dwa kształty:

```text
Na stole leży sto dwadzieścia chlebów, bo piekarz je tam położył.
```

`Na stole` wchodzi w jednym kształcie pod okolicznik, a w drugim nad niego,
i to jest cała różnica między nimi.
Streszczenie nie różni ich ani jednym znakiem,
bo gospodarzem tego modyfikatora jest w obu ten sam czasownik,
więc werdykt liczy dwa czytania
i nie ma czym pokazać, czym się różnią.
Czytelnik nie ma tu przy tym czego rozstrzygać:
określenie przed zdaniem nie mówi nic o tym, co stoi za zdaniem,
a określenie za zdaniem nie mówi nic o tym, co stoi przed nim.
[Odczytaniem jest kształt](subset.md#co-się-liczy-jako-jedno-odczytanie),
więc dwa kształty na jedno odczytanie są usterką tej gramatyki,
a nie faktem o polszczyźnie.

Kształt zdejmuje gramatyka, choć oba znaczą to samo,
bo ani tożsamość czytania, ani warstwa znacząca tu nie sięgają.
Zwinięcie po stronie tożsamości żąda postaci normalnej nad zagnieżdżeniem określeń,
zostawia oba wyprowadzenia w lesie,
a sygnatura grubsza obowiązuje każde zdanie naraz, nie tylko tę parę
([disambiguation.md](disambiguation.md#tożsamość-czytania-jest-tańsza-i-częściowo-już-stoi)).
Warstwa znacząca dziedzinę ma węższą niż gramatyka i tych zdań nie dosięga
([architecture.md](architecture.md#werdykt-liczy-wyprowadzenia-bo-powstaje-pod-dwiema-warstwami-które-liczą-znaczenia)).
Warunek w gramatyce kosztuje za to jedną cechę, a las po nim maleje.

Porządek jest zapisany cechą (`dostawka` w `olski/subset/słowa.py`):
określenie stojące za zdaniem ją wypuszcza,
a określenie wysunięte przed zdanie żąda gospodarza, który jej nie niesie.
Wysunięte wchodzi więc pod to, co stoi za zdaniem, i nigdy nad nie.
Który z dwóch kształtów zostaje, nie rozstrzyga niczego poza sobą:
werdykt nad takim zdaniem wychodzi z obu ten sam.

Zdanie określone z jednej strony ma kształt jeden i warunek tego kształtu nie rusza,
więc nie odbiera on wyprowadzenia ani jednemu zdaniu:
nad Składnicą 180723 odrzuconych zdań jest z nim tyle samo, ile bez niego,
pod złotą morfologią i pod żywą.
Zdanie określone z obu stron ma za to czytań co najmniej o połowę mniej,
bo bez warunku mnoży je każde wysunięcie z każdym określeniem za zdaniem,
a kilkanaście zdań tego banku drzew przechodzi z wieloznacznych do przyjętych,
żadne nie tracąc złotego czytania.
Nad prozą tego repozytorium przechodzi ich kilka
([corpus.md](corpus.md#where-the-analyses-stop) trzyma polecenie).

## Grupa liczebnikowa zgadza się tym, czego nie ma w środku

Liczebnik przyłącza się w polszczyźnie dwoma sposobami
i który to sposób, mówi tag, a nie kontekst:
Morfeusz oznacza `dwie` jako `num:pl:nom.acc.voc:f:congr`,
a `pięć` jako `num:pl:nom.acc.voc:m2.m3.f.n:rec`,
czyli nazywa jeden zgodnym, a drugi rządzącym.
Liczebnik zgodny jest przy rzeczowniku tym, czym przymiotnik przed nim,
i zgadza się z nim w przypadku, liczbie i rodzaju:
`dwie rzeczy`, `cztery wozy`, `oba pliki`.
Liczebnik rządzący wymaga dopełniacza mnogiego,
tak jak wymaga go rzeczownik z dopełniaczem pod głową:
`pięć kobiet`, `kilka dni`, `piętnastu członków`.
Produkcje są więc dwie, a nie jedna z warunkiem w środku,
bo te dwa przyłączenia dzielą tylko nazwę części mowy.

Grupa, którą buduje liczebnik rządzący, zgadza się czymś, czego nie ma pod nią:
`Pięć kobiet przyszło.` żąda czasownika w liczbie pojedynczej i rodzaju nijakim,
choć `kobiet` jest mnogie i żeńskie,
więc liczba i rodzaj są w tej produkcji wypisane wartością.
Cecha wypisana wartością nie jest tu nowa:
[ciąg współrzędny](#nothing-above-a-coordination-distributes-into-it)
ogłasza liczbę mnogą i trzecią osobę tak samo, niezależnie od swoich członów.
Nowe jest to, czemu ta wartość przeczy.
Ciąg jest mnogi, bo dwie rzeczy są dwiema rzeczami,
a `pięć kobiet` jest pojedyncze i nijakie wbrew każdemu słowu w środku,
więc rodzaj nijaki nie opisuje tu niczego prócz zgodności, której polszczyzna żąda.
Rodzaj przechodzi natomiast z liczebnika na dopełniacz,
bo rodzaj męskoosobowy ma w polszczyźnie własną formę liczebnika:
`Pięciu mężczyzn przyszło.` wyprowadza się, a `Pięć mężczyzn przyszło.` nie.
Liczebnik zbiorowy wchodzi tą samą produkcją i nie kosztuje ani jednej pozycji,
bo `dwoje` jest dla Morfeusza liczebnikiem rządzącym
i różni się od `dwa` samą wartością cechy `collectivity`.

Do drabiny [kosztów](design-notes.md#the-cost-ladder) taka cecha nic nie dokłada,
bo jest cechą skończoną jak każda inna,
więc grupa liczebnikowa mieści się na szczeblu 0 razem z resztą gramatyki.
Liczebnik płaci więc nie formalizmem, a
[drugą walutą](design-notes.md#the-second-currency-ambiguity), czyli czytaniami.
Liczebnik rządzący jest synkretyczny między mianownikiem i biernikiem,
więc zdanie z grupą liczebnikową obok drugiej grupy synkretycznej
wychodzi dwoma czytaniami: `Rada gminy liczy piętnastu członków.` czyta się
i tak, że rada liczy członków, i tak, że członkowie liczą radę.
Polszczyzna ma oba te czytania, więc olski to zdanie odrzuca i odrzuca słusznie.
Drugą taką parę czytań daje sam słownik:
`więcej` i `najwięcej` Morfeusz zna jako liczebniki obok przysłówka `dużo`,
więc `otrzymał więcej głosów` wychodzi i grupą liczebnikową, i okolicznikiem,
a te dwa czytania polszczyzna ma tak samo.

### Liczebnik złożony przyłącza się wedle ostatniego członu

`Dwadzieścia dwa chleby leżą.` odmienia się wedle `dwa`,
a `Dwadzieścia siedem chlebów leży.` wedle `siedem`,
czyli wedle tego z dwóch przyłączeń wyżej, które niesie człon skrajnie prawy.
Dwa liczebniki obok siebie są więc łańcuchem o głowie po prawej,
a nie trzecim przyłączeniem ani warunkiem w środku tamtych dwóch:
symbol `Liczebnik` bierze `accommodability` od swojej głowy,
a oba tamte ciała pytają go tym samym, czym pytały terminala.
Łańcuch jest osobnym ciałem, bo sonda wycenia go zdejmowaniem ciał.

Przypadek, liczba i rodzaj są w łańcuchu wspólne wszystkim członom,
bo polszczyzna odmienia każdy z nich:
`Dwudziestu dwóch mężczyzn przyszło.` stawia w mianowniku oba człony,
a `dwadzieścia dwóch` nie jest niczym.
Łańcuch wiąże w prawo, więc `sto dwadzieścia dwa` ma jedno nawiasowanie.

Ostatniego członu `jeden` łańcuch nie bierze.
`Dwadzieścia jeden chlebów` żąda dopełniacza mnogiego,
choć `jeden chleb` żąda zgodności,
czyli ten człon rządzi w łańcuchu inaczej, niż rządzi sam.
Osobne ciało na `jeden` po liczebniku kupiłoby liczby zakończone na jeden,
więc wejdzie dopiero wtedy, gdy takich zdań naliczy się więcej niż garść.

Płaci łańcuch drugą walutą i płaci w dwóch miejscach.
Pierwsze z nich zdejmuje warunek ujemny.
Morfeusz daje `pięć` drugie czytanie — dopełniacz mnogi rzeczownika
odczasownikowego od `piąć` — a rzeczownik odczasownikowy jest
[głową grupy imiennej](#rzeczownik-odczasownikowy-jest-głową-grupy-imiennej-a-nie-pozycją-przy-czasowniku),
więc bez warunku `Dwadzieścia pięć chlebów leży.` wychodzi dwoma czytaniami:
łańcuchem oraz `dwadzieścia` nad grupą, której głową jest `pięć`.
Drugiego polszczyzna nie ma, a kolizja bierze co dziesiątą liczbę pisaną słowem,
bo tyle kończy się na pięć,
więc terminal rzeczownika odczasownikowego tego lematu nie bierze.
Jest to znowu warunek ujemny na lemacie, ten sam ruch co
[przy rozdzielającym `a`](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru).
Zabiera on cały leksem, bo negacji unifikacja nie zna,
więc `Pięcie jest trudne.` przestaje się wyprowadzać,
a skreślenie jednego argumentu oddaje to zdanie z powrotem.

Drugie miejsce zostaje i jest nim zagnieżdżenie.
Grupa, którą buduje liczebnik zgodny, jest dopełniaczem mnogim tak samo jak sam
rzeczownik — `brakuje dwóch mężczyzn` — więc ciało rządzące bierze ją nad sobą
i `Dwudziestu dwóch mężczyzn przyszło.` czyta się dwojako:
o dwudziestu dwóch oraz o dwudziestu z dwóch.
Drugie czytanie polszczyzna pisze przyimkiem, którego w tym zdaniu nie ma,
a cechy dzisiejsze tych dwóch nie odróżniają:
liczebnik zgodny wypuszcza grupę o cechach samego rzeczownika,
więc różni je sam kształt.

Zagnieżdżenie zachodzi tam, gdzie pierwszy człon jest synkretyczny
między rządzącym i zgodnym, czyli w formach męskoosobowych i przypadkach zależnych.
`Dwadzieścia dwa chleby leżą.` wychodzi jednym czytaniem.
Przed tą pozycją zdanie o dwudziestu dwóch przechodziło pod samym zagnieżdżeniem,
więc łańcuch zamienia tu werdykt nieprawdziwy na odmowę
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).

Odróżnia te dwa czytania cecha dopisana, czyli znacznik taki jak
[`ciąg`](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania):
grupa zbudowana przez liczebnik zgodny ogłasza się nim,
ciało rządzące żąda od tego, co pod nim stoi, wartości przeciwnej,
a `Dwudziestu dwóch mężczyzn przyszło.` wychodzi wtedy jednym czytaniem, tym właściwym.
Drugiej kopii pozycji grupy imiennej znacznik nie żąda;
żąda tej cechy w każdej produkcji `grupa_imienna` i `człon_imienny`,
bo żądanie jest dodatnie, a cechy nieobecnej unifikacja nie sprawdza.
Czytanie zostaje mimo to, bo naprawa nie kupuje niczego, co dałoby się zmierzyć.
Zdań stawiających obok siebie dwie formy o czytaniu liczebnikowym
ma Składnica 180723 dziesięć,
znacznik nie rusza liczby czytań ani nad jednym z nich pod żadną z dwóch morfologii
ani nad prozą tego repozytorium,
a rejestr docelowy pisze liczebnik złożony
[cyfrą](#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii), której olski nie bierze.
Liczbę pierwszą daje przejście po złotej morfologii banku drzew,
a pozostałe wariant gramatyki z tą cechą, puszczony przez `harness/ruch.py`.

### Cyfry olski nie bierze, bo cyfra nie niesie morfologii

Rejestr, o który olskiemu chodzi, pisze liczebnik cyfrą:
`w terminie 14 dni`, `3 szkół`, `15 członków`.
Morfeusz daje cyfrze tag `dig` i ani jednej cechy,
a cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc obie produkcje biorą cyfrę naraz.
Odrzucić ją umie żądanie obecności cechy
([design-notes.md](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)),
tyle że odrzuca wtedy każdą cyfrę i wpuszczenia nie kupuje.
`Termin wynosi 14 dni.` wychodzi wtedy trzema czytaniami zamiast dwóch,
bo `dni` jest i dopełniaczem mnogim, i mianownikiem mnogim,
czyli jedna grupa wyprowadza się i pod produkcją rządzącą, i pod zgodną.
Dwa z tych trzech czytań mają streszczenie znak w znak to samo,
bo różni je część mowy słowa pod głową, a nie żadna rola,
i po werdykcie czyta się to jak usterka narzędzia,
a nie jak zdanie, które da się poprawić.

Odmowa jest więc rozstrzygnięciem, a nie przeoczeniem,
i cena jest po jej stronie: cyfra zostaje formą,
której żadna produkcja nie bierze, i werdykt tak o niej mówi.
Wejście żąda dwóch rzeczy, których cyfra sama nie mówi, i tylko jedną da się odczytać.
Które z dwóch przyłączeń zachodzi, mówi rzeczownik po cyfrze:
`14 dni` ma dopełniacz mnogi, więc liczebnik jest tam rządzący,
a `14 dniach` miejscownik, więc zgodny, i tak samo czyta to każdy, kto ten rejestr pisze.
Przypadka samej grupy nie mówi ani cyfra, ani ten rzeczownik:
`pięć` jest mianownikiem, biernikiem albo wołaczem, a cyfra nie jest niczym,
więc grupa bez tej wartości spełnia każde żądanie przypadka w zdaniu.
Wejście stoi na tym drugim i jest to warstwa nad morfologią, a nie produkcja,
która wchodzi tym samym kryterium, co każda inna
([design-notes.md](design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)).

## Liczebnik orzeka o tym, ile czegoś jest

`Tory są dwa.` mówi, ile torów jest, i orzeka to samym liczebnikiem,
a nie rzeczownikiem ani przymiotnikiem.
Pozycja jest orzecznikiem zgodnym, czyli tym samym miejscem, w którym stoi
`Ludzie są wolni.`, bo liczebnik zgadza się tu z podmiotem tak samo jak przymiotnik:
`Warstwy są dwie.` żąda formy żeńskiej, a `Tory są dwa.` męskorzeczowej.
Ciało jest przez to jedno i wypisuje samą parę cech, tak jak orzecznik przymiotnikowy.

Ciało jest osobne, a nie liczebnikiem wpuszczonym do symbolu grupy przymiotnikowej,
bo tamten symbol jest zarazem przydawką,
a liczebnik ma przy rzeczowniku
[własne przyłączenia](#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)
i własne ciała; wpuszczony tam dałby `dwie rzeczy` drugie wyprowadzenie.

Pozycję tę bierze liczebnik zgodny i on jeden.
`Torów jest dwa.` mówi to samo rządzącym i zostaje na zewnątrz:
podmiot stoi tam w dopełniaczu, a orzeczenie nie zgadza się z niczym,
więc jest to osobne ciało i osobna liczba, której nikt nie policzył.

Nad bankiem drzew to ciało wyciąga z odrzucenia dwa zdania —
`Roześmieliśmy się obaj.` i `Ona płakała, a za chwilę płakałyśmy już obie.` —
a jednoznaczności nie odbiera ani jednemu zdaniu przyjętemu wcześniej.
Liczba jest mała, bo mierzy prozę prasową i literacką.
Rejestr, o który olskiemu chodzi, liczy tory i konstrukcje zdanie po zdaniu,
i to on postawił tę pozycję.
Kolejka blokerów jej nie widzi, bo każda forma tych zdań licencję ma,
a odrzucenie stoi na strukturze.

## Przydawka imiesłowowa stoi tam, gdzie przymiotnik

`Wymienione zadania są obowiązkowe.` i `Reguła sięgająca znaku jest tania.`
niosą jedną konstrukcję i jest nią przydawka,
a nie dwie pozycje przy dwóch częściach mowy.

Imiesłów przy rzeczowniku zgadza się z nim przypadkiem, liczbą i rodzajem,
czyli tym samym, czym zgadza się przymiotnik,
i stoi w tych samych dwóch szykach.
Dochodzi więc ciałem symbolu przymiotnikowego, a nie własnym symbolem:
osobny żądałby drugiej kopii każdej pozycji, w której przydawka stoi —
a stoi ich w gramatyce kilkanaście —
i nie kupowałby za to niczego, czego polszczyzna w tych pozycjach rozdziela.
Dopełniacz, którego imiesłów czynny żąda od swojego dopełnienia,
przychodzi przez to za darmo:
ciało z przydawką i dopełniaczem pod głową stało w gramatyce przed nim.

Ciała są dwa, po jednym na imiesłów, bo cena każdego jest osobną liczbą.
Orzecznik bierze przy tym biernego i nie bierze czynnego:
`Dziewczyna milknie zakłopotana.` jest polszczyzną,
a `Reguła jest sięgająca.` nie jest zdaniem, które ten rejestr pisze.

Cena stoi po stronie zgodności z drzewem wzorcowym, a nie po stronie pokrycia.
Przebieg nad Składnicą 180723 wypuszcza z odrzuconych przeszło dwieście zdań
i dokłada kilkadziesiąt przyjętych,
a podnosi przy tym dwie liczby, które mówią o werdykcie, że kłamie:
zdania, w których przyjęte czytanie przeczy drzewu wzorcowemu,
oraz zdania wieloznaczne, którym złote czytanie z lasu wypada.
Werdykt mówi więc o zdaniu nieprawdę częściej niż przed tą pozycją,
a kierunek ten trzyma
[roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę);
czym te zdania są, ten przebieg nie mówi, a wpis trzyma [TODO.md](../TODO.md).
Obie liczby drukuje `harness.pomiar`, a te sprzed tej pozycji trzyma git.

## Rzeczownik odczasownikowy jest głową grupy imiennej, a nie pozycją przy czasowniku

`Przyłączenie`, `wykluczanie`, `sięgnięciu` — Morfeusz daje takiej formie tag
`ger` wraz z liczbą, przypadkiem i rodzajem,
czyli z tym wszystkim, czego gramatyka od głowy grupy imiennej żąda.
Rodzaj jest przy tym zawsze nijaki, a niesie go tag, więc nie żąda go tu nic.

Rejestr, o który olskiemu chodzi, mówi tą formą o czynnościach,
bo dokumentacja opisuje to, co program robi:
`przyłączenie wyrażenia przyimkowego`, `wyznaczenie granicy`,
`sięgnięcie po mocniejszy mechanizm`.
Kolejka nad prozą tego repozytorium postawiła tę klasę na czele
zaraz po [leksykonie projektu](warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma),
a kolejka ze Składnicy trzyma ją w czwartym wierszu
([corpus.md](corpus.md#where-the-analyses-stop)).

Wchodzi ona jako głowa grupy imiennej, a nie jako pozycja przy czasowniku,
i tyle mówi o niej polszczyzna:
dopełnienia żąda w dopełniaczu — `przyłączenie wyrażenia`, a nie `przyłączenie
wyrażenie` — czyli tak, jak żąda go rzeczownik z dopełniaczem pod głową.
Rama czasownika zostaje przez to nietknięta,
a grupa z taką głową stoi w każdej roli, w której stoi każda inna grupa imienna.

Ta głowa dostaje tyle pozycji, ile ma rzeczownik, i dostaje je jednym zapisem:
pętla w `olski/subset/grupa.py` wypisuje każde ciało grupy imiennej dwa razy,
raz z rzeczownikiem i raz z formą odczasownikową.

Jedno wykluczenie stoi po stronie rzeczownika i nie dotyczy tej głowy.
Głowa rządząca dopełniaczem nie jest [zaimkiem rzeczownym](#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
a żaden z tych zaimków nie jest rzeczownikiem odczasownikowym,
więc po tej stronie nie ma czego wykluczać.

Jednej pozycji ta głowa nie ma i jest nią grupa wysunięta przed zdanie względne:
`którego przyłączenia` nie ma wyprowadzenia, gdzie `którego wyrażenia` ma.
Czoło zdania względnego bierze rzeczownik, a tej głowy nie bierze,
i wpuszczenie jej tam trzyma [TODO.md](../TODO.md).

## Łącznik `to` orzeka bez czasownika, a podmiot stoi za nim

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
podmiot postawiony za łącznikiem zgadza się z drzewem wzorcowym niemal wszędzie,
a postawiony przed nim jest niezgodny niemal wszędzie.
Podmiot stoi więc za łącznikiem, czyli tam, gdzie stawia go Składnica.

Grupa przed łącznikiem dostaje własną rolę,
a nie rolę rzeczownika orzekającego
([wyżej](#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną)):
tamten symbol czyni zdaniem każdą swoją córkę,
więc grupa imienna pod nim byłaby pozycją ogólną, którą tamta sekcja odrzuca.
Orzecznikiem nie jest z tego samego powodu, co tamten rzeczownik:
nie ma nad sobą czasownika, więc pozycji jego ramy nie zajmuje.

```sh
python3 -m olski.check -c "Flaga to płat tkaniny określonego kształtu." --readings
```

```text
<text>: valid     Flaga to płat tkaniny określonego kształtu.
                  jedno odczytanie
                  - podmiot: płat tkaniny określonego kształtu, orzecznik_łącznika: Flaga
```

Zakup wynosi nad Składnicą kilkadziesiąt zdań schodzących z odrzucenia,
w większości przyjętych jednoznacznie,
a ceny nie ma żadnej: ani jedno zdanie przyjęte wcześniej nie traci jednoznaczności.
Nad prozą tego repozytorium zakup jest zerowy — ten rejestr pisze się bez łącznika,
bo olski go nie brał — a dwa zdania schodzą z odrzucenia do wieloznaczności,
i obu wieloznaczność daje przyłączenie wewnątrz grupy, a nie sam łącznik.

Poza ciałem zostają dwie konstrukcje i obie trzyma [TODO.md](../TODO.md).
Łącznik przy formie osobowej, w obu szykach:
`Był to nieforemny chłopak.` i `To są oczywistości.` są odrzucone,
bo `to` nie stoi w nich między dwiema grupami, tylko przy czasowniku.
Te dwa szyki prowadzą resztę wiersza `pred`
([corpus.md](corpus.md#where-the-analyses-stop)).
Przeczenie: `Parser to nie kompilator.` jest odrzucone,
bo cząstka przecząca stoi w gramatyce przy czasowniku, a łącznik nim nie jest.
`To jest tanie.` wyprowadza się przy tym bez tej produkcji,
bo `to` jest w nim rzeczownikiem w podmiocie.

## Predykatyw orzeka bez podmiotu i rządzi ramą czasownika

`Trzeba czytać dokumenty.`, `Widać granicę w odpowiedzi.`, `Nie wiadomo.` —
Morfeusz trzyma te słowa pod `pred`, czyli w jednym wierszu kolejki blokerów
([corpus.md](corpus.md#where-the-analyses-stop)).
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
Przy [kopuli opuszczonej](#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną)
zapadł ten sam wybór: rzeczownik orzekający stoi obok orzecznika, a nie jest nim.

Lista lematów jest zamknięta, a poza nią zostaje słowo,
którego czytanie konkurujące staje na czele zdania tego samego kształtu.
`to` takie czytanie ma, i to dwa razy:
grupa imienna bierze jego czytanie rzeczownikowe,
a jako `pred` jest ono łącznikiem, czyli konstrukcją osobną i wpuszczoną osobnym ciałem
([wyżej](#łącznik-to-orzeka-bez-czasownika-a-podmiot-stoi-za-nim)).
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
([niżej](#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu)),
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
której nikt nie policzył, a wpis trzyma [TODO.md](../TODO.md).

Zakup jest liczony w pojedynczych zdaniach banku drzew
i po stronie ceny nie ma nic: ani jedno zdanie przyjęte nie staje się
wieloznaczne, pod żadną z dwóch morfologii.
Nad prozą tego repozytorium nie rusza ani jednego werdyktu,
bo ten rejestr tej formy nie pisze.
Wiersz `bedzie` w kolejce blokerów po tej konstrukcji nie pustoszeje:
zostaje w nim garść zdań, a dlaczego, mówi
[corpus.md](corpus.md#where-the-analyses-stop).

## Czasownik nieosobowy orzeka bez podmiotu i rządzi ramą swojego lematu

`Zgłoszono usterkę.`, `Nie zrobiono nic.`, `Podano do stołu.` —
Morfeusz trzyma te formy pod `imps`, czyli w jednym wierszu kolejki blokerów
([corpus.md](corpus.md#where-the-analyses-stop)).
Orzekają one bez podmiotu tak samo jak predykatyw wyżej,
więc rolę i oba ciała zdania biorą te same co on,
a różnica jest jedna: ta forma jest czasownikiem,
więc ramę bierze z leksykonu swojego lematu
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
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
([subset.md](subset.md#co-się-liczy-jako-jedno-odczytanie)).

Orzecznika zgodnego nie ma ani jedna z tych dwóch ram,
bo zgadza się on z podmiotem, którego takie zdanie nie ma:
`Zgłoszono tania.` nie jest niczym, tak samo jak `Trzeba wolni.`

Rola wspólna z predykatywem kosztuje pomiar różnicowy:
zdjęcie ciała zdania zabiera obie głowy naraz,
więc cenę każdej z nich mierzy się zdjęciem jej terminali
([CLAUDE.md](../CLAUDE.md#code)).

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
([roadmap.md](roadmap.md#readme-jest-przyrządem-pomiarowym)).

Szyki ma ta konstrukcja dwa, te same co predykatyw:
forma stoi przed tym, czym rządzi, a dopełnienie przed formą
([niżej](#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu)).
Cząstki trybu przypuszczającego ta forma nie bierze:
`Zgłoszono by usterkę.` jest odrzucone, bo cząstkę bierze forma na -ł
i tylko ona ([wyżej](#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku)).

## Dopełnienie poprzedza głowę, która orzeka bez podmiotu

`Usterkę zgłoszono.`, `Biura przeniesiono do Krakowa.`, `Nic nie widać.`
Polszczyzna wysuwa dopełnienie przed predykatyw i przed formę nieosobową
tak samo jak przed czasownik, którego podmiot opuszcza — `Cenę liczymy.` —
więc jest to jedna pozycja, a obie głowy biorą ją tak samo,
jak biorą dwa ciała zdania wyżej.

Dopełnienie stoi w niej córką zdania, a nie pod `wypełnienia`:
tamten symbol stoi w ciele za głową i tylko tam,
bo rozwinięcie szyku po nim nie chodzi
([subset.md](subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk)),
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
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).

Wysunięte jest tu samo dopełnienie, a nie każde wypełnienie,
i tyle też po tej pozycji zostaje [subset.md](subset.md#what-it-does-not-cover-yet).

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
[kierunek toru](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).

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
[wybierałaby gospodarza przez przeoczenie](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).

Szerokość ramy domyślnej pozycja dziedziczy i nie pogarsza.
`Córka krawca chciała zejść.` dostaje przez nią czytanie z `krawca`
w roli dopełnienia, choć `zejść` dopełnienia nie bierze,
a to samo czytanie ma już `Córka chciała zejść krawca.`,
bo biernik daje każdemu czasownikowi
[rama domyślna](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej).
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
[zaimki `kto` i `co`](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz).
Gramatyka rośnie przy tym o kilkadziesiąt produkcji,
bo ciała bezokolicznika powstają po dwa na klasę walencyjną.

Szyk jest jeden, ten wypisany, bo cena każdego jest osobną liczbą,
a głowa jedna: forma osobowa, i co po tym zostaje,
wylicza [lista braków](subset.md#what-it-does-not-cover-yet).
Zaimka względnego pozycja ta nie dosięga,
więc `Ustawa, którą organ gminy może wydać, jest tania.` jest dalej odrzucone
([wyżej](#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)),
i to zdanie zostaje tym jednym, które kupuje cecha przeciągana
([design-notes.md](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).

## Forma przyimkowa zaimka żąda przyimka przed sobą

[Wykluczenie](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not) pyta o samą formę,
a jedna klasa czytań, których polszczyzna nie ma, żąda pytania o sąsiada.

Morfeusz czyta `nie` jako biernik zaimka `on`,
a `niego` wyłącznie jako dopełniacz i biernik tegoż,
i polszczyzna stawia te formy jedynie po przyimku: `na nie`, `bez niego`.
Tagset mówi to sam.
Cecha `post_prepositionality` ma wartość `praep` przy formie stojącej po przyimku
i `npraep` przy tej, która stoi bez niego,
a `nim` niesie obie naraz, tak samo jak `niej` i `nich` w miejscowniku,
bo te formy stoją i pod przyimkiem, i bez niego.

Bez warunku na tę cechę wychodzą czytania, których polszczyzna nie ma,
i bywa tak, że takie czytanie zostaje jedynym.
Jedno czytanie zdania przeczytanego na opak jest werdyktem najgorszym,
jaki ten pomiar wydaje
([corpus.md](corpus.md#what-morphological-ambiguity-costs)),
bo `valid` czytelnik przyjmuje bez sprawdzania.

Warunek stoi przez to w warstwie morfologicznej i przed rozbiorem,
a nie na terminalu zaimka;
pyta on graf segmentacji, a jak, mówi `po_przyimku` w `olski/segmentacja.py`.

Licencji udziela sam przyimek tej gramatyki,
więc wykluczenie rozdzielającego `a` stoi i tutaj, nie tylko na terminalu
([wyżej](#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru)).
Zdanie po zdaniu widać ten warunek dopiero razem z członem bez czasownika
([wyżej](#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)),
bo dopiero on daje `, a` cokolwiek za sobą.
Kosztuje ten warunek pojedyncze zdania tej prozy i oba czytania, które zdjął,
były nieprawdziwe: `a nie` wychodziło w nich spójnikiem i zaimkiem
w zdaniu, którego dalsza część potyka się o co innego.

Dwie drogi obok tej odpadły, każda na czym innym.
Terminal wypowiada warunek o parze wiązek cech,
a przyimek stoi nad zaimkiem przez całą grupę imienną,
więc żądanie postawione na terminalu musiałoby zejść przez każde jej ciało osobno —
tą samą drogą, którą przeszła
[negacja](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne),
i za tę samą cenę.
Ciało, które by cechy nie przepuściło, przepuściłoby za to każdą formę,
a takiego przeoczenia nie łapie żaden test.
Warunek sprawdzany po rozbiorze musiałby z kolei znać kształt grupy imiennej
i wyrażenia przyimkowego, czyli być gramatyką napisaną drugi raz,
a to jest właśnie kryterium, po którym warstwa więzowa
[wchodzi albo nie wchodzi](design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej).
Cecha na terminalu zostaje tam, gdzie warunek jest o parę:
zaimek dzierżawczy żąda `npraep` od formy przed rzeczownikiem
([niżej](#zaimek-dzierżawczy-jest-dopełniaczem-przed-rzeczownikiem)),
i pod przyimkiem to żądanie zostaje jedynym, które `bez niego zapisu` odrzuca.

Cena nad Składnicą wychodzi zerowa i mówi to przebieg pod morfologią żywą.
Jednoznaczność zyskuje kilkanaście zdań,
a wyprowadzenie tracą te i tylko te:

```text
Ale nie tylko same ulice irytują.
Po drugiej stronie też nie ma nic.
Posłowie opozycji winią nie tylko Żochowskiego.
W tym roku Zagłębie też nie płaci.
```

Każde z nich było przyjęte na czytaniu, w którym `nie` jest dopełnieniem,
więc odrzucenie jest przy każdym werdyktem uczciwym.
Pod złotą morfologią warunek nie rusza niczego,
bo anotatorzy wybrali tam jedno czytanie na token,
tak samo jak przy wykluczeniu wyżej.

Na zewnątrz zostaje ciąg współrzędny pod jednym przyimkiem.
`dla niego i niej` ma przyimek nad obydwoma członami,
a przed drugim z nich nie ma go wcale,
więc `Program zapisuje ustawienia dla niego i niej.` traci wyprowadzenie,
gdzie `bez nich i plików` je zachowuje,
bo tam forma przyimkowa jest członem pierwszym.
Nad Składnicą nie kosztuje to ani jednego zdania,
a zdanie odrzucone stoi wśród tego,
[czego olski nie bierze](subset.md#what-it-does-not-cover-yet).

Forma, której to wykluczenie zabiera wszystkie czytania — `niego` innych nie ma —
jest dla werdyktu formą bez licencji,
więc `Cena niego rośnie.` wychodzi odrzucone z `niego` wypisanym.
Przebieg nad korpusem czyta ją inaczej i liczy takie zdanie
jako zdanie bez struktury nad całością,
bo `bloker` w `olski/pokrycie.py` nazywa część mowy pierwszego czytania,
a tu nie ma ani jednego.
Rozejście to jest zapowiedziane
([design-notes.md](design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)),
a naprawę trzyma [TODO.md](../TODO.md) razem z wycięciem czytań bez licencji,
które daje tę samą krawędź bez czytań na całej klasie form.

## Zaimek dzierżawczy jest dopełniaczem przed rzeczownikiem

`Jego skutki są znane.`, `Jej cena jest niska.`, `Ich liczba rośnie.`
Posiadanie trzeciej osoby polszczyzna wyraża dopełniaczem zaimka osobowego,
a nie osobnym przymiotnikiem, i tym różni się `jego` od `mój`, `nasz` i `swój`:
te trzy Morfeusz zna jako przymiotniki,
więc bierze je pozycja przymiotnika przy rzeczowniku,
a `jego`, `jej` oraz `ich` czyta jako formy lematu `on`,
więc brakowało trzeciej osoby i tylko jej.

Pozycja jest jedna i stoi przed grupą imienną, bo tam ją polszczyzna stawia.
Dopełniacz po rzeczowniku bierze inna produkcja,
więc `skutki jego` wychodzi tak samo jak `skutki wyboru`
([subset.md](subset.md#what-the-grammar-covers)), i ciało jest dlatego jedno, a nie dwa.

Zgodności ta pozycja nie ma i mieć nie może,
bo zaimek zgadza się ze swoim poprzednikiem, a ten stoi w zdaniu obok:
`Jego skutki` ma zaimek pojedynczy przy rzeczowniku mnogim, a `Ich cena` odwrotnie.
Zmienna wspólna — ta, którą wypuszcza przymiotnik i liczebnik zgodny obok —
wygląda tu poprawnie i odbiera polszczyźnie prawie każdą taką parę;
niezmiennik pilnuje test w `tests/test_subset.py`.

Formę zawężają dwa warunki na cechę, a nie lista lematów:
lematem każdej z tych form jest `on`, więc lista wpuszczałaby je wszystkie naraz.
Pierwszy żąda formy akcentowanej, czyli zostawia poza pozycją `go`:
`Znam go cenę.` nie jest polszczyzną, bo forma nieakcentowana stoi
przy czasowniku, a nie przy rzeczowniku.
Drugi żąda formy nieprzyimkowej, czyli zostawia poza pozycją `niego`, `niej` i `nich`:
`Znam niego cenę.` nie jest polszczyzną tak samo,
a `Bez niego cena rośnie.` jest, bo tam ta forma stoi po przyimku.
Warunek drugi zarabia na siebie właśnie pod przyimkiem, i tylko tam.
Poza nim formę przyimkową odsiewa już morfologia
([wyżej](#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)),
a `bez niego zapisu` ma tę formę po przyimku,
więc odrzuca ją to jedno żądanie i nic poza nim.

Pozycji tej nie ustawiła ani kolejka blokerów
([corpus.md](corpus.md#where-the-analyses-stop)),
ani ranking form bez licencji.
Odrzucenie stało na strukturze, a nie na żadnej z tych form,
bo grupa imienna o jednym zaimku bierze każdą z nich,
więc analiza zatrzymywała się dopiero za zaimkiem:
`Jego skutki są znane.` stawało na `znane`.
Wskazała ją sesja pisząca pod tę gramatykę zdanie po zdaniu.
Ze wszystkiego, co tam zawracało zdanie, ta pozycja zawracała je najczęściej
([pisanie-po-olsku.md](pisanie-po-olsku.md)).

## Zaimki `kto` i `co` wchodzą wszystkimi pozycjami naraz

Morfeusz trzyma te dwa zaimki pod rzeczownikiem,
a przecinek koordynuje w tej gramatyce zdania,
więc bez wykluczenia każde ich użycie ma jeden i ten sam kształt:
zaimek jest podmiotem albo dopełnieniem zdania po przecinku.
`Pyta, kto płaci.` wychodzi wtedy `valid` z czytaniem,
które jest ciągiem dwóch zdań współrzędnych,
czyli którego polszczyzna nie ma.
Jedno czytanie zdania przeczytanego na opak jest werdyktem najgorszym,
jaki ten pomiar wydaje
([corpus.md](corpus.md#what-morphological-ambiguity-costs)).

Pozycji rzeczownej te dwa lematy dlatego nie mają.
Z tą pozycją jeden napis dostaje dwa wyprowadzenia:
`Kto płaci?` wyprowadza się i pytaniem, i zdaniem oznajmującym
zamkniętym pytajnikiem, a role obu są te same.
Wykluczenie stoi na terminalu głowy grupy imiennej,
a nie w `admissible`, bo czytanie `subst` jest tym,
o które pytają czoła niżej;
tym różni się ono od wykluczenia ze słownika
([warstwa-leksykalna.md](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).

Wykluczenie to odbiera pozycję wszystkim użyciom tych zaimków naraz,
a użycie jest w tym rejestrze niejedno.
Dlatego pozycje niżej stoją w gramatyce razem, a nie jedna po drugiej:
pozycja wpuszczona sama zostawia pozostałe bez ani jednego czytania,
a pomiar mówi wtedy o zmianie, że obniża pokrycie,
choć obniża je przez to, że pierwsza pozycja zabiera pozostałym czytanie
nieprawdziwe i nie daje im nic w zamian.

- **Czoło pytania o jednym słowie.**
  `Kto płaci?`, `Pyta, kto płaci.` Grupa pytajna ma dwa ciała:
  zaimek `który` przy rzeczowniku i te dwa zaimki same,
  bo rzeczownika przy sobie nie mają.
  Wyrażenie przyimkowe bierze to czoło osobnym ciałem —
  `Kto z posłów zapisuje ustawienia?` — bo grupy imiennej,
  która by je wzięła, w środku nie ma.
  Przyłączenia tego olski nie wybiera, tak samo jak wszędzie
  ([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)).
  Przymiotnik za zaimkiem jest ciałem trzecim:
  `Kto pierwszy wstaje od stołu?`, `Kto inny zapisuje ustawienia?`
  Zaimek zgadza się z nim sam, bo rzeczownika przy sobie nie ma.
  Ciało bierze terminal, a nie symbol przydawki, i wyklucza zaimek wskazujący:
  Morfeusz czyta `to` także jako przymiotnik od `ten`,
  więc bez wykluczenia `co to` wychodzi grupą pytajną,
  gdzie polszczyzna ma dwa zaimki obok siebie,
  a `Co to jest?` dostaje drugie czytanie.
  Zakupem jest jedno zdanie banku drzew, ceną zero pod obiema morfologiami,
  a szersze ciało kupowałoby więcej i kupowałoby właśnie tamtym czytaniem,
  więc rozstrzyga tu
  [kierunek](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę), a nie pokrycie.
- **Zaimek względny o poprzedniku zaimkowym.**
  `To, co mogło się zepsuć, jest tanie.`,
  `Program zapisuje wszystko, co widzi.`
  Czoło jest osobnym symbolem, a nie drugim ciałem czoła z `który`,
  i rozstrzyga o tym poprzednik: `który` bierze rzeczownik,
  a te dwa zaimka albo całe zdanie
  ([niżej](#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie)).
- **Zdanie względne o poprzedniku zdaniowym.**
  `Cena jest niska, co przekreśla sens działań.`,
  `Bierzemy ostry zakręt, dzięki czemu unikamy zderzenia.`
  Poprzednikiem jest tu zdanie, więc zgodności nie ma z czym sprawdzać,
  a pozycja bierze `co` i nie bierze `kto`, bo tamten jest męskoosobowy.
- **Zdanie względne bez poprzednika w roli podmiotu.**
  `Kto wchodzi w środek, poprzedniego zdania nie przeczytał.`
  Przecinek zamyka ją tak samo jak każde zdanie względne,
  a role jej wnętrza nie są rolami zdania nad nią.
- **Ciąg pytań zależnych pod jednym czasownikiem.**
  `Drzewo mówi, co jest tematem, a co jest nowe.`
  Drugie wypełnienie bierze przy czasowniku sam celownik
  ([warstwa-leksykalna.md](warstwa-leksykalna.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia)),
  więc pozycję ramy zajmuje ciąg cały,
  a znakiem tego ciągu jest spójnik, a nie sam przecinek
  ([wyżej](#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja)).
- **Orzecznik wysunięty na czoło.** `Czym jest parser?`, `to, czym jest GLR.`
  Rola jest w tych dwóch rodzinach trzecia obok podmiotu i dopełnienia,
  a pozycję ma jedną, bo narzędnika żąda sama kopuła.

Zakup i cena są różnicą wobec gramatyki bez tych pozycji,
a między rejestrami rozchodzą się w tę stronę,
którą [kierunek](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę) przewiduje.
Nad prozą tego repozytorium przybywa zdań przyjętych jednoznacznie,
a każde z nich ma w tamtej gramatyce także czytanie ciągu współrzędnego;
kilka zdań dostaje czytanie tam, gdzie tamta nie daje żadnego,
a kilkanaście przechodzi na odrzucone — i tym, co je tam wyprowadza,
jest właśnie ten ciąg; konstrukcję, której im brakuje, nazywa kolejka niżej.
Nad bankiem drzew zakup jest mniejszy, a cena większa,
i tak wychodzi pod jedną morfologią i pod drugą:
kilka zdań, których tamta gramatyka nie wyprowadza, wychodzi przyjętych,
a kilkanaście, które w niej czytanie mają, przechodzi na odrzucone,
więc suma przyjętych spada.
Rozdziela te dwa rejestry poprzednik, a nie częstość:
`, co` niesie tu częściej niż co dwudzieste zdanie,
a w banku drzew rzadziej niż co setne,
tylko że tutaj stoi przed tym zaimkiem `to`, `wszystko` albo `niczego`,
a tam zdanie całe — i to drugie jest tym, czemu wykluczenie zabiera czytanie.

Wykluczenie zostawia po sobie kolejkę konstrukcji, a nie pustą listę,
i stoją na niej te użycia, których czoła nie obejmują:
zaimek stojący nie na czele, czyli drugie pytanie w tym samym zdaniu
(`Kto jest kim?`),
zdanie względne bez poprzednika w roli innej niż podmiot,
oraz przytoczenie samego wyrazu, którym ten rejestr o sobie mówi
(`nikt, kto, nic, coś i ktoś mają u Morfeusza czytanie jedno`).
`TODO.md` trzyma je wszystkie.

Jedno użycie zostaje na tej kolejce mimo ciała trzeciego i zostaje osobno:
`Co innego jest tanie.` wychodzi przyjęte z `Co innego` w okoliczniku,
bo Morfeusz czyta `co` także jako przyimek,
a przymiotnik za zaimkiem tego czytania nie zdejmuje:
`innego` jest dopełniaczem, więc zgadza się z `co` w dopełniaczu,
a rola, w której to stoi, żąda mianownika.
Przydawka i ten napis są więc dwiema robotami, a nie jedną,
i drugą z nich zamyka wykluczenie po stronie słownika, a nie produkcja.

## Poprzednikiem zaimka `co` jest zaimek albo zdanie

Zaimek `który` zastępuje rzeczownik, a `co` zaimek rzeczowny albo całe zdanie,
i są to trzy różne poprzedniki, nie dwa użycia jednego.
Dopóki oba zaimki miały jedno czoło, rzeczownik dostawał zdanie względne z `co`
wszędzie, gdzie parę cech miał przypadkiem —
`Sejm zaaprobował przekroczenie budżetowe, co przekreśliło sens dalszych działań
Trybunału Stanu.` wychodziło `valid` z jednym czytaniem,
w którym `co` jest przydawką przy `przekroczenie`,
a całe zdanie podrzędne wpada w dopełnienie.
Poprzednikiem jest tam zdanie, więc było to czytanie,
którego polszczyzna nie ma,
a werdykt podawał je z pewnością jednego odczytania.
Nad bankiem drzew wychodziło to w jednym wierszu `disagrees` i nigdzie poza nim,
bo zdanie takie olski przyjmuje, a pokrycie liczy je jak przeczytane
([corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)).

Czoła są przez to dwa, każde osobnym symbolem,
i nie jest to podział na lematy, tylko na poprzedniki:
czoło z `który` wchodzi pod rzeczownik,
a czoło z `kto` i `co` pod zaimek rzeczowny oraz pod zdanie.
Zdanie względne bez poprzednika idzie tą drugą drogą,
bo tam stoją zaimki, którymi ono się zaczyna;
`który` wyprowadzenia w tej pozycji nie miał i bez tego podziału,
więc przeniesienie jej nic nie zabiera i nic nie kupuje —
gramatyka mówi po nim to, co i przedtem było prawdą.
Poprzednik zaimkowy stoi przy tym w ciele członu grupy imiennej,
a nie nad grupą całą, bo zaimek rzeczowny dopełniacza nie bierze
([wyżej](#zaimek-rzeczowny-nie-rządzi-dopełniaczem)),
więc przydawki przed sobą nie ma i grupy z niego nie ma po co składać.

Zgodności ta pozycja nie sprawdza,
bo poprzednikiem jest zdanie, które liczby ani rodzaju nie ma.
Wypisuje je więc sama, i są to liczba pojedyncza i rodzaj nijaki,
czyli to, co niesie `co`.
Rozdziela to `co` od `kto` bez osobnej cechy —
`kto` jest męskoosobowy, więc tej pozycji nie dosięga,
a `Cena jest niska, kto przekreśla sens.` zostaje odrzucone.
Przyimek przed zaimkiem wchodzi tą samą drogą co przy poprzedniku zaimkowym,
bo niesie go czoło, a nie ta pozycja, więc `dzięki czemu`, `przez co`, `po czym`
i `wobec czego` wychodzą razem z `co` samym.
Pozycje są dwie — nad zdaniem składowym i nad całym ciągiem współrzędnym —
bo poprzednikiem bywa jedno i drugie,
i są to te same dwie pozycje, które ma okolicznik wyrażony zdaniem
([wyżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)).

Zakup i cena są nad bankiem drzew tego samego rzędu pod obiema morfologiami,
a cena jest o włos większa.
Zakupem jest garść zdań przechodzących z odrzuconych:
`Bierzemy ostry zakręt, dzięki czemu unikamy zderzenia z ciemnoczerwoną ścianą.`
oraz `Podopieczni Leo Beenhakkera w obecnym sezonie nadzwyczaj skutecznie
gromadzą punkty, dzięki czemu ich przewaga nad rywalami nie podlega dyskusji.`
Ceną jest garść zdań tracących jednoznaczność,
a przeczytane po kolei mówią, skąd ona się bierze:
poza jednym wszystkie są pytaniem zależnym — `Wiem, co zrobię.`,
`Sprawdziłeś, o co cię prosiłem?`, `Wiedzą, co robią.` —
któremu ta pozycja dokłada drugie czytanie,
bo `, co` z pytaniem zależnym dzieli napis co do znaku.
Właścicielem tej ceny nie jest ta pozycja, tylko rama domyślna:
pozycję pytania zależnego daje ona każdemu czasownikowi
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
więc drugie czytanie wychodzi i tam, gdzie czasownik pytania nie żąda.
Zawężenie tej pozycji do leksykonu trzyma `TODO.md`,
i ten pomiar jest argumentem za nim.

Drugie czoło kosztuje w produkcjach:
`_wysunięta_rola` wypisuje dla niego wszystkie szyki reszty zdania,
więc gramatyka rośnie o kilka procent,
a liczbę na dziś drukuje kolumna `produkcji` w wydruku sondy luki
([design-notes.md](design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
Kosztu tego dałoby się uniknąć jednym czołem i cechą przy nim,
mówiącą, który zaimek to czoło niesie,
a odrzuca tę wersję pomiar, nie liczba produkcji:
sonda wycenia pozycję zdjęciem produkcji, więc cena osobna żąda symbolu osobnego
([CLAUDE.md](../CLAUDE.md#code)).
Pod jednym czołem zdjęcie ciał zabrałoby razem z `co` także `który`,
czyli tę pozycję dałoby się wpuścić, a nie dałoby się jej wycenić.
Odwraca ten wybór jedno: gdy o cenę tej pozycji nikt już nie pyta,
tańsze jest czoło wspólne.

Pod złotą morfologią, czyli tam, gdzie pomiar sięga po drzewo wzorcowe,
złotego czytania nie traci ani jedno zdanie,
a zdanie o przekroczeniu budżetowym, od którego ta sekcja się zaczyna,
przechodzi z wiersza niezgodnych do zgodnych.
Ani jedno zdanie nie traci też tam wyprowadzenia;
pod żywą traci je jedno, i jest to odrzucenie prawdziwsze od trzech czytań:
`Kiedyś zapytałem kierowcę naszego gazika, kim właściwie jest mój przewodnik?`
wyprowadzało się wyłącznie przez `kim` w przydawce przy `kierowcę`,
a pytania z orzecznikiem wysuniętym za przecinkiem ten podzbiór nie ma,
więc jedyne, czego temu zdaniu brakuje, jest tą pozycją, a nie przydawką
([wyżej](#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)
wylicza ją wśród konstrukcji, które zostają w kolejce).

## Zaimek zwrotny jest terminalem, bo nie zgadza się z niczym

`Widzę siebie.`, `Osie są od siebie niezależne.`
Morfeusz trzyma ten zaimek pod częścią mowy tej jednej formy — `siebie:gen`,
`sobie:dat`, `sobą:inst` — a przypadek jest jedyną cechą, jaką ta część mowy niesie.

Rozstrzyga o tym brak liczby i rodzaju.
Grupa imienna niesie obie, bo zgadza się nimi z przydawką i ze zdaniem względnym,
a ciało grupy bez nich wpuszczałoby ten zaimek wszędzie tam,
gdzie zgodności żąda ktoś inny:
cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc `Widzę siebie, która stoi.` dostawałoby wyprowadzenie.
Ceną terminalu jest to, że przydawki ani dopełniacza ten zaimek pod sobą nie bierze,
a polszczyzna nie daje mu ani jednego, ani drugiego.

Pozycje są dwie: dopełnienie oraz grupa pod przyimkiem.
Dopełnienie powtarza ciała grupy imiennej —
biernik, dopełniacz negacji oraz celownik i dopełniacz z leksykonu
([warstwa-leksykalna.md](warstwa-leksykalna.md#leksykon-licencjonuje-dopełnienie-w-celowniku-i-w-dopełniaczu)) —
a stoją one wypisane, bo z listy leksykonu wchodzą tu dwie pozycje z trzech:
bezokolicznik przypadkiem nie jest.
Mianownika ta część mowy nie ma i mieć nie może,
skoro zaimek ten odsyła do podmiotu, więc podmiotem nie bywa
i produkcji na to nie ma.
Orzecznika narzędnikowego ten zaimek nie dostał,
a zdanie z nim mimo to się wyprowadza:
`Parser jest sobą.` wychodzi jednoznaczne na rzeczowniku `soba` w narzędniku.
Pozycja i ten lemat schodzą się przez to w jedno pytanie, a wpis trzyma
[TODO.md](../TODO.md).

Zakup jest tu kilkudziesięcioma zdaniami banku drzew wyciągniętymi z odrzucenia,
w większości przyjętymi, i po stronie ceny nie ma pod złotą morfologią nic:
ani jedno zdanie przyjęte wcześniej nie staje się wieloznaczne.
Pod żywą płaci ten sam lemat `soba`, którego Morfeusz zna w celowniku,
miejscowniku i narzędniku: jednoznaczności traci kilkanaście zdań z `sobie`
i `sobą`, a `siebie` żadnego.
Każde z nich wychodziło bez tej pozycji jednoznaczne właśnie na rzeczowniku,
czyli na czytaniu, którego polszczyzna tam nie ma
([warstwa-leksykalna.md](warstwa-leksykalna.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)),
więc razem z jednoznacznością ubywa werdyktów nieprawdziwych.
Wykluczenie ze słownika po ten lemat nie sięga, bo jest to rzeczownik odmienny
([warstwa-leksykalna.md](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).
Nad prozą tego repozytorium zakup jest liczony w pojedynczych zdaniach,
a ceny nie ma żadnej.
Z drzewem wzorcowym olski nie zgadza się nad pojedynczymi zdaniami nowo przyjętymi,
a garść czyta bez roli, którą dałoby się z tym drzewem porównać:
podmiot jest w nich opuszczony, a zaimek stoi pod przyimkiem.

## Imiesłów przysłówkowy stoi tam, gdzie okolicznik wyrażony zdaniem

`Program zapisuje ustawienia, sprawdzając zgodność.`
Konstrukcja ta jest okolicznikiem i zajmuje miejsce,
które okolicznik wyrażony zdaniem w tej gramatyce już ma
([wyżej](#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania)),
więc dochodzi jego ciałami, a nie własnym symbolem.
Przemawia za tym to samo, co przy [przydawce
imiesłowowej](#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik):
symbol osobny żądałby drugiej kopii obu pozycji okolicznika
oraz obu ciał nad ciągiem współrzędnym,
a nie kupowałby za to niczego, czego polszczyzna w tych miejscach rozdziela.

Spójnika te ciała nie mają i mieć nie mogą,
bo imiesłów podporządkowuje sam: formą osobową nie jest.
Przecinek zostaje, bo to on tę konstrukcję w zdaniu odgranicza.

Wypełnienie bierze imiesłów ramą swojego lematu,
tak samo jak forma nieosobowa czasownika
([wyżej](#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu)),
i tak samo bez orzecznika zgodnego:
podmiot tego imiesłowu stoi w zdaniu nadrzędnym,
więc pod nim nie ma z czym zgodzić ani orzecznika, ani niczego innego.
Widać to na lemacie, o którym leksykon mówi, że biernika nie bierze:
`Program zapisuje ustawienia, pomagając zgodność.` jest odrzucone,
gdzie `pomagając linterowi` się wyprowadza.
Polszczyzna żąda przy tym od tego imiesłowu tożsamości podmiotu,
a nie zgodności form, więc gramatyka nie ma tego czym złamać:
`pcon` nie niesie ani liczby, ani rodzaju, ani osoby.

Ciała są dwa na każdą pozycję, bo zakup imiesłowu samego —
`Program zapisuje ustawienia, milcząc.` — jest osobną liczbą.
Cząstka zwrotna stoi przy nim po obu stronach, tak samo jak przy formie osobowej.

Przez tę konstrukcję symbol okolicznika wchodzi między gospodarzy przyłączenia,
i jest to jedyna jego głowa, która tego wpisu potrzebuje.
Pod okolicznikiem wyrażonym zdaniem stoi zdanie składowe,
na którym zejście po gospodarza staje wcześniej,
a pod imiesłowem nie stoi żaden inny gospodarz,
więc bez tego wpisu `sprawdzając zgodność z dokumentem`
nazywałoby gospodarzem orzeczenie zdania nadrzędnego
i dwa czytania wychodziłyby z werdyktu jednym napisem
([subset.md](subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)).

Zakup jest tu kilkudziesięcioma zdaniami banku drzew wyciągniętymi z odrzucenia,
w większości wieloznacznymi, a ceny nie ma żadnej pod żadną z dwóch morfologii:
ani jedno zdanie przyjęte wcześniej nie staje się wieloznaczne.
Niezgodnie z drzewem wzorcowym olski nie czyta ani jednego zdania nowo przyjętego.
Nad prozą tego repozytorium zakup jest liczony w pojedynczych zdaniach,
bo ten rejestr pisze tę formę rzadko.

## Narzędnik bez przyimka jest okolicznikiem obok orzecznika

`Mieszczanie zabili okna deskami.` mówi, czym zabili,
a `Wziął lustro wieczorem.` mówi, kiedy wziął,
i polszczyzna wyraża jedno i drugie samym narzędnikiem, bez przyimka.
Olski brał ten przypadek pod przyimkiem i nie brał go bez niego,
bo `inst` było u niego pozycją orzecznika i niczym więcej
([warstwa-leksykalna.md](warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej)).

Pozycja jest okolicznikiem, czyli stoi tam, gdzie stoi wyrażenie przyimkowe
i przysłówek, i wchodzi tą samą listą co one.
Symbol ma własny, choć pozycję dzieli z przysłówkiem,
bo cena każdej z nich ma być osobną liczbą, a sonda bierze ją zdejmowaniem ciał
([CLAUDE.md](../CLAUDE.md#code)).

Od orzecznika różni ten okolicznik to, kto mu udziela licencji.
Orzecznika żąda ramą kopula i nikt poza nią,
a okolicznik stoi przy każdym czasowniku i nie wypełnia przy żadnym pozycji ramy.
Zdanie, w którym kopula stoi przy grupie w narzędniku, ma przez to dwa czytania,
i dlatego kopula wypada z dwóch ciał, w których orzecznika przy niej nie ma:
`Parser jest.` przestaje się wyprowadzać,
a `Parser jest narzędziem.` zostaje przy jednym czytaniu, tym prawdziwym.
Zawężenie to kupuje jednoznaczność także zdaniu złożonemu:
bez niego `Pomiar mówi, że gramatyka jest podzbiorem.` czyta się i tak,
że zdanie podrzędne kończy się na `jest`,
a `podzbiorem` jest okolicznikiem przy `mówi`.
Cena jest jedna i nazwana: zdania orzekającego samym istnieniem — `Bóg jest.` —
olski nie bierze, a ten rejestr go nie pisze.

Zakup liczy się w setkach zdań i jest mniejszy niż ten, którym płacił
[przysłówek](#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe).
Nad Składnicą pod złotą morfologią przeszło sto zdań wychodzi z odrzucenia
z jednym czytaniem, a drugie tyle z kilkoma,
i jest to więcej niż jedno zdanie odrzucone na trzydzieści.
Cena jest kilkunastokrotnie mniejsza:
jednoznaczność traci kilkanaście zdań przyjętych wcześniej.

Ważniejsze od tych dwóch liczb jest to, co werdykt mówi o zdaniach nowo przyjętych.
Z rolami drzewa wzorcowego zgadza się ponad cztery piąte z nich,
a niezgodne jest co dziewiąte.
Wśród niezgodnych stoi `Kwitnie handel paszportami.`,
czyli to samo zdanie, którym
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance)
mierzył, ile kosztuje orzecznik wpuszczony pod każdy czasownik:
olski czyta je teraz tak, jak czyta je czytelnik — handel kwitnie w paszportach —
a drzewo wzorcowe znaczy tam co innego.
Odrzucenie zamieniło się więc na czytanie prawdziwe, a nie na zgodność
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)).

Pod żywą morfologią rachunek jest inny i cała różnica jest w słowniku.
Zdań z odczytaniem przybywa tam podobnie wiele, a przyjętych ubywa kilkanaście:
forma czytana w kilku przypadkach naraz staje odtąd i w tym okoliczniku,
więc drugie czytanie dostaje każde zdanie, w którym taka forma zajmuje rolę.
Nazwa własna i nazwa urzędu mają to po Morfeuszu — `Jan`, `minister` i `redaktor`
niosą czytanie żeńskie nieodmienne obok męskiego — a w tym rejestrze mają to
[notacja](warstwa-leksykalna.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)
oraz [napis przytoczony](#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania),
bo czytanie nieodmienne spełnia każde żądanie przypadku i spełnia też to.
`Zobacz docs/subset.md.` traci przez to jednoznaczność,
a `tests/test_subset.py` trzyma tę cenę wypisaną zdaniami.
Nad prozą tego repozytorium ubywa przez to kilku zdań przyjętych,
a odrzuconych nie ubywa ani jedno.

**Wysunięcia przed zdanie ta pozycja nie dostaje i jest to pomiar odmowny.**
`Wieczorem wziął lustro.` zostaje przez to na zewnątrz,
choć polszczyzna ten szyk pisze, a tor składu go wypisuje
(`tests/test_rozbiór.py`).

Zderza się on z dwoma kształtami zdania, które gramatyka ma:
z [szykiem od czasownika](#the-bare-verb-initial-order-keeps-the-predicative-one-honest)
oraz ze zdaniem o opuszczonym podmiocie.
W obu grupa wysunięta jest jedyną grupą przed czasownikiem,
więc `Wejściem jest zwykły tekst polski.` czyta się i tak, że wejście jest
orzecznikiem, i tak, że tekst jest wejściem, a `Jan jest nauczycielem.` dostaje
czytanie mówiące, że ktoś jest nauczycielem przy pomocy Jana.
Rozdziela te czytania morfologia, a nie struktura:
pierwsze żąda mianownika, drugie narzędnika, a formy, o które idzie, mają oba.
Produkcja nie ma więc czego zażądać,
bo unifikacja przecina zbiory i nie umie zażądać przypadku jedynego
([design-notes.md](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne)).

Sonda mówi to samo liczbą: ciało to wyciąga z odrzucenia jeszcze kilkadziesiąt zdań,
a jednoznaczność odbiera niemal tylu, ilu ją daje,
więc płaci się za nie zdaniem tego rejestru, a dostaje zdania banku drzew.
Liczby te trzyma commit, który to ciało odrzucił.

## Przysłówek wchodzi każdym gospodarzem, bo dalszy zdejmuje czytania nieprawdziwe

Wyrażenie przyimkowe ma dwóch gospodarzy i oba czytania są prawdziwe,
więc olski [oddaje je czytelnikowi](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).
Przysłówek ma trzech gospodarzy, a nad jednym zdaniem prawdziwy jest jeden z nich:
`bardzo` w `Plik jest bardzo duży.` określa przymiotnik i zdania nie określa,
a `tu` w `Mam tu odmienną interpretację.` określa zdanie i przymiotnika nie określa.
Wybór między gospodarzami jest więc rozstrzygnięciem,
a nie wieloznacznością do zgłoszenia,
i dlatego sonda wyceniła każdego z nich osobno, zanim któryś wszedł do gramatyki.

Weszli wszyscy trzej: gospodarz dalszy kosztuje zdania, a kupuje prawdę o drzewie,
i po tym kursie olski przyjmuje każdego.

Gospodarze są trzej, a wariantów cztery:
gramatyka bez przysłówka, po jednym na gospodarza wycenianego osobno i sam olski.
`okolicznik` wpuszcza przysłówek do listy okoliczników,
czyli tam, gdzie stoi wyrażenie przyimkowe, i przed zdanie.
`przy przymiotniku` stawia go pod symbolem przymiotnika,
a bierze tam sam przysłówek stopniowany
([niżej](#naprawę-niesie-tagset-a-formalizm-ją-bierze)).
Gospodarz trzeci osobnego wariantu nie ma,
bo bez listy okoliczników nie wyprowadza niczego,
więc jego cena nie jest osobną liczbą.

Okolicznik kupuje nad Składnicą kilkaset zdań,
czyli podnosi liczbę przyjętych o ponad jedną trzecią,
a określenie przymiotnika kilkanaście razy mniej.
Obaj razem kupują mniej niż okolicznik sam,
więc drugi gospodarz dopisany do pierwszego nie kupuje nic i odbiera mu zdania.
[Krzywa pokrycia](design-notes.md#making-the-trade-measurable)
przewidziała, że dopisanie bywa droższe od tego, co kupuje,
i jest to najciaśniejszy przypadek, jaki się tu trafił:
odbierają sobie zdania dwie połowy jednej konstrukcji,
a nie dwie konstrukcje z osobna.

Cena nie jest przy tym stratą na zdaniach, które olski przyjmował przed przysłówkiem:
jednoznaczności nie traci ani jedno z nich, w żadnym wariancie.
Płaci się ją zakupem pierwszego gospodarza:
zdanie, które każdy z nich osobno przyjmuje jednym czytaniem,
przy obu naraz wychodzi dwoma.

```text
Program zabawy był ściśle ustalony.
```

Pod `okolicznik` orzecznikiem jest `ustalony`, pod `przy przymiotniku`
`ściśle ustalony`, a pod olskim te dwa czytania stoją obok siebie.

Zakupem gospodarza dalszego jest prawda o zdaniach, które zostają.
Pierwszy gospodarz sam wypuszcza jedno na czterdzieści zdań przyjętych
z czytaniem, w którym przysłówek jest okolicznikiem zdania,
choć określa słowo stojące zaraz za nim.
Drugi gospodarz zdejmuje z tych czytań te przed przymiotnikiem,
a trzeci resztę, czyli te przed przysłówkiem,
i po nim nie zostaje ani jedno
([niżej](#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę)).
Zdanie przyjęte z takim drzewem jest droższe od wieloznacznego,
bo `valid` ktoś przeczyta
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
więc każdy gospodarz dalszy zamienia werdykt fałszywy
na werdykt o dwóch czytaniach.
Kurs wychodzi przez to bliski jednemu do jednego:
zdań przyjętych ubywa mniej więcej tyle, ile ubywa czytań nieprawdziwych,
a przy gospodarzu trzecim ubyło jednych i drugich dokładnie tyle samo.

W tę samą stronę idzie zgodność z drzewem wzorcowym.
Okolicznik sam czyta wbrew niemu jedno zdanie na kilkadziesiąt z tych, które kupuje,
a przy gospodarzach dalszych takich zdań jest mniej,
nie tylko w udziale, ale i w liczbie.
Gospodarz trzeci nie rusza przy tym ani jednego z nich:
odbiera jednoznaczność zdaniom czytanym zgodnie z drzewem wzorcowym,
a zdania czytanego wbrew niemu ani nie zabiera, ani nie dokłada.
Drugi gospodarz sam myli się przy tym najczęściej ze wszystkich,
bo czyta wbrew drzewu jedno zdanie na osiem z tych, które kupuje sam:
zostają mu pomyłki na przysłówku odprzymiotnikowym,
który określa i zdanie, więc stopień nie rozdziela niczego —
`Oficjalnie cały Sejm RP śpi.` wychodzi z podmiotem `Oficjalnie cały Sejm RP`.
Ról odwróconych nie ma ani jednej, w żadnym wariancie.

Werdykt nazywa gospodarzy wprost, bo okolicznik przysłówkowy jest w nim rolą:

```sh
python3 -m olski.check --readings -c "Plik jest bardzo duży."
```

```text
<text>: ambiguous Plik jest bardzo duży.
                  2 odczytania, różne w rolach: okolicznik_przysłówkowy, orzecznik
                  - podmiot: Plik, orzecznik: bardzo duży, orzeczenie: jest
                  - podmiot: Plik, orzecznik: duży, orzeczenie: jest, okolicznik_przysłówkowy: bardzo → jest
olskie: 0 z 1 zdania; z odczytaniem: 1
```

Rolę niesie jeden z gospodarzy, i jest to decyzja, a nie przeoczenie.
Dwa czytania rozdziela przez to sama lista ról,
zamiast czekać na to, że czytelnik porówna dwa napisy orzecznika.

Nad rejestrem ustaw okolicznik kupuje w skali dziesięć razy mniejszej,
a drugi gospodarz dokłada tam zdanie, zamiast odejmować,
więc znak tej ceny zależy od rejestru,
a nie od samych gospodarzy.
Trzeci nie rusza tam ani jednego werdyktu, tak samo jak nad korpusem audytowym:
przysłówek przed przysłówkiem jest konstrukcją prozy prasowej,
a rejestr, o który olskiemu chodzi, nie pisze jej wcale.

Nad prozą tego repozytorium przysłówek daje wyprowadzenie,
a jednoznaczności nie daje.
Takim zdaniem jest to, o którym kolejka blokerów mówiła,
że stoi na przysłówku i na niczym więcej
([corpus.md](corpus.md#where-the-analyses-stop)):

```text
Po to ta czarna lista tu stała i cały wywód za nią dalej stoi.
```

Wyprowadzenie dostaje, jednoznaczności nie,
bo w czytaniu, które przysłówek mu daje, `za nią` ma dwóch gospodarzy.
Kolejka mówi więc, gdzie analiza stanęła, i nie mówi, co dopisanie kupi,
także wtedy, gdy zdanie stoi na jednej klasie.

Jedna klasa czytań przyszła razem z tą konstrukcją i nie jest przyłączeniem.
Morfeusz daje czytanie przysłówkowe formom, które ten rejestr pisze
jako przyimek albo spójnik — `wobec`, `gdy`, `jak` —
a okolicznik zdania bierze całą część mowy,
więc `Są oni obdarzeni rozumem i sumieniem i powinni postępować wobec innych
w duchu braterstwa.` ma trzy czytania z `wobec` w roli okolicznika,
w których `innych` jest dopełnieniem,
a `Program zapisuje ustawienia, gdy linter sprawdza tekst.` wyprowadza się
jako dwa zdania spięte przecinkiem, choć zdanie po przecinku jest podrzędne.
Jest to [czytanie, którego polszczyzna nie ma](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not),
a `admissible` po nie nie sięga, bo pyta o czytanie rzeczownikowe.
Kryterium na tę klasę nie jest przy tym oczywiste:
`blisko` i `jak` niosą czytanie przysłówkowe, którego polszczyzna używa,
więc warunek odsiewający przysłówek przy czytaniu przyimkowym zabrałby i je.
[TODO.md](../TODO.md) trzyma ruch wraz z ceną obu kryteriów, które mu się nasuwają.

### Naprawę niesie tagset, a formalizm ją bierze

Gospodarze spierają się o zdanie tylko wtedy,
gdy przysłówek stojący przed przymiotnikiem mógłby określać zdanie,
a Morfeusz tę różnicę niesie:
`tu`, `razem`, `dziś`, `teraz` i `nigdy` wychodzą jako `adv` bez stopnia,
a `bardzo`, `ściśle` i `szybko` jako `adv:pos`.
Stopień ma przysłówek odprzymiotnikowy, a pierwotny go nie ma,
i tylko pierwszy z tych dwóch określa przymiotnik.

Formalizm ma na to warunek i jest nim `niesie`:
`word("adv", niesie="degree")` bierze `bardzo`, a `tu` nie.
Wypisanie wszystkich wartości cechy tego nie mówi,
bo `word("adv", degree={"pos", "com", "sup"})` bierze `tu` tak samo jak `bardzo`.
Dlaczego warunek nie mieszka w unifikacji i co jeszcze jest obok niej,
wywodzi [kanał cech](design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne).

Naprawa jest z góry niepełna i taka wypadła.
Warunek oddaje pierwszemu gospodarzowi niespełna piątą część zdań,
które drugi mu bez niego odbiera,
a resztę drugi gospodarz odbiera nadal:
o te zdania spierają się przysłówki stopniowane i żadna cecha ich nie rozdziela.
Zmienia natomiast to, ile drugi gospodarz kupuje i jak często się myli:
kupuje o dwie piąte mniej zdań i myli się na nich trzy razy rzadziej,
bo dwie trzecie jego pomyłek pada bez niego na przysłówku bez stopnia.
Te trzy liczby wzięto nad gramatyką, w której przysłówka jeszcze nie było,
i żaden przebieg ich dziś nie powtarza:
wariant bez tego warunku nie jest grupą produkcji, tylko innym terminalem w tej samej,
więc sonda różnicowa nie ma go czym zdjąć,
a gramatyki wariantu branej funkcją żąda od tej maszynerii [TODO.md](../TODO.md).
Są przez to ceną, przy której warunek zapadł, a nie figurą o dzisiejszej gramatyce.

### Płaska lista okoliczników mówi o zdaniu nieprawdę

Pierwszy gospodarz nie jest darmowy, bo lista okoliczników jest płaska.
Sam wypuszcza `Program zapisuje ustawienia bardzo szybko.` jednym czytaniem,
a jego kształtem jest `okoliczniki(bardzo okoliczniki(szybko))`,
czyli dwa okoliczniki zdania obok siebie,
gdzie `bardzo` określa `szybko` i zdania nie określa wcale.
Streszczenie nazywa przy tym pierwszy z nich,
bo rola przysłówka nazywa okolicznik pierwszy tak samo jak rola przyłączana,
więc drugi widać dopiero w napisie zdania.
Instrument, który liczy zgodność nad bankiem drzew, tego nie widzi:
porównuje podmiot i dopełnienie, a nie miejsce okolicznika.

Liczy to osobne narzędzie, bo pyta o co innego niż pomiar wyżej:
tamten o werdykt, a ten o drzewo, którym werdykt wypadł.
Pełne wiersze drukuje `python3 -m harness.płaski`,
a te sprzed dopisania gospodarzy dalszych — ono z `--wariant okolicznik`.
Populacją są zdania przyjęte jednym czytaniem,
bo tam odpowiedź jest dokładna, a listę czytań zdania wieloznacznego
ucina granica wyliczania.

Klasy są dwie i różni je to, który gospodarz ma brakującą pozycję.
Przysłówek stopniowany przed przymiotnikiem dochodzi do drugiego,
a przed drugim przysłówkiem do trzeciego.
W olskim obie są przez to puste, i to jest zakup tych dwóch gospodarzy
wypisany osobno: przy samym pierwszym przypada na klasę pierwszą
trzy czwarte płaskich czytań, a na drugą reszta.

Liczba wariantu jest przy tym górnym oszacowaniem,
bo przysłówek stopniowany bywa okolicznikiem zdania
i stoi wtedy przed przymiotnikiem, którego nie określa,
jak w `Ostatecznie nowa ustawa wchodzi w życie.`
Które formy to wywołują, wypisuje każda z tych figur, i prowadzi w nich `bardzo`.
Oszacowanie sięga i przysłówka na czele zdania,
bo pod symbolem przysłówka stoi każdy okolicznik przysłówkowy,
a czoło zdania jest osobnym ciałem produkcji:
`Oficjalnie cały Sejm RP śpi.` liczy się przez to razem z resztą.
Nad rejestrem ustaw ani jedno zdanie przyjęte płaskiego czytania nie dostaje,
więc konstrukcja jest tu droga w rejestrze,
który olskiemu ustawia kolejkę, a nie w tym, o który mu chodzi.

## Przymiotnik w formie poprzyimkowej jest okolicznikiem, a nie wyrażeniem przyimkowym

`Reguła działa po polsku.` wyprowadza się, a `Reguła działa polsku.` nie:
Morfeusz daje takiej formie część mowy `adjp`, czyli formę, która poza przyimkiem nie stoi,
i osobno nie bierze jej żaden terminal, więc para wchodzi jednym ciałem.

Okolicznikiem, a nie wyrażeniem przyimkowym, bo pytanie, na które ta para odpowiada,
jest pytaniem przysłówka: `po cichu` odpowiada tam, gdzie odpowiada `cicho`.
Formalizm mówi to samo, bo `adjp` nie niesie przypadka i przyimek nie ma tu czym rządzić;
ciało wraz z powodem, dla którego głową jest forma, stoi w `olski/subset/grupa.py`.

Przyimka lista nie zawęża, i jest to cena wzięta świadomie.
`w polsku` wyprowadza się przez to tak samo jak `po polsku`,
choć polszczyzna pisze samo drugie.
Która forma `adjp` staje po którym przyimku, jest faktem o leksemie, a nie o gramatyce,
a lista pisana ręką odsiewałaby razem z tym `z bliska` i `od dawna`.
Jednoznaczności to nie kosztuje:
pary, której nikt nie pisze, nie ma w żadnym zdaniu, więc nie dokłada ona czytania żadnemu.

Nad prozą tego repozytorium wiersz `adjp`
[kolejki blokerów](pisanie-po-olsku.md#kolejka-czytana-po-formie-mówi-to-czego-nie-mówi-po-części-mowy)
obiecywał kilkanaście zdań,
a pozycja wyciąga z odrzucenia przeszło połowę z nich;
reszta staje po niej na blokerze następnym, bo zdanie odrzucone niesie zwykle kilka.
Wyciągnięte wychodzą prawie wszystkie wieloznaczne, a jednoznaczne wychodzi jedno,
i tym ta pozycja jest podobna do okolicznika w ogóle: kupuje czytanie, a nie zdanie olskie.

Cena liczona werdyktem wyszła zerowa:
sonda różnicowa nie znalazła nad tą prozą ani jednego zdania,
które traciłoby jednoznaczność, ani żadnego przejścia poza tymi dwoma w górę.
Miejsce, w którym cena mogłaby paść, jednak istnieje,
i jest nim forma niosąca obok `adjp` czytanie przymiotnikowe — `bliska`, `dawna`, `rzadka` —
bo tamto czytanie produkcje brały już przedtem.
Sonda liczy werdykty, więc czytanie dołożone zdaniu i tak wieloznacznemu
stoi poza jej zasięgiem, a `TODO.md` trzyma ten brak;
nad zdaniami cytowanymi w tej prozie, gdzie liczbę czytań widać zdanie po zdaniu
(`harness/cytaty.py`), nie przybyło ono ani jednemu.
