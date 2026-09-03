"""Te własności sondy luki, na których stoi jej werdykt.

Sonda kłamie po cichu, a każde takie kłamstwo czyta się jak dobra wiadomość.
Wariant ``olski`` przepisany, a nie wzięty, przestaje być olskim, i
wtedy każde przejście w tabeli jest przejściem między dwiema cudzymi gramatykami.
Zamknięcie, które nie zatrzyma się na zaimku, wpuszcza wyjęcie z wnętrza zdania
względnego, czyli wariant szerszy, niż sonda o sobie mówi. Luka wypuszczona
spod symbolu, który jej nie niesie, nie zostaje domknięta przez żaden zaimek i
mnoży czytania zdaniom, w których zaimka nie ma wcale. A wariant z luką ogłoszony
najszerszym zabiera tabeli te przejścia, po które ta sonda stoi.

Zdania niżej są zarazem tym, na czym stoi wywód w ``docs/design-notes.md``, więc
przestawiony werdykt psuje tam akapit, a nie sam test. Cenę i zakup trzymają
osobno dwa testy, bo warunek precedencji ma je rozdzielać: gdyby oba warianty
wyszły jednym, tabela nie mierzyłaby szyku luki wcale.
"""

from __future__ import annotations

import pytest

pytest.importorskip("morfeusz2")

from harness.luka import LUKA_SONDA, WARIANTY, niosące
from harness.ruch import gramatyka
from olski.subset import GRAMMAR
from olski.werdykt import check

#: Zdanie względne z wysuniętym podmiotem i drugie z wysuniętym dopełnieniem,
#: czyli dwie z trzech ról, które to zdanie wypełnia. Trzeciej — wyrażenia
#: przyimkowego — luka nie dotyczy, bo okolicznik jest wolny.
PODMIOT = "Reguła, która rozstrzyga, jest tania."
DOPEŁNIENIE = "Polszczyzna, którą ktoś napisał, jest trudna."
#: Wyjęcie z głębi: dopełnienie należy do bezokolicznika pod czasownikiem
#: modalnym, więc żadne ciało ``rdzeń_względny`` po nie nie sięga. Kupione, a nie
#: napotkane: nie ma go ani jeden korpus, jaki to repozytorium czyta, i dlatego
#: jest tym jednym zdaniem, które luka wyprowadza, a wypisane ciała nie.
Z_GŁĘBI = "Ustawa, którą organ gminy może wydać, jest tania."
#: Wysunięta grupa z zaimkiem w środku, a nie sam zaimek. Ciało, które ten szyk
#: wypisuje, wariant zdejmuje razem z resztą rodziny i luką go nie zastępuje, bo
#: luka wiąże się z zaimkiem stojącym samotnie.
GRUPA_NA_CZOLE = "Reguła, której koszt ktoś zna, jest tania."


def werdykt(wariant: str, zdanie: str):
    (jeden,) = check(zdanie, gramatyka(LUKA_SONDA, wariant))
    return jeden


def test_wariant_olskiego_jest_gramatyką_która_stoi():
    assert gramatyka(LUKA_SONDA, "olski").productions == GRAMMAR.productions


def test_wariant_z_luką_odrzuca_zdanie_które_olski_wyprowadza():
    """Wariantu najszerszego ta sonda przez to nie ma, a asercja niżej to trzyma.

    Wpisany dla przyspieszenia liczyłby to zdanie za odrzucone także pod olskim,
    czyli zabrałby tabeli przejście, które jest mierzoną ceną
    (``_bez_zbędnych`` w ``harness/ruch.py``).
    """
    assert werdykt("olski", GRUPA_NA_CZOLE).status == "valid"
    for wariant in WARIANTY[1:]:
        assert werdykt(wariant, GRUPA_NA_CZOLE).status == "rejected"
    assert LUKA_SONDA.najszerszy is None


def test_luki_nie_unosi_grupa_imienna_choć_niesie_zdanie_względne():
    """Zamknięcie liczone z produkcji ma się zatrzymać na zaimku, a nie wyżej.

    Grupa imienna unosi zdanie względne, więc bez tego zatrzymania sięgnęłaby
    luki pod nim i wariant wpuszczałby wyjęcie z wnętrza zdania względnego, czyli
    konstrukcję, której nie ma po co mierzyć.
    """
    unoszą = niosące(GRAMMAR)
    assert "zdanie_składowe" in unoszą
    assert unoszą.isdisjoint({"grupa_imienna", "człon_imienny", "rdzeń_względny", "wypowiedzenie"})


