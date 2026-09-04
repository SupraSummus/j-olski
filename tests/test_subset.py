"""What olski admits, and what it refuses.

The refusals matter more than the acceptances, and there are two kinds of them:
a sentence with no reading is not olski, and a sentence with more than one is not
olski either.

O tych dwóch werdyktach rozstrzyga gramatyka, więc pyta się o nią tutaj,
i pyta się o cały podzbiór naraz: o dwa korpusy zdań, o tożsamość czytania,
o kształt odrzucenia oraz o te niezmienniki deklaracji,
które chodzą po wszystkich produkcjach.
Która produkcja zdanie wpuszcza, pyta plik swojej warstwy,
a warstwy są te same, po których rejestr konstrukcji dzieli swoje pliki
(docs/konstrukcje-gramatyczne/README.md):
``tests/test_orzeczenie.py``, ``tests/test_grupa_imienna.py``,
``tests/test_okolicznik.py``, ``tests/test_zdanie_złożone.py``
oraz ``tests/test_podrzędność.py``.

Warstwę pod gramatyką sprawdza ``tests/test_segmentacja.py``,
a odpowiedzi, które werdykt dokłada nad rozbiorem —
fragment, niedomknięcie, zatrzymanie — sprawdza ``tests/test_werdykt.py``.
Formalizm, którym podzbiór jest napisany, sprawdza ``tests/test_gramatyka.py``,
a to, co z lasu wychodzi nad zdaniem wieloznacznym, ``tests/test_las.py``.
"""

from dataclasses import fields, is_dataclass

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import EMPTY, Grammar, Production, Sym, Word, unify, word
from olski.morph import analyse
from olski.parse import PRZYŁĄCZONY_DO, parse
from olski.segmentacja import morphology, na_czym_stanęło
from olski.subset import DEKLARACJA, GRAMMAR, MIJANE, PRZECINEK, RODZINY
from tests.test_werdykt import role, verdict

# --------------------------------------------------------------------------- #
# Niezmienniki, o które pyta się całą gramatyką, a nie zdaniem
# --------------------------------------------------------------------------- #


def _symbole(produkcja: Production) -> set[str]:
    """Nazwy symboli w ciele tej produkcji; słowa nazwy nie mają."""
    return {part.name for part in produkcja.body if isinstance(part, Sym)}


def test_konstytuent_z_rolą_przyłączaną_jest_gospodarzem_albo_stoi_wśród_mijanych():
    """Symbol dopisany do gramatyki nie zostaje przezroczysty w ciszy.

    Symbol spoza ``gospodarze`` zejście od modyfikatora mija, więc rola
    przyłączana z jego wnętrza dostaje w streszczeniu gospodarza stojącego nad
    nim, a że zdania to nie odbiera i liczby czytań nie rusza, nie widzi tego
    ani suita, ani przebieg nad korpusem. Tu pyta o to gramatyka, a nie lista,
    i pyta o każdy symbol naraz.

    Podziału ten check nie wyprowadza i wyprowadzić go nie może: o tym, czy
    okolicznik w danym konstytuencie określa jego głowę, czy czasownik nad nim,
    gramatyka milczy. Żąda więc odpowiedzi, i tyle wystarcza, bo cała cena
    pominięcia bierze się z tego, że nikt o nie nie pyta.
    """
    przyłączane = set(DEKLARACJA.przyłączane)
    #  `okoliczniki` jest ciągiem tych ról i samo rolą nie jest, więc ciało z nim
    #  niesie rolę przyłączaną tak samo jak ciało z którąkolwiek z nich.
    #  Bez tej asercji rola dopisana do ciągu, a nie do `przyłączane`,
    #  zawężałaby zbiór niżej i check pytałby po cichu o mniej.
    ciąg = {
        symbol
        for produkcja in GRAMMAR.for_head("okoliczniki")
        for symbol in _symbole(produkcja)
    }
    assert ciąg <= przyłączane | {"okoliczniki"}

    niosące = {
        produkcja.head
        for produkcja in GRAMMAR.productions
        if _symbole(produkcja) & (przyłączane | {"okoliczniki"})
    }
    #  Trzy asercje zamiast jednego porównania, żeby czerwony check nazwał symbol.
    assert niosące - set(DEKLARACJA.gospodarze) - set(MIJANE) == set()
    assert set(MIJANE) - niosące == set()
    assert set(MIJANE) & set(DEKLARACJA.gospodarze) == set()


def test_deklaracje_nazywają_wyłącznie_symbole_które_gramatyka_definiuje():
    """Symbol przemianowany zostaje w deklaracji martwym napisem.

    Deklaracje są listami nazw stojącymi obok gramatyki i wpis,
    którego gramatyka nie ma, nie wywraca ani jednego wyprowadzenia: odbiera
    tylko wiersz streszczeniu, tak samo cicho jak wpis pominięty. Pola bierzemy
    z klasy, a nie z listy nazw, żeby pole dopisane później weszło pod ten check
    samo, i z tego samego powodu schodzimy do deklaracji zagnieżdżonej
    (``Obsada`` w ``olski/parse/podsumowanie.py``).
    """
    zdefiniowane = {produkcja.head for produkcja in GRAMMAR.productions}
    wypisane: set[str] = set(MIJANE)
    for deklaracja in (DEKLARACJA, *RODZINY):
        wypisane |= _nazwy(deklaracja)
    assert wypisane - zdefiniowane == set()


