"""Zdanie podrzędne i rodziny czoła, czyli zdanie z jedną rolą wysuniętą przed nie.

Zdanie względne, pytajne i to z ``że`` różnią się czołem oraz tym,
czym stają przy zdaniu nad sobą, a rdzeń mają jeden;
nazwy każdej z tych rodzin wylicza :class:`olski.subset.deklaracja.Rodzina`.
"""

from __future__ import annotations

from olski.grammar import Grammar, Głowa, Part, V, Var, nt, word
from olski.precedencja import Rozwinięcie
from olski.subset.deklaracja import (
    GRUPA_PYTAJNA,
    IMIESŁÓW_PRZYSŁÓWKOWY,
    OKOLICZNIK_ZDANIOWY,
    ORZECZENIE_RZECZOWNIKOWE,
    RODZINY,
    WTRĄCENIE,
    WYRAŻENIE_PRZYIMKOWE,
)
from olski.subset.rama import _bez_orzecznika, _klasy
from olski.subset.słowa import (
    AGREE,
    BEZ_CZOŁA,
    BEZ_DOSTAWKI,
    CIĄG,
    DOSTAWKA,
    GRUPA_ORZECZENIA_ODWRÓCONA,
    POPRZEDNIK,
    PRZECINEK,
    PRZECZENIA,
    PRZYIMEK,
    PRZYSŁÓWEK_WZGLĘDNY,
    PYTAJNIK,
    SPÓJNIK_BEZ_PRZECINKA,
    SPÓJNIK_DOPEŁNIENIOWY,
    SPÓJNIK_PRZECINKOWY,
    SPÓJNIK_PYTAJNY,
    SPÓJNIKI_OKOLICZNIKOWE,
    SPÓJNIKI_TRYBU,
    SPÓJNIKI_WYSUWANE,
    SZYKI_CZĄSTKI,
    TRYB_POD_SPÓJNIKIEM,
    ZAIMEK_PYTAJNO_RZECZOWNY,
    ZAIMEK_PYTAJNO_WZGLĘDNY,
    ZAIMEK_PYTAJNY,
    ZAIMEK_RZECZOWNY,
    ZAIMEK_WSKAZUJĄCY,
)


def zaimek_czoła(liczba: Var, rodzaj: Var) -> dict[str, Var]:
    """Druga para cech czoła zdania względnego: liczba i rodzaj jego zaimka.

    Czoło niesie dwie pary, a rozdziela je to, kto którą czyta. Pierwszą
    (:data:`AGREE`) czyta orzeczenie, bo zgadza się ono z głową czoła, a tę
    poprzednik, bo zgadza się on z zaimkiem. `której przepisy` niesie obie
    różne, a czoło o jednym słowie tę samą dwa razy, i dlatego zmienne wchodzą
    tu argumentem: przy takim czole są to zmienne :data:`AGREE`.

    Czoło, które tej pary nie niesie, zostawia zmienne poprzednika niezwiązane,
    a wtedy zdanie względne wychodzi bez liczby i rodzaju i przyjmuje każdy
    poprzednik. Nazwy cech są polskie, bo cechę tę wybiera ta gramatyka, a nie
    Morfeusz (``olski/morph.py`` nazywa jego kategorie); kto ją czyta, mówi
    docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka.
    """
    return {"liczba_zaimka": liczba, "rodzaj_zaimka": rodzaj}


