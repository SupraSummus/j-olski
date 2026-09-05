"""Czego warstwa szukająca niejasnych odniesień ma nie zgłaszać.

Zgłasza ona zaimek, który zgadza się z dwiema rzeczami z sąsiedniego zdania, więc
sądem nietrywialnym jest tu każde milczenie: co liczy się za jedną rzecz, dokąd
sięga sąsiedztwo i kiedy zaimek jest rozstrzygnięty na miejscu
(``olski/odniesienia.py``). Każdy z tych warunków, zdjęty osobno, zamienia jedno
z tych zdań w zgłoszenie, i to jest jedyny powód, dla którego one tu stoją.

Rozszerzenie stojące za flagą ``w_zdaniu`` szuka rzeczy także w zdaniu zaimka,
więc jego zdania stoją tu parami: pod flagą zgłoszenie, a bez niej milczenie.
Zgłoszenie to nosi własną nazwę, bo to ona trzyma regułę czekającą na awans
poza kodem wyjścia, i jeden z tych sądów jest właśnie o niej.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.werdykt import ODNIESIENIE_W_ZDANIU, nad_tekstem


def zgłoszenia(tekst: str, w_zdaniu: bool = False) -> list[tuple[tuple[str, tuple[str, ...]], ...]]:
    """Zgłoszenia nad tekstem jako pary (zaimek, rzeczy), po jednej krotce na zdanie."""
    return [
        tuple((o.zaimek, o.rzeczy) for o in zdanie.odniesienia)
        for zdanie in nad_tekstem(tekst, w_zdaniu)
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


def test_rzeczy_z_poprzedniego_składowego_wychodzą_dopiero_pod_flagą():
    #  Zaimek stoi w drugim składowym i nie ma przed sobą w nim nic, więc rzeczy
    #  podaje składowe pierwsze. Bez flagi zdanie milczy, choć nazywa i psa,
    #  i kota, a oba zgadzają się z `on`.
    tekst = "Pies gonił kota, a on uciekł."
    assert zgłoszenia(tekst, w_zdaniu=True)[0] == (("on", ("Pies", "kota")),)
    assert zgłoszenia(tekst)[0] == ()


def test_rzeczy_dla_zaimka_dzierżawczego_wychodzą_z_jego_własnego_składowego():
    #  `jego` nie odsyła do zdania obok, tylko do jednej z dwóch grup, które
    #  stoją przed nim w tym samym składowym. Zdanie jest jednym składowym, więc
    #  bez rzeczy z niego samego kandydatów nie ma tu wcale.
    tekst = "Jan poprosił Piotra o jego samochód."
    assert zgłoszenia(tekst, w_zdaniu=True)[0] == (("jego", ("Jan", "Piotra")),)
    assert zgłoszenia(tekst)[0] == ()


def test_pod_flagą_rzeczy_podaje_kawałek_najbliższy_a_nie_każdy_przed_zaimkiem():
    #  Kawałek bliższy niż zdanie obok nazywa jedną rzecz zgodną z `je`, czyli
    #  `kwiaty`, więc czytelnik dalej nie sięga. Kawałki zsumowane dołożyłyby
    #  do niej maki i garnki, czyli wybór, którego on nie rozważa.
    tekst = "Maki rosną w garnkach. Sadzimy kwiaty i podlewamy je."
    assert zgłoszenia(tekst, w_zdaniu=True)[1] == ()


def test_zgłoszenie_spod_flagi_nie_jest_znaleziskiem():
    """Flaga nie rusza kodu wyjścia, bo jej zgłoszenie nosi własną nazwę.

    Reguła za flagą czeka na awans, więc do liczby, po którą pyta ``olski-check``,
    wchodzić jej nie wolno; bez osobnej nazwy wchodziłaby tam razem z regułą
    awansowaną wcześniej.
    """
    zdanie = nad_tekstem("Pies gonił kota, a on uciekł.", w_zdaniu=True)[0]
    assert zdanie.zgłoszenia == (ODNIESIENIE_W_ZDANIU,)
    assert zdanie.znaleziska == ()


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
