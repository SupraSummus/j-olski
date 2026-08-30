"""Kwalifikator słownika, czyli co SGJP mówi o rejestrze formy.

Kwalifikator mówi o formie więcej niż jedną rzecz i tylko jedna z nich jest
rejestrem: `daw.` przy `ócz` odsyła formę poza tę prozę, a `anat.` przy `oczy`
nazywa dziedzinę. Dlatego :data:`POZA_REJESTREM` wypisuje kwalifikatory
odsyłające, a nie przyjmowane; wywód tego podziału wraz z ceną trzyma
``docs/sklad.md``.

Obie strony słownika czytają tę listę i robią z niej co innego.
Synteza formę odesłaną zdejmuje, bo wybiera jedną z kilku poprawnych
i forma spoza rejestru nie jest tam wyborem gorszym, tylko żadnym
(``olski/skład/morfologia.py``).
Analiza jej nie zdejmuje, bo zdanie z taką formą polszczyzna ma,
tylko liczy ją kosztem (:data:`KOSZT_POZA_REJESTREM`).
"""

from __future__ import annotations

from collections.abc import Iterable

#: Kwalifikatory, którymi słownik odsyła formę poza rejestr tego projektu.
#: Podział ten kosztuje dwa razy i oba razy cicho:
#: nazwa rejestru, której tu nie ma, przechodzi jak nazwa dziedziny,
#: a nazwa wpisana tu z literówką nie odsiewa niczego i nie zgłasza tego nigdzie,
#: bo świadka w słowniku ta lista nie ma, a leksykon przyimków obok ma połowę swojego.
#: Skąd się wzięła i czym ją przeliczyć, mówi ``docs/sklad.md``.
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

#: O ile niżej stoi czytanie stojące na formie, którą słownik odesłał poza rejestr.
#: Całkowity i wypisany ręką z tego samego powodu co koszty produkcji
#: (docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie):
#: jest deklaracją o rejestrze, a nie częstością, bo częstości słownik nie zna.
KOSZT_POZA_REJESTREM = 1


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


def koszt(kwalifikatory: Iterable[str]) -> int:
    return KOSZT_POZA_REJESTREM if poza_rejestrem(kwalifikatory) else 0
