"""What olski admits, and what it refuses.

The refusals matter more than the acceptances, and there are two kinds of them:
a sentence with no reading is not olski, and a sentence with more than one is not
olski either.
"""

import os
import subprocess
import sys
from dataclasses import replace

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import EMPTY, Grammar, Głowa, Sym, V, Word, bierze, nt, unify, word
from olski.morph import analyse
from olski.parse import (
    MAX_READINGS,
    PRZYŁĄCZONY_DO,
    SĄSIEDNIE_ZDANIE_SKŁADOWE,
    Cykl,
    Leaf,
    Pozycja,
    las,
    parse,
)
from olski.subset import (
    DEKLARACJA,
    FRAGMENT,
    GRAMMAR,
    OKOLICZNIKOWY,
    PRZECINEK,
    PYTAJNY,
    SPÓJNIK_BEZ_PRZECINKA,
    SPÓJNIK_PRZECINKOWY,
    SPÓJNIKI_PRZECINKOWE,
    WALENCJA,
    WALENCJA_ZWROTNA,
    admissible,
    check,
    morphology,
    sentences,
)


def verdict(text):
    found = check(text)
    assert len(found) == 1, f"expected one sentence, got {len(found)}"
    return found[0]


# --------------------------------------------------------------------------- #
# Unification, which is where agreement lives
# --------------------------------------------------------------------------- #


def test_unification_intersects_feature_values():
    env = unify(frozenset({("case", V("c"))}), {"case": frozenset({"nom", "acc"})}, EMPTY)
    assert env.get("c") == {"nom", "acc"}
    #  A second use of the same variable narrows it.
    narrowed = unify(frozenset({("case", V("c"))}), {"case": frozenset({"acc"})}, env)
    assert narrowed.get("c") == {"acc"}


def test_unification_fails_when_values_do_not_intersect():
    env = unify(frozenset({("case", V("c"))}), {"case": frozenset({"nom"})}, EMPTY)
    assert unify(frozenset({("case", V("c"))}), {"case": frozenset({"acc"})}, env) is None


def test_a_feature_a_word_does_not_have_cannot_disagree():
    #  An uninflected part of speech is not in violation of an agreement it
    #  takes no part in.
    assert unify(frozenset({("case", V("c"))}), {}, EMPTY) is not None


@pytest.mark.parametrize(("forma", "stopniowany"), [("bardzo", True), ("tu", False)])
def test_terminal_żąda_obecności_cechy_a_nie_wartości(forma: str, stopniowany: bool):
    """Żądanie obecności cechy stoi obok unifikacji, bo w niej stać nie może.

    Wypisanie wszystkich wartości cechy wygląda na to samo żądanie i nie jest
    nim: cechy, której forma nie niesie, unifikacja pomija rozmyślnie, więc taki
    terminal bierze `tu` tak samo jak `bardzo`. Oba warunki stoją tu obok siebie,
    bo pomyłka jest właśnie w tym, że jeden podstawia się za drugi.

    Formy przychodzą z Morfeusza, a nie z ręcznie złożonego tagu: różnica, na
    której ten warunek stoi — przysłówek odprzymiotnikowy niesie stopień, a
    pierwotny nie — jest faktem o tagsecie, a nie o tej funkcji.
    """
    [segment] = analyse(forma)
    [czytanie] = segment.readings
    cechy = dict(czytanie.tag.features)
    wartości = word("adv", degree="pos.com.sup")
    obecność = word("adv", niesie="degree")
    assert bierze(wartości, czytanie.tag.pos, czytanie.lemma, cechy, EMPTY) is not None
    wzięty = bierze(obecność, czytanie.tag.pos, czytanie.lemma, cechy, EMPTY) is not None
    assert wzięty is stopniowany


def test_forma_bez_żądanej_cechy_nie_jest_licencjonowana_przez_gramatykę():
    """Odrzucenie ma nazwać formę, na której stanęło, a licencja pyta o terminale.

    Warunek postawiony w tablicy Earleya, a nie w :func:`bierze`, przeszedłby
    testy wyżej i zostawił `Grammar.licencjonuje` przy odpowiedzi, której
    gramatyka nie ma: zdanie wyszłoby odrzucone bez ani jednej formy nazwanej,
    choć stanęło dokładnie na tej jednej.
    """
    grammar = Grammar(start="A")
    grammar.rule("A", [word("adv", niesie="degree")])
    assert grammar.licencjonuje("adv", "bardzo", {"degree": frozenset({"pos"})})
    assert not grammar.licencjonuje("adv", "tu", {})


def test_lewa_rekursja_wyprowadza_się_zamiast_zapętlać():
    #  Zakaz lewej rekursji był ceną enumeratora zstępującego, a tablica Earleya
    #  jej nie płaci: `A` rośnie tu w lewo o interpunkcję i domyka się na
    #  rzeczowniku, a czytanie wychodzi jedno. Wraca przez to wybór, którego olski
    #  nie miał: koordynację wolno teraz napisać jedną produkcją zamiast trzech
    #  poziomów, i TODO.md trzyma, co ten zapis rusza.
    grammar = Grammar(start="A")
    grammar.rule("A", [Głowa(nt("A")), word("interp")])
    grammar.rule("A", [word("subst")])
    [reading] = parse(grammar, morphology("plik.")).readings
    assert reading.span == (0, 2)
    assert [node.span for node in reading.find("A")] == [(0, 2), (0, 1)]


def test_pozycja_stojąca_sama_pod_sobą_jest_zgłaszana_zamiast_liczona():
    #  Czytań jest wtedy nieskończenie wiele, więc liczba z takiego lasu nie jest
    #  liczbą. Wychodzi to dopiero na produkcji jednostkowej w cyklu, bo lewa
    #  rekursja przez terminal rozpiętość powiększa i cyklu nie robi.
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("B")])
    grammar.rule("B", [nt("A")])
    grammar.rule("B", [Głowa(word("subst")), word("interp")])
    with pytest.raises(Cykl):
        parse(grammar, morphology("plik."))


def test_węzeł_bez_dzieci_zna_swoją_rozpiętość():
    #  Rozpiętość wyliczana z `children[0]` i `children[-1]` podnosi na takim węźle wyjątek,
    #  a pyta o nią i zgodność ról z bankiem drzew, i streszczenie czytania.
    #  Produkcji o pustym ciele gramatyka olskiego nie ma, więc test buduje własną:
    #  sprawdzić to można bez dopisywania do niej produkcji,
    #  choć zażąda tego dopiero rozwinięcie szyku do warunków precedencji.
    #  Jest to zarazem jedyne przejście przez pustą produkcję w tablicy Earleya,
    #  gdzie żąda ona osobnej obsługi, więc test pilnuje i tego.
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("Puste"), Głowa(word("subst")), word("interp")])
    grammar.rule("Puste", [])
    [reading] = parse(grammar, morphology("plik.")).readings
    [puste] = reading.find("Puste")
    assert puste.children == ()
    assert puste.span == (0, 0)
    assert reading.span == (0, 2)


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Pod jedną pozycją stoją tu dwie produkcje, a rodzic przyjmuje jedną,
        #  więc iloczyn liczony po samych pozycjach naliczyłby dwa czytania.
        "Zobacz docs/subset.md.",
        #  Tu jest odwrotnie: jeden kształt przechodzi na dwa sposoby, więc dwa
        #  naliczyłaby pozycja rozdzielona po cechach.
        "Projekt jest dla przyjemności.",
    ],
)
def test_czytania_liczy_się_po_kształtach_a_nie_po_wyprowadzeniach(zdanie: str):
    """Oba nadmiary są z przeciwnych stron, i las nie ma prawa na żaden z nich wpaść.

    Zdanie, które przestało pokazywać swój nadmiar, zabiera podstawę wywodowi z
    docs/design-notes.md#co-się-pakuje-rozstrzyga-tożsamość-czytania, i nie widać
    tego po żadnej liczbie: test przechodziłby wtedy sam z siebie.
    """
    wynik = parse(GRAMMAR, morphology(zdanie))
    assert wynik.ile == len(wynik.readings) == 1, wynik.status


def _liście(drzewo):
    return (
        [drzewo]
        if isinstance(drzewo, Leaf)
        else [liść for dziecko in drzewo.children for liść in _liście(dziecko)]
    )


def _po_liściach(liście):
    """Segmenty zdania zawężone do czytań, jakie te liście niosą.

    Zdanie zawężone tak wyprowadza się dokładnie tyle razy,
    ile razy te czytania to drzewo licencjonują,
    i dlatego czytania liści sprawdza sam parser,
    a nie unifikacja napisana w tym pliku drugi raz.
    """
    return [replace(liść.segment, readings=(liść.reading,)) for liść in liście]


