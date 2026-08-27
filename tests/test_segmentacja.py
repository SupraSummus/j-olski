"""Co dochodzi do gramatyki z analizatora, czyli warstwa pod nią.

Segmentacja daje gramatyce graf krawędzi, a nie ciąg form,
i robi nad tym grafem dwie rzeczy naraz.
Zdejmuje czytania, których olski nie bierze —
`do` czytane jako nuta, forma przyimkowa zaimka postawiona bez przyimka —
i dokłada jedno tam, gdzie słownik słowa nie ma:
ścieżce, dacie, formie wersalikowej.
Zdjęte czytanie sprawdza się tu werdyktem o całym zdaniu,
bo widać je dopiero w produkcji, która je brała.

Osobno pyta ten plik o granicę pakietu:
warstwa ta jest poniżej gramatyki, więc jej import gramatyki nie buduje.
"""

import subprocess
import sys

import pytest

pytest.importorskip("morfeusz2")

from olski.morph import analyse
from olski.segmentacja import admissible, morphology, sentences, wersalik
from tests.test_werdykt import role, verdict


@pytest.mark.parametrize("moduł", ["olski.segmentacja", "olski.lematy"])
def test_import_warstwy_pod_gramatyką_nie_buduje_gramatyki(moduł):
    """Docstringi obu modułów obiecują to zdanie, a nie pilnowało go nic.

    Jeden import dopisany do tamtych modułów oddaje koszt gramatyki każdemu,
    kto pyta o samą segmentację, a ``olski/wieloznaczność.py`` jest takim pytającym.
    Zapłacono za to zdanie osobnym modułem na lematy dwóch warstw
    (``olski/lematy.py`` mówi, czym ten koszt jest),
    a wraca ono po cichu: suita przechodzi tak samo z takim importem i bez niego.

    Liczone jest to w osobnym procesie, tak samo jak granica pakietu składu
    (``tests/test_rozbiór.py``), bo w tym gramatykę zaimportowały testy stojące obok.
    """
    kod = f"import {moduł}, sys; print('olski.subset' in sys.modules)"
    przebieg = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True)
    assert przebieg.stdout.strip() == "False", przebieg.stderr


def test_tekst_dzieli_się_na_zdania_a_nie_na_każdej_kropce():
    #  Kropka w docs/linter.md granicą nie jest, a granica akapitu jest, choć
    #  kropki tam nie ma. Jedno i drugie ma olski/document.py i żadnego nie ma
    #  cięcie na każdej kropce, którym ten podział szedł.
    assert sentences("Co działa\n\nCały wywód prowadzi docs/linter.md.") == [
        "Co działa",
        "Cały wywód prowadzi docs/linter.md.",
    ]


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
    assert role(found)[0]["Modifier"] == "do Włoch → Jedziemy"


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
