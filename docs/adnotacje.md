# Adnotacje nad NKJP

Ten dokument rozstrzyga, co ma zapisywać adnotacja nad zdaniem korpusu,
żeby przeżyła gramatykę, wobec której powstała,
i mówi, na które z pytań stawianych czytelnikowi
odpowiada sam podkorpus milionowy NKJP, zanim ktokolwiek zdanie przeczyta.
Po co baza sądów jest i co jest w niej sądem, trzyma
[corpora.md](corpora.md#baza-sądów-ocenia-znaleziska-a-ocenione-nie-wracają).
Tu chodzi o kształt wpisu i o to, co przy nim robi maszyna.

## Sąd o zgłoszeniu starzeje się razem z narzędziem

Wpis bazy mówi o zgłoszeniu.
Nazywa zdanie, zgłoszenie słowem olskiego, wiersz werdyktu z chwili oceny,
sąd `trafne` albo `fałszywe` i powód.
Z tych pięciu pól gramatykę przeżywają dwa.
Zdanie przeżywa, bo stoi w całości i pochodzi z korpusu przypiętego do wydania.
Powód przeżywa, bo mówi o polszczyźnie:
`nagrody czekają, a czekać żąda dopełnienia z przyimkiem na`.
Reszta jest własnością olskiego z tamtej chwili.

Nazwa zgłoszenia jest słownikiem olskiego i widać to na tej bazie.
Wpis nazywa swoje pole `znalezisko` i wpisuje w nie `wieloznaczne`,
a wieloznaczność znaleziskiem być przestała
([subset.md](subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)):
`ZNALEZISKA` w `olski/werdykt/tekst.py` niosą dwie nazwy i tej wśród nich nie ma.
Wpisy zostały prawdziwe, a nazwa ich pola prawdą być przestała,
i nie zgłosił tego żaden check, bo czytnik pyta o `ZGŁOSZENIA`, a nie o nią.

Wiersz werdyktu jest wydrukiem narzędzia
i sonda liczy go za sam zapis tego, co oceniający widział.
Sąd odpowiada na pytanie, które postawił tamten werdykt:
`fałszywe` nad zdaniem o kilkuset odczytaniach mówi,
że czytelnik rozstrzygnął naraz cztery przyłączenia i łańcuch dopełniaczowy,
a nie mówi, jak rozstrzygnął którekolwiek z nich.
Produkcja, która potem zabierze trzy z tych wyborów,
zostawia wpis prawdziwy i bezużyteczny:
sonda powie, że zgłoszenie dalej pada,
a czy zostało czytanie, które czytelnik miał, nie powie nikt.

Powód tę odpowiedź zapisuje, ale zapisuje ją prozą,
której następny olski nie przeczyta niczym poza oczami.

## Jednostką adnotacji jest wybór, a zapisuje się go słowami zdania

Trwałe jest to, co czytelnik odpowiedział na każdy wybór, który zdanie stawia,
a wybory olski już nazywa i nazywa je słowami zdania:
rolę, czyli która grupa jest podmiotem;
przyłączenie, czyli `„w Gryficach” → „leży”, „szpitalu”`;
budowę, czyli konstytuent, który czyta się kilkoma sposobami.
Wpis ma więc zapisywać wybór po wyborze, tak jak robi to już
[plik wyborów przyłączeniowych](rozstrzyganie.md#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów):
fraza, kandydaci, odpowiedź, powód.
Odpowiedzią jest forma zdania, którą czytelnik wybrał,
`oba`, gdy oba czytania mówią o świecie to samo,
`niejasne`, gdy czytelnik ma dwa rozumienia,
albo `żadne`, gdy wybór jest pozorny.
Sąd o zgłoszeniu wychodzi z tego rachunkiem:
wieloznaczność jest `trafne` wtedy, gdy któryś wybór jest `niejasne`,
i niczego więcej wpis o zgłoszeniu nie mówił.

Cztery rzeczy ten kształt kupuje.
Wieloznaczność wraca do znalezisk kształtem, a nie całością
([subset.md](subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem)),
a kształt jest właśnie tym, co wpis o wyborze zapisuje:
sąd nad rolą dwóch grup o zlanych przypadkach
i sąd nad przyłączeniem wyrażenia przyimkowego
stoją w takim wpisie osobno, zamiast składać się na jedno `fałszywe`.
Wybór, który gramatyka potem rozstrzygnie sama, dostaje ocenę, a nie odnotowanie:
sonda pyta, czy rozstrzygnęła go tak, jak czytelnik,
a to jest wzorzec dla warstwy rozstrzygającej, którego brak nazywa
[disambiguation.md](disambiguation.md#czego-brakuje-żeby-odpowiedzieć-pomiarem).
Zawężenie gramatyki, które zabiera czytanie czytelnika,
wychodzi jako strata nad wpisem, choćby zgłoszenie dalej padało.
Produkcja, która nad ocenionym zdaniem stawia wybór nowy,
zgłasza się jako jeden nowy wybór, a nie jako zdanie do przeczytania od nowa.

**Napis, a nie kod.**
Wpis niesie zdanie w całości, choć korpus ma dla niego identyfikator,
bo wpis czyta się i sprawdza bez archiwum,
a wydanie następne go nie unieważnia.
Pole `plik` nazywa próbkę i sekcję,
i to wystarcza, żeby zdanie odnaleźć w warstwach korpusu,
bo tekst sekcji jest tym, z czego proza powstała.
Wybór nazywa się słowami zdania z tego samego powodu:
są jedynymi kodami, których nie rusza żadna zmiana w olskim.
Nazwa roli jest słowem olskiego i wolno ją przemianować,
a rejestr kodów wyborów byłby drugą deklaracją tego, co gramatyka stawia,
czyli kopią, która milczy o wyborze dopisanym później.
Wiersz werdyktu zostaje jako zapis tego, co oceniający widział, a nie jako klucz.

Ta sekcja zastępuje kształt wpisu, który opisuje
[corpora.md](corpora.md#baza-sądów-ocenia-znaleziska-a-ocenione-nie-wracają):
dzisiejsze wpisy są o zgłoszeniu, a nie o wyborze.
Zmiana, która przepisze bazę na wybory, scala te dwa opisy w jeden:
kształt wpisu przechodzi tutaj,
a tamten dokument zostaje właścicielem celu bazy i tego, co jest sądem.

## Korpus sam odpowiada na wybór, który jest odczytaniem formy

Podkorpus milionowy jest anotowany ręcznie
i warstwy tej anotacji jadą w archiwum obok tekstu.
`ann_morphosyntax.xml` daje każdej formie jedno odczytanie wybrane przez anotatora,
`ann_groups.xml` nazywa grupy imienne i przyimkowe wraz z ich głowami,
a `ann_named.xml` i `ann_senses.xml` nazwy własne i znaczenia słów.
Pierwsza z nich odpowiada na część wyborów, które olski stawia,
bo wybór między podmiotem a dopełnieniem jest nad `Czekają nagrody.`
wyborem przypadka jednej formy, a anotator ten przypadek wybrał.
Odpowiedź jest przy tym rodzimego czytelnika i jest nad każdym zdaniem korpusu,
a nie nad tymi kilkudziesięcioma, które przeczytała sesja.

`harness/znaczniki.py` przykłada tę warstwę do gramatyki tak,
jak [pomiar nad Składnicą](corpus.md#what-morphological-ambiguity-costs)
przykłada złote znaczniki banku drzew:
rozbiera zdanie z Morfeuszem i drugi raz z odczytaniami zawężonymi do złotego,
a różnica liczby czytań jest tym, co rozstrzygnął anotator.
Zawężenie schodzi do wartości cechy, bo Morfeusz pisze przypadek alternatywą
i samo odsianie odczytań zostawiłoby `nagrody` z mianownikiem i biernikiem naraz.

```sh
python3 -m harness.znaczniki nkjp/ --proza proza/nkjp
python3 -m harness.znaczniki nkjp/ --sądy
```

Zdanie wieloznaczne wychodzi w jednej z trzech klas.
Rozstrzygnięte: złoto zostawia jedno czytanie,
czyli wieloznaczność była odczytaniem formy.
Pozostaje: czytań zostaje kilka,
czyli różnią się czymś, czego żadna forma nie niesie,
a jest to przyłączenie albo budowa grupy.
Przepadło: żadne czytanie olskiego nie składa się z form, które wybrał anotator.
Zdanie o jednym czytaniu może złotu tylko zaprzeczyć, i to liczy się osobno.

Nad wydaniem 1.2 podkorpusu olski czyta około jednego zdania na pięć,
a większość z czytanych kilkoma czytaniami.
Z tych wieloznacznych złoto rozstrzyga samo około jednego na pięć,
nad drugim tyle samo przepada,
a nad przeszło połowie zostawia kilka czytań.
Zdaniom o jednym czytaniu zaprzecza częściej niż jednemu na dziesięć.
Udział rozstrzygniętych jest najwyższy w warstwach mówionych,
a najniższy w urzędowej.
Podział napisu inny niż u anotatora
i forma bez odczytania zgodnego ze złotym
zabierają razem mniej niż jedną formę na sto,
więc reszta liczb nie jest własnością przyłożenia.
Liczby dzisiejsze drukuje przebieg.

Nad bazą sądów złoto rozstrzyga samo około jednego wpisu na pięć,
a w każdym z nich odczytanie, które zostaje, jest tym, które nazywa powód.
Te wpisy mają przez to drugą ocenę, i jest to ocena rodzimego czytelnika,
której żaden inny wpis bazy nie ma.

**Czego złoto nie mówi.**
Przyłączenia żadna warstwa tego korpusu nie zapisuje:
`w Gryficach` jest w warstwie grup osobną grupą przyimkową, a nie częścią `w szpitalu`,
i tak samo `z Nowej Huty` stoi obok grupy `ciało poszukiwanego noworodka`, a nie w niej.
Nie mówi też, czy drugie czytanie było dla anotatora czytaniem:
anotator musiał wybrać, więc jego wybór mówi, które, a nie czy oba,
i jest to ta sama granica, którą ma bank drzew
([disambiguation.md](disambiguation.md#czego-brakuje-żeby-odpowiedzieć-pomiarem)).
Baza sądów ma przez to czytać zdania z klasy `pozostaje`,
bo tam czytelnik jest jedynym, kto odpowie,
a zdanie rozstrzygnięte złotem kosztuje jego uwagę bez potrzeby.

**Klasa `przepadło` jest kolejką pytań do gramatyki, a nie werdyktem o niej.**
Zdanie wpada tam, gdy każde czytanie olskiego używa odczytania, którego anotator nie wziął.
`Sam jestem odpowiedzią na pytanie.` czyta olski z `Sam` jako przysłówkiem,
a anotator wziął przymiotnik;
`dokładnie odwrotnie` czyta olski przysłówkiem, a anotator partykułą;
`Janina Michaluk` czyta olski nazwiskiem męskim,
bo dwu mianowników żeńskich obok siebie nie ma czym wyprowadzić,
a anotator wziął żeński.
Pierwsze mówi o gramatyce, drugie o granicy między dwoma tagsetami,
trzecie o apozycji, której olski nie ma,
i które z nich jest usterką, rozstrzyga czytanie,
tak jak nad wierszem `lost`
[pomiaru nad Składnicą](corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).
Osobno liczy się forma, której żadne odczytanie Morfeusza nie mieści złotego,
bo słownik nie ma tego słowa
albo wykluczenie leksykalne olskiego zdjęło odczytanie, które anotator wziął;
taka forma zostaje ze wszystkimi odczytaniami, a licznik mówi, ile ich było.

**Klasa `sprzeczne` mierzy to, czego baza sądów zmierzyć nie mogła.**
Baza powstaje ze zgłoszenia, więc o zdaniu, które olski czyta jednym czytaniem,
nie ma ani jednego wpisu
([disambiguation.md](disambiguation.md#wieloznaczność-której-werdykt-nie-melduje)).
Złoto pyta i o nie:
zdanie o jednym czytaniu, które po zawężeniu nie ma żadnego,
używa formy tak, jak anotator jej nie przeczytał,
i olski o tym nie zgłosił nic.
Pierwsze przykłady z wydruku są jednej klasy:
`Wszyscy czuli ulgę.` i `Niektórym się sprawdziło.` czyta olski
z zaimkiem przymiotnym jako rzeczownikiem, bo Morfeusz daje mu i takie odczytanie,
a anotator wziął przymiotnik;
`Sporo wiesz.` czyta przysłówkiem, a anotator liczebnikiem.
Czytanie zostaje to samo i o świecie mówi to samo,
więc zaprzeczenie jest tu pytaniem o to, którym odczytaniem gramatyka ma brać zaimek,
a nie usterką werdyktu.
Które zaprzeczenia są czym innym, mówi dopiero przeczytanie tej klasy.

## Sources

- `README` w archiwum podkorpusu, które mówi, że anotacja jest ręczna,
  i `NKJP_1M_header.xml`, który nazywa jej narzędzie
  ([corpora.md](corpora.md#the-national-corpus-of-polish) mówi, skąd wziąć archiwum)
- Przepiórkowski, Bańko, Górski, Lewandowska-Tomaszczyk (red.),
  *Narodowy Korpus Języka Polskiego*, PWN 2012 — opis warstw anotacji
