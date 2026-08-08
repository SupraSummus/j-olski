"""Podłoże więzowe: łuk jest deklaracją, a rozbiór drzewem zależności.

Produkcja mówi, z czego składa się konstytuent, i przez to mówi naraz trzy
rzeczy: co się z czym zgadza, w jakim stoi porządku i że wychodzi z tego jeden
spójny odcinek tekstu. Tutaj te trzy rzeczy są rozdzielone. Zgodność jest
warunkiem na parę słów, porządek osobnym polem tej samej deklaracji, a spójność
jednym więzem globalnym, który wolno zdjąć.

Co z tego rozdzielenia wyszło nad prozą README, wraz z ceną i z tym, czego to
podłoże nie umie, trzyma `docs/design-notes.md`, i tam stoi polecenie, które te
liczby powtarza. Tutaj jest sam mechanizm.

Cechy, unifikacja i słownik są tu olskiego, a nie własne. Żądanie na słowo jest
`Word` z `olski/grammar.py`, zgodność między głową a zależnym robi wspólna
zmienna przepuszczona przez `unify`, a segmenty przychodzą z
`olski/subset.py`. Porównanie mierzy więc podłoże, bo warstwa morfologiczna w obu
programach jest jedna i ta sama.
"""

from __future__ import annotations

from dataclasses import dataclass

from olski.grammar import EMPTY, Word, unify
from olski.morph import Reading, Segment

#: Głowa łuku, którego nie ma: korzeń zdania.
KORZEŃ = -1

#: Po której stronie głowy wolno stać zależnemu. ``OBIE`` jest domyślne, bo szyk
#: swobodny jest w polszczyźnie regułą, a nie wyjątkiem, i deklaracja, która o
#: porządku nie mówi nic, jest tu deklaracją słabszą, a nie niedokończoną.
PRZED, PO, OBIE = "przed", "po", "obie"


@dataclass(frozen=True)
class Więz:
    """Jeden łuk, który wolno postawić.

    Zgodność biorą wspólne zmienne cech: ``głowa`` i ``zależny`` unifikują się w
    jednym środowisku, więc jedna zmienna liczby postawiona po obu stronach żąda
    tej samej liczby, a jedna zmienna przypadku na przyimku i na rzeczowniku jest
    rządem.
    """

    etykieta: str
    głowa: Word
    zależny: Word
    strona: str = OBIE
    #: Czy zależny musi przylegać do głowy. ``się`` po swoim czasowniku przylega,
    #: a podmiot do orzeczenia nie.
    przyległy: bool = False
    #: Czy głowa bierze najwyżej jeden taki łuk. Podmiot tak, okolicznik nie.
    jedyny: bool = True
    #: Etykiety, które ta sama głowa musi wyprowadzić, żeby ten łuk był dozwolony.
    #: Tędy wchodzi wykluczenie, które gramatyka bezkontekstowa robi brakiem
    #: produkcji: dopełnienie przed czasownikiem żąda podmiotu, bo bez podmiotu
    #: jest polszczyzną przez jego opuszczenie, którego olski nie ma.
    wymaga: tuple[str, ...] = ()
    #: Etykiety, których ta sama głowa wyprowadzić nie może. Walencja w wersji
    #: najsłabszej, jaka do porównania wystarcza: czasownik nie bierze naraz
    #: dopełnienia i orzecznika.
    zakazuje: tuple[str, ...] = ()


@dataclass(frozen=True)
class Zgoda:
    """Zgodność między dwoma łukami jednej głowy.

    Orzecznik zgadza się z podmiotem w liczbie i w rodzaju,
    a nie z czasownikiem, który ich łączy:
    forma osobowa rodzaju nie niesie, więc przez nią ta zgodność nie przechodzi.
    Produkcja ma to za darmo, bo podmiot i orzecznik stoją w niej pod jedną matką
    i wolno im dzielić zmienną.
    """

    pierwszy: str
    drugi: str
    cechy: tuple[str, ...]


@dataclass(frozen=True)
class Żąda:
    """Łuki, które słowo musi wyprowadzić, żeby wolno je było postawić.

    Bez tego przyimek bez swojej grupy imiennej jest poprawnym okolicznikiem: łuk
    mówi, co wolno dołączyć, i nic w nim nie mówi, czego brakować nie może.
    """

    słowo: Word
    etykiety: tuple[str, ...]


