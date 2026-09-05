"""Werdykt o jednym zdaniu wraz z wierszami, którymi się go wypisuje.

:func:`werdykt` jest jedynym miejscem, które ten werdykt składa:
z rozbioru, z poprawki (``olski/werdykt/odrzucone.py``)
i z wykazów liczonych z lasu (``olski/werdykt/wykazy.py``).
Tamte dwa moduły o werdykcie nie wiedzą,
więc funkcja, która pyta werdykt gotowy, jest tutaj, a nie przy swoim temacie:
:func:`dalsze_zatrzymania` i :func:`niespełnione_żądania`
biorą :class:`Verdict` argumentem.
"""

from __future__ import annotations

from dataclasses import dataclass

from olski import cennik
from olski.document import SENTENCE_CLOSE
from olski.grammar import Grammar
from olski.morph import Segment
from olski.osoby import OSOBY_PROJEKTU, Osoby
from olski.parse import (
    PRZYŁĄCZONY_DO,
    Przyłączenie,
    Result,
    Rozbieżność,
    parse,
    streszczenia,
    streszczone,
)
from olski.segmentacja import bez_licencji, morphology, na_czym_stanęło
from olski.subset import (
    DEKLARACJA,
    GRAMMAR,
    NAZWY_SZKOLNE,
    ORZECZNIK_ŁĄCZNIKA,
    WYRAŻENIE_PRZYIMKOWE,
)
from olski.werdykt.odrzucone import Naprawa, _naprawa, _od_zatrzymania
from olski.werdykt.wykazy import (
    OdczytaniaFormy,
    Żądanie,
    _koszty_drzewa,
    _morfologia_zdania,
    _pod_streszczeniem,
    _zwinięte,
    _żądania_streszczenia,
)
from olski.żądania import żąda_osoby

#: Werdykt o tym, czego nikt nie napisał jako zdania: nagłówku, pozycji listy,
#: wierszu tabeli. Odrzucone znaczy „olski tego nie wyprowadza”, a to jest inne
#: zdanie o tekście i inna robota do zrobienia; docs/extraction.md trzyma wywód i
#: mierzy, jak dużą częścią rejestru ta klasa jest.
FRAGMENT = "fragment"

#: Werdykt o napisie, którego nic nie punktuje jako zdania, a który olski czyta,
#: kiedy się go domknie. Odcięty od :data:`FRAGMENT`, bo fragment jest aparatem
#: dokumentu, a ten napis jest zdaniem bez ostatniego znaku. Czemu mówi o napisie,
#: a nie o autorze, wywodzi docs/extraction.md.
NIEDOMKNIĘTE = "unclosed"


def _nierozstrzygnięte(przyłączenie: Przyłączenie) -> str:
    """Modyfikator i głowy, do których dochodzi, jako jeden wiersz werdyktu.

    Cudzysłów jest treścią, bo modyfikator jest ciągiem wziętym ze zdania i sam
    zawiera odstępy, więc bez niego nie widać, gdzie się kończy. Głowy dostają
    go tak samo, choć każda jest jednym słowem: pierwsze, co o nich trzeba
    wiedzieć, to że stoją w zdaniu tak, jak je autor napisał.
    """
    głowy = ", ".join(f"„{głowa}”" for głowa in przyłączenie.gospodarze)
    return f"„{przyłączenie.modyfikator}”{PRZYŁĄCZONY_DO}{głowy}"


def _odczytań(ile: int) -> str:
    """Liczba odczytań w formie, której polski liczebnik żąda po sobie.

    Formę wybiera jedno miejsce, bo werdykt nazywa tę liczbę w kilku wierszach.
    Nazwą jest odczytanie, a nie czytanie, i wywodzi to
    docs/subset.md#co-się-liczy-jako-jedno-odczytanie.
    """
    if ile == 1:
        return "jedno odczytanie"
    if ile % 10 in (2, 3, 4) and ile % 100 not in (12, 13, 14):
        return f"{ile} odczytania"
    return f"{ile} odczytań"


