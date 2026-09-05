"""Te własności korpusu usterek, bez których sonda nad nim wydaje liczbę nieprawdziwą.

Plik jest pisany ręką, więc psuje się po cichu: dwa zdania wklejone w jeden wpis
wywracają mianownik, wpis bez poprawki nie mówi, czy zgłoszenie widzi usterkę,
a klasa zamieniona miejscami odwraca wniosek, którego sonda jest kolejką.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.usterki import (
    BEZ_DOMKNIĘCIA,
    BEZ_LICENCJI,
    CISZA,
    CZYSTE,
    NIECZYTANE,
    SZUM,
    WYKRYTE,
    ZATRZYMANIE,
    ŻADNE,
    Usterka,
    czytaj,
    ostatnie,
    punkt,
    wydruk,
    zbadaj,
)
from olski.segmentacja import sentences
from olski.werdykt import ODNIESIENIE, POPRAWKA, WIELOZNACZNE

WPISY = czytaj()


def test_korpus_ma_wpisy_z_usterką_i_czyste():
    #  Plik z samymi usterkami nie mierzy szumu, a z samymi czystymi nie jest kolejką.
    assert any(not wpis.czysty for wpis in WPISY)
    assert any(wpis.czysty for wpis in WPISY)


@pytest.mark.parametrize("wpis", WPISY, ids=lambda wpis: wpis.zdanie[:40])
def test_zdanie_i_poprawka_są_po_jednym_zdaniu(wpis):
    assert len(sentences(wpis.zdanie)) == 1
    if wpis.poprawka:
        assert len(sentences(wpis.poprawka)) == 1


def test_zdanie_stoi_w_korpusie_raz():
    zdania = [wpis.zdanie for wpis in WPISY]
    assert len(zdania) == len(set(zdania))


def wpis(zdanie, zgłoszenie, poprawka=None, kontekst=()):
    return Usterka(
        kontekst=kontekst,
        zdanie=zdanie,
        usterka="usterka" if zgłoszenie != ŻADNE else "",
        zgłoszenie=zgłoszenie,
        poprawka=poprawka,
    )


@pytest.mark.parametrize(
    ("wpis", "klasa"),
    [
        #  Zaimek pada nad zdaniem i milczy nad poprawką: to jest wykrycie.
        (wpis("On uciekł.", ODNIESIENIE, "Kot uciekł.", ("Pies gonił kota.",)), WYKRYTE),
        #  Wieloznaczność pada i nad zdaniem, i nad poprawką, więc usterki nie widzi.
        (wpis("Czekają nagrody.", WIELOZNACZNE, "Program otwierający się psuje."), SZUM),
        #  Olski zdanie czyta, a zgłoszenia o tej nazwie nie wydaje nikt.
        (wpis("Chałka przewyższa zwykłą bułkę.", "brak chałki", "Bułka jest zwykła."), CISZA),
        #  Olski zdania nie czyta, więc o usterce nie mówi gramatyka, a nie wykrywacz.
        (wpis("Nowa program zapisuje ustawienia.", "niezgodność", "Program zapisuje."), NIECZYTANE),
        #  Poprawka pada nad zdaniem nieczytanym i to jest wykrycie, a nie nieczytanie.
        (
            wpis(
                'Przepisem "Zasad techniki prawodawczej" jest ustawa.',
                POPRAWKA,
                "Przepisem „Zasad techniki prawodawczej” jest ustawa.",
            ),
            WYKRYTE,
        ),
        (wpis("Chałka przewyższa zwykłą bułkę.", ŻADNE), CZYSTE),
        #  Wieloznaczność nad wpisem czystym szumem nie jest: poprawiać nad nią
        #  nie ma czego, bo znaleziskiem nie jest.
        (wpis("Czekają nagrody.", ŻADNE), CZYSTE),
        #  Zaimek nad wpisem czystym szumem jest, bo autor przepisałby to zdanie.
        (wpis("On uciekł.", ŻADNE, kontekst=("Pies gonił kota.",)), SZUM),
    ],
    ids=lambda x: x if isinstance(x, str) else x.zdanie[:30],
)
def test_klasa_bierze_się_ze_zdania_i_z_poprawki_naraz(wpis, klasa):
    assert zbadaj(wpis).klasa == klasa


@pytest.mark.parametrize(
    ("zdanie", "grupa"),
    [
        #  Nazwy własnej ani angielskiego czasownika nie bierze ani jedna produkcja,
        #  więc wpis o takim zdaniu żąda licencji formy, a nie produkcji.
        ("Robocopy kompaktuje pliki.", BEZ_LICENCJI),
        #  Licencję ma tu każda forma, a analiza staje na bezokoliczniku.
        ("Kot jadać rybę.", ZATRZYMANIE),
        #  Analiza dochodzi do końca zdania, a nic go nie domyka,
        #  więc werdykt nie nazywa żadnej formy.
        ("Nowa program zapisuje ustawienia.", BEZ_DOMKNIĘCIA),
    ],
    ids=lambda x: x,
)
def test_nieczytanie_dzieli_się_po_punkcie_zatrzymania(zdanie, grupa):
    verdict = ostatnie((), zdanie).werdykt
    assert punkt(verdict) == grupa, verdict.explain()


def test_poprawek_czytanych_liczy_się_z_wpisów_z_usterką():
    #  Wpis czysty poprawki nie ma, więc do mianownika nie wchodzi.
    #  Wliczony zaniżałby liczbę, po którą się ten wiersz czyta.
    wyniki = [
        zbadaj(wpis("On uciekł.", ODNIESIENIE, "Kot uciekł.", ("Pies gonił kota.",))),
        zbadaj(wpis("Kot jadać rybę.", ODNIESIENIE, "Kot jadać rybę i mięso.")),
        zbadaj(wpis("Chałka przewyższa zwykłą bułkę.", ŻADNE)),
    ]
    assert "poprawek czytanych 1 z 2" in wydruk(wyniki)


def test_wpis_z_usterką_bez_poprawki_jest_błędem(tmp_path):
    plik = tmp_path / "u.txt"
    plik.write_text("zdanie: Czekają nagrody.\nusterka: coś\nzgłoszenie: wieloznaczne\n", encoding="utf-8")
    with pytest.raises(ValueError):
        czytaj(plik)
