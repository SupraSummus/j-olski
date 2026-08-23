"""Czytanie parsera jako drzewo tego zapisu, czyli obieg zamknięty z drugiej strony.

Oba tory stoją na dwóch różnych poziomach i tę różnicę ten moduł przechodzi.
Parser wydaje wyprowadzenie, czyli drzewo nad symbolami gramatyki
wraz z formami i ich cechami, a autor pisze kategorie dziedziny,
w których przypadka nie ma, bo bierze się on z pozycji
(``olski/skład/składnia.py``).
Odwrotnością linearyzacji ten plik zatem nie jest:
jest drugą funkcją, której przeciwdziedziną jest to, co autor napisał,
a wspólnym mają obie typ, a nie kod.
Po co ten obieg stoi, czego z niego nie wraca i co to mówi o obu torach,
trzyma ``docs/sklad.md``, a sam niezmiennik ``docs/design-notes.md``.

Zasady niżej rozstrzygają o kodzie i każda dotyczy każdej funkcji w nim.

**Wydaje krotkę drzew, a nie drzewo.**
Napis do drzewa jest relacją, bo ten zapis ma na jeden napis kilka drzew,
a napis nie mówi ani o relacji okolicznika,
ani o znaczniku tematu postawionym tam, gdzie konstytuent i tak stoi.
Wybór między nimi żądałby rankingu, którego ten projekt nie ma.
Wraz z krotką wychodzi stąd powód, dla którego reszta nie wróciła,
bo krotka pusta nie mówi, która z przyczyn zadziałała (:class:`Odczyt`).

**Rozstrzyga linearyzacja, a nie ten plik.**
Kandydat wychodzi stąd tylko wtedy, gdy wypisany daje te formy,
z których go przeczytano, więc drzewo stąd zwrócone
mówi napisem to, co przeczytano, i nie ma jak skłamać.
Zdejmuje to z tego pliku drugą kopię tego,
co kompilator wie o szyku i o formach,
i jest to ten sam chwyt, którym mierzy się ``olski/skład/przegląd.py``.

**Kształt bierze z drzewa, a wartości z formy.**
Czytanie parsera jest swoim kształtem, a lematy i wartości cech
są z niego wyłączone rozmyślnie (``signature`` w ``olski/parse.py``),
więc lemat wzięty z liścia jest lematem tego wyprowadzenia, które w czytaniu zostało,
a nie tego, o którym mówi zdanie.
Pytana jest zatem krawędź grafu segmentacji, czyli wszystkie czytania formy,
a wybór między nimi zostawia to porównanie.

Z ``olski/skład/__init__.py`` ten moduł nie wychodzi i jest to rozstrzygnięcie.
Czyta on gramatykę, a ta buduje się przy imporcie,
więc wpisany tam kazałby ją zbudować każdemu, kto sięga po sam kompilator,
i parser przestałby być świadkiem, a stałby się zależnością.
Rozstrzygnięcie obejmuje tak samo ``olski/__init__.py``,
bo import podpakietu przechodzi przez pakiet nadrzędny.
Trzyma to ``tests/test_rozbiór.py``.
"""

from __future__ import annotations

import itertools
from collections.abc import Iterator
from dataclasses import dataclass, fields, is_dataclass

from olski.parse import Leaf, Node, parse
from olski.skład.morfologia import BrakFormy, WieleLeksemów
from olski.skład.opowieść import Postać
from olski.skład.przyimki import PRZYIMKI
from olski.skład.składnia import (
    TERAZ,
    Byt,
    Ciąg,
    Czyj,
    Jaki,
    Jest,
    Kontekst,
    Koordynacja,
    Nominalne,
    Okolicznik,
    PozaRamą,
    Przysłówek,
    Robi,
    Rola,
    Rzecz,
    Treść,
    Wyróżnienie,
    Zdanie,
    kompiluj,
)
from olski.skład.spójniki import SPÓJNIKI
from olski.subset import GRAMMAR, OKOLICZNIKOWY, PRZYSŁÓWKOWY, morphology

#: Kopula, którą ``Jest`` wypisuje, czyli jedyny lemat, z którego to zdanie wraca.
#: Gramatyka bierze pięć, a skład umie ten jeden; trzyma to ``TODO.md``.
KOPULA = "być"

#: Znaki, którymi ten zapis pisze listę: spójnik przed ostatnim członem,
#: przecinek przed każdym wcześniejszym. Spójnik inny stoi w innej relacji,
#: więc ``albo`` przeczytane jako ``Ciąg`` mówiłoby co innego, niż napisano.
ZNAKI_LISTY = ("i", ",")

#: Formy, którymi skład wypisuje czasownik: czas teraźniejszy, przeszły i bezokolicznik.
#: Rozkaźnika ani odsłownego na liście nie ma, bo z żadnego z nich ten zapis
#: nie wypisuje niczego, więc czytanie oparte na nich nie miałoby czym wrócić.
CZASOWNIKOWE = ("fin", "praet", "inf")

#: Lemat cząstki, którą polszczyzna przeczy. Forma ``nie`` bywa też spójnikiem
#: i zaimkiem, więc pyta się o nią wraz z częścią mowy, tak jak o znak listy.
PRZECZENIE = "nie"

#: Symbol przymiotnika, którego gramatyka trzyma konstytuentem, bo przysłówek
#: stopniowany go określa, więc kształt ciała nazywa tu symbol tam, gdzie przedtem
#: stało słowo.
PRZYMIOTNIKOWA = "Adjective"

