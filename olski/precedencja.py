"""Dominacja rozdzielona od precedencji, wraz z preprocesorem, który je składa.

Produkcja mówi naraz dwie rzeczy: z czego konstytuent się składa
i w jakiej kolejności te córki stoją.
Polszczyzna stawia je w kilku kolejnościach,
więc gramatyka wypisująca każdą osobno rośnie mnożąc się,
a miejsce na okolicznik, wypisane w każdym ciele z osobna,
bywa w którymś zapomniane.
Zdanie wychodzi wtedy jednym czytaniem, bo drugie nie miało gdzie się wyprowadzić,
i po werdykcie tego nie widać
(docs/parsowanie.md#wyliczone-ciało-myli-się-w-stronę-werdyktu).

Deklaracja niżej mówi te dwie rzeczy osobno.
:class:`Rozwinięcie` niesie to, co jest wspólne całej rodzinie zdaniowej:
symbol okolicznika i odpowiedź na pytanie, po której córce on staje.
:meth:`Rozwinięcie.dominacja` bierze same córki,
obok nich warunek precedencji nad ich kolejnością,
i wpisuje do gramatyki każdy szyk, jaki ten warunek dopuszcza,
w każdym miejscu na okolicznik, jakie ten szyk ma.

Ciała jednego rozwinięcia konkurują potem o to samo zdanie, więc każde dostaje tu
koszt, czyli miejsce w kolejności, w jakiej las wyda te czytania
(``wyprowadzenia`` w ``olski/parse/las.py``).
Wylicza go rozwinięcie, a nie wypisuje deklaracja: produkcji jest tysiąc kilkaset,
z czego siedemset samego ``orzeczenia``, więc koszt wypisany byłby drugą deklaracją
tego samego. Dwie pozycje cennika mówią tu to samo — ``PRZESTAWIENIE`` i
``OKOLICZNIK`` (``olski/cennik.py``): ciało wypisane w deklaracji jest podstawowe,
a odstępstwo od niego stoi niżej.

Preprocesorem jest to dlatego, że rozwinięcie kończy się przed rozbiorem:
tablica Earleya dostaje ciała wypisane, takie same jak pisane ręką.
Warunek sprawdzany dopiero w lesie zdjąłby rozwinięcie i zmieniłby liczbę czytań,
i tam czeka drugi odbiorca takich warunków, czyli luka
(docs/parsowanie.md#kierunek-produkcja-się-rozwarstwia-a-podłoże-zostaje).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import permutations

from olski.cennik import OKOLICZNIK, PRZESTAWIENIE
from olski.grammar import Grammar, Głowa, Part, Sym

#: Warunek precedencji: bierze nazwy córek w kolejności i mówi, czy taki szyk wchodzi.
#: Nazwą jest nazwa symbolu, a terminal nazwy nie ma i wchodzi tam pusty,
#: bo warunek mówi o kolejności konstytuentów, a nie o słowach między nimi.
Warunek = Callable[[tuple[str, ...]], bool]


def _przestawienia(numery: Sequence[int]) -> int:
    """Ile par tego szyku stoi odwrotnie niż w deklaracji, czyli odległość Kendalla."""
    return sum(
        1
        for pierwsza in range(len(numery))
        for druga in range(pierwsza + 1, len(numery))
        if numery[pierwsza] > numery[druga]
    )


def _nazwa(część: Part | Głowa) -> str:
    """Nazwa symbolu tej córki; znacznik głowy jest przezroczysty.

    Głowa mówi o roli córki, a nie o tym, czym ona jest, więc warunek jej nie widzi.
    """
    if isinstance(część, Głowa):
        część = część.część
    return część.name if isinstance(część, Sym) else ""


class Rozwinięcie:
    """Gdzie w konstytuencie staje okolicznik, i wpisywanie takiego konstytuenta do gramatyki.

    Miejsce na okolicznik jest tu wyliczone, a nie wypisane, i wylicza je jedna reguła:
    okolicznik staje po każdej córce, która jest grupą, oraz na końcu konstytuenta.
    Pierwsza połowa reguły jest odpowiedzią na przyłączenie,
    które olski oddaje czytelnikowi: gdzie grupa imienna bierze wyrażenie przyimkowe
    za sobą, tam musi umieć wziąć je też zdanie, bo inaczej gramatyka wybiera
    przyłączenie przez przeoczenie
    (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).

    Córki czasownikowej reguła nie wyjmuje, bo polszczyzna stawia okolicznik i
    tam; co kosztowało wyjmowanie jej, trzyma
    docs/subset.md#zdanie-deklaruje-córki-a-warunek-deklaruje-szyk.

    Miejsca nie dostaje ``grupa_orzeczenia``, bo okolicznik bierze ono samo, przez
    ``wypełnienia``, więc miejsce obok niego byłoby drugim wyprowadzeniem jednego
    napisu. Dotyczy to obu miejsc, jakie taka córka ma — tego za nią i tego na
    końcu konstytuenta — i dlatego pyta o nie jeden zbiór, a nie dwa.
    """

    def __init__(
        self,
        grammar: Grammar,
        okolicznik: Part,
        własny_okolicznik: Iterable[str],
    ) -> None:
        self.grammar = grammar
        self.okolicznik = okolicznik
        self.własny_okolicznik = frozenset(własny_okolicznik)

    def dominacja(
        self,
        symbol: str,
        córki: Sequence[Part | Głowa],
        precedencja: Warunek | None = None,
        koszty: tuple[str, ...] = (),
        **cechy,
    ) -> None:
        """Wpisz ten konstytuent każdym szykiem tych córek i każdym miejscem na okolicznik.

        Warunek precedencji pominięty zostawia szyk jeden, ten wypisany;
        podany przepuszcza te przestawienia córek, na które odpowiada prawdą.
        Cechy są wspólne wszystkim wypisanym ciałom, bo wypuszcza je konstytuent,
        a nie kolejność, w jakiej stoją jego córki.

        Pozycje cennika podane tutaj mówią, czym cała ta rodzina jest nacechowana,
        więc stoi ona w wydruku pod podstawową. Dokładają się do nich dwie pozycje
        wyliczane z deklaracji, bo produkcja niesie jedną listę.
        """
        for szyk_płaci, szyk in self._szyki(córki, precedencja):
            for okolicznik_płaci, ciało in self._miejsca(szyk):
                self.grammar.rule(
                    symbol, ciało, koszty=(*koszty, *szyk_płaci, *okolicznik_płaci), **cechy
                )

    def _szyki(
        self, córki: Sequence[Part | Głowa], precedencja: Warunek | None
    ) -> Iterator[tuple[tuple[str, ...], list[Part | Głowa]]]:
        """Szyki, na które ten warunek pozwala, każdy wraz z tym, czym płaci.

        Odległość Kendalla stoi tu w miejscu pozycji cennika powtórzonej, bo szyk
        odległy o dwie zamiany jest dwa razy dalej od wypisanego niż szyk odległy
        o jedną. Dwa szyki jednego zdania mają córki tej samej rozpiętości, więc
        bez tej pozycji rozstrzygałby o nich alfabet etykiet i `Janek lubi piwo.`
        wychodziłoby czytaniem z `piwo` w podmiocie (``tests/test_morfologia.py``).
        """
        if precedencja is None:
            yield (), list(córki)
            return
        for numery in permutations(range(len(córki))):
            szyk = [córki[numer] for numer in numery]
            if precedencja(tuple(_nazwa(część) for część in szyk)):
                yield (PRZESTAWIENIE,) * _przestawienia(numery), szyk

    def _miejsca(
        self, szyk: Sequence[Part | Głowa]
    ) -> Iterator[tuple[tuple[str, ...], list[Part | Głowa]]]:
        """Ten szyk bez okolicznika, a za nim ten sam szyk z okolicznikiem w każdym miejscu.

        Miejsce jest za każdą córką, która okolicznika nie bierze sama — obok
        takiej córki byłoby ono drugim wyprowadzeniem jednego napisu — i miejsce
        na końcu konstytuenta jest tym za córką ostatnią, a nie regułą obok.

        Miejsca kosztują wszystkie tyle samo: okolicznik postawiony w innym miejscu
        obejmuje inne słowa, więc rozstrzyga o nim cięcie, a nie koszt
        (``_cięcie`` w ``olski/parse/las.py``).
        """
        nazwy = [_nazwa(część) for część in szyk]
        yield (), list(szyk)
        for gdzie, córka in enumerate(nazwy, start=1):
            if córka in self.własny_okolicznik:
                continue
            yield (OKOLICZNIK,), [*szyk[:gdzie], self.okolicznik, *szyk[gdzie:]]
