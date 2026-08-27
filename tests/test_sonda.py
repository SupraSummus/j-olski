"""Te dwie własności sondy, na których stoi jej wynik.

Sonda jest kodem pisanym pod decyzję i większość tego, co mówi, mówi wydrukiem,
którego nikt nie pilnuje. Dwie rzeczy są inne, bo na nich stoi sekcja
`docs/design-notes.md`, która z sondy wyszła: że oba podłoża wydają nad zdaniem
ten sam werdykt, i że nieciągłość jest tam zdejmowanym warunkiem, a nie
konstrukcją.

Pierwsza z nich pilnuje przy tym czegoś więcej niż siebie. ``harness/polszczyzna.py``
jest drugą deklaracją podzbioru, więc zmiana w ``olski/subset.py`` zestarzeje ją
po cichu, a ten test jest jedynym miejscem, w którym to wychodzi. Wtedy albo
deklaracje idą za produkcjami, albo sonda się kasuje, i `TODO.md` mówi, co
rozstrzyga który.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.polszczyzna import GRAMATYKA
from harness.wiezy import rozbierz
from olski.segmentacja import morphology
from olski.werdykt import check

#: Zdania, nad którymi oba podłoża zgadzają się co do werdyktu, po jednym na
#: konstrukcję, która to porównanie kiedykolwiek rozstrzygnęła: orzecznik w
#: narzędniku, orzecznik przymiotnikowy, dwa dopełniacze, współrzędność, zgodność
#: łamana przez rodzaj, przyłączenie oddane czytelnikowi i szyk OVS.
ZGODNE = [
    "Wejściem jest zwykły tekst polski.",
    "Ludzie są wolni.",
    "Celem jest parser tego podzbioru.",
    "Zobacz docs/design-notes.md oraz docs/roadmap.md.",
    "Nowa program zapisuje ustawienia.",
    "Program zapisuje ustawienia w pliku.",
    "Cały wywód prowadzi docs/linter.md.",
]


@pytest.mark.parametrize("zdanie", ZGODNE)
def test_oba_podłoża_wydają_ten_sam_werdykt(zdanie: str):
    werdykty = check(zdanie)
    assert len(werdykty) == 1
    rozbiór = rozbierz(morphology(zdanie), GRAMATYKA, limit=64)
    assert rozbiór.status == werdykty[0].status


def test_zdjęcie_spójności_wpuszcza_frazę_przerwaną_orzeczeniem():
    """Wynik sondy o nieciągłości, zapisany jako różnica dwóch przebiegów.

    Zdanie stoi poza rejestrem olskiego, bo lewostronna ekstrakcja w polskiej
    dokumentacji się nie zdarza, i po to tu jest: mierzy mechanizm, a nie to, ile
    tego mechanizmu README potrzebuje.
    """
    segmenty = morphology("Dobrą Jan pisze polszczyznę.")
    spójny = rozbierz(segmenty, GRAMATYKA, limit=64)
    nieciągły = rozbierz(segmenty, GRAMATYKA, limit=64, spójne=False)

    assert [czytanie.rola("Object") for czytanie in spójny.czytania] == ["polszczyznę"]
    assert "Dobrą polszczyznę (nieciągłe)" in [
        czytanie.rola("Object") for czytanie in nieciągły.czytania
    ]
