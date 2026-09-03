# Role w tym repozytorium

Dokument nazywa role, w których ktoś to repozytorium czyta.
Przy każdej roli stoi pytanie, z którym ona przychodzi.
Stoi tam miejsce, w którym rola wchodzi.
Stoi tam droga, którą ta rola idzie.
Na końcu stoi to, co tę drogę psuje, oraz obsada tej roli.

Potrzeba jest jedna i konkretna.
Zmiana w dokumencie nie ma jak odpowiedzieć, na czyjej drodze leży.
Lista dokumentów w [docs/README.md](README.md) mówi, co stoi w każdym pliku.
Nie mówi, kto po ten plik przychodzi.
Dopisanie akapitu jest przez to tanie.
Przecięcie cudzej drogi jest przy tym niewidoczne.
[Przegląd zmian](../CLAUDE.md#przegląd-sprawdza-zmianę-wobec-całego-tego-pliku)
pyta, jaki problem znika ze zmianą.
Tu stoi druga połowa tego pytania, czyli to, kogo ta zmiana dotyczy.

## Rola jest postawą, nie osobą

Wszystkie role z tej listy obsadza autor repozytorium.
Obsadza je razem z nim każda sesja agenta, która ma w gicie własne commity.
Nie ma wydania ani pakietu.
Nie ma aplikacji, która to wszystko napędza
([README](../README.md#kierunek)).

To jest stan, którego warto pilnować, a nie brak do nadrobienia.
Użytkownik i twórca są zwykle dwiema osobami.
O narzędziu decyduje wtedy ktoś, kto go nie używa.
Używa go ktoś, kto nie ma o nim nic do powiedzenia.
Znika przez to sprzężenie, które trzyma jakość.
Tutaj tego rozejścia nie ma.
Kto pisze produkcję, jest tym, czyje zdanie ona potem odrzuca.
Kto skraca akapit, sam go za tydzień czyta.
Kto odkłada wpis na listę, sam go z tej listy podnosi.
Nieprzyjemna droga boli tego, kto ją zbudował,
i jest to jedyne sprzężenie, które na to działa:
testy pilnują linków i nagłówków,
a tekstu pisanego dla kogoś innego nie zgłasza żaden z nich.

Wychodzą z tego dwie rzeczy dla całej listy poniżej.
Po pierwsze, role są postawami jednej osoby, a nie stanowiskami.
Test dla każdej z nich brzmi przez to tak samo.
Pyta on, czy ktoś w tej postawie trafia na tekst pisany dla innej postawy.
Po drugie, rola bez obsady nie daje żadnego sprzężenia.
Optymalizowanie pod nią jest zgadywaniem.
Każda rola niżej mówi więc, kto ją obsadza.

## Ktoś, kto trafia tu pierwszy raz

Pyta, co to jest i czy go to dotyczy.
Wchodzi na początek [README](../README.md) i czyta w dół.
Wskazanie na [listę dokumentów](README.md) na jego końcu
jest wyjściem, a nie treścią.
Cała droga tej roli mieści się w jednym pliku.
Drugim wejściem jest witryna, o ile ktoś postawi ją pod adresem.
Strona zaczyna od tego samego wprowadzenia i prowadzi do pola tekstowego
([witryna.md](witryna.md#strona-zaczyna-od-tego-czym-olski-jest)).

**Psuje ją** mechanizm postawiony przed ramą.
Psuje ją też nazwa użyta przed wprowadzeniem.
Czytanie i walencja na pierwszej stronie są taką nazwą.
Obie rzeczy są niewidoczne dla autora, bo autor wie, co stoi niżej.
Dlatego [reguła o czytaniu zdanie po zdaniu](../CLAUDE.md#the-reader-goes-sentence-by-sentence)
każe czytać od miejsca edycji tak, jakby dalszej części nie było.

**Obsady** ta rola nie ma.
Jedynym dowodem na tę drogę jest autor czytający README po dłuższej przerwie.

## Ktoś, kto to uruchamia

Pyta, jak odpalić i co znaczy werdykt, który dostał.
Wchodzi przez bloki polecenia w [README](../README.md#co-działa).
Dalej instrukcją jest samo narzędzie.
Flaga `--help` mówi, co program przyjmuje.
Flaga `--readings` pokazuje, czym jedno czytanie różni się od drugiego.
Flaga `--zatrzymania` pokazuje zdania, o których wydruk sam z siebie milczy,
bo znaleziskiem nie jest ani odrzucenie, którego nie zdejmuje jeden znak,
ani napis bez kropki
([pisanie-po-olsku.md](pisanie-po-olsku.md#odrzucenie-mówi-na-czym-stanęło-i-mówi-to-raz)).
Osobnego podręcznika nie ma.
Dokument powtarzający zachowanie gramatyki cicho się z nią rozjeżdża,
bo [kod jest właścicielem tego, co zaimplementowane](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely).
Do dokumentów ta rola wchodzi po jedną rzecz, której z wyjścia nie widać.
Jest nią to,
[dlaczego wieloznaczność jest znaleziskiem, a odrzucenie milczeniem](subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego).

Drugie wejście tej roli jest w przeglądarce i prowadzi do tego samego werdyktu.
Witryna woła tę samą gramatykę.
Pokazuje przy tym frazę, którą drukuje wiersz poleceń
([witryna.md](witryna.md#werdykt-idzie-w-tych-słowach-w-których-drukuje-go-olski-check)).
Osobnego podręcznika strona też nie ma,
bo pole tekstowe pyta o to samo, o co pyta `-c`.

**Psuje ją** werdykt, który nie mówi, czym dwa czytania się różnią.
Psuje ją też odrzucenie podane bez tego, dokąd analiza doszła.

**Obsadza ją** autor, z klona repozytorium.
Instalacji poza klonem nie ma.
Witryna tego nie zmienia, dopóki nikt nie postawi jej pod adresem
([witryna.md](witryna.md#nie-zapadło)).

## Planista

Pyta, co jest na horyzoncie i co jest następne.
Wchodzi w [roadmap.md](roadmap.md), gdzie stoją umowa z autorem, cele i kierunek.
Numerowanych etapów nie ma tam żaden tor gramatyczny,
bo tor ten nie ma końca
([tamże](roadmap.md#tor-gramatyczny-nie-ma-końca)),
a odcinków z kryterium wyjścia dla czegoś, co się nie kończy, nikt nie podnosił.
Kryterium wyjścia ma tam jeden tor i jest nim skład
([tamże](roadmap.md#kryterium-wyjścia-toru-składu-to-znów-readme)).
Dalej rozchodzą się trzy listy.
Granicę między nimi trzyma [nagłówek rejestru](../todo/README.md).
Co zamyka commit w tym repozytorium, jest tam.
Co zamyka świat zewnętrzny, siedzi w [open-questions.md](open-questions.md)
albo w sekcji `Not yet decided` dokumentu, który jest właścicielem tematu.

**Psuje ją** wpis na złej liście.
Wpis czekający na czyjś pomiar, postawiony między pliki do napisania,
czyta się jak następny ruch i nie jest nim.
Plik do napisania odłożony między pytania do świata nie jest w ogóle robotą.

**Obsadzają ją** autor i każda sesja agenta,
bo nagłówek rejestru każe zaglądać tam przed zaczęciem czegokolwiek.

## Autor produkcji

Pyta, jak dopisać gramatyce konstrukcję i co ona kosztuje.
Wchodzi w [subset.md](subset.md), a stamtąd w `olski/subset/`,
gdzie produkcje stoją w module swojego gospodarza.
Testy tych produkcji dzielą się w `tests/` po gospodarzu,
tak jak dzielą się po nim moduły w `olski/subset/`.
Co olski przyjmuje i odrzuca w całości, pyta `tests/test_subset.py`.
Wymaganie idzie z tą rolą od początku i jest jedno:
konstrukcja dopisana gramatyce dokłada czytania każdemu zdaniu, które ją ma.
Zdanie z dwoma czytaniami olski odrzuca.
Pokrycie kupione bez pomiaru bywa przez to pokryciem ujemnym.
Straconym zdaniem jest to, które wychodziło już bez tej produkcji.
Gdzie bez niej nie wychodzi żadne, liczba ruchu nie odwróci.
Co pomiar mówi, trzyma [corpus.md](corpus.md).

Cena odpowiada przy tym na pytanie o wysokość, a nie na pytanie o zasadność.
Kto płaci za odrzucone zdanie, rozstrzyga się z fotela użytkownika.
Kryterium trzyma
[pisanie-po-olsku.md](pisanie-po-olsku.md#kto-płaci-za-odrzucone-zdanie).

Droga jest za każdym razem ta sama.
Tyle o niej trzeba wiedzieć.
Sekcja w [subset.md](subset.md#what-the-grammar-covers) mówi, co już stoi.
Ciało dochodzi do modułu swojego gospodarza w `olski/subset/`.
Cenę wydaje sonda różnicowa pisana na jeden przebieg nad `harness/ruch.py`
([CLAUDE.md](../CLAUDE.md#code)).
Korpusy ściąga się poleceniami z [corpus.md](corpus.md#fetching-it)
oraz z [ustawy.md](ustawy.md#skąd-bierze-się-korpus).
Wywód wraca do sekcji, która tę konstrukcję trzyma,
oraz jednym zdaniem ze wskaźnikiem do [roadmap.md](roadmap.md)
i do dokumentów rejestrów.

**Psuje ją** dokument powtarzający to, co produkcja robi,
bo wtedy istnieją dwie wersje i nie widać, która obowiązuje.

**Obsadzają ją** autor i sesje agenta.

## Ktoś, kto mierzy

Pyta, ile ta gramatyka dziś kosztuje i co ona kupuje.
Odpowiadają mu narzędzia w `harness/`.
Każde z nich drukuje swoje liczby i żadne nie zapisuje ich do repozytorium.
Korpus, bez którego nie ma czego czytać, ściąga się raz na sesję
([corpus.md](corpus.md#fetching-it)).
Dwa programy tego pakietu do repozytorium jednak piszą i pomiarem nie są.
Pliki, które gramatyka potem czyta, wypisują `harness/walenty.py`
oraz `harness/skłonności.py`.
Co z tego wynika, mówi
[CLAUDE.md](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje).
Dokument liczby dokładnej nie nosi, bo zwykły rozwój projektu ją unieważnia.
Zdanie w dokumencie mówi więc rząd wielkości, a przebieg mówi liczbę.
Wyjątkiem są liczby policzone silnikiem, który wyszedł razem z pakietem reguł.
Każdy dokument, który je nosi, mówi to o sobie sam.
[firing-rates.md](firing-rates.md) nazywa wypisane w sobie polecenia zapisem,
a nie robotą do powtórzenia.
[corpora.md](corpora.md#how-the-counts-here-were-taken)
oraz [audit-corpus.md](audit-corpus.md#the-list)
mówią, że ostatni krok ich liczenia pisze na nowo ten, kto je powtarza.

**Psuje ją** liczba w dokumencie bez polecenia, które ją wyprodukowało.
Psuje ją też przebieg wystartowany przed ostatnią edycją.
Taki przebieg mierzy kod sprzed niej i nigdzie tego nie mówi.

**Obsadza ją** autor.
Widać to po tabelach, które mają datowane pochodzenie.

## Czytelnik toru gramatycznego

Pyta, co olski parsuje i dlaczego wieloznaczność jest znaleziskiem, a odrzucenie milczeniem.
Wchodzi w [subset.md](subset.md), a dalej w [design-notes.md](design-notes.md)
po drabinę kosztów i po urwisko nieciągłości.
Sąsiedztwo tego toru opisują [swigra.md](swigra.md),
[glr-in-practice.md](glr-in-practice.md) oraz [prior-art.md](prior-art.md).
W kodzie są to `olski/grammar.py` i `olski/check.py`.
Kto wchodzi stąd w `olski/parse/`, czyta [parsowanie.md](parsowanie.md),
bo ten dokument wywodzi las i to, co werdykt nad nim mówi.

**Psuje ją** dokument tego toru otwierający się zastrzeżeniem,
że tor jest opcjonalny i czyta się go drugi.
Gramatyka jest [tym, co budowane](roadmap.md#co-jest-budowane),
więc takie zdanie odsyła czytelnika, który przyszedł po główną rzecz.

**Obsadza ją** autor, z przerwami.

## Czytelnik toru składu

Pyta, co wchodzi do kompilatora i dlaczego drzewo mówi o rzeczach, a nie o przypadkach.
Wchodzi w [sklad.md](sklad.md), a stamtąd w
[etapy tego toru](roadmap.md#tor-składu-drzewo-wchodzi-polskie-zdanie-wychodzi).
Gramatyki po drodze nie potrzebuje, bo parser stoi tu świadkiem, a nie zależnością
([design-notes.md](design-notes.md#the-round-trip-invariant)).
W kodzie są to `olski/skład/składnia.py` i `olski/skład/morfologia.py`.
Tekstem, na którym widać braki, jest `opowieści/bazyliszek.py`.
Czego nie ma pod nim w żadnym leksykonie, pokazuje losowanie
w `olski/skład/makieta.py`.

**Psuje ją** kategoria opisana słowem z rozbioru zdania.
Zapis, który miał mówić, o czym zdanie jest, mówi wtedy, jak zdanie stoi.
Psuje ją też droga wiodąca przez dokument tamtego toru,
bo czytelnik dostaje najpierw las rozbiorów, a potem to, po co przyszedł.

**Obsadza ją** autor.
Widać to po tym, że kolejkę konstrukcji ustawił tekst,
a nie lista spisana z góry
([kategorie-zapisu.md](kategorie-zapisu.md#najpierw-tekst-potem-drzewo-na-końcu-biblioteka)).

## Ktoś, kto zestawia to z tym, co już istnieje

Pyta, czy to samo nie zostało już zrobione i czy nie zostało zrobione lepiej.
Wchodzi w [prose-linters.md](prose-linters.md) po silniki,
które angielski i japoński już mają.
Wchodzi w [similar-work.md](similar-work.md) po sto języków kontrolowanych
oraz po te ich obietnice, które ktoś zmierzył.
Bierze stamtąd także
[poziom, na którym stoją generatory](similar-work.md#generowanie-rozdziela-się-poziomem-wejścia).
W [swigra.md](swigra.md) szuka tej samej rzeczy na torze gramatycznym.

**Psuje ją** ocena stopniująca bez podstawy.
Ta rola przyszła sprawdzić właśnie takie zdania,
a [jedno niepodparte kosztuje wiarygodność reszty](../CLAUDE.md#a-claim-about-the-world-says-how-to-check-it).

**Obsady** ta rola nie ma.
Sprzężona jest najsłabiej z całej listy.
Trzy dokumenty pisane dla kogoś z zewnątrz czytał tylko ten, kto je napisał.

## Sesja agenta

Pyta, jaka jest konwencja i którą decyzję ta sesja rozstrzyga.
Wchodzi w [CLAUDE.md](../CLAUDE.md) i czyta całość,
bo to jedyna kopia konwencji.
Potem wchodzi w [todo/](../todo/README.md).
Ta rola różni się od pozostałych trzema rzeczami, które robią jej całą drogę.
Przychodzi za każdym razem na zimno.
[Nie widzi innych sesji](../CLAUDE.md#splitting-work-across-sessions).
Dostaje klon,
[który pokazuje historię obciętą albo nieświeżą](../CLAUDE.md#git-w-sesji-zdalnej).

**Psuje ją** konwencja, która istnieje tylko w komunikacie commita
albo w pamięci innej sesji.
Psuje ją też podział pracy zrobiony po plikach zamiast po rozstrzyganych decyzjach,
bo dwie sesje dochodzą wtedy do tego samego wniosku dwa razy
i żaden merge tego nie zgłasza.
Psuje ją wreszcie wpis z [todo/](../todo/README.md) wykonany tak, jak stoi,
bo nie ma kogo zapytać, czy nazwany w nim ruch jest czymś więcej niż zgadnięciem.

**Obsadzają ją** sesje agenta, które mają w gicie własne commity.
Cały [CLAUDE.md](../CLAUDE.md) jest pisany pod tę rolę.

## Czego na tej liście nie ma

Recenzent nie jest rolą, tylko fazą.
Kończy ją każda postawa cokolwiek pisząca.
Opisuje ją [przegląd zmian](../CLAUDE.md#przegląd-sprawdza-zmianę-wobec-całego-tego-pliku).
Nie ma autora reguły, bo wyszedł razem z pakietem reguł.
Kto chciałby tę rolę obsadzić na nowo,
zaczyna od tego, [co ją zamknęło](linter.md#co-zamknęło-pakiet-reguł),
a nie od formatu, w którym reguła kiedyś stała.
Nie ma też roli osoby dokładającej się z zewnątrz.
Rozdzielenie CLAUDE.md na wersję dla autora i wersję dla gości
kosztowałoby dwie kopie tych samych reguł, żeby obsłużyć nikogo.
