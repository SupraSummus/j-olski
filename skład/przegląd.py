"""Czy czytelnik odzyska z tekstu to drzewo, które ten tekst wypuściło.

Drzewo jest jednoznaczne z definicji, a napis, który z niego wychodzi, nie musi być,
i te dwie rzeczy rozchodzą się cicho:
zgodność jest policzona, rama sprawdzona, forma wzięta ze słownika,
a mimo to ``Koszt szynki przewyższa koszt bułki.`` nie mówi, co tu jest większe.
Ten moduł jest miejscem, w którym takie zdanie się zgłasza,
a dlaczego zgłasza, zamiast się nie skompilować,
rozstrzyga ``docs/sklad.md`` wraz z resztą postawy tego przeglądu.

Liczone jest to z form, które skład sam wypisał, i nic poza nimi nie wchodzi.
Rola wraca czytelnikowi z formy i z czasownika, więc pyta się o jedno i o drugie:
czy rola wypisana tutaj stoi w formie, którą czyta się także w tej drugiej pozycji,
i czy czasownik tych dwóch ról nie rozróżnia.
Obie odpowiedzi wychodzą z linearyzacji, bo obie są formami,
a form skład nie zgaduje: wypisuje rolę drugi raz i porównuje napisy.

Jest to ten sam pomiar, który stoi w ``pomijalny`` w ``skład/składnia.py``,
i wart jest tego, żeby to nazwać.
Tamten pyta, czy podmiot wróci czytelnikowi z formy czasownika,
i liczy to tak, że wypisuje formę dla każdego, kto mógłby ją wyciągnąć.
Tutaj pytanie jest o rolę zamiast o podmiot, a sposób ten sam,
i dlatego kolizja nie jest tu wyjątkiem: obie rzeczy są własnością napisu,
a nie błędem drzewa, które ten napis wypuściło.

Wieloznaczność jest przy tym przekleństwem parsera, a nie generatora,
i widać to na tym module najlepiej.
``olski/wieloznaczność.py`` liczy tę samą klasę nad cudzym tekstem
i musi zgadywać z form to, co tutaj wiadomo z drzewa:
gdzie kończy się grupa imienna, co jest uczestnikiem, a co stoi pod przyimkiem,
i przy którym orzeczeniu para stanęła.
Sam nazywa przez to swoją liczbę górnym oszacowaniem.
Tutaj żadne z tych pytań się nie stawia,
bo uczestnicy są w drzewie wymienieni, a orzeczenie jest w nim węzłem.
Idzie to nawet dalej, niż tamten pomiar sięga:
``Mysz goni ogon.`` czyta się dwojako, a tamten tego nie melduje,
bo synkretyzm liczy z jednego czytania słownika,
podczas gdy ``mysz`` niesie mianownik i biernik dwoma osobnymi wpisami.
Porównanie napisów o wpisy nie pyta, więc tę parę widzi;
że tamten jej nie widzi, jest usterką tamtego modułu i trzyma to ``TODO.md``.

Klasa jest tu jedna z dwóch, które ta wieloznaczność ma nad polszczyzną.
Przyłączenia ten przegląd nie zgłasza,
bo o wyrażeniu przyimkowym drzewo mówi to, czego przy rolach nie mówi:
okolicznik dochodzi w nim do zdarzenia zawsze, więc każde miejsce byłoby trafieniem,
a raport zgłaszający każde zdanie z przyimkiem nie oddziela niczego od niczego.
Czym to zawęzić, jest osobnym pytaniem i trzyma je ``TODO.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

from skład.składnia import TERAZ, Kontekst, Zdanie, forma_czasownika, wypisz


@dataclass(frozen=True)
class Kolizja:
    """Dwie role jednego zdarzenia, których czytelnik od siebie nie odróżni.

    Klasy to zgłoszenie nie niesie, bo klasa jest jedna,
    a pole o jednej wartości mówi, że druga zaraz dojdzie,
    i mówi to niezależnie od tego, czy dojdzie.
    """

    #: Napisy, którymi te role stanęły, w kolejności, w której stoją w zdaniu.
    #: Bez nich zgłoszenie nie ma czym się wytłumaczyć,
    #: bo zdanie o dwóch zdarzeniach niesie dwa zarzuty naraz.
    formy: tuple[str, str]

    def opisz(self) -> str:
        """Zdanie, które autor ma przeczytać, wraz z tym, na czym zarzut stoi."""
        stoją = " i ".join(f"„{forma}”" for forma in self.formy)
        return (
            f"{stoją} stoją w formach, które polszczyzna czyta i w jednej roli, "
            "i w drugiej, a czasownik ich nie rozróżnia, "
            "więc zdanie czyta się i jako SVO, i jako OVS"
        )


def przejrzyj(drzewo: Zdanie, kontekst: Kontekst = TERAZ) -> list[Kolizja]:
    """Kolizje w zdaniu, które z tego drzewa wychodzi, po jednej na orzeczenie.

    Zestawiany jest podmiot z każdym uczestnikiem obok niego,
    bo wymienić się mogą tylko te dwie role: pozycji podmiotu jest jedna,
    więc dwa dopełnienia przy jednym czasowniku o nią nie konkurują.
    """
    kolizje = []
    for zdanie in drzewo.zdania:
        (podmiot, _), *reszta = zdanie.uczestnicy(kontekst)
        for rola, przypadek in reszta:
            if _rozróżnia(zdanie, podmiot, rola, przypadek, kontekst):
                continue
            kolizje.append(
                Kolizja(
                    (
                        wypisz(podmiot, "nom", kontekst).napis,
                        wypisz(rola, przypadek, kontekst).napis,
                    )
                )
            )
    return kolizje


def _rozróżnia(zdanie, podmiot, rola, przypadek: str, kontekst: Kontekst) -> bool:
    """Czy cokolwiek w tym zdaniu mówi czytelnikowi, która z tych dwóch ról jest którą.

    Rozróżnić może jedna z trzech rzeczy i wystarczy dowolna.
    Forma podmiotu, gdy w bierniku brzmi inaczej niż w mianowniku:
    wtedy czytelnik wie, że podmiotem nie jest dopełnienie.
    Forma dopełnienia, gdy w mianowniku brzmi inaczej niż tu;
    tędy wychodzi także narzędnik orzecznika i dopełniacz negacji,
    bo ani jeden, ani drugi mianownikowi równy nie jest.
    Czasownik, gdy te dwie role wyciągają z niego różne formy:
    tak rozstrzyga liczba zawsze, a rodzaj w czasie przeszłym,
    bo forma osobowa czasu teraźniejszego rodzaju nie niesie.
    """
    return (
        wypisz(podmiot, "nom", kontekst).napis != wypisz(podmiot, "acc", kontekst).napis
        or wypisz(rola, przypadek, kontekst).napis != wypisz(rola, "nom", kontekst).napis
        or forma_czasownika(zdanie.czasownik, podmiot, kontekst)
        != forma_czasownika(zdanie.czasownik, rola, kontekst)
    )
