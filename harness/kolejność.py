"""Czy czytanie pierwsze przyłącza frazę do gospodarza przeczytanego ręką.

Koszt porządkuje czytania, a nad własnym rejestrem nie ma czym tego porządku
sprawdzić: bank drzew niesie czytanie złote, proza nie niesie żadnego
(docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie).
Wzorzec jest jeden i jest nim ``próba/wybory.txt``: przy pozycji przyłączeniowej
korpusu audytowego nazywa on ręką gospodarza, o którego w tym tekście chodziło.
O tego gospodarza pyta warstwę rozstrzygającą ``harness/wybory.py``, a
kolejność pyta o niego ta sonda: czy fraza dochodzi do niego w czytaniu
wypisanym u góry wydruku.

Odpowiedź bierze się z drzewa, a nie z jego streszczenia, choć czytelnik czyta
streszczenie: streszczenie nazywa gospodarza pierwszej roli przyłączanej w
zdaniu składowym i milczy o okoliczniku drugim oraz o przyłączeniu wewnątrz
konstytuenta (``olski/parse/streszczenie.py``), a wzorzec pyta o pozycje jednego
i drugiego rodzaju. Gospodarza nazywa przy tym ta sama funkcja, z której bierze
go wydruk (``gospodarz`` w tamtym module), bo dwa odczyty jednej reguły
rozeszłyby się po cichu.

Mianownik jest mały i jest to cena, którą ten pomiar płaci za rejestr: zdania
korpusu audytowego są długie, a olski czyta z nich garść. Liczba stąd nie jest
przez to stopą trafień; sonda jest świadkiem przy zmianie ceny i wypisuje wpis
po wpisie, żeby czytający zobaczył, w którą stronę przestawienie poszło.
Powiększa ten mianownik gramatyka, a nie następne losowanie.

Plik podaje się jeden, bo mianownik należy do losowania (``harness/wybory.py``).

    python3 -m harness.kolejność
    python3 -m harness.kolejność próba/wybory-z-odpowiedzią.txt
"""

from __future__ import annotations

import argparse
import collections
import sys
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path

from harness.wybory import DO_PRZEMILCZENIA, PUSTY, WYBORY, Wybór, czytaj
from olski.parse.czytanie import Node
from olski.parse.streszczenie import gospodarz, sklej_formy
from olski.segmentacja import morphology, sentences
from olski.subset import GRAMMAR
from olski.subset.deklaracja import DEKLARACJA
from olski.werdykt import werdykt

#: Czytanie pierwsze przyłącza frazę do gospodarza, którego nazwał czytający.
TRAFNA = "trafna"

#: Przyłącza ją do innego, więc u góry wydruku stoi czytanie, którego czytelnik
#: nie wybrał.
POMYŁKA = "pomyłka"

#: Zdanie jest czytane, a fraza z wzorca konstytuentem tego czytania nie jest:
#: czytanie bierze konstytuent dłuższy albo krótszy, więc gospodarza nie ma z
#: czym porównać. Ręka poprawia we wzorcu i frazę, i gospodarza
#: (``harness/wybory.py``), a fraza poprawiona bywa krótsza od tej, którą
#: wypisuje morfologia.
INNY_KONSTYTUENT = "inny konstytuent"

#: Zdania olski nie czyta, więc czytania pierwszego nie ma.
NIECZYTANE = "nieczytane"

#: Klasy sądu w kolejności wydruku. Krotka, a nie zbiór, bo zbiór postawiony na
#: drodze do wydruku wypisuje w każdym przebiegu co innego.
KLASY = (TRAFNA, POMYŁKA, INNY_KONSTYTUENT, NIECZYTANE)


@dataclass(frozen=True)
class Sąd:
    """Co czytanie pierwsze mówi o jednym wyborze przeczytanym ręką."""

    wybór: Wybór
    klasa: str
    #: Gospodarz z czytania pierwszego; pusty, gdy frazy nie ma w tym czytaniu.
    gospodarz: str = ""


def z_gospodarzem(wybory: Iterable[Wybór]) -> list[Wybór]:
    """Te wpisy, które nazywają gospodarza, czyli mianownik tej sondy.

    Wpis ``oba`` i wpis ``żadne`` mówią, że wyboru nie ma, a wpis bez wzorca nie
    mówi nic (``harness/wybory.py``), więc kolejność nie ma nad żadnym z nich
    czego trafić. Milczenie warstwy było nad nimi odpowiedzią trafną, a
    kolejność milczeć nie umie: czytanie przyłącza frazę zawsze.
    """
    return [
        wybór
        for wybór in wybory
        if wybór.wzorzec != PUSTY and wybór.wzorzec not in DO_PRZEMILCZENIA
    ]


