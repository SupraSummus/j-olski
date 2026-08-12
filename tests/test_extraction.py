"""What the harness does to a document and to a statute, and what it must not invent.

The fixture beside this file carries one instance of every construct each
extraction handles, and the prose beside it is the whole answer: a change in
what the extraction keeps shows up as a diff a reader can judge. Its tail is
the constructs the parser settles rather than this repository — a table written
without leading pipes, a code span of three backticks opening a line, two
one-character emphases in a row — so a preset narrowed to plain CommonMark, or
widened, moves the fixture. The other tests here are the mistakes that would not
show up that way: an extraction that quietly drops prose, and one that leaves a
mark behind where markup stood, which is the failure docs/extraction.md was
written against.
"""

import re
from pathlib import Path

import pytest

from harness import PROSE_SUFFIX, markdown, ustawy

FIXTURES = Path(__file__).parent / "fixtures"

#: Ślad po skasowanej konstrukcji: odstęp podwojony w środku zdania i odstęp
#: przed znakiem, który w polszczyźnie stoi tuż przy słowie. Jedno i drugie jest
#: znakiem, którego nikt nie wpisał, i tyle wystarcza, żeby ekstrakcja była tu
#: winna zero: proza, którą wypuszcza, ma być tą, którą ktoś napisał. Drugi z
#: nich kosztuje przy tym więcej, bo znak przestankowy jest segmentem, więc
#: gramatyka dostaje zdanie o jeden segment dłuższe, niż je napisano, a odstęp
#: podwojony ginie Morfeuszowi wołanemu z ``SKIP_WHITESPACES``.
ŚLAD_PO_KASOWANIU = re.compile(r"(?<=\S)[ ]{2,}(?=\S)|(?<=[ \t])[,.;:!?…](?!\w)")

#: A list that closes a document, in the two shapes that decide whether it is an
#: index or the last thing the author had to say.
CLOSING_LIST = "Wnioski:\n\n- {first}\n- {second}\n"


def test_the_markdown_fixture_extracts_to_the_prose_beside_it():
    source = (FIXTURES / "extraction.md").read_text(encoding="utf-8")
    expected = (FIXTURES / f"extraction{PROSE_SUFFIX}").read_text(encoding="utf-8")
    assert markdown.prose(source) == expected


def test_the_markdown_extraction_leaves_no_mark_behind_where_markup_stood():
    """The fixture's prose is typed clean, so every stray mark in it would be the extractor's.

    Both extractions written before this one deleted inline markup and left the
    space in front of it, which is a space before punctuation per link and a
    doubled space per span in the middle of a sentence. The fixture stands a
    link before a question mark and an image with no description mid-paragraph
    for exactly that reason.
    """
    extracted = markdown.prose((FIXTURES / "extraction.md").read_text(encoding="utf-8"))
    assert ŚLAD_PO_KASOWANIU.findall(extracted) == []


@pytest.mark.parametrize(
    ("first", "second", "survives"),
    [
        ("Pierwszy wniosek.", "Drugi wniosek.", True),
        ("[prom](prom.md) — Rin i promy", "[tlen](tlen.md) — atmosfera", False),
    ],
    ids=["sentences", "links"],
)
def test_a_list_closing_a_document_goes_only_when_its_items_are_links(first, second, survives):
    extracted = markdown.prose(CLOSING_LIST.format(first=first, second=second))
    assert ("wniosek" in extracted) is survives
    assert "Wnioski:" in extracted


def test_the_selection_takes_the_language_and_the_floor_under_it(tmp_path, capsys):
    """A coverage figure over Polish must not have another language in its denominator.

    The floor is the second half and says something else: over how little text
    the share stops meaning anything. Both are needed, because three Polish
    words carry as high a share as three hundred and say nothing by it.
    """
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "pl.md").write_text(
        "Zdanie po polsku, w którym słowa mają ogonki.\n", encoding="utf-8"
    )
    (tmp_path / "src" / "en.md").write_text("A sentence in English.\n", encoding="utf-8")
    (tmp_path / "src" / "krótki.md").write_text("Zdanie za krótkie.\n", encoding="utf-8")
    markdown.main(
        [str(tmp_path / "src"), "--into", str(tmp_path / "out"),
         "--polish", "0.05", "--min-words", "5"]
    )
    assert "1 files into" in capsys.readouterr().out
    assert [path.stem for path in (tmp_path / "out").iterdir()] == ["pl"]


