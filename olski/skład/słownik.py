"""Przestrzenie nazw nad składnią: lemat jako nazwa, a nie jako łańcuch.

Przestrzenie te są całą zdejmowalną warstwą tego pakietu.
Operatory stoją w ``olski.skład.składnia``, bo są zapisem konstruktorów,
a tutaj zostaje to, co da się odjąć, nie tracąc języka.
Import tego modułu nie zmienia zachowania tamtego i tę własność trzyma test.

Zdanie zostaje wywołaniem, choć grupa imienna dostaje operatory.
Powód jest jeden: zdanie ma role, a role czyta się z nazw.
Zapis operatorowy kazałby czytać je z kolejności
oraz z pierwszeństwa działań, którego ten język nie projektował.

Nazw nie brakuje za to łańcuchowi metod po zdaniu,
czyli zapisowi ``V.zejść(kto).którędy_po(~R.schody)``, i on odpada z dwóch powodów.
Relacja i słowo są dwiema osiami, które autor wybiera osobno,
bo ``Gdzie.w`` i ``Dokąd.w`` są dwiema rzeczami do powiedzenia
pisanymi jednym przyimkiem,
a nazwa metody zwija te osie w jedną listę nazw w rodzaju ``gdzie_w``.
Drugiego nie widać w zapisie, tylko w tym, co z nim robi ``ruff format``:
znacznik tematu nie ma w takim łańcuchu czego wyróżnić poza tym,
co dopisano ostatnio, więc staje się pozycyjny,
a formater dokleja go do wywołania następnego,
i wtedy źródło wyróżnia co innego, niż wygląda, że wyróżnia.
Znacznik przyrostkowy tego nie ma, bo nie sięga poza konstytuent, przy którym stoi,
i stoi razem z operatorami w ``olski.skład.składnia``.

Wielka litera odróżnia tu kategorię od funkcji, która coś nad argumentem liczy.
Funkcja składa listę, zwija człon do samego siebie albo dokłada domyślną liczbę,
a kategoria mówi tylko, czym konstytuent jest, więc zostaje klasą wołaną wprost:
druga nazwa dla jednego konstruktora nie kupiłaby nic poza małą literą.

Zwykłe konstrukcje Pythona są tu częścią zapisu, a nie obejściem.
Zmienna nazywa poddrzewo i pozwala postawić je w dwóch zdaniach.
Funkcja jest wzorcem zdania, a funkcja zwracająca listę jest wzorcem akapitu.
Lista wchodzi do zdania przez ``razem``, więc człony koordynacji
mogą powstać z tego, co program dopiero policzył.
Zwykły Python jest całą odpowiedzią tej biblioteki na pytanie,
skąd wziąć powtórzenie i abstrakcję.
"""

from __future__ import annotations

from dataclasses import dataclass

from olski.skład.składnia import (
    Byt,
    Ciąg,
    Jaki,
    Jest,
    Komu,
    Nominalne,
    Okolicznik,
    Opis,
    Przysłówek,
    Rola,
    Rzecz,
    Treść,
    byt,
    nie,
    zdarzenie,
)

