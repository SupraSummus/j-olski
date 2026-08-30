"""Deklaracja podzbioru: co się w olskim wyprowadza, wypisane produkcjami.

Wykluczenia są dwojakie, bo produkcja rozstrzyga o zdaniu, a nie o formie.
Produkcje mówią, jakie zdanie się wyprowadza,
a czytanie odbiera formie warstwa morfologiczna (``olski/segmentacja.py``),
zanim produkcja to czytanie zobaczy.
Co gramatyka orzeka o jednym zdaniu, mówi ``olski/werdykt.py``.

Gramatyka buduje się przy imporcie (:data:`GRAMMAR`),
więc kto pyta o sam lemat, sięga po ``olski/lematy.py``.

Podział na moduły jest tu decyzją i idzie za tym, co dany moduł deklaruje.
``olski.subset.słowa`` trzyma słownictwo, którym produkcje są pisane:
zbiory lematów i terminale, czyli to, co gramatyka bierze od morfologii.
``olski.subset.rama`` trzyma walencję i formy czasownika, które z niej wychodzą.
``olski.subset.deklaracja`` trzyma to, co stoi obok produkcji, a nie w nich:
nazwy ról, rodziny czoła i listy, którymi werdykt schodzi po lesie.
Produkcje same stoją w czterech modułach po gospodarzu —
``wypowiedzenie``, ``zdanie``, ``podrzędne`` i ``grupa`` —
a :func:`build` niżej jest jedynym miejscem, które je składa,
bo kolejność ich wywołań rozstrzyga o kolejności czytań.
Podkreślenie w nazwie znaczy tu prywatne dla pakietu, a nie dla modułu:
poza niego wychodzą same nazwy wyliczone w ``__all__``.
"""

from __future__ import annotations

from olski.grammar import Grammar, V, nt
from olski.precedencja import Rozwinięcie
from olski.subset.deklaracja import (
    CZĄSTKA_ZDANIA,
    DEKLARACJA,
    GRUPA_PYTAJNA,
    MIJANE,
    NAZWY_SZKOLNE,
    NIE_WYPUSZCZANE,
    OKOLICZNIK_NARZĘDNIKOWY,
    OKOLICZNIK_PRZYSŁÓWKOWY,
    OKOLICZNIK_ZDANIOWY,
    ORZECZENIE_BEZOSOBOWE,
    ORZECZENIE_RZECZOWNIKOWE,
    ORZECZNIK_ŁĄCZNIKA,
    RODZINY,
    WTRĄCENIE,
    WYRAŻENIE_PRZYIMKOWE,
)
from olski.subset.grupa import (
    _grupa_imienna,
    _grupa_przymiotnikowa,
    _okoliczniki_leksykalne,
    _przydawka,
)
from olski.subset.podrzędne import _rodziny_czoła, _zdania_podrzędne
from olski.subset.rama import RAMA_BEZ_BIERNIKA, WALENCJA, WALENCJA_ZWROTNA
from olski.subset.słowa import (
    AGREE,
    BEZ_CZOŁA,
    BEZ_ROZDZIELNEJ,
    CZĄSTKI,
    PREDYKATYWY,
    PRZECINEK,
    PRZYSŁÓWEK,
    PRZYSŁÓWEK_STOPNIA,
    SPÓJNIK_BEZ_PRZECINKA,
    SPÓJNIK_PRZECINKOWY,
    SPÓJNIK_PYTAJNY,
    SPÓJNIKI_OKOLICZNIKOWE,
    SPÓJNIKI_PRZECINKOWE,
    SPÓJNIKI_SKORELOWANE,
    SPÓJNIKOWE,
    ZAIMEK_RZECZOWNY,
)
from olski.subset.wypowiedzenie import _interpunkcja_wypowiedzenia, _koordynacja_zdań
from olski.subset.zdanie import (
    _dopełnienie,
    _dostawki_zdania,
    _grupa_orzeczenia,
    _lista_okoliczników,
    _orzeczenie,
    _orzecznik,
    _podmiot,
    _szyki_zdania_składowego,
    _wypełnienia,
)


