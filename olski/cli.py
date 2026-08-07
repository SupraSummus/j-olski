"""The command line interface."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from pathlib import Path
from textwrap import fill

from olski import __version__
from olski.checks import NOT_PLAIN_TEXT, ParamError, count_units
from olski.document import TEXT_SUFFIXES, Document
from olski.engine import Report, Tally, lint_corpus, lint_text, read
from olski.rules import PACK_PACKAGE, Rule, RuleError, load_packs, select

USAGE = """
  olski text.txt                 lint a file
  olski notes/ --explain         lint a directory, with each rule's reasoning
  olski notes/ --format report   what each rule did over the corpus
  olski --list-rules             show the rules that would run
"""

#: What a firing rate cannot say. Printed under every report as well as in the
#: help, because a table pasted somewhere else arrives without the help text.
ONE_SIDED = (
    "A firing rate says whether a rule has anything to do, not whether it can be "
    "trusted, and ranking rules by what they discriminate needs the human half of "
    "the pair; see docs/roadmap.md#milestone-1-the-calibration-harness."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="olski",
        description="A style linter for Polish technical documentation.",
        epilog=USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="*", help="files or directories of plain Polish text")
    parser.add_argument(
        "--packs",
        metavar="PATH",
        action="append",
        default=[],
        help=f"pack module, .py file, or directory of them (default: {PACK_PACKAGE})",
    )
    parser.add_argument(
        "--pack",
        metavar="NAME",
        action="append",
        default=[],
        help="only run rules from this pack; repeatable",
    )
    parser.add_argument(
        "--rule",
        metavar="ID",
        action="append",
        default=[],
        help="only run this rule id, '*' allowed; repeatable",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json", "report"),
        default="text",
        help="output format (default: text). 'report' gives a per-rule firing rate "
        f"over the corpus. {ONE_SIDED}",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="print each finding's justification and sources",
    )
    parser.add_argument(
        "--show-abstentions",
        action="store_true",
        help="report rules that declined to fire, and why",
    )
    parser.add_argument(
        "--list-rules",
        action="store_true",
        help="print the selected rules and exit",
    )
    parser.add_argument("--version", action="version", version=f"olski {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    out = sys.stdout

    try:
        rules = select(load_packs(args.packs or None), args.pack, args.rule)
    except (RuleError, ParamError) as error:
        print(f"olski: {error}", file=sys.stderr)
        return 2

    if not rules:
        print("olski: no rules selected", file=sys.stderr)
        return 2

    if args.list_rules:
        _list_rules(rules, out, args.explain)
        return 0

    if not args.paths:
        parser.print_usage(sys.stderr)
        print("olski: give at least one file or directory to lint", file=sys.stderr)
        return 2

    files, missing = _collect(args.paths)
    for path in missing:
        print(f"olski: no such file or directory: {path}", file=sys.stderr)

    documents, errors = _read(files)
    report = lint_corpus(documents, rules)
    report.errors.extend(errors)
    if not files and not missing:
        print("olski: nothing to lint", file=sys.stderr)
    _note_markup(report)

    if args.format == "json":
        json.dump(_as_json(report, args), out, ensure_ascii=False, indent=2)
        out.write("\n")
    elif args.format == "report":
        _write_report(report, out, args, rules)
    else:
        _write_text(report, out, args)

    for path, reason in report.errors:
        print(f"olski: could not read {path}: {reason}", file=sys.stderr)

    if missing or report.errors:
        return 2
    return 1 if report.findings else 0


def lint_string(text: str, path: str = "<text>") -> Report:
    """Lint a string with the shipped packs. The convenient entry point."""
    return lint_text(text, load_packs(), path)


def _read(files: Sequence[Path]) -> tuple[list[Document], list[tuple[str, str]]]:
    """Read every file before linting any of them.

    A rule may be measuring the corpus rather than a file, so the whole corpus
    has to exist before the first rule runs.
    """
    documents: list[Document] = []
    errors: list[tuple[str, str]] = []
    for file in files:
        document, error = read(file)
        if document is None:
            errors.append((str(file), error))
        else:
            documents.append(document)
    return documents, errors


def _note_markup(report: Report) -> None:
    """Say once that a rule declined because the input was not plain text.

    Abstentions are quiet unless asked for, so a run over Markdown would
    otherwise read as a run over prose that happened to find less. Counted off
    the report rather than off the input, because a run that selected only the
    rules a character settles lost nothing and needs no notice.
    """
    declined = {a.path for a in report.abstentions if a.reason == NOT_PLAIN_TEXT}
    if not declined:
        return
    print(
        f"olski: the rules that measure a whole file declined on "
        f"{_count(len(declined), 'file')} in a format olski does not read as prose; "
        "--show-abstentions names them",
        file=sys.stderr,
    )


def _collect(paths: Sequence[str]) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    missing: list[str] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(
                sorted(p for p in path.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES)
            )
        elif path.is_file():
            files.append(path)
        else:
            missing.append(raw)
    return files, missing


def _write_text(report: Report, out, args) -> None:
    for finding in report.sorted():
        rule = finding.rule
        out.write(f"{finding.location}: {rule.severity}: [{rule.id}] {finding.message}\n")
        if args.explain:
            out.write(_indent(rule.justification))
            for source in rule.sources:
                out.write(f"    see {source}\n")
            out.write(f"    calibration: {rule.calibration}\n")

    if args.show_abstentions:
        for abstention in report.abstentions:
            out.write(f"{abstention.path}: abstained: [{abstention.rule.id}] {abstention.reason}\n")

    out.write(_summary(report) + "\n")


def _summary(report: Report) -> str:
    if not report.findings:
        return f"no findings in {_count(len(report.paths), 'file')}"
    rules = len({f.rule.id for f in report.findings})
    return (
        f"{_count(len(report.findings), 'finding')} "
        f"in {_count(len(report.paths), 'file')} "
        f"from {_count(rules, 'rule')}"
    )


#: Nouns in the output whose plural is not the singular with an s.
PLURALS = {"corpus": "corpora"}


def _count(number: int, noun: str) -> str:
    return f"{number} {noun}" if number == 1 else f"{number} {PLURALS.get(noun, noun + 's')}"


#: The report's columns, and which way each one reads: a name from the left, a
#: number from the right.
REPORT_COLUMNS = (
    ("rule", "<"),
    ("fired", ">"),
    ("abstained", ">"),
    ("measured", ">"),
    ("rate", ">"),
)


def _write_report(report: Report, out, args, rules: list[Rule]) -> None:
    """Print what each rule did over the corpus, one row per rule.

    Ordered by rule id rather than by rate. The rates are in different units, so
    sorting on them would rank a share of documents against a count per thousand
    words, and a fixed order is what lets two runs be put side by side.
    """
    out.write(
        f"{_count(len(report.documents), 'file')}, "
        f"{_count(count_units('word', report.documents), 'word')}, "
        f"{_count(len(rules), 'rule')}\n\n"
    )
    ordered = sorted(report.tally(rules), key=lambda tally: tally.rule.id)
    out.write(_table(_cells(tally) for tally in ordered))
    if args.show_abstentions:
        _write_reasons(report, out)
    out.write("\n" + fill(ONE_SIDED, width=76) + "\n")


def _cells(tally: Tally) -> tuple[str, ...]:
    """One rule's row, in the order :data:`REPORT_COLUMNS` names the columns."""
    return (
        tally.rule.id,
        str(tally.findings),
        str(tally.abstentions),
        _count(tally.measured, tally.unit),
        _rate(tally),
    )


