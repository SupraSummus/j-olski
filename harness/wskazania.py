"""Ile warstwa rozstrzygająca odpowiada nad werdyktami olskiego i ile z tego trafia.

Świadka statystycznego ocenia już ``olski/rozstrzyganie.py --oceń``
i ocenia go na czwórkach lematów wziętych prosto z banku drzew:
przyimek, rzeczownik anotatora, czasownik anotatora, wybrana strona.
Warstwa wypuszczana pracuje na czymś innym.
Pyta ją ``olski-check``, więc pytaniem jest :class:`Przyłączenie` z werdyktu:
gospodarze są formami, form tych bywa więcej niż dwie,
a lemat wybiera dopiero Morfeusz i wybiera ich kilka naraz.
Różnica między jednym a drugim jest tą, o którą pyta ``Skłonność.wybierz``,
kiedy mówi, że rozmycie po lematach kończy się milczeniem.

Ta sonda mierzy drogę drugą, czyli warstwę taką, jaką dostaje autor.
Populację wyznacza werdykt olskiego, a nie bank drzew:
liczone są przyłączenia, przed którymi olski postawił wybór,
bo tylko o takie warstwa jest kiedykolwiek pytana.
Wzorzec dokłada drzewo, czyli odpowiedź na pytanie, dokąd wyrażenie doszło,
i właścicielem tego odczytu jest ``olski/attachment.py``.

**Złączenie idzie formami modyfikatora, bo tyle mają obie strony.**
Werdykt nazywa modyfikator formami i rozpiętości nie niesie
(:class:`Przyłączenie`), więc kluczem jest napis.
Wyrażenie, którego drzewo wzorcowe nie nawiasuje tak samo,
zostaje bez wzorca i wchodzi do osobnego licznika zamiast do mianownika:
``na podłodze w kuchni z pustą paczką`` jest u anotatora jednym wyrażeniem,
a olski nazywa nad nim cztery.
Bez wzorca zostaje też przyłączenie, którego gospodarzem w drzewie
nie jest ani grupa imienna, ani zdanie.

**Stronę wskazania nazywa ta sama funkcja, którą dzieli gospodarzy świadek**
(``strona`` w ``olski/rozstrzyganie.py``),
bo pomiar liczący ją po swojemu mierzyłby innego świadka niż wypuszczany.

**Świadek kontekstowy milczy tu z definicji.**
Zdania banku drzew stoją osobno, więc sąsiedztwem jest puste,
a akapitu, którego ten świadek żąda, nie ma stąd skąd wziąć.
Jego zasięg mierzy ``harness/powtórzenie.py`` nad korpusem audytowym,
a trafność ``harness/wybory.py`` na wyborach przeczytanych ręką.

Wynik czyta ``docs/disambiguation.md``.

    python3 -m harness.wskazania Składnica-frazowa-180723/
"""

from __future__ import annotations

import argparse
import collections
import functools
import xml.etree.ElementTree as ET
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.komenda import Komenda, uruchom
from olski.attachment import attachments
from olski.corpus import Sentence, parse_forest, read_forest
from olski.coverage import po_kawałkach, segments_for
from olski.parse import Przyłączenie, Result, parse, sklej_formy
from olski.rozstrzyganie import (
    STRONA_CZASOWNIKOWA,
    STRONA_IMIENNA,
    Rozstrzygnięcie,
    Świadek,
    domyślni,
    rozstrzygnij,
    strona,
)
from olski.subset import DEKLARACJA, GRAMMAR

#: Ile zdań zachować pod każdą klasą.
#: Klasa bez przykładu jest liczbą, o której nie wiadomo, co ją wywołało,
#: a pytanie tej sondy jest właśnie o to, na czym warstwa staje.
PRZYKŁADY = 8

#: Nazwy klas, pod którymi trzymane są zdania do przeczytania ręką.
MILCZENIE, POMYŁKA, BEZ_WZORCA = "milczenie", "pomyłka", "bez wzorca"


