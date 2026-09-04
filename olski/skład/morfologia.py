"""Formy, czyli Morfeusz czytany w drugą stronę.

Analiza odwzorowuje formę na tagi, synteza lemat wraz z tagiem na formę,
i to drugie jest tym, po co ten moduł jest.
Zapleczem obu jest ten sam SGJP, więc odmiana bierze się tu ze słownika,
a nie ze zgadywania wzorca po zakończeniu wyrazu.
``docs/prior-art.md`` mówi, czym ten słownik jest i czemu przeważył.

Zgodność nie jest tu sprawdzana, tylko liczona.
Parsowanie godzi ze sobą dwie wiązki cech, z których każda niesie kilka wartości,
a synteza żąda jednej formy po tagu, który już stoi rozstrzygnięty.
Cała trudność, dla której olski istnieje, przy tym kierunku nie powstaje.

Trudność, która przy nim powstaje, jest inna i jest w danych.
Tag rozstrzygnięty wskazuje kilka form, a wybór między nimi jest wyborem,
którego autor drzewa nie zrobił i nie ma gdzie zrobić.
Klasy tego wyboru schodzą stąd, każda inaczej.
Kwalifikator, którym słownik odsyła formę poza rejestr, zdejmuje ją
i tę klasę zdejmuje ``olski/rejestr.py``, wraz z analizą, która tę samą listę
czyta kosztem zamiast odsiewem.
Leksem, którego lemat nie wskazuje, zostaje wyborem i jest wyborem autora,
więc ma miejsce, w którym się go pisze: ``olski/skład/leksemy.py``,
a nienapisany zgłasza się wyjątkiem, zamiast zapaść tutaj po cichu.
"""

from __future__ import annotations

import functools

from olski.morph import generuj, tag
from olski.rejestr import poza_rejestrem
from olski.skład.leksemy import leksem


class BrakFormy(Exception):
    """Morfologia takiej formy nie ma.

    Wyjątek, a nie forma zgadnięta albo pominięta,
    bo to jest błąd kompilacji: drzewo żąda czegoś, czego polszczyzna nie odmienia.
    """


class WieleLeksemów(Exception):
    """Pod tą nazwą stoi kilka leksemów i nie zgadzają się one co do odpowiedzi.

    Usterka odwrotna do ``BrakFormy`` i zgłaszana z tego samego powodu:
    kompilator ma tu do wyboru dwie poprawne polszczyzny o różnym znaczeniu,
    a wybór między znaczeniami należy do autora drzewa.

    Treść zgłoszenia stoi tutaj, bo pytają o nią dwa miejsca naraz,
    a odpowiedź jest w obu ta sama: leksem wraz z tym, co z niego wychodzi.
    Tyle wystarcza, żeby wpisać rozstrzygnięcie do ``olski/skład/leksemy.py``,
    i to jest jedyne, po co to zgłoszenie jest czytane.
    """

    def __init__(self, pytanie: str, wedle_leksemu: dict[str, set[str]]) -> None:
        super().__init__(
            f"{pytanie}: leksemy się nie zgadzają, bo "
            + ", ".join(
                f"{identyfikator} daje {', '.join(sorted(dane))}"
                for identyfikator, dane in wedle_leksemu.items()
            )
            + "; który z nich, mówi olski/skład/leksemy.py"
        )


