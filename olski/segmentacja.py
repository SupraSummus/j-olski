"""Warstwa morfologiczna olskiego: z napisu graf segmentacji wraz z czytaniami.

Wykluczenia podzbioru są dwojakie, bo produkcja rozstrzyga o zdaniu, a nie o formie.
Produkcje w ``olski/subset/`` mówią, jakie zdanie się wyprowadza,
a warunki niżej odbierają formie czytanie, zanim produkcja je zobaczy,
oraz dokładają je tam, gdzie słownik milczy.
W jakiej kolejności te warunki idą i czemu w takiej, mówi :func:`morphology`.

Jeden z nich nie jest przy tym zdaniem podzbioru, tylko zdaniem projektu:
``olski/słownictwo.py`` mówi, których lematów projekt nie używa
i którym uchyla wykluczenie słownikowe.

Nad gotowym grafem stoją tu jeszcze dwa pytania o niego,
bo odpowiada na nie i werdykt, i przebieg nad korpusem:
po które czytanie formy nie sięga ani jeden terminal (:func:`licencjonowane`)
oraz na której krawędzi stanęło odrzucenie (:func:`na_czym_stanęło`).
Wejściem obu jest graf, a nie napis, i dlatego stoją tutaj.

Gramatyki moduł ten nie czyta, tylko bierze ją argumentem tych dwóch pytań,
więc kto chce samej morfologii, nie buduje gramatyki;
pilnuje tego ``tests/test_segmentacja.py``.

Warstwę tę wraz z typem, którym oddaje wynik następnej, wylicza docs/architecture.md.
"""

from __future__ import annotations

import re
from dataclasses import replace

from olski import projekt
from olski.document import Document
from olski.grammar import Grammar
from olski.lematy import (
    LEMAT_ZWROTNY,
    PRZYIMEK_ROZDZIELAJĄCY,
    ZNAK_CUDZYSŁOWU_OTWIERAJĄCY,
    ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY,
)
from olski.morph import Reading, Segment, analyse, tag
from olski.słownictwo import SŁOWNICTWO, Słownictwo


def sentences(text: str) -> list[str]:
    """Tnie tekst na zdania i oddaje je tak, jak stoją.

    Podziału nie ma tutaj, tylko w :mod:`olski.document`: żąda on po kropce
    białego znaku i zna skróty. Sam olski skrótów nie ma, więc nad nim
    cięcie na każdej kropce byłoby dokładne. Wejściem jest jednak dokumentacja,
    gdzie ``docs/linter.md`` jest jednym słowem, a cięcie na kropce w jego środku
    wymyśla dwa zdania, których nikt nie napisał.

    Cięcie stoi więc przed analizą, a nie po niej, i z tego samego powodu, z
    którego stoi tam sklejenie notacji (:func:`morphology`): Morfeusz jest
    wołany z ``SKIP_WHITESPACES``, więc po analizie nie ma już czym zobaczyć
    spacji, która granicę zdania odróżnia od nazwy pliku.
    """
    document = Document(text)
    return [document.slice(span) for span in document.sentences]



#: The closed-class parts of speech. A noun reading of a form that also reads as
#: one of these is competing with the reading the form nearly always carries.
#: The pronoun is on the list for that property rather than for its syntax,
#: which docs/subset.md argues and docs/corpus.md prices.
CLOSED_CLASS = frozenset(
    {"prep", "conj", "comp", "qub", "part", "pred", "interj", "ppron3", "ppron12"}
)

#: The seven cases. A noun reading carrying all of them inflects for nothing, so
#: no case demand can fail against it.
EVERY_CASE = frozenset({"nom", "gen", "dat", "acc", "inst", "loc", "voc"})


def _acronym(form: str) -> bool:
    """Whether a form is written the way Polish writes an acronym.

    ``PO``, ``AA`` and ``UP`` inflect for nothing either, and their letters spell
    function words, so the exclusion below would take exactly the reading that is
    right. In capitals the noun is what the form is. One capital says nothing,
    every sentence starting with one.
    """
    return len(form) > 1 and form.isupper()


