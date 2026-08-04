"""Check kinds: the machinery a rule points at.

Adding a rule means editing a pack file. Adding a *kind* of rule means adding a
check here, and that is meant to be the rarer event. Each check validates its
own parameters, declares the fields its findings report, and yields either a
:class:`Hit` or an :class:`Abstain`.

Abstention is a first-class outcome, not a silent no-match. A check that cannot
tell a defect from a legitimate choice — or that is looking at input its rule
was not written for — says so and declines to fire.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field

from olski.document import Document, Span


@dataclass(frozen=True)
class Hit:
    """One thing a check found, before it becomes a finding with a message."""

    span: Span
    fields: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Abstain:
    """A rule declining to answer, with the reason recorded."""

    reason: str


Outcome = Hit | Abstain


@dataclass(frozen=True)
class Check:
    name: str
    #: Field names a finding of this check can report, and therefore the
    #: placeholders a rule's message may use.
    fields: frozenset[str]
    validate: Callable[[dict, str], dict]
    run: Callable[[object, Document], Iterator[Outcome]]


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


def _unit(params: dict, where: str) -> str:
    unit = params.get("unit", "document")
    if unit not in ("document", "paragraph"):
        raise ParamError(f"{where}: 'unit' must be 'document' or 'paragraph'")
    return unit


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
def pattern_density(rule, document: Document) -> Iterator[Outcome]:
    """Flag a unit where a pattern occurs more often than a rate allows.

    ``min_count`` and ``min_words`` exist because a rate computed over a short
    unit is noise: one em dash in a nine-word paragraph is 111 per thousand
    words and means nothing. Below either floor the rule abstains rather than
    reporting a number it does not believe.
    """
    params = rule.params
    for unit in _units(document, params["unit"]):
        matches = list(params["pattern"].finditer(document.slice(unit)))
        if len(matches) < params["min_count"]:
            continue
        words = document.word_count(unit)
        if words < params["min_words"]:
            yield Abstain(
                f"{words} words in this {params['unit']} is too short to measure a rate over"
            )
            continue
        rate = 1000 * len(matches) / words if words else 0.0
        if rate <= params["max_per_1000_words"]:
            continue
        first = Span(unit.start + matches[0].start(), unit.start + matches[0].end())
        yield Hit(
            first,
            {
                "count": len(matches),
                "words": words,
                "rate": f"{rate:.1f}",
                "limit": f"{params['max_per_1000_words']:g}",
                "match": document.excerpt(first),
            },
        )


def _units(document: Document, unit: str):
    if unit == "document":
        return [Span(0, len(document.text))]
    return list(document.paragraphs)


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
