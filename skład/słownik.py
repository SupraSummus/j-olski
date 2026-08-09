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

Zwykłe konstrukcje Pythona są tu częścią zapisu, a nie obejściem.
Zmienna nazywa poddrzewo i pozwala postawić je w dwóch zdaniach.
Funkcja jest wzorcem zdania, a funkcja zwracająca listę jest wzorcem akapitu.
Lista wchodzi do zdania przez ``razem``, więc człony koordynacji
mogą powstać z tego, co program dopiero policzył.
Nic z tego nie jest osobnym mechanizmem tej biblioteki
i to jest cała jej odpowiedź na pytanie, skąd wziąć powtórzenie i abstrakcję.
"""

from __future__ import annotations

from dataclasses import dataclass

from skład.składnia import (
    Byt,
    Jaki,
    Jest,
    Nominalne,
    Okolicznik,
    Przysłówek,
    Rola,
    Rzecz,
    Wyróżnienie,
    byt,
    nie,
    zdarzenie,
)

__all__ = [
    "A",
    "D",
    "Dokąd",
    "Gdzie",
    "R",
    "Skąd",
    "V",
    "czym",
    "jest",
    "nie",
    "nowe",
    "razem",
    "temat",
]


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
    """Czasownik jako wywołanie wraz z rolami: zapisywać przez kogo i co.

    Rozdzielaniem argumentów zajmuje się ``zdarzenie`` w ``skład.składnia``,
    bo to jest składanie drzewa, a nie nazywanie go,
    i tutaj zostaje samo wzięcie lematu z nazwy atrybutu.
    """

    def __getattr__(self, nazwa: str):
        if nazwa.startswith("_"):
            raise AttributeError(nazwa)
        lemat = _lemat(nazwa)
        return lambda kto, *reszta: zdarzenie(kto, lemat, *reszta)


class Okoliczności:
    """Przyimek jako nazwa, w relacji, którą ta przestrzeń nazw trzyma.

    Relacja jest tu wybrana raz, przy nazwie, bo to ona jest kategorią dziedziny,
    a przyimek jest tylko słowem, które tę relację po polsku wyraża.
    ``Gdzie.w`` i ``Dokąd.w`` są więc dwiema różnymi rzeczami do powiedzenia,
    choć piszą się jednym przyimkiem.
    """

    def __init__(self, relacja: str) -> None:
        self._relacja = relacja

    def __getattr__(self, nazwa: str):
        if nazwa.startswith("_"):
            raise AttributeError(nazwa)
        przyimek = _lemat(nazwa)
        return lambda co: Okolicznik(przyimek, self._relacja, byt(co))


#: Rzeczowniki, przymiotniki, czasowniki i przysłówki, każde pod jedną literą,
#: bo w drzewie stoją gęsto i nazwa dłuższa przykryłaby to, co drzewo mówi.
R = Słownik(Rzecz)
A = Słownik(Cecha)
V = Czyny()
D = Słownik(Przysłówek)

#: Relacje okolicznikowe, każda pod swoim pytaniem, bo pytaniem się je rozróżnia.
Gdzie = Okoliczności("miejsce")
Dokąd = Okoliczności("cel")
Skąd = Okoliczności("źródło")


def czym(co: Nominalne | Rola) -> Okolicznik:
    """Narzędzie, czyli okolicznik, którego polszczyzna nie poprzedza przyimkiem."""
    return Okolicznik("", "narzędzie", byt(co))


def razem(elementy) -> Rola:
    """Lista jako koordynacja: to, co w Pythonie stoi obok siebie, stoi obok siebie i w zdaniu.

    Zapis ten zarabia na siebie tam, gdzie człony powstają z listy,
    bo ``&`` żąda ich wypisania jeden po drugim
    i nie ma jak wziąć ich z czegoś, co program dopiero policzył.
    """
    człony = list(elementy)
    wynik = byt(człony[0])
    for element in człony[1:]:
        wynik = wynik & element
    return wynik


def temat(co) -> Wyróżnienie:
    """To, o czym zdanie jest: staje na czele."""
    return Wyróżnienie(byt(co), "czoło")


def nowe(co) -> Wyróżnienie:
    """To, co zdanie dokłada: staje na końcu."""
    return Wyróżnienie(byt(co), "koniec")


def jest(co: Nominalne | Rola, czym: Nominalne | Rola) -> Jest:
    """Orzeczenie imienne wraz z domyślnością, że rzecz znaczy jeden egzemplarz."""
    return Jest(co=byt(co), czym=byt(czym))
