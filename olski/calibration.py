"""Kształty kalibracji, czyli to, co o regule zmierzono.

Kalibracja nie jest regułą i nie jest checkiem, więc stoi w module poniżej obu.
Kupuje to jedno: check nazywa kształt, którego żąda, wprost klasą, a nie
napisem, który ktoś odwzorowuje z powrotem na klasę u siebie.

Reguła wysyłana niesie UNCALIBRATED, bo tyle jest uczciwe, dopóki nikt niczego
nie zmierzył. Harness milestone'u 1 podstawia w to miejsce jeden z dwóch
kształtów, ten, którego żąda check tej reguły. Kształty stoją tutaj, a nie u
tego, kto weźmie pierwszy pomiar, bo format wybrany przez pomiar pasuje do tego
pomiaru i do niczego więcej. Który rodzaj reguły co jest winien, trzyma
docs/linter.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import ClassVar


class CalibrationError(Exception):
    """Kalibracja niesie liczbę, której żaden pomiar nie mógłby dać."""


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

    #: What a rule owes while nothing has been measured, for ``--explain`` to
    #: print under a rule that ships ``UNCALIBRATED``. The phrase names the prose
    #: the first measurement is taken over, because that is what differs between
    #: the shapes and what decides which corpus has to be fetched. Annotated
    #: without a value, so a shape carrying none is a shape nothing can print.
    owed: ClassVar[str]

    corpus: str
    taken: str

    def __post_init__(self) -> None:
        if not isinstance(self.corpus, str) or not self.corpus.strip():
            raise CalibrationError("a calibration names the corpus its numbers came from")
        try:
            date.fromisoformat(self.taken)
        except (TypeError, ValueError):
            raise CalibrationError(f"calibration date {self.taken!r} is not an ISO date") from None


@dataclass(frozen=True)
class Audit(Measurement):
    """A rule's hits, read one by one, and how many of them were real defects.

    The shape for a rule whose answer depends on the site rather than on the
    rate. A firing rate over published prose measures the editor who took the
    defect out rather than the rule, so what such a rule owes is its hits at the
    stage a linter sees them, read by a person. docs/linter.md owns the
    argument.
    """

    owed: ClassVar[str] = "an audit of its hits, read one by one"

    hits: int
    defects: int

    def __post_init__(self) -> None:
        super().__post_init__()
        _whole(self.hits, "hits", least=1)
        _whole(self.defects, "count of real defects", least=0)
        if self.defects > self.hits:
            raise CalibrationError(
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

    owed: ClassVar[str] = "a distribution over human Polish"

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


def _whole(value, what: str, least: int) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value < least:
        raise CalibrationError(f"a calibration's {what} must be a whole number, {least} or more")


def _number(value, what: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
        raise CalibrationError(f"a calibration's {what} must be a non-negative number")


def _share(value, what: str) -> None:
    _number(value, what)
    if value > 1:
        raise CalibrationError(
            f"a calibration's {what} is a share of the whole, so it cannot exceed 1"
        )
