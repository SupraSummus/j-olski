import pytest

pytest.importorskip("morfeusz2")

from olski.morph import analyse, tag, unknown


def test_a_tag_becomes_a_part_of_speech_and_feature_sets():
    parsed = tag("subst:sg:nom.acc:m3")
    assert parsed.pos == "subst"
    assert parsed.get("number") == {"sg"}
    #  The dot is a disjunction, so a feature holds a set.
    assert parsed.get("case") == {"nom", "acc"}
    assert parsed.get("gender") == {"m3"}
    assert parsed.has("case", "nom")


def test_features_are_read_by_value_not_by_position():
    #  Different tagsets order their features differently; nothing here depends
    #  on the order, because every Morfeusz value names its own category.
    assert tag("adj:pl:acc:n:pos").get("degree") == {"pos"}
    assert tag("fin:sg:ter:imperf").get("person") == {"ter"}
    assert tag("prep:loc:nwok").get("case") == {"loc"}


def test_an_unrecognized_chunk_is_kept_rather_than_dropped():
    parsed = tag("subst:sg:nom:m1:czegoś-nowego")
    assert parsed.get("other:czegoś-nowego") == {"czegoś-nowego"}


def test_a_missing_feature_is_the_empty_set():
    assert tag("interp").get("case") == frozenset()


def test_text_is_segmented_and_every_segment_carries_its_readings():
    segments = analyse("Program zapisuje plik.")
    assert [segment.form for segment in segments] == ["Program", "zapisuje", "plik", "."]
    assert [(segment.start, segment.end) for segment in segments] == [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
    ]
    assert segments[0].with_pos("subst")[0].lemma == "program"


def test_one_form_can_have_several_readings_and_none_is_chosen():
    #  pliku is genitive, locative or vocative, and the analyser says so rather
    #  than picking. Choosing is the parser's job.
    cases = set()
    for reading in analyse("pliku")[0].with_pos("subst"):
        cases |= set(reading.tag.get("case"))
    assert cases == {"gen", "loc", "voc"}


def test_a_gerund_is_distinguishable_from_the_noun_it_looks_like():
    #  This is the zombie-noun distinction a suffix pattern cannot make:
    #  ustawienia is a form of the noun ustawienie and of the gerund of ustawić.
    readings = analyse("ustawienia")[0]
    assert {r.lemma for r in readings.with_pos("ger")} == {"ustawić"}
    assert {r.lemma for r in readings.with_pos("subst")} == {"ustawienie"}


def test_lemat_dwukropka_jest_dwukropkiem_a_nie_pustym_napisem():
    #  Lematem dwukropka jest dwukropek, więc obcięcie indeksu homonimu po
    #  pierwszym dwukropku zostawiało tu pusty napis. Po tagu tego nie widać:
    #  terminal żądający lematu „:” nie brał wtedy ani jednego czytania.
    dwukropek = analyse("Cena jest niska: gramatyka jest bezkontekstowa.")[3]
    assert dwukropek.form == ":"
    assert [reading.lemma for reading in dwukropek.readings] == [":"]
    #  Indeks jest dalej obcinany, bo bieg:s1 jest lematem bieg.
    assert analyse("biegu")[0].with_pos("subst")[0].lemma == "bieg"


def test_an_unknown_form_is_reported_rather_than_guessed_at():
    segments = analyse("Program zapisuje plikx.")
    assert [segment.form for segment in unknown(segments)] == ["plikx"]
    assert not segments[2].known