def build() -> Grammar:
    """Gramatyka olskiego, złożona z sekcji rozpisanych po modułach, po jednej na gospodarza.

    Kolejność wywołań jest kolejnością wpisywania produkcji, a tę widać po
    czytaniach: rozstrzyga o nich koszt, a przy równym koszcie właśnie ona
    (``wyprowadzenia`` w ``olski/parse.py``). Sekcja przestawiona zmienia więc
    czytania, a nie sam układ pakietu, i dlatego jej moduł tego nie rusza:
    kolejność stoi tutaj, w jednym miejscu, i dowodzi jej odcisk samej gramatyki
    (``harness/odcisk.py``).
    """
    grammar = Grammar(start="wypowiedzenie", nie_wypuszczane=NIE_WYPUSZCZANE)

    # Symbole, które jedna sekcja wpisuje, a czyta je druga, wraz z kanałem
    # cech, na którym stoją; nazwę czytaną w jednej sekcji deklaruje ta sekcja
    # u siebie. Zmienna cechy jest zakresu produkcji, więc dwie produkcje biorące
    # ten sam obiekt mówią dalej każda o swojej zgodności.
    #
    # Cechę, której żąda się tu od głowy, konstytuent niesie w górę sam
    # (``olski/grammar.py``).
    orzecznikowy = nt("przymiotnik_orzecznikowy", **AGREE)
    przydawka = nt("przydawka", **AGREE)
    przydawka_nierozdzielna = nt("przydawka", rozdzielna=BEZ_ROZDZIELNEJ, **AGREE)
    cechy_zdania = {"number": V("n"), "gender": V("g"), "person": V("p"), "tryb": V("t")}
    okoliczniki = nt("okoliczniki")

    # Walencja jest wspólną zmienną, tak jak zgodność: czasownik wypuszcza z
    # siebie swoją ramę, dopełnienie mówi, którą pozycję ramy zajmuje, a
    # unifikacja przecina jedno z drugim. Czasownik, przy którym nic nie stoi,
    # ramy nie ogłasza nikomu i stoi tu bez niej.
    #
    # Negacja jedzie tą samą drogą i rządzi tym samym: przypadkiem grupy, którą
    # czasownik bierze. Czasownik ogłasza, czy przeczy, dopełnienie mówi, przy
    # jakim przeczeniu stoi. Zgodnością to nie jest — rządzenie nie jest ani
    # symetryczne, ani lokalne — więc dlaczego kanał cech ją mimo to bierze,
    # wywodzi docs/design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne.
    cechy_ramy = {**cechy_zdania, "valency": V("w"), "negacja": V("z"), "druga": V("d")}
    czasownik_ramy = nt("orzeczenie", **cechy_ramy)
    # Ten sam czasownik wraz z cechą, którą stawia mu wypełnienie
    # (:data:`BEZ_KOPULI`). Węzeł jest osobny, bo cechy tej żąda jedno ciało
    # z kilku, w których tamten stoi, a wypisana w nim wszędzie byłaby zmienną,
    # której w pozostałych nikt nie wiąże.
    czasownik_kopuli = nt("orzeczenie", **cechy_ramy, kopula=V("k"))
    dopełnienie = nt("dopełnienie", valency=V("w"), negacja=V("z"), czoło=BEZ_CZOŁA)
    orzecznik_ramy = nt(
        "orzecznik", number=V("n"), gender=V("g"), valency=V("w"), czoło=BEZ_CZOŁA
    )

    # Zdanie deklaruje córki, a kolejność, w jakiej one stoją, deklaruje osobno
    # warunek precedencji nad nimi; rozwinięcie składa jedno z drugim przed
    # rozbiorem (:mod:`olski.precedencja`). Tablica Earleya dostaje przez to
    # ciała wypisane, bo rozwinięcie kończy się przed nią, a rodzina mnożąca się
    # przez szyk i przez miejsca na okolicznik ma sześć deklaracji na kilkadziesiąt
    # ciał.
    #
    # Miejsce na okolicznik wylicza to samo rozwinięcie i przez to nie ma go jak
    # zapomnieć w jednym z ciał: przyłączenie wyrażenia przyimkowego olski oddaje
    # czytelnikowi, więc każde miejsce, w którym grupa imienna takie wyrażenie
    # bierze, musi umieć oddać je też zdaniu. Pozycji brakującej nie widać po
    # zdaniu odrzuconym, tylko po przyjętym: wychodzi ono jednym czytaniem, bo
    # drugie nie miało gdzie się wyprowadzić. docs/subset.md trzyma wywód i cenę.
    #
    # Osoba bierze się z podmiotu, a nie stoi na trzeciej, i to jest to, co
    # wpuszcza zaimek pierwszej i drugiej osoby. Grupa imienna z rzeczownikiem w
    # głowie mówi person=ter sama, więc rozkaźnik dalej takiej nie weźmie.
    zdanie = Rozwinięcie(grammar, okolicznik=okoliczniki, własny_okolicznik=("grupa_orzeczenia",))

    _przydawka(grammar)
    _interpunkcja_wypowiedzenia(grammar)
    _koordynacja_zdań(grammar)
    _szyki_zdania_składowego(
        grammar, zdanie, cechy_zdania, czasownik_ramy, dopełnienie, okoliczniki
    )
    _dostawki_zdania(grammar)
    _podmiot(grammar)
    _dopełnienie(grammar)
    _grupa_orzeczenia(grammar, cechy_zdania, czasownik_ramy, czasownik_kopuli, dopełnienie)
    _zdania_podrzędne(grammar)
    _wypełnienia(grammar, okoliczniki, dopełnienie, orzecznik_ramy)
    _lista_okoliczników(grammar, okoliczniki)
    _orzecznik(grammar)
    _orzeczenie(grammar, okoliczniki)
    _grupa_imienna(grammar, przydawka, przydawka_nierozdzielna)
    _grupa_przymiotnikowa(grammar, orzecznikowy)
    _okoliczniki_leksykalne(grammar)
    _rodziny_czoła(grammar, zdanie)

    return grammar


