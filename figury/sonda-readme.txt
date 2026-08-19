#  Ten plik powstaje przebiegiem: python3 -m harness.figury sonda-readme
polecenie: python3 -m sonda proza/README.txt
korpus: proza/README.txt
czyta: docs/design-notes.md#podłoże-więzowe-zmierzone-sondą
ruszają:
  README.md: 77c9bdac3583
  harness/markdown.py: 77dba5daa3d8
  olski/subset.py: 24ea4b747a3e
  olski/grammar.py: 9077925971d9
  olski/parse.py: b0553f072e6c
  olski/morph.py: 68c6bc12d9f1
  olski/leksykon.txt: 00193493b3ea
  olski/projekt.py: 029325944002
  olski/projekt.txt: bce2eab3e8dc
  sonda/__main__.py: a120c185c8ce
  sonda/polszczyzna.py: 769ccefe812a
  sonda/wiezy.py: 602748c21b83

proza/README.txt: Język olski to język polski, któremu spiłowano p, a razem z nim te części polszczyzny, przez które jest ona trudna dla sztywnych, zimnych maszyn.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, spiłowano, p, ,, ,, ,
proza/README.txt: Zdanie jest w olskim poprawne dopiero wtedy, gdy ma dokładnie jedno czytanie, więc parser tego podzbioru mówi autorowi, że jego zdanie czyta się dwojako, zamiast wybierać za niego.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: dopiero, wtedy, ,, gdy, dokładnie, ,, więc, autorowi, ,, że, dwojako, ,
proza/README.txt: Tanio, deterministycznie i z wyjaśnieniem: jak w kompilatorze, a nie jak w modelu językowym.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: Tanio, ,, deterministycznie, i, z, wyjaśnieniem, :, jak, w, kompilatorze, ,, a, nie, jak, w, modelu, językowym
proza/README.txt: Każdy werdykt przychodzi z czytaniem, które go wydało, a to samo wejście dwa razy daje tę samą odpowiedź.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, wydało, ,, dwa
proza/README.txt: Obok parsera stał tu linter stylu dla polskiej dokumentacji technicznej i został wycofany razem z całą analizą, która schodziła do znaku.
  olski: ambiguous 18 readings
  sonda: rejected  0 readings, nothing attaches: Obok, parsera, stał, tu, linter, stylu, dla, polskiej, dokumentacji, technicznej, i, został, wycofany, razem, z, całą, analizą, ,, która, schodziła, do, znaku
proza/README.txt: Dlaczego, mówi docs/linter.md; ile ten pakiet reguł kosztował, zanim wyszedł, mówi docs/firing-rates.md.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: Dlaczego, ,, ;, kosztował, ,, zanim, wyszedł, ,
proza/README.txt: Język kontrolowany to biała lista: istnieją tylko te konstrukcje, które na niej stoją.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: :, ,
proza/README.txt: Linter to czarna lista: pisz, co chcesz, ale te wzorce zostaną zgłoszone.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: :, ,, ,
proza/README.txt: Zbiór tekstów przechodzących przez wszystkie reguły jest podzbiorem polszczyzny w jednym i w drugim przypadku, a wyznaczenie go przez wykluczanie jest nieporównanie tańsze.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, wyznaczenie, przez, wykluczanie, nieporównanie
proza/README.txt: Po to ta czarna lista tu stała i cały wywód za nią dalej stoi.
  olski: ambiguous 2 readings
  sonda: rejected  0 readings, nothing attaches: tu, dalej
proza/README.txt: Czarna lista kupowała jednak co innego, niż obiecywała.
  olski: valid     one reading
  sonda: rejected  0 readings, nothing attaches: lista, kupowała, ,, obiecywała
