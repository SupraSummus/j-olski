"""Zdanie składowe wraz z rolami, które w nim stoją, i grupą orzeczenia nad nimi.

Szyk deklaruje się tu raz, rozwinięciem (``olski/precedencja.py``),
a nie ciałem na każdą kolejność córek:
zdanie mówi, jakie córki bierze, a warunek nad nimi mówi, w jakiej kolejności stoją.
"""

from __future__ import annotations

from olski.cennik import (
    CZASOWNIK_PRZED_PODMIOTEM,
    OPUSZCZONY_PODMIOT,
    WYSUNIĘTE_DOPEŁNIENIE_BEZOKOLICZNIKA,
    WYSUNIĘTY_ORZECZNIK,
)
from olski.grammar import NIE_NIESIE, Grammar, Głowa, Sym, V, Var, nt, word
from olski.precedencja import Rozwinięcie
from olski.subset.deklaracja import (
    CZĄSTKA_ZDANIA,
    ELIPSA,
    FRAZA_BEZOKOLICZNIKOWA_OTWARTA,
    OKOLICZNIK_NARZĘDNIKOWY,
    OKOLICZNIK_PRZYSŁÓWKOWY,
    ORZECZENIE_BEZOSOBOWE,
    ORZECZENIE_RZECZOWNIKOWE,
    ORZECZNIK_ŁĄCZNIKA,
    PARA_WYPEŁNIEŃ,
    SPÓJNIK,
    WTRĄCENIE,
    WTRĄCENIE_MYŚLNIKOWE,
)
from olski.subset.podrzędne import _zamykane
from olski.subset.rama import (
    BEZ_DRUGIEJ,
    DOKŁADANE_PRZYPADKI,
    DRUGA_BIERNIK,
    DRUGA_CELOWNIK,
    RAMA_BEZOSOBOWA,
    _bez_orzecznika,
    _formy_skończone,
    _klasy,
    _poza_orzeczeniem,
)
from olski.subset.słowa import (
    BEZ_CZOŁA,
    BEZ_KOPULI,
    CZĄSTKA_ZWROTNA,
    DOSTAWKA,
    GRUPA_ORZECZENIA_ODWRÓCONA,
    KOPULARNY,
    MYŚLNIK,
    NAWIAS_OTWIERAJĄCY,
    NAWIAS_ZAMYKAJĄCY,
    PREDYKATYW,
    PRZECINEK,
    PRZECZENIA,
    PRZECZENIE,
    PRZYSŁÓWEK,
    RZECZOWNIK_ORZEKAJĄCY,
    SPÓJNIK_ELIPSY,
    SZYKI_CZĄSTKI,
    TRYB_OZNAJMUJĄCY,
    ŁĄCZNIK,
)
from olski.walencja import KOPULA