def _rozbieżny(rozbieżność: Rozbieżność) -> str:
    """Konstytuent i liczba jego czytań, jako jeden wiersz werdyktu.

    Wiersz ten mówi, gdzie w zdaniu leży wieloznaczność, której nie widać
    w streszczeniach czytań pod nim, i tylko tyle: różnicę autor odczyta z
    konstytuenta, a nazwana byłaby lematem, którego liczba czytań nie liczy
    (:class:`Rozbieżność`).
    """
    return f"„{rozbieżność.konstytuent}” ma {_odczytań(rozbieżność.ile)}"


def _po_szkolnemu(streszczenie: dict[str, str]) -> dict[str, str]:
    """To samo streszczenie nazwami, którymi te role nazywa składnia szkolna.

    Przekłada się samo zdanie z łącznikiem i poznaje się je po obsadzonym
    :data:`ORZECZNIK_ŁĄCZNIKA`, bo `podmiot` znaczy w nim co innego niż w zdaniu
    obok. Pytać trzeba przy tym o streszczenie, a nie o zdanie: `Ty to leń.` ma
    oba naraz, bo w jednym czytaniu `Ty` stoi przed łącznikiem, a w drugim jest
    zwykłym podmiotem. Sąd wykonywany przez ten przekład stoi przy
    :data:`NAZWY_SZKOLNE`.
    """
    if ORZECZNIK_ŁĄCZNIKA not in streszczenie:
        return streszczenie
    return {NAZWY_SZKOLNE.get(rola, rola): treść for rola, treść in streszczenie.items()}


def _nazwy_szkolne(rola: str) -> tuple[str, ...]:
    """Nazwy, pod którymi ta rola wychodzi z :func:`_po_szkolnemu`.

    Rola łącznika wychodzi pod dwiema, bo przekład rozdziela ją na podmiot i
    orzecznik: czytania różne tym, co obsadza pozycję przed łącznikiem, różnią
    się po przekładzie obiema.
    """
    if rola == ORZECZNIK_ŁĄCZNIKA:
        return (NAZWY_SZKOLNE[ORZECZNIK_ŁĄCZNIKA], NAZWY_SZKOLNE["podmiot"])
    return (rola,)


def _naprawiony(naprawa: Naprawa) -> str:
    """Poprawka jednego znaku jako wiersz werdyktu.

    Wiersz zaczyna się liczbą odczytań tak samo jak wiersz o wieloznaczności, bo
    obydwa mówią najpierw to samo: ile odczytań olski nad tym zdaniem ma.
    """
    return f"{_odczytań(naprawa.czytań)} po poprawce jednego znaku: {naprawa.poprawka}"


