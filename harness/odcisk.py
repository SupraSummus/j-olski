"""Odcisk gramatyki: produkcje wraz z deklaracją, wypisane do porównania diffem.

Zmiana, która przestawia gramatykę, nie ruszając tego, co się z niej wyprowadza,
nie ma czym tego dowieść. Odcisk werdyktów po całej prozie trwa parę minut, żąda
Morfeusza i mówi o zdaniach, a nie o produkcjach, więc różnicę pokazuje dopiero
na zdaniu, którego werdykt się przez nią zmienia. Taką zmianą jest deklaracja
czytana w miejsce listy wypisanej ręką: nie rusza ona ani jednego werdyktu, a
dowieść jej trzeba tak samo, i wtedy jedynym przyrządem jest odcisk gramatyki.

Odcisk, który o jakimś polu milczy, jest gorszy od jego braku: mówi, że nie
ruszyło się nic, o zmianie, której nie umiał zobaczyć. Dlatego ``repr`` produkcji
tu nie wystarcza — wypisuje głowę i ciało, a przemilcza cechy, koszty i lematy
terminala — a :func:`wypisz` pyta o pola samą klasę.

Kolejność produkcji jest kolejnością gramatyki, a nie posortowaną, bo gramatyka
tę kolejność widzi: czytania o równym koszcie idą tak, jak ``for_head`` oddaje
produkcje (:meth:`olski.parse.Las.wyprowadzenia`), więc samo przestawienie
dopisań rusza kolejność czytań i ma się w odcisku pokazać. Zbiór wypisuje się za
to posortowany, bo hasze napisów są losowane przy starcie i nieposortowany
pokazywałby różnicę, której nie ma.

Dwa drzewa robocze stawia się przy tym obok siebie, a nie jedno po drugim, tak
samo jak przy zmianie, która ma tylko przyspieszyć:

    git worktree add ../baza HEAD
    diff <(cd ../baza && python3 -m harness.odcisk) <(python3 -m harness.odcisk)
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from dataclasses import MISSING, Field, fields, is_dataclass

from olski.cennik import CENNIK
from olski.grammar import Grammar
from olski.parse import Deklaracja
from olski.subset import DEKLARACJA, GRAMMAR


def _domyślne(pole: Field, wartość: object) -> bool:
    """Czy wolno to pole pominąć: skraca wiersz o połowę, a różnicy nie chowa,
    bo produkcja o innej wartości wypisuje je i tym się od tamtej różni.
    """
    return pole.default is not MISSING and wartość == pole.default


def wypisz(wartość: object) -> str:
    """Wartość gramatyki wypisana tak, że dwa przebiegi piszą ją tak samo.

    Dataclass wypisuje się polami, które sam deklaruje, więc pole dopisane do
    produkcji, terminala albo deklaracji wchodzi tutaj samo. Zbiór idzie
    posortowany po tym, co wypisały jego elementy, bo kolejność samego zbioru
    zależy od haszy losowanych przy starcie.
    """
    if is_dataclass(wartość) and not isinstance(wartość, type):
        wnętrze = ", ".join(
            f"{pole.name}={wypisz(getattr(wartość, pole.name))}"
            for pole in fields(wartość)
            if not _domyślne(pole, getattr(wartość, pole.name))
        )
        return f"{type(wartość).__name__}({wnętrze})"
    if isinstance(wartość, frozenset | set):
        return "{" + ", ".join(sorted(wypisz(element) for element in wartość)) + "}"
    if isinstance(wartość, dict):
        pary = sorted(wartość.items(), key=lambda para: wypisz(para[0]))
        return "{" + ", ".join(f"{wypisz(k)}: {wypisz(v)}" for k, v in pary) + "}"
    if isinstance(wartość, tuple | list):
        return "[" + ", ".join(wypisz(element) for element in wartość) + "]"
    return repr(wartość)


def odcisk(grammar: Grammar, deklaracja: Deklaracja) -> str:
    """Cała gramatyka jednym tekstem, po jednej produkcji na wiersz.

    Deklaracja i cennik stoją nad produkcjami, bo mówią, co werdykt z nich czyta
    i w jakiej kolejności je wydaje, a są od nich o dwa rzędy wielkości krótsze:
    diff pokazujący samą ich zmianę mieści się wtedy na ekranie.
    Cennik jest tu dlatego, że produkcja niesie same nazwy pozycji: cena
    przestawiona w nim samym nie ruszyłaby bez niego ani jednego wiersza niżej,
    a przestawia kolejność czytań (``olski/cennik.py``).
    """
    wiersze = ["deklaracja:"]
    for pole in fields(deklaracja):
        wiersze.append(f"  {pole.name} = {wypisz(getattr(deklaracja, pole.name))}")
    wiersze += ["", "cennik:"]
    wiersze += [f"  {nazwa} = {cena}" for nazwa, cena in CENNIK.items()]
    wiersze += ["", "gramatyka:"]
    #  Pola idą z ``vars``, żeby atrybut dopisany do gramatyki wszedł do odcisku
    #  sam. Odpadają dwa: podkreślone jest tym, co gramatyka o sobie policzyła,
    #  a produkcje mają niżej wiersz na każdą.
    for nazwa, wartość in sorted(vars(grammar).items()):
        if nazwa.startswith("_") or nazwa == "productions":
            continue
        wiersze.append(f"  {nazwa} = {wypisz(wartość)}")
    wiersze += ["", f"produkcje ({len(grammar.productions)}):"]
    wiersze += [f"  {wypisz(produkcja)}" for produkcja in grammar.productions]
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.odcisk",
        description="wypisz gramatykę tak, żeby dwa drzewa robocze dały się porównać diffem",
    )
    parser.parse_args(argv)
    print(odcisk(GRAMMAR, DEKLARACJA))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
