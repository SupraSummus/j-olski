"""Te własności warstwy rozstrzygającej, na których stoi jej prawo do istnienia.

Warstwa jest zalążkiem i większość tego, co mówi, mówi tabelą przeliczaną z banku
drzew, której nikt tu nie pilnuje. Trzy rzeczy są inne, bo bez nich zalążek jest
nie tyle niedokończony, co szkodliwy: że milczy, kiedy nie ma na czym stanąć, że
wskazanie przychodzi z liczbami, i że werdykt zostaje nietknięty.

Czwarta jest o kolejności świadków, bo na niej stoi obietnica z docstringa
``olski/rozstrzyganie.py``: dowód o tym tekście bije dowód o cudzym korpusie,
a nie odwrotnie.

Świadek kontekstowy ma tu własne, bo jego dowodem jest sąsiedztwo, a sąsiedztwo
da się źle przeczytać na kilka sposobów naraz: wziąć zdanie zza granicy akapitu,
wziąć zdanie stojące dalej, wziąć napis zamiast lematu, wziąć za gospodarza ogon
łańcucha dopełniaczowego zamiast jego głowy, albo zejść lematem imiesłowu z
odsłownikiem. Dwa ostatnie kończyły się nad korpusem audytowym wskazaniem, więc
milczenie po nich jest tu asercją równie ważną jak wskazanie.

Świadek ramowy ma tu własne, bo jego kryterium jest połową i połowa ta jest
wyceniona: wskazuje po stronie rzeczownika, a żądanie czasownika odbiera
wskazanie, zamiast wskazywać czasownik. Jedno i drugie da się zepsuć tak, że
wydruk wygląda dalej rozsądnie — świadek zaczyna wskazywać czasownik albo
przestaje milczeć na żądaniu obustronnym — a widać to dopiero w liczbach.

Świadka każdy test buduje sam, z licznika albo z ramy wypisanej na miejscu,
zamiast czytać ``olski/skłonności.txt`` czy ``olski/leksykon.txt``.
Pliki te są generowane, więc test na nich oparty pilnowałby banku drzew
albo Walentego, a nie warstwy, i milkłby razem z nimi. Ostatni test bierze
świadków domyślnych, bo sprawdza samo polecenie, i sprawdza wtedy zdanie, którego
tabela wypisać nie umie: powód świadka kontekstowego cytuje akapit.
"""

import pytest

pytest.importorskip("morfeusz2")

from dataclasses import replace

import olski.check
from olski.parse import Przyłączenie
from olski.rozstrzyganie import (
    PUSTE,
    Powtórzenie,
    Rama,
    Rozstrzygnięcie,
    Skłonność,
    Sąsiedztwo,
    domyślni,
    rozstrzygnij,
    sąsiedztwa,
)
from olski.subset import check

#: Przyłączenie, jakie werdykt wydaje nad ``Daj przepis na faworki.``
FAWORKI = Przyłączenie(modyfikator="na faworki", gospodarze=("Daj", "przepis"))

#: Licznik, przy którym świadek odpowiada: cztery wystąpienia, wszystkie w jedną stronę.
JEDNOZNACZNY = {("na", "noun", "przepis"): (4, 4)}


@pytest.mark.parametrize(
    ("licznik", "dlaczego"),
    [
        ({}, "bez tabeli, czyli po świeżej instalacji"),
        ({("na", "noun", "przepis"): (1, 1)}, "poniżej progu wsparcia"),
        ({("na", "noun", "przepis"): (5, 10)}, "gdy bank drzew przyłącza i tak, i tak"),
    ],
    ids=["bez tabeli", "poniżej wsparcia", "bez przewagi"],
)
def test_świadek_milczy_zamiast_zgadywać(licznik: dict, dlaczego: str):
    """Milczenie jest odpowiedzią domyślną, więc każdy jego powód działa osobno."""
    assert rozstrzygnij([FAWORKI], [Skłonność(licznik=licznik)]) == [FAWORKI], dlaczego


