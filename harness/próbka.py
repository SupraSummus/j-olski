"""Próbka do przeczytania ręką, rozrzucona po całej liście trafień.

Sonda, która wypisuje przykłady, wypisuje je po to, żeby ktoś je przeczytał i
powiedział, czy liczba nad nimi znaczy to, co obiecuje. Głowa listy tego nie
powie: jest pierwszym dokumentem korpusu albo pierwszą literą alfabetu, a nie
korpusem. Wybór stoi więc w jednym miejscu, bo dwa liczyłyby krok inaczej i dwie
sondy czytałoby się dwoma sposobami.
"""

from __future__ import annotations

from collections.abc import Sequence


def rozrzucona(trafione: Sequence, ile: int) -> list:
    """Co ``ile``-ta pozycja listy, od pierwszej.

    Krok jest ilorazem, więc próbka jest ta sama przy każdym przebiegu i daje
    się przeczytać drugi raz po tym samym.
    """
    if ile <= 0 or not trafione:
        return []
    if ile >= len(trafione):
        return list(trafione)
    krok = len(trafione) / ile
    return [trafione[int(i * krok)] for i in range(ile)]
