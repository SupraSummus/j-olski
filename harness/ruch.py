"""Sonda różnicowa: ile konstrukcja kupuje i ile kosztuje, liczone ruchem werdyktu.

Pytanie, które ta maszyneria obsługuje, jest jedno i stawia je każda sonda
osobno: ile zdań konstrukcja odbiera. Zdanie odrzucone przez wieloznaczność jest
droższe niż zdanie, którego gramatyka nie wyprowadza wcale, bo tamto czeka na
produkcję, a to na jej wycofanie, więc sumy z ``olski-corpus`` na to nie
odpowiadają: przejście ``przyjęte → wieloznaczne`` jest ceną, przejście
``odrzucone → przyjęte`` zakupem, a jedno i drugie widać dopiero zdanie po
zdaniu.

Wariantem jest gramatyka olskiego z wyjętą grupą produkcji, a konstrukcję, którą
olski ma, mierzy się właśnie tak, przez zdejmowanie. Dopisana mierzyłaby produkcję
napisaną w sondzie, czyli drugą deklarację tego samego, i rozeszłaby się z olskim
po pierwszej zmianie, której nikt by tu nie powtórzył.

Konstrukcję, której olski nie ma, wyceniało się tu w drugą stronę: sonda
dopisywała ją świeżej gramatyce, a mianownikiem był wariant bez dopisku. Ten
kierunek wyszedł razem z przysłówkiem, czyli z jedyną sondą, która go używała, bo
konstrukcja wyceniona i wpuszczona mierzy się już zdejmowaniem. Gdyby wrócił,
wróci jako gramatyka wariantu brana funkcją, i tego żąda od tej maszynerii
``harness/luka.py``; trzyma to ``TODO.md``.

Podział pracy jest przez to jednozdaniowy. Sonda odpowiada, do której grupy
produkcja należy, a warianty, przebieg, tabelę przejść i konkurencję grup dostaje
z tego pliku; wiersz poleceń przychodzi z ``harness/komenda.py``, wspólny także
sondom, które różnicowe nie są. Wariantów jest tyle, ile grup da się zdjąć
osobno, bo cena każdej z nich jest osobną liczbą.
"""

from __future__ import annotations

import argparse
import collections
import functools
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from harness.komenda import Komenda, uruchom
from olski.corpus import Sentence, read
from olski.coverage import SOURCES, Outcome, po_kawałkach, segments_for
from olski.grammar import Grammar, Production, Sym, Word
from olski.morph import Segment
from olski.parse import parse
from olski.subset import FRAGMENT, build, check

#: Ile zdań zachować pod każdym przejściem. Przejście bez przykładu jest liczbą,
#: o której nie wiadomo, co ją wywołało, a cena jest tu tym, co trzeba przeczytać.
PRZYKŁADY = 8

#: Werdykty w kolejności, w jakiej stoją w tabeli.
STANY = ("valid", "ambiguous", "rejected")

#: Czym zaczyna się klucz przykładów trzymanych pod rolą, a nie pod przejściem.
#: Napisem, a nie drugim słownikiem, bo obie rodziny przykładów wchodzą do
#: jednego budżetu :attr:`Raport.ile_przykładów`, scalają się jednym :func:`scal`
#: i wychodzą jednym wydrukiem.
ROLA = "rola:"

#: Rola, pod którą przykładów nie trzymamy, bo zdanie przeczytane tak jak w banku
#: drzew nie jest tym, co z tej tabeli trzeba przeczytać. Wartość wydaje
#: ``Outcome.agreement`` i tyle o niej wie ten plik.
ZGODNE = "agrees"

#: Nazwy obu morfologii w nagłówku wydruku, bo nagłówek stoi po polsku.
#: Kluczem jest nazwa źródła z ``olski/coverage.py``, żeby źródło dopisane tam
#: zgłosiło się tutaj brakiem nazwy, a nie wydrukiem, który milczy o tym,
#: co mierzył.
MORFOLOGIA = {"gold": "złota", "live": "żywa"}


