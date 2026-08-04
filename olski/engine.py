"""Running rules over a corpus.

The engine knows nothing about Polish. It walks rules, hands each one the corpus
and the check it named, turns every hit into a located finding with a rendered
message, and keeps abstentions separately so that silence-by-decision stays
distinguishable from silence-by-no-match.

The corpus rather than the document is the unit, because a rule may be asking a
question no single file can answer. One file is a corpus of one, so nothing about
the ordinary case changes.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
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


#: Stands where a path would, for a rule that measured the corpus and found no
#: single file to blame. The angle brackets match ``<text>`` in :func:`lint_text`.
CORPUS = "<corpus>"


def lint_corpus(documents: Sequence[Document], rules: Iterable[Rule]) -> Report:
    report = Report(paths=[document.path for document in documents])
    for rule in rules:
        check = get_check(rule.check, f"rule {rule.id}")
        for outcome in check.run(rule, documents):
            if isinstance(outcome, Abstain):
                path = outcome.document.path if outcome.document else CORPUS
                report.abstentions.append(Abstention(rule, path, outcome.reason))
            elif isinstance(outcome, Hit):
                report.findings.append(_finding(rule, outcome))
    return report


def lint(document: Document, rules: Iterable[Rule]) -> Report:
    return lint_corpus([document], rules)


def lint_text(text: str, rules: Iterable[Rule], path: str = "<text>") -> Report:
    return lint(from_text(text, path), rules)


def read(path: str | Path) -> tuple[Document | None, str]:
    """Read one file into a document, or say why it could not be read."""
    path = Path(path)
    try:
        return from_text(path.read_text(encoding="utf-8"), str(path)), ""
    except (OSError, UnicodeDecodeError) as error:
        return None, str(error)


def _finding(rule: Rule, hit: Hit) -> Finding:
    line, column = hit.document.position(hit.span.start)
    return Finding(
        rule=rule,
        path=hit.document.path,
        line=line,
        column=column,
        span=hit.span,
        message=rule.format(hit.fields),
    )