@pytest.mark.parametrize(
    "zdanie",
    [
        #  szynki jest dopełniaczem szynki i mianownikiem szynk, a pozycja pod
        #  NPConjunct licencjonuje z tych dwóch sam dopełniacz. Poprawnym zdaniem
        #  to nie jest, więc czytelnik ogląda te drzewa, żeby zobaczyć różnicę.
        "Koszt szynki przewyższa koszt chleba.",
        #  Dobry jest przymiotnikiem zgodnym z kod i nazwiskiem rządzącym
        #  dopełniaczem, a kod ma obok mianownika dopełniacz kody, więc dwa
        #  czytania słownikowe wiążą się tu w ciele parami.
        "Dobry kod zapisuje ustawienia.",
        #  Zdanie poprawne, o jednym czytaniu: ustawienia jest dopełniaczem
        #  liczby pojedynczej i biernikiem mnogiej, a pozycja dopełnienia bierze
        #  drugie z nich.
        "Program zapisuje ustawienia.",
        #  Jeden kształt przechodzi tu na dwa sposoby, czyli w dwóch liczbach, i
        #  cechy liścia idą wtedy za tą, którą drzewo pokazuje.
        "Projekt jest dla przyjemności.",
        #  Zdanie względne, żeby żądanie cech schodziło głębiej niż o jedną córkę.
        "Program zapisuje ustawienia, które sprawdza linter.",
    ],
)
def test_liść_wyliczonego_drzewa_niesie_czytanie_licencjonujące_jego_pozycję(zdanie: str):
    """Drzewo pokazane czytelnikowi ma być tym, co gramatyka nad tymi czytaniami wyprowadza.

    Pakowanie wyłącza z tożsamości czytania lemat i część mowy
    (`Node.signature` w olski/parse.py),
    więc wyprowadzenia różne samą morfologią są jedną klasą,
    a przedstawiciel klasy mógłby nieść czytania liści wzięte spoza niej:
    dopełniacz pod pozycją dopełniacza jest wtedy w drzewie mianownikiem,
    i myli to jedynego czytelnika, jakiego drzewo ma —
    tego, kto je wypisuje, żeby zrozumieć wieloznaczność.
    """
    for drzewo in parse(GRAMMAR, morphology(zdanie)).readings:
        zawężone = las(GRAMMAR, _po_liściach(_liście(drzewo)))
        sygnatury = {czytanie.signature() for czytanie in zawężone.czytania()}
        assert drzewo.signature() in sygnatury, f"{zdanie}: {[*drzewo.forms()]}"


def test_czytanie_liścia_spoza_licencjonujących_zabiera_drzewu_wyprowadzenie():
    """Przesłanka testu wyżej: zawężenie do czytań liści potrafi wyjść źle.

    Bez tego przechodziłby on sam z siebie,
    bo zawężenie, którego żadne czytanie nie odrzuca, nie sprawdza niczego.
    Mianownik `szynk` pod pozycją dopełniacza jest dokładnie tym,
    co tamten test ma łapać, więc tutaj stoi wstawiony ręcznie.
    """
    for drzewo in parse(GRAMMAR, morphology("Koszt szynki przewyższa koszt chleba.")).readings:
        liście = _liście(drzewo)
        [szynki] = [liść for liść in liście if liść.segment.form == "szynki"]
        assert szynki.reading.tag.get("case") == {"gen"}
        [mianownik] = [
            czytanie for czytanie in szynki.segment.readings if czytanie.lemma == "szynk"
        ]
        podmienione = [
            replace(liść, reading=mianownik) if liść is szynki else liść for liść in liście
        ]
        zawężone = las(GRAMMAR, _po_liściach(podmienione))
        assert drzewo.signature() not in {
            czytanie.signature() for czytanie in zawężone.czytania()
        }


def test_pozycja_odrzucona_przez_rodzica_zostaje_w_tablicy():
    #  To jest przesłanka pierwszego z tych dwóch zdań i nie widać jej po liczbie
    #  czytań: tablica domyka pozycję, gdy produkcja doszła do końca ciała, a o
    #  cechy pyta dopiero unifikacja po lesie. `zobacz` ma ramę domyślną, bez
    #  narzędnika, a notacja rejestru dostaje czytanie nieodmienne i przechodzi w
    #  każdym przypadku, więc `Predicative` buduje się nad nią i ginie u rodzica.
    segments = morphology("Zobacz docs/subset.md.")
    [reading] = parse(GRAMMAR, segments).readings
    assert not reading.find("Predicative")
    assert las(GRAMMAR, segments).wyprowadzenia(Pozycja("Predicative", (1, 2)))


#: Siedem przyłączeń, czyli czytań więcej, niż lista wypisuje.
#: Oba testy pod spodem żądają od zdania tego samego, więc stoi tu raz.
SIEDEM_PRZYŁĄCZEŃ = (
    "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci "
    "w firmie w kraju w Polsce."
)


def test_liczba_czytań_nie_urywa_się_tam_gdzie_lista_czytań():
    """Werdykt nad zdaniem o siedmiu przyłączeniach ma być liczbą, a nie „64+”.

    Las liczy sumą po klasach korzenia, więc `MAX_READINGS` ogranicza wypisywanie
    drzew i nie ogranicza liczenia ich.
    """
    wynik = parse(GRAMMAR, morphology(SIEDEM_PRZYŁĄCZEŃ))
    assert wynik.ile == 128
    assert len(wynik.readings) == MAX_READINGS
    assert wynik.truncated


def test_wypisane_czytania_stoją_w_każdym_przebiegu_w_tej_samej_kolejności():
    """Urwana lista ma być za każdym razem tymi samymi czytaniami.

    Kolejność ustala `ciała` w `olski/parse.py` i tam stoi wywód;
    ten test pilnuje, żeby zbiór postawiony gdziekolwiek po drodze z lasu
    nie oddał jej z powrotem haszowaniu napisów.
    Po liczbie czytań tego nie widać, bo ta jest sumą po klasach,
    a ziarno haszowania jest jedno na proces, więc przebiegi są dwa i osobne.
    """
    kod = f"import olski.check; olski.check.main(['--readings', '-c', {SIEDEM_PRZYŁĄCZEŃ!r}])"
    przebiegi = [
        subprocess.run(
            [sys.executable, "-c", kod],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONHASHSEED": ziarno},
        )
        for ziarno in ("1", "2")
    ]
    for przebieg in przebiegi:
        assert przebieg.returncode == 0, przebieg.stderr
    wypisane = [w for w in przebiegi[0].stdout.splitlines() if w.lstrip().startswith("- ")]
    assert len(wypisane) == MAX_READINGS
    assert przebiegi[0].stdout == przebiegi[1].stdout


def test_rola_różniąca_czytania_zostaje_nazwana_zza_granicy_wyliczania():
    """Werdykt liczony po streszczeniach milczałby o wyborze, który to zdanie zostawia.

    Zdanie jest przepisem z rejestru ustaw
    (docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)
    i ma czytań więcej, niż `MAX_READINGS` wypisuje, a wypisane zgadzają się co
    do podmiotu. Ta zgoda jest przesłanką testu: gdy zniknie, zdanie przestaje
    pokazywać, o co tu idzie, a asercja niżej przechodzi sama z siebie.
    """
    werdykt = verdict(
        "Plan ochrony dóbr kultury na czas wojny zawiera wskazanie zadań "
        "ochrony dóbr kultury na czas wojny z określeniem niezbędnych priorytetów."
    )
    assert werdykt.result.truncated
    assert len({streszczenie.get("Subject") for streszczenie in werdykt.readings}) == 1
    assert "Subject" in werdykt.result.różniące


def test_rola_stojąca_w_czytaniu_dwa_razy_nie_jest_niezgodą_między_czytaniami():
    """Zdanie współrzędne ma własny podmiot, a to nie jest różnica między czytaniami.

    Pozycje o etykiecie `Subject` mają w lesie tego zdania różne rozpiętości,
    więc porównanie ich wszystkich naliczyłoby niezgodę tam, gdzie oba czytania
    mówią to samo. Jednym wystąpieniem roli jest to, które nazywa streszczenie:
    pierwsze w porządku wyprowadzenia.
    """
    werdykt = verdict("Program zapisuje ustawienia i użytkownik czyta plik w katalogu.")
    assert werdykt.result.ile == 2
    assert all(len(czytanie.find("Subject")) == 2 for czytanie in werdykt.result.readings)
    assert werdykt.result.różniące == ()


