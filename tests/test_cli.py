import json

from olski.cli import ONE_SIDED, _calibration, main
from olski.rules import OWED, Audit, Pack

DIRTY = 'Kliknij przycisk "Zapisz".\n'
CLEAN = "Kliknij przycisk „Zapisz”.\n"

#: Ten words and four straight quotation marks, so that a rate over it is a
#: number an assertion can name rather than one the test has to recompute.
TEN_WORDS = 'Kliknij przycisk "Zapisz" i zamknij okno "Ustawienia" w tym module.\n'


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def row(out, rule_id):
    """One rule's row of a report, with the column padding taken out."""
    line = next((line for line in out.splitlines() if line.startswith(f"{rule_id} ")), "")
    return " ".join(line.split())


def test_clean_file_exits_zero(tmp_path, capsys):
    assert main([str(write(tmp_path, "clean.txt", CLEAN))]) == 0
    assert "no findings in 1 file" in capsys.readouterr().out


def test_findings_exit_one_and_report_a_location(tmp_path, capsys):
    path = write(tmp_path, "dirty.txt", DIRTY)
    assert main([str(path)]) == 1
    out = capsys.readouterr().out
    assert f"{path}:1:18: warning: [quote-straight]" in out
    assert "2 findings in 1 file from 1 rule" in out


def test_missing_path_exits_two(tmp_path, capsys):
    assert main([str(tmp_path / "absent.txt")]) == 2
    assert "no such file or directory" in capsys.readouterr().err


def test_no_paths_exits_two(capsys):
    assert main([]) == 2
    assert "give at least one file" in capsys.readouterr().err


def test_a_directory_is_walked_for_text_files(tmp_path, capsys):
    write(tmp_path, "one.txt", DIRTY)
    (tmp_path / "nested").mkdir()
    write(tmp_path / "nested", "two.txt", DIRTY)
    # Not plain text, so the walk leaves it alone. Naming it lints it anyway,
    # for the rules a character settles; the next test is that difference.
    write(tmp_path, "three.md", DIRTY)
    assert main([str(tmp_path)]) == 1
    assert "in 2 files" in capsys.readouterr().out


def test_the_walk_says_how_many_files_it_went_past_and_in_which_formats(tmp_path, capsys):
    #  Without the notice the run below reports over one file of English and
    #  reads as a report over the directory.
    write(tmp_path, "licence.txt", CLEAN)
    write(tmp_path, "one.md", DIRTY)
    write(tmp_path, "two.md", DIRTY)
    write(tmp_path, "logo.png", "")
    assert main([str(tmp_path)]) == 0
    err = capsys.readouterr().err
    assert "went past 3 files in a format olski does not read as prose" in err
    #  The suffixes, most common first, are what say whether the answer is the
    #  extraction or a different directory.
    assert "(.md, .png)" in err
    assert "harness.markdown" in err


def test_the_walk_is_quiet_where_it_went_past_nothing(tmp_path, capsys):
    write(tmp_path, "one.txt", CLEAN)
    assert main([str(tmp_path)]) == 0
    assert capsys.readouterr().err == ""


def test_naming_a_markup_file_is_not_reported_as_going_past_it(tmp_path, capsys):
    #  Naming a file is the move the notice recommends, so making it and being
    #  told the file was skipped would contradict the advice.
    path = write(tmp_path, "note.md", DIRTY)
    assert main([str(path)]) == 1
    assert "went past" not in capsys.readouterr().err


