"""Złote znaczniki NKJP przyłożone do zdania, przeczytane o to, co w tym przyłożeniu psuje się po cichu.

Archiwum nie stoi w repozytorium, więc próbka jest pisana ręką, a zdania w niej
wymyślone: pytają o kształt warstw i o zawężenie, a nie o polszczyznę.

Usterki, o które te testy pytają, wyglądają w wydruku jak wynik: odczytanie
z alternatywą przypadka zostawione w całości liczy się jako wieloznaczność,
której anotator nie rozstrzygnął, a forma bez odczytania zgodnego ze złotym,
zdjęta razem z resztą, liczyłaby się jako czytanie, które przepadło.
"""

from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

from harness.znaczniki import (
    NIECZYTANE,
    POZOSTAJE,
    PRZEPADŁO,
    ROZSTRZYGNIĘTE,
    SPRZECZNE,
    ZGODNE,
    Przyłożenie,
    Wynik,
    Złoty,
    nad_sekcją,
    przyłóż,
    umieść,
    zawęź,
    zgodne,
    złote,
)
from olski.morph import tag
from olski.segmentacja import morphology

PIERWSZE = "Koszt samej szynki przewyższa koszt szynki."
DRUGIE = "Cena rośnie."

TEKST = f"""<?xml version="1.0" encoding="UTF-8"?>
<teiCorpus xmlns="http://www.tei-c.org/ns/1.0">
 <TEI>
  <text xml:id="txt_text" xml:lang="pl">
   <body xml:id="txt_body">
    <div xml:id="txt_1-div">
     <ab n="p1in9" xml:id="txt_1.1-ab">{PIERWSZE}</ab>
     <ab n="p2in9" xml:id="txt_1.2-ab">{DRUGIE}</ab>
    </div>
   </body>
  </text>
 </TEI>
</teiCorpus>
"""

#: Segmenty próbki: akapit, forma, znaczniki do wyboru i który z nich anotator wybrał.
#: Pierwszy ``koszt`` ma alternatywę mianownika i biernika i wybrany mianownik,
#: drugi tę samą alternatywę i wybrany biernik, więc zdanie ma dla anotatora
#: jeden szyk.
SEGMENTY = [
    ("txt_1.1-ab", "Koszt", ("subst:sg:nom:m3", "subst:sg:acc:m3"), 0),
    ("txt_1.1-ab", "samej", ("adj:sg:gen:f:pos",), 0),
    ("txt_1.1-ab", "szynki", ("subst:sg:gen:f",), 0),
    ("txt_1.1-ab", "przewyższa", ("fin:sg:ter:imperf",), 0),
    ("txt_1.1-ab", "koszt", ("subst:sg:nom:m3", "subst:sg:acc:m3"), 1),
    ("txt_1.1-ab", "szynki", ("subst:sg:gen:f",), 0),
    ("txt_1.1-ab", ".", ("interp",), 0),
    ("txt_1.2-ab", "Cena", ("subst:sg:nom:f",), 0),
    ("txt_1.2-ab", "rośnie", ("fin:sg:ter:imperf",), 0),
    ("txt_1.2-ab", ".", ("interp",), 0),
]


def _warstwy(segmenty) -> tuple[str, str]:
    """Segmentacja i morfologia próbki z listy segmentów, tak jak pisze je archiwum."""
    segmentacja, morfologia = [], []
    miejsce: dict[str, int] = {}
    for numer, (akapit, forma, znaczniki, wybrany) in enumerate(segmenty, start=1):
        start = miejsce.get(akapit, 0)
        miejsce[akapit] = start + len(forma) + 1
        segmentacja.append(
            f'<seg corresp="text.xml#string-range({akapit},{start},{len(forma)})" xml:id="segm_{numer}-seg"/>'
        )
        symbole = "".join(
            f'<symbol value="{znacznik.partition(":")[2]}" xml:id="morph_{numer}.{i}-msd"/>'
            for i, znacznik in enumerate(znaczniki, start=1)
        )
        morfologia.append(
            f'<seg corresp="ann_segmentation.xml#segm_{numer}-seg" xml:id="morph_{numer}-seg">'
            '<fs type="morph">'
            f'<f name="orth"><string>{forma}</string></f>'
            '<f name="interps"><fs type="lex">'
            f'<f name="ctag"><symbol value="{znaczniki[0].partition(":")[0]}"/></f>'
            f'<f name="msd"><vAlt>{symbole}</vAlt></f>'
            "</fs></f>"
            f'<f name="disamb"><fs type="tool_report"><f fVal="#morph_{numer}.{wybrany + 1}-msd" name="choice"/></fs></f>'
            "</fs></seg>"
        )
    otwarcie = '<?xml version="1.0" encoding="UTF-8"?>\n<teiCorpus xmlns="http://www.tei-c.org/ns/1.0"><TEI><text><body><p><s>'
    zamknięcie = "</s></p></body></text></TEI></teiCorpus>\n"
    return otwarcie + "".join(segmentacja) + zamknięcie, otwarcie + "".join(morfologia) + zamknięcie


