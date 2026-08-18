"""Sonda: kod pisany po to, żeby rozstrzygnąć decyzję, a nie po to, żeby zostać.

Każdy moduł niżej jest osobną sondą wokół osobnej decyzji i sam mówi, o co pyta
i który dokument czyta jego wynik.

Żadna z sond nie jest częścią pakietu: `include` w `pyproject.toml` wymienia sam
`olski` i sond nie instaluje, żaden moduł `olski` ich nie importuje, a one same
importują z olskiego morfologię, cechy, unifikację i gramatykę, żeby mierzyć
podzbiór, który olski deklaruje, a nie drugi raz napisany słownik. Zależność
biegnie więc w jedną stronę i da się każdą z nich usunąć skasowaniem jej plików.

Po co sonda zostaje w repozytorium, a nie w koszu: figura wzięta programem,
którego nie ma, nie odtwarza się, a `TODO.md` zapisuje to jako usterkę zebraną nad
tabelami `docs/corpus.md`. Zostaje więc ta, której wynik czyta deklaracja figury w
`harness/figury.py` albo dokument, i tak długo, jak któreś z dwojga go czyta.

Wychodzi wtedy, gdy nie czyta go już żadne. Kod trzyma potem git, a sekcja, która
jej wynik cytowała, mówi to o sobie sama — `docs/design-notes.md` robi tak nad
figurami, których sondy już nie ma. Zapadła decyzja sama do kosza nie wystarcza:
sonda odmowy zostaje, bo odmowa wraca, kiedy zakup przestanie być zerem, i to ona
jest tym, co ten moment pokaże.

Kolejność jest przy tym częścią kryterium, a nie osobną ostrożnością: figura idzie
do `figury/` przed skasowaniem sondy, a nie po nim. Skasowana wcześniej zostawia
liczbę, której nikt nie weźmie drugi raz, bo git trzyma źródło sondy, a nie jej
wydruk, i odzyskanie liczby żąda wtedy korpusu i przebiegu zamiast przeczytania
pliku. Świadkiem decyzji jest więc plik figury, nie commit.

Kryterium stosuje się przy zmianie, która i tak tę sondę rusza, tak jak `CLAUDE.md`
każe przyjmować resztę reguł. Listy sond bez figury nikt nie drukuje i jest to
odmowa, a nie brak: taka lista czyta się jak kolejka do domknięcia, a domyka ją
taniej figura dopisana niż sonda skasowana, więc ograniczałaby aparat sond przez
jego rozbudowę.
"""
