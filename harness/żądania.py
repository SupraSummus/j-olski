"""Wydanie TEI Walentego odczytane do żądań, jakie pozycja schematu stawia.

Leksykon walencyjny mówi, co czasownik bierze, a nie mówi, czego od tego żąda:
wydanie tekstowe, z którego on powstaje (``harness/walenty.py``), warstwy
semantycznej nie ma. Niesie ją wydanie TEI z tej samej daty, gdzie rama nazywa
swoje argumenty rolą i żąda od każdego klasy rzeczy
(docs/prior-art.md#polish-language-resources).

Czytanie jest złączeniem trzech warstw, a nie odczytaniem wiersza, i to jest cała
różnica w koszcie wobec tamtego modułu. Argument niesie rolę i preferencję i stoi
w warstwie semantycznej; pozycja wraz z frazą stoi w warstwie składniowej; wiąże
je warstwa spięć, po jednym spięciu na parę argumentu z frazą. Rola dochodzi
przez to do pozycji, którą rozbiór naprawdę obsadził, a nie do samego lematu.

Wiersz wychodzi stąd jeden na rolę w pozycji, a nie jeden na schemat, i jest to ta
sama zgrubność, którą ma leksykon: olski nie ma czym powiedzieć, w którym
znaczeniu czasownik stoi, więc żądania jednej pozycji zbierają się w zbiór po
wszystkich ramach lematu. Zbiór ten jest alternatywą, a nie koniunkcją: pozycja
żądająca ludzi w jednym znaczeniu, a czegokolwiek w drugim, niesie oba żądania i
nie żąda przez to niczego.

Pozycje wychodzą stąd pod nazwami, które olski im daje, a dwie pod nazwami
Walentego, bo olski nie ma ich wcale. Podmiot ma u olskiego własną produkcję, a
nie pozycję ramy, więc zostaje przy ``subj``; pozycja przyimkowa nie jest u niego
pozycją ramy, bo wyrażenie przyimkowe przyłącza się wszędzie, gdzie polszczyzna
je stawia, więc zostaje przy ``prepnp`` wraz z samym przyimkiem. Przypadka nie ma
w tym napisie z tego samego powodu, z którego nie ma go w kolumnie przyimków
leksykonu (:data:`harness.walenty.PRZYIMKOWA`).

Okolicznika ten przekład nie bierze i jest to jego największy brak. Walenty pisze
go kształtem ``xp`` — ``xp(locat)`` jest okolicznikiem miejsca — a olski nie ma
takiej pozycji, więc żądanie dałoby się doprowadzić do zdania tylko przez
przyimek, którego ten kształt nie nazywa: nazywa go dopiero tabela rozwinięć z
tego samego wydania, a tam jedna pozycja miejsca rozwija się w trzydzieści
przyimków. Klasa ``MIEJSCE`` siedzi przy tym głównie na tych pozycjach, więc
żądanie przestrzeni fizycznej zostaje poza tym plikiem; co za tym idzie, trzyma
docs/walencja.md#żądanie-pozycji-jest-osobnym-plikiem-a-nie-kolumną-leksykonu.

Żądanie oparte o synsety plWordNetu nie ma klasy nazwanej, więc wychodzi stąd
sam znacznik (:data:`olski.żądania.NIENAZWANE`). Zbiór milczący o
takim żądaniu kłamałby dwa razy: pozycja żądająca w jednym znaczeniu synsetów, a
w drugim ludzi, wyglądałaby na żądającą samych ludzi, a pozycja żądająca samych
synsetów — na niczego nie żądającą. Czy słowo stojące w zdaniu do klasy należy,
orzeka i tak dopiero wordnet, którego to repozytorium nie ma
(docs/disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma).

Plik wejściowy nie stoi w repozytorium, tak samo jak wydanie tekstowe i bank
drzew, a polecenie wraz z adresem trzyma
docs/walencja.md#żądanie-pozycji-jest-osobnym-plikiem-a-nie-kolumną-leksykonu.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator, Sequence
from pathlib import Path
from typing import NamedTuple
from xml.etree import ElementTree as ET

from harness import walenty
from olski.walencja import (
    BEZOKOLICZNIK,
    BIERNIK,
    CELOWNIK,
    CZASOWNIK,
    CZASOWNIK_ZWROTNY,
    DOPEŁNIACZ,
    PODMIOT,
    PYTANIE_ZALEŻNE,
    ZDANIE_PODRZĘDNE,
)
from olski.żądania import RELACJA, SYNSETY

#: Przestrzeń nazw TEI wraz z przestrzenią, z której bierze się ``xml:id``.
#: Nazwy elementów przychodzą z parsera razem z nimi, więc każde szukanie je
#: dokleja.
TEI = "{http://www.tei-c.org/ns/1.0}"
IDENTYFIKATOR = "{http://www.w3.org/XML/1998/namespace}id"

#: Kwalifikator pewności schematu pod nazwą, którą temu samemu kwalifikatorowi
#: daje wydanie tekstowe. Nazwa jest tu potrzebna do jednego: kryterium, które
#: schematy ten rejestr czyta, ma jednego właściciela i jest nim
#: :data:`harness.walenty.BRANE`. Że kwalifikatory są tą samą szóstką, mówią ich
#: liczności: każda z sześciu jest w obu wydaniach inna i każda się zgadza.
PEWNOŚĆ = {
    "cer": "pewny",
    "unc": "wątpliwy",
    "col": "potoczny",
    "vul": "wulgarny",
    "dat": "archaiczny",
    "bad": "zły",
}

#: Wartość, którą TEI pisze prawdę pola dwuwartościowego. Pyta o nią zwrotność
#: schematu, czyli to, co wydanie tekstowe pisze cząstką przy lemacie.
PRAWDA = "true"

#: Pole, którym TEI nazywa pozycję podmiotu, i wartość, którą tam stawia. Reszta
#: pozycji stoi bez tego pola albo z ``obj``, a olski o tę drugą etykietę nie
#: pyta: biernik bywa u Walentego pozycją bez niej.
FUNKCJA = "function"

#: Kształt frazy imiennej, przyimkowej i zdaniowej, każdy nazwą, którą TEI pisze
#: w atrybucie typu. Bezokolicznik nazywa się tak samo w obu wydaniach, więc
#: bierze się go stamtąd, gdzie stoi kryterium (:data:`harness.walenty.BEZOKOLICZNIK`).
IMIENNA = "np"
PRZYIMKOWA = "prepnp"
ZDANIOWA = "cp"

#: Przypadek, którym pozycja podmiotowa mówi o mianowniku. Walenty pisze tam
#: przypadek strukturalny, tak samo jak w bierniku dopełnienia, więc podmiot
#: poznaje się po funkcji, a nie po przypadku, a ta para odcina pozycję
#: podmiotową obsadzoną przypadkiem innym: `dowiedzieć się` ma taką z celownikiem.
MIANOWNIKOWE = frozenset({"str", "nom"})

#: To, co Walenty pisze w nawiasie kształtu: przypadek grupy imiennej albo
#: spójnik zdania podrzędnego. Kształty tego wydania są jednym napisem, a TEI
#: trzyma każde z tych pól osobno, więc kryterium czyta się stąd, a nie pisze
#: drugi raz.
W_NAWIASIE = re.compile(r"\((.+)\)$")


def _w_nawiasie(kształty: Sequence[str] | str) -> frozenset[str]:
    """Zawartość nawiasu tych kształtów; kształt bez nawiasu nie wnosi nic."""
    napisy = (kształty,) if isinstance(kształty, str) else kształty
    return frozenset(
        trafienie.group(1) for trafienie in map(W_NAWIASIE.search, napisy) if trafienie is not None
    )


#: Przypadek grupy imiennej wraz z nazwą, którą tej pozycji daje olski. Pozycja
#: niepodmiotowa z przypadkiem strukturalnym jest u niego biernikiem, a
#: dopełniacz cząstkowy tą samą pozycją co dopełniacz żądany ramą; oba sądy
#: należą do :mod:`harness.walenty` i stąd się je czyta.
PRZYPADKI = {
    przypadek: pozycja
    for kształty, pozycja in (
        (walenty.BIERNIK, BIERNIK),
        (walenty.CELOWNIK, CELOWNIK),
        (walenty.DOPEŁNIACZ, DOPEŁNIACZ),
    )
    for przypadek in _w_nawiasie(kształty)
}

#: Spójnik zdania podrzędnego wraz z nazwą pozycji. Zdanie z `że` i pytanie
#: zależne są u olskiego dwiema pozycjami, a Walenty rozdziela je właśnie
#: spójnikiem; zdania spod innego spójnika olski nie ma czym wypisać.
SPÓJNIKI = {
    **dict.fromkeys(_w_nawiasie(walenty.ZDANIE), ZDANIE_PODRZĘDNE),
    **dict.fromkeys(_w_nawiasie(walenty.PYTANIE), PYTANIE_ZALEŻNE),
}


class Fraza(NamedTuple):
    """Fraza tak, jak TEI ją pisze: typ wraz z polami, o które olski pyta.

    Pola są trzy, bo tyle kształtów rozdziela wartość pola: grupę imienną
    przypadek, przyimkową przyimek, a zdanie podrzędne spójnik. Bezokolicznik ma
    pozycję jedną, więc wychodzi z samego typu, i tak samo z samego typu wychodzi
    każdy kształt, którego olski pozycją nie ma.
    """

    typ: str
    przypadek: str | None = None
    przyimek: str | None = None
    spójnik: str | None = None


def pozycja(fraza: Fraza, podmiotowa: bool) -> str | None:
    """Nazwa, którą olski daje pozycji o tej frazie, albo ``None``: pozycji nie ma.

    Pytanie idzie o frazę wraz z funkcją pozycji, a nie o samą frazę, bo
    przypadek strukturalny jest w podmiocie mianownikiem, a poza nim biernikiem
    (:data:`MIANOWNIKOWE`).

    ``None`` wraca z dwóch powodów naraz i rozdzielać ich nie ma po co: albo
    kształt nie jest żadnym z tych, które olski ma pozycją — okolicznik, zdanie
    pod zaimkiem, pozycja zleksykalizowana, cząstka zwrotna — albo jest nim, a
    stoi w nim wartość, której olski nie ma: narzędnik, bo `inst` jest u niego
    pozycją orzecznika (``olski/walencja.py``), albo spójnik spoza tych dwóch.
    """
    if podmiotowa:
        return PODMIOT if fraza.typ == IMIENNA and fraza.przypadek in MIANOWNIKOWE else None
    if fraza.typ == IMIENNA:
        return PRZYPADKI.get(fraza.przypadek)
    if fraza.typ == PRZYIMKOWA:
        return f"{PRZYIMKOWA}({fraza.przyimek})"
    if fraza.typ == walenty.BEZOKOLICZNIK:
        return BEZOKOLICZNIK
    if fraza.typ == ZDANIOWA:
        return SPÓJNIKI.get(fraza.spójnik)
    return None


def _pole(element: ET.Element, nazwa: str) -> ET.Element | None:
    """Pole struktury cech o tej nazwie, czyli ``<f name="...">``, albo ``None``."""
    return element.find(f'{TEI}f[@name="{nazwa}"]')


def _wartość(element: ET.Element, nazwa: str) -> str | None:
    """Wartość pola o tej nazwie, czyli atrybut symbolu albo wartości dwuwartościowej.

    Jedno czytanie na oba, bo pole niosące wartość niesie ją jednym dzieckiem, a
    o to, którym elementem TEI ją zapisało, olski nie pyta ani razu.
    """
    pole = _pole(element, nazwa)
    return pole[0].get("value") if pole is not None and len(pole) else None


def _zbiór(element: ET.Element, nazwa: str) -> list[ET.Element]:
    """Elementy zbioru, który stoi w polu o tej nazwie; pola bez zbioru dają pustą listę."""
    pole = _pole(element, nazwa)
    return list(pole[0]) if pole is not None and len(pole) else []


def _wskazany(element: ET.Element) -> str:
    """Identyfikator, na który ten element wskazuje, albo pusty napis.

    Spięcie nie powtarza argumentu ani frazy, tylko wskazuje je przez ``sameAs``
    wraz z krzyżykiem, którym TEI otwiera odnośnik; identyfikator stoi po nim.
    Czytają to obie strony spięcia, więc czytanie jest jedno.
    """
    return element.get("sameAs", "").lstrip("#")


def _odnośnik(element: ET.Element, nazwa: str) -> str:
    """Identyfikator, na który wskazuje pole o tej nazwie; pole puste daje pusty napis."""
    pole = _pole(element, nazwa)
    return _wskazany(pole[0]) if pole is not None and len(pole) else ""


def _fraza(element: ET.Element) -> Fraza:
    """Ta fraza jako :class:`Fraza`.

    Spójnik stoi o jedno zagłębienie niżej niż przypadek i przyimek, bo TEI pisze
    typ zdania podrzędnego własną strukturą cech: to w niej stoi pole spójnika.
    """
    typ = _pole(element, "type")
    return Fraza(
        typ=element.get("type", ""),
        przypadek=_wartość(element, "case"),
        przyimek=_wartość(element, "preposition"),
        spójnik=_wartość(typ[0], "conjunction") if typ is not None and len(typ) else None,
    )


def _pozycje_schematów(warstwa: ET.Element) -> dict[str, tuple[bool, str]]:
    """Fraza po identyfikatorze: zwrotność jej schematu i nazwa pozycji, w której stoi.

    Klucz jest identyfikatorem frazy, bo tym właśnie wskazuje ją spięcie. Zbiera
    się je z góry, a nie schodzi się do nich po spięciu, bo warstwa spięć stoi w
    pliku za składniową i wskazuje w nią wstecz.

    Schemat spoza :data:`harness.walenty.BRANE` odpada cały wraz ze swoimi
    pozycjami, tak samo jak odpada w tamtym module: nazywa on polszczyznę, której
    ten rejestr nie pisze, więc żądanie z niego mówiłoby o czasowniku rzecz,
    której nikt tu nie napisze.

    Fraza, której olski nie ma pozycją, nie wchodzi wcale, i o jedno pytanie
    mniej ma przez to złączenie: wskazanie w nią kończy się tutaj, a nie przy
    wierszu.
    """
    zebrane: dict[str, tuple[bool, str]] = {}
    for schemat in _zbiór(warstwa, "schemata"):
        if PEWNOŚĆ[_wartość(schemat, "opinion")] not in walenty.BRANE:
            continue
        zwrotny = _wartość(schemat, "reflexive_mark") == PRAWDA
        for pozycja_schematu in _zbiór(schemat, "positions"):
            podmiotowa = _wartość(pozycja_schematu, FUNKCJA) == PODMIOT
            for element in _zbiór(pozycja_schematu, "phrases"):
                nazwa = pozycja(_fraza(element), podmiotowa)
                identyfikator = element.get(IDENTYFIKATOR)
                if nazwa is not None and identyfikator:
                    zebrane[identyfikator] = (zwrotny, nazwa)
    return zebrane


def _żądane(argument: ET.Element) -> frozenset[str]:
    """Klasy, których ten argument żąda, wraz ze znacznikiem żądania nienazwanego.

    Zbiór pusty znaczy, że rama nazywa rolę i klasy nie żąda; znacznik znaczy, że
    żąda klasy, której ten plik nie umie nazwać (:data:`SYNSETY`).
    """
    preferencje = _pole(argument, "sel_prefs")
    if preferencje is None or not len(preferencje):
        return frozenset()
    grupy = preferencje[0]
    nazwane = {symbol.get("value", "") for symbol in _zbiór(grupy, "predefs")}
    nienazwane = {
        znacznik
        for znacznik, pole in ((SYNSETY, "synsets"), (RELACJA, "relations"))
        if _zbiór(grupy, pole)
    }
    return frozenset(nazwane | nienazwane)


def _argumenty(warstwa: ET.Element) -> dict[str, tuple[str, frozenset[str]]]:
    """Argument po identyfikatorze: jego rola i to, czego on żąda.

    Rola wychodzi jednym napisem wraz ze swoim uszczegółowieniem, bo to ono
    rozdziela dwie strony jednego zdarzenia: `wynająć` ma inicjatora będącego
    źródłem i inicjatora będącego celem, czyli tego, kto wynajmuje, i tego, komu
    się wynajmuje.

    Argument bez roli nie wchodzi. Jest ich w tym wydaniu kilkaset, żądają one
    samej relacji do argumentu obok i ani jeden nie ma spięcia, więc odsiew ten
    nie zabiera żadnego wiersza; opinii ramy zaś nie czyta nikt, bo mówi ona o
    tym, jak pewne jest znaczenie, a nie o tym, jak pewna jest pozycja.
    """
    zebrane: dict[str, tuple[str, frozenset[str]]] = {}
    for rama in _zbiór(warstwa, "frames"):
        for argument in _zbiór(rama, "arguments"):
            rola = _wartość(argument, "role")
            identyfikator = argument.get(IDENTYFIKATOR)
            if rola is None or not identyfikator:
                continue
            uszczegółowienie = _wartość(argument, "role_attribute")
            if uszczegółowienie is not None:
                rola = f"{rola}.{uszczegółowienie}"
            zebrane[identyfikator] = (rola, _żądane(argument))
    return zebrane


def _spięcia(warstwa: ET.Element) -> Iterator[tuple[str, str]]:
    """Pary identyfikatorów, którymi warstwa spięć wiąże argument z frazą.

    Wymian schematu ta warstwa trzyma kilka i o to, w której stoi spięcie, nikt
    tu nie pyta: wymiana mówi, którą frazą argument bywa obsadzony, a wiersz mówi
    o pozycji i mówi to samo z każdej z nich.
    """
    for wymiana in _zbiór(warstwa, "alternations"):
        for spięcie in _zbiór(wymiana, "connections"):
            argument = _odnośnik(spięcie, "argument")
            for fraza in _zbiór(spięcie, "phrases"):
                yield argument, _wskazany(fraza)


def _wpisy_lematu(wpis: ET.Element) -> Iterator[tuple[str, str, str, frozenset[str]]]:
    """Żądania jednego lematu: klasa słowa, pozycja, rola i klasy, każde raz.

    Lemat bez którejkolwiek z trzech warstw nie ma czego złączyć, a warunek jest
    jeden, bo trzy warstwy chodzą razem: w tym wydaniu każdy czasownik ma je
    wszystkie trzy albo samą składniową, i ilu ich jest, mówi
    docs/prior-art.md#polish-language-resources.
    """
    składniowa = wpis.find(f'{TEI}fs[@type="syntactic_layer"]')
    semantyczna = wpis.find(f'{TEI}fs[@type="semantic_layer"]')
    spięcia = wpis.find(f'{TEI}fs[@type="connections_layer"]')
    if składniowa is None or semantyczna is None or spięcia is None:
        return
    frazy = _pozycje_schematów(składniowa)
    argumenty = _argumenty(semantyczna)
    for argument, fraza in _spięcia(spięcia):
        if argument not in argumenty or fraza not in frazy:
            continue
        zwrotny, nazwa = frazy[fraza]
        rola, żądane = argumenty[argument]
        yield CZASOWNIK_ZWROTNY if zwrotny else CZASOWNIK, nazwa, rola, żądane


def żądania(path: Path | str) -> list[tuple[str, str, str, str, frozenset[str]]]:
    """Żądania całego słownika: lemat, klasa słowa, pozycja, rola i klasy.

    Wiersz jest jeden na rolę w pozycji, więc klasy z kilku ram tego samego
    lematu zbierają się w jeden zbiór; czemu tak, mówi docstring modułu.

    Plik idzie przez :func:`xml.etree.ElementTree.iterparse`, a wpis przeczytany
    zwalnia się od razu, bo wydanie TEI waży kilkaset megabajtów i wczytane całe
    stoi w pamięci kilka razy tyle.

    Rzeczownik ani przymiotnik stąd nie wychodzi i nie ma czym: warstwę
    semantyczną ma w tym wydaniu sam czasownik.
    """
    zebrane: dict[tuple[str, str, str, str], set[str]] = {}
    for _zdarzenie, wpis in ET.iterparse(path, events=("end",)):
        if wpis.tag != f"{TEI}entry":
            continue
        lemat = wpis.findtext(f"{TEI}form/{TEI}orth")
        if lemat is not None and wpis.findtext(f"{TEI}form/{TEI}pos") == "verb":
            for klasa, nazwa, rola, żądane in _wpisy_lematu(wpis):
                zebrane.setdefault((lemat, klasa, nazwa, rola), set()).update(żądane)
        wpis.clear()
    return sorted(
        (lemat, klasa, nazwa, rola, frozenset(klasy))
        for (lemat, klasa, nazwa, rola), klasy in zebrane.items()
    )


NAGŁÓWEK = f"""\
# Żądania olskiego: czego czasownik żąda od słowa, które stoi w jego pozycji.
# Kolumny to lemat, klasa słowa, pozycja, rola, którą rama tej pozycji daje, oraz
# klasy rzeczy, których ona żąda, rozdzielone przecinkiem.
#
# Klasą słowa jest `{CZASOWNIK}` albo `{CZASOWNIK_ZWROTNY}`
# i rozdziela ona wpisy o jednym lemacie tak samo jak w `olski/leksykon.txt`.
#
# Pozycja `{PODMIOT}` jest podmiotem, a `{PRZYIMKOWA}(o)` pozycją pod tym przyimkiem;
# obie noszą nazwę Walentego, bo olski nie ma ich pozycją ramy.
# Pozostałe noszą nazwy olskiego: `{BIERNIK}`, `{CELOWNIK}` i `{DOPEŁNIACZ}` są dopełnieniem
# w tym przypadku, `{BEZOKOLICZNIK}` frazą bezokolicznikową, `{ZDANIE_PODRZĘDNE}` zdaniem
# podrzędnym wprowadzonym przez `że`, a `{PYTANIE_ZALEŻNE}` pytaniem zależnym.
#
# Rola niesie za kropką swoje uszczegółowienie tam, gdzie rama je nazywa:
# `Initiator.Source` jest tym, kto wynajmuje, a `Initiator.Goal` tym, komu się
# wynajmuje.
#
# Kolumna klas jest zbiorem po wszystkich ramach lematu, więc jest alternatywą, a
# nie koniunkcją: `ALL` obok klasy nazwanej znaczy, że w jednym znaczeniu pozycja
# nie żąda niczego. Pusta znaczy, że rama nazywa rolę i klasy nie żąda.
# `{SYNSETY}` i `{RELACJA}` stoją w miejscu klasy, której ten plik nie umie nazwać:
# pierwszy tam, gdzie Walenty żąda zbioru synsetów plWordNetu, drugi tam, gdzie żąda
# rzeczy stojącej w relacji do argumentu obok. Czy słowo do klasy należy, orzeka
# wordnet, którego to repozytorium nie ma.
#
# Plik jest generowany i nie pisze się go ręcznie. Powstaje z Walentego,
# słownika walencyjnego polszczyzny IPI PAN, wydanie TEI z 18 kwietnia 2016,
# i jest utworem zależnym od niego, więc idzie na tych samych warunkach:
# CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/
# Źródło: http://zil.ipipan.waw.pl/Walenty
#
# Wyprowadza go `harness/żądania.py`, który mówi, co stąd bierze, a czego nie;
# docs/walencja.md trzyma polecenie wraz z tym, skąd wziąć plik
# wejściowy, i mówi, po co ten plik jest.
"""


def zapisz(wpisy: Sequence[tuple[str, str, str, str, frozenset[str]]], out) -> None:
    """Wypisz wpisy w tej kolejności, w której przyszły.

    Zbiór klas wychodzi posortowany, bo kolejność zbioru jest inna w każdym
    przebiegu, a plik generowany ma się nie różnić od przebiegu do przebiegu.
    """
    out.write(NAGŁÓWEK)
    for lemat, klasa, nazwa, rola, klasy in wpisy:
        out.write(f"{lemat}\t{klasa}\t{nazwa}\t{rola}\t{','.join(sorted(klasy))}\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.żądania",
        description="Wypisz, czego czasownik żąda od słowa stojącego w jego pozycji.",
    )
    parser.add_argument("wydanie", help="walenty_*.xml z wydania TEI")
    args = parser.parse_args(argv)
    zapisz(żądania(args.wydanie), sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
