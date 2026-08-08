"""Markdown in, Polish prose out.

The rules that measure a whole file need two guarantees plain text gives and
Markdown does not: every character is prose, and every newline is a newline on
the page. This produces both, by dropping the apparatus and by joining what the
renderer would have joined.

Two decisions run through the whole module and are worth stating once.

**Inline markup is replaced by the text it wrapped, never deleted.** A deletion
leaves the space that stood in front of it, and that space arrives at the rules
as a defect somebody typed: docs/extraction.md holds what that cost the two
extractions written before this one. Where a construct has no text to leave
behind, the space in front of it goes with it.

**A line is a line of source, not a line of the page.** Everything a paragraph
holds is joined with single spaces, so a rule about where a line ends measures
where the prose ends rather than where the author's editor wrapped.

Which documents enter the corpus is the same step's business, and it is the
harness package that holds it: a rate over Polish must not have another language
in its denominator, and the extracted prose is what says which language a file is
in. A document is one unit of that selection, and the case where one document
holds two languages is an entry in TODO.md rather than a case this handles.
"""

from __future__ import annotations

import re
from collections.abc import Sequence

from harness import BULLET, Czytnik, Jednostka, uruchom

MARKDOWN_SUFFIX = ".md"

#: YAML frontmatter: a fence of three dashes opening the file, and everything
#: down to the line that closes it.
FRONTMATTER = re.compile(r"\A---[ \t]*\n.*?\n(?:---|\.\.\.)[ \t]*(?:\n|\Z)", re.DOTALL)

#: An HTML comment, which renders as nothing wherever it stands, taking the
#: whitespace in front of it: a comment closing a line leaves that line empty,
#: and one inside a sentence leaves the sentence spaced as it was written.
COMMENT = re.compile(r"[ \t]*<!--.*?-->", re.DOTALL)

#: A fenced code block's opening or closing line, capturing the fence so that a
#: shorter run of the other character inside the block does not close it.
FENCE = re.compile(r"[ ]{0,3}(`{3,}|~{3,})")

#: One level of blockquote marker, which is apparatus around prose rather than
#: prose: the quoted text is what the reader reads.
BLOCKQUOTE = re.compile(r"[ \t]*>[ \t]?")

HEADING = re.compile(r"[ ]{0,3}#{1,6}(?:[ \t]|\Z)")

#: A table row, recognized by the pipe that opens it. A table written without
#: leading pipes is not recognized, which docs/extraction.md records.
TABLE_ROW = re.compile(r"[ ]{0,3}\|")

#: A line of nothing but rule characters. Under a paragraph it is a setext
#: heading's underline and under a blank line it is a thematic break, and the
#: two need no telling apart: both drop, and a heading drops with its underline.
UNDERLINE = re.compile(r"[ ]{0,3}(?:=+|(?:[-_*][ \t]*){3,})[ \t]*\Z")

#: An item that opens with a link, which is what a list of links is made of.
LINK_ITEM = re.compile(r"\[[^\]]*\]\(")

#: Where a reference link's target is declared. It renders as nothing, so it is
#: apparatus wherever it stands.
LINK_DEFINITION = re.compile(r"[ ]{0,3}\[[^\]]*\]:[ \t]")

#: Every inline construct, in one pass, so that the markers inside a code span
#: are code and the emphasis around a link is emphasis. The leading whitespace
#: is captured with the construct: a construct with nothing inside it takes that
#: whitespace along when it goes.
INLINE = re.compile(
    r"""
    (?P<space>[ \t]*)
    (?:
        \\(?P<escaped>[!-/:-@\[-`{-~])
      | (?P<ticks>`+)(?P<code>.+?)(?P=ticks)
      | !\[(?P<alt>[^\]]*)\](?:\([^)]*\)|\[[^\]]*\])
      | \[(?P<link>[^\]]*)\](?:\([^)]*\)|\[[^\]]*\])
      | <(?P<autolink>[a-zA-Z][\w+.-]*:[^>\s]*)>
      | \*\*(?P<strong>\S(?:.*?\S)?)\*\*
      | (?<![\w\\])__(?P<strong_underscore>\S(?:.*?\S)?)__(?!\w)
      | ~~(?P<struck>\S(?:.*?\S)?)~~
      | \*(?P<emphasis>[^\s*](?:.*?[^\s*])?)\*
      | (?<![\w\\])_(?P<emphasis_underscore>[^\s_](?:.*?[^\s_])?)_(?!\w)
    )
    """,
    re.VERBOSE,
)

#: The groups :data:`INLINE` can match, each with whether what it captured is
#: prose in its own right. A code span's content is not — the markers inside it
#: are literal, which is the point of the span — and it is kept anyway, because
#: an identifier standing where the reader sees one costs less than the
#: punctuation a deletion leaves touching. docs/extraction.md has both prices.
INLINE_GROUPS = (
    ("escaped", False),
    ("code", False),
    ("alt", True),
    ("link", True),
    ("autolink", False),
    ("strong", True),
    ("strong_underscore", True),
    ("struck", True),
    ("emphasis", True),
    ("emphasis_underscore", True),
)


