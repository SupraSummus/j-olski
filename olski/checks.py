"""Check kinds: the machinery a rule points at.

Adding a rule means editing a pack file. Adding a *kind* of rule means adding a
check here, and that is meant to be the rarer event. Each check validates its
own parameters, declares the fields its findings report, and yields either a
:class:`Hit` or an :class:`Abstain`.

Abstention is a first-class outcome, not a silent no-match. A check that cannot
tell a defect from a legitimate choice — or that is looking at input its rule
was not written for — says so and declines to fire.

Every check sees the whole corpus, because some defects exist only across files
and no per-document view can reach them. A single file is a corpus of one, so
there is one protocol rather than two, and a check whose question is about one
document says so with :func:`per_document` rather than walking the corpus itself.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field, replace
from functools import wraps

from olski.document import Document, Span


@dataclass(frozen=True)
class Hit:
    """One thing a check found, before it becomes a finding with a message.

    ``document`` is the file the span is in. :func:`per_document` sets it for
    checks that see one document at a time, and a corpus check must set it to
    the example it anchored its measurement at, because the engine has nothing
    else to turn the hit into a location with.
    """

    span: Span
    fields: dict = field(default_factory=dict)
    document: Document | None = None


@dataclass(frozen=True)
class Abstain:
    """A rule declining to answer, with the reason recorded.

    ``document`` is the file the refusal belongs to, and ``None`` when the rule
    was measuring the corpus and no single file owns the answer.
    """

    reason: str
    document: Document | None = None


Outcome = Hit | Abstain


@dataclass(frozen=True)
class Check:
    name: str
    #: Field names a finding of this check can report, and therefore the
    #: placeholders a rule's message may use.
    fields: frozenset[str]
    validate: Callable[[dict, str], dict]
    run: Callable[[object, Sequence[Document]], Iterator[Outcome]]


CHECKS: dict[str, Check] = {}


def get_check(name: str, where: str) -> Check:
    try:
        return CHECKS[name]
    except KeyError:
        raise ParamError(
            f"{where}: unknown check {name!r}; known checks are {', '.join(sorted(CHECKS))}"
        ) from None


class ParamError(Exception):
    """A rule's parameters do not fit the check it names."""


def _register(name: str, fields: set[str], validate) -> Callable:
    def decorate(run):
        CHECKS[name] = Check(name=name, fields=frozenset(fields), validate=validate, run=run)
        return run

    return decorate


def per_document(run) -> Callable:
    """Adapt a check written against one document into one that sees a corpus.

    The walk that runs a per-document check over every file is the same walk
    every time, so it lives here once and a check whose question is about a
    single document is written as if the corpus did not exist.
    """

    @wraps(run)
    def over_corpus(rule, documents: Sequence[Document]) -> Iterator[Outcome]:
        for document in documents:
            for outcome in run(rule, document):
                yield replace(outcome, document=document)

    return over_corpus


# --------------------------------------------------------------------------- #
# Parameter helpers. Every one of these reports the rule it is complaining
# about, because a validation error with no rule id in it is useless.
# --------------------------------------------------------------------------- #


def _known(params: dict, allowed: set[str], where: str) -> None:
    unknown = set(params) - allowed
    if unknown:
        raise ParamError(f"{where}: unknown parameters: {', '.join(sorted(unknown))}")


def _pattern(params: dict, where: str, key: str = "pattern") -> re.Pattern:
    raw = params.get(key)
    if not isinstance(raw, str) or not raw:
        raise ParamError(f"{where}: '{key}' must be a non-empty regular expression")
    flags = re.UNICODE
    for name in params.get("flags", ()) or ():
        if name not in ("ignorecase", "multiline", "dotall", "verbose"):
            raise ParamError(f"{where}: unknown regex flag {name!r}")
        flags |= getattr(re, name.upper())
    try:
        return re.compile(raw, flags)
    except re.error as error:
        raise ParamError(f"{where}: '{key}' is not a valid regular expression: {error}") from error


def _number(params: dict, key: str, where: str, default=None) -> float:
    value = params.get(key, default)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        raise ParamError(f"{where}: '{key}' must be a non-negative number")
    return float(value)


#: The stretches of text a rate can be measured over, widest last.
UNITS = ("paragraph", "document", "corpus")


def _unit(params: dict, where: str) -> str:
    unit = params.get("unit", "document")
    if unit not in UNITS:
        raise ParamError(f"{where}: 'unit' must be one of {', '.join(UNITS)}")
    return unit


def _share(params: dict, key: str, where: str, default=None) -> float:
    value = _number(params, key, where, default)
    if value > 1:
        raise ParamError(f"{where}: '{key}' is a share of the whole, so it cannot exceed 1")
    return value


# --------------------------------------------------------------------------- #
# pattern: one finding per match.
# --------------------------------------------------------------------------- #

PATTERN_PARAMS = {"pattern", "flags", "unless_preceded_by", "unless_followed_by"}


