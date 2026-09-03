"""Składa stronę dokumentów: prozę repozytorium i referencję API z docstringów.

Jedno polecenie, ``python3 -m dokumentacja``, robi to samo, co robi
``.github/workflows/dokumentacja.yml``, więc workflow nie niesie drugiego przepisu.
Czemu strona nie stoi na domyślnym Jekyllu, co sprawdza jej budowanie
i czemu referencja idzie przez mkdocs, a nie obok niego, mówi docs/publikacja.md.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from collections.abc import Iterator
from functools import partial
from pathlib import Path

import griffe

KORZEŃ = Path(__file__).resolve().parent
KONFIGURACJA = KORZEŃ / "mkdocs.yml"
#: Katalog, z którego buduje mkdocs. Jest wynikiem przebiegu, więc stoi
#: w `.gitignore`, a katalog strony deklaruje `mkdocs.yml` i to on go wypisuje.
ŹRÓDŁO = KORZEŃ / "_dokumentacja"
#: Adres własny wychodzi z `site_url` w `mkdocs.yml`, bo GitHub Pages żąda go
#: dwa razy: raz w konfiguracji strony, a raz plikiem `CNAME` w tym, co jedzie
#: na serwer. Wdrożenie bez tego pliku zdejmuje adres własny z ustawień.
SITE_URL = re.compile(r"(?m)^site_url:\s*https://([^/\s]+)")
#: Proza w układzie katalogów z repozytorium. Układ jest tu treścią, a nie
#: wygodą: `../CLAUDE.md` z `docs/` rozwiązuje się tylko wtedy, gdy korzeniem
#: strony jest korzeń repozytorium.
PROZA = ("README.md", "CLAUDE.md", "docs", "todo")
#: Link względny bez kotwicy. Kotwica odpada tutaj, bo pytamy o plik do skopiowania.
LINK = re.compile(r"\[[^\]]*\]\((?!\w+:)([^)\s#]+)")
#: Katalog referencji jest jej adresem: wejście wychodzi pod `/referencja/`,
#: a każdy moduł pod `/referencja/<nazwa modułu>/`.
REFERENCJA = "referencja"
#: Strona wejściowa referencji. Spisu modułów nie ma tu ręką: wypisuje go
#: mkdocstrings z pakietu, więc moduł dopisany jutro sam do niego wchodzi.
WEJŚCIE = """# Referencja API

Strony niżej wypisuje mkdocstrings z docstringów pakietu `olski`,
więc mówią to, co mówi kod w chwili budowania.
Dokumenty obok mówią to, czego kod nie pokaże:
cenę, granicę podzbioru i alternatywę odrzuconą
([docs/publikacja.md](../docs/publikacja.md)).

::: olski
    options:
      summary:
        modules: true
"""
#: Strona modułu. Nagłówek stoi w niej wprost, bo z niego bierze mkdocs
#: podpis w nawigacji i w wyszukiwarce.
STRONA_MODUŁU = """# {moduł}

