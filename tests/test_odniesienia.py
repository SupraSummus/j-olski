"""Czego warstwa szukająca niejasnych odniesień ma nie zgłaszać.

Zgłasza ona zaimek, który zgadza się z dwiema rzeczami z sąsiedniego zdania, więc
sądem nietrywialnym jest tu każde milczenie: co liczy się za jedną rzecz, dokąd
sięga sąsiedztwo i kiedy zaimek jest rozstrzygnięty na miejscu
(``olski/odniesienia.py``). Każdy z tych warunków, zdjęty osobno, zamienia jedno
z tych zdań w zgłoszenie, i to jest jedyny powód, dla którego one tu stoją.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.werdykt import nad_tekstem


def zgłoszenia(tekst: str) -> list[tuple[tuple[str, tuple[str, ...]], ...]]:
    """Zgłoszenia nad tekstem jako pary (zaimek, rzeczy), po jednej krotce na zdanie."""
    return [
        tuple((o.zaimek, o.rzeczy) for o in zdanie.odniesienia) for zdanie in nad_tekstem(tekst)
    ]


def test_zaimek_zgodny_z_dwiema_rzeczami_z_sąsiedniego_zdania_jest_zgłoszeniem():
    """Para, którą docs/roadmap.md stawia jako powód, dla którego umowa jest o tekście."""
    assert zgłoszenia("Maki rosną w garnkach. Są one czerwone.")[1] == (
        ("one", ("Maki", "garnkach")),
    )


def test_rzeczą_jest_najszersza_grupa_imienna_a_nie_rzeczownik_pod_nią():
    #  Zdanie nazywa pole i doniczkę, a `maków` i `bratków` są w nich
    #  określeniami. Zejście pod głowę wydaje kandydatów tylu, ile zdanie ma
    #  rzeczowników, i te dwa określenia zgadzają się z `one` oba.
    tekst = "Ogrodnik ogląda pole maków w doniczce bratków. Są one czerwone."
    assert zgłoszenia(tekst)[1] == ()


def test_rzecz_nazwana_dwa_razy_w_jednym_zdaniu_jest_jedną_rzeczą():
    #  `Maki` i `maków` dzielą lemat, więc czytelnik nie ma tu między czym
    #  wybierać; liczone osobno dałyby zgłoszenie nad każdym zdaniem, które o
    #  czymś mówi dwa razy.
    assert zgłoszenia("Maki rosną wśród maków. Są one czerwone.")[1] == ()


def test_zgodność_liczy_się_parami_odczytań_a_nie_sumą_cech():
    #  `je` jest pojedynczą nijaką albo mnogą niemęskoosobową, a `Program` i
    #  `plik` są pojedyncze męskie. Suma cech zaimka wpuszcza pojedynczą męską,
    #  której to słowo nie ma, i zgadza go wtedy z obydwoma.
    assert zgłoszenia("Program zapisuje plik. Widzimy je.")[1] == ()


def test_zaimek_rozstrzygnięty_we_własnym_zdaniu_zgłoszenia_nie_dostaje():
    #  `kwiaty` stoi przed `je` i zgadza się z nim, więc czytelnik po rzecz do
    #  zdania obok nie sięga. Bez tego wstrzymania oba maki i garnki wychodzą
    #  stąd jako wybór, którego on nie rozważa.
    tekst = "Maki rosną w garnkach. Ogrodnik sadzi kwiaty i podlewa je."
    assert zgłoszenia(tekst)[1] == ()


def test_zdanie_pierwsze_w_akapicie_nie_ma_sąsiada_i_zgłoszenia_nie_dostaje():
    #  Granicą jest akapit, bo akapit jest tym, w czym „obok” się kończy
    #  (`Sąsiedztwo` w `olski/rozstrzyganie.py`).
    assert zgłoszenia("Maki rosną w garnkach.\n\nSą one czerwone.")[1] == ()


def test_rzeczy_podaje_zdanie_obok_a_nie_cały_akapit_przed_zaimkiem():
    #  Maki i garnki stoją dwa zdania wcześniej, więc czytelnik nie ma ich pod
    #  ręką; zdanie obok nie nazywa ani jednej rzeczy zgodnej z `one`.
    tekst = "Maki rosną w garnkach. Ogrodnik pracuje. Są one czerwone."
    assert zgłoszenia(tekst)[2] == ()


def test_zdanie_bez_odczytania_nie_podaje_ani_jednej_rzeczy():
    """Milczenie z braku pokrycia zgłoszenie chowa, a wymyślić go nie może.

    Warunek ten jest tym, na czym stoi decyzja, żeby zaimka bez ani jednego
    kandydata nie zgłaszać: zero kandydatów znaczy tu dwie różne rzeczy.
    """
    tekst = "Nowa program zapisuje ustawienia w garnkach. Są one czerwone."
    assert nad_tekstem(tekst)[0].werdykt.result.rejected
    assert zgłoszenia(tekst)[1] == ()
