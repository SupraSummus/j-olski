"""Warstwa za parserem: co rozstrzyga przyłączenie, którego gramatyka nie rozstrzyga.

Zalążek, a nie maszyna. Stoi tu po to, żeby kierunek dał się zmierzyć,
a nie żeby werdykt zmienić: :func:`rozstrzygnij` bierze gotowy wynik rozbioru
i oddaje osobną odpowiedź obok niego, więc ``valid``, ``ambiguous`` i
``rejected`` znaczą po jej dopisaniu dokładnie to, co znaczyły.
Dlaczego akurat tak, wywodzi ``docs/disambiguation.md``:
ranking wstawiony w werdykt myliłby się co trzecie zdanie w miejscu,
w którym ten parser obiecuje prawdę o zdaniu.

Rozstrzygać jest przy tym co: nad Składnicą przyłączenie jest całą decyzją
w 75% zdań, które olski odrzuca za wieloznaczność (tamże).

**Świadek jest jednostką tej warstwy.** Każdy patrzy na jedno przyłączenie
i albo wskazuje gospodarza wraz z powodem, albo milczy. Milczenie jest
odpowiedzią pełnoprawną i jest odpowiedzią domyślną: świadek, który nie ma na
czym stanąć, nie zgaduje. Powód wraca razem ze wskazaniem, żeby wskazanie dało
się sprawdzić bez zaglądania do tabeli.

**Świadkowie idą w kolejności, a kolejność jest kolejnością rodzaju dowodu.**
Pierwszy odpowiadający wygrywa, więc dowód słownikowy bije statystyczny wszędzie
tam, gdzie oba mówią coś naraz. Dzisiaj świadek jest jeden i jest statystyczny.
Drugi, który tu należy i którego nie ma, to rama walencyjna: fraza, której
czasownik albo rzeczownik żąda swoim schematem, nie konkuruje z niczym, tylko
łamie schemat po drugiej stronie, a nad Składnicą jest to 790 z 4 517 wyrażeń
w pozycji spornej (``docs/subset.md``). Nie da się go dziś napisać, bo
``olski/leksykon.txt`` mówi o bierniku i o bezokoliczniku, a o przyimku nie mówi;
co trzeba zmienić w ``olski/walenty.py``, żeby mówił, trzyma ``TODO.md``.

**Świadek statystyczny nazywa własną częstość pomyłek.** :class:`Skłonność`
liczy, jak często ta para przyimka i gospodarza przyłączała się w banku drzew
w tę stronę, i odpowiada dopiero powyżej progu wsparcia i progu przewagi.
Sam przyimek progu nie przechodzi i to jest zamierzone: leksykon przyimków
myli się nad tym korpusem co szóste wyrażenie, a nad najczęstszymi co trzecie
(``docs/subset.md``), czyli mniej więcej tak jak reguła „zawsze do rzeczownika”,
którą ``docs/subset.md`` odrzuciła jako konwencję.

Tabelę buduje się z banku drzew i ocenia na jego drugiej połowie:

    python3 -m olski.rozstrzyganie Składnica-frazowa-180723/ --oceń
    python3 -m olski.rozstrzyganie Składnica-frazowa-180723/ --zbuduj olski/skłonności.txt
"""

from __future__ import annotations

import argparse
import collections
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Protocol

from olski.morph import analyse
from olski.parse import Przyłączenie

#: Plik z tabelą skłonności, generowany i czytany przy pierwszym pytaniu.
SKŁONNOŚCI = Path(__file__).parent / "skłonności.txt"

#: Ile razy para musi wystąpić w banku drzew, żeby świadek w ogóle na nią patrzył,
#: i jaką część tych wystąpień musi mieć po jednej stronie, żeby odpowiedział.
#: Poniżej pierwszego liczba jest szumem, poniżej drugiego bank drzew mówi, że ta
#: para przyłącza się i tak, i tak.
#:
#: Wartości są punktem na krzywej, a nie prawem: ``--oceń`` wypisuje całą krzywą,
#: bo zasięg kupuje się trafnością i odwrotnie. Te dwie stoją tam, gdzie świadek
#: odpowiada na jedno wyrażenie z ośmiu i myli się w co dziesiątej odpowiedzi,
#: a wybrano je dlatego, że warstwa niczego nie rozstrzyga za autora:
#: gdyby odpowiedź wchodziła do werdyktu, próg należałby wyżej.
WSPARCIE = 2
PRÓG = 0.85

