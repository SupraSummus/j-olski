# Role w tym repozytorium

Dokument nazywa role, w jakich ktoś to repozytorium czyta,
a dla każdej z nich: pytanie, z którym przychodzi,
miejsce, w którym wchodzi, drogę, którą idzie,
to, co tę drogę psuje,
i na koniec to, kto ją obsadza.

Potrzeba jest jedna i konkretna.
Zmiana w dokumencie nie ma jak odpowiedzieć, na czyjej drodze leży.
Lista dokumentów w [README](../README.md) mówi, co w którym jest,
i nie mówi, kto po to przychodzi,
więc dopisanie akapitu jest tanie,
a przecięcie komuś drogi niewidoczne.
[Przegląd zmian](../CLAUDE.md#the-review-pass) pyta, jaki problem znika ze zmianą;
tu stoi druga połowa tego pytania, czyli kogo ta zmiana dotyczy.

## Rola jest postawą, nie osobą

Wszystkie role z tej listy obsadza autor repozytorium, jedna osoba na wszystkie,
plus sesje agenta, które mają w historii gita własne commity.
Nie ma wydania, nie ma pakietu, nie ma aplikacji, która to napędza:
[README](../README.md#kierunek) mówi, że projekt jest dla przyjemności.

To jest stan, którego warto pilnować, a nie brak do nadrobienia.
Alienacja pracy, którą Marks opisał
w *Rękopisach ekonomiczno-filozoficznych* z 1844 roku,
to oddzielenie pracującego od wytworu jego pracy,
a tutaj chodzi o jeden jej przypadek:
użytkownik i twórca to dwie różne osoby.
Wtedy o narzędziu decyduje ktoś, kto go nie używa,
używa go ktoś, kto nie ma o nim nic do powiedzenia,
i znika sprzężenie, które samo z siebie trzyma jakość.
Tutaj tego rozejścia nie ma.
Kto pisze produkcję, jest tym, czyje zdanie ona potem odrzuca;
kto skraca akapit, sam go za tydzień czyta;
kto odkłada wpis na listę, sam go z tej listy podnosi.
Nieprzyjemna droga boli tego, kto ją zbudował,
i jest to jedyne sprzężenie, jakie na to działa:
testy pilnują linków i nagłówków,
a tekstu pisanego dla kogoś innego nie zgłasza żaden z nich.

Stąd dwie rzeczy dla całej listy poniżej.
Po pierwsze, role są postawami tej samej osoby, a nie stanowiskami,
więc test dla każdej z nich brzmi tak samo:
czy ktoś w tej postawie trafia na tekst pisany dla innej postawy.
Po drugie, rola bez obsady nie daje żadnego sprzężenia,
a optymalizowanie pod nią jest zgadywaniem,
więc każda rola niżej mówi, kto ją obsadza.

## Ktoś, kto trafia tu pierwszy raz

Pyta, co to jest i czy go to dotyczy.
Wchodzi na początek [README](../README.md) i czyta w dół,
a lista dokumentów na jego końcu jest wyjściem, nie treścią:
cała droga tej roli mieści się w jednym pliku.

**Psuje ją** mechanizm postawiony przed ramą
i nazwa użyta przed wprowadzeniem, czytanie albo walencja na pierwszej stronie.
Obie rzeczy są niewidoczne dla autora, bo autor wie, co jest niżej,
i dlatego [przegląd zmian](../CLAUDE.md#the-review-pass) każe czytać od miejsca edycji
tak, jakby dalszej części nie było.

**Obsady** ta rola nie ma.
Jedyny dowód, że ta droga działa,
to autor czytający README po dłuższej przerwie.

## Ktoś, kto to uruchamia

Pyta, jak odpalić i co znaczy werdykt, który dostał.
Wchodzi przez bloki polecenia w [README](../README.md#co-działa),
a dalej instrukcją jest samo narzędzie:
`--help` mówi, co przyjmuje, a `--readings` pokazuje,
czym jedno czytanie różni się od drugiego.
Osobnego podręcznika nie ma,
a dokument powtarzający zachowanie gramatyki cicho się z nią rozjeżdża,
bo [kod jest właścicielem tego, co zaimplementowane](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely).
Do dokumentów ta rola wchodzi po jedną rzecz, której z wyjścia nie widać:
[dlaczego poprawność znaczy tu jedno czytanie](subset.md#validity-is-uniqueness-not-just-derivability).

**Psuje ją** werdykt, który nie mówi, czym dwa czytania się różnią,
oraz odrzucenie podane bez tego, dokąd analiza doszła.

**Obsadza ją** autor, z klona repozytorium.
Instalacji poza klonem nie ma.

## Planista

Pyta, co jest na horyzoncie i co jest następne.
Wchodzi w [roadmap.md](roadmap.md), gdzie każdy etap ma kryterium wyjścia,
a numeracja jest kolejnością i jest nośna;
całego toru gramatycznego nie zamyka żadne
([tamże](roadmap.md#tor-gramatyczny-nie-ma-końca)).
Dalej rozchodzą się trzy listy, a granicę między nimi
trzyma nagłówek [TODO.md](../TODO.md):
co zamyka commit w tym repozytorium, jest tam,
a co zamyka świat zewnętrzny, siedzi w [open-questions.md](open-questions.md)
albo w sekcji `Not yet decided` dokumentu, który jest właścicielem tematu.

**Psuje ją** wpis na złej liście.
Wpis czekający na czyjś pomiar, postawiony między pliki do napisania,
czyta się jak następny ruch i nie jest nim,
a plik do napisania odłożony między pytania do świata nie jest w ogóle robotą.

**Obsadzają ją** autor i każda sesja agenta,
bo nagłówek TODO.md każe zaglądać tam przed zaczęciem czegokolwiek.

## Autor produkcji

Pyta, jak dopisać gramatyce konstrukcję i co ona kosztuje.
Wchodzi w [subset.md](subset.md), stamtąd w `olski/subset.py`,
gdzie produkcje stoją jedna pod drugą, z testami w `tests/test_subset.py`.
Wymaganie idzie z tą rolą od początku i jest jedno:
konstrukcja dopisana gramatyce dokłada czytania każdemu zdaniu, które ją ma,
a zdanie z dwoma czytaniami olski odrzuca,
więc pokrycie kupione bez pomiaru bywa pokryciem ujemnym.
Co pomiar mówi, trzyma [corpus.md](corpus.md).

**Psuje ją** produkcja dopisana bez przebiegu nad bankiem drzew,
bo wtedy nie widać, ile zdań straciła,
i dokument powtarzający to, co produkcja robi,
bo wtedy istnieją dwie wersje i nie widać, która obowiązuje.

**Obsadzają ją** autor i sesje agenta.

## Ktoś, kto mierzy

Pyta, która liczba się ruszyła i co trzeba przeliczyć.
Wchodzi w [sekcję Checks](../CLAUDE.md#checks),
bo to ona wymienia dokumenty z liczbami, do których nie dosięga żaden test,
a dalej idzie do tego z nich, który jest właścicielem danej liczby.
Każdy z nich wypisuje polecenia, które jego tabele produkują,
i po to te polecenia tam są.
Jeden wyjątek zna ta droga i jest nazwany na miejscu:
[firing-rates.md](firing-rates.md) mierzył pakietem, którego już nie ma,
więc wypisane w nim polecenia są zapisem, a nie robotą do powtórzenia.

**Psuje ją** liczba w dokumencie bez polecenia, które ją wyprodukowało,
oraz przebieg wystartowany przed ostatnią edycją,
który mierzy kod sprzed niej i nigdzie tego nie mówi.

**Obsadza ją** autor, i widać to po tabelach, które mają datowane pochodzenie.

## Czytelnik toru gramatycznego

Pyta, co olski parsuje i dlaczego zdanie jest poprawne dopiero przy jednym czytaniu.
Wchodzi w [subset.md](subset.md), dalej w [design-notes.md](design-notes.md)
po drabinę kosztów i urwisko nieciągłości,
a sąsiedztwo tego toru opisują
[swigra.md](swigra.md), [glr-in-practice.md](glr-in-practice.md)
i [prior-art.md](prior-art.md).
W kodzie to `olski/grammar.py` i `olski/check.py`.

**Psuje ją** dokument tego toru otwierający się zastrzeżeniem,
że tor jest opcjonalny i czyta się go drugi:
gramatyka jest [tym, co budowane](roadmap.md#co-jest-budowane),
więc takie zdanie odsyła czytelnika, który przyszedł po główną rzecz.

**Obsadza ją** autor, z przerwami.

## Czytelnik toru składu

Pyta, co wchodzi do kompilatora i dlaczego drzewo mówi o rzeczach, a nie o przypadkach.
Wchodzi w [sklad.md](sklad.md), a stamtąd w
[etapy tego toru](roadmap.md#tor-składu-drzewo-wchodzi-polskie-zdanie-wychodzi);
gramatyki po drodze nie potrzebuje, bo parser stoi tu świadkiem, a nie zależnością
([design-notes.md](design-notes.md#the-round-trip-invariant)).
W kodzie to `skład/składnia.py` i `skład/morfologia.py`,
a tekstem, na którym widać, czego brakuje, jest `opowieści/bazyliszek.py`;
czego nie ma pod nim w żadnym leksykonie, pokazuje losowanie w `skład/makieta.py`.

**Psuje ją** kategoria opisana słowem z rozbioru zdania,
bo wtedy zapis, który miał mówić, o czym zdanie jest, mówi, jak zdanie stoi,
oraz droga wiodąca przez dokument tamtego toru,
bo czytelnik dostaje najpierw las rozbiorów, a potem to, po co przyszedł.

**Obsadza ją** autor, i widać to po tym, że kolejkę konstrukcji ustawił tekst,
a nie lista spisana z góry
([sklad.md](sklad.md#najpierw-tekst-potem-drzewo-na-końcu-biblioteka)).

## Ktoś, kto zestawia to z tym, co już istnieje

Pyta, czy to samo nie zostało już zrobione i czy nie zostało zrobione lepiej.
Wchodzi w [prose-linters.md](prose-linters.md) po silniki,
które angielski i japoński już mają,
w [similar-work.md](similar-work.md) po sto języków kontrolowanych,
po to, które z ich obietnic ktoś zmierzył,
oraz po [poziom, na którym stoją generatory](similar-work.md#generowanie-rozdziela-się-poziomem-wejścia),
a w [swigra.md](swigra.md) po tę samą rzecz na torze gramatycznym.

**Psuje ją** ocena stopniująca bez podstawy, najlepszy albo jedyny,
bo ta rola przyszła sprawdzić właśnie takie zdania
i [jedno niepodparte kosztuje wiarygodność reszty](../CLAUDE.md#a-claim-about-the-world-says-how-to-check-it).

**Obsady** ta rola nie ma, i jest sprzężona najsłabiej z całej listy.
Trzy dokumenty pisane dla kogoś z zewnątrz
czytał tylko ten, kto je napisał.

## Sesja agenta

Pyta, jaka jest konwencja i którą decyzję ta sesja rozstrzyga.
Wchodzi w [CLAUDE.md](../CLAUDE.md) i czyta całość,
bo to jedyna kopia konwencji, a potem w [TODO.md](../TODO.md).
Ta rola różni się od pozostałych trzema rzeczami, które robią jej całą drogę:
przychodzi za każdym razem na zimno,
[nie widzi innych sesji](../CLAUDE.md#splitting-work-across-sessions)
i dostaje klon,
[który kłamie o historii](../CLAUDE.md#git-in-remote-sessions-history-is-truncated-or-stale).

**Psuje ją** konwencja, która istnieje tylko w komunikacie commita
albo w pamięci innej sesji,
podział pracy zrobiony po plikach zamiast po rozstrzyganych decyzjach,
bo dwie sesje dochodzą wtedy do tego samego wniosku dwa razy
i żaden merge tego nie zgłasza,
oraz wpis z [TODO.md](../TODO.md) wykonany tak, jak stoi,
bo nie ma kogo zapytać, czy nazwany w nim ruch jest czymś więcej niż zgadnięciem.

**Obsadzają ją** sesje agenta, które mają w gicie własne commity,
i cały [CLAUDE.md](../CLAUDE.md) jest pisany pod tę rolę.

## Czego na tej liście nie ma

Recenzent nie jest rolą, jest fazą,
którą kończy każda postawa cokolwiek pisząca,
i opisuje ją [przegląd zmian](../CLAUDE.md#the-review-pass).
Nie ma autora reguły, bo wyszedł razem z torem lintera,
a kto chciałby tę rolę obsadzić na nowo,
zaczyna od tego, [co ją zamknęło](linter.md#what-closed-the-track),
a nie od formatu, w którym reguła kiedyś stała.
Nie ma też roli osoby dokładającej się z zewnątrz,
i dlatego nie ma osobnego przewodnika dla współpracowników:
CLAUDE.md jest jedyną kopią konwencji,
a rozdzielenie jej na wersję dla autora i wersję dla gości
kosztowałoby dwie kopie tych samych reguł, żeby obsłużyć nikogo.
