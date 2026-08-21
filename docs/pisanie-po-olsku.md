# Pisanie po olsku: feedback z jednej sesji

Dokument zbiera to, co widać z fotela, którego dotąd nikt nie zajmował:
kogoś, kto pisze *pod* tę gramatykę zdanie po zdaniu,
zamiast mierzyć ją nad tekstem już napisanym.
Materiał jest z jednej sesji, tej, która przepisała
[README](../README.md#konwencje) na zdania, które olski wyprowadza.
Przeszło w niej przez `olski.check` blisko czterysta kandydatów na zdanie,
z czego trzecia część wyszła odrzucona,
a trzecia część jednoznaczna.

Planem to nie jest.
Właścicielem ruchu jest [`TODO.md`](../TODO.md),
kolejności [`roadmap.md`](roadmap.md),
a ceny wpuszczenia konstrukcji
[`subset.md`](subset.md#what-the-grammar-covers);
tu stoi tylko materiał, którego te trzy dokumenty nie miały skąd wziąć.

## Główny problem tej sesji: odrzucenie nie mówiło, gdzie stanęło

Na każde dziesięć odrzuceń dziewięć mówiło wtedy tyle,
że nic w olskim tego zdania nie wyprowadza.
Reszta nazwała formę — `no production takes „GLR”` — i ta reszta była łatwa,
bo naprawa jest widoczna od razu.
Cała trudność siedziała w tej asymetrii, a nie w liczbie konstrukcji:
przy wieloznaczności werdykt mówił, co go rozdwoiło,
a przy odrzuceniu nie mówił nic.

Metodą, która wtedy została, była bisekcja ręką.
Zdanie o pięciu członach dzieli się na pół, każdą połowę puszcza osobno,
potem wymienia się w podejrzanym członie jedno słowo i puszcza znowu.
Na jedno odrzucone zdanie wychodziło tak kilka do kilkunastu przebiegów,
a wiedza, która z tego zostaje, jest wiedzą o tym jednym zdaniu.

Werdykt nazywa miejsce, na którym analiza stanęła,
i nazywa je dwoma zdaniami, bo zatrzymanie na formie
i zdanie, którego nic nie domyka, są dwoma zdarzeniami
([`subset.md`](subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka)).
Odpowiada tym na pierwsze pytanie tamtej bisekcji, czyli który człon tknąć.
Reszty bisekcji nie zdejmuje: miejsce zatrzymania jest końcem przedrostka,
który się analizuje, a nie wskazaniem usterki,
więc para niezgodna rodzajem wychodzi dalej, niż stoi.
[`roles.md`](roles.md#ktoś-kto-to-uruchamia) nazywa odrzucenie bez tej odpowiedzi
jako to, co psuje drogę komuś, kto narzędzie uruchamia.

## Czego brakowało najbardziej

Lista jest ułożona według tego, ile razy zawróciła zdanie,
a nie według tego, ile by kosztowało wpuszczenie.
Przy każdej pozycji stoi para zdań, z których pierwsze pada, a drugie przechodzi,
bo różnica między nimi jest tu całą informacją.
Większość tych pozycji nie ma wiersza w
[liście braków](subset.md#what-it-does-not-cover-yet),
a przy tych, które mają, stoi to powiedziane.

**Zaimek dzierżawczy przy rzeczowniku.**
`Jego skutki są znane.` pada, `Skutki tego wyboru są znane.` przechodzi.
Przyczyna najczęstsza z wszystkich i najbardziej myląca,
bo `jego`, `jej` i `ich` nie wyglądają na konstrukcję:
wygląda to tak, jakby padło całe zdanie, a nie jedno słowo w nim.
Objazdem jest powtórzenie rzeczownika, czyli dokładnie to,
czego proza unika zaimkiem.

**Przecinek przed `i` zamykający zdanie podrzędne.**
`Dokument mówi, co gramatyka wpuszcza, i liczy cenę.` pada,
`Dokument mówi, co gramatyka wpuszcza i liczy cenę.` przechodzi,
a z `a` w miejsce `i` przechodzi także z przecinkiem.
Zderzają się tu dwie rzeczy, z których żadna nie jest o koordynacji:
przecinek domyka zdanie podrzędne pierwszego członu,
a gramatyka czyta go jako przecinek koordynacyjny,
którego `i` przed sobą nie bierze
([subset.md](subset.md#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego)).
Wyszło to na liście dokumentów w README, gdzie pozycja mówi o dokumencie dwie rzeczy,
i przez to każda pozycja tej listy jest napisana inaczej, niż była.

**Celownik.**
`Parser mówi autorowi o czytaniach.` pada, `Parser pokazuje oba czytania.` przechodzi.
Zdanie, które README stawia najwyżej — parser mówi *autorowi*, że coś jest dwojakie —
nie da się w olskim powiedzieć wcale,
więc stoi tam dziś bez adresata.
[Walencja poza biernikiem](subset.md#what-it-does-not-cover-yet) obejmuje to jako żądanie,
a nie jako pozycję, i z tego fotela jest to najdroższy pojedynczy brak.

**Wysunięte dopełnienie przy podmiocie opuszczonym.**
`Cenę liczymy.` pada, `Cenę liczy autor.` przechodzi,
a `Liczymy cenę.` przechodzi też.
Pierwsza osoba mnoga jest więc cała,
a brakuje szyku, w którym dopełnienie stoi na czele zdania bez podmiotu —
tego samego, którym ten rejestr mówi o konwencjach: *cenę liczymy przed dopisaniem*.

**Grupa imienna z elipsą głowy.**
`Wszystkie obsadza jedna osoba.` pada, `Wszystkie role obsadza jedna osoba.` przechodzi.
Tak samo padają `ani jedna`, `dwa z tych czytań` i każde inne miejsce,
w którym przymiotnik albo liczebnik stoi za rzeczownik,
którego zdanie przed chwilą użyło.

**Orzecznik na czele z okolicznikiem w środku.**
`Wzorem jest tu kompilator.` pada,
a `Tu wzorem jest kompilator.` i `Kompilator jest tu wzorem.` przechodzą.
Sam szyk jest wpuszczony,
więc pada nie konstrukcja, tylko jedno słowo wstawione między kopułę a podmiot.
Ta klasa myliła najbardziej, bo łamie oczekiwanie,
że gramatyka rozstrzyga o konstrukcjach, a nie o pozycji `tu` i `więc`.

**Liczebnik w orzeczniku.**
`Tory są dwa.` pada, `Torów jest dwa.` też,
a `Działają dwie rzeczy.` przechodzi.
Grupa liczebnikowa jest wpuszczona jako podmiot i jako dopełnienie,
a zdanie, które mówi, ile czegoś jest, dalej nie wychodzi.

**Apozycja z nazwą.**
`Bank drzew Składnica mierzy gramatykę.` pada,
`Składnica jest bankiem drzew.` przechodzi.
Rejestr techniczny nazywa tak każdy artefakt zewnętrzny —
korpus Składnica, słownik Morfeusz, wydanie takie a takie —
a olski żąda na to osobnego zdania.
[Dopowiedzenie z `czyli`](subset.md#what-it-does-not-cover-yet) jest tym samym brakiem
w drugiej postaci.

**Człon bez czasownika po `a nie`.**
`Zgodność jest parsowaniem, a nie sprawdzeniem po nim.` pada,
`Zgodność jest parsowaniem.` przechodzi.
Brak stoi na liście i jest tam wyceniony jako jedna konstrukcja,
a w tym rejestrze jest chwytem na co drugie zdanie,
bo tak właśnie dokumentuje się podzbiór: przez to, czego w nim nie ma.
Elipsa czasownika w drugim członie — `a drugie podmiot opuszczony` — pada tak samo.

**Imiesłów przymiotnikowy.**
`zaprojektowanego podzbioru`, `wygenerowanej polszczyzny`, `nierozstrzygnięty wybór`.
Stoi na liście, a warto do niej dopisać częstość:
w prozie o narzędziach imiesłów przy rzeczowniku jest zwykłym przymiotnikiem,
więc zawracał zdanie kilka razy nawet w tej próbce,
pisanej już z wiedzą, że go nie ma.

**Cząstka wewnątrz grupy imiennej.**
`Istnieją tylko te konstrukcje, które stoją na liście.` pada,
`Istnieją te konstrukcje, które stoją na liście.` przechodzi.
Cząstka ma pozycję przy zdaniu i przy czasowniku
([subset.md](subset.md#cząstka-stoi-tam-gdzie-przysłówek-a-listę-lematów-zamyka-warunek-na-czytanie)),
a `tylko` w tym rejestrze określa najczęściej grupę imienną.

**Czasownik rządzący dopełniaczem.**
`Ten kierunek nie potrzebuje gramatyki.` pada, `Gramatyki skład nie czyta.` przechodzi.
To jest walencja poza biernikiem widziana od strony pisania:
`potrzebować`, `żądać` i `brakować` są w tym rejestrze codzienne.

**Notacja z jednoliterowym członem.**
`docs/pisanie-po-olsku.md jest raportem.` przechodzi,
a `docs/pisanie-w-olskim.md jest raportem.` pada na `-`.
Notację tego rejestru olski bierze jako jeden rzeczownik nieodmienny
([subset.md](subset.md#notacja-tego-rejestru-jest-słowem-którego-słownik-nie-ma)),
a wzorzec pod tym nie przyjmuje członu z jednej litery,
więc nazwy pliku z `w` albo `i` w środku nie da się w olskim wymówić.
Ten dokument nazywa się tak, jak się nazywa, właśnie dlatego.

## Co działało

`--readings` ze streszczeniem było wtedy jedynym miejscem,
w którym werdykt mówił „dlaczego”,
i działało dokładnie tak, jak README obiecuje:
strzałka `„z dodatkami” → „przewyższa”, „koszt”` mówi, co wybrać ma czytelnik,
a nazwy roli mówią, co zdanie znaczy w każdym z czytań.
Diagnoza wieloznaczności zajmuje jedno spojrzenie.

Przebieg nad całym plikiem trwa poniżej sekundy,
więc pętla „popraw i sprawdź” nie ma tarcia,
i to jest ta taniość, o której README mówi na wstępie.
Nad jednym zdaniem `-c` odpowiada, zanim zdąży się przełączyć okno.

Odrzucenie z nazwaną formą naprawia się bez myślenia.
Wieloznaczność przestaje być przy tym po dwudziestu zdaniach sygnałem:
prawie każda bierze się z przyłączenia albo ze synkretyzmu,
o czym projekt rozstrzygnął
([subset.md](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera)),
więc `ambiguous` czyta się jak brak werdyktu.
Nagroda `valid` bywa zaś nie za składnię, a za dobór słów:
to samo zdanie z dopełnieniem żeńskim wychodzi jednoznaczne,
a z rzeczownikiem rodzaju m3 nie.

## Cena, którą to zostawia w prozie

Pisanie pod olskiego popycha w cztery chwyty:
zdanie krótkie, kopułę z narzędnikiem, wyrażenie przyimkowe na czele zdania
i dopełnienie w rodzaju żeńskim.
Trzy pierwsze widać w README po przepisaniu,
a [reguły prozy](../CLAUDE.md#dla-kogo-jest-napisane-zdanie) każą unikać
jednego rytmu na wszystko.
Gramatyka nagradza więc rejestr, który reguły prozy karzą,
i jest to napięcie do rozstrzygnięcia gdzie indziej niż tutaj.

## Czego ten dokument nie mówi

Sesja jest jedna, rejestr jeden, a pisała ją sesja agenta,
nie człowiek redagujący własny plik,
więc jest to raport, a nie pomiar.
Liczby stąd są liczbami tej sesji i trzyma je git,
a nie przebieg, który da się powtórzyć:
zdania kandydujące stały w katalogu tymczasowym i nie weszły do repozytorium.
Powtórzyć da się każdą parę zdań wyżej, przez `olski.check -c`,
i po to każda z nich stoi w tym dokumencie cała.
