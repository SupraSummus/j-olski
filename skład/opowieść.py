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

Opuszczenie jest wąskie i jest wąskie z rozmysłu:
opuszczenie, po którym zdanie czyta się dwojako, nie jest oszczędnością,
i jest to ta sama ostrożność, którą po drugiej stronie ma kryterium jednego czytania.
Warunki trzyma ``pomijalny`` w ``skład/składnia.py``, a nie ten moduł,
bo stawia je także ciąg zdarzeń wewnątrz jednego zdania.
Akapit dokłada do nich jeden własny i jest to jego cała rola w tej regule:
zdanie o kimś, o kim mowa była wcześniej, ale nie w zdaniu obok,
dostaje pełną nazwę, a akapit jest tym, w czym „obok” się kończy.
"""

from __future__ import annotations

from skład.składnia import TERAZ, Kontekst, Rola, byt, kompiluj, pomijalny


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

    def linearyzuj(self, case: str, kontekst: Kontekst = TERAZ) -> str:
        return self.kto.linearyzuj(case, kontekst)


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
    także wtedy, gdy akapit poprzedni skończył się na tej samej postaci,
    i tyle akapit o opuszczeniu rozstrzyga:
    resztę warunków stawia ``pomijalny`` w ``skład/składnia.py``.
    """

    def __init__(self, *zdania) -> None:
        self.zdania = tuple(_rozwiń(zdania))

    def kompiluj(self, czas: str) -> str:
        wypisane = []
        poprzednie = None
        for zdanie in self.zdania:
            pomijany = pomijalny(zdanie, poprzednie, czas)
            wypisane.append(kompiluj(zdanie, Kontekst(czas=czas, pomijany=pomijany)))
            poprzednie = zdanie
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
