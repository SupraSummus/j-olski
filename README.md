# j-olski

*Język olski* to *język polski*, któremu spiłowano *p*,
a razem z nim te części polszczyzny,
przez które jest ona trudna dla sztywnych, zimnych maszyn.

Repozytorium jest projektem wokół tego języka.
Narzędzia tego projektu biorą podzbiór, a nie całą polszczyznę.
Żaden cel nie żąda pełnego pokrycia.
Cele wylicza [docs/roadmap.md](docs/roadmap.md#cele).

**Parser tego podzbioru** zwraca wszystkie odczytania zdania.
Wieloznaczność widać po ich liczbie, a wybór zostaje przy autorze.

Wzorem jest kompilator, a nie model językowy.
Rozbiór jest deterministyczny, więc to samo wejście daje tę samą odpowiedź.
Każdy werdykt przychodzi z odczytaniem, z którego wyszedł.

## Kierunek

Pierwszym torem jest gramatyka podzbioru polszczyzny.
Drugim torem jest skład, którego nazwa jest kalamburem od *składni*.
Oba tory mierzy ten plik.
Dla składu ten plik jest zarazem celem:
skład rośnie tak długo, aż wypuści z drzewa każde zdanie tego pliku.
Gramatyka celu końcowego nie ma,
a cenę produkcji liczy autor przed dopisaniem.
Kierunkiem nie jest sam formalizm:
gramatyka bezkontekstowa jest podłożem olskiego, a nie jest celem,
więc o mocniejszym mechanizmie rozstrzyga cena.
Zobacz [docs/design-notes.md](docs/design-notes.md)
oraz [docs/roadmap.md](docs/roadmap.md#tor-gramatyczny-nie-ma-końca).

Nie ma aplikacji, która napędzałaby to wszystko.

## Co działa

**Gramatyka podzbioru polszczyzny** stoi nad Morfeuszem 2.
Zdanie jest olskie, gdy gramatyka je wyprowadza.
Narzędzie sprawdza zdania polskiego tekstu.
Wieloznaczność jest jego znaleziskiem.
Zdanie o programie ma trzy odczytania,
a dwa odczytania mówią rzecz przeciwną,
więc narzędzie zgłasza to autorowi.

```sh
python3 -m olski.check --readings -c "Zapisz plik konfiguracyjny.
Program otwierający się psuje.
Nowa program zapisuje ustawienia."
```

```text
<text>: valid     Zapisz plik konfiguracyjny.
                  jedno odczytanie
                  - dopełnienie: plik konfiguracyjny, orzeczenie: Zapisz
<text>: ambiguous Program otwierający się psuje.
                  3 odczytania, różne w rolach: dopełnienie, orzeczenie, podmiot
                  - dopełnienie: Program otwierający się, orzeczenie: psuje
                  - podmiot: Program otwierający się, orzeczenie: psuje
                  - podmiot: Program otwierający, orzeczenie: się psuje
<text>: rejected  Nowa program zapisuje ustawienia.
                  brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania
zdań: 3; wieloznaczne: 1; bez odczytania: 1
```

Pierwsze czytanie i drugie dzieli sama rola:
program jest w pierwszym psuty, a w drugim psuje ustawienia.
Trzecie dzieli od nich miejsce cząstki zwrotnej.
Cząstka należy w nim do formy osobowej, a w dwóch pierwszych do imiesłowu.
Obie te formy są w polszczyźnie zwrotne.
Oba miejsca cząstki trzyma
[docs/konstrukcje-gramatyczne/orzeczenie.md](docs/konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika).
Wiersz werdyktu nazywa przy tym role, w których czytania się różnią.
Samego miejsca cząstki wiersz ten nie nazywa i widać je dopiero w czytaniach.

Wybór zostaje przy autorze, a zdania niżej mówią te czytania osobno.

```sh
python3 -m olski.check --readings -c "Program otwierający się jest psuty.
Program otwierający się psuje ustawienia.
Program otwierający psuje się."
```

```text
<text>: valid     Program otwierający się jest psuty.
                  jedno odczytanie
                  - podmiot: Program otwierający się, orzecznik: psuty, orzeczenie: jest
<text>: valid     Program otwierający się psuje ustawienia.
                  jedno odczytanie
                  - podmiot: Program otwierający się, dopełnienie: ustawienia, orzeczenie: psuje
<text>: valid     Program otwierający psuje się.
                  jedno odczytanie
                  - podmiot: Program otwierający, orzeczenie: psuje się
zdań: 3; wieloznaczne: 0; bez odczytania: 0
```

Zgodność form jest tu parsowaniem.
`Nowa program` nie ma wyprowadzenia.
Nie ma tu reguły, która strzeliła.
Werdykt mówi, dokąd analiza doszła, a nie gdzie stoi usterka.
Zdanie bez wyprowadzenia nie jest znaleziskiem.
Olski go nie czyta i o jego polszczyźnie milczy.
Całą tę różnicę trzyma
[docs/subset.md](docs/subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka).

W długim zdaniu analiza staje w kilku miejscach.
Werdykt nazywa pierwsze zatrzymanie.
Osobna flaga nazywa każde zatrzymanie.

```sh
python3 -m olski.check --zatrzymania -c "Cena rośnie, i linter sprawdza tekst, i parser czyta tekst."
```

```text
<text>: rejected  Cena rośnie, i linter sprawdza tekst, i parser czyta tekst.
                  brak odczytania: analiza staje na „i”
                  analiza staje też na „i”
zdań: 1; wieloznaczne: 0; bez odczytania: 1
```

Cięcie nie jest granicą konstrukcji.
Po co ta flaga jest, mówi
[docs/pisanie-po-olsku.md](docs/pisanie-po-olsku.md#odrzucenie-mówi-na-czym-stanęło-i-mówi-to-raz).

Zasięg gramatyki i cenę przyłączenia wyrażenia przyimkowego
trzyma [docs/subset.md](docs/subset.md).

Ekstrakcja zamienia korpus w Markdownie w prozę.
Jest ona krokiem przed gramatyką, a nie jest częścią gramatyki.

```sh
python3 -m harness.markdown korpus/ --into proza/
python3 -m olski.check proza/*.txt
```

Co ekstrakcja po drodze zmyśla,
mówi [docs/extraction.md](docs/extraction.md).

Ustawa przechodzi przez ten sam krok.
Ustawa jest drzewem jednostek redakcyjnych, a nie jest ciągiem zdań.

```sh
python3 -m harness.ustawy ustawy/ --into proza/ustawy
```

Ile z tego rejestru wychodzi i czego żądają od zdania w ustawie
„Zasady techniki prawodawczej”, mówi [docs/ustawy.md](docs/ustawy.md).

**Skład** czyta tego samego Morfeusza w drugą stronę.
Wchodzi drzewo tego, co ma zostać powiedziane,
a wychodzi polskie zdanie.
Z kilku drzew wychodzi tekst.

```python
from olski.skład import kompiluj
from olski.skład.słownik import A, R, V, jest

kompiluj(jest(R.parser / R.podzbiór, R.cel))     # Parser podzbioru jest celem.
kompiluj(V.sprawdzać(R.parser, ~(A.polski * R.tekst)))  # Parser sprawdza polskie teksty.
```

Kategorie tego drzewa są kategoriami dziedziny.
Drzewo nazywa jedną rzecz określeniem drugiej albo jej celem.
Przypadki dobiera skład, a zgodność form liczy po drodze.
Skład pracuje bez gramatyki podzbioru.
Pokrycie tego toru jest osobne.

Nad zdaniem stoi opowieść, bo tekst wie to, czego zdanie samo o sobie nie wie:
czas zdarzenia i osobę, o której mowa była przed chwilą.
Czas przeszły daje pierwszy,
a drugą daje podmiot opuszczony tam, gdzie opuszcza go polszczyzna.

```python
from olski.skład import Akapit, Opowieść, Postać
from olski.skład.słownik import A, Gdzie, R, V, razem

bazyliszek = Postać(R.bazyliszek)
Opowieść(Akapit(
    V.mieszkać(bazyliszek.remat, Gdzie.w(R.piwnica / (A.stary * R.kamienica)).temat),
    V.mieć(bazyliszek, razem([A.koguci * R.dziób, A.wężowy * R.ogon])),
)).kompiluj()
# W piwnicy starej kamienicy mieszkał bazyliszek. Miał koguci dziób i wężowy ogon.
```

Szyk jest tu wnioskiem.
Drzewo mówi, co w zdaniu jest tematem, a co jest nowe.
Kolejność wychodzi dopiero z tego.
Reszta zapisu jest zwykłym Pythonem i to jest w nim zamierzone:
zmienna nazywa postać, funkcja jest wzorcem zdania albo akapitu,
a lista wchodzi do zdania jako koordynacja.
Całą legendę o bazyliszku warszawskim trzyma `opowieści/bazyliszek.py`.

Ten sam kompilator daje tekst do makiety.
Po taki tekst sięga się zwykle do łacińskiej sieczki.

```sh
python3 -m olski.skład.makieta --ziarno 1871 --akapity 1
```

```text
Czeladnik zapłakał w wąskiej piwnicy. Dziewczyna zgubiła glinianą skrzynię, ponieważ czeladnik zszedł. Zdążyła mieszkać przed ciężkim młynem. Córka dała dziewczynie koszyk. Zdążyła wrócić od młodej wdowy. Czeladnik zważył kufry gospodarza i sukno.
```

Losowane jest drzewo.
Zdania dzieli budowa, a same lematy ich nie dzielą.
Zgodność liczy skład po drodze, więc losowanie nie narusza gramatyczności,
a odsiewa ono zdanie, z którego czytelnik nie odzyskałby ról.
Czego takie losowanie zażądało od tego pakietu,
a czego autor drzewa nie musiał nigdy napisać,
mówi [docs/sklad.md](docs/sklad.md#tekst-losowany-żąda-tego-czego-autor-nie-musiał-napisać).

Szyku wewnątrz grupy imiennej skład nie niesie.
Dziura ta stoi w samym składzie.
Braki w leksykonie i braki w formach
wylicza [docs/roadmap.md](docs/roadmap.md#tor-składu-drzewo-wchodzi-polskie-zdanie-wychodzi).
Zobacz [docs/sklad.md](docs/sklad.md).

Witryna pokazuje ten sam werdykt w przeglądarce.
Jest ona bocznym torem i olski nie zależy od niej.
Serwer bierze się ze standardowej biblioteki, więc strona wstaje bez zależności.

```sh
python3 -m witryna
```

Strona woła własne API i jest jego klientem.
Werdykt przychodzi w tych słowach, które drukuje wiersz poleceń.
Zobacz [docs/witryna.md](docs/witryna.md).

Resztą repozytorium są notatki projektowe, przegląd pola,
plan i otwarte pytania.
Co stoi w którym pliku, mówi [docs/README.md](docs/README.md).

## Na czym olski stoi

Zasoby, na których stoi ten parser, napisał Marcin Woliński.
Znaczniki ustala Morfeusz, a leksykon walencyjny ustala Walenty.
Pokrycie mierzy się na Składnicy.
Najbliższym parserem polszczyzny jest jego Świgra.
Czytamy tutaj jej reguły oraz monografię, która opisuje tę gramatykę.
Ta gramatyka spotkała problemy, w które olski wchodzi.
Monografia nazywa przy tym ceny, których kod nie pokazuje.
Zobacz [docs/swigra.md](docs/swigra.md).

## Konwencje

Prozę w tym repozytorium łamiemy według
[Semantic Line Breaks](https://sembr.org),
a nową piszemy po polsku,
więc czytelnik trafia na oba języki naraz.
Ten plik omija przy tym konstrukcje, których olski nie wyprowadza,
a cenę tej konwencji trzyma
[docs/roadmap.md](docs/roadmap.md#readme-jest-przyrządem-pomiarowym).
Konwencje prozy, kodu, testów i commitów trzyma [CLAUDE.md](CLAUDE.md),
a otwartą robotę trzyma [todo/](todo/README.md).