#: Etykiety, pod którymi gramatyka trzyma to, co w zdaniu stoi na swojej pozycji.
#: Ta sama siódemka stoi w ``DEKLARACJA`` w ``olski/subset.py``, gdzie jest listą ról
#: drukowanych w werdykcie, a tutaj tablicą rozdzielczą; pozycja dopisana tam
#: i tu pominięta zgłasza się brakiem kategorii, a nie drzewem bez niej.
#: Nazwy roli przysłówkowej i okolicznikowej bierzemy stamtąd, a nie spisujemy
#: drugi raz: dwie pisownie jednego napisu są tym, po czym grep przestaje odpowiadać.
#: Oba tory dostały te dwie pozycje osobno i w tej samej kolejności: ``Przysłówek``
#: i okoliczność wyrażona zdarzeniem stały w ``olski/skład/składnia.py``, zanim
#: gramatyka wpuściła przysłówek i zdanie okolicznikowe, więc obieg zamknął się na
#: nich dopiero razem z tamtymi produkcjami.
POZYCJE = (
    "Subject",
    "Object",
    "Predicative",
    "Verb",
    "Modifier",
    PRZYSŁÓWKOWY,
    OKOLICZNIKOWY,
)

#: Pozycje wypełnione zdaniem, każda pod swoim symbolem gramatyki.
#: Osobno od ``POZYCJE``, bo tamtą piątkę werdykt drukuje jako role,
#: a te dwie należą do ramy i żadnej roli nie nazywają.
#: Dzieli je podmiot: bezokolicznik dostaje go z góry, a treść ma własny.
BEZOKOLICZNIK = "InfinitivePhrase"
PODRZĘDNE = "SubordinateClause"
ZDANIOWE = (BEZOKOLICZNIK, PODRZĘDNE)

#: Pozycje, których znacznik tematu nie obejmuje, bo szyk ich nie przestawia.
#: Czasownik nie rusza się w tym zapisie nigdy, a zdania nie da się wyróżnić:
#: ``Wyróżnialne`` w ``olski/skład/składnia.py`` obejmuje role, okoliczności
#: i przysłówek, a ani ``Zdanie``, ani ``Treść`` z niego nie dziedziczy.
NIERUCHOME = ("Verb", *ZDANIOWE)

#: Symbole, które pozycji nie są, bo grupują te, które są.
GRUPUJĄCE = ("Predicate", "Complements", "Adjuncts", "ClauseConjunct")

#: Etykieta liścia, bo liść stoi w ciele produkcji formą, a nie symbolem.
#: Nazwana, żeby kształt ciała czytał się tam, gdzie się go dopasowuje.
SŁOWO = "słowo"


class PozaZapisem(Exception):
    """Czytanie, dla którego ten zapis kategorii nie ma.

    Wyjątkiem, a nie wartością, bo pada w środku budowania drzewa,
    a to, co go łapie, jest jedno: :func:`abstrahuj` odpowiada wtedy niczym.
    Odpowiedź pusta jest odpowiedzią, a nie porażką:
    polszczyzna ma zdania, których ten zapis nie mówi,
    i po to ten kierunek stoi obok parsera, żeby było widać które.
    """


def _relacje() -> dict[str, tuple[str, ...]]:
    """Leksykon przyimków czytany od strony napisu, bo tak go czyta rozbiór.

    ``olski/skład/przyimki.py`` odpowiada na pytanie kompilatora, czyli o przypadek
    przy zadanej relacji, a tutaj pytanie jest odwrotne i ma po kilka odpowiedzi:
    ``w`` stoi w relacji celu, czasu i miejsca.
    Liczone jest to z tamtego słownika, a nie wypisane obok,
    bo wpis dopisany tam i tu pominięty odbierałby czytanie bez zgłoszenia.

    Przypadek do klucza nie wchodzi, choć rozdzielałby część relacji,
    i wypada z niego przez zasadę o wartościach branych z formy:
    ``w piwnicę`` odsiewa relację miejsca na porównaniu form,
    a ``w repozytorium`` nie odsiewa żadnej, bo ten rzeczownik ma je równe.
    """
    odwrotny: dict[str, tuple[str, ...]] = {}
    for przyimek, relacja in PRZYIMKI:
        odwrotny[przyimek] = (*odwrotny.get(przyimek, ()), relacja)
    return odwrotny


RELACJE = _relacje()


def _relacje_spójników() -> dict[str, tuple[str, ...]]:
    """Leksykon spójników podrzędnych czytany od strony napisu, tak jak :func:`_relacje`.

    Pytanie jest to samo co przy przyimku i ma tak samo po kilka odpowiedzi:
    ``gdy`` mówi o czasie i o niczym więcej, a ``bo`` o przyczynie,
    więc relacji na jedno słowo bywa tu mniej niż tam, a droga jest ta sama.
    Liczone z ``olski/skład/spójniki.py``, a nie wypisane obok, z tego samego powodu:
    wpis dopisany tam i tu pominięty odbierałby czytanie bez zgłoszenia.
    """
    odwrotny: dict[str, tuple[str, ...]] = {}
    for spójnik, relacja in SPÓJNIKI:
        odwrotny[spójnik] = (*odwrotny.get(spójnik, ()), relacja)
    return odwrotny


RELACJE_SPÓJNIKÓW = _relacje_spójników()


def _nazwa(drzewo: Leaf | Node) -> str:
    """Czym ten węzeł jest, na tyle, na ile ma to stanąć w zgłoszeniu."""
    return drzewo.segment.form if isinstance(drzewo, Leaf) else drzewo.label


def _etykieta(drzewo: Leaf | Node) -> str:
    """Etykieta węzła albo ``SŁOWO``, gdy stoi tam forma."""
    return SŁOWO if isinstance(drzewo, Leaf) else drzewo.label


def _lematy(liść: Leaf, *części: str) -> tuple[str, ...]:
    """Lematy, którymi ta forma bywa w tych częściach mowy, po jednym na lemat.

    Pytana jest krawędź, a nie to czytanie liścia, które w drzewie stoi,
    i to jest zasada, na której stoi cały ten plik: wartości bierze się z formy.
    """
    lematy: list[str] = []
    for czytanie in liść.segment.readings:
        if czytanie.tag.pos in części and czytanie.lemma not in lematy:
            lematy.append(czytanie.lemma)
    return tuple(lematy)