@dataclass(frozen=True)
class Gramatyka:
    """Żądanie na korzeń i wszystkie łuki, jakie wolno postawić."""

    korzeń: Word
    więzy: tuple[Więz, ...]
    zgody: tuple[Zgoda, ...] = ()
    żądania: tuple[Żąda, ...] = ()
    #: Słowo, którym zdanie się zamyka i które do drzewa nie wchodzi, tak jak
    #: kropka nie jest konstytuentem w ``Sentence → Clause interp`` olskiego.
    #: Zależnym być nie może: w zdaniu o dwóch formach osobowych czepiałaby się
    #: każdej z nich po kolei i zdanie wychodziłoby wieloznaczne od interpunkcji.
    domknięcie: Word | None = None


@dataclass(frozen=True)
class Czytanie:
    """Jeden rozbiór: drzewo zależności nad wybranymi czytaniami form.

    Tożsamość czytania trzyma :meth:`sygnatura` i jest to ta sama decyzja, którą
    ``signature`` podejmuje w ``olski/parse.py``: liczy się kształt i część mowy
    każdego słowa, a nie wartości cech ani lematy. Dwa modele różniące się
    przypadkiem, który unifikacja i tak uzgodniła, są jednym czytaniem.
    """

    formy: tuple[str, ...]
    części: tuple[str, ...]
    łuki: tuple[tuple[int, int, str], ...]

    def sygnatura(self):
        return self.części, frozenset(self.łuki)

    def poddrzewo(self, wierzchołek: int) -> tuple[int, ...]:
        """Słowa, które pod tym wierzchołkiem stoją, wraz z nim samym."""
        zebrane = {wierzchołek}
        rosło = True
        while rosło:
            rosło = False
            for dziecko, głowa, _ in self.łuki:
                if głowa in zebrane and dziecko not in zebrane:
                    zebrane.add(dziecko)
                    rosło = True
        return tuple(sorted(zebrane))

    def rola(self, etykieta: str) -> str | None:
        """Co wypełnia tę rolę, jako napis, jeśli da się go zbudować.

        Fraza nieciągła napisem nie jest, i to jest miejsce, w którym raport
        płaci za zdjęcie spójności. Zwracany jest wtedy zapis z przerwą, żeby
        czytelnik zobaczył, że słowa nie stoją obok siebie.
        """
        for dziecko, _, etykieta_łuku in self.łuki:
            if etykieta_łuku != etykieta:
                continue
            słowa = self.poddrzewo(dziecko)
            napis = " ".join(self.formy[i] for i in słowa)
            ciągłe = słowa == tuple(range(słowa[0], słowa[-1] + 1))
            return napis if ciągłe else f"{napis} (nieciągłe)"
        return None


@dataclass
class Rozbiór:
    """Co podłoże powiedziało o jednym zdaniu."""

    czytania: list[Czytanie]
    urwane: bool = False
    #: Słowa, którym przycinanie zabrało wszystkie czytania. Odrzucenie mówi
    #: wtedy, na czym stanęło, czego werdykt olskiego nie mówi wcale.
    bez_głowy: tuple[str, ...] = ()

    @property
    def status(self) -> str:
        if len(self.czytania) == 1:
            return "valid"
        return "ambiguous" if self.czytania else "rejected"


def rozbierz(
    segmenty: list[Segment],
    gramatyka: Gramatyka,
    limit: int = 2,
    spójne: bool = True,
) -> Rozbiór:
    """Czytania zdania, najwyżej ``limit`` różnych.

    ``limit=2`` wystarcza do werdyktu, bo pytanie jest o to, czy czytanie jest
    jedno. Wyższy limit stoi tu do porównywania liczb, a nie do wydania werdyktu.

    ``spójne=False`` zdejmuje projektywność, czyli wpuszcza konstytuent nieciągły.
    """
    słowa = _ścieżka(segmenty)
    if słowa is None:
        return Rozbiór(czytania=[])
    if gramatyka.domknięcie is not None:
        if not słowa or not _którekolwiek(gramatyka.domknięcie, słowa[-1]):
            return Rozbiór(czytania=[])
        słowa = słowa[:-1]
    formy = tuple(segment.form for segment in słowa)
    czytania_form = [segment.readings for segment in słowa]

    tablica = _tablica(czytania_form, gramatyka)
    dziedziny = _dziedziny(tablica)
    puste = tuple(forma for forma, dziedzina in zip(formy, dziedziny, strict=True) if not dziedzina)
    if puste:
        return Rozbiór(czytania=[], bez_głowy=puste)

    znalezione: dict = {}
    for łuki, wybór in _drzewa(tablica, dziedziny, spójne):
        if not _dopuszczalne(tablica, łuki, wybór):
            continue
        czytanie = Czytanie(
            formy=formy,
            części=tuple(czytania_form[i][wybór[i]].tag.pos for i in range(len(słowa))),
            łuki=tuple(sorted(łuk[:3] for łuk in łuki)),
        )
        sygnatura = czytanie.sygnatura()
        if sygnatura in znalezione:
            continue
        znalezione[sygnatura] = czytanie
        if len(znalezione) >= limit:
            return Rozbiór(czytania=list(znalezione.values()), urwane=True)
    return Rozbiór(czytania=list(znalezione.values()))