def prose(text: str) -> str:
    """Return the prose of a Markdown document, one paragraph per line.

    Blank lines separate paragraphs, so that a sentence does not run from one
    paragraph into the next, and nothing else in the result is a line break.
    """
    stripped = COMMENT.sub("", FRONTMATTER.sub("", text))
    lines = _without_trailing_links(stripped.splitlines())
    paragraphs = (_inline(" ".join(block)).strip() for block in _blocks(lines))
    #  A block can come out empty — an image with no description is a paragraph
    #  of nothing — and an empty line between two others would read as a break.
    body = "\n\n".join(paragraph for paragraph in paragraphs if paragraph)
    return body + "\n" if body else ""


def jednostki(text: str) -> list[Jednostka]:
    """Cały dokument, bo dokument jest napisany w jednym języku.

    Ekstrakcja z modułu tnie plik na docstringi i komentarze, każdy z osobna,
    a dokument tnie się na sekcje, których ten krok nie zna: sekcja jest
    nagłówkiem plus prozą pod nim, a tu nagłówki już poszły. TODO.md trzyma to
    jako wpis, bo płaci za to dokument pisany w dwóch językach naraz.
    """
    return [Jednostka(1, prose(text).rstrip("\n"))]


def _without_trailing_links(lines: list[str]) -> list[str]:
    """Drop the list of links that closes a document.

    Such a list is an index rather than prose — every entry is a title, a dash
    and a gloss — and it carries dashes at several times the rate of the text
    above it. Only a list closing the document goes, and only while every item
    of it opens with a link, so an ordinary list that happens to end a document
    stays.
    """
    end = len(lines)
    for index in range(len(lines) - 1, -1, -1):
        if not lines[index].strip():
            continue
        item = BULLET.match(lines[index])
        if item is None or not LINK_ITEM.match(lines[index][item.end() :]):
            break
        end = index
    return lines[:end]


def _blocks(lines: Sequence[str]) -> list[list[str]]:
    """Group the lines that make up each paragraph, apparatus dropped."""
    blocks: list[list[str]] = [[]]
    fence: str | None = None
    quoted = False
    for raw in lines:
        line = _unquoted(raw)
        #  A quotation interrupts the paragraph above it and is interrupted by
        #  the paragraph below, so the two do not join into one line of prose.
        was_quoted, quoted = quoted, line != raw
        if quoted != was_quoted:
            blocks.append([])
        if fence is not None:
            if _closes(fence, line):
                fence = None
        elif opening := FENCE.match(line):
            fence = opening.group(1)
            blocks.append([])
        elif UNDERLINE.match(line):
            blocks[-1].clear()
        elif not line.strip() or _apparatus(line):
            blocks.append([])
        elif item := BULLET.match(line):
            blocks.append([line[item.end() :].strip()])
        else:
            blocks[-1].append(line.strip())
    return [block for block in blocks if block]


def _apparatus(line: str) -> bool:
    """Whether a line is a whole line of apparatus, which ends the paragraph above it."""
    return any(pattern.match(line) for pattern in (HEADING, TABLE_ROW, LINK_DEFINITION))


def _unquoted(line: str) -> str:
    while marker := BLOCKQUOTE.match(line):
        line = line[marker.end() :]
    return line


def _closes(fence: str, line: str) -> bool:
    closing = FENCE.match(line)
    return (
        closing is not None
        and closing.group(1)[0] == fence[0]
        and len(closing.group(1)) >= len(fence)
        and not line[closing.end() :].strip()
    )


def _inline(text: str) -> str:
    return INLINE.sub(_replace, text)


def _replace(match: re.Match) -> str:
    """Put back what a construct wrapped, and nothing else.

    What a construct wraps is prose in its own right, so it goes through the
    same pass again: emphasis around a link leaves the link's text behind rather
    than its brackets. The recursion terminates because every construct here
    spends at least two characters on its own markers.

    A construct with nothing inside it — an image with no description — takes
    the whitespace in front of it along. That is the failure this module was
    written against: a deletion that leaves the space behind reports it as a
    defect somebody typed.
    """
    for name, nested in INLINE_GROUPS:
        inner = match.group(name)
        if inner is None:
            continue
        inner = _inline(inner) if nested else inner
        return (match.group("space") + inner) if inner else ""
    raise AssertionError(f"INLINE matched {match.group()!r} with no group")


# --------------------------------------------------------------------------- #
# The command line
# --------------------------------------------------------------------------- #

USAGE = """
  python3 -m harness.markdown notes/ --into prose/    a tree of notes
  python3 -m harness.markdown note.md --into prose/   one file
"""


CZYTNIK = Czytnik(
    komenda="harness.markdown",
    sufiks=MARKDOWN_SUFFIX,
    nazwa_jednostki="document",
    opis="Extract Polish prose from Markdown, for olski to measure.",
    użycie=USAGE,
    jednostki=jednostki,
)


def main(argv: Sequence[str] | None = None) -> int:
    return uruchom(argv, CZYTNIK)


if __name__ == "__main__":
    raise SystemExit(main())
