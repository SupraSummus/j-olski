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
Dwie kolejności dokładają do tego konstrukcje, w których autor nie wybiera.
Zaimek względny otwiera zdanie podrzędne zawsze,
więc rzecz wskazana przez ``Opis`` staje w nim na czele, czymkolwiek w nim jest.
Okoliczność wyrażona zdarzeniem staje na czele zdania,
o ile pozwala na to jej spójnik, i mówi o tym leksykon,
bo jest to fakt o słowie, a nie o zdaniu, w którym ono stoi.

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
from skład.spójniki import staje_na_czele, wprowadza

#: Czas jako żądanie postawione morfologii, a nie jako gałąź w linearyzacji:
#: forma przeszła zgadza się z podmiotem rodzajem, a teraźniejsza osobą,
#: więc różnią się one tym, o co się pyta, a nie tym, kto pyta.
CZASY = {
    "teraz": lambda podmiot: ("fin", dict(number=podmiot.number, person="ter")),
    "kiedyś": lambda podmiot: ("praet", dict(number=podmiot.number, gender=podmiot.rodzaj)),
}


def _forma(czasownik: str, podmiot: Rola, czas: str) -> str:
    """Forma czasownika, którą ten podmiot z niego wyciąga.

    Tędy idzie każde zdanie, bo zgodność z podmiotem jest jedna
    i nie zależy od tego, czy orzeka się czynność, czy bycie czymś.
    Tędy idzie też pytanie odwrotne, które stawia ``pomijalny``:
    forma jest wszystkim, co po opuszczonym podmiocie zostaje,
    więc jest też miarą tego, czy da się go opuścić.
    """
    pos, cechy = CZASY[czas](podmiot)
    return odmień(czasownik, pos, **cechy)


