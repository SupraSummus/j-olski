"""Te własności sondy nad świadkiem kontekstowym, bez których jej liczba kłamie.

Liczb sonda nie ma czym bronić: wychodzą z korpusu, którego repozytorium nie
trzyma, i zmieniają się z każdą zmianą tego, co ``pytania`` w
``olski/wieloznaczność.py`` liczy za pozycję. Pięć rzeczy jest innych, bo psują
liczbę po cichu i nie zgłasza ich nic.

Populacja ma nie wychodzić z werdyktu, bo gramatyka odrzuca w tym rejestrze
prawie każde zdanie, a zasięg zmierzony na werdyktach jest wtedy liczbą o
gramatyce.

Rozkład zasięgu na dwie przyczyny jest tym, po co ta sonda jest: milczenie nad
zdaniem pierwszym w akapicie i milczenie nad zdaniem, które sąsiada ma, mówią o
czym innym, a zsumowane nie mówią o niczym.

Wariant bez granicy akapitu ma czytać dokument wstecz i tylko wstecz, bo świadek
liczący zdania za sobą mierzyłby coś, czego czytelnik nie ma.

Wariant reguły kandydata ma mierzyć regułę inną niż wypuszczana, bo wycena, w
której oba wiersze wychodzą z jednej reguły, wygląda dokładnie jak wycena.

Mianownik ma stać na przyłączeniach, a nie na zdaniach: zdanie miewa ich kilka.
"""

import pytest

pytest.importorskip("morfeusz2")

from pathlib import Path

from olski.subset import check
from sonda.powtórzenie import przebieg

#: Akapit, w którym fraza stoi dwa razy i za pierwszym razem przy rzeczowniku,
#: obok akapitu drugiego, gdzie to samo zdanie stoi bez niczego przed sobą.
#: Granica akapitu jest tu całą różnicą między dwoma wariantami sondy.
TEKST = """\
Wystąpiła awaria w systemie. Operator zgłosił awarię w systemie.

Operator zgłosił awarię w systemie.
"""


@pytest.fixture
def pomiar(tmp_path: Path):
    (tmp_path / "rejestr.txt").write_text(TEKST, encoding="utf-8")
    return przebieg([tmp_path / "rejestr.txt"])


def test_zasięg_rozkłada_się_na_zdania_z_sąsiedztwem_i_bez_niego(pomiar):
    """Dwie przyczyny milczenia, bo jedna liczba nie mówi, która przeważyła."""
    assert pomiar.zdań == 3
    assert pomiar.bez_sąsiedztwa == 2, "pierwsze zdanie każdego z dwóch akapitów"
    assert pomiar.przyłączeń_z_sąsiedztwem == 1


def test_granica_akapitu_odbiera_świadkowi_zdanie_z_akapitu_obok(pomiar):
    """Cena tej granicy jest różnicą między wariantami, więc warianty mają się różnić.

    Zdanie trzecie jest znak w znak drugim i stoi w akapicie własnym, więc
    świadek odpowiada nad nim tylko wtedy, gdy granicy nie ma.
    """
    assert len(pomiar.odpowiedzi) == 1
    assert len(pomiar.odpowiedzi_bez_granicy) == 2


def test_populacja_nie_wychodzi_z_werdyktu(tmp_path: Path):
    """Zdanie, którego gramatyka nie przyjmuje, ma świadka o co zapytać.

    Populacja wzięta z werdyktów daje nad tym rejestrem 38 pytań na 2 915 zdań
    (``docs/disambiguation.md``), więc zasięg mierzony na niej jest w większości
    liczbą o gramatyce. Sonda wpięta z powrotem w ``check`` przechodzi każdy inny
    test w tym pliku i wypisuje zasięg z powrotem bliski zeru.

    Zdanie jest z korpusu audytowego i odrzucone stoi tu w asercji: gramatyka,
    która je przyjmie, odbiera temu testowi dowód, a nie tylko materiał.
    """
    odrzucone = "Zabronione jest tworzenie opisów w 1 osobie.\n"
    (tmp_path / "rejestr.txt").write_text(odrzucone, encoding="utf-8")
    (werdykt,) = check(odrzucone)
    assert werdykt.result.status == "rejected"
    assert przebieg([tmp_path / "rejestr.txt"]).przyłączeń == 1


