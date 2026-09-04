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

from harness import ruch
from olski.grammar import Grammar, Production, Sym, Var, nt
from olski.subset import BEZ_CZOŁA, build

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
#: wariancie odrzucone tak samo jak bez luki.
ZASTĘPOWANE = ("rdzeń_względny",)
#: Symbol, pod którym luki stanąć nie wolno, bo jest korzeniem: zdanie z luką
#: niedomkniętą zdaniem nie jest.
KORZEŃ = "wypowiedzenie"

WARIANTY = ("olski", "luka wszędzie", "luka kanoniczna")


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


def przeciąganie(wariant: str) -> Grammar:
    """Gramatyka tego wariantu; ``olski`` jest tą, która stoi.

    Tę funkcję woła ``gramatyka`` w ``harness/ruch.py``, więc nazwa wariantu jest
    tam sprawdzona, a gramatyka budowana raz na proces roboczy.

    Funkcją, a nie domknięciem: przebieg posyła sondę do procesu roboczego
    (:class:`ruch.Zdejmowanie` mówi, co to kosztuje).
    """
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
# Sonda
# --------------------------------------------------------------------------- #


#: Deklaracja różnicowa luki. Przebieg, tabelę przejść i wiersz poleceń bierze z
#: ``harness/ruch.py``, bo różni ją od sond obok to, jaką gramatykę składa każdy
#: wariant, a nie to, co się nad tymi wariantami liczy.
#:
#: Wariantu najszerszego nie ma tu żadnego i stąd ``None``
#: w :attr:`ruch.Sonda.najszerszy`.
#: Luka staje pod podmiotem i dopełnieniem (:data:`PUSTE`), a zdejmowane są całe
#: ciała ``rdzeń_względny``, więc bez zastąpienia zostają te, które wysuwają
#: orzecznik, oraz te, które wysuwają grupę z zaimkiem, a nie sam zaimek.
#: Olski wyprowadza przez to zdania, których wariant z luką nie wyprowadza —
#: ``Reguła, której koszt ktoś zna, jest tania.`` — a co by z takiego wariantu
#: wzięło pominięcie rozbiorów, mówi :func:`ruch._bez_zbędnych`.
LUKA_SONDA = ruch.Sonda(
    nazwa="harness.luka",
    opis="co kupuje i co kosztuje luka w zdaniu względnym",
    warianty=WARIANTY,
    gramatyki=przeciąganie,
)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(ruch.main(LUKA_SONDA))
