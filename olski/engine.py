"""Running rules over documents.

The engine knows nothing about Polish. It walks rules, hands each one the
document and the check it named, turns every hit into a located finding with a
rendered message, and keeps abstentions separately so that silence-by-decision
stays distinguishable from silence-by-no-match.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

from olski.checks import Abstain, Hit, get_check
from olski.document import Document, Span, from_text
from olski.rules import Rule


@dataclass(frozen=True)
class Finding:
    rule: Rule
    path: str
    line: int
    column: int
    span: Span
    message: str

    @property
    def location(self) -> str:
        return f"{self.path}:{self.line}:{self.column}"


@dataclass(frozen=True)
class Abstention:
    rule: Rule
    path: str
    reason: str


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    abstentions: list[Abstention] = field(default_factory=list)
    #: Files that were read, in the order they were read.
    paths: list[str] = field(default_factory=list)
    #: Files that could not be read, with the reason.
    errors: list[tuple[str, str]] = field(default_factory=list)

    def extend(self, other: Report) -> None:
        self.findings.extend(other.findings)
        self.abstentions.extend(other.abstentions)
        self.paths.extend(other.paths)
        self.errors.extend(other.errors)

    def sorted(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: (f.path, f.line, f.column, f.rule.id))


def lint(document: Document, rules: Iterable[Rule]) -> Report:
    report = Report(paths=[document.path])
    for rule in rules:
        check = get_check(rule.check, f"rule {rule.id}")
        for outcome in check.run(rule, document):
            if isinstance(outcome, Abstain):
                report.abstentions.append(Abstention(rule, document.path, outcome.reason))
            elif isinstance(outcome, Hit):
                report.findings.append(_finding(rule, document, outcome))
    return report


def lint_text(text: str, rules: Iterable[Rule], path: str = "<text>") -> Report:
    return lint(from_text(text, path), rules)


def lint_path(path: str | Path, rules: Iterable[Rule]) -> Report:
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return Report(errors=[(str(path), str(error))])
    return lint_text(text, rules, str(path))


def _finding(rule: Rule, document: Document, hit: Hit) -> Finding:
    line, column = document.position(hit.span.start)
    return Finding(
        rule=rule,
        path=document.path,
        line=line,
        column=column,
        span=hit.span,
        message=rule.format(hit.fields),
    )
