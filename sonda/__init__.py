"""Sonda: kod pisany po to, żeby rozstrzygnąć decyzję, a nie po to, żeby zostać.

Każdy moduł niżej jest osobną sondą wokół osobnej decyzji i sam mówi, o co pyta
i który dokument czyta jego wynik.

Żadna z sond nie jest częścią pakietu: `include` w `pyproject.toml` wymienia sam
`olski` i sond nie instaluje, żaden moduł `olski` ich nie importuje, a one same
importują z olskiego morfologię, cechy, unifikację i gramatykę, żeby mierzyć
podzbiór, który olski deklaruje, a nie drugi raz napisany słownik. Zależność
biegnie więc w jedną stronę i da się każdą z nich usunąć skasowaniem jej plików.

Po co sonda zostaje w repozytorium, a nie w koszu: figura wzięta programem,
którego nie ma, nie odtwarza się, a `TODO.md` zapisuje to jako usterkę zebraną
nad tabelami `docs/corpus.md`. Sonda, której wynik cokolwiek rozstrzyga, jest tym
samym przypadkiem.
"""
