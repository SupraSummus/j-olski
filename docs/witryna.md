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

## Strona zaczyna od tego, czym olski jest

Strona pod adresem publicznym dostaje czytelnika, który o projekcie nie słyszał
([roles.md](roles.md#ktoś-kto-trafia-tu-pierwszy-raz)),
więc pierwsze akapity mówią, co parser robi i co znaczy jedno odczytanie,
a pole tekstowe jest dopiero pod nimi.
Żart o spiłowanym `p` jest w tym układzie podpisem pod wprowadzeniem:
tłumaczy nazwę, a przeczytany pierwszy nie tłumaczy niczego.

Wprowadzenie streszcza [README](../README.md) i mówi mniej dokładnie niż tamten plik.
Ani liczb, ani wywodu strona nie powtarza, a odsyła do repozytorium,
więc zmiana w README nie zostawia tutaj kopii nieaktualnej
([CLAUDE.md](../CLAUDE.md#one-owner-per-fact-repeat-narrative-freely)).
Wyjaśnienie dłuższe niż dwa zdania wchodzi zwinięte,
bo czytelnik przyszedł sprawdzić własne zdanie,
a nie przeczytać akapit o wieloznaczności.

Lista zastosowań mówi, co dałoby się z parsera zbudować,
i mówi w zdaniu nad sobą, że nikt z tego niczego nie zbudował.
Bez tego zdania czyta się ona jak spis funkcji, których strona nie ma.
Właścicielem listy jest strona, bo na to pytanie nie odpowiada żaden dokument:
[roadmap.md](roadmap.md#cele) wylicza cele, czyli to, czym sprawdzimy narzędzie,
a nie to, co ktoś mógłby z niego złożyć.

Oba tory pokazują się przy wejściu same: strona woła werdykt i makietę,
zanim ktokolwiek naciśnie przycisk.
Sekcja pusta do pierwszego kliknięcia nie mówi, co jest pod przyciskiem,
a dwa żądania naraz obsługują różne workery
([niżej](#ile-to-bierze-pamięci)).

## Werdykt idzie w tych słowach, w których drukuje go `olski-check`

Frazę werdyktu ma na własność kod: `Verdict.explain` w `olski/werdykt.py`.
Witryna jej nie tłumaczy i drugiej nie pisze,
więc przez API idzie `jedno odczytanie`
oraz `brak odczytania: analiza staje na „i”`,
czyli to samo zdanie, które drukuje komenda.

Fraza polska napisana na stronie byłaby drugą kopią,
a druga kopia rozjeżdża się po cichu:
zmiana w `explain` zostawiłaby na stronie zdanie,
którego olski już o żadnym zdaniu nie mówi,
i nie zgłosiłby tego żaden check.
Werdykt należy przez to do kodu,
a podpisy, przyciski, legenda statusów i nagłówki sekcji do strony.
Wiersz o dalszym zatrzymaniu składają dwa miejsca w tym samym brzmieniu —
komenda w `olski/check.py`, strona w `witryna/skrypt.js` —
bo API oddaje pod tym kluczem same formy, a nie zdanie o nich.
Tak samo składa się wiersz morfologii, i z tego samego powodu:
pod tym kluczem idzie forma wraz ze swoimi odczytaniami,
a nie gotowy wiersz o niej.

Klucze JSON-a wybieramy sami, więc są po polsku,
i po polsku jest też nazwa roli w odczytaniu —
`podmiot`, `dopełnienie`, `orzeczenie`, `wyrażenie_przyimkowe` —
bo jest nazwą symbolu gramatyki, którą podaje `DEKLARACJA` w `olski/subset/deklaracja.py`.
Po angielsku zostaje status w znaczku —
`valid`, `ambiguous`, `rejected`, `unclosed`, `fragment` —
i legenda pod polem tłumaczy każdy z nich na polskie zdanie.
Co kosztuje przekład statusu, trzyma [`todo/`](../todo/README.md).

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
a do zgłoszenia albo do `todo/` wkleja się tekst.
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
Trzyma to `todo/`, a robocza odpowiedź jest taka,
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
status, wyjaśnienie, czytania, dalsze zatrzymania, morfologię form
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
   "wyjaśnienie": "jedno odczytanie",
   "czytania": [
    [
     {
      "dopełnienie": "plik konfiguracyjny",
      "orzeczenie": "Zapisz"
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
   "domysły": []
  }
 ],
 "podsumowanie": {
  "olskie": 1,
  "zdań": 1,
  "z_czytaniem": 1,
  "fragmentów": 0,
  "wyjaśnienie": "olskie: 1 z 1 zdania; z odczytaniem: 1"
 },
 "granica_znaków": 4000
}
```

Lista pod kluczem `czytania` niesie streszczenia różne, każde raz
(`Verdict.readings` w `olski/werdykt.py`),
a `liczba_czytań` wychodzi z lasu i mówi, ile czytań zdanie ma.
Jedna z drugiej się przez to nie wylicza,
więc o granicy wyliczania z `MAX_READINGS` w `olski/parse.py`
mówi osobne pole `urwane`, a strona wpisuje je do podpisu zwoju.
Samo streszczenie jest listą po jednym wpisie na zdanie składowe,
bo każde składowe obsadza role własnym materiałem.
Pod `rozbieżne` idą konstytuenty, których wieloznaczność ta lista zostawia
nienazwaną, wraz ze streszczeniami ich kształtów,
a strona daje każdemu z nich własny spis pod tym samym zwojem.
Pod `morfologia` idzie wpis na każde streszczenie z `czytania`,
a w nim formy wraz z odczytaniami, którymi w tym odczytaniu zdania stać mogą:
`lubi` pod orzeczeniem ma tam samo `lubić`, a nie wszystko, co Morfeusz w tej
formie czyta (`Verdict.morfologia` w `olski/werdykt.py` mówi, po co ta odpowiedź jest).
Zdanie bez odczytania dostaje pod tym kluczem jeden wpis
i mówi w nim, co olski w formach czyta, bo odsiać tego nie ma czym.
Komenda żąda na to flagi, a odpowiedź niesie to zawsze,
bo strona zwija to do podpisu i rozwija jednym kliknięciem,
czego wydruk w terminalu nie umie.
Granicę znaków oddaje sama odpowiedź, bo licznik pod polem liczy przy niej,
a wpisana w skrypcie byłaby drugą kopią liczby z serwera.

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
