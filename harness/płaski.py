"""Ile werdyktów przysłówka w okoliczniku mówi o zdaniu nieprawdę.

Lista okoliczników jest płaska, więc pozycja przysłówka przy czasowniku bierze
także przysłówek postawiony przed przymiotnikiem: ``Plik jest bardzo duży.``
wychodzi z niej jednym czytaniem, w którym ``bardzo`` określa zdanie, a nie
``duży``. Zdanie przyjęte z takim drzewem jest droższe od wieloznacznego, bo
``valid`` czyta się jak twierdzenie, a tej ceny nie widzi ani pokrycie, ani
zgodność ról nad bankiem drzew, która porównuje podmiot i dopełnienie.

Mierzy się to nad samym olskim, bo pomiar różnicowy liczy werdykty, a pytanie jest
tu o drzewo, którym werdykt wypadł; wariantem ``okolicznik`` niżej mierzy się to
samo nad gramatyką z pierwszym gospodarzem i bez pozostałych, czyli cenę, przy
której weszli. Populację tworzą zdania przyjęte
jednym czytaniem: odpowiedź jest wtedy dokładna, a listę czytań zdania
wieloznacznego ucina ``MAX_READINGS``.

Klasy są dwie, bo gospodarz, do którego przysłówek doszedłby, jest inny:
przed przymiotnikiem drugi, a przed drugim przysłówkiem trzeci. Nad olskim obie
wychodzą zerem, i to jest zakup tych dwóch gospodarzy; pod wariantem
``okolicznik`` widać, ile takich czytań było przed nimi. Stopnia kryterium żąda,
bo przysłówek pierwotny przymiotnika nie określa i przed nim wychodzi zgodnie z
prawdą.

Liczba jest górnym oszacowaniem, tak samo jak ``całe_przyłączenie`` w
``harness/czytania.py``: przysłówek stopniowany bywa okolicznikiem zdania i wtedy
przymiotnik po nim niczego nie zmienia, jak w ``Ostatecznie nowa ustawa wchodzi w
życie.`` Dlatego pod liczbą wychodzą formy i zdania — osądu o zdaniu sonda nie
wydaje.

Wynik czyta ``docs/subset.md``.

    python3 -m harness.płaski Składnica-frazowa-180723/
    python3 -m harness.płaski proza/README.txt
"""

from __future__ import annotations

import argparse
import collections
import functools
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness import ruch
from harness.komenda import Komenda, uruchom
from harness.ruch import gramatyka
from olski.corpus import read
from olski.coverage import po_kawałkach, segments_for
from olski.grammar import Grammar, Production, nt
from olski.parse import Leaf, Node, Tree, parse
from olski.subset import (
    DEKLARACJA,
    FRAGMENT,
    PRZYSŁÓWEK,
    PRZYSŁÓWEK_STOPNIA,
    PRZYSŁÓWKOWY,
    check,
)

#: Ile zdań zachować pod każdą klasą, tak jak trzymają je pomiary obok.
PRZYKŁADY = 8

OKOLICZNIK = "okolicznik"
PRZY_PRZYMIOTNIKU = "przy przymiotniku"


def gospodarz(produkcja: Production) -> str | None:
    """Przy którym gospodarzu stawia przysłówek ta produkcja; ``None``, gdy żadnym.

    Odpowiada terminal albo symbol przysłówka, a nie lista nazw wypisana obok
    gramatyki: ciało dopisane kiedyś w którymkolwiek z tych miejsc trafi tu samo,
    gdzie lista postarzałaby się bez śladu — pomiar brałby wariant węższy, niż o
    sobie mówi, i nie powiedziałby o tym ani słowem.

    Stopień mają dwaj gospodarze, a nazwa jest tu jedna, bo trzeci bez listy
    okoliczników nie wyprowadza niczego: wariant, który tę listę zdejmuje, zdejmuje
    i jego, więc osobnej ceny ten gospodarz nie ma.

    Okolicznik zdejmuje się przy tym czterema produkcjami, a wystarczyłaby jedna:
    ``Adverb → adv`` jest jedyną, która przysłówek do zdania wpuszcza, więc bez
    niej dwa ciała listy okoliczników i czoło zdania nie mają czym się wypełnić.
    Zdejmowane są mimo to wszystkie, bo wariant ma być gramatyką bez tej
    konstrukcji, a nie gramatyką z symbolem, do którego nic nie prowadzi.
    """
    if PRZYSŁÓWEK_STOPNIA in produkcja.body:
        return PRZY_PRZYMIOTNIKU
    if PRZYSŁÓWEK in produkcja.body or nt(PRZYSŁÓWKOWY) in produkcja.body:
        return OKOLICZNIK
    return None