@dataclass(frozen=True)
class Verdict:
    """What olski says about one sentence."""

    #: Zdanie tak, jak stoi w tekście. Segmenty są krawędziami grafu, a nie
    #: listą, więc sklejone dają naraz każdy podział, jaki Morfeusz na formie
    #: widzi: ``ktoś`` wychodzi wtedy jako ``kto ktoś ś``.
    text: str
    result: Result
    #: Formy nie do ominięcia, którym żadna produkcja nie bierze ani jednego
    #: czytania: odrzucenie stanęło na nich, a nie na strukturze. Pola bez
    #: wartości domyślnej, bo pusta krotka jest tu twierdzeniem o zdaniu, a
    #: ``Nowa program zapisuje ustawienia.`` ma je puste i jest odrzucone.
    nielicencjonowane: tuple[str, ...]
    #: Forma, której nie wzięła ani jedna analiza częściowa, czyli miejsce, na
    #: którym odrzucenie stanęło; ``None``, gdy analiza doszła do ostatniego
    #: znaku zdania. Pola bez wartości domyślnej z tego samego powodu co wyżej:
    #: ``None`` jest tu twierdzeniem, a nie brakiem odpowiedzi.
    #: Twierdzeniem jest tylko wtedy, gdy o zatrzymanie pytano.
    #: Przebieg, który nie pytał (:func:`werdykt`), zostawia tu również ``None``.
    #: Rozdziela te dwa ``Result.furthest`` i o niego pyta :meth:`explain`.
    zatrzymanie: str | None
    #: Poprawka jednego znaku, po której olski ten napis czyta, albo ``None``.
    #: Pole, a nie właściwość, bo :func:`olski.werdykt.odrzucone._naprawa`
    #: kosztuje rozbiór, a właściwość płaciłaby tyle razy, ile razy ktoś ją przeczyta.
    naprawa: Naprawa | None

    @property
    def punktowane(self) -> bool:
        """Czy tekst punktuje ten napis jako zdanie.

        Mianownik pomiaru pyta o to, a nie o :attr:`status`, bo odpowiedź jest ta
        sama nad oboma werdyktami o napisie niepunktowanym i nie kosztuje rozbioru,
        którego kosztuje :attr:`domknięcie`
        (:class:`olski.werdykt.tekst.Podsumowanie`).
        """
        return bool(SENTENCE_CLOSE.search(self.text))

    @property
    def zgłoszenie(self) -> bool:
        """Czy narzędzie ma o tym zdaniu coś do powiedzenia.

        Zgłoszenia widoczne z jednego zdania są dwa: wieloznaczność oraz poprawka
        jednego znaku, a znaleziskiem jest tylko druga
        (docs/subset.md#wieloznaczność-jest-odpowiedzią-a-nie-znaleziskiem).
        Zaimek wskazujący na dwie rzeczy naraz pada obok werdyktu,
        bo rzeczy nazywa zdanie obok (``olski/odniesienia.py``), więc tutaj go nie ma.
        Warunek stoi tu raz, bo pyta o niego wydruk nad każdym zdaniem osobno;
        :class:`olski.werdykt.tekst.Podsumowanie` liczy każde z tych zgłoszeń
        nad tekstem i liczy je osobno.

        Napis niepunktowany zostaje poza zgłoszeniem także wtedy, gdy poprawkę
        ma, bo nagłówek i pozycja listy dochodzą tu jako takie napisy i żadne z
        nich nie jest zdaniem, którego autor nie domknął
        (docs/extraction.md); wydruk pokazuje je do flagi ``--zatrzymania``.
        """
        return self.punktowane and (self.result.ambiguous or self.naprawa is not None)

    @property
    def czytane(self) -> bool:
        """Czy olski to zdanie czyta.

        Nieczytane są trzy: zdanie odrzucone, napis, którego nic nie domyka,
        i fragment. O polszczyźnie żadnego z nich olski nie orzeka,
        więc wydruk milczy o nich do flagi (``olski/check.py``).
        """
        return self.punktowane and not self.result.rejected

    @property
    def status(self) -> str:
        """Klasa, do której werdykt to zdanie liczy, czyli słowo pomiaru.

        Wydruk komendy go nie podaje, bo dzieli zdania po liczbie odczytań,
        a nie po tym, czy narzędzie ma o zdaniu co powiedzieć (:attr:`znalezisko`).
        Czytają je pomiar pokrycia (``olski/pokrycie.py``), sondy w ``harness/``
        i znaczek na stronie (``witryna/skrypt.js``).
        """
        if not self.punktowane:
            return NIEDOMKNIĘTE if self.naprawa else FRAGMENT
        return self.result.status

    @property
    def readings(self) -> list[tuple[dict[str, str], ...]]:
        """Streszczenia odczytań, każde raz (:func:`streszczenia`).

        Odczytanie jest krotką streszczeń, po jednym na zdanie składowe, więc
        wpisem tej listy jest krotka, a nie jedno streszczenie.

        Lista jest po to, żeby pokazać różnicę między odczytaniami,
        a różnicę spoza zasięgu streszczenia nazywa wiersz o konstytuencie
        (:func:`_rozbieżny`), więc powtórzony napis nie zostawia jej nienazwanej.
        Liczbę odczytań podaje las (:attr:`Result.ile`),
        więc skrócenie tej listy jej nie rusza.
        """
        return [
            tuple(map(_po_szkolnemu, streszczenie))
            for streszczenie in streszczenia(self.result.readings, DEKLARACJA)
        ]

    @property
    def morfologia(self) -> list[tuple[OdczytaniaFormy, ...]]:
        """Czym formy stoją w każdym odczytaniu: wpis na streszczenie z :attr:`readings`.

        Po co ta odpowiedź autorowi, mówi
        docs/pisanie-po-olsku.md#skąd-bierze-się-odczytanie-którego-autor-nie-widzi.

        Wiersz dostaje forma czytana więcej niż jednym sposobem, a odczytania w
        nim licencjonują ją w tym kształcie (:attr:`olski.parse.Leaf.odczytania`);
        wiersze składa :func:`olski.werdykt.wykazy._pod_streszczeniem`,
        a nad streszczeniem, które zbiera kilka kształtów,
        bierze odczytania z każdego z nich.
        Wpisów jest tyle, ile streszczeń, więc nad zdaniem urwanym na
        :data:`olski.parse.MAX_READINGS` mówią one o odczytaniach wypisanych.

        Zdanie bez ani jednego odczytania dostaje jeden wpis, a w nim każde
        odczytanie każdej formy (:func:`olski.werdykt.wykazy._morfologia_zdania`):
        odsiać ich nie ma czym.
        Rozstrzyga się to tutaj, a nie w wydruku, bo wydruki są dwa
        (``olski/check.py`` i ``witryna/werdykty.py``) i rozjechałyby się po cichu.
        """
        if self.result.rejected or not self.punktowane:
            return [_morfologia_zdania(self.text)]
        return [
            _pod_streszczeniem(drzewa)
            for _streszczenie, drzewa in streszczone(self.result.readings, DEKLARACJA)
        ]

    @property
    def rachunki(self) -> list[tuple[tuple[str, int], ...]]:
        """Za co płaci każde odczytanie: wpis na streszczenie z :attr:`readings`.

        Wychodzą stąd pozycje policzone, a nie ich suma, bo kolejność czytań
        rozstrzyga koszt czytany od góry drzewa
        (``test_koszt_produkcji_nie_sumuje_się_do_kosztu_rodzica``),
        więc suma czytałaby się na miejsce w kolejce, którym nie jest.

        Streszczenie zbiera czasem kilka kształtów, a rachunek jest tego, który
        wyszedł z lasu pierwszy, czyli tego, przez którego to streszczenie stoi
        tam, gdzie stoi.
        """
        return [
            cennik.rachunek(_koszty_drzewa(drzewa[0]))
            for _streszczenie, drzewa in streszczone(self.result.readings, DEKLARACJA)
        ]

    @property
    def żądania(self) -> list[tuple[Żądanie, ...]]:
        """Czego czasownik żąda od obsadzonych pozycji: wpis na streszczenie z :attr:`readings`.

        Po co ta odpowiedź autorowi i czego ona nie mówi, wywodzi
        ``olski/żądania.py``; wpis jest na streszczenie z tego samego powodu, co
        przy :attr:`morfologia`, i grupuje go to samo pytanie o las.

        Warunku na zdanie odrzucone nie ma i nie ma go czemu stawiać: pozycję
        obsadza czytanie, a takie zdanie nie ma ani jednego, więc lista wychodzi
        stąd pusta sama. Morfologia ma tam wpis, bo mówi o formach, a nie o rolach.
        """
        return [
            _żądania_streszczenia(drzewa)
            for _streszczenie, drzewa in streszczone(self.result.readings, DEKLARACJA)
        ]

    @property
    def rozbieżne(self) -> list[Rozbieżność]:
        """Konstytuenty rozbieżne, którym streszczenia naprawdę się różnią.

        Jedno streszczenie znaczy, że streszczenie tej różnicy nie widzi
        (:class:`Rozbieżność`), a wypisane byłoby wierszem bez treści.
        Warunek stoi tu raz na oba wydruki, na wiersz poleceń i na witrynę,
        bo napisany dwa razy rozjechałby się po cichu.
        """
        return [r for r in self.result.rozbieżności if len(r.czytania) > 1]

    def explain(self) -> str:
        #  Poprawka wyprzedza każde inne wyjaśnienie i wyprzedza je nad zdaniem
        #  odrzuconym tak samo jak nad napisem niedomkniętym: zatrzymanie mówi,
        #  dokąd doszła analiza, a poprawka mówi, co z tym zrobić.
        if self.naprawa is not None:
            return _naprawiony(self.naprawa)
        if self.status == FRAGMENT:
            return "to nie zdanie: nic go nie punktuje jako zdania"
        if self.result.valid:
            return _odczytań(1)
        if self.result.rejected:
            if self.nielicencjonowane:
                # Cudzysłów jest treścią: najczęstszą formą bez licencji jest
                # przecinek, a lista rozdzielana przecinkami gubi bez niego granice.
                formy = ", ".join(f"„{forma}”" for forma in self.nielicencjonowane)
                return f"brak odczytania: żadna produkcja nie bierze {formy}"
            if self.result.furthest is None:
                #  Tak samo odmawia ``bloker`` w ``olski/pokrycie.py`` i z tego
                #  samego powodu: milczenie o zatrzymaniu czytałoby się tu jako
                #  zdanie o analizie, która doszła do końca.
                raise ValueError(
                    "wyjaśnienie odrzucenia nazywa miejsce zatrzymania, "
                    "a ten przebieg o zatrzymanie nie pytał (werdykt w olski/werdykt/zdanie.py)"
                )
            if self.zatrzymanie is None:
                return "brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania"
            return f"brak odczytania: analiza staje na „{self.zatrzymanie}”"
        przyłączenia = self.result.przyłączenia
        # Przekład idzie i tutaj (:func:`_nazwy_szkolne`), bo wiersz ten nie ma
        # nazywać roli, której lista czytań pod nim nie nazywa.
        różne = sorted(
            {
                nazwa
                for role in self.result.różniące
                # Przyłączenie nazwane niżej mówi o tej roli więcej niż sama jej
                # nazwa, więc wypisana obok byłaby tym samym zdaniem dwa razy.
                if not (przyłączenia and role == WYRAŻENIE_PRZYIMKOWE)
                for nazwa in _nazwy_szkolne(role)
            }
        )
        # Liczba i role wychodzą z lasu, więc granica wyliczania sięga listy
        # czytań i nie sięga tego wiersza: liczba jest liczbą, a nie „64+”.
        wiersz = _odczytań(self.result.ile)
        if różne:
            # Dwukropek oddziela nazwy od zdania: bez niego „różne w dopełnienie”
            # czyta się jak rzeczownik, którego przyimek nie odmienił.
            wiersz += f", różne w {'roli' if len(różne) == 1 else 'rolach'}: {', '.join(różne)}"
        return "; ".join(
            [
                wiersz,
                *map(_nierozstrzygnięte, przyłączenia),
                *map(_rozbieżny, self.result.rozbieżności),
            ]
        )


