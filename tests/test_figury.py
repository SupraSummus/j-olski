"""Raport o figurach odpowiada z dwóch napisów i deklaracja rdzewieje jak wskaźnik.

Odpowiedź sprawdza się tu bez pliku i bez sondy, bo ``stan`` bierze treść pliku i
odciski drzewa wprost. Reszta to rdzewienie deklaracji: plik wymieniony w
``ruszają`` da się przemianować, a raport policzy go wtedy za należność i powodu
nie nazwie; sekcję restytuującą da się przemianować jak każdy nagłówek. Jedno i
drugie zawodzi tutaj, a nie u kogoś, kto sięgnął po korpus, bo przeliczenie jest
osobną komendą właśnie po to (``harness/figury.py``).

Rozstrzyganie wskaźników bierze się z ``tests/test_docs.py``, bo slug nagłówka
jest tym samym faktem tu i tam.
"""

from dataclasses import replace

import pytest
from test_docs import ROOT, assert_resolves

from harness.figury import (
    AKTUALNA,
    FIGURY,
    KATALOG,
    NALEŻNA,
    NIEZMIERZONA,
    NIEZNANY,
    NIKT,
    ZAMKNIĘTA,
    Figura,
    ciało,
    należność,
    przelicz,
    stan,
    zapis,
)

PRÓBNA = Figura(
    nazwa="próbna",
    polecenie=("python3", "-m", "sonda.wysunięcie", "proza/README.txt"),
    ruszają=("olski/subset.py", "sonda/wysunięcie.py"),
    czyta=("docs/subset.md#what-the-grammar-covers",),
)
#: Odciski drzewa, w którym nic się nie ruszyło od przebiegu figury.
TERAZ = {"olski/subset.py": "aaaaaaaaaaaa", "sonda/wysunięcie.py": "bbbbbbbbbbbb"}


def figury():
    return [pytest.param(figura, id=figura.nazwa) for figura in FIGURY]


@pytest.mark.parametrize(
    ("pisana", "zapisane", "odpowiedź", "powody"),
    [
        pytest.param(PRÓBNA, TERAZ, AKTUALNA, [], id="nic się nie ruszyło"),
        pytest.param(
            PRÓBNA,
            {**TERAZ, "olski/subset.py": "cccccccccccc"},
            NALEŻNA,
            ["olski/subset.py"],
            id="gramatyka się ruszyła",
        ),
        pytest.param(
            PRÓBNA,
            {**TERAZ, "sonda/wysunięcie.py": NIEZNANY},
            NIEZMIERZONA,
            ["sonda/wysunięcie.py"],
            id="odcisk nieznany bije zgodność reszty",
        ),
        pytest.param(
            replace(PRÓBNA, ruszają=("olski/subset.py",)),
            {"olski/subset.py": "aaaaaaaaaaaa"},
            NALEŻNA,
            ["sonda/wysunięcie.py"],
            id="ruszający dopisany po przebiegu",
        ),
        pytest.param(
            replace(PRÓBNA, polecenie=("python3", "-m", "sonda.wysunięcie", "proza/")),
            TERAZ,
            NALEŻNA,
            ["polecenie"],
            id="przebieg czytał inny korpus",
        ),
    ],
)
def test_odpowiedź_bierze_się_z_odcisków_i_z_polecenia(
    pisana: Figura, zapisane: dict, odpowiedź: str, powody: list
):
    assert stan(PRÓBNA, zapis(pisana, zapisane, "wydruk"), TERAZ) == (odpowiedź, powody)


def test_polecenie_z_nową_linią_nie_wychodzi_z_raportu_jako_należne():
    #  Zdanie podane komendzie po ``-c`` bywa wielowierszowe, a nagłówek pliku
    #  figury czyta się do pierwszego wiersza pustego, więc bez ucieczki polecenie
    #  urywa się w połowie i figura jest należna przeliczenia po każdym przebiegu.
    wielowierszowa = replace(
        PRÓBNA, polecenie=("python3", "-m", "olski.check", "-c", "Zdanie.\nDrugie.")
    )
    zapisane = zapis(wielowierszowa, TERAZ, "wydruk")
    assert stan(wielowierszowa, zapisane, TERAZ) == (AKTUALNA, [])


