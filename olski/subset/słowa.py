"""Słownictwo, którym produkcje są pisane: zbiory lematów i terminale.

Terminal jest tym miejscem, w którym gramatyka styka się z morfologią:
mówi, jakiej części mowy i jakich cech żąda od formy,
a odczytania odbiera jej warstwa niżej (``olski/segmentacja.py``).
Lemat wypisany tutaj zbiorem jest wyborem o polszczyźnie, a nie o formalizmie —
który spójnik bierze przecinek, który stoi na czele zdania —
więc każdy taki zbiór niesie nad sobą swój powód,
a wywód wraz z ceną trzyma docs/subset.md.
"""

from __future__ import annotations

from olski.grammar import Part, V, word
from olski.lematy import (
    LEMAT_PRZECZENIA,
    LEMAT_ZWROTNY,
    PRZYIMEK_ROZDZIELAJĄCY,
    ZNAK_CUDZYSŁOWU_OTWIERAJĄCY,
    ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY,
)

#: Rzeczownik, przy którym polszczyzna opuszcza kopułę: `o których mowa`.
#: Jak często ten zwrot pada w rejestrze ustaw, liczy docs/ustawy.md.
#: Lista jest zamknięta i ma jeden lemat, a pozycję ogólną — zdanie z samej grupy
#: imiennej w mianowniku — zmierzono i odrzucono; wywód trzyma
#: docs/konstrukcje-gramatyczne/podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat.
RZECZOWNIK_ORZEKAJĄCY = "mowa"


#: Spójnik, którym zdanie podrzędne dopełnieniowe zaczepia się o czasownik.
#: Jeden, a nie cała klasa `comp`: `gdy`, `jeśli` i `aby` otwierają okolicznik
#: zdania, więc wpuszczone tą produkcją stanęłyby w pozycji, której nie zajmują.
SPÓJNIK_DOPEŁNIENIOWY = "że"


#: Orzeczenie, w którym dopełnienie stoi przed czasownikiem: `kto go nie używa`.
#: Symbol osobny od grupy orzeczenia, bo szyk ten bierze samo zdanie o czole
#: podmiotowym, a zdanie główne ma go już skądinąd; wywód stoi przy jego ciele.
GRUPA_ORZECZENIA_ODWRÓCONA = "grupa_orzeczenia_odwrócona"


#: Spójnik pytania rozstrzygnięcia: `Pyta, czy go to dotyczy.` Pytanie o rolę
#: podporządkowuje sam zaimek, więc czoło niesie tam rolę wysuniętą
#: (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`), a tutaj podporządkowuje spójnik i zdanie
#: pod nim jest całe. Stąd osobne ciało czoła, a nie lemat dopisany do listy.
SPÓJNIK_PYTAJNY = "czy"


#: Spójniki, których zdanie polszczyzna stawia przed zdaniem nadrzędnym i za nim.
#: Zajmują one obie pozycje okolicznika, a pozostałe stałe niżej wyliczają to,
#: co każda z tych dwóch list trzyma na zewnątrz.
SPÓJNIKI_WYSUWANE = frozenset({
    "gdy", "kiedy", "jeśli", "jeżeli", "zanim", "nim",
    "choć", "chociaż", "dopóki", "póki", "skoro", "ponieważ",
})


#: Spójniki, których zdanie stoi za zdaniem nadrzędnym i tylko tam, bo mówią one
#: o przyczynie dopowiedzianej, a nie o ramie, w której coś zachodzi:
#: `Zostaję w domu, bo pada.` jest polszczyzną, a `Bo pada, zostaję w domu.` nie.
#: Fakt ten jest faktem o słowie, a nie o kierunku, w którym się go używa,
#: i skład trzyma go już o `bo` oraz o `ponieważ`
#: (``staje_na_czele`` w ``olski/skład/spójniki.py``);
#: Oba kierunki przeczytałby jeden leksykon, bo tą samą drogą poszła walencja.
#: Świadka nad bankiem drzew czyta docs/subset.md.
SPÓJNIKI_PO_ZDANIU = frozenset({"bo", "gdyż", "albowiem", "aż"})


#: Spójniki otwierające okolicznik wyrażony zdaniem, czyli obie listy razem.
#: Lista jest zamknięta i stawia formie dwa żądania naraz, bo klasa `comp` niesie
#: także takie spójniki, których ta produkcja wziąć nie może.
#: Kogo zostawia na zewnątrz — `bowiem` i `więc` — i za co, wywodzi
#: docs/konstrukcje-gramatyczne/podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania.
#:
#: Zdanie pod spójnikiem z tej listy stoi w trybie oznajmującym, a spójniki, pod
#: którymi stoi tryb przypuszczający, wylicza :data:`SPÓJNIKI_TRYBU` i bierze
#: osobne ciało, bo żądają one od zdania cechy, której ta lista nie żąda.
SPÓJNIKI_OKOLICZNIKOWE = SPÓJNIKI_WYSUWANE | SPÓJNIKI_PO_ZDANIU


#: Przysłówek względny, którym ten rejestr dopowiada miejsce: `Wchodzi w
#: subset.md, gdzie produkcje stoją jedna pod drugą.` Morfeusz daje mu `adv`, a
#: nie `comp`, więc pozycji spójnika nie dosięga i bierze go ciało osobne.
#:
#: Miejsca ma dwa, tak samo jak :data:`SPÓJNIKI_WYSUWANE`, i drugie z nich
#: dopisał pomiar, a nie wywód: ciało samo za zdaniem odbierało czytanie zdaniu
#: `Gdzie cząstka może należeć do dwóch czasowników naraz, olski wypuszcza oba
#: odczytania.`, czyli napisowi, który ta proza pisze. Zdanie wysunięte znaczy
#: `wszędzie tam, gdzie`, a nie pyta o miejsce.
PRZYSŁÓWEK_WZGLĘDNY = "gdzie"