def _rzeczowniki(liść: Leaf) -> tuple[tuple[str, str], ...]:
    """Lemat wraz z liczbą, po jednej możliwości na czytanie tej formy.

    Liczba idzie razem z lematem, bo razem stoją w czytaniu słownika:
    ``ustawienia`` jest dopełniaczem liczby pojedynczej i mianownikiem mnogiej,
    a to są dwie różne rzeczy do powiedzenia i dwa różne drzewa.
    Forma, która liczby nie rozdziela, wydaje obie, i wtedy napis o niej milczy.
    """
    pary: list[tuple[str, str]] = []
    for czytanie in liść.segment.readings:
        if czytanie.tag.pos != "subst":
            continue
        for liczba in sorted(czytanie.tag.get("number")):
            if (czytanie.lemma, liczba) not in pary:
                pary.append((czytanie.lemma, liczba))
    return tuple(pary)


def _cechy(drzewo: Node) -> tuple[str, ...]:
    """Cechy, którymi ten przymiotnik bywa, po jednej na lemat.

    Przysłówek stojący pod tym samym symbolem kategorii tu nie dostaje:
    ``Jaki`` trzyma cechę napisem, a `bardzo duży` jest stopniem tej cechy,
    czyli tym, o czym drzewo nie ma jak powiedzieć, i to jest ta cisza,
    którą ten kierunek zgłasza zamiast wypuścić drzewo mówiące mniej
    (``docs/sklad.md``).
    """
    kształt = tuple(_etykieta(dziecko) for dziecko in drzewo.children)
    if kształt != (SŁOWO,):
        raise PozaZapisem(f"przymiotnik z {', '.join(kształt)} nie ma tu kategorii")
    return _lematy(drzewo.children[0], "adj")


def _przysłówki(drzewo: Node) -> tuple[Przysłówek, ...]:
    """Okoliczności wyrażone jednym słowem, po jednej na lemat tej formy.

    Stopnia ``Przysłówek`` nie niesie, więc czytanie w stopniu wyższym
    wypada na porównaniu form, tak samo jak czytanie w czasie,
    którego skład nie wypisze (``olski/skład/składnia.py``).

    Ciało dopasowuje się całe, tak samo jak w :func:`_nominalne`:
    przysłówek określający drugi przysłówek stanie tu kiedyś ciałem o dwóch
    częściach, a ten zapis ma wtedy zgłosić brak kategorii, a nie przeczytać
    pierwszą część za całość; ``TODO.md`` trzyma tamten ruch.
    """
    kształt = tuple(_etykieta(dziecko) for dziecko in drzewo.children)
    if kształt != (SŁOWO,):
        raise PozaZapisem(f"przysłówek z {', '.join(kształt)} nie ma tu kategorii")
    return tuple(Przysłówek(lemat) for lemat in _lematy(drzewo.children[0], "adv"))


def _nominalne(drzewo: Node) -> tuple[tuple[Nominalne, str], ...]:
    """Grupy imienne wraz z liczbą, którymi ten konstytuent bywa.

    Kształt ciała produkcji rozstrzyga o kategorii i tyle tu jest treści.
    Wyrażenie przyimkowe pod rzeczownikiem kategorii nie dostaje,
    bo okolicznik dochodzi w tym zapisie do zdarzenia, a nie do rzeczy,
    i to jest ta połowa przyłączenia, której ten kierunek nie mówi
    (``docs/sklad.md``).
    """
    ciała = drzewo.children
    kształt = tuple(_etykieta(dziecko) for dziecko in ciała)
    if kształt == (SŁOWO,):
        return tuple((Rzecz(lemat), liczba) for lemat, liczba in _rzeczowniki(ciała[0]))
    if kształt == (PRZYMIOTNIKOWA, "NPConjunct"):
        return tuple(
            (Jaki(cecha, rzecz), liczba)
            for cecha in _cechy(ciała[0])
            for rzecz, liczba in _nominalne(ciała[1])
        )
    if kształt == (SŁOWO, PRZYMIOTNIKOWA):
        # Przymiotnik po rzeczowniku jest tą samą kategorią, a wraca z niej
        # szyk przed rzeczownikiem, więc odsiewa to porównanie form.
        return tuple(
            (Jaki(cecha, Rzecz(lemat)), liczba)
            for lemat, liczba in _rzeczowniki(ciała[0])
            for cecha in _cechy(ciała[1])
        )
    if kształt == (SŁOWO, "NP"):
        return tuple(
            (Czyj(Rzecz(lemat), określenie), liczba)
            for lemat, liczba in _rzeczowniki(ciała[0])
            for określenie in _role(ciała[1])
        )
    raise PozaZapisem(f"grupa imienna z {', '.join(kształt)} nie ma tu kategorii")


def _role(drzewo: Leaf | Node) -> tuple[Rola, ...]:
    """Role, którymi ta grupa imienna bywa: jeden byt albo kilka bytów w jednej pozycji.

    Koordynacja wychodzi płaska, choć gramatyka wiąże ją w prawo,
    bo ``Koordynacja`` trzyma człony listą i tak je wypisuje.

    Ciało dopasowuje się całe, tak samo jak w :func:`_nominalne`,
    bo gramatyka dopisuje ciała symbolom, które ten plik czyta,
    a ciało nierozpoznane ma się zgłosić brakiem kategorii
    (``docs/sklad.md``).
    """
    etykieta = _etykieta(drzewo)
    if etykieta == "NPConjunct":
        return tuple(Byt(rzecz, liczba) for rzecz, liczba in _nominalne(drzewo))
    if etykieta != "NP":
        raise PozaZapisem(f"{_nazwa(drzewo)} nie jest tu grupą imienną")
    kształt = tuple(_etykieta(dziecko) for dziecko in drzewo.children)
    if kształt == ("NPConjunct",):
        return _role(drzewo.children[0])
    if kształt == ("NPConjunct", SŁOWO, "NP"):
        człon, znak, reszta = drzewo.children
        _znak_listy(znak)
        return tuple(
            Koordynacja((pierwszy, *_człony(ogon)))
            for pierwszy in _role(człon)
            for ogon in _role(reszta)
        )
    raise PozaZapisem(f"grupa imienna z {', '.join(kształt)} nie ma tu kategorii")


