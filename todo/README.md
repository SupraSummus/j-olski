# Work to do in the repository

The running list of work inside the repository itself:
rewrites, merges, documents that have drifted apart,
dangling references, gaps, and code worth improving.
Something noticed while working on another topic goes here
instead of stretching the current change or being forgotten.
[The review pass](../CLAUDE.md#przegląd-sprawdza-zmianę-wobec-całego-tego-pliku) is the other way in:
a refactor too large to do on the spot is written down rather than started,
and the review also checks whether a change deleted the entries it closes.
Read the file your work touches before starting,
because it names the problems somebody has already found there.
The list as a whole is longer than anybody reads,
which is what the files below are for.

Lista nie przypisuje wpisów do torów i nikt nie podnosi ich po kolei,
bo wpis notuje tylko to, na co ktoś trafił przy innej robocie.
[docs/roadmap.md](../docs/roadmap.md#co-jest-budowane) mówi, co jest budowane.

An entry belongs here only if a commit in this repository closes it.
A question the outside world answers is not work in the repository,
and the document that owns the topic keeps it:
[`docs/open-questions.md`](../docs/open-questions.md)
or a document's own `Not yet decided`.
The next move is the tell:
waiting for somebody else's answer is an entry there,
a file to write is an entry here.

A register, not a changelog:
an entry that closes is deleted by the same commit that settles it,
which is the done-marker rule from
[`CLAUDE.md`](../CLAUDE.md#documents-describe-the-present-git-owns-the-past)
applied to this list.

One paragraph per entry, paragraphs separated by a blank line,
lines inside them broken [semantically](../CLAUDE.md#semantic-line-breaks),
and no bullets or numbering,
so that adding or removing an entry gives a clean diff
and leaves its neighbours alone.
Numbering renumbers everything below an entry landing in the middle,
and a bullet indents prose that is meant to read as prose.

Podział na pliki zachowuje ten czysty diff,
więc każdy wpis należy do jednego pliku.
Nazwa pliku mówi, czego wpis dotyka, a nie co jest budowane:
osią jest warstwa, o którą wpis pyta,
czyli ta sama, po której dzieli się [kod](../CLAUDE.md#code).
Wpis sięgający dwóch plików dopisz do tego,
który obejmuje dowód do przeczytania,
bo od dowodu zaczyna ten, kto wpis podnosi.
Plik bez wpisów skasuj razem z jego ostatnim wpisem,
a wiersz indeksu zabierz razem z plikiem;
nowy załóż dopiero wtedy, gdy masz do niego wpis.

An entry that names another one names it by what it is about.
A file name does not identify one, since a file holds many,
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
[splitting work across sessions](../CLAUDE.md#splitting-work-across-sessions).

Wpis nie jest rozstrzygnięciem, bo autor pisał go przy innej robocie
i dał mu tyle uwagi, ile zostało.
Pewne jest w nim jedno: autor na coś trafił.
Kto wpis podnosi, dochodzi więc do ruchu sam
i traktuje nazwany ruch jako propozycję, a nie jako polecenie.
Czasem wychodzi mu ruch inny, a czasem żaden,
bo problemu nie ma albo naprawa kosztuje więcej, niż jest warta;
wtedy całą zmianą jest skasowanie wpisu, z powodem w komunikacie commita.

## Który plik czytać

- [dokumenty.md](dokumenty.md) — proza repozytorium:
  konwencje, wskazania między dokumentem a kodem, nazwy rejestru.
- [komendy.md](komendy.md) — wiersz poleceń, wydruki
  i sondy, których repozytorium nie ma.
- [korpusy.md](korpusy.md) — pobranie korpusu i ekstrakcja nad nim.
- [gramatyka.md](gramatyka.md) — co gramatyka bierze,
  a czego nie bierze: produkcje, symbole, listy lematów.
- [leksykon.md](leksykon.md) — leksykon walencyjny
  i to, czego przekład z Walentego nie przenosi.
- [parser.md](parser.md) — las, koszt i zatrzymanie.
- [werdykt.md](werdykt.md) — co werdykt nazywa,
  a czego o przyjętym czytaniu nie wypisuje.
- [rozstrzyganie.md](rozstrzyganie.md) — warstwa nad werdyktem
  i świadkowie, którymi odpowiada.
- [pomiar.md](pomiar.md) — pomiar pokrycia nad korpusem
  i sondy różnicowe.
- [konstrukcje.md](konstrukcje.md) — konstrukcje polszczyzny,
  których gramatyka nie wyprowadza.
- [skład.md](skład.md) — realizacja powierzchniowa i opowieści.
- [pakiet.md](pakiet.md) — paczka, licencja i przebieg checków.
