import pytest

pytest.importorskip("morfeusz2")

import skład.składnia as składnia
from olski.subset import WALENCJA, check
from olski.walencja import bierze_biernik
from skład import BrakFormy, Byt, Czyj, Jaki, PozaRamą, Rzecz, byt, kompiluj, odmień
from skład.składnia import Jest, Robi
from skład.słownik import A, R, V, jest


def test_zgodność_jest_liczona_a_nie_żądana_od_autora():
    """Przymiotnik dostaje rodzaj z rzeczownika, a przypadek z pozycji w zdaniu.

    Trzy rodzaje naraz, bo pomyłką, którą da się tu zrobić, jest wzięcie rodzaju
    z jednego miejsca dla wszystkich: przy jednym rzeczowniku taki błąd nie widać.
    """
    assert Jaki("dobry", Rzecz("kod")).linearyzuj("nom", "sg") == "dobry kod"
    assert Jaki("dobry", Rzecz("dokumentacja")).linearyzuj("nom", "sg") == "dobra dokumentacja"
    assert Jaki("dobry", Rzecz("narzędzie")).linearyzuj("nom", "sg") == "dobre narzędzie"


def test_ta_sama_rzecz_odmienia_się_wedle_pozycji_w_zdaniu():
    """Przypadek przychodzi od konstruktora zdania, a nie od autora grupy imiennej."""
    tekst = Jaki("polski", Rzecz("tekst"))
    assert Robi(byt(Rzecz("linter")), "sprawdzać", byt(tekst)).linearyzuj() == (
        "linter sprawdza polski tekst"
    )
    assert Jest(byt(tekst), byt(Rzecz("wejście"))).linearyzuj() == (
        "wejściem jest polski tekst"
    )


def test_kierunek_relacji_dopełniaczowej_jest_kształtem_drzewa():
    """Dwa drzewa, dwa zdania, znaczenia przeciwne.

    Nad workiem lematów te dwa zdania są nie do rozróżnienia, i to jest powód,
    dla którego ta kategoria stoi w drzewie zamiast w kolejności słów.
    """
    parser, podzbiór = Rzecz("parser"), Rzecz("podzbiór")
    assert kompiluj(Jest(byt(parser / podzbiór), byt(Rzecz("cel")))) == (
        "Celem jest parser podzbioru."
    )
    assert kompiluj(Jest(byt(podzbiór / parser), byt(Rzecz("cel")))) == (
        "Celem jest podzbiór parsera."
    )


def test_określenie_niesie_własną_liczbę_niezależnie_od_głowy():
    """Bez tego parser podzbiorów nie ma jak powstać, bo liczba głowy zjada obie."""
    parser = Rzecz("parser")
    assert Czyj(parser, Byt(Rzecz("podzbiór"), "pl")).linearyzuj("nom", "sg") == (
        "parser podzbiorów"
    )
    assert Czyj(parser, Byt(Rzecz("podzbiór"))).linearyzuj("nom", "pl") == (
        "parsery podzbioru"
    )


def test_forma_której_słownik_nie_ma_zgłasza_się_zamiast_zostać_zgadnięta():
    """Kompilator, który w tym miejscu zgaduje, wypuszcza polszczyznę nieistniejącą."""
    with pytest.raises(BrakFormy):
        odmień("podzbiór", "subst", case="nom", number="sg", gender="f")
    with pytest.raises(BrakFormy):
        odmień("zzznieistniejący", "subst", case="nom", number="sg")


def test_czasownik_któremu_leksykon_odmawia_biernika_nie_wypuszcza_dopełnienia():
    """Zdanie z roadmapy: `Linter pomaga dobry kod.` nie ma wyjść z tego drzewa.

    Zgłoszenie pada przy budowaniu drzewa, a nie przy linearyzacji,
    więc test niczego nie linearyzuje.
    """
    with pytest.raises(PozaRamą):
        V.pomagać(R.linter, A.dobry * R.kod)


def test_kopuli_biernik_odmówiony_jest_po_obu_stronach_tak_samo():
    """Kopula jest lematem, na którym kopia leksykonu rozjechałaby się najpierw.

    Czemu akurat ona, mówi ``olski/walencja.py``;
    tutaj stoi zdanie, które by z tego rozjazdu wyszło.
    """
    with pytest.raises(PozaRamą):
        V.być(R.program, ~R.ustawienie)


def test_biernika_odmawiają_oba_kierunki_tym_samym_lematom():
    """Jedno źródło znaczy tyle, że nie ma dwóch odpowiedzi na jedno pytanie.

    Odmowy parsera liczone są z ram, a nie wypisane obok nich,
    żeby rama dopisana do gramatyki weszła do tego porównania sama.
    """
    odmawia_parser = {
        lemat
        for rama, lematy in WALENCJA.items()
        if "acc" not in rama.split(".")
        for lemat in lematy.split("|")
    }
    assert {lemat for lemat in odmawia_parser if bierze_biernik(lemat)} == set()
    #  Odmowa postawiona każdemu lematowi przeszłaby powyższe, więc świadek
    #  z drugiej strony: `zapisywać` bierze ramę domyślną po obu.
    assert "zapisywać" not in odmawia_parser
    assert bierze_biernik("zapisywać")


def test_przestrzenie_nazw_niczego_w_składni_nie_zmieniają():
    """Cukier jest zdejmowalny albo nim nie jest, a docstring tego nie rozstrzyga.

    Warstwa dopisująca operatory klasom składni zmieniałaby zachowanie modułu
    przez sam import, więc to samo drzewo znaczyłoby co innego zależnie od tego,
    co jeszcze zostało zaimportowane.
    """
    assert składnia.Rzecz.__truediv__ is składnia.Nominalne.__truediv__
    assert składnia.Rzecz.__invert__ is składnia.Nominalne.__invert__
    assert R.parser / R.podzbiór == Czyj(Rzecz("parser"), byt(Rzecz("podzbiór")))
    assert ~R.ustawienie == Byt(Rzecz("ustawienie"), "pl")
    assert A.dobry * R.kod == Jaki("dobry", Rzecz("kod"))


def test_dwa_przymiotniki_zagnieżdżają_się_w_kolejności_zapisu():
    """Mnożenie wiąże w lewo, więc bez klasy pośredniej wychodzi kolejność odwrotna."""
    assert A.zwykły * A.polski * R.tekst == Jaki("zwykły", Jaki("polski", Rzecz("tekst")))


@pytest.mark.parametrize(
    "drzewo",
    [
        jest(A.zwykły * A.polski * R.tekst, R.wejście),
        jest(R.parser / R.podzbiór, R.cel),
        jest(R.parser / ~R.podzbiór, R.cel),
        V.zapisywać(R.program, ~R.ustawienie),
        V.sprawdzać(R.linter, ~(A.polski * R.tekst)),
    ],
)
def test_to_co_skład_wypuszcza_czyta_się_w_olskim_raz(drzewo):
    """Sprzężenie obu torów jest tu całe i jest jednostronne.

    Skład olskiego nie potrzebuje, bo zgodność liczy, zamiast ją sprawdzać, więc
    ten check jest świadkiem, a nie zależnością: nad zdaniem, którego gramatyka
    nie obejmuje, nie ma czego powiedzieć i wtedy takiego przypadku tu nie ma.
    """
    werdykt = check(kompiluj(drzewo))[0]
    assert werdykt.status == "valid", werdykt.explain()