::: {moduł}
"""
#: Rola reStructuredText, którą docstringi pakietu cytują symbol.
ROLA = re.compile(r":(?:attr|class|const|data|exc|func|meth|mod|obj):`([^`]+)`")
#: Nazwa prywatna, czyli taka, której mkdocstrings nie wypisuje. Dunder przechodzi,
#: bo domyślny filtr handlera odrzuca sam pojedynczy podkreślnik.
PRYWATNA = re.compile(r"^_[^_]")


class Odsyłacze(griffe.Extension):
    """Zamienia rolę reStructuredText na odsyłacz mkdocstrings, gdy cel jest na stronie.

    Docstringi pakietu cytują symbol rolą reStructuredText,
    bo czyta się je przede wszystkim w edytorze i w ``help()``,
    gdzie ta konwencja jest krótsza od linku i niesie ścieżkę raz.
    mkdocstrings zna tylko ``[cel][]``, więc przekład stoi tutaj:
    inaczej płaciłby za stronę każdy docstring pakietu.

    Rola z celem, którego na stronie nie ma — nazwą prywatną albo modułem spoza
    pakietu — schodzi do samego napisu w backtickach, tak jak wypisywał ją pdoc.
    Link do celu, którego nie ma, byłby błędem `--strict`, a rola nietknięta
    trafiłaby na stronę jako `:func:` z napisem obok.
    """

    def on_package(self, *, pkg: griffe.Module, **_) -> None:
        wszystkie = list(obiekty(pkg))
        strony = {
            obiekt.path
            for obiekt in wszystkie
            if not any(PRYWATNA.match(człon) for człon in obiekt.path.split("."))
        }
        for obiekt in wszystkie:
            if obiekt.docstring:
                obiekt.docstring.value = ROLA.sub(
                    partial(odsyłacz, obiekt=obiekt, strony=strony), obiekt.docstring.value
                )


def obiekty(obiekt: griffe.Object) -> Iterator[griffe.Object]:
    """Wylicza obiekt i wszystko, co pod nim zadeklarowano.

    Alias jest nazwą zaimportowaną, a nie deklaracją:
    bez tego warunku symbol wychodziłby stąd tyle razy, ile modułów go bierze,
    a ``import re`` w module wciągnąłby tu bibliotekę standardową.
    """
    yield obiekt
    for pod in obiekt.members.values():
        if not pod.is_alias:
            yield from obiekty(pod)


def odsyłacz(rola: re.Match, obiekt: griffe.Object, strony: set[str]) -> str:
    """Składa odsyłacz do celu roli, rozwiązując nazwę tak, jak rozwiązuje ją Python.

    Rola cytuje symbol nazwą z zasięgu, w którym docstring stoi — samą ``Las``,
    a nie całą ścieżką — a nazwa ta bywa zaimportowana.
    Szuka jej więc od obiektu w górę i schodzi aliasem do miejsca deklaracji,
    bo tam, a nie u importującego, wypisuje symbol mkdocstrings.
    """
    cel = rola.group(1)
    if cel in strony:
        return f"[`{cel}`][{cel}]"
    głowa, _, reszta = cel.partition(".")
    for zasięg in rodzice(obiekt):
        if głowa in zasięg.members:
            pełna = ".".join(filter(None, (zasięg.members[głowa].canonical_path, reszta)))
            return f"[`{cel}`][{pełna}]" if pełna in strony else f"`{cel}`"
    return f"`{cel}`"


def rodzice(obiekt: griffe.Object) -> Iterator[griffe.Object]:
    """Wylicza obiekt i jego przodków, od najbliższego."""
    while obiekt is not None:
        yield obiekt
        obiekt = obiekt.parent


def zbierz_prozę() -> None:
    """Kopiuje prozę do katalogu, z którego buduje mkdocs."""
    shutil.rmtree(ŹRÓDŁO, ignore_errors=True)
    ŹRÓDŁO.mkdir()
    for nazwa in PROZA:
        skąd = KORZEŃ / nazwa
        dokąd = ŹRÓDŁO / nazwa
        if skąd.is_dir():
            shutil.copytree(skąd, dokąd)
        else:
            shutil.copy2(skąd, dokąd)


def dołóż_cele_linków() -> None:
    """Dokłada pliki spoza prozy, na które proza wskazuje linkiem.

    Proza linkuje do modułu, do `pyproject.toml` i do workflowu,
    a link do pliku, którego na stronie nie ma, wywraca budowanie.
    Właścicielem tej listy jest sama proza:
    wypisana tutaj rozjeżdżałaby się z nią po cichu.
    """
    for dokument in sorted(ŹRÓDŁO.rglob("*.md")):
        for link in LINK.finditer(dokument.read_text(encoding="utf-8")):
            cel = (dokument.parent / link.group(1)).resolve()
            if cel.suffix == ".md" or not cel.is_relative_to(ŹRÓDŁO) or cel.exists():
                continue
            oryginał = KORZEŃ / cel.relative_to(ŹRÓDŁO)
            if oryginał.is_file():
                cel.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(oryginał, cel)


def wpisz_adres() -> None:
    """Wypisuje `CNAME` z adresu, który deklaruje `mkdocs.yml`."""
    adres = SITE_URL.search(KONFIGURACJA.read_text(encoding="utf-8"))
    assert adres, "mkdocs.yml nie deklaruje site_url, więc adres własny nie ma skąd wyjść"
    (ŹRÓDŁO / "CNAME").write_text(f"{adres.group(1)}\n", encoding="utf-8")


def moduły(pakiet: griffe.Module) -> Iterator[str]:
    """Wylicza moduły pod pakietem, bo strona powstaje na moduł.

    Podpakiet schodzi tędy tak samo jak moduł, więc `olski.skład.składnia` ma
    swoją stronę, a odsyłacz do symbolu z niego ma dokąd prowadzić.
    """
    for pod in pakiet.modules.values():
        yield pod.path
        yield from moduły(pod)


def wypisz_referencję(pakiet: griffe.Module) -> None:
    """Wypisuje stronę na moduł, żeby mkdocs objął referencję nawigacją i wyszukiwarką."""
    katalog = ŹRÓDŁO / REFERENCJA
    katalog.mkdir()
    (katalog / "index.md").write_text(WEJŚCIE, encoding="utf-8")
    for moduł in sorted(moduły(pakiet)):
        (katalog / f"{moduł}.md").write_text(STRONA_MODUŁU.format(moduł=moduł), encoding="utf-8")


def sprawdź_przekład(pakiet: griffe.Module) -> None:
    """Żąda, żeby żadna rola nie wyszła na stronę napisem.

    Rola, która została w docstringu, znaczy, że griffe nie zawołał `Odsyłaczy`,
    bo hak zmienił nazwę między wydaniami — i awaria jest wtedy cicha:
    strona buduje się zielono i wypisuje `:func:` w środku zdania.
    """
    zostały = [o.path for o in obiekty(pakiet) if o.docstring and ROLA.search(o.docstring.value)]
    assert not zostały, f"rola została w docstringu, więc przekładu nie było: {zostały}"


def zbuduj() -> None:
    """Puszcza mkdocs. `--strict` czyni ostrzeżenie błędem, więc martwy link wywraca przebieg."""
    subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict"], check=True, cwd=KORZEŃ)


def main() -> None:
    zbierz_prozę()
    dołóż_cele_linków()
    wpisz_adres()
    #  Pakiet czyta się tu raz i tym samym rozszerzeniem, którym czyta go
    #  mkdocstrings przy budowaniu, żeby żądanie niżej mierzyło to, co wyjdzie
    #  na stronę. Importu nie ma: griffe czyta źródło, a import żądałby Morfeusza.
    pakiet = griffe.load(
        "olski",
        search_paths=[str(KORZEŃ)],
        extensions=griffe.load_extensions(Odsyłacze),
    )
    wypisz_referencję(pakiet)
    sprawdź_przekład(pakiet)
    zbuduj()


if __name__ == "__main__":
    main()
