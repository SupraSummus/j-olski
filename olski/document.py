"""The object every rule sees.

Input is plain Polish text: every character is prose, and every newline is a
real one. Markup-aware sources (Markdown first) will arrive later and will have
to answer two extra questions this module answers trivially — which characters
are prose, and whether a newline in the file is a newline on the page.
"""

from __future__ import annotations

import re
from bisect import bisect_right
from dataclasses import dataclass, field

#: A word, for the purposes of counting them. Requires a letter at each end, so
#: that numbers, bullets and stray punctuation do not inflate a density.
WORD = re.compile(r"[^\W\d_](?:[\w’'-]*[^\W\d_])?", re.UNICODE)

PARAGRAPH_BREAK = re.compile(r"\n[ \t]*\n")


@dataclass(frozen=True)
class Span:
    start: int
    end: int

    def __contains__(self, offset: int) -> bool:
        return self.start <= offset < self.end

    def __len__(self) -> int:
        return self.end - self.start


@dataclass(frozen=True)
class Document:
    path: str
    text: str
    #: Blank-line separated paragraphs, the unit a density can be measured over.
    paragraphs: tuple[Span, ...] = ()
    #: ``hard`` if a newline in the source is a newline in the rendered output.
    #: Plain text is always hard; a rule about line ends is only meaningful when
    #: nothing downstream reflows the text.
    line_breaks: str = "hard"
    _line_starts: tuple[int, ...] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        starts = [0]
        starts.extend(m.end() for m in re.finditer(r"\n", self.text))
        object.__setattr__(self, "_line_starts", tuple(starts))

    def position(self, offset: int) -> tuple[int, int]:
        """Return the 1-based line and column of a character offset."""
        line = bisect_right(self._line_starts, offset) - 1
        return line + 1, offset - self._line_starts[line] + 1

    def line_span(self, line: int) -> Span:
        """Return the span of a 1-based line number, excluding its newline."""
        start = self._line_starts[line - 1]
        end = self._line_starts[line] - 1 if line < len(self._line_starts) else len(self.text)
        return Span(start, end)

    @property
    def line_count(self) -> int:
        return len(self._line_starts)

    def lines(self):
        """Yield ``(line_number, span)`` for every line, newline excluded."""
        for number in range(1, self.line_count + 1):
            yield number, self.line_span(number)

    def slice(self, span: Span | None = None) -> str:
        return self.text if span is None else self.text[span.start : span.end]

    def excerpt(self, span: Span, limit: int = 60) -> str:
        """Return the text of a span on one line, short enough for a message."""
        raw = " ".join(self.slice(span).split())
        return raw if len(raw) <= limit else raw[: limit - 1] + "…"

    def word_count(self, span: Span | None = None) -> int:
        return sum(1 for _ in WORD.finditer(self.slice(span)))


def from_text(text: str, path: str = "<text>") -> Document:
    return Document(path=path, text=text, paragraphs=tuple(_paragraphs(text)))


def _paragraphs(text: str):
    position = 0
    for separator in PARAGRAPH_BREAK.finditer(text):
        span = _trimmed(text, position, separator.start())
        if span:
            yield span
        position = separator.end()
    span = _trimmed(text, position, len(text))
    if span:
        yield span


def _trimmed(text: str, start: int, end: int) -> Span | None:
    chunk = text[start:end]
    stripped = chunk.strip()
    if not stripped:
        return None
    offset = start + len(chunk) - len(chunk.lstrip())
    return Span(offset, offset + len(stripped))
