"""Sonda: kod pisany po to, żeby rozstrzygnąć decyzję, a nie po to, żeby zostać.

Każdy moduł niżej jest osobną sondą wokół osobnej decyzji i sam mówi, o co pyta
i który dokument czyta jego wynik.

Żadna z sond nie jest częścią pakietu: `include` w `pyproject.toml` wymienia sam
`olski` i sond nie instaluje, żaden moduł `olski` ich nie importuje, a one same
importują z olskiego morfologię, cechy, unifikację i gramatykę, żeby mierzyć
podzbiór, który olski deklaruje, a nie drugi raz napisany słownik. Zależność
biegnie więc w jedną stronę i da się każdą z nich usunąć skasowaniem jej plików.

Sonda wychodzi z drzewa tym samym commitem, którym wchodzi to, co wyceniła.
Domyślne jest kasowanie, bo plik w drzewie płaci poprzeczkę repozytorium —
testy, docstring, przegląd, nazwy — a sonda wyceniająca konstrukcję
wpuszczaną tym samym commitem nie ma dla kogo tej ceny płacić.
Tak zrobiono raz: `c2377c3` skasował `sonda/pakowanie.py` razem z testem,
a jego liczby są do dziś w `docs/design-notes.md`.

Póki nie wiadomo, czy sonda zostaje, pisze się ją jak skrypt na jeden przebieg:
bez własnych testów, bez dopracowanego docstringa, bez reguł rejestru.
Poprzeczkę płaci dopiero ta, którą ktoś nazwał w `powtórzy` przy jej figurze.
Kolejność odwrotna marnuje pracę, a zostaje mniejszość sond.
Dwa żądania obowiązują mimo to od pierwszego wiersza,
bo nie są dopracowaniem, tylko warunkiem prawdziwości pomiaru:
sonda pyta o deklarację olskiego, zamiast pisać podzbiór drugi raz,
a wydruk nie bierze kolejności ze zbioru. Powody obu podaje `CLAUDE.md`.

Odtwarzalność bierze się z gita, a nie z drzewa: `w_gicie` w deklaracji figury
podaje commit, w którym leży skasowany program, i ten sam commit jest w nagłówku
pliku figury. Bez niego polecenie figury wskazuje moduł, którego nie ma.

Zostaje sonda, którą ktoś jeszcze puści, i tego kogoś nazywa `powtórzy`.
Pytanie jest o przyszłego czytelnika, a nie o stan wiedzy: zapadła decyzja nie
przesądza sama, bo sonda odmowy zostaje — odmowa wraca, kiedy zakup przestanie
być zerem, i pokaże ten moment jej przebieg.

Kryterium stosuje się przy zmianie, która i tak tę figurę rusza, tak jak
`CLAUDE.md` każe przyjmować resztę reguł. Listy sond bez figury nikt nie drukuje
i jest to odmowa, a nie brak: taka lista czyta się jak kolejka do domknięcia,
a domyka ją taniej figura dopisana niż sonda skasowana, więc ograniczałaby
aparat sond przez jego rozbudowę.
"""
