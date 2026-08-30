"""The grammar formalism: symbols, productions, and feature unification.

A grammar is data, in Python. What a production says is:
this constituent is made of these parts, and these features of the parts must be
the same feature. Agreement is therefore not a check bolted onto the parse; it is
the parse. A noun phrase whose adjective disagrees with its noun has no
derivation, so it is not olski.

Feature values are sets, because a Polish form is usually ambiguous:
``pliku`` is genitive, locative or vocative, and ``program`` is nominative or
accusative. Unification intersects those sets, and a constituent survives only
while every intersection stays non-empty. That is how ``Program zapisuje
ustawienia`` resolves — nominative for the subject, accusative for the object —
without anything having to choose a reading up front.
"""

from __future__ import annotations

from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class Var:
    """A feature variable, shared between the parts of one production."""

    name: str

    def __repr__(self) -> str:
        return f"?{self.name}"


def V(name: str) -> Var:
    return Var(name)


#: Zbiór napisów, o jaki pyta gramatyka: wartość cechy, część mowy, lemat albo
#: nazwa cechy. Napis pojedynczy znaczy zbiór jednoelementowy, bo o jedną wartość
#: pyta większość tych pytań, a klamry wokół jednej wartości niczego o niej nie
#: mówią.
Zbiór = str | Collection[str]


def _zbiór(wartość: Zbiór | None) -> frozenset[str] | None:
    if wartość is None:
        return None
    return frozenset({wartość} if isinstance(wartość, str) else wartość)


#: What a feature may be constrained to: a variable, or a set of literal values.
Spec = Var | frozenset


def _spec(value: Var | Zbiór) -> Spec:
    return value if isinstance(value, Var) else _zbiór(value)


def _wypisz(spec: Spec) -> str:
    """Więz wypisany tak, że dwa przebiegi piszą go tak samo.

    Hasze napisów są losowane przy starcie, więc ``repr`` zbioru wypisuje
    wartości za każdym razem w innej kolejności, a odcisk gramatyki wzięty
    z dwóch drzew roboczych pokazuje wtedy różnicę, której nie ma.
    """
    return repr(spec) if isinstance(spec, Var) else "{" + ", ".join(sorted(spec)) + "}"


def _constraints(features: dict) -> tuple[tuple[str, Spec], ...]:
    """Więzy w kolejności ustalonej tutaj, bo unifikacja przechodzi je po kolei.

    Przecięcie zbiorów jest przemienne, więc kolejność wyniku nie zmienia,
    a ustalona po nazwie zrównuje dwa symbole napisane w innym porządku cech.
    Nazwy są różne, bo przychodzą ze słownika, więc porównanie nie schodzi do
    specyfikacji obok nazwy, której porównać się nie da.
    """
    return tuple(sorted((name, _spec(value)) for name, value in features.items()))


@dataclass(frozen=True)
class Sym:
    """A reference to a non-terminal, with constraints on its features."""

    name: str
    constraints: tuple[tuple[str, Spec], ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "_hasz", hash((self.name, self.constraints)))

    def __hash__(self) -> int:
        """Hasz policzony raz, z powodu, który podaje :meth:`Production.__hash__`."""
        return self._hasz

    def __repr__(self) -> str:
        if not self.constraints:
            return self.name
        inner = ", ".join(f"{n}={_wypisz(v)}" for n, v in self.constraints)
        return f"{self.name}[{inner}]"


@dataclass(frozen=True)
class Word:
    """A terminal: one morphological reading, constrained by tag and lemma."""

    pos: frozenset[str]
    constraints: tuple[tuple[str, Spec], ...] = ()
    lemmas: frozenset[str] | None = None
    #: Lematy, których ten terminal nie bierze, czyli warunek ujemny. Stoi na
    #: lemacie, bo lemat jest osobnym testem w :func:`bierze`, a nie żądaniem
    #: wobec cech, których przecięcie negacji nie zna; docs/subset.md wywodzi to
    #: pod pierwszym z warunków tego rodzaju i tam rozdziela oba ich zasięgi.
    bez_lematów: frozenset[str] | None = None
    #: Ten sam warunek ujemny o formie zamiast o czytaniu: formę, której lemat
    #: wypada tu którymkolwiek czytaniem, terminal odrzuca całą. Żąda tego zasięgu
    #: rozłączność klas walencyjnych (:func:`_klasy` w ``olski/subset.py``);
    #: czemu zostają dwa, wywodzi docs/subset.md pod warunkiem wyżej.
    bez_lematów_formy: frozenset[str] | None = None
    #: Cechy, które forma ma nieść, żeby ten terminal ją wziął, czyli żądanie
    #: samej obecności: `word("adv", niesie="degree")` bierze `bardzo`, a `tu` nie.
    #: Stoi obok testu na lemat, a nie w :func:`unify`, bo cechy nieobecnej
    #: unifikacja nie sprawdza, więc wypisanie wszystkich wartości znaczy tam tyle,
    #: co milczenie; docs/design-notes.md wywodzi to razem z warunkiem ujemnym
    #: wyżej, bo oba pytają o formę, a nie o zgodność.
    niesione: frozenset[str] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "_hasz",
            hash(
                (
                    self.pos,
                    self.constraints,
                    self.lemmas,
                    self.bez_lematów,
                    self.bez_lematów_formy,
                    self.niesione,
                )
            ),
        )

    def __hash__(self) -> int:
        """Hasz policzony raz, z powodu, który podaje :meth:`Production.__hash__`."""
        return self._hasz

    def __repr__(self) -> str:
        return f"<{'|'.join(sorted(self.pos))}>"


