"""Te własności bazy sądów, bez których sonda nad nią wydaje liczbę nieprawdziwą.

Baza jest plikiem pisanym ręką, więc psuje się inaczej niż kod: dwa zdania
wklejone do jednego wpisu wywracają mianownik po cichu, sąd bez powodu jest
zdaniem, którego nikt nie sprawdzi, a znalezisko wpisane dwa razy liczy jeden
sąd dwa razy. Wiersz werdyktu bramką nie jest: gramatyka, która się ruszyła,
zmienia klasę wpisu, a nie jego prawdziwość.

Nowe znaleziska mają dwie własności, których wydruk sam nie zdradza:
ocenione nie wracają, bo na tym stoi cały obieg,
a porządek jest odciskiem, bo pierwszych czterdzieści po plikach
byłoby pierwszym plikiem korpusu.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.sądy import (
    BUDOWA,
    FAŁSZYWE,
    NAD_CZYSTYM,
    NIECZYTANE,
    POTWIERDZONE,
    PRZEOCZONE,
    PRZYŁĄCZENIE,
    PUSTY,
    ROLE,
    TRAFNE,
    ZDJĘTE,
    Sąd,
    czytaj,
    kształt,
    nowe,
    zapisz,
    zestaw,
    znaleziska,
)
from olski.segmentacja import sentences
from olski.werdykt import ODNIESIENIE, POPRAWKA, WIELOZNACZNE, nad_tekstem

WPISY = czytaj()
PRZECZYTANE = [wpis for wpis in WPISY if wpis.przeczytany]


def test_baza_ma_przeczytane_wpisy():
    #  Plik pusty przechodzi każdy test niżej, bo parametryzacja nie ma wtedy
    #  czego zebrać, a sonda nad nim wypisuje same zera.
    assert PRZECZYTANE


@pytest.mark.parametrize("wpis", WPISY, ids=lambda wpis: wpis.zdanie[:40])
def test_wpis_jest_jednym_zdaniem(wpis):
    assert len(sentences(wpis.zdanie)) == 1


@pytest.mark.parametrize("wpis", PRZECZYTANE, ids=lambda wpis: wpis.zdanie[:40])
def test_sąd_niesie_powód(wpis):
    assert wpis.powód


def test_znalezisko_stoi_w_bazie_raz():
    #  Drugi wpis o tym samym znalezisku liczyłby jeden sąd dwa razy, a przebieg
    #  zdejmowałby znalezisko po którymkolwiek z nich.
    klucze = [wpis.klucz for wpis in WPISY]
    assert len(klucze) == len(set(klucze))


#: Zdania, po jednym na klasę, wraz z tym, czym są dla olskiego dzisiaj.
#: ``Czekają nagrody.`` stoi w bazie i ma dwa odczytania; ``Chałka przewyższa
#: zwykłą bułkę.`` ma jedno, bo przypadki obu grup się nie zlewają
#: (docs/subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego);
#: ``Nowa program`` nie ma wyprowadzenia, bo formy się nie zgadzają.
ZGŁOSZONE = "Czekają nagrody."
JEDNO_ODCZYTANIE = "Chałka przewyższa zwykłą bułkę."
ODRZUCONE = "Nowa program zapisuje ustawienia."


def wpis(zdanie: str, sąd: str, znalezisko: str = WIELOZNACZNE, kontekst=()) -> Sąd:
    return Sąd(
        plik="",
        kontekst=kontekst,
        zdanie=zdanie,
        znalezisko=znalezisko,
        werdykt="",
        sąd=sąd,
        powód="powód",
    )


@pytest.mark.parametrize(
    ("sąd", "zdanie", "klasa"),
    [
        (TRAFNE, ZGŁOSZONE, POTWIERDZONE),
        (FAŁSZYWE, ZGŁOSZONE, NAD_CZYSTYM),
        (TRAFNE, JEDNO_ODCZYTANIE, PRZEOCZONE),
        (FAŁSZYWE, JEDNO_ODCZYTANIE, ZDJĘTE),
        (FAŁSZYWE, ODRZUCONE, NIECZYTANE),
    ],
)
def test_klasa_bierze_się_z_sądu_i_z_dzisiejszego_znaleziska(sąd, zdanie, klasa):
    #  Para „przeoczone” i „zdjęte” jest tu najdroższa: obie znaczą, że
    #  znaleziska nie ma, a mówią rzecz przeciwną, więc zamienione miejscami
    #  odwracają wniosek, który sonda wydaje, i nie widać tego po wydruku.
    assert zestaw(wpis(zdanie, sąd)).klasa == klasa


def test_odniesienie_ocenia_się_za_swoim_akapitem():
    #  Zaimek wskazuje na dwie rzeczy dopiero przy zdaniu obok, więc wpis bez
    #  kontekstu liczyłby to znalezisko jako zdjęte, choć pada.
    z = wpis("Są one czerwone.", TRAFNE, ODNIESIENIE, kontekst=("Maki rosną w garnkach.",))
    assert zestaw(z).klasa == POTWIERDZONE


def test_poprawka_pada_nad_zdaniem_nieczytanym():
    zdanie = 'Przepisem "Zasad techniki prawodawczej" jest ustawa.'
    assert zestaw(wpis(zdanie, TRAFNE, POPRAWKA)).klasa == POTWIERDZONE


@pytest.mark.parametrize(
    ("zdanie", "oczekiwany"),
    [
        (ZGŁOSZONE, ROLE),
        ("Janina Michaluk leży w szpitalu w Gryficach.", f"{PRZYŁĄCZENIE}+{ROLE}"),
        (JEDNO_ODCZYTANIE, ""),
    ],
)
def test_kształt_nazywa_to_czym_czytania_się_różnią(zdanie, oczekiwany):
    #  Zdanie o szpitalu niesie i przyłączenie, i rolę spoza wyrażenia
    #  przyimkowego, więc kształt jest złożeniem obu, a nie samym przyłączeniem.
    assert kształt(nad_tekstem(zdanie)[0].werdykt) == oczekiwany


def test_budowa_jest_osobnym_kształtem():
    zdanie = "Zainteresowana rada gminy wydaje przepis."
    assert BUDOWA in kształt(nad_tekstem(zdanie)[0].werdykt).split("+")


@pytest.fixture
def proza(tmp_path):
    (tmp_path / "a.txt").write_text(f"{JEDNO_ODCZYTANIE} {ODRZUCONE}\n", encoding="utf-8")
    (tmp_path / "b.txt").write_text(f"{ZGŁOSZONE}\n", encoding="utf-8")
    return tmp_path


def test_znaleziskiem_jest_zdanie_zgłoszone_wraz_z_nazwą_i_akapitem(proza):
    lista = znaleziska(proza)
    assert [(z.zdanie, z.znalezisko, z.kontekst) for z in lista] == [
        (ZGŁOSZONE, WIELOZNACZNE, ())
    ]


def test_porządek_znalezisk_jest_odciskiem_a_nie_kolejnością_plików(tmp_path):
    (tmp_path / "a.txt").write_text(f"{ZGŁOSZONE}\n", encoding="utf-8")
    (tmp_path / "b.txt").write_text("Koszt samej szynki przewyższa koszt szynki.\n", encoding="utf-8")
    lista = znaleziska(tmp_path)
    assert len(lista) == 2
    assert [z.odcisk for z in lista] == sorted(z.odcisk for z in lista)


def test_ocenione_znalezisko_nie_wraca(proza):
    lista = znaleziska(proza)
    assert nowe(lista, [(ZGŁOSZONE, WIELOZNACZNE)]) == []
    assert nowe(lista, [(ZGŁOSZONE, POPRAWKA)]) == lista


def test_zdanie_powtórzone_w_korpusie_wychodzi_raz(tmp_path):
    (tmp_path / "a.txt").write_text(f"{ZGŁOSZONE}\n", encoding="utf-8")
    (tmp_path / "b.txt").write_text(f"{ZGŁOSZONE}\n", encoding="utf-8")
    assert len(nowe(znaleziska(tmp_path), [])) == 1


def test_wypisane_znalezisko_czyta_się_z_powrotem_jako_wpis_czekający(proza, tmp_path):
    #  Ten obieg stoi na tym, że wydruk `--nowe` jest po przeniesieniu wpisem bazy.
    plik = tmp_path / "nowe.txt"
    plik.write_text(zapisz(znaleziska(proza)), encoding="utf-8")
    (wpis,) = czytaj(plik)
    assert (wpis.zdanie, wpis.znalezisko, wpis.sąd) == (ZGŁOSZONE, WIELOZNACZNE, PUSTY)
    assert not wpis.przeczytany