class PozaRamą(Exception):
    """Drzewo żąda od słowa pozycji, której jego rama nie ma.

    Wyjątek, a nie zdanie wypuszczone mimo to,
    z tego samego powodu co ``BrakFormy`` w ``skład/morfologia.py``:
    to jest błąd kompilacji,
    bo `Linter pomaga dobry kod.` nie jest zdaniem polskim
    i nikt takiego nie chciał napisać.

    Ramę ma tu czasownik, przyimek i spójnik,
    a pytanie jest we wszystkich trzech wypadkach jedno:
    czy leksykon zna to, co autor postawił w drzewie.
    Spójnik pytany jest przy tym o dwie rzeczy, bo o dwóch mówi:
    o relacji, w której stoi, i o tym, czy jego zdanie staje na czele pary.
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


@dataclass(frozen=True)
class Kawałek:
    """Wypisany konstytuent wraz z przecinkami, których żąda od sąsiadów.

    Przecinek jest tu własnością kawałka, a nie znakiem w napisie,
    bo o tym, czy staje, rozstrzyga dopiero to, co obok niego stanie,
    a tego kawałek o sobie nie wie.
    Zdanie podrzędne żąda przecinka z obu stron i dostaje go z żadnej,
    gdy stoi samo; opis żąda go z jednej,
    bo przecinek otwierający stoi w środku samego opisu.
    Krawędź zdania przecinka nie stawia, i tyle wystarcza,
    żeby kropka nie stanęła po przecinku, a lista nie dostała dwóch.

    Bez tego pola przecinek jedzie wewnątrz napisu, a każde miejsce,
    które po konstytuencie coś stawia, musi o nim wiedzieć z ogona tego napisu.
    Miejsce dopisane bez tej wiedzy stawia drugi przecinek tuż za pierwszym,
    czyli wypuszcza tekst błędny i nigdzie nie zgłoszony.
    """

    napis: str
    przed: bool = False
    po: bool = False


def _rozdziela(lewy: Kawałek, prawy: Kawałek) -> str:
    """Czym stoją obok siebie dwa kawałki: przecinkiem, gdy któryś go żąda.

    Dość jednego żądania, bo polszczyzna stawia tu jeden przecinek, a nie dwa:
    zamknięcie zdania podrzędnego jest tym samym przecinkiem, co rozdzielenie listy.
    """
    return ", " if lewy.po or prawy.przed else " "


def _sklej(kawałki: list[Kawałek]) -> Kawałek:
    """Kawałki jeden po drugim, wraz z żądaniami skrajnych, bo te zostają niespełnione.

    Przecinek wewnętrzny staje tutaj, a zewnętrzny czeka na to,
    co stanie obok całości, więc kawałek sklejony żąda tego samego,
    co żądały jego krańce.
    """
    napis, poprzedni = kawałki[0].napis, kawałki[0]
    for kawałek in kawałki[1:]:
        napis += _rozdziela(poprzedni, kawałek) + kawałek.napis
        poprzedni = kawałek
    return Kawałek(napis, przed=kawałki[0].przed, po=kawałki[-1].po)


def _wypisz(rola: Rola, case: str, kontekst: Kontekst) -> Kawałek:
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
        return _sklej([Kawałek(przymiotnik), self.rzecz.linearyzuj(case, number, kontekst)])


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
        return _sklej([głowa, _wypisz(self.określenie, "gen", kontekst)])


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

    def linearyzuj(self, case: str, kontekst: Kontekst = TERAZ) -> Kawałek:
        return self.rzecz.linearyzuj(case, self.number, kontekst)


def _lista(człony: list[Kawałek]) -> Kawałek:
    """Człony przecinkami, a przed ostatnim spójnik: polska interpunkcja listy.

    Stoi ona w jednym miejscu, bo koordynacja bytów i ciąg zdarzeń
    dzielą ją co do znaku, choć łączą rzeczy różnego rodzaju.
    Przecinka żąda każdy człon od swojego poprzednika,
    więc człon, który zażądał go sam, nie dostaje drugiego.
    """
    początek = _sklej([człony[0], *(replace(człon, przed=True) for człon in człony[1:-1])])
    return _sklej([początek, Kawałek("i"), człony[-1]])


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
        return _lista([_wypisz(człon, case, kontekst) for człon in self.człony])


def byt(rzecz):
    """Rzecz postawiona tam, gdzie stoi rola, znaczy jeden egzemplarz.

    Domyślność zapisana raz, a nie zgadywanie: liczbę mnogą trzeba napisać.
    Co rolą już jest, przechodzi tędy nietknięte,
    więc ta jedna funkcja stoi wszędzie tam, gdzie konstruktor bierze rolę.
    """
    return Byt(rzecz) if isinstance(rzecz, Nominalne) else rzecz


@dataclass(frozen=True)
class Okolicznik:
    """Okoliczność w relacji: w piwnicy, wzrokiem, gdy bazyliszek otworzył oczy.

    Relacja jest kategorią dziedziny i to ona stoi w drzewie,
    a słowo, którym polszczyzna ją wyraża, rozstrzyga o sobie tyle,
    ile go od relacji odróżnia: ``w`` mówi, gdzie i kiedy,
    a ``gdy`` mówi tylko kiedy.

    Okoliczność bywa rzeczą albo zdarzeniem i jest to jedna kategoria,
    bo pytanie stawia się jedno.
    Różnią się one tym, czym słowo przed nimi jest po polsku:
    przed rzeczą stoi przyimek, który rządzi przypadkiem (``skład/przyimki.py``),
    a przed zdarzeniem spójnik, który nie rządzi niczym (``skład/spójniki.py``),
    bo zdanie podrzędne rozdaje przypadki własne.
    Przyimkiem żadnym jest pusty napis, bo narzędzie polszczyzna wyraża
    samym narzędnikiem, a rola bez przyimka jest tu tą samą kategorią co z nim.

    Przyłączenie stoi w drzewie i to jest cała różnica między tym kierunkiem
    a parserem, któremu ``docs/subset.md`` zostawia je przy czytelniku:
    okolicznik postawiony przy czasowniku i określenie postawione przy rzeczy
    są dwoma różnymi drzewami, więc nie ma tu czego rozstrzygać po fakcie.
    """

    słowo: str
    relacja: str
    co: Rola | Zdanie

    @property
    def zdarzeniem(self) -> bool:
        """Czy pod tą okolicznością stoi zdarzenie, a nie rzecz."""
        return isinstance(self.co, Zdanie)

    @property
    def wysuwalna(self) -> bool:
        """Czy wolno postawić tę okoliczność na czele zdania.

        Grupa imienna staje na czele zawsze, bo szyk polszczyzny jest swobodny
        i o wysunięciu rozstrzyga to, o czym zdanie jest.
        Zdarzenie staje tam, gdy pozwala na to jego spójnik,
        i to jest jedyne miejsce w tym pliku, w którym leksykon mówi o szyku.
        """
        return not self.zdarzeniem or staje_na_czele(self.słowo, self.relacja)

    def __post_init__(self) -> None:
        if self.zdarzeniem:
            znane = wprowadza(self.słowo, self.relacja)
        else:
            znane = przypadek(self.słowo, self.relacja) is not None
        if not znane:
            raise PozaRamą(f"{self.słowo or 'sam narzędnik'} nie stoi w relacji {self.relacja}")

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> Kawałek:
        """Słowo wraz z tym, co po nim stoi, a przecinki jako żądanie z obu stron.

        Zdanie podrzędne oddziela się przecinkiem z każdej strony, przy której
        coś stoi, więc żąda go z obu, a krańce zdania żądania nie spełniają.
        Wskazywania i pominięcia podrzędne nie dziedziczy, a czas dziedziczy:
        zaimek wyszedłby z niego na czoło, którego nie ma, a podmiot opuszczony
        odsyłałby do zdania nadrzędnego, czyli tam, gdzie stoi ktoś inny.
        """
        if self.zdarzeniem:
            wewnątrz = replace(kontekst, wskazywany=None, pomijany=None)
            sklejone = _sklej([Kawałek(self.słowo), self.co.linearyzuj(wewnątrz)])
            return replace(sklejone, przed=True, po=True)
        grupa = _wypisz(self.co, przypadek(self.słowo, self.relacja), kontekst)
        return _sklej([Kawałek(self.słowo), grupa]) if self.słowo else grupa


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

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> Kawałek:
        return Kawałek(odmień(self.lemat, "adv", degree="pos"))


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
    Okoliczność wyrażona zdarzeniem żadnej roli nie wskazuje z tego samego powodu:
    zaimek stojący w zdaniu podrzędnym drugiego stopnia nie ma dokąd wyjść.
    """
    goły = _goły(konstytuent)
    if isinstance(goły, Okolicznik):
        return not goły.zdarzeniem and kontekst.wskazuje(goły.co)
    return kontekst.wskazuje(goły)