Part = Sym | Word


@dataclass(frozen=True)
class Głowa:
    """Znacznik na tej córce, którą konstytuent jest.

    Znacznik wchodzi do ciała, a nie obok niego, bo obok byłby numerem pozycji,
    a numer myli się bez śladu: przestawione ciało zostawia go niezmienionym i
    nikt tego nie zauważy. Znacznik przesuwa się razem ze swoją częścią.
    """

    część: Part


def _głowa(head: str, body: list[Part | Głowa]) -> tuple[tuple[Part, ...], int]:
    """Ciało bez znaczników i pozycja głowy w nim.

    Ciało o jednej części ma głowę bez wyboru, więc znacznika nie wymaga. Ciało
    o kilku wymaga go i bez niego nie powstaje: produkcja, która nie mówi, którą
    z córek jest ten konstytuent, zostawia werdykt bez nazwy dla gospodarza
    przyłączenia, a po to jedno głowa tu jest.
    """
    zaznaczone = [i for i, część in enumerate(body) if isinstance(część, Głowa)]
    if len(zaznaczone) > 1:
        raise ValueError(f"{head}: ciało ma dwie głowy, a wolno mu mieć jedną")
    if not zaznaczone and len(body) > 1:
        raise ValueError(f"{head}: ciało o kilku częściach nie mówi, która jest głową")
    części = tuple(część.część if isinstance(część, Głowa) else część for część in body)
    return części, zaznaczone[0] if zaznaczone else 0


@dataclass(frozen=True)
class Production:
    """One way of building a constituent, and the features it comes out with."""

    head: str
    body: tuple[Part, ...]
    #: Cechy, z jakimi konstytuent wychodzi z tej produkcji, zwykle zmiennymi
    #: wspólnymi z ciałem, żeby grupa wzięła liczbę i przypadek od swojego słowa.
    #: Wypisuje się tu to, czego z głowy nie widać:
    #: cechy córki-głowy wpisuje tu :meth:`Grammar.rule`.
    features: tuple[tuple[str, Spec], ...] = ()
    #: Która z córek jest głową, czyli tą, którą ten konstytuent jest i po
    #: której nazywa go werdykt jednym słowem. ``head`` nazywa symbol, który ta
    #: produkcja definiuje, a ``głowa`` pozycję w jej ciele: jedno słowo w dwóch
    #: językach na dwie różne rzeczy. Ciało puste głowy nie ma, a zero nie
    #: nazywa w nim niczego, bo nie ma tam żadnej córki.
    głowa: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "_hasz", hash((self.head, self.body, self.features, self.głowa)))

    def __hash__(self) -> int:
        """Hasz policzony raz, bo gramatyka powstaje raz i już się nie zmienia.

        Produkcja jest częścią każdego stanu tablicy Earleya, a jej części
        stoją w zbiorze, którym rozbiór odsiewa stany (``olski/parse.py``),
        więc każde z tych trojga haszuje się po kilka milionów razy na dokument.
        Hasz wywiedziony z pól przechodziłby za każdym razem całe ciało,
        a w nim więzy każdej części.
        Równość zostaje ta, którą daje ``dataclass``: hasz nie jest polem.
        """
        return self._hasz

    def __repr__(self) -> str:
        return f"{self.head} → {' '.join(repr(part) for part in self.body)}"


