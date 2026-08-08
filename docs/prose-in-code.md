# Proza, którą to repozytorium pisze w kodzie

[Reguła językowa](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie)
robi z docstringa i z komentarza prozę pisaną po polsku,
i przybywa jej przy każdej zmianie w kodzie.
Nad dokumentem żądanie, żeby ta proza nie potykała się o to, co linter wytyka,
jest checkiem, bo [ekstrakcja](extraction.md) wyjmuje z dokumentu prozę.
Nad modułem robi to samo `harness/python.py`:

```sh
python3 -m harness.python olski harness tests --into proza/ \
    --polish 0.12 --min-words 20
python3 -m olski proza/ --format report
```

`tests/test_docs.py` robi to samo bez katalogu pośrodku,
jednostka po jednostce, i tam ten check stoi.

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

## Jednostką jest docstring albo blok komentarza, a nie plik

Dokument stoi w jednym języku, a moduł miesza dwa z założenia:
słowa kluczowe, klucze konfiguracji i API bibliotek zostają po angielsku,
a sekcja napisana przed regułą językową zostaje taka, jaka jest,
bo regułę przyjmujemy leniwie.
Próg policzony nad całym plikiem nie ma więc nad czym stanąć.

Policzony nad jednostką potrzebuje jeszcze podłogi.
Jednostka bywa krótsza od zdania,
a udział diakrytyków nad ośmioma słowami skacze o całą ósmą,
więc dobór ma obok progu podłogę na słowa,
a jednostka spod podłogi wypada z korpusu,
bo nad taką ten udział nie mówi, w jakim ona stoi języku.
Obie liczby stoją w `tests/test_docs.py` i nie stoją w żadnym dokumencie,
bo mierzy się je nad prozą tego repozytorium,
którą rusza każde przeredagowanie komentarza,
a [tam żadna reguła przebiegu nie sięga](../CLAUDE.md#checks).
Ten dobór pokazuje polecenie wypisane wyżej.

Blokiem komentarza jest tyle sąsiadujących wierszy, ile czyta się naraz.
Przerywa go wiersz kodu i przerywa go komentarz dopisany na końcu wiersza kodu,
bo taki mówi o tym wierszu, a nie ciągnie zdania z góry.

## Wiersze akapitu sklejają się, choć pliku źródłowego nikt nie składa

Nad Markdownem sklejenie oddaje to, co zrobiłby renderer.
Tutaj rendererem jest czytelnik, który czyta źródło,
więc koniec wiersza w komentarzu jest końcem wiersza, który ktoś widzi,
i [dwie reguły czytające koniec wiersza](extraction.md#after-joining-a-line-end-rule-has-nothing-left-to-read)
miałyby tu przesłankę, której rejestr dokumentacji im nie daje.
Nie dostają jej.

Łamanie wiersza w komentarzu jest albo zawinięciem na kolumnie,
albo łamaniem semantycznym,
jednym i drugim w tym samym pliku,
a to, o co te reguły proszą, czyli twarda spacja przed jednoliterowym słowem,
w kodzie źródłowym czyta się gorzej niż to słowo zostawione na końcu wiersza.
Rejestrem, którego te reguły chcą, jest tekst, który ktoś złoży,
a nie każdy tekst, który stoi w wierszach.
[TODO.md](../TODO.md) trzyma decyzję, czy pakiet taki rejestr ogłasza,
i ta ekstrakcja jej nie wyprzedza.

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
  Dobór schodzi do docstringa i niżej się nie zapuszcza,
  więc polskie zdanie w angielskim docstringu
  albo przepada razem z tym docstringiem, albo wciąga go całego do korpusu.
  Nad dokumentem to samo jest rozstrzygnięte i rozstrzygnięte inaczej:
  plik mieszany [czeka na przekład w całości](../CLAUDE.md#piszemy-po-polsku-także-w-kodzie),
  bo tam jednostką mniejszą od pliku byłby akapit,
  a akapit po angielsku cytujący polskie przykłady
  niesie diakrytyków tyle samo, co polski.
