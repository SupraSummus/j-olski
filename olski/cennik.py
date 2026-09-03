"""Cennik: co w tej gramatyce jest nacechowane i ile to kosztuje.

Koszt porządkuje czytania i werdyktu nie rusza; czym jest i czego nie robi, mówi
``docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie``.

Produkcja nazywa tutaj pozycje, którymi płaci, a ceny nie wypisuje
(:attr:`olski.grammar.Production.koszty`).
Kalibracja jest przez to edycją jednego pliku,
a czytelnik strony dostaje pod czytaniem nie liczbę bez nazwy,
tylko to, za co ono płaci (``witryna/skrypt.js``).

Cena jest deklaracją o polszczyźnie, a nie częstością wziętą z korpusu:
mówi, że jedno czytanie tego samego napisu jest zwyklejsze od drugiego.
Nikt jej nie zmierzył; czym się ją mierzy i czego ten pomiar dziś nie widzi,
mówi wpis o kolejności czytań w ``todo/pomiar.md``.

Pozycje dzielą się na dwie rodziny i różni je to, dokąd cena sięga.
Pozycję produkcji płaci ciało i płaci ją na miejscu:
rozstrzyga ona między ciałami jednej pozycji lasu, a nad rodzicem już nie waży
(``test_koszt_produkcji_nie_sumuje_się_do_kosztu_rodzica``).
Pozycję morfologii płaci forma, a cena idzie w górę,
aż trafi na ciała, które się nią różnią (``koszt_morfologii`` w ``olski/parse/las.py``).
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
#: do którego z nich należy. Ze wszystkich tych cen zmierzono jeden znak, ten
#: przy okoliczniku
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


def rachunek(koszty: Iterable[str]) -> tuple[tuple[str, int], ...]:
    """Te pozycje policzone — nazwa wraz z liczbą wystąpień — w kolejności :data:`CENNIK`.

    Nazwy przychodzą tu sprawdzone, bo płaci nimi produkcja
    (:class:`olski.grammar.Production`) albo kwalifikator (``olski/rejestr.py``),
    a obie drogi wołają wcześniej :func:`cena`.
    """
    ile = Counter(koszty)
    return tuple((nazwa, ile[nazwa]) for nazwa in CENNIK if nazwa in ile)
