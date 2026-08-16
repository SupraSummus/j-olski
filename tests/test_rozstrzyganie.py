"""Te własności warstwy rozstrzygającej, na których stoi jej prawo do istnienia.

Warstwa jest zalążkiem i większość tego, co mówi, mówi tabelą przeliczaną z banku
drzew, której nikt tu nie pilnuje. Trzy rzeczy są inne, bo bez nich zalążek jest
nie tyle niedokończony, co szkodliwy: że milczy, kiedy nie ma na czym stanąć, że
wskazanie przychodzi z liczbami, i że werdykt zostaje nietknięty.

Czwarta jest o kolejności świadków, bo na niej stoi obietnica z docstringa
``olski/rozstrzyganie.py``: dowód o tym tekście bije dowód o cudzym korpusie,
a nie odwrotnie.

Świadek kontekstowy ma tu własne trzy, bo jego dowodem jest sąsiedztwo, a
sąsiedztwo da się źle wyznaczyć na trzy sposoby naraz: wziąć zdanie zza granicy
akapitu, wziąć zdanie stojące dalej, albo wziąć napis zamiast lematu.

Świadka każdy test buduje sam, z licznika wypisanego na miejscu, zamiast czytać
``olski/skłonności.txt``. Plik ten jest generowany, więc test na nim oparty
pilnowałby banku drzew, a nie warstwy, i milkłby razem z nim. Ostatni test bierze
świadków domyślnych, bo sprawdza samo polecenie, i sprawdza wtedy zdanie, którego
tabela wypisać nie umie: powód świadka kontekstowego cytuje akapit.
"""

import pytest

pytest.importorskip("morfeusz2")

import olski.check
from olski.parse import Przyłączenie
from olski.rozstrzyganie import (
    PUSTE,
    Powtórzenie,
    Rozstrzygnięcie,
    Skłonność,
    Sąsiedztwo,
    rozstrzygnij,
    sąsiedztwa,
)
from olski.subset import check

#: Przyłączenie, jakie werdykt wydaje nad ``Daj przepis na faworki.``
FAWORKI = Przyłączenie(modyfikator="na faworki", gospodarze=("Daj", "przepis"))

#: Licznik, przy którym świadek odpowiada: cztery wystąpienia, wszystkie w jedną stronę.
JEDNOZNACZNY = {("na", "noun", "przepis"): (4, 4)}


@pytest.mark.parametrize(
    ("licznik", "dlaczego"),
    [
        ({}, "bez tabeli, czyli po świeżej instalacji"),
        ({("na", "noun", "przepis"): (1, 1)}, "poniżej progu wsparcia"),
        ({("na", "noun", "przepis"): (5, 10)}, "gdy bank drzew przyłącza i tak, i tak"),
    ],
    ids=["bez tabeli", "poniżej wsparcia", "bez przewagi"],
)
def test_świadek_milczy_zamiast_zgadywać(licznik: dict, dlaczego: str):
    """Milczenie jest odpowiedzią domyślną, więc każdy jego powód działa osobno."""
    assert rozstrzygnij([FAWORKI], [Skłonność(licznik=licznik)]) == [FAWORKI], dlaczego


def test_wskazanie_przychodzi_z_liczbami_które_je_wydały():
    """Wskazanie bez powodu nie da się sprawdzić bez zaglądania do tabeli."""
    (odpowiedź,) = rozstrzygnij([FAWORKI], [Skłonność(licznik=JEDNOZNACZNY)])
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == "przepis"
    assert "4 z 4" in odpowiedź.powód


def test_odpowiedź_niesie_imię_świadka_który_ją_wydał():
    """Podpisuje ją warstwa, więc świadek nie ma jak podpisać się cudzym imieniem."""
    (odpowiedź,) = rozstrzygnij([FAWORKI], [Skłonność(licznik=JEDNOZNACZNY, nazwa="inny")])
    assert odpowiedź.świadek == "inny"


def test_pierwszy_świadek_z_odpowiedzią_wygrywa_z_dalszymi():
    """Kolejność jest kolejnością rodzaju dowodu, więc musi być kolejnością, a nie zbiorem."""

    class Rama:
        nazwa = "rama"

        def __call__(self, przyłączenie, sąsiedztwo):
            return Rozstrzygnięcie(przyłączenie.modyfikator, "Daj", "bo tak")

    (odpowiedź,) = rozstrzygnij([FAWORKI], [Rama(), Skłonność(licznik=JEDNOZNACZNY)])
    assert (odpowiedź.świadek, odpowiedź.gospodarz) == ("rama", "Daj")


def test_warstwa_nie_rusza_werdyktu():
    """Zdanie rozstrzygnięte przez warstwę zostaje dla olskiego wieloznaczne.

    To jest cała różnica między tą warstwą a rankingiem wstawionym w werdykt,
    i jest to różnica, którą ``docs/disambiguation.md`` wywodzi z pomiaru.
    """
    (werdykt,) = check("Daj przepis na faworki.")
    przed = werdykt.status, werdykt.result.ile, werdykt.explain()
    odpowiedzi = rozstrzygnij(werdykt.result.przyłączenia, [Skłonność(licznik=JEDNOZNACZNY)])
    assert any(isinstance(o, Rozstrzygnięcie) for o in odpowiedzi), "świadek nic nie powiedział"
    assert (werdykt.status, werdykt.result.ile, werdykt.explain()) == przed
    assert werdykt.status == "ambiguous"


