"""Składa stronę dokumentów: prozę repozytorium i referencję API z docstringów.

Jedno polecenie, ``python3 -m dokumentacja``, robi to samo, co robi
``.github/workflows/dokumentacja.yml``, więc workflow nie niesie drugiego przepisu.
Czemu strona nie stoi na domyślnym Jekyllu, co sprawdza jej budowanie
i ile kosztuje referencja API, mówi docs/publikacja.md.
"""

from __future__ import annotations

import pkgutil
import re
import shutil
import subprocess
import sys
from pathlib import Path

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
#: Strona, z której czytelnik wchodzi do referencji, i jedyne miejsce, które ją
#: linkuje: pdoc wypisuje drzewo HTML, o którym mkdocs nie wie nic poza tym, że
#: je przenosi.
REFERENCJA = """# Referencja API

Strony pod tym adresem wypisuje pdoc z docstringów pakietu `olski`,
więc mówią to, co mówi kod w chwili budowania.
Dokumenty obok mówią to, czego kod nie pokaże:
cenę, granicę podzbioru i alternatywę odrzuconą
([docs/publikacja.md](docs/publikacja.md)).

[Wejście do referencji](api/index.html)
"""


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


def moduły() -> list[str]:
    """Wylicza moduły pakietu, bo pdoc nie schodzi do tych, których `__all__` nie wylicza.

    Warstwa jest jedna: podpakiet `__all__` nie deklaruje, więc pdoc schodzi do jego
    modułów sam, a nazwa wypisana tu drugi raz mówi mu o dwóch modułach o jednej nazwie.
    """
    import olski

    return ["olski", *(m.name for m in pkgutil.iter_modules(olski.__path__, "olski."))]


def wypisz_referencję() -> None:
    """Puszcza pdoc do katalogu, który mkdocs przenosi na stronę bez zmian."""
    subprocess.run(
        [sys.executable, "-m", "pdoc", "--output-directory", str(ŹRÓDŁO / "api"), *moduły()],
        check=True,
    )
    (ŹRÓDŁO / "referencja.md").write_text(REFERENCJA, encoding="utf-8")


def zbuduj() -> None:
    """Puszcza mkdocs. `--strict` czyni ostrzeżenie błędem, więc martwy link wywraca przebieg."""
    subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict"], check=True, cwd=KORZEŃ)


def main() -> None:
    zbierz_prozę()
    dołóż_cele_linków()
    wpisz_adres()
    wypisz_referencję()
    zbuduj()


if __name__ == "__main__":
    main()
