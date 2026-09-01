"""Wypowiedzenie: znak kończący zdanie oraz ciąg zdań współrzędnych pod nim.

Symbol startowy gramatyki jest tutaj, a pod nim zdanie wraz ze znakiem kończącym,
bo znak ten należy do wypowiedzenia, a nie do zdania,
które i bez niego się wyprowadza (``olski/werdykt.py`` orzeka o niedomknięciu).
"""

from __future__ import annotations

from olski.grammar import Grammar, Głowa, V, nt
from olski.subset.deklaracja import DOPOWIEDZENIE
from olski.subset.słowa import (
    BEZ_CIĄGU,
    CIĄG,
    DWUKROPEK,
    KONIEC_ZDANIA,
    MYŚLNIK,
    PRZECINEK,
    SPÓJNIK_BEZ_PRZECINKA,
    SPÓJNIK_NA_CZELE,
    SPÓJNIK_PRZECINKOWY,
    SPÓJNIK_SKORELOWANY,
    ŚREDNIK,
)


def _interpunkcja_wypowiedzenia(grammar: Grammar) -> None:
    """Znaki, którymi ten rejestr spina zdania, wraz z dopowiedzeniem za dwukropkiem."""
    grammar.rule("wypowiedzenie", [Głowa(nt("zdanie")), KONIEC_ZDANIA])

    # Spójnik na czele całego zdania: `I nikt tego nie zauważył.`, `Zatem
    # milczenie jest wartością.`
    #
    # Ciało należy do zdania, a nie do zdania składowego, i nie jest to ten sam
    # powód co przy dwukropku niżej: na poziomie `zdanie` tej pozycji nie ma jak
    # odgraniczyć od koordynacji, bo `A, i B` miałoby wtedy dwa wyprowadzenia —
    # spójnik zaczyna człon drugi albo koordynuje. Zdanie ma czoło jedno, więc
    # tutaj rozgraniczenie jest za darmo.
    #
    # Zakup, cenę i to, czemu lematy są listą, trzyma
    # docs/konstrukcje-gramatyczne.md#spójnik-na-czele-zdania-wiąże-je-z-poprzednim.
    grammar.rule("wypowiedzenie", [SPÓJNIK_NA_CZELE, Głowa(nt("zdanie")), KONIEC_ZDANIA])

    # Dwukropek otwierający zdanie: `Cena jest niska: gramatyka jest
    # bezkontekstowa.` Produkcja należy do zdania, a nie do zdania składowego, bo
    # `A, B: C.` czyta się jako `(A, B): C`, a na poziomie `zdanie` byłaby
    # prawostronnie rekurencyjna razem z przecinkiem i wypuszczała `A, (B: C)`.
    #
    # Niezmiennik — że jednoznaczności nie odbiera ani jedno z tych ciał —
    # pilnuje tests/test_subset.py, a wywód wraz z zakupem trzyma
    # docs/konstrukcje-gramatyczne.md#interpunkcja-zdaniowa-spina-zdania-które-już-się-wyprowadzają.
    # Ciała są trzy, a nie jedno biorące trzy znaki, bo zakup każdego z nich jest
    # osobną liczbą i sonda bierze ją zdejmowaniem ciał.
    for znak in (DWUKROPEK, ŚREDNIK, MYŚLNIK):
        grammar.rule("wypowiedzenie", [Głowa(nt("zdanie")), znak, nt("zdanie"), KONIEC_ZDANIA])

    # Grupa imienna za dwukropkiem, tam gdzie trzy ciała wyżej żądają zdania:
    # `Warstwa pyta o dwa typy: Zdanie oraz Kontekst.`, `Gramatyka ma dwie role:
    # podmiot i dopełnienie.` Rejestr wylicza tak to, co zdanie przed dwukropkiem
    # nazwało liczbą albo terminem, a wylicza jednym ciągiem współrzędnym, więc
    # grupa bierze tę pozycję cała.
    #
    # Ciało jest osobne, a nie symbolem obejmującym zdanie i grupę, bo cena
    # każdego z nich jest osobną liczbą. Drugiego czytania nie daje żadnemu
    # napisowi, bo grupa imienna zdaniem nie jest, i to pilnuje tests/test_subset.py.
    #
    # Myślnik i średnik tej pozycji nie dostają, bo ten rejestr nie pisze za nimi
    # samej grupy: myślnikiem wtrąca całe zdanie, a średnikiem rozdziela dwa.
    grammar.rule(DOPOWIEDZENIE, [DWUKROPEK, Głowa(nt("grupa_imienna"))])
    # Pytanie zależne w tym samym miejscu: `Sprawdzasz to jednym pytaniem: czy
    # skreślona rzecz jest nadal powiedziana gdzie indziej?`
    #
    # Ciałem jest ciąg, a nie pojedyncze pytanie, bo pytania stoją tu obok siebie
    # tak samo jak przy czasowniku, który je bierze (`ciąg_pytajny`).
    # Rozłączności trzech symboli za tym znakiem pilnuje tests/test_subset.py,
    # a zakup i cenę trzyma docs/subset.md pod interpunkcją zdaniową.
    grammar.rule(DOPOWIEDZENIE, [DWUKROPEK, Głowa(nt("ciąg_pytajny"))])
    grammar.rule("wypowiedzenie", [Głowa(nt("zdanie")), nt(DOPOWIEDZENIE), KONIEC_ZDANIA])