def _ścieżka(segmenty: list[Segment]) -> list[Segment] | None:
    """Segmenty od źródła do ujścia, o ile graf ma dokładnie jedną ścieżkę.

    Graf segmentacji rozchodzi się tam, gdzie Morfeusz widzi w formie dwa
    podziały, i wtedy zdanie ma tyle ciągów słów, ile ścieżek. Sonda takiego
    zdania nie rozbiera i mówi o tym wprost, bo pytanie, dla którego ją napisano,
    jest o łuki, a nie o segmentację, a każde zdanie próbki ma tu ścieżkę jedną.
    """
    po_węźle: dict[int, list[Segment]] = {}
    for segment in segmenty:
        po_węźle.setdefault(segment.start, []).append(segment)
    ścieżka = []
    węzeł = min(po_węźle, default=0)
    koniec = max((segment.end for segment in segmenty), default=0)
    while węzeł != koniec:
        wychodzące = po_węźle.get(węzeł, [])
        if len(wychodzące) != 1:
            return None
        ścieżka.append(wychodzące[0])
        węzeł = wychodzące[0].end
    return ścieżka


@dataclass(frozen=True)
class _Tablica:
    """Co wolno nad tym zdaniem postawić, policzone przed szukaniem drzewa."""

    czytania: list[tuple[Reading, ...]]
    #: Łuki wychodzące z każdego słowa i wchodzące do niego, w obu indeksach ten
    #: sam wpis: drugi koniec łuku, czytanie zależnego, i zbiór czytań głowy,
    #: które ten łuk dopuszcza.
    z_niego: list[list[tuple[int, Więz, int, frozenset[int]]]]
    do_niego: list[list[tuple[int, Więz, int, frozenset[int]]]]
    korzenie: list[list[int]]
    gramatyka: Gramatyka

    def __len__(self) -> int:
        return len(self.czytania)


def _tablica(czytania_form: list[tuple[Reading, ...]], gramatyka: Gramatyka) -> _Tablica:
    """Licencje łuków, policzone raz.

    Licencja łuku zależy tylko od dwóch słów i od wybranych dla nich czytań, więc
    stoi tu cała, a szukanie drzewa jej już nie przelicza. To jest ta lokalność,
    dzięki której podłoże w ogóle da się przeszukiwać: warunek globalny zostaje
    jeden, spójność, plus to, że drzewo ma być drzewem.

    Wpis jest na czytanie zależnego, a nie na parę czytań, i niesie zbiór tych
    czytań głowy, które ten łuk dopuszcza. Tym zbiorem przycina się dziedziny, a
    potem sprawdza głowę, której szukanie jeszcze nie wybrało.
    """
    z_niego: list[list[tuple[int, Więz, int, frozenset[int]]]] = [[] for _ in czytania_form]
    do_niego: list[list[tuple[int, Więz, int, frozenset[int]]]] = [[] for _ in czytania_form]
    korzenie = [
        [
            r
            for r, czytanie in enumerate(czytania)
            if _pasuje(gramatyka.korzeń, czytanie, EMPTY) is not None
        ]
        for czytania in czytania_form
    ]
    for i, czytania in enumerate(czytania_form):
        for j, czytania_głowy in enumerate(czytania_form):
            if i == j:
                continue
            for więz in gramatyka.więzy:
                if not _strona_zgadza(więz, i, j):
                    continue
                zebrane: dict[int, set[int]] = {}
                for rg, czytanie_głowy in enumerate(czytania_głowy):
                    środowisko = _pasuje(więz.głowa, czytanie_głowy, EMPTY)
                    if środowisko is None:
                        continue
                    for rz, czytanie_zależnego in enumerate(czytania):
                        if _pasuje(więz.zależny, czytanie_zależnego, środowisko) is None:
                            continue
                        zebrane.setdefault(rz, set()).add(rg)
                for rz, głowy in zebrane.items():
                    z_niego[i].append((j, więz, rz, frozenset(głowy)))
                    do_niego[j].append((i, więz, rz, frozenset(głowy)))
    return _Tablica(
        czytania=czytania_form,
        z_niego=z_niego,
        do_niego=do_niego,
        korzenie=korzenie,
        gramatyka=gramatyka,
    )


