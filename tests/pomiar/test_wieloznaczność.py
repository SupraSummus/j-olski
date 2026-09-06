"""Co liczy się jako zdanie wieloznaczne w samej polszczyźnie.

Pomiar odpowiada pytaniu, którego werdykt nad zdaniem nie umie zadać sam, a
odpowiada liczbą, więc bronić trzeba tego, co do tej liczby wchodzi, a nie tego,
że wchodzi cokolwiek.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.wieloznaczność import PRZYŁĄCZENIE, SYNKRETYZM, measure, miejsca


def klasy(zdanie):
    return {miejsce.klasa for miejsce in miejsca(zdanie)}


def przyłączenia(zdanie, przyimek):
    return [m for m in miejsca(zdanie) if m.klasa == PRZYŁĄCZENIE and m.formy == (przyimek,)]


def test_zdanie_o_które_pytanie_stoi_niesie_synkretyzm():
    #  docs/open-questions.md cytuje to zdanie jako to, na którym własność
    #  jednoznaczności się rozchodzi: notacja jest nieodmienna, a „wywód” ma
    #  biernik równy mianownikowi, więc SVO i OVS stoją oba.
    assert SYNKRETYZM in klasy("Cały wywód prowadzi docs/linter.md.")


def test_cząstka_się_rozstrzyga_o_bierniku_a_nie_sam_lemat():
    #  Para różni się jedną cząstką: „kończyć” bierze dopełnienie w bierniku, a
    #  „kończyć się” go nie bierze, więc pierwsze zdanie czyta się i jako SVO, i
    #  jako OVS, a drugie ma podmiot jeden. Leksykon zwrotny sklejony z gołym w
    #  jeden zbiór odbiera tę klasę obu naraz.
    assert SYNKRETYZM in klasy("Szkolenie kończy wdrożenie.")
    assert SYNKRETYZM not in klasy("Wdrożenie kończy się szkolenie.")


def test_zgoda_liczby_zdejmuje_grupę_która_podmiotem_być_nie_może():
    #  Obie grupy są obojętne na przypadek, a zdanie ma jedno czytanie: orzeczenie
    #  stoi w pojedynczej, więc „ustawienia” podmiotem nie stanie.
    assert SYNKRETYZM not in klasy("Program zapisuje ustawienia w pliku.")


def test_synkretyzm_rozdzielony_na_wpisy_słownika_liczy_się_tak_samo():
    #  „mysz” wychodzi z Morfeusza jako subst:sg:nom:f i subst:sg:acc:f dwoma
    #  wpisami, a „ogon” jako jedno subst:sg:nom.acc:m3, więc warunek pytany o
    #  czytanie mijał tę parę, a pytany o segment jej nie mija.
    assert SYNKRETYZM in klasy("Mysz goni ogon.")


def test_dwa_zdania_składowe_nie_dają_pary_do_wyboru():
    #  „Wdrożenie” i „kurs” są obojętne na przypadek, a stoją przy dwóch różnych
    #  orzeczeniach, więc o wyborze między SVO a OVS to zdanie nie mówi nic.
    #  Para jest ta sama w obu zdaniach i rozstrzyga o niej sam przecinek,
    #  bo bez niego oba rzeczowniki stają przy jednym „kończy”.
    assert SYNKRETYZM not in klasy("Wdrożenie kończy administratora, a kurs trwa.")
    assert SYNKRETYZM in klasy("Wdrożenie kończy administratora i kurs trwa.")


def test_pozycja_dwuznaczna_żąda_rzeczownika_przed_wyrażeniem_i_czasownika():
    #  Populacja jest ta sama, którą liczy harness/attachment.py: bez rzeczownika
    #  przed wyrażeniem nie ma drugiego przyłączenia, a bez czasownika przed nim
    #  nie ma pierwszego. Zdanie z wysuniętym wyrażeniem jest przy tym tym
    #  wyjściem, które docs/subset.md zostawia autorowi.
    assert PRZYŁĄCZENIE in klasy("Program zapisuje ustawienia w pliku.")
    assert PRZYŁĄCZENIE not in klasy("Pod względem smaku chałka przewyższa zwykłą bułkę.")
    assert PRZYŁĄCZENIE not in klasy("Ustawienia w pliku są ważne.")


def test_gospodarzem_imiennym_jest_cała_grupa_a_nie_jej_ogon():
    #  W łańcuchu dopełniaczowym formą tuż przed przyimkiem jest ogon grupy, a
    #  fraza dochodzi do jej głowy: docs/rozstrzyganie.md czyta „z systemem RIT”
    #  jako przydawkę wymiany, nie danych. Świadek kontekstowy schodzi tą samą
    #  drogą (_łańcuch w olski/rozstrzyganie.py), więc gospodarz wzięty z
    #  jednej formy kazałby mu wskazywać ogon i mylić się na tym łańcuchu.
    (miejsce,) = przyłączenia("Wpływa to na sposób wymiany danych z systemem RIT.", "z")
    assert miejsce.gospodarze[:3] == ("danych", "wymiany", "sposób")


def test_forma_bez_czytania_imiennego_zamyka_grupę():
    #  Bez tego warunku grupą jest cały prefiks zdania, czyli reguła, którą
    #  harness/powtórzenie.py mierzy jako wariant i którą warstwa odrzuca: spójnik
    #  kończy grupę imienną, a za nim zaczyna się opis czegoś innego.
    (miejsce,) = przyłączenia("Opisano nadawanie i funkcjonowanie uprawnień do faktur.", "do")
    assert miejsce.gospodarze[:2] == ("uprawnień", "funkcjonowanie")
    assert "nadawanie" not in miejsce.gospodarze


def test_fragment_nie_wchodzi_do_mianownika():
    #  Kryterium wyjścia liczy zdania, a nagłówek i pozycja listy zdaniami nie są,
    #  więc policzone tutaj mierzyłyby ekstrakcję zamiast rejestru.
    tekst = "Przyłączanie wyrażeń przyimkowych\n\nProgram zapisuje ustawienia w pliku.\n"
    report = measure([tekst])
    assert (report.zdania, report.fragmenty) == (1, 1)