#: Tabela skłonności: ``(przyimek, strona, lemat)`` → ``(w tę stronę, wszystkich)``.
Licznik = dict[tuple[str, str, str], tuple[int, int]]

#: Jeden wybór wzięty z banku drzew: przyimek, lemat rzeczownika, lemat czasownika
#: i strona, którą wybrał anotator. Tabela liczy się z tego i ocena mierzy na tym.
Wypadek = tuple[str, str, str, str]

#: Nazwy dwóch stron wyboru, tak jak nazywa je ``olski/attachment.py``.
RZECZOWNIK, CZASOWNIK = "noun", "clause"

#: Części mowy, po których poznaje się gospodarza czasownikowego.
CZASOWNIKOWE = frozenset(
    {"fin", "praet", "impt", "bedzie", "inf", "ppas", "pact", "winien", "imps", "pred"}
)


@dataclass(frozen=True)
class Rozstrzygnięcie:
    """Wskazanie gospodarza wraz z tym, co je wydało."""

    #: Formy modyfikatora, czyli to samo, czym nazywa go werdykt.
    modyfikator: str
    #: Głowa gospodarza, wybrana spośród :attr:`Przyłączenie.gospodarze`.
    gospodarz: str
    #: Dowód, jednym zdaniem, do postawienia w wydruku obok wskazania.
    powód: str
    #: Nazwa świadka, który odpowiedział. Wypełnia ją :func:`rozstrzygnij` z
    #: :attr:`Świadek.nazwa`, więc świadek nie ma jak podpisać się cudzym imieniem.
    świadek: str = ""


class Świadek(Protocol):
    """Jedno źródło dowodu nad jednym przyłączeniem."""

    nazwa: str

    def __call__(self, przyłączenie: Przyłączenie) -> Rozstrzygnięcie | None:
        """Wskazanie albo milczenie; milczenie jest odpowiedzią, a nie brakiem."""


def rozstrzygnij(
    przyłączenia: Iterable[Przyłączenie], świadkowie: Sequence[Świadek] | None = None
) -> list[Rozstrzygnięcie | Przyłączenie]:
    """Po jednej odpowiedzi na przyłączenie, w kolejności, w jakiej je podano.

    Przyłączenie, o którym nie wypowiedział się nikt, wraca takie, jakie weszło,
    a nie znika: warstwa ma powiedzieć, czego nie rozstrzygnęła, tak samo jak to,
    co rozstrzygnęła.
    """
    if świadkowie is None:
        świadkowie = domyślni()
    odpowiedzi: list[Rozstrzygnięcie | Przyłączenie] = []
    for przyłączenie in przyłączenia:
        odpowiedzi.append(_pierwszy(przyłączenie, świadkowie) or przyłączenie)
    return odpowiedzi


def _pierwszy(przyłączenie: Przyłączenie, świadkowie: Sequence[Świadek]) -> Rozstrzygnięcie | None:
    for świadek in świadkowie:
        odpowiedź = świadek(przyłączenie)
        if odpowiedź is not None:
            return replace(odpowiedź, świadek=świadek.nazwa)
    return None


def domyślni() -> list[Świadek]:
    """Świadkowie w kolejności rodzaju dowodu, od słownikowego do statystycznego."""
    return [Skłonność.z_pliku()]


