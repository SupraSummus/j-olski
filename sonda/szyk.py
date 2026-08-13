"""Ile kupuje i ile kosztuje każdy z czterech dopisanych szyków, nad Składnicą.

Pytanie, ile każdy z czterech odbiera, stawia sam kształt tej gramatyki:
dopełnienie przed czasownikiem jest tam także przydawką dopełniaczową grupy
imiennej przed sobą, a podmiot za czasownikiem jest grupą, która to dopełnienie
może wziąć do siebie, więc każdy z tych szyków konkuruje z czytaniem, które
gramatyka ma bez niego. Sumy z ``olski-corpus`` na to nie odpowiadają, bo
przejście ``przyjęte → wieloznaczne`` widać dopiero zdanie po zdaniu, a wariant
osobny ma każdy z czterech, bo cena każdego jest osobną liczbą.

Cały pomiar prowadzi ``sonda/ruch.py``, wspólny sondom różnicowym tego pakietu, a
tutaj zostaje jedno pytanie: który szyk wypisuje ta produkcja.

Wynik czyta ``docs/subset.md``.

    python3 -m sonda.szyk Składnica-frazowa-180723/
    python3 -m sonda.szyk proza/README.txt
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import Production, Sym
from sonda import ruch

#: Symbol → litera, którą nazywa go nazwa szyku. Szyki nazywają się skrótem
#: angielskim, bo tak nazywa je cała reszta tych dokumentów i bo litery są
#: literami symboli gramatyki, które stoją po angielsku razem ze słownikiem.
LITERY = {"Subject": "S", "Object": "O", "Verb": "V"}

#: Szyki dopisane, czyli te, których cenę ta sonda liczy. Dwa, które olski miał,
#: tu nie stoją: ``OVS`` wypisuje się w tej gramatyce tak samo, a ``SVO`` wcale,
#: bo dopełnienie wisi tam pod ``Predicate`` razem z czasownikiem.
DOPISANE = ("SOV", "OSV", "VSO", "VOS")


def szyk(produkcja: Production) -> str | None:
    """Który z dopisanych szyków wypisuje ta produkcja; ``None``, gdy żadnego.

    Pytanie stawiane produkcji, a nie liście nazw obok gramatyki: piąte miejsce
    na okolicznik dopisane kiedyś do jednego z tych szyków odpowie tu samo, a
    lista obok przemilczałaby je i sonda mierzyłaby dalej czternaście ciał.

    Czyta się z ciała same trzy symbole, które szyk nazywa, więc okolicznik
    wypada z odczytu i cztery wersje jednego szyku wychodzą jedną nazwą. Zdanie
    względne ma własną rodzinę ciał i własne szyki, więc pytanie stoi przy
    symbolu zdania składowego, a nie przy każdym, którego ciało te trzy symbole
    niesie.
    """
    if produkcja.head != "ClauseConjunct":
        return None
    nazwa = "".join(
        LITERY[część.name]
        for część in produkcja.body
        if isinstance(część, Sym) and część.name in LITERY
    )
    return nazwa if nazwa in DOPISANE else None


SONDA = ruch.Sonda(
    prog="python3 -m sonda.szyk",
    opis="Ile kupuje i ile kosztuje każdy z czterech dopisanych szyków.",
    warianty=("bez czterech szyków", *DOPISANE, "wszystkie cztery"),
    grupa=szyk,
    pytania=(
        "dwa szyki ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)


def main(argv: Sequence[str] | None = None) -> int:
    return ruch.main(SONDA, argv)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