def _szyki_zdania_składowego(
    grammar: Grammar,
    zdanie: Rozwinięcie,
    cechy_zdania: dict[str, Var],
    czasownik_ramy: Sym,
    dopełnienie: Sym,
    okoliczniki: Sym,
) -> None:
    """Zdanie składowe w każdym szyku, jaki ma, wraz z głowami, które orzekają bez podmiotu."""
    # Części zdania, nazwane raz, bo każda z nich stoi w kilku szykach naraz.
    #
    # Rodzaj przechodzi przez każdy szyk, bo żąda go czas przeszły, i dlatego
    # podmiot jest tu jeden zamiast dwóch; wywód trzyma
    # docs/konstrukcje-gramatyczne/orzeczenie.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku,
    # a niezmiennik pilnuje test w tests/test_orzeczenie.py.
    #
    # Tryb przechodzi przez każdy szyk tą samą drogą i z tego samego powodu: żąda
    # go spójnik, który cząstkę tego trybu niesie sam (:data:`SPÓJNIKI_TRYBU`), a
    # cechy, której konstytuent nie niesie, unifikacja nie sprawdza, więc szyk,
    # który by trybu nie przepuścił, przepuściłby pod taki spójnik każdy tryb.
    podmiot = nt("podmiot", number=V("n"), gender=V("g"), person=V("p"), czoło=BEZ_CZOŁA)
    orzeczenie = nt("grupa_orzeczenia", number=V("n"), gender=V("g"), person=V("p"), tryb=V("t"))
    czasownik = nt("orzeczenie", **cechy_zdania)
    orzecznik_wysunięty = nt("orzecznik", number=V("n"), gender=V("g"), czoło=BEZ_CZOŁA)

    # Orzecznik zgodny, wraz z żądaniem, które stawia czasownikowi. Dwa razy
    # ``nom``, a nie wspólna zmienna, bo rama nie zastępuje pozycji: wspólna
    # zmienna wpuszcza tu kopulę z narzędnikiem. Co ona wtedy przyjmuje nad
    # Składnicą, mierzy docs/walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej.
    orzecznik = nt("orzecznik", valency="nom", number=V("n"), gender=V("g"))
    czasownik_orzecznika = nt(
        "orzeczenie", number=V("n"), gender=V("g"), person=V("p"), valency="nom", tryb=V("t")
    )

    # Kopula po zwinięciu jej w ramę: czasownik, który bierze orzecznik w
    # narzędniku. Osobnego symbolu nie ma, bo rama mówi to samo, a jeden lemat
    # wychodził spod dwóch nazw. Żądanie jest tu na czasowniku, a nie wspólną
    # zmienną z orzecznikiem, i to jest ta sama cena co wyżej.
    kopula = nt(
        "orzeczenie", number=V("n"), gender=V("g"), person=V("p"), valency="inst", tryb=V("t")
    )

    # Czasownik, który bierze bezokolicznik: `może`, `musi`, `chce`. Pozycja `inf`
    # stoi tu wartością, żeby zmienna ramy została wolna dla dopełnienia, które ten
    # bezokolicznik bierze (:data:`FRAZA_BEZOKOLICZNIKOWA_OTWARTA`).
    czasownik_bezokolicznika = nt(
        "orzeczenie",
        number=V("n"),
        gender=V("g"),
        person=V("p"),
        valency="inf",
        negacja=V("z"),
        tryb=V("t"),
    )

    zdanie.dominacja("zdanie_składowe", [podmiot, Głowa(orzeczenie)])

    # Podmiot opuszczony w szyku, w którym za czasownikiem coś stoi: `Liczymy cenę.`
    # Pozycja cennika jest ta sama, co przy dopełnieniu wysuniętym przed czasownik,
    # bo konstrukcja jest ta sama: podmiotu każe szukać w zdaniu obok.
    # Ciało konkuruje tu z `zdanie_składowe → czasownik podmiot`, które płaci
    # `czasownik przed podmiotem`, więc darmowe orzeka, że opuszczenie podmiotu
    # jest zwyklejsze niż podmiot stojący na miejscu.
    # Cenę tej pozycji nad prozą trzyma
    # docs/disambiguation.md#kolejność-czytań-ustala-koszt-i-późne-domknięcie.
    zdanie.dominacja(
        "zdanie_składowe",
        [nt("grupa_orzeczenia", tryb=V("t"))],
        koszty=(OPUSZCZONY_PODMIOT,),
    )

    # Mianownika pojedynczego żąda ten terminal, bo tyle mówi o tej konstrukcji
    # polszczyzna: zwrot ma jedną formę, a każda inna forma tego lematu stoi pod
    # czasownikiem — `nie ma mowy` — i zdaniem tej produkcji nie jest. Dwie cechy,
    # a nie sam przypadek: `mowy` jest u Morfeusza i dopełniaczem pojedynczym, i
    # mianownikiem mnogim, więc warunek na sam przypadek wpuszcza `o których mowy`.
    # Rodzaju nie żąda, bo zgodzić się ten rzeczownik nie ma z czym.
    grammar.rule(
        ORZECZENIE_RZECZOWNIKOWE,
        [Głowa(word("subst", lemma=RZECZOWNIK_ORZEKAJĄCY, case="nom", number="sg"))],
    )

    # Zdanie składowe, w którym ten rzeczownik orzeka. Okolicznik stoi w nim córką
    # żądaną, a nie miejscem wyliczonym, bo kopuła opuszczona żąda tego, o czym
    # mowa, i dlatego rozwinięcie szyku tej deklaracji nie pisze: pisałoby ciało
    # bez okolicznika razem z nim.
    #
    # Ciało drugie stoi pod czołem zdania względnego (``olski/subset/podrzędne.py``),
    # bo tam to wyrażenie jest wysunięte. Co zdjęcie któregoś z dwóch kosztuje, mierzy
    # docs/konstrukcje-gramatyczne/podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat.
    grammar.rule(
        "zdanie_składowe", [Głowa(nt(ORZECZENIE_RZECZOWNIKOWE)), okoliczniki], tryb=TRYB_OZNAJMUJĄCY
    )

    # Zdanie z łącznikiem: `Flaga to płat tkaniny.`, `Parser to nie kompilator.`
    # Czasownika ono nie ma, a które z dwóch grup jest podmiotem, rozstrzygnął
    # pomiar wobec banku drzew:
    # docs/konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim.
    #
    # Zgodności ciało nie żąda i nie ma czego zgadzać: `Lata dziewięćdziesiąte to
    # okres rozwoju.` różni się w liczbie po obu stronach łącznika.
    #
    # Wartości cechy `negacja` ciało z cząstką nie wypuszcza, choć reszta gramatyki
    # wypuszcza ją razem z cząstką (:data:`PRZECZENIA`): czyta tę cechę dopełnienie,
    # a dopełnienia zdanie z łącznikiem nie bierze.
    #
    # Grupa przed łącznikiem jest córką opuszczalną: `To kot.` i `To nie kot.`
    # są polszczyzną. Rozwinięciem szyku, a nie ciałem wypisanym, bo miejsca na
    # okolicznik wylicza tylko ono, a `Był to wczoraj problem.` jest polszczyzną.
    for przeczenie, _ in PRZECZENIA:
        for grupa in ((), (nt(ORZECZNIK_ŁĄCZNIKA),)):
            zdanie.dominacja(
                "zdanie_składowe",
                [*grupa, Głowa(ŁĄCZNIK), *przeczenie, podmiot],
                tryb=TRYB_OZNAJMUJĄCY,
            )
    grammar.rule(ORZECZNIK_ŁĄCZNIKA, [nt("grupa_imienna", case="nom")])

    # Ten sam łącznik przy formie osobowej kopuli, w trzech szykach: `Był to
    # nieforemny chłopak.`, `To są oczywistości.`, `Kot to jest zwierzę.`
    # Przeczenie wchodzi tymi ciałami samo, bo cząstka stoi przy czasowniku.
    #
    # Kopula zgadza się tu z podmiotem, czyli z grupą za łącznikiem, i dopiero to
    # rozstrzyga stronę, której ciało wyżej nie miało czym rozstrzygnąć.
    # Czasownik dowolny dałby przy tym drugie czytanie zdaniu `Czytał to nieforemny
    # chłopak.`, w którym `to` jest dopełnieniem, i to żądanie narzędnika je odsiewa.
    # Narzędnik przy kopuli nie stoi, bo rama jest stanem, a nie zasobem,
    # więc pozycja niewypełniona córki nie żąda.
    #
    # Ciała są trzy, a nie jedno z pozycją opuszczalną, bo cena każdego szyku jest
    # osobną liczbą; ile który kupił, mówi dokument wyżej.
    #
    # Rozwinięciem szyku, tak jak ciała wyżej. Kopula stoi tu samym orzeczeniem,
    # a nie grupą orzeczenia, więc okolicznika nie bierze sama i miejsce obok niej
    # drugim wyprowadzeniem jednego napisu nie jest.
    zdanie.dominacja("zdanie_składowe", [Głowa(kopula), ŁĄCZNIK, podmiot])
    zdanie.dominacja("zdanie_składowe", [ŁĄCZNIK, Głowa(kopula), podmiot])
    zdanie.dominacja(
        "zdanie_składowe",
        [nt(ORZECZNIK_ŁĄCZNIKA), ŁĄCZNIK, Głowa(kopula), podmiot],
    )

    # Głowa, która orzeka bez podmiotu: predykatyw i forma nieosobowa czasownika.
    # Rama i `wypełnienia` są u obu te same, co u czasownika, a różni je to, skąd
    # rama przychodzi: predykatyw ma jedną wpisaną obok listy lematów, a forma
    # nieosobowa bierze ramę swojego lematu tak samo jak forma osobowa
    # (:func:`_klasy`). Orzecznika zgodnego nie ma żadna z tych dwóch ram, bo
    # zgadzać się on nie ma z czym (:func:`_bez_orzecznika`).
    # Cząstka `się` stoi przy formie nieosobowej tak samo jak przy osobowej i pyta
    # o ten sam leksykon zwrotny: `zajmowano się sprawą` jest tym samym
    # czasownikiem co `zajmuje się sprawą`.
    #
    # Wywody trzymają
    # docs/konstrukcje-gramatyczne/orzeczenie.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika oraz
    # docs/konstrukcje-gramatyczne/orzeczenie.md#czasownik-nieosobowy-rządzi-ramą-swojego-lematu.
    forma_przyszła = word("bedzie", number="sg", person="ter")
    for przeczenie, negacja in PRZECZENIA:
        grammar.rule(
            ORZECZENIE_BEZOSOBOWE,
            [*przeczenie, Głowa(PREDYKATYW)],
            valency=RAMA_BEZOSOBOWA,
            negacja=negacja,
            druga=BEZ_DRUGIEJ,
        )
        # Czas przyszły tej głowy, w obu szykach: `Trzeba będzie zmierzyć cenę.`
        # i `Będzie trzeba zmierzyć cenę.` Liczba i osoba stoją wypisane wartością,
        # a nie zmienną, bo predykatyw nie niesie ani jednej, a cechy, której
        # konstytuent nie niesie, unifikacja nie sprawdza: bez tych dwóch wartości
        # `Trzeba będą zmierzyć cenę.` się wyprowadza. Cenę każdego szyku osobno mówi
        # docs/konstrukcje-gramatyczne/orzeczenie.md#forma-bedzie-składa-czas-przyszły-także-z-predykatywem.
        for ciało in (
            [*przeczenie, Głowa(PREDYKATYW), forma_przyszła],
            [*przeczenie, forma_przyszła, Głowa(PREDYKATYW)],
        ):
            grammar.rule(
                ORZECZENIE_BEZOSOBOWE,
                ciało,
                valency=RAMA_BEZOSOBOWA,
                negacja=negacja,
                druga=BEZ_DRUGIEJ,
            )
        for zwrotne, cząstka in ((False, ()), (True, (CZĄSTKA_ZWROTNA,))):
            for warunek, rama, druga in _klasy(zwrotne):
                grammar.rule(
                    ORZECZENIE_BEZOSOBOWE,
                    [*przeczenie, Głowa(word("imps", **warunek)), *cząstka],
                    valency=_bez_orzecznika(rama),
                    negacja=negacja,
                    druga=druga,
                )

    # Zdaniem składowym jest ta głowa wprost, bo `grupa_orzeczenia` ma ciało z podmiotem,
    # którego to zdanie nie ma. Ciała są dwa, a nie jedno, bo zakup ciała bez
    # wypełnienia — `Nie wiadomo.`, `Zgłoszono.` — jest osobną liczbą;
    # `wypełnienia` pustego ciała nie ma, a dodane tam dawałoby je każdemu
    # czasownikowi naraz.
    grammar.rule(
        "zdanie_składowe",
        [
            Głowa(nt(ORZECZENIE_BEZOSOBOWE, valency=V("w"), negacja=V("z"), druga=V("d"))),
            nt("wypełnienia", valency=V("w"), negacja=V("z"), druga=V("d")),
        ],
        tryb=TRYB_OZNAJMUJĄCY,
    )
    grammar.rule("zdanie_składowe", [nt(ORZECZENIE_BEZOSOBOWE)], tryb=TRYB_OZNAJMUJĄCY)

    # Dopełnienie przed głową, która orzeka bez podmiotu: `Usterkę zgłoszono.`
    # Córką zdania, a nie pod `wypełnienia`: tamten symbol stoi w ciele wyżej
    # za głową i tylko tam, a córka zdania dostaje miejsce na okolicznik wyliczone,
    # więc `Usterkę zgłoszono wczoraj` zostawia okolicznik za głową.
    # docs/konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu
    zdanie.dominacja(
        "zdanie_składowe",
        [dopełnienie, Głowa(nt(ORZECZENIE_BEZOSOBOWE, valency=V("w"), negacja=V("z")))],
        tryb=TRYB_OZNAJMUJĄCY,
    )

    # Podmiot, dopełnienie i czasownik w każdym szyku, jaki polszczyzna ma, poza
    # tym jednym, który składa podmiot z orzeczeniem (:func:`_poza_orzeczeniem`).
    # Szyk spoza olskiego ma być wykluczony warunkiem, a nie brakiem produkcji,
    # bo wykluczenia przez przemilczenie zabrania tej gramatyce
    # docs/parsowanie.md#earley-wydaje-las-a-glr-zostaje-optymalizacją,
    # i wykluczony jest tu jeden szyk, który ten warunek wypowiada.
    zdanie.dominacja(
        "zdanie_składowe",
        [podmiot, dopełnienie, Głowa(czasownik_ramy)],
        precedencja=_poza_orzeczeniem,
    )

    # Dopełnienie przed czasownikiem, którego podmiot jest opuszczony: `Cenę
    # liczymy.`, `Ustawienia zapisujemy.` Polszczyzna opuszcza podmiot w każdym
    # szyku, a nie w tym jednym, w którym za czasownikiem nic nie stoi; ten
    # rejestr mówi tym szykiem o swoich konwencjach.
    #
    # Szyku odwrotnego ta deklaracja nie ma z tego samego powodu, dla którego nie
    # ma go deklaracja z podmiotem (:func:`_poza_orzeczeniem`): czasownik wraz z
    # dopełnieniem za nim składa `grupa_orzeczenia`, a zdanie bez podmiotu jest nim samym.
    #
    # Pozycja cennika stoi tu dlatego, że ta deklaracja i deklaracja z podmiotem
    # biorą ten sam napis wszędzie tam, gdzie grupa przed czasownikiem jest
    # mianownikiem i biernikiem naraz: `Program otwierający się psuje.` Zdanie z
    # podmiotem obsadzonym stoi nad zdaniem, które podmiotu każe szukać obok.
    zdanie.dominacja(
        "zdanie_składowe", [dopełnienie, Głowa(czasownik_ramy)], koszty=(OPUSZCZONY_PODMIOT,)
    )

    # Dopełnienie bezokolicznika, wysunięte przed formę osobową, która ten
    # bezokolicznik bierze: `premier większości nie może ruszyć`. Wywód i cenę trzyma
    # docs/konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-bezokolicznika-wysuwa-się-przed-formę-osobową-która-go-bierze.
    #
    # Dopełnienie wchodzi tu tym samym symbolem, co w szykach bez bezokolicznika, i
    # dzieli z nimi obie swoje zmienne. Ramę czyta jednak nie forma osobowa, a
    # bezokolicznik, bo pozycja, którą to dopełnienie zajmuje, jest w jego ramie;
    # przeczenie czyta forma osobowa, bo dopełniacza żąda cząstka stojąca przy niej
    # (docs/konstrukcje-gramatyczne/orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem).
    #
    # Szyk jest jeden, ten wypisany, bo cena każdego jest osobną liczbą, a ten
    # jeden jest szykiem, którego żąda bank drzew.
    zdanie.dominacja(
        "zdanie_składowe",
        [
            podmiot,
            dopełnienie,
            Głowa(czasownik_bezokolicznika),
            nt(FRAZA_BEZOKOLICZNIKOWA_OTWARTA, wysunięte=V("w")),
        ],
        koszty=(WYSUNIĘTE_DOPEŁNIENIE_BEZOKOLICZNIKA,),
    )

    # Czasownik przed podmiotem: Nadchodzi druga rewolucja, Są oni obdarzeni
    # rozumem. Podmiot nie bierze tu własnych dopełnień, więc Zapisuje program
    # ustawienia się nie wyprowadza i żadne zdanie SVO nie konkuruje z czytaniem
    # samego siebie od czasownika. Szyku odwrotnego te dwie deklaracje nie mają
    # z tego samego powodu co deklaracja wyżej.
    #
    # Pozycja cennika mówi to, co szyk: podmiot za czasownikiem stoi pod podmiotem
    # przed nim wszędzie tam, gdzie ten sam napis wychodzi oboma ciałami.
    zdanie.dominacja(
        "zdanie_składowe", [Głowa(czasownik), podmiot], koszty=(CZASOWNIK_PRZED_PODMIOTEM,)
    )
    zdanie.dominacja(
        "zdanie_składowe",
        [Głowa(czasownik_orzecznika), podmiot, orzecznik],
        koszty=(CZASOWNIK_PRZED_PODMIOTEM,),
    )

    # Predykatyw przed swoją kopulą: Wejściem jest zwykły tekst polski, W metodzie
    # Cieszyńskiej najważniejsza jest rozmowa. Lustro reguły OVS, którego
    # predykatyw nie miał, więc ten sam szyk wychodził raz tak, a raz wcale,
    # zależnie od tego, co po czasowniku stoi. Orzecznik stoi tu otwarty, bo oba
    # szyki bank drzew ma, a kopula trzyma ten szyk przy orzeczniku: żądanie
    # narzędnika postawione czasownikowi jest tym, co w tej gramatyce znaczy
    # „kopula”, i wysunięcie należy do niej także wtedy, gdy orzecznik jest zgodny.
    #
    # Warunku precedencji nie dostaje ani ta deklaracja, ani ta nad nią, bo różni
    # je rama, a nie kolejność: kopula żąda narzędnika, a czasownik orzecznika
    # zgodnego żąda mianownika, więc przestawiona jedna z nich wypisałaby szyk,
    # który ma już druga, i jednemu napisowi dałaby dwa wyprowadzenia.
    # Pozycja cennika mówi tu to, co wysunięcie: konstrukcja jest nacechowana. Bez niej
    # `On jest wolny.` wychodzi pierwszym czytaniem z `wolny` w podmiocie, bo oba
    # ciała mają córki tej samej rozpiętości i rozstrzyga między nimi alfabet
    # etykiet. Czytań przy tym nie ubywa i zdanie zostaje wieloznaczne.
    zdanie.dominacja(
        "zdanie_składowe",
        [orzecznik_wysunięty, Głowa(kopula), podmiot],
        koszty=(WYSUNIĘTY_ORZECZNIK,),
    )