def _człony(rola: Rola) -> tuple[Rola, ...]:
    """Człony koordynacji albo sama rola, bo lista trzyma je płasko."""
    return rola.człony if isinstance(rola, Koordynacja) else (rola,)


def _znak_listy(znak: Leaf | Node) -> None:
    """Zgłasza spójnik, który w tym zapisie znaczy co innego niż lista.

    ``Ciąg`` i ``Koordynacja`` wypisują się przez ``i``,
    więc czytanie ``albo`` jako którejkolwiek z nich
    wydałoby drzewo mówiące co innego, niż napisano,
    a porównanie form tego nie odsieje: wypisany ``i`` różni się od ``albo``
    dopiero na tym słowie, którego to porównanie nie minie.
    """
    if isinstance(znak, Node) or not set(_lematy(znak, "conj", "interp")) & set(ZNAKI_LISTY):
        raise PozaZapisem(f"{_nazwa(znak)} nie jest znakiem listy tego zapisu")


def _okoliczniki(drzewo: Node) -> tuple[Okolicznik, ...]:
    """Okoliczności, którymi to wyrażenie przyimkowe bywa, po jednej na relację.

    Relacji jest w leksykonie więcej niż przypadków, które one rozdzielają,
    więc jeden napis wychodzi z kilku różnych rzeczy do powiedzenia,
    i to jest pierwsza z dwóch cisz, o których mówi nagłówek tego modułu.
    """
    przyimek, grupa = drzewo.children
    if isinstance(przyimek, Node):
        raise PozaZapisem(f"{_nazwa(przyimek)} nie jest przyimkiem")
    return tuple(
        Okolicznik(słowo, relacja, co)
        for słowo in _lematy(przyimek, "prep")
        for relacja in RELACJE.get(słowo, ())
        for co in _role(grupa)
    )


def _okoliczniki_zdaniowe(drzewo: Node) -> tuple[Okolicznik, ...]:
    """Okoliczności, którymi to zdanie okolicznikowe bywa, po jednej na relację.

    Droga jest ta sama co przy wyrażeniu przyimkowym w :func:`_okoliczniki`
    i różnią je dwie rzeczy, obie wzięte z tego, że pod spójnikiem stoi zdanie.
    Przecinek należy do tego konstytuentu i stoi po tej stronie, po której stoi
    zdanie nadrzędne, więc spójnika szuka się po kształcie ciała, a nie na pierwszym
    miejscu. Pod spójnikiem stoi zaś zdanie, więc wraca ono tą samą drogą co treść
    zdania dopełnieniowego, czyli z własnym podmiotem i na nic nie czekając.

    Szyku ta funkcja nie sprawdza, choć leksykon o nim mówi
    (``staje_na_czele`` w ``olski/skład/spójniki.py``):
    okoliczność wysunięta wbrew leksykonowi nie wypisze się z powrotem tak,
    jak ją przeczytano, więc odsiewa ją porównanie form, a nie warunek tutaj.
    """
    kształt = tuple(_etykieta(dziecko) for dziecko in drzewo.children)
    if kształt == (SŁOWO, SŁOWO, "Clause"):
        spójnik = drzewo.children[1]
    elif kształt == (SŁOWO, "Clause", SŁOWO):
        spójnik = drzewo.children[0]
    else:
        raise PozaZapisem(f"zdanie okolicznikowe z {', '.join(kształt)} nie ma tu kategorii")
    zdanie = next(dziecko for dziecko in drzewo.children if _etykieta(dziecko) == "Clause")
    return tuple(
        Okolicznik(słowo, relacja, co)
        for słowo in _lematy(spójnik, "comp")
        for relacja in RELACJE_SPÓJNIKÓW.get(słowo, ())
        for co in _ciąg(zdanie)
    )


def _pozycje(drzewo: Node) -> Iterator[tuple[str, Leaf | Node]]:
    """Pozycje tego zdania w kolejności, w której stoją w tekście.

    Symbole grupujące schodzą tu do niczego, bo ten zapis ich nie ma:
    ``Predicate`` i ``Complements`` mówią, co czasownik bierze,
    a ``Robi`` trzyma to polami. Kolejność zostaje kolejnością tekstu,
    bo dzieci węzła stoją w niej, i to ona rozstrzyga potem o znacznikach.
    """
    for dziecko in drzewo.children:
        etykieta = _etykieta(dziecko)
        if etykieta in GRUPUJĄCE:
            yield from _pozycje(dziecko)
        elif etykieta in POZYCJE or etykieta in ZDANIOWE:
            yield etykieta, dziecko
        else:
            raise PozaZapisem(f"{_nazwa(dziecko)} nie ma tu swojej pozycji")


def _pozycje_bezokolicznika(drzewo: Node) -> Iterator[tuple[str, Leaf | Node]]:
    """Pozycje zdania, którym jest fraza bezokolicznikowa.

    Podmiotu ta fraza nie ma i tym jednym różni się od zdania osobowego:
    wykonawcę wskazuje czasownik nad nią, więc podmiot przychodzi z góry
    tak samo jak po opuszczeniu, o którym rozstrzyga ``pomijalny``.

    Pozycją czasownika jest tu cała fraza, a nie jej głowa,
    bo w ciele frazy cząstka przecząca poprzedza formę tak samo jak w ciele ``Verb``,
    i ten sam :func:`_czasowniki` czyta oba.
    Resztę fraza trzyma pod symbolem grupującym,
    więc te pozycje wychodzą tą samą drogą co w zdaniu osobowym,
    a węzeł innego kształtu zgłasza się tam, zamiast wypadać po cichu.
    """
    yield "Verb", drzewo
    for dziecko in drzewo.children:
        if isinstance(dziecko, Node):
            yield from _pozycje(dziecko)