@functools.lru_cache(maxsize=4096)
def paradygmat(nazwa: str, pos: str) -> tuple[tuple[str, frozenset, str], ...]:
    """Formy nazwy w danej części mowy, które ten rejestr bierze, wraz z cechami i leksemem.

    Liczone raz na nazwę, bo linearyzacja pyta o tę samą nazwę tyle razy,
    ile stoi ona w drzewie, a Morfeusz i tak wydaje cały paradygmat naraz.

    Nazwa idzie do słownika przez ``leksem``, więc nazwa wybrana w tym repozytorium
    pyta o jeden leksem, a lemat pyta o wszystkie, które słownik pod nim trzyma.
    Leksem wychodzi stąd przy każdej formie, bo wybór między leksemami zapada wyżej,
    a rozpoznać go da się tylko po tym polu: tag obu bywa ten sam.

    Odsianie kwalifikatorem stoi tutaj, a nie przy wyborze niżej,
    bo forma odesłana poza rejestr nie jest wyborem gorszym, tylko żadnym:
    ``odmień`` nie ma jej po co widzieć, a ``rodzaj_rzeczownika`` tym bardziej.
    """
    formy = []
    for forma, identyfikator, surowy, _nazwy, kwalifikatory in generuj(leksem(nazwa)):
        czytanie = tag(surowy)
        if czytanie.pos == pos and not poza_rejestrem(kwalifikatory):
            formy.append((forma, czytanie.features, identyfikator))
    return tuple(formy)


def odmień(nazwa: str, pos: str, **żądane: str) -> str:
    """Forma nazwy, która spełnia żądanie postawione cechami.

    Cechy, której cały paradygmat nie ma, żądanie nie dotyczy.
    Żądanie jest tu kryterium wyboru, a nad kolumną o jednej wartości
    kryterium nie wybiera niczego, więc odsianie po niej byłoby odsianiem wszystkiego.
    Widać to na przysłówku: ``nagle`` ma stopień i ``wkrótce`` go nie ma,
    a żądać stopnia równego trzeba od obu, bo o odmienności rozstrzyga leksem.
    Cecha, którą paradygmat ma, a której ta forma nie niesie, żądania nadal nie spełnia,
    i to jest różnica między brakiem wyboru a wyborem chybionym.

    Gdzie żądaniu odpowiadają leksemy zgodne co do jakiejś formy, bierze tę formę.
    Zgoda leksemów jest tu odpowiedzią, a nie kolejność, w jakiej słownik je wydaje:
    ``dziób`` odesłany do żeglarstwa ma w dopełniaczu ``dzioba`` obok ``dziobu``,
    a ten bez kwalifikatora ``dzióba`` obok ``dzioba``,
    więc ``dzioba`` jest dobre pod oba i autor nie ma tu o czym rozstrzygać.

    Gdzie leksemy nie zgadzają się co do żadnej formy, zgłasza ``WieleLeksemów``,
    bo wtedy każda odpowiedź mówi co innego:
    ``oczy`` obok ``oka`` albo ``stoi`` obok ``stanie``, czyli teraz obok potem.
    Który leksem, jest wtedy pytaniem do autora i odpowiada na nie
    ``olski/skład/leksemy.py``.
    Kosztem tego jest cisza tam, gdzie leksemy różnią się poza żądaną komórką,
    czyli w miejscu, w którym autor o żaden wybór nie pytał.

    Gdzie zostaje kilka form jednego leksemu, bierze pierwszą.
    Wybór ten zostaje jedynym miejscem, w którym kompilator wybiera i nie mówi o tym,
    a reszta wyborów stoi w drzewie, które napisał autor.
    Wybiera przy tym z form, które ``paradygmat`` już przepuścił,
    więc forma odesłana poza rejestr nie stoi tu ani pierwsza, ani żadna:
    ``któren`` i ``zgasnęła`` wychodziły stąd, dopóki kwalifikatora nikt nie czytał.
    """
    formy = paradygmat(nazwa, pos)
    obecne = {cecha for _forma, cechy, _identyfikator in formy for cecha, _wartości in cechy}
    kryterium = {cecha: wartość for cecha, wartość in żądane.items() if cecha in obecne}
    # Kolejność trzyma lista, a nie zbiór, bo pierwsza forma jednego leksemu
    # jest tu odpowiedzią i musi być tą, którą słownik wydał pierwszą.
    trafienia: list[str] = []
    wedle_leksemu: dict[str, set[str]] = {}
    for forma, cechy, identyfikator in formy:
        if _spełnia(dict(cechy), kryterium):
            trafienia.append(forma)
            wedle_leksemu.setdefault(identyfikator, set()).add(forma)
    if not trafienia:
        raise BrakFormy(f"{nazwa} ({pos}) nie ma formy {żądane}")
    zgodne = set.intersection(*wedle_leksemu.values())
    if not zgodne:
        raise WieleLeksemów(f"{nazwa} ({pos}) w formie {żądane}", wedle_leksemu)
    return next(forma for forma in trafienia if forma in zgodne)