def test_wskazanie_przychodzi_z_liczbami_które_je_wydały():
    """Wskazanie bez powodu nie da się sprawdzić bez zaglądania do tabeli."""
    (odpowiedź,) = rozstrzygnij([FAWORKI], [Skłonność(licznik=JEDNOZNACZNY)])
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == "przepis"
    assert "4 z 4" in odpowiedź.powód


def test_odpowiedź_niesie_imię_świadka_który_ją_wydał():
    """Podpisuje ją warstwa, więc świadek nie ma jak podpisać się cudzym imieniem."""
    (odpowiedź,) = rozstrzygnij([FAWORKI], [Skłonność(licznik=JEDNOZNACZNY, nazwa="inny")])
    assert odpowiedź.świadek == "inny"


def test_pierwszy_świadek_z_odpowiedzią_wygrywa_z_dalszymi():
    """Kolejność jest kolejnością rodzaju dowodu, więc musi być kolejnością, a nie zbiorem.

    Świadek stojący pierwszy jest tu wypisany na miejscu, a nie wzięty z
    ``domyślni``, bo test pyta o samą kolejność: świadek prawdziwy odpowiadałby
    tylko na te przyłączenia, na które ma czym odpowiedzieć.
    """

    class Zawsze:
        nazwa = "zawsze"

        def __call__(self, przyłączenie, sąsiedztwo):
            return Rozstrzygnięcie(przyłączenie.modyfikator, "Daj", "bo tak")

    (odpowiedź,) = rozstrzygnij([FAWORKI], [Zawsze(), Skłonność(licznik=JEDNOZNACZNY)])
    assert (odpowiedź.świadek, odpowiedź.gospodarz) == ("zawsze", "Daj")


def test_warstwa_nie_rusza_werdyktu():
    """Zdanie rozstrzygnięte przez warstwę zostaje dla olskiego wieloznaczne.

    To jest cała różnica między tą warstwą a rankingiem wstawionym w werdykt,
    i jest to różnica, którą ``docs/disambiguation.md`` wywodzi z pomiaru.
    """
    (werdykt,) = check("Daj przepis na faworki.")
    przed = werdykt.status, werdykt.result.ile, werdykt.explain()
    odpowiedzi = rozstrzygnij(werdykt.result.przyłączenia, [Skłonność(licznik=JEDNOZNACZNY)])
    assert any(isinstance(o, Rozstrzygnięcie) for o in odpowiedzi), "świadek nic nie powiedział"
    assert (werdykt.status, werdykt.result.ile, werdykt.explain()) == przed
    assert werdykt.status == "ambiguous"


#: Przyłączenie, jakie werdykt wydaje nad ``Operator zgłosił awarię w systemie.``
#: Zdanie to czyta się po polsku dwojako, a dlaczego akurat takie, a nie
#: przykładowe z ``z`` i narzędnikiem, mówi ``docs/disambiguation.md``.
AWARIA = Przyłączenie(modyfikator="w systemie", gospodarze=("zgłosił", "awarię"))


@pytest.mark.parametrize(
    ("zdanie", "gospodarz"),
    [
        ("Wystąpiła awaria w systemie.", "awarię"),
        #  Ta sama droga wskazuje czasownik, bo świadek pyta, co stało przed
        #  frazą, a nie czy jest to rzeczownik.
        ("Zgłosiliśmy w systemie usterki.", "zgłosił"),
    ],
    ids=["gospodarz rzeczownikowy", "gospodarz czasownikowy"],
)
def test_powtórzona_fraza_wskazuje_tego_gospodarza_przy_którym_już_stała(zdanie, gospodarz):
    """Cały dowód tego świadka: autor postawił tę frazę przy tym gospodarzu wyżej."""
    (odpowiedź,) = rozstrzygnij([AWARIA], [Powtórzenie()], Sąsiedztwo((zdanie,)))
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == gospodarz
    assert zdanie in odpowiedź.powód