#: Przysłówki, którymi ten rejestr pyta o okoliczność:
#: `Dlaczego gramatyka rośnie?`, `Pyta, dlaczego gramatyka rośnie.`
#:
#: Kształt pytania jest dla nich wspólny — przysłówek wysunięty przed zdanie,
#: a zdanie pod nim całe (`okolicznik_pytajny` w ``olski/subset/podrzędne.py``) —
#: i dlatego zbiór, a nie lemat. Wpuszcza się je za to pojedynczo,
#: bo rozdziela je reszta czytań, które Morfeusz daje każdemu z nich,
#: i osobno się każdy wycenia; `dlaczego` ma czytanie jedno i weszło samo.
#: Kto czeka poza zbiorem i na co, wylicza
#: docs/konstrukcje-gramatyczne/podrzędność.md#pytanie-o-okoliczność-wysuwa-przysłówek-a-zdanie-pod-nim-jest-całe.
PRZYSŁÓWKI_PYTAJNE = frozenset({"dlaczego"})


#: Spójniki, które niosą cząstkę trybu przypuszczającego: `żeby` to `że` i `by`,
#: `gdyby` to `gdy` i `by`, `aby` to `a` i `by`, a `jakby` to `jak` i `by`.
#: Cząstka stoi w nich raz, więc pod nimi stoi forma na -ł bez własnej cząstki i
#: żąda ich ciało cechą ``tryb`` (:data:`TRYB_POD_SPÓJNIKIEM`): bez tego żądania
#: wyprowadzałoby się `aby program zapisuje ustawienia`, a obietnicą podzbioru
#: jest, że każde zdanie olskiego jest zdaniem polskim.
#:
#: Oba miejsca okolicznika bierze każdy z nich, i tym różnią się one
#: od :data:`SPÓJNIKI_PO_ZDANIU`.
#:
#: `iżby` i `by` w roli cząstki na tej liście nie stoją, choć Morfeusz zna oba:
#: pierwszego bank drzew nie ma ani raz, a drugie bierze terminal cząstki
#: (:data:`CZĄSTKA_TRYBU`), bo `by` jest jedną formą w dwóch rolach i rozdziela je
#: część mowy, którą słownik daje: `comp` spójnikowi, `part` cząstce.
SPÓJNIKI_TRYBU = frozenset({"aby", "ażeby", "żeby", "by", "gdyby", "jakby"})


#: Spójniki zdaniowe, przed którymi polszczyzna stawia przecinek: `Plany są
#: niczym, ale planowanie jest wszystkim.` przecinka żąda, a `Program zapisuje
#: ustawienia i linter sprawdza tekst.` nie bierze go wcale. Fakt jest to o słowie,
#: tak samo jak wysunięcie okolicznika (:data:`SPÓJNIKI_WYSUWANE`), więc lista
#: rozdziela spójnik zdaniowy na dwie klasy i obejmuje dwie części mowy naraz
#: (:data:`SPÓJNIKOWE`). Kogo nie obejmuje, za ile i po co, wywodzi docs/subset.md.
SPÓJNIKI_PRZECINKOWE = frozenset({
    "ale", "a", "lecz", "natomiast", "więc", "zatem", "toteż", "czyli",
})


#: Spójniki, za którymi ten rejestr opuszcza czasownik (:data:`ELIPSA`):
#: `a nie z projektu`, `czyli o obiekt składniowy`, `tylko w drugą stronę`.
#:
#: Lista jest węższa od :data:`SPÓJNIKI_PRZECINKOWE` i węższa być musi, bo
#: obietnicą podzbioru jest, że każde zdanie olskiego jest zdaniem polskim:
#: `Cena jest niska, więc gramatyka.` polszczyzną nie jest. Poza listą zostają
#: więc te trzy, które dokładają skutek: `więc`, `zatem` i `toteż`.
#:
#: `tylko` tu stoi, choć poza cząstkami zostało z powodu, który mówi o dwóch
#: czytaniach jednego napisu (:data:`CZĄSTKI`): warunek na spójnik czytania
#: cząstkowego tu nie wpuszcza.
SPÓJNIKI_ELIPSY = frozenset({"a", "ale", "lecz", "natomiast", "tylko", "czyli"})


#: Spójniki, które ten rejestr stawia wewnątrz swojego zdania (:data:`SPÓJNIK`):
#: `Milczenie jest zatem wartością.`, `Reguła jest bowiem tania.`
#:
#: Trzy z nich — `bowiem`, `zaś` i `jednak` — polszczyzna stawia za pierwszym
#: wyrazem zdania i nigdzie poza tym, więc olski nie brał ich wcale; pozostałe
#: stoją zarazem na czele zdania i tam biorą je :data:`SPÓJNIKI_PRZECINKOWE`.
#: Pozycja wewnątrz zdania czoła zdania składowego nie dostaje, i to trzyma jeden
#: napis przy jednym czytaniu: `Cena jest niska, więc gramatyka jest tania.` ma
#: spójnik za przecinkiem, więc bierze go tamta lista. Czoło całego zdania jest
#: pozycją trzecią i bierze tę listę wraz z tamtą (:data:`SPÓJNIK_NA_CZELE`).
SPÓJNIKI_WEWNĘTRZNE = frozenset({"zatem", "więc", "bowiem", "natomiast", "zaś", "jednak"})


