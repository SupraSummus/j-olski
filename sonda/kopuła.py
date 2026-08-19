"""Co kupuje i co kosztuje kopuła opuszczona, liczone zdejmowaniem obu jej ciał.

Rejestr ustaw pisze `zadania, o których mowa w ustawie`, czyli zdanie względne,
w którym orzeka sam rzeczownik, a `jest` nikt nie pisze. Zwrot ten niesie co
siódme zdanie dwóch korpusów tego rejestru i jest w nich najczęstszym zdaniem
względnym, a wariant bez kopuli opuszczonej nie wyprowadza go wcale, bo zdania
składowego bez czasownika nie ma (``docs/ustawy.md``).

Trudność nie leży w produkcjach, bo tych są cztery. Leży w tym, z czym takie
zdanie konkuruje. Rzeczownik w mianowniku jest w każdym innym miejscu tej
gramatyki podmiotem albo orzecznikiem, więc zdanie bez czasownika staje obok
czytania, w którym ten sam wyraz jest grupą imienną w zdaniu nad nim, a
przecinek koordynacji stoi tam, gdzie zdanie względne otwiera swój.

Grupy są dwie i każda jest jednym ciałem, bo cena każdej z nich jest osobną liczbą.
``rzeczownik pod czołem`` to ciało czoła, w którym wysunięte wyrażenie przyimkowe
bierze ten rzeczownik wprost: `o których` jest tym, o czym on orzeka, więc zdania
składowego pod tym czołem nie ma wcale. ``rzeczownik z okolicznikiem`` to zdanie składowe, w którym
rzeczownik bierze okolicznik sam — `Mowa o zadaniach.` — i to ono konkuruje z
przyłączeniem tego wyrażenia wyżej, bo `zadania, o których mowa w ustawie`
wyprowadza się i pod jednym ciałem, i pod drugim, a przyłączenie ma w nich inne.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.kopuła Składnica-frazowa-180723/
    python3 -m sonda.kopuła proza/ustawy.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production
from olski.subset import ORZEKAJĄCY
from sonda import ruch

POD_CZOŁEM = "rzeczownik pod czołem"
Z_OKOLICZNIKIEM = "rzeczownik z okolicznikiem"

#: Symbol listy okoliczników. Napisem, tak jak w pozostałych sondach pytających o
#: kształt produkcji: gramatyka nazwy tego symbolu nie wypisuje stałą, a sonda
#: pyta o produkcję, nie o listę obok niej.
OKOLICZNIK = "Adjuncts"


def ciało(produkcja: Production) -> str | None:
    """Którym z dwóch ciał wpuszcza ten rzeczownik ta produkcja.

    Odpowiada kształt ciała, a nie lista nazw wypisana obok gramatyki: rozdziela je
    okolicznik, bo zdanie składowe go żąda, a czoło bierze rzeczownik sam, więc
    czoło dopisane kiedyś którejkolwiek z rodzin trafi tu samo, gdzie lista nazw
    postarzałaby się bez śladu.

    Produkcja samego rzeczownika zostaje w każdym wariancie i nie należy do żadnej
    z grup, bo oba ciała ją biorą; tak samo zostaje grupa wysunięta w
    ``sonda/wysunięcie.py``. Wariant bez kopuli opuszczonej zostawia ją przez to
    bez drogi z góry, a symbol nieosiągalny nie wyprowadza niczego.
    """
    if not ruch.ma_symbol(produkcja, ORZEKAJĄCY):
        return None
    return Z_OKOLICZNIKIEM if ruch.ma_symbol(produkcja, OKOLICZNIK) else POD_CZOŁEM


SONDA = ruch.Sonda(
    prog="python3 -m sonda.kopuła",
    opis="Ile kopuła opuszczona kupuje i ile kosztuje.",
    warianty=("bez kopuli opuszczonej", POD_CZOŁEM, Z_OKOLICZNIKIEM, "olski"),
    grupa=ciało,
    pytania=(
        "oba ciała ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
