"""Abstrakcyjna składnia: co da się powiedzieć, bez tego, jak to brzmi.

Kategoria mówi, jaki byt drzewo w tym miejscu trzyma,
a konstruktor mówi, co z czym wolno złożyć.
Drzewo dobrze złożone jest jednoznaczne z definicji,
więc jednoznaczność tego zapisu nie potrzebuje żadnego sprawdzenia:
kształt drzewa jest tym, co niesie znaczenie.

Poziomem tych kategorii jest dziedzina, a nie polszczyzna.
``Czyj`` mówi, że jedna rzecz jest określeniem drugiej,
a że wyjdzie z tego dopełniacz, rozstrzyga linearyzacja niżej.
Tak samo ``Okolicznik``: drzewo mówi, że coś jest celem,
a przypadek po przyimku przychodzi z ``skład/przyimki.py``.
Ten poziom jest tym, co odróżnia ten zapis od rozbioru zdania pisanego z góry;
wywód trzyma
``docs/design-notes.md``.

Szyk jest tu skutkiem, a nie zapisem.
Drzewo mówi, co w zdaniu jest tematem, a co nowe, przez ``Wyróżnienie``,
i dopiero z tego wychodzi kolejność, w której konstytuenty się wypisują.
Czasownik przy tym nie rusza się nigdy,
więc wyróżnienie przestawia to, co wokół niego stoi, a nie całe zdanie.
Jedną kolejność dokłada do tego ``Opis`` i tej autor nie wybiera:
zaimek względny otwiera zdanie podrzędne zawsze,
więc rzecz wskazana staje w nim na czele, czymkolwiek w nim jest.

Czego drzewo nie niesie, jest tu decyzją, a nie brakiem.
Nie ma w nim przypadka, bo przypadek bierze się z pozycji.
Nie ma rodzaju, bo rodzaj rzeczownika jest leksykalny.
Nie ma osoby ani czasu, bo obie te rzeczy niesie ``Kontekst``:
czas jest własnością opowiadania, a nie pojedynczego zdarzenia.
Dziury są dwie i obie są dziurami, a nie decyzjami.
Wewnątrz grupy imiennej szyku nie ma nadal,
bo ``Jaki`` stawia przymiotnik przed rzeczownikiem zawsze,
choć przymiotnik po rzeczowniku nazywa, a przed nim określa.
Rzecz stoi tu pod lematem, choć jednym napisem odmieniają się leksemy
o różnej odmianie, więc wybiera je kolejność odpowiedzi słownika.
Trzyma to ``TODO.md``, a kolejność ``docs/roadmap.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from olski.walencja import bierze_biernik
from skład.morfologia import odmień, rodzaj_rzeczownika
from skład.przyimki import przypadek

#: Czas jako żądanie postawione morfologii, a nie jako gałąź w linearyzacji:
#: forma przeszła zgadza się z podmiotem rodzajem, a teraźniejsza osobą,
#: więc różnią się one tym, o co się pyta, a nie tym, kto pyta.
CZASY = {
    "teraz": lambda podmiot: ("fin", dict(number=podmiot.number, person="ter")),
    "kiedyś": lambda podmiot: ("praet", dict(number=podmiot.number, gender=podmiot.rodzaj)),
}


class PozaRamą(Exception):
    """Drzewo żąda od słowa pozycji, której jego rama nie ma.

    Wyjątek, a nie zdanie wypuszczone mimo to,
    z tego samego powodu co ``BrakFormy`` w ``skład/morfologia.py``:
    to jest błąd kompilacji,
    bo `Linter pomaga dobry kod.` nie jest zdaniem polskim
    i nikt takiego nie chciał napisać.

    Ramę ma tu czasownik i ma ją przyimek,
    a pytanie jest w obu wypadkach jedno:
    czy leksykon zna pozycję, którą autor postawił w drzewie.
    """


@dataclass(frozen=True)
class Kontekst:
    """Czego linearyzacja nie znajduje w drzewie, które właśnie wypisuje.

    Pierwsze dwie rzeczy są własnościami tekstu, a nie zdania,
    więc zdanie ich w sobie nie trzyma:
    ta sama rzecz opowiedziana raz jako to, co się stało, a raz jako to, co się dzieje,
    jest jednym drzewem i dwoma czasami.
    Kto tymi dwoma steruje, mówi ``skład/opowieść.py``.

    Trzecia jest własnością miejsca, w którym zdanie stoi.
    Zdanie wypisywane jako opis rzeczy mówi o tej rzeczy zaimkiem, a nie nazwą,
    i steruje tym drzewo, a nie tekst; mechanizm trzyma ``Opis`` niżej.
    Stoi tu obok tamtych dwóch, bo pytanie jest jedno:
    czego wypisywane drzewo o sobie nie wie.

    Wartość domyślna jest zdaniem stojącym samo:
    dzieje się teraz, nie ma za sobą nikogo, kogo dałoby się pominąć,
    i niczego nie opisuje.
    """

    czas: str = "teraz"
    pomijany: object = None
    wskazywany: object = None

    def pomija(self, rola: Rola) -> bool:
        """Czy podmiot jest tym, o kim mowa była zdanie wcześniej.

        Pominięty podmiot jest w polszczyźnie zwykłym sposobem mówienia dalej
        o tym samym, bo osobę i rodzaj niesie sam czasownik,
        więc nie ma czego powtarzać.
        """
        return self.pomijany is not None and rola.tożsamość is self.pomijany

    def wskazuje(self, rola: Rola) -> bool:
        """Czy to ta rola, którą wypisywane zdanie wskazuje.

        Porównaniem jest tożsamość obiektu, a nie równość,
        bo tą samą rzeczą jest tu ta sama zmienna, tak samo jak przy ``Postać``:
        dwie równe grupy imienne są dwiema rzeczami, dopóki autor nie użyje jednej.
        """
        return self.wskazywany is not None and _rdzeń(rola) is _rdzeń(self.wskazywany)


TERAZ = Kontekst()


def _rdzeń(rola: Rola):
    """Rzecz spod roli, bo dopiero ona jest tym, co autor nazwał zmienną.

    ``byt`` zawija rzecz od nowa w każdym miejscu, w którym ona stoi,
    więc jedna zmienna trzymająca samą rzecz stoi w dwóch różnych rolach,
    a porównanie samych ról orzekłoby o niej, że jest dwiema rzeczami.
    Zejście pod rolę zdejmuje autorowi pytanie, którego nie ma po co sobie zadawać:
    czy zmienna, którą napisał, trzyma rzecz, czy rzecz wraz z liczbą.
    Pod ``Postać`` to zejście nie schodzi, bo tam żądanie jest odwrotne:
    dwie postaci o jednej rzeczy są dwiema rzeczami z rozmysłu,
    bo opowieść bywa o dwóch braciach.
    """
    return rola.rzecz if isinstance(rola, Byt) else rola


def _wypisz(rola: Rola, case: str, kontekst: Kontekst) -> str:
    """Rola wypisana nazwą albo zaimkiem, gdy to ją wypisywane zdanie wskazuje.

    Tędy idzie każde miejsce, które rolę stawia,
    bo zaimek jest jedną decyzją i ma jedno miejsce, w którym zapada.
    Zgadza się on z rzeczą rodzajem i liczbą, a przypadek dostaje z pozycji,
    czyli tak samo jak wszystko inne w tym pliku.
    Osobne w ``Opis`` jest tylko to, że pozycja ta stoi w zdaniu podrzędnym,
    a rzecz, której zaimek dotyczy, w nadrzędnym.
    """
    if kontekst.wskazuje(rola):
        return odmień(
            "który", "adj", case=case, number=rola.number, gender=rola.rodzaj, degree="pos"
        )
    return rola.linearyzuj(case, kontekst)


class Nominalne:
    """Wszystko, co może stanąć w grupie imiennej, wraz z zapisem operatorowym.

    Operatory stoją tutaj, a nie warstwę wyżej, bo są zapisem konstruktorów,
    a nie drugim sposobem mówienia: ``a / b`` buduje dokładnie ``Czyj(a, byt(b))``.
    Zdejmowalną warstwą są same przestrzenie nazw w ``skład.słownik``.

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

    def linearyzuj(self, case: str, number: str, kontekst: Kontekst = TERAZ) -> str:
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

    def linearyzuj(self, case: str, number: str, kontekst: Kontekst = TERAZ) -> str:
        przymiotnik = odmień(
            self.cecha, "adj", case=case, number=number, gender=self.rodzaj, degree="pos"
        )
        return f"{przymiotnik} {self.rzecz.linearyzuj(case, number, kontekst)}"


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

    def linearyzuj(self, case: str, number: str, kontekst: Kontekst = TERAZ) -> str:
        głowa = self.głowa.linearyzuj(case, number, kontekst)
        return f"{głowa} {_wypisz(self.określenie, 'gen', kontekst)}"


