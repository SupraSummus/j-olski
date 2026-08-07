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

The scope a check needs also decides which input it can answer about at all. A
check that points at one site is answerable on a file of any format, because the
reader can look at the site and judge it. A check that measures the whole of a
document is measuring that document's markup along with its prose, so it says so
with :func:`needs_plain_text`.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass, field, replace
from functools import wraps
from math import sqrt

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


#: The two shapes a calibration takes, named as strings because a check cannot
#: know what a rule is. ``olski.rules`` holds the classes that carry them.
AUDIT = "audit"
DISTRIBUTION = "distribution"


@dataclass(frozen=True)
class Check:
    name: str
    #: Field names a finding of this check can report, given a rule's validated
    #: parameters, and therefore the placeholders that rule's message may use. A
    #: function of the parameters rather than one set per kind, because what a
    #: finding has to report follows from which findings the rule asked for: a
    #: rate rule that set no ceiling has no occurrence to quote.
    fields: Callable[[dict], set[str]]
    #: Which shape of calibration a rule using this check owes: an audit where
    #: the check points at a site and its hits are read one by one, a
    #: distribution where it compares a measurement to a threshold the rule
    #: sets. docs/linter.md owns the argument.
    calibrated_by: str
    #: The unit a rate over this check's findings is a rate of, given a rule's
    #: validated parameters: what the check can fire at most once per. A check
    #: with no such bound, since a pattern matches as often as the prose gives
    #: it cause, is counted against the quantity of prose instead. Every check
    #: says which it is rather than inheriting a default, because a wrong
    #: denominator is a wrong number rather than a missing one.
    counted_over: Callable[[dict], str]
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


#  Keyword-only past the name: two of the four arguments are functions of a
#  rule's parameters, and position alone does not tell them apart.
def _register(
    name: str,
    *,
    fields: Callable[[dict], set[str]],
    validate,
    counted_over: Callable[[dict], str],
    calibrated_by: str,
) -> Callable:
    def decorate(run):
        CHECKS[name] = Check(
            name=name,
            fields=fields,
            calibrated_by=calibrated_by,
            counted_over=counted_over,
            validate=validate,
            run=run,
        )
        return run

    return decorate


#: Why a check that has to look at a whole document declines on one whose format
#: olski does not read. One reason for every such check, because the cause is the
#: same and which guarantee a given rule wanted is in that rule's justification.
#: It is also how a caller picks this abstention out from the others.
NOT_PLAIN_TEXT = (
    "this file is not plain text, and olski reads no other format, so it cannot "
    "vouch for the text as prose laid out as written"
)


def needs_plain_text(run) -> Callable:
    """Decline on documents whose whole text olski cannot vouch for.

    A count is a count of something, and in a markup file the something takes in
    the frontmatter, the headings and the link lists. The error that makes is not
    a bias anyone could discount later — docs/generated-polish.md measures one
    rule reading a quarter high over one body of Markdown and true over another
    by the same writer — so this declines instead.

    The documents that do carry the guarantee are passed through, so a run over
    a mixed directory measures what it can and says what it skipped.
    """

    @wraps(run)
    def over_prose(rule, documents: Sequence[Document]) -> Iterator[Outcome]:
        prose = []
        for document in documents:
            if document.plain_text:
                prose.append(document)
            else:
                yield Abstain(NOT_PLAIN_TEXT, document=document)
        # Nothing left to measure is not the same thing as a corpus too small to
        # measure over, and handing an empty one down says the second: a check
        # with a floor would add its own abstention on top of the ones above.
        if prose:
            yield from run(rule, prose)

    return over_prose


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


#: How to find one document's worth of a unit, narrowest first. A corpus is not
#: here because it is every document at once rather than a span of one, and
#: :func:`_scopes` owns that difference.
UNIT_SPANS = {
    "sentence": lambda document: document.sentences,
    "paragraph": lambda document: document.paragraphs,
    "document": lambda document: (Span(0, len(document.text)),),
}