def _dostawki_zdania(grammar: Grammar) -> None:
    """Wtrącenie, elipsa i okolicznik, które stają obok gotowego zdania składowego."""
    # Wtrącenie w nawiasie: `Zdanie stoi (docs/subset.md).`, `Cena jest zerowa
    # (niżej).` Wnętrzem jest grupa imienna albo przysłówek, bo tym są te
    # dopowiedzenia: nazwą dokumentu i wskazaniem, gdzie szukać. Przysłówek wchodzi
    # tu terminalem, a nie symbolem swojej roli, bo okolicznikiem zdania w nawiasie
    # nie jest.
    #
    # Pozycje są dwie i żaden napis nie ma ich obu naraz: nawias zamykający zdanie
    # składowe stoi tutaj, a nawias zamykający zdanie względne przed jego
    # przecinkiem stoi w ciele `zdanie_względne` niżej. Zdanie z nawiasem ma przez
    # to jedno czytanie, a nie tyle, ile gospodarzy ma wyrażenie przyimkowe.
    # Dlaczego wolno tu wybrać jedno miejsce, a przy wyrażeniu przyimkowym nie
    # wolno, i co obie pozycje zostawiają na zewnątrz, wywodzi
    # docs/konstrukcje-gramatyczne/zdanie-złożone.md#interpunkcja-obejmująca-cudzysłów-wchodzi-w-grupę-a-nawias-staje-obok-zdania.
    for wnętrze in (nt("grupa_imienna"), PRZYSŁÓWEK):
        grammar.rule(WTRĄCENIE, [NAWIAS_OTWIERAJĄCY, Głowa(wnętrze), NAWIAS_ZAMYKAJĄCY])

    # Wtrącenie w parze myślników (:data:`WTRĄCENIE_MYŚLNIKOWE`): `Zepsute miejsce
    # — w prozie czy w kodzie — nie potrzebuje lepszej wersji.` Miejsce daje mu
    # lista okoliczników (:func:`_lista_okoliczników`), bo tam para stoi w tym
    # rejestrze: w środku zdania, a nie za jego ostatnią córką.
    #
    # Wypełnienia są trzy i cena każdego z nich jest osobną liczbą, więc każde ma
    # swoje ciało. Zdanie składowe w środku pary jest zdaniem — `Program — cena
    # rośnie — zapisuje ustawienia.` — a rolą zostaje mimo to całe wtrącenie, tak
    # samo jak przy nawiasie: para dopowiada obok zdania i pozycji w nim nie
    # wypełnia.
    # Trybu to ciało od zdania w środku nie żąda i żądać nie ma czym: cecha
    # wypisana tu zmienną nie wiąże się z niczym, a wyszłaby z głowy w górę i
    # rozdzielała pozycje lasu bez czytelnika (:data:`NIE_WYPUSZCZANE`).
    for wnętrze in (
        nt("grupa_imienna"),
        nt("wyrażenie_przyimkowe"),
        nt("zdanie_składowe"),
    ):
        grammar.rule(WTRĄCENIE_MYŚLNIKOWE, [MYŚLNIK, Głowa(wnętrze), MYŚLNIK])

    # Człon bez czasownika (:data:`ELIPSA`). Wypełnieniem jest konstytuent, który
    # zajmuje w zdaniu pozycję, a ciała są osobne, po jednym na wypełnienie, bo
    # cena każdego z nich jest osobną liczbą. Przysłówka wśród nich nie ma, bo
    # zmierzono go i nie wyszedł
    # (docs/konstrukcje-gramatyczne/zdanie-złożone.md#człon-bez-czasownika-stoi-za-spójnikiem-który-go-bierze).
    #
    # Cząstka przecząca stoi w ciele parą, bo ten rejestr pisze oba: `a nie
    # zdanie` i `czyli o obiekt`. Dopełniaczem nie rządzi i nie ma czym, bo
    # czasownika pod nią nie ma, więc cechy ``negacja`` to ciało nie niesie.
    #
    # Zdanie nadrzędne biegnie za tym członem — `a nie przypadkiem, i pilnuje go
    # test` — więc przecinek zamykający dokłada :func:`_zamykane`, tak samo jak
    # zdaniom podrzędnym.
    for wnętrze in (nt("grupa_imienna"), nt("grupa_przymiotnikowa"), nt("wyrażenie_przyimkowe")):
        for przeczenie in ((), (PRZECZENIE,)):
            _zamykane(grammar, ELIPSA, [PRZECINEK, SPÓJNIK_ELIPSY, *przeczenie, Głowa(wnętrze)])

    # Oba te konstytuenty dostawiają się do zdania składowego jednym ciałem, bo
    # oba są tym samym: grupą postawioną obok zdania i nazwaną całym napisem.
    # Pętla trzyma je zgodnymi — pozycja dopisana jednemu dochodzi i drugiemu —
    # a osobne ciała dałyby się rozejść po pierwszej takiej pozycji.
    for dostawiony in (WTRĄCENIE, ELIPSA):
        grammar.rule(
            "zdanie_składowe",
            [Głowa(nt("zdanie_składowe", tryb=V("t"))), nt(dostawiony)],
            dostawka=DOSTAWKA,
        )

    # Okolicznik wysunięty przed zdanie. Polszczyzna określa rzeczownik wyrażeniem
    # przyimkowym tylko od tyłu, więc przed zdaniem nie ma rzeczownika, do którego
    # to wyrażenie mogłoby się przyłączyć, i wieloznaczności przyłączenia tu nie ma.
    #
    # Przysłówek dostaje tu ciało wypisane, a nie listę okoliczników, bo `okoliczniki`
    # w tym miejscu dałoby wyrażeniu przyimkowemu drugie wyprowadzenie tego samego
    # kształtu, czyli czytanie, którego nie ma czym odsiać.
    grammar.rule(
        "zdanie_składowe",
        [
            nt("wyrażenie_przyimkowe"),
            Głowa(nt("zdanie_składowe", tryb=V("t"), dostawka=NIE_NIESIE)),
        ],
    )
    # Okolicznik narzędnikowy tej pozycji nie dostaje, choć polszczyzna go tu
    # stawia — `Wieczorem wziął lustro.` — bo grupa wysunięta jest wtedy jedyną
    # grupą przed czasownikiem, tak samo jak w szyku od czasownika i w zdaniu
    # o opuszczonym podmiocie. Rozdziela te czytania morfologia, a nie struktura,
    # więc produkcja nie ma czego zażądać; pomiar odmowny trzyma
    # docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika.
    for przy_zdaniu in (OKOLICZNIK_PRZYSŁÓWKOWY, CZĄSTKA_ZDANIA):
        grammar.rule(
            "zdanie_składowe",
            [nt(przy_zdaniu), Głowa(nt("zdanie_składowe", tryb=V("t"), dostawka=NIE_NIESIE))],
        )


