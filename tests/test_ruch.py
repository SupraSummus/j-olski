"""Własności sondy różnicowej, bez których jej tabela mówi o innej gramatyce.

Sonda może skłamać po cichu na dwa sposoby: wariant, który miał być olskim, a nie
jest, bo przepisanie produkcji coś po drodze zgubiło, oraz wariant jednej grupy,
który zdejmuje cudzą albo zostawia obie. Oba zostawiają wydruk takim, jak
wyglądał, więc widać je dopiero w liczbach `docs/subset.md`. Trzecia własność jest
o zdaniach, którymi te dwie są sprawdzane: zdanie stojące na jednej grupie ma
wychodzić jednoznaczne także pod wszystkimi grupami naraz.

Te trzy idą po `SONDY`, a nie po jednej z nich, bo są własnościami deklaracji, a
nie przecinka ani liczebnika: sonda dopisana do tej listy dostaje je za darmo, a
pominięta w niej nie ma ich wcale. Idą przy tym po `Sonda.czysty`, a nie po
numerze wariantu, bo tak samo pyta o niego `sonda/płaski.py`.

Niżej stoi jeden test o jednej sondzie, bo grupy, której żadne zdanie nie pokaże,
nie ma jak sprawdzić z listy wyżej.
"""

from __future__ import annotations

import pytest

pytest.importorskip("morfeusz2")

from olski.corpus import FULL, Sentence
from olski.subset import GRAMMAR, check
from sonda import liczebnik, negacja, okolicznikowe, przecinek, przysłówek, szyk
from sonda.ruch import Sonda, gramatyka, zmierz

SONDY = [
    przecinek.SONDA,
    liczebnik.SONDA,
    negacja.SONDA,
    szyk.SONDA,
    przysłówek.SONDA,
    okolicznikowe.SONDA,
]

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
    (szyk.SONDA, "SOV", "Inwestorzy pomysł ten zwalczali."),
    (szyk.SONDA, "OSV", "Ustawienia program zapisuje."),
    (szyk.SONDA, "VSO", "Podzieli ona Twoje nadzieje."),
    (szyk.SONDA, "VOS", "Porastają ją wiekowe akacje."),
    (przysłówek.SONDA, "okolicznik", "Teraz program zapisuje ustawienia."),
    (przysłówek.SONDA, "przy przymiotniku", "Koszt bardzo dużego pliku jest niski."),
    (
        okolicznikowe.SONDA,
        "za zdaniem",
        "Program zapisuje ustawienia, ponieważ linter sprawdza dokumentację.",
    ),
    (
        okolicznikowe.SONDA,
        "przed zdaniem",
        "Ponieważ linter sprawdza dokumentację, program zapisuje ustawienia.",
    ),
]


@pytest.mark.parametrize("sonda", SONDY, ids=lambda sonda: sonda.prog)
def test_wariant_czysty_jest_dokładnie_gramatyką_olskiego(sonda: Sonda):
    assert gramatyka(sonda, sonda.czysty).productions == GRAMMAR.productions


@pytest.mark.parametrize(
    ("sonda", "zdanie"), [(sonda, zdanie) for sonda, _, zdanie in NA_JEDNEJ_GRUPIE]
)
def test_zdanie_stojące_na_jednej_grupie_wychodzi_jednoznaczne_pod_wszystkimi_grupami(
    sonda: Sonda, zdanie: str
):
    """Zakup każdej grupy przeżywa wszystkie pozostałe, i to jest tu żądanie.

    Wariant grupy zdejmuje cudze produkcje, więc `valid` pod nim nie mówi nic o
    tym, co zdanie robi w gramatyce pełnej: druga grupa może dać mu drugie
    czytanie i wtedy pierwsza dalej je kupuje, a gramatyka z obiema je odrzuca.
    Bez tej linii taką stratę widać dopiero w tabeli `docs/subset.md`.

    Pytamy wariant ostatni, który jest samym olskim, bo żądanie jest o
    jednoznaczność pod wszystkim, co sonda mierzy razem.
    """
    pełna = gramatyka(sonda, sonda.czysty)
    assert [w.status for w in check(zdanie, pełna)] == ["valid"]


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


def test_przebieg_po_morfologii_żywej_nie_porównuje_ról_z_drzewem_wzorcowym():
    """Rozpiętości spod żywej morfologii nie są rozpiętościami drzewa wzorcowego.

    Pozycje idą tam za znakami napisu, a nie za tokenami banku drzew, więc
    porównanie ról odpowiadałoby o czym innym, niż o co pyta. Zdanie stoi tu bez
    ani jednego segmentu i to jest część żądania: przebieg po żywej morfologii
    czyta sam napis, więc bank drzew jest mu potrzebny do jednego — do tego, żeby
    było co czytać.
    """
    zdanie = Sentence(
        sent_id="żywa",
        text="Program zapisuje ustawienia, ponieważ linter sprawdza dokumentację.",
        verdict=FULL,
        roles=(("Subject", 0, 1),),
    )
    raport = zmierz(okolicznikowe.SONDA, [zdanie], źródło="live")
    assert raport.przejścia[okolicznikowe.SONDA.czysty] == {"rejected → valid": 1}
    assert not raport.zgodność


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
