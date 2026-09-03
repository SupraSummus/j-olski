# Formy i leksemy: warstwa pod kategoriami

Kategoria dziedziny dochodzi do napisu przez zgodność, przez morfologię
i przez dwa leksykony obok nich.
Ten dokument mówi, co się w tej warstwie liczy zamiast sprawdzać,
skąd bierze się forma i czego brakuje:
słowa, którego słownik nie ma,
formy odesłanej poza rejestr
i leksemu, którego lemat nie wskazuje.
Same kategorie trzyma [kategorie-zapisu.md](kategorie-zapisu.md),
a poziom, na którym one stoją,
[sklad.md](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka).

## Checks that are cheap, deterministic, and explainable

All finite-domain, all effectively linear time,
all able to say why they failed:

- Noun-phrase-internal agreement,
  adjective and determiner against noun,
  on case, number, and gender
- Subject-verb agreement on person and number,
  and on gender in the past tense and conditional
- Verbal government:
  `używać` demands genitive,
  so `używam komputera` and not `używam komputer`
- Prepositional government,
  each preposition licensing a fixed set of cases
- Genitive of negation,
  applied as a rewrite during linearization
  so that it is automatic rather than checked
- Aspect and tense legality:
  `będę zrobił` is unconstructible,
  and perfective present is future
- Gender resolution under coordination:
  `Jan i Maria przyszli`, never `przyszły`
- Clitic and `się` placement

Every failure should report two feature bundles and their provenance,
along the lines of
*`czarna` is nom.sg.f, `kota` is acc.sg.m2,
mismatch on case and gender, from lines 3 and 4*.
That is a diagnostic a human can act on,
and it is the thing a language model structurally cannot provide:
it cannot say which rule fired,
and it will not give the same answer twice.

## Morphology generation is the underestimated piece

Analysis maps a form to tags.
Generation maps a lemma plus tags to a form.
The compiler needs the second,
and Polish inflection carries enough irregularity,
stem alternation,
and paradigm classes
that hand-writing it is a multi-year detour.

Morfeusz 2 exposes generation over SGJP,
whose 2020 edition characterizes nearly 456,000 Polish lexemes,
and both are distributed under a liberal BSD licence.
That one dependency is the difference
between a weekend-scale core and a years-scale one,
which is why the open lexicon is a settled decision.

## Leksykon projektu: SGJP nie zna słów, których używa rejestr

Słownik pod spodem nie zastępuje pisania w dwóch miejscach.
Nie ma słów, które rejestr techniczny tworzy sam — `komit`, `olski`, `lintować`
dostają `ign`, czyli nie mają czego wypuścić.
I nie ma leksemów, które ten rejestr dokłada do napisów znanych:
projekt piszący o agentach jako o programach żąda liczby mnogiej `agenty`,
a `agenty`, które SGJP wydaje, jest formą deprecjatywną leksemu osobowego,
czyli tym, czym mówi się o ludziach z góry, a nie liczbą mnogą rzeczy nieżywotnej.
Wpis takiego leksykonu nazywa więc leksem wraz z odmianą,
a nie sam napis dopisany do listy słów.

