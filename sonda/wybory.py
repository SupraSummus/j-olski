"""Co warstwa rozstrzygająca mówi o wyborach przeczytanych ręką, w ich własnym tekście.

Świadka statystycznego można ocenić bankiem drzew, bo tam odpowiedź stoi w
drzewie. Świadka kontekstowego nie można: bank drzew jest zbiorem zdań stojących
osobno, a dowodem tego świadka jest zdanie poprzednie. Nad korpusem audytowym
sytuacja jest odwrotna — tekst jest ciągły, a odpowiedzi nie ma tam żadnej.
Ta sonda dokłada tę odpowiedź i jest jedynym miejscem w repozytorium, gdzie
wzorzec pochodzi z przeczytania, a nie z cudzego korpusu ani z przebiegu.

**Zdania są cudze, a wzorzec nasz.** Zdanie wymyślone pod świadka mierzy autora,
a nie rejestr, więc pozycje bierze się z korpusu audytowego takie, jakie tam
stoją, i losuje spośród wszystkich (``rozrzucona`` w ``olski/próbka.py``).
Ręką dopisuje się jedno: który gospodarz jest tym, o którego w tym tekście
chodziło. Rozkładu to nie rusza, bo o rozkładzie decyduje losowanie, a nie ten,
kto potem czyta.

**Pozycji nie wyznacza werdykt, tylko morfologia**, bo werdyktów jest nad tym
rejestrem za mało, żeby cokolwiek zmierzyć; wywód i liczby pod nim trzyma
``pytania`` w ``olski/wieloznaczność.py``, a zasięg nad tą samą populacją mierzy
``sonda/powtórzenie.py``. Ceną jest to, że wybór bywa pozorny: przyimek, którego
żąda schemat czasownika, stoi w tej pozycji i do wyboru nie stoi wcale, a odsiewa
go dopiero czytający.

**Wzorzec ma dwie odpowiedzi poza samymi gospodarzami.** ``oba`` znaczy, że
tekst nie rozstrzyga i czytelnik też nie, a ``żadne``, że wyboru nie ma wcale, bo
pozycja nie jest przyłączeniem. Obie są tu po to, żeby milczenie warstwy dało się
ocenić: nad takim wpisem milczenie jest odpowiedzią trafną, a nie brakiem
odpowiedzi. Rozdzielone są, bo mówią o czym innym — pierwsza o rejestrze, druga o
celności szukacza pozycji — a złożone w jeden licznik dawałyby liczbę, która nie
wie, o czym jest.

Plik z wyborami jest połową droższą i nie jest generowany: ``--zbuduj`` wypisuje
kandydatów z pustym wzorcem na wyjście, a wzorzec wpisuje się ręką wraz z
powodem. Wypisuje przy tym całość, więc puszczony na plik z wzorcami skasowałby
je wszystkie; nowe wpisy przenosi się do niego ręką.

    python3 -m sonda.wybory --zbuduj proza/ --ile 30 > nowe.txt
    python3 -m sonda.wybory próba/wybory.txt
"""

from __future__ import annotations

import argparse
import collections
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from olski.document import Document
from olski.parse import Przyłączenie
from olski.próbka import rozrzucona
from olski.rozstrzyganie import (
    Rozstrzygnięcie,
    Sąsiedztwo,
    Świadek,
    domyślni,
    rozstrzygnij,
    sąsiedztwa,
)
from olski.wieloznaczność import pytania

#: Rozszerzenie, którym ekstrakcja pisze prozę (``harness/markdown.py``).
PROZA = "*.txt"

#: Plik z wyborami przeczytanymi ręką, czyli jedyny wzorzec, jaki ta warstwa ma.
WYBORY = Path(__file__).parent.parent / "próba" / "wybory.txt"

#: Wzorzec zdania, którego ten tekst nie rozstrzyga: warstwa ma nad nim milczeć.
OBA = "oba"

#: Wzorzec pozycji, w której wyboru nie ma wcale: fraza nie jest frazą albo stoi
#: przy niej jeden gospodarz. Milczenie jest tu tak samo trafne jak przy
#: :data:`OBA`, a liczy się osobno, bo mówi o czym innym: tamto o rejestrze, a to
#: o celności szukacza pozycji z ``olski/wieloznaczność.py``.
ŻADNE = "żadne"

#: Wzorce, na które trafną odpowiedzią jest milczenie.
DO_PRZEMILCZENIA = (OBA, ŻADNE)

#: Wzorzec jeszcze niewpisany. Wpis z nim nie wchodzi do żadnego mianownika,
#: bo pytanie bez odpowiedzi nie jest ani trafieniem, ani pomyłką.
PUSTY = "?"