#: Deklaracja różnicowa przysłówka, czyli warianty, którymi ten pomiar buduje
#: gramatykę bez któregoś gospodarza. Stoi tutaj, bo tutaj ma jedynego
#: czytelnika: przebieg wyceniający samo wpuszczenie przysłówka jest w gicie.
PRZYSŁÓWEK_SONDA = ruch.Sonda(
    nazwa="harness.płaski",
    opis="Przy którym gospodarzu stoi przysłówek w mierzonej gramatyce.",
    warianty=("bez przysłówka", OKOLICZNIK, PRZY_PRZYMIOTNIKU, "olski"),
    grupa=gospodarz,
    pytania=(
        "obaj gospodarze ruszają to samo zdanie",
        "razem wychodzi co innego niż osobno",
    ),
)

#: Cecha, którą Morfeusz oddziela przysłówek odprzymiotnikowy od pierwotnego.
STOPIEŃ = "degree"

#: Części mowy, które kryterium liczy za przymiotnik, czyli te same, które olski
#: bierze za orzecznikowe: imiesłów bierny jest tam przymiotnikiem i tu jest nim
#: tak samo (`nieporównanie tańsze`, `znacznie rozszerzony`).
PRZYMIOTNIKOWE = frozenset({"adj", "ppas"})

#: Klasy, w kolejności wydruku. Nazwa mówi, przed czym przysłówek stanął, bo tym
#: się te dwie różnią: pierwszą pozycję ma gospodarz drugi, a drugą trzeci.
PRZED_PRZYMIOTNIKIEM = "przed przymiotnikiem"
PRZED_PRZYSŁÓWKIEM = "przed przysłówkiem"
KLASY = (PRZED_PRZYMIOTNIKIEM, PRZED_PRZYSŁÓWKIEM)


def _liście(drzewo: Tree, rodzic: str | None = None) -> list[tuple[str | None, Leaf]]:
    """Liście czytania w kolejności zdania, każdy z etykietą swojego rodzica.

    Kolejność wychodzi z ciał produkcji, bo dziecko siedzi w ciele tam, gdzie jego
    forma padła w zdaniu, więc zejście w głąb od lewej daje napis. Rodzic idzie
    obok liścia, a nie drugim przejściem, bo kryterium pyta o oba naraz: czy
    przysłówek wisi wprost pod listą okoliczników i co padło zaraz po nim.
    """
    if isinstance(drzewo, Leaf):
        return [(rodzic, drzewo)]
    return [para for dziecko in drzewo.children for para in _liście(dziecko, drzewo.label)]


def płaskie(drzewo: Node) -> list[tuple[str, str]]:
    """Klasy i formy, którymi to czytanie wypadło płasko; pusta lista, gdy nie.

    Para, a nie sama klasa, bo forma jest tym, co pod liczbą trzeba przeczytać:
    ``bardzo`` przed przymiotnikiem jest pomyłką, a ``ostatecznie`` przed nim może
    nie być, i rozstrzyga o tym słowo, a nie klasa.

    Rodzicem musi być symbol przysłówka zdania (:data:`PRZYSŁÓWKOWY`), bo pod nim
    stoi przysłówek okolicznikowy i tylko on: przysłówek określający przymiotnik
    wisi w czytaniu drugiego gospodarza pod symbolem tego przymiotnika i wtedy
    drzewo mówi o nim prawdę. Płaskim czyni takie czytanie lista okoliczników nad
    nim, która bierze przysłówek i drugą taką listę za nim, a o to, co ten
    przysłówek określa, nie pyta.
    """
    liście = _liście(drzewo)
    znalezione = []
    for (rodzic, liść), (_, następny) in zip(liście, liście[1:], strict=False):
        if rodzic != PRZYSŁÓWKOWY or liść.reading.tag.pos != "adv":
            continue
        if not liść.reading.tag.get(STOPIEŃ):
            continue
        pos = następny.reading.tag.pos
        if pos in PRZYMIOTNIKOWE:
            znalezione.append((PRZED_PRZYMIOTNIKIEM, liść.segment.form))
        elif pos == "adv":
            znalezione.append((PRZED_PRZYSŁÓWKIEM, liść.segment.form))
    return znalezione