@dataclass(frozen=True)
class Sonda:
    """Co jedna sonda różnicowa mówi o sobie wspólnemu przebiegowi.

    Warianty stoją w kolejności wydruku. Pierwszy zdejmuje wszystko i jest
    mianownikiem, wobec którego liczone są przejścia; ostatni zdejmuje zero i
    dopiero on pokazuje konkurencję między grupami, o którą sondzie chodzi.
    Między nimi stoi po jednym wariancie na grupę zdejmowaną osobno.

    Ostatni jest przez to samym olskim, bo grupy nie zdejmuje żadnej.
    """

    #: Nazwa modułu, czyli ``harness.płaski``. Wiersz poleceń robi z niej i pomoc,
    #: i prefiks komunikatu o brakującej ścieżce (``harness/komenda.py``).
    nazwa: str
    #: O co ta sonda pyta, jednym zdaniem, do wydruku pomocy.
    opis: str
    #: Nazwy wariantów, one zaś są etykietami wiersza w tabeli, więc stoją tu
    #: pełnym napisem: `bez przecinka`, a nie `bez`. Nazwy pośrednie są przy tym
    #: nazwami grup, czyli tym, co oddaje :attr:`grupa`, i po tym wspólnym napisie
    #: wariant poznaje swoje produkcje.
    warianty: tuple[str, ...]
    #: Do której grupy należy ta produkcja; ``None``, gdy do żadnej i gdy zostaje
    #: w każdym wariancie. To jedno pytanie jest wszystkim, czym sondy różnicowe
    #: się różnią, i dlatego gramatykę wariantu składa :func:`gramatyka` niżej,
    #: jedna dla wszystkich, a nie każda sonda po swojemu.
    grupa: Callable[[Production], str | None]
    #: Dwa pytania o konkurencję grup, w kolejności wydruku, każde całym zdaniem.
    #: Całym, a nie rzeczownikiem do wstawienia w gotowy wzór: wzór żądałby od
    #: każdej sondy formy fleksyjnej, a nagłówek nad tymi dwoma wierszami nazwy
    #: grupy nie potrzebuje, bo one same ją noszą.
    #: Konkurencja ma dwa stopnie. Zdanie, które rusza się pod jedną grupą i pod
    #: drugą, jest zdaniem, o które grupy się spierają. Zdanie, o którym oba
    #: warianty naraz mówią co innego, niż mówi którykolwiek z nich osobno, jest
    #: zdaniem, na którym ten spór coś kosztuje: dwie produkcje dały mu czytanie,
    #: którego żadna z nich nie dała.
    #: Puste, kiedy grupa jest jedna: nie ma wtedy z czym konkurować, a pomiar na
    #: jednej grupie jest tym, co pisze się w sesji najczęściej.
    pytania: tuple[str, ...] = ()

    @property
    def osobne(self) -> tuple[str, ...]:
        """Warianty zdejmujące po jednej grupie, czyli te między mianownikiem a całością."""
        return self.warianty[1:-1]

    @property
    def czysty(self) -> str:
        """Wariant, który jest dokładnie gramatyką olskiego, czyli ten, co nie zdejmuje nic.

        Nazwany, a nie brany numerem, bo pyta o niego także ``harness/płaski.py``,
        która nad tą gramatyką liczy drzewa, a nie werdykty; niezmiennik pilnuje
        ``tests/test_ruch.py``.
        """
        return self.warianty[-1]


#: Części mowy, pod którymi Morfeusz trzyma spójnik. Dwie, bo rozdziela on
#: podrzędny od współrzędnego, a interpunkcja przed spójnikiem tego podziału nie zna.
SPÓJNIKOWE = frozenset({"conj", "comp"})


def koordynuje(produkcja: Production) -> bool:
    """Czy ta produkcja koordynuje, czyli czy jej symbol stoi wśród własnych córek.

    Ciąg współrzędny jest resztą ciągu po odjęciu członu, więc symbol koordynacji
    stoi nad sobą i tym się poznaje; tak samo poznaje go werdykt
    (``_koordynuje`` w ``olski/parse.py``).

    Pytają o to sondy, które zdejmują znak koordynacji, bo sam znak w ciele na to
    nie odpowiada: polszczyzna stawia przecinek i tam, gdzie nic się nie koordynuje,
    a zdjęta produkcja podrzędna zostawiłaby symbol bez ani jednego ciała,
    a gramatyka z symbolem nieokreślonym nie rozbiera niczego.
    """
    return any(
        isinstance(część, Sym) and część.name == produkcja.head for część in produkcja.body
    )


