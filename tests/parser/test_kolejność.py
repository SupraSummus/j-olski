"""Kolejność czytań stoi na deklaracji, a nie na kolejności dopisań ani na haszach.

Czym ta kolejność jest i po co, mówi
docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie.

Hasze napisów losuje start procesu, więc zbiór postawiony na drodze do wydruku
wypisuje w każdym przebiegu co innego.
Widać to wyłącznie między procesami, bo ziarno jest jedno na proces,
więc pyta o to podproces, i pyta dwa razy.

Dwie własności na końcu należą do sondy, która tę kolejność zestawia z wzorcem
przeczytanym ręką (harness/kolejność.py).
Plik dzieli się po tym, o którą warstwę test pyta, a ona pyta o tę samą.
"""

import os
import random
import subprocess
import sys
from itertools import islice
from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

from harness.kolejność import INNY_KONSTYTUENT, TRAFNA, osądź
from harness.wybory import Wybór
from olski.cennik import (
    CENNIK,
    CZASOWNIK_PRZED_PODMIOTEM,
    OKOLICZNIK,
    OPUSZCZONY_PODMIOT,
    razem,
)
from olski.grammar import Grammar, Głowa, nt, word
from olski.parse import parse
from olski.parse.las import _iloczyn
from olski.rejestr import POZA_REJESTREM, pozycje
from olski.segmentacja import morphology
from olski.subset import build
from olski.werdykt import check
from tests.parser.test_las import SIEDEM_PRZYŁĄCZEŃ

#: Zdania wieloznaczne, każde inną decyzją: przyłączenie wyrażenia przyimkowego,
#: szyk podmiotu i dopełnienia oraz oba naraz. Kolejność czytań rozstrzyga się
#: w każdym z nich gdzie indziej, więc jedno zdanie nie starczy na tę własność.
ZDANIA = [
    "Program zapisuje ustawienia w pliku.",
    "Ustawienia zapisuje program.",
    "Nowy program zapisuje ustawienia użytkownika w pliku.",
]


def _czytania(grammar: Grammar) -> list[list[str]]:
    """Czytania każdego z tych zdań, w kolejności, w jakiej widzi je czytelnik."""
    werdykty = check("\n\n".join(ZDANIA), grammar)
    assert all(werdykt.readings for werdykt in werdykty), "zdanie bez czytań nic tu nie mierzy"
    return [[str(streszczenie) for streszczenie in werdykt.readings] for werdykt in werdykty]


def _potasowana(seed: int) -> Grammar:
    """Te same produkcje dopisane do gramatyki w innej kolejności."""
    wzór = build()
    produkcje = list(wzór.productions)
    random.Random(seed).shuffle(produkcje)
    grammar = Grammar(start=wzór.start, nie_wypuszczane=wzór.nie_wypuszczane)
    for production in produkcje:
        grammar.dopisz(production)
    return grammar


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_kolejność_czytań_nie_zależy_od_kolejności_dopisania_produkcji(seed: int):
    assert _czytania(_potasowana(seed)) == _czytania(build())


def test_produkcja_tańsza_wydaje_swoje_czytanie_wcześniej():
    """Koszt rozstrzyga przed cięciem, więc tańsze ciało wychodzi z lasu pierwsze.

    Gramatyka jest napisana pod tę jedną własność: dwa ciała o córkach tej samej
    rozpiętości zostawiają kosztowi całą decyzję, a nad zdaniem olskiego
    rozstrzygnęłoby ją zwykle cięcie i test nie mierzyłby kosztu.
    """
    kolejność = []
    for lewe, prawe in (((), (OKOLICZNIK,)), ((OKOLICZNIK,), ())):
        grammar = Grammar(start="zdanie")
        grammar.rule("zdanie", [Głowa(nt("lewe"))], koszty=lewe)
        grammar.rule("zdanie", [Głowa(nt("prawe"))], koszty=prawe)
        grammar.rule("lewe", [Głowa(word("subst")), word("interp")])
        grammar.rule("prawe", [Głowa(word("subst")), word("interp")])
        czytania = parse(grammar, morphology("plik.")).readings
        kolejność.append([drzewo.children[0].label for drzewo in czytania])
    assert kolejność == [["lewe", "prawe"], ["prawe", "lewe"]]


