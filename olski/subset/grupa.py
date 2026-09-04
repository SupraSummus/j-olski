"""Grupa imienna i przymiotnikowa wraz z tym, co przy nich stoi.

Grupa imienna jest tym konstytuentem, o który wieloznaczność przyłączenia się opiera:
wyrażenie przyimkowe dochodzi i do niej, i do zdania nad nią,
a olski tego wyboru nie robi i oddaje go czytelnikowi
(docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).
"""

from __future__ import annotations

from olski.grammar import Grammar, Głowa, Sym, V, nt, word
from olski.subset.deklaracja import (
    CIĄG_PRZYIMKOWY,
    CZĄSTKA_ZDANIA,
    CZŁON_PRZYIMKOWY,
    OKOLICZNIK_NARZĘDNIKOWY,
    OKOLICZNIK_PRZYSŁÓWKOWY,
    SPÓJNIK,
    WYRAŻENIE_PRZYIMKOWE,
)
from olski.subset.słowa import (
    AGREE,
    BEZ_ROZDZIELNEJ,
    CUDZYSŁÓW_OTWIERAJĄCY,
    CUDZYSŁÓW_ZAMYKAJĄCY,
    CZĄSTKA,
    CZĄSTKA_PRZY_LICZEBNIKU,
    CZĄSTKA_ZWROTNA,
    FORMA_POPRZYIMKOWA,
    PIĘCIE,
    PRZECINEK,
    PRZYIMEK,
    PRZYSŁÓWEK,
    PRZYSŁÓWEK_STOPNIA,
    PRZYSŁÓWEK_WZGLĘDNY,
    ROZDZIELNA,
    SPÓJNIK_BEZ_PRZECINKA,
    SPÓJNIK_SKORELOWANY,
    SPÓJNIK_WEWNĘTRZNY,
    ZAIMEK_DZIERŻAWCZY,
    ZAIMEK_PYTAJNO_RZECZOWNY,
    ZAIMEK_PYTAJNO_WZGLĘDNY,
    ZAIMEK_RZECZOWNY,
    ZWROTNY,
)
from olski.walencja import KOPULA