@dataclass
class Raport:
    """Co jeden przebieg naliczył."""

    ile_przykładów: int = PRZYKŁADY
    #: Zdania z pełnym drzewem wzorcowym, czyli mianownik całego przebiegu.
    zmierzone: int = 0
    #: Zdania, nad którymi werdykt nazwał choć jedno nierozstrzygnięte przyłączenie.
    ze_sporem: int = 0
    #: Przyłączenia nazwane werdyktem, czyli wszystkie pytania, jakie warstwa dostaje.
    przyłączeń: int = 0
    #: Z nich te, na które drzewo wzorcowe odpowiada, czyli mianownik trafności.
    ze_wzorcem: int = 0
    #: Ilu gospodarzy niosło przyłączenie; klucz jest ich liczbą.
    #: Ocena z ``olski/rozstrzyganie.py`` zna wyłącznie dwóch,
    #: więc wiersz o trzech mówi, czego ona nie mierzy.
    gospodarzy: collections.Counter[int] = field(default_factory=collections.Counter)
    #: Gdzie drzewo wzorcowe przyłączyło te ze wzorcem; klucz jest stroną.
    #: Reguła „zawsze do rzeczownika” trafia tyle, ile wynosi tu strona
    #: rzeczownikowa, i jest podłogą, której świadek ma nie ustępować.
    wzorzec: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Odpowiedzi po świadku, liczone nad przyłączeniami ze wzorcem.
    odpowiedzi: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Z nich te, które wskazały stronę drzewa wzorcowego.
    trafień: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Zdania zachowane pod klasą, najkrótsze, z modyfikatorem i tym, co o nim padło.
    przykłady: dict[str, list[tuple[int, str, str]]] = field(default_factory=dict)

    def zanotuj(self, klucz: str, przykład: tuple[int, str, str]) -> None:
        """Zachowaj wypadek pod klasą, zostawiając najkrótsze.

        Najkrótsze, bo przykład ma być do przeczytania, a nie do przewinięcia,
        i bo wybór po długości nie zależy od kolejności, w jakiej kawałki wracają.
        """
        zachowane = self.przykłady.setdefault(klucz, [])
        zachowane.append(przykład)
        zachowane.sort()
        del zachowane[self.ile_przykładów :]


def dokąd_doszły(element: ET.Element, zdanie: Sentence) -> dict[str, str]:
    """Formy wyrażenia przyimkowego → strona, po której doszło w drzewie wzorcowym.

    Napis powtórzony w jednym zdaniu z dwiema stronami wypada,
    bo klucz wskazujący dwa wzorce naraz nie jest wzorcem żadnego z nich.
    """
    znalezione: dict[str, str] = {}
    sporne: set[str] = set()
    for a in attachments(element):
        if a.host not in (STRONA_IMIENNA, STRONA_CZASOWNIKOWA):
            continue
        formy = sklej_formy(s.form for s in zdanie.segments if a.start <= s.start < a.end)
        if znalezione.setdefault(formy, a.host) != a.host:
            sporne.add(formy)
    return {formy: host for formy, host in znalezione.items() if formy not in sporne}


def zmierz(ścieżki: Sequence[Path], przykłady: int = PRZYKŁADY) -> Raport:
    """Jeden przebieg po lasach, bez procesów pod spodem.

    Świadkowie powstają raz na przebieg, a nie raz na zdanie:
    tabela skłonności wchodzi z pliku, a lasów jest tyle, ile plików.
    """
    raport = Raport(przykłady)
    świadkowie = domyślni()
    for ścieżka in ścieżki:
        element = read_forest(ścieżka)
        zdanie = parse_forest(element)
        if not zdanie.annotated:
            continue
        segmenty = segments_for(zdanie, "gold")
        if not segmenty:
            continue
        raport.zmierzone += 1
        result = parse(GRAMMAR, list(segmenty), deklaracja=DEKLARACJA, zatrzymanie=False)
        if result.przyłączenia:
            _sporne(raport, zdanie, result, świadkowie, dokąd_doszły(element, zdanie))
    return raport


def _sporne(
    raport: Raport,
    zdanie: Sentence,
    result: Result,
    świadkowie: Sequence[Świadek],
    złoty: dict[str, str],
) -> None:
    """Naliczenia nad zdaniem, nad którym werdykt zostawił wybór przyłączenia."""
    raport.ze_sporem += 1
    odpowiedzi = rozstrzygnij(result.przyłączenia, świadkowie)
    for przyłączenie, odpowiedź in zip(result.przyłączenia, odpowiedzi, strict=True):
        raport.przyłączeń += 1
        raport.gospodarzy[len(przyłączenie.gospodarze)] += 1
        gdzie = złoty.get(przyłączenie.modyfikator)
        if gdzie is None:
            raport.zanotuj(BEZ_WZORCA, _przykład(zdanie, przyłączenie, "drzewo nazywa co innego"))
            continue
        raport.ze_wzorcem += 1
        raport.wzorzec[gdzie] += 1
        if not isinstance(odpowiedź, Rozstrzygnięcie):
            raport.zanotuj(MILCZENIE, _przykład(zdanie, przyłączenie, f"wzorzec: {gdzie}"))
            continue
        raport.odpowiedzi[odpowiedź.świadek] += 1
        if strona(odpowiedź.gospodarz) == gdzie:
            raport.trafień[odpowiedź.świadek] += 1
            continue
        raport.zanotuj(
            POMYŁKA,
            _przykład(zdanie, przyłączenie, f"→ „{odpowiedź.gospodarz}”, wzorzec: {gdzie}"),
        )


def _przykład(zdanie: Sentence, przyłączenie: Przyłączenie, co: str) -> tuple[int, str, str]:
    return (len(zdanie.tokens), f"„{przyłączenie.modyfikator}” {co}", zdanie.text)