def werdykt(
    zdanie: str,
    segmenty: list[Segment],
    grammar: Grammar | None = None,
    zatrzymanie: bool = True,
) -> Verdict:
    """Werdykt o zdaniu już zsegmentowanym, wraz z całym podsumowaniem.

    Segmenty przychodzą argumentem, a nie powstają tutaj, bo zależą od napisu, a
    nie od gramatyki: kto pyta o jedno zdanie kilka gramatyk — sonda różnicowa
    nad prozą — segmentuje je raz i pyta tyle razy, ile ma wariantów.

    Zatrzymanie jest najdroższym z podsumowań i jedynym, które wolno pominąć.
    Nad zdaniem odrzuconym przechodzi tablicę drugi raz
    i unifikuje przy tym przebyte ciała (:func:`olski.parse.podsumuj`),
    a nad prozą, której olski w większości nie wyprowadza,
    odrzuconych jest osiem zdań na dziesięć,
    więc waży w takim przebiegu więcej niż każde inne podsumowanie.
    Czytają je :meth:`Verdict.explain` i kolejka blokerów (``olski/pokrycie.py``);
    kto go nie czyta, prosi o werdykt bez niego.

    Flagą, a nie pytaniem leniwym: ``Result`` trzymający las liczyłby punkt przy
    pierwszym pytaniu, ale przebieg nad bankiem drzew pyta o niego przy każdym
    zdaniu odrzuconym, a las porzuca rozmyślnie, bo waży tyle, ile jego tablica
    (``zmierz_zdanie`` w ``harness/pomiar.py``).

    Napis bez znaku kończącego pyta o zatrzymanie mimo flagi, bo od niego zależy
    wtedy sam status: poprawki domykającej szuka się nad analizą, która doszła
    do końca (:func:`olski.werdykt.odrzucone._naprawa`),
    a nad napisem punktowanym nie szuka się jej wcale.
    """
    grammar = grammar or GRAMMAR
    pytane = zatrzymanie or not SENTENCE_CLOSE.search(zdanie)
    result = parse(grammar, segmenty, deklaracja=DEKLARACJA, zatrzymanie=pytane)
    stanęło = na_czym_stanęło(segmenty, result.furthest) if pytane else None
    #  Brak formy jest dojściem do końca dopiero wtedy, gdy pytano:
    #  bez pytania ``stanęło`` jest puste także nad analizą, która stanęła.
    doszło_do_końca = pytane and stanęło is None
    nielicencjonowane = bez_licencji(segmenty, grammar)
    return Verdict(
        text=zdanie,
        result=result,
        nielicencjonowane=nielicencjonowane,
        zatrzymanie=stanęło.form if stanęło is not None else None,
        naprawa=_naprawa(zdanie, grammar, result.rejected, nielicencjonowane, doszło_do_końca),
    )


