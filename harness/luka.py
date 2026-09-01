"""Co kupuje i co kosztuje luka, czyli szczebel 2 drabiny kosztów.

Zdanie względne stoi w gramatyce wypisane rolą po roli: kilkadziesiąt ciał
``rdzeń_względny``, po jednym na czoło razy wysunięta rola razy szyk reszty zdania
razy miejsce na okolicznik razy przeczenie. Wyjęcia z głębi — ``ustawa, którą
organ gminy może wydać`` — nie ma tam wcale, bo dopełnienie dochodzi tylko do
formy osobowej.

Odpowiedzią drabiny jest cecha przeciągana, czyli szczebel 2: konstytuent niesie
w cechach to, czego mu w środku brakuje, luka jest produkcją o pustym ciele, a
zdanie względne wiąże ją ze swoim zaimkiem. Zdanie względne dostaje wtedy każdy
szyk i każde miejsce na okolicznik, jakie ma zdanie zwykłe, wraz z wyjęciem z
głębi, a wypisać trzeba samo przeciąganie.

Warianty są dwa, bo pomiarem jest różnica między nimi. Luka nie ma napisu, więc
szyk nią nie przestawia niczego: ciało, które stawia ją gdzie indziej, wydaje ten
sam napis drugim kształtem. ``luka wszędzie`` ma ją w każdej pozycji, jaką ma jej
rola, i traci przez to jednoznaczność każdego zdania względnego; ``luka
kanoniczna`` dokłada warunek precedencji na samą lukę i jednoznaczność odzyskuje.

Werdykt tego pomiaru wraz z trzecią ceną, której żaden z dwóch wariantów nie
zdejmuje, czyta ``docs/design-notes.md``.

    python3 -m harness.luka Składnica-frazowa-180723/
    python3 -m harness.luka proza/README.txt
    python3 -m harness.luka -c "Reguła, która rozstrzyga, jest tania."
"""

from __future__ import annotations

import argparse
import collections
import functools
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.corpus import Sentence, read
from harness.komenda import Komenda, nagłówek, uruchom
from harness.pomiar import Outcome, po_kawałkach
from olski.grammar import Grammar, Production, Sym, Var, nt
from olski.parse import parse
from olski.subset import BEZ_CZOŁA, build
from olski.werdykt import check

#: Cecha niosąca przypadek luki, czyli to, czego temu konstytuentowi w środku
#: brakuje. ``brak`` stoi wypisany, a nie pominięty: cechy, której konstytuent
#: nie niesie, rodzic nie sprawdza, więc luka pominięta przechodziłaby wszędzie.
LUKA = "luka"
#: Liczba i rodzaj luki, czyli reszta kategorii, którą zaimek ma podjąć. Idą
#: osobno od przypadka, bo przypadka żąda pozycja, a te dwie cechy poprzednik.
LUKA_N = "luka_number"
LUKA_G = "luka_gender"
BRAK = frozenset({"brak"})

#: Symbole, pod którymi luka staje, czyli te, które dostają produkcję pustą.
#: Jest to cała decyzja tej sondy o tym, gdzie luki wolno szukać.
PUSTE = ("podmiot", "dopełnienie")
#: Symbole, które lukę domykają, wiążąc ją ze swoim zaimkiem. Wyżej luka nie idzie,
#: i dlatego wyjęcie z wnętrza zdania względnego nie wyprowadza się wcale.
#: Rodzin względnych jest dwie, bo dwa poprzedniki biorą dwa czoła
#: (``zaimek_względny_rzeczowny`` w ``olski/subset/podrzędne.py``), a domyka luki obie tak samo.
DOMYKA = ("rdzeń_względny", "rdzeń_względny_rzeczowny")
#: Rodzina, której ciała luka zastępuje, czyli zasięg tej sondy. Węższa od
#: :data:`DOMYKA` i tym zaniża pomiar, bo zdanie z `co` na czole wychodzi w
#: wariancie odrzucone tak samo jak bez luki; todo/ trzyma ten brak.
ZASTĘPOWANE = ("rdzeń_względny",)
#: Symbol, pod którym luki stanąć nie wolno, bo jest korzeniem: zdanie z luką
#: niedomkniętą zdaniem nie jest.
KORZEŃ = "wypowiedzenie"

WARIANTY = ("olski", "luka wszędzie", "luka kanoniczna")