def test_the_walk_reads_a_suffix_the_way_naming_the_file_would(tmp_path, capsys):
    #  One list of suffixes, read through one function, so that a walk and a
    #  named path cannot disagree about what a file is.
    write(tmp_path, "SZUM.TXT", DIRTY)
    assert main([str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert "2 findings in 1 file" in captured.out
    assert captured.err == ""


def test_a_named_markup_file_is_linted_for_what_a_character_settles(tmp_path, capsys):
    path = write(tmp_path, "note.md", 'Kliknij przycisk "Zapisz" — tak.\n')
    assert main([str(path), "--show-abstentions"]) == 1
    captured = capsys.readouterr()
    #  A straight quotation mark is a straight quotation mark in any format.
    assert "[quote-straight]" in captured.out
    #  A rate over the whole file would be a rate over its markup as well.
    assert "abstained: [em-dash-density]" in captured.out
    assert "declined on 1 file in a format olski does not read" in captured.err


def test_the_markup_notice_speaks_only_where_a_rule_actually_declined(tmp_path, capsys):
    #  With one character rule selected nothing was suppressed, so a line saying
    #  rules declined would be telling the reader about something that did not
    #  happen.
    path = write(tmp_path, "note.md", 'Kliknij przycisk "Zapisz" — tak.\n')
    assert main([str(path), "--rule", "quote-straight"]) == 1
    assert capsys.readouterr().err == ""


def test_rule_selection_narrows_what_runs(tmp_path, capsys):
    path = write(tmp_path, "dirty.txt", 'Zapisz  plik "tak".\n')
    assert main([str(path), "--rule", "double-space"]) == 1
    out = capsys.readouterr().out
    assert "double-space" in out
    assert "quote-straight" not in out


def test_unknown_pack_selection_exits_two(tmp_path, capsys):
    path = write(tmp_path, "clean.txt", CLEAN)
    assert main([str(path), "--pack", "fiction"]) == 2
    assert "no rules selected" in capsys.readouterr().err


def test_explain_prints_the_justification_and_the_calibration_state(tmp_path, capsys):
    path = write(tmp_path, "dirty.txt", DIRTY)
    main([str(path), "--explain"])
    out = capsys.readouterr().out
    assert "Polish typography uses" in out
    assert "calibration: uncalibrated" in out
    assert "see docs/linter.md#typography-tier-a" in out


def test_an_uncalibrated_rule_names_the_measurement_it_is_waiting_for(capsys):
    #  Which shape a rule owes is which corpus the first measurement needs, and
    #  reading it off the check kind is the lookup this line exists to save. The
    #  shipped pack reaches both shapes, so both phrases have to come out.
    assert main(["--list-rules", "--explain"]) == 0
    lines = capsys.readouterr().out.splitlines()
    printed = {line.split("calibration: ")[1] for line in lines if "calibration: " in line}
    assert printed == {f"uncalibrated; owes {phrase}" for phrase in OWED.values()}


def test_a_measured_rule_reports_its_numbers_and_owes_nothing():
    #  What a rule owes is what it has not got, so the phrase goes the moment
    #  somebody takes the measurement.
    rule = Pack(name="p").rule(
        id="a",
        check="pattern",
        params=dict(pattern="a"),
        message="m",
        justification="j",
        calibration=Audit(hits=124, defects=119, corpus="drafts-2026", taken="2026-08-07"),
    )
    assert _calibration(rule) == str(rule.calibration)


def test_json_output_is_machine_readable(tmp_path, capsys):
    path = write(tmp_path, "dirty.txt", DIRTY)
    assert main([str(path), "--format", "json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["files"] == [str(path)]
    assert payload["findings"][0]["rule"] == "quote-straight"
    assert payload["findings"][0]["line"] == 1
    assert payload["findings"][0]["calibration"] == "uncalibrated"


def test_the_report_rates_every_rule_including_the_ones_that_found_nothing(tmp_path, capsys):
    path = write(tmp_path, "text.txt", TEN_WORDS)
    assert main([str(path), "--format", "report"]) == 1
    out = capsys.readouterr().out
    assert "1 file, 10 words, 1 sentence, 9 rules" in out
    assert row(out, "quote-straight") == "quote-straight 4 0 10 words 400.0 per 1000"
    #  Whether a rule has anything to do is half of what the rate is asked, so a
    #  rule that ran and found nothing gets a row rather than being left out.
    assert row(out, "double-space") == "double-space 0 0 10 words 0.0 per 1000"


def test_a_rule_reporting_on_a_whole_scope_is_rated_over_scopes_and_not_over_words(
    tmp_path, capsys
):
    write(tmp_path, "one.txt", TEN_WORDS)
    write(tmp_path, "two.txt", TEN_WORDS)
    main([str(tmp_path), "--format", "report"])
    out = capsys.readouterr().out
    #  em-dash-density fires at most once per document, so a rate per thousand
    #  words would be the rate of something that cannot happen.
    assert row(out, "em-dash-density") == "em-dash-density 0 0 2 documents 0.0%"


def test_a_rule_that_abstained_everywhere_reports_no_rate_rather_than_a_rate_of_zero(
    tmp_path, capsys
):
    path = write(tmp_path, "note.md", TEN_WORDS)
    main([str(path), "--format", "report"])
    out = capsys.readouterr().out
    #  Zero would say the rule looked at the document and found nothing in it.
    assert row(out, "em-dash-density") == "em-dash-density 0 1 0 documents —"
    #  On the same corpus a rule that could measure reports zero, which is what
    #  the row above would be indistinguishable from.
    assert row(out, "quote-straight") == "quote-straight 4 0 10 words 400.0 per 1000"


def test_the_report_names_why_a_rule_abstained_when_asked(tmp_path, capsys):
    path = write(tmp_path, "note.md", TEN_WORDS)
    main([str(path), "--format", "report", "--show-abstentions"])
    out = capsys.readouterr().out
    assert "em-dash-density abstained:" in out
    assert "1  this file is not plain text" in out


def test_the_report_says_that_it_is_one_side_of_the_pair(tmp_path, capsys):
    #  Without it a table pasted somewhere else reads as a ranking of rules,
    #  which is the one thing a run over a single corpus cannot produce.
    path = write(tmp_path, "text.txt", TEN_WORDS)
    main([str(path), "--format", "report"])
    assert ONE_SIDED in " ".join(capsys.readouterr().out.split())


def test_list_rules_shows_the_pack_and_exits_zero(capsys):
    assert main(["--list-rules"]) == 0
    out = capsys.readouterr().out
    assert "quote-straight  [typography, tier A, technical, general]" in out
    assert "em-dash-density  [typography, tier A, technical]" in out


def test_abstentions_are_reported_only_when_asked(tmp_path, capsys):
    #  Nothing abstains on plain text, so asking is quiet rather than noisy.
    path = write(tmp_path, "clean.txt", CLEAN)
    main([str(path), "--show-abstentions"])
    assert "abstained" not in capsys.readouterr().out


def test_a_project_pack_can_replace_the_shipped_one(tmp_path, capsys):
    pack = write(
        tmp_path,
        "project.py",
        "from olski.rules import Pack\n"
        "pack = Pack(name='project', registers=('technical',))\n"
        "pack.rule(id='dedykowany', check='pattern', params=dict(pattern=r'dedykowan\\w+'),\n"
        "          message='calque {match}; Polish has osobny or przeznaczony',\n"
        "          justification='An English calque with ordinary Polish equivalents.')\n",
    )
    text = write(tmp_path, "text.txt", 'Mamy dedykowany serwer i "cytat".\n')
    assert main([str(text), "--packs", str(pack)]) == 1
    out = capsys.readouterr().out
    assert "[dedykowany] calque dedykowany" in out
    assert "quote-straight" not in out


def test_a_broken_project_pack_exits_two(tmp_path, capsys):
    pack = write(tmp_path, "broken.py", "from olski.rules import Pack\npack = Pack(name='x')\n")
    text = write(tmp_path, "text.txt", CLEAN)
    assert main([str(text), "--packs", str(pack)]) == 2
    assert "declares no rules" in capsys.readouterr().err


def test_unreadable_file_exits_two(tmp_path, capsys):
    path = tmp_path / "binary.txt"
    path.write_bytes(b"\xff\xfe\x00garbage")
    assert main([str(path)]) == 2
    assert "could not read" in capsys.readouterr().err
