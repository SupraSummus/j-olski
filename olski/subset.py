"""Olski itself: the subset of Polish this grammar admits.

Two properties define it, and both are exclusions rather than inventions:

**Every olski sentence is a well-formed Polish sentence.** No helper notation, no
convenient deviation. What olski leaves out, it leaves out entirely.

**Every olski sentence has exactly one reading.** This is the property doing the
real work. Polish is full of sentences that parse two ways, and a reader resolves
them from context or from knowing what the writer meant. Olski excludes them,
because a sentence with two readings has no checkable meaning and, more
importantly, no reliable one.

The grammar below admits every order the subject, the object and the verb can
stand in, since Polish uses all six of them, which is precisely why case
syncretism makes some sentences ambiguous. The alternative — declaring that olski
is SVO and reading the first noun phrase as the subject — would make those
sentences unambiguous to a reader who knows the convention and still ambiguous to
every other Polish speaker. Rejecting them keeps the promise that olski is
readable as ordinary Polish.

That property is about Polish, and a dictionary offers readings Polish does not,
so the subset excludes readings as well as constructions: see ``admissible``
below.
"""

from __future__ import annotations

import re
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
    describe,
    parse,
)
from olski.precedencja import Rozwinięcie
from olski.walencja import BEZ_BIERNIKA, BEZ_BIERNIKA_ZWROTNE

#: Rola, którą gramatyka zostawia nierozstrzygniętą rozmyślnie,
#: więc streszczenie czytania nazywa przy niej i to, co ona określa:
#: bez tego dwa czytania różne samym miejscem przyłączenia wychodzą jednym napisem.
PRZYŁĄCZANY = "Modifier"

#: Rola przysłówka, czyli tego, który określa zdanie. Przysłówek określający
#: przymiotnik roli nie dostaje: stoi on wewnątrz orzecznika albo przydawki, więc
#: widać go w wypełnieniu tamtej roli, a wypisany drugi raz obok mówiłby o zdaniu,
#: że ma okolicznik, którego ono nie ma.
PRZYSŁÓWKOWY = "Adverb"

#: Rola okolicznika wyrażonego zdaniem, czyli tego, który mówi, kiedy, dlaczego
#: albo pod jakim warunkiem zachodzi to, co mówi zdanie nad nim. Rolą jest z tego
#: samego powodu, z którego jest nią przysłówek: werdykt nazywa role etykietami
#: węzłów, a zdanie przyjęte z takim okolicznikiem wychodziłoby bez słowa o tym,
#: co olski w nim przyjął. Stoi ona zarazem wśród zdań podrzędnych, bo wnętrze
#: tego okolicznika jest osobnym zdaniem, i tyle właśnie znaczy nazwanie go
#: rolą: streszczenie nazywa go całym napisem i w środek nie zagląda.
OKOLICZNIKOWY = "AdverbialClause"

#: Rola grupy pytajnej, czyli tego, o co zdanie pyta: `które zadania` w `Ustawy
#: określają, które zadania mają charakter obowiązkowy.` Rolą jest z tego samego
#: powodu, z którego jest nią okolicznik wyrażony zdaniem: werdykt nazywa role
#: etykietami węzłów, a zdanie pytające przyjęte bez tej etykiety wychodziłoby
#: `valid` bez słowa o tym, o co pyta, czyli bez tego, co o nim trzeba wiedzieć
#: najpierw. Konstytuentem jest zaś grupa imienna, więc wnętrze streszczenie
#: nazywa całym napisem, tak samo jak wnętrze podmiotu.
PYTAJNY = "Interrogative"

#: Rola rzeczownika, który orzeka bez czasownika: `mowa` w `zadania, o których
#: mowa w ustawie`. Rolą jest z tego samego powodu, z którego jest nią grupa
#: pytajna: werdykt nazywa role etykietami węzłów, a zdanie z tym rzeczownikiem
#: nie ma ani podmiotu, ani czasownika, więc przyjęte bez tej etykiety wychodziłoby
#: `valid` bez ani jednej roli, czyli bez słowa o tym, co olski w nim przyjął.
#:
#: Rola stoi obok `Predicative`, a nie jest nią, bo orzecznik jest pozycją ramy,
#: a ten rzeczownik nie ma nad sobą czasownika, który by ramę ogłaszał; co
#: przyjmuje gramatyka zlewająca te dwie, mierzy
#: docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną.
ORZEKAJĄCY = "NominalPredicate"

#: Rola predykatywu, czyli słowa, które orzeka bez podmiotu i bez czasownika:
#: `trzeba` w `Trzeba czytać dokumenty.`, `widać` w `Widać granicę w odpowiedzi.`
#: Rolą jest z tego samego powodu, z którego jest nią rzeczownik orzekający, a
#: osobną od niego dlatego, że orzeka innym kształtem: tamten stoi w mianowniku i
#: żąda okolicznika, a ten rządzi tym, co rządziłby czasownik, i podmiotu nie ma.
#:
#: Rola stoi obok `Verb`, a nie jest nią, bo predykatyw czasownikiem nie jest:
#: osoby, liczby ani rodzaju nie niesie, więc `Verb: trzeba` mówiłoby o zdaniu, że
#: ma orzeczenie zgodne z podmiotem, którego ono nie ma. Co wpuszczenie tej klasy
#: kosztuje, mierzy
#: docs/subset.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika.
BEZOSOBOWY = "ImpersonalPredicate"