def test_fraza_dopasowuje_się_lematem_a_nie_napisem():
    """``w systemach`` i ``w systemie`` są tą samą frazą o tej samej rzeczy."""
    sąsiedztwo = Sąsiedztwo(("Wystąpiły awarie w systemach.",))
    przyłączenie = Przyłączenie(modyfikator="w systemie", gospodarze=("zgłosił", "awarie"))
    (odpowiedź,) = rozstrzygnij([przyłączenie], [Powtórzenie()], sąsiedztwo)
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == "awarie"


#: Sąsiedztwo z łańcuchem dopełniaczowym przed frazą, wzorowane na zdaniu korpusu
#: audytowego, na którym ten świadek raz się pomylił (``docs/disambiguation.md``).
#: Głową grupy jest ``wymiany``, a sąsiadem bezpośrednim frazy ``danych``.
ŁAŃCUCH = Sąsiedztwo(("Opisano sposób wymiany danych z systemami zewnętrznymi.",))


def test_fraza_wskazuje_głowę_łańcucha_dopełniaczowego_a_nie_jego_ogon():
    """Gospodarz stoi przed frazą, a nie zawsze tuż przed nią.

    Świadek pytający o sąsiada bezpośredniego wskazuje w tym zdaniu ``danych``,
    czyli ogon grupy, do której fraza dochodzi całą jej głową.
    """
    przyłączenie = Przyłączenie(modyfikator="z systemem RIT", gospodarze=("Wpływa", "wymiany"))
    (odpowiedź,) = rozstrzygnij([przyłączenie], [Powtórzenie()], ŁAŃCUCH)
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == "wymiany"


def test_łańcuch_z_dwoma_gospodarzami_kończy_się_milczeniem():
    """Dowód wskazujący dwie strony naraz nie wskazuje żadnej, i tu jest nim łańcuch.

    Jest to ten sam warunek, którym świadek milczy nad frazą powtórzoną przy obu
    gospodarzach, tyle że wypadek bierze się z grupy imiennej, a nie z dwóch
    miejsc tekstu: sąsiedztwo powtarza tu sporne przyłączenie, a nie rozstrzyga je.
    """
    przyłączenie = Przyłączenie(modyfikator="z systemem RIT", gospodarze=("wymiany", "danych"))
    assert rozstrzygnij([przyłączenie], [Powtórzenie()], ŁAŃCUCH) == [przyłączenie]


def test_łańcuch_zamyka_się_na_słowie_bez_czytania_imiennego():
    """Grupa imienna kończy się na spójniku, więc kandydaci kończą się tam samo.

    ``nadawanie`` stoi w tym zdaniu przed frazą i gospodarzem też jest, a mimo to
    dowodu nie wydaje: między nim a frazą stoi ``i``, czyli granica grupy. Bez
    tego warunku dowód wskazywałby obu gospodarzy naraz i świadek by zamilkł,
    tracąc wskazanie, które nad korpusem audytowym trafia.
    """
    sąsiedztwo = Sąsiedztwo(("Nadawanie i funkcjonowanie uprawnień do przeglądania trwa.",))
    przyłączenie = Przyłączenie(
        modyfikator="do przeglądania", gospodarze=("nadawaniu", "uprawnień")
    )
    (odpowiedź,) = rozstrzygnij([przyłączenie], [Powtórzenie()], sąsiedztwo)
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == "uprawnień"


#: Przyłączenie, którego fraza niesie odsłownik ``żądań``. Morfeusz sprowadza do
#: czasownika i jego, i imiesłów ``żądającym``, więc dopasowanie idące lematem
#: wszystkich czytań bierze te dwa słowa za jedno.
ŻĄDANIA = Przyłączenie(
    modyfikator="o sposobie przetwarzania żądań", gospodarze=("zawiera", "informacje")
)


