"""Czego warstwa szukająca imiesłowów bez podmiotu ma nie zgłaszać.

Zgłasza ona imiesłów przysłówkowy stojący przy orzeczeniu bezosobowym, więc
sądem nietrywialnym jest tu każde milczenie: co jest głową okolicznika, dokąd
sięga zdanie, od którego imiesłów pożycza podmiot, i gdzie kończy się kształt,
a zaczyna znaczenie (``olski/imiesłowy.py``). Każdy z tych warunków, zdjęty
osobno, zamienia jedno z tych zdań w zgłoszenie, i to jest jedyny powód, dla
którego one tu stoją.

Zdania z usterką stoją w ``próba/usterki.txt``, a że zgłoszenie nad nimi pada i
nad ich poprawkami milczy, mówi ``python3 -m harness.usterki``; tutaj stoi to,
czego tamten przebieg nie pyta.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.imiesłowy import Imiesłów, imiesłowy_bez_podmiotu
from olski.werdykt import IMIESŁÓW_BEZ_PODMIOTU, check, nad_tekstem


def zgłoszenia(zdanie: str) -> tuple[Imiesłów, ...]:
    """Zgłoszenia nad tym jednym zdaniem, tą drogą, którą idzie ``olski-check``."""
    return imiesłowy_bez_podmiotu(check(zdanie)[0].result.readings)


def test_imiesłów_przy_orzeczeniu_bezosobowym_nazywa_obie_formy():
    """Wiersz ma powiedzieć autorowi, co z czym poprawić, a nie że coś jest nie tak."""
    assert zgłoszenia("Idąc do pracy, zgubiono klucze.") == (Imiesłów("Idąc", "zgubiono"),)


def test_predykatyw_daje_zgłoszenie_tak_samo_jak_forma_nieosobowa():
    #  Głowy orzeczenia bezosobowego są dwie i żadna z nich podmiotu nie ma, więc
    #  warunek stoi na roli, a nie na formie: zapytany o samo `imps` przemilczałby
    #  połowę tej roli, a `Trzeba` nazywa wykonawcę tak samo mało jak `zgubiono`.
    assert zgłoszenia("Trzeba czytać dokumenty, sprawdzając zgodność.") == (
        Imiesłów("sprawdzając", "Trzeba"),
    )


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Poprawka z korpusu usterek: `zgubiłem` niesie podmiot domyślny, więc
        #  imiesłów ma go skąd wziąć.
        "Idąc do pracy, zgubiłem klucze.",
        #  Granica, którą docs/subset.md stawia między kształtem zdania a
        #  znaczeniem słowa: deszcz do pracy nie chodzi, ale orzeka o tym
        #  znaczenie, a po składni zdanie jest w porządku, bo podmiot ma.
        "Idąc do pracy, padał deszcz.",
    ],
)
def test_zdanie_nadrzędne_z_podmiotem_zgłoszenia_nie_dostaje(zdanie: str):
    assert zgłoszenia(zdanie) == ()


def test_orzeczenie_bezosobowe_ze_składowego_obok_zgłoszenia_nie_daje():
    #  Imiesłów określa `śpiewał`, które podmiot ma, a `Zgubiono` stoi w składowym
    #  obok i podmiotu temu imiesłowowi nie odbiera. Bez podziału na składowe
    #  wystarczyłoby, żeby obie formy stały w jednym zdaniu.
    assert zgłoszenia("Zgubiono klucze, a Jan śpiewał, idąc do pracy.") == ()


def test_okolicznik_wyrażony_zdaniem_pod_spójnikiem_zgłoszenia_nie_daje():
    #  Ten sam symbol niesie okolicznik wyrażony zdaniem, a takie zdanie ma własny
    #  podmiot i od orzeczenia nadrzędnego niczego nie pożycza. Warunek postawiony
    #  na samym symbolu okolicznika zgłaszałby każde zdanie bezosobowe z takim
    #  okolicznikiem, czyli w tym rejestrze wiele.
    assert zgłoszenia("Trzeba wdrożyć ją szybko, aby jej efekty były widoczne.") == ()


def test_zgłoszenie_spod_flagi_nie_jest_znaleziskiem():
    """Flaga nie rusza kodu wyjścia, bo jej zgłoszenie nosi własną nazwę.

    Reguła za flagą czeka na sądy czytelnika, więc do liczby, po którą pyta
    ``olski-check``, wchodzić jej nie wolno; nazwa jest zarazem tym, pod czym
    ocenia ją baza sądów (``harness/sądy.py``).
    """
    zdanie = nad_tekstem("Idąc do pracy, zgubiono klucze.")[0]
    assert zdanie.zgłoszenia == (IMIESŁÓW_BEZ_PODMIOTU,)
    assert zdanie.znaleziska == ()
