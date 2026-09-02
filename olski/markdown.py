"""Markdown in, Polish prose out.

The grammar needs a guarantee plain text gives and Markdown does not: every
character is prose. This produces it, by dropping the apparatus and by joining
what the renderer would have joined.

Moduł należy do ``olski``, bo dokument czyta ``olski-check``, a nie krok przed
nim; czemu granica pakietów pada tutaj, mówi ``harness/__init__.py``.

The decisions below run through the whole module.

**A parser says where a construct is; this module says what to do with it.**
Which characters are markup is a question about CommonMark, and markdown-it-py
answers it, so that what no pattern settles — which of two adjacent emphases a
marker closes, whether a run of backticks opens a fence or a code span — is
settled by something tested against the specification. What stays here is the
half a renderer has no opinion on: which constructs are apparatus, and what a
construct leaves behind when it goes.

**Inline markup is replaced by the text it wrapped, never deleted.** A deletion
leaves the space that stood in front of it, and the sentence then reaches the
grammar with a gap nobody typed: docs/extraction.md holds what that cost the two
extractions written before this one. Where a construct has no text to leave
behind, the space in front of it goes with it.

**A line is a line of source, not a line of the page.** Everything a paragraph
holds is joined with single spaces, because that is what a renderer does with a
newline inside one, and where the author's editor wrapped then leaves no trace
in what comes out.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Iterator

from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

MARKDOWN_SUFFIX = ".md"

#: CommonMark, plus the two GitHub constructs the corpora are written with. A
#: table is apparatus and goes whole, so what enabling it buys is the row that
#: opens without a pipe; strikethrough wraps prose the way emphasis does, and
#: without it a struck sentence reaches the grammar with its tildes still in.
PARSER = MarkdownIt("commonmark").enable(["table", "strikethrough"])

#: YAML frontmatter: a fence of three dashes opening the file, and everything
#: down to the line that closes it. It is matched rather than parsed because it
#: is not Markdown: to a parser those dashes are a heading's underline.
FRONTMATTER = re.compile(r"\A---[ \t]*\n.*?\n(?:---|\.\.\.)[ \t]*(?:\n|\Z)", re.DOTALL)

#: Węzły, które trzymają akapity, a same akapitem nie są. Prozą jest to, co w
#: środku: znak listy i znak cytowania są aparatem wokół niej, a każda pozycja
#: listy jest osobnym akapitem, bo zdanie nie biegnie z jednej do następnej.
CONTAINERS = frozenset({"blockquote", "bullet_list", "ordered_list", "list_item"})

LISTS = frozenset({"bullet_list", "ordered_list"})

#: Węzły w linii, których treść jest tekstem tak, jak stoi. Treść wstawki
#: kodowej prozą nie jest — znaczniki w jej środku są znakami i po to ta wstawka
#: jest — a zostaje mimo to, bo identyfikator stojący tam, gdzie czytelnik go
#: widzi, kosztuje mniej niż punktacja, którą kasowanie zostawia stykiem.
#: docs/extraction.md ma obie ceny.
LITERAL = frozenset({"text", "text_special", "code_inline"})

#: Węzły, które prozę owijają, więc zostaje po nich to, co owinęły.
WRAPPING = frozenset({"link", "image", "em", "strong", "s"})

#: Złamanie wiersza w źródle, które renderuje się jako odstęp.
BREAKS = frozenset({"softbreak", "hardbreak"})


def prose(text: str) -> str:
    """Return the prose of a Markdown document, one paragraph per line.

    Blank lines separate paragraphs, so that a sentence does not run from one
    paragraph into the next, and nothing else in the result is a line break.
    """
    root = SyntaxTreeNode(PARSER.parse(FRONTMATTER.sub("", text)))
    paragraphs = (paragraph.strip() for paragraph in _paragraphs(_without_trailing_links(root)))
    #  A block can come out empty — an image with no description is a paragraph
    #  of nothing — and an empty line between two others would read as a break.
    body = "\n\n".join(paragraph for paragraph in paragraphs if paragraph)
    return body + "\n" if body else ""


def _paragraphs(nodes: Iterable[SyntaxTreeNode]) -> Iterator[str]:
    """Zejdź po drzewie i wydaj prozę każdego akapitu, jeden ciąg na akapit.

    Akapit jest jedynym węzłem, który prozę niesie, a poza nim i pojemnikami
    wszystko jest aparatem: nagłówek, tabela, blok kodu — z wcięcia tak samo jak
    spod płotka — blok surowego HTML-a i linia oddzielająca odpadają razem z
    tym, co w środku. Tekst, który przy tym pada, jest tekstem, którego
    gramatyka i tak by nie wyprowadziła: nagłówek i komórka tabeli nie są
    zdaniem, a ``<summary>`` stoi w bloku, który renderer bierze w całości jako
    HTML.
    """
    for node in nodes:
        if node.type == "paragraph":
            yield _inline(node.children[0].children)
        elif node.type in CONTAINERS:
            yield from _paragraphs(node.children)


def _inline(nodes: Iterable[SyntaxTreeNode]) -> str:
    """Złóż prozę akapitu z tego, co zostawiają po sobie jego konstrukcje.

    Konstrukcja, po której nic nie zostaje — obrazek bez opisu, komentarz HTML,
    surowy tag — zabiera ze sobą odstęp, który przed nią stał. To jest ta
    usterka, przeciw której moduł powstał: kasowanie, które odstęp zostawia,
    dochodzi do gramatyki jako znak, który ktoś wpisał.

    Tekst idzie osobną gałęzią właśnie dlatego, a nie dla porządku. Parser
    stawia węzeł tekstu pustej długości tam, gdzie sam nic nie zjadł — za twardym
    złamaniem wiersza stoi taki węzeł — więc wpuszczony do gałęzi konstrukcji
    zabrałby odstęp, który złamanie wnosi, i skleiłby dwa zdania w jedno.

    To, co owija prozę, przechodzi tędy jeszcze raz, więc emfaza wokół odnośnika
    zostawia tekst odnośnika, a nie jego nawiasy.
    """
    text = ""
    for node in nodes:
        if node.type in LITERAL:
            text += node.content
        elif node.type in BREAKS:
            text += " "
        else:
            wnętrze = _inline(node.children) if node.type in WRAPPING else ""
            text = text + wnętrze if wnętrze else text.rstrip(" \t")
    return text


def _without_trailing_links(root: SyntaxTreeNode) -> list[SyntaxTreeNode]:
    """Drop the list of links that closes a document.

    Such a list is an index rather than prose — every entry is a title, a dash
    and a gloss — and it carries dashes at several times the rate of the text
    above it. Only a list closing the document goes, and only while every item
    of it opens with a link, so an ordinary list that happens to end a document
    stays, and so does an entry standing above an aside in the middle of one.
    """
    blocks = list(root.children)
    while blocks and blocks[-1].type in LISTS:
        items = list(blocks[-1].children)
        while items and _opens_with_link(items[-1]):
            items.pop()
        #  Whatever stayed takes the list's place, which is also what ends the
        #  walk: an item is not a list, so only a list that went whole lets the
        #  outer loop reach the block above it.
        blocks[-1:] = items
    return blocks


def _opens_with_link(item: SyntaxTreeNode) -> bool:
    """Whether a list item is an entry of an index rather than something said."""
    opening = item.children[0] if item.children else None
    if opening is None or opening.type != "paragraph":
        return False
    inline = opening.children[0].children
    return bool(inline) and inline[0].type == "link"