@dataclass
class Raport:
    """Co jeden przebieg naliczył."""

    ile_przykładów: int = PRZYKŁADY
    #: Zdania, o które sonda w ogóle zapytała, czyli mianownik werdyktów.
    zmierzone: int = 0
    #: Zdania, które wariant przyjmuje jednym czytaniem, czyli populacja.
    przyjęte: int = 0
    #: Zdania przyjęte, których jedyne czytanie stoi płasko, pod kluczem klasy.
    #: Zdanie o dwóch takich przysłówkach liczy się w każdej klasie raz, bo
    #: pytanie jest o zdanie, a nie o wystąpienie.
    płaskie: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Zdania przyjęte, których czytanie stoi płasko którąkolwiek klasą.
    #: Liczone osobno, bo suma po klasach liczyłaby takie zdanie dwa razy.
    razem: int = 0
    #: Formy przysłówka, którymi to wychodzi, pod kluczem klasy.
    formy: collections.Counter[tuple[str, str]] = field(default_factory=collections.Counter)
    #: Zdania zachowane pod klasą, najkrótsze, żeby dały się przeczytać.
    przykłady: dict[str, list[tuple[int, str]]] = field(default_factory=dict)
    #: Dlaczego zdanie nie weszło do mianownika.
    pominięte: collections.Counter[str] = field(default_factory=collections.Counter)

    def zapisz(self, tekst: str, drzewa: Sequence[Node]) -> None:
        """Zapisz jedno zdanie wraz z czytaniem, którym wariant je przyjął.

        Czytań jest tu zawsze jedno albo żadne, bo populację tworzą zdania
        przyjęte. Lista, a nie jedno drzewo, bo tyle oddaje werdykt i nie ma po co
        rozpakowywać jej u siebie.
        """
        self.zmierzone += 1
        if len(drzewa) != 1:
            return
        self.przyjęte += 1
        znalezione = płaskie(drzewa[0])
        for klasa, forma in znalezione:
            self.formy[(klasa, forma)] += 1
        #  Klasy idą w kolejności deklaracji, a nie zbiorem: zbiór chodzi się w
        #  każdym przebiegu inaczej, a przykłady mieszczą się w budżecie.
        trafione = {klasa for klasa, _ in znalezione}
        for klasa in KLASY:
            if klasa not in trafione:
                continue
            self.płaskie[klasa] += 1
            self.zanotuj(klasa, (len(tekst), tekst))
        if znalezione:
            self.razem += 1

    def zanotuj(self, klucz: str, przykład: tuple[int, str]) -> None:
        """Zachowaj zdanie pod klasą, zostawiając najkrótsze.

        Najkrótsze, bo wybór po długości nie zależy od kolejności, w jakiej
        kawałki wracają z procesów pod spodem.
        """
        zachowane = self.przykłady.setdefault(klucz, [])
        zachowane.append(przykład)
        zachowane.sort()
        del zachowane[self.ile_przykładów :]


def wariant(nazwa: str = PRZYSŁÓWEK_SONDA.czysty) -> Grammar:
    """Gramatyka olskiego z przysłówkiem u tego gospodarza, którego nazwa mówi.

    Bierze się z sondy różnicowej, a nie z produkcji wypisanych tutaj, bo wariant
    zmierzony tabelą w ``docs/subset.md`` i wariant, którego werdykty ta sonda
    czyta, mają być jedną gramatyką. Dopisane drugi raz rozeszłyby się z tamtą
    tabelą przy pierwszej zmianie i żadna liczba by o tym nie powiedziała.

    Domyślny jest sam olski, bo o jego werdykty tu chodzi, a stoi w nim para
    gospodarzy. Wariant ``okolicznik`` odpowiada na pytanie poprzednie, czyli ile
    fałszywych czytań dawałby pierwszy gospodarz bez drugiego, i to jest cena, przy
    której drugiego wpuszczono.
    """
    return gramatyka(PRZYSŁÓWEK_SONDA, nazwa)


def zmierz(
    ścieżki: Sequence[Path],
    przykłady: int = PRZYKŁADY,
    nazwa: str = PRZYSŁÓWEK_SONDA.czysty,
) -> Raport:
    """Jeden przebieg po lasach banku drzew, bez procesów pod spodem."""
    raport = Raport(przykłady)
    grammar = wariant(nazwa)
    for ścieżka in ścieżki:
        zdanie = read(ścieżka)
        if not zdanie.annotated:
            continue
        segmenty = segments_for(zdanie, "gold")
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        result = parse(grammar, list(segmenty), deklaracja=DEKLARACJA)
        raport.zapisz(zdanie.text, result.readings)
    return raport


