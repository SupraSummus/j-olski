# The subset, as implemented

What `olski/subset/` admits,
and the decisions that shaped it.
The constructions themselves are in
[konstrukcje-gramatyczne/](konstrukcje-gramatyczne/README.md),
and what olski takes for a word is in
[warstwa-leksykalna.md](warstwa-leksykalna.md).
For the theory behind the track, see [design-notes.md](design-notes.md).

## Wieloznaczność jest odpowiedzią, a nie znaleziskiem

Zdanie jest olskie, gdy gramatyka je wyprowadza.
Narzędzie nad tą gramatyką sprawdza zdania polskiego tekstu
i wydaje autorowi dwa rodzaje wierszy.
Znalezisko mówi, co w zdaniu poprawić,
i ma padać tam, gdzie poprawiłby też czytelnik.
Znaleziska są dwa: poprawka jednego znaku
([niżej](#poprawkę-jednego-znaku-poświadcza-gramatyka))
i zaimek, który wskazuje na dwie rzeczy naraz
([niżej](#zaimek-wskazujący-na-dwie-rzeczy-jest-drugim-znaleziskiem)).
One wchodzą do kodu wyjścia `olski-check` i do liczby znalezisk w podsumowaniu.
Odpowiedź mówi, co olski o zdaniu wie, i o nic nie prosi.
Wieloznaczność jest odpowiedzią:
zdanie o kilku odczytaniach różnego kształtu
([niżej](#co-się-liczy-jako-jedno-odczytanie))
dostaje wiersz z tymi odczytaniami, podsumowanie liczy je osobno,
a kod wyjścia i liczba znalezisk ich nie widzą.

Rozstrzygnęła to baza sądów (`próba/nkjp-sądy.txt`, `harness/sądy.py`).
Każde zgłoszenie wieloznaczności ocenione nad podkorpusem NKJP
czytelnik uznał za fałszywe,
a nad korpusem audytowym zgłoszenie to pada nad prawie każdym zdaniem
z pozycją przyłączeniową
([open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma)).
Reguła, która strzela nad większością zdań i nie trafia w żadne,
znaleziskiem nie jest, i ten sam powód zamknął pakiet reguł
([linter.md](linter.md#co-zamknęło-pakiet-reguł)).
Baza jest mała, a do zdjęcia mała wystarcza:
zgłoszenie wraca do znalezisk dopiero z sądem, który je potwierdza,
a takiego nie ma ani jednego.
Wraca przy tym kształtem, a nie całością,
bo baza dzieli sądy po tym, czym czytania się różnią:
rola dwóch grup o zlanych przypadkach jest pierwszym kandydatem,
a przyłączenie wyrażenia przyimkowego ostatnim.

Wieloznaczność zostaje w wydruku, bo mówi o zdaniu prawdę.
Zdanie, które pokazuje, o jaką prawdę chodzi:

```text
Koszt samej szynki przewyższa koszt szynki z dodatkami.
```

`koszt` jest mianownikiem albo biernikiem, bo synkretyzm rzeczowników m3 jest zupełny,
a polszczyzna dopuszcza i SVO, i OVS,
więc zdanie ma dwa odczytania i w każdym mówi rzecz przeciwną,
a czytelnik nie ma z czego poznać, które było zamierzone.
Nie robi tego samo porównanie.
Ten sam czasownik z podmiotem i dopełnieniem, których przypadki się nie zlewają,
daje jedno odczytanie:

```text
Chałka przewyższa zwykłą bułkę.
```

`chałka` jest mianownikiem i niczym innym, `bułkę` biernikiem i niczym innym,
więc OVS nie ma gdzie się wyprowadzić.
Narzędzie odczytań nie rozstrzyga, i jest to decyzja, a nie brak:
konwencja, że pierwsza grupa imienna jest podmiotem,
czytałaby się jednoznacznie tylko temu, kto tę konwencję zna,
a olski ma się czytać jak zwyczajna polszczyzna każdemu, kto mówi po polsku.
Cena tej decyzji jest zmierzona i mówi,
że ten sam wiersz dostaje `Operator ustala priorytet.`,
czyli zwykłe zdanie SVO, którego drugiego czytania czytelnik nie ma.
Dlatego wiersz jest odpowiedzią na pytanie, ile czytań zdanie ma,
a autor czyta go, kiedy o to pyta.

Zdanie, którego gramatyka nie wyprowadza, znaleziskiem nie jest,
dopóki nie dzieli go od czytania jeden znak
([niżej](#poprawkę-jednego-znaku-poświadcza-gramatyka)).
Olski go nie czyta i o jego polszczyźnie milczy,
a werdykt mówi wtedy, dokąd analiza doszła
([niżej](#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).
Nad prozą, której większości ten podzbiór nie bierze,
jest to zwykły przypadek, a nie sąd o zdaniu.
Czym milczenie z braku pokrycia różni się od wstrzymania się, wywodzi
[linter.md](linter.md#abstention-is-allowed).
Z tego samego powodu wydruk stoi na zgłoszeniu:
zdanie bez odpowiedzi i bez znaleziska nie dostaje ani wiersza,
a milczenie liczy się osobno.

Odpowiedź ma mówić o zdaniu, a nie o gramatyce.
Odczytanie, którego polszczyzna nie ma, zdejmuje się więc z gramatyki,
a odczytanie, które polszczyzna ma, zostaje w werdykcie,
choćby zdanie wychodziło przez nie wieloznaczne
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).
Jedno wykluczenie ogranicza zasięg tej odpowiedzi.
Fraza musi być ciągłym odcinkiem tekstu,
więc zdanie, którego drugie odczytanie potrzebuje frazy nieciągłej,
wychodzi z jednym odczytaniem,
a werdykt nie mówi nic o odczytaniu, którego nie umiał wyprowadzić.
Ile to zdań i co kosztowałoby wpuszczenie ich, mierzy
[design-notes.md](design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze).

Odwrócenia są tu dwa i stoją po to, żeby nikt ich nie przywrócił przez przeoczenie.
Najpierw olskie było zdanie o dokładnie jednym odczytaniu, a zdanie o dwóch olski odrzucał.
Ta jedna własność ustawiała wiersz podsumowania, kod wyjścia i pierwsze zdania README,
więc zdanie wieloznaczne w polszczyźnie wychodziło odrzucone
za wieloznaczność, którą naprawdę ma
([open-questions.md](open-questions.md#odpowiedź-o-wieloznaczności-nie-mówi-czy-ma-ją-też-czytelnik)).
Potem wieloznaczność była znaleziskiem obok poprawki jednego znaku i zaimka,
i to ustawiało kod wyjścia tak, że zgłaszał co drugie czytane zdanie cudzej prozy.
Wielkiej litery na początku zdania nie zgłasza nic,
a ruch trzyma `todo/`.

## Co się liczy jako jedno odczytanie

Dwa wyprowadzenia są jednym odczytaniem, kiedy mają ten sam kształt.
Liczy się więc to, co strukturę zmienia:
która fraza jest podmiotem, co jest dopełnieniem
i gdzie przyłącza się modyfikator.

Nazwą jest odczytanie, a nie czytanie.
Czytanie nazywa po polsku czynność albo posiedzenie —
projekt ustawy ma w Sejmie pierwsze czytanie —
więc jako nazwa wyniku było kalką z angielskiego `reading`.
Odczytaniem polszczyzna nazywa wynik i tak mówi o przepisie,
który dopuszcza dwa odczytania.
Dawną nazwę poprawiamy przy okazji,
a nowy tekst pisze się od razu nową.

Z liczenia odczytań wyłączone są rozmyślnie trzy rzeczy,
a każda z innego powodu.

- **Lematy.** `zapisuje` należy i do `zapisywać`, i do `zapisować`.
  Polskie formy są homonimiczne wszędzie,
  więc liczone jako wieloznaczność odrzuciłyby prawie całą polszczyznę.
  Wieloznaczność leksykalna jest do rozstrzygnięcia dla czytelnika.
- **Wartości cech.** To, czy fraza stanęła na nijakiej mnogiej,
  czy na męskiej pojedynczej,
  nie jest rzeczą, między którą czytelnik wybiera.
  Zgodność wymusiła już unifikacja.
- **Części mowy.** Tam, gdzie część mowy zmienia strukturę,
  różni te wyprowadzenia już kształt,
  więc `do` jako przyimek i jako nuta dalej są dwoma odczytaniami.
  Zostaje przypadek, w którym kształt jest ten sam,
  i tam nie ma czym różnicy uzasadnić.

Ostatnie z tych trzech jest odwróceniem
i stoi tu po to, żeby nikt go nie przywrócił przez przeoczenie:
część mowy liczyła się obok kształtu.
Rozstrzyga odsłownik.
Morfeusz daje formie `zdanie` odczytanie `subst` i odczytanie `ger`,
a produkcja z odsłownikiem w głowie grupy imiennej
dawałaby każdemu takiemu zdaniu drugie wyprowadzenie tego samego kształtu,
różniące się niczym, na co czytelnik mógłby zareagować.
Nie jest to jedna forma ani klasa rzadka.
Tę parę odczytań niosą rzeczowniki,
którymi ten rejestr mówi o samym sobie:

```sh
python3 -c 'import sys
from olski.morph import analyse
for forma in sys.argv[1:]:
    print(forma, sorted({r.tag.pos for r in analyse(forma)[0].readings}))' \
  zdanie czytanie wyrażenie polecenie wejście wyjście dopełnienie żądanie
```

Drugie wyjście z tej klasy było wykluczeniem w słowniku
i stanęło na tym, że nie ma czego wykluczyć.
Olski takie wykluczenie ma i pyta ono o odczytanie funkcyjne obok rzeczownikowego
([warstwa-leksykalna.md](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)),
a tutaj oba odczytania są nominalne,
i szersze kryterium kasowałoby odczytanie, które polszczyzna ma:
`zdanie` jest i rzeczą, i czynnością.
Wykluczenie odbiera formie odczytanie, którego czytelnik nie ma,
a to nie jest ten przypadek.

Odwrócenie kupuje nad Składnicą 180723 sześć zdań,
które pod żywą morfologią przechodzą z wieloznacznych do przyjętych,
i ani jednego pod złotą, gdzie anotatorzy wybrali po jednym odczytaniu na token;
totale obu przebiegów trzyma
[corpus.md](corpus.md#what-morphological-ambiguity-costs).

Te sześć zdań stoi na trzech parach części mowy i na dwóch mechanizmach.
Dwie pary bierze jeden terminal:
`Dziewczyna milknie zakłopotana.` stoi na `adj|ppas`,
a `Mam ogromną prośbę.` na `fin|impt`.
Trzeciej nie bierze żaden.
`Znam go.` ma `subst` obok `ppron3`,
a te dochodzą do grupy imiennej dwiema różnymi produkcjami,
z których każda robi ją z jednego słowa.

Ta trzecia jest zarazem odczytaniem, którego polszczyzna nie ma,
tyle że wziętym z drugiej strony.
`go` jest grą i jest nieodmienne dokładnie tak jak nuta,
więc to czytanie zdejmuje wykluczenie ze słownika
([warstwa-leksykalna.md](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)).
Werdyktu nad tym zdaniem wykluczenie i tak nie rusza,
bo dopełnieniem jest w obu czytaniach jedno słowo, czyli kształt jest ten sam.

Reszta tego, co się kupuje, przychodzi z odsłownikiem
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#rzeczownik-odczasownikowy-jest-głową-grupy-imiennej-a-nie-pozycją-przy-czasowniku)).
Bez odwrócenia ta głowa obniżałaby pokrycie, zamiast je podnosić,
bo każdemu zdaniu z formą taką jak `czytanie`
dawałaby drugie wyprowadzenie tego samego kształtu;
z odwróceniem zdanie już przyjęte nie ma jak stracić na niej jednoznaczności,
i dlatego cena tej głowy wyszła zerowa.

Rozróżnienie to jest tym, na którym
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure)
się przewrócił i to zapisał:
liczenie prób zamiast wyników
kazało tamtemu narzędziu milczeć nad wierszami, które zrozumiało bez reszty.

## Odrzucenie mówi, dokąd analiza doszła, a nie gdzie stoi usterka

Odrzucenie ma trzy przyczyny i werdykt rozdziela je trzema zdaniami,
bo za każdą stoi inna robota do zrobienia.
Pierwszą jest forma, po którą nie sięga ani jedna produkcja,
i tę werdykt nazywa wprost, bo widać ją przed rozbiorem;
[Świgra](swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)
trzyma ją osobno tak samo.
Dwie pozostałe są strukturą,
a rozdziela je to, dokąd doszła analiza częściowa
(`Las.najdalszy` w `olski/parse/las.py`).

Analiza staje wewnątrz zdania, przed formą, której nie wzięła żadna analiza częściowa.

```sh
python3 -m olski.check -c "Tory są dwa: gramatyka i skład."
```

Werdykt nazywa tam dwukropek,
czyli szew, którym to zdanie wychodzi poza podzbiór.
Albo analiza bierze każdą formę zdania i nie domyka całości:
`Gramatyka jest tania, a nie droga.` dochodzi do kropki,
bo drugi człon nie ma czasownika,
i werdykt mówi wtedy, że zdania nic nie zamyka.
Znak kończący nazwany jako zatrzymanie kazałby autorowi poprawić kropkę,
więc te dwa zdarzenia dostają dwa zdania.
Zatrzymanie wewnątrz zdania jest z tych dwóch częstsze:
nad prozą tych dokumentów pada tak przeszło osiem odrzuceń na dziesięć,
a kolejkę form, na których staje, drukuje sam werdykt.

```sh
python3 -m harness.markdown docs/ --into proza/
python3 -m olski.check proza/*.txt | grep -oP 'staje na „\K[^”]+' | sort | uniq -c | sort -rn
```

Kolejka ta stawia na czele `i`, `a`, `więc`, przecinek, dwukropek i `czyli`,
czyli spójnik i znak, którym zdanie tego rejestru dokłada człon.
Jest to inna kolejka niż ta ze Składnicy,
która rankinguje część mowy, a nie formę
([corpus.md](corpus.md#where-the-analyses-stop)).
Ściągać do niej nie ma czego, więc puszcza ją każda sesja.

Nazwane miejsce jest końcem najdłuższego przedrostka, który się analizuje,
i nie jest wskazaniem usterki.
Widać tę różnicę na zdaniu, którym [README](../README.md#co-działa) pokazuje odrzucenie:
`Nowa program zapisuje ustawienia.` staje na `ustawienia`,
choć niezgodna para stoi na czele zdania.
Przedrostek ten analizuje się swobodnym szykiem:
`Nowa` jest mianownikiem, a `program` biernikiem,
więc `Nowa program zapisuje` przechodzi jako podmiot, dopełnienie i orzeczenie
w tej właśnie kolejności, a `ustawienia` nie ma już czym być.
Werdykt mówi o analizie prawdę, a wskazania usterki nie obiecuje.

Czego gramatyka w tym miejscu oczekiwała, werdykt nie podaje,
i nie podaje dlatego, że na formę nie czeka tam nic.
Analiza częściowa, która na formę czeka i tę formę bierze,
przesuwa zatrzymanie za nią,
więc przejście po `_przed_formą` w `olski/parse/las.py` oddaje w miejscu zatrzymania
zbiór pusty nad każdym zdaniem tej prozy odrzuconym na strukturze.
Wydruk oczekiwań milczałby zatem dokładnie tam, gdzie autor jest zgubiony.

Zdanie odrzucone bywa przy tym oddalone od czytania o jeden znak,
i wtedy werdykt mówi nie tylko, dokąd analiza doszła, ale i co poprawić
([niżej](#poprawkę-jednego-znaku-poświadcza-gramatyka)).

## Poprawkę jednego znaku poświadcza gramatyka

Autor cytuje cudzysłowem maszynowym tam, gdzie ten rejestr pisze `„ ”`,
albo nie stawia kropki na końcu zdania.
Olski takiego zdania nie czyta, a dzieli je od czytania jeden znak,
i taka poprawka jest pierwszym z dwu znalezisk
([wyżej](#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)).

```sh
python3 -m olski.check -c 'Przepisem "Zasad techniki prawodawczej" jest ustawa.
Przepisem „Zasad techniki prawodawczej” jest ustawa.'
```

```text
<text>: Przepisem "Zasad techniki prawodawczej" jest ustawa.
        jedno odczytanie po poprawce jednego znaku: cudzysłów „ i ” w miejsce tego, którym zdanie cytuje
zdań: 2; wieloznaczne: 0; bez odczytania: 1; do poprawki jednym znakiem: 1
```

Zdanie drugie jest tym pierwszym po poprawce i werdykt o nim milczy,
bo gramatyka bierze parę `„ ”` i żadnej innej
([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).

Świadkiem jest tu gramatyka, a nie znak,
bo poprawka wchodzi do werdyktu dopiero wtedy,
gdy rozbiór poprawionego napisu daje odczytanie.
Reguła stojąca na takim świadku nie orzeka o niczym, czego przedtem nie sprawdziła,
więc nie żąda kalibracji, której brak zamknął pakiet reguł
([linter.md](linter.md#co-zamknęło-pakiet-reguł)).

Reguła na samym znaku odpowiada inaczej i jest to zmierzone.
Poprzednia wersja tej reguły dopisywała zdanie o cudzysłowie do każdej formy
bez licencji, którą cudzysłów otwierał albo zamykał,
i nad prozą tego repozytorium padała tak kilkadziesiąt razy, ani razu trafnie:
za każdym razem nad zdaniem angielskim,
w którym cudzysłów nie jest jedyną rzeczą, przez którą olski go nie czyta.
Ta sama proza nie daje dziś ani jednego trafienia.
Rejestrem, dla którego reguła powstała, jest korpus audytowy,
gdzie znak liczono i gdzie ma on rację w dwóch trzecich wystąpień
([firing-rates.md](firing-rates.md#quote-straight-fired-442-times-and-was-right-about-296)),
a poprawki poświadczonej gramatyką nad tym korpusem nikt nie zmierzył.

Poprawki są dwie i żaden napis nie pyta o obie.
Napis, którego nic nie punktuje jako zdania, pyta o znak na końcu,
i to ta poprawka rozdziela nagłówek od zdania bez kropki
([extraction.md](extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem)).
Zdanie punktowane i odrzucone pyta o cudzysłów.
Napis, w którym stoi jedno i drugie, wychodzi bez poprawki i tak ma być:
dzieli go od czytania nie jeden znak, tylko dwa.
Ceną każdej z nich jest drugi rozbiór nad tym samym zdaniem,
więc obie stoją za warunkiem tańszym od niego.
Poprawka cudzysłowu pyta przedtem o pierwszy i ostatni znak formy bez licencji.

Zdanie naprawialne zostaje odrzucone i pokrycie liczy je tak samo jak przedtem,
bo znalezisko mówi o autorze, a podzbiór mierzy się tym, co gramatyka wyprowadza.
Wiersz podsumowania liczy je przez to dwa razy,
raz jako znalezisko i raz jako milczenie.

Łącznika żadna poprawka nie obejmuje, choć myślnik ten rejestr pisze pauzą,
i nie stoi za tym kryterium, tylko cena.
Nazwa pliku i flaga, które też dają formę `-` bez licencji
([pisanie-po-olsku.md](pisanie-po-olsku.md#czego-brakuje-najbardziej)),
odsiewają się przy takim świadku same:
podmiana, po której zdanie się nie wyprowadza, poprawki nie wydaje.
Zostaje rachunek i ten jest zmierzony.
Nad prozą tego repozytorium formę `-` bez licencji ma kilkaset zdań odrzuconych,
a myślnik w jej miejsce nie daje odczytania ani jednemu z nich,
więc taka poprawka płaciłaby rozbiór za każde i nie zgłaszała nic.
Odwróci to rejestr, w którym ta podmiana zdanie wyprowadza,
a pomiar nad nim trzyma `todo/pomiar.md`.

Poprawka odstępu po kropce stoi poza tą klasą, a wyklucza ją rachuba zdań.
Kropka bez odstępu za nią — `niska.Cena` — nie jest granicą zdania
(`SENTENCE_END` w `olski/document.py`),
więc po poprawce olski czyta nie to zdanie, tylko dwa,
a werdykt o jednym zdaniu nie ma gdzie takiej odpowiedzi postawić.
Wpis o niej trzyma `todo/werdykt.md`.

## Naprawa całego słowa nie jest jednoznaczna

O naprawę całego słowa prosi autor, który chce, żeby olski wciągnął tekst z usterką.
Zdanie odrzucone dostaje wtedy jedno słowo w innej formie tego samego lematu,
jedno słowo skreślone albo jedno słowo dołożone,
a świadkiem zostaje ta sama gramatyka co przy poprawce znaku:
naprawa liczy się dopiero wtedy, gdy rozbiór poprawionego zdania daje odczytanie.
Formy, której słownik nie zna, naprawa ta nie dotyczy —
o niej rozstrzyga warstwa morfologiczna, a nie drugi rozbiór
([warstwa-leksykalna.md](warstwa-leksykalna.md#forma-o-której-słownik-milczy-jest-rzeczownikiem-nieoznaczonym)).

Naprawa prawie nigdy nie jest jedna i dlatego znaleziskiem nie jest.
Mierzy się to nad zdaniem zepsutym, a nie odrzuconym, bo odpowiedź ma być znana:
zdanie, które olski czyta, dostaje jedną formę podmienioną na inną formę
tego samego lematu, aż wypadnie z podzbioru.
Nad prozą tych dokumentów zepsutą w ten sposób
naprawa znajduje się w dziewięciu zdaniach na dziesięć,
a jednoznaczna jest w mniej niż co czwartym z nich.
W pozostałych zbiór ma kilka pozycji i każda z nich jest zdaniem polskim:
`Nowa program zapisuje ustawienia.` naprawia i `Nowy program`, i `Nowa programu`,
a oba te zdania olski czyta jednym odczytaniem.

Wyróżnić naprawę mogłaby miara jej naturalności, a kandydat jest jeden:
koszt, po którym las porządkuje czytania
([disambiguation.md](disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie)).
Suma kosztów całego drzewa, o którą pyta `todo/parser.md`,
nie postawiła naprawy prawdziwej za żadną konkurentką ani raz,
a wyróżniła ją rzadziej niż raz na pięćdziesiąt zdań:
jest bezpieczna i prawie bezczynna.
Wychodzi tak dlatego, że koszt jest zadeklarowany dla szyku,
dla miejsca okolicznika i dla formy odesłanej poza rejestr,
a podmiana jednej formy nie rusza żadnej z tych trzech rzeczy.
Dwie miary, które rozstrzygają częściej, rozstrzygają fałszywie:
liczba czytań stawia naprawę prawdziwą za konkurentką w co czwartym zdaniu,
a odległość znakowa w co trzecim.
Miara naturalności musiałaby przez to być kosztem zadeklarowanym dla naprawy,
a nie dla produkcji, i taka deklaracja żąda własnego pomiaru.
Sonda liczy przy tym sumę nad lasem przed unifikacją,
więc może ją zaniżyć, a nie zawyżyć.

Ruch ten kosztuje również tam, gdzie usterki nie ma.
Zdanie polskie, którego olski nie wyprowadza, bo brakuje produkcji,
też bywa oddalone o jedno słowo od odczytania —
nad tą prozą rzadziej niż jedno odrzucone na dziesięć —
a naprawy przeczytane ręką mówią o formie tam, gdzie brak jest w gramatyce.
`Dwa pierwsze zamyka deklaracja i podłoże ma je zamknięte.` naprawia `me`,
a `Środka nie wybiera się natomiast tam, gdzie fakt rozstrzygający nie stoi w żadnym słowniku.` naprawia `Środek`,
i oba zdania olski po takiej naprawie czyta jednym odczytaniem.
Zdaniu zdrowemu naprawa zmienia przez to znaczenie,
a brak w gramatyce nazywa usterką autora.

Miejsca naprawy nie podaje też zatrzymanie i to jest zmierzone.
Nad zdaniami zepsutymi jedną formą analiza staje na tej właśnie formie
rzadziej niż raz na pięćdziesiąt zdań,
a nad blisko trzecią częścią z nich dochodzi do końca i nie staje wcale.
Sekcja wyżej wywodzi to na przykładzie `Nowa program`,
a liczba mówi, że przykład ten nie jest wyjątkiem:
niezgodność cech nie wypada w przedrostku,
bo unifikacja przechodzi po lesie, a nie po tablicy.

Brakującego słowa naprawa nie nazywa, tylko wylicza.
Krawędź o dowolnych cechach dołożona do grafu segmentacji
domyka zdanie w kilku miejscach naraz i kilkoma częściami mowy,
bo szyk jest swobodny: `Program ustawienia.` domyka czasownik przed grupą imienną,
między grupami i za nimi, i to każdą formą osobową, jaką gramatyka bierze.
Takie dołożenie przyjmuje przy tym i zdanie, któremu nie brakuje nic:
`Program zapisuje ustawienia.` przyjmuje je kilkudziesięcioma sposobami,
więc pytanie „czy brakuje słowa” ma odpowiedź twierdzącą i nad zdaniem całym.

Odwróci ten ruch klasa napraw jednoznaczna z budowy,
taka jak dwie poprawki znaku wyżej, gdzie kandydat jest jeden,
albo rejestr, w którym usterka jest częsta.
Ten drugi warunek jest ten sam, który sekcja wyżej stawia poprawce znaku,
i mierzy się go na tym samym korpusie audytowym.

## Wpis korpusu usterek nazywa kształt zdania, a nie znaczenie słowa

`próba/usterki.txt` wylicza zgłoszenia, których autor potrzebuje,
i jest kolejką roboty, a nie listą życzeń.
Wpis wchodzi tam wtedy, gdy jego zgłoszenie ma świadka,
a świadka dają dwie drogi.
Pierwszą jest odczytanie: gramatyka zdanie wyprowadza,
a wykrywacz czyta jego drzewo — albo sam napis, kiedy drzewa nie potrzebuje.
Drugą jest naprawa: gramatyka zdania nie wyprowadza,
wyprowadza jedno zdanie poprawione,
i to odczytanie poświadcza zgłoszenie tak samo jak przy
[poprawce jednego znaku](#poprawkę-jednego-znaku-poświadcza-gramatyka).
Wpisu, którego zgłoszenia nie poświadcza ani jedna droga, ani druga,
nie zamyka żadna robota, więc kolejki nie ustawia,
a cel nad tym korpusem przestaje mówić, co by go osiągnęło
([roadmap.md](roadmap.md#cele)).
Rozstrzyga to jedno pytanie: co wykrywacz musiałby wiedzieć nad tym zdaniem?
Odpowiedź „kształt tego zdania” wpis w korpusie zostawia,
a odpowiedź „znaczenie tego słowa” zabiera go stamtąd.

**Zgłoszenie o zdaniu, którego polszczyzna nie ma, poświadcza naprawa, a nie produkcja.**
`Zespół programistów spotkali się rano.` jest zdaniem z usterką,
a gramatyka pilnująca zgodności takiego zdania nie wyprowadza.
Produkcja, która by je wpuściła, zdejmuje zgodność wszystkim zdaniom naraz,
czyli zabiera dokładnie ten warunek, o który wpis prosi,
i łamie obietnicę, że każde zdanie olskiego jest zdaniem polskim
([roadmap.md](roadmap.md#podzbiór-jest-umową-a-nie-zasięgiem)).
Odczytanie, które takiemu zdaniu ta gramatyka daje,
jest czytaniem, którego polszczyzna nie ma, i zabiera je kierunek
([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).
Samo odrzucenie zgłoszenia nie zastępuje, bo mówi tylko,
[dokąd analiza doszła](#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka).
Zostaje naprawa, i to jej wpisy o niezgodności żądają:
zgłoszenie o parze, która się nie zgadza, poświadcza odczytanie napisu,
w którym orzeczenie dostało formę, której żąda podmiot.

**Zgłoszenie jest jedno, choćby naprawa nie była.**
Naprawą jest tu całe orzeczenie, a nie jedno słowo:
`Lista błędów i ostrzeżeń zostały zapisane.` naprawia `została zapisana`,
czyli obie formy naraz, bo obie mają tę samą liczbę i ten sam rodzaj.
Formę tę rozstrzyga podmiot, więc przy jednym podmiocie naprawa jest jedna,
a przy dwóch kandydatach na podmiot są dwie
i każda nazywa tę samą parę, która się nie zgadza.
Ruszyć wolno przy tym samo orzeczenie:
to zdanie naprawia także `Listy` w miejsce `Lista`,
ale zdanie z `Listy` mówi co innego, bo list jest w nim kilka.
Werdykt nazywa przy tym parę, a nie napis do przepisania,
więc druga naprawa nie dokłada autorowi wyboru.
Tym ta klasa różni się od naprawy całego słowa, gdzie każdy kandydat
mówi co innego i wybór między nimi zostaje przy autorze
([wyżej](#naprawa-całego-słowa-nie-jest-jednoznaczna)).

**Usterka, o której orzeka znaczenie słowa, zostaje poza korpusem.**
`Idąc do pracy, padał deszcz.` olski wyprowadza
i po składni nie ma w tym zdaniu czego poprawić:
imiesłów zajmuje miejsce okolicznika, a zdanie nadrzędne ma podmiot.
Usterką jest to, że deszcz do pracy nie chodzi,
a orzeka o tym znaczenie, którego olski nie rozstrzyga
([roadmap.md](roadmap.md#podzbiór-jest-umową-a-nie-zasięgiem)).
Zdanie to podchodzi pod żądanie pozycji,
a ono czeka na zasób, którego to repozytorium nie ma
([walencja.md](walencja.md#werdykt-nazywa-żądanie-obsadzonej-pozycji)).
Korpus stawia więc wariant, w którym usterka jest kształtem:
`Zespół programistów spotkali się rano.` ma orzeczenie w innej liczbie niż podmiot,
a zgłoszenie o tej parze poświadcza naprawa, czyli druga z dwu dróg wyżej.
Ceną jest usterka, której autor nie dostanie zgłoszonej:
umowa jej nie obejmuje, więc odpowiada za nią sam.

**Pytaj o zgłoszenie, a nie o warunek, przy którym ono pada.**
`Idąc do pracy, zgubiono klucze.` ma orzeczenie bezosobowe przy imiesłowie,
warunek ten czyta się z drzewa i wpis o tym zdaniu stał tu z tego powodu.
Zgłoszenie nad nim kształtem jednak nie jest:
o tym, czy autor wykonawcę ukrył, czy nazwać go nie miał po co,
orzeka wykonawca domyślny obu orzeczeń, a nie drzewo zdania,
i nad cudzą prozą wychodziło z tego trafienie fałszywe za trafieniem
([linter.md](linter.md#reguła-o-imiesłowie-bez-podmiotu-myliła-się-w-każdym-trafieniu)).
Wpis wchodzi więc wtedy, gdy z kształtu zdania wychodzi samo zgłoszenie,
a nie wtedy, gdy wychodzi warunek, przy którym ono czasem pada.

**Wariant „poza gramatyką” odrzucamy, bo korpus jest kolejką.**
Rodzaj wpisu, którego cel nie liczy, zostawiłby usterkę znaczeniową w korpusie
i nie zobowiązywał nikogo.
Klasa wyjęta spod celu rośnie jednak każdą usterką, której nie umiemy zgłosić,
więc cel liczony bez niej mierzy w końcu to, co i tak umiemy.
Odwróci to plik osobny, który jest rejestrem usterek poza umową, a nie kolejką;
ceną są wtedy dwa pliki i pytanie, kto czyta ten drugi.
Wariant drugi — cel zostawiony nieosiągalnym — odrzuca zasada,
że cel nazywa, czym się go sprawdza
([roadmap.md](roadmap.md#cele)).

## Zaimek wskazujący na dwie rzeczy jest drugim znaleziskiem

Poprawka jednego znaku mieści się w jednym zdaniu, a to znalezisko nie mieści się.
`Są one czerwone.` dostaje ten sam werdykt po `Widzimy pole maków.`
i po `Maki rosną w garnkach.`,
choć po pierwszym z nich czytelnik ma jedną rzecz do wyboru, a po drugim dwie.
Rozbiór zdania z zaimkiem o zdaniu obok nic nie wie,
więc pyta o nie warstwa nad werdyktem (`olski/odniesienia.py`),
a kryterium bierze to samo, którym olski liczy odczytania: więcej niż jedno.

```sh
python3 -m olski.check -c "Narzędzie sprawdza zdania tekstu.
Autor poprawia je sam."
```

```text
<text>: Autor poprawia je sam.
        „je” wskazuje na „Narzędzie” albo „zdania”
zdań: 2; wieloznaczne: 0; bez odczytania: 0; niejasne odniesienia: 1
```

Zgłoszenie mówi o zdaniu prawdę sprawdzalną bez zaglądania czytelnikowi w głowę:
te dwie rzeczy naprawdę stoją w zdaniu obok i naprawdę zgadzają się z zaimkiem.
Czy czytelnik waha się nad nimi, mówi ono tak samo mało,
jak mówi o tym odpowiedź o wieloznaczności
([open-questions.md](open-questions.md#odpowiedź-o-wieloznaczności-nie-mówi-czy-ma-ją-też-czytelnik)),
i jest to ta sama cena wzięta drugi raz.
Rozdziela je częstość, i dlatego to jest znaleziskiem, a tamta nie.
Wieloznaczność melduje się nad prawie każdym zdaniem z pozycją przyłączeniową (tamże),
bo gramatyka wypisuje wszystkie czytania, jakie zdanie ma.
Zaimek melduje się rzadko: ta sama komenda puszczona na prozę tego repozytorium
zgłasza go raz na kilkadziesiąt zdań czytanych,
bo rzeczy podaje samo zdanie obok, a zaimek rozstrzygnięty na miejscu milczy.
Sądu czytelnika nad zgłoszeniem, które ta reguła wydaje, baza sądów jeszcze nie ma,
więc znaleziskiem jest ono na kredyt tej częstości;
sądy, które w bazie stoją, są o rozszerzeniu tej reguły
([niżej](#rzeczy-z-tego-samego-zdania-czekają-za-flagą)).

Kandydatów ubywa przy tym tam, gdzie gramatyka zdania obok nie wyprowadza,
i ubywa ich wyłącznie w jedną stronę:
milczenie z braku pokrycia może zgłoszenie schować, a wymyślić go nie może.
Ilu zgłoszeń nie widzieliśmy, nie mówi żaden przebieg, bo mówiłby o zdaniach,
których olski nie czyta.
Dlatego zaimek bez ani jednego kandydata zgłoszenia nie dostaje,
choć odniesienie wiszące jest usterką:
zero kandydatów znaczy i „nikt tej rzeczy nie nazwał”,
i „olski tamtego zdania nie przeczytał”, a warstwa tych dwóch nie rozróżnia.

Granicę stawia część mowy i stawia ją wąsko.
Wchodzi tu zaimek trzeciej osoby, czyli `on` wraz z każdą formą przypadkową.
Zaimek wskazujący nie wchodzi:
`to` i `ten` niosą w polszczyźnie łącznik, cząstkę i przydawkę,
a rozdzielenie tych robót jest osobną robotą.
Poza granicą zostaje przez to `to` w pozycji podmiotu akapitu,
które `CLAUDE.md` wylicza jako usterkę.
Zgłasza je osobna warstwa i osobnym kształtem, bo nie ma tam czego wyliczać:
zdanie podjęte przez ten zaimek rzeczą nie jest, więc kandydatów nie ma
([linter.md](linter.md#wykrywacz-chwytu-zgłasza-to-bez-rzeczownika-przy-sobie)).

## Rzeczy z tego samego zdania czekają za flagą

Cięcie na kropce nie jest cięciem, które robi czytelnik.
`Pies gonił kota, a on uciekł.` stawia go przed tym samym wyborem
co para zdań wyżej, a rzeczy stoją tam w składowym obok, nie w zdaniu obok.
Zaimek dzierżawczy sięga jeszcze bliżej, bo podejmuje rzecz nazwaną w swoim składowym:
`Jan poprosił Piotra o jego samochód.` nie odsyła do żadnego zdania wcześniejszego,
a wybór między Janem a Piotrem zostawia czytelnikowi.

Rozszerzenie, które te dwa zdania zgłasza, stoi za flagą
(`w_zdaniu` w `olski/odniesienia.py`).
Kawałkiem jest w nim zdanie składowe: najpierw własne, w części przed zaimkiem,
potem składowe stojące przed nim, jedno po drugim wstecz, a na końcu zdanie obok;
rozstrzyga pierwszy z nich, który nazywa cokolwiek zgodnego z zaimkiem.
Reguła dzisiejsza jest tym samym przebiegiem, w którym kawałek własnego zdania
rozstrzyga milczeniem zamiast listą rzeczy.

Za flagą rozszerzenie zostaje dlatego, że sądy czytelnika go nie awansowały.
Nad prozą NKJP wydaje ono trafienia, których reguła dzisiejsza nie ma;
czterdzieści z nich przeczytano i trafne są trzy
(`próba/nkjp-sądy.txt`, a wypisuje je `harness/sądy.py --nowe`).
Trafienia te noszą własną nazwę — `niejasne odniesienie w zdaniu` —
więc baza ocenia dwie reguły osobno i nie miesza ich w jednej liczbie,
a kod wyjścia nazwy spod flagi nie widzi.
Fałszywe są w większości jednym z czterech kształtów,
i to one nazywają, co trzeba zawęzić przed następnym podejściem:
kandydatem bywa druga głowa tej samej grupy — `radny Mitkiewicz`, `lewą nogą` —
czyli jedna rzecz policzona dwa razy;
bywa nim spójnik albo przyimek, który morfologia czyta też jako rzeczownik — `Kiedy`, `Od`;
bywa nim podmiot własnego składowego, którego zaimek dzierżawczy wyklucza,
bo o podmiocie mówi się `swój`;
a bywa nim rzecz, której nikt nie podejmuje, bo zdanie orzeka o niej co innego —
`nad ich szczebiotem` po `W gałęziach nawołują ptaki`.
Trzy pierwsze kształty zdejmuje zawężenie, a czwarty, którym jest ich większość,
nie schodzi żadnym, bo rozstrzyga o nim znaczenie, a nie zgodność.
Trzy trafne mówią, po co to rozszerzenie wraca:
`Na centralnie umieszczonym bolcu osadzamy krążek i dopiero wtedy naklejamy na nim
gotową etykietę.` nie mówi, na czym etykieta staje.

Sonda oceniająca puszcza flagę zawsze, i to jest jedyne miejsce, które ją włącza:
baza sądów jest tym, co rozstrzyga o awansie,
więc reguła czekająca na awans musi mieć czym trafienia wydać
([linter.md](linter.md#kolejna-reguła-zaczyna-się-od-zdania-z-usterką-a-kalibracja-przychodzi-przed-awansem)).

## What the grammar covers

- Clauses in all six orders the subject, the object and the verb stand in,
  from `Program zapisuje ustawienia.` to `Zapisuje ustawienia program.`
- Subjectless clauses, both imperative (`Zapisz plik.`)
  and pro-drop indicative (`Zapisuje ustawienia.`),
  with the object in front of the verb as well: `Cenę liczymy.`,
  the order `CLAUDE.md` writes its own rules in
- A verb before its subject, with an agreeing predicative after it or without one:
  `Są oni obdarzeni rozumem.`, `Nadchodzi druga rewolucja.`
- A predicative before the copula, which is the mirror of OVS:
  `Wejściem jest zwykły tekst polski.`
- Reflexive verbs, with `się` in either position beside the verb it belongs to,
  finite or not: `Rachunek zwraca się.`, `Rachunek się zwraca.`,
  `Cena zaczyna się otwierać.`
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika))
- An agreeing predicative, under the copula and under a verb that is not one:
  `Ludzie są wolni.`, `Ludzie rodzą się wolni.`
- A nominal predicative in the instrumental, under the copula and nowhere else:
  `Jan jest nauczycielem.`
  The copula is a closed list of lemmas
  ([walencja.md](walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
  which is what keeps the instrumental of `Kwitnie handel paszportami.`
  out of the predicative under every other verb;
  where it does stand under one, it is an adjunct
  ([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
  What the list leaves out is the copula that takes `się`:
  `okazać się` and `stać się` govern the same case
  and the production has no place for the particle.
- Okoliczność wyrażona narzędnikiem bez przyimka, przy każdym czasowniku
  i na każdym miejscu, na którym stoi okolicznik przyimkowy:
  `Mieszczanie zabili okna deskami.`, `Granica jest czasem granicą modułu.`
  Wysunięcia przed zdanie ta pozycja nie ma i nie ma go z pomiaru
  ([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika))
- Okoliczność wyrażona przyimkiem i formą, która poza przyimkiem nie stoi:
  `Reguła działa po polsku.`, `Mówi po cichu.`, `Widać to z bliska.`
  ([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#przymiotnik-w-formie-poprzyimkowej-jest-okolicznikiem-a-nie-wyrażeniem-przyimkowym))
- Liczebnik zgodny w orzeczniku, czyli zdanie mówiące, ile czegoś jest:
  `Tory są dwa.`, `Warstwy są dwie.`
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-orzeka-o-tym-ile-czegoś-jest))
- Negation, with the genitive it demands of an object,
  through an infinitive chain and into a fronted relative pronoun:
  `Program nie zapisuje ustawień.`, `Nie chcę czytać książki.`,
  `polszczyzna, której nikt nie napisał`
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem))
- What a verb takes, from a lexicon rather than from a production:
  `być` takes no accusative object,
  so `On jest wolny.` loses the reading in which `wolny` is one.
- Dopełnienie w celowniku obok drugiego wypełnienia, tam gdzie leksykon parę wpuszcza:
  `Parser pokazuje autorowi oba czytania.`,
  `Parser mówi autorowi, że zdanie czyta się dwojako.`
  ([walencja.md](walencja.md#celownik-obok-wypełnienia-jest-drugą-pozycją-ramy))
- Zdanie podrzędne obok dopełnienia w bierniku, tam gdzie leksykon tę parę wpuszcza:
  `Kierownik poinformował pracownika, że wniosek został odrzucony.`
  ([walencja.md](walencja.md#biernik-obok-zdania-podrzędnego-jest-drugą-pozycją-ramy))
- Forma, o której słownik milczy, jako rzeczownik o nieoznaczonym przypadku,
  rodzaju i liczbie — notacja tego rejestru, wersalik i nazwa narzędzia:
  `Zobacz docs/subset.md.`, `README mówi o podzbiorze.`,
  `Narzędzie Robocopy kopiuje pliki.`
  ([warstwa-leksykalna.md](warstwa-leksykalna.md#forma-o-której-słownik-milczy-jest-rzeczownikiem-nieoznaczonym))
- Liczba pisana cyfrą wraz z jednostką pisaną skrótem, jako cała grupa imienna:
  `Alokacja wymaga 2 GB.`
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii))
- Złożenie przymiotnikowe pisane łącznikiem: `Kościół ewangelicko-reformowany rośnie.`
  ([warstwa-leksykalna.md](warstwa-leksykalna.md#notację-i-łącznik-rozstrzyga-segmentacja))
- Myślnik pisany łącznikiem, czyli tak, jak pisze go klawiatura:
  `Cena jest niska - gramatyka jest bezkontekstowa.`
  ([warstwa-leksykalna.md](warstwa-leksykalna.md#notację-i-łącznik-rozstrzyga-segmentacja))
- A modal with its infinitive: `Program powinien zapisać ustawienia.`
- An infinitive as what any other verb takes,
  and a chain of them with no rule of its own:
  `Program pozwala zapisać ustawienia.`, `Wpis ma pomagać pisać.`
- Noun phrases with an adjective before or after the noun,
  a genitive modifier, or a prepositional modifier,
  and an adjective after the noun with a genitive under it as well:
  `dobrem wspólnym wszystkich obywateli`, which is how the register of statutes
  names a term and then says whose it is
  ([ustawy.md](ustawy.md#gramatyka-bierze-termin-z-dopełniaczem-bo-ten-rejestr-go-nazywa))
- Przydawka imiesłowowa, czyli imiesłów przy rzeczowniku, w obu szykach przydawki
  i wraz z dopełniaczem, którego jego czasownik żąda:
  `Wymienione zadania są obowiązkowe.`, `Reguła sięgająca znaku jest tania.`
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik))
- Rzeczownik odczasownikowy jako głowa grupy imiennej, w każdej pozycji, którą
  ma rzeczownik: `Przyłączenie jest tanie.`, `Wyznaczenie granicy jest tańsze.`
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#rzeczownik-odczasownikowy-jest-głową-grupy-imiennej-a-nie-pozycją-przy-czasowniku))
- Pronouns, and with them first and second person subjects.
  Person comes from the subject rather than being fixed at the third,
  so `Ja zapisuje plik.` is a disagreement
  in the way `Nowa program` is one.
- Zaimek dzierżawczy przed rzeczownikiem, czyli `jego`, `jej` i `ich`:
  `Jego skutki są znane.`, `Ich cena jest niska.`
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#zaimek-dzierżawczy-jest-dopełniaczem-przed-rzeczownikiem))
- Coordination, of noun phrases, of adjective phrases, of attributes,
  of prepositional phrases and of clauses, joined by a conjunction or by a comma.
  The conjunction is the one Polish writes without a comma in front of it,
  on all five levels, so `Plik jest nowy ale duży.` has no derivation
- Ciąg współrzędny wyrażeń przyimkowych, czyli piąty z tych poziomów,
  z przyimkiem powtórzonym przed każdym członem:
  `Leksykon mówi o bierniku i o bezokoliczniku.`
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#wyrażenie-przyimkowe-koordynuje-się-tak-jak-grupa-imienna))
- Przydawka złożona z kilku przymiotników, w obu szykach przydawki,
  wraz z tym szykiem, w którym człony dzielą między siebie rzeczownik:
  `Nowy i tani parser zapisuje ustawienia.`, `Warstwy trzecia i czwarta pracują.`
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#przydawka-koordynuje-się-i-rozdziela-rzeczownik-tylko-za-nim))
- Two clauses joined by a comma and a conjunction at once,
  which is how Polish punctuates the conjunctions it puts a comma in front of:
  `Plany są niczym, ale planowanie jest wszystkim.`
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają))
- Przecinek zamykający zdanie podrzędne przed spójnikiem bez przecinka:
  `Dokument mówi, że cena jest niska, i liczy cenę.`
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#przecinek-zamykający-należy-do-zdania-podrzędnego-a-nie-do-spójnika-za-nim))
- Człon, którego czasownik ten rejestr opuszcza:
  `Milczenie obejmuje wybór, a nie zdanie.`,
  `Warstwa pyta o Przyłączenie, czyli o obiekt składniowy.`
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze))
- Spójnik stojący wewnątrz swojego zdania, a nie na jego czele:
  `Milczenie jest zatem wartością.`, `Reguła jest bowiem tania.`
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-wewnątrz-zdania-ma-jedną-pozycję-i-jedno-odczytanie))
- Ten sam spójnik na czele całego zdania, wiążący je z poprzednim:
  `I nikt tego nie zauważył.`, `Zatem milczenie jest wartością.`
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-na-czele-zdania-wiąże-je-z-poprzednim))
- Spójnik skorelowany, czyli powtórzony przed każdym członem,
  na poziomie zdaniowym i imiennym:
  `Ani parser nie rośnie, ani linter nie sprawdza.`,
  `Ani parser, ani linter nie rośnie.`
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-skorelowany-powtarza-się-przed-każdym-członem))
- A colon opening a clause or a noun phrase,
  which is how this register introduces an explanation,
  and a semicolon or a dash separating two clauses:
  `Cena jest niska: gramatyka jest bezkontekstowa.`,
  `Gramatyka ma dwie role: podmiot i dopełnienie.`
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają))
- Tryb przypuszczający, czyli czas przeszły z cząstką `by` za sobą:
  `Czytelnik nie odzyskałby ról.`, `Napisałbym program.`, `Zażądałem, by wyszedł.`
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#tryb-przypuszczający-jest-jedną-cząstką))
- Czas przyszły w obu rolach formy `bedzie`:
  sama orzeka o podmiocie, a nad czasownikiem niedokonanym składa czas złożony —
  `Cena będzie niska.`, `Program będzie zapisywał ustawienia.`,
  `Program będzie zapisywać ustawienia.`
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony))
- Predykatyw, czyli słowo, które orzeka bez podmiotu i bez czasownika:
  `Trzeba czytać dokumenty.`, `Widać granicę w odpowiedzi.`, `Nie wiadomo.`
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika))
- Cząstka przy zdaniu i wewnątrz grupy imiennej:
  `Program już zapisuje ustawienia.`, `Już program zapisuje ustawienia.`,
  `Nawet ptaki przestały śpiewać.`
  ([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#cząstka-ma-dwóch-gospodarzy-i-przy-jednym-dostaje-etykietę))
- Cząstka przybliżająca przed liczebnikiem, czyli granica, którą ten rejestr
  pisze zamiast liczby dokładnej: `Kupuje przeszło sto zdań.`
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#cząstkę-przybliżającą-przyłącza-liczebnik-a-nie-grupa-imienna))
- Cudzysłów obejmujący grupę imienną, czyli tytuł albo termin cytowany:
  `Same „Zasady techniki prawodawczej” stoją poza tą sumą.`
  Grupa przechodzi przez niego cała, więc odmienia się wedle roli, w której stanęła.
- Nawias obok zdania składowego, czyli wtrącenie, którym ten rejestr dopowiada:
  `Zdanie stoi (docs/subset.md).`, `Cena jest niska (niżej).`
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania))
- Para myślników obejmująca wtrącenie w środku zdania, tam gdzie staje okolicznik:
  `Zepsute miejsce — w prozie czy w kodzie — nie potrzebuje lepszej wersji.`,
  `Reszta jest prywatna — nazwa funkcji w module — i rusza ją zwykła robota.`
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#para-myślników-obejmuje-wtrącenie-w-środku-zdania-a-nawias-na-jego-końcu))
- The past tense, agreeing with the subject in gender as well as in number,
  and with the person clitic Morfeusz cuts off the form:
  `Program zapisywał ustawienia.`, `Napisałem program.`
  What the form does to agreement is [konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku)
- A `że` clause as what a verb takes, which is a position in its frame
  rather than a construction beside the others:
  `Mieszkańcy grożą, że zablokują ulice.`
- Okolicznik wyrażony zdaniem, przed swoim zdaniem i za nim:
  `Program zapisuje ustawienia, gdy linter sprawdza tekst.`
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania))
- A relative clause on a noun phrase, agreeing with it in number and gender,
  with the pronoun standing for the subject, for the object,
  for the object in the genitive its verb's frame demands
  (`cena, której żądamy`, `Kogo dotyczy zmiana?`,
  [konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#dopełniacz-z-ramy-wysuwa-się-na-czoło-a-celownik-nie)),
  or under a fronted preposition together with the group it stands in:
  `Widoczny jest wzrost aspiracji społeczeństwa, które chce zdobywać wykształcenie.`,
  `ustawy, na podstawie której jest ono wydawane`
  The group carries the number and gender of the pronoun rather than of its own head,
  because it is the pronoun that agrees with the antecedent;
  the construction is argued
  [konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)
- Zdanie względne z zaimkiem `co`, o poprzedniku zaimkowym albo zdaniowym,
  nad zdaniem składowym i nad całym ciągiem współrzędnym:
  `To, co mogło się zepsuć, jest tanie.`,
  `Cena jest niska, co przekreśla sens działań.`,
  `Bierzemy ostry zakręt, dzięki czemu unikamy zderzenia.`
  Rzeczownika ten zaimek za poprzednik nie bierze, i to jest cała różnica
  między nim a `który`
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie))
- Zdanie pytające o grupie imiennej na czole,
  w pozycji podmiotu, dopełnienia i wyrażenia przyimkowego:
  `Który aktor robi na tobie największe wrażenie?`, `Które zadania gmina wykonuje?`,
  `W którym roku ustawa weszła?`
  Grupą pytajną jest zaimek przy rzeczowniku, a nie sam zaimek,
  i jest ona rolą, którą werdykt nazywa, bo mówi, o co zdanie pyta.
  Pod przyimkiem stoi ta sama grupa, więc pozycja trzecia jest drugim czołem,
  a nie trzecim kształtem grupy.
- Pytanie zależne jako to, co czasownik bierze,
  czyli pozycja ramy osobna od pozycji zdania z `że`:
  `Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.`
  Spójnika ono nie ma, bo podporządkowuje sam zaimek.
- Pytanie o okoliczność, w obu miejscach, w których pytanie stoi:
  `Dlaczego gramatyka rośnie?`, `Pyta, dlaczego gramatyka rośnie.`
  Wysunięty jest tu przysłówek, a nie rola, więc zdanie pod nim jest całe,
  a lematy wchodzą pojedynczo, bo rozdziela je reszta czytań, które mają
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#pytanie-o-okoliczność-wysuwa-przysłówek-a-zdanie-pod-nim-jest-całe))
- Kopuła opuszczona przy jednym rzeczowniku, czyli zdanie składowe bez czasownika:
  `Przepisy, o których mowa, obowiązują.`, `Mowa o zadaniach.`
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat))
- Łącznik `to` między dwiema grupami w mianowniku, czyli drugie zdanie bez czasownika:
  `Flaga to płat tkaniny określonego kształtu.`, `Parser to nie kompilator.`
  Podmiotem jest grupa za łącznikiem, a orzecznikiem ta przed nim,
  a grupa przed łącznikiem jest córką opuszczalną: `To prawda.`, `To nie kot.`
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim))
- Ten sam łącznik przy formie osobowej kopuli, w trzech szykach:
  `Był to nieforemny chłopak.`, `To są oczywistości.`, `Kot to jest zwierzę.`
  Kopula zgadza się tu z podmiotem stojącym za łącznikiem,
  a przeczenie wchodzi tymi ciałami samo: `Parser to nie jest kompilator.`
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#przy-kopuli-ten-sam-łącznik-ma-trzy-szyki-a-zgodność-wybiera-podmiot))
- Przysłówek u trzech gospodarzy: jako okolicznik zdania, w każdej pozycji, którą
  okolicznik ma (`Program zapisuje ustawienia szybko.`, `Teraz program zapisuje
  ustawienia.`), oraz jako określenie przymiotnika i drugiego przysłówka, gdzie
  stoi sam przysłówek stopniowany (`Koszt bardzo dużego pliku jest niski.`,
  `Program zapisuje ustawienia bardzo szybko.`).
  ([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy))
- Any number of prepositional adjuncts on one verb,
  because `postępować wobec innych w duchu braterstwa` has two
- Prepositional phrases, with the preposition governing the case.
  One lemma stays out, by name: Morfeusz reads `a` as the preposition
  of `dwa bilety a pięć złotych`, which this register does not have
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#rozdzielające-a-nie-jest-przyimkiem-tego-rejestru))
- A prepositional phrase in front of the clause,
  which modifies the clause rather than any noun in it
- An adjunct in every other position a prepositional phrase can follow
  a noun phrase in: around the verb in each of the orders,
  before the object, after a noun that already carries
  an adjective or a genitive, and after a participle.
  The positions are one decision rather than a list,
  and [Przyłączanie wyrażeń przyimkowych](#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)
  is where it is taken, enumerated and priced.
- Agreement throughout, as unification rather than as a separate check:
  `Nowa program zapisuje ustawienia.` has no derivation at all

Agreement being the parse rather than a check on the parse
is what makes the rejection precise.
There is no rule that says an adjective must agree with its noun.
There is only a production that shares a variable between them,
and a sentence that cannot satisfy it is not in the language.

## Zdanie deklaruje córki, a warunek deklaruje szyk

Produkcja mówi naraz dwie rzeczy: z czego zdanie się składa
i w jakiej kolejności te córki stoją.
Rozdzielone, te dwie rzeczy mieszczą się w kilku deklaracjach,
z których rozwinięcie pisze kilkadziesiąt ciał `zdanie_składowe`.
Deklaracja wymienia same córki,
warunek precedencji obok niej mówi, które ich przestawienia wchodzą,
a rozwinięcie składa jedno z drugim przed rozbiorem
(`olski/precedencja.py`).
Kończy się ono przed tablicą Earleya, więc tablica dostaje ciała wypisane.
Olski zajmuje przez to szczebel 1 [drabiny](design-notes.md#the-cost-ladder)
i płaci dokładnie tym, czym ten szczebel każe płacić:
preprocesorem gramatyki, a nie innym parserem.

Warunek wyklucza jeden szyk — ten, który zdanie składa już z podmiotu
i orzeczenia — i mówi to wprost, zamiast go przemilczeć.
Tego żąda od tej gramatyki decyzja o szyku wyżej —
szyk spoza olskiego ma być wykluczony warunkiem, a nie brakiem ciała —
i żąda tego samego od każdego szyku dopisanego później.

Miejsce na okolicznik wylicza to samo rozwinięcie.
Reguła jest jedna: okolicznik staje po każdej córce, która jest grupą,
oraz na końcu zdania, którego nie zamyka orzeczenie —
to bierze swój okolicznik samo, przez `wypełnienia`.
Pierwsza połowa tej reguły jest odpowiedzią na przyłączenie oddawane czytelnikowi
([niżej](#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)):
gdzie grupa imienna bierze wyrażenie przyimkowe za sobą,
tam musi umieć wziąć je też zdanie.

Reguła obejmuje przy tym córkę czasownikową,
bo polszczyzna okolicznik między czasownikiem a podmiotem stawia.
Bez tej pozycji płaci się w obu walutach naraz:
`Trwa w tej sprawie dochodzenie.` nie wyprowadza się wcale,
a `Zapisuje w pliku program ustawienia.` wychodzi jednym czytaniem,
w którym `program ustawienia` jest dopełnieniem,
i nie wychodzi tym, w którym `program` zapisuje `ustawienia`.
Drugie z tych dwóch jest tą samą pomyłką,
przed którą broni [reguła o obu czytaniach](#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
a po werdykcie jej nie widać, bo o takim zdaniu narzędzie milczy.
Zawężenie takiego kształtu mieści się po rozwinięciu w jednym argumencie
deklaracji, a nie w kilkudziesięciu ciałach, z których żadne go nie wypowiada,
i dopiero wtedy da się je wycenić jednym przebiegiem.

Regułę liczy rozwinięcie, a nie ręka, i widać to na zdaniu względnym:
miejsc na okolicznik jest tam za wysuniętą rolą trzy,
a bez trzeciego `Ustawa, którą organ w tym trybie wydaje, jest tania.`
wychodzi jednym czytaniem, w którym `w tym trybie` dochodzi do `organ`,
a czytania z okolicznikiem przy `wydaje` nie ma skąd wziąć —
czyli milczenie nad zdaniem, które czytelnik czyta dwojako.

## Przyłączanie wyrażeń przyimkowych: olski nie wybiera

```text
Program zapisuje ustawienia w pliku.
```

`w pliku` dochodzi do czasownika albo do dopełnienia,
a to są dwa różne zdania o tym, gdzie te ustawienia są.
Oba wyprowadzenia są polszczyzną,
więc własność jednoznaczności to zdanie odrzuca.

Konstrukcja nie jest przy tym rzadka.
Niemal każde zdanie z wyrażeniem przyimkowym po dopełnieniu
jest wieloznaczne tak samo,
więc własność w tym brzmieniu
wyklucza dużą i zwyczajną część technicznej polszczyzny.

Porównanie, którym ten dokument się otwiera, na to trafia.
`przewyższać` porównuje pod jakimś względem —
w czym jedno przewyższa drugie —
i to brak tego względu każe `Chałka przewyższa zwykłą bułkę.`
czytać sztywno,
więc kto pisze to zdanie, ten ten wzgląd nazywa:
`Chałka przewyższa zwykłą bułkę pod względem smaku.`
A to znowu są dwa czytania,
jedno, w którym wzgląd należy do porównania,
i drugie, w którym należy do bułki.

Jedna pozycja z tego wychodzi i gramatyka ją bierze:

```text
Pod względem smaku chałka przewyższa zwykłą bułkę.
```

Wyrażenie przyimkowe określa polski rzeczownik tylko zza niego,
więc przed zdaniem nie ma rzeczownika, do którego mogłoby dojść,
i czytania, w którym smak należy do bułki, nie ma —
ani dla parsera, ani dla polskiego czytelnika.
Wysunięcie nie żąda od czytelnika niczego,
bo jest pozycją, którą język ma,
a co daje jego dopuszczenie nad bankiem drzew,
liczy [corpus.md](corpus.md#where-the-analyses-stop).

Wyjścia z tego są trzy: przyjąć koszt i odrzucać takie zdania,
przyłączać zawsze do czasownika, chyba że coś wymusza inaczej,
albo uznać, że te dwa czytania mówią o jednej sytuacji
i liczyć je za jedno.
Rozstrzyga między nimi prawdziwa polszczyzna, a nie gust.

### Bank drzew nie zna domyślnego przyłączenia

Ściągnięcie korpusu opisuje [corpus.md](corpus.md#fetching-it), a potem:

```sh
python3 -m harness.attachment Składnica-frazowa-180723/
```

W wydaniu 2018 Składnicy stoi 5 837 wyrażeń przyimkowych
w pozycji, w której olski widzi dwa czytania:
tuż za grupą imienną, która się na nich kończy,
więc przyłączenie do rzeczownika jest do wzięcia.
4 517 z nich stoi w zdaniu, w którym czasownik stoi przed wyrażeniem,
czyli przyłączenie do czasownika jest do wzięcia tak samo.
Wybór anotatorów rozkłada się na nich tak:

| dokąd doszło | wyrażeń | |
| --- | --- | --- |
| do rzeczownika | 2 698 | 59.7% |
| do czasownika albo do zdania | 1 378 | 30.5% |
| gdzie indziej | 441 | 9.8% |

„Gdzie indziej” to fraza wymagana szersza niż samo wyrażenie,
fraza przymiotnikowa i drugie wyrażenie przyimkowe;
żadne z tych trzech nie jest tym wyborem, o który tu chodzi.

Tabeli nie rusza zmiana w gramatyce, bo mierzone są cudze drzewa
i żadna produkcja olskiego nic do tych liczb nie wnosi.
Rusza ją wydanie korpusu i to, co `harness/attachment.py` liczy:
które kategorie są zdaniem, a które grupą imienną, i co znaczy „po czasowniku”.

Rozkład nie zmienia się na tyle, żeby przyimek go przewidywał.
Odsetki niżej liczą się z dwóch przyłączeń, o które tu chodzi,
a nie z całej tabeli wyżej, więc porównują się do 66.2%,
czyli do tego, ile z tych dwóch bierze rzeczownik.
Nad `w` jest to 65.0% do rzeczownika, nad `na` 65.2%,
nad `do` 60.6%, a najbardziej przechylone `dla` daje 83.1%,
więc nawet leksykon przyimków myliłby się co szóste zdanie,
a nad najczęstszymi co trzecie.

### Dlatego olski przyjmuje koszt

Wyjście drugie, przyłączaj do czasownika, jest czytaniem mniejszościowym:
stawiałoby na 30% wtedy, gdy polszczyzna wybiera 60%.
Konwencja, która myli się ponad dwa razy częściej, niż trafia,
nie jest konwencją, którą czytelnik ma;
to jest ten sam zarzut, który obalił ustalenie szyku na SVO,
tyle że tutaj z liczbą pod spodem.

Wyjście trzecie musiałoby twierdzić, że te dwa czytania
mówią o jednej sytuacji.
Klasa się na to nie zgadza, i mierzy to ta sama komenda:
576 przyłączeń do czasownika to frazy, których czasownik wymaga swoim schematem,
a 214 przyłączeń do rzeczownika to frazy, których żąda sam rzeczownik.
Po żadnej z tych dwóch stron nie ma parafrazy:
przeczytanie frazy wymaganej po drugiej stronie
łamie schemat tego, kto jej żądał.
Twierdzenia o jednej sytuacji nie da się postawić nad taką klasą.

Zostaje wyjście pierwsze i olski je bierze.
Autor wysuwa wyrażenie przed zdanie albo dzieli zdanie na dwa,
a olski melduje dwa czytania i zdania nie przyjmuje.

Ile ta decyzja kosztuje nad rejestrem, a nie nad bankiem drzew,
jest zmierzone osobno i wychodzi wysoko:
pozycję dwuznaczną niesie większość zdań polskiej dokumentacji,
a czytelnik ma nad nią jedno rozumienie.
Decyzji to nie przewraca, bo liczby wyżej mówią o tym,
czego nie da się zgadnąć, a nie o tym, co czytelnik widzi,
i te dwie rzeczy są prawdziwe naraz.
Rachunek wraz z próbką przeczytaną ręką trzyma
[open-questions.md](open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma).

### Przyjąć koszt to znaczy dać oba czytania wszędzie

Wyjście pierwsze wygląda na takie, które od gramatyki nie żąda niczego,
i to jest w nim mylące.
Odrzucenie jest uczciwe tylko wtedy,
gdy oba przyłączenia w ogóle mają gdzie się wyprowadzić.
Pozycja, w której gramatyka ma regułę na jedno z nich i nie ma na drugie,
nie odrzuca zdania — przyjmuje je z jednym czytaniem,
czyli wybiera przez przeoczenie to,
czego ta decyzja wybierać zabrania.

Takich pozycji jest tyle, ile zdanie ma miejsc,
w których za grupą imienną może stanąć wyrażenie przyimkowe,
i każda z nich jest zwyczajną polszczyzną:

- po podmiocie w szyku SVO, przed orzeczeniem
  (`Przybysze z najnowszej fali na ogół stronią od organizacji.`)
- po dopełnieniu i po podmiocie w szyku OVS
  (`Ustawienia w pliku zapisuje program.`)
- po każdej z dwóch grup imiennych w czterech pozostałych szykach
  (`Program ustawienia w pliku zapisuje.`)
- po podmiocie w szykach z czasownikiem na czele,
  przed orzecznikiem i za nim
  (`Trwa dochodzenie w tej sprawie.`)
- po orzeczniku wysuniętym przed kopulę i po podmiocie za nią
  (`Wejściem w tym trybie jest zwykły tekst.`)
- wokół łącznika `to`, w każdym jego ciele
  (`Był to w tej sprawie problem.`, `Są to w przeważającej większości lasy sosnowe.`)
- przed dopełnieniem, wewnątrz orzeczenia
  (`Program zapisuje w pliku ustawienia.`)
- po czasowniku w szykach z czasownikiem na czele
  (`Trwa w tej sprawie dochodzenie.`, `Zapisuje w pliku program ustawienia.`)
- za całym ciągiem współrzędnym, imiennym i przymiotnikowym,
  obok tego samego wyrażenia stojącego pod członem ostatnim
  (`pliki i katalogi w tym drzewie`, `wolni i równi pod względem swej godności`)
- po rzeczowniku, który już ma przy sobie przymiotnik, dopełniacz albo oba
  (`akcja zbrojna w Strefie Gazy`, `zadania ochrony ludności w gminie`),
  oraz po imiesłowie (`powiązani z interesami postkomunistów`)
- wewnątrz zdania względnego, wokół tego, co w nim zostało:
  po zaimku, między podmiotem a czasownikiem i na końcu
  (`reguła, która w tym trybie rozstrzyga`,
  `polszczyzna, którą ktoś w tym trybie napisał`)
- wewnątrz pytania, w tych samych trzech miejscach za grupą pytajną
  (`Który program w tym trybie zapisuje ustawienia?`)

Produkcji jest kilkadziesiąt,
bo pozycja powtarza się w każdym szyku, który ją ma,
a szyk jest w tej gramatyce osobną produkcją.
Ile ich jest dzisiaj, mówi `olski/subset/podrzędne.py`, a nie ten akapit:
rusza je każde dopisanie do gramatyki,
a liczy się je tak, jak się je zdejmuje.
Wiersz kosztuje przez to tym więcej ciał, im więcej szyków go ma,
i to jest w tej gramatyce cena jednego szyku więcej.
Przysłówek dostaje każdą pozycję listy okoliczników za darmo,
bo lista bierze go tak samo jak wyrażenie przyimkowe
([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy)),
a pytanie kosztuje najwięcej, bo ma własne czoło i własne orzeczenie.
Wiersz ostatni, czyli okolicznik po czasowniku,
ma pozycję w każdym szyku, w którym czasownik stoi przed grupą imienną.
Pozycję wewnątrz zdania względnego i wewnątrz pytania pisze
[rozwinięcie szyku](#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk), a nie ręka,
i jest to jedna pozycja w dwóch konstrukcjach z listy wyżej,
którą gramatyka pisana ręką miała w dwóch ciałach z trzech.
Wchodzi produkcja, w której `okoliczniki` stoją obok czegoś jeszcze,
w tym obok drugiego okolicznika,
oraz ta, w której `wyrażenie_przyimkowe` dochodzi do głowy mającej już przydawkę
albo do imiesłowu, czyli `człon_przymiotnikowy → adj|ppas wyrażenie_przyimkowe`.
Wchodzi też ciało, w którym `wyrażenie_przyimkowe` stoi
za całym ciągiem współrzędnym,
bo to samo wyrażenie mieści się zarazem pod członem ostatnim
([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#nothing-above-a-coordination-distributes-into-it)).
Nie wchodzi `człon_imienny → subst wyrażenie_przyimkowe`, czyli naga głowa z okolicznikiem:
jest to sama grupa imienna z wyrażeniem przyimkowym,
a nie drugie miejsce, w którym to wyrażenie się mieści.
Nie wchodzi z tego samego powodu `zdanie_składowe → orzeczenie_rzeczownikowe okoliczniki`,
czyli [kopuła opuszczona](konstrukcje-gramatyczne/podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat)
z okolicznikiem: rzeczownik orzekający grupą imienną nie jest,
więc temu wyrażeniu nie ma tam do czego dojść poza zdaniem składowym.
Granica jest wypisana dlatego, że liczba nad nią jest zapisana w dwóch dokumentach,
a policzyć ją drugi raz można tylko wtedy, gdy wiadomo, co się liczy.
Rusza tę liczbę każda produkcja dająca modyfikatorowi pozycję,
a policzenie jej na nowo jest odliczeniem ręką według granicy wyżej,
bo żaden przebieg jej nie drukuje.

Zniesienie tej ceny jedną produkcją rekurencyjną nie stoi
i mówi to sonda różnicowa (`harness/ruch.py`) nad wariantem,
który zdejmuje cztery ciała `człon_imienny` niosące to wyrażenie
i wpisuje `grupa_imienna → grupa_imienna wyrażenie_przyimkowe` w ich miejsce.
Wariant ten odbiera jednoznaczność blisko stu zdaniom Składnicy, a oddaje ją dwóm;
nad prozą tego repozytorium odbiera ją kilku, a oddaje jednemu.
Przyczyną jest zasięg produkcji:
cztery zdjęte ciała stoją przy głowie rzeczownikowej i odsłownikowej,
a produkcja rekurencyjna przyłącza wyrażenie do każdego kształtu głowy naraz,
w tym do zaimka.
Czterdzieści przeczytanych zdań traci jednoznaczność właśnie na tym —
`Nadziałem je na haczyk i zarzuciłem.`, `Kierują go na kursy dywersji.` —
a jedno na grupie liczebnikowej.
Odwraca to odrzucenie cecha odróżniająca głowę, która przyłączenie bierze,
od zaimka, który go nie bierze:
produkcja żąda wtedy tej cechy, zamiast brać wszystko.

Dwa z tych zdań pokazują, po czym brakującą pozycję poznać,
i nie jest to zdanie odrzucone.
`Ustawienia w pliku zapisuje program.` wygląda na pozycję,
w której zostaje samo czytanie rzeczownikowe, i nią nie jest:
gdy reguła OVS okolicznika nie bierze, wyrażenie dochodzi tylko do rzeczownika,
a zdanie wychodzi jednoznaczne tam, gdzie polski czytelnik ma oba czytania.
`Program zapisuje w pliku ustawienia.` wychodzi wtedy jednym czytaniem,
w którym `w pliku ustawienia` jest jedną frazą i dopełnienia nie ma wcale.
Oba zdania są wieloznaczne, a bez swojej pozycji każde z nich zostaje przyjęte,
i to jest ta różnica, której po samym werdykcie nie widać.

Nad Składnicą płaci się za to przyjętymi zdaniami,
a kupuje czytania, których olski nie czyta odwrotnie:
gramatyka bez pozycji przy grupie imiennej i przymiotnikowej
czyta wbrew ręcznemu rozbiorowi ponad dwieście zdań,
a z nimi dwadzieścia kilka, i żadne z nich nie jest przyłączeniem, które olski wybrał.
Ile ich dokładnie jest po obu stronach i czym są te, które zostają, trzyma
[corpus.md](corpus.md#agreement-which-matters-more-than-acceptance);
tutaj stoi rzędem wielkości, bo liczba zapisana w obu miejscach
rozeszła się już raz i nikt tego nie zauważył.

Klasa nie jest przez to zamknięta:
576 z 4 517 wyrażeń wyżej, czyli 13%, to frazy, których czasownik żąda swoim schematem,
a tam odczytanie rzeczownikowe schemat łamie, zamiast z nim konkurować.
Tyle zdjąłby [leksykon walencyjny](walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej) dochodzący do każdej pozycji,
a ten nie zdejmuje z klasy nic,
bo mówi o bierniku, a fraza wymagana jest tu przyimkowa.

## What it does not cover yet

Every one of these is a sentence that gets rejected and should not be:

- Nawias stojący w środku grupy imiennej:
  `Grupa imienna (ta z dopełniaczem) stoi tu.` jest odrzucone,
  gdzie `Grupa imienna stoi tu (niżej).` wyprowadza się
  i gdzie `Grupa imienna, która stoi (niżej), jest tania.` też,
  bo pozycje nawiasu są dwie i obie zamykają zdanie
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania)).
- Grupa imienna z elipsą głowy, czyli przydawka stojąca za rzeczownik,
  którego zdanie przed chwilą użyło:
  `Wszystkie obsadza jedna osoba.` jest odrzucone,
  gdzie `Wszystkie role obsadza jedna osoba.` wyprowadza się,
  i tak samo padają `ani jedna`, `dwie z nich` oraz `w każdym z nich`.
  Pozycja jest jednym ciałem — człon grupy imiennej złożony z samej przydawki —
  i to ciało wyceniła sonda różnicowa (`harness/ruch.py`).
  Nad bankiem drzew wyciąga ono pod złotą morfologią 89 zdań z odrzucenia,
  a jednoznaczność odbiera 168 zdaniom przyjętym wcześniej;
  z tych 89 zgadza się z drzewem wzorcowym 54, a 27 wychodzi przeczytanych na opak.
  Pod żywą morfologią wyciąga 54, a jednoznaczność odbiera 313.
  Nad prozą tego repozytorium przyjmuje kilkanaście zdań,
  a jednoznaczność odbiera kilkadziesiąt.
  Bilans jest ujemny w każdym z trzech przebiegów, i to jest cała odpowiedź:
  konstrukcję tę pisze ten rejestr zdanie po zdaniu,
  a płaci za nią autor przepisaniem
  ([pisanie-po-olsku.md](pisanie-po-olsku.md#czego-brakuje-najbardziej)).
- Forma przyimkowa zaimka w drugim członie ciągu pod jednym przyimkiem:
  `Program zapisuje ustawienia dla niego i niej.` jest odrzucone,
  gdzie `Program zapisuje ustawienia dla niego.` wyprowadza się,
  bo licencji udziela tej formie przyimek stojący przed nią
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą)).
- Two separating signs in one sentence, whether the same one twice or one of each.
  `Cena jest niska; gramatyka jest bezkontekstowa; parser jest tani.` is rejected
  where either half of it derives,
  and so is a sentence carrying a colon and a semicolon at once.
  Both signs stand at the level of the sentence
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają)),
  and `zdanie` carries neither, so there is nothing to recurse through.
  What such a production would have to settle is what the second sign separates:
  `(A; B); C` and `A; (B; C)` are the same string
  and a right-recursive body would give it two derivations,
  where the enumeration this register writes with semicolons is one flat list.
- Wypełnienie inne niż dopełnienie, wysunięte przed to, co orzeka bez podmiotu:
  `Czytać trzeba dokumenty.` jest odrzucone,
  gdzie `Usterkę zgłoszono.` wyprowadza się
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu)).
  `Programy trzeba czytać.` zostaje na zewnątrz z innego powodu:
  `programy` jest tam dopełnieniem bezokolicznika, a nie predykatywu,
  a dopełnienie wysunięte przed bezokolicznik, który je bierze,
  ma pozycję przy formie osobowej i tylko przy niej
  ([konstrukcje-gramatyczne/orzeczenie.md](konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze)).
- Dopełnienie w celowniku wysunięte na czoło:
  `Komu parser odpowiada?` jest odrzucone,
  gdzie `Kogo dotyczy zmiana?` wyprowadza się
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#dopełniacz-z-ramy-wysuwa-się-na-czoło-a-celownik-nie)).
  Pozycja jest tam wypisana dopełniaczem, a nie wzięta z leksykonu całą listą,
  i tamta sekcja trzyma pomiar, który celownik zatrzymał.
- Słowa, którymi ten rejestr pyta poza tymi, które już wchodzą
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz)
  oraz [konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#pytanie-o-rozstrzygnięcie-podporządkowuje-spójnikiem-a-nie-rolą)):
  `jak`, `jaki`, `ile`.
  Pozycja ta stoi na tej liście inaczej niż pozostałe, bo zdania z nią nie padają:
  `Pyta, ile ta gramatyka kosztuje.` wyprowadza się,
  a wyprowadza się czytaniem, którego polszczyzna nie ma.
  Morfeusz daje `jak` oraz `ile` część mowy `adv`, a `jaki` przymiotnikową,
  i olski bierze te części mowy całe, więc słowo pytające staje okolicznikiem
  albo przydawką, a pytania zależnego w takim zdaniu nie ma.
  Dopisanie ma więc dwie połowy i pierwsza z nich jest zawężeniem:
  czytanie okolicznikowe ma zejść przed czołem, które je zastąpi
  ([roadmap.md](roadmap.md#kierunek-werdykt-ma-mówić-prawdę-o-tekście)).
  Każde z tych słów żąda przy tym innego kształtu,
  więc jest to kolejka konstrukcji, a nie jedna pozycja:
  `jak` i `ile` mają poza pytaniem czytania, które ta gramatyka bierze —
  spójnik porównania i liczebnik rządzący dopełniaczem —
  a `jaki` żąda kształtu grupy pytajnej.
  Czwartym z nich było `dlaczego` i ono weszło
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#pytanie-o-okoliczność-wysuwa-przysłówek-a-zdanie-pod-nim-jest-całe)).
- Pytanie o miejsce: `Gdzie są przetrzymywani zakładnicy?` jest odrzucone,
  gdzie `Wchodzi w roadmap.md, gdzie każdy etap ma kryterium wyjścia.`
  wyprowadza się
  ([konstrukcje-gramatyczne/podrzędność.md](konstrukcje-gramatyczne/podrzędność.md#przysłówek-względny-otwiera-okolicznik-i-nie-określa-zdania)).
  Kształt tej pozycji gramatyka ma, odkąd bierze pytanie o okoliczność,
  i zostaje sam lemat, którego dopisanie zmierzono i odłożono:
  daje ono drugie czytanie każdemu zdaniu, w którym `gdzie` otwiera okolicznik
  pod czasownikiem spoza leksykonu, bo pytanie zależne stoi w ramie domyślnej.
  Wraca razem z zawężeniem tamtej pozycji, a `todo/` trzyma i pomiar, i ruch.
- Liczebnik pisany cyfrą przed rzeczownikiem, czyli ten, którym ten rejestr liczy:
  `Termin wynosi 14 dni.` jest odrzucone,
  gdzie `Termin wynosi czternaście dni.` wyprowadza się dwoma czytaniami
  i gdzie `Alokacja wymaga 2 GB.` wyprowadza się, bo po cyfrze stoi tam skrót.
  Cenę i warunek wejścia trzyma
  [cyfry olski nie bierze](konstrukcje-gramatyczne/grupa-imienna.md#cyfry-olski-nie-bierze-bo-cyfra-nie-niesie-morfologii),
  a liczebnik rządzący z dopełniaczem pojedynczym — `półtora roku` — stoi poza tym
  z tego samego powodu, z którego mnogi wszedł: rządzi innym przypadkiem.
- Narzędnik bez przyimka wysunięty przed zdanie:
  `Wieczorem wziął lustro.` jest odrzucone,
  gdzie `Wziął lustro wieczorem.` wyprowadza się.
  Pozycja ta jest zmierzona i odrzucona, bo zderza się z orzecznikiem wysuniętym
  przed kopulę
  ([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)),
  więc wraca dopiero z cechą, która te dwa rozdzieli.
- Liczebnik rządzący w orzeczniku:
  `Torów jest dwa.` jest odrzucone,
  gdzie `Tory są dwa.` wyprowadza się
  ([konstrukcje-gramatyczne/grupa-imienna.md](konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-orzeka-o-tym-ile-czegoś-jest)).
  Podmiot stoi tam w dopełniaczu, a orzeczenie nie zgadza się z niczym,
  więc jest to osobne ciało i osobna liczba, której nikt nie policzył;
  `todo/` trzyma ten przebieg.
- Zdanie orzekające samym istnieniem: `Bóg jest.` jest odrzucone,
  gdzie `Świeca zgasła.` wyprowadza się.
  Kopula wypadła z ciała, w którym przy czasowniku nic nie stoi,
  i wypadła po to, żeby narzędnik nie czytał się przy niej dwojako
  ([konstrukcje-gramatyczne/okolicznik.md](konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika)).
- Człon bez czasownika wtrącony w środek zdania, a nie postawiony na jego końcu:
  `Skład, czyli Morfeusz, jest tani.` jest odrzucone,
  gdzie `Parser jest tani, czyli Morfeusz.` wyprowadza się
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze)).
  Pozycja jest jedna i stoi na końcu zdania składowego, tak samo jak pozycja
  nawiasu, a miejsce w środku zdania ma odtąd para myślników
  ([konstrukcje-gramatyczne/zdanie-złożone.md](konstrukcje-gramatyczne/zdanie-złożone.md#para-myślników-obejmuje-wtrącenie-w-środku-zdania-a-nawias-na-jego-końcu)).
  Człon w tym miejscu żąda przecinka po obu stronach,
  a przecinek zamykający jest w tej gramatyce ciałem osobnym, nie cechą,
  więc pozycja wpuściłaby w środek zdania także człon niedomknięty;
  `todo/` trzyma ten przebieg.
- Nazwa postawiona przy rzeczowniku bez spójnika, kiedy słownik tę nazwę zna:
  `Bank drzew Składnica mierzy gramatykę.` jest odrzucone,
  gdzie `Składnica jest bankiem drzew.` wyprowadza się
  i gdzie `Narzędzie Robocopy kopiuje pliki.` wyprowadza się,
  bo `Robocopy` przypadka nie niesie i przechodzi pod żądaniem dopełniacza
  ([warstwa-leksykalna.md](warstwa-leksykalna.md#forma-o-której-słownik-milczy-jest-rzeczownikiem-nieoznaczonym)).
  Ten rejestr nazywa tak każdy artefakt zewnętrzny — korpus Składnica,
  słownik Morfeusz — a od członu bez czasownika różni tę konstrukcję to,
  że spójnika nie ma, więc nie ma czym jej wpuścić bez wpuszczenia zarazem
  dwóch rzeczowników postawionych obok siebie przez pomyłkę.
  Znamię to ma nazwa, o której słownik milczy, bo przypadka nie niesie,
  a ciało pisane na nią zmierzono i nie kupuje ono ani jednego zdania,
  więc zostaje z tej pozycji nazwa, którą słownik zna, i jej znamienia nie ma.

## Implementation

`olski/morph.py` wraps Morfeusz 2, which supplies segmentation
and every reading of every form, choosing none of them.

`olski/grammar.py` is the formalism:
productions, symbols, and feature unification.
A grammar is Python data rather than a notation of its own.
It also answers whether any terminal takes a reading at all,
which is what lets a rejected sentence say what it stood on:
[więzy wyprowadzone z gramatyki](parsowanie.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej)
owns why that question belongs here rather than in a layer beside the grammar.

That formalism is tier 0 of
[the cost ladder](design-notes.md#the-cost-ladder):
every feature value is a finite set of tagset atoms,
unification is intersection,
and a variable is scoped to the production that uses it,
so the grammar underneath the features is context-free,
for the reason [design-notes.md](design-notes.md#why-a-subset-really) gives.
Reading a segmentation graph rather than a string does not reach past it,
the context-free languages being closed under intersection with a regular one.
Tier 0 is where the implementation stands and not what the track is committed to;
[design-notes.md](design-notes.md#formalizm-jest-środkiem-a-nie-celem)
owns that distinction.

`olski/parse/` builds the forest and summarizes it.
It is an Earley chart over the segmentation graph,
so one packed position stands for a constituent shape
however many derivations sit under it,
and a sentence with six undecided attachments
is six positions rather than sixty-four trees.
That is what the verdict wanted sooner than the grammar did:
the reader is shown the preposition and the heads it reaches,
one line per undecided choice.
[Werdykt jest zapytaniem o las](parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)
owns that argument,
and [tożsamość czytania](parsowanie.md#co-się-pakuje-rozstrzyga-tożsamość-czytania)
owns what may share a position and how the counting joins two of them.

`olski/subset/` is olski itself:
the grammar, what it reads as one word,
the readings it declines to consider, and the verdicts.

```sh
python3 -m olski.check -c "Zapisz plik konfiguracyjny." --readings
```
