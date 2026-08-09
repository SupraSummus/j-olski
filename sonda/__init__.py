"""Sonda: kod pisany po to, żeby rozstrzygnąć decyzję, a nie po to, żeby stać.

Pakiet trzyma dwie sondy, każdą wokół innej decyzji.

`sonda/__main__.py` wraz z `polszczyzna.py` i `wiezy.py` pyta, czy podzbiór,
który dzisiaj stoi na gramatyce bezkontekstowej, powiedziałby to samo, gdyby
stał na więzach nad grafem segmentów. Pytanie jest o podłoże, a nie o pokrycie,
i dlatego odpowiedzią jest porównanie dwóch programów nad tymi samymi zdaniami,
a nie liczba nad korpusem. Wynik czyta `docs/design-notes.md`, który trzyma
drabinę kosztów i kąt parsujący.

`sonda/przecinek.py` pyta, ile kosztuje koordynacja przecinkiem, i tu
odpowiedzią jest właśnie liczba nad korpusem: ruch werdyktu nad Składnicą
między gramatyką z tą produkcją i bez niej. Wynik czyta `docs/subset.md`.

Żadna z sond nie jest częścią pakietu: `include` w `pyproject.toml` wymienia sam
`olski` i sond nie instaluje, żaden moduł `olski` ich nie importuje, a one same
importują z olskiego morfologię, cechy, unifikację i gramatykę, żeby mierzyć
podzbiór, który stoi, a nie drugi raz napisany słownik. Zależność biegnie więc w
jedną stronę i da się każdą z nich usunąć skasowaniem jej plików.

Po co to stoi w repozytorium, a nie w koszu: figura wzięta programem, którego nie
ma, nie odtwarza się, i `TODO.md` trzyma to jako usterkę zebraną nad tabelami
`docs/corpus.md`. Sonda, której wynik cokolwiek rozstrzyga, jest tym samym
przypadkiem.
"""