def _przydawka(grammar: Grammar) -> None:
    """Przymiotnik przy rzeczowniku i w orzeczniku, wraz z ciągiem współrzędnym przydawek."""
    # Przymiotnik przy rzeczowniku i przymiotnik w orzeczniku, nazwane raz, bo
    # oba wykluczają ten sam lemat i wykluczenie ma być w każdym ciele to samo.
    #
    # Konstytuentem, a nie słowem, bo przysłówek stopniowany przymiotnik określa:
    # `bardzo duży`, `nieporównanie tańsze`. Symbol stawia tę pozycję raz, zamiast
    # dokładać ją do każdego ciała, w którym przymiotnik stoi, i stawia ją pod
    # przymiotnikiem, a nie obok rzeczownika, którego ten przysłówek nie określa.
    # Cenę tego gospodarza trzyma
    # docs/konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy.
    #
    # Przydawką jest tu także imiesłów, bo stoi on tam, gdzie przymiotnik, i zgadza
    # się tak samo; wywód i cenę trzyma
    # docs/konstrukcje-gramatyczne/grupa-imienna.md#przydawka-imiesłowowa-stoi-tam-gdzie-przymiotnik.
    # Imiesłowy dochodzą dwoma wierszami, a nie jednym terminalem o dwóch częściach
    # mowy, bo cena każdego z nich ma być osobną liczbą. Orzecznik bierze `ppas` i
    # nie bierze `pact`: `Reguła jest sięgająca.` nie jest zdaniem tego rejestru.
    #
    # Imiesłów czynny bierze przy tym cząstkę zwrotną, bo jest formą czasownika,
    # który ją bierze: `program otwierający się`. Wiersz jest osobny i pozycja
    # jedna, za głową, bo tam ją polszczyzna stawia; `program się otwierający`
    # zdaniem tego rejestru nie jest. Bierny jej nie bierze wcale, bo strony
    # biernej czasownik zwrotny nie ma.
    #
    # Bez tego wiersza cząstkę zabiera forma osobowa stojąca za przydawką i
    # `Program otwierający się psuje.` wychodzi jednym czytaniem, z `się psuje`
    # w orzeczeniu, gdzie polszczyzna ma tam dwa: cząstka należy do imiesłowu
    # albo do czasownika, a rozstrzyga o tym znaczenie.
    for symbol, słowo, za in (
        ("człon_przydawki", word("adj", bez_lematu=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE), ()),
        ("człon_przydawki", word("ppas", **AGREE), ()),
        ("człon_przydawki", word("pact", **AGREE), ()),
        ("człon_przydawki", word("pact", bez_lematu_formy=KOPULA, **AGREE), (CZĄSTKA_ZWROTNA,)),
        (
            "przymiotnik_orzecznikowy",
            word({"adj", "ppas"}, bez_lematu=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE),
            (),
        ),
    ):
        grammar.rule(symbol, [Głowa(słowo), *za])
        grammar.rule(symbol, [PRZYSŁÓWEK_STOPNIA, Głowa(słowo), *za])
    przymiotnik = nt("człon_przydawki", **AGREE)

    # Ciąg współrzędny przymiotników przy rzeczowniku: `nowy i tani parser`.
    # Para symboli jest ta sama, co u grupy imiennej, i z tego samego powodu;
    # wywód trzyma docs/subset.md pod „Nothing above a coordination distributes
    # into it”, a cenę każdego ciała
    # docs/konstrukcje-gramatyczne/grupa-imienna.md#przydawka-koordynuje-się-i-rozdziela-rzeczownik-tylko-za-nim.
    #
    # Ogon jest nierozdzielny, bo ciąg mieszany — `warstwy nowe i trzecia
    # i czwarta` — polszczyzną nie jest.
    grammar.rule("przydawka", [przymiotnik], rozdzielna=BEZ_ROZDZIELNEJ)
    zgodny_ogon = nt("przydawka", rozdzielna=BEZ_ROZDZIELNEJ, **AGREE)
    grammar.rule(
        "przydawka",
        [Głowa(przymiotnik), SPÓJNIK_BEZ_PRZECINKA, zgodny_ogon],
        rozdzielna=BEZ_ROZDZIELNEJ,
    )
    grammar.rule(
        "przydawka",
        [Głowa(przymiotnik), PRZECINEK, zgodny_ogon],
        rozdzielna=BEZ_ROZDZIELNEJ,
    )
    # Ciąg rozdzielny, czyli ten, którego człony dzielą między siebie rzeczownik:
    # `warstwy trzecia i czwarta` mówi o dwóch warstwach, a `warstwy nowe i tanie`
    # o warstwach, które są jedno i drugie naraz.
    # Liczba idzie wartością, bo żaden człon jej nie ma: mnogi jest ciąg,
    # a każdy przymiotnik w nim pojedynczy.
    rozdzielny_człon = nt("człon_przydawki", case=V("c"), number="sg", gender=V("g"))
    grammar.rule(
        "przydawka",
        [
            Głowa(rozdzielny_człon),
            SPÓJNIK_BEZ_PRZECINKA,
            nt("przydawka", case=V("c"), number="sg", gender=V("g"), rozdzielna=BEZ_ROZDZIELNEJ),
        ],
        number="pl",
        rozdzielna=ROZDZIELNA,
    )