def test_kod_niezerowy_jest_pomiarem_tylko_przy_pustym_wyjściu_błędu(tmp_path, monkeypatch):
    #  ``olski-check`` odpowiada 1, kiedy nie każde zdanie jest olskim, czyli nad
    #  każdą prawdziwą prozą, a tym samym kodem kończy Python na wyjątku. Bez tego
    #  rozróżnienia figurą stałby się ślad stosu i nic by tego nie powiedziało.
    #  Korzeń idzie razem z katalogiem, bo przeliczenie liczy odciski względem
    #  niego i drukuje ścieżkę pliku figury jako względną.
    monkeypatch.setattr("harness.figury.KORZEŃ", tmp_path)
    monkeypatch.setattr("harness.figury.KATALOG", tmp_path / "figury")
    pomiar = replace(
        PRÓBNA, nazwa="pomiar", polecenie=("sh", "-c", "echo liczba; exit 1"), kody=(0, 1)
    )
    assert przelicz(pomiar) == 0
    assert ciało(pomiar.plik.read_text(encoding="utf-8")) == "liczba"

    ślad = replace(
        pomiar, nazwa="ślad", polecenie=("sh", "-c", "echo liczba; echo błąd >&2; exit 1")
    )
    assert przelicz(ślad) == 2
    assert not ślad.plik.exists()


@pytest.mark.parametrize("figura", figury())
def test_każdy_zadeklarowany_ruszający_jest_plikiem_który_istnieje(figura: Figura):
    for plik in figura.ruszają:
        assert (ROOT / plik).exists(), f"{figura.nazwa} nazywa plik, którego nie ma: {plik}"


@pytest.mark.parametrize("figura", figury())
def test_każda_figura_nazywa_sekcję_która_ją_restytuuje(figura: Figura):
    assert figura.czyta, f"{figura.nazwa} nie nazywa sekcji, która ją restytuuje"
    for sekcja in figura.czyta:
        path, _, anchor = sekcja.partition("#")
        assert_resolves(ROOT / path, anchor, figura.nazwa)


def test_figura_której_nikt_nie_powtórzy_nie_jest_należna_choć_gramatyka_się_ruszyła():
    #  To jest cały zysk z tego pola: jedna zmiana w `olski/subset.py` czyni dziś
    #  należnymi czterdzieści figur, a przebieg, którego nikt nie powtórzy, nie
    #  jest wśród nich winien przeliczenia nikomu.
    assert należność(replace(PRÓBNA, powtórzy=NIKT)) == (ZAMKNIĘTA, [])


@pytest.mark.parametrize("figura", figury())
def test_figura_zamknięta_ma_wydruk_który_ją_zamyka(figura: Figura):
    #  Zamknięcie mówi, że przebiegu nikt nie powtórzy, więc figura bez pliku
    #  zamknięta być nie może: nie ma liczby, którą ten przebieg miałby zostawić.
    if figura.zamknięta:
        assert figura.plik.exists(), f"{figura.nazwa} jest zamknięta bez wydruku"


@pytest.mark.parametrize("figura", figury())
def test_figura_programu_spoza_drzewa_nazywa_commit_który_go_trzyma(figura: Figura):
    #  Kasowanie sondy jest tu domyślne, więc figura zostaje z poleceniem, którego
    #  nikt nie wykona. Bez commita liczba przestaje być odtwarzalna dokładnie w tej
    #  chwili, a plik figury czyta się później niż commit, który sondę skasował.
    moduły = [słowo for słowo in figura.polecenie if słowo.startswith("sonda.")]
    for moduł in moduły:
        ścieżka = ROOT / f"sonda/{moduł.removeprefix('sonda.')}.py"
        if not ścieżka.exists():
            assert figura.w_gicie, f"{figura.nazwa} bierze {moduł}, którego nie ma w drzewie"


def test_commit_trzymający_sondę_wchodzi_do_nagłówka_pliku_figury():
    #  Deklaracja i plik figury czytają się osobno: po commicie sięga ten, kto
    #  znalazł liczbę, a nie ten, kto czyta `FIGURY`, więc nagłówek niesie go też.
    skasowana = replace(PRÓBNA, w_gicie="c2377c3")
    assert "w gicie: c2377c3" in zapis(skasowana, TERAZ, "wydruk")


def test_każdy_plik_w_katalogu_jest_zadeklarowany():
    #  Tylko w tę stronę: figura zadeklarowana bez pliku jest stanem, o którym
    #  raport mówi ``bez pliku``, czyli deklaracją stojącą przed pierwszym
    #  przebiegiem, a plik bez deklaracji jest wydrukiem, którego nic nie umie
    #  powtórzyć ani orzec o nim, czy jest jeszcze aktualny.
    zadeklarowane = {figura.plik for figura in FIGURY}
    for plik in KATALOG.glob("*.txt"):
        assert plik in zadeklarowane, f"wydruk bez deklaracji w FIGURY: {plik.name}"