def _validate_pattern(params: dict, where: str) -> dict:
    _known(params, PATTERN_PARAMS, where)
    validated = {"pattern": _pattern(params, where)}
    if "unless_preceded_by" in params:
        # Anchored to end, so that it has to match up against the match itself
        # rather than anywhere earlier in the text.
        validated["unless_preceded_by"] = _pattern(
            {**params, "unless_preceded_by": params["unless_preceded_by"] + r"\Z"},
            where,
            key="unless_preceded_by",
        )
    if "unless_followed_by" in params:
        validated["unless_followed_by"] = _pattern(params, where, key="unless_followed_by")
    return validated


@_register("pattern", {"match"}, _validate_pattern)
@per_document
def pattern(rule, document: Document) -> Iterator[Outcome]:
    """Flag every match of a regular expression.

    The two ``unless`` parameters are where precision is bought back. Either one
    naming the context around a match means the match is a legitimate use, and
    the rule stays quiet. Each exemption is a deliberate false omission: the
    alternative is a rule that accuses correct Polish, which costs the reader's
    trust in every other rule.
    """
    before = rule.params.get("unless_preceded_by")
    after = rule.params.get("unless_followed_by")
    for match in rule.params["pattern"].finditer(document.text):
        if before is not None and before.search(document.text, 0, match.start()):
            continue
        if after is not None and after.match(document.text, match.end()):
            continue
        span = Span(*match.span())
        yield Hit(span, {"match": document.excerpt(span)})


# --------------------------------------------------------------------------- #
# pattern-density: how often something happens per thousand words.
# --------------------------------------------------------------------------- #

DENSITY_PARAMS = {"pattern", "flags", "unit", "max_per_1000_words", "min_count", "min_words"}


def _validate_density(params: dict, where: str) -> dict:
    _known(params, DENSITY_PARAMS, where)
    return {
        "pattern": _pattern(params, where),
        "unit": _unit(params, where),
        "max_per_1000_words": _number(params, "max_per_1000_words", where),
        "min_count": int(_number(params, "min_count", where, default=1)),
        "min_words": int(_number(params, "min_words", where, default=0)),
    }


@_register(
    "pattern-density",
    {"count", "words", "rate", "limit", "match"},
    _validate_density,
)
def pattern_density(rule, documents: Sequence[Document]) -> Iterator[Outcome]:
    """Flag a scope where a pattern occurs more often than a rate allows.

    ``min_count`` and ``min_words`` exist because a rate computed over a short
    scope is noise: one em dash in a nine-word paragraph is 111 per thousand
    words and means nothing. Below either floor the rule abstains rather than
    reporting a number it does not believe.

    At ``unit="corpus"`` the rate is one number for the whole body of text,
    anchored at the first match rather than raised against every one of them.
    See docs/rules.md for why that is the point rather than a shortcut.
    """
    params = rule.params
    for owner, pieces in _scopes(documents, params["unit"]):
        found = [
            (document, Span(piece.start + match.start(), piece.start + match.end()))
            for document, piece in pieces
            for match in params["pattern"].finditer(document.slice(piece))
        ]
        if len(found) < params["min_count"]:
            continue
        words = sum(document.word_count(piece) for document, piece in pieces)
        if words < params["min_words"]:
            yield Abstain(
                f"{words} words in this {params['unit']} is too short to measure a rate over",
                document=owner,
            )
            continue
        rate = 1000 * len(found) / words if words else 0.0
        if rate <= params["max_per_1000_words"]:
            continue
        document, first = found[0]
        yield Hit(
            first,
            {
                "count": len(found),
                "words": words,
                "rate": f"{rate:.1f}",
                "limit": f"{params['max_per_1000_words']:g}",
                "match": document.excerpt(first),
            },
            document=document,
        )


_Scope = tuple[Document | None, tuple[tuple[Document, Span], ...]]


def _scopes(documents: Sequence[Document], unit: str) -> Iterator[_Scope]:
    """Yield the stretches of text a rate gets measured over.

    Each is the file an abstention would belong to — ``None`` for a corpus,
    where no single file owns the answer — and the pieces the stretch is made
    of. A paragraph and a document are one piece; a corpus is every document at
    once, which is why a scope is a list of pieces rather than one span.
    """
    if unit == "corpus":
        yield None, tuple((d, Span(0, len(d.text))) for d in documents)
        return
    for document in documents:
        whole = (Span(0, len(document.text)),)
        for piece in whole if unit == "document" else document.paragraphs:
            yield document, ((document, piece),)


# --------------------------------------------------------------------------- #
# line-end-word: Polish typography, and the abstention that goes with it.
# --------------------------------------------------------------------------- #

LINE_END_PARAMS = {"words", "case_sensitive"}