def _wysunięta_rola(zdanie: Rozwinięcie, symbol: str, czoło: str) -> None:
    """Wpisz zdanie, w którym jedna rola stoi wysunięta na jego czoło.

    Zdanie takie jest zdaniem bez tej roli, którą wysunięty konstytuent zajmuje, i
    dlatego deklarację dostaje tu każda rola, a nie każdy szyk zdania. Czoło stoi
    pierwsze zawsze, bo tak stawia je polszczyzna, i tyle mówi tu warunek
    precedencji; reszta zdania szyk ma swój.

    Ten sam kształt ma zdanie względne — z `który` (`reguła, która rozstrzyga`,
    `ustawa, której przepisy obowiązują`) oraz z `co` (`to, co mogło się zepsuć`) —
    i pytanie (`które zadania mają charakter obowiązkowy`), a różni je samo czoło,
    więc deklaracje powstają raz i biorą czoło nazwą symbolu. Wypisane osobno dla
    każdego czoła rozeszłyby się na pierwszym dopisanym szyku, a rozejście widać
    dopiero na zdaniu, którego jedno z czół nie wyprowadza.

    Role są dwie: podmiot i dopełnienie. Trzeciej — wyrażenia przyimkowego —
    tutaj nie ma, bo wysuwa się ono razem z przyimkiem i z grupą, w której zaimek
    stoi, więc jest czołem innego kształtu; wypisuje je jednym ciałem ta sama
    pętla, która wywołuje tę funkcję.

    Obie te role czoło nosi etykietą, taką samą jak rola wypełniona na swoim
    miejscu, więc funkcja pisze nad czołem `podmiot` albo `dopełnienie`, a dopiero
    pod nimi zdanie. Po co i jakim kosztem, mówi :data:`BEZ_CZOŁA`.

    Orzeczenie zgadza się z głową czoła, a poprzednik z jego zaimkiem, więc
    orzeczenie bierze ``number`` i ``gender``, a w górę idzie para druga; wywód
    jest przy :func:`zaimek_czoła`. Tyle wystarcza, żeby czołem była grupa,
    a nie sam zaimek.
    """

    def czoło_pierwsze(szyk: tuple[str, ...]) -> bool:
        """Czy czoło stoi w tym szyku pierwsze; o reszcie córek warunek milczy.

        Czoło poznaje się po etykiecie roli, bo pod nią stoi w ciele, a nie pod
        nazwą swojego symbolu. Dopełnienia na swoim miejscu to ciało nie ma,
        więc etykieta wskazuje w nim jedną córkę.
        """
        return szyk[0] == "dopełnienie"

    # Osoba i liczba orzeczenia biorą się z czoła, bo ono jest podmiotem; w
    # deklaracji z dopełnieniem biorą się z podmiotu, który stoi obok, i dlatego
    # zmienne liczby oraz rodzaju są tam inne niż zmienne czoła.
    zaimek = zaimek_czoła(V("nz"), V("gz"))
    orzeczenie = nt("grupa_orzeczenia", number=V("n"), gender=V("g"), person="ter")
    podmiot = nt("podmiot", number=V("nv"), gender=V("gv"), person=V("p"), czoło=BEZ_CZOŁA)

    # Etykieta roli nad czołem: `podmiot` i `dopełnienie`, czyli te same nazwy, które
    # zdanie daje rolom wypełnionym na miejscu. Konstytuentem, a nie cechą na
    # czole, bo rolę czyta się z etykiety węzła (``Node.find`` w
    # ``olski/parse.py``), a wpuszcza ją cecha `czoło` (:data:`BEZ_CZOŁA`).
    zdanie.grammar.rule(
        "podmiot",
        [nt(czoło, case="nom", number=V("n"), gender=V("g"), **zaimek)],
        czoło=czoło,
    )
    czoło_podmiot = nt("podmiot", number=V("n"), gender=V("g"), czoło=czoło, **zaimek)
    zdanie.dominacja(symbol, [czoło_podmiot, Głowa(orzeczenie)], **POPRZEDNIK)

    # Ten sam podmiot wysunięty nad orzeczeniem, w którym dopełnienie stoi przed
    # czasownikiem: `ktoś, kto go nie używa`, `aplikacja, która to napędza`,
    # `Pyta, co olski parsuje.` Szyk ten polszczyzna pisze w zdaniu podrzędnym tak
    # samo jak ten drugi, a zdanie główne miało go od początku, więc bez tego
    # ciała gramatyka mówiła o szyku rzecz nieprawdziwą: że zależy on od tego, czy
    # rola stoi wysunięta.
    #
    # Ciało jest drugie, a nie szyk dopisany do córek wyżej, bo przestawia ono
    # córki orzeczenia, a nie córki zdania; symbol trzyma tę różnicę
    # (:data:`GRUPA_ORZECZENIA_ODWRÓCONA`).
    #
    # Przed czasownik wychodzi samo dopełnienie, a nie całe `wypełnienia`:
    # tamten symbol niesie okolicznik w swoich ciałach, a okolicznik stawia przed
    # czasownikiem także :meth:`Rozwinięcie.dominacja` tutaj, więc `którzy na niej
    # stoją` miałoby dwa wyprowadzenia jednego kształtu.
    orzeczenie_odwrócone = nt(
        GRUPA_ORZECZENIA_ODWRÓCONA, number=V("n"), gender=V("g"), person="ter"
    )
    zdanie.dominacja(symbol, [czoło_podmiot, Głowa(orzeczenie_odwrócone)], **POPRZEDNIK)

    # Podmiot za wysuniętym dopełnieniem stoi po czasowniku i przed nim, bo czoło
    # wysuwa polszczyzna zawsze, a dopełnienie z wyboru
    # (docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka).
    # Wypowiada to sam warunek precedencji: żąda on czoła na pierwszym miejscu i
    # nie żąda niczego od dwóch pozostałych córek.
    #
    # Przypadek czoła rozstrzyga tu przeczenie stojące za nim: `polszczyzna, którą
    # napisał autor` obok `polszczyzna, której nie napisał autor`. Wspólnej zmiennej
    # te dwa nie dostają, bo czoło przypadka nie wybiera — żąda go czasownik —
    # więc para przypadka i wartości cechy stoi wypisana tak samo jak przy
    # dopełnieniu wyżej. Rządzenie sięga tu przez całą resztę zdania składowego, a
    # więc dalej niż gdziekolwiek indziej w tej gramatyce, i tyle też kosztuje:
    # jedna deklaracja rośnie do dwóch. Rozwinięcia szyku to nie dotyka, bo mnoży
    # tu cecha, a nie kolejność.
    #
    # Dopełniacz, którego czasownik żąda ramą, a nie przeczeniem, wysuwa się tą
    # samą trójką ciał: `cena, której żądamy`, `pozycja, której brakuje`, `Kogo
    # dotyczy zmiana?` Przeczenia to ciało nie ogłasza i nie ma czego, dokładnie
    # jak dopełnienie na swoim miejscu: dopełniacz negacji wchodzi w miejsce
    # biernika i tam kończy się jego zasięg, a `nie brakuje ceny` stoi w
    # dopełniaczu tak samo jak `brakuje ceny`.
    #
    # Para stoi wypisana, a nie wzięta z :data:`DOKŁADANE_PRZYPADKI`, bo z tamtej
    # listy wchodzi tu jedna pozycja z dwóch: celownik zmierzono i nie kupił ani
    # jednego zdania prawdziwego
    # (docs/subset.md#dopełniacz-z-ramy-wysuwa-się-na-czoło-a-celownik-nie).
    # Bezokolicznika nie ma w tamtej liście wcale, bo przypadkiem nie jest, a na
    # czoło i tak by się nie wysuwał: jest wypełnieniem innym niż dopełnienie.
    pozycje = (("acc", "acc", "aff"), ("gen", "acc", "neg"), ("gen", "gen", None))
    for przypadek, rama, negacja in pozycje:
        przeczenie = {} if negacja is None else {"negacja": negacja}
        zdanie.grammar.rule(
            "dopełnienie",
            [nt(czoło, case=przypadek, **zaimek)],
            valency=rama,
            czoło=czoło,
            **przeczenie,
        )
        czoło_dopełnienie = nt(
            "dopełnienie", valency=rama, czoło=czoło, **zaimek, **przeczenie
        )
        czasownik = nt(
            "orzeczenie",
            number=V("nv"),
            gender=V("gv"),
            person=V("p"),
            valency=rama,
            **przeczenie,
        )
        zdanie.dominacja(
            symbol,
            [czoło_dopełnienie, Głowa(czasownik), podmiot],
            precedencja=czoło_pierwsze,
            **POPRZEDNIK,
        )

        # Podmiot opuszczony: `imprezy, które zorganizował`, `Które zadania
        # wykonuje?` Polszczyzna opuszcza go tu tak samo jak w zdaniu głównym,
        # gdzie deklaracja bez podmiotu stoi obok tej z podmiotem
        # (``zdanie_składowe → grupa_orzeczenia``), więc i tu jest to druga deklaracja.
        # Warunku precedencji nie ma, bo czoło stoi pierwsze, a za nim została
        # jedna córka. Cenę i zakup trzyma
        # docs/subset.md#zdanie-względne-niesie-liczbę-i-rodzaj-swojego-zaimka.
        zdanie.dominacja(symbol, [czoło_dopełnienie, Głowa(czasownik)], **POPRZEDNIK)

    # Orzecznik wysunięty na czoło: `Czym jest parser?`, `to, czym jest GLR`.
    # Rola jest tu trzecia obok podmiotu i dopełnienia, a pozycję ma jedną, bo
    # narzędnika żąda kopula i nikt poza nią (:data:`KOPULA`), więc szyk jest jeden:
    # czoło, kopula i podmiot, dokładnie jak w zdaniu oznajmującym.
    #
    # Liczby ani rodzaju czoło tu nie niesie, bo orzecznik narzędnikowy z niczym
    # się nie zgadza; kopula zgadza się z podmiotem, który stoi za nią.
    zdanie.grammar.rule(
        "orzecznik", [nt(czoło, case="inst", **zaimek)], valency="inst", czoło=czoło
    )
    czoło_orzecznik = nt("orzecznik", valency="inst", czoło=czoło, **zaimek)
    kopula = nt("orzeczenie", number=V("nv"), gender=V("gv"), person=V("p"), valency="inst")
    zdanie.dominacja(symbol, [czoło_orzecznik, Głowa(kopula), podmiot], **POPRZEDNIK)


