"""Tablica Earleya: rozbiór, z którego powstaje las.

Tablica jest prywatna dla pakietu: pyta ją las (``olski/parse/las.py``) i nikt poza nim,
bo pozycja tablicy jest stanem rozbioru, a czytaniem dopiero to, co las z niej składa.
"""

from __future__ import annotations

from collections.abc import Sequence

from olski.grammar import EMPTY, Grammar, Part, Production, Sym, Word, bierze
from olski.morph import Segment
from olski.parse.czytanie import Pozycja


def _first(segments: Sequence[Segment]) -> int:
    return min((segment.start for segment in segments), default=0)


#: Stan tablicy: produkcja, ile jej ciała już przeszło, i pozycja grafu, w której się zaczęła.
#: Cech w tym nie ma rozmyślnie:
#: stan niosący środowisko cech rozdzieliłby pozycje
#: i policzyłby wyprowadzenia zamiast czytań.
#: Unifikacja przechodzi po tablicy osobno, w :meth:`Las.klasy`.
#: Stanu o kropce na zerze tablica nie trzyma (:meth:`_Tablica._rozwiń`),
#: poza jednym przypadkiem: przy pustym ciele kropka zerowa jest domknięciem,
#: a domknięcia tablica trzyma wszystkie.
_Stan = tuple[Production, int, int]