def admissible(segment: Segment, słownictwo: Słownictwo = SŁOWNICTWO) -> Segment:
    """Drop the noun reading of a form olski reads as a closed-class word.

    Morfeusz reads ``do`` as the preposition and as the musical note, and the
    note inflects for nothing (:data:`EVERY_CASE`), so every ``do`` in a text
    otherwise hands its sentence a second reading. That is ambiguity in the
    dictionary rather than in Polish, and no parse can tell the two apart, so
    the lexicon rules it out instead. docs/subset.md argues the criterion and
    docs/corpus.md measures what it is worth and what it costs.

    Wieloznaczność ta jest jednak wieloznacznością w rejestrze, a nie w słowniku:
    `Go jest grą.` polszczyzna ma, a to wykluczenie odbiera jej podmiot.
    Lemat, o którym projekt mówi, że go używa, zostaje przez to nietknięty
    (``olski/słownictwo.py``), a projekt bez takiej deklaracji dostaje kryterium
    całe, bo o grze nie pisze prawie nikt.
    """
    if _acronym(segment.form):
        return segment
    if not any(reading.tag.pos in CLOSED_CLASS for reading in segment.readings):
        return segment
    kept = tuple(
        reading
        for reading in segment.readings
        if reading.lemma in słownictwo.wpuszczane
        or not (reading.tag.pos == "subst" and reading.tag.get("case") >= EVERY_CASE)
    )
    if len(kept) == len(segment.readings):
        return segment
    # A closed-class reading is not a noun reading, so the one that spared this
    # segment is itself among the survivors and the tuple is never emptied.
    return replace(segment, readings=kept)


def w_słownictwie(segment: Segment, słownictwo: Słownictwo = SŁOWNICTWO) -> Segment:
    """Zdejmij czytania lematu, o którym projekt mówi, że go nie używa.

    Warunek wyżej pyta o kształt czytania, a ten o sam lemat, i po to jest:
    `soba` odmienia się przez przypadki, więc kryterium nieodmienności po nią nie
    dochodzi, a od zaimka zwrotnego nie odróżnia jej żadne znamię formalne.
    Kryterium nie ma tu skąd wyjść i rozstrzyga deklaracja (``olski/słownictwo.py``).

    Krawędź wolno temu warunkowi opróżnić i tym różni się on od warunku wyżej,
    a zgadza z :func:`po_przyimku`: projekt, który mówi, że słowa nie używa,
    mówi to także o zdaniu, w którym stoi ono samo, a werdykt nazywa wtedy formę
    bez licencji (:func:`bez_licencji`).
    """
    kept = tuple(
        reading for reading in segment.readings if reading.lemma not in słownictwo.pomijane
    )
    if len(kept) == len(segment.readings):
        return segment
    return replace(segment, readings=kept)


#: Cecha, którą tagset daje formie zaimka po tym, czy stoi ona po przyimku.
#: Wartość ``praep`` bez ``npraep`` obok niej nazywa formę, którą polszczyzna
#: stawia wyłącznie tam: `niego`, `nich`, `nie`. Forma o obu wartościach naraz —
#: `nim`, a w miejscowniku także `niej` i `nich` — stoi i pod przyimkiem, i bez niego.
PRZYIMKOWOŚĆ = "post_prepositionality"
BEZ_PRZYIMKA = "npraep"


def _tylko_po_przyimku(reading: Reading) -> bool:
    """Czy tagset mówi o tym czytaniu, że stoi wyłącznie po przyimku."""
    wartości = reading.tag.get(PRZYIMKOWOŚĆ)
    return bool(wartości) and BEZ_PRZYIMKA not in wartości


