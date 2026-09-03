"""Moduł wchodzi, polska proza wychodzi.

Repozytorium pisze o sobie nie tylko w dokumentach: docstring i blok komentarza
są prozą, którą CLAUDE.md obejmuje tymi samymi regułami, a przybywa jej przy
każdej zmianie w kodzie, bo prozę i nazwy bierzemy po polsku. Nad dokumentem
sprowadza tę prozę pod ``olski-check`` ``olski/markdown.py``; nad modułem
sprowadza ją ten krok, więc ``olski-check olski/parse/las.py`` mówi o docstringu
to samo, co o akapicie dokumentu.

Dwie decyzje przechodzą przez cały moduł i warto je powiedzieć raz.

**Jednostką jest docstring albo blok komentarza, a nie plik.** Moduł miesza
polszczyznę z angielszczyzną z założenia: słowa kluczowe, klucze i API bibliotek
zostają po angielsku, a sekcja napisana wcześniej zostaje taka, jaka jest, bo
regułę językową przyjmujemy leniwie. Udział diakrytyków liczony nad całym
plikiem nie ma więc nad czym stanąć i liczy się go nad jednostką
(``polish_share`` w ``harness/__init__.py``).

**Wiersze akapitu sklejają się w jeden, tak jak w Markdownie.** Powód jest tu
inny: pliku źródłowego nikt nie składa, więc złamanie wiersza w komentarzu jest
albo zawijaniem na kolumnie, albo łamaniem semantycznym, a żadne z nich nie jest
tym, co czytelnik widzi jako koniec wiersza.

Znaczniki reST czyta tu wzorzec, a nie parser, i tym ten krok różni się od tego
nad Markdownem. Cenę tej różnicy trzyma docs/extraction.md, razem z rachunkiem z
tego, co jeden i drugi po drodze zmyśla.
"""

from __future__ import annotations

import ast
import io
import re
import textwrap
import tokenize
from collections.abc import Iterator, Sequence

PYTHON_SUFFIX = ".py"

#: Znak pozycji listy, punktowanej albo numerowanej. Każda pozycja jest osobnym
#: akapitem, bo zdanie nie biegnie z jednej do następnej.
POZYCJA = re.compile(r"[ \t]*(?:[-*+]|\d{1,9}[.)])[ \t]+")

#: Znak komentarza wraz z dwukropkiem, którym Sphinx dokumentuje stałą. Spacja
#: po nim zostaje, bo jest wcięciem, a wcięcie bloku zdejmuje się całe naraz:
#: narrację w komentarzu pisze to repozytorium od dwóch spacji, a zdjęta po
#: jednej reszta czytałaby się jak przykład i przepadła.
ZNACZNIK = re.compile(r"#:?")

#: Znaczniki reST w wierszu, jednym przejściem: konstrukcja zostawia po sobie
#: tekst, który obejmowała, a odstęp przed nią zabiera ze sobą tylko wtedy, gdy
#: nie ma czego zostawić. Rola Sphinksa niesie nazwę, którą czytelnik widzi,
#: więc wychodzi z niej ta nazwa, a nie sama rola. Wyróżnienia jedną gwiazdką tu
#: nie ma, bo w docstringu gwiazdka częściej otwiera ``*args`` niż wyróżnienie, a
#: ogon wyróżnienia dwiema jest leniwy, żeby dwa krótkie wyróżnienia w akapicie
#: wyszły jako dwa.
WSTAWKI = re.compile(
    r"""
    (?P<odstęp>[ \t]*)
    (?:
        :\w+:`(?P<rola>[^`]*)`
      | ``(?P<dosłownie>[^`]*)``
      | `(?P<kod>[^`]*)`
      | \*\*(?P<mocno>\S(?:.*?\S)??)\*\*
    )
    """,
    re.VERBOSE,
)

GRUPY_WSTAWEK = ("rola", "dosłownie", "kod", "mocno")

#: Podwojony dwukropek, którym reST zapowiada przykład. Przykład ekstrakcja
#: wyrzuca, a zapowiedź zostaje i renderuje się jako jeden dwukropek, więc
#: zostawiona parą dochodzi do gramatyki jako dwukropek bez spacji po nim, czyli
#: jako znak, którego nikt nie napisał. Ze spacją przed sobą znika razem z nią.
ZAPOWIEDŹ = re.compile(r"(?P<odstęp>[ \t]*)::\Z")

#: Węzły, które niosą docstring. Instrukcji przypisania to nie obejmuje: łańcuch
#: pod stałą jest docstringiem dla Sphinksa i zwykłym wyrażeniem dla Pythona, a
#: to repozytorium dokumentuje stałą komentarzem z dwukropkiem.
DOKUMENTOWANE = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)


