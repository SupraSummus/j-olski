import pytest

from olski import rules as rules_module
from olski.rules import (
    UNCALIBRATED,
    Audit,
    Distribution,
    Pack,
    Rule,
    RuleError,
    load_packs,
    select,
)

AUDIT_NUMBERS = dict(hits=124, defects=119, corpus="drafts-2026", taken="2026-08-07")
SPREAD_NUMBERS = dict(
    median=2.1, accused=0.03, scopes=812, corpus="nkjp-expository", taken="2026-08-07"
)


def test_shipped_packs_load():
    rules = load_packs()
    assert rules
    assert all(isinstance(rule, Rule) for rule in rules)


def test_every_shipped_rule_carries_what_the_roadmap_asks_for():
    for rule in load_packs():
        assert rule.id and rule.pack and rule.registers
        assert rule.message.strip()
        assert rule.justification.strip()


@pytest.mark.parametrize(
    ("check", "params", "calibration"),
    [
        ("pattern", dict(pattern="a"), Audit(**AUDIT_NUMBERS)),
        (
            "pattern-density",
            dict(pattern="a", max_per_1000_words=10),
            Distribution(**SPREAD_NUMBERS),
        ),
    ],
)
def test_a_measured_rule_says_what_its_numbers_were_taken_over(check, params, calibration):
    """Either shape reads back with its provenance, which is what --explain
    prints and what somebody redoing the measurement needs."""
    rule = Pack(name="p").rule(
        id="a",
        check=check,
        params=params,
        message="m",
        justification="j",
        calibration=calibration,
    )
    assert rule.calibration.corpus in str(rule.calibration)
    assert rule.calibration.taken in str(rule.calibration)


def test_an_audit_reports_the_share_of_hits_that_were_real_defects():
    assert Audit(**AUDIT_NUMBERS).precision == pytest.approx(119 / 124)
    assert "96%" in str(Audit(**AUDIT_NUMBERS))


@pytest.mark.parametrize(
    ("shape", "fields", "complaint"),
    [
        (Audit, {**AUDIT_NUMBERS, "hits": 0}, "whole number"),
        (Audit, {**AUDIT_NUMBERS, "defects": 200}, "cannot find"),
        (Audit, {**AUDIT_NUMBERS, "corpus": " "}, "names the corpus"),
        (Audit, {**AUDIT_NUMBERS, "taken": "August 2026"}, "not an ISO date"),
        (Distribution, {**SPREAD_NUMBERS, "accused": 3.0}, "cannot exceed 1"),
        (Distribution, {**SPREAD_NUMBERS, "scopes": 0}, "whole number"),
    ],
)
def test_a_number_no_measurement_could_have_produced_is_refused(shape, fields, complaint):
    with pytest.raises(RuleError, match=complaint):
        shape(**fields)


@pytest.mark.parametrize(
    ("check", "params", "calibration"),
    [
        ("pattern", dict(pattern="a"), "audited over drafts, mostly fine"),
        ("pattern", dict(pattern="a"), Distribution(**SPREAD_NUMBERS)),
        ("pattern-density", dict(pattern="a", max_per_1000_words=10), Audit(**AUDIT_NUMBERS)),
    ],
)
def test_a_rule_carries_only_the_calibration_its_check_calls_for(check, params, calibration):
    """Three ways to get it wrong. Prose says a number was taken without saying
    which, over what, or when. A distribution on a rule with no threshold has no
    threshold to place, and an audit on a rate rule reads hits nobody read."""
    with pytest.raises(RuleError, match="calls for"):
        Pack(name="p").rule(
            id="a",
            check=check,
            params=params,
            message="m",
            justification="j",
            calibration=calibration,
        )


def test_pack_defaults_apply_and_a_rule_can_override_them():
    pack = Pack(name="p", registers=("technical", "general"), severity="warning")
    inherited = pack.rule(
        id="a", check="pattern", params=dict(pattern="a"), message="m", justification="j"
    )
    overridden = pack.rule(
        id="b",
        check="pattern",
        params=dict(pattern="b"),
        message="m",
        justification="j",
        severity="note",
        registers=("technical",),
    )
    assert inherited.pack == "p"
    assert inherited.registers == ("technical", "general")
    assert inherited.severity == "warning"
    assert inherited.calibration is UNCALIBRATED
    assert overridden.severity == "note"
    assert overridden.registers == ("technical",)


