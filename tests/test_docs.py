"""The prose is checked the way rules are checked.

A renamed section leaves a live-looking link behind,
and nothing in a Markdown file fails when that happens,
so the review pass had to grep for it by hand.
Code names documents too — a rule's ``sources`` cite the section
its justification comes from — and those rot the same way,
out of reach of a check that only reads Markdown.

The check commands are the same problem with something other than a name.
The block in ``CLAUDE.md`` is what a person runs,
the workflow's steps are what a push runs,
and nothing derives one from the other.

A document the README does not list is the same rot with nothing renamed:
it is on no reader's path, and adding one without listing it costs nothing.
Which path a document sits on is what ``docs/roles.md`` names.

The last of them is the linter turned on the prose that asks for it. While a
document stands in English the rules have nothing to measure over it, so the
demand that this repository not trip over what its own tool reports is a
declaration; over a document written in Polish it is a check, and this is where
it runs. It runs the same way over a docstring and a block of comment, which the
language rule counts as prose like any other and docs/prose-in-code.md extracts.
"""

import re
from pathlib import Path

import pytest

from harness import polish_share
from harness.markdown import prose
from harness.python import jednostki
from olski.document import WORD
from olski.engine import lint_text
from olski.rules import load_packs

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").glob("*.md"))
#: Every module the repository holds, because a citation rots wherever it
#: stands: in the linter, in the harness beside it, or in a test's docstring.
SOURCES = sorted(
    path for package in ("olski", "harness", "tests") for path in (ROOT / package).rglob("*.py")
)
WORKFLOW = ROOT / ".github" / "workflows" / "checks.yml"
#: Where a document counts as Polish, which is where it counts as translated.
#: ``harness/__init__.py`` owns the measurement, and this sits at the bottom of
#: the range it puts Polish in rather than in the gap below it, because the gap is
#: where a document being translated section by section sits. Selecting one is
#: what the threshold is set high to avoid: the pack pointed at the English half
#: of a mixed file reports Polish typography over English sentences.
POLISH = 0.13

#: Gdzie po polsku jest jednostka kodu, czyli docstring albo blok komentarza.
#: Próg jest wyżej niż nad dokumentem i ma pod sobą podłogę, bo populacje leżą
#: tu bliżej siebie: komentarz po angielsku cytuje polskie przykłady, a
#: jednostka bywa krótsza od zdania, więc udział liczony nad nią skacze o całe
#: dziesiąte części. Liczb nie zapisujemy, bo mierzy się je nad prozą tego
#: repozytorium i rusza je każde przeredagowanie komentarza, a nie zmiana w
#: kodzie; poleceniem, które ten dobór odtwarza, jest::
#:
#:     python3 -m harness.python olski harness tests --into proza/ \
#:         --polish 0.12 --min-words 20
POLISH_UNIT, UNIT_FLOOR = 0.12, 20
RELATIVE_LINK = re.compile(r"\[[^\]]*\]\((?!\w+:)([^)\s]+)\)")
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


@pytest.mark.parametrize(("document", "target"), relative_links())
def test_every_relative_link_resolves(document: Path, target: str):
    path, _, anchor = target.partition("#")
    assert_resolves(document.parent / path if path else document, anchor, document.name)


@pytest.mark.parametrize(("source", "target"), cited_documents())
def test_every_document_cited_from_code_resolves(source: Path, target: str):
    path, _, anchor = target.partition("#")
    assert_resolves(ROOT / path, anchor, source.name)


def polish_documents():
    extracted = [(document, prose(document.read_text())) for document in DOCUMENTS]
    return [
        pytest.param(text, id=document.name)
        for document, text in extracted
        if polish_share(text) >= POLISH
    ]


@pytest.mark.parametrize("text", polish_documents())
def test_every_polish_document_passes_the_linter_this_repository_is_about(text: str):
    report = lint_text(text, load_packs())
    #  The findings rather than their count, so that a failure reads as the
    #  sentence somebody would have to fix.
    assert [f"{finding.rule.id}: {finding.message}" for finding in report.sorted()] == []


def polskie_jednostki():
    return [
        pytest.param(jednostka.tekst, id=f"{source.relative_to(ROOT)}:{jednostka.wiersz}")
        for source in SOURCES
        for jednostka in jednostki(source.read_text())
        if polish_share(jednostka.tekst) >= POLISH_UNIT
        and len(WORD.findall(jednostka.tekst)) >= UNIT_FLOOR
    ]


@pytest.mark.parametrize("tekst", polskie_jednostki())
def test_każda_polska_jednostka_kodu_przechodzi_przez_linter(tekst: str):
    """Nad dokumentem to samo żądanie stoi wyżej, a niżej stała deklaracja.

    Reguła językowa robi z docstringa i komentarza prozę, którą to repozytorium
    pisze o sobie po polsku, i przybywa jej przy każdej zmianie w kodzie.
    Dopóki nie ma czym wyjąć tej prozy z modułu, żądanie, żeby nie potykała się
    o to, co linter wytyka, jest nad nią deklaracją; ekstrakcja jest tym, co
    sprowadza je do checka.
    """
    report = lint_text(tekst, load_packs())
    #  Znaleziska, a nie ich liczba, żeby porażka czytała się jak zdanie, które
    #  ktoś ma poprawić.
    assert [f"{finding.rule.id}: {finding.message}" for finding in report.sorted()] == []


def test_every_document_is_listed_in_the_readme():
    listed = set(LISTED_DOCUMENT.findall((ROOT / "README.md").read_text()))
    assert {path.name for path in (ROOT / "docs").glob("*.md")} == listed


def test_the_checks_a_person_runs_are_the_checks_a_push_runs():
    listed = LISTED_CHECKS.search((ROOT / "CLAUDE.md").read_text())
    assert listed, "CLAUDE.md has no Checks section carrying a shell block"
    assert listed.group(1).splitlines() == WORKFLOW_STEP.findall(WORKFLOW.read_text())
