"""The command line interface."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from textwrap import fill

from olski import __version__
from olski.checks import NOT_PLAIN_TEXT, ParamError
from olski.document import TEXT_SUFFIXES, Document
from olski.engine import Report, lint_corpus, lint_text, read
from olski.rules import PACK_PACKAGE, Rule, RuleError, load_packs, select

USAGE = """
  olski text.txt                 lint a file
  olski notes/ --explain         lint a directory, with each rule's reasoning
  olski --list-rules             show the rules that would run
"""


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
        choices=("text", "json"),
        default="text",
        help="output format (default: text)",
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


def _count(number: int, noun: str) -> str:
    return f"{number} {noun}" if number == 1 else f"{number} {noun}s"


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
