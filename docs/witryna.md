# Witryna: werdykt w przeglądarce, na jednym dynie

Witryna jest bocznym torem: wkleja się do niej tekst,
a wraca to samo, co drukuje `olski-check` na klonie.
Serwer i strona jadą na jednym dynie,
czyli w jednym kontenerze, jaki Scalingo uruchamia z tego repozytorium.
Bazy danych nie ma i nie ma czego w niej trzymać,
bo werdykt zależy od tekstu i od gramatyki, a nie od tego, kto pyta.

Dokument mówi, czym witryna jest wobec rdzenia,
jakie decyzje niesie jej kod
i czego o wdrożeniu nikt jeszcze nie sprawdził.
Kod wołany po drugiej stronie API opisuje
[architecture.md](architecture.md), a nie ten plik.

## Boczny tor znaczy, że rdzeń o witrynie nie wie

Import idzie w jedną stronę.
`witryna/werdykty.py` woła olskiego,
a w `olski/` nie ma ani jednego wiersza, który wołałby witrynę.
Pakiet `witryna/` leży przy tym poza paczką, tak jak `harness/` obok niego:
`[tool.setuptools.packages.find]` bierze samo `olski*`,
więc `pip install olski` nie przynosi ani serwera, ani strony.

Powodem tego układu jest to, co z niego wychodzi.
Kto klonuje repozytorium po parser, instaluje tyle, ile instalował.
Kto psuje witrynę, gramatyki nie rusza, bo gramatyka o niej nie wie.
Kto psuje gramatykę, psuje witrynę, i to jest właściwy kierunek zależności.

