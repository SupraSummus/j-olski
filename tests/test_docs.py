"""The prose is checked the way the code is.

A renamed section leaves a live-looking link behind,
and nothing in a Markdown file fails when that happens,
so the review pass had to grep for it by hand.
Code names documents too — a docstring cites the section
that owns the decision it implements — and those rot the same way,
out of reach of a check that only reads Markdown.

The check commands are the same problem with something other than a name.
The block in ``CLAUDE.md`` is what a person runs,
the workflow's steps are what a push runs,
and nothing derives one from the other.

A document ``docs/README.md`` does not list is the same rot with nothing renamed:
it is on no reader's path, and adding one without listing it costs nothing.
Which path a document sits on is what ``docs/roles.md`` names.

A module named in prose rots the same way and used to rot unwatched.
Prose points at code because code owns what is implemented,
so a document naming a module is making a claim about where a fact lives,
and a renamed file leaves that claim looking live.
``docs/architecture.md`` is where the claims are densest,
its whole content being the map from a layer to the module that is one,
and the check that reads it found a deleted test file named in ``todo/``.

Wskazanie mówiące, w którą stronę przewijać, jest zdaniem o kolejności w pliku.
Sekcja przestawiona czyni je nieprawdą, a link rozwiązuje się dalej,
więc nic w Markdownie nie czerwienieje.
"""

import re
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS = (
    sorted(ROOT.glob("*.md"))
    + sorted((ROOT / "docs").rglob("*.md"))
    + sorted((ROOT / "todo").glob("*.md"))
)
#: Every module the repository holds, because a citation rots wherever it
#: stands: in the grammar, in the harness beside it, in a spike whose whole point
#: is a document, or in a test's docstring.
#: Plik danych stoi tu obok modułów, bo nagłówek wyprowadzony przez generator
#: cytuje sekcję tak samo jak docstring, a poza tą listą nie widzi go nic.
#: Skrypt w korzeniu stoi tu obok pakietów, bo cytuje dokument tak samo jak moduł
#: w środku: ``dokumentacja.py`` nazywa dokument, który jest właścicielem decyzji
#: o stronie, a ``README.py`` nazywa ten, który trzyma kryterium wyjścia.
SOURCES = sorted(
    [
        path
        for package in ("olski", "harness", "opowieści", "tests", "witryna")
        for wzorzec in ("*.py", "*.txt")
        for path in (ROOT / package).rglob(wzorzec)
    ]
    + list(ROOT.glob("*.py"))
)
WORKFLOW = ROOT / ".github" / "workflows" / "checks.yml"
RELATIVE_LINK = re.compile(r"\[[^\]]*\]\((?!\w+:)([^)\s]+)\)")
#: A module or data file named inside an inline code span, which is how prose
#: points at the code that owns a fact. Renaming the file leaves the span
#: looking live, exactly as a renamed section leaves a link looking live.
#: Strona witryny stoi tu obok modułów, bo dokument nazywa jej pliki tak samo,
#: a przeglądarka bierze je z tablicy tras i przemianowany daje 404.
#: Plik danych stojący w korzeniu, a nie w pakiecie: konfiguracja projektu leży
#: tam, bo mówi o projekcie, a nie o polszczyźnie (``olski/konfiguracja.py``).
#: Nazwany wprost, bo wzorzec na samą nazwę pliku łapałby każde `plik.toml`
#: z bloku polecenia. Skrypty w korzeniu stoją obok niego z tego samego powodu:
#: proza nazywa je tak jak moduł, a wzorzec na `*.py` bez katalogu łapałby
#: każdą nazwę pliku z polecenia.
#: Pakiet nazywa się ukośnikiem na końcu — `olski/subset/` — i zdanie o nim
#: rotuje tak samo jak zdanie o module, bo przemianowany katalog zostawia
#: żywo wyglądającą nazwę.
W_KORZENIU = r"olski\.toml|README\.py|dokumentacja\.py|mkdocs\.yml"
CITED_PATH = re.compile(
    r"`((?:olski|harness|tests|opowieści|próba|witryna)"
    r"/[\w./ąćęłńóśźżĄĆĘŁŃÓŚŹŻ-]+?(?:\.(?:py|txt|html|css|js)|/)"
    rf"|{W_KORZENIU})`"
)
#: The one document whose subject is code that is gone: it prices the retired
#: pack at the state it was retired in, and ``CLAUDE.md`` says nothing in it is
#: to be recomputed. A module name there is about that program, not about this
#: one, so it outlives the file the same way its figures do.
O_USUNIĘTYM = "firing-rates.md"
#: Rejestr otwartej roboty jest katalogiem, a nie plikiem, więc kod cytujący go
#: nazywa katalog; ``todo/README.md`` jest jego nagłówkiem i cytuje się tak samo.
#: Rejestr konstrukcji jest katalogiem wewnątrz ``docs/``, więc cytat z kodu
#: nazywa plik w nim: sam katalog nie mówi, która warstwa jest właścicielem.
CITED_DOCUMENT = re.compile(
    r"(?:docs/[\w-]+(?:/[\w-]+)?|CLAUDE)\.md(?:#[\w-]+)?|todo/(?:README\.md)?"
)
#: An entry in the docs register's list of documents, which is the only place
#: that puts a document on somebody's path. Rejestr konstrukcji jest katalogiem,
#: więc wchodzi na tę listę tak jak dokument, a wiersz nazywa katalog:
#: bez tego rejestr zszedłby ze ścieżki czytelnika i nic by nie czerwieniało.
#: Wiersz nazywa plik bez katalogu, bo spis stoi w tym samym katalogu co on.
LISTED_DOCUMENT = re.compile(r"(?m)^- \[([\w-]+\.md|[\w-]+/)\]")
HEADING = re.compile(r"(?m)^#+\s+(.*)$")
#: Słowo, którym wskazanie mówi, w którą stronę przewijać. Kierunek jest
#: własnością pary — wskazania i celu — a nie samego linku.
W_DÓŁ = frozenset({"below", "niżej", "poniżej"})
W_GÓRĘ = frozenset({"above", "wyżej", "powyżej"})
DEIKTYCZNE = re.compile(rf"\[({'|'.join(sorted(W_DÓŁ | W_GÓRĘ))})\]\(#([\w-]+)\)")
LISTED_CHECKS = re.compile(r"(?ms)^## Checks\n.*?^```sh\n(.*?)^```")
WORKFLOW_STEP = re.compile(r"(?m)^\s*- run: (.*)$")