#: Ile zdań pokazać przy przejściu. Przejście bez przykładu jest liczbą, o której
#: nie wiadomo, co ją wywołało, a cena jest tu tym, co trzeba przeczytać.
PRZYKŁADY = 6

STANY = ("valid", "ambiguous", "rejected")


# --------------------------------------------------------------------------- #
# Wariant
# --------------------------------------------------------------------------- #


def niosące(grammar: Grammar) -> frozenset[str]:
    """Symbole, przez które luka przechodzi, wyliczone z gramatyki, a nie wypisane.

    Luka idzie w górę od miejsca, w którym stanęła, do symbolu, który ją domyka,
    więc unosi ją każdy symbol między jednym a drugim. Domknięcie liczy się z
    produkcji, bo lista wypisana ręcznie starzeje się bez śladu: symbol dopisany
    do zdania nie dostałby przeciągania, sonda mierzyłaby wariant węższy, niż
    mówi, i nie powiedziałaby o tym ani słowem.

    Zamknięcie zatrzymuje się na :data:`DOMYKA` i na korzeniu, i to jest jedyny
    powód, dla którego nie obejmuje ono grupy imiennej: grupa unosi zdanie
    względne, a zdanie względne lukę domyka.
    """
    unoszą = set(PUSTE)
    rośnie = True
    while rośnie:
        rośnie = False
        for produkcja in grammar.productions:
            if produkcja.head in unoszą or produkcja.head in DOMYKA + (KORZEŃ,):
                continue
            if any(isinstance(część, Sym) and część.name in unoszą for część in produkcja.body):
                unoszą.add(produkcja.head)
                rośnie = True
    return frozenset(unoszą)


def _z_cechami(część: Sym, **cechy) -> Sym:
    razem = {**dict(część.constraints), **cechy}
    return Sym(name=część.name, constraints=tuple(sorted(razem.items())))


def _zmienna(część: Sym, nazwa: str) -> Var | None:
    """Zmienna, jaką ta córka wiąże na tej cesze; ``None``, gdy żadnej."""
    for imię, spec in część.constraints:
        if imię == nazwa and isinstance(spec, Var):
            return spec
    return None


def _wiązka(część: Sym, i: int) -> dict[str, Var]:
    """Cechy, którymi ta córka wypuszcza swoją lukę do rodzica.

    Przypadek idzie zawsze. Liczba i rodzaj idą stamtąd, skąd pochodzą: przy
    podmiocie z jego zgodności z orzeczeniem, bo z luką podmiotową orzeczenie się
    zgadza; przy dopełnieniu z niczego, bo dopełnienie liczby ani rodzaju z resztą
    zdania nie dzieli i rozstrzyga o nich sam zaimek; a przy symbolu, który lukę
    tylko unosi, przelotem, bo on je już niesie.
    """
    wiązka: dict[str, Var] = {LUKA: Var(f"luka{i}")}
    if część.name == "podmiot":
        for cecha, nazwa in ((LUKA_N, "number"), (LUKA_G, "gender")):
            zmienna = _zmienna(część, nazwa)
            if zmienna is not None:
                wiązka[cecha] = zmienna
    elif część.name != "dopełnienie":
        wiązka[LUKA_N] = Var(f"lukan{i}")
        wiązka[LUKA_G] = Var(f"lukag{i}")
    return wiązka


def _kanoniczna(produkcja: Production, i: int) -> bool:
    """Czy luka stoi w tej córce na pozycji, jaką ta rola zajmuje kanonicznie.

    Podmiot stoi na czele, bo tam go stawia zdanie względne. Dopełnienie stoi
    tuż za czasownikiem, który je rządzi, czyli albo pod symbolem ``wypełnienia``,
    albo w ciele, w którym idzie zaraz za ``orzeczenie``.
    """
    część = produkcja.body[i]
    if część.name == "podmiot":
        return i == 0
    if część.name == "dopełnienie":
        if produkcja.head == "wypełnienia":
            return True
        poprzednia = produkcja.body[i - 1] if i else None
        return isinstance(poprzednia, Sym) and poprzednia.name == "orzeczenie"
    return True


def _wysunięty_okolicznik(produkcja: Production) -> bool:
    """Czy to ciało zdania względnego wysuwa wyrażenie przyimkowe, a nie sam zaimek.

    Takie ciało zostaje w wariancie nieruszone, bo okolicznik jest wolny i luki
    pod sobą nie żąda: za wysuniętym wyrażeniem następuje zdanie składowe całe.
    """
    return any(
        isinstance(część, Sym) and część.name == "wyrażenie_przyimkowe_względne"
        for część in produkcja.body
    )


