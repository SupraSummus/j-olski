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

#: Sentence-final punctuation, taking the closing marks that ride along with it,
#: and requiring whitespace after. That requirement is what keeps a bare domain
#: name whole: the stop in ``zabytek.pl`` has a letter after it and never looks
#: like a boundary.
SENTENCE_END = re.compile(r"[.!?…]+[”»\"')\]]*(?=\s|\Z)", re.UNICODE)

#: Abbreviations whose full stop is not the end of a sentence. An entry earns its
#: place by ordinarily continuing the sentence it stands in, which is why ``itd.``
#: and ``itp.`` are absent: those ordinarily close one, and listing them would
#: merge two sentences wherever they occur. Some entries take a dot only in
#: careless Polish, which writes ``dr``, ``mgr``, ``mln`` and ``pkt`` without one;
#: they are listed because a stop nobody should have typed still splits a
#: sentence, and this linter is pointed at text somebody is about to correct.
#:
#: The reverse error is the accepted one: an abbreviation here can also end a
#: sentence — ``Ustawa weszła w życie w 2011 r.`` is ordinary Polish — and then
#: the sentence runs on into the next. A splitter has to choose which way to be
#: wrong, and a missed boundary understates a count where a false one invents a
#: sentence nobody wrote.
ABBREVIATIONS = frozenset(
    {
        "al.", "ang.", "art.", "cf.", "cz.", "dot.", "dr.", "ds.", "dz.", "gen.",
        "gm.", "godz.", "hab.", "im.", "in.", "inż.", "łac.", "m.in.", "mgr.",
        "min.", "mld.", "mln.", "np.", "ok.", "os.", "par.", "pkt.", "pl.", "płk.",
        "por.", "poz.", "proc.", "prof.", "pt.", "r.", "red.", "rozdz.", "rys.",
        "sek.", "str.", "św.", "sygn.", "tab.", "tj.", "tys.", "tzn.", "tzw.", "ul.",
        "ur.", "ust.", "wg.", "woj.", "ww.", "wyd.", "zał.", "zm.", "zob.",
    }
)  # fmt: skip

#: The word or number immediately before a full stop, dots included so that a
#: multi-part abbreviation arrives whole.
TOKEN_BEFORE = re.compile(r"[\w.]*\Z", re.UNICODE)

#: How far back to look for that token. The pattern is anchored to its end, so
#: matching it against the whole text before a full stop makes the splitter
#: quadratic in the length of a document: the engine restarts the search at the
#: beginning once per sentence. A window longer than any abbreviation on the list
#: gives the same answer in constant time.
TOKEN_REACH = 12

#: The first letter of the next word, which is what tells an ordinal from a
#: numeral that ends a sentence.
NEXT_WORD = re.compile(r"\s*(\w)", re.UNICODE)


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
    #: Sentences, which do not cross a paragraph boundary. The narrowest unit a
    #: rate or a spread can be measured over.
    sentences: tuple[Span, ...] = ()
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
    paragraphs = tuple(_paragraphs(text))
    return Document(
        path=path,
        text=text,
        paragraphs=paragraphs,
        sentences=tuple(_sentences(text, paragraphs)),
    )


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


def _sentences(text: str, paragraphs):
    """Split each paragraph at sentence-final punctuation.

    A paragraph boundary ends a sentence whether or not anything punctuates it,
    which is what gives a heading or a list item a span of its own rather than
    letting it run into the prose below.
    """
    for paragraph in paragraphs:
        start = paragraph.start
        for match in SENTENCE_END.finditer(text, paragraph.start, paragraph.end):
            if _mid_sentence(text, match):
                continue
            span = _trimmed(text, start, match.end())
            if span:
                yield span
            start = match.end()
        span = _trimmed(text, start, paragraph.end)
        if span:
            yield span


def _mid_sentence(text: str, match: re.Match) -> bool:
    """Whether a full stop stands inside a sentence rather than closing one.

    Three things put it there, and two of them are plain properties of the token
    before it: a listed abbreviation and an initial.

    A numeral is the third and needs the word after it as well, because a full
    stop after digits is an ordinal or a list marker in ``12. dzień`` and the end
    of a sentence in ``poz. 1446.`` — and technical documentation is full of both.
    The following word separates them: an ordinal is followed by the noun it
    counts, in lower case.
    """
    if match.group() != ".":
        return False
    reach = max(0, match.start() - TOKEN_REACH)
    token = TOKEN_BEFORE.search(text, reach, match.start()).group()
    if not token:
        return False
    if token.isdigit():
        following = NEXT_WORD.match(text, match.end())
        return following is not None and following.group(1).islower()
    return (len(token) == 1 and token.isalpha()) or f"{token.lower()}." in ABBREVIATIONS


def _trimmed(text: str, start: int, end: int) -> Span | None:
    chunk = text[start:end]
    stripped = chunk.strip()
    if not stripped:
        return None
    offset = start + len(chunk) - len(chunk.lstrip())
    return Span(offset, offset + len(stripped))