#: Spójniki, które polszczyzna powtarza przed każdym członem ciągu, żądając przed
#: drugim przecinka: `Ani parser nie rośnie, ani linter nie sprawdza.`
#:
#: Klasa, a nie lemat, bo polszczyzna powtarza tak również `i` oraz `czy`;
#: oba zmierzono i oba wypadły, każde z innego powodu, a wywód trzyma
#: docs/konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-skorelowany-powtarza-się-przed-każdym-członem.
SPÓJNIKI_SKORELOWANE = frozenset({"ani"})


#: Spójniki łączące, które ten rejestr stawia na czele całego zdania, a których
#: żadna lista wyżej nie ma: `I nikt tego nie zauważył.`, `Albo inaczej.`
#:
#: Lista jest trzecia i jest krótka, bo dwie pozostałe niosą już `a`, `ale`,
#: `lecz`, `więc` i `zatem`, czyli to, czym ten rejestr zdanie otwiera najczęściej.
#: `ani` do niej nie należy, choć bank drzew otwiera nim zdania: otwiera je
#: spójnikiem skorelowanym — `Ani X, ani Y nie podpisują się` — czyli konstrukcją,
#: której olski nie ma, a wpuszczone tutaj samo `ani` odbiera jednoznaczność
#: `Ani jedno zdanie nie czyta się odwrotnie.` i nie kupuje ani jednego zdania.
SPÓJNIKI_ŁĄCZĄCE = frozenset({"i", "albo"})


#: Zaimek pytajno-względny, któremu Morfeusz daje znacznik przymiotnika.
#: Przymiotnikiem przy rzeczowniku nie jest nigdy, więc terminale przydawki i
#: orzecznika go nie biorą. Bierze go czoło zdania względnego oraz grupa pytajna
#: (:data:`GRUPA_PYTAJNA`), i te dwie pozycje są wszystkim, co ta gramatyka mu daje.
#: Ten warunek odbiera zdaniu podrzędnemu czytanie współrzędne, i za ile,
#: mierzy docs/subset.md.
#:
#: Nazwa mówi o obu pozycjach, bo lemat jest jeden: `Która reguła rozstrzyga?`
#: pyta, a `reguła, która rozstrzyga` zastępuje poprzednik, i rozdziela te dwa
#: użycia produkcja, a nie słownik.
ZAIMEK_PYTAJNO_WZGLĘDNY = "który"


#: Zaimek, którym pyta się o osobę i o rzecz, a Morfeusz trzyma go pod
#: rzeczownikiem: `kto` i `co`. Czoła są z niego dwa — pytania i zdania względnego
#: — a pozycji rzeczownej nie ma, bo dopóki ją miał, jeden napis dostawał dwa
#: wyprowadzenia.
#:
#: Wykluczenie stoi na terminalu, a nie w `admissible` w ``olski/segmentacja.py``,
#: bo czytanie `subst`
#: jest tym, o które pytają oba czoła. Odbiera ono pozycję wszystkim użyciom tych
#: zaimków naraz, więc razem z czołami wchodzi wszystko, co ta pozycja dotąd
#: niosła: zdanie względne bez poprzednika, ciąg pytań zależnych i orzecznik
#: wysunięty. Wywód i cenę trzyma
#: docs/konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz.
ZAIMEK_PYTAJNO_RZECZOWNY = frozenset({"kto", "co"})


#: Zaimek wskazujący, którego Morfeusz trzyma pod przymiotnikiem: formy `ten`,
#: `ta`, `to`. Przydawką przy rzeczowniku on jest — `ten parser` — więc terminale
#: przydawki go biorą, a wyklucza go jedno miejsce: przymiotnik za zaimkiem
#: pytajno-rzeczownym, gdzie `co to` wychodziłoby grupą pytajną, a polszczyzna
#: ma tam dwa zaimki obok siebie. Wywód i cenę trzyma
#: docs/konstrukcje-gramatyczne/podrzędność.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz.
ZAIMEK_WSKAZUJĄCY = "ten"


#: `Pięcie`, czyli rzeczownik odczasownikowy od `piąć`. Jego dopełniacz mnogi
#: Morfeusz pisze `pięć` i daje mu liczbę mnogą oraz rodzaj nijaki, czyli to,
#: czego liczebnik rządzący żąda od tego, co pod nim stoi, więc bez tego warunku
#: `dwadzieścia pięć chlebów` ma drugie czytanie z `pięć` w głowie grupy.
#: Wywód i cenę trzyma
#: docs/konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-złożony-przyłącza-się-wedle-ostatniego-członu.
PIĘCIE = "piąć"


#: Zaimki rzeczowne, którym Morfeusz daje czytanie `subst`. Dopełniacza żaden z nich
#: nie bierze: `tego podzbioru` jest przymiotnikiem przy rzeczowniku i niczym
#: więcej, a produkcja z dopełniaczem po głowie czyta to drugi raz jako zaimek
#: rządzący rzeczownikiem. Lista jest zamknięta, bo czytanie tych form niczym się
#: nie różni od czytania rzeczownika: `nikt` jest `subst:sg:nom:m1` tak samo jak
#: `parser` jest `subst:sg:nom:m3`. docs/subset.md wywodzi kryterium i mierzy cenę.
ZAIMEK_RZECZOWNY = frozenset({
    "to", "tamto", "owo", "kto", "któż", "ktoś", "ktokolwiek",
    "co", "cóż", "coś", "cokolwiek", "nikt", "nic", "wszystko",
})


