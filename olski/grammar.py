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

from dataclasses import dataclass


@dataclass(frozen=True)
class Var:
    """A feature variable, shared between the parts of one production."""

    name: str

    def __repr__(self) -> str:
        return f"?{self.name}"


def V(name: str) -> Var:
    return Var(name)


#: What a feature may be constrained to: a variable, or a set of literal values.
Spec = Var | frozenset


def _spec(value) -> Spec:
    if isinstance(value, Var):
        return value
    if isinstance(value, str):
        return frozenset(value.split("."))
    return frozenset(value)


def _constraints(features: dict) -> frozenset[tuple[str, Spec]]:
    return frozenset((name, _spec(value)) for name, value in features.items())


@dataclass(frozen=True)
class Sym:
    """A reference to a non-terminal, with constraints on its features."""

    name: str
    constraints: frozenset[tuple[str, Spec]] = frozenset()

    def __repr__(self) -> str:
        if not self.constraints:
            return self.name
        inner = ", ".join(f"{n}={v!r}" for n, v in sorted(self.constraints, key=lambda c: c[0]))
        return f"{self.name}[{inner}]"


@dataclass(frozen=True)
class Word:
    """A terminal: one morphological reading, constrained by tag and lemma."""

    pos: frozenset[str]
    constraints: frozenset[tuple[str, Spec]] = frozenset()
    lemmas: frozenset[str] | None = None
    #: Lematy, których ten terminal nie bierze, czyli warunek ujemny. Stoi na
    #: lemacie, bo lemat jest osobnym testem w :func:`bierze`, a nie żądaniem
    #: wobec cech, których przecięcie negacji nie zna; docs/subset.md wywodzi to
    #: pod jedynym warunkiem tego rodzaju, jaki gramatyka stawia.
    bez_lematów: frozenset[str] | None = None
    #: Cechy, które forma ma nieść, żeby ten terminal ją wziął, czyli żądanie
    #: samej obecności: `word("adv", niesie="degree")` bierze `bardzo`, a `tu` nie.
    #: Stoi obok testu na lemat, a nie w :func:`unify`, bo cechy nieobecnej
    #: unifikacja nie sprawdza, więc wypisanie wszystkich wartości znaczy tam tyle,
    #: co milczenie; docs/design-notes.md wywodzi to razem z warunkiem ujemnym
    #: wyżej, bo oba pytają o formę, a nie o zgodność.
    niesione: frozenset[str] | None = None

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
    #: Features of the resulting constituent, usually variables shared with the
    #: body so that a phrase inherits the number and case of its head word.
    features: frozenset[tuple[str, Spec]] = frozenset()
    #: Która z córek jest głową, czyli tą, którą ten konstytuent jest i po
    #: której nazywa go werdykt jednym słowem. ``head`` nazywa symbol, który ta
    #: produkcja definiuje, a ``głowa`` pozycję w jej ciele: jedno słowo w dwóch
    #: językach na dwie różne rzeczy. Ciało puste głowy nie ma, a zero nie
    #: nazywa w nim niczego, bo nie ma tam żadnej córki.
    głowa: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "_hasz", hash((self.head, self.body, self.features, self.głowa)))

    def __hash__(self) -> int:
        """Hasz policzony raz, bo produkcja powstaje raz i już się nie zmienia.

        Produkcja jest częścią każdego stanu tablicy Earleya,
        a stany trzyma słownik,
        więc hasz wywiedziony z pól przechodziłby całe ciało,
        a w nim cechy każdej części, raz na wpis i raz na odczyt.
        Równość zostaje ta, którą daje ``dataclass``: hasz nie jest polem.
        """
        return self._hasz

    def __repr__(self) -> str:
        return f"{self.head} → {' '.join(repr(part) for part in self.body)}"


def nt(name: str, **features) -> Sym:
    """Refer to a non-terminal: ``nt("NP", case="nom", number=V("n"))``."""
    return Sym(name=name, constraints=_constraints(features))


def word(
    pos: str,
    lemma: str | None = None,
    bez_lematu: str | None = None,
    niesie: str | None = None,
    **features,
) -> Word:
    """Match a morphological reading: ``word("subst", case=V("c"))``.

    ``pos`` may name alternatives, as in ``"fin|praet"``.
    ``bez_lematu`` names alternatives the same way and excludes them instead.
    ``niesie`` nazywa cechy, które forma ma nieść, tak samo rozdzielone kreską.
    """
    return Word(
        pos=frozenset(pos.split("|")),
        constraints=_constraints(features),
        lemmas=None if lemma is None else frozenset(lemma.split("|")),
        bez_lematów=None if bez_lematu is None else frozenset(bez_lematu.split("|")),
        niesione=None if niesie is None else frozenset(niesie.split("|")),
    )


