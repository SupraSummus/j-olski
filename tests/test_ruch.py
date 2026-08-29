"""Własności pomiaru różnicowego, bez których jego tabela mówi o innej gramatyce.

Przebieg może skłamać po cichu na dwa sposoby: wariant, który miał być olskim, a
nie jest, bo przepisanie produkcji coś po drodze zgubiło, oraz wariant jednej
grupy, który zdejmuje cudzą albo zostawia obie. Oba zostawiają wydruk takim, jak
wyglądał, więc widać je dopiero w liczbach `docs/subset.md`. Trzecia własność jest
o zdaniach, którymi te dwie są sprawdzane: zdanie stojące na jednej grupie ma
wychodzić jednoznaczne także pod wszystkimi grupami naraz.

Idą po `SONDY`, bo są własnościami deklaracji, a nie przysłówka: deklaracja
dopisana do tej listy dostaje je za darmo. Stoi w niej jedna, bo przebieg
wyceniający wpuszczenie konstrukcji jest skryptem sesji i do drzewa nie wchodzi
(`CLAUDE.md#code`), a ta jedna została, bo `harness/płaski.py` buduje nią wariant.
"""

from __future__ import annotations

import pickle

import pytest

pytest.importorskip("morfeusz2")

from harness import płaski
from harness.corpus import FULL, Sentence
from harness.ruch import Sonda, gramatyka, nad_prozą, zmierz
from olski.subset import GRAMMAR
from olski.werdykt import check

SONDY = [płaski.PRZYSŁÓWEK_SONDA]

#: Deklaracja, wariant i zdanie, które stoi dokładnie na tej jednej grupie
#: produkcji. Po jednym zdaniu na grupę zdejmowaną osobno, bo grupa bez zdania
#: nie jest sprawdzona przez nic.
NA_JEDNEJ_GRUPIE = [
    (płaski.PRZYSŁÓWEK_SONDA, "okolicznik", "Teraz program zapisuje ustawienia."),
    (płaski.PRZYSŁÓWEK_SONDA, "przy przymiotniku", "Koszt bardzo dużego pliku jest niski."),
]


@pytest.mark.parametrize("sonda", SONDY, ids=lambda sonda: sonda.nazwa)
def test_sonda_przechodzi_do_procesu_roboczego(sonda: Sonda):
    """`przebieg` posyła sondę do procesu roboczego, więc sonda ma się dać posłać.

    Usterka, którą to łapie: pole `gramatyki` wypełnione domknięciem. Sonda liczy
    wtedy w jednym procesie to samo, co liczyłaby w kilku, więc każdy test obok
    przechodzi, a `--jobs` większe od jednego wywraca przebieg nad całym bankiem
    drzew — czyli dokładnie ten, po który sonda stoi.
    """
    assert pickle.loads(pickle.dumps(sonda)) == sonda


@pytest.mark.parametrize("sonda", SONDY, ids=lambda sonda: sonda.nazwa)
def test_wariant_czysty_jest_dokładnie_gramatyką_olskiego(sonda: Sonda):
    assert gramatyka(sonda, sonda.czysty).productions == GRAMMAR.productions


@pytest.mark.parametrize("sonda", SONDY, ids=lambda sonda: sonda.nazwa)
def test_wariant_jest_podzbiorem_olskiego_i_nie_dopisuje_ani_jednej_produkcji(sonda: Sonda):
    """Pominięcie rozbiorów w `_warianty` opiera się na tej własności i nie bada jej.

    Czytania wariantu są podzbiorem czytań olskiego dopóty,
    dopóki podzbiorem są jego produkcje,
    i tylko wtedy zdanie odrzucone przez olskiego wolno uznać za odrzucone
    pod każdym wariantem.
    Produkcja dopisana wariantowi z tej listy dałaby więc wiersz o zdaniach,
    których nikt nie rozebrał, i nic w wydruku by tego nie pokazało.
    Sondzie wyceniającej pozycję, której olski nie ma, dopisywać wolno,
    a kolejność wariantów odpowiada tam za to samo (`Sonda` w `harness/ruch.py`).
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
    raport = zmierz(płaski.PRZYSŁÓWEK_SONDA, [zdanie], źródło="live")
    assert raport.przejścia[płaski.PRZYSŁÓWEK_SONDA.czysty] == {"rejected → valid": 1}
    assert not raport.zgodność


#: Proza pod przebieg nad nią: zdanie, które kupuje przysłówek u pierwszego
#: gospodarza, zdanie odrzucone przez każdy wariant i napis, którego nic nie
#: punktuje jako zdania. Trzy, bo o trzy rzeczy naraz pyta pominięcie rozbiorów.
PROZA = (
    "Teraz program zapisuje ustawienia. "
    "Nowa program zapisuje ustawienia. "
    "Nagłówek bez kropki\n\n"
    #  Napis, który olski czyta po domknięciu, czyli werdykt `unclosed`. Stoi tu
    #  dlatego, że pominięcie oparte na tym werdykcie zamiast na samym znaku
    #  wpuszczałoby go do mianownika, a przebieg mierzyłby wtedy ekstrakcję.
    "Cena jest niska"
)


def test_zdanie_przyjęte_przez_wariant_przeżywa_pominięcie_zbędnych_rozbiorów():
    """Rozbiór pomija się po werdykcie olskiego, a nie po werdykcie mianownika.

    Mianownik zdejmuje wszystko, więc odrzuca właśnie te zdania, które sonda ma
    policzyć jako zakup: pominięcie oparte na nim wypisałoby je odrzucone pod
    każdym wariantem, kolumna przyjętych stanęłaby na zerze i żaden wiersz
    wydruku by nie powiedział, że przebieg mierzył co innego, niż mówi.
    """
    raport = nad_prozą(płaski.PRZYSŁÓWEK_SONDA, PROZA)
    sonda = płaski.PRZYSŁÓWEK_SONDA
    assert raport.stany[sonda.czysty] == {"valid": 1, "rejected": 1}
    assert raport.stany[sonda.warianty[0]] == {"rejected": 2}
    assert raport.przejścia[sonda.czysty] == {"rejected → valid": 1}


def test_napis_bez_znaku_kończącego_nie_wchodzi_do_mianownika_przebiegu_nad_prozą():
    """Nagłówek i pozycja listy dochodzą tu jako akapity i zdaniem nie są.

    Policzone jako odrzucone mierzyłyby ekstrakcję zamiast podzbioru, więc stoją
    osobno, wypisane z powodem, a nie odjęte po cichu.

    Liczy się tu sam brak znaku, a nie werdykt: napisów bez znaku są dwa rodzaje,
    bo jeden z nich olski po domknięciu czyta, a oba stoją poza mianownikiem
    (`Verdict.punktowane` w `olski/werdykt.py`).
    """
    raport = nad_prozą(płaski.PRZYSŁÓWEK_SONDA, PROZA)
    assert raport.pominięte == {"fragment, a nie zdanie": 2}
    assert raport.zmierzone == 2
