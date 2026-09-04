# Witryna: werdykt w przeglądarce, w jednym kontenerze

Witryna jest bocznym torem.
Wkleja się do niej tekst, a wraca to samo, co na klonie drukuje wiersz poleceń.
Serwer i strona jadą w jednym kontenerze.
Scalingo uruchamia go z tego repozytorium.
Bazy danych nie ma i nie ma w niej czego trzymać,
bo werdykt zależy od tekstu i od gramatyki.
Kto pyta, nie ma znaczenia.

Dokument mówi, czym jest witryna wobec rdzenia i które decyzje niesie jej kod.
Wylicza na koniec pytania o wdrożenie, które zostają otwarte.
Kodu po drugiej stronie API ten plik nie opisuje.
Opisuje go [architecture.md](architecture.md).

## Boczny tor znaczy, że rdzeń o witrynie nie wie

Kierunek importu jest jeden.
`witryna/werdykty.py` woła olskiego,
a rdzeń nie ma wiersza, który wołałby witrynę.
Poza paczką leżą przy tym dwa katalogi, `witryna` i `harness`.
W `pyproject.toml` deklaracja paczki wylicza sam pakiet `olski`,
więc zainstalowana paczka nie przynosi ani serwera, ani strony.

Ten układ kupuje trzy rzeczy.
Kto przychodzi po parser, instaluje tyle, ile instalował.
Kto psuje witrynę, gramatyki nie rusza, bo gramatyka nie zna witryny.
Kto psuje gramatykę, psuje witrynę.
Ten kierunek zależności jest właściwy.

Blok checków nie rośnie od tego toru.
Aplikacja jest zwykłą funkcją WSGI,
więc suita woła ją wprost i nie potrzebuje serwera ani portu.
`tests/test_witryna.py` podaje jej słownik środowiska i czyta odpowiedź.
Zależnością wykonawczą witryny jest gunicorn.
Deklaruje go dodatek `witryna`, a suita go nie instaluje.

## Strona zaczyna od tego, czym olski jest

