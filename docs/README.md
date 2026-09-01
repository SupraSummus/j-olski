# Dokumenty

W tym katalogu są notatki projektowe, przegląd pola, plan i otwarte pytania.
Ramę — czym olski jest, co działa i dokąd to idzie — daje
[README](../README.md), a każdy dokument z tego spisu rozwija jej kawałek.
Spisu nie czyta się od góry: czytelnik przebiega go do swojego dokumentu.
Dzielimy go po torach, bo czytelnik przychodzi po jeden tor.
Kto po który dokument sięga, mówi [roles.md](roles.md).

Dokument dostaje tu zdanie albo dwa i nie powtarza swoich liczb,
bo właścicielem faktu jest ten dokument, a nie spis
([CLAUDE.md](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely)).
Dokument, którego tu nie ma, nie leży na niczyjej drodze,
więc `tests/test_docs.py` żąda wiersza dla każdego pliku tego katalogu.

## Tor gramatyczny

- [subset.md](subset.md) mówi, kiedy zdanie jest olskie i czym jest znalezisko,
  co gramatyka wpuszcza i ile kosztuje przyłączanie wyrażeń przyimkowych.
- [konstrukcje-gramatyczne/](konstrukcje-gramatyczne/README.md)
  wycenia każdą wpuszczoną konstrukcję osobno.
  Czytelnik przebiega ten rejestr do swojego wpisu.
- [warstwa-leksykalna.md](warstwa-leksykalna.md) mówi,
  co olski bierze za słowo i czego czasownik żąda od swojego leksykonu.
- [design-notes.md](design-notes.md) mówi,
  co czyni polszczyznę trudną do parsowania.
  Pokazuje drabinę kosztów i urwisko nieciągłości.
- [parsowanie.md](parsowanie.md) mówi, co jest między gramatyką a werdyktem.
  Wybiera parser i nazywa to, co pakuje się pod jedną pozycję lasu.
- [disambiguation.md](disambiguation.md) nazywa to,
  co warstwa za parserem musi rozstrzygnąć.
  Wycenia trzy pytania, na które ujednoznacznianie się rozpada, i odrzuca ranking.
- [rozstrzyganie.md](rozstrzyganie.md) opisuje warstwę rozstrzygającą za parserem.
  Świadek wskazuje gospodarza obok werdyktu, a dokument liczy jego pomyłki.
- [corpus.md](corpus.md) mierzy gramatykę na Składnicy.
  Mówi, co daje pierwszy pomiar i czego nie dowodzi liczba pokrycia.
  Składnica jest tam bankiem drzew.
- [ustawy.md](ustawy.md) mówi,
  czego żądają od zdania w ustawie „Zasady techniki prawodawczej”.
- [pisanie-po-olsku.md](pisanie-po-olsku.md)
  zbiera feedback z fotela użytkownika.
  Autor płaci za jedno odrzucone zdanie, a gramatyka za drugie.
- [extraction.md](extraction.md)
  prowadzi korpus w Markdownie do gramatyki
  i mówi, co ten krok po drodze zmyśla.
- [corpora.md](corpora.md) przegląda polszczyznę pisaną przez ludzi
  i mówi, co każdy kandydat na korpus niesie w swoim rejestrze.
- [audit-corpus.md](audit-corpus.md) nazywa repozytoria,
  z których zrobiony jest korpus audytowy.
  Podaje commity, na których stoją liczby.
- [prior-art.md](prior-art.md)
  wylicza Morfeusza, Świgrę i resztę pola.
- [swigra.md](swigra.md) nazywa teren,
  który zajmuje najbliższy parser polszczyzny.
  Warto wziąć z tych źródeł kilka mechanizmów.
  Sonda mierzy przy tym czas rozbioru.
- [glr-in-practice.md](glr-in-practice.md) jest raportem z terenu
  o systemie, który puszcza swój parser nad prawdziwą polszczyzną.
- [witryna.md](witryna.md) mówi, co witryna pokazuje w przeglądarce.
  Boczny tor nie rusza rdzenia.
  Dokument nazywa cenę tego układu.

## Tor składu

- [sklad.md](sklad.md) mówi, co tekst wie ponad zdaniem
  i czego brakuje w leksykonie.

## Oba tory

- [roles.md](roles.md) nazywa role,
  w których ktoś to repozytorium czyta.
  Wszystkie te role obsadza jedna osoba.
- [architecture.md](architecture.md) wylicza warstwy,
  przez które zdanie przechodzi w obu kierunkach.
  Oba tory mają dwie warstwy wspólne.
- [roadmap.md](roadmap.md) wylicza cele oraz etapy dwóch torów.
  Jeden tor ma kierunek, a drugi ma kryterium wyjścia.
- [open-questions.md](open-questions.md) wylicza rozwidlenia,
  na których nie zapadła decyzja.
- [similar-work.md](similar-work.md) mówi,
  które obietnice stu kontrolowanych języków naturalnych ktoś naprawdę zmierzył.

## Linter

Linter jest wykrywaczem wzorców prozy
i jednym z [celów](roadmap.md#cele).

- [linter.md](linter.md) wylicza cztery osie reguły
  i mówi, co zamknęło wycofany pakiet reguł.
- [firing-rates.md](firing-rates.md) mówi,
  co pakiet typograficzny robił nad polszczyzną, którą ktoś napisał.
  Nazywa cenę, za którą pakiet został wycofany.
- [prose-linters.md](prose-linters.md) nazywa silniki,
  które angielski i japoński już mają.
  Jeden z nich zmierzył własną częstość fałszywych trafień.
- [fiction.md](fiction.md) mówi,
  co psuje się w prozie literackiej z modelu i co z niej da się lintować.
- [generated-polish.md](generated-polish.md)
  mierzy prawdziwy zbiór polszczyzny z modelu.
