# Olski as a linter

The motivation, stated plainly:
a linter for Polish prose,
used to check texts produced by language models.
Not for syntactic errors —
models rarely make those —
but for the patterns they habitually fall into.

A linter helps write good code.
This is to help write good Polish.

Wycofaliśmy pakiet reguł, a nie linter.
Usunięte są silnik reguł, pakiet typograficzny i polecenie, które je uruchamiało.
Linter został celem.
[Lista celów](roadmap.md#cele) nazywa go wykrywaczem wzorców prozy.
Powody tamtej decyzji zostają w tym dokumencie.
Zostają dlatego, że mówią o polszczyźnie, a nie o programie.
Ile razy reguły strzeliły nad tekstem, który ktoś napisał,
liczy [firing-rates.md](firing-rates.md).
Tam są też wszystkie liczby, na których decyzja się oparła.

## Co zamknęło pakiet reguł

Powody są trzy.
Żaden z nich nie mówi, że linter to zły pomysł.
Każdy dotyczy innej z [czterech osi](#cztery-osie-każdej-reguły) opisanych niżej.

**Every rule that shipped was decided by a character,
and a character is not what this repository is about.**
The pack held seven rules, and every one of them
needed nothing but a tokenizer to fire:
quotation marks, spacing, a stray dash.
That is the shallowest of the depths
[the tier ladder below](#how-deep-does-each-rule-have-to-see) sets out.
A rule that has to know what a word *is* was never written,
and the second finding is why.
The grammar, by contrast, asks whether a sentence has exactly one reading,
which is a question about what the sentence means to a reader,
and the repository is for that question.

**A deeper tier was expected to be the escape and is not.**
The cheap version of the central plain-Polish rule
matches `-anie`, `-enie` and `-cie`,
and the plan was that a lemma-keyed version would supersede it
once morphological analysis arrived.
[What the nominalization endings match](#what-the-nominalization-endings-match)
measured the succession instead of assuming it:
a lemma removes the matches that are inflections
and cannot touch the ambiguous ones, which are what the rule turns on.
So the shallow rule reads characters
and the deep one does not answer the question either.

**Calibration never happened, and without it a rule is an opinion.**
[Calibration](#the-thing-that-makes-or-breaks-it-calibration)
is stated below as the thing that makes or breaks the whole pack,
and no rule ever carried one: each shipped saying so in its own declaration.
What ran instead was a firing rate over two bodies of Polish,
which is [half of the pair](#what-a-rate-on-human-polish-means-depends-on-the-rule)
and says whether a rule has anything to do
rather than whether it can be trusted.
Reading the hits said the rest, and it reads badly:
the rule with the most hits was right about two thirds of them,
another was measuring two tables rather than anybody's prose,
and [the two rules that left the pack before it](firing-rates.md#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt)
had fired over a hundred times without finding one defect.
The counts are that document's.

## Cztery osie każdej reguły

Każdą regułę da się ustawić na czterech osiach.
Osie są od siebie niezależne.
Każda rozstrzyga co innego.

| oś | wartości | co rozstrzyga |
| --- | --- | --- |
| głębokość | znak, morfologia, rozbiór | ile maszynerii reguła potrzebuje |
| kształt | werdykt o zdaniu, stopa nad tekstem | czy potrzebny jest próg |
| populacja | proza własna, cudza polszczyzna | czy trafienia da się przeczytać wszystkie |
| pytanie | o strukturę, o uzus | czy głębsza analiza pomoże |

Każdy z trzech powodów [zamknięcia](#co-zamknęło-pakiet-reguł) dotyczy innej osi.
Pierwszy dotyczy głębokości: reguła rozstrzygała się na samym znaku.
Drugi dotyczy pytania: nominalizacja pyta o uzus.
Trzeci dotyczy kształtu i populacji naraz: stopa nad cudzą prozą, bez progu.

Tylko jeden z tych powodów dotyczy więc głębokości.
Jest to zarazem powód najsłabszy.
Mówi on, że taka reguła jest w tym repozytorium nieciekawa.
Nie mówi, że jest nietrafna.
Dwa pozostałe powody dotyczą reguły na każdej głębokości.
Weźmy regułę, która liczy konstrukcję zamiast znaku.
Jest głębsza od reguł z tamtego pakietu.
Dalej jest jednak stopą nad cudzą prozą, więc progu potrzebuje tak samo.

Praktyczne wnioski są takie.
Reguła, która jest stopą, potrzebuje progu, a próg trzeba skalibrować.
Reguła, która jest werdyktem o zdaniu, progu nie ma i kalibracji nie potrzebuje.
Reguła, która chodzi po naszym własnym tekście i ma nie znaleźć nic,
progu też nie potrzebuje, bo wszystkie trafienia i tak się czyta.
Tak jest zbudowany cel [wykrywacza wzorców prozy](roadmap.md#cele).
Reguła, która pyta o uzus, nie zyska na głębszej analizie.
Reguła, która pyta o strukturę, zyska tylko na niej.

Wszystkie cztery osie nazywaliśmy przedtem słowem „linter”.
Dlatego wycofanie pakietu wyglądało jak wycofanie celu.
Gdzie linter wypadnie na tych osiach, rozstrzygnie reguła, którą ktoś napisze.

## Kolejna reguła zaczyna się od zdania z usterką, a kalibracja przychodzi przed awansem

Katalog zasad dobrego pisania jest długi, a każda z nich brzmi rozsądnie,
dopóki się jej nie zmierzy — i to jest ta sama pułapka,
w którą wpadł [wycofany pakiet](#co-zamknęło-pakiet-reguł).
Pułapka druga stoi po przeciwnej stronie:
reguła, która ma być zmierzona przed napisaniem, nie powstaje,
bo pomiar kosztuje więcej niż ona.
Kolejność jest więc taka, i pomiar stoi w niej przed awansem, a nie przed pisaniem.

1. **Zacznij od zdania w korpusie usterek.**
   Reguła ma zdanie, w którym czytelnik usterkę by poprawił,
   i poprawkę, nad którą ma milczeć (`próba/usterki.txt`).
   Reguła bez takiego zdania jest pomysłem, a nie kandydatką.
2. **Zapytaj, czego żąda od maszynerii.**
   Regułę, która rozstrzyga się na rozbiorze, warto pisać tutaj
   ([niżej](#suffixes-buy-more-than-expected));
   regułę, której wystarczy znacznik, można pisać wszędzie,
   a pisze się ją tu wtedy, gdy stoi na niej zdanie z korpusu.
   Role, których taka reguła potrzebuje, wpisz do wpisu korpusu:
   sonda odpowie wtedy `źle czytane` zamiast ciszy,
   a to znaczy, że przed regułą stoi gramatyka.
3. **Napisz wykrywacz za flagą.**
   Wchodzi do kodu, gdy trafia w swoje zdania korpusu i milczy nad ich poprawkami
   (`python3 -m harness.usterki`).
   Sondy nad rejestrem przed tym krokiem nie ma,
   bo wykrywacz za flagą kosztuje jedną funkcję i jeden test.
4. **Przeczytaj trafienia nad cudzym tekstem, a nie samą ich liczbę.**
   Wypisuje je baza sądów (`harness/sądy.py`), a czyta czytelnik,
   i mówi o każdym, czy poprawiłby to, co zgłoszenie wskazuje.
   Reguła, która trafia często, a każde trafienie jest chybione,
   jest gorsza od reguły, która milczy, i schodzi z kodu.
5. **Awansuj do znalezisk po sądach.**
   Zgłoszenie wchodzi do wydruku domyślnego i do kodu wyjścia,
   gdy sądy je potwierdzają, a ile ich trzeba, mówi
   [reguła trzech](corpora.md#baza-sądów-ocenia-znaleziska-a-ocenione-nie-wracają).
   Brak sądów wstrzymuje awans, a nie krok trzeci.
   Reguła, z której wychodzi próg, zostaje za flagą, dopóki nie ma korpusu.
6. **Zawężaj ją tak, żeby myliła się w jedną stronę.**
   Zawężenie, które zdejmuje trafienia, może zgłoszenie schować;
   takie, które je dokłada, umie zgłoszenie wymyślić,
   a wymyślone kosztuje zaufanie do wszystkich pozostałych reguł.
   Co zawęzić, mówi szum nad poprawką w korpusie usterek.

Sześć kandydatek przeczytano nad prozą tego repozytorium
i żadna z nich nie ma stąd zamkniętej drogi:
ta proza jest pisana rejestrem, który katalog chwytów nazywa usterką,
więc trafienia nad nią mówią o niej, a nie o tekście autora.
Kandydatka wraca, gdy jej zdanie stanie w korpusie usterek.
Co przeczytanie pokazało, zostaje, bo mówi o kształcie każdej z nich.
Odległość podmiotu od orzeczenia trafia nad README kilka razy,
a za każdym razem stoi między nimi zwykły okolicznik albo szyk odwrócony.
Zdanie podrzędne zagnieżdżone w podrzędnym trafia nad tą prozą raz.
Czasownik domowy trafia nie rzadziej niż w co czwarte zdanie tej prozy,
więc wskazuje dokument, a nie zdanie w nim, i jest stopą, a nie werdyktem.
Nominalizacja w pozycji imiennej trafia w większość zdań,
bo rzeczownik odczasownikowy jest w tym rejestrze zwykłym terminem:
`przeliczenie` i `zatrzymanie` nazywają tu rzeczy, których inaczej nie ma jak nazwać.
Wzmacniacz bez treści nie trafia w tej prozie ani raz poza `słowo kluczowe`,
czyli poza kolokacją, która wzmacniaczem nie jest,
a nie trafia dlatego, że katalog chwytów go zakazuje i ktoś tę prozę pod niego przepisał;
o tekście autora to zero nie mówi nic.

Jedno twierdzenie na zdanie odpadło dwoma predykatami, a nie jednym,
i warto powiedzieć, na czym stanął każdy.
Liczba twierdzeń rozstrzyga się rejestrem:
`CLAUDE.md` pozwala tak pisać wywód,
a zakazuje instrukcji, więc reguła ta żąda progu, którego nie ma czym skalibrować.
Dwa człony spięte spójnikiem trafiają przy tym w ponad połowę zdań instrukcji,
a przeczytane mówią, że `Skreślony tekst zostaje w gicie, więc pomyłka jest odwracalna.`
jest zdaniem dobrym.
Drugim predykatem jest sam skrót, czyli słowo wzięte z członu wcześniejszego,
i jego trafienia są w większości zaimkiem przymiotnym stojącym bez rzeczownika —
`którego`, `ta`, `każda` — albo zwykłą koordynacją o wspólnym podmiocie.
Rozdzielić jedno od drugiego umie dopiero rozbiór,
bo pyta się tu o to, czy przymiotnik jest głową grupy, czy orzecznikiem,
a tego morfologia nie mówi.
Tej głębokości żąda [cel o żądaniu pozycji](roadmap.md#cele) i tam ten predykat wraca.

Dwie kandydatki z korpusu usterek przeczytano tak samo, a wykrywacza nie ma żadna.
Orzeczenie bez wykonawcy brane z samej formy nieosobowej
trafia nad tą prozą w co kilkadziesiąte zdanie,
a trafienia są w większości czasownikiem, który czynność orzeka —
`zmierzono`, `wybrano`, `przeczytano` — i wykonawcą jest tam sesja,
której nazwanie nie dokłada nic.
Z tego rozdziału wyszła reguła o
[czasowniku pustym](#trzeci-wykrywacz-zgłasza-czasownik-pusty-przed-rzeczownikiem-odczasownikowym):
`Podjęto decyzję o odłożeniu wdrożenia.` różni się od tamtych trafień tym,
że czynność nazywa rzeczownik, a nie ten czasownik.
Łańcuch dopełniaczy czytany z morfologii o łańcuchu nie mówi,
bo dopełniacz jest zlany z innymi przypadkami:
`zdania tego jednego pliku` wychodzi łańcuchem czterech,
a sekcje angielskie dokładają trafienia bez ani jednego dopełniacza,
bo Morfeusz czyta ich słowa jako polskie formy.
Reguła ta żąda rozbioru i wraca z nim.

Liczb tu nie ma, bo rusza je przeredagowanie akapitu;
kto chce dzisiejszych, pisze predykat na nowo i puszcza go.

## Gdzie na tych osiach wypada reguła o zaimku

Pierwsza reguła wydana po zamknięciu pakietu zgłasza zaimek,
który zgadza się z dwiema rzeczami nazwanymi w zdaniu obok
([subset.md](subset.md#zaimek-wskazujący-na-dwie-rzeczy-jest-drugim-znaleziskiem)).
Na każdej z [czterech osi](#cztery-osie-każdej-reguły)
wypada inaczej niż reguły wycofanego pakietu,
i to jest powód, dla którego weszła.

Głębokością jest rozbiór, czyli ten poziom,
pod który gdzie indziej trzeba najpierw napisać parser polszczyzny.
Zdanie obok wydaje tylu kandydatów, ile ma najszerszych grup imiennych,
a nie tylu, ile ma rzeczowników,
i tej różnicy nie pokaże ani znacznik, ani lepsze wyrażenie regularne:
w `Ogrodnik ogląda pole maków w doniczce bratków.`
rzeczowniki są cztery, a rzeczy nazwane dwie.

Kształtem jest werdykt o zdaniu, a nie stopa nad tekstem.
Progu ta reguła przez to nie ma i kalibracji nie potrzebuje,
czyli nie brakuje jej tego, czego brak zamknął pakiet.
Kryterium „więcej niż jedno” progiem wybranym nie jest:
tym samym kryterium olski liczy odczytania jednego zdania.

Pytanie jest o strukturę, a nie o uzus,
bo o zgodności liczby i rodzaju rozstrzyga znacznik, a nie częstość.
Populacją jest i proza własna, i cudza, a rozdziela je to samo, co przy pakiecie.
Nad prozą tego repozytorium wszystkie trafienia się czyta.
Nad cudzą reguła stopy nie obiecuje, bo żadnej nie liczy:
zgłasza pojedyncze zdanie i wypisuje przy nim rzeczy, o które chodzi.

## Wykrywacz chwytu zgłasza „to” bez rzeczownika przy sobie

Reguła o zaimku wskazującym na dwie rzeczy jest znaleziskiem,
czyli mówi o polszczyźnie zdania.
Druga reguła wydana po zamknięciu pakietu mówi o rejestrze, w którym je napisano,
i jest pierwszym wzorcem z katalogu chwytów,
który wytrzymał [pomiar](#kolejna-reguła-zaczyna-się-od-zdania-z-usterką-a-kalibracja-przychodzi-przed-awansem).
`To` otwierające zdanie, które nie ma przy sobie rzeczownika,
podejmuje całe zdanie obok, a naprawą jest rzeczownik wstawiony w jego miejsce.
Wykrywa go `olski/chwyty.py`, a wypisuje flaga `--chwyty`.

Na [czterech osiach](#cztery-osie-każdej-reguły) wypada to tak:
głębokością jest morfologia, kształtem werdykt o zdaniu,
populacją nasza własna proza, a pytanie jest o strukturę.
Progu przez to nie ma i kalibracji ta reguła nie potrzebuje.
Rozstrzyga ją jeden warunek: czy rzeczownik zgodny z zaimkiem stoi przy nim,
czyli przed orzeczeniem zdania.
`To zdanie ma dwa czytania.` przechodzi, bo zaimek określa tam rzeczownik,
a `To jest miejsce, gdzie olski milczy.` nie przechodzi,
bo rzeczownik za orzeczeniem zaimka nie określa.

Wiersz o chwycie pada obok werdyktu i tylko pod flagą.
Populacją jest proza, za którą odpowiadamy,
a autor sprawdzający swój tekst tego katalogu nie zna.
Chwyt czyta się przy tym z morfologii, więc pada też nad zdaniem,
którego gramatyka nie wyprowadza, czyli nad większością tych dokumentów,
a werdykt mówi tam, dokąd doszła analiza.

Nad prozą tego repozytorium przebieg stanął na zerze,
a kosztowało to kilkadziesiąt zdań przepisanych w dokumentach, w modułach i w testach.
Zostają w nim same zdania przytoczone w grawisach jako przykład:
ekstrakcja zdejmuje grawisy, a kropka w środku przykładu punktuje prozę wokół niego
([extraction.md](extraction.md#what-the-reader-sees-is-not-always-polish)),
więc wykrywacz dostaje `To jest tanie.` jako zdanie tego dokumentu.
Odróżnić ich nie ma czym, dopóki ekstrakcja nie mówi, co było przytoczeniem.

## Drugi wykrywacz zgłasza zwrot zastępujący orzeczenie członu

Zwrot `tak samo` zamykający człon, w którym nie ma orzeczenia,
zastępuje orzeczenie tego członu:
czytelnik ma je wziąć z członu wcześniejszego, a kto wszedł w środek akapitu,
tamtego członu nie przeczytał.
Tak samo działają `też` i `odwrotnie`, więc wykrywacz bierze wszystkie trzy.
Naprawą jest powtórzony czasownik, choćby zdanie wyszło dłuższe.
Wykrywa ten zwrot `olski/chwyty.py`,
a wypisuje go ta sama flaga `--chwyty` co zaimek wyżej.

Na [czterech osiach](#cztery-osie-każdej-reguły) reguła ta wypada tam,
gdzie reguła o zaimku: kształtem jest werdykt o zdaniu,
populacją nasza własna proza, pytanie jest o strukturę,
a głębokością morfologia, bo orzeczenie w członie poznaje się ze znacznika,
a człony rozdziela interpunkcja.
Progu przez to nie ma i kalibracji ta reguła nie potrzebuje.

Zawężenia są trzy — zwrot zamyka człon, w członie nie ma orzeczenia,
a człon następny nie otwiera się spójnikiem porównania — i każde zdejmuje
inną klasę zdań poprawnych; przykład przy każdym stoi w `olski/chwyty.py`.
Wzięły się z pomiaru, a nie z wywodu:
predykat bez nich zgłasza kilkakrotnie więcej zdań tej prozy,
a jego trafienia są w większości porównaniami `tak samo jak X`.

Myli się ta reguła w jedną stronę:
zwrot, za którym stoi przeczenie — `części mowy też nie` — mówi to samo
i wykrywacz go nie widzi, bo człon zamyka tam przeczenie.
Zdanie zaczynające się małą literą reguła oddaje bez werdyktu z tego powodu,
z którego oddaje je reguła wyżej: takie zdanie ucięła ekstrakcja na kropce,
którą postawił przykład przytoczony w grawisach.

Zdania, które reguła ta zgłosiła nad prozą repozytorium, przepisano —
kilkanaście w dokumentach, w modułach i w testach —
a nad prozą przepisaną reguła milczy.
Zwrot ten jest tanią częścią reguły o jednym twierdzeniu na zdanie,
a co odrzuciło resztę tamtej reguły,
mówi [krok czwarty](#kolejna-reguła-zaczyna-się-od-zdania-z-usterką-a-kalibracja-przychodzi-przed-awansem).

## Trzeci wykrywacz zgłasza czasownik pusty przed rzeczownikiem odczasownikowym

`Dokonano przeprowadzenia analizy` nazywa czynność rzeczownikiem,
a czasownik niesie z niej sam czas i tryb, choć czynność jest jedna
i czasownik ma czym ją orzec: `Zespół przeanalizował awarię`.
Naprawą jest ten czasownik, a nie krótsze zdanie.
Wykrywa to `olski/chwyty.py`, a wypisuje ta sama flaga `--chwyty` co reguły wyżej.
Reguła ta jest pierwszą, którą postawił
[korpus usterek](roadmap.md#kolejkę-ustawia-korpus-usterek-a-nie-kolejka-blokerów):
zdanie z usterką i jego poprawka stały w `próba/usterki.txt`,
zanim ktokolwiek napisał predykat.

Na [czterech osiach](#cztery-osie-każdej-reguły) kształtem jest werdykt o zdaniu,
populacją nasza własna proza, a pytanie jest o strukturę:
rozstrzyga się tu, czy czynność orzeka czasownik, czy rzeczownik obok niego.
Progu przez to nie ma i kalibracji ta reguła nie potrzebuje.
Głębokością jest morfologia, a oba zawężenia tej reguły —
rzeczownik stojący zaraz za czasownikiem i rzeczownik bez czytania
rzeczownikowego — biorą się z tego, czego morfologia nie mówi:
ani czy ten rzeczownik jest dopełnieniem tego czasownika,
ani którym ze swoich czytań stoi.
Rozbiór by ją przez to zaostrzył, a przykład przy każdym zawężeniu
stoi w `olski/chwyty.py`.
Nominalizacji z wycofanego pakietu reguła ta nie wskrzesza:
tamta pytała, czy rzeczownik odczasownikowy jest gorszy od czasownika,
i pytała o to nad każdym, a ta pyta o zamkniętą listę czasowników,
które czynności nie orzekają.

Nad prozą repozytorium reguła nie kosztowała ani jednego zdania przepisanego
i tym różni się od dwóch reguł wyżej:
tego wzorca nikt tu nie napisał, bo katalog chwytów go zakazuje.
Zostają w jej przebiegu same zdania przytoczone jako przykład,
tu i w `olski/chwyty.py`, i jest to ta sama pozostałość, którą ma reguła o zaimku
([wyżej](#wykrywacz-chwytu-zgłasza-to-bez-rzeczownika-przy-sobie)).

```sh
python3 -m olski.check --chwyty CLAUDE.md README.md docs/*.md docs/*/*.md todo/*.md
python3 -m olski.check --chwyty $(find olski harness tests witryna opowieści -name '*.py')
```

Reszta tego dokumentu opisuje tamten pakiet i argumenty, które za nim przemawiały.

## The target register: technical documentation

A style linter is close to useless for accomplished prose,
where every rule it enforces is one a good writer breaks on purpose.
For technical documentation it is exactly the right instrument.

This is not a compromise, it is the field's own answer.
Every controlled language with measured results behind it
was built for technical documentation:
Simplified Technical English for aircraft maintenance manuals,
Caterpillar's languages for heavy machinery,
the whole type C and type T cluster in Kuhn's survey.
Nobody has ever usefully controlled literary prose,
and the reason is not that nobody tried.

There is a sharper version of this point in
[glr-in-practice.md](glr-in-practice.md),
which observes that the archival shorthand it parses
is *already* a controlled natural language,
controlled by editorial convention rather than by design,
and that this is the only reason
a few hundred lines of grammar get anywhere.
Technical documentation is the same kind of object:
a register that professional convention has already narrowed,
which is why rules over it can be both few and defensible.

Fixing the target register resolves the hardest calibration problem.
In technical documentation,
nominalization, impersonal constructions, hedging and uniformity
are defects by professional consensus.
In fiction the same features are instruments.
Scoping olski to expository and technical Polish
means its rules can be defended
instead of endlessly qualified.

See [the fiction question](#and-fiction) for the other half of this.

## This is the same subset, approached from behind

A controlled natural language is a whitelist.
It says: only these constructions exist,
everything else is outside the language.

A linter is a blacklist.
It says: write whatever you like,
but these patterns get flagged.

The set of texts that pass every rule
is still a subset of Polish.
It is simply defined by exclusion rather than by construction,
and that turns out to be enormously cheaper.

### It dissolves the habitability problem

The single largest risk in the controlled-language framing
was habitability:
the closer olski got to Polish,
the less an author could feel where the boundary lay,
and the more often good Polish would be rejected
for reasons that felt arbitrary.
See [similar-work.md](similar-work.md#the-habitability-problem).

A linter has no boundary to feel.
There is no rejection, only advice,
and the author remains free to ignore it.
The failure mode drops from
"the tool refuses my sentence"
to "the tool nags about my sentence",
which is a category of failure every programmer already tolerates daily.

Cenę tę u olskiego płaci autor, a odrabia mu ją kształt odpowiedzi.
Werdykt wypisuje odczytania, które zdanie ma,
więc autor czyta granicę z samej odpowiedzi, a nie z odmowy
([README](../README.md#co-działa)).
Rachunek z fotela autora opisuje
[pisanie-po-olsku.md](pisanie-po-olsku.md#kto-płaci-za-odrzucone-zdanie).

### It also removes two hard requirements

No generator is needed,
so the round-trip invariant is no longer load-bearing.
No unambiguous surface form is needed,
so the tension between closeness to Polish and round-tripping disappears.

What remains of the grammar work
is a question of *depth*:
how much analysis does each rule need in order to fire correctly.

## How deep does each rule have to see

This replaces [the cost ladder](design-notes.md#the-cost-ladder)
as the project's central tradeoff,
and it is far friendlier,
because most useful rules sit at the bottom.

| Tier | Machinery | Rules it enables |
| --- | --- | --- |
| A | Tokenizer, sentence splitter, regular expressions | Typography, literal stock phrases, connector density, sentence-length variance, list and bullet density |
| A+ | Suffix regexes over word endings | A surprising amount of tier B, without a tagger. See below |
| B | Morphological analysis and lemmatization | Lexical rules over inflected forms, nominalization density, part-of-speech ratios, impersonal and passive constructions, adjective stacking |
| C | Chunking or dependency parsing | Subject-predicate distance, clause depth, coordination length, constructions rather than strings |
| D | Full constituency parse | Very few rules genuinely need this |

### Suffixes buy more than expected

[glr-in-practice.md](glr-in-practice.md) records a working Polish system
that classifies occupations
with a single alternation over agent-noun endings —
`-strz`, `-nik`, `-arz`, `-acz`, `-iec`, `-ica`, `-nier`, `-iusz`, `-ant` —
with no dictionary and no lemmatizer.
Crude, and it works.

That matters here more than it did there.
The central plain-Polish rule,
nominalization density over `-anie`, `-enie` and `-cie`,
is a suffix pattern by definition,
so it needs no morphology at all.
The same goes for impersonal `-no` and `-to` forms.
Several rules that belong under tier B by their subject matter
are really tier A with a better regex,
which moved the morphology dependency later
and made the first useful rule pack look cheaper than it was.

Lemma-keyed lexical rules need real morphology.
So does one of the three nominalization endings,
and what the other two want is not morphology at all.
[What the nominalization endings match](#what-the-nominalization-endings-match)
is that measured rather than predicted.

Wyciągnęliśmy stąd wniosek w dwóch krokach.
Krok pierwszy: poziomy A i B niosą większość wartości takiego narzędzia.
Krok drugi: parser i las rozbiorów nie są więc linterowi potrzebne,
a linter ma z tym repozytorium mało wspólnego.

Krok pierwszy zostaje.
Potwierdza go japoński pakiet reguł, w którym po morfologię sięga garść reguł
([prose-linters.md](prose-linters.md#japanese-is-the-proof-that-this-transfers)).
Krok drugi z pierwszego nie wynika.
Reguła, która nie potrzebuje naszej maszynerii, jest dalej regułą, której chcemy.
O tym, czy reguła jest warta wydania, rozstrzyga kalibracja, a nie głębokość.

Zostaje jedna rzecz, której nie da się zbudować gdzie indziej.
Jest to reguła, która rozstrzyga się na rozbiorze polskiego zdania.
U nas poziom C i D kosztuje tyle, co napisanie samej reguły, bo parser już jest.
Gdzie indziej trzeba do tego napisać parser polszczyzny.
Pierwszą taką regułą jest
[zaimek na dwie rzeczy](#gdzie-na-tych-osiach-wypada-reguła-o-zaimku).

### What the nominalization endings match

Over the 31,417 words of prose extracted from
[the audit corpus](audit-corpus.md#the-list),
at the commits that list pins,
`-anie`, `-enie` and `-cie` match 906 words.
`harness/endings.py` asks Morfeusz what each match is
and files it by the first class its readings satisfy.
The run that list prints is what leaves the prose in `proza/ksef` and `proza/rit`,
and one command over those two produces this table and the one in the next section:

```sh
python3 -m harness.endings proza/ksef proza/rit --probe nominalization --probe impersonal
```

| class | words | | commonest |
| --- | --- | --- | --- |
| gerund and ordinary noun both | 446 | 49.2% | `pobranie`, `uprawnienie`, `nadanie` |
| a gerund and nothing else | 259 | 28.6% | `uwierzytelnianie`, `pobieranie`, `uwierzytelnienie` |
| an inflected form of another word | 147 | 16.2% | `kontekście`, `formacie`, `dokumencie` |
| a verb form | 37 | 4.1% | `zostanie`, `dacie` |
| no verb behind it and no other lemma | 9 | 1.0% | `liście`, `oczywiście`, `kilkanaście` |
| no reading | 8 | 0.9% | `samofakturowanie` |

Two of the classes move the rule between tiers,
and they move it in opposite directions.

**A lemma removes two thirds of `-cie` and leaves nothing to act on.**
135 of that ending's 198 matches are the locative singular of a masculine noun
whose stem ends in `t` — `format`, `kontekst`, `dokument`, `moment`, `certyfikat` —
where the ending is an inflection and not a suffix,
and 9 more are adverbs, a numeral, a region and a plural noun:
`oczywiście`, `osobiście`, `kilkanaście`, `Podkarpacie`, `liście`.
The other two endings carry 12 inflected forms between them,
so the contamination belongs to this ending rather than to the three,
and it grows with the register,
Polish technical prose taking its nouns from English and Latin stems in `t`.
What survives the lemma is 46 words,
every one of them in the ambiguous class below:
this ending's gerund column is empty
where `-anie` fills it 202 times.
So a lemma moves the rule from firing on 198 words to firing on 46
and does not make one of the 46 decidable.
That 135 is a floor, and so is the inflected class it sits in:
the classifier tests for a verb first, on the strength of `zostanie`,
so the 6 occurrences of `dacie` and the one of `powiecie` are counted
in the verb row above,
where a document dating an invoice means the locative of `data`
and an address the locative of `powiat`.

**No tier removes the ambiguous class, which is the larger one.**
Morfeusz reads `pobranie`, `przeznaczenie` and `uprawnienie`
as a gerund and as an ordinary noun both,
and it gives `zdanie` and `mieszkanie`
the same pair of readings it gives `pobranie`.
Those two were the standing examples of words the rule must not fire on,
so the analyser agrees with the ending about every word the ending gets wrong.
What separates them is that a Polish reader has a verb available for one
and only the noun for the other,
and no reading records that:
morphology answers whether a word derives from a verb,
where the rule asks whether a verb would do instead.
The two questions have the same answer often enough
for the suffix to look like a cheap version of a lemma rule,
and they come apart over nearly half of this corpus.

This is the finding that shut the plan's escape hatch,
and [it is one of the three that closed the pack](#co-zamknęło-pakiet-reguł).
A suffix rule was to ship early
on the promise that a later lemma version would have to beat it on the numbers,
and here the lemma version is the same rule:
it removes the 147 inflected forms and the 9 words with no verb behind them,
and cannot touch the 446.
What would settle those is a count of how established each pairing is,
which is a corpus and not an analyser,
and no tier of analysis is a shortcut to one.

### The impersonal endings come out the other way

The same run over `-no` and `-to`, the pack's other suffix pair,
answers a different question and gets a friendlier answer.
Here the target is a tag rather than a judgement:
Morfeusz reads an impersonal form as `imps`, and there is nothing to argue about.

| ending | matched | the `imps` target | what the rest is |
| --- | --- | --- | --- |
| `-no` | 395 | 362, 91.6% | 24 adverbs, 9 else |
| `-to` | 153 | 39, 25.5% | 99 of the pronoun `to`, 15 else |

**The predicted problem is the smaller one.**
The roadmap warns that a great many Polish adverbs end in `-no`,
and 24 of 395 do: `zarówno` 17 times and `osobno` 7.
At 6.1% that ending is the cleanest measured anywhere in this section,
and `dodano`, `rozszerzono` and `zaktualizowano` are what it is finding.

**What costs is one word.**
99 of `-to`'s 153 matches are the pronoun `to`,
which is among the commonest words in the language,
and taking that single word out leaves 54 matches of which 39 are the target.
So this is not the undecidable class above but a stoplist,
and buying precision back with a list of exceptions in the data
is cheaper than a tier of analysis.

Between them the two pairs say the plain-Polish pack is not one prognosis.
`-no` ships on a tag.
`-to` ships behind a list of the words the ending catches that are not verbs.
Nominalization ships or does not on a question no tag answers,
and which of the three a rule is
cannot be read off the fact that all three are suffixes.

A smaller thing the run turns up belongs to the corpus rather than to an ending.
3 of the two endings' matches are an English identifier reaching the prose,
`validto`, which is [the extraction](extraction.md)
leaving a name where a reader sees one,
and it puts a floor under any rate either ending reports over documentation.

### Recognizing a phrase by what it is not costs more

The suffix finding moves rules down a tier.
One kind of rule moves the other way:
a rule that has to know a phrase is *not* the subject.
Rules about word order are of this kind.

`Trzech pozostałych wskaźników projekt nie ustala`
puts a genitive phrase where the subject belongs,
and every step of recognizing that is contested.
`trzech` has a nominative reading beside its genitive one,
`projekt` is nominative or accusative,
and a numeral in the nominative takes a genitive noun anyway,
so the fronted phrase reads as a subject
until gender government rules it out —
the numeral's nominative reading is masculine personal
and `wskaźnik` is not.
Settling that is agreement over a chunk, not a tag over a word,
which is tier C.
A better regex does not reach it,
and neither does a lemma.

Nor does the precision-first escape:
fire only where every reading agrees, and stay quiet otherwise.
On real Polish that rule never fires.
`nie` carries a pronoun reading beside the particle,
so no negated sentence ever qualifies,
and the genitive of negation is what puts a fronted object
in the genitive to begin with.
A check that declines everywhere is not a cautious check;
it is one that does not reach its input,
which [is a different thing from abstaining](#abstention-is-allowed).

Tier C here means chunking.
It does not mean the parse forests,
so the honest consequence above survives:
what these rules need is the shallow end of the deeper track.

## The thing that makes or breaks it: calibration

**A rule without a measured false-positive rate on good human Polish
is a stylistic prejudice, not a linter rule.**

Good Polish writers use em dashes.
They use three-item lists.
They nominalize when nominalizing is right.
A rule set assembled from intuition
will punish exactly the human writing it claims to protect,
and there is no way to know which rules are like that
without measuring.

So the pack needed a paired corpus:

- **Human Polish**, in the register a pack is scoped to
  and at the stage a linter runs at.
  [corpora.md](corpora.md#the-composition-this-argues-for) surveys what is obtainable
  and arrives at two bodies rather than one,
  because a rule whose hits get read
  and a rule reporting a rate against a norm want different prose.
- **Generated Polish**, from several models,
  on comparable topics and in comparable registers.
  This half is cheap, on the condition that it is generated and then left alone.
  Text that has been edited against style detectors
  reports a floor rather than a rate,
  which [generated-polish.md](generated-polish.md#what-this-corpus-cannot-support)
  measures on a corpus that had been.

Then every rule carries two numbers,
and the two questions behind them are
whether the rule can be trusted
and whether it has anything to do.
Trust is a number on the human side whatever the rule.
A rule whose hits get read has both of its numbers out of that one reading,
its hits and the defects among them,
and it is a rule reporting a rate against a threshold
that wants the generated half for the second:
where human Polish sits on a statistic
says nothing yet about how much generated Polish stands beyond the threshold.

This was to be the replacement for the coverage curve,
and it is the better experiment:
cheaper to run, and it produces a rule set
that has earned each of its rules.
It is also the piece that never got built,
which is [the third finding](#co-zamknęło-pakiet-reguł).

### What a rate on human Polish means depends on the rule

The number that decides whether a rule ships is the one on the human side,
and reading a firing rate there as a false-positive rate assumes something.
proselint made the assumption by choosing its corpus:
a hit on prose from a magazine that edits properly is a false alarm,
because a real defect would have been taken out before it was printed.
[prose-linters.md](prose-linters.md#what-beating-them-takes)
holds the score that rests on the assumption
and says it has to be stated out loud.

Stated out loud, it turns out to be a claim about the corpus,
and the corpus that makes it true of one rule makes it vacuous for another.
Typesetting removes a double space and a straight quotation mark mechanically,
so `double-space` and `quote-straight` fire on published Polish
at a rate near zero,
and that rate measures the typesetter rather than the rule.
The corpus could not have held what they look for.

What they look for lives one stage earlier,
which is also the stage a linter runs at.
A straight quotation mark in a draft is usually ambiguous —
an inch mark, a fragment of code, a citation left in English,
which is [generated-polish.md](generated-polish.md#polish-closing-quotation-marks-are-absent)'s
list and its account of the corpus where it happened not to bite —
and that ambiguity is the rule's real false-positive risk,
out of reach on prose that has been through a typesetter.
So these rules ask for prose caught where the linter will see it,
and their hits there have to be read rather than counted.
Reading them is cheap, which is the good half of the bargain:
a quotation mark is a quotation mark,
and a hundred of them are settled in an afternoon.
Where reading every hit would be expensive —
a nominalization that might be the right word,
a dash that might be the right mark —
an editor decided about the defect instead of removing it,
which is exactly when the assumption does its job
and the rate stands on its own.

The typesetter is one such step and not the only one,
which matters when the corpus gets chosen.
A corpus build renormalizes characters as thoroughly,
and [corpora.md](corpora.md#its-text-layer-has-been-character-normalized)
measures that happening to the reference corpus of Polish,
so what these rules ask for is not prose from before typesetting
but prose that reached its reader through no step that rewrote its characters.

So one demand, in two shapes:

- **A rule whose answer depends on the site rather than on the rate**
  owes an audit, over prose at the stage it will run on.
  Its hits are read, and the share of them that were real defects
  is the number.
- **A rule reporting a rate against a norm** owes a distribution
  over prose somebody edited.
  Where good human Polish sits on the statistic it measures
  is where a threshold can go
  without accusing the writing the rule was built to protect.

The two shapes want different corpora,
and neither was ever sourced.

Discrimination between the human and the generated half
belongs to the second shape alone,
and there it sets a threshold rather than deciding that a rule exists.
A detector's figure of merit is discrimination and a linter's is precision.
The two come apart here:
a rule catching a real defect in human and generated Polish alike
is doing the job a linter is for and failing the job a detector is for,
and [olski is the first of those](#limits-worth-stating-up-front).
What no rule may do is fire on Polish that is fine.

### Abstention is allowed

A rule that cannot tell
whether it is looking at a defect or a legitimate choice
should decline to fire rather than guess.

This is the same instinct as the extractor in
[glr-in-practice.md](glr-in-practice.md#ambiguity-as-a-confidence-measure),
which answers only when its parse is unambiguous
and otherwise leaves the field empty for a human.
Ambiguity there is not resolved but used as a confidence measure.

The measured version of that system sharpens the argument
and separates two things the first reading of it ran together.

Deliberate abstention is nearly free there.
It fires on 2 rows in 1000.
Silence from *lack of coverage* is what costs:
202 rows in 1000 fail to parse at all.
Both return nothing to the caller,
but only the first is the precision instinct at work;
the second is a grammar that does not reach its input,
and its linter analogue is not abstention but
*no rule matched*, which is the normal case and not a decision.

What the extracted 47.3% shows is that
when the thing does commit, it is right.
That is the property worth copying,
and the rows it stayed quiet on
were already queued for human review,
so quiet cost nothing.

One of those two abstentions is a warning.
The readings it declined to choose between
were byte-identical,
produced twice by an optional-whitespace rule,
so the check discarded a line it had understood perfectly.
A linter that abstains
must compare *distinct* outcomes rather than counting attempts,
or it will fall silent on exactly the cases it got right.

For a linter the equivalent is a bias toward precision over recall.
A missed defect costs nothing.
A false accusation against good Polish
costs the user's trust in every other rule,
and trust is the only thing that makes a linter get run twice.

## Anchor to Polish norms, not to model fingerprints

There are two ways to justify a rule.

*This is what models do* dates immediately.
Wikipedia's editors observe that
"stands as a testament" places a text in 2023 or 2024 specifically.
Tells decay as models change,
so a rule set built on fingerprints
needs continuous maintenance
and is trivially obsoleted by the next release.

*This is bad Polish style* does not date.
And it happens to catch the same texts,
because what makes model prose recognizable in Polish
is largely that it is nominal, impersonal, hedged, and uniform —
which Polish style authorities were already against.

**Prosta polszczyzna supplies a citable norm.**
The Pracownia Prostej Polszczyzny at the University of Wrocław
has spent over a decade codifying it,
and its rules are directly mechanizable:

- **Rzeczowniki zombie** — nouns in `-anie`, `-enie`, `-cie`;
  check whether a verb would do instead
- Phrases that invite them —
  `w celu`, `w razie`, `z powodu`, `na skutek`,
  especially at the start of a paragraph
- Keep subject and predicate close together
  and near the start of the sentence;
  avoid interpolations
- Write personally:
  avoid `-no` and `-to` forms, avoid `się` passives,
  avoid `można`, `trzeba`, `należy`, `warto`

Every one of those is also a model tell.
That overlap is the project's best piece of luck:
the rules can be defended on Polish stylistic grounds
and still do the job they were wanted for.

## What already exists

**Prose linters.**
Half a dozen mature engines exist for English,
and [prose-linters.md](prose-linters.md) is the survey:
what their rule formats reach,
which of their mechanisms have no Polish data behind them,
and what the one tool that measured its own false-positive rate
asks of a rule set.

**LanguageTool is the most important existing thing.**
It is an open-source rule-based proofreading tool
with a mature Polish rule set,
described in Miłkowski's *Developing an open-source, rule-based proofreading tool*
(Software: Practice and Experience, 2010),
built on **Morfologik**,
one of the few freely licensed Polish morphological analysers,
with roughly 3.5 million forms.

That makes it either the platform to extend
or the thing to deliberately not be.
Writing olski's rules as LanguageTool XML
is a legitimate delivery route
and would come with an installed base,
an editor integration story,
and a Polish morphology layer already wired up.

**StyloMetrix**, developed at NASK,
extracts up to 195 stylometric features for Polish —
grammatical forms, lexical types,
part-of-speech frequencies, syntactic structures.
If the statistical rules need a feature extractor,
it exists and it speaks Polish.

**Wikipedia's *Signs of AI Writing***,
maintained by WikiProject AI Cleanup,
is the closest thing to the rule set olski wants:
roughly 15,000 words,
distilled from thousands of flagged articles since 2023,
explicitly descriptive rather than prescriptive.
It is English, and it is a model for how to organize such a catalogue.

**Jasnopis** is the Polish readability tool,
scoring difficulty from 1 to 7 and simplifying automatically since 2023.
Readability is adjacent to, not the same as, style linting.

## What the research says

The strongest documented markers are lexical,
and specifically stylistic verbs and adjectives rather than content words.
In English, `delves` runs at 28 times its pre-LLM baseline,
`underscores` at 13.8,
`showcasing` at 10.7.

Across studies, measures of **lexical richness** are the most robust signal,
while most other proposed indicators
depend strongly on the particular model and text domain.
Work in PNAS finds that models
use a narrower vocabulary,
lean on auxiliary verbs,
carry fewer content words,
and fail to reproduce the stylistic variation
that distinguishes human genres from one another.

The same work puts rates on three constructions rather than on words,
which is what makes it usable outside English.
Instruction-tuned models write present participial clauses
at two to five times the human rate
and nominalizations at one and a half to two times.
Both were candidate rules here,
and the Polish counterpart of an English participial clause
is the `-ąc` form,
which makes the citation behind it a mapping across languages
rather than a measurement on Polish.
The agentless passive runs the other way,
at roughly half the human rate,
against the intuition that model prose is the more impersonal.
The impersonal and `się`-passive entry survives that,
because what cites it is the plain-Polish norm and not model behaviour —
[anchoring to norms](#anchor-to-polish-norms-not-to-model-fingerprints)
earning its keep in the one case where the two disagree.

Polish work points at
repetitive sentence structures,
predictable vocabulary,
uniform sentence length,
and conspicuously textbook-correct syntax
that avoids irregular or ambiguous constructions.

**And the gap is explicit.**
The stylometric study behind those feature lists
analysed English Wikipedia introductions only,
and its authors state that the findings
do not generalize across language typologies.
Polish-targeted detectors are reported
to run at 10 to 15 percent error.
A calibrated, explainable, Polish-specific rule set
does not appear to exist.

## And fiction

The harder and more interesting wish:
some way for language models to write good Polish prose.

[fiction.md](fiction.md) is the survey behind this section:
the catalogue of documented failure modes,
the evidence that post-training rather than prompting produces them,
and the interventions that have results behind them.
What follows is the summary.

A linter cannot deliver that.
A linter removes defects.
Removing every defect from a text
produces something competent and dead,
which is already the characteristic failure of model fiction.
No amount of subtraction adds voice.

### What is nevertheless lintable in fiction

More than one might expect,
because prose craft has its own catalogue of defects,
and they are as mechanical as the technical ones:

- **Cliché** — a corpus-derived blacklist of exhausted Polish literary phrases,
  the `serce zabiło mocniej` family.
  This is the most tractable fiction rule of all,
  and it is pure tier A.
  The corpus is the trap, not the rule:
  see [fiction.md](fiction.md#what-this-means-for-olski)
  on why mining Wolne Lektury yields period marking rather than cliché.
- **Filter words** — `poczuł, że`, `zauważył, że`, `wydawało się, że`,
  constructions that hold the reader one step away from the scene
- **Adverbial dialogue tags** — `powiedział cicho`, `odparła nerwowo`
- **Repeated sentence openers**, especially subject-first every time
- **Abstraction density** — the ratio of concrete to abstract nouns,
  where model prose reliably drifts abstract

And a structural observation worth keeping:
several metrics serve both registers with **inverted thresholds**,
and [fiction.md](fiction.md#what-this-means-for-olski)
holds the measurements behind that.
It means one engine and one set of measurements,
with per-pack targets rather than per-pack code,
which is why the check that measured sentence-length variation
carried a floor and a ceiling and asked each pack for either.

Which of the two a technical pack sets
would have had to be settled before a rule declared one,
and it never was.
Low variance is the tell in technical documentation,
which asks for the floor,
while a register described as wanting uniformity
is one where the ceiling is the flag,
and nothing here decides between the two readings.

### The handle on a defect above the phrase is position or recurrence

The list above stops where it does because a rule matches a string,
and the defects that make model fiction unreadable are not strings.
Two of them turn out to be reachable anyway,
and neither is reachable as a string.
One is a property of *where* a sentence stands,
the other of *how often* the text comes back to something.
Both are countable.

**Position.** A theme explained in the last sentence of a section
is not a sentence a blacklist can hold,
but the position is a place a tool can point at,
and the rate at that position is a number.
[generated-polish.md](generated-polish.md#the-closing-sentence-is-measurably-different)
owns the measurement.

**Recurrence.** An entity introduced with apparatus and then dropped
is a legitimate choice once and a habit at scale,
so the defect exists at the corpus and not in any file.
[generated-polish.md](generated-polish.md#two-entities-in-five-are-introduced-and-dropped)
owns that measurement, and a check was written against it
before the pack was retired.

Both reach a trace and not a cause.
[fiction.md](fiction.md#what-this-means-for-olski) reads
four of the ceiling defects as one failure to model minds across a text,
and a text can end fewer sections on a negation
without acquiring anyone to have written them.
What a rate buys is a critic with something specific to say,
which is the whole of the claim in
[what would actually help](#what-would-actually-help-and-is-not-linting)
and none of the claim that the defect has been addressed.

So a rule aimed above the phrase
either names a position or names a thing that recurs,
or it is a trope, and a trope is not lintable.
The third case has been attempted and is worth learning from:
[generated-polish.md](generated-polish.md#what-happened-when-the-rules-were-deleted)
records a taxonomy of genre-exhausted ideas
reimplemented as keyword lists, and deleted with them.
What is worth keeping after such an attempt is the taxonomy,
which was the argument for making a rule's justification and its sources
fields of the declaration rather than comments in a checker.

### What would actually help, and is not linting

Three directions, none of them a linter,
listed in increasing order of interest:

**Constraint instead of prohibition.**
Rules that say *you must do this*
rather than *avoid that*.
Every scene contains a physical object that recurs.
Point of view never leaves one head.
Constraints of this kind force choices a model would not default to,
which is where voice comes from.
The Oulipo understood this better than any style guide.

**Stylometric targets rather than stylometric alarms.**
StyloMetrix already extracts 195 features for Polish.
A linter uses that to measure distance from a norm and complain.
The generative move is to invert it:
name a point in that feature space —
the sentence-length distribution and lexical richness
of a particular Polish author, say —
and steer toward it.
Same instrument, opposite sign,
and far more likely to produce something with a voice
than any amount of flagging.

**The linter as a critic in a revision loop.**
This is where olski's determinism genuinely earns its place.
A model revising its own draft
against a vague instruction to write better
produces a differently bland draft.
A model revising against
*`spojrzenie` occurs eleven times in nine hundred words,
sentence lengths vary by a standard deviation of two,
and the concrete-noun ratio is half your target*
has something to actually act on.
Explainable and deterministic beats
judgement-by-another-model here,
precisely because it is the same complaint every time.

This is the best-supported of the three,
and the support is measured rather than aesthetic:
model judges rank generated fiction above New Yorker short stories,
so a revision loop with a model critic
optimizes toward the defect it was meant to remove.
See [fiction.md](fiction.md#the-evaluation-trap) for the evidence.

Honest asymmetry:
the technical-documentation linter is a project that can be finished.
Making models write good Polish fiction is an open research question.
Keeping them in that order,
with the second labelled as a wish rather than a milestone,
is what keeps this repository honest.

## Limits worth stating up front

**This cannot be a detector, and should not claim to be.**
Any linter that flags model tells
is defeated by anyone who runs the linter and fixes the flags.
That is fine — it is the same relationship
a code linter has with bad code.
The framing that survives is the one already chosen:
it helps write good Polish.
Framing it as detection would overclaim
and would age badly.

**Rules decay.**
Fingerprint rules need versioning,
a recorded date of observation,
and a policy for retiring them.
Norm-anchored rules mostly do not,
which is the second argument for anchoring to Polish style.

**False positives are the real failure mode,
and register is how they get in.**
Formal Polish written by humans — legal, academic, official —
is nominal, impersonal and hedged by convention,
and literary Polish breaks every rule deliberately.
This is why the target register is declared rather than assumed.
Rules belong to packs,
packs belong to registers,
and no rule ships without knowing which pack it is in.

## Sources

- <https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.971> — Miłkowski, developing an open-source rule-based proofreading tool
- <https://community.languagetool.org/?lang=pl> — LanguageTool's Polish rule community
- <https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup/Guide> — WikiProject AI Cleanup guide
- <https://en.wikipedia.org/wiki/Wikipedia_talk:Signs_of_AI_writing> — discussion of the signs-of-AI-writing catalogue
- <https://www.pnas.org/doi/10.1073/pnas.2422455122> — do LLMs write like humans, variation in grammatical and rhetorical styles
- <https://www.sciencedirect.com/science/article/abs/pii/S0957417425026181> — stylometry recognizes human and LLM-generated texts in short samples
- <https://arxiv.org/pdf/2606.04177> — systematic analysis of linguistic features in AI-generated text detection
- <https://blog.humanistyka.dev/2026/03/stylometryczne-cechy-tekstow-generowanych-maszynowo> — stylometric features of machine-generated text, with StyloMetrix
- <https://blog.humanistyka.dev/2026/02/rozpoznawanie-tekstow-ai-piec-grup-cech-zamiast-jednego-wskaznika> — five groups of features
- <https://dobratresc.com/2019/02/14/rzeczowniki-zombie-i-slowa-bufony-kontra-prosta-polszczyzna/> — rzeczowniki zombie and plain Polish
- <https://mycompanypolska.pl/artykul/10-zasad-prostej-polszczyzny/16380> — ten rules of plain Polish
- <https://jasnopis.pl/prosty-jezyk/> — Jasnopis and plain Polish