def dalsze_zatrzymania(verdict: Verdict, grammar: Grammar | None = None) -> tuple[str, ...]:
    """Zatrzymania tego zdania poza tym, które nazwał już werdykt.

    Zdanie z czytaniem nie stanęło nigdzie, więc krotka jest wtedy pusta, i tak
    samo pusta jest nad fragmentem. Segmentacja idzie tu drugi raz, bo werdykt
    segmentów nie niesie (:func:`werdykt`).

    Pierwsze zatrzymanie bierze się z ``Result.furthest``, a nie z rozbioru:
    werdykt tę liczbę już policzył,
    a rozbiór po całym zdaniu jest najdroższy z całej pętli.
    Węzeł stamtąd nazywa tutaj tę samą krawędź,
    bo oba wołania :func:`olski.segmentacja.morphology` biorą ten sam napis.
    """
    if not verdict.punktowane or not verdict.result.rejected:
        return ()
    if verdict.result.furthest is None:
        #  Tak samo odmawiają ``Verdict.explain`` i ``bloker`` (``olski/pokrycie.py``):
        #  krotka pusta czytałaby się jak zdanie stające raz.
        raise ValueError(
            "zatrzymania dalsze liczą się od pierwszego, "
            "a ten przebieg o zatrzymanie nie pytał (werdykt w olski/werdykt/zdanie.py)"
        )
    segmenty = morphology(verdict.text)
    stanęło = na_czym_stanęło(segmenty, verdict.result.furthest)
    return _od_zatrzymania(segmenty, grammar or GRAMMAR, stanęło)[1:]


