#  Ten plik powstaje przebiegiem: python3 -m harness.figury readme
polecenie: python3 -m olski.check proza/README.txt
korpus: proza/README.txt
czyta: docs/corpus.md#where-the-analyses-stop
ruszają:
  README.md: 77c9bdac3583
  harness/markdown.py: 77dba5daa3d8
  olski/subset.py: 24ea4b747a3e
  olski/grammar.py: 9077925971d9
  olski/parse.py: b0553f072e6c
  olski/morph.py: 68c6bc12d9f1
  olski/check.py: 268664a6f662
  olski/document.py: 1aaece1977ef
  olski/leksykon.txt: 00193493b3ea
  olski/projekt.py: 029325944002
  olski/projekt.txt: bce2eab3e8dc

proza/README.txt: rejected  Język olski to język polski, któremu spiłowano p, a razem z nim te części polszczyzny, przez które jest ona trudna dla sztywnych, zimnych maszyn.
                            no reading: no production takes „spiłowano”, „p”
proza/README.txt: rejected  Zdanie jest w olskim poprawne dopiero wtedy, gdy ma dokładnie jedno czytanie, więc parser tego podzbioru mówi autorowi, że jego zdanie czyta się dwojako, zamiast wybierać za niego.
                            no reading: no production takes „dopiero”
proza/README.txt: rejected  Tanio, deterministycznie i z wyjaśnieniem: jak w kompilatorze, a nie jak w modelu językowym.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Każdy werdykt przychodzi z czytaniem, które go wydało, a to samo wejście dwa razy daje tę samą odpowiedź.
                            no reading: nothing in olski derives this
proza/README.txt: ambiguous Obok parsera stał tu linter stylu dla polskiej dokumentacji technicznej i został wycofany razem z całą analizą, która schodziła do znaku.
                            18 readings, differing in Object, Predicative; „dla polskiej dokumentacji technicznej” → „stał”, „linter”, „stylu”; „z całą analizą, która schodziła” → „został”, „razem”; „do znaku” → „został”, „schodziła”
proza/README.txt: rejected  Dlaczego, mówi docs/linter.md; ile ten pakiet reguł kosztował, zanim wyszedł, mówi docs/firing-rates.md.
                            no reading: no production takes „;”
proza/README.txt: rejected  Język kontrolowany to biała lista: istnieją tylko te konstrukcje, które na niej stoją.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Linter to czarna lista: pisz, co chcesz, ale te wzorce zostaną zgłoszone.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Zbiór tekstów przechodzących przez wszystkie reguły jest podzbiorem polszczyzny w jednym i w drugim przypadku, a wyznaczenie go przez wykluczanie jest nieporównanie tańsze.
                            no reading: no production takes „wyznaczenie”, „wykluczanie”
proza/README.txt: ambiguous Po to ta czarna lista tu stała i cały wywód za nią dalej stoi.
                            2 readings; „za nią” → „wywód”, „stoi”
proza/README.txt: valid     Czarna lista kupowała jednak co innego, niż obiecywała.
                            one reading
proza/README.txt: rejected  Reguła, która rozstrzyga o zdaniu znakiem w nim postawionym, nie mówi o polszczyźnie tego zdania nic, a na głębszym poziomie analizy przestaje być tania: pomiar nad dwoma korpusami mówi, że taki poziom odpowiada na inne pytanie niż to, które reguła zadaje.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Cenę białej listy płacimy więc tym, że autor nie czuje, którędy biegnie granica, a odrabiamy tym, że parser pokazuje oba czytania zamiast samej odmowy: granicę widać w odpowiedzi, a nie tylko w tym, że odpowiedzi nie ma.
                            no reading: no production takes „widać”
proza/README.txt: rejected  Tory są dwa: gramatyka zaprojektowanego podzbioru polszczyzny i skład, nazwany kalamburem od składni.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Oba tory mierzymy na tym pliku, który dla jednego z nich jest zarazem celem: skład rośnie tak długo, aż każde jego zdanie wypuści z drzewa, a gramatyka celu końcowego nie ma i rośnie za cenę liczoną przed dopisaniem.
                            no reading: no production takes „zarazem”, „dopisaniem”
