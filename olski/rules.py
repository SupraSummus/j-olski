"""Rules as data, written in Python.

A rule is a declaration, not a function: it names a check kind, supplies that
check's parameters, and carries the four things the roadmap asks of every rule —
an identifier, a message, the pack and registers it belongs to, and a recorded
justification. Adding a rule means adding a declaration to a pack module.
Adding a *kind* of rule means adding a check, which is the rarer event.

What a rule has been measured for is data in the same way. A rule ships
``UNCALIBRATED``, and the milestone 1 harness replaces that with an
:class:`Audit` or a :class:`Distribution`, whichever the rule's check calls for.
The shapes are settled here rather than by whoever takes the first measurement,
because a format chosen by a measurement fits that measurement and nothing else.
docs/linter.md owns which kind of rule owes which.

Python rather than YAML because the configuration is already a program's data
structure: a declaration is validated the moment its pack is imported, the
error names the rule, patterns are ordinary raw strings, and there is no schema
language standing between the two.
"""

from __future__ import annotations

import importlib
import importlib.util
import pkgutil
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from string import Formatter

SEVERITIES = ("note", "warning", "error")

TIERS = ("A", "A+", "B", "C", "D")


class RuleError(Exception):
    """A rule declaration is not usable."""


@dataclass(frozen=True)
class Uncalibrated:
    """Nothing has been measured, which is what every rule ships with.

    The honest default: a rule that nobody has measured says so, rather than
    carrying a number nobody took.
    """

    def __str__(self) -> str:
        return "uncalibrated"


#: The default. One instance, because an absence of numbers has no variants.
UNCALIBRATED = Uncalibrated()


@dataclass(frozen=True)
class Measurement:
    """The provenance a number carries: the prose it came from, and the date.

    What a rate can mean is decided by the body of text it was taken over, so a
    number without those two is not a measurement. ``corpus`` names prose
    somebody else can fetch, which is what lets a number be redone rather than
    believed.
    """

    corpus: str
    taken: str

    def __post_init__(self) -> None:
        if not isinstance(self.corpus, str) or not self.corpus.strip():
            raise RuleError("a calibration names the corpus its numbers came from")
        try:
            date.fromisoformat(self.taken)
        except (TypeError, ValueError):
            raise RuleError(f"calibration date {self.taken!r} is not an ISO date") from None


@dataclass(frozen=True)
class Audit(Measurement):
    """A rule's hits, read one by one, and how many of them were real defects.

    The shape for a rule whose answer depends on the site rather than on the
    rate. A firing rate over published prose measures the editor who took the
    defect out rather than the rule, so what such a rule owes is its hits at the
    stage a linter sees them, read by a person. docs/linter.md owns the
    argument.
    """

    hits: int
    defects: int

    def __post_init__(self) -> None:
        super().__post_init__()
        _whole(self.hits, "hits", least=1)
        _whole(self.defects, "count of real defects", least=0)
        if self.defects > self.hits:
            raise RuleError(
                f"a calibration over {self.hits} hits cannot find "
                f"{self.defects} real defects among them"
            )

    @property
    def precision(self) -> float:
        """The share of the hits that were real defects."""
        return self.defects / self.hits

    def __str__(self) -> str:
        return (
            f"{self.defects} of {self.hits} hits were real defects "
            f"({self.precision:.0%}), read over {self.corpus}, {self.taken}"
        )


@dataclass(frozen=True)
class Distribution(Measurement):
    """Where a rule's threshold sits in the distribution of human Polish.

    The shape for a rule reporting a rate against a norm. ``median`` is where
    prose somebody edited sits on the statistic the rule measures, ``accused``
    is the share of that prose the threshold fires on, which is what the
    threshold costs the writing the rule was built to protect, and ``scopes``
    is how many documents, paragraphs or sentences the distribution was taken
    over, since a distribution over five of them is not one.

    The threshold itself is not here. A rule's ``params`` own it, and a second
    copy would go stale the first time it moved.
    """

    median: float
    accused: float
    scopes: int

    def __post_init__(self) -> None:
        super().__post_init__()
        _whole(self.scopes, "scopes", least=1)
        _number(self.median, "median")
        _share(self.accused, "accused")

    def __str__(self) -> str:
        scopes = f"{self.scopes} scope" + ("" if self.scopes == 1 else "s")
        return (
            f"fires on {self.accused:.1%} of human prose, whose median is {self.median:g}, "
            f"over {scopes} of {self.corpus}, {self.taken}"
        )


