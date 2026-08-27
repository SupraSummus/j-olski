"""Sonda nieciągłości: skąd liczy szczeliny i czym różni od siebie dwie strony ceny.

Lasy są tu pisane ręcznie z tego samego powodu, co w ``tests/test_corpus.py``:
Składnica stoi pod GPL, a to repozytorium nie ma pliku licencji.

Sonda może skłamać po cichu trzy razy, i wszystkie trzy kłamstwa czytają się jak
dobra wiadomość. Szczelina policzona z pliku, a nie z drzewa wybranego, daje
zakup kilka razy większy, niż jest, bo annotator odrzucał właśnie ją. Ta sama
pomyłka na odwrót zeruje maskowanie, bo szukana jest tam szczelina odrzucona, a
drzewo wybrane ma ją tylko w zdaniach, których to pytanie nie dotyczy. A dwie
strony ceny puszczone z tym samym warunkiem spójności dają tabelę samych przejść
``x → x``, czyli wydruk mówiący, że nieciągłość nie kosztuje nic.
"""

import xml.etree.ElementTree as ET

import pytest

pytest.importorskip("morfeusz2")

from harness.nieciągłość import SZCZELINA, podłoże, szczeliny, w_lesie
from olski.corpus import read_forest
from olski.segmentacja import morphology
from tests.test_corpus import forest, phrase, terminal


def zdanie(szczelina: str, obok: str = ""):
    """*Jednej siostrze mogła się zwierzyć.* — z kategorią, którą podano, nad frazą wysuniętą.

    Dopełnienie bezokolicznika stoi przed formą osobową, czyli tak, jak wygląda
    zdanie, dla którego szczelina w Świgrze jest. Węzeł ``6`` jest tą frazą, a
    argument mówi, czym on jest: szczeliną albo zwykłą frazą wymaganą.

    ``obok`` dokłada węzeł, którego odpowiedź nie bierze, czyli drugie czytanie
    tego samego zdania. Tak wygląda w Składnicy zdanie maskowane: drzewo wybrane
    obywa się bez szczeliny, a Świgra znalazła obok niego analizę z nią.
    """
    return forest(
        phrase(0, 0, 6, "zdanie", [6, 2, 4, 9])
        + phrase(6, 0, 2, szczelina, [7])
        + phrase(7, 0, 2, "fno", [8, 10])
        + terminal(8, 0, 1, "Jednej", "adj:sg:dat:f:pos", lemma="jeden")
        + terminal(10, 1, 2, "siostrze", "subst:sg:dat:f", lemma="siostra")
        + phrase(2, 2, 3, "ff", [3])
        + terminal(3, 2, 3, "mogła", "praet:sg:f:imperf", lemma="móc")
        + phrase(4, 3, 5, "fwe", [5, 11])
        + terminal(5, 3, 4, "się", "qub")
        + terminal(11, 4, 5, "zwierzyć", "inf:perf", lemma="zwierzyć")
        + terminal(9, 5, 6, ".", "interp")
        + obok,
        text="Jednej siostrze mogła się zwierzyć.",
    )


def na_dysku(tmp_path, las, nazwa: str):
    """Ten las w pliku, bo ``w_lesie`` czyta bajty, a gotowy element ich nie ma."""
    ścieżka = tmp_path / nazwa
    ścieżka.write_bytes(ET.tostring(las, encoding="utf-8"))
    return ścieżka


def test_szczelina_liczy_się_z_drzewa_wybranego_a_nie_z_pliku():
    """Węzeł, którego odpowiedź nie bierze, nie jest zdaniem polszczyzny.

    Ten sam las z tą samą kategorią w środku, raz w odpowiedzi i raz poza nią.
    Bez tej różnicy zakup wychodzi z częstości, z jaką annotator szczelinę
    odrzucał, a nie z częstości, z jaką ją wybierał.
    """
    assert szczeliny(zdanie(SZCZELINA)) == 1
    assert szczeliny(zdanie("fw")) == 0


def test_maskowanie_liczy_szczelinę_odrzuconą_a_nie_wybraną(tmp_path):
    """Ten sam plik daje zero z drzewa wybranego i szczelinę z lasu.

    Na tej różnicy stoi cały ten licznik, a ``w_lesie`` przepisane na rozebrany
    las — ruch, który czyta się jak porządki — melduje maskowanie zerowe
    niezależnie od tego, ile go jest.
    """
    ciągłe = na_dysku(tmp_path, zdanie("fw"), "ciągłe.xml")
    maskowane = na_dysku(
        tmp_path,
        zdanie("fw", obok=phrase(20, 0, 2, SZCZELINA, [7], chosen="false")),
        "maskowane.xml",
    )

    assert szczeliny(read_forest(maskowane)) == 0
    assert w_lesie(maskowane)
    assert not w_lesie(ciągłe)


def test_zdjęcie_spójności_odbiera_zdaniu_jednoznaczność():
    """Dwie strony ceny są dwiema stronami, a nie dwoma przebiegami jednej.

    ``do poprzedniej wagi`` dochodzi do ``Człowiek`` ponad czasownikiem, gdy
    fraza nie musi już być odcinkiem tekstu, i to jest ta jedna wartość logiczna,
    na której cała cena stoi. Sonda, która oba przebiegi puszcza tak samo,
    wypisuje tabelę bez ani jednego ruchu i czyta się jak wynik.
    """
    segmenty = morphology("Człowiek wraca do poprzedniej wagi.")
    assert podłoże(segmenty, spójne=True, budżet=10.0) == "valid"
    assert podłoże(segmenty, spójne=False, budżet=10.0) == "ambiguous"
