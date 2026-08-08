"""Dokąd bank drzew przyłącza wyrażenie przyimkowe stojące po grupie imiennej.

To jest pomiar korpusu, a nie gramatyki, i tym różni się od
``olski/coverage.py`` obok. Pyta o samą polszczyznę: gdy zdanie stawia wyrażenie
przyimkowe tuż za grupą imienną, a więc daje czytelnikowi dwa przyłączenia do
wyboru, to które z nich wybiera człowiek, który to zdanie rozbierał. Liczba stąd
rozstrzygnęła, którym wyjściem z przyłączania idzie olski
(``docs/subset.md``), i stoi tu po to, żeby dało się ją powtórzyć.

Rusza ją wydanie korpusu i to, co ten moduł liczy, a nie zmiana w gramatyce:
żadna produkcja olskiego nie ma tu nic do powiedzenia, bo mierzone są cudze
drzewa. Przebieg idzie więc jednym procesem, gdzie ``olski/coverage.py`` obok
dzieli pracę na pulę: raz na wydanie korpusu minuta nie jest ceną, za którą warto
mieć drugą maszynerię.

Populacją są wyrażenia w pozycji dwuznacznej, a nie wszystkie. Wyrażenie, przed
którym nie kończy się żadna grupa imienna, nie ma do czego się przyłączyć poza
zdaniem, więc o wyborze nie mówi nic i wchodzi tylko do liczby wszystkich.
Wyrażenie, przed którym nie stoi żadna forma czasownikowa, zwęża wybór z drugiej
strony, i to dlatego liczba po czasowniku jest tu mianownikiem, a nie tamta.
"""

from __future__ import annotations

import argparse
import collections
import sys
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.corpus import Constituent, constituents, parse_forest, pliki, read_forest

#: Kategoria wyrażenia przyimkowego w gramatyce, z której Składnica powstała.
PP = "fpm"

#: Kategoria grupy imiennej.
NP = "fno"

#: Kategorie, których węzeł jest zdaniem albo frazą czasownikową, czyli tym, co
#: dla olskiego jest przyłączeniem do czasownika.
CLAUSE = frozenset({"wypowiedzenie", "zdanie", "ff", "fzd", "formaczas", "condaglt"})

#: Fraza wymagana i fraza luźna: to, czy schemat czasownika tej frazy żąda, czy
#: stoi ona przy nim swobodnie. Różnica dzieli przyłączenia do czasownika na te,
#: które rozstrzygnie walencja, i na resztę.
WYMAGANA, LUŹNA = "fw", "fl"

#: Części mowy, które w tagsecie Składnicy niesie forma czasownikowa.
CZASOWNIK = frozenset(
    {"fin", "praet", "impt", "bedzie", "inf", "ppas", "pact", "winien", "imps", "pred"}
)


@dataclass(frozen=True)
class Attachment:
    """Jedno wyrażenie przyimkowe stojące za grupą imienną, i dokąd doszło."""

    #: ``noun``, ``clause`` albo kategoria węzła, jeśli to ani jedno, ani drugie.
    host: str
    #: Czy przed wyrażeniem stoi forma czasownikowa. Bez niej przyłączenie do
    #: czasownika nie było do wzięcia.
    postverbal: bool
    #: Przyimek, jak stoi w tekście, małymi literami.
    prep: str
    #: ``fw``, ``fl`` albo ``None``, gdy wyrażenie nie stoi pod żadną z nich.
    frame: str | None


def attachments(element: ET.Element) -> list[Attachment]:
    """Wyrażenia przyimkowe jednego lasu, te w pozycji dwuznacznej."""
    sentence = parse_forest(element)
    if not sentence.annotated:
        return []
    nodes = constituents(element)
    forms = {segment.start: segment for segment in sentence.segments}
    verbs = [
        start
        for start, segment in forms.items()
        if any(reading.tag.pos in CZASOWNIK for reading in segment.readings)
    ]
    kończy_się = {node.end for node in nodes if node.category == NP}
    found = []
    for node in nodes:
        if node.category != PP or node.start not in kończy_się:
            continue
        host, frame = _dokąd_doszło(node)
        if host is None:
            continue
        prep = forms.get(node.start)
        found.append(
            Attachment(
                host=host,
                postverbal=any(verb < node.start for verb in verbs),
                prep=prep.form.lower() if prep else "",
                frame=frame,
            )
        )
    return found