__all__ = [
    "A",
    "Czym",
    "D",
    "Dlaczego",
    "Dokąd",
    "Gdzie",
    "Kiedy",
    "Którędy",
    "R",
    "Skutek",
    "Skąd",
    "Treść",
    "V",
    "jest",
    "komu",
    "nie",
    "opis",
    "potem",
    "razem",
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

    Rozdzielaniem argumentów zajmuje się ``zdarzenie`` w ``olski.skład.składnia``,
    bo to jest składanie drzewa, a nie nazywanie go,
    i tutaj zostaje samo wzięcie lematu z nazwy atrybutu.
    """

    def __getattr__(self, nazwa: str):
        if nazwa.startswith("_"):
            raise AttributeError(nazwa)
        lemat = _lemat(nazwa)
        return lambda kto, *reszta: zdarzenie(kto, lemat, *reszta)


class Okoliczności:
    """Słowo jako nazwa, w relacji, którą ta przestrzeń nazw trzyma.

    Relacja jest tu wybrana raz, przy nazwie, bo to ona jest kategorią dziedziny,
    a przyimek albo spójnik jest tylko słowem, które tę relację po polsku wyraża.
    ``Gdzie.w`` i ``Dokąd.w`` są więc dwiema różnymi rzeczami do powiedzenia,
    choć piszą się jednym przyimkiem.

    Relację bez słowa pisze się wywołaniem samej przestrzeni nazw,
    bo polszczyzna wyraża część relacji samym przypadkiem:
    ``Czym(R.lustro)`` daje `lustrem`, a ``Kiedy(R.wieczór)`` daje `wieczorem`.
    Osobnej funkcji na to nie ma i nie ma być:
    relacja bez przyimka jest tą samą kategorią co z nim,
    a każda taka funkcja byłaby drugą drogą do jednego konstruktora.

    Rzecz i zdarzenie wchodzą jedną drogą, bo pytanie stawia się jedno:
    ``Kiedy.w(R.noc)`` i ``Kiedy.gdy(V.zgasnąć(świeca))`` mówią, kiedy.
    Nic tu tych dwóch nie rozdziela, bo ``byt`` przepuszcza wszystko,
    co rzeczą nie jest, a co ze słowem zrobić, wie ``Okolicznik``.
    """

    def __init__(self, relacja: str) -> None:
        self._relacja = relacja

    def __call__(self, co) -> Okolicznik:
        return Okolicznik("", self._relacja, byt(co))

    def __getattr__(self, nazwa: str):
        if nazwa.startswith("_"):
            raise AttributeError(nazwa)
        słowo = _lemat(nazwa)
        return lambda co: Okolicznik(słowo, self._relacja, byt(co))


#: Rzeczowniki, przymiotniki, czasowniki i przysłówki, każde pod jedną literą,
#: bo w drzewie stoją gęsto i nazwa dłuższa przykryłaby to, co drzewo mówi.
R = Słownik(Rzecz)
A = Słownik(Cecha)
V = Czyny()
D = Słownik(Przysłówek)

#: Relacje okolicznikowe, każda pod swoim pytaniem, bo pytaniem się je rozróżnia.
#: Pytanie jest jedno dla rzeczy i dla zdarzenia,
#: więc ``Kiedy`` trzyma i ``w nocy``, i ``gdy zgasła świeca``.
Gdzie = Okoliczności("miejsce")
Dokąd = Okoliczności("cel")
Skąd = Okoliczności("źródło")
Którędy = Okoliczności("droga")
Kiedy = Okoliczności("czas")
Dlaczego = Okoliczności("przyczyna")

#: Narzędzie, czyli relacja, której polszczyzna nie poprzedza przyimkiem nigdy,
#: więc jej przestrzeń nazw wywołuje się, a nie sięga po słowo.
Czym = Okoliczności("narzędzie")

#: Skutek pytania jednym słowem nie ma, więc nazywa się relacją:
#: tyle jest w tej konwencji nazw, ile jest w niej pytań.
Skutek = Okoliczności("skutek")


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


def potem(*zdarzenia) -> Ciąg:
    """Zdarzenia jednym zdaniem, w kolejności, w której się stały.

    Nazwa mówi o następstwie, a nie o spójniku, bo tyle autor rozstrzyga:
    że jedno stało się po drugim i że jest to jedna rzecz do opowiedzenia.
    Że wyjdzie z tego ``i``, a podmiot wyjdzie raz, rozstrzyga ``Ciąg``.

    Jedno zdarzenie przechodzi tędy nietknięte, tak samo jak jeden byt przez
    ``razem``: następstwo, w którym nic po niczym nie następuje, jest samym zdarzeniem.
    """
    return Ciąg(zdarzenia) if len(zdarzenia) > 1 else zdarzenia[0]


def opis(rzecz: Rola, zdanie) -> Opis:
    """Rzecz wraz ze zdarzeniem, które mówi, o którą rzecz chodzi.

    Rzecz stoi tu dwa razy: raz jako ta opisywana, a raz w zdaniu, które ją opisuje,
    i to drugie wystąpienie jest tym, co wyjdzie zaimkiem.
    Zapisu na to nie ma, bo zapisem jest zmienna:
    ta sama zmienna postawiona w obu miejscach jest tą samą rzeczą,
    a rzecz napisana dwa razy z osobna jest dwiema, jak wszędzie w tym pakiecie.
    """
    return Opis(byt(rzecz), zdanie)


def komu(kto: Nominalne | Rola) -> Komu:
    """Ten, komu zdarzenie się przydarza, wraz z domyślnością, że rzecz znaczy jeden egzemplarz.

    Funkcją, a nie kategorią wołaną wprost, z tego samego powodu co ``jest`` niżej:
    dokłada domyślną liczbę, a tyle wystarcza, żeby autor nie pisał jej sam.
    """
    return Komu(byt(kto))


def jest(
    co: Nominalne | Rola,
    czym: Nominalne | Rola,
    *okoliczności,
    czasownik: str = Jest.CZASOWNIK,
) -> Jest:
    """Orzeczenie imienne wraz z domyślnością, że rzecz znaczy jeden egzemplarz.

    Kopula jest tu argumentem nazwanym, bo autor wybiera ją rzadziej,
    niż pisze samo orzekanie: `zostawać` mówi o zmianie, a `być` o niej milczy.
    Okoliczności wchodzą tak jak do zdarzenia, czyli po tyle, ile autor postawi.
    """
    return Jest(
        co=byt(co),
        czym=byt(czym),
        czasownik=czasownik,
        okoliczniki=tuple(okoliczności),
    )
