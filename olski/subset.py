"""Olski itself: the subset of Polish this grammar admits.

Two properties define it, and both are exclusions rather than inventions:

**Every olski sentence is a well-formed Polish sentence.** No helper notation, no
convenient deviation. What olski leaves out, it leaves out entirely.

**Every olski sentence has exactly one reading.** This is the property doing the
real work. Polish is full of sentences that parse two ways, and a reader resolves
them from context or from knowing what the writer meant. Olski excludes them,
because a sentence with two readings has no checkable meaning and, more
importantly, no reliable one.

The grammar below admits every order the subject, the object and the verb can
stand in, since Polish uses all six of them, which is precisely why case
syncretism makes some sentences ambiguous. The alternative — declaring that olski
is SVO and reading the first noun phrase as the subject — would make those
sentences unambiguous to a reader who knows the convention and still ambiguous to
every other Polish speaker. Rejecting them keeps the promise that olski is
readable as ordinary Polish.

That property is about Polish, and a dictionary offers readings Polish does not,
so the subset excludes readings as well as constructions: see ``admissible``
below.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace

from olski.document import SENTENCE_CLOSE, Document
from olski.grammar import Grammar, Głowa, Part, V, Var, nt, word
from olski.morph import Reading, Segment, analyse, tag
from olski.parse import PRZYŁĄCZONY_DO, Deklaracja, Przyłączenie, Result, describe, parse
from olski.walencja import BEZ_BIERNIKA, BEZ_BIERNIKA_ZWROTNE

#: Rola, którą gramatyka zostawia nierozstrzygniętą rozmyślnie,
#: więc streszczenie czytania nazywa przy niej i to, co ona określa:
#: bez tego dwa czytania różne samym miejscem przyłączenia wychodzą jednym napisem.
PRZYŁĄCZANY = "Modifier"

DEKLARACJA = Deklaracja(
    role=("Subject", "Object", "Predicative", "Verb", PRZYŁĄCZANY),
    przyłączany=PRZYŁĄCZANY,
    # Konstytuenty, do których wyrażenie przyimkowe dochodzi,
    # czyli te, w których produkcji stoi ono wypisane:
    # grupa imienna, grupa przymiotnikowa i zdanie składowe.
    # Streszczenie nazywa ten z nich, który stoi najbliżej, bo tam przyłączenie zapadło,
    # a okolicznik zdania nie ma nad sobą żadnego z dwóch pierwszych i zostaje przy zdaniu.
    # Zdanie względne jest tu czwarte i jest zdaniem tak samo jak ``ClauseConjunct``:
    # bez niego okolicznik z jego wnętrza wychodzi w górę do grupy imiennej,
    # którą to zdanie określa, i werdykt nazywa poprzednik zamiast orzeczenia.
    gospodarze=("NP", "AP", "ClauseConjunct", "RelativeCore"),
    # Symbole, które się koordynują: grupa imienna, grupa przymiotnikowa i zdanie.
    # Człon nazywa tu produkcja spójnikowa i przecinkowa każdego z nich,
    # a nie symbol z końcówką ``Conjunct``, który jest jednym członem, a nie ciągiem.
    współrzędne=("NP", "AP", "Clause"),
    # Zdanie składowe, czyli człon ciągu, który koordynuje `Clause`.
    # Symbol jest tu ten z końcówką `Conjunct`, bo streszczenie pyta o rozpiętość
    # jednego zdania, a nie o ciąg, w którym ono stoi.
    składowe=("ClauseConjunct",),
    # Zdania podrzędne: względne i dopełnieniowe.
    # Oba symbole opakowują takie zdanie, a nie są symbolem samego zdania,
    # bo `Clause` koordynuje — jest wypisane wyżej wśród współrzędnych —
    # więc zatrzymanie na nim objęłoby także zdanie współrzędne,
    # którego role są rolami tego samego zdania.
    podrzędne=("RelativeClause", "SubordinateClause"),
)

#: Werdykt o tym, czego nikt nie napisał jako zdania: nagłówku, pozycji listy,
#: wierszu tabeli. Odrzucone znaczy „olski tego nie wyprowadza”, a to jest inne
#: zdanie o tekście i inna robota do zrobienia; docs/extraction.md trzyma wywód i
#: mierzy, jak dużą częścią rejestru ta klasa jest.
FRAGMENT = "fragment"

#: Kopula: czasownik, który bierze orzecznik w narzędniku, i jedyny, który go
#: bierze. Lista jest zamknięta i docs/subset.md wywodzi, czego na niej nie ma.
KOPULA = "być|zostać|zostawać|pozostać|pozostawać"

#: Spójnik, którym zdanie podrzędne dopełnieniowe zaczepia się o czasownik.
#: Jeden, a nie cała klasa `comp`: `gdy`, `jeśli` i `aby` otwierają okolicznik
#: zdania, więc wpuszczone tą produkcją stanęłyby w pozycji, której nie zajmują.
SPÓJNIK_DOPEŁNIENIOWY = "że"

#: Zaimek względny, któremu Morfeusz daje znacznik przymiotnika. Przymiotnikiem
#: przy rzeczowniku nie jest nigdy, więc terminale przydawki i orzecznika go nie
#: biorą, a bierze go czoło zdania względnego i nikt poza nim. Ten warunek
#: odbiera zdaniu podrzędnemu czytanie współrzędne, i za ile,
#: mierzy docs/subset.md.
ZAIMEK_WZGLĘDNY = "który"

#: Rama czasownika spoza leksykonu: dopełnienie w bierniku, orzecznik zgodny,
#: bezokolicznik i zdanie podrzędne. Narzędnika w niej nie ma, i to jest to jedno
#: miejsce, w którym rama domyślna czegoś zabrania: orzecznik narzędnikowy bierze
#: kopula i nikt poza nią. Zdanie podrzędne stoi w niej mimo tego, że leksykon
#: wylicza lematy, które je biorą: zawężenie zmierzono i nie odbiera ono ani
#: jednego drugiego czytania, a kosztuje zdanie; docs/subset.md trzyma pomiar.
RAMA_DOMYŚLNA = "nom.acc.inf.comp"

#: Rama lematu, o którym leksykon mówi, że biernika nie bierze. Wyliczona z
#: domyślnej, a nie wypisana obok niej, żeby pozycję dopisaną tam widziała i ta.
RAMA_BEZ_BIERNIKA = ".".join(p for p in RAMA_DOMYŚLNA.split(".") if p != "acc")


def _walencja() -> tuple[dict[str, str], dict[str, str]]:
    """Leksykon jako klasy walencyjne, osobno dla formy z cząstką ``się`` i bez niej.

    Zwrotność jest drugim wymiarem klucza, a nie częścią lematu, i dlaczego,
    mówi ``olski/walencja.py``, czyli ten, który leksykon czyta dla obu
    kierunków. Tutaj zostaje to, co jest zdaniem samej gramatyki.

    Kluczem klasy jest rama, a nie lemat, bo tak wychodzi produkcja: powstaje raz
    na ramę, a nie raz na lemat. Kopula zabiera leksykonowi swoje lematy, zamiast
    stanąć obok nich, bo klasy mają się nie zachodzić: Walenty mówi o niej to samo
    co leksykon o każdym innym lemacie, a rama kopuli mówi ponadto o narzędniku.

    Zdanie leksykonu jest tu jedno, o bierniku, choć plik mówi trzy. Co zdejmuje
    dwa pozostałe, mówi :data:`RAMA_DOMYŚLNA`.
    """
    return (
        {
            RAMA_BEZ_BIERNIKA: "|".join(sorted(BEZ_BIERNIKA - set(KOPULA.split("|")))),
            "nom.inst": KOPULA,
        },
        {RAMA_BEZ_BIERNIKA: "|".join(sorted(BEZ_BIERNIKA_ZWROTNE))},
    )


#: Walencja: co czasownik bierze, wypisane lematami, a nie produkcjami. Ramą jest
#: zbiór dopełnień, nazwanych przypadkiem grupy, którą czasownik bierze, wraz z
#: ``inf`` dla bezokolicznika, bo bezokolicznik przypadka nie ma.
#:
#: Leksykon jest otwarty: stoi w nim czasownik, którego rama jest węższa od
#: domyślnej, a każdy inny bierze domyślną, więc czasownik dopisuje się wpisem, a
#: nie produkcją i nie kosztuje ani jednego przyjętego zdania, dopóki go nie ma.
#: docs/subset.md wywodzi, czym taki leksykon jest, a czym nie jest.
WALENCJA, WALENCJA_ZWROTNA = _walencja()

#: Zaimek rzeczowny, którego Morfeusz daje obok przymiotnikowego `ten`. Dopełniacza
#: nie bierze: `tego podzbioru` jest przymiotnikiem przy rzeczowniku i niczym
#: więcej, a produkcja z dopełniaczem po głowie czyta to drugi raz jako zaimek
#: rządzący rzeczownikiem. docs/subset.md wywodzi kryterium i mierzy jego cenę.
ZAIMEK_RZECZOWNY = "to"

#: The three features a Polish noun or adjective phrase agrees in, as the
#: variables every production sharing them uses. Spelling them out once is what
#: keeps two parts of one phrase demonstrably talking about the same agreement.
AGREE = {"case": V("c"), "number": V("n"), "gender": V("g")}

#: Przecinek jako znak koordynacji. Warunek na lemat, a nie sama część mowy, bo
#: ``interp`` niesie całą interpunkcję naraz, a średnika, myślnika i nawiasu ten
#: podzbiór nie bierze.
PRZECINEK = word("interp", lemma=",")

#: Cząstka przecząca, czyli jedyne słowo, którym olski przeczy. Warunek na lemat,
#: a nie sama część mowy, tak samo jak przy przecinku: ``part`` niesie całą klasę
#: cząstek naraz, a ``by``, ``czy`` i ``no`` ten podzbiór zostawia na zewnątrz.
PRZECZENIE = word("part", lemma="nie")

#: Przeczenie jako para: co dochodzi na początek ciała i jaką wartość cechy
#: ``negacja`` to ciało wypuszcza. Para, bo obie strony powstają razem: ciało bez
#: cząstki, które nie ogłasza ``aff``, przepuszcza dopełniacz negacji tam, gdzie
#: żadnego przeczenia nie ma, i cechy, której konstytuent nie niesie, unifikacja
#: nie sprawdza. Zdanie przeczące ma dokładnie jedno przeczenie, więc lista jest
#: pętlą po dwóch wartościach, a nie cząstką doklejaną gdziekolwiek.
PRZECZENIA: tuple[tuple[tuple[Part, ...], str], ...] = (((), "aff"), ((PRZECZENIE,), "neg"))


def _klasy(zwrotne: bool) -> list[tuple[dict[str, str], str]]:
    """Klasy walencyjne: warunek na lemat i rama, którą ten warunek wpuszcza.

    Ostatnia jest klasa domyślna, i jest nią warunek ujemny na wszystkie lematy
    leksykonu naraz, bo klasy mają się nie zachodzić: forma wzięta dwiema klasami
    byłaby dwoma czytaniami tego samego kształtu.

    Forma z cząstką ``się`` pyta o swój leksykon, bo jest innym czasownikiem;
    lemat, którego tamten leksykon nie wymienia, bierze ramę domyślną tak samo
    jak każdy inny nieznany.
    """
    leksykon = WALENCJA_ZWROTNA if zwrotne else WALENCJA
    klasy = [({"lemma": lematy}, rama) for rama, lematy in leksykon.items()]
    return [*klasy, ({"bez_lematu": "|".join(leksykon.values())}, RAMA_DOMYŚLNA)]


def _formy_skończone(warunek: dict[str, str]) -> list[tuple[list[Part | Głowa], Var | str]]:
    """Ciała formy osobowej czasownika, każde wraz z osobą, którą niesie.

    Trzy, bo czas przeszły niesie osobę inaczej niż teraźniejszy. ``fin`` niesie
    osobę i liczbę, a rodzaju nie ma; ``praet`` odwrotnie, więc osoba trzecia
    jest w nim wpisana tutaj, a bez tego ``Ja napisał program.`` się wyprowadza:
    cechy, której konstytuent nie niesie, unifikacja nie sprawdza. Osobę pierwszą
    i drugą wnosi aglutynant, czyli końcówkę, którą Morfeusz odcina od formy —
    ``napisałem`` wchodzi tu jako ``napisał`` i ``em`` — i która liczbę ma tę samą
    co czasownik przy niej.

    Głowa stoi w każdym ciele, choć dwa z trzech mają jedną część: ciało wychodzi
    stąd do produkcji zwrotnej, która dopisuje mu cząstkę ``się``, a ciało o
    dwóch częściach bez głowy nie powstaje.
    """
    czasownik = word("praet", number=V("n"), gender=V("g"), **warunek)
    return [
        ([Głowa(word("fin|impt", number=V("n"), person=V("p"), **warunek))], V("p")),
        ([Głowa(czasownik)], "ter"),
        ([Głowa(czasownik), word("aglt", number=V("n"), person=V("p"))], V("p")),
    ]


def build() -> Grammar:
    grammar = Grammar(start="Sentence")

    # Przymiotnik przy rzeczowniku i przymiotnik w orzeczniku, nazwane raz, bo
    # oba wykluczają ten sam lemat i wykluczenie ma być w każdym ciele to samo.
    # Zaimka względnego nie bierze ani jeden z nich: pozycję ma on jedną i stoi
    # ona niżej, na czole zdania względnego.
    przymiotnik = word("adj", bez_lematu=ZAIMEK_WZGLĘDNY, **AGREE)
    orzecznikowy = word("adj|ppas", bez_lematu=ZAIMEK_WZGLĘDNY, **AGREE)

    grammar.rule("Sentence", [Głowa(nt("Clause")), word("interp", lemma=".|!|?")])

    # Koordynacja jest jednym członem, znakiem koordynacji i resztą,
    # na każdym z trzech poziomów, które ją mają.
    # To, co człon może zawierać, rozstrzyga,
    # do czego koordynację da się przyłączyć z zewnątrz,
    # i na tym stoi zawężenie zasięgu, a nie na kształcie tych produkcji.
    # X → X conj X powiedziałoby to samo o zasięgu
    # i tablica Earleya bierze taką produkcję bez skargi,
    # a różni je liczba czytań ciągu współrzędnego; TODO.md trzyma ten wybór.
    #
    # Znakiem koordynacji jest spójnik albo przecinek,
    # i dlatego stoją po dwie produkcje na poziom,
    # a nie jedna z osobnym symbolem na oba znaki.
    # Wspólny symbol powiedziałby to samo raz,
    # ale przecinek przestałby stać przy swoim poziomie,
    # a cena i zakup każdego z trzech są osobnymi liczbami,
    # które `sonda/przecinek.py` bierze, zdejmując te produkcje po jednej.
    #
    # Zasięg koordynacji wywodzi docs/subset.md pod „Nothing above a
    # coordination distributes into it”, a cenę przecinka
    # docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania.
    grammar.rule("Clause", [nt("ClauseConjunct")])
    grammar.rule("Clause", [Głowa(nt("ClauseConjunct")), word("conj"), nt("Clause")])
    grammar.rule("Clause", [Głowa(nt("ClauseConjunct")), PRZECINEK, nt("Clause")])

    # Części zdania, nazwane raz, bo każda z nich stoi w kilku szykach naraz.
    # Zmienna cechy jest zakresu produkcji, więc dwie produkcje biorące ten sam
    # obiekt mówią dalej każda o swojej zgodności.
    #
    # Rodzaj przechodzi przez każdy szyk, bo żąda go czas przeszły, i dlatego
    # podmiot jest tu jeden zamiast dwóch; wywód trzyma
    # docs/subset.md#czas-przeszły-żąda-rodzaju-od-każdego-szyku,
    # a niezmiennik pilnuje test w tests/test_subset.py.
    podmiot = nt("Subject", number=V("n"), gender=V("g"), person=V("p"))
    orzeczenie = nt("Predicate", number=V("n"), gender=V("g"), person=V("p"))
    czasownik = nt("Verb", number=V("n"), gender=V("g"), person=V("p"))
    okoliczniki = nt("Adjuncts")

    # Walencja jest wspólną zmienną, tak jak zgodność: czasownik wypuszcza z
    # siebie swoją ramę, dopełnienie mówi, którą pozycję ramy zajmuje, a
    # unifikacja przecina jedno z drugim. Czasownik, przy którym nic nie stoi,
    # ramy nie ogłasza nikomu i stoi tu bez niej.
    #
    # Negacja jedzie tą samą drogą i rządzi tym samym: przypadkiem grupy, którą
    # czasownik bierze. Czasownik ogłasza, czy przeczy, dopełnienie mówi, przy
    # jakim przeczeniu stoi. Zgodnością to nie jest — rządzenie nie jest ani
    # symetryczne, ani lokalne — więc dlaczego kanał cech ją mimo to bierze,
    # wywodzi docs/design-notes.md#cechy-biorą-to-co-zawęża-jest-symetryczne-i-lokalne.
    czasownik_ramy = nt(
        "Verb", number=V("n"), gender=V("g"), person=V("p"), valency=V("w"), negacja=V("z")
    )
    dopełnienie = nt("Object", valency=V("w"), negacja=V("z"))
    orzecznik_ramy = nt("Predicative", number=V("n"), gender=V("g"), valency=V("w"))
    orzecznik_wysunięty = nt("Predicative", number=V("n"), gender=V("g"))

    # Orzecznik zgodny, wraz z żądaniem, które stawia czasownikowi. Dwa razy
    # ``nom``, a nie wspólna zmienna, bo rama nie zastępuje pozycji: wspólna
    # zmienna wpuszcza tu kopulę z narzędnikiem i przyjmuje nad Składnicą
    # ``Na to jest zbyt wielkim tchórzem.``, gdzie podmiotem wychodzi ``zbyt``.
    # docs/subset.md trzyma ten pomiar wraz z drugim takim.
    orzecznik = nt("Predicative", valency="nom", number=V("n"), gender=V("g"))
    czasownik_orzecznika = nt("Verb", number=V("n"), gender=V("g"), person=V("p"), valency="nom")

    # Kopula po zwinięciu jej w ramę: czasownik, który bierze orzecznik w
    # narzędniku. Osobnego symbolu nie ma, bo rama mówi to samo, a jeden lemat
    # wychodził spod dwóch nazw. Żądanie jest tu na czasowniku, a nie wspólną
    # zmienną z orzecznikiem, i to jest ta sama cena co wyżej.
    kopula = nt("Verb", number=V("n"), gender=V("g"), person=V("p"), valency="inst")

    # Szyki zdania, każdy w tylu wersjach, ile ma miejsc na okolicznik.
    #
    # Wersje z okolicznikiem są jedną decyzją, a nie ośmioma: przyłączenie
    # wyrażenia przyimkowego olski oddaje czytelnikowi, więc każde miejsce, w
    # którym grupa imienna takie wyrażenie bierze, musi umieć oddać je też
    # zdaniu. Pozycji brakującej nie widać po zdaniu odrzuconym, tylko po
    # przyjętym: wychodzi ono jednym czytaniem, bo drugie nie miało gdzie się
    # wyprowadzić. docs/subset.md trzyma wywód i cenę.
    #
    # Osoba bierze się z podmiotu, a nie stoi na trzeciej, i to jest to, co
    # wpuszcza zaimek pierwszej i drugiej osoby. Grupa imienna z rzeczownikiem w
    # głowie mówi person=ter sama, więc rozkaźnik dalej takiej nie weźmie.
    grammar.rule("ClauseConjunct", [podmiot, Głowa(orzeczenie)])
    grammar.rule("ClauseConjunct", [podmiot, okoliczniki, Głowa(orzeczenie)])

    # Zdanie bez podmiotu: Zapisz plik podmiotu nie ma i nie potrzebuje, tak samo
    # jak Zapisuje ustawienia.
    grammar.rule("ClauseConjunct", [nt("Predicate")])

    grammar.rule("ClauseConjunct", [dopełnienie, Głowa(czasownik_ramy), podmiot])
    grammar.rule("ClauseConjunct", [dopełnienie, okoliczniki, Głowa(czasownik_ramy), podmiot])
    grammar.rule("ClauseConjunct", [dopełnienie, Głowa(czasownik_ramy), podmiot, okoliczniki])

    # Czasownik przed podmiotem: Nadchodzi druga rewolucja, Są oni obdarzeni
    # rozumem. Podmiot nie bierze tu własnych dopełnień, więc Zapisuje program
    # ustawienia się nie wyprowadza i żadne zdanie SVO nie konkuruje z czytaniem
    # samego siebie od czasownika.
    grammar.rule("ClauseConjunct", [Głowa(czasownik), podmiot])
    grammar.rule("ClauseConjunct", [Głowa(czasownik), podmiot, okoliczniki])
    grammar.rule("ClauseConjunct", [Głowa(czasownik_orzecznika), podmiot, orzecznik])
    grammar.rule("ClauseConjunct", [Głowa(czasownik_orzecznika), podmiot, okoliczniki, orzecznik])
    grammar.rule("ClauseConjunct", [Głowa(czasownik_orzecznika), podmiot, orzecznik, okoliczniki])

    # Predykatyw przed swoją kopulą: Wejściem jest zwykły tekst polski, W metodzie
    # Cieszyńskiej najważniejsza jest rozmowa. Lustro reguły OVS, którego
    # predykatyw nie miał, więc ten sam szyk wychodził raz tak, a raz wcale,
    # zależnie od tego, co po czasowniku stoi. Orzecznik stoi tu otwarty, bo oba
    # szyki bank drzew ma, a kopula trzyma ten szyk przy orzeczniku: żądanie
    # narzędnika postawione czasownikowi jest tym, co w tej gramatyce znaczy
    # „kopula”, i wysunięcie należy do niej także wtedy, gdy orzecznik jest zgodny.
    grammar.rule("ClauseConjunct", [orzecznik_wysunięty, Głowa(kopula), podmiot])
    grammar.rule("ClauseConjunct", [orzecznik_wysunięty, okoliczniki, Głowa(kopula), podmiot])
    grammar.rule("ClauseConjunct", [orzecznik_wysunięty, Głowa(kopula), podmiot, okoliczniki])

    # Cztery pozostałe szyki podmiotu, dopełnienia i czasownika. Polszczyzna ma
    # wszystkie sześć, a olski miał dwa, i brakujące cztery były wykluczone
    # brakiem produkcji, nie decyzją, czego docs/design-notes.md#angle-one-parsing
    # tej gramatyce zabrania. Cenę i zakup trzyma
    # docs/subset.md#szyk-zmierzono-kupuje-44-zdania-i-odbiera-cztery.
    #
    # Miejsca na okolicznik wylicza tu pętla, a nie ręka: stoi jedno po każdej
    # grupie imiennej i jedno na końcu zdania, a te dwa są jednym tam, gdzie
    # grupa imienna zdanie zamyka. Szyki wyżej wypisują to samo ciałami, i tego
    # ta pętla nie zdejmuje: ciało kończące się na ``Predicate`` okolicznika na
    # końcu nie bierze, bo bierze go ``Complements`` niżej. TODO.md trzyma ruch.
    for szyk in (
        [podmiot, dopełnienie, Głowa(czasownik_ramy)],
        [dopełnienie, podmiot, Głowa(czasownik_ramy)],
        [Głowa(czasownik_ramy), podmiot, dopełnienie],
        [Głowa(czasownik_ramy), dopełnienie, podmiot],
    ):
        grammar.rule("ClauseConjunct", szyk)
        miejsca = {i + 1 for i, część in enumerate(szyk) if część in (podmiot, dopełnienie)}
        for gdzie in sorted(miejsca | {len(szyk)}):
            grammar.rule("ClauseConjunct", [*szyk[:gdzie], okoliczniki, *szyk[gdzie:]])

    # A fronted adjunct. Polish modifies a noun with a prepositional phrase only
    # from behind it, so in front of a clause there is no noun to attach to and
    # the attachment ambiguity docs/subset.md is about cannot arise.
    grammar.rule("ClauseConjunct", [nt("Modifier"), Głowa(nt("ClauseConjunct"))])

    grammar.rule(
        "Subject",
        [nt("NP", case="nom", number=V("n"), gender=V("g"), person=V("p"))],
        number=V("n"),
        gender=V("g"),
        person=V("p"),
    )
    # Dopełnienie wychodzi z pozycją ramy, którą zajmuje, bo tym jest przypadek,
    # który czasownik rządzi: żądanie wobec czasownika stoi więc raz, tutaj, a nie
    # w każdym szyku, w którym dopełnienie stoi.
    #
    # Dopełniacz negacji zajmuje tę samą pozycję ramy, więc jest drugą produkcją
    # dopełnienia, a nie drugą pozycją. Wartość cechy jest tu wypisana, a nie
    # zmienna, bo o przypadku rozstrzyga właśnie ta produkcja.
    grammar.rule("Object", [nt("NP", case="acc")], valency="acc", negacja="aff")
    grammar.rule("Object", [nt("NP", case="gen")], valency="acc", negacja="neg")

    # A predicate is a verb with what it takes. What it takes is one symbol
    # rather than a list of bodies, so that the finite verb and the infinitive
    # below share it instead of each carrying its own copy.
    grammar.rule("Predicate", [czasownik], number=V("n"), gender=V("g"), person=V("p"))
    grammar.rule(
        "Predicate",
        [
            Głowa(czasownik_ramy),
            nt(
                "Complements",
                number=V("n"),
                gender=V("g"),
                valency=V("w"),
                negacja=V("z"),
            ),
        ],
        number=V("n"),
        person=V("p"),
        gender=V("g"),
    )

    # A modal and its infinitive. Powinien inflects for gender and not for
    # person, so the clause it heads agrees with its subject in gender and
    # leaves person to whatever else constrains it.
    for przeczenie, negacja in PRZECZENIA:
        grammar.rule(
            "Predicate",
            [
                *przeczenie,
                Głowa(word("winien", number=V("n"), gender=V("g"))),
                nt("InfinitivePhrase", negacja=negacja),
            ],
            number=V("n"),
            gender=V("g"),
        )
    # Fraza bezokolicznikowa niesie pozycję ramy, którą zajmuje, tak samo jak
    # dopełnienie i orzecznik, więc żądanie wobec czasownika stoi raz, na niej, a
    # nie w każdym ciele, w którym stoi ona. Łańcuch nie potrzebuje przy tym
    # własnej produkcji, bo InfinitivePhrase → inf Complements wraca do ciał niżej
    # i ma pomagać pisać wychodzi z tych dwóch.
    for przeczenie, _ in PRZECZENIA:
        grammar.rule("InfinitivePhrase", [*przeczenie, Głowa(word("inf"))], valency="inf")

    # Zdanie podrzędne dopełnieniowe: `pomiar mówi, że poziom odpowiada`. Pozycję
    # ramy niesie ono tak samo jak dopełnienie i bezokolicznik, więc żądanie wobec
    # czasownika stoi raz, tutaj, a nie w każdym szyku, w którym to zdanie stoi.
    # Przecinek należy do tego konstytuentu, a nie do produkcji nad nim, i tym
    # różni się podrzędność od koordynacji; wywód trzyma docs/subset.md.
    grammar.rule(
        "SubordinateClause",
        [PRZECINEK, word("comp", lemma=SPÓJNIK_DOPEŁNIENIOWY), Głowa(nt("Clause"))],
        valency="comp",
    )

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
    # jak Muszę jechać do domu.
    #
    # Negację niosą dwa z czterech wypełnień i to wystarcza, żeby niosły ją te
    # produkcje: zmienna, której nie zwiąże ani orzecznik, ani zdanie podrzędne,
    # zostaje wolna i konstytuent wychodzi bez tej cechy, a cechy, której
    # konstytuent nie niesie, rodzic nie sprawdza. Orzecznik narzędnikowy stoi
    # więc przy `nie jest` tak samo jak przy `jest`, i tak stoi go polszczyzna.
    for wypełnienie in (
        dopełnienie,
        nt("InfinitivePhrase", valency=V("w"), negacja=V("z")),
        orzecznik_ramy,
        nt("SubordinateClause", valency=V("w")),
    ):
        for ciało in (
            [wypełnienie],
            [okoliczniki, Głowa(wypełnienie)],
            [Głowa(wypełnienie), okoliczniki],
            [okoliczniki, Głowa(wypełnienie), okoliczniki],
        ):
            grammar.rule(
                "Complements",
                ciało,
                number=V("n"),
                gender=V("g"),
                valency=V("w"),
                negacja=V("z"),
            )
    grammar.rule("Complements", [okoliczniki])

    # More than one adjunct, because postępować wobec innych w duchu braterstwa
    # has two and a verb that takes one of them takes any number.
    grammar.rule("Adjuncts", [nt("Modifier")])
    grammar.rule("Adjuncts", [Głowa(nt("Modifier")), okoliczniki])

    # What is predicated of the subject: an adjective phrase agreeing with it,
    # or a noun phrase in the instrumental. Both are what być takes, and the
    # first is also what rodzą się wolni i równi predicates without one.
    #
    # Pozycja ramy wychodzi z orzecznika, bo tym się te dwa różnią i to na nim stoi
    # ograniczenie wyżej: zgodny bierze każdy czasownik, narzędnikowy kopula.
    grammar.rule(
        "Predicative",
        [nt("AP", case="nom", number=V("n"), gender=V("g"))],
        valency="nom",
        number=V("n"),
        gender=V("g"),
    )
    grammar.rule("Predicative", [nt("NP", case="inst")], valency="inst")

    # Rozkaźnik idzie razem z oznajmującą, bo różni je to, co niosą tagi, a nie
    # to, co mówi ta produkcja.
    #
    # Czasownik zwrotny różni się od formy bez cząstki dwiema rzeczami i tyle też
    # mówi o nim ta pętla: stoi przy nim `się`, a rama bierze się z drugiego
    # leksykonu, bo otwierać bierze dopełnienie w bierniku, a otwierać się nie.
    # Cząstka stoi w polszczyźnie i gdzie indziej, a olski bierze tylko tę pozycję.
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
    for zwrotne, cząstka in ((False, ()), (True, (word("part", lemma="się"),))):
        for warunek, rama in _klasy(zwrotne):
            for ciało, osoba in _formy_skończone(warunek):
                for przeczenie, negacja in PRZECZENIA:
                    grammar.rule(
                        "Verb",
                        [*przeczenie, *ciało, *cząstka],
                        number=V("n"),
                        gender=V("g"),
                        person=osoba,
                        valency=rama,
                        negacja=negacja,
                    )

    # Bezokolicznik pyta o leksykon niezwrotny i ma pętlę osobną zamiast warunku
    # wewnątrz tamtej. Cząstki nie bierze, więc `zaczyna otwierać się` nie ma
    # wyprowadzenia, i jest to ta sama dziura, którą docs/subset.md wypisuje pod
    # walencją: `się` dochodzi do czasownika, przy którym stoi, a nie do tego, do
    # którego należy.
    #
    # Fraza bez własnej cząstki wypuszcza negację, którą wzięła od dołu, więc
    # `Nie chcę czytać książki` żąda dopełniacza od dopełnienia stojącego pod
    # bezokolicznikiem, i tak samo przez łańcuch dowolnej długości.
    #
    # Fraza z własną cząstką nie wypuszcza tej cechy wcale i tym zamyka
    # przenoszenie: `Program ma nie zapisywać ustawień` przeczy bezokolicznikowi,
    # a forma osobowa nad nim nie przeczy. Nieobecnością cechy broni się tu tak
    # samo jak grupa współrzędna, która rodzaju nie niesie.
    for warunek, rama in _klasy(zwrotne=False):
        grammar.rule(
            "InfinitivePhrase",
            [Głowa(word("inf", **warunek)), nt("Complements", valency=rama, negacja=V("z"))],
            valency="inf",
            negacja=V("z"),
        )
        grammar.rule(
            "InfinitivePhrase",
            [
                PRZECZENIE,
                Głowa(word("inf", **warunek)),
                nt("Complements", valency=rama, negacja="neg"),
            ],
            valency="inf",
        )

    grammar.rule(
        "NP",
        [nt("NPConjunct", person=V("p"), **AGREE)],
        person=V("p"),
        **AGREE,
    )
    # Zdanie względne po grupie imiennej, w liczbie i rodzaju swojego zaimka:
    # `reguła, która rozstrzyga`. Przypadka nie niesie, bo zaimek bierze go z
    # roli, którą zajmuje w zdaniu podrzędnym, a nie od poprzednika.
    #
    # Stoi to tutaj, a nie wśród ciał `NPConjunct`, i nie jest to wybór wygody:
    # na tamtym poziomie produkcja rekurencyjna daje `te [konstrukcje, które
    # stoją]` obok `[te konstrukcje], które stoją`, czyli dwa wyprowadzenia
    # jednej struktury, których nie ma czym odsiać. Cenę tego poziomu — człon
    # lewy zdania względnego nie unosi — trzyma TODO.md, a docs/subset.md
    # wywodzi, co zgodność z poprzednikiem odbiera przyłączeniu.
    grammar.rule(
        "NP",
        [
            Głowa(nt("NPConjunct", person=V("p"), **AGREE)),
            nt("RelativeClause", number=V("n"), gender=V("g")),
        ],
        person=V("p"),
        **AGREE,
    )
    # A coordination of noun phrases is plural and third person whatever its
    # conjuncts are, and it carries no gender: Polish resolves the gender of
    # rozum i sumienie by rules unification cannot state, and a feature a phrase
    # does not carry is one no agreement can fail against.
    grammar.rule(
        "NP",
        [Głowa(nt("NPConjunct", case=V("c"))), word("conj"), nt("NP", case=V("c"))],
        case=V("c"),
        number="pl",
        person="ter",
    )
    grammar.rule(
        "NP",
        [Głowa(nt("NPConjunct", case=V("c"))), PRZECINEK, nt("NP", case=V("c"))],
        case=V("c"),
        number="pl",
        person="ter",
    )

    # Noun phrases: a noun, an agreeing adjective before it, a genitive
    # modifier after it. Agreement is the unification, not a separate check,
    # and every one of these shares the same three variables, so they are named
    # once. A conjunct headed by a noun is third person by saying so; leaving
    # that off one of them would quietly let a first person verb take it.
    grammar.rule(
        "NPConjunct", [word("subst", **AGREE)], person="ter", **AGREE
    )
    grammar.rule(
        "NPConjunct",
        [przymiotnik, Głowa(nt("NPConjunct", **AGREE))],
        person="ter",
        **AGREE,
    )
    # Głowa, która rządzi dopełniaczem, nie jest zaimkiem rzeczownym: bez tego
    # warunku każda forma paradygmatu ten, którą Morfeusz zna też jako rzeczownik,
    # daje grupie imiennej drugie czytanie tego samego kształtu. Nazwana raz, bo
    # ciał z dopełniaczem pod głową jest kilka, a warunek ma być w każdym ten sam;
    # wywód i cenę trzyma docs/subset.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem.
    głowa_dopełniacza = word("subst", bez_lematu=ZAIMEK_RZECZOWNY, **AGREE)
    grammar.rule(
        "NPConjunct",
        [Głowa(głowa_dopełniacza), nt("NP", case="gen")],
        person="ter",
        **AGREE,
    )
    # Polish puts an attributive adjective after the noun in terminology:
    # plik konfiguracyjny, język polski. Both orders are the language, so both
    # are here, and where a sentence admits both readings it is ambiguous.
    grammar.rule(
        "NPConjunct",
        [Głowa(word("subst", **AGREE)), przymiotnik],
        person="ter",
        **AGREE,
    )
    grammar.rule(
        "NPConjunct",
        [Głowa(word("subst", **AGREE)), nt("Modifier")],
        person="ter",
        **AGREE,
    )
    # Oba szyki przydawki naraz: dobrem wspólnym wszystkich obywateli, zadania
    # ochrony ludności. Bez tej pozycji dopełniacz dochodzi tylko do przymiotnika
    # stojącego przed rzeczownikiem, więc termin nazwany drugim szykiem nie ma
    # wyprowadzenia, a rejestr ustaw nazywa tak swoje terminy zdanie po zdaniu:
    # docs/ustawy.md trzyma, ile ta pozycja tam daje i ile odbiera.
    grammar.rule(
        "NPConjunct",
        [Głowa(głowa_dopełniacza), przymiotnik, nt("NP", case="gen")],
        person="ter",
        **AGREE,
    )
    # Wyrażenie przyimkowe po rzeczowniku, który już coś przy sobie ma: akcja
    # zbrojna w Strefie Gazy, rozmieszczenie ogrodów działkowych w Polsce,
    # zadania ochrony ludności w gminie. Bez tych trzech pozycji przyłączenie do
    # rzeczownika w takiej grupie nie istnieje, a zdanie wychodzi jednym
    # czytaniem przez czasownik. Trzecia idzie razem z przydawką wyżej: bez niej
    # wyrażenie po takim terminie dochodzi do dopełniacza i do nikogo więcej,
    # czyli gramatyka wybiera przyłączenie, którego wybierać nie ma.
    grammar.rule(
        "NPConjunct",
        [Głowa(word("subst", **AGREE)), przymiotnik, nt("Modifier")],
        person="ter",
        **AGREE,
    )
    grammar.rule(
        "NPConjunct",
        [Głowa(głowa_dopełniacza), nt("NP", case="gen"), nt("Modifier")],
        person="ter",
        **AGREE,
    )
    grammar.rule(
        "NPConjunct",
        [Głowa(głowa_dopełniacza), przymiotnik, nt("NP", case="gen"), nt("Modifier")],
        person="ter",
        **AGREE,
    )
    # Grupa liczebnikowa, w dwóch ciałach, bo polszczyzna ma dwa przyłączenia
    # liczebnika i Morfeusz rozdziela je cechą `accommodability`.
    #
    # Liczebnik zgodny stoi jak przymiotnik przy rzeczowniku i zgadza się z nim
    # we wszystkich trzech cechach: `dwie rzeczy`, `cztery wozy`, `oba pliki`.
    # Głową jest rzeczownik, tak samo jak pod przymiotnikiem wyżej.
    #
    # Liczebnik rządzący wymaga dopełniacza mnogiego i wypuszcza grupę, której
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
    grammar.rule(
        "NPConjunct",
        [word("num", accommodability="congr", **AGREE), Głowa(nt("NPConjunct", **AGREE))],
        person="ter",
        **AGREE,
    )
    grammar.rule(
        "NPConjunct",
        [
            Głowa(word("num", accommodability="rec", case=V("c"), gender=V("g"))),
            nt("NP", case="gen", number="pl", gender=V("g")),
        ],
        case=V("c"),
        number="sg",
        gender="n",
        person="ter",
    )

    # A pronoun is the one conjunct that carries its own person, which is the
    # whole reason it is here: without one, first and second person subjects
    # have no noun phrase to be.
    grammar.rule(
        "NPConjunct",
        [word("ppron3|ppron12", person=V("p"), **AGREE)],
        person=V("p"),
        **AGREE,
    )

    # Adjective phrases, coordinated the same way and agreeing throughout, so
    # that wolni i równi is one predicative and wolna i równi is none.
    grammar.rule("AP", [nt("APConjunct", **AGREE)], **AGREE)
    grammar.rule(
        "AP", [Głowa(nt("APConjunct", **AGREE)), word("conj"), nt("AP", **AGREE)], **AGREE
    )
    grammar.rule(
        "AP", [Głowa(nt("APConjunct", **AGREE)), PRZECINEK, nt("AP", **AGREE)], **AGREE
    )
    # A passive participle is an adjective for these purposes, and it keeps the
    # complement its verb governed: obdarzeni rozumem i sumieniem.
    grammar.rule("APConjunct", [orzecznikowy], **AGREE)
    grammar.rule(
        "APConjunct", [Głowa(orzecznikowy), nt("NP", case="inst")], **AGREE
    )
    # Trzecie miejsce, do którego wyrażenie przyimkowe dochodzi: powiązani z
    # interesami postkomunistów, przeznaczany na budowę.
    grammar.rule("APConjunct", [Głowa(orzecznikowy), nt("Modifier")], **AGREE)

    # A preposition governs a case, and the noun phrase has to be in it.
    grammar.rule("Modifier", [Głowa(word("prep", case=V("c"))), nt("NP", case=V("c"))])

    # Zdanie względne, czyli przecinek i `RelativeCore`, którym jest samo zdanie
    # bez przecinków odgraniczających. Przecinek zamykający stawia polszczyzna
    # wtedy, gdy zdanie nadrzędne biegnie dalej, więc oba ciała są tu razem, a
    # zdanie dostaje to z nich, które pasuje do jego interpunkcji.
    for ciało in (
        [PRZECINEK, Głowa(nt("RelativeCore", number=V("n"), gender=V("g")))],
        [PRZECINEK, Głowa(nt("RelativeCore", number=V("n"), gender=V("g"))), PRZECINEK],
    ):
        grammar.rule("RelativeClause", ciało, number=V("n"), gender=V("g"))

    # Zaimek względny jest grupą imienną o jednym słowie i osobnym symbolem, bo
    # grupa imienna stoi w zdaniu wszędzie, a on w jednym miejscu: na czele
    # zdania względnego. Wpuszczony do grupy imiennej stanąłby w każdej jej
    # pozycji, a `Program zapisuje który.` polszczyzną nie jest.
    grammar.rule("RelativePronoun", [word("adj", lemma=ZAIMEK_WZGLĘDNY, **AGREE)], **AGREE)
    grammar.rule(
        "RelativeModifier",
        [
            Głowa(word("prep", case=V("c"))),
            nt("RelativePronoun", case=V("c"), number=V("n"), gender=V("g")),
        ],
        number=V("n"),
        gender=V("g"),
    )

    # Zdanie względne bez zaimka jest zdaniem bez tej roli, którą zaimek zajmuje,
    # i dlatego szyków jest tu tyle, ile ról, a nie tyle, ile szyków ma zdanie.
    # Zaimek stoi na czele zawsze, bo tak stawia go polszczyzna, więc pozycja
    # brakująca jest zawsze pierwsza i reszta zdania jest ciałem, jakie gramatyka
    # ma wypisane wyżej.
    #
    # Trzy role, bo trzy stoją w tym rejestrze: podmiot (`reguła, która
    # rozstrzyga`), dopełnienie (`polszczyzna, którą ktoś napisał`) i wyrażenie
    # przyimkowe (`język, o którym to repozytorium jest`). Ostatnia jest jedną
    # produkcją i sięga najdalej, bo za wyrażeniem przyimkowym stoi zdanie
    # składowe całe, w każdym szyku, jaki ono ma.
    zaimek_podmiot = nt("RelativePronoun", case="nom", number=V("n"), gender=V("g"))
    # Osoba i liczba orzeczenia biorą się tu z zaimka, bo on jest podmiotem;
    # w ciałach z dopełnieniem biorą się z podmiotu, który stoi obok, i dlatego
    # zmienna liczby jest tam inna niż zmienna liczby zaimka.
    orzeczenie_względne = nt("Predicate", number=V("n"), gender=V("g"), person="ter")
    podmiot_względny = nt("Subject", number=V("nv"), gender=V("gv"), person=V("p"))
    grammar.rule(
        "RelativeCore",
        [nt("RelativeModifier", number=V("n"), gender=V("g")), Głowa(nt("ClauseConjunct"))],
        number=V("n"),
        gender=V("g"),
    )
    for ciało in (
        [zaimek_podmiot, Głowa(orzeczenie_względne)],
        [zaimek_podmiot, okoliczniki, Głowa(orzeczenie_względne)],
    ):
        grammar.rule("RelativeCore", ciało, number=V("n"), gender=V("g"))

    # Podmiot za wysuniętym dopełnieniem stoi po czasowniku i przed nim, choć
    # zdanie główne ma ten szyk tylko w pierwszej wersji: `które ktoś napisał`
    # jest w polszczyźnie zwyczajne, a `Teksty ktoś napisał` nie, i różni je to,
    # że zaimek względny wysuwa polszczyzna zawsze, a dopełnienie z wyboru.
    #
    # Okolicznik dostaje obie strony reszty, tak samo jak w szykach zdania
    # wyżej i z tego samego powodu: pozycji brakującej nie widać po zdaniu
    # odrzuconym, tylko po przyjętym, które wychodzi jednym czytaniem, bo drugie
    # nie miało gdzie się wyprowadzić.
    #
    # Przypadek zaimka rozstrzyga tu przeczenie stojące za nim: `polszczyzna,
    # którą ktoś napisał` obok `polszczyzna, której nikt nie napisał`. Wspólnej
    # zmiennej te dwa nie dostają, bo zaimek przypadka nie wybiera — żąda go
    # czasownik — więc para przypadka i wartości cechy stoi wypisana tak samo jak
    # przy dopełnieniu wyżej. Rządzenie sięga tu przez całą resztę zdania
    # składowego, a więc dalej niż gdziekolwiek indziej w tej gramatyce, i tyle
    # też kosztuje: sześć ciał rośnie do dwunastu.
    for przypadek, negacja in (("acc", "aff"), ("gen", "neg")):
        zaimek_dopełnienie = nt(
            "RelativePronoun", case=przypadek, number=V("n"), gender=V("g")
        )
        czasownik_względny = nt(
            "Verb",
            number=V("nv"),
            gender=V("gv"),
            person=V("p"),
            valency="acc",
            negacja=negacja,
        )
        for reszta in (
            [Głowa(czasownik_względny), podmiot_względny],
            [podmiot_względny, Głowa(czasownik_względny)],
        ):
            for ciało in (
                [zaimek_dopełnienie, *reszta],
                [zaimek_dopełnienie, okoliczniki, *reszta],
                [zaimek_dopełnienie, *reszta, okoliczniki],
            ):
                grammar.rule("RelativeCore", ciało, number=V("n"), gender=V("g"))

    return grammar


GRAMMAR = build()


def _nierozstrzygnięte(przyłączenie: Przyłączenie) -> str:
    """Modyfikator i głowy, do których dochodzi, jako jeden wiersz werdyktu.

    Cudzysłów jest treścią, bo modyfikator jest ciągiem wziętym ze zdania i sam
    zawiera odstępy, więc bez niego nie widać, gdzie się kończy. Głowy dostają
    go tak samo, choć każda jest jednym słowem: pierwsze, co o nich trzeba
    wiedzieć, to że stoją w zdaniu tak, jak je autor napisał.
    """
    głowy = ", ".join(f"„{głowa}”" for głowa in przyłączenie.gospodarze)
    return f"„{przyłączenie.modyfikator}”{PRZYŁĄCZONY_DO}{głowy}"


@dataclass(frozen=True)
class Verdict:
    """What olski says about one sentence."""

    #: Zdanie tak, jak stoi w tekście. Segmenty są krawędziami grafu, a nie
    #: listą, więc sklejone dają naraz każdy podział, jaki Morfeusz na formie
    #: widzi: ``ktoś`` wychodzi wtedy jako ``kto ktoś ś``.
    text: str
    result: Result
    #: Formy nie do ominięcia, którym żadna produkcja nie bierze ani jednego
    #: czytania: odrzucenie stanęło na nich, a nie na strukturze. Pola bez
    #: wartości domyślnej, bo pusta krotka jest tu twierdzeniem o zdaniu, a
    #: ``Nowa program zapisuje ustawienia.`` ma je puste i jest odrzucone.
    nielicencjonowane: tuple[str, ...]

    @property
    def status(self) -> str:
        if not SENTENCE_CLOSE.search(self.text):
            return FRAGMENT
        return self.result.status

    @property
    def readings(self) -> list[dict[str, str]]:
        return [describe(reading, DEKLARACJA) for reading in self.result.readings]

    def explain(self) -> str:
        if self.status == FRAGMENT:
            return "not a sentence: nothing punctuates it as one"
        if self.result.valid:
            return "one reading"
        if self.result.rejected:
            if self.nielicencjonowane:
                # Cudzysłów jest treścią: najczęstszą formą bez licencji jest
                # przecinek, a lista rozdzielana przecinkami gubi bez niego granice.
                formy = ", ".join(f"„{forma}”" for forma in self.nielicencjonowane)
                return f"no reading: no production takes {formy}"
            return "no reading: nothing in olski derives this"
        przyłączenia = self.result.przyłączenia
        differing = sorted(
            role
            for role in self.result.różniące
            # Przyłączenie nazwane niżej mówi o tej roli więcej niż sama jej
            # nazwa, więc wypisana obok byłaby tym samym zdaniem dwa razy.
            if not (przyłączenia and role == PRZYŁĄCZANY)
        )
        # Liczba i role wychodzą z lasu, więc granica wyliczania sięga listy
        # czytań i nie sięga tego wiersza: liczba jest liczbą, a nie „64+”.
        count = f"{self.result.ile} readings"
        if differing:
            count += f", differing in {', '.join(differing)}"
        return "; ".join([count, *map(_nierozstrzygnięte, przyłączenia)])


#: The closed-class parts of speech. A noun reading of a form that also reads as
#: one of these is competing with the reading the form nearly always carries.
CLOSED_CLASS = frozenset({"prep", "conj", "comp", "qub", "part", "pred", "interj"})

#: The seven cases. A noun reading carrying all of them inflects for nothing, so
#: no case demand can fail against it.
EVERY_CASE = frozenset({"nom", "gen", "dat", "acc", "inst", "loc", "voc"})


def _acronym(form: str) -> bool:
    """Whether a form is written the way Polish writes an acronym.

    ``PO``, ``AA`` and ``UP`` inflect for nothing either, and their letters spell
    function words, so the exclusion below would take exactly the reading that is
    right. In capitals the noun is what the form is. One capital says nothing,
    every sentence starting with one.
    """
    return len(form) > 1 and form.isupper()


def admissible(segment: Segment) -> Segment:
    """Drop the noun reading of a form olski reads as a function word.

    Morfeusz reads ``do`` as the preposition and as the musical note, and the
    note inflects for nothing: carrying all seven cases, it satisfies every
    demand unification can make, which is the only filter olski has. So every
    ``do`` in a text hands its sentence a second reading. That is ambiguity in
    the dictionary rather than in Polish, and no parse can tell the two apart,
    so the lexicon rules it out instead. docs/subset.md argues the criterion and
    docs/corpus.md measures what it is worth and what it costs.
    """
    if _acronym(segment.form):
        return segment
    if not any(reading.tag.pos in CLOSED_CLASS for reading in segment.readings):
        return segment
    kept = tuple(
        reading
        for reading in segment.readings
        if not (reading.tag.pos == "subst" and reading.tag.get("case") >= EVERY_CASE)
    )
    if len(kept) == len(segment.readings):
        return segment
    # A closed-class reading is not a noun reading, so the one that spared this
    # segment is itself among the survivors and the tuple is never emptied.
    return replace(segment, readings=kept)


#: Notacja tego rejestru: ścieżka, nazwa pliku, nazwa modułu. Człony spaja
#: ukośnik albo kropka, po której nie ma spacji, człon ma dwa znaki wyrazowe albo
#: więcej, w całości stoi przynajmniej jedna litera, a łącznik spaja tylko wewnątrz
#: takiej ścieżki. docs/subset.md wywodzi, co każde z tych czterech żądań trzyma na
#: zewnątrz i dlaczego. Klasa w podglądzie jest sumą pozostałych, bo litery szuka
#: dokładnie tam, gdzie sięgnie dopasowanie: znak spajający dodany do wzorca
#: dodaje się i tam.
CZŁON = r"\w{2,}"
NOTACJA = re.compile(
    rf"(?<![\w./])(?=[\w./_-]*[^\W\d_]){CZŁON}(?:[-_]{CZŁON})*(?:[./]{CZŁON}(?:[-_]{CZŁON})*)+"
)

#: Czytanie, które notacja dostaje: rzeczownik nieodmienny, dokładnie ten tag,
#: który Morfeusz daje `menu` i `atelier`.
NIEODMIENNY = tag("subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:n:ncol")


def morphology(text: str) -> list[Segment]:
    """Analizuje tekst tak, jak czyta go olski.

    Dwie rzeczy dzieją się tu przed gramatyką. Notacja rejestru dostaje jedną
    krawędź z jednym czytaniem, bo Morfeusz rozbija ``docs/linter.md`` na pięć
    krawędzi, a czytelnik ma tam jedno słowo. Reszta idzie do Morfeusza i traci te
    czytania, które odrzuca :func:`admissible`.

    Sklejenie stoi przed analizą, a nie za nią. Segment niesie numery węzłów
    grafu, a nie przesunięcia w tekście, więc po analizie nie ma już czym zobaczyć
    spacji, która ukośnik w ścieżce odróżnia od ukośnika między dwoma słowami.
    """
    return [admissible(segment) for segment in _segmenty(text)]


def _segmenty(text: str) -> list[Segment]:
    """Krawędzie grafu segmentacji, notację liczące za jedną z nich.

    Grafy kolejnych kawałków stają jeden za drugim, przesunięte o numer węzła, na
    którym poprzedni się skończył. Wolno tak, bo każdy z nich ma jedno źródło i
    jedno ujście: Morfeusz numeruje od zera, a wszystkie ścieżki przez kawałek
    kończą się na tym samym węźle, choćby w środku rozchodziły się na dwie.
    """
    segmenty: list[Segment] = []
    węzeł = 0
    for kawałek, notacja in _kawałki(text):
        krawędzie = _krawędzie(kawałek) if notacja else analyse(kawałek)
        segmenty.extend(
            replace(segment, start=segment.start + węzeł, end=segment.end + węzeł)
            for segment in krawędzie
        )
        węzeł += max((segment.end for segment in krawędzie), default=0)
    return segmenty


def _kawałki(text: str):
    """Tnie tekst na kawałki, każdy z odpowiedzią, czy jest notacją."""
    znak = 0
    for match in NOTACJA.finditer(text):
        yield text[znak : match.start()], False
        yield match.group(), True
        znak = match.end()
    yield text[znak:], False


def _krawędzie(forma: str) -> list[Segment]:
    return [Segment(start=0, end=1, form=forma, readings=(Reading(forma, forma, NIEODMIENNY),))]


def bez_licencji(segments: list[Segment], grammar: Grammar) -> tuple[str, ...]:
    """Formy nie do ominięcia, którym gramatyka nie bierze ani jednego czytania.

    Odrzucenie ma dwie przyczyny i są to dwie różne roboty do zrobienia: forma,
    po którą nie sięga żadna produkcja, i struktura, której gramatyka nie
    licencjonuje. Świgra trzyma je osobno (docs/swigra.md), a tę pierwszą widać
    przed rozbiorem i widać ją wyprowadzoną z gramatyki: skoro unifikacja tylko
    zawęża, czytanie odrzucone przez każdy terminal wobec ``EMPTY`` nie
    przejdzie w żadnym zdaniu.

    Liczy się przy tym krawędź, bez której nie ma drogi przez zdanie, a nie
    każda pusta dziedzina: podział, który Morfeusz dokłada obok formy całej, nie
    jest słowem, które ktokolwiek napisał. Wywód i to, co ten warunek daje za
    darmo, trzyma docs/design-notes.md.

    Forma stoi na liście raz, choćby w zdaniu powtórzyła się kilka razy, bo
    odpowiedzią jest to, czego gramatyka nie bierze, a nie ile razy autor to
    napisał.
    """
    formy: list[str] = []
    for segment in segments:
        if any(
            grammar.licencjonuje(reading.tag.pos, reading.lemma, dict(reading.tag.features))
            for reading in segment.readings
        ):
            continue
        if _omijalna(segments, segment) or segment.form in formy:
            continue
        formy.append(segment.form)
    return tuple(formy)


def _omijalna(segments: list[Segment], krawędź: Segment) -> bool:
    """Czy przez graf segmentacji idzie droga, która tej krawędzi nie bierze.

    Krawędzie idą w górę po numerach węzłów, więc osiągalność liczy się jednym
    przejściem po posortowanych, bez cofania się.
    """
    ujście = max(segment.end for segment in segments)
    osiągalne = {min(segment.start for segment in segments)}
    for segment in sorted(segments, key=lambda segment: segment.start):
        if segment is not krawędź and segment.start in osiągalne:
            osiągalne.add(segment.end)
    return ujście in osiągalne


def sentences(text: str) -> list[str]:
    """Tnie tekst na zdania i oddaje je tak, jak stoją.

    Podziału nie ma tutaj, tylko w :mod:`olski.document`: żąda on po kropce
    białego znaku i zna skróty. Sam olski skrótów nie ma, więc nad nim
    cięcie na każdej kropce byłoby dokładne. Wejściem jest jednak dokumentacja,
    gdzie ``docs/linter.md`` jest jednym słowem, a cięcie na kropce w jego środku
    wymyśla dwa zdania, których nikt nie napisał.

    Cięcie stoi więc przed analizą, a nie po niej. Morfeusz jest wołany z
    ``SKIP_WHITESPACES``, a segment niesie numery węzłów grafu zamiast przesunięć
    w tekście, więc po analizie nie ma już czym zobaczyć spacji, która odróżnia
    granicę zdania od nazwy pliku.
    """
    document = Document(text)
    return [document.slice(span) for span in document.sentences]


def check(text: str, grammar: Grammar | None = None) -> list[Verdict]:
    """Check every sentence of a text against the grammar."""
    grammar = grammar or GRAMMAR
    verdicts = []
    for sentence in sentences(text):
        segments = morphology(sentence)
        verdicts.append(
            Verdict(
                text=sentence,
                result=parse(grammar, segments, deklaracja=DEKLARACJA),
                nielicencjonowane=bez_licencji(segments, grammar),
            )
        )
    return verdicts