def _grupa_imienna(grammar: Grammar, przydawka: Sym, przydawka_nierozdzielna: Sym) -> None:
    """Grupa imienna wraz z członem, z którego się składa, i z liczebnikiem w tym członie."""
    grammar.rule("grupa_imienna", [nt("człon_imienny", person=V("p"), **AGREE)])
    # Zdanie względne po grupie imiennej, w liczbie i rodzaju swojego zaimka:
    # `reguła, która rozstrzyga`. Przypadka nie niesie, bo zaimek bierze go z
    # roli, którą zajmuje w zdaniu podrzędnym, a nie od poprzednika.
    #
    # Stoi to tutaj, a nie wśród ciał `człon_imienny`, i nie jest to wybór wygody:
    # na tamtym poziomie produkcja rekurencyjna daje `te [konstrukcje, które
    # stoją]` obok `[te konstrukcje], które stoją`, czyli dwa wyprowadzenia
    # jednej struktury, których nie ma czym odsiać. Cenę tego poziomu — człon
    # lewy zdania względnego nie unosi — nikt nie policzył, a docs/subset.md
    # wywodzi, co zgodność z poprzednikiem odbiera przyłączeniu.
    grammar.rule(
        "grupa_imienna",
        [
            Głowa(nt("człon_imienny", person=V("p"), **AGREE)),
            nt("zdanie_względne", number=V("n"), gender=V("g")),
        ],
    )
    # Poprzednik zaimkowy, czyli druga droga zdania względnego z `co`:
    # `to, co mogło się zepsuć`, `wszystko, co zjadł`, `nikt, kto wchodzi w środek`
    # (`zaimek_względny_rzeczowny`).
    #
    # Poprzednikiem jest tu terminal, a nie grupa imienna, bo zaimek rzeczowny
    # dopełniacza nie bierze
    # (docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem)
    # i przydawki przed sobą nikt tu nie policzył. Lematy schodzą się z dwóch
    # deklaracji obok, zamiast stać trzecią listą, którą rozjeżdża dopisanie do
    # którejkolwiek z nich.
    poprzednik_zaimkowy = word(
        "subst", lemma=ZAIMEK_RZECZOWNY, bez_lematu=ZAIMEK_PYTAJNO_RZECZOWNY, **AGREE
    )
    grammar.rule(
        "człon_imienny",
        [
            Głowa(poprzednik_zaimkowy),
            nt("zdanie_względne_rzeczowne", number=V("n"), gender=V("g")),
        ],
        person="ter",
    )
    # Tytuł i termin w cudzysłowie: `„Zasady techniki prawodawczej”`. Grupa
    # przechodzi przez cudzysłów cała, bo polszczyzna odmienia to, co on obejmuje,
    # wedle roli, w której grupa stanęła: `przepisem „Zasad techniki
    # prawodawczej”` ma dopełniacz w środku, a `Same „Zasady” stoją` mianownik.
    # Cechy idą przez to zmienną wspólną, a nie wypisane wartością.
    #
    # Wnętrzem jest sama grupa imienna, więc `„to nie zdanie”` zostaje na zewnątrz;
    # docs/subset.md trzyma, co jeszcze zostaje i za ile ta pozycja weszła.
    grammar.rule(
        "człon_imienny",
        [
            CUDZYSŁÓW_OTWIERAJĄCY,
            Głowa(nt("grupa_imienna", person=V("p"), **AGREE)),
            CUDZYSŁÓW_ZAMYKAJĄCY,
        ],
    )
    # Rodzaju ciąg współrzędny nie niesie: rodzaj `rozumu i sumienia` polszczyzna
    # rozstrzyga regułami, których unifikacja nie wypowie, a cechy, której fraza
    # nie niesie, nie ma o co zawieść żadna zgodność.
    grammar.rule(
        "grupa_imienna",
        [
            Głowa(nt("człon_imienny", case=V("c"))),
            SPÓJNIK_BEZ_PRZECINKA,
            nt("grupa_imienna", case=V("c")),
        ],
        number="pl",
        person="ter",
    )
    grammar.rule(
        "grupa_imienna",
        [Głowa(nt("człon_imienny", case=V("c"))), PRZECINEK, nt("grupa_imienna", case=V("c"))],
        number="pl",
        person="ter",
    )
    # Ten sam spójnik skorelowany, co na poziomie zdaniowym: `Ani parser, ani
    # linter nie rośnie.`
    #
    # Liczba idzie tu z członu, a nie wartością `pl` jak w dwóch ciałach wyżej:
    # ten ciąg orzeka w liczbie pojedynczej, bo przeczenie rozdziela człony,
    # zamiast je sumować, a mnoga wychodzi z niego wtedy, gdy niosą ją człony
    # (`Ani parsery, ani lintery nie rosną.`).
    grammar.rule(
        "grupa_imienna",
        [
            SPÓJNIK_SKORELOWANY,
            Głowa(nt("człon_imienny", case=V("c"), number=V("n"), gender=V("g"))),
            PRZECINEK,
            SPÓJNIK_SKORELOWANY,
            nt("grupa_imienna", case=V("c")),
        ],
        person="ter",
    )
    # Wyrażenie przyimkowe za całym ciągiem: `pliki i katalogi w tym drzewie`
    # mówi o obu, gdzie ciało wyżej mówi o samych katalogach, bo ciąg wiąże się
    # w prawo i wyrażenie zostaje pod członem ostatnim. Cechy, której konstytuent
    # nie niesie, unifikacja nie sprawdza, więc rodzaju brakującego ciągowi to
    # wyrażenie nie potrzebuje — inaczej niż przydawka, której tamten brak tę
    # pozycję odbiera.
    #
    # Ciała są dwa, po jednym na spójnik i na przecinek, bo spójnik w ciele jest
    # tym, co odróżnia je od `grupa_imienna → grupa_imienna wyrażenie_przyimkowe`;
    # czemu produkcja rekurencyjna nie wchodzi i ile ta pozycja kosztowała, trzyma
    # docs/konstrukcje-gramatyczne/grupa-imienna.md#nothing-above-a-coordination-distributes-into-it.
    for spinacz in (SPÓJNIK_BEZ_PRZECINKA, PRZECINEK):
        grammar.rule(
            "grupa_imienna",
            [
                Głowa(nt("człon_imienny", case=V("c"))),
                spinacz,
                nt("grupa_imienna", case=V("c")),
                nt(WYRAŻENIE_PRZYIMKOWE),
            ],
            number="pl",
            person="ter",
        )

    # Zgodność jest tu samą unifikacją, a nie osobnym sprawdzeniem, i wszystkie te
    # ciała dzielą te same trzy zmienne (:data:`AGREE`). Człon z rzeczownikiem w
    # głowie ogłasza trzecią osobę wprost, bo bez tego ogłoszenia wziąłby go po
    # cichu czasownik w pierwszej.
    grammar.rule(
        "człon_imienny",
        [przydawka_nierozdzielna, Głowa(nt("człon_imienny", **AGREE))],
        person="ter",
    )
    # Głową grupy imiennej jest rzeczownik albo rzeczownik odczasownikowy, więc
    # każda pozycja niżej wychodzi dwoma ciałami, po jednym na głowę. Terminala o
    # dwóch częściach mowy tu nie ma i nie jest to wybór wygody: cena tej głowy ma
    # być osobną liczbą, a sonda różnicowa wycenia ją zdejmowaniem ciał, więc
    # pozycja zlana w jeden terminal nie byłaby żadnym ciałem osobno. Pętla trzyma
    # zarazem oba komplety zgodnymi: pozycja dopisana rzeczownikowi dochodzi tą
    # samą deklaracją i drugiej głowie.
    # docs/subset.md wywodzi, czemu ta głowa jest głową grupy, a nie pozycją ramy.
    #
    # Głowa, która rządzi dopełniaczem, nie jest zaimkiem rzeczownym: bez tego
    # warunku każdy taki zaimek daje grupie imiennej drugie czytanie tego samego
    # kształtu. Warunek stoi w deklaracji pary, a nie w każdym ciele, bo ciał z
    # dopełniaczem pod głową jest kilka, a rzeczownikiem odczasownikowym nie jest
    # żaden z tych zaimków i wykluczać tam nie ma czego;
    # wywód i cenę trzyma docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem.
    for głowa, głowa_dopełniacza in (
        (
            word("subst", bez_lematu=ZAIMEK_PYTAJNO_RZECZOWNY, **AGREE),
            word("subst", bez_lematu=ZAIMEK_RZECZOWNY, **AGREE),
        ),
        (word("ger", bez_lematu=PIĘCIE, **AGREE), word("ger", bez_lematu=PIĘCIE, **AGREE)),
    ):
        grammar.rule("człon_imienny", [głowa], person="ter")
        grammar.rule(
            "człon_imienny",
            [Głowa(głowa_dopełniacza), nt("grupa_imienna", case="gen")],
            person="ter",
        )
        # Przydawkę terminu polszczyzna stawia za rzeczownikiem: `plik
        # konfiguracyjny`, `język polski`. Oba szyki są polszczyzną, więc oba stoją
        # tutaj, a zdanie, które przyjmuje oba czytania, jest wieloznaczne.
        grammar.rule("człon_imienny", [Głowa(głowa), przydawka], person="ter")
        grammar.rule("człon_imienny", [Głowa(głowa), nt("wyrażenie_przyimkowe")], person="ter")
        # Oba szyki przydawki naraz: dobrem wspólnym wszystkich obywateli, zadania
        # ochrony ludności. Bez tej pozycji dopełniacz dochodzi tylko do przymiotnika
        # stojącego przed rzeczownikiem, więc termin nazwany drugim szykiem nie ma
        # wyprowadzenia, a rejestr ustaw nazywa tak swoje terminy zdanie po zdaniu:
        # docs/ustawy.md trzyma, ile ta pozycja tam daje i ile odbiera.
        grammar.rule(
            "człon_imienny",
            [Głowa(głowa_dopełniacza), przydawka, nt("grupa_imienna", case="gen")],
            person="ter",
        )
        # Wyrażenie przyimkowe po rzeczowniku, który już coś przy sobie ma: akcja
        # zbrojna w Strefie Gazy, rozmieszczenie ogrodów działkowych w Polsce,
        # zadania ochrony ludności w gminie. Bez tych trzech pozycji przyłączenie do
        # rzeczownika w takiej grupie nie istnieje, a zdanie wychodzi jednym
        # czytaniem przez czasownik. Trzecia idzie razem z przydawką wyżej: bez niej
        # wyrażenie po takim terminie dochodzi do dopełniacza i do nikogo więcej,
        # czyli gramatyka wybiera przyłączenie, którego wybierać nie ma.
        grammar.rule(
            "człon_imienny", [Głowa(głowa), przydawka, nt("wyrażenie_przyimkowe")], person="ter"
        )
        grammar.rule(
            "człon_imienny",
            [Głowa(głowa_dopełniacza), nt("grupa_imienna", case="gen"), nt("wyrażenie_przyimkowe")],
            person="ter",
        )
        grammar.rule(
            "człon_imienny",
            [
                Głowa(głowa_dopełniacza),
                przydawka,
                nt("grupa_imienna", case="gen"),
                nt("wyrażenie_przyimkowe"),
            ],
            person="ter",
        )
    # Grupa liczebnikowa, w dwóch ciałach, bo polszczyzna ma dwa przyłączenia
    # liczebnika i Morfeusz rozdziela je cechą `accommodability`.
    #
    # liczebnik zgodny stoi jak przymiotnik przy rzeczowniku: `dwie rzeczy`,
    # `cztery wozy`, `oba pliki`.
    #
    # liczebnik rządzący wymaga dopełniacza mnogiego i wypuszcza grupę, której
    # liczba i rodzaj nie są liczbą ani rodzajem żadnego słowa pod nią:
    # `Pięć kobiet przyszło` żąda czasownika w liczbie pojedynczej i rodzaju
    # nijakim, choć `kobiet` jest mnogie i żeńskie. Cechy są tu więc wypisane
    # wartością, a nie zmienną wspólną z córką, tak samo jak w koordynacji niżej,
    # z tą różnicą, że tam wartość opisuje ciąg, a tu przeczy każdemu słowu w
    # środku. Zmienna wspólna wygląda tu poprawnie i odwraca zgodność: przyjmuje
    # `Pięć kobiet przyszły`, którego polszczyzna nie ma.
    # Głową jest liczebnik, tak samo jak pod rzeczownikiem rządzącym
    # dopełniaczem: rządzi on przypadkiem tego, co pod nim stoi.
    #
    # Rodzaj przechodzi z liczebnika na dopełniacz, bo polszczyzna go tam żąda:
    # `pięciu mężczyzn` ma rodzaj męskoosobowy, a `pięć kobiet` żeński, i są to
    # dwie różne formy liczebnika. Cyfry żadne z tych ciał nie bierze i dlaczego,
    # mówi docs/subset.md pod „Cyfry olski nie bierze”, gdzie stoi też pomiar obu.
    #
    # Oba pytają symbolu `liczebnik`, a nie terminala, bo liczebnik złożony
    # przyłącza się wedle członu skrajnie prawego: `dwadzieścia dwa chleby` wedle
    # `dwa`, a `dwadzieścia pięć chlebów` wedle `pięć`. Symbol jest łańcuchem o
    # głowie po prawej i od niej bierze `accommodability`; czego nie bierze i co
    # płaci, mówi
    # docs/konstrukcje-gramatyczne/grupa-imienna.md#liczebnik-złożony-przyłącza-się-wedle-ostatniego-członu.
    grammar.rule("liczebnik", [word("num", accommodability=V("a"), **AGREE)])
    grammar.rule(
        "liczebnik",
        [word("num", **AGREE), Głowa(nt("liczebnik", accommodability=V("a"), **AGREE))],
    )
    # Cząstka przybliżająca przed liczebnikiem: `przeszło sto zdań`. Ciało wchodzi
    # w łańcuch, a nie przed grupę imienną, bo tamtą pozycję cząstka ma już
    # (`człon_imienny → part człon_imienny` niżej), a wpisane tam brałoby oba
    # przyłączenia liczebnika naraz; rozłączności obu list pilnuje
    # :data:`CZĄSTKI_PRZY_LICZEBNIKU`. Cechy idą w górę z liczebnika, tak samo jak
    # w łańcuchu wyżej, więc oba przyłączenia pytają grupy z cząstką tym samym,
    # czym pytają jej bez. Co ta pozycja kupuje i czego nie bierze, mówi
    # docs/konstrukcje-gramatyczne/grupa-imienna.md#cząstkę-przybliżającą-przyłącza-liczebnik-a-nie-grupa-imienna.
    grammar.rule(
        "liczebnik",
        [CZĄSTKA_PRZY_LICZEBNIKU, Głowa(nt("liczebnik", accommodability=V("a"), **AGREE))],
    )
    grammar.rule(
        "człon_imienny",
        [nt("liczebnik", accommodability="congr", **AGREE), Głowa(nt("człon_imienny", **AGREE))],
        person="ter",
    )
    grammar.rule(
        "człon_imienny",
        [
            Głowa(nt("liczebnik", accommodability="rec", case=V("c"), gender=V("g"))),
            nt("grupa_imienna", case="gen", number="pl", gender=V("g")),
        ],
        number="sg",
        gender="n",
        person="ter",
    )

    # Zaimek jest tym jednym członem, który niesie własną osobę, i po to jedno tu
    # stoi: bez niego podmiot w pierwszej i w drugiej osobie nie ma czym być.
    grammar.rule("człon_imienny", [word({"ppron3", "ppron12"}, person=V("p"), **AGREE)])

    # Zaimek dzierżawczy przed grupą imienną: `jego skutki`, `ich cena`
    # (:data:`ZAIMEK_DZIERŻAWCZY`). Zgodności ta pozycja nie ma i mieć nie może:
    # zaimek zgadza się liczbą i rodzajem ze swoim poprzednikiem, a poprzednik stoi
    # w zdaniu obok, więc cechy grupy są cechami samej głowy. Tym różni się to
    # ciało od przymiotnika i od liczebnika zgodnego, które dzielą z głową
    # wszystkie trzy cechy.
    #
    # Ciało jest jedno, bo dopełniacz po rzeczowniku bierze produkcja wyżej.
    # Co ta pozycja kosztuje, mierzy
    # docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-dzierżawczy-jest-dopełniaczem-przed-rzeczownikiem.
    grammar.rule(
        "człon_imienny", [ZAIMEK_DZIERŻAWCZY, Głowa(nt("człon_imienny", **AGREE))], person="ter"
    )

    # Cząstka przed grupą imienną, czyli jej gospodarz drugi: `Nawet ptaki przestały
    # śpiewać.` Kurs, po którym weszła, trzyma
    # docs/konstrukcje-gramatyczne/okolicznik.md#cząstka-ma-dwóch-gospodarzy-i-przy-jednym-dostaje-etykietę.
    #
    # Córką lewą jest terminal, a nie symbol :data:`CZĄSTKA_ZDANIA`: etykieta roli
    # mówiłaby o zdaniu, że ma cząstkę zdania, a ta stoi w grupie.
    #
    # Osobę ta pozycja przepuszcza, a nie ogłasza `ter` jak przymiotnik i zaimek
    # dzierżawczy nad nią, bo cząstka staje i przed zaimkiem
    # (`Nawet ja zapisuję ustawienia.`).
    grammar.rule("człon_imienny", [CZĄSTKA, Głowa(nt("człon_imienny", person=V("p"), **AGREE))])