class _Tablica:
    """Tablica Earleya nad grafem segmentów.

    Earley przyjmuje każdą gramatykę bezkontekstową,
    lewą rekursję i produkcję o pustym ciele włącznie,
    i oddaje las ze współdzielonymi węzłami sam z siebie, bez budowania automatu.
    Dla gramatyki, która się jeszcze zmienia, ten ostatni punkt jest całym argumentem
    (docs/parsowanie.md#earley-wydaje-las-a-glr-zostaje-optymalizacją).

    Segmenty są krawędziami grafu, a nie listą, więc pozycją jest węzeł grafu:
    ``ktoś`` daje naraz jeden segment i trzy,
    a tablica nie musi wybierać między tymi podziałami przed rozbiorem.
    """

    def __init__(self, grammar: Grammar, segments: list[Segment], start: str) -> None:
        missing = grammar.undefined()
        if missing:
            raise ValueError(f"grammar refers to undefined symbols: {', '.join(sorted(missing))}")
        self.grammar = grammar
        self.segments = segments
        self.start = start
        self.krawędzie: dict[int, list[Segment]] = {}
        for segment in segments:
            self.krawędzie.setdefault(segment.start, []).append(segment)
        self.początek = _first(segments)
        self.koniec = max((segment.end for segment in segments), default=0)
        #: (produkcja, kropka, źródło, k) → ciała, jakie się w tym złożyły.
        self._ciała_memo: dict[tuple, tuple[tuple[Pozycja, ...], ...]] = {}
        #: Węzły grafu w kolejności rosnącej, bo krawędź nigdy nie idzie w tył.
        self.pozycje_grafu = sorted(
            {self.początek, self.koniec}
            | {segment.start for segment in segments}
            | {segment.end for segment in segments}
        )
        #: Pozycja grafu → stan → skąd stan tu doszedł,
        #: czyli para pozycji poprzedniej i córki, która je rozdzieliła.
        #: Miejsce każdej pozycji stoi od początku,
        #: bo ``setdefault`` składałby przy każdym wpisie pusty słownik na darmo.
        self.stany: dict[int, dict[_Stan, set[tuple[int, Pozycja]]]] = {
            k: {} for k in self.pozycje_grafu
        }
        #: Pozycja grafu → symbol → część ciała za tym symbolem → stany, które tu czekają.
        #: Pod częścią, bo po niej odsiewa domknięcie (:meth:`_zamknij`);
        #: ciało kończące się tym symbolem stoi pod ``None``, bo odsiewu nie przechodzi.
        self._oczekujące: dict[int, dict[str, dict[Part | None, list[_Stan]]]] = {
            k: {} for k in self.pozycje_grafu
        }
        #: Pozycja grafu → symbole, które się w niej zamknęły o zerowej rozpiętości.
        #: Bez tego produkcja o pustym ciele przepada dla stanu dopisanego po niej,
        #: bo ten nie ma już czego dokończyć.
        self._puste: dict[int, set[str]] = {}
        #: Konstytuenty, o które posunięto już czekające na nie stany (:meth:`_zamknij`).
        #: Nie to samo co domknięte produkcje: tych jest pod jednym konstytuentem kilka,
        #: i czyta je :meth:`domknięte`.
        self._posunięte: set[Pozycja] = set()
        self._zaczynane = grammar.zaczynane()
        #: Pozycja grafu → (symbol, źródło) → produkcje, które się tu domknęły.
        self._domknięcia_memo: dict[int, dict[tuple[str, int], tuple[Production, ...]]] = {}
        #: Pozycja grafu → terminal → krawędzie, które on w niej bierze.
        self._brane_memo: dict[int, dict[Word, tuple[Segment, ...]]] = {}
        #: Pozycja grafu → części ciała, którymi da się w niej zacząć córkę.
        self._możliwe_memo: dict[int, frozenset[Part]] = {}
        self._rozbierz()

    # -- budowanie ---------------------------------------------------------- #

    def _rozbierz(self) -> None:
        for k in self.pozycje_grafu:
            kolejka = list(self.stany[k])
            if k == self.początek:
                # Symbol startowy przewiduje początek zdania, a nie żaden stan.
                self._rozwiń(k, self.start, kolejka)
            i = 0
            while i < len(kolejka):
                self._krok(k, kolejka[i], kolejka)
                i += 1

    def _krok(self, k: int, stan: _Stan, kolejka: list[_Stan]) -> None:
        """Zrób ze stanem to, czego żąda następna część jego ciała.

        Ciało przebyte do końca domyka się, terminal wczytuje formę,
        a symbol się przewiduje.
        Stan przychodzi tu z kolejki pozycji albo wprost z rozwinięcia symbolu
        (:meth:`_rozwiń`), bo pierwszy krok stanu o kropce na zerze
        jest tym samym krokiem, co każdy następny.
        """
        production, kropka, _źródło = stan
        if kropka == len(production.body):
            self._zamknij(k, stan, kolejka)
            return
        część = production.body[kropka]
        if isinstance(część, Word):
            self._wczytaj(k, stan, część)
        else:
            self._przewiduj(k, stan, część, kolejka)

    def _dodaj(self, k: int, stan: _Stan, wstecz: tuple[int, Pozycja] | None) -> bool:
        """Wpisz stan i powiedz, czy jest nowy; wpis powtórzony dokłada samo wstecz.

        Stan, którego następna córka nie ma w tej pozycji od czego się zacząć
        (:meth:`możliwe`), nie wchodzi i liczy się jak powtórzony:
        ciała nie dokończy, więc nie wejdzie do żadnego czytania.
        Odsiew sięga w głąb, bo stan nieprzyjęty nie rozwinie już symbolu,
        na który czekał, a tamten nie rozwinie swoich.
        Stanu o kropce na zerze nie ma tu czego odsiewać, bo do tablicy nie wchodzi;
        odsiewa go tym samym warunkiem :meth:`_rozwiń`.
        Nie zmienia to również odpowiedzi na to, dokąd doszła analiza częściowa
        (:meth:`Las.najdalszy`): tam liczy się przejście po formie wziętej,
        a żadna córka odsianego stanu takiej formy tu nie zaczyna.
        """
        production, kropka, źródło = stan
        if kropka < len(production.body) and production.body[kropka] not in self.możliwe(k):
            return False
        w_pozycji = self.stany[k]
        istniejące = w_pozycji.get(stan)
        if istniejące is None:
            w_pozycji[stan] = set() if wstecz is None else {wstecz}
            return True
        if wstecz is not None:
            istniejące.add(wstecz)
        return False

    def _przewiduj(self, k: int, stan: _Stan, część: Sym, kolejka: list[_Stan]) -> None:
        """Wpisz stan jako oczekujący, a symbol, na który czeka, rozwiń raz.

        Rozwinięcie przy stanie drugim i każdym następnym wpisałoby to samo,
        bo produkcje symbolu są w tej pozycji już rozwinięte.
        Czy symbol był już rozwinięty, mówi lista oczekujących:
        wpisuje się do niej każdy czekający stan, a pierwszy ją zakłada.
        Lista powstaje przed rozwinięciem, bo rozwinięcie schodzi po pierwszych
        córkach i przy gramatyce lewostronnie rekurencyjnej wraca po ten sam symbol.
        """
        production, kropka, _źródło = stan
        po = production.body[kropka + 1] if kropka + 1 < len(production.body) else None
        oczekujące = self._oczekujące[k]
        grupy = oczekujące.get(część.name)
        if grupy is None:
            oczekujące[część.name] = {po: [stan]}
            self._rozwiń(k, część.name, kolejka)
        else:
            grupy.setdefault(po, []).append(stan)
        if część.name in self._puste.get(k, ()):
            self._posuń(k, [stan], k, Pozycja(część.name, (k, k)), kolejka)

    def _rozwiń(self, k: int, symbol: str, kolejka: list[_Stan]) -> None:
        """Rozwiń symbol przewidziany w tej pozycji: każdą jego produkcję od pierwszej córki.

        Stan o kropce na zerze do tablicy nie wchodzi, bo nie niesie nic
        poza zapisem, że produkcję w tej pozycji przewidziano,
        a zapis ten niosą już :attr:`_oczekujące` wraz z produkcjami symbolu.
        Produkcja zaczynana terminalem przechodzi więc od razu formą,
        a zaczynana symbolem wchodzi wprost na listę oczekujących,
        i tablica trzyma same stany, które już coś przeszły.
        Produkcję, której pierwsza córka nie ma w tej pozycji od czego się zacząć,
        odsiewa tu ten sam warunek, jakim odsiewa stany :meth:`_dodaj`.

        Zejście po pierwszych córkach jest rekurencyjne,
        a głębokie najwyżej na liczbę symboli gramatyki,
        bo każde piętro rozwija inny symbol: rozwiniętego drugi raz się nie rozwija.

        Ciało puste jest wyjątkiem i do tablicy wchodzi,
        bo tam kropka zerowa jest domknięciem, a domknięcia czyta :meth:`domknięte`.

        Pytanie o pierwszą córkę pada raz na jej kształt, a nie raz na produkcję:
        produkcje ma symbol pogrupowane po tej córce
        (:meth:`Grammar.po_pierwszej_części`), a ``orzeczenie`` ma ich setki
        przy rząd wielkości mniejszej liczbie różnych początków.
        """
        grupy = self.grammar.po_pierwszej_części().get(symbol)
        if not grupy:
            return
        możliwe = self.możliwe(k)
        for część, produkcje in grupy.items():
            if część is None:
                for production in produkcje:
                    stan = (production, 0, k)
                    if self._dodaj(k, stan, None):
                        self._krok(k, stan, kolejka)
            elif część in możliwe:
                for production in produkcje:
                    self._krok(k, (production, 0, k), kolejka)

    def _wczytaj(self, k: int, stan: _Stan, terminal: Word) -> None:
        """Przejdź każdą krawędzią grafu, którą ten terminal bierze."""
        production, kropka, źródło = stan
        for segment in self._brane(k).get(terminal, ()):
            self._dodaj(
                segment.end,
                (production, kropka + 1, źródło),
                (k, Pozycja(None, (k, segment.end))),
            )

    def _brane(self, k: int) -> dict[Word, tuple[Segment, ...]]:
        """Terminal → krawędzie wychodzące z tej pozycji, których czytanie on bierze.

        Pytanie pada z ``EMPTY``, a nie ze środowiskiem rodzeństwa,
        bo stan tablicy cech nie niesie.
        Zawężenie potrafi tylko odsiewać,
        więc na tym etapie tablica przyjmuje co najwyżej za dużo,
        a nadmiar odsiewa potem unifikacja po lesie.
        Odpowiedź nie zależy przez to od stanu,
        a pyta o nią odsiew wszystkich stanów tej pozycji naraz (:meth:`możliwe`),
        więc liczy się ją raz i od razu dla każdego terminala.
        Liczy się przy pierwszym pytaniu, bo do części pozycji rozbiór nie dochodzi.
        Krawędź wchodzi tu raz, choćby terminal brał kilka jej czytań.
        """
        gotowe = self._brane_memo.get(k)
        if gotowe is None:
            zebrane: dict[Word, dict[Segment, None]] = {}
            for segment in self.krawędzie.get(k, ()):
                for reading in segment.readings:
                    pos, cechy = reading.tag.pos, reading.tag.cechy
                    for terminal in self.grammar.terminale_dla(pos):
                        if (
                            bierze(terminal, pos, reading.lemma, segment.lematy, cechy, EMPTY)
                            is not None
                        ):
                            zebrane.setdefault(terminal, {})[segment] = None
            gotowe = self._brane_memo[k] = {
                terminal: tuple(krawędzie) for terminal, krawędzie in zebrane.items()
            }
        return gotowe

    def możliwe(self, k: int) -> frozenset[Part]:
        """Części ciała, którymi w tej pozycji grafu da się zacząć córkę.

        Symbol wchodzi tu przez terminale, od których się zaczyna
        (:meth:`Grammar.zaczynane`), więc jedno pytanie odsiewa i terminal,
        i konstytuent nad nim.

        Nazwa jest bez podkreślenia, bo o ten warunek pyta nie tylko budowanie:
        pyta o niego i las, szukając punktu, na którym stanęło odrzucenie
        (:meth:`Las._zaczyna_się_tu`).
        """
        gotowe = self._możliwe_memo.get(k)
        if gotowe is None:
            gotowe = self._możliwe_memo[k] = self._zaczynane[None].union(
                *(self._zaczynane.get(terminal, ()) for terminal in self._brane(k))
            )
        return gotowe

    def _zamknij(self, k: int, stan: _Stan, kolejka: list[_Stan]) -> None:
        """Posuń o ten konstytuent stany, które na niego czekały; raz na konstytuent.

        Domknięć jest tyle, ile produkcji ten symbol na tej rozpiętości złożyło,
        a konstytuent wychodzi z nich jeden, bo :class:`Pozycja` produkcji nie widzi:
        drugie domknięcie posuwa te same stany o tę samą córkę i dokłada wpis,
        który już stoi. Bez tego warunku schodzi tędy przeszło trzecia część
        wszystkich wpisów do tablicy, bo produkcji ma symbol nawet setki.
        Czytań to nie zabiera: stan domknięty stoi w :attr:`stany` niezależnie
        od tego przejścia, a wyprowadzenia czytają właśnie stany (:meth:`domknięte`).

        Lista oczekujących po pierwszym domknięciu nie rośnie:
        pisze do niej :meth:`_przewiduj` w pozycji ``źródło``,
        a ta jest przy ``k`` dalszym niż ``źródło`` przejechana do końca.
        Przy ``k`` równym ``źródło`` rośnie, a stan dopisany po domknięciu
        posuwa sobie samo :meth:`_przewiduj` przez :attr:`_puste`.

        Stan, którego następna część nie ma tutaj od czego się zacząć, schodzi
        z listy tu, a nie przy wpisywaniu: stany są pod tę część pogrupowane
        (:attr:`_oczekujące`), więc jedno pytanie zdejmuje całą grupę, a bez tego
        schodzi tędy przeszło połowa posuwanych stanów, każdy za cenę wołania.
        Warunek jest ten sam, którym odsiewa :meth:`_dodaj`, i tam zostaje,
        bo tam ma jednego właściciela, a wzięty stąd miałby dwóch.
        """
        production, _kropka, źródło = stan
        symbol = production.head
        if źródło == k:
            self._puste.setdefault(k, set()).add(symbol)
        pozycja = Pozycja(symbol, (źródło, k))
        if pozycja in self._posunięte:
            return
        self._posunięte.add(pozycja)
        grupy = self._oczekujące[źródło].get(symbol)
        if not grupy:
            return
        możliwe = self.możliwe(k)
        czekający = [
            oczekujący
            for po, lista in grupy.items()
            if po is None or po in możliwe
            for oczekujący in lista
        ]
        self._posuń(k, czekający, źródło, pozycja, kolejka)

    def _posuń(
        self, k: int, stany: list[_Stan], j: int, dziecko: Pozycja, kolejka: list[_Stan]
    ) -> None:
        """Posuń każdy z tych stanów o tę córkę."""
        for production, kropka, źródło in stany:
            dalej = (production, kropka + 1, źródło)
            if self._dodaj(k, dalej, (j, dziecko)):
                kolejka.append(dalej)

    # -- czytanie ----------------------------------------------------------- #

    def domknięte(self, symbol: str, źródło: int, k: int) -> tuple[Production, ...]:
        """Produkcje tego symbolu, które doszły do końca ciała na tej rozpiętości.

        Domyka się rzadziej niż co dziesiąta, a pytana o każdą z osobna
        odpowiadałaby tyle razy, ile symbol ma produkcji.
        Odpowiedź składa się więc raz na pozycję grafu, z jej własnych stanów,
        i kosztuje potem jedno spojrzenie do słownika.
        Pozycję liczymy przy pierwszym pytaniu, bo o część pozycji nie pyta nikt.

        Kolejność jest kolejnością stanów tablicy, a nie gramatyki, więc czytania
        o równym koszcie porządkuje u wołającego numer produkcji
        (:meth:`Grammar.numery`).
        """
        gotowe = self._domknięcia_memo.get(k)
        if gotowe is None:
            zebrane: dict[tuple[str, int], list[Production]] = {}
            for production, kropka, skąd in self.stany[k]:
                if kropka == len(production.body):
                    zebrane.setdefault((production.head, skąd), []).append(production)
            gotowe = self._domknięcia_memo[k] = {
                klucz: tuple(produkcje) for klucz, produkcje in zebrane.items()
            }
        return gotowe.get((symbol, źródło), ())

    def ciała(
        self, production: Production, kropka: int, źródło: int, k: int
    ) -> tuple[tuple[Pozycja, ...], ...]:
        """Ciała, jakimi ta produkcja doszła tutaj: krotki pozycji córek.

        Tablica pamięta same krawędzie wstecz, po jednej na córkę,
        więc ciało powstaje ze złożenia ich w łańcuch.
        Krotek jest tyle, na ile sposobów ta produkcja dzieli tu rozpiętość,
        czyli tyle, ile wyprowadzeń mieści jedna pozycja.

        Kolejności nie ustalają, choć wychodzą ze zbioru, a haszowanie napisów
        jest losowane przy starcie: porządkuje je :meth:`Las.wyprowadzenia`,
        i to porządkiem liniowym, więc przebieg drugi wydaje te same czytania.
        """
        if kropka == 0:
            return ((),) if źródło == k else ()
        klucz = (production, kropka, źródło, k)
        gotowe = self._ciała_memo.get(klucz)
        if gotowe is not None:
            return gotowe
        stan = (production, kropka, źródło)
        self._ciała_memo[klucz] = tuple(
            {
                (*prefiks, dziecko)
                for j, dziecko in self.stany[k].get(stan, ())
                for prefiks in self.ciała(production, kropka - 1, źródło, j)
            }
        )
        return self._ciała_memo[klucz]
