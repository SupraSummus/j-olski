"""Podkorpus milionowy NKJP wchodzi w TEI, polskie wycinki wychodzą.

Próbka tego korpusu nie jest ciągłym tekstem: stoi w niej kilkanaście sekcji
``div``, każda wzięta z innego miejsca książki albo gazety, i numer akapitu w
źródle niesie przy każdej atrybut ``n``. Ciągłość sięga więc jednego ``div``-a,
i dlatego ten krok wypisuje plik na sekcję: w pliku na próbkę zdanie z początku
jednej sekcji sąsiadowałoby ze zdaniem z końca innej, a nikt by tego nie
odróżnił od tekstu. Jak krótkie te sekcje są i którego znaleziska ta długość
pozbawia wejścia, mówi docs/corpora.md.

Deklaracji ``Czytnik`` ten krok nie bierze, bo dwa założenia tamtego rozdania tu
nie zachodzą: plik wychodzi na sekcję, a nie na plik wejściowy, i pliki
wejściowe rozpoznaje nazwa, a nie sufiks — obok ``text.xml`` stoi w katalogu
próbki sześć plików anotacji z tym samym ``.xml``.

Warstwa nazywa katalog wyjściowy, bo sądy o trafieniach czyta się warstwa po
warstwie. Bierze się ona z taksonomii w nagłówku, a nie z nazwy katalogu
próbki: nazwa mówi, z którego źródła próbka pochodzi, a samej publicystyki
płynie tu z kilkudziesięciu.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path
from xml.etree import ElementTree

from harness import PROSE_SUFFIX

#: Przestrzeń nazw TEI P5, w której stoi każdy element tego wydania,
#: oraz ta, w której stoi samo ``xml:id``.
TEI = "{http://www.tei-c.org/ns/1.0}"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"

#: Plik próbki, w którym stoi jej tekst, i plik, w którym stoi jej nagłówek.
TEKST = "text.xml"
NAGŁÓWEK = "header.xml"

#: Typ tekstu w nagłówku próbki. Stoi w ``catRef`` obok kanału, więc wzorzec
#: pyta o samo ``typ_``: kanał znaczy nośnik, a nie rejestr, i nazywa go
#: ``kanal_``.
TYP = re.compile(r'target="#(typ_[\w-]+)"')

USAGE = """
  python3 -m harness.nkjp nkjp/ --into proza/nkjp
  python3 -m harness.nkjp nkjp/ --into proza/nkjp --typ typ_konwers
"""


def typ(nagłówek: str) -> str | None:
    """Typ tekstu z nagłówka próbki, albo nic, gdy nagłówek go nie nazywa."""
    trafienie = TYP.search(nagłówek)
    return trafienie.group(1) if trafienie else None


def wycinki(tekst: str) -> Iterator[tuple[str, str]]:
    """Sekcje ``div`` tej próbki, każda ze swoją nazwą i prozą.

    Akapity jednej sekcji idą po sobie w źródle, więc rozdziela je pusty
    wiersz. Sekcja bez akapitu nie wychodzi, bo schemat archiwum pozwala jej
    stać z samym ``gap``, a plik pusty korpus liczyłby jak każdy inny.

    Nazwą jest ``xml:id``, który wiąże sekcję z akapitem źródła wypisanym w
    nagłówku, a schemat czyni ten atrybut opcjonalnym — stąd nazwa zapasowa,
    bez której sekcja bez identyfikatora nadpisywałaby sąsiadkę.

    Akapit składa się z ``itertext``, a nie z samego ``text``, choć w wydaniu
    1.2 żaden ``ab`` nie ma dziecka: znacznik dopisany w wydaniu następnym
    urwałby akapit w miejscu, w którym stanął, i nie powiedziałby o tym nic.
    """
    for numer, div in enumerate(ElementTree.fromstring(tekst).iter(f"{TEI}div"), start=1):
        akapity = ["".join(ab.itertext()).strip() for ab in div.findall(f"{TEI}ab")]
        proza = "\n\n".join(akapit for akapit in akapity if akapit)
        if proza:
            yield div.get(XML_ID) or f"div{numer}", proza


def próbki(paths: Sequence[str]) -> Iterator[tuple[Path, Path]]:
    """Katalogi próbek pod tym, co nazwano w wierszu poleceń.

    Próbką jest katalog niosący oba pliki naraz, bo warstwy bez nagłówka nie ma
    czym nazwać. Ścieżka względna idzie obok, żeby wyjście powtórzyło kształt
    wejścia poniżej katalogu warstwy, i liczy się od katalogu nad próbką, a nie
    od nazwanego: próbka nazwana wprost trzymałaby inaczej samą nazwę sekcji,
    a sekcje nazywają się w każdej próbce tak samo i nadpisywałyby się nawzajem.
    """
    for raw in paths:
        korzeń = Path(raw)
        nadrzędny = korzeń.parent if (korzeń / TEKST).exists() else korzeń
        for tekst in sorted(korzeń.rglob(TEKST)):
            if (tekst.parent / NAGŁÓWEK).exists():
                yield tekst.parent.relative_to(nadrzędny), tekst.parent


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="harness.nkjp",
        description="Extract Polish prose from the NKJP one-million subcorpus.",
        epilog=USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="+", help="the unpacked archive, or directories of samples")
    parser.add_argument(
        "--into",
        metavar="DIR",
        required=True,
        help=f"where to write the prose, as {PROSE_SUFFIX} files under a directory per text type",
    )
    parser.add_argument(
        "--typ",
        metavar="TYP",
        action="append",
        help="keep only samples of this text type, e.g. typ_konwers (repeatable)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    into = Path(args.into)
    for path in [p for p in args.paths if not Path(p).exists()]:
        print(f"harness.nkjp: no such file or directory: {path}", file=sys.stderr)

    napisane, bez_typu = 0, 0
    for relative, próbka in próbki(args.paths):
        warstwa = typ((próbka / NAGŁÓWEK).read_text(encoding="utf-8"))
        if warstwa is None:
            bez_typu += 1
            continue
        if args.typ and warstwa not in args.typ:
            continue
        for nazwa, proza in wycinki((próbka / TEKST).read_text(encoding="utf-8")):
            plik = into / warstwa / relative / f"{nazwa}{PROSE_SUFFIX}"
            plik.parent.mkdir(parents=True, exist_ok=True)
            plik.write_text(proza + "\n", encoding="utf-8")
            napisane += 1
    print(f"{napisane} files into {into}, {bez_typu} samples with no text type")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
