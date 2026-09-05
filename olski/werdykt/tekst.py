"""Werdykt o całym tekście: wpis na zdanie oraz jedna odpowiedź policzona z wpisów.

Wejścia są dwa: :func:`check` oddaje same werdykty,
a :func:`nad_tekstem` dokłada do każdego z nich to, czego z jednego zdania nie widać.
Werdykt o zdaniu przychodzi tu gotowy, a ten moduł zamyka import pakietu.
"""

from __future__ import annotations

import collections
from collections.abc import Sequence
from dataclasses import dataclass

from olski.grammar import Grammar
from olski.odniesienia import Odniesienie, niejasne_odniesienia
from olski.rozstrzyganie import Sąsiedztwo, sąsiedztwa
from olski.segmentacja import morphology, sentences
from olski.werdykt.zdanie import Verdict, werdykt

#: Nazwy zgłoszeń, tak jak pisze je czytelnik bazy sądów i jak liczy je
#: podsumowanie. Krotka, bo kolejność jest kolejnością wydruku.
WIELOZNACZNE = "wieloznaczne"
POPRAWKA = "poprawka jednego znaku"
ODNIESIENIE = "niejasne odniesienie"

#: Nazwa zgłoszenia spod flagi ``w_zdaniu`` (``olski/odniesienia.py``): rzeczy
#: stoją w zdaniu zaimka, a nie w zdaniu obok. Nazwa jest osobna, bo baza sądów
#: ocenia dwie reguły i mieszać ich nie wolno: tamtej sądów jeszcze nie ma,
#: a ta czeka na awans. Podsumowanie tego zgłoszenia nie liczy i kod wyjścia go
#: nie widzi (:data:`ZNALEZISKA`), więc flaga nie rusza ani jednej liczby.
ODNIESIENIE_W_ZDANIU = "niejasne odniesienie w zdaniu"

ZGŁOSZENIA = (
    WIELOZNACZNE,
    POPRAWKA,
    ODNIESIENIE,
    ODNIESIENIE_W_ZDANIU,
)

#: Te zgłoszenia, które są znaleziskiem, czyli mówią autorowi, co poprawić.
#: Wieloznaczności tu nie ma, bo baza sądów nie potwierdziła ani jednego jej
#: zgłoszenia (docs/subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem);
#: wraca tu kształtem, który baza potwierdzi, a nie całością.
ZNALEZISKA = (POPRAWKA, ODNIESIENIE)


def check(text: str, grammar: Grammar | None = None) -> list[Verdict]:
    """Check every sentence of a text against the grammar.

    Bare verdicts and nothing else:
    what the surrounding text adds comes with :func:`nad_tekstem`.
    """
    return [werdykt(zdanie, morphology(zdanie), grammar) for zdanie in sentences(text)]


@dataclass(frozen=True)
class Zdanie:
    """Jedno zdanie tekstu: werdykt o nim wraz z tym, co dokłada tekst wokół.

    Werdykt orzeka o samym zdaniu, a dwa pozostałe pola biorą się z akapitu,
    bo zdanie samo nie wie, co stoi przed nim.
    """

    werdykt: Verdict
    #: Zdania, które w tym akapicie stoją przed tym; czyta je ``olski/rozstrzyganie.py``.
    sąsiedztwo: Sąsiedztwo
    #: Zaimki wskazujące na dwie rzeczy naraz, drugie ze znalezisk (``olski/odniesienia.py``).
    odniesienia: tuple[Odniesienie, ...]

    @property
    def zgłoszenia(self) -> tuple[str, ...]:
        """Nazwy zgłoszeń, które olski ma o tym zdaniu, w kolejności :data:`ZGŁOSZENIA`.

        Jedno miejsce mówi, co olski nad zdaniem zgłasza: liczy z niego
        :class:`Podsumowanie` i ocenia je baza sądów (``harness/sądy.py``).
        Napis niepunktowany nie ma żadnego, jak w :attr:`Verdict.zgłoszenie`.
        """
        if not self.werdykt.punktowane:
            return ()
        obecne = {
            WIELOZNACZNE: bool(self.werdykt.result.ambiguous),
            POPRAWKA: self.werdykt.naprawa is not None,
            ODNIESIENIE: any(not o.w_zdaniu for o in self.odniesienia),
            ODNIESIENIE_W_ZDANIU: any(o.w_zdaniu for o in self.odniesienia),
        }
        return tuple(nazwa for nazwa in ZGŁOSZENIA if obecne[nazwa])

    @property
    def znaleziska(self) -> tuple[str, ...]:
        """Te ze zgłoszeń, które są znaleziskiem (:data:`ZNALEZISKA`)."""
        return tuple(nazwa for nazwa in self.zgłoszenia if nazwa in ZNALEZISKA)


def nad_tekstem(text: str, w_zdaniu: bool = False) -> list[Zdanie]:
    """Co narzędzie ma do powiedzenia o tekście: wpis na zdanie, w kolejności zdań.

    Wejście jest jedno na oba wyjścia — wiersz poleceń (``olski/check.py``)
    i witrynę (``witryna/werdykty.py``) — bo różnią się one brzegiem, a nie
    środkiem: pierwsze drukuje wiersze, drugie składa JSON. Znalezisko dopisane
    następne dochodzi przez to w jednym miejscu i w jednym się liczy
    (:meth:`Podsumowanie.ze_zdań`).

    ``w_zdaniu`` przepuszcza flagę do warstwy zaimkowej i pyta o nią sonda
    oceniająca, a nie wydruk (``olski/odniesienia.py``).

    Sąsiedztwa liczą się zawsze, choć wiersz poleceń pyta o warstwę
    rozstrzygającą dopiero pod flagą: obok rozbioru nie kosztują nic, bo tną
    tekst na zdania, a słowa liczą w nich dopiero pod świadkiem
    (:class:`olski.rozstrzyganie.Sąsiedztwo`).
    """
    werdykty = check(text)
    return [
        Zdanie(verdict, sąsiedztwo, odniesienia)
        for verdict, sąsiedztwo, odniesienia in zip(
            werdykty,
            sąsiedztwa(text),
            niejasne_odniesienia(text, [verdict.result for verdict in werdykty], w_zdaniu),
            strict=True,
        )
    ]


