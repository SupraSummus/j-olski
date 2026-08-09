"""Formy, czyli Morfeusz czytany w drugą stronę.

Analiza odwzorowuje formę na tagi, synteza lemat wraz z tagiem na formę,
i to drugie jest tym, po co ten moduł jest.
Zapleczem obu jest ten sam SGJP, więc odmiana bierze się tu ze słownika,
a nie ze zgadywania wzorca po zakończeniu wyrazu.
``docs/prior-art.md`` mówi, czym ten słownik jest i czemu przeważył.

Zgodność nie jest tu sprawdzana, tylko liczona.
Parsowanie godzi ze sobą dwie wiązki cech, z których każda niesie kilka wartości,
a synteza żąda jednej formy po tagu, który już stoi rozstrzygnięty.
Cała trudność, dla której olski istnieje, przy tym kierunku nie powstaje,
i dlatego ten moduł jest krótki.
"""

from __future__ import annotations

import functools

import morfeusz2

from olski.morph import tag


class BrakFormy(Exception):
    """Morfologia takiej formy nie ma.

    Wyjątek, a nie forma zgadnięta albo pominięta,
    bo to jest błąd kompilacji: drzewo żąda czegoś, czego polszczyzna nie odmienia.
    """


@functools.lru_cache(maxsize=1)
def _synteza() -> morfeusz2.Morfeusz:
    """Morfeusz w trybie syntezy, trzymany jeden, bo słownik siedzi w pamięci."""
    return morfeusz2.Morfeusz(generate=True, expand_tags=False)


@functools.lru_cache(maxsize=4096)
def paradygmat(lemat: str, pos: str) -> tuple[tuple[str, frozenset], ...]:
    """Wszystkie formy lematu w danej części mowy, wraz z cechami każdej.

    Liczone raz na lemat, bo linearyzacja pyta o ten sam lemat tyle razy,
    ile stoi on w drzewie, a Morfeusz i tak wydaje cały paradygmat naraz.
    """
    formy = []
    for forma, _lemat, surowy, *_ in _synteza().generate(lemat):
        czytanie = tag(surowy)
        if czytanie.pos == pos:
            formy.append((forma, czytanie.features))
    return tuple(formy)


def odmień(lemat: str, pos: str, **żądane: str) -> str:
    """Forma lematu, która spełnia żądanie postawione cechami.

    Cechy, której cały paradygmat nie ma, żądanie nie dotyczy.
    Żądanie jest tu kryterium wyboru, a nad kolumną o jednej wartości
    kryterium nie wybiera niczego, więc odsianie po niej byłoby odsianiem wszystkiego.
    Widać to na przysłówku: ``nagle`` ma stopień i ``wkrótce`` go nie ma,
    a żądać stopnia równego trzeba od obu, bo o odmienności rozstrzyga leksem.
    Cecha, którą paradygmat ma, a której ta forma nie niesie, żądania nadal nie spełnia,
    i to jest różnica między brakiem wyboru a wyborem chybionym.

    Gdzie żądaniu odpowiada kilka różnych form, bierze pierwszą.
    To jest jedyne miejsce, w którym kompilator wybiera i nie mówi o tym,
    a reszta wyborów stoi w drzewie, które napisał autor.
    Czym ten wybór ma być, nie zapadło, i trzyma to ``TODO.md``.
    """
    formy = paradygmat(lemat, pos)
    obecne = {nazwa for _forma, cechy in formy for nazwa, _wartości in cechy}
    kryterium = {nazwa: wartość for nazwa, wartość in żądane.items() if nazwa in obecne}
    trafienia = [forma for forma, cechy in formy if _spełnia(dict(cechy), kryterium)]
    if not trafienia:
        raise BrakFormy(f"{lemat} ({pos}) nie ma formy {żądane}")
    return trafienia[0]


def _spełnia(cechy: dict[str, frozenset[str]], żądane: dict[str, str]) -> bool:
    """Czy forma niesie każdą żądaną wartość.

    Cecha, której forma nie niesie, żądania nie spełnia, i to jest tu zamierzone.
    Przy analizie brak cechy znaczy, że nie ma czym się nie zgodzić,
    a przy syntezie znaczy, że nie ma czego wypisać.
    """
    return all(wartość in cechy.get(nazwa, frozenset()) for nazwa, wartość in żądane.items())


@functools.lru_cache(maxsize=4096)
def rodzaj_rzeczownika(lemat: str) -> str:
    """Rodzaj wzięty z mianownika liczby pojedynczej.

    Rodzaj rzeczownika jest leksykalny: autor go nie wybiera, a zgodność go żąda,
    więc nie stoi w drzewie, tylko przychodzi stąd.
    """
    for _forma, cechy in paradygmat(lemat, "subst"):
        słownik = dict(cechy)
        if "nom" in słownik.get("case", ()) and "sg" in słownik.get("number", ()):
            return sorted(słownik["gender"])[0]
    raise BrakFormy(f"{lemat} nie ma mianownika liczby pojedynczej")
