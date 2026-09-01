"""Trzy odpowiedzi, które werdykt dokłada nad rozbiorem, i podsumowanie nad tekstem.

O zdaniu przyjętym i o odrzuconym rozstrzyga gramatyka,
więc pyta o nie ``tests/test_subset.py``.
Fragment jest napisem, którego nikt nie napisał jako zdania,
a niedomknięcie zdaniem bez ostatniego znaku;
czemu granica między nimi biegnie tędy, wywodzi ``docs/extraction.md``.
Zatrzymanie nazywa formę, na której stanęła analiza zdania odrzuconego,
a po co ta odpowiedź jest, mówi ``docs/pisanie-po-olsku.md``.
Wszystkie trzy mówią o napisie autora, a nie o grafie segmentacji.

Czwarte pytanie jest o podsumowanie tekstu,
bo od niego zależy, czego pomiar pokrycia nie liczy jako zdania.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.segmentacja import morphology
from olski.werdykt import (
    FRAGMENT,
    NIEDOMKNIĘTE,
    Domknięcie,
    Podsumowanie,
    check,
    werdykt,
    zatrzymania,
)


#  Wołają je też pliki pytające o gramatykę, o las i o segmentację,
#  a kopia w każdym z nich rozjechałaby się po cichu.
#  Wyliczenia nie ma, bo plik warstwy dopisany do `tests/` wydłuża tę listę,
#  a nic o niej wtedy nie przypomina.
def verdict(text):
    found = check(text)
    assert len(found) == 1, f"expected one sentence, got {len(found)}"
    return found[0]


def role(werdykt):
    """Role czytań zdania o jednym zdaniu składowym, po słowniku na czytanie.

    Streszczeniem czytania jest krotka o słowniku na każde zdanie składowe
    (``describe`` w ``olski/parse/streszczenie.py``).
    Zdanie o dwóch składowych wywraca ten pomocnik,
    zamiast wyjść z niego samym składowym pierwszym.
    """
    return [jedno for (jedno,) in werdykt.readings]


def test_werdykt_niesie_zdanie_tak_jak_stoi_a_nie_graf_segmentacji():
    #  Morfeusz dzieli ktoś na kto i ś obok formy całej, więc jest to zdanie,
    #  które wypisywało się jako cztery słowa, choć stoją w nim trzy.
    assert verdict("Ktoś zapisał plik.").text == "Ktoś zapisał plik."


def test_fragment_bez_znaku_zamykajacego_nie_jest_zdaniem_odrzuconym():
    #  Nagłówek i pozycja listy dochodzą do olskiego jako akapity, a produkcja
    #  wypowiedzenie żąda na końcu kropki, więc odrzucone mierzyłyby ekstrakcję.
    assert verdict("Zapisywanie pliku").status == FRAGMENT
    assert verdict("Nowa program zapisuje ustawienia.").status == "rejected"


def test_napis_który_olski_czyta_po_domknięciu_nie_jest_fragmentem():
    """Fragment jest aparatem dokumentu, a to jest zdanie bez ostatniego znaku.

    Rozdział ten jest całym zyskiem z werdyktu `unclosed`: bez niego autor, który
    kropki nie postawił, dostawał odpowiedź, że nikt tego zdaniem nie napisał.
    """
    niedomknięte = verdict("Cena jest niska")
    assert niedomknięte.status == NIEDOMKNIĘTE
    assert niedomknięte.domknięcie == Domknięcie(".", 1)


def test_niedomknięte_pytanie_dostaje_pytajnik_a_nie_kropkę():
    #  Kropka stoi w DOMKNIĘCIA pierwsza, więc pytajnik wychodzi tylko tam, gdzie
    #  kropka czytania nie daje: PYTAJNIK bierze jeden znak, a KONIEC_ZDANIA trzy.
    assert verdict("Który program zapisuje ustawienia").domknięcie == Domknięcie("?", 1)


def test_domknięcie_wieloznaczne_też_jest_niedomknięciem_a_nie_fragmentem():
    """Warunkiem jest czytanie, a nie czytanie jedno.

    `Program zapisuje ustawienia w pliku.` wychodzi dwoma czytaniami, bo `w pliku`
    dochodzi raz do czasownika, a raz do dopełnienia. Brak kropki jest w tym
    napisie tym samym brakiem co wyżej, a warunek na jedno czytanie schowałby go
    pod odpowiedzią o wieloznaczności.
    """
    niedomknięte = verdict("Program zapisuje ustawienia w pliku")
    assert niedomknięte.status == NIEDOMKNIĘTE
    assert niedomknięte.domknięcie.czytań > 1


# --------------------------------------------------------------------------- #
# Zatrzymania, czyli miejsca, na których staje analiza
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("zdanie", "oczekiwane"),
    [
        #  Werdykt nazywa jedno miejsce, bo jedno jest końcem przedrostka, który
        #  się analizuje, a zdanie o kilkunastu wyrazach ma ich kilka i pierwsze
        #  zasłania resztę.
        ("Dokument nazywa role, w jakich ktoś czyta, a dla każdej: pytanie.", ("czyta", "a", ":")),
        ("Zapisz plik konfiguracyjny.", ()),
    ],
)
def test_zatrzymania_nazywają_każde_miejsce_a_nie_samo_pierwsze(zdanie, oczekiwane):
    assert zatrzymania(morphology(zdanie)) == oczekiwane


def test_analiza_wznawia_się_za_formą_zatrzymania_a_nie_na_niej():
    #  Usterka, którą to łapie: przebieg wznowiony na formie zatrzymania. Formy,
    #  której nie wzięła żadna analiza częściowa, nie weźmie też analiza zaczęta
    #  od niej, więc taki przebieg nazywałby ją bez końca.
    #  Oba zatrzymania stoją tu na spójniku i biorą się z przecinka przed nim,
    #  którego polszczyzna tam nie stawia (docs/subset.md). Drugiego nie znajdzie
    #  przebieg wznowiony na formie pierwszego, bo tamta forma nie ruszy się z
    #  miejsca, więc para jest tu całym pytaniem: jedno zatrzymanie przechodziłoby
    #  i wznowieniu błędnemu.
    zdanie = "Cena rośnie, i linter sprawdza tekst, i parser czyta tekst."
    assert zatrzymania(morphology(zdanie)) == ("i", "i")


def test_werdykt_bez_pytania_o_zatrzymanie_daje_ten_sam_status():
    #  Na tym stoi cała oszczędność: sonda różnicowa czyta z werdyktu sam status
    #  i po to o zatrzymanie nie pyta (``harness/ruch.py``).
    #  Zdanie odrzucone, bo tylko nad takim zatrzymanie w ogóle się liczy.
    zdanie = "Nowa program zapisuje ustawienia."
    segmenty = morphology(zdanie)
    pytany = werdykt(zdanie, segmenty)
    milczący = werdykt(zdanie, segmenty, zatrzymanie=False)
    assert (milczący.status, milczący.result.ile) == (pytany.status, pytany.result.ile)


def test_wyjaśnienie_odrzucenia_bez_zatrzymania_odmawia_zamiast_zmyślać():
    #  Usterka, którą to łapie: ``zatrzymanie`` jest ``None`` i wtedy, gdy analiza
    #  doszła do końca, i wtedy, gdy nikt nie pytał, więc wyjaśnienie czytające
    #  sam ten brak mówiłoby o zdaniu rzecz nieprawdziwą.
    zdanie = "Nowa program zapisuje ustawienia."
    milczący = werdykt(zdanie, morphology(zdanie), zatrzymanie=False)
    assert milczący.result.rejected
    with pytest.raises(ValueError, match="o zatrzymanie nie pytał"):
        milczący.explain()


def test_napis_bez_znaku_pyta_o_zatrzymanie_mimo_że_wołający_nie_prosił():
    #  Domknięcie stawia się nad analizą, która doszła do końca, a status napisu
    #  bez znaku od domknięcia zależy: flaga posłuchana tutaj dosłownie robi z
    #  niedomknięcia fragment.
    zdanie = "Cena jest niska"
    milczący = werdykt(zdanie, morphology(zdanie), zatrzymanie=False)
    assert milczący.status == NIEDOMKNIĘTE
    assert milczący.domknięcie == Domknięcie(".", 1)


# --------------------------------------------------------------------------- #
# Cały tekst, czyli werdykt na każde zdanie i podsumowanie nad nimi
# --------------------------------------------------------------------------- #


def test_niedomknięte_stoi_poza_mianownikiem_tak_samo_jak_fragment():
    """Domknięcia nie postawił nikt, więc zdaniem tekstu ten napis nie jest.

    Liczone w mianowniku podniosłoby go o nagłówek, który po domknięciu się
    wyprowadza, a `docs/extraction.md` mierzy tym mianownikiem podzbiór, a nie
    ekstrakcję.
    """
    podsumowanie = Podsumowanie.z_werdyktów(check("Cena jest niska\n\nZapisz plik."))
    assert (podsumowanie.olskie, podsumowanie.zdań) == (1, 1)
    assert podsumowanie.fragmentów == 1


def test_every_sentence_of_a_text_is_checked():
    verdicts = check("Zapisz plik. Nowa program zapisuje ustawienia.")
    assert [found.status for found in verdicts] == ["valid", "rejected"]


def test_podsumowanie_nie_liczy_fragmentu_ani_w_liczniku_ani_w_mianowniku():
    """Fragment nie jest zdaniem, więc tekst z nagłówkiem nie ma gorszego wyniku.

    Reguła ta ma jednego właściciela dlatego, że pytają o nią wołający po obu
    stronach repozytorium — wiersz poleceń i witryna — a policzona u każdego z
    nich osobno daje mianownik większy o nagłówek i czyta się jak pomiar.
    """
    podsumowanie = Podsumowanie.z_werdyktów(
        check("Co działa\n\nZapisz plik. Nowa program zapisuje ustawienia.")
    )
    assert (podsumowanie.olskie, podsumowanie.zdań) == (1, 2)
    assert (podsumowanie.z_czytaniem, podsumowanie.fragmentów) == (1, 1)