def _role_czytań(zbudowany):
    """Rozpiętości podmiotu i dopełnienia w kolejnych czytaniach, po jednej parze."""
    return [
        (
            frozenset(węzeł.span for węzeł in drzewo.find("Subject")),
            frozenset(węzeł.span for węzeł in drzewo.find("Object")),
        )
        for drzewo in zbudowany.czytania()
    ]


@pytest.mark.parametrize(
    "zdanie",
    [
        "Koszt samej szynki przewyższa koszt szynki z dodatkami.",
        "Program zapisuje ustawienia w pliku w katalogu.",
        "Program zapisuje ustawienia i użytkownik czyta plik w katalogu.",
    ],
)
def test_las_numeruje_te_i_tylko_te_rozdania_ról_które_wychodzą_z_jego_drzew(zdanie: str):
    """Pytanie o czytanie nazwane rolami ma odpowiadać to, co daje wyliczenie.

    Sprawdzane w obie strony, bo osobno łatwo o obie pomyłki: rozdanie z drzewa
    nieznalezione i rozdanie znalezione bez drzewa, które by je dało. Drugie jest
    tym, co robi porównanie po jednej roli naraz — bierze podmiot z jednego
    czytania i dopełnienie z drugiego — więc iloczyn niżej sprawdza właśnie je.

    Sam numer sprawdza się przeciw miejscu w wyliczeniu, bo tym numer jest:
    numer liczony osobno byłby kolejnością czytań wypisaną drugi raz.
    """
    zbudowany = las(GRAMMAR, morphology(zdanie))
    z_drzew = _role_czytań(zbudowany)
    assert len(set(z_drzew)) > 1, "zdanie bez dwóch rozdań niczego tu nie rozstrzyga"
    for podmioty in {rozdanie[0] for rozdanie in z_drzew}:
        for dopełnienia in {rozdanie[1] for rozdanie in z_drzew}:
            role = {"Subject": podmioty, "Object": dopełnienia}
            szukane = (podmioty, dopełnienia)
            oczekiwany = z_drzew.index(szukane) + 1 if szukane in z_drzew else None
            assert zbudowany.numer_czytania(role) == oczekiwany, role


def test_czytanie_nazwane_rolami_znajduje_się_zza_granicy_wyliczania():
    """Pytanie o cudze czytanie idzie do lasu, bo lista czytań urywa się przed nim.

    Zdanie o siedmiu przyłączeniach ma osiem rozdań ról, a wypisane `MAX_READINGS`
    czytań niesie z nich dwa: rozdanie liczone po liście wychodziłoby przepadłe
    sześć razy na osiem. Wieloznaczne są zaś dokładnie te zdania, na których ta
    granica pada, czyli te, o które to pytanie w ogóle się zadaje.

    Numer wychodzi zza tej granicy razem z odpowiedzią, bo granica jest wydruku,
    a nie wyliczenia: gdyby wiązała także tu, sześć z tych ośmiu nie miałoby numeru.
    """
    zbudowany = las(GRAMMAR, morphology(SIEDEM_PRZYŁĄCZEŃ))
    czytania = _role_czytań(zbudowany)
    poza_listą = set(czytania) - set(czytania[:MAX_READINGS])
    assert len(poza_listą) == 6
    for podmioty, dopełnienia in poza_listą:
        numer = zbudowany.numer_czytania({"Subject": podmioty, "Object": dopełnienia})
        assert numer is not None and numer > MAX_READINGS


def test_pusty_zbiór_żąda_czytania_które_tej_roli_nigdzie_nie_obsadza():
    """Etykieta bez rozpiętości jest żądaniem, a nie pominięciem etykiety.

    Bez tego czytanie z dopełnieniem przechodziłoby jako cudze czytanie
    bez dopełnienia, czyli jako to samo czytanie zawężone,
    a `Outcome.agreement` w `olski/coverage.py` liczy taką parę jako niezgodę.
    """
    zbudowany = las(GRAMMAR, morphology("Program zapisuje ustawienia."))
    podmiot = frozenset({(0, 1)})
    assert zbudowany.numer_czytania({"Subject": podmiot, "Object": frozenset({(2, 3)})}) == 1
    assert zbudowany.numer_czytania({"Subject": podmiot, "Object": frozenset()}) is None


def test_werdykt_nazywa_przyimek_i_głowy_a_nie_wylicza_iloczynu():
    """Wpisów jest tyle, ile nierozstrzygniętych wyborów, a nie ile czytań.

    Iloczyn rośnie tu z każdym wyrażeniem przyimkowym, a wyborów jest po jednym na
    wyrażenie, i to jest ta różnica, dla której werdykt pyta las, a nie listę
    czytań (docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań).
    """
    zdanie = "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci w firmie w kraju."
    wynik = parse(GRAMMAR, morphology(zdanie), deklaracja=DEKLARACJA)
    assert wynik.ile == 64
    przyłączenia = wynik.przyłączenia
    assert [p.modyfikator for p in przyłączenia] == [
        "w pliku",
        "w katalogu",
        "w systemie",
        "w sieci",
        "w firmie",
        "w kraju",
    ]
    assert przyłączenia[0].gospodarze == ("zapisuje", "ustawienia")
    assert przyłączenia[-1].gospodarze == ("zapisuje", "firmie")


@pytest.mark.parametrize(
    ("zdanie", "modyfikator", "gospodarze"),
    [
        (
            "Władza zwierzchnia w Rzeczypospolitej Polskiej należy do Narodu.",
            "w Rzeczypospolitej Polskiej",
            ("Władza", "należy"),
        ),
        (
            "Sejm sprawuje kontrolę nad działalnością Rady Ministrów.",
            "nad działalnością Rady Ministrów",
            ("sprawuje", "kontrolę"),
        ),
    ],
)
def test_gospodarza_nazywa_jego_głowa_a_nie_materiał_przed_modyfikatorem(
    zdanie: str, modyfikator: str, gospodarze: tuple[str, ...]
):
    """Głowa rozdziela gospodarzy, którym materiał przed modyfikatorem jest wspólny.

    Grupa imienna otwierająca pierwsze z tych zdań dzieli ten materiał z całym
    zdaniem, więc nazwa wzięta z materiału daje na oboje jeden napis; wywód
    mieści docs/design-notes.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań.
    Oba zdania są wypisane razem z werdyktem w
    docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem.
    """
    found = verdict(zdanie)
    [przyłączenie] = found.result.przyłączenia
    assert przyłączenie.modyfikator == modyfikator
    assert przyłączenie.gospodarze == gospodarze


def test_werdykt_nazywa_konstytuent_gdy_dwa_czytania_mają_jedno_streszczenie():
    """Dwa czytania o jednym napisie mają zostać nazwane, a nie zostać samą liczbą.

    Różni je tu czytanie słownikowe: `zainteresowana` jest i rzeczownikiem, a
    `rada` formą `rad`, więc podmiotem jest w obu czytaniach ten sam napis. Bez
    tego wiersza werdykt mówi samo `2 readings`, a `--readings` drukuje jedno
    streszczenie dwa razy, co po werdykcie czyta się jak usterka narzędzia.
    Zdanie jest z rejestru ustaw
    (docs/ustawy.md#co-gramatyka-z-tego-wyprowadza).
    """
    found = verdict("Dodatkowych przedstawicieli wyznacza zainteresowana rada gminy.")
    assert found.result.ile == 2, found.explain()
    pierwsze, drugie = found.readings
    assert pierwsze == drugie
    [rozbieżność] = found.result.rozbieżności
    assert (rozbieżność.konstytuent, rozbieżność.ile) == ("zainteresowana rada gminy", 2)
    assert found.explain() == "2 readings; „zainteresowana rada gminy” reads 2 ways"


def test_wiersz_o_konstytuencie_nie_powtarza_wyboru_nazwanego_przyłączeniem():
    """Wpisów ma być tyle, ile wyborów, więc wybór nazwany raz nie wraca drugim wierszem.

    Dwanaście czytań tego zdania składa się z trzech gospodarzy jednego
    wyrażenia przyimkowego, dwóch drugiego i dwóch kształtów `ulicy Pomorskiej`,
    a wieloznaczność zamknięta w zdaniu podrzędnym jest poza zasięgiem
    streszczenia: wiersz o przyłączeniu granicy tego zdania nie zna, więc gdyby
    ten wiersz szedł po samej granicy, wypisałby te same dwa wybory jeszcze raz,
    konstytuentem długim na całe zdanie podrzędne. Zdanie jest ze Składnicy.
    """
    found = verdict(
        "Władze miasta zapewniają, że remont kapitalny torowiska na ulicy Pomorskiej "
        "rozpocznie się w pierwszej połowie bieżącego roku."
    )
    assert found.result.ile == 12, found.explain()
    assert [p.modyfikator for p in found.result.przyłączenia] == [
        "na ulicy Pomorskiej",
        "w pierwszej połowie bieżącego roku",
    ]
    [rozbieżność] = found.result.rozbieżności
    assert (rozbieżność.konstytuent, rozbieżność.ile) == ("ulicy Pomorskiej", 2)


