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

from harness.corpus import FULL, Sentence, constituents, parse_forest, pliki, read
from harness.pomiar import Outcome, main, measure, przebieg, scal, zmierz_zdanie
from olski.parse import parse
from olski.pokrycie import NO_STRUCTURE, render
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


def phrase(nid, start, end, category, children, slot=None, chosen="true", rule="r", **cechy):
    #  Cechy idą słowami kluczowymi, bo test pisze zwykle jedną — `przypadek`
    #  albo `klasa` — a pozycyjny słownik kazałby wypisywać ją w każdym wywołaniu,
    #  także tam, gdzie o cechy nie chodzi.
    pola = "".join(f'<f type="{nazwa}">{wartość}</f>' for nazwa, wartość in cechy.items())
    slot_f = f'<f type="tfw">{slot}</f>' if slot else ""
    kids = "".join(f'<child nid="{child}"/>' for child in children)
    return (
        f'<node nid="{nid}" from="{start}" to="{end}" chosen="{chosen}">'
        f"<nonterminal><category>{category}</category>{slot_f}{pola}</nonterminal>"
        f'<children rule="{rule}" chosen="{chosen}">{kids}</children>'
        f"</node>"
    )


#: Tag czasownika, po który nie sięga żadna produkcja, więc zdanie z nim
#: wychodzi odrzucone i te testy mają czym mierzyć odrzucenie. Imiesłów
#: przysłówkowy, czyli konstrukcja, której podzbiór nie ma
#: (docs/subset.md#what-it-does-not-cover-yet).
POZA_PODZBIOREM = "pcon:imperf"


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


def test_a_phrase_case_reads_the_same_whether_written_in_polish_or_latin():
    """Składnica pisze przypadek raz po polsku, raz po łacinie, w jednym wydaniu.

    Sonda pytająca o przypadek frazy dostałaby bez tego przekładu dwie odpowiedzi
    na jedną konstrukcję i policzyła każdą z nich osobno.
    """
    po_polsku = phrase(0, 0, 1, "fno", [1], przypadek="cel") + terminal(1, 0, 1, "mu", "ppron3")
    po_łacinie = po_polsku.replace(">cel<", ">dat<")

    assert constituents(forest(po_polsku))[0].przypadek == "dat"
    assert constituents(forest(po_łacinie))[0].przypadek == "dat"


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
    assert sentence.spans("podmiot") == frozenset({(0, 1)})


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
    assert parse_forest(forest(SVO)).spans("podmiot") == frozenset({(0, 1)})


def test_a_bare_subject_slot_counts_too():
    #  Składnica writes both subj and subj(np(nom)).
    assert parse_forest(forest(svo(subject="subj"))).spans("podmiot") == frozenset({(0, 1)})


def test_an_accusative_object_slot_is_read_as_an_object():
    assert parse_forest(forest(SVO)).spans("dopełnienie") == frozenset({(2, 3)})


@pytest.mark.parametrize("slot", ["np(bier)", "np(acc)", "np(accgen)"])
def test_the_object_slot_is_recognized_under_either_naming(slot):
    #  Cases are named in Polish and in Latin interchangeably, sometimes in one
    #  frame, so bier and acc have to mean the same thing.
    assert parse_forest(forest(svo(obj=slot))).spans("dopełnienie") == frozenset({(2, 3)})


@pytest.mark.parametrize("slot", ["np(dat)", "np(cel)", "np(gen)", "np(dop)"])
def test_dopełnienie_w_przypadku_z_leksykonu_jest_dopełnieniem(slot):
    #  Celownik i dopełniacz są u olskiego pozycją dopełnienia, bo wpuszcza je
    #  leksykon (`DOKŁADANE` w `olski/subset/rama.py`), więc drzewo wzorcowe ma tu
    #  z czym się zgodzić. Bez tego zdanie nowo przyjęte liczy się w tabeli
    #  zgodności jako niezgodne, choć rozeszła się sama nazwa roli.
    assert parse_forest(forest(svo(obj=slot))).spans("dopełnienie") == frozenset({(2, 3)})