def _zamykane(grammar: Grammar, symbol: str, ciało: list[Part | Głowa], **cechy) -> None:
    """Wpisz ciało zdania podrzędnego i to samo ciało zamknięte przecinkiem.

    Przecinek zamykający stawia polszczyzna wtedy, gdy zdanie nadrzędne biegnie
    dalej, i biegnie ono dalej także spójnikiem: `Dokument mówi, że cena jest
    niska, i liczy cenę.` Bez ciała zamkniętego przecinek ten dochodzi do
    koordynacji, która spójnika przed sobą nie bierze, więc zdanie nie ma ani
    jednego czytania.

    Ciała są dwa, a nie jedno z przecinkiem opcjonalnym, bo opcjonalności ten
    formalizm nie ma. Fakt jest jeden na każde zdanie podrzędne, więc stoi tu raz;
    docs/subset.md wywodzi go pod podrzędnością.
    """
    for domknięcie in ((), (PRZECINEK,)):
        grammar.rule(symbol, [*ciało, *domknięcie], **cechy)


def _zdania_podrzędne(grammar: Grammar) -> None:
    """Zdanie podrzędne dopełnieniowe i okolicznik wyrażony zdaniem, w każdej jego postaci."""
    # Zdanie podrzędne dopełnieniowe: `pomiar mówi, że poziom odpowiada`. Pozycję
    # ramy niesie ono tak samo jak dopełnienie i bezokolicznik wyżej,
    # a przecinek zamykający dokłada :func:`_zamykane`.
    _zamykane(
        grammar,
        "zdanie_podrzędne",
        [PRZECINEK, word("comp", lemma=SPÓJNIK_DOPEŁNIENIOWY), Głowa(nt("zdanie"))],
        valency="comp",
    )

    # Okolicznik wyrażony zdaniem: `Program zapisuje ustawienia, gdy linter
    # sprawdza tekst.` i `Gdy linter sprawdza tekst, program zapisuje ustawienia.`
    # Konstrukcja jest okolicznikiem, a nie pozycją ramy, i tym różni się od
    # zdania z `że`: czasownik jej nie żąda i nie ma czasownika, który by jej
    # zabraniał, więc dochodzi ona do zdania, a nie do jego orzeczenia
    # (docs/subset.md#zdanie-z-że-jest-pozycją-ramy-a-nie-konstrukcją-obok-niej).
    #
    # Przecinek należy do tego konstytuentu, tak samo jak w zdaniu dopełnieniowym
    # i względnym, i po tym poznaje ciąg współrzędny werdykt oraz sonda
    # (docs/subset.md#podrzędność-i-koordynacja-dzielą-przecinek-a-rozdziela-je-produkcja).
    # Stoi on po tej stronie zdania podrzędnego, po której stoi zdanie nadrzędne,
    # więc cecha `pozycja` wiąże ciało z miejscem: bez niej ciało z przecinkiem
    # z przodu staje na czele zdania i olski wyprowadza napis zaczynający się
    # przecinkiem, którego nikt nie napisał.
    #
    # Spójnik jest w obu ciałach inny, bo wysunięcie jest faktem o słowie:
    # ciało za zdaniem bierze każdy z listy, a ciało przed zdaniem tylko te,
    # których zdanie polszczyzna wysuwa (:data:`SPÓJNIKI_WYSUWANE`).
    #
    # Przecinek zamykający dostaje ciało za zdaniem (:func:`_zamykane`), a ciało
    # przed zdaniem go nie dostaje, bo już go niesie: zdanie nadrzędne biegnie za
    # nim zawsze.
    _zamykane(
        grammar,
        OKOLICZNIK_ZDANIOWY,
        [PRZECINEK, word("comp", lemma=SPÓJNIKI_OKOLICZNIKOWE), Głowa(nt("zdanie"))],
        pozycja="za",
    )
    grammar.rule(
        OKOLICZNIK_ZDANIOWY,
        [word("comp", lemma=SPÓJNIKI_WYSUWANE), Głowa(nt("zdanie")), PRZECINEK],
        pozycja="przed",
    )

    # Ten sam okolicznik otwarty przysłówkiem względnym (:data:`PRZYSŁÓWEK_WZGLĘDNY`),
    # a nie spójnikiem: `Wchodzi w roadmap.md, gdzie każdy etap ma kryterium wyjścia.`
    # Ciało jest osobne od dwóch wyżej, bo pyta o inną część mowy, i ma jedno
    # miejsce, bo zapowiednika ta gramatyka nie ma; oba fakty stoją przy stałej.
    #
    # Gospodarza ta pozycja nie wybiera i jest to ta sama odmowa, którą olski
    # wydaje o wyrażeniu przyimkowym: `gdzie` dopowiada miejsce nazwane w zdaniu
    # nadrzędnym, a które to miejsce, rozstrzyga znaczenie, nie składnia
    # (docs/subset.md#przyłączanie-wyrażeń-przyimkowych-olski-nie-wybiera).
    przysłówek_względny = word("adv", lemma=PRZYSŁÓWEK_WZGLĘDNY)
    _zamykane(
        grammar,
        OKOLICZNIK_ZDANIOWY,
        [PRZECINEK, przysłówek_względny, Głowa(nt("zdanie"))],
        pozycja="za",
    )
    grammar.rule(
        OKOLICZNIK_ZDANIOWY,
        [przysłówek_względny, Głowa(nt("zdanie")), PRZECINEK],
        pozycja="przed",
    )

    # Ten sam okolicznik pod spójnikiem, który niesie cząstkę trybu
    # (:data:`SPÓJNIKI_TRYBU`): `Gdyby Polacy byli świadomi, zdawaliby sobie
    # sprawę.`, `Trzeba wdrożyć ją szybko, aby jej efekty były widoczne.` Ciała są
    # osobne od tych wyżej, bo tylko one żądają od zdania formy na -ł, a spójnik
    # bierze oba miejsca, bo zdanie z każdym z tych spójników polszczyzna wysuwa.
    #
    # Wypełnieniem bywa fraza bezokolicznikowa zamiast zdania i jest to w tym
    # rejestrze użycie równie częste: `Odnotowuję to, żeby złagodzić wrażenie.`
    # Bezokolicznik podmiotu nie ma i trybu nie niesie, więc ciało z nim o tryb nie
    # pyta, a cenę i zakup ma osobne, bo jest osobnym ciałem.
    spójnik = word("comp", lemma=SPÓJNIKI_TRYBU)
    for wnętrze in (nt("zdanie", tryb=TRYB_POD_SPÓJNIKIEM), nt("fraza_bezokolicznikowa")):
        _zamykane(grammar, OKOLICZNIK_ZDANIOWY, [PRZECINEK, spójnik, Głowa(wnętrze)], pozycja="za")
        grammar.rule(OKOLICZNIK_ZDANIOWY, [spójnik, Głowa(wnętrze), PRZECINEK], pozycja="przed")

    # Ten sam okolicznik wyrażony imiesłowem przysłówkowym: `Program zapisuje
    # ustawienia, sprawdzając zgodność.` Ciała stoją pod tym symbolem, a nie pod
    # własnym: imiesłów zajmuje miejsce, które ten symbol już ma, więc symbol
    # osobny żądałby drugiej kopii obu pozycji i obu ciał nad ciągiem współrzędnym.
    # Spójnika te ciała nie mają, bo imiesłów podporządkowuje sam.
    #
    # Ciała są dwa na każdą pozycję, bo zakup imiesłowu bez wypełnienia jest osobną
    # liczbą. Wywód, pozycje i cenę trzyma
    # docs/subset.md#imiesłów-przysłówkowy-stoi-tam-gdzie-okolicznik-wyrażony-zdaniem.
    imiesłów = nt(IMIESŁÓW_PRZYSŁÓWKOWY, valency=V("w"), negacja=V("z"), druga=V("d"))
    wypełnienie_imiesłowu = nt("wypełnienia", valency=V("w"), negacja=V("z"), druga=V("d"))
    for wnętrze in ([Głowa(imiesłów), wypełnienie_imiesłowu], [Głowa(nt(IMIESŁÓW_PRZYSŁÓWKOWY))]):
        _zamykane(grammar, OKOLICZNIK_ZDANIOWY, [PRZECINEK, *wnętrze], pozycja="za")
        grammar.rule(OKOLICZNIK_ZDANIOWY, [*wnętrze, PRZECINEK], pozycja="przed")

    # Głowa tego okolicznika. Symbolem, a nie ciałem wypisanym w każdej z sześciu
    # pozycji wyżej, bo klas walencyjnych jest kilkadziesiąt i każda pozycja
    # niosłaby je wszystkie osobno.
    #
    # Ramę bierze imiesłów z leksykonu swojego lematu, tak samo jak forma
    # nieosobowa, i tak samo bez orzecznika zgodnego: podmiot tego imiesłowu stoi
    # w zdaniu nadrzędnym, więc pod nim nie ma z czym zgodzić ani jego, ani
    # niczego innego.
    for przeczenie, negacja in PRZECZENIA:
        for zwrotne, przed, za in SZYKI_CZĄSTKI:
            for warunek, rama, druga in _klasy(zwrotne):
                grammar.rule(
                    IMIESŁÓW_PRZYSŁÓWKOWY,
                    [*przed, *przeczenie, Głowa(word("pcon", **warunek)), *za],
                    valency=_bez_orzecznika(rama),
                    negacja=negacja,
                    druga=druga,
                )

    # Dwie pozycje, bo polszczyzna stawia ten okolicznik przed swoim zdaniem i za
    # nim, a szyku wewnątrz zdania nadrzędnego nie zmienia ani jedna, ani druga.
    grammar.rule(
        "zdanie_składowe",
        [Głowa(nt("zdanie_składowe", tryb=V("t"))), nt(OKOLICZNIK_ZDANIOWY, pozycja="za")],
        dostawka=DOSTAWKA,
    )
    grammar.rule(
        "zdanie_składowe",
        [
            nt(OKOLICZNIK_ZDANIOWY, pozycja="przed"),
            Głowa(nt("zdanie_składowe", tryb=V("t"), dostawka=BEZ_DOSTAWKI)),
        ],
    )

    # Te same dwie pozycje nad całym ciągiem współrzędnym, bo okolicznik mówi i o
    # obu członach naraz, i o samym drugim; oba zdania trzyma
    # docs/subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania.
    # Ciała powyżej dają czytanie drugie, te dwa dają pierwsze,
    # i bez nich olski wybiera przez przeoczenie
    # (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    #
    # Ciągu żąda tu cecha (:data:`CIĄG`), a dostawki żąda ciało z okolicznikiem
    # wysuniętym, tak samo jak ciało zdania składowego wyżej; bez jednego i bez
    # drugiego żądania jeden napis wyprowadza się dwoma kształtami.
    grammar.rule(
        "zdanie",
        [Głowa(nt("zdanie", tryb=V("t"), ciąg=CIĄG)), nt(OKOLICZNIK_ZDANIOWY, pozycja="za")],
        dostawka=DOSTAWKA,
    )
    grammar.rule(
        "zdanie",
        [
            nt(OKOLICZNIK_ZDANIOWY, pozycja="przed"),
            Głowa(nt("zdanie", tryb=V("t"), ciąg=CIĄG, dostawka=BEZ_DOSTAWKI)),
        ],
    )

    # Zdanie względne, którego poprzednikiem jest całe zdanie przed przecinkiem:
    # `Cena jest niska, co przekreśla sens działań.`, `Bierzemy ostry zakręt,
    # dzięki czemu unikamy zderzenia.` Liczba i rodzaj stoją wypisane wartością,
    # bo poprzednikiem jest zdanie, które ich nie ma, a tyle niesie zaimek `co` —
    # i tym ta pozycja bierze `co`, a nie `kto` (`zaimek_względny_rzeczowny`).
    #
    # Pozycje są dwie, tak samo jak przy okoliczniku wyrażonym zdaniem wyżej:
    # poprzednikiem bywa jedno zdanie składowe albo cały ciąg (:data:`CIĄG`),
    # a dostawkę ogłaszają oba (:data:`DOSTAWKA`).
    zdaniowe = nt("zdanie_względne_rzeczowne", number="sg", gender="n")
    grammar.rule(
        "zdanie_składowe",
        [Głowa(nt("zdanie_składowe", tryb=V("t"))), zdaniowe],
        dostawka=DOSTAWKA,
    )
    grammar.rule(
        "zdanie",
        [Głowa(nt("zdanie", tryb=V("t"), ciąg=CIĄG)), zdaniowe],
        dostawka=DOSTAWKA,
    )


