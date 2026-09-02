"""Dokąd gold tree przyłącza wyrażenie przyimkowe, czytane z kształtu drzewa.

Lasy są tu pisane ręcznie z tego samego powodu, co w ``tests/test_corpus.py``:
Składnica stoi pod GPL, a to repozytorium nie ma pliku licencji. Kształt, o który
tu chodzi, jest przy tym mniejszy niż cokolwiek, co korpus naprawdę zawiera —
jedna grupa imienna, jedno wyrażenie za nią i jeden węzeł nad nimi — więc las
prawdziwy niósłby przy okazji dziesięć innych rzeczy.
"""

import xml.etree.ElementTree as ET

import pytest

pytest.importorskip("morfeusz2")

from harness.attachment import Report, attachments, measure, render
from tests.test_corpus import forest, phrase, terminal


def zdanie(host):
    """*Trwa dochodzenie w tej sprawie.* z wyrażeniem przyłączonym gdzie trzeba.

    ``host`` mówi, pod czym stoi ``w tej sprawie``: pod grupą imienną, czyli
    przy rzeczowniku, albo pod zdaniem, czyli przy czasowniku. Reszta drzewa jest
    w obu przypadkach ta sama, więc różnica w wyniku bierze się z przyłączenia.
    """
    wnętrze = (
        phrase(3, 1, 2, "fno", [4])
        + terminal(4, 1, 2, "dochodzenie", "subst:sg:nom:n")
        + phrase(5, 2, 5, "fl", [6])
        + phrase(6, 2, 5, "fpm", [7, 8])
        + terminal(7, 2, 3, "w", "prep:loc")
        + phrase(8, 3, 5, "fno", [9, 10])
        + terminal(9, 3, 4, "tej", "adj:sg:loc:f:pos")
        + terminal(10, 4, 5, "sprawie", "subst:sg:loc:f")
    )
    if host == "noun":
        góra = phrase(0, 0, 6, "zdanie", [1, 2, 12]) + phrase(2, 1, 5, "fno", [3, 5])
    else:
        góra = phrase(0, 0, 6, "zdanie", [1, 3, 5, 12])
    return forest(
        góra
        + phrase(1, 0, 1, "ff", [11])
        + terminal(11, 0, 1, "Trwa", "fin:sg:ter:imperf", lemma="trwać")
        + wnętrze
        + terminal(12, 5, 6, ".", "interp"),
        text="Trwa dochodzenie w tej sprawie.",
    )


@pytest.mark.parametrize("host", ["noun", "clause"])
def test_przyłączenie_czyta_się_z_tego_pod_czym_wyrażenie_stoi(host):
    found = attachments(zdanie(host))
    assert [attachment.host for attachment in found] == [host]


def przed_czasownikiem():
    """*Dochodzenie w tej sprawie trwa.* — ta sama grupa, czasownik za nią.

    Przyłączenie do czasownika jest w polszczyźnie do wzięcia i tutaj, ale
    pomiar tego nie rozstrzyga i dlatego takie wyrażenie liczy się osobno.
    """
    return forest(
        phrase(0, 0, 6, "zdanie", [2, 1, 12])
        + phrase(2, 0, 4, "fno", [3, 5])
        + phrase(3, 0, 1, "fno", [4])
        + terminal(4, 0, 1, "Dochodzenie", "subst:sg:nom:n")
        + phrase(5, 1, 4, "fl", [6])
        + phrase(6, 1, 4, "fpm", [7, 8])
        + terminal(7, 1, 2, "w", "prep:loc")
        + phrase(8, 2, 4, "fno", [9, 10])
        + terminal(9, 2, 3, "tej", "adj:sg:loc:f:pos")
        + terminal(10, 3, 4, "sprawie", "subst:sg:loc:f")
        + phrase(1, 4, 5, "ff", [11])
        + terminal(11, 4, 5, "trwa", "fin:sg:ter:imperf", lemma="trwać")
        + terminal(12, 5, 6, ".", "interp"),
        text="Dochodzenie w tej sprawie trwa.",
    )