GRAMMAR = build()

__all__ = [
    "AGREE",
    "BEZ_CZOŁA",
    "CZĄSTKA_ZDANIA",
    "CZĄSTKI",
    "DEKLARACJA",
    "GRAMMAR",
    "GRUPA_PYTAJNA",
    "MIJANE",
    "OKOLICZNIK_NARZĘDNIKOWY",
    "OKOLICZNIK_PRZYSŁÓWKOWY",
    "OKOLICZNIK_ZDANIOWY",
    "ORZECZENIE_BEZOSOBOWE",
    "ORZECZENIE_RZECZOWNIKOWE",
    "NAZWY_SZKOLNE",
    "ORZECZNIK_ŁĄCZNIKA",
    "PREDYKATYWY",
    "PRZECINEK",
    "PRZYSŁÓWEK",
    "PRZYSŁÓWEK_STOPNIA",
    "RAMA_BEZ_BIERNIKA",
    "RODZINY",
    "SPÓJNIKI_OKOLICZNIKOWE",
    "SPÓJNIKI_PRZECINKOWE",
    "SPÓJNIKI_SKORELOWANE",
    "SPÓJNIKOWE",
    "SPÓJNIK_BEZ_PRZECINKA",
    "SPÓJNIK_PRZECINKOWY",
    "SPÓJNIK_PYTAJNY",
    "WALENCJA",
    "WALENCJA_ZWROTNA",
    "WTRĄCENIE",
    "WYRAŻENIE_PRZYIMKOWE",
    "ZAIMEK_RZECZOWNY",
    "build",
]
