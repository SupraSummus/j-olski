"""Co formalizm gramatyki sprawdza: unifikację na zabawce, a niżej całą deklarację.

Zgodność liczy unifikacja, więc pyta się o nią tutaj,
a nie przez zdanie, które jej użyło.
Zabawka odpowiada za to, czego nad prawdziwą gramatyką nie widać:
lewą rekursję, cykl i ciało puste ma tablica Earleya,
a olski żadnego z nich nie wyprowadza.
Sprawdzenia z ``olski/grammar.py`` stoją niżej dwa razy —
raz nad gramatyką napisaną w teście, raz nad :data:`olski.subset.GRAMMAR` —
bo osobno łatwo o obie pomyłki: sprawdzenie, które nie łapie,
i gramatyka, która pod nie nie podpada.

Co gramatyka wpuszcza, a co odrzuca, pyta ``tests/test_subset.py``;
co z lasu wychodzi nad zdaniem wieloznacznym, ``tests/test_las.py``.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import EMPTY, Grammar, Głowa, V, bierze, nt, unify, word
from olski.morph import VALUES, analyse
from olski.parse import Cykl, parse
from olski.segmentacja import morphology
from olski.subset import GRAMMAR


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
    wartości = word("adv", degree={"pos", "com", "sup"})
    obecność = word("adv", niesie="degree")
    assert (
        bierze(wartości, czytanie.tag.pos, czytanie.lemma, segment.lematy, cechy, EMPTY)
        is not None
    )
    wzięty = (
        bierze(obecność, czytanie.tag.pos, czytanie.lemma, segment.lematy, cechy, EMPTY)
        is not None
    )
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
    assert grammar.licencjonuje(
        "adv", "bardzo", frozenset({"bardzo"}), {"degree": frozenset({"pos"})}
    )
    assert not grammar.licencjonuje("adv", "tu", frozenset({"tu"}), {})


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

def test_a_grammar_referring_to_a_symbol_it_never_defines_is_refused():
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("Nieznane")])
    with pytest.raises(ValueError, match="undefined symbols: Nieznane"):
        parse(grammar, morphology("plik."))


def test_symbol_zdefiniowany_i_nieosiągalny_jest_zgłaszany():
    #  Tyle zostaje po literówce w głowie produkcji.
    grammar = Grammar(start="A")
    grammar.rule("A", [word("subst")])
    grammar.rule("Bd", [word("adj")])
    assert grammar.nieosiągalne() == frozenset({"Bd"})


def test_więz_na_cechę_której_symbol_nie_wypuszcza_jest_zgłaszany():
    #  Tyle zostaje po literówce w nazwie cechy: zgodność, która nie zawęża niczego.
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("B", nubmer=V("n"))])
    grammar.rule("B", [word("subst", number=V("n"))], number=V("n"))
    assert grammar.więzy_niesprawdzane() == frozenset({("B", "nubmer")})


def test_cecha_żądana_od_głowy_wychodzi_z_konstytuenta_bez_wypisywania():
    #  Tyle zostaje po wierszu pominiętym w wypisywaniu: cechy nieobecnej
    #  unifikacja nie sprawdza, więc konstytuent milczący o liczbie przechodził
    #  pod każdy więz na nią. Wypisane wygrywa, bo produkcja wypuszczająca co
    #  innego niż jej głowa mówi to wprost.
    grammar = Grammar(start="A")
    z_głowy = grammar.rule("A", [Głowa(nt("B", number=V("n"))), word("interp")])
    wypisane = grammar.rule("A", [Głowa(nt("B", number=V("n")))], number="pl")
    assert dict(z_głowy.features) == {"number": V("n")}
    assert dict(wypisane.features) == {"number": frozenset({"pl"})}


def test_cecha_wypisana_wśród_niewypuszczanych_z_głowy_nie_wychodzi():
    #  Zdanie składowe nie niesie liczby swojego czasownika, bo nad zdaniem nie
    #  ma z czym jej zgadzać. Wyjątek jest wypisany raz na symbol i na cechę
    #  (:data:`olski.subset.NIE_WYPUSZCZANE`).
    grammar = Grammar(start="A", nie_wypuszczane={"A": ("number",)})
    produkcja = grammar.rule("A", [Głowa(nt("B", number=V("n"), gender=V("g")))])
    assert dict(produkcja.features) == {"gender": V("g")}


def test_wpis_niewypuszczanej_cechy_bez_żądania_jest_zgłaszany():
    #  Tyle zostaje po produkcji zdjętej albo przemianowanej: wyjątek, który
    #  zatrzymuje cechę, o którą już nikt nie pyta.
    grammar = Grammar(start="A", nie_wypuszczane={"A": ("number", "gender")})
    grammar.rule("A", [word("subst", number=V("n"))])
    assert grammar.nie_wypuszczane_bez_żądania() == frozenset({("A", "gender")})


def test_cecha_wypuszczana_zmienną_której_nic_nie_wiąże_jest_zgłaszana():
    #  Tyle zostaje po literówce w nazwie zmiennej: deklaracja, która milczy,
    #  bo zmiennej nie wiąże żaden więz na córce.
    grammar = Grammar(start="A")
    grammar.rule("A", [word("subst", number=V("n"))], number=V("nn"))
    assert grammar.wypuszczane_bez_wiązania() == frozenset({("A", "number")})


def test_ciało_o_kilku_częściach_bez_głowy_nie_powstaje():
    #  Produkcja dopisana bez znacznika nazwałaby gospodarza przyłączenia pierwszą
    #  córką, cokolwiek nią jest, a werdykt wskazywałby wtedy nie to słowo i nie
    #  mówiłby o tym niczego. Odmowa pada na wierszu, na którym produkcja stoi.
    grammar = Grammar(start="A")
    with pytest.raises(ValueError, match="która jest głową"):
        grammar.rule("A", [word("subst"), word("interp")])


def test_the_grammar_is_a_grammar_of_something():
    assert len(GRAMMAR) > 5
    assert GRAMMAR.undefined() == frozenset()


def test_każdy_symbol_gramatyki_jest_osiągalny_od_startu():
    assert GRAMMAR.nieosiągalne() == frozenset()


def test_każdy_więz_gramatyki_pyta_o_cechę_wypuszczaną():
    assert GRAMMAR.więzy_niesprawdzane() == frozenset()


def test_każda_cecha_wypuszczana_przez_gramatykę_ma_co_wiązać_jej_zmienną():
    assert GRAMMAR.wypuszczane_bez_wiązania() == frozenset()


def test_każdy_wpis_wśród_niewypuszczanych_zatrzymuje_jakąś_cechę():
    assert GRAMMAR.nie_wypuszczane_bez_żądania() == frozenset()


def test_każdy_więz_na_terminalu_pyta_o_cechę_którą_morfologia_zna():
    """Literówka w nazwie cechy formy przepuszcza każdą formę i nie rusza wydruku.

    Inwentarz podaje tu wołający, bo formalizm gramatyki morfologii nie zna,
    a więzów na terminalach jest w tej gramatyce kilkaset.
    """
    assert GRAMMAR.więzy_terminali_niesprawdzane(set(VALUES.values())) == frozenset()

