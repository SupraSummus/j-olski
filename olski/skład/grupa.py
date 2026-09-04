"""Grupa imienna: to, o czym zdanie orzeka, i to, czym wypełnia się jego pozycje.

Moduł deklaruje kategorie, które niosą rzecz, i nic poza nimi.
Zdania nie zna: o pozycjach ramy i o okolicznościach mówi
``olski/skład/składnia.py``, a to, co w nich staje, przychodzi stąd.
Granica biegnie po tym, co kategoria deklaruje, a nie po konstrukcji,
i dlatego ``Opis`` leży tam, a nie tutaj: rolą bywa, ale trzyma zdanie.
``Wyróżnialne`` przekracza tę granicę i przekroczyć ją musi:
dziedziczą po nim także pozycje zdania,
a znacznik zawija konstytuent w rolę (``byt`` niżej), czyli w to, co stoi tutaj.
"""

from __future__ import annotations

from dataclasses import dataclass

from olski.skład.kontekst import TERAZ, Kontekst
from olski.skład.morfologia import odmień, rodzaj_rzeczownika
from olski.skład.powierzchnia import Kawałek, lista, sklej


def wypisz(rola: Rola, case: str, kontekst: Kontekst) -> Kawałek:
    """Rola wypisana nazwą albo zaimkiem, gdy to ją wypisywane zdanie wskazuje.

    Tędy idzie każde miejsce, które rolę stawia,
    bo zaimek jest jedną decyzją i ma jedno miejsce, w którym zapada.
    Zgadza się on z rzeczą rodzajem i liczbą, a przypadek dostaje z pozycji,
    czyli tak samo jak wszystko inne w tym pliku.
    Osobne w ``Opis`` jest tylko to, że pozycja ta stoi w zdaniu podrzędnym,
    a rzecz, której zaimek dotyczy, w nadrzędnym.
    """
    if kontekst.wskazuje(rola):
        return Kawałek(
            odmień("który", "adj", case=case, number=rola.number, gender=rola.rodzaj, degree="pos")
        )
    return rola.linearyzuj(case, kontekst)


@dataclass(frozen=True)
class Wyróżnienie:
    """Konstytuent wraz z tym, czym jest w zdaniu: tematem albo rematem.

    Kategorię tę polszczyzna niesie szykiem.
    Drzewo mówi, o czym zdanie jest i co o tym dokłada,
    a kolejność słów jest z tego wnioskiem, wyciąganym przy linearyzacji.
    Wariantu szyku dopisanego do linearyzacji tu nie ma i nie ma być,
    bo taki parametr opisywałby zdanie, a to drzewo opisuje to, o czym zdanie jest.
    """

    co: object
    miejsce: str


class Wyróżnialne:
    """Znacznik tematu i rematu, dopisywany za konstytuentem.

    Znacznik stoi za konstytuentem i wolno mu tam stać,
    bo o tym, gdzie wypadną słowa wyróżnionego konstytuenta, nie mówi nic:
    mówi ``szyk`` w ``olski/skład/składnia.py``.
    Zapis przedrostkowy kazałby czytelnikowi wracać po nawiasach do tego,
    co znacznik objął,
    a dopisany z tyłu czyta się tam, gdzie konstytuent się skończył.
    Przeczenie z tyłu nie stanie i dlatego zostaje wywołaniem:
    ``nie`` wypada w tekście przed czasownikiem,
    więc zapis, który je tam stawia, mówi o wyjściu prawdę.

    Znacznikiem, a nie wywołaniem, bo mówi, czym konstytuent w zdaniu jest,
    a nie co się z nim robi.
    Dochodzą tędy wszystkie kategorie, które konstytuentem bywają,
    bo zawinięcie w rolę (``byt`` niżej) rzecz zawija,
    a okoliczność i przysłówek przepuszcza nietknięte.
    ``Wyróżnienie`` tych znaczników nie dziedziczy i nie ma dziedziczyć:
    drugi znacznik na jednym konstytuencie łamie się wtedy na samym znaczniku,
    a nie dopiero pod ``_goły`` w ``olski/skład/składnia.py``,
    który z zagnieżdżonego wyróżnienia zdejmuje jedną warstwę.

    Płaci się za to nawiasem tam, gdzie grupę zbudowały operatory.
    Kropka wiąże mocniej niż tylda i niż gwiazdka,
    więc liczba mnoga i określenie żądają nawiasu przed znacznikiem:
    ``(~R.mieszczanin).remat`` i ``(A.duży * R.lustro).remat``.
    """

    @property
    def temat(self) -> Wyróżnienie:
        """To, o czym zdanie jest: staje na czele."""
        return Wyróżnienie(byt(self), "czoło")

    @property
    def remat(self) -> Wyróżnienie:
        """To, co zdanie o temacie dokłada: staje na końcu.

        Nazwa jest tu parą do ``temat`` i dlatego jest terminem, a nie słowem zwykłym:
        `nowe` nie zgadza się rodzajem z niczym, co się w nie wkłada,
        a rozstrzygnięcie, które ten znacznik zapisuje, jest jedno z dwóch,
        więc czyta się je z pary albo nie czyta się wcale.
        """
        return Wyróżnienie(byt(self), "koniec")


