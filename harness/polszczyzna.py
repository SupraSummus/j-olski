"""Ten sam podzbiór polszczyzny, powiedziany łukami zamiast produkcjami.

Porównanie ma sens tylko wtedy, gdy oba opisy mówią o tym samym, więc każda
deklaracja niżej wskazuje produkcję z ``olski/subset/``, którą oddaje, a
morfologia, cechy i unifikacja są w obu programach jedne i te same.

Gdzie liczba deklaracji rozjeżdża się z liczbą produkcji i co z tego wynika, mówi
`docs/design-notes.md`. Jest to wynik sondy, a nie jej opis, więc stoi tam, a nie
tutaj.
"""

from __future__ import annotations

from harness.wiezy import PO, PRZED, Gramatyka, Więz, Zgoda, Żąda
from olski.grammar import V, word
from olski.lematy import KOPULA
from olski.subset import AGREE, ZAIMEK_RZECZOWNY

#: Formy osobowe, które olski bierze: oznajmująca i rozkaźnik.
OSOBOWY = frozenset({"fin", "impt"})

#: Głowy, pod które idzie dopełnienie i bezokolicznik: forma osobowa i sam
#: bezokolicznik, bo ``ma pomagać pisać`` wiesza bezokolicznik pod bezokolicznikiem.
CZASOWNIK = frozenset({"fin", "impt", "inf"})

#: To, co wypełnia pozycję rzeczownikową: rzeczownik albo zaimek. Zaimek stoi
#: osobno wszędzie tam, gdzie osoba wchodzi do zgodności, bo tag rzeczownika osoby
#: nie niesie, a unifikacja cechy, której nie ma, nie sprawdza.
NOMINALNE = frozenset({"subst", "ppron3", "ppron12"})

#: Przymiotnik i imiesłów przymiotnikowy bierny, jak w symbolu ``człon_przymiotnikowy`` olskiego.
PRZYMIOTNIK = frozenset({"adj", "ppas"})

