"""Co kupuje i co kosztuje przysłówek, liczone zdejmowaniem go z gramatyki.

Kolejka blokerów prowadzi do przysłówka dwoma wierszami z rzędu: ``adv`` stoi w
niej druga z 1992 zdaniami, a nad prozą tego repozytorium przysłówek stoi zaraz za
dwukropkiem (``docs/corpus.md``).

Trudność nie leży w produkcjach, bo tych jest sześć. Leży w tym, że przysłówek ma
w polszczyźnie więcej niż jednego gospodarza i staje przy każdym z nich w tym
samym miejscu napisu: ``Plik jest bardzo duży`` czyta się z ``bardzo`` przy
``duży`` i z ``bardzo`` przy całym zdaniu, a olski odrzuca zdanie, które wychodzi
dwoma czytaniami. Jednoznaczność jest własnością, którą przysłówek atakuje wprost,
i dlatego pomiar rozdziela gospodarzy, zamiast wyceniać konstrukcję w całości.

Wycena szła tu kiedyś w drugą stronę, bo gramatyka przysłówka nie miała, a sonda
dopisywała go świeżej gramatyce. Teraz olski go ma, więc mierzy się przez
zdejmowanie, jak każdą inną konstrukcję stojącą w gramatyce: dopisek byłby drugą
deklaracją tego samego i rozszedłby się z olskim po pierwszej zmianie
(``sonda/ruch.py``).

Grupy są dwie i każda jest jednym gospodarzem. ``okolicznik`` to przysłówek w
liście okoliczników, czyli tam, gdzie stoi wyrażenie przyimkowe, i przed zdaniem.
``przy przymiotniku`` to przysłówek stopniowany pod symbolem przymiotnika, i
żadnego innego tam nie ma, bo przymiotnik określa przysłówek odprzymiotnikowy, a
nie pierwotny, i tę różnicę Morfeusz niesie stopniem.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.przysłówek Składnica-frazowa-180723/
    python3 -m sonda.przysłówek proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, nt
from olski.subset import PRZYSŁÓWEK, PRZYSŁÓWEK_STOPNIA, PRZYSŁÓWKOWY
from sonda import ruch

OKOLICZNIK = "okolicznik"
PRZY_PRZYMIOTNIKU = "przy przymiotniku"


def gospodarz(produkcja: Production) -> str | None:
    """Przy którym gospodarzu stawia przysłówek ta produkcja; ``None``, gdy żadnym.

    Odpowiada terminal albo symbol przysłówka, a nie lista nazw wypisana obok
    gramatyki: ciało dopisane kiedyś w którymkolwiek z dwóch miejsc trafi tu samo,
    gdzie lista postarzałaby się bez śladu — sonda mierzyłaby wariant węższy, niż o
    sobie mówi, i nie powiedziałaby o tym ani słowem.

    Okolicznik zdejmuje się przy tym czterema produkcjami, a wystarczyłaby jedna:
    ``Adverb → adv`` jest jedyną, która przysłówek do zdania wpuszcza, więc bez
    niej dwa ciała listy okoliczników i czoło zdania nie mają czym się wypełnić.
    Zdejmowane są mimo to wszystkie, bo wariant ma być gramatyką bez tej
    konstrukcji, a nie gramatyką z symbolem, do którego nic nie prowadzi.
    """
    if PRZYSŁÓWEK_STOPNIA in produkcja.body:
        return PRZY_PRZYMIOTNIKU
    if PRZYSŁÓWEK in produkcja.body or nt(PRZYSŁÓWKOWY) in produkcja.body:
        return OKOLICZNIK
    return None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.przysłówek",
    opis="Ile przysłówek kupuje i ile kosztuje.",
    warianty=("bez przysłówka", OKOLICZNIK, PRZY_PRZYMIOTNIKU, "olski"),
    grupa=gospodarz,
    pytania=(
        "obaj gospodarze ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
