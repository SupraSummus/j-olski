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

Druga reguła tej warstwy zgłasza zaimek dzierżawczy, którego posiadaczem jest
podmiot zdania, bo o rzeczy podmiotu polszczyzna mówi `swój`. Trafienie ma ona
jedno i milczeń kilka, więc sądy nietrywialne są tu te same co wyżej: co zdejmuje
kandydata i dokąd sięga kawałek, w którym się go szuka.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.werdykt import ODNIESIENIE_W_ZDANIU, ZAIMEK_NIEZWROTNY, nad_tekstem


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


def niezwrotne(tekst: str) -> list[tuple[tuple[str, str, str], ...]]:
    """Zgłoszenia o zaimkach dzierżawczych jako trójki, po jednej krotce na zdanie."""
    return [
        tuple((n.zaimek, n.rzecz, n.podmiot) for n in zdanie.werdykt.niezwrotne)
        for zdanie in nad_tekstem(tekst)
    ]


def test_zaimek_dzierżawczy_zgodny_z_samym_podmiotem_jest_zgłoszeniem():
    """Zdanie, na którym reguła stoi (``próba/nkjp-sądy.txt``).

    Kandydatem na posiadacza jest tu sam podmiot, a `swojego` jest tym, co autor
    napisałby o stosunku kandydata, więc czytelnik nie ma dokąd pójść.
    Kandydat jest jeden dzięki temu, że grupa imienna z zaimkiem rzeczy nie
    wydaje: bez tego zawężenia `omawiania` i `stosunku` dokładają dwóch i
    zgłoszenie schodzi.
    """
    zdanie = "Kandydat sam natychmiast przystąpił do omawiania jego stosunku do służby."
    assert niezwrotne(zdanie)[0] == (("jego", "stosunku", "Kandydat"),)


def test_rzecz_zgodna_obok_podmiotu_zdejmuje_zgłoszenie():
    #  O półciężarówce Marka autor napisałby `swoją`, więc `jego` podejmuje
    #  Grzesia i czytelnik ma dokąd pójść. Zdanie o kilku kandydatach jest tym,
    #  o co pyta reguła obok, a nie ta.
    zdanie = "Marek stał na poboczu, czekając na Grzesia i jego półciężarówkę."
    assert niezwrotne(zdanie)[0] == ()


def test_rzecz_spięta_z_zaimkiem_spójnikiem_kandydatem_zostaje():
    #  Ciąg współrzędny obejmuje `jego`, a artysta stoi obok zaimka, nie nad nim,
    #  więc posiadaczem być może; zdjęty razem z całym ciągiem zostawiałby tu
    #  `Manifest` jako kandydata jedynego.
    zdanie = "Manifest brał pod opiekę artystę i jego twórczość."
    assert niezwrotne(zdanie)[0] == ()


def test_zaimek_stojący_w_podmiocie_zgłoszenia_nie_dostaje():
    #  `swój` podejmuje podmiot, więc w samym podmiocie orzekałby o sobie i
    #  polszczyzna go tam nie stawia; autor nie ma tu czego poprawiać.
    zdanie = "Rada Ministrów i jej prezes powinni określić termin."
    assert niezwrotne(zdanie)[0] == ()


def test_podmiot_stojący_za_zaimkiem_kandydatem_nie_jest():
    #  Czytelnik szuka posiadacza wstecz, tak samo jak przy regule obok, a
    #  `telefon` stoi za zaimkiem i nie jest niczym, co on podejmuje.
    zdanie = "U jego stóp leżał zrujnowany telefon."
    assert niezwrotne(zdanie)[0] == ()


def test_zgłoszenie_o_zaimku_dzierżawczym_nie_jest_znaleziskiem():
    """Reguła czeka na sądy czytelnika, więc kodu wyjścia nie rusza.

    Sąd ten jest o tej samej granicy co sąd o rozszerzeniu spod ``w_zdaniu``,
    a stoi osobno, bo obie nazwy trzeba było wpisać poza :data:`ZNALEZISKA`
    osobno.
    """
    zdanie = nad_tekstem("Kandydat przystąpił do omawiania jego stosunku do służby.")[0]
    assert ZAIMEK_NIEZWROTNY in zdanie.zgłoszenia
    assert zdanie.znaleziska == ()


def test_zdanie_bez_odczytania_nie_podaje_ani_jednej_rzeczy():
    """Milczenie z braku pokrycia zgłoszenie chowa, a wymyślić go nie może.

    Warunek ten jest tym, na czym stoi decyzja, żeby zaimka bez ani jednego
    kandydata nie zgłaszać: zero kandydatów znaczy tu dwie różne rzeczy.
    """
    tekst = "Nowa program zapisuje ustawienia w garnkach. Są one czerwone."
    assert nad_tekstem(tekst)[0].werdykt.result.rejected
    assert zgłoszenia(tekst)[1] == ()
