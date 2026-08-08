import pytest

from olski.calibration import Audit, CalibrationError, Distribution
from olski.checks import CHECKS

AUDIT_NUMBERS = dict(hits=124, defects=119, corpus="drafts-2026", taken="2026-08-07")
SPREAD_NUMBERS = dict(
    median=2.1, accused=0.03, scopes=812, corpus="nkjp-expository", taken="2026-08-07"
)


@pytest.mark.parametrize(
    "calibration", [Audit(**AUDIT_NUMBERS), Distribution(**SPREAD_NUMBERS)], ids=["audit", "spread"]
)
def test_a_measurement_says_what_it_was_taken_over(calibration):
    """Either shape reads back with its provenance, which is what --explain
    prints and what somebody redoing the measurement needs."""
    assert calibration.corpus in str(calibration)
    assert calibration.taken in str(calibration)


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
    with pytest.raises(CalibrationError, match=complaint):
        shape(**fields)


def test_every_shape_a_check_calls_for_says_what_an_uncalibrated_rule_owes():
    """The phrase stands on the shape rather than in a table beside it, so what
    catches a shape shipped without one is this and the --explain that reads it."""
    assert all(check.calibrated_by.owed.strip() for check in CHECKS.values())