def _miejsce(konstytuent, kontekst: Kontekst):
    """Gdzie ten konstytuent staje: na czele, na końcu albo tam, gdzie zwykle.

    Rzecz wskazana staje na czele i nie jest to wybór autora:
    zaimek względny otwiera w polszczyźnie zdanie podrzędne,
    a nie stoi w nim tam, gdzie stałaby rzecz, którą zastępuje.
    Wyróżnienie napisane nad tą samą rzeczą jest więc albo tym samym czołem,
    albo drzewem, które żąda dwóch rzeczy naraz, i wtedy się zgłasza.

    Zgłasza się także czoło żądane od okoliczności, która na czele nie staje,
    bo o tym rozstrzyga leksykon, a nie autor:
    zdanie z ``więc`` na przodzie nie jest zdaniem o innym szyku,
    tylko zdaniem, którego polszczyzna nie ma.
    """
    goły = _goły(konstytuent)
    napisane = konstytuent.miejsce if isinstance(konstytuent, Wyróżnienie) else None
    if napisane == "czoło" and isinstance(goły, Okolicznik) and not goły.wysuwalna:
        raise PozaRamą(f"{goły.słowo} nie staje na czele")
    if not _wskazany(konstytuent, kontekst):
        return napisane
    if napisane not in (None, "czoło"):
        raise PozaRamą(f"rzecz wskazana nie staje jako {napisane}, bo staje na czele")
    return "czoło"


def _podmiot(pole, kontekst: Kontekst) -> list[tuple[str | None, Kawałek]]:
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


def _szyk(pozycje: list[tuple[str | None, Kawałek]]) -> Kawałek:
    """Kolejność wypisania: czoło, środek w porządku domyślnym, koniec.

    Środek jest tu porządkiem, którego nikt nie wybierał,
    więc zdanie bez żadnego wyróżnienia wychodzi w szyku podmiot, czasownik, reszta.

    Wyróżnione miejsce bierze jeden konstytuent, bo na czele stoi jedna rzecz,
    więc drugi zgłasza się tak samo jak drugie dopełnienie w ``zdarzenie``:
    dwa tematy naraz są drzewem błędnym, a nie zdaniem o dziwnym szyku.
    """
    wyróżnione: dict[str, Kawałek] = {}
    środek: list[Kawałek] = []
    for miejsce, kawałek in pozycje:
        if miejsce is None:
            środek.append(kawałek)
            continue
        if miejsce in wyróżnione:
            raise PozaRamą(f"dwa konstytuenty wyróżnione jako {miejsce}")
        wyróżnione[miejsce] = kawałek
    kolejność = (wyróżnione.get("czoło"), *środek, wyróżnione.get("koniec"))
    return _sklej([część for część in kolejność if część is not None])