proza/README.txt: rejected  Kierunkiem nie jest sam formalizm: gramatyka bezkontekstowa jest tym, na czym olski stoi, a nie tym, do czego zmierza, więc o sięgnięciu po mocniejszy mechanizm rozstrzyga cena.
                            no reading: no production takes „sięgnięciu”
proza/README.txt: valid     Zobacz docs/design-notes.md oraz docs/roadmap.md.
                            one reading
proza/README.txt: rejected  Nie ma aplikacji, która by to wszystko napędzała.
                            no reading: no production takes „by”
proza/README.txt: valid     Projekt jest dla przyjemności.
                            one reading
proza/README.txt: valid     Działają dwie rzeczy.
                            one reading
proza/README.txt: rejected  Gramatyka podzbioru polszczyzny, nad Morfeuszem 2, w której zdanie jest olski wtedy, gdy ma dokładnie jedno czytanie.
                            no reading: no production takes „2”
proza/README.txt: rejected  Nie chodzi o samo jedno wyprowadzenie: Koszt samej szynki przewyższa koszt szynki z dodatkami rozkłada się na kilka czytań, a dwa z nich mówią rzecz przeciwną, więc olski to zdanie odrzuca.
                            no reading: no production takes „wyprowadzenie”
proza/README.txt: rejected  Czytania szynki różnią się szykiem i tym, do czego dochodzi z dodatkami.
                            no reading: nothing in olski derives this
proza/README.txt: ambiguous Pierwsze i czwarte dzieli sam szyk, a podmiot jednego jest dopełnieniem drugiego.
                            3 readings, differing in Adverb, Object, Subject
proza/README.txt: rejected  Wiersz werdyktu nazywa przy tym sam wybór, a nie wylicza jego skutków: wierszy jest tyle, ile zdanie zostawia nierozstrzygniętych wyborów, a czytań bywa tyle, ile ich iloczyn.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Wyborem jest tu przyłączenie, a nad innym zdaniem bywa nim konstytuent, który czyta się kilkoma sposobami tam, gdzie streszczenie nie zagląda.
                            no reading: no production takes „przyłączenie”
proza/README.txt: rejected  Zgodność form jest tu parsowaniem, a nie sprawdzeniem po nim: Nowa program nie ma wyprowadzenia, więc nie jest to reguła, która strzeliła, tylko zdanie, którego nie ma.
                            no reading: no production takes „parsowaniem”, „sprawdzeniem”, „wyprowadzenia”
proza/README.txt: rejected  Co gramatyka obejmuje, czego nie obejmuje i dlaczego przyłączenie wyrażenia przyimkowego zostaje przy czytelniku, mówi docs/subset.md.
                            no reading: no production takes „przyłączenie”
proza/README.txt: fragment  Ekstrakcja zamienia korpus w Markdownie w prozę i jest krokiem przed gramatyką, a nie jej częścią:
                            not a sentence: nothing punctuates it as one
proza/README.txt: ambiguous Co ekstrakcja po drodze zmyśla, mówi docs/extraction.md.
                            8 readings, differing in Object, Subject; „po drodze” → „zmyśla”, „ekstrakcja”
proza/README.txt: fragment  Tą samą drogą dochodzi ustawa, tylko że nie akapitami, bo ustawa jest drzewem jednostek redakcyjnych, a nie ciągiem zdań:
                            not a sentence: nothing punctuates it as one
proza/README.txt: rejected  Ile z tego rejestru wychodzi i czego żądają od zdania w ustawie „Zasady techniki prawodawczej”, mówi docs/ustawy.md.
                            no reading: no production takes „„”, „””
proza/README.txt: rejected  Skład, czyli ten sam Morfeusz czytany w drugą stronę.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Wchodzi drzewo tego, co ma zostać powiedziane, a wychodzi polskie zdanie, a z kilku drzew postawionych obok siebie wychodzi tekst.
                            no reading: no production takes „siebie”