def _podmiot(grammar: Grammar) -> None:
    """Czym bywa podmiot: grupą imienną, bezokolicznikiem albo zdaniem względnym."""
    grammar.rule(
        "podmiot",
        [nt("grupa_imienna", case="nom", number=V("n"), gender=V("g"), person=V("p"))],
        czoło=BEZ_CZOŁA,
    )
    # Zdanie względne bez poprzednika w roli podmiotu: `Kto wchodzi w środek,
    # poprzedniego zdania nie przeczytał.`, `Kto chce liczby dzisiejszej, puszcza
    # narzędzie.` Poprzednika ta konstrukcja nie ma i nie potrzebuje, bo zaimek
    # sam nazywa to, o czym zdanie orzeka, a orzeczenie zgadza się z nim: liczbę i
    # rodzaj wypuszcza więc ten podmiot z rdzenia, którego głową jest jego zaimek.
    #
    # Przecinek stoi w ciele podmiotu, a nie między nim a orzeczeniem, bo zamyka
    # on zdanie względne, tak samo jak w :func:`_zamykane`; osoba jest trzecia,
    # bo zaimek jest zaimkiem trzeciej osoby.
    #
    # Bez wykluczenia z pozycji rzeczownej (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`)
    # konstrukcja ta wyprowadza się ciągiem współrzędnym, którego podmiotem jest
    # ten zaimek, więc pozycja stoi w gramatyce razem z tamtym wykluczeniem.
    grammar.rule(
        "zdanie_względne_bez_poprzednika",
        [Głowa(nt("rdzeń_względny_rzeczowny", number=V("n"), gender=V("g"))), PRZECINEK],
    )
    grammar.rule(
        "podmiot",
        [Głowa(nt("zdanie_względne_bez_poprzednika", number=V("n"), gender=V("g")))],
        person="ter",
        czoło=BEZ_CZOŁA,
    )
    # Dopełnienie wychodzi z pozycją ramy, którą zajmuje, bo tym jest przypadek,
    # który czasownik rządzi: żądanie wobec czasownika stoi więc raz, tutaj, a nie
    # w każdym szyku, w którym dopełnienie stoi.
    #
    # Dopełniacz negacji zajmuje tę samą pozycję ramy, więc jest drugą produkcją
    # dopełnienia, a nie drugą pozycją. Wartość cechy jest tu wypisana, a nie
    # zmienna, bo o przypadku rozstrzyga właśnie ta produkcja.
    grammar.rule(
        "dopełnienie",
        [nt("grupa_imienna", case="acc")],
        valency="acc",
        negacja="aff",
        czoło=BEZ_CZOŁA,
    )
    grammar.rule(
        "dopełnienie",
        [nt("grupa_imienna", case="gen")],
        valency="acc",
        negacja="neg",
        czoło=BEZ_CZOŁA,
    )