def test_wariant_bez_granicy_czyta_wstecz_a_nie_w_obie_strony(tmp_path: Path):
    """Zdanie, którego czytelnik jeszcze nie przeczytał, dowodem nie jest.

    Dowód stoi tu za zdaniem spornym, a stoi bez czasownika przed frazą, więc sam
    pozycji przyłączeniowej nie niesie i o nic pytany nie jest. Sonda czytająca w
    obie strony rozstrzygnęłaby mimo to zdanie pierwsze.
    """
    odwrotnie = "Operator zgłosił awarię w systemie.\n\nAwaria w systemie.\n"
    (tmp_path / "rejestr.txt").write_text(odwrotnie, encoding="utf-8")
    pomiar = przebieg([tmp_path / "rejestr.txt"])
    assert pomiar.przyłączeń == 1, "drugie zdanie nie ma czasownika przed frazą"
    assert pomiar.odpowiedzi == []
    assert pomiar.odpowiedzi_bez_granicy == []


def test_wariant_reguły_kandydata_mierzy_regułę_inną_niż_wypuszczana(tmp_path: Path):
    """Trzy wiersze tej tabeli mają mierzyć trzy reguły, a nie trzy razy jedną.

    Wariant wpięty bez podstawienia ``kandydaci`` odpowiada tyle samo razy co
    reguła wypuszczana i wygląda przez to na wycenę, której nie ma. Łańcuch
    dopełniaczowy jest tu miejscem, w którym reguły się rozchodzą: świadek
    wypuszczany widzi w nim dwóch gospodarzy i milczy, a pytający o sąsiada
    bezpośredniego wskazuje ogon grupy (``docs/disambiguation.md``).
    """
    łańcuch = (
        "Opisano sposób wymiany danych z systemami zewnętrznymi. "
        "Wpływa to na sposób wymiany danych z systemem RIT.\n"
    )
    (tmp_path / "rejestr.txt").write_text(łańcuch, encoding="utf-8")
    pomiar = przebieg([tmp_path / "rejestr.txt"])
    assert pomiar.odpowiedzi_bez_granicy == []
    (odpowiedź,) = pomiar.warianty["sąsiad bezpośredni"]
    assert odpowiedź.rozstrzygnięcie.gospodarz == "danych"


def test_wariant_z_kopulą_wycenia_warunek_w_granicy_akapitu(tmp_path: Path):
    """Wiersz o kopuli ma mierzyć ten sam akapit co wiersz nad nim.

    Wariant wpięty poza granicą akapitu wypisałby cenę warunku nad inną
    populacją niż ta, w której ten warunek odbiera wskazanie, i różnica dwóch
    wierszy przestałaby być ceną czegokolwiek.
    """
    kopula = (
        "Wymaga się, aby opisy tworzone były w 3 osobie. "
        "Zabronione jest tworzenie opisów w 1 osobie.\n"
    )
    (tmp_path / "rejestr.txt").write_text(kopula, encoding="utf-8")
    pomiar = przebieg([tmp_path / "rejestr.txt"])
    assert pomiar.odpowiedzi == []
    (odpowiedź,) = pomiar.odpowiedzi_z_kopulą
    assert odpowiedź.rozstrzygnięcie.gospodarz == "jest"


def test_mianownik_liczy_przyłączenia_a_nie_zdania(tmp_path: Path):
    """Zdanie z dwoma wyrażeniami przyimkowymi stawia więcej niż jeden wybór.

    Liczby dokładnej nie ma w asercji celowo: ile pozycji stoi w tym zdaniu,
    rozstrzyga ``pytania`` w ``olski/wieloznaczność.py``, a ta sonda ma tylko nie
    zliczać ich po zdaniach — pomyłka o jeden mianownik przesuwa figurę, którą
    czyta dokument.
    """
    dwa = "Rozdział zawiera informacje o awariach w systemie.\n"
    (tmp_path / "rejestr.txt").write_text(dwa, encoding="utf-8")
    pomiar = przebieg([tmp_path / "rejestr.txt"])
    assert pomiar.zdań == 1
    assert pomiar.przyłączeń > 1