def _zdania_pod(konstytuent):
    """Zdania stojące pod konstytuentem, czyli te, które niosą własny podmiot.

    Schodzi tak głęboko jak ``_wskazany``, czyli do roli i do roli pod przyimkiem,
    i z tego samego powodu: głębiej zdanie podrzędne nie ma po co stać,
    bo nie ma stamtąd jak nic wyprowadzić.
    """
    goły = _goły(konstytuent)
    if isinstance(goły, Okolicznik):
        if goły.zdarzeniem:
            yield goły.co
            return
        goły = goły.co
    if isinstance(goły, Opis):
        yield goły.zdanie


class Zdanie:
    """To, co orzeka o kimś: jedno zdarzenie albo kilka opowiedzianych naraz.

    Klasa ta jest tu po to, żeby dało się o nią zapytać.
    Okolicznik pyta, bo od tego zależy, czy jego słowo jest przyimkiem,
    czy spójnikiem, a lista kategorii wypisana obok rozjechałaby się
    z pierwszą kategorią dopisaną i tam niedopisaną.

    Wnosi jedno liczenie i żąda za nie trzech rzeczy, które daje każda kategoria:
    podmiotu, o którym zdanie orzeka, czasownika, którym orzeka,
    oraz konstytuentów, czyli tego, z czego się wypisuje.
    """

    @property
    def podmioty(self) -> tuple[Rola, ...]:
        """Role, które w tym zdaniu stoją jako podmiot, wraz z tymi ze zdań pod nim.

        Zdanie proste ma jeden podmiot, a złożone ma go tyle, ile ma zdarzeń,
        i wszystkie one są tym, na co czytelnik trafia,
        szukając podmiotu, którego zdanie obok nie wypisało.
        """
        pod = (
            rola
            for konstytuent in self.konstytuenty
            for niższe in _zdania_pod(konstytuent)
            for rola in niższe.podmioty
        )
        return (self.podmiot, *pod)

    def _orzeczenie(self, kontekst: Kontekst) -> str:
        """Czasownik w formie, której żąda podmiot, wraz z przeczeniem.

        Stoi tu, bo przeczenie stawia ``nie`` przed czasownikiem tak samo
        w zdaniu o czynności i w orzeczeniu imiennym.
        Różni je to, co przeczenie robi poza czasownikiem:
        dopełnienie traci biernik na rzecz dopełniacza, a orzecznik nie ma czego stracić,
        bo narzędnika przeczenie w polszczyźnie nie rusza.
        """
        forma = _forma(self.czasownik, self.podmiot, kontekst.czas)
        return f"nie {forma}" if self.przeczenie else forma


@dataclass(frozen=True)
class Jest(Zdanie):
    """Orzeczenie imienne: zwykły tekst polski jest wejściem.

    Orzecznik idzie w narzędniku, bo tyle bierze kopula.
    Szyk wychodzi z wyróżnień tak samo jak przy zdarzeniu,
    więc `Wejściem jest zwykły tekst polski.` jest tu orzecznikiem postawionym
    na czele wraz z podmiotem odesłanym na koniec, a nie wariantem linearyzacji.
    """

    co: Rola | Wyróżnienie
    czym: Rola | Wyróżnienie
    przeczenie: bool = False

    #: Lemat kopuli, wpisany na stałe, bo drzewo go nie niesie.
    #: Kopula jest tu jedna, a gramatyka bierze pięć; trzyma to ``TODO.md``.
    czasownik = "być"

    @property
    def podmiot(self) -> Rola:
        return _goły(self.co)

    @property
    def konstytuenty(self) -> tuple:
        return (self.co, self.czym)

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> Kawałek:
        return _szyk(
            [
                *_podmiot(self.co, kontekst),
                (None, Kawałek(self._orzeczenie(kontekst))),
                (
                    _miejsce(self.czym, kontekst),
                    _wypisz(_goły(self.czym), "inst", kontekst),
                ),
            ]
        )