def test_the_partitive_object_slot_is_read_as_an_object():
    #  `np(part)` jest nazwą banku drzew na dopełnienie, którego przypadek
    #  rozstrzygają czasownik i przeczenie razem — `Kampania nie przyniosła
    #  skutku.`, `Marzec przyniósł 6 zagranicznych delegacji.` — więc rola jest
    #  tam ta sama co pod `np(accgen)`. Bez tego odwzorowania gold nie ma
    #  dopełnienia, z którym można by się zgodzić, i dobre czytanie liczy się w
    #  tabeli zgodności jako niezgodne (docs/corpus.md).
    assert parse_forest(forest(svo(obj="np(part)"))).spans("dopełnienie") == frozenset({(2, 3)})


@pytest.mark.parametrize("slot", ["np(inst)", "xp(temp)", "advp", "prepnp(do,gen)"])
def test_a_slot_olski_has_no_role_for_is_not_forced_into_one(slot):
    sentence = parse_forest(forest(svo(obj=slot)))
    assert sentence.spans("dopełnienie") == frozenset()
    assert sentence.spans("podmiot") == frozenset({(0, 1)})


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
    return zmierz_zdanie(sentence, sentence.segments, comparable=True)


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
    assert sentence.spans("podmiot") == frozenset({(0, 1), (1, 2)})
    #  The object slot the gold tree marks is on a span olski calls the verb.
    podmieniony = Sentence(
        sent_id=sentence.sent_id,
        text=sentence.text,
        verdict=sentence.verdict,
        segments=sentence.segments,
        roles=(("dopełnienie", 1, 2), ("podmiot", 0, 1), ("podmiot", 1, 2)),
    )
    assert zmierz_zdanie(podmieniony, podmieniony.segments, comparable=True).agreement == (
        "disagrees"
    )


def test_a_role_the_gold_tree_marks_and_olski_does_not_is_partial_not_agreement():
    #  A second subject, on the verb phrase, that olski assigns nothing to. Its
    #  reading is not contradicted, so it is not a disagreement, and not a
    #  confirmed agreement either.
    extra = svo(verb="subj(np(nom))")
    assert parse_forest(forest(extra)).spans("podmiot") == frozenset({(0, 1), (1, 2)})
    assert outcome(extra).agreement == "partial"


def test_a_rejected_sentence_is_not_asked_about_agreement():
    #  A verb form outside the subset leaves no reading to judge.
    found = outcome(svo(tag=POZA_PODZBIOREM))
    assert found.status == "rejected"
    assert found.agreement is None


def test_a_rejected_sentence_names_the_part_of_speech_it_stopped_on():
    assert outcome(svo(tag=POZA_PODZBIOREM)).blocker == "pcon"


def bez_czasownika():
    """*Cisza.* — zdanie bez czasownika, czyli konstrukcja, której olski nie ma.

    Analiza bierze tu każdą formę zdania i żadna nie domyka całości, więc
    zatrzymanie pada na kropce. Bank drzew jest takich zdań pełny, bo korpus
    prasowy niesie nagłówki i podpisy pod zdjęciami.
    """
    return (
        phrase(0, 0, 2, "wypowiedzenie", [1, 3])
        + phrase(1, 0, 1, "fw", [2], slot="subj(np(nom))")
        + terminal(2, 0, 1, "Cisza", "subst:sg:nom:f", lemma="cisza")
        + terminal(3, 1, 2, ".", "interp")
    )


def test_zdanie_bez_struktury_nad_całością_nie_wpada_do_wiersza_znaku_kończącego():
    #  Dwa zdarzenia, które werdykt rozdziela dwoma zdaniami: zdanie stojące na
    #  przecinku ma formę bez wyprowadzenia, a to doszło do końca i nie domknęło
    #  się. Wiersz `interp` liczył je razem, więc kolejka blokerów obiecywała
    #  interpunkcję tam, gdzie brakuje zdania bez czasownika.
    found = outcome(bez_czasownika(), text="Cisza.")
    assert found.status == "rejected"
    assert found.blocker == NO_STRUCTURE


