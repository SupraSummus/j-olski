# j-olski

*Język olski* to *język polski*, któremu spiłowano *p*,
a razem z nim te części polszczyzny,
przez które jest ona trudna dla sztywnych zimnych maszyn.

Celem jest **parser tego podzbioru**.
Zdanie jest w nim poprawne dopiero wtedy, gdy ma dokładnie jedno czytanie,
więc taki parser mówi autorowi, że jego zdanie czyta się dwojako, i jak,
zamiast wybierać za niego czytanie prawdopodobniejsze.

Tanio, deterministycznie i z wyjaśnieniem:
jak w kompilatorze, a nie jak w modelu językowym.
Każdy werdykt przychodzi z czytaniem, które go wydało,
a to samo wejście dwa razy daje tę samą odpowiedź.

Stał tu obok linter stylu dla polskiej dokumentacji technicznej
i został wycofany razem z całą analizą, która schodziła do znaku.
Dlaczego, mówi [docs/linter.md](docs/linter.md#what-closed-the-track);
ile ten pakiet reguł kosztował, zanim wyszedł,
mówi [docs/firing-rates.md](docs/firing-rates.md).

## Dlaczego biała lista, skoro czarna była tańsza

Język kontrolowany to biała lista:
istnieją tylko te konstrukcje, które na niej stoją.
Linter to czarna lista:
pisz, co chcesz, ale te wzorce zostaną zgłoszone.

Zbiór tekstów przechodzących przez wszystkie reguły
jest podzbiorem polszczyzny w jednym i w drugim przypadku,
a wyznaczenie go przez wykluczanie jest nieporównanie tańsze.
Po to ta czarna lista tu stała
i [cały wywód za nią](docs/linter.md#this-is-the-same-subset-approached-from-behind)
dalej stoi.

Czarna lista kupowała jednak co innego, niż obiecywała.
Reguła, która rozstrzyga o zdaniu znakiem w nim postawionym,
nie mówi o polszczyźnie tego zdania nic,
a niżej przestaje być tania:
[pomiar](docs/linter.md#what-closed-the-track) nad dwoma korpusami mówi,
że głębszy poziom analizy odpowiada na inne pytanie niż to, które reguła zadaje.
Cenę białej listy płacimy więc tym, że autor nie czuje, którędy biegnie granica,
a odrabiamy tym, że parser pokazuje oba czytania zamiast samej odmowy:
granicę widać w odpowiedzi, a nie tylko w tym, że odpowiedzi nie ma.

## Kierunek

Tory są dwa: gramatyka zaprojektowanego podzbioru polszczyzny
i skład, nazwany kalamburem od *składni*.
Ten plik mierzy oba tory, a dla jednego z nich jest celem:
skład rośnie tak długo, aż każde jego zdanie wypuści z drzewa,
a gramatyka celu końcowego nie ma i rośnie za cenę liczoną przed dopisaniem.
Kierunkiem nie jest sam formalizm:
gramatyka bezkontekstowa jest tym, na czym olski stoi,
a nie tym, do czego zmierza,
więc o sięgnięciu po mocniejszy mechanizm rozstrzyga cena.
Zobacz [docs/design-notes.md](docs/design-notes.md)
oraz [docs/roadmap.md](docs/roadmap.md#tor-gramatyczny-nie-ma-końca).

Nie ma aplikacji, która by to wszystko napędzała.
Projekt jest dla przyjemności.

## Co działa

Działają dwie rzeczy.

**Gramatyka podzbioru polszczyzny**, nad Morfeuszem 2,
w której zdanie jest olski wtedy, gdy ma dokładnie jedno czytanie.
Nie chodzi o samo jedno wyprowadzenie:
`Koszt samej szynki przewyższa koszt szynki z dodatkami`
rozkłada się na kilka czytań, a dwa z nich mówią rzecz przeciwną,
więc olski to zdanie odrzuca.

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

Czytania szynki różnią się szykiem i tym, do czego dochodzi `z dodatkami`.
Pierwsze i czwarte dzieli sam szyk,
a podmiot jednego jest dopełnieniem drugiego.
Wiersz werdyktu nazywa przy tym sam wybór, a nie wylicza jego skutków:
wierszy jest tyle, ile zdanie zostawia nierozstrzygniętych przyłączeń,
a czytań bywa tyle, ile ich iloczyn.

Zgodność form jest tu parsowaniem, a nie sprawdzeniem po nim:
`Nowa program` nie ma wyprowadzenia,
więc nie jest to reguła, która strzeliła, tylko zdanie, którego nie ma.
Co gramatyka obejmuje, czego nie obejmuje
i dlaczego przyłączenie wyrażenia przyimkowego zostaje przy czytelniku,
mówi [docs/subset.md](docs/subset.md).

Ekstrakcja zamienia korpus w Markdownie w prozę
i jest krokiem przed gramatyką, a nie jej częścią:

```sh
python3 -m harness.markdown korpus/ --into proza/
python3 -m olski.check proza/*.txt
```

Co ekstrakcja po drodze zmyśla,
mówi [docs/extraction.md](docs/extraction.md).

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
kompiluj(V.sprawdzać(R.parser, ~(A.polski * R.tekst)))  # Parser sprawdza polskie teksty.
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
from skład.słownik import A, Gdzie, R, V, razem

bazyliszek = Postać(R.bazyliszek)
Opowieść(Akapit(
    V.mieszkać(bazyliszek.remat, Gdzie.w(R.piwnica / (A.stary * R.kamienica)).temat),
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

Szyku wewnątrz grupy imiennej skład nie niesie, i to jest dziura w nim samym.
Czego brakuje pod nim, w leksykonie i w formach, i w jakiej kolejności to dochodzi,
mówi [docs/roadmap.md](docs/roadmap.md#tor-składu-drzewo-wchodzi-polskie-zdanie-wychodzi).
Zobacz [docs/sklad.md](docs/sklad.md).

Reszta repozytorium to notatki projektowe, przegląd pola,
plan i otwarte pytania.

- [docs/roles.md](docs/roles.md):
  role, w jakich ktoś to repozytorium czyta,
  gdzie każda z nich wchodzi i co jej drogę psuje,
  i dlaczego wszystkie obsadza jedna osoba
- [docs/subset.md](docs/subset.md):
  co gramatyka wpuszcza, dlaczego poprawność znaczy jedno czytanie
  i ile kosztuje przyłączanie wyrażeń przyimkowych
- [docs/sklad.md](docs/sklad.md):
  na jakim poziomie stoją kategorie drzewa, co tekst wie ponad zdaniem
  i czego brakuje pod tym w leksykonie i w formach
- [docs/corpus.md](docs/corpus.md):
  jak mierzy się gramatykę na banku drzew Składnica,
  co mówi pierwszy pomiar
  i czego nie dowodzi liczba pokrycia wzięta na wyjściu jednej gramatyki
- [docs/ustawy.md](docs/ustawy.md):
  czego „Zasady techniki prawodawczej” żądają od zdania w ustawie,
  ile z tego rejestru gramatyka wyprowadza
  i dlaczego regularne jest w nim drzewo jednostek redakcyjnych, a nie zdanie
- [docs/linter.md](docs/linter.md):
  po co był linter, ile analizy potrzebowała która reguła,
  dlaczego kalibracja rozstrzygała wszystko
  i co zamknęło ten tor
- [docs/fiction.md](docs/fiction.md):
  co psuje się w prozie literackiej z modelu,
  dlaczego odpowiada za to post-training,
  dlaczego modele w roli sędziów stawiają ją wyżej od New Yorkera
  i co z niej da się lintować
- [docs/generated-polish.md](docs/generated-polish.md):
  co mierzy prawdziwy zbiór wygenerowanej polszczyzny,
  które wzorce w niej widać
  i dlaczego korpus redagowany pod detektory jest podłogą, a nie próbką
- [docs/extraction.md](docs/extraction.md):
  jak korpus w Markdownie dociera do gramatyki jako proza
  i co ten krok po drodze zmyśla
- [docs/corpora.md](docs/corpora.md):
  jaką polszczyznę pisaną przez ludzi da się w ogóle zdobyć,
  co każdy kandydat na korpus mówi o swoim rejestrze, pochodzeniu i licencji,
  i za jakim doborem przemawia ten przegląd
- [docs/audit-corpus.md](docs/audit-corpus.md):
  z jakich repozytoriów zrobiony jest korpus audytowy,
  co trzeba pokazać, żeby do niego wejść,
  i jak ściągnąć je na tych commitach, na których wzięto liczby
- [docs/firing-rates.md](docs/firing-rates.md):
  co pakiet typograficzny robił nad polszczyzną, którą ktoś napisał,
  czym okazały się jego trafienia, kiedy się je przeczytało,
  i za jaką cenę ten tor został wycofany
- [docs/roadmap.md](docs/roadmap.md):
  etapy dwóch torów, kierunek jednego i kryterium wyjścia drugiego,
  i to, dlaczego numeracja jednego nie sięga drugiego
- [docs/prose-linters.md](docs/prose-linters.md):
  silniki, które angielski i japoński już mają,
  ten jeden, który zmierzył własną częstość fałszywych trafień,
  i to, czego trzeba było, żeby po polsku je pobić
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
a nowa powstaje po polsku, w języku, o którym to repozytorium jest,
więc czytelnik trafia na oba języki naraz.
Konwencje prozy, kodu, testów i commitów trzyma [CLAUDE.md](CLAUDE.md),
a otwartą robotę wewnątrz repozytorium [TODO.md](TODO.md).