@dataclass(frozen=True)
class Wybór:
    """Jedno przyłączenie z korpusu wraz z tym, dokąd doszło, i z jego akapitem."""

    plik: str
    #: Zdania tego akapitu stojące przed zdaniem spornym, w kolejności.
    kontekst: tuple[str, ...]
    zdanie: str
    #: Formy modyfikatora, czyli to, o co pytana jest warstwa.
    fraza: str
    #: Formy gospodarzy, tak jak nazywa je werdykt.
    gospodarze: tuple[str, ...]
    #: Gospodarz, o którego w tym tekście chodziło, albo :data:`OBA`,
    #: :data:`ŻADNE`, albo :data:`PUSTY`.
    wzorzec: str = PUSTY
    #: Czym to rozstrzygnięto, jednym zdaniem. Wzorzec bez powodu jest sądem,
    #: którego nikt nie sprawdzi, a sprawdzalność jest tu całą wartością wpisu.
    powód: str = ""

    @property
    def przyłączenie(self) -> Przyłączenie:
        return Przyłączenie(modyfikator=self.fraza, gospodarze=self.gospodarze)

    @property
    def sąsiedztwo(self) -> Sąsiedztwo:
        return Sąsiedztwo(self.kontekst)


@dataclass
class Ocena:
    """Ile warstwa odpowiada nad wyborami z wzorcem i ile z tego trafia."""

    #: Wpisy ze wzorcem wpisanym, czyli mianownik.
    wypadków: int = 0
    #: Z nich te do przemilczenia, po jednym liczniku na powód: tekst nie
    #: rozstrzyga albo wyboru nie ma wcale.
    do_przemilczenia: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Odpowiedzi i trafienia po świadku. Milczenie bywa trafieniem i świadka
    #: nie ma, więc liczy się osobno.
    odpowiedzi: collections.Counter[str] = field(default_factory=collections.Counter)
    trafień: collections.Counter[str] = field(default_factory=collections.Counter)
    #: Przemilczane trafnie, czyli wpisy z :data:`DO_PRZEMILCZENIA`,
    #: nad którymi warstwa milczy.
    przemilczanych: int = 0
    #: Wpisy bez wzorca, do przeczytania przez tego, kto plik uzupełnia.
    bez_wzorca: int = 0
    #: Co padło nad którym wpisem, do wypisania pod liczbami.
    wypisy: list[str] = field(default_factory=list)


def oceń(wybory: Iterable[Wybór], świadkowie: Sequence[Świadek] | None = None) -> Ocena:
    """Zapytaj warstwę o każdy wybór i zestaw odpowiedź z wzorcem.

    Świadkowie są ci sami, których wypuszcza ``olski-check``, a nie kopia
    przepisana tutaj: sonda mierząca własny odpis mierzyłaby siebie.
    """
    if świadkowie is None:
        świadkowie = domyślni()
    ocena = Ocena()
    for wybór in wybory:
        if wybór.wzorzec == PUSTY:
            ocena.bez_wzorca += 1
            continue
        ocena.wypadków += 1
        if wybór.wzorzec in DO_PRZEMILCZENIA:
            ocena.do_przemilczenia[wybór.wzorzec] += 1
        (odpowiedź,) = rozstrzygnij([wybór.przyłączenie], świadkowie, wybór.sąsiedztwo)
        _zapisz(ocena, wybór, odpowiedź if isinstance(odpowiedź, Rozstrzygnięcie) else None)
    return ocena


def _zapisz(ocena: Ocena, wybór: Wybór, odpowiedź: Rozstrzygnięcie | None) -> None:
    if odpowiedź is None:
        milczeć = wybór.wzorzec in DO_PRZEMILCZENIA
        ocena.przemilczanych += milczeć
        ocena.wypisy.append(
            f"  {'cisza +' if milczeć else 'cisza  '} „{wybór.fraza}” "
            f"[{wybór.wzorzec}] w: {wybór.zdanie}"
        )
        return
    trafiła = odpowiedź.gospodarz == wybór.wzorzec
    ocena.odpowiedzi[odpowiedź.świadek] += 1
    ocena.trafień[odpowiedź.świadek] += trafiła
    ocena.wypisy.append(
        f"  {'trafna ' if trafiła else 'pomyłka'} „{wybór.fraza}” → „{odpowiedź.gospodarz}”, "
        f"wzorzec: {wybór.wzorzec}\n    {wybór.zdanie}\n    {odpowiedź.powód}"
    )


# --------------------------------------------------------------------------- #
# Plik z wyborami
# --------------------------------------------------------------------------- #

#: Klucze wpisu, w kolejności, w jakiej stoją w pliku. Kontekst bywa kilkoma
#: wierszami, bo akapit bywa kilkoma zdaniami.
KLUCZE = ("plik", "kontekst", "zdanie", "fraza", "gospodarze", "wzorzec", "powód")