# --------------------------------------------------------------------------- #
# Świadek statystyczny
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Skłonność:
    """Jak często para przyimka i gospodarza przyłączała się w banku drzew w tę stronę.

    Kluczem jest lemat, a nie forma, bo ``o gwieździe`` i ``o gwiazdach`` mówią
    o tej samej parze. Forma gospodarza ma jednak lematów kilka, a warstwa ta
    stoi za parserem, który lematu nie wybrał (``signature`` w ``olski/parse.py``),
    więc pytanie idzie o każdy lemat formy naraz i liczniki się sumują. Podnosi
    to wsparcie i rozmywa skłonność, a rozmycie kończy się milczeniem, czyli
    stroną bezpieczną.
    """

    #: ``(przyimek, strona, lemat)`` → ``(przyłączeń w tę stronę, wszystkich)``.
    licznik: Licznik
    nazwa: str = "skłonność"
    wsparcie: int = WSPARCIE
    próg: float = PRÓG

    @classmethod
    def z_pliku(cls, path: Path = SKŁONNOŚCI, **kwargs) -> Skłonność:
        return cls(licznik=czytaj(path), **kwargs)

    def __call__(self, przyłączenie: Przyłączenie) -> Rozstrzygnięcie | None:
        formy = przyłączenie.modyfikator.split()
        if not formy or len(przyłączenie.gospodarze) < 2:
            return None
        przyimek = formy[0].lower()
        kandydaci = [
            (gospodarz, CZASOWNIK if _czasownikowa(gospodarz) else RZECZOWNIK, _lematy(gospodarz))
            for gospodarz in przyłączenie.gospodarze
        ]
        wybrany = self.wybierz(przyimek, kandydaci)
        if wybrany is None:
            return None
        gospodarz, _, trafień, wszystkich = wybrany
        return Rozstrzygnięcie(
            modyfikator=przyłączenie.modyfikator,
            gospodarz=gospodarz,
            powód=(
                f"„{przyimek}” przy „{gospodarz}” doszło tam w {trafień} z {wszystkich} "
                f"wypadków banku drzew, {trafień / wszystkich:.0%}"
            ),
        )

    def wybierz(
        self, przyimek: str, kandydaci: Sequence[tuple[str, str, Iterable[str]]]
    ) -> tuple[str, str, int, int] | None:
        """Kandydat o najwyższej skłonności, albo ``None``, gdy żaden nie przechodzi progów.

        Jedno miejsce, w którym progi rozstrzygają, bo pytają o to dwie strony:
        werdykt, który ma formy gospodarzy, i ocena, która ma lematy z banku drzew.
        Druga kopia tej reguły kazałaby ocenie mierzyć innego świadka niż ten,
        którego wypuszcza ``olski-check``.

        Kandydat jest trójką ``(etykieta, strona, lematy)``, bo forma gospodarza
        ma lematów kilka, a warstwa ta stoi za parserem, który lematu nie wybrał
        (``signature`` w ``olski/parse.py``), więc liczniki sumują się po nich.
        Podnosi to wsparcie i rozmywa skłonność, a rozmycie kończy się milczeniem.
        """
        najlepszy = None
        for etykieta, strona, lematy in kandydaci:
            trafień, wszystkich = self._para(przyimek, strona, lematy)
            if wszystkich < self.wsparcie or trafień / wszystkich < self.próg:
                continue
            udział = trafień / wszystkich
            if najlepszy is None or udział > najlepszy[0]:
                najlepszy = (udział, etykieta, strona, trafień, wszystkich)
        return najlepszy[1:] if najlepszy else None

    def _para(self, przyimek: str, strona: str, lematy: Iterable[str]) -> tuple[int, int]:
        """Liczniki pary, zsumowane po podanych lematach."""
        trafień = wszystkich = 0
        for lemat in lematy:
            para = self.licznik.get((przyimek, strona, lemat))
            if para:
                trafień += para[0]
                wszystkich += para[1]
        return trafień, wszystkich


def _czytania(forma: str) -> list:
    """Czytania formy, ze wszystkich krawędzi grafu segmentacji, jakie ona ma.

    Gospodarz jest w werdykcie jedną formą, a Morfeusz dzieli niektóre formy na
    kilka segmentów, więc pytanie idzie o całość grafu, a nie o pierwszą krawędź.
    """
    return [reading for segment in analyse(forma) for reading in segment.readings]


def _lematy(forma: str) -> set[str]:
    return {reading.lemma.lower() for reading in _czytania(forma)} or {forma.lower()}


def _czasownikowa(forma: str) -> bool:
    return any(reading.tag.pos in CZASOWNIKOWE for reading in _czytania(forma))


# --------------------------------------------------------------------------- #
# Tabela: budowa, zapis, odczyt
# --------------------------------------------------------------------------- #

NAGŁÓWEK = """\
# Skłonności przyłączeniowe: jak często para przyimka i gospodarza przyłączała
# się w tę stronę. Kolumny to przyimek, strona (`noun` albo `clause`), lemat
# gospodarza, przyłączeń w tę stronę i przyłączeń wszystkich.
#
# Plik jest generowany i nie pisze się go ręcznie. Powstaje ze Składnicy przez
# `python3 -m olski.rozstrzyganie <korpus> --zbuduj`, a co z niej bierze, mówi
# `olski/attachment.py`. Wpisy o wsparciu poniżej progu tu nie wchodzą, bo
# świadek i tak by na nie nie patrzył.
#
# Bank drzew jest prozą literacką i prasową, a olski celuje w dokumentację
# techniczną, więc skłonność wzięta stąd jest punktem wyjścia, a nie pomiarem
# rejestru, o który chodzi.
"""