#: Zaimek zwrotny, którego Morfeusz trzyma pod częścią mowy tej jednej formy:
#: `siebie:gen`, `sobie:dat`, `sobą:inst`. Terminalem, a nie ciałem grupy imiennej,
#: bo grupa niesie liczbę i rodzaj, a ciało bez nich wpuściłoby ten zaimek tam,
#: gdzie zgodności żąda ktoś inny: cechy, której konstytuent nie niesie, unifikacja
#: nie sprawdza, więc `Widzę siebie, która stoi.` by się wyprowadzało.
#: Cenę i pozycje trzyma
#: docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-zwrotny-jest-terminalem-bo-nie-zgadza-się-z-niczym.
ZWROTNY = word("siebie", case=V("c"))


#: The three features a Polish noun or adjective phrase agrees in, as the
#: variables every production sharing them uses. Spelling them out once is what
#: keeps two parts of one phrase demonstrably talking about the same agreement.
AGREE = {"case": V("c"), "number": V("n"), "gender": V("g")}


#: Liczba i rodzaj, w których zdanie względne zgadza się ze swoim poprzednikiem,
#: czyli ta z dwóch par czoła (:func:`zaimek_czoła`), którą poprzednik czyta.
POPRZEDNIK = {"number": V("nz"), "gender": V("gz")}


#: Wartość cechy `czoło` dla roli, którą wypełnia konstytuent stojący na swoim
#: miejscu; rola wysunięta niesie tam nazwę czoła, którym ją wypełniono.
#:
#: Cecha rozdziela dwie rodziny produkcji jednego symbolu i po to jedno tu jest:
#: `podmiot` wpisany do ciała czoła wpuszcza tam także `podmiot → grupa_imienna`, a wartość
#: osobna dla każdego czoła trzyma rodzinę względną osobno od pytającej.
#: Co bez niej wraca i ile ta etykieta kupuje, wywodzi
#: docs/konstrukcje-gramatyczne/podrzędność.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza.
BEZ_CZOŁA = "żadne"


#: Wartość cechy `dostawka`, czyli tego, że za zdaniem składowym coś już stoi.
#: Konstytuent dostawiony za zdanie ją wypuszcza, a konstytuent wysunięty przed
#: zdanie żąda od swojego gospodarza, żeby dostawki nie niósł
#: (:data:`olski.grammar.NIE_NIESIE`), więc wysunięty wchodzi pod dostawiony
#: i nigdy nad niego. Zdanie składowe, które nie ma ani jednego, ani drugiego,
#: cechy tej nie niesie, i pod to żądanie przechodzi.
#:
#: Wartość jest przez to jedna: żądanie ujemne pisze się w tej gramatyce pustym
#: więzem, a nie drugą wartością, której nikt nie wypuszcza
#: (:meth:`olski.grammar.Grammar.więzy_niespełnialne`).
#:
#: Bez tego żądania jeden napis wyprowadza się dwoma kształtami; co je różni, czego
#: nie różni i dlaczego warunek stoi tutaj, wywodzi
#: docs/konstrukcje-gramatyczne/okolicznik.md#określenie-przed-zdaniem-wchodzi-pod-to-które-stoi-za-nim.
DOSTAWKA = "jest"


#: Wartości cechy `ciąg`, czyli tego, czy zdanie ma kilka członów współrzędnych.
#: Żąda jej okolicznik zdaniowy dochodzący do całego ciągu, bo bez tego żądania
#: zdanie o jednym członie wyprowadza się dwoma kształtami: raz z okolicznikiem
#: przy członie, raz z tym samym okolicznikiem nad ciągiem, którym ten człon jest.
#:
#: Żądanie jest dodatnie, a cechy nieobecnej unifikacja nie sprawdza, więc cechę
#: wypuszcza każda produkcja `zdanie`: ta, która o ciągu przemilczy, wpuści
#: okolicznik nad zdanie pojedyncze. Tym różni się ta cecha od :data:`DOSTAWKA`,
#: której żądanie jest ujemne i której przemilczenie nic nie psuje. Cenę pozycji
#: trzyma
#: docs/konstrukcje-gramatyczne/podrzędność.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania.
CIĄG = "jest"


BEZ_CIĄGU = "brak"


#: Wartości cechy `rozdzielna`, czyli tego, czy ciąg przymiotników dzieli swój
#: rzeczownik między człony: `warstwy trzecia i czwarta` są dwiema warstwami,
#: a `warstwy nowe i tanie` warstwami, które są jedno i drugie naraz.
#:
#: Cecha rozdziela dwie rodziny ciał jednego symbolu, tak samo jak
#: :data:`BEZ_CZOŁA`, i po to jedno tu jest: polszczyzna stawia ciąg rozdzielny
#: za rzeczownikiem i nie stawia go przed nim.
#: Cenę obu ciał trzyma
#: docs/konstrukcje-gramatyczne/grupa-imienna.md#przydawka-koordynuje-się-i-rozdziela-rzeczownik-tylko-za-nim.
ROZDZIELNA = "jest"


BEZ_ROZDZIELNEJ = "brak"


