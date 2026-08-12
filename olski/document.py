"""Gdzie w tekście kończy się jedno zdanie, a zaczyna następne.

Gramatyka bierze zdanie, a wejściem jest plik, więc ktoś musi jedno pociąć na
drugie, zanim analizator zobaczy pierwszy segment. Robi to ten moduł i nic poza
nim, bo cięcie jest rozstrzygnięciem o polszczyźnie — który skrót kończy zdanie,
a który je ciągnie — a nie krokiem czytania pliku.

Cięcie stoi przed analizą, a nie po niej, i dlaczego, mówi ``sentences`` w
olski/subset.py: po analizie nie ma już czym zobaczyć spacji, która odróżnia
granicę zdania od nazwy pliku.
"""

from __future__ import annotations

import re
from dataclasses import KW_ONLY, dataclass
from functools import cached_property

PARAGRAPH_BREAK = re.compile(r"\n[ \t]*\n")

#: Sentence-final punctuation, taking the closing marks that ride along with it.
CLOSING_MARK = r"[.!?…]+[”»\"')\]]*"

#: Where a sentence ends: the punctuation above, with whitespace required after.
#: That requirement is what keeps a bare domain name whole: the stop in
#: ``zabytek.pl`` has a letter after it and never looks like a boundary.
SENTENCE_END = re.compile(CLOSING_MARK + r"(?=\s|\Z)", re.UNICODE)

#: To samo zamknięcie na końcu tekstu, czyli pytanie „czy to jest zdanie”.
#: Podział niżej oddaje też akapit, którego nic nie punktuje, bo inaczej nagłówek
#: wpadłby w prozę pod sobą, a kto pyta o zdanie, pyta tym wyrażeniem. Mierzy ono
#: to, czym zdanie zamyka polszczyzna, a nie to, co bierze gramatyka olskiego,
#: bo akapit zamknięty wielokropkiem jest zdaniem, którego olski nie wyprowadza.
SENTENCE_CLOSE = re.compile(CLOSING_MARK + r"\s*\Z", re.UNICODE)

#: Abbreviations whose full stop is not the end of a sentence. An entry earns its
#: place by ordinarily continuing the sentence it stands in, which is why ``itd.``
#: and ``itp.`` are absent: those ordinarily close one, and listing them would
#: merge two sentences wherever they occur. Some entries take a dot only in
#: careless Polish, which writes ``dr``, ``mgr``, ``mln`` and ``pkt`` without one;
#: they are listed because a stop nobody should have typed still splits a
#: sentence, and the text this reads is documentation rather than a fair copy.
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


@dataclass(frozen=True)
class Document:
    """Tekst i podział, który się z niego wylicza.

    Podział jest leniwy i pamiętany, bo pyta o niego dopiero ten, kto zdania
    liczy albo im się przygląda, a wylicza się przy pierwszym pytaniu, więc nie
    ma dokumentu półgotowego: dwa o tym samym tekście odpowiadają tak samo,
    obojętne, które miejsce w programie je zbudowało.
    """

    text: str
    #: Reszta po nazwie, bo tekst i ścieżka są oba napisami: zamienione miejscami
    #: dają dokument, który tnie na zdania własną nazwę, i nic tego nie zgłasza.
    _: KW_ONLY
    path: str = "<text>"

    @cached_property
    def paragraphs(self) -> tuple[Span, ...]:
        """Akapity rozdzielone pustym wierszem, wewnątrz których stoją zdania."""
        return tuple(_paragraphs(self.text))

    @cached_property
    def sentences(self) -> tuple[Span, ...]:
        """Zdania, których żadne nie przechodzi przez granicę akapitu."""
        return tuple(_sentences(self.text, self.paragraphs))

    def slice(self, span: Span | None = None) -> str:
        return self.text if span is None else self.text[span.start : span.end]


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
