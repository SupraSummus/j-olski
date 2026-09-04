"""Ekstrakcja NKJP przeczytana o to, co w niej może zniknąć po cichu.

Archiwum nie stoi w repozytorium, więc próbki tych testów są pisane ręką.
Zdania w nich są wymyślone, bo pytają one o kształt pliku TEI, a nie o
polszczyznę: sądy o cudzych zdaniach stoją w ``próba/``.

Awarie, o które te testy pytają, wyglądają w wydruku jak sukces: sklejone
sekcje czytają się jak tekst, akapit urwany na znaczniku jest zdaniem
krótszym, a plik nadpisany nie liczy się dwa razy.
"""

from pathlib import Path

from harness.nkjp import main, typ, wycinki

PRÓBKA = """<?xml version="1.0" encoding="UTF-8"?>
<teiCorpus xmlns="http://www.tei-c.org/ns/1.0">
 <TEI>
  <text xml:id="txt_text" xml:lang="pl">
   <body xml:id="txt_body">
    <div xml:id="txt_1-div">
     <ab n="p10in90" xml:id="txt_1.1-ab">Parser czyta plik.</ab>
     <ab n="p11in90" xml:id="txt_1.2-ab">Potem go zamyka.</ab>
    </div>
    <div xml:id="txt_2-div">
     <ab n="p80in90" xml:id="txt_2.1-ab">Cena rośnie.</ab>
    </div>
   </body>
  </text>
 </TEI>
</teiCorpus>
"""

NAGŁÓWEK = """<?xml version="1.0" encoding="UTF-8"?>
<teiHeader xmlns="http://www.tei-c.org/ns/1.0">
 <profileDesc>
  <textClass>
   <catRef scheme="#taxonomy-NKJP-type" target="#typ_nd"/>
   <catRef scheme="#taxonomy-NKJP-channel" target="#kanal_ksiazka"/>
  </textClass>
 </profileDesc>
</teiHeader>
"""


def _archiwum(katalog: Path, *nazwy: str) -> Path:
    """Katalog z próbkami tej samej treści, po jednej na nazwę."""
    for nazwa in nazwy:
        (katalog / nazwa).mkdir(parents=True)
        (katalog / nazwa / "text.xml").write_text(PRÓBKA, encoding="utf-8")
        (katalog / nazwa / "header.xml").write_text(NAGŁÓWEK, encoding="utf-8")
    return katalog


def test_każda_sekcja_wychodzi_osobno_a_nie_zszyta_w_jedną_prozę():
    assert list(wycinki(PRÓBKA)) == [
        ("txt_1-div", "Parser czyta plik.\n\nPotem go zamyka."),
        ("txt_2-div", "Cena rośnie."),
    ]


def test_akapit_ze_znacznikiem_w_środku_nie_gubi_tekstu_za_nim():
    z_wyróżnieniem = PRÓBKA.replace("Cena rośnie.", 'Cena <hi rend="bold">stale</hi> rośnie.')
    assert dict(wycinki(z_wyróżnieniem))["txt_2-div"] == "Cena stale rośnie."


def test_sekcja_bez_akapitu_nie_wychodzi_pustym_plikiem():
    z_luką = PRÓBKA.replace('<ab n="p80in90" xml:id="txt_2.1-ab">Cena rośnie.</ab>', "<gap/>")
    assert [nazwa for nazwa, _ in wycinki(z_luką)] == ["txt_1-div"]


def test_warstwę_nazywa_taksonomia_typu_a_nie_kanał_obok_niej():
    assert typ(NAGŁÓWEK) == "typ_nd"
    assert typ('<catRef target="#kanal_ksiazka"/>') is None


def test_próbki_nazwane_wprost_nie_nadpisują_sobie_sekcji(tmp_path: Path):
    pierwsza, druga = "030-2-000000001", "030-2-000000002"
    archiwum = _archiwum(tmp_path / "nkjp", pierwsza, druga)
    into = tmp_path / "proza"

    main([str(archiwum / pierwsza), str(archiwum / druga), "--into", str(into)])

    assert sorted(p.relative_to(into).as_posix() for p in into.rglob("*.txt")) == [
        "typ_nd/030-2-000000001/txt_1-div.txt",
        "typ_nd/030-2-000000001/txt_2-div.txt",
        "typ_nd/030-2-000000002/txt_1-div.txt",
        "typ_nd/030-2-000000002/txt_2-div.txt",
    ]


def test_archiwum_nazwane_korzeniem_powtarza_kształt_wejścia(tmp_path: Path):
    archiwum = _archiwum(tmp_path / "nkjp", "DP2000/próbka-1")
    into = tmp_path / "proza"

    main([str(archiwum), "--into", str(into)])

    assert [p.relative_to(into).as_posix() for p in sorted(into.rglob("*.txt"))] == [
        "typ_nd/DP2000/próbka-1/txt_1-div.txt",
        "typ_nd/DP2000/próbka-1/txt_2-div.txt",
    ]
