# Konstrukcje gramatyczne

Sekcja na konstrukcję: co gramatyka wpuszcza, jakim ciałem i ile to kosztowało.
Rejestru nie czyta się od góry — czytelnik przebiega go do swojego wpisu.
Wylicza te konstrukcje [lista pokrycia](../subset.md#what-the-grammar-covers),
a czym jest ważność i co mówi odrzucenie, wykłada [subset.md](../subset.md).

Cenę i zakup piszemy tu w rzędzie wielkości albo granicą, a nie liczbą dokładną,
bo liczbę dokładną unieważnia dopisanie do gramatyki i unieważnia ją po cichu.
Która liczba zostaje mimo to dokładna, wylicza
[CLAUDE.md](../../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje).
Ten rejestr dokłada do tamtej listy jedną:
liczbę przypiętą do gramatyki, której już nie ma,
o ile zdanie obok mówi, że żaden przebieg jej nie powtarza.
Taka liczba jest ceną, przy której decyzja zapadła,
a nie figurą o gramatyce dzisiejszej.
Zero i jedno zostają zawsze, bo mówią kierunek, a nie wielkość.
Pełną precyzję ten rejestr miał i zszedł z niej dlatego,
że nie pilnuje jej żaden check: cenę przelicza przebieg nad korpusem,
a korpus jest archiwem, którego suita nie pobiera
([CLAUDE.md](../../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)).
Wróci ona wtedy, gdy cenę będzie przeliczał check —
tak jak `tests/test_wydruki.py` przelicza blok wydruku.

Konstrukcja dostaje w tym rejestrze sekcję, bo sekcja jest jego jednostką.
Podsekcję dostaje to, co kwalifikuje cenę jednej konstrukcji,
a konstrukcją obok niej nie jest.
Osią podziału na pliki jest warstwa, o którą sekcja pyta,
czyli gospodarz, do którego konstrukcja dochodzi.
Konstrukcja sięgająca dwóch warstw stoi w pliku tej, która ją wpuszcza,
bo od niej zaczyna czytelnik.

Wskazanie z zewnątrz nazywa plik razem z kotwicą, bo sam katalog nie mówi,
w której warstwie sekcja stoi.
Sekcja przeniesiona między te pliki unieważnia przez to każde wskazanie na siebie,
a przeniesienie kosztuje tyle, ile jest tych wskazań.
Cichym rozjazdem to nie grozi:
każde takie wskazanie przechodzi przez `tests/test_docs.py`,
który czyta i prozę, i cytaty z kodu.

## Który plik czytać

- [orzeczenie.md](orzeczenie.md) — formy czasownika, czas, tryb,
  cząstka zwrotna i przeczenie,
  a wraz z nimi pozycje ramy: predykatyw, łącznik `to`, czasownik nieosobowy
  i dopełnienie wysunięte przed formę osobową.
- [zdanie-złożone.md](zdanie-złożone.md) — czym wypowiedzenie spina dwa zdania
  i co obejmuje znak: interpunkcja zdaniowa i obejmująca,
  spójnik na czele zdania i wewnątrz niego,
  człon bez czasownika za spójnikiem.
- [podrzędność.md](podrzędność.md) — zdanie podrzędne, względne i pytanie
  wraz z wysunięciem na czoło oraz przecinkiem, który podrzędność wnosi w sobie.
- [grupa-imienna.md](grupa-imienna.md) — koordynacja i jej zasięg,
  przydawka, grupa liczebnikowa oraz zaimki wewnątrz grupy.
- [okolicznik.md](okolicznik.md) — przysłówek, cząstka, narzędnik bez przyimka
  i imiesłów przysłówkowy, czyli to, co określa zdanie,
  nie zajmując pozycji ramy.
