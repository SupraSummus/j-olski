"""Reading Składnica, and measuring the grammar against it.

The forests here are written by hand rather than copied out of the treebank.
Składnica is distributed under the GPL and this repository carries no licence
file, so vendoring even a few of its trees would decide a licensing question that
is not the tests' to decide. Hand-written fixtures also let a single forest carry
exactly the one property under test, which a real one never does.

The format is not invented, though. It is what the 2018 release actually
contains: a forest of nodes, a gold tree marked by ``chosen`` links between them
rather than by a flag on each node, disambiguated tags on the terminals, and
valency slots on the required phrases naming which one is the subject.
"""

import xml.etree.ElementTree as ET

import pytest

pytest.importorskip("morfeusz2")

from olski.corpus import FULL, Sentence, parse_forest, pliki, read
from olski.coverage import Outcome, main, measure, przebieg, render, scal
from olski.parse import parse
from olski.subset import GRAMMAR


def forest(nodes, text="Program zapisuje ustawienia.", verdict=FULL, sent_id="t/1-s"):
    return ET.fromstring(
        f'<forest sent_id="{sent_id}">'
        f"<text>{text}</text>"
        f'<answer-data><base-answer type="{verdict}"/></answer-data>'
        f"{nodes}"
        f"</forest>"
    )


def terminal(nid, start, end, orth, tag, lemma=None, chosen="true"):
    #  ``chosen=None`` zostawia węzeł bez tej flagi, bo Składnica takie pisze.
    flaga = f' chosen="{chosen}"' if chosen else ""
    return (
        f'<node nid="{nid}" from="{start}" to="{end}"{flaga}>'
        f'<terminal token_id="s.{nid}-seg" disamb="true">'
        f"<orth>{orth}</orth><base>{lemma or orth}</base>"
        f'<f type="tag">{tag}</f>'
        f"</terminal></node>"
    )


def phrase(nid, start, end, category, children, slot=None, chosen="true", rule="r"):
    slot_f = f'<f type="tfw">{slot}</f>' if slot else ""
    kids = "".join(f'<child nid="{child}"/>' for child in children)
    return (
        f'<node nid="{nid}" from="{start}" to="{end}" chosen="{chosen}">'
        f"<nonterminal><category>{category}</category>{slot_f}</nonterminal>"
        f'<children rule="{rule}" chosen="{chosen}">{kids}</children>'
        f"</node>"
    )


#: Tag czasownika, po który nie sięga żadna produkcja, więc zdanie z nim
#: wychodzi odrzucone i te testy mają czym mierzyć odrzucenie. Forma nieosobowa,
#: bo podzbiór jej nie ma i żaden etap jej nie planuje.
POZA_PODZBIOREM = "imps:perf"


def svo(subject="subj(np(nom))", obj="np(accgen)", verb=None, tag="fin:sg:ter:imperf"):
    """*Program zapisuje ustawienia.* — subject first, object last, both marked.

    The slots are arguments so that a test can move a role onto the wrong phrase
    without rewriting the XML by string substitution, which is how the first
    version of these fixtures quietly lost its final full stop.
    """
    return (
        phrase(0, 0, 4, "wypowiedzenie", [1, 5, 9, 11])
        + phrase(1, 0, 1, "fw", [2], slot=subject)
        + terminal(2, 0, 1, "Program", "subst:sg:nom:m3")
        + phrase(5, 1, 2, "ff", [6], slot=verb)
        + terminal(6, 1, 2, "zapisuje", tag, lemma="zapisywać")
        + phrase(9, 2, 3, "fw", [10], slot=obj)
        + terminal(10, 2, 3, "ustawienia", "subst:pl:acc:n", lemma="ustawienie")
        + terminal(11, 3, 4, ".", "interp")
    )


SVO = svo()


# --------------------------------------------------------------------------- #
# The gold tree is the chosen links, not the chosen flags
# --------------------------------------------------------------------------- #


def test_a_forest_yields_its_gold_terminals_in_order():
    sentence = parse_forest(forest(SVO))
    assert sentence.annotated
    assert sentence.tokens == ("Program", "zapisuje", "ustawienia", ".")
    assert sentence.sent_id == "t/1-s"


