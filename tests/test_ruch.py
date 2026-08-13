"""Własności sondy różnicowej, bez których jej tabela mówi o innej gramatyce.

Sonda może skłamać po cichu na trzy sposoby: wariant, który miał być olskim, a nie
jest, bo przepisanie produkcji coś po drodze zgubiło; wariant jednej grupy, który
zdejmuje cudzą albo zostawia obie; oraz produkcja dopisana bez nazwy grupy, która
zostaje w mianowniku i każe sondzie mierzyć zero. Każdy z trzech zostawia wydruk
takim, jak wyglądał, więc widać go dopiero w liczbach `docs/subset.md`. Czwarta
własność jest o zdaniach, którymi te trzy są sprawdzane: zdanie stojące na jednej
grupie ma wychodzić jednoznaczne także pod wszystkimi grupami naraz.

Te cztery idą po `SONDY`, a nie po jednej z nich, bo są własnościami deklaracji, a
nie przecinka ani liczebnika: sonda dopisana do tej listy dostaje je za darmo, a
pominięta w niej nie ma ich wcale. Idą przy tym po `Sonda.czysty`, a nie po
numerze wariantu, bo sonda dopisująca ma olskiego na przeciwnym końcu listy niż
sonda zdejmująca.

Niżej stoją trzy testy o jednej sondzie każdy, bo tyle grup i wstawek nie ma
zdania, które by je pokazało z listy wyżej.
"""

from __future__ import annotations

import pytest

pytest.importorskip("morfeusz2")

from olski.subset import GRAMMAR, build, check
from sonda import liczebnik, negacja, przecinek, przysłówek, szyk
from sonda.ruch import Sonda, gramatyka

SONDY = [przecinek.SONDA, liczebnik.SONDA, negacja.SONDA, szyk.SONDA, przysłówek.SONDA]

#: Sondy mierzące konstrukcję, której olski nie ma. Osobna lista, bo dopisek jest
#: tym, o czym mówi test niżej, a sonda zdejmująca przeszłaby go bez treści.
DOPISUJĄCE = [sonda for sonda in SONDY if sonda.dopisuje is not None]

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
]


@pytest.mark.parametrize("sonda", SONDY, ids=lambda sonda: sonda.prog)
def test_wariant_czysty_jest_dokładnie_gramatyką_olskiego(sonda: Sonda):
    assert gramatyka(sonda, sonda.czysty).productions == GRAMMAR.productions


@pytest.mark.parametrize("sonda", DOPISUJĄCE, ids=lambda sonda: sonda.prog)
def test_każda_produkcja_dopisana_należy_do_jakiejś_grupy(sonda: Sonda):
    """Dopisek bez nazwy grupy zostaje w mianowniku i sonda mierzy wtedy zero.

    Odsiew pyta o grupę i nic więcej, więc produkcja, o której sonda mówi
    ``None``, przechodzi do każdego wariantu — mianownika włącznie — i różnica,
    którą sonda liczy, jest wtedy różnicą wobec gramatyki, która tę produkcję już
    ma. Wydruk wygląda przy tym tak samo, tylko z zerami w wierszach.
    """
    świeża = build()
    ile = len(świeża.productions)
    sonda.dopisuje(świeża)
    dopisane = świeża.productions[ile:]
    assert dopisane
    assert [p for p in dopisane if sonda.grupa(p) is None] == []


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

    Pytamy wariant ostatni, a nie olskiego: u sondy dopisującej olski tego zdania
    nie wyprowadza wcale, bo dopiero dopisek daje mu wyprowadzenie, a żądanie
    jest to samo — jednoznaczność pod wszystkim, co sonda mierzy razem.
    """
    pełna = gramatyka(sonda, sonda.warianty[-1])
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


def test_przysłówek_nie_dochodzi_do_zaimka_względnego():
    """Pozycję przysłówka dostaje klasa otwarta, a nie każdy znacznik `adj`.

    Zaimek względny ma w Morfeuszu znacznik przymiotnika, więc pozycja liczona z
    samego znacznika dosięgnie i jego, a `bardzo który` polszczyzną nie jest.
    Warunek na wypisany lemat jest tym, co go wyłącza, i jest najbardziej
    oczywistym uproszczeniem tej sondy.
    """
    zdanie = "Plik, bardzo który program zapisuje, jest nowy."
    for wariant in przysłówek.SONDA.warianty:
        assert [w.status for w in check(zdanie, gramatyka(przysłówek.SONDA, wariant))] == [
            "rejected"
        ]


def test_gospodarzem_przyłączenia_zostaje_przymiotnik_a_nie_przysłówek_przed_nim():
    """Głowa jest numerem pozycji w ciele, więc przesuwa się razem z wstawką.

    Bez przesunięcia werdykt nazywa gospodarzem przyłączenia przysłówek —
    `z interesami → bardzo` — czyli zdanie o zdaniu, którego polszczyzna nie ma,
    a liczba czytań zostaje przy tym ta sama i tabela sondy niczego nie pokazuje.

    Gospodarze wchodzą tu zbiorem, bo żądanie jest o to, którzy nimi są, a nie o
    kolejność, w jakiej las wydaje czytania.
    """
    [werdykt] = check(
        "Program jest bardzo powiązany z interesami.",
        gramatyka(przysłówek.SONDA, "przy przymiotniku"),
    )
    assert {czytanie.get("Modifier") for czytanie in werdykt.readings} == {
        "z interesami → powiązany",
        "z interesami → jest",
    }