def _nazwy(wartość) -> set[str]:
    """Nazwy symboli wypisane w tej wartości, wraz z zagnieżdżonymi w niej deklaracjami."""
    if isinstance(wartość, str):
        return {wartość}
    if is_dataclass(wartość):
        return set().union(*(_nazwy(getattr(wartość, pole.name)) for pole in fields(wartość)))
    return set(wartość)


def test_konstytuenty_przyłączenia_są_symbolami_tej_gramatyki():
    #  Symbol przemianowany w `build` nie zgłasza się tu niczym:
    #  streszczenie nazywa wtedy całe zdanie zamiast grupy, do której przyłączenie doszło,
    #  a żaden werdykt ani żadna liczba czytań się przez to nie rusza.
    assert set(DEKLARACJA.gospodarze) <= {production.head for production in GRAMMAR.productions}


@pytest.mark.parametrize("symbol", DEKLARACJA.współrzędne)
def test_symbol_stojący_nad_sobą_ze_słowem_w_ciele_ma_w_nim_znak_koordynacji(symbol):
    #  Kryterium, na którym stoją dwie rzeczy naraz: `_koordynuje` w `olski/parse/streszczenie.py`
    #  poznaje ciąg współrzędny po tym, że symbol stoi nad sobą i że znak spinający
    #  go stoi w ciele słowem, a po tym samym poznaje go pomiar różnicowy, żeby
    #  wiedzieć, którą produkcję zdjąć. Produkcja, która to rozdziela, psuje jedno
    #  z dwóch po cichu: nawias staje tam, gdzie ciągu nie ma, albo sonda zdejmuje
    #  zdanie podrzędne zamiast koordynacji. Pusta lista łapie przemianowany symbol.
    #
    #  Samo stanie nad sobą ciągu nie znaczy: okolicznik zdaniowy dochodzący do
    #  całego ciągu stoi nad symbolem `zdanie` i znaku nie ma. Rozdziela je słowo stojące
    #  w ciele wprost i to ma je rozdzielać dalej.
    produkcje = [production for production in GRAMMAR.productions if production.head == symbol]
    assert produkcje, symbol
    for production in produkcje:
        nad_sobą = any(
            isinstance(part, Sym) and part.name == symbol for part in production.body
        )
        ze_słowem = any(isinstance(part, Word) for part in production.body)
        ze_znakiem = any(
            isinstance(part, Word) and (part == PRZECINEK or "conj" in part.pos)
            for part in production.body
        )
        assert (nad_sobą and ze_słowem) == ze_znakiem, production


def test_każda_para_ciał_okalających_symbol_ma_zapisany_porządek():
    """Ciało dopisane z jednej strony bez warunku na drugą daje napisowi dwa kształty.

    Dwie rodziny produkcji dochodzące do jednego symbolu nie mówią same z siebie,
    która dochodzi pierwsza, a pojedyncze zdanie tego nie łapie, bo ciał jest po
    kilka z każdej strony i zdanie przechodzi przez jedną ich parę
    (docs/konstrukcje-gramatyczne/okolicznik.md#określenie-przed-zdaniem-wchodzi-pod-to-które-stoi-za-nim).
    Warunek jest tu cechą, której wartości się nie przecinają, i pyta o niego
    unifikacja, więc porządek zapisany inną cechą przechodzi tak samo.
    """
    lewe, prawe = [], []
    for production in GRAMMAR.productions:
        głowa = production.body[production.głowa]
        if len(production.body) < 2 or not isinstance(głowa, Sym):
            continue
        if głowa.name != production.head:
            continue
        if production.głowa == len(production.body) - 1:
            lewe.append(production)
        elif production.głowa == 0:
            prawe.append(production)
    assert lewe and prawe, (lewe, prawe)
    for wysunięte in lewe:
        gospodarz = wysunięte.body[wysunięte.głowa].constraints
        for dostawione in prawe:
            if dostawione.head != wysunięte.head:
                continue
            wypuszczane = {
                nazwa: wartość
                for nazwa, wartość in dostawione.features
                if isinstance(wartość, frozenset)
            }
            assert unify(gospodarz, wypuszczane, EMPTY) is None, (wysunięte, dostawione)


# --------------------------------------------------------------------------- #
# Sentences olski accepts
# --------------------------------------------------------------------------- #


