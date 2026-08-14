from collections import Counter
from dataclasses import fields, is_dataclass
from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

from olski.walencja import bierze_bezokolicznik, bierze_biernik, bierze_zdanie
from skład import Kontekst, Opowieść, kompiluj
from skład.makieta import (
    CECHY,
    CECHY_OSÓB,
    CZYNY_RUCHU,
    CZYNY_STANU,
    CZYNY_Z_BEZOKOLICZNIKIEM,
    CZYNY_Z_BIERNIKIEM,
    CZYNY_ZE_ZDANIEM,
    MIEJSCA,
    OKOLICZNOŚCI_CZYNNE,
    OKOLICZNOŚCI_RUCHU,
    OSOBY,
    OSÓB,
    PORY,
    PORY_W_MIEJSCOWNIKU,
    PRZYSŁÓWKI,
    RZECZY,
    losuj,
)
from skład.morfologia import odmień, rodzaj_rzeczownika
from skład.opowieść import Postać
from skład.przegląd import przejrzyj
from skład.przyimki import przypadek
from skład.składnia import Okolicznik, Przysłówek, Rzecz, byt, zdarzenie

ROOT = Path(__file__).resolve().parent.parent

#: Wszystkie rzeczowniki inwentarza, bo każdy z nich staje w każdym przypadku,
#: który losowanie umie postawić.
RZECZOWNIKI = (*OSOBY, *RZECZY, *MIEJSCA, *PORY, *PORY_W_MIEJSCOWNIKU)

#: Przypadki, w których losowanie stawia grupę imienną,
#: i liczby, w których ją stawia.
PRZYPADKI = ("nom", "gen", "acc", "inst", "loc")
LICZBY = ("sg", "pl")

#: Rodzaje, które inwentarz niesie, czyli te, których czasownik może zażądać
#: od formy przeszłej. Liczba mnoga w tym żądaniu nie stoi,
#: bo podmiotem jest tu zawsze jedna postać.
RODZAJE = ("f", "m1", "m3", "n")

#: Tekst, który wychodzi z tego jednego ziarna, znak w znak.
#: Trzymany tak samo jak legenda o bazyliszku w ``tests/test_opowieść.py``
#: i z tego samego powodu: napis jest tu jedyną rzeczą, którą da się porównać,
#: a rusza go i zmiana inwentarza, i zmiana kształtu zdania, i zmiana kolejności
#: losowań, czyli wszystko, co rozstrzyga, jak ta makieta czyta się jako proza.
MAKIETA = """\
Czeladnik zapłakał w wąskiej piwnicy. \
Próbował wrócić na ulicę. \
Sukno znalazło bochenki i nie stało w nocy. \
Czeladnik zasnął. \
Ponieważ córka zeszła od młodej wdowy, nie zamknął zegara. \
Sukno podniosło beczki i dużą skrzynię.

Zanim kucharka zeszła z podwórza, czeladnik schował ciężki zegar. \
Klucz schował okno. \
Kucharka zasnęła pod krzywą kamienicą sąsiadki. \
Klucz nie otworzył lustra i nie zasnął w ogrodach. \
Zasłonił okno.

Zegar wziął skrzynię, którą wdowa znalazła. \
Czeladnik był cichym chłopcem. \
Wyszedł. \
Szal zamknął skrzynię, którą zegar rozbił. \
Zegar przyniósł klucze i krzywy dzban."""

#: Kategorie, które niesie zapis z ``skład/składnia.py`` wraz z ``Postać`` nad nim,
#: czyli wszystko, z czego wolno zbudować drzewo.
KATEGORIE = {
    "Byt",
    "Ciąg",
    "Czyj",
    "Jaki",
    "Jest",
    "Koordynacja",
    "Okolicznik",
    "Opis",
    "Postać",
    "Przysłówek",
    "Robi",
    "Rzecz",
    "Treść",
    "Wyróżnienie",
}


def test_makieta_z_jednego_ziarna_stoi_znak_w_znak():
    assert losuj(1871, akapitów=3).kompiluj() == MAKIETA


def test_readme_pokazuje_akapit_który_z_tego_ziarna_naprawdę_wychodzi():
    """Wydruk w README jest drugą kopią tego tekstu, więc trzyma ją test, a nie oko.

    Kopia ta rusza się z każdą zmianą inwentarza i z każdą zmianą kształtu zdania,
    a README o tym nie wie, bo stoi w nim napis, a nie polecenie do przebiegnięcia.
    """
    akapit = losuj(1871, akapitów=1).kompiluj()
    assert akapit in (ROOT / "README.md").read_text(encoding="utf-8")


def test_to_samo_ziarno_daje_ten_sam_tekst():
    """Losowanie ma własne źródło, a nie globalne, więc tekst wraca powtarzalny.

    Bez tego makieta zmieniałaby się przy każdym wywołaniu,
    a ziarno wypisane przez ``main`` nie prowadziłoby z powrotem do niczego.
    """
    assert losuj(7).kompiluj() == losuj(7).kompiluj()
    assert losuj(7).kompiluj() != losuj(8).kompiluj()