class Nominalne(Wyróżnialne):
    """Wszystko, co może stanąć w grupie imiennej, wraz z zapisem operatorowym.

    Operatory stoją tutaj, a nie warstwę wyżej, bo są zapisem konstruktorów,
    a nie drugim sposobem mówienia: ``a / b`` buduje dokładnie ``Czyj(a, byt(b))``.
    Zdejmowalną warstwą są same przestrzenie nazw w ``olski.skład.słownik``.

    Kontekst wchodzi do każdej linearyzacji poniżej, choć rzeczownik go nie czyta.
    Bierze się to z ``Czyj``: określeniem bywa rzecz opisana zdaniem,
    a zdanie pyta o czas i o to, czy mówić o rzeczy zaimkiem,
    więc gałąź, która kontekstu nie przekazuje, gubi go dopiero pod sobą.
    """

    def __truediv__(self, inne) -> Czyj:
        """Dopełniacz, czyli określenie po głowie: parser przez podzbiór."""
        return Czyj(self, byt(inne))

    def __invert__(self) -> Byt:
        """Liczba mnoga."""
        return Byt(self, "pl")

    def __and__(self, inne) -> Koordynacja:
        """Koordynacja: koguci dziób oraz wężowy ogon."""
        return byt(self) & inne


@dataclass(frozen=True)
class Rzecz(Nominalne):
    """Rodzaj bytu, bez rozstrzygnięcia, ile go i który."""

    lemat: str

    @property
    def rodzaj(self) -> str:
        return rodzaj_rzeczownika(self.lemat)

    def linearyzuj(self, case: str, number: str, kontekst: Kontekst = TERAZ) -> Kawałek:
        return Kawałek(odmień(self.lemat, "subst", case=case, number=number))


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

    def linearyzuj(self, case: str, number: str, kontekst: Kontekst = TERAZ) -> Kawałek:
        przymiotnik = odmień(
            self.cecha, "adj", case=case, number=number, gender=self.rodzaj, degree="pos"
        )
        return sklej([Kawałek(przymiotnik), self.rzecz.linearyzuj(case, number, kontekst)])


@dataclass(frozen=True)
class Czyj(Nominalne):
    """Rzecz określona drugą rzeczą: parser podzbioru.

    Kierunek tej relacji jest kształtem drzewa, a nie kolejnością słów,
    więc parser podzbioru i podzbiór parsera są dwoma różnymi drzewami.
    Nad samym workiem lematów te dwa zdania są nie do rozróżnienia,
    i to jest ta wieloznaczność, którą ten poziom zdejmuje za darmo.

    Określenie jest rolą, a nie rzeczą, bo niesie własną liczbę:
    bez tego parser podzbiorów nie miałby jak powstać.
    """

    głowa: Nominalne
    określenie: Rola

    @property
    def rodzaj(self) -> str:
        return self.głowa.rodzaj

    def linearyzuj(self, case: str, number: str, kontekst: Kontekst = TERAZ) -> Kawałek:
        głowa = self.głowa.linearyzuj(case, number, kontekst)
        return sklej([głowa, wypisz(self.określenie, "gen", kontekst)])


