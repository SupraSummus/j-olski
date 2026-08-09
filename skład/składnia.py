"""Abstrakcyjna składnia: co da się powiedzieć, bez tego, jak to brzmi.

Kategoria mówi, jaki byt drzewo w tym miejscu trzyma,
a konstruktor mówi, co z czym wolno złożyć.
Drzewo dobrze złożone jest jednoznaczne z definicji,
więc jednoznaczność tego zapisu nie potrzebuje żadnego sprawdzenia:
kształt drzewa jest tym, co niesie znaczenie.

Poziomem tych kategorii jest dziedzina, a nie polszczyzna.
``Czyj`` mówi, że jedna rzecz jest określeniem drugiej,
a że wyjdzie z tego dopełniacz, rozstrzyga linearyzacja niżej.
Ten poziom jest tym, co odróżnia ten zapis od rozbioru zdania pisanego z góry;
wywód trzyma
``docs/design-notes.md``.

Czego drzewo nie niesie, jest tu decyzją, a nie brakiem.
Nie ma w nim przypadka, bo przypadek bierze się z pozycji.
Nie ma rodzaju, bo rodzaj rzeczownika jest leksykalny.
Nie ma szyku, i to jedno jest dziurą, a nie decyzją:
polszczyzna niesie szykiem temat i remat, więc jest co powiedzieć,
a ten zapis nie ma czym. Trzyma to ``TODO.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

from skład.morfologia import odmień, rodzaj_rzeczownika


class Nominalne:
    """Wszystko, co może stanąć w grupie imiennej, wraz z zapisem operatorowym.

    Operatory stoją tutaj, a nie warstwę wyżej, bo są zapisem konstruktorów,
    a nie drugim sposobem mówienia: ``a / b`` buduje dokładnie ``Czyj(a, byt(b))``.
    Zdejmowalną warstwą są same przestrzenie nazw w ``skład.słownik``.
    """

    def __truediv__(self, inne) -> Czyj:
        """Dopełniacz, czyli określenie po głowie: parser przez podzbiór."""
        return Czyj(self, byt(inne))

    def __invert__(self) -> Byt:
        """Liczba mnoga."""
        return Byt(self, "pl")


@dataclass(frozen=True)
class Rzecz(Nominalne):
    """Rodzaj bytu, bez rozstrzygnięcia, ile go i który."""

    lemat: str

    @property
    def rodzaj(self) -> str:
        return rodzaj_rzeczownika(self.lemat)

    def linearyzuj(self, case: str, number: str) -> str:
        return odmień(self.lemat, "subst", case=case, number=number)


@dataclass(frozen=True)
class Jaki(Nominalne):
    """Rzecz wraz z określeniem przymiotnikowym: zwykły tekst, dobry kod.

    Przymiotnik zgadza się z rzeczą w przypadku, liczbie i rodzaju,
    a wszystkie trzy przychodzą policzone: dwa z pozycji, rodzaj z leksykonu.
    """

    cecha: str
    rzecz: Nominalne

    @property
    def rodzaj(self) -> str:
        return self.rzecz.rodzaj

    def linearyzuj(self, case: str, number: str) -> str:
        przymiotnik = odmień(
            self.cecha, "adj", case=case, number=number, gender=self.rodzaj, degree="pos"
        )
        return f"{przymiotnik} {self.rzecz.linearyzuj(case, number)}"


@dataclass(frozen=True)
class Czyj(Nominalne):
    """Rzecz określona drugą rzeczą: parser podzbioru.

    Kierunek tej relacji jest kształtem drzewa, a nie kolejnością słów,
    więc parser podzbioru i podzbiór parsera są dwoma różnymi drzewami.
    Nad samym workiem lematów te dwa zdania są nie do rozróżnienia,
    i to jest ta wieloznaczność, którą ten poziom zdejmuje za darmo.

    Określenie jest bytem, a nie rzeczą, bo niesie własną liczbę:
    bez tego parser podzbiorów nie miałby jak powstać.
    """

    głowa: Nominalne
    określenie: Byt

    @property
    def rodzaj(self) -> str:
        return self.głowa.rodzaj

    def linearyzuj(self, case: str, number: str) -> str:
        głowa = self.głowa.linearyzuj(case, number)
        return f"{głowa} {self.określenie.linearyzuj('gen')}"


@dataclass(frozen=True)
class Byt:
    """Rzecz wraz z liczbą.

    Liczba stoi w drzewie, bo jest znaczeniem: jeden plik i wiele plików
    to dwie różne rzeczy do powiedzenia, a nie dwie formy jednej.
    """

    rzecz: Nominalne
    number: str = "sg"

    def linearyzuj(self, case: str) -> str:
        return self.rzecz.linearyzuj(case, self.number)


def byt(rzecz) -> Byt:
    """Rzecz postawiona tam, gdzie stoi byt, znaczy jeden egzemplarz.

    Domyślność zapisana raz, a nie zgadywanie: liczbę mnogą trzeba napisać.
    """
    return rzecz if isinstance(rzecz, Byt) else Byt(rzecz)


@dataclass(frozen=True)
class Jest:
    """Orzeczenie imienne: wejściem jest zwykły tekst polski.

    Orzecznik idzie w narzędniku, bo tyle bierze kopula,
    a szyk z orzecznikiem na czele jest tu zaszyty i jest tym brakiem,
    o którym mówi docstring modułu.
    """

    co: Byt
    czym: Byt

    def linearyzuj(self) -> str:
        kopula = odmień("być", "fin", number=self.co.number, person="ter")
        return f"{self.czym.linearyzuj('inst')} {kopula} {self.co.linearyzuj('nom')}"


@dataclass(frozen=True)
class Robi:
    """Zdanie o czynności: program zapisuje ustawienia.

    Dopełnienie idzie w bierniku, co jest ramą domyślną, a nie ramą czasownika:
    walencja jest w tym repozytorium leksykonem i ten konstruktor jej nie pyta.
    Trzyma to ``TODO.md``.
    """

    kto: Byt
    czyn: str
    co: Byt

    def linearyzuj(self) -> str:
        czasownik = odmień(self.czyn, "fin", number=self.kto.number, person="ter")
        return f"{self.kto.linearyzuj('nom')} {czasownik} {self.co.linearyzuj('acc')}"


def kompiluj(drzewo) -> str:
    """Drzewo jako zdanie: wielka litera na początku i kropka na końcu.

    Wielkość litery należy do składu, a nie do lematu,
    bo ta sama rzecz stoi raz na początku zdania, a raz w jego środku.
    """
    tekst = drzewo.linearyzuj()
    return f"{tekst[0].upper()}{tekst[1:]}."