def _spełnia(cechy: dict[str, frozenset[str]], żądane: dict[str, str]) -> bool:
    """Czy forma niesie każdą żądaną wartość.

    Cecha, której forma nie niesie, żądania nie spełnia, i to jest tu zamierzone.
    Przy analizie brak cechy znaczy, że nie ma czym się nie zgodzić,
    a przy syntezie znaczy, że nie ma czego wypisać.
    """
    return all(wartość in cechy.get(nazwa, frozenset()) for nazwa, wartość in żądane.items())


def _rodzaje(nazwa: str, liczba: str) -> dict[str, set[str]]:
    """Rodzaje, które leksemy tej nazwy niosą w mianowniku tej liczby."""
    rodzaje: dict[str, set[str]] = {}
    for _forma, cechy, identyfikator in paradygmat(nazwa, "subst"):
        słownik = dict(cechy)
        if "nom" in słownik.get("case", ()) and liczba in słownik.get("number", ()):
            # Jeden leksem wydaje mianownik kilka razy, gdy rodzajów ma kilka,
            # więc rodzaj leksemu jest sumą jego wierszy, a nie pierwszym z nich.
            rodzaje.setdefault(identyfikator, set()).update(słownik["gender"])
    return rodzaje


@functools.lru_cache(maxsize=4096)
def rodzaj_rzeczownika(nazwa: str) -> str:
    """Rodzaj wzięty z mianownika tej liczby, którą ten rzeczownik ma.

    Rodzaj rzeczownika jest leksykalny: autor go nie wybiera, a zgodność go żąda,
    więc nie stoi w drzewie, tylko przychodzi stąd.

    Liczba pojedyncza idzie pierwsza i jest odpowiedzią wszędzie tam,
    gdzie rzeczownik ma obie, a mnoga jest tu dla tych, które pojedynczej nie mają:
    `drzwi` i `Włochy` stoją tylko w mnogiej i rodzaj niosą tam, gdzie stoją,
    więc pytanie o samą pojedynczą odbierałoby im każdą pozycję,
    z której wychodzi czasownik albo człon koordynacji.

    Rodzaj wychodzi stąd tak, jak forma wychodzi z ``odmień``, i z tego samego
    powodu: zgoda leksemów jest odpowiedzią, a brak zgody jest pytaniem do autora.
    Pod napisem ``potwór`` stoją dwa leksemy i jeden z nich jest zwierzęciem,
    a drugi zwierzęciem albo osobą, więc zwierzę jest tym, co oba przyjmują.
    Zostaje po tym rodzaj, który sam słownik wypisuje dwiema wartościami,
    i tu ta funkcja bierze pierwszą alfabetycznie, nie mówiąc o tym nigdzie.
    Tamto jest wyborem autora, a to jest słownik mówiący „albo tak, albo tak”,
    więc drugiego ``olski/skład/leksemy.py`` nie rozstrzyga.
    """
    rodzaje = _rodzaje(nazwa, "sg") or _rodzaje(nazwa, "pl")
    if not rodzaje:
        raise BrakFormy(f"{nazwa} nie ma mianownika w żadnej liczbie")
    zgodne = set.intersection(*rodzaje.values())
    if not zgodne:
        raise WieleLeksemów(f"rodzaj, który niesie {nazwa}", rodzaje)
    return sorted(zgodne)[0]
