"""Cennik: co w tej gramatyce jest nacechowane i ile to kosztuje.

Koszt porządkuje czytania i werdyktu nie rusza; czym jest i czego nie robi, mówi
``docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie``.

Produkcja nazywa tutaj pozycje, którymi płaci, a ceny nie wypisuje
(:attr:`olski.grammar.Production.koszty`).
Kalibracja jest przez to edycją jednego pliku,
a czytelnik strony dostaje pod czytaniem nazwy obok liczb:
to, za co ono płaci, i to, ile płaci razem (``witryna/skrypt.js``).

Cena jest deklaracją o polszczyźnie, a nie częstością wziętą z korpusu:
mówi, że jedno czytanie tego samego napisu jest zwyklejsze od drugiego.
Czytania porządkuje suma pozycji po całym drzewie (:func:`razem`),
więc pozycja policzona przy korzeniu waży tyle samo, co pozycja spod niego.
Rozstrzyga przy tym porządek, w jakim pozycje stoją, a nie wysokość stawek,
i mówi to pomiar wariantami tej tabeli
(``docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie``).

Obie rodziny pozycji płaci się na miejscu:
pozycję produkcji ciało, które ją nosi,
a pozycję morfologii liść, na którym forma stoi
(:attr:`olski.parse.czytanie.Leaf.koszty`).
Wyżej żadna z nich nie idzie, bo suma bierze je spod całego drzewa.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

OKOLICZNIK = "okolicznik"
PRZESTAWIENIE = "przestawienie"
WYSUNIĘTY_ORZECZNIK = "wysunięty orzecznik"
CZASOWNIK_PRZED_PODMIOTEM = "czasownik przed podmiotem"
OPUSZCZONY_PODMIOT = "opuszczony podmiot"
WYSUNIĘTE_DOPEŁNIENIE_BEZOKOLICZNIKA = "wysunięte dopełnienie bezokolicznika"
FORMA_SPOZA_REJESTRU = "forma spoza rejestru"

#: Nazwa pozycji i jej cena. Nazwa jest po polsku i wychodzi na wierzch — pod
#: czytaniem na stronie i pod flagą ``--koszt`` — więc nazywa konstrukcję,
#: a nie produkcję, która ją wypisuje.
#:
#: Jednostką jest odstępstwo od szyku wypisanego w deklaracji, bo o nim
#: polszczyzna mówi najmniej: szyk swobodny znaczy, że przestawiony jest inny,
#: a nie że jest zły. Dwa razy tyle płacą konstrukcje, które żądają czegoś spoza
#: zdania: opuszczony podmiot każe szukać podmiotu w zdaniu obok, a wysunięte
#: dopełnienie bezokolicznika każe czytać dwa czasowniki naraz, żeby powiedzieć,
#: do którego z nich należy
#: (``docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie``).
#:
#: Jednostką jest sto, a nie jeden, i kupuje to miejsce na cenę pośrednią:
#: konstrukcja wyceniona kiedyś między okolicznikiem a opuszczonym podmiotem
#: dostaje sto pięćdziesiąt, zamiast każąc przenumerować cały cennik.
#: Porównuje się tu same różnice, więc skala nie znaczy nic poza tym.
#:
#: Kolejność wpisów jest kolejnością wydruku (:func:`rachunek`), więc rachunki
#: dwóch czytań jednego zdania stoją pod sobą w tym samym porządku.
CENNIK: dict[str, int] = {
    PRZESTAWIENIE: 100,
    OKOLICZNIK: 100,
    WYSUNIĘTY_ORZECZNIK: 100,
    CZASOWNIK_PRZED_PODMIOTEM: 100,
    OPUSZCZONY_PODMIOT: 200,
    WYSUNIĘTE_DOPEŁNIENIE_BEZOKOLICZNIKA: 200,
    FORMA_SPOZA_REJESTRU: 100,
}


def cena(nazwa: str) -> int:
    """Cena pozycji o tej nazwie.

    Nazwa nieznana podnosi wyjątek, zamiast kosztować zero:
    literówka w deklaracji przemilczana zdejmowałaby cenę
    i nie byłoby tego widać po niczym poza kolejnością czytań.
    """
    try:
        return CENNIK[nazwa]
    except KeyError:
        raise KeyError(f"cennik nie ma pozycji o nazwie {nazwa!r}") from None


def suma(koszty: Iterable[str]) -> int:
    """Ile płaci ten, kto płaci tymi pozycjami; pozycja powtórzona płaci tyle razy."""
    return sum(cena(nazwa) for nazwa in koszty)


def razem(policzone: Iterable[tuple[str, int]]) -> int:
    """Ile płaci czytanie o tym rachunku (:func:`rachunek`).

    Liczba ta jest miejscem w kolejce: las porządkuje czytania sumą cennika po
    całym drzewie (``docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie``),
    więc rachunek wypisany bez niej mówi, za co czytanie płaci, i przemilcza,
    czemu stoi tam, gdzie stoi.
    """
    return sum(cena(nazwa) * ile for nazwa, ile in policzone)


def rachunek(koszty: Iterable[str]) -> tuple[tuple[str, int], ...]:
    """Te pozycje policzone — nazwa wraz z liczbą wystąpień — w kolejności :data:`CENNIK`.

    Nazwy przychodzą tu sprawdzone, bo płaci nimi produkcja
    (:class:`olski.grammar.Production`) albo kwalifikator (``olski/rejestr.py``),
    a obie drogi wołają wcześniej :func:`cena`.
    """
    ile = Counter(koszty)
    return tuple((nazwa, ile[nazwa]) for nazwa in CENNIK if nazwa in ile)