def ma_symbol(produkcja: Production, nazwa: str) -> bool:
    """Czy w ciele tej produkcji stoi ten symbol.

    Pytają o to sondy grupujące produkcje po tym, co produkcja bierze, a nie po
    tym, co definiuje. Pozycję konstrukcji stawia bowiem ciało, więc to ciało
    należy do grupy zdejmowanej, a symbol, który w nim stoi, zostaje.
    """
    return any(isinstance(część, Sym) and część.name == nazwa for część in produkcja.body)


def ze_spójnikiem(produkcja: Production) -> bool:
    """Czy w ciele tej produkcji stoi spójnik (:data:`SPÓJNIKOWE`).

    Rozdziela to dwa znaki koordynacji, które polszczyzna stawia przed zdaniem
    składowym, a sondy mierzą osobno: sam przecinek i przecinek przed spójnikiem.
    """
    return any(isinstance(część, Word) and część.pos & SPÓJNIKOWE for część in produkcja.body)


@functools.cache
def gramatyka(sonda: Sonda, wariant: str) -> Grammar:
    """Gramatyka olskiego bez tych grup produkcji, których ten wariant nie ma.

    Przepisujemy produkcje ze świeżej gramatyki, takie jakie są, bo złożona drugi
    raz z części gubiłaby głowę (``Grammar.dopisz``). Wariant pełny dostaje przez
    to wszystkie, a wariant :attr:`Sonda.czysty` dokładnie te, które olski ma, co
    pilnuje ``tests/test_ruch.py``.

    Budowana raz na proces roboczy, bo budowa jest droższa niż rozbiór jednego
    zdania, a gramatyka po zbudowaniu się nie zmienia.
    """
    if wariant not in sonda.warianty:
        raise ValueError(f"{sonda.nazwa}: nieznany wariant: {wariant}")
    pełna = build()
    okrojona = Grammar(start=pełna.start)
    for produkcja in pełna.productions:
        grupa = sonda.grupa(produkcja)
        if grupa is not None and wariant != sonda.warianty[-1] and grupa != wariant:
            continue
        okrojona.dopisz(produkcja)
    return okrojona


@dataclass
class Raport:
    """Liczniki jednego przebiegu, wraz ze zdaniami, które je czynią czytelnymi."""

    sonda: Sonda
    #: Ile zdań zachować pod każdym przejściem. Stoi przy licznikach, a nie przy
    #: każdym wołaniu, bo jest tym samym przez cały przebieg i przy scalaniu.
    ile_przykładów: int = PRZYKŁADY
    #: Wariant → ile zdań wyszło którym werdyktem.
    stany: dict[str, collections.Counter] = field(default_factory=dict)
    #: Wariant → ile zdań przeszło z którego werdyktu na który.
    przejścia: dict[str, collections.Counter] = field(default_factory=dict)
    #: (wariant, przejście) → zdania, na których to przejście widać.
    przykłady: dict[tuple[str, str], list[str]] = field(default_factory=dict)
    #: Wariant → jak role zdań nowo przyjętych mają się do drzewa wzorcowego.
    #: Zdanie przyjęte odwrotnie niż w banku drzew nie jest zakupem.
    zgodność: dict[str, collections.Counter] = field(default_factory=dict)
    #: Czy grupy produkcji wchodzą sobie w drogę; co to znaczy, mówi
    #: :attr:`Sonda.pytania`.
    konkurencja: collections.Counter = field(default_factory=collections.Counter)
    #: Zdania, których nie zmierzono, po powodzie. Wypisane, a nie odjęte po
    #: cichu, bo mianownik bez nich byłby mianownikiem zdań łatwych.
    pominięte: collections.Counter = field(default_factory=collections.Counter)

    @property
    def zmierzone(self) -> int:
        return sum(self.stany.get(self.sonda.warianty[0], collections.Counter()).values())

    def zapisz(
        self,
        tekst: str,
        stany: dict[str, str],
        role: dict[str, str | None],
    ) -> None:
        """Zapisz jedno zdanie: werdykt pod każdym wariantem i role pod nowo przyjętym.

        Werdykt jest tu napisem, a nie wynikiem rozbioru, bo zdanie przychodzi z
        dwóch korpusów naraz: z banku drzew, gdzie niesie drzewo wzorcowe, i z
        prozy, gdzie nie niesie żadnego. Role przychodzą więc obok werdyktu i nad
        prozą stoją puste, zamiast rozdwajać ten licznik na dwa.
        """
        mianownik = stany[self.sonda.warianty[0]]
        for wariant, stan in stany.items():
            self.stany.setdefault(wariant, collections.Counter())[stan] += 1
            if wariant == self.sonda.warianty[0] or stan == mianownik:
                continue
            przejście = f"{mianownik} → {stan}"
            self.przejścia.setdefault(wariant, collections.Counter())[przejście] += 1
            self.zanotuj((wariant, przejście), tekst)
            if stan == "valid" and wariant in role:
                zgoda = role[wariant] or "brak roli"
                self.zgodność.setdefault(wariant, collections.Counter())[zgoda] += 1
                #  Przejście, pod którym takie zdanie stoi, trzyma je razem z
                #  kilkudziesięcioma zgodnymi, więc pod rolą stoi drugi raz.
                if zgoda != ZGODNE:
                    self.zanotuj((wariant, f"{ROLA} {zgoda}"), tekst)
        self._konkurencja(tekst, stany, mianownik)

    def _konkurencja(self, tekst: str, stany: dict[str, str], mianownik: str) -> None:
        ruszone = {
            wariant: stany[wariant]
            for wariant in self.sonda.osobne
            if stany[wariant] != mianownik
        }
        if len(self.sonda.pytania) < 2:
            return
        if len(ruszone) >= 2:
            self._policz(self.sonda.pytania[0], tekst)
        if stany[self.sonda.warianty[-1]] not in {mianownik, *ruszone.values()}:
            self._policz(self.sonda.pytania[1], tekst)

    def _policz(self, nazwa: str, tekst: str) -> None:
        self.konkurencja[nazwa] += 1
        self.zanotuj(("konkurencja", nazwa), tekst)

    def zanotuj(self, klucz: tuple[str, str], tekst: str) -> None:
        """Zachowaj zdanie pod kluczem, dopóki mieści się w budżecie przykładów."""
        zachowane = self.przykłady.setdefault(klucz, [])
        if len(zachowane) < self.ile_przykładów:
            zachowane.append(tekst)