def _rodziny_czoła(grammar: Grammar, zdanie: Rozwinięcie) -> None:
    """Zdania, w których jedna rola stoi wysunięta na czoło: względne i pytajne."""
    # Zdanie względne, czyli przecinek i `rdzeń_względny`, którym jest samo zdanie
    # bez przecinków odgraniczających. Przecinek zamykający dokłada
    # :func:`_zamykane`, tak samo jak trzem pozostałym zdaniom podrzędnym.
    #
    # Wtrącenie w nawiasie dostaje pozycję w ciele zamykanym przecinkiem i tylko
    # w nim, bo tam stoi ono przed tym przecinkiem, a przyłączone do zdania
    # nadrzędnego stanęłoby za nim, czyli dałoby inny napis. Ciało bez przecinka
    # kończy się tam, gdzie zdanie nadrzędne, więc ta sama pozycja dałaby tam
    # dwa czytania jednego napisu, i dlatego jest to ciało osobne, a nie druga
    # córka w obu; docs/subset.md wywodzi to razem z ceną.
    rdzeń = Głowa(nt("rdzeń_względny", number=V("n"), gender=V("g")))
    _zamykane(grammar, "zdanie_względne", [PRZECINEK, rdzeń])
    grammar.rule("zdanie_względne", [PRZECINEK, rdzeń, nt(WTRĄCENIE), PRZECINEK])

    # To samo zdanie względne z czołem rzeczownym: rzeczownik bierze tamten symbol,
    # a poprzednik zaimkowy i zdaniowy ten (`zaimek_względny_rzeczowny`).
    # Wtrącenia w nawiasie to ciało nie ma, bo pozycji tej nad nim nikt nie policzył.
    rdzeń_rzeczowny = Głowa(nt("rdzeń_względny_rzeczowny", number=V("n"), gender=V("g")))
    _zamykane(grammar, "zdanie_względne_rzeczowne", [PRZECINEK, rdzeń_rzeczowny])

    # Zaimek względny jest grupą imienną o jednym słowie i osobnym symbolem, bo
    # grupa imienna stoi w zdaniu wszędzie, a on w jednym miejscu: na czele
    # zdania względnego. Wpuszczony do grupy imiennej stanąłby w każdej jej
    # pozycji, a `Program zapisuje który.` polszczyzną nie jest.
    # Obie pary cech czoła są tu jedną parą, bo głową jest sam zaimek
    # (:func:`zaimek_czoła`).
    grammar.rule(
        "zaimek_względny",
        [word("adj", lemma=ZAIMEK_PYTAJNO_WZGLĘDNY, **AGREE)],
        **zaimek_czoła(V("n"), V("g")),
    )

    # Ten sam zaimek, którym zdanie pyta, zastępuje też poprzednik: `to, co mogło
    # się zepsuć`, `wszystko, co zjadł`. Symbol jest osobny od zaimka względnego,
    # bo rozstrzyga poprzednik, a nie lemat: `co` zastępuje zaimek rzeczowny albo
    # całe zdanie, a `który` rzeczownik, więc jednym symbolem rzeczownik dostawał
    # zdanie względne z `co`. Wywód, cenę i zakup rozdzielenia trzyma
    # docs/subset.md#poprzednikiem-zaimka-co-jest-zaimek-albo-zdanie.
    #
    # Liczba i rodzaj zaimka odróżniają przy tym `co` od `kto` bez osobnej cechy:
    # `co` jest nijakie, a `kto` męskoosobowe (:func:`zaimek_czoła`).
    # Jedno wykluczenie z pozycji rzeczownej stoi pod tym czołem i pod pytaniem
    # (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`).
    grammar.rule(
        "zaimek_względny_rzeczowny",
        [word("subst", lemma=ZAIMEK_PYTAJNO_RZECZOWNY, **AGREE)],
        **zaimek_czoła(V("n"), V("g")),
    )

    # Grupa, którą polszczyzna wysuwa przed zdanie względne razem z zaimkiem:
    # rzeczownik z zaimkiem w dopełniaczu za sobą (`na podstawie której`) i ten
    # sam rzeczownik z zaimkiem przed sobą (`o którego zdaniu`).
    #
    # Tu obie pary czoła są różne i to jest cała trudność tej grupy: `której
    # przepisy` jest mnogie, a jego zaimek pojedynczy (:func:`zaimek_czoła`).
    # Przypadek wypuszcza rzeczownik, bo o przypadek pyta przyimek nad grupą albo
    # rola, w której grupa stanęła.
    #
    # Każdy z tych dwóch kształtów jest osobnym ciałem, bo cechy nie przechodzą
    # przez grupę imienną same, więc głowa z przydawką pod sobą wysunięcia nie ma.
    #
    # Zaimka rzeczownego ta głowa nie bierze z tego samego powodu, z którego nie
    # bierze go głowa grupy imiennej wyżej: zaimek w dopełniaczu jest tu przydawką,
    # a zaimek rzeczowny przydawki dopełniaczowej przy sobie nie ma.
    głowa_grupy = word("subst", bez_lematu=ZAIMEK_RZECZOWNY, **AGREE)
    zaimek_dopełniacza = nt("zaimek_względny", case="gen", **POPRZEDNIK)
    for ciało in (
        [Głowa(głowa_grupy), zaimek_dopełniacza],
        [zaimek_dopełniacza, Głowa(głowa_grupy)],
    ):
        grammar.rule("grupa_imienna_względna", ciało, **zaimek_czoła(V("nz"), V("gz")))

    # Grupa pytajna: zaimek pytajny i grupa imienna, przy której on stoi. Głową
    # jest grupa imienna, bo pytanie jest o rzecz, którą ona nazywa, a zaimek mówi
    # tylko, że pyta się o to, która z nich. Zaimek zgadza się z tą głową, więc
    # obie pary czoła są i tu jedną parą; niesie ją grupa po to, żeby czoło obu
    # rodzin pisała jedna funkcja, a nie po to, żeby ktoś ją w pytaniu czytał.
    grammar.rule(
        GRUPA_PYTAJNA,
        [ZAIMEK_PYTAJNY, Głowa(nt("grupa_imienna", **AGREE))],
        **zaimek_czoła(V("n"), V("g")),
    )

    # Czoło pytania o jednym słowie: `kto` i `co`, czyli zaimki, którymi pyta się
    # o osobę i o rzecz, a nie o to, która z nich. Rzeczownika przy sobie nie mają,
    # więc ciało jest drugie, a nie ten sam lemat dopisany do listy wyżej.
    #
    # Ciało tego samego symbolu, a nie symbol osobny jak przy zaimku względnym:
    # tam czoła są dwa dlatego, że cena każdego z nich ma być osobną liczbą, a tu
    # jest ona osobną i tak, bo zdejmuje się to jedno ciało. Symbol osobny kazałby
    # ponadto :func:`_wysunięta_rola` wypisać dla niego wszystkie szyki drugi raz.
    zaimek_pytajny_rzeczowny = word("subst", lemma=ZAIMEK_PYTAJNO_RZECZOWNY, **AGREE)
    grammar.rule(GRUPA_PYTAJNA, [zaimek_pytajny_rzeczowny], **zaimek_czoła(V("n"), V("g")))
    # Wyrażenie przyimkowe przy tym zaimku: `Kto z posłów zapisuje ustawienia?`
    # Grupa pytajna wyżej bierze je przez grupę imienną, którą ma w środku, a to
    # czoło grupy imiennej nie ma, więc pozycja jest tu osobnym ciałem. Bez niej
    # zdanie z takim wyrażeniem wychodzi przyjęte i mówi o zdaniu nieprawdę, bo
    # wyrażenie przyłącza się wtedy do orzeczenia: pytanie jest o `kto z posłów`,
    # a nie o `kto`.
    grammar.rule(
        GRUPA_PYTAJNA,
        [Głowa(zaimek_pytajny_rzeczowny), nt(WYRAŻENIE_PRZYIMKOWE)],
        **zaimek_czoła(V("n"), V("g")),
    )
    # Przymiotnik za tym zaimkiem: `Kto pierwszy wstaje od stołu?`, `Kto inny
    # zapisuje ustawienia?` Zaimek zgadza się z nim sam, bo rzeczownika przy sobie
    # nie ma: `kto` jest rodzaju męskiego, a `co` nijakiego.
    #
    # Terminal, a nie symbol przydawki, bo wyklucza zaimek wskazujący
    # (:data:`ZAIMEK_WSKAZUJĄCY`); przysłówka stopnia ta pozycja przez to nie
    # bierze i nikt go tu nie policzył. Cenę i to, czego ta pozycja nie naprawia,
    # trzyma docs/subset.md#zaimki-kto-i-co-wchodzą-wszystkimi-pozycjami-naraz.
    grammar.rule(
        GRUPA_PYTAJNA,
        [Głowa(zaimek_pytajny_rzeczowny), word("adj", bez_lematu=ZAIMEK_WSKAZUJĄCY, **AGREE)],
        **zaimek_czoła(V("n"), V("g")),
    )

    # Zdanie względne i pytanie dzielą kształt: jedna rola stoi w nich wysunięta na
    # czoło, a reszta zdania jest tą samą resztą, więc deklaracje wypisuje jedna
    # funkcja dla obu (:func:`_wysunięta_rola`). Czół jest w zdaniu względnym dwa —
    # sam zaimek i grupa, w której on stoi — i każde z nich wchodzi w obie pozycje:
    # w rolę zdania składowego i pod przyimek. Pytanie ma czoło jedno, bo grupa
    # pytajna obejmuje tam także sam zaimek.
    #
    # Trzecią rolę pętla wypisuje raz na rodzinę, bo jest w niej jednym ciałem:
    # za wysuniętym wyrażeniem przyimkowym stoi zdanie składowe całe, w każdym
    # szyku, jaki ono ma, więc rozwinięcia szyku ta rola od nikogo nie żąda.
    # Symbol wyrażenia jest osobny dla każdej z rodzin, bo wspólny wpuściłby grupę
    # pytajną na czoło zdania względnego, gdzie nie ma się z czym zgodzić.
    #
    # Czoło grupowe stoi obok zaimkowego zamiast je obejmować, i rozstrzyga o tym
    # pomiar: cena każdej z dwóch pozycji jest osobną liczbą,
    # zdejmując produkcje. Czołem jednym pozycja bez przyimka nie byłaby żadnym
    # ciałem osobno, bo te same ciała brałby sam zaimek, więc nie byłoby czego zdjąć.
    for rodzina in RODZINY:
        for czoło in rodzina.czoła:
            _wysunięta_rola(zdanie, rodzina.rdzeń, czoło)
            grammar.rule(
                rodzina.modyfikator,
                [Głowa(PRZYIMEK), nt(czoło, case=V("c"), **zaimek_czoła(V("nz"), V("gz")))],
                **POPRZEDNIK,
            )
        # Za wysuniętym wyrażeniem przyimkowym stoi zdanie składowe albo sam
        # rzeczownik orzekający, bo kopuła opuszczona zostawia po zdaniu jeden
        # wyraz (:data:`ORZECZENIE_RZECZOWNIKOWE`). Dwa ciała, a nie jedno z symbolem wspólnym:
        # cena każdego z nich jest osobną liczbą.
        for wnętrze in (nt("zdanie_składowe"), nt(ORZECZENIE_RZECZOWNIKOWE)):
            grammar.rule(
                rodzina.rdzeń,
                [nt(rodzina.modyfikator, **POPRZEDNIK), Głowa(wnętrze)],
                **POPRZEDNIK,
            )

    # Zdanie pytające: czoło pytania i pytajnik. Ciało jest osobne od zdania
    # oznajmującego, a nie wzięte przez :data:`KONIEC_ZDANIA`, bo pytanie zamyka
    # jeden znak z trzech, które tamten terminal bierze.
    grammar.rule("wypowiedzenie", [Głowa(nt("rdzeń_pytajny")), PYTAJNIK])

    # Pytanie zależne: przecinek i to samo czoło. Pozycję ramy niesie ono tak samo
    # jak zdanie z `że`, a pozycja jest osobna i dlaczego, mówi
    # :data:`RAMA_DOMYŚLNA`. Spójnika w ciele nie ma, bo podporządkowuje tu sam
    # zaimek, i tym się to zdanie podrzędne od dwóch pozostałych różni.
    # Przecinek zamykający dokłada :func:`_zamykane`.
    _zamykane(
        grammar,
        "zdanie_pytajne",
        [PRZECINEK, Głowa(nt("ciąg_pytajny"))],
        valency="int",
    )

    # Ciąg pytań pod jednym czasownikiem: `Drzewo mówi, co w zdaniu jest tematem,
    # a co jest nowe.`, `Dokument mówi, po co był linter i co zamknęło ten tor.`
    # Pozycję ramy zajmuje cały ciąg, a nie każdy człon osobno, bo drugie
    # wypełnienie bierze przy czasowniku sam celownik (:data:`DRUGA_CELOWNIK`),
    # i dlatego ciąg jest tu symbolem, a nie drugim ciałem zdania podrzędnego.
    #
    # Znakiem ciągu jest spójnik, a nie sam przecinek: przecinek w tym miejscu
    # zamyka zdanie podrzędne (:func:`_zamykane`), więc ciało z nim samym dałoby
    # jednemu napisowi dwa wyprowadzenia. Ten rejestr pisze ten ciąg spójnikiem.
    #
    # Bez wykluczenia z pozycji rzeczownej (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`)
    # człon drugi wyprowadza się zdaniem współrzędnym, którego podmiotem albo
    # dopełnieniem jest ten zaimek, więc ciąg stoi razem z tamtym wykluczeniem.
    # Czoło pytania o rozstrzygnięcie: `Czy program zapisuje ustawienia?`, `Pyta,
    # czy go to dotyczy.` Wysuniętej roli tu nie ma, bo pytanie jest o całe zdanie,
    # a nie o to, co w nim stoi w którymś miejscu, więc ciało bierze `zdanie` całe
    # i nie przechodzi przez :func:`_wysunięta_rola`.
    #
    # Ten sam lemat bierze zarazem koordynacja bez przecinka
    # (:data:`SPÓJNIK_BEZ_PRZECINKA`), gdzie `czy` znaczy `albo`, i te dwa użycia
    # rozdziela materiał pod spójnikiem: koordynacja stawia po nim człon, a to
    # ciało zdanie. Napisu wspólnego oba nie mają, więc drugiego czytania to ciało
    # nie dokłada nikomu.
    grammar.rule(
        "rdzeń_pytajny",
        [word("conj", lemma=SPÓJNIK_PYTAJNY), Głowa(nt("zdanie"))],
    )

    człon_pytania = Głowa(nt("rdzeń_pytajny"))
    grammar.rule("ciąg_pytajny", [człon_pytania])
    grammar.rule(
        "ciąg_pytajny",
        [człon_pytania, SPÓJNIK_BEZ_PRZECINKA, nt("ciąg_pytajny")],
    )
    grammar.rule(
        "ciąg_pytajny",
        [człon_pytania, PRZECINEK, SPÓJNIK_PRZECINKOWY, nt("ciąg_pytajny")],
    )
