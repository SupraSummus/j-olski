"""Kontekst: czego wypisywane drzewo o sobie nie wie.

Moduł nie zna ani kategorii, ani napisu, i dlatego jest w tym torze pierwszy.
Roli nie rozpoznaje po typie, tylko pyta ją o to, co każda o sobie mówi:
o tożsamość oraz o rdzeń (``Rola`` w ``olski/skład/grupa.py``),
więc kategoria dopisana tam nie dokłada tutaj gałęzi.

Adnotacji ta rola nie ma i jest to brak nazwany, a nie przeoczony:
typ wpisany tu z powrotem zawróciłby import do kategorii.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Kontekst:
    """Czego linearyzacja nie znajduje w drzewie, które właśnie wypisuje.

    Pierwsze dwie rzeczy są własnościami tekstu, a nie zdania,
    więc zdanie ich w sobie nie trzyma:
    ta sama rzecz opowiedziana raz jako to, co się stało, a raz jako to, co się dzieje,
    jest jednym drzewem i dwoma czasami.
    Kto tymi dwoma steruje, mówi ``olski/skład/opowieść.py``.

    Pozostałe są własnościami miejsca, w którym zdanie stoi.
    Zdanie wypisywane jako opis rzeczy mówi o tej rzeczy zaimkiem, a nie nazwą.
    Zdanie wypisywane jako dopełnienie czasownika nad nim nie ma podmiotu wcale,
    bo wykonawcę bierze stamtąd, i wychodzi bezokolicznikiem;
    to samo miejsce niesie przeczenie tamtego czasownika,
    bo dopełniacz negacji sięga przez bezokolicznik do jego dopełnienia.
    Steruje tym wszystkim drzewo, a nie tekst,
    a mechanizmy trzymają ``Opis`` oraz ``Robi`` w ``olski/skład/składnia.py``.
    Stoją tu obok czasu, bo pytanie jest jedno:
    czego wypisywane drzewo o sobie nie wie.

    Wartość domyślna jest zdaniem stojącym samo:
    dzieje się teraz, nie ma za sobą nikogo, kogo dałoby się pominąć,
    niczego nie opisuje, orzeka o własnym podmiocie i nikt go nie przeczy.
    """

    czas: str = "teraz"
    pomijany: object = None
    wskazywany: object = None
    sprawca: object = None
    pod_przeczeniem: bool = False

    def podrzędne(self) -> Kontekst:
        """Kontekst, który dostaje zdanie postawione pod tym zdaniem.

        Czas dziedziczy się, bo jest własnością opowiadania, a nie zdania.
        Reszta nie dziedziczy się i każde pole ma na to własny powód:
        zaimek względny wyszedłby z niższego zdania na czoło, którego ono nie ma,
        podmiot opuszczony odsyłałby tam, gdzie stoi ktoś inny,
        a bezokolicznik i przeczenie sięgają jednego piętra,
        bo tyle sięga czasownik, który je narzucił.
        Stoi to jedną metodą, bo pole dopisane do tej klasy i tu pominięte
        przeciekłoby w dół po cichu, i to w miejscu, którego autor nie widzi.
        """
        return Kontekst(czas=self.czas)

    def pomija(self, rola) -> bool:
        """Czy podmiot jest tym, o kim mowa była zdanie wcześniej.

        Pominięty podmiot jest w polszczyźnie zwykłym sposobem mówienia dalej
        o tym samym, bo osobę i rodzaj niesie sam czasownik,
        więc nie ma czego powtarzać.
        """
        return self.pomijany is not None and rola.tożsamość is self.pomijany

    def wypisuje(self, rola) -> bool:
        """Czy podmiot wyjdzie w tekście, czy czytelnik odzyska go bez niego.

        Powody są dwa i schodzą się tutaj, bo pytają o nie dwa miejsca:
        linearyzacja, żeby podmiotu nie wypisać,
        i ``olski/skład/przegląd.py``, żeby nie liczyć formy, której nikt nie zobaczy.
        Zdanie obok orzekało o tym samym i wtedy mówi o tym ``pomija`` wyżej,
        albo wykonawcę wskazał czasownik nad tym zdaniem i wtedy wychodzi
        bezokolicznik, który podmiotu nie ma wcale.
        """
        return self.sprawca is None and not self.pomija(rola)

    def wskazuje(self, rola) -> bool:
        """Czy to ta rola, którą wypisywane zdanie wskazuje.

        Porównaniem jest tożsamość obiektu, a nie równość,
        bo tą samą rzeczą jest tu ta sama zmienna, tak samo jak przy ``Postać``:
        dwie równe grupy imienne są dwiema rzeczami, dopóki autor nie użyje jednej.
        """
        return self.wskazywany is not None and rola.rdzeń is self.wskazywany.rdzeń


TERAZ = Kontekst()

