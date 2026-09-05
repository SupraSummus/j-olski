"""Kwalifikator słownika, czyli co SGJP mówi o rejestrze formy.

Kwalifikator mówi o formie więcej niż jedną rzecz i tylko jedna z nich jest
rejestrem: `daw.` przy `ócz` odsyła formę poza tę prozę, a `anat.` przy `oczy`
nazywa dziedzinę. Dlatego :data:`POZA_REJESTREM` wypisuje kwalifikatory
odsyłające, a nie przyjmowane; wywód tego podziału wraz z ceną trzyma
``docs/formy-i-leksemy.md``.

Obie strony słownika czytają tę listę i robią z niej co innego.
Synteza formę odesłaną zdejmuje, bo wybiera jedną z kilku poprawnych
i forma spoza rejestru nie jest tam wyborem gorszym, tylko żadnym
(``olski/skład/morfologia.py``).
Analiza jej nie zdejmuje, bo zdanie z taką formą polszczyzna ma,
tylko liczy ją kosztem (:func:`pozycje`).
"""

from __future__ import annotations

from collections.abc import Iterable

from olski import cennik

#: Kwalifikatory, którymi słownik odsyła formę poza rejestr tego projektu.
#: Podział ten kosztuje dwa razy i oba razy cicho:
#: nazwa rejestru, której tu nie ma, przechodzi jak nazwa dziedziny,
#: a nazwa wpisana tu z literówką nie odsiewa niczego i nie zgłasza tego nigdzie,
#: bo świadka w słowniku ta lista nie ma, a leksykon przyimków obok ma połowę swojego.
#: Skąd się wzięła i czym ją przeliczyć, mówi ``docs/formy-i-leksemy.md``.
POZA_REJESTREM = frozenset(
    {
        "daw.",
        "daw._dziś_gwar.",
        "gwar.",
        "indyw.",
        "podniosłe",
        "poet.",
        "pogard.",
        "pot.",
        "przest.",
        "przest._dziś_książk.",
        "reg.",
        "rub.",
        "rzad.",
        "środ.",
        "wulg.",
        "żart.",
    }
)


def poza_rejestrem(kwalifikatory: Iterable[str]) -> bool:
    """Czy któryś kwalifikator tej formy odsyła ją poza rejestr.

    Słownik wydaje kwalifikatory sklejone przecinkiem w jednym napisie,
    a ``daw._dziś_gwar.`` jest jednym kwalifikatorem wraz z podkreślnikami,
    więc rozdzielać wolno tylko przecinek.
    Dość jednego odsyłającego, żeby forma wypadła, także obok nazwy dziedziny:
    ``ócz`` niesie kwalifikator dawny razem z anatomicznym i wypada,
    a ``oczy``, które niosą sam anatomiczny, zostają.
    """
    nazwy = {nazwa for napis in kwalifikatory for nazwa in napis.split(",")}
    return bool(nazwy & POZA_REJESTREM)


def pozycje(kwalifikatory: Iterable[str]) -> tuple[str, ...]:
    """Pozycje cennika, którymi płaci czytanie o tych kwalifikatorach.

    Nazwy, a nie liczba, bo pyta o nie i las, który po nich porządkuje czytania,
    i rachunek, który pod czytaniem wypisuje, za co ono płaci
    (``Verdict.rachunki`` w ``olski/werdykt/zdanie.py``). Cenę ma na własność cennik,
    a to, które kwalifikatory odsyłają, ten plik.
    """
    return (cennik.FORMA_SPOZA_REJESTRU,) if poza_rejestrem(kwalifikatory) else ()


def koszt(kwalifikatory: Iterable[str]) -> int:
    return cennik.suma(pozycje(kwalifikatory))