NAGŁÓWEK = """\
# Wybory przyłączeniowe korpusu audytowego, z gospodarzem przeczytanym ręką.
#
# Plik stoi poza `sonda/`, bo sonda jest kodem pisanym pod decyzję i kasowalnym,
# a te wpisy są tu najdroższą rzeczą: kasując `sonda/wybory.py`, kasuje się
# program, a nie przeczytane zdania.
#
# Wpisy wypisuje `python3 -m sonda.wybory --zbuduj`, a `wzorzec` i `powód`
# wpisuje w nie człowiek: jest to jedyny wzorzec, jaki warstwa rozstrzygająca w
# tym repozytorium ma, i jedyne miejsce, w którym sąd o zdaniu pochodzi stąd, a
# nie z cudzego korpusu. Zdania są cudze i losowane, żeby rozkład był rejestru,
# a nie autora; skąd je wziąć, mówi docs/audit-corpus.md.
#
# Nowych wpisów ta komenda tutaj nie dopisze i tego pliku nie umie uzupełnić:
# wypisuje całość na wyjście, więc puszczona w to miejsce skasowałaby każdy
# wzorzec, jaki tu stoi. Nowe idą do pliku obok i przenosi się je ręką.
#
# Wpisy pochodzą z korpusu audytowego przy ksef-docs 1c34fe2 i rit-dokumentacja
# 32f85cc. Zdanie i kontekst stoją w nich w całości, więc nowsze wydanie tamtych
# repozytoriów wpisu nie unieważnia; mówi tylko, że wylosowano go z tamtego.
#
# `wzorzec` jest jedną z form z `gospodarze`, słowem `oba`, kiedy tekst nie
# rozstrzyga i czytelnik też nie, albo słowem `żadne`, kiedy wyboru nie ma
# wcale, bo fraza nie jest frazą albo stoi przy niej jeden gospodarz. Nad
# dwoma ostatnimi milczenie warstwy jest odpowiedzią trafną. `powód` mówi, na
# czym stanął sąd, bo wzorzec bez powodu jest zdaniem, którego nikt nie
# sprawdzi.
#
# `fraza` i `gospodarze` też są poprawiane ręką: budowniczy proponuje je z
# morfologii, więc bierze ogon łańcucha dopełniaczowego za głowę grupy i sięga
# frazą dalej, niż ona idzie. Wpis ma opisywać wybór, który widzi czytelnik.
"""


def czytaj(path: Path = WYBORY) -> list[Wybór]:
    """Wpisy z pliku; wpis bez zdania albo bez frazy jest błędem, a nie ciszą."""
    wybory = []
    for numer, blok in _bloki(path.read_text(encoding="utf-8")):
        pola: dict[str, list[str]] = {}
        for wiersz in blok:
            klucz, _, wartość = wiersz.partition(":")
            if klucz not in KLUCZE:
                raise ValueError(f"{path}:{numer}: nieznany klucz {klucz!r}")
            pola.setdefault(klucz, []).append(wartość.strip())
        brakujące = {"zdanie", "fraza", "gospodarze"} - pola.keys()
        if brakujące:
            raise ValueError(f"{path}:{numer}: wpis bez {', '.join(sorted(brakujące))}")
        wybory.append(
            Wybór(
                plik=" ".join(pola.get("plik", ())),
                kontekst=tuple(pola.get("kontekst", ())),
                zdanie=pola["zdanie"][0],
                fraza=pola["fraza"][0],
                gospodarze=tuple(g.strip() for g in pola["gospodarze"][0].split(",")),
                wzorzec=pola.get("wzorzec", [PUSTY])[0] or PUSTY,
                powód=" ".join(pola.get("powód", ())),
            )
        )
    return wybory


def _bloki(tekst: str) -> list[tuple[int, list[str]]]:
    """Wpisy pliku, każdy ze swoim pierwszym wierszem, żeby błąd miał adres."""
    bloki, blok, numer = [], [], 0
    for i, wiersz in enumerate(tekst.splitlines(), start=1):
        if wiersz.startswith("#") or not wiersz.strip():
            if blok:
                bloki.append((numer, blok))
                blok = []
            continue
        if not blok:
            numer = i
        blok.append(wiersz)
    if blok:
        bloki.append((numer, blok))
    return bloki


def zapisz(wybory: Iterable[Wybór]) -> str:
    """Wpisy jako tekst pliku, w kolejności podanej."""
    bloki = []
    for wybór in wybory:
        wiersze = [f"plik: {wybór.plik}"]
        wiersze += [f"kontekst: {zdanie}" for zdanie in wybór.kontekst]
        wiersze += [
            f"zdanie: {wybór.zdanie}",
            f"fraza: {wybór.fraza}",
            f"gospodarze: {', '.join(wybór.gospodarze)}",
            f"wzorzec: {wybór.wzorzec}",
            f"powód: {wybór.powód}",
        ]
        bloki.append("\n".join(wiersze))
    return NAGŁÓWEK + "\n" + "\n\n".join(bloki) + "\n"