Pod adresem publicznym strona dostaje czytelnika, który o projekcie nie słyszał
([roles.md](roles.md#ktoś-kto-trafia-tu-pierwszy-raz)).
Pierwsze akapity mówią więc, czym jest parser i czym jest jedno odczytanie,
a pole tekstowe jest dopiero pod nimi.
Żart o spiłowanym `p` jest w tym układzie podpisem pod wprowadzeniem.
Tłumaczy on nazwę, a przeczytany pierwszy nie tłumaczy niczego.

Wprowadzenie jest streszczeniem [README](../README.md).
Mówi ono mniej dokładnie niż tamten plik.
Ani liczb, ani wywodu strona nie powtarza, a odsyła do repozytorium,
więc zmiana README nie zostawia tutaj kopii nieaktualnej.
Wyjaśnienie dłuższe niż dwa zdania wchodzi zwinięte,
bo czytelnik przyszedł po werdykt o własnym zdaniu,
a nie po akapit o wieloznaczności.

Lista zastosowań mówi, co dałoby się zbudować z parsera.
Zdanie nad listą mówi, że nikt niczego z tego nie zbudował.
Bez tego zdania lista obiecuje funkcje, których na stronie nie ma.
Właścicielem listy jest strona, bo na to pytanie nie odpowiada żaden dokument.
[roadmap.md](roadmap.md#cele) wylicza cele, czyli sprawdziany narzędzia.
Nie wylicza tego, co ktoś mógłby z niego złożyć.

Oba tory pokazują się przy wejściu same: strona woła werdykt i makietę,
zanim ktokolwiek naciśnie przycisk.
Do pierwszego kliknięcia sekcja jest pusta i nie mówi, co jest pod przyciskiem.
Dwa żądania naraz idą do różnych workerów
([niżej](#ile-to-bierze-pamięci)).

## Werdykt idzie w tych słowach, w których drukuje go `olski-check`

Fraza werdyktu należy do kodu: `Verdict.explain` w `olski/werdykt.py`.
Witryna nie tłumaczy jej i nie pisze drugiej.
Przez API idzie więc to samo zdanie, które drukuje komenda:
`jedno odczytanie` albo `brak odczytania: analiza staje na „i”`.

Polska fraza napisana na stronie byłaby drugą kopią.
Druga kopia rozjeżdża się po cichu.
Zmiana w `Verdict.explain` zostawiłaby na stronie zdanie,
którego olski o żadnym zdaniu już nie mówi.
Nie zgłosiłby tego żaden check.
Przez to werdykt należy do kodu.
Podpisy, przyciski, legenda statusów i nagłówki sekcji należą do strony.
Wiersz o dalszym zatrzymaniu składają dwa miejsca w tym samym brzmieniu:
komenda w `olski/check.py` i strona w `witryna/skrypt.js`.
API oddaje pod tym kluczem same formy, a nie zdanie o nich.
Wiersz morfologii składają te same dwa miejsca z tego samego powodu:
pod tym kluczem idzie forma wraz ze swoimi odczytaniami,
a nie gotowy wiersz o niej.

Tak samo należy do kodu nazwa pozycji cennika, którą płaci czytanie.
Strona bierze ją taką, jaka przyszła, i pisze wokół niej swoje:
zwój o tym, czym kolejność czytań jest, a czym nie.

Klucze odpowiedzi wybiera ten projekt, więc są po polsku.
Nazwa roli w odczytaniu jest po polsku,
bo jest nazwą symbolu gramatyki,
którą podaje `DEKLARACJA` w `olski/subset/deklaracja.py`.
Rolami są na przykład `podmiot`, `dopełnienie`, `orzeczenie` i `wyrażenie_przyimkowe`.
Po angielsku zostaje status w znaczku,
a legenda pod polem tłumaczy każdy status na polskie zdanie.
Statusów jest pięć: `valid`, `ambiguous`, `rejected`, `unclosed` i `fragment`.
Znaczek jest wyborem strony, a nie drugim wydrukiem komendy:
komenda statusu nie drukuje, bo dzieli on zdania po liczbie odczytań,
a nie po tym, czy narzędzie ma o zdaniu co powiedzieć
(`Verdict.status` w `olski/werdykt.py`).
Cenę przekładu statusu trzyma wpis o statusie werdyktu
w `todo/dokumenty.md`.

## API oddaje dane, a nie HTML

Strona jest klientem API, a nie jego wnętrzem.
Serwer oddaje JSON, więc odpowiada tak samo curlowi i przeglądarce.
Strona wybiera, co z tych danych pokaże.
Zdanie jednoznaczne dostaje swoje jedno czytanie rozwinięte.
Zdanie o kilku streszczeniach dostaje zwinięty spis pod podpisem.
Milczenia komendy strona przy tym nie powtarza.
Kto wkleił jedno zdanie, przyszedł po odpowiedź o tym zdaniu.
Komendę nad katalogiem puszcza się po znaleziska
([README](../README.md#co-działa)).

Odrzuciliśmy oddawanie fragmentów HTML, czyli to, co robi się dziś htmxem.
Powód jest ten sam, który stoi nad frazą werdyktu.
Serwer, który składa HTML, byłby drugą warstwą prezentacji.
Podpisy przy werdykcie mają wtedy dwóch właścicieli: serwer i stronę.
Nie widać wtedy, czyj podpis obowiązuje.
Przeładowanie całej strony odrzucamy z powodu prostszego.
Gubi ono tekst w polu.
Zostawia też API zamknięte dla wszystkiego poza tą jedną stroną.

Każde zdanie ma przycisk, który kopiuje jego werdykt do schowka.
Blok na stronie czyta się okiem,
a do zgłoszenia albo do rejestru otwartej roboty wkleja się tekst.
Tekst ten składa strona, a nie serwer.
Powód jest ten sam: pole z gotowym tekstem w odpowiedzi byłoby drugą warstwą prezentacji.
Schowek wymaga kontekstu bezpiecznego, czyli HTTPS albo localhosta.
Gdzie przeglądarka go nie daje, przycisku nie ma,
bo przycisk, który zawsze odmawia, jest gorszy niż jego brak.

Stronę i API oddaje przy tym jeden kontener.
Z osobnego adresu strona żądałaby nagłówków CORS,
drugiego wdrożenia i drugiego rachunku.
Strona z trzech plików tego nie potrzebuje.

## Ramy nie ma, bo warstwa HTTP jest tablicą tras

Cała warstwa HTTP to tablica tras w `witryna/serwer.py`,
jeden typ odpowiedzi i jeden wyjątek na odmowę.
Rama kupuje routing, walidację i serializację.
Ramą byłby tu Flask albo FastAPI.
Tutaj routing jest słownikiem o kilku wpisach.
Walidacja pyta, czy przyszedł napis i czy nie jest dłuższy niż granica.
Serializacją jest `json.dumps`.
Zależność wykonawcza jest za to jedna i nietrywialna: gunicorn.
Mówienie po HTTP wprost do internetu jest robotą, której nikt nie pisze ręką.
Biblioteka wchodzi zatem tam, gdzie robota jest trudna,
a rozdanie kilku tras nie jest trudne.

Odwraca to piąty rodzaj żądania:
logowanie, wysyłka pliku, granica na adres albo strumień.
Wtedy rama wchodzi, a wymiana jest lokalna.
Aplikacja WSGI jest po obu stronach tym samym interfejsem,
więc strona nie zauważy wymiany.

Z tego samego powodu strona nie ma ramy ani kroku budowania.
Stanem strony są jedno pole tekstowe i lista wyników.
React kupowałby diffowanie widoku, którego nie ma co diffować,
a płaciłby npm w blokach checków oraz paczką,
która waży więcej niż wszystko, co ta strona wysyła.
Trzy pliki jadą tak, jak stoją w repozytorium.
Odwraca to stan po stronie przeglądarki: historia, cofanie albo kilka widoków.
Wtedy biblioteka wchodzi.

Cena tej decyzji jest jedna i suita jej nie łapie: `witryna/skrypt.js` nie ma testu.
W blokach checków nie ma Node.js.
Wpis o tym pliku trzyma `todo/pakiet.md`.
Robocza odpowiedź jest taka: skrypt rysuje dane i nie liczy niczego,
więc niemal każda usterka siedzi po stronie Pythona.
Wyjątkiem jest tekst dla schowka, bo składa go sama strona.
Suita pyta o niego jedno: czy strona woła te adresy, które ma serwer.

## Co witryna pokazuje

| trasa | metoda | co daje |
| --- | --- | --- |
| `/` | GET | strona, czyli `witryna/strona.html` wraz ze stylem i skryptem |
| `/werdykt` | POST | werdykt o każdym zdaniu tekstu wraz z podsumowaniem całości |
| `/makieta` | GET | tekst do makiety z drugiego toru, wraz z ziarnem |

Werdykt niesie to, co z flagami drukuje komenda —
wyjaśnienie, czytania, dalsze zatrzymania, morfologię form
oraz to, co zgaduje warstwa rozstrzygająca —
a obok tego status, po którym strona rysuje znaczek.
Domysł tej warstwy nie jest werdyktem
([architecture.md](architecture.md#warstwa-rozstrzygająca-wydaje-zawężenie-z-powodem-a-nie-znaczenie)),
więc dostaje na stronie znak zapytania i osobny podpis.

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
   "wyjaśnienie": "jedno odczytanie",
   "czytania": [
    [
     {
      "dopełnienie": "plik konfiguracyjny",
      "orzeczenie": "Zapisz"
     }
    ]
   ],
   "koszty": [
    [
     {
      "pozycja": "opuszczony podmiot",
      "ile": 1,
      "koszt": 200
     }
    ]
   ],
   "liczba_czytań": 1,
   "urwane": false,
   "rozbieżne": [],
   "dalsze_zatrzymania": [],
   "morfologia": [
    [
     {
      "forma": "plik",
      "odczytania": [
       "plik subst:sg:nom.acc:m3"
      ]
     },
     {
      "forma": "konfiguracyjny",
      "odczytania": [
       "konfiguracyjny adj:sg:acc:m3:pos"
      ]
     }
    ]
   ],
   "odniesienia": [],
   "domysły": []
  }
 ],
 "podsumowanie": {
  "zdań": 1,
  "wieloznaczne": 0,
  "naprawialne": 0,
  "bez_odczytania": 0,
  "fragmentów": 0,
  "niejasnych_odniesień": 0,
  "wyjaśnienie": "zdań: 1; wieloznaczne: 0; bez odczytania: 0"
 },
 "granica_znaków": 4000
}
```

Lista pod kluczem `czytania` niesie różne streszczenia.
Każde streszczenie stoi tam raz (`Verdict.readings` w `olski/werdykt.py`).
Pole `liczba_czytań` wychodzi z lasu i mówi, ile czytań zdanie ma.
Lista i liczba nie wynikają z siebie nawzajem.
O granicy wyliczania z `MAX_READINGS` w `olski/parse/las.py`
mówi więc osobne pole `urwane`, a strona wpisuje je do podpisu zwoju.
Samo streszczenie jest listą po jednym wpisie na zdanie składowe,
bo każde składowe obsadza role własnym materiałem.
Pod `odniesienia` idą zaimki, które wskazują na dwie rzeczy naraz,
wraz z formami tych rzeczy (`olski/odniesienia.py`).
Klucz ten mówi o zdaniu obok, a nie o tym zdaniu, i dlatego stoi poza werdyktem.
Strona dopisuje go pod wyjaśnieniem, a nie pod zwojem,
bo jest on znaleziskiem tak samo jak wyjaśnienie.
Pod `rozbieżne` idą konstytuenty, których wieloznaczności ta lista nie nazywa,
wraz ze streszczeniami ich kształtów.
Strona daje każdemu konstytuentowi własny spis pod tym samym zwojem.
Pod `morfologia` idzie wpis na każde streszczenie z `czytania`.
W nim stoją formy wraz z odczytaniami, które dopuszcza to odczytanie zdania.
`lubi` pod orzeczeniem ma tam samo `lubić`, a nie wszystko, co Morfeusz w tej formie czyta.
`Verdict.morfologia` w `olski/werdykt.py` mówi, po co jest ta odpowiedź.
Zdanie bez odczytania dostaje pod tym kluczem jeden wpis.
Wpis ten wylicza wszystko, co olski czyta w formach,
bo odsiewa je dopiero odczytanie zdania.
Komenda żąda na to flagi, a odpowiedź niesie to zawsze.
Strona zwija to do podpisu i rozwija jednym kliknięciem,
czego wydruk w terminalu nie umie.
Pod `koszty` idzie wpis na każde streszczenie z `czytania`,
a w nim pozycje cennika, którymi to czytanie płaci,
każda wraz z liczbą wystąpień i tym, ile te wystąpienia kosztują.
Liczy tę cenę serwer, bo cennik jest w `olski/cennik.py`,
a strona licząca ją sama miałaby drugą kopię tabeli cen.
Sumy na czytanie odpowiedź nie podaje, bo kolejność czytań rozstrzyga koszt
czytany od góry drzewa, a nie suma rachunku
([disambiguation.md](disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie)),
więc suma czytałaby się na miejsce w kolejce, którym nie jest.
Granicę znaków oddaje sama odpowiedź, bo licznik pod polem liczy przy niej.
Granica wpisana w skrypcie byłaby drugą kopią liczby z serwera.

```sh
curl -s 'localhost:8000/makieta?ziarno=1871&akapity=1'
```

```json
{
 "ziarno": 1871,
 "akapitów": 1,
 "tekst": "Czeladnik zapłakał w wąskiej piwnicy. Dziewczyna zgubiła glinianą skrzynię, ponieważ czeladnik zszedł. Zdążyła mieszkać przed ciężkim młynem. Córka dała dziewczynie koszyk. Zdążyła wrócić od młodej wdowy. Czeladnik zważył kufry gospodarza i sukno."
}
```

Bloki te odtwarza `tests/test_witryna.py`.
Puszcza on polecenie nad blokiem i porównuje odpowiedź z blokiem pod nim.
Blok wklejony ręką rozjeżdża się po cichu z każdą zmianą w werdykcie.

Sond witryna nie wystawia.
Pomiar czyta bank drzew albo korpus audytowy,
czyli archiwa dziesiątek megabajtów, których w kontenerze nie ma
([corpus.md](corpus.md#fetching-it)).
Ekstrakcja przyjmuje katalog Markdownu, a nie wklejone zdanie.
Kto mierzy, ma klon i `harness`.

## Granice są granicami kontenera

Tekst wchodzi przycięty do kilku tysięcy znaków.
Granicę trzyma `NAJWIĘCEJ_ZNAKÓW` w `witryna/serwer.py`.
Kontener liczy jednym procesem na żądanie.
Wklejony cudzy korpus zająłby ten proces na minuty,
a strona przestałaby odpowiadać komukolwiek innemu.
Najgorsze zdania, jakie umiem napisać, idą przy tej długości pod sekundę.
Worker ginie po granicy z `--timeout` w `Procfile`.
Granica ta stoi rząd wielkości nad tym pomiarem i kilka razy pod granicą routera.
Zabity worker wstaje z powrotem,
więc żądanie zapętlone kosztuje jedno żądanie, a nie stronę milczącą do restartu.
Żądanie dłuższe odpada na `Content-Length`, czyli przed dekodowaniem.
Żądanie bez tego nagłówka odpada również,
bo czytanie z gniazda bez granicy jest tym, co zabija kontener.

Uwierzytelnienia nie ma i nie ma granicy na adres,
więc witryna pod adresem publicznym jest otwarta dla wszystkich.
Jest to decyzja, a nie przeoczenie.
Witryna liczy z wejścia, którego nie zapisuje,
więc ktoś obcy może najwyżej zająć kontener na sekundę.
Zmieni się to dopiero przy koszcie widocznym na rachunku.

## Ile to bierze pamięci

Proces z wczytanym słownikiem bierze ponad sto megabajtów.
Każdy następny worker dodaje do tego kilka megabajtów, a nie drugą setkę.
Słownik Morfeusza wchodzi z pliku i jego strony są wspólne.
Gramatykę buduje `--preload` raz, w procesie nadrzędnym.
Cała witryna mieści się zatem w kontenerze S, czyli w 256 megabajtach.
Dla tej wielkości ją napisano.

Workery są dwa, a powodem nie jest przepustowość.
Przy jednym workerze sekundowy rozbiór wstrzymuje żądanie o styl i o skrypt,
więc strona z pustym polem tekstowym czekałaby na cudze zdanie.

Liczby te daje przebieg, bo rusza je wydanie Morfeusza i rozmiar gramatyki.
Uruchom `Procfile` lokalnie, zawołaj `/werdykt`
i przeczytaj `Pss` z `/proc/<pid>/smaps_rollup`
dla procesu nadrzędnego i każdego workera.
Morfeusz wczytuje słownik dopiero przy pierwszej analizie.
Trzeba więc zawołać słownik żądaniem,
a pomiar zrobiony przed pierwszym żądaniem mówi o połowie tej pamięci.

## Wdrożenie

Witryna stoi pod [olski.pl](https://olski.pl).
Dokumentacja stoi pod osobnym adresem i jedzie osobną drogą, z GitHub Pages
([publikacja.md](publikacja.md)).

Platforma czyta z repozytorium trzy pliki.
`requirements.txt` mówi jej, że to jest aplikacja Pythona.
W środku ma jeden wiersz `.[witryna]`, czyli wskazanie na `pyproject.toml`.
Właścicielem zależności zostaje `pyproject.toml`, a nie ten plik.
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
bo gramatyka czyta słownik przy imporcie.

## Nie zapadło

Czy kontener S wystarcza pod obciążeniem, nie zostało zmierzone:
liczby z sekcji o pamięci wychodzą z przebiegu na pustej witrynie,
a nie z witryny, do której ktoś naraz wkleja tekst.

Strona pod adresem publicznym jest zaproszeniem dla czytelnika spoza projektu.
[roles.md](roles.md#rola-jest-postawą-nie-osobą) mówi,
że tutaj każdą rolę obsadza jedna osoba.
Warto pilnować tego stanu.
Witryna sama tego nie łamie, bo obsługuje tę samą osobę w przeglądarce.

## Sources

- <https://doc.scalingo.com/languages/python/start> — po czym buildpack poznaje aplikację Pythona i skąd bierze wersję
- <https://doc.scalingo.com/platform/internals/container-sizes> — wielkości kontenerów wraz z pamięcią
- <https://doc.scalingo.com/platform/internals/routing> — granice routera, w tym czas na pierwszą odpowiedź
- <https://pypi.org/project/morfeusz2/> — wydania Morfeusza wraz z wariantami wheela
- <https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText> — czego pisanie do schowka żąda od strony
