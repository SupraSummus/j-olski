"""Przestrzenie nazw nad składnią: lemat jako nazwa, a nie jako łańcuch.

To jest cała zdejmowalna warstwa tego pakietu.
Operatory stoją w ``skład.składnia``, bo są zapisem konstruktorów,
a tutaj zostaje to, co naprawdę da się odjąć, nie tracąc języka.
Import tego modułu nie zmienia zachowania tamtego,
i to jest własność, którą trzyma test, a nie tylko ten akapit.

Zdanie zostaje wywołaniem, choć grupa imienna dostaje operatory.
Powód jest jeden: zdanie ma role, a role czyta się z nazw.
Zapis operatorowy kazałby czytać je z kolejności
oraz z pierwszeństwa działań, którego ten język nie projektował.
"""

from __future__ import annotations

from dataclasses import dataclass

from skład.składnia import Byt, Jaki, Jest, Nominalne, Robi, Rzecz, byt


@dataclass(frozen=True)
class Cecha:
    """Przymiotnik, dopóki nie wiadomo, czego dotyczy."""

    lemat: str

    def __mul__(self, inne):
        """Określenie: zwykły razy tekst daje zwykły tekst."""
        if isinstance(inne, Cecha):
            return Cechy((self, inne))
        if isinstance(inne, Byt):
            return Byt(Jaki(self.lemat, inne.rzecz), inne.number)
        return Jaki(self.lemat, inne)


@dataclass(frozen=True)
class Cechy:
    """Kilka przymiotników czekających na rzecz.

    Klasa jest tu dlatego, że mnożenie wiąże w lewo,
    więc dwa przymiotniki spotykają się ze sobą, zanim spotkają rzeczownik.
    """

    lematy: tuple[Cecha, ...]

    def __mul__(self, inne):
        if isinstance(inne, Cecha):
            return Cechy((*self.lematy, inne))
        wynik = inne
        for cecha in reversed(self.lematy):
            wynik = cecha * wynik
        return wynik


def _lemat(nazwa: str) -> str:
    """Jeden końcowy podkreślnik omija słowo kluczowe Pythona i z lematu znika.

    Ucinany jest dokładnie jeden, żeby lemat, który podkreślnik naprawdę niesie,
    dało się nadal napisać.
    """
    return nazwa[:-1] if nazwa.endswith("_") else nazwa


class Słownik:
    """Nazwa atrybutu jako lemat, zamiast lematu pisanego w cudzysłowie.

    Leksykon jest otwarty, bo otwarty jest słownik pod spodem,
    więc ta przestrzeń nazw nie ma listy i nie sprawdza niczego:
    forma, której SGJP nie zna, zgłasza się dopiero przy linearyzacji.
    """

    def __init__(self, buduj) -> None:
        self._buduj = buduj

    def __getattr__(self, nazwa: str):
        if nazwa.startswith("_"):
            raise AttributeError(nazwa)
        return self._buduj(_lemat(nazwa))


class Czyny:
    """Czasownik jako wywołanie wraz z rolami: zapisywać przez kogo i co."""

    def __getattr__(self, nazwa: str):
        if nazwa.startswith("_"):
            raise AttributeError(nazwa)
        lemat = _lemat(nazwa)

        def czyn(kto: Nominalne | Byt, co: Nominalne | Byt) -> Robi:
            return Robi(kto=byt(kto), czyn=lemat, co=byt(co))

        return czyn


#: Rzeczowniki, przymiotniki i czasowniki, każde pod jedną literą,
#: bo w drzewie stoją gęsto i nazwa dłuższa przykryłaby to, co drzewo mówi.
R = Słownik(Rzecz)
A = Słownik(Cecha)
V = Czyny()


def jest(co: Nominalne | Byt, czym: Nominalne | Byt) -> Jest:
    """Orzeczenie imienne wraz z domyślnością, że rzecz znaczy jeden egzemplarz."""
    return Jest(co=byt(co), czym=byt(czym))