#: The stretches of text a rate can be measured over, widest last.
UNITS = (*UNIT_SPANS, "corpus")

#: How much of a unit one document holds, which is the denominator a firing
#: rate is taken against. Three of these count what :data:`UNIT_SPANS` yields.
#: ``line`` is here as well because a rule about a line end fires at most once
#: per line, and ``word`` because a check with no such bound is counted against
#: the quantity of prose instead. A corpus is absent for the reason it is
#: absent above, and :func:`count_units` owns that difference.
UNIT_COUNTS = {
    "word": lambda document: document.word_count(),
    #  Not ``line_count``, which counts the position after a trailing newline:
    #  nothing is written there, so no rule can ever fire on it.
    "line": lambda document: len(document.text.splitlines()),
    "sentence": lambda document: len(document.sentences),
    "paragraph": lambda document: len(document.paragraphs),
    "document": lambda document: 1,
}


def count_units(unit: str, documents: Sequence[Document]) -> int:
    """How many of a unit a corpus holds.

    A corpus is one of itself rather than one per document, and none at all when
    there is nothing in it, since a rate needs something to divide by.
    """
    if unit == "corpus":
        return 1 if documents else 0
    return sum(UNIT_COUNTS[unit](document) for document in documents)


def _unit(params: dict, where: str, allowed: tuple[str, ...] = UNITS, default="document") -> str:
    """Validate the scope a check was pointed at, against the scopes it accepts.

    Which units are meaningful is the check's business — a spread cannot be
    measured over a corpus — so the allowed set is a parameter and the checking
    of it happens once.
    """
    unit = params.get("unit", default)
    if unit not in allowed:
        raise ParamError(f"{where}: 'unit' must be one of {', '.join(allowed)}")
    return unit


def _bounds(params: dict, quantity: str, where: str) -> dict:
    """Validate an optional floor and ceiling, of which a rule sets at least one.

    A one-sided threshold can only say a text has too much of something, and
    several of the measurements this project wants have a register where too
    little is the defect: fact density is reported *low* in generated prose, and
    monotony is a spread that is too narrow.
    """
    low, high = f"min_{quantity}", f"max_{quantity}"
    if low not in params and high not in params:
        raise ParamError(f"{where}: needs '{low}', '{high}', or both")
    bounds = {key: _number(params, key, where) for key in (low, high) if key in params}
    if len(bounds) == 2 and bounds[low] > bounds[high]:
        raise ParamError(f"{where}: '{low}' stands above '{high}', so no text can pass both")
    return bounds


def _outside(value: float, params: dict, quantity: str) -> tuple[str, float] | None:
    """Which bound a measurement fell outside, and the value of that bound.

    A finding has to name the side, or its message cannot tell a writer whether
    the text ran hot or cold.
    """
    low = params.get(f"min_{quantity}")
    high = params.get(f"max_{quantity}")
    if low is not None and value < low:
        return "below", low
    if high is not None and value > high:
        return "above", high
    return None


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


@_register(
    "pattern",
    fields=lambda params: {"match"},
    validate=_validate_pattern,
    counted_over=lambda params: "word",
    calibrated_by=AUDIT,
)
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

DENSITY_PARAMS = {
    "pattern",
    "flags",
    "unit",
    "min_per_1000_words",
    "max_per_1000_words",
    "min_count",
    "min_words",
}


def _validate_density(params: dict, where: str) -> dict:
    _known(params, DENSITY_PARAMS, where)
    return {
        "pattern": _pattern(params, where),
        "unit": _unit(params, where),
        "min_count": int(_number(params, "min_count", where, default=1)),
        "min_words": int(_number(params, "min_words", where, default=0)),
        **_bounds(params, "per_1000_words", where),
    }