def _rate(tally: Tally) -> str:
    """How often a rule fired over what it measured.

    A share where the check fires at most once per unit, and a rate per thousand
    words where it has no such bound and fires as often as the prose gives it
    cause. An em dash where the rule measured nothing, since a rule that
    declined everywhere has no rate, and 0 is the answer of a rule that looked.
    """
    if tally.rate is None:
        return "—"
    if tally.unit == "word":
        return f"{1000 * tally.rate:.1f} per 1000"
    return f"{tally.rate:.1%}"


def _table(rows: Iterable[Sequence[str]]) -> str:
    """Lay rows out under the column headings, each column as wide as it needs."""
    headings = tuple(heading for heading, _ in REPORT_COLUMNS)
    lines = [headings, *rows]
    widths = [max(len(cell) for cell in column) for column in zip(*lines, strict=True)]
    return "".join(
        "  ".join(
            f"{cell:{align}{width}}"
            for cell, (_, align), width in zip(line, REPORT_COLUMNS, widths, strict=True)
        ).rstrip()
        + "\n"
        for line in lines
    )


def _write_reasons(report: Report, out) -> None:
    """Why each rule that abstained did, with the reasons counted.

    A run over a corpus repeats one reason as often as it has files, so what a
    reader can use is the reason and how often it came up rather than a line
    per file.
    """
    reasons: dict[str, Counter] = defaultdict(Counter)
    for abstention in report.abstentions:
        reasons[abstention.rule.id][abstention.reason] += 1
    for rule_id in sorted(reasons):
        out.write(f"\n{rule_id} abstained:\n")
        for reason, count in reasons[rule_id].most_common():
            out.write(_indent(f"{count}  {reason}"))


def _list_rules(rules: list[Rule], out, explain: bool) -> None:
    for rule in rules:
        registers = ", ".join(rule.registers) or "unscoped"
        out.write(f"{rule.id}  [{rule.pack}, tier {rule.tier}, {registers}]\n")
        out.write(f"    {rule.check}: {rule.message}\n")
        if explain:
            out.write(_indent(rule.justification))
            for source in rule.sources:
                out.write(f"    see {source}\n")
            out.write(f"    calibration: {rule.calibration}\n")
    out.write(_count(len(rules), "rule") + "\n")


def _indent(prose: str, width: int = 76) -> str:
    return fill(prose, width=width, initial_indent="    ", subsequent_indent="    ") + "\n"


def _as_json(report: Report, args) -> dict:
    payload = {
        "files": report.paths,
        "findings": [
            {
                "path": f.path,
                "line": f.line,
                "column": f.column,
                "rule": f.rule.id,
                "pack": f.rule.pack,
                "severity": f.rule.severity,
                "message": f.message,
                "calibration": f.rule.calibration,
                **(
                    {"justification": f.rule.justification, "sources": list(f.rule.sources)}
                    if args.explain
                    else {}
                ),
            }
            for f in report.sorted()
        ],
    }
    if args.show_abstentions:
        payload["abstentions"] = [
            {"path": a.path, "rule": a.rule.id, "reason": a.reason} for a in report.abstentions
        ]
    return payload


if __name__ == "__main__":
    raise SystemExit(main())
