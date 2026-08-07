import json

from olski.cli import main

DIRTY = 'Kliknij przycisk "Zapisz".\n'
CLEAN = "Kliknij przycisk „Zapisz”.\n"


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


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


def test_json_output_is_machine_readable(tmp_path, capsys):
    path = write(tmp_path, "dirty.txt", DIRTY)
    assert main([str(path), "--format", "json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["files"] == [str(path)]
    assert payload["findings"][0]["rule"] == "quote-straight"
    assert payload["findings"][0]["line"] == 1
    assert payload["findings"][0]["calibration"] == "uncalibrated"


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
