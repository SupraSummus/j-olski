"""Ile zdań banku drzew niesie konstrukcja, której gramatyka nie ma.

Wpis o takiej konstrukcji kończy się zwykle tym, że bez tej
liczby jest samą ceną. Kolejka blokerów jej nie podaje, bo nazywa formę, na
której analiza stanęła, a nie konstrukcję, której zabrakło
(``olski/pokrycie.py``). Nad drzewem wzorcowym liczy się ją wprost.

Kilka konstrukcji idzie jednym przebiegiem, bo wszystkie czytają to samo drzewo,
a przejście banku drzew kosztuje minuty.

**Pytamy o regułę, a nie o kształt.** Bank drzew powstał z gramatyki, więc każde
rozwinięcie niesie nazwę reguły, która je zbudowała, a jeden kształt bywa kilkoma
konstrukcjami: ``fno`` o dwóch dzieciach ``fno`` jest przydawką dopełniaczową,
apozycją albo zaimkiem dzierżawczym przed rzeczownikiem. Liczba wzięta kształtem
zsumowałaby te trzy i nie mówiłaby o żadnej z nich, a licznik przydawki niżej
stoi po to, żeby było widać, ile taka pomyłka kosztuje.

**Wychodzi stąd górna granica zakupu, a nie zakup.** Zdanie z konstrukcją bywa
odrzucone z drugiego powodu, więc jej wpuszczenie go nie kupuje, a konstrukcja
bywa zasłonięta czytaniem, którego polszczyzna nie ma, więc jej wpuszczenie
odbiera zdanie już przyjęte. Ile z obietnicy zostawało dotąd, mówi
``docs/roadmap.md``.
"""

from __future__ import annotations

import argparse
import collections
import functools
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.attachment import LUŹNA, NP
from harness.corpus import Constituent, constituents, parse_forest, read_forest
from harness.komenda import Komenda, uruchom
from harness.pomiar import po_kawałkach

#: Ile zdań pokazać pod każdą liczbą, bo kształt nazwany regułą cudzej gramatyki
#: sprawdza się czytaniem zdań, a nie odczytaniem samej liczby.
PRZYKŁADY = 6

#: Kategorie tej gramatyki, których nie nazywa jeszcze żadna sonda; grupę imienną
#: i pozycję luźną nazywa ``harness/attachment.py`` i stamtąd tu idą.
FRAZA_PRZYMIOTNIKOWA = "fpt"
ZDANIE_PODRZĘDNE = "fzd"
PRZECINEK, SPÓJNIK = "przec", "spójnik"

#: Klasa głowy, która czyni grupę imienną rzeczownikową: ``fno`` idzie w tej
#: gramatyce także nad zaimkiem, a rozdziela je dopiero ta klasa.
GŁOWA_RZECZOWNA = "rzecz"

#: Lemat zaimka zwrotnego, tak jak nazywa go bank drzew. Kopia nazwy z
#: ``olski/subset/słowa.py`` byłaby tu fałszywa: tamta stoi po stronie Morfeusza, a ta
#: po stronie Świgry.
LEMAT_ZWROTNY = "siebie"

#: Reguła apozycji z przecinkiem i reguła apozycji bez niego. Obie liczą się
#: osobno, bo kolejka pyta o pierwszą — ``Przyszli moi sąsiedzi, lekarz i
#: nauczyciel.`` — a druga stoi już policzona wśród zawyżeń pomiaru
#: wieloznaczności jako ``podpis CERTYFIKAT`` (``docs/open-questions.md``).
APOZYCJA_Z_PRZECINKIEM, APOZYCJA_BEZ_PRZECINKA = "noapp", "noap"

#: Reguła przydawki dopełniaczowej, czyli tej konstrukcji, z którą kształt zlewa
#: apozycję: obie są węzłem ``fno`` o dwojgu dzieci ``fno``.
PRZYDAWKA_DOPEŁNIACZOWA = "noa1"

#: Dzieci węzła w porządku rozpiętości. Kształt pyta o nie przez to wejście, a nie
#: przez pole w :class:`~harness.corpus.Constituent`, bo drzewo wzorcowe niesie
#: dowiązanie do rodzica i lista dzieci byłaby tam drugą kopią tego samego.
Dzieci = Callable[[Constituent], Sequence[Constituent]]