def test_iloczyn_wydaje_najtańsze_kombinacje_i_nie_tyka_reszty():
    """Kombinacje idą od najtańszej, a ze strumieni schodzi tylko tyle, ile trzeba.

    Iloczyn kartezjański z biblioteki materializuje swoje wejścia, więc granica
    `MAX_READINGS` przestałaby nad zdaniem wieloznacznym cokolwiek ograniczać.
    Remis rozstrzygają wskaźniki i to jest tu pomyłka prawdopodobna:
    kombinacji o jednym koszcie nie odróżni nic poza kolejnością, bo czytań nie ubywa.
    """
    pobrane = [0, 0]

    def strumień(miejsce: int):
        for numer, koszt in enumerate([0, 100, 200, 300, 400]):
            pobrane[miejsce] = numer + 1
            yield koszt, f"{miejsce}{numer}"

    wydane = list(islice(_iloczyn([strumień(0), strumień(1)]), 3))
    assert wydane == [
        (0, ("00", "10")),
        (100, ("00", "11")),
        (100, ("01", "10")),
    ]
    #  Iloczyn z biblioteki zszedłby po oba strumienie do końca, czyli [5, 5],
    #  a każde drzewo, po które sięga strumień, kosztuje całe swoje poddrzewo.
    assert pobrane == [2, 3]


def test_czytania_wychodzą_od_najtańszego():
    """Suma rachunku nie maleje wzdłuż listy odczytań, bo to ona ją porządkuje.

    Zdanie o siedmiu przyłączeniach płaci od zera do siedmiu okoliczników,
    więc lista porządkowana czymkolwiek innym wychodzi tu nieposortowana.
    Sumę liczymy z rachunku, czyli z tego, co widzi czytelnik pod czytaniem
    (`_wiersz_sumy` w `olski/check.py`): las porządkujący po innej liczbie niż
    ta wypisana byłby dwiema odpowiedziami o jednym czytaniu.
    """
    (werdykt,) = check(SIEDEM_PRZYŁĄCZEŃ)
    sumy = [razem(rachunek) for rachunek in werdykt.rachunki]
    assert len(set(sumy)) > 1, "jedna suma na całe zdanie nie ma czego porządkować"
    assert sumy == sorted(sumy)


def test_koszt_córki_waży_nad_rodzicem():
    """Kolejność rozstrzyga suma po całym drzewie, więc płaci się i za poddrzewo.

    Gramatyka jest napisana pod tę jedną własność: `lewe` i `prawe` mają córki
    tej samej rozpiętości, a ciała `zdania` kosztują tyle samo, więc bez sumy
    rozstrzygałby o kolejności alfabet etykiet i przodem szłoby `lewe`.
    Widać tę różnicę tylko po kolejności: czytań nie ubywa.
    """
    grammar = Grammar(start="zdanie")
    grammar.rule("zdanie", [Głowa(nt("lewe"))])
    grammar.rule("zdanie", [Głowa(nt("prawe"))])
    grammar.rule("lewe", [Głowa(word("subst")), word("interp")], koszty=(OKOLICZNIK,))
    grammar.rule("prawe", [Głowa(word("subst")), word("interp")])
    czytania = parse(grammar, morphology("plik.")).readings
    assert [drzewo.children[0].label for drzewo in czytania] == ["prawe", "lewe"]


def test_każdą_pozycję_cennika_ktoś_płaci():
    """Cennik nie trzyma pozycji, której nie płaci ani produkcja, ani forma.

    Nazwa wpisana do produkcji, a nie do cennika, wywraca budowanie gramatyki
    (`cena` w `olski/cennik.py`), więc pilnowania żąda druga strona:
    pozycja, której nikt nie płaci, zostaje po konstrukcji wycofanej z gramatyki
    i wycenia coś, czego już nie ma.
    """
    płacone = {nazwa for produkcja in build().productions for nazwa in produkcja.koszty}
    #  Kwalifikatory odsyłające, bo pozycji morfologii nie płaci żadna produkcja.
    płacone.update(pozycje(POZA_REJESTREM))
    assert set(CENNIK) == płacone


def test_rachunek_stoi_przy_tym_odczytaniu_które_płaci():
    """Rachunek jest wpisem na odczytanie, a nie jedną odpowiedzią o zdaniu.

    `Program otwierający się psuje.` czyta się na trzy sposoby, a płaci jeden:
    ten, który grupę przed czasownikiem bierze za dopełnienie i każe szukać
    podmiotu w zdaniu obok.
    """
    (werdykt,) = check("Program otwierający się psuje.")
    assert werdykt.rachunki == [(), (), ((OPUSZCZONY_PODMIOT, 1),)]


def test_czytania_różniące_się_przyłączeniem_mają_różne_rachunki():
    """Okolicznik pod wypełnieniami płaci, więc rachunek rozróżnia czytania przyłączeniowe.

    Przyłączenie jest większością wieloznaczności olskiego, a pozycje szyku na
    nim milczą: oba czytania `Program zapisuje ustawienia w pliku.` stoją w szyku,
    który deklaracja im wypisała. Póki to ciało było darmowe, oba rachunki były
    puste i suma nie miała czego porównać
    (docs/disambiguation.md#miara-porównywalna-nad-czytaniami).
    """
    (werdykt,) = check("Program zapisuje ustawienia w pliku.")
    assert werdykt.rachunki == [(), ((OKOLICZNIK, 1),)]


