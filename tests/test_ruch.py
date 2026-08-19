"""Własności sondy różnicowej, bez których jej tabela mówi o innej gramatyce.

Sonda może skłamać po cichu na dwa sposoby: wariant, który miał być olskim, a nie
jest, bo przepisanie produkcji coś po drodze zgubiło, oraz wariant jednej grupy,
który zdejmuje cudzą albo zostawia obie. Oba zostawiają wydruk takim, jak
wyglądał, więc widać je dopiero w liczbach `docs/subset.md`. Trzecia własność jest
o zdaniach, którymi te dwie są sprawdzane: zdanie stojące na jednej grupie ma
wychodzić jednoznaczne także pod wszystkimi grupami naraz.

Te trzy idą po `SONDY`, a nie po jednej z nich, bo są własnościami deklaracji, a
nie przysłówka ani wysunięcia: sonda dopisana do tej listy dostaje je za darmo, a
pominięta w niej nie ma ich wcale. Idą przy tym po `Sonda.czysty`, a nie po
numerze wariantu, bo tak samo pyta o niego `sonda/płaski.py`.

Lista jest krótka, bo sonda różnicowa wychodzi z drzewa razem z konstrukcją,
którą wyceniła (`sonda/__init__.py`), a te własności są o kształcie deklaracji,
więc sprawdza je każda sonda, która akurat stoi.
"""

from __future__ import annotations

import pytest

pytest.importorskip("morfeusz2")

from olski.corpus import FULL, Sentence
from olski.subset import GRAMMAR, check
from sonda import przysłówek, wysunięcie
from sonda.ruch import Sonda, gramatyka, zmierz

SONDY = [
    przysłówek.SONDA,
    wysunięcie.SONDA,
]

#: Sonda, wariant i zdanie, które stoi dokładnie na tej jednej grupie produkcji.
#: Po jednym zdaniu na grupę zdejmowaną osobno, bo grupa bez zdania nie jest
#: sprawdzona przez nic.
NA_JEDNEJ_GRUPIE = [
    (przysłówek.SONDA, "okolicznik", "Teraz program zapisuje ustawienia."),
    (przysłówek.SONDA, "przy przymiotniku", "Koszt bardzo dużego pliku jest niski."),
    (
        wysunięcie.SONDA,
        "grupa względna z przyimkiem",
        "Reguła, na podstawie której program zapisuje ustawienia, jest tania.",
    ),
    (
        wysunięcie.SONDA,
        "grupa względna bez przyimka",
        "Ustawa, której przepisy obowiązują, jest tania.",
    ),
    (wysunięcie.SONDA, "grupa pytajna z przyimkiem", "W którym roku ustawa weszła?"),
]


@pytest.mark.parametrize("sonda", SONDY, ids=lambda sonda: sonda.prog)
def test_wariant_czysty_jest_dokładnie_gramatyką_olskiego(sonda: Sonda):
    assert gramatyka(sonda, sonda.czysty).productions == GRAMMAR.productions


@pytest.mark.parametrize("sonda", SONDY, ids=lambda sonda: sonda.prog)
def test_wariant_jest_podzbiorem_olskiego_i_nie_dopisuje_ani_jednej_produkcji(sonda: Sonda):
    """Pominięcie rozbiorów w `_warianty` opiera się na tej własności i nie bada jej.

    Czytania wariantu są podzbiorem czytań olskiego dopóty,
    dopóki podzbiorem są jego produkcje,
    i tylko wtedy zdanie odrzucone przez olskiego wolno uznać za odrzucone
    pod każdym wariantem.
    Sonda dopisująca produkcję dałaby więc wiersz o wariancie,
    którego nikt nie policzył, i nic w wydruku by tego nie pokazało.
    Kierunek przez dopisywanie ta maszyneria miała i może go odzyskać.
    """
    olski = gramatyka(sonda, sonda.czysty).productions
    for wariant in sonda.warianty:
        assert set(gramatyka(sonda, wariant).productions) <= set(olski), wariant


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
        text="Teraz program zapisuje ustawienia.",
        verdict=FULL,
        roles=(("Subject", 0, 1),),
    )
    raport = zmierz(przysłówek.SONDA, [zdanie], źródło="live")
    assert raport.przejścia[przysłówek.SONDA.czysty] == {"rejected → valid": 1}
    assert not raport.zgodność
