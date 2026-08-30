# Notatki dla agentów AI

Tu jest cała konwencja pracy w tym repozytorium.
Osobnego przewodnika dla współpracowników nie ma;
ten plik jest jedyną kopią.

Reguły prozy obejmują README, wszystko w `docs/`,
`TODO.md`, ten plik,
komunikaty commitów i opisy pull requestów.

## Reguły przyjmujemy leniwie

Nowy tekst piszemy według reguł niżej.
Te same reguły stosujemy do zdania, które poprawiamy z innego powodu.
Starego tekstu poza tym nie ruszamy.
Sekcja napisana przed regułą nie jest przez to usterką.

Ta pobłażliwość dotyczy stylu, nie prawdy.
Zdanie, akapit i wpis z listy, które twoja zmiana unieważnia,
poprawiasz tym samym commitem, bo potem nikt nie widzi, że są nieaktualne.

## Piszemy po polsku, także w kodzie

Nowy tekst w tym repozytorium powstaje po polsku.
Reguła obejmuje prozę z listy na początku tego pliku,
komentarze i docstringi, które do prozy liczy
[łamanie wierszy](#semantic-line-breaks),
komunikaty, które drukuje narzędzie,
oraz nazwy, które w kodzie wybieramy:
modułów, klas, funkcji, testów, poleceń i flag.
Po angielsku zostaje to, czego nie wybieramy:
słowa kluczowe Pythona, API bibliotek, klucze konfiguracji i nazwy formatów.
W nazwie w kodzie piszemy znaki diakrytyczne, tak samo jak w zdaniu:
Python przyjmuje takie identyfikatory,
a pliki repozytorium są w UTF-8 (`.editorconfig`).
Nazw przy tym nie ukuwamy:
kalka czyta się jak termin, którego nikt tu nie zdefiniował,
więc gdzie polszczyzna nazwy nie ma, zdanie mówi, co się robi.

Żaden check nie pilnuje tej reguły ani żadnej innej reguły prozy:
sprawdzamy je w przeglądzie zmian, a nie w testach.
Gramatyka olskiego takim checkiem nie jest i nie ma być:
wyprowadza znacznie mniej, niż te dokumenty zawierają.

Zdanie, którego olski nie bierze, wolno jednak w każdym dokumencie ruszyć,
i wolno przy tym ruszyć zamiast niego gramatykę.
Który z tych dwóch ruchów wykonać nad danym zdaniem, a kiedy oba naraz,
rozstrzyga
[`docs/pisanie-po-olsku.md`](docs/pisanie-po-olsku.md#ruchy-są-dwa-i-spotykają-się-w-punkcie-kompromisu),
i on jest właścicielem tego kryterium.
Granica jest jedna i pada na zdanie, a nie na dokument:
zdanie po przepisaniu ma mówić to samo i mówić nie gorzej,
a takie, które pod parser zbiedniało, zostaje przy wersji autorskiej,
choćby przez to dalej nie przechodziło.
Przebieg po całym dokumencie jest przez to osobną zmianą, a nie robotą przy okazji:
każde zdanie rozstrzyga się w nim osobno,
a przebieg mechaniczny łamie tę granicę na tych zdaniach, których nie przeczytał.
Dokument przepisany zostawia po sobie zdania odrzucone i zostawić je musi,
bo część konstrukcji tańsza jest do wpuszczenia niż do obejścia.

README stoi pod tą regułą najostrzej i jest to wyjątek nazwany:
zdania tego jednego pliku piszemy tak, żeby olski je wyprowadzał,
a wieloznaczność mu zostawiamy, bo wyboru za czytelnika nie robi.
Cenę tego — pokrycie, które mierzy pisanie tak samo jak gramatykę —
trzyma [`docs/roadmap.md`](docs/roadmap.md#readme-jest-przyrządem-pomiarowym),
a polecenie, którym się to sprawdza,
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop).

Regułę przyjmujemy [leniwie](#reguły-przyjmujemy-leniwie) jak resztę,
ale jednostka jest tu inna.
Jednostką reguł prozy jest pojedyncze zdanie, bo zdanie poprawia się osobno,
a jednostką języka jest akapit, docstring, komentarz, komunikat
albo nazwa wraz z jej wywołaniami.
Akapit nowy powstaje po polsku także w sekcji angielskiej
i w dokumencie, który po polsku nie jest,
a akapit mocno przepisywany przekładamy przy okazji, tą samą zmianą.
Zdanie dopisane do akapitu angielskiego, którego nie przepisujesz,
piszemy po angielsku razem z nim, bo akapit czyta się w jednym języku.
Przekład całego dokumentu jest osobną zmianą.

## Six forces

Every rule below follows from one of six forces.
A rule you can derive from a force needs no separate justification,
and a newly noticed failure mode has an obvious place to go —
or a reason not to be written down at all.

- **The reader.**
  A document is read once, top to bottom,
  and only what came earlier is known.
  Test: can this sentence be understood from what stands above it?
- **The next change.**
  A fact changes in one place
  and leaves no stale copy anywhere else.
  Test: when this fact changes, how many places have to move?
- **Word choice.**
  A phrase was picked rather than arriving together with the topic.
  Test: did I write this, or did it assemble itself?
- **Plainness.**
  A sentence is written for somebody who has to act on it,
  rather than for somebody who will admire the writing.
  Test: rewrite it in the plainest Polish you can —
  what was lost besides the impression that the author can write?
- **Checkability.**
  A claim about the world names what would settle it.
  Test: what do I show someone who asks how I know?
- **The reader's time.**
  A passage is paid for by everyone who reads past it,
  whether it was needed or not.
  Test: what does this passage buy someone who has read what stands above it?

A failure mode that derives from none of the six
means either that a seventh force is missing
or that the rule is not worth having.

## Decyzja arbitralna nie dostaje wywodu

Część tego, co tu obowiązuje, jest kwestią gustu:
język, w którym piszemy, jeden plik zamiast osobnego przewodnika,
pięćdziesiąt znaków w temacie commita.
Taka decyzja mówi, co obowiązuje, i na tym koniec.
Wywód dorobiony do niej po fakcie jest oszustwem,
nawet jeżeli każde zdanie z osobna się broni:
podaje jako powód coś, co powodem nie było,
a czytelnik nie ma go czym odrzucić, bo decyzja i tak od wywodu nie zależy.
Zostaje to, co z decyzji wynika — koszt, granica stosowania, wyjątek —
a nie to, co ją rzekomo poprzedza.

## Skreślenie bywa całą naprawą

Zepsute miejsce — w prozie czy w kodzie — nie zawsze potrzebuje lepszej wersji.
Zanim napiszesz tę wersję, przeczytaj okolicę bez tego miejsca:
jeżeli reszta mówi już to samo, skreślenie jest całą zmianą.
Skreślony tekst zostaje w gicie, więc pomyłka jest odwracalna.

Skreślać wolno przy okazji:
miejsce, które ruszasz z innego powodu, wolno odchudzić.
Jednostką jest to miejsce, a nie plik — przebiegów po całym dokumencie nie robimy.
Tak samo przyjmujemy [reguły prozy](#reguły-przyjmujemy-leniwie).

Wolno tylko wtedy, gdy skreślenie niczego nie zabiera.
Sprawdzasz to jednym pytaniem:
czy skreślona rzecz jest nadal powiedziana gdzie indziej?
Jest — bo fakt ma [właściciela](#one-owner-per-fact-repeat-narrative-freely),
bo to drugie zdanie o tym samym,
bo to komentarz powtarzający wiersz nad sobą,
bo to sprawozdanie, które odtwarza się poleceniem.
Skreślasz wtedy od razu i bez pytania.
Nie jest — bo to jedyna kopia tej myśli.
Wtedy nie odchudzasz, tylko wycofujesz regułę albo wywód:
wpisz to do [`TODO.md`](TODO.md) i zostaw decyzję osobnej zmianie.

**Nie pisz sprawozdań. Sprawozdanie, które zastaniesz, skreśl.**
Nie potrzebujesz na to zgody ani lepszej wersji na jego miejsce.
Pisz to, czego bez sesji nie da się odtworzyć:
decyzję, odrzuconą alternatywę
oraz te zdania korpusu, które trzeba przeczytać, żeby werdyktowi uwierzyć.
Tabela, wyliczenie i sprawozdanie z przebiegu odtwarzają się poleceniem.
Sprawozdanie poznasz po dwóch rzeczach.
Sekcja pisana w czasie przeszłym przebiegu — „wyszło”, „policzono” —
jest sprawozdaniem, a nie dokumentem.
Pozycja bez konsekwencji, czyli taka, która nie ruszyła
ani decyzji, ani kodu, ani następnego ruchu, jest wyliczeniem tego, co próbowano.
Licencja jest tu potrzebna dlatego, że sprawozdanie kosztowało sesję,
a rzeczy zdobytej całą sesją nikt sam nie skreśli, dopóki nie wolno.
O samej liczbie mówi [akapit o liczbie kruchej](#pomiar-i-liczba-która-po-nim-zostaje),
a tu chodzi o cały pasaż.

**Wywodu ta licencja nie tyka.**
Powtórzenie polecenia kosztuje minuty,
a dwie wersje jednego wywodu kosztują więcej niż liczba nieaktualna:
liczby nikt nie broni, a rozjazdu dwóch wywodów nie łapie żaden test
([jeden właściciel](#one-owner-per-fact-repeat-narrative-freely)).
Kto skreśla, pyta więc o jedno:
czy po tym trzeba będzie puścić polecenie, czy podjąć decyzję.

**Rejestr nie jest sprawozdaniem.**
Rejestr rośnie razem z pracą —
sekcja na konstrukcję, wpis na sondę, wiersz na figurę —
i nie żąda przeczytania:
przebiega się go do swojego wpisu, więc wolno mu mieć stałe pola albo tabelę
zamiast prozy, którą czyta się od początku.
Wpis zamknięty nie żąda przy tym sekcji, tylko zdania w tej,
która jest jego wnioskiem
(znacznik zrobionego
[kasuje się z tego samego powodu](#documents-describe-the-present-git-owns-the-past)).

Skreślenie zrobione przy okazji idzie osobnym commitem,
bo wmieszanego w zmianę merytoryczną nikt w przeglądzie nie zobaczy.
Skreślenie, którego twoja zmiana wymaga, robisz w tym samym commicie co ją.

## The reader goes sentence by sentence

The test is not whether a sentence is true or on topic,
but whether it can be understood in the place it stands.
A sentence that fails it is in the wrong place,
however well the section around it is titled.
The same few things cause the confusion:

- **A name used before it is introduced** —
  a tier, a register, a pack, an abstention, LCFRS.
  The first occurrence says what it is; later ones need not.
- **A reference with no antecedent** —
  "this difference", "those requirements", "the above".
  The reader goes back and hunts,
  and if the antecedent is further down the hunt fails.
- **A conclusion before its premise.**
  This works in the other direction too:
  a paragraph laying out numbers before saying why they are worth reading
  asks the reader to memorize them for no reason,
  so provenance and measurement belong under the conclusion they produce
  rather than above it.
- **A variant before its condition.**
  A fallback argued for before the words "this applies when"
  reads as the plan.
- **A forward pointer used as a patch.**
  A pointer says where a fact's owner lives, and nothing else.
  If a sentence makes no sense until you follow it,
  the order is wrong and the pointer hid it.

Hence frame before detail.
The README states what olski is, why it is a subset,
where it is going and what runs,
before any document explains a mechanism.
A goal that takes half a document to reach sits too low,
however well it is described once you get there.

A heading serves that order and does not substitute for it.
It announces what the following paragraphs do,
and it does not fix a paragraph placed too early.
It pays for itself where a reader would otherwise
dig through twenty lines about something else to reach their own question:
[the analysis tiers](docs/linter.md#how-deep-does-each-rule-have-to-see)
are found by the reader who came for them.

The tail of a document is fixed, because there the order follows from the role:
a `Sources` section closes a document that cites,
and the document's own list of unsettled things
sits immediately before it —
[`Not yet decided`](docs/corpora.md#not-yet-decided) in `docs/corpora.md`.
Such a list only enumerates;
everything that justifies its entries is already behind the reader.

The test at the end of a change:
reread from the point where you started editing,
pretending you have not seen what follows.
An author remembers what is further down and cannot see the defect unaided.
A section you moved has two such points, and the one to reread from is where it landed:
there it precedes what used to introduce it,
which is invisible from the altitude a file is read at before editing.

## One owner per fact; repeat narrative freely

Prose may repeat; facts may not.
Restating context so a document reads standalone is good writing,
and scope notes, per-audience retellings
and "the neighbouring document covers X" summaries are welcome.
But every fact that can change —
a decision, a status, a threshold, a measured number, a boundary —
has exactly one owning section, and that is where edits land.
A restatement elsewhere names the owner, by link or by section heading,
and stays coarser than the original:
volatile detail is not re-enumerated at full precision a second time.
If a restatement is as precise as its owner,
a reader cannot tell which copy is current,
which is how two documents come to contradict each other.
The document list in the README is the reference example —
a sentence or two per document, no numbers, and every entry links its owner.

**A list owns its length.**
"Five reasons follow" copies what stands in plain sight below it,
and a sixth reason makes the copy wrong,
the way a constant holding an array's length does.
A count stays where it claims the set is closed:
[the six forces](#six-forces) are six until somebody finds a seventh.

**Reasoning has an owner in the same way a fact does.**
A mechanism is explained once,
and other places state the conclusion in a sentence and point at it.
`docs/linter.md` does this with the abstention-against-no-coverage distinction:
it uses the conclusion and credits
[`glr-in-practice.md`](docs/glr-in-practice.md#ambiguity-as-a-confidence-measure),
which owns the argument and the numbers.

**A construction admitted to the grammar is the fact these documents duplicate most.**
Its argument belongs to its section in
[`docs/subset.md`](docs/subset.md),
and the blocker queue, the stage plan and the register documents
state the conclusion in a clause and link that section.
A construction re-derived in a second document
makes the next addition a rewrite in two places.

**Code owns what is implemented; documents own what code cannot show.**
Which productions the grammar has, what a lexicon entry says,
what a probe counts: the module is the truthful copy,
and a document restating it acquires a second version that goes stale silently.
Documents own provenance, rejected alternatives,
rationale that spans several modules, planned work, and open questions.
An example that illustrates a *format* earns its place,
while a copy of behaviour does not.

**Komentarz nad ciałem jest właścicielem mechanizmu,
a pisze się go tam, gdzie rozkmina jest głębsza od kodu.**
Kod ma być zrozumiały sam:
nazwa symbolu, nazwa cechy i kształt ciała mówią, co ta produkcja bierze,
więc komentarz, który to powtarza, zabiera czytelnikowi czas i niczego nie dodaje.
Zostaje ten, którego z kodu nie widać:
czemu warunek stoi w tym ciele, czemu stała jest osobna
i co by się wyprowadziło bez tej cechy.
Tego potrzebuje ten, kto to ciało zmienia,
a on czyta ciało, nie dokument,
więc taki wywód stoi w komentarzu nad ciałem, wraz ze swoim przykładem.
Dokument, któremu ten wniosek jest potrzebny, powtarza go
i nazywa przy tym moduł, a nie nazwę w jego środku
([na czym wolno oprzeć zdanie](#na-czym-wolno-oprzeć-zdanie)).
Dokumentowi zostaje polszczyzna, cena, granica podzbioru
i alternatywa odrzucona, czyli to, czego kod nie pokaże.
Przesłankę formalizmu — taką jak ta o cesze,
której konstytuent nie niesie i której unifikacja nie sprawdza —
wolno powtórzyć przy każdym ciele, które na niej stoi,
bo jednym zdaniem podaje ona kontekst, a nie drugą kopię wywodu.

Komentarz wolno przy tym skrócić,
i nie jest to skreślenie, którego [reguła o skreślaniu](#skreślenie-bywa-całą-naprawą)
żąda tylko wtedy, gdy druga kopia stoi gdzie indziej:
zdanie, które powtarza wiersz pod sobą,
oraz akapit, który wywodzi to, co dokument już wywiódł,
schodzą do jednego zdania z nazwą modułu albo sekcji.
Skraca ten, kto to ciało czyta, i robi to bez pytania.

## Na czym wolno oprzeć zdanie

Zdanie w dokumencie opiera się zwykle na czymś poza sobą.
Nazwa pliku i nagłówek sekcji są publiczne i wolno się na nich oprzeć:
kto je zmieni, dostanie czerwone `tests/test_docs.py`.
Reszta jest prywatna —
nazwa funkcji w module, kolejność pozycji na liście,
liczba, przykład, format wydruku —
i rusza ją zwykła robota, która o tym zdaniu nie wie.

Naprawą jest wskazanie właściciela zamiast jego wnętrza:
nazwa modułu zamiast nazwy funkcji w środku,
nazwa reguły z linkiem zamiast miejsca w kolejności.

Na rzecz prywatną wolno się oprzeć tam, gdzie pilnuje jej test:
blok wydruku wszedł do dokumentu dlatego, że `tests/test_wydruki.py`
puszcza komendę i porównuje wiersze.

## Documents describe the present; git owns the past

A document that narrates its own evolution becomes a changelog,
and git already keeps a better one:
complete, dated, and attached to the actual diffs.
The test for a sentence about the past:
**does it change what a reader working with the current state should do?**
If it only records that something happened or was once different, delete it.
If it explains why the present looks the way it does,
keep it as present-tense rationale rather than as an event.

History that earns its place, always as rationale for the current state:

- **A rejected alternative and the reason for rejecting it**,
  which saves the next person from proposing it again.
  [Dlaczego biała lista, skoro czarna była tańsza](README.md#dlaczego-biała-lista-skoro-czarna-była-tańsza)
  in the README is the reference example:
  the linter framing is named, and priced, and turned down.
- **A deliberate reversal or renaming**, so that nobody restores it by accident.
  `docs/roadmap.md` says the grammar is no longer the goal
  and what it survives as.
- **A date that identifies an external artifact** —
  a corpus version, a published measurement,
  the observation that "stands as a testament" dates a text to 2023 or 2024.
  That is provenance and it stays.

History that is deadweight:

- **Done markers.**
  When an entry in an open list closes, delete it;
  no ~~strikethrough~~ trophies.
  If it leaves a decision behind,
  the decision moves into the section that owns it and the entry still goes.
- **Status narration** — "update (2026-07): …", "now implemented".
  Fold the current state into the sentence that owns the fact.
- **A date whose only job is to order the document's own edits.**
  Such a date means an append happened where a rewrite was needed.

A word-level tell for all of these:
temporal adverbs — "still", "already", "no longer", "not yet", "for now" —
anchor a sentence to the moment of writing
and quietly assume a future edit
("still uncalibrated" reads as "uncalibrated until someone updates this sentence").
Write the plain present instead,
or pin the claim to a dated external artifact
when the point is that the known state has not moved.
Only the temporal sense is a smell —
logical uses are fine — so a hit is a prompt to reread the sentence,
not a verdict.

**Rewrite in place; do not append amendments.**
When a decision changes, the section that owns it changes,
so that the document reads true from top to bottom.
A section announcing that the above is amended as follows
turns the document into a patch series
the reader has to apply in their head.
The one legitimate two-state case is a decision taken but not yet built,
where the document really does describe both what exists and what will:
the target gets its own section naming what it supersedes,
each superseded section gets a one-line pointer forward,
and the instruction to merge them is written into the section itself.
Executing that merge is part of the change that implements the decision.

## A phrase that arrived ready-made was not chosen

Prose can be assembled from parts that come with the topic:
the obvious image, the word that sounds equal to the gravity of the matter,
the sentence added for the rhythm of the paragraph.
It reads smoothly and is not a choice —
nobody checked whether the image fits the thing
or whether the word predicates what it was meant to predicate.
The recurring patterns:

- **The worn metaphor.**
  An image used without a thought for its literal meaning
  stops being checked,
  and in technical prose it smuggles in mechanics nobody meant to claim.
  A fresh metaphor that does work stays.
- **The echo sentence.**
  A second sentence saying what the first said in other words,
  usually a plain version and a rhetorical one side by side.
  The better one stays, not both.
- **The intensifier with no content.**
  "Key", "crucial", "it is worth noting", "absolutely central"
  sound like information about weight and are often decoration.
  A statement of weight stays when it carries a decision
  ("the only rule that must not fire on human Polish");
  bare emphasis goes.
- **Ready-made officialese.**
  A nominalization where a verb would do,
  and a construction with no agent ("a decision was made", "it was agreed").
  Where an action has an actor, the actor is the content,
  so a sentence that drops it drops the next move along with it.
  A technical term doing its job is not decoration:
  "abstention", "false-positive rate", "type-token ratio" are precise and stay.
- **The contrastive frame.**
  A sentence taking its precision from what it excludes
  rather than from what it asserts:
  "X does Y, not Z", "the reading Polish does not have".
  Strike the negated half and read what is left standing.
  An exclusion somebody would actually propose survives that,
  since a subset is documented by exclusion;
  a foil invented to give the sentence a shape does not.
  Where what is left says nothing definite,
  the frame was doing the predicating and the verb under it was never chosen,
  so the repair is a sharper assertion rather than a shorter sentence.

Each pattern is a prompt to reread, not a verdict.
The test: strike the suspect word, parenthesis or sentence
and read the place without it.
If nothing was lost, the deletion stands,
and of two versions carrying the same content the shorter one is better.

Shorter does not mean telegraphic.
The other forces spend words deliberately:
repeated context buys a document that stands on its own,
and frame before detail buys comprehension.
The cutting applies to words that buy nothing.

## Dla kogo jest napisane zdanie

Reguła wyżej pyta, czy fraza została wybrana.
Ta reguła pyta o adresata: czy zdanie jest napisane dla kogoś,
kto ma z nim coś zrobić,
czy dla kogoś, kto ma docenić, że autor umie pisać.

Popis jest napisany starannie, więc tamten test go nie łapie.
Test jest tu inny: przepisz zdanie najprostszą polszczyzną, jaką umiesz,
i sprawdź, co ubyło.
Jeżeli ubyło samo wrażenie, zostaje wersja prosta.

Rejestr, który przeważa w tych dokumentach,
to stylizacja na esejistykę inteligencką.
Powtarza się w niej kilka chwytów.

- **Peryfraza w miejscu nazwy.**
  Zdanie omawia rzecz, którą umie nazwać.
  Najbardziej szkodzi w temacie commita i w nagłówku,
  bo tam zdanie czyta się bez akapitu pod spodem.
  Naprawą jest rzeczownik, a nie skrócenie zdania.
- **Wymyślony sprawca.**
  Reguła o urzędowej frazie wyżej gubi wykonawcę,
  a tutaj wykonawcą zostaje abstrakcja:
  pomiar rusza się sam, zdanie gubi role, dokument dostaje wskazanie.
  Skutek jest ten sam co przy zgubionym wykonawcy,
  czyli nie widać, kto ma co zrobić.
  Metonimia zwykła zostaje, bo dokument mówi i reguła żąda
  bez udawania, że któreś z nich czegoś chce.
  Wykreślamy dopiero to, co rzeczy przypisuje wolę albo doznanie.
- **Czasownik domowy.**
  „Stoi”, „trzyma”, „bierze”, „niesie”, „kosztuje”, „schodzi”
  obsłużyły już w tych dokumentach tyle znaczeń,
  że żadnego nie znaczą osobno:
  „stoi” zastępuje jest, obowiązuje, zależy i znajduje się.
  Czyta się to jak termin i nie jest zdefiniowane nigdzie.
  Test podstawieniowy: wstaw czasownik dokładny i sprawdź, czy zdanie zyskało.
  „Sklejenie stoi przed analizą” → „Sklejenie poprzedza analizę”.
  W nagłówku czasownik domowy szkodzi najbardziej,
  z tego samego powodu co peryfraza wyżej,
  a dokłada się do tego cena przemianowania,
  którą nazywa [reguła o liczbie w nagłówku](#pomiar-i-liczba-która-po-nim-zostaje).
  Test podstawieniowy obowiązuje tam od pierwszej wersji nagłówka,
  a nagłówek sekcji ruszanej z innego powodu liczy się jako ruszony,
  choćby jego wiersz nie wszedł do zmiany.
  Gdzie czasownik dokładny nie pasuje, nagłówek nazywa sam temat,
  a tezę sekcji piszesz w jej pierwszym akapicie.
- **Zdanie spakowane.**
  Autor wyrzuca z niego to, co czytelnik w zasadzie umie odtworzyć:
  granicę między dwoma zdaniami, powtórzony rzeczownik, powtórzony czasownik.
  Sam tego nie zauważa, bo zna treść i niczego nie odtwarza.
  Tędy biegnie granica cięcia z reguły wyżej:
  skreślone słowo, którego czytelnik nie odtwarza, jest zyskiem,
  a skreślone słowo, które musi odtworzyć, jest kosztem.
  Policz twierdzenia: w instrukcji ma być jedno na zdanie.
  Sygnałem są dwa człony spięte przez „a”, „więc” albo „i”,
  każdy z innym podmiotem.
  Sprawdź potem, czy któregoś rzeczownika albo czasownika
  nie trzeba wziąć z członu wcześniejszego, i wstaw słowo z powrotem.
  „Sprawozdania nie pisze się, a napisane skreśla każdy, kto je zauważy” →
  „Nie pisz sprawozdań. Sprawozdanie, które zastaniesz, skreśl”.
  Dwa takie skróty mają niżej własne nazwy.
- **„To” jako podmiot akapitu.**
  Zaimek odsyła do całego poprzedniego zdania, a nie do rzeczownika.
  Wstaw w miejsce zaimka rzeczownik.
- **Domyślne orzeczenie.**
  Sygnałem jest „tak samo”, „też” albo „odwrotnie” w miejscu orzeczenia.
  Kto wchodzi w środek, poprzedniego zdania nie przeczytał,
  więc powtórz czasownik, choćby zdanie wyszło dłuższe:
  „a zdanie, które i tak poprawiasz, tak samo” →
  „Te same reguły stosujemy do zdania, które poprawiamy z innego powodu”.
- **Jeden rytm na wszystko.**
  Trzy zdania pod rząd o tym samym kształcie —
  teza, przecinek, człon spięty przez „a”, „bo” albo „więc”,
  podmiot odłożony za orzeczenie —
  składają się na rejestr, w którym każde zdanie brzmi jak maksyma,
  więc żadnego nie da się już wyróżnić.
  Krótkie zdanie po trzech długich robi więcej niż „warto zauważyć”.
  Test: przeczytaj trzy kolejne zdania na głos.

Nie każde takie zdanie jest usterką.
Tekst, który się dobrze czyta, jest tu jednym z celów.
Granica biegnie między wywodem a instrukcją.
Wywód wolno tak pisać: README i te dokumenty, które o coś argumentują,
czyta się w jednym ciągu, i tam dobrze napisane zdanie się opłaca.
Instrukcji tak pisać nie wolno: ten plik, tematy commitów oraz `TODO.md`
mówią komuś, co ma zrobić.
Zdanie, które trzeba najpierw rozszyfrować,
dokłada mu pracy do tej, którą już ma,
a napisać je jasno trzeba raz.

Rejestr bierze się głównie z tego pliku,
bo każda sesja zaczyna od jego przeczytania i pisze potem jego głosem;
widać to w `git log --pretty=%s`,
gdzie tematy powtarzają jeden szyk i jeden niewielki zbiór czasowników.
Regułę przyjmujemy [leniwie](#reguły-przyjmujemy-leniwie) jak resztę,
a sekcję przepisywaną z innego powodu
sprowadzamy przy okazji do zwykłej polszczyzny.

## A claim about the world says how to check it

A sentence about the world outside the repository
either names what would settle it — a register, a document, a measurement,
your own observation — or it goes.
These documents are the ground for rule justifications,
so one unsupported sentence costs the credibility of the rest.

Two patterns produce most unsupported sentences:

- **The grading or excluding judgement** —
  "the best", "the largest", "the only", "typical".
  It sounds like a fact and is often an impression added for effect.
  A judgement with its grounds beside it stays; bare amplification goes.
- **Someone else's intention** — "wants", "plans", "aims to".
  What is checkable about another project is what it did:
  its code, its documentation, its published numbers.
  An interest somebody demonstrably has can be argued as your own reasoning;
  a plan attributed to them either goes
  or becomes an entry in an open-questions list.

A measured number carries what it was measured on.
"What this number is not" in [`docs/corpus.md`](docs/corpus.md#what-this-number-is-not)
is the reference example:
the figure and the reasons it cannot mean more than it does,
in the same place.

## Semantic line breaks

All prose here follows [Semantic Line Breaks](https://sembr.org) (sembr).
Instead of hard-wrapping at a fixed column
or putting each paragraph on one long line,
break lines at boundaries of meaning.

The rules, in order of precedence:

1. A line break must not change the rendered meaning of the text.
2. Insert a line break after a sentence.
3. Insert a line break after an independent clause
   punctuated by a comma, semicolon, colon, or em dash.
4. Optionally insert a line break
   after a dependent clause,
   a long phrase,
   or a list item.

Pojedynczy nowy wiersz zwija się w spację w Markdownie i w HTML-u,
więc czytelnik widzi to samo, a różny jest diff:
przeredagowane zdanie rusza tylko te wiersze, które naprawdę się zmieniły,
zamiast przelewać cały akapit albo dawać jeden wiersz nie do przeczytania.

Granicą reguły nie jest lista formatów, tylko warunek, który to zwijanie stawia:
proza w pliku wersjonowanym, a złamanie wiersza nie zmienia tego, co widzi czytelnik.
Markdown i zwykły tekst spełniają ten warunek tak samo jak akapit w HTML-u,
komentarz, docstring, ciało komunikatu commita i opis pull requesta;
wyliczenie to jest przykładami, a nie granicą.
Gdzie wiersz idzie dosłownie — `pre` i `textarea` w HTML-u, blok kodu w Markdownie —
łamać nie wolno, i mówi to pierwsza reguła wyżej.
Komentarz mieszczący się w jednym wierszu zostaje w jednym wierszu.
Samego kodu reguła nie tyka:
formatuje go zwykłe narzędzie danego języka.

Two mechanical consequences:

- Do not use two trailing spaces for a hard line break.
  Trailing whitespace is stripped here (see `.editorconfig`),
  so end the line with a backslash or start a new paragraph.
- Line-length linting is off (see `.markdownlint.jsonc`),
  because sembr line lengths are meant to vary.

## Where open work goes

Something noticed while working on another topic
belongs on a list rather than in the current change,
and which list follows from who closes the entry.
If a commit in this repository closes the entry, it belongs in [`TODO.md`](TODO.md),
whose header owns that boundary, the conventions for entries,
and what an entry is worth to whoever picks it up.
If the outside world closes the entry, it belongs in the list
in the document that owns the topic,
in [`docs/open-questions.md`](docs/open-questions.md)
or in a document's own `Not yet decided`.
The other list may carry a one-line pointer, and nothing more.

Alternatywy odrzuconej nie zamyka nikt, więc nie jest wpisem na żadnej z tych list.
Jest [wywodem o stanie dzisiejszym](#documents-describe-the-present-git-owns-the-past)
i należy do dokumentu, który jest właścicielem tematu,
razem z warunkiem, który ją odwraca.

## Splitting work across sessions

Several sessions can run at once,
and what decides whether they may is the judgment each one settles
rather than the files each one touches.
Two sessions editing one document cost a merge.
Two sessions answering one question cost the answer twice,
and the two answers need not agree,
which no merge tool reports and no test catches.

So a split names, per session, the decision that session settles —
what makes two derivations one reading, say,
which the docstring of `Node.signature` in `olski/parse.py` settles.
Where two come out the same, it is one session.
This is the demand [`TODO.md`](TODO.md) makes of a single entry —
that it name the evidence it reads and not only the files it changes —
applied to a batch of them.

A construction admitted alone pays the whole fixed cost of its own section —
the heading, the frame, the entry on the coverage list,
the clause in the stage plan — where several admitted together divide it,
so several may go into one session unless one of them blocks the others.
Several are also worth more together than apart,
because the probe prices each one against whatever else the grammar has,
so a position admitted alone can measure near zero
and hide that it is worth having
([docs/pisanie-po-olsku.md](docs/pisanie-po-olsku.md#zasłanianie-działa-w-obie-strony)).

A session is worth starting when one decision settles several entries.
An entry that cannot be settled until another session answers
is parked rather than parallelised,
and stays on the list with the blocker named,
so that whoever picks it up next does not start it cold.
The session that answers deletes the blocker,
because nothing rereads a parked entry until somebody picks it up.

Where two sessions both correct figures in one document,
split by the kind of number rather than by the section,
since a section is a place and a number has a cause:
one moves hit counts, the other denominators,
and whoever lands second reruns the tables.
Splitting by section reads as clean and is not,
because one decision reaches wherever its number went.

## Checks

```sh
pip install -e '.[dev]'
python3 -m pytest
ruff check .
npx --yes markdownlint-cli@0.45.0 '**/*.md'
```

Morfeusz 2 jest zależnością wykonawczą i instaluje się z PyPI,
więc instalacja edytowalna przynosi go razem z pytestem, ruffem
i parserem, którym harness czyta Markdown.
Gdzie jego wheel się nie buduje,
każdy plik testowy dochodzący do analizatora jest pomijany,
zamiast wywracać zbiórkę,
więc przebieg melduje testy stojące obok niego, a nie zero testów.
Pilnuje tego `tests/test_zbiórka.py`, bo dochodzi się tam
przez cudzy import i pominięcia brakującego nie widać w przebiegu z Morfeuszem.
Przebieg zielony w takim środowisku nie sprawdza niczego,
co do analizatora dochodzi, i widać to po liczbie pominięć.

[`.github/workflows/checks.yml`](.github/workflows/checks.yml)
uruchamia te same checki przy każdym pushu,
i to on sprawdza złożenie dwóch sesji, które się nie widziały.
Jego krok instalacyjny bierze Morfeusza z PyPI i wywraca zadanie, kiedy to zawiedzie,
więc ostatni commit gałęzi nie opiera się nigdy na samym przebiegu częściowym.
Lista poleceń wyżej i kroki workflowu są dwiema kopiami,
a `tests/test_docs.py` utrzymuje je równe,
więc check dopisany do jednej wywraca suitę, dopóki nie znajdzie się w drugiej.
Workflow nie nosi znaczka.

## Pomiar i liczba, która po nim zostaje

**Liczby kruchej nie wpisujemy do dokumentu.**
Krucha jest ta, którą zwykły rozwój projektu unieważnia:
ile zdań korpusu gramatyka przyjmuje, ile czytań daje konstrukcja,
ile zdań kupiła produkcja dopisana w zeszłym miesiącu.
Właścicielem takiej liczby jest narzędzie, które ją drukuje,
a nie akapit, bo akapit unieważnia się po cichu i nikt tego nie widzi.
Dokument mówi rząd wielkości, stosunek albo kierunek —
„przeszło sto zdań”, „nie odbiera ani jednego”, „kupuje kilkadziesiąt” —
bo takie zdanie zostaje prawdą, kiedy 148 robi się 151.
Kto chce liczby dzisiejszej, puszcza narzędzie.
Skąd wzięła się liczba w zdaniu napisanym kiedyś, mówi git.
Krucha nie jest przy tym liczba, którą rusza samo pobranie korpusu:
częstość formy w rejestrze, skład banku drzew i rozmiar słownika
mówią o korpusie przypiętym do wydania i zostają w pełnej precyzji.
Zejście z niej byłoby stratą, bo nikt jej nie przeliczy inaczej niż tym samym
pobraniem, a rozjazd z korpusem widać dopiero wtedy, gdy liczba jest dokładna.
Krucha nie jest też liczba sądów przeczytanych ręką:
mówi, ile ktoś przeczytał, a tego żaden przebieg nie przelicza ani nie unieważnia.

**Stosunek zgrubny rusza się tak samo, więc pisze się go granicą, a nie środkiem.**
`roughly one in twelve` w `docs/corpus.md` był taki
i przestał być prawdą przy jednym gospodarzu dopisanym do gramatyki,
bo stosunek jest tam liczbą powiedzianą inaczej i rusza go to samo.
Granica tylko się umacnia:
`better than one in eight` zostaje prawdą, kiedy jedna ósma robi się jedna siódma.
Po której stronie ją postawić, rozstrzyga pomiar, a nie życzenie.

**Nagłówek nie trzyma liczby, którą przeliczenie rusza,** bo nagłówek jest adresem.
`Złote czytanie ocalało w 613 z 673 zdań wieloznacznych` był taki,
a jedna zmiana w gramatyce przemianowała go, jego anchor
i siedem plików, które go linkowały,
z `tests/test_docs.py` wywracającym się na każdym po kolei.
W nagłówku wolno napisać rząd wielkości albo kierunek,
a stosunek wolno napisać zgrubny, bo dokładny rusza się jak liczba:
sekcja o złotym czytaniu w `docs/corpus.md` nosi
[sam kierunek](docs/corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).

Pomiary nie wchodzą do [bloku checków](#checks) i nie uruchamiają się przy pushu:
korpusy są archiwami dziesiątek megabajtów pobieranymi raz na sesję,
a runner pobierający je przy każdym commicie płaciłby za to raz na commit.
Wykonuje je więc ten, kto ma korpus, a suita nie startuje żadnego.

Przebieg czyta kod raz, przy imporcie,
a trwa dość długo, żeby zaprosić do puszczenia go i edytowania dalej.
Przebieg wystartowany przed edycją zmierzył kod z tamtej chwili,
dwa przebiegi za jedną komendą nie muszą mierzyć tego samego kodu,
a żaden z nich nie mówi tego w swoim wydruku.
Przeliczaj po ostatniej edycji, a nie obok niej.

**Zmianę, która ma tylko przyspieszyć, mierzy się na przemian i dowodzi odciskiem.**
Zegar maszyny rusza się między przebiegami o kilkanaście procent,
więc czas sprzed zmiany i czas po niej mówią tyle o zmianie, co o maszynie:
baza i zmiana idą naprzemiennie w jednej komendzie, a porównuje się sąsiednie pary.
Bazą jest drzewo robocze gita ze stanem sprzed zmiany (`git worktree add`),
bo oba katalogi stoją wtedy naraz,
a przełączanie gałęzi każe mierzyć jedno po drugim.
Że nie ruszyło się nic poza czasem, mówi odcisk całej prozy repozytorium:
werdykt, liczba czytań i punkt, na którym stanęło odrzucenie, zdanie po zdaniu.
Suita tego nie łapie, bo kolejność czytań i nazwę gospodarza sprawdza na garści zdań,
a rusza je każda zmiana porządku, w jakim rozbiór odwiedza produkcje.

Odcisk nad prozą pokazuje różnicę dopiero na zdaniu, którego werdykt się zmienił,
więc zmiana przestawiająca same produkcje potrzebuje odcisku samej gramatyki:
produkcje wraz z deklaracją wypisuje `harness/odcisk.py`.

**Blok wydruku stoi w dokumencie pod komendą, która go odtwarza.**
Rusza go to, co werdykt drukuje obok swoich liczb —
wiersz dopisany w `explain` w `olski/werdykt.py`
albo pole dopisane w `Deklaracja` w `olski/parse.py` —
i wtedy każdy taki blok bierze się ręką.
Który to blok, mówi `tests/test_wydruki.py`:
puszcza komendę stojącą nad wydrukiem
i żąda, żeby każdy wypisany wiersz komenda naprawdę drukowała.
Blok bez takiej komendy rozjeżdża się po cichu, więc go nie wklejamy.
Arytmetyki pod nim test nie widzi:
dokument mówiący, ile z czytań zdania werdykt wyjaśnia, liczy wiersze sam.

Zdania zacytowanego w backtickach nie pilnuje ani ten test, ani `tests/test_docs.py`,
a zmienia je dopisanie do gramatyki.
Werdykt i liczbę czytań każdego takiego zdania wypisuje `harness/cytaty.py`,
znów do porównania między dwoma drzewami roboczymi;
zdanie, którego werdykt się zmienił, czyta się potem wraz z akapitem nad nim,
bo dopisanie bywa naprawą tego zdania, a bywa unieważnieniem tamtego akapitu.

**Plik, który czyta sam kod, powstaje przebiegiem i nie poprawia się go ręką.**
`olski/leksykon.txt` jest leksykonem walencyjnym,
który `harness/walenty.py` wyprowadza z Walentego,
a `olski/skłonności.txt` tabelą skłonności,
którą `harness/skłonności.py` liczy nad Składnicą.
Polecenie i wejścia podaje przy pierwszym
[sekcja o leksykonie](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej),
a przy drugim
[sekcja o świadku](docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek).
Wpis dopisany do takiego pliku wprost ginie przy następnym przebiegu generatora,
a razem z nim ginie powód, dla którego go dopisano.
Jedną rzeczą różnią się na tyle, żeby wiedzieć to przed skasowaniem któregoś:
gramatyka czyta leksykon przy imporcie i bez niego nie startuje,
a brak tabeli skłonności czyni tylko warstwę nad nią milczącą.

Reguła ta obejmuje dane paczki, a nie każdy plik, który kod czyta.
`olski.toml` w korzeniu jest konfiguracją projektu i pisze się go ręką,
bo odpowiada on na pytania, na które nie odpowiada żaden korpus:
wedle którego leksemu odmienia się słowo, którego słownik nie ma,
oraz których lematów ten projekt używa, a których nie używa wcale
([`docs/subset.md`](docs/subset.md#leksykon-projektu-wpuszcza-polskie-słowo-którego-słownik-nie-ma)).
Ten plik nie ma generatora; przebiegiem wychodzą z niego formy, a nie wpisy.

## Code

**Prefer removing a branch to adding one, and unify divergent paths.**
Where callers differ only in where an input comes from,
push the difference to the edges
and route every caller through one branch-free core.
A branch is a second path to read, test and keep in sync;
a unified flow is proven once.

**Sondę różnicową puszcza się tam, gdzie liczba może ruch odwrócić.**
Wycenia ona konstrukcję, zdejmując jej produkcje;
prowadzi ją `harness/ruch.py`, gdzie stoją też warunki prawdziwości pomiaru.
Predykat pisze się w sesji, na jeden przebieg, i do drzewa nie wchodzi,
bo cena odpowiada na pytanie zadane raz — wpuszczać czy nie —
a rok później mierzyłaby już co innego.
Kto chce liczby dzisiejszej, pisze predykat na nowo i puszcza go;
kto chce tej sprzed roku, czyta commit, który konstrukcję wpuścił.

**Kod pyta o deklarację i nie trzyma jej drugiej kopii.**
Produkcję pyta i predykat sondy, i kod chodzący po gramatyce,
a nie listę nazw wypisaną obok niej,
bo lista milczy o produkcji dopisanej później.
Podzbiór deklaruje na nowo jeden program i jest to wybór z ceną:
co kupił `harness/polszczyzna.py`, mówi
[`design-notes.md`](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą),
a `TODO.md`, czy zostaje.

**Pozycja, której cena ma być osobną liczbą, musi być osobnym ciałem.**
Sonda mierzy zdjęciem produkcji,
więc kształt gramatyki rozstrzyga, co da się wycenić,
a nie tylko co się wyprowadza.
Symbol obejmujący dwie pozycje naraz oszczędza kilkanaście produkcji
i odbiera pomiar, bo zdjęcie jego ciał zabiera obie pozycje, a nie jedną.
Gdzie o cenę osobną nikt nie pyta, wybieramy symbol wspólny, bo jest tańszy.

**Plik dzieli się po tym, czym są jego kawałki, a nie po konstrukcji.**
O jednej konstrukcji mówią trzy miejsca i każde grupuje inaczej:
produkcje po gospodarzu, dokument po konstrukcji wraz z jej ceną,
a test po zdaniu, które przechodzi przez kilka konstrukcji naraz.
Podział zrobiony w tych trzech miejscach jednakowo
daje więc czwartą rzecz do utrzymania — mapę nazw między trzema drzewami —
a jej rozejścia nie łapie żaden check.
Każde z nich tnie się przez to osobno:
`olski/subset/` po warstwie, czyli po tym, co dany moduł deklaruje,
a `tests/` po tym, o którą warstwę test pyta.

**Printed output does not take its order from a set.**
String hashing is randomised at startup,
so a set walked in order to print something prints a different thing in every run,
and over a sentence truncated at `MAX_READINGS` it prints different readings.
One place fixes the order and everything downstream inherits it:
`ciała` in `olski/parse.py` does that for the forest,
and where a sort key can tie, the tiebreak is written into the key.
A single value picked out of a set is the same defect wearing one value
instead of many, and it hides better:
one line of output that changes between runs
reads as a difference in the input rather than as a coin toss,
which is how it survived in `Powtórzenie` in `olski/rozstrzyganie.py`
until a probe printed the same finding twice.

## Tests

Plain module-level `def test_*` functions with bare `assert`,
fixtures instead of setup and teardown methods,
and `pytest.mark.parametrize` instead of loops or copied cases.

A test's name says what is guaranteed,
which is why `test_an_annotated_sentence_with_no_morphology_is_reported_rather_than_dropped`
is worth its length.
A trivial test is worse than no test:
it costs a read, it has to be kept working,
and it demonstrates a property nobody doubted.
The tests worth writing are the ones
that would have caught a mistake somebody could plausibly make,
which is what `tests/test_subset.py` and `tests/test_segmentacja.py`
spend their length on:
a production that admits a phrase nothing should derive,
a segmentation graph stitched together one node out,
a lexical exclusion taking a reading the grammar needed.

A narrowing change leaves older conditions to re-check,
because one of them may now be guarded by nothing:
its test still passes, the new narrowing having taken over
the sentence that test rejects.
Take the older condition out and watch the suite go red;
where it stays green, that test wants a sentence
the new narrowing leaves alone.

## Commit messages

The subject says why, in the imperative;
the what is in the diff already.
Aim for 50 characters and treat 72 as the limit;
detail that does not fit goes in the body, in semantic line breaks.

Where the change is a name, a number, a threshold or a decision,
that word is in the subject.
A subject is read alone, in `git log --oneline` and in a list of pull requests,
so one that defers its content to the body has none:
`Nazwij po imieniu to, co tor składu robi`
announces that something was named and withholds the name,
where `Nazwij tor składu realizacją powierzchniową`
fits the same limit and says it.
Test: does the subject carry the word the body turns on?
If a change deliberately hands some information over to git history —
a deleted done-marker, a dropped section — the message says so
rather than implying nothing was lost.

## Git w sesji zdalnej

Klon w sesji zdalnej pokazuje historię obciętą albo nieświeżą.
`.git/shallow` ją ucina,
a ref zdalny pobrany przy starcie kontenera przestaje nadążać za gałęzią.
Obie przyczyny dają to samo złudzenie:
`main` długi na dwa commity, `git merge-base` bez wspólnego przodka,
`git log main..HEAD` wypisujący całą historię, jakby linie były rozłączne.
`git rev-parse --is-shallow-repository` wykrywa tylko pierwszą z nich,
a przy drugiej odpowiada `false`.
`git fetch --all` i `git fetch origin --unshallow` usuwają obie,
więc puść je, zanim oprzesz na refie wniosek o historii, diff albo squash.
Świeży klon nie jest tu wyjątkiem.

Przed squashem znajdź własny pierwszy commit, bo nazwa gałęzi,
której wartości nie sprawdziłeś, sięga czasem dalej wstecz, niż myślisz,
i wciąga wtedy w squash cudzy commit razem z jego autorstwem i komunikatem.
Po drzewie tej straty nie widać, więc łapie się ją tylko przed pushem.
Sprawdź potem, co przepisujesz:
`git log --oneline <baza>..HEAD` ma wypisać twoje commity i nic poza tym,
a diffstat tej bazy — tylko pliki, które ruszałeś.
Dopiero wtedy resetuj na `<pierwszy-commit>^`,
a po squashu `git diff <po-squashu> <dawny-head>` ma być pusty.

## Przegląd sprawdza zmianę wobec całego tego pliku

Poproszony o przegląd, spójrz świeżym okiem na to, co weszło w tej sesji.
Czytaj ten plik od góry i sprawdzaj zmiany regułą po regule.
Sprawdzaj to, co mogło się zepsuć:
sprawdzenie, które nie może wypaść źle, niczego nie dowodzi.
Drobne poprawki rób od razu,
a większe wpisuj do [`TODO.md`](TODO.md), zamiast je zaczynać.
Przed werdyktem puść [blok checków](#checks).

Lista niżej nie dokłada reguł i żadnej z nich nie streszcza
([jeden właściciel](#one-owner-per-fact-repeat-narrative-freely)).
Zbiera pytania, które zadaje się przy przeglądzie,
a których nie zadaje żadna sekcja wyżej.

- **Kierunek.** Czy zmiana idzie w dobrą stronę?
  Problem nie musi zniknąć od razu.
  Wystarczy, że umiesz powiedzieć, czemu po tej zmianie jest do niego bliżej.
  Zmiana, która tylko przestawia tekst, nie idzie nigdzie.
- **Czyja ścieżka.** Kto przeczyta zmienione miejsce
  i czy nadal znajdzie tam tekst dla siebie?
  Role opisuje [`docs/roles.md`](docs/roles.md).
- **Elegancja.** Czy rozwiązanie jest proste?
  Kod testów ma być tak samo prosty.
  Które testy są warte pisania, mówi [sekcja o testach](#tests).
- **Uczciwość.** Czy to miejsce mówi prawdę o tym, co robi?
  Czy ktoś, kto tu wejdzie za pół roku, zrozumie je bez pytania?
- **Komentarze.** Czy w kodzie nie ma ich za dużo?
  Który komentarz zarabia na siebie, mówi
  [reguła o jednym właścicielu](#one-owner-per-fact-repeat-narrative-freely).
- **Co się otworzyło.** Czy da się teraz uprościć coś,
  czego wcześniej nie dało się ruszyć?
  Drobiazg zrób od razu, większe wpisz do `TODO.md`.
- **Listy i dokumenty.** Co dopisać, a co skasować —
  w `TODO.md`, w tym pliku, w README, w `docs/`?
  Wpis, który ta zmiana zamyka, kasujesz
  ([dokument opisuje teraźniejszość](#documents-describe-the-present-git-owns-the-past)),
  a wpis zamknięty w połowie przepisujesz na to, co z niego zostało.
- **Nagłówek.** Przeczytaj sam nagłówek każdej ruszonej sekcji
  i powiedz, czego się pod nim spodziewasz.
  Czytasz od miejsca, w którym zaczęła się edycja, a nagłówek jest nad nim,
  więc bez tego pytania nie przeczyta go nikt.
  Jaki nagłówek jest zły, mówi
  [dla kogo jest napisane zdanie](#dla-kogo-jest-napisane-zdanie).
- **Poza zasięgiem suity.** Czego `tests/test_docs.py` nie sprawdzi:
  nazwy napisanej bez backticków, nazwy sekcji
  ([na czym wolno oprzeć zdanie](#na-czym-wolno-oprzeć-zdanie))
  i przykładu, który przestał pasować do reguły cytującej go.
  Poszukaj ich grepem, kiedy coś kasujesz albo przemianowujesz;
  `TODO.md` też nazywa pliki i sekcje.
- **Złamana reguła.** Czy zmiana łamie którąś regułę celowo?
  Wtedy zła jest reguła.
  Popraw ją tym samym commitem — tutaj, w README albo w nagłówku `TODO.md`.
- **Werdykt.** Ciągniemy dalej, zamykamy jak jest, czy wycofujemy całość?
  Z uzasadnieniem.
