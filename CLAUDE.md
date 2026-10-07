# Notatki dla agentów AI

## Kierunek

Olski jest kompilatorem polszczyzny:
front-end (Morfeusz i gramatyka), reprezentacja pośrednia,
przebieg semantyczny na tej reprezentacji i back-end (skład).
Zasady, otwarte decyzje i następny krok opisuje `docs/kierunek.md`.
Kierunek ustala właściciel projektu.
Kiedy pomiar mówi, że kierunek nie działa, powiedz to wprost,
zamiast przeformułowywać cel albo dopisywać reguły.

## Stan sprzed resetu

Commit `d79da51` ma pełną prozę poprzedniego kierunku:
`docs/`, rejestr `todo/` i dawny `CLAUDE.md`.
Komentarze w kodzie i w plikach konfiguracji odsyłają do tamtych dokumentów.
Czytaj je gitem (`git show d79da51:docs/subset.md`), jako uzasadnienie kodu, a nie jako obowiązujące reguły.
Komentarz, który ruszasz z innego powodu, wolno skrócić albo usunąć.

## Checki

```sh
pip install -e '.[dev]'
python3 -m pytest
ruff check .
reuse lint
npx --yes markdownlint-cli@0.45.0 '**/*.md'
```

To samo uruchamia `.github/workflows/checks.yml` na pull requeście.
Drugi workflow buduje stronę dokumentacji:

```sh
pip install -e '.[dokumentacja]'
python3 -m dokumentacja
```

Budowanie idzie z `--strict`, więc martwy link w README albo w `docs/` je wywraca.

## Kod

- Nazwy w kodzie są po polsku, z diakrytykami, tak jak w istniejącym kodzie.
- Komentarz piszemy wtedy, gdy mówi coś, czego kod nie pokazuje.
- Testy: zwykłe funkcje `test_*`, gołe `assert`, `pytest.mark.parametrize` zamiast pętli.
- Wydruk nie bierze kolejności ze zbioru, bo hash napisów zmienia się między przebiegami.
- Blok wydruku `olski.check` wklejony do README sprawdza `tests/dokumenty/test_wydruki.py`.

## Ewaluacja

- Liczy się wynik na cudzym tekście, nie na prozie repozytorium.
- `próba/` trzyma ocenione zdania z NKJP i z dokumentacji technicznej.
  Oceny pisały głównie sesje agenta, więc wynik, na którym opiera się decyzja,
  potwierdza człowiek na próbce.
- Liczbę z pomiaru zapisuj razem z poleceniem i commitem, na którym wyszła.
- `parse` wylicza najwyżej 64 czytania; pomiar bierze wszystkie z `las(...).czytania()`.

## Proza

- Po polsku i prosto, dla kogoś, kto ma na tym tekście działać.
- Wiersz łamiemy po zdaniu albo po zdaniu składowym ([sembr](https://sembr.org)).
- Otwarta robota idzie do `TODO.md`; wpis kasuje commit, który go zamyka.
- Dokument opisuje stan obecny; historię trzyma git.

## Commity i sesje

- Temat commita po polsku, w trybie rozkazującym, do 72 znaków.
- Sesja dostaje cel (na przykład demo albo pomiar), a nie pojedynczy commit.
- Przed wnioskami o historii gita: `git fetch --all` i `git fetch origin --unshallow`.