def test_prose_written_with_semantic_line_breaks_is_folded():
    rule = Pack(name="p").rule(
        id="a",
        check="pattern",
        params=dict(pattern="a"),
        message="m",
        justification="""
        Pierwsze zdanie.
        Drugie zdanie.
        """,
    )
    assert rule.justification == "Pierwsze zdanie. Drugie zdanie."


def test_duplicate_id_within_a_pack_is_refused():
    pack = Pack(name="p")
    pack.rule(id="a", check="pattern", params=dict(pattern="a"), message="m", justification="j")
    with pytest.raises(RuleError, match="duplicate rule id"):
        pack.rule(id="a", check="pattern", params=dict(pattern="b"), message="m", justification="j")


def test_empty_justification_is_refused():
    with pytest.raises(RuleError, match="justification is empty"):
        Pack(name="p").rule(
            id="a", check="pattern", params=dict(pattern="a"), message="m", justification="   "
        )


def test_unknown_severity_is_refused():
    with pytest.raises(RuleError, match="severity must be one of"):
        Pack(name="p").rule(
            id="a",
            check="pattern",
            params=dict(pattern="a"),
            message="m",
            justification="j",
            severity="shouting",
        )


def test_unknown_tier_is_refused():
    with pytest.raises(RuleError, match="tier must be one of"):
        Pack(name="p").rule(
            id="a",
            check="pattern",
            params=dict(pattern="a"),
            message="m",
            justification="j",
            tier="Z",
        )


def test_select_filters_by_pack_and_by_globbed_id():
    rules = load_packs()
    assert select(rules, packs=["typography"]) == rules
    assert select(rules, packs=["nonexistent"]) == []
    assert [r.id for r in select(rules, ids=["quote-*"])] == ["quote-straight", "quote-english"]
    assert [r.id for r in select(rules, ids=["double-space"])] == ["double-space"]


def test_a_pack_can_be_loaded_from_a_file(tmp_path):
    pack_file = tmp_path / "project.py"
    pack_file.write_text(
        "from olski.rules import Pack\n"
        "pack = Pack(name='project', registers=('technical',))\n"
        "pack.rule(id='no-synergy', check='pattern', params=dict(pattern=r'synergi\\\\w+'),\n"
        "          message='calque {match}', justification='a calque with a Polish equivalent')\n",
        encoding="utf-8",
    )
    rules = load_packs([pack_file])
    assert [r.id for r in rules] == ["no-synergy"]
    assert rules[0].origin.endswith("project.py")


def test_a_pack_directory_can_be_loaded(tmp_path):
    (tmp_path / "one.py").write_text(
        "from olski.rules import Pack\n"
        "pack = Pack(name='one')\n"
        "pack.rule(id='a', check='pattern', params=dict(pattern='a'), message='m',\n"
        "          justification='j')\n",
        encoding="utf-8",
    )
    assert [r.id for r in load_packs([tmp_path])] == ["a"]


def test_a_broken_pack_file_names_itself(tmp_path):
    pack_file = tmp_path / "broken.py"
    pack_file.write_text("raise ValueError('nope')\n", encoding="utf-8")
    with pytest.raises(RuleError, match="broken.py: ValueError: nope"):
        load_packs([pack_file])


def test_a_module_without_a_pack_is_refused(tmp_path):
    pack_file = tmp_path / "empty.py"
    pack_file.write_text("rules = []\n", encoding="utf-8")
    with pytest.raises(RuleError, match="expected a module-level 'pack'"):
        load_packs([pack_file])


def test_a_missing_pack_is_reported(tmp_path):
    with pytest.raises(RuleError, match="no such pack"):
        load_packs([tmp_path / "absent.py"])


def test_ids_are_unique_across_packs(tmp_path):
    first = tmp_path / "first.py"
    second = tmp_path / "second.py"
    body = (
        "from olski.rules import Pack\n"
        "pack = Pack(name='{name}')\n"
        "pack.rule(id='shared', check='pattern', params=dict(pattern='a'), message='m',\n"
        "          justification='j')\n"
    )
    first.write_text(body.format(name="first"), encoding="utf-8")
    second.write_text(body.format(name="second"), encoding="utf-8")
    with pytest.raises(RuleError, match="already declared in"):
        load_packs([first, second])


def test_pack_records_where_it_was_declared():
    assert rules_module.load_packs()[0].origin == "olski.packs.typography"