def _treści(drzewo: Node) -> tuple[Treść, ...]:
    """Treści, którymi to zdanie podrzędne bywa, po jednej na zdanie pod spójnikiem.

    Podmiot ma ono własny, więc wraca z samego napisu i na nic nie czeka,
    i tym różni się ta pozycja od frazy bezokolicznikowej wyżej.

    Czytany jest sam kształt ciała, a nie słowa, które je wypełniają:
    ``Treść`` trzyma ``że`` stałą, bo autor nie wybiera tu słowa,
    przecinek należy do tego konstytuenta po obu stronach,
    a innego spójnika gramatyka w tej pozycji nie wypuszcza.
    Ciało dopasowuje się przy tym całe, tak samo jak w :func:`_nominalne`,
    bo ciało nierozpoznane ma się zgłosić brakiem kategorii (``docs/sklad.md``).
    """
    kształt = tuple(_etykieta(dziecko) for dziecko in drzewo.children)
    if kształt != (SŁOWO, SŁOWO, "Clause"):
        raise PozaZapisem(f"zdanie podrzędne z {', '.join(kształt)} nie ma tu kategorii")
    return tuple(Treść(zdanie) for zdanie in _ciąg(drzewo.children[-1]))


def _czasowniki(drzewo: Node) -> tuple[tuple[str, bool], ...]:
    """Lematy, którymi ta pozycja orzeka, każdy wraz z tym, czy zdanie przeczy.

    Czytane jest całe ciało, a nie sama głowa, bo przeczenie wychodzi tu słowem,
    a jest kategorią, którą ten zapis ma: ``nie`` w ``olski/skład/składnia.py``
    zmienia zdaniu jedno pole. Cząstka należy przy tym do zdania,
    a własnej pozycji nie ma i zajmuje pozycję czasownika,
    więc lemat, o który tu chodzi, bywa drugą częścią ciała, a nie pierwszą.

    Przeczenie wychodzi wyżej parą z lematem, bo po drugiej stronie jest z nim
    jednym polem zdania i rozjechać się z nim nie może.
    """
    ciała = drzewo.children
    przeczenie = PRZECZENIE in _lematy(ciała[0], "part")
    if przeczenie:
        ciała = ciała[1:]
    return tuple((lemat, przeczenie) for lemat in _lematy(ciała[0], *CZASOWNIKOWE))


def _konstytuenty(pozycja: str, drzewo: Leaf | Node) -> tuple:
    """Czym ta pozycja bywa w tym zapisie, po jednej możliwości na element.

    Czasownik wychodzi stąd lematem, a nie konstytuentem,
    bo ``Robi`` trzyma go polem, którego nie da się wyróżnić ani przestawić.
    Formy ten lemat nie niesie i nie ma nieść: czas jest własnością opowiadania,
    a osoba wychodzi z podmiotu, więc czytanie w czasie albo osobie,
    których skład nie wypisze, wypada na porównaniu form.
    Tą samą drogą wypada cząstka ``się``, bo skład jej nie wypisuje wcale.

    Zdanie wypełniające pozycję ramy wychodzi stąd na dwa sposoby
    i dzieli je podmiot. Treść ma własny, więc wychodzi gotowa.
    Bezokolicznik orzeka o podmiocie czasownika nad nim,
    a ta funkcja tego podmiotu nie zna, bo wypełnia on inną pozycję
    tego samego zdania, więc wychodzi stąd sam węzeł, a :func:`_dopełnienia`
    składa go, gdy podmiot jest już wybrany.

    Pozycja bez ani jednego wariantu zgłasza się tutaj, a nie u tego, kto pyta,
    bo tam wygasza iloczyn kandydatów i wraca pustką, o której nie ma co powiedzieć.
    Pusto bywa z dwóch rzeczy naraz i zgłoszenie ich nie rozdziela:
    rozkaźnik nie ma lematu wśród ``CZASOWNIKOWE``,
    a przyimek spoza ``RELACJE`` nie ma relacji.
    """
    if pozycja == "Verb":
        warianty = _czasowniki(drzewo)
    elif pozycja == "Modifier":
        warianty = _okoliczniki(drzewo)
    elif pozycja == PRZYSŁÓWKOWY:
        warianty = _przysłówki(drzewo)
    elif pozycja == OKOLICZNIKOWY:
        warianty = _okoliczniki_zdaniowe(drzewo)
    elif pozycja == BEZOKOLICZNIK:
        warianty = (drzewo,)
    elif pozycja == PODRZĘDNE:
        warianty = _treści(drzewo)
    else:
        warianty = _role(drzewo.children[0])
    if not warianty:
        raise PozaZapisem(f"„{' '.join(drzewo.forms())}” nie ma tu czym być w pozycji {pozycja}")
    return warianty


def _znaczniki(pozycje: list[str]) -> Iterator[dict[int, str]]:
    """Znaczniki tematu i rematu, których ten szyk może chcieć.

    Wyróżnić da się to, co stoi pierwsze, i to, co stoi ostatnie,
    bo tyle robi ``_szyk``: bierze jeden konstytuent na czoło, jeden na koniec,
    a resztę wypisuje w porządku, którego nikt nie wybierał.
    Wydawana jest każda z nich, a nie ta jedna, którą szyk zdradza,
    bo znacznik postawiony tam, gdzie konstytuent i tak stoi, niczego nie przestawia,
    a mimo to jest tym, co autor napisał.
    Pozycje ``NIERUCHOME`` z tej listy wypadają, bo znacznika nie biorą.
    """
    czoło = {0: "czoło"} if pozycje[0] not in NIERUCHOME else {}
    koniec = {len(pozycje) - 1: "koniec"} if pozycje[-1] not in NIERUCHOME else {}
    warianty: list[dict[int, str]] = [{}]
    for znaczniki in (czoło, koniec, {**czoło, **koniec}):
        if znaczniki and znaczniki not in warianty:
            warianty.append(znaczniki)
    yield from warianty