def test_odsłownik_jest_rzeczownikiem_więc_dopasowanie_frazy_go_bierze():
    """Zawężenie do czytań imiennych ma zostawić odsłownik, bo jest rzeczownikiem."""
    sąsiedztwo = Sąsiedztwo(("Przekazujemy informacje o żądaniach.",))
    (odpowiedź,) = rozstrzygnij([ŻĄDANIA], [Powtórzenie()], sąsiedztwo)
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert odpowiedź.gospodarz == "informacje"


def test_imiesłów_przymiotnikowy_nie_jest_tą_samą_frazą_co_odsłownik():
    """Zdanie o żądającym dowodzi czegoś o kimś, a nie o żądaniu.

    Bez warunku na część mowy w tagu świadek wskazuje tu gospodarza po dowodzie
    mówiącym o czym innym, a wskazanie samo nie różni się wtedy niczym od
    trafnego: nad korpusem audytowym raz tak wskazał (``docs/disambiguation.md``).
    """
    sąsiedztwo = Sąsiedztwo(("Przekazujemy informacje o żądającym.",))
    assert rozstrzygnij([ŻĄDANIA], [Powtórzenie()], sąsiedztwo) == [ŻĄDANIA]


def test_kopula_dowodem_nie_jest_bo_okolicznik_przyłącza_się_do_niej_wszędzie():
    """Powtórzenie przy ``być`` jest prawdziwe i nie mówi, dokąd fraza doszła.

    Oba zdania mają tu za orzeczenie kopulę, a fraza dochodzi w obu do rzeczy.
    Bez tego warunku świadek wskazuje ``jest`` i nad korpusem audytowym tak
    właśnie wskazał, raz na osiem odpowiedzi (``docs/disambiguation.md``).
    """
    sąsiedztwo = Sąsiedztwo(("Wymaga się, aby opisy tworzone były w 3 osobie.",))
    przyłączenie = Przyłączenie(modyfikator="w 1 osobie", gospodarze=("jest", "tworzenie"))
    assert rozstrzygnij([przyłączenie], [Powtórzenie()], sąsiedztwo) == [przyłączenie]


def test_powód_wybiera_lemat_kolejnością_a_nie_z_worka():
    """Powód ma być ten sam w każdym przebiegu, a zbiór lematów kolejności nie ma.

    ``danych`` pasuje tu czterema lematami naraz — ``dana``, ``dane``, ``dany``
    i ``dać`` — więc bez ustalonej kolejności ten wydruk zmienia się z każdym
    uruchomieniem, bo mieszanie napisów jest losowane przy starcie.
    """
    sąsiedztwo = Sąsiedztwo(("Opisano sposób wymiany danych z systemami zewnętrznymi.",))
    przyłączenie = Przyłączenie(modyfikator="z systemem RIT", gospodarze=("Wpływa", "danych"))
    (odpowiedź,) = rozstrzygnij([przyłączenie], [Powtórzenie()], sąsiedztwo)
    assert "stało już przy „dana”" in odpowiedź.powód


@pytest.mark.parametrize(
    ("sąsiedztwo", "dlaczego"),
    [
        (PUSTE, "zdanie postawione samo, czyli olski-check -c"),
        (Sąsiedztwo(("Mamy nowy system.",)), "rzecz wprowadzona, ale nie przy gospodarzu"),
        (
            Sąsiedztwo(("Zgłosił w systemie awarię w systemie.",)),
            "stała przy obu gospodarzach",
        ),
    ],
    ids=["bez sąsiedztwa", "bez powtórzenia frazy", "przy obu gospodarzach"],
)
def test_świadek_kontekstowy_milczy_zamiast_zgadywać(sąsiedztwo: Sąsiedztwo, dlaczego: str):
    """Milczenie jest odpowiedzią domyślną także tutaj, a powodów ma trzy.

    Środkowy jest tym, którego łatwo nie zauważyć: rzecz raz wymieniona nie
    przestaje opisywać rzeczownika, więc samo jej wprowadzenie dowodem nie jest.
    """
    assert rozstrzygnij([AWARIA], [Powtórzenie()], sąsiedztwo) == [AWARIA], dlaczego