#: Rola cząstki, czyli tej, która stoi przy zdaniu: `już`, `dopiero`, `także`.
#: Rolą jest z tego samego powodu, z którego jest nią przysłówek, a osobną od niego
#: dlatego, że cząstka przysłówkiem nie jest: werdykt nazywa rolę etykietą węzła,
#: więc `Adverb: już` mówiłoby o zdaniu, że ma okolicznik przysłówkowy, którego ono
#: nie ma. Pozycję ma tę samą co przysłówek i dlatego pisze je jedna pętla.
CZĄSTKOWY = "Particle"

#: Rola wtrącenia w nawiasie, czyli tego, co ten rejestr dopowiada obok zdania:
#: `(docs/subset.md)`, `(niżej)`. Rolą jest z tego samego powodu, z którego jest
#: nią przysłówek: werdykt nazywa role etykietami węzłów, a zdanie przyjęte z
#: wtrąceniem wychodziłoby bez słowa o tym, że olski wziął w nim nawias.
#:
#: Rolą zdania jest przy tym samo wtrącenie, a nie to, co ono niesie: nawias
#: dopowiada, a nie wypełnia pozycji, więc grupa imienna w jego środku nie jest
#: ani podmiotem, ani dopełnieniem, i streszczenie nazywa ją całym napisem.
WTRĄCONY = "Parenthetical"