@dataclass(frozen=True)
class Robi(Zdanie):
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

    Przeczenie stoi tu polem, a nie osobnym konstruktorem,
    bo sięga dwóch rzeczy naraz: stawia ``nie`` przed czasownikiem
    i zabiera dopełnieniu biernik na rzecz dopełniacza,
    a te dwie rzeczy są jedną decyzją i rozjechać się nie mogą.
    Pierwszą z nich robi ``Zdanie`` dla obu kategorii, a druga jest tutaj,
    bo orzeczenie imienne dopełnienia nie ma.
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
    def czasownik(self) -> str:
        """Lemat, którym to zdanie orzeka.

        Czyn jest kategorią dziedziny, a czasownik słowem, które z niej wychodzi,
        więc jedno pole odpowiada tu na dwa pytania i oba są nazwane:
        drzewo pisze się czynem, a o formę pyta się czasownika.
        """
        return self.czyn

    @property
    def podmiot(self) -> Rola:
        return _goły(self.kto)

    @property
    def konstytuenty(self) -> tuple:
        dopełnienie = () if self.co is None else (self.co,)
        return (self.kto, *dopełnienie, *self.okoliczniki)

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> Kawałek:
        pozycje = _podmiot(self.kto, kontekst)
        pozycje.append((None, Kawałek(self._orzeczenie(kontekst))))
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


def nie(zdanie: Jest | Robi) -> Jest | Robi:
    """To samo zdanie zaprzeczone.

    Konstruktorem to nie jest, tylko zmianą jednej cechy zdania,
    bo zaprzeczone zdanie ma te same role co twierdzące
    i drugi konstruktor kazałby wypisać je jeszcze raz.

    Sięga jednego orzeczenia, bo tyle znaczy ``nie`` w polszczyźnie,
    więc ciąg zdarzeń przeczy się zdarzenie po zdarzeniu,
    a nie w całości: `Nie podniosła deski i nie zeszła po schodach.`
    """
    return replace(zdanie, przeczenie=True)


@dataclass(frozen=True)
class Ciąg(Zdanie):
    """Kilka zdarzeń opowiedzianych jednym zdaniem: podniósł deskę i zszedł.

    Kategorią dziedziny jest tu następstwo, a nie spójnik.
    Autor mówi, że jedno stało się po drugim i że jest to jedna rzecz do opowiedzenia,
    a to, że wychodzi z tego ``i``, rozstrzyga linearyzacja,
    tak samo jak rozstrzyga przypadek.
    Węższe to jest niż polskie ``i``, które łączy także zdarzenia równoczesne,
    i węższe z rozmysłu: kolejność zdarzeń niesie tu kolejność zapisu,
    więc kategoria, która by o niej nie mówiła, kłamałaby o połowie swoich zdań.

    Od koordynacji bytów różni się tym, czego żąda opuszczenie podmiotu.
    Byty stoją w jednej roli i żaden z nich nie ma czasownika,
    a zdarzenia mają go po jednym, więc drugie z nich mówi o tym samym,
    o kim mówiło pierwsze, i podmiotu nie powtarza.
    Rozstrzyga o tym ``pomijalny`` niżej, czyli ten sam warunek,
    z którego korzysta akapit, bo pytanie jest jedno:
    czy czytelnik odzyska podmiot, którego nie ma.
    """

    zdarzenia: tuple

    @property
    def podmiot(self) -> Rola:
        return self.zdarzenia[0].podmiot

    @property
    def czasownik(self) -> str:
        return self.zdarzenia[0].czasownik

    @property
    def konstytuenty(self) -> tuple:
        return tuple(część for zdarzenie in self.zdarzenia for część in zdarzenie.konstytuenty)

    @property
    def podmioty(self) -> tuple[Rola, ...]:
        """Podmioty wszystkich zdarzeń, a nie samego pierwszego.

        Domyślne liczenie schodzi pod konstytuenty, a te ciąg ma sklejone,
        więc znalazłoby zdania pod zdarzeniami i minęłoby same zdarzenia.
        """
        return tuple(rola for zdarzenie in self.zdarzenia for rola in zdarzenie.podmioty)

    def linearyzuj(self, kontekst: Kontekst = TERAZ) -> Kawałek:
        poprzednie = self.zdarzenia[0]
        wypisane = [poprzednie.linearyzuj(kontekst)]
        for zdarzenie in self.zdarzenia[1:]:
            pomijany = pomijalny(zdarzenie, poprzednie, kontekst.czas)
            wypisane.append(zdarzenie.linearyzuj(replace(kontekst, pomijany=pomijany)))
            poprzednie = zdarzenie
        return _lista(wypisane)


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

    def linearyzuj(self, case: str, kontekst: Kontekst = TERAZ) -> Kawałek:
        """Rzecz, przecinek, zdanie o niej, a przecinek zamykający jako żądanie.

        Przypadek dostaje sama rzecz, bo to ona stoi w zdaniu nadrzędnym,
        a zdanie podrzędne rozdaje przypadki własne i dostaje od tego kontekstu
        czas oraz to, którą rzecz ma powiedzieć zaimkiem.
        Pomijanie podmiotu w nim nie działa, i to nie jest brak:
        podmiot opuszczony w zdaniu podrzędnym czytałby się jako ten,
        którego zaimek właśnie zastąpił.

        Przecinek otwierający staje tutaj, bo stoi w środku tego kawałka,
        a zamykający zostaje żądaniem, bo stoi na jego krańcu
        i rozstrzyga o nim to, co obok stanie.
        """
        wewnątrz = replace(kontekst, wskazywany=self.rzecz, pomijany=None)
        zdanie = replace(self.zdanie.linearyzuj(wewnątrz), przed=True)
        return replace(_sklej([_wypisz(self.rzecz, case, kontekst), zdanie]), po=True)