def przebieg(ścieżki: Sequence[Path], jobs: int, przykłady: int = PRZYKŁADY) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport."""
    praca = functools.partial(zmierz, przykłady=przykłady)
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden, przykłady włącznie."""
    scalony = Raport(przykłady)
    for raport in raporty:
        scalony.zmierzone += raport.zmierzone
        scalony.ze_sporem += raport.ze_sporem
        scalony.przyłączeń += raport.przyłączeń
        scalony.ze_wzorcem += raport.ze_wzorcem
        scalony.gospodarzy.update(raport.gospodarzy)
        scalony.wzorzec.update(raport.wzorzec)
        scalony.odpowiedzi.update(raport.odpowiedzi)
        scalony.trafień.update(raport.trafień)
        for klucz, zachowane in raport.przykłady.items():
            for przykład in zachowane:
                scalony.zanotuj(klucz, przykład)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(raport: Raport, nagłówek: str) -> str:
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań z drzewem wzorcowym",
        "",
        f"  {raport.ze_sporem} zdań, nad którymi werdykt zostawia przyłączenie,",
        f"  a w nich {raport.przyłączeń} przyłączeń, czyli tyle pytań warstwa dostaje",
    ]
    if not raport.przyłączeń:
        return "\n".join(wiersze)

    wiersze += ["", "  gospodarzy na przyłączenie:"]
    for ilu, ile in sorted(raport.gospodarzy.items()):
        wiersze.append(f"  {ile:>7}  {ile / raport.przyłączeń:>6.1%}  {ilu}")

    bez = raport.przyłączeń - raport.ze_wzorcem
    wiersze += [
        "",
        f"  ze wzorcem w drzewie: {raport.ze_wzorcem}, "
        f"czyli {raport.ze_wzorcem / raport.przyłączeń:.1%} przyłączeń",
        f"  bez wzorca: {bez}, bo drzewo nawiasuje tę frazę inaczej "
        "albo przyłącza ją do czegoś, co nie jest ani grupą imienną, ani zdaniem",
    ]
    if not raport.ze_wzorcem:
        return "\n".join(wiersze)

    wiersze += _świadkowie(raport)
    for nazwa in (POMYŁKA, MILCZENIE, BEZ_WZORCA):
        wiersze += _przykłady(raport, nazwa)
    return "\n".join(wiersze)


def _świadkowie(raport: Raport) -> list[str]:
    """Zasięg i trafność świadka po świadku, pod podłogą, której ma nie ustępować.

    Podłoga stoi w tej samej tabeli, a nie pod nią, bo bez niej trafność świadka
    czyta się jak wynik: nad tym korpusem rzeczownik bierze dwie trzecie wyborów,
    więc świadek trafiający tyle samo nie kupuje niczego
    (``docs/subset.md``).
    """
    wiersze = ["", f"  co warstwa mówi o {raport.ze_wzorcem} przyłączeniach ze wzorcem:"]
    razem_odpowiedzi = sum(raport.odpowiedzi.values())
    razem_trafień = sum(raport.trafień.values())
    for nazwa in [*sorted(raport.odpowiedzi), None]:
        odpowiedzi = razem_odpowiedzi if nazwa is None else raport.odpowiedzi[nazwa]
        trafień = razem_trafień if nazwa is None else raport.trafień[nazwa]
        trafność = f"{trafień / odpowiedzi:>6.1%}" if odpowiedzi else "     —"
        wiersze.append(
            f"  {odpowiedzi:>7}  {odpowiedzi / raport.ze_wzorcem:>6.1%} odpowiedzi, "
            f"{trafność} trafień    {nazwa or 'razem'}"
        )
    podłoga = raport.wzorzec[STRONA_IMIENNA] / raport.ze_wzorcem
    wiersze.append(
        f"  {raport.ze_wzorcem:>7}  100,0% odpowiedzi, "
        f"{podłoga:>6.1%} trafień    podłoga: zawsze do rzeczownika"
    )
    return wiersze


def _przykłady(raport: Raport, nazwa: str) -> list[str]:
    zachowane = raport.przykłady.get(nazwa)
    if not zachowane:
        return []
    return [
        "",
        f"  najkrótsze zdania klasy „{nazwa}”:",
        *(f"    {co}\n      {tekst}" for _, co, tekst in zachowane),
    ]


def _korpus(ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    raport = przebieg(ścieżki, args.jobs, przykłady=args.przykłady)
    return wydruk(raport, "Składnica, morfologia złota")


KOMENDA = Komenda(
    nazwa="harness.wskazania",
    opis="Policz, ile warstwa rozstrzygająca odpowiada nad werdyktami olskiego.",
    przykłady=PRZYKŁADY,
    korpus=_korpus,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