DEKLARACJA = Deklaracja(
    role=(
        "Subject",
        "Object",
        "Predicative",
        "Verb",
        ORZEKAJĄCY,
        BEZOSOBOWY,
        PRZYSŁÓWKOWY,
        CZĄSTKOWY,
        OKOLICZNIKOWY,
        PYTAJNY,
        WTRĄCONY,
        PRZYŁĄCZANY,
    ),
    przyłączany=PRZYŁĄCZANY,
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
    # Czoło pytania stoi tu drugie i jest rozpiętością jednego zdania tak samo,
    # bo pytanie o wyrażenie przyimkowe wynosi grupę pytajną ponad zdanie
    # składowe, w którym ona rolę zajmuje. Bez tego symbolu grupa ta leży cała
    # przed składowym i dostaje znak :data:`SĄSIEDNIE_ZDANIE_SKŁADOWE`, czyli
    # zdanie o jednym zdaniu składowym mówi, że streszczenie milczy o drugim,
    # a streszczenie właśnie to składowe wypisuje.
    składowe=("ClauseConjunct", "InterrogativeCore"),
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
    podrzędne=(
        "RelativeClause",
        "SubordinateClause",
        "InterrogativeClause",
        OKOLICZNIKOWY,
        WTRĄCONY,
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
#: mowa`, a `jest` nikt tam nie pisze. Zwrot ten niesie co siódme zdanie rejestru
#: ustaw i jest w nim najczęstszym zdaniem względnym; docs/ustawy.md go liczy.
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
SPÓJNIKI_PRZECINKOWE = "ale|a|lecz|natomiast|więc|zatem|toteż"

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

#: Rama czasownika spoza leksykonu: dopełnienie w bierniku, orzecznik zgodny,
#: bezokolicznik, zdanie podrzędne i pytanie zależne. Narzędnika w niej nie ma, i
#: to jest to jedno miejsce, w którym rama domyślna czegoś zabrania: orzecznik
#: narzędnikowy bierze kopula i nikt poza nią. Zdanie podrzędne stoi w niej mimo
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


def _walencja() -> tuple[dict[str, str], dict[str, str]]:
    """Leksykon jako klasy walencyjne, osobno dla formy z cząstką ``się`` i bez niej.

    Zwrotność jest drugim wymiarem klucza, a nie częścią lematu, i dlaczego,
    mówi ``olski/walencja.py``, czyli ten, który leksykon czyta dla obu
    kierunków. Tutaj zostaje to, co jest zdaniem samej gramatyki.

    Kluczem klasy jest rama, a nie lemat, bo tak wychodzi produkcja: powstaje raz
    na ramę, a nie raz na lemat. Kopula zabiera leksykonowi swoje lematy, zamiast
    stanąć obok nich, bo klasy mają się nie zachodzić: Walenty mówi o niej to samo
    co leksykon o każdym innym lemacie, a rama kopuli mówi ponadto o narzędniku.

    Zdanie leksykonu jest tu jedno, o bierniku, choć plik mówi trzy. Co zdejmuje
    dwa pozostałe, mówi :data:`RAMA_DOMYŚLNA`.
    """
    return (
        {
            RAMA_BEZ_BIERNIKA: "|".join(sorted(BEZ_BIERNIKA - set(KOPULA.split("|")))),
            "nom.inst": KOPULA,
        },
        {RAMA_BEZ_BIERNIKA: "|".join(sorted(BEZ_BIERNIKA_ZWROTNE))},
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

#: Zaimek rzeczowny, którego Morfeusz daje obok przymiotnikowego `ten`. Dopełniacza
#: nie bierze: `tego podzbioru` jest przymiotnikiem przy rzeczowniku i niczym
#: więcej, a produkcja z dopełniaczem po głowie czyta to drugi raz jako zaimek
#: rządzący rzeczownikiem. docs/subset.md wywodzi kryterium i mierzy jego cenę.
ZAIMEK_RZECZOWNY = "to"

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
CUDZYSŁÓW_OTWIERAJĄCY = word("interp", lemma="„")
CUDZYSŁÓW_ZAMYKAJĄCY = word("interp", lemma="”")

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
SPÓJNIK_PRZECINKOWY = word("conj|comp", lemma=SPÓJNIKI_PRZECINKOWE)
SPÓJNIK_BEZ_PRZECINKA = word("conj", bez_lematu=SPÓJNIKI_PRZECINKOWE)

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

#: Cząstka w okoliczniku: sama lista i nic więcej, tak samo jak przysłówek niżej
#: bierze samą część mowy.
CZĄSTKA = word("part", lemma=CZĄSTKI)

#: Rama predykatywu (:data:`PREDYKATYWY`): domyślna bez orzecznika zgodnego.
#: Wyliczona z domyślnej z tego samego powodu, z którego wylicza się z niej
#: :data:`RAMA_BEZ_BIERNIKA`, a mianownika nie ma w niej dlatego, że orzecznik
#: zgadza się z podmiotem, którego zdanie z predykatywem nie ma:
#: `Trzeba wolni.` nie jest niczym.
RAMA_BEZOSOBOWA = ".".join(p for p in RAMA_DOMYŚLNA.split(".") if p != "nom")

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
#: cząstka nad nim.
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
PRZECZENIE = word("part", lemma="nie")

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

    Forma z cząstką ``się`` pyta o swój leksykon, bo jest innym czasownikiem;
    lemat, którego tamten leksykon nie wymienia, bierze ramę domyślną tak samo
    jak każdy inny nieznany.
    """
    leksykon = WALENCJA_ZWROTNA if zwrotne else WALENCJA
    klasy = [({"lemma": lematy}, rama) for rama, lematy in leksykon.items()]
    return [*klasy, ({"bez_lematu": "|".join(leksykon.values())}, RAMA_DOMYŚLNA)]


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
        number=V("n"),
        gender=V("g"),
        czoło=czoło,
        **zaimek,
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
            **zaimek,
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


def build() -> Grammar:
    grammar = Grammar(start="Sentence")

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
    for symbol, słowo in (
        ("Adjective", word("adj", bez_lematu=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE)),
        ("PredicativeAdjective", word("adj|ppas", bez_lematu=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE)),
    ):
        grammar.rule(symbol, [Głowa(słowo)], **AGREE)
        grammar.rule(symbol, [PRZYSŁÓWEK_STOPNIA, Głowa(słowo)], **AGREE)
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
    człon = nt("ClauseConjunct", tryb=V("t"))
    grammar.rule("Clause", [człon], tryb=V("t"))
    grammar.rule("Clause", [Głowa(człon), SPÓJNIK_BEZ_PRZECINKA, nt("Clause")], tryb=V("t"))
    grammar.rule("Clause", [Głowa(człon), PRZECINEK, nt("Clause")], tryb=V("t"))
    # Przecinek i spójnik naraz, czyli ta interpunkcja, której polszczyzna żąda
    # przed `ale`, `a` i `więc` (:data:`SPÓJNIKI_PRZECINKOWE`). Poziom zdaniowy
    # ma tę pozycję, a imienny i przymiotnikowy nie, bo lista tych spójników jest
    # listą spójników zdaniowych: `nie polszczyzny, a dziedziny` jest w niej
    # elipsą, a nie ciągiem współrzędnym dwóch grup imiennych.
    grammar.rule(
        "Clause",
        [Głowa(człon), PRZECINEK, SPÓJNIK_PRZECINKOWY, nt("Clause")],
        tryb=V("t"),
    )

    # Części zdania, nazwane raz, bo każda z nich stoi w kilku szykach naraz.
    # Zmienna cechy jest zakresu produkcji, więc dwie produkcje biorące ten sam
    # obiekt mówią dalej każda o swojej zgodności.
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
    orzecznik_ramy = nt("Predicative", number=V("n"), gender=V("g"), valency=V("w"))
    orzecznik_wysunięty = nt("Predicative", number=V("n"), gender=V("g"))

    # Orzecznik zgodny, wraz z żądaniem, które stawia czasownikowi. Dwa razy
    # ``nom``, a nie wspólna zmienna, bo rama nie zastępuje pozycji: wspólna
    # zmienna wpuszcza tu kopulę z narzędnikiem i przyjmuje nad Składnicą
    # ``Na to jest zbyt wielkim tchórzem.``, gdzie podmiotem wychodzi ``zbyt``.
    # docs/subset.md trzyma ten pomiar wraz z drugim takim.
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
    zdanie.dominacja("ClauseConjunct", [podmiot, Głowa(orzeczenie)], tryb=V("t"))

    # Zdanie bez podmiotu: Zapisz plik podmiotu nie ma i nie potrzebuje, tak samo
    # jak Zapisuje ustawienia.
    zdanie.dominacja("ClauseConjunct", [nt("Predicate", tryb=V("t"))], tryb=V("t"))

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
    grammar.rule(
        "ClauseConjunct", [Głowa(nt(ORZEKAJĄCY)), okoliczniki], tryb=TRYB_OZNAJMUJĄCY
    )

    # Predykatyw wraz z tym, czym rządzi: `Trzeba czytać dokumenty.`, `Nie widać
    # granicy.` Rama i `Complements` są te same, co u czasownika, a zdaniem składowym
    # jest predykatyw wprost, bo `Predicate` ma ciało z podmiotem, którego to zdanie
    # nie ma; wywód trzyma
    # docs/subset.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika.
    #
    # Ciało bez wypełnienia — `Nie wiadomo.` — jest osobne, bo jego zakup jest osobną
    # liczbą; `Complements` pustego ciała nie ma, a dodane tam dawałoby je każdemu
    # czasownikowi naraz.
    for przeczenie, negacja in PRZECZENIA:
        grammar.rule(
            BEZOSOBOWY,
            [*przeczenie, Głowa(PREDYKATYW)],
            valency=RAMA_BEZOSOBOWA,
            negacja=negacja,
        )
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
        tryb=V("t"),
    )

    # Czasownik przed podmiotem: Nadchodzi druga rewolucja, Są oni obdarzeni
    # rozumem. Podmiot nie bierze tu własnych dopełnień, więc Zapisuje program
    # ustawienia się nie wyprowadza i żadne zdanie SVO nie konkuruje z czytaniem
    # samego siebie od czasownika. Szyku odwrotnego te dwie deklaracje nie mają z
    # tego samego powodu, dla którego nie ma go deklaracja wyżej: składa go
    # podmiot z orzeczeniem.
    zdanie.dominacja("ClauseConjunct", [Głowa(czasownik), podmiot], tryb=V("t"))
    zdanie.dominacja(
        "ClauseConjunct", [Głowa(czasownik_orzecznika), podmiot, orzecznik], tryb=V("t")
    )

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
    zdanie.dominacja(
        "ClauseConjunct", [orzecznik_wysunięty, Głowa(kopula), podmiot], tryb=V("t")
    )

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
    grammar.rule(
        "ClauseConjunct",
        [Głowa(nt("ClauseConjunct", tryb=V("t"))), nt(WTRĄCONY)],
        tryb=V("t"),
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
        [nt("Modifier"), Głowa(nt("ClauseConjunct", tryb=V("t")))],
        tryb=V("t"),
    )
    for przy_zdaniu in (PRZYSŁÓWKOWY, CZĄSTKOWY):
        grammar.rule(
            "ClauseConjunct",
            [nt(przy_zdaniu), Głowa(nt("ClauseConjunct", tryb=V("t")))],
            tryb=V("t"),
        )

    grammar.rule(
        "Subject",
        [nt("NP", case="nom", number=V("n"), gender=V("g"), person=V("p"))],
        number=V("n"),
        gender=V("g"),
        person=V("p"),
        czoło=BEZ_CZOŁA,
    )
    # Dopełnienie wychodzi z pozycją ramy, którą zajmuje, bo tym jest przypadek,
    # który czasownik rządzi: żądanie wobec czasownika stoi więc raz, tutaj, a nie
    # w każdym szyku, w którym dopełnienie stoi.
    #
    # Dopełniacz negacji zajmuje tę samą pozycję ramy, więc jest drugą produkcją
    # dopełnienia, a nie drugą pozycją. Wartość cechy jest tu wypisana, a nie
    # zmienna, bo o przypadku rozstrzyga właśnie ta produkcja.
    grammar.rule(
        "Object", [nt("NP", case="acc")], valency="acc", negacja="aff", czoło=BEZ_CZOŁA
    )
    grammar.rule(
        "Object", [nt("NP", case="gen")], valency="acc", negacja="neg", czoło=BEZ_CZOŁA
    )

    # A predicate is a verb with what it takes. What it takes is one symbol
    # rather than a list of bodies, so that the finite verb and the infinitive
    # below share it instead of each carrying its own copy.
    grammar.rule(
        "Predicate", [czasownik], number=V("n"), gender=V("g"), person=V("p"), tryb=V("t")
    )
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
        number=V("n"),
        person=V("p"),
        gender=V("g"),
        tryb=V("t"),
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
            number=V("n"),
            gender=V("g"),
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
    grammar.rule(
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
    for ciało, pozycja in (
        (
            [PRZECINEK, word("comp", lemma=SPÓJNIKI_OKOLICZNIKOWE), Głowa(nt("Clause"))],
            "za",
        ),
        (
            [word("comp", lemma=SPÓJNIKI_WYSUWANE), Głowa(nt("Clause")), PRZECINEK],
            "przed",
        ),
    ):
        grammar.rule(OKOLICZNIKOWY, ciało, pozycja=pozycja)

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
        grammar.rule(OKOLICZNIKOWY, [PRZECINEK, spójnik, Głowa(wnętrze)], pozycja="za")
        grammar.rule(OKOLICZNIKOWY, [spójnik, Głowa(wnętrze), PRZECINEK], pozycja="przed")

    # Dwie pozycje, bo polszczyzna stawia ten okolicznik przed swoim zdaniem i za
    # nim, a szyku wewnątrz zdania nadrzędnego nie zmienia ani jedna, ani druga.
    # Zdanie nadrzędne jest tu składowym, a nie ciągiem współrzędnym: okolicznik
    # dochodzi do jednego zdania, a nie do wszystkiego, co przecinek połączył,
    # i jest to ta sama granica, którą trzyma zasięg koordynacji
    # (docs/subset.md#nothing-above-a-coordination-distributes-into-it).
    grammar.rule(
        "ClauseConjunct",
        [Głowa(nt("ClauseConjunct", tryb=V("t"))), nt(OKOLICZNIKOWY, pozycja="za")],
        tryb=V("t"),
    )
    grammar.rule(
        "ClauseConjunct",
        [nt(OKOLICZNIKOWY, pozycja="przed"), Głowa(nt("ClauseConjunct", tryb=V("t")))],
        tryb=V("t"),
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
            grammar.rule(
                "Complements",
                ciało,
                number=V("n"),
                gender=V("g"),
                valency=V("w"),
                negacja=V("z"),
            )
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

    # What is predicated of the subject: an adjective phrase agreeing with it,
    # or a noun phrase in the instrumental. Both are what być takes, and the
    # first is also what rodzą się wolni i równi predicates without one.
    #
    # Pozycja ramy wychodzi z orzecznika, bo tym się te dwa różnią i to na nim stoi
    # ograniczenie wyżej: zgodny bierze każdy czasownik, narzędnikowy kopula.
    grammar.rule(
        "Predicative",
        [nt("AP", case="nom", number=V("n"), gender=V("g"))],
        valency="nom",
        number=V("n"),
        gender=V("g"),
    )
    grammar.rule("Predicative", [nt("NP", case="inst")], valency="inst")

    # Rozkaźnik idzie razem z oznajmującą, bo różni je to, co niosą tagi, a nie
    # to, co mówi ta produkcja.
    #
    # Czasownik zwrotny różni się od formy bez cząstki dwiema rzeczami i tyle też
    # mówi o nim ta pętla: stoi przy nim `się`, a rama bierze się z drugiego
    # leksykonu, bo otwierać bierze dopełnienie w bierniku, a otwierać się nie.
    # Cząstka stoi w polszczyźnie i gdzie indziej, a olski bierze tylko tę pozycję.
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
    for zwrotne, cząstka in ((False, ()), (True, (word("part", lemma="się"),))):
        for warunek, rama in _klasy(zwrotne):
            for ciało, osoba, tryb in _formy_skończone(warunek):
                for przeczenie, negacja in PRZECZENIA:
                    grammar.rule(
                        "Verb",
                        [*przeczenie, *ciało, *cząstka],
                        number=V("n"),
                        gender=V("g"),
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

    grammar.rule(
        "NP",
        [nt("NPConjunct", person=V("p"), **AGREE)],
        person=V("p"),
        **AGREE,
    )
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
        person=V("p"),
        **AGREE,
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
        person=V("p"),
        **AGREE,
    )
    # A coordination of noun phrases is plural and third person whatever its
    # conjuncts are, and it carries no gender: Polish resolves the gender of
    # rozum i sumienie by rules unification cannot state, and a feature a phrase
    # does not carry is one no agreement can fail against.
    grammar.rule(
        "NP",
        [Głowa(nt("NPConjunct", case=V("c"))), SPÓJNIK_BEZ_PRZECINKA, nt("NP", case=V("c"))],
        case=V("c"),
        number="pl",
        person="ter",
    )
    grammar.rule(
        "NP",
        [Głowa(nt("NPConjunct", case=V("c"))), PRZECINEK, nt("NP", case=V("c"))],
        case=V("c"),
        number="pl",
        person="ter",
    )

    # Noun phrases: a noun, an agreeing adjective before it, a genitive
    # modifier after it. Agreement is the unification, not a separate check,
    # and every one of these shares the same three variables, so they are named
    # once. A conjunct headed by a noun is third person by saying so; leaving
    # that off one of them would quietly let a first person verb take it.
    grammar.rule(
        "NPConjunct",
        [przymiotnik, Głowa(nt("NPConjunct", **AGREE))],
        person="ter",
        **AGREE,
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
    # warunku każda forma paradygmatu ten, którą Morfeusz zna też jako rzeczownik,
    # daje grupie imiennej drugie czytanie tego samego kształtu. Warunek stoi w
    # deklaracji pary, a nie w każdym ciele, bo ciał z dopełniaczem pod głową jest
    # kilka, a paradygmat odczasownikowy `to` nie ma i wykluczać tam nie ma czego;
    # wywód i cenę trzyma docs/subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem.
    for głowa, głowa_dopełniacza in (
        (word("subst", **AGREE), word("subst", bez_lematu=ZAIMEK_RZECZOWNY, **AGREE)),
        (word("ger", **AGREE), word("ger", **AGREE)),
    ):
        grammar.rule("NPConjunct", [głowa], person="ter", **AGREE)
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), nt("NP", case="gen")],
            person="ter",
            **AGREE,
        )
        # Polish puts an attributive adjective after the noun in terminology:
        # plik konfiguracyjny, język polski. Both orders are the language, so both
        # are here, and where a sentence admits both readings it is ambiguous.
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa), przymiotnik],
            person="ter",
            **AGREE,
        )
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa), nt("Modifier")],
            person="ter",
            **AGREE,
        )
        # Oba szyki przydawki naraz: dobrem wspólnym wszystkich obywateli, zadania
        # ochrony ludności. Bez tej pozycji dopełniacz dochodzi tylko do przymiotnika
        # stojącego przed rzeczownikiem, więc termin nazwany drugim szykiem nie ma
        # wyprowadzenia, a rejestr ustaw nazywa tak swoje terminy zdanie po zdaniu:
        # docs/ustawy.md trzyma, ile ta pozycja tam daje i ile odbiera.
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), przymiotnik, nt("NP", case="gen")],
            person="ter",
            **AGREE,
        )
        # Wyrażenie przyimkowe po rzeczowniku, który już coś przy sobie ma: akcja
        # zbrojna w Strefie Gazy, rozmieszczenie ogrodów działkowych w Polsce,
        # zadania ochrony ludności w gminie. Bez tych trzech pozycji przyłączenie do
        # rzeczownika w takiej grupie nie istnieje, a zdanie wychodzi jednym
        # czytaniem przez czasownik. Trzecia idzie razem z przydawką wyżej: bez niej
        # wyrażenie po takim terminie dochodzi do dopełniacza i do nikogo więcej,
        # czyli gramatyka wybiera przyłączenie, którego wybierać nie ma.
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa), przymiotnik, nt("Modifier")],
            person="ter",
            **AGREE,
        )
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), nt("NP", case="gen"), nt("Modifier")],
            person="ter",
            **AGREE,
        )
        grammar.rule(
            "NPConjunct",
            [Głowa(głowa_dopełniacza), przymiotnik, nt("NP", case="gen"), nt("Modifier")],
            person="ter",
            **AGREE,
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
    grammar.rule(
        "NPConjunct",
        [word("num", accommodability="congr", **AGREE), Głowa(nt("NPConjunct", **AGREE))],
        person="ter",
        **AGREE,
    )
    grammar.rule(
        "NPConjunct",
        [
            Głowa(word("num", accommodability="rec", case=V("c"), gender=V("g"))),
            nt("NP", case="gen", number="pl", gender=V("g")),
        ],
        case=V("c"),
        number="sg",
        gender="n",
        person="ter",
    )

    # A pronoun is the one conjunct that carries its own person, which is the
    # whole reason it is here: without one, first and second person subjects
    # have no noun phrase to be.
    grammar.rule(
        "NPConjunct",
        [word("ppron3|ppron12", person=V("p"), **AGREE)],
        person=V("p"),
        **AGREE,
    )

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
    grammar.rule(
        "NPConjunct",
        [ZAIMEK_DZIERŻAWCZY, Głowa(nt("NPConjunct", **AGREE))],
        person="ter",
        **AGREE,
    )

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
    grammar.rule(
        "NPConjunct",
        [CZĄSTKA, Głowa(nt("NPConjunct", person=V("p"), **AGREE))],
        person=V("p"),
        **AGREE,
    )

    # Adjective phrases, coordinated the same way and agreeing throughout, so
    # that wolni i równi is one predicative and wolna i równi is none.
    grammar.rule("AP", [nt("APConjunct", **AGREE)], **AGREE)
    grammar.rule(
        "AP",
        [Głowa(nt("APConjunct", **AGREE)), SPÓJNIK_BEZ_PRZECINKA, nt("AP", **AGREE)],
        **AGREE,
    )
    grammar.rule(
        "AP", [Głowa(nt("APConjunct", **AGREE)), PRZECINEK, nt("AP", **AGREE)], **AGREE
    )
    # A passive participle is an adjective for these purposes, and it keeps the
    # complement its verb governed: obdarzeni rozumem i sumieniem.
    grammar.rule("APConjunct", [orzecznikowy], **AGREE)
    grammar.rule(
        "APConjunct", [Głowa(orzecznikowy), nt("NP", case="inst")], **AGREE
    )
    # Trzecie miejsce, do którego wyrażenie przyimkowe dochodzi: powiązani z
    # interesami postkomunistów, przeznaczany na budowę.
    grammar.rule("APConjunct", [Głowa(orzecznikowy), nt("Modifier")], **AGREE)

    # A preposition governs a case, and the noun phrase has to be in it.
    # One lemma is excluded and it is excluded by name
    # (:data:`PRZYIMEK_ROZDZIELAJĄCY`).
    grammar.rule("Modifier", [Głowa(PRZYIMEK), nt("NP", case=V("c"))])

    # Przysłówek zdania jako konstytuent, a nie jako słowo w liście okoliczników,
    # bo werdykt nazywa role etykietami węzłów: bez tego symbolu zdanie przyjęte z
    # okolicznikiem przysłówkowym wychodziłoby `valid` bez słowa o tym, co olski w
    # nim przyjął (:data:`PRZYSŁÓWKOWY`).
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

    # Zdanie względne, czyli przecinek i `RelativeCore`, którym jest samo zdanie
    # bez przecinków odgraniczających. Przecinek zamykający stawia polszczyzna
    # wtedy, gdy zdanie nadrzędne biegnie dalej, więc oba ciała są tu razem, a
    # zdanie dostaje to z nich, które pasuje do jego interpunkcji.
    #
    # Wtrącenie w nawiasie dostaje pozycję w ciele zamykanym przecinkiem i tylko
    # w nim, bo tam stoi ono przed tym przecinkiem, a przyłączone do zdania
    # nadrzędnego stanęłoby za nim, czyli dałoby inny napis. Ciało bez przecinka
    # kończy się tam, gdzie zdanie nadrzędne, więc ta sama pozycja dałaby tam
    # dwa czytania jednego napisu, i dlatego jest to ciało osobne, a nie druga
    # córka w obu; docs/subset.md wywodzi to razem z ceną.
    rdzeń = Głowa(nt("RelativeCore", number=V("n"), gender=V("g")))
    for ciało in (
        [PRZECINEK, rdzeń],
        [PRZECINEK, rdzeń, PRZECINEK],
        [PRZECINEK, rdzeń, nt(WTRĄCONY), PRZECINEK],
    ):
        grammar.rule("RelativeClause", ciało, number=V("n"), gender=V("g"))

    # Zaimek względny jest grupą imienną o jednym słowie i osobnym symbolem, bo
    # grupa imienna stoi w zdaniu wszędzie, a on w jednym miejscu: na czele
    # zdania względnego. Wpuszczony do grupy imiennej stanąłby w każdej jej
    # pozycji, a `Program zapisuje który.` polszczyzną nie jest.
    # Obie pary cech czoła są tu jedną parą, bo głową jest sam zaimek
    # (:func:`zaimek_czoła`).
    grammar.rule(
        "RelativePronoun",
        [word("adj", lemma=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE)],
        **AGREE,
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
    głowa_grupy = word("subst", **AGREE)
    zaimek_dopełniacza = nt("RelativePronoun", case="gen", **POPRZEDNIK)
    for ciało in (
        [Głowa(głowa_grupy), zaimek_dopełniacza],
        [zaimek_dopełniacza, Głowa(głowa_grupy)],
    ):
        grammar.rule("RelativeNP", ciało, **AGREE, **zaimek_czoła(V("nz"), V("gz")))

    # Grupa pytajna: zaimek pytajny i grupa imienna, przy której on stoi. Głową
    # jest grupa imienna, bo pytanie jest o rzecz, którą ona nazywa, a zaimek mówi
    # tylko, że pyta się o to, która z nich. Zaimek zgadza się z tą głową, więc
    # obie pary czoła są i tu jedną parą; niesie ją grupa po to, żeby czoło obu
    # rodzin pisała jedna funkcja, a nie po to, żeby ktoś ją w pytaniu czytał.
    grammar.rule(
        PYTAJNY,
        [ZAIMEK_PYTAJNY, Głowa(nt("NP", **AGREE))],
        **AGREE,
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
            grammar.rule(
                symbol,
                [nt(modyfikator, **POPRZEDNIK), Głowa(wnętrze)],
                **POPRZEDNIK,
            )

    # Zdanie pytające: czoło pytania i pytajnik. Ciało jest osobne od zdania
    # oznajmującego, a nie wzięte przez :data:`KONIEC_ZDANIA`, bo pytanie zamyka
    # jeden znak z trzech, które tamten terminal bierze.
    grammar.rule("Sentence", [Głowa(nt("InterrogativeCore")), PYTAJNIK])

    # Pytanie zależne: przecinek i to samo czoło. Pozycję ramy niesie ono tak samo
    # jak zdanie z `że`, a pozycja jest osobna i dlaczego, mówi
    # :data:`RAMA_DOMYŚLNA`. Spójnika w ciele nie ma, bo podporządkowuje tu sam
    # zaimek, i tym się to zdanie podrzędne od dwóch pozostałych różni.
    grammar.rule(
        "InterrogativeClause",
        [PRZECINEK, Głowa(nt("InterrogativeCore"))],
        valency="int",
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
        return [describe(reading, DEKLARACJA) for reading in self.result.readings]

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
                return f"no reading: no production takes {formy}"
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
    """
    licencjonujące = {
        segment.end
        for segment in segments
        if any(reading.tag.pos == "prep" for reading in segment.readings)
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

#: Czytanie, które notacja dostaje: rzeczownik nieodmienny, dokładnie ten tag,
#: który Morfeusz daje `menu` i `atelier`.
NIEODMIENNY = tag("subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:n:ncol")


def morphology(text: str) -> list[Segment]:
    """Analizuje tekst tak, jak czyta go olski.

    Cztery rzeczy dzieją się tu przed gramatyką. Notacja rejestru dostaje jedną
    krawędź z jednym czytaniem, bo Morfeusz rozbija ``docs/linter.md`` na pięć
    krawędzi, a czytelnik ma tam jedno słowo. Słowo, którego słownik nie ma,
    dostaje czytania z leksykonu projektu (:mod:`olski.projekt`), bo ``commitów``
    jest dopełniaczem liczby mnogiej i nikt nie ma tam czytania nieodmiennego.
    Reszta idzie do Morfeusza i traci te czytania, które odrzuca
    :func:`admissible`, a po nich te, które :func:`po_przyimku` odrzuca formie
    stojącej bez przyimka.

    Ostatni z czterech warunków pyta o sąsiada, a nie o samą formę, więc idzie
    po liście gotowej, a nie po jednym segmencie jak trzy przed nim.

    Sklejenie stoi przed analizą, a nie za nią. Segment niesie numery węzłów
    grafu, a nie przesunięcia w tekście, więc po analizie nie ma już czym zobaczyć
    spacji, która ukośnik w ścieżce odróżnia od ukośnika między dwoma słowami.
    """
    return po_przyimku([admissible(_z_leksykonu(segment)) for segment in _segmenty(text)])


def _z_leksykonu(segment: Segment) -> Segment:
    """Krawędź wraz z czytaniami, jakie leksykon projektu daje jej formie.

    Czytania leksykonu dochodzą do tych, które ma słownik, a nie zastępują ich,
    bo leksykon orzeka o formie, a nie łata milczenie Morfeusza: forma, którą
    słownik zna, a leksykon o niej mówi, ma czytania jednego i drugiego, i tyle
    właśnie czytań ma wtedy w polszczyźnie.

    Czytanie ``ign`` stąd schodzi, bo mówi ono, że słowa nie zna nikt, a
    leksykon właśnie je nazwał. Krawędź bez czytań z tego nie wyjdzie: znika ono
    tylko tam, gdzie leksykon coś dołożył.
    """
    czytania = projekt.czytania(segment.form)
    if not czytania:
        return segment
    znane = tuple(reading for reading in segment.readings if reading.tag.known)
    return replace(segment, readings=znane + czytania)


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


def bez_licencji(segments: list[Segment], grammar: Grammar) -> tuple[str, ...]:
    """Formy nie do ominięcia, którym gramatyka nie bierze ani jednego czytania.

    Odrzucenie ma dwie przyczyny i są to dwie różne roboty do zrobienia: forma,
    po którą nie sięga żadna produkcja, i struktura, której gramatyka nie
    licencjonuje. Świgra trzyma je osobno (docs/swigra.md), a tę pierwszą widać
    przed rozbiorem i widać ją wyprowadzoną z gramatyki: skoro unifikacja tylko
    zawęża, czytanie odrzucone przez każdy terminal wobec ``EMPTY`` nie
    przejdzie w żadnym zdaniu.

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
        if any(
            grammar.licencjonuje(reading.tag.pos, reading.lemma, reading.tag.cechy)
            for reading in segment.readings
        ):
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


def gdzie_stanęło(segments: list[Segment], furthest: int) -> str | None:
    """Forma, na której odrzucenie stanęło; ``None``, gdy stanęło na końcu zdania.

    Ostatniego znaku zdania nie nazywa, bo zdanie, które bierze każdą swoją
    formę i nie domyka się, jest drugim zdarzeniem i dostaje drugie zdanie
    werdyktu (``Verdict.explain``).

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
    return max(stojące, key=lambda segment: segment.end).form


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


def check(text: str, grammar: Grammar | None = None) -> list[Verdict]:
    """Check every sentence of a text against the grammar."""
    grammar = grammar or GRAMMAR
    verdicts = []
    for sentence in sentences(text):
        segments = morphology(sentence)
        result = parse(grammar, segments, deklaracja=DEKLARACJA)
        verdicts.append(
            Verdict(
                text=sentence,
                result=result,
                nielicencjonowane=bez_licencji(segments, grammar),
                zatrzymanie=gdzie_stanęło(segments, result.furthest),
            )
        )
    return verdicts