def nt(name: str, **features) -> Sym:
    """Refer to a non-terminal: ``nt("grupa_imienna", case="nom", number=V("n"))``."""
    return Sym(name=name, constraints=_constraints(features))


def word(
    pos: Zbiór,
    lemma: Zbiór | None = None,
    bez_lematu: Zbiór | None = None,
    bez_lematu_formy: Zbiór | None = None,
    niesie: Zbiór | None = None,
    **features,
) -> Word:
    """Match a morphological reading: ``word("subst", case=V("c"))``.

    ``pos`` may name alternatives, as in ``{"fin", "praet"}``.
    ``bez_lematu`` names alternatives the same way and excludes them instead,
    and ``bez_lematu_formy`` excludes them by the whole form
    rather than by the one reading being matched.
    ``niesie`` nazywa cechy, które forma ma nieść, tym samym zbiorem.
    """
    return Word(
        pos=_zbiór(pos),
        constraints=_constraints(features),
        lemmas=_zbiór(lemma),
        bez_lematów=_zbiór(bez_lematu),
        bez_lematów_formy=_zbiór(bez_lematu_formy),
        niesione=_zbiór(niesie),
    )


class Grammar:
    """A set of productions, indexed by the constituent they build.

    Cechy, których produkcja żąda od córki oznaczonej :class:`Głowa`,
    wychodzą z konstytuenta same, bo konstytuent jest tą córką:
    ``grupa_orzeczenia`` żądające liczby i rodzaju od czasownika
    wypuszcza tę liczbę i ten rodzaj bez wypisywania ich drugi raz.
    Wypisane wygrywa, więc produkcja wypuszczająca co innego mówi to wprost,
    a symbol, który cechy swojej głowy w górę nie niesie,
    stoi w :attr:`nie_wypuszczane`.

    Domyślność idzie w tę stronę, bo pomyłki są tu nierówne.
    Cechy nieobecnej unifikacja nie sprawdza,
    więc konstytuent milczący o cesze przechodzi pod każdy więz na nią
    i wypisanie pominięte luzowałoby gramatykę bez śladu w wydruku,
    a wpis zbędny w :attr:`nie_wypuszczane` zawęża
    i widać go po zdaniu, które przestało się wyprowadzać.
    """

    def __init__(
        self, start: str, nie_wypuszczane: Mapping[str, Iterable[str]] | None = None
    ) -> None:
        self.start = start
        #: Cechy, których symbol nie niesie w górę,
        #: choć jego produkcje żądają ich od swoich głów;
        #: powód każdego wpisu stoi przy liście u wołającego.
        self.nie_wypuszczane = {
            symbol: frozenset(cechy) for symbol, cechy in (nie_wypuszczane or {}).items()
        }
        self.productions: list[Production] = []
        self._by_head: dict[str, list[Production]] = {}
        self._po_części_mowy: dict[str, tuple[Word, ...]] | None = None
        self._zaczynane: dict[Word | None, frozenset[Part]] | None = None
        self._nieokreślone: frozenset[str] | None = None

    def rule(self, head: str, body: list[Part | Głowa], **features) -> Production:
        części, głowa = _głowa(head, body)
        return self.dopisz(
            Production(
                head=head,
                body=części,
                features=self._wypuszczane(head, features, części[głowa] if części else None),
                głowa=głowa,
            )
        )

    def _wypuszczane(
        self, head: str, features: dict, głowa: Part | None
    ) -> tuple[tuple[str, Spec], ...]:
        """Cechy wypisane, a za nimi te, które wychodzą z głowy same.

        Wypisana wygrywa: ``rdzeń_względny`` wypuszcza liczbę i rodzaj swojego zaimka,
        a nie te, których żąda od czasownika.
        Ciało puste głowy nie ma, więc nie ma wtedy skąd wypuszczać.
        """
        wypisane = _constraints(features)
        if głowa is None:
            return wypisane
        nazwy = {name for name, _ in wypisane} | self.nie_wypuszczane.get(head, frozenset())
        z_głowy = [(name, spec) for name, spec in głowa.constraints if name not in nazwy]
        return tuple(sorted([*wypisane, *z_głowy]))

    def dopisz(self, production: Production) -> Production:
        """Wpisz produkcję gotową, czyli wziętą z innej gramatyki.

        Tędy powstaje wariant gramatyki: sonda przepisuje produkcje do gramatyki
        uboższej takimi, jakie są. Złożona drugi raz z części gubiłaby to,
        czego ``rule`` nie przyjmuje osobnym argumentem, czyli głowę.
        """
        self.productions.append(production)
        self._by_head.setdefault(production.head, []).append(production)
        #  Wszystko, co gramatyka policzyła o sobie, przestaje być prawdą.
        self._po_części_mowy = self._zaczynane = self._nieokreślone = None
        return production

    def for_head(self, head: str) -> list[Production]:
        return self._by_head.get(head, [])

    def licencjonuje(
        self,
        pos: str,
        lemma: str,
        lematy: frozenset[str],
        features: dict[str, frozenset[str]],
    ) -> bool:
        """Czy jakikolwiek terminal tej gramatyki bierze takie czytanie formy.

        Pytanie stawiane przed rozbiorem i wyprowadzone z gramatyki, a nie
        napisane obok niej: czytanie, którego nie bierze tu żaden terminal, nie
        przejdzie przy żadnym środowisku cech, bo unifikacja tylko zawęża. Forma,
        której w ten sposób nie zostaje ani jedno czytanie, jest tym, na czym
        odrzucenie stanęło; docs/design-notes.md wywodzi, czemu warstwa mówiąca
        to samo obok gramatyki byłaby gramatyką napisaną dwa razy.
        """
        return any(
            bierze(terminal, pos, lemma, lematy, features, EMPTY) is not None
            for terminal in self.terminale_dla(pos)
        )

    def terminale_dla(self, pos: str) -> tuple[Word, ...]:
        """Terminale, które w ogóle biorą tę część mowy, każdy raz.

        Pytanie o licencję pada raz na czytanie formy, a odpowiada za nie część
        mowy w większości przypadków, więc indeks stoi na niej: bez niego każde
        czytanie przechodzi przez wszystkie terminale gramatyki. Ten sam terminal
        stoi w kilku produkcjach, a odpowiada wszędzie tak samo, więc wchodzi tu raz.
        """
        if self._po_części_mowy is None:
            indeks: dict[str, dict[Word, None]] = {}
            for production in self.productions:
                for part in production.body:
                    if isinstance(part, Word):
                        for nazwa in part.pos:
                            indeks.setdefault(nazwa, {})[part] = None
            self._po_części_mowy = {nazwa: tuple(słowa) for nazwa, słowa in indeks.items()}
        return self._po_części_mowy.get(pos, ())

    def zaczynane(self) -> dict[Word | None, frozenset[Part]]:
        """Terminal → części ciała, którymi konstytuent może się od niego zacząć.

        Terminal zaczyna sam siebie, a symbol każdym terminalem, do którego
        schodzi po pierwszych córkach; pod kluczem ``None`` stoją części
        zaczynające się bez żadnego terminala, czyli te o wyprowadzeniu pustym,
        i klucz ten stoi tu nawet pusty, bo odsiew sięga po niego bez pytania.
        Odsiewa on stan, którego następna córka nie ma w swojej pozycji grafu
        od czego się zacząć (``olski/parse.py``): taki stan ciała nie dokończy,
        więc nie wejdzie do żadnego czytania. Pyta o to pozycja grafu, a nie
        stan, więc odpowiedź jest ułożona po terminalach.
        """
        if self._zaczynane is None:
            rogi: dict[str, frozenset[Word | None]] = dict.fromkeys(self.heads(), frozenset())

            def od_czego(część: Part) -> frozenset[Word | None]:
                return frozenset({część}) if isinstance(część, Word) else rogi[część.name]

            rosło = True
            while rosło:
                rosło = False
                for production in self.productions:
                    nowe: frozenset[Word | None] = frozenset()
                    for część in production.body:
                        pod = od_czego(część)
                        nowe |= pod - {None}
                        if None not in pod:
                            break
                    else:
                        #  Każda córka schodzi do niczego, więc ciało też.
                        nowe |= {None}
                    if not nowe <= rogi[production.head]:
                        rogi[production.head] |= nowe
                        rosło = True
            zebrane: dict[Word | None, set[Part]] = {None: set()}
            części = {część for production in self.productions for część in production.body}
            for część in części:
                for róg in od_czego(część):
                    zebrane.setdefault(róg, set()).add(część)
            self._zaczynane = {róg: frozenset(gdzie) for róg, gdzie in zebrane.items()}
        return self._zaczynane

    def heads(self) -> frozenset[str]:
        return frozenset(self._by_head)

    def undefined(self) -> frozenset[str]:
        """Non-terminals referred to by some production and defined by none.

        Odpowiedź stoi w gramatyce, a pyta o nią każde rozbierane zdanie,
        więc liczy się ją raz.
        """
        if self._nieokreślone is None:
            referenced = {
                part.name
                for production in self.productions
                for part in production.body
                if isinstance(part, Sym)
            }
            self._nieokreślone = frozenset(referenced | {self.start}) - self.heads()
        return self._nieokreślone

    def nieosiągalne(self) -> frozenset[str]:
        """Symbole, które gramatyka definiuje, a start do nich nie schodzi.

        Literówka w nazwie symbolu zgłasza się tylko z jednej strony:
        w referencji odmawia rozbioru (:meth:`undefined`),
        a w głowie produkcji daje symbol, do którego nie sięga żadne czytanie,
        i wtedy gramatyka wyprowadza dalej to, co wyprowadzała przedtem.
        Odpowiedź liczy się przy każdym pytaniu, bo pyta o nią przegląd,
        a nie zdanie.
        """
        osiągalne: set[str] = set()
        kolejka = [self.start]
        while kolejka:
            symbol = kolejka.pop()
            if symbol in osiągalne:
                continue
            osiągalne.add(symbol)
            kolejka.extend(
                part.name
                for production in self.for_head(symbol)
                for part in production.body
                if isinstance(part, Sym)
            )
        return self.heads() - osiągalne

    def więzy_niesprawdzane(self) -> frozenset[tuple[str, str]]:
        """Pary symbolu i cechy, o którą pyta referencja, a symbol jej nie wypuszcza.

        Cechy nieobecnej :func:`unify` nie sprawdza, więc taki więz przepuszcza
        każdy konstytuent, a literówka w nazwie cechy luzuje gramatykę,
        nie zmieniając ani jednego wiersza wydruku.
        Wypuszczaniem jest suma po produkcjach symbolu, a nie przecięcie:
        jedna produkcja niesie cechę, której druga nie niesie,
        i tym właśnie różni się forma odmienna od nieodmiennej.

        Więzu na terminalu to nie obejmuje: cechy formy przychodzą z morfologii,
        a nie z produkcji, więc inwentarz ich nazw podaje formalizmowi wołający
        (:meth:`więzy_terminali_niesprawdzane`).
        """
        wypuszczane: dict[str, set[str]] = {}
        for production in self.productions:
            wypuszczane.setdefault(production.head, set()).update(
                name for name, _ in production.features
            )
        return frozenset(
            (part.name, name)
            for production in self.productions
            for part in production.body
            if isinstance(part, Sym)
            for name, _ in part.constraints
            if name not in wypuszczane.get(part.name, ())
        )

    def wypuszczane_bez_wiązania(self) -> frozenset[tuple[str, str]]:
        """Pary symbolu i cechy wypuszczanej zmienną, której nie wiąże ani jedna córka.

        Taka cecha nie wychodzi z konstytuenta nigdy:
        zmienną wiąże tylko więz na córce (:func:`unify`),
        a nierozwiązanej :func:`features_of` nie wypuszcza, więc deklaracja milczy.
        Literówka w nazwie zmiennej zgłasza się przez to tutaj,
        tak jak literówka w nazwie cechy zgłasza się w :meth:`więzy_niesprawdzane`.
        """
        martwe = set()
        for production in self.productions:
            wiązane = {
                spec.name
                for part in production.body
                for _name, spec in part.constraints
                if isinstance(spec, Var)
            }
            martwe.update(
                (production.head, name)
                for name, spec in production.features
                if isinstance(spec, Var) and spec.name not in wiązane
            )
        return frozenset(martwe)

    def nie_wypuszczane_bez_żądania(self) -> frozenset[tuple[str, str]]:
        """Wpisy :attr:`nie_wypuszczane`, których nie żąda od głowy żadna produkcja.

        Taki wpis zatrzymuje cechę, która i bez niego z konstytuenta nie wychodzi,
        więc mówi o gramatyce coś, czego w niej nie ma;
        zostaje po produkcji zdjętej albo przemianowanej i cichnie tak samo,
        jak cichnie więz na cechę, której nikt nie wypuszcza
        (:meth:`więzy_niesprawdzane`).
        """
        żądane = {
            (production.head, name)
            for production in self.productions
            if production.body
            for name, _spec in production.body[production.głowa].constraints
        }
        return frozenset(
            (symbol, cecha)
            for symbol, cechy in self.nie_wypuszczane.items()
            for cecha in cechy
            if (symbol, cecha) not in żądane
        )

    def więzy_terminali_niesprawdzane(self, cechy: Collection[str]) -> frozenset[tuple[str, str]]:
        """Pary części mowy i cechy, o którą pyta terminal, a inwentarz jej nie zna.

        Cecha o nazwie spoza inwentarza nie przychodzi z żadnej formy, więc więz
        na nią przepuszcza każdą i literówka luzuje gramatykę, nie zmieniając ani
        jednego wiersza wydruku — tak samo jak w :meth:`więzy_niesprawdzane`,
        tylko że tam nazwy pilnuje sama gramatyka, a tu morfologia, o której ten
        formalizm nie wie nic. Inwentarz przychodzi więc argumentem od
        wołającego, który zna oba: cechy formy zamyka ``VALUES``
        w ``olski/morph.py``.

        Żądanie samej obecności (:attr:`Word.niesione`) idzie tą samą drogą,
        bo nazywa cechę tego samego inwentarza.
        """
        return frozenset(
            ("|".join(sorted(part.pos)), cecha)
            for production in self.productions
            for part in production.body
            if isinstance(part, Word)
            for cecha in {name for name, _spec in part.constraints} | set(part.niesione or ())
            if cecha not in cechy
        )

    def __len__(self) -> int:
        return len(self.productions)


