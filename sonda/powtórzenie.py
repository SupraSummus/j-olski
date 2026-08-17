"""Ile świadek kontekstowy odpowiada nad rejestrem, o który olskiemu chodzi.

`Powtórzenie` w ``olski/rozstrzyganie.py`` wskazuje gospodarza, przy którym ta
sama fraza stała już w tym akapicie, a ile razy zdarza się to nad prozą, mówi ta
sonda i nic poza nią. Świadka statystycznego ocenia bank drzew i ocena stoi w tamtym
module, bo tabela i materiał do oceny wychodzą z jednego korpusu. Tu jest
inaczej: dowodem jest akapit, więc materiałem musi być tekst ciągły, a bank
drzew jest zbiorem zdań stojących osobno.

**Pozycji nie wyznacza werdykt, tylko morfologia**, bo świadek pytany o
przyłączenia z werdyktów odpowiadałby o gramatyce; wywód i liczby pod nim trzyma
``pytania`` w ``olski/wieloznaczność.py``. Wzorzec czytany ręką stoi nad tą samą
populacją (``sonda/wybory.py``), więc zasięg zmierzony tutaj i trafność zmierzona
tam mówią o jednych pytaniach.

**Milczenie ma dwie przyczyny i osobno każda z nich myli.** Świadek nie ma czego
przeczytać, bo zdanie stoi pierwsze w swoim akapicie; albo przeczytał i fraza tam
nie stała. Pierwsza jest własnością rejestru, druga świadka, a jedna liczba na
wyjściu nie mówi, która przeważyła, więc sonda wypisuje oba mianowniki obok
siebie.

**Granicę sąsiedztwa wycenia wariant, tak jak sonda różnicowa wycenia grupę
produkcji.** Wariantem jest cały dokument czytany wstecz, czyli sąsiedztwo bez
granicy akapitu, a różnica między nim a akapitem jest ceną tej granicy. Wariant
nie jest propozycją: akapit ma uzasadnienie, które trzyma
``docs/disambiguation.md``, a cenę trzeba znać, zanim ktoś je podważy.

**Regułę kandydata wycenia drugi wariant, tą samą drogą.** Wariantem jest inne
``kandydaci`` w :class:`Powtórzenie`, czyli inna odpowiedź na to, co w sąsiedztwie
liczy się za miejsce przy gospodarzu: sam sąsiad bezpośredni frazy albo cały
prefiks zdania przed nią, obok łańcucha imiennego, który warstwa wypuszcza.
Warianty te mierzy się bez granicy akapitu, bo w jej granicy świadek milczy tak
czy owak, a wybór między trzema regułami stoi na przeczytaniu odpowiedzi, nie na
ich liczbie.

Trafności ta sonda nie liczy i nie ma czym: wzorca, który mówi, przy którym
gospodarzu fraza stoi naprawdę, nad tym korpusem nie ma. Wypisuje więc każdą
odpowiedź wraz ze zdaniem, nad którym padła, bo trafność nad tym materiałem
czyta się ręką, a przeczytane stoi w ``docs/disambiguation.md``.

Korpusem jest proza wyekstrahowana z korpusu audytowego, a skąd ją wziąć, mówi
``docs/audit-corpus.md``:

    python3 -m sonda.powtórzenie proza/
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.document import Document
from olski.rozstrzyganie import Powtórzenie, Rozstrzygnięcie, Sąsiedztwo, sąsiedztwa
from olski.wieloznaczność import pytania

#: Rozszerzenie, którym ekstrakcja pisze prozę (``harness/markdown.py``).
PROZA = "*.txt"


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

    #: Zdania korpusu, czyli mianownik całego przebiegu.
    zdań: int = 0
    #: Zdania stojące pierwsze w swoim akapicie, czyli te bez czego przeczytać.
    bez_sąsiedztwa: int = 0
    #: Pozycje przyłączeniowe, o które świadek jest pytany.
    przyłączeń: int = 0
    #: Z nich te, które mają za sobą choć jedno zdanie tego samego akapitu.
    przyłączeń_z_sąsiedztwem: int = 0
    odpowiedzi: list[Odpowiedź] = field(default_factory=list)
    #: To samo, gdy granicą sąsiedztwa jest dokument, a nie akapit.
    odpowiedzi_bez_granicy: list[Odpowiedź] = field(default_factory=list)
    #: To samo dla każdej reguły kandydata z :data:`REGUŁY`, po nazwie reguły.
    #: Bez granicy akapitu, bo w jej granicy każda z nich milczy tak czy owak.
    warianty: dict[str, list[Odpowiedź]] = field(default_factory=dict)


def przebieg(paths: Iterable[Path]) -> Pomiar:
    """Przejdź prozę zdanie po zdaniu i zapytaj świadka o każde przyłączenie.

    Świadek jest tu tym samym, którego wypuszcza ``olski-check``, a nie kopią
    przepisaną tutaj: sonda mierząca własny odpis mierzyłaby siebie. Warianty
    różnią się od niego jednym polem, więc i one są nim, a nie jego odpisem.
    """
    pomiar = Pomiar(warianty={nazwa: [] for nazwa, _ in REGUŁY})
    for path in sorted(paths):
        _plik(path, pomiar)
    return pomiar


def _plik(path: Path, pomiar: Pomiar) -> None:
    text = path.read_text(encoding="utf-8")
    document = Document(text)
    akapity = sąsiedztwa(text)
    #  Wariant bez granicy akapitu jest prefiksem zdań tego pliku, więc zdania
    #  trzyma się w liście: akapit niesie tylko te ze swojego.
    zdania = [document.slice(span) for span in document.sentences]
    świadek = Powtórzenie()
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
                (świadek, dokument, pomiar.odpowiedzi_bez_granicy),
                *((wariant, dokument, gdzie) for wariant, gdzie in warianty),
            ]
            for kto, sąsiedztwo, gdzie in wołania:
                odpowiedź = kto(przyłączenie, sąsiedztwo)
                if odpowiedź is not None:
                    gdzie.append(Odpowiedź(path, zdanie, odpowiedź))


def _wypisz(nagłówek: str, odpowiedzi: Sequence[Odpowiedź], przyłączeń: int) -> None:
    udział = len(odpowiedzi) / przyłączeń if przyłączeń else 0.0
    print(f"  {nagłówek}: {len(odpowiedzi)}, czyli {udział:.1%} przyłączeń")
    for o in odpowiedzi:
        print(f"    {o.plik}: {o.zdanie}")
        print(f"      „{o.rozstrzygnięcie.modyfikator}” → „{o.rozstrzygnięcie.gospodarz}”")
        print(f"      {o.rozstrzygnięcie.powód}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m sonda.powtórzenie",
        description="Policz, ile świadek kontekstowy odpowiada nad prozą.",
    )
    parser.add_argument("root", help="katalog z prozą wyekstrahowaną do plików .txt")
    args = parser.parse_args(argv)

    root = Path(args.root)
    ścieżki = sorted(root.rglob(PROZA))
    if not ścieżki:
        print(f"sonda.powtórzenie: nie ma tu prozy: {root}/{PROZA}")
        print("sonda.powtórzenie: skąd wziąć korpus, mówi docs/audit-corpus.md")
        return 2

    pomiar = przebieg(ścieżki)
    print(f"{len(ścieżki)} plików, {pomiar.zdań} zdań")
    print(
        f"  pierwszych w akapicie: {pomiar.bez_sąsiedztwa} "
        f"({pomiar.bez_sąsiedztwa / pomiar.zdań:.1%}), czyli bez czego przeczytać"
    )
    print(
        f"  przyłączeń: {pomiar.przyłączeń}, z tego z sąsiedztwem: "
        f"{pomiar.przyłączeń_z_sąsiedztwem}"
    )
    _wypisz("odpowiedzi w granicy akapitu", pomiar.odpowiedzi, pomiar.przyłączeń)
    _wypisz("odpowiedzi bez granicy akapitu", pomiar.odpowiedzi_bez_granicy, pomiar.przyłączeń)
    for nazwa, _ in REGUŁY:
        _wypisz(f"to samo przy regule „{nazwa}”", pomiar.warianty[nazwa], pomiar.przyłączeń)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