def wypadki(paths: Iterable[Path]) -> list[Wypadek]:
    """Wybory z banku drzew, po jednym na wyrażenie, przed którym wybór w ogóle stał.

    Populacją są wyrażenia przyimkowe stojące za grupą imienną i za czasownikiem,
    czyli ta sama, którą liczy ``olski/attachment.py``, zawężona do tych z oboma
    lematami. Import jest tutejszy, bo ``olski-check`` woła tę warstwę o werdykt
    i nie ma powodu wciągać przy tym czytnika banku drzew.
    """
    from olski.attachment import attachments
    from olski.corpus import read_forest

    zebrane = []
    for path in paths:
        for a in attachments(read_forest(path)):
            if not a.postverbal or a.host not in (RZECZOWNIK, CZASOWNIK):
                continue
            if a.prep and a.noun and a.verb:
                zebrane.append((a.prep, a.noun, a.verb, a.host))
    return zebrane


def zbuduj(wybory: Iterable[Wypadek], wsparcie: int = WSPARCIE) -> Licznik:
    """Policz pary nad wyborami z banku drzew i zostaw te, które przechodzą próg wsparcia.

    Bierze gotowe wybory, a nie ścieżki, bo ocena buduje tabelę z połowy tych
    samych wyborów, na których potem mierzy: dwa przejścia po korpusie
    rozeszłyby się na pierwszej zmianie w tym, co liczy się za wybór.
    """
    trafień: collections.Counter[tuple[str, str, str]] = collections.Counter()
    wszystkich: collections.Counter[tuple[str, str, str]] = collections.Counter()
    for przyimek, rzeczownik, czasownik, gospodarz in wybory:
        for strona, lemat in ((RZECZOWNIK, rzeczownik), (CZASOWNIK, czasownik)):
            wszystkich[(przyimek, strona, lemat)] += 1
            if gospodarz == strona:
                trafień[(przyimek, strona, lemat)] += 1
    return {klucz: (trafień[klucz], ile) for klucz, ile in wszystkich.items() if ile >= wsparcie}


def zapisz(licznik: Licznik, path: Path) -> None:
    wiersze = [
        f"{przyimek}\t{strona}\t{lemat}\t{trafień}\t{ile}"
        for (przyimek, strona, lemat), (trafień, ile) in sorted(licznik.items())
    ]
    path.write_text(NAGŁÓWEK + "\n".join(wiersze) + "\n", encoding="utf-8")


def czytaj(path: Path = SKŁONNOŚCI) -> Licznik:
    """Tabela z pliku; brak pliku znaczy świadka, który milczy zawsze."""
    if not path.exists():
        return {}
    licznik = {}
    for wiersz in path.read_text(encoding="utf-8").splitlines():
        if not wiersz or wiersz.startswith("#"):
            continue
        przyimek, strona, lemat, trafień, ile = wiersz.split("\t")
        licznik[(przyimek, strona, lemat)] = (int(trafień), int(ile))
    return licznik


# --------------------------------------------------------------------------- #
# Ocena
# --------------------------------------------------------------------------- #


@dataclass
class Ocena:
    """Ile świadek odpowiada i ile z tego trafia, na materiale, którego nie widział."""

    wypadków: int = 0
    odpowiedzi: int = 0
    trafień: int = 0

    @property
    def zasięg(self) -> float:
        return self.odpowiedzi / self.wypadków if self.wypadków else 0.0

    @property
    def trafność(self) -> float:
        return self.trafień / self.odpowiedzi if self.odpowiedzi else 0.0


#: Ustawienia, które ocena przechodzi, gdy nikt nie poda swoich. Krzywa, a nie
#: punkt, bo świadka tego rodzaju wybiera się właśnie na niej: zasięg kupuje się
#: trafnością i odwrotnie, a która para jest do przyjęcia, rozstrzyga to, co
#: warstwa ma robić z odpowiedzią.
KRZYWA = ((2, 0.70), (2, 0.85), (3, 0.85), (5, 0.85), (5, 0.95))