#: Zdania, które olski przyjmuje. Stoją jedną listą, bo pytania są o nie dwa:
#: czy się wyprowadzają i czy werdykt nad nimi milczy o formach bez licencji.
PRZYJMOWANE = [
    #  An imperative with no subject, which needs none.
    "Zapisz plik.",
    "Program zapisuje ustawienia.",
    #  Pro-drop: the subject is understood, which is ordinary Polish.
    "Zapisuje ustawienia.",
    #  An attributive adjective after its noun, as Polish terminology puts it.
    "Zapisz plik konfiguracyjny.",
    #  OVS resolved by agreement: the singular verb picks the singular noun
    #  as its subject, whatever order they come in.
    "Programy zapisuje ustawienie.",
    #  A modifier in front of the clause, which is the position where a
    #  prepositional phrase has no noun to attach to and so stays out of the
    #  attachment ambiguity the same phrase carries after an object.
    "Pod względem smaku chałka przewyższa zwykłą bułkę.",
    #  In front of the clause whatever order the clause is in, and in front
    #  of a subjectless one too.
    "Pod względem smaku zwykłą bułkę przewyższa chałka.",
    "W pliku zapisuje ustawienia.",
    #  Dopełnienie przed czasownikiem zdania, którego podmiot jest opuszczony,
    #  czyli szyk, którym ten rejestr mówi o swoich konwencjach.
    "Cenę liczymy.",
    #  A reflexive verb, which is the form with się after it. The subject is
    #  masculine personal: a nominative that is also an accusative reads as a
    #  fronted object over a subjectless clause as well.
    "Autor zapisuje się.",
    #  Przeczenie, czyli druga cząstka, którą ten podzbiór bierze.
    "Program nie zapisuje ustawień.",
    #  The copula, with a predicative agreeing with the subject and with a
    #  noun phrase in the instrumental.
    "Ludzie są wolni.",
    "Jan jest nauczycielem.",
    "Jan zostaje nauczycielem.",
    #  A predicative under a verb that is not the copula.
    "Ludzie rodzą się wolni.",
    #  Coordination, of noun phrases and of clauses.
    "Ludzie mają rozum i sumienie.",
    "Program zapisuje ustawienia i program zapisuje dane.",
    #  Przecinek przed spójnikiem, czyli ta interpunkcja, której polszczyzna żąda
    #  przed `ale` i przed `więc`, a przed `i` nie stawia jej wcale.
    "Plany są niczym, ale planowanie jest wszystkim.",
    "Program zapisuje ustawienia, więc linter sprawdza polszczyznę.",
    #  Dwukropek otwierający zdanie, czyli ten, którym ten rejestr wprowadza
    #  wyjaśnienie. Obie połowy wyprowadzają się osobno i osobno raz.
    "Cena jest niska: gramatyka jest bezkontekstowa.",
    #  A modal and its infinitive, agreeing with the subject in gender
    #  because powinien inflects for one and not for person.
    "Ludzie powinni postępować.",
    #  Bezokolicznik pod zwykłym czasownikiem, i łańcuch bezokoliczników,
    #  którego żadna reguła nie opisuje: fraza bezokolicznikowa bierze
    #  dopełnienia, a jest jednym z nich.
    "Program pozwala zapisać ustawienia.",
    "To ma pomagać pisać dobrą polszczyznę.",
    #  Okolicznik przed orzecznikiem w narzędniku i przed bezokolicznikiem, czyli
    #  dwie z pozycji, których lista dopełnień nie miała, choć polszczyzna je ma.
    "Arek jest w głębi serca monogamistą.",
    "Musi na niego skoczyć.",
    #  Termin z przymiotnikiem za rzeczownikiem i dopełniaczem pod nim, czyli
    #  kształt, którym rejestr ustaw nazywa swoje terminy. Zdanie jest § 54
    #  „Zasad techniki prawodawczej”; docs/ustawy.md mierzy, ile ta pozycja daje.
    "Podstawową jednostką redakcyjną ustawy jest artykuł.",
    #  A pronoun subject, and with it a person that is not the third.
    "Ja zapisuję plik.",
    #  Czas przeszły, czyli forma, która niesie rodzaj i nie niesie osoby.
    "Program zapisywał ustawienia.",
    #  Osoba pierwsza tego czasu, czyli aglutynant, którego Morfeusz odcina od
    #  formy: Napisałem wchodzi tu jako Napisał i em.
    "Napisałem program.",
    #  Czas przeszły dochodzi też do formy z cząstką `się`, czyli do drugiego
    #  leksykonu walencyjnego, a nie tylko do tego bez cząstki.
    "Program otwierał się.",
    #  Tryb przypuszczający, czyli ten sam czas z cząstką `by` za sobą, w osobie
    #  trzeciej i w pierwszej.
    "Czytelnik nie odzyskałby ról.",
    "Napisałbym program.",
    #  Czas przyszły `być`, czyli forma `bedzie` stojąca sama, z orzecznikiem
    #  zgodnym i z narzędnikowym.
    "Cena będzie niska.",
    "Parser będzie celem.",
    #  Czas przyszły złożony, czyli ta sama forma nad czasownikiem niedokonanym:
    #  raz nad formą na -ł, która wnosi rodzaj, raz nad bezokolicznikiem, który
    #  rodzaju nie wnosi.
    "Program będzie zapisywał ustawienia.",
    "Program będzie zapisywać ustawienia.",
    #  Ten sam tryb pod spójnikiem, który cząstkę niesie sam, w obu miejscach
    #  okolicznika. Zdanie pod takim spójnikiem stoi w formie na -ł bez cząstki.
    "Program zapisuje ustawienia, żeby linter sprawdził polszczyznę.",
    "Gdyby linter sprawdził polszczyznę, program zapisuje ustawienia.",
    #  Fraza bezokolicznikowa pod tym samym spójnikiem, czyli to, czym ten rejestr
    #  wyraża cel najczęściej.
    "Program zapisuje ustawienia, aby sprawdzić polszczyznę.",
    "Aby sprawdzić polszczyznę, program zapisuje ustawienia.",
    #  Człon, którego czasownik ten rejestr opuszcza, czyli grupa imienna za
    #  spójnikiem i bez orzeczenia nad sobą.
    "Parser jest tani, czyli Morfeusz.",
    #  Spójnik stojący wewnątrz swojego zdania, a nie na jego czele.
    "Milczenie jest zatem wartością.",
    #  Ten sam spójnik na czele całego zdania, w obu częściach mowy, którymi
    #  Morfeusz tę klasę zapisuje: `i` jest tam `conj`, a `zatem` `comp`.
    "I nikt tego nie zauważył.",
    "Zatem milczenie jest wartością.",
    #  Przymiotnik za zaimkiem, którym pyta się o osobę i o rzecz.
    "Kto pierwszy wstaje od stołu?",
    #  Okoliczność wyrażona samym narzędnikiem, w obu miejscach, które okolicznik
    #  ma za czasownikiem: przy dopełnieniu i bez niego.
    "Mieszczanie zabili okna deskami.",
    "Wziął lustro wieczorem.",
    #  liczebnik zgodny w orzeczniku, czyli zdanie mówiące, ile czegoś jest.
    "Tory są dwa.",
    #  Kopula, którą lista dostała razem z tym orzecznikiem.
    "Odpowiedzią bywa decyzja.",
    #  Spójnik skorelowany na obu poziomach, które go dostały.
    "Ani parser nie rośnie, ani linter nie sprawdza.",
    "Ani parser, ani linter nie rośnie.",
    #  Grupa imienna za dwukropkiem, czyli wyliczenie tego, co zdanie przed nim
    #  nazwało liczbą.
    "Gramatyka ma dwie role: podmiot i dopełnienie.",
    #  Zaimek zwrotny w dopełnieniu i pod przyimkiem, czyli w obu pozycjach, które
    #  ta część mowy zajmuje. Przypadek jest jedyną cechą, którą ona niesie.
    "Widzę siebie.",
    "Osie są od siebie niezależne.",
    #  Czas przyszły predykatywu, czyli forma `bedzie` za słowem, które orzeka bez
    #  podmiotu i bez czasownika.
    "Trzeba będzie zmierzyć cenę.",
    #  Imiesłów przysłówkowy w obu miejscach okolicznika, i osobno bez wypełnienia.
    "Program zapisuje ustawienia, sprawdzając zgodność.",
    "Sprawdzając zgodność, program zapisuje ustawienia.",
    "Program zapisuje ustawienia, milcząc.",
    #  Para myślników wraz z każdym z trzech wypełnień, jakie ta gramatyka jej daje.
    #  Każde z nich wychodzi jednym czytaniem, bo miejsce pary wskazują dwa znaki.
    "Cena — pokrycie — jest niska.",
    "Cena — w prozie — jest niska.",
    "Cena — gramatyka rośnie — jest niska.",
    #  Ta sama para, a za nią myślnik rozdzielający dwa zdania: znaki są trzy,
    #  a czytanie zostaje jedno.
    "Cena — pokrycie — jest niska — parser rośnie.",
    #  Ciąg współrzędny wyrażeń przyimkowych, oboma spinaczami. Przyimek stoi
    #  przed każdym członem, a przypadek każdy z nich bierze od swojego.
    "Cena stoi w prozie i w kodzie.",
    "Działa w Polsce, w okolicach Kielc.",
]