def test_przebieg_który_nie_pytał_o_zatrzymanie_nie_zlicza_blokerów_z_niczego():
    #  Bloker nazywa formę z miejsca zatrzymania, więc bez tej odpowiedzi
    #  tabela blokerów wyszłaby pusta, jakby żadne zdanie nigdzie nie stanęło.
    zdanie = parse_forest(forest(svo(tag=POZA_PODZBIOREM)))
    bez_pytania = Outcome(
        sentence=zdanie,
        result=parse(GRAMMAR, list(zdanie.segments), zatrzymanie=False),
    )
    assert bez_pytania.status == "rejected"
    with pytest.raises(ValueError, match="zatrzymanie"):
        _ = bez_pytania.blocker


def przyłączenie(subject="subj(np(nom))", obj="np(accgen)", przyimkowe=None):
    """*Program zapisuje ustawienia w pliku.* — dwa czytania, bo przyimek ma dwóch gospodarzy.

    Drzewo wzorcowe daje wyrażenie przyimkowe dopełnieniu, czyli to z dwóch
    czytań, które olski też ma. Oba gniazda są argumentami, żeby test mógł
    przesunąć rolę na frazę, której olski w żadnym czytaniu tak nie nazywa.
    """
    return (
        phrase(0, 0, 6, "wypowiedzenie", [1, 5, 9, 20])
        + phrase(1, 0, 1, "fw", [2], slot=subject)
        + terminal(2, 0, 1, "Program", "subst:sg:nom:m3")
        + phrase(5, 1, 2, "ff", [6])
        + terminal(6, 1, 2, "zapisuje", "fin:sg:ter:imperf", lemma="zapisywać")
        + phrase(9, 2, 5, "fw", [10, 12], slot=obj)
        + terminal(10, 2, 3, "ustawienia", "subst:pl:acc:n", lemma="ustawienie")
        + phrase(12, 3, 5, "fpm", [13, 14], slot=przyimkowe)
        + terminal(13, 3, 4, "w", "prep:loc")
        + terminal(14, 4, 5, "pliku", "subst:sg:loc:m3", lemma="plik")
        + terminal(20, 5, 6, ".", "interp")
    )


PRZYŁĄCZENIE_TEKST = "Program zapisuje ustawienia w pliku."


def test_złote_czytanie_zdania_wieloznacznego_zostaje_odnalezione_wśród_czytań():
    #  Zdanie, którego olski nie przyjmuje, bo czyta je dwoma sposobami. Dotąd
    #  przebieg nie mówił o nim nic poza tym, że coś się wyprowadziło, a czytanie
    #  drzewa wzorcowego jest jednym z tych dwóch.
    found = outcome(przyłączenie(), text=PRZYŁĄCZENIE_TEKST)
    assert found.status == "ambiguous"
    assert found.ocalenie == "survives"
    #  Że numer jest miejscem w kolejności czytań, pilnuje `tests/test_las.py`;
    #  tutaj chodzi o to, że dochodzi on tędy razem z werdyktem.
    assert found.głębokość == 1


def test_złote_czytanie_którego_żadne_z_czytań_nie_daje_wychodzi_przepadłe():
    #  Rola przesunięta na samo `w pliku`: olski ma tam wyrażenie przyimkowe przy
    #  dopełnieniu albo przy zdaniu, a dopełnieniem nie czyni go w żadnym czytaniu.
    found = outcome(przyłączenie(obj=None, przyimkowe="np(accgen)"), text=PRZYŁĄCZENIE_TEKST)
    assert found.status == "ambiguous"
    assert found.ocalenie == "lost"
    assert found.głębokość is None


def test_o_ocalenie_pyta_się_zdania_wieloznacznego_a_nie_przyjętego_ani_odrzuconego():
    #  O zdaniu przyjętym mówi `agreement` i mówi więcej, bo rozdziela czytanie
    #  zawężone od odwróconego, więc dwa liczniki jednej miary policzyłyby je dwa razy.
    assert outcome(SVO).ocalenie is None
    assert outcome(svo(tag=POZA_PODZBIOREM)).ocalenie is None


def test_zdanie_wieloznaczne_bez_złotej_roli_nie_wchodzi_do_mianownika(tmp_path):
    #  Bez tego mianownik zawężałby się sam: zdanie, o które nie ma jak zapytać,
    #  liczyłoby się jako przepadłe.
    write(tmp_path, "a-s.xml", przyłączenie(subject=None, obj=None), text=PRZYŁĄCZENIE_TEKST)
    report = przebieg(pliki(tmp_path), jobs=1)
    assert report.statuses["ambiguous"] == 1
    assert report.ocalenia == {}
    assert report.bez_roli == 1


