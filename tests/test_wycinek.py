"""Te własności cięcia na wycinki, bez których rejestr przeczytanego kłamie.

Rejestr mówi, ile cudzej prozy ktoś przeczytał, a mówi to przez nazwy wycinków,
więc kłamie na dwa sposoby, których wydruk sam nie zdradza. Zdanie, którego nie
bierze żaden wycinek, nie zostanie przeczytane nigdy, choć rejestr dojdzie do
końca korpusu. Zdanie wzięte dwa razy wraca do sesji, która ma czytać prozę nową.
Nad rejestrem czyta się przy tym warstwę po warstwie, więc wycinek złożony z
dwóch warstw psuje ten podział, i to też widać dopiero po nazwach plików.
"""

import pytest

pytest.importorskip("morfeusz2")

from harness.wycinek import CEL, następny, przeczytane, wycinki


@pytest.fixture
def korpus(tmp_path):
    """Korpus dwuwarstwowy, w którym jeden plik jest dłuższy od całego wycinka."""
    for warstwa, ile in (("typ_a", 40), ("typ_b", 30)):
        for numer in range(1, 4):
            plik = tmp_path / warstwa / f"próbka/txt_{numer}.txt"
            plik.parent.mkdir(parents=True, exist_ok=True)
            plik.write_text("\n".join(f"Zdanie numer {i}." for i in range(ile)), encoding="utf-8")
    długi = tmp_path / "typ_a/próbka/txt_9.txt"
    długi.write_text("\n".join(f"Zdanie numer {i}." for i in range(CEL * 2 + 5)), encoding="utf-8")
    return tmp_path


def test_każde_zdanie_korpusu_wchodzi_do_dokładnie_jednego_wycinka(korpus):
    wzięte = [
        (kawałek.plik, numer)
        for wycinek in wycinki(korpus)
        for kawałek in wycinek.kawałki
        for numer in range(kawałek.od, kawałek.do + 1)
    ]
    assert len(wzięte) == len(set(wzięte))
    assert set(wzięte) == {
        (plik.relative_to(korpus), numer)
        for plik in korpus.rglob("*.txt")
        for numer in range(1, len(plik.read_text(encoding="utf-8").splitlines()) + 1)
    }


def test_wycinek_nie_przechodzi_przez_granicę_warstwy(korpus):
    for wycinek in wycinki(korpus):
        assert len({kawałek.plik.parts[0] for kawałek in wycinek.kawałki}) == 1


def test_plik_dłuższy_od_wycinka_tnie_się_na_zakresy_zdań(korpus):
    zakresy = sorted(
        (kawałek.od, kawałek.do)
        for wycinek in wycinki(korpus)
        for kawałek in wycinek.kawałki
        if kawałek.plik.name == "txt_9.txt"
    )
    assert zakresy == [(1, CEL), (CEL + 1, 2 * CEL), (2 * CEL + 1, 2 * CEL + 5)]


def test_plik_krótszy_od_wycinka_wchodzi_w_całości(korpus):
    """Cięcie w środku takiego pliku zabrałoby zdaniom po obu jego stronach kontekst."""
    długości = {"typ_a": 40, "typ_b": 30}
    for wycinek in wycinki(korpus):
        for kawałek in wycinek.kawałki:
            if kawałek.plik.name != "txt_9.txt":
                assert (kawałek.od, kawałek.do) == (1, długości[kawałek.plik.parts[0]])


def test_wycinek_z_rejestru_nie_wraca(korpus):
    wszystkie = wycinki(korpus)
    pierwszy = następny(wszystkie, set())
    assert następny(wszystkie, {pierwszy.od}) != pierwszy


def test_rejestru_którego_nie_ma_nikt_nie_czytał(tmp_path):
    assert przeczytane(tmp_path / "nie-ma-takiego.txt") == set()