def test_okolicznik_kosztuje_tyle_samo_obok_wypełnienia_co_bez_niego():
    """Cena okolicznika nie zależy od tego, czy czasownik wypełnia przy okazji pozycję ramy.

    Okolicznik stoi pod wypełnieniami w czterech rodzinach ciał i każda wypisuje
    się osobno (`_wypełnienia` w `olski/subset/zdanie.py`), więc cena dopisana do
    jednej z nich orzekałaby o zdaniu rzecz, której nikt nie zadeklarował:
    `deskami` płaciłoby, a `dotąd` nie, choć oba dochodzą do orzeczenia.
    """
    z_dopełnieniem, bez_dopełnienia = check(
        "Mieszczanie zabili okna deskami.\n\nRachunek zwraca się dotąd."
    )
    assert z_dopełnieniem.rachunki == bez_dopełnienia.rachunki == [((OKOLICZNIK, 1),)]


def test_czytanie_oparte_na_formie_spoza_rejestru_wychodzi_z_lasu_później():
    """Koszt morfologii idzie w górę, aż trafi na ciała, które się nim różnią.

    `Wszystko` jest u Morfeusza i rzeczownikiem, i przysłówkiem regionalnym
    (``olski/rejestr.py``), a czytania te różnią się dopiero pod `zdanie_składowe`.
    Koszt liczony na miejscu nie ruszyłby więc żadnego z nich.
    Czytań przy tym nie ubywa i werdykt zostaje ten sam.
    """
    (werdykt,) = check("Wszystko jest podmiotem.")
    assert [sorted(zdanie) for (zdanie,) in werdykt.readings] == [
        ["orzeczenie", "orzecznik", "podmiot"],
        ["okolicznik_przysłówkowy", "orzeczenie", "orzecznik"],
    ]


def test_podmiot_za_czasownikiem_wychodzi_przed_czytaniem_bez_podmiotu():
    """Opuszczenie podmiotu płaci w każdym szyku, więc i tam, gdzie za czasownikiem coś stoi.

    `Rozstrzyga odsłownik.` czyta się dwojako: z `odsłownik` w podmiocie za
    czasownikiem albo w dopełnieniu, z podmiotem opuszczonym.
    Bez ceny drugie czytanie było darmowe, a pierwsze płaciło `czasownik przed
    podmiotem`, więc gramatyka orzekała rzecz, której nikt nie zadeklarował:
    że szukanie podmiotu w zdaniu obok jest zwyklejsze od podmiotu, który stoi
    na miejscu.
    """
    (werdykt,) = check("Rozstrzyga odsłownik.")
    assert [sorted(zdanie) for (zdanie,) in werdykt.readings] == [
        ["orzeczenie", "podmiot"],
        ["dopełnienie", "orzeczenie"],
    ]
    assert werdykt.rachunki == [
        ((CZASOWNIK_PRZED_PODMIOTEM, 1),),
        ((OPUSZCZONY_PODMIOT, 1),),
    ]


def _wydruk(ziarno: str, ścieżka: Path) -> str:
    """Wydruk komendy z procesu o tym ziarnie haszy napisów.

    Flagi są wszystkie, bo każda dokłada listę; kod wyjścia jest jedynką, bo
    komenda te zdania zgłasza, więc awarię odróżnia od zgłoszenia wyjście błędów.
    """
    komenda = ("olski.check", "--readings", "--morfologia", "--rozstrzygaj", "--zatrzymania")
    przebieg = subprocess.run(
        [sys.executable, "-m", *komenda, str(ścieżka)],
        env={**os.environ, "PYTHONHASHSEED": ziarno},
        capture_output=True,
        text=True,
    )
    assert not przebieg.stderr, przebieg.stderr
    return przebieg.stdout