@dataclass(frozen=True)
class Kształt:
    """Jedna konstrukcja, o którą pyta kolejka, wraz z pytaniem o węzeł.

    Nazwa jest kluczem licznika i nagłówkiem wydruku naraz, bo dwa napisy na
    jedną konstrukcję rozjeżdżają się, a nikt ich nie czyta obok siebie.
    """

    nazwa: str
    #: Czy ten węzeł jest tą konstrukcją. Drugim argumentem idzie odpowiedź na
    #: pytanie „jakie dzieci ma ten węzeł”, a nie sama lista dzieci pytanego
    #: węzła, żeby kształt pytający o wnuka pytał tak samo jak ten pytający o
    #: dziecko i nie żądał w przebiegu własnej ścieżki.
    pyta: Callable[[Constituent, Dzieci], bool]


def _apozycja_z_przecinkiem(węzeł: Constituent, dzieci: Dzieci) -> bool:
    """``Przyszli moi sąsiedzi, lekarz i nauczyciel.``, czyli człon za przecinkiem.

    Reguła rozdziela tę konstrukcję od koordynacji, której olski już ma na
    czterech poziomach, a kształt jej nie rozdziela: ciąg współrzędny rozdzielony
    przecinkiem ma te same trzy dzieci. Stąd pytanie o regułę.
    """
    return węzeł.rule == APOZYCJA_Z_PRZECINKIEM


def _apozycja_bez_przecinka(węzeł: Constituent, dzieci: Dzieci) -> bool:
    """``siostra Placyda``, ``pan ojciec``: dwa człony bez znaku między nimi."""
    return węzeł.rule == APOZYCJA_BEZ_PRZECINKA


def _przydawka_dopełniaczowa(węzeł: Constituent, dzieci: Dzieci) -> bool:
    """``grób męża``, ``Rolę teoretyków``: rzeczownik i dopełniacz pod nim.

    Nie jest brakiem gramatyki — olski ma tę pozycję — i stoi tu po to, żeby
    liczba obok niej mówiła, ile kosztowałoby liczenie apozycji kształtem: obie
    konstrukcje mają dwoje dzieci ``fno`` i rozdziela je dopiero reguła.
    """
    return węzeł.rule == PRZYDAWKA_DOPEŁNIACZOWA


def _wolne_celowniki(węzeł: Constituent, dzieci: Dzieci) -> list[Constituent]:
    """Grupy imienne w celowniku, których schemat czasownika nie żąda.

    Pozycja luźna jest tu całym kryterium: celownik wymagany stoi pod ``fw`` i
    wchodzi do olskiego leksykonem, a ten dochodzi do orzeczenia bez żądania i
    dlatego nie ma go jak wpisać do schematu (``docs/subset.md``).
    """
    if węzeł.category != LUŹNA:
        return []
    return [
        dziecko
        for dziecko in dzieci(węzeł)
        if dziecko.category == NP and dziecko.przypadek == "dat"
    ]


def _wolny_celownik_rzeczownikowy(węzeł: Constituent, dzieci: Dzieci) -> bool:
    """``Kompilator wyprowadza psa agentowi.``: wolny celownik wyrażony rzeczownikiem.

    Rozdzielony od zaimkowego, bo wpis kolejki żąda pozycji okolicznika obok
    wyrażenia przyimkowego i przysłówka, a zaimek zwrotny olski ma już terminalem
    (``docs/subset.md``), więc ``sobie`` tej pozycji od niego nie żąda.
    """
    return any(_rzeczownikowy(celownik) for celownik in _wolne_celowniki(węzeł, dzieci))


def _wolny_celownik_zaimkowy(węzeł: Constituent, dzieci: Dzieci) -> bool:
    """``Rozbiłaś mi samochód!``, ``lubię sobie popatrzeć``: wolny celownik zaimka."""
    return any(not _rzeczownikowy(celownik) for celownik in _wolne_celowniki(węzeł, dzieci))


def _rzeczownikowy(grupa: Constituent) -> bool:
    """Czy głową tej grupy imiennej jest rzeczownik, a nie zaimek.

    Zaimek zwrotny wypada tu wprost, bo bank drzew liczy go do klasy ``rzecz``,
    a olski ma go terminalem (``docs/subset.md``): zostawiony w tej klasie
    zawyżałby wiersz o pozycję, której ta konstrukcja od gramatyki nie żąda.
    """
    return grupa.klasa == GŁOWA_RZECZOWNA and grupa.lemat != LEMAT_ZWROTNY


def _człon_lewy_ze_zdaniem_względnym(węzeł: Constituent, dzieci: Dzieci) -> bool:
    """``pliki, które rosną, i katalogi``: zdanie względne pod lewym członem ciągu.

    Olski wyprowadza ten ciąg z prawej strony i nie z lewej, bo produkcja zdania
    względnego żąda członu, a koordynacja daje po lewej człon i po prawej ciąg.
    Liczy się tu sam człon lewy, bo prawy już się wyprowadza.
    """
    rodzeństwo = dzieci(węzeł)
    if not rodzeństwo or not any(dziecko.category == SPÓJNIK for dziecko in rodzeństwo):
        return False
    lewy = rodzeństwo[0]
    return lewy.category == NP and any(
        wnuk.category == ZDANIE_PODRZĘDNE for wnuk in dzieci(lewy)
    )