def _oznacz(konstytuent, miejsce: str | None):
    """Konstytuent wraz z tym, czym jest w zdaniu, albo goły, gdy szyk o tym milczy."""
    return konstytuent if miejsce is None else Wyróżnienie(konstytuent, miejsce)


def _złóż(
    pozycje: list[str],
    konstytuenty: tuple,
    znaczniki: dict[int, str],
    podmiot: Rola | None,
    postać: bool,
) -> Iterator[Zdanie]:
    """Zdania z pozycji, które gramatyka nazwała, i konstytuentów, które w nich stoją.

    Kopula rozdziela tu dwie kategorie, bo w tym zapisie są dwie:
    ``Jest`` orzeka o podmiocie orzecznikiem, a ``Robi`` czynnością.
    Orzecznik przy czasowniku innym niż kopula nie ma tu czym być,
    bo ``Jest`` trzyma kopulę wpisaną na stałe,
    a okoliczność przy orzeczeniu imiennym nie ma pozycji.

    Przeczenie dostają obie, bo obie mają je polem,
    a różnicę między nimi robi dopełniacz negacji, którego orzecznik nie bierze,
    i liczy ją linearyzacja, a nie ten plik.

    Zdań wychodzi stąd kilka tylko wtedy, gdy dopełnieniem jest bezokolicznik,
    bo zdanie pod nim powstaje dopiero tutaj (:func:`_dopełnienia`).
    Wykonawcą jest podmiot goły, bo tego samego obiektu żąda ``Robi``,
    a wyróżnienie orzeka o zdaniu nadrzędnym i niżej nie sięga.
    """
    pola: dict[str, object] = {}
    okoliczniki: list = []
    sprawca = podmiot
    czasownik, przeczenie = konstytuenty[pozycje.index("Verb")]
    for numer, (pozycja, konstytuent) in enumerate(zip(pozycje, konstytuenty, strict=True)):
        if pozycja == "Verb":
            continue
        if pozycja == "Subject":
            if postać:
                konstytuent = Postać(konstytuent)
            sprawca = konstytuent
        oznaczony = _oznacz(konstytuent, znaczniki.get(numer))
        #  Okoliczność i przysłówek stoją w ``Robi`` jedną listą, bo obie mówią,
        #  jak albo gdzie coś się dzieje, więc obie idą tutaj, a nie polem.
        #  Okoliczność wyrażona zdarzeniem jest tą samą kategorią co wyrażona rzeczą
        #  (``Okolicznik`` w ``olski/skład/składnia.py``), więc idzie tą samą listą.
        if pozycja in ("Modifier", PRZYSŁÓWKOWY, OKOLICZNIKOWY):
            okoliczniki.append(oznaczony)
        else:
            pola[pozycja] = oznaczony
    kto = pola.get("Subject", podmiot)
    if kto is None:
        raise PozaZapisem("zdanie bez podmiotu nie ma tu kategorii")
    if czasownik == KOPULA and "Predicative" in pola and not okoliczniki:
        yield Jest(co=kto, czym=pola["Predicative"], przeczenie=przeczenie)
        return
    if czasownik == KOPULA or "Predicative" in pola:
        raise PozaZapisem(f"{czasownik} nie składa tu orzeczenia imiennego")
    for dopełnienie in _dopełnienia(pola, sprawca):
        yield Robi(
            kto=kto,
            czyn=czasownik,
            co=dopełnienie,
            okoliczniki=tuple(okoliczniki),
            przeczenie=przeczenie,
        )


def _dopełnienia(pola: dict[str, object], sprawca: Rola | None) -> Iterator:
    """Czym bywa dopełnienie tego zdania: zdarzeniem, treścią, rzeczą albo niczym.

    Trzy pierwsze wykluczają się, bo pod ``Complements`` staje jedno wypełnienie,
    więc pytania idą tu jedno po drugim, a nie w iloczynie.
    Kilka odpowiedzi daje samo zdarzenie, bo jedyne z trzech powstaje tutaj:
    czeka na wykonawcę, którym jest podmiot zdania nad nim.
    """
    if BEZOKOLICZNIK in pola:
        pozycje = list(_pozycje_bezokolicznika(pola[BEZOKOLICZNIK]))
        yield from _zdania(pozycje, podmiot=sprawca)
        return
    yield pola.get(PODRZĘDNE, pola.get("Object"))


def _zdania(
    pozycje: list[tuple[str, Leaf | Node]],
    podmiot: Rola | None = None,
    postać: bool = False,
) -> Iterator[Zdanie]:
    """Zdania, którymi te pozycje bywają, bo bywają nimi po kilka naraz.

    Pozycje przychodzą policzone, a nie węzłem do policzenia,
    bo zdanie osobowe i fraza bezokolicznikowa różnią się dokładnie nimi:
    czasownik stoi w jednej pod swoim symbolem, a w drugiej liściem.
    Reszta tej funkcji o tej różnicy nie wie i wiedzieć nie ma.

    Podmiot przychodzi z zewnątrz wtedy, gdy zdanie go nie ma,
    czyli po opuszczeniu, o którym rozstrzyga ``pomijalny``,
    albo pod bezokolicznikiem, który podmiotu nie ma nigdy;
    tylko w pierwszym z tych dwóch przychodzi deklaracja tożsamości,
    bo bez niej ten sam napis by z tego drzewa nie wyszedł.
    """
    nazwy = [nazwa for nazwa, _ in pozycje]
    if nazwy.count("Verb") != 1:
        raise PozaZapisem("zdanie tego zapisu orzeka jednym czasownikiem")
    warianty = [_konstytuenty(nazwa, węzeł) for nazwa, węzeł in pozycje]
    for wybór in itertools.product(*warianty):
        for znaczniki in _znaczniki(nazwy):
            yield from _złóż(nazwy, wybór, znaczniki, podmiot, postać)