def _warianty(
    sonda: Sonda,
    zdanie: Sentence,
    segmenty: list[Segment],
    comparable: bool,
) -> dict[str, Outcome]:
    """Werdykt każdego wariantu, bez rozbiorów, których odpowiedź jest już znana.

    Wariant produkcje zdejmuje i żaden nie dopisuje ani jednej (:func:`gramatyka`),
    więc jego czytania są podzbiorem czytań olskiego:
    zdanie, którego olski nie wyprowadza, nie wyprowadza się pod żadnym z nich.
    Rozbiór olskiego idzie przez to pierwszy,
    a odrzucenie zamyka pozostałe warianty jedną odpowiedzią,
    bo o zdaniu odrzuconym mówią one to samo.
    Olski odrzuca większość zdań banku drzew, co drukuje ``olski-corpus``,
    więc z przebiegu wypada przeszło połowa rozbiorów.
    Że wariant naprawdę niczego nie dopisuje, pilnuje ``tests/test_ruch.py``:
    kierunek przez dopisywanie ta maszyneria kiedyś miała i może go odzyskać.
    """

    def wynik(wariant: str) -> Outcome:
        return Outcome(
            sentence=zdanie,
            result=parse(gramatyka(sonda, wariant), segmenty, zatrzymanie=False),
            segments=tuple(segmenty),
            comparable=comparable,
        )

    czysty = wynik(sonda.czysty)
    if czysty.result.rejected:
        return dict.fromkeys(sonda.warianty, czysty)
    wyniki = {wariant: wynik(wariant) for wariant in sonda.warianty[:-1]}
    wyniki[sonda.czysty] = czysty
    return wyniki


