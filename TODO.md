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
and not only the files it changes.
Two entries can edit disjoint files
and still turn on one judgment about one body of text,
such as what a rule's hits over a corpus are.
A file list does not show that overlap,
so the two are picked up together
and the judgment is reached twice.

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
Wtedy całą zmianą jest skasowanie wpisu,
tak samo jak przy wpisie, który się zamknął,
z powodem w komunikacie commita,
bo skasowany wpis nie zostawia po sobie nic innego.

The line that says what a walk went past counts a repository's `.git` with it.
`_collect` in `olski/cli.py` reaches every file under a named directory,
so `olski rit-dokumentacja/` reports going past 39 files
in `.sample`, no suffix, `.md`, `.png`, `.idx`, `.pack` and `.rev`,
where the 7 Markdown files are the only ones a reader would have guessed at
and the pack and index files are git's own.
The walk always descended there and the count is what made it visible,
which is the warning working rather than a second defect.
The move is for the walk to skip a directory whose name begins with a dot,
and to say in `_collect` that a repository is the expected input
and its version control is not part of the corpus.
Against it: a dotted directory somebody names outright is then unreachable,
so the skip belongs to the walk and not to the suffix test.

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
and finds that member losing three quarters of its Markdown to the extraction,
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
Do przeczytania jest to, co pakiet zgłasza nad tymi polami dzisiaj,
bo wszystkie stoją po angielsku,
a nad angielszczyzną ten check jest deklaracją tak samo,
jak był nad modułem, zanim ekstrakcja powstała.

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
Czytelnik dostaje więc dwa razy ten sam wiersz i nie ma z czego zobaczyć,
czym te czytania się różnią,
a jest to dokładnie to rozróżnienie, dla którego
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
and to carry the rename through
`CLAUDE.md`, `README.md`, this file,
`docs/design-notes.md`, `docs/prior-art.md`, `docs/subset.md`, `docs/swigra.md`,
and the citations in `olski/corpus.py`, `olski/coverage.py`, `olski/subset.py`
and `tests/test_subset.py`.
`tests/test_docs.py` catches the Markdown links and the citations in code,
and nothing catches the plain-prose mentions,
so those are the ones to grep for.
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
a gubi go z drzewa, którym mierzy się jedyną liczbę, jaką to repozytorium podaje.
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
This is ordered behind the chart parser
that the implementation note in `olski/parse.py` defers,
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
where git LFS asks for an install that the session clone precedes,
so tracked files arrive as pointer files and a hook has to pull them,
and spends an allowance that GitHub's billing documentation puts at
1 GB stored and 1 GB of bandwidth a month,
which is ten fetches of Składnica.
LFS buys that back over a binary somebody versions,
and these are frozen archives.
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
"prose in comments and docstrings", and no module here writes them that way.
Every file in `olski/` and `harness/` wraps its comments to a column instead,
so the rule and the code have disagreed for as long as both have existed
and a new docstring following the rule reads as a typo beside its neighbours.
Two ways out, and the choice is a judgement about the whole package
rather than about whichever function is being edited at the time:
narrow the rule in `CLAUDE.md` to Markdown, commit messages
and the prose fields of a declaration,
which is where the tighter diff is actually collected,
or keep the rule and reflow the docstrings under
[lazy adoption](CLAUDE.md#adopt-these-rules-lazily), file by file as they are touched.
Narrowing costs a second rule as well:
[the language rule](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
reaches comments and docstrings
by pointing at semantic line breaks for what counts as prose,
so narrowing them out there takes them out of Polish too.
The second answer also needs saying out loud,
because the mixed state it passes through is what a reader will read as drift.

To samo `jest` wychodzi w raporcie raz kopulą, a raz czasownikiem.
`Ludzie są wolni.` daje rolę `Verb`, a `Jan jest nauczycielem.` rolę `Copula`,
bo orzecznik w narzędniku bierze osobna produkcja, i `ROLES` wymienia oba.
`Copula` w `olski/subset.py` jest osobnym symbolem, a nie cechą czasownika,
bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza,
więc żądanie „bądź kopulą” postawione czasownikowi przechodziłoby każdemu.
Ruchem jest ujemna lemma w `word()` z `olski/grammar.py`:
produkcja ogólna `Verb` przestaje brać lematy kopuli, kopula dostaje własną
z cechą, którą wtedy obie niosą, i węzeł w obu przypadkach nazywa się `Verb`.
Przeciw: byłby to pierwszy warunek ujemny w tej gramatyce,
gdzie unifikacja jest przecięciem, a przecięcie negacji nie zna,
więc symetria jest z `lemmas`, a nie z cechami.
Do przeczytania jest, czy podział lematami rozłącza czytania:
forma bywa dwoma lematami naraz, a warunek działa na czytaniu, nie na formie.

`olski-check` nie mówi, na czym zdanie stanęło, a `olski-corpus` mówi.
`Outcome.blocker` w `olski/coverage.py` nazywa część mowy tokenu,
na którym rozbiór się zatrzymał, i `Report.blockers` z tego rankuje kolejkę,
gdzie `Verdict` w `olski/subset.py` ma na odrzucenie jedno zdanie:
`no reading: nothing in olski derives this`.
Obie drogi wołają ten sam parser,
więc różnica jest w tym, co która z nich z niego wyjmuje, a nie w tym, co widzi.
Kolejność, w jakiej README ustawia braki gramatyki, z tego polecenia więc nie wychodzi:
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)
opisuje ją jako listę słów, których żadna produkcja nie bierze,
a [kryterium wyjścia toru](docs/roadmap.md#celem-toru-jest-to-readme)
każe ten sam przebieg powtarzać po każdej zmianie w gramatyce.
Ruchem jest zejście `blocker` na `Result` w `olski/parse.py`,
tak jak zeszedł tam `status`, który stał w obu klasach w dwóch kopiach,
plus segmenty, których `Verdict` nie niesie, a `blocker` ich potrzebuje,
i wypisanie rankingu przez `olski-check` nad plikiem.
Do przeczytania jest to, czy blocker liczony nad żywą morfologią
mówi cokolwiek ponad to, co mówi lista form nieznanych:
`docs/corpus.md` ostrzega, że przy wielu czytaniach formy
blocker nazywa pierwsze z nich,
a nad dokumentacją nikt czytań nie ujednoznacznia,
więc blocker jest tam zawsze tym przybliżonym.

`olski` chodzi po katalogu, a `olski-check` bierze tylko pliki.
`_collect` w `olski/cli.py` schodzi po `rglob`, pyta `is_plain_text` o każdy plik
i liczy to, co minął, żeby przebieg nad katalogiem nie lintował licencji,
a `main` w `olski/check.py` czyta po prostu każdą podaną ścieżkę.
Widać to w poleceniu, którym
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów: stoi przed nim `find`, bo inaczej nie ma czego podać.
Ruchem jest wyjęcie `_collect` z `olski/cli.py` do wspólnego miejsca
i zawołanie go z obu komend, po czym `find` z tamtego polecenia znika.
Do rozstrzygnięcia jest to, co druga komenda robi z pominiętymi:
`olski` mówi o nich, bo pominięcie zmienia mianownik częstości,
a `olski-check` ma już mianownik, o który się w tej sesji rozegrało,
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

Przecinek stoi na czele kolejki i sam nie kupuje nic.
`interp` prowadzi [tabelę blokerów](docs/corpus.md#where-the-analyses-stop),
przecinek jest w tym wierszu drugą formą po pauzie,
a pauza należy do rejestru, którego dokumentacja nie ma,
więc to przecinek jest tym, co ta tabela naprawdę stawia jako następne.
Ruchem jest koordynacja przecinkiem tam, gdzie stoi dziś spójnik:
`Clause`, `NP` i `AP` mają każde swoją produkcję ze spójnikiem
i żadne nie ma jej z przecinkiem.
Przeczytane jest to, co te trzy produkcje robią nad prozą wyciągniętą z README,
i nie robią nic:
zdanie, które niesie w tym pliku przecinek,
niesie też zdanie podrzędne, przysłówek albo rzeczownik odczasownikowy,
więc reguła sama z siebie nie wyprowadzi tam ani jednego zdania
i wchodzi razem z podrzędnym albo nie wchodzi wcale.
Jest to własność całej kolejki, a nie tej jednej reguły,
i pomiar nad czterema pozostałymi konstrukcjami trzyma
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop).
Do przeczytania zostaje cena nad Składnicą,
bo przecinek między zdaniami konkuruje z przecinkiem w grupie imiennej
wszędzie tam, gdzie po przecinku stoi rzeczownik,
a to jest ta wieloznaczność, której olski nie znosi.

Rzeczownikowe czytanie przymiotnika zabiera README jedno zdanie.
`Linter pomaga pisać dobry kod.` wychodzi dwoma czytaniami tego samego kształtu,
bo Morfeusz daje `dobry` czytanie `subst:sg:nom.acc:m3` obok przymiotnikowego,
a `kod` czytanie lematu `koda` w dopełniaczu mnogim,
więc `dobry kod` jest raz przymiotnikiem przed rzeczownikiem,
a raz rzeczownikiem z dopełniaczem po nim.
Wykluczenie z `admissible` w `olski/subset.py` tu nie dochodzi,
bo żąda naraz czytania nieodmiennego i wyrazu funkcyjnego obok niego,
a to czytanie odmienia się i wyrazu funkcyjnego przy sobie nie ma;
[`docs/corpus.md`](docs/corpus.md#what-morphological-ambiguity-costs)
trzyma tę samą granicę zmierzoną na `sam` nad bankiem drzew.
Zdanie jest pierwszą połową pary, którą README stawia obok siebie,
a druga połowa się wyprowadza,
więc stoi na nim [kryterium wyjścia toru](docs/roadmap.md#celem-toru-jest-to-readme).
Ruchem jest kryterium, a nie ten jeden przypadek,
i pierwszym pytaniem jest, czy jakiekolwiek kryterium tu jest.
Warunek na kształt drzewa — odpada czytanie rzeczownikowe formy,
którą Morfeusz zna też jako przymiotnik, jeśli stoi przed dopełniaczem —
zabiera każde zdanie, w którym rzeczownik odprzymiotnikowy dopełniaczem rządzi.
Do przeczytania jest więc, ile takich zdań niesie Składnica,
bo w prozie tego repozytorium jest ich tyle, co to jedno.

Nazwisko ze słownika zabiera README drugie zdanie.
`Celem jest parser tego podzbioru.` wychodzi dwoma czytaniami tego samego kształtu,
bo Morfeusz daje formie `Celem` lemat `Cel:Sm1` obok lematu `cel`,
czyli nazwisko obok rzeczownika pospolitego, oba w narzędniku liczby pojedynczej.
Wykluczenie z `admissible` w `olski/subset.py` tu nie dochodzi,
bo żąda czytania, które się nie odmienia, a nazwisko się odmienia;
[`docs/subset.md`](docs/subset.md#the-dictionary-offers-readings-polish-does-not)
wymienia `Tam` jako ten sam przypadek
i mówi, dlaczego etykieta słownika tej klasy nie oddziela.
Klasa jest szersza niż to jedno zdanie,
bo czytanie nazwiskowe uprawdopodabnia wielka litera,
a wielką literą zaczyna się każde zdanie,
więc dotyczy każdego rzeczownika stojącego w tej pozycji.
Ruchem jest kryterium na pozycję:
czytanie nazwiskowe odpada tam, gdzie wielka litera bierze się z początku zdania,
a nie z samego wyrazu.
Do przeczytania jest, ile zdań Składnicy takie kryterium zabiera,
bo nazwisko na początku zdania jest w gazecie zwyczajne,
a w dokumentacji go nie ma;
stoi na tym [kryterium wyjścia toru](docs/roadmap.md#celem-toru-jest-to-readme).

Jedna forma o dwóch czytaniach nominalnych daje olskiemu dwa czytania zdania.
`wejście` ma w Morfeuszu czytanie `subst` i czytanie `ger`,
a sygnatura czytania w `olski/parse.py` rozróżnia części mowy,
więc produkcja z `ger` w głowie grupy imiennej
daje `Wejściem jest zwykły tekst polski.` drugie czytanie tego samego kształtu
i zabiera jedno z tych zdań, które olski dziś przyjmuje;
[`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop) mierzy ten spadek.
Rozstrzygnąć da się w dwóch miejscach i wybrać trzeba jedno.
Albo `admissible` w `olski/subset.py`,
które dziś żąda czytania funkcyjnego obok rzeczownikowego
i tej pary nie obejmuje, dostaje drugie kryterium.
Albo sygnatura przestaje liczyć część mowy tam, gdzie kształt drzewa jest ten sam,
co jest tym samym argumentem, którym już pomija lematy,
i wtedy `do` jako przyimek i jako nuta dalej są dwoma czytaniami,
bo różnią się kształtem.
Do przeczytania jest, ile takich par ten rejestr niesie:
formy z czytaniem `ger` i `subst` naraz
nad prozą wyciągniętą z dokumentów tego repozytorium,
bo jedno zdanie nie mówi, które z dwóch wyjść jest warte swojej maszynerii.
Wpis stoi przed rzeczownikiem odczasownikowym w gramatyce, a nie za nim,
bo reguła dodana pierwsza obniża pokrycie
i sesja, która ją doda, zmierzy spadek zamiast zysku.

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
The entry that takes `blocker` down to `Result` in `olski/parse.py`
moves the property the blocking form would be carried on,
so whichever of the two is taken first decides where it is computed
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
Wszystkie trzy są liśćmi — w `olski` nikt ich nie importuje poza nimi samymi —
a mimo to instalują się z pakietem (`include = ["olski*"]` w `pyproject.toml`)
i jeden z nich ma własną komendę,
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
czytnik banku drzew i dwa programy pomiarowe są w nim,
a nikt, kto lintuje tekst, ich nie woła.

Kto instaluje samego lintera, buduje przy okazji analizator morfologiczny.
`dependencies` w `pyproject.toml` żąda `morfeusz2` bezwarunkowo,
a tor linterowy nie sięga po niego ani razu:
`olski/cli.py`, `olski/engine.py`, `olski/checks.py`, `olski/document.py`,
`olski/rules.py`, `olski/calibration.py` i `olski/packs/` nie importują `olski/morph.py`,
czyli jedynego miejsca, w którym stoi `import morfeusz2`,
a wołają go `olski/parse.py`, `olski/subset.py`, `olski/corpus.py`
i `olski/coverage.py`, przez `subset` zaś także `olski/check.py`,
a przez `corpus` także `olski/attachment.py`.
[Sekcja Checks](CLAUDE.md#checks) opisuje środowisko,
w którym koło Morfeusza się nie zbudowało,
a `tests/test_morph.py`, `tests/test_subset.py` i `tests/test_corpus.py`
pomijają się zamiast wywracać zbiórkę.
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
`morph`, `parse`, `subset` i `check` zostają w pakiecie i dalej ciągną Morfeusza.
Do przeczytania jest, na których platformach PyPI ma gotowe koło,
bo to rozstrzyga, czy podział kupuje instalację, której dziś nie ma,
czy tylko nazywa dwa tory drugi raz:
`morfeusz2` 1.99.15 wchodzi na Linuksie x86-64 pod Pythonem 3.11
bez budowania czegokolwiek.

Jedyna deklaracja reguł poza pakietem nie jest przez nic ładowana.
`harness/counts.py` deklaruje cztery liczniki,
`tests/test_rules.py` sprawdza pakiety z `olski/packs/`,
a ten pakiet podaje się ścieżką do `--packs` i wchodzi tylko wtedy,
gdy ktoś ręcznie przelicza tabele w
[`docs/corpora.md`](docs/corpora.md#how-the-counts-here-were-taken)
albo w [`docs/generated-polish.md`](docs/generated-polish.md#what-was-measured).
Walidacja dzieje się przy budowie reguły,
więc zmiana w rodzajach checków albo w ich parametrach
przewraca ten plik dopiero w środku przebiegu, który trwa minuty.
Ruchem jest test ładujący go tak, jak ładuje go `--packs`.
Przeciw: reguł tego pakietu nie da się sprawdzić tak, jak sprawdza się wysyłane,
bo o polszczyźnie niczego nie twierdzą i po to stoją poza linterem,
więc zostaje z tego asercja, że plik się wczytuje,
i trzeba zdecydować, czy tyle jest warte testu.

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