#: Przyłączenie, jakie werdykt wydaje nad ``Widzę człowieka z lornetką.``
LORNETKA = Przyłączenie(modyfikator="z lornetką", gospodarze=("Widzę", "człowieka"))


@pytest.mark.parametrize(
    ("zdanie", "gospodarz"),
    [
        ("W tłumie stał człowiek z lornetką.", "człowieka"),
        #  Ta sama droga wskazuje czasownik, bo świadek pyta, co stało przed
        #  frazą, a nie czy jest to rzeczownik.
        ("Widziałem z lornetką ptaki.", "Widzę"),
    ],
    ids=["gospodarz rzeczownikowy", "gospodarz czasownikowy"],
)
def test_powtórzona_fraza_wskazuje_tego_gospodarza_przy_którym_już_stała(zdanie, gospodarz):
    """Cały dowód tego świadka: autor postawił tę frazę przy tym gospodarzu wyżej."""
    (odpowiedź,) = rozstrzygnij([LORNETKA], [Powtórzenie()], Sąsiedztwo((zdanie,)))
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == gospodarz
    assert zdanie in odpowiedź.powód


def test_fraza_dopasowuje_się_lematem_a_nie_napisem():
    """``z lornetkami`` i ``z lornetką`` są tą samą frazą o tej samej rzeczy."""
    sąsiedztwo = Sąsiedztwo(("Stali tam ludzie z lornetkami.",))
    przyłączenie = Przyłączenie(modyfikator="z lornetką", gospodarze=("Widzę", "ludzi"))
    (odpowiedź,) = rozstrzygnij([przyłączenie], [Powtórzenie()], sąsiedztwo)
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == "ludzi"


@pytest.mark.parametrize(
    ("sąsiedztwo", "dlaczego"),
    [
        (PUSTE, "zdanie postawione samo, czyli olski-check -c"),
        (Sąsiedztwo(("Mam lornetkę.",)), "rzecz wprowadzona, ale nie przy gospodarzu"),
        (Sąsiedztwo(("Widzę z lornetką człowieka z lornetką.",)), "stała przy obu gospodarzach"),
    ],
    ids=["bez sąsiedztwa", "bez powtórzenia frazy", "przy obu gospodarzach"],
)
def test_świadek_kontekstowy_milczy_zamiast_zgadywać(sąsiedztwo: Sąsiedztwo, dlaczego: str):
    """Milczenie jest odpowiedzią domyślną także tutaj, a powodów ma trzy.

    Środkowy jest tym, którego łatwo nie zauważyć: rzecz raz wymieniona nie
    przestaje opisywać rzeczownika, więc samo jej wprowadzenie dowodem nie jest.
    """
    assert rozstrzygnij([LORNETKA], [Powtórzenie()], sąsiedztwo) == [LORNETKA], dlaczego


def test_sąsiedztwem_są_zdania_wcześniejsze_i_tylko_z_tego_akapitu():
    """Akapit jest granicą, a czytelnik idzie do przodu, więc wstecz i nie dalej."""
    tekst = "Pierwsze zdanie. Drugie zdanie.\n\nTrzecie zdanie."
    assert [s.zdania for s in sąsiedztwa(tekst)] == [
        (),
        ("Pierwsze zdanie.",),
        (),
    ]


def test_powtórzenie_bije_skłonność_przeciwnego_zdania():
    """Dowód o tym tekście bije dowód o cudzym korpusie, więc kolejność jest ta.

    Tabela wskazuje tu czasownik, a akapit rzeczownik, i o to w tej parze chodzi:
    świadek dopisany po ``Skłonność`` nie odezwałby się nigdy tam, gdzie tabela
    ma parę policzoną.
    """
    tabela = Skłonność(licznik={("z", "clause", "widzieć"): (4, 4)})
    sąsiedztwo = Sąsiedztwo(("W tłumie stał człowiek z lornetką.",))
    (odpowiedź,) = rozstrzygnij([LORNETKA], [Powtórzenie(), tabela], sąsiedztwo)
    assert (odpowiedź.świadek, odpowiedź.gospodarz) == ("powtórzenie", "człowieka")


def test_polecenie_daje_świadkowi_sąsiedztwo_tego_zdania(capsys):
    """Sąsiedztwo liczy się nad tekstem, a wchodzi do świadka po zdaniu.

    Testy wyżej wołają warstwę wprost, więc żaden z nich nie zauważyłby
    pomyłki o jedno zdanie ani sąsiedztwa pustego podanego wszędzie: obie
    powstają dopiero tam, gdzie polecenie idzie po dokumencie.
    """
    olski.check.main(
        ["--rozstrzygaj", "-c", "W tłumie stał człowiek z lornetką. Widzę człowieka z lornetką."]
    )
    wypisane = capsys.readouterr().out
    assert '? „z lornetką” → „człowieka”: „z lornetką” stało już przy „człowiek”' in wypisane
    assert wypisane.count("stało już przy") == 1, "pierwsze zdanie nie ma przed sobą niczego"
