"""Słownictwo projektu, czyli zdanie o lemacie, którego podzbiór nie wypowiada.

Wykluczenie słownikowe jest zakładem o rejestr: dobrym tam, gdzie o grze nikt nie
pisze, i fałszywym w tekście o grze. Pilnowane jest to, co deklaracja robi i czego
nie robi: że sięga lematu, o który prosi, i żadnego obok, oraz że kosztuje.

Sam plik, wraz z tym, co zgłasza zamiast przemilczeć, pilnuje
``tests/test_konfiguracja.py``.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.morph import analyse
from olski.segmentacja import admissible, morphology, w_słownictwie
from olski.słownictwo import Słownictwo
from olski.werdykt import werdykt


def lematy(segmenty, forma):
    """Lematy, jakie analiza zostawiła tej formie."""
    return {
        czytanie.lemma
        for segment in segmenty
        if segment.form == forma
        for czytanie in segment.readings
    }


# --------------------------------------------------------------------------- #
# Kierunek `wpuszczane`, czyli uchylenie wykluczenia słownikowego
# --------------------------------------------------------------------------- #


def test_lemat_wpuszczony_zostaje_przy_czytaniu_które_wykluczenie_zdejmuje():
    #  Cała treść tego kierunku: `go` jest u Morfeusza grą obok zaimka, a gra nie
    #  odmienia się przez nic, więc wykluczenie zabiera ją każdemu. Tekstowi o
    #  grze zabiera przy tym słowo, o którym on jest.
    forma = analyse("go")[0]
    assert lematy([admissible(forma)], "go") == {"on"}
    wpuszczone = Słownictwo(wpuszczane=frozenset({"go"}))
    assert lematy([admissible(forma, wpuszczone)], "go") == {"on", "go"}


def test_tekst_o_grze_wyprowadza_się_dopiero_z_deklaracją():
    #  Zdanie idzie przez cały łańcuch, a nie przez sam warunek, bo uchylenie ma
    #  wrócić werdyktem, a nie czytaniem, którego żadna produkcja nie bierze.
    #  Bez deklaracji `Go` nie ma czytania rzeczownikowego, więc podmiotu nie ma
    #  z czego zbudować i analiza staje za nim.
    zdanie = "Go jest grą."
    assert werdykt(zdanie, morphology(zdanie), None).status == "rejected"
    z_deklaracją = morphology(zdanie, Słownictwo(wpuszczane=frozenset({"go"})))
    assert werdykt(zdanie, z_deklaracją, None).status == "valid"


def test_uchylenie_sięga_lematu_o_który_prosi_i_żadnego_obok():
    #  Deklaracja jest o lemacie, a nie o klasie czytań, więc `do` zostaje przy
    #  nucie zdjętej także w projekcie, który zadeklarował `go`. Warunek pisany
    #  na część mowy albo na samą nieodmienność uchylałby wykluczenie całe.
    słownictwo = Słownictwo(wpuszczane=frozenset({"go"}))
    assert lematy(morphology("Jedziemy do Włoch.", słownictwo), "do") == {"do"}


def test_uchylenie_oddaje_całe_czytanie_więc_zaimek_traci_jednoznaczność():
    #  Cena tego kierunku i jedyne miejsce, w którym ją widać: uchylone czytanie
    #  jest nieodmienne, więc żądaniu przypadka nie odmawia nigdy, a `go` jest
    #  w tekście o grze zarazem zaimkiem. Zdanie z zaimkiem dostaje przez to
    #  czytanie podmiotowe, którego polszczyzna nie ma, bo zaimek `go` jest
    #  biernikiem i dopełniaczem. Kto ten warunek zawęzi, ma tu zobaczyć, że
    #  deklaracja przestała kosztować.
    zdanie = "Kierują go na kursy dywersji."
    assert werdykt(zdanie, morphology(zdanie), None).status == "valid"
    z_deklaracją = morphology(zdanie, Słownictwo(wpuszczane=frozenset({"go"})))
    znalezione = werdykt(zdanie, z_deklaracją, None)
    assert znalezione.status == "ambiguous"
    assert any("Subject" in jedno for (jedno,) in znalezione.readings)


def test_przydawki_dopełniaczowej_deklaracja_nie_kupuje_bo_niesie_ją_zaimek():
    #  Granica tego, po co ta deklaracja jest, i łatwo ją przeoczyć: zaimek `go`
    #  jest także dopełniaczem, więc gra w tej pozycji wyprowadza się bez niczego.
    #  Kto by tego nie wiedział, deklarowałby lemat po to, czego już ma, i płacił
    #  za to jednoznacznością zdań z zaimkiem (test wyżej).
    zdanie = "Zasady go są proste."
    assert werdykt(zdanie, morphology(zdanie), None).status == "valid"


# --------------------------------------------------------------------------- #
# Kierunek `pomijane`, czyli lemat, którego projekt nie używa
# --------------------------------------------------------------------------- #


def test_lemat_pomijany_schodzi_z_formy_którą_dzieli_z_zaimkiem():
    #  Po to ten kierunek jest: `sobie` czyta się zaimkiem zwrotnym i celownikiem
    #  rzeczownika `soba`, a kryterium z `admissible` po ten lemat nie sięga i
    #  sięgnąć nie może, bo `soba` odmienia się przez przypadki.
    assert lematy(morphology("Zrobiłem sobie profil."), "sobie") == {"siebie", "soba"}
    słownictwo = Słownictwo(pomijane=frozenset({"soba"}))
    assert lematy(morphology("Zrobiłem sobie profil.", słownictwo), "sobie") == {"siebie"}


def test_pominięcie_zostawia_krawędź_bez_ani_jednego_czytania():
    #  Tym różni się ten warunek od `admissible`, które krawędzi nie opróżnia
    #  nigdy, a zgadza się z `po_przyimku`: projekt, który mówi, że słowa nie
    #  używa, mówi to także o zdaniu, w którym stoi ono samo, i werdykt nazywa
    #  wtedy formę bez licencji, zamiast wyprowadzić zdanie ze słowa, którego ten
    #  projekt się wyrzekł.
    forma = analyse("soba")[0]
    assert w_słownictwie(forma, Słownictwo(pomijane=frozenset({"soba"}))).readings == ()