def _ciąg_przymiotników_samym_przecinkiem(węzeł: Constituent, dzieci: Dzieci) -> bool:
    """``Warstwy trzecia, czwarta i piąta``: trzeci człon przydawki pisany przecinkiem.

    Sam przecinek jest tu całym pytaniem, bo o czwarte ciało tej rodziny prosi
    wpis kolejki, a trzy ciała, które przydawka ma, biorą spójnik.
    """
    rodzeństwo = dzieci(węzeł)
    return (
        węzeł.category == FRAZA_PRZYMIOTNIKOWA
        and any(dziecko.category == PRZECINEK for dziecko in rodzeństwo)
        and not any(dziecko.category == SPÓJNIK for dziecko in rodzeństwo)
    )


def _ciąg_przymiotników_przecinkiem_i_spójnikiem(węzeł: Constituent, dzieci: Dzieci) -> bool:
    """``nie tylko martyrologiczny i bezinteresowny, ale i zewnętrznoroszczeniowy``.

    Stoi tu obok tamtego, bo bez niego wiersz zerowy czyta się jak usterka sondy:
    przecinek między przydawkami bank drzew ma, tyle że zawsze ze spójnikiem po nim.
    """
    rodzeństwo = dzieci(węzeł)
    return (
        węzeł.category == FRAZA_PRZYMIOTNIKOWA
        and any(dziecko.category == PRZECINEK for dziecko in rodzeństwo)
        and any(dziecko.category == SPÓJNIK for dziecko in rodzeństwo)
    )


#: Kolejność stała, a nie po liczbie, żeby dwa przebiegi dały się porównać wiersz
#: po wierszu; liczba jest tym, co się między nimi zmienia.
KSZTAŁTY = (
    Kształt("apozycja z przecinkiem", _apozycja_z_przecinkiem),
    Kształt("apozycja bez przecinka", _apozycja_bez_przecinka),
    Kształt("przydawka dopełniaczowa (nie jest brakiem)", _przydawka_dopełniaczowa),
    Kształt("wolny celownik rzeczownikowy", _wolny_celownik_rzeczownikowy),
    Kształt("wolny celownik zaimkowy", _wolny_celownik_zaimkowy),
    Kształt("człon lewy ciągu ze zdaniem względnym", _człon_lewy_ze_zdaniem_względnym),
    Kształt("ciąg przymiotników samym przecinkiem", _ciąg_przymiotników_samym_przecinkiem),
    Kształt(
        "ciąg przymiotników przecinkiem i spójnikiem",
        _ciąg_przymiotników_przecinkiem_i_spójnikiem,
    ),
)