@pytest.mark.parametrize(
    ("las", "po_czasowniku"),
    [(lambda: zdanie("clause"), True), (przed_czasownikiem, False)],
)
def test_po_czasowniku_znaczy_że_przyłączenie_do_czasownika_było_do_wzięcia(las, po_czasowniku):
    #  Wyrażenie, przed którym czasownika nie ma, o wyborze nic nie mówi:
    #  przyłączenie do rzeczownika jest tam jedynym, jakie stało otworem.
    (znalezione,) = attachments(las())
    assert znalezione.postverbal is po_czasowniku
    assert znalezione.prep == "w"


def test_opakowanie_nie_jest_miejscem_przyłączenia():
    #  fl i fw mają tę samą rozpiętość co samo wyrażenie, więc zejście w górę
    #  przez nie przechodzi, a to, że wyrażenie stoi pod frazą luźną, wraca
    #  osobnym polem.
    (znalezione,) = attachments(zdanie("clause"))
    assert znalezione.frame == "fl"


def bez_grupy_przed_wyrażeniem():
    """*W pliku zapisuje ustawienia.* — wyrażenie, przed którym nie ma grupy imiennej.

    Przyłączenia do rzeczownika nie było, więc pozycja nie jest dwuznaczna i do
    rozkładu nie wchodzi.
    """
    return forest(
        phrase(0, 0, 5, "zdanie", [1, 5, 7, 9])
        + phrase(1, 0, 2, "fl", [2])
        + phrase(2, 0, 2, "fpm", [3, 4])
        + terminal(3, 0, 1, "W", "prep:loc")
        + phrase(4, 1, 2, "fno", [10])
        + terminal(10, 1, 2, "pliku", "subst:sg:loc:m3")
        + phrase(5, 2, 3, "ff", [6])
        + terminal(6, 2, 3, "zapisuje", "fin:sg:ter:imperf", lemma="zapisywać")
        + phrase(7, 3, 4, "fno", [8])
        + terminal(8, 3, 4, "ustawienia", "subst:pl:acc:n", lemma="ustawienie")
        + terminal(9, 4, 5, ".", "interp"),
        text="W pliku zapisuje ustawienia.",
    )


def test_wyrażenie_bez_grupy_imiennej_przed_sobą_nie_wchodzi_do_rozkładu():
    #  Czytnik oddaje je razem z resztą, bo pyta o nie pomiar szukający wzorca
    #  dla warstwy rozstrzygającej, a zwęża populację dopiero raport. Gdyby
    #  zwężał ją czytnik, `seen` liczyłoby co innego, niż mówi docs/subset.md.
    (znalezione,) = attachments(bez_grupy_przed_wyrażeniem())
    assert znalezione.postnominal is False
    report = Report()
    report.record(znalezione)
    assert report.seen == 0


def test_las_bez_gold_tree_nie_wchodzi_do_pomiaru():
    #  Cztery piąte korpusu to lasy z werdyktem innym niż FULL, a drzewa
    #  wybranego nie ma w nich wcale, więc liczenie ich zaniżałoby każdą stopę.
    assert attachments(forest("", verdict="NO_TREE")) == []


def test_raport_liczy_udział_przyimka_i_frazy_wymaganej(tmp_path):
    for numer, host in enumerate(["noun", "noun", "clause"]):
        (tmp_path / f"{numer}.xml").write_bytes(ET.tostring(zdanie(host), encoding="utf-8"))
    report = measure(sorted(tmp_path.glob("*.xml")))
    assert report.postverbal == {"noun": 2, "clause": 1}
    assert report.preps["w"] == {"noun": 2, "clause": 1}
    #  Wyrażenie stoi tu pod frazą luźną, więc walencja nie ma go czym zdjąć.
    assert report.required == {}
    wydruk = render(report)
    assert "3 wyrażeń przyimkowych za grupą imienną" in wydruk
    assert "66.7% do rzeczownika" in wydruk