proza/README.txt: rejected  Kategorie tego drzewa są kategoriami dziedziny, a nie polszczyzny: mówią, że jedna rzecz jest określeniem drugiej, a nie że stoi tam dopełniacz, i że coś jest celem, a nie że stoi tam biernik.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Zgodność jest liczona po drodze, a nie sprawdzana po niej, więc ten kierunek nie potrzebuje gramatyki i nie dziedziczy jej pokrycia.
                            no reading: nothing in olski derives this
proza/README.txt: ambiguous Nad zdaniem stoi opowieść, bo tekst wie to, czego zdanie samo o sobie nie wie: kiedy to było i o kim mowa była przed chwilą.
                            144 readings, differing in Adverb, AdverbialClause, Object, Subject; „o sobie” → „wie”, „zdanie”; „tekst wie to” reads 2 ways
proza/README.txt: rejected  Pierwsze daje czas przeszły, a drugie podmiot opuszczony tam, gdzie opuszcza go polszczyzna.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Szyk jest tu wnioskiem, a nie zapisem: drzewo mówi, co w zdaniu jest tematem, a co nowe, i dopiero z tego wychodzi kolejność.
                            no reading: no production takes „dopiero”
proza/README.txt: ambiguous Reszta zapisu jest zwykłym Pythonem i to jest w nim zamierzone: zmienna nazywa postać, funkcja jest wzorcem zdania albo akapitu, a lista wchodzi do zdania jako koordynacja.
                            4 readings, differing in Object; „jako koordynacja” → „wchodzi”, „zdania”
proza/README.txt: ambiguous Całą legendę o bazyliszku warszawskim trzyma opowieści/bazyliszek.py.
                            2 readings, differing in Object; „o bazyliszku warszawskim” → „legendę”, „trzyma”
proza/README.txt: fragment  Tym samym kompilatorem wychodzi tekst do makiety, czyli to, po co zwykle sięga się do łacińskiej sieczki:
                            not a sentence: nothing punctuates it as one
proza/README.txt: rejected  Losowane jest drzewo, a nie słowa wstawione w gotowe zdanie, więc zdania różnią się budową, a nie samymi lematami.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Gramatyczności nie ma tu czym naruszyć, bo zgodność jest liczona po drodze, a jedyne, co losowanie odsiewa, to zdanie, z którego czytelnik nie odzyskałby ról.
                            no reading: no production takes „by”
proza/README.txt: ambiguous Czego takie losowanie zażądało od tego pakietu, a czego autor drzewa nie musiał nigdy napisać, mówi docs/sklad.md.
                            2 readings, differing in Object
proza/README.txt: rejected  Szyku wewnątrz grupy imiennej skład nie niesie, i to jest dziura w nim samym.
                            no reading: nothing in olski derives this
proza/README.txt: rejected  Czego brakuje pod nim, w leksykonie i w formach, i w jakiej kolejności to dochodzi, mówi docs/roadmap.md.
                            no reading: nothing in olski derives this
proza/README.txt: valid     Zobacz docs/sklad.md.
                            one reading
proza/README.txt: rejected  Reszta repozytorium to notatki projektowe, przegląd pola, plan i otwarte pytania.
                            no reading: nothing in olski derives this
