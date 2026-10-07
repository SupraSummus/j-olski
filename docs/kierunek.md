# Kierunek

Olski ma być kompilatorem polszczyzny:
front-end czyta zdanie sztywną gramatyką,
reprezentacja pośrednia mówi, kto co robi,
przebieg semantyczny sprawdza tę reprezentację,
a back-end składa z niej polskie zdanie.
Ten dokument mówi, czemu taki układ, co jest w nim do rozstrzygnięcia i od czego zacząć.

## Zasady

- Parser i skład są sztywne i deterministyczne.
  Gramatyki i leksykonu nie zastępuje model.
- Model uczony wolno postawić tylko za reprezentacją pośrednią.
  Jego wejściem jest struktura: lemat, rola, cechy, klasa semantyczna.
  Napisu zdania model nie dostaje.
- O tym, czy zmiana działa, rozstrzyga wynik na cudzym tekście,
  oceniony przez człowieka.
  Własna proza repozytorium nie jest miarą.

## Czemu reprezentacja pośrednia

Gramatyka daje wiele rozbiorów tam, gdzie czytelnik widzi jeden.
Na tekstach z NKJP żadne z ocenionych zgłoszeń wieloznaczności się nie potwierdziło.
Każde z nich ma w `próba/nkjp-sądy.txt` zapisany powód,
czyli czytanie, które czytelnik odrzuca, i dlaczego.
Powody dzielą się z grubsza na trzy grupy.

**Czytania mówią o świecie to samo.**
To mniej więcej jedna trzecia zgłoszeń.
W zdaniu `Akcja zbierania podpisów jest prowadzona od wtorku.`
fraza `od wtorku` przyłącza się do `jest` albo do `prowadzona`,
a znaczenie zostaje to samo.
Tu nie brakuje semantyki.
Wieloznaczność liczono na drzewach, a powinno się ją liczyć na reprezentacji:
dwa drzewa, które dają tę samą strukturę predykatowo-argumentową, są jednym czytaniem.

**Jedno czytanie łączy słowa, które do siebie nie pasują.**
To druga mniej więcej jedna trzecia.
W `Spotkali się wzrokiem z Polkiem.` nikt nie czyta „wzroku z Polkiem”.
Rozstrzyga tu dopasowanie argumentu do miejsca przy orzeczeniu.
To jest miejsce na typy z Walentego i na model uczony na strukturach.

**Gramatyka bierze ramę, której czasownik nie ma.**
To kilka zgłoszeń.
`Czekają nagrody.` dostaje czytanie z dopełnieniem w bierniku,
choć `czekać` żąda `na`.
Naprawą jest leksykon, a nie model.

Resztę rozstrzyga interpunkcja, kontekst poprzedniego zdania albo nazwa własna.
Podział na grupy jest ręczny i zgrubny, a powody pisały sesje agenta,
więc to są proporcje do sprawdzenia, a nie pomiar.

## Potok

1. **Front-end:** `olski.segmentacja` daje graf form z Morfeusza,
   a `olski.parse` z gramatyką z `olski.subset` daje las rozbiorów.
2. **Reprezentacja pośrednia:** do zbudowania.
   Kandydatem jest drzewo wejściowe składu (`olski.skład.składnia`),
   bo ma już kategorie dziedziny, a nie kategorie składni.
   Wtedy tekst przechodzi w reprezentację i z powrotem w tekst.
   Zalążek tego przejścia już jest: `olski.skład.rozbiór` zamienia czytanie parsera
   w drzewo składu.
3. **Przebieg semantyczny:** do zbudowania.
   Najpierw typy: Walenty żąda od pozycji klasy rzeczy
   (na przykład osoby, miejsca, komunikatu),
   a `olski/żądania.txt` trzyma te żądania w postaci gotowej do czytania.
   Zalążek tego sprawdzenia już jest: `olski-check --żądania` wypisuje żądania pozycji,
   a `--osoby` zgłasza rzecz w pozycji, która żąda osoby.
   Osobę rozpoznaje po zamkniętej liście lematów z `olski.toml`, bo Słowosieci tu nie ma.
   Potem model ocenia trójki (orzeczenie, rola, argument)
   tam, gdzie typy nie rozstrzygają.
4. **Werdykt:** wieloznaczne jest zdanie, które ma więcej niż jedną wiarygodną reprezentację.
   Zaimek jest niejasny, gdy więcej niż jeden kandydat
   przechodzi morfologię i pasuje znaczeniem do miejsca zaimka.
5. **Back-end:** `olski.skład` składa z wybranej reprezentacji zdanie,
   które da się zaproponować autorowi jako jednoznaczne.

Model może się uczyć na trójkach wyjętych ze struktur:
ze złotych drzew Składnicy, ze zdań NKJP czytanych jednoznacznie
i z innych banków drzew polszczyzny.

## Do rozstrzygnięcia

- **Cechy z tekstu.**
  Czy model może brać wektory lematów wyuczone na surowym tekście?
  Wejściem zostaje wtedy struktura, ale wiedza modelu pochodzi z tekstu.
- **Pokrycie.**
  Gramatyka czyta niewiele ponad jedno zdanie Składnicy na pięć.
  Kompilator może odrzucać, czego nie rozumie,
  albo budować reprezentację z największych przeczytanych fragmentów zdania.
- **Słowosieć.**
  Klasy semantyczne Walentego są zbiorami synsetów Słowosieci,
  a tej nie da się dziś pobrać bez zgłoszenia (zob. [zasoby](zasoby.md#słowosieć)).

## Pierwszy krok

Zbudować reprezentację pośrednią dla zdań, które gramatyka czyta,
zaczynając od `olski.skład.rozbiór`, i porównywać czytania po obniżeniu do niej.
Pomiar: ile zgłoszeń wieloznaczności z `próba/nkjp-sądy.txt` znika bez żadnego modelu.
Na tym, co zostanie, postawić model zliczeniowy nad trójkami ze Składnicy
i sprawdzić go na tych samych sądach, na sądach o zaimkach
i na przyłączeniach z `próba/wybory-z-odpowiedzią.txt`.
Zbiorem testowym jest świeży wycinek NKJP oceniony przez człowieka.

## Stan sprzed resetu

Do commita `d79da51` olski był sprawdzaczem,
który zgłaszał usterki samą gramatyką podzbioru,
a projekt mierzył się w dużej części na własnej prozie.
Zatrzymały go dwa wyniki i jeden brak.
Na NKJP potwierdziło się 11 z 305 ocenionych zgłoszeń.
Gramatyka czytała niewiele ponad jedno zdanie Składnicy na pięć, a długich prawie wcale.
Użytkownika narzędzia nikt nie nazwał.
Odpowiedzią na pierwszy wynik jest semantyka na reprezentacji,
a nie kolejne produkcje gramatyki.

Tamte dokumenty uzasadniają wiele decyzji, które zostały w kodzie,
i komentarze w kodzie do nich odsyłają.
Czyta się je gitem, na przykład `git show d79da51:docs/subset.md`.