def test_positions_are_treebank_token_numbers_so_spans_compare():
    sentence = parse_forest(forest(SVO))
    assert [(s.start, s.end) for s in sentence.segments] == [(0, 1), (1, 2), (2, 3), (3, 4)]


def test_gold_tags_become_readings_the_parser_can_use():
    sentence = parse_forest(forest(SVO))
    reading = sentence.segments[0].readings[0]
    assert reading.tag.pos == "subst"
    assert reading.tag.get("case") == frozenset({"nom"})
    #  One reading per terminal: the treebank has already disambiguated.
    assert all(len(segment.readings) == 1 for segment in sentence.segments)


def test_a_node_outside_the_chosen_tree_is_left_out():
    #  The node is flagged chosen — it takes part in some chosen derivation — but
    #  nothing in the tree links to it, so it is not part of the answer. Trusting
    #  the flag would put a second terminal on a span the sentence already has.
    stray = terminal(99, 0, 1, "Program", "subst:sg:acc:m3")
    sentence = parse_forest(forest(SVO + stray))
    assert sentence.tokens == ("Program", "zapisuje", "ustawienia", ".")


def test_an_unchosen_expansion_is_not_followed():
    other = phrase(30, 0, 1, "fno", [31], chosen="false")
    stray = terminal(31, 0, 1, "Program", "subst:sg:voc:m3", chosen="false")
    sentence = parse_forest(forest(SVO + other + stray))
    assert sentence.tokens == ("Program", "zapisuje", "ustawienia", ".")


def test_a_forest_that_does_not_number_its_root_zero_still_reads():
    #  Every FULL forest in the 2018 release numbers its root 0, so the fallback
    #  to the widest chosen node never runs on real data. Untested defensive code
    #  is where the next release's bug would hide.
    #  Only the root carries nid="0"; children are referenced by their own nids.
    sentence = parse_forest(forest(SVO.replace('nid="0"', 'nid="900"')))
    assert sentence.tokens == ("Program", "zapisuje", "ustawienia", ".")
    assert sentence.spans("Subject") == frozenset({(0, 1)})


def test_a_forest_with_no_gold_tree_carries_its_verdict_and_nothing_else():
    sentence = parse_forest(forest("", verdict="NO_TREE"))
    assert not sentence.annotated
    assert sentence.verdict == "NO_TREE"
    assert sentence.segments == ()


# --------------------------------------------------------------------------- #
# Znaczniki NKJP, którymi bank drzew mówi to, co gramatyka czyta po morfeuszowsku
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("nkjp", "morfeusz"),
    [("qub", "part"), ("psubst:sg:dat:m1", "subst"), ("padj", "adj"), ("padv", "adv")],
)
def test_znacznik_nkjp_dochodzi_do_gramatyki_pod_nazwą_morfeusza(nkjp, morfeusz):
    sentence = parse_forest(forest(terminal(0, 0, 1, "to", nkjp)))
    assert sentence.segments[0].readings[0].tag.pos == morfeusz


def test_przełożony_znacznik_niesie_swoje_cechy_dalej():
    sentence = parse_forest(forest(terminal(0, 0, 1, "tym", "psubst:sg:inst:m1")))
    tag = sentence.segments[0].readings[0].tag
    assert tag.get("case") == frozenset({"inst"})
    assert str(tag) == "subst:sg:inst:m1"


def test_cząstka_znaczona_po_nkjp_wyprowadza_zdanie_zwrotne():
    """Produkcja, którą gramatyka ma, ma nad bankiem drzew wystrzelić.

    Zdanie stoi tu całe, a nie sam znacznik, bo o przekład idzie właśnie po to:
    bez niego terminal cząstki nie bierze nad złotą morfologią ani jednej formy,
    a wiersz blokerów nazywa nazwę znacznika zamiast konstrukcji, której brak.
    """
    zwrotne = (
        phrase(0, 0, 4, "wypowiedzenie", [1, 5, 9, 11])
        + phrase(1, 0, 1, "fw", [2], slot="subj(np(nom))")
        + terminal(2, 0, 1, "Program", "subst:sg:nom:m3")
        + phrase(5, 1, 2, "ff", [6])
        + terminal(6, 1, 2, "zapisuje", "fin:sg:ter:imperf", lemma="zapisywać")
        + phrase(9, 2, 3, "fw", [10])
        + terminal(10, 2, 3, "się", "qub")
        + terminal(11, 3, 4, ".", "interp")
    )
    assert outcome(zwrotne, text="Program zapisuje się.").status == "valid"