def test_sąsiedztwem_są_zdania_wcześniejsze_i_tylko_z_tego_akapitu():
    """Akapit jest granicą, a czytelnik idzie do przodu, więc wstecz i nie dalej."""
    tekst = "Pierwsze zdanie. Drugie zdanie.\n\nTrzecie zdanie."
    assert [s.zdania for s in sąsiedztwa(tekst)] == [
        (),
        ("Pierwsze zdanie.",),
        (),
    ]


# --------------------------------------------------------------------------- #
# Świadek ramowy
# --------------------------------------------------------------------------- #

#: Przyłączenie, jakie werdykt wydaje nad ``Program zapisuje informacje o błędach.``
#: Rama ``informacja`` żąda tu ``o``, a rama ``zapisywać`` nie żąda go, czyli jest
#: to ta klasa, na której świadek ramowy odpowiada.
BŁĘDY = Przyłączenie(modyfikator="o błędach", gospodarze=("zapisuje", "informacje"))


def rama(żądania: dict[tuple[str, str], set[str]]) -> Rama:
    """Świadek ramowy z ramą wypisaną na miejscu, po lemacie i stronie wyboru.

    ``olski/leksykon.txt`` jest generowany, więc test na nim oparty pilnowałby
    Walentego, a nie świadka, i milkłby razem z nim — tak samo jak przy tabeli
    skłonności wyżej.
    """
    return Rama(leksykon=lambda lemat, gdzie: frozenset(żądania.get((lemat, gdzie), ())))


def test_rama_wskazuje_rzeczownika_którego_schemat_żąda_tego_przyimka():
    """Wskazanie przychodzi z wierszem leksykonu, bo bez niego nie da się go sprawdzić."""
    (odpowiedź,) = rozstrzygnij([BŁĘDY], [rama({("informacja", "noun"): {"o"}})])
    assert isinstance(odpowiedź, Rozstrzygnięcie)
    assert (odpowiedź.świadek, odpowiedź.gospodarz) == ("rama", "informacje")
    assert "„o”" in odpowiedź.powód and "„informacja”" in odpowiedź.powód


def test_żądanie_samego_czasownika_nie_wskazuje_go_choć_świadek_je_widzi():
    """Połowa kryterium, której świadek nie bierze, i to jest połowa wyceniona.

    Rama czasownika trafia nad bankiem drzew tyle, ile rzut monetą nad wyborem
    dwóch stron, więc wskazania z niej nie ma; ``docs/disambiguation.md`` liczy,
    ile ta odmowa oddaje.
    """
    świadek = rama({("zapisywać", "clause"): {"o"}})
    assert rozstrzygnij([BŁĘDY], [świadek]) == [BŁĘDY]


def test_żądanie_po_obu_stronach_kończy_się_milczeniem():
    """Weto: schematu nie łamie wtedy żadne czytanie, więc nie ma czego rozstrzygać."""
    świadek = rama({("informacja", "noun"): {"o"}, ("zapisywać", "clause"): {"o"}})
    assert rozstrzygnij([BŁĘDY], [świadek]) == [BŁĘDY]


def test_wariant_bez_weta_odpowiada_tam_gdzie_weto_milczy():
    """Wariant, którym ``--oceń`` wycenia weto, ma naprawdę mierzyć co innego.

    Pole zignorowane dałoby w tym wydruku dwa wiersze identyczne i nic by tego
    nie zgłosiło.
    """
    żądania = {("informacja", "noun"): {"o"}, ("zapisywać", "clause"): {"o"}}
    bez_weta = replace(rama(żądania), weto=False)
    (odpowiedź,) = rozstrzygnij([BŁĘDY], [bez_weta])
    assert odpowiedź.gospodarz == "informacje"