#: Zdania, którym okolicznik narzędnikowy zabrał jednoznaczność, a nie odczytanie,
#: więc stoją tu, a nie wśród przyjmowanych, choć pytanie drugie jest o nie to samo.
#: Każde niesie formę, którą słownik czyta i w narzędniku, i w przypadku roli,
#: jaką ona tu zajmuje, więc drugie czytanie stawia ją okolicznikiem;
#: cenę tę trzyma
#: docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika.
WIELOZNACZNE_PRZEZ_NARZĘDNIK = [
    #  Notacja rejestru w roli dopełnienia, czyli jedno zdanie README. Czytanie
    #  nieodmienne spełnia każde żądanie przypadku (`olski/segmentacja.py`),
    #  więc spełnia i to.
    "Zobacz docs/subset.md.",
    #  Zdanie, którego graf segmentacji się rozchodzi: Morfeusz dzieli Ktoś
    #  na Kto i ś obok formy całej, a ś nie ma ani jednego czytania, które
    #  bierze jakakolwiek produkcja.
    "Ktoś zna docs/subset.md.",
    #  Pytanie zależne za dwukropkiem, czyli trzecia rzecz, jaką ten znak bierze.
    #  Tu narzędnik jest prawdziwy — `jednym pytaniem` sprawdza się coś — więc
    #  czytanie pierwsze jest tym, którego to zdanie nie miało przed tą pozycją.
    "Sprawdzasz to jednym pytaniem: czy skreślona rzecz jest powiedziana gdzie indziej?",
]


