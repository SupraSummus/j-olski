# Mapa kodu

Krótki przewodnik po pakietach.
Szczegóły mówi kod i referencja API, którą strona dokumentacji wypisuje z docstringów.

## Front-end

- `olski/morph.py`: cienka warstwa nad Morfeuszem 2, czyli znaczniki, czytania i segmenty.
- `olski/segmentacja.py`: graf segmentacji zdania wraz z czytaniami form,
  z naprawami grafu (łącznik, skrót, cudzysłów, ścieżka pliku, słowo nieznane).
- `olski/document.py`: podział tekstu na zdania.
- `olski/grammar.py`: formalizm, czyli symbole, produkcje i unifikacja cech,
  w której wartość cechy jest zbiorem.
- `olski/parse/`: parser Earleya nad grafem segmentacji i las rozbiorów,
  który liczy czytania bez wypisywania ich i wylicza je od najtańszego.
- `olski/subset/`: gramatyka podzbioru polszczyzny, pisana ręką.
- `olski/precedencja.py`: dozwolone szyki produkcji, każdy ze swoją ceną.
- `olski/cennik.py`: ceny konstrukcji nacechowanych, które porządkują czytania.

## Leksykon

- `olski/walencja.py` nad `olski/leksykon.txt`: co czasownik i rzeczownik bierze.
- `olski/żądania.py` nad `olski/żądania.txt`: czego czasownik żąda od słowa w swojej pozycji.
- `olski/projekt.py`, `olski/konfiguracja.py`, `olski/słownictwo.py`:
  słowa projektu, których słownik nie zna, deklarowane w `olski.toml`.
- Pliki danych wypisują `harness/walenty.py`, `harness/żądania.py` i `harness/skłonności.py`.

## Werdykt

- `olski/werdykt/`: werdykt o zdaniu i o tekście.
- `olski/check.py`: polecenie `olski-check`.
- `olski/odniesienia.py`: zaimek wskazujący na dwie rzeczy.
- `olski/rozstrzyganie.py`: warstwa za parserem, która wskazuje przyłączenie
  z powtórzenia w akapicie, z ramy w leksykonie albo ze statystyki Składnicy.
- `olski/markdown.py`, `olski/python.py`: proza wyjęta z Markdownu i z modułów Pythona.

## Back-end

- `olski/skład/`: drzewo w kategoriach dziedziny wchodzi, polskie zdanie wychodzi.
  `składnia.py` ma kategorie drzewa, `morfologia.py` odmianę przez Morfeusza,
  a `opowieść.py` tekst złożony z kilku zdań.
- `olski/skład/rozbiór.py`: czytanie parsera zamienione w drzewo składu,
  czyli obieg zamknięty od strony tekstu; jedyna część składu, która woła parser.
- `olski/skład/przegląd.py`: czy czytelnik odzyska z wypisanego tekstu drzewo, z którego wyszedł.
- `olski/skład/makieta.py`: losowy tekst do makiety.

## Poza pakietem

- `harness/`: czytniki Składnicy, NKJP i ustaw, pomiar pokrycia (`harness/pomiar.py`)
  i ocena przyłączeń wobec wzorca czytanego ręką (`harness/wybory.py`).
- `witryna/`: aplikacja WSGI ze standardowej biblioteki i strona, która woła jej API.
- `dokumentacja.py`: buduje stronę dokumentacji z README, z `docs/` i z docstringów.