def _przepisz(produkcja: Production, luka: int | None, niosące: frozenset[str]) -> Production:
    """Ta produkcja z luką w tej córce, albo bez luki wcale.

    Córka nieoznaczona dostaje ``luka=brak``, więc luk w ciele jest najwyżej
    jedna: cecha przeciągana nie jest zgodnością i przez rodzeństwo nie
    przechodzi. Tym samym ``brak`` przypina lukę symbol, który jej nie unosi, i
    stąd bierze się to, że luka nie ucieka poza zdanie, w którym jej szukano.
    """
    ciało = list(produkcja.body)
    cechy = dict(produkcja.features)
    wiązka = {LUKA: BRAK} if luka is None else _wiązka(ciało[luka], luka)
    for i, część in enumerate(ciało):
        if isinstance(część, Sym) and część.name in niosące:
            ciało[i] = _z_cechami(część, **(wiązka if i == luka else {LUKA: BRAK}))
    if produkcja.head in niosące:
        cechy.update(wiązka)
    return Production(
        head=produkcja.head,
        body=tuple(ciało),
        features=frozenset(cechy.items()),
        głowa=produkcja.głowa,
    )


@functools.cache
def gramatyka(wariant: str) -> Grammar:
    """Gramatyka tego wariantu; ``olski`` jest tą, która stoi.

    Budowana raz na proces roboczy, bo budowa jest droższa niż rozbiór jednego
    zdania, a gramatyka po zbudowaniu się nie zmienia.
    """
    if wariant not in WARIANTY:
        raise ValueError(f"nieznany wariant: {wariant}")
    pełna = build()
    if wariant == "olski":
        return pełna
    kanonicznie = wariant == "luka kanoniczna"
    unoszą = niosące(pełna)
    wariantowa = Grammar(start=pełna.start)
    for produkcja in pełna.productions:
        # Zdanie względne wypisane rolą po roli jest tym, co luka zastępuje, więc
        # z wariantu wychodzi. Zostaje ciało z wysuniętym wyrażeniem
        # przyimkowym, bo okolicznik jest wolny i luki nie potrzebuje.
        if produkcja.head in ZASTĘPOWANE and not _wysunięty_okolicznik(produkcja):
            continue
        wariantowa.dopisz(_przepisz(produkcja, None, unoszą))
        if produkcja.head not in unoszą:
            continue
        for i, część in enumerate(produkcja.body):
            if not isinstance(część, Sym) or część.name not in unoszą:
                continue
            if kanonicznie and not _kanoniczna(produkcja, i):
                continue
            wariantowa.dopisz(_przepisz(produkcja, i, unoszą))

    # Luka sama: produkcja o pustym ciele, niosąca przypadek, jakiego pozycja
    # żąda. Dopełnienie ma dwie, bo dopełniacz negacji jest tą samą pozycją przy
    # czasowniku przeczącym, a samo przeczenie niesie już cecha, która stoi.
    #
    # Wypisane jest przy tym `czoło`, choć luka staje tylko na swoim miejscu:
    # ten wariant zdejmuje ciała, które czoła żądają (:data:`DOMYKA`), a cecha
    # pominięta wpuściłaby lukę pod każde takie ciało, które kiedyś zostanie —
    # cechy, której konstytuent nie niesie, rodzic nie sprawdza, tak samo jak
    # przy :data:`LUKA` wyżej.
    bez_czoła = ("czoło", frozenset({BEZ_CZOŁA}))
    wariantowa.dopisz(
        Production(
            head="podmiot",
            body=(),
            features=frozenset({(LUKA, frozenset({"nom"})), bez_czoła}),
        )
    )
    for przypadek, negacja in (("acc", "aff"), ("gen", "neg")):
        wariantowa.dopisz(
            Production(
                head="dopełnienie",
                body=(),
                features=frozenset(
                    {
                        (LUKA, frozenset({przypadek})),
                        ("valency", frozenset({"acc"})),
                        ("negacja", frozenset({negacja})),
                        bez_czoła,
                    }
                ),
            )
        )

    # Zdanie względne: zaimek i zdanie, któremu brakuje dokładnie tego, czym on
    # jest. Jedna produkcja w miejsce piętnastu ciał.
    wariantowa.dopisz(
        Production(
            head="rdzeń_względny",
            body=(
                nt("zaimek_względny", case=Var("c"), number=Var("n"), gender=Var("g")),
                nt("zdanie_składowe", **{LUKA: Var("c"), LUKA_N: Var("n"), LUKA_G: Var("g")}),
            ),
            features=frozenset({("number", Var("n")), ("gender", Var("g"))}),
            głowa=1,
        )
    )
    return wariantowa