#: What a rule may carry: nothing measured, or numbers in one of the two shapes.
Calibration = Uncalibrated | Measurement

#: Which class carries which shape, the other half of ``Check.calibrated_by``,
#: which is where the names come from.
SHAPES = {"audit": Audit, "distribution": Distribution}


def _whole(value, what: str, least: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < least:
        raise RuleError(f"a calibration's {what} must be a whole number, {least} or more")


def _number(value, what: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        raise RuleError(f"a calibration's {what} must be a non-negative number")


def _share(value, what: str) -> None:
    _number(value, what)
    if value > 1:
        raise RuleError(f"a calibration's {what} is a share of the whole, so it cannot exceed 1")


@dataclass(frozen=True)
class Rule:
    id: str
    #: The name of a check in :mod:`olski.checks`.
    check: str
    #: A format template. Placeholders are filled from the fields the check
    #: reports for these parameters, and are checked against them on construction.
    message: str
    #: Why this rule exists, in prose. Anchored to a Polish style norm where one
    #: exists, because a rule justified by a model's habits dates and a rule
    #: justified by Polish style does not.
    justification: str
    #: Parameters for the named check, as the check validated them.
    params: dict = field(default_factory=dict)
    sources: tuple[str, ...] = ()
    pack: str = "unnamed"
    registers: tuple[str, ...] = ()
    tier: str = "A"
    severity: str = "warning"
    #: What has been measured about this rule, as a :class:`Calibration`: the
    #: default until the milestone 1 harness replaces it with an :class:`Audit`
    #: or a :class:`Distribution`, whichever the rule's check calls for.
    calibration: Calibration = UNCALIBRATED
    origin: str = "<memory>"

    def __post_init__(self) -> None:
        from olski.checks import ParamError, get_check  # one-way layering

        where = f"{self.origin}: rule {self.id!r}"
        if not self.id or not isinstance(self.id, str):
            raise RuleError(f"{self.origin}: a rule is missing its id")
        for name in ("message", "justification"):
            if not getattr(self, name).strip():
                raise RuleError(f"{where}: {name} is empty")
        if self.severity not in SEVERITIES:
            raise RuleError(f"{where}: severity must be one of {', '.join(SEVERITIES)}")
        if self.tier not in TIERS:
            raise RuleError(f"{where}: tier must be one of {', '.join(TIERS)}")

        # Prose is written with semantic line breaks, so fold it before use.
        object.__setattr__(self, "message", _fold(self.message))
        object.__setattr__(self, "justification", _fold(self.justification))

        try:
            check = get_check(self.check, where)
            object.__setattr__(self, "params", check.validate(dict(self.params), where))
        except ParamError as error:
            raise RuleError(str(error)) from None

        owed = SHAPES[check.calibrated_by]
        if not isinstance(self.calibration, (Uncalibrated, owed)):
            raise RuleError(
                f"{where}: check {self.check!r} calls for {check.calibrated_by} calibration, "
                f"so this rule carries UNCALIBRATED or {owed.__name__}, not {self.calibration!r}"
            )

        #  What a check reports can follow from the parameters just validated —
        #  a rate rule with no ceiling has no occurrence to quote — so the fields
        #  are asked for after the validation and not before it.
        fields = check.fields(self.params)
        unsupported = _placeholders(self.message) - fields
        if unsupported:
            named = ", ".join(sorted(unsupported))
            reports = ", ".join(sorted(fields)) or "nothing"
            raise RuleError(
                f"{where}: message uses {named}, but check {self.check!r} reports {reports}"
            )

    def format(self, fields: dict) -> str:
        return self.message.format(**fields)


class Pack:
    """A named group of rules that share a register and a set of defaults.

    Rules belong to packs and packs belong to registers, so that no rule ships
    without knowing which register it is defensible in.
    """

    def __init__(
        self,
        name: str,
        *,
        registers: tuple[str, ...] = (),
        tier: str = "A",
        severity: str = "warning",
        calibration: Calibration = UNCALIBRATED,
        origin: str | None = None,
    ) -> None:
        self.name = name
        self.origin = origin or _caller_module()
        self.defaults = {
            "pack": name,
            "registers": registers,
            "tier": tier,
            "severity": severity,
            "calibration": calibration,
            "origin": self.origin,
        }
        self.rules: list[Rule] = []

    def rule(self, **fields) -> Rule:
        """Declare a rule, filling anything unset from the pack's defaults."""
        rule = Rule(**{**self.defaults, **fields})
        if any(existing.id == rule.id for existing in self.rules):
            raise RuleError(f"{self.origin}: duplicate rule id {rule.id!r}")
        self.rules.append(rule)
        return rule

    def __iter__(self):
        return iter(self.rules)

    def __len__(self) -> int:
        return len(self.rules)


#: Where the shipped packs live.
PACK_PACKAGE = "olski.packs"

#: Module namespace for packs loaded from a path rather than imported by name.
LOADED_PREFIX = "olski._loaded_packs."


def load_packs(paths: list[str | Path] | None = None) -> list[Rule]:
    """Collect rules from the shipped packs, or from given pack modules.

    A path may be a ``.py`` file declaring a :class:`Pack`, a directory of them,
    or an importable module name.
    """
    if paths is None:
        packs = [_import(name) for name in _shipped()]
    else:
        packs = []
        for path in paths:
            packs.extend(_load_path(path))

    rules: list[Rule] = []
    seen: dict[str, str] = {}
    for pack in packs:
        for rule in pack:
            if rule.id in seen:
                raise RuleError(
                    f"{rule.origin}: duplicate rule id {rule.id!r}, "
                    f"already declared in {seen[rule.id]}"
                )
            seen[rule.id] = rule.origin
            rules.append(rule)
    return rules


def _shipped() -> list[str]:
    package = importlib.import_module(PACK_PACKAGE)
    return sorted(
        f"{PACK_PACKAGE}.{info.name}"
        for info in pkgutil.iter_modules(package.__path__)
        if not info.name.startswith("_")
    )


def _load_path(path: str | Path) -> list[Pack]:
    candidate = Path(path)
    if candidate.is_dir():
        files = sorted(p for p in candidate.glob("*.py") if not p.name.startswith("_"))
        if not files:
            raise RuleError(f"no pack modules in {candidate}")
        return [_import_file(f) for f in files]
    if candidate.suffix == ".py":
        if not candidate.exists():
            raise RuleError(f"no such pack: {candidate}")
        return [_import_file(candidate)]
    return [_import(str(path))]


def _import(name: str) -> Pack:
    try:
        module = importlib.import_module(name)
    except ImportError as error:
        raise RuleError(f"cannot import pack {name!r}: {error}") from error
    return _pack_of(module, name)


def _import_file(path: Path) -> Pack:
    name = f"{LOADED_PREFIX}{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuleError(f"cannot load pack from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as error:  # a pack is code; say which file broke
        del sys.modules[name]
        raise RuleError(f"{path}: {type(error).__name__}: {error}") from error
    return _pack_of(module, str(path))


def _pack_of(module, where: str) -> Pack:
    pack = getattr(module, "pack", None)
    if not isinstance(pack, Pack):
        raise RuleError(f"{where}: expected a module-level 'pack' of type Pack")
    if not len(pack):
        raise RuleError(f"{where}: pack {pack.name!r} declares no rules")
    return pack


def select(rules: list[Rule], packs: Sequence[str] = (), ids: Sequence[str] = ()) -> list[Rule]:
    """Filter rules by pack name and by rule id, both optional, ids globbable."""
    chosen = rules
    if packs:
        chosen = [r for r in chosen if r.pack in packs]
    if ids:
        patterns = [re.compile(_glob(i)) for i in ids]
        chosen = [r for r in chosen if any(p.fullmatch(r.id) for p in patterns)]
    return chosen


def _fold(prose: str) -> str:
    return " ".join(prose.split())


def _placeholders(template: str) -> set[str]:
    return {name for _, name, _, _ in Formatter().parse(template) if name}


def _glob(pattern: str) -> str:
    return ".*".join(re.escape(part) for part in pattern.split("*"))


def _caller_module() -> str:
    """Name the module a pack was declared in, for use in error messages."""
    frame = sys._getframe(2)
    name = frame.f_globals.get("__name__", "<memory>")
    # A pack loaded from a path has a synthetic module name that would mean
    # nothing to the person who wrote the file, so name the file instead.
    if name.startswith(LOADED_PREFIX):
        return frame.f_globals.get("__file__", name)
    return name
