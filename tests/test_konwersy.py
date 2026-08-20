"""Kryterium, którym sonda zgaduje konwers z kształtu pozycji.

Walentego ten test nie potrzebuje, tak samo jak ``tests/test_walenty.py``:
schematy pisane ręcznie mówią o kryterium wszystko, co się o nim rozstrzyga, a
plik wejściowy nie stoi w repozytorium.
"""

import pytest

from harness.konwersy import alternatywy, konwersy, opisz

#: Para, o którą tej sondzie chodzi: ``wynająć komuś`` i ``wynająć od kogoś``,
#: obie w postaci, w jakiej stoją w Walentym.
ODBIORCA = "subj{np(str)} + obj{np(str)} + {np(dat)} + {prepnp(do,gen)}"
ŹRÓDŁO = "subj{np(str)} + obj{np(str)} + {prepnp(od,gen)}"


def test_para_schematów_o_dwóch_stronach_wymiany_wraca_z_lematem():
    znalezione = konwersy({"wynająć": [ODBIORCA, ŹRÓDŁO]})
    assert [konwers.lemat for konwers in znalezione] == ["wynająć"]
    assert znalezione[0].odbiorca == ODBIORCA
    assert znalezione[0].źródło == ŹRÓDŁO


def test_obie_pozycje_w_jednym_schemacie_zdejmują_cały_lemat():
    #  Odbiorca i źródło stojące w jednym zdaniu obok siebie opowiadają je z
    #  jednej strony, więc drugi schemat tego lematu nie jest drugą stroną
    #  niczego. Zdjęty jest cały lemat, a nie sam ten schemat: bez tego zostałaby
    #  para złożona z dwóch schematów jednostronnych.
    razem = "subj{np(str)} + obj{np(str)} + {np(dat)} + {prepnp(od,gen)}"
    assert konwersy({"kupić": [ODBIORCA, ŹRÓDŁO, razem]}) == []


def test_celownik_zleksykalizowany_nie_zamyka_pary():
    #  ``pożyczyć coś od kogoś dla siebie`` ma celownik żądający słowa ``siebie``,
    #  więc uczestnika w tej pozycji nie ma i wymiany ona nie nazywa. Czytana
    #  jako celownik zdejmowałaby lemat regułą wyżej.
    siebie = "subj{np(str)} + obj{np(part)} + {prepnp(od,gen)} + {lex(np(dat),_,'siebie',natr)}"
    assert opisz(siebie).celownik is False
    assert [konwers.lemat for konwers in konwersy({"pożyczyć": [ODBIORCA, siebie]})] == ["pożyczyć"]


@pytest.mark.parametrize(
    ("schemat", "przechodni"),
    [
        (ODBIORCA, True),
        #  ``obj`` jest kawałkiem napisu ``subj``, więc etykiety czytane samym
        #  ``in`` dają dopełnienie każdemu schematowi z podmiotem.
        ("subj{np(str)} + {np(dat)}", False),
        ("subj,controller{np(str)} + controllee{infp(_)}", False),
        ("subj{np(str)} + obj,controller{np(str)} + controllee{infp(_)}", True),
    ],
)
def test_dopełnienia_szuka_się_poza_pozycją_podmiotu(schemat, przechodni):
    assert opisz(schemat).przechodni is przechodni


def test_fraza_źródłowa_w_pozycji_podmiotu_nie_nazywa_uczestnika():
    #  ``od`` z dopełniaczem stoi w podmiocie zdania o tym, co się od czegoś
    #  zaczyna, i mówi tam co innego niż w pozycji obok dopełnienia.
    assert opisz("subj{prepnp(od,gen)} + obj{np(str)}").źródło is False


def test_alternatywy_rozcinają_się_po_średnikach_spoza_nawiasów():
    #  Średnik rozdziela kształty, którymi pozycja może się wypełnić, a stoi też
    #  wewnątrz pozycji zleksykalizowanej, gdzie rozdziela słowa: Walenty pisze
    #  tam ``OR('twarz';'usta')``.
    assert alternatywy("{np(str);ncp(str,że)}") == ["np(str)", "ncp(str,że)"]
    zleksykalizowana = "{lex(prepnp(na,loc),_,OR('twarz';'usta'),atr);np(dat)}"
    assert alternatywy(zleksykalizowana) == ["np(dat)"]