def osądź(wybór: Wybór) -> Sąd:
    """Zapytaj olskiego o zdanie tego wpisu i zestaw czytanie pierwsze z wzorcem.

    Zdania wpisu wyznacza ``sentences``, a nie sam napis z pliku, i idą one
    pętlą: wpis niesie jedno zdanie korpusu i tak go zbudowano, a podział jest
    tu ten sam, którego używa werdykt.
    """
    czytane = False
    for napis in sentences(wybór.zdanie):
        drzewo = _czytanie_pierwsze(napis)
        if drzewo is None:
            continue
        czytane = True
        znaleziony = _gospodarz_frazy(drzewo, wybór.fraza)
        if znaleziony is not None:
            return Sąd(wybór, TRAFNA if znaleziony == wybór.wzorzec else POMYŁKA, znaleziony)
    return Sąd(wybór, INNY_KONSTYTUENT if czytane else NIECZYTANE)


def _czytanie_pierwsze(napis: str) -> Node | None:
    """Drzewo czytania pierwszego tego zdania; ``None``, gdy olski go nie czyta.

    Pierwsze z lasu, czyli to, którego streszczenie stoi u góry wydruku
    (``Verdict.readings`` w ``olski/werdykt/zdanie.py`` grupuje po streszczeniu i
    kolejności pierwszego wystąpienia nie rusza).

    O zatrzymanie się nie pyta, bo tej sondzie nie mówi ono nic, a kosztuje
    drugie przejście tablicy; czym stanęło odrzucenie, mówi ``olski-check``.
    """
    wynik = werdykt(napis, morphology(napis), GRAMMAR, zatrzymanie=False)
    return wynik.result.readings[0] if wynik.result.ile else None


def _gospodarz_frazy(drzewo: Node, fraza: str) -> str | None:
    """Gospodarz konstytuenta o tych formach; ``None``, gdy takiego w drzewie nie ma.

    Dopasowanie idzie po całej frazie, więc fraza wzorca stojąca w środku
    konstytuenta wychodzi stąd bez odpowiedzi: gospodarz konstytuenta szerszego
    odpowiada na inne pytanie niż to, które zadał czytający, i porównany z
    wzorcem wydawałby pomyłki tam, gdzie czytanie przyłącza dobrze.
    Konstytuent bierze się najszerszy z pasujących, bo pod przyłączeniem idzie
    łańcuch węzłów o jednej córce i tej samej rozpiętości.
    """
    szukana = _ściśnięta(fraza)
    for węzeł in _węzły(drzewo):
        if _ściśnięta(sklej_formy(węzeł.forms())) == szukana:
            return gospodarz(drzewo, węzeł, DEKLARACJA.gospodarze)
    return None


def _węzły(drzewo: Node) -> Iterator[Node]:
    """Węzły tego drzewa, od korzenia w dół, rodzic przed córkami."""
    yield drzewo
    for dziecko in drzewo.children:
        if isinstance(dziecko, Node):
            yield from _węzły(dziecko)


def _ściśnięta(napis: str) -> str:
    """Ten napis o odstępach ściśniętych do jednego, bo frazę wzorca pisze ręka."""
    return " ".join(napis.split())


def wydruk(sądy: Sequence[Sąd]) -> str:
    """Liczby klas, a pod nimi wpis po wpisie, bo kierunek czyta człowiek.

    Zero wypisane, a nie pominięte: klasa, do której nie wpadł ani jeden wpis,
    jest odpowiedzią o tym rejestrze. Wpisu nieczytanego wydruk nie wypisuje —
    sonda nie ma o nim nic do powiedzenia poza tym, że nie wchodzi do liczb.
    """
    ile = collections.Counter(sąd.klasa for sąd in sądy)
    szerokość = max(len(klasa) for klasa in KLASY)
    wiersze = [f"{len(sądy)} wyborów z gospodarzem przeczytanym ręką", ""]
    wiersze += [f"  {ile[klasa]:>4}  {klasa}" for klasa in KLASY]
    wypisy = [_wypis(sąd, szerokość) for sąd in sądy if sąd.klasa != NIECZYTANE]
    if wypisy:
        wiersze += ["", "  wpis po wpisie:", *wypisy]
    return "\n".join(wiersze)


def _wypis(sąd: Sąd, szerokość: int) -> str:
    dokąd = f" → „{sąd.gospodarz}”" if sąd.gospodarz else ""
    return (
        f"  {sąd.klasa:>{szerokość}}  „{sąd.wybór.fraza}”{dokąd}, "
        f"wzorzec: {sąd.wybór.wzorzec}\n    {sąd.wybór.zdanie}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.kolejność",
        description="Zestaw czytanie pierwsze z gospodarzem przeczytanym ręką.",
    )
    parser.add_argument(
        "plik",
        nargs="?",
        help=f"plik z wyborami (domyślnie {WYBORY.parent.name}/{WYBORY.name})",
    )
    args = parser.parse_args(argv)
    path = Path(args.plik) if args.plik else WYBORY
    if not path.is_file():
        print(f"harness.kolejność: nie ma takiego pliku: {path}", file=sys.stderr)
        return 2
    print(wydruk([osądź(wybór) for wybór in z_gospodarzem(czytaj(path))]))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
