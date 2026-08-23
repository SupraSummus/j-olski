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

from olski.grammar import EMPTY, Grammar, Głowa, Sym, V, Var, Word, bierze, nt, unify, word
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
    BEZOSOBOWY,
    CZĄSTKI,
    CZĄSTKOWY,
    DEKLARACJA,
    FRAGMENT,
    GRAMMAR,
    OKOLICZNIKOWY,
    ORZEKAJĄCY,
    PREDYKATYWY,
    PRZECINEK,
    PRZYSŁÓWKOWY,
    PRZYŁĄCZANY,
    PYTAJNY,
    SPÓJNIK_BEZ_PRZECINKA,
    SPÓJNIK_PRZECINKOWY,
    SPÓJNIKI_PRZECINKOWE,
    WALENCJA,
    WALENCJA_ZWROTNA,
    WTRĄCONY,
    admissible,
    check,
    morphology,
    na_czym_stanęło,
    sentences,
    wersalik,
    zatrzymania,
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
    cechy = czytanie.tag.cechy
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
    #  a żąda jej luka, której olski nie bierze.
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
            6,
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
    #  Tryb przypuszczający, czyli ten sam czas z cząstką `by` za sobą, w osobie
    #  trzeciej i w pierwszej.
    "Czytelnik nie odzyskałby ról.",
    "Napisałbym program.",
    #  Ten sam tryb pod spójnikiem, który cząstkę niesie sam, w obu miejscach
    #  okolicznika. Zdanie pod takim spójnikiem stoi w formie na -ł bez cząstki.
    "Program zapisuje ustawienia, żeby linter sprawdził polszczyznę.",
    "Gdyby linter sprawdził polszczyznę, program zapisuje ustawienia.",
    #  Fraza bezokolicznikowa pod tym samym spójnikiem, czyli to, czym ten rejestr
    #  wyraża cel najczęściej.
    "Program zapisuje ustawienia, aby sprawdzić polszczyznę.",
    "Aby sprawdzić polszczyznę, program zapisuje ustawienia.",
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
    #  projektu nazywa, ma czytania i licencję (`olski/projekt.txt`), więc
    #  odpowiedź pierwszą pokazuje dopiero forma spoza tego leksykonu.
    forma = verdict("Modele stawiają prozę wyżej od New Yorkera.")
    assert forma.nielicencjonowane == ("Yorkera",)
    assert "no production takes" in forma.explain()
    struktura = verdict("Nowa program zapisuje ustawienia.")
    assert struktura.nielicencjonowane == ()
    #  Zdanie to stoi w README jako przykład odrzucenia, więc jego werdykt stoi
    #  tam wypisany co do znaku. Czemu analiza staje na `ustawienia`, a nie na
    #  niezgodnej parze, mówi `na_czym_stanęło` w `olski/subset.py`.
    assert struktura.explain() == "no reading: the analysis stops at „ustawienia”"


def test_licencja_bierze_się_z_gramatyki_a_nie_z_listy_obok_niej():
    #  Gramatyka, która nie ma czasownika, przestaje licencjonować jego czytanie:
    #  gdyby licencja stała napisana obok, ta zmiana nie doszłaby do niej wcale.
    uboga = Grammar(start="NP")
    uboga.rule("NP", [word("subst")])
    czytanie = next(r for r in analyse("zapisuje")[0].readings if r.tag.pos == "fin")
    cechy = czytanie.tag.cechy
    assert not uboga.licencjonuje(czytanie.tag.pos, czytanie.lemma, cechy)
    assert GRAMMAR.licencjonuje(czytanie.tag.pos, czytanie.lemma, cechy)


def test_odrzucenie_nazywa_formę_na_której_analiza_stanęła():
    #  Polish puts a comma in front of ale and this sentence has none, so no level
    #  of coordination derives it and the analysis stops on the conjunction itself.
    #  The form is licensed all the same, by the position that has the comma, so
    #  the list of unlicensed forms is empty and the furthest point is what says
    #  where the sentence ran out.
    zdanie = "Plany są niczym ale planowanie jest wszystkim."
    assert parse(GRAMMAR, morphology(zdanie)).furthest == 3
    assert verdict(zdanie).explain() == "no reading: the analysis stops at „ale”"