def _członowie(drzewo: Node) -> list[Node]:
    """Zdania składowe koordynacji, spłaszczone, bo ``Ciąg`` trzyma je listą.

    Ciało dopasowuje się całe z tego samego powodu co w :func:`_role`,
    choć zdanie złożone innych ciał niż te dwa nie ma:
    grupa imienna też ich nie miała, kiedy ten plik powstawał.
    """
    kształt = tuple(_etykieta(dziecko) for dziecko in drzewo.children)
    if kształt == ("ClauseConjunct",):
        return [drzewo.children[0]]
    if kształt == ("ClauseConjunct", SŁOWO, "Clause"):
        człon, znak, reszta = drzewo.children
        _znak_listy(znak)
        return [człon, *_członowie(reszta)]
    raise PozaZapisem(f"zdanie złożone z {', '.join(kształt)} nie ma tu kategorii")


def _ciąg(drzewo: Node) -> Iterator[Zdanie]:
    """Zdanie albo następstwo zdarzeń, którym to zdanie złożone bywa.

    Podmiot opuszczony w drugim zdarzeniu wraca tu z pierwszego
    i wraca wraz z tożsamością, bo tylko ona go opuszcza.
    Jest to jedyne miejsce, w którym tożsamość odzyskuje się z napisu:
    wewnątrz jednego zdania widać ją po tym, czego w nim nie ma,
    a między zdaniami nie widać jej wcale.
    """
    człony = [list(_pozycje(człon)) for człon in _członowie(drzewo)]
    if len(człony) == 1:
        yield from _zdania(człony[0])
        return
    dzieli = any("Subject" not in [nazwa for nazwa, _ in człon] for człon in człony[1:])
    for pierwsze in _zdania(człony[0], postać=dzieli):
        dalsze = [list(_zdania(człon, podmiot=pierwsze.podmiot)) for człon in człony[1:]]
        for reszta in itertools.product(*dalsze):
            yield Ciąg((pierwsze, *reszta))


def _słowa(napis: str) -> tuple[str, ...]:
    """Napis jako słowa, którymi da się go porównać z formami czytania.

    Znaki interpunkcyjne stoją tu osobno, bo parser dostaje je krawędziami,
    i stoją, a nie odpadają, bo przecinek jest w tym zapisie rozstrzygnięciem:
    lista pisana przez ``i`` przy każdym członie znaczy to samo, co pisana
    przecinkami, a wychodzi z niej inny napis i to on ma wrócić.
    Wielkość litery odpada, bo należy do zdania, a nie do drzewa.
    """
    return tuple(napis.replace(",", " ,").replace(".", " .").casefold().split())


def _rozjazd(drzewo: Zdanie, czytanie: Node, kontekst: Kontekst) -> str | None:
    """Czym to drzewo rozmija się z czytaniem, albo nic, gdy wypisuje jego formy.

    To jest cała obrona tego modułu i dlatego stoi na kompilatorze,
    a nie na drugiej kopii tego, co kompilator wie o szyku i o formach.
    Porażki linearyzacji są tu odpowiedzią, a nie błędem:
    drzewo, którego nie da się wypisać, nie jest drzewem tego czytania,
    a ``WieleLeksemów`` mówi ponadto, czego czytanie nie niesie,
    bo leksem deklaruje autor.

    Napis wypisany wchodzi do powodu, bo różnicę widzi tylko to porównanie,
    a czytelnik zgłoszenia ma przed sobą zdanie swoje, a nie to z drzewa.
    """
    try:
        napis = kompiluj(drzewo, kontekst)
    except (PozaRamą, BrakFormy) as błąd:
        return str(błąd)
    except WieleLeksemów as błąd:
        return f"kilka leksemów odpowiada na {błąd}"
    if _słowa(napis) == tuple(forma.casefold() for forma in czytanie.forms()):
        return None
    return f"wychodzi z tego „{napis}”"


@dataclass(frozen=True)
class Odczyt:
    """Drzewa, którymi czytanie wraca, wraz z powodami tych, którymi nie wróciło.

    Powodów jest kilka rodzajów i rozdziela je ``docs/sklad.md``,
    a krotka drzew sama nie mówi, który zadziałał na tym zdaniu.
    Powód opisuje kandydata, który odpadł, a nie odpowiedź,
    więc zdanie z drzewami ma jedno i drugie naraz.

    Rodzaje te dzielą się przy tym na dwa i tę granicę niesie ``kandydaci``,
    bo powód jest zdaniem dla czytelnika, a nie kluczem tabeli:
    zero mówi, że kategorii nie ma i drzewa nie było z czego zbudować,
    a liczba dodatnia przy pustych drzewach, że kandydat powstał
    i wypisuje się innym napisem, niż ten, który go wywołał.
    Pyta o to pomiar nad rejestrem (``sonda/znaczenia.py``),
    któremu pierwsze mówi, czego temu zapisowi brakuje,
    a drugie, gdzie oba kierunki mówią co innego o jednym zdaniu.
    """

    drzewa: tuple[Zdanie, ...]
    powody: tuple[str, ...]
    #: Ilu kandydatów zbudowano, zanim linearyzacja o nich rozstrzygnęła.
    kandydaci: int = 0


def _bez_powtórzeń(powody: list[str]) -> tuple[str, ...]:
    """Powody w kolejności, w której padły, każdy raz.

    Zbiór wypisywałby je w każdym przebiegu inaczej
    (``CLAUDE.md``, o porządku wypisywanego wyjścia).
    """
    return tuple(dict.fromkeys(powody))


def abstrahuj(czytanie: Node, kontekst: Kontekst = TERAZ) -> Odczyt:
    """Drzewa tego zapisu, z których wychodzi to czytanie parsera.

    Krotka pusta jest odpowiedzią: polszczyzna ma czytania,
    których ten zapis nie mówi, a które z nich to są,
    widać po tym, co stąd nie wraca.
    Czemu akurat to nie wróciło, mówi ``powody``.
    """
    if czytanie.label != "Sentence":
        raise ValueError(f"czytanie zdania, a nie {czytanie.label}")
    try:
        kandydaci = list(_ciąg(czytanie.children[0]))
    except (PozaZapisem, PozaRamą) as błąd:
        return Odczyt((), (str(błąd),))
    drzewa: list[Zdanie] = []
    powody: list[str] = []
    for drzewo in kandydaci:
        powód = _rozjazd(drzewo, czytanie, kontekst)
        if powód is None:
            drzewa.append(drzewo)
        else:
            powody.append(powód)
    return Odczyt(tuple(drzewa), _bez_powtórzeń(powody), len(kandydaci))


