"""Ile kupuje i ile kosztuje negacja, zmierzone nad Składnicą.

Negacja jest w olskim dwiema rzeczami naraz i dlatego ma sondę. Cząstka ``nie``
dochodzi przed formę czasownika, a dopełniacz negacji zmienia przypadek
dopełnienia, którego czasownik żąda, i sięga po nie ponad bezokolicznikiem, przy
którym cząstki nie ma. Pytanie brzmi, ile zdań każda z tych dwóch odbiera:
dopełniacz negacji stawia w pozycji dopełnienia ten sam przypadek, w którym stoi
przydawka dopełniaczowa, więc zdanie, w którym obie mają gdzie stanąć, wychodzi
dwoma czytaniami, a takie zdanie olski odrzuca. Sumy z ``olski-corpus`` na to nie
odpowiadają, bo przejście ``przyjęte → wieloznaczne`` widać dopiero zdanie po
zdaniu.

Wariant, który zostawia sam dopełniacz, mierzy przy tym, czy te dwie rzeczy są
jedną: dopełniacza negacji nie licencjonuje nic poza czasownikiem, który przeczy,
więc bez cząstki nie ma on jak wystrzelić i wariant ma oddać dokładnie to, co
wariant bez negacji. Zero jest tu więc odczytem, a nie przeoczeniem.

Cały pomiar prowadzi ``sonda/ruch.py``, wspólny sondom różnicowym tego pakietu, a
tutaj zostaje jedno pytanie: do której z dwóch rzeczy należy produkcja.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.negacja Składnica-frazowa-180723/
    python3 -m sonda.negacja proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, Spec, Sym, Word
from olski.subset import PRZECZENIE
from sonda import ruch

#: Wartość cechy ``negacja``, którą niesie konstytuent stojący pod przeczeniem.
#: Ta sama, którą Morfeusz nazywa negację formy, i to jest zbieg nazw: gramatyka
#: pyta o przeczenie zdania, a nie o cechę tagu.
NEG = "neg"


def _przeczy(warunki: frozenset[tuple[str, Spec]]) -> bool:
    """Czy ten pęk warunków albo cech mówi o zdaniu przeczącym."""
    return any(
        nazwa == "negacja" and isinstance(wartość, frozenset) and NEG in wartość
        for nazwa, wartość in warunki
    )


def rzecz(produkcja: Production) -> str | None:
    """Którą z dwóch rzeczy wnosi ta produkcja; ``None``, gdy żadnej.

    Pytanie stawiane produkcji, a nie liście nazw obok gramatyki: pozycja
    dopisana kiedyś dla trzeciego miejsca, w którym przeczenie stoi, odpowie tu
    sama, a lista obok przemilczałaby ją.

    Cząstka jest pytaniem pierwszym, bo produkcja z cząstką ogłasza przy niej i
    ``neg``, a należy do cząstki: to ona wnosi przeczenie, a wartość cechy jest
    tym, co przeczenie o sobie mówi dalej.
    """
    if PRZECZENIE in produkcja.body:
        return "cząstka"
    if _przeczy(produkcja.features):
        return "dopełniacz"
    if any(
        isinstance(część, Sym | Word) and _przeczy(część.constraints)
        for część in produkcja.body
    ):
        return "dopełniacz"
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.negacja",
    opis="Ile negacja kupuje i ile kosztuje.",
    warianty=("bez negacji", "cząstka", "dopełniacz", "obie"),
    grupa=rzecz,
    pytania=(
        "obie rzeczy ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
