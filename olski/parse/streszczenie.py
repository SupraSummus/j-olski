"""Streszczenie czytania: jeden wiersz, którym werdykt nazywa, co zdanie mówi.

Czego ten napis nie odróżnia,
mówi :class:`Rozbieżność` (``olski/parse/podsumowanie.py``).
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence

from olski.parse.czytanie import Leaf, Node, Tree
from olski.parse.podsumowanie import Deklaracja

#: Znak, którym streszczenie oddziela modyfikator od tego, do czego doszedł.
#: Bez słowa, bo słowo żądałoby przypadka od tego, co po nim następuje,
#: a następuje tam forma wzięta ze zdania i nieodmieniana.
PRZYŁĄCZONY_DO = " → "

#: Znak, którym streszczenie oddziela dwa wypełnienia jednej roli.
#: Przecinka tu nie ma, bo przecinkiem wiersz streszczenia oddziela role od siebie
#: (``_role`` w ``olski/check.py``), więc rola o dwóch wypełnieniach czytałaby się
#: jak dwie role.
OBOK = " + "

#: Formy, przed którymi w napisie nie ma odstępu.
#: Wewnątrz konstytuentu gramatyka bierze jeden znak interpunkcyjny, przecinek
#: koordynacji; kropkę niesie węzeł nad rolami i do streszczenia nie dochodzi.
PRZYLEGAJĄCE = frozenset({","})


def liście(drzewo: Tree) -> Iterator[Leaf]:
    """Liście tego drzewa, w porządku zdania.

    Pyta o nie werdykt, bo odczytania formy niesie liść
    (:attr:`Leaf.odczytania`), a nie węzeł nad nim.
    """
    if isinstance(drzewo, Leaf):
        yield drzewo
        return
    for dziecko in drzewo.children:
        yield from liście(dziecko)


def sklej_formy(formy: Iterable[str]) -> str:
    """Formy jako jeden napis, tak jak stoją w zdaniu.

    Przecinek jest osobnym segmentem, więc sklejenie przez sam odstęp
    daje ``wolni , równi``, czego autor w swoim zdaniu nie napisał.
    """
    napis = ""
    for forma in formy:
        if napis and forma not in PRZYLEGAJĄCE:
            napis += " "
        napis += forma
    return napis


def describe(node: Node, deklaracja: Deklaracja) -> tuple[dict[str, str], ...]:
    """Streszczenie czytania: co stoi w której roli i do czego doszedł modyfikator.

    Streszczeń jest tyle, ile zdanie ma zdań składowych, po jednym na składowe,
    bo każde z nich obsadza role własnym materiałem
    (:func:`_zakresy` dzieli między nie zdanie),
    i widać w nich przez to całe zdanie współrzędne.
    Czemu nie jedno na zdanie i co ten podział kosztuje, mówi
    docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań.

    Dwa czytania jednego zdania gdzieś się różnią,
    a streszczenie pokazuje tę różnicę temu, kto ma zdanie poprawić.
    Same role tego nie pokazują,
    bo grupa przyimkowa dochodzi raz do jednej głowy, a raz do drugiej,
    i formy stojące nad nią zostają wtedy te same:
    ``koszt szynki z dodatkami`` jest tym samym dopełnieniem niezależnie od tego,
    czy ``z dodatkami`` doszło do ``koszt``, czy do ``szynki``.
    Rola przyłączana dostaje więc obok wypełnienia to, co modyfikator określa.

    Drugim takim miejscem jest granica członu w ciągu współrzędnym,
    i tam odpowiada nawias, a nie nazwa obok:
    granica biegnie wewnątrz wypełnienia, więc widać ją tylko w samym napisie.
    Co dostaje nawias, a co nie, mówi :func:`_nawiasuj`.

    Żądają tego role przyłączane,
    bo ich gospodarza gramatyka zostawia nierozstrzygniętego rozmyślnie:
    podmiot i dopełnienie rozstrzyga przypadek,
    a pozycje przyłączeniowe stoją po to, żeby dać oba czytania
    (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    Dopisane jest wypełnienie, a nie pozycja obok niego,
    więc :attr:`Deklaracja.role` zostaje listą ról.

    Rola przyłączana jest nazwana pierwszym wystąpieniem w składowym
    (:func:`_streszcz`), więc dwa czytania różne miejscem drugiego okolicznika
    tej samej roli wychodzą stąd jednym napisem.
    Streszczeń wychodzi przez to nie więcej niż czytań, bo powtórzone na listę
    nie wchodzi (``Verdict.readings`` w ``olski/werdykt.py``);
    zdanie, którego to nie rozstrzyga, rozstrzyga :meth:`Las.przyłączenia`,
    gdzie wpisów jest tyle, ile nierozstrzygniętych wyborów.

    Zdanie podrzędne jest z tego wyszukiwania wyjęte
    (:attr:`Deklaracja.podrzędne`), bo streszczane jest zdanie zewnętrzne.
    Zdanie współrzędne wyjęte nie jest, bo jego role są rolami tego samego
    zdania; osobne jest tylko streszczenie, w którym one stoją.
    """
    return tuple(
        _streszcz(node, deklaracja, zakres) for zakres in _zakresy(node, deklaracja.składowe)
    )


def _streszcz(node: Node, deklaracja: Deklaracja, zakres: tuple[int, int]) -> dict[str, str]:
    """Streszczenie tej części zdania: co stoi w której roli w niej.

    Rola przyłączana jest nazwana pierwszym wystąpieniem, a wypełniająca
    wszystkimi, i rozdziela je liczba, jaką każda z nich mieć może.
    Okoliczników stoi przy zdaniu dowolnie wiele, więc wypisane wszystkie
    rozmnożyłyby streszczenia. Wypełnień stoi najwyżej dwa
    (``PARA_WYPEŁNIEŃ`` w ``olski/subset/deklaracja.py``), a pierwsze z nich samo zostawia
    `Parser pokazuje autorowi oba czytania.` bez połowy tego, co olski w nim wziął.

    Rolę przypisuje zakresowi jej początek, a nie cała rozpiętość:
    dopowiedzenie za dwukropkiem stoi poza zdaniem składowym
    (``wypowiedzenie → zdanie : grupa_imienna .``), więc porównanie całych rozpiętości
    zostawiłoby je bez zakresu i streszczenie milczałoby o nim.
    """
    streszczenie = {}
    for rola in deklaracja.role:
        znalezione = [
            węzeł
            for węzeł in node.find(rola, deklaracja.podrzędne)
            if zakres[0] <= węzeł.span[0] < zakres[1]
        ]
        if not znalezione:
            continue
        if rola in deklaracja.przyłączane:
            napis = _nawiasuj(znalezione[0], deklaracja.współrzędne)
            napis += PRZYŁĄCZONY_DO + _attachment(node, znalezione[0], deklaracja.gospodarze)
        else:
            napis = OBOK.join(_nawiasuj(węzeł, deklaracja.współrzędne) for węzeł in znalezione)
        streszczenie[rola] = napis
    return streszczenie


def streszczenia(
    drzewa: Iterable[Node], deklaracja: Deklaracja
) -> list[tuple[dict[str, str], ...]]:
    """Streszczenia tych drzew, każde raz i w kolejności pierwszego wystąpienia.

    Dwa drzewa różne poza zasięgiem :func:`describe` wychodzą z niego jednym
    napisem, a napis wypisany drugi raz nie mówi nic ponad ten nad sobą.
    Wołają to dwa miejsca — odczytania zdania i kształty konstytuentu — i pierwsze
    z nich pokazuje, ile powtórzeń bywa: zdanie o siedmiu wyrażeniach
    przyimkowych ma odczytań ponad sto, a napisów różnych kilka.
    """
    return [streszczenie for streszczenie, _drzewa in streszczone(drzewa, deklaracja)]


def streszczone(
    drzewa: Iterable[Node], deklaracja: Deklaracja
) -> list[tuple[tuple[dict[str, str], ...], list[Node]]]:
    """Te drzewa pogrupowane po streszczeniu, w kolejności pierwszego wystąpienia.

    Odsiew ze :func:`streszczenia` jest tu jeden na oba pytania, bo werdykt pyta
    o jedno i drugie: o same streszczenia i o to, czym forma stoi pod każdym z
    nich (``Verdict.morfologia`` w ``olski/werdykt.py``). Napisany dwa razy
    rozjechałby się po cichu i wtedy morfologia opisywałaby inne streszczenie
    niż to, które nad nią wypisano.

    Grupa ma pod sobą drzewa, a nie jedno z nich, bo streszczenie zbiera czasem
    kilka kształtów, a odczytania formy nie muszą być w nich te same.
    """
    wynik: list[tuple[tuple[dict[str, str], ...], list[Node]]] = []
    for drzewo in drzewa:
        streszczenie = describe(drzewo, deklaracja)
        for gotowe, pod_nim in wynik:
            if gotowe == streszczenie:
                pod_nim.append(drzewo)
                break
        else:
            wynik.append((streszczenie, [drzewo]))
    return wynik


def _zakresy(node: Node, symbole: Sequence[str]) -> list[tuple[int, int]]:
    """Zdanie podzielone na tyle części, ile ma zdań składowych, po jednej na składowe.

    Granicą jest początek składowego następnego, a nie koniec poprzedniego,
    więc każde słowo zdania wpada dokładnie do jednej części
    i nie ginie z niej to, co między składowymi stoi: spójnik, przecinek,
    a za ostatnim składowym dopowiedzenie i kropka.
    Zdanie o jednym składowym wychodzi stąd całe i jedną częścią,
    tak samo jak konstytuent, który składowego nie ma pod sobą wcale.
    """
    początki = _początki_składowych(node, symbole)
    granice = [node.span[0], *początki[1:], node.span[1]]
    return [(granice[i], granice[i + 1]) for i in range(len(granice) - 1)]


def _początki_składowych(node: Node, symbole: Sequence[str]) -> list[int]:
    """Początki zdań składowych tego czytania, w porządku zdania.

    Bierzemy zdanie najwyższe w gałęzi, a nie każdy węzeł o tej etykiecie:
    okolicznik zdania dokłada nad zdaniem składowym drugie o tej samej etykiecie
    (``zdanie_składowe → wyrażenie_przyimkowe zdanie_składowe``),
    a członem ciągu jest zewnętrzne z tych dwóch.
    Zdanie podrzędne jest wewnątrz składowego, więc zejście do niego nie dochodzi
    i nie trzeba go tu odejmować osobno.
    Sam początek, bo granicą podziału jest początek składowego następnego
    (:func:`_zakresy`), a końca nie pyta nikt.
    """
    if node.label in symbole:
        return [node.span[0]]
    return [
        początek
        for dziecko in node.children
        if isinstance(dziecko, Node)
        for początek in _początki_składowych(dziecko, symbole)
    ]


def _nawiasuj(node: Node, współrzędne: Sequence[str]) -> str:
    """Formy tej roli, z członem ciągu współrzędnego w nawiasie kwadratowym.

    Ciąg współrzędny jest drugim po przyłączeniu miejscem,
    w którym dwa czytania mają w jednej roli te same formy:
    ``wolni i równi pod względem swej godności i swych praw``
    jest jednym orzecznikiem niezależnie od tego,
    czy wyrażenie przyimkowe należy do drugiego członu, czy do całego zdania.
    Nawias pokazuje granicę członu,
    więc te dwa przestają wychodzić jednym napisem.

    Nawiasujemy ciąg, którym jest sama rola, a nie każdy ciąg pod nią,
    i dlatego pętla niżej mija wyłącznie węzły o jednej córce.
    Ciąg pod przyimkiem albo pod rzeczownikiem jest częścią wypełnienia,
    a nie podziałem roli,
    więc nawias nad nim wypadłby w każdym czytaniu ten sam
    (``pod względem [swej godności] i [swych praw]``).
    """
    while not _koordynuje(node, współrzędne):
        if len(node.children) != 1 or isinstance(node.children[0], Leaf):
            return sklej_formy(node.forms())
        node = node.children[0]
    return sklej_formy(_kawałki(node, współrzędne))


def _kawałki(ciąg: Node, współrzędne: Sequence[str]) -> list[str]:
    """Ciąg rozpisany na napisy: człon dłuższy niż słowo w nawiasie, spójnik bez zmian.

    Ciąg trzech członów jest w tej gramatyce ciągiem dwóch,
    którego drugi jest ciągiem dwóch (``grupa_imienna → człon_imienny conj grupa_imienna``),
    więc po prawym skraju schodzimy rekurencyjnie:
    inaczej ``ustawienia, dane i pliki`` miałoby drugi człon długi na resztę ciągu.
    Człon jednosłowny nawiasu nie dostaje, bo jego granicę widać po spójniku obok.
    """
    kawałki = []
    for dziecko in ciąg.children:
        if isinstance(dziecko, Node) and _koordynuje(dziecko, współrzędne):
            kawałki.extend(_kawałki(dziecko, współrzędne))
        elif len(dziecko.forms()) > 1:
            kawałki.append(f"[{sklej_formy(dziecko.forms())}]")
        else:
            kawałki.append(sklej_formy(dziecko.forms()))
    return kawałki


def ciało_koordynuje(etykieta: str | None, córki: Iterable[str | None]) -> bool:
    """Czy ciało o tych córkach koordynuje: etykieta powtórzona wśród nich, a znak obok.

    Ciąg współrzędny jest resztą ciągu po odjęciu członu,
    więc symbol koordynacji stoi wśród własnych córek.
    Liczba córek-konstytuentów tego nie mówi:
    `grupa_imienna → człon_imienny zdanie_względne` ma je dwie i koordynacją nie jest.
    Samo powtórzenie symbolu też go nie mówi,
    bo nad ciągiem stoi jeszcze okolicznik zdaniowy dochodzący do całego ciągu,
    który powtarza go tak samo.
    Rozdziela je znak: koordynacja spina członów słowem,
    a przecinek okolicznika należy do konstytuentu, który spójnik tworzy,
    więc słowem w tym ciele nie stoi.
    Znak wchodzi tu pustą nazwą, bo :class:`Pozycja` liścia etykiety nie ma,
    i po tym samym poznają go pozostałe dwa wejścia.

    Pytają o to kryterium trzy miejsca:
    nawias w napisie roli (:func:`_koordynuje`),
    wybór przemilczany wśród rozbieżności (:meth:`Las._nazwany_gdzie_indziej`)
    i pomiar różnicowy (``koordynuje`` w ``harness/ruch.py``).
    Stoi w jednym, bo rozejście tych trzech widać dopiero w liczbach,
    a niezmiennik, na którym ono stoi, pilnuje ``tests/test_subset.py``.
    """
    nazwy = list(córki)
    return etykieta in nazwy and None in nazwy


def _koordynuje(node: Node, współrzędne: Sequence[str]) -> bool:
    """Czy produkcja tego węzła koordynuje; kryterium trzyma :func:`ciało_koordynuje`."""
    return node.label in współrzędne and ciało_koordynuje(
        node.label,
        (dziecko.label if isinstance(dziecko, Node) else None for dziecko in node.children),
    )


def _attachment(root: Node, modifier: Node, hosts: tuple[str, ...]) -> str:
    """Co modyfikator określa: konstytuent, do którego doszedł, nazwany swoją głową.

    Ani węzeł, pod którym modyfikator stoi bezpośrednio,
    ani najbliższy węzeł z materiałem obok na to pytanie nie odpowiadają:
    okolicznik zdania stoi w drzewie tuż obok dopełnienia, którego nie określa.
    Odpowiada konstytuent wyliczony w :attr:`Deklaracja.gospodarze`,
    czyli ten, w którego produkcji to przyłączenie stoi.
    """
    return _host(root, modifier, hosts, root).forma_głowy()


def _host(tree: Tree, modifier: Node, hosts: tuple[str, ...], outer: Node) -> Node | None:
    """Najbliższy konstytuent z ``hosts``, w którym stoi ten modyfikator; ``None`` poza nim.

    ``outer`` jest odpowiedzią dla korzenia,
    bo modyfikator, nad którym nie stoi żaden z tych konstytuentów, określa całe czytanie.
    """
    if tree is modifier:
        return outer
    if isinstance(tree, Leaf):
        return None
    inner = tree if tree.label in hosts else outer
    for child in tree.children:
        found = _host(child, modifier, hosts, inner)
        if found is not None:
            return found
    return None
