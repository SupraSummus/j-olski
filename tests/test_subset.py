"""What olski admits, and what it refuses.

The refusals matter more than the acceptances, and there are two kinds of them:
a sentence with no reading is not olski, and a sentence with more than one is not
olski either.

O tych dwóch werdyktach rozstrzyga gramatyka, więc pyta się o nią tutaj.
Warstwę pod nią sprawdza ``tests/test_segmentacja.py``,
a odpowiedzi, które werdykt dokłada nad rozbiorem —
fragment, niedomknięcie, zatrzymanie — sprawdza ``tests/test_werdykt.py``.
Formalizm, którym podzbiór jest napisany, sprawdza ``tests/test_gramatyka.py``,
a to, co z lasu wychodzi nad zdaniem wieloznacznym, ``tests/test_las.py``.
Deklaracja zostaje tutaj, bo jest wypisana obok tych produkcji
i rozejść się może już tylko z nimi.
"""

from dataclasses import fields

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import (
    EMPTY,
    Grammar,
    Production,
    Sym,
    Var,
    Word,
    bierze,
    unify,
    word,
)
from olski.lematy import KOPULA
from olski.morph import analyse, generuj
from olski.parse import (
    PRZYŁĄCZONY_DO,
    parse,
    streszczenia,
)
from olski.segmentacja import bez_licencji, morphology, na_czym_stanęło
from olski.subset import (
    CZĄSTKA_ZDANIA,
    CZĄSTKI,
    DEKLARACJA,
    GRAMMAR,
    GRUPA_PYTAJNA,
    MIJANE,
    OKOLICZNIK_PRZYSŁÓWKOWY,
    OKOLICZNIK_ZDANIOWY,
    ORZECZENIE_BEZOSOBOWE,
    ORZECZENIE_RZECZOWNIKOWE,
    ORZECZNIK_ŁĄCZNIKA,
    PREDYKATYWY,
    PRZECINEK,
    RAMA_BEZ_BIERNIKA,
    RODZINY,
    SPÓJNIK_BEZ_PRZECINKA,
    SPÓJNIK_PRZECINKOWY,
    SPÓJNIK_PYTAJNY,
    SPÓJNIKI_PRZECINKOWE,
    SPÓJNIKI_SKORELOWANE,
    WALENCJA,
    WALENCJA_ZWROTNA,
    WTRĄCENIE,
    WYRAŻENIE_PRZYIMKOWE,
)
from tests.test_werdykt import role, verdict