def nad_prozą(
    tekst: str, przykłady: int = PRZYKŁADY, nazwa: str = PRZYSŁÓWEK_SONDA.czysty
) -> Raport:
    """To samo pytanie nad prozą, którą olski ma czytać.

    Bank drzew mówi, ile płaskich czytań wychodzi w cudzej polszczyźnie, a rejestr
    własny odpowiada osobno i odpowiada inaczej, bo to on jest tym, o który olskiemu
    chodzi. Fragment do mianownika nie wchodzi: nikt go nie napisał jako zdania.
    """
    raport = Raport(przykłady)
    grammar = wariant(nazwa)
    for werdykt in check(tekst, grammar):
        if werdykt.status == FRAGMENT:
            raport.pominięte["fragment, a nie zdanie"] += 1
            continue
        raport.zapisz(werdykt.text, werdykt.result.readings)
    return raport


def _kawałek(ścieżki: Sequence[Path], przykłady: int, nazwa: str) -> Raport:
    return zmierz(ścieżki, przykłady, nazwa)


def przebieg(
    ścieżki: Sequence[Path],
    jobs: int,
    przykłady: int = PRZYKŁADY,
    nazwa: str = PRZYSŁÓWEK_SONDA.czysty,
) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport."""
    praca = functools.partial(_kawałek, przykłady=przykłady, nazwa=nazwa)
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden, przykłady włącznie."""
    scalony = Raport(przykłady)
    for raport in raporty:
        scalony.zmierzone += raport.zmierzone
        scalony.przyjęte += raport.przyjęte
        scalony.razem += raport.razem
        scalony.płaskie.update(raport.płaskie)
        scalony.formy.update(raport.formy)
        scalony.pominięte.update(raport.pominięte)
        for klucz, zachowane in raport.przykłady.items():
            for przykład in zachowane:
                scalony.zanotuj(klucz, przykład)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(raport: Raport, nagłówek: str) -> str:
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań",
        "",
        f"  {raport.przyjęte:>7}  przyjętych jednym czytaniem, czyli populacja",
        *(f"  {ile:>7}  niezmierzone: {powód}" for powód, ile in raport.pominięte.most_common()),
    ]
    if not raport.przyjęte:
        return "\n".join(wiersze)

    udział = raport.razem / raport.przyjęte
    wiersze += ["", f"płaskie czytanie w {raport.razem} z {raport.przyjęte} zdań, {udział:.1%}:"]
    for klasa in KLASY:
        ile = raport.płaskie.get(klasa, 0)
        wiersze.append(f"  {ile:>7}  {ile / raport.przyjęte:>6.1%}  {klasa}")

    for klasa in KLASY:
        formy = [(forma, ile) for (nazwa, forma), ile in raport.formy.items() if nazwa == klasa]
        if not formy:
            continue
        wypisane = ", ".join(
            f"`{forma}` {ile}" for forma, ile in sorted(formy, key=lambda para: (-para[1], para[0]))
        )
        wiersze += ["", f"  formy, {klasa}: {wypisane}"]

    for klasa in KLASY:
        zachowane = raport.przykłady.get(klasa)
        if not zachowane:
            continue
        wiersze += ["", f"  najkrótsze zdania, {klasa}:"]
        wiersze += [f"    {tekst}" for _, tekst in zachowane]
    return "\n".join(wiersze)


def _wariant(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--wariant",
        default=PRZYSŁÓWEK_SONDA.czysty,
        choices=PRZYSŁÓWEK_SONDA.warianty,
        help="u którego gospodarza stoi przysłówek w mierzonej gramatyce",
    )


def _korpus(ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    raport = przebieg(ścieżki, args.jobs, przykłady=args.przykłady, nazwa=args.wariant)
    return wydruk(raport, f"Składnica, morfologia złota, wariant „{args.wariant}”")


def _proza(tekst: str, ścieżka: Path, args: argparse.Namespace) -> str:
    raport = nad_prozą(tekst, args.przykłady, args.wariant)
    return wydruk(raport, f"{ścieżka.name}, proza, wariant „{args.wariant}”")


KOMENDA = Komenda(
    nazwa="harness.płaski",
    opis="Policz zdania, którym płaska lista okoliczników daje fałszywe czytanie.",
    przykłady=PRZYKŁADY,
    korpus=_korpus,
    proza=_proza,
    argumenty=_wariant,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
