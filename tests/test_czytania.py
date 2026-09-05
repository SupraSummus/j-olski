"""Ta jedna własność sondy o czytaniach, na której stoi jej tabela.

Sonda dzieli zdania wieloznaczne na klasy nazwane tym, co werdykt o zdaniu
wypisuje, i cała wartość tabeli leży w tym, że klasa da się sprawdzić przez
przeczytanie werdyktu. Rozejść się mogą po jednym ruchu, który docstring
:class:`olski.parse.Deklaracja` wprost zapowiada: podsumowanie następne dokłada
tam pole, ``explain`` zaczyna je wypisywać, a ``klasa`` o nim nie wie, więc
zdanie z nowym wierszem werdyktu wpada do klasy „sama liczba czytań” i tabela
mówi, że werdykt milczy tam, gdzie mówi.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.czytania import SAMA_LICZBA, całe_przyłączenie, klasa
from olski.werdykt import check
from olski.werdykt.zdanie import _odczytań

#: Po jednym zdaniu na klasę, którą ta sonda kiedykolwiek naliczyła nad
#: Składnicą, w brzmieniu, które przechodzi przez żywą morfologię.
ZDANIA = [
    "Koszt samej szynki przewyższa koszt szynki z dodatkami.",
    "W poniedziałek spotkał się z wiernymi na południowej modlitwie.",
    "Nadchodzi druga rewolucja internetowa.",
    "Znajdujemy się u początku naszego eksperymentu.",
    "Tata musiał pojechać do domu.",
]


@pytest.mark.parametrize("zdanie", ZDANIA)
def test_klasa_milczy_dokładnie_tam_gdzie_milczy_werdykt(zdanie: str):
    werdykty = check(zdanie)
    assert len(werdykty) == 1
    werdykt = werdykty[0]
    assert werdykt.result.ambiguous
    milczy = werdykt.explain() == _odczytań(werdykt.result.ile)
    assert (klasa(werdykt.result) == SAMA_LICZBA) is milczy


@pytest.mark.parametrize(
    ("zdanie", "całe"),
    [
        ("Czeka koń z furą.", True),
        ("Koszt samej szynki przewyższa koszt szynki z dodatkami.", False),
    ],
)
def test_przyłączenie_jest_całą_decyzją_wtedy_gdy_iloczyn_gospodarzy_wyczerpuje_las(
    zdanie: str, całe: bool
):
    """Te dwa zdania niosą cały wywód spod tabeli, więc one są tu świadkiem.

    Oba mają w werdykcie i rolę, i przyłączenie, a decyzję zostawiają inną:
    nad `Czeka koń z furą.` podmiot rusza się dlatego, że rusza się przyłączenie,
    a nad zdaniem o szynce szyk odwraca się niezależnie od niego. Nazwa klasy
    nie odróżnia ich wcale i to jest powód, dla którego liczy je osobno iloczyn.
    """
    werdykt = check(zdanie)[0]
    assert werdykt.result.ambiguous
    assert klasa(werdykt.result) == "rola + przyłączenie"
    assert całe_przyłączenie(werdykt.result) is całe
