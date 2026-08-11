# Work to do in the repository

The running list of work inside the repository itself:
rewrites, merges, documents that have drifted apart,
dangling references, gaps, and code worth improving.
Something noticed while working on another topic lands here
instead of stretching the current change or being forgotten.
The second inflow is [the review pass](CLAUDE.md#the-review-pass):
a refactor too large to do on the spot comes down to this list,
and the review also checks whether a change deleted the entries it closes.
Look here before starting new work —
the list doubles as a map of the places that sag.

Lista nie mówi jednak, w który tor praca idzie.
Wpis jest notatką po tym, na co ktoś przy innej robocie trafił,
a nie kolejką, którą się odbiera po kolei,
i rozstrzyga to [docs/roadmap.md](docs/roadmap.md#co-jest-budowane).

An entry belongs here only if a commit in this repository closes it.
A question the outside world answers —
a measurement, which human Polish counts as the good half of the corpus,
a fork not yet taken —
is not work in the repository,
and the document that owns the topic keeps it:
[`docs/open-questions.md`](docs/open-questions.md)
or a document's own `Not yet decided`.
The next move is the tell:
waiting for somebody else's answer is an entry there,
a file to write is an entry here.

A register, not a changelog:
an entry that closes, or that turns out to have been misjudged,
is deleted by the same commit that settles it,
which is the done-marker rule from
[`CLAUDE.md`](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
applied to this file.

One paragraph per entry, paragraphs separated by a blank line,
without bullets, numbering or headings,
so that adding or removing an entry gives a clean diff
and leaves its neighbours alone.
An entry that names another one names it by what it is about,
because that is all there is to name it by:
a pointer saying which way to scroll is wrong
as soon as anything lands between the two.
Inside a paragraph the lines break
[semantically](CLAUDE.md#semantic-line-breaks).
Write so that the entry can be picked up cold,
and name the concrete next move —
what actually has to change in the text or in the code.
"Check some day" is a hope, not a move.

An entry names the evidence it has to read,
and not only the files it changes,
because two entries editing disjoint files
can still turn on one judgment about one body of text,
which a file list does not show.
What that costs is
[splitting work across sessions](CLAUDE.md#splitting-work-across-sessions).

Wpis nie jest rozstrzygnięciem.
Po to ta lista jest: kto go pisał, siedział wtedy przy czymś innym,
a notatka dostała tyle uwagi, ile zostało.
Pewne jest w takim wpisie to, że autor na coś trafił,
a nie to, że dobrze zgadł, co z tym zrobić.
Kto wpis podnosi, dochodzi więc do ruchu sam:
zaczyna od dowodu, który wpis nazywa,
a nazwany ruch czyta jako propozycję, a nie jako polecenie.
Wychodzi z tego czasem ruch inny niż nazwany, a czasem żaden,
bo problemu nie ma albo naprawa kosztuje więcej niż to, co kupuje.
Wtedy całą zmianą jest skasowanie wpisu, z powodem w komunikacie commita,
bo nic innego po nim nie zostaje.

---

Werdykt nad zdaniem o kilku nierozstrzygniętych przyłączeniach nie mówi,
o które przyłączenia idzie, i nie zdejmie tego szybsze wyliczanie.
`explain` w `olski/subset.py` nazywa role, które się między czytaniami różnią,
a `describe` w `olski/parse.py` bierze pierwszy węzeł roli, a nie wszystkie,
więc ta sama para nazw wychodzi nad zdaniem o dwóch przyłączeniach i o sześciu,
gdzie liczba stoi już urwana o `MAX_READINGS`.
Do przeczytania jest wyjście dwóch poleceń,
wraz z odrzuconym wyjściem tańszym, które te polecenia stawiają pod nosem,
i trzyma jedno i drugie
[`docs/design-notes.md`](docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań).
Ruchem jest parser tablicowy nad lasem ze współdzielonymi węzłami,
w którym nierozstrzygnięte przyłączenia są osobnymi spakowanymi węzłami,
a nie iloczynem drzew,
i werdykt wskazuje przyimek wraz z głowami, do których dochodzi.
Warunkiem, bez którego las na to pytanie nie odpowie,
jest pakowanie po sygnaturze czytania, a nie po środowisku cech;
`analyses` w `olski/parse.py` tę dyscyplinę już trzyma i trzeba ją zachować.
Sama ona nie wystarcza, a na czym liczba ma stanąć zamiast iloczynu,
pyta wpis o sumie iloczynów, i idzie on przed tym,
bo rozstrzyga, co ten parser pakuje.
Zmiana nie rusza ani jednej produkcji,
więc sprawdza się ją werdykt po werdykcie wobec tego, co stoi,
nad prozą README i nad Składnicą.
Zamyka to wpis o głębokości zagrzebania złotego czytania,
bo dopiero po lesie jest po czym chodzić.
Otwiera przy tym dwie rzeczy, i to są dwie osobne sesje, a nie część tej.
Zakaz lewej rekursji przestaje wiązać,
a na nim stoi „nic ponad współrzędnością się do niej nie rozdziela”
z [`docs/subset.md`](docs/subset.md#nothing-above-a-coordination-distributes-into-it):
zawężenie jest tam obronione na własnych prawach,
więc po lesie staje się wyborem i trzeba je przeargumentować, a nie odziedziczyć.
I `--max-tokens`, którym `olski-corpus` omija zdania, na jakie enumeratora nie stać:
liczenie czytań bez wyliczania ich powinno ten próg podnieść,
a o ile, jest do zmierzenia, a nie do założenia.

Werdykt nad zdaniem mówi, na czym odrzucenie stanęło, a przebieg nad korpusem zgaduje.
`licencjonuje` w `olski/grammar.py` odpowiada na to wyprowadzone z gramatyki,
i `olski-check` tę odpowiedź nad zdaniem wypisuje,
gdzie `blocker` w `olski/coverage.py` nazywa część mowy pierwszego czytania formy
i sam w docstringu mówi, że między czytaniami wybiera dowolnie,
więc kolejka z [`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)
jest rankingiem stojącym na tym wyborze,
choć ten dokument opisuje ją jako listę słów, których żadna produkcja nie bierze.
Ruchem jest wycięcie czytań bez licencji przed rozbiorem,
po którym forma bez ani jednego czytania jest dla `blockera` brakiem licencji,
a nie brakiem struktury, którym ją dziś nazwie.
Samo wycięcie nie rusza ani jednego werdyktu i wywód na to trzyma
[`docs/design-notes.md`](docs/design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej).
Rusza za to kolejkę, więc wpis jest winien przebiegi,
których [sekcja Checks](CLAUDE.md#checks) żąda od zmiany w czytaniach,
jakie gramatyka dostaje.
Do przeczytania jest, ile ta kolejka na tym się zmienia,
i tę różnicę trzeba przeczytać przed wybraniem korpusu:
złota morfologia zostawia bank drzew bez ani jednej formy nieznanej,
więc tam wycięcie nie rozdzieli niczego,
a nad prozą README brak w słowniku stoi w tej kolejce zaraz za przecinkiem.
Zostaje przy tym pytanie, którego werdykt nad zdaniem nie zadaje:
`olski-check` mówi o zdaniu, a nie o pliku,
więc rankingu form bez licencji nad dokumentem nie wypisuje nikt,
i do rozstrzygnięcia jest, czy jest to wiersz tej komendy, czy tryb obok niej.
Czytelników takiego rankingu jest już dwóch:
[kolejka nad rejestrem ustaw](docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
jest wzięta potokiem z grepem, który ten dokument drukuje,
bo nie ma komendy, która by ją wypisała.

Suma iloczynów po lesie rozbiorów liczy pary, których unifikacja nie przepuszcza,
i nie widać, które z dwóch wyjść jest tańsze.
Zdanie, które to pokazuje, mechanizm i oba wyjścia trzyma
[tożsamość czytania](docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania).
Ruchem jest przebieg nad prozą README i nad Składnicą,
bo rozstrzyga między tymi wyjściami to,
ile pozycji rozszczepienie naprawdę rozdziela,
a rozdziela je dopiero forma stojąca w zdaniu.
Nadmiar ma przy tym gotową pułapkę:
zdanie z tamtej sekcji stoi w `PRZYJMOWANE` w `tests/test_subset.py`,
więc las liczący iloczynem przewraca test, a nie samą liczbę.
Wpis stoi przed wpisem o parserze tablicowym, bo rozstrzyga, co ten parser pakuje.

Szyk zdania stoi w produkcjach wypisany, a kupuje go rozdzielenie dominacji
od precedencji.
`build` w `olski/subset.py` ma kilkanaście produkcji `ClauseConjunct`,
bo każdy szyk wypisuje się osobno,
a każdy jeszcze raz w tylu wersjach, ile ma miejsc na okolicznik,
i to jest ta część gramatyki, która przy każdej nowej konstrukcji rośnie mnożąc się.
Pomiar, od którego się tu zaczyna, wylicza
[subset.md](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie):
pozycje na wyrażenie przyimkowe i produkcje, w których stoją.
[Sonda](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą) zmierzyła,
że po stronie więzów SVO i OVS są jedną deklaracją, a okolicznik trzema,
i że nie potrzeba do tego ani innego podłoża, ani innej klasy złożoności:
dominacja rozdzielona od precedencji jest
[szczeblem 1](docs/design-notes.md#the-cost-ladder),
i tak samo radzi z tym GPSG,
co [kąt parsujący](docs/design-notes.md#angle-one-parsing) już wylicza.
Ruchem jest produkcja mówiąca, jakie są córki, wraz z osobnymi warunkami
precedencji, i preprocesor rozwijający jedno w drugie przed parsowaniem.
Miejsce jest przy tym drugie i dochodzi się do niego inną drogą.
`NPConjunct` ma osiem ciał, z czego sześć jest iloczynem
trzech kształtów głowy przez obecność `Modifier` po niej,
i mnoży to nie permutacja argumentów, tylko obecność i kolejność
rodzajów przydawki, więc etap 4 dołoży tam trzeci rodzaj, a nie czwarty szyk.
`Adjuncts` w tym samym pliku się nie mnoży, bo okoliczniki są jednego rodzaju.
Pułapka na tej drodze jest jedna i leży poza gramatyką.
Pozycja opcjonalna zwija się produkcją pustą, taka produkcja dziś się parsuje,
ale `Node.span` w `olski/parse.py` sięga po `children[0]`,
więc pusty węzeł wywraca każdego, kto o rozpiętość zapyta,
a niezmiennika „węzeł ma dziecko” nie pilnuje nic.
Kupuje to jeszcze jedną rzecz, którą sonda pokazała mimochodem:
szyk wykluczony z olskiego przestaje być wykluczony brakiem produkcji.
Do przeczytania jest, co ten preprocesor robi z liczbą czytań,
bo permutacja dopisana przez rozwinięcie jest czytaniem tak samo jak każde inne,
a próba nad prozą README stoi w `sonda/` gotowa do porównania.
Tego pytania nie ma czym przeczytać nad listą czytań urwaną o `MAX_READINGS`,
więc wpis o parserze tablicowym nad lasem idzie przed tym.
Blokerem nie jest już leksykon walencyjny,
bo to on kasuje czytania, które rozwinięcie permutacji dopisuje,
i mówi o tysiącach lematów, a nie o samej kopuli;
ile ich jest, trzyma
[`docs/subset.md`](docs/subset.md#leksykon-mówi-dwa-zdania-na-lemat-i-bierze-je-z-walentego).
Tym samym ruchem sonda się wycofuje:
`sonda/polszczyzna.py` jest drugą deklaracją tego samego podzbioru,
czyli tym drugim właścicielem faktu, przed którym broni
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely),
i pilnuje jej tylko siedem zdań z `tests/test_sonda.py`.
Te dwie deklaracje już się rozeszły na koordynacji przecinkiem:
olski bierze przecinek na trzech poziomach, a sonda spójnik,
i nad prozą README nie widać tego po żadnej liczbie.
Póki liczby z niej cokolwiek trzymają, kopia zarabia na siebie;
kiedy szyk zejdzie do warunków precedencji i zostanie zmierzony,
przestaje, i wtedy idzie
`git rm sonda/__main__.py sonda/polszczyzna.py sonda/wiezy.py`
wraz z `tests/test_sonda.py`,
z figurami tamtej sekcji i z wierszem o niej w [sekcji Checks](CLAUDE.md#checks).
Katalog zostaje, bo `sonda/przecinek.py` jest osobną sondą wokół osobnej decyzji,
i zostaje z nim nazwa `sonda` w `SOURCES` z `tests/test_docs.py`.
Zostaje z sekcji to, co figur nie potrzebuje:
że nieciągłość jest warunkiem zdejmowanym, a nie szczeblem,
i że jednoznaczność bywa osiągana bez trafności.

Liczba pozycji na `Modifier` w `sonda/polszczyzna.py` nie ma wyprowadzenia.
Komentarz przy więzach okolicznika mówi „trzy deklaracje zamiast jedenastu pozycji”,
a jedenastu nie daje żaden sposób liczenia produkcji `build` w `olski/subset.py`,
jakim udało się tę liczbę odtworzyć:
córkę `Adjuncts` albo `Modifier` ma szesnaście produkcji,
samo `Modifier` stoi w siedmiu z nich,
a produkcji `ClauseConjunct` z okolicznikiem jest osiem.
Regułę liczenia rozstrzygnęła po swojej stronie
[`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie):
liczy produkcje, i te, które zdejmuje, mierząc, co pozycje przyłączenia kupują,
czyli okolicznik stojący obok czegoś jeszcze
albo wyrażenie dochodzące do frazy, która już coś przy sobie ma,
i wychodzi ich dwadzieścia jeden.
Ruchem jest przepisanie komentarza na regułę i liczbę,
przy czym sonda liczy miejsca w zdaniu, a tamten dokument produkcje,
więc albo przejmuje tę regułę, albo mówi, czemu liczy co innego.
Bez reguły żadna zmiana w gramatyce nie umie tej liczby ponieść,
a [sekcja Checks](CLAUDE.md#checks) każe ponieść figury sondy razem z gramatyką.

Rama mówi, co czasownik bierze, i nie mówi, ile tego bierze.
Dopełnień stoi przy czasowniku najwyżej jedno,
bo tyle stoi w ciele każdej produkcji `Complements` w `olski/subset.py`,
a nie dlatego, że rama tak mówi;
ruchem jest rama zużywana, czyli ta,
[którą pokazuje Świgra](docs/swigra.md#valency-as-a-resource-that-gets-consumed):
pozycja zajęta znika z tego, co niesie reszta grupy.
Wolno ją wyrazić cechą o dziedzinie skończonej,
bo pozycji jest w ramie skończenie wiele,
więc rozwinięcie idzie przed parsowaniem i nie rusza klasy złożoności.
Kupuje to jednak dokładnie tyle, ile jest ram o dwóch pozycjach naraz, a takich nie ma:
biernik z bezokolicznikiem naraz zmierzono i nad Składnicą pod złotą morfologią
przyjmuje 289 zdań zamiast 293, a wieloznacznych ma 116 zamiast 110,
bo grupa imienna za bezokolicznikiem dochodzi wtedy i do niego, i do formy osobowej.
Wpis czeka więc na pozycję, która z inną naprawdę stoi,
czyli na dopełnienie w celowniku obok biernika — `dać uczniowi książkę` —
którego produkcji olski dziś nie ma;
bez niej mechanizm rozwija się na jedną pozycję i nie liczy niczego.

Nothing in the harness says which construct a finding came out of,
so every audit of extracted prose maps its hits back by hand.
`docs/extraction.md` did it for a couple of hundred spacing findings,
and [the audit corpus's tables](docs/firing-rates.md#what-the-hits-over-the-audit-corpus-turned-out-to-be)
for several hundred more,
both with a throwaway script and neither with anything reusable.
The classes that cost the most to reach are the ones a program could settle:
whether a hit stands in a code span or in a link's text,
which is what the two largest non-defect classes over the audit corpus are.
The parser hands that over already —
every stretch of a paragraph comes out of a node with a type —
so the move is for `prose` in `harness/markdown.py`
to keep the type beside the characters it produced,
and for something to print it beside a finding.
That is a second output from the extraction
and wants deciding whether it rides along with the prose files
or is a separate mode over one document.
What the parser does not hand over is where in the source the node was:
a block token carries a line range and an inline token carries nothing,
so a mode that prints the source line as well
is a second pass over the document rather than a field to pick up.
Against it: the classes that decide whether a hit is a *defect*
are the ones needing a reader anyway,
so this halves an audit rather than removing it,
and a corpus of this size can be read by hand, as it twice already has been.

`docs/extraction.md` compares one member of the audit corpus against its files
and the corpus has two.
Its table runs the notes, the memoir and `ksef-docs` twice each,
where [`docs/firing-rates.md`](docs/firing-rates.md#the-audit-corpus)
audits `rit-dokumentacja` beside `ksef-docs`
and finds that member losing three fifths of its Markdown to the extraction,
which is the case the table has no column for.
The move is a fourth column,
which means running `rit-dokumentacja` with its names changed to `.txt`
and checking the spacing findings one by one against their source
the way the section's own method demands,
since a count that agrees is not yet a hit that points at the same place.

Only one of the corpora in
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken)
reaches the rules through a program this repository holds.
`harness/markdown.py` reads Markdown,
which is what the KSeF figures there are taken with,
while NKJP is XML, Śmigiel is JSONL,
`python-docs-pl` is PO files and Wolne Lektury is plain-text exports,
so every figure over those is still counted by hand.
One of the four needs no extraction at all,
since a text export is what olski reads,
and what it needs instead is a selection anybody can repeat:
the Wolne Lektury count in that document
runs over "the first forty `Epika` entries the catalogue returns",
which is not an order to rerun into.
[`docs/firing-rates.md`](docs/firing-rates.md#wolne-lektury)
already fetches the same library by naming every slug it takes,
so that half is a rewrite of one paragraph rather than a program.
The move is to decide, per corpus, whether it joins the harness
as an extraction beside the Markdown one,
as a fetch-and-select command in the document that cites it,
or not at all because the survey has already ruled the corpus out.

Uzasadnienie reguły jest prozą, której nie czyta żaden check.
[Reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
liczy pole `justification` deklaracji do prozy,
dokładnie tak jak liczy docstring i komentarz,
a `tests/test_docs.py` puszcza przez linter dokument i jednostkę modułu,
i nie puszcza żadnego uzasadnienia,
bo [ekstrakcja nad modułem](docs/prose-in-code.md) czyta docstringi i komentarze,
a uzasadnienie jest łańcuchem pod kluczem i tędy nie wychodzi.
Ruchem jest wzięcie ich stamtąd, skąd bierze się je do raportu,
czyli z `load_packs()`, a nie z tekstu pliku:
`_fold` w `olski/rules.py` składa je do jednego akapitu przed użyciem,
więc do lintera trafiłoby to samo, co czyta ktoś, kto raport dostaje.
Do rozstrzygnięcia jest przy tym, co takie uzasadnienie wybiera:
czy idzie za wpisem swojego modułu na [liście](tests/nie-po-polsku.txt),
czy deklaracja jest tu jednostką osobną od pliku, w którym stoi.
Do przeczytania jest to, co pakiet zgłasza nad tymi polami,
bo wszystkie stoją po angielsku,
a nad angielszczyzną ten check jest deklaracją, a nie sprawdzeniem.

A run says which files a format made a rule decline, and not which ones the text did.
`_note_markup` in `olski/cli.py` prints one line
when a whole-file rule declined on a file in a format olski does not read,
because a run over Markdown would otherwise read as a run over prose
that happened to find less.
A refusal the text caused is followed by the same silence:
`olski notatka.txt` over a file under `em-dash-density`'s word floor
prints no finding and no notice,
and only `--format report` or `--show-abstentions`
shows that nothing was measured.
The move is a decision about how much the default mode says —
a notice for every refusal a run tripped,
which is `--show-abstentions` in summary,
or the format notice alone,
on the grounds that a reader can see how long their own file is
and cannot see what a suffix promised on its behalf.

Raport nie odróżnia dwóch czytań, które różni samo miejsce przyłączenia.
`Koszt samej szynki przewyższa koszt szynki z dodatkami.` ma sześć czytań,
a `describe` w `olski/parse.py` streszcza je rolami z `ROLES`,
więc dwie pary wychodzą z tego identyczne:
`z dodatkami` dochodzi raz do `koszt`, a raz do `szynki`,
i w obu przypadkach dopełnieniem jest ten sam `koszt szynki z dodatkami`,
a modyfikatorem ten sam `z dodatkami`.
Jest to dokładnie to rozróżnienie, dla którego
[te pozycje](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)
w gramatyce stoją.
Ruchem jest nazwanie w streszczeniu tego, do czego modyfikator doszedł,
czyli rozpiętości albo roli węzła, pod którym stoi;
`Node` w `olski/parse.py` niesie rozpiętość, więc jest to pytanie o wydruk,
a nie o parser.
Do rozstrzygnięcia jest, czy `ROLES` zostaje listą ról,
skoro to, co trzeba dopisać, rolą nie jest.

`docs/corpus.md` and `docs/corpora.md` differ by two letters
and hold unrelated things:
the first measures the grammar against the Składnica treebank,
the second surveys the corpora the linter would calibrate against.
A link to either one reads the same,
and a grep for one of them finds both,
and finds `docs/audit-corpus.md` too,
which is about one of the corpora the second surveys.
The move is to rename `docs/corpus.md` to `docs/skladnica.md`,
which says what it holds and matches `docs/swigra.md` beside it,
and to carry the rename through every file that names it.
`tests/test_docs.py` catches the Markdown links and the citations in code,
and nothing catches the plain-prose mentions,
so those are the ones to grep for.
That name lands beside `docs/sklad.md`, which is the compiler and not the treebank,
so a grep for `sklad` finds both,
and the pair this entry is about becomes that one.
The package has the same collision twice over and the same argument settles it.
`olski/check.py` is the grammar command
and `olski/checks.py` is the linter's check kinds,
one letter apart and on opposite tracks:
[`docs/roles.md`](docs/roles.md) sends the grammar reader to the first
and [`docs/rules.md`](docs/rules.md#check-kinds) sends the rule author to the second,
and the two already stand a few lines apart in this file.
`olski-corpus` is the third: it runs `olski/coverage.py`,
where `olski/corpus.py` is the treebank reader beside it,
so the command, the module and the document
are three names for what a reader takes to be one thing.
Renaming the document alone leaves both of those in place,
which is why they are one entry:
what has to be decided is what these things are called,
and the answer for the document is the answer for the module and the command.
The entry about the harness boundary reaches the third of them on its own grounds,
since one of the two answers it offers moves the treebank reader to `harness/`
and takes the command along as `python3 -m harness.coverage`,
which leaves nothing there to rename,
so whichever entry is picked up first is answering for the other.

The check table in `docs/rules.md` copies data owned by `olski/checks.py`.
Its `Reports` column restates what each check's `fields` answers,
and the `params=dict(...)` blocks restate what each validator accepts,
so both drift silently as soon as a check gains a parameter.
`fields` is a function of a rule's validated parameters,
which the `pattern-density` row carries as a condition in prose,
so whichever move is picked reaches a check's fields through some rule's parameters.
Either the CLI grows a `--list-checks` output that the document points at,
the way it already points readers at `--list-rules`,
or the table stays hand-written and a test asserts it against `CHECKS`,
the way `tests/test_docs.py` holds the links in the prose.
Pick one and the document stops being a second copy.

Czytelnik Składnicy gubi węzeł bez słowa w dwóch miejscach,
a gubi go z drzewa, na którym stoi zgodność ról, a nie samo przyjęcie zdania.
`_gold` w `olski/corpus.py` pomija dziecko, którego `nid` do niczego nie prowadzi,
a `NIEWYBRANY` wycina węzły, którym `chosen` przeczy,
i stoi na tym, że format tak to znaczy, a nie na sprawdzeniu.
Łapie oba jedno kryterium: terminale wybranego drzewa
mają pokrywać rozpiętość korzenia bez dziur i bez zakładek.
Nad wydaniem 2018 żaden las z werdyktem `FULL` mu nie przeczy,
a lasy bez werdyktu przeczą mu masowo,
bo tam `_root` schodzi do najszerszego wybranego węzła i znajduje fragment,
więc kryterium obejmuje `annotated` i nic poza tym.
Do rozstrzygnięcia zostaje, co ma się stać z lasem, który mu przeczy:
przerwać przebieg czy wejść do niemierzonych obok zdań dłuższych niż `--max-tokens`,
i to drugie żąda wiersza w wydruku, którego pierwsze nie żąda.
Sprawdzianem do napisania obok jest las, który kryterium łamie,
bo `tests/test_corpus.py` pisze lasy ręcznie i taki też napisze.

`olski-corpus` asks Składnica whether a sentence derives at all,
where the same treebank supports a sharper question.
Świgra's evaluation walks its packed forest per sentence
and counts the trees consistent with the corpus disambiguation
(see [`docs/swigra.md`](docs/swigra.md#failure-is-diagnosable-and-coverage-is-measured-against-gold)),
so coverage becomes whether the gold reading is among the readings
and how deeply it is buried,
rather than whether anything came out at all.
This is ordered behind the entry about the verdict that names no attachment,
whose move is the chart parser and the packed forest,
because the enumerator builds no forest to walk
and caps enumeration at `MAX_READINGS`,
which is exactly the tail a burial-depth number would be measuring.

The archives these documents send a reader to fetch are pinned by URL and by nothing else.
[Składnica](docs/corpus.md#fetching-it)
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
name a release in the query string of a wiki attachment,
and Świgra is `swigra_current.zip`, which names none,
so [`docs/swigra.md`](docs/swigra.md#what-was-read-and-what-was-not)
dates it by the timestamps of the files inside instead.
[The audit corpus](docs/audit-corpus.md#the-list) pins its members to a commit
and says what a pin is for:
so that a second person fetches the same bytes.
The archives make that promise
and give a reader no way to hold anyone to it.
The move is `sha256sum` over each one,
with the digest beside the command that fetches it,
which turns a substitution upstream into a failed check
rather than a figure that quietly stops reproducing.

The corpora these documents send a reader to fetch
come from hosts that gain nothing by serving them,
once per session rather than once per person,
because a Claude Code session on the web starts from an empty container.
[The Wolne Lektury run](docs/firing-rates.md#wolne-lektury)
takes 326 files at one request each from a volunteer library,
[Składnica](docs/corpus.md#fetching-it) is 92 MB
that [the checks](CLAUDE.md#checks) make a condition of touching the grammar,
and [NKJP](docs/corpora.md#the-national-corpus-of-polish)
is a tarball from the institute that serves Składnica.
The licences do not run in that order.
NKJP carries CC BY, which permits the redistribution a mirror is,
every Wolne Lektury file ships the library's licence in its own tail,
which that run cuts off before counting,
and Składnica is GPL,
which the fetching section raises against vendoring
and which settles nothing about mirroring,
since a mirror redistributes under Składnica's terms
whatever this repository decides about its own.
So the order of work is NKJP, Wolne Lektury, Składnica,
and the transport is the smaller half of each.
A release asset on a mirror repository holds 2 GB per file against no quota
and keeps the fetch the `curl -L` those sections print,
where git LFS asks for an install that the session clone precedes
and spends an allowance that GitHub's billing documentation puts at
1 GB stored and 1 GB of bandwidth a month, which is ten fetches of Składnica.
LFS buys that back over a binary somebody versions, and these are frozen archives.
The audit corpus needs none of it,
being clones pinned to a commit, which is what a mirror would be.
None of this starts before the entry on digests,
since a mirror nobody can check against upstream
is the second copy of a fact that
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely) warns about.

The repository ships no licence.
`pyproject.toml` carries no `license` field and there is no `LICENSE` file,
so the terms under which any of this may be used are unstated.
The move is to pick one, add the file,
and set `license` in `pyproject.toml` to match.
Reading a GPL v3 parser of Polish is what raised it
(see [`docs/swigra.md`](docs/swigra.md#why-wrapping-it-does-not-get-there)),
and the answer decides whether olski could ever link against such a thing.

[Semantic line breaks](CLAUDE.md#semantic-line-breaks) cover
"prose in comments and docstrings", and the code is divided about it.
`skład/`, `opowieści/`, `olski/walencja.py` and `harness/ustawy.py`
break their comments at boundaries of meaning,
and everything else in `olski/`, `harness/` and `sonda/` wraps to a column.
The division follows neither track nor language:
`olski/walenty.py` and `olski/wieloznaczność.py` wrap to a column
though both stand in Polish
and both sit beside `olski/walencja.py`, which does not.
Two ways out, and the choice is a judgement about the whole package
rather than about whichever function is being edited at the time:
narrow the rule in `CLAUDE.md` to Markdown, commit messages
and the prose fields of a declaration,
which is where the tighter diff is actually collected,
or keep the rule and reflow the rest under
[lazy adoption](CLAUDE.md#adopt-these-rules-lazily), file by file as they are touched.
Narrowing costs a second rule as well:
[the language rule](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
reaches comments and docstrings
by pointing at semantic line breaks for what counts as prose,
so narrowing them out there takes them out of Polish too,
and it leaves the modules that already break semantically
keeping a habit `CLAUDE.md` no longer asks for.

`docs/subset.md` jest dokumentem mieszanym i przez to stoi na
[liście plików, których check nie czyta](tests/nie-po-polsku.txt).
Polskie sekcje dopisano tam do angielskiego dokumentu,
a [reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
żąda przekładu całego pliku,
więc dopóki go nie ma, linter nie czyta także tych sekcji, które już stoją po polsku.
Ruchem jest przekład reszty dokumentu
i skreślenie wpisu z `tests/nie-po-polsku.txt` tym samym commitem.

Cząstka `się` stoi przy formie osobowej, a należy do bezokolicznika za nią.
`Zebranie ma się odbyć.` jest u olskiego czasownikiem `mieć się`,
bo produkcja `Verb` w `olski/subset.py` skleja cząstkę z formą osobową
i tylko z nią, a polszczyzna kładzie ją tam także wtedy,
gdy zwrotny jest bezokolicznik.
Płaci za to [gramatyka](docs/subset.md#leksykon-mówi-dwa-zdania-na-lemat-i-bierze-je-z-walentego):
zawężenie o bezokolicznik jest wobec Walentego prawdziwe,
a nad Składnicą kosztuje dwa zdania i nie kupuje żadnej jednoznaczności,
więc parser tego zdania leksykonu nie czyta, choć skład je czyta,
i mówi w `olski/walenty.py`, dlaczego.
Ruchem jest cząstka licencjonowana przez czasownik, do którego należy,
a nie przez ten, przy którym stoi.
Do rozstrzygnięcia jest, czy da się to postawić bez czytania,
w którym oba czasowniki biorą ją naraz,
bo takie czytanie jest drugim czytaniem tego samego zdania.
Zamierzone jest po tym powtórzenie tamtego pomiaru,
bo zawężenie o bezokolicznik wraca wtedy do rozważenia.

Sprawdzian leksykonu jest skryptem pisanym od nowa przy każdej zmianie.
[Liczba, na której leksykon stoi](docs/subset.md#leksykon-mówi-dwa-zdania-na-lemat-i-bierze-je-z-walentego)
— 615 z 616 lematów potwierdzonych bankiem drzew — bierze się ręcznie,
bo `_slot_role` w `olski/corpus.py` czyta z pola `tfw` dwie role olskiego,
a rama czasownika stoi w tym polu cała.
Ruchem jest zejście po wybranym drzewie do węzłów `zdanie`,
wzięcie lematu głowy i pozycji fraz wymaganych obok niej,
i porównanie tego z `WALENCJA` w `olski/subset.py`.
Do rozstrzygnięcia jest, co taki przebieg drukuje:
sama niezgodność jest liczbą, a pożytek z niej ma dopiero ten,
kto widzi lemat, zdanie i pozycję, o którą poszło.
Do rozstrzygnięcia jest też, czy to jest flaga `olski-corpus`,
czy komenda obok niej, bo tamta mierzy gramatykę, a ta leksykon.
Zdejmuje to zarazem pytanie, którego dziś nikt nie zadaje po zmianie w
`olski/walenty.py`: czy nowe czytanie Walentego dalej zgadza się z bankiem.

Leksykon walencyjny mówi o bierniku i o bezokoliczniku, a o przypadkach nie mówi.
Narzędnika [przekład](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)
nie bierze, bo `inst` jest u olskiego pozycją orzecznika,
a Walenty nie odróżnia jej od argumentu narzędnikowego,
więc kopula zostaje listą pisaną ręcznie w `olski/subset.py`.
Do przeczytania jest, czy bank drzew tę różnicę widzi:
pozycja `adjp(pred)` stoi w polu `tfw` obok `np(inst)`,
a `olski/corpus.py` czyta dziś z tego pola podmiot i dopełnienie.
Gdyby ją widział, kopula przestaje być listą, a staje się wpisem jak każdy inny,
i wtedy pytaniem jest, ile czasowników poza nią orzecznik w narzędniku bierze.

`olski` chodzi po katalogu, a `olski-check` bierze tylko pliki,
i to samo chodzenie schodzi do `.git`.
`_collect` w `olski/cli.py` schodzi po `rglob`, pyta `is_plain_text` o każdy plik
i liczy to, co minął, żeby przebieg nad katalogiem nie lintował licencji,
a `main` w `olski/check.py` czyta po prostu każdą podaną ścieżkę.
Widać to w poleceniu, którym
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów: stoi przed nim `find`, bo inaczej nie ma czego podać.
Ten sam `rglob` melduje nad `olski rit-dokumentacja/` 39 plików minionych
w `.sample`, bez rozszerzenia, `.md`, `.png`, `.idx`, `.pack` i `.rev`,
gdzie 7 markdownowych jest jedynymi, jakich czytelnik by się spodziewał,
a paczki i indeksy są gitowe;
schodził tam zawsze i pokazała to dopiero ta liczba,
czyli ostrzeżenie działające, a nie druga usterka.
Ruchem jest wyjęcie `_collect` z `olski/cli.py` do wspólnego miejsca
i zawołanie go z każdej komendy, po czym `find` z tamtego polecenia znika,
wraz z pominięciem katalogu, którego nazwa zaczyna się kropką,
i zdaniem w `_collect`, że wejściem jest repozytorium,
a jego kontrola wersji nie jest częścią korpusu.
Przeciw pominięciu: katalog z kropką podany wprost staje się wtedy nieosiągalny,
więc należy ono do chodzenia, a nie do testu na rozszerzenie.
Komend jest przy tym trzy, a nie dwie:
`main` w `olski/wieloznaczność.py` czyta ścieżki tak samo jak `olski-check`,
i tak samo trzeba mu je rozwinąć powłoką.
Do rozstrzygnięcia jest to, co druga komenda robi z pominiętymi:
`olski` mówi o nich, bo pominięcie zmienia mianownik częstości,
a `olski-check` ma mianownik, który tamten dokument cytuje,
więc nie jest oczywiste, czy to jest ta sama notatka, czy druga obok niej.

`olski-check` daje dokumentowi liczbę i nie ma pod sobą żadnego testu.
Nic w `tests/` nie importuje `olski/check.py`:
werdykt nad zdaniem czyta `tests/test_subset.py` przez `check()` w `olski/subset.py`,
a opakowanie wokół niego nie jest czytane nigdzie.
Zostają w nim trzy kody wyjścia
(2 bez argumentów i nad ścieżką, której nie da się przeczytać,
1 wtedy, gdy nie każde zdanie przeszło),
liczenie fragmentów obok zdań
oraz układ wierszy, które komenda wypisuje.
Ostatni z nich jest tym, po co dokument tę komendę woła:
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów nad korpusem audytowym z ostatniego wiersza wydruku,
więc figura w dokumencie stoi na formacie, którego nic nie trzyma.
Druga komenda ma `tests/test_cli.py`, więc wzór jest na miejscu:
wołanie `main` z listą argumentów i czytanie `capsys`.
Testem nie jest wydruk przepisany wiersz po wierszu:
kosztuje przy każdej zmianie układu
i nie broni niczego, czego by czytelnik nie zobaczył.
Warte pisania są dwie rzeczy: podsumowanie, bo jest figurą, którą cytuje dokument,
i kody wyjścia, bo widzi je tylko ten, kto komendę wpina w potok.

Rzeczownikowe czytanie przymiotnika zabiera README ostatnie zdanie
i nie widać przy nim tego, co zdjęło zaimek.
`Linter pomaga pisać dobry kod.` wychodzi dwoma czytaniami tego samego kształtu,
bo Morfeusz daje `dobry` czytanie `subst:sg:nom.acc:m3` obok przymiotnikowego,
a `kod` czytanie lematu `koda` w dopełniaczu mnogim,
więc `dobry kod` jest raz przymiotnikiem przed rzeczownikiem,
a raz rzeczownikiem z dopełniaczem po nim.
Zaimek rzeczowny zdjął z tej klasy
[warunek w produkcji](docs/subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem),
bo `to` dopełniacza nie bierze,
a `dobry` bierze: rzeczownik odprzymiotnikowy dopełniaczem rządzi
i kryterium na tę pozycję zabiera zdania Składnicy, w których rządzi,
co zmierzone stoi w
[`docs/subset.md`](docs/subset.md#dwa-szersze-kryteria-zmierzono-i-żadne-nie-stoi).
Zostaje więc sąsiad, nie głowa:
pary nie ma bez dopełniacza `kod`, czyli bez lematu `koda`,
którego ten rejestr nie zna,
a rzadkość formalnego znamienia nie ma.
Do przeczytania jest, czy da się ją policzyć tak,
żeby liczba mówiła o polszczyźnie, a nie o korpusie, w którym się ją policzyło,
i pierwszym pytaniem jest, czy jakiekolwiek kryterium tu jest;
wykluczenie zbyt szerokie zabiera zwyczajne polskie słowa,
co [`docs/subset.md`](docs/subset.md#the-dictionary-offers-readings-polish-does-not)
pokazuje na `jury` i `menu`.
Stoi na tym zdaniu
[kryterium wyjścia toru](docs/roadmap.md#celem-toru-jest-to-readme).

Wykluczenie ze słownika nie sięga po zaimek, a `go` jest grą.
`CLOSED_CLASS` w `olski/subset.py` wylicza siedem klas zamkniętych,
od przyimka po wykrzyknik, a zaimka wśród nich nie ma,
więc `admissible` zostawia formie `go` czytanie `subst` obok `ppron3`,
choć jest ono nieodmienne dokładnie tak jak nuta,
której to samo wykluczenie odmawia
([`docs/subset.md`](docs/subset.md#the-dictionary-offers-readings-polish-does-not)).
Tam, gdzie oba czytania dają jeden kształt, nie kosztuje to nic,
bo [czytanie jest kształtem](docs/subset.md#co-się-liczy-jako-jedno-czytanie),
i tak wychodzą trzy z sześciu zdań, które tamta sekcja liczy.
Zostaje to, gdzie kształty się różnią,
czyli produkcja dająca głowie grupy imiennej dopełniacz po niej:
zaimka jako głowy ta produkcja nie bierze, a rzeczownik bierze.
Kosztuje to już jedną figurę i to jest tańsza połowa dowodu.
`olski/wieloznaczność.py` liczy nad korpusem audytowym to, co zostawia
`admissible`, więc para `go` i `gov.pl` wychodzi tam dwiema grupami imiennymi,
a udział, który stąd rośnie, cytuje
[`docs/open-questions.md`](docs/open-questions.md#kryterium-wyjścia-toru-żąda-jednoznaczności-od-zdania-które-jej-nie-ma)
jako miękką z dwóch swoich liczb.
Do przeczytania zostaje to, czy takie zdanie kosztuje także werdykt,
bo dopiero ono mówi, czy jest tu co naprawiać w gramatyce;
przebieg nad Składnicą, który to pokaże, jest tym samym,
którym mierzy się cenę
[dwóch szerszych kryteriów](docs/subset.md#dwa-szersze-kryteria-zmierzono-i-żadne-nie-stoi),
czyli liczbą lasów tracących czytanie wybrane przez anotatorów.
Ruchem, gdyby było, jest `ppron3` i `ppron12` dopisane do `CLOSED_CLASS`.
Przeciw: zaimek nie jest wyrazem funkcyjnym w tym sensie, w którym są nim tamte,
a kryterium rozszerzone na niego przestaje mówić to, co mówi dziś.

Part of what [`docs/corpus.md`](docs/corpus.md) quotes has no command behind it.
`olski-corpus` prints the verdict tables, the length curve
and the blocker ranking by part of speech,
while the commonest forms under each blocker,
the count of sentences the two runs both accept,
and the column with `admissible` switched off
come from scripts written for one session and thrown away.
So a change to the grammar updates the tables that have a command
and silently leaves the rest stale,
which is the failure the rerun rule in
[`CLAUDE.md`](CLAUDE.md#checks) exists to prevent.
The move is in `olski/coverage.py`:
carry the blocking form beside its part of speech in `Report.blockers`,
add the exclusion-free morphology as a third `SOURCES` entry,
and let the CLI take two runs and print what they disagree about.
That last part has a second caller,
so it should not be tied to the morphology sources:
a point on [the coverage curve](docs/design-notes.md#making-the-trade-measurable)
is a net of what a tier buys against what it costs in uniqueness,
which is two grammars disagreeing rather than two morphologies.
The entry about cutting unlicensed readings before the parse
moves what `blocker` reads off a form,
so whichever of the two is taken first decides what the blocking form is,
and they are one session.
The section that owns the reproduction path says meanwhile which figures are hand-taken,
and that sentence goes when the commands cover them.

`missing-space-after-punctuation` reads the colon of a label such as `**Exit:**`
in [`docs/roadmap.md`](docs/roadmap.md#milestone-4-the-delivery-decision)
as a missing space,
because that colon stands in front of an emphasis marker rather than a word.
Either the documents settle on a label that leaves no mark inside the emphasis,
which is what [`docs/roles.md`](docs/roles.md) does
by opening the sentence with the bold phrase itself,
or the rule gets an exemption for an emphasis marker after the mark,
which is what its audit over published Polish argues for:
most of its hits there are that class, counted in
[`docs/firing-rates.md`](docs/firing-rates.md#missing-space-after-punctuation-mostly-read-an-emphasis-marker).
That audit is one corpus and not both.
The audit corpus reaches the rules through the extraction,
which puts back what an emphasis wrapped and drops the markers,
so the rule never meets the class there and
[the audit over that corpus](docs/firing-rates.md#missing-space-after-punctuation-read-a-colon-inside-an-identifier)
reads a colon inside an identifier instead.
The hit above survives because a named file is linted whatever its format,
which is how this repository's own documents are run
and is not the run either audit was taken over.
So the exemption is still the more expensive of the two,
because it moves what the rule's hits are
and so drags the rerun [`CLAUDE.md`](CLAUDE.md#checks) demands
over published Polish and over the classes that document reports having read.

The booster stems are the last pattern
[milestone 2](docs/roadmap.md#milestone-2-the-plain-polish-pack-without-an-analyser)
rests on that nothing has been run over,
and `harness/endings.py` does not reach them as it stands.
A `Probe` there matches with `endswith`,
where `kluczow` and `istotn` are what a word begins with,
so either the declaration grows a matching side beside the classes it carries,
or the boosters get a run of their own and this module stays about endings.
The choice is worth making on the classes rather than on the matching,
which is the cheaper half and the one the two probes there settle by example:
each of them turns on a tag, `ger` and `imps`,
and a booster's question is whether an adjective is doing any work,
which no tag answers and which
[the nominalization probe](docs/linter.md#what-the-nominalization-endings-match)
already shows a run can come back undecidable on.
So the run to write first is the one that says
how much of what the stems match is the adjective at all,
and it belongs in front of the rules rather than after them,
because what it decides is whether the rule exists rather than how it is tuned.

The `verb` class of `NOMINALIZATION` in `harness/endings.py`
stands before every nominal one,
which is right for `zostanie` and wrong for `dacie`.
Both carry a verb reading beside a nominal one,
and a document dating an invoice means the locative of `data`
where the order files the second person plural of `dać`,
so the inflected share quoted in
[`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match)
is a floor and not a count.
The move is either an order the corpus settles —
the nominal reading first where the verb reading is a person the register does not use —
or the floor stated wherever the share is quoted,
which is that section alone,
the roadmap having taken the same finding coarsely and quoted no number.
The evidence is 7 words: 6 `dacie` and 1 `powiecie`,
both of which the register uses as nouns.

Granica harnessu jest napisana raz, a stosuje się dwa razy inaczej.
`harness/__init__.py` mówi, że korpus w formacie znacznikowym
dochodzi do reguł tędy, a nie przez `olski`,
a `harness/endings.py` dokłada, że stoi tam,
bo o polszczyźnie niczego nie twierdzi.
Oba kryteria trafiają w `olski/corpus.py`, który czyta XML Składnicy,
w `olski/coverage.py`, który mierzy nim gramatykę
i produkuje tabele [`docs/corpus.md`](docs/corpus.md),
oraz w `olski/attachment.py`, który mierzy nim sam korpus
i produkuje tabelę
[`docs/subset.md`](docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia).
Trzeci z nich jest przy tym przypadkiem najostrzejszym,
bo o gramatyce nie mówi nic, tak samo jak `harness/endings.py`.
Czwarty pokazuje, że samo kryterium jest za grube:
`olski/wieloznaczność.py` też o gramatyce nie mówi nic
i mimo to do `harness/` nie pójdzie,
bo liczy przez `admissible` i przez leksykon walencyjny,
czyli przez dwie decyzje toru gramatycznego naraz.
Trzy z tych czterech są liśćmi,
a czwarty odbiera `olski/attachment.py` bycie liściem, importując go,
i wszystkie instalują się z pakietem
(`include = ["olski*", "skład*"]` w `pyproject.toml`),
a jeden ma własną komendę,
gdzie tak samo pomiarowe programy toru linterowego
nie mają ani instalacji, ani komendy.
Ruchem jest rozstrzygnięcie granicy, a nie przeniesienie plików:
albo obie idą do `harness/`, a `olski-corpus` staje się
`python3 -m harness.coverage` jak dwie pozostałe komendy pomiarowe,
co przepisuje polecenia w [`docs/corpus.md`](docs/corpus.md#fetching-it)
i w [sekcji Checks](CLAUDE.md#checks),
albo `harness/__init__.py` mówi, że jest harnessem toru linterowego,
co nie kosztuje nic i przestaje odpowiadać dwa razy.
Do przeczytania jest to, co pakiet ma dawać temu, kto go instaluje:
czytnik banku drzew i trzy programy pomiarowe są w nim,
a nikt, kto lintuje tekst, ich nie woła.

Kto instaluje samego lintera, buduje przy okazji analizator morfologiczny.
`dependencies` w `pyproject.toml` żąda `morfeusz2` bezwarunkowo,
a lintowanie nie sięga po niego ani razu:
`olski/cli.py`, `olski/engine.py`, `olski/checks.py`, `olski/document.py`,
`olski/rules.py`, `olski/calibration.py` i `olski/packs/` nie importują `olski/morph.py`,
czyli jedynego miejsca, w którym stoi `import morfeusz2`,
a wołają go `olski/parse.py`, `olski/subset.py`, `olski/corpus.py`
i `olski/coverage.py`, przez `subset` zaś także `olski/check.py`,
a przez `corpus` także `olski/attachment.py`.
[Sekcja Checks](CLAUDE.md#checks) opisuje środowisko,
w którym koło Morfeusza się nie zbudowało,
a testy, które go wołają, pomijają się zamiast wywracać zbiórkę.
Udokumentowana instalacja do tego środowiska nie prowadzi:
`pip install -e '.[dev]'` kończy się wtedy błędem, a nie środowiskiem z pytestem,
więc pomijanie broni stanu, w który wchodzi się bokiem,
instalując pytest osobno i wołając go z klonu.
Ruchem jest zejście `morfeusz2` z `dependencies`
do `[project.optional-dependencies] grammar`,
po czym instalacja w workflow bierze oba dodatki, `dev` i `grammar`,
żeby przebieg na pushu dalej dotykał gramatyki;
kroki workflow i blok w `CLAUDE.md` trzyma równe
`test_the_checks_a_person_runs_are_the_checks_a_push_runs`,
więc obie kopie ruszają się razem.
Wpis nie zamyka się razem z granicą harnessu:
gdyby czytnik banku drzew i program pomiarowy poszły do `harness/`,
`morph`, `parse`, `subset` i `check` zostają w pakiecie i dalej ciągną Morfeusza,
a razem z nimi `skład/`, który instaluje się z tego samego wpisu
i woła `morfeusz2` w drugą stronę.
Do przeczytania jest, na których platformach PyPI ma gotowe koło,
bo to rozstrzyga, czy podział kupuje instalację, której dziś nie ma,
czy tylko nazywa dwa tory drugi raz:
`morfeusz2` 1.99.15 wchodzi na Linuksie x86-64 pod Pythonem 3.11
bez budowania czegokolwiek.

`docs/open-questions.md` trzyma listę decyzji zamkniętych,
a każda z nich ma właściciela gdzie indziej.
Sekcja `Settled` powtarza to, co jest budowane, wraz z kryterium wyjścia
([`docs/roadmap.md`](docs/roadmap.md#celem-toru-jest-to-readme)),
opcjonalność toru linterowego (README i [`docs/linter.md`](docs/linter.md)),
bliskość polszczyzny
([`docs/design-notes.md`](docs/design-notes.md#decisions-taken)),
kalibrację
([`docs/linter.md`](docs/linter.md#the-thing-that-makes-or-breaks-it-calibration)),
to, że narzędzie nie jest detektorem
([`docs/linter.md`](docs/linter.md#limits-worth-stating-up-front)),
i dwa słowniki do dwóch zadań,
czyli tę jedną decyzję, przy której `docs/design-notes.md` pisze wprost,
że nie jest zapisana dwa razy.
Ruchem jest usunięcie sekcji na rzecz zdania mówiącego, gdzie decyzje zapadłe stoją,
czyli [zakaz znaczników zrobionego](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
zastosowany do listy otwartych pytań.
Przeciw: lista zamkniętych rozwidleń oszczędza komuś otwierania ich z powrotem.
Do przeczytania jest więc, czy któraś pozycja niesie odrzuconą alternatywę,
której jej właściciel nie trzyma — taka zostaje, a reszta idzie.

Ten sam zepsuty pakiet raportuje się dwiema drogami inaczej.
`_import_file` w `olski/rules.py` łapie `Exception`,
więc pakiet podany ścieżką wychodzi wierszem `olski:` i kodem 2,
a ten sam plik podany nazwą modułu idzie przez `_import`,
które zawija tylko `ImportError`, i drukuje ślad stosu z kodem 1.
Do przeczytania jest pakiet podnoszący cokolwiek poza tym,
co moduły tego pakietu nazywają:
`--packs ./pakiet.py` obok `--packs pakiet` nad tym samym plikiem.
Nazwą modułu ładują się pakiety wysyłane z olskim,
więc tą gorszą drogą chodzi ten, kto edytuje `olski/packs/`.
Drugą połową tego samego jest krotka w `main` z `olski/cli.py`:
`RuleError`, `ParamError` i `CalibrationError` łapane razem,
bo dla tego, kto woła komendę, są jednym zdarzeniem,
a każdy następny moduł, który cokolwiek waliduje, dokłada do niej element.
Ruchem jest jedna klasa bazowa dla tych trzech,
łapana zamiast krotki, plus `_import` zawijające tak jak `_import_file`.
Do rozstrzygnięcia zostaje, gdzie ta klasa stoi,
bo moduł poniżej wszystkich trzech powstałby dla niej samej,
a `olski/calibration.py` stoi najniżej i o deklaracjach nie mówi nic.

Lista dokumentów w README miesza dwa tory, które sekcja nad nią rozdziela.
[`Co działa`](README.md#co-działa) mówi, że działają dwie rzeczy,
a lista pod nią biegnie bez podziału i rośnie z każdym dokumentem,
więc czytelnik toru gramatycznego i autor reguły
przechodzą przez cudze pozycje, zanim dojdą do swoich.
Ruchem jest pogrupowanie listy — tor linterowy, tor gramatyczny
i to, co obsługuje oba — bez ruszania linków,
czyli najtańsza zmiana, jaką ta lista przyjmie.
Przeciw katalogom w `docs/`: przepisałyby każdy link względny po to,
żeby dać indeks, którym ta lista już jest.
Do rozstrzygnięcia jest, gdzie idą pozycje graniczne,
bo [`docs/roles.md`](docs/roles.md), [`docs/roadmap.md`](docs/roadmap.md)
i [`docs/open-questions.md`](docs/open-questions.md) obsługują oba tory.
Etykiety grup nie ruszą `test_every_document_is_listed_in_the_readme`,
który czyta pozycje wzorcem `^- [docs/…]` i nie patrzy, co stoi między nimi.

`docs/firing-rates.md` wyprowadza drugi raz to, co należy do
[listy korpusu audytowego](docs/audit-corpus.md#the-list):
dlaczego `rit-dokumentacja` traci na ekstrakcji tyle, ile traci,
czyli że jej tabele API stoją bez wiodących kresek
i że takie tabele są większością jej dokumentów.
Przyczyna stoi w obu miejscach w pełnej precyzji,
a jeden właściciel rozumowania żąda tam zdania ze wskaźnikiem.
Wniosek, po który `firing-rates.md` po nią sięga, zostaje:
różnica formatu jest większością tego, czym trafienia niżej nie są.

Skład nie ma czym powiedzieć, co jest tematem wewnątrz grupy imiennej,
więc `Jaki` w `skład/składnia.py` zawsze stawia przymiotnik przed rzeczownikiem,
choć polszczyzna ma oba szyki i różnią się one tym, co niosą:
przymiotnik po rzeczowniku nazywa, a przed nim określa.
Widać to bez żadnego pomiaru, na jednym zdaniu:
README pisze `zwykły tekst polski`,
a to samo drzewo wypuszcza `zwykły polski tekst`.
Do przeczytania jest ta para wraz z tym,
co [`docs/sklad.md`](docs/sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
mówi o tym, czego drzewo nie niesie.
Ruchem jest ta sama kategoria, którą zdanie już ma, wpuszczona do grupy imiennej:
`Wyróżnienie` stoi w `skład/składnia.py` i przestawia konstytuenty zdania,
a wewnątrz grupy nie sięga niczego, bo `Cechy` w `skład/słownik.py`
zwija przymiotniki, zanim spotkają rzeczownik.
Rozstrzygnięcia żąda przy tym co innego niż w zdaniu:
tam wyróżnienie przestawia to, co i tak stało osobno,
a tu przymiotnik postawiony po rzeczowniku zmienia znaczenie całej grupy,
więc nazwa `temat` na to nie przystaje.

Kolejne żądania legendy stoją w
[`docs/sklad.md`](docs/sklad.md#lepszy-tekst-żąda-czego-innego-niż-dłuższy)
pod liczebnikami porządkowymi, a liczebnik jest złym kręgosłupem dla tej listy.
Pozycje od `Pierwszym` do `Siódme` rozciągnęły tę sekcję na najdłuższą w pliku,
a żądanie dopisane w środku każe przenumerować wszystko pod nim,
choć kolejność nic tam nie niesie: nie jest ani czasem, ani wagą.
Kręgosłup, który niesie coś, sekcja już znalazła i mówi o nim wprost:
warstwa, która za żądanie zapłaciła.
Jedne żądania zostały w składni, jedne zeszły o dwie warstwy niżej,
do wyboru formy i do czytania cudzego słownika,
a jedno zapłaciło samym zapisem, i to jest podział, który ta sekcja przy sobie robi
zdaniem „dwa razy pod rząd nie jest zbiegiem”.
Do przeczytania jest cała ta sekcja wraz z
[etapem 5](docs/roadmap.md#etap-5-konstrukcje-których-żąda-readme),
bo to on trzyma listę konstrukcji, a ta sekcja trzyma to, co je zamówiło,
i przy podziale po warstwach te dwie listy przestają się mylić.
Ruchem jest pogrupowanie akapitów po warstwie, która płaciła,
i wyjęcie liczebników; wpisu żaden pomiar nie jest przy tym winien,
bo nic pod tą sekcją nie stoi liczbą.

Anafora sięga podmiotu i nic poza nim,
a opowieść o bazyliszku pokazuje, gdzie to boli:
`opowieści/bazyliszek.py` pisze `wzrok potwora` dwa razy,
a polszczyzna napisałaby drugi raz `jego wzrok`.
Tak samo dopełnienie: po `Bazyliszek zobaczył własne odbicie.`
legenda pisze `zamienił bazyliszka w kamień`,
a polszczyzna napisałaby `zamienił go`.
Do przeczytania jest to, co
[`docs/sklad.md`](docs/sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)
mówi o wąskim opuszczaniu podmiotu,
wraz z `pomijalny` w `skład/składnia.py`, który te warunki trzyma,
bo zaimek dziedziczy stamtąd warunek, a nie tylko mechanizm:
zaimek postawiony tam, gdzie czytelnik trafia na dwie osoby, jest gorszy od powtórzenia.
Ruchem jest zaimek osobowy w miejscu roli innej niż podmiot,
liczony z tego samego `Kontekst`.
Trzy rzeczy stoją przy tym ruchu i każda robi go innym, niż wygląda,
a wywód trzyma
[`docs/sklad.md`](docs/sklad.md#lepszy-tekst-żąda-czego-innego-niż-dłuższy).
Warunek jest ostrzejszy niż przy podmiocie, bo zaimek niesie rodzaj i liczbę,
a nie osobę, więc blokuje go każda rzecz obok o tej samej formie zaimka,
i wtedy do zmierzenia jest, czy pozycja zwalnia się w tej legendzie gdziekolwiek.
Szyk jest drugi: `Chciał ją znaleźć.` stawia zaimek przed czasownikiem osobowym,
czyli poza zdaniem, w którym on stoi,
więc to jedna zmiana wraz z
[dopełnieniem wyrażonym zdarzeniem](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
a nie zmiana obok niego.
Trzecim jest `jego wzrok`, czyli zaimek dzierżawczy:
przestawia on grupę imienną, a nie wypełnia pozycję w zdaniu,
i wtedy do rozstrzygnięcia jest, czy `swój` i `jego` są jedną kategorią, czy dwiema,
bo pierwszy odsyła do podmiotu zdania, a drugi poza nie.

`Zdanie.podmioty` w `skład/składnia.py` schodzi pod konstytuent na dwa poziomy,
czyli tam, gdzie sięga `_wskazany`, a zdanie podrzędne stoi czasem głębiej:
`Mysz goniła ogon myszy, która spała.` ma dwa podmioty, a widać stąd jeden.
Kosztuje to opuszczenie postawione tam, gdzie czytelnik trafia na dwie rzeczy
wyciągające z czasownika jedną formę, czyli dokładnie to, przed czym ten warunek broni.
Do przeczytania jest `_zdania_pod` wraz z `_wskazany` w tym samym pliku,
bo schodzą tak samo głęboko i tylko jednej z nich to wystarcza:
tamta pyta, skąd zaimek wyjdzie na czoło, a ta, na kogo czytelnik trafi.
Ruchem jest zejście po całym drzewie roli zamiast po dwóch jego poziomach,
i jest ono tańsze niż tamto, bo nie ma z niego nic do wyprowadzenia.

Rama czasownika, o którą pyta `Robi` w `skład/składnia.py`,
odpowiada na dwa pytania z listy: o biernik i o bezokolicznik,
więc rola w przypadku innym nie ma po tej stronie o co zapytać
i nie ma jak stanąć w drzewie.
Kosztuje to trzy klasy zdań, a wszystkich trzech chciała druga wersja legendy,
trzecia poprosiła o dwie z nich znowu i wszystkie trzy z niej wypadły.
`Czeladnik nie powiedział nikomu.` żąda celownika,
`Czeladnik szukał córki krawca.` żąda dopełniacza,
i to drugie `Robi` odrzuca, bo leksykon `szukać` wymienia jako czasownik bez biernika,
czyli mówi o nim prawdę i mówi ją w jedyny sposób, jaki ma.
`Córka krawca nie wierzyła w bazyliszka.` żąda wyrażenia przyimkowego,
którego czasownik wymaga, a nie takiego, które autor dokłada jako okoliczność,
i ta klasa jest gorsza niż brak, bo `Dokąd.w` wypuści to zdanie jako cel,
czyli powie, że ktoś w coś wierzy tak, jak mówi się, że ktoś dokądś idzie.
Czwarty koszt jest cichy i przez to najgorszy z nich:
`chcieć` ma u Walentego i dopełniacz, i przypadek strukturalny,
więc przechodzi tu przez pytanie o biernik i wypuszcza `Kot chce mysz.`,
czyli zdanie, którego polszczyzna woli nie mówić, a nikt tego nie zgłasza.
Jedna pozycja znaczy tu więc nie tylko odmowę tam, gdzie brakuje przypadka,
ale i wybór najgorszej z ram, które lemat ma.
Do przeczytania jest `olski/walenty.py` wraz z tym,
co [`docs/subset.md`](docs/subset.md#leksykon-mówi-dwa-zdania-na-lemat-i-bierze-je-z-walentego)
mówi o tym, co ten przekład z Walentego bierze, a czego nie,
bo Walenty niesie wszystkie te ramy i jest to jedna zmiana po obu stronach.
Bezokolicznik pokazał przy tym, ile z tej zmiany jest już zrobione, a ile nie:
przekład umie wziąć drugie zdanie, plik umie je unieść, a `Robi` umie o nie zapytać,
i mimo to każde nowe pytanie jest osobnym polem oraz osobną gałęzią w konstruktorze.
Ruchem jest rama jako zbiór pozycji, a nie lista pytań,
oraz `zdarzenie` w tym samym pliku rozdzielające argumenty po tym zbiorze,
a nie po kategorii okoliczności.

`Przysłówek` w `skład/składnia.py` żąda od słownika formy przysłówkowej,
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

`_obojętny` w `olski/wieloznaczność.py` liczy synkretyzm z jednego czytania,
więc mija formę, której słownik daje mianownik i biernik dwoma osobnymi wpisami.
`Mysz goni ogon.` olski czyta dwojako,
a `miejsca` nie stawia tam żadnej pozycji,
bo `mysz` wychodzi z Morfeusza jako `subst:sg:nom:f` i `subst:sg:acc:f` osobno,
podczas gdy `ogon` wychodzi jako jedno `subst:sg:nom.acc:m3`.
Pomiar sam nazywa swoją liczbę górnym oszacowaniem,
a to jest błąd w drugą stronę i tam go nie ma.
Zgłosił to skład, który tę samą klasę liczy porównaniem form i tej pary nie mija,
i trzyma tę rozbieżność `tests/test_przegląd.py`.
Do przeczytania jest, ile form rejestru dzieli te dwa przypadki na wpisy,
oraz to, czym staje się wtedy zgoda:
warunek żąda dziś liczby i rodzaju od jednego czytania,
a nad dwoma trzeba wskazać, które z nich ma zgodzić się z orzeczeniem.
Ruchem jest warunek pytany o segment zamiast o czytanie.
Wpis jest zaparkowany, bo poprawka rusza liczbę,
którą [`docs/open-questions.md`](docs/open-questions.md#kryterium-wyjścia-toru-żąda-jednoznaczności-od-zdania-które-jej-nie-ma)
podaje nad korpusem audytowym,
więc zamyka go dopiero sesja, która ten korpus ściągnie i przebieg powtórzy.
Tę samą liczbę rusza wpis o zaimku wykluczonym ze słownika,
bo `admissible` stoi między tekstem a tym pomiarem,
więc przebieg jest jeden i oba wpisy podnosi się razem.

`przejrzyj` w `skład/przegląd.py` zgłasza jedną klasę z dwóch,
bo przyłączenia zawęzić nie ma dziś czym.
Okolicznik dochodzi w drzewie do zdarzenia zawsze,
więc każde wyrażenie przyimkowe stojące za grupą imienną byłoby trafieniem,
a raport zgłaszający każde zdanie z przyimkiem nie oddziela niczego od niczego:
nad `opowieści/bazyliszek.py` trafiłby w kilka z dziewiętnastu zdań
i żadne z tych zgłoszeń nie mówiłoby autorowi, co miałby z nim zrobić.
Do przeczytania jest, czym się różnią te miejsca,
oraz to, co [`docs/subset.md`](docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia)
mierzy nad Składnicą, bo tam ta sama klasa jest policzona nad cudzymi drzewami.
Stoi nad tym wpisem pytanie
[`docs/open-questions.md`](docs/open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma),
które pyta o to samo od strony parsera i mówi, że wyjścia nie ma w gramatyce.
Przegląd stoi wobec niego inaczej i to jest tu jedyna nadzieja:
on niczego nie odrzuca, więc pomyłka kosztuje tu wiersz raportu,
a nie zdanie, którego autor nie napisze.
Ruchem jest kryterium, które oddziela przyłączenie niosące różnicę znaczenia
od tego, przy którym oba czytania mówią to samo,
albo rozstrzygnięcie, że takiego kryterium nie ma
i że ta klasa do przeglądu nie wchodzi.

Stopnia nie ma w składzie żadnego, a jest on kategorią dziedziny.
`Jaki` w `skład/składnia.py` żąda od przymiotnika stopnia równego na stałe,
`Przysłówek` obok żąda tego samego i mówi w docstringu,
że stopień wyższy „mówi co innego” i czeka na kategorię.
Bez niego nie da się powiedzieć `Koszt szynki jest wyższy niż koszt bułki.`,
czyli tego zdania, które mówi to samo co `Koszt szynki przewyższa koszt bułki.`
i mówi to bez kolizji, którą `skład/przegląd.py` w drugim zgłasza.
Do przeczytania jest, czy porównanie jest kategorią osobną od cechy,
bo `wyższy` jest formą przymiotnika, a `niż koszt bułki` jest drugim uczestnikiem,
więc drzewo ma tu do postawienia relację, a nie stopień przy rzeczy.
Ruchem jest ta kategoria wraz z linearyzacją stawiającą `niż`,
a nie przełącznik wybierający między dwoma zdaniami za autora:
przegląd zgłasza, żeby autor napisał drugie drzewo,
a nie żeby kompilator podmienił mu pierwsze.

`Jest` w `skład/składnia.py` umie jedną kopulę, a gramatyka bierze pięć.
`Jan zostaje nauczycielem.` wyprowadza się w olskim i stoi w `PRZYJMOWANE`
w `tests/test_subset.py`, a ze składu nie wyjdzie,
bo lemat kopuli stoi w tym konstruktorze jako stała, a nie jako pole drzewa.
Widać to dopiero od zmiany, po której rama czasownika przychodzi z leksykonu:
`KOPULA` w `olski/subset.py` jest tą częścią walencji, której Walenty nie niesie,
i [`docs/subset.md`](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)
nazywa ją jedynym wpisem leksykonu pisanym ręcznie,
a stoi ona w gramatyce, a nie w `olski/walencja.py`, czyli tam, gdzie leksykon.
Do przeczytania jest ta sekcja wraz z wpisem o narzędniku,
bo ten sam przekład rozstrzyga, czy kopula w ogóle zostaje listą.
Ruchem jest `KOPULA` przeniesiona do `olski/walencja.py`
oraz `Jest` biorące lemat tak, jak bierze go `Robi`,
wraz z odmową dla czasownika, którego ta lista nie wymienia.
Czyta ją stamtąd także `sonda/polszczyzna.py`, więc import idzie razem z nią.

`odmień` w `skład/morfologia.py` bierze pierwszą z form jednego leksemu,
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
[`docs/sklad.md`](docs/sklad.md#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)
mówi o kryterium, które zostało zbudowane obok tej klasy,
bo pytanie jest tu tym samym pytaniem o jedno piętro niżej:
wybór między leksemami zapada w nazwie, a ten zapada pod jednym leksemem.
Ruchem jest rozstrzygnięcie, czym ten wybór ma być, i kandydatów jest dwóch.
Zgłoszenie jak `WieleLeksemów` żąda od autora wpisu przy każdym wariancie,
także tam, gdzie oba warianty znaczą to samo, czyli przy `oczami` obok `oczyma`.
Wpis wskazujący formę, jak `skład/leksemy.py` wskazuje leksem,
kosztuje wpis tylko tam, gdzie ktoś na wariant trafi,
a milczy dokładnie tak jak dziś, dopóki nikt go nie napisze.
Rozstrzyga między nimi to, ile takich wariantów rejestr naprawdę spotyka,
i tego nikt nie policzył.

`rodzaj_rzeczownika` w `skład/morfologia.py` zgłasza `BrakFormy` nad rzeczownikiem,
który liczby pojedynczej nie ma, bo szuka rodzaju w mianowniku pojedynczym.
Kosztuje to podmiot: `drzwi` i `Włochy` nie staną w zdaniu, z którego wyjdzie czasownik,
i nie staną w koordynacji, która rodzaju od członów żąda,
choć jako dopełnienie wychodzą, i tak stoją w `opowieści/bazyliszek.py`.
Do przeczytania jest to, co `paradygmat` w tym samym pliku dostaje z SGJP
dla takiego leksemu: rodzaj stoi tam przy formach liczby mnogiej,
więc rzecz jest w miejscu, w którym się go szuka, a nie w danych.
Ruchem jest rodzaj brany z mianownika tej liczby, którą ten leksem ma,
wraz z testem na obie liczby, bo inaczej poprawka pokryje jedną z nich.

`skład/przyimki.py` zna przyimek w jednej postaci,
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

Leksykonu projektu nie ma, a rejestr, w którym się pisze, żąda go od obu kierunków:
`komit`, `olski` i `lintować` dostają z SGJP `ign`,
więc synteza nie ma czego wypuścić, a analiza czyta formę, której nie zna.
Osobno stoi leksem, którego słownik nie ma, choć napis zna:
projekt piszący o agentach jako o programach żąda liczby mnogiej `agenty`,
a `agenty` z SGJP jest formą deprecjatywną leksemu osobowego,
czyli czym innym niż liczba mnoga rzeczy nieżywotnej.
Do przeczytania jest to, co
[`docs/sklad.md`](docs/sklad.md#leksykon-projektu-sgjp-nie-zna-słów-których-używa-rejestr)
mówi o cenie słownika dołożonego Morfeuszowi i o tym, co wpis ma nazywać,
wraz z `olski/leksykon.txt` i `skład/leksemy.py`, czyli dwoma leksykonami,
które już stoją, a żaden z nich na to pytanie nie odpowiada.
Ruchem jest rozstrzygnięcie, czy wpis wypisuje formy,
czy wskazuje leksem, wedle którego się odmienia,
a po nim plik z wpisami na te słowa, których to repozytorium używa o sobie.
Drugą z tych dróg widać już na `skład/leksemy.py`, ale tylko połowę:
wpis wskazuje tam leksem, który słownik ma,
a tutaj trzeba wskazać leksem, wedle którego odmienia się słowo,
którego słownik nie ma wcale.

Liczby wzięte nad własnym README stoją w dwóch dokumentach,
a [`CLAUDE.md`](CLAUDE.md#checks) żąda, żeby liczby nad własną prozą nie zapisywać,
bo rusza ją przeredagowanie, którego żadna reguła przeliczania nie dosięga.
Jedno przeredagowanie rusza tam cztery liczby naraz:
mianownik i dwie zgodności w
[`docs/design-notes.md`](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)
oraz licznik klasy zdań w
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop),
a temu, kto przeredagowuje, nie mówi o tym nic.
Do przeczytania jest ta reguła wraz z listą przeliczeń pod nią i oba te akapity.
Ruchem jest rozstrzygnięcie, które z dwojga:
albo reguła dostaje wyjątek na figurę o kodzie liczoną nad własną prozą,
wraz z przeliczeniem należnym przy przeredagowaniu README,
albo te akapity przestają nosić mianownik i mówią o zgodzie bez niego.

Grupa imienna nie bierze rzeczownika z przymiotnikiem za nim i dopełniaczem pod nim,
a rejestr, który nazywa terminy właśnie tak, trafia w tę dziurę zdaniem po zdaniu:
`Rzeczpospolita Polska jest dobrem wspólnym wszystkich obywateli.` nie ma wyprowadzenia,
a `wspólnym dobrem wszystkich obywateli` w tym samym zdaniu ma jedno.
`NPConjunct` w `olski/subset.py` ma osobno rzeczownik z przymiotnikiem,
osobno rzeczownik z dopełniaczem
i osobno każdą z tych dwóch pozycji z wyrażeniem przyimkowym za nią,
więc brakuje jednej pozycji w liście, którą cztery sąsiednie już mają.
Do przeczytania jest ta lista wraz z
[`docs/ustawy.md`](docs/ustawy.md#rejestr-znalazł-dziurę-w-grupie-imiennej),
gdzie stoi, czym ten kształt jest w rejestrze ustaw,
i wraz z [przyłączaniem wyrażeń przyimkowych](docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera),
bo to ono uzasadnia dwie pozycje z tych czterech i ono powie, czy piąta jest tego samego rodzaju.
Ruchem jest ta produkcja wraz z pomiarem, ile daje i ile odbiera:
przymiotnik za rzeczownikiem konkuruje z orzecznikiem przymiotnym,
a dopełniacz pod nim z dopełniaczem pod rzeczownikiem po lewej,
więc zakup trzeba przeczytać jako przejścia między werdyktami, a nie jako liczbę pokrycia.
Wpis jest przez to winien przebiegi,
których [sekcja Checks](CLAUDE.md#checks) żąda od zmiany w gramatyce.

Pomijania testów bez Morfeusza nie pilnuje nic, a raz już się rozeszło.
[Sekcja Checks](CLAUDE.md#checks) mówi, że plik testowy sięgający analizatora
pomija się zamiast wywracać zbiórkę,
a `tests/test_przecinek.py` sięgał go bez `importorskip` odkąd powstał,
bo `olski/subset.py` ciągnie `olski/morph.py`,
gdzie `import morfeusz2` stoi na górze pliku.
Brakującą linię ten plik ma, a własności, którą ona przywraca, nie pilnuje nic:
przebieg z Morfeuszem przechodzi tak samo z nią i bez niej,
więc rozejście widać wyłącznie w tym stanie, w który wchodzi się bokiem,
a opisuje go wpis o `morfeusz2` w `dependencies`.
Ruchem jest test czytający pliki z `tests/`:
ten, którego import dochodzi do `olski/morph.py`,
ma nad tym importem `pytest.importorskip("morfeusz2")`.
Do rozstrzygnięcia jest, czy liczyć import wypisany w pliku,
czy to, dokąd on dochodzi:
`tests/test_przecinek.py` sięgał analizatora przez dwa moduły,
a `tests/test_endings.py` nie sięga go wcale,
bo `harness/endings.py` woła `morfeusz2` dopiero w `main`.
