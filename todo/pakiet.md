# Pakiet, instalacja i testy

Trzy warstwy toru gramatycznego mają własny pakiet
(`olski/parse/`, `olski/subset/`, `olski/skład/`),
a dwie leżą luzem w `olski/`:
morfologia w czterech modułach, które wylicza tabela w
[`docs/architecture.md`](../docs/architecture.md#pięć-warstw-toru-gramatycznego),
oraz to, co nad parserem, czyli `olski/werdykt.py`, `olski/rozstrzyganie.py`,
`olski/pokrycie.py` i `olski/check.py`.
Obok nich leżą moduły, którym tabela nie przypisuje żadnej warstwy,
a `olski/lematy.py` mówi w docstringu, że pyta o niego więcej niż jedna.
Usterką to nie jest, bo granica warstwy jest tam granicą modułu albo pakietu,
a import między pakietami idzie w jedną stronę.
Ruchem jest osobny pakiet dla morfologii, na wzór tamtych trzech,
a nie przebieg po całym wierzchu.
Podejmuje go dopiero sesja, która tej warstwie dopisuje moduł
albo i tak przemianowuje jej ścieżki.
Cena jest w ścieżkach: moduły morfologii nazywa z dokumentów i rejestru
kilkanaście plików, a każdą taką nazwę pilnuje `tests/test_docs.py`.
Do przeczytania przed ruchem są importy `olski/segmentacja.py`,
bo czyta on `olski/grammar.py`, więc morfologia nie leży pod formalizmem, tylko obok niego,
i pakiet tę zależność albo przyjmuje, albo przecina.

`witryna/skrypt.js` jest jedynym plikiem w repozytorium, którego nic nie uruchamia.
Suita pyta o niego z zewnątrz jedno — czy strona woła trasy, które serwer ma
(`tests/test_witryna.py`) — a samego skryptu nie wykonuje,
bo w [bloku checków](../CLAUDE.md#checks) nie ma node'a
i dopisanie go tam kosztuje drugie środowisko w workflowie.
Decyzja robi się potrzebna wtedy, gdy skrypt zacznie cokolwiek liczyć;
dziś rysuje dane, a po stronie Pythona jest prawie wszystko, co może być nie tak —
poza tekstem, który przycisk kopiuje do schowka
([`docs/witryna.md`](../docs/witryna.md#ramy-nie-ma-bo-warstwa-http-jest-tablicą-tras)).
Ruchy są dwa i różnią się tym, co przyjmują za granicę:
albo node wchodzi do checków wraz z jednym testem strony w przeglądarce bezgłowej,
albo skrypt zostaje bez testu, a regułą staje się to,
że logika nie schodzi do przeglądarki.
Przeczytaj przed decyzją `tests/test_wydruki.py`,
bo pokazuje on, ile pilnowania da się zrobić bez drugiego środowiska.

The repository ships no licence.
`pyproject.toml` carries no `license` field and there is no `LICENSE` file,
so the terms under which any of this may be used are unstated.
The move is to pick one, add the file,
and set `license` in `pyproject.toml` to match.
Reading a GPL v3 parser of Polish is what raised it
(see [`docs/swigra.md`](../docs/swigra.md#why-wrapping-it-does-not-get-there)),
and the answer decides whether olski could ever link against such a thing.

`ruff format` nie stoi w [bloku checków](../CLAUDE.md#checks),
a nad kilkudziesięcioma plikami ma zdanie inne niż to,
co w nich stoi: wypisuje je `ruff format --check .`,
a `--diff` pokazuje, że różnica jest w miejscach łamania wiersza, nie w kodzie.
Wyborem to nie jest, bo [reguła o łamaniu](../CLAUDE.md#semantic-line-breaks)
oddaje kod zwykłemu narzędziu języka, a tym narzędziem jest tutaj ten formater.
Płaci za to ten, kto puści go na pliku, który akurat poprawia:
diff obejmuje wtedy wiersze, których nie tknął.
Ruchem jest jedno z dwojga — `ruff format --check .` dopisany do bloku checków
i do workflowu wraz z jednym przebiegiem po całym drzewie,
albo zdanie w `CLAUDE.md`, że formatera tu nie używamy,
a `ruff check` jest całym sprawdzeniem kodu.
Do przeczytania jest `ruff format --diff olski/parse/las.py`,
bo mówi, co ten przebieg zrobiłby z adnotacją typu rozbitą ręką na trzy wiersze.
