"""Własności kryterium ramowego, bez których jego tabela mówi o czym innym.

Sonda z `sonda/rama.py` stoi na jednym pytaniu — czy lemat żąda tego przyimka —
i odpowiedzieć na nie twierdząco można z trzech powodów, z których dwa ramą
lematu nie są: przyimek w pozycji podmiotu oraz przyimek zleksykalizowany wraz ze
swoim rzeczownikiem. Oba zawyżałyby zasięg po cichu, bo wydruk wygląda tak samo,
a różnicę widać dopiero w liczbach `docs/disambiguation.md`.

Testy idą po samym kryterium, a nie po przebiegu nad korpusem: Walenty i bank
drzew nie stoją w repozytorium, a schematy wpisane tutaj ręką są dokładnie tym, o
co kryterium pyta.
"""

from __future__ import annotations

import pytest

from sonda.rama import Odpowiedź, przyimki, render

#: Schemat `informacja`, skrócony do pozycji, o które pyta kryterium. Rama
#: rzeczownika jest tą połową, którą pomiar przyjmuje, więc wpis stąd jest
#: zarazem przykładem, na którym stoi wniosek tamtego dokumentu. `cp(że)` stoi w
#: nim po to, żeby pozycja nieprzyimkowa miała czym się nie dopasować.
INFORMACJA = " pewny: : : : {prepnp(o,loc);cp(że)} + {possp} + {prepnp(dla,gen)}"

#: Schemat, w którym przyimek stoi zleksykalizowany: `czekać na czas dobry` żąda
#: `na` wraz z rzeczownikiem, który przy nim stoi, a nie przy dowolnym.
ZLEKSYKALIZOWANY = " pewny: _: : imperf: subj{np(str)} + {lex(prepnp(na,acc),pl,'czas',natr)}"

#: Schemat, w którym przyimek stoi w pozycji podmiotu. Podmiot ma u olskiego
#: własną produkcję, a nie pozycję ramy, więc żądaniem o gospodarzu nie jest.
W_PODMIOCIE = " pewny: _: : imperf: subj{prepnp(o,loc)} + {np(str)}"


def test_rama_zbiera_pozycje_niepodmiotowe_i_pomija_nieprzyimkowe():
    assert przyimki([INFORMACJA]) == frozenset({"o", "dla"})


def test_przyimek_zleksykalizowany_nie_jest_żądaniem_ramy():
    assert przyimki([ZLEKSYKALIZOWANY]) == frozenset()


def test_przyimek_w_podmiocie_nie_jest_żądaniem_o_gospodarzu():
    assert przyimki([W_PODMIOCIE]) == frozenset()


@pytest.mark.parametrize(
    ("kwalifikator", "żądane"),
    [("potoczny", frozenset({"o"})), ("archaiczny", frozenset())],
)
def test_kwalifikator_rejestru_zostaje_a_kwalifikator_dawnej_polszczyzny_odpada(
    kwalifikator, żądane
):
    """Para, na której `BRANE` jest wyborem, a nie listą wszystkiego.

    Oba kwalifikatory odsyłają schemat poza polszczyznę ogólną, a odsyłają go w
    różne miejsca: `potoczny` mówi o rejestrze i schemat zostaje schematem,
    `archaiczny` mówi, że nikt tak nie napisze. Warunek pisany bez tej różnicy
    przechodzi wszystko albo odrzuca oba.
    """
    assert przyimki([f" {kwalifikator}: : : : {{prepnp(o,loc)}}"]) == żądane


def test_tylko_pewne_zawęża_do_schematów_niewątpliwych():
    wątpliwy = [" wątpliwy: : : : {prepnp(o,loc)}"]
    assert przyimki(wątpliwy) == frozenset({"o"})
    assert przyimki(wątpliwy, tylko_pewne=True) == frozenset()


def test_trafność_liczy_się_z_odpowiedzi_a_zasięg_z_populacji():
    """Dwa mianowniki, bo milczenie jest odpowiedzią o pozycji, a nie o gospodarzu.

    Trafność wzięta z populacji spadałaby wraz z milczeniem, którego świadek nie
    ma czym poprawić, i mówiłaby o zasięgu drugi raz zamiast o pomyłkach.
    """

    def odpowiedź(wskazany: str) -> Odpowiedź:
        return Odpowiedź(
            przyimek="o",
            czasownik="być",
            rzeczownik="informacja",
            wskazany=wskazany,
            wzorcowy="noun",
            fraza=None,
        )

    wydruk = render([odpowiedź("noun"), odpowiedź("clause"), odpowiedź(""), odpowiedź("")])
    assert "4 spornych przyłączeń" in wydruk
    assert "50.0% zasięg" in wydruk
    assert "50.0% trafność" in wydruk