#: Czy ten czasownik żąda orzecznika w narzędniku, czyli czy jest kopulą.
#:
#: Cecha powtarza to, co mówi rama (:data:`KOPULA`), i stoi obok niej dlatego,
#: że rama jest zbiorem, a unifikacja go przecina: żądanie umie wypisać `inst`
#: i wpuścić kopulę, a żądania odwrotnego nie ma jak wypisać.
#: Wartość :data:`KOPULARNY` jest przez to nośna, choć nie żąda jej ani jedno
#: ciało: bez niej produkcje kopuli tej cechy nie niosą wcale,
#: a cechy nieobecnej unifikacja nie sprawdza, więc żądanie przeszłoby i przy niej.
#: Para taka jest w tej gramatyce zwykłym sposobem na powiedzenie „nie” o wartości
#: — tak samo stoją :data:`BEZ_CZOŁA` i :data:`BEZ_CIĄGU` — a „nie” o samej cesze
#: pisze się pustym więzem (:data:`olski.grammar.NIE_NIESIE`), bo pod niego
#: przechodzi milczenie i tylko ono. Który warunek ujemny wchodzi do unifikacji,
#: a który stoi poza nią, wywodzi
#: docs/parsowanie.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne.
#:
#: Żądają jej dwa ciała i oba są zdaniem, w którym przy czasowniku nie stoi
#: żadne wypełnienie ramy (``build``): orzeczenie z samego czasownika oraz
#: wypełnienie złożone z samych okoliczników. Kopula w takim zdaniu nie stoi,
#: bo orzeka zawsze coś o czymś, a wpuszczona dałaby drugie czytanie każdemu
#: zdaniu, w którym orzeka narzędnikiem (:data:`OKOLICZNIK_NARZĘDNIKOWY`).
#: Cenę i zakup tego żądania trzyma
#: docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika.
KOPULARNY = "jest"


BEZ_KOPULI = "brak"


#: Przecinek jako znak koordynacji. Warunek na lemat, a nie sama część mowy, bo
#: ``interp`` niesie całą interpunkcję naraz, a każdy znak, który ten podzbiór
#: bierze, stoi tu osobnym terminalem i osobno się o jego cenę pyta.
PRZECINEK = word("interp", lemma=",")


#: Dwukropek, którym ten rejestr otwiera wyjaśnienie. Warunek na lemat, tak samo
#: jak przy przecinku, i z tego samego powodu.
DWUKROPEK = word("interp", lemma=":")


#: Średnik, którym ten rejestr rozdziela dwa zdania spięte treścią. Stoi obok
#: dwukropka, bo rozdziela na tej samej wysokości i tak samo nie konkuruje z
#: niczym: przed tą produkcją nie brał go żaden terminal.
ŚREDNIK = word("interp", lemma=";")


#: Cudzysłów, którym ten rejestr obejmuje tytuł i termin cytowany: `„Zasady
#: techniki prawodawczej”`. Terminale są dwa, po jednym na każdy znak
#: (``olski/lematy.py``), i po to ta para jest jednym napisem obu:
#: produkcja bez znaku zamykającego wpuszczałaby napis niedomknięty.
CUDZYSŁÓW_OTWIERAJĄCY = word("interp", lemma=ZNAK_CUDZYSŁOWU_OTWIERAJĄCY)


CUDZYSŁÓW_ZAMYKAJĄCY = word("interp", lemma=ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY)


#: Nawias, którym ten rejestr dopowiada obok zdania. Znaki są dwa tak samo jak
#: przy cudzysłowie i z tego samego powodu.
NAWIAS_OTWIERAJĄCY = word("interp", lemma="(")


NAWIAS_ZAMYKAJĄCY = word("interp", lemma=")")


#: Myślnik, którym ten rejestr rozdziela zdanie: `Cena jest niska — gramatyka jest
#: bezkontekstowa.` Stoi obok dwukropka i średnika (:data:`ŚREDNIK`).
#:
#: Znaki są dwa, bo polszczyzna pisze myślnik pauzą i półpauzą, a łącznik spaja
#: wewnątrz wyrazu — `16-latków`, `UTF-8` — więc tego warunek nie bierze. Co to
#: wykluczenie kosztuje, mierzy docs/subset.md.
MYŚLNIK = word("interp", lemma={"—", "–"})


#: Znak, którym ktoś zamknął zdanie. Nazwany raz, bo bierze go każde ciało zdania.
KONIEC_ZDANIA = word("interp", lemma={".", "!", "?"})


#: Pytajnik, którym ktoś zamknął zdanie pytające. Osobno od :data:`KONIEC_ZDANIA`,
#: bo tamten bierze każdy z trzech znaków, a zdanie pytające zamyka się jednym:
#: `Który aktor robi wrażenie.` polszczyzną nie jest.
#:
#: Tamtemu terminalowi ten warunek pytajnika nie odbiera i odbierać nie ma:
#: `Program zapisuje ustawienia?` jest pytaniem o rozstrzygnięcie, czyli zdaniem
#: oznajmującym zamkniętym tym znakiem, i tak je ta gramatyka wyprowadza.
PYTAJNIK = word("interp", lemma="?")


#: Zaimek na czele grupy pytajnej: ta sama forma co na czele zdania względnego
#: (:data:`ZAIMEK_PYTAJNO_WZGLĘDNY`) i ta sama zgodność, a różni je pozycja.
#: Terminal jest osobny, a nie wzięty z zaimka względnego: tamten symbol jest grupą
#: imienną o jednym słowie, a ten zaimek stoi przy rzeczowniku, który głową grupy
#: pytajnej jest.
ZAIMEK_PYTAJNY = word("adj", lemma=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE)