def test_zdanie_którego_nic_nie_domyka_nie_nazywa_znaku_kończącego_jako_zatrzymania():
    #  Drugi człon nie ma czasownika, więc żadna analiza nie zamyka zdania, choć
    #  każdą jego formę bierze jakaś produkcja. Zatrzymanie pada wtedy na kropce,
    #  a werdykt nazywający kropkę kazałby autorowi poprawić interpunkcję.
    werdykt = verdict("Gramatyka jest tania, a nie droga.")
    assert werdykt.status == "rejected"
    assert werdykt.zatrzymanie is None
    assert werdykt.explain() == (
        "no reading: the analysis reaches the end and nothing closes the sentence"
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
    [roles] = verdict("Autor działa i zapisuje ustawienia.").readings
    assert roles == {"Subject": "Autor…", "Object": "…ustawienia", "Verb": "działa…"}


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


@pytest.mark.parametrize("symbol", ["Clause", "ClauseConjunct", "Predicate", "Verb"])
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
def test_symbol_współrzędny_stoi_nad_sobą_dokładnie_tam_gdzie_ma_znak_koordynacji(symbol):
    #  Kryterium, na którym stoją dwie rzeczy naraz: `_nawiasuj` w `olski/parse.py`
    #  poznaje ciąg współrzędny po tym, że symbol stoi nad sobą, i po tym samym
    #  poznaje go pomiar różnicowy, żeby wiedzieć, którą produkcję zdjąć.
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


@pytest.mark.parametrize("lemat", [":", ";", "—", "–"])
def test_znak_rozdzielający_bierze_jedna_produkcja_więc_nie_ma_z_czym_konkurować(lemat):
    #  Na tej jedynce stoi zdanie, że ani dwukropek, ani średnik nie odbiera
    #  jednoznaczności ani jednemu zdaniu: znak wchodzący w jedno ciało albo
    #  wyprowadza zdanie tą produkcją, albo nie wyprowadza go wcale. Drugie ciało
    #  z tym znakiem czyni z tego zera liczbę do zmierzenia i ten test jest tym,
    #  co o tym powie.
    biorące = [
        produkcja
        for produkcja in GRAMMAR.productions
        if any(
            isinstance(część, Word) and bierze(część, "interp", lemat, {}, EMPTY) is not None
            for część in produkcja.body
        )
    ]
    assert len(biorące) == 1, biorące


def test_cudzysłów_przepuszcza_przypadek_grupy_którą_obejmuje():
    #  Usterka, którą to łapie: przypadek wypisany wartością zamiast zmiennej.
    #  Polszczyzna odmienia to, co cudzysłów obejmuje, wedle roli grupy, więc
    #  wartość wpisana w produkcję przyjmuje jeden z tych dwóch napisów i odrzuca
    #  drugi, a oba są zdaniami tej dokumentacji.
    mianownik = verdict("Same „Zasady techniki prawodawczej” są rozporządzeniem.")
    assert mianownik.status == "valid", mianownik.explain()
    orzecznik = verdict("Ustawa jest przepisem „Zasad techniki prawodawczej”.")
    assert orzecznik.status == "valid", orzecznik.explain()


def test_wtrącenie_nie_oddaje_zdaniu_ról_ze_swojego_wnętrza():
    #  Wtrącenie jest rolą całym napisem, więc zejście po role zatrzymuje się na
    #  nim (`Deklaracja.podrzędne`). Bez tego wyrażenie przyimkowe z jego wnętrza
    #  wychodzi rolą przyłączaną zdania, którego ono nie określa, i werdykt mówi o
    #  zdaniu nieprawdę, zamiast odrzucić.
    werdykt = verdict("Cena jest niska (koszt w pliku).")
    assert werdykt.status == "valid", werdykt.explain()
    [czytanie] = werdykt.readings
    assert czytanie[WTRĄCONY] == "( koszt w pliku )", czytanie
    assert PRZYŁĄCZANY not in czytanie, czytanie


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
    #  Produkcja stoi na poziomie zdania, a `Clause` żadnego z tych znaków nie ma,
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
    found = verdict("Autor zapisuje w pliku w katalogu.")
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


def test_okolicznik_staje_po_czasowniku_i_daje_zdaniu_czytanie_z_podmiotem():
    """Pozycja okolicznika po córce czasownikowej, wzięta z obu stron naraz.

    Zdania są dwa, bo brak tej pozycji płacił w dwóch walutach: pierwsze było
    odrzucone, a drugie wychodziło jednym czytaniem, w którym `program
    ustawienia` jest dopełnieniem, czyli werdyktem `valid` mówiącym o zdaniu
    nieprawdę.
    """
    trwa = verdict("Trwa w tej sprawie dochodzenie.")
    assert trwa.status == "valid", trwa.explain()
    assert trwa.readings[0]["Subject"] == "dochodzenie"
    zapisuje = verdict("Zapisuje w pliku program ustawienia.")
    assert ("program", "ustawienia") in {
        (czytanie.get("Subject"), czytanie.get("Object")) for czytanie in zapisuje.readings
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
    assert {czytanie.get("Adverb") for czytanie in found.readings} == {
        "bardzo szybko",
        "bardzo",
    }


def test_przysłówek_okolicznikowy_dostaje_rolę_a_nie_samo_wyprowadzenie():
    #  Pozycja dopisana bez roli daje `valid` bez słowa o tym, co olski w zdaniu
    #  przyjął, a rola jest tym, po co werdykt stoi (docs/roadmap.md).
    found = verdict("Program zapisuje ustawienia szybko.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Adverb"] == "szybko"


def test_cząstka_dostaje_rolę_osobną_od_przysłówka_w_obu_pozycjach():
    #  Rola jest osobna, bo cząstka przysłówkiem nie jest: `Adverb: już` mówiłoby o
    #  zdaniu, że ma okolicznik przysłówkowy, którego ono nie ma. Pozycje przy zdaniu
    #  są dwie i pisze je jedna pętla razem z przysłówkiem, więc zdania są dwa:
    #  rozejście się tych dwóch kompletów widać dopiero na tym, którego jedna z nich
    #  nie bierze. Zdanie drugie cząstkę wpuszcza także do podmiotu, więc pytamy o
    #  rolę wśród czytań, a nie o pierwsze z nich.
    okolicznik = verdict("Program już zapisuje ustawienia.")
    assert okolicznik.readings[0][CZĄSTKOWY] == "już", okolicznik.explain()
    assert PRZYSŁÓWKOWY not in okolicznik.readings[0], okolicznik.explain()
    czoło = verdict("Już program zapisuje ustawienia.")
    assert "Już" in {czytanie.get(CZĄSTKOWY) for czytanie in czoło.readings}, czoło.explain()


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
        (czytanie.get("Subject"), czytanie.get(CZĄSTKOWY)) for czytanie in found.readings
    } == {("Nawet ptaki", None), ("ptaki", "Nawet")}, found.explain()


def test_cząstka_w_grupie_imiennej_przepuszcza_osobę_zaimka():
    #  Przymiotnik i zaimek dzierżawczy ogłaszają trzecią osobę, a cząstka ją
    #  przepuszcza, bo staje i przed zaimkiem. Z `ter` w tym ciele grupa nie zgodziłaby
    #  się z czasownikiem osobą i to czytanie by nie wyszło.
    found = verdict("Nawet ja zapisuję ustawienia.")
    assert "Nawet ja" in {czytanie.get("Subject") for czytanie in found.readings}, found.explain()


@pytest.mark.parametrize("lemat", CZĄSTKI.split("|"))
def test_cząstka_z_listy_nie_ma_czytania_branego_gdzie_indziej(lemat):
    #  Kryterium na wejście do tej listy, postawione lemat po lemacie: cząstka,
    #  której inne czytanie gramatyka bierze, daje jednemu napisowi dwa
    #  wyprowadzenia. `tylko` jest u Morfeusza także spójnikiem, więc dopisane tu
    #  kosztowałoby czytanie każdego zdania, w którym stoi, i tego ten test pilnuje
    #  po stronie listy, a nie po stronie zdania.
    czytania = [(r.tag.pos, r.lemma, r.tag.cechy) for r in analyse(lemat)[0].readings]
    brane = [c for c in czytania if GRAMMAR.licencjonuje(*c)]
    assert brane, (lemat, czytania)
    assert {pos for pos, _, _ in brane} == {"part"}, (lemat, brane)


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


def test_zaimek_bez_czytania_przymiotnikowego_też_nie_bierze_dopełniacza():
    #  Lista zawężona do paradygmatu ten zostawia to zdanie wieloznacznym: nikt ma
    #  u Morfeusza czytanie jedno i rzeczownikowe, więc czytania, w którym nikt nas
    #  jest grupą imienną, nie zdejmuje ani anotator, ani wykluczenie ze słownika.
    found = verdict("Wtedy nikt nas nie zauważy.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Subject"] == "nikt"


def test_zaimek_rzeczowny_nie_unosi_wysuniętego_zaimka_względnego():
    #  Drugie miejsce, w którym przydawką dopełniaczową jest zaimek: grupa
    #  wysuwana przed zdanie względne. Warunek postawiony w samej grupie imiennej
    #  zostawia to zdanie wieloznacznym, bo której nikt wychodzi taką grupą.
    found = verdict("Polszczyzna, której nikt nie napisał, jest podzbiorem.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Subject"] == "Polszczyzna, której nikt nie napisał,"


def test_rzeczownik_dalej_bierze_dopełniacz_po_sobie():
    #  Druga połowa warunku: wyłączona jest lista lematów, a nie produkcja, więc
    #  grupa imienna z dopełniaczem po głowie stoi tam, gdzie stała.
    found = verdict("Wejściem jest opis podzbioru.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Subject"] == "opis podzbioru"


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
    assert mnogi.readings[0]["Subject"] == "Jego skutki"
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
    assert found.readings == [{"Subject": "Ustawy", "Verb": "określają"}]


def test_pytanie_stawia_grupę_pytajną_w_podmiocie_i_w_dopełnieniu():
    #  Dwie role, bo tyle deklaruje `_wysunięta_rola`, i obie idą tą samą
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
    dopełnienie = verdict("Ustawa, której przepisy minister ogłasza, jest tania.")
    assert dopełnienie.status == "valid", dopełnienie.explain()
    przeczenie = verdict("Ustawa, której przepisów minister nie ogłasza, jest tania.")
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
    #  zagląda i tam ta usterka jest niewidoczna (:data:`olski.subset.ORZEKAJĄCY`).
    found = verdict("Mowa o zadaniach.")
    assert found.status == "valid", found.explain()
    [reading] = found.readings
    assert reading[ORZEKAJĄCY] == "Mowa", found.explain()


def test_kopuła_opuszczona_żąda_jednej_formy_i_żąda_lematu():
    #  Dwa warunki naraz i każdy jest osobną usterką do zrobienia. Bez lematu
    #  zdaniem wychodzi każda grupa imienna w mianowniku, więc `o których cisza`
    #  przechodzi razem ze zwrotem tego rejestru, a przecinek koordynacji czyta
    #  wtedy wyliczenie jako ciąg zdań
    #  (docs/subset.md#kopuła-opuszczona-jest-wpisem-na-lemat-a-nie-pozycją-ogólną).
    #  Bez liczby przechodzi `o których mowy`, i mianownik sam tego nie łapie:
    #  Morfeusz zna `mowy` i jako dopełniacz pojedynczy, i jako mianownik mnogi,
    #  więc warunek na sam przypadek bierze tę formę drugim czytaniem.
    forma = verdict("Przepisy, o których mowy, obowiązują.")
    assert forma.status == "rejected", forma.explain()
    lemat = verdict("Przepisy, o których cisza, obowiązują.")
    assert lemat.status == "rejected", lemat.explain()


def test_predykatyw_orzeka_bez_podmiotu_i_nie_czyni_go_z_biernika():
    #  Usterka, którą to łapie: predykatyw wpuszczony jako `Predicate`, po którym
    #  `Programy trzeba czytać.` wychodzi zdaniem o podmiocie `Programy`
    #  (docs/subset.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika).
    found = verdict("Trzeba czytać dokumenty.")
    assert found.readings[0][BEZOSOBOWY] == "Trzeba", found.explain()
    wysunięte = verdict("Programy trzeba czytać.")
    assert wysunięte.status == "rejected", wysunięte.explain()


@pytest.mark.parametrize("lemat", PREDYKATYWY.split("|"))
def test_każdy_predykatyw_z_listy_ma_czytanie_którego_gramatyka_sięga(lemat):
    #  Usterka, którą to łapie: lemat wpisany na listę, którego Morfeusz pod `pred`
    #  nie ma. `trudno` i `łatwo` są u niego przysłówkami, więc wpisane tutaj byłyby
    #  wierszem martwym, a martwego wiersza nie widać po żadnym zdaniu.
    czytania = [(r.tag.pos, r.lemma, r.tag.cechy) for r in analyse(lemat)[0].readings]
    brane = [c for c in czytania if c[0] == "pred" and GRAMMAR.licencjonuje(*c)]
    assert brane, (lemat, czytania)


def test_czasownik_nieosobowy_orzeka_bez_podmiotu_i_nie_czyni_go_z_biernika():
    #  Usterka, którą to łapie: forma `imps` wpuszczona pod symbolem `Verb`.
    #  Zgodności ta forma nie niesie żadnej, a cechy, której konstytuent nie
    #  niesie, unifikacja nie sprawdza, więc pod tamtym symbolem `program`
    #  wychodzi podmiotem, choć jest tam biernikiem
    #  (docs/subset.md#czasownik-nieosobowy-orzeka-bez-podmiotu-i-rządzi-ramą-swojego-lematu).
    found = verdict("Zgłoszono program.")
    assert found.readings[0][BEZOSOBOWY] == "Zgłoszono", found.explain()
    assert "Subject" not in found.readings[0], found.explain()


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
    assert found.readings[0]["Object"] == "usterki", found.explain()
    biernik = verdict("Nie zgłoszono usterkę.")
    assert biernik.status == "rejected", biernik.explain()


def test_rzeczownik_orzekający_nie_jest_orzecznikiem_pod_kopulą():
    #  Rola stoi obok `Predicative`, a nie jest nią, a to zdanie jest tym, co
    #  tamto wyjście przyjmuje: orzecznik przed kopulą ramy nie żąda, więc rzeczownik
    #  wpuszczony do `Predicative` stanąłby tam i przyjął zdanie, w którym olski
    #  czyta orzecznik w mianowniku (:data:`olski.subset.ORZEKAJĄCY`).
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
        ("Reguła, która rozstrzyga, jest tania.", "Subject", "która"),
        ("Polszczyzna, którą napisał autor, jest tania.", "Object", "którą"),
        ("Ustawa, której autorzy piszą, jest tania.", "Subject", "której autorzy"),
        ("Ustawa, której przepisy minister ogłasza, jest tania.", "Object", "której przepisy"),
        ("Który aktor robi na tobie największe wrażenie?", "Subject", "Który aktor"),
        ("Które zadania gmina wykonuje?", "Object", "Które zadania"),
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

    Usterka, którą to łapie, jest ceną samej etykiety: `Subject` wpisany do ciała
    czoła bez cechy rozdzielającej wpuszcza tam `Subject → NP`, więc `reguła, ta
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
    #  wynosi rolę tak samo, ale stoi pod `ClauseConjunct`, a streszczenie bierze
    #  z gałęzi to najwyższe. Bez czoła pytania w `Deklaracja.składowe` pytanie o
    #  jednym zdaniu składowym dostaje więc wielokropek mówiący, że streszczenie
    #  milczy o drugim.
    found = verdict("W którym roku ustawa weszła?")
    assert found.status == "valid", found.explain()
    assert found.readings[0][PYTAJNY] == "którym roku"


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
    found = verdict("Istnieją ci ludzie, którzy na niej stoją.")
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
    (streszczenie,) = roles.readings
    assert streszczenie["Subject"] == "program"
    assert streszczenie["AdverbialClause"] == "Ponieważ linter sprawdza dokumentację,"


def test_okolicznik_zdaniowy_dochodzi_do_obu_zdań_i_werdykt_to_nazywa():
    #  Okolicznik za zdaniem dopełnieniowym dochodzi do niego i do zdania nad
    #  nim, i są to dwa czytania, które polszczyzna nad tym zdaniem ma. Widać je
    #  po roli, bo streszczenie nazywa ją wtedy, gdy okolicznik stoi w zdaniu
    #  streszczanym, a milczy, gdy stoi w tamtym.
    found = verdict("Pomiar mówi, że autor pisze, ponieważ tekst jest gotowy.")
    assert found.result.ile == 2, found.explain()
    assert found.result.różniące == ("AdverbialClause",)
    assert {OKOLICZNIKOWY in reading for reading in found.readings} == {False, True}


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
# Forma przyimkowa zaimka, czyli wykluczenie pytające o sąsiada
# --------------------------------------------------------------------------- #


def test_forma_przyimkowa_bez_przyimka_zostaje_bez_ani_jednego_czytania():
    #  `niego` czytania nieprzyimkowego nie ma, więc bez przyimka to wykluczenie
    #  zabiera mu wszystkie i tym różni się od `admissible`, które krawędzi nie
    #  opróżnia nigdy. Werdykt nazywa wtedy formę, a nie strukturę, i tego nie
    #  wolno naprawić odmową opróżniania: grupa imienna bierze zaimek w każdej
    #  swojej pozycji, więc zdanie wychodziłoby znów przyjęte.
    werdykt = verdict("Cena niego rośnie.")
    assert werdykt.status == "rejected"
    assert werdykt.nielicencjonowane == ("niego",), werdykt.explain()


def test_wykluczenie_przyimkowe_kupuje_jednoznaczność_zdaniu_z_przeczeniem():
    #  `nie` jest u Morfeusza biernikiem `on`, więc bez tego wykluczenia staje
    #  dopełnieniem w zdaniu, które przeczy, i zdanie wychodzi dwoma czytaniami,
    #  gdzie polszczyzna ma jedno. Ta klasa jest tym, za co wykluczenie weszło.
    assert verdict("Zagłębie nie płaci.").status == "valid"


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Pod przyimkiem ta forma jest polszczyzną, więc warunek pytający o samą
        #  formę, bez sąsiada, zabierałby ją i tutaj.
        "Bez niego cena rośnie.",
        #  `nim` niesie `praep` i `npraep` naraz, bo polszczyzna stawia je i po
        #  przyimku, i bez niego, więc warunek na samą obecność `praep`
        #  zabierałby tę formę wszędzie.
        "Program jest nim.",
    ],
)
def test_wykluczenie_przyimkowe_zostawia_formę_której_polszczyzna_tam_używa(zdanie):
    assert verdict(zdanie).status == "valid"


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


def test_forma_wersalikowa_której_słownik_nie_ma_jest_rzeczownikiem_nieodmiennym():
    #  Druga połowa tej samej myśli co notacja: `README` nie niesie ani kropki,
    #  ani ukośnika, więc wzorzec notacji go nie widzi, a Morfeusz oddaje `ign`,
    #  którego nie bierze ani jedna produkcja.
    found = verdict("README mówi o podzbiorze.")
    assert found.readings, found.explain()


def test_wersalik_nie_dokłada_czytania_formie_którą_słownik_czyta():
    #  Usterka, którą to łapie: warunek postawiony na samym piśmie formy. `NIE`
    #  słownik czyta jako cząstkę przeczącą, a czytanie nieodmienne postawione na
    #  jej miejscu odbiera zdaniu przeczenie.
    segment = analyse("NIE")[0]
    assert wersalik(segment) is segment


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


# --------------------------------------------------------------------------- #
# Zatrzymania, czyli miejsca, na których staje analiza
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("zdanie", "oczekiwane"),
    [
        #  Werdykt nazywa jedno miejsce, bo jedno jest końcem przedrostka, który
        #  się analizuje, a zdanie o kilkunastu wyrazach ma ich kilka i pierwsze
        #  zasłania resztę.
        ("Dokument nazywa role, w jakich ktoś czyta, a dla każdej: pytanie.", ("czyta", "a", ":")),
        ("Zapisz plik konfiguracyjny.", ()),
    ],
)
def test_zatrzymania_nazywają_każde_miejsce_a_nie_samo_pierwsze(zdanie, oczekiwane):
    assert zatrzymania(morphology(zdanie)) == oczekiwane


def test_analiza_wznawia_się_za_formą_zatrzymania_a_nie_na_niej():
    #  Usterka, którą to łapie: przebieg wznowiony na formie zatrzymania. Formy,
    #  której nie wzięła żadna analiza częściowa, nie weźmie też analiza zaczęta
    #  od niej, więc taki przebieg nazywałby ją bez końca.
    assert zatrzymania(morphology("Parser jest tani, i gramatyka jest tania.")) == ("i",)