WIĘZY = (
    # Podmiot, czyli ``podmiot → grupa_imienna[nom]`` wraz ze zgodnością,
    # którą w olskim robią szyki zdania. Dwie deklaracje, bo trzecią osobę trzeba postawić na
    # czasowniku wprost: gdyby stała na rzeczowniku, unifikacja by ją pominęła i
    # czasownik pierwszej osoby wziąłby rzeczownik za podmiot.
    Więz(
        "podmiot",
        word(OSOBOWY, number=V("n"), person="ter"),
        word("subst", case="nom", number=V("n")),
    ),
    Więz(
        "podmiot",
        word(OSOBOWY, number=V("n"), person=V("p")),
        word({"ppron3", "ppron12"}, case="nom", number=V("n"), person=V("p")),
    ),
    # Dopełnienie, czyli ``dopełnienie → grupa_imienna[acc]``, w dwóch deklaracjach
    # zamiast jednej: za czasownikiem bez warunku, przed nim z tym, który uzasadnia
    # pole ``wymaga``.
    # Głową nie jest kopula, bo biernika nie bierze, i to jest tu cała walencja:
    # rama, którą olski wypuszcza z czasownika, wychodzi po tej stronie warunkiem
    # na lemat głowy łuku.
    Więz(
        "dopełnienie",
        word(CZASOWNIK, bez_lematu=KOPULA),
        word(NOMINALNE, case="acc"),
        strona=PO,
        zakazuje=("orzecznik", "orzecznik_narzędnikowy"),
    ),
    Więz(
        "dopełnienie",
        word(CZASOWNIK, bez_lematu=KOPULA),
        word(NOMINALNE, case="acc"),
        strona=PRZED,
        wymaga=("podmiot",),
        zakazuje=("orzecznik", "orzecznik_narzędnikowy"),
    ),
    # Orzecznik w narzędniku, którego nie bierze nic poza kopulą, i orzecznik
    # przymiotnikowy, który bierze każdy czasownik. Ograniczenie lematem jest to
    # samo, którym olski trzyma ramę kopuli.
    #
    # Dwie etykiety, a nie jedna, bo z podmiotem zgadza się orzecznik
    # przymiotnikowy, a narzędnikowy nie: w olskim ``orzecznik → grupa_imienna[inst]``
    # wypuszcza z siebie sam przypadek, więc liczby ani rodzaju nie ma tam czym
    # sprawdzić. Raport nazywa oba orzecznikiem, bo takie one dla czytelnika są.
    Więz(
        "orzecznik_narzędnikowy",
        word(OSOBOWY, lemma=KOPULA),
        word("subst", case="inst"),
        strona=PO,
        zakazuje=("orzecznik",),
    ),
    Więz(
        "orzecznik_narzędnikowy",
        word(OSOBOWY, lemma=KOPULA),
        word("subst", case="inst"),
        strona=PRZED,
        wymaga=("podmiot",),
        zakazuje=("orzecznik",),
    ),
    Więz(
        "orzecznik",
        word(OSOBOWY),
        word(PRZYMIOTNIK, case="nom"),
        strona=PO,
        zakazuje=("orzecznik_narzędnikowy",),
    ),
    Więz(
        "orzecznik",
        word(OSOBOWY),
        word(PRZYMIOTNIK, case="nom"),
        strona=PRZED,
        wymaga=("podmiot",),
        zakazuje=("orzecznik_narzędnikowy",),
    ),
    # Bezokolicznik jako to, co czasownik bierze, i modalne ``winien`` obok. Stoi
    # za swoją głową, bo bez tego łańcuch ``ma pomagać pisać`` zwiesza się dwoma
    # sposobami: raz tak, jak stoi w tekście, a raz z drugim bezokolicznikiem pod
    # trzecim.
    Więz("bezokolicznik", word(CZASOWNIK), word("inf"), strona=PO),
    Więz("bezokolicznik", word("winien"), word("inf"), strona=PO),
    # Zwrotne ``się`` przylega do swojego czasownika i stoi po nim.
    Więz("cząstka_zwrotna", word(OSOBOWY), word("part", lemma="się"), strona=PO, przyległy=True),
    # Grupa imienna: przymiotnik zgodny po obu stronach rzeczownika, dopełniacz za
    # nim. Zgodność jest tu tą samą trójką zmiennych, którą wymienia AGREE.
    Więz("przydawka", word("subst", **AGREE), word(PRZYMIOTNIK, **AGREE), jedyny=False),
    # Dopełniacz jest jeden na rzeczownik, tak jak jedno ``grupa_imienna[gen]`` w ciele
    # produkcji: bez tego ``tego podzbioru`` wisi u ``parser`` dwoma dopełniaczami
    # obok siebie i wychodzi z tego czytanie, którego olski nie ma. Głową nie jest
    # zaimek rzeczowny, i to jest ten sam warunek ujemny, który stoi w produkcji.
    Więz(
        "dopełniacz",
        word("subst", bez_lematu=ZAIMEK_RZECZOWNY),
        word("subst", case="gen"),
        strona=PO,
    ),
    # Okolicznik: przyimek dochodzi do czasownika, do rzeczownika i do
    # przymiotnika, czyli do tych trzech głów, pod którymi olski ma pozycje
    # na ``wyrażenie_przyimkowe``.
    Więz("wyrażenie_przyimkowe", word(CZASOWNIK), word("prep"), jedyny=False),
    Więz("wyrażenie_przyimkowe", word("subst"), word("prep"), strona=PO, jedyny=False),
    Więz("wyrażenie_przyimkowe", word(PRZYMIOTNIK), word("prep"), strona=PO, jedyny=False),
    # Przyimek rządzi przypadkiem swojej grupy, i rząd jest tu wspólną zmienną,
    # dokładnie jak w ``wyrażenie_przyimkowe → prep grupa_imienna[case]``.
    Więz("przyimek", word("prep", case=V("c")), word(NOMINALNE, case=V("c")), strona=PO),
    # Współrzędność na trzech poziomach, na których olski ją ma. Drugi członek
    # wisi pod pierwszym, więc zgodność członów jest parą słów, a spójnik wisi tam
    # samo. Oba łuki żądają siebie wzajemnie, bo bez tego dwa rzeczowniki obok
    # siebie są członami bez spójnika, a to jest już inna konstrukcja, której
    # olski nie ma: bez tego warunku ``Nowa program`` przechodzi.
    Więz(
        "człon",
        word("subst", case=V("c")),
        word("subst", case=V("c")),
        strona=PO,
        jedyny=False,
        wymaga=("spójnik_szeregu",),
    ),
    Więz(
        "człon",
        word(PRZYMIOTNIK, **AGREE),
        word(PRZYMIOTNIK, **AGREE),
        strona=PO,
        jedyny=False,
        wymaga=("spójnik_szeregu",),
    ),
    Więz(
        "człon",
        word(OSOBOWY),
        word(OSOBOWY),
        strona=PO,
        jedyny=False,
        wymaga=("spójnik_szeregu",),
    ),
    Więz(
        "spójnik_szeregu",
        word({"subst", "adj", "ppas", "fin", "impt"}),
        word("conj"),
        strona=PO,
        wymaga=("człon",),
    ),
)

ZGODY = (
    # Orzecznik przymiotnikowy zgadza się z podmiotem, a nie z czasownikiem.
    Zgoda("podmiot", "orzecznik", ("number", "gender")),
)

ŻĄDANIA = (
    # Przyimek bez swojej grupy imiennej okolicznikiem nie jest.
    Żąda(word("prep"), ("przyimek",)),
)

GRAMATYKA = Gramatyka(
    korzeń=word(OSOBOWY),
    więzy=WIĘZY,
    zgody=ZGODY,
    żądania=ŻĄDANIA,
    domknięcie=word("interp", lemma={".", "!", "?"}),
)