@pytest.mark.parametrize("text", PRZYJMOWANE)
def test_these_are_olski(text):
    assert verdict(text).status == "valid", verdict(text).explain()


@pytest.mark.parametrize("text", [*PRZYJMOWANE, *WIELOZNACZNE_PRZEZ_NARZĘDNIK])
def test_zdanie_z_czytaniem_nie_zgłasza_żadnej_formy(text):
    #  Usterka, którą to łapie: werdykt nad zdaniem przyjętym nazywa ś z Ktoś,
    #  czyli krawędź, której ścieżka tego czytania w ogóle nie bierze.
    assert verdict(text).nielicencjonowane == ()


def test_a_valid_sentence_says_what_fills_each_role():
    roles = role(verdict("Program zapisuje ustawienia."))[0]
    assert roles["podmiot"] == "Program"
    assert roles["dopełnienie"] == "ustawienia"
    assert roles["orzeczenie"] == "zapisuje"


# --------------------------------------------------------------------------- #
# Sentences with no reading
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "text",
    [
        #  Gender disagreement between adjective and noun.
        "Nowa program zapisuje ustawienia.",
        #  The verb is plural and neither noun is.
        "Program zapisują ustawienie.",
        #  A form Morfeusz does not know cannot be given a part of speech.
        "Program zapisuje plikx.",
        #  The predicative disagrees with the subject in gender.
        "Ludzie są wolna.",
        #  So does the modal, which inflects for gender and not for person.
        "Ludzie powinna postępować.",
        #  A first person subject with a third person verb: person comes from
        #  the subject, so this disagrees the way Nowa program does.
        "Ja zapisuje plik.",
        #  Czas przeszły zgadza się z podmiotem w rodzaju, a nie tylko w liczbie,
        #  i to jest ta zgodność, której czas teraźniejszy nie ma czym złamać.
        "Lista stał.",
        #  Osobę trzecią wpisuje formie praet produkcja, bo tag jej nie niesie,
        #  a bez tego podmiot pierwszej osoby nie ma się z czym nie zgodzić.
        "Ja napisał program.",
        #  Osoba, którą wnosi aglutynant, jest osobą całego orzeczenia, więc
        #  podmiot drugiej osoby przy końcówce pierwszej się nie zgadza.
        "Ty napisałem program.",
        #  Spójnik, przed którym polszczyzna stawia przecinek, bez tego przecinka.
        #  Oba zdania wyprowadzały się, dopóki jeden terminal brał całą klasę
        #  `conj`, i były to napisy, których polszczyzna nie ma. Drugie jest
        #  koordynacją przymiotników, czyli poziomem, który pozycji z przecinkiem
        #  nie ma wcale, więc wychodziło jednym czytaniem.
        "Program zapisuje ustawienia ale linter sprawdza polszczyznę.",
        "Plik jest nowy ale duży.",
        #  Spójnik niosący cząstkę trybu żąda formy na -ł, a forma osobowa jej nie
        #  jest. Bez cechy trybu nad zdaniem oba te napisy się wyprowadzają, bo
        #  cechy, której konstytuent nie niesie, unifikacja nie sprawdza.
        "Program zapisuje ustawienia, żeby linter sprawdza tekst.",
        "Gdyby linter sprawdza tekst, program zapisuje ustawienia.",
        #  Cząstka stoi raz: w spójniku albo przy czasowniku, a nie w obu miejscach.
        "Program zapisuje ustawienia, żeby linter sprawdziłby tekst.",
        #  Aglutynant zajmuje miejsce, które pod takim spójnikiem zajmuje jego
        #  własna końcówka: polszczyzna ma `żebym napisał`, a nie `żeby napisałem`.
        "Program zapisuje ustawienia, żeby napisałem plik.",
        #  Liczbę niesie w czasie przyszłym złożonym forma `bedzie`, a bezokolicznik
        #  pod nią nie niesie ani liczby, ani rodzaju, więc bez liczby ogłoszonej
        #  przez samo ciało zdanie to się wyprowadza.
        "Programy będzie zapisywać ustawienia.",
        #  Rodzaj wnosi w tym czasie forma na -ł i to jest ta zgodność, której
        #  wariant z bezokolicznikiem nie ma czym złamać.
        "Lista będzie stał.",
        #  Ten czas składa się z czasownikiem niedokonanym i z żadnym innym, więc
        #  `zapisywał` wchodzi, a `zapisał` nie: `będzie zapisał` nie jest niczym.
        "Program będzie zapisał ustawienia.",
        #  Liczbę i osobę formy `bedzie` przy predykatywie wpisuje ciało, bo
        #  predykatyw nie niesie ani jednej, a cechy, której konstytuent nie
        #  niesie, unifikacja nie sprawdza: bez tych dwóch wartości oba te napisy
        #  się wyprowadzają.
        "Trzeba będą zmierzyć cenę.",
        "Trzeba będziesz zmierzyć cenę.",
        #  Mianownika ta część mowy nie ma, więc podmiotem ten zaimek nie bywa.
        "Siebie zapisuje ustawienia.",
        #  Zaimek zwrotny wchodzi terminalem właśnie po to: jako ciało grupy
        #  imiennej nie niósłby liczby ani rodzaju, a cechy, której konstytuent
        #  nie niesie, unifikacja nie sprawdza, więc zdanie względne zgodziłoby
        #  się z nim w każdej.
        "Widzę siebie, która stoi.",
        #  Para myślników niedomknięta, czyli znak jeden tam, gdzie wtrącenie żąda
        #  dwóch. Licencji udzielają jej oba znaki, tak samo jak przy nawiasie
        #  i przy cudzysłowie.
        "Cena — pokrycie jest niska.",
    ],
)
def test_these_have_no_reading(text):
    assert verdict(text).status == "rejected"