def _dokąd_doszło(node: Constituent) -> tuple[str | None, str | None]:
    """Do czego wyrażenie doszło i pod jaką frazą po drodze stanęło.

    Miejscem przyłączenia jest pierwszy przodek szerszy od samego wyrażenia.
    Węzły o tej samej rozpiętości są opakowaniem — fraza wymagana, fraza luźna —
    a nie miejscem przyłączenia, więc zejście przez nie przechodzi i po drodze je
    zapamiętuje.
    """
    frame = None
    parent = node.parent
    while parent is not None and (parent.start, parent.end) == (node.start, node.end):
        if frame is None and parent.category in (WYMAGANA, LUŹNA):
            frame = parent.category
        parent = parent.parent
    if parent is None:
        return None, frame
    if parent.category == NP:
        return "noun", frame
    if parent.category in CLAUSE:
        return "clause", frame
    return parent.category, frame


@dataclass
class Report:
    """Rozkład przyłączeń, i tyle podziałów, ile go czyta."""

    #: Ile wyrażeń stanęło za grupą imienną, czyli mianownik szerszy z dwóch.
    seen: int = 0
    postverbal: collections.Counter = field(default_factory=collections.Counter)
    #: Rozkład po przyimku, po jednym liczniku na przyimek.
    preps: dict[str, collections.Counter] = field(default_factory=dict)
    #: Ile przyłączeń niesie fraza wymagana, po jednym liczniku na miejsce
    #: przyłączenia. Po stronie czasownika jest to ta część klasy, która czeka
    #: na walencję, a nie na czytelnika; po stronie rzeczownika — wyrażenie,
    #: którego żąda sam rzeczownik, a więc nie stojące do wyboru wcale.
    required: collections.Counter = field(default_factory=collections.Counter)

    def record(self, attachment: Attachment) -> None:
        self.seen += 1
        if not attachment.postverbal:
            return
        self.postverbal[attachment.host] += 1
        if attachment.host not in ("noun", "clause"):
            return
        self.preps.setdefault(attachment.prep, collections.Counter())[attachment.host] += 1
        if attachment.frame == WYMAGANA:
            self.required[attachment.host] += 1


def measure(paths: Iterable[Path]) -> Report:
    report = Report()
    for path in paths:
        for attachment in attachments(read_forest(path)):
            report.record(attachment)
    return report


def render(report: Report, preps: int = 10) -> str:
    po = sum(report.postverbal.values())
    lines = [
        f"{report.seen} wyrażeń przyimkowych za grupą imienną,",
        f"z czego {po} w zdaniu, w którym czasownik stoi przed wyrażeniem.",
        "",
        "dokąd doszły te ostatnie:",
    ]
    for host, count in report.postverbal.most_common():
        lines.append(f"  {count:6} {count / po:6.1%}  {host}")
    lines += [
        "",
        "z tego frazą wymaganą jest "
        f"{report.required['clause']} przyłączonych do czasownika "
        f"i {report.required['noun']} przyłączonych do rzeczownika",
        "",
        "po przyimku, wśród przyłączeń do rzeczownika i do czasownika:",
    ]
    ranking = sorted(report.preps.items(), key=lambda para: -sum(para[1].values()))
    for prep, counts in ranking[:preps]:
        razem = sum(counts.values())
        lines.append(f"  {prep:12} {razem:6}  {counts['noun'] / razem:6.1%} do rzeczownika")
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m olski.attachment",
        description="Policz, dokąd Składnica przyłącza wyrażenie przyimkowe za grupą imienną.",
    )
    parser.add_argument("root", help="katalog z rozpakowaną Składnicą")
    parser.add_argument("--limit", type=int, help="zatrzymaj się po tylu lasach")
    parser.add_argument("--preps", type=int, default=10, help="ile przyimków wypisać")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"olski.attachment: nie ma takiego katalogu: {root}", file=sys.stderr)
        print("olski.attachment: skąd wziąć korpus, mówi docs/corpus.md", file=sys.stderr)
        return 2
    print(render(measure(pliki(root)[: args.limit]), args.preps))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
