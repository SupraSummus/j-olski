"""Sonda nieciągłości: skąd liczy szczeliny i czym różni od siebie dwie strony ceny.

Lasy są tu pisane ręcznie z tego samego powodu, co w ``tests/test_corpus.py``:
Składnica stoi pod GPL, a to repozytorium nie ma pliku licencji.

Sonda może skłamać po cichu dwa razy, i oba kłamstwa czytają się jak dobra
wiadomość. Szczelina policzona z pliku, a nie z drzewa wybranego, daje zakup
kilka razy większy, niż jest, bo annotator odrzucał właśnie ją. A dwie strony
ceny puszczone z tym samym warunkiem spójności dają tabelę samych przejść
``x → x``, czyli wydruk mówiący, że nieciągłość nie kosztuje nic.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.subset import morphology
from sonda.nieciągłość import SZCZELINA, podłoże, szczeliny
from tests.test_corpus import forest, phrase, terminal


def zdanie(szczelina: str):
    """*Jednej siostrze mogła się zwierzyć.* — z kategorią, którą podano, nad frazą wysuniętą.

    Dopełnienie bezokolicznika stoi przed formą osobową, czyli tak, jak wygląda
    zdanie, dla którego szczelina w Świgrze jest. Węzeł ``6`` jest tą frazą, a
    argument mówi, czym on jest: szczeliną albo zwykłą frazą wymaganą.
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
        + terminal(9, 5, 6, ".", "interp"),
        text="Jednej siostrze mogła się zwierzyć.",
    )


def test_szczelina_liczy_się_z_drzewa_wybranego_a_nie_z_pliku():
    """Węzeł, którego odpowiedź nie bierze, nie jest zdaniem polszczyzny.

    Ten sam las z tą samą kategorią w środku, raz w odpowiedzi i raz poza nią.
    Bez tej różnicy zakup wychodzi z częstości, z jaką annotator szczelinę
    odrzucał, a nie z częstości, z jaką ją wybierał.
    """
    assert szczeliny(zdanie(SZCZELINA)) == 1
    assert szczeliny(zdanie("fw")) == 0


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
