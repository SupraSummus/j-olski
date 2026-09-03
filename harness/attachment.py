"""Dokąd bank drzew przyłącza wyrażenie przyimkowe stojące po grupie imiennej.

Sonda ta mierzy korpus, a nie gramatykę, i tym różni się od
``harness/pomiar.py`` obok. Pyta o samą polszczyznę: gdy zdanie stawia wyrażenie
przyimkowe tuż za grupą imienną, a więc daje czytelnikowi dwa przyłączenia do
wyboru, to które z nich wybiera człowiek, który to zdanie rozbierał. Liczba stąd
rozstrzygnęła, którym wyjściem z przyłączania idzie olski
(``docs/subset.md``), i stoi tu po to, żeby dało się ją powtórzyć.

Rusza ją wydanie korpusu i to, co ten moduł liczy, a nie zmiana w gramatyce:
żadna produkcja olskiego nie ma tu nic do powiedzenia, bo mierzone są cudze
drzewa. Przebieg idzie więc jednym procesem, gdzie ``harness/pomiar.py`` obok
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
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.corpus import Constituent, constituents, parse_forest, read_forest
from harness.komenda import Komenda, uruchom

#: Ile przyimków wchodzi pod rozkład, gdy wiersz poleceń nie mówi inaczej.
PRZYIMKI = 10

#: Kategoria wyrażenia przyimkowego w gramatyce, z której Składnica powstała.
PP = "fpm"

#: Kategoria grupy imiennej.
NP = "fno"

#: Kategorie, których węzeł jest zdaniem albo frazą czasownikową, czyli tym, co
#: dla olskiego jest przyłączeniem do czasownika.
CLAUSE = frozenset({"wypowiedzenie", "zdanie", "ff", "fzd", "formaczas", "condaglt"})

#: Dwie strony wyboru, czyli wartości pola ``host``: gospodarz imienny i gospodarz
#: czasownikowy. Napis wydany tutaj jest zarazem kluczem liczników niżej i
#: wydrukiem, a czytają go stąd sondy z ``harness/``; ``olski/rozstrzyganie.py``
#: trzyma drugą kopię i mówi przy niej, dlaczego.
STRONA_IMIENNA, STRONA_CZASOWNIKOWA = "noun", "clause"

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
    """Jedno wyrażenie przyimkowe wybranego drzewa, i dokąd doszło."""

    #: :data:`STRONA_IMIENNA`, :data:`STRONA_CZASOWNIKOWA` albo kategoria węzła,
    #: jeśli to ani jedno, ani drugie.
    host: str
    #: Czy przed wyrażeniem stoi forma czasownikowa. Bez niej przyłączenie do
    #: czasownika nie było do wzięcia.
    postverbal: bool
    #: Czy tuż przed wyrażeniem kończy się grupa imienna. Bez niej wyboru nie
    #: było z drugiej strony, więc te dwa pola razem mówią, czy pozycja jest
    #: dwuznaczna.
    postnominal: bool
    #: Przyimek, jak stoi w tekście, małymi literami.
    prep: str
    #: ``fw``, ``fl`` albo ``None``, gdy wyrażenie nie stoi pod żadną z nich.
    frame: str | None
    #: Lemat rzeczownika, do którego wyrażenie mogło dojść: ostatnia forma grupy
    #: imiennej kończącej się tuż przed nim. Pusty, gdy tej formy nie ma.
    noun: str = ""
    #: Lemat najbliższej formy czasownikowej przed wyrażeniem, czyli drugiego
    #: gospodarza do wzięcia. Pusty, gdy przed wyrażeniem czasownika nie ma.
    verb: str = ""
    #: Lemat ostatniej formy samego wyrażenia, czyli tego, czym przyimek rządzi.
    #: Trzy lematy razem są czwórką, na której pole mierzy przyłączanie, i biorą
    #: się stąd, a nie z drzewa, bo maszyna rozstrzygająca też ich stąd nie ma:
    #: zna zdanie i las, a nie rozbiór wzorcowy.
    object: str = ""
    #: Rozpiętość samego wyrażenia w numerach tokenów Składnicy, czyli to, po
    #: czym wybiera się jego formy z ``Sentence.segments``.
    start: int = 0
    end: int = 0


def attachments(element: ET.Element) -> list[Attachment]:
    """Wyrażenia przyimkowe wybranego drzewa, każde z tym, gdzie stoi i dokąd doszło.

    Populacji ta funkcja nie stawia, bo pytają o nią dwa pomiary i każdy o inną.
    :class:`Report` niżej liczy pozycję dwuznaczną. Wzorca dla warstwy
    rozstrzygającej szuka się natomiast tam, gdzie wybór postawił werdykt
    olskiego, czyli i przy wyrażeniu, przed którym grupa imienna się nie kończy
    (``harness/wskazania.py``). Zwężenie jest więc polem, a nie pominięciem.
    """
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
        if node.category != PP:
            continue
        host, frame = _dokąd_doszło(node)
        if host is None:
            continue
        prep = forms.get(node.start)
        poprzednie = [start for start in forms if start < node.start]
        found.append(
            Attachment(
                host=host,
                postverbal=any(verb < node.start for verb in verbs),
                postnominal=node.start in kończy_się,
                prep=prep.form.lower() if prep else "",
                frame=frame,
                noun=_lemat(forms, max(poprzednie, default=None)),
                verb=_lemat(forms, max((v for v in verbs if v < node.start), default=None)),
                object=_lemat(forms, max((s for s in forms if s < node.end), default=None)),
                start=node.start,
                end=node.end,
            )
        )
    return found


def _lemat(forms: dict[int, object], start: int | None) -> str:
    """Lemat formy zaczynającej się w tym miejscu, małymi literami.

    Pod złotą morfologią Składnicy forma ma dokładnie jedno czytanie, więc lemat
    jest jeden; pusty napis znaczy, że formy tam nie ma.
    """
    segment = forms.get(start) if start is not None else None
    if segment is None or not segment.readings:
        return ""
    return segment.readings[0].lemma.lower()


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
        return STRONA_IMIENNA, frame
    if parent.category in CLAUSE:
        return STRONA_CZASOWNIKOWA, frame
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
        if not attachment.postnominal:
            return
        self.seen += 1
        if not attachment.postverbal:
            return
        self.postverbal[attachment.host] += 1
        if attachment.host not in (STRONA_IMIENNA, STRONA_CZASOWNIKOWA):
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


def render(report: Report, preps: int = PRZYIMKI) -> str:
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
        f"{report.required[STRONA_CZASOWNIKOWA]} przyłączonych do czasownika "
        f"i {report.required[STRONA_IMIENNA]} przyłączonych do rzeczownika",
        "",
        "po przyimku, wśród przyłączeń do rzeczownika i do czasownika:",
    ]
    ranking = sorted(report.preps.items(), key=lambda para: -sum(para[1].values()))
    for prep, counts in ranking[:preps]:
        razem = sum(counts.values())
        lines.append(
            f"  {prep:12} {razem:6}  {counts[STRONA_IMIENNA] / razem:6.1%} do rzeczownika"
        )
    return "\n".join(lines)


def _przyimki(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--przyimki", type=int, default=PRZYIMKI, help="ile przyimków wypisać")


def _korpus(ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    return render(measure(ścieżki), args.przyimki)


KOMENDA = Komenda(
    nazwa="harness.attachment",
    opis="Policz, dokąd Składnica przyłącza wyrażenie przyimkowe za grupą imienną.",
    korpus=_korpus,
    argumenty=_przyimki,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
