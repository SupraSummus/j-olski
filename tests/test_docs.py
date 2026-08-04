"""The prose links are checked the way rules are checked.

A renamed section leaves a live-looking link behind,
and nothing in a Markdown file fails when that happens,
so the review pass had to grep for it by hand.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS = sorted(ROOT.glob("*.md")) + sorted((ROOT / "docs").glob("*.md"))
RELATIVE_LINK = re.compile(r"\[[^\]]*\]\((?!\w+:)([^)\s]+)\)")
HEADING = re.compile(r"(?m)^#+\s+(.*)$")


def anchor_of(heading: str) -> str:
    """Slug a heading as GitHub does for ordinary headings: fold case, drop punctuation."""
    return re.sub(r"\s+", "-", re.sub(r"[^\w\s-]", "", heading.strip().lower()))


def relative_links():
    return [
        pytest.param(document, link.group(1), id=f"{document.name} -> {link.group(1)}")
        for document in DOCUMENTS
        for link in RELATIVE_LINK.finditer(document.read_text())
    ]


@pytest.mark.parametrize(("document", "target"), relative_links())
def test_every_relative_link_resolves(document: Path, target: str):
    path, _, anchor = target.partition("#")
    destination = document.parent / path if path else document
    assert destination.exists(), f"{document.name} links to a file that is not there"
    if anchor:
        headings = HEADING.findall(destination.read_text())
        assert anchor in {anchor_of(heading) for heading in headings}, (
            f"{document.name} links to #{anchor}, which no heading in {destination.name} makes"
        )