def proza(źródło: str) -> str:
    """Proza modułu, akapit w wierszu, w kolejności, w jakiej stoi w pliku.

    Puste wiersze rozdzielają akapity, tak jak po drugiej stronie
    (:func:`olski.markdown.prose`), więc zdanie nie przechodzi z jednego
    docstringa w następny.
    """
    ciało = "\n\n".join(tekst for _, tekst in jednostki(źródło))
    return ciało + "\n" if ciało else ""


def jednostki(źródło: str) -> list[tuple[int, str]]:
    """Każdy docstring i każdy blok komentarza, po kolei, puste pominięte.

    Wiersz idzie przed prozą, bo po ekstrakcji nie ma z czego go odtworzyć: w
    prozie modułu nie ma już kodu, który stał między jedną jednostką a drugą.
    Pytający robi z tej pary jednostkę wyboru po języku
    (:class:`harness.Jednostka`), a wybór ten należy do harnessu, bo waży go ten,
    kto składa korpus, a nie ten, kto sprawdza swój plik.
    """
    znalezione = [*_docstringi(źródło), *_komentarze(źródło)]
    return sorted(((wiersz, tekst) for wiersz, tekst in znalezione if tekst), key=lambda j: j[0])


def _docstringi(źródło: str) -> Iterator[tuple[int, str]]:
    for węzeł in ast.walk(ast.parse(źródło)):
        if isinstance(węzeł, DOKUMENTOWANE) and (
            docstring := ast.get_docstring(węzeł, clean=True)
        ):
            yield węzeł.body[0].lineno, _akapity(docstring.splitlines())


def _komentarze(źródło: str) -> Iterator[tuple[int, str]]:
    """Blok komentarza, czyli tyle sąsiadujących wierszy, ile czyta się naraz.

    Blok przerywa wiersz kodu między komentarzami i komentarz dopisany na końcu
    wiersza kodu, bo taki mówi o tym wierszu i nie ciągnie zdania z góry.
    """
    blok: list[str] = []
    początek, ostatni = 0, None
    for token in tokenize.generate_tokens(io.StringIO(źródło).readline):
        if token.type != tokenize.COMMENT:
            continue
        numer, sam = token.start[0], not token.line[: token.start[1]].strip()
        if blok and (ostatni is None or numer != ostatni + 1 or not sam):
            yield początek, _akapity(_bez_wcięcia(blok))
            blok = []
        początek = początek if blok else numer
        blok.append(ZNACZNIK.sub("", token.string, count=1))
        ostatni = numer if sam else None
    if blok:
        yield początek, _akapity(_bez_wcięcia(blok))


def _bez_wcięcia(blok: Sequence[str]) -> list[str]:
    """Zdejmuje z bloku wcięcie, które ma każdy jego wiersz.

    Docstringowi robi to ``ast``, a komentarzowi nie ma kto, bo wcięcie zaczyna
    się dopiero za znakiem komentarza. Zdjęte całe naraz zostawia to, co jeden
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
            if pozycja := POZYCJA.match(wiersz):
                bloki.append([wiersz[pozycja.end() :].strip()])
            else:
                bloki[-1].append(wiersz.strip())
    akapity = (_bez_zapowiedzi(_wstawki(" ".join(blok)).strip()) for blok in bloki if blok)
    return "\n\n".join(akapit for akapit in akapity if akapit)


def _bez_zapowiedzi(akapit: str) -> str:
    return ZAPOWIEDŹ.sub(lambda trafienie: "" if trafienie.group("odstęp") else ":", akapit)


def _wstawki(tekst: str) -> str:
    return WSTAWKI.sub(_zastąp, tekst)


def _zastąp(trafienie: re.Match) -> str:
    """To samo, co robi ``_inline`` w ``olski/markdown.py``, i z tego samego powodu.

    Konstrukcja zostawia po sobie tekst, który obejmowała, a taka, po której nic
    nie zostaje, zabiera ze sobą odstęp stojący przed nią: kasowanie, które ten
    odstęp zostawia, dochodzi do gramatyki jako znak, którego nikt nie wpisał.
    """
    for nazwa in GRUPY_WSTAWEK:
        wnętrze = trafienie.group(nazwa)
        if wnętrze is None:
            continue
        return (trafienie.group("odstęp") + wnętrze) if wnętrze else ""
    raise AssertionError(f"WSTAWKI dopasowały {trafienie.group()!r} i żadnej grupy")