def test_odrzucenie_odróżnia_formę_bez_produkcji_od_struktury_bez_produkcji():
    #  Dwie odpowiedzi, które Świgra trzyma osobno, i dwie różne roboty do
    #  zrobienia. Formy, której Morfeusz odmienioną nie zna, nie bierze żaden
    #  terminal; Nowa program ma każdą formę wziętą i stoi na zgodności rodzaju,
    #  więc test pilnuje, żeby zdania zostały dwa.
    #
    #  Formą jest tu nazwa obca, a nie `commitów`, bo słowo, które leksykon
    #  projektu nazywa, ma czytania i licencję (`olski.toml`), więc
    #  odpowiedź pierwszą pokazuje dopiero forma spoza tego leksykonu.
    forma = verdict("Modele stawiają prozę wyżej od New Yorkera.")
    assert forma.nielicencjonowane == ("Yorkera",)
    assert "żadna produkcja nie bierze" in forma.explain()
    struktura = verdict("Nowa program zapisuje ustawienia.")
    assert struktura.nielicencjonowane == ()
    #  Zdanie to stoi w README jako przykład odrzucenia, więc jego werdykt stoi
    #  tam wypisany co do znaku. Analiza dochodzi tu do końca, bo tablica domyka
    #  pozycję po samym kształcie ciała, a o cechy pyta dopiero unifikacja po
    #  lesie, więc `program` staje w tablicy okolicznikiem narzędnikowym i ginie
    #  dopiero na przypadku.
    #  Że werdykt mówi, dokąd analiza doszła, a nie gdzie stoi usterka, wywodzi
    #  docs/subset.md#odrzucenie-mówi-dokąd-analiza-doszła-a-nie-gdzie-stoi-usterka.
    assert struktura.explain() == (
        "brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania"
    )


def test_licencja_bierze_się_z_gramatyki_a_nie_z_listy_obok_niej():
    #  Gramatyka, która nie ma czasownika, przestaje licencjonować jego czytanie:
    #  gdyby licencja stała napisana obok, ta zmiana nie doszłaby do niej wcale.
    uboga = Grammar(start="grupa_imienna")
    uboga.rule("grupa_imienna", [word("subst")])
    [segment] = analyse("zapisuje")
    czytanie = next(r for r in segment.readings if r.tag.pos == "fin")
    cechy = czytanie.tag.cechy
    lematy = segment.lematy
    assert not uboga.licencjonuje(czytanie.tag.pos, czytanie.lemma, lematy, cechy)
    assert GRAMMAR.licencjonuje(czytanie.tag.pos, czytanie.lemma, lematy, cechy)


def test_odrzucenie_nazywa_formę_na_której_analiza_stanęła():
    #  Polish puts a comma in front of ale and this sentence has none, so no level
    #  of coordination derives it and the analysis stops on the conjunction itself.
    #  The form is licensed all the same, by the position that has the comma, so
    #  the list of unlicensed forms is empty and the furthest point is what says
    #  where the sentence ran out.
    zdanie = "Plany są niczym ale planowanie jest wszystkim."
    assert parse(GRAMMAR, morphology(zdanie)).furthest == 3
    assert verdict(zdanie).explain() == "brak odczytania: analiza staje na „ale”"