# --------------------------------------------------------------------------- #
# Budowa kandydatów
# --------------------------------------------------------------------------- #


def kandydaci(paths: Iterable[Path], korzeń: Path) -> list[Wybór]:
    """Pozycje przyłączeniowe całego korpusu, każda ze swoim akapitem.

    Pozycje i frazy daje ``pytania`` w ``olski/wieloznaczność.py``, czyli to samo
    miejsce, z którego bierze je sonda mierząca zasięg świadka kontekstowego
    (``sonda/powtórzenie.py``): wzorzec czytany ręką ma opisywać tę populację,
    którą ta sonda mierzy, a nie populację obok niej.
    """
    znalezione = []
    for path in sorted(paths):
        tekst = path.read_text(encoding="utf-8")
        document = Document(tekst)
        #  Akapit wyznacza ta sama funkcja, która podaje go świadkowi w
        #  ``olski-check``, więc wpis niesie kontekst dokładnie ten, który
        #  warstwa dostanie nad tym zdaniem.
        for span, sąsiedztwo in zip(document.sentences, sąsiedztwa(tekst), strict=True):
            zdanie = document.slice(span)
            znalezione += [
                Wybór(
                    plik=str(path.relative_to(korzeń)),
                    kontekst=sąsiedztwo.zdania,
                    zdanie=zdanie,
                    fraza=pytanie.modyfikator,
                    gospodarze=pytanie.gospodarze,
                )
                for pytanie in pytania(zdanie)
            ]
    return znalezione



# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(ocena: Ocena) -> str:
    milczkiem = sum(ocena.do_przemilczenia.values())
    wiersze = [f"{ocena.wypadków} wyborów ze wzorcem, z tego {milczkiem} do przemilczenia"]
    for nazwa in sorted(ocena.do_przemilczenia):
        wiersze.append(f"  {ocena.do_przemilczenia[nazwa]:>4}  {nazwa}")
    if ocena.bez_wzorca:
        wiersze.append(f"  {ocena.bez_wzorca} wpisów czeka na wzorzec i nie wchodzi do liczb")
    if not ocena.wypadków:
        return "\n".join(wiersze)

    wiersze += ["", "  co warstwa odpowiedziała:"]
    for nazwa in sorted(ocena.odpowiedzi):
        odpowiedzi, trafień = ocena.odpowiedzi[nazwa], ocena.trafień[nazwa]
        wiersze.append(
            f"  {odpowiedzi:>4}  {odpowiedzi / ocena.wypadków:>6.1%} odpowiedzi, "
            f"{trafień / odpowiedzi:>6.1%} trafień    {nazwa}"
        )
    if milczkiem:
        wiersze.append(
            f"  {ocena.przemilczanych:>4}  {ocena.przemilczanych / milczkiem:>6.1%} "
            "wyborów do przemilczenia przemilczanych"
        )
    trafień = sum(ocena.trafień.values()) + ocena.przemilczanych
    wiersze.append(
        f"  {trafień:>4}  {trafień / ocena.wypadków:>6.1%} wyborów rozstrzygniętych dobrze"
    )
    wiersze += ["", "  wpis po wpisie:", *ocena.wypisy]
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m sonda.wybory",
        description="Oceń warstwę rozstrzygającą na wyborach przeczytanych ręką.",
    )
    parser.add_argument("root", nargs="?", help="plik z wyborami; przy --zbuduj katalog z prozą")
    parser.add_argument("--zbuduj", action="store_true", help="wypisz kandydatów z pustym wzorcem")
    parser.add_argument("--ile", type=int, default=30, help="ilu kandydatów wylosować")
    args = parser.parse_args(argv)

    if not args.zbuduj:
        path = Path(args.root) if args.root else WYBORY
        if not path.is_file():
            print(f"sonda.wybory: nie ma takiego pliku: {path}", file=sys.stderr)
            return 2
        print(wydruk(oceń(czytaj(path))))
        return 0

    root = Path(args.root or ".")
    ścieżki = sorted(root.rglob(PROZA))
    if not ścieżki:
        print(f"sonda.wybory: nie ma tu prozy: {root}/{PROZA}", file=sys.stderr)
        print("sonda.wybory: skąd wziąć korpus, mówi docs/audit-corpus.md", file=sys.stderr)
        return 2
    print(zapisz(rozrzucona(kandydaci(ścieżki, root), args.ile)), end="")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
