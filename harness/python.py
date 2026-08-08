"""Python in, Polish prose out.

Repozytorium pisze o sobie nie tylko w dokumentach: docstring i komentarz też są
prozą, którą CLAUDE.md obejmuje tymi samymi regułami, a przybywa jej przy każdej
zmianie w kodzie, bo nazwy i komentarze bierzemy po polsku. Żądanie, żeby ten
tekst nie potykał się o to, co jego własne narzędzie wytyka, jest nad dokumentem
checkiem, bo `harness/markdown.py` wyjmuje z dokumentu prozę; nad modułem
sprowadza je do checka ten krok.

Dwie decyzje przechodzą przez cały moduł i warto je powiedzieć raz.

**Jednostką jest docstring albo blok komentarza, a nie plik.** Moduł miesza
polszczyznę z angielszczyzną z założenia: słowa kluczowe, klucze i API bibliotek
zostają po angielsku, a sekcja pisana wcześniej zostaje taka, jaka jest, bo
regułę językową przyjmujemy leniwie. Próg liczony nad całym plikiem nie ma więc
nad czym stanąć i liczy się go nad jednostką.

**Wiersze akapitu sklejają się w jeden, tak jak w Markdownie.** Powód jest tu
inny: pliku źródłowego nikt nie składa, więc łamanie wiersza w komentarzu jest
albo zawijaniem na kolumnie, albo łamaniem semantycznym, a żadne z nich nie jest
tym łamaniem, o które pytają reguły czytające koniec wiersza. Zostawione
mówiłyby autorowi, żeby wstawił w kod twardą spację.

Rachunek z tego, co ten krok zmyśla, wraz z poleceniem, którym się go odtwarza,
trzyma docs/prose-in-code.md; to, co jest w nim wspólne z krokiem nad
Markdownem, trzyma docs/extraction.md.
"""

from __future__ import annotations

import ast
import io
import re
import textwrap
import tokenize
from collections.abc import Iterator, Sequence

from harness import BULLET, Czytnik, Jednostka, uruchom

PYTHON_SUFFIX = ".py"

#: Znak komentarza wraz z dwukropkiem, którym Sphinx dokumentuje stałą. Spacja
#: po nim zostaje, bo jest wcięciem, a wcięcie bloku zdejmuje się całe naraz:
#: to repozytorium pisze narrację w komentarzu od dwóch spacji, a zdjęta po
#: jednej reszta czytałaby się jak przykład i przepadła.
MARKER = re.compile(r"#:?")

#: Znaczniki reST, jednym przejściem, tak samo jak w Markdownie: konstrukcja
#: zostawia po sobie tekst, który obejmowała, a odstęp przed nią zabiera ze sobą
#: tylko wtedy, gdy nie ma czego zostawić. Rola Sphinksa niesie nazwę, którą
#: czytelnik widzi, więc wychodzi z niej ta nazwa, a nie sama rola. Wyróżnienia
#: jedną gwiazdką tu nie ma, bo w docstringu gwiazdka częściej otwiera *args
#: niż wyróżnienie, a ogon wyróżnienia dwiema jest leniwy, żeby dwa krótkie
#: wyróżnienia w akapicie wyszły jako dwa.
INLINE = re.compile(
    r"""
    (?P<space>[ \t]*)
    (?:
        :\w+:`(?P<rola>[^`]*)`
      | ``(?P<dosłownie>[^`]*)``
      | `(?P<kod>[^`]*)`
      | \*\*(?P<mocno>\S(?:.*?\S)??)\*\*
    )
    """,
    re.VERBOSE,
)

INLINE_GROUPS = ("rola", "dosłownie", "kod", "mocno")

#: Podwojony dwukropek, którym reST zapowiada przykład. Przykład ekstrakcja
#: wyrzuca, a zapowiedź zostaje i renderuje się jako jeden dwukropek, więc
#: zostawiona parą trafia do reguł jako dwukropek bez spacji po nim, czyli jako
#: znalezisko, którego nikt nie napisał. Ze spacją przed sobą znika razem z nią.
ZAPOWIEDŹ = re.compile(r"(?P<space>[ \t]*)::\Z")

#: Węzły, które niosą docstring. Instrukcji przypisania to nie obejmuje: łańcuch
#: pod stałą jest docstringiem dla Sphinksa i zwykłym wyrażeniem dla Pythona,
#: a to repozytorium dokumentuje stałe komentarzem z dwukropkiem.
DOCUMENTED = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)


