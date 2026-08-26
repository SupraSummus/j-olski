"""To, co `olski-check` obiecuje wołającemu spoza swojego wydruku.

Wydruku wiersz po wierszu ten plik nie przepisuje: kosztowałby przy każdej
zmianie układu i nie bronił niczego, czego by czytelnik nie zobaczył. Wiersze
przepisane do dokumentów pilnuje ``tests/test_wydruki.py``, a co robi warstwa
rozstrzygająca dopisana obok werdyktu — ``tests/test_rozstrzyganie.py``.

Zostają dwie rzeczy, których nie widzi ani czytelnik wydruku, ani tamte pliki.
Pierwszą jest ostatni wiersz, bo liczbę fragmentów bierze z niego
``docs/extraction.md``, a formatu tego wiersza nie sprawdzało nic.
Drugą są kody wyjścia, bo widzi je tylko ten, kto komendę wpina w potok:
zdanie odrzucone daje jeden, a wołanie, którego nie da się wykonać, dwa,
i te dwie odpowiedzi nie mogą się zlać w jedną.
"""

import pytest

pytest.importorskip("morfeusz2")

import olski.check

#: Tekst o jednym zdaniu olskim, jednym odrzuconym i jednym nagłówku, czyli
#: fragmencie, którego podsumowanie nie liczy jako zdania.
MIESZANY = "Co działa\n\nZapisz plik. Nowa program zapisuje ustawienia."


def _podsumowanie(capsys) -> str:
    """Ostatni wiersz wydruku, czyli ten, po który przychodzi dokument."""
    return capsys.readouterr().out.splitlines()[-1]


def test_ostatni_wiersz_wydruku_niesie_liczbę_fragmentów(capsys):
    """Z tego wiersza bierze liczbę fragmentów `docs/extraction.md`."""
    assert olski.check.main(["-c", MIESZANY]) == 1
    ostatni = _podsumowanie(capsys)
    assert "olskie: 1 z 2 zdań" in ostatni
    assert "fragmenty, których nic nie punktuje jako zdania: 1" in ostatni


def test_tekst_bez_fragmentów_nie_mówi_o_nich_ani_słowa(capsys):
    """Wiersz o fragmentach pada wtedy, gdy tekst je ma, a nie zawsze."""
    assert olski.check.main(["-c", "Zapisz plik."]) == 0
    assert "fragment" not in _podsumowanie(capsys)


def test_ścieżka_której_nie_da_się_przeczytać_daje_kod_dwa(capsys, tmp_path):
    assert olski.check.main([str(tmp_path / "nie-ma.txt")]) == 2
    assert "nie udało się przeczytać" in capsys.readouterr().err


def test_wołanie_bez_zdania_do_sprawdzenia_daje_kod_dwa(capsys):
    """Bez ścieżki i bez ``-c`` komenda nie ma o czym orzekać, więc nie orzeka."""
    assert olski.check.main([]) == 2
    assert "usage" in capsys.readouterr().err
