"""Zaimek, który wskazuje na dwie rzeczy naraz.

Wieloznaczność, którą liczy werdykt, kończy się na kropce:
mówi ona, ile kształtów ma jedno zdanie (``olski/werdykt.py``).
Zaimek trzeciej osoby wychodzi poza tę granicę,
bo rzecz, na którą wskazuje, nazwało zdanie wcześniejsze,
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
Tutaj stoją trzy warunki, których z kodu nie widać, i cena każdego z nich.

**Rzecz nazywa najszersza grupa imienna, a nie każdy rzeczownik pod nią.**
`duże pole maków` nazywa pole, a `maków` jest w nim określeniem.
Bez tego zawężenia kandydatów jest tylu, ile zdanie ma rzeczowników:
`Ogrodnik ogląda pole maków w doniczce bratków.` nazywa dwie rzeczy,
a wydałoby czterech kandydatów, wśród nich `maków` i `bratków`,
więc `Są one czerwone.` dostałoby po nim zgłoszenie.
Tu widać, czego ta warstwa żąda od rozbioru:
morfologia mówi, że `pole` i `maków` są rzeczownikami,
a która z tych dwóch form jest głową grupy, mówi dopiero drzewo.

**Granicą jest zdanie obok, a nie akapit.**
Bierzemy ją stamtąd, skąd bierze ją druga strona:
``olski/skład/opowieść.py`` opuszcza podmiot tylko wtedy,
gdy o rzeczy była mowa w zdaniu obok.
Kandydaci z całego akapitu byliby przez to szersi niż to,
co druga strona uznaje za rzecz podaną czytelnikowi.

**Zaimek rozstrzygnięty we własnym zdaniu zgłoszenia nie dostaje.**
`Pierwsze ma jedno odczytanie, więc autor nie ma w nim czego wybierać.`
nie odsyła czytelnika do zdania obok,
bo `Pierwsze` stoi przed `nim` i zgadza się z nim;
sięganie dalej byłoby zgadywaniem, którego czytelnik nie wykonuje.
Wstrzymanie się jest tu odpowiedzią pełnoprawną
(docs/linter.md#abstention-is-allowed) i płaci się je milczeniem:
nad prozą tego repozytorium zdejmuje ono więcej zgłoszeń, niż zostawia,
a wśród zdjętych jest `Olski go nie czyta i o jego polszczyźnie milczy.`,
gdzie kandydatem miejscowym jest sam podmiot zdania,
a rzecz podejmowana stoi w zdaniu obok.
Warunek zostaje mimo to, bo zdejmuje w większości trafienia chybione,
a chybione kosztuje więcej:
autor przepisuje przez nie zdanie bez powodu (docs/roadmap.md#cele).
Zawężenia, po którym `Olski` przestaje być kandydatem, nikt nie napisał.

Wszystkie trzy warunki mylą się w jedną stronę: zdejmują kandydatów,
a nie dokładają ich, i tak samo myli się zdanie obok,
którego gramatyka nie wyprowadza wcale.
Na tej asymetrii stoi decyzja o zaimku bez ani jednego kandydata.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field

from olski.document import Document
from olski.morph import Reading, zgadza
from olski.parse import Leaf, Node, Result, Tree, liście
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
    """Zaimek wraz z rzeczami, na które w zdaniu obok może wskazywać.

    Rzeczy nazwane są formą, tak jak :class:`olski.parse.Przyłączenie` nazywa
    gospodarzy: autor ma je odszukać w zdaniu obok, a stoją tam właśnie w tej formie.
    """

    #: Zaimek tak, jak stoi w zdaniu.
    zaimek: str
    #: Formy rzeczy, które się z nim zgadzają, ustawione tak jak w zdaniu obok.
    rzeczy: tuple[str, ...]


@dataclass
class _Rzecz:
    """Rzecz nazwana w zdaniu obok: forma, którą się ją wypisuje, i czym ona jest.

    Lematy zbierają się dlatego, że jedna rzecz nazwana dwa razy jest jedną rzeczą:
    `Maki` i `maków` w jednym zdaniu nie stawiają czytelnika przed wyborem,
    a policzone osobno dałyby zgłoszenie nad każdym zdaniem,
    które o czymś mówi dwa razy.
    """

    forma: str
    lematy: set[str]
    odczytania: list[Reading] = field(default_factory=list)


def niejasne_odniesienia(text: str, wyniki: Sequence[Result]) -> list[tuple[Odniesienie, ...]]:
    """Zgłoszenia o zaimkach, po jednej krotce na zdanie i w kolejności zdań.

    Tekstem, a nie samym podziałem, bo tak bierze go druga warstwa tekstowa
    (:func:`olski.rozstrzyganie.sąsiedztwa`), i tak samo buduje sobie dokument.
    Zdanie obok wskazuje ostatni z numerów, które podaje
    :attr:`olski.document.Document.wcześniejsze`.

    Rozbiór, a nie werdykt nad nim: i zaimki, i kandydatów wyjmuje się z czytań,
    a werdykt czyta stąd (:func:`olski.werdykt.nad_tekstem`), więc import
    w tamtą stronę zamykałby krąg.
    """
    return [
        _zgłoszenia(wynik, wyniki[poprzednie[-1]] if poprzednie else None)
        for wynik, poprzednie in zip(wyniki, Document(text).wcześniejsze, strict=True)
    ]


def _zgłoszenia(wynik: Result, obok: Result | None) -> tuple[Odniesienie, ...]:
    """Zgłoszenia o zaimkach jednego zdania; pusta krotka jest milczeniem.

    Zdanie bez zaimka wychodzi stąd po jednym przejściu po liściach, bo takich
    zdań jest większość, a obie listy niżej kosztują przejście po drzewie.
    """
    zaimki = _zaimki(wynik.readings)
    if obok is None or not zaimki:
        return ()
    rzeczy = _rzeczy(obok.readings)
    własne = list(_głowy(wynik.readings))
    zgłoszenia = []
    for zaimek in zaimki:
        odczytania = [r for r in zaimek.odczytania if r.tag.pos == ZAIMEK]
        if any(
            głowa.span[1] <= zaimek.span[0] and zgadza(odczytania, _imienne(głowa), ZGODNE)
            for głowa in własne
        ):
            continue
        zgodne = [rzecz for rzecz in rzeczy if zgadza(odczytania, rzecz.odczytania, ZGODNE)]
        if len(zgodne) > 1:
            zgłoszenia.append(
                Odniesienie(zaimek.segment.form, tuple(rzecz.forma for rzecz in zgodne))
            )
    return tuple(zgłoszenia)


def _rzeczy(czytania: Sequence[Node]) -> list[_Rzecz]:
    """Rzeczy nazwane w tych czytaniach, każda raz i w kolejności zdania.

    Czytań jest kilka tam, gdzie zdanie obok jest wieloznaczne,
    i wtedy głowa grupy imiennej bywa w każdym z nich inna;
    bierzemy je wszystkie, bo czytelnik też ma je wszystkie do wyboru.
    """
    rzeczy: list[_Rzecz] = []
    for głowa in _głowy(czytania):
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