def _grupa_przymiotnikowa(grammar: Grammar, orzecznikowy: Sym) -> None:
    """Ciąg współrzędny przymiotników, a pod przymiotnikiem narzędnik i wyrażenie przyimkowe."""
    # Grupa przymiotnikowa koordynuje się tak samo i zgadza się przez cały ciąg,
    # więc `wolni i równi` jest jednym orzecznikiem, a `wolna i równi` żadnym.
    człon_przymiotnika = nt("człon_przymiotnikowy", **AGREE)
    ciąg_przymiotników = nt("grupa_przymiotnikowa", **AGREE)
    grammar.rule("grupa_przymiotnikowa", [człon_przymiotnika])
    for spinacz in (SPÓJNIK_BEZ_PRZECINKA, PRZECINEK):
        grammar.rule(
            "grupa_przymiotnikowa", [Głowa(człon_przymiotnika), spinacz, ciąg_przymiotników]
        )
    # Wyrażenie przyimkowe za całym ciągiem przymiotników, czyli ta sama pozycja,
    # którą ciąg grup imiennych dostaje wyżej i z tego samego powodu:
    # `wolni i równi pod względem swej godności` mówi o obu członach, gdzie ciało
    # bez tego wyrażenia zostawia je przy samych równych.
    #
    # Zgodność ciąg przymiotnikowy niesie przez cały siebie, inaczej niż imienny,
    # więc zmienne idą tu przez oba człony (:data:`AGREE`). Zasięgu wyrażenia
    # zgodność nie zawęża, bo żadnej z tych cech ono nie dotyka.
    for spinacz in (SPÓJNIK_BEZ_PRZECINKA, PRZECINEK):
        grammar.rule(
            "grupa_przymiotnikowa",
            [Głowa(człon_przymiotnika), spinacz, ciąg_przymiotników, nt(WYRAŻENIE_PRZYIMKOWE)],
        )
    # Imiesłów bierny jest tu przymiotnikiem i zatrzymuje dopełnienie, którym
    # rządził jego czasownik: `obdarzeni rozumem i sumieniem`.
    grammar.rule("człon_przymiotnikowy", [orzecznikowy])
    grammar.rule("człon_przymiotnikowy", [Głowa(orzecznikowy), nt("grupa_imienna", case="inst")])
    # Trzecie miejsce, do którego wyrażenie przyimkowe dochodzi: powiązani z
    # interesami postkomunistów, przeznaczany na budowę.
    grammar.rule("człon_przymiotnikowy", [Głowa(orzecznikowy), nt("wyrażenie_przyimkowe")])