class Rola:
    """To, co wypełnia w zdaniu jedną rolę: jeden byt albo kilka bytów naraz.

    Rola niesie liczbę i rodzaj, bo tego żąda od niej zgodność z czasownikiem,
    i odpowiada na jeden przypadek, bo tyle daje jej pozycja, w której stoi.

    Tożsamości rola z zasady nie ma.
    Ma ją dopiero ``Postać`` w ``skład/opowieść.py``, czyli ten, do kogo tekst wraca,
    i to jest jedyne miejsce, w którym dwa wystąpienia jednego lematu
    są tą samą rzeczą, a nie dwiema takimi samymi.
    """

    tożsamość = None

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

    def linearyzuj(self, case: str, kontekst: Kontekst = TERAZ) -> str:
        return self.rzecz.linearyzuj(case, self.number, kontekst)


def _przecinkami(człony: list[str]) -> str:
    """Człony rozdzielone przecinkiem, chyba że poprzedni już się nim zamknął.

    ``Opis`` niżej zamyka zdanie podrzędne przecinkiem,
    bo nie wie, czy coś po nim stanie.
    Ta funkcja jest jedynym miejscem, które po konstytuencie stawia przecinek rozdzielający,
    więc jedynym, które tamten przecinek musi zobaczyć.
    Polszczyzna stawia tu jeden przecinek, a nie dwa,
    bo zamknięcie zdania podrzędnego jest tym samym przecinkiem, co rozdzielenie listy.
    """
    wynik = człony[0]
    for człon in człony[1:]:
        wynik += f" {człon}" if wynik.endswith(",") else f", {człon}"
    return wynik


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

    def linearyzuj(self, case: str, kontekst: Kontekst = TERAZ) -> str:
        wypisane = [_wypisz(człon, case, kontekst) for człon in self.człony]
        return f"{_przecinkami(wypisane[:-1])} i {wypisane[-1]}"