def test_wydruk_wychodzi_ten_sam_pod_dwoma_ziarnami_haszy(tmp_path):
    """Ani kolejności wewnątrz wydruku, ani wyboru wartości nie oddaje się haszom.

    Zdania idą plikiem, bo świadek kontekstowy czyta zdanie stojące wyżej
    w akapicie.
    """
    zdania = (
        #  Czytań więcej, niż lista wypisuje.
        SIEDEM_PRZYŁĄCZEŃ,
        #  Druga taka lista, ta pod konstytuentem: kształty wybiera tam odsiew
        #  po zbiorze pozycji żywych.
        "Ustawa mówi, że organ gminy wydaje przepis.",
        #  Wskazanie tabeli skłonności.
        "Daj przepis na faworki.",
        #  Wskazanie świadka kontekstowego: jego powód cytuje lemat wybrany
        #  ze zbioru lematów formy (`_pasujący` w `olski/rozstrzyganie.py`).
        "Wystąpiła awaria w systemie. Operator zgłosił awarię w systemie.",
        #  Zdanie bez czytania, czyli zatrzymania wraz z morfologią.
        "Go jest grą.",
    )
    ścieżka = tmp_path / "zdania.txt"
    ścieżka.write_text("\n".join(zdania) + "\n", encoding="utf-8")
    pierwszy = _wydruk("1", ścieżka)
    #  Wydruk, który którąś z tych list stracił, zgadza się sam ze sobą,
    #  więc najpierw sprawdzamy, że jest w nim co pomylić.
    listy = (
        "czyta się tak:",
        "odczytanie 1:",
        "? „na faworki”",
        "? „w systemie”",
        "brak odczytania:",
    )
    for wiersz in listy:
        assert wiersz in pierwszy, f"wydruk nie ma tego, o co tu idzie: {wiersz}"
    wypisane = [w for w in pierwszy.splitlines() if w.lstrip().startswith("- ")]
    assert len(wypisane) > 1, "jedno czytanie nie ma kolejności, którą można pomylić"
    assert pierwszy == _wydruk("12345", ścieżka)


#: Zdanie o dwóch wyrażeniach przyimkowych, czyli o dwóch pozycjach jednej roli.
#: Pisane ręką, a nie wzięte z próby: zdania korpusu audytowego są długie,
#: a obie własności niżej czyta się na jednym krótkim.
DWA_PRZYIMKI = "Program zapisuje ustawienia w pliku na dysku."


def _wybór(fraza: str, wzorzec: str = "pliku") -> Wybór:
    """Wpis próby o tej frazie i tym gospodarzu we wzorcu."""
    return Wybór(
        plik="próba",
        kontekst=(),
        zdanie=DWA_PRZYIMKI,
        fraza=fraza,
        gospodarze=("zapisuje", "ustawienia", "pliku"),
        wzorzec=wzorzec,
        powód="własność testu, a nie sąd o rejestrze",
    )


def test_sonda_kolejności_pyta_drzewo_tam_gdzie_streszczenie_o_pozycji_milczy():
    """`na dysku` dochodzi w czytaniu pierwszym do `pliku`, a streszczenie o tym milczy.

    Rola przyłączana jest w streszczeniu nazwana pierwszym wystąpieniem
    (`olski/parse/streszczenie.py`), więc wypisuje się z niej `w pliku na dysku`,
    a o pozycji drugiej mówi tam tylko drzewo.
    Sonda czytająca samo streszczenie liczyłaby ten wpis jako przemilczany.
    """
    sąd = osądź(_wybór("na dysku"))
    assert (sąd.klasa, sąd.gospodarz) == (TRAFNA, "pliku")


def test_fraza_krótsza_od_konstytuentu_dostaje_jego_gospodarza():
    """`w pliku` konstytuentem tego czytania nie jest; jest nim `w pliku na dysku`.

    Przyłączenie jest w obu to samo, bo lewa krawędź jest ta sama i jest nią
    przyimek, o który pytał czytający. Dopasowanie po całej frazie zostawiałoby
    tu wpis bez odpowiedzi, a fraza krótsza od konstytuentu pada we wzorcu nie
    raz: budowniczy proponuje przyimek wraz z trzema formami za nim, a ręka
    skraca (`harness/wybory.py`).
    """
    sąd = osądź(_wybór("w pliku", wzorzec="ustawienia"))
    assert (sąd.klasa, sąd.gospodarz) == (TRAFNA, "ustawienia")


def test_gospodarza_nie_dostaje_fraza_która_przyłączeniem_nie_jest():
    """`ustawienia w pliku` stoi w tym czytaniu, a przyłączeniem nie jest.

    Konstytuent zaczynający się tą frazą tu jest — całe dopełnienie — a jego
    gospodarz odpowiada o przyłączeniu dopełnienia, o które nikt nie pytał.
    Sonda pyta przez to o pozycje rozstrzygane, tym samym kryterium, którym
    wybiera modyfikator werdykt (`_nazwane_przyłączenia` w
    `olski/parse/decyzje.py`).
    """
    sąd = osądź(_wybór("ustawienia w pliku"))
    assert sąd.klasa == INNY_KONSTYTUENT
    assert not sąd.gospodarz