def po_przyimku(segments: list[Segment]) -> list[Segment]:
    """Zdejmij formie przyimkowej zaimka czytanie tam, gdzie przyimka nie ma.

    Grupa imienna bierze zaimek w każdej swojej pozycji, więc bez tego warunku
    `Cena niego rośnie.` się wyprowadza, a `nie` stoi dopełnieniem w zdaniu,
    które przeczy. Są to czytania, których polszczyzna nie ma, czyli to samo, co
    odbiera :func:`admissible`; dlaczego warunek stoi tutaj, a nie na terminalu
    zaimka ani za rozbiorem, wywodzi
    docs/subset.md#forma-przyimkowa-zaimka-żąda-przyimka-przed-sobą.

    Pytany jest graf, a nie lista: licencji udziela każda krawędź z czytaniem
    przyimkowym, która kończy się w węźle, gdzie ta się zaczyna. Krawędź bez ani
    jednego czytania z tego wychodzi — `niego` innych nie ma — i jest wtedy formą
    bez licencji, którą werdykt wypisuje (:func:`bez_licencji`).

    Licencji udziela przyimek, który ta gramatyka bierze, a nie każda forma z
    czytaniem przyimkowym, i dlatego wykluczenie stoi tu to samo, co na terminalu
    (:data:`PRZYIMEK_ROZDZIELAJĄCY`). Bez niego `Cena jest niska, a nie.`
    wyprowadza się: rozdzielające `a` niesie u Morfeusza czytanie przyimka, więc
    licencjonuje `nie` stojące za nim, a wyrażenia przyimkowego z tego `a` nie ma
    jak zbudować, czyli licencji udziela pozycja, której nikt nie zajmuje.
    """
    licencjonujące = {
        segment.end
        for segment in segments
        if any(
            reading.tag.pos == "prep" and reading.lemma != PRZYIMEK_ROZDZIELAJĄCY
            for reading in segment.readings
        )
    }
    return [
        segment
        if segment.start in licencjonujące
        else replace(
            segment,
            readings=tuple(
                reading for reading in segment.readings if not _tylko_po_przyimku(reading)
            ),
        )
        for segment in segments
    ]


def po_słowie(segments: list[Segment]) -> list[Segment]:
    """Zdejmij cząstce zwrotnej odczytanie tam, gdzie nie stoi przed nią żadne słowo.

    Cząstka stoi przy swojej formie osobowej po obu jej stronach
    (`SZYKI_CZĄSTKI` w ``olski/subset/słowa.py``), a pozycja przednia sięga początku zdania
    i miejsca
    tuż za znakiem: bez tego warunku `Się myli.` oraz `Cena rośnie, się nie
    liczy.` się wyprowadzają, a takich napisów polszczyzna nie ma. Cząstka opiera
    się bowiem na słowie przed sobą, a znak słowem nie jest. Spójnik nim jest i
    licencji udziela, bo `i przyrasta, i się topi` bank drzew pisze.

    Pozycja tylna do tych miejsc nie sięga, bo przed nią stoi jej własna forma,
    więc warunek nie zdejmuje ani jednego odczytania, które olski brał przed
    wpuszczeniem pozycji przedniej.

    Pytany jest graf, a nie lista, i pytanie jest to samo, które stawia
    :func:`po_przyimku`: odczytanie zostaje tam, gdzie w węźle otwierającym tę
    krawędź kończy się krawędź z odczytaniem, które nie jest znakiem.

    Warunek stoi w warstwie morfologicznej, a nie na terminalu cząstki, z tego
    samego powodu, z którego stoi tam tamten: miejsce, którego cząstka nie ma
    zająć, jest miejscem w zdaniu, a terminal widzi samą formę.
    docs/subset.md#cząstka-zwrotna-należy-do-swojego-czasownika
    trzyma, co warunek ten zostawia na zewnątrz.
    """
    licencjonujące = {
        segment.end
        for segment in segments
        if any(reading.tag.pos != "interp" for reading in segment.readings)
    }
    return [
        segment
        if segment.start in licencjonujące
        else replace(
            segment,
            readings=tuple(
                reading for reading in segment.readings if reading.lemma != LEMAT_ZWROTNY
            ),
        )
        for segment in segments
    ]


