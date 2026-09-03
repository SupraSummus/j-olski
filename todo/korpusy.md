# Korpusy, ekstrakcja i figury

Only one of the corpora in
[`docs/corpora.md`](../docs/corpora.md#how-the-counts-here-were-taken)
is counted by a program this repository holds.
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
[`docs/firing-rates.md`](../docs/firing-rates.md#wolne-lektury)
already fetches the same library by naming every slug it takes,
so that half is a rewrite of one paragraph rather than a program.
The move is to decide, per corpus, whether it joins the harness
as an extraction beside the Markdown one,
as a fetch-and-select command in the document that cites it,
or not at all because the survey has already ruled the corpus out.

The corpus archives these documents send a reader to fetch
are pinned by URL and by nothing else.
[Składnica](../docs/corpus.md#fetching-it)
and [NKJP](../docs/corpora.md#the-national-corpus-of-polish)
name a release in the query string of a wiki attachment,
which says which release without saying which bytes.
`harness/świgra.py` is the one fetch that carries a digest,
and it needed one worst: `swigra_current.zip` names no release at all.
[The audit corpus](../docs/audit-corpus.md#the-list) pins its members to a commit
and says what a pin is for:
so that a second person fetches the same bytes.
The corpus archives make that promise
and give a reader no way to hold anyone to it.
The move is `sha256sum` over Składnica and over NKJP,
with the digest beside the command that fetches it,
the way `harness/świgra.py` carries one,
which turns a substitution upstream into a failed check
rather than a figure that quietly stops reproducing.

The corpora these documents send a reader to fetch
come from hosts that gain nothing by serving them,
once per session rather than once per person,
because a Claude Code session on the web starts from an empty container.
[The Wolne Lektury run](../docs/firing-rates.md#wolne-lektury)
takes 326 files at one request each from a volunteer library,
[Składnica](../docs/corpus.md#fetching-it) is 92 MB
that [recomputation](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje) makes a condition of touching the grammar,
and [NKJP](../docs/corpora.md#the-national-corpus-of-polish)
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
[`CLAUDE.md`](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely) warns about.

Leksykon projektu rusza liczby brane nad prozą README, bo tam zmierzono, że rusza,
a czy rusza je nad korpusem audytowym i nad rejestrem ustaw, nie sprawdził nikt,
choć oba korpusy czytają tekst tą samą drogą.
Rozstrzyga o tym jedna rzecz: czy ta proza pisze którąkolwiek formę tego leksykonu,
bo wiersz nazywa formę, której słownik nie czyta,
więc nad korpusem, który tej formy nie pisze, nie rusza on ani jednej liczby.
Ruchem jest więc grep form tego leksykonu po `proza/`,
a po nim albo przeliczenie liczb obu tych korpusów, albo zdanie mówiące,
czemu ten leksykon nad tą prozą nie rusza nic; formy wypisuje `odmiana` w
`olski/projekt.py`.

Ekstrakcja ustaw robi zdanie z pozycji wyliczenia, która jest samą nazwą,
a takie zdanie przyjmuje się na czytaniu czasownikowym:
`Kalisz.`, `Przemyśl.` i `Nowy Sącz.` są pozycjami wyliczenia okręgów wyborczych
i zajmują cztery ze 144 zdań przyjętych tego rejestru, a zdaniem żadne z nich nie jest
([`docs/warstwa-leksykalna.md`](../docs/warstwa-leksykalna.md#kilka-procent-zdań-przyjętych-opiera-się-na-czytaniu-którego-polszczyzna-nie-ma)).
Kropkę dopisuje `zdania` w `harness/ustawy.py` rozmyślnie i mówi to jej docstring:
bez niej werdyktem nad każdą pozycją każdego wyliczenia byłoby „to nie zdanie”.
Cena tej kropki jest przez to policzona po jednej stronie, a po drugiej nie:
ile pozycji wyliczenia jest zdaniem, którego czytelnik nie odrzuci, nie liczy nikt.
Ruchem jest ta druga liczba, a po niej wybór:
albo pozycja bez formy czasownikowej wychodzi bez kropki i wpada w `fragment`,
albo kropka zostaje, a cena zapisuje się przy niej.
Wykluczenie ze słownika tej klasy nie zabierze przy żadnym z dwóch wyjść,
bo czytanie czasownikowe nie jest nieodmienne
i `admissible` w `olski/segmentacja.py` po nie nie sięga.
Do przeczytania jest
[`docs/extraction.md`](../docs/extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem),
bo druga ekstrakcja odpowiada na to samo pytanie odwrotnie
i werdykt `fragment` jest tam odpowiedzią wybraną.

Ekstrakcja oddaje zdania pojedynczo, a jednostką sprawdzaną jest tekst
([`docs/roadmap.md`](../docs/roadmap.md#podzbiór-jest-umową-a-nie-zasięgiem)),
więc kolejność zdań i to, co je rozdziela, zaczyna ważyć na werdykcie.
Nagłówek, pozycja listy i wiersz tabeli wychodzą stąd jako akapity,
których nic nie punktuje, i przebieg liczy je osobno
([`docs/extraction.md`](../docs/extraction.md#nie-każdy-akapit-który-stąd-wychodzi-jest-zdaniem)),
a rachunek nad tekstem potrzebuje o każdym z nich jednej rzeczy:
czy niesie grupę imienną, do której wolno odesłać, czy odesłanie przerywa.
Nagłówek niesie ją zwykle, a wiersz tabeli sąsiaduje z wierszem,
którego autor nie czytał po kolei.
Ruchem jest granica akapitu przenoszona przez ekstrakcję razem z jego rodzajem,
zamiast samego ciągu zdań,
oraz decyzja, które rodzaje rachunek nad tekstem przeskakuje.
Do przeczytania jest, ile takich pozycji ma proza tego repozytorium
i ile z nich rozdziela dwa zdania mówiące o sobie,
bo dopiero ta druga liczba mówi, czy rzecz w ogóle boli.
