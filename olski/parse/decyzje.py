"""Decyzje, których czytania nie rozstrzygają: rola, przyłączenie i konstytuent.

Każdą z tych trzech liczy się po lesie, a nie po streszczeniach wypisanych czytań,
bo wpisów ma być tyle, ile decyzji.
Wywód trzyma docs/parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań,
a postać wpisu :class:`Przyłączenie`.

Deklaracja stoi w konstruktorze, bo cała trójka pyta o nią naraz (:func:`podsumuj`).
Bez tego każda pamięć podręczna nosiłaby ją w kluczu,
a dwóch deklaracji nad jednym lasem nikt nie stawia.

Do lasu ten moduł nie pisze i do jego pamięci podręcznych nie sięga;
co ta granica kosztuje, mówi docstring pakietu.
"""

from __future__ import annotations

from itertools import islice

from olski.parse.czytanie import Pozycja
from olski.parse.las import MAX_READINGS, Klasa, Las
from olski.parse.podsumowanie import Deklaracja, Przyłączenie, Rozbieżność
from olski.parse.streszczenie import ciało_koordynuje, sklej_formy, streszczenia


def _wewnątrz(węższa: tuple[int, int], szersza: tuple[int, int]) -> bool:
    """Czy pierwsza rozpiętość mieści się w drugiej; rozpiętość równa mieści się w sobie."""
    return węższa[0] >= szersza[0] and węższa[1] <= szersza[1]