def test_agreement_is_not_claimed_when_spans_are_not_comparable():
    #  Live morphology numbers positions in characters, so a span from the parser
    #  and a span from the gold tree are not the same kind of thing.
    sentence = parse_forest(forest(SVO))
    found = zmierz_zdanie(sentence, sentence.segments, comparable=False)
    assert found.agreement is None
    assert found.ocalenie is None


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


#: Wybrane drzewo, którego terminale nie pokrywają zdania. Dziura powstaje przez
#: dowiązanie, którego korzeń nie ma — tak gubi węzeł `_gold` — a zakładka przez
#: drugi terminal na rozpiętości, którą pierwszy już zajął.
NIEPOKRYTE = {
    "dziura": SVO.replace('<child nid="9"/>', ""),
    "zakładka": SVO.replace('<child nid="9"/>', '<child nid="9"/><child nid="40"/>')
    + terminal(40, 2, 4, "ustawienia.", "subst:pl:acc:n", lemma="ustawienie"),
}


@pytest.mark.parametrize("nodes", NIEPOKRYTE.values(), ids=NIEPOKRYTE)
def test_terminale_wybranego_drzewa_mają_pokrywać_zdanie_bez_dziur_i_zakładek(nodes):
    #  Dwa miejsca gubią tu węzeł bez słowa i oba stoją na tym, że format tak
    #  znaczy. Zgubiony terminal zabiera zdaniu słowo, a wraz z nim rozpiętość,
    #  na której stoi zgodność ról, i sam z siebie nie mówi o tym nic.
    assert not parse_forest(forest(nodes)).całe


def test_las_z_niepokrytym_zdaniem_jest_meldowany_a_nie_mierzony(tmp_path):
    #  Meldowany, a nie pomijany, bo pokrycie policzone bez niego mówiłoby o
    #  korpusie mniejszym, niż mówi jego mianownik, i nikt by tego nie zobaczył.
    write(tmp_path, "a-s.xml", NIEPOKRYTE["dziura"])
    report = przebieg(pliki(tmp_path), jobs=1)
    assert report.verdicts == {FULL: 1}
    assert report.measured == 0
    assert report.skipped == {"gold terminals do not tile the sentence": 1}


def test_an_unknown_morphology_source_is_refused():
    with pytest.raises(ValueError, match="unknown morphology source"):
        measure([], source="wishful")


def test_the_report_renders_what_it_measured(tmp_path):
    write(tmp_path, "a-s.xml", SVO)
    text = render(przebieg(pliki(tmp_path), jobs=1, keep_examples=1), "Składnica")
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
    #
    #  Szósty las jest wieloznaczny ze złotym czytaniem wśród czytań, żeby przez
    #  scalanie przeszły także dwa liczniki, które tylko takie zdanie zapełnia.
    write(tmp_path, "a-s.xml", SVO, text="Program zapisuje ustawienia.")
    write(tmp_path, "b-s.xml", svo(subject=None, obj=None), sent_id="t/2-s", text="Zapisuje.")
    write(tmp_path, "c-s.xml", svo(tag=POZA_PODZBIOREM), sent_id="t/3-s", text="Zapisał to.")
    write(tmp_path, "d-s.xml", "", verdict="NO_TREE", sent_id="t/4-s", text="Bez drzewa.")
    write(tmp_path, "e-s.xml", "", sent_id="t/5-s", text="Bez morfologii.")
    write(tmp_path, "f-s.xml", przyłączenie(), sent_id="t/6-s", text=PRZYŁĄCZENIE_TEKST)

    ścieżki = pliki(tmp_path)
    całość = measure((read(path) for path in ścieżki), keep_examples=1)
    kawałki = [measure([read(path)], keep_examples=1) for path in ścieżki]
    assert render(scal(kawałki, source="gold", keep_examples=1), "Składnica") == render(
        całość, "Składnica"
    )


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
    assert "no gold role to compare" in render(report, "Składnica")