Blok checków w [CLAUDE.md](../CLAUDE.md#checks) nie rośnie od tego toru.
Aplikacja jest zwykłą funkcją WSGI,
więc suita woła ją wprost, bez serwera pod spodem i bez portu,
a `tests/test_witryna.py` podaje jej słownik środowiska i czyta odpowiedź.
Zależnością wykonawczą witryny jest sam gunicorn i deklaruje go dodatek `witryna`,
którego suita nie instaluje.

## Werdykt idzie w tych słowach, w których drukuje go `olski-check`

Frazę werdyktu ma na własność kod: `Verdict.explain` w `olski/subset.py`.
Witryna jej nie tłumaczy i drugiej nie pisze,
więc przez API idzie `one reading` oraz `no reading: the analysis stops at „ustawienia”`,
czyli angielskie zdania na polskiej stronie.

Cena jest widoczna i płacimy ją rozmyślnie.
Tłumaczenie na polski byłoby drugą kopią tej frazy,
a druga kopia rozjeżdża się po cichu:
zmiana w `explain` zostawiłaby na stronie zdanie,
którego olski już o żadnym zdaniu nie mówi,
i nie zgłosiłby tego żaden check.
Po polsku jest zatem wszystko, co o zdaniu nie orzeka —
podpisy, przyciski, legenda statusów, nagłówki sekcji —
bo tego kod nie drukuje i właścicielem tego jest strona.

Klucze JSON-a wybieramy sami, więc są po polsku.
Nazwy roli w czytaniu — `Subject`, `Object`, `Verb`, `Modifier` —
przychodzą z `DEKLARACJA` w `olski/subset.py` i zostają takie, jakie przyszły.

## API oddaje dane, a nie HTML

Strona jest klientem API, a nie jego wnętrzem.
Serwer oddaje JSON, więc odpowiada tak samo curlowi i przeglądarce,
a strona wybiera, co z tych danych pokazać:
zdanie olskie dostaje swoje jedno czytanie rozwinięte,
a zdanie, którego streszczeń jest kilka, dostaje je zwinięte pod podpisem.

Odrzucone zostało oddawanie fragmentów HTML,
czyli to, co robi się dziś htmxem.
Powód jest ten sam, który stoi nad frazą werdyktu:
serwer składający HTML staje się drugą warstwą prezentacji,
a wtedy podpisy przy werdykcie mają dwóch właścicieli — serwer i stronę —
i nie widać, który z nich obowiązuje.
Przeładowanie całej strony odrzucamy z powodu prostszego:
gubi ono tekst w polu, a API zostawia takie,
że nie da się go zawołać niczym poza tą jedną stroną.

Każde zdanie ma przycisk, który kopiuje jego werdykt do schowka,
bo blok na stronie czyta się okiem,
a do zgłoszenia albo do `TODO.md` wkleja się tekst.
Tekst ten składa strona, a nie serwer,
z tego samego powodu, z którego serwer nie oddaje HTML:
pole z gotowym tekstem w odpowiedzi byłoby drugą warstwą prezentacji.
Schowek wymaga kontekstu bezpiecznego, czyli https albo localhosta;
gdzie przeglądarka go nie daje, przycisku nie ma,
bo przycisk, który zawsze odmawia, jest gorszy niż jego brak.

Stronę i API oddaje przy tym jeden dyno.
Strona wzięta z osobnego adresu żądałaby nagłówków CORS,
drugiego wdrożenia i drugiego rachunku,
a kupowałaby to, czego strona z trzech plików nie potrzebuje.

## Ramy nie ma, bo warstwa HTTP jest tablicą tras

Cała warstwa HTTP to tablica tras w `witryna/serwer.py`,
jeden typ odpowiedzi i jeden wyjątek na odmowę.
Rama — Flask albo FastAPI — kupuje routing, walidację i serializację,
a tutaj routing jest słownikiem na kilka par,
walidacją jest pytanie, czy przyszedł napis i czy nie jest dłuższy niż granica,
a serializacją jest `json.dumps`.
Zależność wykonawcza za to jest jedna i nietrywialna:
gunicorn, bo mówienie po HTTP wprost do internetu
jest robotą, której nie pisze się ręką.
Biblioteka wchodzi zatem tam, gdzie robota jest trudna,
a rozdanie kilku tras trudne nie jest.

Odwraca to piąty rodzaj żądania —
logowanie, wysyłka pliku, granica na adres, strumień.
Wtedy rama wchodzi, a wymiana jest lokalna,
bo aplikacja WSGI jest tym samym interfejsem po obu stronach
i strona jej nie zauważy.

Strona nie ma ramy ani kroku budowania z tego samego powodu.
Stanem strony jest jedno pole tekstowe i lista wyników,
więc React kupowałby diffowanie widoku, którego nie ma co diffować,
a płaciłby npm w blokach checków oraz paczką,
która waży więcej niż wszystko, co ta strona wysyła.
Trzy pliki jadą tak, jak stoją w repozytorium.
Odwraca to stan po stronie przeglądarki:
historia, cofanie albo kilka widoków, i wtedy biblioteka wchodzi.

Cena tej decyzji jest jedna i suita jej nie łapie:
`witryna/skrypt.js` nie ma testu, bo w blokach checków nie ma node'a.
Trzyma to `TODO.md`, a robocza odpowiedź jest taka,
że skrypt rysuje dane i nie liczy niczego,
więc prawie wszystko, co może być nie tak, siedzi po stronie Pythona.
Wyjątkiem jest tekst dla schowka, którego nie składa nic poza stroną.
Suita pyta o niego jedno z zewnątrz: czy strona woła te adresy, które serwer ma.

## Co witryna pokazuje

| trasa | metoda | co daje |
| --- | --- | --- |
| `/` | GET | strona, czyli `witryna/strona.html` wraz ze stylem i skryptem |
| `/werdykt` | POST | werdykt o każdym zdaniu tekstu wraz z podsumowaniem całości |
| `/makieta` | GET | tekst do makiety z drugiego toru, wraz z ziarnem |

Werdykt niesie to, co drukuje `olski-check` z flagami:
status, wyjaśnienie, czytania, dalsze zatrzymania
oraz to, co zgaduje warstwa rozstrzygająca.
Domysł tej warstwy dostaje na stronie znak zapytania i osobny podpis,
bo nie jest werdyktem
([architecture.md](architecture.md#warstwa-rozstrzygająca-wydaje-zawężenie-z-powodem-a-nie-znaczenie)).

```sh
curl -s localhost:8000/werdykt -H 'Content-Type: application/json' \
  -d '{"tekst": "Zapisz plik konfiguracyjny."}'
```

```json
{
 "zdania": [
  {
   "zdanie": "Zapisz plik konfiguracyjny.",
   "status": "valid",
   "wyjaśnienie": "one reading",
   "czytania": [
    {
     "Object": "plik konfiguracyjny",
     "Verb": "Zapisz"
    }
   ],
   "liczba_czytań": 1,
   "urwane": false,
   "rozbieżne": [],
   "dalsze_zatrzymania": [],
   "domysły": []
  }
 ],
 "podsumowanie": {
  "olskie": 1,
  "zdań": 1,
  "z_czytaniem": 1,
  "fragmentów": 0,
  "wyjaśnienie": "1 of 1 sentences are olski, and 1 have a reading"
 },
 "granica_znaków": 4000
}
```

Lista pod kluczem `czytania` niesie streszczenia różne, każde raz
(`Verdict.readings` w `olski/subset.py`),
a `liczba_czytań` wychodzi z lasu i mówi, ile czytań zdanie ma.
Jedna z drugiej się przez to nie wylicza,
więc o granicy wyliczania z `MAX_READINGS` w `olski/parse.py`
mówi osobne pole `urwane`, a strona wpisuje je do podpisu zwoju.
Pod `rozbieżne` idą konstytuenty, których wieloznaczność ta lista zostawia
nienazwaną, wraz ze streszczeniami ich kształtów,
a strona daje każdemu z nich własny spis pod tym samym zwojem.
Granicę znaków oddaje sama odpowiedź, bo licznik pod polem liczy przy niej,
a wpisana w skrypcie byłaby drugą kopią liczby z serwera.

```sh
curl -s 'localhost:8000/makieta?ziarno=1871&akapity=1'
```

```json
{
 "ziarno": 1871,
 "akapitów": 1,
 "tekst": "Czeladnik zapłakał w wąskiej piwnicy. Próbował wrócić na ulicę. Sukno znalazło bochenki i nie stało w nocy. Czeladnik zasnął. Ponieważ córka zeszła od młodej wdowy, nie zamknął zegara. Sukno podniosło beczki i dużą skrzynię."
}
```

Bloki te odtwarza `tests/test_witryna.py`:
puszcza polecenie stojące nad blokiem i porównuje odpowiedź z tym, co pod nim,
bo blok wklejony ręką rozjeżdża się po cichu z każdą zmianą w werdykcie
([CLAUDE.md](../CLAUDE.md#pomiar-i-liczba-która-po-nim-zostaje)).

Sond witryna nie wystawia i nie ma z czego.
Pomiar czyta bank drzew albo korpus audytowy,
czyli archiwa dziesiątek megabajtów, których na dynie nie ma
([corpus.md](corpus.md#fetching-it)),
a ekstrakcja przyjmuje katalog Markdownu, a nie wklejone zdanie.
Kto mierzy, ma klon i `harness/`.

## Granice są granicami dyna

Tekst wchodzi przycięty do granicy z `NAJWIĘCEJ_ZNAKÓW` w `witryna/serwer.py`,
czyli do kilku tysięcy znaków.
Dyno liczy jednym procesem na żądanie,
a wklejony cudzy korpus zająłby go na tyle,
że strona przestałaby odpowiadać komukolwiek innemu.
Najgorsze zdania, jakie umiem napisać, idą przy tej długości pod sekundę,
a worker ginie po granicy z `--timeout` w `Procfile`,
która stoi rząd wielkości nad tym pomiarem i kilka razy pod granicą routera.
Zabity worker wstaje z powrotem, więc żądanie zapętlone kosztuje jedno żądanie,
a nie stronę milczącą do restartu.
Żądanie dłuższe odpada na `Content-Length`, czyli przed dekodowaniem,
a żądanie bez tego nagłówka odpada również,
bo czytanie z gniazda bez granicy jest tym, co dyno zabija.

Uwierzytelnienia nie ma i granicy na adres nie ma,
więc witryna postawiona pod adresem publicznym jest otwarta dla każdego.
Jest to decyzja, a nie przeoczenie:
witryna liczy z wejścia, którego nie zapisuje,
więc najgorsze, co komuś wolno, to zająć dyno na sekundę.
Zmienia to dopiero koszt widoczny na rachunku.

## Ile to bierze pamięci

Proces z wczytanym słownikiem bierze przeszło sto megabajtów,
a każdy następny worker dokłada do tego kilka, a nie tyle samo:
słownik Morfeusza wchodzi z pliku i jego strony są wspólne,
a gramatykę buduje `--preload` raz, w procesie nadrzędnym.
Cała witryna mieści się zatem w kontenerze S,
czyli w 256 megabajtach, i to jest ta wielkość, dla której to napisano.

Workerów jest w `Procfile` więcej niż jeden i nie dla przepustowości:
przy jednym rozbiór trwający sekundę wstrzymuje żądanie o styl i o skrypt,
więc strona z pustym polem tekstowym czekałaby na cudze zdanie.

Liczby te bierze się przebiegiem, bo rusza je wydanie Morfeusza
i rozmiar gramatyki: uruchom `Procfile` lokalnie,
zawołaj `/werdykt` i przeczytaj `Pss` z `/proc/<pid>/smaps_rollup`
dla procesu nadrzędnego i każdego workera.
Sam wielki słownik trzeba przy tym zawołać żądaniem,
bo Morfeusz wczytuje go leniwie, przy pierwszej analizie,
i pomiar zrobiony przed pierwszym żądaniem mówi o połowie tej pamięci.

## Wdrożenie

Platforma czyta z repozytorium trzy pliki.
`requirements.txt` mówi jej, że to aplikacja Pythona,
a w środku ma jeden wiersz `.[witryna]`, czyli wskazanie na `pyproject.toml`;
właścicielem zależności zostaje `pyproject.toml`, a nie ten plik.
`Procfile` mówi, co uruchomić, i tam stoi wywołanie gunicorna.
`.python-version` przypina wersję do tej,
na której blok checków puszcza suitę.

Morfeusz 2 jest zależnością wykonawczą i wchodzi z PyPI,
a jego wheel jest zbudowany na `manylinux_2_28` w wariancie `abi3`,
więc jednym plikiem obsługuje każdy Python od 3.10 w górę.
Sprawdza się to bez wdrożenia:
`pip download --only-binary :all: morfeusz2` na Linuksie x86-64
albo pobiera koło, albo mówi, że go nie ma.
Bez Morfeusza witryna nie wstanie w ogóle,
bo gramatyka czyta słownik przy imporcie
([CLAUDE.md](../CLAUDE.md#checks)).

## Nie zapadło

Wdrożenia nikt nie puścił.
Kod, `Procfile` i `requirements.txt` są napisane pod Scalingo,
a to, czy slug się zbuduje i czy proces wstanie,
mówi dopiero pierwsze `git push scalingo`.
Do sprawdzenia są przy tym dwie rzeczy naraz:
czy buildpack instaluje wheel Morfeusza
i czy kontener S wystarcza pod obciążeniem, a nie na pustym przebiegu.

Adresu nie ma i nie wiadomo, czy witryna ma go mieć.
Strona pod adresem publicznym jest zaproszeniem dla kogoś z zewnątrz,
a [roles.md](roles.md#rola-jest-postawą-nie-osobą) mówi,
że tutaj każdą rolę obsadza jedna osoba
i że jest to stan, którego warto pilnować.
Witryna sama tego nie łamie, bo obsługuje tę samą osobę w przeglądarce,
a rozstrzyga to dopiero ten, kto wpisze domenę.

## Sources

- <https://doc.scalingo.com/languages/python/start> — po czym buildpack poznaje aplikację Pythona i skąd bierze wersję
- <https://doc.scalingo.com/platform/internals/container-sizes> — wielkości kontenerów wraz z pamięcią
- <https://doc.scalingo.com/platform/internals/routing> — granice routera, w tym czas na pierwszą odpowiedź
- <https://pypi.org/project/morfeusz2/> — wydania Morfeusza wraz z wariantami wheela
- <https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText> — czego pisanie do schowka żąda od strony
