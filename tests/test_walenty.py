"""Walenty przeczytany o te zdania i o tę pozycję ramy, które olski z niego bierze.

Słownika te testy nie potrzebują: schematy pisane ręcznie mówią o czytaniu
wszystko, co się o nim rozstrzyga, a pliki wejściowe nie stoją w repozytorium.

Kryterium przyimkowe ma tu własne testy, bo odpowiedzieć na jego pytanie
twierdząco można z trzech powodów, z których dwa ramą lematu nie są: przyimek
w pozycji podmiotu oraz przyimek zleksykalizowany wraz ze swoim rzeczownikiem.
Oba zawyżałyby zasięg świadka ramowego po cichu, bo wydruk wygląda tak samo,
a różnicę widać dopiero w liczbach `docs/disambiguation.md`.
"""

import pytest

from olski.walencja import (
    BIERZE_BEZOKOLICZNIK,
    CZASOWNIK,
    CZASOWNIK_ZWROTNY,
    NIE_BIERZE_BIERNIKA,
    RZECZOWNIK,
)
from olski.walenty import (
    BIERNIK,
    CELOWNIK,
    DOPEŁNIACZ,
    bierze,
    bierze_bezokolicznik_podmiotu,
    bierze_celownik_przy_wypełnieniu,
    bierze_ramą,
    leksykon,
    pozycje,
    przyimki,
)

#: Schemat `informacja`, skrócony do pozycji, o które pyta kryterium przyimkowe.
#: Rama rzeczownika jest tą połową, którą świadek ramowy wskazuje, więc wpis stąd
#: jest zarazem przykładem, na którym stoi wniosek tamtego dokumentu. `cp(że)` stoi
#: w nim po to, żeby pozycja nieprzyimkowa miała czym się nie dopasować.
INFORMACJA = " pewny: : : : {prepnp(o,loc);cp(że)} + {possp} + {prepnp(dla,gen)}"

#: Schemat, w którym przyimek stoi zleksykalizowany: `czekać na czas dobry` żąda
#: `na` wraz z rzeczownikiem, który przy nim stoi, a nie przy dowolnym.
ZLEKSYKALIZOWANY = " pewny: _: : imperf: subj{np(str)} + {lex(prepnp(na,acc),pl,'czas',natr)}"

#: Schemat, w którym przyimek stoi w pozycji podmiotu. Podmiot ma u olskiego
#: własną produkcję, a nie pozycję ramy, więc żądaniem o gospodarzu nie jest.
W_PODMIOCIE = " pewny: _: : imperf: subj{prepnp(o,loc)} + {np(str)}"


def test_pozycja_zleksykalizowana_nie_rozcina_się_na_swoim_plusie():
    #  Plus rozdziela pozycje, a stoi też wewnątrz pozycji zleksykalizowanej, w
    #  nawiasach. Rozbiór po samym plusie robi z jednej pozycji dwie i drugiej z
    #  nich urywa etykietę, więc pozycja podmiotu przestaje wyglądać na podmiot.
    schemat = "subj{np(str)} + {lex(np(str),sg,'czas',atr({adjp(agr)}+{np(gen)}))}"
    assert [etykieta for etykieta, _ in pozycje(schemat)] == ["subj", ""]


@pytest.mark.parametrize(
    ("schemat", "biernik"),
    [
        ("subj{np(str)} + {xp(locat)}", False),
        ("subj{np(str)} + obj{np(str)}", True),
        ("subj{np(str)} + {np(acc)}", True),
        #  Biernik bywa u Walentego pozycją bez etykiety obj i bywa schowany w
        #  pozycji zleksykalizowanej; jedno i drugie jest dopełnieniem, którego
        #  olski ma nie odbierać.
        ("subj{np(str)} + {lex(np(str),sg,'ochota',natr)}", True),
        #  Przypadek strukturalny w pozycji podmiotu jest mianownikiem, a nie
        #  biernikiem, więc sam podmiot dopełnienia nie zapowiada.
        ("subj,controller{np(str)} + controllee{infp(_)}", False),
    ],
)
def test_biernik_liczy_się_tylko_w_pozycji_niepodmiotowej(schemat, biernik):
    assert bierze([schemat], BIERNIK) is biernik


@pytest.mark.parametrize(
    ("schemat", "bierze_go"),
    [
        ("subj,controller{np(str)} + controllee{infp(_)}", True),
        #  Aspekt stoi u Walentego w nawiasie i olski o niego nie pyta, więc
        #  bezokolicznik dokonany jest tą samą pozycją co dowolny.
        ("subj,controller{np(str)} + controllee{np(str);infp(perf)}", True),
        #  Kontroluje celownik, czyli wykonawcą jest ten, komu kazano, i takiego
        #  zdania ta gramatyka nie ma czym zapisać.
        ("subj{np(str)} + controller{np(dat)} + controllee{infp(_)}", False),
        ("subj{np(str)} + obj{np(str)}", False),
    ],
)
def test_bezokolicznik_liczy_się_tylko_pod_kontrolą_podmiotu(schemat, bierze_go):
    assert bierze_bezokolicznik_podmiotu([schemat]) is bierze_go