def byt(rzecz):
    """Rzecz postawiona tam, gdzie stoi rola, znaczy jeden egzemplarz.

    Domyślność zapisana raz, a nie zgadywanie: liczbę mnogą trzeba napisać.
    Co rolą już jest, przechodzi tędy nietknięte,
    więc ta jedna funkcja stoi wszędzie tam, gdzie konstruktor bierze rolę.
    """
    return Byt(rzecz) if isinstance(rzecz, Nominalne) else rzecz


@dataclass(frozen=True)
class Okolicznik:
    """Okoliczność wyrażona grupą imienną: w piwnicy, do miasta, wzrokiem.

    Relacja jest kategorią dziedziny i to ona stoi w drzewie,
    a przyimek wraz z przypadkiem wychodzi z ``skład/przyimki.py``.
    Przyimkiem żadnym jest pusty napis, bo narzędzie polszczyzna wyraża
    samym narzędnikiem, a rola bez przyimka jest tu tą samą kategorią co z nim.

    Przyłączenie stoi w drzewie i to jest cała różnica między tym kierunkiem
    a parserem, któremu ``docs/subset.md`` zostawia je przy czytelniku:
    okolicznik postawiony przy czasowniku i określenie postawione przy rzeczy
    są dwoma różnymi drzewami, więc nie ma tu czego rozstrzygać po fakcie.
    """

    przyimek: str
    relacja: str
    co: Rola

    def __post_init__(self) -> None:
        if przypadek(self.przyimek, self.relacja) is None:
            raise PozaRamą(f"{self.przyimek or 'sam narzędnik'} nie stoi w relacji {self.relacja}")

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> str:
        grupa = _wypisz(self.co, przypadek(self.przyimek, self.relacja), kontekst)
        return " ".join(część for część in (self.przyimek, grupa) if część)


@dataclass(frozen=True)
class Przysłówek:
    """Okoliczność wyrażona jednym słowem: wkrótce, nagle.

    Stopnia drzewo nie niesie i dlatego linearyzacja żąda równego:
    przysłówek w stopniu wyższym mówi co innego niż w równym,
    a mówienie tego dopiero czeka na kategorię.
    Przysłówka, który stopnia nie ma, żądanie to nie dotyczy,
    i rozstrzyga to ``odmień`` w ``skład/morfologia.py``.
    """

    lemat: str

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> str:
        return odmień(self.lemat, "adv", degree="pos")