def test_zdanie_którego_nic_nie_domyka_nie_nazywa_znaku_kończącego_jako_zatrzymania():
    #  Liczebnika rządzącego w orzeczniku ta gramatyka nie ma — `Torów jest dwa.`
    #  ma go, a `Warstwy są dwie.` stoi na liczebniku zgodnym i wchodzi
    #  (docs/konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-orzeka-o-tym-ile-czegoś-jest) — więc żadna analiza
    #  nie zamyka tu zdania, choć każdą jego formę bierze jakaś produkcja.
    #  Zatrzymanie pada wtedy na kropce, a werdykt nazywający kropkę kazałby
    #  autorowi poprawić interpunkcję.
    werdykt = verdict("Cena jest dwa.")
    assert werdykt.status == "rejected"
    assert werdykt.zatrzymanie is None
    assert werdykt.explain() == (
        "brak odczytania: analiza dochodzi do końca, a nic nie domyka zdania"
    )


def test_zatrzymanie_nazywa_formę_którą_autor_napisał_a_nie_jej_część():
    #  Morfeusz widzi w `kiedyś` także `kiedy` i `ś`, więc z jednego węzła grafu
    #  wychodzą dwie krawędzie, a krótsza jest częścią dłuższej. Nazwana bez
    #  wyboru — pierwsza z brzegu — mówiłaby autorowi o słowie, którego w zdaniu
    #  nie ma, i mówiłaby to zależnie od kolejności krawędzi.
    segmenty = morphology("Liczbę napisano kiedyś.")
    [węzeł] = {segment.start for segment in segmenty if segment.form == "kiedy"}
    assert na_czym_stanęło(segmenty, węzeł).form == "kiedyś"


# --------------------------------------------------------------------------- #
# Sentences with more than one reading, which olski refuses just as firmly
# --------------------------------------------------------------------------- #


def test_case_syncretism_plus_free_word_order_makes_a_sentence_ambiguous():
    #  koszt is nominative or accusative and Polish permits both SVO and OVS,
    #  so this sentence does not say which cost is the greater one.
    found = verdict("Koszt samej szynki przewyższa koszt szynki z dodatkami.")
    assert found.status == "ambiguous"
    subjects = {reading["podmiot"] for reading in role(found)}
    #  Trzeci podmiot jest z drugiej wieloznaczności, nie z tej: z dodatkami
    #  dochodzi do zdania zamiast do kosztu, więc podmiotem zostaje sam koszt.
    assert subjects == {"Koszt samej szynki", "koszt szynki z dodatkami", "koszt szynki"}
    assert "podmiot" in found.explain()


def test_the_same_comparison_is_unambiguous_when_the_cases_are_not_syncretic():
    #  Same verb in the same frame as the sentence above, but chałka is
    #  nominative only and bułkę accusative only, so OVS has nowhere to derive:
    #  what that sentence loses, it loses to the syncretism and not to the verb.
    found = verdict("Chałka przewyższa zwykłą bułkę.")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {"podmiot": "Chałka", "dopełnienie": "zwykłą bułkę", "orzeczenie": "przewyższa"}
    ]


@pytest.mark.parametrize(
    "text",
    [
        "Program zapisuje ustawienia w pliku.",
        "Program zapisuje ustawienia w pliku konfiguracyjnym.",
        #  Here the phrase cannot be dropped: przewyższać compares along a
        #  dimension, so naming it is what makes the comparison read like Polish.
        "Chałka przewyższa zwykłą bułkę pod względem smaku.",
    ],
)
def test_prepositional_attachment_is_reported_as_the_ambiguity_it_is(text):
    #  w pliku attaches to the verb or to the object, and the two readings are
    #  different claims about where the settings are. Nearly every sentence with
    #  a prepositional phrase is ambiguous this way, which is the largest
    #  habitability cost the uniqueness property has run into so far.
    found = verdict(text)
    assert found.status == "ambiguous"
    assert len({reading["dopełnienie"] for reading in role(found)}) == 2


def test_czytania_różne_samym_przyłączeniem_wychodzą_osobnymi_streszczeniami():
    #  W tym zdaniu stoją dwie wieloznaczności naraz i po rolach widać jedną:
    #  dwie pary czytań różnią się samym miejscem, do którego doszło `z dodatkami`,
    #  a formy nad nim stojące zostają w każdej parze te same.
    #  Streszczenie, które przyłączenia nie nazywa, oddaje więc cztery napisy na sześć czytań
    #  i o dwóch milczy, choć są to dwa różne zdania o szynce.
    found = verdict("Koszt samej szynki przewyższa koszt szynki z dodatkami.")
    napisy = {tuple(sorted(reading.items())) for reading in role(found)}
    assert len(napisy) == len(role(found)) == 6
    assert {reading["wyrażenie_przyimkowe"] for reading in role(found)} == {
        "z dodatkami → koszt",
        "z dodatkami → szynki",
        "z dodatkami → przewyższa",
    }