@pytest.mark.parametrize(
    ("schemat", "kształty", "bierze_go"),
    [
        (" pewny: _: : imperf: subj{np(str)} + {np(dat)}", CELOWNIK, True),
        (" pewny: _: : imperf: subj{np(str)} + obj{np(gen)}", DOPEŁNIACZ, True),
        #  Dopełniacz cząstkowy realizuje polszczyzna tą samą formą, co żądany
        #  ramą, więc jest tą samą pozycją: `potrzebować` ma w Walentym `np(part)`.
        (" pewny: _: : imperf: subj{np(str)} + {np(part)}", DOPEŁNIACZ, True),
        #  Schemat ze zleksykalizowaną pozycją jest zwrotem — `mieć komuś za złe` —
        #  a celownik należy w nim do zwrotu, a nie do ramy lematu.
        (
            " pewny: _: : imperf: subj{np(str)} + {np(dat)}"
            " + {lex(prepadjp(za,acc),sg,n,pos,'zły',natr)}",
            CELOWNIK,
            False,
        ),
        #  Kwalifikator dawnej polszczyzny odsyła schemat poza ten rejestr tak
        #  samo, jak odsyła go w kolumnie przyimków (`BRANE`).
        (" archaiczny: _: : imperf: subj{np(str)} + {np(dat)}", CELOWNIK, False),
        #  Podmiotu to pytanie nie widzi, bo podmiot ma u olskiego własną produkcję.
        (" pewny: _: : imperf: subj{np(dat)}", CELOWNIK, False),
    ],
)
def test_dopełnienie_poza_biernikiem_liczy_się_z_samego_schematu_o_ramie(
    schemat, kształty, bierze_go
):
    """Zdanie twierdzące ramę poszerza, więc bierze mniej schematów niż ujemne.

    Kryterium ujemne — o bierniku — pyta wszystkich schematów, bo policzone za
    szeroko zostawia lemat przy ramie domyślnej. Tutaj ta sama pomyłka wpuszcza
    dopełnienie, którego polszczyzna przy tym czasowniku nie stawia, więc odpada
    cały schemat mówiący o zwrocie albo o polszczyźnie spoza tego rejestru.
    """
    assert bierze_ramą([schemat], kształty) is bierze_go


@pytest.mark.parametrize(
    ("schematy", "para"),
    [
        ([" pewny: _: : imperf: subj{np(str)} + {np(dat)} + {np(str)}"], True),
        ([" pewny: _: : imperf: subj{np(str)} + {np(dat)} + {cp(int)}"], True),
        #  Celownik z jednego schematu i biernik z drugiego pary nie dowodzą:
        #  lemat bierze wtedy każdy z nich osobno i żaden schemat nie stawia ich
        #  obok siebie.
        (
            [
                " pewny: _: : imperf: subj{np(str)} + {np(dat)}",
                " pewny: _: : imperf: subj{np(str)} + {np(str)}",
            ],
            False,
        ),
        #  Sąsiad, którego olski nie ma pozycją ramy, pary nie robi: wyrażenie
        #  przyimkowe przyłącza się u niego za darmo.
        ([" pewny: _: : imperf: subj{np(str)} + {np(dat)} + {prepnp(o,loc)}"], False),
        #  Jedna pozycja oferująca celownik albo pytanie — `dziwić się` — jest
        #  wyborem, a nie parą, więc kształt trafiony drugi raz w tej samej
        #  pozycji nie liczy się za sąsiada.
        ([" pewny: _: : imperf: subj{np(str)} + {np(dat);cp(int)}"], False),
    ],
)
def test_parę_liczy_się_z_jednego_schematu_i_z_dwóch_jego_pozycji(schematy, para):
    assert bierze_celownik_przy_wypełnieniu(schematy) is para


def test_rama_zbiera_pozycje_niepodmiotowe_i_pomija_nieprzyimkowe():
    assert przyimki([INFORMACJA]) == frozenset({"o", "dla"})


def test_przyimek_zleksykalizowany_nie_jest_żądaniem_ramy():
    assert przyimki([ZLEKSYKALIZOWANY]) == frozenset()


def test_przyimek_w_podmiocie_nie_jest_żądaniem_o_gospodarzu():
    assert przyimki([W_PODMIOCIE]) == frozenset()