#: Zaimek dzierżawczy: `jego`, `jej`, `ich`, czyli dopełniacz zaimka trzeciej
#: osoby. Tym polszczyzna wyraża posiadanie i osobnego przymiotnika na to nie ma,
#: a `mój`, `nasz` oraz `swój` są u Morfeusza przymiotnikami i bierze je pozycja
#: przymiotnika.
#:
#: Warunek jest na cechę, a nie na lemat, bo lematem każdej z tych form jest `on`:
#: ``akc`` zostawia poza pozycją nieakcentowane `go`, a ``npraep`` przyimkowe
#: `niego`, `niej` i `nich`, których polszczyzna przy rzeczowniku nie stawia.
#: Warunek drugi odrzuca `bez niego zapisu`, czyli tę formę stojącą po przyimku;
#: poza przyimkiem nie ma jej już czym odrzucać,
#: bo zdejmuje ją `po_przyimku` w ``olski/segmentacja.py``.
ZAIMEK_DZIERŻAWCZY = word(
    "ppron3", case="gen", accentability="akc", post_prepositionality="npraep"
)


#: Części mowy, pod którymi Morfeusz trzyma spójnik: `ale` jest `conj`, a `więc`
#: `comp`, bo słownik rozdziela spójnik podrzędny od współrzędnego. Interpunkcja
#: przed spójnikiem tego podziału nie zna (:data:`SPÓJNIKI_PRZECINKOWE`), więc
#: terminale niżej pytają o obie naraz. Pyta o nie także sonda, która szuka
#: spójnika w cudzym ciele (``harness/ruch.py``).
SPÓJNIKOWE = frozenset({"conj", "comp"})


#: Dwie klasy, na jakie :data:`SPÓJNIKI_PRZECINKOWE` rozdziela spójnik zdaniowy.
#: Druga jest warunkiem ujemnym na pierwszą, bo klasy mają się nie zachodzić:
#: lemat wzięty obiema pozycjami dałby polszczyźnie dwa napisy tam, gdzie ma jeden.
#: Bierze ją także grupa imienna i przymiotnikowa, choć pozycji z przecinkiem te
#: dwa poziomy nie mają: `Plik jest nowy ale duży.` nie jest polszczyzną,
#: a `nie polszczyzny, a dziedziny` jest w nich elipsą, nie ciągiem współrzędnym.
#:
#: Klasa druga wyklucza ponadto cząstkę przeczącą, bo gramatyka ma dla tej formy
#: pozycję przy czasowniku (:data:`PRZECZENIE`), a Morfeusz czyta ją także jako
#: spójnik; kryterium jest to samo, którym stoi lista cząstek (:data:`CZĄSTKI`).
#: Cenę tego warunku trzyma docs/subset.md pod interpunkcją zdaniową.
SPÓJNIK_PRZECINKOWY = word(SPÓJNIKOWE, lemma=SPÓJNIKI_PRZECINKOWE)


SPÓJNIK_BEZ_PRZECINKA = word("conj", bez_lematu=SPÓJNIKI_PRZECINKOWE | {LEMAT_PRZECZENIA})


#: Spójnik przed członem bez czasownika, i spójnik wewnątrz swojego zdania.
SPÓJNIK_ELIPSY = word(SPÓJNIKOWE, lemma=SPÓJNIKI_ELIPSY)


SPÓJNIK_WEWNĘTRZNY = word(SPÓJNIKOWE, lemma=SPÓJNIKI_WEWNĘTRZNE)


#: Spójnik powtarzany przed każdym członem ciągu (:data:`SPÓJNIKI_SKORELOWANE`).
SPÓJNIK_SKORELOWANY = word(SPÓJNIKOWE, lemma=SPÓJNIKI_SKORELOWANE)


#: Spójnik na czele całego zdania, czyli ten sam spójnik zdaniowy, przed którym
#: nie stoi zdanie: `I nikt tego nie zauważył.`, `Zatem milczenie jest wartością.`
#:
#: Lematy schodzą się z trzech list, a wszystkie trzy nazywają spójnik łączący
#: dwa zdania. Listą, a nie wykluczeniem, bo formy o czytaniu spójnikowym, którym
#: ta gramatyka daje inną pozycję — `czy`, `to`, `jak`, `tymczasem` — dostają pod
#: wykluczeniem drugie czytanie, a klasy tej nie widać nad jednym korpusem;
#: pomiar trzyma docs/konstrukcje-gramatyczne/zdanie-złożone.md#spójnik-na-czele-zdania-wiąże-je-z-poprzednim.
#:
#: Obie części mowy naraz (:data:`SPÓJNIKOWE`), bo `zatem` i `więc` na czele
#: zdania dostają u Morfeusza `comp`, a bank drzew nazywa je tam `conj`; samo
#: `conj` wzięłoby więc te lematy nad korpusem i nie wzięłoby ich nad tekstem
#: czytanym na żywo.
SPÓJNIK_NA_CZELE = word(
    SPÓJNIKOWE, lemma=SPÓJNIKI_PRZECINKOWE | SPÓJNIKI_WEWNĘTRZNE | SPÓJNIKI_ŁĄCZĄCE
)


#: Przyimek wyrażenia przyimkowego, tego zwykłego i tego, które wysunęło zaimek
#: względny. Nazwany raz, bo oba wykluczają ten sam lemat i wykluczenie ma być w
#: obu to samo (:data:`PRZYIMEK_ROZDZIELAJĄCY`).
PRZYIMEK = word("prep", bez_lematu=PRZYIMEK_ROZDZIELAJĄCY, case=V("c"))


