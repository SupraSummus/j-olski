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

Wypisuje je w kontekście, którym linearyzacja to zdanie składała,
bo to on rozstrzyga, jakim napisem ono wyszło:
podmiot bywa opuszczony, a rzecz wskazana wychodzi zaimkiem.
Zdanie mierzone jako stojące samo jest przez to innym zdaniem
niż to, które autor dostał, i te dwa mają różne role widoczne.

Jest to ten sam pomiar, który stoi w ``pomijalny`` w ``olski/skład/składnia.py``.
Tamten pyta, czy podmiot wróci czytelnikowi z formy czasownika,
i liczy to tak, że wypisuje formę dla każdego, kto mógłby ją wyciągnąć.
Tutaj pytanie jest o rolę zamiast o podmiot, a sposób ten sam,
i dlatego kolizja nie jest tu wyjątkiem: obie rzeczy są własnością napisu,
a nie błędem drzewa, które ten napis wypuściło.

Wieloznaczność jest przy tym przekleństwem parsera, a nie generatora.
``harness/wieloznaczność.py`` liczy tę samą klasę nad cudzym tekstem
i musi zgadywać z form to, co tutaj wiadomo z drzewa:
gdzie kończy się grupa imienna, co jest uczestnikiem, a co stoi pod przyimkiem,
i przy którym orzeczeniu para stanęła.
Sam nazywa przez to swoją liczbę górnym oszacowaniem.
Tutaj żadne z tych pytań się nie stawia,
bo uczestnicy są w drzewie wymienieni, a orzeczenie jest w nim węzłem.
Poprawiło to raz tamten pomiar, o czym mówi w nim ``_obojętny``.

Klasa jest tu jedna z dwóch, które ta wieloznaczność ma nad polszczyzną.
Przyłączenia ten przegląd nie zgłasza,
bo o wyrażeniu przyimkowym drzewo mówi to, czego przy rolach nie mówi:
okolicznik dochodzi w nim do zdarzenia zawsze, więc każde miejsce byłoby trafieniem,
a raport zgłaszający każde zdanie z przyimkiem nie oddziela niczego od niczego.
Czym to zawęzić, jest osobnym pytaniem i trzyma je ``TODO.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

from olski.skład.składnia import TERAZ, Kontekst, Zdanie, forma_czasownika, wypisz


@dataclass(frozen=True)
class Kolizja:
    """Dwie role jednego zdarzenia, których czytelnik od siebie nie odróżni.

    Klasy to zgłoszenie nie niesie, bo klasa jest jedna,
    a pole o jednej wartości mówi, że druga zaraz dojdzie,
    i mówi to niezależnie od tego, czy dojdzie.
    """

    #: Napisy, którymi te role w tekście stanęły, w kolejności, w której stoją.
    #: Bez nich zgłoszenie nie ma czym się wytłumaczyć,
    #: bo zdanie o dwóch zdarzeniach niesie dwa zarzuty naraz.
    #: Napis jest jeden tam, gdzie podmiot z tekstu wypadł,
    #: bo forma, której nie widać, nie jest tym, na co autor ma spojrzeć.
    formy: tuple[str, ...]

    def opisz(self) -> str:
        """Zdanie, które autor ma przeczytać, wraz z tym, na czym zarzut stoi."""
        if len(self.formy) == 1:
            return (
                f"„{self.formy[0]}” stoi w formie, którą polszczyzna czyta "
                "i w jednej roli, i w drugiej, a podmiotu to zdanie nie wypisuje, "
                "więc czytelnik nie ma z czego odzyskać, która rola jest którą"
            )
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

    Kontekst każde zdanie dostaje własny i bierze go z ``konteksty``,
    czyli stamtąd, skąd bierze go linearyzacja.
    Bez tego przegląd mierzyłby zdanie wypisane samo,
    a mierzyć ma to, co wyszło: podmiot bywa opuszczony,
    a rzecz wskazana wychodzi zaimkiem, który przypadek pokazuje.
    """
    kolizje = []
    for zdanie, jego in drzewo.konteksty(kontekst):
        (podmiot, _), *reszta = zdanie.uczestnicy(jego)
        #  Krotka pusta tam, gdzie podmiot z tekstu wypadł, bo zgłoszenie wymienia
        #  formy, które autor w napisie zobaczy, a tej nie zobaczy żadnej.
        wypisany = (wypisz(podmiot, "nom", jego).napis,) if jego.wypisuje(podmiot) else ()
        for rola, przypadek in reszta:
            if not _rozróżnia(zdanie, podmiot, rola, przypadek, jego):
                kolizje.append(Kolizja((*wypisany, wypisz(rola, przypadek, jego).napis)))
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

    Pierwsza z nich odpada tam, gdzie podmiotu w tekście nie ma:
    zdanie, które go opuściło, żadnej jego formy czytelnikowi nie pokazuje,
    więc rozróżnienie wzięte z niej byłoby rozróżnieniem wziętym z drzewa.
    Zostają wtedy dwie i obie mierzą to, co widać:
    formę, którą uczestnik stanął, oraz formę czasownika,
    bo tą drugą czytelnik odzyskuje opuszczony podmiot.
    O to, czy podmiot stanął, pyta się tutaj, a nie bierze się tego od wołającego,
    bo nie jest to jego wybór, tylko fakt o kontekście i o tej roli.
    """
    if kontekst.wypisuje(podmiot) and (
        wypisz(podmiot, "nom", kontekst).napis != wypisz(podmiot, "acc", kontekst).napis
    ):
        return True
    return (
        wypisz(rola, przypadek, kontekst).napis != wypisz(rola, "nom", kontekst).napis
        or forma_czasownika(zdanie.czasownik, podmiot, kontekst)
        != forma_czasownika(zdanie.czasownik, rola, kontekst)
    )