@dataclass
class Raport:
    """Ile zdań niesie każdy kształt, i garść tych zdań do przeczytania."""

    ile_przykładów: int = PRZYKŁADY
    #: Lasy z drzewem wzorcowym, czyli mianownik każdej liczby niżej.
    drzewa: int = 0
    #: Zdania niosące kształt, po jednym na zdanie, a nie na wystąpienie: wpis
    #: kolejki pyta, ile zdań konstrukcja kupuje, a zdanie kupuje się raz,
    #: choćby konstrukcja stała w nim dwa razy.
    zdania: collections.Counter = field(default_factory=collections.Counter)
    #: Wystąpienia, bo zdanie z dwoma apozycjami mówi o częstości co innego niż
    #: dwa zdania z jedną, a wpis, który dopisuje ciało, płaci za wystąpienie.
    wystąpienia: collections.Counter = field(default_factory=collections.Counter)
    przykłady: dict[str, list[tuple[int, str]]] = field(default_factory=dict)

    def zanotuj(self, nazwa: str, ile: int, zdanie: str) -> None:
        self.zdania[nazwa] += 1
        self.wystąpienia[nazwa] += ile
        self.zanotuj_przykład(nazwa, zdanie)

    def zanotuj_przykład(self, nazwa: str, zdanie: str) -> None:
        """Zachowaj to zdanie, jeśli jest wśród najkrótszych pod tą nazwą.

        Osobno od liczenia, bo :func:`scal` składa liczniki wprost i zdania
        kawałka przechodzą tędy drugi raz, już bez podnoszenia liczb.

        Najkrótsze, bo kształt sprawdza się czytaniem, a zdanie banku drzew bywa
        na cztery wiersze. Porządek jest przy tym pełny — długość, potem napis —
        bo po samej długości dwa zdania równej długości wychodziłyby w porządku,
        w którym akurat przyszły, a ten zależy od podziału na kawałki.
        """
        zachowane = self.przykłady.setdefault(nazwa, [])
        zachowane.append((len(zdanie.split()), zdanie))
        zachowane.sort()
        del zachowane[self.ile_przykładów :]


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden, tak samo jak robią to pozostałe sondy."""
    scalony = Raport(przykłady)
    for raport in raporty:
        scalony.drzewa += raport.drzewa
        scalony.zdania.update(raport.zdania)
        scalony.wystąpienia.update(raport.wystąpienia)
        for nazwa, zachowane in raport.przykłady.items():
            for _, zdanie in zachowane:
                scalony.zanotuj_przykład(nazwa, zdanie)
    return scalony


def _dzieci(węzły: Sequence[Constituent]) -> Dzieci:
    """Odpowiedź na „jakie dzieci ma ten węzeł” dla węzłów jednego drzewa.

    Zbierana raz na drzewo, bo pyta o nią każdy kształt nad każdym węzłem, a
    liczona za każdym pytaniem byłaby przejściem po całym drzewie na węzeł.

    Klucz jest tożsamością, a nie węzłem: :class:`Constituent` jest zamrożony,
    więc haszuje się przez wartości, a wśród nich jest rodzic — czyli haszowanie
    węzła schodzi po rodzicach aż do korzenia, przy każdym pytaniu. Rodzic jest
    tu przy tym tym samym obiektem, którego szukamy, więc tożsamość odpowiada
    wprost i nie płaci za to zejście.
    """
    zebrane: dict[int, list[Constituent]] = {}
    for węzeł in węzły:
        if węzeł.parent is not None:
            zebrane.setdefault(id(węzeł.parent), []).append(węzeł)
    for rodzeństwo in zebrane.values():
        # Porządek rozpiętości, bo kształt pyta o człon lewy, a zejście
        # `constituents` idzie stosem i wydaje rodzeństwo odwrotnie.
        rodzeństwo.sort(key=lambda węzeł: (węzeł.start, węzeł.end))
    return lambda węzeł: zebrane.get(id(węzeł), ())


def zmierz(ścieżki: Iterable[Path], przykłady: int = PRZYKŁADY) -> Raport:
    """Policz każdy kształt nad tymi lasami.

    Populacja jest ta sama, co u pozostałych sond nad bankiem drzew: las z
    drzewem wzorcowym, bez granicy na długość zdania. Las bez takiego drzewa
    odpada, bo kształtu nie ma w czym policzyć — annotator nie wybrał odpowiedzi.
    """
    raport = Raport(przykłady)
    for ścieżka in ścieżki:
        forest = read_forest(ścieżka)
        zdanie = parse_forest(forest)
        if not zdanie.annotated:
            continue
        raport.drzewa += 1
        węzły = constituents(forest)
        dzieci = _dzieci(węzły)
        for kształt in KSZTAŁTY:
            ile = sum(1 for węzeł in węzły if kształt.pyta(węzeł, dzieci))
            if ile:
                raport.zanotuj(kształt.nazwa, ile, zdanie.text)
    return raport


def wydruk(raport: Raport, nagłówek: str) -> str:
    """Liczba na kształt, z przykładami pod nią."""
    wiersze = [nagłówek, f"  lasów z drzewem wzorcowym: {raport.drzewa}", ""]
    for kształt in KSZTAŁTY:
        zdań = raport.zdania[kształt.nazwa]
        wystąpień = raport.wystąpienia[kształt.nazwa]
        wiersze.append(f"  {kształt.nazwa}: {zdań} zdań, {wystąpień} wystąpień")
        for długość, zdanie in raport.przykłady.get(kształt.nazwa, []):
            wiersze.append(f"    {długość:>3}  {zdanie}")
        wiersze.append("")
    return "\n".join(wiersze)


def _kawałek(ścieżki: Sequence[Path], przykłady: int) -> Raport:
    return zmierz(ścieżki, przykłady)


def przebieg(ścieżki: Sequence[Path], jobs: int, przykłady: int = PRZYKŁADY) -> Raport:
    """Zmierz te lasy w puli procesów i złóż to, co każdy kawałek policzył."""
    praca = functools.partial(_kawałek, przykłady=przykłady)
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


def _korpus(ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    return wydruk(przebieg(ścieżki, args.jobs, args.przykłady), "Składnica")


KOMENDA = Komenda(
    nazwa="harness.kształty",
    opis="Policz, ile zdań banku drzew niesie kształt, o który pyta kolejka konstrukcji.",
    przykłady=PRZYKŁADY,
    korpus=_korpus,
    pula=True,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
