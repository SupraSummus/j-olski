"""Rules as data, written in Python.

A rule is a declaration, not a function: it names a check kind, supplies that
check's parameters, and carries the four things the roadmap asks of every rule —
an identifier, a message, the pack and registers it belongs to, and a recorded
justification. Adding a rule means adding a declaration to a pack module.
Adding a *kind* of rule means adding a check, which is the rarer event.

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
from pathlib import Path
from string import Formatter

SEVERITIES = ("note", "warning", "error")

TIERS = ("A", "A+", "B", "C", "D")


class RuleError(Exception):
    """A rule declaration is not usable."""


@dataclass(frozen=True)
class Rule:
    id: str
    #: The name of a check in :mod:`olski.checks`.
    check: str
    #: A format template. Placeholders are filled from the fields the check
    #: reports, and are checked against that check on construction.
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
    #: What is known about this rule's discrimination. Every rule ships
    #: ``uncalibrated`` until the milestone 1 harness gives it two numbers:
    #: how often it fires on generated Polish, and how often on good human
    #: Polish. A rule that fires equally on both is worthless.
    calibration: str = "uncalibrated"
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

        unsupported = _placeholders(self.message) - check.fields
        if unsupported:
            named = ", ".join(sorted(unsupported))
            reports = ", ".join(sorted(check.fields)) or "nothing"
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
        calibration: str = "uncalibrated",
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