Rozróżnianie leksemów jest przy tym pytaniem, które słownik już zadaje
i na które sam odpowiada wszędzie tam, gdzie leksemy rozdzielił.
`zamek:Sm3~a` i `zamek:Sm3~u` to dwa leksemy różniące się dopełniaczem,
a `Włochy:Sn_pt~szech` i `Włochy:Sn_pt~chach` to kraj i dzielnica Warszawy,
różniące się miejscownikiem.
Ten identyfikator czyta jeden kierunek:
synteza pyta o niego przez `olski/skład/leksemy.py`
([niżej](#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)),
a `olski/morph.py` ucina go przy analizie.
Kwalifikator słownik niesie tym samym polem, a czytają go oba kierunki,
każdy inaczej, i jedna lista mówi im obu to samo (`POZA_REJESTREM`
w `olski/rejestr.py`).
Synteza formę odesłaną poza rejestr zdejmuje, bo wybiera jedną z kilku poprawnych;
analiza jej nie zdejmuje, bo zdanie z formą dawną polszczyzna ma, tylko liczy ją
kosztem, przez który czytanie na niej stojące schodzi niżej w kolejności
([disambiguation.md](disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie)).
`projekta` oznaczone jako `daw.` ze składu przez to nie wyjdzie,
a do parsera wejdzie czytaniem droższym od pozostałych.
Brak słowa, rozdzielony leksem i przeczytany kwalifikator
widać naraz, nad `pl.sgjp.sgjp-2026.06.01`:

```sh
python3 -c "
import morfeusz2
morf = morfeusz2.Morfeusz()
for lemat in ('projekt', 'zamek', 'komit'):
    for forma, leksem, tag, _, kwalifikatory in morf.generate(lemat):
        if 'pl:nom' in tag or 'sg:gen' in tag or tag == 'ign':
            print(forma, leksem, tag, kwalifikatory)
"
```

Leksykon projektu jest plikiem, który czyta to repozytorium,
a nie słownikiem dołożonym Morfeuszowi, i decyduje o tym cena wejścia.
Morfeusz przyjmuje słownik własny przez `dict_path`,
ale przyjmuje go skompilowanego,
a pakiet z PyPI wydaje bibliotekę wraz z wiązaniem do Pythona i nic poza tym,
co widać po zawartości katalogu, w który się instaluje,
więc tamta droga żąda łańcucha narzędzi spoza PyPI
i zabiera to, co [`CLAUDE.md`](../CLAUDE.md#checks) ma za instalację jednym poleceniem.
Plik czytany przez oba kierunki kupuje przy tym to samo,
co kupuje [leksykon walencyjny](walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej):
że `komit` jest słowem raz, a nie dwa razy.

Czym wpis jest, zapadło po stronie analizy i wpis wskazuje leksem:
`olski.toml` nazywa leksem, wedle którego słowo się odmienia,
wraz z jedną formą, którą ten leksem ma wydać.
Alternacja tematu, która przeciw wskazaniu leksemu stała,
schodzi na sam wzorzec, a to, czego takie wskazanie nie kupuje,
trzyma [warstwa-leksykalna.md](warstwa-leksykalna.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma).
Czyta tę sekcję strona analizy, a skład jej nie czyta,
więc obietnica z akapitu wyżej — że `komit` jest słowem raz, a nie dwa razy —
czeka na drugiego czytelnika, i ruch do niej trzyma [`todo/`](../todo/README.md).

## Kwalifikator mówi o formie dwie rzeczy i tylko jedna jest rejestrem

Kwalifikator jest jedynym kryterium wyboru formy,
które w danych stoi gotowe i nie żąda niczego poza przestaniem go wyrzucać.
Co za tym stoi, widać na dwóch słowach, których obu żąda opowieść o bazyliszku,
i widać na nich od razu, że kryterium nie jest jedno.

Bez odsiania wychodzi polszczyzna, której nikt nie pisze.
Zaimek względny rodzaju męskiego wychodził jako `któren`,
oznaczone w SGJP jako `daw._dziś_gwar.`,
a przeszła forma `zgasnąć` jako `zgasnęła`, oznaczone jako `rzad.`
Obie stoją w słowniku przed formą zwykłą,
więc kompilator brał je nie dlatego, że coś rozstrzygnął, tylko dlatego, że nie pytał.

Po odsianiu każdego kwalifikatora naraz wychodzi polszczyzna o innym znaczeniu.
SGJP rozdziela `oko` na dwa leksemy i temu o liczbie mnogiej `oczy`
daje kwalifikator `anat.`, a temu o liczbie mnogiej `oka` nie daje żadnego,
więc kryterium bez podziału zamieniłoby zdanie legendy
`Bazyliszek otworzył oczy.` na `Bazyliszek otworzył oka.`,
czyli na oczka w sieci albo w rosole.
Nazwa dziedziny nie odsyła tu formy poza rejestr, tylko mówi, w którym znaczeniu
leksem tak się odmienia, i jest to zupełnie inne zdanie o tej samej formie.

Podział jest więc rozstrzygnięciem, a nie odczytem,
i stoi w `POZA_REJESTREM` w `olski/rejestr.py`.
Nazwy, które w słowniku występują, wypisuje polecenie
nad listą lematów, którą to repozytorium już ma:

```sh
python3 -c "
import collections, morfeusz2
morf = morfeusz2.Morfeusz(generate=True, expand_tags=False)
lematy = [w.split()[0] for w in open('olski/leksykon.txt') if not w.startswith('#')]
nazwy = collections.Counter(
    nazwa
    for lemat in lematy
    for *_, kwalifikatory in morf.generate(lemat)
    for napis in kwalifikatory
    for nazwa in napis.split(',')
)
for nazwa, ile in nazwy.most_common():
    print(ile, nazwa)
"
```

Zasięg tego polecenia jest zasięgiem tamtej listy, czyli czasownikami,
i to jest jedyna słabość tego wywodu:
`anat.`, `mors.` oraz `daw._dziś_gwar.` wychodzą dopiero na rzeczownikach,
więc lista nazw jest sumą dwóch przebiegów, a nie wyjściem jednego polecenia.
Nazwa, której żaden przebieg nie pokazał, przechodzi jak nazwa dziedziny,
i to ten podział kosztuje.
Odwrotny domyślny kosztowałby więcej, bo formę odsianą przez pomyłkę
widać dopiero wtedy, gdy jej brak wywali całą komórkę paradygmatu.

## Nazwę leksemu wybiera autor, bo lemat go nie wskazuje

Kwalifikator jest kryterium, które w danych stoi gotowe.
Leksem jest kryterium, którego w danych nie ma:
identyfikator słownik niesie, a które z dwóch znaczeń autor miał na myśli,
mówi tylko autor.

Że wybiera go autor, a nie cecha, widać na dwóch parach naraz.
`oko` rozdziela się na leksem zbiorowy i niezbiorowy,
a różnicę tę niesie tag, bo `oczy` mają cechę `col`, a `oka` `ncol`,
więc dałoby się je rozróżnić żądaniem cechy, tak jak żąda się przypadka.
`Włochy` rozdzielają się na kraj i dzielnicę Warszawy,
a tag obu jest w miejscowniku ten sam, `subst:pl:loc:n:pt`,
i różni je wyłącznie identyfikator.
Kryterium cechowe pokryłoby więc pierwszą parę i nie tknęłoby drugiej,
a leksem pokrywa obie.

Drugą połową ustalenia jest to, że w drzewie stoi nazwa, a nie identyfikator.
Poziomem kategorii tego pakietu jest
[dziedzina](sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka),
a kod paradygmatu jest napisem z wnętrza słownika innego projektu,
więc drzewo pisze `R.oko_w_rosole`,
a z identyfikatorem wiąże tę nazwę `olski/skład/leksemy.py`.
Wiązanie jest wiele do jednego z założenia:
oczko w sieci i oko w rosole to jeden leksem i dwie rzeczy, o których się pisze,
więc nazw jest tyle, ile rzeczy, a nie tyle, ile leksemów.
Nazwa goła jest wpisem tego samego rodzaju:
`oko` znaczy w tym repozytorium oko, a nie oczko,
i tyle wystarcza, żeby legenda otwierała bazyliszkowi oczy
bez wpisu przy każdym użyciu.

Kiedy wpis jest potrzebny, rozstrzyga zgoda leksemów, a nie ich liczba.
`dziób` ma dwa leksemy, z których jeden słownik odsyła do żeglarstwa,
i oba mają w dopełniaczu `dzioba`,
więc pytanie o dopełniacz ma odpowiedź, pod którą oba podpisują się naraz.
`oko` w liczbie mnogiej odpowiedzi wspólnej nie ma,
i wtedy `odmień` zgłasza `WieleLeksemów` wraz z formami, które z każdego wychodzą,
bo autor rozstrzyga między znaczeniami i widzi je po tym, co z nich wyjdzie.

Najdroższy przypadek nie jest przy tym rzeczownikiem:
`stać` ma leksem niedokonany i dokonany,
a forma dokonana w czasie teraźniejszym jest w polszczyźnie przyszła,
więc milczenie wypuszczałoby stąd zdanie o tym, co będzie,
zamiast zdania o tym, co jest.

Tym samym kryterium schodzi rodzaj, który jest wartością, a nie formą:
`potwór` ma leksem zwierzęcy oraz osobowo-zwierzęcy,
więc zwierzę jest tym, pod czym podpisują się oba,
a wybór alfabetyczny dałby tu osobę.

Ceną tego kryterium jest cisza w miejscu, o które nikt nie pytał:
leksemy różniące się poza żądaną komórką przechodzą bez zgłoszenia,
bo pytanie brzmi „która forma”, a nie „który leksem”.
Otwarte zostaje to, na co to kryterium nie sięga,
i jest to słownik mówiący „albo tak, albo tak” pod jednym leksemem:
`postaci` obok `postacie` w jednej komórce
oraz `anioł` z rodzajem wypisanym dwiema wartościami w jednym tagu.
Identyfikator nie rozstrzyga ani jednego, ani drugiego, i trzyma to
[`todo/`](../todo/README.md).

Leksykon ten jest przy tym innym plikiem niż
[leksykon projektu](#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr),
bo odpowiada na inne pytanie:
tamten dokłada leksem, którego słownik nie ma, a ten wybiera z tych, które ma.

Po stronie analizy nie zmienia się nic i jest to rozstrzygnięcie, a nie zaległość.
Identyfikatora nie potrzebuje tam nic:
`Rosół ma oka.` i `Bazyliszek ma oczy.` wyprowadzają się po jednym czytaniu,
a reguły o zbiorowość nie pytają.
Leksem wpuszczony do czytania sięgnąłby za to każdego szukania po lemacie,
czyli leksykonu walencyjnego i `KOPULA` w `olski/walencja.py`,
i każde z nich musiałoby powiedzieć, którą połowę identyfikatora dopasowuje.
Wchodzi on tam wtedy, gdy będzie reguła, która tożsamości leksemu zażąda.
Kryterium, które po tamtej stronie już stoi, jest innego rodzaju i nie zastępuje tego:
[`admissible`](warstwa-leksykalna.md#the-dictionary-offers-readings-polish-does-not)
wyrzuca czytanie, którego polszczyzna nie ma,
a tutaj oba czytania polszczyzna ma i różnią się tym, o czym mówią.