proza/README.txt: Reguła, która rozstrzyga o zdaniu znakiem w nim postawionym, nie mówi o polszczyźnie tego zdania nic, a na głębszym poziomie analizy przestaje być tania: pomiar nad dwoma korpusami mówi, że taki poziom odpowiada na inne pytanie niż to, które reguła zadaje.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, znakiem, ,, ,, :, dwoma, ,, że, ,
proza/README.txt: Cenę białej listy płacimy więc tym, że autor nie czuje, którędy biegnie granica, a odrabiamy tym, że parser pokazuje oba czytania zamiast samej odmowy: granicę widać w odpowiedzi, a nie tylko w tym, że odpowiedzi nie ma.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: więc, ,, że, ,, którędy, ,, ,, że, oba, :, widać, ,, ,, że
proza/README.txt: Tory są dwa: gramatyka zaprojektowanego podzbioru polszczyzny i skład, nazwany kalamburem od składni.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: dwa, :, ,
proza/README.txt: Oba tory mierzymy na tym pliku, który dla jednego z nich jest zarazem celem: skład rośnie tak długo, aż każde jego zdanie wypuści z drzewa, a gramatyka celu końcowego nie ma i rośnie za cenę liczoną przed dopisaniem.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: Oba, ,, zarazem, :, długo, ,, aż, ,, przed, dopisaniem
proza/README.txt: Kierunkiem nie jest sam formalizm: gramatyka bezkontekstowa jest tym, na czym olski stoi, a nie tym, do czego zmierza, więc o sięgnięciu po mocniejszy mechanizm rozstrzyga cena.
  olski: rejected  0 readings
  sonda: rejected  0 readings
proza/README.txt: Zobacz docs/design-notes.md oraz docs/roadmap.md.
  olski: valid     one reading
  sonda: valid     one reading
    - Object: docs/design-notes.md oraz docs/roadmap.md
proza/README.txt: Nie ma aplikacji, która by to wszystko napędzała.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: aplikacji, ,, by, napędzała
proza/README.txt: Projekt jest dla przyjemności.
  olski: valid     one reading
  sonda: valid     one reading
    - Subject: Projekt, Modifier: dla przyjemności
proza/README.txt: Działają dwie rzeczy.
  olski: valid     one reading
  sonda: rejected  0 readings, nothing attaches: dwie
proza/README.txt: Gramatyka podzbioru polszczyzny, nad Morfeuszem 2, w której zdanie jest olski wtedy, gdy ma dokładnie jedno czytanie.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, 2, ,, wtedy, ,, gdy, dokładnie
proza/README.txt: Nie chodzi o samo jedno wyprowadzenie: Koszt samej szynki przewyższa koszt szynki z dodatkami rozkłada się na kilka czytań, a dwa z nich mówią rzecz przeciwną, więc olski to zdanie odrzuca.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: wyprowadzenie, :, ,, dwa, ,, więc
proza/README.txt: Czytania szynki różnią się szykiem i tym, do czego dochodzi z dodatkami.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: szykiem, ,
proza/README.txt: Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego.
  olski: ambiguous 3 readings
  sonda: rejected  0 readings, nothing attaches: ,
proza/README.txt: Wiersz werdyktu nazywa przy tym sam wybór, a nie wylicza jego skutków: wierszy jest tyle, ile zdanie zostawia nierozstrzygniętych wyborów, a czytań bywa tyle, ile ich iloczyn.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, :, ,, ,, ,
proza/README.txt: Wyborem jest tu przyłączenie, a nad innym zdaniem bywa nim konstytuent, który czyta się kilkoma sposobami tam, gdzie streszczenie nie zagląda.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: tu, przyłączenie, ,, ,, kilkoma, ,, gdzie
proza/README.txt: Zgodność form jest tu parsowaniem, a nie sprawdzeniem po nim: Nowa program nie ma wyprowadzenia, więc nie jest to reguła, która strzeliła, tylko zdanie, którego nie ma.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: tu, parsowaniem, ,, sprawdzeniem, :, wyprowadzenia, ,, więc, ,, strzeliła, ,, ,, którego
proza/README.txt: Co gramatyka obejmuje, czego nie obejmuje i dlaczego przyłączenie wyrażenia przyimkowego zostaje przy czytelniku, mówi docs/subset.md.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, dlaczego, przyłączenie, ,
proza/README.txt: Co ekstrakcja po drodze zmyśla, mówi docs/extraction.md.
  olski: ambiguous 8 readings
  sonda: rejected  0 readings, nothing attaches: ,
proza/README.txt: Ile z tego rejestru wychodzi i czego żądają od zdania w ustawie „Zasady techniki prawodawczej”, mówi docs/ustawy.md.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: Ile, „, ”, ,
proza/README.txt: Skład, czyli ten sam Morfeusz czytany w drugą stronę.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: Skład, ,, czyli, ten, sam, Morfeusz, czytany, w, drugą, stronę
proza/README.txt: Wchodzi drzewo tego, co ma zostać powiedziane, a wychodzi polskie zdanie, a z kilku drzew postawionych obok siebie wychodzi tekst.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, ,, ,, kilku, obok, siebie
proza/README.txt: Kategorie tego drzewa są kategoriami dziedziny, a nie polszczyzny: mówią, że jedna rzecz jest określeniem drugiej, a nie że stoi tam dopełniacz, i że coś jest celem, a nie że stoi tam biernik.
  olski: rejected  0 readings
  sonda: rejected  0 readings