# --------------------------------------------------------------------------- #
# Deklaracja zgadza się z gramatyką, obok której jest wypisana
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

    Deklaracje są listami nazw stojącymi obok gramatyki (CLAUDE.md#code) i wpis,
    którego gramatyka nie ma, nie wywraca ani jednego wyprowadzenia: odbiera
    tylko wiersz streszczeniu, tak samo cicho jak wpis pominięty. Pola bierzemy
    z klasy, a nie z listy nazw, żeby pole dopisane później weszło pod ten check
    samo.
    """
    zdefiniowane = {produkcja.head for produkcja in GRAMMAR.productions}
    wypisane: set[str] = set(MIJANE)
    for deklaracja in (DEKLARACJA, *RODZINY):
        for pole in fields(deklaracja):
            wartość = getattr(deklaracja, pole.name)
            wypisane |= {wartość} if isinstance(wartość, str) else set(wartość)
    assert wypisane - zdefiniowane == set()


def _po_głowach(symbol: str, widziane: set[str] | None = None) -> set[str]:
    """Symbole, do których schodzi się od tego samymi głowami ciał."""
    widziane = set() if widziane is None else widziane
    for produkcja in GRAMMAR.for_head(symbol):
        if not produkcja.body:
            continue
        głowa = produkcja.body[produkcja.głowa]
        if isinstance(głowa, Sym) and głowa.name not in widziane:
            widziane.add(głowa.name)
            _po_głowach(głowa.name, widziane)
    return widziane


def test_symbol_opakowujący_rodzinę_czoła_ma_pod_głową_jej_rdzeń():
    """Rodzina wypisana ręką ma stać zgodnie z tym, co gramatyka wyprowadza.

    Cztery miejsca czytają dziś jedną :class:`Rodzina`, więc rozejść się może
    już tylko ona sama z gramatyką, i najciszej wtedy, gdy nazwa jest symbolem
    prawdziwym, tylko cudzym: symbol opakowujący wpisany do niewłaściwej rodziny
    zatrzymuje streszczenie tam, gdzie role są rolami zdania nad nim.

    Pytamy o łańcuch głów, a nie o córkę ani o dosięgnięcie w ogóle: zdanie
    pytające dochodzi do swojego rdzenia przez ciąg pytań, więc córką rdzeń nie
    jest, a dosięgnąć stąd można prawie każdego symbolu, bo zdanie podrzędne ma
    pod sobą całe zdanie.
    """
    rdzenie = {rodzina.rdzeń for rodzina in RODZINY}
    for rodzina in RODZINY:
        for symbol in rodzina.opakowujące:
            assert _po_głowach(symbol) & rdzenie == {rodzina.rdzeń}, symbol


def test_przyimek_pod_zaimkiem_pytajnym_dostaje_w_werdykcie_swojego_gospodarza():
    """Czoło pytania zatrzymuje zejście, bo przyimek pod nim określa sam zaimek.

    Czytań pominięcie takiego gospodarza nie rusza, więc nie widać go po ich
    liczbie: zejście mija wtedy czoło i oba czytania dostają jednego gospodarza,
    czyli orzeczenie, choć w pierwszym z nich przyimek stoi pod `Kto`.
    """
    found = verdict("Kto z posłów zapisuje ustawienia?")
    assert found.result.ile == 2, found.explain()
    [przyłączenie] = found.result.przyłączenia
    assert przyłączenie.modyfikator == "z posłów"
    assert przyłączenie.gospodarze == ("Kto", "zapisuje")


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


def test_termin_z_dopełniaczem_bierze_wyrażenie_przyimkowe_na_własną_głowę():
    #  Usterka, przed którą to broni: pozycja z przymiotnikiem i dopełniaczem
    #  dopisana bez swojej pozycji z okolicznikiem za nią. Zdanie zostaje wtedy
    #  wieloznaczne, więc po werdykcie nie widać, że w pliku nie dochodzi już do
    #  samych ustawień, choć polszczyzna to czytanie ma — i stąd liczba obok
    #  zbioru, bo dwa z trzech czytań mają to samo dopełnienie i różnią się
    #  wewnątrz niego, czyli tym, do czego w pliku doszło
    #  (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    found = verdict("Program zapisuje ustawienia domyślne użytkownika w pliku.")
    assert found.status == "ambiguous", found.explain()
    assert len(found.readings) == 3
    assert {reading["dopełnienie"] for reading in role(found)} == {
        "ustawienia domyślne użytkownika w pliku",
        "ustawienia domyślne użytkownika",
    }


def test_predykatyw_przed_czasownikiem_nie_jest_czytany_jako_podmiot():
    #  Lustro reguły OVS. Bez niego ten sam szyk wychodził raz tak, a raz wcale,
    #  zależnie od tego, czy po czasowniku stoi dopełnienie, czy orzecznik, a
    #  ryzykiem przy nim jest zamiana ról: podmiot stoi tu za czasownikiem.
    found = verdict("Wejściem jest zwykły tekst polski.")
    assert found.status == "valid", found.explain()
    assert role(found)[0] == {
        "podmiot": "zwykły tekst polski",
        "orzecznik": "Wejściem",
        "orzeczenie": "jest",
    }


def test_a_valid_sentence_says_what_fills_each_role():
    roles = role(verdict("Program zapisuje ustawienia."))[0]
    assert roles["podmiot"] == "Program"
    assert roles["dopełnienie"] == "ustawienia"
    assert roles["orzeczenie"] == "zapisuje"


def test_a_fronted_modifier_belongs_to_the_clause_and_not_to_the_subject():
    #  Nothing but the clause rule can take it there, and the failure to guard
    #  against is the subject swallowing it: człon_imienny → subst wyrażenie_przyimkowe makes
    #  the same phrase between the subject and the verb come out valid and wrong.
    roles = role(verdict("Pod względem smaku chałka przewyższa zwykłą bułkę."))[0]
    assert roles["podmiot"] == "chałka"
    #  Streszczenie nazywa konstytuent, do którego przyłączenie doszło, jego
    #  głową, więc zdanie z nazwy tego testu stoi w samym napisie, a nie tylko w
    #  podmiocie obok: gospodarzem jest tu czasownik, a nie `chałka`.
    assert roles["wyrażenie_przyimkowe"] == "Pod względem smaku → przewyższa"


def test_object_first_order_is_polish_and_is_read_that_way():
    #  Free word order is real: here the plural verb forces the plural noun to
    #  be the subject, so the sentence is unambiguous despite the OVS order.
    roles = role(verdict("Program zapisują ustawienia."))[0]
    assert roles["podmiot"] == "ustawienia"
    assert roles["dopełnienie"] == "Program"


def test_dopełniacz_negacji_przed_czasownikiem_ma_czym_się_wyprowadzić():
    #  Bez szyku SOV `tego` brała tu tylko przydawka dopełniaczowa, więc zdanie
    #  wychodziło jednym czytaniem, pewnym siebie i odwrotnym niż drzewo wzorcowe.
    #  Usterka, którą to łapie, jest powrotem tamtego stanu: zdanie znów wychodzi
    #  jednoznaczne, a rola, którą czyta czytelnik, nie ma ciała.
    found = verdict("Apostołowie tego nie praktykowali.")
    assert found.status == "ambiguous", found.explain()
    czytania = {(reading.get("podmiot"), reading.get("dopełnienie")) for reading in role(found)}
    assert ("Apostołowie", "tego") in czytania, found.explain()
    assert ("Apostołowie tego", None) in czytania, found.explain()


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
    ],
)
def test_these_have_no_reading(text):
    assert verdict(text).status == "rejected"


def test_coordination_does_not_loosen_agreement_inside_a_conjunct():
    #  The failure to guard against: an adjective scoping over the whole
    #  coordination, which would let a singular feminine one head two masculine
    #  plural nouns. An adjective attaches inside a conjunct, so nowe programy i
    #  pliki is [nowe programy] i [pliki] and the disagreement below has nowhere
    #  to hide.
    assert verdict("Nowa programy i pliki mają nazwy.").status == "rejected"


@pytest.mark.parametrize(
    "zdanie",
    [
        "Wstaję, wyglądam przez okno.",
        "Kobiety muszą zakrywać włosy, ramiona, nogi.",
        "Plik jest nowy, duży.",
    ],
)
def test_przecinek_koordynuje_na_każdym_poziomie_i_wyprowadza_raz(zdanie: str):
    #  Trzy poziomy, bo przecinek dopisany do dwóch z nich zostawia trzeci na
    #  spójniku i nikt tego nie zobaczy po zdaniu odrzuconym gdzie indziej. Raz,
    #  a nie w ogóle: przecinek zdaniowy miał konkurować z przecinkiem w grupie
    #  imiennej, a docs/subset.md trzyma pomiar mówiący, ile tej konkurencji
    #  jest nad bankiem drzew.
    assert verdict(zdanie).status == "valid"


def test_koordynacja_przecinkiem_żąda_zgodności_tak_samo_jak_spójnik():
    #  Usterka, przed którą to stoi: produkcja z przecinkiem dopisana bez cech
    #  zgodności, która wygląda jak lustro produkcji ze spójnikiem i przyjmuje
    #  grupę przymiotnikową uzgodnioną z niczym.
    assert verdict("Pliki są nowe, duże.").status == "valid"
    assert verdict("Pliki są nowe, duży.").status == "rejected"


def test_ciąg_przydawki_zgadza_się_z_rzeczownikiem_każdym_członem():
    #  Usterka, przed którą to stoi: ogon ciągu dopisany bez cech zgodności,
    #  czyli produkcja, która wygląda jak koordynacja imienna, a wpuszcza pod
    #  jeden rzeczownik przymiotniki uzgodnione z niczym.
    assert verdict("Nowy i tani parser zapisuje ustawienia.").status == "valid"
    assert verdict("Nowy i tania parser zapisuje ustawienia.").status == "rejected"


def test_ciąg_przydawki_o_trzech_członach_wyprowadza_się_raz():
    #  Usterka, przed którą to stoi: przydawka koordynowana produkcją stojącą
    #  nad samą sobą, bez pary symboli. Zdanie wychodzi wtedy przyjęte tak samo,
    #  a czytań ma tyle, ile ten ciąg dopuszcza nawiasowań, więc widać ją po
    #  jednoznaczności, a nie po tym, czy zdanie się wyprowadza.
    found = verdict("Nowy, tani i szybki parser zapisuje ustawienia.")
    assert found.status == "valid", found.explain()


def test_ciąg_rozdzielny_stoi_za_rzeczownikiem_i_nie_stoi_przed_nim():
    #  Usterka, przed którą to stoi: ciało rozdzielne wpuszczone w oba szyki
    #  przydawki, czyli czytanie, w którym `Trzecia i czwarta` są dwiema
    #  warstwami stojącymi przed swoim rzeczownikiem, a polszczyzna go nie ma.
    #  Zdania to nie odrzuca, bo wyprowadza się ono ciągiem imiennym, więc bez
    #  cechy zatrzymującej ten szyk wychodzi ono wieloznaczne.
    assert verdict("Warstwy trzecia i czwarta pracują.").status == "valid"
    assert verdict("Trzecia i czwarta warstwy pracują.").status == "valid"


def test_ciąg_zgodny_nie_bierze_ogona_rozdzielnego():
    #  Usterka, przed którą to stoi: ogon ciągu zgodnego pytany o samą zgodność,
    #  bez cechy, czyli czytanie, w którym pierwsza przydawka orzeka o wszystkich
    #  warstwach, a dwie następne dzielą je między siebie. Zdanie zostaje przyjęte
    #  ciągiem imiennym, więc usterkę widać po jednoznaczności.
    assert verdict("Warstwy nowe i trzecia i czwarta pracują.").status == "valid"


def test_wyrażenie_przyimkowe_dochodzi_i_do_członu_ostatniego_i_do_całego_ciągu():
    #  Usterka, przed którą to stoi: pozycja nad ciągiem dopisana produkcją
    #  rekurencyjną `grupa_imienna → grupa_imienna wyrażenie_przyimkowe`,
    #  czyli bez spójnika w ciele. Zdania są dwa, bo każde pokazuje inną jej połowę.
    #  Nawias mówi, którego członu wyrażenie sięga, więc zasięgi są tu trzy i każdy
    #  da się nazwać; tamta produkcja zabiera nawias ostatniemu z nich, bo
    #  gospodarzem jest w nim cała grupa.
    found = verdict("Pliki i katalogi w tym drzewie rosną.")
    assert found.status == "ambiguous", found.explain()
    assert {reading["podmiot"] for reading in role(found)} == {
        "Pliki i katalogi",
        "Pliki i [katalogi w tym drzewie]",
        "Pliki i katalogi [w tym drzewie]",
    }
    #  Grupa bez koordynacji ma dwa czytania i tyle ma ich mieć: tamta produkcja
    #  dokłada trzecie, którego werdykt nie ma czym odróżnić od pierwszego, bo obu
    #  daje tego samego gospodarza.
    bez_ciągu = verdict("Katalogi w tym drzewie rosną.")
    assert len(bez_ciągu.readings) == 2, bez_ciągu.explain()


def test_grupa_liczebnikowa_zgadza_się_tym_czego_nie_ma_w_środku():
    #  Usterka, przed którą to stoi: liczba i rodzaj wypuszczone z liczebnika
    #  zmienną wspólną, tak jak wypuszcza je każda inna produkcja tej gramatyki.
    #  Wygląda to poprawnie i odwraca zgodność, bo `pięć` jest mnogie, a grupa,
    #  którą buduje, żąda czasownika w liczbie pojedynczej i rodzaju nijakim.
    #  Zdanie przyjęte tego nie łapie, bo cechy, której konstytuent nie niesie,
    #  unifikacja nie sprawdza, więc para zdań rozstrzyga o obu stronach naraz.
    assert verdict("Pięć kobiet przyszło.").status == "valid"
    assert verdict("Pięć kobiet przyszły.").status == "rejected"


def test_liczebnik_zgodny_zgadza_się_ze_swoim_rzeczownikiem():
    #  Ciało zgodne jest tu tym, czym przymiotnik przed rzeczownikiem, więc pilnuje
    #  go to samo, co tamtego: rodzaj złamany parą form, których polszczyzna obok
    #  siebie nie stawia.
    assert verdict("Dwie kobiety przyszły.").status == "valid"
    assert verdict("Dwa kobiety przyszły.").status == "rejected"


def test_liczebnik_rządzący_żąda_rodzaju_od_swojego_dopełniacza():
    #  Rodzaj przechodzi z liczebnika na dopełniacz, choć grupa nad nimi wychodzi
    #  nijaka, i bez tego warunku obie formy liczebnika biorą każdy rzeczownik:
    #  rodzaj męskoosobowy ma w polszczyźnie własną formę i to ona tu rozstrzyga.
    assert verdict("Pięciu mężczyzn przyszło.").status == "valid"
    assert verdict("Pięć mężczyzn przyszło.").status == "rejected"


def test_liczebnik_złożony_przyłącza_się_wedle_swojego_ostatniego_członu():
    #  Usterka, przed którą to stoi: łańcuch wypuszczający `accommodability` członu
    #  pierwszego albo zmienną wspólną wszystkim członom. Jedno i drugie wygląda
    #  poprawnie, bo `dwadzieścia` rządzi dopełniaczem, a przyłączenie rozstrzyga tu
    #  człon skrajnie prawy: `dwa` żąda mianownika mnogiego i czasownika mnogiego,
    #  `siedem` dopełniacza mnogiego i czasownika pojedynczego. Cechy, której
    #  konstytuent nie niesie, unifikacja nie sprawdza, więc każda strona żąda pary.
    #  Zdanie ostatnie stawia z przodu dwa człony naraz, bo łańcuch spłaszczony do
    #  dwóch członów przechodzi wszystkie pozostałe zdania.
    assert verdict("Dwadzieścia dwa chleby leżą.").status == "valid"
    assert verdict("Dwadzieścia dwa chleby leży.").status == "rejected"
    assert verdict("Dwadzieścia siedem chlebów leży.").status == "valid"
    assert verdict("Dwadzieścia siedem chlebów leżą.").status == "rejected"
    assert verdict("Sto dwadzieścia dwa chleby leżą.").status == "valid"


def test_łańcuch_liczebnikowy_żąda_jednego_przypadka_od_każdego_członu():
    #  Polszczyzna odmienia każdy człon, więc przypadek jest w łańcuchu zmienną
    #  wspólną. Bez niej `dwadzieścia dwóch` wyprowadza się tak samo jak
    #  `dwudziestu dwóch`, czyli mianownik miesza się z dopełniaczem.
    assert verdict("Dwadzieścia dwóch mężczyzn przyszło.").status == "rejected"


def test_pięć_nie_jest_dopełniaczem_rzeczownika_odczasownikowego():
    #  Bez tego warunku `pięć` staje głową grupy imiennej w dopełniaczu mnogim,
    #  czyli dokładnie tam, gdzie ciało rządzące żąda dopełniacza, i każda liczba
    #  zakończona na pięć wychodzi dwoma czytaniami. Drugie zdanie jest ceną, którą
    #  ten warunek płaci, i stoi tu dlatego, że płaci ją rozmyślnie.
    assert verdict("Dwadzieścia pięć chlebów leży.").status == "valid"
    assert verdict("Pięcie jest trudne.").status == "rejected"


def test_cyfra_nie_jest_liczebnikiem_bo_nie_niesie_ani_przypadka_ani_liczby():
    #  Rejestr, o który olskiemu chodzi, pisze liczebnik cyfrą, a Morfeusz daje jej
    #  tag `dig` bez ani jednej cechy, więc oba ciała biorą ją naraz i `14 dni`
    #  wychodzi dwoma wyprowadzeniami o jednym streszczeniu. Odmowa jest przez to
    #  rozstrzygnięciem, a nie przeoczeniem, i docs/subset.md trzyma jej cenę.
    werdykt = verdict("Termin wynosi 14 dni.")
    assert werdykt.status == "rejected"
    assert werdykt.nielicencjonowane == ("14",)


def test_rzeczownik_odczasownikowy_stoi_w_każdej_pozycji_rzeczownika():
    #  Usterka, którą to łapie: pozycja dopisana rzeczownikowi i nie dopisana tej
    #  głowie. Ciała wypisuje jedna pętla, więc rozejście się dwóch kompletów nie
    #  daje ani jednego zdania odrzuconego, dopóki nikt nie zapyta o pozycję
    #  osobno, a zdania niżej są tymi pytaniami: głowa sama, z przymiotnikiem, z
    #  dopełniaczem i z wyrażeniem przyimkowym po sobie.
    #
    #  Ostatnie z nich wychodzi wieloznaczne i wychodzi tak słusznie: wyrażenie
    #  przyimkowe przyłącza się i do tej głowy, i do zdania, a olski między tymi
    #  dwoma czytaniami nie wybiera. Przyłączenie do głowy jest tu tym, o co pyta
    #  ten test, i widać je po tym, że czytania są dwa, a nie jedno.
    assert verdict("Przyłączenie jest tanie.").status == "valid"
    assert verdict("Nowe przyłączenie jest tanie.").status == "valid"
    assert verdict("Przyłączenie wyrażenia jest tanie.").status == "valid"
    przyimkowe = verdict("Przyłączenie do czasownika jest tanie.")
    assert przyimkowe.status == "ambiguous", przyimkowe.explain()
    [przyłączenie] = przyimkowe.result.przyłączenia
    assert przyłączenie.gospodarze == ("Przyłączenie", "jest"), przyimkowe.explain()


def test_rzeczownik_odczasownikowy_żąda_dopełniacza_a_nie_biernika():
    #  Ta głowa jest głową grupy imiennej, a nie pozycją przy czasowniku, i tyle
    #  właśnie znaczy: dopełnienia żąda w dopełniaczu, tak jak żąda go rzeczownik
    #  z dopełniaczem pod sobą. Bez tego warunku `przyłączenie wyrażenie`
    #  wyprowadza się jako grupa, której polszczyzna nie ma.
    assert verdict("Wyznaczenie granicy jest tanie.").status == "valid"
    assert verdict("Wyznaczenie granica jest tanie.").status == "rejected"


def test_dwa_czytania_tej_samej_głowy_są_jednym_czytaniem():
    #  Na tym stoi zerowa cena tej głowy: `czytanie` jest u Morfeusza i
    #  rzeczownikiem, i formą odczasownikową `czytać`, a ciała są dwa, więc zdanie
    #  ma dwa wyprowadzenia. Kształt mają jeden, a część mowy jest z tożsamości
    #  czytania wyłączona (`Node.signature` w `olski/parse.py`), więc wpadają do
    #  jednej klasy i zdanie zostaje jednoznaczne.
    werdykt = verdict("Czytanie jest tanie.")
    assert werdykt.status == "valid", werdykt.explain()


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


@pytest.mark.parametrize(
    "zdanie",
    [
        'Przepisem "Zasad techniki prawodawczej" jest ustawa.',
        #  Cudzysłów pojedynczy Morfeusz scala ze słowem w jedną formę, więc
        #  podpowiedź pytająca o samą formę nie widzi go wcale.
        "Przepisem 'Zasad techniki prawodawczej' jest ustawa.",
    ],
)
def test_werdykt_nad_cudzysłowem_z_innego_rejestru_nazywa_parę_którą_gramatyka_bierze(zdanie):
    #  Sama nazwana forma mówi autorowi tyle, że jego cudzysłów nie przechodzi.
    werdykt = verdict(zdanie)
    assert werdykt.status == "rejected"
    assert werdykt.explain().endswith("; a cytat otwiera się znakiem „ i zamyka znakiem ”")


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Łącznik: forma `-` bez licencji zostaje po nazwie pliku i po fladze,
        #  a odróżnia je od myślnika sam odstęp, którego w formie nie ma.
        "Cena jest niska - gramatyka jest tania.",
        #  Apostrof w środku słowa: warunek pytający o samo zawieranie brał go za
        #  cytat nad kilkunastoma zdaniami prozy tego repozytorium.
        "Reguła nazywa document's own list.",
    ],
)
def test_podpowiedzi_o_cudzysłowie_nie_dostaje_znak_którym_nikt_nie_cytował(zdanie):
    assert "quotation" not in verdict(zdanie).explain()


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


def test_zdanie_względne_bierze_okolicznik_między_podmiotem_a_czasownikiem():
    #  Miejsce, które gramatyka pisana ręką miała w dwóch ciałach z trzech i w
    #  trzecim je pominęła. Usterka jest niewidoczna po werdykcie: zdanie nie
    #  zostaje odrzucone, tylko wychodzi jednym czytaniem, w którym `w tym trybie`
    #  dochodzi do `organ`, bo czytanie z przyłączeniem do `wydaje` nie ma gdzie
    #  się wyprowadzić. Powrotem tamtego stanu jest `valid` nad tym zdaniem.
    found = verdict("Ustawa, którą organ w tym trybie wydaje, jest tania.")
    assert found.status == "ambiguous", found.explain()
    [przyłączenie] = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("wydaje", "organ"), found.explain()


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


@pytest.mark.parametrize(
    ("text", "rola", "modyfikator"),
    [
        ("Począł myśleć gorączkowo.", "okolicznik_przysłówkowy", "gorączkowo"),
        ("Począł myśleć już.", "cząstka_zdania", "już"),
    ],
)
def test_okolicznik_bez_przyimka_nazywa_gospodarza_tak_jak_wyrażenie_przyimkowe(
    text, rola, modyfikator
):
    #  Gospodarz jest tu całą różnicą między dwoma czytaniami:
    #  `począł (myśleć gorączkowo)` i `(począł myśleć) gorączkowo`.
    #  Usterka, którą to łapie: rola przyłączana bez nazwy gospodarza,
    #  po której werdykt drukuje jeden wiersz dwa razy
    #  i nie mówi o zdaniu nic poza liczbą czytań.
    found = verdict(text)
    assert found.status == "ambiguous", found.explain()
    assert {reading[rola] for reading in role(found)} == {
        f"{modyfikator} → myśleć",
        f"{modyfikator} → Począł",
    }


def test_streszczenie_wiąże_okolicznik_ze_zdaniem_a_nie_z_dopełnieniem():
    #  `okoliczniki` stoją w drzewie pod `wypełnienia`, czyli tuż obok dopełnienia,
    #  więc przyłączenie wzięte z najbliższego węzła z materiałem obok
    #  nazwałoby okolicznik zdania określeniem dopełnienia —
    #  i byłoby to akurat to drugie czytanie, od którego olski to pierwsze odróżnia.
    found = verdict("Program zapisuje ustawienia w pliku w katalogu.")
    zdaniowe = [reading for reading in role(found) if reading["dopełnienie"] == "ustawienia"]
    assert {reading["wyrażenie_przyimkowe"] for reading in zdaniowe} == {
        "w pliku → zapisuje",
        "w pliku w katalogu → zapisuje",
    }


def test_streszczenie_nie_wstawia_odstępu_przed_przecinkiem():
    #  Przecinek jest segmentem jak każde inne słowo, więc sklejenie form przez sam
    #  odstęp dawało `ustawienia , dane i pliki`, czyli napis, którego w tym zdaniu
    #  nikt nie napisał. Usterka jest widoczna w każdym zdaniu z koordynacją
    #  przecinkiem i w żadnym innym.
    roles = role(verdict("Program zapisuje ustawienia, dane i pliki."))[0]
    assert roles["dopełnienie"] == "ustawienia, dane i pliki"


def test_czytanie_rozcinające_zdanie_nie_wychodzi_streszczeniem_całości():
    #  Usterka, którą to łapie: streszczenie czytające się jak streszczenie całości.
    #  Morfeusz zna `szczęśliwi` jako `szczęśliwić fin:sg:ter:imperf`, więc `i szczęśliwi`
    #  wychodzi drugim zdaniem składowym bez podmiotu. Streszczenie jedno na zdanie
    #  mówi `orzecznik: wolni, równi`, o reszcie zdania milczy i nie widać,
    #  że dwa czytania różni rozcięcie zdania na dwa, a nie żadna rola.
    found = verdict("Ludzie są wolni, równi i szczęśliwi.")
    assert found.readings == [
        ({"podmiot": "Ludzie", "orzecznik": "wolni, równi i szczęśliwi", "orzeczenie": "są"},),
        (
            {"podmiot": "Ludzie", "orzecznik": "wolni, równi", "orzeczenie": "są"},
            {"orzeczenie": "szczęśliwi"},
        ),
    ]
    #  Tę różnicę nazywa rolą samo pytanie o zdanie całe: każde zdanie składowe
    #  osobno niesie jeden orzecznik, bo stoi w jednym z tych dwóch czytań.
    assert found.result.różniące == ("orzecznik",)


def test_zdanie_współrzędne_dostaje_streszczenie_na_każde_zdanie_składowe():
    #  Zdanie jednoznaczne, więc streszczenia nie bierze się z żadnej wieloznaczności:
    #  dopełnienie jest w drugim zdaniu składowym, a podmiot i czasownik w pierwszym,
    #  i widać to po tym, w którym streszczeniu która rola stoi. Streszczenie jedno na
    #  zdanie nazywa pierwsze wystąpienie roli, więc wychodzi z niego werdykt `valid`
    #  o dopełnieniu i podmiocie z dwóch różnych zdań składowych.
    [streszczenie] = verdict("Autor działa i zapisuje ustawienia.").readings
    assert streszczenie == (
        {"podmiot": "Autor", "orzeczenie": "działa"},
        {"dopełnienie": "ustawienia", "orzeczenie": "zapisuje"},
    )


def test_okolicznik_na_czele_zdania_nie_wychodzi_drugim_zdaniem_składowym():
    #  Usterka, którą to łapie: zdanie składowe policzone dwa razy. Okolicznik
    #  zdania dokłada nad składowym drugi węzeł o tej samej etykiecie
    #  (`zdanie_składowe → wyrażenie_przyimkowe zdanie_składowe`), więc zbieranie wszystkich
    #  takich węzłów zamiast najwyższego w gałęzi widzi tu ciąg dwóch zdań
    #  i rozcina streszczenie na dwa, choć zdanie składowe jest jedno.
    [streszczenie] = verdict("Pod względem smaku chałka przewyższa zwykłą bułkę.").readings
    assert len(streszczenie) == 1, streszczenie


def test_dwa_czytania_różne_granicą_członu_nie_wychodzą_jednym_napisem():
    #  Usterka, którą to łapie: streszczenie sklejone z samych form. Dwa z tych
    #  trzech czytań mają w każdej roli te same formy i różnią się granicą członu
    #  wewnątrz dopełnienia, więc bez nawiasu dawały znak w znak ten sam wiersz,
    #  co po werdykcie czyta się jak usterka narzędzia, a nie jak dwa czytania.
    #  Ciąg wpuszcza tu `sera` dlatego, że forma jest i dopełniaczem od `ser`,
    #  i biernikiem mnogim od `serum`, a biernika żąda pozycja dopełnienia.
    found = verdict("Koszt szynki i sera przewyższa koszt chleba.")
    streszczenia = [tuple(sorted(reading.items())) for reading in role(found)]
    assert len(set(streszczenia)) == len(streszczenia), found.explain()
    assert "[Koszt szynki] i sera" in {reading["dopełnienie"] for reading in role(found)}


@pytest.mark.parametrize("symbol", ["orzeczenie", "podmiot"])
def test_każdy_szyk_zdania_przepuszcza_rodzaj_między_podmiotem_a_czasownikiem(symbol):
    #  Czas przeszły zgadza się z podmiotem w rodzaju, a teraźniejszy tej cechy nie
    #  niesie, więc szyk, który rodzaju nie przepuszcza, wygląda przy `zapisuje` na
    #  poprawny i przyjmuje `Lista stał`. Zdanie tego nie łapie, bo szyków jest
    #  kilkanaście, a zdanie sprawdza jeden. Cechy, której konstytuent nie niesie,
    #  unifikacja nie sprawdza, i to jest ta cisza, którą ten test przerywa.
    odniesienia = [
        part
        for production in GRAMMAR.productions
        for part in production.body
        if isinstance(part, Sym) and part.name == symbol
    ]
    assert odniesienia, symbol
    for part in odniesienia:
        assert "gender" in dict(part.constraints), part
    #  Rodzaj wychodzi z głowy sam, więc pyta ten test o córkę, która głową nie
    #  jest: ciało biorące rodzaj od niej wypuszcza go tylko wtedy, gdy sam to
    #  mówi. Produkcja, której o rodzaj nie pyta ani jedna córka, przepuszczać go
    #  nie ma: czas teraźniejszy tej cechy nie niesie.
    for production in GRAMMAR.productions:
        if production.head != symbol:
            continue
        if any("gender" in dict(part.constraints) for part in production.body):
            assert "gender" in dict(production.features), production


@pytest.mark.parametrize("symbol", ["zdanie", "zdanie_składowe", "grupa_orzeczenia", "orzeczenie"])
def test_każda_produkcja_od_czasownika_do_zdania_wypuszcza_tryb(symbol):
    #  Usterka, przed którą to stoi: ciało zdania dopisane bez cechy trybu.
    #  Spójnik niosący cząstkę tego trybu żąda jej od zdania pod sobą, a cechy,
    #  której konstytuent nie niesie, unifikacja nie sprawdza, więc takie ciało
    #  wpuszcza pod ten spójnik każdy tryb i wyprowadza `żeby program zapisuje
    #  ustawienia`. Pojedyncze zdanie tego nie łapie, bo ciał jest kilkadziesiąt,
    #  a jedno zdanie przechodzi przez jedno z nich.
    #
    #  Zmienna wypisana i niezwiązana milczy tak samo jak cecha pominięta, więc
    #  test pyta o jedno i o drugie: cechę w produkcji i tę samą zmienną w którejś
    #  z jej córek.
    produkcje = [production for production in GRAMMAR.productions if production.head == symbol]
    assert produkcje, symbol
    for production in produkcje:
        tryb = dict(production.features).get("tryb")
        assert tryb is not None, production
        if isinstance(tryb, Var):
            assert any(dict(part.constraints).get("tryb") == tryb for part in production.body), (
                production
            )


def test_tryb_przypuszczający_bierze_osobę_stamtąd_skąd_czas_przeszły():
    #  Usterka, którą to łapie: osoba wypisana zmienną w ciele bez aglutynanta.
    #  `praet` osoby nie niesie, więc bez wpisanej trzeciej `Ja napisałby program.`
    #  się wyprowadza, a zdanie z aglutynantem wychodzi wtedy poprawnie i tej
    #  pomyłki nie pokazuje. Dopełnienie stoi tu w bierniku rozmyślnie: pod
    #  dopełniaczem zdanie odrzuca sam przypadek i test przechodzi z usterką.
    found = verdict("Ja napisałby program.")
    assert found.status == "rejected", found.explain()


@pytest.mark.parametrize("symbol", DEKLARACJA.współrzędne)
def test_symbol_stojący_nad_sobą_ze_słowem_w_ciele_ma_w_nim_znak_koordynacji(symbol):
    #  Kryterium, na którym stoją dwie rzeczy naraz: `_koordynuje` w `olski/parse.py`
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


def _biorące(lemat):
    """Produkcje, w których ciele stoi ten znak."""
    return [
        produkcja
        for produkcja in GRAMMAR.productions
        if any(_znak(część, lemat) for część in produkcja.body)
    ]


def _znak(część, lemat):
    """Czy ta część ciała jest tym znakiem."""
    return (
        isinstance(część, Word)
        and bierze(część, "interp", lemat, frozenset({lemat}), {}, EMPTY) is not None
    )


@pytest.mark.parametrize("lemat", [";", "—", "–"])
def test_znak_rozdzielający_bierze_jedna_produkcja_więc_nie_ma_z_czym_konkurować(lemat):
    #  Na tej jedynce stoi zdanie, że średnik ani myślnik nie odbiera
    #  jednoznaczności ani jednemu zdaniu: znak wchodzący w jedno ciało albo
    #  wyprowadza zdanie tą produkcją, albo nie wyprowadza go wcale. Drugie ciało
    #  z tym znakiem czyni z tego zera liczbę do zmierzenia i ten test jest tym,
    #  co o tym powie.
    assert len(_biorące(lemat)) == 1, _biorące(lemat)


def test_ciała_dwukropka_żądają_za_nim_symboli_rozłącznych():
    #  Dwukropek stoi w kilku ciałach, więc jedynki wyżej mieć nie może, a zdanie
    #  o jednoznaczności zostaje to samo i stoi na czym innym: za dwukropkiem
    #  jedno ciało żąda zdania, drugie grupy imiennej, a trzecie ciągu pytań
    #  zależnych, i żaden z tych trzech napisów nie ma wyprowadzenia pozostałymi —
    #  grupa imienna zdaniem nie jest, a zdanie składowe nie zaczyna się ani `czy`
    #  (:data:`SPÓJNIK_NA_CZELE` tego lematu nie ma), ani zaimkiem, który pozycji
    #  rzeczownej nie dostał (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`).
    #  Usterka, którą to łapie: symbol dopisany za dwukropkiem do któregoś z tych
    #  ciał tak, że dwa biorą ten sam napis.
    za_dwukropkiem = set()
    for produkcja in _biorące(":"):
        [gdzie] = [
            numer
            for numer, część in enumerate(produkcja.body)
            if _znak(część, ":")
        ]
        za_dwukropkiem.add(produkcja.body[gdzie + 1].name)
    assert za_dwukropkiem == {"zdanie", "grupa_imienna", "ciąg_pytajny"}


@pytest.mark.parametrize(
    "zdanie",
    [
        #  `czy` podporządkowuje u olskiego pytanie o rozstrzygnięcie.
        "Czy zmiana idzie w dobrą stronę?",
        #  `to` jest zaimkiem, a Morfeusz daje mu czytanie spójnikowe.
        "To samo wejście daje tę samą odpowiedź.",
    ],
)
def test_lemat_o_własnej_pozycji_nie_staje_na_czele_zdania_spójnikiem(zdanie: str):
    #  Usterka, przed którą to stoi: czoło zdania pisane wykluczeniem zamiast listy
    #  lematów. Oba te zdania mają wtedy dwa czytania, a polszczyzna czyta je raz;
    #  docs/subset.md trzyma pomiar, przy którym lista wygrała z wykluczeniem.
    assert verdict(zdanie).status == "valid"


def test_człon_bez_czasownika_nie_wchodzi_za_spójnikiem_dokładającym_skutek():
    #  Usterka, którą to łapie: SPÓJNIK_PRZECINKOWY postawiony przed tym członem
    #  zamiast węższej listy. Obie listy niosą `a` i `czyli`, więc zdanie przyjęte
    #  nie powie, którą wzięto; rozdziela je `więc`, za którym polszczyzna samej
    #  grupy imiennej nie stawia.
    assert role(verdict("Parser jest tani, a nie Morfeusz."))
    assert not role(verdict("Parser jest tani, więc Morfeusz."))


def test_człon_bez_czasownika_przepuszcza_zdanie_nadrzędne_za_przecinkiem():
    #  Usterka, którą to łapie: ciało bez przecinka zamykającego, czyli to samo
    #  przeoczenie, które zdaniom podrzędnym naprawia `_zamykane`. Zdanie
    #  nadrzędne biegnie za tym członem i biegnie spójnikiem bez przecinka, więc
    #  bez tego ciała `i pilnuje go test` nie ma się o co zaczepić.
    zamknięty = verdict(
        "Granica pakietu jest rozstrzygnięciem, a nie przypadkiem, i pilnuje go test."
    )
    assert zamknięty.readings, zamknięty.explain()


def test_ciąg_skorelowany_bierze_liczbę_z_członu_a_nie_wartością():
    #  Usterka, którą to łapie: `number="pl"` przepisane z dwóch ciał koordynacji
    #  obok. Ciąg z przeczeniem rozdziela człony, zamiast je sumować, więc orzeka
    #  w liczbie pojedynczej, a wartość `pl` odbiera temu zdaniu każde czytanie.
    assert verdict("Ani parser, ani linter nie rośnie.").status == "valid"
    assert verdict("Ani parsery, ani lintery nie rosną.").status == "valid"
    #  Zgodność zostaje przy tym zgodnością: człon w innej liczbie niż orzeczenie
    #  czytania nie ma.
    assert verdict("Ani parser, ani linter nie rosną.").status == "rejected"


def test_ciąg_skorelowany_nie_bierze_lematu_o_własnej_pozycji():
    #  Usterka, którą to łapie: `czy` dopisane do listy skorelowanych. Lemat ten
    #  podporządkowuje pytanie o rozstrzygnięcie, więc ciąg dawałby `Pyta, czy
    #  rośnie, czy maleje.` drugie wyprowadzenie tego samego kształtu, a werdykt
    #  zostawałby ten sam: zdanie jest wieloznaczne i bez tego czytania, więc
    #  pomiar różnicowy tej ceny nie pokaże (docs/subset.md).
    assert SPÓJNIK_PYTAJNY not in SPÓJNIKI_SKORELOWANE


def test_analiza_staje_na_spójniku_przed_którym_stoi_zbędny_przecinek():
    #  Usterka, którą to łapie: `i` dopisane do listy spójników skorelowanych.
    #  Terminal ciągu wpuszcza tę formę na czoło członu, czyli wszędzie tam, gdzie
    #  człon może się zacząć, więc analiza idzie przez nią dalej, niż napis na to
    #  pozwala: przecinka przed `i` polszczyzna nie stawia (docs/subset.md).
    stanęło = verdict("Cena rośnie, i linter sprawdza tekst.")
    assert stanęło.status == "rejected", stanęło.explain()
    assert stanęło.zatrzymanie == "i", stanęło.explain()


def test_spójnik_ma_czoło_całego_zdania_a_nie_czoło_zdania_składowego():
    #  Granica biegnie między dwoma poziomami, a jedno zdanie sprawdza oba.
    #  Usterka po stronie zdania składowego: SPÓJNIK dopisany do pętli, która
    #  daje cząstce i przysłówkowi czoło składowego, albo ciało czoła postawione
    #  przy symbolu `zdanie` zamiast przy `wypowiedzenie`. `więc` stoi wtedy w dwóch pozycjach
    #  naraz — na czele drugiego składowego i w jego liście okoliczników — więc
    #  zdanie spięte przecinkiem dostaje drugie czytanie tego samego kształtu.
    spięte = verdict("Cena jest niska, więc gramatyka jest tania.")
    assert spięte.status == "valid", spięte.explain()
    #  Ten sam spójnik między dwoma zdaniami bez przecinka, czyli druga z dwóch
    #  klas, na jakie gramatyka dzieli spójnik zdaniowy.
    assert verdict("Cena jest niska i gramatyka jest tania.").status == "valid"


def test_cząstka_przecząca_nie_spina_dwóch_zdań_w_ciąg_współrzędny():
    #  Morfeusz czyta `nie` także jako spójnik, a gramatyka ma dla tej formy
    #  pozycję przy czasowniku, więc bez wykluczenia w klasie spójników bez
    #  przecinka jeden napis ma dwa wyprowadzenia, a drugie jest czytaniem,
    #  którego polszczyzna nie ma. Usterka, którą to łapie: wykluczenie zdjęte
    #  przy okazji dopisywania lematu do listy spójników przecinkowych.
    assert not role(verdict("Program zapisuje ustawienia nie linter sprawdza tekst."))
    assert verdict("Program nie zapisuje ustawień.").status == "valid"


def test_rozdzielające_a_nie_licencjonuje_formy_przyimkowej_zaimka():
    #  `a` niesie u Morfeusza czytanie przyimka, którego wyrażenie przyimkowe nie
    #  bierze, więc licencji nie udziela też forma stojąca za nim. Usterka, którą
    #  to łapie: warunek w `po_przyimku` pytający o samą część mowy, przy którym
    #  `Cena jest niska, a nie.` wychodzi członem bez czasownika, a `nie` w nim
    #  biernikiem zaimka `on`.
    assert not role(verdict("Cena jest niska, a nie."))
    #  Przyimek, który gramatyka bierze, licencjonuje dalej.
    assert role(verdict("Program zapisuje ustawienia dla niego."))


def test_cudzysłów_przepuszcza_przypadek_grupy_którą_obejmuje():
    #  Usterka, którą to łapie: przypadek wypisany wartością zamiast zmiennej.
    #  Polszczyzna odmienia to, co cudzysłów obejmuje, wedle roli grupy, więc
    #  wartość wpisana w produkcję przyjmuje jeden z tych dwóch napisów i odrzuca
    #  drugi, a oba są zdaniami tej dokumentacji.
    mianownik = verdict("Same „Zasady techniki prawodawczej” są rozporządzeniem.")
    assert mianownik.status == "valid", mianownik.explain()
    orzecznik = verdict("Ustawa jest przepisem „Zasad techniki prawodawczej”.")
    assert orzecznik.status == "valid", orzecznik.explain()


def test_przytoczenie_bierze_licencję_od_cudzysłowu_a_nie_od_pisma_napisu():
    #  Usterka, którą to łapie: warunek pytający o samą formę. Litera jest u
    #  Morfeusza skrótem — `B` pod lematem `bajt` — i skrótów ta gramatyka nie ma,
    #  więc bez cudzysłowu napisowi nie zostaje ani jedno czytanie do wzięcia.
    #
    #  `nacisnąć`, a nie `wcisnąć`: drugie ma drugą pozycję ramy, a grupa w
    #  cudzysłowie idzie przez każdy przypadek, więc para dokłada temu zdaniu
    #  czytanie z `„B”` w celowniku i pytanie o cudzysłów tonie w nim.
    #  Pytanie jest tu o odczytanie, a nie o jednoznaczność: napis nieodmienny
    #  spełnia każde żądanie przypadku, więc stoi i w dopełnieniu, i w okoliczniku
    #  narzędnikowym (WIELOZNACZNE_PRZEZ_NARZĘDNIK wyżej), a licencji udziela mu
    #  jedno i drugie tak samo.
    przytoczony = verdict("Naciśnij klawisz „B” i zapisz plik konfiguracyjny.")
    assert przytoczony.readings, przytoczony.explain()
    assert not verdict("Naciśnij klawisz B i zapisz plik konfiguracyjny.").readings


def test_przytoczeniem_jest_napis_domknięty_i_jednosłowny():
    #  Usterka, którą to łapie: warunek pytający o jeden znak z dwóch albo o
    #  cudzysłów gdziekolwiek w zdaniu, zamiast o oba sąsiedztwa napisu. Wnętrzem
    #  dłuższym niż jedno słowo jest grupa imienna albo nic.
    assert not verdict("Wciśnij klawisz „B.").readings
    assert not verdict("Znam „to nie zdanie”.").readings


def test_przytoczenie_zostawia_tytuł_jednosłowny_grupie_imiennej():
    #  Usterka, którą to łapie: GRUPA_JEDNYM_SŁOWEM opróżniona albo zawężona do
    #  samego rzeczownika. Czytanie nieodmienne spełnia każdy przypadek i niesie
    #  rodzaj nijaki, więc zamiana daje takiemu napisowi drugie czytanie w roli
    #  podmiotu, a orzecznikowi żeńskiemu odbiera zgodność.
    dopełnienie = verdict("Program zapisuje „ustawienia”.")
    assert dopełnienie.status == "valid", dopełnienie.explain()
    orzecznik = verdict("„Reguła” jest tania.")
    assert orzecznik.status == "valid", orzecznik.explain()


def test_wtrącenie_nie_oddaje_zdaniu_ról_ze_swojego_wnętrza():
    #  Wtrącenie jest rolą całym napisem, więc zejście po role zatrzymuje się na
    #  nim (`Deklaracja.podrzędne`). Bez tego wyrażenie przyimkowe z jego wnętrza
    #  wychodzi rolą przyłączaną zdania, którego ono nie określa, i werdykt mówi o
    #  zdaniu nieprawdę, zamiast odrzucić.
    werdykt = verdict("Cena jest niska (koszt w pliku).")
    assert werdykt.status == "valid", werdykt.explain()
    [(czytanie,)] = werdykt.readings
    assert czytanie[WTRĄCENIE] == "( koszt w pliku ) → jest", czytanie
    assert WYRAŻENIE_PRZYIMKOWE not in czytanie, czytanie


def test_wtrącenie_w_zdaniu_względnym_wychodzi_jednym_czytaniem():
    #  Nawias przed przecinkiem zamykającym zdanie względne ma jednego gospodarza,
    #  bo przyłączony do zdania nadrzędnego stanąłby za tym przecinkiem, czyli
    #  dałby inny napis.
    werdykt = verdict("Reguła, która rozstrzyga (niżej), jest tania.")
    assert werdykt.status == "valid", werdykt.explain()


def test_zdanie_względne_na_końcu_zdania_bierze_nawias_od_zdania_nadrzędnego():
    #  Usterka, którą to łapie: ta sama pozycja dopisana przez symetrię do ciała
    #  zdania względnego bez przecinka. Ten napis obsługuje w całości pozycja przy
    #  zdaniu składowym, więc druga dołożyłaby mu drugiego gospodarza i drugie
    #  czytanie, nie kupując ani jednego zdania.
    werdykt = verdict("Program zapisuje regułę, która rozstrzyga (niżej).")
    assert werdykt.status == "valid", werdykt.explain()


def test_zdanie_bierze_jeden_znak_rozdzielający_a_nie_ciąg_takich_znaków():
    #  Produkcja stoi na poziomie zdania, a `zdanie` żadnego z tych znaków nie ma,
    #  więc rekurencji nie ma czym zbudować i drugi znak w zdaniu odrzuca je. Jest
    #  to granica wypowiedziana, a nie przeoczona: docs/subset.md trzyma ją wśród
    #  tego, czego olski nie bierze, i ten test jest jej świadkiem.
    assert verdict("Cena jest niska; gramatyka jest bezkontekstowa.").status == "valid"
    dwa = verdict("Cena jest niska; gramatyka jest bezkontekstowa; parser jest tani.")
    assert dwa.status == "rejected", dwa.explain()


@pytest.mark.parametrize(("znak", "status"), [("—", "valid"), ("–", "valid"), ("-", "rejected")])
def test_myślnik_rozdziela_zdanie_a_łącznik_nie(znak, status):
    #  Usterka, którą to łapie: łącznik dopisany do lematów myślnika. Polszczyzna
    #  spaja nim wewnątrz wyrazu — `UTF-8` — a rozdzielanie zdania należy do pauzy
    #  i półpauzy, więc znaki są trzy i tylko dwa z nich rozdzielają
    #  (:data:`olski.subset.MYŚLNIK`).
    found = verdict(f"Cena jest niska {znak} gramatyka jest bezkontekstowa.")
    assert found.status == status, found.explain()


@pytest.mark.parametrize("lemat", sorted(SPÓJNIKI_PRZECINKOWE))
def test_dwie_klasy_spójnika_zdaniowego_nie_zachodzą_na_siebie(lemat: str):
    #  Lemat wzięty obiema pozycjami dałby polszczyźnie i `A, ale B`, i `A ale B`,
    #  a pominięty na liście nie wszedłby do żadnej z nich. Literówka wygląda
    #  dokładnie tak jak pominięcie: pozycja z przecinkiem milczy wtedy o słowie
    #  i nie widać tego po żadnym zdaniu.
    [segment] = analyse(lemat)
    czytania = [(r.tag.pos, r.lemma, segment.lematy) for r in segment.readings]
    brane = [c for c in czytania if bierze(SPÓJNIK_PRZECINKOWY, *c, {}, EMPTY) is not None]
    assert brane, (lemat, czytania)
    assert not [c for c in czytania if bierze(SPÓJNIK_BEZ_PRZECINKA, *c, {}, EMPTY) is not None]
    #  Spójnik spoza listy idzie odwrotnie, więc klasy pokrywają ją całą.
    jedno = frozenset({"i"})
    assert bierze(SPÓJNIK_BEZ_PRZECINKA, "conj", "i", jedno, {}, EMPTY) is not None
    assert bierze(SPÓJNIK_PRZECINKOWY, "conj", "i", jedno, {}, EMPTY) is None


def test_rozdzielające_a_nie_wchodzi_do_wyrażenia_przyimkowego():
    #  Usterka, którą to łapie, jest usterką werdyktu, a nie pokrycia: `a` ma w
    #  słowniku czytanie przyimkowe rządzące mianownikiem, więc bez tego warunku
    #  każde czytanie tego zdania niesie okolicznik `a linter`, którego zdanie nie
    #  ma, i przecinek przed spójnikiem nie ma czego kupić.
    found = verdict("Program zapisuje ustawienia, a linter sprawdza polszczyznę.")
    assert found.status == "valid", found.explain()
    #  Żądanie idzie do każdego streszczenia, bo zdanie ma dwa składowe,
    #  a okolicznik z tego czytania stoi w drugim z nich.
    assert all(
        "wyrażenie_przyimkowe" not in składowe
        for czytanie in found.readings
        for składowe in czytanie
    )


def test_konstytuenty_przyłączenia_są_symbolami_tej_gramatyki():
    #  Symbol przemianowany w `build` nie zgłasza się tu niczym:
    #  streszczenie nazywa wtedy całe zdanie zamiast grupy, do której przyłączenie doszło,
    #  a żaden werdykt ani żadna liczba czytań się przez to nie rusza.
    assert set(DEKLARACJA.gospodarze) <= {production.head for production in GRAMMAR.productions}


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


@pytest.mark.parametrize(
    "text",
    [
        #  Po podmiocie w szyku SVO, i po dopełnieniu w szyku OVS.
        "Program w tym trybie zapisuje ustawienia.",
        "Ustawienia w pliku zapisuje program.",
        #  Po podmiocie w szykach z czasownikiem na czele, przed orzecznikiem i za nim.
        "Trwa dochodzenie w tej sprawie.",
        "Są ludzie w tej sprawie wolni.",
        #  Po orzeczniku wysuniętym przed kopulę.
        "Wejściem w tym trybie jest zwykły tekst.",
        #  Przed dopełnieniem, wewnątrz orzeczenia.
        "Program zapisuje w pliku ustawienia.",
        #  Za bezokolicznikiem, gdzie dochodzi i do niego, i do formy osobowej.
        "Muszę jechać do domu.",
        #  Po rzeczowniku, który ma już przy sobie przymiotnik albo dopełniacz,
        #  i po imiesłowie.
        "Trwa akcja zbrojna w Strefie Gazy.",
        "Rozmieszczenie ogrodów w Polsce jest nierównomierne.",
        "Ludzie są powiązani z interesami.",
    ],
)
def test_żadna_pozycja_okolicznika_nie_daje_jednego_czytania(text):
    #  Cena decyzji z docs/subset.md o przyłączaniu wyrażeń przyimkowych, i to ta
    #  jej połowa, której nie widać po zdaniach odrzuconych. Gdy gramatyka ma
    #  regułę na jedno z dwóch przyłączeń, zdanie wychodzi jednoznaczne i olski
    #  wybiera po cichu to, czego wybierać nie miał. Każde zdanie tutaj stoi na
    #  innej pozycji okolicznika i żadne nie ma wychodzić jednym czytaniem.
    assert verdict(text).status == "ambiguous", verdict(text).explain()


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
    #  `admissible` nie sięga, bo tamten warunek pyta o czytanie rzeczownikowe;
    #  todo/ trzyma ruch i pomiar, którego on żąda.
    assert {drugie["wyrażenie_przyimkowe"] for _pierwsze, drugie in found.readings} == {
        "wobec innych → postępować",
        "wobec innych w duchu → postępować",
        "wobec innych w duchu braterstwa → postępować",
        "w duchu braterstwa → postępować",
        "w duchu braterstwa → innych",
    }


def test_rama_kopuli_zdejmuje_dopełnienie_którego_nikt_w_tym_zdaniu_nie_ma():
    #  wolny czyta się jako przymiotnik i jako rzeczownik, a być dopełnienia w
    #  bierniku nie bierze, więc czytania z dopełnieniem nie ma żaden czytelnik
    #  tego zdania. Zabiera je rama kopuli i to jest to, co walencja kupuje.
    #  Zostają dwa czytania i każde stoi na innej dziurze: na rzeczownikowym
    #  czytaniu przymiotnika `wolny`, i na tym, że Morfeusz daje formie `On`
    #  czytanie przymiotnikowe obok zaimkowego, więc staje ona tam, gdzie stoi
    #  orzecznik wysunięty. Wykluczenie słownikowe po żadne z dwóch nie sięga,
    #  bo pyta o czytanie nieodmienne, a te dwa odmieniają się jak każde inne.
    found = verdict("On jest wolny.")
    assert found.status == "ambiguous"
    assert role(found) == [
        {"podmiot": "On", "orzecznik": "wolny", "orzeczenie": "jest"},
        {"podmiot": "wolny", "orzecznik": "On", "orzeczenie": "jest"},
    ]


def test_orzecznik_w_narzędniku_bierze_tylko_kopula():
    #  Ta sama luka, z której da się wyjąć jeden slot i nie więcej. Bez
    #  ograniczenia narzędnik okolicznikowy czyta się jako orzecznik pod każdym
    #  czasownikiem, co docs/corpus.md liczyło jako niezgodność z bankiem drzew:
    #  handel wychodził wtedy orzekany o paszportach, a nie kwitnący w nich.
    #  Odkąd narzędnik ma pozycję okolicznika, zdanie to nie pada, tylko czyta się
    #  tak, jak czyta je czytelnik, i to jest sprawdzian ostrzejszy niż odrzucenie:
    #  gdyby luka się otworzyła, `paszportami` wróciłoby do orzecznika.
    handel = verdict("Kwitnie handel paszportami.")
    assert role(handel) == [
        {
            "podmiot": "handel",
            "orzeczenie": "Kwitnie",
            "okolicznik_narzędnikowy": "paszportami → Kwitnie",
        }
    ], handel.explain()
    assert verdict("Jan jest nauczycielem.").status == "valid"


def test_kopula_nie_stoi_tam_gdzie_okolicznik_narzędnikowy_a_stoi_przy_innym():
    """Zawężenie, którym kopula płaci za okolicznik narzędnikowy, wraz z jego granicą.

    Obie połowy tego testu są pomyłkami, które ta pozycja wpędza po kolei.
    Bez zawężenia `narzędziem` wychodzi raz orzecznikiem, a raz okolicznikiem
    przy czasowniku, który nic nie bierze, więc każde zdanie orzekające
    narzędnikiem traci jednoznaczność.
    Zawężenie postawione na całej liście okoliczników zamiast na narzędniku w niej
    zabiera z kolei czytanie zdaniu, w którym przy kopuli stoi sam przysłówek.
    """
    orzecznik = verdict("Parser jest narzędziem.")
    assert role(orzecznik) == [
        {"podmiot": "Parser", "orzecznik": "narzędziem", "orzeczenie": "jest"}
    ], orzecznik.explain()
    przysłówek = verdict("Cena jest gdzie indziej.")
    assert przysłówek.status == "valid", przysłówek.explain()


@pytest.mark.parametrize(
    ("text", "status"),
    [
        ("Program pozwala zapisać ustawienia.", "valid"),
        ("Program pozwala zostać ustawienia.", "rejected"),
    ],
)
def test_rama_dochodzi_do_bezokolicznika_tak_samo_jak_do_formy_osobowej(text, status):
    #  Bezokolicznik bierze dopełnienia z tego samego leksykonu, co forma osobowa,
    #  i widać to dopiero na parze zdań: samo przyjęcie pierwszego przechodziłoby
    #  też gramatyce, która bezokolicznikowi ramy nie stawia wcale.
    assert verdict(text).status == status


def test_rama_bezokolicznika_rozdziela_orzecznik_od_okolicznika_narzędnikowego():
    #  Para narzędnikowa tego samego pytania. Statusem jej nie widać, odkąd
    #  narzędnik ma pozycję okolicznika przy każdym czasowniku: oba zdania mają
    #  odczytanie, a różni je rola, którą narzędnik w nich zajmuje. `zostać` jest
    #  kopulą i bierze go orzecznikiem, `zapisać` nie jest i zostawia mu samą
    #  pozycję okolicznika (docs/warstwa-leksykalna.md#walencja-jest-leksykonem-o-ramie-domyślnej).
    kopula = verdict("Program pozwala zostać nauczycielem.")
    assert any("orzecznik" in czytanie for czytanie in role(kopula)), kopula.explain()
    zwykły = verdict("Program pozwala zapisać nauczycielem.")
    assert not any("orzecznik" in czytanie for czytanie in role(zwykły)), zwykły.explain()


@pytest.mark.parametrize(
    ("text", "status"),
    [
        ("Werdykt służy czytelnikowi.", "valid"),
        ("Parser wyprowadza czytelnikowi.", "rejected"),
        ("Wpis żąda dowodu.", "valid"),
        ("Sonda mierzy dowodu.", "rejected"),
    ],
)
def test_dopełnienia_poza_biernikiem_wpuszcza_leksykon_a_nie_przypadek(text, status):
    #  Pary, na których widać, że pozycję wpuszcza wpis, a nie sam przypadek grupy:
    #  `służyć` i `żądać` mają ją w Walentym, `wyprowadzać` i `mierzyć` nie mają.
    #  Gramatyka biorąca każdy celownik i każdy dopełniacz przechodzi zdanie
    #  pierwsze i trzecie tak samo, a różni się dopiero na drugim i czwartym.
    assert verdict(text).status == status


def test_dopełniacz_z_leksykonu_i_dopełniacz_negacji_dają_jedno_odczytanie():
    #  Czasownik, który dopełniacz bierze ramą, bierze go pod przeczeniem także w
    #  miejscu biernika, więc jeden napis wyprowadza się dwa razy. Odczytanie jest
    #  jedno, bo kształt obu wyprowadzeń jest ten sam, i tego nie widać po
    #  werdykcie żadnego innego zdania: para produkcji jest tu jedyna.
    assert verdict("Wpis nie żąda dowodu.").result.ile == 1


def test_druga_pozycja_ramy_wchodzi_zdaniem_leksykonu_a_nie_sumą_dwóch_pozycji():
    #  Usterka, którą to łapie: para złożona z dwóch zdań leksykonu policzonych
    #  osobno. `pomagać` celownik bierze, a pary z biernikiem nie ma w żadnym
    #  schemacie, więc zdanie drugie odróżnia jedno zdanie leksykonu od drugiego;
    #  bez niego odrzucenie czytałoby się jak brak celownika w ramie.
    assert verdict("Parser pokazuje autorowi oba czytania.").status == "valid"
    assert verdict("Reguła pomaga autorowi.").status == "valid"
    assert not verdict("Reguła pomaga autorowi oba czytania.").readings


def test_druga_pozycja_ramy_stoi_w_obu_szykach_i_nie_stoi_dwa_razy():
    #  Usterka, którą to łapie: wypełnienie pary wzięte zmienną ramy zamiast
    #  wartością. Zmienna przecina się z tą samą ramą co celownik, więc wpuszcza
    #  drugi celownik w miejsce biernika.
    assert verdict("Parser pokazuje oba czytania autorowi.").status == "valid"
    assert not verdict("Parser pokazuje autorowi autorowi.").readings


def test_druga_pozycja_ramy_stoi_obok_każdego_wypełnienia_a_nie_samego_biernika():
    #  Zdanie podrzędne i bezokolicznik zajmują pozycję ramy tak samo jak
    #  dopełnienie, więc celownik staje obok każdego z nich.
    #
    #  `usiąść`, a nie `zejść`: drugie ma u Morfeusza czytanie rzeczownikowe w
    #  dopełniaczu mnogim, więc `córce zejść` wychodzi jedną grupą imienną i to
    #  zdanie wyprowadzało się także bez tej pozycji.
    assert verdict("Parser mówi autorowi, że zdanie czyta się dwojako.").readings
    assert verdict("Krawiec kazał córce usiąść.").status == "valid"


def test_wolny_celownik_pada_obok_dopełnienia_a_nie_na_leksykonie():
    #  Celownik posiadacza dochodzi do orzeczenia dowolnego czasownika, więc
    #  pierwsze zdanie jest polszczyzną, a olski go nie ma. Wpis w leksykonie tego
    #  nie zmieni, bo dopełnienie stoi tu obok dopełnienia, i to jest ta granica,
    #  którą para zdań z tej sekcji łatwo czyta się na opak: leksykon rozstrzyga o
    #  pozycji ramy, a nie o tym, czy przy czasowniku wolno postawić celownik.
    assert verdict("Kompilator wyprowadza psa agentowi.").status == "rejected"
    assert verdict("Kompilator wyprowadza psa.").status == "valid"


def test_pozycje_okolicznika_w_orzeczeniu_nie_zachodzą_na_siebie():
    #  Cztery ciała `wypełnienia` stawiają okolicznik przed dopełnieniem i za nim,
    #  a `okoliczniki` nawraca samo na siebie, więc dwie pozycje łatwo tu wypisać tak,
    #  żeby jedno zdanie wychodziło dwoma kształtami drzewa. Nie widać tego po
    #  werdykcie, bo zdanie jest wieloznaczne w jedną i w drugą stronę, i nie widać
    #  po rolach, bo obie pary przyłączeń zostają te same; widać po liczbie czytań.
    #  Werdykt nazywa tu jedno przyłączenie z dwóch, i to jest ta ostrość, którą
    #  las kupuje: `w pliku` dochodzi do zdania w obu czytaniach.
    found = verdict("Autor zapisuje w pliku w katalogu.")
    assert found.explain() == '2 odczytania; „w katalogu” → „zapisuje”, „pliku”'


def test_forma_poprzyimkowa_nie_stoi_okolicznikiem_bez_przyimka_przed_sobą():
    #  `adjp` jest u Morfeusza formą, która poza przyimkiem nie stoi, i cała ta
    #  pozycja jest ciałem o dwóch córkach właśnie dlatego. Usterka, którą to
    #  łapie: `adjp` dopisane do części mowy terminala okolicznika zamiast do
    #  osobnego ciała — wtedy każde zdanie z taką formą samą dostaje czytanie,
    #  którego polszczyzna nie ma, a werdykt drugiego zdania mówi `valid`.
    assert verdict("Reguła działa po polsku.").status == "valid"
    assert verdict("Reguła działa polsku.").status == "rejected"


@pytest.mark.parametrize("leksykon", [WALENCJA, WALENCJA_ZWROTNA])
def test_klasy_walencyjne_nie_zachodzą_na_siebie(leksykon):
    #  Lemat wzięty dwiema klasami jest dwoma czytaniami tego samego kształtu, a
    #  te dwa zwijają się w jedno, bo czytanie liczy kształt: werdykt tego nie
    #  pokaże i żaden inny test tu nie sięga. Zachodzą klasy łatwo, bo Walenty
    #  mówi o kopuli to samo, co o każdym innym lemacie leksykonu, więc wpis
    #  ręczny musi swoje lematy leksykonowi zabrać, a nie stanąć obok nich.
    lematy = [lemat for klasa in leksykon.values() for lemat in klasa]
    assert len(lematy) == len(set(lematy))


def test_żadna_forma_nie_wpada_w_dwie_klasy_walencyjne_naraz():
    #  Test wyżej pilnuje rozłączności po lematach, a rama jest własnością formy,
    #  więc forma o lematach w dwóch klasach niesie dwie ramy i wychodzi dwoma
    #  wyprowadzeniami jednego kształtu, których liczba czytań nie rozdziela.
    #  Klasa domyślna pyta o całą formę i pary z nią już nie ma, więc zostaje para
    #  dwóch klas twierdzących: kopuła obok klasy wąskiej. Formy idą z syntetyzatora,
    #  bo pytanie jest o słownik, a nie o to, co któryś rejestr napisał.
    wąskie = WALENCJA[RAMA_BEZ_BIERNIKA]
    zderzenia = [
        (forma, sorted(segment.lematy & wąskie))
        for lemat in KOPULA
        for forma, *_ in generuj(lemat)
        for segment in analyse(forma)
        if segment.lematy & KOPULA and segment.lematy & wąskie
    ]
    assert not zderzenia, zderzenia


def test_forma_o_dwóch_lematach_nie_omija_zawężenia_leksykonem():
    #  Zawężenie postawione lematowi omija forma, której słownik daje lemat jeszcze
    #  inny: `zapisuje` jest i od `zapisywać`, i od `zapisować`, a tego drugiego
    #  leksykon nie wymienia, więc czytanie stąd brało ramę domyślną z biernikiem,
    #  którego `zapisywać się` nie bierze. Drugie zdanie jest w parze dlatego, że
    #  czasownik bez cząstki biernik bierze i zawężenie nie ma się na niego rozlać.
    assert verdict("Program zapisuje się ustawienia.").status == "rejected"
    assert verdict("Program zapisuje ustawienia.").status == "valid"


def test_wykluczenie_leksykalne_mówi_o_czytaniu_a_nie_o_formie():
    #  Warunki ujemne są dwa i różni je zasięg, a nad Składnicą nie różni ich ani
    #  jedno zdanie (docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem), więc
    #  jeden podstawiony za drugi nie wywraca ani suity, ani przebiegu nad korpusem.
    #  Pilnuje ich zatem to jedno miejsce. `nie` jest u Morfeusza cząstką `nie`
    #  i formą `on`: wykluczenie o czytaniu zostawia to drugie czytanie, a o formie
    #  zabiera oba, czyli zabiera czytanie, o którym nic nie mówi.
    [segment] = analyse("nie")
    zaimek = next(reading for reading in segment.readings if reading.lemma == "on")
    pytanie = (zaimek.tag.pos, zaimek.lemma, segment.lematy, zaimek.tag.cechy, EMPTY)
    o_czytaniu = word(zaimek.tag.pos, bez_lematu="nie")
    o_formie = word(zaimek.tag.pos, bez_lematu_formy="nie")
    assert bierze(o_czytaniu, *pytanie) is not None
    assert bierze(o_formie, *pytanie) is None


def test_cząstka_się_pyta_leksykonu_o_inny_czasownik_niż_forma_bez_niej():
    #  Otwierać bierze dopełnienie w bierniku, a otwierać się go nie bierze, i
    #  Morfeusz daje obu formom ten sam lemat. Leksykon trzymany pod samym lematem
    #  dałby więc jednemu z tych dwóch zdań ramę drugiego, a widać to dopiero na
    #  parze: jedno przechodzi w każdą stronę, a drugie nie.
    otwarcie = verdict("Otwierają się drzwi.")
    assert role(otwarcie) == [{"podmiot": "drzwi", "orzeczenie": "Otwierają się"}]
    assert verdict("Otwierają drzwi.").status == "ambiguous"


def test_cząstka_zwrotna_przed_formą_pyta_o_ten_sam_leksykon_zwrotny():
    #  Pozycja przednia jest tą samą pozycją tego samego czasownika, więc ramę ma
    #  brać z leksykonu zwrotnego tak samo jak tylna. Ciało napisane z ramą
    #  niezwrotną przechodziłoby zdanie drugie, bo otwierać się biernika nie
    #  bierze, a otwierać go bierze.
    assert role(verdict("Drzwi się otwierają.")) == [
        {"podmiot": "Drzwi", "orzeczenie": "się otwierają"}
    ]
    assert verdict("Drzwi się otwierają okno.").status == "rejected"


def test_cząstka_zwrotna_poprzedza_przeczenie_swojej_formy():
    #  Polszczyzna stawia w pozycji przedniej cząstkę przed przeczeniem, a nie
    #  między nim i formą, i te dwa napisy różni sama ta kolejność.
    assert verdict("Rachunek się nie zwraca.").status == "valid"
    assert verdict("Rachunek nie się zwraca.").status == "rejected"


def test_kopula_nie_bierze_cząstki_zwrotnej_w_żadnej_z_dwóch_pozycji():
    #  Klasa domyślna leksykonu zwrotnego wpuszcza cząstkę do każdego lematu, którego
    #  ten leksykon nie wymienia, a kopula jest wśród nich, więc bez odmowy `być się`
    #  wychodzi czasownikiem w obu pozycjach cząstki i w czasie przyszłym.
    #  Czasownik, przy którym cząstka stoi naprawdę, odmowa zostawia.
    assert verdict("Cena się jest niska.").status == "rejected"
    assert verdict("Cena jest się niska.").status == "rejected"
    assert verdict("Cena się będzie niska.").status == "rejected"
    assert verdict("Rachunek się zwraca.").status == "valid"


def test_cząstka_zwrotna_opiera_się_o_słowo_a_nie_o_znak():
    #  Pozycja przednia sięga początku zdania i miejsca tuż za znakiem, a takich
    #  napisów polszczyzna nie ma. Warunek zdejmuje tam cząstce odczytanie
    #  (po_słowie), więc werdykt nazywa formę bez licencji, a nie strukturę,
    #  której zdaniu brakuje. Spójnik słowem jest i licencji udziela, więc para
    #  ostatnia różni się samym nim.
    assert verdict("Się myli.").status == "rejected"
    assert bez_licencji(morphology("Się myli."), GRAMMAR) == ("Się",)
    assert bez_licencji(morphology("Nic się nie zmienia."), GRAMMAR) == ()
    assert verdict("Cena rośnie, się nie liczy.").status == "rejected"
    assert verdict("Cena rośnie, a się nie liczy.").status == "valid"


@pytest.mark.parametrize(
    ("text", "role_zdania"),
    [
        #  Cząstka stoi między dwoma czasownikami i należy do drugiego: mieć się
        #  jest polszczyzną (ma się dobrze), a bezokolicznika nie bierze.
        ("Zebranie ma się odbyć.", {"podmiot": "Zebranie", "orzeczenie": "ma"}),
        #  Bezokolicznik ma obie pozycje, tak samo jak forma osobowa, więc oba
        #  szyki wychodzą tym samym odczytaniem.
        ("Cena zaczyna otwierać się.", {"podmiot": "Cena", "orzeczenie": "zaczyna"}),
        ("Cena zaczyna się otwierać.", {"podmiot": "Cena", "orzeczenie": "zaczyna"}),
    ],
)
def test_cząstka_należy_do_bezokolicznika_a_nie_do_formy_osobowej_przy_nim(text, role_zdania):
    #  Bez pozycji przy bezokoliczniku cząstkę bierze forma osobowa obok i każde
    #  z tych zdań wychodzi jednym odczytaniem z czasownikiem, którego polszczyzna
    #  nie ma; werdykt ręczy wtedy za czytanie nieprawdziwe.
    assert role(verdict(text)) == [role_zdania]


def test_leksykon_zostawia_bezokolicznik_czasownikowi_zwrotnemu_który_go_bierze():
    #  Odjęcie bezokolicznika ramie zwrotnej daje zdaniu wyżej jedno odczytanie
    #  zamiast dwóch, a bierze je z leksykonu, a nie z całej klasy: bez tego wpisu
    #  odjęcie sięga też czasowników, przy których bezokolicznik naprawdę stoi.
    assert role(verdict("Stara się ustalić granicę.")) == [
        {"dopełnienie": "granicę", "orzeczenie": "Stara się"}
    ]


def test_zdanie_leksykonu_o_bezokoliczniku_nie_żąda_kontroli_podmiotu():
    #  Zdanie węższe, o bezokoliczniku pod kontrolą podmiotu, czyta sam skład.
    #  Parser czytający je zamiast szerszego odbiera bezokolicznik czasownikom
    #  bezosobowym — udać się i dać się kontrolowane są z celownika — i tych zdań
    #  Składnicy nie wyprowadza, choć polszczyzną są.
    assert verdict("Nie udało się ustalić rasy.").status == "valid"
    assert verdict("W teatrze nie da się oszukać widza.").status == "valid"


def test_imiesłów_czynny_bierze_cząstkę_zwrotną_stojącą_za_nim():
    #  Polszczyzna ma tu dwa odczytania, bo cząstka należy albo do imiesłowu, albo
    #  do czasownika, a wybiera między nimi znaczenie. Bez tej pozycji cząstkę
    #  bierze forma osobowa za przydawką i zostaje samo drugie.
    czytania = role(verdict("Program otwierający się psuje."))
    assert {"podmiot": "Program otwierający", "orzeczenie": "się psuje"} in czytania
    assert {"podmiot": "Program otwierający się", "orzeczenie": "psuje"} in czytania


def test_leksykon_odrzuca_zdanie_czytane_dotąd_z_dopełnieniem_którego_tam_nie_ma():
    #  Cena leksykonu, wypisana zdaniem ze Składnicy. Pracować dopełnienia w
    #  bierniku nie bierze, więc dzień i noc nie jest tu dopełnieniem, tylko
    #  okolicznikiem w bierniku, a okolicznika w bierniku olski nie ma. Zdanie
    #  przechodziło, dopóki stało na czytaniu, którego nie ma żaden czytelnik.
    assert verdict("Pracujemy nad tą grupą dzień i noc.").status == "rejected"


def test_pozycja_orzecznika_żąda_ramy_sama_zamiast_dzielić_z_nią_zmienną():
    #  Trzy pozycje orzecznika wyglądają na jedną, w której orzecznik i czasownik
    #  dzielą zmienną walencyjną, a to zdanie ze Składnicy jest ceną takiego
    #  zlania: wychodzi z niego przyjęte i przeczytane na opak, z podmiotem
    #  ustalenia. docs/subset.md trzyma pomiar.
    #
    #  Drugim takim zdaniem było `Na to jest zbyt wielkim tchórzem.`, gdzie
    #  podmiotem wychodziło `zbyt`, i zeszło ono stąd razem z przysłówkiem:
    #  `zbyt` ma teraz pozycję okolicznika, więc olski przyjmuje to zdanie
    #  z czytaniem, które mówi o nim prawdę, i świadkiem tamtej ceny ono nie jest.
    assert verdict("Inne wymagają ustalenia.").status == "rejected"


def test_dwóch_gospodarzy_przysłówka_rozdziela_w_streszczeniu_rola():
    """Para gospodarzy jest tym, czym przysłówek atakuje jednoznaczność.

    Zdanie z przysłówkiem stopniowanym przed przymiotnikiem ma dwa czytania i oba
    są polszczyzną w tym sensie, w jakim liczy je ta gramatyka: raz przysłówek
    określa przymiotnik, a raz całe zdanie. Streszczenie ma je rozdzielać, i
    rozdziela je rolą, bo określenie przymiotnika stoi wewnątrz orzecznika, a
    okolicznik zdania niesie własną rolę; docs/subset.md wycenia tę parę.
    """
    found = verdict("Plik jest bardzo duży.")
    assert found.status == "ambiguous", found.explain()
    assert {czytanie.get("orzecznik") for czytanie in role(found)} == {
        "bardzo duży",
        "duży",
    }
    assert {czytanie.get("okolicznik_przysłówkowy") for czytanie in role(found)} == {
        None,
        "bardzo → jest",
    }


def test_okolicznik_staje_po_czasowniku_i_daje_zdaniu_czytanie_z_podmiotem():
    """Pozycja okolicznika po córce czasownikowej, wzięta z obu stron naraz.

    Zdania są dwa, bo brak tej pozycji płacił w dwóch walutach: pierwsze było
    odrzucone, a drugie wychodziło jednym czytaniem, w którym `program
    ustawienia` jest dopełnieniem, czyli werdyktem `valid` mówiącym o zdaniu
    nieprawdę.
    """
    trwa = verdict("Trwa w tej sprawie dochodzenie.")
    assert trwa.status == "valid", trwa.explain()
    assert role(trwa)[0]["podmiot"] == "dochodzenie"
    zapisuje = verdict("Zapisuje w pliku program ustawienia.")
    assert ("program", "ustawienia") in {
        (czytanie.get("podmiot"), czytanie.get("dopełnienie")) for czytanie in role(zapisuje)
    }, zapisuje.explain()


def test_przysłówek_przed_przysłówkiem_dochodzi_do_niego_a_nie_do_zdania():
    """Gospodarz trzeci, czyli ten, który zdejmuje ostatnią klasę płaskich czytań.

    Bez niego zdanie wychodziło jednym czytaniem, w którym `bardzo` jest
    okolicznikiem zdania na równi z `szybko`, czyli werdyktem `valid` mówiącym o
    zdaniu nieprawdę; kurs, po którym ta pozycja weszła, trzyma docs/subset.md.
    Czytania są odtąd dwa i rozdziela je rola, tak samo jak przy przymiotniku:
    pod trzecim gospodarzem cały `bardzo szybko` jest jednym okolicznikiem.
    """
    found = verdict("Program zapisuje ustawienia bardzo szybko.")
    assert found.status == "ambiguous", found.explain()
    assert {czytanie.get("okolicznik_przysłówkowy") for czytanie in role(found)} == {
        "bardzo szybko → zapisuje",
        "bardzo → zapisuje",
    }


def test_przysłówek_okolicznikowy_dostaje_rolę_a_nie_samo_wyprowadzenie():
    #  Pozycja dopisana bez roli daje `valid` bez słowa o tym, co olski w zdaniu
    #  przyjął, a rola jest tym, po co werdykt stoi (docs/roadmap.md).
    found = verdict("Program zapisuje ustawienia szybko.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["okolicznik_przysłówkowy"] == "szybko → zapisuje"


def test_cząstka_dostaje_rolę_osobną_od_przysłówka_w_obu_pozycjach():
    #  Rola jest osobna, bo cząstka przysłówkiem nie jest: `okolicznik_przysłówkowy: już` mówiłoby o
    #  zdaniu, że ma okolicznik przysłówkowy, którego ono nie ma. Pozycje przy zdaniu
    #  są dwie i pisze je jedna pętla razem z przysłówkiem, więc zdania są dwa:
    #  rozejście się tych dwóch kompletów widać dopiero na tym, którego jedna z nich
    #  nie bierze. Zdanie drugie cząstkę wpuszcza także do podmiotu, więc pytamy o
    #  rolę wśród czytań, a nie o pierwsze z nich.
    okolicznik = verdict("Program już zapisuje ustawienia.")
    assert role(okolicznik)[0][CZĄSTKA_ZDANIA] == "już → zapisuje", okolicznik.explain()
    assert OKOLICZNIK_PRZYSŁÓWKOWY not in role(okolicznik)[0], okolicznik.explain()
    czoło = verdict("Już program zapisuje ustawienia.")
    assert "Już → zapisuje" in {
        czytanie.get(CZĄSTKA_ZDANIA) for czytanie in role(czoło)
    }, czoło.explain()


def test_cząstka_w_grupie_imiennej_wchodzi_w_zasięg_roli_a_nie_obok_niej():
    """Gospodarz drugi, czyli ten, po którym podmiotem jest cała `Nawet ptaki`.

    Bez niego zdanie wychodziło jednym czytaniem, w którym podmiotem jest samo
    `ptaki`, choć bank drzew czyta tam grupę razem z cząstką; cenę tej pozycji
    trzyma docs/subset.md. Czytania są dwa, bo o gospodarzu nie rozstrzyga ani
    cecha, ani lemat, a rozdziela je zasięg podmiotu wraz z listą ról: cząstka
    obejmująca grupę etykiety nie nosi.
    """
    found = verdict("Nawet ptaki przestały śpiewać.")
    assert found.status == "ambiguous", found.explain()
    assert {
        (czytanie.get("podmiot"), czytanie.get(CZĄSTKA_ZDANIA)) for czytanie in role(found)
    } == {("Nawet ptaki", None), ("ptaki", "Nawet → przestały")}, found.explain()


def test_cząstka_w_grupie_imiennej_przepuszcza_osobę_zaimka():
    #  Przymiotnik i zaimek dzierżawczy ogłaszają trzecią osobę, a cząstka ją
    #  przepuszcza, bo staje i przed zaimkiem. Z `ter` w tym ciele grupa nie zgodziłaby
    #  się z czasownikiem osobą i to czytanie by nie wyszło.
    found = verdict("Nawet ja zapisuję ustawienia.")
    assert "Nawet ja" in {czytanie.get("podmiot") for czytanie in role(found)}, found.explain()


@pytest.mark.parametrize("lemat", sorted(CZĄSTKI))
def test_cząstka_z_listy_nie_ma_czytania_branego_gdzie_indziej(lemat):
    #  Kryterium na wejście do tej listy, postawione lemat po lemacie: cząstka,
    #  której inne czytanie gramatyka bierze, daje jednemu napisowi dwa
    #  wyprowadzenia. `tylko` jest u Morfeusza także spójnikiem, więc dopisane tu
    #  kosztowałoby czytanie każdego zdania, w którym stoi, i tego ten test pilnuje
    #  po stronie listy, a nie po stronie zdania.
    [segment] = analyse(lemat)
    czytania = [(r.tag.pos, r.lemma, segment.lematy, r.tag.cechy) for r in segment.readings]
    brane = [c for c in czytania if GRAMMAR.licencjonuje(*c)]
    assert brane, (lemat, czytania)
    assert {pos for pos, *_ in brane} == {"part"}, (lemat, brane)


@pytest.mark.parametrize(
    ("zdanie", "status"),
    [
        ("Koszt bardzo dużego pliku jest niski.", "valid"),
        ("Koszt tu dużego pliku jest niski.", "rejected"),
    ],
)
def test_do_przymiotnika_dochodzi_przysłówek_stopniowany_a_do_zdania_każdy(zdanie, status):
    """Terminale są dwa, bo warunek należy do jednego gospodarza, a nie do obu.

    Bez tego podziału pozycja przy przymiotniku bierze `tu` tak samo jak `bardzo`,
    a przysłówek bez stopnia stoi wtedy w dwóch trzecich zdań, które ta pozycja
    czyta wbrew drzewu wzorcowemu (docs/subset.md). Zdania są dwa i różni je sam
    przysłówek, bo o różnicę między dwiema jego klasami tu chodzi: pozycji w
    grupie imiennej `tu` nie ma, a okolicznik zdania w tym miejscu nie stoi.
    """
    assert verdict(zdanie).status == status


def test_gospodarzem_przyłączenia_zostaje_przymiotnik_a_nie_przysłówek_przed_nim():
    """Głowa jest numerem pozycji w ciele, więc stoi na przymiotniku, a nie przed nim.

    Bez tego werdykt nazywa gospodarzem przyłączenia przysłówek —
    `z interesami → bardzo` — czyli mówi o zdaniu coś, czego polszczyzna nie ma,
    a liczba czytań zostaje przy tym ta sama, więc żadna tabela tego nie pokaże.

    Gospodarze wchodzą tu zbiorem, bo żądanie jest o to, którzy nimi są, a nie o
    kolejność, w jakiej las wydaje czytania.
    """
    found = verdict("Program jest bardzo powiązany z interesami.")
    assert {czytanie.get("wyrażenie_przyimkowe") for czytanie in role(found)} == {
        "z interesami → powiązany",
        "z interesami → jest",
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


def test_zaimek_rzeczowny_nie_bierze_dopełniacza():
    #  tego jest dopełniaczem ten przy podzbioru i dopełniaczem to obok niego,
    #  czyli raz przymiotnikiem przy rzeczowniku, a raz zaimkiem rządzącym
    #  rzeczownikiem, więc bez warunku ujemnego zdanie wychodzi dwoma drzewami o
    #  różnym kształcie i o identycznym streszczeniu ról.
    found = verdict("Celem jest parser tego podzbioru.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["podmiot"] == "parser tego podzbioru"


def test_zaimek_bez_czytania_przymiotnikowego_też_nie_bierze_dopełniacza():
    #  Lista zawężona do paradygmatu ten zostawia to zdanie wieloznacznym: nikt ma
    #  u Morfeusza czytanie jedno i rzeczownikowe, więc czytania, w którym nikt nas
    #  jest grupą imienną, nie zdejmuje ani anotator, ani wykluczenie ze słownika.
    found = verdict("Wtedy nikt nas nie zauważy.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["podmiot"] == "nikt"


def test_zaimek_rzeczowny_nie_unosi_wysuniętego_zaimka_względnego():
    #  Drugie miejsce, w którym przydawką dopełniaczową jest zaimek: grupa
    #  wysuwana przed zdanie względne. Warunek postawiony w samej grupie imiennej
    #  zostawia to zdanie wieloznacznym, bo której nikt wychodzi taką grupą.
    found = verdict("Polszczyzna, której nikt nie napisał, jest podzbiorem.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["podmiot"] == "Polszczyzna, której nikt nie napisał,"


def test_rzeczownik_dalej_bierze_dopełniacz_po_sobie():
    #  Druga połowa warunku: wyłączona jest lista lematów, a nie produkcja, więc
    #  grupa imienna z dopełniaczem po głowie stoi tam, gdzie stała.
    found = verdict("Wejściem jest opis podzbioru.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["podmiot"] == "opis podzbioru"


def test_zaimek_rzeczowny_zostaje_wszędzie_indziej():
    #  Warunek stoi na jednej pozycji jednej produkcji, więc zaimek rzeczowny
    #  dalej jest tym, czym w polszczyźnie jest.
    assert verdict("To ma pomagać pisać dobrą polszczyznę.").status == "valid"


def test_zaimek_dzierżawczy_nie_zgadza_się_z_rzeczownikiem_przy_którym_stoi():
    #  Usterka, przed którą to stoi: zgodność wypuszczona zmienną wspólną, tak jak
    #  wypuszcza ją przymiotnik i liczebnik zgodny obok. Wygląda to poprawnie i
    #  odbiera polszczyźnie prawie każdą taką parę, bo zaimek zgadza się ze swoim
    #  poprzednikiem, który stoi w zdaniu obok. Para zdań łapie obie liczby.
    mnogi = verdict("Jego skutki są znane.")
    assert mnogi.status == "valid", mnogi.explain()
    assert role(mnogi)[0]["podmiot"] == "Jego skutki"
    assert verdict("Ich cena jest niska.").status == "valid"


def test_zaimek_dzierżawczy_bierze_formę_akcentowaną_i_nieprzyimkową():
    #  Enklityka stoi przy czasowniku, a forma przyimkowa po przyimku, więc bez tych
    #  dwóch warunków pozycja bierze `go` oraz `niego`, a zdanie z nimi wychodzi
    #  jednym czytaniem, czyli twierdzeniem. Warunek zbyt szeroki kosztuje z drugiej
    #  strony, dlatego pierwszy ma obok zdanie, które ma przejść.
    #
    #  Warunku drugiego nie sprawdza zdanie bez przyimka: formę przyimkową zdejmuje
    #  tam już morfologia (`po_przyimku`), więc `Znam niego cenę.` byłoby odrzucone
    #  i bez tego warunku. Sprawdza go grupa pod przyimkiem, gdzie ta forma czytanie
    #  zachowuje i gdzie ten warunek jest jedyną rzeczą, która ją odrzuca.
    assert verdict("Znam jego cenę.").status == "valid"
    assert verdict("Znam go cenę.").status == "rejected"
    assert verdict("Cena bez niego zapisu rośnie.").status == "rejected"


# --------------------------------------------------------------------------- #
# Podrzędność
# --------------------------------------------------------------------------- #


def test_zdanie_podrzędne_z_że_wyprowadza_się_raz_mimo_przecinka_koordynacji():
    #  Przecinek koordynuje zdania, więc gramatyka, która bierze go na poziomie
    #  zdania i nie ma podrzędności, czyta zdanie podrzędne jako współrzędne.
    #  Rozdziela je miejsce przecinka: tutaj stoi on wewnątrz konstytuentu,
    #  który zdanie podrzędne tworzy, a nie nad dwoma zdaniami.
    found = verdict("Pomiar mówi, że gramatyka jest podzbiorem.")
    assert found.status == "valid", found.explain()


def test_pytanie_zależne_nie_wychodzi_zdaniem_współrzędnym():
    #  Morfeusz daje `które` ten sam znacznik co `nowe`, więc bez warunku
    #  ujemnego `które zadania własne gminy` jest grupą imienną i staje się
    #  podmiotem zdania po przecinku. Wychodzi z tego jedno czytanie, pewne
    #  siebie i błędne, czyli werdykt najgorszy z tych, jakie olski wydaje.
    #  Zdanie ma jedno czytanie i jest nim pytanie zależne, a nie tamto: role
    #  współrzędnego niosłyby znak sąsiedniego zdania składowego, a role pytania
    #  zależnego są rolami zdania nadrzędnego i tylko nimi.
    found = verdict("Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"podmiot": "Ustawy", "orzeczenie": "określają"}]


def test_pytanie_zależne_z_kto_nie_wychodzi_zdaniem_współrzędnym():
    #  Zdanie to jest werdyktem najgorszym, jaki ten podzbiór wydaje: Morfeusz
    #  czyta `kto` jako zaimek rzeczowny, przecinek koordynuje zdania, więc bez
    #  wykluczenia zaimek staje podmiotem zdania po przecinku i zdanie wychodzi
    #  jednym czytaniem, które polszczyzny nie jest. Statusu to nie rusza — `valid`
    #  było przed wykluczeniem i jest po nim — więc rozdzielają je same role:
    #  ciąg współrzędny niesie dwa zdania składowe, a pytanie zależne jedno.
    found = verdict("Pyta, kto płaci.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"orzeczenie": "Pyta"}]


def test_zaimek_pytajny_o_jednym_słowie_daje_zdaniu_jedno_wyprowadzenie():
    #  Wykluczenie z pozycji rzeczownej i czoło pytania wchodzą razem, bo bez
    #  pierwszego drugie dokłada każdemu takiemu zdaniu drugie wyprowadzenie:
    #  pytanie oraz zdanie oznajmujące zamknięte pytajnikiem, w którym zaimek jest
    #  podmiotem. Oba czytania mają te same role, więc widać je po ich liczbie.
    found = verdict("Kto płaci?")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"podmiot": "Kto", "orzeczenie": "płaci", GRUPA_PYTAJNA: "Kto"}]


def test_przymiotnik_za_zaimkiem_pytajnym_nie_bierze_zaimka_wskazującego():
    #  Usterka, przed którą to stoi: symbol przydawki postawiony w tym ciele
    #  zamiast terminala z wykluczeniem. Morfeusz czyta `to` także jako przymiotnik
    #  od `ten`, więc `co to` wychodzi wtedy grupą pytajną, a polszczyzna ma tam
    #  dwa zaimki obok siebie: pytanie dostaje drugie czytanie, którego nie ma.
    pierwszy = verdict("Kto inny zapisuje ustawienia?")
    assert role(pierwszy) == [
        {
            "podmiot": "Kto inny",
            "dopełnienie": "ustawienia",
            "orzeczenie": "zapisuje",
            GRUPA_PYTAJNA: "Kto inny",
        }
    ], pierwszy.explain()
    #  Zdanie to jest odrzucone i było przyjęte na czytaniu, którego polszczyzna
    #  nie ma: `Co to` wychodziło wyrażeniem przyimkowym przy `jest`, bo kopula
    #  stała wtedy bez orzecznika (:data:`olski.subset.BEZ_KOPULI`). Pytanie tego
    #  testu jest jednak to samo: gdyby `co to` stało się grupą pytajną, zdanie
    #  wróciłoby do przyjętych.
    assert verdict("Co to jest?").status == "rejected"


def test_wykluczenie_zaimka_pytajnego_nie_tyka_pozostałych_zaimków_rzeczownych():
    #  Zawężenie stoi na dwóch lematach, a nie na całej liście zaimków rzeczownych:
    #  `to` i `nic` mają u Morfeusza tę samą klasę, a pytania nie zadaje nimi nikt,
    #  więc pozycję rzeczowną mają dalej.
    assert role(verdict("To jest tanie.")) == [
        {"podmiot": "To", "orzecznik": "tanie", "orzeczenie": "jest"}
    ]
    assert role(verdict("Nic nie rośnie.")) == [{"podmiot": "Nic", "orzeczenie": "nie rośnie"}]


def test_zaimek_pytajny_zastępuje_też_poprzednik():
    #  Ta sama forma, którą zdanie pyta, stoi na czele zdania względnego, a
    #  poprzednikiem jest przy niej zaimek rzeczowny. Bez tego ciała wykluczenie z
    #  pozycji rzeczownej odbiera zdaniu względnemu z `co` każde czytanie, a ten
    #  rejestr pisze je częściej niż pytanie.
    #
    #  Poprzednik stoi tu w podmiocie, bo za orzeczeniem to samo zdanie jest
    #  wieloznaczne: `co` niesie tam także zdanie względne o poprzedniku zdaniowym,
    #  i tę cenę trzyma test niżej razem z zakupem.
    found = verdict("To, co mogło się zepsuć, jest tanie.")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {"podmiot": "To, co mogło się zepsuć,", "orzecznik": "tanie", "orzeczenie": "jest"}
    ]


def test_zdanie_względne_bez_poprzednika_jest_podmiotem_a_nie_zdaniem_współrzędnym():
    #  `Kto` bez poprzednika nazywa sam to, o czym zdanie orzeka, więc zdanie z nim
    #  jest podmiotem zdania nadrzędnego. Bez tej pozycji wychodziło ono zdaniem
    #  współrzędnym, czyli czytaniem nieprawdziwym, a rozdzielają je role: orzeczenie
    #  zdania nadrzędnego jest jedno i stoi za przecinkiem.
    found = verdict("Kto wchodzi w środek, poprzedniego zdania nie przeczytał.")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {
            "podmiot": "Kto wchodzi w środek,",
            "dopełnienie": "poprzedniego zdania",
            "orzeczenie": "nie przeczytał",
        }
    ]


def test_poprzednikiem_zaimka_co_jest_zdanie_a_nie_rzeczownik_przed_przecinkiem():
    #  Usterka, którą to łapie: jedno czoło na oba poprzedniki. Wygląda ona
    #  poprawnie, bo zdanie dalej wychodzi `valid` z jednym czytaniem, a czytanie
    #  jest inne, niż mówi zdanie: zaimek doczepia się przydawką do rzeczownika,
    #  który parę cech ma przypadkiem, i całe zdanie podrzędne wpada w dopełnienie.
    #  Nad Składnicą łapał to jeden wiersz `disagrees` i nic poza nim.
    found = verdict("Sejm zaaprobował przekroczenie, co przekreśliło sens działań.")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {"podmiot": "Sejm", "dopełnienie": "przekroczenie", "orzeczenie": "zaaprobował"}
    ]

    #  Poprzednika rzeczownikowego zaimek `który` ma dalej, i to on rozdziela te dwa
    #  czoła: bez rozdzielenia oba zdania niżej wychodzą tym samym kształtem.
    zgodny = verdict("Sejm zaaprobował przekroczenie, które przekreśliło sens działań.")
    assert zgodny.status == "valid", zgodny.explain()
    assert role(zgodny) == [
        {
            "podmiot": "Sejm",
            "dopełnienie": "przekroczenie, które przekreśliło sens działań",
            "orzeczenie": "zaaprobował",
        }
    ]


def test_poprzednik_zdaniowy_bierze_zaimek_co_a_nie_kto():
    #  Rodzaj zaimka jest tu całym kryterium: pozycja żąda poprzednika nijakiego, bo
    #  tyle niesie `co`, a `kto` jest męskoosobowy. Cechy osobnej na to nie ma, więc
    #  para zdań niżej jest jedynym miejscem, które ten wybór pilnuje.
    #
    #  Przyimek przed zaimkiem wchodzi przez czoło
    #  (`wyrażenie_przyimkowe_względne_rzeczowne`), a nie przez tę pozycję,
    #  i pierwsze zdanie jest tym, co to pokazuje.
    found = verdict("Bierzemy ostry zakręt, dzięki czemu unikamy zderzenia.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"dopełnienie": "ostry zakręt", "orzeczenie": "Bierzemy"}]

    #  Para stoi w tej samej ramie i różni ją sam zaimek, więc mówi o rodzaju, a nie
    #  o czymś innym w zdaniu. Pierwszy wiersz jest ujemny rozmyślnie: `co` daje temu
    #  zdaniu dwa czytania szykiem wewnątrz zdania podrzędnego, czyli różnicą, o
    #  której ten test nie orzeka.
    assert verdict("Cena jest niska, co przekreśla sens działań.").status != "rejected"
    assert verdict("Cena jest niska, kto przekreśla sens działań.").status == "rejected"


def test_orzecznik_wysunięty_na_czoło_nie_wypełnia_szyku_zdania_oznajmującego():
    #  Usterka, którą to łapie: szyk zdania oznajmującego żądający orzecznika bez
    #  cechy `czoło`. Wygląda ona poprawnie, bo zdanie dalej się wyprowadza, a
    #  wyprowadza się dwoma drzewami o tych samych rolach: orzecznik wysunięty
    #  wypełnia wtedy i pytanie, i szyk zdania oznajmującego zamkniętego pytajnikiem.
    #  Żądań orzecznika są trzy, więc pominięcie w którymkolwiek widać dopiero po
    #  liczbie czytań.
    found = verdict("Czym jest parser?")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {"podmiot": "parser", "orzecznik": "Czym", "orzeczenie": "jest", GRUPA_PYTAJNA: "Czym"}
    ]


def test_ciąg_pytań_zależnych_stoi_pod_jednym_czasownikiem():
    #  Czasownik bierze jedno wypełnienie, więc ciąg pytań zajmuje tę pozycję cały.
    #  Znakiem ciągu jest spójnik: przecinek w tym miejscu zamyka zdanie podrzędne,
    #  więc zdanie z przecinkiem samym nie jest ciągiem i nie ma czytania.
    #
    #  Członem jest tu `kto`, a nie `co`, i pilnuje tego sam wiersz z odrzuceniem:
    #  `co` za zdaniem domkniętym niesie zdanie względne o poprzedniku zdaniowym
    #  (`zaimek_względny_rzeczowny` w `olski/subset/podrzędne.py`), więc napis bez spójnika
    #  wyprowadza się tamtędy i o ciągu nie mówi nic. `kto` jest męskoosobowe,
    #  a tamta pozycja żąda poprzednika nijakiego, więc go nie bierze.
    found = verdict("Drzewo mówi, kto jest tematem, a kto jest nowy.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"podmiot": "Drzewo", "orzeczenie": "mówi"}]
    assert verdict("Drzewo mówi, kto jest tematem, kto jest nowy.").status == "rejected"


def test_przecinek_za_pytaniem_zależnym_zamyka_je_i_nie_otwiera_ciągu():
    #  Zdanie nadrzędne biegnie dalej spójnikiem, a przecinek przed nim zamyka
    #  pytanie zależne (`_zamykane`). Ciało ciągu bierze ten sam spójnik, więc bez
    #  tej linii nie widać, że jeden napis nie dostał dwóch wyprowadzeń.
    #
    #  Pytaniem jest tu `kto`, a nie `co`, z tego samego powodu co w teście wyżej:
    #  drugie wyprowadzenie dałoby temu napisowi zdanie względne o poprzedniku
    #  zdaniowym, a nie ciało ciągu, czyli test mierzyłby nie to, co mówi.
    found = verdict("Drzewo mówi, kto jest tematem, i liczy cenę.")
    assert found.status == "valid", found.explain()
    assert found.readings == [
        (
            {"podmiot": "Drzewo", "orzeczenie": "mówi"},
            {"dopełnienie": "cenę", "orzeczenie": "liczy"},
        )
    ]


def test_pytanie_stawia_grupę_pytajną_w_podmiocie_i_w_dopełnieniu():
    #  Dwie role, bo tyle deklaruje `_wysunięta_rola`, i obie idą tą samą
    #  drogą co w zdaniu względnym. Werdykt nazywa grupę pytajną rolą, bo pytanie
    #  przyjęte bez niej nie mówiłoby, o co pyta.
    podmiot = verdict("Który aktor robi na tobie największe wrażenie?")
    assert podmiot.status == "valid", podmiot.explain()
    assert role(podmiot)[0][GRUPA_PYTAJNA] == "Który aktor"
    dopełnienie = verdict("Które zadania gmina wykonuje?")
    assert dopełnienie.status == "valid", dopełnienie.explain()
    assert role(dopełnienie)[0][GRUPA_PYTAJNA] == "Które zadania"


def test_zdanie_pytające_żąda_pytajnika():
    #  Znak jest tu warunkiem, a nie interpunkcją do pominięcia: ta sama forma
    #  zamknięta kropką nie jest polszczyzną, a `KONIEC_ZDANIA` wziąłby oba.
    found = verdict("Który aktor robi na tobie największe wrażenie.")
    assert found.status == "rejected", found.explain()


def test_grupa_pytajna_zgadza_się_ze_swoją_głową():
    #  Zaimek stoi przy rzeczowniku, a nie nad zdaniem, więc niezgodny w rodzaju
    #  nie ma wyprowadzenia. Bez tej zgodności grupa pytajna brałaby każdą formę
    #  zaimka do każdej grupy imiennej.
    found = verdict("Który zadania gmina wykonuje?")
    assert found.status == "rejected", found.explain()


def test_grupa_wysunięta_zgadza_się_z_poprzednikiem_swoim_zaimkiem_a_nie_głową():
    #  Usterka, którą to łapie: liczba i rodzaj wypuszczone z głowy grupy, a nie
    #  z zaimka. Wygląda ona poprawnie, bo grupa imienna wszędzie indziej w tej
    #  gramatyce wypuszcza cechy swojej głowy, i przechodzi każdym zdaniem, w
    #  którym głowa jest tego samego rodzaju co poprzednik — `na podstawie
    #  której` przy `ustawa` jest właśnie takim zdaniem. Rozdziela je głowa
    #  rodzaju innego niż poprzednik: `wyniku` jest męskie, `Reguła` żeńska, a
    #  zaimek zgadza się z poprzednikiem, więc stoi w rodzaju żeńskim.
    found = verdict("Reguła, w wyniku której program zapisuje ustawienia, jest tania.")
    assert found.status == "valid", found.explain()
    głowa = verdict("Reguła, w wyniku którego program zapisuje ustawienia, jest tania.")
    assert głowa.status == "rejected", głowa.explain()


def test_grupa_wysunięta_wchodzi_oboma_szykami_zaimka_i_głowy():
    #  Polszczyzna stawia zaimek w dopełniaczu za głową i przed nią, więc oba
    #  szyki są tu ciałami produkcji. Drugiego z nich nie pilnuje nic poza tą
    #  linią: rejestr ustaw niesie sam pierwszy, więc żaden przebieg nad korpusem
    #  nie zauważy, że ciało z zaimkiem przed głową wyszło z gramatyki.
    za = verdict("Reguła, na podstawie której program zapisuje ustawienia, jest tania.")
    assert za.status == "valid", za.explain()
    przed = verdict("Program, o którego pliku ustawa mówi, jest tani.")
    assert przed.status == "valid", przed.explain()


def test_przyimek_grupy_wysuniętej_rządzi_przypadkiem_głowy_a_nie_zaimka():
    #  Przypadek rozchodzi się w tej grupie w drugą stronę niż liczba i rodzaj:
    #  zaimek jest dopełniaczem przy głowie, a przyimek pyta o przypadek głowy.
    #  Rozdziela to przyimek rządzący dopełniaczem, czyli tym przypadkiem, który
    #  zaimek ma: `bez podstawy której` wyprowadza się, bo dopełniaczem jest tam
    #  głowa, a `bez podstawie której` nie, choć `której` dopełniaczem jest w obu.
    głowa = verdict("Reguła, bez podstawy której program zapisuje ustawienia, jest tania.")
    assert głowa.status == "valid", głowa.explain()
    zaimek = verdict("Reguła, bez podstawie której program zapisuje ustawienia, jest tania.")
    assert zaimek.status == "rejected", zaimek.explain()


def test_grupa_wysunięta_bez_przyimka_zgadza_orzeczenie_z_głową_a_poprzednik_z_zaimkiem():
    #  Obie pary cech czoła widać dopiero tutaj, bo tutaj są różne, i usterką jest
    #  każda z nich wzięta za obie. Para zaimka przyjmuje `której autorzy pisze`,
    #  bo `Ustawa` jest pojedyncza; para głowy przyjmuje `Ustawy, której autorzy
    #  piszą`, bo z `autorzy` zgadza się tam wszystko.
    #
    #  Głowa jest męskoosobowa, bo przy głowie o mianowniku równym biernikowi oba
    #  te napisy wyprowadza czoło w dopełnieniu z opuszczonym podmiotem, więc
    #  odrzucenie nie mówiłoby o parach cech nic.
    found = verdict("Ustawa, której autorzy piszą, jest tania.")
    assert found.status == "valid", found.explain()
    głowa = verdict("Ustawa, której autorzy pisze, jest tania.")
    assert głowa.status == "rejected", głowa.explain()
    zaimek = verdict("Ustawy, której autorzy piszą, są tanie.")
    assert zaimek.status == "rejected", zaimek.explain()


def test_grupa_wysunięta_bez_przyimka_staje_także_w_dopełnieniu():
    #  Drugą rolę deklaruje `_wysunięta_rola` osobno, więc podmiot wyżej o niej
    #  nie świadczy. Przypadka żąda tam czasownik, a nie sama pozycja, więc
    #  przeczenie za nim przestawia grupę na dopełniacz tak samo jak przestawia
    #  czoło o jednym słowie.
    dopełnienie = verdict("Ustawa, której przepisy urzędnik ogłasza, jest tania.")
    assert dopełnienie.status == "valid", dopełnienie.explain()
    przeczenie = verdict("Ustawa, której przepisów urzędnik nie ogłasza, jest tania.")
    assert przeczenie.status == "valid", przeczenie.explain()


@pytest.mark.parametrize(
    "zdanie",
    ["Dyrektor wymienia imprezy, które zorganizował.", "Które zadania wykonuje?"],
)
def test_czoło_w_dopełnieniu_wyprowadza_zdanie_z_opuszczonym_podmiotem(zdanie):
    """Podmiot polszczyzna tutaj opuszcza, więc deklaracje są dwie, jak w zdaniu głównym.

    Zdania są dwa, bo ciała pisze obu rodzinom czół jedna funkcja, a rozejście
    się tych rodzin widać dopiero na zdaniu, którego jedna z nich nie wyprowadza.
    """
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


@pytest.mark.parametrize(
    "zdanie",
    ["Przepisy, o których mowa, są nowe.", "O którym akcie mowa?"],
)
def test_wysunięte_wyrażenie_bierze_rzeczownik_orzekający_pod_oboma_czołami(zdanie):
    """Kopuła opuszczona wchodzi pod czoło zdania względnego i pod czoło pytania.

    Pierwsze zdanie jest tym, na którym stoi rejestr ustaw: `o których mowa` niesie
    co siódme jego zdanie i bez tego ciała nie przechodzi ani jedno
    (docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze). Drugie tego rejestru nie
    ma ani razu, więc pilnuje go sama ta linia: ciało wypisane poza pętlą, która
    obie rodziny czoła obsługuje, dałoby tę konstrukcję jednej z nich, a żaden
    przebieg nad korpusem tego nie zauważy.
    """
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


def test_rzeczownik_orzekający_żąda_tego_o_czym_orzeka():
    #  Kopuła opuszczona żąda tego, o czym ten rzeczownik orzeka, więc stoi on
    #  sam wyłącznie pod wysuniętym wyrażeniem przyimkowym, a w zdaniu składowym
    #  ma przy sobie okolicznik. Bez tego żądania olski przyjmuje `Mowa.` jako
    #  zdanie, czego polszczyzna w tej formie nie ma, a obietnicą podzbioru jest,
    #  że każde zdanie olskiego jest zdaniem polskim.
    samo = verdict("Mowa.")
    assert samo.status == "rejected", samo.explain()
    okolicznik = verdict("Mowa o zadaniach.")
    assert okolicznik.status == "valid", okolicznik.explain()


def test_rzeczownik_orzekający_niesie_etykietę_roli():
    #  Zdanie to nie ma ani podmiotu, ani czasownika, więc bez tej etykiety
    #  wychodzi `valid` bez ani jednej roli, czyli bez słowa o tym, co olski w nim
    #  przyjął. Pilnuje jej samo streszczenie, bo w zdanie względne ono nie
    #  zagląda i tam ta usterka jest niewidoczna (:data:`olski.subset.ORZECZENIE_RZECZOWNIKOWE`).
    found = verdict("Mowa o zadaniach.")
    assert found.status == "valid", found.explain()
    [(reading,)] = found.readings
    assert reading[ORZECZENIE_RZECZOWNIKOWE] == "Mowa", found.explain()


def test_kopuła_opuszczona_żąda_jednej_formy_i_żąda_lematu():
    #  Dwa warunki naraz i każdy jest osobną usterką do zrobienia. Bez lematu
    #  zdaniem wychodzi każda grupa imienna w mianowniku, więc `o których cisza`
    #  przechodzi razem ze zwrotem tego rejestru, a przecinek koordynacji czyta
    #  wtedy wyliczenie jako ciąg zdań
    #  (docs/konstrukcje-gramatyczne/podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat).
    #  Bez liczby przechodzi `o których mowy`, i mianownik sam tego nie łapie:
    #  Morfeusz zna `mowy` i jako dopełniacz pojedynczy, i jako mianownik mnogi,
    #  więc warunek na sam przypadek bierze tę formę drugim czytaniem.
    forma = verdict("Przepisy, o których mowy, obowiązują.")
    assert forma.status == "rejected", forma.explain()
    lemat = verdict("Przepisy, o których cisza, obowiązują.")
    assert lemat.status == "rejected", lemat.explain()


def test_łącznik_wiąże_pozycję_podmiotu_z_grupą_za_sobą():
    #  Obie grupy stoją w mianowniku, więc unifikacja nie odróżnia stron i wybiera
    #  o tym samo ciało. Bank drzew stawia pozycję `subj` za łącznikiem, a wariant
    #  odwrotny przyjmuje te same zdania, czytając je niezgodnie z drzewem
    #  wzorcowym (docs/konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim).
    #  Pytanie idzie tu do streszczenia sprzed przekładu na nazwy szkolne, bo po
    #  przekładzie obie strony wyglądają tak samo, a zgodność ze Składnicą liczy
    #  się właśnie przed nim (`_slot_role` w `harness/corpus.py`).
    found = verdict("Flaga to płat tkaniny określonego kształtu.")
    assert found.status == "valid", found.explain()
    [(wewnętrzne,)] = streszczenia(found.result.readings, DEKLARACJA)
    assert wewnętrzne["podmiot"] == "płat tkaniny określonego kształtu", found.explain()
    assert wewnętrzne[ORZECZNIK_ŁĄCZNIKA] == "Flaga", found.explain()


def test_wydruk_nazywa_podmiotem_grupę_przed_łącznikiem_a_orzecznikiem_tę_za_nim():
    #  Usterka, którą to łapie: nazwy wewnętrzne wypuszczone do werdyktu. Wydruk
    #  czyta człowiek znający składnię szkolną, a ta nazywa te role odwrotnie niż
    #  pozycja `subj` w schemacie GFJP; sąd, który ten przekład wykonuje, stoi
    #  przy `NAZWY_SZKOLNE` w `olski/subset/deklaracja.py`.
    found = verdict("Flaga to płat tkaniny określonego kształtu.")
    [(reading,)] = found.readings
    assert reading["podmiot"] == "Flaga", found.explain()
    assert reading["orzecznik"] == "płat tkaniny określonego kształtu", found.explain()
    assert ORZECZNIK_ŁĄCZNIKA not in reading, found.explain()


def test_przekład_na_nazwy_szkolne_pyta_o_czytanie_a_nie_o_zdanie():
    #  Usterka, którą to łapie: warunek przekładu postawiony na zdaniu. `Ty to
    #  leń.` ma oba czytania naraz — w jednym `Ty` stoi przed łącznikiem, w drugim
    #  jest zwykłym podmiotem — więc przekład puszczony na całe zdanie zamieniłby
    #  podmiot temu drugiemu.
    found = verdict("Ty to leń.")
    assert found.status == "ambiguous", found.explain()
    assert {reading["podmiot"] for (reading,) in found.readings} == {"Ty"}, found.explain()


def test_kopula_łącznika_zgadza_się_z_podmiotem_za_nim_a_nie_z_grupą_przed_łącznikiem():
    #  Usterka, którą to łapie: zgodność związana z grupą przed łącznikiem. Ciało
    #  bezczasownikowe zgodności nie żąda i żądać nie może, bo `Lata
    #  dziewięćdziesiąte to okres rozwoju.` różni się liczbą po obu stronach, więc
    #  strona zgodności rozstrzyga się dopiero tutaj i po wydruku jej nie widać:
    #  oba warianty przyjmują `Kot to jest zwierzę.` i różnią się na tej parze.
    zgodne = verdict("Te książki to jest skarb.")
    assert zgodne.status == "valid", zgodne.explain()
    [(wewnętrzne,)] = streszczenia(zgodne.result.readings, DEKLARACJA)
    assert wewnętrzne["podmiot"] == "skarb", zgodne.explain()
    assert wewnętrzne[ORZECZNIK_ŁĄCZNIKA] == "Te książki", zgodne.explain()

    niezgodne = verdict("Te książki to są skarb.")
    assert niezgodne.status == "rejected", niezgodne.explain()


def test_łącznik_przy_formie_osobowej_żąda_kopuli_a_nie_czasownika_każdego():
    #  Usterka, którą to łapie: ciało napisane na `orzeczenie` bez żądania kopuli.
    #  `to` jest wtedy łącznikiem przy każdym czasowniku, więc `Czytał to
    #  nieforemny chłopak.` dostaje drugie czytanie, w którym `to` nie jest
    #  dopełnieniem, a polszczyzna ma tu jedno.
    found = verdict("Czytał to nieforemny chłopak.")
    assert found.status == "valid", found.explain()
    [(reading,)] = found.readings
    assert reading["dopełnienie"] == "to", found.explain()


def test_przeczenie_stoi_przy_łączniku_i_bez_czasownika_i_z_czasownikiem():
    #  Usterki, które to łapie, są dwie i leżą po przeciwnych stronach. Ciało bez
    #  czasownika napisane bez cząstki gubi zdanie drugie. Ciało dopisane cząstce
    #  przy kopuli, choć ta bierze ją sama, czyni zdanie pierwsze wieloznacznym,
    #  bo `valid` znaczy tu jedno czytanie, a nie jakiekolwiek.
    z_czasownikiem = verdict("Parser to nie jest kompilator.")
    assert z_czasownikiem.status == "valid", z_czasownikiem.explain()

    bez_czasownika = verdict("Parser to nie kompilator.")
    assert bez_czasownika.status == "valid", bez_czasownika.explain()


def test_łącznik_żąda_lematu_a_nie_samej_części_mowy():
    #  Usterka, którą to łapie: ciało łącznika napisane na samą część mowy `pred`.
    #  Predykatyw stoi wtedy między dwiema grupami w mianowniku i olski przyjmuje
    #  `Cena widać koszt.`, czego polszczyzna nie pisze, a obietnicą podzbioru
    #  jest, że każde zdanie olskiego jest zdaniem polskim.
    found = verdict("Cena widać koszt.")
    assert found.status == "rejected", found.explain()


def test_predykatyw_orzeka_bez_podmiotu_i_nie_czyni_go_z_biernika():
    #  Usterka, którą to łapie: predykatyw wpuszczony jako `grupa_orzeczenia`, po którym
    #  `Programy trzeba czytać.` wychodzi zdaniem o podmiocie `Programy`
    #  (docs/konstrukcje-gramatyczne/orzeczenie.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika).
    found = verdict("Trzeba czytać dokumenty.")
    assert role(found)[0][ORZECZENIE_BEZOSOBOWE] == "Trzeba", found.explain()
    wysunięte = verdict("Programy trzeba czytać.")
    assert wysunięte.status == "rejected", wysunięte.explain()


@pytest.mark.parametrize("lemat", sorted(PREDYKATYWY))
def test_każdy_predykatyw_z_listy_ma_czytanie_którego_gramatyka_sięga(lemat):
    #  Usterka, którą to łapie: lemat wpisany na listę, którego Morfeusz pod `pred`
    #  nie ma. `trudno` i `łatwo` są u niego przysłówkami, więc wpisane tutaj byłyby
    #  wierszem martwym, a martwego wiersza nie widać po żadnym zdaniu.
    [segment] = analyse(lemat)
    czytania = [(r.tag.pos, r.lemma, segment.lematy, r.tag.cechy) for r in segment.readings]
    brane = [c for c in czytania if c[0] == "pred" and GRAMMAR.licencjonuje(*c)]
    assert brane, (lemat, czytania)


def test_czasownik_nieosobowy_orzeka_bez_podmiotu_i_nie_czyni_go_z_biernika():
    #  Usterka, którą to łapie: forma `imps` wpuszczona pod symbolem `orzeczenie`.
    #  Zgodności ta forma nie niesie żadnej, a cechy, której konstytuent nie
    #  niesie, unifikacja nie sprawdza, więc pod tamtym symbolem `program`
    #  wychodzi podmiotem, choć jest tam biernikiem
    #  (docs/konstrukcje-gramatyczne/orzeczenie.md#czasownik-nieosobowy-rządzi-ramą-swojego-lematu).
    found = verdict("Zgłoszono program.")
    assert role(found)[0][ORZECZENIE_BEZOSOBOWE] == "Zgłoszono", found.explain()
    assert "podmiot" not in role(found)[0], found.explain()


def test_dopełnienie_wysunięte_przed_głowę_bez_podmiotu_zostawia_okolicznik_za_nią():
    #  Usterki, które to łapie: pozycja wpisana jednej z dwóch głów zamiast wzięta
    #  nazwą symbolu, po której wysunięcie ma predykatyw albo forma nieosobowa, a
    #  nie obie; oraz dopełnienie wpisane pod `wypełnienia`, po którym
    #  `Usterkę zgłoszono wczoraj.` nie ma gdzie postawić okolicznika, bo tamten
    #  symbol stoi w ciele za głową i tylko tam
    #  (docs/konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu).
    forma = verdict("Usterkę zgłoszono.")
    assert role(forma)[0]["dopełnienie"] == "Usterkę", forma.explain()
    predykatyw = verdict("Nic nie widać.")
    assert role(predykatyw)[0]["dopełnienie"] == "Nic", predykatyw.explain()
    #  Okolicznik jest tu przysłówkiem bez czytania rzeczownikowego: `wczoraj` ma
    #  u Morfeusza obok przysłówka rzeczownik nieodmienny, więc stanęłoby zarazem
    #  w okoliczniku narzędnikowym i pytanie o pozycję utonęłoby w tamtej parze.
    okolicznik = verdict("Usterkę zgłoszono szybko.")
    assert okolicznik.status == "valid", okolicznik.explain()
    #  Szyk odwrotny ma własne ciało, a nie przestawienie tego, więc jeden napis
    #  wychodzi jednym wyprowadzeniem, a nie dwoma.
    odwrotny = verdict("Zgłoszono usterkę.")
    assert odwrotny.status == "valid", odwrotny.explain()


def test_czasownik_nieosobowy_nie_bierze_orzecznika_zgodnego():
    #  Usterka, którą to łapie: rama leksykonu wzięta tej formie taka, jaka jest.
    #  Orzecznik zgodny zgadza się z podmiotem, więc zdanie bez podmiotu nie ma go
    #  z czym zgodzić, a zdanie niżej wychodzi wtedy przyjęte.
    found = verdict("Zgłoszono tania.")
    assert found.status == "rejected", found.explain()


def test_czasownik_nieosobowy_bierze_ramę_swojego_lematu_a_nie_jednej_konstrukcji():
    #  Usterka, którą to łapie: jedna rama wpisana tej konstrukcji obok listy
    #  lematów, tak jak ma ją predykatyw. Leksykon mówi, że `pomagać` biernika nie
    #  bierze, i forma nieosobowa tego lematu nie bierze go tak samo.
    biernik = verdict("Pomagano usterkę.")
    assert biernik.status == "rejected", biernik.explain()
    sama = verdict("Pomagano.")
    assert sama.status == "valid", sama.explain()


def test_forma_nieosobowa_z_cząstką_pyta_o_leksykon_zwrotny():
    #  Usterka, którą to łapie: pętla zwrotna pytająca o leksykon niezwrotny.
    #  `bawić` bierze biernik, a `bawić się` nie bierze, więc z tamtego leksykonu
    #  zdanie pierwsze wychodzi przyjęte.
    biernik = verdict("Bawiono się usterkę.")
    assert biernik.status == "rejected", biernik.explain()
    okolicznik = verdict("Bawiono się w parku.")
    assert okolicznik.status == "valid", okolicznik.explain()


def test_czasownik_nieosobowy_przeczy_dopełniaczem_tak_jak_forma_osobowa():
    #  Usterka, którą to łapie: ciało napisane bez cząstki przeczącej. Zdanie z nią
    #  wychodzi wtedy odrzucone, a `nie` czyta się jak brak licencji na formę.
    found = verdict("Nie zgłoszono usterki.")
    assert role(found)[0]["dopełnienie"] == "usterki", found.explain()
    biernik = verdict("Nie zgłoszono usterkę.")
    assert biernik.status == "rejected", biernik.explain()


def test_rzeczownik_orzekający_nie_jest_orzecznikiem_pod_kopulą():
    #  Rola stoi obok orzecznika, a nie jest nim, a to zdanie jest tym, co
    #  tamto wyjście przyjmuje: orzecznik przed kopulą ramy nie żąda, więc rzeczownik
    #  wpuszczony do orzecznika stanąłby tam i przyjął zdanie, w którym olski
    #  czyta orzecznik w mianowniku (:data:`olski.subset.ORZECZENIE_RZECZOWNIKOWE`).
    found = verdict("Mowa jest ustawa.")
    assert found.status == "rejected", found.explain()


def test_oba_ciała_kopuli_opuszczonej_dają_temu_zdaniu_po_jednym_przyłączeniu():
    #  Usterka, którą to łapie: jedno z dwóch ciał zdjęte. Zdania nie odrzuca ani
    #  jedno, bo każde wyprowadza je osobno, tylko każde z innym przyłączeniem
    #  `w ustawie` — pod czołem wychodzi ono do `określa`, a w zdaniu składowym
    #  zostaje przy `mowa` — więc olski wybiera przyłączenie, którego wybierać nie
    #  ma (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    found = verdict("Ustawa określa zadania, o których mowa w ustawie.")
    assert found.status == "ambiguous", found.explain()
    [przyłączenie] = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("określa", "mowa"), found.explain()


@pytest.mark.parametrize(
    ("zdanie", "rola", "czoło"),
    [
        ("Reguła, która rozstrzyga, jest tania.", "podmiot", "która"),
        ("Polszczyzna, którą napisał autor, jest tania.", "dopełnienie", "którą"),
        ("Ustawa, której autorzy piszą, jest tania.", "podmiot", "której autorzy"),
        ("Ustawa, której przepisy urzędnik ogłasza, jest tania.", "dopełnienie", "której przepisy"),
        ("Który aktor robi na tobie największe wrażenie?", "podmiot", "Który aktor"),
        ("Które zadania gmina wykonuje?", "dopełnienie", "Które zadania"),
    ],
)
def test_czoło_niesie_etykietę_roli_którą_zajmuje(zdanie, rola, czoło):
    """Wysunięty konstytuent jest podmiotem albo dopełnieniem i tak się nazywa.

    Bez tej etykiety olski wyprowadza te zdania dokładnie tak, jak czyta je bank
    drzew, a czytanie wychodzi o tę jedną rolę uboższe, więc porównanie ról nie
    ma go z czym zestawić i złote czytanie nie równa się żadnemu
    (docs/corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).
    Pilnuje jej samo drzewo, bo w zdanie względne streszczenie nie zagląda.

    Sześć zdań, bo tyle jest par czoła i roli: sam zaimek, grupa, w której on
    stoi, i grupa pytajna, każde w podmiocie i w dopełnieniu. Grupa pytajna
    niesie tę etykietę obok własnej, a tamtej pilnuje
    :func:`test_pytanie_stawia_grupę_pytajną_w_podmiocie_i_w_dopełnieniu`.
    """
    werdykt = verdict(zdanie)
    assert werdykt.status == "valid", werdykt.explain()
    obsadzone = {" ".join(węzeł.forms()) for węzeł in werdykt.result.readings[0].find(rola)}
    assert czoło in obsadzone


def test_etykieta_roli_nie_wpuszcza_na_czoło_swoich_pozostałych_produkcji():
    """Podmiot na czole zdania względnego jest czołem, a nie każdą grupą imienną.

    Usterka, którą to łapie, jest ceną samej etykiety: `podmiot` wpisany do ciała
    czoła bez cechy rozdzielającej wpuszcza tam `podmiot → grupa_imienna`, więc `reguła, ta
    reguła rozstrzyga` staje się zdaniem względnym, a `Który aktor robi
    wrażenie.` zdaniem oznajmującym o takim podmiocie, czyli wraca czytanie,
    które zdjął warunek na lemat.
    """
    względne = verdict("Reguła, ta reguła rozstrzyga, jest tania.")
    assert względne.status == "rejected", względne.explain()
    oznajmujące = verdict("Który aktor robi wrażenie.")
    assert oznajmujące.status == "rejected", oznajmujące.explain()


def test_czoło_jednej_rodziny_nie_staje_na_czele_drugiej():
    """Zdanie względne bierze swoje czoła, a pytanie swoje.

    Obie rodziny noszą tę samą etykietę roli, więc wartość rozdzielająca jest
    nazwą czoła, a nie jednym „wysunięte”: wspólna zlałaby je i `ustawa, który
    przepis obowiązuje` wyszłoby zdaniem względnym z grupą pytajną na czole,
    a `Który zapisuje ustawienia?` pytaniem o sam zaimek.
    """
    pytajna = verdict("Ustawa, który przepis obowiązuje, jest nowa.")
    assert pytajna.status == "rejected", pytajna.explain()
    zaimek = verdict("Który zapisuje ustawienia?")
    assert zaimek.status == "rejected", zaimek.explain()


def test_pytanie_wysuwa_grupę_pytajną_razem_z_przyimkiem():
    #  Czoło pytania jest tu drugie i jest wyrażeniem przyimkowym, a nie nowym
    #  kształtem grupy: pod przyimkiem stoi ta sama grupa pytajna, którą pytanie
    #  stawia w podmiocie i w dopełnieniu, więc rolę werdykt nazywa tak samo.
    #
    #  Napis roli jest tu drugim żądaniem, a nie sprawdzeniem tego samego dwa
    #  razy. Ta pozycja wynosi grupę pytajną ponad zdanie składowe i jest jedyną,
    #  która robi to bez zdania składowego nad sobą: okolicznik na czele zdania
    #  wynosi rolę tak samo, ale stoi pod symbolem `zdanie_składowe`, a streszczenie bierze
    #  z gałęzi to najwyższe. Bez czoła pytania w `Deklaracja.składowe` pytanie o
    #  jednym zdaniu składowym dostaje więc wielokropek mówiący, że streszczenie
    #  milczy o drugim.
    found = verdict("W którym roku ustawa weszła?")
    assert found.status == "valid", found.explain()
    assert role(found)[0][GRUPA_PYTAJNA] == "którym roku"


def test_pytanie_nie_wysuwa_z_przyimkiem_samego_zaimka():
    #  Rzeczownika ta pozycja żąda, bo pytanie bez niego każe go domyślić z
    #  tego, co stoi obok, a konstrukcji do domyślenia olski nie ma. Wpuszczony
    #  zaimek sam dałby ponadto drugie czytanie każdemu pytaniu tego kształtu.
    found = verdict("W którym ustawa weszła?")
    assert found.status == "rejected", found.explain()


def test_zdanie_względne_zgadza_się_z_poprzednikiem_i_tym_odbiera_przyłączenie():
    #  Liczba i rodzaj zaimka mówią o poprzedniku, a przypadek o roli w zdaniu
    #  podrzędnym, więc `które` w liczbie mnogiej ma się do czego przyłączyć
    #  tylko raz. Gramatyka przyłączenia nie wybiera, tak samo jak przy
    #  wyrażeniu przyimkowym; odbiera je zgodność.
    jedno = verdict("Zbiór tekstów, które są polskie, jest podzbiorem.")
    assert jedno.status == "valid", jedno.explain()
    dwa = verdict("Zbiór tekstu, który jest polski, jest podzbiorem.")
    assert dwa.status == "ambiguous", dwa.explain()
    assert dwa.result.ile == 2


def test_zdanie_względne_nie_daje_dwóch_wyprowadzeń_jednej_struktury():
    #  Usterka, którą to łapie: produkcja rekurencyjna na poziomie członu.
    #  Zdanie względne dochodzi wtedy pod przymiotnikiem i nad nim, czyli
    #  `ci [ludzie, którzy stoją]` obok `[ci ludzie], którzy stoją`,
    #  a te dwa kształty są różne, więc liczą się jako dwa czytania.
    #
    #  Zaimek jest męskoosobowy, bo `które` jest zarazem mianownikiem i
    #  biernikiem, więc zdanie z nim wychodzi drugim czytaniem — z opuszczonym
    #  podmiotem — i to czytanie zasłoniłoby usterkę, o którą tu idzie.
    #
    #  Ten sam napis łapie drugą usterkę tego samego kształtu: ciało z
    #  dopełnieniem przed czasownikiem (:data:`GRUPA_ORZECZENIA_ODWRÓCONA`) biorące
    #  całe wypełnienie ramy zamiast samego dopełnienia. Wypełnienie niesie
    #  okolicznik w swoich ciałach, a przed czasownikiem stawia go także
    #  rozwinięcie szyku, więc `na niej` wychodzi wtedy dwoma wyprowadzeniami.
    found = verdict("Istnieją ci ludzie, którzy na niej stoją.")
    assert found.status == "valid", found.explain()


def test_dopełnienie_przed_czasownikiem_nie_dubluje_szyku_zdania_głównego():
    #  Usterka, którą to łapie: szyk z dopełnieniem przed czasownikiem dopisany
    #  do grupy orzeczenia zamiast do osobnego symbolu. Zdanie główne ma ten szyk już
    #  z deklaracji swoich córek, więc dopisany tam daje jednemu napisowi dwa
    #  wyprowadzenia tego samego kształtu, czyli drugie odczytanie.
    #
    #  Zdanie podrzędne i główne stoją tu obok siebie, bo dopisanie zdejmuje
    #  odrzucenie pierwszemu i wolno mu przy tym nie ruszyć drugiego.
    podrzędne = verdict("Reguła, która tekst sprawdza, jest tania.")
    assert podrzędne.status == "valid", podrzędne.explain()
    główne = verdict("Reguła tekst sprawdza.")
    assert główne.status == "valid", główne.explain()


def test_przysłówek_względny_nie_stoi_okolicznikiem_zdania_współrzędnego():
    #  Usterka, którą to łapie: `gdzie` zostawione w terminalu okolicznika obok
    #  własnego ciała. Zdanie za przecinkiem wyprowadza się wtedy członem
    #  współrzędnym, w którym ta forma jest okolicznikiem, i jest to czytanie,
    #  którego polszczyzna nie ma; drugie czytanie zdania jest tu całą usterką,
    #  bo werdykt bez wykluczenia niczego nie odrzuca.
    #
    #  Dopełnienie jest żeńskie, bo `tekst` jest zarazem mianownikiem i
    #  biernikiem, więc zdanie z nim wychodzi drugim czytaniem na synkretyzmie
    #  i to czytanie zasłoniłoby usterkę, o którą tu idzie.
    found = verdict("Wchodzi w roadmap.md, gdzie linter sprawdza regułę.")
    assert found.status == "valid", found.explain()


def test_przysłówek_względny_określa_drugi_przysłówek():
    #  Wykluczenie wyżej zabiera parę, w której ta forma zdania nie otwiera, więc
    #  para ma własne ciało. Bez niego wykluczenie odbiera zdania, które ta proza
    #  pisze, i jest to cena płacona za czytanie, o które szło tamtemu testowi.
    found = verdict("Cena jest gdzie indziej.")
    assert found.status == "valid", found.explain()


def test_pytanie_o_rozstrzygnięcie_nie_dubluje_się_z_koordynacją():
    #  `czy` bierze zarazem koordynacja bez przecinka, gdzie znaczy `albo`, więc
    #  usterką byłoby czoło pytania biorące człon zamiast zdania: jeden napis
    #  dostałby wtedy oba wyprowadzenia. Rozdziela je materiał pod spójnikiem i
    #  tego pilnuje ta para.
    pytanie = verdict("Pyta, czy go to dotyczy.")
    assert pytanie.status == "valid", pytanie.explain()
    ciąg = verdict("Pyta, kto płaci i czy to działa.")
    assert ciąg.status == "valid", ciąg.explain()


def test_okolicznik_ze_zdania_względnego_zostaje_w_nim():
    #  Zdanie względne jest zdaniem, więc stoi wśród gospodarzy przyłączenia.
    #  Bez tego okolicznik z jego wnętrza wychodzi w górę do grupy imiennej,
    #  którą to zdanie określa, i werdykt nazywa poprzednik zamiast orzeczenia.
    #  Widać to po wpisie o przyłączeniu, bo ten chodzi po lesie i granicy zdania
    #  nie zna; streszczenie o tym okoliczniku milczy, jak o całym tym zdaniu.
    found = verdict("Reguła, która rozstrzyga o zdaniu w pliku, jest tania.")
    assert found.result.ile == 2, found.explain()
    (przyłączenie,) = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("rozstrzyga", "zdaniu")


def test_okolicznik_przy_bezokoliczniku_ma_dwóch_gospodarzy():
    #  Fraza bezokolicznikowa bierze okolicznik przez to samo `wypełnienia`,
    #  którym bierze go forma osobowa nad nią, więc stoi wśród gospodarzy
    #  przyłączenia. Bez niej okolicznik wychodzi do zdania w obu czytaniach,
    #  oba streszczają się jednym napisem, a werdykt mówi samo `2 odczytania`.
    found = verdict("Syn usiłował wejść na ołtarz.")
    assert found.result.ile == 2, found.explain()
    (przyłączenie,) = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("usiłował", "wejść")


def test_streszczenie_nazywa_czasownik_zdania_a_nie_zdania_względnego():
    #  Usterka, którą to łapie: zejście do pierwszego węzła roli, gdziekolwiek on
    #  stoi. Zdanie względne stoi tu w podmiocie, czyli przed czasownikiem
    #  zdania, więc zejście bez granicy nazywa czasownikiem `rozstrzyga`, a
    #  `jest` nie pada wtedy w wierszu wcale.
    roles = role(verdict("Reguła, która rozstrzyga o zdaniu, jest tania."))[0]
    assert roles["orzeczenie"] == "jest"
    assert "wyrażenie_przyimkowe" not in roles


def test_streszczenie_nie_nazywa_roli_wziętej_ze_zdania_dopełnieniowego():
    #  Druga granica, i tu widać ją mocniej: zdanie nadrzędne dopełnienia nie ma
    #  wcale, więc `dopełnienie` wzięty ze zdania podrzędnego nazywa rolę, której to
    #  zdanie nie ma. Wiersz werdyktu łapie przy tym drugie podsumowanie: bez tej
    #  samej granicy ogłasza niezgodę o rolę, której lista czytań nie nazywa.
    #  Wieloznaczność zostaje po tej stronie granicy nazwana konstytuentem, w
    #  którym leży, i tym wierszem, a nie rolą tamtego zdania.
    found = verdict("Ustawa mówi, że organ gminy wydaje przepis.")
    assert found.result.ile == 2, found.explain()
    assert all(
        "dopełnienie" not in składowe for czytanie in found.readings for składowe in czytanie
    )
    assert found.explain() == "2 odczytania; „organ gminy wydaje przepis” ma 2 odczytania"


@pytest.mark.parametrize(
    "zdanie",
    [
        "Program zapisuje ustawienia, ponieważ linter sprawdza dokumentację.",
        "Ponieważ linter sprawdza dokumentację, program zapisuje ustawienia.",
    ],
)
def test_zdanie_okolicznikowe_wyprowadza_się_raz_w_obu_pozycjach(zdanie):
    #  Polszczyzna stawia ten okolicznik przed swoim zdaniem i za nim, a szyku
    #  wewnątrz zdania nadrzędnego nie zmienia ani jedna pozycja, ani druga.
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


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


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Wysunięty modyfikator z okolicznikiem wyrażonym zdaniem, czyli to zdanie,
        #  na którym tę parę kształtów zauważono, oraz z wtrąceniem.
        "Na stole leży sto dwadzieścia chlebów, bo piekarz je tam położył.",
        "Na stole leży chleb (docs/subset.md).",
    ],
)
def test_określenie_z_obu_stron_zdania_nie_daje_dwóch_kształtów(zdanie):
    #  Niezmiennik wyżej mówi o produkcjach, a to zdanie o werdykcie, bo cecha
    #  zapisana w ciałach i zdanie wychodzące jednym czytaniem to dwie rzeczy.
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Cztery zdania podrzędne, po jednym na wywołanie `_zamykane`, bo pozycja
        #  dopisana jednemu z nich nie mówi nic o pozostałych trzech.
        "Dokument mówi, że cena jest niska, i liczy cenę.",
        "Parser jest tani, bo cena jest niska, i gramatyka jest tania.",
        "Dokument mówi, który parser jest tani, i liczy cenę.",
        "Parser czyta regułę, która rozstrzyga, i liczy cenę.",
    ],
)
def test_zdanie_podrzędne_zamyka_się_przecinkiem_przed_spójnikiem(zdanie):
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


def test_przecinek_przed_spójnikiem_bez_zdania_podrzędnego_nie_wyprowadza_się():
    #  Usterka, którą to łapie: przecinek zamykający wpuszczony do koordynacji
    #  zamiast do zdania podrzędnego. Polszczyzna nie stawia go przed `i` między
    #  dwoma zdaniami, więc olski wyprowadzałby wtedy napis, którego ona nie ma.
    found = verdict("Parser jest tani, i gramatyka jest tania.")
    assert found.status == "rejected", found.explain()


@pytest.mark.parametrize(
    "zdanie",
    [
        "Program zapisuje ustawienia ponieważ linter sprawdza dokumentację.",
        "Ponieważ linter sprawdza dokumentację program zapisuje ustawienia.",
    ],
)
def test_zdanie_okolicznikowe_niesie_przecinek_po_stronie_zdania_nadrzędnego(zdanie):
    #  Usterka, którą to łapie: ciało bez cechy wiążącej przecinek z pozycją.
    #  Ciało z przecinkiem z przodu, wpuszczone na czoło zdania, wyprowadza napis
    #  zaczynający się przecinkiem, a ciało z przecinkiem z tyłu, wpuszczone na
    #  koniec, wyprowadza zdanie bez przecinka przed spójnikiem. Polszczyzna
    #  stawia ten znak zawsze, więc oba są zdaniami, których nie ma.
    found = verdict(zdanie)
    assert found.status == "rejected", found.explain()


@pytest.mark.parametrize(
    ("zdanie", "status"),
    [
        ("Program zapisuje ustawienia, gdyż linter sprawdza dokumentację.", "valid"),
        ("Gdyż linter sprawdza dokumentację, program zapisuje ustawienia.", "rejected"),
    ],
)
def test_spójnik_przyczyny_dopowiedzianej_nie_wysuwa_swojego_zdania(zdanie, status):
    #  Wysunięcie jest faktem o słowie, a nie o pozycji, więc ciała biorą dwie
    #  różne listy lematów. Bez tego podziału olski wyprowadza `Gdyż pada,
    #  zostaję w domu.`, czego polszczyzna nie ma, a `ponieważ` w tym samym
    #  miejscu ma i bierze je ciało wysunięte.
    found = verdict(zdanie)
    assert found.status == status, found.explain()


def test_spójnik_żądający_trybu_przypuszczającego_nie_otwiera_okolicznika():
    #  `aby` żąda zdania w trybie przypuszczającym, a cechy trybu żadna produkcja
    #  zdania nie niesie, więc spójnik nie ma czego żądać, choć samą cząstkę `by`
    #  forma czasownika bierze. Wpuszczone na listę spójników okolicznikowych
    #  wyprowadzałoby zdanie, którego polszczyzna nie ma, przeciwko obietnicy
    #  podzbioru.
    found = verdict("Program zapisuje ustawienia, aby linter sprawdza dokumentację.")
    assert found.status == "rejected", found.explain()


def test_streszczenie_nazywa_okolicznik_zdaniowy_a_wnętrza_jego_nie_otwiera():
    #  Usterka, którą to łapie: zejście po role do wnętrza tego okolicznika.
    #  Zdanie podrzędne stoi tu przed zdaniem nadrzędnym, więc zejście bez
    #  granicy nazywa podmiotem `linter`, czyli podmiot tamtego zdania, a nie
    #  tego. Rola jest przy tym nazwana całym napisem, bo symbol stoi i wśród
    #  ról, i wśród zdań podrzędnych.
    roles = verdict("Ponieważ linter sprawdza dokumentację, program zapisuje ustawienia.")
    [(streszczenie,)] = roles.readings
    assert streszczenie["podmiot"] == "program"
    assert (
        streszczenie["okolicznik_zdaniowy"] == "Ponieważ linter sprawdza dokumentację, → zapisuje"
    )


def test_okolicznik_zdaniowy_dochodzi_do_obu_zdań_i_werdykt_to_nazywa():
    #  Okolicznik za zdaniem dopełnieniowym dochodzi do niego i do zdania nad
    #  nim, i są to dwa czytania, które polszczyzna nad tym zdaniem ma. Widać je
    #  po roli, bo streszczenie nazywa ją wtedy, gdy okolicznik stoi w zdaniu
    #  streszczanym, a milczy, gdy stoi w tamtym.
    found = verdict("Pomiar mówi, że autor pisze, ponieważ tekst jest gotowy.")
    assert found.result.ile == 2, found.explain()
    assert found.result.różniące == ("okolicznik_zdaniowy",)
    assert {OKOLICZNIK_ZDANIOWY in reading for reading in role(found)} == {False, True}


def test_okolicznik_zdaniowy_dochodzi_do_całego_ciągu_współrzędnego():
    #  `aby rozwiązać problemy` mówi tu o obu członach naraz, a ciało stawiające
    #  ten okolicznik przy zdaniu składowym daje samo czytanie o członie drugim.
    #  Usterka, którą to łapie, nie jest odrzuceniem: zdanie wychodzi wtedy
    #  jednoznaczne i jednoznaczne jest w nim czytanie, którego czytelnik nie bierze.
    found = verdict("Dwoisz się i troisz, aby rozwiązać problemy.")
    assert found.result.ile == 2, found.explain()
    assert {drugie[OKOLICZNIK_ZDANIOWY] for _pierwsze, drugie in found.readings} == {
        ", aby rozwiązać problemy → troisz",
        ", aby rozwiązać problemy → Dwoisz",
    }


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Okolicznik za zdaniem i przed nim, każdy nad zdaniem o jednym członie.
        "Program zapisuje ustawienia, ponieważ tekst jest gotowy.",
        "Gdyby tekst był gotowy, program zapisałby ustawienia.",
    ],
)
def test_zdanie_o_jednym_członie_nie_bierze_okolicznika_nad_ciągiem(zdanie):
    #  Ciało nad ciągiem żąda ciągu cechą, bo nad zdaniem pojedynczym dawałoby ten
    #  sam napis drugim kształtem: raz z okolicznikiem przy członie, raz nad ciągiem
    #  o jednym członie. Powrotem tamtego stanu jest liczba czytań wyższa niż jeden.
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


# --------------------------------------------------------------------------- #
# Przydawka imiesłowowa
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Imiesłów bierny w obu szykach przydawki, tych samych, które ma przymiotnik.
        "Wymienione zadania są obowiązkowe.",
        "Zadania wymienione są obowiązkowe.",
        #  Imiesłów czynny wraz z dopełniaczem, którego żąda jego czasownik: ciało z
        #  przydawką i dopełniaczem stało w gramatyce przed nim i bierze go za darmo.
        "Reguła sięgająca znaku jest tania.",
    ],
)
def test_przydawka_imiesłowowa_stoi_tam_gdzie_przymiotnik(zdanie):
    found = verdict(zdanie)
    assert found.readings, found.explain()


def test_imiesłów_czynny_nie_dochodzi_do_orzecznika():
    #  Orzecznik bierze `ppas` i nie bierze `pact`, bo `Reguła jest sięgająca.` nie
    #  jest zdaniem tego rejestru. Usterka, którą to łapie: imiesłów wpuszczony
    #  jednym terminalem do obu symboli przymiotnikowych naraz.
    found = verdict("Reguła jest sięgająca.")
    assert found.status == "rejected", found.explain()


# --------------------------------------------------------------------------- #
# Imiesłów przysłówkowy
# --------------------------------------------------------------------------- #


def test_imiesłów_przysłówkowy_bierze_ramę_swojego_lematu():
    #  Rama idzie z głowy cechą, tak samo jak przy formie nieosobowej, więc lemat,
    #  o którym leksykon mówi, że biernika nie bierze, nie bierze go i tutaj.
    #  Usterka, którą to łapie: rama wypisana przy tych ciałach ręką, po której
    #  imiesłów bierze wszystko, co bierze czasownik dowolny.
    assert verdict("Program zapisuje ustawienia, pomagając linterowi.").status == "valid"
    odrzucone = verdict("Program zapisuje ustawienia, pomagając zgodność.")
    assert odrzucone.status == "rejected", odrzucone.explain()


@pytest.mark.parametrize(
    ("zdanie", "gospodarz"),
    [
        #  Imiesłów nie ma pod sobą zdania składowego, więc bez wpisu wśród
        #  gospodarzy zejście mija cały ten okolicznik i nazywa orzeczenie zdania
        #  nadrzędnego. Usterka, którą to łapie: oba czytania mówią wtedy
        #  `→ zapisuje`, więc wychodzą z werdyktu jednym napisem.
        ("Program zapisuje ustawienia, sprawdzając zgodność z dokumentem.", "sprawdzając"),
        #  Drugiej głowy tego symbolu ten sam wpis ruszyć nie ma: pod zdaniem
        #  podrzędnym stoi `zdanie_składowe`, na którym zejście staje wcześniej.
        ("Program zapisuje ustawienia, gdy linter sprawdza zgodność z dokumentem.", "sprawdza"),
    ],
)
def test_gospodarzem_pod_okolicznikiem_jest_jego_własna_głowa(zdanie: str, gospodarz: str):
    found = verdict(zdanie)
    assert f"„z dokumentem” → „{gospodarz}”" in found.explain(), found.explain()


# --------------------------------------------------------------------------- #
# Negacja i dopełniacz, którego ona żąda
# --------------------------------------------------------------------------- #


def test_przeczenie_żąda_od_dopełnienia_dopełniacza():
    #  Biernik pod przeczeniem to jest ta jedna rzecz, którą dopełniacz negacji
    #  zabrania, więc bez tego zakazu cała cecha jest ozdobą: zdanie przeczące
    #  wychodziłoby wtedy dwoma czytaniami zamiast jednego, po jednym na przypadek.
    dopełniacz = verdict("Program nie zapisuje ustawień.")
    assert dopełniacz.status == "valid", dopełniacz.explain()
    assert verdict("Program nie zapisuje plik konfiguracyjny.").status == "rejected"


def test_zdanie_bez_przeczenia_nie_bierze_dopełniacza_negacji():
    #  Druga strona tego samego: gdyby ciało bez cząstki nie ogłaszało `aff`,
    #  dopełniacz negacji stałby w każdym zdaniu, bo cechy, której konstytuent
    #  nie niesie, unifikacja nie sprawdza.
    assert verdict("Program zapisuje ustawień.").status == "rejected"


def test_dopełniacz_negacji_sięga_pod_bezokolicznik_nad_którym_stoi_cząstka():
    #  Rządzenie sięga tu dalej niż zgodność kiedykolwiek: cząstka stoi przy
    #  formie osobowej, a przypadek zmienia się dopełnieniu, które wisi pod
    #  bezokolicznikiem, i przez łańcuch dowolnej długości.
    found = verdict("Program nie pozwala zapisać ustawień.")
    assert found.status == "valid", found.explain()
    assert verdict("Program nie pozwala zapisać ustawienia i dane.").status == "rejected"


def test_przeczenie_przy_bezokoliczniku_zamyka_żądanie_z_góry():
    #  Fraza z własną cząstką nie wypuszcza tej cechy wcale, więc zdanie
    #  nadrzędne, które nie przeczy, nie żąda od niej biernika.
    found = verdict("Program ma nie zapisywać ustawień.")
    assert found.status == "valid", found.explain()


def test_orzecznik_narzędnikowy_stoi_pod_przeczeniem_tak_jak_bez_niego():
    #  Dopełniacz negacji sięga po biernik i po nic więcej, więc kopula pod
    #  przeczeniem bierze swój narzędnik nietknięty.
    found = verdict("Jan nie jest nauczycielem.")
    assert found.status == "valid", found.explain()


def test_zaimek_względny_w_dopełniaczu_przy_przeczącym_zdaniu_względnym():
    #  Przypadek wysuniętego zaimka rozstrzyga przeczenie stojące za resztą
    #  zdania składowego, czyli rządzenie przez cały konstytuent.
    #  Podmiot stoi za czasownikiem, bo rzeczownik zaraz za zaimkiem czyta się
    #  także jako głowa grupy wysuniętej i oba czytania polszczyzna ma.
    found = verdict("Polszczyzna, której nie napisał autor, jest podzbiorem.")
    assert found.status == "valid", found.explain()
    assert verdict("Polszczyzna, którą nie napisał autor, jest podzbiorem.").status == "rejected"


# --------------------------------------------------------------------------- #
# Dopełnienie bezokolicznika wysunięte przed formę osobową
# --------------------------------------------------------------------------- #


def test_dopełnienie_bezokolicznika_wysunięte_przed_formę_osobową_dostaje_swoją_rolę():
    #  Zdanie Składnicy, nad którym bank drzew czyta `premier` podmiotem, a
    #  `większości` dopełnieniem, które bierze `ruszyć`. Bez tej pozycji zostaje
    #  samo czytanie z grupą imienną, więc asercja jest o obu naraz: gramatyka ma
    #  oddać oba, a nie wymienić jedno na drugie.
    found = verdict("Premier większości nie może ruszyć.")
    assert found.result.ile == 2, found.explain()
    assert {streszczenie.get("dopełnienie") for streszczenie in role(found)} == {None, "większości"}


def test_dopełnienie_wysunięte_pyta_o_ramę_bezokolicznika_a_o_przeczenie_formę_osobową():
    #  Dwa kanały biegną tu w przeciwne strony i pomylenie każdego widać osobno.
    #
    #  Rama: celownik wpuszcza leksykon na lemat, `musieć` go nie ma, a `pomagać`
    #  ma, więc pozycja stoi wtedy i tylko wtedy, gdy licencjonuje ją bezokolicznik.
    assert verdict("Program autorowi musi pomagać.").status == "valid"
    assert verdict("Program autorowi musi znać.").status == "rejected"
    assert verdict("Program autorowi musi.").status == "rejected"
    #  Przeczenie odwrotnie: dopełniacza żąda cząstka stojąca przy formie osobowej.
    assert verdict("Premier ustawień może zapisać.").result.ile == 1
    assert verdict("Premier ustawień nie może zapisać.").result.ile == 2


def test_dopełnienie_wysunięte_nie_daje_drugiego_wyprowadzenia_zdaniu_które_już_stoi():
    #  Dopełnienie za swoim bezokolicznikiem wyprowadza się przez `wypełnienia`
    #  bezokolicznika, a pozycja wysunięta ma szyk jeden, ten wypisany, więc napis
    #  ten zostaje przy jednym czytaniu.
    found = verdict("Premier nie może ruszyć większości.")
    assert found.status == "valid", found.explain()


def test_okolicznik_ma_przy_wysuniętym_dopełnieniu_tyle_gospodarzy_ile_bez_niego():
    #  Tor zwykły daje okolicznikowi za bezokolicznikiem dwóch gospodarzy, a przed
    #  nim jednego, bo `wypełnienia` bezokolicznika stoi za swoją głową i przed nią
    #  nie sięga.
    assert verdict("Premier nie może ruszyć szybko.").result.ile == 2
    assert verdict("Premier nie może szybko ruszyć.").result.ile == 1
    #  Wysunięcie dokłada każdemu z tych czytań drugie, z dopełnieniem, i nie dokłada
    #  nic ponad to, więc liczby się podwajają. Nierówność znaczy, że któreś z ciał
    #  wybiera gospodarza przez przeoczenie.
    assert verdict("Premier większości nie może ruszyć szybko.").result.ile == 4
    assert verdict("Premier większości nie może szybko ruszyć.").result.ile == 2


def test_okolicznik_przy_wysuniętym_dopełnieniu_nazywa_swojego_gospodarza():
    #  Bez wpisu w `gospodarze` (`DEKLARACJA`) dwa czytania różne samym miejscem
    #  okolicznika streszczają się jednym napisem, a werdykt milczy o wyborze,
    #  który to zdanie zostawia.
    found = verdict("Premier większości nie może ruszyć szybko.")
    assert len({tuple(sorted(s.items())) for s in role(found)}) == found.result.ile
