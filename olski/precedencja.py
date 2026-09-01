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
tego samego. Dwie stałe niżej mówią to samo:
ciało wypisane w deklaracji jest podstawowe, a odstępstwo od niego stoi niżej.

Preprocesorem jest to dlatego, że rozwinięcie kończy się przed rozbiorem:
tablica Earleya dostaje ciała wypisane, takie same jak pisane ręką.
Warunek sprawdzany dopiero w lesie zdjąłby rozwinięcie i zmieniłby liczbę czytań,
i tam czeka drugi odbiorca takich warunków, czyli luka
(docs/parsowanie.md#kierunek-produkcja-się-rozwarstwia-a-podłoże-zostaje).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Sequence
from itertools import permutations

from olski.grammar import Grammar, Głowa, Part, Sym

#: Warunek precedencji: bierze nazwy córek w kolejności i mówi, czy taki szyk wchodzi.
#: Nazwą jest nazwa symbolu, a terminal nazwy nie ma i wchodzi tam pusty,
#: bo warunek mówi o kolejności konstytuentów, a nie o słowach między nimi.
Warunek = Callable[[tuple[str, ...]], bool]

#: Ile kosztuje konstytuent, który bierze okolicznik, wobec tego samego bez niego.
#: Znak jest zmierzony, wielkość nie
#: (docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie).
KOSZT_OKOLICZNIKA = 1

#: Ile kosztuje jedna para córek stojąca odwrotnie niż w wypisanej deklaracji.
#: Szyk wypisany kosztuje przez to zero, a każdy inny tyle, ile par trzeba
#: w nim odwrócić. Dwa szyki jednego zdania mają córki tej samej rozpiętości,
#: więc bez tej stałej rozstrzygałby o nich alfabet etykiet i `Janek lubi piwo.`
#: wychodziłoby czytaniem z `piwo` w podmiocie (``tests/test_morfologia.py``).
KOSZT_PRZESTAWIENIA = 1


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
        koszt: int = 0,
        **cechy,
    ) -> None:
        """Wpisz ten konstytuent każdym szykiem tych córek i każdym miejscem na okolicznik.

        Warunek precedencji pominięty zostawia szyk jeden, ten wypisany;
        podany przepuszcza te przestawienia córek, na które odpowiada prawdą.
        Cechy są wspólne wszystkim wypisanym ciałom, bo wypuszcza je konstytuent,
        a nie kolejność, w jakiej stoją jego córki.

        Koszt podany tutaj mówi, że cała ta rodzina jest konstrukcją nacechowaną,
        więc stoi w wydruku pod podstawową. Dodają się do niego dwa koszty
        wyliczane z deklaracji, bo produkcja niesie jedną liczbę.
        """
        for koszt_szyku, szyk in self._szyki(córki, precedencja):
            for koszt_okolicznika, ciało in self._miejsca(szyk):
                self.grammar.rule(
                    symbol, ciało, koszt=koszt + koszt_szyku + koszt_okolicznika, **cechy
                )

    def _szyki(
        self, córki: Sequence[Part | Głowa], precedencja: Warunek | None
    ) -> Iterator[tuple[int, list[Part | Głowa]]]:
        """Szyki, na które ten warunek pozwala, każdy wraz ze swoim kosztem."""
        if precedencja is None:
            yield 0, list(córki)
            return
        for numery in permutations(range(len(córki))):
            szyk = [córki[numer] for numer in numery]
            if precedencja(tuple(_nazwa(część) for część in szyk)):
                yield _przestawienia(numery) * KOSZT_PRZESTAWIENIA, szyk

    def _miejsca(self, szyk: Sequence[Part | Głowa]) -> Iterator[tuple[int, list[Part | Głowa]]]:
        """Ten szyk bez okolicznika, a za nim ten sam szyk z okolicznikiem w każdym miejscu.

        Miejsce jest za każdą córką, która okolicznika nie bierze sama — obok
        takiej córki byłoby ono drugim wyprowadzeniem jednego napisu — i miejsce
        na końcu konstytuenta jest tym za córką ostatnią, a nie regułą obok.

        Miejsca kosztują wszystkie tyle samo: okolicznik postawiony w innym miejscu
        obejmuje inne słowa, więc rozstrzyga o nim cięcie, a nie koszt
        (``_cięcie`` w ``olski/parse/las.py``).
        """
        nazwy = [_nazwa(część) for część in szyk]
        yield 0, list(szyk)
        for gdzie, córka in enumerate(nazwy, start=1):
            if córka in self.własny_okolicznik:
                continue
            yield KOSZT_OKOLICZNIKA, [*szyk[:gdzie], self.okolicznik, *szyk[gdzie:]]
