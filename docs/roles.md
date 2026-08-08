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
Kto pisze regułę, jest tym, w kogo ta reguła potem strzela;
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
i nazwa użyta przed wprowadzeniem, tier albo abstencja na pierwszej stronie.
Obie rzeczy są niewidoczne dla autora, bo autor wie, co jest niżej,
i dlatego [przegląd zmian](../CLAUDE.md#the-review-pass) każe czytać od miejsca edycji
tak, jakby dalszej części nie było.

**Obsady** ta rola nie ma.
Jedyny dowód, że ta droga działa,
to autor czytający README po dłuższej przerwie.

## Ktoś, kto to uruchamia

Pyta, jak odpalić i co znaczy komunikat, który dostał.
Wchodzi przez bloki polecenia w [README](../README.md#co-działa),
a dalej instrukcją jest samo narzędzie:
`--help` mówi, co przyjmuje, `--list-rules` co się uruchomi,
`--explain` dokłada uzasadnienie każdej reguły.
Osobnego podręcznika nie ma,
a dokument powtarzający zachowanie reguły cicho się z nią rozjeżdża,
bo [kod jest właścicielem tego, co zaimplementowane](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely).
Do dokumentów ta rola wchodzi po jedną rzecz, której z wyjścia nie widać:
[czym różni się abstencja od braku trafień](rules.md#abstention-is-not-silence).

**Psuje ją** komunikat, który nie mówi, która reguła go wypisała,
oraz próg podany bez informacji, że jest nieskalibrowany.

**Obsadza ją** autor, z klona repozytorium.
Instalacji poza klonem nie ma,
a którą drogą narzędzie miałoby trafiać do kogoś innego,
rozstrzyga [milestone 4](roadmap.md#milestone-4-the-delivery-decision).

## Planista

Pyta, co jest na horyzoncie i co jest następne.
Wchodzi w [roadmap.md](roadmap.md), gdzie każdy milestone ma kryterium wyjścia,
a numeracja jest kolejnością i jest nośna.
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

## Autor reguły

Pyta, jak dopisać regułę i ile wolno jej wiedzieć.
Wchodzi w [rules.md](rules.md), stamtąd w [rodzaje checków](rules.md#check-kinds),
a przykładem roboczym jest pakiet typograficzny w `olski/packs/typography.py`
z testami w `tests/test_checks.py`.
Dwa wymagania idą z tą rolą od początku:
[ile analizy regule wolno zażądać](linter.md#how-deep-does-each-rule-have-to-see)
oraz [to, że bez kalibracji próg jest opinią z przecinkiem](linter.md#the-thing-that-makes-or-breaks-it-calibration).
Inwentarz kandydatów w [rule-inventory.md](rule-inventory.md)
jest listą, z której ta rola bierze następną regułę,
a [fiction.md](fiction.md) i [generated-polish.md](generated-polish.md)
tłumaczą, skąd część tych pozycji się tam wzięła.

**Psuje ją** rodzaj checka, o którym dokument milczy,
bo wtedy trzeba go przeczytać z silnika,
i dokument powtarzający parametry checka,
bo wtedy istnieją dwie wersje i nie widać, która obowiązuje.

**Obsadzają ją** autor i sesje agenta,
a pakiet typograficzny jest tym, co ta rola zdążyła zrobić.

## Ktoś, kto mierzy

Pyta, która liczba się ruszyła i co trzeba przeliczyć.
Wchodzi w [sekcję Checks](../CLAUDE.md#checks),
bo to ona wymienia dokumenty z liczbami, do których nie dosięga żaden test,
a dalej idzie do tego z nich, który jest właścicielem danej liczby.
Każdy z nich wypisuje polecenia, które jego tabele produkują,
i po to te polecenia tam są.

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

## Ktoś, kto zestawia to z tym, co już istnieje

Pyta, czy to samo nie zostało już zrobione i czy nie zostało zrobione lepiej.
Wchodzi w [prose-linters.md](prose-linters.md) po silniki,
które angielski i japoński już mają,
w [similar-work.md](similar-work.md) po sto języków kontrolowanych
i po to, które z ich obietnic ktoś zmierzył,
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
Nie ma też roli osoby dokładającej się z zewnątrz,
i dlatego nie ma osobnego przewodnika dla współpracowników:
CLAUDE.md jest jedyną kopią konwencji,
a rozdzielenie jej na wersję dla autora i wersję dla gości
kosztowałoby dwie kopie tych samych reguł, żeby obsłużyć nikogo.