#: Notacja tego rejestru: ścieżka, nazwa pliku, nazwa modułu. Człony spaja
#: ukośnik albo kropka, po której nie ma spacji, człon ma dwa znaki wyrazowe albo
#: więcej, w całości stoi przynajmniej jedna litera, a łącznik spaja tylko wewnątrz
#: takiej ścieżki. docs/subset.md wywodzi, co każde z tych czterech żądań trzyma na
#: zewnątrz i dlaczego. Klasa w podglądzie jest sumą pozostałych, bo litery szuka
#: dokładnie tam, gdzie sięgnie dopasowanie: znak spajający dodany do wzorca
#: dodaje się i tam.
CZŁON = r"\w{2,}"
NOTACJA = re.compile(
    rf"(?<![\w./])(?=[\w./_-]*[^\W\d_]){CZŁON}(?:[-_]{CZŁON})*(?:[./]{CZŁON}(?:[-_]{CZŁON})*)+"
)

#: Czytanie, które dostaje notacja, wersalik i przytoczenie: rzeczownik
#: nieodmienny, dokładnie ten tag, który Morfeusz daje `menu` i `atelier`.
NIEODMIENNY = tag("subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:n:ncol")


def wersalik(segment: Segment) -> Segment:
    """Daj formie pisanej wersalikami czytanie nieodmienne, gdy słownik jej nie ma.

    ``README``, ``GLR`` i ``SGJP`` są w tym rejestrze codzienne i wracają jako
    ``ign``, którego nie bierze ani jedna produkcja. Notacja wyżej dostaje to samo
    czytanie i różni się znakiem, który ją spaja (:data:`NOTACJA`).

    Warunek pyta o milczenie słownika, a nie o samo pismo formy, i tym broni
    polszczyzny: ``NIE`` i ``PAN`` słownik czyta, więc zdanie z nimi nie traci
    czytania, które ma. Wywód i cenę trzyma docs/subset.md pod wersalikiem.
    """
    if not _acronym(segment.form):
        return segment
    if any(reading.tag.known for reading in segment.readings):
        return segment
    return replace(segment, readings=(Reading(segment.form, segment.form, NIEODMIENNY),))


#: Części mowy, którymi grupa imienna staje sama jednym słowem. Napisu z takim
#: czytaniem przytoczenie nie rusza, bo cudzysłów bierze go już jako grupę, a
#: zamiana odebrałaby mu i przypadek, i rodzaj. Za co dokładnie, mówi
#: docs/subset.md w sekcji o interpunkcji obejmującej.
GRUPA_JEDNYM_SŁOWEM = frozenset({"subst", "ger", "ppron12", "ppron3"})


def _przytoczony(segment: Segment, otwarte: set[int], zamknięte: set[int]) -> bool:
    """Czy cudzysłów obejmuje sam ten napis, a grupą imienną on nie jest."""
    if segment.start not in otwarte or segment.end not in zamknięte:
        return False
    return not any(reading.tag.pos in GRUPA_JEDNYM_SŁOWEM for reading in segment.readings)


def przytoczenie(segments: list[Segment]) -> list[Segment]:
    """Daj napisowi objętemu cudzysłowem czytanie nieodmienne, gdy grupą nie jest.

    Napis przytoczony — `„B”`, `„nie”` — nie odmienia się, więc produkcja
    przepuszczająca przypadek grupy nie ma na nim czego przepuszczać, a rzeczownik
    nieodmienny spełnia każde żądanie przypadku, bo żadnego nie nosi. Wywód, cenę
    i granicę warunku trzyma docs/subset.md w sekcji o interpunkcji obejmującej.

    Licencji udziela cudzysłów po obu stronach, więc pytany jest graf, a nie sama
    forma, tak samo jak przy formie przyimkowej (:func:`po_przyimku`). Warunek na
    oba znaki naraz żąda przy tym, żeby napis wypełniał wnętrze sam. Czytania są
    zamienione, a nie dołożone, bo napisu przytoczonego to zdanie nie używa jako
    słowa.
    """
    otwarte = {
        segment.end
        for segment in segments
        if any(reading.lemma == ZNAK_CUDZYSŁOWU_OTWIERAJĄCY for reading in segment.readings)
    }
    zamknięte = {
        segment.start
        for segment in segments
        if any(reading.lemma == ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY for reading in segment.readings)
    }
    return [
        replace(segment, readings=(Reading(segment.form, segment.form, NIEODMIENNY),))
        if _przytoczony(segment, otwarte, zamknięte)
        else segment
        for segment in segments
    ]