def rozbierz(zdanie: str, kontekst: Kontekst = TERAZ) -> Odczyt:
    """Drzewa tego zapisu, z których wychodzi to zdanie, po wszystkich czytaniach.

    Wieloznaczność napisu wychodzi tędy jako kilka drzew i nic jej nie odsiewa,
    bo pytanie jest tu o to, co autor mógł napisać, a nie o werdykt:
    werdykt wydaje ``olski/subset.py`` i wydaje go czytelnikowi tekstu.
    Drzewo powtórzone przez dwa czytania stoi raz,
    bo dwa razy to samo nie jest dwiema odpowiedziami.

    Powody zbierają się po wszystkich czytaniach, a nie po tym jednym,
    które zaszło najdalej, bo czytania są tu odpowiedziami równorzędnymi
    i zdanie odrzucone przez każde z nich bywa odrzucone przez każde inaczej.

    Zdanie bez czytań ma powód osobny, bo mówi on o czym innym:
    pustka jest wtedy werdyktem gramatyki, a nie brakiem kategorii w tym zapisie,
    i zero kandydatów mówi tu o czytaniu, którego nie było, a nie o kategorii.
    """
    czytania = parse(GRAMMAR, morphology(zdanie), zatrzymanie=False).readings
    if not czytania:
        return Odczyt((), ("gramatyka olskiego nie wyprowadza tego zdania",))
    wynik: dict[tuple, Zdanie] = {}
    powody: list[str] = []
    kandydaci = 0
    for czytanie in czytania:
        odczyt = abstrahuj(czytanie, kontekst)
        powody.extend(odczyt.powody)
        kandydaci += odczyt.kandydaci
        for drzewo in odczyt.drzewa:
            wynik.setdefault(sygnatura(drzewo), drzewo)
    return Odczyt(tuple(wynik.values()), _bez_powtórzeń(powody), kandydaci)


def sygnatura(drzewo) -> tuple:
    """Co czyni dwa drzewa tego zapisu jednym drzewem.

    Drzewo mówi o sobie wszystko, co ma znaczyć, więc sygnatura jest nim samym
    z jedną różnicą: tożsamość wychodzi numerem, a nie obiektem.
    Obiekt jest zapisem tożsamości, bo tyle daje zmienna w Pythonie,
    a dwa drzewa zbudowane osobno nie mają jak dzielić obiektów,
    więc porównanie ich wprost odpowiadałoby przecząco zawsze.
    Numer nadawany po kolei trzyma to, co ta deklaracja niesie:
    nie która rzecz jest którą, tylko które wystąpienia są jedną.

    Liczone jest to po polach, a nie kategoria po kategorii,
    bo kategoria dopisana do składni i tu pominięta
    porównywałaby się z dokładnością do niczego.
    """
    return _sygnatura(drzewo, {})


def _sygnatura(co, tożsamości: dict[int, int]):
    if isinstance(co, Postać):
        numer = tożsamości.setdefault(id(co), len(tożsamości))
        return ("postać", numer, _sygnatura(co.kto, tożsamości))
    if is_dataclass(co):
        wartości = (_sygnatura(getattr(co, pole.name), tożsamości) for pole in fields(co))
        return (type(co).__name__, *wartości)
    if isinstance(co, tuple):
        return tuple(_sygnatura(element, tożsamości) for element in co)
    return co


@dataclass(frozen=True)
class Obieg:
    """Drzewo puszczone w obieg: napis, który z niego wyszedł, i drzewa, które wróciły.

    Niezmiennikiem jest przynależność, a nie równość, i wywodzi to
    ``docs/design-notes.md``: drzewo do napisu jest funkcją, napis do drzewa relacją,
    więc żąda się tego, żeby drzewo pierwotne stało wśród tych, które wróciły.
    """

    napis: str
    drzewo: Zdanie
    odczyt: Odczyt

    @property
    def wróciło(self) -> bool:
        return sygnatura(self.drzewo) in [sygnatura(drzewo) for drzewo in self.odczyt.drzewa]

    def opisz(self) -> str:
        """Zdanie, które ma przeczytać ten, komu obieg się nie zamknął."""
        if self.wróciło:
            return f"„{self.napis}” wraca tym drzewem"
        if not self.odczyt.drzewa:
            zdanie = f"„{self.napis}” nie wraca żadnym drzewem tego zapisu"
        else:
            #  Napisu drzew, które wróciły, nie ma tu po co wypisywać:
            #  każde z nich wypisuje się tym samym napisem i to jest warunek,
            #  po którym stąd wyszło, więc różnica siedzi w drzewie, a nie w tekście.
            zdanie = f"„{self.napis}” wraca {len(self.odczyt.drzewa)} drzewami i żadnym z nich"
        if not self.odczyt.powody:
            return zdanie
        return f"{zdanie}: {'; '.join(self.odczyt.powody)}"


def obieg(drzewo: Zdanie, kontekst: Kontekst = TERAZ) -> Obieg:
    """Drzewo wypisane i przeczytane z powrotem.

    Parser jest tu świadkiem, a nie zależnością, i to się przez ten moduł nie zmienia:
    zdanie, którego gramatyka nie obejmuje, wraca stąd bez żadnego drzewa,
    a kompilatorowi nie odbiera to niczego.
    Wywód trzyma ``docs/design-notes.md``.
    """
    napis = kompiluj(drzewo, kontekst)
    return Obieg(napis=napis, drzewo=drzewo, odczyt=rozbierz(napis, kontekst))