def _dopełnienie(grammar: Grammar) -> None:
    """Pozycje ramy, które wypełnia grupa imienna, wraz z tymi, które wpuszcza leksykon."""
    # Dopełnienie w przypadku, którego żąda sam czasownik: `Parser mówi autorowi.`,
    # `Wpis żąda dowodu.` Pozycja jest tu ta sama co wyżej, a różni ją przypadek i
    # to, że wpuszcza ją leksykon, a nie rama domyślna (:data:`DOKŁADANE`), więc
    # forma w celowniku stoi przy tych czasownikach, którym Walenty celownik daje,
    # i nie stoi przy żadnym innym.
    #
    # Przeczenia te dwa ciała nie ogłaszają i nie mają czego: dopełniacz negacji
    # wchodzi w miejsce biernika i tam kończy się jego zasięg
    # (docs/konstrukcje-gramatyczne/orzeczenie.md#negacja-żąda-dopełniacza-i-żąda-go-ponad-bezokolicznikiem),
    # a `nie mówi autorowi` stoi w celowniku tak samo jak `mówi autorowi`. Cechy,
    # której konstytuent nie niesie, unifikacja nie sprawdza, więc oba przypadki
    # stoją przy przeczeniu i bez niego.
    #
    # Dopełniacz z leksykonu i dopełniacz z przeczenia dają jednemu napisowi dwa
    # wyprowadzenia tam, gdzie czasownik bierze oba — `nie żąda dowodu` — a jedno
    # czytanie, bo kształt mają ten sam
    # (docs/subset.md#co-się-liczy-jako-jedno-odczytanie).
    for przypadek in DOKŁADANE_PRZYPADKI:
        grammar.rule(
            "dopełnienie", [nt("grupa_imienna", case=przypadek)], valency=przypadek, czoło=BEZ_CZOŁA
        )

    # Te same cztery pozycje wypełnione zaimkiem zwrotnym (:data:`ZWROTNY`):
    # `Widzę siebie.`, `Nie widzę siebie.` Dwie pierwsze idą z ramy domyślnej i
    # stoją wypisane, bo o przeczeniu mówią to, czego lista pozycji nie mówi;
    # dwie następne są pozycjami dokładanymi i czytają tę samą listę, co ciała z
    # grupą imienną wyżej, żeby przypadek dopisany do leksykonu wszedł tu razem z
    # nimi (:data:`DOKŁADANE_PRZYPADKI`).
    #
    # Mianownika ta część mowy nie ma, więc podmiotu nie ma czym wypełnić.
    for przypadek, rama, negacja in (
        ("acc", "acc", "aff"),
        ("gen", "acc", "neg"),
        *((przypadek, przypadek, None) for przypadek in DOKŁADANE_PRZYPADKI),
    ):
        przeczenie = {} if negacja is None else {"negacja": negacja}
        grammar.rule(
            "dopełnienie",
            [word("siebie", case=przypadek)],
            valency=rama,
            czoło=BEZ_CZOŁA,
            **przeczenie,
        )