@pytest.fixture
def archiwum(tmp_path: Path) -> Path:
    próbka = tmp_path / "nkjp" / "próbka"
    próbka.mkdir(parents=True)
    segmentacja, morfologia = _warstwy(SEGMENTY)
    (próbka / "text.xml").write_text(TEKST, encoding="utf-8")
    (próbka / "ann_segmentation.xml").write_text(segmentacja, encoding="utf-8")
    (próbka / "ann_morphosyntax.xml").write_text(morfologia, encoding="utf-8")
    return tmp_path / "nkjp"


def test_złoty_segment_niesie_miejsce_w_akapicie_i_znacznik_wybrany_a_nie_pierwszy(archiwum):
    pierwszy, *_, drugi_koszt, _, _ = złote(archiwum / "próbka")["txt_1.1-ab"]
    assert (pierwszy.forma, pierwszy.start, pierwszy.długość) == ("Koszt", 0, 5)
    assert pierwszy.znacznik.raw == "subst:sg:nom:m3"
    assert (drugi_koszt.forma, drugi_koszt.znacznik.raw) == ("koszt", "subst:sg:acc:m3")


def test_złoto_rozstrzyga_wieloznaczność_która_jest_przypadkiem_jednej_formy(archiwum):
    wyniki, nieumieszczone = nad_sekcją(archiwum, "typ_nd/próbka/txt_1-div.txt", f"{PIERWSZE}\n\n{DRUGIE}\n")
    assert nieumieszczone == 0
    assert [(w.klasa, w.ile, w.ile_ze_złotem) for w in wyniki] == [
        (ROZSTRZYGNIĘTE, 2, 1),
        (ZGODNE, 1, 1),
    ]


def test_zawężenie_zwęża_alternatywę_przypadka_a_nie_tylko_odsiewa_odczytania():
    #  Morfeusz pisze ``nagrody`` jednym odczytaniem o trzech przypadkach, więc
    #  odsiew odczytań zostawiłby je w całości i gramatyka dalej stawiałaby formę
    #  w obu rolach.
    zawężone = zawęź(tag("subst:pl:nom.acc.voc:f"), tag("subst:pl:nom:f"))
    assert zawężone.raw == "subst:pl:nom:f"
    assert zawężone.get("case") == {"nom"}


def test_cecha_której_tagset_nkjp_nie_ma_nie_rozstrzyga_o_zgodności():
    assert zgodne(tag("subst:sg:nom.acc.voc:n:ncol"), tag("subst:sg:acc:n"))
    assert zgodne(tag("part"), tag("qub"))
    assert not zgodne(tag("adv"), tag("qub"))


def _złote_zdania(zdanie: str, znaczniki: dict[str, str]) -> list[Złoty]:
    """Złote segmenty jednego zdania stojącego na początku akapitu, z zadanymi znacznikami."""
    zebrane, start = [], 0
    for forma in zdanie.replace(".", " .").split():
        zebrane.append(Złoty("ab", start, len(forma), forma, tag(znaczniki.get(forma, "interp"))))
        start += len(forma) + 1
    return zebrane


def test_forma_bez_odczytania_zgodnego_ze_złotym_zostaje_ze_wszystkimi_odczytaniami():
    #  Zdjęcie wszystkich odczytań zabrałoby zdaniu każde czytanie, a liczba
    #  czytałaby się wtedy jak złote czytanie, które przepadło.
    segmenty = morphology(DRUGIE)
    złote_zdania = _złote_zdania(DRUGIE, {"Cena": "subst:sg:nom:f", "rośnie": "subst:sg:nom:f"})
    zawężone, przyłożenie = przyłóż(segmenty, DRUGIE, złote_zdania, 0)
    assert przyłożenie.bez_odczytania == 1
    assert zawężone[1].readings == segmenty[1].readings


def test_forma_podzielona_inaczej_niż_u_anotatora_zostaje_nieprzyłożona():
    segmenty = morphology(DRUGIE)
    sklejone = [
        Złoty("ab", 0, len("Cena rośnie"), "Cena rośnie", tag("subst:sg:nom:f")),
        Złoty("ab", len("Cena rośnie"), 1, ".", tag("interp")),
    ]
    _, przyłożenie = przyłóż(segmenty, DRUGIE, sklejone, 0)
    assert przyłożenie.nieprzyłożone == 2


def test_zdanie_szuka_się_od_miejsca_poprzedniego_i_w_kolejnych_akapitach():
    akapity = [("ab1", f"  {PIERWSZE} {DRUGIE}"), ("ab2", DRUGIE)]
    assert umieść([PIERWSZE, DRUGIE, DRUGIE, "Nie ma mnie."], akapity) == [
        ("ab1", 2),
        ("ab1", 3 + len(PIERWSZE)),
        ("ab2", 0),
        None,
    ]


@pytest.mark.parametrize(
    ("ile", "ile_ze_złotem", "klasa"),
    [
        (0, None, NIECZYTANE),
        (1, 1, ZGODNE),
        (1, 0, SPRZECZNE),
        (2, 1, ROZSTRZYGNIĘTE),
        (2, 2, POZOSTAJE),
        (2, 0, PRZEPADŁO),
    ],
)
def test_klasa_bierze_się_z_liczby_czytań_przed_zawężeniem_i_po_nim(ile, ile_ze_złotem, klasa):
    assert Wynik("", "", ile, ile_ze_złotem, Przyłożenie()).klasa == klasa