class Decyzje:
    """Trzy podsumowania, które werdykt drukuje obok liczby czytań.

    Który wybór do którego wiersza należy, rozstrzygają między sobą
    (:meth:`_nazwany_gdzie_indziej`), więc pytane osobno
    powtórzyłyby jeden wybór dwoma wierszami.
    """

    def __init__(self, las: Las, deklaracja: Deklaracja) -> None:
        self._las = las
        self._deklaracja = deklaracja
        #: (para, etykieta) → rozpiętości,
        #: jakie pierwszy węzeł tej etykiety pod nią bierze.
        self._pierwsze_role: dict[
            tuple[tuple[Pozycja, Klasa], str], frozenset[tuple[int, int] | None]
        ] = {}
        #: Pozycja → co pod nią widzą dwa pozostałe podsumowania (:meth:`_pod`).
        self._pod_pozycją: dict[Pozycja, tuple[bool, frozenset[int]]] = {}
        #: Pozycje, do których streszczenie zagląda (:meth:`_widoczne`).
        self._widoczne_pozycje: set[Pozycja] | None = None
        #: Pozycje, które streszczenie streszcza osobno (:meth:`_składowe`).
        self._składowe_pozycje: set[Pozycja] | None = None
        #: Wybory przyłączenia, którym werdykt daje wiersz.
        self._nazwane: dict[int, tuple[Pozycja, tuple[str, ...]]] | None = None
        #: Pozycja → ciała, jakimi stoi w czytaniach (:meth:`_ciała_pozycji`).
        self._ciała: dict[Pozycja, set[tuple[Pozycja, ...]]] | None = None

    # -- role, o które czytania się różnią ---------------------------------- #

    def różniące(self) -> tuple[str, ...]:
        """Te z ról, które nie mają w każdym czytaniu tego samego wypełnienia.

        Pytamy las, a nie streszczenia czytań.
        Streszczeń jest najwyżej :data:`MAX_READINGS`,
        a zdanie ustawy ma czytań dziesiątki tysięcy,
        więc rola różniąca się dopiero za tą granicą nie zostałaby nazwana,
        choć liczba obok niej granicy nie ma.

        Jednym wystąpieniem roli jest to, które nazywa :func:`describe`,
        czyli pierwsze w zdaniu składowym i spoza zdań podrzędnych.
        Etykieta pada w czytaniu kilka razy, bo zdanie współrzędne ma własny podmiot,
        a dwa podmioty stojące obok siebie w jednym czytaniu
        nie mówią nic o różnicy między czytaniami.
        Pytamy więc o zdanie całe i o każde jego składowe osobno.
        Bez pytania o składowe werdykt milczy o roli, którą lista czytań rozdziela:
        czytania różne dopiero w składowym drugim mają w pierwszym to samo.
        Bez pytania o zdanie całe milczy o rozcięciu zdania na dwa,
        bo każde składowe niesie wtedy jedną rozpiętość, stojąc w jednym z czytań.
        Iloczynu po składowych stąd nie ma:
        pytanie zadane każdemu osobno kosztuje tyle, ile ich jest,
        a rozpiętości brane naraz mnożyłyby się jak czytania.

        Porównujemy rozpiętości, a nie formy:
        formy nad jedną rozpiętością są w każdym czytaniu te same,
        a różni je podział na segmenty, którego streszczenie i tak nie pokazuje.
        Rozpiętość ``None`` jest czytaniem bez tej roli,
        tak jak streszczenie bez tego klucza.
        """
        składowe = self._składowe()
        return tuple(
            etykieta
            for etykieta in self._deklaracja.role
            if self._niezgodna(self._las.korzeń, etykieta)
            or any(self._niezgodna(pozycja, etykieta) for pozycja in składowe)
        )

    def _niezgodna(self, pozycja: Pozycja, etykieta: str) -> bool:
        """Czy pierwszy węzeł tej etykiety jest pod tą pozycją w kilku miejscach.

        Klasa martwa nie wchodzi, i z tego samego powodu co w :meth:`_ile_kształtów`:
        niezgoda ma być niezgodą między czytaniami.
        Korzenia to nie dotyczyło, bo jego klasy są żywe wszystkie,
        a pozycja zdania składowego bywa i martwa.
        """
        żywe = self._las._żywe()
        wystąpienia = {
            rozpiętość
            for klasa in self._las.klasy(pozycja)
            if (pozycja, klasa) in żywe
            for rozpiętość in self._pierwsza_rola((pozycja, klasa), etykieta)
        }
        return len(wystąpienia) > 1

    def _pierwsza_rola(
        self, para: tuple[Pozycja, Klasa], etykieta: str
    ) -> frozenset[tuple[int, int] | None]:
        """Czym bywa pierwszy węzeł tej etykiety pod tą parą; ``None``, gdy go nie ma.

        Ciało przechodzi się od lewej i kończy na pierwszej córce,
        która tę rolę niesie w każdym swoim czytaniu:
        dalsze córki są wtedy za pierwszym wystąpieniem i nie nazywają go.
        Wyborów córek nic nie wiąże, więc suma po nich jest tym, co dają czytania,
        a wyników jest tyle, ile rozpiętości, a nie ile drzew.

        Córkę ze zdaniem podrzędnym mijamy tak jak liść,
        bo rola z jej wnętrza jest rolą tamtego zdania (:attr:`Deklaracja.podrzędne`),
        chyba że ta córka sama jest szukaną rolą:
        okolicznik wyrażony zdaniem jest rolą, w której nazywa się całe zdanie,
        a jego wnętrze zostaje mimo to nieotwarte, tak samo jak w :meth:`Node.find`.
        """
        pozycja, _klasa = para
        if pozycja.label == etykieta:
            return frozenset({pozycja.span})
        klucz = (para, etykieta)
        gotowe = self._pierwsze_role.get(klucz)
        if gotowe is not None:
            return gotowe
        podrzędne = self._deklaracja.podrzędne
        znalezione: set[tuple[int, int] | None] = set()
        for kombinacja in self._las._krawędzie(para):
            bez_roli = True
            for dziecko, klasa in kombinacja:
                if dziecko.liść or (dziecko.label in podrzędne and dziecko.label != etykieta):
                    continue
                pod_córką = self._pierwsza_rola((dziecko, klasa), etykieta)
                znalezione |= pod_córką - {None}
                if None not in pod_córką:
                    bez_roli = False
                    break
            if bez_roli:
                znalezione.add(None)
        self._pierwsze_role[klucz] = frozenset(znalezione)
        return self._pierwsze_role[klucz]

    # -- przyłączenia ------------------------------------------------------- #

    def przyłączenia(self) -> list[Przyłączenie]:
        """Modyfikatory, którym czytania dają więcej niż jednego gospodarza.

        Jeden wpis na wybór, bo tyle wyborów zdanie zostawia.
        Modyfikator występuje w każdym czytaniu raz,
        więc dwóch gospodarzy jednej pozycji to dwa czytania różniące się tym przyłączeniem,
        i zdanie o sześciu wyrażeniach przyimkowych
        daje sześć wpisów wobec sześćdziesięciu czterech czytań.

        Wyborem jest przyimek, a nie pozycja,
        i dlatego pozycje o jednym początku wchodzą tu razem.
        ``w pliku`` i ``w pliku w katalogu`` to dwie pozycje z dwóch różnych czytań,
        a decyzja pod nimi jest jedna: gdzie przyłącza się wyrażenie otwarte przez ``w``.
        Licząc po pozycjach, dostalibyśmy wpis na każdą parę przyimków,
        czyli znów kwadrat zamiast długości zdania.
        """
        wybory = self._nazwane_przyłączenia()
        return [
            Przyłączenie(sklej_formy(self._las._przedstawiciel(pozycja).forms()), nazwy)
            for _początek, (pozycja, nazwy) in sorted(wybory.items())
        ]

    def _nazwane_przyłączenia(self) -> dict[int, tuple[Pozycja, tuple[str, ...]]]:
        """Początek modyfikatora → jego najkrótsza pozycja i głowy, o które czytania się spierają.

        Osobno od :meth:`przyłączenia`, bo pyta o to samo drugi raz :meth:`rozbieżności`:
        wybór nazwany tutaj jest wyborem, którego ona nie ma nazywać po raz drugi.
        """
        if self._nazwane is not None:
            return self._nazwane
        u_kogo: dict[int, set[Pozycja]] = {}
        najkrótsze: dict[int, Pozycja] = {}
        for pozycja in sorted({para[0] for para in self._las._żywe()}, key=lambda p: p.span):
            if pozycja.label != self._deklaracja.rozstrzygany:
                continue
            początek = pozycja.span[0]
            najkrótsze.setdefault(początek, pozycja)
            u_kogo.setdefault(początek, set()).update(self._gospodarze(pozycja))
        znalezione: dict[int, tuple[Pozycja, tuple[str, ...]]] = {}
        for początek, pozycja in sorted(najkrótsze.items()):
            # Etykieta rozstrzyga remis: `W skład rady wchodzą radni w liczbie.`
            # daje gospodarzy `grupa_przymiotnikowa` i `grupa_imienna` o jednej rozpiętości,
            # a zbiór ich nie porządkuje.
            gospodarze_pozycji = sorted(u_kogo[początek], key=lambda p: (p.span, p.label))
            if len(gospodarze_pozycji) < 2:
                continue
            # Dwie pozycje o jednej głowie są jednym wyborem,
            # bo grupa imienna dłuższa o inny modyfikator jest tą samą grupą imienną.
            nazwy = list(
                dict.fromkeys(
                    self._las._przedstawiciel(gospodarz).forma_głowy()
                    for gospodarz in gospodarze_pozycji
                )
            )
            if len(nazwy) < 2:
                continue
            znalezione[początek] = (pozycja, tuple(nazwy))
        self._nazwane = znalezione
        return znalezione

    def _gospodarze(self, pozycja: Pozycja) -> set[Pozycja]:
        """Konstytuenty z :attr:`Deklaracja.gospodarze`, w których ten modyfikator stoi.

        Szukamy w górę, bo pytanie dotyczy tego, co modyfikator określa,
        a nie tego, pod czym się znalazł:
        okolicznik zdania sąsiaduje w drzewie z dopełnieniem, którego nie określa.
        Modyfikator bez żadnego z tych konstytuentów nad sobą określa całe czytanie
        i wychodzi stąd korzeniem, tak samo jak w :func:`_host`.
        """
        gospodarze = self._deklaracja.gospodarze
        znalezione: set[Pozycja] = set()
        obejrzane: set[tuple[Pozycja, Klasa]] = set()
        stos = [para for para in self._las._żywe() if para[0] == pozycja]
        while stos:
            para = stos.pop()
            if para in obejrzane:
                continue
            obejrzane.add(para)
            rodzice = self._las._rodzicielskie().get(para, set())
            if not rodzice:
                znalezione.add(self._las.korzeń)
            for rodzic in rodzice:
                if rodzic[0].label in gospodarze:
                    znalezione.add(rodzic[0])
                else:
                    stos.append(rodzic)
        return znalezione

    # -- rozbieżności poza zasięgiem streszczenia ---------------------------- #

    def rozbieżności(self) -> list[Rozbieżność]:
        """Konstytuenty, którym czytania dają kilka kształtów tam, gdzie streszczenie nie zagląda.

        Jeden wpis na wybór, tak jak w :meth:`przyłączenia`,
        i wyborem jest tu konstytuent o kilku ciałach:
        rozpiętość pozycja ma jedną, więc rozstrzygane jest w takim miejscu to,
        z czego ona się składa, a nie to, gdzie stoi.
        Ciała są po unifikacji, więc wpis dostaje konstytuent,
        który naprawdę czyta się kilkoma sposobami;
        po co werdyktowi ten wiersz, mówi :class:`Rozbieżność`.

        Wykluczenia są trzy, po jednym na wiersz, który werdykt drukuje bez tego
        podsumowania (:meth:`_nazwany_gdzie_indziej`), a po nich zostaje najwęższy
        z konstytuentów: wpis, którego napis obejmuje napis innego wpisu, mówi o tym
        samym słowie i o kilku obok niego, bo wieloznaczność wychodzi w górę.
        ``równych praw kobiet`` czyta się dwoma sposobami przez samo ``równych``,
        a ``równych praw kobiet i mężczyzn`` trzema, i naprawić trzeba jedno słowo.
        """
        kandydaci = [
            pozycja
            for pozycja, ciała in self._ciała_pozycji().items()
            if len(ciała) > 1 and not self._nazwany_gdzie_indziej(pozycja, ciała)
        ]
        wybrani: list[Pozycja] = []
        # Od najkrótszego, żeby każdy kandydat zastał już wybrane wszystko, co
        # obejmuje. Remis rozstrzyga etykieta: dwie pozycje o jednej rozpiętości
        # mówią o tych samych słowach, więc wpis dostaje jedna z nich.
        for pozycja in sorted(kandydaci, key=lambda p: (p.span[1] - p.span[0], p.span, p.label)):
            if not any(_wewnątrz(inny.span, pozycja.span) for inny in wybrani):
                wybrani.append(pozycja)
        return [
            Rozbieżność(
                sklej_formy(self._las._przedstawiciel(pozycja).forms()),
                self._ile_kształtów(pozycja),
                #  Kształtów wyliczamy tyle, ile czytań wylicza się nad zdaniem,
                #  bo granica jest tu z tego samego powodu: wieloznaczność
                #  konstytuentu mnoży się jak wieloznaczność zdania.
                tuple(
                    streszczenia(
                        islice(self._las._kształty(pozycja), MAX_READINGS), self._deklaracja
                    )
                ),
            )
            for pozycja in sorted(wybrani, key=lambda p: (p.span, p.label))
        ]

    def _ile_kształtów(self, pozycja: Pozycja) -> int:
        """Ile czytań ten konstytuent ma w czytaniach zdania.

        Klasa, której żaden rodzic nie przyjmuje, nie wchodzi:
        kształty pod nią stoją w tablicy, a w żadnym czytaniu zdania nie stoją
        (:meth:`Las._żywe`), i liczba obok konstytuenta ma mówić o czytaniach.
        Klasy żywej to nie dotyczy w środku,
        bo klasą jest zbiór cech wypuszczanych,
        więc rodzic przyjmuje każdy kształt z niej albo żaden.
        """
        żywe = self._las._żywe()
        return sum(
            ile for klasa, ile in self._las.klasy(pozycja).items() if (pozycja, klasa) in żywe
        )

    def _nazwany_gdzie_indziej(self, pozycja: Pozycja, ciała: set[tuple[Pozycja, ...]]) -> bool:
        """Czy o wyborze pod tą pozycją mówi już któryś z pozostałych wierszy werdyktu.

        Ciąg współrzędny mówi go nawiasem w napisie roli,
        więc kryterium jest tu to samo, co w :func:`ciało_koordynuje`.
        Rolę nazywa :meth:`różniące`, a gospodarza modyfikatora :meth:`przyłączenia`,
        i oba widzą dokładnie to, co :meth:`_pod` znajduje w ciałach tej pozycji.
        Modyfikator o jednym gospodarzu wiersza tam nie ma,
        więc wybór nad nim zostaje temu podsumowaniu.
        """
        if pozycja.label in self._deklaracja.współrzędne and any(
            ciało_koordynuje(pozycja.label, (dziecko.label for dziecko in ciało)) for ciało in ciała
        ):
            return True
        pod = [self._pod(dziecko) for ciało in ciała for dziecko in ciało]
        if pozycja in self._widoczne() and any(rola for rola, _ in pod):
            return True
        nazwane = set(self._nazwane_przyłączenia())
        return any(przyłączane & nazwane for _rola, przyłączane in pod)

    def _pod(self, pozycja: Pozycja) -> tuple[bool, frozenset[int]]:
        """Co pod tą pozycją, ją samą licząc, widzą dwa pozostałe podsumowania.

        Pierwsza odpowiedź mówi, czy stoi tu rola, którą nazwie :meth:`różniące`,
        i zejście po nią kończy się na zdaniu podrzędnym, bo tam kończy je tamto
        podsumowanie (:attr:`Deklaracja.podrzędne`).
        Druga wylicza początki modyfikatorów, po których liczy wybory
        :meth:`przyłączenia`, i granicy zdania podrzędnego nie zna, bo tamto też jej nie zna.
        Jedno przejście na dwie odpowiedzi, bo obie pytają o to samo wnętrze,
        a różni je tylko miejsce, w którym się zatrzymują.

        Spamiętywanie jest tu bezpieczne bez straży na cykl:
        pozycja stojąca sama pod sobą przerywa :meth:`Las.klasy` wyjątkiem :class:`Cykl`,
        więc pozycje żywe składają się w graf bez cyklu.
        """
        gotowe = self._pod_pozycją.get(pozycja)
        if gotowe is not None:
            return gotowe
        deklaracja = self._deklaracja
        przyłączane = {pozycja.span[0]} if pozycja.label == deklaracja.rozstrzygany else set()
        rola = pozycja.label in deklaracja.role
        # Liść klas nie ma, więc pętla nad nim się nie wykonuje i liść nie potrzebuje warunku.
        for klasa in self._las.klasy(pozycja):
            for kombinacja in self._las._krawędzie((pozycja, klasa)):
                for dziecko, _klasa in kombinacja:
                    rola_pod, przyłączane_pod = self._pod(dziecko)
                    rola = rola or (rola_pod and pozycja.label not in deklaracja.podrzędne)
                    przyłączane |= przyłączane_pod
        self._pod_pozycją[pozycja] = (rola, frozenset(przyłączane))
        return self._pod_pozycją[pozycja]

    def _ciała_pozycji(self) -> dict[Pozycja, set[tuple[Pozycja, ...]]]:
        """Pozycja → ciała, jakimi ona w czytaniach stoi, czyli same krotki córek.

        Klasy z ciała schodzą, bo dwa ciała różne samą klasą córki
        są jednym wyborem tej pozycji i różnym wyborem tamtej córki,
        a wpisów ma być tyle, ile wyborów.
        Liścia nie ma tu ani wśród kluczy, ani w ciele:
        czytaniem liścia jest sama rozpiętość, więc etykiety i ciała nie ma (:class:`Pozycja`).
        """
        if self._ciała is not None:
            return self._ciała
        zebrane: dict[Pozycja, set[tuple[Pozycja, ...]]] = {}
        for para in self._las._żywe():
            for kombinacja in self._las._krawędzie(para):
                ciało = tuple(dziecko for dziecko, _klasa in kombinacja)
                zebrane.setdefault(para[0], set()).add(ciało)
        self._ciała = zebrane
        return zebrane

    def _widoczne(self) -> set[Pozycja]:
        """Pozycje, do których streszczenie zagląda: od korzenia i bez wchodzenia w podrzędne.

        Tą samą drogą chodzi :meth:`Node.find` po drzewie,
        więc pozycja spoza tego zbioru jest pozycją, o której streszczenie milczy.
        Zdanie podrzędne samo do zbioru wchodzi, bo mijane jest jego wnętrze,
        i nie ma to znaczenia: etykietą roli ono nie jest.
        """
        if self._widoczne_pozycje is not None:
            return self._widoczne_pozycje
        podrzędne = self._deklaracja.podrzędne
        znalezione: set[Pozycja] = set()
        stos = [self._las.korzeń]
        while stos:
            pozycja = stos.pop()
            if pozycja in znalezione:
                continue
            znalezione.add(pozycja)
            if pozycja.label in podrzędne:
                continue
            for klasa in self._las.klasy(pozycja):
                for kombinacja in self._las._krawędzie((pozycja, klasa)):
                    stos.extend(dziecko for dziecko, _klasa in kombinacja if not dziecko.liść)
        self._widoczne_pozycje = znalezione
        return znalezione

    def _składowe(self) -> set[Pozycja]:
        """Pozycje zdań składowych, czyli te, które streszczenie streszcza osobno.

        Od korzenia i bez wchodzenia w składowe już znalezione,
        bo składowym ciągu jest zdanie najwyższe w gałęzi,
        i tą samą drogą chodzi po drzewie :func:`_początki_składowych`.
        Pozycje z różnych czytań stoją tu obok siebie i nie zlewają się:
        zdanie, którego czytania rozcinają je w różnych miejscach,
        daje jedną pozycję na każde takie rozcięcie,
        a pytanie o rolę zadaje się każdej z nich osobno.
        """
        if self._składowe_pozycje is not None:
            return self._składowe_pozycje
        składowe = self._deklaracja.składowe
        znalezione: set[Pozycja] = set()
        odwiedzone: set[Pozycja] = set()
        stos = [self._las.korzeń]
        while stos:
            pozycja = stos.pop()
            if pozycja in odwiedzone:
                continue
            odwiedzone.add(pozycja)
            if pozycja.label in składowe:
                znalezione.add(pozycja)
                continue
            for klasa in self._las.klasy(pozycja):
                for kombinacja in self._las._krawędzie((pozycja, klasa)):
                    stos.extend(dziecko for dziecko, _klasa in kombinacja if not dziecko.liść)
        self._składowe_pozycje = znalezione
        return znalezione
