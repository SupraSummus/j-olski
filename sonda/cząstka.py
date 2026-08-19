"""Co kupuje i co kosztuje cząstka przy zdaniu, liczone zdejmowaniem jej.

Wiersz ``part`` stoi w kolejce blokerów ze Składnicy drugi, a nad prozą tego
repozytorium cząstka prowadzi tę kolejkę, odkąd gramatyka ma rzeczownik
odczasownikowy (``docs/corpus.md``).

Trudność nie leży w kształcie tej produkcji, bo cząstka stoi tam, gdzie przysłówek,
i tę pozycję gramatyka już ma. Leży w liście lematów. ``part`` niesie u Morfeusza
całą klasę cząstek naraz, a w niej `nie`, `się`, `by` i `czy`, czyli słowa, które
olski bierze albo wyklucza osobno, oraz `tylko` i `też`, które mają czytanie
brane już gdzie indziej — więc lista zamknięta jest tu warunkiem prawdziwości, a
nie ostrożnością, i to ją ta sonda wycenia.

Cena stoi tam, gdzie zdanie już przyjęte przestaje być jednoznaczne, bo cząstka
wpuszczona do listy okoliczników konkuruje z każdym innym czytaniem swojej formy.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.cząstka Składnica-frazowa-180723/
    python3 -m sonda.cząstka proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production
from olski.subset import CZĄSTKA, CZĄSTKOWY
from sonda import ruch

OKOLICZNIK = "w liście okoliczników"
NA_CZELE = "na czele zdania"

#: Symbol zdania składowego, czyli tego, przed którym stoi cząstka wysunięta.
#: Napisem, tak jak w pozostałych sondach pytających o kształt produkcji.
ZDANIE_SKŁADOWE = "ClauseConjunct"


def grupa(produkcja: Production) -> str | None:
    """W której pozycji ta produkcja stawia cząstkę; ``None``, gdy w żadnej.

    Odpowiada symbol cząstki stojący w ciele, a nie lista nazw obok gramatyki:
    pozycja dopisana kiedyś tej klasie trafi tu sama, gdzie lista postarzałaby się
    bez śladu. Rozstrzyga przy tym symbol, który tę pozycję stawia, a nie kształt
    ciała: cząstka wysunięta stoi przed zdaniem składowym, a w liście okoliczników
    stoi przy czasowniku.

    Produkcja samej cząstki zostaje w każdym wariancie i nie należy do żadnej
    grupy, bo obie pozycje ją biorą; wariant mianownikowy zostawia ją przez to bez
    drogi z góry, a symbol nieosiągalny nie wyprowadza niczego — tak samo jak przy
    grupie wysuniętej w ``sonda/wysunięcie.py``.
    """
    if CZĄSTKA in produkcja.body or not ruch.ma_symbol(produkcja, CZĄSTKOWY):
        return None
    return NA_CZELE if produkcja.head == ZDANIE_SKŁADOWE else OKOLICZNIK


SONDA = ruch.Sonda(
    prog="python3 -m sonda.cząstka",
    opis="Ile kupuje i ile kosztuje cząstka przy zdaniu.",
    warianty=("bez cząstki", OKOLICZNIK, NA_CZELE, "olski"),
    grupa=grupa,
    pytania=(
        "obie pozycje ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
