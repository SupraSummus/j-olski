"""Te własności korpusu usterek, bez których sonda nad nim wydaje liczbę nieprawdziwą.

Plik jest pisany ręką, więc psuje się po cichu: dwa zdania wklejone w jeden wpis
wywracają mianownik, wpis bez poprawki nie mówi, czy zgłoszenie widzi usterkę,
a klasa zamieniona miejscami odwraca wniosek, którego sonda jest kolejką.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.usterki import (
    CISZA,
    CZYSTE,
    NIECZYTANE,
    SZUM,
    WYKRYTE,
    ŹLE_CZYTANE,
    ŻADNE,
    Usterka,
    czytaj,
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


def wpis(zdanie, zgłoszenie, poprawka=None, kontekst=(), odczytanie=()):
    return Usterka(
        kontekst=kontekst,
        zdanie=zdanie,
        usterka="usterka" if zgłoszenie != ŻADNE else "",
        zgłoszenie=zgłoszenie,
        poprawka=poprawka,
        odczytanie=odczytanie,
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
    ("wpis", "klasa"),
    [
        #  Rola obsadzona tak, jak wpis prosi: zgłoszenie miałoby co przeczytać,
        #  więc brakuje samego wykrywacza.
        (
            wpis(
                "Chałka przewyższa zwykłą bułkę.",
                "brak chałki",
                "Bułka jest zwykła.",
                odczytanie=(("podmiot", "Chałka"),),
            ),
            CISZA,
        ),
        #  Ta sama rola obsadzona czym innym: wykrywacz nie ma czego przeczytać.
        (
            wpis(
                "Chałka przewyższa zwykłą bułkę.",
                "brak chałki",
                "Bułka jest zwykła.",
                odczytanie=(("podmiot", "zwykłą bułkę"),),
            ),
            ŹLE_CZYTANE,
        ),
        #  Role mają się spotkać w jednym odczytaniu: te dwie obsadza to zdanie
        #  każdą z osobna, a razem żadne z jego dwóch odczytań.
        (
            wpis(
                "Operator ustala priorytet.",
                "brak operatora",
                "Priorytet jest ustalony.",
                odczytanie=(("podmiot", "Operator"), ("dopełnienie", "Operator")),
            ),
            ŹLE_CZYTANE,
        ),
        #  Zdanie składowe jest przezroczyste: obie role stoją w jednym odczytaniu,
        #  a streszczenia mają osobne.
        (
            wpis(
                "Pies gonił kota, a on uciekł.",
                "niejasne odniesienie",
                "Pies gonił kota, a kot uciekł.",
                odczytanie=(("podmiot", "Pies"), ("podmiot", "on")),
            ),
            CISZA,
        ),
        #  Nieczytanie wyprzedza złe czytanie: zdanie bez odczytań żąda produkcji,
        #  a nie roli przestawionej w odczytaniu, którego nie ma.
        (
            wpis(
                "Nowa program zapisuje ustawienia.",
                "niezgodność",
                "Program zapisuje.",
                odczytanie=(("podmiot", "Nowa program"),),
            ),
            NIECZYTANE,
        ),
    ],
    ids=lambda x: x if isinstance(x, str) else x.zdanie[:30],
)
def test_role_wpisu_odróżniają_ciszę_od_złego_czytania(wpis, klasa):
    assert zbadaj(wpis).klasa == klasa


def korpus(tmp_path, *wiersze):
    plik = tmp_path / "u.txt"
    plik.write_text("\n".join(wiersze) + "\n", encoding="utf-8")
    return plik


def test_wpis_z_usterką_bez_poprawki_jest_błędem(tmp_path):
    plik = korpus(
        tmp_path,
        "zdanie: Czekają nagrody.",
        "usterka: coś",
        "zgłoszenie: wieloznaczne",
    )
    with pytest.raises(ValueError):
        czytaj(plik)


def test_odczytanie_rozpada_się_na_rolę_i_wypełnienie(tmp_path):
    #  Wypełnienie przychodzi z odstępem po dwukropku, a porównuje się je
    #  z napisem roli co do znaku, więc odstęp nieobcięty wywracałby każdy wpis
    #  w źle czytane.
    plik = korpus(
        tmp_path,
        "zdanie: Zespół programistów spotkali się rano.",
        "usterka: coś",
        "zgłoszenie: niezgodność",
        "odczytanie: podmiot: Zespół programistów",
        "odczytanie: orzeczenie: spotkali się",
        "poprawka: Zespół programistów spotkał się rano.",
    )
    (wpis,) = czytaj(plik)
    assert wpis.odczytanie == (("podmiot", "Zespół programistów"), ("orzeczenie", "spotkali się"))


def test_odczytanie_bez_wypełnienia_jest_błędem(tmp_path):
    #  Rola bez wypełnienia nie ma czego porównać z odczytaniem, więc wpis
    #  wychodziłby źle czytany, cokolwiek olski nad tym zdaniem przeczyta.
    plik = korpus(
        tmp_path,
        "zdanie: Czekają nagrody.",
        "usterka: coś",
        "zgłoszenie: wieloznaczne",
        "odczytanie: podmiot",
        "poprawka: Program otwierający się psuje.",
    )
    with pytest.raises(ValueError):
        czytaj(plik)


def test_wpis_czysty_z_odczytaniem_jest_błędem(tmp_path):
    #  Wpis czysty nie ma zgłoszenia, więc nie ma ról, których by ono potrzebowało,
    #  a pole przemilczane leżałoby w nim bez żadnego skutku.
    plik = korpus(
        tmp_path,
        "zdanie: Operator ustala priorytet.",
        "zgłoszenie: żadne",
        "odczytanie: podmiot: Operator",
    )
    with pytest.raises(ValueError):
        czytaj(plik)