@dataclass(frozen=True)
class Wyróżnienie:
    """Konstytuent wraz z tym, czym jest w zdaniu: tematem albo tym, co nowe.

    To jest ta kategoria, którą polszczyzna niesie szykiem.
    Drzewo mówi, o czym zdanie jest i co o tym dokłada,
    a kolejność słów jest z tego wnioskiem, wyciąganym przy linearyzacji.
    Wariantu szyku dopisanego do linearyzacji tu nie ma i nie ma być,
    bo taki parametr opisywałby zdanie, a to drzewo opisuje to, o czym zdanie jest.
    """

    co: object
    miejsce: str


def _goły(konstytuent):
    """Konstytuent bez wyróżnienia, bo zgodność liczy się z rzeczy, a nie z jej roli w tekście."""
    return konstytuent.co if isinstance(konstytuent, Wyróżnienie) else konstytuent


def _wskazany(konstytuent, kontekst: Kontekst) -> bool:
    """Czy to ten konstytuent niesie rzecz, którą wypisywane zdanie wskazuje.

    Rola stoi w zdaniu na dwóch głębokościach: sama albo pod okolicznikiem,
    bo `w której mieszkał bazyliszek` wskazuje piwnicę spod przyimka.
    Głębiej ta funkcja nie schodzi, i dlatego ``Opis`` pyta o to samo,
    zanim zdanie powstanie: rzecz wskazana spod grupy imiennej
    nie miałaby jak wyjść na czoło, więc jest błędem, a nie zdaniem o dziwnym szyku.
    """
    goły = _goły(konstytuent)
    if isinstance(goły, Okolicznik):
        return kontekst.wskazuje(goły.co)
    return kontekst.wskazuje(goły)


def _miejsce(konstytuent, kontekst: Kontekst):
    """Gdzie ten konstytuent staje: na czele, na końcu albo tam, gdzie zwykle.

    Rzecz wskazana staje na czele i nie jest to wybór autora:
    zaimek względny otwiera w polszczyźnie zdanie podrzędne,
    a nie stoi w nim tam, gdzie stałaby rzecz, którą zastępuje.
    Wyróżnienie napisane nad tą samą rzeczą jest więc albo tym samym czołem,
    albo drzewem, które żąda dwóch rzeczy naraz, i wtedy się zgłasza.
    """
    napisane = konstytuent.miejsce if isinstance(konstytuent, Wyróżnienie) else None
    if not _wskazany(konstytuent, kontekst):
        return napisane
    if napisane not in (None, "czoło"):
        raise PozaRamą(f"rzecz wskazana nie staje jako {napisane}, bo staje na czele")
    return "czoło"


def _podmiot(pole, kontekst: Kontekst) -> list[tuple[str | None, str]]:
    """Podmiot na swojej pozycji albo nic, gdy zdanie wcześniej miało ten sam.

    Lista, a nie napis, bo pominięty podmiot nie zostawia po sobie pozycji.
    Reguła stoi tu raz, bo zdanie o czynności i orzeczenie imienne
    opuszczają podmiot tak samo, a dwie kopie tej reguły rozjechałyby się
    na pierwszym zdaniu, które ma kopulę zamiast czasownika.
    """
    rola = _goły(pole)
    if kontekst.pomija(rola):
        return []
    return [(_miejsce(pole, kontekst), _wypisz(rola, "nom", kontekst))]


def _szyk(pozycje: list[tuple[str | None, str]]) -> str:
    """Kolejność wypisania: czoło, środek w porządku domyślnym, koniec.

    Środek jest tu porządkiem, którego nikt nie wybierał,
    więc zdanie bez żadnego wyróżnienia wychodzi w szyku podmiot, czasownik, reszta.

    Wyróżnione miejsce bierze jeden konstytuent, bo na czele stoi jedna rzecz,
    więc drugi zgłasza się tak samo jak drugie dopełnienie w ``zdarzenie``:
    dwa tematy naraz są drzewem błędnym, a nie zdaniem o dziwnym szyku.
    """
    wyróżnione: dict[str, str] = {}
    środek: list[str] = []
    for miejsce, tekst in pozycje:
        if miejsce is None:
            środek.append(tekst)
            continue
        if miejsce in wyróżnione:
            raise PozaRamą(f"dwa konstytuenty wyróżnione jako {miejsce}")
        wyróżnione[miejsce] = tekst
    kolejność = (wyróżnione.get("czoło"), *środek, wyróżnione.get("koniec"))
    return " ".join(część for część in kolejność if część)


