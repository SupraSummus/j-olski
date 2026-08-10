"""Czym polszczyzna wprowadza okoliczność wyrażoną zdarzeniem.

Przyimek stoi przed rzeczą, a spójnik przed zdarzeniem,
i jedno, i drugie jest słowem, którym relacja wychodzi na wierzch,
więc ten plik jest tym samym co ``skład/przyimki.py`` o piętro wyżej.
Relacja przy tym się nie zmienia: ``w nocy`` i ``gdy zapadła noc``
odpowiadają na jedno pytanie i różnią się tym, co pod tym pytaniem stoi.

Wpis mówi mniej niż tamten, bo spójnik nie rządzi niczym:
zdanie podrzędne rozdaje przypadki własne i nie bierze ich stąd.
Zostaje samo pytanie, czy słowo w tej relacji stoi,
a jest ono tym samym pytaniem, na które tamten plik odpowiada przypadkiem:
``gdy`` mówi, kiedy, a ``bo`` mówi, dlaczego,
i drzewo, które je zamienia miejscami, nie ma powstać.

Wpis niesie za to jedno, czego tamten nie niesie, i jest to fakt o szyku.
Zdanie z ``gdy`` staje na czele pary albo za nią, i o tym rozstrzyga autor,
a zdanie z ``więc`` stoi za nią zawsze, bo polszczyzna nie ma pary,
która zaczyna się od skutku.
Stoi to tutaj, a nie w linearyzacji, bo jest to fakt o słowie,
tak samo jak przypadek jest faktem o przyimku.

Świadek w słowniku jest tu pełniejszy niż tam i sięga tylko pierwszej kolumny.
SGJP znakuje spójnik podrzędny jako ``comp`` i rozdziela go od współrzędnego,
więc słowo wypisane tutaj, a tak nieznakowane, zgłasza się w ``tests/test_spójniki.py``.
Doboru relacji ten świadek nie sprawdza, tak jak przy przyimkach,
a o szyku nie mówi nic, bo ``więc`` znakuje tak samo jak ``bo``,
więc rozstrzyga o obu ten plik i nic poza nim.
"""

from __future__ import annotations

#: Spójniki podrzędne, każdy w relacji, którą wprowadza,
#: wraz z tym, czy jego zdanie staje na czele pary.
#: Kluczem jest para, a nie sam spójnik, bo relacja jest kategorią dziedziny,
#: a spójników jednej relacji polszczyzna ma kilka.
SPÓJNIKI: dict[tuple[str, str], bool] = {
    ("bo", "przyczyna"): False,
    ("gdy", "czas"): True,
    ("kiedy", "czas"): True,
    ("ponieważ", "przyczyna"): True,
    ("więc", "skutek"): False,
    ("zanim", "czas"): True,
}


def wprowadza(spójnik: str, relacja: str) -> bool:
    """Czy tym słowem polszczyzna wprowadza zdarzenie stojące w tej relacji.

    Odpowiedzią jest prawda albo fałsz, a nie wyjątek,
    bo zgłasza go konstruktor okolicznika w ``skład/składnia.py``,
    czyli to samo miejsce, które zgłasza milczenie leksykonu przyimków.
    """
    return (spójnik, relacja) in SPÓJNIKI


def staje_na_czele(spójnik: str, relacja: str) -> bool:
    """Czy zdanie z tym spójnikiem wolno wysunąć przed to, przy którym stoi.

    Pytany jest ten leksykon, a nie polszczyzna liczona z relacji,
    bo ``bo`` i ``ponieważ`` stoją w jednej relacji i odpowiadają różnie.
    """
    return SPÓJNIKI[spójnik, relacja]