def morphology(text: str, słownictwo: Słownictwo = SŁOWNICTWO) -> list[Segment]:
    """Analizuje tekst tak, jak czyta go olski.

    Kilka rzeczy dzieje się tu przed gramatyką. Notacja rejestru dostaje jedną
    krawędź z jednym czytaniem, bo Morfeusz rozbija ``docs/linter.md`` na pięć
    krawędzi, a czytelnik ma tam jedno słowo. Słowo, którego słownik nie ma,
    dostaje czytania z leksykonu projektu (:mod:`olski.projekt`), bo ``commitów``
    jest dopełniaczem liczby mnogiej i nikt nie ma tam czytania nieodmiennego.
    Forma pisana wersalikami, której słownik nie czyta wcale, dostaje czytanie
    nieodmienne (:func:`wersalik`). Reszta idzie do Morfeusza i traci te czytania,
    które odrzuca :func:`admissible`, po nich te, których lematu projekt nie używa
    (:func:`w_słownictwie`), a po nich te, które :func:`po_przyimku`
    odrzuca formie stojącej bez przyimka oraz :func:`po_słowie` cząstce zwrotnej
    stojącej bez słowa przed sobą, a na końcu napis objęty cudzysłowem dostaje
    czytanie nieodmienne przytoczenia (:func:`przytoczenie`).

    Trzy ostatnie warunki pytają o sąsiada, a nie o samą formę, więc idą po liście
    gotowej, a nie po jednym segmencie jak te przed nimi. Przytoczenie idzie
    ostatnie, bo pyta o czytania, które zostały: ``be`` traci rzeczownik w
    :func:`admissible` i przytoczenie zastaje tam sam przymiotnik.

    Słownictwo projektu wchodzi tu argumentem, a nie stałą czytaną w dwóch
    warunkach, bo bez tego nie da się przeczytać jednego zdania dwoma
    deklaracjami, a takiego pytania żąda i suita, i każdy, kto tę deklarację
    wycenia (``olski/słownictwo.py``).

    Sklejenie stoi przed analizą, a nie za nią. Segment niesie numery węzłów
    grafu, a nie przesunięcia w tekście, więc po analizie nie ma już czym zobaczyć
    spacji, która ukośnik w ścieżce odróżnia od ukośnika między dwoma słowami.
    """
    return przytoczenie(
        po_słowie(
            po_przyimku([
                w_słownictwie(
                    admissible(wersalik(projekt.z_leksykonu(segment)), słownictwo), słownictwo
                )
                for segment in _segmenty(text)
            ])
        )
    )


def _segmenty(text: str) -> list[Segment]:
    """Krawędzie grafu segmentacji, notację liczące za jedną z nich.

    Grafy kolejnych kawałków stają jeden za drugim, przesunięte o numer węzła, na
    którym poprzedni się skończył. Wolno tak, bo każdy z nich ma jedno źródło i
    jedno ujście: Morfeusz numeruje od zera, a wszystkie ścieżki przez kawałek
    kończą się na tym samym węźle, choćby w środku rozchodziły się na dwie.
    """
    segmenty: list[Segment] = []
    węzeł = 0
    for kawałek, notacja in _kawałki(text):
        krawędzie = _krawędzie(kawałek) if notacja else analyse(kawałek)
        segmenty.extend(
            replace(segment, start=segment.start + węzeł, end=segment.end + węzeł)
            for segment in krawędzie
        )
        węzeł += max((segment.end for segment in krawędzie), default=0)
    return segmenty


def _kawałki(text: str):
    """Tnie tekst na kawałki, każdy z odpowiedzią, czy jest notacją."""
    znak = 0
    for match in NOTACJA.finditer(text):
        yield text[znak : match.start()], False
        yield match.group(), True
        znak = match.end()
    yield text[znak:], False


def _krawędzie(forma: str) -> list[Segment]:
    return [Segment(start=0, end=1, form=forma, readings=(Reading(forma, forma, NIEODMIENNY),))]