# --------------------------------------------------------------------------- #
# Przebieg
# --------------------------------------------------------------------------- #


@dataclass
class Raport:
    """Liczniki jednego przebiegu, wraz ze zdaniami, które je czynią czytelnymi."""

    ile_przykładów: int = PRZYKŁADY
    stany: dict[str, collections.Counter] = field(default_factory=dict)
    przejścia: dict[str, collections.Counter] = field(default_factory=dict)
    przykłady: dict[tuple[str, str], list[str]] = field(default_factory=dict)
    #: Wariant → jak role zdań nowo przyjętych mają się do drzewa wzorcowego.
    #: Zdanie przyjęte odwrotnie niż w banku drzew nie jest zakupem, i po to ten
    #: licznik tu stoi: na nim stanął ten pomiar.
    zgodność: dict[str, collections.Counter] = field(default_factory=dict)
    pominięte: collections.Counter = field(default_factory=collections.Counter)

    @property
    def zmierzone(self) -> int:
        return sum(self.stany.get(WARIANTY[0], collections.Counter()).values())

    def zapisz(self, tekst: str, stany: dict[str, str], role: dict[str, str | None]) -> None:
        mianownik = stany[WARIANTY[0]]
        for wariant, stan in stany.items():
            self.stany.setdefault(wariant, collections.Counter())[stan] += 1
            if wariant == WARIANTY[0] or stan == mianownik:
                continue
            przejście = f"{mianownik} → {stan}"
            self.przejścia.setdefault(wariant, collections.Counter())[przejście] += 1
            self.zanotuj((wariant, przejście), tekst)
            if stan == "valid":
                zgoda = role.get(wariant) or "brak roli"
                self.zgodność.setdefault(wariant, collections.Counter())[zgoda] += 1

    def zanotuj(self, klucz: tuple[str, str], tekst: str) -> None:
        zachowane = self.przykłady.setdefault(klucz, [])
        if len(zachowane) < self.ile_przykładów:
            zachowane.append(tekst)


def zmierz(zdania: Iterable[Sentence], przykłady: int = PRZYKŁADY) -> Raport:
    """Przepuść zdania banku drzew przez każdy wariant i policz, co się rusza.

    Populacja jest ta sama, co w ``harness.pomiar.measure``: każde zdanie z
    drzewem wzorcowym, bez granicy na długość.
    """
    raport = Raport(przykłady)
    for zdanie in zdania:
        if not zdanie.annotated:
            continue
        segmenty = list(zdanie.segments)
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        wyniki = {
            wariant: Outcome(
                sentence=zdanie,
                result=parse(gramatyka(wariant), segmenty, zatrzymanie=False),
                segments=tuple(segmenty),
            )
            for wariant in WARIANTY
        }
        raport.zapisz(
            zdanie.text,
            {wariant: wynik.status for wariant, wynik in wyniki.items()},
            {wariant: wynik.agreement for wariant, wynik in wyniki.items()},
        )
    return raport


def nad_prozą(tekst: str, przykłady: int = PRZYKŁADY) -> Raport:
    """To samo porównanie nad prozą, którą olski ma czytać.

    Ról nie ma czym porównać, bo drzewa wzorcowego proza nie niesie, a fragment
    nie jest zdaniem i do mianownika nie wchodzi.
    """
    raport = Raport(przykłady)
    wyniki = {wariant: check(tekst, gramatyka(wariant)) for wariant in WARIANTY}
    for kolejne in zip(*wyniki.values(), strict=True):
        werdykty = dict(zip(WARIANTY, kolejne, strict=True))
        if not werdykty[WARIANTY[0]].punktowane:
            raport.pominięte["fragment, a nie zdanie"] += 1
            continue
        raport.zapisz(
            werdykty[WARIANTY[0]].text,
            {wariant: werdykt.status for wariant, werdykt in werdykty.items()},
            {},
        )
    return raport


def _kawałek(ścieżki: Sequence[Path], przykłady: int) -> Raport:
    return zmierz((read(ścieżka) for ścieżka in ścieżki), przykłady)