@pytest.mark.parametrize("zdanie", [PODMIOT, DOPEŁNIENIE])
def test_luka_stojąca_wszędzie_odbiera_zdaniu_względnemu_jednoznaczność(zdanie: str):
    """Kształtów jest tyle, ile pozycji roli, bo luka napisu nie ma i szyk jej nie widzi."""
    assert werdykt("olski", zdanie).status == "valid"
    assert werdykt("luka wszędzie", zdanie).status == "ambiguous"


@pytest.mark.parametrize("zdanie", [PODMIOT, DOPEŁNIENIE])
def test_luka_przypięta_do_pozycji_roli_jednoznaczność_oddaje(zdanie: str):
    assert werdykt("luka kanoniczna", zdanie).result.ile == 1


def test_luka_kupuje_to_czego_wypisane_ciała_nie_mają():
    """Zakupem jest wyprowadzenie, więc tyle i tylko tyle żąda się tu od obu wariantów.

    Jednoznaczność tego zdania jest osobną własnością i trzyma ją test niżej, tak
    samo jak przy zdaniach z wysuniętym podmiotem i dopełnieniem wyżej.
    """
    assert werdykt("olski", Z_GŁĘBI).status == "rejected"
    for wariant in WARIANTY[1:]:
        assert werdykt(wariant, Z_GŁĘBI).result.ile > 0


def test_luka_stojąca_wszędzie_odbiera_jednoznaczność_także_wyjęciu_z_głębi():
    """Kształtów jest tyle, ile pozycji w gramatyce, i wyjęcie z głębi nie jest wyjątkiem.

    Dopełnienie bezokolicznika ma pozycję wypisaną obok tej, w którą wypada luka
    (``FRAZA_BEZOKOLICZNIKOWA_OTWARTA`` w ``olski/subset/deklaracja.py``),
    więc luka stojąca wszędzie wydaje ten napis dwoma kształtami.
    Warunek precedencji zdejmuje tę cenę tutaj
    w całości, a przy ``Plik, który program zapisuje`` nie w całości, i o tę
    różnicę idzie w tabeli sondy.
    """
    assert werdykt("luka wszędzie", Z_GŁĘBI).status == "ambiguous"
    assert werdykt("luka kanoniczna", Z_GŁĘBI).result.ile == 1


@pytest.mark.parametrize("wariant", WARIANTY[1:])
def test_zdanie_bez_zaimka_względnego_luki_nie_dostaje(wariant: str):
    """Luka niedomknięta jest drugim kształtem zdania, w którym nikt jej nie szukał.

    Zdanie bez zaimka wychodzi tyloma czytaniami, iloma wychodzi w olskim, i
    dopiero to mówi, że przeciąganie domyka się na korzeniu.
    """
    for zdanie in ("Program zapisuje ustawienia.", "Zapisz plik konfiguracyjny."):
        assert werdykt(wariant, zdanie).result.ile == werdykt("olski", zdanie).result.ile


@pytest.mark.parametrize("wariant", WARIANTY[1:])
def test_luka_wypełnia_rolę_pustą_rozpiętością(wariant: str):
    """Na tym stanął pomiar, bo bank drzew stawia tę rolę na zaimku.

    Rola wypełniona niczym jest w drzewie i nie ma napisu, więc pomiar pokrycia
    porównuje rozpiętość pustą ze złotą i liczy niezgodę. Werdykt tego nie
    pokazuje: streszczenie czytania zatrzymuje się na zdaniu podrzędnym, więc o
    roli z jego wnętrza milczy tak samo, jak milczy o roli wypełnionej zaimkiem.
    """
    jeden = werdykt(wariant, "Myślę o regule, która rozstrzyga.")
    (podmiot,) = jeden.result.readings[0].find("podmiot")
    assert podmiot.forms() == []
    assert "podmiot" not in jeden.readings[0]