def _grupa_orzeczenia(
    grammar: Grammar,
    cechy_zdania: dict[str, Var],
    czasownik_ramy: Sym,
    czasownik_kopuli: Sym,
    dopełnienie: Sym,
) -> None:
    """Czasownik wraz z tym, co bierze, a przy nim `winien` i fraza bezokolicznikowa."""
    # To, co czasownik bierze, jest jednym symbolem, a nie listą ciał, żeby forma
    # osobowa i bezokolicznik niżej dzieliły ją, zamiast nieść każde swoją kopię.
    dopełnienia = nt(
        "wypełnienia",
        number=V("n"),
        gender=V("g"),
        valency=V("w"),
        negacja=V("z"),
        druga=V("d"),
        kopula=V("k"),
    )
    # Orzeczenie z samego czasownika: `Świeca zgasła.`, `Córka krawca nie wróciła.`
    # Kopula stoi poza nim, więc `Parser jest.` się nie wyprowadza
    # (:data:`BEZ_KOPULI`).
    grammar.rule("grupa_orzeczenia", [nt("orzeczenie", **cechy_zdania, kopula=BEZ_KOPULI)])
    # Ta sama cecha idzie tu zmienną wspólną, bo żąda jej wypełnienie, a nie ta
    # produkcja: ciało z samymi okolicznikami ogłasza wartość, a każde ciało
    # z wypełnieniem milczy i zostawia zmienną wolną (`wypełnienia` niżej).
    grammar.rule("grupa_orzeczenia", [Głowa(czasownik_kopuli), dopełnienia])

    # To samo orzeczenie z dopełnieniem przed czasownikiem: `kto go nie używa`,
    # `która to wszystko napędza`. Symbol jest osobny od grupy orzeczenia, a nie jest drugim
    # jego ciałem, i rozstrzyga o tym zdanie główne: ono ma ten szyk już z
    # deklaracji swoich córek (:meth:`Rozwinięcie.dominacja`), więc ciało dopisane
    # tam dałoby `Reguła tekst sprawdza.` drugie wyprowadzenie tego samego
    # kształtu. Bierze go zdanie, którego czoło jest podmiotem, i ono jedno
    # (:func:`_wysunięta_rola`).
    grammar.rule(
        GRUPA_ORZECZENIA_ODWRÓCONA,
        [dopełnienie, Głowa(czasownik_ramy)],
        druga=BEZ_DRUGIEJ,
    )

    # `winien` odmienia się przez rodzaj, a nie przez osobę, więc zdanie, którego
    # jest głową, zgadza się z podmiotem rodzajem, a osobę zostawia temu, co ją
    # zawęża gdzie indziej.
    #
    # Tryb stoi tu wypisany, bo `winien` cząstki trybu nie bierze: `żeby powinien`
    # nie jest polszczyzną, a cechy, której konstytuent nie niesie, unifikacja nie
    # sprawdza, więc orzeczenie milczące o trybie przeszłoby pod każdy spójnik.
    for przeczenie, negacja in PRZECZENIA:
        grammar.rule(
            "grupa_orzeczenia",
            [
                *przeczenie,
                Głowa(word("winien", number=V("n"), gender=V("g"))),
                nt("fraza_bezokolicznikowa", negacja=negacja),
            ],
            tryb=TRYB_OZNAJMUJĄCY,
        )
    # Fraza bezokolicznikowa niesie pozycję ramy, którą zajmuje, tak samo jak
    # dopełnienie i orzecznik, więc żądanie wobec czasownika stoi raz, na niej, a
    # nie w każdym ciele, w którym stoi ona. Łańcuch nie potrzebuje przy tym
    # własnej produkcji, bo fraza_bezokolicznikowa → inf wypełnienia wraca do ciał niżej
    # i ma pomagać pisać wychodzi z tych dwóch.
    #
    # Cząstka zwrotna stoi przy tej głowie tak samo jak przy formie osobowej
    # (:data:`SZYKI_CZĄSTKI`), bo należy do czasownika, a nie do formy, w jakiej on
    # stoi. Klasy walencyjnej to ciało nie pyta, bo dopełnienia nie ma i rama nie ma
    # tu czego licencjonować, więc z leksykonu zwrotnego zostaje sama odmowa kopuli:
    # `być się` czasownikiem nie jest w żadnej formie.
    for zwrotne, przed, za in SZYKI_CZĄSTKI:
        głowa = word("inf", bez_lematu_formy=KOPULA) if zwrotne else word("inf")
        for przeczenie, _ in PRZECZENIA:
            grammar.rule(
                "fraza_bezokolicznikowa", [*przed, *przeczenie, Głowa(głowa), *za], valency="inf"
            )


def _wypełnienia(
    grammar: Grammar, okoliczniki: Sym, dopełnienie: Sym, orzecznik_ramy: Sym
) -> None:
    """Symbol, który czasownik bierze pod sobą, wraz z parą o celowniku w drugiej pozycji."""
    # To, co czasownik bierze: jedno dopełnienie, a okolicznik z obu jego stron.
    # Dopełnienie w bierniku, bezokolicznik i orzecznik — zgodny albo w narzędniku —
    # różnią się tym, którą pozycję ramy zajmują, a nie tym, gdzie stoją, więc każde
    # wychodzi z tych samych czterech ciał: Program zapisuje ustawienia, Linter
    # pomaga pisać dobry kod, Ludzie są wolni, Jan jest nauczycielem. Narzędnik
    # dochodzi przez to do kopuli i do nikogo poza nią, bo tylko jej rama go ma.
    #
    # Cztery ciała są jedną decyzją, a nie dwunastoma, i jest to ta sama decyzja,
    # którą szyki zdania podejmują wyżej: brakująca pozycja okolicznika nie odrzuca
    # zdania, tylko wypuszcza jednym czytaniem takie, które ma dwa przyłączenia,
    # jak Muszę jechać do domu. Rozwinięcie tych czterech ciał nie pisze i pisać
    # nie może, choć odpowiada na to samo pytanie: tam okolicznik staje w jednym
    # miejscu naraz, a tu po obu stronach wypełnienia i po obu naraz.
    #
    # Negację niosą dwa z czterech wypełnień i to wystarcza, żeby niosły ją te
    # produkcje: zmienna, której nie zwiąże ani orzecznik, ani zdanie podrzędne,
    # zostaje wolna i konstytuent wychodzi bez tej cechy, a cechy, której
    # konstytuent nie niesie, rodzic nie sprawdza. Orzecznik narzędnikowy stoi
    # więc przy `nie jest` tak samo jak przy `jest`, i tak stoi go polszczyzna.
    for wypełnienie in (
        dopełnienie,
        nt("fraza_bezokolicznikowa", valency=V("w"), negacja=V("z")),
        orzecznik_ramy,
        nt("zdanie_podrzędne", valency=V("w")),
        nt("zdanie_pytajne", valency=V("w")),
    ):
        for ciało in (
            [wypełnienie],
            [okoliczniki, Głowa(wypełnienie)],
            [Głowa(wypełnienie), okoliczniki],
            [okoliczniki, Głowa(wypełnienie), okoliczniki],
        ):
            grammar.rule("wypełnienia", ciało)

    # Same okoliczniki, czyli czasownik, który pozycji ramy nie wypełnia niczym:
    # `Mieszczanie zabili okna deskami.` ma tu `deskami`, a `Rachunek zwraca się
    # dotąd.` ma `dotąd`.
    #
    # Wartość cechy przychodzi z listy, a nie stoi tu wypisana, bo kopulę zamyka
    # sam narzędnik w tej liście, a nie każdy okolicznik (:data:`BEZ_KOPULI`):
    # `Parser jest narzędziem.` ma odtąd jedno czytanie,
    # a `Cena jest gdzie indziej.` nie traci swojego.
    grammar.rule("wypełnienia", [nt("okoliczniki", kopula=V("k"))], kopula=V("k"))

    # Druga pozycja ramy: dopełnienie w celowniku obok wypełnienia, które pozycję
    # ramy zajmuje. `Parser pokazuje autorowi oba czytania.`, `Parser mówi
    # autorowi, że zdanie czyta się dwojako.`, `Krawiec kazał córce usiąść.`
    #
    # Licencję niesie cecha, a nie pozycja ramy (:data:`DRUGA_CELOWNIK`), i wpuszcza
    # ją osobne zdanie leksykonu, liczone z jednego schematu Walentego
    # (``harness/walenty.py``).
    #
    # Wypełnieniem pary jest biernik wypisany wartością, a nie ``dopełnienie`` ze
    # zmienną: zmienna przecina się z tą samą ramą co celownik, więc wpuszcza tu
    # drugi celownik. Orzecznika w tej krotce nie ma, bo Walenty nie odróżnia go od
    # argumentu narzędnikowego (:data:`harness.walenty.WYPEŁNIENIA`).
    #
    # Szyki są dwa, bo polszczyzna ma oba, a okolicznik staje między członami, bo
    # ten rejestr tak pisze: `pokazuje autorowi w wydruku oba czytania`. Miejsca
    # wokół całej pary wylicza ``wypełnienia`` niżej.
    celownikowe = nt("dopełnienie", valency=DRUGA_CELOWNIK, czoło=BEZ_CZOŁA)
    for wypełnienie in (
        nt("dopełnienie", valency="acc", negacja=V("z"), czoło=BEZ_CZOŁA),
        nt("fraza_bezokolicznikowa", valency=V("w"), negacja=V("z")),
        nt("zdanie_podrzędne", valency=V("w")),
        nt("zdanie_pytajne", valency=V("w")),
    ):
        for ciało in (
            [celownikowe, Głowa(wypełnienie)],
            [celownikowe, okoliczniki, Głowa(wypełnienie)],
            [Głowa(wypełnienie), celownikowe],
            [Głowa(wypełnienie), okoliczniki, celownikowe],
        ):
            grammar.rule(PARA_WYPEŁNIEŃ, ciało, druga=DRUGA_CELOWNIK)

    # Druga para: zdanie podrzędne obok dopełnienia w bierniku. `Kierownik
    # poinformował pracownika, że wniosek został odrzucony.`
    #
    # Obie córki zajmują tu pozycję ramy, a przy celowniku wyżej zajmuje ją jedna z
    # dwóch, i dlatego zdanie leksykonu jest tu węższe: nazywa sąsiada, a nie
    # przemilcza go (``bierze_biernik_przy_zdaniu`` w ``harness/walenty.py``).
    # Licencję niesie ta sama cecha co przy celowniku (:data:`DRUGA_BIERNIK`),
    # a szyk jest jeden, bo zdanie podrzędne niesie swój przecinek i staje za tym,
    # co zdanie nadrzędne mówi bez niego.
    #
    # Negację ogłasza ta produkcja, bo niesie ją tu córka, która głową nie jest:
    # dopełniacz negacji wchodzi w miejsce biernika, a zdanie podrzędne o negacji
    # milczy, więc bez tego ogłoszenia `Nie poinformował firmę, że wniosek został
    # odrzucony.` się wyprowadza.
    grammar.rule(
        PARA_WYPEŁNIEŃ,
        [
            nt("dopełnienie", valency="acc", negacja=V("z"), czoło=BEZ_CZOŁA),
            Głowa(nt("zdanie_podrzędne", valency=V("w"))),
        ],
        druga=DRUGA_BIERNIK,
        negacja=V("z"),
    )

    para = nt(PARA_WYPEŁNIEŃ, valency=V("w"), negacja=V("z"), druga=V("d"))
    for ciało in (
        [para],
        [okoliczniki, Głowa(para)],
        [Głowa(para), okoliczniki],
        [okoliczniki, Głowa(para), okoliczniki],
    ):
        grammar.rule("wypełnienia", ciało)