#: Przysłówek w okoliczniku: cała część mowy bez przysłówka względnego i bez
#: pytajnych. Stopnia nie żąda, bo `teraz` stopnia nie niesie, a `bardzo` niesie
#: `pos`, i oba są okolicznikami zdania.
#:
#: Wykluczenie stoi tu z tego samego powodu, z którego pozycji rzeczownej nie mają
#: `kto` i `co` (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`): okolicznikiem zdania
#: oznajmującego żaden z tych lematów nie bywa, a wpuszczony tutaj daje każdemu
#: zdaniu z nim czytanie ciągu współrzędnego, w którym przysłówek określa człon
#: drugi. Czytania tego polszczyzna nie ma, a jest ono jedynym, jakie te formy
#: dostają bez własnych ciał (:data:`PRZYSŁÓWEK_WZGLĘDNY`,
#: :data:`PRZYSŁÓWKI_PYTAJNE`), więc każde wykluczenie i jego ciało wchodzą razem.
PRZYSŁÓWEK = word("adv", bez_lematu=PRZYSŁÓWKI_PYTAJNE | {PRZYSŁÓWEK_WZGLĘDNY})


#: Przysłówek, którym zaczyna się pytanie o okoliczność (:data:`PRZYSŁÓWKI_PYTAJNE`).
PRZYSŁÓWEK_PYTAJNY = word("adv", lemma=PRZYSŁÓWKI_PYTAJNE)


#: Przymiotnik w formie poprzyimkowej: `polsku`, `cichu`, `prostu`, `bliska`.
#: Cała część mowy, bo `adjp` jest u Morfeusza formą, która poza przyimkiem nie
#: stoi, więc lista lematów nie miałaby czego odsiać.
FORMA_POPRZYIMKOWA = word("adjp")


#: Cząstki, które ten rejestr stawia przy zdaniu: `już`, `dopiero`, `także`.
#: Lista jest zamknięta, bo ``part`` niesie całą klasę cząstek naraz, a kryterium
#: na wejście jest jedno: cząstka ma nie mieć czytania, które gramatyka bierze już
#: gdzie indziej. `tylko` go ma — Morfeusz czyta je także jako spójnik, a spójnik
#: bierze koordynacja — więc wpuszczone tutaj dałoby jednemu napisowi dwa
#: wyprowadzenia, i tym samym warunkiem stoi lista spójników przecinkowych obok
#: listy bez przecinka (:data:`SPÓJNIKI_PRZECINKOWE`).
#: Kto zostaje poza listą i z jakiego powodu, wylicza
#: docs/konstrukcje-gramatyczne/okolicznik.md#cząstka-ma-dwóch-gospodarzy-i-przy-jednym-dostaje-etykietę.
CZĄSTKI = frozenset({
    "już", "jeszcze", "dopiero", "także", "również", "nawet", "zarazem", "naprawdę",
    "znowu", "wreszcie", "ponadto", "jedynie", "niemal", "niespełna", "zresztą", "przynajmniej",
})


#: Cząstka w okoliczniku: sama lista i nic więcej, tak samo jak :data:`PRZYSŁÓWEK`
#: bierze samą część mowy.
CZĄSTKA = word("part", lemma=CZĄSTKI)


#: Cząstki, które przybliżają liczbę i stoją przed liczebnikiem: `przeszło sto zdań`.
#: Lista jest rozłączna z :data:`CZĄSTKI` i rozłączna być musi: cząstka tamtej listy
#: dochodzi do grupy imiennej całej, więc lemat stojący na obu dałby `niemal sto zdań`
#: dwa wyprowadzenia jednego kształtu, a po statusie żadnego zdania tego nie widać.
#: Kryterium na wejście, cenę i to, kto zostaje na zewnątrz, trzyma
#: docs/konstrukcje-gramatyczne/grupa-imienna.md#cząstkę-przybliżającą-przyłącza-liczebnik-a-nie-grupa-imienna.
CZĄSTKI_PRZY_LICZEBNIKU = frozenset({"przeszło"})


#: Cząstka przybliżająca jako terminal (:data:`CZĄSTKI_PRZY_LICZEBNIKU`).
CZĄSTKA_PRZY_LICZEBNIKU = word("part", lemma=CZĄSTKI_PRZY_LICZEBNIKU)


#: Cząstka czasownika zwrotnego jako terminal.
CZĄSTKA_ZWROTNA = word("part", lemma=LEMAT_ZWROTNY)


#: Szyki cząstki zwrotnej wobec jej formy osobowej, każdy trójką: czy forma jest
#: zwrotna, co dochodzi do ciała przed przeczeniem i co za formą. Forma bez cząstki
#: ma oba miejsca puste, a forma z cząstką wchodzi tu raz na każdą pozycję, jaką
#: polszczyzna cząstce przy niej daje: `mieści się` i `się mieści`. Szyki stoją
#: wypisane, a nie składają się z listy pozycji, bo dwie pozycje puste dałyby formie
#: bez cząstki dwa ciała jednym napisem.
#:
#: Cząstka poprzedza przeczenie, a nie stoi między nim i formą, bo tak stawia je
#: polszczyzna: `się nie mieści`, a nie `nie się mieści`.
#: docs/konstrukcje-gramatyczne/orzeczenie.md#cząstka-zwrotna-należy-do-swojego-czasownika
#: wywodzi cenę pozycji przedniej i mówi, czego ona nie obejmuje.
SZYKI_CZĄSTKI: tuple[tuple[bool, tuple[Part, ...], tuple[Part, ...]], ...] = (
    (False, (), ()),
    (True, (), (CZĄSTKA_ZWROTNA,)),
    (True, (CZĄSTKA_ZWROTNA,), ()),
)


