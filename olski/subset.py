"""Deklaracja podzbioru: produkcje, wykluczenia i werdykt nad zdaniem.

Wykluczenia są dwojakie, bo produkcja rozstrzyga o zdaniu, a nie o formie.
Produkcje niżej mówią, jakie zdanie się wyprowadza,
a ``admissible`` odbiera formie czytania, zanim produkcja je zobaczy.

Werdykt mówi o zdaniu więcej niż sam status, bo autor ma je poprawić.
Zdanie o dwóch czytaniach nie jest olskie
(docs/subset.md#validity-is-uniqueness-not-just-derivability),
a :meth:`Verdict.explain` pokazuje, gdzie te czytania się rozchodzą;
zdanie odrzucone dostaje miejsce, na którym rozbiór stanął,
a :func:`zatrzymania` każde takie miejsce, bo pierwsze zasłania następne.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, replace

from olski import projekt
from olski.document import SENTENCE_CLOSE, Document
from olski.grammar import Grammar, Głowa, Part, V, Var, nt, word
from olski.morph import Reading, Segment, analyse, tag
from olski.parse import (
    PRZYŁĄCZONY_DO,
    Deklaracja,
    Przyłączenie,
    Result,
    Rozbieżność,
    parse,
    streszczenia,
)
from olski.precedencja import Rozwinięcie
from olski.walencja import (
    BEZ_BIERNIKA,
    BEZ_BIERNIKA_ZWROTNE,
    Z_CELOWNIKIEM,
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

#: Rola okolicznika wyrażonego zdaniem,
#: czyli tego, który mówi, kiedy, dlaczego albo pod jakim warunkiem
#: zachodzi to, co mówi zdanie nad nim.
#: Stoi ona zarazem wśród zdań podrzędnych,
#: bo wnętrze tego okolicznika jest osobnym zdaniem,
#: i tyle właśnie znaczy nazwanie go rolą:
#: streszczenie nazywa go całym napisem i w środek nie zagląda.
OKOLICZNIKOWY = "AdverbialClause"

#: Rola grupy pytajnej, czyli tego, o co zdanie pyta:
#: `które zadania` w `Ustawy określają, które zadania mają charakter obowiązkowy.`
#: Konstytuentem jest zaś grupa imienna,
#: więc wnętrze streszczenie nazywa całym napisem, tak samo jak wnętrze podmiotu.
PYTAJNY = "Interrogative"

#: Rola rzeczownika, który orzeka bez czasownika:
#: `mowa` w `zadania, o których mowa w ustawie`.
#: Zdanie z tym rzeczownikiem nie ma ani podmiotu, ani czasownika,
#: więc bez tej etykiety wychodziłoby `valid` bez ani jednej roli.
#:
#: Rola stoi obok `Predicative`, a nie jest nią,
#: bo orzecznik jest pozycją ramy,
#: a ten rzeczownik nie ma nad sobą czasownika, który by ramę ogłaszał;
#: co przyjmuje gramatyka zlewająca te dwie, mierzy
#: docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną.
ORZEKAJĄCY = "NominalPredicate"

#: Rola tego, co orzeka bez podmiotu. Głowy są dwie i obie rządzą ramą czasownika:
#: predykatyw — `trzeba` w `Trzeba czytać dokumenty.` — oraz forma `imps` —
#: `zgłoszono` w `Zgłoszono usterkę.`
#: Od rzeczownika orzekającego różni tę rolę kształt orzekania:
#: tamten stoi w mianowniku i żąda okolicznika,
#: a te dwie rządzą tym, czym rządziłby czasownik, i podmiotu nie mają.
#:
#: Rola stoi obok `Verb`, a nie jest nią, bo żadna z tych dwóch głów zgodności nie
#: niesie: `Verb: trzeba` mówiłoby o zdaniu, że ma orzeczenie zgodne z podmiotem,
#: którego ono nie ma, a `Verb: zgłoszono` dałoby `Zgłoszono program.` podmiot
#: `program`, bo cechy, której konstytuent nie niesie, unifikacja nie sprawdza.
#: Co wpuszczenie każdej z tych dwóch głów kosztuje, mierzą
#: docs/subset.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika oraz
#: docs/subset.md#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu.
BEZOSOBOWY = "ImpersonalPredicate"

#: Rola cząstki, czyli tej, która stoi przy zdaniu: `już`, `dopiero`, `także`.
#: Od przysłówka różni ją część mowy: cząstka przysłówkiem nie jest,
#: więc `Adverb: już` mówiłoby o zdaniu,
#: że ma okolicznik przysłówkowy, którego ono nie ma.
#: Pozycję ma tę samą co przysłówek i dlatego pisze je jedna pętla.
CZĄSTKOWY = "Particle"

#: Rola wtrącenia w nawiasie,
#: czyli tego, co ten rejestr dopowiada obok zdania: `(docs/subset.md)`, `(niżej)`.
#: Rolą zdania jest samo wtrącenie, a nie to, co ono niesie:
#: nawias dopowiada, a nie wypełnia pozycji,
#: więc grupa imienna w jego środku nie jest ani podmiotem, ani dopełnieniem,
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

#: Rola spójnika, który stoi wewnątrz swojego zdania: `zatem` w `Milczenie jest
#: zatem wartością.` Od cząstki różni ją to, co to słowo robi: cząstka określa
#: zdanie, a ten spójnik wiąże je z tym, co stoi przed nim, więc `Particle:
#: zatem` mówiłoby o zdaniu, że ma określenie, którego ono nie ma.
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
    # Konstytuenty, do których wyrażenie przyimkowe dochodzi,
    # czyli te, na których zatrzymuje się zejście w górę od modyfikatora
    # (``_gospodarze`` w ``olski/parse.py``):
    # grupa imienna, grupa przymiotnikowa i zdanie składowe.
    # Streszczenie nazywa ten z nich, który stoi najbliżej, bo tam przyłączenie zapadło,
    # a okolicznik zdania nie ma nad sobą żadnego z dwóch pierwszych i zostaje przy zdaniu.
    # Zdanie względne jest tu czwarte i jest zdaniem tak samo jak ``ClauseConjunct``:
    # bez niego okolicznik z jego wnętrza wychodzi w górę do grupy imiennej,
    # którą to zdanie określa, i werdykt nazywa poprzednik zamiast orzeczenia.
    # Fraza bezokolicznikowa jest tu piąta i bierze okolicznik przez to samo ``Complements``,
    # którym bierze go forma osobowa nad nią: bez niej okolicznik wychodzi z niej do zdania,
    # a oba czytania streszczają się wtedy jednym napisem.
    # Czoło pytania jest tu szóste i jest zdaniem tak samo jak ``RelativeCore``:
    # bez niego okolicznik z pytania wychodzi w górę do zdania nadrzędnego,
    # a werdykt nazywa jego orzeczenie zamiast tego, przy którym okolicznik stoi.
    gospodarze=(
        "NP",
        "AP",
        "ClauseConjunct",
        "RelativeCore",
        "InfinitivePhrase",
        "InterrogativeCore",
    ),
    # Symbole, które się koordynują: grupa imienna, grupa przymiotnikowa i zdanie.
    # Człon nazywa tu produkcja spójnikowa i przecinkowa każdego z nich,
    # a nie symbol z końcówką ``Conjunct``, który jest jednym członem, a nie ciągiem.
    współrzędne=("NP", "AP", "Clause"),
    # Zdanie składowe, czyli człon ciągu, który koordynuje `Clause`.
    # Symbol jest tu ten z końcówką `Conjunct`, bo streszczenie pyta o rozpiętość
    # jednego zdania, a nie o ciąg, w którym ono stoi.
    # Symbol jest jeden, bo jeden jest ciąg zdań składowych.
    # Czoło pytania członem tego ciągu nie bywa, więc dopisane tutaj
    # nie rozdzieliłoby ani jednego streszczenia.
    składowe=("ClauseConjunct",),
    # Zdania podrzędne: względne, dopełnieniowe, pytanie zależne i okolicznikowe.
    # Każdy z tych symboli opakowuje takie zdanie, a nie jest symbolem samego zdania,
    # bo `Clause` koordynuje — jest wypisane wyżej wśród współrzędnych —
    # więc zatrzymanie na nim objęłoby także zdanie współrzędne,
    # którego role są rolami tego samego zdania.
    # Czwarty stoi zarazem wśród ról, bo okolicznik jest rolą zdania nad nim,
    # a zdaniem osobnym jest jego wnętrze; :data:`OKOLICZNIKOWY` trzyma wywód.
    # Piąty zdaniem nie jest i mówi o tej liście to, czego cztery pierwsze nie mówią:
    # zatrzymuje ona zejście po role wszędzie, gdzie konstytuent nazywa się całym
    # napisem, a nie tylko przy zdaniu podrzędnym. Wtrącenie w nawiasie jest takim
    # konstytuentem, bo przysłówek w jego środku nie jest okolicznikiem zdania nad
    # nim, a grupa imienna nie jest w nim żadną rolą; :data:`WTRĄCONY` trzyma wywód.
    # Szósty i siódmy stoją tu z tego samego powodu co piąty: człon bez czasownika
    # i dopowiedzenie za dwukropkiem nazywają się całym napisem, bo grupa imienna
    # w środku żadnej z tych dwóch konstrukcji nie zajmuje pozycji zdania nad nią;
    # wywody trzymają :data:`ELIPSA` oraz :data:`DOPOWIEDZIANY`.
    # Zdanie względne bez poprzednika jest tu ósme i jest zdaniem podrzędnym tak
    # samo jak pierwsze z tej listy, a różni je pozycja: tamto określa rzeczownik,
    # a to samo stoi w roli, więc jego role nie są rolami zdania nad nim.
    podrzędne=(
        "RelativeClause",
        "SubordinateClause",
        "InterrogativeClause",
        "FreeRelativeClause",
        OKOLICZNIKOWY,
        WTRĄCONY,
        ELIPSA,
        DOPOWIEDZIANY,
    ),
)

#: Werdykt o tym, czego nikt nie napisał jako zdania: nagłówku, pozycji listy,
#: wierszu tabeli. Odrzucone znaczy „olski tego nie wyprowadza”, a to jest inne
#: zdanie o tekście i inna robota do zrobienia; docs/extraction.md trzyma wywód i
#: mierzy, jak dużą częścią rejestru ta klasa jest.
FRAGMENT = "fragment"

#: Kopula: czasownik, który bierze orzecznik w narzędniku, i jedyny, który go
#: bierze. Lista jest zamknięta i docs/subset.md wywodzi, czego na niej nie ma.
KOPULA = "być|zostać|zostawać|pozostać|pozostawać"

#: Rzeczownik, który orzeka bez czasownika, czyli ten, przy którym polszczyzna
#: opuszcza kopułę: `zadania, o których mowa w ustawie` znaczy `o których jest
#: mowa`, a `jest` nikt tam nie pisze. Jak często ten zwrot pada w rejestrze
#: ustaw, liczy docs/ustawy.md.
#:
#: Lista jest zamknięta i ma jeden lemat, a pozycję ogólną — zdanie z samej grupy
#: imiennej w mianowniku — zmierzono i odrzucono; wywód trzyma
#: docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną.
RZECZOWNIK_ORZEKAJĄCY = "mowa"

#: Spójnik, którym zdanie podrzędne dopełnieniowe zaczepia się o czasownik.
#: Jeden, a nie cała klasa `comp`: `gdy`, `jeśli` i `aby` otwierają okolicznik
#: zdania, więc wpuszczone tą produkcją stanęłyby w pozycji, której nie zajmują.
SPÓJNIK_DOPEŁNIENIOWY = "że"

#: Spójniki, których zdanie polszczyzna stawia przed zdaniem nadrzędnym i za nim.
#: Zajmują one obie pozycje okolicznika, a pozostałe stałe niżej wyliczają to,
#: co każda z tych dwóch list trzyma na zewnątrz.
SPÓJNIKI_WYSUWANE = "gdy|kiedy|jeśli|jeżeli|zanim|nim|choć|chociaż|dopóki|póki|skoro|ponieważ"

#: Spójniki, których zdanie stoi za zdaniem nadrzędnym i tylko tam, bo mówią one
#: o przyczynie dopowiedzianej, a nie o ramie, w której coś zachodzi:
#: `Zostaję w domu, bo pada.` jest polszczyzną, a `Bo pada, zostaję w domu.` nie.
#: Fakt ten jest faktem o słowie, a nie o kierunku, w którym się go używa,
#: i skład trzyma go już o `bo` oraz o `ponieważ`
#: (``staje_na_czele`` w ``olski/skład/spójniki.py``);
#: TODO.md trzyma ruch, którym oba kierunki przeczytałyby jeden leksykon,
#: bo tą samą drogą poszła walencja.
#: Świadka nad bankiem drzew czyta docs/subset.md.
SPÓJNIKI_PO_ZDANIU = "bo|gdyż|albowiem|aż"

#: Spójniki otwierające okolicznik wyrażony zdaniem, czyli obie listy razem.
#: Lista jest zamknięta i stawia formie dwa żądania naraz, bo klasa `comp` niesie
#: także takie spójniki, których ta produkcja wziąć nie może.
#:
#: Spójnik ma stać na czele swojego zdania, czego `bowiem` nie robi: polszczyzna
#: stawia je za pierwszym wyrazem zdania, więc wpuszczone tutaj brałoby pozycję,
#: której nie zajmuje.
#:
#: Zdanie pod spójnikiem z tej listy stoi w trybie oznajmującym, a spójniki, pod
#: którymi stoi tryb przypuszczający, wylicza :data:`SPÓJNIKI_TRYBU` i bierze
#: osobne ciało, bo żądają one od zdania cechy, której ta lista nie żąda.
#:
#: `więc` Morfeusz znakuje tak samo, a nie ma go tu, bo zdania nie podporządkowuje,
#: tylko dokłada skutek: `Program zapisuje ustawienia, więc linter sprawdza tekst.`
#: jest dwoma zdaniami spiętymi spójnikiem po przecinku, więc bierze je lista niżej.
SPÓJNIKI_OKOLICZNIKOWE = f"{SPÓJNIKI_WYSUWANE}|{SPÓJNIKI_PO_ZDANIU}"

#: Spójniki, które niosą cząstkę trybu przypuszczającego: `żeby` to `że` i `by`,
#: `gdyby` to `gdy` i `by`, `aby` to `a` i `by`, a `jakby` to `jak` i `by`.
#: Cząstka stoi w nich raz, więc pod nimi stoi forma na -ł bez własnej cząstki i
#: żąda ich ciało cechą ``tryb`` (:data:`TRYB_POD_SPÓJNIKIEM`): bez tego żądania
#: wyprowadzałoby się `aby program zapisuje ustawienia`, a obietnicą podzbioru
#: jest, że każde zdanie olskiego jest zdaniem polskim.
#:
#: Oba miejsca okolicznika bierze każdy z nich, bo zdanie z każdym polszczyzna
#: wysuwa: `Żeby zostać rezydentem, musisz mieć oszczędności.` obok `Odnotowuję to,
#: żeby złagodzić wrażenie.` Tym różnią się one od :data:`SPÓJNIKI_PO_ZDANIU`.
#:
#: `iżby` i `by` w roli cząstki na tej liście nie stoją, choć Morfeusz zna oba:
#: pierwszego bank drzew nie ma ani raz, a drugie bierze terminal cząstki
#: (:data:`CZĄSTKA_TRYBU`), bo `by` jest jedną formą w dwóch rolach i rozdziela je
#: część mowy, którą słownik daje: `comp` spójnikowi, `part` cząstce.
SPÓJNIKI_TRYBU = "aby|ażeby|żeby|by|gdyby|jakby"

#: Spójniki zdaniowe, przed którymi polszczyzna stawia przecinek: `Plany są
#: niczym, ale planowanie jest wszystkim.` przecinka żąda, a `Program zapisuje
#: ustawienia i linter sprawdza tekst.` nie bierze go wcale. Fakt jest to o słowie,
#: tak samo jak wysunięcie okolicznika (:data:`SPÓJNIKI_WYSUWANE`), więc lista
#: rozdziela spójnik zdaniowy na dwie klasy i obejmuje dwie części mowy naraz,
#: bo Morfeusz zna `więc` jako `comp`, a `ale` jako `conj`. Kogo nie obejmuje,
#: za ile i po co, wywodzi docs/subset.md.
SPÓJNIKI_PRZECINKOWE = "ale|a|lecz|natomiast|więc|zatem|toteż|czyli"

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
SPÓJNIKI_ELIPSY = "a|ale|lecz|natomiast|tylko|czyli"

#: Spójniki, które ten rejestr stawia wewnątrz swojego zdania (:data:`SPÓJNIKOWY`):
#: `Milczenie jest zatem wartością.`, `Reguła jest bowiem tania.`
#:
#: Trzy z nich — `bowiem`, `zaś` i `jednak` — polszczyzna stawia za pierwszym
#: wyrazem zdania i nigdzie poza tym, więc olski nie brał ich wcale; pozostałe
#: stoją zarazem na czele zdania i tam biorą je :data:`SPÓJNIKI_PRZECINKOWE`.
#: Czoła ta lista nie dostaje wcale, i to trzyma jeden napis przy jednym
#: czytaniu: `Cena jest niska, więc gramatyka jest tania.` ma spójnik za
#: przecinkiem, więc bierze go tamta lista.
SPÓJNIKI_WEWNĘTRZNE = "zatem|więc|bowiem|natomiast|zaś|jednak"

#: Rozdzielające `a`, czyli to z `dwa bilety a pięć złotych`: Morfeusz daje mu
#: czytanie przyimka rządzącego mianownikiem, a wyrażenie przyimkowe olskiego tego
#: czytania nie bierze, bo bez tego warunku każde `, a` wychodzi okolicznikiem
#: wysuniętym zdania po przecinku, którego podmiot w mianowniku właśnie stoi.
#: Warunek pada na lemat, a nie na przypadek; czego kryterium na przypadek zabrałoby
#: razem z nim, wywodzi docs/subset.md, i ono trzyma też cenę.
PRZYIMEK_ROZDZIELAJĄCY = "a"

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
#: wyprowadzenia: `Kto płaci?` wyprowadzało się i pytaniem, i zdaniem
#: oznajmującym zamkniętym pytajnikiem, a role obu były te same.
#:
#: Wykluczenie stoi na terminalu, a nie w :func:`admissible`, bo czytanie `subst`
#: jest tym, o które pytają oba czoła. Odbiera ono pozycję wszystkim użyciom tych
#: zaimków naraz, więc razem z czołami wchodzi wszystko, co ta pozycja dotąd
#: niosła: zdanie względne bez poprzednika, ciąg pytań zależnych i orzecznik
#: wysunięty. Wywód i cenę trzyma
#: docs/subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz.
ZAIMEK_PYTAJNO_RZECZOWNY = "kto|co"

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
RAMA_DOMYŚLNA = "nom.acc.inf.comp.int"

#: Rama lematu, o którym leksykon mówi, że biernika nie bierze. Wyliczona z
#: domyślnej, a nie wypisana obok niej, żeby pozycję dopisaną tam widziała i ta.
RAMA_BEZ_BIERNIKA = ".".join(p for p in RAMA_DOMYŚLNA.split(".") if p != "acc")

#: Pozycja przypadkowa, której rama domyślna nie ma, a leksykon ją lematowi daje:
#: nazwa pozycji wraz ze zbiorami lematów, osobno dla formy bez cząstki ``się``
#: i z nią. Kolejność jest kolejnością, w której te pozycje dochodzą do ramy, więc
#: jedna rama wychodzi stąd jednym napisem, a nie dwoma o tych samych pozycjach.
#:
#: Zdanie leksykonu jest tu twierdzące, a przy bierniku ujemne, i przeciwne są
#: domyślności, od których oba odejmują: biernik stoi w ramie domyślnej, a
#: przypadek poza nim nie stoi w niej wcale.
DOKŁADANE = (
    ("dat", Z_CELOWNIKIEM, Z_CELOWNIKIEM_ZWROTNE),
    ("gen", Z_DOPEŁNIACZEM, Z_DOPEŁNIACZEM_ZWROTNE),
)


def _dokładane(zwrotne: bool) -> list[tuple[str, frozenset[str]]]:
    """Pozycje dokładane wraz z lematami tej klasy słowa (:data:`DOKŁADANE`)."""
    return [(nazwa, zwrotni if zwrotne else zwykli) for nazwa, zwykli, zwrotni in DOKŁADANE]


def _rama(
    lemat: str, bez_biernika: frozenset[str], dokładane: Sequence[tuple[str, frozenset]]
) -> str:
    """Rama tego lematu: domyślna bez tego, czego leksykon mu odmawia, i z tym, co mu daje."""
    odjęta = RAMA_BEZ_BIERNIKA if lemat in bez_biernika else RAMA_DOMYŚLNA
    return ".".join([odjęta, *(nazwa for nazwa, lematy in dokładane if lemat in lematy)])


def _klasy_walencyjne(
    bez_biernika: frozenset[str],
    dokładane: Sequence[tuple[str, frozenset]],
    poza: frozenset[str] = frozenset(),
) -> dict[str, str]:
    """Lematy leksykonu zebrane w klasy po ramie, którą leksykon każdemu z nich daje.

    ``poza`` zabiera lematy, które mają ramę wypisaną ręcznie: klasy mają się nie
    zachodzić, a lemat wzięty dwiema byłby dwoma czytaniami tego samego kształtu.
    """
    klasy: dict[str, set[str]] = {}
    for lemat in bez_biernika.union(*(lematy for _nazwa, lematy in dokładane)) - poza:
        klasy.setdefault(_rama(lemat, bez_biernika, dokładane), set()).add(lemat)
    return {rama: "|".join(sorted(lematy)) for rama, lematy in sorted(klasy.items())}


def _walencja() -> tuple[dict[str, str], dict[str, str]]:
    """Leksykon jako klasy walencyjne, osobno dla formy z cząstką ``się`` i bez niej.

    Zwrotność jest drugim wymiarem klucza, a nie częścią lematu, i dlaczego,
    mówi ``olski/walencja.py``, czyli ten, który leksykon czyta dla obu
    kierunków. Tutaj zostaje to, co jest zdaniem samej gramatyki.

    Kluczem klasy jest rama, a nie lemat, bo tak wychodzi produkcja: powstaje raz
    na ramę, a nie raz na lemat. Kopula zabiera leksykonowi swoje lematy, zamiast
    stanąć obok nich, bo klasy mają się nie zachodzić: Walenty mówi o niej to samo
    co leksykon o każdym innym lemacie, a rama kopuli mówi ponadto o narzędniku.

    Zdania leksykonu są tu trzy — o bierniku, o celowniku i o dopełniaczu — a plik
    mówi pięć. Co zdejmuje dwa pozostałe, mówi :data:`RAMA_DOMYŚLNA`.
    """
    return (
        {
            **_klasy_walencyjne(BEZ_BIERNIKA, _dokładane(False), frozenset(KOPULA.split("|"))),
            "nom.inst": KOPULA,
        },
        _klasy_walencyjne(BEZ_BIERNIKA_ZWROTNE, _dokładane(True)),
    )


#: Walencja: co czasownik bierze, wypisane lematami, a nie produkcjami. Ramą jest
#: zbiór dopełnień, nazwanych przypadkiem grupy, którą czasownik bierze, wraz z
#: ``inf`` dla bezokolicznika, bo bezokolicznik przypadka nie ma.
#:
#: Leksykon jest otwarty: stoi w nim czasownik, którego rama jest węższa od
#: domyślnej, a każdy inny bierze domyślną, więc czasownik dopisuje się wpisem, a
#: nie produkcją i nie kosztuje ani jednego przyjętego zdania, dopóki go nie ma.
#: docs/subset.md wywodzi, czym taki leksykon jest, a czym nie jest.
WALENCJA, WALENCJA_ZWROTNA = _walencja()

#: Zaimki rzeczowne, którym Morfeusz daje czytanie `subst`. Dopełniacza żaden z nich
#: nie bierze: `tego podzbioru` jest przymiotnikiem przy rzeczowniku i niczym
#: więcej, a produkcja z dopełniaczem po głowie czyta to drugi raz jako zaimek
#: rządzący rzeczownikiem. Lista jest zamknięta, bo czytanie tych form niczym się
#: nie różni od czytania rzeczownika: `nikt` jest `subst:sg:nom:m1` tak samo jak
#: `parser` jest `subst:sg:nom:m3`. docs/subset.md wywodzi kryterium i mierzy cenę.
ZAIMEK_RZECZOWNY = (
    "to|tamto|owo|kto|któż|ktoś|ktokolwiek|co|cóż|coś|cokolwiek|nikt|nic|wszystko"
)

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
#: techniki prawodawczej”`. Znaki są dwa i są różne, bo polszczyzna otwiera
#: cudzysłów innym znakiem, niż go zamyka, i po to ta para jest jednym napisem
#: obu: produkcja bez znaku zamykającego wpuszczałaby napis niedomknięty.
#:
#: Znaki są tu nazwane osobno, bo używa ich i terminal, i warunek, którym
#: cudzysłów licencjonuje napis przytoczony (:func:`przytoczenie`).
ZNAK_CUDZYSŁOWU_OTWIERAJĄCY = "„"
ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY = "”"
CUDZYSŁÓW_OTWIERAJĄCY = word("interp", lemma=ZNAK_CUDZYSŁOWU_OTWIERAJĄCY)
CUDZYSŁÓW_ZAMYKAJĄCY = word("interp", lemma=ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY)

#: Znaki, którymi cytuje się poza tym rejestrem: cudzysłów maszynowy, pojedynczy,
#: angielski i ostrokątny. Gramatyka bierze samą parę wyżej, a nad którymkolwiek
#: z tych znaków werdykt dopowiada, którą (:func:`_podpowiedź`).
ZAMIENNIKI_CUDZYSŁOWU = ('"', "'", "‘", "’", "‚", "“", "«", "»")

#: Nawias, którym ten rejestr dopowiada obok zdania. Znaki są dwa tak samo jak
#: przy cudzysłowie i z tego samego powodu.
NAWIAS_OTWIERAJĄCY = word("interp", lemma="(")
NAWIAS_ZAMYKAJĄCY = word("interp", lemma=")")

#: Myślnik, którym ten rejestr rozdziela zdanie: `Cena jest niska — gramatyka jest
#: bezkontekstowa.` Stoi obok dwukropka i średnika, bo rozdziela na tej samej
#: wysokości i tak samo nie konkuruje z niczym.
#:
#: Znaki są dwa, bo polszczyzna pisze myślnik pauzą i półpauzą, a łącznik spaja
#: wewnątrz wyrazu — `16-latków`, `UTF-8` — więc tego warunek nie bierze. Co to
#: wykluczenie kosztuje, mierzy docs/subset.md.
MYŚLNIK = word("interp", lemma="—|–")

#: Znak, którym ktoś zamknął zdanie. Nazwany raz, bo bierze go każde ciało zdania.
KONIEC_ZDANIA = word("interp", lemma=".|!|?")

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
#: poza przyimkiem nie ma jej już czym odrzucać, bo zdejmuje ją :func:`po_przyimku`.
ZAIMEK_DZIERŻAWCZY = word(
    "ppron3", case="gen", accentability="akc", post_prepositionality="npraep"
)

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
SPÓJNIK_PRZECINKOWY = word("conj|comp", lemma=SPÓJNIKI_PRZECINKOWE)
SPÓJNIK_BEZ_PRZECINKA = word(
    "conj", bez_lematu=f"{SPÓJNIKI_PRZECINKOWE}|{LEMAT_PRZECZENIA}"
)

#: Spójnik przed członem bez czasownika, i spójnik wewnątrz swojego zdania. Oba
#: pytają o dwie części mowy naraz, tak samo jak :data:`SPÓJNIK_PRZECINKOWY` i z
#: tego samego powodu: Morfeusz zna `więc` jako `comp`, a `ale` jako `conj`.
SPÓJNIK_ELIPSY = word("conj|comp", lemma=SPÓJNIKI_ELIPSY)
SPÓJNIK_WEWNĘTRZNY = word("conj|comp", lemma=SPÓJNIKI_WEWNĘTRZNE)

#: Przyimek wyrażenia przyimkowego, tego zwykłego i tego, które wysunęło zaimek
#: względny. Nazwany raz, bo oba wykluczają ten sam lemat i wykluczenie ma być w
#: obu to samo (:data:`PRZYIMEK_ROZDZIELAJĄCY`).
PRZYIMEK = word("prep", bez_lematu=PRZYIMEK_ROZDZIELAJĄCY, case=V("c"))

#: Przysłówek w okoliczniku: cała część mowy i nic więcej. Stopnia nie żąda, bo
#: `teraz` stopnia nie niesie, a `bardzo` niesie `pos`, i oba są okolicznikami
#: zdania.
PRZYSŁÓWEK = word("adv")

#: Cząstki, które ten rejestr stawia przy zdaniu: `już`, `dopiero`, `także`.
#: Lista jest zamknięta, bo ``part`` niesie całą klasę cząstek naraz, a kryterium
#: na wejście jest jedno: cząstka ma nie mieć czytania, które gramatyka bierze już
#: gdzie indziej. `tylko` go ma — Morfeusz czyta je także jako spójnik, a spójnik
#: bierze koordynacja — więc wpuszczone tutaj dałoby jednemu napisowi dwa
#: wyprowadzenia, i tym samym warunkiem stoi lista spójników przecinkowych obok
#: listy bez przecinka (:data:`SPÓJNIKI_PRZECINKOWE`).
#:
#: Poza listą zostaje przez to `tylko`, `też`, `bo` i `to`, a poza nią z powodu
#: własnego cztery cząstki, które olski bierze albo wyklucza osobno: `nie` przeczy
#: (:data:`PRZECZENIE`), `się` stoi przy czasowniku zwrotnym, `by` niesie tryb
#: przypuszczający (:data:`CZĄSTKA_TRYBU`), a `czy` otwiera pytanie o
#: rozstrzygnięcie, którego ta gramatyka nie ma (docs/subset.md).
CZĄSTKI = (
    "już|jeszcze|dopiero|także|również|nawet|zarazem|naprawdę"
    "|znowu|wreszcie|ponadto|jedynie|niemal|niespełna|zresztą|przynajmniej"
)

#: Cząstka w okoliczniku: sama lista i nic więcej, tak samo jak :data:`PRZYSŁÓWEK`
#: bierze samą część mowy.
CZĄSTKA = word("part", lemma=CZĄSTKI)

#: Lemat cząstki czasownika zwrotnego. Stoi tu osobno od listy wyżej, bo leksykon
#: czyta tę cząstkę jako drugi wymiar lematu, a nie jako określenie: `otwierać`
#: bierze dopełnienie w bierniku, a `otwierać się` go nie bierze (:func:`_klasy`).
#: Pyta o niego terminal oraz warunek na pozycję tej cząstki (:func:`po_słowie`).
LEMAT_ZWROTNY = "się"

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
#: docs/subset.md#cząstka-zwrotna-stoi-po-obu-stronach-swojej-formy-osobowej
#: wywodzi cenę pozycji przedniej i mówi, czego ona nie obejmuje.
SZYKI_CZĄSTKI: tuple[tuple[bool, tuple[Part, ...], tuple[Part, ...]], ...] = (
    (False, (), ()),
    (True, (), (CZĄSTKA_ZWROTNA,)),
    (True, (CZĄSTKA_ZWROTNA,), ()),
)


def _bez_orzecznika(rama: str) -> str:
    """Ta rama bez orzecznika zgodnego, czyli rama zdania, które podmiotu nie ma.

    Orzecznik zgodny zgadza się z podmiotem, więc zdanie bez podmiotu nie ma go z
    czym zgodzić: `Trzeba wolni.` nie jest niczym i `Zgłoszono tania.` też nie.
    Pytają o to obie głowy roli :data:`BEZOSOBOWY`, a każda o inną ramę —
    predykatyw o domyślną (:data:`RAMA_BEZOSOBOWA`), forma nieosobowa o ramę
    swojego lematu — więc odejmowanie jest funkcją, a nie drugą stałą obok nich.
    """
    return ".".join(pozycja for pozycja in rama.split(".") if pozycja != "nom")


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
PREDYKATYWY = "można|trzeba|warto|wiadomo|widać|wolno|słychać|znać"

#: Predykatyw na czele swojego zdania: sama lista i nic więcej, tak samo jak
#: :data:`CZĄSTKA`.
PREDYKATYW = word("pred", lemma=PREDYKATYWY)

#: Przysłówek przy przymiotniku: ta sama część mowy i żądanie stopnia. Stopień ma
#: przysłówek odprzymiotnikowy, a pierwotny go nie ma, i tylko pierwszy z tych
#: dwóch przymiotnik określa, więc `tu duży` z tej pozycji wypada, a `bardzo duży`
#: zostaje. Terminale są przez to dwa, choć część mowy jedna: warunek należy do
#: jednego gospodarza, a drugi bierze przysłówek każdy. Czym jest żądanie obecności
#: cechy, mówi ``niesione`` w olski/grammar.py, a cenę tego warunku trzyma
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
TRYB_FORMY_NA_Ł = f"{TRYB_OZNAJMUJĄCY}.{TRYB_POD_SPÓJNIKIEM}"

#: Przeczenie jako para: co dochodzi na początek ciała i jaką wartość cechy
#: ``negacja`` to ciało wypuszcza. Para, bo obie strony powstają razem: ciało bez
#: cząstki, które nie ogłasza ``aff``, przepuszcza dopełniacz negacji tam, gdzie
#: żadnego przeczenia nie ma, i cechy, której konstytuent nie niesie, unifikacja
#: nie sprawdza. Zdanie przeczące ma dokładnie jedno przeczenie, więc lista jest
#: pętlą po dwóch wartościach, a nie cząstką doklejaną gdziekolwiek.
PRZECZENIA: tuple[tuple[tuple[Part, ...], str], ...] = (((), "aff"), ((PRZECZENIE,), "neg"))


def _klasy(zwrotne: bool) -> list[tuple[dict[str, str], str]]:
    """Klasy walencyjne: warunek na lemat i rama, którą ten warunek wpuszcza.

    Ostatnia jest klasa domyślna, i jest nią warunek ujemny na wszystkie lematy
    leksykonu naraz, bo klasy mają się nie zachodzić: forma wzięta dwiema klasami
    byłaby dwoma czytaniami tego samego kształtu.

    Pyta on o formę, a nie o jedno jej czytanie, bo rama jest własnością formy:
    zapytany o czytanie rozdziela lematy zamiast form i wpuszcza ramę domyślną
    formie, której lemat leksykon wymienia. Reprodukcję, cenę i zysk trzyma
    docs/subset.md#walencja-jest-leksykonem-o-ramie-domyślnej.

    Forma z cząstką ``się`` pyta o swój leksykon, bo jest innym czasownikiem;
    lemat, którego tamten leksykon nie wymienia, bierze ramę domyślną tak samo
    jak każdy inny nieznany.
    """
    leksykon = WALENCJA_ZWROTNA if zwrotne else WALENCJA
    klasy = [({"lemma": lematy}, rama) for rama, lematy in leksykon.items()]
    return [*klasy, ({"bez_lematu_formy": "|".join(leksykon.values())}, RAMA_DOMYŚLNA)]


def _formy_skończone(
    warunek: dict[str, str],
) -> list[tuple[list[Part | Głowa], Var | str, str]]:
    """Ciała formy osobowej czasownika, każde wraz z osobą i trybem, które niesie.

    Trzy pierwsze, bo czas przeszły niesie osobę inaczej niż teraźniejszy. ``fin``
    niesie osobę i liczbę, a rodzaju nie ma; ``praet`` odwrotnie, więc osoba trzecia
    jest w nim wpisana tutaj, a bez tego ``Ja napisał program.`` się wyprowadza:
    cechy, której konstytuent nie niesie, unifikacja nie sprawdza. Osobę pierwszą
    i drugą wnosi aglutynant, czyli końcówkę, którą Morfeusz odcina od formy —
    ``napisałem`` wchodzi tu jako ``napisał`` i ``em`` — i która liczbę ma tę samą
    co czasownik przy niej.

    Dwa ostatnie są trybem przypuszczającym i różnią się od dwóch nad sobą jedną
    cząstką (:data:`CZĄSTKA_TRYBU`): ``odzyskałby`` i ``odzyskałbym``. Dostaje ją
    czas przeszły i on jeden, bo tak stawia tę cząstkę polszczyzna: ``zapisujeby``
    nie jest niczym. Ciała są dwa, a nie jedno z cząstką pominiętą, bo cena trybu
    ma być osobną liczbą, a sonda różnicowa bierze ją zdejmowaniem ciał.

    Tryb wychodzi stąd wartością cechy, bo pyta o niego spójnik, który cząstkę
    niesie sam (:data:`SPÓJNIKI_TRYBU`). Forma na -ł bez cząstki wychodzi z obiema
    wartościami naraz (:data:`TRYB_FORMY_NA_Ł`), a ta sama forma z aglutynantem już
    nie: aglutynant zajmuje miejsce, które pod takim spójnikiem zajmuje jego własna
    końcówka, więc polszczyzna ma ``żebym wiedział``, a nie ``żeby wiedziałem``.

    Głowa stoi w każdym ciele, choć dwa z pięciu mają jedną część: ciało wychodzi
    stąd do produkcji zwrotnej, która dopisuje mu cząstkę ``się``, a ciało o
    dwóch częściach bez głowy nie powstaje.
    """
    czasownik = word("praet", number=V("n"), gender=V("g"), **warunek)
    aglutynant = word("aglt", number=V("n"), person=V("p"))
    return [
        (
            [Głowa(word("fin|impt", number=V("n"), person=V("p"), **warunek))],
            V("p"),
            TRYB_OZNAJMUJĄCY,
        ),
        ([Głowa(czasownik)], "ter", TRYB_FORMY_NA_Ł),
        ([Głowa(czasownik), aglutynant], V("p"), TRYB_OZNAJMUJĄCY),
        ([Głowa(czasownik), CZĄSTKA_TRYBU], "ter", TRYB_PRZYPUSZCZAJĄCY),
        ([Głowa(czasownik), CZĄSTKA_TRYBU, aglutynant], V("p"), TRYB_PRZYPUSZCZAJĄCY),
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

    Ten sam kształt ma zdanie względne (`reguła, która rozstrzyga`, `ustawa,
    której przepisy obowiązują`) i pytanie (`które zadania mają charakter
    obowiązkowy`), a różni je samo czoło, więc deklaracje powstają raz i biorą
    czoło nazwą symbolu. Wypisane osobno dla każdego czoła rozeszłyby się na
    pierwszym dopisanym szyku, a rozejście widać dopiero na zdaniu, którego
    jedno z czół nie wyprowadza.

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

    # Podmiot za wysuniętym dopełnieniem stoi po czasowniku i przed nim, choć
    # zdanie główne ma ten szyk tylko w pierwszej wersji: `które ktoś napisał`
    # jest w polszczyźnie zwyczajne, a `Teksty ktoś napisał` nie, i różni je to,
    # że czoło wysuwa polszczyzna zawsze, a dopełnienie z wyboru. Wypowiada to
    # sam warunek precedencji: żąda on czoła na pierwszym miejscu i nie żąda
    # niczego od dwóch pozostałych córek.
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
#: swojego czasownika, bo nad zdaniem nie ma z czym ich zgadzać.
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
    "ClauseConjunct": ("number", "gender", "person", "valency", "negacja", "dostawka"),
    "Clause": ("dostawka",),
    "Predicate": ("valency", "negacja"),
    "RelativeCore": ("person", "valency", "negacja"),
    "InterrogativeCore": ("person", "valency", "negacja"),
    OKOLICZNIKOWY: ("tryb",),
    ORZEKAJĄCY: ("case", "number"),
    "Subject": ("case",),
    "Object": ("case",),
    "Predicative": ("case",),
    "Modifier": ("case",),
    "RelativeModifier": ("case",),
    "InterrogativeModifier": ("case",),
    "Complements": ("czoło",),
    "NPConjunct": ("accommodability",),
}


def build() -> Grammar:
    grammar = Grammar(start="Sentence", nie_wypuszczane=NIE_WYPUSZCZANE)

    # Przymiotnik przy rzeczowniku i przymiotnik w orzeczniku, nazwane raz, bo
    # oba wykluczają ten sam lemat i wykluczenie ma być w każdym ciele to samo.
    # Zaimka względnego nie bierze ani jeden z nich: pozycję ma on jedną i stoi
    # ona niżej, na czole zdania względnego.
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
    for symbol, słowo in (
        ("Adjective", word("adj", bez_lematu=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE)),
        ("Adjective", word("ppas", **AGREE)),
        ("Adjective", word("pact", **AGREE)),
        ("PredicativeAdjective", word("adj|ppas", bez_lematu=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE)),
    ):
        grammar.rule(symbol, [Głowa(słowo)])
        grammar.rule(symbol, [PRZYSŁÓWEK_STOPNIA, Głowa(słowo)])
    przymiotnik = nt("Adjective", **AGREE)
    orzecznikowy = nt("PredicativeAdjective", **AGREE)

    grammar.rule("Sentence", [Głowa(nt("Clause")), KONIEC_ZDANIA])

    # Dwukropek otwierający zdanie: `Cena jest niska: gramatyka jest
    # bezkontekstowa.` Produkcja należy do zdania, a nie do zdania składowego, bo
    # `A, B: C.` czyta się jako `(A, B): C`, a na poziomie `Clause` byłaby
    # prawostronnie rekurencyjna razem z przecinkiem i wypuszczała `A, (B: C)`.
    #
    # Jednoznaczności nie odbiera ani jednemu zdaniu i wynika to z gramatyki, nie
    # z przebiegu: dwukropka nie bierze żaden inny terminal, więc zdanie z nim nie
    # ma bez tej produkcji ani jednego czytania (``bez_licencji``). Niezmiennik
    # pilnuje tests/test_subset.py, a wywód wraz z zakupem i z tym, czego ta
    # produkcja nie bierze, trzyma docs/subset.md.
    # Średnik rozdziela zdanie tak samo i tym samym kształtem: `Dlaczego, mówi
    # docs/linter.md; ile ten pakiet kosztował, mówi docs/firing-rates.md.` Ciała
    # są mimo to dwa, a nie jedno biorące oba znaki, bo zakup każdego z nich jest
    # osobną liczbą i sonda bierze ją zdejmowaniem ciał.
    # Myślnik jest trzeci i rozdziela tym samym kształtem (:data:`MYŚLNIK`).
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
    # napisowi: grupa imienna zdaniem nie jest, więc napis wzięty tym ciałem nie
    # ma wyprowadzenia tamtym, i to jest to, co pilnuje tests/test_subset.py.
    #
    # Myślnik i średnik tej pozycji nie dostają, bo ten rejestr nie pisze za nimi
    # samej grupy: myślnikiem wtrąca całe zdanie, a średnikiem rozdziela dwa.
    grammar.rule(DOPOWIEDZIANY, [DWUKROPEK, Głowa(nt("NP"))])
    grammar.rule("Sentence", [Głowa(nt("Clause")), nt(DOPOWIEDZIANY), KONIEC_ZDANIA])

    # Koordynacja jest jednym członem, znakiem koordynacji i resztą,
    # na każdym z trzech poziomów, które ją mają.
    # To, co człon może zawierać, rozstrzyga,
    # do czego koordynację da się przyłączyć z zewnątrz,
    # i na tym stoi zawężenie zasięgu, a nie na kształcie tych produkcji.
    # X → X conj X powiedziałoby to samo o zasięgu
    # i tablica Earleya bierze taką produkcję bez skargi,
    # a różni je liczba czytań ciągu współrzędnego; TODO.md trzyma ten wybór.
    #
    # Znakiem koordynacji jest spójnik albo przecinek,
    # i dlatego stoją po dwie produkcje na poziom,
    # a nie jedna z osobnym symbolem na oba znaki.
    # Wspólny symbol powiedziałby to samo raz,
    # ale przecinek przestałby stać przy swoim poziomie,
    # a cena i zakup każdego z trzech są osobnymi liczbami,
    # których cenę wzięto zdejmowaniem po jednej.
    #
    # Zasięg koordynacji wywodzi docs/subset.md pod „Nothing above a
    # coordination distributes into it”.
    #
    # Tryb ciąg wypuszcza z członu pierwszego, a od pozostałych nie żąda niczego,
    # i jest to ta sama granica: spójnik trybu nad ciągiem żąda formy na -ł od
    # członu, którym ten ciąg jest, a nie od każdego z osobna. Zmienna wspólna
    # żądałaby jej od wszystkich i zabierałaby przy tym zdania już przyjęte, bo
    # `Program zapisuje ustawienia, a linter sprawdziłby tekst.` koordynuje tryb
    # oznajmujący z przypuszczającym.
    #
    # Ciągiem albo jednym członem ogłasza się każde z tych ciał (:data:`CIĄG`).
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

    # Zdanie bez podmiotu: Zapisz plik podmiotu nie ma i nie potrzebuje, tak samo
    # jak Zapisuje ustawienia.
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

    # Zdanie składowe, w którym ten rzeczownik orzeka, a okolicznik stoi w nim
    # córką żądaną, a nie miejscem wyliczonym: kopuła opuszczona żąda tego, o czym
    # mowa, więc `Mowa o zadaniach.` jest polszczyzną, a `Mowa.` nie jest.
    # Rozwinięcie szyku tej deklaracji nie pisze, bo pisałoby ciało bez okolicznika
    # razem z nim.
    #
    # Ciało drugie stoi pod czołem zdania względnego niżej, bo tam to wyrażenie
    # jest wysunięte. Co zdjęcie któregoś z dwóch kosztuje, mierzy
    # docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną.
    grammar.rule("ClauseConjunct", [Głowa(nt(ORZEKAJĄCY)), okoliczniki], tryb=TRYB_OZNAJMUJĄCY)

    # Głowa, która orzeka bez podmiotu: predykatyw — `Trzeba czytać dokumenty.`,
    # `Nie widać granicy.` — oraz forma nieosobowa czasownika — `Zgłoszono
    # usterkę.`, `Nie mówiono o tym.` Rama i `Complements` są u obu te same, co u
    # czasownika, a różni je to, skąd rama przychodzi: predykatyw ma jedną wpisaną
    # obok listy lematów, a forma nieosobowa bierze ramę swojego lematu tak samo
    # jak forma osobowa (:func:`_klasy`). Orzecznika zgodnego nie ma żadna z tych
    # dwóch ram, bo zgadzać się on nie ma z czym (:func:`_bez_orzecznika`).
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
        )
        for zwrotne, cząstka in ((False, ()), (True, (CZĄSTKA_ZWROTNA,))):
            for warunek, rama in _klasy(zwrotne):
                grammar.rule(
                    BEZOSOBOWY,
                    [*przeczenie, Głowa(word("imps", **warunek)), *cząstka],
                    valency=_bez_orzecznika(rama),
                    negacja=negacja,
                )

    # Zdaniem składowym jest ta głowa wprost, bo `Predicate` ma ciało z podmiotem,
    # którego to zdanie nie ma. Ciała są dwa, a nie jedno, bo zakup ciała bez
    # wypełnienia — `Nie wiadomo.`, `Zgłoszono.` — jest osobną liczbą;
    # `Complements` pustego ciała nie ma, a dodane tam dawałoby je każdemu
    # czasownikowi naraz.
    grammar.rule(
        "ClauseConjunct",
        [
            Głowa(nt(BEZOSOBOWY, valency=V("w"), negacja=V("z"))),
            nt("Complements", valency=V("w"), negacja=V("z")),
        ],
        tryb=TRYB_OZNAJMUJĄCY,
    )
    grammar.rule("ClauseConjunct", [nt(BEZOSOBOWY)], tryb=TRYB_OZNAJMUJĄCY)

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

    # Czasownik przed podmiotem: Nadchodzi druga rewolucja, Są oni obdarzeni
    # rozumem. Podmiot nie bierze tu własnych dopełnień, więc Zapisuje program
    # ustawienia się nie wyprowadza i żadne zdanie SVO nie konkuruje z czytaniem
    # samego siebie od czasownika. Szyku odwrotnego te dwie deklaracje nie mają z
    # tego samego powodu, dla którego nie ma go deklaracja wyżej: składa go
    # podmiot z orzeczeniem.
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

    # Człon, którego czasownik ten rejestr opuszcza: `Milczenie obejmuje wybór, a
    # nie zdanie.`, `Warstwa pyta o Przyłączenie, czyli o obiekt składniowy.`
    #
    # Wypełnieniem jest konstytuent, który zajmuje w zdaniu pozycję, a ciała są
    # osobne, po jednym na wypełnienie, bo cena każdego z nich jest osobną
    # liczbą. Przysłówka wśród nich nie ma, bo zmierzono go i nie wyszedł
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

    # A fronted adjunct. Polish modifies a noun with a prepositional phrase only
    # from behind it, so in front of a clause there is no noun to attach to and
    # the attachment ambiguity docs/subset.md is about cannot arise.
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
        [Głowa(nt("RelativeCore", number=V("n"), gender=V("g"))), PRZECINEK],
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

    # A predicate is a verb with what it takes. What it takes is one symbol
    # rather than a list of bodies, so that the finite verb and the infinitive
    # below share it instead of each carrying its own copy.
    grammar.rule("Predicate", [czasownik])
    grammar.rule(
        "Predicate",
        [
            Głowa(czasownik_ramy),
            nt(
                "Complements",
                number=V("n"),
                gender=V("g"),
                valency=V("w"),
                negacja=V("z"),
            ),
        ],
    )

    # A modal and its infinitive. Powinien inflects for gender and not for
    # person, so the clause it heads agrees with its subject in gender and
    # leaves person to whatever else constrains it.
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
    for przeczenie, _ in PRZECZENIA:
        grammar.rule("InfinitivePhrase", [*przeczenie, Głowa(word("inf"))], valency="inf")

    # Zdanie podrzędne dopełnieniowe: `pomiar mówi, że poziom odpowiada`. Pozycję
    # ramy niesie ono tak samo jak dopełnienie i bezokolicznik, więc żądanie wobec
    # czasownika stoi raz, tutaj, a nie w każdym szyku, w którym to zdanie stoi.
    # Przecinek należy do tego konstytuentu, a nie do produkcji nad nim, i tym
    # różni się podrzędność od koordynacji; wywód trzyma docs/subset.md.
    # Przecinek zamykający dokłada :func:`_zamykane`.
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

    # Te same dwie pozycje nad całym ciągiem współrzędnym, bo `Dwoisz się i troisz,
    # aby rozwiązać problemy.` mówi o obu członach naraz, a `Mieszkał z ojcem i nie
    # chciał, żeby ktoś wiedział.` o samym drugim. Ciała powyżej dają czytanie
    # drugie, te dwa dają pierwsze, i bez nich olski wybiera przez przeoczenie
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

    # More than one adjunct, because postępować wobec innych w duchu braterstwa
    # has two and a verb that takes one of them takes any number.
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

    # What is predicated of the subject: an adjective phrase agreeing with it,
    # or a noun phrase in the instrumental. Both are what być takes, and the
    # first is also what rodzą się wolni i równi predicates without one.
    #
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
    # leksykonu, bo otwierać bierze dopełnienie w bierniku, a otwierać się nie.
    # Pozycje cząstki stoją obie przy tej formie (:data:`SZYKI_CZĄSTKI`);
    # przy bezokoliczniku i w oddaleniu od swojej formy cząstka pozycji nie ma.
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
        for warunek, rama in _klasy(zwrotne):
            for ciało, osoba, tryb in _formy_skończone(warunek):
                for przeczenie, negacja in PRZECZENIA:
                    grammar.rule(
                        "Verb",
                        [*przed, *przeczenie, *ciało, *za],
                        person=osoba,
                        valency=rama,
                        negacja=negacja,
                        tryb=tryb,
                    )

    # Bezokolicznik pyta o leksykon niezwrotny i ma pętlę osobną zamiast warunku
    # wewnątrz tamtej. Cząstki nie bierze, więc `zaczyna otwierać się` nie ma
    # wyprowadzenia, i jest to ta sama dziura, którą docs/subset.md wypisuje pod
    # walencją: `się` dochodzi do czasownika, przy którym stoi, a nie do tego, do
    # którego należy.
    #
    # Fraza bez własnej cząstki wypuszcza negację, którą wzięła od dołu, więc
    # `Nie chcę czytać książki` żąda dopełniacza od dopełnienia stojącego pod
    # bezokolicznikiem, i tak samo przez łańcuch dowolnej długości.
    #
    # Fraza z własną cząstką nie wypuszcza tej cechy wcale i tym zamyka
    # przenoszenie: `Program ma nie zapisywać ustawień` przeczy bezokolicznikowi,
    # a forma osobowa nad nim nie przeczy. Nieobecnością cechy broni się tu tak
    # samo jak grupa współrzędna, która rodzaju nie niesie.
    for warunek, rama in _klasy(zwrotne=False):
        grammar.rule(
            "InfinitivePhrase",
            [Głowa(word("inf", **warunek)), nt("Complements", valency=rama, negacja=V("z"))],
            valency="inf",
            negacja=V("z"),
        )
        grammar.rule(
            "InfinitivePhrase",
            [
                PRZECZENIE,
                Głowa(word("inf", **warunek)),
                nt("Complements", valency=rama, negacja="neg"),
            ],
            valency="inf",
        )

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
    # A coordination of noun phrases is plural and third person whatever its
    # conjuncts are, and it carries no gender: Polish resolves the gender of
    # rozum i sumienie by rules unification cannot state, and a feature a phrase
    # does not carry is one no agreement can fail against.
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

    # Noun phrases: a noun, an agreeing adjective before it, a genitive
    # modifier after it. Agreement is the unification, not a separate check,
    # and every one of these shares the same three variables, so they are named
    # once. A conjunct headed by a noun is third person by saying so; leaving
    # that off one of them would quietly let a first person verb take it.
    grammar.rule("NPConjunct", [przymiotnik, Głowa(nt("NPConjunct", **AGREE))], person="ter")
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
        # Polish puts an attributive adjective after the noun in terminology:
        # plik konfiguracyjny, język polski. Both orders are the language, so both
        # are here, and where a sentence admits both readings it is ambiguous.
        grammar.rule("NPConjunct", [Głowa(głowa), przymiotnik], person="ter")
        grammar.rule("NPConjunct", [Głowa(głowa), nt("Modifier")], person="ter")
        # Oba szyki przydawki naraz: dobrem wspólnym wszystkich obywateli, zadania
        # ochrony ludności. Bez tej pozycji dopełniacz dochodzi tylko do przymiotnika
        # stojącego przed rzeczownikiem, więc termin nazwany drugim szykiem nie ma
        # wyprowadzenia, a rejestr ustaw nazywa tak swoje terminy zdanie po zdaniu:
        # docs/ustawy.md trzyma, ile ta pozycja tam daje i ile odbiera.
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), przymiotnik, nt("NP", case="gen")],
            person="ter",
        )
        # Wyrażenie przyimkowe po rzeczowniku, który już coś przy sobie ma: akcja
        # zbrojna w Strefie Gazy, rozmieszczenie ogrodów działkowych w Polsce,
        # zadania ochrony ludności w gminie. Bez tych trzech pozycji przyłączenie do
        # rzeczownika w takiej grupie nie istnieje, a zdanie wychodzi jednym
        # czytaniem przez czasownik. Trzecia idzie razem z przydawką wyżej: bez niej
        # wyrażenie po takim terminie dochodzi do dopełniacza i do nikogo więcej,
        # czyli gramatyka wybiera przyłączenie, którego wybierać nie ma.
        grammar.rule("NPConjunct", [Głowa(głowa), przymiotnik, nt("Modifier")], person="ter")
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), nt("NP", case="gen"), nt("Modifier")],
            person="ter",
        )
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), przymiotnik, nt("NP", case="gen"), nt("Modifier")],
            person="ter",
        )
    # Grupa liczebnikowa, w dwóch ciałach, bo polszczyzna ma dwa przyłączenia
    # liczebnika i Morfeusz rozdziela je cechą `accommodability`.
    #
    # Liczebnik zgodny stoi jak przymiotnik przy rzeczowniku i zgadza się z nim
    # we wszystkich trzech cechach: `dwie rzeczy`, `cztery wozy`, `oba pliki`.
    # Głową jest rzeczownik, tak samo jak pod przymiotnikiem wyżej.
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

    # A pronoun is the one conjunct that carries its own person, which is the
    # whole reason it is here: without one, first and second person subjects
    # have no noun phrase to be.
    grammar.rule("NPConjunct", [word("ppron3|ppron12", person=V("p"), **AGREE)])

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

    # Adjective phrases, coordinated the same way and agreeing throughout, so
    # that wolni i równi is one predicative and wolna i równi is none.
    grammar.rule("AP", [nt("APConjunct", **AGREE)])
    grammar.rule("AP", [Głowa(nt("APConjunct", **AGREE)), SPÓJNIK_BEZ_PRZECINKA, nt("AP", **AGREE)])
    grammar.rule("AP", [Głowa(nt("APConjunct", **AGREE)), PRZECINEK, nt("AP", **AGREE)])
    # A passive participle is an adjective for these purposes, and it keeps the
    # complement its verb governed: obdarzeni rozumem i sumieniem.
    grammar.rule("APConjunct", [orzecznikowy])
    grammar.rule("APConjunct", [Głowa(orzecznikowy), nt("NP", case="inst")])
    # Trzecie miejsce, do którego wyrażenie przyimkowe dochodzi: powiązani z
    # interesami postkomunistów, przeznaczany na budowę.
    grammar.rule("APConjunct", [Głowa(orzecznikowy), nt("Modifier")])

    # A preposition governs a case, and the noun phrase has to be in it.
    # One lemma is excluded and it is excluded by name
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

    # Cząstka przy zdaniu, tym samym prawem co przysłówek nad nią: zdanie przyjęte
    # z `już` albo `dopiero` wychodziłoby bez tej etykiety `valid` bez słowa o tym,
    # co olski w nim przyjął. Lista lematów jest zamknięta i kryterium na nią stoi
    # przy :data:`CZĄSTKI`.
    grammar.rule(CZĄSTKOWY, [CZĄSTKA])

    # Spójnik wewnątrz swojego zdania: `Milczenie jest zatem wartością.`,
    # `Reguła jest bowiem tania.` Rola jest osobna od cząstki, bo ten spójnik wiąże
    # zdanie z tym, co stoi przed nim, zamiast je określać (:data:`SPÓJNIKOWY`).
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
    # się zepsuć`, `wszystko, co zjadł`. Ciało jest osobne, bo lemat ma inną część
    # mowy niż `który`, a nie dlatego, że pozycja jest inna — pozycja jest ta sama.
    # Poprzednikiem jest tu rzeczownik rodzaju nijakiego, bo tego rodzaju są oba
    # zaimki, i o zgodność z nim pyta zdanie względne (:func:`zaimek_czoła`).
    # Ten rejestr pisze to zdanie częściej niż pytanie, a jedno wykluczenie stoi
    # pod obydwoma (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`).
    grammar.rule(
        "RelativePronoun",
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
    # Wyrażenie przyimkowe przy tym zaimku: `Kto z państwa senatorów jest za?`
    # Grupa pytajna wyżej bierze je przez grupę imienną, którą ma w środku, a to
    # czoło grupy imiennej nie ma, więc pozycja jest tu osobnym ciałem. Bez niej
    # zdanie z takim wyrażeniem wychodzi przyjęte i mówi o zdaniu nieprawdę, bo
    # wyrażenie przyłącza się wtedy do orzeczenia: pytanie jest o `kto z państwa`,
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
    # Pozycję ramy zajmuje cały ciąg, a nie każdy człon osobno, bo czasownik bierze
    # jedno wypełnienie (``Complements``), i dlatego ciąg jest tu symbolem, a nie
    # drugim ciałem zdania podrzędnego.
    #
    # Znakiem ciągu jest spójnik, a nie sam przecinek: przecinek w tym miejscu
    # zamyka zdanie podrzędne (:func:`_zamykane`), więc ciało z nim samym dałoby
    # jednemu napisowi dwa wyprowadzenia. Ten rejestr pisze ten ciąg spójnikiem.
    #
    # Bez wykluczenia z pozycji rzeczownej (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`)
    # człon drugi wyprowadza się zdaniem współrzędnym, którego podmiotem albo
    # dopełnieniem jest ten zaimek, więc ciąg stoi razem z tamtym wykluczeniem.
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


def _nierozstrzygnięte(przyłączenie: Przyłączenie) -> str:
    """Modyfikator i głowy, do których dochodzi, jako jeden wiersz werdyktu.

    Cudzysłów jest treścią, bo modyfikator jest ciągiem wziętym ze zdania i sam
    zawiera odstępy, więc bez niego nie widać, gdzie się kończy. Głowy dostają
    go tak samo, choć każda jest jednym słowem: pierwsze, co o nich trzeba
    wiedzieć, to że stoją w zdaniu tak, jak je autor napisał.
    """
    głowy = ", ".join(f"„{głowa}”" for głowa in przyłączenie.gospodarze)
    return f"„{przyłączenie.modyfikator}”{PRZYŁĄCZONY_DO}{głowy}"


def _rozbieżny(rozbieżność: Rozbieżność) -> str:
    """Konstytuent i liczba jego czytań, jako jeden wiersz werdyktu.

    Wiersz ten mówi, gdzie w zdaniu leży wieloznaczność, której nie widać
    w streszczeniach czytań pod nim, i tylko tyle: różnicę autor odczyta z
    konstytuenta, a nazwana byłaby lematem, którego liczba czytań nie liczy
    (:class:`Rozbieżność`).
    """
    return f"„{rozbieżność.konstytuent}” reads {rozbieżność.ile} ways"


def _podpowiedź(nielicencjonowane: tuple[str, ...]) -> str:
    """Znaki, którymi ten rejestr cytuje, gdy autor zacytował innymi; inaczej nic.

    Czemu podpowiedź dostaje ten znak, a nie łącznik, mówi
    docs/subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka.

    Pytanie jest o pierwszy i ostatni znak formy, bo Morfeusz scala cudzysłów
    pojedynczy ze słowem w jedną formę — ``'Zasad'`` wychodzi jednym segmentem —
    a apostrof w środku słowa nie cytuje: ``fact's`` brałby podpowiedź, gdyby
    warunek pytał o samo zawieranie.
    """
    if not any(
        forma[0] in ZAMIENNIKI_CUDZYSŁOWU or forma[-1] in ZAMIENNIKI_CUDZYSŁOWU
        for forma in nielicencjonowane
    ):
        return ""
    #  Średnik otwiera podpowiedź, bo tym znakiem wycina ją kolejka form bez
    #  licencji (docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze).
    return (
        f"; a quotation opens with {ZNAK_CUDZYSŁOWU_OTWIERAJĄCY}"
        f" and closes with {ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY}"
    )


@dataclass(frozen=True)
class Verdict:
    """What olski says about one sentence."""

    #: Zdanie tak, jak stoi w tekście. Segmenty są krawędziami grafu, a nie
    #: listą, więc sklejone dają naraz każdy podział, jaki Morfeusz na formie
    #: widzi: ``ktoś`` wychodzi wtedy jako ``kto ktoś ś``.
    text: str
    result: Result
    #: Formy nie do ominięcia, którym żadna produkcja nie bierze ani jednego
    #: czytania: odrzucenie stanęło na nich, a nie na strukturze. Pola bez
    #: wartości domyślnej, bo pusta krotka jest tu twierdzeniem o zdaniu, a
    #: ``Nowa program zapisuje ustawienia.`` ma je puste i jest odrzucone.
    nielicencjonowane: tuple[str, ...]
    #: Forma, której nie wzięła ani jedna analiza częściowa, czyli miejsce, na
    #: którym odrzucenie stanęło; ``None``, gdy analiza doszła do ostatniego
    #: znaku zdania. Pola bez wartości domyślnej z tego samego powodu co wyżej:
    #: ``None`` jest tu twierdzeniem, a nie brakiem odpowiedzi.
    zatrzymanie: str | None

    @property
    def status(self) -> str:
        if not SENTENCE_CLOSE.search(self.text):
            return FRAGMENT
        return self.result.status

    @property
    def readings(self) -> list[dict[str, str]]:
        """Streszczenia czytań, każde raz (:func:`streszczenia`).

        Lista jest po to, żeby pokazać różnicę między czytaniami,
        a różnicę spoza zasięgu streszczenia nazywa wiersz o konstytuencie
        (:func:`_rozbieżny`), więc powtórzony napis nie zostawia jej nienazwanej.
        Liczbę czytań podaje las (:attr:`Result.ile`),
        więc skrócenie tej listy jej nie rusza.
        """
        return streszczenia(self.result.readings, DEKLARACJA)

    @property
    def rozbieżne(self) -> list[Rozbieżność]:
        """Konstytuenty rozbieżne, którym streszczenia naprawdę się różnią.

        Jedno streszczenie znaczy, że streszczenie tej różnicy nie widzi
        (:class:`Rozbieżność`), a wypisane byłoby wierszem bez treści.
        Warunek stoi tu raz na oba wydruki, na wiersz poleceń i na witrynę,
        bo napisany dwa razy rozjechałby się po cichu.
        """
        return [r for r in self.result.rozbieżności if len(r.czytania) > 1]

    def explain(self) -> str:
        if self.status == FRAGMENT:
            return "not a sentence: nothing punctuates it as one"
        if self.result.valid:
            return "one reading"
        if self.result.rejected:
            if self.nielicencjonowane:
                # Cudzysłów jest treścią: najczęstszą formą bez licencji jest
                # przecinek, a lista rozdzielana przecinkami gubi bez niego granice.
                formy = ", ".join(f"„{forma}”" for forma in self.nielicencjonowane)
                podpowiedź = _podpowiedź(self.nielicencjonowane)
                return f"no reading: no production takes {formy}{podpowiedź}"
            if self.zatrzymanie is None:
                return "no reading: the analysis reaches the end and nothing closes the sentence"
            return f"no reading: the analysis stops at „{self.zatrzymanie}”"
        przyłączenia = self.result.przyłączenia
        differing = sorted(
            role
            for role in self.result.różniące
            # Przyłączenie nazwane niżej mówi o tej roli więcej niż sama jej
            # nazwa, więc wypisana obok byłaby tym samym zdaniem dwa razy.
            if not (przyłączenia and role == PRZYŁĄCZANY)
        )
        # Liczba i role wychodzą z lasu, więc granica wyliczania sięga listy
        # czytań i nie sięga tego wiersza: liczba jest liczbą, a nie „64+”.
        count = f"{self.result.ile} readings"
        if differing:
            count += f", differing in {', '.join(differing)}"
        return "; ".join(
            [
                count,
                *map(_nierozstrzygnięte, przyłączenia),
                *map(_rozbieżny, self.result.rozbieżności),
            ]
        )


#: The closed-class parts of speech. A noun reading of a form that also reads as
#: one of these is competing with the reading the form nearly always carries.
CLOSED_CLASS = frozenset({"prep", "conj", "comp", "qub", "part", "pred", "interj"})

#: The seven cases. A noun reading carrying all of them inflects for nothing, so
#: no case demand can fail against it.
EVERY_CASE = frozenset({"nom", "gen", "dat", "acc", "inst", "loc", "voc"})


def _acronym(form: str) -> bool:
    """Whether a form is written the way Polish writes an acronym.

    ``PO``, ``AA`` and ``UP`` inflect for nothing either, and their letters spell
    function words, so the exclusion below would take exactly the reading that is
    right. In capitals the noun is what the form is. One capital says nothing,
    every sentence starting with one.
    """
    return len(form) > 1 and form.isupper()


def admissible(segment: Segment) -> Segment:
    """Drop the noun reading of a form olski reads as a function word.

    Morfeusz reads ``do`` as the preposition and as the musical note, and the
    note inflects for nothing: carrying all seven cases, it satisfies every
    demand unification can make, which is the only filter olski has. So every
    ``do`` in a text hands its sentence a second reading. That is ambiguity in
    the dictionary rather than in Polish, and no parse can tell the two apart,
    so the lexicon rules it out instead. docs/subset.md argues the criterion and
    docs/corpus.md measures what it is worth and what it costs.
    """
    if _acronym(segment.form):
        return segment
    if not any(reading.tag.pos in CLOSED_CLASS for reading in segment.readings):
        return segment
    kept = tuple(
        reading
        for reading in segment.readings
        if not (reading.tag.pos == "subst" and reading.tag.get("case") >= EVERY_CASE)
    )
    if len(kept) == len(segment.readings):
        return segment
    # A closed-class reading is not a noun reading, so the one that spared this
    # segment is itself among the survivors and the tuple is never emptied.
    return replace(segment, readings=kept)


#: Cecha, którą tagset daje formie zaimka po tym, czy stoi ona po przyimku.
#: Wartość ``praep`` bez ``npraep`` obok niej nazywa formę, którą polszczyzna
#: stawia wyłącznie tam: `niego`, `nich`, `nie`. Forma o obu wartościach naraz —
#: `nim`, a w miejscowniku także `niej` i `nich` — stoi i pod przyimkiem, i bez niego.
PRZYIMKOWOŚĆ = "post_prepositionality"
BEZ_PRZYIMKA = "npraep"


def _tylko_po_przyimku(reading: Reading) -> bool:
    """Czy tagset mówi o tym czytaniu, że stoi wyłącznie po przyimku."""
    wartości = reading.tag.get(PRZYIMKOWOŚĆ)
    return bool(wartości) and BEZ_PRZYIMKA not in wartości


def po_przyimku(segments: list[Segment]) -> list[Segment]:
    """Zdejmij formie przyimkowej zaimka czytanie tam, gdzie przyimka nie ma.

    Grupa imienna bierze zaimek w każdej swojej pozycji, więc bez tego warunku
    `Cena niego rośnie.` się wyprowadza, a `nie` stoi dopełnieniem w zdaniu,
    które przeczy. Są to czytania, których polszczyzna nie ma, czyli to samo, co
    odbiera :func:`admissible`; dlaczego warunek stoi tutaj, a nie na terminalu
    zaimka ani za rozbiorem, wywodzi
    docs/subset.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą.

    Pytany jest graf, a nie lista: licencji udziela każda krawędź z czytaniem
    przyimkowym, która kończy się w węźle, gdzie ta się zaczyna. Krawędź bez ani
    jednego czytania z tego wychodzi — `niego` innych nie ma — i jest wtedy formą
    bez licencji, którą werdykt wypisuje (:func:`bez_licencji`).

    Licencji udziela przyimek, który ta gramatyka bierze, a nie każda forma z
    czytaniem przyimkowym, i dlatego wykluczenie stoi tu to samo, co na terminalu
    (:data:`PRZYIMEK_ROZDZIELAJĄCY`). Bez niego `Cena jest niska, a nie.`
    wyprowadza się: rozdzielające `a` niesie u Morfeusza czytanie przyimka, więc
    licencjonuje `nie` stojące za nim, a wyrażenia przyimkowego z tego `a` nie ma
    jak zbudować, czyli licencji udziela pozycja, której nikt nie zajmuje.
    """
    licencjonujące = {
        segment.end
        for segment in segments
        if any(
            reading.tag.pos == "prep" and reading.lemma != PRZYIMEK_ROZDZIELAJĄCY
            for reading in segment.readings
        )
    }
    return [
        segment
        if segment.start in licencjonujące
        else replace(
            segment,
            readings=tuple(
                reading for reading in segment.readings if not _tylko_po_przyimku(reading)
            ),
        )
        for segment in segments
    ]


def po_słowie(segments: list[Segment]) -> list[Segment]:
    """Zdejmij cząstce zwrotnej odczytanie tam, gdzie nie stoi przed nią żadne słowo.

    Cząstka stoi przy swojej formie osobowej po obu jej stronach
    (:data:`SZYKI_CZĄSTKI`), a pozycja przednia sięga początku zdania i miejsca
    tuż za znakiem: bez tego warunku `Się myli.` oraz `Cena rośnie, się nie
    liczy.` się wyprowadzają, a takich napisów polszczyzna nie ma. Cząstka opiera
    się bowiem na słowie przed sobą, a znak słowem nie jest. Spójnik nim jest i
    licencji udziela, bo `i przyrasta, i się topi` bank drzew pisze.

    Pozycja tylna do tych miejsc nie sięga, bo przed nią stoi jej własna forma,
    więc warunek nie zdejmuje ani jednego odczytania, które olski brał przed
    wpuszczeniem pozycji przedniej.

    Pytany jest graf, a nie lista, i pytanie jest to samo, które stawia
    :func:`po_przyimku`: odczytanie zostaje tam, gdzie w węźle otwierającym tę
    krawędź kończy się krawędź z odczytaniem, które nie jest znakiem.

    Warunek stoi w warstwie morfologicznej, a nie na terminalu cząstki, z tego
    samego powodu, z którego stoi tam tamten: miejsce, którego cząstka nie ma
    zająć, jest miejscem w zdaniu, a terminal widzi samą formę.
    docs/subset.md#cząstka-zwrotna-stoi-po-obu-stronach-swojej-formy-osobowej
    trzyma, co warunek ten zostawia na zewnątrz.
    """
    licencjonujące = {
        segment.end
        for segment in segments
        if any(reading.tag.pos != "interp" for reading in segment.readings)
    }
    return [
        segment
        if segment.start in licencjonujące
        else replace(
            segment,
            readings=tuple(
                reading for reading in segment.readings if reading.lemma != LEMAT_ZWROTNY
            ),
        )
        for segment in segments
    ]


#: Notacja tego rejestru: ścieżka, nazwa pliku, nazwa modułu. Człony spaja
#: ukośnik albo kropka, po której nie ma spacji, człon ma dwa znaki wyrazowe albo
#: więcej, w całości stoi przynajmniej jedna litera, a łącznik spaja tylko wewnątrz
#: takiej ścieżki. docs/subset.md wywodzi, co każde z tych czterech żądań trzyma na
#: zewnątrz i dlaczego. Klasa w podglądzie jest sumą pozostałych, bo litery szuka
#: dokładnie tam, gdzie sięgnie dopasowanie: znak spajający dodany do wzorca
#: dodaje się i tam.
CZŁON = r"\w{2,}"
NOTACJA = re.compile(
    rf"(?<![\w./])(?=[\w./_-]*[^\W\d_]){CZŁON}(?:[-_]{CZŁON})*(?:[./]{CZŁON}(?:[-_]{CZŁON})*)+"
)

#: Czytanie, które dostaje notacja, wersalik i przytoczenie: rzeczownik
#: nieodmienny, dokładnie ten tag, który Morfeusz daje `menu` i `atelier`.
NIEODMIENNY = tag("subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:n:ncol")


def wersalik(segment: Segment) -> Segment:
    """Daj formie pisanej wersalikami czytanie nieodmienne, gdy słownik jej nie ma.

    ``README``, ``GLR`` i ``SGJP`` są w tym rejestrze codzienne i wracają jako
    ``ign``, którego nie bierze ani jedna produkcja. Notacja wyżej dostaje to samo
    czytanie i różni się znakiem, który ją spaja (:data:`NOTACJA`).

    Warunek pyta o milczenie słownika, a nie o samo pismo formy, i tym broni
    polszczyzny: ``NIE`` i ``PAN`` słownik czyta, więc zdanie z nimi nie traci
    czytania, które ma. Wywód i cenę trzyma docs/subset.md pod wersalikiem.
    """
    if not _acronym(segment.form):
        return segment
    if any(reading.tag.known for reading in segment.readings):
        return segment
    return replace(segment, readings=(Reading(segment.form, segment.form, NIEODMIENNY),))


#: Części mowy, którymi grupa imienna staje sama jednym słowem. Napisu z takim
#: czytaniem przytoczenie nie rusza, bo cudzysłów bierze go już jako grupę, a
#: zamiana odebrałaby mu i przypadek, i rodzaj. Za co dokładnie, mówi
#: docs/subset.md w sekcji o interpunkcji obejmującej.
GRUPA_JEDNYM_SŁOWEM = frozenset({"subst", "ger", "ppron12", "ppron3"})


def _przytoczony(segment: Segment, otwarte: set[int], zamknięte: set[int]) -> bool:
    """Czy cudzysłów obejmuje sam ten napis, a grupą imienną on nie jest."""
    if segment.start not in otwarte or segment.end not in zamknięte:
        return False
    return not any(reading.tag.pos in GRUPA_JEDNYM_SŁOWEM for reading in segment.readings)


def przytoczenie(segments: list[Segment]) -> list[Segment]:
    """Daj napisowi objętemu cudzysłowem czytanie nieodmienne, gdy grupą nie jest.

    Napis przytoczony — `„B”`, `„nie”` — nie odmienia się, więc produkcja
    przepuszczająca przypadek grupy nie ma na nim czego przepuszczać, a rzeczownik
    nieodmienny spełnia każde żądanie przypadku, bo żadnego nie nosi. Wywód, cenę
    i granicę warunku trzyma docs/subset.md w sekcji o interpunkcji obejmującej.

    Licencji udziela cudzysłów po obu stronach, więc pytany jest graf, a nie sama
    forma, tak samo jak przy formie przyimkowej (:func:`po_przyimku`). Warunek na
    oba znaki naraz żąda przy tym, żeby napis wypełniał wnętrze sam. Czytania są
    zamienione, a nie dołożone, bo napisu przytoczonego to zdanie nie używa jako
    słowa.
    """
    otwarte = {
        segment.end
        for segment in segments
        if any(reading.lemma == ZNAK_CUDZYSŁOWU_OTWIERAJĄCY for reading in segment.readings)
    }
    zamknięte = {
        segment.start
        for segment in segments
        if any(reading.lemma == ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY for reading in segment.readings)
    }
    return [
        replace(segment, readings=(Reading(segment.form, segment.form, NIEODMIENNY),))
        if _przytoczony(segment, otwarte, zamknięte)
        else segment
        for segment in segments
    ]


def morphology(text: str) -> list[Segment]:
    """Analizuje tekst tak, jak czyta go olski.

    Kilka rzeczy dzieje się tu przed gramatyką. Notacja rejestru dostaje jedną
    krawędź z jednym czytaniem, bo Morfeusz rozbija ``docs/linter.md`` na pięć
    krawędzi, a czytelnik ma tam jedno słowo. Słowo, którego słownik nie ma,
    dostaje czytania z leksykonu projektu (:mod:`olski.projekt`), bo ``commitów``
    jest dopełniaczem liczby mnogiej i nikt nie ma tam czytania nieodmiennego.
    Forma pisana wersalikami, której słownik nie czyta wcale, dostaje czytanie
    nieodmienne (:func:`wersalik`). Reszta idzie do Morfeusza i traci te czytania,
    które odrzuca :func:`admissible`, a po nich te, które :func:`po_przyimku`
    odrzuca formie stojącej bez przyimka oraz :func:`po_słowie` cząstce zwrotnej
    stojącej bez słowa przed sobą, a na końcu napis objęty cudzysłowem dostaje
    czytanie nieodmienne przytoczenia (:func:`przytoczenie`).

    Trzy ostatnie warunki pytają o sąsiada, a nie o samą formę, więc idą po liście
    gotowej, a nie po jednym segmencie jak te przed nimi. Przytoczenie idzie
    ostatnie, bo pyta o czytania, które zostały: ``be`` traci rzeczownik w
    :func:`admissible` i przytoczenie zastaje tam sam przymiotnik.

    Sklejenie stoi przed analizą, a nie za nią. Segment niesie numery węzłów
    grafu, a nie przesunięcia w tekście, więc po analizie nie ma już czym zobaczyć
    spacji, która ukośnik w ścieżce odróżnia od ukośnika między dwoma słowami.
    """
    return przytoczenie(
        po_słowie(
            po_przyimku(
                [admissible(wersalik(projekt.z_leksykonu(segment))) for segment in _segmenty(text)]
            )
        )
    )


def _segmenty(text: str) -> list[Segment]:
    """Krawędzie grafu segmentacji, notację liczące za jedną z nich.

    Grafy kolejnych kawałków stają jeden za drugim, przesunięte o numer węzła, na
    którym poprzedni się skończył. Wolno tak, bo każdy z nich ma jedno źródło i
    jedno ujście: Morfeusz numeruje od zera, a wszystkie ścieżki przez kawałek
    kończą się na tym samym węźle, choćby w środku rozchodziły się na dwie.
    """
    segmenty: list[Segment] = []
    węzeł = 0
    for kawałek, notacja in _kawałki(text):
        krawędzie = _krawędzie(kawałek) if notacja else analyse(kawałek)
        segmenty.extend(
            replace(segment, start=segment.start + węzeł, end=segment.end + węzeł)
            for segment in krawędzie
        )
        węzeł += max((segment.end for segment in krawędzie), default=0)
    return segmenty


def _kawałki(text: str):
    """Tnie tekst na kawałki, każdy z odpowiedzią, czy jest notacją."""
    znak = 0
    for match in NOTACJA.finditer(text):
        yield text[znak : match.start()], False
        yield match.group(), True
        znak = match.end()
    yield text[znak:], False


def _krawędzie(forma: str) -> list[Segment]:
    return [Segment(start=0, end=1, form=forma, readings=(Reading(forma, forma, NIEODMIENNY),))]


def licencjonowane(segment: Segment, grammar: Grammar) -> tuple[Reading, ...]:
    """Czytania formy, po które sięga choć jeden terminal tej gramatyki.

    Pytają o to dwie odpowiedzi o jednym kryterium: werdykt wypisuje formę, której
    nie zostaje ani jedno (:func:`bez_licencji`), a przebieg nad korpusem nazywa
    część mowy tego, które zostało (``Outcome.blocker`` w ``olski/coverage.py``).
    Kryterium wyprowadza z gramatyki :meth:`olski.grammar.Grammar.licencjonuje`,
    a ta funkcja jest samym jego zastosowaniem do czytań formy.
    """
    return tuple(
        reading
        for reading in segment.readings
        if grammar.licencjonuje(reading.tag.pos, reading.lemma, segment.lematy, reading.tag.cechy)
    )


def bez_licencji(segments: list[Segment], grammar: Grammar) -> tuple[str, ...]:
    """Formy nie do ominięcia, którym gramatyka nie bierze ani jednego czytania.

    Odrzucenie ma dwie przyczyny i są to dwie różne roboty do zrobienia: forma,
    po którą nie sięga żadna produkcja, i struktura, której gramatyka nie
    licencjonuje. Świgra trzyma je osobno (docs/swigra.md), a tę pierwszą widać
    przed rozbiorem i widać ją wyprowadzoną z gramatyki
    (:meth:`olski.grammar.Grammar.licencjonuje` wywodzi, czemu wolno).

    Liczy się przy tym krawędź, bez której nie ma drogi przez zdanie, a nie
    każda pusta dziedzina: podział, który Morfeusz dokłada obok formy całej, nie
    jest słowem, które ktokolwiek napisał. Wywód i to, co ten warunek daje za
    darmo, trzyma docs/design-notes.md.

    Forma stoi na liście raz, choćby w zdaniu powtórzyła się kilka razy, bo
    odpowiedzią jest to, czego gramatyka nie bierze, a nie ile razy autor to
    napisał.
    """
    formy: list[str] = []
    for segment in segments:
        if licencjonowane(segment, grammar):
            continue
        if _omijalna(segments, segment) or segment.form in formy:
            continue
        formy.append(segment.form)
    return tuple(formy)


def _omijalna(segments: list[Segment], krawędź: Segment) -> bool:
    """Czy przez graf segmentacji idzie droga, która tej krawędzi nie bierze.

    Krawędzie idą w górę po numerach węzłów, więc osiągalność liczy się jednym
    przejściem po posortowanych, bez cofania się.
    """
    ujście = max(segment.end for segment in segments)
    osiągalne = {min(segment.start for segment in segments)}
    for segment in sorted(segments, key=lambda segment: segment.start):
        if segment is not krawędź and segment.start in osiągalne:
            osiągalne.add(segment.end)
    return ujście in osiągalne


def na_czym_stanęło(segments: list[Segment], furthest: int) -> Segment | None:
    """Krawędź, na której odrzucenie stanęło; ``None``, gdy stanęło na końcu zdania.

    Ostatniego znaku zdania nie nazywa, bo zdanie, które bierze każdą swoją
    formę i nie domyka się, jest drugim zdarzeniem i dostaje drugie zdanie
    werdyktu (``Verdict.explain``) oraz drugi wiersz przebiegu nad korpusem
    (``NO_STRUCTURE`` w ``olski/coverage.py``).

    Krawędź, a nie forma, bo pytają o nią dwie odpowiedzi: werdykt bierze stąd
    formę, a ranking blokerów część mowy jej czytania, i kryterium jest jedno.

    Z jednego węzła grafu wychodzi czasem kilka form, bo ``ktoś`` wychodzi
    także jako ``kto`` i ``ś``. Nazwana jest najdłuższa, czyli ta, którą autor
    napisał, a krótsza jest jej częścią.

    Nazwane miejsce jest końcem przedrostka, który się analizuje, i nie jest
    wskazaniem usterki; wywód i cenę trzyma
    docs/subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka.
    """
    ujście = max((segment.end for segment in segments), default=furthest)
    stojące = [
        segment for segment in segments if segment.start == furthest and segment.end < ujście
    ]
    if not stojące:
        return None
    return max(stojące, key=lambda segment: segment.end)


def zatrzymania(segmenty: list[Segment], grammar: Grammar | None = None) -> tuple[str, ...]:
    """Każde zatrzymanie odrzuconego zdania, a nie samo pierwsze.

    Werdykt nazywa jedno miejsce (:func:`na_czym_stanęło`), a zdanie długie ma ich
    kilka i pierwsze zasłania resztę, więc kto pisze pod tę gramatykę, nie widzi z
    werdyktu, ile jeszcze poprawek to zdanie zabierze; po co ta odpowiedź jest,
    mówi docs/pisanie-po-olsku.md.

    Analiza rusza od nowa **za** formą zatrzymania, a nie na niej: formy, której
    nie wzięła żadna analiza częściowa, nie weźmie też analiza zaczęta od niej, a
    przebieg stałby na miejscu. Krawędź przekraczającą cięcie trzeba przy tym
    zdjąć, bo graf segmentacji rozchodzi się na kilka dróg — ``ktoś`` wychodzi
    także jako ``kto`` i ``ś`` — a takiej krawędzi nie ma z czym w kawałku złożyć.

    Cięcie nie wskazuje usterki ani granicy konstrukcji, tak samo jak jedno
    zatrzymanie jej nie wskazuje.
    """
    grammar = grammar or GRAMMAR
    formy: list[str] = []
    while segmenty:
        stanęło = na_czym_stanęło(segmenty, parse(grammar, segmenty).furthest)
        if stanęło is None:
            break
        formy.append(stanęło.form)
        segmenty = [
            replace(segment, start=segment.start - stanęło.end, end=segment.end - stanęło.end)
            for segment in segmenty
            if segment.start >= stanęło.end
        ]
    return tuple(formy)


def sentences(text: str) -> list[str]:
    """Tnie tekst na zdania i oddaje je tak, jak stoją.

    Podziału nie ma tutaj, tylko w :mod:`olski.document`: żąda on po kropce
    białego znaku i zna skróty. Sam olski skrótów nie ma, więc nad nim
    cięcie na każdej kropce byłoby dokładne. Wejściem jest jednak dokumentacja,
    gdzie ``docs/linter.md`` jest jednym słowem, a cięcie na kropce w jego środku
    wymyśla dwa zdania, których nikt nie napisał.

    Cięcie stoi więc przed analizą, a nie po niej. Morfeusz jest wołany z
    ``SKIP_WHITESPACES``, a segment niesie numery węzłów grafu zamiast przesunięć
    w tekście, więc po analizie nie ma już czym zobaczyć spacji, która odróżnia
    granicę zdania od nazwy pliku.
    """
    document = Document(text)
    return [document.slice(span) for span in document.sentences]


def werdykt(zdanie: str, segmenty: list[Segment], grammar: Grammar | None = None) -> Verdict:
    """Werdykt o zdaniu już zsegmentowanym, wraz z całym podsumowaniem.

    Segmenty przychodzą argumentem, a nie powstają tutaj, bo zależą od napisu, a
    nie od gramatyki: kto pyta o jedno zdanie kilka gramatyk — sonda różnicowa
    nad prozą — segmentuje je raz i pyta tyle razy, ile ma wariantów.

    Podsumowania werdykt bierze wszystkie, także te, których wołający nie czyta.
    Drugie wejście, pytające o mniej, byłoby drugą ścieżką do utrzymania, a
    oszczędza najwyżej jeden rozbiór na zdanie — tyle bierze zatrzymanie nad
    zdaniem odrzuconym (:func:`olski.parse.podsumuj`) — podczas gdy pominięcie
    rozbiorów, których odpowiedź jest znana, oszczędza ich tyle, ile wariantów
    minus jeden (``_bez_zbędnych`` w ``harness/ruch.py``).
    """
    grammar = grammar or GRAMMAR
    result = parse(grammar, segmenty, deklaracja=DEKLARACJA)
    stanęło = na_czym_stanęło(segmenty, result.furthest)
    return Verdict(
        text=zdanie,
        result=result,
        nielicencjonowane=bez_licencji(segmenty, grammar),
        zatrzymanie=stanęło.form if stanęło is not None else None,
    )


def dalsze_zatrzymania(verdict: Verdict, grammar: Grammar | None = None) -> tuple[str, ...]:
    """Zatrzymania tego zdania poza tym, które nazwał już werdykt.

    Zdanie z czytaniem nie stanęło nigdzie, więc krotka jest wtedy pusta, i tak
    samo pusta jest nad fragmentem. Segmentacja idzie tu drugi raz, bo werdykt
    segmentów nie niesie (:func:`werdykt`).
    """
    if verdict.status == FRAGMENT or not verdict.result.rejected:
        return ()
    return zatrzymania(morphology(verdict.text), grammar)[1:]


def check(text: str, grammar: Grammar | None = None) -> list[Verdict]:
    """Check every sentence of a text against the grammar."""
    return [werdykt(zdanie, morphology(zdanie), grammar) for zdanie in sentences(text)]


@dataclass(frozen=True)
class Podsumowanie:
    """Ile zdań tekstu jest olskich, dla tego, kto pyta o cały tekst.

    Liczby te wychodzą z werdyktów jedną regułą — fragment nie jest zdaniem, więc
    nie wchodzi do mianownika, a zdanie odrzucone nie ma czytania — i pyta o nie
    więcej niż jeden wołający, więc policzone u każdego z nich rozjeżdżają się po
    cichu: mianownik mniejszy o fragment czyta się jak pomiar, a nie jak pomyłka.
    """

    #: Zdania, którym gramatyka daje dokładnie jedno czytanie, czyli zdania olskie.
    olskie: int
    #: Zdania, czyli to, o czym werdykt orzeka: fragmentów nie ma tu ani w liczniku.
    zdań: int
    #: Zdania, którym gramatyka daje przynajmniej jedno czytanie.
    z_czytaniem: int
    #: Napisy, których nic nie interpunkuje jako zdania.
    fragmentów: int

    @classmethod
    def z_werdyktów(cls, werdykty: Sequence[Verdict]) -> Podsumowanie:
        zdania = [verdict for verdict in werdykty if verdict.status != FRAGMENT]
        return cls(
            olskie=sum(verdict.result.valid for verdict in zdania),
            zdań=len(zdania),
            z_czytaniem=sum(not verdict.result.rejected for verdict in zdania),
            fragmentów=len(werdykty) - len(zdania),
        )

    def explain(self) -> str:
        summary = (
            f"{self.olskie} of {self.zdań} sentences are olski, "
            f"and {self.z_czytaniem} have a reading"
        )
        if self.fragmentów:
            summary += f", beside {self.fragmentów} fragments that are not sentences"
        return summary
