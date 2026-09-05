"""Co olski mówi o napisie, którego gramatyka nie wyprowadza.

Odpowiedzi są dwie i obie kosztują rozbiór drugi:
poprawka jednego znaku (:class:`Naprawa`) mówi, co dzieli ten napis od odczytania,
a zatrzymania (:func:`zatrzymania`) — na których formach analiza po drodze staje.
Pyta się tu gramatyki wprost, napisem albo segmentami,
więc moduł ten o werdykcie nie wie.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from olski.document import SENTENCE_CLOSE
from olski.grammar import Grammar
from olski.lematy import (
    ZAMIENNIKI_CUDZYSŁOWU,
    ZNAK_CUDZYSŁOWU_OTWIERAJĄCY,
    ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY,
)
from olski.morph import Segment
from olski.parse import las, parse
from olski.segmentacja import morphology, na_czym_stanęło
from olski.subset import DEKLARACJA, GRAMMAR

#: Znaki, którymi :func:`_domknięcie` domyka napis, wraz z nazwą, pod którą
#: werdykt je wypisuje; kolejność jest kolejnością prób. Wykrzyknika nie ma, bo
#: terminal końca zdania bierze każdy z trzech, więc kropka zamyka każde
#: czytanie, które zamknąłby on, i mówi przy tym o gramatyce, a nie o tonie
#: autora. Pytajnik jest, bo pytanie zamyka się tylko nim
#: (`KONIEC_ZDANIA` i `PYTAJNIK` w ``olski/subset/słowa.py``).
DOMKNIĘCIA = {".": "kropka na końcu", "?": "pytajnik na końcu"}


@dataclass(frozen=True)
class Naprawa:
    """Poprawka jednego znaku, po której olski to zdanie czyta.

    Klasa jest jedna na wszystkie takie poprawki, bo autorowi mówią one to samo:
    olski tego zdania nie czyta, a od czytania dzieli je jeden znak. Świadkiem
    jest w każdej z nich gramatyka, bo poprawka wchodzi tutaj dopiero wtedy, gdy
    rozbiór poprawionego napisu daje odczytanie. Reguła stojąca na takim świadku
    nie żąda kalibracji, której brak zamknął pakiet reguł
    (docs/linter.md#co-zamknęło-pakiet-reguł).

    Liczba odczytań idzie razem z poprawką, bo policzona drugi raz żądałaby
    trzeciego rozbioru nad zdaniem, które werdykt rozebrał już dwa razy.
    """

    #: Co autor ma poprawić, tak jak to stoi w wierszu werdyktu.
    poprawka: str
    #: Liczba odczytań, które olski nad poprawionym napisem czyta.
    czytań: int


def _domknięcie(zdanie: str, grammar: Grammar) -> Naprawa | None:
    """Poprawka napisu, którego nic nie punktuje jako zdania: znak na jego końcu.

    Warunek na to pytanie stawia :func:`_naprawa`, bo drugi rozbiór jest tu
    całym kosztem.
    """
    for znak, poprawka in DOMKNIĘCIA.items():
        wynik = parse(grammar, morphology(zdanie + znak), deklaracja=DEKLARACJA)
        if not wynik.rejected:
            return Naprawa(poprawka, wynik.ile)
    return None


def _przecytowane(zdanie: str) -> str:
    """To samo zdanie cytowane parą znaków, którą bierze gramatyka.

    Który znak otwiera, a który zamyka, wychodzi z kolejności, a nie z samego
    znaku, bo cudzysłów maszynowy cytuje w obie strony. Apostrof w środku słowa
    tę kolejność przewraca i nie pilnuje tego nic: napis, który stąd wyjdzie,
    odczytania nie ma, więc poprawki :func:`_cudzysłów` z niego nie zrobi.
    """
    otwarty = False
    znaki: list[str] = []
    for znak in zdanie:
        if znak in ZAMIENNIKI_CUDZYSŁOWU:
            znaki.append(ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY if otwarty else ZNAK_CUDZYSŁOWU_OTWIERAJĄCY)
            otwarty = not otwarty
        else:
            znaki.append(znak)
    return "".join(znaki)


def _cudzysłów(
    zdanie: str, nielicencjonowane: tuple[str, ...], grammar: Grammar
) -> Naprawa | None:
    """Poprawka zdania, które cytuje znakiem spoza tego rejestru: para z gramatyki.

    Czemu poprawka dotyczy tego znaku, a nie łącznika, mówi
    docs/subset.md#poprawkę-jednego-znaku-poświadcza-gramatyka.

    Warunek tani stoi przed rozbiorem i pyta o pierwszy oraz ostatni znak formy
    bez licencji. Pyta o oba, bo Morfeusz scala cudzysłów pojedynczy ze słowem w
    jedną formę: ``'Zasad'`` wychodzi jednym segmentem. Nie pyta o samo
    zawieranie, bo apostrof w środku słowa nie cytuje, a ``fact's`` kosztowałby
    wtedy rozbiór.
    """
    if not any(
        forma[0] in ZAMIENNIKI_CUDZYSŁOWU or forma[-1] in ZAMIENNIKI_CUDZYSŁOWU
        for forma in nielicencjonowane
    ):
        return None
    poprawione = _przecytowane(zdanie)
    wynik = parse(grammar, morphology(poprawione), deklaracja=DEKLARACJA)
    if wynik.rejected:
        return None
    return Naprawa(
        f"cudzysłów {ZNAK_CUDZYSŁOWU_OTWIERAJĄCY} i {ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY}"
        " w miejsce tego, którym zdanie cytuje",
        wynik.ile,
    )


def _naprawa(
    zdanie: str,
    grammar: Grammar,
    odrzucone: bool,
    nielicencjonowane: tuple[str, ...],
    doszło_do_końca: bool,
) -> Naprawa | None:
    """Poprawka jednego znaku, po której olski ten napis czyta, albo ``None``.

    Poprawki są dwie, a pyta się o jedną z nich, bo każda kosztuje drugi rozbiór:
    napis bez znaku kończącego pyta o ten znak, a zdanie punktowane o cudzysłów.
    Rozłączności pilnuje sama gramatyka, bo napisu, któremu brakuje obu znaków,
    nie wyprowadzi żadna z tych poprawek z osobna, więc warunki niżej oszczędzają
    rozbiór, a nie strzegą odpowiedzi. Na tej rozłączności stoi
    :attr:`olski.werdykt.zdanie.Verdict.status`:
    o niedomknięciu rozstrzyga tam sama obecność poprawki.

    Domknięcie żąda warunku tańszego jeszcze: analiza doszła do końca napisu i
    każda forma ma licencję. Warunek jest konieczny, bo czytanie nad napisem
    domkniętym bierze każdą formę, więc bierze ją i analiza częściowa nad napisem
    bez znaku. Nie wystarcza: analiza dochodzi do końca także tam, gdzie żadnego
    konstytuentu nie domyka.
    """
    if not odrzucone:
        return None
    if SENTENCE_CLOSE.search(zdanie):
        return _cudzysłów(zdanie, nielicencjonowane, grammar)
    if doszło_do_końca and not nielicencjonowane:
        return _domknięcie(zdanie, grammar)
    return None


def zatrzymania(segmenty: list[Segment], grammar: Grammar | None = None) -> tuple[str, ...]:
    """Każde zatrzymanie odrzuconego zdania, a nie samo pierwsze.

    Werdykt nazywa jedno miejsce (:func:`na_czym_stanęło`), a zdanie długie ma ich
    kilka i pierwsze zasłania resztę, więc kto pisze pod tę gramatykę, nie widzi z
    werdyktu, ile jeszcze poprawek to zdanie zabierze; po co ta odpowiedź jest,
    mówi docs/pisanie-po-olsku.md.

    Cięcie nie wskazuje usterki ani granicy konstrukcji, tak samo jak jedno
    zatrzymanie jej nie wskazuje.
    """
    grammar = grammar or GRAMMAR
    return _od_zatrzymania(segmenty, grammar, _pierwsze_zatrzymanie(segmenty, grammar))


def _pierwsze_zatrzymanie(segmenty: list[Segment], grammar: Grammar) -> Segment | None:
    """Krawędź, na której staje analiza tego kawałka; ``None``, gdy nie staje nigdzie.

    Las odpowiada tu samym :meth:`olski.parse.Las.najdalszy`, a nie całym ``Result``:
    czyta się stąd jedną liczbę,
    a :func:`olski.parse.podsumuj` policzyłby obok niej czytania kawałka
    i wyliczył z nich drzewa.
    Kawałek ostatni bywa zdaniem, więc drzewa te naprawdę powstają.

    Kawałek pusty nie staje, bo nie ma na czym.
    """
    if not segmenty:
        return None
    return na_czym_stanęło(segmenty, las(grammar, segmenty).najdalszy())


def _od_zatrzymania(
    segmenty: list[Segment], grammar: Grammar, stanęło: Segment | None
) -> tuple[str, ...]:
    """Formy zatrzymań tego zdania, licząc od tego, na którym analiza już stanęła.

    Pierwsze zatrzymanie przychodzi argumentem, bo tylko nim wołający się różnią:
    :func:`zatrzymania` rozbiera je z segmentów,
    a :func:`olski.werdykt.zdanie.dalsze_zatrzymania`
    bierze je z werdyktu, który je już policzył.

    Analiza rusza od nowa **za** formą zatrzymania, a nie na niej: formy, której
    nie wzięła żadna analiza częściowa, nie weźmie też analiza zaczęta od niej, a
    przebieg stałby na miejscu. Krawędź przekraczającą cięcie trzeba przy tym
    zdjąć, bo graf segmentacji rozchodzi się na kilka dróg — ``ktoś`` wychodzi
    także jako ``kto`` i ``ś`` — a takiej krawędzi nie ma z czym w kawałku złożyć.
    """
    formy: list[str] = []
    while stanęło is not None:
        formy.append(stanęło.form)
        segmenty = [
            replace(segment, start=segment.start - stanęło.end, end=segment.end - stanęło.end)
            for segment in segmenty
            if segment.start >= stanęło.end
        ]
        stanęło = _pierwsze_zatrzymanie(segmenty, grammar)
    return tuple(formy)