# --------------------------------------------------------------------------- #
# Valency slots, which is how the gold tree names the subject
# --------------------------------------------------------------------------- #


def test_the_subject_slot_is_read_as_a_subject():
    assert parse_forest(forest(SVO)).spans("Subject") == frozenset({(0, 1)})


def test_a_bare_subject_slot_counts_too():
    #  Składnica writes both subj and subj(np(nom)).
    assert parse_forest(forest(svo(subject="subj"))).spans("Subject") == frozenset({(0, 1)})


def test_an_accusative_object_slot_is_read_as_an_object():
    assert parse_forest(forest(SVO)).spans("Object") == frozenset({(2, 3)})


@pytest.mark.parametrize("slot", ["np(bier)", "np(acc)", "np(accgen)"])
def test_the_object_slot_is_recognized_under_either_naming(slot):
    #  Cases are named in Polish and in Latin interchangeably, sometimes in one
    #  frame, so bier and acc have to mean the same thing.
    assert parse_forest(forest(svo(obj=slot))).spans("Object") == frozenset({(2, 3)})


@pytest.mark.parametrize("slot", ["np(gen)", "np(inst)", "xp(temp)", "advp", "prepnp(do,gen)"])
def test_a_slot_olski_has_no_role_for_is_not_forced_into_one(slot):
    sentence = parse_forest(forest(svo(obj=slot)))
    assert sentence.spans("Object") == frozenset()
    assert sentence.spans("Subject") == frozenset({(0, 1)})


# --------------------------------------------------------------------------- #
# Reading from disk
# --------------------------------------------------------------------------- #


def write(directory, name, nodes, **kwargs):
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    element = forest(nodes, **kwargs)
    path.write_bytes(ET.tostring(element, encoding="utf-8"))
    return path


def test_a_forest_file_reads_the_same_as_the_element(tmp_path):
    path = write(tmp_path, "one-s.xml", SVO)
    assert read(path).tokens == parse_forest(forest(SVO)).tokens


def test_niewybrany_węzeł_wycięty_z_pliku_nie_zmienia_odpowiedzi(tmp_path):
    #  Czytanie wycina niewybrane węzły, zanim XML z pliku powstanie, bo las jest
    #  w większości rozwinięciami, których odpowiedź nie bierze. Test jest o tym,
    #  że wycięcie niczego nie zabiera: ten sam las z takim rozwinięciem i bez
    #  niego czyta się na to samo zdanie.
    obce = phrase(30, 0, 1, "fno", [31], chosen="false")
    dalsze = terminal(31, 0, 1, "Program", "subst:sg:voc:m3", chosen="false")
    z_lasem = read(write(tmp_path, "a-s.xml", SVO + obce + dalsze))
    bez_lasu = read(write(tmp_path, "b-s.xml", SVO))
    assert z_lasem == bez_lasu
    assert z_lasem.tokens == ("Program", "zapisuje", "ustawienia", ".")


def test_węzeł_bez_flagi_wyboru_zostaje_w_lesie(tmp_path):
    #  Zejście po dowiązaniach dosięga takiego węzła tak samo jak reszty, więc
    #  wycięcie wszystkiego, co nie jest wybrane, zabrałoby zdaniu token.
    węzły = (
        phrase(0, 0, 2, "wypowiedzenie", [1, 3])
        + phrase(1, 0, 1, "fw", [2], slot="subj")
        + terminal(2, 0, 1, "Program", "subst:sg:nom:m3", chosen=None)
        + terminal(3, 1, 2, ".", "interp")
    )
    assert read(write(tmp_path, "a-s.xml", węzły)).tokens == ("Program", ".")


def test_a_broken_file_is_named_in_the_error(tmp_path):
    #  Walking twenty thousand files, a parse error that says only "line 1,
    #  column 0" identifies nothing.
    path = tmp_path / "broken-s.xml"
    path.write_text("<forest><text>nie zamknięty", encoding="utf-8")
    with pytest.raises(ET.ParseError, match="broken-s.xml"):
        read(path)


