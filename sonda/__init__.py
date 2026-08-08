"""Sonda: kod pisany po to, żeby rozstrzygnąć decyzję, a nie po to, żeby stać.

Pakiet trzyma jedną sondę: czy podzbiór, który dzisiaj stoi na gramatyce
bezkontekstowej, powiedziałby to samo, gdyby stał na więzach nad grafem
segmentów. Pytanie jest o podłoże, a nie o pokrycie, i dlatego odpowiedzią jest
porównanie dwóch programów nad tymi samymi zdaniami, a nie liczba nad korpusem.
Wynik czyta `docs/design-notes.md`, który trzyma drabinę kosztów i kąt parsujący.

Sonda nie jest częścią pakietu: `include` w `pyproject.toml` wymienia sam `olski`
i sondy nie instaluje, żaden moduł `olski` jej nie importuje, a ona sama importuje z olskiego
morfologię, cechy i unifikację, żeby porównanie mierzyło podłoże, a nie dwa razy
napisany słownik. Zależność biegnie więc w jedną stronę i da się ją usunąć
skasowaniem katalogu.

Po co to stoi w repozytorium, a nie w koszu: figura wzięta programem, którego nie
ma, nie odtwarza się, i `TODO.md` trzyma to jako usterkę zebraną nad tabelami
`docs/corpus.md`. Sonda, której wynik cokolwiek rozstrzyga, jest tym samym
przypadkiem.
"""