@_register(
    "pattern-density",
    #  ``match`` only where the rule set a ceiling, since only a reading above one
    #  has an occurrence to quote.
    fields=lambda params: {"count", "words", "rate", "limit", "side"}
    | ({"match"} if "max_per_1000_words" in params else set()),
    validate=_validate_density,
    #  The scope the rate is measured over is the scope one finding covers, so
    #  this is the only check whose denominator its rule chooses.
    counted_over=lambda params: params["unit"],
    calibrated_by=DISTRIBUTION,
)
@needs_plain_text
def pattern_density(rule, documents: Sequence[Document]) -> Iterator[Outcome]:
    """Flag a scope where a pattern occurs more often than a rate allows, or less.

    The two floors guard two different things, and falling under either one is
    the rule declining rather than the rule finding nothing. ``min_words`` is the
    denominator: a rate over a short scope is noise, since one em dash in a
    nine-word paragraph is 111 per thousand words and means nothing, so it is
    tested before the bounds and below it the rule abstains whatever the scope
    turns out to hold. ``min_count`` is the evidence a *hot* reading needs, and it
    does not stand under the floor, where too few matches is the finding rather
    than a reason to doubt one: the scope a rule with a floor most wants is the
    one where the pattern never occurs at all. So it is tested where the side is
    known, and there it abstains too. Both abstain rather than pass the scope
    over, because a refusal is what the engine takes off the denominator a rate is
    reported against; docs/rules.md owns why that is the right place for it.

    At ``unit="corpus"`` the rate is one number for the whole body of text,
    anchored at one place in it rather than raised against every match. See
    docs/rules.md for why that is the point rather than a shortcut.
    """
    params = rule.params
    for owner, pieces in _scopes(documents, params["unit"]):
        words = sum(document.word_count(piece) for document, piece in pieces)
        #  At least one word whatever the rule asked for, since a rate over no
        #  words is not one.
        floor = max(params["min_words"], 1)
        if words < floor:
            #  The floor rather than this scope's own count: a per-scope number
            #  makes a distinct reason per scope, and the report counts causes.
            yield Abstain(
                f"this {params['unit']} is under the {floor}-word floor a rate over it needs",
                document=owner,
            )
            continue
        found = [
            (document, Span(piece.start + match.start(), piece.start + match.end()))
            for document, piece in pieces
            for match in params["pattern"].finditer(document.slice(piece))
        ]
        rate = 1000 * len(found) / words
        outside = _outside(rate, params, "per_1000_words")
        if outside is None:
            continue
        side, limit = outside
        hot = side == "above"
        if hot and len(found) < params["min_count"]:
            yield Abstain(
                f"this {params['unit']} is under the {params['min_count']}-match floor "
                f"a rate above {limit:g} needs",
                document=owner,
            )
            continue
        #  A hot finding points at the first occurrence, so that the number can
        #  be checked against the text. A cold one has no occurrence to point
        #  at — what it found is the text that went by without one — so it
        #  points at the scope, as length-variation points at its document.
        document, span = found[0] if hot else pieces[0]
        yield Hit(
            span,
            {
                "count": len(found),
                "words": words,
                "rate": f"{rate:.1f}",
                "limit": f"{limit:g}",
                "side": side,
                "match": document.excerpt(span) if hot else "",
            },
            document=document,
        )


_Scope = tuple[Document | None, tuple[tuple[Document, Span], ...]]


def _scopes(documents: Sequence[Document], unit: str) -> Iterator[_Scope]:
    """Yield the stretches of text a rate gets measured over.

    Each is the file an abstention would belong to — ``None`` for a corpus,
    where no single file owns the answer — and the pieces the stretch is made
    of. Every unit below a corpus is one piece; a corpus is every document at
    once, which is why a scope is a list of pieces rather than one span.
    """
    if unit == "corpus":
        yield None, tuple((d, Span(0, len(d.text))) for d in documents)
        return
    for document in documents:
        for piece in UNIT_SPANS[unit](document):
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


