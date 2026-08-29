"""Deklaracja podzbioru: co się w olskim wyprowadza, wypisane produkcjami.

Wykluczenia są dwojakie, bo produkcja rozstrzyga o zdaniu, a nie o formie.
Produkcje niżej mówią, jakie zdanie się wyprowadza,
a czytanie odbiera formie warstwa morfologiczna (``olski/segmentacja.py``),
zanim produkcja to czytanie zobaczy.
Co gramatyka orzeka o jednym zdaniu, mówi ``olski/werdykt.py``.

Gramatyka buduje się przy imporcie (:data:`GRAMMAR`),
więc kto pyta o sam lemat, sięga po ``olski/lematy.py``.
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Grammar, Głowa, Part, V, Var, nt, word
from olski.lematy import (
    KOPULA,
    LEMAT_ZWROTNY,
    PRZYIMEK_ROZDZIELAJĄCY,
    ZNAK_CUDZYSŁOWU_OTWIERAJĄCY,
    ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY,
)
from olski.parse import Deklaracja
from olski.precedencja import Rozwinięcie
from olski.walencja import (
    BEZ_BIERNIKA,
    BEZ_BIERNIKA_ZWROTNE,
    Z_BEZOKOLICZNIKIEM_ZWROTNE,
    Z_CELOWNIKIEM,
    Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU,
    Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU_ZWROTNE,
    Z_CELOWNIKIEM_ZWROTNE,
    Z_DOPEŁNIACZEM,
    Z_DOPEŁNIACZEM_ZWROTNE,
)

#: Rola, którą gramatyka zostawia nierozstrzygniętą rozmyślnie,
#: więc streszczenie czytania nazywa przy niej i to, co ona określa:
#: bez tego dwa czytania różne samym miejscem przyłączenia wychodzą jednym napisem.
PRZYŁĄCZANY = "Modifier"

#: Rola przysłówka, czyli tego, który określa zdanie. Przysłówek określający
#: przymiotnik roli nie dostaje: stoi on wewnątrz orzecznika albo przydawki, więc
#: widać go w wypełnieniu tamtej roli, a wypisany drugi raz obok mówiłby o zdaniu,
#: że ma okolicznik, którego ono nie ma.
PRZYSŁÓWKOWY = "Adverb"

#: Rola okolicznika wyrażonego zdaniem.
#: Stoi ona zarazem wśród zdań podrzędnych, bo wnętrze tego okolicznika
#: jest osobnym zdaniem, i tyle znaczy nazwanie go rolą:
#: streszczenie nazywa go całym napisem i w środek nie zagląda.
OKOLICZNIKOWY = "AdverbialClause"

#: Rola grupy pytajnej:
#: `które zadania` w `Ustawy określają, które zadania mają charakter obowiązkowy.`
#: Konstytuentem jest grupa imienna,
#: więc wnętrze streszczenie nazywa całym napisem, tak samo jak wnętrze podmiotu.
PYTAJNY = "Interrogative"

#: Rola rzeczownika, który orzeka bez czasownika:
#: `mowa` w `zadania, o których mowa w ustawie`.
#: Zdanie z tym rzeczownikiem nie ma ani podmiotu, ani czasownika,
#: więc bez tej etykiety wychodziłoby `valid` bez ani jednej roli.
#: Czemu rola stoi obok `Predicative`, a nie jest nią, wywodzi
#: docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną.
ORZEKAJĄCY = "NominalPredicate"

#: Rola tego, co orzeka bez podmiotu. Głowy są dwie i obie rządzą ramą czasownika:
#: predykatyw — `trzeba` w `Trzeba czytać dokumenty.` — oraz forma `imps` —
#: `zgłoszono` w `Zgłoszono usterkę.`
#:
#: Rola stoi obok `Verb`, a nie jest nią, bo żadna z tych dwóch głów zgodności nie
#: niesie: `Verb: trzeba` mówiłoby o zdaniu, że ma orzeczenie zgodne z podmiotem,
#: którego ono nie ma, a `Verb: zgłoszono` dałoby `Zgłoszono program.` podmiot
#: `program`, bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza.
#: Co wpuszczenie każdej z tych dwóch głów kosztuje, mierzą
#: docs/subset.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika oraz
#: docs/subset.md#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu.
BEZOSOBOWY = "ImpersonalPredicate"

#: Rola cząstki stojącej przy zdaniu: `już`, `dopiero`, `także`.
#: Od przysłówka różni ją część mowy, a pozycję ma tę samą,
#: i dlatego pisze je jedna pętla.
CZĄSTKOWY = "Particle"

#: Rola wtrącenia w nawiasie: `(docs/subset.md)`, `(niżej)`.
#: Rolą zdania jest samo wtrącenie, a nie to, co ono niesie,
#: bo nawias dopowiada, a nie wypełnia pozycji:
#: grupa imienna w jego środku nie jest ani podmiotem, ani dopełnieniem,
#: i streszczenie nazywa ją całym napisem.
WTRĄCONY = "Parenthetical"

#: Rola członu, którego czasownik ten rejestr opuszcza: `a nie zdanie` w
#: `Milczenie obejmuje wybór, a nie zdanie.`, `czyli o obiekt składniowy` w
#: `Warstwa pyta o Przyłączenie, czyli o obiekt składniowy.`
#:
#: Nazwa mówi o kształcie, a nie o tym, co ten człon robi, bo jednego od drugiego
#: gramatyka nie odróżnia: `a nie` przeczy, `czyli` powtarza to samo innymi
#: słowami, a spójnik jest jedyną różnicą i o znaczeniu nie rozstrzyga. Czemu ten
#: człon przeczy, milczy tym samym prawem: `Wybór obejmuje milczenie, a nie
#: zdanie.` przeciwstawia albo dopełnieniu, albo podmiotowi.
#:
#: Rolą jest cały człon, a nie to, co on niesie, i z tego samego powodu, z
#: którego rolą jest całe wtrącenie (:data:`WTRĄCONY`).
ELIPSA = "Ellipsis"

#: Symbol pary wypełnień: dopełnienie w celowniku obok wypełnienia, które zajmuje
#: pozycję ramy. Symbolem, a nie ciałami wypisanymi w `Complements`, bo inaczej
#: szyk pary mnoży się przez miejsca na okolicznik wokół niej, a tak każde z tych
#: dwóch mnoży się osobno. Rolą ta nazwa nie jest — role wylicza
#: :data:`DEKLARACJA` — bo werdykt nazywa dopełnienie dopełnieniem, a nie parą.
DRUGA_POZYCJA = "SecondComplement"

#: Symbol frazy bezokolicznikowej, której pozycji ramy nie wypełnia nic w jej
#: środku: wypełnia ją konstytuent stojący przed formą osobową, która tę frazę
#: bierze — `większości` w `premier większości nie może ruszyć`. Rama idzie z tej
#: frazy w górę cechą `wysunięte`, bo o pozycję pyta dopełnienie stojące poza nią.
#:
#: Symbolem, a nie ciałem obok pozostałych ciał `InfinitivePhrase`, bo cena tej
#: pozycji ma być osobną liczbą, a sonda różnicowa bierze ją zdejmowaniem ciał
#: (CLAUDE.md#code): ciała dopisane tamtemu symbolowi schodziłyby razem z frazą,
#: która pozycję ramy wypełnia sama.
BEZOKOLICZNIK_OTWARTY = "OpenInfinitivePhrase"

#: Rola spójnika, który stoi wewnątrz swojego zdania: `zatem` w `Milczenie jest
#: zatem wartością.` Od cząstki różni ją to, co to słowo robi: cząstka określa
#: zdanie, a ten spójnik wiąże je z tym, co stoi przed nim.
SPÓJNIKOWY = "Connective"

#: Rola grupy imiennej, którą ten rejestr wylicza za dwukropkiem: `Zdanie oraz
#: Kontekst` w `Warstwa pyta o dwa typy: Zdanie oraz Kontekst.` Rolą jest cała
#: grupa, z tego samego powodu co przy :data:`WTRĄCONY`.
#:
#: Rola stoi osobno od :data:`ELIPSA`, choć `, czyli Morfeusz` i `: Morfeusz`
#: dopowiadają to samo, bo rozdziela je kształt: tamten człon stoi za spójnikiem
#: i w zdaniu składowym, a ten za dwukropkiem i w zdaniu całym, gdzie dwukropek
#: musi stać (:data:`DWUKROPEK`). Jedna rola na oba żądałaby cechy, która by te
#: dwa poziomy rozdzieliła, czyli maszynerii droższej niż druga nazwa.
DOPOWIEDZIANY = "Apposition"

DEKLARACJA = Deklaracja(
    # Konstrukcja, na którą nie ma tu etykiety,
    # wychodzi `valid` bez słowa o tym, co olski w niej przyjął.
    role=(
        "Subject",
        "Object",
        "Predicative",
        "Verb",
        ORZEKAJĄCY,
        BEZOSOBOWY,
        PRZYSŁÓWKOWY,
        CZĄSTKOWY,
        SPÓJNIKOWY,
        OKOLICZNIKOWY,
        PYTAJNY,
        WTRĄCONY,
        ELIPSA,
        DOPOWIEDZIANY,
        PRZYŁĄCZANY,
    ),
    # Tu stoi każda rola, którą gramatyka wpuszcza w kilka miejsc:
    # bez nazwy gospodarza dwa czytania różne samym miejscem
    # wychodzą z werdyktu jednym wierszem powtórzonym dwa razy.
    # W `Począł myśleć gorączkowo.` czytania różni tylko to,
    # czy `gorączkowo` doszło do bezokolicznika, czy do formy osobowej nad nim.
    # Kryterium bierzemy z kształtu gramatyki i płacimy strzałką,
    # która powtarza czasownik zdania tam, gdzie gospodarz jest jeden.
    # Strzałka stawiana dopiero tam, gdzie gospodarz się rusza, byłaby tańsza,
    # a zabrałaby ją zdaniu o jednym czytaniu, gdzie nie rusza się nigdy,
    # choć mówi jedyną rzecz, jakiej o tym czytaniu nie widać po rolach.
    # Dopowiedzenie zostaje przez to poza listą,
    # bo gramatyka daje mu jedno miejsce (`Sentence` niżej),
    # więc jego strzałka powtarzałaby czasownik zawsze.
    przyłączane=(
        PRZYŁĄCZANY,
        PRZYSŁÓWKOWY,
        CZĄSTKOWY,
        SPÓJNIKOWY,
        OKOLICZNIKOWY,
        WTRĄCONY,
        ELIPSA,
    ),
    rozstrzygany=PRZYŁĄCZANY,
    # Konstytuenty, na których zatrzymuje się zejście w górę od modyfikatora
    # (``_gospodarze`` w ``olski/parse.py``).
    # Streszczenie nazywa ten z nich, który stoi najbliżej, bo tam przyłączenie zapadło,
    # a okolicznik zdania nie ma nad sobą ani grupy imiennej, ani przymiotnikowej
    # i zostaje przy zdaniu.
    # Pominięty wpis nie odbiera zdania, tylko przekłamuje streszczenie:
    # okolicznik wychodzi z takiego konstytuentu w górę,
    # a werdykt nazywa gospodarza stojącego nad nim
    # — bez ``RelativeCore`` poprzednik zamiast orzeczenia zdania względnego —
    # albo streszcza oba czytania jednym napisem, jak bez ``InfinitivePhrase``.
    gospodarze=(
        "NP",
        "AP",
        "ClauseConjunct",
        "RelativeCore",
        "NominalRelativeCore",
        "InfinitivePhrase",
        BEZOKOLICZNIK_OTWARTY,
        "InterrogativeCore",
    ),
    # Symbole, których ciąg nawiasuje napis roli: grupa imienna, grupa
    # przymiotnikowa i zdanie.
    # Człon nazywa tu produkcja spójnikowa i przecinkowa każdego z nich,
    # a nie symbol z końcówką ``Conjunct``, który jest jednym członem, a nie ciągiem.
    # Przydawka koordynuje się tak samo i tutaj nie stoi:
    # nawias schodzi do ciągu przez węzły o jednej córce (``_nawiasuj`` w ``olski/parse.py``),
    # a przydawka stoi pod rzeczownikiem, czyli w ciele o kilku córkach,
    # więc wpisana tu odbierałaby wiersz o konstytuencie, nie dając w zamian nawiasu.
    współrzędne=("NP", "AP", "Clause"),
    # Symbol jest tu ten z końcówką `Conjunct`, bo streszczenie pyta o rozpiętość
    # jednego zdania, a nie o ciąg, w którym ono stoi.
    # Czoło pytania członem tego ciągu nie bywa, więc dopisane tutaj
    # nie rozdzieliłoby ani jednego streszczenia.
    składowe=("ClauseConjunct",),
    # Lista zatrzymuje zejście po role wszędzie, gdzie konstytuent nazywa się
    # całym napisem, a nie tylko przy zdaniu podrzędnym: wywody trzymają
    # :data:`OKOLICZNIKOWY`, :data:`WTRĄCONY`, :data:`ELIPSA` i :data:`DOPOWIEDZIANY`.
    # Zdania podrzędne stoją tu symbolem opakowującym, a nie samym `Clause`,
    # bo `Clause` koordynuje — jest wypisane wyżej wśród współrzędnych —
    # więc zatrzymanie na nim objęłoby także zdanie współrzędne,
    # którego role są rolami tego samego zdania.
    podrzędne=(
        "RelativeClause",
        "NominalRelativeClause",
        "SubordinateClause",
        "InterrogativeClause",
        "FreeRelativeClause",
        OKOLICZNIKOWY,
        WTRĄCONY,
        ELIPSA,
        DOPOWIEDZIANY,
    ),
)

#: Rzeczownik, przy którym polszczyzna opuszcza kopułę: `o których mowa`.
#: Jak często ten zwrot pada w rejestrze ustaw, liczy docs/ustawy.md.
#: Lista jest zamknięta i ma jeden lemat, a pozycję ogólną — zdanie z samej grupy
#: imiennej w mianowniku — zmierzono i odrzucono; wywód trzyma
#: docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną.
RZECZOWNIK_ORZEKAJĄCY = "mowa"

#: Spójnik, którym zdanie podrzędne dopełnieniowe zaczepia się o czasownik.
#: Jeden, a nie cała klasa `comp`: `gdy`, `jeśli` i `aby` otwierają okolicznik
#: zdania, więc wpuszczone tą produkcją stanęłyby w pozycji, której nie zajmują.
SPÓJNIK_DOPEŁNIENIOWY = "że"

#: Orzeczenie, w którym dopełnienie stoi przed czasownikiem: `kto go nie używa`.
#: Symbol osobny od `Predicate`, bo szyk ten bierze samo zdanie o czole
#: podmiotowym, a zdanie główne ma go już skądinąd; wywód stoi przy jego ciele.
ORZECZENIE_ODWRÓCONE = "InvertedPredicate"

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
#: TODO.md trzyma ruch, którym oba kierunki przeczytałyby jeden leksykon,
#: bo tą samą drogą poszła walencja.
#: Świadka nad bankiem drzew czyta docs/subset.md.
SPÓJNIKI_PO_ZDANIU = frozenset({"bo", "gdyż", "albowiem", "aż"})

#: Spójniki otwierające okolicznik wyrażony zdaniem, czyli obie listy razem.
#: Lista jest zamknięta i stawia formie dwa żądania naraz, bo klasa `comp` niesie
#: także takie spójniki, których ta produkcja wziąć nie może.
#: Kogo zostawia na zewnątrz — `bowiem` i `więc` — i za co, wywodzi
#: docs/subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania.
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

#: Cząstka przecząca jako lemat, bo pytają o nią dwa miejsca: terminal, którym
#: olski przeczy (:data:`PRZECZENIE`), i wykluczenie w klasie spójników bez
#: przecinka (:data:`SPÓJNIK_BEZ_PRZECINKA`). Napisana dwa razy rozeszłaby się
#: po pierwszej zmianie któregoś z nich.
LEMAT_PRZECZENIA = "nie"

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

#: Spójniki, które ten rejestr stawia wewnątrz swojego zdania (:data:`SPÓJNIKOWY`):
#: `Milczenie jest zatem wartością.`, `Reguła jest bowiem tania.`
#:
#: Trzy z nich — `bowiem`, `zaś` i `jednak` — polszczyzna stawia za pierwszym
#: wyrazem zdania i nigdzie poza tym, więc olski nie brał ich wcale; pozostałe
#: stoją zarazem na czele zdania i tam biorą je :data:`SPÓJNIKI_PRZECINKOWE`.
#: Czoła ta lista nie dostaje wcale, i to trzyma jeden napis przy jednym
#: czytaniu: `Cena jest niska, więc gramatyka jest tania.` ma spójnik za
#: przecinkiem, więc bierze go tamta lista.
SPÓJNIKI_WEWNĘTRZNE = frozenset({"zatem", "więc", "bowiem", "natomiast", "zaś", "jednak"})

#: Zaimek pytajno-względny, któremu Morfeusz daje znacznik przymiotnika.
#: Przymiotnikiem przy rzeczowniku nie jest nigdy, więc terminale przydawki i
#: orzecznika go nie biorą. Bierze go czoło zdania względnego oraz grupa pytajna
#: (:data:`PYTAJNY`), i te dwie pozycje są wszystkim, co ta gramatyka mu daje.
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
#: docs/subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz.
ZAIMEK_PYTAJNO_RZECZOWNY = frozenset({"kto", "co"})

#: `Pięcie`, czyli rzeczownik odczasownikowy od `piąć`. Jego dopełniacz mnogi
#: Morfeusz pisze `pięć` i daje mu liczbę mnogą oraz rodzaj nijaki, czyli to,
#: czego liczebnik rządzący żąda od tego, co pod nim stoi, więc bez tego warunku
#: `dwadzieścia pięć chlebów` ma drugie czytanie z `pięć` w głowie grupy.
#: Wywód i cenę trzyma
#: docs/subset.md#liczebnik-złożony-przyłącza-się-wedle-ostatniego-członu.
PIĘCIE = "piąć"

#: Rama czasownika spoza leksykonu: dopełnienie w bierniku, orzecznik zgodny,
#: bezokolicznik, zdanie podrzędne i pytanie zależne. Zabrania ona dwóch rzeczy.
#: Narzędnika w niej nie ma, bo orzecznik narzędnikowy bierze kopula i nikt poza
#: nią, a celownika ani dopełniacza nie ma, bo dopełnienie w tych przypadkach
#: wpuszcza wpis w leksykonie (:data:`DOKŁADANE`). Zdanie podrzędne stoi w niej mimo
#: tego, że leksykon wylicza lematy, które je biorą: zawężenie zmierzono i nie
#: odbiera ono ani jednego drugiego czytania, a kosztuje zdanie; docs/subset.md
#: trzyma pomiar.
#:
#: Pytanie zależne jest pozycją osobną od zdania z `że`, a nie tym samym `comp`,
#: bo Walenty rozdziela je kształtem i mówi to o kilkuset lematach; wywód i
#: polecenie trzyma docs/subset.md. Stoi ono w ramie domyślnej tak samo jak `comp`,
#: a zawężenia tej pozycji do leksykonu nikt nie zmierzył — TODO.md trzyma ten
#: przebieg.
RAMA_DOMYŚLNA = frozenset({"nom", "acc", "inf", "comp", "int"})


#: Rama lematu, o którym leksykon mówi, że biernika nie bierze.
#:
#: Ramy węższe odejmują od domyślnej, a nie stoją wypisane obok niej, żeby
#: pozycję dopisaną tam widziała każda z nich.
RAMA_BEZ_BIERNIKA = RAMA_DOMYŚLNA - {"acc"}

#: Rama czasownika zwrotnego spoza leksykonu: domyślna bez bezokolicznika.
#:
#: Odjęcie to jest zdaniem o cząstce, a nie o czasowniku. Cząstka stoi po obu
#: stronach swojej formy osobowej i po obu stronach bezokolicznika pod nią, więc w
#: `ma się odbyć` jeden napis pasuje do dwóch ciał naraz: `[ma się] [odbyć]` oraz
#: `[ma] [się odbyć]`. Polszczyzna ma tam jedno czytanie, a rozstrzyga o nim
#: leksykon: `mieć się` bezokolicznika nie bierze, a `starać się` bierze
#: (:data:`Z_BEZOKOLICZNIKIEM_ZWROTNE`). Bez tego odjęcia pozycja przy
#: bezokoliczniku dokłada drugie wyprowadzenie każdemu zdaniu tego kształtu,
#: zamiast odbierać nieprawdziwe.
#:
#: Po stronie niezwrotnej pozycja ta zostaje w ramie domyślnej, bo tam konkurencji
#: nie ma i zawężenie zmierzono: nie kupiło ani jednego drugiego czytania
#: (:data:`RAMA_DOMYŚLNA`). Cenę odjęcia zwrotnego trzyma
#: docs/subset.md#cząstka-zwrotna-należy-do-swojego-czasownika.
RAMA_DOMYŚLNA_ZWROTNA = RAMA_DOMYŚLNA - {"inf"}

#: Pozycja, której rama domyślna tej klasy słowa nie ma, a leksykon ją lematowi
#: daje: nazwa pozycji wraz ze zbiorami lematów, osobno dla formy bez cząstki
#: ``się`` i z nią.
#:
#: Zdanie leksykonu jest tu twierdzące, a przy bierniku ujemne, i przeciwne są
#: domyślności, od których oba odejmują: biernik stoi w ramie domyślnej, a
#: przypadek poza nim nie stoi w niej wcale. Bezokolicznik odejmuje w jedną stronę
#: i dokłada w drugą, bo domyślności są tu dwie: rama zwykła go ma, a zwrotna nie
#: (:data:`RAMA_DOMYŚLNA_ZWROTNA`), więc zbiór zwykły jest pusty.
DOKŁADANE = (
    ("dat", Z_CELOWNIKIEM, Z_CELOWNIKIEM_ZWROTNE),
    ("gen", Z_DOPEŁNIACZEM, Z_DOPEŁNIACZEM_ZWROTNE),
    ("inf", frozenset(), Z_BEZOKOLICZNIKIEM_ZWROTNE),
)


def _dokładane(zwrotne: bool) -> list[tuple[str, frozenset[str]]]:
    """Pozycje dokładane wraz z lematami tej klasy słowa (:data:`DOKŁADANE`)."""
    return [(nazwa, zwrotni if zwrotne else zwykli) for nazwa, zwykli, zwrotni in DOKŁADANE]


#: Druga pozycja ramy, czyli dopełnienie dokładane stojące obok wypełnienia:
#: `Parser pokazuje autorowi oba czytania.` Wartość nazywa przypadek tego
#: dopełnienia, a :data:`BEZ_DRUGIEJ` mówi, że lemat pary nie ma.
#:
#: Cechą osobną, a nie pozycją ramy, bo rama jest zbiorem, którego unifikacja
#: przecina, więc żądanie dwóch pozycji naraz wypisane w niej byłoby ich
#: alternatywą: ta cecha licencjonuje celownik, a rama równolegle wypełnienie,
#: obok którego on stoi.
#:
#: Wartość jest jedna, bo jeden przypadek ma tę parę zmierzoną: dopełniacz obok
#: wypełnienia bierze u Walentego kilkadziesiąt lematów, a celownik kilka tysięcy;
#: liczby trzyma docs/subset.md#druga-pozycja-ramy-jest-celownikiem-obok-wypełnienia.
DRUGA_CELOWNIK = "dat"
BEZ_DRUGIEJ = "bez"


def _rama(
    lemat: str,
    domyślna: frozenset[str],
    bez_biernika: frozenset[str],
    dokładane: Sequence[tuple[str, frozenset]],
) -> frozenset[str]:
    """Rama tego lematu: domyślna bez tego, czego leksykon mu odmawia, i z tym, co mu daje.

    ``domyślna`` jest domyślną jego klasy słowa, bo klasy te mają dwie różne
    (:data:`RAMA_DOMYŚLNA_ZWROTNA`).
    """
    odjęta = domyślna - {"acc"} if lemat in bez_biernika else domyślna
    return odjęta | {nazwa for nazwa, lematy in dokładane if lemat in lematy}


def _klasy_walencyjne(
    domyślna: frozenset[str],
    bez_biernika: frozenset[str],
    dokładane: Sequence[tuple[str, frozenset]],
    poza: frozenset[str] = frozenset(),
) -> dict[frozenset[str], frozenset[str]]:
    """Lematy leksykonu zebrane w klasy po ramie, którą leksykon każdemu z nich daje.

    ``poza`` zabiera lematy, które mają ramę wypisaną ręcznie: klasy mają się nie
    zachodzić, a lemat wzięty dwiema byłby dwoma czytaniami tego samego kształtu.

    Klucz sortowania jest wypisany, bo rama jest zbiorem, a ``<`` na zbiorach
    porównuje zawieraniem: ``sorted`` bez klucza oddaje kolejność wejścia i nie
    wywraca się przy tym. Kolejność klas ustala kolejność produkcji, a ta
    kolejność, w jakiej las wydaje czytania (CLAUDE.md#code).
    """
    klasy: dict[frozenset[str], set[str]] = {}
    for lemat in bez_biernika.union(*(lematy for _nazwa, lematy in dokładane)) - poza:
        klasy.setdefault(_rama(lemat, domyślna, bez_biernika, dokładane), set()).add(lemat)
    return {
        rama: frozenset(lematy)
        for rama, lematy in sorted(klasy.items(), key=lambda para: sorted(para[0]))
    }


def _walencja() -> tuple[
    dict[frozenset[str], frozenset[str]], dict[frozenset[str], frozenset[str]]
]:
    """Leksykon jako klasy walencyjne, osobno dla formy z cząstką ``się`` i bez niej.

    Zwrotność jest drugim wymiarem klucza, a nie częścią lematu, i dlaczego,
    mówi ``olski/walencja.py``, czyli ten, który leksykon czyta dla obu
    kierunków. Tutaj zostaje to, co jest zdaniem samej gramatyki.

    Kluczem klasy jest rama, a nie lemat, bo tak wychodzi produkcja: powstaje raz
    na ramę, a nie raz na lemat. Kopula zabiera leksykonowi swoje lematy, zamiast
    stanąć obok nich, bo klasy mają się nie zachodzić: Walenty mówi o niej to samo
    co leksykon o każdym innym lemacie, a rama kopuli mówi ponadto o narzędniku.

    Zdania leksykonu są tu cztery — o bierniku, o celowniku, o dopełniaczu i o
    bezokoliczniku — a plik mówi pięć. Bezokolicznik czyta sama strona zwrotna;
    co zdejmuje go po drugiej i co zdejmuje piąte zdanie, mówi :data:`RAMA_DOMYŚLNA`.
    """
    return (
        {
            **_klasy_walencyjne(RAMA_DOMYŚLNA, BEZ_BIERNIKA, _dokładane(False), KOPULA),
            frozenset({"nom", "inst"}): KOPULA,
        },
        _klasy_walencyjne(RAMA_DOMYŚLNA_ZWROTNA, BEZ_BIERNIKA_ZWROTNE, _dokładane(True)),
    )


#: Walencja: co czasownik bierze, wypisane lematami, a nie produkcjami.
#: Leksykon jest otwarty i ma ramę domyślną, więc czasownik dopisuje się wpisem, a
#: nie produkcją; czym taki leksykon jest, a czym nie jest, wywodzi
#: docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej.
WALENCJA, WALENCJA_ZWROTNA = _walencja()

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
#: `Subject` wpisany do ciała czoła wpuszcza tam także `Subject → NP`, a wartość
#: osobna dla każdego czoła trzyma rodzinę względną osobno od pytającej.
#: Co bez niej wraca i ile ta etykieta kupuje, wywodzi
#: docs/subset.md#czoło-niesie-etykietę-roli-którą-zajmuje-a-werdyktu-nie-rusza.
BEZ_CZOŁA = "żadne"

#: Wartości cechy `dostawka`, czyli tego, czy za zdaniem składowym coś już stoi.
#: Konstytuent dostawiony za zdanie wypuszcza :data:`DOSTAWKA`, a konstytuent
#: wysunięty przed zdanie żąda :data:`BEZ_DOSTAWKI` od swojego gospodarza, więc
#: wysunięty wchodzi pod dostawiony i nigdy nad niego. Zdanie składowe, które nie
#: ma ani jednego, ani drugiego, cechy tej nie niesie, a cechy nieobecnej
#: unifikacja nie sprawdza, więc żądanie przez takie zdanie przechodzi.
#:
#: Bez tego żądania jeden napis wyprowadza się dwoma kształtami; co je różni, czego
#: nie różni i dlaczego warunek stoi tutaj, wywodzi
#: docs/subset.md#określenie-przed-zdaniem-wchodzi-pod-to-które-stoi-za-nim.
DOSTAWKA = "jest"
BEZ_DOSTAWKI = "brak"

#: Wartości cechy `ciąg`, czyli tego, czy zdanie ma kilka członów współrzędnych.
#: Żąda jej okolicznik zdaniowy dochodzący do całego ciągu, bo bez tego żądania
#: zdanie o jednym członie wyprowadza się dwoma kształtami: raz z okolicznikiem
#: przy członie, raz z tym samym okolicznikiem nad ciągiem, którym ten człon jest.
#:
#: Żądanie jest dodatnie, a cechy nieobecnej unifikacja nie sprawdza, więc cechę
#: wypuszcza każda produkcja `Clause`: ta, która o ciągu przemilczy, wpuści
#: okolicznik nad zdanie pojedyncze. Tym różni się ta cecha od :data:`DOSTAWKA`,
#: której żądanie jest ujemne i której przemilczenie nic nie psuje. Cenę pozycji
#: trzyma
#: docs/subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania.
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
#: docs/subset.md#przydawka-koordynuje-się-i-rozdziela-rzeczownik-tylko-za-nim.
ROZDZIELNA = "jest"
BEZ_ROZDZIELNEJ = "brak"


def zaimek_czoła(liczba: Var, rodzaj: Var) -> dict[str, Var]:
    """Druga para cech czoła zdania względnego: liczba i rodzaj jego zaimka.

    Czoło niesie dwie pary, a rozdziela je to, kto którą czyta. Pierwszą
    (:data:`AGREE`) czyta orzeczenie, bo zgadza się ono z głową czoła, a tę
    poprzednik, bo zgadza się on z zaimkiem. `której przepisy` niesie obie
    różne, a czoło o jednym słowie tę samą dwa razy, i dlatego zmienne wchodzą
    tu argumentem: przy takim czole są to zmienne :data:`AGREE`.

    Czoło, które tej pary nie niesie, zostawia zmienne poprzednika niezwiązane,
    a wtedy zdanie względne wychodzi bez liczby i rodzaju i przyjmuje każdy
    poprzednik. Nazwy cech są polskie, bo cechę tę wybiera ta gramatyka, a nie
    Morfeusz (``olski/morph.py`` nazywa jego kategorie); kto ją czyta, mówi
    docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka.
    """
    return {"liczba_zaimka": liczba, "rodzaj_zaimka": rodzaj}


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
#: Terminal jest osobny, a nie wzięty z `RelativePronoun`: tamten symbol jest grupą
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

#: Przyimek wyrażenia przyimkowego, tego zwykłego i tego, które wysunęło zaimek
#: względny. Nazwany raz, bo oba wykluczają ten sam lemat i wykluczenie ma być w
#: obu to samo (:data:`PRZYIMEK_ROZDZIELAJĄCY`).
PRZYIMEK = word("prep", bez_lematu=PRZYIMEK_ROZDZIELAJĄCY, case=V("c"))

#: Przysłówek w okoliczniku: cała część mowy bez przysłówka względnego. Stopnia
#: nie żąda, bo `teraz` stopnia nie niesie, a `bardzo` niesie `pos`, i oba są
#: okolicznikami zdania.
#:
#: `gdzie` zostaje na zewnątrz z tego samego powodu, z którego pozycji rzeczownej
#: nie mają `kto` i `co` (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`): okolicznikiem zdania
#: oznajmującego ono nie bywa, a wpuszczone tutaj daje każdemu zdaniu z nim
#: czytanie ciągu współrzędnego, w którym `gdzie` określa człon drugi. Czytania
#: tego polszczyzna nie ma, a jest ono jedynym, jakie ta forma dostaje bez
#: własnego ciała (:data:`PRZYSŁÓWEK_WZGLĘDNY`), więc wykluczenie i to ciało
#: wchodzą razem.
PRZYSŁÓWEK = word("adv", bez_lematu=PRZYSŁÓWEK_WZGLĘDNY)

#: Cząstki, które ten rejestr stawia przy zdaniu: `już`, `dopiero`, `także`.
#: Lista jest zamknięta, bo ``part`` niesie całą klasę cząstek naraz, a kryterium
#: na wejście jest jedno: cząstka ma nie mieć czytania, które gramatyka bierze już
#: gdzie indziej. `tylko` go ma — Morfeusz czyta je także jako spójnik, a spójnik
#: bierze koordynacja — więc wpuszczone tutaj dałoby jednemu napisowi dwa
#: wyprowadzenia, i tym samym warunkiem stoi lista spójników przecinkowych obok
#: listy bez przecinka (:data:`SPÓJNIKI_PRZECINKOWE`).
#: Kto zostaje poza listą i z jakiego powodu, wylicza
#: docs/subset.md#cząstka-wchodzi-obu-gospodarzami-a-w-grupie-nie-nosi-etykiety.
CZĄSTKI = frozenset({
    "już", "jeszcze", "dopiero", "także", "również", "nawet", "zarazem", "naprawdę",
    "znowu", "wreszcie", "ponadto", "jedynie", "niemal", "niespełna", "zresztą", "przynajmniej",
})

#: Cząstka w okoliczniku: sama lista i nic więcej, tak samo jak :data:`PRZYSŁÓWEK`
#: bierze samą część mowy.
CZĄSTKA = word("part", lemma=CZĄSTKI)

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
#: docs/subset.md#cząstka-zwrotna-należy-do-swojego-czasownika
#: wywodzi cenę pozycji przedniej i mówi, czego ona nie obejmuje.
SZYKI_CZĄSTKI: tuple[tuple[bool, tuple[Part, ...], tuple[Part, ...]], ...] = (
    (False, (), ()),
    (True, (), (CZĄSTKA_ZWROTNA,)),
    (True, (CZĄSTKA_ZWROTNA,), ()),
)


def _bez_orzecznika(rama: frozenset[str]) -> frozenset[str]:
    """Ta rama bez orzecznika zgodnego, czyli rama zdania, które podmiotu nie ma.

    Orzecznik zgodny zgadza się z podmiotem, więc zdanie bez podmiotu nie ma go z
    czym zgodzić: `Trzeba wolni.` nie jest niczym i `Zgłoszono tania.` też nie.
    Pytają o to obie głowy roli :data:`BEZOSOBOWY`, a każda o inną ramę —
    predykatyw o domyślną (:data:`RAMA_BEZOSOBOWA`), forma nieosobowa o ramę
    swojego lematu — więc odejmowanie jest funkcją, a nie drugą stałą obok nich.
    """
    return rama - {"nom"}


#: Rama predykatywu (:data:`PREDYKATYWY`): domyślna bez orzecznika zgodnego.
#: Wyliczona z domyślnej z tego samego powodu, z którego wylicza się z niej
#: :data:`RAMA_BEZ_BIERNIKA`.
RAMA_BEZOSOBOWA = _bez_orzecznika(RAMA_DOMYŚLNA)

#: Predykatyw: słowo, które orzeka bez podmiotu i bez czasownika, a rządzi tym, co
#: rządziłby czasownik. `Trzeba czytać dokumenty.`, `Widać granicę w odpowiedzi.`,
#: `Wiadomo, że reguła jest tania.`
#:
#: Lista jest zamknięta, bo ``pred`` niesie całą klasę naraz, a kryterium na wejście
#: jest jedno: czytanie konkurujące nie może stanąć na czele zdania tego samego
#: kształtu. Kogo ono zostawia na zewnątrz i za ile, wywodzi
#: docs/subset.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika.
PREDYKATYWY = frozenset({
    "można", "trzeba", "warto", "wiadomo", "widać", "wolno", "słychać", "znać",
})

#: Predykatyw na czele swojego zdania: sama lista i nic więcej, tak samo jak
#: :data:`CZĄSTKA`.
PREDYKATYW = word("pred", lemma=PREDYKATYWY)

#: Przysłówek przy przymiotniku: ta sama część mowy i żądanie stopnia, więc
#: `tu duży` z tej pozycji wypada, a `bardzo duży` zostaje. Terminale są przez to
#: dwa, choć część mowy jedna: warunek należy do jednego gospodarza, a drugi bierze
#: przysłówek każdy. Czym jest żądanie obecności cechy, mówi ``niesione``
#: w olski/grammar.py, a cenę tego warunku trzyma
#: docs/subset.md#naprawę-niesie-tagset-a-formalizm-ją-bierze.
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
#: docs/subset.md#cząstka-trybu-stoi-przy-czasowniku-albo-w-spójniku.
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


def _klasy(zwrotne: bool) -> list[tuple[dict[str, frozenset[str]], frozenset[str], str]]:
    """Klasy walencyjne: warunek na lemat, rama i druga pozycja, którą warunek wpuszcza.

    Ostatnia jest klasa domyślna, i jest nią warunek ujemny na wszystkie lematy
    leksykonu naraz, bo klasy mają się nie zachodzić: forma wzięta dwiema klasami
    byłaby dwoma czytaniami tego samego kształtu.

    Pyta on o formę, a nie o jedno jej czytanie, bo rama jest własnością formy:
    zapytany o czytanie rozdziela lematy zamiast form i wpuszcza ramę domyślną
    formie, której lemat leksykon wymienia. Reprodukcję, cenę i zysk trzyma
    docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej.

    Forma z cząstką ``się`` pyta o swój leksykon, bo jest innym czasownikiem;
    lemat, którego tamten leksykon nie wymienia, bierze ramę domyślną tak samo
    jak każdy inny nieznany, bo cząstkę stawia polszczyzna przy czasowniku
    dowolnym, a Walenty wymienia z niej samą zwrotność zleksykalizowaną.
    Domyślne są przy tym dwie i różni je bezokolicznik, o czym mówi
    :data:`RAMA_DOMYŚLNA_ZWROTNA`.

    Klasa domyślna leksykonu zwrotnego odmawia przy tym kopuli (:data:`KOPULA`), i
    jest to jedyny czasownik, któremu ta gramatyka cząstki odmawia wprost: bez tego
    ``Cena się jest niska.`` się wyprowadza, a ``być się`` czasownikiem nie jest.
    Lematu ``zostać`` odmowa ta nie tyka, bo leksykon zwrotny go wymienia i klasa
    domyślna po niego nie sięga. Cenę i odrzuconą alternatywę trzyma
    docs/subset.md#cząstka-zwrotna-należy-do-swojego-czasownika.

    Klasa ramy dzieli się na dwie tam, gdzie leksykon daje części jej lematów
    drugą pozycję (:data:`DRUGA_CELOWNIK`), a klasa domyślna drugiej pozycji nie
    ma: zdanie o parze mówi o celowniku, więc lemat, który je niesie, stoi w
    leksykonie i tej klasy nie dosięga.
    """
    leksykon = WALENCJA_ZWROTNA if zwrotne else WALENCJA
    z_parą = Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU_ZWROTNE if zwrotne else Z_CELOWNIKIEM_PRZY_WYPEŁNIENIU
    klasy = [
        ({"lemma": wybrane}, rama, druga)
        for rama, lematy in leksykon.items()
        for druga, wybrane in _po_drugiej(lematy, z_parą)
        if wybrane
    ]
    poza_domyślną = (KOPULA if zwrotne else frozenset()).union(*leksykon.values())
    domyślna = RAMA_DOMYŚLNA_ZWROTNA if zwrotne else RAMA_DOMYŚLNA
    return [*klasy, ({"bez_lematu_formy": poza_domyślną}, domyślna, BEZ_DRUGIEJ)]


def _po_drugiej(
    lematy: frozenset[str], z_parą: frozenset[str]
) -> list[tuple[str, frozenset[str]]]:
    """Lematy klasy rozdzielone na te z drugą pozycją i te bez niej."""
    return [(DRUGA_CELOWNIK, lematy & z_parą), (BEZ_DRUGIEJ, lematy - z_parą)]


def _formy_skończone(
    warunek: dict[str, str],
) -> list[tuple[list[Part | Głowa], dict[str, Var | str]]]:
    """Ciała czasownika w formie skończonej, każde wraz z cechami, które ogłasza.

    Czas teraźniejszy i przeszły dzielą trzy ciała, bo osobę niosą inaczej. ``fin``
    niesie osobę i liczbę, a rodzaju nie ma; ``praet`` odwrotnie, więc osoba trzecia
    jest w nim wpisana tutaj, a bez tego ``Ja napisał program.`` się wyprowadza:
    cechy, której konstytuent nie niesie, unifikacja nie sprawdza. Osobę pierwszą
    i drugą wnosi aglutynant, czyli końcówkę, którą Morfeusz odcina od formy —
    ``napisałem`` wchodzi tu jako ``napisał`` i ``em`` — i która liczbę ma tę samą
    co czasownik przy niej.

    Tryb przypuszczający ma dwa ciała i różnią się one od dwóch przeszłych jedną
    cząstką (:data:`CZĄSTKA_TRYBU`): ``odzyskałby`` i ``odzyskałbym``. Dostaje ją
    czas przeszły i on jeden, bo tak stawia tę cząstkę polszczyzna: ``zapisujeby``
    nie jest niczym. Ciała są dwa, a nie jedno z cząstką pominiętą, bo cena trybu
    ma być osobną liczbą, a sonda różnicowa bierze ją zdejmowaniem ciał.

    Tryb wychodzi stąd wartością cechy, bo pyta o niego spójnik, który cząstkę
    niesie sam (:data:`SPÓJNIKI_TRYBU`). Forma na -ł bez cząstki wychodzi z obiema
    wartościami naraz (:data:`TRYB_FORMY_NA_Ł`), a ta sama forma z aglutynantem już
    nie: aglutynant zajmuje miejsce, które pod takim spójnikiem zajmuje jego własna
    końcówka, więc polszczyzna ma ``żebym wiedział``, a nie ``żeby wiedziałem``.

    Czas przyszły ma trzy ciała.
    Forma ``bedzie`` stoi w nich osobno od ``fin``, choć liczbę i osobę niesie
    tak samo, z tego samego powodu, z którego osobno stoi tryb.
    Bezokolicznik nie niesie ani liczby, ani rodzaju,
    więc liczbę ogłasza to ciało samo — bez tego
    ``Programy będzie zapisywać ustawienia.`` się wyprowadza —
    a rodzaju nie żąda nikt.
    Głową jest czasownik, a nie ``bedzie``, bo rama należy do czasownika
    i po nim werdykt nazywa gospodarza przyłączenia.
    Polszczyznę i cenę trzyma
    docs/subset.md#forma-bedzie-orzeka-sama-albo-składa-czas-przyszły-złożony.

    Głowa stoi w każdym ciele, także w tym o jednej części: ciało wychodzi
    stąd do produkcji zwrotnej, która dopisuje mu cząstkę ``się``, a ciało o
    dwóch częściach bez głowy nie powstaje.
    """
    czasownik = word("praet", number=V("n"), gender=V("g"), **warunek)
    aglutynant = word("aglt", number=V("n"), person=V("p"))
    forma_przyszła = word("bedzie", number=V("n"), person=V("p"))
    niedokonany = {"aspect": "imperf"}
    return [
        (
            [Głowa(word({"fin", "impt"}, number=V("n"), person=V("p"), **warunek))],
            {"person": V("p"), "tryb": TRYB_OZNAJMUJĄCY},
        ),
        ([Głowa(czasownik)], {"person": "ter", "tryb": TRYB_FORMY_NA_Ł}),
        ([Głowa(czasownik), aglutynant], {"person": V("p"), "tryb": TRYB_OZNAJMUJĄCY}),
        (
            [Głowa(czasownik), CZĄSTKA_TRYBU],
            {"person": "ter", "tryb": TRYB_PRZYPUSZCZAJĄCY},
        ),
        (
            [Głowa(czasownik), CZĄSTKA_TRYBU, aglutynant],
            {"person": V("p"), "tryb": TRYB_PRZYPUSZCZAJĄCY},
        ),
        (
            [Głowa(word("bedzie", number=V("n"), person=V("p"), **warunek))],
            {"person": V("p"), "tryb": TRYB_OZNAJMUJĄCY},
        ),
        (
            [
                forma_przyszła,
                Głowa(word("praet", number=V("n"), gender=V("g"), **niedokonany, **warunek)),
            ],
            {"person": V("p"), "tryb": TRYB_OZNAJMUJĄCY},
        ),
        (
            [forma_przyszła, Głowa(word("inf", **niedokonany, **warunek))],
            {"person": V("p"), "number": V("n"), "tryb": TRYB_OZNAJMUJĄCY},
        ),
    ]


def _poza_orzeczeniem(szyk: tuple[str, ...]) -> bool:
    """Czy tego szyku zdania nie składa już podmiot z orzeczeniem.

    ``Predicate`` jest czasownikiem wraz z tym, co on bierze, a stoi za podmiotem,
    więc zdanie o szyku podmiot-czasownik-dopełnienie ma wyprowadzenie tamtędy.
    Wypisane płasko drugi raz dałoby jednemu napisowi dwa wyprowadzenia.
    Pozostałych pięciu szyków ``Predicate`` nie składa, bo albo podmiot nie stoi w
    nich pierwszy, albo między nim a czasownikiem coś stoi.
    """
    return szyk[:2] != ("Subject", "Verb")


def _wysunięta_rola(zdanie: Rozwinięcie, symbol: str, czoło: str) -> None:
    """Wpisz zdanie, w którym jedna rola stoi wysunięta na jego czoło.

    Zdanie takie jest zdaniem bez tej roli, którą wysunięty konstytuent zajmuje, i
    dlatego deklarację dostaje tu każda rola, a nie każdy szyk zdania. Czoło stoi
    pierwsze zawsze, bo tak stawia je polszczyzna, i tyle mówi tu warunek
    precedencji; reszta zdania szyk ma swój.

    Ten sam kształt ma zdanie względne — z `który` (`reguła, która rozstrzyga`,
    `ustawa, której przepisy obowiązują`) oraz z `co` (`to, co mogło się zepsuć`) —
    i pytanie (`które zadania mają charakter obowiązkowy`), a różni je samo czoło,
    więc deklaracje powstają raz i biorą czoło nazwą symbolu. Wypisane osobno dla
    każdego czoła rozeszłyby się na pierwszym dopisanym szyku, a rozejście widać
    dopiero na zdaniu, którego jedno z czół nie wyprowadza.

    Role są dwie: podmiot i dopełnienie. Trzeciej — wyrażenia przyimkowego —
    tutaj nie ma, bo wysuwa się ono razem z przyimkiem i z grupą, w której zaimek
    stoi, więc jest czołem innego kształtu; wypisuje je jednym ciałem ta sama
    pętla, która wywołuje tę funkcję.

    Obie te role czoło nosi etykietą, taką samą jak rola wypełniona na swoim
    miejscu, więc funkcja pisze nad czołem `Subject` albo `Object`, a dopiero
    pod nimi zdanie. Po co i jakim kosztem, mówi :data:`BEZ_CZOŁA`.

    Orzeczenie zgadza się z głową czoła, a poprzednik z jego zaimkiem, więc
    orzeczenie bierze ``number`` i ``gender``, a w górę idzie para druga; wywód
    jest przy :func:`zaimek_czoła`. Tyle wystarcza, żeby czołem była grupa,
    a nie sam zaimek.
    """

    def czoło_pierwsze(szyk: tuple[str, ...]) -> bool:
        """Czy czoło stoi w tym szyku pierwsze; o reszcie córek warunek milczy.

        Czoło poznaje się po etykiecie roli, bo pod nią stoi w ciele, a nie pod
        nazwą swojego symbolu. Dopełnienia na swoim miejscu to ciało nie ma,
        więc etykieta wskazuje w nim jedną córkę.
        """
        return szyk[0] == "Object"

    # Osoba i liczba orzeczenia biorą się z czoła, bo ono jest podmiotem; w
    # deklaracji z dopełnieniem biorą się z podmiotu, który stoi obok, i dlatego
    # zmienne liczby oraz rodzaju są tam inne niż zmienne czoła.
    zaimek = zaimek_czoła(V("nz"), V("gz"))
    orzeczenie = nt("Predicate", number=V("n"), gender=V("g"), person="ter")
    podmiot = nt("Subject", number=V("nv"), gender=V("gv"), person=V("p"), czoło=BEZ_CZOŁA)

    # Etykieta roli nad czołem: `Subject` i `Object`, czyli te same nazwy, które
    # zdanie daje rolom wypełnionym na miejscu. Konstytuentem, a nie cechą na
    # czole, bo rolę czyta się z etykiety węzła (``Node.find`` w
    # ``olski/parse.py``), a wpuszcza ją cecha `czoło` (:data:`BEZ_CZOŁA`).
    zdanie.grammar.rule(
        "Subject",
        [nt(czoło, case="nom", number=V("n"), gender=V("g"), **zaimek)],
        czoło=czoło,
    )
    czoło_podmiot = nt("Subject", number=V("n"), gender=V("g"), czoło=czoło, **zaimek)
    zdanie.dominacja(symbol, [czoło_podmiot, Głowa(orzeczenie)], **POPRZEDNIK)

    # Ten sam podmiot wysunięty nad orzeczeniem, w którym dopełnienie stoi przed
    # czasownikiem: `ktoś, kto go nie używa`, `aplikacja, która to napędza`,
    # `Pyta, co olski parsuje.` Szyk ten polszczyzna pisze w zdaniu podrzędnym tak
    # samo jak ten drugi, a zdanie główne miało go od początku, więc bez tego
    # ciała gramatyka mówiła o szyku rzecz nieprawdziwą: że zależy on od tego, czy
    # rola stoi wysunięta.
    #
    # Ciało jest drugie, a nie szyk dopisany do córek wyżej, bo przestawia ono
    # córki orzeczenia, a nie córki zdania; symbol trzyma tę różnicę
    # (:data:`ORZECZENIE_ODWRÓCONE`).
    #
    # Przed czasownik wychodzi samo dopełnienie, a nie całe `Complements`:
    # tamten symbol niesie okolicznik w swoich ciałach, a okolicznik stawia przed
    # czasownikiem także :meth:`Rozwinięcie.dominacja` tutaj, więc `którzy na niej
    # stoją` miałoby dwa wyprowadzenia jednego kształtu.
    orzeczenie_odwrócone = nt(
        ORZECZENIE_ODWRÓCONE, number=V("n"), gender=V("g"), person="ter"
    )
    zdanie.dominacja(symbol, [czoło_podmiot, Głowa(orzeczenie_odwrócone)], **POPRZEDNIK)

    # Podmiot za wysuniętym dopełnieniem stoi po czasowniku i przed nim, bo czoło
    # wysuwa polszczyzna zawsze, a dopełnienie z wyboru
    # (docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka).
    # Wypowiada to sam warunek precedencji: żąda on czoła na pierwszym miejscu i
    # nie żąda niczego od dwóch pozostałych córek.
    #
    # Przypadek czoła rozstrzyga tu przeczenie stojące za nim: `polszczyzna, którą
    # napisał autor` obok `polszczyzna, której nie napisał autor`. Wspólnej zmiennej
    # te dwa nie dostają, bo czoło przypadka nie wybiera — żąda go czasownik —
    # więc para przypadka i wartości cechy stoi wypisana tak samo jak przy
    # dopełnieniu wyżej. Rządzenie sięga tu przez całą resztę zdania składowego, a
    # więc dalej niż gdziekolwiek indziej w tej gramatyce, i tyle też kosztuje:
    # jedna deklaracja rośnie do dwóch. Rozwinięcia szyku to nie dotyka, bo mnoży
    # tu cecha, a nie kolejność.
    for przypadek, negacja in (("acc", "aff"), ("gen", "neg")):
        zdanie.grammar.rule(
            "Object",
            [nt(czoło, case=przypadek, **zaimek)],
            valency="acc",
            negacja=negacja,
            czoło=czoło,
        )
        czoło_dopełnienie = nt(
            "Object", valency="acc", negacja=negacja, czoło=czoło, **zaimek
        )
        czasownik = nt(
            "Verb",
            number=V("nv"),
            gender=V("gv"),
            person=V("p"),
            valency="acc",
            negacja=negacja,
        )
        zdanie.dominacja(
            symbol,
            [czoło_dopełnienie, Głowa(czasownik), podmiot],
            precedencja=czoło_pierwsze,
            **POPRZEDNIK,
        )

        # Podmiot opuszczony: `imprezy, które zorganizował`, `Które zadania
        # wykonuje?` Polszczyzna opuszcza go tu tak samo jak w zdaniu głównym,
        # gdzie deklaracja bez podmiotu stoi obok tej z podmiotem
        # (``ClauseConjunct → Predicate``), więc i tu jest to druga deklaracja.
        # Warunku precedencji nie ma, bo czoło stoi pierwsze, a za nim została
        # jedna córka. Cenę i zakup trzyma
        # docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka.
        zdanie.dominacja(symbol, [czoło_dopełnienie, Głowa(czasownik)], **POPRZEDNIK)

    # Orzecznik wysunięty na czoło: `Czym jest parser?`, `to, czym jest GLR`.
    # Rola jest tu trzecia obok podmiotu i dopełnienia, a pozycję ma jedną, bo
    # narzędnika żąda kopula i nikt poza nią (:data:`KOPULA`), więc szyk jest jeden:
    # czoło, kopula i podmiot, dokładnie jak w zdaniu oznajmującym.
    #
    # Liczby ani rodzaju czoło tu nie niesie, bo orzecznik narzędnikowy z niczym
    # się nie zgadza; kopula zgadza się z podmiotem, który stoi za nią.
    zdanie.grammar.rule(
        "Predicative", [nt(czoło, case="inst", **zaimek)], valency="inst", czoło=czoło
    )
    czoło_orzecznik = nt("Predicative", valency="inst", czoło=czoło, **zaimek)
    kopula = nt("Verb", number=V("nv"), gender=V("gv"), person=V("p"), valency="inst")
    zdanie.dominacja(symbol, [czoło_orzecznik, Głowa(kopula), podmiot], **POPRZEDNIK)


def _zamykane(grammar: Grammar, symbol: str, ciało: list[Part | Głowa], **cechy) -> None:
    """Wpisz ciało zdania podrzędnego i to samo ciało zamknięte przecinkiem.

    Przecinek zamykający stawia polszczyzna wtedy, gdy zdanie nadrzędne biegnie
    dalej, i biegnie ono dalej także spójnikiem: `Dokument mówi, że cena jest
    niska, i liczy cenę.` Bez ciała zamkniętego przecinek ten dochodzi do
    koordynacji, która spójnika przed sobą nie bierze, więc zdanie nie ma ani
    jednego czytania.

    Ciała są dwa, a nie jedno z przecinkiem opcjonalnym, bo opcjonalności ten
    formalizm nie ma. Fakt jest jeden na każde zdanie podrzędne, więc stoi tu raz;
    docs/subset.md wywodzi go pod podrzędnością.
    """
    for domknięcie in ((), (PRZECINEK,)):
        grammar.rule(symbol, [*ciało, *domknięcie], **cechy)


#: Cechy, których symbol nie niesie w górę, choć żąda ich od swojej głowy.
#: Reszta wychodzi z głowy sama (``olski/grammar.py``),
#: więc zgodności nie wypisuje drugi raz żadna produkcja,
#: a wpis tutaj mówi o symbolu to, czego z jego ciał nie widać.
#:
#: Powody są trzy. Zdanie nie niesie liczby, rodzaju, osoby, ramy ani przeczenia
#: swojego czasownika, bo nad zdaniem nie ma z czym ich zgadzać;
#: tak samo czasownik nie niesie aspektu, o który pyta jedno jego ciało
#: (:func:`_formy_skończone`).
#: Rola nie niesie przypadka, bo sama go ustala.
#: Cecha o kształcie wewnątrz konstytuenta — `czoło` wypełnienia,
#: `accommodability` liczebnika, `dostawka` zdania — kończy się na nim.
#:
#: Żadnego z tych wpisów nie widać po werdykcie i nie jest to przypadek:
#: o cechę, którą wpis zatrzymuje, nie pyta nad tym symbolem ani jedna produkcja
#: poza `dostawka`, a nad prozą tego repozytorium gramatyka bez tych wpisów
#: wydaje werdykt i liczbę czytań co do zdania te same.
#: Wpisy zostają, bo cechę wypuszczaną rozdziela las na klasy pozycji
#: (`klasy` w ``olski/parse.py``), więc niesiona bez czytelnika kosztuje rozbiór;
#: zdjęcie ich jest zmianą w gramatyce i pomiaru żąda osobno (TODO.md).
NIE_WYPUSZCZANE = {
    "ClauseConjunct": ("number", "gender", "person", "valency", "negacja", "druga", "dostawka"),
    "Clause": ("dostawka",),
    "Verb": ("aspect",),
    "Predicate": ("valency", "negacja", "druga"),
    ORZECZENIE_ODWRÓCONE: ("valency", "negacja", "druga"),
    "RelativeCore": ("person", "valency", "negacja"),
    "NominalRelativeCore": ("person", "valency", "negacja"),
    "InterrogativeCore": ("person", "valency", "negacja"),
    OKOLICZNIKOWY: ("tryb",),
    ORZEKAJĄCY: ("case", "number"),
    "Subject": ("case",),
    "Object": ("case",),
    "Predicative": ("case",),
    "Modifier": ("case",),
    "RelativeModifier": ("case",),
    "NominalRelativeModifier": ("case",),
    "InterrogativeModifier": ("case",),
    "Complements": ("czoło",),
    "NPConjunct": ("accommodability",),
}


def build() -> Grammar:
    grammar = Grammar(start="Sentence", nie_wypuszczane=NIE_WYPUSZCZANE)

    # Przymiotnik przy rzeczowniku i przymiotnik w orzeczniku, nazwane raz, bo
    # oba wykluczają ten sam lemat i wykluczenie ma być w każdym ciele to samo.
    #
    # Konstytuentem, a nie słowem, bo przysłówek stopniowany przymiotnik określa:
    # `bardzo duży`, `nieporównanie tańsze`. Symbol stawia tę pozycję raz, zamiast
    # dokładać ją do każdego ciała, w którym przymiotnik stoi, i stawia ją pod
    # przymiotnikiem, a nie obok rzeczownika, którego ten przysłówek nie określa.
    # Cenę tego gospodarza trzyma
    # docs/subset.md#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe.
    #
    # Przydawką jest tu także imiesłów, bo stoi on tam, gdzie przymiotnik, i zgadza
    # się tak samo; wywód i cenę trzyma
    # docs/subset.md#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik.
    # Imiesłowy dochodzą dwoma wierszami, a nie jednym terminalem o dwóch częściach
    # mowy, bo cena każdego z nich ma być osobną liczbą. Orzecznik bierze `ppas` i
    # nie bierze `pact`: `Reguła jest sięgająca.` nie jest zdaniem tego rejestru.
    #
    # Imiesłów czynny bierze przy tym cząstkę zwrotną, bo jest formą czasownika,
    # który ją bierze: `program otwierający się`. Wiersz jest osobny i pozycja
    # jedna, za głową, bo tam ją polszczyzna stawia; `program się otwierający`
    # zdaniem tego rejestru nie jest. Bierny jej nie bierze wcale, bo strony
    # biernej czasownik zwrotny nie ma.
    #
    # Bez tego wiersza cząstkę zabiera forma osobowa stojąca za przydawką i
    # `Program otwierający się psuje.` wychodzi jednym czytaniem, z `się psuje`
    # w orzeczeniu, gdzie polszczyzna ma tam dwa: cząstka należy do imiesłowu
    # albo do czasownika, a rozstrzyga o tym znaczenie.
    for symbol, słowo, za in (
        ("AdjectiveConjunct", word("adj", bez_lematu=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE), ()),
        ("AdjectiveConjunct", word("ppas", **AGREE), ()),
        ("AdjectiveConjunct", word("pact", **AGREE), ()),
        ("AdjectiveConjunct", word("pact", bez_lematu_formy=KOPULA, **AGREE), (CZĄSTKA_ZWROTNA,)),
        (
            "PredicativeAdjective",
            word({"adj", "ppas"}, bez_lematu=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE),
            (),
        ),
    ):
        grammar.rule(symbol, [Głowa(słowo), *za])
        grammar.rule(symbol, [PRZYSŁÓWEK_STOPNIA, Głowa(słowo), *za])
    przymiotnik = nt("AdjectiveConjunct", **AGREE)
    orzecznikowy = nt("PredicativeAdjective", **AGREE)

    # Ciąg współrzędny przymiotników przy rzeczowniku: `nowy i tani parser`.
    # Para symboli jest ta sama, co u grupy imiennej, i z tego samego powodu;
    # wywód trzyma docs/subset.md pod „Nothing above a coordination distributes
    # into it”, a cenę każdego ciała
    # docs/subset.md#przydawka-koordynuje-się-i-rozdziela-rzeczownik-tylko-za-nim.
    #
    # Ogon jest nierozdzielny, bo ciąg mieszany — `warstwy nowe i trzecia
    # i czwarta` — polszczyzną nie jest.
    grammar.rule("Adjective", [przymiotnik], rozdzielna=BEZ_ROZDZIELNEJ)
    zgodny_ogon = nt("Adjective", rozdzielna=BEZ_ROZDZIELNEJ, **AGREE)
    grammar.rule(
        "Adjective",
        [Głowa(przymiotnik), SPÓJNIK_BEZ_PRZECINKA, zgodny_ogon],
        rozdzielna=BEZ_ROZDZIELNEJ,
    )
    grammar.rule(
        "Adjective",
        [Głowa(przymiotnik), PRZECINEK, zgodny_ogon],
        rozdzielna=BEZ_ROZDZIELNEJ,
    )
    # Ciąg rozdzielny, czyli ten, którego człony dzielą między siebie rzeczownik:
    # `warstwy trzecia i czwarta` mówi o dwóch warstwach, a `warstwy nowe i tanie`
    # o warstwach, które są jedno i drugie naraz.
    # Liczba idzie wartością, bo żaden człon jej nie ma: mnogi jest ciąg,
    # a każdy przymiotnik w nim pojedynczy.
    rozdzielny_człon = nt("AdjectiveConjunct", case=V("c"), number="sg", gender=V("g"))
    grammar.rule(
        "Adjective",
        [
            Głowa(rozdzielny_człon),
            SPÓJNIK_BEZ_PRZECINKA,
            nt("Adjective", case=V("c"), number="sg", gender=V("g"), rozdzielna=BEZ_ROZDZIELNEJ),
        ],
        number="pl",
        rozdzielna=ROZDZIELNA,
    )
    przydawka = nt("Adjective", **AGREE)
    przydawka_nierozdzielna = nt("Adjective", rozdzielna=BEZ_ROZDZIELNEJ, **AGREE)

    grammar.rule("Sentence", [Głowa(nt("Clause")), KONIEC_ZDANIA])

    # Dwukropek otwierający zdanie: `Cena jest niska: gramatyka jest
    # bezkontekstowa.` Produkcja należy do zdania, a nie do zdania składowego, bo
    # `A, B: C.` czyta się jako `(A, B): C`, a na poziomie `Clause` byłaby
    # prawostronnie rekurencyjna razem z przecinkiem i wypuszczała `A, (B: C)`.
    #
    # Niezmiennik — że jednoznaczności nie odbiera ani jedno z tych ciał —
    # pilnuje tests/test_subset.py, a wywód wraz z zakupem trzyma
    # docs/subset.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają.
    # Ciała są trzy, a nie jedno biorące trzy znaki, bo zakup każdego z nich jest
    # osobną liczbą i sonda bierze ją zdejmowaniem ciał.
    for znak in (DWUKROPEK, ŚREDNIK, MYŚLNIK):
        grammar.rule("Sentence", [Głowa(nt("Clause")), znak, nt("Clause"), KONIEC_ZDANIA])

    # Grupa imienna za dwukropkiem, tam gdzie trzy ciała wyżej żądają zdania:
    # `Warstwa pyta o dwa typy: Zdanie oraz Kontekst.`, `Gramatyka ma dwie role:
    # podmiot i dopełnienie.` Rejestr wylicza tak to, co zdanie przed dwukropkiem
    # nazwało liczbą albo terminem, a wylicza jednym ciągiem współrzędnym, więc
    # grupa bierze tę pozycję cała.
    #
    # Ciało jest osobne, a nie symbolem obejmującym zdanie i grupę, bo cena
    # każdego z nich jest osobną liczbą. Drugiego czytania nie daje żadnemu
    # napisowi, bo grupa imienna zdaniem nie jest, i to pilnuje tests/test_subset.py.
    #
    # Myślnik i średnik tej pozycji nie dostają, bo ten rejestr nie pisze za nimi
    # samej grupy: myślnikiem wtrąca całe zdanie, a średnikiem rozdziela dwa.
    grammar.rule(DOPOWIEDZIANY, [DWUKROPEK, Głowa(nt("NP"))])
    grammar.rule("Sentence", [Głowa(nt("Clause")), nt(DOPOWIEDZIANY), KONIEC_ZDANIA])

    # To, co człon może zawierać, rozstrzyga,
    # do czego koordynację da się przyłączyć z zewnątrz,
    # i na tym stoi zawężenie zasięgu, a nie na kształcie tych produkcji.
    # X → X conj X powiedziałoby to samo o zasięgu
    # i tablica Earleya bierze taką produkcję bez skargi,
    # a różni je liczba czytań ciągu współrzędnego; TODO.md trzyma ten wybór.
    # Symbol wspólny na spójnik i na przecinek powiedziałby to samo raz,
    # ale przecinek przestałby stać przy swoim poziomie,
    # a cena i zakup każdego z czterech poziomów są osobnymi liczbami,
    # które wzięto zdejmowaniem po jednej.
    # Zasięg koordynacji wywodzi docs/subset.md pod „Nothing above a
    # coordination distributes into it”.
    #
    # Tryb ciąg wypuszcza z członu pierwszego, a od pozostałych nie żąda niczego,
    # i jest to ta sama granica: spójnik trybu nad ciągiem żąda formy na -ł od
    # członu, którym ten ciąg jest, a nie od każdego z osobna. Zmienna wspólna
    # żądałaby jej od wszystkich i zabierałaby przy tym zdania już przyjęte, bo
    # `Program zapisuje ustawienia, a linter sprawdziłby tekst.` koordynuje tryb
    # oznajmujący z przypuszczającym.
    człon = nt("ClauseConjunct", tryb=V("t"))
    grammar.rule("Clause", [człon], ciąg=BEZ_CIĄGU)
    grammar.rule("Clause", [Głowa(człon), SPÓJNIK_BEZ_PRZECINKA, nt("Clause")], ciąg=CIĄG)
    grammar.rule("Clause", [Głowa(człon), PRZECINEK, nt("Clause")], ciąg=CIĄG)
    # Przecinek i spójnik naraz, czyli ta interpunkcja, której polszczyzna żąda
    # przed `ale`, `a` i `więc` (:data:`SPÓJNIKI_PRZECINKOWE`). Poziom zdaniowy
    # ma tę pozycję, a imienny i przymiotnikowy nie, bo lista tych spójników jest
    # listą spójników zdaniowych: `nie polszczyzny, a dziedziny` jest w niej
    # elipsą, a nie ciągiem współrzędnym dwóch grup imiennych.
    grammar.rule("Clause", [Głowa(człon), PRZECINEK, SPÓJNIK_PRZECINKOWY, nt("Clause")], ciąg=CIĄG)

    # Części zdania, nazwane raz, bo każda z nich stoi w kilku szykach naraz.
    # Zmienna cechy jest zakresu produkcji, więc dwie produkcje biorące ten sam
    # obiekt mówią dalej każda o swojej zgodności.
    #
    # Cechę, której żąda się tu od głowy, konstytuent niesie w górę sam
    # (``olski/grammar.py``).
    #
    # Rodzaj przechodzi przez każdy szyk, bo żąda go czas przeszły, i dlatego
    # podmiot jest tu jeden zamiast dwóch; wywód trzyma
    # docs/subset.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku,
    # a niezmiennik pilnuje test w tests/test_subset.py.
    #
    # Tryb przechodzi przez każdy szyk tą samą drogą i z tego samego powodu: żąda
    # go spójnik, który cząstkę tego trybu niesie sam (:data:`SPÓJNIKI_TRYBU`), a
    # cechy, której konstytuent nie niesie, unifikacja nie sprawdza, więc szyk,
    # który by trybu nie przepuścił, przepuściłby pod taki spójnik każdy tryb.
    podmiot = nt("Subject", number=V("n"), gender=V("g"), person=V("p"), czoło=BEZ_CZOŁA)
    orzeczenie = nt("Predicate", number=V("n"), gender=V("g"), person=V("p"), tryb=V("t"))
    czasownik = nt("Verb", number=V("n"), gender=V("g"), person=V("p"), tryb=V("t"))
    okoliczniki = nt("Adjuncts")

    # Walencja jest wspólną zmienną, tak jak zgodność: czasownik wypuszcza z
    # siebie swoją ramę, dopełnienie mówi, którą pozycję ramy zajmuje, a
    # unifikacja przecina jedno z drugim. Czasownik, przy którym nic nie stoi,
    # ramy nie ogłasza nikomu i stoi tu bez niej.
    #
    # Negacja jedzie tą samą drogą i rządzi tym samym: przypadkiem grupy, którą
    # czasownik bierze. Czasownik ogłasza, czy przeczy, dopełnienie mówi, przy
    # jakim przeczeniu stoi. Zgodnością to nie jest — rządzenie nie jest ani
    # symetryczne, ani lokalne — więc dlaczego kanał cech ją mimo to bierze,
    # wywodzi docs/design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne.
    czasownik_ramy = nt(
        "Verb",
        number=V("n"),
        gender=V("g"),
        person=V("p"),
        valency=V("w"),
        negacja=V("z"),
        druga=V("d"),
        tryb=V("t"),
    )
    dopełnienie = nt("Object", valency=V("w"), negacja=V("z"), czoło=BEZ_CZOŁA)
    orzecznik_ramy = nt(
        "Predicative", number=V("n"), gender=V("g"), valency=V("w"), czoło=BEZ_CZOŁA
    )
    orzecznik_wysunięty = nt("Predicative", number=V("n"), gender=V("g"), czoło=BEZ_CZOŁA)

    # Orzecznik zgodny, wraz z żądaniem, które stawia czasownikowi. Dwa razy
    # ``nom``, a nie wspólna zmienna, bo rama nie zastępuje pozycji: wspólna
    # zmienna wpuszcza tu kopulę z narzędnikiem. Co ona wtedy przyjmuje nad
    # Składnicą, mierzy docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej.
    orzecznik = nt("Predicative", valency="nom", number=V("n"), gender=V("g"))
    czasownik_orzecznika = nt(
        "Verb", number=V("n"), gender=V("g"), person=V("p"), valency="nom", tryb=V("t")
    )

    # Kopula po zwinięciu jej w ramę: czasownik, który bierze orzecznik w
    # narzędniku. Osobnego symbolu nie ma, bo rama mówi to samo, a jeden lemat
    # wychodził spod dwóch nazw. Żądanie jest tu na czasowniku, a nie wspólną
    # zmienną z orzecznikiem, i to jest ta sama cena co wyżej.
    kopula = nt("Verb", number=V("n"), gender=V("g"), person=V("p"), valency="inst", tryb=V("t"))

    # Czasownik, który bierze bezokolicznik: `może`, `musi`, `chce`. Pozycja `inf`
    # stoi tu wartością, żeby zmienna ramy została wolna dla dopełnienia, które ten
    # bezokolicznik bierze (:data:`BEZOKOLICZNIK_OTWARTY`).
    czasownik_bezokolicznika = nt(
        "Verb",
        number=V("n"),
        gender=V("g"),
        person=V("p"),
        valency="inf",
        negacja=V("z"),
        tryb=V("t"),
    )

    # Zdanie deklaruje córki, a kolejność, w jakiej one stoją, deklaruje osobno
    # warunek precedencji nad nimi; rozwinięcie składa jedno z drugim przed
    # rozbiorem (:mod:`olski.precedencja`). Tablica Earleya dostaje przez to
    # ciała wypisane, bo rozwinięcie kończy się przed nią, a rodzina mnożąca się
    # przez szyk i przez miejsca na okolicznik ma sześć deklaracji na kilkadziesiąt
    # ciał.
    #
    # Miejsce na okolicznik wylicza to samo rozwinięcie i przez to nie ma go jak
    # zapomnieć w jednym z ciał: przyłączenie wyrażenia przyimkowego olski oddaje
    # czytelnikowi, więc każde miejsce, w którym grupa imienna takie wyrażenie
    # bierze, musi umieć oddać je też zdaniu. Pozycji brakującej nie widać po
    # zdaniu odrzuconym, tylko po przyjętym: wychodzi ono jednym czytaniem, bo
    # drugie nie miało gdzie się wyprowadzić. docs/subset.md trzyma wywód i cenę.
    #
    # Osoba bierze się z podmiotu, a nie stoi na trzeciej, i to jest to, co
    # wpuszcza zaimek pierwszej i drugiej osoby. Grupa imienna z rzeczownikiem w
    # głowie mówi person=ter sama, więc rozkaźnik dalej takiej nie weźmie.
    zdanie = Rozwinięcie(grammar, okolicznik=okoliczniki, własny_okolicznik=("Predicate",))
    zdanie.dominacja("ClauseConjunct", [podmiot, Głowa(orzeczenie)])

    zdanie.dominacja("ClauseConjunct", [nt("Predicate", tryb=V("t"))])

    # Mianownika pojedynczego żąda ten terminal, bo tyle mówi o tej konstrukcji
    # polszczyzna: zwrot ma jedną formę, a każda inna forma tego lematu stoi pod
    # czasownikiem — `nie ma mowy` — i zdaniem tej produkcji nie jest. Dwie cechy,
    # a nie sam przypadek: `mowy` jest u Morfeusza i dopełniaczem pojedynczym, i
    # mianownikiem mnogim, więc warunek na sam przypadek wpuszcza `o których mowy`.
    # Rodzaju nie żąda, bo zgodzić się ten rzeczownik nie ma z czym.
    grammar.rule(
        ORZEKAJĄCY,
        [Głowa(word("subst", lemma=RZECZOWNIK_ORZEKAJĄCY, case="nom", number="sg"))],
    )

    # Zdanie składowe, w którym ten rzeczownik orzeka. Okolicznik stoi w nim córką
    # żądaną, a nie miejscem wyliczonym, bo kopuła opuszczona żąda tego, o czym
    # mowa, i dlatego rozwinięcie szyku tej deklaracji nie pisze: pisałoby ciało
    # bez okolicznika razem z nim.
    #
    # Ciało drugie stoi pod czołem zdania względnego niżej, bo tam to wyrażenie
    # jest wysunięte. Co zdjęcie któregoś z dwóch kosztuje, mierzy
    # docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną.
    grammar.rule("ClauseConjunct", [Głowa(nt(ORZEKAJĄCY)), okoliczniki], tryb=TRYB_OZNAJMUJĄCY)

    # Głowa, która orzeka bez podmiotu: predykatyw i forma nieosobowa czasownika.
    # Rama i `Complements` są u obu te same, co u czasownika, a różni je to, skąd
    # rama przychodzi: predykatyw ma jedną wpisaną obok listy lematów, a forma
    # nieosobowa bierze ramę swojego lematu tak samo jak forma osobowa
    # (:func:`_klasy`). Orzecznika zgodnego nie ma żadna z tych dwóch ram, bo
    # zgadzać się on nie ma z czym (:func:`_bez_orzecznika`).
    # Cząstka `się` stoi przy formie nieosobowej tak samo jak przy osobowej i pyta
    # o ten sam leksykon zwrotny: `zajmowano się sprawą` jest tym samym
    # czasownikiem co `zajmuje się sprawą`.
    #
    # Wywody trzymają
    # docs/subset.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika oraz
    # docs/subset.md#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu.
    for przeczenie, negacja in PRZECZENIA:
        grammar.rule(
            BEZOSOBOWY,
            [*przeczenie, Głowa(PREDYKATYW)],
            valency=RAMA_BEZOSOBOWA,
            negacja=negacja,
            druga=BEZ_DRUGIEJ,
        )
        for zwrotne, cząstka in ((False, ()), (True, (CZĄSTKA_ZWROTNA,))):
            for warunek, rama, druga in _klasy(zwrotne):
                grammar.rule(
                    BEZOSOBOWY,
                    [*przeczenie, Głowa(word("imps", **warunek)), *cząstka],
                    valency=_bez_orzecznika(rama),
                    negacja=negacja,
                    druga=druga,
                )

    # Zdaniem składowym jest ta głowa wprost, bo `Predicate` ma ciało z podmiotem,
    # którego to zdanie nie ma. Ciała są dwa, a nie jedno, bo zakup ciała bez
    # wypełnienia — `Nie wiadomo.`, `Zgłoszono.` — jest osobną liczbą;
    # `Complements` pustego ciała nie ma, a dodane tam dawałoby je każdemu
    # czasownikowi naraz.
    grammar.rule(
        "ClauseConjunct",
        [
            Głowa(nt(BEZOSOBOWY, valency=V("w"), negacja=V("z"), druga=V("d"))),
            nt("Complements", valency=V("w"), negacja=V("z"), druga=V("d")),
        ],
        tryb=TRYB_OZNAJMUJĄCY,
    )
    grammar.rule("ClauseConjunct", [nt(BEZOSOBOWY)], tryb=TRYB_OZNAJMUJĄCY)

    # Dopełnienie przed głową, która orzeka bez podmiotu: `Usterkę zgłoszono.`
    # Córką zdania, a nie wewnątrz `Complements`: tamten symbol stoi w ciele wyżej
    # za głową i tylko tam, a córka zdania dostaje miejsce na okolicznik wyliczone,
    # więc `Usterkę zgłoszono wczoraj` zostawia okolicznik za głową.
    # docs/subset.md#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu
    zdanie.dominacja(
        "ClauseConjunct",
        [dopełnienie, Głowa(nt(BEZOSOBOWY, valency=V("w"), negacja=V("z")))],
        tryb=TRYB_OZNAJMUJĄCY,
    )

    # Podmiot, dopełnienie i czasownik w każdym szyku, jaki polszczyzna ma, poza
    # tym jednym, który składa podmiot z orzeczeniem (:func:`_poza_orzeczeniem`).
    # Szyk spoza olskiego ma być wykluczony warunkiem, a nie brakiem produkcji,
    # bo wykluczenia przez przemilczenie zabrania tej gramatyce
    # docs/design-notes.md#angle-one-parsing, i wykluczony jest tu jeden szyk,
    # który ten warunek wypowiada.
    zdanie.dominacja(
        "ClauseConjunct",
        [podmiot, dopełnienie, Głowa(czasownik_ramy)],
        precedencja=_poza_orzeczeniem,
    )

    # Dopełnienie przed czasownikiem, którego podmiot jest opuszczony: `Cenę
    # liczymy.`, `Ustawienia zapisujemy.` Polszczyzna opuszcza podmiot w każdym
    # szyku, a nie w tym jednym, w którym za czasownikiem nic nie stoi; ten
    # rejestr mówi tym szykiem o swoich konwencjach (CLAUDE.md).
    #
    # Szyku odwrotnego ta deklaracja nie ma z tego samego powodu, dla którego nie
    # ma go deklaracja z podmiotem (:func:`_poza_orzeczeniem`): czasownik wraz z
    # dopełnieniem za nim składa `Predicate`, a zdanie bez podmiotu jest nim samym.
    zdanie.dominacja("ClauseConjunct", [dopełnienie, Głowa(czasownik_ramy)])

    # Dopełnienie bezokolicznika, wysunięte przed formę osobową, która ten
    # bezokolicznik bierze: `premier większości nie może ruszyć`. Wywód i cenę trzyma
    # docs/subset.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze.
    #
    # Dopełnienie wchodzi tu tym samym symbolem, co w szykach bez bezokolicznika, i
    # dzieli z nimi obie swoje zmienne. Ramę czyta jednak nie forma osobowa, a
    # bezokolicznik, bo pozycja, którą to dopełnienie zajmuje, jest w jego ramie;
    # przeczenie odwrotnie, bo dopełniacza żąda cząstka stojąca przy formie osobowej
    # (docs/subset.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem).
    #
    # Szyk jest jeden, ten wypisany, bo cena każdego jest osobną liczbą, a ten
    # jeden jest szykiem, którego żąda bank drzew.
    zdanie.dominacja(
        "ClauseConjunct",
        [
            podmiot,
            dopełnienie,
            Głowa(czasownik_bezokolicznika),
            nt(BEZOKOLICZNIK_OTWARTY, wysunięte=V("w")),
        ],
    )

    # Czasownik przed podmiotem: Nadchodzi druga rewolucja, Są oni obdarzeni
    # rozumem. Podmiot nie bierze tu własnych dopełnień, więc Zapisuje program
    # ustawienia się nie wyprowadza i żadne zdanie SVO nie konkuruje z czytaniem
    # samego siebie od czasownika. Szyku odwrotnego te dwie deklaracje nie mają
    # z tego samego powodu co deklaracja wyżej.
    zdanie.dominacja("ClauseConjunct", [Głowa(czasownik), podmiot])
    zdanie.dominacja("ClauseConjunct", [Głowa(czasownik_orzecznika), podmiot, orzecznik])

    # Predykatyw przed swoją kopulą: Wejściem jest zwykły tekst polski, W metodzie
    # Cieszyńskiej najważniejsza jest rozmowa. Lustro reguły OVS, którego
    # predykatyw nie miał, więc ten sam szyk wychodził raz tak, a raz wcale,
    # zależnie od tego, co po czasowniku stoi. Orzecznik stoi tu otwarty, bo oba
    # szyki bank drzew ma, a kopula trzyma ten szyk przy orzeczniku: żądanie
    # narzędnika postawione czasownikowi jest tym, co w tej gramatyce znaczy
    # „kopula”, i wysunięcie należy do niej także wtedy, gdy orzecznik jest zgodny.
    #
    # Warunku precedencji nie dostaje ani ta deklaracja, ani ta nad nią, bo różni
    # je rama, a nie kolejność: kopula żąda narzędnika, a czasownik orzecznika
    # zgodnego żąda mianownika, więc przestawiona jedna z nich wypisałaby szyk,
    # który ma już druga, i jednemu napisowi dałaby dwa wyprowadzenia.
    zdanie.dominacja("ClauseConjunct", [orzecznik_wysunięty, Głowa(kopula), podmiot])

    # Wtrącenie w nawiasie: `Zdanie stoi (docs/subset.md).`, `Cena jest zerowa
    # (niżej).` Wnętrzem jest grupa imienna albo przysłówek, bo tym są te
    # dopowiedzenia: nazwą dokumentu i wskazaniem, gdzie szukać. Przysłówek wchodzi
    # tu terminalem, a nie symbolem swojej roli, bo okolicznikiem zdania w nawiasie
    # nie jest.
    #
    # Pozycje są dwie i żaden napis nie ma ich obu naraz: nawias zamykający zdanie
    # składowe stoi tutaj, a nawias zamykający zdanie względne przed jego
    # przecinkiem stoi w ciele `RelativeClause` niżej. Zdanie z nawiasem ma przez
    # to jedno czytanie, a nie tyle, ile gospodarzy ma wyrażenie przyimkowe.
    # Dlaczego wolno tu wybrać jedno miejsce, a przy wyrażeniu przyimkowym nie
    # wolno, i co obie pozycje zostawiają na zewnątrz, wywodzi
    # docs/subset.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania.
    for wnętrze in (nt("NP"), PRZYSŁÓWEK):
        grammar.rule(WTRĄCONY, [NAWIAS_OTWIERAJĄCY, Głowa(wnętrze), NAWIAS_ZAMYKAJĄCY])

    # Człon bez czasownika (:data:`ELIPSA`). Wypełnieniem jest konstytuent, który
    # zajmuje w zdaniu pozycję, a ciała są osobne, po jednym na wypełnienie, bo
    # cena każdego z nich jest osobną liczbą. Przysłówka wśród nich nie ma, bo
    # zmierzono go i nie wyszedł
    # (docs/subset.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze).
    #
    # Cząstka przecząca stoi w ciele parą, bo ten rejestr pisze oba: `a nie
    # zdanie` i `czyli o obiekt`. Dopełniaczem nie rządzi i nie ma czym, bo
    # czasownika pod nią nie ma, więc cechy ``negacja`` to ciało nie niesie.
    #
    # Zdanie nadrzędne biegnie za tym członem — `a nie przypadkiem, i pilnuje go
    # test` — więc przecinek zamykający dokłada :func:`_zamykane`, tak samo jak
    # zdaniom podrzędnym.
    for wnętrze in (nt("NP"), nt("AP"), nt("Modifier")):
        for przeczenie in ((), (PRZECZENIE,)):
            _zamykane(grammar, ELIPSA, [PRZECINEK, SPÓJNIK_ELIPSY, *przeczenie, Głowa(wnętrze)])

    # Oba te konstytuenty dostawiają się do zdania składowego jednym ciałem, bo
    # oba są tym samym: grupą postawioną obok zdania i nazwaną całym napisem.
    # Pętla trzyma je zgodnymi — pozycja dopisana jednemu dochodzi i drugiemu —
    # a osobne ciała dałyby się rozejść po pierwszej takiej pozycji.
    for dostawiony in (WTRĄCONY, ELIPSA):
        grammar.rule(
            "ClauseConjunct",
            [Głowa(nt("ClauseConjunct", tryb=V("t"))), nt(dostawiony)],
            dostawka=DOSTAWKA,
        )

    # Okolicznik wysunięty przed zdanie. Polszczyzna określa rzeczownik wyrażeniem
    # przyimkowym tylko od tyłu, więc przed zdaniem nie ma rzeczownika, do którego
    # to wyrażenie mogłoby się przyłączyć, i wieloznaczności przyłączenia tu nie ma.
    #
    # Przysłówek dostaje tu ciało wypisane, a nie listę okoliczników, bo `Adjuncts`
    # w tym miejscu dałoby wyrażeniu przyimkowemu drugie wyprowadzenie tego samego
    # kształtu, czyli czytanie, którego nie ma czym odsiać.
    grammar.rule(
        "ClauseConjunct",
        [nt("Modifier"), Głowa(nt("ClauseConjunct", tryb=V("t"), dostawka=BEZ_DOSTAWKI))],
    )
    for przy_zdaniu in (PRZYSŁÓWKOWY, CZĄSTKOWY):
        grammar.rule(
            "ClauseConjunct",
            [nt(przy_zdaniu), Głowa(nt("ClauseConjunct", tryb=V("t"), dostawka=BEZ_DOSTAWKI))],
        )

    grammar.rule(
        "Subject",
        [nt("NP", case="nom", number=V("n"), gender=V("g"), person=V("p"))],
        czoło=BEZ_CZOŁA,
    )
    # Zdanie względne bez poprzednika w roli podmiotu: `Kto wchodzi w środek,
    # poprzedniego zdania nie przeczytał.`, `Kto chce liczby dzisiejszej, puszcza
    # narzędzie.` Poprzednika ta konstrukcja nie ma i nie potrzebuje, bo zaimek
    # sam nazywa to, o czym zdanie orzeka, a orzeczenie zgadza się z nim: liczbę i
    # rodzaj wypuszcza więc ten podmiot z rdzenia, którego głową jest jego zaimek.
    #
    # Przecinek stoi w ciele podmiotu, a nie między nim a orzeczeniem, bo zamyka
    # on zdanie względne, tak samo jak w :func:`_zamykane`; osoba jest trzecia,
    # bo zaimek jest zaimkiem trzeciej osoby.
    #
    # Bez wykluczenia z pozycji rzeczownej (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`)
    # konstrukcja ta wyprowadza się ciągiem współrzędnym, którego podmiotem jest
    # ten zaimek, więc pozycja stoi w gramatyce razem z tamtym wykluczeniem.
    grammar.rule(
        "FreeRelativeClause",
        [Głowa(nt("NominalRelativeCore", number=V("n"), gender=V("g"))), PRZECINEK],
    )
    grammar.rule(
        "Subject",
        [Głowa(nt("FreeRelativeClause", number=V("n"), gender=V("g")))],
        person="ter",
        czoło=BEZ_CZOŁA,
    )
    # Dopełnienie wychodzi z pozycją ramy, którą zajmuje, bo tym jest przypadek,
    # który czasownik rządzi: żądanie wobec czasownika stoi więc raz, tutaj, a nie
    # w każdym szyku, w którym dopełnienie stoi.
    #
    # Dopełniacz negacji zajmuje tę samą pozycję ramy, więc jest drugą produkcją
    # dopełnienia, a nie drugą pozycją. Wartość cechy jest tu wypisana, a nie
    # zmienna, bo o przypadku rozstrzyga właśnie ta produkcja.
    grammar.rule("Object", [nt("NP", case="acc")], valency="acc", negacja="aff", czoło=BEZ_CZOŁA)
    grammar.rule("Object", [nt("NP", case="gen")], valency="acc", negacja="neg", czoło=BEZ_CZOŁA)

    # Dopełnienie w przypadku, którego żąda sam czasownik: `Parser mówi autorowi.`,
    # `Wpis żąda dowodu.` Pozycja jest tu ta sama co wyżej, a różni ją przypadek i
    # to, że wpuszcza ją leksykon, a nie rama domyślna (:data:`DOKŁADANE`), więc
    # forma w celowniku stoi przy tych czasownikach, którym Walenty celownik daje,
    # i nie stoi przy żadnym innym.
    #
    # Przeczenia te dwa ciała nie ogłaszają i nie mają czego: dopełniacz negacji
    # wchodzi w miejsce biernika i tam kończy się jego zasięg
    # (docs/subset.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem),
    # a `nie mówi autorowi` stoi w celowniku tak samo jak `mówi autorowi`. Cechy,
    # której konstytuent nie niesie, unifikacja nie sprawdza, więc oba przypadki
    # stoją przy przeczeniu i bez niego.
    #
    # Dopełniacz z leksykonu i dopełniacz z przeczenia dają jednemu napisowi dwa
    # wyprowadzenia tam, gdzie czasownik bierze oba — `nie żąda dowodu` — a jedno
    # czytanie, bo kształt mają ten sam
    # (docs/subset.md#co-się-liczy-jako-jedno-odczytanie).
    for przypadek, _lematy, _zwrotne in DOKŁADANE:
        grammar.rule("Object", [nt("NP", case=przypadek)], valency=przypadek, czoło=BEZ_CZOŁA)

    # To, co czasownik bierze, jest jednym symbolem, a nie listą ciał, żeby forma
    # osobowa i bezokolicznik niżej dzieliły ją, zamiast nieść każde swoją kopię.
    dopełnienia = nt(
        "Complements",
        number=V("n"),
        gender=V("g"),
        valency=V("w"),
        negacja=V("z"),
        druga=V("d"),
    )
    grammar.rule("Predicate", [czasownik])
    grammar.rule("Predicate", [Głowa(czasownik_ramy), dopełnienia])

    # To samo orzeczenie z dopełnieniem przed czasownikiem: `kto go nie używa`,
    # `która to wszystko napędza`. Symbol jest osobny od `Predicate`, a nie drugim
    # jego ciałem, i rozstrzyga o tym zdanie główne: ono ma ten szyk już z
    # deklaracji swoich córek (:meth:`Rozwinięcie.dominacja`), więc ciało dopisane
    # tam dałoby `Reguła tekst sprawdza.` drugie wyprowadzenie tego samego
    # kształtu. Bierze go zdanie, którego czoło jest podmiotem, i ono jedno
    # (:func:`_wysunięta_rola`).
    grammar.rule(
        ORZECZENIE_ODWRÓCONE,
        [dopełnienie, Głowa(czasownik_ramy)],
        druga=BEZ_DRUGIEJ,
    )

    # `winien` odmienia się przez rodzaj, a nie przez osobę, więc zdanie, którego
    # jest głową, zgadza się z podmiotem rodzajem, a osobę zostawia temu, co ją
    # zawęża gdzie indziej.
    #
    # Tryb stoi tu wypisany, bo `winien` cząstki trybu nie bierze: `żeby powinien`
    # nie jest polszczyzną, a cechy, której konstytuent nie niesie, unifikacja nie
    # sprawdza, więc orzeczenie milczące o trybie przeszłoby pod każdy spójnik.
    for przeczenie, negacja in PRZECZENIA:
        grammar.rule(
            "Predicate",
            [
                *przeczenie,
                Głowa(word("winien", number=V("n"), gender=V("g"))),
                nt("InfinitivePhrase", negacja=negacja),
            ],
            tryb=TRYB_OZNAJMUJĄCY,
        )
    # Fraza bezokolicznikowa niesie pozycję ramy, którą zajmuje, tak samo jak
    # dopełnienie i orzecznik, więc żądanie wobec czasownika stoi raz, na niej, a
    # nie w każdym ciele, w którym stoi ona. Łańcuch nie potrzebuje przy tym
    # własnej produkcji, bo InfinitivePhrase → inf Complements wraca do ciał niżej
    # i ma pomagać pisać wychodzi z tych dwóch.
    #
    # Cząstka zwrotna stoi przy tej głowie tak samo jak przy formie osobowej
    # (:data:`SZYKI_CZĄSTKI`), bo należy do czasownika, a nie do formy, w jakiej on
    # stoi. Klasy walencyjnej to ciało nie pyta, bo dopełnienia nie ma i rama nie ma
    # tu czego licencjonować, więc z leksykonu zwrotnego zostaje sama odmowa kopuli:
    # `być się` czasownikiem nie jest w żadnej formie.
    for zwrotne, przed, za in SZYKI_CZĄSTKI:
        głowa = word("inf", bez_lematu_formy=KOPULA) if zwrotne else word("inf")
        for przeczenie, _ in PRZECZENIA:
            grammar.rule(
                "InfinitivePhrase", [*przed, *przeczenie, Głowa(głowa), *za], valency="inf"
            )

    # Zdanie podrzędne dopełnieniowe: `pomiar mówi, że poziom odpowiada`. Pozycję
    # ramy niesie ono tak samo jak dopełnienie i bezokolicznik wyżej,
    # a przecinek zamykający dokłada :func:`_zamykane`.
    _zamykane(
        grammar,
        "SubordinateClause",
        [PRZECINEK, word("comp", lemma=SPÓJNIK_DOPEŁNIENIOWY), Głowa(nt("Clause"))],
        valency="comp",
    )

    # Okolicznik wyrażony zdaniem: `Program zapisuje ustawienia, gdy linter
    # sprawdza tekst.` i `Gdy linter sprawdza tekst, program zapisuje ustawienia.`
    # Konstrukcja jest okolicznikiem, a nie pozycją ramy, i tym różni się od
    # zdania z `że`: czasownik jej nie żąda i nie ma czasownika, który by jej
    # zabraniał, więc dochodzi ona do zdania, a nie do jego orzeczenia
    # (docs/subset.md#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej).
    #
    # Przecinek należy do tego konstytuentu, tak samo jak w zdaniu dopełnieniowym
    # i względnym, i po tym poznaje ciąg współrzędny werdykt oraz sonda
    # (docs/subset.md#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja).
    # Stoi on po tej stronie zdania podrzędnego, po której stoi zdanie nadrzędne,
    # więc cecha `pozycja` wiąże ciało z miejscem: bez niej ciało z przecinkiem
    # z przodu staje na czele zdania i olski wyprowadza napis zaczynający się
    # przecinkiem, którego nikt nie napisał.
    #
    # Spójnik jest w obu ciałach inny, bo wysunięcie jest faktem o słowie:
    # ciało za zdaniem bierze każdy z listy, a ciało przed zdaniem tylko te,
    # których zdanie polszczyzna wysuwa (:data:`SPÓJNIKI_WYSUWANE`).
    #
    # Przecinek zamykający dostaje ciało za zdaniem (:func:`_zamykane`), a ciało
    # przed zdaniem go nie dostaje, bo już go niesie: zdanie nadrzędne biegnie za
    # nim zawsze.
    _zamykane(
        grammar,
        OKOLICZNIKOWY,
        [PRZECINEK, word("comp", lemma=SPÓJNIKI_OKOLICZNIKOWE), Głowa(nt("Clause"))],
        pozycja="za",
    )
    grammar.rule(
        OKOLICZNIKOWY,
        [word("comp", lemma=SPÓJNIKI_WYSUWANE), Głowa(nt("Clause")), PRZECINEK],
        pozycja="przed",
    )

    # Ten sam okolicznik otwarty przysłówkiem względnym (:data:`PRZYSŁÓWEK_WZGLĘDNY`),
    # a nie spójnikiem: `Wchodzi w roadmap.md, gdzie każdy etap ma kryterium wyjścia.`
    # Ciało jest osobne od dwóch wyżej, bo pyta o inną część mowy, i ma jedno
    # miejsce, bo zapowiednika ta gramatyka nie ma; oba fakty stoją przy stałej.
    #
    # Gospodarza ta pozycja nie wybiera i jest to ta sama odmowa, którą olski
    # wydaje o wyrażeniu przyimkowym: `gdzie` dopowiada miejsce nazwane w zdaniu
    # nadrzędnym, a które to miejsce, rozstrzyga znaczenie, nie składnia
    # (docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).
    przysłówek_względny = word("adv", lemma=PRZYSŁÓWEK_WZGLĘDNY)
    _zamykane(
        grammar,
        OKOLICZNIKOWY,
        [PRZECINEK, przysłówek_względny, Głowa(nt("Clause"))],
        pozycja="za",
    )
    grammar.rule(
        OKOLICZNIKOWY,
        [przysłówek_względny, Głowa(nt("Clause")), PRZECINEK],
        pozycja="przed",
    )

    # Ten sam okolicznik pod spójnikiem, który niesie cząstkę trybu
    # (:data:`SPÓJNIKI_TRYBU`): `Gdyby Polacy byli świadomi, zdawaliby sobie
    # sprawę.`, `Trzeba wdrożyć ją szybko, aby jej efekty były widoczne.` Ciała są
    # osobne od tych wyżej, bo tylko one żądają od zdania formy na -ł, a spójnik
    # bierze oba miejsca, bo zdanie z każdym z tych spójników polszczyzna wysuwa.
    #
    # Wypełnieniem bywa fraza bezokolicznikowa zamiast zdania i jest to w tym
    # rejestrze użycie równie częste: `Odnotowuję to, żeby złagodzić wrażenie.`
    # Bezokolicznik podmiotu nie ma i trybu nie niesie, więc ciało z nim o tryb nie
    # pyta, a cenę i zakup ma osobne, bo jest osobnym ciałem.
    spójnik = word("comp", lemma=SPÓJNIKI_TRYBU)
    for wnętrze in (nt("Clause", tryb=TRYB_POD_SPÓJNIKIEM), nt("InfinitivePhrase")):
        _zamykane(grammar, OKOLICZNIKOWY, [PRZECINEK, spójnik, Głowa(wnętrze)], pozycja="za")
        grammar.rule(OKOLICZNIKOWY, [spójnik, Głowa(wnętrze), PRZECINEK], pozycja="przed")

    # Dwie pozycje, bo polszczyzna stawia ten okolicznik przed swoim zdaniem i za
    # nim, a szyku wewnątrz zdania nadrzędnego nie zmienia ani jedna, ani druga.
    grammar.rule(
        "ClauseConjunct",
        [Głowa(nt("ClauseConjunct", tryb=V("t"))), nt(OKOLICZNIKOWY, pozycja="za")],
        dostawka=DOSTAWKA,
    )
    grammar.rule(
        "ClauseConjunct",
        [
            nt(OKOLICZNIKOWY, pozycja="przed"),
            Głowa(nt("ClauseConjunct", tryb=V("t"), dostawka=BEZ_DOSTAWKI)),
        ],
    )

    # Te same dwie pozycje nad całym ciągiem współrzędnym, bo okolicznik mówi i o
    # obu członach naraz, i o samym drugim; oba zdania trzyma
    # docs/subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania.
    # Ciała powyżej dają czytanie drugie, te dwa dają pierwsze,
    # i bez nich olski wybiera przez przeoczenie
    # (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    #
    # Ciągu żąda tu cecha (:data:`CIĄG`), a dostawki żąda ciało z okolicznikiem
    # wysuniętym, tak samo jak ciało zdania składowego wyżej; bez jednego i bez
    # drugiego żądania jeden napis wyprowadza się dwoma kształtami.
    grammar.rule(
        "Clause",
        [Głowa(nt("Clause", tryb=V("t"), ciąg=CIĄG)), nt(OKOLICZNIKOWY, pozycja="za")],
        dostawka=DOSTAWKA,
    )
    grammar.rule(
        "Clause",
        [
            nt(OKOLICZNIKOWY, pozycja="przed"),
            Głowa(nt("Clause", tryb=V("t"), ciąg=CIĄG, dostawka=BEZ_DOSTAWKI)),
        ],
    )

    # Zdanie względne, którego poprzednikiem jest całe zdanie przed przecinkiem:
    # `Cena jest niska, co przekreśla sens działań.`, `Bierzemy ostry zakręt,
    # dzięki czemu unikamy zderzenia.` Liczba i rodzaj stoją wypisane wartością,
    # bo poprzednikiem jest zdanie, które ich nie ma, a tyle niesie zaimek `co` —
    # i tym ta pozycja bierze `co`, a nie `kto` (`NominalRelativePronoun`).
    #
    # Pozycje są dwie, tak samo jak przy okoliczniku wyrażonym zdaniem wyżej:
    # poprzednikiem bywa jedno zdanie składowe albo cały ciąg (:data:`CIĄG`),
    # a dostawkę ogłaszają oba (:data:`DOSTAWKA`).
    zdaniowe = nt("NominalRelativeClause", number="sg", gender="n")
    grammar.rule(
        "ClauseConjunct",
        [Głowa(nt("ClauseConjunct", tryb=V("t"))), zdaniowe],
        dostawka=DOSTAWKA,
    )
    grammar.rule(
        "Clause",
        [Głowa(nt("Clause", tryb=V("t"), ciąg=CIĄG)), zdaniowe],
        dostawka=DOSTAWKA,
    )

    # To, co czasownik bierze: jedno dopełnienie, a okolicznik z obu jego stron.
    # Dopełnienie w bierniku, bezokolicznik i orzecznik — zgodny albo w narzędniku —
    # różnią się tym, którą pozycję ramy zajmują, a nie tym, gdzie stoją, więc każde
    # wychodzi z tych samych czterech ciał: Program zapisuje ustawienia, Linter
    # pomaga pisać dobry kod, Ludzie są wolni, Jan jest nauczycielem. Narzędnik
    # dochodzi przez to do kopuli i do nikogo poza nią, bo tylko jej rama go ma.
    #
    # Cztery ciała są jedną decyzją, a nie dwunastoma, i jest to ta sama decyzja,
    # którą szyki zdania podejmują wyżej: brakująca pozycja okolicznika nie odrzuca
    # zdania, tylko wypuszcza jednym czytaniem takie, które ma dwa przyłączenia,
    # jak Muszę jechać do domu. Rozwinięcie tych czterech ciał nie pisze i pisać
    # nie może, choć odpowiada na to samo pytanie: tam okolicznik staje w jednym
    # miejscu naraz, a tu po obu stronach wypełnienia i po obu naraz.
    #
    # Negację niosą dwa z czterech wypełnień i to wystarcza, żeby niosły ją te
    # produkcje: zmienna, której nie zwiąże ani orzecznik, ani zdanie podrzędne,
    # zostaje wolna i konstytuent wychodzi bez tej cechy, a cechy, której
    # konstytuent nie niesie, rodzic nie sprawdza. Orzecznik narzędnikowy stoi
    # więc przy `nie jest` tak samo jak przy `jest`, i tak stoi go polszczyzna.
    for wypełnienie in (
        dopełnienie,
        nt("InfinitivePhrase", valency=V("w"), negacja=V("z")),
        orzecznik_ramy,
        nt("SubordinateClause", valency=V("w")),
        nt("InterrogativeClause", valency=V("w")),
    ):
        for ciało in (
            [wypełnienie],
            [okoliczniki, Głowa(wypełnienie)],
            [Głowa(wypełnienie), okoliczniki],
            [okoliczniki, Głowa(wypełnienie), okoliczniki],
        ):
            grammar.rule("Complements", ciało)
    grammar.rule("Complements", [okoliczniki])

    # Druga pozycja ramy: dopełnienie w celowniku obok wypełnienia, które pozycję
    # ramy zajmuje. `Parser pokazuje autorowi oba czytania.`, `Parser mówi
    # autorowi, że zdanie czyta się dwojako.`, `Krawiec kazał córce usiąść.`
    #
    # Licencję niesie cecha, a nie pozycja ramy (:data:`DRUGA_CELOWNIK`), i wpuszcza
    # ją osobne zdanie leksykonu, liczone z jednego schematu Walentego
    # (``harness/walenty.py``).
    #
    # Wypełnieniem pary jest biernik wypisany wartością, a nie ``dopełnienie`` ze
    # zmienną: zmienna przecina się z tą samą ramą co celownik, więc wpuszcza tu
    # drugi celownik. Orzecznika w tej krotce nie ma, bo Walenty nie odróżnia go od
    # argumentu narzędnikowego (:data:`harness.walenty.WYPEŁNIENIA`).
    #
    # Szyki są dwa, bo polszczyzna ma oba, a okolicznik staje między członami, bo
    # ten rejestr tak pisze: `pokazuje autorowi w wydruku oba czytania`. Miejsca
    # wokół całej pary wylicza ``Complements`` niżej.
    celownikowe = nt("Object", valency=DRUGA_CELOWNIK, czoło=BEZ_CZOŁA)
    for wypełnienie in (
        nt("Object", valency="acc", negacja=V("z"), czoło=BEZ_CZOŁA),
        nt("InfinitivePhrase", valency=V("w"), negacja=V("z")),
        nt("SubordinateClause", valency=V("w")),
        nt("InterrogativeClause", valency=V("w")),
    ):
        for ciało in (
            [celownikowe, Głowa(wypełnienie)],
            [celownikowe, okoliczniki, Głowa(wypełnienie)],
            [Głowa(wypełnienie), celownikowe],
            [Głowa(wypełnienie), okoliczniki, celownikowe],
        ):
            grammar.rule(DRUGA_POZYCJA, ciało, druga=DRUGA_CELOWNIK)

    para = nt(DRUGA_POZYCJA, valency=V("w"), negacja=V("z"), druga=V("d"))
    for ciało in (
        [para],
        [okoliczniki, Głowa(para)],
        [Głowa(para), okoliczniki],
        [okoliczniki, Głowa(para), okoliczniki],
    ):
        grammar.rule("Complements", ciało)

    # Okoliczników bywa więcej niż jeden, bo `postępować wobec innych w duchu
    # braterstwa` ma dwa, a czasownik, który bierze jeden, bierze każdą ich liczbę.
    #
    # Okolicznikiem jest wyrażenie przyimkowe albo przysłówek, więc lista bierze
    # jedno i drugie, a przysłówek dostaje przez nią każdą pozycję, jaką okolicznik
    # w zdaniu ma. Lista jest przy tym płaska, więc `bardzo szybko` wychodzi dwoma
    # okolicznikami zdania obok siebie; ile takich czytań zostaje, mierzy
    # docs/subset.md#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę.
    #
    # Cząstka stoi w tej liście obok przysłówka, bo pozycję w zdaniu ma tę samą, i
    # dlatego oba wypisuje jedna pętla; rolą jest przy tym każde z nich osobno,
    # bo cząstka przysłówkiem nie jest (:data:`CZĄSTKOWY`).
    grammar.rule("Adjuncts", [nt("Modifier")])
    grammar.rule("Adjuncts", [Głowa(nt("Modifier")), okoliczniki])
    for przy_zdaniu in (PRZYSŁÓWKOWY, CZĄSTKOWY):
        grammar.rule("Adjuncts", [nt(przy_zdaniu)])
        grammar.rule("Adjuncts", [Głowa(nt(przy_zdaniu)), okoliczniki])

    # Spójnik wewnętrzny wchodzi tą samą listą i tyle wystarcza, żeby stanął tam,
    # gdzie go polszczyzna stawia: miejsce na okolicznik wylicza się za każdą
    # córką, a nie przed pierwszą (``olski/precedencja.py``), więc czoła zdania
    # ta lista nie daje. Do pętli wyżej ten symbol przez to nie wchodzi: ona daje
    # także czoło, a czoło dałoby `Cena jest niska, więc gramatyka jest tania.`
    # drugie czytanie tego samego kształtu.
    grammar.rule("Adjuncts", [nt(SPÓJNIKOWY)])
    grammar.rule("Adjuncts", [Głowa(nt(SPÓJNIKOWY)), okoliczniki])

    # Pozycja ramy wychodzi z orzecznika, bo tym się te dwa różnią i to na nim stoi
    # ograniczenie wyżej: zgodny bierze każdy czasownik, narzędnikowy kopula.
    # Cechę `czoło` niosą oba ciała po to, żeby szyk z orzecznikiem wysuniętym
    # umiał zażądać orzecznika stojącego na swoim miejscu: bez niej orzecznik
    # wysunięty na czoło pytania wypełniałby także tamten szyk, i `Czym jest
    # parser?` miałoby dwa wyprowadzenia — pytanie oraz zdanie oznajmujące
    # zamknięte pytajnikiem (:data:`BEZ_CZOŁA`).
    grammar.rule(
        "Predicative",
        [nt("AP", case="nom", number=V("n"), gender=V("g"))],
        valency="nom",
        czoło=BEZ_CZOŁA,
    )
    grammar.rule("Predicative", [nt("NP", case="inst")], valency="inst", czoło=BEZ_CZOŁA)

    # Rozkaźnik idzie razem z oznajmującą, bo różni je to, co niosą tagi, a nie
    # to, co mówi ta produkcja.
    #
    # Czasownik zwrotny różni się od formy bez cząstki dwiema rzeczami i tyle też
    # mówi o nim ta pętla: stoi przy nim `się`, a rama bierze się z drugiego
    # leksykonu (:data:`LEMAT_ZWROTNY`). Pozycje cząstki stoją obie przy tej formie
    # (:data:`SZYKI_CZĄSTKI`); przy bezokoliczniku i w oddaleniu od swojej formy
    # cząstka pozycji nie ma.
    #
    # Ramę niosą wszystkie te produkcje, a nie tylko niektóre. Cechy, której
    # konstytuent nie niesie, unifikacja nie sprawdza, więc rama postawiona części
    # czasowników przechodziłaby reszcie za darmo, a żądanie „bądź kopulą” nie
    # byłoby wtedy żądaniem. Po to leksykon ma ramę domyślną.
    #
    # Cząstka przecząca poprzedza formę i nic z tego, co czasownik bierze, przed
    # nią nie stanie, więc przeczenie kosztuje jedną pozycję zamiast pozycji w
    # każdym szyku zdania. Ciało bez cząstki ogłasza przy tym `aff`, bo milczenie
    # przepuściłoby dopełniacz negacji do zdania, które nie przeczy.
    for zwrotne, przed, za in SZYKI_CZĄSTKI:
        for warunek, rama, druga in _klasy(zwrotne):
            for ciało, cechy in _formy_skończone(warunek):
                for przeczenie, negacja in PRZECZENIA:
                    grammar.rule(
                        "Verb",
                        [*przed, *przeczenie, *ciało, *za],
                        valency=rama,
                        negacja=negacja,
                        druga=druga,
                        **cechy,
                    )

    # Bezokolicznik pyta o ten sam leksykon co forma osobowa i o tę samą stronę
    # jego dwóch: z cząstką `się` o zwrotną, bez cząstki o zwykłą. Pętla jest
    # osobna, bo ciało niesie tu własne dopełnienia, a nie dlatego, że rama byłaby
    # inna.
    #
    # Fraza bez własnej cząstki wypuszcza negację, którą wzięła od dołu, więc
    # `Nie chcę czytać książki` żąda dopełniacza od dopełnienia stojącego pod
    # bezokolicznikiem, i tak samo przez łańcuch dowolnej długości.
    #
    # Fraza z własną cząstką nie wypuszcza tej cechy wcale i tym zamyka
    # przenoszenie: `Program ma nie zapisywać ustawień` przeczy bezokolicznikowi,
    # a forma osobowa nad nim nie przeczy. Nieobecnością cechy broni się tu tak
    # samo jak grupa współrzędna, która rodzaju nie niesie.
    for zwrotne, przed, za in SZYKI_CZĄSTKI:
        for warunek, rama, druga in _klasy(zwrotne):
            grammar.rule(
                "InfinitivePhrase",
                [
                    *przed,
                    Głowa(word("inf", **warunek)),
                    *za,
                    nt("Complements", valency=rama, negacja=V("z"), druga=druga),
                ],
                valency="inf",
                negacja=V("z"),
            )
            grammar.rule(
                "InfinitivePhrase",
                [
                    *przed,
                    PRZECZENIE,
                    Głowa(word("inf", **warunek)),
                    *za,
                    nt("Complements", valency=rama, negacja="neg", druga=druga),
                ],
                valency="inf",
            )

    # Fraza bezokolicznikowa, która ramy swojego lematu nie zużywa na własną córkę, tylko
    # wypuszcza ją w górę, bo pozycję z tej ramy zajmuje dopełnienie stojące przed
    # formą osobową (:data:`BEZOKOLICZNIK_OTWARTY`).
    #
    # Cząstki przeczącej te ciała nie mają i nie ma jej po co: dopełnienie wysunięte
    # przed formę osobową stoi przed każdym miejscem, w którym cząstka tej frazy by
    # stanęła, więc przeczenie schodzi się z nim przy formie osobowej albo nigdzie.
    #
    # Miejsce na okolicznik jest za głową i nie ma go przed nią, bo tyle gospodarzy
    # ma okolicznik na torze zwykłym: `Complements` bezokolicznika stoi za swoją
    # głową i przed nią nie sięga, więc `nie może ruszyć szybko` ma tam dwóch
    # gospodarzy, a `nie może szybko ruszyć` jednego. Bez miejsca za głową ta
    # pozycja wybierałaby gospodarza przez przeoczenie
    # (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    for warunek, rama, _druga in _klasy(zwrotne=False):
        głowa = Głowa(word("inf", **warunek))
        grammar.rule(BEZOKOLICZNIK_OTWARTY, [głowa], wysunięte=rama)
        grammar.rule(BEZOKOLICZNIK_OTWARTY, [głowa, okoliczniki], wysunięte=rama)

    grammar.rule("NP", [nt("NPConjunct", person=V("p"), **AGREE)])
    # Zdanie względne po grupie imiennej, w liczbie i rodzaju swojego zaimka:
    # `reguła, która rozstrzyga`. Przypadka nie niesie, bo zaimek bierze go z
    # roli, którą zajmuje w zdaniu podrzędnym, a nie od poprzednika.
    #
    # Stoi to tutaj, a nie wśród ciał `NPConjunct`, i nie jest to wybór wygody:
    # na tamtym poziomie produkcja rekurencyjna daje `te [konstrukcje, które
    # stoją]` obok `[te konstrukcje], które stoją`, czyli dwa wyprowadzenia
    # jednej struktury, których nie ma czym odsiać. Cenę tego poziomu — człon
    # lewy zdania względnego nie unosi — trzyma TODO.md, a docs/subset.md
    # wywodzi, co zgodność z poprzednikiem odbiera przyłączeniu.
    grammar.rule(
        "NP",
        [
            Głowa(nt("NPConjunct", person=V("p"), **AGREE)),
            nt("RelativeClause", number=V("n"), gender=V("g")),
        ],
    )
    # Poprzednik zaimkowy, czyli druga droga zdania względnego z `co`:
    # `to, co mogło się zepsuć`, `wszystko, co zjadł`, `nikt, kto wchodzi w środek`
    # (`NominalRelativePronoun`).
    #
    # Poprzednikiem jest tu terminal, a nie grupa imienna, bo zaimek rzeczowny
    # dopełniacza nie bierze
    # (docs/subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)
    # i przydawki przed sobą nikt tu nie policzył. Lematy schodzą się z dwóch
    # deklaracji obok, zamiast stać trzecią listą, którą rozjeżdża dopisanie do
    # którejkolwiek z nich.
    poprzednik_zaimkowy = word(
        "subst", lemma=ZAIMEK_RZECZOWNY, bez_lematu=ZAIMEK_PYTAJNO_RZECZOWNY, **AGREE
    )
    grammar.rule(
        "NPConjunct",
        [
            Głowa(poprzednik_zaimkowy),
            nt("NominalRelativeClause", number=V("n"), gender=V("g")),
        ],
        person="ter",
    )
    # Tytuł i termin w cudzysłowie: `„Zasady techniki prawodawczej”`. Grupa
    # przechodzi przez cudzysłów cała, bo polszczyzna odmienia to, co on obejmuje,
    # wedle roli, w której grupa stanęła: `przepisem „Zasad techniki
    # prawodawczej”` ma dopełniacz w środku, a `Same „Zasady” stoją` mianownik.
    # Cechy idą przez to zmienną wspólną, a nie wypisane wartością.
    #
    # Wnętrzem jest sama grupa imienna, więc `„to nie zdanie”` zostaje na zewnątrz;
    # docs/subset.md trzyma, co jeszcze zostaje i za ile ta pozycja weszła.
    grammar.rule(
        "NPConjunct",
        [
            CUDZYSŁÓW_OTWIERAJĄCY,
            Głowa(nt("NP", person=V("p"), **AGREE)),
            CUDZYSŁÓW_ZAMYKAJĄCY,
        ],
    )
    # Rodzaju ciąg współrzędny nie niesie: rodzaj `rozumu i sumienia` polszczyzna
    # rozstrzyga regułami, których unifikacja nie wypowie, a cechy, której fraza
    # nie niesie, nie ma o co zawieść żadna zgodność.
    grammar.rule(
        "NP",
        [Głowa(nt("NPConjunct", case=V("c"))), SPÓJNIK_BEZ_PRZECINKA, nt("NP", case=V("c"))],
        number="pl",
        person="ter",
    )
    grammar.rule(
        "NP",
        [Głowa(nt("NPConjunct", case=V("c"))), PRZECINEK, nt("NP", case=V("c"))],
        number="pl",
        person="ter",
    )

    # Zgodność jest tu samą unifikacją, a nie osobnym sprawdzeniem, i wszystkie te
    # ciała dzielą te same trzy zmienne (:data:`AGREE`). Człon z rzeczownikiem w
    # głowie ogłasza trzecią osobę wprost, bo bez tego ogłoszenia wziąłby go po
    # cichu czasownik w pierwszej.
    grammar.rule(
        "NPConjunct", [przydawka_nierozdzielna, Głowa(nt("NPConjunct", **AGREE))], person="ter"
    )
    # Głową grupy imiennej jest rzeczownik albo rzeczownik odczasownikowy, więc
    # każda pozycja niżej wychodzi dwoma ciałami, po jednym na głowę. Terminala o
    # dwóch częściach mowy tu nie ma i nie jest to wybór wygody: cena tej głowy ma
    # być osobną liczbą, a sonda różnicowa wycenia ją zdejmowaniem ciał, więc
    # pozycja zlana w jeden terminal nie byłaby żadnym ciałem osobno. Pętla trzyma
    # zarazem oba komplety zgodnymi: pozycja dopisana rzeczownikowi dochodzi tą
    # samą deklaracją i drugiej głowie.
    # docs/subset.md wywodzi, czemu ta głowa jest głową grupy, a nie pozycją ramy.
    #
    # Głowa, która rządzi dopełniaczem, nie jest zaimkiem rzeczownym: bez tego
    # warunku każdy taki zaimek daje grupie imiennej drugie czytanie tego samego
    # kształtu. Warunek stoi w deklaracji pary, a nie w każdym ciele, bo ciał z
    # dopełniaczem pod głową jest kilka, a rzeczownikiem odczasownikowym nie jest
    # żaden z tych zaimków i wykluczać tam nie ma czego;
    # wywód i cenę trzyma docs/subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem.
    for głowa, głowa_dopełniacza in (
        (
            word("subst", bez_lematu=ZAIMEK_PYTAJNO_RZECZOWNY, **AGREE),
            word("subst", bez_lematu=ZAIMEK_RZECZOWNY, **AGREE),
        ),
        (word("ger", bez_lematu=PIĘCIE, **AGREE), word("ger", bez_lematu=PIĘCIE, **AGREE)),
    ):
        grammar.rule("NPConjunct", [głowa], person="ter")
        grammar.rule("NPConjunct", [Głowa(głowa_dopełniacza), nt("NP", case="gen")], person="ter")
        # Przydawkę terminu polszczyzna stawia za rzeczownikiem: `plik
        # konfiguracyjny`, `język polski`. Oba szyki są polszczyzną, więc oba stoją
        # tutaj, a zdanie, które przyjmuje oba czytania, jest wieloznaczne.
        grammar.rule("NPConjunct", [Głowa(głowa), przydawka], person="ter")
        grammar.rule("NPConjunct", [Głowa(głowa), nt("Modifier")], person="ter")
        # Oba szyki przydawki naraz: dobrem wspólnym wszystkich obywateli, zadania
        # ochrony ludności. Bez tej pozycji dopełniacz dochodzi tylko do przymiotnika
        # stojącego przed rzeczownikiem, więc termin nazwany drugim szykiem nie ma
        # wyprowadzenia, a rejestr ustaw nazywa tak swoje terminy zdanie po zdaniu:
        # docs/ustawy.md trzyma, ile ta pozycja tam daje i ile odbiera.
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), przydawka, nt("NP", case="gen")],
            person="ter",
        )
        # Wyrażenie przyimkowe po rzeczowniku, który już coś przy sobie ma: akcja
        # zbrojna w Strefie Gazy, rozmieszczenie ogrodów działkowych w Polsce,
        # zadania ochrony ludności w gminie. Bez tych trzech pozycji przyłączenie do
        # rzeczownika w takiej grupie nie istnieje, a zdanie wychodzi jednym
        # czytaniem przez czasownik. Trzecia idzie razem z przydawką wyżej: bez niej
        # wyrażenie po takim terminie dochodzi do dopełniacza i do nikogo więcej,
        # czyli gramatyka wybiera przyłączenie, którego wybierać nie ma.
        grammar.rule("NPConjunct", [Głowa(głowa), przydawka, nt("Modifier")], person="ter")
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), nt("NP", case="gen"), nt("Modifier")],
            person="ter",
        )
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), przydawka, nt("NP", case="gen"), nt("Modifier")],
            person="ter",
        )
    # Grupa liczebnikowa, w dwóch ciałach, bo polszczyzna ma dwa przyłączenia
    # liczebnika i Morfeusz rozdziela je cechą `accommodability`.
    #
    # Liczebnik zgodny stoi jak przymiotnik przy rzeczowniku: `dwie rzeczy`,
    # `cztery wozy`, `oba pliki`.
    #
    # Liczebnik rządzący wymaga dopełniacza mnogiego i wypuszcza grupę, której
    # liczba i rodzaj nie są liczbą ani rodzajem żadnego słowa pod nią:
    # `Pięć kobiet przyszło` żąda czasownika w liczbie pojedynczej i rodzaju
    # nijakim, choć `kobiet` jest mnogie i żeńskie. Cechy są tu więc wypisane
    # wartością, a nie zmienną wspólną z córką, tak samo jak w koordynacji niżej,
    # z tą różnicą, że tam wartość opisuje ciąg, a tu przeczy każdemu słowu w
    # środku. Zmienna wspólna wygląda tu poprawnie i odwraca zgodność: przyjmuje
    # `Pięć kobiet przyszły`, którego polszczyzna nie ma.
    # Głową jest liczebnik, tak samo jak pod rzeczownikiem rządzącym
    # dopełniaczem: rządzi on przypadkiem tego, co pod nim stoi.
    #
    # Rodzaj przechodzi z liczebnika na dopełniacz, bo polszczyzna go tam żąda:
    # `pięciu mężczyzn` ma rodzaj męskoosobowy, a `pięć kobiet` żeński, i są to
    # dwie różne formy liczebnika. Cyfry żadne z tych ciał nie bierze i dlaczego,
    # mówi docs/subset.md pod „Cyfry olski nie bierze”, gdzie stoi też pomiar obu.
    #
    # Oba pytają symbolu `Liczebnik`, a nie terminala, bo liczebnik złożony
    # przyłącza się wedle członu skrajnie prawego: `dwadzieścia dwa chleby` wedle
    # `dwa`, a `dwadzieścia pięć chlebów` wedle `pięć`. Symbol jest łańcuchem o
    # głowie po prawej i od niej bierze `accommodability`; czego nie bierze i co
    # płaci, mówi
    # docs/subset.md#liczebnik-złożony-przyłącza-się-wedle-ostatniego-członu.
    grammar.rule("Liczebnik", [word("num", accommodability=V("a"), **AGREE)])
    grammar.rule(
        "Liczebnik",
        [word("num", **AGREE), Głowa(nt("Liczebnik", accommodability=V("a"), **AGREE))],
    )
    grammar.rule(
        "NPConjunct",
        [nt("Liczebnik", accommodability="congr", **AGREE), Głowa(nt("NPConjunct", **AGREE))],
        person="ter",
    )
    grammar.rule(
        "NPConjunct",
        [
            Głowa(nt("Liczebnik", accommodability="rec", case=V("c"), gender=V("g"))),
            nt("NP", case="gen", number="pl", gender=V("g")),
        ],
        number="sg",
        gender="n",
        person="ter",
    )

    # Zaimek jest tym jednym członem, który niesie własną osobę, i po to jedno tu
    # stoi: bez niego podmiot w pierwszej i w drugiej osobie nie ma czym być.
    grammar.rule("NPConjunct", [word({"ppron3", "ppron12"}, person=V("p"), **AGREE)])

    # Zaimek dzierżawczy przed grupą imienną: `jego skutki`, `ich cena`
    # (:data:`ZAIMEK_DZIERŻAWCZY`). Zgodności ta pozycja nie ma i mieć nie może:
    # zaimek zgadza się liczbą i rodzajem ze swoim poprzednikiem, a poprzednik stoi
    # w zdaniu obok, więc cechy grupy są cechami samej głowy. Tym różni się to
    # ciało od przymiotnika i od liczebnika zgodnego, które dzielą z głową
    # wszystkie trzy cechy.
    #
    # Ciało jest jedno, bo dopełniacz po rzeczowniku bierze produkcja wyżej.
    # Co ta pozycja kosztuje, mierzy
    # docs/subset.md#zaimek-dzierżawczy-jest-dopełniaczem-przed-rzeczownikiem.
    grammar.rule("NPConjunct", [ZAIMEK_DZIERŻAWCZY, Głowa(nt("NPConjunct", **AGREE))], person="ter")

    # Cząstka przed grupą imienną, czyli jej gospodarz drugi: `Nawet ptaki przestały
    # śpiewać.` Kurs, po którym weszła, trzyma
    # docs/subset.md#cząstka-wchodzi-obu-gospodarzami-a-w-grupie-nie-nosi-etykiety.
    #
    # Córką lewą jest terminal, a nie symbol :data:`CZĄSTKOWY`: etykieta roli
    # mówiłaby o zdaniu, że ma cząstkę zdania, a ta stoi w grupie.
    #
    # Osobę ta pozycja przepuszcza, a nie ogłasza `ter` jak przymiotnik i zaimek
    # dzierżawczy nad nią, bo cząstka staje i przed zaimkiem
    # (`Nawet ja zapisuję ustawienia.`).
    grammar.rule("NPConjunct", [CZĄSTKA, Głowa(nt("NPConjunct", person=V("p"), **AGREE))])

    # Grupa przymiotnikowa koordynuje się tak samo i zgadza się przez cały ciąg,
    # więc `wolni i równi` jest jednym orzecznikiem, a `wolna i równi` żadnym.
    grammar.rule("AP", [nt("APConjunct", **AGREE)])
    grammar.rule("AP", [Głowa(nt("APConjunct", **AGREE)), SPÓJNIK_BEZ_PRZECINKA, nt("AP", **AGREE)])
    grammar.rule("AP", [Głowa(nt("APConjunct", **AGREE)), PRZECINEK, nt("AP", **AGREE)])
    # Imiesłów bierny jest tu przymiotnikiem i zatrzymuje dopełnienie, którym
    # rządził jego czasownik: `obdarzeni rozumem i sumieniem`.
    grammar.rule("APConjunct", [orzecznikowy])
    grammar.rule("APConjunct", [Głowa(orzecznikowy), nt("NP", case="inst")])
    # Trzecie miejsce, do którego wyrażenie przyimkowe dochodzi: powiązani z
    # interesami postkomunistów, przeznaczany na budowę.
    grammar.rule("APConjunct", [Głowa(orzecznikowy), nt("Modifier")])

    # Jeden lemat jest tu wykluczony i wykluczony jest z nazwy
    # (:data:`PRZYIMEK_ROZDZIELAJĄCY`).
    grammar.rule("Modifier", [Głowa(PRZYIMEK), nt("NP", case=V("c"))])

    # Przysłówek zdania jako konstytuent, a nie jako słowo w liście okoliczników,
    # bo bez tego symbolu okolicznik przysłówkowy nie ma węzła, który werdykt nazwie
    # (:data:`PRZYSŁÓWKOWY`).
    grammar.rule(PRZYSŁÓWKOWY, [PRZYSŁÓWEK])
    # Przysłówek przed przysłówkiem, czyli gospodarz trzeci: `bardzo szybko`.
    # Stopnia żąda od córki lewej z tego samego powodu, z którego żąda go pozycja
    # przy przymiotniku: `tu szybko` nie jest niczym. Bez tej pozycji `bardzo`
    # dochodziło do zdania na równi z `szybko`, czyli zdanie przyjęte mówiło o
    # sobie nieprawdę, a kurs, po którym ta pozycja weszła, trzyma
    # docs/subset.md#przysłówek-wchodzi-każdym-gospodarzem-bo-dalszy-zdejmuje-czytania-nieprawdziwe.
    #
    # Córka prawa jest tym samym symbolem, a nie słowem, bo `wyjątkowo bardzo
    # szybko` jest tą samą pozycją postawioną dwa razy, a nad Składnicą oba ciała
    # wypadły tą samą ceną: ciało rekurencyjne bierze łańcuch za darmo.
    grammar.rule(PRZYSŁÓWKOWY, [PRZYSŁÓWEK_STOPNIA, Głowa(nt(PRZYSŁÓWKOWY))])
    # `gdzie indziej`, czyli para, w której przysłówek względny nie otwiera zdania,
    # tylko określa drugi przysłówek. Ciało jest osobne, bo terminal okolicznika
    # ten lemat wyklucza (:data:`PRZYSŁÓWEK`), a bez tego ciała wykluczenie
    # zabiera zdania, które ta proza pisze: `Cena jest gdzie indziej.`
    grammar.rule(
        PRZYSŁÓWKOWY,
        [word("adv", lemma=PRZYSŁÓWEK_WZGLĘDNY), Głowa(word("adv", lemma="indziej"))],
    )

    # Cząstka przy zdaniu, tym samym prawem co przysłówek nad nią
    # (:data:`CZĄSTKOWY`); kryterium na jej listę stoi przy :data:`CZĄSTKI`.
    grammar.rule(CZĄSTKOWY, [CZĄSTKA])

    grammar.rule(SPÓJNIKOWY, [SPÓJNIK_WEWNĘTRZNY])

    # Zdanie względne, czyli przecinek i `RelativeCore`, którym jest samo zdanie
    # bez przecinków odgraniczających. Przecinek zamykający dokłada
    # :func:`_zamykane`, tak samo jak trzem pozostałym zdaniom podrzędnym.
    #
    # Wtrącenie w nawiasie dostaje pozycję w ciele zamykanym przecinkiem i tylko
    # w nim, bo tam stoi ono przed tym przecinkiem, a przyłączone do zdania
    # nadrzędnego stanęłoby za nim, czyli dałoby inny napis. Ciało bez przecinka
    # kończy się tam, gdzie zdanie nadrzędne, więc ta sama pozycja dałaby tam
    # dwa czytania jednego napisu, i dlatego jest to ciało osobne, a nie druga
    # córka w obu; docs/subset.md wywodzi to razem z ceną.
    rdzeń = Głowa(nt("RelativeCore", number=V("n"), gender=V("g")))
    _zamykane(grammar, "RelativeClause", [PRZECINEK, rdzeń])
    grammar.rule("RelativeClause", [PRZECINEK, rdzeń, nt(WTRĄCONY), PRZECINEK])

    # To samo zdanie względne z czołem rzeczownym: rzeczownik bierze tamten symbol,
    # a poprzednik zaimkowy i zdaniowy ten (`NominalRelativePronoun`).
    # Wtrącenia w nawiasie to ciało nie ma, bo pozycji tej nad nim nikt nie policzył.
    rdzeń_rzeczowny = Głowa(nt("NominalRelativeCore", number=V("n"), gender=V("g")))
    _zamykane(grammar, "NominalRelativeClause", [PRZECINEK, rdzeń_rzeczowny])

    # Zaimek względny jest grupą imienną o jednym słowie i osobnym symbolem, bo
    # grupa imienna stoi w zdaniu wszędzie, a on w jednym miejscu: na czele
    # zdania względnego. Wpuszczony do grupy imiennej stanąłby w każdej jej
    # pozycji, a `Program zapisuje który.` polszczyzną nie jest.
    # Obie pary cech czoła są tu jedną parą, bo głową jest sam zaimek
    # (:func:`zaimek_czoła`).
    grammar.rule(
        "RelativePronoun",
        [word("adj", lemma=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE)],
        **zaimek_czoła(V("n"), V("g")),
    )

    # Ten sam zaimek, którym zdanie pyta, zastępuje też poprzednik: `to, co mogło
    # się zepsuć`, `wszystko, co zjadł`. Symbol jest osobny od `RelativePronoun`,
    # bo rozstrzyga poprzednik, a nie lemat: `co` zastępuje zaimek rzeczowny albo
    # całe zdanie, a `który` rzeczownik, więc jednym symbolem rzeczownik dostawał
    # zdanie względne z `co`. Wywód, cenę i zakup rozdzielenia trzyma
    # docs/subset.md#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie.
    #
    # Liczba i rodzaj zaimka odróżniają przy tym `co` od `kto` bez osobnej cechy:
    # `co` jest nijakie, a `kto` męskoosobowe (:func:`zaimek_czoła`).
    # Jedno wykluczenie z pozycji rzeczownej stoi pod tym czołem i pod pytaniem
    # (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`).
    grammar.rule(
        "NominalRelativePronoun",
        [word("subst", lemma=ZAIMEK_PYTAJNO_RZECZOWNY, **AGREE)],
        **zaimek_czoła(V("n"), V("g")),
    )

    # Grupa, którą polszczyzna wysuwa przed zdanie względne razem z zaimkiem:
    # rzeczownik z zaimkiem w dopełniaczu za sobą (`na podstawie której`) i ten
    # sam rzeczownik z zaimkiem przed sobą (`o którego zdaniu`).
    #
    # Tu obie pary czoła są różne i to jest cała trudność tej grupy: `której
    # przepisy` jest mnogie, a jego zaimek pojedynczy (:func:`zaimek_czoła`).
    # Przypadek wypuszcza rzeczownik, bo o przypadek pyta przyimek nad grupą albo
    # rola, w której grupa stanęła.
    #
    # Każdy z tych dwóch kształtów jest osobnym ciałem, bo cechy nie przechodzą
    # przez grupę imienną same, więc głowa z przydawką pod sobą wysunięcia nie ma.
    #
    # Zaimka rzeczownego ta głowa nie bierze z tego samego powodu, z którego nie
    # bierze go głowa grupy imiennej wyżej: zaimek w dopełniaczu jest tu przydawką,
    # a zaimek rzeczowny przydawki dopełniaczowej przy sobie nie ma.
    głowa_grupy = word("subst", bez_lematu=ZAIMEK_RZECZOWNY, **AGREE)
    zaimek_dopełniacza = nt("RelativePronoun", case="gen", **POPRZEDNIK)
    for ciało in (
        [Głowa(głowa_grupy), zaimek_dopełniacza],
        [zaimek_dopełniacza, Głowa(głowa_grupy)],
    ):
        grammar.rule("RelativeNP", ciało, **zaimek_czoła(V("nz"), V("gz")))

    # Grupa pytajna: zaimek pytajny i grupa imienna, przy której on stoi. Głową
    # jest grupa imienna, bo pytanie jest o rzecz, którą ona nazywa, a zaimek mówi
    # tylko, że pyta się o to, która z nich. Zaimek zgadza się z tą głową, więc
    # obie pary czoła są i tu jedną parą; niesie ją grupa po to, żeby czoło obu
    # rodzin pisała jedna funkcja, a nie po to, żeby ktoś ją w pytaniu czytał.
    grammar.rule(
        PYTAJNY,
        [ZAIMEK_PYTAJNY, Głowa(nt("NP", **AGREE))],
        **zaimek_czoła(V("n"), V("g")),
    )

    # Czoło pytania o jednym słowie: `kto` i `co`, czyli zaimki, którymi pyta się
    # o osobę i o rzecz, a nie o to, która z nich. Rzeczownika przy sobie nie mają,
    # więc ciało jest drugie, a nie ten sam lemat dopisany do listy wyżej.
    #
    # Ciało tego samego symbolu, a nie symbol osobny jak przy zaimku względnym:
    # tam czoła są dwa dlatego, że cena każdego z nich ma być osobną liczbą, a tu
    # jest ona osobną i tak, bo zdejmuje się to jedno ciało. Symbol osobny kazałby
    # ponadto :func:`_wysunięta_rola` wypisać dla niego wszystkie szyki drugi raz.
    zaimek_pytajny_rzeczowny = word("subst", lemma=ZAIMEK_PYTAJNO_RZECZOWNY, **AGREE)
    grammar.rule(PYTAJNY, [zaimek_pytajny_rzeczowny], **zaimek_czoła(V("n"), V("g")))
    # Wyrażenie przyimkowe przy tym zaimku: `Kto z posłów zapisuje ustawienia?`
    # Grupa pytajna wyżej bierze je przez grupę imienną, którą ma w środku, a to
    # czoło grupy imiennej nie ma, więc pozycja jest tu osobnym ciałem. Bez niej
    # zdanie z takim wyrażeniem wychodzi przyjęte i mówi o zdaniu nieprawdę, bo
    # wyrażenie przyłącza się wtedy do orzeczenia: pytanie jest o `kto z posłów`,
    # a nie o `kto`.
    grammar.rule(
        PYTAJNY,
        [Głowa(zaimek_pytajny_rzeczowny), nt(PRZYŁĄCZANY)],
        **zaimek_czoła(V("n"), V("g")),
    )

    # Zdanie względne i pytanie dzielą kształt: jedna rola stoi w nich wysunięta na
    # czoło, a reszta zdania jest tą samą resztą, więc deklaracje wypisuje jedna
    # funkcja dla obu (:func:`_wysunięta_rola`). Czół jest w zdaniu względnym dwa —
    # sam zaimek i grupa, w której on stoi — i każde z nich wchodzi w obie pozycje:
    # w rolę zdania składowego i pod przyimek. Pytanie ma czoło jedno, bo grupa
    # pytajna obejmuje tam także sam zaimek.
    #
    # Trzecią rolę pętla wypisuje raz na rodzinę, bo jest w niej jednym ciałem:
    # za wysuniętym wyrażeniem przyimkowym stoi zdanie składowe całe, w każdym
    # szyku, jaki ono ma, więc rozwinięcia szyku ta rola od nikogo nie żąda.
    # Symbol wyrażenia jest osobny dla każdej z rodzin, bo wspólny wpuściłby grupę
    # pytajną na czoło zdania względnego, gdzie nie ma się z czym zgodzić.
    #
    # Czoło grupowe stoi obok zaimkowego zamiast je obejmować, i rozstrzyga o tym
    # pomiar: cena każdej z dwóch pozycji jest osobną liczbą,
    # zdejmując produkcje. Czołem jednym pozycja bez przyimka nie byłaby żadnym
    # ciałem osobno, bo te same ciała brałby sam zaimek, więc nie byłoby czego zdjąć.
    for symbol, modyfikator, czoła in (
        ("RelativeCore", "RelativeModifier", ("RelativePronoun", "RelativeNP")),
        ("NominalRelativeCore", "NominalRelativeModifier", ("NominalRelativePronoun",)),
        ("InterrogativeCore", "InterrogativeModifier", (PYTAJNY,)),
    ):
        for czoło in czoła:
            _wysunięta_rola(zdanie, symbol, czoło)
            grammar.rule(
                modyfikator,
                [Głowa(PRZYIMEK), nt(czoło, case=V("c"), **zaimek_czoła(V("nz"), V("gz")))],
                **POPRZEDNIK,
            )
        # Za wysuniętym wyrażeniem przyimkowym stoi zdanie składowe albo sam
        # rzeczownik orzekający, bo kopuła opuszczona zostawia po zdaniu jeden
        # wyraz (:data:`ORZEKAJĄCY`). Dwa ciała, a nie jedno z symbolem wspólnym:
        # cena każdego z nich jest osobną liczbą.
        for wnętrze in (nt("ClauseConjunct"), nt(ORZEKAJĄCY)):
            grammar.rule(symbol, [nt(modyfikator, **POPRZEDNIK), Głowa(wnętrze)], **POPRZEDNIK)

    # Zdanie pytające: czoło pytania i pytajnik. Ciało jest osobne od zdania
    # oznajmującego, a nie wzięte przez :data:`KONIEC_ZDANIA`, bo pytanie zamyka
    # jeden znak z trzech, które tamten terminal bierze.
    grammar.rule("Sentence", [Głowa(nt("InterrogativeCore")), PYTAJNIK])

    # Pytanie zależne: przecinek i to samo czoło. Pozycję ramy niesie ono tak samo
    # jak zdanie z `że`, a pozycja jest osobna i dlaczego, mówi
    # :data:`RAMA_DOMYŚLNA`. Spójnika w ciele nie ma, bo podporządkowuje tu sam
    # zaimek, i tym się to zdanie podrzędne od dwóch pozostałych różni.
    # Przecinek zamykający dokłada :func:`_zamykane`.
    _zamykane(
        grammar,
        "InterrogativeClause",
        [PRZECINEK, Głowa(nt("InterrogativeChain"))],
        valency="int",
    )

    # Ciąg pytań pod jednym czasownikiem: `Drzewo mówi, co w zdaniu jest tematem,
    # a co jest nowe.`, `Dokument mówi, po co był linter i co zamknęło ten tor.`
    # Pozycję ramy zajmuje cały ciąg, a nie każdy człon osobno, bo drugie
    # wypełnienie bierze przy czasowniku sam celownik (:data:`DRUGA_CELOWNIK`),
    # i dlatego ciąg jest tu symbolem, a nie drugim ciałem zdania podrzędnego.
    #
    # Znakiem ciągu jest spójnik, a nie sam przecinek: przecinek w tym miejscu
    # zamyka zdanie podrzędne (:func:`_zamykane`), więc ciało z nim samym dałoby
    # jednemu napisowi dwa wyprowadzenia. Ten rejestr pisze ten ciąg spójnikiem.
    #
    # Bez wykluczenia z pozycji rzeczownej (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`)
    # człon drugi wyprowadza się zdaniem współrzędnym, którego podmiotem albo
    # dopełnieniem jest ten zaimek, więc ciąg stoi razem z tamtym wykluczeniem.
    # Czoło pytania o rozstrzygnięcie: `Czy program zapisuje ustawienia?`, `Pyta,
    # czy go to dotyczy.` Wysuniętej roli tu nie ma, bo pytanie jest o całe zdanie,
    # a nie o to, co w nim stoi w którymś miejscu, więc ciało bierze `Clause` całe
    # i nie przechodzi przez :func:`_wysunięta_rola`.
    #
    # Ten sam lemat bierze zarazem koordynacja bez przecinka
    # (:data:`SPÓJNIK_BEZ_PRZECINKA`), gdzie `czy` znaczy `albo`, i te dwa użycia
    # rozdziela materiał pod spójnikiem: koordynacja stawia po nim człon, a to
    # ciało zdanie. Napisu wspólnego oba nie mają, więc drugiego czytania to ciało
    # nie dokłada nikomu.
    grammar.rule(
        "InterrogativeCore",
        [word("conj", lemma=SPÓJNIK_PYTAJNY), Głowa(nt("Clause"))],
    )

    człon_pytania = Głowa(nt("InterrogativeCore"))
    grammar.rule("InterrogativeChain", [człon_pytania])
    grammar.rule(
        "InterrogativeChain",
        [człon_pytania, SPÓJNIK_BEZ_PRZECINKA, nt("InterrogativeChain")],
    )
    grammar.rule(
        "InterrogativeChain",
        [człon_pytania, PRZECINEK, SPÓJNIK_PRZECINKOWY, nt("InterrogativeChain")],
    )

    return grammar


GRAMMAR = build()
