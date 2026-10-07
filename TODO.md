# TODO

Otwarta robota w repozytorium.
Wpis kasuje commit, który go zamyka.
Plan kierunku jest w `docs/kierunek.md`, a nie tutaj.

## Narzędzia do mierzenia prozy repozytorium

`--chwyty` wypisuje wzorce z katalogu, który stał w dawnym `CLAUDE.md` (`olski/chwyty.py`),
a polecenie `olski-pokrycie` (`olski/pokrycie.py`) liczy kolejkę blokerów nad własnym tekstem.
Oba służyły mierzeniu prozy tego repozytorium.
Rozstrzygnąć, czy zostają, czy wypadają razem z testami.
`--żądania` i `--osoby` zostają, bo są zalążkiem przebiegu semantycznego
(`docs/kierunek.md`).

## Testy kolejności czytań

Razem z sondami odeszły `tests/parser/test_kolejność.py`, `tests/parser/test_cena.py`
i `tests/werdykt/test_czytania.py`, bo stały na skasowanych modułach `harness`.
Część z nich pilnowała kolejności czytań i cennika (`olski/cennik.py`).
Jeśli werdykt ma dalej obiecywać kolejność czytań,
napisać na nowo te z nich, które pytają o samo `olski` (`git show d79da51:<ścieżka>`).

## Licencja zdań w `próba/`

`próba/usterki.txt` i `próba/przeczytane.txt` niosą zdania z NKJP i z Microsoft Learn,
a `REUSE.toml` obejmuje je wpisem domyślnym, czyli MIT.
Dać im wpisy z warunkami źródeł, tak jak mają `próba/nkjp-*.txt` i `próba/wybory*.txt`.