proza/README.txt: fragment  docs/roles.md: role, w jakich ktoś to repozytorium czyta, gdzie każda z nich wchodzi i co jej drogę psuje, i dlaczego wszystkie obsadza jedna osoba
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/architecture.md: przez jakie warstwy przechodzi zdanie w obu kierunkach, jakim typem jedna oddaje wynik następnej i którą z nich oba tory mają wspólną
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/subset.md: co gramatyka wpuszcza, dlaczego poprawność znaczy jedno czytanie i ile kosztuje przyłączanie wyrażeń przyimkowych
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/sklad.md: na jakim poziomie stoją kategorie drzewa, co tekst wie ponad zdaniem i czego brakuje pod tym w leksykonie i w formach
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/corpus.md: jak mierzy się gramatykę na banku drzew Składnica, co mówi pierwszy pomiar i czego nie dowodzi liczba pokrycia wzięta na wyjściu jednej gramatyki
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/ustawy.md: czego „Zasady techniki prawodawczej” żądają od zdania w ustawie, ile z tego rejestru gramatyka wyprowadza i dlaczego regularne jest w nim drzewo jednostek redakcyjnych, a nie zdanie
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/linter.md: po co był linter, ile analizy potrzebowała która reguła, dlaczego kalibracja rozstrzygała wszystko i co zamknęło ten tor
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/fiction.md: co psuje się w prozie literackiej z modelu, dlaczego odpowiada za to post-training, dlaczego modele w roli sędziów stawiają ją wyżej od New Yorkera i co z niej da się lintować
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/generated-polish.md: co mierzy prawdziwy zbiór wygenerowanej polszczyzny, które wzorce w niej widać i dlaczego korpus redagowany pod detektory jest podłogą, a nie próbką
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/extraction.md: jak korpus w Markdownie dociera do gramatyki jako proza i co ten krok po drodze zmyśla
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/corpora.md: jaką polszczyznę pisaną przez ludzi da się w ogóle zdobyć, co każdy kandydat na korpus mówi o swoim rejestrze, pochodzeniu i licencji, i za jakim doborem przemawia ten przegląd
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/audit-corpus.md: z jakich repozytoriów zrobiony jest korpus audytowy, co trzeba pokazać, żeby do niego wejść, i jak ściągnąć je na tych commitach, na których wzięto liczby
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/firing-rates.md: co pakiet typograficzny robił nad polszczyzną, którą ktoś napisał, czym okazały się jego trafienia, kiedy się je przeczytało, i za jaką cenę ten tor został wycofany
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/roadmap.md: cele, których część jest nieosiągalna, etapy dwóch torów, kierunek jednego i kryterium wyjścia drugiego, i to, dlaczego numeracja jednego nie sięga drugiego
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/prose-linters.md: silniki, które angielski i japoński już mają, ten jeden, który zmierzył własną częstość fałszywych trafień, i to, czego trzeba było, żeby po polsku je pobić
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/similar-work.md: sto kontrolowanych języków naturalnych, jak pole je klasyfikuje i które z ich obietnic ktoś naprawdę zmierzył
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/design-notes.md: tor gramatyczny, czyli co czyni polszczyznę trudną do parsowania, drabina kosztów, urwisko nieciągłości i to, że sam formalizm jest na tym torze środkiem
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/disambiguation.md: co musiałaby rozstrzygać warstwa za parserem, ile z tego jest przyłączeniem, z jaką skutecznością robią to cudze maszyny i dlaczego reszty nie rozstrzyga nic, co stoi w zdaniu
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/open-questions.md: rozwidlenia, na których nie zapadła decyzja
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/prior-art.md: Morfeusz, Morfologik, Świgra, Grammatical Framework i reszta
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/glr-in-practice.md: raport z terenu o małym systemie, który puszcza parser GLR nad prawdziwą polszczyzną, co robi z lasem rozbiorów i co wychodzi jego gramatyce na tysiącu z górą wierszy
                            not a sentence: nothing punctuates it as one
proza/README.txt: fragment  docs/swigra.md: jaki teren zajmuje najbliższy istniejący parser polszczyzny, co zostawia otwarte dla toru gramatycznego i które mechanizmy warto wziąć z jego źródeł
                            not a sentence: nothing punctuates it as one
proza/README.txt: rejected  Prozę w tym repozytorium łamiemy według Semantic Line Breaks, a nową piszemy po polsku, więc czytelnik trafia na oba języki naraz.
                            no reading: no production takes „Semantic”, „Line”, „Breaks”, „polsku”
proza/README.txt: rejected  Konwencje prozy, kodu, testów i commitów trzyma CLAUDE.md, a otwartą robotę wewnątrz repozytorium TODO.md.
                            no reading: nothing in olski derives this
5 of 48 sentences are olski, beside 25 fragments that are not sentences
