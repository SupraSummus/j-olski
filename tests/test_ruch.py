"""Te dwie własności sondy różnicowej, na których stoi jej tabela.

Jedyne, czym taka sonda może skłamać po cichu: wariant pełny, który miał być
olskim, a nie jest, bo przepisanie produkcji coś po drodze zgubiło, oraz wariant
jednej grupy, który zdejmuje cudzą albo zostawia obie. Wtedy każda liczba w
`docs/subset.md` jest liczbą o innej gramatyce i nic tego nie widać po wydruku.

Testy idą po `SONDY`, a nie po jednej z nich, bo obie własności są własnościami
deklaracji, a nie przecinka ani liczebnika: sonda dopisana do tej listy dostaje
je za darmo, a pominięta w niej nie ma ich wcale.
"""

from __future__ import annotations

import pytest

pytest.importorskip("morfeusz2")

from olski.subset import GRAMMAR, check
from sonda import liczebnik, negacja, przecinek
from sonda.ruch import Sonda, gramatyka

SONDY = [przecinek.SONDA, liczebnik.SONDA, negacja.SONDA]

#: Sonda, wariant i zdanie, które stoi dokładnie na tej jednej grupie produkcji.
#: Po jednym zdaniu na grupę zdejmowaną osobno, bo grupa bez zdania nie jest
#: sprawdzona przez nic.
NA_JEDNEJ_GRUPIE = [
    (przecinek.SONDA, "zdaniowy", "Wstaję, wyglądam przez okno."),
    (przecinek.SONDA, "imienny", "Kobiety muszą zakrywać włosy, ramiona, nogi."),
    (przecinek.SONDA, "przymiotnikowy", "Plik jest nowy, duży."),
    (liczebnik.SONDA, "zgodny", "Działają dwie rzeczy."),
    (liczebnik.SONDA, "rządzący", "Pięć kobiet przyszło."),
    (negacja.SONDA, "cząstka", "Program nie działa."),
]


@pytest.mark.parametrize("sonda", SONDY, ids=lambda sonda: sonda.prog)
def test_wariant_pełny_jest_dokładnie_gramatyką_olskiego(sonda: Sonda):
    assert gramatyka(sonda, sonda.warianty[-1]).productions == GRAMMAR.productions


@pytest.mark.parametrize(("sonda", "wariant", "zdanie"), NA_JEDNEJ_GRUPIE)
def test_wariant_grupy_zostawia_swoją_produkcję_i_zdejmuje_pozostałe(
    sonda: Sonda, wariant: str, zdanie: str
):
    """Zdanie, które stoi na jednej grupie, rozstrzyga o obu stronach naraz.

    Wariant, który zdejmuje za dużo, odrzuci je mimo swojej nazwy, a wariant,
    który zdejmuje za mało, przyjmie je pod cudzą. Mianownik jest wspólny, więc
    jeden taki błąd rozjeżdża całą tabelę, a nie jeden jej wiersz.
    """
    assert [w.status for w in check(zdanie, gramatyka(sonda, sonda.warianty[0]))] == ["rejected"]
    for nazwa in sonda.osobne:
        oczekiwane = "valid" if nazwa == wariant else "rejected"
        assert [w.status for w in check(zdanie, gramatyka(sonda, nazwa))] == [oczekiwane]


def test_dopełniacz_negacji_sam_nie_licencjonuje_ani_jednego_zdania():
    """Grupa, której nie pokaże żadne zdanie, i to jest o niej odczyt.

    Reszta tego pliku sprawdza grupy zdaniem, które stoi na jednej z nich, a ta
    grupa takiego zdania nie ma: dopełniacz negacji wpuszcza czasownik, który
    przeczy, więc bez cząstki nie ma go co wystrzelić. Wariant jest przez to
    kopią mianownika i tak go czyta `docs/subset.md` — zero w jego wierszu jest
    odczytem, a nie przeoczeniem, i przestałoby nim być po cichu, gdyby ta
    produkcja kiedyś dostała drugiego licencjodawcę.
    """
    for zdanie in ("Program nie zapisuje ustawień.", "Program zapisuje ustawienia."):
        bez = [w.status for w in check(zdanie, gramatyka(negacja.SONDA, "bez negacji"))]
        sam = [w.status for w in check(zdanie, gramatyka(negacja.SONDA, "dopełniacz"))]
        assert sam == bez