def _okoliczniki_leksykalne(grammar: Grammar) -> None:
    """Konstytuenty, którymi ten rejestr wyraża okoliczność, wraz z wyrażeniem przyimkowym."""
    # Jeden lemat jest tu wykluczony i wykluczony jest z nazwy
    # (:data:`PRZYIMEK_ROZDZIELAJĄCY`).
    grammar.rule(CZŁON_PRZYIMKOWY, [Głowa(PRZYIMEK), nt("grupa_imienna", case=V("c"))])

    # To samo wyrażenie z zaimkiem zwrotnym pod przyimkiem: `Reguły odsyłają do
    # siebie.` Ciało jest osobne, bo zakup jest osobną liczbą, a przypadek idzie
    # tą samą zmienną, więc przyimek rządzi zaimkiem tak, jak rządzi grupą.
    grammar.rule(CZŁON_PRZYIMKOWY, [Głowa(PRZYIMEK), ZWROTNY])

    # Ciąg współrzędny wyrażeń przyimkowych: `Leksykon mówi o bierniku i o
    # bezokoliczniku.` Poziom jest piąty i ostatni z tych, które polszczyzna
    # koordynuje, a olski miał cztery
    # (docs/konstrukcje-gramatyczne/grupa-imienna.md#nothing-above-a-coordination-distributes-into-it).
    #
    # Symbole są trzy. Człon i ciąg nad nim wybrano dla liczby czytań, tak samo jak
    # przy grupie imiennej (dokument wyżej). Trzeci jest rolą i stoi nad ciągiem,
    # bo ogon ciągu pod nazwą roli wychodziłby drugim wyborem przyłączenia,
    # którego streszczenie czytania nie wypisuje.
    #
    # Przypadka nie wypuszcza ani człon, ani ciąg — rządzi nim przyimek, a nie to,
    # co ciąg zajmuje (:data:`NIE_WYPUSZCZANE`) — więc dwa człony pod różnymi
    # przyimkami stoją w jednym ciągu.
    #
    # Spinacze są dwa, po jednym ciele na każdy, tak samo jak na czterech poziomach
    # obok, i cena każdego jest osobną liczbą. Przecinek bierze przy tym zarazem
    # zawężenie — `Działa w Polsce, w okolicach Kielc.` — czyli apozycję, której
    # olski nie ma, i jest to ta sama zamiana co na poziomie imiennym; ile który
    # spinacz kupuje, mierzy
    # docs/konstrukcje-gramatyczne/grupa-imienna.md#wyrażenie-przyimkowe-koordynuje-się-tak-jak-grupa-imienna.
    grammar.rule("wyrażenie_przyimkowe", [nt(CIĄG_PRZYIMKOWY)])
    grammar.rule(CIĄG_PRZYIMKOWY, [nt(CZŁON_PRZYIMKOWY)])
    for spinacz in (SPÓJNIK_BEZ_PRZECINKA, PRZECINEK):
        grammar.rule(
            CIĄG_PRZYIMKOWY,
            [Głowa(nt(CZŁON_PRZYIMKOWY)), spinacz, nt(CIĄG_PRZYIMKOWY)],
        )

    # Przysłówek zdania jako konstytuent, a nie jako słowo w liście okoliczników,
    # bo bez tego symbolu okolicznik przysłówkowy nie ma węzła, który werdykt nazwie
    # (:data:`OKOLICZNIK_PRZYSŁÓWKOWY`).
    grammar.rule(OKOLICZNIK_PRZYSŁÓWKOWY, [PRZYSŁÓWEK])
    # Przysłówek przed przysłówkiem, czyli gospodarz trzeci: `bardzo szybko`.
    # Stopnia żąda od córki lewej z tego samego powodu, z którego żąda go pozycja
    # przy przymiotniku: `tu szybko` nie jest niczym. Bez tej pozycji `bardzo`
    # dochodziło do zdania na równi z `szybko`, czyli zdanie przyjęte mówiło o
    # sobie nieprawdę, a kurs, po którym ta pozycja weszła, trzyma
    # docs/konstrukcje-gramatyczne/okolicznik.md#przysłówek-dostaje-wszystkich-trzech-gospodarzy.
    #
    # Córka prawa jest tym samym symbolem, a nie słowem, bo `wyjątkowo bardzo
    # szybko` jest tą samą pozycją postawioną dwa razy, a nad Składnicą oba ciała
    # wypadły tą samą ceną: ciało rekurencyjne bierze łańcuch za darmo.
    grammar.rule(OKOLICZNIK_PRZYSŁÓWKOWY, [PRZYSŁÓWEK_STOPNIA, Głowa(nt(OKOLICZNIK_PRZYSŁÓWKOWY))])
    # `gdzie indziej`, czyli para, w której przysłówek względny nie otwiera zdania,
    # tylko określa drugi przysłówek. Ciało jest osobne, bo terminal okolicznika
    # ten lemat wyklucza (:data:`PRZYSŁÓWEK`), a bez tego ciała wykluczenie
    # zabiera zdania, które ta proza pisze: `Cena jest gdzie indziej.`
    grammar.rule(
        OKOLICZNIK_PRZYSŁÓWKOWY,
        [word("adv", lemma=PRZYSŁÓWEK_WZGLĘDNY), Głowa(word("adv", lemma="indziej"))],
    )
    # Przyimek z przymiotnikiem w formie poprzyimkowej: `po polsku`, `po cichu`.
    # Okolicznikiem, a nie wyrażeniem przyimkowym, bo `adjp` nie niesie przypadka,
    # więc przyimek nie rządzi tu niczym, a pytanie, na które ta para odpowiada,
    # jest pytaniem przysłówka.
    #
    # Głową jest forma, a nie przyimek, i z tego samego powodu: głowa wypuszcza
    # swoje cechy w górę (``Grammar._wypuszczane``), więc przyimek wypuszczałby
    # przypadek, którego okolicznik nie ma z czym uzgadniać.
    grammar.rule(OKOLICZNIK_PRZYSŁÓWKOWY, [PRZYIMEK, Głowa(FORMA_POPRZYIMKOWA)])

    # Cząstka przy zdaniu, tym samym prawem co przysłówek nad nią
    # (:data:`CZĄSTKA_ZDANIA`); kryterium na jej listę stoi przy :data:`CZĄSTKI`.
    grammar.rule(CZĄSTKA_ZDANIA, [CZĄSTKA])

    # Okoliczność wyrażona narzędnikiem bez przyimka (:data:`OKOLICZNIK_NARZĘDNIKOWY`).
    # Konstytuentem, a nie samą grupą wpuszczoną do listy okoliczników, z tego
    # samego powodu, z którego jest nim przysłówek: bez węzła werdykt nie ma czego
    # nazwać, a `okoliczniki` samo jest w :data:`MIJANE`.
    #
    # Licencji ta pozycja nie żąda od niczego, i tym różni się od orzecznika
    # narzędnikowego, którego żąda ramą kopula (`kopula` wyżej). Cenę tej różnicy
    # płaci zdanie z kopulą: `Parser jest narzędziem.` ma odtąd dwa wyprowadzenia,
    # bo grupa w narzędniku stoi w nim raz orzecznikiem, a raz okolicznikiem.
    # Ile takich zdań traci przez to jednoznaczność, mierzy
    # docs/konstrukcje-gramatyczne/okolicznik.md#narzędnik-bez-przyimka-jest-okolicznikiem-obok-orzecznika.
    grammar.rule(OKOLICZNIK_NARZĘDNIKOWY, [nt("grupa_imienna", case="inst")])

    grammar.rule(SPÓJNIK, [SPÓJNIK_WEWNĘTRZNY])
