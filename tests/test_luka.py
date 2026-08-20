"""Te własności sondy luki, na których stoi jej werdykt.

Sonda może skłamać po cichu trzy razy, i każde kłamstwo czyta się jak dobra
wiadomość. Wariant ``olski`` przepisany, a nie wzięty, przestaje być olskim, i
wtedy każde przejście w tabeli jest przejściem między dwiema cudzymi gramatykami.
Zamknięcie, które nie zatrzyma się na zaimku, wpuszcza wyjęcie z wnętrza zdania
względnego, czyli wariant szerszy, niż sonda o sobie mówi. A luka wypuszczona
spod symbolu, który jej nie niesie, nie zostaje domknięta przez żaden zaimek i
mnoży czytania zdaniom, w których zaimka nie ma wcale.

Zdania niżej są zarazem tym, na czym stoi wywód w ``docs/design-notes.md``, więc
przestawiony werdykt psuje tam akapit, a nie sam test. Cenę i zakup trzymają
osobno dwa testy, bo warunek precedencji ma je rozdzielać: gdyby oba warianty
wyszły jednym, tabela nie mierzyłaby szyku luki wcale.
"""

from __future__ import annotations

import pytest

pytest.importorskip("morfeusz2")

from harness.luka import WARIANTY, gramatyka, niosące
from olski.subset import GRAMMAR, check

#: Zdanie względne z wysuniętym podmiotem i drugie z wysuniętym dopełnieniem,
#: czyli dwie z trzech ról, które to zdanie wypełnia. Trzeciej — wyrażenia
#: przyimkowego — luka nie dotyczy, bo okolicznik jest wolny.
PODMIOT = "Reguła, która rozstrzyga, jest tania."
DOPEŁNIENIE = "Polszczyzna, którą ktoś napisał, jest trudna."
#: Zdanie względne z wysuniętym dopełnieniem i opuszczonym podmiotem, czyli to,
#: co luka nad Składnicą naprawdę kupuje: cztery zdania tego kształtu i nic poza
#: nimi. Każde ciało ``RelativeCore`` ma podmiot wypisany.
BEZ_PODMIOTU = "Dyrektor wymienia imprezy, które zorganizował."
#: Wyjęcie z głębi: dopełnienie należy do bezokolicznika pod czasownikiem
#: modalnym, więc żadne ciało ``RelativeCore`` po nie nie sięga. Kupione, a nie
#: napotkane: nie ma go ani jeden korpus, jaki to repozytorium czyta, i dlatego
#: stoi tu obok tamtego, a nie zamiast niego.
Z_GŁĘBI = "Ustawa, którą organ gminy może wydać, jest tania."


def werdykt(wariant: str, zdanie: str):
    (jeden,) = check(zdanie, gramatyka(wariant))
    return jeden


def test_wariant_olskiego_jest_gramatyką_która_stoi():
    assert gramatyka("olski").productions == GRAMMAR.productions


def test_luki_nie_unosi_grupa_imienna_choć_niesie_zdanie_względne():
    """Zamknięcie liczone z produkcji ma się zatrzymać na zaimku, a nie wyżej.

    Grupa imienna unosi zdanie względne, więc bez tego zatrzymania sięgnęłaby
    luki pod nim i wariant wpuszczałby wyjęcie z wnętrza zdania względnego, czyli
    konstrukcję, której nie ma po co mierzyć.
    """
    unoszą = niosące(GRAMMAR)
    assert "ClauseConjunct" in unoszą
    assert unoszą.isdisjoint({"NP", "NPConjunct", "RelativeCore", "Sentence"})


@pytest.mark.parametrize("zdanie", [PODMIOT, DOPEŁNIENIE])
def test_luka_stojąca_wszędzie_odbiera_zdaniu_względnemu_jednoznaczność(zdanie: str):
    """Kształtów jest tyle, ile pozycji roli, bo luka napisu nie ma i szyk jej nie widzi."""
    assert werdykt("olski", zdanie).status == "valid"
    assert werdykt("luka wszędzie", zdanie).status == "ambiguous"


@pytest.mark.parametrize("zdanie", [PODMIOT, DOPEŁNIENIE])
def test_luka_przypięta_do_pozycji_roli_jednoznaczność_oddaje(zdanie: str):
    assert werdykt("luka kanoniczna", zdanie).result.ile == 1


@pytest.mark.parametrize("zdanie", [BEZ_PODMIOTU, Z_GŁĘBI])
def test_luka_kupuje_to_czego_wypisane_ciała_nie_mają(zdanie: str):
    assert werdykt("olski", zdanie).status == "rejected"
    for wariant in WARIANTY[1:]:
        assert werdykt(wariant, zdanie).result.ile == 1


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
    jeden = werdykt(wariant, "Myślę o tym człowieku, który mnie podglądał.")
    (podmiot,) = jeden.result.readings[0].find("Subject")
    assert podmiot.forms() == []
    assert "Subject" not in jeden.readings[0]
