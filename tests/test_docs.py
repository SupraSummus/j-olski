"""The prose is checked the way the code is.

A renamed section leaves a live-looking link behind,
and nothing in a Markdown file fails when that happens,
so the review pass had to grep for it by hand.
Code names documents too — a docstring cites the section
that owns the decision it implements — and those rot the same way,
out of reach of a check that only reads Markdown.

The check commands are the same problem with something other than a name.
The block in ``CLAUDE.md`` is what a person runs,
the workflow's steps are what a push runs,
and nothing derives one from the other.

A document the README does not list is the same rot with nothing renamed:
it is on no reader's path, and adding one without listing it costs nothing.
Which path a document sits on is what ``docs/roles.md`` names.

A module named in prose rots the same way and used to rot unwatched.
Prose points at code because code owns what is implemented,
so a document naming a module is making a claim about where a fact lives,
and a renamed file leaves that claim looking live.
``docs/architecture.md`` is where the claims are densest,
its whole content being the map from a layer to the module that is one,
and the check that reads it found a deleted test file named in ``TODO.md``.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").glob("*.md"))
#: Every module the repository holds, because a citation rots wherever it
#: stands: in the grammar, in the harness beside it, in a spike whose whole point
#: is a document, or in a test's docstring.
SOURCES = sorted(
    path
    for package in ("olski", "harness", "opowieści", "sonda", "tests")
    for path in (ROOT / package).rglob("*.py")
)
WORKFLOW = ROOT / ".github" / "workflows" / "checks.yml"
RELATIVE_LINK = re.compile(r"\[[^\]]*\]\((?!\w+:)([^)\s]+)\)")
#: A module or data file named inside an inline code span, which is how prose
#: points at the code that owns a fact. Renaming the file leaves the span
#: looking live, exactly as a renamed section leaves a link looking live.
CITED_PATH = re.compile(
    r"`((?:olski|harness|sonda|tests|opowieści|próba)/[\w./ąćęłńóśźżĄĆĘŁŃÓŚŹŻ-]+?\.(?:py|txt))`"
)
#: The one document whose subject is code that is gone: it prices the retired
#: pack at the state it was retired in, and ``CLAUDE.md`` says nothing in it is
#: to be recomputed. A module name there is about that program, not about this
#: one, so it outlives the file the same way its figures do.
O_USUNIĘTYM = "firing-rates.md"
CITED_DOCUMENT = re.compile(r"docs/[\w-]+\.md(?:#[\w-]+)?")
#: An entry in the README's list of documents, which is the only place that
#: puts a document on somebody's path.
LISTED_DOCUMENT = re.compile(r"(?m)^- \[docs/([\w-]+\.md)\]")
HEADING = re.compile(r"(?m)^#+\s+(.*)$")
LISTED_CHECKS = re.compile(r"(?ms)^## Checks\n.*?^```sh\n(.*?)^```")
WORKFLOW_STEP = re.compile(r"(?m)^\s*- run: (.*)$")


def anchor_of(heading: str) -> str:
    """Slug a heading as GitHub does for ordinary headings: fold case, drop punctuation."""
    return re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", heading.strip().lower()))


def assert_resolves(destination: Path, anchor: str, origin: str) -> None:
    assert destination.exists(), f"{origin} names a document that is not there"
    if anchor:
        headings = HEADING.findall(destination.read_text())
        assert anchor in {anchor_of(heading) for heading in headings}, (
            f"{origin} names #{anchor}, which no heading in {destination.name} makes"
        )


def relative_links():
    return [
        pytest.param(document, link.group(1), id=f"{document.name} -> {link.group(1)}")
        for document in DOCUMENTS
        for link in RELATIVE_LINK.finditer(document.read_text())
    ]


def cited_documents():
    return [
        pytest.param(source, citation.group(0), id=f"{source.name} -> {citation.group(0)}")
        for source in SOURCES
        for citation in CITED_DOCUMENT.finditer(source.read_text())
    ]


def cited_paths():
    return [
        pytest.param(document, cited.group(1), id=f"{document.name} -> {cited.group(1)}")
        for document in DOCUMENTS
        if document.name != O_USUNIĘTYM
        for cited in CITED_PATH.finditer(document.read_text())
    ]


@pytest.mark.parametrize(("document", "target"), cited_paths())
def test_every_module_named_in_prose_is_there(document: Path, target: str):
    assert (ROOT / target).exists(), f"{document.name} names {target}, which is not there"


@pytest.mark.parametrize(("document", "target"), relative_links())
def test_every_relative_link_resolves(document: Path, target: str):
    path, _, anchor = target.partition("#")
    assert_resolves(document.parent / path if path else document, anchor, document.name)


@pytest.mark.parametrize(("source", "target"), cited_documents())
def test_every_document_cited_from_code_resolves(source: Path, target: str):
    path, _, anchor = target.partition("#")
    assert_resolves(ROOT / path, anchor, source.name)


def test_every_document_is_listed_in_the_readme():
    listed = set(LISTED_DOCUMENT.findall((ROOT / "README.md").read_text()))
    assert {path.name for path in (ROOT / "docs").glob("*.md")} == listed


def test_the_checks_a_person_runs_are_the_checks_a_push_runs():
    listed = LISTED_CHECKS.search((ROOT / "CLAUDE.md").read_text())
    assert listed, "CLAUDE.md has no Checks section carrying a shell block"
    assert listed.group(1).splitlines() == WORKFLOW_STEP.findall(WORKFLOW.read_text())
