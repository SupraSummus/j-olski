# Work to do in the repository

The running list of work inside the repository itself:
rewrites, merges, documents that have drifted apart,
dangling references, gaps, and code worth improving.
Something noticed while working on another topic goes here
instead of stretching the current change or being forgotten.
[The review pass](CLAUDE.md#the-review-pass) is the other way in:
a refactor too large to do on the spot is written down rather than started,
and the review also checks whether a change deleted the entries it closes.
Read the list before starting new work,
because it names the problems somebody has already found.

Lista nie przypisuje wpisów do torów i nikt nie podnosi ich po kolei,
bo wpis notuje tylko to, na co ktoś trafił przy innej robocie.
[docs/roadmap.md](docs/roadmap.md#co-jest-budowane) mówi, co jest budowane.

An entry belongs here only if a commit in this repository closes it.
A question the outside world answers is not work in the repository,
and the document that owns the topic keeps it:
[`docs/open-questions.md`](docs/open-questions.md)
or a document's own `Not yet decided`.
The next move is the tell:
waiting for somebody else's answer is an entry there,
a file to write is an entry here.

A register, not a changelog:
an entry that closes is deleted by the same commit that settles it,
which is the done-marker rule from
[`CLAUDE.md`](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
applied to this file.

One paragraph per entry, paragraphs separated by a blank line,
lines inside them broken [semantically](CLAUDE.md#semantic-line-breaks),
and no bullets or numbering,
so that adding or removing an entry gives a clean diff
and leaves its neighbours alone.
Numbering renumbers everything below an entry landing in the middle,
and a bullet indents prose that is meant to read as prose.

Podział na sekcje zachowuje ten czysty diff,
więc każdy wpis należy do jednej sekcji.
Nazwa sekcji mówi, czego wpis dotyka, a nie co jest budowane.
Wpis sięgający dwóch sekcji dopisz do tej,
która obejmuje dowód do przeczytania,
bo od dowodu zaczyna ten, kto wpis podnosi.
Sekcję bez wpisów skasuj razem z ostatnim wpisem, który z niej wyszedł,
a nową sekcję załóż dopiero wtedy, gdy masz do niej wpis.

An entry that names another one names it by what it is about.
A section name does not identify one, since a section holds many,
and a pointer saying which way to scroll is wrong
as soon as anything lands between the two.

Write so that an entry can be picked up cold,
and name the concrete next move —
what actually has to change in the text or in the code.
"Check some day" is a hope, not a move.
Name the evidence to read as well, and not only the files to change,
because two entries over disjoint files can turn on one judgment
that a file list does not show,
and what such an overlap costs is in
[splitting work across sessions](CLAUDE.md#splitting-work-across-sessions).

Wpis nie jest rozstrzygnięciem, bo autor pisał go przy innej robocie
i dał mu tyle uwagi, ile zostało.
Pewne jest w nim jedno: autor na coś trafił.
Kto wpis podnosi, dochodzi więc do ruchu sam
i traktuje nazwany ruch jako propozycję, a nie jako polecenie.
Czasem wychodzi mu ruch inny, a czasem żaden,
bo problemu nie ma albo naprawa kosztuje więcej, niż jest warta;
wtedy całą zmianą jest skasowanie wpisu, z powodem w komunikacie commita.

## Dokumenty i konwencje

`docs/corpus.md` and `docs/corpora.md` differ by two letters
and hold unrelated things:
the first measures the grammar against the Składnica treebank,
the second surveys the corpora of human Polish this repository can obtain.
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
The package has the same collision and the same argument settles it.
`olski-corpus` runs `olski/coverage.py`,
where `olski/corpus.py` is the treebank reader beside it,
so the command, the module and the document
are three names for what a reader takes to be one thing.
Renaming the document alone leaves the module and the command as they are,
which is why they are one entry:
what has to be decided is what these things are called,
and the answer for the document is the answer for the other two.
The entry about the harness boundary reaches the third of them on its own grounds,
since one of the two answers it offers moves the treebank reader to `harness/`
and takes the command along as `python3 -m harness.coverage`,
which leaves nothing there to rename,
so whichever entry is picked up first is answering for the other.

[Semantic line breaks](CLAUDE.md#semantic-line-breaks) cover
"prose in comments and docstrings", and the code is divided about it.
`olski/skład/`, `opowieści/`, `olski/walencja.py` and `harness/ustawy.py`
break their comments at boundaries of meaning,
and everything else in `olski/`, `harness/` and `sonda/` wraps to a column.
`olski/parse.py` holds both kinds,
which is what [lazy adoption](CLAUDE.md#adopt-these-rules-lazily) produces
where a rule reaches a file already written the other way.
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

`docs/subset.md` jest dokumentem mieszanym.
Polskie sekcje dopisano tam do angielskiego dokumentu,
a [reguła językowa](CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
żąda przekładu całego pliku.
Ruchem jest przekład reszty, jednym commitem, bo mieszanina jest tym,
co ta reguła liczy jako koszt, a pół dokumentu przełożonego jej nie zdejmuje.
Wpis ważył więcej, dopóki lista plików była zasięgiem checka;
checka nie ma, więc został sam powód, dla którego ta reguła stoi.

`docs/open-questions.md` trzyma listę decyzji zamkniętych,
a każda z nich ma właściciela gdzie indziej.
Sekcja `Settled` powtarza to, co jest budowane, wraz z kierunkiem toru
([`docs/roadmap.md`](docs/roadmap.md#tor-gramatyczny-nie-ma-końca)),
wycofanie toru linterowego ([`docs/linter.md`](docs/linter.md#what-closed-the-track)),
bliskość polszczyzny
([`docs/design-notes.md`](docs/design-notes.md#decisions-taken)),
i słownik morfologiczny,
czyli tę jedną decyzję, przy której `docs/design-notes.md` pisze wprost,
że nie jest zapisana dwa razy.
Ruchem jest usunięcie sekcji na rzecz zdania mówiącego, gdzie decyzje zapadłe stoją,
czyli [zakaz znaczników zrobionego](CLAUDE.md#documents-describe-the-present-git-owns-the-past)
zastosowany do listy otwartych pytań.
Przeciw: lista zamkniętych rozwidleń oszczędza komuś otwierania ich z powrotem.
Do przeczytania jest więc, czy któraś pozycja niesie odrzuconą alternatywę,
której jej właściciel nie trzyma — taka zostaje, a reszta idzie.

Lista dokumentów w README miesza dwa tory, które sekcja nad nią rozdziela.
[`Co działa`](README.md#co-działa) mówi, że działają dwie rzeczy,
a lista pod nią biegnie bez podziału i rośnie z każdym dokumentem,
więc czytelnik toru gramatycznego i czytelnik toru składu
przechodzą przez cudze pozycje, zanim dojdą do swoich.
Ruchem jest pogrupowanie listy — tor gramatyczny, tor składu,
to, co obsługuje oba, i zapis toru wycofanego — bez ruszania linków,
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
Wpis waży mniej, odkąd tamten dokument jest zapisem, którego nic nie rusza:
zostaje z niego czytelnik trafiający na to samo wyprowadzenie dwa razy,
a nie dwie kopie, które się rozjadą.

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

## Komendy i sondy

Sonda różnicowa nad prozą bierze jeden plik, a rejestr ustaw to siedem plików.
`main` w `sonda/ruch.py` rozgałęzia się na katalog, który czyta jako Składnicę,
i na plik, który czyta jako prozę, więc siedmiu aktów nie ma jak podać:
figury nad tym rejestrem trzeba wziąć po zlepieniu ich w jeden plik,
i to zlepienie jest krokiem, którego dokument nie ma jak wydrukować obok liczby,
a [`docs/ustawy.md`](docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze)
cytuje ruch każdej konstrukcji nad tym rejestrem osobno.
Ruchem jest wiele ścieżek prozy w jednym przebiegu, złożonych jednym raportem,
czyli to, co `przebieg` już robi nad lasami banku drzew:
`nad_prozą` bierze napis, a nie ścieżkę, więc scalanie jest w tym pliku gotowe.
Do rozstrzygnięcia zostaje, co robi ścieżka katalogu z prozą w środku:
Składnica też jest katalogiem, a rozpoznawanie po rozszerzeniu plików w środku
byłoby trzecim znaczeniem jednego argumentu.

`olski` chodził po katalogu, a `olski-check` bierze tylko pliki.
Widać to w poleceniu, którym
[`docs/extraction.md`](docs/extraction.md#what-the-numbers-here-were-run-over)
bierze liczbę fragmentów: stoi przed nim `find`, bo inaczej nie ma czego podać.
Komenda, która po katalogu chodziła, wyszła razem z torem lintera,
a chodzenia po drzewie nie ma teraz żadna z dwóch, które zostały:
`main` w `olski/check.py` i `main` w `olski/wieloznaczność.py`
czytają po prostu każdą podaną ścieżkę, więc obu rozwija się je powłoką.
Ruchem jest jedno miejsce, które schodzi po `rglob`,
bierze pliki o rozszerzeniu, które ekstrakcja pisze,
pomija katalog o nazwie zaczynającej się kropką — bo korpus stoi w repozytorium,
a jego kontrola wersji korpusem nie jest — i woła się z obu komend,
po czym `find` z tamtego polecenia znika.
Przeciw pominięciu: katalog z kropką podany wprost staje się wtedy nieosiągalny,
więc należy ono do chodzenia, a nie do testu na rozszerzenie.
Do rozstrzygnięcia jest, czy komenda mówi o plikach, które minęła:
`olski-check` ma mianownik, który tamten dokument cytuje,
więc pominięcie w ciszy zmienia figurę, o której nikt się nie dowie.

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
Wzorem jest wołanie `main` z listą argumentów i czytanie `capsys`,
czyli to, co robi `tests/test_attachment.py`.
Testem nie jest wydruk przepisany wiersz po wierszu:
kosztuje przy każdej zmianie układu
i nie broni niczego, czego by czytelnik nie zobaczył.
Warte pisania są dwie rzeczy: podsumowanie, bo jest figurą, którą cytuje dokument,
i kody wyjścia, bo widzi je tylko ten, kto komendę wpina w potok.

`sonda/luka.py` przepisuje z `sonda/ruch.py` cały przebieg różnicowy:
liczniki, przejścia, scalanie kawałków, tryb nad prozą, tabelę i wiersz poleceń,
czyli około stu osiemdziesięciu wierszy stojących drugi raz.
Połowa powodu, dla którego nie dało się ich wziąć stamtąd, zeszła:
`Sonda.dopisuje` daje wariant bogatszy od mianownika,
a odsiew grup działa nad dopiskiem tak samo jak nad produkcjami olskiego,
czego dowodem jest `sonda/przysłówek.py`, która nic z `ruch.py` nie przepisuje.
Zostaje to, że warianty luki są dwiema wersjami jednego dopisku,
a nie jednym wariantem na grupę zdejmowaną osobno:
wariant ostatni nie jest wtedy „obie naraz”,
więc `pytania` i `Raport._konkurencja` — dwa wiersze o tym,
czy grupy wchodzą sobie w drogę — nad nimi nie znaczą nic.
Ruchem jest `Sonda` biorąca gramatykę wariantu wprost, funkcją zamiast grupy,
wraz z konkurencją zepchniętą do sond, które grupy zdejmują.
Do przeczytania są właśnie te dwa pola, bo to one się nie generalizują,
oraz `gramatyka` w `ruch.py`, która jest jedynym miejscem
wiążącym wariant z grupą produkcji, i `dopisuje` obok niej,
bo dopisek wchodzący przed odsiewem jest tym, co funkcja wariantu ma zastąpić.
Tej samej maszynerii żąda z drugiej strony wpis o figurach
`docs/corpus.md` bez polecenia:
tam wariantem są dwie gramatyki, a nie dwie morfologie,
więc ten, kto podnosi którykolwiek z dwóch, wybiera kształt dla drugiego,
i jest to jedna sesja.

Klasa `verb` w `NOMINALIZATION` z `harness/endings.py`
stoi przed każdą nominalną,
co jest słuszne dla `zostanie` i niesłuszne dla `dacie`.
Oba niosą czytanie czasownikowe obok nominalnego,
a dokument datujący fakturę ma na myśli miejscownik od `data`
tam, gdzie ta kolejność wpisuje drugą osobę liczby mnogiej od `dać`,
więc udział form odmienionych cytowany w
[`docs/linter.md`](docs/linter.md#what-the-nominalization-endings-match)
jest podłogą, a nie liczbą.
Ruchem jest albo kolejność, którą rozstrzyga korpus —
czytanie nominalne przed czasownikowym tam, gdzie czasownikowe jest osobą,
której rejestr nie używa — albo podłoga wypisana tam, gdzie udział jest cytowany,
czyli w tamtej sekcji i nigdzie indziej.
Dowodem jest 7 słów: 6 razy `dacie` i raz `powiecie`,
a rejestr obu używa jako rzeczowników.
Waga wpisu spadła razem z torem, który tę sondę zamawiał:
figura, którą on prostuje, jest teraz częścią zapisu o czymś wycofanym,
a nie liczbą, na której coś stoi.

`Cena trzecia` w
[`docs/design-notes.md`](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)
opiera się na zdaniu, którego README nie ma.
Cytuje `Zbiór tekstów przechodzących przez wszystkie reguły
jest podzbiorem polszczyzny w jednym i w drugim przypadku`
i liczy je ponad sześć sekund,
a README niesie to zdanie z drugim członem,
`a wyznaczenie go przez wykluczanie jest nieporównanie tańsze`,
którego słów sonda nie przyłącza:
dziedziny przycinają się wcześnie
i cały plik kończy się najwolniejszym czasem poniżej dziesiątej części sekundy.
Sam cytat podany przez `-c` liczy się ponad osiem sekund,
więc zjawisko zostaje, a przykład z tego pliku wyszedł.
Rozjeżdża się razem z nim drugie zdanie tamtego akapitu:
mówi ono o `dokładnie jednym` zdaniu odrzuconym bez ani jednej formy spoza produkcji,
gdzie [`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop) liczy takich pięć.
Do przeczytania jest ten akapit obok `python3 -m sonda proza/README.txt`
i tego samego zdania podanego przez `-c`.
Ruchem jest albo zdanie, które README naprawdę ma i które ten czas pokazuje,
albo powiedzenie tej ceny bez zdania z tego pliku.
Liczby w tamtym akapicie zostały nieprzeliczone razem z resztą,
bo przeliczenie jednej z nich w wywodzie bez dowodu czyta się jak uzgodnienie.
Widać to teraz po samej sekcji: mówi ona wyżej o 48 zdaniach prozy README,
a ten akapit o pozostałych 42, i różnicy nie tłumaczy w niej nic.
Wpisu o figurach nad własną prozą to nie zamyka:
tamten pyta, czy mianownik w ogóle zapisywać.

## Korpusy, ekstrakcja i figury

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
so every figure over those is counted by hand.
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

Figury, które [`docs/corpus.md`](docs/corpus.md#the-measurement) bierze ręcznie,
są w większości sondami różnicowymi i nie ma ich czym puścić.
Wiersz `prep` z jedną grupą produkcji zdjętą, ten sam z drugą, trzydzieści pozycji
przyłączeniowych zdjętych naraz oraz kolumna najczęstszych form przy każdym blokerze
powstają dziś skryptem pisanym na jeden przebieg i kasowanym po nim,
a sekcja o nich wskazuje ten plik jako miejsce, gdzie stoi, co by je uwolniło.
`sonda/ruch.py` jest tym kształtem od tej strony, której brakowało:
sonda deklaruje, do której grupy należy produkcja, a przebieg, warianty i tabelę
dostaje gotowe, więc dwie pierwsze figury są predykatem i sześcioma wierszami deklaracji.
Brakuje temu przebiegowi jednej rzeczy, której te figury żądają, a przecinek i liczebnik nie:
liczy on przejścia werdyktu, a nie blokery, więc wiersz `prep` nie ma skąd wyjść.
Ruchem jest licznik blokerów na wariant w `Raport`, wzorowany na `Report.blockers`
z `olski/coverage.py`, i dwie sondy na te dwie grupy produkcji.
Nie obejmuje to jednej figury z tamtej listy: kolumna bez wykluczenia słownikowego
jest wariantem morfologii, a nie grupy produkcji, i pod ten kształt nie podchodzi.
Do rozstrzygnięcia jest przy tym, czy sonda na figurę, którą czyta jeden dokument,
zarabia na siebie, czy taniej jest wpisać kryterium obok liczby,
co [tamta sekcja](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)
robi dla trzydziestu pozycji i co pozwoliło wziąć tę liczbę drugi raz.

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

Wieloznaczność rejestru ustaw jest w jednym dokumencie policzona dwa razy i różnie.
[Odczyt z § 6](docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)
mówi o 228 zdaniach wieloznacznych, czyli o 77% tych, którym olski daje czytanie,
a [tabela wyżej](docs/ustawy.md#co-gramatyka-z-tego-wyprowadza) w tym samym dokumencie
ma 272 na 344, czyli 79%, i to tabela zgadza się z przebiegiem.
Tamta sekcja ma jeszcze dwie liczby z tego samego przebiegu:
zdań o czytaniach liczniejszych niż `MAX_READINGS` jest 21, a nie osiemnaście,
a porównanie ze Składnicą mówi 27% (122 wieloznaczne na 447 przeczytanych),
gdzie przebieg oddaje 32% (549 na 1728, [`docs/corpus.md`](docs/corpus.md#the-measurement)).
Najdłuższe zdanie stoi niezmienione na 28 042 czytaniach,
a zdanie o tym, że czytania różnią się najczęściej podmiotem i dopełnieniem,
przebieg potwierdza: 160 razy podmiot i 112 dopełnienie na `differing in`.
Ruchem jest więc poprawka samych liczb wraz ze zdaniami, które je czytają,
a do przeczytania są oba polecenia, które ten dokument drukuje.
Ekstrakcja rozejścia nie tłumaczy, bo zdań jest dalej 4921.
Tabelę ktoś nad tym przebiegiem poprawił, a tamtej sekcji nie,
więc poprawka ma przejść cały dokument, a nie same liczby wypisane tutaj.

## Gramatyka, parser i pomiar pokrycia

Terminal nie umie zażądać, żeby forma jakąś cechę w ogóle niosła,
a bez tego przysłówek wchodzi do gramatyki połową albo wcale.
`word("adv", degree="pos.com.sup")` bierze `tu` tak samo jak `bardzo`,
bo `unify` w `olski/grammar.py` pomija cechę, której konstytuent nie niesie,
i pomija ją rozmyślnie — część mowy nieodmienna nie narusza zgodności,
w której nie bierze udziału — więc warunek odwrotny nie ma tam formy.
Stopień jest tą cechą, po której Morfeusz oddziela przysłówek odprzymiotnikowy
od pierwotnego, czyli klasę określającą przymiotnik od tej, która go nie określa,
i tego warunku żąda pozycja przy przymiotniku:
bez niego kupuje ona nad Składnicą zero i odbiera 39 zdań pozycji przy czasowniku,
a 15 z 47 zdań, które kupuje sama, olski czyta wbrew drzewu wzorcowemu
([`docs/subset.md`](docs/subset.md#naprawę-widać-w-tagsecie-i-nie-da-się-jej-postawić-w-gramatyce)).
Ruchem jest pole na `Word` wyliczające nazwy cech obowiązkowych,
sprawdzane w `bierze` obok testu na lemat, który już tam stoi.
Sonda po nim nie potrzebuje nowego wariantu, tylko drugiego terminala:
`PRZYSŁÓWEK` w `sonda/przysłówek.py` jest jeden i biorą go obie grupy,
a warunek należy do jednej z nich, więc grupa przy przymiotniku dostaje własny.
Razem z nim `gospodarz` ma poznać oba, bo pyta dziś o ten jeden,
a produkcja z drugim wypadłaby bez grupy — co zgłasza `tests/test_ruch.py`.
Porównanie biegnie potem między dwoma przebiegami sondy — przed warunkiem i po
nim — a nie między wierszami jednej tabeli.
Do przeczytania przed decyzją jest, czy podział na dwie klasy przysłówka trzyma
w drugą stronę: `bardzo lubię` stawia przysłówek stopniowany przy czasowniku,
więc warunek zawęża jednego gospodarza i nie zwalnia drugiego,
a zdania, w których gospodarze dalej się spierają, zostają po nim wieloznaczne.

Przysłówka gramatyka nie ma, a pozycja przy czasowniku jest wyceniona
i kupuje 428 zdań Składnicy, nie odbierając jednoznaczności żadnemu zdaniu
przyjętemu wcześniej
([`docs/subset.md`](docs/subset.md#przysłówek-zmierzono-przed-dopisaniem-i-drugi-gospodarz-odbiera-39-zdań)).
Zakup jest największy ze wszystkich zmierzonych i nie znaczy to, że jest do wzięcia:
lista okoliczników bierze przysłówki płasko,
więc `Program zapisuje ustawienia bardzo szybko.` wychodzi jednym czytaniem,
w którym `bardzo` jest okolicznikiem zdania na równi z `szybko`,
a zgodność ról nad bankiem drzew tej pomyłki nie widzi,
bo porównuje podmiot i dopełnienie.
Nie widzi jej też streszczenie czytania:
`DEKLARACJA` w `olski/subset.py` nie ma roli na przysłówek,
więc werdykt nie nazywa ani tego, który określa zdanie, ani tego, który nie,
i pozycja dopisana bez tej roli daje `valid` bez słowa o tym, co przyjęła.
Ruchem jest decyzja, czy pozycja wchodzi przed warunkiem z wpisu wyżej,
a przed nią pomiar tego, ile zdań Składnicy dostaje ten płaski kształt:
mierzy się on nad wariantem sondy, a nie nad gramatyką, i nie jest zmierzony.
Wpis wyżej i ten stoją na jednym rozstrzygnięciu — czy przysłówek ma dwie klasy —
więc jedna sesja podnosi oba albo żaden.

Dopełnienie stoi przed swoim czasownikiem w czterech szykach dopisanych,
a przed bezokolicznikiem, który je bierze, nie stoi w żadnym.
Ciała biorą `Verb`, czyli formę osobową, więc `premier większości nie może
ruszyć` dalej wychodzi z jednym podmiotem i bez dopełnienia,
i jest to jedno zdanie Składnicy, które olski czyta odwrotnie, niż czyta je
czytelnik
([`docs/subset.md`](docs/subset.md#cena-stoi-w-trafności-a-nie-w-liczbie-czytań)),
a pomyłka jest droższa od wieloznaczności, bo werdykt `valid` ktoś przeczyta.
Do przeczytania jest, ile ta pozycja zabiera poza tym jednym zdaniem:
dopełnienie przed łańcuchem `może ruszyć` konkuruje z przydawką dopełniaczową
tam, gdzie cztery szyki już konkurują z nią przed formą osobową,
i cenę tamtych czterech zna
[`sonda/szyk.py`](sonda/szyk.py) — cztery zdania —
więc ta pozycja ma z czym się porównać, zanim zapadnie decyzja.
Ruchem jest ciało `Complements`, a nie piąty szyk:
pozycję ramy niesie fraza bezokolicznikowa
([`docs/subset.md`](docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej)),
więc dopełnienie przed nią stoi wewnątrz orzeczenia,
a nie w kolejności podmiotu wobec czasownika.
Sonda różnicowa nad tym jednym ciałem, wzorowana na `sonda/szyk.py`,
idzie przed decyzją.

Forma `nie` ma u Morfeusza czytanie zaimkowe, którego polszczyzna w tym miejscu
nie ma: jest to biernik `on` w postaci popodstawowej, czyli tej, która stoi
wyłącznie po przyimku (`na nie`, `za nie`).
Grupa imienna bierze `ppron3` bez warunku, więc to czytanie stoi w każdej
pozycji dopełnienia, i to ono odbiera jednoznaczność jedynemu zdaniu,
które ją nad trzema rejestrami straciło przy wpuszczeniu negacji
([`docs/subset.md`](docs/subset.md#negacja-zmierzona-kupuje-148-zdań-i-odbiera-jedno)).
Kryterium słownikowe `admissible` w `olski/subset.py` po nie nie sięga,
bo wyrzuca rzeczownik nieodmienny, a tu chodzi o zaimek,
i cecha, po której to czytanie widać, jest inna: `praep` w tagu.
Ruchem jest warunek `npraep` na terminalu zaimka w grupie imiennej wraz z drogą
dla grupy pod przyimkiem, która `praep` brać musi, a przed nim pomiar,
ile czytań ten warunek zdejmuje nad Składnicą:
tagów `praep` jest w niej więcej niż samo `nie`.

Zamknięta lista kopul nie ma `stawać się` ani `okazywać się`,
a polszczyzna orzeka nimi narzędnik tak samo jak `zostawać`.
`Mao stał się na wiele lat przywódcą największego narodu na kuli ziemskiej.`
i `Człowiek staje się wyleniałym tygrysem.` są przez to odrzucone,
i są to dwa z 75 zdań, które zawężenie narzędnika odrzuca nad Składnicą,
a jedyne dwa, które odrzuca niesłusznie
([`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)).
Przeszkodą nie jest lista, tylko cząstka: `KOPULA` w `olski/subset.py` jest
warunkiem na lemat, a te dwa czasowniki są kopulami wyłącznie z `się`,
którego produkcja kopuli nie ma gdzie postawić —
[`docs/subset.md`](docs/subset.md#what-the-grammar-covers) mówi to przy liście.
Ruchem jest ramka narzędnikowa w leksykonie zwrotnym,
czyli ta sama droga, którą walencja rozdziela formę z cząstką od formy bez niej,
a do przeczytania jest, co zwrotna kopula robi z `Ludzie rodzą się wolni.`,
gdzie orzecznik zgodny stoi dziś przy czasowniku zwrotnym niebędącym kopulą.

Współrzędność wypisuje się trzema produkcjami, a mogłaby jedną, lewostronnie rekurencyjną.
`X → X conj X` powiedziałoby o zasięgu to samo co trzy poziomy z `build`
w `olski/subset.py`, bo zawężenie zasięgu stoi na rodzaju,
którego koordynacja nie ma
([`docs/subset.md`](docs/subset.md#nothing-above-a-coordination-distributes-into-it)),
a nie na kształcie produkcji.
Przeciw takiej produkcji był parser i już go nie ma:
tablica Earleya bierze lewą rekursję, co pilnuje `tests/test_subset.py`.
Różni te dwa zapisy liczba czytań ciągu współrzędnego,
bo wyprowadzeń tego samego ciągu jest pod nimi inaczej wiele,
i to jest jedyne, co tu jest do zmierzenia.
Do przeczytania są figury, które nad tymi poziomami bierze
[`sonda/przecinek.py`](docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania),
bo zmiana rusza je razem z werdyktami.
Ruchem jest jedna produkcja w miejsce trzech, o ile pomiar pokaże,
że czytań nie przybywa; przy przeciwnym wyniku ruchem jest samo zdanie w tej sekcji
mówiące, że wybór padł na trzy poziomy dla liczby czytań, a nie dla parsera.
Widać na czym mierzyć: zdanie ustawy o siedmiu członach ma dziś 28 042 czytania
([`docs/ustawy.md`](docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)),
i nie jest policzone, ile z tej liczby bierze sama współrzędność.

Gospodarz o dwóch kształtach ma dwie głowy, a werdykt nazywa jedną i nie mówi którą.
`Organ gminy może wyznaczyć swojego przedstawiciela do udziału w zgromadzeniu.`
daje wiersz `„do udziału” → „może”, „przedstawiciela”`,
a grupa imienna nazwana tam `przedstawiciela` jest w innym czytaniu grupą,
w której głową jest `swojego`:
przymiotnik ma czytanie rzeczownikowe, a rzeczownik dopełniaczowe,
czyli tę samą parę, o którą pyta wpis o rzeczownikowym czytaniu przymiotnika.
Wybór między tymi dwiema nazwami robi porządek, w jakim las wydaje drzewa,
bo `_przedstawiciel` w `olski/parse.py` bierze pierwsze z nich,
a porządek ten idzie po rozpiętościach córek (`ciała` w tym samym pliku)
i o tym, która głowa nazywa grupę imienną, nie mówi nic.
Formom to nie grozi, bo konstytuent ma je w każdym czytaniu te same.
Ruchem jest albo obie głowy w tym wierszu, albo pierwsza z zadeklarowanym kryterium.
Przeciw pierwszemu: wiersz przyłączenia mówi o jednym wyborze,
a `swojego` bierze się z czytania słownikowego, nie z przyłączenia,
więc wiersz zaczyna mówić o dwóch wieloznacznościach naraz;
przeciw drugiemu: kryterium na kształt grupy imiennej to gramatyka pisana drugi raz.
Do przeczytania jest, jak często rejestr ustaw taki wiersz wydaje,
bo od tego zależy, czy ten wpis jest wart ceny któregokolwiek z dwóch ruchów.

Czas przeszły zostawił za sobą 297 zdań Składnicy, których nikt nie przeczytał.
`praet` prowadził kolejkę blokerów z 2934 zdaniami,
a po dopisaniu tej formy do `Verb` w `olski/subset.py` wiersz ten czytał 297,
i są to zdania, które na czasie przeszłym stawały i dalej na nim stają.
Wiersz czyta dziś 331 ([`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)),
a 34 dołożył liczebnik, przesuwając na czasownik blokery zdań, których nie przyjął,
więc do przeczytania jest cała ta resztka, a nie tamte 297.
Nie wiadomo, czy stoi za tym jedna konstrukcja, czy dwadzieścia:
`Wózek zwolnił biegu i przystanął.` i `Pani Zofia była w rozpaczy.`
są w tej resztce obok siebie, a łączy je tyle, że bloker wskazał czasownik.
Ruchem jest odczytanie tej resztki i rozbicie jej na klasy,
z tego klasy nazwane w [`docs/subset.md`](docs/subset.md#what-it-does-not-cover-yet),
jeśli któraś jest konstrukcją, a nie zbiegiem okoliczności.
Do przeczytania jest sam `blocker` w `olski/coverage.py`:
nazywa on formę, na której rozbiór stanął,
a przy zdaniu z czasownikiem w środku bywa to forma stojąca za prawdziwą przyczyną,
więc część tej resztki może być artefaktem tego odczytu, a nie brakiem w gramatyce.

Aglutynant dochodzi tylko do czasownika, przy którym stoi.
`_formy_skończone` w `olski/subset.py` bierze `praet` z `aglt` po nim,
bo tak Morfeusz tnie `napisałem`,
a polszczyzna stawia tę końcówkę także przy innym słowie zdania:
`gdzieś ty był`, `myśmy przyszli`, `dlaczegoś to zrobił`.
Ruchem jest aglutynant przyłączany do zdania, a nie do czasownika,
czyli cecha osoby wypuszczana w górę z miejsca, w którym końcówka stanęła.
Do rozstrzygnięcia jest, czy warto:
konstrukcja jest w rejestrze technicznym rzadka albo nieobecna,
a w prozie literackiej Składnicy nie jest, i nikt nie policzył, ile jej tam.
Do przeczytania są zdania Składnicy, w których `aglt` stoi poza `praet`,
bo od ich liczby zależy, czy ten wpis jest wart ceny ruchu.

Zdanie względne z wysuniętym dopełnieniem żąda podmiotu, a polszczyzna go tam opuszcza.
Każde z dwunastu ciał `RelativeCore` z dopełnieniem ma w `olski/subset.py`
wypisany `podmiot_względny`, więc `Dyrektor wymienia imprezy, które zorganizował.`
nie wyprowadza się wcale, a `Dyrektor wymienia imprezy, które on zorganizował.` raz.
Nad Składnicą są to cztery zdania i wyszły one z
[pomiaru luki](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze),
który je kupił mimochodem, mierząc co innego:
cechy przeciąganej te cztery zdania do kupienia nie potrzebują.
Ruchem są ciała bez podmiotu obok tych z podmiotem,
czyli to samo, co zdanie główne ma w `ClauseConjunct → Predicate`.
Do przeczytania jest, ile ta pozycja dokłada wieloznaczności:
zdanie względne bez podmiotu konkuruje z czytaniem, w którym podmiotem jest zaimek,
a rodzina ta liczy piętnaście ciał i mnoży się przez szyk oraz przeczenie,
więc pierwszym pytaniem jest, czy ciał ma być dwanaście nowych, czy mniej.
Cenę i zakup bierze się sondą różnicową, tak jak przy każdym dopisaniu
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
a wpis jest winien przebiegi, których żąda [sekcja Checks](CLAUDE.md#checks).

Luka jest węzłem o pustej rozpiętości, więc rola wypełniona przez nią nie ma nazwy,
i na tym stanął pomiar cechy przeciąganej
([`docs/design-notes.md`](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)).
`agreement` w `olski/coverage.py` porównuje rozpiętości,
więc rozpiętość pusta nie trafia w żadną złotą i liczy się jako niezgodna —
wszystkie cztery zdania, jakie luka wyciągnęła ze Składnicy, wyszły tak,
choć role widoczne mają dobre.
Werdykt tej ceny nie płaci: luka stoi wewnątrz zdania względnego,
gdzie streszczenie nie zagląda,
więc o roli wypełnionej luką milczy tak samo jak o roli wypełnionej zaimkiem.
Ruchem jest luka wskazująca zaimek, który ją wiąże, a nie miejsce, w którym stoi:
etykieta roli nad zaimkiem, a nie nad pustym węzłem,
czyli to, co bank drzew robi na tych zdaniach.
Do rozstrzygnięcia jest, czy niesie ją produkcja, czy porównanie ról,
i różnicę robi to, że wybór po stronie gramatyki zostawia las, w którym rola ma słowo,
a wybór po stronie porównania zostawia las, w którym go nie ma.
Do przeczytania jest przy tym `Node.span` w `olski/parse.py`,
bo pole to wpisano pod produkcję o pustym ciele, a ta sonda jest jego pierwszym czytelnikiem.
Nie zamyka tego wpisu cała cena: warunek precedencji na lukę pilnuje pozycji w ciele,
a nie w napisie, więc zdanie zagnieżdżone dalej wychodzi dwoma kształtami,
i tę resztę zamyka to samo rozdzielenie dominacji od precedencji,
o które prosi wpis o szyku wypisanym w produkcjach.

Zaimek `który` stoi w polszczyźnie w trzech konstrukcjach, a olski ma jedną.
`RelativePronoun` w `olski/subset.py` bierze go na czele zdania względnego,
a `przymiotnik` w tym samym pliku odbiera mu pozycję przydawki,
więc pytanie — `Który aktor robi na tobie największe wrażenie?` —
i pytanie zależne — `Ustawy określają, które zadania mają charakter obowiązkowy.` —
nie wyprowadzają się wcale.
Pierwsze wychodziło wcześniej jako przymiotnik przed rzeczownikiem
i jest jedynym zdaniem, jakie warunek odbiera Składnicy pod Morfeuszem;
drugie wychodziło jako zdanie współrzędne po przecinku, czyli błędnie,
i cenę obu trzyma
[`docs/subset.md`](docs/subset.md#zaimek-względny-nie-jest-przymiotnikiem-przy-rzeczowniku).
Ruchem jest grupa imienna z zaimkiem pytajnym na czele,
wpuszczona w pozycji podmiotu i dopełnienia zdania pytającego
oraz w pozycji ramy tam, gdzie dziś stoi `SubordinateClause`.
Do rozstrzygnięcia jest przy tym, czy pytanie zależne jest tą samą pozycją ramy
co zdanie z `że`, czy osobną: leksykon walencyjny mówi o nich to samo,
a czasownik, który bierze jedno i nie bierze drugiego, tę pozycję rozdziela.
Do przeczytania jest, ile zdanie pytające w ogóle w tych rejestrach waży,
bo nad README nie ma go ani razu, a nad Składnicą `który` niesie i tę konstrukcję, i zdanie względne.

Zaimek względny wysunięty razem ze swoją grupą nie ma wyprowadzenia.
`RelativeModifier` w `olski/subset.py` bierze przyimek i sam zaimek,
a polszczyzna wysuwa razem z nim całą grupę, w której on stoi:
`ustawy, na podstawie której jest ono wydawane` jest zdaniem
„Zasad techniki prawodawczej”, które przez to przechodzi z wieloznaczności w odrzucenie
([`docs/subset.md`](docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka)).
Ruchem jest grupa imienna, w której zaimek stoi jako dopełniacz przy głowie,
z liczbą i rodzajem wypuszczonymi z zaimka, a nie z głowy,
bo to zaimek zgadza się z poprzednikiem, a nie rzeczownik, przy którym stoi.
Do rozstrzygnięcia jest, jak daleko ta grupa sięga:
polszczyzna wysuwa i `na podstawie której`, i `o którego zdaniu`,
a każdy kolejny kształt jest osobnym ciałem,
dopóki cechy nie przechodzą przez grupę imienną same.

Człon lewy ciągu współrzędnego nie unosi zdania względnego.
Produkcja `NP → NPConjunct RelativeClause` w `olski/subset.py`
żąda członu, a produkcja koordynacji daje po lewej człon i po prawej ciąg,
więc `pliki, które rosną, i katalogi` nie ma wyprowadzenia,
a `pliki i katalogi, które rosną` ma.
Ruchem jest symbol między `NP` a `NPConjunct`, przez który idą oba człony,
i ruch ten zbudowano na próbę, więc cena jest policzona, a zakup nie.
Cena ma trzy pozycje.
Nad Składnicą pod Morfeuszem jedno zdanie traci jednoznaczność —
`Przez czynniki ekonomiczne należy rozumieć te, które kształtują rozmiary
i strukturę dochodów oraz wydatków budżetowych.` wychodzi trzema czytaniami
zamiast jednego, bo `te, które kształtują rozmiary` staje się członem ciągu —
i jest to czytanie, które polszczyzna ma, więc nie jest to usterka, tylko cena.
Pod złotą morfologią nie rusza się ani jedno zdanie.
Trzecią pozycją jest `_role` w `olski/skład/rozbiór.py`:
czyta ono kształty gramatyki po etykiecie,
więc każdy nowy poziom kosztuje tam gałąź, a obieg zamknięty bez niej pada.
Do policzenia zostaje zakup, czyli ile zdań z takim ciągiem rejestr ma;
nad Składnicą i nad ustawami nie policzył ich nikt.
Dopóki tej liczby nie ma, wpis stoi po stronie ceny,
bo jednoznaczność płacona za pokrycie niepoliczone
idzie wbrew cenie kroku, której żąda
[`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę).

Wyrażenie przyimkowe przyłącza się do ostatniego członu ciągu współrzędnego
albo do zdania, a do całego ciągu nie przyłącza się wcale.
`Pliki i katalogi w tym drzewie rosną.` wychodzi dwoma czytaniami —
`Pliki i [katalogi w tym drzewie]` oraz `w tym drzewie` przy `rosną` —
a czytania, w którym w tym drzewie są i pliki, i katalogi, nie ma,
choć polszczyzna je ma.
Powodem są produkcje przyjmujące `Modifier`:
`NPConjunct` i `APConjunct` w `olski/subset.py` mają go pod głową członu,
a produkcje koordynacji nie mają go wcale.
[Zawężenie o przydawce](docs/subset.md#nothing-above-a-coordination-distributes-into-it)
tej pozycji nie uzasadnia, bo wywodzi się z braku rodzaju u ciągu:
przymiotnik nad ciągiem zgadzałby się z niczym,
a wyrażenie przyimkowe nie zgadza się z niczym również pod członem.
Ruch przepisuje tamtą sekcję, bo tytuł mówi tam o wszystkim,
co nad ciągiem stoi, a wywód pod nim o samej przydawce.
Żąda jej natomiast
[reguła o obu czytaniach wszędzie](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
bo pozycja z produkcją na jedno przyłączenie i bez produkcji na drugie
wybiera przez przeoczenie.
Ruchem są dwa ciała `NP` i dwa `AP`, po jednym na spójnik i na przecinek,
z `Modifier` za całym ciągiem.
`NP → NP Modifier` tym ruchem nie jest:
dałoby drugie wyprowadzenie każdej grupie bez koordynacji,
czyli czytanie, którego polszczyzna tam nie ma.
Do przeczytania jest
`test_pierwszy_artykuł_deklaracji_stoi_na_przyłączeniu_wyrażenia_przyimkowego`
w `tests/test_subset.py`, bo wylicza dwa czytania pierwszego artykułu Deklaracji,
a ruch dopisuje im trzecie.
Wpis jest winien przebiegi, których [sekcja Checks](CLAUDE.md#checks)
żąda od zmiany w gramatyce,
wraz z listą pozycji przyłączeniowych w
[`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
która rośnie o tę jedną.
Te same produkcje przepisuje wpis o współrzędności wypisanej trzema poziomami
zamiast jedną produkcją lewostronnie rekurencyjną,
więc ten z dwóch, który wejdzie pierwszy, wybiera kształt dla drugiego.

`pod względem` żąda licencji od słowa, do którego się przyłącza,
a olski żąda licencji tylko od dopełnienia.
Czytelnik odrzuca `wolni pod względem swej godności` bez pomocy składni,
bo `równy` ma pozycję na wzgląd, a `wolny` jej nie ma.
Tę samą obserwację robi nad `przewyższać`
[`docs/subset.md`](docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera),
gdzie porównanie mówi, w czym jedno przewyższa drugie,
i nie ma jej dziś gdzie zapisać.
Leksykon walencyjny mówi trzy zdania i wszystkie trzy zawężają ramę dopełnienia
([`docs/subset.md`](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)),
a okolicznik pozycji ramy nie zajmuje i przyłącza się do każdego czasownika za darmo,
więc żaden wpis nie odbiera czytania,
w którym wzgląd dochodzi do `rodzą się`.
Ruchem jest zdanie leksykonu odwrócone wobec tamtych trzech:
nie „ten czasownik czegoś nie bierze”, tylko „to wyrażenie przyimkowe
przyłącza się tam, gdzie licencjonuje je leksykon”,
czyli cecha przy przyimku zleksykalizowanym, a nie przy jego gospodarzu.
Robi ono z pierwszego artykułu Deklaracji zdanie olskie:
odejmuje czytanie z `rodzą się`, bo ten czasownik wzglądu nie licencjonuje,
a zostaje czytanie z `równi`, czyli jedno.
Odejmuje też czytanie nad całym ciągiem współrzędnym,
kiedy dopisze je wpis o wyrażeniu przyimkowym przyłączanym do ciągu,
bo `wolny` wzglądu nie licencjonuje tak samo.
Do rozstrzygnięcia jest, czy to jeszcze walencja, czy już ta warstwa,
którą [`docs/open-questions.md`](docs/open-questions.md#olski-melduje-wieloznaczność-której-czytelnik-nie-ma)
odkłada poza gramatykę jako odpowiedź trzecią;
różnicę robi to, że leksykon w gramatyce już jest, a tamta warstwa nie.
Do przeczytania jest, ile takich przyimków rejestr ma,
bo `pod względem` jest jednym z nich i nikt nie policzył, ile jest reszty,
oraz co Walenty mówi o wzglądzie:
pozycje zleksykalizowane wypisuje on w schemacie,
a przymiotnika, który licencjonuje tu wzgląd, nie ma w pliku czasownikowym,
z którego leksykon powstaje,
choć archiwum obok tego pliku niesie katalog przymiotnikowy.
Kryterium wejścia ma ten ruch to samo, co każda warstwa więzowa:
[wyprowadza się z gramatyki albo jest gramatyką pisaną drugi raz](docs/design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej),
a leksykalnie znaczy to tyle, że pozycję wypisuje słownik.
Jeśli Walenty jej nie wypisuje, ruchu nie ma i cały wpis zamyka skasowanie,
bo „brzmi nielogicznie” jest sądem o świecie, a nie faktem o słowie:
olski melduje wtedy wieloznaczność, tak samo jak melduje ją wszędzie indziej.

Apozycji olski nie ma, więc przecinek przed wyliczeniem ma u niego jedno czytanie.
`Przyszli moi sąsiedzi, lekarz i nauczyciel.` wychodzi jednym czytaniem,
`[moi sąsiedzi], lekarz i nauczyciel`, czyli ciągiem o trzech członach,
a polszczyzna czyta to zdanie także drugim sposobem,
w którym lekarz i nauczyciel są tymi samymi sąsiadami.
Jest to jednoznaczność z braku produkcji,
czyli to, czemu zapobiega
[reguła o obu czytaniach wszędzie](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
tyle że tam brakująca pozycja zostawiała zdanie odrzucone, a tu przyjęte,
więc po werdykcie nie widać jej wcale.
Ruchem jest produkcja apozycji, czyli człon, przecinek i drugi człon
w tym samym przypadku, i cena jest widoczna przed pomiarem:
przecinek jest już znakiem koordynacji na trzech poziomach
([`docs/subset.md`](docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania)),
więc apozycja dokłada czytanie każdemu ciągowi rozdzielonemu przecinkiem.
Do przeczytania jest, ile apozycji rejestr ma, bo bez tej liczby wpis jest samą ceną,
a gotowej nie ma gdzie wziąć:
[pomiar wieloznaczności](docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
wymienia apozycję wśród swoich zawyżeń, ale tę bez przecinka — `podpis CERTYFIKAT` —
czyli konstrukcję inną niż ta.
Pierwszym pytaniem jest więc, czy bank drzew rozdziela apozycję od koordynacji
etykietą, po której da się ją policzyć.

Fraza bezokolicznikowa jest gospodarzem przyłączenia, a werdykt nazywa nad nią zdanie.
`Syn usiłował wejść na ołtarz.` ma dwa czytania,
bo `na ołtarz` dochodzi do `wejść` albo do zdania nad nim,
a streszczenie mówi w obu `Modifier: na ołtarz → usiłował`,
czyli o jednym z nich nieprawdę:
`gospodarze` w `DEKLARACJA` w `olski/subset.py` wylicza
`NP`, `AP`, `ClauseConjunct` i `RelativeCore`, a frazy bezokolicznikowej nie,
więc `_gospodarze` w `olski/parse.py` wychodzi z niej do zdania.
Kosztuje to wiersz o przyłączeniu, którego nad takim zdaniem nie ma wcale,
a razem z nim wiersz o konstytuencie, bo wyklucza go rola stojąca pod konstytuentem
([`docs/design-notes.md`](docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań)),
więc nad 23 z 549 zdań wieloznacznych Składnicy
werdykt nie mówi nic poza liczbą czytań.
Ruchem jest `InfinitivePhrase` dopisane do tej listy,
po którym 20 z tych 23 dostaje wiersz o przyłączeniu,
a nad `Syn usiłował wejść na ołtarz.` jest to `„na ołtarz” → „usiłował”, „wejść”`.
Rejestr ustaw z tego ruchu nie ma nic: milczących werdyktów jest tam 7 z 272
i żadnego z nich fraza bezokolicznikowa nie tłumaczy,
więc do przeczytania są właśnie te siedem,
bo mieszczą klasę, której ten wpis nie nazywa.
Do przeczytania jest przy tym `tests/test_attachment.py`,
gdzie gospodarze są wypisani po symbolu,
oraz `_host` w `olski/parse.py`, bo streszczenie nazywa gospodarza jego głową,
a głową frazy bezokolicznikowej jest bezokolicznik i to on wejdzie do wiersza.

Grupa liczebnikowa w pozycji dopełnienia ma w banku drzew gniazdo,
którego porównanie ról nie czyta, więc dobre czytanie liczy się jako niezgodne.
`Marzec przyniósł 6 zagranicznych delegacji.` olski czyta tak, jak czyta je czytelnik,
a drzewo wzorcowe daje temu dopełnieniu `np(part)`,
czyli przypadek strukturalny, którym polszczyzna oznacza właśnie tę frazę,
i `_role` w `olski/corpus.py` nie tłumaczy tego gniazda na żadną rolę olskiego.
Gold nie ma wtedy dopełnienia, z którym można by się zgodzić,
a `agreement` w `olski/coverage.py` liczy rolę przypisaną poza gniazdem jako `disagrees`,
więc wiersz niezgodnych z [`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)
jest o jedno zdanie za długi i będzie rósł razem z liczebnikiem.
Ruchem jest `np(part)` odwzorowane na `Object` obok `np(acc)` i `np(accgen)`.
Do rozstrzygnięcia jest, czy to gniazdo jest dopełnieniem zawsze:
`Napiłem się wody` ma w nim dopełniacz partytywny, który dopełnieniem jest,
a olski go nie bierze, więc odwzorowanie nie zmieni na nim niczego,
i pytanie brzmi, czy bank drzew stawia tam kiedykolwiek coś, co dopełnieniem nie jest.
Do przeczytania są zdania Składnicy z tym gniazdem
wraz z werdyktem, jaki nad nimi wydaje `olski-corpus --morphology gold`,
bo tylko one mogą tę zmianę cokolwiek kosztować.
Ruch jest winien przebiegi, których [sekcja Checks](CLAUDE.md#checks)
żąda od zmiany w tabeli zgodności, i rusza ją w obu kolumnach.

Werdykt nad zdaniem mówi, na czym odrzucenie stanęło, a przebieg nad korpusem zgaduje.
`blocker` w `olski/coverage.py` nazywa część mowy pierwszego czytania formy
i sam w docstringu mówi, że między czytaniami wybiera dowolnie,
więc kolejka z [`docs/corpus.md`](docs/corpus.md#where-the-analyses-stop)
jest rankingiem stojącym na tym wyborze,
choć ten dokument opisuje ją jako listę słów, których żadna produkcja nie bierze.
Ruchem jest wycięcie czytań bez licencji przed rozbiorem,
po którym forma bez ani jednego czytania jest dla `blockera` brakiem licencji,
a nie brakiem struktury, którym ją dziś nazwie,
i wywód wraz z ceną tego wycięcia trzyma
[`docs/design-notes.md`](docs/design-notes.md#więzy-wchodzą-wyprowadzone-z-gramatyki-a-nie-napisane-obok-niej).
Rusza ono kolejkę, więc wpis jest winien przebiegi,
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
That net is what the grammar track now asks of every addition before it lands
([`docs/roadmap.md`](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę)),
so this part of the entry carries a rule rather than a convenience,
and a session that prices an addition by hand is doing this work and throwing it away.
Two probes in `sonda/` have already computed such a net by hand,
`przecinek.py` for the comma and `nieciągłość.py` for discontinuity,
and their transition tables are one table with different variants under it,
so the general version would replace both rather than start from nothing.
The entry about cutting unlicensed readings before the parse
moves what `blocker` reads off a form,
so whichever of the two is taken first decides what the blocking form is,
and they are one session.
The section that owns the reproduction path says meanwhile which figures are hand-taken,
and that sentence goes when the commands cover them.

Six of those figures were left stale by the change that admitted
[four word orders](docs/subset.md#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery),
and they are named here so that the next session does not have to find them.
Each counts sentences and each moved with the accepted set, and none has a command:
what the past tense bought, in
[`docs/subset.md`](docs/subset.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku),
whose `praet` row the blocker table has contradicted since negation and the numeral
landed; and five in
[`docs/corpus.md`](docs/corpus.md#agreement-which-matters-more-than-acceptance)
and the section after it — the instrumental dropped from every valency class,
the rest of the valency lexicon, the condition that the substantival pronoun
governs no genitive, the live totals with the dictionary exclusion switched off,
and what the frame settles under live morphology.
The values are in those documents and not repeated here,
because a value copied into this list is stale twice over once somebody retakes it.
Taking them by hand is the work this entry is about not doing twice,
so the general version above is the move, and retaking them meanwhile is the fallback.

Szyk zdania stoi w produkcjach wypisany, a kupuje go rozdzielenie dominacji
od precedencji.
`build` w `olski/subset.py` ma dwadzieścia dziewięć produkcji `ClauseConjunct`,
bo każdy szyk wypisuje się osobno,
a każdy jeszcze raz w tylu wersjach, ile ma miejsc na okolicznik,
i to jest ta część gramatyki, która przy każdej nowej konstrukcji rośnie mnożąc się.
Czternaście z tych dwudziestu dziewięciu dołożyły
[cztery szyki](docs/subset.md#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery),
czyli jedna zmiana podwoiła tę rodzinę,
i jest to najbliższy pomiar tego, co ten wpis wycenia.
Ruchem jest produkcja mówiąca, jakie są córki, wraz z osobnymi warunkami
precedencji, i preprocesor rozwijający jedno w drugie przed parsowaniem.
Krok tańszy od niego stoi w `olski/subset.py` zrobiony do połowy i wart dokończenia:
cztery szyki dopisane wyliczają swoje miejsca na okolicznik pętlą,
czyli jedno po każdej grupie imiennej i jedno na końcu zdania,
a szyki starsze wypisują to samo ciałami.
Ta sama pętla oddaje osiem rodzin ciał z dziewięciu znak w znak,
a dziewiąta jest powodem, dla którego to nie jest refaktor:
ciało `Subject Predicate` okolicznika na końcu nie ma,
bo bierze go `Complements` pod `Predicate`,
więc pętla dopisałaby tam wyprowadzenie drugie tego samego kształtu,
czyli wieloznaczność wziętą z niczego.
Dopóki `Complements` niesie własne miejsca, wyjątek trzeba wypisać,
a wypisany wyjątek jest tym, co ta pętla miała zdjąć.
Miejsce tego ruchu w kolejności trzyma
[kierunek](docs/design-notes.md#kierunek-produkcja-się-rozwarstwia-a-podłoże-zostaje),
jego wycenę [sonda](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą),
a pomiar, od którego się zaczyna, wylicza
[subset.md](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
Drugie miejsce, w którym gramatyka mnoży ciała, dochodzi inną drogą:
`NPConjunct` ma dwanaście ciał, z czego osiem jest iloczynem
czterech kształtów głowy przez obecność `Modifier` po niej,
i mnoży to obecność oraz kolejność rodzajów przydawki,
a nie permutacja argumentów.
Czwarty kształt głowy, czyli przymiotnik z dopełniaczem naraz,
wszedł jako dwa ciała, bo `Modifier` musiał wejść razem z nim,
i tyle samo zażąda każdy następny.
Zdanie względne tego iloczynu nie ruszyło i pokazuje, którędy się go omija:
dochodzi ono do `NP`, czyli o poziom wyżej, więc jest jedną produkcją,
a nie trzecim rodzajem przydawki razy cztery kształty głowy.
Kosztowało to symetrię w koordynacji i osobny wpis wyżej,
a `Adjuncts` w tym samym pliku się nie mnoży,
bo okoliczniki są jednego rodzaju.
Samo zdanie względne dołożyło za to trzecie miejsce, w którym szyk się wypisuje:
`RelativeCore` ma piętnaście ciał, bo rola wysunięta ma trzy kształty,
a reszta zdania szyk i miejsca na okolicznik,
więc preprocesor zastanie tu dwie rodziny symboli zdaniowych zamiast jednej.
Sześć z tych piętnastu dołożyła negacja, i nie dołożyła ich za szyk:
przypadek wysuniętego zaimka zależy od tego, czy czasownik za nim przeczy,
więc każde ciało z dopełnieniem stoi w dwóch wersjach
([`docs/subset.md`](docs/subset.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem)).
Preprocesor precedencji tego nie zdejmie, bo mnoży tu cecha, a nie kolejność,
i jest to najbliższy przykład tego, co ten ruch zostawia po sobie.
Drugim odbiorcą warunków precedencji jest luka, i on już czeka:
[pomiar cechy przeciąganej](docs/design-notes.md#lukę-zmierzono-i-olski-jej-nie-bierze)
pokazał, że luka bez takiego warunku odbiera jednoznaczność każdemu zdaniu względnemu,
a warunek postawiony w ciele produkcji zdejmuje z tego tyle,
ile pozycja w ciele mówi o pozycji w napisie, czyli nie wszystko.
Preprocesor mówiący o napisie zdejmuje jedno i drugie naraz.
Do przeczytania jest, co preprocesor robi z liczbą czytań,
bo permutacja dopisana przez rozwinięcie jest czytaniem tak samo jak każde inne,
a próba nad prozą README stoi w `sonda/` gotowa do porównania,
i liczbę czytań podaje teraz las, bez granicy, jaką miała lista.
Kupuje to jeszcze jedną rzecz, którą sonda pokazała mimochodem:
szyk wykluczony z olskiego przestaje być wykluczony brakiem produkcji.

`sonda/polszczyzna.py` jest drugą deklaracją podzbioru,
który deklaruje `olski/subset.py`,
czyli tym drugim właścicielem faktu, przed którym broni
[`CLAUDE.md`](CLAUDE.md#one-owner-per-fact-repeat-narrative-freely),
i pilnuje jej tylko siedem zdań z `tests/test_sonda.py`.
Te dwie deklaracje rozeszły się na koordynacji przecinkiem
— olski bierze przecinek na trzech poziomach, a sonda spójnik —
i drugi raz na podrzędności, której sonda nie ma wcale,
a nad prozą README nie widać po żadnej liczbie ani jednego z tych rozejść.
Trzecie rozejście widać i jest to grupa liczebnikowa:
`Działają dwie rzeczy` olski wyprowadza jednym czytaniem, a sonda odrzuca,
więc liczba zdań zgodnych spadła i mówi teraz o tym, czego sonda nie ma,
a nie o tym, czym się te dwa opisy różnią
([`docs/design-notes.md`](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)).
Jest to pierwsze rozejście, które ta liczba pokazuje,
i przez to pierwszy dowód, że kopia starzeje się przy każdej produkcji.
Póki liczby z niej cokolwiek trzymają, kopia zarabia na siebie;
przestaje wtedy, gdy szyk zejdzie do warunków precedencji i zostanie zmierzony,
więc wpis stoi za tamtym.
Ruchem jest wtedy `git rm sonda/__main__.py sonda/polszczyzna.py sonda/wiezy.py`
wraz z `tests/test_sonda.py`,
z figurami [tamtej sekcji](docs/design-notes.md#podłoże-więzowe-zmierzone-sondą)
i z wierszem o niej w [sekcji Checks](CLAUDE.md#checks).
Katalog zostaje, bo `sonda/przecinek.py` jest osobną sondą wokół osobnej decyzji,
i zostaje z nim nazwa `sonda` w `SOURCES` z `tests/test_docs.py`.
Zostaje z sekcji to, co figur nie potrzebuje:
że nieciągłość jest warunkiem zdejmowanym, a nie szczeblem,
i że jednoznaczność bywa osiągana bez trafności.
Kasowanie zabiera przy tym jedyny mechanizm w repozytorium,
który wypuszcza konstytuent nieciągły:
`spójne` w `sonda/wiezy.py` jest warunkiem zdejmowanym,
a produkcja z `olski/subset.py` spójności zdjąć nie umie.
Tym warunkiem zmierzono cenę nieciągłości i zamknięto
[rozwidlenie o przestawianiu](docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze),
a liczy ją `sonda/nieciągłość.py`, czyli trzeci plik tego katalogu,
który `sonda/wiezy.py` i `sonda/polszczyzna.py` czyta.
Lista plików wyżej nie obejmuje więc tego, co kasowanie naprawdę zabiera,
a [sekcja Checks](CLAUDE.md#checks) każe tę cenę przeliczać razem z gramatyką.
Ruch dopisuje sobie przez to jedno rozstrzygnięcie:
albo cena nieciągłości przestaje być figurą przeliczaną
i tamta sekcja mówi o niej to, co `docs/firing-rates.md` mówi o sobie,
czyli że jest ceną, przy której decyzja zapadła,
albo podłoże zostaje po to jedno, a kasowanie obejmuje samo porównanie deklaracji.

Liczba pozycji na `Modifier` w `sonda/polszczyzna.py` nie ma wyprowadzenia.
Komentarz przy więzach okolicznika mówi „trzy deklaracje zamiast jedenastu pozycji”,
a jedenastu nie daje żaden sposób liczenia produkcji `build` w `olski/subset.py`,
jakim udało się tę liczbę odtworzyć:
córkę `Adjuncts` albo `Modifier` ma szesnaście produkcji,
samo `Modifier` stoi w siedmiu z nich,
a produkcji `ClauseConjunct` z okolicznikiem jest osiem.
Regułę liczenia rozstrzygnęła po swojej stronie
[`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie),
która liczy produkcje i mówi, które z nich zdejmuje.
Ruchem jest przepisanie komentarza na regułę i liczbę,
przy czym sonda liczy miejsca w zdaniu, a tamten dokument produkcje,
więc albo przejmuje tę regułę, albo mówi, czemu liczy co innego.
Bez reguły żadna zmiana w gramatyce nie umie tej liczby ponieść,
a [sekcja Checks](CLAUDE.md#checks) każe ponieść figury sondy razem z gramatyką.
Zamyka ten wpis także wycofanie sondy,
bo komentarz stoi w pliku, który wtedy znika.

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
przerwać przebieg czy wejść do niemierzonych obok zdań bez morfologii,
i to drugie żąda wiersza w wydruku, którego pierwsze nie żąda.
Sprawdzianem do napisania obok jest las, który kryterium łamie,
bo `tests/test_corpus.py` pisze lasy ręcznie i taki też napisze.

Rola wysuniętego zaimka względnego nie ma etykiety, a bank drzew ją nazywa.
`RelativeCore` w `olski/subset.py` bierze `RelativePronoun` w pozycji podmiotu
i w pozycji dopełnienia, a etykiety `Subject` ani `Object` mu nie daje,
więc czytanie olskiego jest o tę jedną rolę uboższe niż drzewo wzorcowe,
choć wyprowadza zdanie dokładnie tak, jak czyta je bank.
Kosztuje to 22 z 41 zdań w wierszu `lost`
oraz cztery z 31 zdań przyjętych, które się nie zgadzają
([`docs/corpus.md`](docs/corpus.md#złote-czytanie-ocalało-w-437-z-478-zdań-wieloznacznych)),
i te dwie liczby są pierwszym pomiarem tej luki.
Ruchem jest etykieta na zaimku, czyli `Subject` albo `Object` nad `RelativePronoun`
zamiast samego `RelativePronoun` w ciele,
a przed nim rozstrzygnięcie, czy nie psuje to `_pierwsza_rola` w `olski/parse.py`:
zdanie względne jest w `DEKLARACJA` podrzędne, więc streszczenie tam nie zagląda,
ale `Node.find` bez pomijania zagląda i to ono czyta zgodność.
Do przeczytania jest przy tym, co robi z tym `_role` w `olski/skład/rozbiór.py`,
które czyta kształty gramatyki po etykiecie.
Ruch rusza wiersze zgodności w obu kolumnach oraz tabelę ocalenia,
więc jest winien przebiegi, których żąda [sekcja Checks](CLAUDE.md#checks).

Cząstka `się` stoi przy formie osobowej, a należy do bezokolicznika za nią.
`Zebranie ma się odbyć.` jest u olskiego czasownikiem `mieć się`,
bo produkcja `Verb` w `olski/subset.py` skleja cząstkę z formą osobową
i tylko z nią, a polszczyzna kładzie ją tam także wtedy,
gdy zwrotny jest bezokolicznik.
Płaci za to [gramatyka](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego):
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
[Liczba, na której leksykon stoi](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)
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
Ten sam sąd niesie wpis o zaimku wykluczonym ze słownika,
bo oba pytają, co wykluczeniu w `admissible` wolno powiedzieć,
więc rozstrzyga je jedna sesja, a nie dwie.
Zdanie to jest przy tym warunkiem pod
[kierunkiem toru](docs/roadmap.md#kierunek-werdykt-ma-mówić-o-zdaniu-prawdę),
bo czytanie, którego polszczyzna nie ma, jest dokładnie tym,
czego werdykt meldować nie powinien.

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
[`docs/open-questions.md`](docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
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
którą [`docs/open-questions.md`](docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma)
podaje nad korpusem audytowym,
więc zamyka go dopiero sesja, która ten korpus ściągnie i przebieg powtórzy.
Tę samą liczbę rusza wpis o zaimku wykluczonym ze słownika,
bo `admissible` stoi między tekstem a tym pomiarem,
więc przebieg jest jeden i oba wpisy podnosi się razem.

Maskowanie nieciągłości zmierzono nad Składnicą, a nad rejestrem docelowym nie,
i korpus prasowy zaniża tę liczbę względem dokumentacji, zamiast ją zawyżać,
czym różni się od pozostałych liczb tamtej sekcji.
[Sekcja](docs/design-notes.md#nieciągłość-zmierzono-i-olski-jej-nie-bierze)
wywodzi tę klasę z rzeczownika,
który wybiera ten sam przyimek co rama czasownika przed nim —
`dziadek do orzechów`, `maszyna do szycia` —
a dokumentacja techniczna tak właśnie nazywa swoje narzędzia,
więc `narzędzie do podpisu` czy `moduł do fakturowania` są tam budulcem.
Ruchem jest trzecia pozycja dopisana do `olski/wieloznaczność.py`,
który dwie takie liczy nad korpusem audytowym i ma na to całą maszynerię:
rzeczownik, forma osobowa, a za nią przyimek, który ten rzeczownik bierze.
Do przeczytania jest najpierw to, skąd wziąć ostatni warunek,
bo `olski/leksykon.txt` ma ramy czasowników i nic o przyimku przy rzeczowniku,
a `olski/walenty.py` bierze z Walentego tylko je.
Bez tego pozycja liczy się z listy pisanej ręcznie
i jest warta tyle, co ta lista,
czyli mniej niż dwie pozycje, obok których by stanęła.

Nie wiadomo, ile zdań przyjętych opiera się na czytaniu,
którego polszczyzna nie ma.
Nad rejestrem ustaw widać dwa takie z 69 na jednej klasie i jedno na drugiej
([`docs/ustawy.md`](docs/ustawy.md#co-gramatyka-z-tego-wyprowadza)),
a przeczytano je okiem, nie policzono:
`Kalisz.` wyprowadza się jako czasownik, a `Polski Czerwony Krzyż` jako nazwisko
nieodmienne, czyli forma zgodna z każdą liczbą naraz.
Zdanie przyjęte na takim czytaniu jest gorsze niż odrzucone,
bo pokrycie liczy je jak zdanie przeczytane, a
[wykluczenie ze słownika](docs/subset.md#the-dictionary-offers-readings-polish-does-not)
po nie nie sięga: żąda ono, żeby forma miała obok czytanie z klasy zamkniętej.
Do przeczytania jest `admissible` w `olski/subset.py` wraz z tym wykluczeniem
i z [pomiarem jego ceny](docs/corpus.md#what-morphological-ambiguity-costs),
bo to on mówi, co dzisiejsze kryterium zdejmuje i za ile.
Ruchem jest liczba: ile zdań przyjętych każdego korpusu traci czytanie,
gdy zdjąć czytania nieodmienne wszędzie, a nie tylko przy klasie zamkniętej.
Dopóki jej nie ma, nie wiadomo, czy szersze kryterium jest zakupem, czy stratą,
bo [dwa szersze zmierzono i oba brały za dużo](docs/subset.md#dwa-szersze-kryteria-zmierzono-i-żadne-nie-stoi).

Figury `docs/corpus.md` brane nad gramatyką z wyjętą grupą produkcji
bierze każda sesja własnym skryptem, bo żadnego nie ma w repozytorium,
i dobiera do niego wariant, którego dokument nie nazywa.
Przy pozycjach przyłączeniowych granica grupy jest już wypisana
([`docs/subset.md`](docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie)),
a przy [zdaniach, które rama zdejmuje](docs/corpus.md#what-morphological-ambiguity-costs)
nie jest: liczby odtwarza leksykon z biernikiem dopisanym kopuli,
i dokument tego nie mówi.
Wariantów jest przy tym więcej niż dwa i każdy stawia tę samą pułapkę.
Cena podrzędności żąda gramatyki bez `SubordinateClause` i bez `comp` w ramie,
a cena zdania względnego — bez produkcji względnych,
przy czym wariant zbudowany przez podmianę `ZAIMEK_WZGLĘDNY`
zdejmuje oba naraz, bo ta stała stoi i w wykluczeniu, i w terminalu zaimka,
więc sesja mierzy wtedy co innego, niż myśli, i nic jej o tym nie mówi.
Do przeczytania jest ta sekcja wraz z `_klasy` z `olski/subset.py`,
bo ramę zawęża ona i tylko ona.
Ruchem jest sonda obok `sonda/przecinek.py`, która te warianty buduje i drukuje,
wraz ze zdaniem w obu dokumentach mówiącym, że figury bierze się nią.
Sonda zdejmuje z tych figur najdroższą pozycję:
zgadywanie, co poprzednia sesja zmierzyła.

Żadna z dwóch kolumn w
[`docs/corpus.md`](docs/corpus.md#what-morphological-ambiguity-costs)
nie pochodzi od tagera, więc nikt nie policzył, ile z ich różnicy tager odbiera.
Kandydatem jest [Concraft](docs/prior-art.md#polish-language-resources),
a rozstrzyga o nim jedna własność wyjścia:
czy wybrana interpretacja niesie jedną wartość przypadka, czy dysjunkcję.
`subst:sg:nom.acc:m3` jest w `olski/morph.py` jedną interpretacją z cechą mnogą,
więc tager, który ją wybierze i zostawi `nom.acc`, synkretyzmu nie zdejmuje,
a od synkretyzmu własność jednoznaczności się zaczyna
([`docs/subset.md`](docs/subset.md#validity-is-uniqueness-not-just-derivability)).
Ruchem jest przebieg Concrafta nad kilkoma zdaniami i odczytanie tego pola.
Trzecia kolumna dopiero po nim, bo Concraft to binarium Haskella
i model stumegabajtowy, czyli zależność pomiaru z fetchem, jak Składnica i Walenty,
a takiej nie warto zaciągać pod przebieg, który nie ruszy ani jednego zdania.
Po stronie złotej morfologii pytanie wygląda na zamknięte:
`terminal` w `tests/test_corpus.py` pisze `subst:sg:nom:m3` z jedną wartością,
a docstring tego pliku ręczy, że format przepisano z wydania z 2018.
Ręczy jedna osoba i żaden plik banku, więc gdyby Concraft wypadł ciekawie,
sprawdź to na wydaniu, zanim trzecia liczba wejdzie do dokumentu.

## Skład i opowieści

Skład nie ma czym powiedzieć, co jest tematem wewnątrz grupy imiennej,
więc `Jaki` w `olski/skład/składnia.py` zawsze stawia przymiotnik przed rzeczownikiem,
choć polszczyzna ma oba szyki i różnią się one tym, co niosą:
przymiotnik po rzeczowniku nazywa, a przed nim określa.
Widać to bez żadnego pomiaru, na jednej frazie:
README pisze `kontrolowanych języków naturalnych`,
a to samo drzewo wypuszcza `kontrolowany naturalny język`.
Po drugiej stronie stoi to jako czytanie, które z
[obiegu](docs/sklad.md#czytanie-parsera-wraca-drzewem-a-jedno-czytanie-kilkoma)
nie wraca żadnym drzewem, i trzyma to `tests/test_rozbiór.py`.
Do przeczytania jest ta para wraz z tym,
co [`docs/sklad.md`](docs/sklad.md#czwarta-architektura-poziom-dziedziny-a-nie-poziom-języka)
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
Widać to dopiero od [treści](docs/sklad.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi),
bo okoliczność wyrażona zdarzeniem stoi obok zdarzenia nadrzędnego w czasie,
a treść stoi pod nim, i tam czas przestaje być własnością samego opowiadania.
Do przeczytania jest `CZASY` oraz `Kontekst` w `olski/skład/składnia.py`
wraz z tym, co [`docs/sklad.md`](docs/sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie)
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
[pole generowania](docs/similar-work.md#generowanie-rozdziela-się-poziomem-wejścia),
bo ruch ten ma tam nazwę wraz z literaturą,
a warunek, który dziedziczy, jest testem na zbiór dystraktorów,
czyli tym, co tamten algorytm liczy nad opisem rzeczy.
Do przeczytania jest też `pomijalny` w `olski/skład/składnia.py`,
który trzyma warunki [wąskiego opuszczania podmiotu](docs/sklad.md#tekst-wie-to-czego-zdanie-o-sobie-nie-wie),
bo zaimek dziedziczy stamtąd warunek, a nie tylko mechanizm,
wraz z [ceną tego ruchu](docs/sklad.md#lepszy-tekst-żąda-czego-innego-niż-dłuższy),
która trzyma cztery rzeczy czyniące go innym, niż wygląda:
ostrzejszy warunek na zaimek, szyk łączący go w jedną zmianę z
[dopełnieniem wyrażonym zdarzeniem](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
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

`Zdanie.podmioty` w `olski/skład/składnia.py` schodzi pod konstytuent na dwa poziomy,
czyli tam, gdzie sięga `_wskazany`, a zdanie podrzędne stoi czasem głębiej:
`Mysz goniła ogon myszy, która spała.` ma dwa podmioty, a widać stąd jeden.
Kosztuje to opuszczenie postawione tam, gdzie czytelnik trafia na dwie rzeczy
wyciągające z czasownika jedną formę, czyli dokładnie to, przed czym ten warunek broni.
Do przeczytania jest `_zdania_pod` wraz z `_wskazany` w tym samym pliku,
bo schodzą tak samo głęboko i tylko jednej z nich to wystarcza:
tamta pyta, skąd zaimek wyjdzie na czoło, a ta, na kogo czytelnik trafi.
Ruchem jest zejście po całym drzewie roli zamiast po dwóch jego poziomach,
i jest ono tańsze niż tamto, bo nie ma z niego nic do wyprowadzenia.

Rama czasownika, o którą pyta `Robi` w `olski/skład/składnia.py`,
odpowiada na trzy pytania z listy: o biernik, o bezokolicznik i o zdanie podrzędne,
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
Czwarta wersja legendy obeszła to zdanie z drugiej strony,
bo `nie wierzyła, że w piwnicy mieszkał bazyliszek` bierze
[treść](docs/sklad.md#treść-jest-zdarzeniem-o-którym-ktoś-coś-sądzi)
zamiast wyrażenia przyimkowego, a mówi to samo o postaci;
klasa zostaje jednak w tej samej cenie, bo wiara w rzecz zdaniem podrzędnym nie wyjdzie.
Czwarty koszt jest cichy i przez to najgorszy z nich:
`chcieć` ma u Walentego i dopełniacz, i przypadek strukturalny,
więc przechodzi tu przez pytanie o biernik i wypuszcza `Kot chce mysz.`,
czyli zdanie, którego polszczyzna woli nie mówić, a nikt tego nie zgłasza.
Jedna pozycja znaczy tu więc nie tylko odmowę tam, gdzie brakuje przypadka,
ale i wybór najgorszej z ram, które lemat ma.
Piątą klasę dokłada losowanie: `czekał na izbach` wychodzi z drzewa,
w którym `na izbach` jest okolicznością miejsca,
a czyta się przez `czekać na kogoś`, czyli przez ramę, której tu nie ma,
więc `olski/skład/makieta.py` ten czasownik pomija, zamiast wypuszczać takie zdania.
Do przeczytania jest `olski/walenty.py` wraz z tym,
co [`docs/subset.md`](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego)
mówi o tym, co ten przekład z Walentego bierze, a czego nie,
bo Walenty niesie wszystkie te ramy i jest to jedna zmiana po obu stronach.
Zdanie podrzędne dopisane po bezokoliczniku przesądziło ten wpis,
bo pokazało, ile z tej zmiany jest zrobione, a ile nie:
przekład umie wziąć trzecie zdanie, plik umie je unieść, a `Robi` umie o nie zapytać,
i mimo to każde nowe pytanie jest osobną gałęzią w konstruktorze,
a `_dopełnienie` obok rozdziela dziś trzy kształty tam, gdzie rozdzielało dwa.
Ruchem jest rama jako zbiór pozycji, a nie lista pytań,
oraz `zdarzenie` w tym samym pliku rozdzielające argumenty po tym zbiorze,
a nie po kategorii okoliczności.

Treść bierze jeden spójnik i przez to jedną z dwóch rzeczy, które ta pozycja mówi.
`że` orzeka, że tak jest, a `żeby` — że tak ma być,
więc `Czeladnik chciał, żeby córka krawca wróciła.` z tego drzewa nie wyjdzie,
choć jest to zdanie, którym polszczyzna mówi o cudzym zdarzeniu pod czyjąś wolą.
Stoi to obok odmowy, którą `Robi` wydaje bezokolicznikowi o cudzym wykonawcy,
i te dwie rzeczy są jedną dziurą widzianą z dwóch stron:
[`docs/sklad.md`](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie)
nazywa tamto zdanie polskim, którego bezokolicznik nie wyraża,
a wyraża je dokładnie ta pozycja i ten drugi spójnik.
Do przeczytania jest `cp(żeby)` obok `cp(że)` u Walentego,
bo słownik te dwa kształty rozdziela i mówi, który lemat bierze który,
oraz `Treść` w `olski/skład/składnia.py`, gdzie spójnik stoi stałą.
Ruchem jest kategoria dziedziny na to, czy treść jest orzekana, czy żądana,
wraz z czwartym zdaniem leksykonu; wpis jest przez to winien
przebieg `olski/walenty.py` oraz poprawkę liczb w
[`docs/subset.md`](docs/subset.md#leksykon-mówi-trzy-zdania-na-lemat-i-bierze-je-z-walentego).

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

`Jest` w `olski/skład/składnia.py` umie jedną kopulę, a gramatyka bierze pięć.
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
[`docs/sklad.md`](docs/sklad.md#nazwę-leksemu-wybiera-autor-bo-lemat-go-nie-wskazuje)
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

`rodzaj_rzeczownika` w `olski/skład/morfologia.py` zgłasza `BrakFormy` nad rzeczownikiem,
który liczby pojedynczej nie ma, bo szuka rodzaju w mianowniku pojedynczym.
Kosztuje to podmiot: `drzwi` i `Włochy` nie staną w zdaniu, z którego wyjdzie czasownik,
i nie staną w koordynacji, która rodzaju od członów żąda,
choć jako dopełnienie wychodzą, i tak stoją w `opowieści/bazyliszek.py`.
Do przeczytania jest to, co `paradygmat` w tym samym pliku dostaje z SGJP
dla takiego leksemu: rodzaj stoi tam przy formach liczby mnogiej,
więc rzecz jest w miejscu, w którym się go szuka, a nie w danych.
Ruchem jest rodzaj brany z mianownika tej liczby, którą ten leksem ma,
wraz z testem na obie liczby, bo inaczej poprawka pokryje jedną z nich.

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
wraz z `olski/leksykon.txt` i `olski/skład/leksemy.py`, czyli dwoma leksykonami,
które już stoją, a żaden z nich na to pytanie nie odpowiada.
Ruchem jest rozstrzygnięcie, czy wpis wypisuje formy,
czy wskazuje leksem, wedle którego się odmienia,
a po nim plik z wpisami na te słowa, których to repozytorium używa o sobie.
Drugą z tych dróg widać już na `olski/skład/leksemy.py`, ale tylko połowę:
wpis wskazuje tam leksem, który słownik ma,
a tutaj trzeba wskazać leksem, wedle którego odmienia się słowo,
którego słownik nie ma wcale.

`olski/skład/rozbiór.py` nie wypuszcza dopełnienia wyrażonego zdarzeniem,
więc `Linter pomaga pisać dobry kod.` nie wraca żadnym drzewem,
choć zdanie to mają oba tory naraz.
Bierze się to z kolejności, w której rozbiór składa kandydatów:
konstytuenty powstają, zanim wiadomo, co jest podmiotem,
a bezokolicznik żąda tego samego obiektu, którym stoi podmiot nad nim,
bo tyle sprawdza `Robi` w `olski/skład/składnia.py`.
Do przeczytania jest `_złóż` wraz z `_ciąg` w tym samym pliku,
bo drugie z nich przekazuje już podmiot w dół, czego pierwsze potrzebuje,
oraz [dopełnienie wyrażone zdarzeniem](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
które trzyma warunek o cudzym wykonawcy.
Ruchem jest zbudowanie zdania pod bezokolicznikiem po podmiocie, a nie przed nim.

Przeczenie ma kategorię po obu stronach, a rozbiór jej nie odczytuje.
`Robi` oraz `Jest` w `olski/skład/składnia.py` mają pole `przeczenie`,
gramatyka wypuszcza cząstkę w ciele `Verb` przed formą czasownika,
a `_konstytuenty` w `olski/skład/rozbiór.py` bierze z tej pozycji samo `children[0]`,
czyli trafia na `nie` i nie znajduje pod nim żadnego lematu czasownika.
`Nie wyniósł z piwnicy lustra.` wraca stąd powodem
`„Nie wyniósł” nie ma tu czym być w pozycji Verb`,
choć jest to zdanie, które oba tory mają naraz.
Kategorii tu nie brakuje, brakuje odczytania kształtu, który ją niesie,
i tym różni się ten wpis od sąsiednich.
Do przeczytania jest `_konstytuenty` wraz z produkcją `Verb`
w `olski/subset.py` oraz `nie` w `olski/skład/składnia.py`, czyli druga strona tej kategorii.
Ruchem jest pozycja czasownika czytana całym ciałem,
tak jak `_role` czyta ciało grupy imiennej,
wraz z przeczeniem podanym do `_złóż`.

Liczebnik ma produkcję w gramatyce, a w tym zapisie nie ma kategorii,
więc `Działają dwie rzeczy.` wraca powodem
`„dwie rzeczy” nie ma tu czym być w pozycji Subject`,
i tą samą drogą przepada każde zdanie z liczbą.
Do przeczytania jest `_nominalne` w `olski/skład/rozbiór.py`,
czyli lista ciał grupy imiennej, które ten kierunek mówi,
wraz z [ceną liczebnika](docs/subset.md#liczebnik-zmierzono-i-nie-odbiera-ani-jednego-zdania),
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
[`docs/sklad.md`](docs/sklad.md#tekst-losowany-żąda-tego-czego-autor-nie-musiał-napisać)
wylicza jako fakty poza leksykonami tego pakietu,
oraz `PRZYIMKI` w `olski/skład/przyimki.py`, bo pytanie jest o kolumnę, której ten plik nie ma.
Ruchem jest ta kolumna, czyli przyimek dopisany przy rzeczowniku, a nie przy relacji,
wraz z rozstrzygnięciem, czy milczenie takiego leksykonu odmawia, jak przy przyimkach,
czy przepuszcza, jak przy ramie domyślnej czasownika;
świadka w słowniku ta wiedza nie ma, bo SGJP kolokacji nie znakuje.

Aspekt bezokolicznika nie jest sprawdzany, a czasownik nad nim go wybiera:
`zacząć` żąda niedokonanego, więc `Czeladnik zaczął zapłakać.`
przechodzi przez pytanie o ramę, które stawia `Robi` w `olski/skład/składnia.py`,
i wychodzi zdaniem, którego polszczyzna nie ma.
Rama jest tu sprawdzona co do pozycji i niesprawdzona co do formy,
która tę pozycję wypełnia, i jest to ta sama luka, którą ma
[dopełnienie wyrażone zdarzeniem](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie),
tylko o piętro niżej: tam leksykon mówi, czy bezokolicznik wolno postawić,
a tutaj nie mówi, który.
Kosztuje to dziś czasownik w tabeli `olski/skład/makieta.py`,
która `zacząć` i `przestać` pomija, żeby losowanie takiego zdania nie wypuściło.
Do przeczytania jest to, co `olski/walenty.py` bierze z Walentego,
bo słownik ten aspekt przy pozycji `infp` wypisuje,
oraz `bierze_bezokolicznik` w `olski/walencja.py`, czyli zdanie, które to pytanie zadaje.
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
[`docs/sklad.md`](docs/sklad.md#dopełnienie-nie-pyta-czy-stoi-pod-nim-rzecz-czy-zdarzenie)
mówi o tym, że podmiot w takim zdaniu nie staje nigdy,
oraz [postawa przeglądu](docs/sklad.md#drzewo-jest-jednoznaczne-a-napis-z-niego-nie-musi-być),
która o tym pomiarze mówi, że liczy się go z form, które w tekście stanęły.
Zażąda to od `_rozróżnia` czasownika z innego zdania niż uczestnik,
bo trzeci warunek pyta o formę, którą rola z czasownika wyciąga,
a bezokolicznik nie wydaje żadnej i obu rolom oddałby tę samą;
formą, która te dwie rozdziela, jest `chciał` ze zdania nadrzędnego.
Dzisiaj obie strony tego porównania biorą się z jednego zdania i tylko stamtąd.

`Jest` w `olski/skład/składnia.py` nie ma pozycji na okoliczność,
choć `Robi` obok ma ich tyle, ile autor postawi,
więc `Kot jest zwierzęciem w piwnicy.` nie wyjdzie ze składu,
a olski to zdanie czyta i czyta je dwojako.
Kosztuje to każde zdanie, które o czymś orzeka i mówi, gdzie albo kiedy,
czyli klasę, której README nie żąda, a opowieść żądałaby jej w pierwszym akapicie.
Do przeczytania jest `linearyzuj` w obu tych klasach,
bo różnią się one o tę jedną pętlę, i
[okoliczność](docs/sklad.md#okoliczność-nie-pyta-czy-stoi-pod-nią-rzecz-czy-zdarzenie),
która trzyma wywód o tym, że okoliczność dochodzi do zdarzenia.
Ruchem jest to samo pole na obu, wraz z rozstrzygnięciem,
czy okoliczność przy orzeczeniu imiennym mówi o byciu czymś,
czy o rzeczy, która czymś jest, bo `w piwnicy` przy `Kot jest zwierzęciem.`
czyta się i tak, i tak, a drzewo ma powiedzieć jedno.

## Pakiet, instalacja i testy

The repository ships no licence.
`pyproject.toml` carries no `license` field and there is no `LICENSE` file,
so the terms under which any of this may be used are unstated.
The move is to pick one, add the file,
and set `license` in `pyproject.toml` to match.
Reading a GPL v3 parser of Polish is what raised it
(see [`docs/swigra.md`](docs/swigra.md#why-wrapping-it-does-not-get-there)),
and the answer decides whether olski could ever link against such a thing.

Granica harnessu jest napisana raz, a stosuje się dwa razy inaczej.
`harness/__init__.py` mówi, że korpus w formacie znacznikowym
dochodzi do gramatyki tędy, a nie przez `olski`,
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
(`include = ["olski*"]` w `pyproject.toml`),
a jeden ma własną komendę,
gdzie tak samo pomiarowe programy w `harness/`
nie mają ani instalacji, ani komendy.
Ruchem jest rozstrzygnięcie granicy, a nie przeniesienie plików:
albo obie idą do `harness/`, a `olski-corpus` staje się
`python3 -m harness.coverage` jak dwie pozostałe komendy pomiarowe,
co przepisuje polecenia w [`docs/corpus.md`](docs/corpus.md#fetching-it)
i w [sekcji Checks](CLAUDE.md#checks),
albo `harness/__init__.py` mówi, czym granica jest,
co nie kosztuje nic i przestaje odpowiadać dwa razy.
Do przeczytania jest to, co pakiet ma dawać temu, kto go instaluje:
czytnik banku drzew i trzy programy pomiarowe są w nim,
a kto sprawdza zdanie gramatyką, żadnego z nich nie woła.

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