def test_dwaj_gospodarze_imienni_żądający_kończą_się_milczeniem():
    """Dowód wskazujący dwie strony naraz nie wskazuje żadnej, tak jak przy powtórzeniu."""
    przyłączenie = Przyłączenie(
        modyfikator="o błędach", gospodarze=("zapisuje", "informacje", "awarię")
    )
    świadek = rama({("informacja", "noun"): {"o"}, ("awaria", "noun"): {"o"}})
    assert rozstrzygnij([przyłączenie], [świadek]) == [przyłączenie]


def test_przyimek_dopasowuje_się_lematem_a_nie_napisem():
    """``z`` i ``ze`` są jednym słowem, a Walenty wypisuje w schemacie lemat."""
    przyłączenie = Przyłączenie(modyfikator="ze systemem", gospodarze=("zapisuje", "wymiany"))
    (odpowiedź,) = rozstrzygnij([przyłączenie], [rama({("wymiana", "noun"): {"z"}})])
    assert odpowiedź.gospodarz == "wymiany"


def test_powtórzenie_bije_skłonność_przeciwnego_zdania():
    """Dowód o tym tekście bije dowód o cudzym korpusie, więc kolejność jest ta.

    Tabela wskazuje tu czasownik, a akapit rzeczownik, i o to w tej parze chodzi:
    świadek dopisany po ``Skłonność`` nie odezwałby się nigdy tam, gdzie tabela
    ma parę policzoną.
    """
    tabela = Skłonność(licznik={("w", "clause", "zgłosić"): (4, 4)})
    sąsiedztwo = Sąsiedztwo(("Wystąpiła awaria w systemie.",))
    (odpowiedź,) = rozstrzygnij([AWARIA], [Powtórzenie(), tabela], sąsiedztwo)
    assert (odpowiedź.świadek, odpowiedź.gospodarz) == ("powtórzenie", "awarię")


def test_kolejność_wypuszczana_jest_tą_samą_którą_sprawdza_test_wyżej():
    """Tamten test podaje świadków ręką, więc przestawienie ``domyślni`` mija go.

    Przestawić jest przy tym czym: świadek statystyczny odpowiada nad bankiem
    drzew o rząd wielkości częściej od kontekstowego, więc pomiar zasięgu mówi,
    żeby postawić go pierwszego. Kolejności tej nie broni żadna trafność, tylko
    hipoteza z ``docs/disambiguation.md``, i dlatego broni jej test.
    Świadek ramowy stoi z tego samego powodu w środku: jego dowód jest o
    polszczyźnie, więc bije częstość nad cudzym korpusem i przegrywa z akapitem,
    który autor napisał.
    """
    assert [type(świadek) for świadek in domyślni()] == [Powtórzenie, Rama, Skłonność]


def test_polecenie_daje_świadkowi_sąsiedztwo_tego_zdania(capsys):
    """Sąsiedztwo liczy się nad tekstem, a wchodzi do świadka po zdaniu.

    Testy wyżej wołają warstwę wprost, więc żaden z nich nie zauważyłby
    pomyłki o jedno zdanie ani sąsiedztwa pustego podanego wszędzie: obie
    powstają dopiero tam, gdzie polecenie idzie po dokumencie.
    """
    olski.check.main(
        [
            "--rozstrzygaj",
            "-c",
            "Wystąpiła awaria w systemie. Operator zgłosił awarię w systemie.",
        ]
    )
    wypisane = capsys.readouterr().out
    assert '? „w systemie” → „awarię”: „w systemie” stało już przy „awaria”' in wypisane
    assert wypisane.count("stało już przy") == 1, "pierwsze zdanie nie ma przed sobą niczego"
