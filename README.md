# j-olski

*Język olski* to *język polski*, któremu spiłowano *p*,
a razem z nim te części polszczyzny,
przez które jest ona trudna dla sztywnych zimnych maszyn.

Celem jest **parser tego podzbioru**.
Zdanie jest w nim poprawne dopiero wtedy, gdy ma dokładnie jedno czytanie,
więc taki parser mówi autorowi, że jego zdanie czyta się dwojako, i jak,
zamiast wybierać za niego czytanie prawdopodobniejsze.

Obok stoi **linter stylu dla polskiej dokumentacji technicznej**,
przydatny między innymi do sprawdzania tekstów,
które napisały modele językowe.
Nie do błędów składniowych, bo tych modele robią rzadko,
tylko do wzorców, w które wpadają z przyzwyczajenia.
Linter pomaga pisać dobry kod.
To ma pomagać pisać dobrą polszczyznę.

Jedno i drugie tanio, deterministycznie i z wyjaśnieniem:
jak w kompilatorze, a nie jak w modelu językowym.
Każdy werdykt przychodzi z tym, co go wydało, regułą albo czytaniem,
a to samo wejście dwa razy daje tę samą odpowiedź.

## Dlaczego mimo wszystko jest to podzbiór polszczyzny

Język kontrolowany to biała lista:
istnieją tylko te konstrukcje, które na niej stoją.
Linter to czarna lista:
pisz, co chcesz, ale te wzorce zostaną zgłoszone.