def _lista_okoliczników(grammar: Grammar, okoliczniki: Sym) -> None:
    """Lista okoliczników przy jednym czasowniku, o dowolnej długości."""
    # Okoliczników bywa więcej niż jeden, bo `postępować wobec innych w duchu
    # braterstwa` ma dwa, a czasownik, który bierze jeden, bierze każdą ich liczbę.
    #
    # Okolicznikiem jest wyrażenie przyimkowe albo przysłówek, więc lista bierze
    # jedno i drugie, a przysłówek dostaje przez nią każdą pozycję, jaką okolicznik
    # w zdaniu ma. Lista jest przy tym płaska, więc `bardzo szybko` wychodzi dwoma
    # okolicznikami zdania obok siebie; ile takich czytań zostaje, mierzy
    # docs/konstrukcje-gramatyczne/okolicznik.md#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę.
    #
    # Cząstka stoi w tej liście obok przysłówka, bo pozycję w zdaniu ma tę samą, i
    # dlatego oba wypisuje jedna pętla; rolą jest przy tym każde z nich osobno,
    # bo cząstka przysłówkiem nie jest (:data:`CZĄSTKA_ZDANIA`).
    #
    # Cechę `kopula` wypuszcza ta lista stamtąd, gdzie stoi w niej okolicznik
    # narzędnikowy, i tylko stamtąd (:data:`BEZ_KOPULI`). Ogon niesie ją zmienną
    # wspólną, bo okolicznik ten bywa w liście drugi: `zwraca się dotąd ręką`.
    ogon = nt("okoliczniki", kopula=V("k"))
    grammar.rule("okoliczniki", [nt("wyrażenie_przyimkowe")])
    grammar.rule("okoliczniki", [Głowa(nt("wyrażenie_przyimkowe")), ogon], kopula=V("k"))
    for przy_zdaniu in (OKOLICZNIK_PRZYSŁÓWKOWY, CZĄSTKA_ZDANIA):
        grammar.rule("okoliczniki", [nt(przy_zdaniu)])
        grammar.rule("okoliczniki", [Głowa(nt(przy_zdaniu)), ogon], kopula=V("k"))
    # Ogona te dwa ciała nie pytają o nic, bo wartość ogłaszają same i ogłaszają ją
    # niezależnie od tego, co stoi w liście za nimi.
    grammar.rule("okoliczniki", [nt(OKOLICZNIK_NARZĘDNIKOWY)], kopula=BEZ_KOPULI)
    grammar.rule(
        "okoliczniki", [Głowa(nt(OKOLICZNIK_NARZĘDNIKOWY)), okoliczniki], kopula=BEZ_KOPULI
    )

    # Spójnik wewnętrzny wchodzi tą samą listą i tyle wystarcza, żeby stanął tam,
    # gdzie go polszczyzna stawia: miejsce na okolicznik wylicza się za każdą
    # córką, a nie przed pierwszą (``olski/precedencja.py``), więc czoła zdania
    # ta lista nie daje. Do pętli wyżej ten symbol przez to nie wchodzi: ona daje
    # także czoło, a czoło dałoby `Cena jest niska, więc gramatyka jest tania.`
    # drugie czytanie tego samego kształtu.
    grammar.rule("okoliczniki", [nt(SPÓJNIK)])
    grammar.rule("okoliczniki", [Głowa(nt(SPÓJNIK)), ogon], kopula=V("k"))

    # Wtrącenie w parze myślników wchodzi tą samą listą, bo pyta o to samo: o
    # miejsce, w którym coś staje obok zdania, nie zajmując w nim pozycji. Lista
    # daje mu przez to każde miejsce, jakie ma okolicznik, i tego ta konstrukcja
    # żąda: para stoi w tym rejestrze między podmiotem a orzeczeniem, za
    # dopełnieniem i na końcu zdania składowego, a wypisane ciało na każde z tych
    # miejsc byłoby drugą deklaracją szyku (``olski/precedencja.py``).
    #
    # Cechy `kopula` to ciało nie ogłasza, tak samo jak przysłówek wyżej: para nie
    # jest narzędnikiem, więc kopuli nie zamyka.
    grammar.rule("okoliczniki", [nt(WTRĄCENIE_MYŚLNIKOWE)])
    grammar.rule("okoliczniki", [Głowa(nt(WTRĄCENIE_MYŚLNIKOWE)), ogon], kopula=V("k"))