class Rola(Wyróżnialne):
    """To, co wypełnia w zdaniu jedną rolę: jeden byt albo kilka bytów naraz.

    Rola niesie liczbę i rodzaj, bo tego żąda od niej zgodność z czasownikiem,
    i odpowiada na jeden przypadek, bo tyle daje jej pozycja, w której stoi.

    Tożsamości rola z zasady nie ma.
    Ma ją dopiero ``Postać`` w ``olski/skład/opowieść.py``, czyli ten, do kogo tekst wraca,
    i to jest jedyne miejsce, w którym dwa wystąpienia jednego lematu
    są tą samą rzeczą, a nie dwiema takimi samymi.
    """

    tożsamość = None

    @property
    def rdzeń(self):
        """Rzecz, którą autor nazwał zmienną, bo dopiero ona jest jedną rzeczą.

        ``byt`` zawija rzecz od nowa w każdym miejscu, w którym ona stoi,
        więc jedna zmienna trzymająca samą rzecz stoi w dwóch różnych rolach,
        a porównanie samych ról orzekłoby o niej, że jest dwiema rzeczami.
        Odpowiada na to każda kategoria sama, a nie pytanie o typ postawione obok,
        bo pyta stąd ``olski/skład/kontekst.py``, a on o kategoriach nie wie.
        ``Postać`` w ``olski/skład/opowieść.py`` zostaje przez to przy sobie,
        bo tam żądanie jest odwrotne: dwie postaci o jednej rzeczy
        są dwiema rzeczami z rozmysłu, bo opowieść bywa o dwóch braciach.
        """
        return self

    def __and__(self, inne) -> Koordynacja:
        return Koordynacja((self, byt(inne)))


@dataclass(frozen=True)
class Byt(Rola):
    """Rzecz wraz z liczbą.

    Liczba stoi w drzewie, bo jest znaczeniem: jeden plik i wiele plików
    to dwie różne rzeczy do powiedzenia, a nie dwie formy jednej.
    """

    rzecz: Nominalne
    number: str = "sg"

    @property
    def rodzaj(self) -> str:
        return self.rzecz.rodzaj

    @property
    def rdzeń(self) -> Nominalne:
        """Rzecz spod liczby, czyli to, co autor napisał przed zawinięciem."""
        return self.rzecz

    def linearyzuj(self, case: str, kontekst: Kontekst = TERAZ) -> Kawałek:
        return self.rzecz.linearyzuj(case, self.number, kontekst)


@dataclass(frozen=True)
class Koordynacja(Rola):
    """Kilka bytów w jednej roli: koguci dziób, wężowy ogon i żabie oczy.

    Przypadek dostają wszystkie człony ten sam, bo daje go jedna pozycja,
    a liczbę każdy własną, bo każdy jest osobną rzeczą.
    Rodzaj wychodzi z członów i wychodzi po polsku:
    dość jednego męskoosobowego, żeby cała grupa była męskoosobowa,
    a bez niego rodzaj bierze się z pierwszego,
    bo formy niemęskoosobowe czasownik ma wspólne.

    Przecinek stoi między wszystkimi członami prócz ostatniego,
    a przed ostatnim staje spójnik, i to jest polska interpunkcja tej listy.
    """

    człony: tuple[Rola, ...]

    #: Liczba grupy, a nie któregokolwiek z członów: dwie rzeczy to więcej niż jedna.
    number = "pl"

    @property
    def rodzaj(self) -> str:
        rodzaje = [człon.rodzaj for człon in self.człony]
        return "m1" if "m1" in rodzaje else rodzaje[0]

    def __and__(self, inne) -> Koordynacja:
        return Koordynacja((*self.człony, byt(inne)))

    def linearyzuj(self, case: str, kontekst: Kontekst = TERAZ) -> Kawałek:
        return lista([wypisz(człon, case, kontekst) for człon in self.człony])


def byt(rzecz):
    """Rzecz postawiona tam, gdzie stoi rola, znaczy jeden egzemplarz.

    Domyślność zapisana raz, a nie zgadywanie: liczbę mnogą trzeba napisać.
    Co rolą już jest, przechodzi tędy nietknięte,
    więc ta jedna funkcja stoi wszędzie tam, gdzie konstruktor bierze rolę.
    """
    return Byt(rzecz) if isinstance(rzecz, Nominalne) else rzecz