class Grammar:
    """A set of productions, indexed by the constituent they build."""

    def __init__(self, start: str) -> None:
        self.start = start
        self.productions: list[Production] = []
        self._by_head: dict[str, list[Production]] = {}
        self._po_części_mowy: dict[str, tuple[Word, ...]] | None = None

    def rule(self, head: str, body: list[Part | Głowa], **features) -> Production:
        części, głowa = _głowa(head, body)
        return self.dopisz(
            Production(head=head, body=części, features=_constraints(features), głowa=głowa)
        )

    def dopisz(self, production: Production) -> Production:
        """Wpisz produkcję gotową, czyli wziętą z innej gramatyki.

        Tędy powstaje wariant gramatyki: sonda przepisuje produkcje do gramatyki
        uboższej takimi, jakie są. Złożona drugi raz z części gubiłaby to,
        czego ``rule`` nie przyjmuje osobnym argumentem, czyli głowę.
        """
        self.productions.append(production)
        self._by_head.setdefault(production.head, []).append(production)
        self._po_części_mowy = None
        return production

    def for_head(self, head: str) -> list[Production]:
        return self._by_head.get(head, [])

    def licencjonuje(self, pos: str, lemma: str, features: dict[str, frozenset[str]]) -> bool:
        """Czy jakikolwiek terminal tej gramatyki bierze takie czytanie formy.

        Pytanie stawiane przed rozbiorem i wyprowadzone z gramatyki, a nie
        napisane obok niej: czytanie, którego nie bierze tu żaden terminal, nie
        przejdzie przy żadnym środowisku cech, bo unifikacja tylko zawęża. Forma,
        której w ten sposób nie zostaje ani jedno czytanie, jest tym, na czym
        odrzucenie stanęło; docs/design-notes.md wywodzi, czemu warstwa mówiąca
        to samo obok gramatyki byłaby gramatyką napisaną dwa razy.
        """
        return any(
            bierze(terminal, pos, lemma, features, EMPTY) is not None
            for terminal in self._terminale_dla(pos)
        )

    def _terminale_dla(self, pos: str) -> tuple[Word, ...]:
        """Terminale, które w ogóle biorą tę część mowy.

        Pytanie o licencję pada raz na czytanie formy, a odpowiada za nie część
        mowy w większości przypadków, więc indeks stoi na niej: bez niego każde
        czytanie przechodzi przez wszystkie terminale gramatyki.
        """
        if self._po_części_mowy is None:
            indeks: dict[str, list[Word]] = {}
            for production in self.productions:
                for part in production.body:
                    if isinstance(part, Word):
                        for nazwa in part.pos:
                            indeks.setdefault(nazwa, []).append(part)
            self._po_części_mowy = {nazwa: tuple(słowa) for nazwa, słowa in indeks.items()}
        return self._po_części_mowy.get(pos, ())

    def heads(self) -> frozenset[str]:
        return frozenset(self._by_head)

    def undefined(self) -> frozenset[str]:
        """Non-terminals referred to by some production and defined by none."""
        referenced = {
            part.name
            for production in self.productions
            for part in production.body
            if isinstance(part, Sym)
        }
        return frozenset(referenced | {self.start}) - self.heads()

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
    constraints: frozenset[tuple[str, Spec]],
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
    for name, spec in sorted(constraints, key=lambda c: c[0]):
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
    features: dict[str, frozenset[str]],
    env: Env,
) -> Env | None:
    """Czy terminal bierze to czytanie formy, i z jakimi wiązaniami.

    Warunek na czytanie stoi tu raz, a pytają o niego dwie rzeczy. Rozbiór pyta
    ze środowiskiem, które przyszło od rodzeństwa, a :meth:`Grammar.licencjonuje`
    pyta z ``EMPTY``, żeby odpowiedź nie zależała od zdania, w którym forma
    stanęła.
    """
    if pos not in terminal.pos:
        return None
    if terminal.lemmas is not None and lemma not in terminal.lemmas:
        return None
    if terminal.bez_lematów is not None and lemma in terminal.bez_lematów:
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
