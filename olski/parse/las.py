"""Pakowanie czytań, liczenie ich, wyliczanie i punkt, na którym stanęło odrzucenie.

Czemu pyta się lasu, a nie listy czytań, wywodzi :class:`Las`.
Decyzje, których czytania nie rozstrzygają, liczy z tego lasu ``olski.parse.decyzje``.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import replace
from itertools import product

from olski.grammar import EMPTY, Env, Part, Production, Sym, Word, bierze, features_of, unify
from olski.morph import Reading, Segment
from olski.parse.czytanie import Cykl, Leaf, Node, Pozycja
from olski.parse.tablica import _Stan, _Tablica

#: Cechy, z jakimi konstytuent wychodzi do rodzica, w postaci dającej się zahaszować.
#: Tyle o nim rodzic wie,
#: i dlatego tyle wystarczy, żeby liczyć czytania bez wyliczania ich.
Cechy = frozenset[tuple[str, frozenset[str]]]

#: Kształty jednej pozycji dzielą się na klasy po tym, z jakimi cechami wychodzą.
#: Klasą jest zbiór, a nie jedne cechy,
#: bo forma o kilku czytaniach daje jeden kształt i kilka sposobów, na jakie on przechodzi.
Klasa = frozenset[Cechy]


#: Czym córka jest w jednym sposobie, na jaki przechodzi przez ciało produkcji:
#: liściem, bo terminal bierze jedno czytanie formy,
#: albo cechami, bo tyle rodzic z konstytuentu widzi.
Wybór = Leaf | Cechy

#: Enumeration is capped,
#: because an ambiguous sentence can have very many readings
#: and the answer past the second one is always the same: too many.
#: The count itself is not capped, the forest giving it without walking the trees.
MAX_READINGS = 64


def _cięcie(ciało: tuple[Pozycja, ...]) -> tuple[tuple[int, int, str], ...]:
    """Rozpiętości córek malejąco, a pod każdą jej etykieta.

    Malejąco, czyli przodem idzie ciało o dłuższej pierwszej córce, a to znaczy,
    że materiał dołączył do konstytuentu tuż przed nim, a nie do tego wyżej.
    Kierunek wybrano pomiarem, bo argumentu z góry na niego nie było
    (docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie).
    Etykieta pod rozpiętością rozstrzyga ciała, których gramatyka nie różnicuje
    ani kosztem, ani cięciem, i jest wyborem arbitralnym; liść wchodzi tam pusty,
    bo czytaniem liścia jest sama rozpiętość.
    """
    return tuple((-pozycja.span[0], -pozycja.span[1], pozycja.label or "") for pozycja in ciało)


def _klucz_cech(cechy: Cechy) -> list[tuple[str, list[str]]]:
    """Cechy w postaci, którą można porównać, bo zbiór własnej kolejności nie ma.

    Wyliczone drzewo wybiera między cechami jednej klasy,
    a wybór po kolejności zbioru byłby inny w każdym przebiegu,
    bo haszowanie napisów jest losowane przy starcie.
    Kolejności samych drzew to nie ustala:
    ustala ją :meth:`_Tablica.ciała`, i tam jest wypisana.
    """
    return sorted((nazwa, sorted(wartości)) for nazwa, wartości in cechy)


def _jedne(klasa: Klasa) -> Cechy:
    """Jedne cechy z tej klasy, do wyliczenia drzewa tam, gdzie cech nie żąda rodzic.

    Klasa zbiera cechy, na jakie kształt przechodzi, a odczytaniem jest kształt,
    więc która z nich wychodzi na wierzch, żadnego odczytania nie odróżnia:
    ``dla przyjemności`` jest jedną grupą przyimkową w dwóch liczbach
    i drzewo pokazuje ją w jednej.
    Niżej w drzewie cech żąda rodzic, więc ten wybór pada raz na drzewo.
    Odczytań formy pod tym drzewem nie rozstrzyga (:meth:`Las._wsparte`).
    """
    return min(klasa, key=_klucz_cech)


def _z_odczytaniami(
    wybory: tuple[Wybór, ...], wsparte: tuple[frozenset, ...]
) -> tuple[Wybór, ...]:
    """Te same wybory, a na liściach każde wsparte odczytanie, nie jedno.

    Kolejność jest kolejnością odczytań segmentu, a nie zbioru wspartych:
    zbiór wypisany po kolei różniłby się między przebiegami
    (:meth:`_Tablica.ciała` mówi, czemu to psuje wydruk).
    """
    return tuple(
        replace(
            wybór,
            odczytania=tuple(c for c in wybór.segment.readings if c in wsparte[miejsce]),
        )
        if isinstance(wybór, Leaf)
        else wybór
        for miejsce, wybór in enumerate(wybory)
    )


#: Rozpiętości ról jednego czytania: jedna pozycja na etykietę,
#: w kolejności etykiet, o które zapytano.
#: Jedna etykieta bierze zbiór, bo czytanie o zdaniu współrzędnym ma dwa podmioty,
#: a wszystkie etykiety idą w jednym rozdaniu,
#: bo pytanie o cudze czytanie dotyczy przypisania naraz:
#: czytanie z dobrym podmiotem i cudzym dopełnieniem tym czytaniem nie jest.
Rozdanie = tuple[frozenset[tuple[int, int]], ...]


def _rozdanie_drzewa(drzewo: Node, etykiety: tuple[str, ...]) -> Rozdanie:
    """Rozdanie ról jednego wyliczonego czytania.

    Tą samą miarą, jaką składa je z lasu :meth:`Las._rozdania`,
    czyli każdym węzłem tej etykiety pod korzeniem (:meth:`Node.find`),
    bo dopiero wtedy numer jest numerem czytania, o które pytano.
    """
    return tuple(frozenset(node.span for node in drzewo.find(etykieta)) for etykieta in etykiety)


def _ponad(rozdanie: Rozdanie, żądane: Rozdanie) -> bool:
    """Czy to rozdanie obsadza rolę rozpiętością, której żądane nie ma."""
    return any(obsadzone - wolno for obsadzone, wolno in zip(rozdanie, żądane, strict=True))


def _zsumuj(
    dotąd: Iterable[Rozdanie], dokładane: Iterable[Rozdanie], żądane: Rozdanie
) -> set[Rozdanie]:
    """Rozdania z każdej pary tych dwóch, bez tych, które wychodzą ponad żądane."""
    dokładane = list(dokładane)
    złożone = set()
    for zebrane in dotąd:
        for córka in dokładane:
            razem = tuple(a | b for a, b in zip(zebrane, córka, strict=True))
            if not _ponad(razem, żądane):
                złożone.add(razem)
    return złożone


class Las:
    """Las ze współdzielonymi węzłami i podsumowania, jakie z niego wychodzą.

    Taki las odpowiada na pytanie olskiego pod dwoma warunkami.
    Jedną pozycję dostaje to, co jest jednym czytaniem,
    o czym rozstrzyga :class:`Pozycja`;
    liczba z jednej pozycji łączy się z liczbą z sąsiedniej tak, jak łączy je unifikacja,
    o czym rozstrzyga :meth:`klasy`.
    Wywód obu i pomiar, którym wybrano drugi, mieści
    docs/parsowanie.md#co-się-pakuje-rozstrzyga-tożsamość-czytania.
    """

    def __init__(self, tablica: _Tablica) -> None:
        self._tablica = tablica
        self.grammar = tablica.grammar
        self.korzeń = Pozycja(tablica.start, (tablica.początek, tablica.koniec))
        #: Rozpiętość → czytania form, jakie przez nią przechodzą.
        #: Kluczem jest rozpiętość, a nie segment, bo czytaniem liścia jest sama rozpiętość.
        self._czytania_liścia: dict[tuple[int, int], list[tuple[Segment, Reading]]] = {}
        for segment in tablica.segments:
            miejsce = self._czytania_liścia.setdefault((segment.start, segment.end), [])
            miejsce.extend((segment, reading) for reading in segment.readings)
        self._wyprowadzenia: dict[Pozycja, dict[tuple[Pozycja, ...], tuple[Production, ...]]] = {}
        #: Pozycja → koszt najtańszej morfologii pod nią (:meth:`koszt_morfologii`),
        #: wpisywany razem z wyprowadzeniami, bo liczy się go z tego samego przejścia.
        self._koszty: dict[Pozycja, int] = {}
        #: Pozycje, których koszt właśnie się liczy, czyli strażnik cyklu w
        #: gramatyce, gdzie symbol stoi pod sobą o tej samej rozpiętości.
        self._liczone: set[Pozycja] = set()
        self._klasy: dict[Pozycja, dict[Klasa, int]] = {}
        #: (pozycja, klasa) → kombinacja klas córek → produkcje, którymi przeszła.
        #: Las jest tu już po unifikacji:
        #: kombinacji, której ona nie przepuszcza, nie ma tu wcale,
        #: więc każda gałąź kończy się czytaniem.
        #: Produkcji jest tu kilka, bo dwie o jednym ciele są jednym kształtem,
        #: a różnić je może i terminal, i wypuszczane cechy (:meth:`wyprowadzenia`),
        #: i wyliczenie drzewa wybiera stąd tę, która wypuszcza żądane
        #: (:meth:`_drzewa`).
        #: Odczytania form czyta za to z każdej z nich (:meth:`_wsparte_kształtu`).
        #: Wpisuje tu sama :meth:`klasy`, a czyta się przez :meth:`_krawędzie`.
        self._krawędzie_lasu: dict[tuple[Pozycja, Klasa], dict[tuple, tuple[Production, ...]]] = {}
        self._czynne: set[Pozycja] = set()
        self._żywe_pary: set[tuple[Pozycja, Klasa]] | None = None
        self._rodzice: dict[tuple[Pozycja, Klasa], set[tuple[Pozycja, Klasa]]] | None = None
        self._prefiksy: dict[tuple, frozenset[Env]] = {}
        #: (produkcja, kombinacja, cechy dozwolone, miejsce, środowisko) → czy ciało
        #: domyka się od tego miejsca. Pyta o to raz na odczytanie liścia
        #: (:meth:`_wsparte`), a pary powtarzają się między odczytaniami.
        self._domknięcia: dict[tuple, bool] = {}
        #: (produkcje, kombinacja, cechy dozwolone) → czym każda córka w tym
        #: kształcie być może (:meth:`_wsparte_kształtu`). Ciało pojedyncze drugiego
        #: takiego słownika nie ma: pyta o nie sama ta suma, więc jego klucz nie
        #: powtórzyłby się nigdy.
        self._wsparcia_kształtów: dict[tuple, tuple[frozenset, ...]] = {}
        #: (para, etykiety, żądane rozdanie) → rozdania, jakie ta para umie złożyć.
        #: Żądane jest w kluczu, bo to ono odsiewa:
        #: rozdania spoza niego nie ma tu wcale (:meth:`_rozdania`).
        self._rozdania_pary: dict[
            tuple[tuple[Pozycja, Klasa], tuple[str, ...], Rozdanie], frozenset[Rozdanie]
        ] = {}
        #: (produkcja, kombinacja, żądane cechy) → czym jest w tym ciele każda córka.
        #: Kluczem jest całe ciało, a nie jedna córka,
        #: bo o czytaniu jednego liścia rozstrzyga unifikacja z pozostałymi.
        self._wybory_ciał: dict[tuple, tuple[Wybór, ...] | None] = {}
        self._przedstawiciele: dict[Pozycja, Node] = {}
        self._najdalszy: int | None = None

    # -- tablica -------------------------------------------------------------#

    def wyprowadzenia(self, pozycja: Pozycja) -> dict[tuple[Pozycja, ...], tuple[Production, ...]]:
        """Wyprowadzenia pod tą pozycją: ciało → produkcje, które je złożyły.

        Kluczem jest ciało, a nie produkcja,
        bo o kształcie rozstrzygają etykiety i rozpiętości córek.
        Dwie produkcje o jednym ciele dają jedno czytanie i wchodzą tu razem,
        choćby brały co innego: nad jedną formą ``człon_imienny`` z rzeczownika i
        ``człon_imienny`` z zaimka są jednym ciałem, bo liść jest swoją rozpiętością.
        Odczytania obu niesie potem liść (:meth:`Las._wsparte_kształtu`).

        Pytana o pozycję, której tablica nie domknęła, oddaje pusty słownik,
        więc jest to zarazem sposób zapytania lasu, czy taki konstytuent w ogóle powstał.
        Odpowiedź kosztuje przy tym całe poddrzewo, bo wycena schodzi po córkach
        (:meth:`koszt_morfologii`), a nie samo domknięcie tej jednej pozycji.

        To jedno miejsce ustala kolejność, w jakiej las wydaje drzewa —
        dziedziczą ją klasy pozycji, krawędzie pod nimi i drzewa z tych krawędzi —
        a rozstrzyga o niej koszt ciała, a pod nim :func:`_cięcie`.
        Nieposortowane szłyby tak, jak ``for_head`` oddaje produkcje,
        czyli w kolejności dopisywania ich do gramatyki (docs/disambiguation.md).
        """
        gotowe = self._wyprowadzenia.get(pozycja)
        if gotowe is not None:
            return gotowe
        znalezione: dict[tuple[Pozycja, ...], list[Production]] = {}
        if not pozycja.liść:
            źródło, k = pozycja.span
            for production in self.grammar.for_head(pozycja.label):
                if not self._tablica.zamknięte(production, źródło, k):
                    continue
                for ciało in self._tablica.ciała(production, len(production.body), źródło, k):
                    znalezione.setdefault(ciało, []).append(production)
        self._liczone.add(pozycja)
        try:
            wyceny = {
                ciało: [
                    (production.koszt, self._morfologia_ciała(production, ciało))
                    for production in produkcje
                ]
                for ciało, produkcje in znalezione.items()
            }
        finally:
            self._liczone.discard(pozycja)
        # Morfologia dodaje się do kosztu tej produkcji, która ją wzięła,
        # bo to jej terminale mówią, którym czytaniem forma tu weszła;
        # ciało kosztuje potem tyle, co najtańsza z produkcji, które je składają.
        koszty = {ciało: min(k + m for k, m in pary) for ciało, pary in wyceny.items()}
        zebrane = {
            ciało: tuple(sorted(znalezione[ciało], key=lambda p: p.koszt))
            for ciało in sorted(znalezione, key=lambda c: (koszty[c], _cięcie(c)))
        }
        self._wyprowadzenia[pozycja] = zebrane
        self._koszty[pozycja] = min((m for pary in wyceny.values() for _k, m in pary), default=0)
        return zebrane

    def _morfologia_ciała(self, production: Production, ciało: tuple[Pozycja, ...]) -> int:
        """Koszt morfologii pod tym ciałem: po córce, a pod liściem po terminalu.

        Koszt morfologii sumuje się po poddrzewie, a koszt produkcji zostaje przy
        swoim ciele, i jest to ten sam warunek czytany dwa razy:
        koszt rozstrzyga między ciałami jednej pozycji,
        więc zostaje tam, gdzie konkurencja jest, a idzie wyżej, gdy jej nie ma.
        Ciała córki rozstrzygnęła sama córka,
        a czytania formy nie rozstrzyga nikt, bo liść ciał nie ma (:class:`Pozycja`).
        Bez tego pchania w górę `Wszystko jest podmiotem.` wydaje przodem czytanie
        z `Wszystko` w okoliczniku, choć opiera się ono na przysłówku,
        który słownik nazywa regionalnym (``olski/rejestr.py``):
        te dwa czytania różnią się dopiero pod `zdanie_składowe`,
        a przysłówek jest trzy pozycje niżej.
        """
        return sum(
            self._tablica.koszt_morfologii(część, dziecko.span)
            if dziecko.liść
            else self.koszt_morfologii(dziecko)
            for część, dziecko in zip(production.body, ciało, strict=True)
        )

    def koszt_morfologii(self, pozycja: Pozycja) -> int:
        """Najtańsza morfologia, na jakiej ten konstytuent się opiera.

        Liść kosztuje zero, bo jego czytania widzi dopiero terminal, który je bierze
        (:meth:`_Tablica.koszt_morfologii`):
        jedna pozycja liścia obsługuje wszystkie terminale, jakie w niej stoją.

        Pozycja stojąca pod sobą kosztuje tutaj zero i cyklu nie zgłasza,
        bo zgłasza go :meth:`klasy`, licząc czytania.
        Tam cykl jest błędem, a tutaj byłby nim porządek postawiony przed
        odpowiedzią na pytanie, czy zdanie ma w ogóle czytania.
        """
        if pozycja.liść or pozycja in self._liczone:
            return 0
        self.wyprowadzenia(pozycja)
        return self._koszty[pozycja]

    # -- unifikacja po lesie ------------------------------------------------ #

    def klasy(self, pozycja: Pozycja) -> dict[Klasa, int]:
        """Ile kształtów stoi pod tą pozycją, w klasach po tym, co wypuszczają.

        Iloczyn liczy się tutaj po parach, które unifikacja przepuszcza,
        a nie po samych pozycjach:
        kombinacja klas córek, której żadna produkcja nie składa,
        nie wnosi ani jednego czytania.

        Klasą jest zbiór cech, a nie jedne cechy,
        bo jeden kształt przechodzi czasem na kilka sposobów:
        ``dla przyjemności`` jest jedną grupą przyimkową w dwóch liczbach.
        Rodzic widzi z córki tylko to, co ona wypuszcza,
        więc grupowanie po tym zbiorze pozwala liczyć kształty zamiast sposobów:
        dwa kształty o jednym zbiorze wpadają do jednej klasy i sumują się,
        a jeden kształt wpada do dokładnie jednej.
        """
        gotowe = self._klasy.get(pozycja)
        if gotowe is not None:
            return gotowe
        if pozycja in self._czynne:
            raise Cykl(
                f"{pozycja.label} na {pozycja.span} stoi samo pod sobą; "
                "czytań jest wtedy nieskończenie wiele"
            )
        self._czynne.add(pozycja)
        klasy: dict[Klasa, int] = {}
        try:
            for ciało, produkcje in self.wyprowadzenia(pozycja).items():
                listy = [
                    [(None, 1)] if dziecko.liść else list(self.klasy(dziecko).items())
                    for dziecko in ciało
                ]
                for kombinacja in product(*listy):
                    wybór = tuple(klasa for klasa, _ile in kombinacja)
                    wypuszczane: set[Cechy] = set()
                    przeszłe = []
                    for production in produkcje:
                        cechy = self._przejdź(production, ciało, wybór)
                        if cechy:
                            wypuszczane |= cechy
                            przeszłe.append(production)
                    if not przeszłe:
                        continue
                    klasa = frozenset(wypuszczane)
                    ile = math.prod(liczba for _klasa, liczba in kombinacja)
                    klasy[klasa] = klasy.get(klasa, 0) + ile
                    self._krawędzie_lasu.setdefault((pozycja, klasa), {}).setdefault(
                        tuple(zip(ciało, wybór, strict=True)), tuple(przeszłe)
                    )
        finally:
            self._czynne.discard(pozycja)
        self._klasy[pozycja] = klasy
        return klasy

    def _krawędzie(self, para: tuple[Pozycja, Klasa]) -> dict[tuple, tuple[Production, ...]]:
        """Kombinacje klas córek pod tą parą → produkcje, którymi każda z nich przeszła.

        Krawędzie wpisuje :meth:`klasy`, więc pytanie o parę zaczyna się od
        policzenia klas jej pozycji.
        Kto czyta las, nie musi przez to wiedzieć,
        czy ktoś przed nim policzył czytania.
        Liczymy pozycję pytaną, a nie las od korzenia.
        Liczeniem od korzenia jest samo :meth:`klasy` na korzeniu,
        więc objęłoby ono pozycje, o które nikt w tym przebiegu nie pyta.

        Para spoza klas swojej pozycji podnosi tu wyjątek.
        Pustka udawałaby konstytuent, który stoi w czytaniu bez ani jednego ciała.
        Liść tu nie dochodzi, bo klas nie ma (:meth:`wyprowadzenia`).
        """
        self.klasy(para[0])
        return self._krawędzie_lasu[para]

    def _sposoby(
        self, część: Part, dziecko: Pozycja, cechy: Sequence[Cechy], env: Env
    ) -> Iterator[tuple[int, Wybór, Env]]:
        """Na jakie środowiska ta córka zawęża to jedno, i czym za każdym razem jest.

        Córka wchodzi tu samymi cechami, jakie wypuszcza, bo tyle o niej rodzic wie;
        liść wchodzi czytaniami, bo terminal sprawdza i część mowy, i lemat.
        Wychodzi stąd obok środowiska to, czym córka w tym sposobie była,
        bo wyliczone drzewo pokazuje jeden z tych sposobów,
        a nie czytanie spoza nich (:attr:`Leaf.reading`).
        Numer jest pozycją sposobu w tym, co tu weszło,
        i po nim wybiera :meth:`_wybierz`.

        Unifikacja dotyka lasu tylko w tym jednym miejscu,
        i dlatego to jedna metoda, a nie dwie:
        wołają ją liczenie kształtów, szukanie punktu, na którym odrzucenie stanęło,
        i wyliczanie drzew.
        """
        if isinstance(część, Word):
            for numer, (segment, reading) in enumerate(
                self._czytania_liścia.get(dziecko.span, ())
            ):
                złożone = bierze(
                    część,
                    reading.tag.pos,
                    reading.lemma,
                    segment.lematy,
                    reading.tag.cechy,
                    env,
                )
                if złożone is not None:
                    yield numer, Leaf(segment, (reading,)), złożone
            return
        for numer, wypuszczone in enumerate(cechy):
            złożone = unify(część.constraints, dict(wypuszczone), env)
            if złożone is not None:
                yield numer, wypuszczone, złożone

    def _dołóż(
        self,
        część: Part,
        dziecko: Pozycja,
        cechy: Iterable[Cechy],
        środowiska: Iterable[Env],
    ) -> set[Env]:
        """Środowiska po dołożeniu tej córki do tych, z jakimi ciało doszło przed nią.

        Sposób, którym córka przeszła, tu nie dochodzi,
        bo liczenie kształtów pyta o liczbę, a nie o to, którędy.
        """
        cechy = list(cechy)
        return {
            złożone
            for env in środowiska
            for _numer, _wybór, złożone in self._sposoby(część, dziecko, cechy, env)
        }

    def _przejdź(
        self, production: Production, ciało: tuple[Pozycja, ...], wybór: tuple[Klasa | None, ...]
    ) -> set[Cechy]:
        """Cechy, z jakimi ta produkcja wychodzi nad tymi córkami; pusty zbiór, gdy z żadnymi.

        Środowisko przechodzi ciało od lewej, tak jak przechodzi je wyprowadzenie:
        zmienna wiązana przy pierwszej córce zawęża to, co wolno drugiej.
        """
        środowiska = {EMPTY}
        for część, dziecko, klasa in zip(production.body, ciało, wybór, strict=True):
            środowiska = self._dołóż(część, dziecko, klasa or (), środowiska)
            if not środowiska:
                return set()
        return {frozenset(features_of(production, env).items()) for env in środowiska}

    # -- liczba czytań ------------------------------------------------------ #

    def ile_czytań(self) -> int:
        """Ile czytań ma zdanie: suma po klasach korzenia, bez wyliczania drzew."""
        return sum(self.klasy(self.korzeń).values())

    # -- zatrzymanie -------------------------------------------------------- #

    def najdalszy(self) -> int:
        """Dokąd doszła jakakolwiek analiza częściowa, czyli na czym odrzucenie stanęło.

        Liczy się przejście terminalem, bo bloker ma nazwać formę z tego miejsca zdania,
        a czym jest tu analiza częściowa, mówi :meth:`_przed_formą`.
        """
        if self._najdalszy is not None:
            return self._najdalszy
        if self.klasy(self.korzeń):
            # Czytanie sięga przez całe zdanie, więc dalej niż jego koniec nie ma gdzie.
            self._najdalszy = self._tablica.koniec
            return self._najdalszy
        najdalszy = self._tablica.początek
        for k, (production, kropka, źródło) in self._przed_formą():
            terminal = production.body[kropka]
            środowiska = self._prefiks(production, kropka, źródło, k)
            for segment in self._tablica.krawędzie.get(k, ()):
                if segment.end > najdalszy and self._przechodzi(
                    terminal, (k, segment.end), środowiska
                ):
                    najdalszy = segment.end
        self._najdalszy = najdalszy
        return najdalszy

    def _przechodzi(
        self, terminal: Word, rozpiętość: tuple[int, int], środowiska: Iterable[Env]
    ) -> bool:
        """Czy ten terminal przechodzi tę rozpiętość przy którymkolwiek z tych środowisk.

        Pyta o to samo, o co pyta dołożenie córki do ciała,
        więc pyta tym samym: liściem jest tu rozpiętość bez etykiety,
        czyli dokładnie to, czym stoi w ciele.
        """
        return bool(self._dołóż(terminal, Pozycja(None, rozpiętość), (), środowiska))

    def _przed_formą(self) -> Iterator[tuple[int, _Stan]]:
        """Analizy częściowe zatrzymane przed terminalem, pozycja po pozycji od lewej.

        Analizą częściową jest stan pod dwoma warunkami.
        Pierwszy: jego przebyte ciało unifikuje się z czymkolwiek.
        Stan bez ani jednego takiego środowiska w tablicy jest,
        bo ta pyta o cechy dopiero po lesie, a analizą nie jest.
        Drugi: przewidziała go inna analiza częściowa.
        Bez niego wystarczyłoby, że symbolu oczekuje w tym miejscu jakikolwiek stan,
        choćby sam nie był analizą,
        i odrzucenie stawałoby wtedy na formie, do której nie doszedł nikt.

        Przewidywanie ożywia stany tej samej pozycji, w której je czyta,
        więc pozycja przechodzona stan po stanie musiałaby się powtarzać
        do punktu stałego, a każdy stan przechodziłby oba warunki raz na przebieg.
        Kolejka to zdejmuje.
        O żywości rozstrzyga para produkcji i źródła, a nie kropka w ciele,
        więc stany pozycji zebrane są pod taką parą,
        a para wchodzi do kolejki wtedy, kiedy ożywa.
        Symbol ożywia w pozycji wszystkie swoje produkcje naraz,
        a produkcja ma jedną głowę, więc rozwinięcie pilnowane po symbolu
        wpisuje każdą z nich dokładnie raz i sprawdzania duplikatu tu nie ma.
        Pilnowane po produkcji sprawdzałoby go przy każdym kolejnym żądaniu symbolu
        tyle razy, ile ma on produkcji, a ``orzeczenie`` ma ich siedemset;
        tak samo i z tego samego powodu pilnuje tablica (:meth:`_Tablica._przewiduj`).

        Stanu o kropce na zerze tablica nie trzyma (:meth:`_Tablica._rozwiń`),
        a analizą częściową on bywa, bo czeka na pierwszą formę swojego ciała.
        Wychodzi tu więc z pary, a nie z tablicy (:meth:`_zaczyna_się_tu`),
        i pierwszy warunek spełnia zawsze, bo przebyte ciało ma puste.
        """
        żywe = {
            (production, self._tablica.początek)
            for production in self.grammar.for_head(self._tablica.start)
        }
        rozwinięte = {(self._tablica.start, self._tablica.początek)}
        for k in self._tablica.pozycje_grafu:
            kropki: dict[tuple[Production, int], list[int]] = {}
            for production, kropka, źródło in self._tablica.stany[k]:
                if kropka < len(production.body):
                    kropki.setdefault((production, źródło), []).append(kropka)
            kolejka = [para for para in kropki if para in żywe]
            if k == self._tablica.początek:
                # Produkcje symbolu startowego przewiduje początek zdania,
                # a nie stan, więc do kolejki nie wchodzą przez ożywienie.
                kolejka.extend(para for para in żywe if para not in kropki)
            i = 0
            while i < len(kolejka):
                production, źródło = kolejka[i]
                i += 1
                miejsca = kropki.get((production, źródło), ())
                if self._zaczyna_się_tu(production, źródło, k):
                    miejsca = (0, *miejsca)
                for kropka in miejsca:
                    if not self._prefiks(production, kropka, źródło, k):
                        continue
                    część = production.body[kropka]
                    if not isinstance(część, Sym):
                        yield k, (production, kropka, źródło)
                        continue
                    if (część.name, k) in rozwinięte:
                        continue
                    rozwinięte.add((część.name, k))
                    for przewidziana in self.grammar.for_head(część.name):
                        zaczęta = (przewidziana, k)
                        żywe.add(zaczęta)
                        kolejka.append(zaczęta)

    def _zaczyna_się_tu(self, production: Production, źródło: int, k: int) -> bool:
        """Czy ta produkcja czeka w tej pozycji na pierwszą córkę swojego ciała.

        Stanu o kropce na zerze tablica nie trzyma (:meth:`_przed_formą`),
        więc odpowiedź składa się z dwóch pytań o samą produkcję:
        czy zaczyna się w tej pozycji i czy pierwsza część jej ciała
        ma tu od czego się zacząć, czyli czy przechodzi warunek,
        którym tablica odsiewa swoje stany (:meth:`_Tablica.możliwe`).
        """
        return (
            źródło == k
            and bool(production.body)
            and production.body[0] in self._tablica.możliwe(k)
        )

    def _prefiks(
        self, production: Production, kropka: int, źródło: int, k: int
    ) -> frozenset[Env]:
        """Środowiska, z jakimi ta produkcja doszła tu przebytym ciałem.

        To samo pytanie co w :meth:`_przejdź`, zadane o inne miejsce w ciele:
        tam o cechy wychodzące nad ciałem domkniętym,
        a tutaj o środowisko w jego środku,
        bo terminal następujący po córce dostaje jej zawężenie.
        Córka wchodzi tu wszystkimi swoimi klasami naraz,
        bo pytanie nie dotyczy jednego kształtu.
        """
        if kropka == 0:
            return frozenset({EMPTY}) if źródło == k else frozenset()
        klucz = (production, kropka, źródło, k)
        gotowe = self._prefiksy.get(klucz)
        if gotowe is not None:
            return gotowe
        część = production.body[kropka - 1]
        środowiska: set[Env] = set()
        for j, dziecko in self._tablica.stany[k].get((production, kropka, źródło), ()):
            cechy = [] if dziecko.liść else [c for klasa in self.klasy(dziecko) for c in klasa]
            środowiska |= self._dołóż(
                część, dziecko, cechy, self._prefiks(production, kropka - 1, źródło, j)
            )
        self._prefiksy[klucz] = frozenset(środowiska)
        return self._prefiksy[klucz]

    # -- wyliczanie drzew --------------------------------------------------- #

    def czytania(self) -> Iterator[Node]:
        """Czytania jako drzewa, po jednym na kształt.

        Kolejność, w jakiej wychodzą, ustala :meth:`_Tablica.ciała`.

        Każda gałąź kończy się czytaniem,
        bo ``klasy`` odsiały już kombinacje, których unifikacja nie przepuszcza.
        Dlatego urwanie po :data:`MAX_READINGS` kosztuje tyle, ile wypisane drzewa,
        i nic ponad to.
        """
        return self._kształty(self.korzeń)

    def _kształty(self, pozycja: Pozycja) -> Iterator[Node]:
        """Drzewa tego konstytuentu, po jednym na kształt.

        Klasa, której żaden rodzic nie przyjmuje, nie wchodzi (:meth:`_żywe`),
        więc drzew wychodzi tyle, ile czytań ten konstytuent ma w czytaniach zdania:
        kształty pod taką klasą stoją w tablicy,
        a w żadnym czytaniu zdania nie stoją.
        Korzeń przechodzi przez ten odsiew bez straty, bo jego klasy są żywe wszystkie,
        i dlatego czytania zdania idą tą samą drogą.
        """
        żywe = self._żywe()
        for klasa in self.klasy(pozycja):
            if (pozycja, klasa) in żywe:
                yield from self._drzewa(pozycja, klasa, _jedne(klasa), klasa)

    def _drzewa(
        self, pozycja: Pozycja, klasa: Klasa, wymagane: Cechy, dozwolone: Klasa
    ) -> Iterator[Node]:
        """Drzewa tej pozycji, wypuszczające te cechy: po jednym na kształt pod tą klasą.

        Cechy przychodzą z góry, bo tylko rodzic wie, których żąda:
        klasa zbiera wszystkie, na jakie ten kształt przechodzi,
        a ``szynki`` w pozycji dopełniacza przechodzi tam jednym odczytaniem z dwóch.
        Bez tego żądania drzewo pokazywałoby na liściu odczytanie dowolne,
        więc i takie, którego pozycja nad nim nie licencjonuje.

        Drzew jest tyle, ile kształtów, niezależnie od żądanych cech:
        każda kombinacja z tej klasy wypuszcza każde cechy tej klasy,
        bo klasą jest dokładnie zbiór cech tej kombinacji.
        Dwie produkcje o jednym ciele są jednym kształtem, więc wychodzi z nich jedno drzewo,
        i bierzemy tę, która żądane cechy wypuszcza.

        ``dozwolone`` są cechy, jakie ten kształt wolno tu wypuścić, czyli zwykle
        cała klasa, i idą osobno od żądanych, bo osobno od kształtu liczą się
        odczytania form pod nim (:meth:`_wsparte_kształtu`).
        """
        for kombinacja, produkcje in self._krawędzie((pozycja, klasa)).items():
            wsparte = self._wsparte_kształtu(produkcje, kombinacja, dozwolone)
            for production in produkcje:
                wybory = self._wybory_ciała(production, kombinacja, wymagane)
                if wybory is None:
                    continue
                yield from self._z_córek(
                    pozycja, production, kombinacja, _z_odczytaniami(wybory, wsparte), wsparte, ()
                )
                break
            else:
                raise AssertionError(
                    f"{pozycja} nie wypuszcza {_klucz_cech(wymagane)} "
                    "ciałem, które stoi w jej klasie"
                )

    def _z_córek(
        self,
        pozycja: Pozycja,
        production: Production,
        kombinacja: tuple,
        wybory: tuple[Wybór, ...],
        wsparte: tuple[frozenset, ...],
        zebrane: tuple,
    ) -> Iterator[Node]:
        """Drzewa, jakie z tych córek wychodzą, budowane od lewej i po jednym.

        Iloczyn kartezjański z biblioteki materializuje swoje wejścia,
        więc granica z :data:`MAX_READINGS` przestałaby cokolwiek ograniczać:
        zdanie o dziesiątkach tysięcy czytań wypisałoby je wszystkie,
        żeby oddać sześćdziesiąt cztery.
        Tutaj każde drzewo kosztuje osobno.
        """
        if len(zebrane) == len(kombinacja):
            yield Node(
                label=pozycja.label or "",
                children=zebrane,
                span=pozycja.span,
                głowa=production.głowa,
                koszty=production.koszty,
            )
            return
        miejsce = len(zebrane)
        dziecko, córka = kombinacja[miejsce]
        wybór = wybory[miejsce]
        córki = (
            [wybór]
            if dziecko.liść
            else self._drzewa(dziecko, córka, wybór, wsparte[miejsce])
        )
        for drzewo in córki:
            yield from self._z_córek(
                pozycja, production, kombinacja, wybory, wsparte, (*zebrane, drzewo)
            )

    def _wybory_ciała(
        self, production: Production, kombinacja: tuple, wymagane: Cechy
    ) -> tuple[Wybór, ...] | None:
        """Czym jest każda córka w ciele, które wypuszcza te cechy; ``None``, gdy w żadnym.

        Wybór jest jeden na całe ciało, a nie jeden na córkę,
        bo córki wiąże unifikacja:
        odczytanie przymiotnika wybrane przy pierwszej z nich
        zawęża odczytania rzeczownika, który się z nim zgadza,
        i zawęża cechy, jakie ciało wypuszcza w górę.

        Wybór mówi o kształcie i tylko o nim.
        Odczytań forma stąd nie dostaje: dokłada je :func:`_z_odczytaniami`
        w :meth:`_drzewa`, bo nie liczy ich ani ten wybór, ani samo to ciało
        (:meth:`_wsparte_kształtu`).
        """
        klucz = (production, kombinacja, wymagane)
        if klucz not in self._wybory_ciał:
            self._wybory_ciał[klucz] = self._wybierz(
                production, kombinacja, wymagane, 0, frozenset({EMPTY})
            )
        return self._wybory_ciał[klucz]

    def _wsparte_kształtu(
        self, produkcje: tuple[Production, ...], kombinacja: tuple, dozwolone: Klasa
    ) -> tuple[frozenset, ...]:
        """Czym każda córka być może w tym kształcie: suma po ciałach, które go budują.

        Odczytaniem jest kształt (:meth:`Node.signature`), a jeden kształt buduje
        w tej gramatyce kilka ciał, więc forma stoi tu każdym odczytaniem, które
        licencjonuje ją w którymkolwiek z nich.
        Ciało wybrane, pytane samo, odpowiada tylko za swoje odczytania:
        ``człon_imienny`` robi grupę imienną z jednej formy trzema ciałami —
        rzeczownikowym, odsłownikowym i zaimkowym — więc bez sumy pod
        dopełnieniem `Znam to polecenie.` wychodzi sam odsłownik `polecieć`,
        a rzeczownik `polecenie` nie wychodzi wcale.

        Zawężenia to nie luzuje: ``dozwolone`` jest tu tym samym, czym w
        :meth:`_wsparte`, więc ciało, które przy tych cechach się nie domyka, nie
        dokłada ani jednego odczytania.
        Że suma nie sięga dalej niż kształt, sprawdza ``tests/test_las.py``,
        zawężając zdanie do odczytań, które liście niosą.

        Zapamiętana, bo pyta o nią każde drzewo tej pozycji, czyli nad zdaniem
        wieloznacznym tyle razy, ile ono ma odczytań.
        """
        klucz = (produkcje, kombinacja, dozwolone)
        gotowe = self._wsparcia_kształtów.get(klucz)
        if gotowe is None:
            wsparcia = [
                self._wsparte(production, kombinacja, dozwolone) for production in produkcje
            ]
            gotowe = tuple(
                frozenset().union(*(wsparte[miejsce] for wsparte in wsparcia))
                for miejsce in range(len(kombinacja))
            )
            self._wsparcia_kształtów[klucz] = gotowe
        return gotowe

    def _wsparte(
        self, production: Production, kombinacja: tuple, dozwolone: Klasa
    ) -> tuple[frozenset, ...]:
        """Czym każda córka w tym ciele być może: wpis na córkę, w porządku ciała.

        Liść dostaje zbiór odczytań formy, a konstytuent zbiór cech, jakie
        wypuszcza, czyli to samo, czym jedno i drugie wchodzi do wyboru
        (:data:`Wybór`).

        Wybór córki liczy się wtedy, gdy przechodzi przy którymś środowisku, do
        jakiego ciało dochodzi z lewej, i gdy po nim ciało domyka się jeszcze
        cechami dozwolonymi (:meth:`_domyka`).
        Sprawdzane są wszystkie środowiska, do jakich ciało dochodzi, a nie te z
        jednego przebytego ciała, bo odczytanie odsiane wyborem sąsiada
        wyglądałoby jak odczytanie, którego gramatyka nie bierze.
        Dozwolona jest przy tym cała klasa, a nie cechy żądane od drzewa:
        kształt wypuszcza każde cechy swojej klasy, więc jedne z nich wybrane
        (:func:`_jedne`) odsiałyby odczytania, którymi forma w tym kształcie stoi.
        """
        córki = [
            (production.body[miejsce], dziecko, sorted(klasa, key=_klucz_cech) if klasa else ())
            for miejsce, (dziecko, klasa) in enumerate(kombinacja)
        ]
        przed = [frozenset({EMPTY})]
        for miejsce, (część, dziecko, cechy) in enumerate(córki):
            przed.append(frozenset(self._dołóż(część, dziecko, cechy, przed[miejsce])))
        wynik = []
        for miejsce, (część, dziecko, cechy) in enumerate(córki):
            zebrane = set()
            for env in przed[miejsce]:
                for _numer, wybór, złożone in self._sposoby(część, dziecko, cechy, env):
                    wartość = wybór.reading if isinstance(wybór, Leaf) else wybór
                    if wartość not in zebrane and self._domyka(
                        production, kombinacja, dozwolone, miejsce + 1, złożone
                    ):
                        zebrane.add(wartość)
            wynik.append(frozenset(zebrane))
        return tuple(wynik)

    def _domyka(
        self,
        production: Production,
        kombinacja: tuple,
        dozwolone: Klasa,
        miejsce: int,
        env: Env,
    ) -> bool:
        """Czy ciało domyka się od tego miejsca cechami dozwolonymi, z tego środowiska.

        Pytanie jest o jedno środowisko, a nie o zbiór, i dlatego odpowiedź da
        się zapamiętać: miejsc w ciele jest kilka, a środowisk tyle, ile
        unifikacja przepuszcza, więc pytanie stawiane raz na odczytanie liścia
        powtarza się nad tymi samymi parami.
        """
        klucz = (production, kombinacja, dozwolone, miejsce, env)
        gotowe = self._domknięcia.get(klucz)
        if gotowe is not None:
            return gotowe
        if miejsce == len(kombinacja):
            odpowiedź = frozenset(features_of(production, env).items()) in dozwolone
        else:
            część = production.body[miejsce]
            dziecko, klasa = kombinacja[miejsce]
            cechy = sorted(klasa, key=_klucz_cech) if klasa else ()
            odpowiedź = any(
                self._domyka(production, kombinacja, dozwolone, miejsce + 1, złożone)
                for _numer, _wybór, złożone in self._sposoby(część, dziecko, cechy, env)
            )
        self._domknięcia[klucz] = odpowiedź
        return odpowiedź

    def _wybierz(
        self,
        production: Production,
        kombinacja: tuple,
        wymagane: Cechy,
        miejsce: int,
        środowiska: frozenset[Env],
    ) -> tuple[Wybór, ...] | None:
        """Sposoby od tego miejsca ciała w prawo; ``None``, gdy przy tych środowiskach żadnych.

        Córka wchodzi w tyle sposobów, w ile ją przepuszcza unifikacja:
        konstytuent w tyle, ile cech wypuszcza, a forma w tyle, ile ma tu czytań.
        Sposób, po którym ciała nie da się domknąć żądanymi cechami,
        oddaje ``None`` i nawrót bierze następny,
        bo o cechach wypuszczanych rozstrzyga całe przebyte ciało, a nie jedna córka.
        """
        if miejsce == len(kombinacja):
            domyka = any(
                frozenset(features_of(production, env).items()) == wymagane
                for env in środowiska
            )
            return () if domyka else None
        część = production.body[miejsce]
        dziecko, klasa = kombinacja[miejsce]
        cechy = sorted(klasa, key=_klucz_cech) if klasa else ()
        sposoby: dict[int, tuple[Wybór, set[Env]]] = {}
        for env in środowiska:
            for numer, wybór, złożone in self._sposoby(część, dziecko, cechy, env):
                sposoby.setdefault(numer, (wybór, set()))[1].add(złożone)
        for numer in sorted(sposoby):
            wybór, dalej = sposoby[numer]
            reszta = self._wybierz(
                production, kombinacja, wymagane, miejsce + 1, frozenset(dalej)
            )
            if reszta is not None:
                return (wybór, *reszta)
        return None

    # -- czytanie nazwane rolami z zewnątrz --------------------------------- #

    def numer_czytania(self, role: Mapping[str, frozenset[tuple[int, int]]]) -> int | None:
        """Którym z kolei czytaniem jest to, które przypisuje te role; ``None``, gdy żadnym.

        Pyta ten, kto ma cudze czytanie jednego z tych zdań
        i chce wiedzieć, czy ono w tym lesie ocalało, a jeśli tak, to jak głęboko.
        Numer jest tym, ile odpowiedź „ocalało” jest warta:
        czytanie drugie z dwóch i czytanie tysięczne z dwudziestu ośmiu tysięcy
        ocalały jednakowo, a przeczyta z nich ktoś jedno.

        Rolami, a nie kształtem, bo dwie gramatyki grupują materiał każda po swojemu,
        więc porównanie nawiasów mierzyłoby różnicę między formalizmami.
        Rolę obie orzekają o zdaniu, i tą samą miarą mierzy zgodność
        ``Outcome.agreement`` w ``harness/pomiar.py``, więc obie odpowiedzi mówią o jednym.

        Odpowiedź składa się z dwóch pytań zadanych po kolei i oba są tu potrzebne.
        Czy takie czytanie w lesie jest, mówi las bez wyliczania drzew,
        i po to ta połowa tu jest: lista urywa się na :data:`MAX_READINGS`,
        a zdania wieloznaczne są dokładnie tymi, nad którymi ta granica pada,
        więc czytanie ocalałe za nią wyszłoby z listy przepadłe.
        Którym z kolei jest, mówi dopiero wyliczanie,
        bo numer jest miejscem w kolejności, którą ustala :meth:`_Tablica.ciała`,
        a numer policzony obok byłby tą kolejnością wypisaną drugi raz.

        Wyliczanie rusza więc dopiero po odpowiedzi twierdzącej i na tym czytaniu przystaje,
        czyli kosztuje tyle, ile numer, a nie tyle, ile las ma czytań;
        granica z :data:`MAX_READINGS` nie jest mu przez to potrzebna.
        Ile to kosztuje nad bankiem drzew, mówi
        docs/corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym.

        Zbiór pusty jest żądaniem, a nie jego brakiem:
        etykieta, której pytający nigdzie nie obsadza,
        żąda czytania, które nie obsadza jej również.
        """
        etykiety = tuple(sorted(role))
        żądane: Rozdanie = tuple(frozenset(role[etykieta]) for etykieta in etykiety)
        if not any(
            żądane in self._rozdania((self.korzeń, klasa), etykiety, żądane)
            for klasa in self.klasy(self.korzeń)
        ):
            return None
        for numer, drzewo in enumerate(self.czytania(), 1):
            if _rozdanie_drzewa(drzewo, etykiety) == żądane:
                return numer
        raise AssertionError(
            "las składa to rozdanie ról, a wyliczanie nie wydało drzewa o tym rozdaniu"
        )

    def _rozdania(
        self, para: tuple[Pozycja, Klasa], etykiety: tuple[str, ...], żądane: Rozdanie
    ) -> frozenset[Rozdanie]:
        """Rozdania, jakie czytania tej pary składają, z pominięciem tych ponad żądane.

        Rozdanie pary jest sumą rozdań córek i tego, co para wnosi sama,
        a wnosi rozpiętość wtedy, gdy sama nosi jedną z tych etykiet —
        czyli tyle, ile pod tą parą znajduje :meth:`Node.find`.

        Odsiewamy w trakcie, bo rozdań bywa tyle, ile czytań,
        a po odsianiu najwyżej tyle, ile żądane ma podzbiorów, czyli garść:
        rozdanie z rozpiętością spoza żądanego żądanym już nie zostanie,
        bo suma rozpiętości nie zabiera.
        Odsiew zależy od żądanego, więc żądane wchodzi do klucza spamiętywania.
        """
        klucz = (para, etykiety, żądane)
        gotowe = self._rozdania_pary.get(klucz)
        if gotowe is not None:
            return gotowe
        pozycja, _klasa = para
        własne: Rozdanie = tuple(
            frozenset({pozycja.span}) if pozycja.label == etykieta else frozenset()
            for etykieta in etykiety
        )
        zebrane: set[Rozdanie] = set()
        if not _ponad(własne, żądane):
            for kombinacja in self._krawędzie(para):
                złożone = {własne}
                for dziecko, klasa in kombinacja:
                    if dziecko.liść:
                        continue
                    pod = self._rozdania((dziecko, klasa), etykiety, żądane)
                    złożone = _zsumuj(złożone, pod, żądane)
                    if not złożone:
                        break
                zebrane |= złożone
        self._rozdania_pary[klucz] = frozenset(zebrane)
        return self._rozdania_pary[klucz]

    def _żywe(self) -> set[tuple[Pozycja, Klasa]]:
        """Pary pozycja–klasa, które stoją w którymś czytaniu.

        Schodzimy od korzenia,
        bo tablica domyka i takie pozycje, których żadne czytanie nie przyjmuje,
        a werdykt ma mówić o czytaniach.
        """
        if self._żywe_pary is not None:
            return self._żywe_pary
        żywe: set[tuple[Pozycja, Klasa]] = set()
        stos = [(self.korzeń, klasa) for klasa in self.klasy(self.korzeń)]
        while stos:
            para = stos.pop()
            if para in żywe:
                continue
            żywe.add(para)
            for kombinacja in self._krawędzie(para):
                stos.extend((dziecko, klasa) for dziecko, klasa in kombinacja if not dziecko.liść)
        self._żywe_pary = żywe
        return żywe

    def _rodzicielskie(self) -> dict[tuple[Pozycja, Klasa], set[tuple[Pozycja, Klasa]]]:
        """Para pozycja–klasa → pary, w których ciałach ona stoi.

        Z par żywych, a nie osobnym zejściem od korzenia:
        rodzicem ma być ten, kto sam stoi w którymś czytaniu.
        Liść klucza nie dostaje, bo klasy nie ma i parą lasu nie jest.
        """
        if self._rodzice is not None:
            return self._rodzice
        rodzice: dict[tuple[Pozycja, Klasa], set[tuple[Pozycja, Klasa]]] = {}
        for para in self._żywe():
            for kombinacja in self._krawędzie(para):
                for dziecko, klasa in kombinacja:
                    if not dziecko.liść:
                        rodzice.setdefault((dziecko, klasa), set()).add(para)
        self._rodzice = rodzice
        return rodzice

    def _przedstawiciel(self, pozycja: Pozycja) -> Node:
        """Jedno z drzew tej pozycji, do nazwania jej.

        Nazwać trzeba konstytuent, a nie czytanie, a formy ma on w każdym swoim
        czytaniu te same; różni je podział na segmenty, którego nazwa i tak nie
        pokazuje. Głowa tak daleko nie sięga: ``dobry kod`` jest raz
        przymiotnikiem przed rzeczownikiem, a raz rzeczownikiem z dopełniaczem
        po nim, więc jedna rozpiętość ma tam dwie głowy, a nazwa bierze tę z
        pierwszego drzewa i tego wyboru nie ogłasza.
        """
        gotowe = self._przedstawiciele.get(pozycja)
        if gotowe is not None:
            return gotowe
        for klasa in self.klasy(pozycja):
            for drzewo in self._drzewa(pozycja, klasa, _jedne(klasa), klasa):
                self._przedstawiciele[pozycja] = drzewo
                return drzewo
        raise AssertionError(f"pozycja {pozycja} stoi w lesie bez ani jednego drzewa")