def _validate_line_end(params: dict, where: str) -> dict:
    _known(params, LINE_END_PARAMS, where)
    words = params.get("words")
    if not isinstance(words, list) or not words or not all(isinstance(w, str) and w for w in words):
        raise ParamError(f"{where}: 'words' must be a non-empty list of words")
    case_sensitive = params.get("case_sensitive", False)
    if not isinstance(case_sensitive, bool):
        raise ParamError(f"{where}: 'case_sensitive' must be true or false")
    return {"words": tuple(words), "case_sensitive": case_sensitive}


@_register("line-end-word", {"word"}, _validate_line_end)
@per_document
def line_end_word(rule, document: Document) -> Iterator[Outcome]:
    """Flag listed words left at the end of a line.

    Polish typography does not leave a one-letter conjunction or preposition
    hanging at a line end. Whether that has happened depends on where lines
    actually break in the output, so the rule only applies to text whose line
    breaks survive rendering. Where they do not, it abstains: a soft-wrapped
    source says nothing about the rendered line, and guessing would flag
    correct text.
    """
    if document.line_breaks != "hard":
        yield Abstain(
            "line breaks in this document are soft, so a word at the end of a "
            "source line is not a word at the end of a rendered line"
        )
        return

    words = rule.params["words"]
    lookup = words if rule.params["case_sensitive"] else tuple(w.lower() for w in words)
    for number, span in document.lines():
        if number == document.line_count and not document.slice(span).strip():
            continue
        last = _last_word(document.slice(span))
        if last is None:
            continue
        candidate = last.group() if rule.params["case_sensitive"] else last.group().lower()
        if candidate in lookup:
            hit = Span(span.start + last.start(), span.start + last.end())
            yield Hit(hit, {"word": document.slice(hit)})


def _last_word(line: str) -> re.Match | None:
    """Return the final word of a line, looking past trailing punctuation."""
    stripped = line.rstrip()
    matches = list(re.finditer(r"[^\W\d_]+", stripped, re.UNICODE))
    if not matches:
        return None
    last = matches[-1]
    return last if re.fullmatch(r"\W*", stripped[last.end() :]) else None


# --------------------------------------------------------------------------- #
# entity-recurrence: what a text introduces with apparatus and then drops.
# --------------------------------------------------------------------------- #

RECURRENCE_PARAMS = {
    "introduce",
    "flags",
    "min_mentions",
    "min_introductions",
    "max_walk_on_share",
}


def _validate_recurrence(params: dict, where: str) -> dict:
    _known(params, RECURRENCE_PARAMS, where)
    introduce = _pattern(params, where, key="introduce")
    if introduce.groups != 1:
        raise ParamError(
            f"{where}: 'introduce' captures the entity's name, so it needs exactly one "
            f"group, and this one has {introduce.groups}"
        )
    return {
        "introduce": introduce,
        "min_mentions": int(_number(params, "min_mentions", where, default=3)),
        "min_introductions": int(_number(params, "min_introductions", where, default=1)),
        "max_walk_on_share": _share(params, "max_walk_on_share", where),
    }


@_register(
    "entity-recurrence",
    {"entity", "mentions", "walk_ons", "introductions", "share", "limit"},
    _validate_recurrence,
)
def entity_recurrence(rule, documents: Sequence[Document]) -> Iterator[Outcome]:
    """Report the share of what a corpus introduces that it then never uses.

    ``introduce`` matches where a text sets an entity up with apparatus — a name
    with a parenthesis after it, a term with its expansion — and captures the
    name. An entity named fewer than ``min_mentions`` times in the file that
    introduced it is a walk-on, the introduction counted among the mentions.

    The finding is the share across the corpus, anchored at one example, because
    a single walk-on is a legitimate choice and only a rate tells a choice from
    a habit. See docs/rules.md, and docs/generated-polish.md for the measurement
    this was written against.
    """
    params = rule.params
    introductions: dict[tuple[str, str], tuple[Document, Span]] = {}
    for document in documents:
        for match in params["introduce"].finditer(document.text):
            introductions.setdefault(
                (document.path, match.group(1)), (document, Span(*match.span(1)))
            )

    if len(introductions) < params["min_introductions"]:
        yield Abstain(
            f"{len(introductions)} introductions in this corpus "
            "is too few to measure a share over"
        )
        return

    walk_ons = [
        (document, span, name, mentions)
        for (_, name), (document, span) in introductions.items()
        if (mentions := _mentions(document, name)) < params["min_mentions"]
    ]
    #  An empty list is a share of zero, so it comes in under any threshold and
    #  needs no case of its own.
    share = len(walk_ons) / len(introductions)
    if share <= params["max_walk_on_share"]:
        return

    document, span, name, mentions = walk_ons[0]
    yield Hit(
        span,
        {
            "entity": name,
            "mentions": mentions,
            "walk_ons": len(walk_ons),
            "introductions": len(introductions),
            "share": f"{share:.0%}",
            "limit": f"{params['max_walk_on_share']:.0%}",
        },
        document=document,
    )


def _mentions(document: Document, name: str) -> int:
    return len(re.findall(rf"\b{re.escape(name)}\b", document.text))