@pytest.mark.parametrize("lemat", RZECZOWNIKI)
def test_każdy_rzeczownik_inwentarza_ma_rodzaj_i_każdą_potrzebną_formę(lemat):
    """Świadkiem inwentarza jest tu SGJP, a nie oko tego, kto go pisał.

    Rodzaju żąda zgodność z czasownikiem i z przymiotnikiem,
    a form żąda pozycja, w której grupa imienna stanie,
    więc lemat bez którejkolwiek z nich zgłosiłby ``BrakFormy`` dopiero na tekście,
    i to nie na każdym, a na tym, w którym akurat wypadł.
    Leksem, o który autor nie rozstrzygnął, zgłasza się tu tym samym pomiarem:
    ``odmień`` odpowiada wtedy ``WieleLeksemów``.
    """
    assert rodzaj_rzeczownika(lemat) in RODZAJE
    for liczba in LICZBY:
        for przypadek_ in PRZYPADKI:
            assert odmień(lemat, "subst", case=przypadek_, number=liczba)


@pytest.mark.parametrize("lemat", (*CECHY, *CECHY_OSÓB))
def test_każdy_przymiotnik_inwentarza_stoi_w_każdym_rodzaju(lemat):
    for rodzaj in RODZAJE:
        assert odmień(lemat, "adj", case="nom", number="sg", gender=rodzaj, degree="pos")


@pytest.mark.parametrize("lemat", PRZYSŁÓWKI)
def test_każdy_przysłówek_inwentarza_ma_formę_przysłówkową(lemat):
    """Partykuła tu nie przejdzie, a wygląda w tabeli tak samo jak przysłówek.

    ``Przysłówek`` w ``skład/składnia.py`` żąda znakowania ``adv``,
    więc `znowu`, które SGJP zna jako partykułę, zgłosiłoby ``BrakFormy``.
    """
    assert Przysłówek(lemat).linearyzuj().napis


@pytest.mark.parametrize("lemat", (*CZYNY_RUCHU, *CZYNY_STANU, *CZYNY_Z_BIERNIKIEM))
def test_każdy_czasownik_inwentarza_ma_formę_przeszłą_w_każdym_rodzaju(lemat):
    for rodzaj in RODZAJE:
        assert odmień(lemat, "praet", number="sg", gender=rodzaj)


@pytest.mark.parametrize("lemat", CZYNY_Z_BIERNIKIEM)
def test_czasownik_z_tabeli_biernikowej_biernik_bierze(lemat):
    """Ramy pilnuje leksykon, a nie tabela, i to on jest tu świadkiem.

    ``Robi`` w ``skład/składnia.py`` zgłasza ``PozaRamą``, gdy drzewo żąda pozycji,
    której lemat nie ma, więc wpis chybiony zabiera losowaniu zdanie,
    zamiast wypuścić tekst, którego polszczyzna nie ma.
    """
    assert bierze_biernik(lemat)


@pytest.mark.parametrize("lemat", CZYNY_Z_BEZOKOLICZNIKIEM)
def test_czasownik_z_tabeli_bezokolicznikowej_bezokolicznik_bierze(lemat):
    assert bierze_bezokolicznik(lemat)
    assert odmień(lemat, "inf")


@pytest.mark.parametrize("lemat", CZYNY_ZE_ZDANIEM)
def test_czasownik_z_tabeli_zdaniowej_zdanie_podrzędne_bierze(lemat):
    assert bierze_zdanie(lemat)


#: Wszystkie wiersze okoliczności, bez powtórzeń, bo czas wchodzi do obu tabel.
WIERSZE = tuple(dict.fromkeys((*OKOLICZNOŚCI_RUCHU, *OKOLICZNOŚCI_CZYNNE)))


@pytest.mark.parametrize("wiersz", WIERSZE)
def test_każda_okoliczność_inwentarza_stoi_w_leksykonie_i_wypisuje_się(wiersz):
    """Wiersz tabeli mówi dwie rzeczy naraz i obie mają tu świadka.

    Para słowa z relacją jest zdaniem o polszczyźnie i o niej rozstrzyga
    ``skład/przyimki.py``, więc para, której tam nie ma, zgłasza ``PozaRamą``.
    Dobór rzeczowników jest zdaniem o tej tabeli i nie ma świadka w słowniku,
    a sprawdzić da się o nim tyle, że każdy z nich staje w przypadku,
    którego ten przyimek żąda.
    """
    słowo, relacja, rzeczowniki = wiersz
    assert przypadek(słowo, relacja) is not None
    for lemat in rzeczowniki:
        assert Okolicznik(słowo, relacja, byt(Rzecz(lemat))).linearyzuj().napis