def test_walking_a_directory_finds_forests_at_any_depth(tmp_path):
    write(tmp_path, "doc/morph_1-p/a-s.xml", SVO)
    write(tmp_path, "doc/morph_2-p/b-s.xml", "", verdict="TOO_DIFFICULT")
    found = [read(path) for path in pliki(tmp_path)]
    assert [sentence.verdict for sentence in found] == [FULL, "TOO_DIFFICULT"]


# --------------------------------------------------------------------------- #
# Measuring, and what the measurement is allowed to claim
# --------------------------------------------------------------------------- #


def outcome(nodes, **kwargs):
    sentence = parse_forest(forest(nodes, **kwargs))
    return Outcome(sentence=sentence, result=parse(GRAMMAR, list(sentence.segments)))


def test_a_sentence_olski_derives_once_agrees_with_the_gold_roles():
    found = outcome(SVO)
    assert found.status == "valid"
    assert found.agreement == "agrees"


def test_a_subject_the_gold_tree_calls_the_object_is_reported_as_reversed():
    #  The gold tree's roles exchanged, so olski's reading is not imprecise but
    #  backwards. Counted apart from an extent disagreement, because this is the
    #  failure the ambiguity design exists to prevent.
    reversed_gold = svo(subject="np(accgen)", obj="subj(np(nom))")
    assert outcome(reversed_gold).agreement == "reversed"


def test_a_disagreement_outranks_a_partial_on_the_other_role():
    #  Partial on the subject — a second one olski assigns nothing to — and wrong
    #  on the object, whose gold span is the verb. Judging the roles in order and
    #  returning on the first would report this as merely partial, which is the
    #  milder of the two claims.
    both = svo(verb="subj(np(nom))", obj="np(gen)") + phrase(
        20, 1, 2, "fw", [6], slot="np(bier)", chosen="false"
    )
    sentence = parse_forest(forest(both))
    assert sentence.spans("Subject") == frozenset({(0, 1), (1, 2)})
    #  The object slot the gold tree marks is on a span olski calls the verb.
    found = Outcome(
        sentence=Sentence(
            sent_id=sentence.sent_id,
            text=sentence.text,
            verdict=sentence.verdict,
            segments=sentence.segments,
            roles=(("Object", 1, 2), ("Subject", 0, 1), ("Subject", 1, 2)),
        ),
        result=parse(GRAMMAR, list(sentence.segments)),
    )
    assert found.agreement == "disagrees"


def test_a_role_the_gold_tree_marks_and_olski_does_not_is_partial_not_agreement():
    #  A second subject, on the verb phrase, that olski assigns nothing to. Its
    #  reading is not contradicted, so it is not a disagreement, and not a
    #  confirmed agreement either.
    extra = svo(verb="subj(np(nom))")
    assert parse_forest(forest(extra)).spans("Subject") == frozenset({(0, 1), (1, 2)})
    assert outcome(extra).agreement == "partial"


def test_a_rejected_sentence_is_not_asked_about_agreement():
    #  A verb form outside the subset leaves no reading to judge.
    found = outcome(svo(tag=POZA_PODZBIOREM))
    assert found.status == "rejected"
    assert found.agreement is None


def test_a_rejected_sentence_names_the_part_of_speech_it_stopped_on():
    assert outcome(svo(tag=POZA_PODZBIOREM)).blocker == "imps"


def test_agreement_is_not_claimed_when_spans_are_not_comparable():
    #  Live morphology numbers positions in characters, so a span from the parser
    #  and a span from the gold tree are not the same kind of thing.
    sentence = parse_forest(forest(SVO))
    found = Outcome(
        sentence=sentence,
        result=parse(GRAMMAR, list(sentence.segments)),
        comparable=False,
    )
    assert found.agreement is None


def test_measuring_counts_every_forest_but_parses_only_the_annotated_ones(tmp_path):
    write(tmp_path, "a-s.xml", SVO)
    write(tmp_path, "b-s.xml", "", verdict="NO_TREE")
    report = przebieg(pliki(tmp_path), jobs=1)
    assert report.verdicts == {FULL: 1, "NO_TREE": 1}
    assert report.measured == 1
    assert report.statuses["valid"] == 1