@dataclass(frozen=True)
class Jest:
    """Orzeczenie imienne: zwykły tekst polski jest wejściem.

    Orzecznik idzie w narzędniku, bo tyle bierze kopula.
    Szyk wychodzi z wyróżnień tak samo jak przy zdarzeniu,
    więc `Wejściem jest zwykły tekst polski.` jest tu orzecznikiem postawionym
    na czele wraz z podmiotem odesłanym na koniec, a nie wariantem linearyzacji.
    """

    co: Rola | Wyróżnienie
    czym: Rola | Wyróżnienie

    @property
    def podmiot(self) -> Rola:
        return _goły(self.co)

    @property
    def konstytuenty(self) -> tuple:
        return (self.co, self.czym)

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> str:
        pos, cechy = CZASY[kontekst.czas](self.podmiot)
        return _szyk(
            [
                *_podmiot(self.co, kontekst),
                (None, odmień("być", pos, **cechy)),
                (
                    _miejsce(self.czym, kontekst),
                    _wypisz(_goły(self.czym), "inst", kontekst),
                ),
            ]
        )


@dataclass(frozen=True)
class Robi:
    """Zdanie o czynności: program zapisuje ustawienia.

    Dopełnienie idzie w bierniku wtedy,
    gdy leksykon walencyjny czasownikowi biernika nie odmawia.
    Pytany jest ten sam plik, o który pyta parser po drugiej stronie,
    bo rama jest faktem o słowie, a nie o kierunku;
    ``olski/walencja.py`` czyta go dla obu i trzyma wywód.

    Pytanie pada w konstruktorze, a nie w linearyzacji,
    bo to konstruktor mówi, co z czym wolno złożyć,
    i bo drzewo, które tego nie przechodzi, jest błędne całe,
    a nie w tym jednym miejscu, gdzie się je wypisuje.

    Przeczenie stoi tu, a nie osobnym konstruktorem,
    bo sięga dwóch rzeczy naraz: stawia ``nie`` przed czasownikiem
    i zabiera dopełnieniu biernik na rzecz dopełniacza,
    a te dwie rzeczy są jedną decyzją i rozjechać się nie mogą.
    """

    kto: Rola | Wyróżnienie
    czyn: str
    co: Rola | Wyróżnienie | None = None
    okoliczniki: tuple = ()
    przeczenie: bool = False

    def __post_init__(self) -> None:
        if self.co is not None and not bierze_biernik(self.czyn):
            raise PozaRamą(f"{self.czyn} nie bierze dopełnienia w bierniku")

    @property
    def podmiot(self) -> Rola:
        return _goły(self.kto)

    @property
    def konstytuenty(self) -> tuple:
        dopełnienie = () if self.co is None else (self.co,)
        return (self.kto, *dopełnienie, *self.okoliczniki)

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> str:
        pozycje = _podmiot(self.kto, kontekst)
        pozycje.append((None, self._czasownik(kontekst)))
        if self.co is not None:
            przypadek_dopełnienia = "gen" if self.przeczenie else "acc"
            pozycje.append(
                (
                    _miejsce(self.co, kontekst),
                    _wypisz(_goły(self.co), przypadek_dopełnienia, kontekst),
                )
            )
        for okolicznik in self.okoliczniki:
            pozycje.append(
                (_miejsce(okolicznik, kontekst), _goły(okolicznik).linearyzuj(kontekst))
            )
        return _szyk(pozycje)

    def _czasownik(self, kontekst: Kontekst) -> str:
        pos, cechy = CZASY[kontekst.czas](self.podmiot)
        forma = odmień(self.czyn, pos, **cechy)
        return f"nie {forma}" if self.przeczenie else forma


#: Kategorie, które w zdaniu stoją jako okoliczność, a nie jako uczestnik zdarzenia.
OKOLICZNOŚCI = (Okolicznik, Przysłówek)


def zdarzenie(kto, czyn: str, *reszta) -> Robi:
    """Zdarzenie złożone z tego, co dostało, po kategoriach, a nie po pozycjach.

    Pierwszy argument jest tym, kto działa, i stoi zawsze.
    Reszta rozdziela się kategorią: okoliczności może być wiele,
    a uczestnik zdarzenia poza działającym jest jeden,
    więc liczenie pozycji zostaje po tej stronie, a nie po stronie autora.
    Czasownik nieprzechodni składa się więc tak samo jak przechodni,
    a o dopełnienie pyta rama z leksykonu, którą sprawdza ``Robi``.
    """
    dopełnienia: list = []
    okoliczniki: list = []
    for część in reszta:
        cel = okoliczniki if isinstance(_goły(część), OKOLICZNOŚCI) else dopełnienia
        cel.append(część)
    if len(dopełnienia) > 1:
        raise PozaRamą(f"{czyn} dostaje {len(dopełnienia)} dopełnienia zamiast jednego")
    return Robi(
        kto=byt(kto),
        czyn=czyn,
        co=byt(dopełnienia[0]) if dopełnienia else None,
        okoliczniki=tuple(okoliczniki),
    )