def test_osób_każdego_rodzaju_jest_więcej_niż_obsada_zabiera():
    """Orzecznik szuka osoby tego rodzaju co podmiot i spoza obsady, więc musi mieć z czego.

    Tabela, w której jednego rodzaju jest tyle, ilu ludzi bierze akapit,
    zostawiłaby ten wybór pusty i zgłosiłaby to dopiero na tym losowaniu,
    w którym obsada wybrała wszystkich, a nie na każdym.
    """
    wedle_rodzaju = Counter(rodzaj_rzeczownika(lemat) for lemat in OSOBY)
    assert set(wedle_rodzaju) == {"f", "m1"}
    assert min(wedle_rodzaju.values()) > max(OSÓB)


@pytest.mark.parametrize("ziarno", range(24))
def test_żadna_makieta_nie_niesie_kolizji_ról(ziarno):
    """To jest cała obrona tego modułu i dlatego stoi nad dwudziestoma czterema ziarnami.

    Zdanie, którego role czytają się na dwa sposoby, wypada z losowania
    i wraca do puli, więc nad wyjściem nie ma ani jednego zgłoszenia.
    Liczone jest to po kontekstach akapitu, a nie po zdaniach stojących osobno,
    i tam też odsiew pyta: podmiot opuszczony żadnej swojej formy nie pokazuje,
    więc zdanie odsiane samo bywa dwojakie dopiero za sąsiadem.
    """
    opowieść = losuj(ziarno)
    assert [
        kolizja
        for akapit in opowieść.akapity
        for zdanie, kontekst in akapit.konteksty(Opowieść.CZAS)
        for kolizja in przejrzyj(zdanie, kontekst)
    ] == []


def test_inwentarz_umie_zdanie_którego_role_czytają_się_dwojako():
    """Odsianie nie jest tu martwe i to zdanie mówi, przed czym ono broni.

    Rzecz podmiotem stojąca kolizję robi, bo biernik rzeczy nieżywotnej
    równa się mianownikowi, a czas przeszły rodzaju tych dwóch nie rozdziela.
    Osoba jej nie robi i dlatego pętla losowania się domyka.
    """
    kontekst = Kontekst(czas=Opowieść.CZAS)
    assert "zegar" in RZECZY and "kufer" in RZECZY and "zasłonić" in CZYNY_Z_BIERNIKIEM
    dwojakie = zdarzenie(Rzecz("zegar"), "zasłonić", Rzecz("kufer"))
    assert kompiluj(dwojakie, kontekst) == "Zegar zasłonił kufer."
    assert [kolizja.formy for kolizja in przejrzyj(dwojakie, kontekst)] == [("zegar", "kufer")]

    assert "czeladnik" in OSOBY
    jednoznaczne = zdarzenie(Rzecz("czeladnik"), "zasłonić", Rzecz("kufer"))
    assert przejrzyj(jednoznaczne, kontekst) == []


def test_makieta_wystawia_każdą_kategorię_zapisu():
    """Makieta pokazuje, co ten zapis umie, więc kategoria pominięta jest tu usterką.

    Tak wypadł dopełniacz: `klucz kucharki` nie wychodził z żadnego kształtu,
    choć `Czyj` w składni stoi od początku, a po samym tekście tego nie widać.
    Kategoria dopisana do składni należy przez to i tutaj,
    i ten test jest miejscem, w którym ten dług się zgłasza.
    """
    widziane = {
        kategoria
        for ziarno in range(24)
        for akapit in losuj(ziarno).akapity
        for zdanie in akapit.zdania
        for kategoria in _kategorie(zdanie)
    }
    assert widziane == KATEGORIE


def _kategorie(węzeł) -> set[str]:
    """Nazwy kategorii w tym drzewie, zebrane po polach dataklas i po krotkach.

    Schodzi po polach, a nie po nazwach, których losowanie użyło,
    bo drzewo nie niesie tego, którym kształtem powstało,
    a wpisanie tego do drzewa dołożyłoby składni pole, którego ona nie potrzebuje.
    """
    if isinstance(węzeł, tuple):
        return {kategoria for człon in węzeł for kategoria in _kategorie(człon)}
    dzieci = (
        [getattr(węzeł, pole.name) for pole in fields(węzeł)]
        if is_dataclass(węzeł)
        else [węzeł.kto]
        if isinstance(węzeł, Postać)
        else []
    )
    pod = (
        kategoria
        for dziecko in dzieci
        if dziecko is not None and not isinstance(dziecko, (str, bool))
        for kategoria in _kategorie(dziecko)
    )
    return {type(węzeł).__name__, *pod}


def test_akapit_opuszcza_podmiot_choć_zdania_powstają_osobno():
    """Obsada jest tu treścią, a nie oszczędnością na losowaniach.

    Podmiot opuszcza się tylko wtedy, gdy dwa zdania obok siebie mówią
    o jednej i tej samej rzeczy, a tożsamość niesie ``Postać``, nie lemat,
    więc losowanie budujące postać osobno dla każdego zdania
    wypuściłoby tekst, w którym każde zdanie powtarza swój podmiot.
    """
    pominięte = [
        kontekst.pomijany
        for ziarno in range(8)
        for akapit in losuj(ziarno).akapity
        for _zdanie, kontekst in akapit.konteksty(Opowieść.CZAS)
        if kontekst.pomijany is not None
    ]
    assert pominięte