def zmierz(
    sonda: Sonda,
    zdania: Iterable[Sentence],
    przykłady: int = PRZYKŁADY,
    źródło: str = "gold",
) -> Raport:
    """Przepuść zdania banku drzew przez każdy wariant i policz, co się rusza.

    Populacja jest ta sama, co w ``olski.coverage.measure``: każde zdanie z
    drzewem wzorcowym, bez granicy na długość.

    Morfologia jest dwojaka i konstrukcja bywa taka, że pod jedną z nich nie
    kosztuje nic. Anotator wybrał w banku drzew jedno czytanie na token, więc
    konstrukcja konkurująca z czytaniem, którego on nie wybrał, wychodzi pod złotą
    morfologią darmowa, a płaci dopiero tam, gdzie czytania są wszystkie —
    czyli w tekście, który olski dostaje do sprawdzenia.
    Ról pod żywą morfologią nie porównujemy, bo rozpiętości nie są wtedy
    rozpiętościami drzewa wzorcowego (``Outcome.comparable``),
    i tym ten przebieg jest podobny do przebiegu nad prozą niżej.
    """
    raport = Raport(sonda, przykłady)
    for zdanie in zdania:
        if not zdanie.annotated:
            continue
        segmenty = segments_for(zdanie, źródło)
        if not segmenty:
            raport.pominięte["bez morfologii"] += 1
            continue
        wyniki = _warianty(sonda, zdanie, segmenty, comparable=źródło == "gold")
        raport.zapisz(
            zdanie.text,
            {wariant: wynik.status for wariant, wynik in wyniki.items()},
            {wariant: wynik.agreement for wariant, wynik in wyniki.items()}
            if źródło == "gold"
            else {},
        )
    return raport


def nad_prozą(sonda: Sonda, tekst: str, przykłady: int = PRZYKŁADY) -> Raport:
    """To samo porównanie nad prozą, którą olski ma czytać.

    Bank drzew rankinguje konstrukcje w rejestrze, którego olski nie ma, i mówi
    przez to, ile konstrukcja kupuje w cudzej polszczyźnie. Drugie pytanie jest o
    rejestr własny i pada tu. Ról nie ma czym porównać, bo drzewa wzorcowego
    proza nie niesie, a fragment nie jest zdaniem i do mianownika nie wchodzi.
    """
    raport = Raport(sonda, przykłady)
    wyniki = {wariant: check(tekst, gramatyka(sonda, wariant)) for wariant in sonda.warianty}
    for kolejne in zip(*wyniki.values(), strict=True):
        werdykty = dict(zip(sonda.warianty, kolejne, strict=True))
        pierwszy = werdykty[sonda.warianty[0]]
        if pierwszy.status == FRAGMENT:
            raport.pominięte["fragment, a nie zdanie"] += 1
            continue
        raport.zapisz(
            pierwszy.text,
            {wariant: werdykt.status for wariant, werdykt in werdykty.items()},
            {},
        )
    return raport


def _kawałek(ścieżki: Sequence[Path], sonda: Sonda, przykłady: int, źródło: str):
    return zmierz(sonda, (read(ścieżka) for ścieżka in ścieżki), przykłady, źródło)


def przebieg(
    sonda: Sonda,
    ścieżki: Sequence[Path],
    jobs: int,
    przykłady: int = PRZYKŁADY,
    źródło: str = "gold",
) -> Raport:
    """Zmierz listę lasów na tylu procesach, ile podano, i złóż jeden raport.

    Podział na kawałki jest ten sam, którym idzie ``olski-corpus``, i stoi tam,
    bo decyzja o jego rozmiarze jest jedna. Składanie zostaje tutaj, bo licznik,
    który z kawałka wraca, jest licznikiem sondy.
    """
    praca = functools.partial(_kawałek, sonda=sonda, przykłady=przykłady, źródło=źródło)
    return scal(sonda, po_kawałkach(ścieżki, jobs, praca), przykłady)


def scal(sonda: Sonda, raporty: Iterable[Raport], przykłady: int = PRZYKŁADY) -> Raport:
    """Złóż raporty kawałków w jeden.

    Kawałki są odcinkami jednej posortowanej listy plików i wchodzą tu w jej
    kolejności, więc scalony raport jest tym samym raportem, co z jednego
    przebiegu nad całością, przykłady włącznie.
    """
    scalony = Raport(sonda, przykłady)
    for raport in raporty:
        for wariant, licznik in raport.stany.items():
            scalony.stany.setdefault(wariant, collections.Counter()).update(licznik)
        for wariant, licznik in raport.przejścia.items():
            scalony.przejścia.setdefault(wariant, collections.Counter()).update(licznik)
        for wariant, licznik in raport.zgodność.items():
            scalony.zgodność.setdefault(wariant, collections.Counter()).update(licznik)
        scalony.konkurencja.update(raport.konkurencja)
        scalony.pominięte.update(raport.pominięte)
        for klucz, zachowane in raport.przykłady.items():
            for tekst in zachowane:
                scalony.zanotuj(klucz, tekst)
    return scalony


# --------------------------------------------------------------------------- #
# Wydruk
# --------------------------------------------------------------------------- #