@pytest.mark.parametrize(
    ("zdanie", "ile", "konstytuent"),
    [
        (
            "Podręczniki powinny uwzględniać zasadę równych praw kobiet i mężczyzn.",
            7,
            "równych praw kobiet",
        ),
        (
            "Po upływie kadencji rady gminy zarząd działa do dnia wyboru nowego zarządu.",
            3,
            "nowego zarządu",
        ),
    ],
)
def test_wiersz_o_konstytuencie_nazywa_najwęższy_z_nich(zdanie: str, ile: int, konstytuent: str):
    """Jeden wybór to jeden wiersz, choć wieloznaczność jednego słowa wychodzi w górę.

    W pierwszym zdaniu `równych` jest przymiotnikiem albo rzeczownikiem, i przez
    to czyta się dwoma sposobami `równych praw kobiet`, a trzema `równych praw
    kobiet i mężczyzn`, czyli człon ciągu z drugiego czytania; sam ciąg wiersza
    nie dostaje, bo granicę członu pokazuje nawias w napisie roli. W drugim
    dwoma sposobami czyta się `nowego zarządu`, a przez to i `wyboru nowego
    zarządu`, czyli konstytuent o innym początku. Naprawić trzeba w obu wypadkach
    jedno słowo, więc wiersz jest jeden i nazywa napis najkrótszy. Pierwsze
    zdanie jest ze Składnicy, drugie z ustawy o samorządzie gminnym
    (docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem).
    """
    found = verdict(zdanie)
    assert found.result.ile == ile, found.explain()
    assert [r.konstytuent for r in found.result.rozbieżności] == [konstytuent]


def test_a_grammar_referring_to_a_symbol_it_never_defines_is_refused():
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("Nieznane")])
    with pytest.raises(ValueError, match="undefined symbols: Nieznane"):
        parse(grammar, morphology("plik."))


def test_ciało_o_kilku_częściach_bez_głowy_nie_powstaje():
    #  Produkcja dopisana bez znacznika nazwałaby gospodarza przyłączenia pierwszą
    #  córką, cokolwiek nią jest, a werdykt wskazywałby wtedy nie to słowo i nie
    #  mówiłby o tym niczego. Odmowa pada na wierszu, na którym produkcja stoi.
    grammar = Grammar(start="A")
    with pytest.raises(ValueError, match="która jest głową"):
        grammar.rule("A", [word("subst"), word("interp")])


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
    #  A reflexive verb, which is the form with się after it.
    "Program zapisuje się.",
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
    #  Notacja rejestru w roli dopełnienia, czyli jedno zdanie README.
    "Zobacz docs/subset.md.",
    #  Zdanie, którego graf segmentacji się rozchodzi: Morfeusz dzieli Ktoś
    #  na Kto i ś obok formy całej, a ś nie ma ani jednego czytania, które
    #  bierze jakakolwiek produkcja.
    "Ktoś zna docs/subset.md.",
    #  Czas przeszły, czyli forma, która niesie rodzaj i nie niesie osoby.
    "Program zapisywał ustawienia.",
    #  Osoba pierwsza tego czasu, czyli aglutynant, którego Morfeusz odcina od
    #  formy: Napisałem wchodzi tu jako Napisał i em.
    "Napisałem program.",
    #  Czas przeszły dochodzi też do formy z cząstką `się`, czyli do drugiego
    #  leksykonu walencyjnego, a nie tylko do tego bez cząstki.
    "Program otwierał się.",
]


@pytest.mark.parametrize("text", PRZYJMOWANE)
def test_these_are_olski(text):
    assert verdict(text).status == "valid", verdict(text).explain()


@pytest.mark.parametrize("text", PRZYJMOWANE)
def test_zdanie_z_czytaniem_nie_zgłasza_żadnej_formy(text):
    #  Usterka, którą to łapie: werdykt nad zdaniem przyjętym nazywa ś z Ktoś,
    #  czyli krawędź, której ścieżka tego czytania w ogóle nie bierze.
    assert verdict(text).nielicencjonowane == ()


