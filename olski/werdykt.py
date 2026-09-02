"""Werdykt o zdaniu: znalezisko wraz z tym, co autor ma przeczytać.

Werdykt mówi o zdaniu więcej niż to, do której klasy je liczy,
bo autor ma na niego zareagować.
Zdanie o dwóch odczytaniach jest znaleziskiem
(docs/subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego),
a :meth:`Verdict.explain` pokazuje, gdzie te odczytania się rozchodzą;
znaleziskiem jest też zdanie, które od odczytania dzieli jeden znak
(:class:`Naprawa`);
zdanie odrzucone dostaje miejsce, na którym rozbiór stanął,
a :func:`zatrzymania` każde takie miejsce, bo pierwsze zasłania następne.
Skąd te odczytania się biorą, mówi ``Verdict.morfologia``:
rozchodzą się w rolach, a zaczynają w lemacie i znaczniku formy.

Kto pyta o cały tekst, dostaje :func:`check` i :class:`Podsumowanie`,
czyli tyle werdyktów, ile zdań, oraz jedną odpowiedź policzoną z nich regułą.

Warstwa ta ani nie wnosi wieloznaczności, ani jej nie zdejmuje,
bo jest wypowiedzią o warstwach pod nią (docs/architecture.md).
Gramatykę czyta gotową z ``olski/subset/``,
a segmentację, po której werdykt pada, z ``olski/segmentacja.py``.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field, replace

from olski.document import SENTENCE_CLOSE
from olski.grammar import Grammar
from olski.lematy import (
    LEMAT_PRZECZENIA,
    LEMAT_ZWROTNY,
    ZAMIENNIKI_CUDZYSŁOWU,
    ZNAK_CUDZYSŁOWU_OTWIERAJĄCY,
    ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY,
)
from olski.morph import Reading, Segment
from olski.osoby import OSOBY_PROJEKTU, Osoby
from olski.parse import (
    PRZYŁĄCZONY_DO,
    Node,
    Przyłączenie,
    Result,
    Rozbieżność,
    liście,
    parse,
    sklej_formy,
    streszczenia,
    streszczone,
    w_zakresie,
    zakresy,
)
from olski.segmentacja import bez_licencji, morphology, na_czym_stanęło, sentences
from olski.subset import (
    DEKLARACJA,
    GRAMMAR,
    NAZWY_SZKOLNE,
    ORZECZNIK_ŁĄCZNIKA,
    WYRAŻENIE_PRZYIMKOWE,
)
from olski.walencja import BIERNIK, CZASOWNIK, CZASOWNIK_ZWROTNY, DOPEŁNIACZ, PODMIOT
from olski.żądania import NIENAZWANE, PRZYPADKI, żąda_osoby, żądane

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

#: Znaki, którymi :func:`_domknięcie` domyka napis, wraz z nazwą, pod którą
#: werdykt je wypisuje; kolejność jest kolejnością prób. Wykrzyknika nie ma, bo
#: terminal końca zdania bierze każdy z trzech, więc kropka zamyka każde
#: czytanie, które zamknąłby on, i mówi przy tym o gramatyce, a nie o tonie
#: autora. Pytajnik jest, bo pytanie zamyka się tylko nim
#: (`KONIEC_ZDANIA` i `PYTAJNIK` w ``olski/subset/słowa.py``).
DOMKNIĘCIA = {".": "kropka na końcu", "?": "pytajnik na końcu"}

#: Symbole, na których staje zejście po role wiersza żądania: zdanie podrzędne
#: oraz konstytuent obsadzający ramę własnego czasownika
#: (:class:`olski.parse.Obsada`). Streszczenie staje na pierwszej z tych list,
#: a nie na drugiej, bo nazywa rolę wraz z wypełnieniem i nie pyta, czyja ona jest.
_STOP = (*DEKLARACJA.podrzędne, *DEKLARACJA.obsada.własna_rama)


@dataclass(frozen=True)
class Naprawa:
    """Poprawka jednego znaku, po której olski to zdanie czyta.

    Klasa jest jedna na wszystkie takie poprawki, bo autorowi mówią one to samo:
    olski tego zdania nie czyta, a od czytania dzieli je jeden znak. Świadkiem
    jest w każdej z nich gramatyka, bo poprawka wchodzi tutaj dopiero wtedy, gdy
    rozbiór poprawionego napisu daje odczytanie. Reguła stojąca na takim świadku
    nie żąda kalibracji, której brak zamknął pakiet reguł
    (docs/linter.md#co-zamknęło-pakiet-reguł).

    Liczba odczytań idzie razem z poprawką, bo policzona drugi raz żądałaby
    trzeciego rozbioru nad zdaniem, które werdykt rozebrał już dwa razy.
    """

    #: Co autor ma poprawić, tak jak to stoi w wierszu werdyktu.
    poprawka: str
    #: Liczba odczytań, które olski nad poprawionym napisem czyta.
    czytań: int


def _domknięcie(zdanie: str, grammar: Grammar) -> Naprawa | None:
    """Poprawka napisu, którego nic nie punktuje jako zdania: znak na jego końcu.

    Warunek na to pytanie stawia :func:`_naprawa`, bo drugi rozbiór jest tu
    całym kosztem.
    """
    for znak, poprawka in DOMKNIĘCIA.items():
        wynik = parse(grammar, morphology(zdanie + znak), deklaracja=DEKLARACJA)
        if not wynik.rejected:
            return Naprawa(poprawka, wynik.ile)
    return None


def _przecytowane(zdanie: str) -> str:
    """To samo zdanie cytowane parą znaków, którą bierze gramatyka.

    Który znak otwiera, a który zamyka, wychodzi z kolejności, a nie z samego
    znaku, bo cudzysłów maszynowy cytuje w obie strony. Apostrof w środku słowa
    tę kolejność przewraca i nie pilnuje tego nic: napis, który stąd wyjdzie,
    odczytania nie ma, więc poprawki :func:`_cudzysłów` z niego nie zrobi.
    """
    otwarty = False
    znaki: list[str] = []
    for znak in zdanie:
        if znak in ZAMIENNIKI_CUDZYSŁOWU:
            znaki.append(ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY if otwarty else ZNAK_CUDZYSŁOWU_OTWIERAJĄCY)
            otwarty = not otwarty
        else:
            znaki.append(znak)
    return "".join(znaki)


def _cudzysłów(
    zdanie: str, nielicencjonowane: tuple[str, ...], grammar: Grammar
) -> Naprawa | None:
    """Poprawka zdania, które cytuje znakiem spoza tego rejestru: para z gramatyki.

    Czemu poprawka dotyczy tego znaku, a nie łącznika, mówi
    docs/subset.md#poprawkę-jednego-znaku-poświadcza-gramatyka.

    Warunek tani stoi przed rozbiorem i pyta o pierwszy oraz ostatni znak formy
    bez licencji. Pyta o oba, bo Morfeusz scala cudzysłów pojedynczy ze słowem w
    jedną formę: ``'Zasad'`` wychodzi jednym segmentem. Nie pyta o samo
    zawieranie, bo apostrof w środku słowa nie cytuje, a ``fact's`` kosztowałby
    wtedy rozbiór.
    """
    if not any(
        forma[0] in ZAMIENNIKI_CUDZYSŁOWU or forma[-1] in ZAMIENNIKI_CUDZYSŁOWU
        for forma in nielicencjonowane
    ):
        return None
    poprawione = _przecytowane(zdanie)
    wynik = parse(grammar, morphology(poprawione), deklaracja=DEKLARACJA)
    if wynik.rejected:
        return None
    return Naprawa(
        f"cudzysłów {ZNAK_CUDZYSŁOWU_OTWIERAJĄCY} i {ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY}"
        " w miejsce tego, którym zdanie cytuje",
        wynik.ile,
    )


def _naprawa(
    zdanie: str,
    grammar: Grammar,
    odrzucone: bool,
    nielicencjonowane: tuple[str, ...],
    doszło_do_końca: bool,
) -> Naprawa | None:
    """Poprawka jednego znaku, po której olski ten napis czyta, albo ``None``.

    Poprawki są dwie, a pyta się o jedną z nich, bo każda kosztuje drugi rozbiór:
    napis bez znaku kończącego pyta o ten znak, a zdanie punktowane o cudzysłów.
    Rozłączności pilnuje sama gramatyka, bo napisu, któremu brakuje obu znaków,
    nie wyprowadzi żadna z tych poprawek z osobna, więc warunki niżej oszczędzają
    rozbiór, a nie strzegą odpowiedzi. Na tej rozłączności stoi
    :attr:`Verdict.status`: o niedomknięciu rozstrzyga tam sama obecność poprawki.

    Domknięcie żąda warunku tańszego jeszcze: analiza doszła do końca napisu i
    każda forma ma licencję. Warunek jest konieczny, bo czytanie nad napisem
    domkniętym bierze każdą formę, więc bierze ją i analiza częściowa nad napisem
    bez znaku. Nie wystarcza: analiza dochodzi do końca także tam, gdzie żadnego
    konstytuentu nie domyka.
    """
    if not odrzucone:
        return None
    if SENTENCE_CLOSE.search(zdanie):
        return _cudzysłów(zdanie, nielicencjonowane, grammar)
    if doszło_do_końca and not nielicencjonowane:
        return _domknięcie(zdanie, grammar)
    return None


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
    #: Pole, a nie właściwość, bo :func:`_naprawa` kosztuje rozbiór, a właściwość
    #: płaciłaby tyle razy, ile razy ktoś ją przeczyta.
    naprawa: Naprawa | None

    @property
    def punktowane(self) -> bool:
        """Czy tekst punktuje ten napis jako zdanie.

        Mianownik pomiaru pyta o to, a nie o :attr:`status`, bo odpowiedź jest ta
        sama nad oboma werdyktami o napisie niepunktowanym i nie kosztuje rozbioru,
        którego kosztuje :attr:`domknięcie` (:class:`Podsumowanie`).
        """
        return bool(SENTENCE_CLOSE.search(self.text))

    @property
    def znalezisko(self) -> bool:
        """Czy narzędzie ma o tym zdaniu coś do powiedzenia.

        Znaleziska są dwa: wieloznaczność oraz poprawka jednego znaku
        (docs/subset.md#wieloznaczność-jest-znaleziskiem-a-nie-definicją-olskiego).
        Warunek stoi tu raz, bo pyta o niego wydruk nad każdym zdaniem osobno;
        :class:`Podsumowanie` liczy oba znaleziska nad tekstem i liczy je osobno.

        Napis niepunktowany zostaje poza znaleziskiem także wtedy, gdy poprawkę
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
    def readings(self) -> list[dict[str, str]]:
        """Streszczenia odczytań, każde raz (:func:`streszczenia`).

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
        wiersze składa :func:`_pod_streszczeniem`, a nad streszczeniem, które
        zbiera kilka kształtów, bierze odczytania z każdego z nich.
        Wpisów jest tyle, ile streszczeń, więc nad zdaniem urwanym na
        :data:`olski.parse.MAX_READINGS` mówią one o odczytaniach wypisanych.

        Zdanie bez ani jednego odczytania dostaje jeden wpis, a w nim każde
        odczytanie każdej formy (:func:`_morfologia_zdania`): odsiać ich nie ma
        czym. Rozstrzyga się to tutaj, a nie w wydruku, bo wydruki są dwa
        (``olski/check.py`` i ``witryna/werdykty.py``) i rozjechałyby się po cichu.
        """
        if self.result.rejected or not self.punktowane:
            return [_morfologia_zdania(self.text)]
        return [
            _pod_streszczeniem(drzewa)
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
                    "a ten przebieg o zatrzymanie nie pytał (werdykt w olski/werdykt.py)"
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


def zatrzymania(segmenty: list[Segment], grammar: Grammar | None = None) -> tuple[str, ...]:
    """Każde zatrzymanie odrzuconego zdania, a nie samo pierwsze.

    Werdykt nazywa jedno miejsce (:func:`na_czym_stanęło`), a zdanie długie ma ich
    kilka i pierwsze zasłania resztę, więc kto pisze pod tę gramatykę, nie widzi z
    werdyktu, ile jeszcze poprawek to zdanie zabierze; po co ta odpowiedź jest,
    mówi docs/pisanie-po-olsku.md.

    Analiza rusza od nowa **za** formą zatrzymania, a nie na niej: formy, której
    nie wzięła żadna analiza częściowa, nie weźmie też analiza zaczęta od niej, a
    przebieg stałby na miejscu. Krawędź przekraczającą cięcie trzeba przy tym
    zdjąć, bo graf segmentacji rozchodzi się na kilka dróg — ``ktoś`` wychodzi
    także jako ``kto`` i ``ś`` — a takiej krawędzi nie ma z czym w kawałku złożyć.

    Cięcie nie wskazuje usterki ani granicy konstrukcji, tak samo jak jedno
    zatrzymanie jej nie wskazuje.
    """
    grammar = grammar or GRAMMAR
    formy: list[str] = []
    while segmenty:
        stanęło = na_czym_stanęło(segmenty, parse(grammar, segmenty).furthest)
        if stanęło is None:
            break
        formy.append(stanęło.form)
        segmenty = [
            replace(segment, start=segment.start - stanęło.end, end=segment.end - stanęło.end)
            for segment in segmenty
            if segment.start >= stanęło.end
        ]
    return tuple(formy)


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
    do końca (:func:`_naprawa`), a nad napisem punktowanym nie szuka się jej wcale.
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
    """
    if not verdict.punktowane or not verdict.result.rejected:
        return ()
    return zatrzymania(morphology(verdict.text), grammar)[1:]


@dataclass(frozen=True)
class OdczytaniaFormy:
    """Forma zdania wraz z odczytaniami, którymi tam stać może, każde napisem.

    Odczytanie jest napisem, a nie parą lematu i znacznika, bo oba wydruki
    wypisują je razem, a rozdzielone kazałyby każdemu z nich składać ten napis
    osobno.
    """

    forma: str
    odczytania: tuple[str, ...]


def _napisy(segment: Segment, odczytania: Iterable[Reading]) -> tuple[str, ...]:
    """Te odczytania jako napisy, każdy raz i w kolejności odczytań segmentu.

    Raz, bo lemat traci przy analizie indeks homonimu (:func:`olski.morph.analyse`),
    więc `Zamek` wychodzi z Morfeusza dwoma odczytaniami o jednym lemacie i jednym
    znaczniku, a wypisane oba czytają się jak pomyłka wydruku.

    Kolejność jest kolejnością segmentu, bo odczytania przychodzą tu zbiorem,
    z liści kilku drzew (:func:`_pod_streszczeniem`).
    """
    wybrane = set(odczytania)
    napisy: list[str] = []
    for czytanie in segment.readings:
        napis = f"{czytanie.lemma} {czytanie.tag}"
        if czytanie in wybrane and napis not in napisy:
            napisy.append(napis)
    return tuple(napisy)


def _pod_streszczeniem(drzewa: Iterable[Node]) -> tuple[OdczytaniaFormy, ...]:
    """Czym formy stoją pod tym streszczeniem: wiersz na formę, w porządku zdania.

    Rozpiętość liścia jest kluczem, bo forma powtórzona w zdaniu stoi w dwóch
    miejscach i każde bierze swoje odczytania: `koszt` przed dopełniaczem czyta
    się inaczej niż `koszt` w dopełnieniu.
    Zbiór wystarcza, bo kolejność wiersza bierze segment (:func:`_napisy`).
    """
    zebrane: dict[tuple[int, int], tuple[Segment, set[Reading]]] = {}
    for drzewo in drzewa:
        for liść in liście(drzewo):
            _segment, odczytania = zebrane.setdefault(liść.span, (liść.segment, set()))
            odczytania.update(liść.odczytania)
    return tuple(
        OdczytaniaFormy(segment.form, _napisy(segment, odczytania))
        for _span, (segment, odczytania) in sorted(zebrane.items())
        if len(segment.readings) > 1
    )


@dataclass(frozen=True)
class Żądanie:
    """Czego czasownik zdania żąda od tego, co w jego pozycji stanęło.

    Wiersz jest jeden na obsadzoną pozycję, a nie jeden na rolę, bo jedna rola
    obsadza czasem dwie pozycje naraz: `Autor doradza czytelnikowi poprawkę.`
    ma dopełnienie w celowniku obok dopełnienia w bierniku, a czasownik żąda
    od nich czego innego.
    """

    #: Rola, którą streszczenie nazywa to wypełnienie.
    rola: str
    #: Formy wypełnienia i forma czasownika, tak jak stoją w zdaniu.
    wypełnienie: str
    czasownik: str
    #: Żądane klasy jako alternatywa, nazwane przed nienazwanymi
    #: (:data:`olski.żądania.NIENAZWANE`), a w każdej z tych grup alfabetycznie.
    klasy: tuple[str, ...]
    #: Lematy głowy wypełnienia, czyli słowa, którymi ta pozycja stoi. O nie pyta
    #: deklaracja osób (``olski/osoby.py``), bo deklaruje się lemat, a nie formę.
    #: Poza porównaniem, bo wiersz jest o pozycji, a nie o głowie, i dwa kształty
    #: dają czasem tę samą pozycję o dwóch głowach (:func:`_zwinięte`).
    lematy: frozenset[str] = field(compare=False)


@dataclass(frozen=True)
class _Czasownik:
    """Czasownik zdania składowego: słowa, którymi bywa, jego forma i przeczenie."""

    #: Pary lematu i klasy słowa, czyli klucze, którymi pyta się pliku żądań.
    #: Jest ich kilka tam, gdzie formę licencjonuje w tym kształcie kilka odczytań.
    słowa: frozenset[tuple[str, str]]
    forma: str
    #: Czy przy tym czasowniku stoi przeczenie (:data:`olski.lematy.LEMAT_PRZECZENIA`).
    przeczony: bool


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


def _zwinięte(żądania: Iterable[Żądanie]) -> tuple[Żądanie, ...]:
    """Te żądania bez powtórzeń, z lematami zebranymi po wszystkich kształtach.

    Wiersz mówi o pozycji, a nie o głowie wypełnienia,
    więc pozycja, którą dwa kształty nazywają dwiema głowami, wychodzi stąd raz:
    podmiotem w `Wszystko to deklaruje REUSE.toml.` jest `wszystko` z określeniem
    `to` albo `to` z określeniem `wszystko`, a żądanie stoi w obu to samo.
    Lematy zbierają się wtedy tak, jak zbiera je żądanie po słowach czasownika
    (:func:`olski.żądania.żądane`), i deklaracja pyta o zbiór cały
    (:meth:`olski.osoby.Osoby.nazywają`).
    """
    zebrane: dict[Żądanie, frozenset[str]] = {}
    for żądanie in żądania:
        zebrane[żądanie] = zebrane.get(żądanie, frozenset()) | żądanie.lematy
    return tuple(replace(żądanie, lematy=lematy) for żądanie, lematy in zebrane.items())


def _żądania_streszczenia(drzewa: Iterable[Node]) -> tuple[Żądanie, ...]:
    """Żądania obsadzonych pozycji tych czytań, każde raz i rolami po kolei.

    Drzew jest kilka z tego samego powodu co w :func:`_pod_streszczeniem`:
    jedno streszczenie zbiera czasem kilka kształtów, a wiersz powtórzony nie
    mówi nic ponad ten nad sobą.

    Zdanie składowe pyta o swój czasownik osobno, tak samo jak osobno się
    streszcza, a zdania podrzędnego ta warstwa nie otwiera i z tego samego
    powodu: pozycje tamtego zdania są ramą tamtego czasownika
    (:attr:`olski.parse.Deklaracja.podrzędne`).
    """
    return _zwinięte(
        żądanie
        for drzewo in drzewa
        for zakres in zakresy(drzewo, DEKLARACJA.składowe)
        for żądanie in _żądania_składowego(drzewo, zakres)
    )


def _żądania_składowego(drzewo: Node, zakres: tuple[int, int]) -> Iterator[Żądanie]:
    """Żądania jednego zdania składowego, po jednym na obsadzoną pozycję."""
    obsada = DEKLARACJA.obsada
    czasownik = _czasownik(drzewo, zakres)
    if czasownik is None:
        return
    for rola in (obsada.podmiot, *obsada.przypadkowe):
        for węzeł in w_zakresie(drzewo, rola, _STOP, zakres):
            klasy = _żądane_od(węzeł, rola, czasownik)
            if klasy:
                głowa = węzeł.liść_głowy()
                yield Żądanie(
                    rola,
                    sklej_formy(węzeł.forms()),
                    czasownik.forma,
                    klasy,
                    frozenset(czytanie.lemma for czytanie in głowa.odczytania),
                )


def _czasownik(drzewo: Node, zakres: tuple[int, int]) -> _Czasownik | None:
    """Czasownik, który rządzi ramą tego zdania składowego, albo ``None``.

    ``None`` znaczy, że zdanie orzeka bez czasownika: orzeczeniem rzeczownikowym
    albo orzecznikiem przy kopuli, i ramy nie ma wtedy o co pytać.

    Cząstka zwrotna i przeczenie stoją w tym samym konstytuencie co czasownik —
    ``orzeczenie → się otwiera`` — więc obie widać po jego liściach.
    Pierwsza z nich czyni z niego inne słowo, więc wchodzi do klucza pliku żądań,
    a druga zostaje osobno, bo mówi o przypadku dopełnienia, a nie o słowie.
    """
    for rola in DEKLARACJA.obsada.orzeczenia:
        for węzeł in w_zakresie(drzewo, rola, _STOP, zakres):
            lematy = {czytanie.lemma for liść in liście(węzeł) for czytanie in liść.odczytania}
            klasa = CZASOWNIK_ZWROTNY if LEMAT_ZWROTNY in lematy else CZASOWNIK
            głowa = węzeł.liść_głowy()
            return _Czasownik(
                słowa=frozenset((czytanie.lemma, klasa) for czytanie in głowa.odczytania),
                forma=głowa.segment.form,
                przeczony=LEMAT_PRZECZENIA in lematy,
            )
    return None


def _żądane_od(węzeł: Node, rola: str, czasownik: _Czasownik) -> tuple[str, ...]:
    """Klasy, których czasownik żąda od tego wypełnienia; krotka pusta jest milczeniem.

    Pozycji kandydujących bywa kilka (:func:`_pozycje`), a wiersz wychodzi stąd
    dopiero wtedy, gdy żąda dokładnie jedna z nich: przy dwóch żądających nie
    widać, które z tych żądań autor ma przeczytać.
    """
    żądające = [
        klasy
        for pozycja in _pozycje(węzeł, rola, czasownik)
        if (klasy := żądane(czasownik.słowa, pozycja))
    ]
    if len(żądające) != 1:
        return ()
    return tuple(sorted(żądające[0], key=lambda klasa: (klasa in NIENAZWANE, klasa)))


def _pozycje(węzeł: Node, rola: str, czasownik: _Czasownik) -> tuple[str, ...]:
    """Pozycje ramy, w których to wypełnienie stać może.

    Podmiot nazywa swoją pozycję sam, a rola przypadkowa nazywa ją przypadkiem
    głowy wypełnienia: `ustawienia` w bierniku obsadza pozycję ``acc``.
    Przypadek bierze się z odczytań licencjonujących ten kształt, a nie z jednego
    z nich, bo forma bywa dwoma słowami naraz — `ustawienia` jest rzeczownikiem
    i odsłownikiem — i pozycję obsadza w obu tak samo.

    Pozycje są dwie tam, gdzie przy czasowniku stoi przeczenie: dopełnienie
    w bierniku staje pod nim w dopełniaczu
    (docs/konstrukcje-gramatyczne/orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem),
    więc dopełniacz nazywa tam obie pozycje naraz.
    """
    if rola == DEKLARACJA.obsada.podmiot:
        return (PODMIOT,)
    przypadki = frozenset.intersection(
        *(czytanie.tag.get("case") for czytanie in węzeł.liść_głowy().odczytania)
    )
    kandydaci = set(przypadki) & set(PRZYPADKI)
    if czasownik.przeczony and DOPEŁNIACZ in kandydaci:
        kandydaci.add(BIERNIK)
    return tuple(sorted(kandydaci))


def _morfologia_zdania(zdanie: str) -> tuple[OdczytaniaFormy, ...]:
    """Formy zdania wraz z każdym odczytaniem, jakie olski w nich czyta.

    Odsiewu gramatyką nie ma: wchodzi tu i odczytanie, po które nie sięga żaden
    terminal, a formę, której gramatyka nie bierze wcale, nazywa werdykt
    (:attr:`Verdict.nielicencjonowane`).
    Odczytania odsiane leksykalnie zdejmuje :func:`olski.segmentacja.morphology`,
    więc wykaz jest tym, co weszło do rozbioru.

    Segmentacja idzie tu drugi raz, bo werdykt segmentów nie niesie
    (:func:`werdykt`), a forma dzielona przez Morfeusza jeszcze inaczej dostaje
    tyle wierszy, ile podziałów ma w grafie (:attr:`Verdict.text`).
    """
    return tuple(
        OdczytaniaFormy(segment.form, _napisy(segment, segment.readings))
        for segment in morphology(zdanie)
    )


def check(text: str, grammar: Grammar | None = None) -> list[Verdict]:
    """Check every sentence of a text against the grammar."""
    return [werdykt(zdanie, morphology(zdanie), grammar) for zdanie in sentences(text)]


@dataclass(frozen=True)
class Podsumowanie:
    """Znaleziska nad tekstem i to, o czym olski milczy, dla tego, kto pyta o cały tekst.

    Liczby te wychodzą z werdyktów jedną regułą — fragment nie jest zdaniem, więc
    nie wchodzi do mianownika, a zdanie odrzucone jest milczeniem, dopóki nie ma
    poprawki — i pyta o nie więcej niż jeden wołający, więc policzone u każdego z
    nich rozjeżdżają się po cichu: mianownik mniejszy o fragment czyta się jak
    pomiar, a nie jak pomyłka.

    Zdanie naprawialne stoi w dwóch licznikach naraz, w :attr:`naprawialne` i w
    :attr:`bez_odczytania`, bo gramatyka go nie wyprowadza i pokrycie liczy je
    tak samo jak przedtem: znalezisko mówi o autorze, a nie o podzbiorze.
    """

    #: Zdania, czyli to, o czym werdykt orzeka: fragmentów nie ma tu ani w liczniku.
    zdań: int
    #: Zdania o kilku odczytaniach, czyli znaleziska wieloznaczności.
    wieloznaczne: int
    #: Zdania, które od odczytania dzieli jeden znak, czyli drugie ze znalezisk
    #: (:class:`Naprawa`). Liczba jest osobna od :attr:`wieloznaczne`, bo mówi o
    #: zdaniu rzecz przeciwną: tamto olski czyta i ma o nim za dużo do
    #: powiedzenia, a to zdanie czyta dopiero po poprawce.
    naprawialne: int
    #: Zdania, których gramatyka nie wyprowadza. Olski o nich milczy, a milczenie
    #: liczy się osobno, bo bez tej liczby przebieg nad tekstem, którego nie
    #: przeczytał, czytałby się jak czysty.
    bez_odczytania: int
    #: Napisy, których nic nie interpunkuje jako zdania. Liczba jest jedna na oba
    #: werdykty o takim napisie, :data:`FRAGMENT` i :data:`NIEDOMKNIĘTE`, bo o
    #: mianowniku rozstrzyga jedno i to samo: domknięcia nie postawił nikt.
    fragmentów: int

    @property
    def znalezisk(self) -> int:
        """Ile zdań tekstu narzędzie zgłasza, bez względu na to, które znalezisko.

        Pyta o to kod wyjścia (``olski/check.py``), bo o samym zgłoszeniu
        rozstrzyga tu jedno miejsce, a znalezisko dopisane później dostaje ten
        kod wyjścia razem z własnym licznikiem.
        """
        return self.wieloznaczne + self.naprawialne

    @classmethod
    def z_werdyktów(cls, werdykty: Sequence[Verdict]) -> Podsumowanie:
        zdania = [verdict for verdict in werdykty if verdict.punktowane]
        return cls(
            zdań=len(zdania),
            wieloznaczne=sum(verdict.result.ambiguous for verdict in zdania),
            naprawialne=sum(verdict.naprawa is not None for verdict in zdania),
            bez_odczytania=sum(verdict.result.rejected for verdict in zdania),
            fragmentów=len(werdykty) - len(zdania),
        )

    def explain(self) -> str:
        #  Wiersz jest listą par, a nie zdaniem: liczba stoi za dwukropkiem, więc
        #  nie żąda zgody od słowa przed sobą i nic tu się nie odmienia.
        podsumowanie = (
            f"zdań: {self.zdań}; wieloznaczne: {self.wieloznaczne};"
            f" bez odczytania: {self.bez_odczytania}"
        )
        #  Wiersz rośnie o tę parę dopiero tam, gdzie poprawka pada, bo nad
        #  tekstem bez ani jednej mówiłaby zero o znalezisku, którego nie ma.
        if self.naprawialne:
            podsumowanie += f"; do poprawki jednym znakiem: {self.naprawialne}"
        if self.fragmentów:
            #  Nie „fragmenty, które nie są zdaniami”: napis niedomknięty jest w tej
            #  liczbie, a werdykt nad nim mówi, że olski to zdanie czyta.
            podsumowanie += f"; fragmenty, których nic nie punktuje jako zdania: {self.fragmentów}"
        return podsumowanie
