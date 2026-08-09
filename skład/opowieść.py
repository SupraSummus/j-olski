"""Tekst, a nie zdanie: co wie kompilator, który widzi zdania obok siebie.

Zdanie skompilowane osobno nie wie o niczym poza sobą,
więc wypisuje każdą rzecz pełną nazwą i stawia ją w czasie, w którym stoi samo.
Tekst wie dwie rzeczy więcej i obie zmieniają to, co wychodzi.

**Wie, kiedy to było.** Opowieść mówi o tym, co się stało,
więc czas przeszły jest własnością opowiadania, a nie któregokolwiek ze zdarzeń.
To samo drzewo opowiedziane jako to, co się dzieje, dałoby czas teraźniejszy,
i dlatego czasu nie ma w drzewie, tylko w ``Kontekst``.

**Wie, o kim mowa.** Podmiot powtórzony zdanie po zdaniu czyta się źle,
a polszczyzna ma na to zwykły sposób: opuszcza go,
bo osobę, liczbę i rodzaj niesie sam czasownik.
Opuszczenie wymaga tożsamości, czyli wiedzy, że dwa wystąpienia lematu
są tą samą rzeczą, a nie dwiema takimi samymi,
i tego jedno drzewo nie ma czym powiedzieć.
Niesie to ``Postać``, a rozstrzyga o tym zmienna, którą autor tej postaci nadał:
dwa razy napisany ``R.bazyliszek`` jest dwoma bazyliszkami,
a dwa razy użyta jedna ``Postać`` jest jednym.

Opuszczenie jest wąskie i jest wąskie z rozmysłu.
Podmiot znika tylko wtedy, gdy zdanie wcześniej miało ten sam podmiot
i gdy stoi ono w tym samym akapicie,
bo tyle wystarczy, żeby czytelnik nie miał na kogo innego trafić.
Zdanie o kimś, o kim mowa była wcześniej, ale nie przed chwilą,
dostaje pełną nazwę, i to jest ta sama ostrożność,
którą po drugiej stronie ma kryterium jednego czytania:
opuszczenie, po którym zdanie czyta się dwojako, nie jest oszczędnością.
"""

from __future__ import annotations

from skład.składnia import Kontekst, Rola, byt, kompiluj


class Postać(Rola):
    """Rzecz, do której tekst wraca, wraz z tożsamością, której lemat nie daje.

    Postacią jest to, co opowieść wymienia więcej niż raz.
    Rzecz wspomniana raz postaci nie potrzebuje i zostaje zwykłym bytem,
    więc ten konstruktor jest deklaracją autora, a nie kosztem płaconym wszędzie.

    Tożsamość jest tożsamością obiektu, bo taką daje zmienna w Pythonie,
    i to jest cały mechanizm: postać przypisana do nazwy
    i użyta pod tą nazwą dwa razy jest w obu miejscach tą samą.
    Dwie postaci o tym samym lemacie są dwiema różnymi rzeczami,
    i to też jest zamierzone: opowieść bywa o dwóch braciach.

    Czego to nie obejmuje, jest widać na drugim określeniu:
    ``bazyliszek`` i ``potwór`` są dla tego kompilatora dwiema rzeczami,
    bo tożsamość deklaruje autor, a nie słownik synonimów.
    """

    def __init__(self, kto) -> None:
        self.kto = byt(kto)

    @property
    def number(self) -> str:
        return self.kto.number

    @property
    def rodzaj(self) -> str:
        return self.kto.rodzaj

    @property
    def tożsamość(self) -> Postać:
        return self

    def linearyzuj(self, case: str) -> str:
        return self.kto.linearyzuj(case)


def _rozwiń(elementy):
    """Listy i krotki rozpakowane w miejscu, w którym stoją.

    Funkcja budująca kilka zdań naraz zwraca listę,
    a akapit ma je przyjąć tak, jakby autor wypisał je po kolei,
    bo inaczej każde takie miejsce trzeba by rozpakowywać gwiazdką ręcznie.
    """
    for element in elementy:
        if isinstance(element, (list, tuple)):
            yield from _rozwiń(element)
        else:
            yield element


class Akapit:
    """Ciąg zdarzeń opowiedzianych jedno po drugim.

    Akapit jest jednostką, w której podmiot da się opuścić,
    bo jest jednostką, w której czytelnik trzyma jeden wątek.
    Pierwsze zdanie akapitu wypisuje podmiot zawsze,
    także wtedy, gdy akapit poprzedni skończył się na tej samej postaci.
    """

    def __init__(self, *zdania) -> None:
        self.zdania = tuple(_rozwiń(zdania))

    def kompiluj(self, czas: str) -> str:
        wypisane = []
        poprzedni = None
        for zdanie in self.zdania:
            tożsamość = zdanie.podmiot.tożsamość
            pomijany = tożsamość if tożsamość is poprzedni else None
            wypisane.append(kompiluj(zdanie, Kontekst(czas=czas, pomijany=pomijany)))
            poprzedni = tożsamość
        return " ".join(wypisane)


class Opowieść:
    """Akapity o tym, co się stało.

    Czasu ten konstruktor nie przyjmuje i nie ma przyjmować.
    Opowieść jest z definicji mówieniem o tym, co już było,
    więc czas przeszły jest tu znaczeniem słowa, a nie ustawieniem;
    tekst o tym, co się dzieje, jest inną rzeczą i doczeka się innego konstruktora.
    """

    #: Czym opowieść jest wobec chwili, w której się ją opowiada.
    CZAS = "kiedyś"

    def __init__(self, *akapity: Akapit) -> None:
        self.akapity = akapity

    def kompiluj(self) -> str:
        return "\n\n".join(akapit.kompiluj(self.CZAS) for akapit in self.akapity)
