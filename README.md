# j-olski

*Język olski* to *język polski*, któremu spiłowano *p*,
a razem z nim te części polszczyzny,
przez które jest ona trudna dla sztywnych, zimnych maszyn.

Zdanie jest w olskim poprawne dopiero wtedy, gdy ma dokładnie jedno czytanie.
**Parser tego podzbioru** mówi, że zdanie czyta się dwojako,
a za autora nie wybiera.

Wzorem jest kompilator, a model językowy nie jest tu wzorem.
Parser jest tani i deterministyczny,
a każdy werdykt przychodzi z czytaniem, które go wydało.
To samo wejście daje tę samą odpowiedź.

Obok parsera stał tu linter stylu dla polskiej dokumentacji technicznej.
Linter jest wycofany, a analiza, która schodziła do znaku, zeszła razem z nim.
Przyczynę trzyma [docs/linter.md](docs/linter.md#what-closed-the-track),
a cenę pakietu liczy [docs/firing-rates.md](docs/firing-rates.md).

## Dlaczego biała lista, skoro czarna była tańsza

Język kontrolowany jest białą listą,
a biała lista mówi, które konstrukcje istnieją.
Linter jest czarną listą,
a czarna lista mówi, które wzorce zostaną zgłoszone.
Autor pisze poza tym, co chce.

Zbiór tekstów, które przechodzą przez wszystkie reguły,
jest w obu przypadkach podzbiorem polszczyzny,
a wyznaczenie tego zbioru przez wykluczanie jest nieporównanie tańsze.
Po to ta czarna lista tu stała.
[Wywód, który za nią stał](docs/linter.md#this-is-the-same-subset-approached-from-behind),
stoi dalej.

Czarna lista kupowała jednak co innego, niż obiecywała.
Reguła, która sięga do znaku w zdaniu,
nie mówi o polszczyźnie tego zdania nic,
a na głębszym poziomie analizy przestaje być tania:
[pomiar](docs/linter.md#what-closed-the-track) nad dwoma korpusami mówi,
że taki poziom odpowiada na inne pytanie, niż zadaje reguła.
Cenę białej listy płaci autor, bo nie czuje granicy.
Odrabia ją parser, bo zamiast samej odmowy pokazuje oba czytania.
Granicę pokazuje sama odpowiedź.

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
Projekt jest dla przyjemności.

## Co działa

Działają dwie rzeczy.

**Gramatyka podzbioru polszczyzny** stoi nad Morfeuszem 2.
Zdanie jest w niej olskie dopiero wtedy, gdy ma dokładnie jedno czytanie.
Nie chodzi o samo jedno wyprowadzenie:
zdanie o koszcie szynki ma kilka czytań,
a dwa czytania mówią rzecz przeciwną,
więc olski nie bierze tego zdania.

```sh
python3 -m olski.check --readings -c "Zapisz plik konfiguracyjny.
Koszt samej szynki przewyższa koszt szynki z dodatkami.
Nowa program zapisuje ustawienia."
```

```text
<text>: valid     Zapisz plik konfiguracyjny.
                  one reading
                  - Object: plik konfiguracyjny, Verb: Zapisz
<text>: ambiguous Koszt samej szynki przewyższa koszt szynki z dodatkami.
                  6 readings, differing in Object, Subject; „z dodatkami” → „przewyższa”, „koszt”, „szynki”
                  - Subject: Koszt samej szynki, Object: koszt szynki z dodatkami, Verb: przewyższa, Modifier: z dodatkami → szynki
                  - Subject: Koszt samej szynki, Object: koszt szynki z dodatkami, Verb: przewyższa, Modifier: z dodatkami → koszt
                  - Subject: Koszt samej szynki, Object: koszt szynki, Verb: przewyższa, Modifier: z dodatkami → przewyższa
                  - Subject: koszt szynki z dodatkami, Object: Koszt samej szynki, Verb: przewyższa, Modifier: z dodatkami → szynki
                  - Subject: koszt szynki z dodatkami, Object: Koszt samej szynki, Verb: przewyższa, Modifier: z dodatkami → koszt
                  - Subject: koszt szynki, Object: Koszt samej szynki, Verb: przewyższa, Modifier: z dodatkami → przewyższa
<text>: rejected  Nowa program zapisuje ustawienia.
                  no reading: nothing in olski derives this
1 of 3 sentences are olski
```

Czytania szynki dzieli szyk oraz gospodarz frazy `z dodatkami`.
Pierwsze i czwarte dzieli sam szyk,
a podmiot jednego jest dopełnieniem drugiego.
Wiersz werdyktu nazywa przy tym sam wybór.
Skutków tego wyboru wiersz nie wylicza:
każdy wybór, którego zdanie nie rozstrzyga, dostaje jeden wiersz,
a iloczyn tych wyborów daje liczbę czytań.
Przyłączenie jest tu wyborem.
Nad innym zdaniem takim wyborem jest konstytuent,
którego streszczenie nie pokazuje.

Zgodność form jest tu parsowaniem.
`Nowa program` nie ma wyprowadzenia.
Nie ma tu reguły, która strzeliła.
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
Drzewo mówi, że jedna rzecz jest określeniem drugiej albo celem.
Przypadków drzewo nie nazywa.
Zgodność liczy skład po drodze.
Gramatyki skład nie czyta.
Pokrycia gramatyki skład nie dziedziczy.

Nad zdaniem stoi opowieść, bo tekst wie to, czego zdanie samo o sobie nie wie:
kiedy to było i o kim mowa była przed chwilą.
Czas przeszły daje pierwsze,
a drugie daje podmiot opuszczony tam, gdzie opuszcza go polszczyzna.

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
Czeladnik zapłakał w wąskiej piwnicy. Próbował wrócić na ulicę. Sukno znalazło bochenki i nie stało w nocy. Czeladnik zasnął. Ponieważ córka zeszła od młodej wdowy, nie zamknął zegara. Sukno podniosło beczki i dużą skrzynię.
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

Resztą repozytorium są notatki projektowe, przegląd pola,
plan i otwarte pytania.

- [docs/roles.md](docs/roles.md) nazywa role,
  w których ktoś to repozytorium czyta.
  Wszystkie te role obsadza jedna osoba.
- [docs/architecture.md](docs/architecture.md) wylicza warstwy,
  przez które zdanie przechodzi w obu kierunkach.
  Oba tory mają jedną warstwę wspólną.
- [docs/subset.md](docs/subset.md) mówi, co gramatyka wpuszcza
  i ile kosztuje przyłączanie wyrażeń przyimkowych.
- [docs/sklad.md](docs/sklad.md) mówi, co tekst wie ponad zdaniem
  i czego brakuje w leksykonie.
- [docs/pisanie-po-olsku.md](docs/pisanie-po-olsku.md)
  zbiera feedback z sesji, która pisała pod tę gramatykę.
- [docs/corpus.md](docs/corpus.md) mierzy gramatykę na Składnicy.
  Mówi, co daje pierwszy pomiar i czego nie dowodzi liczba pokrycia.
  Składnica jest tam bankiem drzew.
- [docs/ustawy.md](docs/ustawy.md) mówi,
  czego żądają od zdania w ustawie „Zasady techniki prawodawczej”.
- [docs/linter.md](docs/linter.md) mówi, po co był linter
  i co zamknęło ten tor.
- [docs/fiction.md](docs/fiction.md) mówi,
  co psuje się w prozie literackiej z modelu i co z niej da się lintować.
- [docs/generated-polish.md](docs/generated-polish.md)
  mierzy prawdziwy zbiór polszczyzny z modelu.
- [docs/extraction.md](docs/extraction.md)
  prowadzi korpus w Markdownie do gramatyki
  i mówi, co ten krok po drodze zmyśla.
- [docs/corpora.md](docs/corpora.md) przegląda polszczyznę pisaną przez ludzi
  i mówi, co każdy kandydat na korpus niesie w swoim rejestrze.
- [docs/audit-corpus.md](docs/audit-corpus.md) nazywa repozytoria,
  z których zrobiony jest korpus audytowy.
  Podaje commity, na których stoją liczby.
- [docs/firing-rates.md](docs/firing-rates.md) mówi,
  co pakiet typograficzny robił nad polszczyzną, którą ktoś napisał.
  Nazywa cenę, za którą ten tor został wycofany.
- [docs/roadmap.md](docs/roadmap.md) wylicza cele oraz etapy dwóch torów.
  Jeden tor ma kierunek, a drugi ma kryterium wyjścia.
- [docs/prose-linters.md](docs/prose-linters.md) nazywa silniki,
  które angielski i japoński już mają.
  Jeden z nich zmierzył własną częstość fałszywych trafień.
- [docs/similar-work.md](docs/similar-work.md) mówi,
  które obietnice stu kontrolowanych języków naturalnych ktoś naprawdę zmierzył.
- [docs/design-notes.md](docs/design-notes.md) mówi,
  co czyni polszczyznę trudną do parsowania.
  Pokazuje drabinę kosztów i urwisko nieciągłości.
- [docs/disambiguation.md](docs/disambiguation.md) nazywa to,
  co warstwa za parserem musi rozstrzygnąć.
- [docs/open-questions.md](docs/open-questions.md) wylicza rozwidlenia,
  na których nie zapadła decyzja.
- [docs/prior-art.md](docs/prior-art.md)
  wylicza Morfeusza, Świgrę i resztę pola.
- [docs/glr-in-practice.md](docs/glr-in-practice.md) jest raportem z terenu
  o systemie, który puszcza swój parser nad prawdziwą polszczyzną.
- [docs/swigra.md](docs/swigra.md) nazywa teren,
  który zajmuje najbliższy parser polszczyzny.
  Warto wziąć z tych źródeł kilka mechanizmów.

## Konwencje

Prozę w tym repozytorium łamiemy według
[Semantic Line Breaks](https://sembr.org),
a nową piszemy po polsku,
więc czytelnik trafia na oba języki naraz.
Ten plik omija przy tym konstrukcje, których olski nie wyprowadza,
a cenę tej konwencji trzyma
[docs/roadmap.md](docs/roadmap.md#readme-jest-przyrządem-pomiarowym).
Konwencje prozy, kodu, testów i commitów trzyma [CLAUDE.md](CLAUDE.md),
a otwartą robotę trzyma [TODO.md](TODO.md).
