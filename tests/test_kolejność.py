"""Kolejność czytań stoi na deklaracji, a nie na kolejności dopisań ani na haszach.

Czym ta kolejność jest i po co, mówi
docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie.

Hasze napisów losuje start procesu, więc zbiór postawiony na drodze do wydruku
wypisuje w każdym przebiegu co innego (CLAUDE.md#code).
Widać to wyłącznie między procesami, bo ziarno jest jedno na proces,
więc pyta o to podproces, i pyta dwa razy.
"""

import os
import random
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

from olski.cennik import CENNIK, CZASOWNIK_PRZED_PODMIOTEM, OKOLICZNIK, OPUSZCZONY_PODMIOT
from olski.grammar import Grammar, Głowa, nt, word
from olski.parse import parse
from olski.rejestr import POZA_REJESTREM, pozycje
from olski.segmentacja import morphology
from olski.subset import build
from olski.werdykt import check
from tests.test_las import SIEDEM_PRZYŁĄCZEŃ

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


def test_koszt_produkcji_nie_sumuje_się_do_kosztu_rodzica():
    """Ciała córki rozstrzygnęła córka, więc jej koszt nie waży już nad rodzicem.

    Gramatyka jest napisana pod tę jedną własność: `lewe` i `prawe` mają córki
    tej samej rozpiętości i kosztują tyle samo, więc o kolejności rozstrzyga
    alfabet etykiet, a koszt zsumowany po poddrzewie wpuszczałby przodem `prawe`.
    Sumowanie jest tu pomyłką prawdopodobną, bo tak właśnie sumuje się koszt
    morfologii, a widać ją tylko po kolejności: czytań nie ubywa.
    """
    grammar = Grammar(start="zdanie")
    grammar.rule("zdanie", [Głowa(nt("lewe"))])
    grammar.rule("zdanie", [Głowa(nt("prawe"))])
    grammar.rule("lewe", [Głowa(word("subst")), word("interp")], koszty=(OKOLICZNIK,))
    grammar.rule("prawe", [Głowa(word("subst")), word("interp")])
    czytania = parse(grammar, morphology("plik.")).readings
    assert [drzewo.children[0].label for drzewo in czytania] == ["lewe", "prawe"]


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