def _dziedziny(tablica: _Tablica) -> list[set[int]]:
    """Czytania, które po przycięciu jeszcze w czymkolwiek stoją.

    Czytanie bez ani jednej dozwolonej głowy nie wejdzie do żadnego drzewa, więc
    wypada, a razem z nim wypada wsparcie, które dawało czytaniom sąsiadów, i
    dlatego przycinanie chodzi w pętli aż do braku zmian. Jest to zwykła spójność
    łukowa. Żądania walencyjne przycinają w drugą stronę: czytanie, które żąda
    łuku pod sobą, wypada wtedy, gdy nie ma go skąd wziąć.
    """
    dziedziny = [set(range(len(czytania))) for czytania in tablica.czytania]
    zmiana = True
    while zmiana:
        zmiana = False
        for i, dziedzina in enumerate(dziedziny):
            odpada = {r for r in dziedzina if not _wsparte(tablica, dziedziny, i, r)}
            if odpada:
                dziedziny[i] = dziedzina - odpada
                zmiana = True
    return dziedziny


def _wsparte(tablica: _Tablica, dziedziny: list[set[int]], i: int, r: int) -> bool:
    ma_głowę = r in tablica.korzenie[i] or any(
        rz == r and głowy & dziedziny[j] for j, _więz, rz, głowy in tablica.z_niego[i]
    )
    if not ma_głowę:
        return False
    for żądanie in tablica.gramatyka.żądania:
        if _pasuje(żądanie.słowo, tablica.czytania[i][r], EMPTY) is None:
            continue
        for etykieta in żądanie.etykiety:
            if not any(
                więz.etykieta == etykieta and r in głowy and rz in dziedziny[k]
                for k, więz, rz, głowy in tablica.do_niego[i]
            ):
                return False
    return True


def _którekolwiek(żądanie: Word, segment: Segment) -> bool:
    return any(_pasuje(żądanie, czytanie, EMPTY) is not None for czytanie in segment.readings)


def _dopuszczalne(tablica: _Tablica, łuki, wybór) -> bool:
    """Czy gotowe drzewo spełnia to, czego nie da się sprawdzić po jednym łuku.

    Wszystkie trzy warunki mówią o łukach jednej głowy naraz, więc żadnego nie ma
    czym sprawdzić, dopóki drzewo nie stoi całe.
    """
    return (
        _zgody_stoją(tablica, łuki, wybór)
        and _żądania_stoją(tablica, łuki, wybór)
        and _wymagania_stoją(łuki)
    )


def _zgody_stoją(tablica: _Tablica, łuki, wybór) -> bool:
    for zgoda in tablica.gramatyka.zgody:
        for dziecko, głowa, etykieta, _ in łuki:
            if etykieta != zgoda.pierwszy:
                continue
            for inne, ta_sama, etykieta_drugiego, _drugi in łuki:
                if ta_sama != głowa or etykieta_drugiego != zgoda.drugi:
                    continue
                jedno = dict(tablica.czytania[dziecko][wybór[dziecko]].tag.features)
                drugie = dict(tablica.czytania[inne][wybór[inne]].tag.features)
                for cecha in zgoda.cechy:
                    tu, tam = jedno.get(cecha), drugie.get(cecha)
                    if tu and tam and not (tu & tam):
                        return False
    return True


def _żądania_stoją(tablica: _Tablica, łuki, wybór) -> bool:
    for żądanie in tablica.gramatyka.żądania:
        for i, czytania in enumerate(tablica.czytania):
            if _pasuje(żądanie.słowo, czytania[wybór[i]], EMPTY) is None:
                continue
            wyprowadzone = {etykieta for _, głowa, etykieta, _więz in łuki if głowa == i}
            if not set(żądanie.etykiety) <= wyprowadzone:
                return False
    return True


def _wymagania_stoją(łuki) -> bool:
    for _, głowa, etykieta, więz in łuki:
        if not więz.wymaga and not więz.zakazuje:
            continue
        pod_głową = {inna for _, ta_sama, inna, _inny in łuki if ta_sama == głowa}
        if not set(więz.wymaga) <= pod_głową:
            return False
        if set(więz.zakazuje) & (pod_głową - {etykieta}):
            return False
    return True


def _strona_zgadza(więz: Więz, zależny: int, głowa: int) -> bool:
    if więz.przyległy and abs(zależny - głowa) != 1:
        return False
    if więz.strona == PRZED:
        return zależny < głowa
    if więz.strona == PO:
        return zależny > głowa
    return True