def _orzecznik(grammar: Grammar) -> None:
    """Orzecznik zgodny i orzecznik w narzędniku, wraz z liczebnikiem orzekającym."""
    # Pozycja ramy wychodzi z orzecznika, bo tym się te dwa różnią i to na nim stoi
    # ograniczenie wyżej: zgodny bierze każdy czasownik, narzędnikowy kopula.
    # Cechę `czoło` niosą oba ciała po to, żeby szyk z orzecznikiem wysuniętym
    # umiał zażądać orzecznika stojącego na swoim miejscu: bez niej orzecznik
    # wysunięty na czoło pytania wypełniałby także tamten szyk, i `Czym jest
    # parser?` miałoby dwa wyprowadzenia — pytanie oraz zdanie oznajmujące
    # zamknięte pytajnikiem (:data:`BEZ_CZOŁA`).
    grammar.rule(
        "orzecznik",
        [nt("grupa_przymiotnikowa", case="nom", number=V("n"), gender=V("g"))],
        valency="nom",
        czoło=BEZ_CZOŁA,
    )
    grammar.rule("orzecznik", [nt("grupa_imienna", case="inst")], valency="inst", czoło=BEZ_CZOŁA)

    # liczebnik orzekający, czyli zdanie mówiące, ile czegoś jest: `Tory są dwa.`,
    # `Konstrukcje są trzy.` Pozycja jest orzecznikiem zgodnym, a nie ramą, bo
    # liczebnik zgadza się z podmiotem tak samo jak przymiotnik nad nim, i dlatego
    # ta sama para cech idzie zmienną.
    #
    # Ciało jest osobne, a nie liczebnikiem wpuszczonym do grupy przymiotnikowej,
    # bo tamten symbol jest zarazem przydawką (`człon_przymiotnikowy` niżej),
    # a liczebnik ma przy rzeczowniku
    # własne ciała i własne przyłączenie (`człon_imienny` niżej); wpuszczony tam
    # dałby `dwie rzeczy` drugie wyprowadzenie.
    #
    # `congr` stoi tu wartością, bo orzeka sam liczebnik zgodny. Rządzący orzeka
    # innym zdaniem — `Torów jest dwa.` — którego podmiot stoi w dopełniaczu, a
    # orzeczenie nie zgadza się z niczym, więc jest to osobne ciało i osobna
    # liczba; docs/konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-orzeka-o-tym-ile-czegoś-jest trzyma oba.
    grammar.rule(
        "orzecznik",
        [nt("liczebnik", accommodability="congr", case="nom", number=V("n"), gender=V("g"))],
        valency="nom",
        czoło=BEZ_CZOŁA,
    )


def _orzeczenie(grammar: Grammar, okoliczniki: Sym) -> None:
    """Formy czasownika, którymi ten rejestr orzeka, wraz z frazą bezokolicznikową."""
    # Rozkaźnik idzie razem z oznajmującą, bo różni je to, co niosą tagi, a nie
    # to, co mówi ta produkcja.
    #
    # Czasownik zwrotny różni się od formy bez cząstki dwiema rzeczami i tyle też
    # mówi o nim ta pętla: stoi przy nim `się`, a rama bierze się z drugiego
    # leksykonu (:data:`LEMAT_ZWROTNY`). Pozycje cząstki stoją obie przy tej formie
    # (:data:`SZYKI_CZĄSTKI`); przy bezokoliczniku i w oddaleniu od swojej formy
    # cząstka pozycji nie ma.
    #
    # Ramę niosą wszystkie te produkcje, a nie tylko niektóre. Cechy, której
    # konstytuent nie niesie, unifikacja nie sprawdza, więc rama postawiona części
    # czasowników przechodziłaby reszcie za darmo, a żądanie „bądź kopulą” nie
    # byłoby wtedy żądaniem. Po to leksykon ma ramę domyślną.
    #
    # Cząstka przecząca poprzedza formę i nic z tego, co czasownik bierze, przed
    # nią nie stanie, więc przeczenie kosztuje jedną pozycję zamiast pozycji w
    # każdym szyku zdania. Ciało bez cząstki ogłasza przy tym `aff`, bo milczenie
    # przepuściłoby dopełniacz negacji do zdania, które nie przeczy.
    for zwrotne, przed, za in SZYKI_CZĄSTKI:
        for warunek, rama, druga in _klasy(zwrotne):
            for ciało, cechy in _formy_skończone(warunek):
                for przeczenie, negacja in PRZECZENIA:
                    grammar.rule(
                        "orzeczenie",
                        [*przed, *przeczenie, *ciało, *za],
                        valency=rama,
                        negacja=negacja,
                        druga=druga,
                        kopula=KOPULARNY if "inst" in rama else BEZ_KOPULI,
                        **cechy,
                    )

    # Bezokolicznik pyta o ten sam leksykon co forma osobowa i o tę samą stronę
    # jego dwóch: z cząstką `się` o zwrotną, bez cząstki o zwykłą. Pętla jest
    # osobna, bo ciało niesie tu własne dopełnienia, a nie dlatego, że rama byłaby
    # inna.
    #
    # Fraza bez własnej cząstki wypuszcza negację, którą wzięła od dołu, więc
    # `Nie chcę czytać książki` żąda dopełniacza od dopełnienia stojącego pod
    # bezokolicznikiem, i tak samo przez łańcuch dowolnej długości.
    #
    # Fraza z własną cząstką nie wypuszcza tej cechy wcale i tym zamyka
    # przenoszenie: `Program ma nie zapisywać ustawień` przeczy bezokolicznikowi,
    # a forma osobowa nad nim nie przeczy. Nieobecnością cechy broni się tu tak
    # samo jak grupa współrzędna, która rodzaju nie niesie.
    for zwrotne, przed, za in SZYKI_CZĄSTKI:
        for warunek, rama, druga in _klasy(zwrotne):
            #  Klasa bez pary żąda od wypełnienia milczenia, a nie wartości:
            #  drugą pozycję wypuszcza sama para (:data:`PARA_WYPEŁNIEŃ`),
            #  a wypełnienie bez niej tej cechy nie niesie wcale, więc żądanie
            #  wartości :data:`BEZ_DRUGIEJ` przechodziłoby milczeniem i tylko nim.
            #  Czasownik ogłasza tę samą klasę wartością, bo cechę tę niesie
            #  każde jego ciało i milczeniem nie odróżniłby jednej klasy od drugiej.
            żądana = NIE_NIESIE if druga == frozenset({BEZ_DRUGIEJ}) else druga
            grammar.rule(
                "fraza_bezokolicznikowa",
                [
                    *przed,
                    Głowa(word("inf", **warunek)),
                    *za,
                    nt("wypełnienia", valency=rama, negacja=V("z"), druga=żądana),
                ],
                valency="inf",
                negacja=V("z"),
            )
            grammar.rule(
                "fraza_bezokolicznikowa",
                [
                    *przed,
                    PRZECZENIE,
                    Głowa(word("inf", **warunek)),
                    *za,
                    nt("wypełnienia", valency=rama, negacja="neg", druga=żądana),
                ],
                valency="inf",
            )

    # Fraza bezokolicznikowa, która ramy swojego lematu nie zużywa na własną córkę, tylko
    # wypuszcza ją w górę, bo pozycję z tej ramy zajmuje dopełnienie stojące przed
    # formą osobową (:data:`FRAZA_BEZOKOLICZNIKOWA_OTWARTA`).
    #
    # Cząstki przeczącej te ciała nie mają i nie ma jej po co: dopełnienie wysunięte
    # przed formę osobową stoi przed każdym miejscem, w którym cząstka tej frazy by
    # stanęła, więc przeczenie schodzi się z nim przy formie osobowej albo nigdzie.
    #
    # Miejsce na okolicznik jest za głową i nie ma go przed nią, bo tyle gospodarzy
    # ma okolicznik na torze zwykłym: `wypełnienia` bezokolicznika stoi za swoją
    # głową i przed nią nie sięga, więc `nie może ruszyć szybko` ma tam dwóch
    # gospodarzy, a `nie może szybko ruszyć` jednego. Bez miejsca za głową ta
    # pozycja wybierałaby gospodarza przez przeoczenie
    # (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    for warunek, rama, _druga in _klasy(zwrotne=False):
        głowa = Głowa(word("inf", **warunek))
        grammar.rule(FRAZA_BEZOKOLICZNIKOWA_OTWARTA, [głowa], wysunięte=rama)
        grammar.rule(FRAZA_BEZOKOLICZNIKOWA_OTWARTA, [głowa, okoliczniki], wysunięte=rama)