@pytest.mark.parametrize(
    ("kwalifikator", "żądane"),
    [("potoczny", frozenset({"o"})), ("archaiczny", frozenset())],
)
def test_kwalifikator_rejestru_zostaje_a_kwalifikator_dawnej_polszczyzny_odpada(
    kwalifikator, żądane
):
    """Para, na której `BRANE` jest wyborem, a nie listą wszystkiego.

    Oba kwalifikatory odsyłają schemat poza polszczyznę ogólną, a odsyłają go w
    różne miejsca: `potoczny` mówi o rejestrze i schemat zostaje schematem,
    `archaiczny` mówi, że nikt tak nie napisze. Warunek pisany bez tej różnicy
    przechodzi wszystko albo odrzuca oba.
    """
    assert przyimki([f" {kwalifikator}: : : : {{prepnp(o,loc)}}"]) == żądane


def test_tylko_pewne_zawęża_do_schematów_niewątpliwych():
    wątpliwy = [" wątpliwy: : : : {prepnp(o,loc)}"]
    assert przyimki(wątpliwy) == frozenset({"o"})
    assert przyimki(wątpliwy, tylko_pewne=True) == frozenset()


def _pliki(tmp_path, czasowniki: str, rzeczowniki: str = ""):
    """Para plików wejściowych, każdy z podanymi wierszami."""
    (tmp_path / "verbs.txt").write_text(czasowniki, encoding="utf-8")
    (tmp_path / "nouns.txt").write_text(rzeczowniki, encoding="utf-8")
    return tmp_path / "verbs.txt", tmp_path / "nouns.txt"


def test_do_leksykonu_wchodzi_słowo_wraz_ze_zdaniami_które_są_o_nim_prawdziwe(tmp_path):
    #  Lemat, o którym prawdziwe nie jest żadne z tych zdań i którego rama nie żąda
    #  żadnego przyimka, nie wchodzi: zostaje mu rama domyślna, a wpis, który tylko
    #  ją powtarza, niczego nie rozstrzyga. `abonować` jest tu tym wpisem.
    #  Zwrotność schodzi z lematu do klasy słowa, bo Morfeusz jej w lemacie nie
    #  ma: cząstka jest u olskiego osobnym tokenem.
    #  Oba zdania naraz są tu wpisem jednym, a nie dwoma, bo słowo jest jedno.
    czasowniki, rzeczowniki = _pliki(
        tmp_path,
        "% komentarz\n"
        "działać: pewny: _: : imperf: subj{np(str)} + {xp(locat)}\n"
        "abonować: pewny: _: : imperf: subj{np(str)} + obj{np(str)}\n"
        "bawić się: pewny: _: : imperf: subj{np(str)} + {np(inst)}\n"
        "chcieć: pewny: _: : imperf: subj,controller{np(str)} + controllee{np(str);infp(_)}\n"
        "bać się: pewny: _: : imperf: subj,controller{np(str)} + controllee{infp(_)}\n",
    )
    assert leksykon(czasowniki, rzeczowniki) == [
        ("bawić", CZASOWNIK_ZWROTNY, (NIE_BIERZE_BIERNIKA,), frozenset()),
        ("bać", CZASOWNIK_ZWROTNY, (NIE_BIERZE_BIERNIKA, BIERZE_BEZOKOLICZNIK), frozenset()),
        ("chcieć", CZASOWNIK, (BIERZE_BEZOKOLICZNIK,), frozenset()),
        ("działać", CZASOWNIK, (NIE_BIERZE_BIERNIKA,), frozenset()),
    ]


def test_słowo_bez_ani_jednego_zdania_wchodzi_do_leksykonu_samym_przyimkiem(tmp_path):
    """Warunek wejścia jest sumą dwóch, a nie samymi zdaniami.

    Rzeczownik żadnego zdania tego leksykonu nie orzeka — mówią one o bierniku,
    o bezokoliczniku i o zdaniu podrzędnym — więc pytany o same zdania nie wszedłby
    do pliku ani razu, a kolumna przyimków zostałaby pusta dokładnie po tej
    stronie, po której świadek ramowy wskazuje. Tak samo wchodzi czasownik o ramie
    domyślnej, bo wetem jest u tego świadka jego przyimek, a nie jego zdania.

    `krzesło` jest tu słowem, którego rama przyimka nie żąda, i ono nie wchodzi.
    """
    czasowniki, rzeczowniki = _pliki(
        tmp_path,
        "mówić: pewny: _: : imperf: subj{np(str)} + obj{np(str)} + {prepnp(o,loc)}\n",
        "informacja: pewny: : : : {prepnp(o,loc)} + {prepnp(dla,gen)}\n"
        "krzesło: pewny: : : : {np(gen)}\n",
    )
    assert leksykon(czasowniki, rzeczowniki) == [
        ("informacja", RZECZOWNIK, (), frozenset({"o", "dla"})),
        ("mówić", CZASOWNIK, (), frozenset({"o"})),
    ]
