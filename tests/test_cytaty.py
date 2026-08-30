"""Co odsiewa cytat od nazwy i czym wydruk cytatów jest, kiedy akapit się przesunie.

Komenda z ``harness/cytaty.py`` jest przyrządem porównawczym: czyta się nie ją
samą, tylko diff dwóch jej przebiegów. Skłamać może więc dwojako. Pominięte
zdanie jest tą jedną rzeczą, dla której ta komenda powstała, więc kryterium
sprawdza się od strony pominięcia, a nie od strony nazwy, która się prześlizgnie.
Kolejność wydruku jest drugą: posortowana zdaniem mówi o gramatyce, a kolejność
dokumentu mówiłaby też o tym, gdzie akapit stoi.
"""

from __future__ import annotations

import pytest

pytest.importorskip("morfeusz2")

from harness.cytaty import cytat, wstawki, wydruk

MARKDOWN = """\
Akapit ze wstawką `Program zapisuje ustawienia.` w środku.

- Pozycja listy ze wstawką `Plik jest tani.` w niej.

```text
Zdanie z bloku tekstowego.
```

```python
Zdanie z bloku pythonowego.
```
"""


def test_wstawki_schodzi_do_pozycji_listy_i_pomija_blok_o_innym_języku():
    #  Usterka, przed którą to stoi: wstawki szukane wzorcem po wierszach.
    #  Wzorzec nie schodzi do pozycji listy tak samo jak do akapitu, a ciąg
    #  backticków otwierający blok czyta jak wstawkę, więc bierze `python` razem
    #  z `text` i gubi wstawkę, o którą chodzi.
    assert list(wstawki(MARKDOWN)) == [
        "Program zapisuje ustawienia.",
        "Plik jest tani.",
        "Zdanie z bloku tekstowego.",
    ]


CYTATY = {
    "zdanie oznajmujące": ("Program zapisuje ustawienia.", True),
    "pytanie": ("Czym jest parser?", True),
    "zdanie jednowyrazowe": ("Wstaje.", True),
    "nazwa pliku": ("docs/subset.md", False),
    "nazwa w kodzie": ("Verdict.punktowane", False),
    "flaga": ("--readings", False),
    "wiersz wydruku": ("<text>: valid     Zapisz plik konfiguracyjny.", False),
    "zdanie niedomknięte": ("Program zapisuje ustawienia", False),
}


@pytest.mark.parametrize("rodzaj", sorted(CYTATY))
def test_cytatem_jest_zdanie_a_nie_nazwa(rodzaj):
    napis, spodziewane = CYTATY[rodzaj]
    assert cytat(napis) is spodziewane


def test_wydruk_idzie_zdaniem_a_nie_kolejnością_dokumentu(tmp_path):
    #  Ten sam plik z przestawionymi akapitami ma dać wydruk co do znaku ten sam,
    #  bo przestawiony akapit nie jest zmianą w tym, co gramatyka o zdaniu mówi.
    pierwszy, drugi = tmp_path / "przed", tmp_path / "po"
    for katalog in (pierwszy, drugi):
        katalog.mkdir()
    (pierwszy / "jeden.md").write_text(
        "`Plik jest tani.`\n\n`Program zapisuje ustawienia.`\n", encoding="utf-8"
    )
    (drugi / "jeden.md").write_text(
        "`Program zapisuje ustawienia.`\n\n`Plik jest tani.`\n", encoding="utf-8"
    )
    assert wydruk([pierwszy / "jeden.md"]) == wydruk([drugi / "jeden.md"])


def test_cytat_powtórzony_w_pliku_daje_jeden_wiersz(tmp_path):
    plik = tmp_path / "dwa.md"
    plik.write_text("`Plik jest tani.` oraz `Plik jest tani.`\n", encoding="utf-8")
    assert len(wydruk([plik]).splitlines()) == 1