def oceń(
    paths: Sequence[Path], krzywa: Sequence[tuple[int, float]] = KRZYWA
) -> tuple[list[tuple[int, float, Ocena]], Ocena]:
    """Zbuduj tabelę na połowie banku drzew i sprawdź ją na drugiej.

    Podział idzie po parzystości numeru pliku, a nie losowaniem, żeby ta sama
    komenda dwa razy dała tę samą liczbę. Obie połowy czyta się raz, a ustawienia
    przechodzi się po gotowych czwórkach, bo czytanie lasów jest tu całym kosztem.

    Wraca krzywa świadka i ocena podłogi, czyli tego samego pomiaru dla reguły
    „zawsze do rzeczownika”: świadek, który podłogi nie pobija, nie kupuje
    niczego, bo nad tym korpusem rzeczownik bierze dwie trzecie wyborów
    (``docs/subset.md``).
    """
    najniższe = min(wsparcie for wsparcie, _ in krzywa)
    licznik = zbuduj(wypadki(paths[::2]), najniższe)
    testowe = wypadki(paths[1::2])

    podłoga = Ocena(wypadków=len(testowe), odpowiedzi=len(testowe))
    podłoga.trafień = sum(gospodarz == RZECZOWNIK for *_, gospodarz in testowe)

    krzywe = []
    for wsparcie, próg in krzywa:
        świadek = Skłonność(licznik=licznik, wsparcie=wsparcie, próg=próg)
        ocena = Ocena(wypadków=len(testowe))
        for przyimek, rzeczownik, czasownik, gospodarz in testowe:
            #  Lematy idą tu wprost z banku drzew, a nie przez Morfeusza, bo
            #  anotator wybrał po jednym na formę. Ile wieloznaczność lematu
            #  dokłada świadkowi nad żywym tekstem, jest osobnym pytaniem.
            kandydaci = [
                (RZECZOWNIK, RZECZOWNIK, [rzeczownik]),
                (CZASOWNIK, CZASOWNIK, [czasownik]),
            ]
            wybrany = świadek.wybierz(przyimek, kandydaci)
            if wybrany is None:
                continue
            ocena.odpowiedzi += 1
            ocena.trafień += wybrany[0] == gospodarz
        krzywe.append((wsparcie, próg, ocena))
    return krzywe, podłoga


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m olski.rozstrzyganie",
        description="Zbuduj albo oceń tabelę skłonności przyłączeniowych.",
    )
    parser.add_argument("root", help="katalog z rozpakowaną Składnicą")
    parser.add_argument("--zbuduj", type=Path, nargs="?", const=SKŁONNOŚCI, help="zapisz tabelę")
    parser.add_argument("--oceń", action="store_true", help="sprawdź świadka na drugiej połowie")
    parser.add_argument("--limit", type=int, help="zatrzymaj się po tylu lasach")
    parser.add_argument(
        "--wsparcie",
        type=int,
        default=WSPARCIE,
        help="ile wystąpień minimum trafia do budowanej tabeli; oceny nie rusza",
    )
    args = parser.parse_args(argv)

    from olski.corpus import pliki

    root = Path(args.root)
    if not root.is_dir():
        print(f"olski.rozstrzyganie: nie ma takiego katalogu: {root}", file=sys.stderr)
        print("olski.rozstrzyganie: skąd wziąć korpus, mówi docs/corpus.md", file=sys.stderr)
        return 2
    ścieżki = pliki(root)[: args.limit]
    if args.zbuduj:
        licznik = zbuduj(wypadki(ścieżki), args.wsparcie)
        zapisz(licznik, args.zbuduj)
        print(f"{len(licznik)} par o wsparciu co najmniej {args.wsparcie} → {args.zbuduj}")
    if args.oceń or not args.zbuduj:
        krzywe, podłoga = oceń(ścieżki)
        print(f"ocena na połowie, której świadek nie widział: {podłoga.wypadków} wyborów")
        print(f"  podłoga: zawsze do rzeczownika, trafia w {podłoga.trafność:.1%}")
        for wsparcie, próg, ocena in krzywe:
            print(
                f"  wsparcie {wsparcie}, próg {próg:.0%}: "
                f"odpowiada w {ocena.zasięg:>5.1%}, trafia w {ocena.trafność:>5.1%}"
            )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