@dataclass(frozen=True)
class Podsumowanie:
    """Znaleziska nad tekstem i to, o czym olski milczy, dla tego, kto pyta o cały tekst.

    Liczby te wychodzą z wpisów jedną regułą — fragment nie jest zdaniem, więc
    nie wchodzi do mianownika, a zdanie odrzucone jest milczeniem, dopóki nie ma
    poprawki — i pyta o nie więcej niż jeden wołający, więc policzone u każdego z
    nich rozjeżdżają się po cichu: mianownik mniejszy o fragment czyta się jak
    pomiar, a nie jak pomyłka.

    Zdanie naprawialne stoi w dwóch licznikach naraz, w :attr:`naprawialne` i w
    :attr:`bez_odczytania`, bo gramatyka go nie wyprowadza i pokrycie liczy je
    tak samo jak przedtem: znalezisko mówi o autorze, a nie o podzbiorze.
    """

    #: Zdania, czyli to, o czym werdykt orzeka: fragmentów nie ma tu ani w liczniku.
    zdań: int
    #: Zdania o kilku odczytaniach. Liczba mówi, ile zdań olski czyta na kilka
    #: sposobów, a znaleziskiem nie jest i do :attr:`znalezisk` nie wchodzi.
    wieloznaczne: int
    #: Zdania, które od odczytania dzieli jeden znak, czyli pierwsze ze znalezisk
    #: (:class:`Naprawa`). Liczba jest osobna od :attr:`wieloznaczne`, bo mówi o
    #: zdaniu rzecz przeciwną: tamto olski czyta i ma o nim za dużo do
    #: powiedzenia, a to zdanie czyta dopiero po poprawce.
    naprawialne: int
    #: Zdania, których gramatyka nie wyprowadza. Olski o nich milczy, a milczenie
    #: liczy się osobno, bo bez tej liczby przebieg nad tekstem, którego nie
    #: przeczytał, czytałby się jak czysty.
    bez_odczytania: int
    #: Napisy, których nic nie interpunkuje jako zdania. Liczba jest jedna na oba
    #: werdykty o takim napisie, :data:`FRAGMENT` i :data:`NIEDOMKNIĘTE`, bo o
    #: mianowniku rozstrzyga jedno i to samo: domknięcia nie postawił nikt.
    fragmentów: int
    #: Zdania z zaimkiem, który wskazuje na dwie rzeczy naraz, czyli drugie ze
    #: znalezisk (``olski/odniesienia.py``). Zdanie wieloznaczne z takim zaimkiem
    #: stoi w dwóch licznikach naraz, tak samo jak zdanie naprawialne, i z tego
    #: samego powodu: liczby mówią o zdaniu co innego.
    niejasnych_odniesień: int

    @property
    def znalezisk(self) -> int:
        """Ile znalezisk narzędzie ma nad tekstem, bez względu na to, które.

        Pyta o to kod wyjścia (``olski/check.py``), bo o samym znalezisku
        rozstrzyga tu jedno miejsce, a znalezisko dopisane później dostaje ten
        kod wyjścia razem z własnym licznikiem. Wieloznaczność do tej liczby nie
        wchodzi (:data:`ZNALEZISKA`).
        """
        return self.naprawialne + self.niejasnych_odniesień

    @classmethod
    def ze_zdań(cls, zdania: Sequence[Zdanie]) -> Podsumowanie:
        """Podsumowanie tych zdań, choćby przyszły z kilku plików naraz."""
        punktowane = [wpis.werdykt for wpis in zdania if wpis.werdykt.punktowane]
        ile = collections.Counter(nazwa for wpis in zdania for nazwa in wpis.zgłoszenia)
        return cls(
            zdań=len(punktowane),
            wieloznaczne=ile[WIELOZNACZNE],
            naprawialne=ile[POPRAWKA],
            bez_odczytania=sum(verdict.result.rejected for verdict in punktowane),
            fragmentów=len(zdania) - len(punktowane),
            niejasnych_odniesień=ile[ODNIESIENIE],
        )

    def explain(self) -> str:
        #  Wiersz jest listą par, a nie zdaniem: liczba stoi za dwukropkiem, więc
        #  nie żąda zgody od słowa przed sobą i nic tu się nie odmienia.
        podsumowanie = (
            f"zdań: {self.zdań}; wieloznaczne: {self.wieloznaczne};"
            f" bez odczytania: {self.bez_odczytania}"
        )
        #  Wiersz rośnie o tę parę dopiero tam, gdzie poprawka pada, bo nad
        #  tekstem bez ani jednej mówiłaby zero o znalezisku, którego nie ma.
        if self.naprawialne:
            podsumowanie += f"; do poprawki jednym znakiem: {self.naprawialne}"
        #  Ta para rośnie pod tym samym warunkiem i z tego samego powodu.
        if self.niejasnych_odniesień:
            podsumowanie += f"; niejasne odniesienia: {self.niejasnych_odniesień}"
        if self.fragmentów:
            #  Nie „fragmenty, które nie są zdaniami”: napis niedomknięty jest w tej
            #  liczbie, a werdykt nad nim mówi, że olski to zdanie czyta.
            podsumowanie += f"; fragmenty, których nic nie punktuje jako zdania: {self.fragmentów}"
        return podsumowanie