def test_an_annotated_sentence_with_no_morphology_is_reported_rather_than_dropped(tmp_path):
    #  Reported and not dropped, so that the denominator under the coverage figure
    #  is the whole annotated corpus or says what it is missing.
    write(tmp_path, "a-s.xml", "")
    report = przebieg(pliki(tmp_path), jobs=1)
    assert report.verdicts == {FULL: 1}
    assert report.measured == 0
    assert report.skipped == {"no morphology": 1}


def test_an_unknown_morphology_source_is_refused():
    with pytest.raises(ValueError, match="unknown morphology source"):
        measure([], source="wishful")


def test_the_report_renders_what_it_measured(tmp_path):
    write(tmp_path, "a-s.xml", SVO)
    text = render(przebieg(pliki(tmp_path), jobs=1, keep_examples=1))
    assert "gold morphology" in text
    assert "valid" in text
    assert "Program zapisuje ustawienia." in text


def test_raport_scalony_z_kawałków_jest_tym_samym_raportem(tmp_path):
    #  Proces roboczy oddaje `Report` za swój kawałek listy plików, więc każdy
    #  wiersz wydruku stoi na tym, że kawałki scalają się w raport z jednego
    #  przebiegu. Piąty las ma drzewo wzorcowe i nie ma morfologii, żeby przez
    #  scalanie przeszedł także wiersz niemierzonych.
    #
    #  Teksty są różne, bo przykłady sprawdzają to najostrzej: `Report.record`
    #  zachowuje pierwsze zdanie, jakie dostał, więc kawałki scalone nie w
    #  kolejności korpusu drukowałyby inne zdanie niż jeden przebieg.
    write(tmp_path, "a-s.xml", SVO, text="Program zapisuje ustawienia.")
    write(tmp_path, "b-s.xml", svo(subject=None, obj=None), sent_id="t/2-s", text="Zapisuje.")
    write(tmp_path, "c-s.xml", svo(tag=POZA_PODZBIOREM), sent_id="t/3-s", text="Zapisał to.")
    write(tmp_path, "d-s.xml", "", verdict="NO_TREE", sent_id="t/4-s", text="Bez drzewa.")
    write(tmp_path, "e-s.xml", "", sent_id="t/5-s", text="Bez morfologii.")

    ścieżki = pliki(tmp_path)
    całość = measure((read(path) for path in ścieżki), keep_examples=1)
    kawałki = [measure([read(path)], keep_examples=1) for path in ścieżki]
    assert render(scal(kawałki, source="gold", keep_examples=1)) == render(całość)


def test_pula_procesów_drukuje_to_samo_co_jeden_proces(tmp_path, capsys):
    #  Przez granicę procesu idzie licznik, a nie las, który go zbudował, więc to
    #  jest o tym, że licznik daje się przez nią przenieść i złożyć z powrotem.
    write(tmp_path, "a-s.xml", SVO)
    write(tmp_path, "b-s.xml", svo(tag=POZA_PODZBIOREM), sent_id="t/2-s")
    main([str(tmp_path), "--examples", "1", "--jobs", "1"])
    jeden = capsys.readouterr().out
    main([str(tmp_path), "--examples", "1", "--jobs", "2"])
    assert capsys.readouterr().out == jeden
    #  Pula, która zgubiłaby kawałek, dalej drukowałaby to samo co jeden proces,
    #  gdyby jeden proces gubił go tak samo, więc liczba lasów jest tu osobno.
    assert "corpus: 2 forests" in jeden


def test_an_accepted_sentence_with_no_gold_role_is_counted_not_dropped(tmp_path):
    #  Pro-drop realizes no subject, so the gold tree marks nothing to compare
    #  and the agreement table has no row for the sentence. Left uncounted, the
    #  table's denominator would quietly become the sentences it could judge.
    write(tmp_path, "a-s.xml", SVO)
    write(tmp_path, "b-s.xml", svo(subject=None, obj=None), sent_id="t/2-s")
    report = przebieg(pliki(tmp_path), jobs=1)
    assert report.statuses["valid"] == 2
    assert sum(report.agreements.values()) == 1
    assert report.unjudged == 1
    assert "no gold role to compare" in render(report)