# --------------------------------------------------------------------------- #
# Unification
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Env:
    """Variable bindings, immutable so that chart items can be hashed."""

    bindings: frozenset[tuple[str, frozenset[str]]] = frozenset()

    def get(self, name: str) -> frozenset[str] | None:
        for bound, values in self.bindings:
            if bound == name:
                return values
        return None

    def bind(self, name: str, values: frozenset[str]) -> Env:
        kept = frozenset((n, v) for n, v in self.bindings if n != name)
        return Env(kept | {(name, values)})

    def resolve(self, spec: Spec) -> frozenset[str] | None:
        """The values a spec stands for, or None if a variable is still free."""
        return self.get(spec.name) if isinstance(spec, Var) else spec


EMPTY = Env()


def unify(
    constraints: tuple[tuple[str, Spec], ...],
    features: dict[str, frozenset[str]],
    env: Env,
) -> Env | None:
    """Match constraints against a constituent's features.

    Returns the extended bindings, or None if some feature's values do not
    intersect — which is what disagreement looks like from here.

    A feature the constituent does not carry cannot disagree, so it is skipped
    rather than failed: an uninflected part of speech is not in violation of an
    agreement it takes no part in. A terminal demanding that a form carry the
    feature at all says so outside this function, in ``Word.niesione``.
    """
    for name, spec in constraints:
        available = features.get(name)
        if not available:
            continue
        if isinstance(spec, Var):
            bound = env.get(spec.name)
            merged = available if bound is None else bound & available
            if not merged:
                return None
            env = env.bind(spec.name, merged)
        else:
            if not (spec & available):
                return None
    return env


