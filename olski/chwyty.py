"""Chwyt rejestru, czyli wzorzec prozy, którego w tym repozytorium nie chcemy.

Katalog takich wzorców stoi w CLAUDE.md, a sprawdza je przegląd zmian, czyli
człowiek czytający zdanie po zdaniu. Wzorzec, który dostanie tu wykrywacz,
przestaje tego czekać.

Wiersz o chwycie pada obok werdyktu i tylko pod flagą, bo populacją jest proza,
za którą odpowiadamy: autor sprawdzający swój tekst tego katalogu nie zna.
Czemu ta jedna reguła progu nie potrzebuje i co odrzucił pomiar, który ją wybrał,
mówi docs/linter.md#wykrywacz-chwytu-zgłasza-to-bez-rzeczownika-przy-sobie.
"""

from __future__ import annotations

from dataclasses import dataclass

from olski.morph import Reading, Segment, zgadza
from olski.segmentacja import morphology

#: Zaimek, który podejmuje całe zdanie obok, zamiast wskazywać rzecz w nim.
#: Wielka litera jest tu warunkiem, a nie zapisem jednego z dwóch wariantów:
#: zdanie zaczyna się wielką literą, więc małe `to` na jego czele znaczy, że
#: ekstrakcja zdjęła grawisy słowu, o którym ta proza mówi, albo że kropkę
#: postawił przykład (docs/extraction.md#what-the-reader-sees-is-not-always-polish),
#: a o żadnym z tych dwóch napisów reguła nie orzeka.
PODEJMUJĄCE = "To"

#: Części mowy, którymi zdanie nazywa rzecz. Rzeczownik odczasownikowy jest nią
#: tak samo, więc `To przeliczenie` chwytem nie jest.
IMIENNE = frozenset({"subst", "depr", "ger"})

#: Cechy, którymi zaimek zgadza się z rzeczą stojącą przy nim; przypadek jest
#: wśród nich, bo zaimek stoi w tej samej grupie co ona (:func:`olski.morph.zgadza`).
ZGODNE = ("number", "gender", "case")

#: Znak, po którym `to` zapowiada zdanie podrzędne, a nie podejmuje zdanie obok.
#: `To, czy fraza stanęła na nijakiej mnogiej, nie jest rzeczą` mówi o tym, co
#: stoi za przecinkiem, więc rzeczownika w miejsce tego `to` nie ma jak wstawić.
ZAPOWIEDŹ_PODRZĘDNEGO = ","

#: Formy, którymi zdanie stawia orzeczenie, czyli granica grupy podmiotu
#: (:func:`_grupa`). Wartości ``pred`` tu nie ma, bo `to` samo ją niesie.
OSOBOWE = frozenset({"fin", "praet", "impt", "imps", "winien", "bedzie"})


@dataclass(frozen=True)
class Chwyt:
    """Chwyt rejestru w jednym zdaniu: forma, na której stoi, i co z nią zrobić.

    Naprawa idzie razem z formą, bo katalog ją nazywa, a wiersz bez niej mówiłby
    autorowi tyle, że coś jest nie tak.
    """

    #: Forma tak, jak stoi w zdaniu.
    forma: str
    #: Co z nią zrobić, jednym zdaniem.
    naprawa: str


def chwyty(zdanie: str) -> tuple[Chwyt, ...]:
    """Chwyty rejestru w tym zdaniu; pusta krotka jest milczeniem.

    Morfologię bierze stąd, skąd bierze ją gramatyka
    (:func:`olski.segmentacja.morphology`), bo zdanie ma być czytane raz i
    jednakowo: czytanie odebrane formie przez leksykon projektu nie ma tu wracać.
    """
    chwyt = _podjęte_zdanie(morphology(zdanie))
    return (chwyt,) if chwyt else ()


def _podjęte_zdanie(segmenty: list[Segment]) -> Chwyt | None:
    """Zaimek `to` otwierający zdanie, a nie mający przy sobie rzeczownika.

    Zaimek ten odsyła wtedy do całego zdania poprzedniego, a nie do rzeczy
    nazwanej w nim (CLAUDE.md#katalog-chwytów-rejestru), i tym różni się od
    zaimka, o który pyta ``olski/odniesienia.py``: tam kandydatów wylicza
    zgodność, a tu nie ma czego wyliczać, bo zdanie rzeczą nie jest.

    Pytamy o pierwszą formę zdania, bo tam ten zaimek stoi w podmiocie. Dalej w
    zdaniu `to` bywa łącznikiem i bywa zapowiedzią, a rozdziela je dopiero
    rozbiór, którego nad tą prozą nie ma.
    """
    if not segmenty or segmenty[0].form != PODEJMUJĄCE:
        return None
    zaimek = segmenty[0].with_pos("subst")
    if not zaimek or (len(segmenty) > 1 and segmenty[1].form == ZAPOWIEDŹ_PODRZĘDNEGO):
        return None
    if any(zgadza(zaimek, _imienne(segment), ZGODNE) for segment in _grupa(segmenty)):
        return None
    return Chwyt(segmenty[0].form, "podejmuje całe zdanie obok: wstaw w jego miejsce rzeczownik")


def _grupa(segmenty: list[Segment]) -> list[Segment]:
    """Segmenty stojące przy zaimku, czyli te przed orzeczeniem zdania.

    Rzeczownik za orzeczeniem zaimka nie określa i cichnąć po nim nie wolno, bo
    `To jest miejsce, gdzie olski milczy.` jest tym samym chwytem co `To jest
    tanie.`, a różni je sam rodzaj rzeczownika, który za orzeczeniem stanął.
    Zdanie bez formy osobowej oddaje całą swoją resztę, bo granicy nie ma wtedy
    czym postawić.
    """
    for numer, segment in enumerate(segmenty[1:], start=1):
        if any(czytanie.tag.pos in OSOBOWE for czytanie in segment.readings):
            return segmenty[1:numer]
    return segmenty[1:]


def _imienne(segment: Segment) -> list[Reading]:
    return [czytanie for czytanie in segment.readings if czytanie.tag.pos in IMIENNE]
