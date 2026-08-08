"""Running rules over a corpus.

The engine knows nothing about Polish. It walks rules, hands each one the corpus
and the check it named, turns every hit into a located finding with a rendered
message, and keeps abstentions separately so that silence-by-decision stays
distinguishable from silence-by-no-match. That distinction survives into
:meth:`Report.tally`, which counts what each rule did over the whole run.

The corpus rather than the document is the unit, because a rule may be asking a
question no single file can answer. One file is a corpus of one, so nothing about
the ordinary case changes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.checks import Abstain, Hit, count_units, get_check
from olski.document import Document, Span, from_text, is_plain_text
from olski.rules import Rule, load_packs


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
    #: Whether the rule declined the file rather than one scope in it. See
    #: :class:`olski.checks.Abstain`, which is where a check says so.
    whole_file: bool = False


@dataclass(frozen=True)
class Tally:
    """What one rule did over a corpus, which is a row of a firing-rate report.

    ``measured`` is how much of ``unit`` the rule reached a verdict on: what the
    corpus held, less what the rule declined. Subtracting is what keeps the two
    silences apart, because a rule that declined everywhere then has nothing to
    divide by and reports no rate rather than a rate of zero.
    """

    rule: Rule
    findings: int
    abstentions: int
    measured: int
    unit: str

    @property
    def rate(self) -> float | None:
        """Findings per unit, and ``None`` where the rule measured nothing."""
        return self.findings / self.measured if self.measured else None


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    abstentions: list[Abstention] = field(default_factory=list)
    #: Files that were read, in the order they were read. The documents rather
    #: than their names, because a rate over the run needs the text to divide by.
    documents: list[Document] = field(default_factory=list)
    #: Files that could not be read, with the reason.
    errors: list[tuple[str, str]] = field(default_factory=list)

    @property
    def paths(self) -> list[str]:
        return [document.path for document in self.documents]

    def sorted(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: (f.path, f.line, f.column, f.rule.id))

    def tally(self, rules: Iterable[Rule]) -> list[Tally]:
        """What each rule did over the run, the ones that did nothing included.

        A rule that neither fired nor declined appears nowhere in a report, and
        whether a rule has anything to do is exactly what a firing rate is
        asked, so the rules are what this walks and the report is what it counts
        against them.
        """
        found = Counter(finding.rule.id for finding in self.findings)
        declined: dict[str, list[Abstention]] = defaultdict(list)
        for abstention in self.abstentions:
            declined[abstention.rule.id].append(abstention)
        return [_tally(rule, self.documents, found[rule.id], declined[rule.id]) for rule in rules]


def _tally(
    rule: Rule, documents: Sequence[Document], findings: int, abstentions: list[Abstention]
) -> Tally:
    unit = get_check(rule.check, f"rule {rule.id}").counted_over(rule.params)
    #  Both kinds of abstention come off the denominator, and they differ in how
    #  much they take with them: a rule that declined a file never saw the scopes
    #  in it, where one that declined a scope saw that scope and no other. Which
    #  of the two it was rides along on the abstention, because it is the check
    #  that knows and a reason string only reads as though it said.
    whole_files = [a for a in abstentions if a.whole_file]
    unread = {abstention.path for abstention in whole_files}
    scopes = count_units(unit, [d for d in documents if d.path not in unread])
    return Tally(
        rule=rule,
        findings=findings,
        abstentions=len(abstentions),
        measured=scopes - (len(abstentions) - len(whole_files)),
        unit=unit,
    )


#: Stands where a path would, for a rule that measured the corpus and found no
#: single file to blame. The angle brackets match ``<text>`` in :func:`lint_text`.
CORPUS = "<corpus>"


def lint_corpus(documents: Sequence[Document], rules: Iterable[Rule]) -> Report:
    report = Report(documents=list(documents))
    for rule in rules:
        check = get_check(rule.check, f"rule {rule.id}")
        for outcome in check.run(rule, documents):
            if isinstance(outcome, Abstain):
                path = outcome.document.path if outcome.document else CORPUS
                report.abstentions.append(
                    Abstention(rule, path, outcome.reason, outcome.whole_file)
                )
            elif isinstance(outcome, Hit):
                report.findings.append(_finding(rule, outcome))
    return report


def lint(document: Document, rules: Iterable[Rule]) -> Report:
    return lint_corpus([document], rules)


def lint_text(text: str, rules: Iterable[Rule], path: str = "<text>") -> Report:
    return lint(from_text(text, path), rules)


def lint_string(text: str, path: str = "<text>") -> Report:
    """Lint a string with the shipped packs. The convenient entry point."""
    return lint_text(text, load_packs(), path)


def read(path: str | Path) -> tuple[Document | None, str]:
    """Read one file into a document, or say why it could not be read.

    A file olski cannot read as prose is read all the same, because the rules
    that point at a site are answerable on it and the reader may well have meant
    to run them. What it does not get is the plain-text guarantee, so the rules
    that measure the whole of it decline instead of reporting a number about
    somebody's markup.
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return None, str(error)
    return from_text(text, str(path), plain_text=is_plain_text(path)), ""


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