@_register(
    "line-end-word",
    fields=lambda params: {"word"},
    validate=_validate_line_end,
    counted_over=lambda params: "line",
    calibrated_by=AUDIT,
)
@needs_plain_text
@per_document
def line_end_word(rule, document: Document) -> Iterator[Outcome]:
    """Flag listed words left at the end of a line.

    Polish typography does not leave a one-letter conjunction or preposition
    hanging at a line end. Whether that has happened depends on where lines
    actually break in the output, which is why this is one of the checks that
    needs a plain-text document: a source line of a format that reflows says
    nothing about the rendered line, and guessing would flag correct text.
    """
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
# length-variation: whether a document's units are all the same length.
# --------------------------------------------------------------------------- #

#: What a length can vary across inside one document. A document is not among
#: them: here it is the scope the measurement is taken over rather than a piece
#: of itself, and a corpus mixes documents whose lengths have no reason to agree.
VARIATION_UNITS = ("sentence", "paragraph")

VARIATION_PARAMS = {"unit", "min_variation", "max_variation", "min_units", "min_words"}


def _validate_variation(params: dict, where: str) -> dict:
    _known(params, VARIATION_PARAMS, where)
    return {
        "unit": _unit(params, where, VARIATION_UNITS, default="sentence"),
        "min_units": int(_number(params, "min_units", where, default=2)),
        "min_words": int(_number(params, "min_words", where, default=0)),
        **_bounds(params, "variation", where),
    }


@_register(
    "length-variation",
    fields=lambda params: {"unit", "count", "words", "mean", "sd", "variation", "limit", "side"},
    validate=_validate_variation,
    #  Not the unit in the parameters: that is what the lengths vary across,
    #  while the spread they make is a property of the whole document.
    counted_over=lambda params: "document",
    calibrated_by=DISTRIBUTION,
)
@needs_plain_text
@per_document
def length_variation(rule, document: Document) -> Iterator[Outcome]:
    """Report a document whose units are too alike in length, or too unlike.

    The statistic is the coefficient of variation: the standard deviation of the
    units' word counts, over their mean. Dividing by the mean is what lets one
    threshold serve every document, since a spread of four words means one thing
    among nine-word sentences and another among thirty-word ones. The deviation
    is taken over every unit the document has rather than a sample of them, so it
    divides by their count and not by one less.

    Uniformity is why this check exists: sentence-length variance is among the
    most robust of the documented differences between generated and human prose.
    It is a property of the document and of no sentence in it, so the finding is
    anchored at the whole document. Anchoring it at a sentence would invite
    editing that sentence until the number moved, which leaves the prose worse
    and the measurement meaningless. See docs/rules.md and docs/linter.md.
    """
    params = rule.params
    lengths = [document.word_count(span) for span in UNIT_SPANS[params["unit"]](document)]
    words = sum(lengths)
    if len(lengths) < params["min_units"]:
        yield Abstain(
            f"{len(lengths)} {params['unit']}s in this document "
            "is too few to measure a spread over"
        )
        return
    #  At least one word whatever the rule asked for: a mean of zero has no
    #  coefficient to report.
    if words < max(params["min_words"], 1):
        yield Abstain(f"{words} words in this document is too short to measure a spread over")
        return

    mean = words / len(lengths)
    sd = sqrt(sum((length - mean) ** 2 for length in lengths) / len(lengths))
    variation = sd / mean
    outside = _outside(variation, params, "variation")
    if outside is None:
        return
    side, limit = outside
    yield Hit(
        Span(0, len(document.text)),
        {
            "unit": params["unit"],
            "count": len(lengths),
            "words": words,
            "mean": f"{mean:.1f}",
            "sd": f"{sd:.1f}",
            "variation": f"{variation:.2f}",
            "limit": f"{limit:g}",
            "side": side,
        },
    )


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
    fields=lambda params: {"entity", "mentions", "walk_ons", "introductions", "share", "limit"},
    validate=_validate_recurrence,
    counted_over=lambda params: "corpus",
    calibrated_by=DISTRIBUTION,
)
@needs_plain_text
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
