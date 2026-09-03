# Publikacja: dokumentacja i referencja API pod jednym adresem

Dokumentacja stoi pod `dokumentacja.olski.pl`,
a wydaje ją GitHub Pages z tego repozytorium.
Na stronę idzie proza, którą repozytorium już ma —
[README](../README.md), ten katalog, [`todo/`](../todo/README.md)
i [CLAUDE.md](../CLAUDE.md) —
oraz referencja API wypisana z docstringów pakietu.
Demo parsera stoi osobno, pod `olski.pl`, i opisuje je [witryna.md](witryna.md).

Buduje to `python3 -m dokumentacja`, jednym poleceniem i lokalnie.
Workflow woła to samo polecenie, więc przepis jest jeden, a nie dwa.
Adres stoi w `mkdocs.yml` jeden raz:
plik `CNAME`, którego żąda GitHub Pages, wychodzi z tamtego wiersza przebiegiem.

Samą prozę GitHub renderuje już dziś, w tej konwencji kotwic,
w której pisane są linki.
Strona dokłada do tego adres dla czytelnika, który o projekcie nie słyszał
([roles.md](roles.md#ktoś-kto-trafia-tu-pierwszy-raz)),
jedną wyszukiwarkę po prozie i po referencji naraz
oraz samą referencję API, której GitHub nie pokaże w ogóle,
bo docstring jest w pliku `.py`.

Dokument mówi, czemu strona nie stoi na domyślnym Jekyllu,
co sprawdza jej budowanie i ile kosztuje referencja API.
Wylicza na koniec to, na czym decyzja nie zapadła.

## Domyślny Jekyll kasuje diakrytyki z kotwic

GitHub Pages renderuje Markdown kramdownem,
a ten zostawia w kotwicy same znaki ASCII:
z nagłówka `Skreślenie bywa całą naprawą` wychodzi mu `skrelenie-bywa-ca-napraw`.
Sprawdza się to bez wdrożenia, na kramdownie 2.5.2:
`gem install kramdown`, a potem `Kramdown::Document.new("## …").to_html`.

Większość kotwic w tym repozytorium niesie diakrytyk,
więc na domyślnym Jekyllu większość linków między dokumentami prowadzi w pustkę.
Awaria jest przy tym cicha z dwóch stron naraz.
Kramdown kotwicy nie zgłasza, bo wystawia własną.
Suita jej nie zgłasza, bo `anchor_of` w `tests/test_docs.py`
pilnuje konwencji GitHuba, a nie tego, co wystawi strona.

## Korzeniem strony jest korzeń repozytorium

Z `docs/` i z `todo/` wychodzi kilkaset linków ponad swój katalog:
do README, do CLAUDE.md i do rejestru otwartej roboty.
Katalog `docs/` wydany sam urywa je wszystkie,
więc na stronę idzie proza w tym układzie katalogów, w którym stoi w repozytorium.

Układ ten składa `dokumentacja.py` w katalogu `_dokumentacja/`,
a stronę wypisuje z niego mkdocs do `_strona/`.
Oba katalogi są wynikiem przebiegu i stoją w `.gitignore`.
Proza linkuje też do modułu, do `pyproject.toml` i do workflowu,
więc skrypt dokłada każdy plik, na który wskazuje link.
Listy tych plików nie ma nigdzie wypisanej:
właścicielem jest sama proza, a lista obok niej rozjeżdżałaby się z nią po cichu.

## Kotwica na stronie zgadza się z kotwicą na GitHubie

Kotwice liczy `slugify` z pymdown-extensions, wołany z `mkdocs.yml`.
Na nagłówkach tego repozytorium daje on to samo, co `github-slugger`,
czyli ta sama kotwica działa w obu miejscach i linku nie trzeba pisać dwa razy.
Tak samo liczy ją suita (`anchor_of` w `tests/test_docs.py`).

Sprawdza to `mkdocs build --strict`:
mkdocs porównuje każdą kotwicę z tym, co naprawdę wystawił,
a `--strict` czyni ostrzeżenie błędem.
Konwencji pilnują przez to dwa checki nad dwoma silnikami:
suita nad GitHubem, a budowanie nad stroną.

## Referencja API powstaje z docstringów

Wypisuje ją mkdocstrings z pakietu `olski`, i nie jest to druga kopia faktu:
kod jest właścicielem tego, co zaimplementowane
([CLAUDE.md](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely)),
a referencja powstaje z niego przy każdym budowaniu.
Docstringi są tu prozą pod
[łamaniem wierszy](../CLAUDE.md#semantic-line-breaks),
a pojedynczy nowy wiersz zwija się w spację, więc renderują się jak akapit.

Referencja jest częścią tej strony, a nie drzewem obok niej.
Każdy moduł dostaje stronę Markdown — nagłówek i wiersz `::: olski.check` —
więc mkdocs zna te strony tak samo jak dokumenty:
wciąga je do nawigacji, indeksuje jedną wyszukiwarką i renderuje tym samym motywem,
a symbol cytowany w docstringu prowadzi linkiem tam, gdzie go zadeklarowano.
Generator wypisujący własne drzewo HTML tego nie umie i dlatego tu go nie ma:
pdoc wystawiał referencję z własnym motywem i własnym oknem szukania,
a mkdocs nie wiedział o niej nic poza tym, że przenosi jej pliki.
Odwraca tę decyzję wydruk, którego mkdocstrings nie umie:
referencja wraca wtedy obok strony, a razem z nią drugie okno szukania.

Docstringi cytują symbol rolą reStructuredText, a mkdocstrings zna tylko własną składnię:
przekłada ją `dokumentacja.py`, a nie autor docstringu,
i tam też stoi powód, dla którego konwencja w kodzie zostaje ta sama.
Że przekład się wykonał, żąda samo budowanie,
bo rola przepuszczona na stronę nie wywraca przebiegu sama z siebie.

Ceną jest cytat dokumentu i widać ją na stronie:
docstring cytuje go gołym napisem, a nie linkiem,
i robi to kilkadziesiąt modułów pakietu,
więc w referencji te cytaty są martwym tekstem.
Wpis o tym trzyma [`todo/dokumenty.md`](../todo/dokumenty.md).

## Nawigacji nie piszemy ręką

Nawigację układa mkdocs z drzewa katalogów.
Wypisana w `mkdocs.yml` byłaby drugą kopią spisu z [README](README.md),
a spis ten mówi o każdym dokumencie zdanie i wskazuje właściciela faktu.
Dwie listy tych samych dokumentów rozjeżdżają się przy pierwszym dopisanym pliku,
a suita żąda wiersza tylko w tej pierwszej.

Referencja wchodzi do tej nawigacji tą samą drogą,
bo strony modułów wypisuje `dokumentacja.py` z drzewa modułów pakietu.
Moduł dopisany jutro dostaje przez to stronę bez wiersza dopisanego gdziekolwiek,
a spis modułów na wejściu do referencji liczy z pakietu mkdocstrings.

Podpisy strony, nazwa motywu i przełącznik motywu należą do `mkdocs.yml`,
tak jak podpisy demo należą do jego strony
([witryna.md](witryna.md#werdykt-idzie-w-tych-słowach-w-których-drukuje-go-olski-check)).

## Push buduje stronę, a wydaje ją tylko main

Robi to [`.github/workflows/dokumentacja.yml`](../.github/workflows/dokumentacja.yml).
Buduje przy każdym pushu, bo `--strict` jest sprawdzeniem:
martwy link ma wywrócić przebieg na gałęzi, a nie po scaleniu.
Wydanie jest osobnym zadaniem i czeka na `main`, bo adres jest jeden.

Do [bloku checków](../CLAUDE.md#checks) budowanie nie wchodzi.
mkdocs i mkdocstrings instaluje dodatek `dokumentacja` z `pyproject.toml`,
a suita go nie instaluje — tak samo jak nie instaluje gunicorna dla demo.
Ceną jest to, że o martwym linku mówi dopiero push,
a nie lokalny przebieg bloku checków.

## Nie zapadło

Czy DNS-y wskazują, czy GitHub Pages przyjmuje adres własny z pliku `CNAME`
i czy artefakt tej wielkości przechodzi,
mówi dopiero pierwszy przebieg na `main`.

## Sources

- <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-custom-domain-for-your-github-pages-site> — czego GitHub Pages żąda od adresu własnego i skąd bierze plik `CNAME`
- <https://kramdown.gettalong.org/converter/html.html#auto-ids> — jak kramdown liczy kotwicę z nagłówka
- <https://github.com/Flet/github-slugger> — kotwica w konwencji GitHuba, wraz z kodem, który ją liczy
- <https://www.mkdocs.org/user-guide/configuration/#validation> — co mkdocs sprawdza w linkach i w kotwicach
- <https://mkdocstrings.github.io/python/usage/> — co mkdocstrings wypisuje z modułu i którą opcją
- <https://mkdocstrings.github.io/griffe/extensions/> — czego griffe żąda od rozszerzenia i kiedy woła jego haki
