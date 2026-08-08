"""The calibration harness: what turns a corpus into something olski can read.

Milestone 0 keeps document formats out of the linter, so a corpus in a markup
format reaches the rules through here rather than through olski. What an
extraction invents by doing that is docs/extraction.md for a document and
docs/prose-in-code.md for a module, since a transformation rules fire on owes an
account exactly as a rule owes a false-positive rate.

Only the reading of one file differs between formats. The walk over a tree, the
selection by language and the mirrored output are the same step every time, so
they live here, and a format arrives as a declaration rather than as a second
path through them.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

from olski.document import TEXT_SUFFIXES, WORD

#: What an extraction writes, taken from olski rather than spelled again, so
#: that the format this produces and the format the linter walks cannot drift
#: apart. The first entry is the ordinary one.
PROSE_SUFFIX = TEXT_SUFFIXES[0]


@dataclass(frozen=True)
class Jednostka:
    """Kawałek prozy z jednego pliku i wiersz, w którym się zaczyna.

    Jednostką jest tyle tekstu, ile stoi w jednym języku, bo tyle właśnie waży
    wybór po języku. Dokument jest nią w całości, a w module jest nią docstring
    albo blok komentarza z osobna: słowa kluczowe i klucze konfiguracji zostają
    po angielsku, a prozę i nazwy bierzemy po polsku (zob. CLAUDE.md), więc moduł
    miesza dwa języki z założenia i próg nad całym plikiem nie ma nad czym stanąć.

    Wiersz idzie razem z tekstem, bo po ekstrakcji nie ma z czego go odtworzyć:
    w prozie modułu nie ma już kodu, który stał między jedną jednostką a drugą.
    """

    wiersz: int
    tekst: str


@dataclass(frozen=True)
class Czytnik:
    """Czym jeden format różni się od drugiego, gdy prozę wyjmuje się z pliku.

    Reszta kroku jest jedna, więc format jest tu deklaracją, a nie drugą ścieżką
    przez ten sam kod: niesie sufiks, po którym obejście drzewa poznaje jego
    pliki, funkcję, która z pliku robi jednostki, i to, czym komenda przedstawia
    się w pomocy, ze słowem na jednostkę włącznie, bo dokument i docstring nie
    nazywają się tak samo.
    """

    komenda: str
    sufiks: str
    nazwa_jednostki: str
    opis: str
    użycie: str
    jednostki: Callable[[str], Sequence[Jednostka]]


#: A letter Polish spelling has and English spelling does not, which is the
#: cheapest evidence available about which language a text is in.
DIACRITIC = re.compile(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]")


def polish_share(text: str) -> float:
    """The share of a text's words that carry a Polish diacritic.

    A repository of notes holds the ones its author wrote in English, and a rate
    over Polish should not have them in its denominator. The two populations
    separate rather than shade into each other: over the notes
    docs/generated-polish.md measures, one English note in forty reaches 3% and
    every Polish one is above 13%, so any threshold between the two picks the
    same documents. Words are counted as olski counts them, so the share and the
    rates it selects for are measured over the same tokens.

    A third population sits between those two: a document whose prose is English
    and whose sections are being written in Polish one at a time. No threshold
    separates it from either, so what settles it is the unit rather than the
    number. The share is asked of a whole document, and a mixed one is left out
    until it has been translated. Asked of a paragraph it separates nothing at
    all, an English paragraph quoting Polish examples carrying as many diacritics
    as a Polish one, so the finer unit is not available.

    It is available where the unit is a docstring or a block of comment, since
    that unit is not a paragraph but everything one author wrote in one language,
    and a floor on words is what keeps the shortest of them out of the measure.
    So the threshold belongs to the caller rather than to this function, and
    docs/prose-in-code.md owns what it takes to set one over code.
    """
    words = WORD.findall(text)
    return sum(1 for word in words if DIACRITIC.search(word)) / len(words) if words else 0.0


def uruchom(argv: Sequence[str] | None, czytnik: Czytnik) -> int:
    """Wypisuje prozę tego, co nazwano w wierszu poleceń, plik za plikiem.

    Plik, z którego nie została ani jedna jednostka, nie powstaje: inaczej wybór
    po języku zostawiałby po odrzuconym dokumencie pusty plik, który korpus liczy
    jak każdy inny.
    """
    args = _parser(czytnik).parse_args(argv)
    into = Path(args.into)
    missing = [path for path in args.paths if not Path(path).exists()]
    for path in missing:
        print(f"{czytnik.komenda}: no such file or directory: {path}", file=sys.stderr)

    written, left_out = 0, 0
    for relative, file in _sources(args.paths, czytnik.sufiks):
        units = czytnik.jednostki(file.read_text(encoding="utf-8"))
        kept = [j for j in units if _po_polsku(j.tekst, args.polish, args.min_words)]
        left_out += len(units) - len(kept)
        if not kept:
            continue
        destination = into / relative.with_suffix(PROSE_SUFFIX)
        destination.parent.mkdir(parents=True, exist_ok=True)
        body = "\n\n".join(j.tekst for j in kept)
        destination.write_text(body + "\n" if body else "", encoding="utf-8")
        written += 1
    print(f"{written} files into {into}, {left_out} left out by the selection")
    return 2 if missing else 0


def _po_polsku(text: str, share: float, floor: int) -> bool:
    """Czy jednostka wchodzi do korpusu polszczyzny: udział i długość naraz.

    Podłoga jest osobnym parametrem, a nie liczbą ukrytą w progu, bo mówi coś
    innego: nad którym tekstem ten udział w ogóle coś znaczy.
    """
    return polish_share(text) >= share and len(WORD.findall(text)) >= floor


def _parser(czytnik: Czytnik) -> argparse.ArgumentParser:
    unit = czytnik.nazwa_jednostki
    parser = argparse.ArgumentParser(
        prog=czytnik.komenda,
        description=czytnik.opis,
        epilog=czytnik.użycie,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="+", help=f"{czytnik.sufiks} files or directories of them")
    parser.add_argument(
        "--into",
        metavar="DIR",
        required=True,
        help=f"where to write the prose, as {PROSE_SUFFIX} files mirroring the input tree",
    )
    parser.add_argument(
        "--polish",
        metavar="SHARE",
        type=float,
        default=0.0,
        help=f"leave out a {unit} whose words carry a Polish diacritic less often than this "
        f"(default: 0, which keeps every {unit})",
    )
    parser.add_argument(
        "--min-words",
        metavar="N",
        type=int,
        default=0,
        help=f"leave out a {unit} shorter than this, whose share of diacritics "
        "is too coarse to say which language it is in (default: 0)",
    )
    return parser


def _sources(paths: Sequence[str], suffix: str) -> Iterator[tuple[Path, Path]]:
    """Yield each source file with the path it keeps under the output directory.

    A directory is walked and its tree preserved; a named file arrives as itself,
    since the tree of a single file is its name.
    """
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for file in sorted(path.rglob(f"*{suffix}")):
                yield file.relative_to(path), file
        elif path.is_file():
            yield Path(path.name), path