def test_werdykt_rośnie_z_liczbą_wyborów_a_nie_z_liczbą_czytań():
    #  Drugie zdanie ma szesnaście razy więcej czytań niż pierwsze i trzy razy
    #  więcej nierozstrzygniętych przyłączeń, i to ta druga krotność ma stać w
    #  werdykcie. Na tych dwóch napisach stoi sekcja docs/design-notes.md o
    #  werdykcie jako zapytaniu o las, więc padają razem.
    dwa = verdict("Program zapisuje ustawienia w pliku w katalogu.")
    sześć = verdict(
        "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci w firmie w kraju."
    )
    assert dwa.explain() == (
        "4 odczytania, różne w roli: dopełnienie; "
        "„w pliku” → „zapisuje”, „ustawienia”; "
        "„w katalogu” → „zapisuje”, „pliku”"
    )
    assert sześć.explain().count(PRZYŁĄCZONY_DO) == 6
    assert sześć.explain().startswith("64 odczytania, różne w roli: dopełnienie; „w pliku” → ")


def test_pierwszy_artykuł_deklaracji_stoi_na_przyłączeniu_wyrażenia_przyimkowego():
    #  Zdanie, które wpędziło do gramatyki konstrukcje wyliczone wyżej: czasownik
    #  zwrotny, orzecznik i dopełniacz w koordynacji, kwantyfikator. Wszystkie w
    #  nim są, a zdaniem olskim nie jest, bo pod względem swej godności określa
    #  samych równych, oboje albo całe zdanie, i te trzy czytania olski melduje
    #  zamiast wybierać jedno z nich.
    found = verdict(
        "Wszyscy ludzie rodzą się wolni i równi "
        "pod względem swej godności i swych praw."
    )
    assert found.status == "ambiguous", found.explain()
    #  Nawias nazywa człon, w którym wyrażenie się znalazło, i tym odróżnia dwa
    #  zasięgi wewnątrz orzecznika: ciąg wiąże się w prawo, więc pod członem
    #  ostatnim wzgląd określa samych równych, a nad ciągiem oboje. Czytanie
    #  trzecie zostawia orzecznik bez wyrażenia, bo wzgląd doszedł tam do zdania
    #  (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    assert {reading["orzecznik"] for reading in role(found)} == {
        "wolni i równi",
        "wolni i [równi pod względem swej godności i swych praw]",
        "wolni i równi [pod względem swej godności i swych praw]",
    }


def test_the_second_article_sentence_derives_and_is_still_not_olski():
    #  Everything it needs is in the grammar — verb before subject with a
    #  predicative, a participle with its instrumental complement, a modal, two
    #  coordinations — and what stops it is the attachment problem alone: w
    #  duchu braterstwa is an adjunct of postępować or a modifier of innych.
    found = verdict(
        "Są oni obdarzeni rozumem i sumieniem "
        "i powinni postępować wobec innych w duchu braterstwa."
    )
    assert found.status == "ambiguous"
    #  Okolicznik stoi w drugim zdaniu składowym, więc pytamy o streszczenie tamtego
    #  składowego, a nie o pierwsze z dwóch.
    #
    #  Dwa ostatnie wiersze są ceną przysłówka i nie są przyłączeniem: Morfeusz
    #  daje formie `wobec` czytanie przysłówkowe obok przyimkowego, więc okolicznik
    #  zdania bierze ją jako słowo, a `innych` zostaje wtedy dopełnieniem. Jest to
    #  czytanie, którego polszczyzna w tym miejscu nie ma, i klasa, po którą
    #  `admissible` nie sięga, bo tamten warunek pyta o czytanie rzeczownikowe.
    assert {drugie["wyrażenie_przyimkowe"] for _pierwsze, drugie in found.readings} == {
        "wobec innych → postępować",
        "wobec innych w duchu → postępować",
        "wobec innych w duchu braterstwa → postępować",
        "w duchu braterstwa → postępować",
        "w duchu braterstwa → innych",
    }


def test_readings_differing_only_in_lemma_or_feature_values_are_one_reading():
    #  zapisuje belongs to two homonymous verbs, and ustawienia has several
    #  noun readings. None of that gives a reader anything to choose between,
    #  so the sentence has one reading.
    assert len(verdict("Program zapisuje ustawienia.").result.readings) == 1


def test_czytania_różniące_się_samą_częścią_mowy_są_jednym_czytaniem():
    #  go jest zaimkiem i jest grą, a dopełnieniem jest jedno słowo tak czy tak,
    #  więc oba wyprowadzenia mają ten sam kształt i czytelnik nie ma między czym
    #  wybierać. Dochodzą tam dwiema produkcjami, a nie jednym terminalem, i jest
    #  to zarazem czytanie, po które wykluczenie ze słownika nie sięga.
    assert verdict("Znam go.").status == "valid"
