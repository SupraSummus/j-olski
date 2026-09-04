"""To, co `olski-check` obiecuje wołającemu spoza swojego wydruku.

Wydruku wiersz po wierszu ten plik nie przepisuje: kosztowałby przy każdej
zmianie układu i nie bronił niczego, czego by czytelnik nie zobaczył. Wiersze
przepisane do dokumentów pilnuje ``tests/test_wydruki.py``, a co robi warstwa
rozstrzygająca dopisana obok werdyktu — ``tests/test_rozstrzyganie.py``.

Zostają cztery rzeczy, których nie widzi ani czytelnik wydruku, ani tamte pliki.
Pierwszą jest to, o których zdaniach wydruk mówi, a które przemilcza.
Bloku, którego nie ma, żaden dokument nie wkleja,
więc wydruk zgłaszający każde zdanie z powrotem przechodzi tamten plik.
Drugą jest ostatni wiersz, bo liczbę fragmentów bierze z niego
``docs/extraction.md``, a formatu tego wiersza nie sprawdzało nic.
Trzecią są kody wyjścia, bo widzi je tylko ten, kto komendę wpina w potok:
znalezisko daje jeden, a wołanie, którego nie da się wykonać, dwa,
i te dwie odpowiedzi nie mogą się zlać w jedną.
Zdanie, którego olski nie wyprowadza, nie jest znaleziskiem
(``docs/subset.md``), więc kodu nie rusza.
Czwartą jest to, czym komenda czyta plik: dokument dochodzi do gramatyki bez
swojego aparatu, a plik prozy tak, jak leży, i wydruk nie mówi, którą drogą
tekst przyszedł.
"""

import pytest

pytest.importorskip("morfeusz2")

import olski.check

#: Tekst o jednym zdaniu jednoznacznym, jednym odrzuconym i jednym nagłówku,
#: czyli napisie, którego nic nie punktuje jako zdania i który podsumowanie
#: liczy osobno.
MIESZANY = "Co działa\n\nZapisz plik. Nowa program zapisuje ustawienia."


def _podsumowanie(capsys) -> str:
    """Ostatni wiersz wydruku, czyli ten, po który przychodzi dokument."""
    return capsys.readouterr().out.splitlines()[-1]


@pytest.mark.parametrize(
    ("flagi", "wypisane"),
    [
        #  Bez flagi nie ma tu ani jednego znaleziska, więc zostaje sam ostatni wiersz.
        ((), ()),
        (("--zatrzymania",), ("Co działa", "Nowa program zapisuje ustawienia.")),
        (("--readings",), ("Zapisz plik.",)),
    ],
)
def test_wydruk_nazywa_zdania_o_których_przebieg_ma_wiersz(flagi, wypisane, capsys):
    """Flaga dokłada wiersze i tym samym dokłada zdania (`_wiersze` w `olski/check.py`)."""
    assert olski.check.main([*flagi, "-c", MIESZANY]) == 0
    nagłówki = [w for w in capsys.readouterr().out.splitlines() if w.startswith("<text>: ")]
    assert nagłówki == [f"<text>: {zdanie}" for zdanie in wypisane]


def test_ostatni_wiersz_wydruku_niesie_liczbę_fragmentów(capsys):
    """Z tego wiersza bierze liczbę fragmentów `docs/extraction.md`."""
    olski.check.main(["-c", MIESZANY])
    assert "fragmenty, których nic nie punktuje jako zdania: 1" in _podsumowanie(capsys)


def test_kod_jeden_dostaje_każde_znalezisko_a_odrzucenie_bez_poprawki_nie():
    """Kod wyjścia niesie znaleziska, a zdanie poza gramatyką znaleziskiem nie jest.

    Zdanie naprawialne stoi tu obok wieloznacznego, bo kod wyjścia jest pytaniem
    o znalezisko, a nie o wieloznaczność (`Podsumowanie.znalezisk`).
    """
    assert olski.check.main(["-c", "Program otwierający się psuje."]) == 1
    assert olski.check.main(["-c", 'Przepisem "Zasad techniki prawodawczej" jest ustawa.']) == 1
    assert olski.check.main(["-c", "Nowa program zapisuje ustawienia."]) == 0


def test_tekst_bez_fragmentów_nie_mówi_o_nich_ani_słowa(capsys):
    """Wiersz o fragmentach pada wtedy, gdy tekst je ma, a nie zawsze."""
    assert olski.check.main(["-c", "Zapisz plik."]) == 0
    assert "fragment" not in _podsumowanie(capsys)


#: Nagłówek i znacznik w środku zdania, czyli aparat, który dokument niesie, a
#: proza nie. Wyekstrahowany daje jedno zdanie i nic poza nim; przeczytany
#: wprost daje gwiazdki w zdaniu i nagłówek policzony jako fragment.
DOKUMENT = "# Co działa\n\nZapisz **plik**.\n"


def test_dokument_dochodzi_do_gramatyki_bez_swojego_aparatu(capsys, tmp_path):
    plik = tmp_path / "notatka.md"
    plik.write_text(DOKUMENT, encoding="utf-8")
    #  Zdanie wyekstrahowane olski wyprowadza, więc bez flagi wydruk o nim milczy.
    assert olski.check.main(["--readings", str(plik)]) == 0
    wypisane = capsys.readouterr().out.splitlines()
    assert f"{plik}: Zapisz plik." in wypisane
    assert wypisane[-1].startswith("zdań: 1;") and "fragment" not in wypisane[-1]


def test_plik_o_nieznanym_rozszerzeniu_dochodzi_tak_jak_stoi(capsys, tmp_path):
    """Ekstrakcja idzie za rozszerzeniem, a nie za tym, co w pliku wygląda na aparat."""
    plik = tmp_path / "notatka.txt"
    plik.write_text(DOKUMENT, encoding="utf-8")
    assert olski.check.main(["--zatrzymania", str(plik)]) == 0
    wypisane = capsys.readouterr().out.splitlines()
    assert f"{plik}: Zapisz **plik**." in wypisane
    assert "fragmenty, których nic nie punktuje jako zdania: 1" in wypisane[-1]


#: Moduł, którego docstring jest zdaniem, a kod pod nim nie jest prozą niczyją.
#: Nazwa i przypisanie są tym, co ta ekstrakcja zostawia za sobą, więc do
#: gramatyki nie dochodzi ani jedno, ani drugie.
MODUŁ = '''"""Zapisz plik."""\n\nSTAŁA = 1\n'''


def test_moduł_dochodzi_do_gramatyki_swoim_docstringiem(capsys, tmp_path):
    """Docstring jest prozą tych samych reguł co dokument."""
    plik = tmp_path / "moduł.py"
    plik.write_text(MODUŁ, encoding="utf-8")
    assert olski.check.main(["--readings", str(plik)]) == 0
    wypisane = capsys.readouterr().out.splitlines()
    assert f"{plik}: Zapisz plik." in wypisane
    assert wypisane[-1].startswith("zdań: 1;") and "fragment" not in wypisane[-1]


def test_ścieżka_której_nie_da_się_przeczytać_daje_kod_dwa(capsys, tmp_path):
    assert olski.check.main([str(tmp_path / "nie-ma.txt")]) == 2
    assert "nie udało się przeczytać" in capsys.readouterr().err


def test_wołanie_bez_zdania_do_sprawdzenia_daje_kod_dwa(capsys):
    """Bez ścieżki i bez ``-c`` komenda nie ma o czym orzekać, więc nie orzeka."""
    assert olski.check.main([]) == 2
    assert "usage" in capsys.readouterr().err