def pomijalny(zdanie: Zdanie, poprzednie: Zdanie | None, czas: str):
    """Podmiot, którego nie trzeba wypisywać, bo czytelnik odzyska go z czasownika.

    Warunków jest cztery i każdy chroni przed inną stratą.
    Podmiot bez tożsamości nie jest tym samym podmiotem, tylko takim samym,
    a podmiot inny niż w zdaniu obok odsyła czytelnika do kogoś, o kim nie mowa.
    Podmiot opisany zdaniem przepada wraz z opisem, czyli wraz z tym,
    co autor o nim akurat powiedział, więc opuszczeniem to nie jest.

    Czwarty warunek jest tym, którego reguła sama z siebie nie ma,
    a bez którego opuszczenie mówi co innego, niż mówił autor.
    Po opuszczonym podmiocie zostaje forma czasownika, więc podmiot wraca stamtąd
    tylko wtedy, gdy nikt inny tej samej formy z tego czasownika nie wyciąga.
    Skrzynia stojąca w piwnicy odbiera córce krawca rodzaj żeński,
    a bazyliszek odbiera czeladnikowi rodzaj męski,
    i wtedy podmiot staje wypisany, choć zdanie obok mówiło o tym samym.
    Liczone jest to tym samym czasownikiem, który podmiotu nie wypisze,
    bo różnice, których on nie robi, nie są różnicami dla czytelnika:
    czas przeszły rozdziela rodzaje, a teraźniejszy nie rozdziela żadnego.
    """
    podmiot = zdanie.podmiot
    tożsamość = podmiot.tożsamość
    if tożsamość is None or poprzednie is None:
        return None
    if poprzednie.podmiot.tożsamość is not tożsamość or isinstance(podmiot, Opis):
        return None
    forma = _forma(zdanie.czasownik, podmiot, czas)
    mylące = (
        rola
        for rola in (*poprzednie.podmioty, *zdanie.podmioty)
        if rola.tożsamość is not tożsamość
    )
    if any(_forma(zdanie.czasownik, rola, czas) == forma for rola in mylące):
        return None
    return tożsamość


def kompiluj(drzewo, kontekst: Kontekst = TERAZ) -> str:
    """Drzewo jako zdanie: wielka litera na początku i kropka na końcu.

    Wielkość litery należy do składu, a nie do lematu,
    bo ta sama rzecz stoi raz na początku zdania, a raz w jego środku.

    Przecinek, którego żądają krańce zdania, nie staje nigdzie,
    bo z jednej strony stoi kropka, a z drugiej nie stoi nic.
    Odjąć go stąd nie ma czego: żądanie krańca jest polem ``Kawałek``,
    a nie znakiem doklejonym do napisu.
    """
    tekst = drzewo.linearyzuj(kontekst).napis
    return f"{tekst[0].upper()}{tekst[1:]}."