Zbiór tekstów przechodzących przez wszystkie reguły
jest podzbiorem polszczyzny w jednym i w drugim przypadku.
Wyznaczenie go przez wykluczanie jest nieporównanie tańsze
i znika przy nim kłopot, który biała lista ma na stałe:
autor nie czuje, którędy biegnie jej granica.
Cały wywód prowadzi
[docs/linter.md](docs/linter.md#this-is-the-same-subset-approached-from-behind).

## Kierunek

**Teraz.** Gramatyka zaprojektowanego podzbioru polszczyzny,
a przy niej kalambur: *skład* obok *składni*.
Cel ma jeden i jest nim ten plik:
gramatyka rośnie tak długo, aż rozbierze go zdanie po zdaniu,
a skład tak długo, aż każde jego zdanie wypuści z drzewa.
Celem nie jest sam formalizm:
gramatyka bezkontekstowa jest tym, na czym olski stoi,
a nie tym, do czego zmierza,
więc o sięgnięciu po mocniejszy mechanizm rozstrzyga cena.
Zobacz [docs/design-notes.md](docs/design-notes.md)
oraz [docs/roadmap.md](docs/roadmap.md#celem-toru-jest-to-readme).

**Opcjonalnie, obok.** Silnik reguł, skalibrowany zestaw reguł
i ta polszczyzna pisana przez ludzi, która rozstrzyga,
którym regułom można ufać, a które są tylko opiniami.
Gramatyka dochodzi do tego toru jako najgłębszy poziom analizy,
do którego schodzą tylko te reguły, które sobie na to zasłużą.
Zobacz [docs/linter.md](docs/linter.md).

Nie ma aplikacji, która by to wszystko napędzała.
Projekt jest dla przyjemności.

## Co działa

Działają trzy rzeczy.

**Gramatyka podzbioru polszczyzny**, nad Morfeuszem 2,
w której zdanie jest olski wtedy, gdy ma dokładnie jedno czytanie.
Nie chodzi o samo jedno wyprowadzenie:
`Koszt samej szynki przewyższa koszt szynki z dodatkami`
rozkłada się na kilka czytań, a dwa z nich mówią rzecz przeciwną,
więc olski to zdanie odrzuca.

```sh
python3 -m olski.check -c "Zapisz plik konfiguracyjny." --readings
```

```text
<text>: valid     Zapisz plik konfiguracyjny.
                  one reading
                  - Object: plik konfiguracyjny, Verb: Zapisz
<text>: ambiguous Koszt samej szynki przewyższa koszt szynki z dodatkami.
                  6 readings, differing in Object, Subject
<text>: rejected  Nowa program zapisuje ustawienia.
                  no reading: nothing in olski derives this
```

Zgodność form jest tu parsowaniem, a nie sprawdzeniem po nim:
`Nowa program` nie ma wyprowadzenia,
więc nie jest to reguła, która strzeliła, tylko zdanie, którego nie ma.
Co gramatyka obejmuje, czego nie obejmuje
i dlaczego przyłączenie wyrażenia przyimkowego zostaje przy czytelniku,
mówi [docs/subset.md](docs/subset.md).

**Silnik reguł i pakiet typograficzny**, nad zwykłym tekstem polskim.

```sh
python3 -m olski tekst.txt
python3 -m olski tekst.txt --explain          # z uzasadnieniem każdej reguły
python3 -m olski korpus/ --format report      # co każda reguła zrobiła nad korpusem
python3 -m olski --list-rules
```

```text
tekst.txt:3:42: warning: [quote-straight] Straight quotation mark; Polish takes „ opening and ” closing.
tekst.txt:5:15: warning: [missing-space-after-punctuation] No space after ,.
tekst.txt: abstained: [em-dash-density] this document is under the 150-word floor a rate over it needs
```

Reguły tego rodzaju zarabiają na siebie tylko tam,
gdzie rozstrzyga znak, a nie struktura:
cudzysłów, odstęp, zabłąkana pauza.
Reguła, która musi wiedzieć, czym słowo *jest*, należy do gramatyki,
i dlatego pakietu wzorców nad samą polszczyzną nie ma.
Siedem reguł, wszystkie z poziomu A, wszystkie oznaczone jako `uncalibrated`,
bo żadnej nie zmierzono na polszczyźnie pisanej przez ludzi,
a próg bez takiego pomiaru jest opinią z przecinkiem.
Tryb raportu jest tą połową pomiaru, którą jeden przebieg umie wyprodukować:
jak często każda reguła strzeliła nad całym korpusem i nad jaką jego częścią.
[docs/firing-rates.md](docs/firing-rates.md) jest tym, co ten tryb wypisał
nad dwoma zbiorami polszczyzny, które ktoś napisał.
Wejściem jest zwykły tekst polski.
Plik w formacie znacznikowym dostaje te reguły, które rozstrzyga sam znak,
oraz abstencje od tych, które mierzyłyby jego aparat.
Zobacz [docs/rules.md](docs/rules.md).

To, co zamienia korpus w Markdownie w prozę,
którą reszta reguł umie zmierzyć,
stoi obok lintera, a nie w nim:

```sh
python3 -m harness.markdown korpus/ --into proza/
```

Właścicielem tego, co ten krok zmyśla,
jest [docs/extraction.md](docs/extraction.md).

Tą samą drogą dochodzi ustawa, tylko że nie akapitami,
bo ustawa jest drzewem jednostek redakcyjnych, a nie ciągiem zdań:

```sh
python3 -m harness.ustawy ustawy/ --into proza/ustawy
```

Ile z tego rejestru wychodzi i czego żądają od zdania w ustawie
„Zasady techniki prawodawczej”, mówi [docs/ustawy.md](docs/ustawy.md).

**Skład**, czyli ten sam Morfeusz czytany w drugą stronę.
Wchodzi drzewo tego, co ma zostać powiedziane, a wychodzi polskie zdanie,
a z kilku drzew postawionych obok siebie wychodzi tekst.

```python
from skład import kompiluj
from skład.słownik import A, R, V, jest

kompiluj(jest(R.parser / R.podzbiór, R.cel))     # Parser podzbioru jest celem.
kompiluj(V.sprawdzać(R.linter, ~(A.polski * R.tekst)))  # Linter sprawdza polskie teksty.
```

Kategorie tego drzewa są kategoriami dziedziny, a nie polszczyzny:
mówią, że jedna rzecz jest określeniem drugiej, a nie że stoi tam dopełniacz,
i że coś jest celem, a nie że stoi tam biernik.
Zgodność jest liczona po drodze, a nie sprawdzana po niej,
więc ten kierunek nie potrzebuje gramatyki i nie dziedziczy jej pokrycia.

Nad zdaniem stoi opowieść, bo tekst wie to, czego zdanie samo o sobie nie wie:
kiedy to było i o kim mowa była przed chwilą.
Pierwsze daje czas przeszły,
a drugie podmiot opuszczony tam, gdzie opuszcza go polszczyzna.

```python
from skład import Akapit, Opowieść, Postać
from skład.słownik import A, Gdzie, R, V, nowe, razem, temat

bazyliszek = Postać(R.bazyliszek)
Opowieść(Akapit(
    V.mieszkać(nowe(bazyliszek), temat(Gdzie.w(R.piwnica / (A.stary * R.kamienica)))),
    V.mieć(bazyliszek, razem([A.koguci * R.dziób, A.wężowy * R.ogon])),
)).kompiluj()
# W piwnicy starej kamienicy mieszkał bazyliszek. Miał koguci dziób i wężowy ogon.
```

Szyk jest tu wnioskiem, a nie zapisem:
drzewo mówi, co w zdaniu jest tematem, a co nowe, i dopiero z tego wychodzi kolejność.
Reszta zapisu jest zwykłym Pythonem i to jest w nim zamierzone:
zmienna nazywa postać, funkcja jest wzorcem zdania albo akapitu,
a lista wchodzi do zdania jako koordynacja.
Całą legendę o bazyliszku warszawskim trzyma `opowieści/bazyliszek.py`.

Rzecz nazywa lematem tam, gdzie stoi leksem,
a szyku wewnątrz grupy imiennej nie niesie, i to są dwie dziury w nim samym.
Czego brakuje pod nim, w leksykonie i w formach, i w jakiej kolejności to dochodzi,
mówi [docs/roadmap.md](docs/roadmap.md#tor-składu-drzewo-wchodzi-polskie-zdanie-wychodzi).
Zobacz [docs/design-notes.md](docs/design-notes.md).

Reszta repozytorium to notatki projektowe, przegląd pola,
plan i otwarte pytania.

- [docs/roles.md](docs/roles.md):
  role, w jakich ktoś to repozytorium czyta,
  gdzie każda z nich wchodzi i co jej drogę psuje,
  i dlaczego wszystkie obsadza jedna osoba
- [docs/subset.md](docs/subset.md):
  co gramatyka wpuszcza, dlaczego poprawność znaczy jedno czytanie
  i ile kosztuje przyłączanie wyrażeń przyimkowych
- [docs/rules.md](docs/rules.md):
  jak pisze się regułę, jakie są rodzaje checków
  i czym różni się abstencja od braku trafień
- [docs/corpus.md](docs/corpus.md):
  jak mierzy się gramatykę na banku drzew Składnica,
  co mówi pierwszy pomiar
  i czego nie dowodzi liczba pokrycia wzięta na wyjściu jednej gramatyki
- [docs/ustawy.md](docs/ustawy.md):
  czego „Zasady techniki prawodawczej” żądają od zdania w ustawie,
  ile z tego rejestru gramatyka wyprowadza
  i dlaczego regularne jest w nim drzewo jednostek redakcyjnych, a nie zdanie
- [docs/linter.md](docs/linter.md):
  po co jest linter, ile analizy potrzebuje która reguła,
  dlaczego kalibracja rozstrzyga wszystko
  i co w prozie literackiej da się, a czego nie da się lintować
- [docs/rule-inventory.md](docs/rule-inventory.md):
  kolejka reguł do napisania, pogrupowana poziomem analizy,
  którego każda pozycja potrzebuje,
  i to, które pozycje mają za sobą źródło, a które są hipotezami
- [docs/fiction.md](docs/fiction.md):
  co psuje się w prozie literackiej z modelu,
  dlaczego odpowiada za to post-training,
  dlaczego modele w roli sędziów stawiają ją wyżej od New Yorkera
  i co z niej da się lintować
- [docs/generated-polish.md](docs/generated-polish.md):
  co mierzy prawdziwy zbiór wygenerowanej polszczyzny,
  które wzorce wnosi do inwentarza
  i dlaczego korpus redagowany pod detektory jest podłogą, a nie próbką
- [docs/extraction.md](docs/extraction.md):
  jak korpus w Markdownie dociera do reguł jako proza
  i co ten krok po drodze zmyśla
- [docs/prose-in-code.md](docs/prose-in-code.md):
  jak do tych samych reguł dochodzi proza, którą repozytorium pisze
  w docstringach i komentarzach, i czym ten krok różni się od tamtego
- [docs/corpora.md](docs/corpora.md):
  jaką polszczyznę pisaną przez ludzi da się w ogóle zdobyć,
  co każdy kandydat na korpus mówi o swoim rejestrze, pochodzeniu i licencji,
  i za jakim doborem przemawia ten przegląd
- [docs/audit-corpus.md](docs/audit-corpus.md):
  z jakich repozytoriów zrobiony jest korpus audytowy,
  co trzeba pokazać, żeby do niego wejść,
  i jak ściągnąć je na tych commitach, na których wzięto liczby
- [docs/firing-rates.md](docs/firing-rates.md):
  co pakiet typograficzny robi nad polszczyzną, którą ktoś napisał,
  czym okazują się jego trafienia, kiedy się je przeczyta,
  i dlaczego zerowa częstość może mówić o korpusie zamiast o regule
- [docs/roadmap.md](docs/roadmap.md):
  etapy trzech torów, każdy ze swoim kryterium wyjścia,
  i to, dlaczego numeracja jednego nie sięga pozostałych
- [docs/prose-linters.md](docs/prose-linters.md):
  silniki, które angielski i japoński już mają,
  ten jeden, który zmierzył własną częstość fałszywych trafień,
  i to, czego trzeba, żeby po polsku je pobić
- [docs/similar-work.md](docs/similar-work.md):
  sto kontrolowanych języków naturalnych,
  jak pole je klasyfikuje
  i które z ich obietnic ktoś naprawdę zmierzył
- [docs/design-notes.md](docs/design-notes.md):
  tor gramatyczny,
  czyli co czyni polszczyznę trudną do parsowania,
  drabina kosztów, urwisko nieciągłości
  i to, że sam formalizm jest na tym torze środkiem
- [docs/open-questions.md](docs/open-questions.md):
  rozwidlenia, na których nie zapadła decyzja
- [docs/prior-art.md](docs/prior-art.md):
  Morfeusz, Morfologik, Świgra, Grammatical Framework i reszta
- [docs/glr-in-practice.md](docs/glr-in-practice.md):
  raport z terenu o małym systemie,
  który puszcza parser GLR nad prawdziwą polszczyzną,
  co robi z lasem rozbiorów
  i co wychodzi jego gramatyce na tysiącu z górą wierszy
- [docs/swigra.md](docs/swigra.md):
  jaki teren zajmuje najbliższy istniejący parser polszczyzny,
  co zostawia otwarte dla toru gramatycznego
  i które mechanizmy warto wziąć z jego źródeł

## Konwencje

Proza w tym repozytorium łamie wiersze według
[Semantic Line Breaks](https://sembr.org),
a nowa powstaje po polsku, w języku, który to narzędzie lintuje,
więc czytelnik trafia na oba języki naraz.
Konwencje prozy, kodu, testów i commitów trzyma [CLAUDE.md](CLAUDE.md),
a otwartą robotę wewnątrz repozytorium [TODO.md](TODO.md).
