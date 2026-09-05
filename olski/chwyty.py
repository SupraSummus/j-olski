"""Chwyt rejestru, czyli wzorzec prozy, którego w tym repozytorium nie chcemy.

Katalog takich wzorców jest konwencją repozytorium, a sprawdza je przegląd zmian, czyli
człowiek czytający zdanie po zdaniu. Wzorzec, który dostanie tu wykrywacz,
przestaje tego czekać.

Wiersz o chwycie pada obok werdyktu i tylko pod flagą, bo populacją jest proza,
za którą odpowiadamy: autor sprawdzający swój tekst tego katalogu nie zna.
Czemu reguła o zaimku progu nie potrzebuje i co odrzucił pomiar, który ją wybrał,
mówi docs/linter.md#wykrywacz-chwytu-zgłasza-to-bez-rzeczownika-przy-sobie.
O regule zastępującej orzeczenie mówi to samo
docs/linter.md#drugi-wykrywacz-zgłasza-zwrot-zastępujący-orzeczenie-członu,
a o regule o czasowniku pustym
docs/linter.md#trzeci-wykrywacz-zgłasza-czasownik-pusty-przed-rzeczownikiem-odczasownikowym.
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

#: Formy osobowe, czyli granica grupy podmiotu (:func:`_grupa`).
#: Wartości ``pred`` tu nie ma, bo `to` samo ją niesie.
OSOBOWE = frozenset({"fin", "praet", "impt", "imps", "winien", "bedzie"})

#: Formy, którymi człon stawia orzeczenie (:func:`_domyślne_orzeczenia`).
#: ``pred`` jest tu, a przy granicy grupy podmiotu go nie ma:
#: `Dowieść jej trzeba tak samo.` orzeka słowem `trzeba`, więc zwrot określa
#: tam orzeczenie, zamiast stać w jego miejsce.
ORZEKAJĄCE = OSOBOWE | {"pred"}

#: Zwroty, którymi człon orzeka bez czasownika: orzeczenie czytelnik ma wziąć
#: z członu wcześniejszego. Zwrot jest krotką form, bo Morfeusz wydaje formy,
#: a `tak samo` jest dwiema.
ZASTĘPUJĄCE_ORZECZENIE = frozenset({("tak", "samo"), ("też",), ("odwrotnie",)})

#: Znaki, którymi interpunkcja rozdziela człony zdania (:func:`_człony`).
#: Nawias jest wśród nich, bo wtrącenie zamknięte zwrotem orzeka bez czasownika,
#: a bez tej granicy człon wziąłby orzeczenie zdania, w które wtrącenie wpadło.
GRANICE_CZŁONÓW = frozenset({",", ";", ":", "—", "–", "(", ")", ".", "!", "?", "…"})

#: Spójniki porównania. Zwrot, za którym stoi jeden z nich, porównuje rzecz
#: z rzeczą i orzeczenia nie zastępuje; pytamy o człon następny, bo porównanie
#: bywa odcięte przecinkiem: `czyli tak samo, jak czyta do przyimkiem i nutą`.
PORÓWNANIE = frozenset({"jak", "niż"})


#: Nazwy chwytów, po jednej na regułę. Wydruk ich nie pokazuje, bo autorowi mówi
#: to samo naprawa stojąca w wierszu; pyta o nie korpus usterek, gdzie wpis nazywa
#: zgłoszenie, które ma paść, a nazwa wspólna nie mówiłaby, która reguła padła.
PODJĘTE_ZDANIE = "zaimek podejmujący zdanie"
ZASTĘPCZE_ORZECZENIE = "zwrot zastępujący orzeczenie"
CZASOWNIK_PUSTY = "czasownik pusty"

#: Czasowniki, które przed rzeczownikiem odczasownikowym nie orzekają czynności:
#: nazywa ją wtedy rzeczownik, a czasownik niesie z niej sam czas i tryb.
#: Pustka jest własnością lematu, a nie kształtu zdania, więc lista jest zamknięta
#: i wpisuje się do niej lemat, a nie wzorzec: `Rada wykonuje zadania.` orzeka
#: czynność czasownikiem, a `Dokonano przeprowadzenia analizy.` rzeczownikiem.
PUSTE = frozenset(
    {
        "dokonać",
        "dokonywać",
        "nastąpić",
        "następować",
        "podejmować",
        "podjąć",
        "przeprowadzać",
        "przeprowadzić",
        "ulec",
        "ulegać",
        "wykonać",
        "wykonywać",
    }
)

#: Części mowy, którymi forma stoi za rzeczownik zwykły
#: (:func:`_puste_czasowniki`).
RZECZOWNIKOWE = frozenset({"subst", "depr"})


@dataclass(frozen=True)
class Chwyt:
    """Chwyt rejestru w jednym zdaniu: forma albo zwrot wraz z naprawą.

    Naprawa idzie razem z formą, bo katalog ją nazywa, a wiersz bez niej mówiłby
    autorowi tyle, że coś jest nie tak.
    """

    #: Która reguła to zgłasza.
    nazwa: str
    #: Forma albo zwrot dwóch form, tak jak je zdanie zapisuje.
    forma: str
    #: Co z tym zrobić, jednym zdaniem.
    naprawa: str


def chwyty(zdanie: str) -> tuple[Chwyt, ...]:
    """Chwyty rejestru w tym zdaniu; pusta krotka jest milczeniem.

    Morfologię bierze stąd, skąd bierze ją gramatyka
    (:func:`olski.segmentacja.morphology`), bo zdanie ma być czytane raz i
    jednakowo: czytanie odebrane formie przez leksykon projektu nie ma tu wracać.
    """
    segmenty = morphology(zdanie)
    return (
        _podjęte_zdanie(segmenty)
        + _domyślne_orzeczenia(segmenty)
        + _puste_czasowniki(segmenty)
    )


def _podjęte_zdanie(segmenty: list[Segment]) -> tuple[Chwyt, ...]:
    """Zaimek `to` otwierający zdanie, a nie mający przy sobie rzeczownika.

    Zaimek ten odsyła wtedy do całego zdania poprzedniego, a nie do rzeczy
    nazwanej w nim, i tym różni się od
    zaimka, o który pyta ``olski/odniesienia.py``: tam kandydatów wylicza
    zgodność, a tu nie ma czego wyliczać, bo zdanie rzeczą nie jest.

    Pytamy o pierwszą formę zdania, bo tam ten zaimek stoi w podmiocie. Dalej w
    zdaniu `to` bywa łącznikiem i bywa zapowiedzią, a rozdziela je dopiero
    rozbiór, którego nad tą prozą nie ma.
    """
    if not segmenty or segmenty[0].form != PODEJMUJĄCE:
        return ()
    zaimek = segmenty[0].with_pos("subst")
    if not zaimek or (len(segmenty) > 1 and segmenty[1].form == ZAPOWIEDŹ_PODRZĘDNEGO):
        return ()
    if any(zgadza(zaimek, _imienne(segment), ZGODNE) for segment in _grupa(segmenty)):
        return ()
    return (
        Chwyt(
            PODJĘTE_ZDANIE,
            segmenty[0].form,
            "podejmuje całe zdanie obok: wstaw w jego miejsce rzeczownik",
        ),
    )


def _grupa(segmenty: list[Segment]) -> list[Segment]:
    """Segmenty stojące przy zaimku, czyli te przed orzeczeniem zdania.

    Rzeczownik za orzeczeniem zaimka nie określa i cichnąć po nim nie wolno, bo
    `To jest miejsce, gdzie olski milczy.` jest tym samym chwytem co `To jest
    tanie.`, a różni je sam rodzaj rzeczownika, który za orzeczeniem stanął.
    Zdanie bez formy osobowej oddaje całą swoją resztę, bo granicy nie ma wtedy
    czym postawić.
    """
    for numer, segment in enumerate(segmenty[1:], start=1):
        if _orzeka(segment, OSOBOWE):
            return segmenty[1:numer]
    return segmenty[1:]


def _imienne(segment: Segment) -> list[Reading]:
    return [czytanie for czytanie in segment.readings if czytanie.tag.pos in IMIENNE]


def _orzeka(segment: Segment, klasy: frozenset[str]) -> bool:
    return any(czytanie.tag.pos in klasy for czytanie in segment.readings)


def _domyślne_orzeczenia(segmenty: list[Segment]) -> tuple[Chwyt, ...]:
    """Zwroty, którymi człon bez orzeczenia orzeka o rzeczy nazwanej w nim.

    `a korpus audytowy odwrotnie` każe czytelnikowi wziąć orzeczenie z członu
    wcześniejszego, a kto wszedł w środek akapitu, tamtego członu nie przeczytał.
    Naprawą jest powtórzony czasownik, choćby zdanie wyszło dłuższe.

    Warunki są trzy i każdy zdejmuje inną klasę zdań poprawnych.
    Zwrot zamyka człon, bo `tak samo jak przy dwukropku` porównuje rzecz z rzeczą
    i nazywa przy tym drugi jej człon.
    Orzeczenia w członie nie ma, bo `Tak samo przyjmujemy reguły prozy.`
    orzeczenie stawia i zwrot tylko je określa (:data:`ORZEKAJĄCE`).
    Człon następny nie zaczyna się od spójnika porównania, bo taki spójnik bywa
    odcięty przecinkiem (:data:`PORÓWNANIE`).

    Zdanie zaczynające się małą literą oddajemy bez werdyktu, tak samo jak przy
    zaimku podejmującym (:data:`PODEJMUJĄCE`) i z tego samego powodu: ekstrakcja
    cięła prozę na kropce, którą postawił przykład przytoczony w grawisach.
    """
    if not segmenty or not segmenty[0].form[:1].isupper():
        return ()
    człony = _człony(segmenty)
    znalezione = []
    for numer, człon in enumerate(człony):
        if any(_orzeka(segment, ORZEKAJĄCE) for segment in człon):
            continue
        zwrot = _zwrot_na_końcu(człon)
        if zwrot and not _porównanie(człony[numer + 1 :]):
            znalezione.append(
                Chwyt(ZASTĘPCZE_ORZECZENIE, zwrot, "zastępuje orzeczenie: powtórz czasownik")
            )
    return tuple(znalezione)


def _człony(segmenty: list[Segment]) -> list[list[Segment]]:
    """Segmenty pocięte interpunkcją na człony, bez znaków, które je rozdzielają.

    Cięcie to nie jest rozbiorem i zdania składowego nie wyznacza: człon wychodzi
    z niego i przed zdaniem względnym, i przed okolicznikiem odciętym przecinkiem.
    Regule to wystarcza, bo pyta ona tylko o człon zamknięty zwrotem,
    a nie o to, czym ten człon jest w zdaniu.

    Lista idzie tu tak, jak ją wydała segmentacja, więc segmentacja niejednoznaczna
    wkłada do jednego członu krawędzie równoległe. Reguła myli się przez to w
    stronę milczenia: forma dołożona albo postawi w członie orzeczenie, albo
    stanie za zwrotem, a jednym i drugim zgłoszenie zdejmuje.
    """
    człony: list[list[Segment]] = [[]]
    for segment in segmenty:
        if segment.form in GRANICE_CZŁONÓW:
            człony.append([])
        else:
            człony[-1].append(segment)
    return człony


def _zwrot_na_końcu(człon: list[Segment]) -> str | None:
    """Zwrot zamykający ten człon, tak jak go zdanie zapisuje, albo nic.

    Zwroty różnią się ostatnią formą, więc na jednym ogonie stanie co najwyżej
    jeden i kolejność sprawdzania nie rusza wyniku.
    """
    formy = [segment.form for segment in człon]
    for zwrot in ZASTĘPUJĄCE_ORZECZENIE:
        ogon = formy[-len(zwrot) :]
        if tuple(forma.lower() for forma in ogon) == zwrot:
            return " ".join(ogon)
    return None


def _porównanie(dalsze: list[list[Segment]]) -> bool:
    """Czy człon następny zaczyna się od spójnika porównania.

    Człon pusty jest tu tym, co daje kropka na końcu zdania, i porównaniem nie
    jest; pusty w środku zdania daje para znaków przestankowych obok siebie.
    """
    for człon in dalsze:
        if człon:
            return człon[0].form.lower() in PORÓWNANIE
    return False


def _puste_czasowniki(segmenty: list[Segment]) -> tuple[Chwyt, ...]:
    """Czasownik pusty stojący przed rzeczownikiem odczasownikowym.

    `Dokonano przeprowadzenia analizy` nazywa czynność rzeczownikiem, a czasownik
    niesie z niej sam czas i tryb, choć czynność jest jedna i czasownik ma czym ją
    orzec: `Zespół przeanalizował awarię`. Naprawą jest ten czasownik, a nie
    krótsze zdanie.

    Warunki są dwa, a każdy bierze się z tego, czego morfologia nie mówi.
    Rzeczownik stoi za czasownikiem bez niczego pomiędzy, bo o formie stojącej
    między nimi morfologia nie mówi, czy jest dopełnieniem tego czasownika;
    `Dokonano wczoraj przeprowadzenia analizy.` reguła przez to przemilcza.
    Rzeczownik nie ma czytania rzeczownikowego (:data:`RZECZOWNIKOWE`), bo forma
    czytana i jako rzeczownik zwykły stoi w prozie zwykle nim, a którym ze swoich
    czytań stoi tutaj, morfologia nie mówi: bez tego warunku
    `Rada wykonuje zadania, o których mowa w ustawie.` dostaje zgłoszenie
    za `zadania` czytane od `zadać`.
    Ceną jest milczenie nad `Bufor ulega przepełnieniu.`,
    bo `przepełnienie` jest u Morfeusza także rzeczownikiem zwykłym.
    """
    znalezione = []
    for segment, następny in zip(segmenty, segmenty[1:], strict=False):
        if not any(czytanie.lemma in PUSTE for czytanie in segment.readings):
            continue
        części = {czytanie.tag.pos for czytanie in następny.readings}
        if "ger" in części and not części & RZECZOWNIKOWE:
            znalezione.append(
                Chwyt(
                    CZASOWNIK_PUSTY,
                    f"{segment.form} {następny.form}",
                    "nazywa czynność rzeczownikiem: orzeknij ją czasownikiem",
                )
            )
    return tuple(znalezione)