def anchor_of(heading: str) -> str:
    """Slug a heading as GitHub does for ordinary headings: fold case, drop punctuation.

    Odstęp idzie na kreskę pojedynczo, a nie ciągiem, bo tak robi `github-slugger`:
    znak interpunkcyjny odpada razem ze sobą, a odstępy po obu jego stronach zostają
    i dają dwie kreski. Zwijanie ciągu przepuszczało link, który na GitHubie jest martwy.
    """
    return re.sub(r"[^\w\s-]", "", heading.strip().lower()).replace(" ", "-")


def assert_resolves(destination: Path, anchor: str, origin: str) -> None:
    assert destination.exists(), f"{origin} names a document that is not there"
    if anchor:
        headings = HEADING.findall(destination.read_text())
        assert anchor in {anchor_of(heading) for heading in headings}, (
            f"{origin} names #{anchor}, which no heading in {destination.name} makes"
        )


def relative_links():
    return [
        pytest.param(document, link.group(1), id=f"{document.name} -> {link.group(1)}")
        for document in DOCUMENTS
        for link in RELATIVE_LINK.finditer(document.read_text())
    ]


def cited_documents():
    return [
        pytest.param(source, citation.group(0), id=f"{source.name} -> {citation.group(0)}")
        for source in SOURCES
        for citation in CITED_DOCUMENT.finditer(source.read_text())
    ]


def cited_paths():
    return [
        pytest.param(document, cited.group(1), id=f"{document.name} -> {cited.group(1)}")
        for document in DOCUMENTS
        if document.name != O_USUNIĘTYM
        for cited in CITED_PATH.finditer(document.read_text())
    ]


def wskazania_deiktyczne():
    parametry = []
    for document in DOCUMENTS:
        proza = document.read_text()
        nagłówki = {anchor_of(m.group(1)): m.start() for m in HEADING.finditer(proza)}
        for wskazanie in DEIKTYCZNE.finditer(proza):
            # Kotwicy, której nie ma, pilnuje test wskazań względnych obok.
            if wskazanie.group(2) not in nagłówki:
                continue
            wiersz = proza.count("\n", 0, wskazanie.start()) + 1
            parametry.append(
                pytest.param(
                    wskazanie.group(1),
                    wskazanie.start() < nagłówki[wskazanie.group(2)],
                    id=f"{document.name}:{wiersz} -> {wskazanie.group(2)}",
                )
            )
    return parametry


@pytest.mark.parametrize(("słowo", "cel_niżej"), wskazania_deiktyczne())
def test_słowo_kierunkowe_zgadza_się_z_tym_gdzie_stoi_cel(słowo: str, cel_niżej: bool):
    assert (słowo in W_DÓŁ) == cel_niżej, (
        f"wskazanie mówi {słowo}, a cel stoi {'niżej' if cel_niżej else 'wyżej'}"
    )


@pytest.mark.parametrize(("document", "target"), cited_paths())
def test_every_module_named_in_prose_is_there(document: Path, target: str):
    assert (ROOT / target).exists(), f"{document.name} names {target}, which is not there"


@pytest.mark.parametrize(("document", "target"), relative_links())
def test_every_relative_link_resolves(document: Path, target: str):
    path, _, anchor = target.partition("#")
    assert_resolves(document.parent / path if path else document, anchor, document.name)


@pytest.mark.parametrize(("source", "target"), cited_documents())
def test_every_document_cited_from_code_resolves(source: Path, target: str):
    path, _, anchor = target.partition("#")
    assert_resolves(ROOT / path, anchor, source.name)


def test_every_document_is_listed_in_the_docs_register():
    register = ROOT / "docs" / "README.md"
    listed = set(LISTED_DOCUMENT.findall(register.read_text()))
    documents = {path.name for path in (ROOT / "docs").glob("*.md")} - {register.name}
    registers = {f"{path.name}/" for path in (ROOT / "docs").iterdir() if path.is_dir()}
    assert documents | registers == listed


def test_the_checks_a_person_runs_are_the_checks_a_push_runs():
    listed = LISTED_CHECKS.search((ROOT / "CLAUDE.md").read_text())
    assert listed, "CLAUDE.md has no Checks section carrying a shell block"
    assert listed.group(1).splitlines() == WORKFLOW_STEP.findall(WORKFLOW.read_text())


def test_every_path_in_reuse_toml_matches_a_file():
    """Ścieżka wyjątku jest nazwą prywatną i rusza ją przemianowanie pliku.

    ``reuse lint`` pyta o pokrycie, więc plik, do którego wyjątek przestał trafiać,
    bierze po cichu licencję domyślną, czyli cudze dane wychodzą wtedy na MIT.
    """
    with (ROOT / "REUSE.toml").open("rb") as plik:
        annotations = tomllib.load(plik)["annotations"]
    declared = [
        path
        for entry in annotations
        for path in ([entry["path"]] if isinstance(entry["path"], str) else entry["path"])
    ]
    assert [path for path in declared if not any(ROOT.glob(path))] == []