def _koordynacja_zdań(grammar: Grammar) -> None:
    """Ciąg współrzędny zdań składowych, spięty spójnikiem albo przecinkiem."""
    # To, co człon może zawierać, rozstrzyga,
    # do czego koordynację da się przyłączyć z zewnątrz,
    # i na tym stoi zawężenie zasięgu, a nie na kształcie tych produkcji.
    # X → X conj X powiedziałoby to samo o zasięgu
    # i tablica Earleya bierze taką produkcję bez skargi,
    # a różni je liczba czytań ciągu współrzędnego; todo/ trzyma ten wybór.
    # Symbol wspólny na spójnik i na przecinek powiedziałby to samo raz,
    # ale przecinek przestałby stać przy swoim poziomie,
    # a cena i zakup każdego z czterech poziomów są osobnymi liczbami,
    # które wzięto zdejmowaniem po jednej.
    # Zasięg koordynacji wywodzi docs/subset.md pod „Nothing above a
    # coordination distributes into it”.
    #
    # Tryb ciąg wypuszcza z członu pierwszego, a od pozostałych nie żąda niczego,
    # i jest to ta sama granica: spójnik trybu nad ciągiem żąda formy na -ł od
    # członu, którym ten ciąg jest, a nie od każdego z osobna. Zmienna wspólna
    # żądałaby jej od wszystkich i zabierałaby przy tym zdania już przyjęte, bo
    # `Program zapisuje ustawienia, a linter sprawdziłby tekst.` koordynuje tryb
    # oznajmujący z przypuszczającym.
    człon = nt("zdanie_składowe", tryb=V("t"))
    grammar.rule("zdanie", [człon], ciąg=BEZ_CIĄGU)
    grammar.rule("zdanie", [Głowa(człon), SPÓJNIK_BEZ_PRZECINKA, nt("zdanie")], ciąg=CIĄG)
    grammar.rule("zdanie", [Głowa(człon), PRZECINEK, nt("zdanie")], ciąg=CIĄG)
    # Przecinek i spójnik naraz, czyli ta interpunkcja, której polszczyzna żąda
    # przed `ale`, `a` i `więc` (:data:`SPÓJNIKI_PRZECINKOWE`). Poziom zdaniowy
    # ma tę pozycję, a imienny i przymiotnikowy nie, bo lista tych spójników jest
    # listą spójników zdaniowych: `nie polszczyzny, a dziedziny` jest w niej
    # elipsą, a nie ciągiem współrzędnym dwóch grup imiennych.
    grammar.rule("zdanie", [Głowa(człon), PRZECINEK, SPÓJNIK_PRZECINKOWY, nt("zdanie")], ciąg=CIĄG)
    # Spójnik skorelowany, czyli powtórzony przed każdym członem: `Ani parser nie
    # rośnie, ani linter nie sprawdza.` Ciało jest trzecim na tym poziomie, a nie
    # drugą listą lematów, bo polszczyzna stawia spójnik dwa razy i przed drugim
    # żąda przecinka, gdzie koordynacja wyżej stawia go raz i między członami.
    # Zakup i cenę trzyma
    # docs/konstrukcje-gramatyczne.md#spójnik-skorelowany-powtarza-się-przed-każdym-członem.
    grammar.rule(
        "zdanie",
        [SPÓJNIK_SKORELOWANY, Głowa(człon), PRZECINEK, SPÓJNIK_SKORELOWANY, nt("zdanie")],
        ciąg=CIĄG,
    )