def test_pierwszy_artykuł_deklaracji_stoi_na_przyłączeniu_wyrażenia_przyimkowego():
    #  Zdanie, które wpędziło do gramatyki konstrukcje wyliczone wyżej: czasownik
    #  zwrotny, orzecznik i dopełniacz w koordynacji, kwantyfikator. Wszystkie w
    #  nim są, a zdaniem olskim nie jest, bo pod względem swej godności określa
    #  równych albo całe zdanie, i te dwa czytania olski melduje zamiast wybierać
    #  jedno z nich.
    found = verdict(
        "Wszyscy ludzie rodzą się wolni i równi "
        "pod względem swej godności i swych praw."
    )
    assert found.status == "ambiguous", found.explain()
    #  Nawias nazywa człon, w którym wyrażenie się znalazło, czyli mówi, że wzgląd
    #  określa samych równych: ciąg wiąże się w prawo, więc drugim członem jest
    #  `równi` wraz z tym wyrażeniem, a nie para `wolni i równi`.
    assert {reading["Predicative"] for reading in found.readings} == {
        "wolni i równi",
        "wolni i [równi pod względem swej godności i swych praw]",
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
    assert {reading["Object"] for reading in found.readings} == {
        "ustawienia domyślne użytkownika w pliku",
        "ustawienia domyślne użytkownika",
    }


def test_predykatyw_przed_czasownikiem_nie_jest_czytany_jako_podmiot():
    #  Lustro reguły OVS. Bez niego ten sam szyk wychodził raz tak, a raz wcale,
    #  zależnie od tego, czy po czasowniku stoi dopełnienie, czy orzecznik, a
    #  ryzykiem przy nim jest zamiana ról: podmiot stoi tu za czasownikiem.
    found = verdict("Wejściem jest zwykły tekst polski.")
    assert found.status == "valid", found.explain()
    assert found.readings[0] == {
        "Subject": "zwykły tekst polski",
        "Predicative": "Wejściem",
        "Verb": "jest",
    }


def test_a_valid_sentence_says_what_fills_each_role():
    roles = verdict("Program zapisuje ustawienia.").readings[0]
    assert roles["Subject"] == "Program"
    assert roles["Object"] == "ustawienia"
    assert roles["Verb"] == "zapisuje"


def test_a_fronted_modifier_belongs_to_the_clause_and_not_to_the_subject():
    #  Nothing but the clause rule can take it there, and the failure to guard
    #  against is the subject swallowing it: NPConjunct → subst Modifier makes
    #  the same phrase between the subject and the verb come out valid and wrong.
    roles = verdict("Pod względem smaku chałka przewyższa zwykłą bułkę.").readings[0]
    assert roles["Subject"] == "chałka"
    #  Streszczenie nazywa konstytuent, do którego przyłączenie doszło, jego
    #  głową, więc zdanie z nazwy tego testu stoi w samym napisie, a nie tylko w
    #  podmiocie obok: gospodarzem jest tu czasownik, a nie `chałka`.
    assert roles["Modifier"] == "Pod względem smaku → przewyższa"


def test_object_first_order_is_polish_and_is_read_that_way():
    #  Free word order is real: here the plural verb forces the plural noun to
    #  be the subject, so the sentence is unambiguous despite the OVS order.
    roles = verdict("Program zapisują ustawienia.").readings[0]
    assert roles["Subject"] == "ustawienia"
    assert roles["Object"] == "Program"


def test_dopełniacz_negacji_przed_czasownikiem_ma_czym_się_wyprowadzić():
    #  Bez szyku SOV `tego` brała tu tylko przydawka dopełniaczowa, więc zdanie
    #  wychodziło jednym czytaniem, pewnym siebie i odwrotnym niż drzewo wzorcowe.
    #  Usterka, którą to łapie, jest powrotem tamtego stanu: zdanie znów wychodzi
    #  jednoznaczne, a rola, którą czyta czytelnik, nie ma ciała.
    found = verdict("Apostołowie tego nie praktykowali.")
    assert found.status == "ambiguous", found.explain()
    czytania = {(reading.get("Subject"), reading.get("Object")) for reading in found.readings}
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


def test_cyfra_nie_jest_liczebnikiem_bo_nie_niesie_ani_przypadka_ani_liczby():
    #  Rejestr, o który olskiemu chodzi, pisze liczebnik cyfrą, a Morfeusz daje jej
    #  tag `dig` bez ani jednej cechy, więc oba ciała biorą ją naraz i `14 dni`
    #  wychodzi dwoma wyprowadzeniami o jednym streszczeniu. Odmowa jest przez to
    #  rozstrzygnięciem, a nie przeoczeniem, i docs/subset.md trzyma jej cenę.
    werdykt = verdict("Termin wynosi 14 dni.")
    assert werdykt.status == "rejected"
    assert werdykt.nielicencjonowane == ("14",)


def test_odrzucenie_odróżnia_formę_bez_produkcji_od_struktury_bez_produkcji():
    #  Dwie odpowiedzi, które Świgra trzyma osobno, i dwie różne roboty do
    #  zrobienia. Formy, której Morfeusz odmienioną nie zna, nie bierze żaden
    #  terminal; Nowa program ma każdą formę wziętą i stoi na zgodności rodzaju,
    #  więc test pilnuje, żeby zdania zostały dwa.
    forma = verdict("Konwencje prozy, kodu, testów i commitów trzyma CLAUDE.md.")
    assert forma.nielicencjonowane == ("commitów",)
    assert "no production takes" in forma.explain()
    struktura = verdict("Nowa program zapisuje ustawienia.")
    assert struktura.nielicencjonowane == ()
    assert struktura.explain() == "no reading: nothing in olski derives this"


def test_licencja_bierze_się_z_gramatyki_a_nie_z_listy_obok_niej():
    #  Gramatyka, która nie ma czasownika, przestaje licencjonować jego czytanie:
    #  gdyby licencja stała napisana obok, ta zmiana nie doszłaby do niej wcale.
    uboga = Grammar(start="NP")
    uboga.rule("NP", [word("subst")])
    czytanie = next(r for r in analyse("zapisuje")[0].readings if r.tag.pos == "fin")
    cechy = dict(czytanie.tag.features)
    assert not uboga.licencjonuje(czytanie.tag.pos, czytanie.lemma, cechy)
    assert GRAMMAR.licencjonuje(czytanie.tag.pos, czytanie.lemma, cechy)


def test_a_rejection_says_how_far_the_analysis_got_when_asked_and_not_otherwise():
    """``0`` would pass for an answer, so the unasked case is pinned here as well.

    Asking costs a second walk over the table,
    so a parse that was not asked holds ``None`` rather than a position.
    """
    #  Polish puts a comma in front of ale and this sentence has none, so no level
    #  of coordination derives it and the analysis stops on the conjunction itself.
    #  The form is licensed all the same, by the position that has the comma, so
    #  the list of unlicensed forms is empty and the furthest point is what says
    #  where the sentence ran out.
    zdanie = "Plany są niczym ale planowanie jest wszystkim."
    result = parse(GRAMMAR, morphology(zdanie), najdalszy=True)
    assert result.rejected
    assert result.furthest == 3
    assert verdict(zdanie).result.furthest is None


# --------------------------------------------------------------------------- #
# Sentences with more than one reading, which olski refuses just as firmly
# --------------------------------------------------------------------------- #


def test_case_syncretism_plus_free_word_order_makes_a_sentence_ambiguous():
    #  koszt is nominative or accusative and Polish permits both SVO and OVS,
    #  so this sentence does not say which cost is the greater one.
    found = verdict("Koszt samej szynki przewyższa koszt szynki z dodatkami.")
    assert found.status == "ambiguous"
    subjects = {reading["Subject"] for reading in found.readings}
    #  Trzeci podmiot jest z drugiej wieloznaczności, nie z tej: z dodatkami
    #  dochodzi do zdania zamiast do kosztu, więc podmiotem zostaje sam koszt.
    assert subjects == {"Koszt samej szynki", "koszt szynki z dodatkami", "koszt szynki"}
    assert "Subject" in found.explain()


def test_the_same_comparison_is_unambiguous_when_the_cases_are_not_syncretic():
    #  Same verb in the same frame as the sentence above, but chałka is
    #  nominative only and bułkę accusative only, so OVS has nowhere to derive:
    #  what that sentence loses, it loses to the syncretism and not to the verb.
    found = verdict("Chałka przewyższa zwykłą bułkę.")
    assert found.status == "valid", found.explain()
    assert found.readings == [
        {"Subject": "Chałka", "Object": "zwykłą bułkę", "Verb": "przewyższa"}
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
    assert len({reading["Object"] for reading in found.readings}) == 2


def test_czytania_różne_samym_przyłączeniem_wychodzą_osobnymi_streszczeniami():
    #  W tym zdaniu stoją dwie wieloznaczności naraz i po rolach widać jedną:
    #  dwie pary czytań różnią się samym miejscem, do którego doszło `z dodatkami`,
    #  a formy nad nim stojące zostają w każdej parze te same.
    #  Streszczenie, które przyłączenia nie nazywa, oddaje więc cztery napisy na sześć czytań
    #  i o dwóch milczy, choć są to dwa różne zdania o szynce.
    found = verdict("Koszt samej szynki przewyższa koszt szynki z dodatkami.")
    napisy = {tuple(sorted(reading.items())) for reading in found.readings}
    assert len(napisy) == len(found.readings) == 6
    assert {reading["Modifier"] for reading in found.readings} == {
        "z dodatkami → koszt",
        "z dodatkami → szynki",
        "z dodatkami → przewyższa",
    }


def test_streszczenie_wiąże_okolicznik_ze_zdaniem_a_nie_z_dopełnieniem():
    #  `Adjuncts` stoi w drzewie pod `Complements`, czyli tuż obok dopełnienia,
    #  więc przyłączenie wzięte z najbliższego węzła z materiałem obok
    #  nazwałoby okolicznik zdania określeniem dopełnienia —
    #  i byłoby to akurat to drugie czytanie, od którego olski to pierwsze odróżnia.
    found = verdict("Program zapisuje ustawienia w pliku w katalogu.")
    zdaniowe = [reading for reading in found.readings if reading["Object"] == "ustawienia"]
    assert {reading["Modifier"] for reading in zdaniowe} == {
        "w pliku → zapisuje",
        "w pliku w katalogu → zapisuje",
    }


def test_streszczenie_nie_wstawia_odstępu_przed_przecinkiem():
    #  Przecinek jest segmentem jak każde inne słowo, więc sklejenie form przez sam
    #  odstęp dawało `ustawienia , dane i pliki`, czyli napis, którego w tym zdaniu
    #  nikt nie napisał. Usterka jest widoczna w każdym zdaniu z koordynacją
    #  przecinkiem i w żadnym innym.
    roles = verdict("Program zapisuje ustawienia, dane i pliki.").readings[0]
    assert roles["Object"] == "ustawienia, dane i pliki"


def test_czytanie_rozcinające_zdanie_nie_wychodzi_streszczeniem_całości():
    #  Usterka, którą to łapie: streszczenie czytające się jak streszczenie całości.
    #  Morfeusz zna `szczęśliwi` jako `szczęśliwić fin:sg:ter:imperf`, więc `i szczęśliwi`
    #  wychodzi drugim zdaniem składowym bez podmiotu, a nazwane jest pierwsze
    #  wystąpienie każdej roli, czyli same role zdania pierwszego. Bez znaku wiersz
    #  mówi `Predicative: wolni, równi`, o reszcie zdania milczy i nie widać,
    #  że dwa czytania różni rozcięcie zdania na dwa, a nie żadna rola.
    found = verdict("Ludzie są wolni, równi i szczęśliwi.")
    assert {reading["Predicative"] for reading in found.readings} == {
        "wolni, równi i szczęśliwi",
        "wolni, równi…",
    }


def test_znak_składowej_pada_po_tej_stronie_roli_po_której_zdanie_idzie_dalej():
    #  Zdanie jednoznaczne, więc znak nie bierze się z żadnej wieloznaczności:
    #  dopełnienie jest w drugim zdaniu składowym, a podmiot i czasownik w pierwszym,
    #  i widać to po stronie, z której pada znak.
    [roles] = verdict("Program działa i zapisuje ustawienia.").readings
    assert roles == {"Subject": "Program…", "Object": "…ustawienia", "Verb": "działa…"}


def test_okolicznik_na_czele_zdania_znaku_składowej_nie_dostaje():
    #  Usterka, którą to łapie: zdanie składowe policzone dwa razy. Okolicznik
    #  zdania dokłada nad składowym drugi węzeł o tej samej etykiecie
    #  (`ClauseConjunct → Modifier ClauseConjunct`), więc zbieranie wszystkich
    #  takich węzłów zamiast najwyższego w gałęzi widzi tu ciąg dwóch zdań
    #  i znakuje sam okolicznik, choć zdanie składowe jest jedno.
    [roles] = verdict("Pod względem smaku chałka przewyższa zwykłą bułkę.").readings
    assert SĄSIEDNIE_ZDANIE_SKŁADOWE not in "".join(roles.values())


def test_dwa_czytania_różne_granicą_członu_nie_wychodzą_jednym_napisem():
    #  Usterka, którą to łapie: streszczenie sklejone z samych form. Dwa z tych
    #  trzech czytań mają w każdej roli te same formy i różnią się granicą członu
    #  wewnątrz dopełnienia, więc bez nawiasu dawały znak w znak ten sam wiersz,
    #  co po werdykcie czyta się jak usterka narzędzia, a nie jak dwa czytania.
    #  Ciąg wpuszcza tu `sera` dlatego, że forma jest i dopełniaczem od `ser`,
    #  i biernikiem mnogim od `serum`, a biernika żąda pozycja dopełnienia.
    found = verdict("Koszt szynki i sera przewyższa koszt chleba.")
    streszczenia = [tuple(sorted(reading.items())) for reading in found.readings]
    assert len(set(streszczenia)) == len(streszczenia), found.explain()
    assert "[Koszt szynki] i sera" in {reading["Object"] for reading in found.readings}


@pytest.mark.parametrize("symbol", ["Verb", "Subject"])
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
    for production in GRAMMAR.productions:
        if production.head == symbol:
            assert "gender" in dict(production.features), production


@pytest.mark.parametrize("symbol", DEKLARACJA.współrzędne)
def test_symbol_współrzędny_stoi_nad_sobą_dokładnie_tam_gdzie_ma_znak_koordynacji(symbol):
    #  Kryterium, na którym stoją dwie rzeczy naraz: `_nawiasuj` w `olski/parse.py`
    #  poznaje ciąg współrzędny po tym, że symbol stoi nad sobą, i po tym samym
    #  poznaje go `sonda/przecinek.py`, żeby wiedzieć, którą produkcję zdjąć.
    #  Produkcja, która to rozdziela, psuje jedno z dwóch po cichu: nawias staje
    #  tam, gdzie ciągu nie ma, albo sonda zdejmuje zdanie podrzędne zamiast
    #  koordynacji. Pusta lista łapie przemianowany symbol.
    produkcje = [production for production in GRAMMAR.productions if production.head == symbol]
    assert produkcje, symbol
    for production in produkcje:
        nad_sobą = any(
            isinstance(part, Sym) and part.name == symbol for part in production.body
        )
        ze_znakiem = any(
            isinstance(part, Word) and (part == PRZECINEK or "conj" in part.pos)
            for part in production.body
        )
        assert nad_sobą == ze_znakiem, production


def test_dwukropka_bierze_jedna_produkcja_więc_nie_ma_z_czym_konkurować():
    #  Na tej jedynce stoi zdanie, że dwukropek nie odbiera jednoznaczności ani
    #  jednemu zdaniu: znak wchodzący w jedno ciało albo wyprowadza zdanie tą
    #  produkcją, albo nie wyprowadza go wcale. Drugie ciało z dwukropkiem czyni
    #  z tego zera liczbę do zmierzenia i ten test jest tym, co o tym powie.
    biorące = [
        produkcja
        for produkcja in GRAMMAR.productions
        if any(
            isinstance(część, Word) and bierze(część, "interp", ":", {}, EMPTY) is not None
            for część in produkcja.body
        )
    ]
    assert len(biorące) == 1, biorące


@pytest.mark.parametrize("lemat", SPÓJNIKI_PRZECINKOWE.split("|"))
def test_dwie_klasy_spójnika_zdaniowego_nie_zachodzą_na_siebie(lemat: str):
    #  Lemat wzięty obiema pozycjami dałby polszczyźnie i `A, ale B`, i `A ale B`,
    #  a pominięty na liście nie wszedłby do żadnej z nich. Literówka wygląda
    #  dokładnie tak jak pominięcie: pozycja z przecinkiem milczy wtedy o słowie
    #  i nie widać tego po żadnym zdaniu.
    czytania = [(r.tag.pos, r.lemma) for r in analyse(lemat)[0].readings]
    brane = [c for c in czytania if bierze(SPÓJNIK_PRZECINKOWY, *c, {}, EMPTY) is not None]
    assert brane, (lemat, czytania)
    assert not [c for c in czytania if bierze(SPÓJNIK_BEZ_PRZECINKA, *c, {}, EMPTY) is not None]
    #  Spójnik spoza listy idzie odwrotnie, więc klasy pokrywają ją całą.
    assert bierze(SPÓJNIK_BEZ_PRZECINKA, "conj", "i", {}, EMPTY) is not None
    assert bierze(SPÓJNIK_PRZECINKOWY, "conj", "i", {}, EMPTY) is None


def test_rozdzielające_a_nie_wchodzi_do_wyrażenia_przyimkowego():
    #  Usterka, którą to łapie, jest usterką werdyktu, a nie pokrycia: `a` ma w
    #  słowniku czytanie przyimkowe rządzące mianownikiem, więc bez tego warunku
    #  każde czytanie tego zdania niesie okolicznik `a linter`, którego zdanie nie
    #  ma, i przecinek przed spójnikiem nie ma czego kupić.
    found = verdict("Program zapisuje ustawienia, a linter sprawdza polszczyznę.")
    assert found.status == "valid", found.explain()
    assert all("Modifier" not in reading for reading in found.readings)


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
        "4 readings, differing in Object; "
        "„w pliku” → „zapisuje”, „ustawienia”; "
        "„w katalogu” → „zapisuje”, „pliku”"
    )
    assert sześć.explain().count(PRZYŁĄCZONY_DO) == 6
    assert sześć.explain().startswith("64 readings, differing in Object; „w pliku” → ")


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
    #  Wielokropek jest z drugiej koordynacji: okolicznik stoi w drugim zdaniu
    #  składowym, a streszczenie opisuje jedno zdanie i tym znakiem to mówi.
    #
    #  Dwa ostatnie wiersze są ceną przysłówka i nie są przyłączeniem: Morfeusz
    #  daje formie `wobec` czytanie przysłówkowe obok przyimkowego, więc okolicznik
    #  zdania bierze ją jako słowo, a `innych` zostaje wtedy dopełnieniem. Jest to
    #  czytanie, którego polszczyzna w tym miejscu nie ma, i klasa, po którą
    #  `admissible` nie sięga, bo tamten warunek pyta o czytanie rzeczownikowe;
    #  TODO.md trzyma ruch i pomiar, którego on żąda.
    assert {reading["Modifier"] for reading in found.readings} == {
        "…wobec innych → postępować",
        "…wobec innych w duchu → postępować",
        "…wobec innych w duchu braterstwa → postępować",
        "…w duchu braterstwa → postępować",
        "…w duchu braterstwa → innych",
    }


def test_rama_kopuli_zdejmuje_dopełnienie_którego_nikt_w_tym_zdaniu_nie_ma():
    #  wolny czyta się jako przymiotnik i jako rzeczownik, a być dopełnienia w
    #  bierniku nie bierze, więc czytania z dopełnieniem nie ma żaden czytelnik
    #  tego zdania. Zabiera je rama kopuli i to jest to, co walencja kupuje.
    #  Zostają dwa czytania i każde stoi na innej dziurze: rzeczownikowym czytaniu
    #  przymiotnika, i na tym, że On jest w słowniku Morfeusza nazwiskiem
    #  nieodmiennym, więc staje tam, gdzie stoi orzecznik wysunięty, a wykluczenie
    #  słownikowe go zostawia, bo zaimek wyrazem funkcyjnym nie jest.
    found = verdict("On jest wolny.")
    assert found.status == "ambiguous"
    assert found.readings == [
        {"Subject": "On", "Predicative": "wolny", "Verb": "jest"},
        {"Subject": "wolny", "Predicative": "On", "Verb": "jest"},
    ]


def test_orzecznik_w_narzędniku_bierze_tylko_kopula():
    #  Ta sama luka, z której da się wyjąć jeden slot i nie więcej. Bez
    #  ograniczenia narzędnik okolicznikowy czyta się jako orzecznik pod każdym
    #  czasownikiem, co docs/corpus.md liczy jako niezgodność z bankiem drzew:
    #  handel wychodzi wtedy orzekany o paszportach, a nie kwitnący w nich.
    assert verdict("Kwitnie handel paszportami.").status == "rejected"
    assert verdict("Jan jest nauczycielem.").status == "valid"


@pytest.mark.parametrize(
    ("text", "status"),
    [
        ("Program pozwala zostać nauczycielem.", "valid"),
        ("Program pozwala zapisać ustawienia.", "valid"),
        ("Program pozwala zapisać nauczycielem.", "rejected"),
        ("Program pozwala zostać ustawienia.", "rejected"),
    ],
)
def test_rama_dochodzi_do_bezokolicznika_tak_samo_jak_do_formy_osobowej(text, status):
    #  Bezokolicznik bierze dopełnienia z tego samego leksykonu, co forma osobowa,
    #  i widać to dopiero na parze zdań: samo przyjęcie dwóch pierwszych
    #  przechodziłoby też gramatyce, która bezokolicznikowi ramy nie stawia wcale.
    assert verdict(text).status == status


def test_pozycje_okolicznika_w_orzeczeniu_nie_zachodzą_na_siebie():
    #  Cztery ciała `Complements` stawiają okolicznik przed dopełnieniem i za nim,
    #  a `Adjuncts` nawraca samo na siebie, więc dwie pozycje łatwo tu wypisać tak,
    #  żeby jedno zdanie wychodziło dwoma kształtami drzewa. Nie widać tego po
    #  werdykcie, bo zdanie jest wieloznaczne w jedną i w drugą stronę, i nie widać
    #  po rolach, bo obie pary przyłączeń zostają te same; widać po liczbie czytań.
    #  Werdykt nazywa tu jedno przyłączenie z dwóch, i to jest ta ostrość, którą
    #  las kupuje: `w pliku` dochodzi do zdania w obu czytaniach.
    found = verdict("Program zapisuje w pliku w katalogu.")
    assert found.explain() == '2 readings; „w katalogu” → „zapisuje”, „pliku”'


@pytest.mark.parametrize("leksykon", [WALENCJA, WALENCJA_ZWROTNA])
def test_klasy_walencyjne_nie_zachodzą_na_siebie(leksykon):
    #  Lemat wzięty dwiema klasami jest dwoma czytaniami tego samego kształtu, a
    #  te dwa zwijają się w jedno, bo czytanie liczy kształt: werdykt tego nie
    #  pokaże i żaden inny test tu nie sięga. Zachodzą klasy łatwo, bo Walenty
    #  mówi o kopuli to samo, co o każdym innym lemacie leksykonu, więc wpis
    #  ręczny musi swoje lematy leksykonowi zabrać, a nie stanąć obok nich.
    lematy = [lemat for alternatywa in leksykon.values() for lemat in alternatywa.split("|")]
    assert len(lematy) == len(set(lematy))


def test_cząstka_się_pyta_leksykonu_o_inny_czasownik_niż_forma_bez_niej():
    #  Otwierać bierze dopełnienie w bierniku, a otwierać się go nie bierze, i
    #  Morfeusz daje obu formom ten sam lemat. Leksykon trzymany pod samym lematem
    #  dałby więc jednemu z tych dwóch zdań ramę drugiego, a widać to dopiero na
    #  parze: jedno przechodzi w każdą stronę, a drugie nie.
    otwarcie = verdict("Otwierają się drzwi.")
    assert otwarcie.readings == [{"Subject": "drzwi", "Verb": "Otwierają się"}]
    assert verdict("Otwierają drzwi.").status == "ambiguous"


def test_leksykon_nie_zabiera_czasownikowi_bezokolicznika():
    #  Walenty mówi i o bezokoliczniku, a przekład go nie bierze, bo cząstka się
    #  staje przy formie osobowej, należąc do bezokolicznika za nią: mieć się
    #  bezokolicznika w Walentym nie ma, a to zdanie stoi na nim. Nad Składnicą
    #  zawężenie o bezokolicznik kosztuje dwa zdania i nie kupuje ani jednej
    #  jednoznaczności, i to jest ten pomiar; docs/subset.md go trzyma.
    assert verdict("Zebranie ma się odbyć.").status == "valid"


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
    assert {czytanie.get("Predicative") for czytanie in found.readings} == {
        "bardzo duży",
        "duży",
    }
    assert {czytanie.get("Adverb") for czytanie in found.readings} == {None, "bardzo"}


def test_przysłówek_okolicznikowy_dostaje_rolę_a_nie_samo_wyprowadzenie():
    #  Pozycja dopisana bez roli daje `valid` bez słowa o tym, co olski w zdaniu
    #  przyjął, a rola jest tym, po co werdykt stoi (docs/roadmap.md).
    found = verdict("Program zapisuje ustawienia szybko.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Adverb"] == "szybko"


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
    assert {czytanie.get("Modifier") for czytanie in found.readings} == {
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
    assert found.readings[0]["Subject"] == "parser tego podzbioru"


def test_rzeczownik_dalej_bierze_dopełniacz_po_sobie():
    #  Druga połowa warunku: wyłączony jest jeden lemat, a nie produkcja, więc
    #  grupa imienna z dopełniaczem po głowie stoi tam, gdzie stała.
    found = verdict("Wejściem jest opis podzbioru.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Subject"] == "opis podzbioru"


def test_zaimek_rzeczowny_zostaje_wszędzie_indziej():
    #  Warunek stoi na jednej pozycji jednej produkcji, więc zaimek rzeczowny
    #  dalej jest tym, czym w polszczyźnie jest.
    assert verdict("To ma pomagać pisać dobrą polszczyznę.").status == "valid"


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
    assert found.readings == [{"Subject": "Ustawy", "Verb": "określają"}]


def test_pytanie_stawia_grupę_pytajną_w_podmiocie_i_w_dopełnieniu():
    #  Dwie role, bo tyle wypisuje `_ciała_z_wysuniętą_rolą`, i obie idą tą samą
    #  drogą co w zdaniu względnym. Werdykt nazywa grupę pytajną rolą, bo pytanie
    #  przyjęte bez niej nie mówiłoby, o co pyta.
    podmiot = verdict("Który aktor robi na tobie największe wrażenie?")
    assert podmiot.status == "valid", podmiot.explain()
    assert podmiot.readings[0][PYTAJNY] == "Który aktor"
    dopełnienie = verdict("Które zadania gmina wykonuje?")
    assert dopełnienie.status == "valid", dopełnienie.explain()
    assert dopełnienie.readings[0][PYTAJNY] == "Które zadania"


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
    #  `te [konstrukcje, które stoją]` obok `[te konstrukcje], które stoją`,
    #  a te dwa kształty są różne, więc liczą się jako dwa czytania.
    found = verdict("Istnieją te konstrukcje, które na niej stoją.")
    assert found.status == "valid", found.explain()


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
    #  Fraza bezokolicznikowa bierze okolicznik przez to samo `Complements`,
    #  którym bierze go forma osobowa nad nią, więc stoi wśród gospodarzy
    #  przyłączenia. Bez niej okolicznik wychodzi do zdania w obu czytaniach,
    #  oba streszczają się jednym napisem, a werdykt mówi samo `2 readings`.
    found = verdict("Syn usiłował wejść na ołtarz.")
    assert found.result.ile == 2, found.explain()
    (przyłączenie,) = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("usiłował", "wejść")


def test_streszczenie_nazywa_czasownik_zdania_a_nie_zdania_względnego():
    #  Usterka, którą to łapie: zejście do pierwszego węzła roli, gdziekolwiek on
    #  stoi. Zdanie względne stoi tu w podmiocie, czyli przed czasownikiem
    #  zdania, więc zejście bez granicy nazywa czasownikiem `rozstrzyga`, a
    #  `jest` nie pada wtedy w wierszu wcale.
    roles = verdict("Reguła, która rozstrzyga o zdaniu, jest tania.").readings[0]
    assert roles["Verb"] == "jest"
    assert "Modifier" not in roles


def test_streszczenie_nie_nazywa_roli_wziętej_ze_zdania_dopełnieniowego():
    #  Druga granica, i tu widać ją mocniej: zdanie nadrzędne dopełnienia nie ma
    #  wcale, więc `Object` wzięty ze zdania podrzędnego nazywa rolę, której to
    #  zdanie nie ma. Wiersz werdyktu łapie przy tym drugie podsumowanie: bez tej
    #  samej granicy ogłasza niezgodę o rolę, której lista czytań nie nazywa.
    #  Wieloznaczność zostaje po tej stronie granicy nazwana konstytuentem, w
    #  którym leży, i tym wierszem, a nie rolą tamtego zdania.
    found = verdict("Ustawa mówi, że organ gminy wydaje przepis.")
    assert found.result.ile == 2, found.explain()
    assert all("Object" not in reading for reading in found.readings)
    assert found.explain() == "2 readings; „organ gminy wydaje przepis” reads 2 ways"


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
    #  `aby` żąda zdania w trybie przypuszczającym, a gramatyka nie odróżnia go
    #  od czasu przeszłego, bo cząstki `by` nie bierze żadna produkcja. Wpuszczone
    #  na listę spójników okolicznikowych wyprowadzałoby zdanie, którego
    #  polszczyzna nie ma, przeciwko obietnicy podzbioru.
    found = verdict("Program zapisuje ustawienia, aby linter sprawdza dokumentację.")
    assert found.status == "rejected", found.explain()


def test_streszczenie_nazywa_okolicznik_zdaniowy_a_wnętrza_jego_nie_otwiera():
    #  Usterka, którą to łapie: zejście po role do wnętrza tego okolicznika.
    #  Zdanie podrzędne stoi tu przed zdaniem nadrzędnym, więc zejście bez
    #  granicy nazywa podmiotem `linter`, czyli podmiot tamtego zdania, a nie
    #  tego. Rola jest przy tym nazwana całym napisem, bo symbol stoi i wśród
    #  ról, i wśród zdań podrzędnych.
    roles = verdict("Ponieważ linter sprawdza dokumentację, program zapisuje ustawienia.")
    (streszczenie,) = roles.readings
    assert streszczenie["Subject"] == "program"
    assert streszczenie["AdverbialClause"] == "Ponieważ linter sprawdza dokumentację,"


def test_okolicznik_zdaniowy_dochodzi_do_obu_zdań_i_werdykt_to_nazywa():
    #  Okolicznik za zdaniem dopełnieniowym dochodzi do niego i do zdania nad
    #  nim, i są to dwa czytania, które polszczyzna nad tym zdaniem ma. Widać je
    #  po roli, bo streszczenie nazywa ją wtedy, gdy okolicznik stoi w zdaniu
    #  streszczanym, a milczy, gdy stoi w tamtym.
    found = verdict("Pomiar mówi, że linter działa, ponieważ tekst jest gotowy.")
    assert found.result.ile == 2, found.explain()
    assert found.result.różniące == ("AdverbialClause",)
    assert {OKOLICZNIKOWY in reading for reading in found.readings} == {False, True}


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
    found = verdict("Polszczyzna, której nikt nie napisał, jest podzbiorem.")
    assert found.status == "valid", found.explain()
    assert verdict("Polszczyzna, którą nikt nie napisał, jest podzbiorem.").status == "rejected"


# --------------------------------------------------------------------------- #
# Readings the dictionary offers and olski does not take
# --------------------------------------------------------------------------- #


def test_a_preposition_is_not_also_read_as_the_note_of_the_same_name():
    #  Morfeusz reads do as the preposition and as the musical note. The note
    #  inflects for nothing, so unification can never rule it out, and do Włoch
    #  would derive as a noun phrase as well as a prepositional one.
    #  docs/corpus.md counts how much of the corpus that reaches.
    found = verdict("Jedziemy do Włoch.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Modifier"] == "do Włoch → Jedziemy"


def test_an_uninflected_noun_stays_where_its_form_is_only_a_noun():
    #  The other half of the exclusion: jury inflects for nothing either, and
    #  nothing else reads it, so it is an ordinary Polish noun and stays.
    assert verdict("Jury ogłasza wyniki.").status == "valid"


def test_an_acronym_keeps_the_noun_reading_the_exclusion_would_take():
    #  PO inflects for nothing, exactly as the note does, and shares its letters
    #  with a preposition. In capitals the noun is what the form is, so this is
    #  where the exclusion has to stop.
    assert verdict("PO ogłasza wyniki.").status == "valid"


def test_excluding_a_reading_never_leaves_a_form_with_none():
    #  A segment with no readings at all is a form Morfeusz does not know, which
    #  is a different verdict and a wrong one here. What spares the segment is
    #  the function-word reading, so that one is always among the survivors.
    unfiltered = analyse("do")[0]
    assert {reading.tag.pos for reading in unfiltered.readings} == {"prep", "subst"}
    assert [reading.tag.pos for reading in admissible(unfiltered).readings] == ["prep"]


# --------------------------------------------------------------------------- #
# Notacja rejestru, czyli słowo, którego słownik nie ma
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "text, formy",
    [
        #  Ścieżkę Morfeusz rozbija na pięć krawędzi, bo ukośnik i kropka są dla
        #  niego interpunkcją, a czytelnik ma tam jedno słowo, którego rozbitego
        #  nie bierze żadna produkcja. Łącznik idzie z nią, bo stoi w jej środku.
        ("Zobacz docs/design-notes.md.", ["Zobacz", "docs/design-notes.md", "."]),
        #  Łącznik sam ścieżki nie robi, a złożenie przymiotnikowe Morfeusz zna po
        #  członach: sklejone w jedno wypadłoby ze słownika i z gramatyki.
        ("czarno-biały", ["czarno", "-", "biały"]),
        #  Skrót z kropką w środku ma człony jednoliterowe, więc wzorzec go mija.
        ("m.in.", ["m.in", "."]),
        #  Data spaja się kropkami tak samo jak ścieżka, a rzeczownikiem nie jest.
        ("2018.07.23", ["2018.07.23"]),
    ],
)
def test_notacja_jest_jednym_słowem_i_nic_poza_nią_nim_nie_jest(text, formy):
    assert [segment.form for segment in morphology(text)] == formy


def test_graf_kawałka_niejednoznacznego_zszywa_się_z_notacją_bez_przesunięcia():
    #  Sklejanie stawia grafy kolejnych kawałków jeden za drugim, więc pomyłka o
    #  jeden węzeł rozerwałaby zdanie w miejscu, którego nikt nie zobaczy w
    #  formach. Morfeusz dzieli ktoś na kto i ś obok formy całej, czyli daje temu
    #  kawałkowi graf, który się rozchodzi, i to on tę pomyłkę pokazuje.
    krawędzie = [(s.start, s.end, s.form) for s in morphology("Ktoś zna docs/subset.md.")]
    assert krawędzie == [
        (0, 1, "Kto"),
        (0, 2, "Ktoś"),
        (1, 2, "ś"),
        (2, 3, "zna"),
        (3, 4, "docs/subset.md"),
        (4, 5, "."),
    ]


def test_wykluczenie_słownikowe_nie_zdejmuje_czytaniu_notacji():
    #  Notacja niesie jedno czytanie, i to nieodmienne, czyli dokładnie to, co
    #  admissible odrzuca — broni jej przed tym drugi warunek, ten o wyrazie
    #  funkcyjnym obok. Bez niego notacja wychodziłaby stąd bez czytań, a to jest
    #  werdykt o formie, której Morfeusz nie zna, i tutaj byłby fałszywy.
    segment = morphology("docs/subset.md")[0]
    assert [reading.tag.raw for reading in segment.readings] == [
        "subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:n:ncol"
    ]


# --------------------------------------------------------------------------- #
# Splitting
# --------------------------------------------------------------------------- #


def test_tekst_dzieli_się_na_zdania_a_nie_na_każdej_kropce():
    #  Kropka w docs/linter.md granicą nie jest, a granica akapitu jest, choć
    #  kropki tam nie ma. Jedno i drugie ma olski/document.py i żadnego nie ma
    #  cięcie na każdej kropce, którym ten podział szedł.
    assert sentences("Co działa\n\nCały wywód prowadzi docs/linter.md.") == [
        "Co działa",
        "Cały wywód prowadzi docs/linter.md.",
    ]


def test_werdykt_niesie_zdanie_tak_jak_stoi_a_nie_graf_segmentacji():
    #  Morfeusz dzieli ktoś na kto i ś obok formy całej, więc jest to zdanie,
    #  które wypisywało się jako cztery słowa, choć stoją w nim trzy.
    assert verdict("Ktoś zapisał plik.").text == "Ktoś zapisał plik."


def test_fragment_bez_znaku_zamykajacego_nie_jest_zdaniem_odrzuconym():
    #  Nagłówek i pozycja listy dochodzą do olskiego jako akapity, a produkcja
    #  Sentence żąda na końcu kropki, więc odrzucone mierzyłyby ekstrakcję.
    assert verdict("Zapisywanie pliku").status == FRAGMENT
    assert verdict("Nowa program zapisuje ustawienia.").status == "rejected"


def test_every_sentence_of_a_text_is_checked():
    verdicts = check("Zapisz plik. Nowa program zapisuje ustawienia.")
    assert [found.status for found in verdicts] == ["valid", "rejected"]


def test_the_grammar_is_a_grammar_of_something():
    assert len(GRAMMAR) > 5
    assert GRAMMAR.undefined() == frozenset()