proza/README.txt: Zgodność jest liczona po drodze, a nie sprawdzana po niej, więc ten kierunek nie potrzebuje gramatyki i nie dziedziczy jej pokrycia.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, ,, więc
proza/README.txt: Nad zdaniem stoi opowieść, bo tekst wie to, czego zdanie samo o sobie nie wie: kiedy to było i o kim mowa była przed chwilą.
  olski: ambiguous 64+ readings
  sonda: rejected  0 readings, nothing attaches: ,, bo, ,, :, kiedy, było
proza/README.txt: Pierwsze daje czas przeszły, a drugie podmiot opuszczony tam, gdzie opuszcza go polszczyzna.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, ,, gdzie
proza/README.txt: Szyk jest tu wnioskiem, a nie zapisem: drzewo mówi, co w zdaniu jest tematem, a co nowe, i dopiero z tego wychodzi kolejność.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: tu, ,, :, ,, ,, ,, dopiero
proza/README.txt: Reszta zapisu jest zwykłym Pythonem i to jest w nim zamierzone: zmienna nazywa postać, funkcja jest wzorcem zdania albo akapitu, a lista wchodzi do zdania jako koordynacja.
  olski: ambiguous 4 readings
  sonda: rejected  0 readings, nothing attaches: :, ,, ,
proza/README.txt: Całą legendę o bazyliszku warszawskim trzyma opowieści/bazyliszek.py.
  olski: ambiguous 2 readings
  sonda: ambiguous 2 readings
    - Subject: opowieści/bazyliszek.py, Object: Całą legendę o bazyliszku warszawskim, Modifier: o bazyliszku warszawskim
    - Subject: opowieści/bazyliszek.py, Object: Całą legendę, Modifier: o bazyliszku warszawskim
proza/README.txt: Losowane jest drzewo, a nie słowa wstawione w gotowe zdanie, więc zdania różnią się budową, a nie samymi lematami.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, ,, więc, ,
proza/README.txt: Gramatyczności nie ma tu czym naruszyć, bo zgodność jest liczona po drodze, a jedyne, co losowanie odsiewa, to zdanie, z którego czytelnik nie odzyskałby ról.
  olski: rejected  0 readings
  sonda: rejected  0 readings
proza/README.txt: Czego takie losowanie zażądało od tego pakietu, a czego autor drzewa nie musiał nigdy napisać, mówi docs/sklad.md.
  olski: ambiguous 2 readings
  sonda: rejected  0 readings, nothing attaches: Czego, zażądało, ,, musiał, nigdy, napisać, ,
proza/README.txt: Szyku wewnątrz grupy imiennej skład nie niesie, i to jest dziura w nim samym.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: Szyku, ,, samym
proza/README.txt: Czego brakuje pod nim, w leksykonie i w formach, i w jakiej kolejności to dochodzi, mówi docs/roadmap.md.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: Czego, ,, ,, ,
proza/README.txt: Zobacz docs/sklad.md.
  olski: valid     one reading
  sonda: valid     one reading
    - Object: docs/sklad.md
proza/README.txt: Reszta repozytorium to notatki projektowe, przegląd pola, plan i otwarte pytania.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: Reszta, repozytorium, to, notatki, projektowe, ,, przegląd, pola, ,, plan, i, otwarte, pytania
proza/README.txt: Prozę w tym repozytorium łamiemy według Semantic Line Breaks, a nową piszemy po polsku, więc czytelnik trafia na oba języki naraz.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: według, Semantic, Line, Breaks, ,, polsku, ,, więc, oba
proza/README.txt: Konwencje prozy, kodu, testów i commitów trzyma CLAUDE.md, a otwartą robotę wewnątrz repozytorium TODO.md.
  olski: rejected  0 readings
  sonda: rejected  0 readings, nothing attaches: ,, ,, ,
48 of 48 sentences finished inside 10s, the slowest in 0.07s, and 39 of those get the same verdict from both, 39 the same number of readings
