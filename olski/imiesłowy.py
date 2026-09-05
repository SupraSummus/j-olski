"""Imiesłów przysłówkowy przy orzeczeniu, które podmiotu nie ma.

`Idąc do pracy, zgubiono klucze.` nie mówi, kto szedł:
imiesłów podmiotu nie niesie i pożycza go od zdania, które określa,
a orzeczenie bezosobowe pożyczyć nie ma czego, bo samo podmiotu nie ma.
Po co to znalezisko autorowi, co znajduje nad cudzą prozą i czemu czeka za flagą,
trzyma docs/subset.md#imiesłów-przy-orzeczeniu-bezosobowym-czeka-za-flagą.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from olski.parse import Node, w_zakresie, zakresy
from olski.subset import (
    DEKLARACJA,
    IMIESŁÓW_PRZYSŁÓWKOWY,
    OKOLICZNIK_ZDANIOWY,
    ORZECZENIE_BEZOSOBOWE,
)


@dataclass(frozen=True)
class Imiesłów:
    """Imiesłów i orzeczenie, które podmiotu mu nie daje, oba formą ze zdania.

    Formą, tak jak :class:`olski.parse.Przyłączenie` nazywa gospodarzy:
    autor ma je odszukać w zdaniu, a stoją tam właśnie w tej formie.
    """

    imiesłów: str
    orzeczenie: str


def imiesłowy_bez_podmiotu(czytania: Sequence[Node]) -> tuple[Imiesłów, ...]:
    """Zgłoszenia o imiesłowach tego zdania; pusta krotka jest milczeniem.

    Czytania, a nie werdykt nad nimi: warunek czyta się z drzewa, a werdykt czyta
    stąd (``olski/werdykt/zdanie.py``), więc import w tamtą stronę zamykałby krąg.

    **Podmiotu pożycza imiesłów od swojego zdania składowego**, więc kryterium
    bierzemy stamtąd, skąd bierze je streszczenie czytania
    (:func:`olski.parse.w_zakresie`), i wiersz mówi o tym samym składowym,
    o którym mówi streszczenie obok niego.
    Bez tego podziału zgłoszenie dostawałoby `Zgubiono klucze, a Jan śpiewał,
    idąc do pracy.`, gdzie orzeczenie bezosobowe stoi w składowym obok.

    **Kształt wystarcza w jednym odczytaniu, a nie w każdym**, bo zdanie
    wieloznaczne stawia czytelnika przed każdym z nich; tak samo bierze je
    warstwa zaimkowa (``olski/odniesienia.py``).
    Ceną jest jedno trafienie na trzynaście przeczytanych nad NKJP, a czytelnik
    odrzucił je właśnie dlatego, że imiesłów należy tam do orzeczenia z podmiotem
    (``próba/nkjp-sądy.txt``).
    Iloczynu po odczytaniach mimo to nie bierzemy: wyliczanie urywa się na
    :data:`olski.parse.MAX_READINGS`, więc mówiłby on o odczytaniach wypisanych,
    a czytałby się jak zdanie o wszystkich, których zdanie ma więcej.

    Para wchodzi raz, choćby stała w kilku odczytaniach albo w kilku składowych,
    bo wiersz wypisany drugi raz nie mówi nic ponad ten nad sobą.
    Kolejnością jest kolejność odczytań i zdania w nich, a nie kolejność zbioru,
    bo dwa przebiegi mają wypisywać to samo.
    """
    znalezione: dict[tuple[str, str], None] = {}
    for czytanie in czytania:
        for zakres in zakresy(czytanie, DEKLARACJA.składowe):
            orzeczenia = w_zakresie(czytanie, ORZECZENIE_BEZOSOBOWE, DEKLARACJA.podrzędne, zakres)
            if not orzeczenia:
                continue
            #  Pierwsze w porządku zdania, bo składowe ma zwykle jedno, a wiersz
            #  mówi autorowi, przy którym orzeczeniu podmiotu brakuje.
            orzeczenie = orzeczenia[0].forma_głowy()
            for okolicznik in w_zakresie(
                czytanie, OKOLICZNIK_ZDANIOWY, DEKLARACJA.podrzędne, zakres
            ):
                imiesłów = _imiesłów(okolicznik)
                if imiesłów is not None:
                    znalezione.setdefault((imiesłów, orzeczenie), None)
    return tuple(Imiesłów(*para) for para in znalezione)


def _imiesłów(okolicznik: Node) -> str | None:
    """Forma imiesłowu, którym ten okolicznik orzeka, albo nic, gdy orzeka czym innym.

    Głowa deklarowana produkcją, a nie dowolny imiesłów pod tym symbolem:
    ten sam symbol niesie okolicznik wyrażony zdaniem — `Trzeba wdrożyć ją
    szybko, aby jej efekty były widoczne.` — a tamto zdanie ma własny podmiot,
    więc imiesłów zagnieżdżony w nim pożycza podmiot stamtąd, a nie stąd.
    Ceną jest milczenie nad ciałem dopisanym później, które imiesłów czymś
    opakuje, czyli pomyłka w stronę zgłoszenia niewydanego, a nie wymyślonego.
    Głębiej po głowie się nie schodzi, bo pod imiesłowem stoi jego przeczenie
    i cząstka zwrotna (``olski/subset/podrzędne.py``).
    """
    głowa = okolicznik.children[okolicznik.głowa]
    if isinstance(głowa, Node) and głowa.label == IMIESŁÓW_PRZYSŁÓWKOWY:
        return głowa.forma_głowy()
    return None