def bierze(
    terminal: Word,
    pos: str,
    lemma: str,
    lematy: frozenset[str],
    features: dict[str, frozenset[str]],
    env: Env,
) -> Env | None:
    """Czy terminal bierze to czytanie formy, i z jakimi wiązaniami.

    Warunek na czytanie stoi tu raz, a pytają o niego dwie rzeczy. Rozbiór pyta
    ze środowiskiem, które przyszło od rodzeństwa, a :meth:`Grammar.licencjonuje`
    pyta z ``EMPTY``, żeby odpowiedź nie zależała od zdania, w którym forma
    stanęła.

    ``lemma`` jest lematem tego czytania, a ``lematy`` lematami całej formy, czyli
    tym, o co pyta :attr:`Word.bez_lematów_formy`. Oba przychodzą argumentem, żeby
    warunek został w jednej kopii dla każdego, kto go woła. Odpowiedź od zdania nie
    zależy przez to dalej: lematy formy są własnością formy, a nie jej miejsca.
    """
    if pos not in terminal.pos:
        return None
    if terminal.lemmas is not None and lemma not in terminal.lemmas:
        return None
    if terminal.bez_lematów is not None and lemma in terminal.bez_lematów:
        return None
    if terminal.bez_lematów_formy is not None and terminal.bez_lematów_formy & lematy:
        return None
    if terminal.niesione is not None and any(
        not features.get(cecha) for cecha in terminal.niesione
    ):
        return None
    return unify(terminal.constraints, features, env)


def features_of(production: Production, env: Env) -> dict[str, frozenset[str]]:
    """The features a completed constituent carries out of its production."""
    resolved: dict[str, frozenset[str]] = {}
    for name, spec in production.features:
        values = env.resolve(spec)
        if values:
            resolved[name] = values
    return resolved