def _pasuje(żądanie: Word, czytanie: Reading, środowisko):
    if czytanie.tag.pos not in żądanie.pos:
        return None
    if żądanie.lemmas is not None and czytanie.lemma not in żądanie.lemmas:
        return None
    cechy = dict(czytanie.tag.features)
    return unify(żądanie.constraints, cechy, środowisko)


def _drzewa(tablica: _Tablica, dziedziny: list[set[int]], spójne: bool):
    """Każde drzewo zależności nad tym zdaniem, wraz z czytaniami, na których stoi.

    Czytanie wybiera się tu razem z głową, a nie przed szukaniem drzewa, więc
    forma, której nie da się do niczego doczepić, ucina gałąź zamiast wracać w
    każdej kombinacji z osobna. Łuk postawiony w przód zostawia na swojej głowie
    warunek, czyli zbiór czytań, które dopuszcza, i głowa wybiera potem czytanie z
    przecięcia tego, co zostawili jej wszyscy zależni.

    Sprawdza się przy tym to, co da się sprawdzić od razu: korzeń jest jeden, cykl
    nie powstaje, łuk jedyny nie powtarza się pod jedną głową, a przy ``spójne``
    żaden łuk nie krzyżuje się z postawionym wcześniej.
    """
    ile = len(tablica)
    korzenie = tablica.korzenie
    po_czytaniu: list[dict[int, list[tuple[int, Więz, frozenset[int]]]]] = []
    for wpisy in tablica.z_niego:
        pogrupowane: dict[int, list[tuple[int, Więz, frozenset[int]]]] = {}
        for j, więz, rz, głowy_łuku in wpisy:
            pogrupowane.setdefault(rz, []).append((j, więz, głowy_łuku))
        po_czytaniu.append(pogrupowane)
    porządek = [sorted(dziedzina) for dziedzina in dziedziny]

    wybór: list[int] = [-1] * ile
    głowy: list[int] = [KORZEŃ] * ile
    postawione: list[tuple[int, int, str, Więz]] = []
    zajęte: set[tuple[int, str]] = set()
    warunki: list[list[frozenset[int]]] = [[] for _ in range(ile)]

    def dalej(i: int, korzeń: int | None):
        if i == ile:
            if korzeń is None:
                return
            if spójne and any(_obejmuje(łuk, korzeń) for łuk in postawione):
                return
            yield tuple(postawione), tuple(wybór)
            return
        for r in porządek[i]:
            if any(r not in dopuszczone for dopuszczone in warunki[i]):
                continue
            wybór[i] = r
            if korzeń is None and r in korzenie[i]:
                yield from dalej(i + 1, i)
            for j, więz, głowy_łuku in po_czytaniu[i].get(r, ()):
                if j < i:
                    if wybór[j] not in głowy_łuku:
                        continue
                elif not głowy_łuku & dziedziny[j]:
                    continue
                if więz.jedyny and (j, więz.etykieta) in zajęte:
                    continue
                if _cykl(i, j, głowy):
                    continue
                łuk = (i, j, więz.etykieta, więz)
                if spójne and any(_krzyżuje(łuk, inny) for inny in postawione):
                    continue
                głowy[i] = j
                postawione.append(łuk)
                if więz.jedyny:
                    zajęte.add((j, więz.etykieta))
                if j > i:
                    warunki[j].append(głowy_łuku)
                yield from dalej(i + 1, korzeń)
                if j > i:
                    warunki[j].pop()
                if więz.jedyny:
                    zajęte.discard((j, więz.etykieta))
                postawione.pop()
                głowy[i] = KORZEŃ

    yield from dalej(0, None)


def _cykl(zależny: int, głowa: int, głowy: list[int]) -> bool:
    """Czy łuk zamknąłby cykl na tym, co już postawiono.

    Głowy słów o numerze mniejszym od ``zależny`` stoją już wybrane, a dalszych
    jeszcze nie, więc pod górę idzie się tylko po wybranych. Cykl i tak nie
    ucieknie: ten jego element, który ma numer największy, dostaje głowę
    ostatni, a wtedy cała reszta pierścienia jest już wybrana.
    """
    idący = głowa
    while idący != KORZEŃ:
        if idący == zależny:
            return True
        if idący > zależny:
            return False
        idący = głowy[idący]
    return False


def _obejmuje(łuk, korzeń: int) -> bool:
    a, b = sorted(łuk[:2])
    return a < korzeń < b


def _krzyżuje(jeden, drugi) -> bool:
    a, b = sorted(jeden[:2])
    c, d = sorted(drugi[:2])
    return a < c < b < d or c < a < d < b