def licencjonowane(segment: Segment, grammar: Grammar) -> tuple[Reading, ...]:
    """Czytania formy, po które sięga choć jeden terminal tej gramatyki.

    Pytają o to dwie odpowiedzi o jednym kryterium: werdykt wypisuje formę, której
    nie zostaje ani jedno (:func:`bez_licencji`), a przebieg nad korpusem nazywa
    część mowy tego, które zostało (``bloker`` w ``olski/pokrycie.py``).
    Kryterium wyprowadza z gramatyki :meth:`olski.grammar.Grammar.licencjonuje`,
    a ta funkcja jest samym jego zastosowaniem do czytań formy.
    """
    return tuple(
        reading
        for reading in segment.readings
        if grammar.licencjonuje(reading.tag.pos, reading.lemma, segment.lematy, reading.tag.cechy)
    )


def bez_licencji(segments: list[Segment], grammar: Grammar) -> tuple[str, ...]:
    """Formy nie do ominięcia, którym gramatyka nie bierze ani jednego czytania.

    Odrzucenie ma dwie przyczyny i są to dwie różne roboty do zrobienia: forma,
    po którą nie sięga żadna produkcja, i struktura, której gramatyka nie
    licencjonuje. Świgra trzyma je osobno (docs/swigra.md), a tę pierwszą widać
    przed rozbiorem i widać ją wyprowadzoną z gramatyki
    (:meth:`olski.grammar.Grammar.licencjonuje` wywodzi, czemu wolno).

    Liczy się przy tym krawędź, bez której nie ma drogi przez zdanie, a nie
    każda pusta dziedzina: podział, który Morfeusz dokłada obok formy całej, nie
    jest słowem, które ktokolwiek napisał. Wywód i to, co ten warunek daje za
    darmo, trzyma docs/design-notes.md.

    Forma stoi na liście raz, choćby w zdaniu powtórzyła się kilka razy, bo
    odpowiedzią jest to, czego gramatyka nie bierze, a nie ile razy autor to
    napisał.
    """
    formy: list[str] = []
    for segment in segments:
        if licencjonowane(segment, grammar):
            continue
        if _omijalna(segments, segment) or segment.form in formy:
            continue
        formy.append(segment.form)
    return tuple(formy)


def _omijalna(segments: list[Segment], krawędź: Segment) -> bool:
    """Czy przez graf segmentacji idzie droga, która tej krawędzi nie bierze.

    Krawędzie idą w górę po numerach węzłów, więc osiągalność liczy się jednym
    przejściem po posortowanych, bez cofania się.
    """
    ujście = max(segment.end for segment in segments)
    osiągalne = {min(segment.start for segment in segments)}
    for segment in sorted(segments, key=lambda segment: segment.start):
        if segment is not krawędź and segment.start in osiągalne:
            osiągalne.add(segment.end)
    return ujście in osiągalne


def na_czym_stanęło(segments: list[Segment], furthest: int) -> Segment | None:
    """Krawędź, na której odrzucenie stanęło; ``None``, gdy stanęło na końcu zdania.

    Ostatniego znaku zdania nie nazywa, bo zdanie, które bierze każdą swoją
    formę i nie domyka się, jest drugim zdarzeniem i dostaje drugie zdanie
    werdyktu (``Verdict.explain``) oraz drugi wiersz przebiegu nad korpusem
    (``NO_STRUCTURE`` w ``olski/pokrycie.py``).

    Krawędź, a nie forma, bo pytają o nią dwie odpowiedzi: werdykt bierze stąd
    formę, a ranking blokerów część mowy jej czytania, i kryterium jest jedno.

    Z jednego węzła grafu wychodzi czasem kilka form, bo ``ktoś`` wychodzi
    także jako ``kto`` i ``ś``. Nazwana jest najdłuższa, czyli ta, którą autor
    napisał, a krótsza jest jej częścią.

    Nazwane miejsce jest końcem przedrostka, który się analizuje, i nie jest
    wskazaniem usterki; wywód i cenę trzyma
    docs/subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka.
    """
    ujście = max((segment.end for segment in segments), default=furthest)
    stojące = [
        segment for segment in segments if segment.start == furthest and segment.end < ujście
    ]
    if not stojące:
        return None
    return max(stojące, key=lambda segment: segment.end)

