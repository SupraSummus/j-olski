# Proza, którą to repozytorium pisze w kodzie

[Reguła językowa](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
robi z docstringa i z komentarza prozę pisaną po polsku,
i przybywa jej przy każdej zmianie w kodzie.
Nad dokumentem żądanie, żeby ta proza nie potykała się o to, co linter wytyka,
jest checkiem, bo [ekstrakcja](extraction.md) wyjmuje z dokumentu prozę.
Nad modułem robi to samo `harness/python.py`:

```sh
python3 -m harness.python sonda --into proza/
python3 -m olski proza/ --format report
```

`tests/test_docs.py` robi to samo bez katalogu pośrodku
i tam ten check stoi.
Ekstrakcja o język nie pyta,
więc puszczona nad modułem mieszanym wyciąga i angielskie docstringi.
Pyta o niego lista plików, których proza po polsku w całości nie stoi,
czyli [`tests/nie-po-polsku.txt`](../tests/nie-po-polsku.txt),
a `sonda/` stoi w poleceniu wyżej dlatego, że lista jej nie wymienia.

Ekstrakcja jest przekształceniem, na którym dopiero strzelają reguły,
więc jest winna rachunek z tego, co zmyśla,
tak samo jak reguła jest winna odsetek fałszywych trafień.
Tym rachunkiem jest ten dokument.
Co jest w nim wspólne z krokiem nad Markdownem —
że konstrukcja zostawia po sobie tekst, a nie dziurę po sobie,
i co ze sklejenia wierszy wynika dla reguł czytających koniec wiersza —
trzyma [tamten rachunek](extraction.md),
a tutaj stoi to, czym te dwa kroki się różnią.
Osobnym plikiem, a nie sekcją tamtego, bo tamten stoi po angielsku:
rachunek pisany po polsku w środku angielskiego pliku
byłby prozą, której ten check nie czyta,
skoro bierze dokument, który po polsku stoi w całości.

## Korpusem to nie jest

Które ekstrakcje jest winien korpus audytowy,
rozstrzyga [lista repozytoriów](audit-corpus.md#the-list) i nic poza nią,
bo [roadmap](roadmap.md#the-two-pieces-are-not-the-same-size)
każe wybrać listę, zanim ekstrakcja dostanie zakres.
Ten krok czyta jedno repozytorium, i jest nim to repozytorium.
Projekt, którego polszczyzna siedzi w komentarzach,
miałby czym zostać przeczytany, gdyby na listę wszedł,
ale decyzją byłoby jego wejście, a nie istnienie tego pliku.

## Ekstrakcja schodzi do docstringa, a pokrycie zostaje przy pliku

Dokument stoi w jednym języku, a moduł miesza dwa z założenia:
słowa kluczowe, klucze konfiguracji i API bibliotek zostają po angielsku,
a sekcja napisana przed regułą językową zostaje taka, jaka jest,
bo regułę przyjmujemy leniwie.
Wychodzi więc stąd docstring i blok komentarza z osobna, a nie plik naraz,
bo tyle stoi w jednym języku i tyle daje się nad cudzym repozytorium wybrać.

Doborem to nie jest, a przynajmniej nie tutaj.
Które pliki tego repozytorium check czyta,
mówi [lista](../tests/nie-po-polsku.txt) i nic poza nią,
a [dlaczego wypisana, a nie policzona](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie),
stoi przy regule językowej.
Nad plikiem, którego lista nie wymienia, check bierze każdą jednostkę,
także tę krótszą od zdania:
w pliku zadeklarowanym po polsku nie ma czego wybierać.
Próg i podłoga na słowa zostają przy `--polish` i `--min-words`,
czyli przy ekstrakcji nad korpusem, którego nikt za nas nie zadeklarował,
i to, czego one nie rozstrzygają,
mówi `polish_share` w `harness/__init__.py`.

Blokiem komentarza jest tyle sąsiadujących wierszy, ile czyta się naraz.
Przerywa go wiersz kodu i przerywa go komentarz dopisany na końcu wiersza kodu,
bo taki mówi o tym wierszu, a nie ciągnie zdania z góry.

## Wiersze akapitu sklejają się, choć pliku źródłowego nikt nie składa

Nad Markdownem sklejenie oddaje to, co zrobiłby renderer.
Tutaj rendererem jest czytelnik, który czyta źródło,
więc koniec wiersza w komentarzu jest końcem wiersza, który ktoś widzi,
i reguła czytająca koniec wiersza miałaby tu przesłankę,
której rejestr dokumentacji jej nie daje.
Nie dostaje jej.

Łamanie wiersza w komentarzu jest albo zawinięciem na kolumnie,
albo łamaniem semantycznym,
jednym i drugim w tym samym pliku,
a to, o co taka reguła prosi, czyli twarda spacja przed jednoliterowym słowem,
w kodzie źródłowym czyta się gorzej niż to słowo zostawione na końcu wiersza.
Rejestrem, którego takie reguły chcą, jest tekst, który ktoś złoży,
a nie każdy tekst, który stoi w wierszach.
Pakiet miał dwie takie reguły i nie ma żadnej,
a ten akapit jest jednym z powodów:
resztę trzyma
[odczyt, który je usunął](firing-rates.md#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt).

## Przykład wychodzi po wcięciu, bo ogrodzenia w docstringu nie ma

Blok zaczynający się od wcięcia jest tu tym, czym w Markdownie blok ogrodzony:
poleceniem powłoki pod dwukropkiem albo kawałkiem kodu.
Wcięcie w środku akapitu jest czym innym, bo ciągnie się nim pozycja listy,
i zostaje.
Zapowiedź, czyli podwojony dwukropek reST,
schodzi do jednego znaku razem z przykładem pod sobą,
bo zostawiona parą trafia do reguł jako dwukropek bez spacji po nim,
czyli jako znalezisko, którego nikt nie napisał.

Znak komentarza zdejmujemy bez spacji, która za nim stoi,
a wcięcie bloku całe naraz.
Repozytorium pisze narrację w komentarzu od dwóch spacji,
a stałą dokumentuje jedną z dwukropkiem,
więc zdjęcie po jednej spacji zostawiałoby narrację wciętą o jedną,
czyli czytaną jak przykład, czyli wyrzucaną w całości.

## Czego ten krok nie rozpoznaje

- **Zakomentowany kod.**
  Komentarz jest tu prozą bez pytania, co w nim stoi,
  i nad cudzym repozytorium ta klasa ważyłaby ze wszystkich najwięcej.
  Tutaj nie waży nic, bo komentarz powtarzający kod, przy którym stoi,
  jest [szumem, który przegląd wycina](../CLAUDE.md#the-review-pass).
- **Łańcuch, który jest prozą.**
  `justification` reguły jest prozą tak samo jak docstring,
  a nie jest ani docstringiem, ani komentarzem, więc tędy nie wychodzi.
  Sięga się po niego deklaracją, a nie tekstem pliku,
  i [TODO.md](../TODO.md) trzyma ten ruch.
- **Doctest.**
  Blok `>>>` niewcięty wychodzi stąd jako akapit prozy.
  Żaden docstring w tym repozytorium go nie pisze.
- **Moduł, który się nie parsuje.**
  Przebieg staje na nim, zamiast go pominąć,
  bo drzewo składniowe jest tym, czym dochodzi się do docstringów.
  Nad tym repozytorium taki plik przewraca wcześniej cały suite,
  więc pominięcie go byłoby ciszą kupioną za nic.
- **Dwa języki w jednej jednostce.**
  Ekstrakcja schodzi do docstringa i niżej się nie zapuszcza,
  więc polskie zdanie w angielskim docstringu
  albo przepada razem z tym docstringiem, albo wciąga go całego do korpusu,
  zależnie od tego, co z tym docstringiem zrobi dobór nad cudzym repozytorium.
  Nad tym repozytorium nic na tym nie stoi:
  pokrycie bierze plik w całości,
  a plik mieszany [czeka na przekład](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
  tak samo jak dokument.
