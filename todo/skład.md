# Skład i opowieści

`README.py` powstał drzewami przed tekstem, czyli odwrotnie, niż deklaruje
`opowieści/__init__.py`, więc mierzy, co skład powiedzieć umie, a nie co trzeba.
Ruchem jest napisać najpierw polski tekst oddający wstęp `README.md`,
potem drzewa pod niego, a różnicę między jednym a drugim przeczytać,
bo dopiero ona mówi, czego tym kategoriom brakuje.
Wtedy ten napis dostaje właściciela i wchodzi do testu tak,
jak `BAZYLISZEK` stoi w `tests/test_opowieść.py`;
dziś nie trzyma go nic i `README.py` mówi w nagłówku, dlaczego.
Kryterium wyjścia toru składu to i tak nie jest
([`docs/roadmap.md`](../docs/roadmap.md#kryterium-wyjścia-toru-składu-to-znów-readme)),
bo tamto żąda znak w znak nad `README.md`, a nie treści oddanej innymi zdaniami.

Trzy pozycje, których skład nie ma, stoją każda w innym miejscu;
dwie pierwsze widać w `README.py`.
Lematu `olski` Morfeusz nie zna wcale, więc nazwa własna tego języka
nie stanie w składanym zdaniu w żadnej roli:
`olski/skład/leksemy.py` wybiera między leksemami, które SGJP ma,
i sam mówi, że leksem nieznany nie ma ani jednej formy.
Odmianę tego słowa deklaruje `olski.toml`, a skład go nie czyta,
i tym zajmuje się wpis o leksykonie projektu czytanym przez oba kierunki,
a nie ta pozycja.
Liczebnika nie ma `olski/skład/składnia.py`, więc `jedno odczytanie` z drzewa nie wyjdzie,
i jest to ta sama konstrukcja, którą gramatyka po drugiej stronie już ma
([`docs/konstrukcje-gramatyczne/grupa-imienna.md`](../docs/konstrukcje-gramatyczne/grupa-imienna.md#grupa-liczebnikowa-zgadza-się-tym-czego-nie-ma-w-środku)),
czyli tor składu jest tu za nią, a nie przed.
Relacja `przyczyna` nie ma w `olski/skład/przyimki.py` wpisu pod żadnym przyimkiem,
a ma wpis w `olski/skład/spójniki.py`, więc wychodzi zdaniem i nie wychodzi frazą:
`Dlaczego.bo(zdarzenie)` składa się, a `Dlaczego.dla(rzecz)` zgłasza `PozaRamą`.
Jest to jedyna z tych trzech pozycji, przy której skład ma pół konstrukcji, a nie zero.
Do przeczytania przy niej jest ten leksykon obok
`tests/test_przyimki.py`, który świadkuje przypadkom, a nie doborowi relacji.

Komunikat werdyktu jest napisem wpisanym w kod, a repozytorium ma tor,
który polskie zdanie składa z drzewa,
więc werdykt mógłby być pierwszym konsumentem tego toru:
formę po liczebniku liczyłaby wtedy morfologia,
a nie tabela na trzy przedziały w `_odczytań` w `olski/werdykt.py`.
Wpis stoi zaparkowany za wpisem o pozycjach, których skład nie ma,
bo liczebnik jest jedną z nich,
a bez liczebnika nie wyjdzie z drzewa ani jeden wiersz tego werdyktu.
Liczebnik nie jest przy tym wszystkim, czego temu komunikatowi brakuje.
Wiersz werdyktu cytuje formę wziętą ze sprawdzanego zdania,
a drzewo składu nie ma pozycji na napis, którego się nie odmienia.
Skład zgłasza przy tym `BrakFormy` oraz `PozaRamą` nad drzewem,
którego nie umie zrealizować, a werdykt wypisuje się nad każdym zdaniem,
więc komunikat z drzewa dokłada gałąź na wypadek, którego napis nie ma.
Do przeczytania jest `explain` w `olski/werdykt.py`,
bo część jego wierszy jest polskim zdaniem, a część listą par i liczbą,
czyli rozstrzygnąć trzeba i to, ile z tego wydruku skład bierze.

Słowo, którego SGJP nie ma, mówi gramatyka i nie mówi go skład.
`olski.toml` deklaruje leksem, wedle którego takie słowo się odmienia
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)),
a `olski/skład/morfologia.py` pyta o formy sam Morfeusz i tego pliku nie czyta,
więc `README.py` dalej nie wypuści zdania o olskim.
Ruchem jest `odmień` pytające o ten leksykon tam, gdzie słownik milczy,
bo `odmiana` w `olski/projekt.py` wydaje dokładnie to, co `paradygmat`
w tamtym pliku: formę wraz z cechami i leksemem.
Do przeczytania są przy tym dwa odsiewy, których leksykon projektu nie ma:
`POZA_REJESTREM` w `olski/rejestr.py` odsiewa kwalifikatorem,
a wpis kwalifikatorów nie niesie,
choć wzorzec bywa nimi oznaczony,
i `WieleLeksemów`, bo wiersz wskazuje leksem wprost, czyli odpowiada już na to pytanie.
Rozstrzygnąć trzeba przy tym, czy skład bierze stąd same formy,
czy pyta jeszcze wzorzec o kwalifikatory, których wpis nie niesie.

Skład nie ma czym powiedzieć, co jest tematem wewnątrz grupy imiennej,
więc `Jaki` w `olski/skład/składnia.py` zawsze stawia przymiotnik przed rzeczownikiem,
choć polszczyzna ma oba szyki i różnią się one tym, co niosą:
przymiotnik po rzeczowniku nazywa, a przed nim określa.
Widać to bez żadnego pomiaru, na jednej frazie:
README pisze `kontrolowanych języków naturalnych`,
a to samo drzewo wypuszcza `kontrolowany naturalny język`.
Po drugiej stronie stoi to jako czytanie, które z
[obiegu](../docs/sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma)
nie wraca żadnym drzewem, i trzyma to `tests/test_rozbiór.py`.
Do przeczytania jest ta para wraz z tym,
co [`docs/sklad.md`](../docs/sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
mówi o tym, czego drzewo nie niesie.
Ruchem jest ta sama kategoria, którą zdanie już ma, wpuszczona do grupy imiennej:
`Wyróżnienie` stoi w `olski/skład/składnia.py` i przestawia konstytuenty zdania,
a wewnątrz grupy nie sięga niczego, bo `Cechy` w `olski/skład/słownik.py`
zwija przymiotniki, zanim spotkają rzeczownik.
Rozstrzygnięcia żąda przy tym co innego niż w zdaniu:
tam wyróżnienie przestawia to, co i tak stało osobno,
a tu przymiotnik postawiony po rzeczowniku zmienia znaczenie całej grupy,
więc nazwa `temat` na to nie przystaje.

Opowieść stawia jeden czas we wszystkich swoich orzeczeniach,
a polszczyzna liczy czas zdania podrzędnego wobec zdania nad nim,
więc `Wiedział, że pod ścianą stały postaci.` wychodzi tam,
gdzie polszczyzna napisałaby `stoją`.
Oba te zdania są polskie i mówią co innego,
czyli brakuje tu kategorii dziedziny, a nie formy do policzenia:
pyta ona o to, czy rzecz z dołu trwała wtedy, czy skończyła się przedtem.
Widać to dopiero od [treści](../docs/sklad.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi),
bo okoliczność wyrażona zdarzeniem stoi obok zdarzenia nadrzędnego w czasie,
a treść stoi pod nim, i tam czas przestaje być własnością samego opowiadania.
Do przeczytania jest `CZASY` oraz `Kontekst` w `olski/skład/składnia.py`
wraz z tym, co [`docs/sklad.md`](../docs/sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)
mówi o czasie jako własności tekstu,
bo ta kategoria tego zdania nie odwołuje, tylko dokłada do niego drugie:
czas opowiadania zostaje, a zdanie podrzędne dostaje go względem swojego zdania.
Ruchem jest ta kategoria przy `Treść`,
wraz z rozstrzygnięciem, czy jest ona tym samym co aspekt, czy czym innym,
bo `stoją` i `stały` różnią się tu czasem, a nie dokonaniem.
Do zmierzenia jest, ile zdań tej legendy wyszłoby wtedy inaczej,
a jest ich dziś dwa i oba stoją pod `Treść`.

Anafora sięga podmiotu i nic poza nim,
a opowieść o bazyliszku pokazuje, gdzie to boli:
`opowieści/bazyliszek.py` pisze `wzrok potwora` dwa razy,
a polszczyzna napisałaby drugi raz `jego wzrok`.
Tak samo dopełnienie: po `Bazyliszek zobaczył własne odbicie.`
legenda pisze `zamienił bazyliszka w kamień`,
a polszczyzna napisałaby `zamienił go`.
Ruchem jest zaimek osobowy w miejscu roli innej niż podmiot,
liczony z tego samego `Kontekst`.
Do przeczytania jest to, co o tej pozycji mówi
[pole generowania](../docs/similar-work.md#generowanie-rozdziela-się-poziomem-wejścia),
bo ruch ten ma tam nazwę wraz z literaturą,
a warunek, który dziedziczy, jest testem na zbiór dystraktorów,
czyli tym, co tamten algorytm liczy nad opisem rzeczy.
Do przeczytania jest też `pomijalny` w `olski/skład/składnia.py`,
który trzyma warunki [wąskiego opuszczania podmiotu](../docs/sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie),
bo zaimek dziedziczy stamtąd warunek, a nie tylko mechanizm,
wraz z [ceną tego ruchu](../docs/sklad.md#lepszy-tekst-żąda-czego-innego-niż-dłuższy),
która trzyma cztery rzeczy czyniące go innym, niż wygląda:
ostrzejszy warunek na zaimek, szyk łączący go w jedną zmianę z
[dopełnieniem wyrażonym zdarzeniem](../docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
osobne miejsce zaimka dzierżawczego,
oraz podmiot zdania podrzędnego, który zaimka nie bierze wcale i stoi niżej.
Do zmierzenia jest, czy pozycja zwalnia się w tej legendzie gdziekolwiek,
a do rozstrzygnięcia, czy `swój` i `jego` są jedną kategorią, czy dwiema,
bo pierwszy odsyła do podmiotu zdania, a drugi poza nie.

Osobno stoi podmiot zdania podrzędnego, bo polszczyzna nie pisze tam zaimka,
tylko go opuszcza, a `Kontekst.podrzędne` opuszczenie w dół nie przekazuje.
Odbiera to legendzie zdanie, którego ona chce:
`Czeladnik znał córkę krawca. Nie wiedział, że stała pod ścianą.`
mówi, że on nie wiedział o niej, a nie o sobie, i mówi to samą formą,
a wersja z wypisanym podmiotem powtarza `córkę krawca` w zdaniu obok.
Pozycja jest tam wolna wedle warunku, który już stoi:
`wiedzieć` rozdziela czeladnika od córki rodzajem, i `stać` rozdziela ich tak samo,
więc oba opuszczenia mierzy dziś `pomijalny` i oba przechodzą.
Brakuje zasięgu: dziś antecedensem jest podmiot zdania poprzedniego,
a tu jest nim jego dopełnienie.
Do rozstrzygnięcia jest, czy zasięg obejmuje też okoliczność wyrażoną zdarzeniem,
i stoi za tym argument, którego treść nie ma:
zdanie z `gdy` wysunięte na czoło stoi przed swoim antecedensem,
więc opuszczenie w nim odsyłałoby wstecz do niczego,
a treść stoi za zdaniem nadrzędnym zawsze.
Do przeczytania jest `Kontekst.podrzędne` wraz z powodem,
dla którego każde pole gaśnie tam osobno,
bo ten ruch jednemu z nich ten powód odbiera.
Ruchem jest antecedens liczony z uczestników zdania poprzedniego i nadrzędnego,
a nie z samych ich podmiotów, wraz z testem na parę zdań,
w której rodzaj tych dwóch ról jest wspólny, bo tam opuszczenie ma się nie stać.

Rama, o którą pyta `Robi` w `olski/skład/składnia.py`, wylicza pozycje,
których żąda sam czasownik, i nie ma wśród nich wyrażenia przyimkowego,
więc `Córka krawca nie wierzyła w bazyliszka.` z drzewa nie wyjdzie.
Klasa ta jest gorsza niż brak, bo `Dokąd.w` wypuści to zdanie jako cel,
czyli powie, że ktoś w coś wierzy tak, jak mówi się, że ktoś dokądś idzie.
Czwarta wersja legendy obeszła to zdanie z drugiej strony,
bo `nie wierzyła, że w piwnicy mieszkał bazyliszek` bierze
[treść](../docs/sklad.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi)
zamiast wyrażenia przyimkowego, a mówi to samo o postaci;
klasa zostaje jednak w tej samej cenie, bo wiara w rzecz zdaniem podrzędnym nie wyjdzie.
Drugą klasę dokłada losowanie: `czekał na izbach` wychodzi z drzewa,
w którym `na izbach` jest okolicznością miejsca,
a czyta się przez `czekać na kogoś`, czyli przez ramę, której tu nie ma,
więc `olski/skład/makieta.py` ten czasownik pomija, zamiast wypuszczać takie zdania.
Kolumnę przyimków leksykon niesie i czyta ją dziś świadek ramowy
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)),
więc zostaje strona składu i to ona jest tym wpisem.
Do przeczytania jest `rama` w `olski/walencja.py`, bo pozycja przyimkowa
jest pierwszą, której nie da się nazwać jednym napisem morfologii:
przyimek i przypadek są tu dwiema rzeczami naraz.
Ruchem jest ta pozycja w tym zbiorze wraz z kategorią, która ją wypełnia,
i rozstrzygnięciem, czym ta kategoria różni się od `Okolicznik`,
bo autor pisze dziś jedno i drugie tym samym `Dokąd.w`.

`chcieć` ma u Walentego i dopełniacz, i przypadek strukturalny,
więc `PRZYPADKI_DOPEŁNIENIA` w `olski/skład/składnia.py` daje mu biernik
i wychodzi z tego `Kot chce mysz.`,
czyli zdanie, którego polszczyzna woli nie mówić, a nikt tego nie zgłasza.
Pierwszeństwo biernika jest w tej krotce wyborem na przeszło trzysta lematów
i dla większości z nich jest wyborem dobrym:
`brać` i `dawać` mają u Walentego oba przypadki, a `brać chleba` mówi co innego
niż `brać chleb`, więc odmowa w tym miejscu kosztowałaby te zdania.
Do zmierzenia jest, ile z tych lematów woli dopełniacz i po czym je poznać,
bo bez tej liczby nie widać, czy jest to wybór złej ramy, czy wyjątek.
Ruchem jest kryterium wybierające przypadek albo zgłoszenie żądające go od autora;
drugie z nich żąda przy tym zapisu na przypadek, którego to drzewo nie ma nigdzie,
więc tańsze jest tylko z pozoru.

Treść bierze jeden spójnik i przez to jedną z dwóch rzeczy, które ta pozycja mówi.
`że` orzeka, że tak jest, a `żeby` — że tak ma być,
więc `Czeladnik chciał, żeby córka krawca wróciła.` z tego drzewa nie wyjdzie,
choć jest to zdanie, którym polszczyzna mówi o cudzym zdarzeniu pod czyjąś wolą.
Stoi to obok odmowy, którą `Robi` wydaje bezokolicznikowi o cudzym wykonawcy,
i te dwie rzeczy są jedną dziurą widzianą z dwóch stron:
[`docs/sklad.md`](../docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie)
nazywa tamto zdanie polskim, którego bezokolicznik nie wyraża,
a wyraża je dokładnie ta pozycja i ten drugi spójnik.
Do przeczytania jest `cp(żeby)` obok `cp(że)` u Walentego,
bo słownik te dwa kształty rozdziela i mówi, który lemat bierze który,
oraz `Treść` w `olski/skład/składnia.py`, gdzie spójnik stoi stałą.
Ruchem jest kategoria dziedziny na to, czy treść jest orzekana, czy żądana,
wraz z osobnym zdaniem leksykonu o `cp(żeby)`; wpis jest przez to winien
przebieg `harness/walenty.py` oraz poprawkę liczb w
[`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on).

`Przysłówek` w `olski/skład/składnia.py` żąda od słownika formy przysłówkowej,
a część okoliczności polszczyzna wyraża partykułą:
`znowu` ma w SGJP sam `part`, więc `D.znowu` zgłasza `BrakFormy`.
To zdanie legenda o bazyliszku chciała postawić w zakończeniu,
gdzie miasto zabija wejście drugi raz, i postawiła je bez tego słowa.
Do przeczytania jest wyjście `paradygmat` dla `znowu`, `tam` i `wkrótce`,
bo `tam` niesie oba znakowania naraz i pokazuje,
że granica między nimi nie idzie po tym, czym słowo jest w zdaniu.
Ruchem jest rozstrzygnięcie, czy okoliczność wyrażona jednym słowem
jest jedną kategorią dziedziny niezależnie od tego, czym słownik to słowo znakuje,
bo jeśli jest, to `Przysłówek` pyta o część mowy tam,
gdzie od części mowy nie zależy ani szyk, ani zgodność, ani forma.

`przejrzyj` w `olski/skład/przegląd.py` zgłasza jedną klasę z dwóch,
bo przyłączenia zawęzić nie ma dziś czym.
Okolicznik dochodzi w drzewie do zdarzenia zawsze,
więc każde wyrażenie przyimkowe stojące za grupą imienną byłoby trafieniem,
a raport zgłaszający każde zdanie z przyimkiem nie oddziela niczego od niczego:
nad `opowieści/bazyliszek.py` trafiłby w trzynaście z dwudziestu jeden zdań,
bo tyle z nich niesie wyrażenie przyimkowe,
i żadne z tych zgłoszeń nie mówiłoby autorowi, co miałby z nim zrobić.
Do przeczytania jest, czym się różnią te miejsca,
oraz to, co [`docs/subset.md`](../docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia)
mierzy nad Składnicą, bo tam ta sama klasa jest policzona nad cudzymi drzewami.
Stoi nad tym wpisem pytanie
[`docs/open-questions.md`](../docs/open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma),
które pyta o to samo od strony parsera i mówi, że wyjścia nie ma w gramatyce.
Przegląd stoi wobec niego inaczej i to jest tu jedyna nadzieja:
on niczego nie odrzuca, więc pomyłka kosztuje tu wiersz raportu,
a nie zdanie, którego autor nie napisze.
Ruchem jest kryterium, które oddziela przyłączenie niosące różnicę znaczenia
od tego, przy którym oba czytania mówią to samo,
albo rozstrzygnięcie, że takiego kryterium nie ma
i że ta klasa do przeglądu nie wchodzi.

Stopnia nie ma w składzie żadnego, a jest on kategorią dziedziny.
`Jaki` w `olski/skład/składnia.py` żąda od przymiotnika stopnia równego na stałe,
`Przysłówek` obok żąda tego samego i mówi w docstringu,
że stopień wyższy „mówi co innego” i czeka na kategorię.
Bez niego nie da się powiedzieć `Koszt szynki jest wyższy niż koszt bułki.`,
czyli tego zdania, które mówi to samo co `Koszt szynki przewyższa koszt bułki.`
i mówi to bez kolizji, którą `olski/skład/przegląd.py` w drugim zgłasza.
Do przeczytania jest, czy porównanie jest kategorią osobną od cechy,
bo `wyższy` jest formą przymiotnika, a `niż koszt bułki` jest drugim uczestnikiem,
więc drzewo ma tu do postawienia relację, a nie stopień przy rzeczy.
Ruchem jest ta kategoria wraz z linearyzacją stawiającą `niż`,
a nie przełącznik wybierający między dwoma zdaniami za autora:
przegląd zgłasza, żeby autor napisał drugie drzewo,
a nie żeby kompilator podmienił mu pierwsze.

`odmień` w `olski/skład/morfologia.py` bierze pierwszą z form jednego leksemu,
gdy żądaniu odpowiada ich kilka, i nie mówi o tym nigdzie.
Jest to jedyne miejsce, w którym kompilator wybiera w milczeniu,
i zostaje po dwóch kryteriach, na które ta klasa nie sięga:
kwalifikatora ta forma nie ma, a leksem ma ten sam, co forma obok niej.
Widać ją w dwóch postaciach, a przyczyna jest jedna, więc idą razem.
Pierwszą jest wariant w jednej komórce: `postaci` obok `postacie`
w mianowniku mnogim, i pierwszy z nich wypisuje `opowieści/bazyliszek.py`,
bo pierwszy z nich wydaje słownik.
Drugą jest rodzaj wypisany dwiema wartościami w jednym tagu,
z których `rodzaj_rzeczownika` w tym samym pliku bierze alfabetycznie pierwszą:
`anioł` dostaje stąd rodzaj osobowy, choć słownik nie rozstrzyga, czy jest osobowy,
a rodzaj jest tu wartością, z której liczy się zgodność całego zdania.
Do przeczytania jest to, co
[`docs/sklad.md`](../docs/sklad.md#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)
mówi o kryterium, które zostało zbudowane obok tej klasy,
bo pytanie jest tu tym samym pytaniem o jedno piętro niżej:
wybór między leksemami zapada w nazwie, a ten zapada pod jednym leksemem.
Ruchem jest rozstrzygnięcie, czym ten wybór ma być, i kandydatów jest dwóch.
Zgłoszenie jak `WieleLeksemów` żąda od autora wpisu przy każdym wariancie,
także tam, gdzie oba warianty znaczą to samo, czyli przy `oczami` obok `oczyma`.
Wpis wskazujący formę, jak `olski/skład/leksemy.py` wskazuje leksem,
kosztuje wpis tylko tam, gdzie ktoś na wariant trafi,
a milczy dokładnie tak jak dziś, dopóki nikt go nie napisze.
Rozstrzyga między nimi to, ile takich wariantów rejestr naprawdę spotyka,
i tego nikt nie policzył.

`olski/skład/przyimki.py` zna przyimek w jednej postaci,
więc `we Wrocławiu`, `ze wsi` i `pode mną` z drzewa nie wyjdą,
a wyjdzie z niego `w Wrocławiu`, którego polszczyzna nie ma.
Danych do tego nie brakuje: Morfeusz znakuje obie postaci cechą `vocalicity`,
a `olski/morph.py` tę cechę czyta, więc `we` stoi w słowniku obok `w`.
Brakuje warunku, kiedy postać zgłoskotwórcza jest tą właściwą,
a jest to warunek fonologiczny nad tym, co po przyimku stoi,
czyli jedyna rzecz w tym pakiecie, której nie da się wziąć z lematu ani z pozycji.
Do przeczytania jest wyjście `paradygmat` dla `w`, `z` i `pod`
wraz z tym, co `docs/prior-art.md` mówi o tym, czego ten słownik nie niesie.
Ruchem jest ten warunek zapisany raz, w linearyzacji okolicznika,
wraz z rozstrzygnięciem, czy wpis leksykonu wymienia obie postaci,
czy jedną, a drugą liczy się z niej.

Leksem dokładany do napisu, który słownik zna, stoi poza `olski.toml`
i jest drugą połową klasy, którą ten plik obsługuje; czym się te dwie różnią,
trzyma [`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma).
Wiersz na taki leksem — na `agent`, żeby projekt pisał o agentach `agenty` —
dokłada czytanie formie, którą słownik już czyta,
więc łamie własność, na której stoi zerowa cena tej warstwy,
a cena takiego wiersza jest przez to ceną zwykłą,
mierzoną w czytaniach zdań przyjętych.
Ruchem jest ten pomiar, a nie wiersz dopisany bez niego,
i tym różni się ta połowa od tamtej: tam cena wychodziła z własności,
a tu wychodzi z przebiegu.
Do przeczytania jest `test_żadnej_formy_leksykonu_słownik_nie_zna`
w `tests/test_projekt.py`, bo wiersz na `agent` wywraca właśnie ten test,
i rozstrzygnąć trzeba, czy test ten zostaje z wyjątkiem wypisanym obok,
czy schodzi razem z własnością.

O bezokolicznik gramatyka nie pyta wcale, a skład pyta o niego leksykon,
i te dwa zdania nie zgadzają się co do `pomagać`.
`Linter pomaga pisać dobry kod.` stoi w komentarzu `olski/subset/zdanie.py`
jako przykład ciał produkcji `wypełnienia`, olski je wyprowadza,
a `Robi` w `olski/skład/składnia.py` odmawia mu ramy,
bo `olski/leksykon.txt` mówi o tym lemacie samo `nie_bierze_biernika`.
Widać to na obiegu i nigdzie więcej, bo osobno każdy z tych kierunków
ma tylko własne zdanie i nie ma go z czym porównać;
tym różni się ten wpis od tych, które nazywają brak po jednej stronie.
Wywód trzyma
[`docs/sklad.md`](../docs/sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma),
a odmowę jako powód sprawdza `tests/test_rozbiór.py`.
Do przeczytania jest, co `harness/walenty.py` bierze z Walentego przy pozycji `infp`,
bo pytanie jest o to, czy słownik tego lematu z bezokolicznikiem nie ma,
czy ma go w kształcie, którego ten przekład nie bierze,
wraz z tym, co [`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#zdania-leksykonu-pochodzą-z-walentego-i-mówią-mniej-niż-on)
mówi o granicach tego przekładu.
Ruchem jest jedno z dwóch, zależnie od tego, co słownik powie:
przekład biorący ten kształt, wraz z przebiegiem generatora
i poprawką liczb w tamtej sekcji,
albo zdanie przykładowe w tamtym komentarzu zamienione na takie,
które oba tory mają naraz.

Liczebnik ma produkcję w gramatyce, a w tym zapisie nie ma kategorii,
więc `Działają dwie rzeczy.` wraca powodem
`„dwie rzeczy” nie ma tu czym być w pozycji podmiotu`,
i tą samą drogą przepada każde zdanie z liczbą.
Do przeczytania jest `_nominalne` w `olski/skład/rozbiór.py`,
czyli lista ciał grupy imiennej, które ten kierunek mówi,
wraz z ceną liczebnika, którą trzyma commit, który go wpuścił,
bo tamta strona ma go zmierzonego od strony gramatyki.
Ruchem jest kategoria w `olski/skład/składnia.py`, a nie samo ciało w rozbiorze:
liczebnik rządzi liczbą i przypadkiem rzeczownika, którego dotyczy,
więc bez niej nie ma z czego wypisać tego, co ma wrócić.

Wybór między `w` i `na` jest faktem o rzeczowniku, a tego faktu nie ma tu nigdzie:
`olski/skład/przyimki.py` mówi, jakiego przypadka żąda przyimek w danej relacji,
i o tym, przed którym rzeczownikiem on stanie, nie mówi nic,
więc `w ulicy` oraz `na izbie` wychodzą z drzewa tak samo dobrze jak `na ulicy`.
Widać to dopiero od strony tekstu, którego nikt nie pisał zdanie po zdaniu:
autor pisze `na rynku`, nie zauważając, że wybrał,
a `olski/skład/makieta.py` wybrać musi i dlatego rozdziela `MIEJSCA_W` od `MIEJSCA_NA`,
czyli trzyma fakt o polszczyźnie w tabeli jednego programu.
Do przeczytania jest ta para tabel wraz z tym, co
[`docs/sklad.md`](../docs/sklad.md#tekst-losowany-żąda-tego-czego-autor-nie-musiał-napisać)
wylicza jako fakty poza leksykonami tego pakietu,
oraz `PRZYIMKI` w `olski/skład/przyimki.py`, bo pytanie jest o kolumnę, której ten plik nie ma.
Ruchem jest ta kolumna, czyli przyimek dopisany przy rzeczowniku, a nie przy relacji,
wraz z rozstrzygnięciem, czy milczenie takiego leksykonu odmawia, jak przy przyimkach,
czy przepuszcza, jak przy ramie domyślnej czasownika;
świadka w słowniku ta wiedza nie ma, bo SGJP kolokacji nie znakuje.
Świadkiem nie jest przy tym kolumna przyimków w `olski/leksykon.txt`, choć wygląda
na niego: mówi ona, jakiego przyimka żąda rama rzeczownika — `informacja o czymś` —
a nie, którym przyimkiem mówi się o rzeczy, że coś jest przy niej.

Aspekt bezokolicznika nie jest sprawdzany, a czasownik nad nim go wybiera:
`zacząć` żąda niedokonanego, więc `Czeladnik zaczął zapłakać.`
przechodzi przez pytanie o ramę, które stawia `Robi` w `olski/skład/składnia.py`,
i wychodzi zdaniem, którego polszczyzna nie ma.
Rama jest tu sprawdzona co do pozycji i niesprawdzona co do formy,
która tę pozycję wypełnia, i jest to ta sama luka, którą ma
[dopełnienie wyrażone zdarzeniem](../docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
tylko o piętro niżej: tam leksykon mówi, czy bezokolicznik wolno postawić,
a tutaj nie mówi, który.
Kosztuje to dziś czasownik w tabeli `olski/skład/makieta.py`,
która `zacząć` i `przestać` pomija, żeby losowanie takiego zdania nie wypuściło.
Do przeczytania jest to, co `harness/walenty.py` bierze z Walentego,
bo słownik ten aspekt przy pozycji `infp` wypisuje,
oraz `POZYCJE_LEKSYKONU` w `olski/walencja.py`,
czyli zdanie leksykonu, które tę pozycję wpuszcza.
Ruchem jest czwarta kolumna leksykonu wraz z żądaniem postawionym `odmień`,
albo rozstrzygnięcie, że aspekt jest wyborem lematu i że wybiera go autor,
a wtedy ruchem jest zdanie o tym w docstringu `Robi`.

`przejrzyj` w `olski/skład/przegląd.py` uczestnika bezokolicznika z niczym nie zestawia,
więc `Zegar chciał wynieść klucz.` nie zgłasza się,
choć jest to ta sama klasa co `Koszt szynki przewyższa koszt bułki.`,
od którego ten moduł powstał:
oba rzeczowniki brzmią w mianowniku i w bierniku tak samo,
forma przeszła `chciał` rodzaju tych dwóch nie rozdziela,
i polszczyzna czyta ten ciąg zarówno jako SVO, jak i jako OVS.
Zamykają go dwa miejsca naraz:
`_zdania_pod` w `olski/skład/składnia.py` wypuszcza treść i okoliczność wyrażoną zdarzeniem,
a zdania postawionego jako dopełnienie nie wypuszcza,
i `Robi.uczestnicy` obok niego bezokolicznika za uczestnika nie liczy.
Ruchem jest uczestnik bezokolicznika zestawiony z podmiotem czasownika nad nim,
a nie ze swoim, bo bezokolicznik podmiotu nie ma;
para przechodzi więc przez piętro, czego żadna dzisiejsza para nie robi.
Do przeczytania jest to, co
[`docs/sklad.md`](../docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie)
mówi o tym, że podmiot w takim zdaniu nie staje nigdy,
oraz [postawa przeglądu](../docs/sklad.md#drzewo-jest-jednoznaczne-a-napis-z-niego-nie-musi-być),
która o tym pomiarze mówi, że liczy się go z form, które w tekście stanęły.
Zażąda to od `_rozróżnia` czasownika z innego zdania niż uczestnik,
bo trzeci warunek pyta o formę, którą rola z czasownika wyciąga,
a bezokolicznik nie wydaje żadnej i obu rolom oddałby tę samą;
formą, która te dwie rozdziela, jest `chciał` ze zdania nadrzędnego.
Dzisiaj obie strony tego porównania biorą się z jednego zdania i tylko stamtąd.

`abstrahuj` w `olski/skład/rozbiór.py` nie ma pozycji na `orzecznik_łącznika`,
więc `Flaga to kawałek tkaniny.` wraca brakiem kategorii,
choć gramatyka to zdanie wyprowadza
([`docs/konstrukcje-gramatyczne/orzeczenie.md`](../docs/konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim)).
Rola stoi w `DEKLARACJA` w `olski/subset/deklaracja.py` i nie stoi w `POZYCJE`,
czyli jest to ta usterka, którą komentarz nad `POZYCJE` opisuje.
Samo dopisanie pozycji nie kupuje jednak nic i dlatego wpis jest jeden, a nie dwa:
kandydat odpada wtedy na linearyzacji, bo `Jest` wypisuje kopulę,
więc pierwsze rozstrzygnięcie jest o tym, czy łącznik niesie coś ponad nią.
Niesie — wtedy jest kategorią dziedziny obok `Wyróżnienie`,
a `Flaga to kawałek tkaniny.` i `Flaga jest kawałkiem tkaniny.` znaczą co innego.
Nie niesie — wtedy zdejmuje go `znaczenie` tak samo jak znacznik tematu,
linearyzacja przestaje być funkcją,
a niezmiennik obiegu żąda przynależności po obu stronach
([`docs/design-notes.md`](../docs/design-notes.md#the-round-trip-invariant)).
Pomiar nad Składnicą daje do tego rozkład obu konstrukcji, a nie samo rozstrzygnięcie,
bo to jest osąd o polszczyźnie.