def scal(raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    scalony = Raport(przykłady)
    for raport in raporty:
        for pole in ("stany", "przejścia", "zgodność"):
            for wariant, licznik in getattr(raport, pole).items():
                getattr(scalony, pole).setdefault(wariant, collections.Counter()).update(licznik)
        scalony.pominięte.update(raport.pominięte)
        for klucz, zachowane in raport.przykłady.items():
            for tekst in zachowane:
                scalony.zanotuj(klucz, tekst)
    return scalony


def przebieg(ścieżki: Sequence[Path], jobs: int, przykłady: int = PRZYKŁADY) -> Raport:
    praca = functools.partial(_kawałek, przykłady=przykłady)
    return scal(po_kawałkach(ścieżki, jobs, praca), przykłady)


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(raport: Raport, nagłówek: str) -> str:
    szerokość = max(len(wariant) for wariant in WARIANTY)
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań",
        "",
        f"{'wariant':>{szerokość}}  {'produkcji':>9} {'przyjęte':>9}"
        f" {'wieloznaczne':>13} {'odrzucone':>10}",
    ]
    for wariant in WARIANTY:
        licznik = raport.stany.get(wariant, collections.Counter())
        przyjęte, wieloznaczne, odrzucone = (licznik.get(stan, 0) for stan in STANY)
        wiersze.append(
            f"{wariant:>{szerokość}}  {len(gramatyka(wariant)):>9} {przyjęte:>9}"
            f" {wieloznaczne:>13} {odrzucone:>10}"
        )
    for powód, ile in raport.pominięte.most_common():
        wiersze.append(f"{ile:>7}          niezmierzone: {powód}")

    for wariant in WARIANTY[1:]:
        wiersze += ["", f"ruch wobec wariantu „{WARIANTY[0]}” — {wariant}:"]
        przejścia = raport.przejścia.get(wariant, collections.Counter())
        if not przejścia:
            wiersze.append("  żadne zdanie nie zmieniło werdyktu")
        for przejście, ile in przejścia.most_common():
            wiersze.append(f"  {ile:>7}  {przejście}")
        zgodność = raport.zgodność.get(wariant)
        if zgodność:
            wiersze.append("  role zdań nowo przyjętych wobec drzewa wzorcowego:")
            for nazwa, ile in zgodność.most_common():
                wiersze.append(f"  {ile:>7}    {nazwa}")

    for wariant in WARIANTY[1:]:
        for przejście, _ in raport.przejścia.get(wariant, collections.Counter()).most_common():
            zachowane = raport.przykłady.get((wariant, przejście), [])
            if zachowane:
                wiersze += ["", f"{wariant}, {przejście}:"]
                wiersze += [f"  {tekst}" for tekst in zachowane]
    return "\n".join(wiersze)


def wydruk_zdań(tekst: str) -> str:
    """Werdykt każdego wariantu nad podanymi zdaniami, po jednym wierszu na zdanie.

    Po to, żeby cena i zakup dały się przeczytać na zdaniu, a nie tylko policzyć
    nad korpusem: nad Składnicą luka rusza kilka zdań, a minimalna para pokazuje,
    czym rusza.
    """
    wyniki = {wariant: check(tekst, gramatyka(wariant)) for wariant in WARIANTY}
    wiersze = []
    for kolejne in zip(*wyniki.values(), strict=True):
        werdykty = dict(zip(WARIANTY, kolejne, strict=True))
        opis = "  ".join(
            f"{wariant}: {werdykt.status} ({werdykt.result.ile})"
            for wariant, werdykt in werdykty.items()
        )
        wiersze.append(f"{werdykty[WARIANTY[0]].text}\n  {opis}")
    return "\n".join(wiersze)


def _korpus(ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    return wydruk(przebieg(ścieżki, args.jobs, args.przykłady), "Składnica, morfologia złota")


def _proza(wejścia: Sequence[tuple[Path, str]], args: argparse.Namespace) -> str:
    raporty = (nad_prozą(tekst, args.przykłady) for _, tekst in wejścia)
    return wydruk(scal(raporty, args.przykłady), f"{nagłówek(wejścia)}, proza")


KOMENDA = Komenda(
    nazwa="harness.luka",
    opis="co kupuje i co kosztuje luka w zdaniu względnym",
    przykłady=PRZYKŁADY,
    korpus=_korpus,
    proza=_proza,
    zdania=wydruk_zdań,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(uruchom(KOMENDA))