def test_the_command_mirrors_a_tree_into_files_olski_reads_as_prose(tmp_path, capsys):
    (tmp_path / "notes" / "deep").mkdir(parents=True)
    (tmp_path / "notes" / "one.md").write_text("# Tytuł\n\nZdanie.\n", encoding="utf-8")
    (tmp_path / "notes" / "deep" / "two.md").write_text("Drugie\nzdanie.\n", encoding="utf-8")
    assert markdown.main([str(tmp_path / "notes"), "--into", str(tmp_path / "prose")]) == 0
    assert "2 files" in capsys.readouterr().out
    assert (tmp_path / "prose" / f"one{PROSE_SUFFIX}").read_text(encoding="utf-8") == "Zdanie.\n"
    assert (tmp_path / "prose" / "deep" / f"two{PROSE_SUFFIX}").read_text(
        encoding="utf-8"
    ) == "Drugie zdanie.\n"


#: Jednostka redakcyjna z jednostką pod sobą, w której typ tej niższej jest do
#: wstawienia: o zszyciu rozstrzyga właśnie typ, a reszta zapisu jest bez zmian.
JEDNOSTKA_W_JEDNOSTCE = """\
<div class="unit unit_pass pro-text">
   <h3>1.</h3>
   <div class="unit-inner">
      <div data-template="xText" CLASS="pro-text">Gmina wykonuje zadania:</div>
      <div class="unit {typ} pro-text">
         <h3>1)</h3>
         <div class="unit-inner">
            <div data-template="xText" CLASS="pro-text">własne.</div>
         </div>
      </div>
   </div>
</div>
"""


def test_ustawa_próbna_wychodzi_prozą_która_stoi_obok_niej():
    źródło = (FIXTURES / "ustawa.html").read_text(encoding="utf-8")
    oczekiwane = (FIXTURES / f"ustawa{PROSE_SUFFIX}").read_text(encoding="utf-8")
    assert ustawy.proza(źródło) == oczekiwane


def test_ekstrakcja_z_ustawy_nie_zostawia_śladu_po_tym_co_skasowała():
    """Proza fixture'u jest wpisana czysto, więc każdy zabłąkany znak nad nią jest ekstrakcji.

    Wydawca wstawia adres publikacji między przecinek i przecinek, więc kasowanie,
    które ślad po nim zostawia, daje przecinek podwojony i przecinek z odstępem
    przed sobą. Po to fixture stawia jeden taki adres w środku zdania.
    """
    wyszło = ustawy.proza((FIXTURES / "ustawa.html").read_text(encoding="utf-8"))
    assert ŚLAD_PO_KASOWANIU.findall(wyszło) == []


@pytest.mark.parametrize(
    ("typ", "zszyte"),
    [("unit_pint", True), ("unit_lett", True), ("unit_pass", False), ("unit_tire", False)],
    ids=["punkt", "litera", "ustęp", "typ, którego wydawca tu nie ma"],
)
def test_przesłankę_dostaje_pozycja_wyliczenia_a_nie_każda_jednostka_niżej(typ, zszyte):
    """Zszycie w głąb bez warunku dokleja preambułę do każdego przepisu ustawy.

    Ustęp stoi sam, więc tekst jednostki nad nim jest osobnym zdaniem, a punkt i
    litera ciągną go dalej, bo wyliczenie dzieli przesłankę między pozycje. Typ
    spoza tej listy idzie tam, gdzie ustęp, bo zszywa lista, a nie jej brak.
    """
    proza = ustawy.proza(JEDNOSTKA_W_JEDNOSTCE.format(typ=typ))
    assert ("Gmina wykonuje zadania własne." in proza) is zszyte
