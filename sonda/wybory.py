"""Co warstwa rozstrzygająca mówi o wyborach przeczytanych ręką, w ich własnym tekście.

Świadka statystycznego można ocenić bankiem drzew, bo tam odpowiedź stoi w
drzewie. Świadka kontekstowego nie można: bank drzew jest zbiorem zdań stojących
osobno, a dowodem tego świadka jest zdanie poprzednie. Nad korpusem audytowym
sytuacja jest odwrotna — tekst jest ciągły, a odpowiedzi nie ma tam żadnej.
Ta sonda dokłada tę odpowiedź i jest jedynym miejscem w repozytorium, gdzie
wzorzec pochodzi z przeczytania, a nie z cudzego korpusu ani z przebiegu.

**Zdania są cudze, a wzorzec nasz.** Zdanie wymyślone pod świadka mierzy autora,
a nie rejestr, więc pozycje bierze się z korpusu audytowego takie, jakie tam
stoją, i losuje (``rozrzucona`` w ``olski/próbka.py``).
Ręką dopisuje się jedno: który gospodarz jest tym, o którego w tym tekście
chodziło. Rozkładu to nie rusza, bo o rozkładzie decyduje losowanie, a nie ten,
kto potem czyta.

**Losowania są dwa i mierzą dwie różne rzeczy**, więc mają dwa pliki, a nie jeden
z kolumną obok wpisu: mianownik należy do losowania, a jeden wydruk z dwoma
mianownikami czyta się jako jeden. ``próba/wybory.txt`` losuje spośród wszystkich
pozycji i mówi, jak często warstwa odpowiada;
``próba/wybory-z-odpowiedzią.txt`` losuje spośród tych, nad którymi się odzywa,
i mówi, jak często się myli. Drugie z nich robi :func:`z_odpowiedzią`,
która wyjaśnia, dlaczego pierwsze na częstość pomyłek nie starcza.

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
    python3 -m sonda.wybory --zbuduj proza/ --ile 30 --z-odpowiedzią > nowe.txt
    python3 -m sonda.wybory próba/wybory.txt
    python3 -m sonda.wybory próba/wybory-z-odpowiedzią.txt
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

#: Pliki z wyborami przeczytanymi ręką, czyli jedyny wzorzec, jaki ta warstwa ma.
#: Pierwszy jest losowaniem z całej populacji, drugi zawężonym do samych odpowiedzi.
WYBORY = Path(__file__).parent.parent / "próba" / "wybory.txt"
WYBORY_Z_ODPOWIEDZIĄ = Path(__file__).parent.parent / "próba" / "wybory-z-odpowiedzią.txt"

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
# nie z cudzego korpusu. Zdania są cudze, żeby rozkład był rejestru, a nie
# autora; skąd je wziąć, mówi docs/audit-corpus.md.
#
# Nowych wpisów ta komenda tutaj nie dopisze i tego pliku nie umie uzupełnić:
# wypisuje całość na wyjście, więc puszczona w to miejsce skasowałaby każdy
# wzorzec, jaki tu stoi. Nowe idą do pliku obok i przenosi się je ręką.
#
# Wzorzec wpisuje się przed puszczeniem sondy nad plikiem, bo wydruk pokazuje
# odpowiedź warstwy wraz z jej powodem, a sąd czytany po niej broni się już tylko
# tym, co ma zapisane w `powód`.
#
{skąd}#
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
# morfologii, więc sięga frazą dalej, niż ona idzie, a gospodarzem proponuje cały
# łańcuch imienny, który homonimia przedłuża czasem przez orzeczenie. Wpis ma
# opisywać wybór, który widzi czytelnik.
"""

#: Zdanie o losowaniu, po jednym na każde z dwóch, jakie ma `--zbuduj`. Stoi
#: w pliku, bo mianownik, do którego wpisy należą, jest własnością losowania:
#: nad próbą z całej populacji mianownikiem jest pozycja rejestru, a nad próbą
#: spośród pozycji z odpowiedzią — odpowiedź warstwy, i te dwie liczby mówią o
#: czym innym.
Z_CAŁOŚCI = """\
# Losowane spośród wszystkich pozycji przyłączeniowych korpusu, więc mianownikiem
# jest pozycja rejestru: liczy się nad tym plikiem i to, jak często warstwa
# odpowiada, i to, jak często trafia.
"""

Z_ODPOWIEDZIĄ = """\
# Losowane spośród tych pozycji, nad którymi warstwa się odzywa, więc mianownikiem
# jest odpowiedź, a nie pozycja rejestru: częstość odpowiedzi tego pliku nie mierzy
# i wychodzi w nim z założenia bliska całości. Mierzy się nad nim częstość pomyłek,
# której próba z całej populacji nie unosi, bo odpowiedzi pada w niej kilka.
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


def zapisz(wybory: Iterable[Wybór], skąd: str = Z_CAŁOŚCI) -> str:
    """Wpisy jako tekst pliku, w kolejności podanej, wraz ze zdaniem o losowaniu."""
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
    return NAGŁÓWEK.format(skąd=skąd) + "\n" + "\n\n".join(bloki) + "\n"


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


def z_odpowiedzią(
    wybory: Iterable[Wybór], świadkowie: Sequence[Świadek] | None = None
) -> list[Wybór]:
    """Te z pozycji, nad którymi warstwa się odzywa, w kolejności podanej.

    Losowanie z całej populacji daje częstość odpowiedzi i nie daje częstości
    pomyłek: warstwa odzywa się nad tym rejestrem raz na dziewięć pozycji, więc
    trzydzieści wylosowanych zdań niesie pięć odpowiedzi i jedna pomyłka przesuwa
    stopę o dwadzieścia punktów. Populacja zawężona do odpowiedzi ma tego samego
    rzędu wielkości liczbę wpisów do przeczytania i mianownik, którym mierzy się
    pomyłkę.

    Zawężenie idzie po tym, czy odzywa się którykolwiek świadek, a nie po tym,
    który: warunek nazywający świadka trzeba by dopisać do świadka dopisanego
    jutro, a częstość pomyłek jest pytaniem o warstwę.

    Cena zawężenia jest w propozycji: pytanie idzie o frazę i gospodarzy, jakich
    daje morfologia, a czytający poprawia oboje, więc wpis, na który warstwa
    odpowiedziała przed poprawką, bywa po niej wpisem, nad którym milczy. Wychodzi
    to w liczbach tego pliku i nie jest usterką losowania: fraza poprawiona jest
    tą, o którą pyta czytelnik.
    """
    if świadkowie is None:
        świadkowie = domyślni()
    zebrane = []
    for wybór in wybory:
        (odpowiedź,) = rozstrzygnij([wybór.przyłączenie], świadkowie, wybór.sąsiedztwo)
        if isinstance(odpowiedź, Rozstrzygnięcie):
            zebrane.append(wybór)
    return zebrane


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
    parser.add_argument(
        "--z-odpowiedzią",
        action="store_true",
        help="losuj spośród pozycji, nad którymi warstwa się odzywa",
    )
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
    populacja = kandydaci(ścieżki, root)
    skąd = Z_CAŁOŚCI
    if args.z_odpowiedzią:
        populacja, skąd = z_odpowiedzią(populacja), Z_ODPOWIEDZIĄ
    print(zapisz(rozrzucona(populacja, args.ile), skąd), end="")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
