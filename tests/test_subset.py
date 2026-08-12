"""What olski admits, and what it refuses.

The refusals matter more than the acceptances, and there are two kinds of them:
a sentence with no reading is not olski, and a sentence with more than one is not
olski either.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import EMPTY, Grammar, V, nt, unify, word
from olski.morph import analyse
from olski.parse import LeftRecursion, parse
from olski.subset import (
    FRAGMENT,
    GRAMMAR,
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


def test_a_left_recursive_grammar_is_reported_rather_than_looped_on():
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("A"), word("interp")])
    with pytest.raises(LeftRecursion):
        parse(grammar, morphology("plik."))


def test_a_grammar_referring_to_a_symbol_it_never_defines_is_refused():
    grammar = Grammar(start="A")
    grammar.rule("A", [nt("Nieznane")])
    with pytest.raises(ValueError, match="undefined symbols: Nieznane"):
        parse(grammar, morphology("plik."))


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
    #  A pronoun subject, and with it a person that is not the third.
    "Ja zapisuję plik.",
    #  Notacja rejestru w roli dopełnienia, czyli jedno zdanie README.
    "Zobacz docs/subset.md.",
    #  Zdanie, którego graf segmentacji się rozchodzi: Morfeusz dzieli Ktoś
    #  na Kto i ś obok formy całej, a ś nie ma ani jednego czytania, które
    #  bierze jakakolwiek produkcja.
    "Ktoś zna docs/subset.md.",
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
    assert {reading["Predicative"] for reading in found.readings} == {
        "wolni i równi",
        "wolni i równi pod względem swej godności i swych praw",
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
    assert roles["Modifier"] == "Pod względem smaku"


def test_object_first_order_is_polish_and_is_read_that_way():
    #  Free word order is real: here the plural verb forces the plural noun to
    #  be the subject, so the sentence is unambiguous despite the OVS order.
    roles = verdict("Program zapisują ustawienia.").readings[0]
    assert roles["Subject"] == "ustawienia"
    assert roles["Object"] == "Program"


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


def test_a_rejection_says_how_far_the_analysis_got():
    #  The copula, the coordination and the comma joining two clauses are all in
    #  the grammar. A comma standing in front of the conjunction is not, so the
    #  analysis gets past the comma and stops on ale, which is where it stands.
    result = verdict("Plany są niczym, ale planowanie jest wszystkim.").result
    assert result.rejected
    assert result.furthest == 4


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


def test_werdykt_nie_nazywa_ani_jednego_z_nierozstrzygniętych_przyłączeń():
    #  Przypięta jest tu usterka, a nie własność, i po to jest ten komentarz:
    #  drugie zdanie ma sześć nierozstrzygniętych przyłączeń i szesnaście razy
    #  więcej czytań niż pierwsze, a werdykt oddaje ten sam napis. Kiedy werdykt
    #  zacznie wskazywać same przyłączenia, ten test padnie, i wtedy razem z nim
    #  idzie sekcja docs/design-notes.md, która na tych dwóch napisach stoi.
    dwa = verdict("Program zapisuje ustawienia w pliku w katalogu.")
    sześć = verdict(
        "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci w firmie w kraju."
    )
    assert dwa.explain() == "4 readings, differing in Modifier, Object"
    assert sześć.explain() == "64+ readings, differing in Modifier, Object"


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
    assert {reading["Modifier"] for reading in found.readings} == {
        "wobec innych",
        "wobec innych w duchu",
        "wobec innych w duchu braterstwa",
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
    found = verdict("Program zapisuje w pliku w katalogu.")
    assert found.explain() == "2 readings, differing in Modifier"


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


@pytest.mark.parametrize(
    "text", ["Na to jest zbyt wielkim tchórzem.", "Inne wymagają ustalenia."]
)
def test_pozycja_orzecznika_żąda_ramy_sama_zamiast_dzielić_z_nią_zmienną(text):
    #  Trzy pozycje orzecznika wyglądają na jedną, w której orzecznik i czasownik
    #  dzielą zmienną walencyjną, a te dwa zdania ze Składnicy są ceną takiego
    #  zlania: oba wychodzą z niego przyjęte i oba przeczytane na opak, raz z
    #  podmiotem zbyt, a raz z podmiotem ustalenia. docs/subset.md trzyma pomiar.
    assert verdict(text).status == "rejected"


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
# Readings the dictionary offers and olski does not take
# --------------------------------------------------------------------------- #


def test_a_preposition_is_not_also_read_as_the_note_of_the_same_name():
    #  Morfeusz reads do as the preposition and as the musical note. The note
    #  inflects for nothing, so unification can never rule it out, and do Włoch
    #  would derive as a noun phrase as well as a prepositional one.
    #  docs/corpus.md counts how much of the corpus that reaches.
    found = verdict("Jedziemy do Włoch.")
    assert found.status == "valid", found.explain()
    assert found.readings[0]["Modifier"] == "do Włoch"


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
