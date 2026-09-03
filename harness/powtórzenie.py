"""Ile świadek kontekstowy odpowiada nad rejestrem, o który olskiemu chodzi.

`Powtórzenie` w ``olski/rozstrzyganie.py`` wskazuje gospodarza, przy którym ta
sama fraza stała już w tym akapicie, a ile razy zdarza się to nad prozą, mówi ta
sonda i nic poza nią. Świadka statystycznego ocenia bank drzew i ocena stoi w tamtym
module, bo tabela i materiał do oceny wychodzą z jednego korpusu. Tu jest
inaczej: dowodem jest akapit, więc materiałem musi być tekst ciągły, a bank
drzew jest zbiorem zdań stojących osobno.

**Pozycji nie wyznacza werdykt, tylko morfologia**, bo świadek pytany o
przyłączenia z werdyktów odpowiadałby o gramatyce; wywód i liczby pod nim trzyma
``pytania`` w ``harness/wieloznaczność.py``. Wzorzec czytany ręką stoi nad tą samą
populacją (``harness/wybory.py``), więc zasięg zmierzony tutaj i trafność zmierzona
tam mówią o jednych pytaniach.

**Milczenie ma dwie przyczyny i osobno każda z nich myli.** Świadek nie ma czego
przeczytać, bo zdanie stoi pierwsze w swoim akapicie; albo przeczytał i fraza tam
nie stała. Pierwsza jest własnością rejestru, druga świadka, a jedna liczba na
wyjściu nie mówi, która przeważyła, więc sonda wypisuje oba mianowniki obok
siebie.

**Wariant wycenia jeden warunek świadka**, tak jak sonda różnicowa wycenia grupę
produkcji: różnica między świadkiem wypuszczanym a tym samym świadkiem z jednym
warunkiem zdjętym jest ceną tego warunku. Które warunki i przy jakiej granicy
sąsiedztwa, mówi :class:`Pomiar`. Wariant nie jest propozycją: akapit ma
uzasadnienie, które trzyma ``docs/rozstrzyganie.md``, a cenę trzeba znać, zanim
ktoś je podważy.

Trafności ta sonda nie liczy i nie ma czym: wzorca, który mówi, przy którym
gospodarzu fraza stoi naprawdę, nad tym korpusem nie ma. Wypisuje więc każdą
odpowiedź wraz ze zdaniem, nad którym padła, bo trafność nad tym materiałem
czyta się ręką, a przeczytane stoi w ``docs/rozstrzyganie.md``.

Korpusem jest proza wyekstrahowana z korpusu audytowego, a skąd ją wziąć, mówi
``docs/audit-corpus.md``:

    python3 -m harness.powtórzenie proza/
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.komenda import Komenda, uruchom
from harness.wieloznaczność import pytania
from olski.document import Document
from olski.rozstrzyganie import Powtórzenie, Rozstrzygnięcie, Sąsiedztwo, sąsiedztwa


def _sąsiad(słowa: Sequence[str], i: int) -> Iterator[str]:
    """Sam sąsiad bezpośredni frazy, czyli reguła węższa od łańcucha imiennego."""
    yield słowa[i - 1]


def _prefiks(słowa: Sequence[str], i: int) -> Iterator[str]:
    """Każde słowo zdania stojące przed frazą, czyli łańcuch bez granicy grupy."""
    yield from reversed(słowa[:i])


#: Reguły kandydata mierzone obok tej, którą warstwa wypuszcza: jedna węższa,
#: jedna szersza. Nazwa jest nagłówkiem wiersza, a funkcja odpowiedzią na pytanie,
#: co w sąsiedztwie liczy się za miejsce przy gospodarzu.
REGUŁY = (("sąsiad bezpośredni", _sąsiad), ("cały prefiks zdania", _prefiks))


@dataclass(frozen=True)
class Odpowiedź:
    """Wskazanie świadka wraz z miejscem, w którym padło, do przeczytania ręką.

    Plik idzie ścieżką, a nie nazwą: korpus audytowy ma dwa ``README.txt``, po
    jednym na repozytorium, a odpowiedź, której nie da się znaleźć w tekście,
    nie da się też przeczytać.
    """

    plik: Path
    zdanie: str
    rozstrzygnięcie: Rozstrzygnięcie


@dataclass
class Pomiar:
    """Co świadek zastał w rejestrze i ile z tego wykorzystał."""

    #: Pliki, po których wyszły liczby niżej.
    plików: int = 0
    #: Zdania korpusu, czyli mianownik całego przebiegu.
    zdań: int = 0
    #: Zdania stojące pierwsze w swoim akapicie, czyli te bez czego przeczytać.
    bez_sąsiedztwa: int = 0
    #: Pozycje przyłączeniowe, o które świadek jest pytany.
    przyłączeń: int = 0
    #: Z nich te, które mają za sobą choć jedno zdanie tego samego akapitu.
    przyłączeń_z_sąsiedztwem: int = 0
    odpowiedzi: list[Odpowiedź] = field(default_factory=list)
    #: Te same odpowiedzi bez warunku na kopulę, czyli cena tego warunku w granicy akapitu.
    odpowiedzi_z_kopulą: list[Odpowiedź] = field(default_factory=list)
    #: Te same odpowiedzi, gdy granicą sąsiedztwa jest dokument, a nie akapit.
    odpowiedzi_bez_granicy: list[Odpowiedź] = field(default_factory=list)
    #: Te same odpowiedzi dla każdej reguły kandydata z :data:`REGUŁY`, po nazwie reguły.
    #: Bez granicy akapitu, bo w jej granicy każda z nich milczy tak czy owak.
    warianty: dict[str, list[Odpowiedź]] = field(default_factory=dict)


def przebieg(wejścia: Iterable[tuple[Path, str]]) -> Pomiar:
    """Przejdź prozę zdanie po zdaniu i zapytaj świadka o każde przyłączenie.

    Świadek jest tu tym samym, którego wypuszcza ``olski-check``, a nie kopią
    przepisaną tutaj: sonda mierząca własny odpis mierzyłaby siebie. Warianty
    różnią się od niego jednym polem, więc i one są nim, a nie jego odpisem.

    Tekst przychodzi razem ze ścieżką, bo pliki czyta wiersz poleceń
    (``harness/komenda.py``), a ścieżka nazywa potem miejsce każdej odpowiedzi.
    """
    pomiar = Pomiar(warianty={nazwa: [] for nazwa, _ in REGUŁY})
    for path, text in sorted(wejścia):
        _plik(path, text, pomiar)
    return pomiar


def _plik(path: Path, text: str, pomiar: Pomiar) -> None:
    pomiar.plików += 1
    document = Document(text)
    akapity = sąsiedztwa(text)
    #  Wariant bez granicy akapitu jest prefiksem zdań tego pliku, więc zdania
    #  trzyma się w liście: akapit niesie tylko te ze swojego.
    zdania = [document.slice(span) for span in document.sentences]
    świadek = Powtórzenie()
    z_kopulą = Powtórzenie(kopuly=frozenset())
    warianty = [
        (Powtórzenie(kandydaci=reguła), pomiar.warianty[nazwa]) for nazwa, reguła in REGUŁY
    ]
    pomiar.zdań += len(zdania)
    pomiar.bez_sąsiedztwa += sum(not akapit.zdania for akapit in akapity)
    for i, (zdanie, akapit) in enumerate(zip(zdania, akapity, strict=True)):
        dokument = Sąsiedztwo(tuple(zdania[:i]))
        for przyłączenie in pytania(zdanie):
            pomiar.przyłączeń += 1
            pomiar.przyłączeń_z_sąsiedztwem += bool(akapit.zdania)
            wołania = [
                (świadek, akapit, pomiar.odpowiedzi),
                (z_kopulą, akapit, pomiar.odpowiedzi_z_kopulą),
                (świadek, dokument, pomiar.odpowiedzi_bez_granicy),
                *((wariant, dokument, gdzie) for wariant, gdzie in warianty),
            ]
            for kto, sąsiedztwo, gdzie in wołania:
                odpowiedź = kto(przyłączenie, sąsiedztwo)
                if odpowiedź is not None:
                    gdzie.append(Odpowiedź(path, zdanie, odpowiedź))


def _wiersze(nagłówek: str, odpowiedzi: Sequence[Odpowiedź], przyłączeń: int) -> list[str]:
    udział = len(odpowiedzi) / przyłączeń if przyłączeń else 0.0
    wiersze = [f"  {nagłówek}: {len(odpowiedzi)}, czyli {udział:.1%} przyłączeń"]
    for o in odpowiedzi:
        wiersze.append(f"    {o.plik}: {o.zdanie}")
        wskazanie = f"„{o.rozstrzygnięcie.modyfikator}” → „{o.rozstrzygnięcie.gospodarz}”"
        wiersze.append(f"      {wskazanie}")
        wiersze.append(f"      {o.rozstrzygnięcie.powód}")
    return wiersze


def wydruk(pomiar: Pomiar) -> str:
    """Zasięg świadka wraz z każdą jego odpowiedzią, bo trafność czyta się ręką."""
    wiersze = [
        f"{pomiar.plików} plików, {pomiar.zdań} zdań",
        f"  pierwszych w akapicie: {pomiar.bez_sąsiedztwa} "
        f"({pomiar.bez_sąsiedztwa / pomiar.zdań:.1%}), czyli bez czego przeczytać",
        f"  przyłączeń: {pomiar.przyłączeń}, z tego z sąsiedztwem: "
        f"{pomiar.przyłączeń_z_sąsiedztwem}",
    ]
    listy = [
        ("odpowiedzi w granicy akapitu", pomiar.odpowiedzi),
        ("to samo bez warunku na kopulę", pomiar.odpowiedzi_z_kopulą),
        ("odpowiedzi bez granicy akapitu", pomiar.odpowiedzi_bez_granicy),
        *((f"to samo przy regule „{nazwa}”", pomiar.warianty[nazwa]) for nazwa, _ in REGUŁY),
    ]
    for nagłówek, odpowiedzi in listy:
        wiersze += _wiersze(nagłówek, odpowiedzi, pomiar.przyłączeń)
    return "\n".join(wiersze)


def _proza(wejścia: Sequence[tuple[Path, str]], args: argparse.Namespace) -> str:
    return wydruk(przebieg(wejścia))


KOMENDA = Komenda(
    nazwa="harness.powtórzenie",
    opis="Policz, ile świadek kontekstowy odpowiada nad prozą.",
    proza=_proza,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