def nie(zdanie: Robi) -> Robi:
    """To samo zdarzenie zaprzeczone.

    Konstruktorem to nie jest, tylko zmianą jednej cechy zdarzenia,
    bo zaprzeczone zdanie ma te same role co twierdzące
    i drugi konstruktor kazałby wypisać je jeszcze raz.
    """
    return replace(zdanie, przeczenie=True)


@dataclass(frozen=True)
class Opis(Rola):
    """Rzecz wskazana zdarzeniem, w którym stoi: postaci, których nikt nie liczył.

    Kategorią dziedziny jest tu wskazywanie, a nie zdanie podrzędne.
    ``Jaki`` wskazuje rzecz cechą, ta klasa wskazuje ją zdarzeniem,
    i pytanie jest w obu wypadkach jedno: o którą rzecz mowa.
    Że wychodzi z tego przydawka zdaniowa wraz z zaimkiem i przecinkami,
    rozstrzyga linearyzacja, tak samo jak rozstrzyga przypadek.

    Które miejsce w zdarzeniu zostaje zaimkiem, mówi tożsamość obiektu,
    a nie osobny znacznik postawiony w tym miejscu.
    Autor pisze rzecz raz i stawia tę samą zmienną w zdaniu, które ją opisuje,
    czyli robi to samo, co robi z ``Postać`` w ``skład/opowieść.py``:
    tam ta sama zmienna dwa razy jest jedną rzeczą w dwóch zdaniach,
    a tutaj jest jedną rzeczą w zdaniu nadrzędnym i podrzędnym naraz.

    Zdanie, które tej rzeczy nie stawia w miejscu, skąd zaimek wyjdzie na czoło,
    zgłasza się od razu, bo opis, który nie opisuje, jest błędem drzewa.
    Czym jest to miejsce, mówi ``_wskazany``.
    """

    rzecz: Rola
    zdanie: object

    def __post_init__(self) -> None:
        kontekst = Kontekst(wskazywany=self.rzecz)
        if not any(_wskazany(część, kontekst) for część in self.zdanie.konstytuenty):
            raise PozaRamą("zdanie opisujące nie stawia opisywanej rzeczy")

    @property
    def number(self) -> str:
        return self.rzecz.number

    @property
    def rodzaj(self) -> str:
        return self.rzecz.rodzaj

    @property
    def tożsamość(self):
        return self.rzecz.tożsamość

    def linearyzuj(self, case: str, kontekst: Kontekst = TERAZ) -> str:
        """Rzecz, przecinek, zdanie o niej i przecinek zamykający.

        Przypadek dostaje sama rzecz, bo to ona stoi w zdaniu nadrzędnym,
        a zdanie podrzędne rozdaje przypadki własne i dostaje od tego kontekstu
        czas oraz to, którą rzecz ma powiedzieć zaimkiem.
        Pomijanie podmiotu w nim nie działa, i to nie jest brak:
        podmiot opuszczony w zdaniu podrzędnym czytałby się jako ten,
        którego zaimek właśnie zastąpił.
        """
        wewnątrz = replace(kontekst, wskazywany=self.rzecz, pomijany=None)
        return f"{_wypisz(self.rzecz, case, kontekst)}, {self.zdanie.linearyzuj(wewnątrz)},"


def kompiluj(drzewo, kontekst: Kontekst = TERAZ) -> str:
    """Drzewo jako zdanie: wielka litera na początku i kropka na końcu.

    Wielkość litery należy do składu, a nie do lematu,
    bo ta sama rzecz stoi raz na początku zdania, a raz w jego środku.

    Przecinek zamykający opis znika przed kropką, bo polszczyzna nie stawia obu.
    Zamyka go ``Opis``, który nie wie, czy coś jeszcze po nim stanie,
    a wie to dopiero to miejsce, i tylko o jednym miejscu w zdaniu:
    o jego końcu.
    """
    tekst = drzewo.linearyzuj(kontekst).removesuffix(",")
    return f"{tekst[0].upper()}{tekst[1:]}."