#: Predykatyw: słowo, które orzeka bez podmiotu i bez czasownika, a rządzi tym, co
#: rządziłby czasownik. `Trzeba czytać dokumenty.`, `Widać granicę w odpowiedzi.`,
#: `Wiadomo, że reguła jest tania.`
#:
#: Lista jest zamknięta, bo ``pred`` niesie całą klasę naraz, a kryterium na wejście
#: jest jedno: czytanie konkurujące nie może stanąć na czele zdania tego samego
#: kształtu. Kogo ono zostawia na zewnątrz i za ile, wywodzi
#: docs/konstrukcje-gramatyczne/orzeczenie.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika.
PREDYKATYWY = frozenset({
    "można", "trzeba", "warto", "wiadomo", "widać", "wolno", "słychać", "znać",
})


#: Predykatyw na czele swojego zdania: sama lista i nic więcej, tak samo jak
#: :data:`CZĄSTKA`.
PREDYKATYW = word("pred", lemma=PREDYKATYWY)


#: Łącznik między orzecznikiem a podmiotem, oba w mianowniku:
#: `to` w `Flaga to płat tkaniny.`
#: Warunek na lemat, a nie sama część mowy, tak samo jak przy predykatywie wyżej:
#: ``pred`` niesie całą klasę naraz.
ŁĄCZNIK = word("pred", lemma="to")


#: Przysłówek przy przymiotniku: ta sama część mowy i żądanie stopnia, więc
#: `tu duży` z tej pozycji wypada, a `bardzo duży` zostaje. Terminale są przez to
#: dwa, choć część mowy jedna: warunek należy do jednego gospodarza, a drugi bierze
#: przysłówek każdy. Czym jest żądanie obecności cechy, mówi ``niesione``
#: w olski/grammar.py, a cenę tego warunku trzyma
#: docs/konstrukcje-gramatyczne/okolicznik.md#naprawę-niesie-tagset-a-formalizm-ją-bierze.
PRZYSŁÓWEK_STOPNIA = word("adv", niesie="degree")


#: Cząstka przecząca, czyli jedyne słowo, którym olski przeczy. Warunek na lemat,
#: a nie sama część mowy, tak samo jak przy przecinku: ``part`` niesie całą klasę
#: cząstek naraz, a ``by``, ``czy`` i ``no`` ten podzbiór zostawia na zewnątrz.
PRZECZENIE = word("part", lemma=LEMAT_PRZECZENIA)


#: Cząstka trybu przypuszczającego, czyli ta, którą Morfeusz odcina od formy:
#: `odzyskałby` wchodzi jako `odzyskał` i `by`, a `napisałbym` jako `napisał`, `by`
#: i `m`. Warunek na lemat, a nie sama część mowy, tak samo jak przy przeczeniu i z
#: tego samego powodu: ``part`` niesie całą klasę cząstek naraz.
#:
#: Pozycję ma tę jedną, przy czasowniku; co zostaje poza nią — cząstka stojąca dalej
#: i cząstka wchodząca w spójnik — wywodzi
#: docs/konstrukcje-gramatyczne/orzeczenie.md#tryb-przypuszczający-jest-jedną-cząstką.
CZĄSTKA_TRYBU = word("part", lemma="by")


#: Wartości cechy ``tryb``, czyli tej, którą zdanie ogłasza, gdzie stoi cząstka
#: trybu przypuszczającego. Pyta o nią spójnik, który tę cząstkę niesie sam
#: (:data:`SPÓJNIKI_TRYBU`), a wypuszcza ją w górę każda produkcja zdania.
#:
#: Tryb oznajmujący, czyli zdanie bez cząstki: forma osobowa, a także forma na -ł
#: z aglutynantem.
TRYB_OZNAJMUJĄCY = "ozn"


#: Tryb przypuszczający, którego cząstka stoi przy czasowniku: `zapisałby`.
TRYB_PRZYPUSZCZAJĄCY = "przyp"


#: Tryb przypuszczający, którego cząstkę niesie spójnik nad zdaniem: `żeby` to
#: `że` i `by`, `gdyby` to `gdy` i `by`, więc pod takim spójnikiem stoi forma na -ł
#: bez własnej cząstki (:data:`SPÓJNIKI_TRYBU`).
TRYB_POD_SPÓJNIKIEM = "pod_spójnikiem"


#: Tryb formy na -ł stojącej bez cząstki, czyli obie wartości naraz: `zapisał`
#: orzeka w trybie oznajmującym, kiedy stoi samo, i w przypuszczającym, kiedy
#: cząstkę niesie spójnik nad nim. Jedna forma w dwóch trybach jest tu tym samym,
#: czym jest jedna forma w dwóch przypadkach: zbiorem, który unifikacja przecina.
TRYB_FORMY_NA_Ł = frozenset({TRYB_OZNAJMUJĄCY, TRYB_POD_SPÓJNIKIEM})


#: Przeczenie jako para: co dochodzi na początek ciała i jaką wartość cechy
#: ``negacja`` to ciało wypuszcza. Para, bo obie strony powstają razem: ciało bez
#: cząstki, które nie ogłasza ``aff``, przepuszcza dopełniacz negacji tam, gdzie
#: żadnego przeczenia nie ma, i cechy, której konstytuent nie niesie, unifikacja
#: nie sprawdza. Zdanie przeczące ma dokładnie jedno przeczenie, więc lista jest
#: pętlą po dwóch wartościach, a nie cząstką doklejaną gdziekolwiek.
PRZECZENIA: tuple[tuple[tuple[Part, ...], str], ...] = (((), "aff"), ((PRZECZENIE,), "neg"))