def prose(source: str) -> str:
    """Zwraca prozę modułu, akapit w wierszu, w kolejności, w jakiej stoi w pliku.

    Puste wiersze rozdzielają akapity, tak jak po drugiej stronie, więc zdanie
    nie przechodzi z jednego docstringa w następny.
    """
    body = "\n\n".join(jednostka.tekst for jednostka in jednostki(source))
    return body + "\n" if body else ""


def jednostki(source: str) -> list[Jednostka]:
    """Każdy docstring i każdy blok komentarza, po kolei, puste pominięte."""
    znalezione = [*_docstringi(source), *_komentarze(source)]
    return sorted((j for j in znalezione if j.tekst), key=lambda j: j.wiersz)


def _docstringi(source: str) -> Iterator[Jednostka]:
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, DOCUMENTED) and (docstring := ast.get_docstring(node, clean=True)):
            yield Jednostka(node.body[0].lineno, _akapity(docstring.splitlines()))


def _komentarze(source: str) -> Iterator[Jednostka]:
    """Blok komentarza, czyli tyle sąsiadujących wierszy, ile czyta się naraz.

    Blok przerywa wiersz kodu między komentarzami i komentarz dopisany na końcu
    wiersza kodu, bo taki mówi o tym wierszu i nie ciągnie zdania z góry.
    """
    blok: list[str] = []
    początek, ostatni = 0, None
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.COMMENT:
            continue
        numer, sam = token.start[0], not token.line[: token.start[1]].strip()
        if blok and (ostatni is None or numer != ostatni + 1 or not sam):
            yield Jednostka(początek, _akapity(_bez_wcięcia(blok)))
            blok = []
        początek = początek if blok else numer
        blok.append(MARKER.sub("", token.string, count=1))
        ostatni = numer if sam else None
    if blok:
        yield Jednostka(początek, _akapity(_bez_wcięcia(blok)))


def _bez_wcięcia(blok: Sequence[str]) -> list[str]:
    """Zdejmuje z bloku wcięcie, które ma każdy jego wiersz.

    Docstringowi robi to ast, a komentarzowi nie ma kto, bo wcięcie zaczyna się
    dopiero za znakiem komentarza. Zdjęte całe naraz zostawia to, co jeden
    wiersz ma ponad resztę, czyli pozycję listy i przykład.
    """
    return textwrap.dedent("\n".join(blok)).splitlines()


def _akapity(wiersze: Sequence[str]) -> str:
    """Skleja wiersze każdego akapitu, przykłady po drodze wyrzucone.

    Przykładem jest blok, który zaczyna się od wcięcia: polecenie powłoki pod
    dwukropkiem albo kawałek kodu, czyli to, czym w Markdownie jest blok
    ogrodzony. Wcięcie w środku akapitu jest czym innym, bo pozycja listy ciągnie
    się nim dalej, i zostaje.
    """
    bloki: list[list[str]] = [[]]
    przykład = False
    for wiersz in wiersze:
        if not wiersz.strip():
            bloki.append([])
            przykład = False
        elif wiersz[:1] in " \t" and (przykład or not bloki[-1]):
            przykład = True
        else:
            if przykład:
                bloki.append([])
                przykład = False
            if pozycja := BULLET.match(wiersz):
                bloki.append([wiersz[pozycja.end() :].strip()])
            else:
                bloki[-1].append(wiersz.strip())
    akapity = (_bez_zapowiedzi(_inline(" ".join(blok)).strip()) for blok in bloki if blok)
    return "\n\n".join(akapit for akapit in akapity if akapit)


def _bez_zapowiedzi(akapit: str) -> str:
    return ZAPOWIEDŹ.sub(lambda match: "" if match.group("space") else ":", akapit)


def _inline(text: str) -> str:
    return INLINE.sub(_zastąp, text)


def _zastąp(match: re.Match) -> str:
    """To samo, co `_replace` w `harness/markdown.py`, i z tego samego powodu."""
    for name in INLINE_GROUPS:
        inner = match.group(name)
        if inner is None:
            continue
        return (match.group("space") + inner) if inner else ""
    raise AssertionError(f"INLINE matched {match.group()!r} with no group")


# --------------------------------------------------------------------------- #
# The command line
# --------------------------------------------------------------------------- #

USAGE = """
  python3 -m harness.python olski/ --into prose/            a package
  python3 -m harness.python olski/rules.py --into prose/    one module
"""


CZYTNIK = Czytnik(
    komenda="harness.python",
    sufiks=PYTHON_SUFFIX,
    nazwa_jednostki="comment or docstring",
    opis="Extract Polish prose from Python comments and docstrings.",
    użycie=USAGE,
    jednostki=jednostki,
)


def main(argv: Sequence[str] | None = None) -> int:
    return uruchom(argv, CZYTNIK)


if __name__ == "__main__":
    raise SystemExit(main())