def niespełnione_żądania(
    verdict: Verdict, deklaracja: Osoby = OSOBY_PROJEKTU
) -> tuple[Żądanie, ...]:
    """Pozycje, w których czasownik żąda kogoś, a nikt w nich nie stoi.

    Obie połowy pytania spotykają się tutaj: żądanie przychodzi z pliku żądań
    (:func:`olski.żądania.żąda_osoby`), a spełnienie z deklaracji projektu
    (``olski/osoby.py``). Wiersz zostaje po tej pozycji, której żądania nie
    spełnia nic z tego, czym jest jej głowa.

    **Wiersz jest o zdaniu, a nie o odczytaniu**, i tym różni się ten wykaz od
    :attr:`Verdict.żądania`. Pozycję obsadza czytanie, więc wiersz mówi tyle,
    że w którymś z nich stoi rzecz tam, gdzie czasownik żąda kogoś. Zdanie
    wieloznaczne ma czytań kilkanaście, a wiersz o jednej pozycji w każdym z nich
    ten sam, więc wykaz na odczytanie kazałby przeczytać kilkanaście kopii
    jednego wiersza.
    """
    return tuple(
        żądanie
        for żądanie in _zwinięte(żądanie for tabela in verdict.żądania for żądanie in tabela)
        if żąda_osoby(żądanie.klasy) and not deklaracja.nazywają(żądanie.lematy)
    )