def wydruk(raport: Raport, nagłówek: str) -> str:
    sonda = raport.sonda
    szerokość = max(len("wariant"), *(len(wariant) for wariant in sonda.warianty))
    wiersze = [
        f"{nagłówek}, {raport.zmierzone} zdań",
        "",
        f"{'wariant':>{szerokość}}  {'przyjęte':>10} {'wieloznaczne':>13} {'odrzucone':>10}",
    ]
    for wariant in sonda.warianty:
        licznik = raport.stany.get(wariant, collections.Counter())
        przyjęte, wieloznaczne, odrzucone = (licznik.get(stan, 0) for stan in STANY)
        wiersze.append(
            f"{wariant:>{szerokość}}  {przyjęte:>10} {wieloznaczne:>13} {odrzucone:>10}"
        )
    for powód, ile in raport.pominięte.most_common():
        wiersze.append(f"{ile:>7}          niezmierzone: {powód}")

    for wariant in sonda.warianty[1:]:
        przejścia = raport.przejścia.get(wariant)
        wiersze += ["", f"ruch wobec wariantu „{sonda.warianty[0]}” — {wariant}:"]
        if not przejścia:
            wiersze.append("  żadne zdanie nie zmieniło werdyktu")
            continue
        for przejście, ile in przejścia.most_common():
            wiersze.append(f"  {ile:>7}  {przejście}")
        zgodność = raport.zgodność.get(wariant)
        if zgodność:
            wiersze.append("  role zdań nowo przyjętych wobec drzewa wzorcowego:")
            for nazwa, ile in zgodność.most_common():
                wiersze.append(f"  {ile:>7}    {nazwa}")
                for tekst in raport.przykłady.get((wariant, f"{ROLA} {nazwa}"), []):
                    wiersze.append(f"             {tekst}")

    # Zero wypisane, a nie pominięte: liczba, której nie ma, czyta się jak
    # pomiar, którego nie było, a to jest ta liczba, po którą sonda stoi.
    wiersze += ["", "konkurencja, nad zdaniem po zdaniu:"]
    for nazwa in sonda.pytania:
        wiersze.append(f"  {raport.konkurencja.get(nazwa, 0):>7}  {nazwa}")

    for nazwa in sonda.pytania:
        zachowane = raport.przykłady.get(("konkurencja", nazwa), [])
        if zachowane:
            wiersze += ["", f"konkurencja, {nazwa}:"]
            wiersze += [f"  {tekst}" for tekst in zachowane]

    for wariant in sonda.warianty[1:]:
        for przejście, _ in raport.przejścia.get(wariant, collections.Counter()).most_common():
            zachowane = raport.przykłady.get((wariant, przejście), [])
            if not zachowane:
                continue
            wiersze += ["", f"{wariant}, {przejście}:"]
            wiersze += [f"  {tekst}" for tekst in zachowane]

    return "\n".join(wiersze)


def _morfologia(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--morfologia",
        choices=SOURCES,
        default="gold",
        help="czytania banku drzew: wybrane przez anotatora czy wszystkie, jakie ma Morfeusz",
    )


def _korpus(sonda: Sonda, ścieżki: Sequence[Path], args: argparse.Namespace) -> str:
    raport = przebieg(sonda, ścieżki, args.jobs, przykłady=args.przykłady, źródło=args.morfologia)
    return wydruk(raport, f"Składnica, morfologia {MORFOLOGIA[args.morfologia]}")


def _proza(sonda: Sonda, tekst: str, ścieżka: Path, args: argparse.Namespace) -> str:
    return wydruk(nad_prozą(sonda, tekst, args.przykłady), f"{ścieżka.name}, proza")


def main(sonda: Sonda, argv: Sequence[str] | None = None) -> int:
    """Puszcza sondę różnicową nad bankiem drzew albo nad plikiem prozy.

    Sonda pisana pod jedną decyzję woła to jednym wierszem,
    bo od sond wpisanych do drzewa różni się tym, co zdejmuje,
    a nie tym, o co pyta w wierszu poleceń (``CLAUDE.md#code``).
    """
    return uruchom(
        Komenda(
            nazwa=sonda.nazwa,
            opis=sonda.opis,
            przykłady=PRZYKŁADY,
            korpus=functools.partial(_korpus, sonda),
            proza=functools.partial(_proza, sonda),
            argumenty=_morfologia,
        ),
        argv,
    )
