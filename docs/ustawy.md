# Ustawy

Ustawa opisuje mechanikę państwa,
a pisze się ją pod regułami, które same są prawem:
„Zasady techniki prawodawczej” żądają od zdania w ustawie
w przybliżeniu tego, czego olski żąda od zdania w dokumentacji.
Rejestr, który to żądanie stawia sam sobie,
warto zmierzyć nawet wtedy, gdy olski pod niego nie powstał:
pomiar mówi wtedy coś o gramatyce, a nie tylko o rejestrze.

Mówi to, że regularność ustawy nie stoi w zdaniu.
Nad siedmioma ustawami gramatyka wyprowadza jednoznacznie 63 zdania z 4921,
czyli 1,3%, a nad [Składnicą](corpus.md#the-measurement) wyprowadza 2,4%,
choć tamten bank drzew jest zbudowany z gazet i prozy.
Wieloznacznych jest tu 4,1% wobec 0,9% tam,
więc zdanie ustawy, które olski w ogóle czyta,
czyta on najczęściej na kilka sposobów.
Regularne w ustawie jest drzewo jednostek redakcyjnych,
a zdanie jest w niej długie i podrzędnie złożone,
czyli takie, jakiego olski nie ma.

## Rejestr ma własne reguły, a te reguły nie mają miary

„Zasady techniki prawodawczej” są załącznikiem do rozporządzenia
Prezesa Rady Ministrów z dnia 20 czerwca 2002 r.,
więc nie są poradnikiem, tylko obowiązują.
Trzy przepisy z nich mówią o tym samym, o czym jest to repozytorium:

- § 5: „Przepisy ustawy redaguje się zwięźle i syntetycznie,
  unikając nadmiernej szczegółowości […]”
- § 6: „Przepisy ustawy redaguje się tak, aby dokładnie i w sposób zrozumiały
  dla adresatów zawartych w nich norm wyrażały intencje prawodawcy.”
- § 7: „Zdania w ustawie redaguje się zgodnie z powszechnie przyjętymi regułami
  składni języka polskiego, unikając zdań wielokrotnie złożonych.”

§ 7 jest żądaniem podzbioru postawionym przez wykluczenie,
czyli tak, jak [wyznaczał go linter](linter.md#this-is-the-same-subset-approached-from-behind):
składnia polska wolna, a jedna konstrukcja zabroniona.
§ 6 jest kryterium jednoznaczności:
zrozumiały dla adresata jest przepis, który czyta się jednym sposobem,
i to samo mówi olski, gdy każe zdaniu mieć dokładnie jedno czytanie.
§ 55 ust. 2 żąda przy tym, żeby artykuł był w miarę możliwości jednozdaniowy,
czyli żeby jednostce redakcyjnej wystarczyło jedno zdanie.

Korekta żadnego z tych trzech nie mierzy.
Wielokrotne złożenie zdania jest własnością zdania, a nie znakiem w nim,
a jednoznaczność jest własnością wyprowadzenia,
więc spór o nią rozstrzyga sąd, czyli po uchwaleniu i po jednej sprawie naraz.
Inwentarz kandydatów na reguły tego rejestru nie obejmuje,
tak samo jak nie obejmuje prozy literackiej,
a to, co dla tego rejestru dałoby się mierzyć, zostaje niżej.

## Skąd bierze się korpus

API ELI Sejmu oddaje tekst aktu w HTML-u pod adresem ELI,
czyli pod rocznikiem i pozycją Dziennika Ustaw:

```sh
mkdir -p ustawy
for eli in 1990/95 1999/688 2001/1198 2011/112 2014/1195 2015/1485 2024/1907; do
  curl -sS -o "ustawy/DU-$(echo "$eli" | tr / -).html" \
    "https://api.sejm.gov.pl/eli/acts/DU/$eli/text.html"
done
```

Korpus mówi o sobie [pięć rzeczy](corpora.md#what-a-corpus-has-to-say-about-itself),
a akt normatywny odpowiada na każdą z nich,
i na licencję, rejestr oraz etap produkcji odpowiada tak,
jak żaden korpus tamtego przeglądu odpowiedzieć nie mógł.

**Licencja.** Żadna, w najlepszym sensie:
art. 4 pkt 1 ustawy o prawie autorskim i prawach pokrewnych
wyłącza akty normatywne z przedmiotu prawa autorskiego,
więc nie ma czego redystrybuować ani na co się zgadzać.

**Rozmiar.** Siedem ustaw wyżej to 104 062 słowa i 4921 zdań,
co starcza na czytanie trafień, a nie na rozkład.
Rozkład jest tu jednak kwestią pobrania, a nie dostępności:

```sh
curl -sS "https://api.sejm.gov.pl/eli/acts/DU/2024" | grep -o '"type":"Ustawa"' | wc -l
```

Rocznik 2024 ma 115 ustaw i API oddaje w HTML-u każdą z nich.

**Rejestr.** Jeden i zadeklarowany:
tekst pisany pod „Zasadami techniki prawodawczej”, a nie pod niczyim gustem.

**Pochodzenie.** Polszczyzna napisana po polsku,
z jednym zastrzeżeniem, którego ten pomiar nie sprawdzał:
dyrektywa transponowana jest tłumaczeniem,
a ustawa, która ją wdraża, może nieść jego składnię.
Ustawy wyżej stoją od 1990 do 2024 roku, więc rocznik nie jest tu zmienną ukrytą.

**Etap produkcji.** Trzeci, którego tamten przegląd nie ma:
tekst po redakcji i po korekcie, ogłoszony,
i przy tym nietknięty od ogłoszenia, bo zmienia go dopiero nowelizacja z własną pozycją.
Adres ELI jest przez to mocniejszym przypięciem niż commit:
akt pod nim nie może się już zmienić.
Zmienić się może HTML, w którym wydawca go podaje,
i to jest jedyne, co pod tym pomiarem może się ruszyć bez naszego udziału.

Adresy wyżej wskazują ustawy w brzmieniu ogłoszonym, a nie ujednoliconym,
bo tekst jednolity jest załącznikiem do obwieszczenia
i jego HTML niesie obwieszczenie razem z aktem.
Ustawa o samorządzie gminnym stoi tu więc taka, jaka była w 1990 roku,
i o taką, jaka jest dzisiaj, ten pomiar nie pyta.

Osobno stoją same „Zasady techniki prawodawczej”,
bo są rozporządzeniem, a nie ustawą, i o nich jest ten dokument w drugą stronę:

```sh
mkdir -p ztp
curl -sS -o ztp/DU-2016-283.html "https://api.sejm.gov.pl/eli/acts/DU/2016/283/text.html"
```

Jest to tekst jednolity z 2016 roku, czyli ostatni, który API oddaje w HTML-u;
nowszy jest ogłoszony w PDF-ie i tej ekstrakcji nie dotyczy.

## Ustawa dochodzi do gramatyki jako drzewo, nie jako tekst

Tekst jednostki redakcyjnej najczęściej nie jest zdaniem:

```text
Art. 1. Ustawa określa:
  1) zadania ochrony ludności i obrony cywilnej;
  2) organy i podmioty realizujące zadania ochrony ludności i obrony cywilnej;
```

Zdaniem jest gałąź: przesłanka złożona z każdą pozycją po kolei.
Więc `harness/ustawy.py` składa drzewo w zdania,
a nie przepisuje tekst jednostka po jednostce,
i wyliczenie o siedmiu pozycjach daje siedem zdań.
Zszywa tylko punkt i literę, bo tylko wyliczenie dzieli przesłankę między pozycje;
artykuł i ustęp stoją same.

```sh
python3 -m harness.ustawy ustawy/ --into proza/ustawy
python3 -m harness.ustawy ztp/ --into proza/ztp
```

Ten krok zmyśla trzy rzeczy, dwie zabiera,
a jedną zabrał wydawca przed nim,
i tyle razem kosztuje czytanie ustawy zdaniami.

**Zdanie, którego nikt nie napisał.**
`Ustawa określa zadania ochrony ludności i obrony cywilnej.`
stoi w ustawie w dwóch jednostkach i pod dwoma numerami.
Werdykt gramatyki dotyczy tego złożenia, a nie zapisu,
i jest to jedyna forma, w której treść ustawy jest zdaniami w ogóle.

**Przesłanka powielona.**
Wychodzi raz na pozycję, więc częstość liczona nad tą prozą liczyłaby ją wielokrotnie.
Dlatego korpus idzie pod gramatykę, która pyta o zdanie po zdaniu.

**Kropka dopisana.**
Gałąź kończy się średnikiem albo przecinkiem, a zdanie kropką.
Bez niej werdykt brzmiałby „to nie zdanie”
nad każdą pozycją każdego wyliczenia i nie mówiłby nic o polszczyźnie.

**Tekst ustawy zmienianej odjęty.**
Rozdział o zmianach w przepisach obowiązujących cytuje cudze przepisy,
a te są tekstem innej ustawy i odpadają.
Zostaje po nich przesłanka, która czyta się jak całe zdanie:
`W ustawie z dnia 14 czerwca 1960 r. - Kodeks postępowania administracyjnego
art. 221 otrzymuje brzmienie.`
Zdanie tego kształtu jest w tym korpusie odrzucone i nie jest to werdykt o polszczyźnie.

**Biały znak znormalizowany.**
Wcięcia HTML-a idą do jednej spacji,
więc odstęp podwojony i odstęp przed znakiem przestankowym
nad tą prozą nie stoją nigdzie.
To zero jest zerem ekstrakcji, nie rejestru.

**Myślnik, którego HTML nie ma.**
Ustawa ogłoszona w PDF-ie ma w nazwie kodeksu półpauzę
(`ustawa z dnia 14 czerwca 1960 r. – Kodeks postępowania administracyjnego`),
a HTML tego samego aktu ma tam dywiz i półpauzy nie ma nigdzie.
Kto liczy pauzy nad tym HTML-em, mierzy więc wydawcę, a nie prawodawcę,
i jest to ta sama usterka korpusu, którą przegląd korpusów zgłasza
[warstwie tekstowej NKJP](corpora.md#its-text-layer-has-been-character-normalized).

## Co gramatyka z tego wyprowadza

```sh
python3 -m olski.check proza/ustawy/DU-1990-95.txt
python3 -m olski.check proza/ustawy/*.txt | grep -oE ': (valid|ambiguous|rejected|fragment) ' \
  | sort | uniq -c
```

| akt | zdań | jednoznacznych | wieloznacznych | odrzuconych |
| --- | --- | --- | --- | --- |
| samorząd gminny (1990/95) | 386 | 17 | 32 | 337 |
| inicjatywa ustawodawcza (1999/688) | 84 | 0 | 0 | 84 |
| informacja publiczna (2001/1198) | 126 | 0 | 1 | 125 |
| Kodeks wyborczy (2011/112) | 2908 | 25 | 81 | 2802 |
| petycje (2014/1195) | 48 | 3 | 2 | 43 |
| zgromadzenia (2015/1485) | 127 | 0 | 1 | 126 |
| ochrona ludności (2024/1907) | 1242 | 18 | 85 | 1139 |
| razem | 4921 | 63 | 202 | 4656 |

Same „Zasady techniki prawodawczej” stoją poza tą sumą, bo są rozporządzeniem:
699 zdań, z tego 4 jednoznaczne i 14 wieloznacznych.
Werdyktu „to nie zdanie” nie ma nigdzie ani razu, bo kropkę stawia ekstrakcja.

Zdania wyprowadzone jednoznacznie mają jeden kształt,
i jest to kształt, dla którego olski powstał.
Cztery z ustaw i dwa z „Zasad techniki prawodawczej”:

```text
Gmina posiada osobowość prawną.
Mieszkańcy gminy tworzą z mocy prawa wspólnotę samorządową.
Działalność sołtysa wspomaga rada sołecka.
Budżet oraz wysokość składek uchwala sejmik.
Ustawa zawiera przepisy merytoryczne.
Artykuł powinien być w miarę możliwości jednozdaniowy.
```

Dwa ostatnie są przepisami „Zasad techniki prawodawczej”:
zdanie, które żąda od artykułu jednozdaniowości, jest jednym zdaniem olskiego,
a definicja części ustawy z § 14 ust. 1 przechodzi przez ekstrakcję i przez gramatykę naraz.

Średnie zdanie ma tu 21 słów (104 062 na 4921),
a pokrycie gramatyki [urywa się nad dziesięcioma](corpus.md#the-measurement),
więc 1,3% jest z tej długości, a nie z rejestru.
Nad README ta sama gramatyka wyprowadza garść zdań
i [tamten przebieg](corpus.md#where-the-analyses-stop) trzyma ich liczbę,
więc różnica między jednym pomiarem a drugim
jest różnicą długości zdania, a nie staranności piszącego.

## Wieloznaczność jest tu odczytem z § 6, ale nie jest zarzutem

Wieloznacznych jest 202, czyli 76% zdań, którym olski daje jakiekolwiek czytanie,
a nad Składnicą jest to 27% (115 wieloznacznych na 430 przeczytanych).
Różnią się najczęściej podmiotem i dopełnieniem,
bo za nimi stoi jedna rzecz: przyłączenie wyrażenia przyimkowego,
którego [olski nie wybiera](subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).
Najdłuższe urywają się na 64 czytaniach, czyli na `MAX_READINGS` z `olski/parse.py`.

Kształt tej wieloznaczności widać najkrócej nad zdaniami,
których w tym korpusie nie ma:
Konstytucja jest w API tylko w PDF-ie, więc ta ekstrakcja jej nie czyta,
a jej artykuły są dla tego rejestru krótkie i pisane wprost.

```sh
python3 -m olski.check -c "Władza zwierzchnia w Rzeczypospolitej Polskiej należy do Narodu."
python3 -m olski.check -c "Sejm sprawuje kontrolę nad działalnością Rady Ministrów."
```

```text
<text>: ambiguous Władza zwierzchnia w Rzeczypospolitej Polskiej należy do Narodu.
                  4 readings, differing in Subject
<text>: ambiguous Sejm sprawuje kontrolę nad działalnością Rady Ministrów.
                  2 readings, differing in Object
```

Drugie z tych zdań pokazuje, dlaczego 202 nie jest liczbą przepisów niejednoznacznych:
oba jego czytania mówią, że Sejm kontroluje działalność Rady Ministrów,
i różnią się drzewem, a nie normą.
202 jest liczbą przepisów, w których jednoznaczność bierze się z wiedzy o świecie,
a nie ze składni,
i to jest wszystko, co pomiar tej wielkości mówi:
[wieloznaczność mierzy pewność](glr-in-practice.md#ambiguity-as-a-confidence-measure),
a nie poprawność.

Pozostałe mają w tym rejestrze wagę, której nie mają w dokumentacji.
Spór o to, do czego w przepisie dochodzi wyrażenie przyimkowe,
jest sporem o to, kogo przepis dotyczy,
i rozstrzyga go sąd, a nie autor.
Narzędzie, które autorowi pokazuje oba czytania przed uchwaleniem,
odpowiada więc na pytanie, które inaczej zadaje się dopiero w sporze,
i to jest jedyne miejsce w tym repozytorium,
gdzie werdykt „wieloznaczne” ma adresata poza autorem tekstu.

## Gdzie stają analizy w tym rejestrze

```sh
python3 -m olski.check proza/ustawy/*.txt | grep -oP '(?<=„)[^”]+(?=”)' \
  | sort | uniq -c | sort -rn | head -20
```

Z 4656 odrzuceń 3799 stanęło na formie, której żadna produkcja nie bierze,
a 857 na samej strukturze.
Formy z czoła tego rankingu grupują się w cztery klasy:

| klasa | najczęstsze formy |
| --- | --- |
| aparat odsyłaczowy | `art` 717, dywiz 666, `§` 595, `r` 254, nawiasy 232 i 223, liczby |
| przysłówki | `odpowiednio` 175, `niezwłocznie` 162, `także` 116, `również` 95 |
| spójniki podrzędne | `Jeżeli` 171 i `jeżeli` 154, `że` 83, `gdy` 49 |
| imiesłowy i odsłowniki | `obejmujący` 100, `wykonywania` 88, `wniesienia` 61 |

Pierwsza klasa zajmuje dziewięć pierwszych miejsc rankingu,
i jest to jedna konstrukcja, a nie dziewięć:
odsyłacz `art. 96 ust. 1 pkt 1` w środku zdania,
dywiz z nazwy kodeksu i nawias wokół adresu publikacji.

Kolejka wychodzi więc inna niż ta,
którą [Składnica ustawiła](corpus.md#where-the-analyses-stop),
i różnica jest informacją o rejestrze.
Czas przeszły stoi tam na pierwszym miejscu z 2891 zdaniami,
a tutaj cały daje 64 trafienia (`był`, `była`, `było`, `były`, `został`, `została`)
i do dwudziestu pierwszych miejsc nie wchodzi:
ustawa mówi w czasie teraźniejszym o tym, co ma być,
a przeszły zostaje jej na przepisy przechodnie.
Najtańszy duży zakup z tamtej kolejki jest tu więc wart prawie zera.
Zamiast niego stoi wysoko zdanie warunkowe,
czyli kształt, w którym norma jest w ogóle zapisana:
`Jeżeli` z 325 trafieniami na dwie pisownie jest tu tym, czym `był` jest tam.

## Rejestr znalazł dziurę w grupie imiennej

```sh
python3 -m olski.check -c "Rzeczpospolita Polska jest dobrem wspólnym wszystkich obywateli."
python3 -m olski.check -c "Rzeczpospolita Polska jest wspólnym dobrem wszystkich obywateli."
```

Pierwsze zdanie nie ma wyprowadzenia, drugie ma jedno.
`NPConjunct` bierze rzeczownik z przymiotnikiem po nim,
bierze rzeczownik z dopełniaczem po nim,
bierze rzeczownik z przymiotnikiem i wyrażeniem przyimkowym,
bierze rzeczownik z dopełniaczem i wyrażeniem przyimkowym,
a rzeczownika z przymiotnikiem i dopełniaczem nie bierze.
Rejestr trafia w tę dziurę stale,
bo nazywa terminy rzeczownikiem z przymiotnikiem za nim
(`obrona cywilna`, `informacja publiczna`, `władza zwierzchnia`, `dobro wspólne`),
a terminowi dokłada dopełniacz.
Wpis stoi w [TODO.md](../TODO.md).

## Pakiet typograficzny nad tym rejestrem milczał

Pakiet jest wycofany ([linter.md](linter.md#what-closed-the-track)),
więc ten przebieg jest zapisem, a nie poleceniem do powtórzenia.
Nad 104 062 słowami nie strzeliła ani jedna reguła.
Cudzysłowów prostych i angielskich nie ma,
polskie stoją parami (116 otwierających i 116 zamykających),
pauzy nie ma żadnej, a znaki przestankowe mają po sobie odstęp wszędzie.
Dwie z tych zer są zerami ekstrakcji, jak wyżej,
a pozostałe są własnością tekstu, który złożyła Kancelaria Sejmu.

Zero mówiło tu więc o korpusie, a nie o regule,
tak samo jak [tam, gdzie reguły cudzysłowu nie miały czego znaleźć](firing-rates.md#where-the-quotation-mark-rules-had-nothing-to-find):
tekst, nad którym pakiet milczy, jest podłogą, a nie próbką.
Nad oboma korpusami, które [odczyt częstości](firing-rates.md#the-rates) trzyma,
pakiet trafienia miał,
więc był to jedyny korpus tego repozytorium, nad którym nie miał żadnego.

## Nierozstrzygnięte

Czy ten korpus wchodzi do przeglądu korpusów
([corpora.md](corpora.md#the-composition-this-argues-for))
jako polszczyzna pisana przez ludzi.
Ma licencję, rejestr i etap produkcji, których tamten przegląd nie znalazł,
a nie ma tego, czego żądała od niego reguła typograficzna:
biały znak i pauzę zjada albo ekstrakcja, albo wydawca.
Rozstrzyga to pytanie ekstrakcja z PDF-a, którego API oddaje obok HTML-a,
a dopóki jej nie ma, ten korpus mierzy gramatykę i nic poza nią.

## Źródła

- Rozporządzenie Prezesa Rady Ministrów z dnia 20 czerwca 2002 r.
  w sprawie „Zasad techniki prawodawczej”,
  tekst jednolity Dz. U. z 2016 r. poz. 283 (`DU/2016/283`)
- Ustawa z dnia 4 lutego 1994 r. o prawie autorskim i prawach pokrewnych,
  art. 4 pkt 1 (`DU/1994/83`)
- API ELI Kancelarii Sejmu, `https://api.sejm.gov.pl/eli`,
  które oddaje akt pod adresem ELI w HTML-u i w PDF-ie
- Siedem ustaw korpusu, pod adresami ELI z polecenia wyżej;
  liczby w tym dokumencie wzięto 10 sierpnia 2026
  nad tym, co API wtedy oddało
