"""Zaimek, który wskazuje na dwie rzeczy naraz.

Wieloznaczność, którą liczy werdykt, kończy się na kropce:
mówi ona, ile kształtów ma jedno zdanie (``olski/werdykt/zdanie.py``).
Zaimek trzeciej osoby wychodzi poza tę granicę,
bo rzecz, na którą wskazuje, nazywa czasem dopiero zdanie wcześniejsze,
a rozbiór zdania z zaimkiem o tamtym zdaniu nic nie wie.
Werdykt nad `Są one czerwone.` jest przez to ten sam po `Widzimy pole maków.`
i po `Maki rosną w garnkach.`,
choć po pierwszym z nich czytelnik ma jedną rzecz do wyboru, a po drugim dwie.
Umowa olskiego jest o tekście właśnie z tego powodu
(docs/roadmap.md#podzbiór-jest-umową-a-nie-zasięgiem),
a ta warstwa jest tym kawałkiem umowy, którego rozbiór jednego zdania nie obejmuje.

Zaimek dostaje zgłoszenie wtedy, gdy zdanie obok nazywa dwie rzeczy albo więcej,
a każda z nich zgadza się z nim liczbą i rodzajem.
Co to znalezisko mówi autorowi i jakie zaimki bierze, trzyma
docs/subset.md#zaimek-wskazujący-na-dwie-rzeczy-jest-drugim-znaleziskiem.
Tutaj stoją trzy warunki, których z kodu nie widać, cena każdego z nich
oraz rozszerzenie, które czeka za flagą.

**Rzecz nazywa najszersza grupa imienna, a nie każdy rzeczownik pod nią.**
`duże pole maków` nazywa pole, a `maków` jest w nim określeniem.
Bez tego zawężenia kandydatów jest tylu, ile zdanie ma rzeczowników:
`Ogrodnik ogląda pole maków w doniczce bratków.` nazywa dwie rzeczy,
a wydałoby czterech kandydatów, wśród nich `maków` i `bratków`,
więc `Są one czerwone.` dostałoby po nim zgłoszenie.
Tu widać, czego ta warstwa żąda od rozbioru:
morfologia mówi, że `pole` i `maków` są rzeczownikami,
a która z tych dwóch form jest głową grupy, mówi dopiero drzewo.

**Rzeczy podaje pierwszy kawałek tekstu przed zaimkiem, który cokolwiek nazywa.**
Kawałkiem jest zdanie składowe: najpierw własne, w części stojącej przed zaimkiem,
potem składowe stojące przed nim w tym samym zdaniu, jedno po drugim wstecz,
a na końcu zdanie obok.
Kawałek własnego zdania rozstrzyga milczeniem, a nie listą rzeczy,
i to jest wstrzymanie się nad zaimkiem rozstrzygniętym na miejscu:
`Pierwsze ma jedno odczytanie, więc autor nie ma w nim czego wybierać.`
nie odsyła czytelnika do zdania obok, bo `autor` stoi przed `nim` i zgadza się z nim,
a sięganie dalej byłoby zgadywaniem, którego czytelnik nie wykonuje.
Wstrzymanie się jest tu odpowiedzią pełnoprawną
(docs/linter.md#abstention-is-allowed) i płaci się je milczeniem:
wśród zdjętych zgłoszeń jest `Olski go nie czyta i o jego polszczyźnie milczy.`,
gdzie kandydatem miejscowym jest sam podmiot zdania,
a rzecz podejmowana stoi w zdaniu obok.
Zawężenia, po którym `Olski` przestaje być kandydatem, nikt nie napisał.

**Granicą sięgania wstecz jest zdanie obok, a nie akapit.**
Bierzemy ją stamtąd, skąd bierze ją druga strona:
``olski/skład/opowieść.py`` opuszcza podmiot tylko wtedy,
gdy o rzeczy była mowa w zdaniu obok.
Kandydaci z całego akapitu byliby przez to szersi niż to,
co druga strona uznaje za rzecz podaną czytelnikowi.

Wszystkie trzy warunki mylą się w jedną stronę: zdejmują kandydatów,
a nie dokładają ich, i tak samo myli się zdanie obok,
którego gramatyka nie wyprowadza wcale.
Na tej asymetrii stoi decyzja o zaimku bez ani jednego kandydata.

**Za flagą ``w_zdaniu`` kawałek własnego zdania wydaje rzeczy zamiast milczeć.**
Zaimek dostaje wtedy zgłoszenie i tam, gdzie dwie rzeczy nazywa składowe obok —
`Pies gonił kota, a on uciekł.` —
i tam, gdzie nazywa je własne składowe zaimka dzierżawczego —
`Jan poprosił Piotra o jego samochód.`
Rozszerzenie stoi za flagą, bo sądy czytelnika go nie awansowały:
przeczytane trafienia nad NKJP są w większości fałszywe
(docs/subset.md#rzeczy-z-tego-samego-zdania-czekają-za-flagą).
Zgłoszenie spod flagi nosi własną nazwę
(:data:`olski.werdykt.ODNIESIENIE_W_ZDANIU`), więc baza sądów ocenia dwie reguły
osobno, a kod wyjścia tej nazwy nie liczy;
przebieg, który tych trafień żąda, jest sondą oceniającą (``harness/sądy.py``).
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field

from olski.document import Document
from olski.morph import Reading, zgadza
from olski.parse import Leaf, Node, Result, Tree, liście, zakresy
from olski.subset import DEKLARACJA

#: Część mowy zaimka trzeciej osoby: `on`, `ona`, `ono`, `oni`, `one`
#: wraz z każdą formą przypadkową — `go`, `jej`, `nim`, `nich` i resztą.
#: Czemu zaimka wskazującego tu nie ma, mówi
#: docs/subset.md#zaimek-wskazujący-na-dwie-rzeczy-jest-drugim-znaleziskiem.
ZAIMEK = "ppron3"

#: Części mowy, którymi tekst nazywa rzecz. Zaimka wśród nich nie ma i nie jest to
#: przeoczenie: zaimek rzeczy nie nazywa, tylko na nią wskazuje, więc policzony jako
#: kandydat odsyłałby czytelnika do jeszcze wcześniejszego zdania.
IMIENNE = frozenset({"subst", "depr"})

#: Cechy, którymi zaimek zgadza się z rzeczą (:func:`olski.morph.zgadza`).
#: Przypadka wśród nich nie ma, bo przypadka żąda pozycja, w której zaimek stoi,
#: a nie rzecz, którą on podejmuje.
ZGODNE = ("number", "gender")


@dataclass(frozen=True)
class Odniesienie:
    """Zaimek wraz z rzeczami, na które może wskazywać.

    Rzeczy nazwane są formą, tak jak :class:`olski.parse.Przyłączenie` nazywa
    gospodarzy: autor ma je odszukać w tekście, a stoją tam właśnie w tej formie.
    """

    #: Zaimek tak, jak stoi w zdaniu.
    zaimek: str
    #: Formy rzeczy, które się z nim zgadzają, ustawione tak jak w kawałku,
    #: z którego wyszły.
    rzeczy: tuple[str, ...]
    #: Czy rzeczy stoją w zdaniu zaimka, czy w zdaniu obok. Rozdziela to dwie
    #: reguły, bo pierwszą z nich wydaje samo rozszerzenie za flagą, a baza sądów
    #: ocenia je osobno (:data:`olski.werdykt.ODNIESIENIE_W_ZDANIU`).
    w_zdaniu: bool


@dataclass
class _Rzecz:
    """Rzecz nazwana w kawałku tekstu: forma, którą się ją wypisuje, i czym ona jest.

    Lematy zbierają się dlatego, że jedna rzecz nazwana dwa razy jest jedną rzeczą:
    `Maki` i `maków` w jednym kawałku nie stawiają czytelnika przed wyborem,
    a policzone osobno dałyby zgłoszenie nad każdym zdaniem,
    które o czymś mówi dwa razy.
    """

    forma: str
    lematy: set[str]
    odczytania: list[Reading] = field(default_factory=list)


def niejasne_odniesienia(
    text: str, wyniki: Sequence[Result], w_zdaniu: bool = False
) -> list[tuple[Odniesienie, ...]]:
    """Zgłoszenia o zaimkach, po jednej krotce na zdanie i w kolejności zdań.

    Tekstem, a nie samym podziałem, bo tak bierze go druga warstwa tekstowa
    (:func:`olski.rozstrzyganie.sąsiedztwa`), i tak samo buduje sobie dokument.
    Zdanie obok wskazuje ostatni z numerów, które podaje
    :attr:`olski.document.Document.wcześniejsze`.

    ``w_zdaniu`` jest flagą rozszerzenia, którego sądy czytelnika nie awansowały;
    co za nią stoi i czemu domyślnie milczy, trzyma docstring modułu.

    Rozbiór, a nie werdykt nad nim: i zaimki, i kandydatów wyjmuje się z czytań,
    a werdykt czyta stąd (:func:`olski.werdykt.nad_tekstem`), więc import
    w tamtą stronę zamykałby krąg.
    """
    return [
        _zgłoszenia(wynik, wyniki[poprzednie[-1]] if poprzednie else None, w_zdaniu)
        for wynik, poprzednie in zip(wyniki, Document(text).wcześniejsze, strict=True)
    ]


def _zgłoszenia(wynik: Result, obok: Result | None, w_zdaniu: bool) -> tuple[Odniesienie, ...]:
    """Zgłoszenia o zaimkach jednego zdania; pusta krotka jest milczeniem.

    Zdanie bez zaimka wychodzi stąd po jednym przejściu po liściach, bo takich
    zdań jest większość, a listy niżej kosztują przejście po drzewie.
    """
    zaimki = _zaimki(wynik.readings)
    if not zaimki:
        return ()
    własne = list(_głowy(wynik.readings))
    granice = _granice(wynik.readings)
    obce = _rzeczy(_głowy(obok.readings)) if obok is not None else []
    zgłoszenia = (_odniesienie(zaimek, własne, granice, obce, w_zdaniu) for zaimek in zaimki)
    return tuple(zgłoszenie for zgłoszenie in zgłoszenia if zgłoszenie is not None)


def _odniesienie(
    zaimek: Leaf,
    własne: Sequence[Leaf],
    granice: Sequence[int],
    obce: Sequence[_Rzecz],
    w_zdaniu: bool,
) -> Odniesienie | None:
    """Zgłoszenie o tym zaimku, albo nic, gdy rzecz jest jedna albo nie ma żadnej.

    Rzeczy podaje pierwszy kawałek przed zaimkiem, który nazywa cokolwiek zgodnego;
    kawałki idą od najbliższego, a zdanie obok jest ostatnim z nich.
    Kawałek własnego zdania rozstrzyga milczeniem albo listą rzeczy,
    i tym jednym różni się rozszerzenie od reguły dzisiejszej;
    czemu rozstrzyga pierwszy, a nie ich suma, trzyma docstring modułu.
    """
    odczytania = [r for r in zaimek.odczytania if r.tag.pos == ZAIMEK]
    for zakres in _kawałki(granice, zaimek.span[0]):
        rzeczy = _rzeczy(g for g in własne if zakres[0] <= g.span[0] < zakres[1])
        if zgodne := _zgodne(odczytania, rzeczy):
            return _zgłoszenie(zaimek, zgodne, w_zdaniu=True) if w_zdaniu else None
    return _zgłoszenie(zaimek, _zgodne(odczytania, obce), w_zdaniu=False)


def _zgodne(odczytania: Sequence[Reading], rzeczy: Iterable[_Rzecz]) -> list[_Rzecz]:
    """Te z rzeczy, które zgadzają się z zaimkiem liczbą i rodzajem."""
    return [rzecz for rzecz in rzeczy if zgadza(odczytania, rzecz.odczytania, ZGODNE)]


def _zgłoszenie(zaimek: Leaf, zgodne: Sequence[_Rzecz], w_zdaniu: bool) -> Odniesienie | None:
    """Zgłoszenie o wyborze, albo nic: rzecz jedna wyboru czytelnikowi nie stawia."""
    if len(zgodne) < 2:
        return None
    return Odniesienie(zaimek.segment.form, tuple(rzecz.forma for rzecz in zgodne), w_zdaniu)


def _granice(czytania: Sequence[Node]) -> list[int]:
    """Początki zdań składowych tego zdania, w porządku zdania.

    Te same, którymi werdykt dzieli zdanie na streszczenia
    (:func:`olski.parse.zakresy`). Zdanie wieloznaczne bywa podzielone w każdym
    czytaniu inaczej, więc granice idą ze wszystkich naraz i kawałek jest przez
    to najmniejszy, jaki którekolwiek czytanie wyznacza; kandydatów ubywa przez
    to tak samo jak przy trzech warunkach wyżej.
    """
    return sorted(
        {zakres[0] for czytanie in czytania for zakres in zakresy(czytanie, DEKLARACJA.składowe)}
    )


def _kawałki(granice: Sequence[int], początek: int) -> list[tuple[int, int]]:
    """Kawałki zdania stojące przed tym miejscem, od najbliższego.

    Ostatnią granicą jest samo to miejsce, bo rzecz nazwana za zaimkiem nie jest
    rzeczą, którą on podejmuje.
    """
    cięcia = [*(granica for granica in granice if granica <= początek), początek]
    return [(cięcia[i], cięcia[i + 1]) for i in reversed(range(len(cięcia) - 1))]


def _rzeczy(głowy: Iterable[Leaf]) -> list[_Rzecz]:
    """Rzeczy nazwane przez te głowy, każda raz i w kolejności zdania.

    Głów jest kilka nad jedną formą tam, gdzie zdanie jest wieloznaczne,
    i wtedy głowa grupy imiennej bywa w każdym czytaniu inna;
    bierzemy je wszystkie, bo czytelnik też ma je wszystkie do wyboru.
    """
    rzeczy: list[_Rzecz] = []
    for głowa in głowy:
        odczytania = _imienne(głowa)
        lematy = {odczytanie.lemma for odczytanie in odczytania}
        for rzecz in rzeczy:
            if rzecz.lematy & lematy:
                rzecz.lematy |= lematy
                rzecz.odczytania += odczytania
                break
        else:
            rzeczy.append(_Rzecz(głowa.segment.form, set(lematy), list(odczytania)))
    return rzeczy


def _głowy(drzewa: Iterable[Tree]) -> Iterator[Leaf]:
    """Głowy najszerszych grup imiennych, w kolejności zdania.

    Bierze i listę czytań, i córki węzła, bo zejście jest w obu wypadkach to samo.
    Najszerszych, bo rzecz nazywa cała grupa, a nie rzeczownik pod nią;
    wywód trzyma docstring modułu.
    Głowa bez odczytania imiennego odpada tutaj, a nie u pytającego,
    bo zgodność liczy się nad odczytaniami imiennymi i nad żadnymi innymi
    (:func:`olski.morph.zgadza`), więc taka głowa nie zgodziłaby się z niczym.
    """
    for drzewo in drzewa:
        if isinstance(drzewo, Leaf):
            continue
        if drzewo.label == DEKLARACJA.grupa_imienna:
            głowa = drzewo.liść_głowy()
            if _imienne(głowa):
                yield głowa
            continue
        yield from _głowy(drzewo.children)


def _imienne(liść: Leaf) -> list[Reading]:
    return [odczytanie for odczytanie in liść.odczytania if odczytanie.tag.pos in IMIENNE]


def _zaimki(czytania: Sequence[Node]) -> list[Leaf]:
    """Zaimki tych czytań, każdy raz i w kolejności zdania.

    Kluczem jest forma, a nie miejsce:
    zaimek powtórzony w jednym zdaniu wskazuje na to samo,
    więc drugi wiersz nie mówiłby nic ponad ten nad sobą.
    Kolejność jest kolejnością zdania, a nie kolejnością zbioru,
    bo dwa przebiegi mają wypisywać to samo.
    """
    znalezione: dict[str, Leaf] = {}
    for czytanie in czytania:
        for liść in liście(czytanie):
            if any(odczytanie.tag.pos == ZAIMEK for odczytanie in liść.odczytania):
                znalezione.setdefault(liść.segment.form, liść)
    return sorted(znalezione.values(), key=lambda liść: liść.span)
