"""Orzeczenie: forma czasownika, jego rama i głowy orzekające bez podmiotu.

Plik pyta o jedną warstwę, a nie o jedną konstrukcję,
i jest to ta warstwa, która ma swój plik w rejestrze konstrukcji
(docs/konstrukcje-gramatyczne/orzeczenie.md);
kryterium przynależności podaje nagłówek tamtego rejestru.
Szyk zdania należy tutaj, bo rodzaju żąda od niego czas przeszły.

Czy zdanie jest olskim — dwa korpusy zdań i kształt odrzucenia —
pyta ``tests/test_subset.py``.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import Sym, Var
from olski.morph import analyse, generuj
from olski.parse import streszczenia
from olski.segmentacja import bez_licencji, morphology
from olski.subset import (
    DEKLARACJA,
    GRAMMAR,
    ORZECZENIE_BEZOSOBOWE,
    ORZECZNIK_ŁĄCZNIKA,
    PREDYKATYWY,
    RAMA_BEZ_BIERNIKA,
    WALENCJA,
    WALENCJA_ZWROTNA,
)
from olski.walencja import KOPULA
from tests.test_werdykt import role, verdict


def test_predykatyw_przed_czasownikiem_nie_jest_czytany_jako_podmiot():
    #  Lustro reguły OVS. Bez niego ten sam szyk wychodził raz tak, a raz wcale,
    #  zależnie od tego, czy po czasowniku stoi dopełnienie, czy orzecznik, a
    #  ryzykiem przy nim jest zamiana ról: podmiot stoi tu za czasownikiem.
    found = verdict("Wejściem jest zwykły tekst polski.")
    assert found.status == "valid", found.explain()
    assert role(found)[0] == {
        "podmiot": "zwykły tekst polski",
        "orzecznik": "Wejściem",
        "orzeczenie": "jest",
    }


def test_object_first_order_is_polish_and_is_read_that_way():
    #  Free word order is real: here the plural verb forces the plural noun to
    #  be the subject, so the sentence is unambiguous despite the OVS order.
    roles = role(verdict("Program zapisują ustawienia."))[0]
    assert roles["podmiot"] == "ustawienia"
    assert roles["dopełnienie"] == "Program"


def test_dopełniacz_negacji_przed_czasownikiem_ma_czym_się_wyprowadzić():
    #  Bez szyku SOV `tego` brała tu tylko przydawka dopełniaczowa, więc zdanie
    #  wychodziło jednym czytaniem, pewnym siebie i odwrotnym niż drzewo wzorcowe.
    #  Usterka, którą to łapie, jest powrotem tamtego stanu: zdanie znów wychodzi
    #  jednoznaczne, a rola, którą czyta czytelnik, nie ma ciała.
    found = verdict("Apostołowie tego nie praktykowali.")
    assert found.status == "ambiguous", found.explain()
    czytania = {(reading.get("podmiot"), reading.get("dopełnienie")) for reading in role(found)}
    assert ("Apostołowie", "tego") in czytania, found.explain()
    assert ("Apostołowie tego", None) in czytania, found.explain()


@pytest.mark.parametrize("symbol", ["orzeczenie", "podmiot"])
def test_każdy_szyk_zdania_przepuszcza_rodzaj_między_podmiotem_a_czasownikiem(symbol):
    #  Czas przeszły zgadza się z podmiotem w rodzaju, a teraźniejszy tej cechy nie
    #  niesie, więc szyk, który rodzaju nie przepuszcza, wygląda przy `zapisuje` na
    #  poprawny i przyjmuje `Lista stał`. Zdanie tego nie łapie, bo szyków jest
    #  kilkanaście, a zdanie sprawdza jeden. Cechy, której konstytuent nie niesie,
    #  unifikacja nie sprawdza, i to jest ta cisza, którą ten test przerywa.
    odniesienia = [
        part
        for production in GRAMMAR.productions
        for part in production.body
        if isinstance(part, Sym) and part.name == symbol
    ]
    assert odniesienia, symbol
    for part in odniesienia:
        assert "gender" in dict(part.constraints), part
    #  Rodzaj wychodzi z głowy sam, więc pyta ten test o córkę, która głową nie
    #  jest: ciało biorące rodzaj od niej wypuszcza go tylko wtedy, gdy sam to
    #  mówi. Produkcja, której o rodzaj nie pyta ani jedna córka, przepuszczać go
    #  nie ma: czas teraźniejszy tej cechy nie niesie.
    for production in GRAMMAR.productions:
        if production.head != symbol:
            continue
        if any("gender" in dict(part.constraints) for part in production.body):
            assert "gender" in dict(production.features), production


@pytest.mark.parametrize("symbol", ["zdanie", "zdanie_składowe", "grupa_orzeczenia", "orzeczenie"])
def test_każda_produkcja_od_czasownika_do_zdania_wypuszcza_tryb(symbol):
    #  Usterka, przed którą to stoi: ciało zdania dopisane bez cechy trybu.
    #  Spójnik niosący cząstkę tego trybu żąda jej od zdania pod sobą, a cechy,
    #  której konstytuent nie niesie, unifikacja nie sprawdza, więc takie ciało
    #  wpuszcza pod ten spójnik każdy tryb i wyprowadza `żeby program zapisuje
    #  ustawienia`. Pojedyncze zdanie tego nie łapie, bo ciał jest kilkadziesiąt,
    #  a jedno zdanie przechodzi przez jedno z nich.
    #
    #  Zmienna wypisana i niezwiązana milczy tak samo jak cecha pominięta, więc
    #  test pyta o jedno i o drugie: cechę w produkcji i tę samą zmienną w którejś
    #  z jej córek.
    produkcje = [production for production in GRAMMAR.productions if production.head == symbol]
    assert produkcje, symbol
    for production in produkcje:
        tryb = dict(production.features).get("tryb")
        assert tryb is not None, production
        if isinstance(tryb, Var):
            assert any(dict(part.constraints).get("tryb") == tryb for part in production.body), (
                production
            )


def test_tryb_przypuszczający_bierze_osobę_stamtąd_skąd_czas_przeszły():
    #  Usterka, którą to łapie: osoba wypisana zmienną w ciele bez aglutynanta.
    #  `praet` osoby nie niesie, więc bez wpisanej trzeciej `Ja napisałby program.`
    #  się wyprowadza, a zdanie z aglutynantem wychodzi wtedy poprawnie i tej
    #  pomyłki nie pokazuje. Dopełnienie stoi tu w bierniku rozmyślnie: pod
    #  dopełniaczem zdanie odrzuca sam przypadek i test przechodzi z usterką.
    found = verdict("Ja napisałby program.")
    assert found.status == "rejected", found.explain()


def test_rama_kopuli_zdejmuje_dopełnienie_którego_nikt_w_tym_zdaniu_nie_ma():
    #  wolny czyta się jako przymiotnik i jako rzeczownik, a być dopełnienia w
    #  bierniku nie bierze, więc czytania z dopełnieniem nie ma żaden czytelnik
    #  tego zdania. Zabiera je rama kopuli i to jest to, co walencja kupuje.
    #  Zostają dwa czytania i każde stoi na innej dziurze: na rzeczownikowym
    #  czytaniu przymiotnika `wolny`, i na tym, że Morfeusz daje formie `On`
    #  czytanie przymiotnikowe obok zaimkowego, więc staje ona tam, gdzie stoi
    #  orzecznik wysunięty. Wykluczenie słownikowe po żadne z dwóch nie sięga,
    #  bo pyta o czytanie nieodmienne, a te dwa odmieniają się jak każde inne.
    found = verdict("On jest wolny.")
    assert found.status == "ambiguous"
    assert role(found) == [
        {"podmiot": "On", "orzecznik": "wolny", "orzeczenie": "jest"},
        {"podmiot": "wolny", "orzecznik": "On", "orzeczenie": "jest"},
    ]


def test_orzecznik_w_narzędniku_bierze_tylko_kopula():
    #  Ta sama luka, z której da się wyjąć jeden slot i nie więcej. Bez
    #  ograniczenia narzędnik okolicznikowy czyta się jako orzecznik pod każdym
    #  czasownikiem, co docs/corpus.md liczyło jako niezgodność z bankiem drzew:
    #  handel wychodził wtedy orzekany o paszportach, a nie kwitnący w nich.
    #  Odkąd narzędnik ma pozycję okolicznika, zdanie to nie pada, tylko czyta się
    #  tak, jak czyta je czytelnik, i to jest sprawdzian ostrzejszy niż odrzucenie:
    #  gdyby luka się otworzyła, `paszportami` wróciłoby do orzecznika.
    handel = verdict("Kwitnie handel paszportami.")
    assert role(handel) == [
        {
            "podmiot": "handel",
            "orzeczenie": "Kwitnie",
            "okolicznik_narzędnikowy": "paszportami → Kwitnie",
        }
    ], handel.explain()
    assert verdict("Jan jest nauczycielem.").status == "valid"


def test_kopula_nie_stoi_tam_gdzie_okolicznik_narzędnikowy_a_stoi_przy_innym():
    """Zawężenie, którym kopula płaci za okolicznik narzędnikowy, wraz z jego granicą.

    Obie połowy tego testu są pomyłkami, które ta pozycja wpędza po kolei.
    Bez zawężenia `narzędziem` wychodzi raz orzecznikiem, a raz okolicznikiem
    przy czasowniku, który nic nie bierze, więc każde zdanie orzekające
    narzędnikiem traci jednoznaczność.
    Zawężenie postawione na całej liście okoliczników zamiast na narzędniku w niej
    zabiera z kolei czytanie zdaniu, w którym przy kopuli stoi sam przysłówek.
    """
    orzecznik = verdict("Parser jest narzędziem.")
    assert role(orzecznik) == [
        {"podmiot": "Parser", "orzecznik": "narzędziem", "orzeczenie": "jest"}
    ], orzecznik.explain()
    przysłówek = verdict("Cena jest gdzie indziej.")
    assert przysłówek.status == "valid", przysłówek.explain()


@pytest.mark.parametrize(
    ("text", "status"),
    [
        ("Program pozwala zapisać ustawienia.", "valid"),
        ("Program pozwala zostać ustawienia.", "rejected"),
    ],
)
def test_rama_dochodzi_do_bezokolicznika_tak_samo_jak_do_formy_osobowej(text, status):
    #  Bezokolicznik bierze dopełnienia z tego samego leksykonu, co forma osobowa,
    #  i widać to dopiero na parze zdań: samo przyjęcie pierwszego przechodziłoby
    #  też gramatyce, która bezokolicznikowi ramy nie stawia wcale.
    assert verdict(text).status == status


def test_rama_bezokolicznika_rozdziela_orzecznik_od_okolicznika_narzędnikowego():
    #  Para narzędnikowa tego samego pytania. Statusem jej nie widać, odkąd
    #  narzędnik ma pozycję okolicznika przy każdym czasowniku: oba zdania mają
    #  odczytanie, a różni je rola, którą narzędnik w nich zajmuje. `zostać` jest
    #  kopulą i bierze go orzecznikiem, `zapisać` nie jest i zostawia mu samą
    #  pozycję okolicznika (docs/walencja.md#walencja-jest-leksykonem-o-ramie-domyślnej).
    kopula = verdict("Program pozwala zostać nauczycielem.")
    assert any("orzecznik" in czytanie for czytanie in role(kopula)), kopula.explain()
    zwykły = verdict("Program pozwala zapisać nauczycielem.")
    assert not any("orzecznik" in czytanie for czytanie in role(zwykły)), zwykły.explain()


@pytest.mark.parametrize(
    ("text", "status"),
    [
        ("Werdykt służy czytelnikowi.", "valid"),
        ("Parser wyprowadza czytelnikowi.", "rejected"),
        ("Wpis żąda dowodu.", "valid"),
        ("Sonda mierzy dowodu.", "rejected"),
    ],
)
def test_dopełnienia_poza_biernikiem_wpuszcza_leksykon_a_nie_przypadek(text, status):
    #  Pary, na których widać, że pozycję wpuszcza wpis, a nie sam przypadek grupy:
    #  `służyć` i `żądać` mają ją w Walentym, `wyprowadzać` i `mierzyć` nie mają.
    #  Gramatyka biorąca każdy celownik i każdy dopełniacz przechodzi zdanie
    #  pierwsze i trzecie tak samo, a różni się dopiero na drugim i czwartym.
    assert verdict(text).status == status


def test_dopełniacz_z_leksykonu_i_dopełniacz_negacji_dają_jedno_odczytanie():
    #  Czasownik, który dopełniacz bierze ramą, bierze go pod przeczeniem także w
    #  miejscu biernika, więc jeden napis wyprowadza się dwa razy. Odczytanie jest
    #  jedno, bo kształt obu wyprowadzeń jest ten sam, i tego nie widać po
    #  werdykcie żadnego innego zdania: para produkcji jest tu jedyna.
    assert verdict("Wpis nie żąda dowodu.").result.ile == 1


def test_druga_pozycja_ramy_wchodzi_zdaniem_leksykonu_a_nie_sumą_dwóch_pozycji():
    #  Usterka, którą to łapie: para złożona z dwóch zdań leksykonu policzonych
    #  osobno. `pomagać` celownik bierze, a pary z biernikiem nie ma w żadnym
    #  schemacie, więc zdanie drugie odróżnia jedno zdanie leksykonu od drugiego;
    #  bez niego odrzucenie czytałoby się jak brak celownika w ramie.
    assert verdict("Parser pokazuje autorowi oba czytania.").status == "valid"
    assert verdict("Reguła pomaga autorowi.").status == "valid"
    assert not verdict("Reguła pomaga autorowi oba czytania.").readings


def test_druga_pozycja_ramy_stoi_w_obu_szykach_i_nie_stoi_dwa_razy():
    #  Usterka, którą to łapie: wypełnienie pary wzięte zmienną ramy zamiast
    #  wartością. Zmienna przecina się z tą samą ramą co celownik, więc wpuszcza
    #  drugi celownik w miejsce biernika.
    assert verdict("Parser pokazuje oba czytania autorowi.").status == "valid"
    assert not verdict("Parser pokazuje autorowi autorowi.").readings


def test_druga_pozycja_ramy_stoi_obok_każdego_wypełnienia_a_nie_samego_biernika():
    #  Zdanie podrzędne i bezokolicznik zajmują pozycję ramy tak samo jak
    #  dopełnienie, więc celownik staje obok każdego z nich.
    #
    #  `usiąść`, a nie `zejść`: drugie ma u Morfeusza czytanie rzeczownikowe w
    #  dopełniaczu mnogim, więc `córce zejść` wychodzi jedną grupą imienną i to
    #  zdanie wyprowadzało się także bez tej pozycji.
    assert verdict("Parser mówi autorowi, że zdanie czyta się dwojako.").readings
    assert verdict("Krawiec kazał córce usiąść.").status == "valid"


def test_wolny_celownik_pada_obok_dopełnienia_a_nie_na_leksykonie():
    #  Celownik posiadacza dochodzi do orzeczenia dowolnego czasownika, więc
    #  pierwsze zdanie jest polszczyzną, a olski go nie ma. Wpis w leksykonie tego
    #  nie zmieni, bo dopełnienie stoi tu obok dopełnienia, i to jest ta granica,
    #  którą para zdań z tej sekcji łatwo czyta się na opak: leksykon rozstrzyga o
    #  pozycji ramy, a nie o tym, czy przy czasowniku wolno postawić celownik.
    assert verdict("Kompilator wyprowadza psa agentowi.").status == "rejected"
    assert verdict("Kompilator wyprowadza psa.").status == "valid"


@pytest.mark.parametrize("leksykon", [WALENCJA, WALENCJA_ZWROTNA])
def test_klasy_walencyjne_nie_zachodzą_na_siebie(leksykon):
    #  Lemat wzięty dwiema klasami jest dwoma czytaniami tego samego kształtu, a
    #  te dwa zwijają się w jedno, bo czytanie liczy kształt: werdykt tego nie
    #  pokaże i żaden inny test tu nie sięga. Zachodzą klasy łatwo, bo Walenty
    #  mówi o kopuli to samo, co o każdym innym lemacie leksykonu, więc wpis
    #  ręczny musi swoje lematy leksykonowi zabrać, a nie stanąć obok nich.
    lematy = [lemat for klasa in leksykon.values() for lemat in klasa]
    assert len(lematy) == len(set(lematy))


def test_żadna_forma_nie_wpada_w_dwie_klasy_walencyjne_naraz():
    #  Test wyżej pilnuje rozłączności po lematach, a rama jest własnością formy,
    #  więc forma o lematach w dwóch klasach niesie dwie ramy i wychodzi dwoma
    #  wyprowadzeniami jednego kształtu, których liczba czytań nie rozdziela.
    #  Klasa domyślna pyta o całą formę i pary z nią już nie ma, więc zostaje para
    #  dwóch klas twierdzących: kopuła obok klasy wąskiej. Formy idą z syntetyzatora,
    #  bo pytanie jest o słownik, a nie o to, co któryś rejestr napisał.
    wąskie = WALENCJA[RAMA_BEZ_BIERNIKA]
    zderzenia = [
        (forma, sorted(segment.lematy & wąskie))
        for lemat in KOPULA
        for forma, *_ in generuj(lemat)
        for segment in analyse(forma)
        if segment.lematy & KOPULA and segment.lematy & wąskie
    ]
    assert not zderzenia, zderzenia


def test_forma_o_dwóch_lematach_nie_omija_zawężenia_leksykonem():
    #  Zawężenie postawione lematowi omija forma, której słownik daje lemat jeszcze
    #  inny: `zapisuje` jest i od `zapisywać`, i od `zapisować`, a tego drugiego
    #  leksykon nie wymienia, więc czytanie stąd brało ramę domyślną z biernikiem,
    #  którego `zapisywać się` nie bierze. Drugie zdanie jest w parze dlatego, że
    #  czasownik bez cząstki biernik bierze i zawężenie nie ma się na niego rozlać.
    assert verdict("Program zapisuje się ustawienia.").status == "rejected"
    assert verdict("Program zapisuje ustawienia.").status == "valid"


def test_cząstka_się_pyta_leksykonu_o_inny_czasownik_niż_forma_bez_niej():
    #  Otwierać bierze dopełnienie w bierniku, a otwierać się go nie bierze, i
    #  Morfeusz daje obu formom ten sam lemat. Leksykon trzymany pod samym lematem
    #  dałby więc jednemu z tych dwóch zdań ramę drugiego, a widać to dopiero na
    #  parze: jedno przechodzi w każdą stronę, a drugie nie.
    otwarcie = verdict("Otwierają się drzwi.")
    assert role(otwarcie) == [{"podmiot": "drzwi", "orzeczenie": "Otwierają się"}]
    assert verdict("Otwierają drzwi.").status == "ambiguous"


def test_cząstka_zwrotna_przed_formą_pyta_o_ten_sam_leksykon_zwrotny():
    #  Pozycja przednia jest tą samą pozycją tego samego czasownika, więc ramę ma
    #  brać z leksykonu zwrotnego tak samo jak tylna. Ciało napisane z ramą
    #  niezwrotną przechodziłoby zdanie drugie, bo otwierać się biernika nie
    #  bierze, a otwierać go bierze.
    assert role(verdict("Drzwi się otwierają.")) == [
        {"podmiot": "Drzwi", "orzeczenie": "się otwierają"}
    ]
    assert verdict("Drzwi się otwierają okno.").status == "rejected"


def test_cząstka_zwrotna_poprzedza_przeczenie_swojej_formy():
    #  Polszczyzna stawia w pozycji przedniej cząstkę przed przeczeniem, a nie
    #  między nim i formą, i te dwa napisy różni sama ta kolejność.
    assert verdict("Rachunek się nie zwraca.").status == "valid"
    assert verdict("Rachunek nie się zwraca.").status == "rejected"


def test_kopula_nie_bierze_cząstki_zwrotnej_w_żadnej_z_dwóch_pozycji():
    #  Klasa domyślna leksykonu zwrotnego wpuszcza cząstkę do każdego lematu, którego
    #  ten leksykon nie wymienia, a kopula jest wśród nich, więc bez odmowy `być się`
    #  wychodzi czasownikiem w obu pozycjach cząstki i w czasie przyszłym.
    #  Czasownik, przy którym cząstka stoi naprawdę, odmowa zostawia.
    assert verdict("Cena się jest niska.").status == "rejected"
    assert verdict("Cena jest się niska.").status == "rejected"
    assert verdict("Cena się będzie niska.").status == "rejected"
    assert verdict("Rachunek się zwraca.").status == "valid"


def test_cząstka_zwrotna_opiera_się_o_słowo_a_nie_o_znak():
    #  Pozycja przednia sięga początku zdania i miejsca tuż za znakiem, a takich
    #  napisów polszczyzna nie ma. Warunek zdejmuje tam cząstce odczytanie
    #  (po_słowie), więc werdykt nazywa formę bez licencji, a nie strukturę,
    #  której zdaniu brakuje. Spójnik słowem jest i licencji udziela, więc para
    #  ostatnia różni się samym nim.
    assert verdict("Się myli.").status == "rejected"
    assert bez_licencji(morphology("Się myli."), GRAMMAR) == ("Się",)
    assert bez_licencji(morphology("Nic się nie zmienia."), GRAMMAR) == ()
    assert verdict("Cena rośnie, się nie liczy.").status == "rejected"
    assert verdict("Cena rośnie, a się nie liczy.").status == "valid"


@pytest.mark.parametrize(
    ("text", "role_zdania"),
    [
        #  Cząstka stoi między dwoma czasownikami i należy do drugiego: mieć się
        #  jest polszczyzną (ma się dobrze), a bezokolicznika nie bierze.
        ("Zebranie ma się odbyć.", {"podmiot": "Zebranie", "orzeczenie": "ma"}),
        #  Bezokolicznik ma obie pozycje, tak samo jak forma osobowa, więc oba
        #  szyki wychodzą tym samym odczytaniem.
        ("Cena zaczyna otwierać się.", {"podmiot": "Cena", "orzeczenie": "zaczyna"}),
        ("Cena zaczyna się otwierać.", {"podmiot": "Cena", "orzeczenie": "zaczyna"}),
    ],
)
def test_cząstka_należy_do_bezokolicznika_a_nie_do_formy_osobowej_przy_nim(text, role_zdania):
    #  Bez pozycji przy bezokoliczniku cząstkę bierze forma osobowa obok i każde
    #  z tych zdań wychodzi jednym odczytaniem z czasownikiem, którego polszczyzna
    #  nie ma; werdykt ręczy wtedy za czytanie nieprawdziwe.
    assert role(verdict(text)) == [role_zdania]


def test_leksykon_zostawia_bezokolicznik_czasownikowi_zwrotnemu_który_go_bierze():
    #  Odjęcie bezokolicznika ramie zwrotnej daje zdaniu wyżej jedno odczytanie
    #  zamiast dwóch, a bierze je z leksykonu, a nie z całej klasy: bez tego wpisu
    #  odjęcie sięga też czasowników, przy których bezokolicznik naprawdę stoi.
    assert role(verdict("Stara się ustalić granicę.")) == [
        {"dopełnienie": "granicę", "orzeczenie": "Stara się"}
    ]


def test_zdanie_leksykonu_o_bezokoliczniku_nie_żąda_kontroli_podmiotu():
    #  Zdanie węższe, o bezokoliczniku pod kontrolą podmiotu, czyta sam skład.
    #  Parser czytający je zamiast szerszego odbiera bezokolicznik czasownikom
    #  bezosobowym — udać się i dać się kontrolowane są z celownika — i tych zdań
    #  Składnicy nie wyprowadza, choć polszczyzną są.
    assert verdict("Nie udało się ustalić rasy.").status == "valid"
    assert verdict("W teatrze nie da się oszukać widza.").status == "valid"


def test_imiesłów_czynny_bierze_cząstkę_zwrotną_stojącą_za_nim():
    #  Polszczyzna ma tu dwa odczytania, bo cząstka należy albo do imiesłowu, albo
    #  do czasownika, a wybiera między nimi znaczenie. Bez tej pozycji cząstkę
    #  bierze forma osobowa za przydawką i zostaje samo drugie.
    czytania = role(verdict("Program otwierający się psuje."))
    assert {"podmiot": "Program otwierający", "orzeczenie": "się psuje"} in czytania
    assert {"podmiot": "Program otwierający się", "orzeczenie": "psuje"} in czytania


def test_leksykon_odrzuca_zdanie_czytane_dotąd_z_dopełnieniem_którego_tam_nie_ma():
    #  Cena leksykonu, wypisana zdaniem ze Składnicy. Pracować dopełnienia w
    #  bierniku nie bierze, więc dzień i noc nie jest tu dopełnieniem, tylko
    #  okolicznikiem w bierniku, a okolicznika w bierniku olski nie ma. Zdanie
    #  przechodziło, dopóki stało na czytaniu, którego nie ma żaden czytelnik.
    assert verdict("Pracujemy nad tą grupą dzień i noc.").status == "rejected"


def test_pozycja_orzecznika_żąda_ramy_sama_zamiast_dzielić_z_nią_zmienną():
    #  Trzy pozycje orzecznika wyglądają na jedną, w której orzecznik i czasownik
    #  dzielą zmienną walencyjną, a to zdanie ze Składnicy jest ceną takiego
    #  zlania: wychodzi z niego przyjęte i przeczytane na opak, z podmiotem
    #  ustalenia. docs/subset.md trzyma pomiar.
    #
    #  Drugim takim zdaniem było `Na to jest zbyt wielkim tchórzem.`, gdzie
    #  podmiotem wychodziło `zbyt`, i zeszło ono stąd razem z przysłówkiem:
    #  `zbyt` ma teraz pozycję okolicznika, więc olski przyjmuje to zdanie
    #  z czytaniem, które mówi o nim prawdę, i świadkiem tamtej ceny ono nie jest.
    assert verdict("Inne wymagają ustalenia.").status == "rejected"


def test_łącznik_wiąże_pozycję_podmiotu_z_grupą_za_sobą():
    #  Obie grupy stoją w mianowniku, więc unifikacja nie odróżnia stron i wybiera
    #  o tym samo ciało. Bank drzew stawia pozycję `subj` za łącznikiem, a wariant
    #  odwrotny przyjmuje te same zdania, czytając je niezgodnie z drzewem
    #  wzorcowym (docs/konstrukcje-gramatyczne/orzeczenie.md#łącznik-to-orzeka-sam-albo-przy-kopuli-a-podmiot-stoi-za-nim).
    #  Pytanie idzie tu do streszczenia sprzed przekładu na nazwy szkolne, bo po
    #  przekładzie obie strony wyglądają tak samo, a zgodność ze Składnicą liczy
    #  się właśnie przed nim (`_slot_role` w `harness/corpus.py`).
    found = verdict("Flaga to płat tkaniny określonego kształtu.")
    assert found.status == "valid", found.explain()
    [(wewnętrzne,)] = streszczenia(found.result.readings, DEKLARACJA)
    assert wewnętrzne["podmiot"] == "płat tkaniny określonego kształtu", found.explain()
    assert wewnętrzne[ORZECZNIK_ŁĄCZNIKA] == "Flaga", found.explain()


def test_wydruk_nazywa_podmiotem_grupę_przed_łącznikiem_a_orzecznikiem_tę_za_nim():
    #  Usterka, którą to łapie: nazwy wewnętrzne wypuszczone do werdyktu. Wydruk
    #  czyta człowiek znający składnię szkolną, a ta nazywa te role odwrotnie niż
    #  pozycja `subj` w schemacie GFJP; sąd, który ten przekład wykonuje, stoi
    #  przy `NAZWY_SZKOLNE` w `olski/subset/deklaracja.py`.
    found = verdict("Flaga to płat tkaniny określonego kształtu.")
    [(reading,)] = found.readings
    assert reading["podmiot"] == "Flaga", found.explain()
    assert reading["orzecznik"] == "płat tkaniny określonego kształtu", found.explain()
    assert ORZECZNIK_ŁĄCZNIKA not in reading, found.explain()


def test_przekład_na_nazwy_szkolne_pyta_o_czytanie_a_nie_o_zdanie():
    #  Usterka, którą to łapie: warunek przekładu postawiony na zdaniu. `Ty to
    #  leń.` ma oba czytania naraz — w jednym `Ty` stoi przed łącznikiem, w drugim
    #  jest zwykłym podmiotem — więc przekład puszczony na całe zdanie zamieniłby
    #  podmiot temu drugiemu.
    found = verdict("Ty to leń.")
    assert found.status == "ambiguous", found.explain()
    assert {reading["podmiot"] for (reading,) in found.readings} == {"Ty"}, found.explain()


def test_kopula_łącznika_zgadza_się_z_podmiotem_za_nim_a_nie_z_grupą_przed_łącznikiem():
    #  Usterka, którą to łapie: zgodność związana z grupą przed łącznikiem. Ciało
    #  bezczasownikowe zgodności nie żąda i żądać nie może, bo `Lata
    #  dziewięćdziesiąte to okres rozwoju.` różni się liczbą po obu stronach, więc
    #  strona zgodności rozstrzyga się dopiero tutaj i po wydruku jej nie widać:
    #  oba warianty przyjmują `Kot to jest zwierzę.` i różnią się na tej parze.
    zgodne = verdict("Te książki to jest skarb.")
    assert zgodne.status == "valid", zgodne.explain()
    [(wewnętrzne,)] = streszczenia(zgodne.result.readings, DEKLARACJA)
    assert wewnętrzne["podmiot"] == "skarb", zgodne.explain()
    assert wewnętrzne[ORZECZNIK_ŁĄCZNIKA] == "Te książki", zgodne.explain()

    niezgodne = verdict("Te książki to są skarb.")
    assert niezgodne.status == "rejected", niezgodne.explain()


def test_łącznik_przy_formie_osobowej_żąda_kopuli_a_nie_czasownika_każdego():
    #  Usterka, którą to łapie: ciało napisane na `orzeczenie` bez żądania kopuli.
    #  `to` jest wtedy łącznikiem przy każdym czasowniku, więc `Czytał to
    #  nieforemny chłopak.` dostaje drugie czytanie, w którym `to` nie jest
    #  dopełnieniem, a polszczyzna ma tu jedno.
    found = verdict("Czytał to nieforemny chłopak.")
    assert found.status == "valid", found.explain()
    [(reading,)] = found.readings
    assert reading["dopełnienie"] == "to", found.explain()


def test_przeczenie_stoi_przy_łączniku_i_bez_czasownika_i_z_czasownikiem():
    #  Usterki, które to łapie, są dwie i leżą po przeciwnych stronach. Ciało bez
    #  czasownika napisane bez cząstki gubi zdanie drugie. Ciało dopisane cząstce
    #  przy kopuli, choć ta bierze ją sama, czyni zdanie pierwsze wieloznacznym,
    #  bo `valid` znaczy tu jedno czytanie, a nie jakiekolwiek.
    z_czasownikiem = verdict("Parser to nie jest kompilator.")
    assert z_czasownikiem.status == "valid", z_czasownikiem.explain()

    bez_czasownika = verdict("Parser to nie kompilator.")
    assert bez_czasownika.status == "valid", bez_czasownika.explain()


@pytest.mark.parametrize(
    "text",
    [
        "Problem to bowiem gramatyka.",
        "Problem to bowiem nie gramatyka.",
        "To bowiem problem.",
        "To bowiem nie problem.",
        "Był to bowiem problem.",
        "To był bowiem problem.",
        "Kot to jest bowiem zwierzę.",
    ],
)
def test_okolicznik_wchodzi_w_każde_ciało_zdania_z_łącznikiem(text):
    #  Usterka, którą to łapie: ciało łącznika wpisane przez `grammar.rule` zamiast
    #  przez rozwinięcie szyku. Miejsca na okolicznik wylicza rozwinięcie
    #  (``olski/precedencja.py``), więc ciało wpisane obok niego ich nie ma,
    #  a po samym ciele tego nie widać: miejsc na okolicznik nie wypisuje ani jedno.
    #  Zdanie na ciało, bo ciało pominięte gubi dokładnie jedno z nich.
    found = verdict(text)
    assert found.status == "valid", found.explain()


def test_łącznik_żąda_lematu_a_nie_samej_części_mowy():
    #  Usterka, którą to łapie: ciało łącznika napisane na samą część mowy `pred`.
    #  Predykatyw stoi wtedy między dwiema grupami w mianowniku i olski przyjmuje
    #  `Cena widać koszt.`, czego polszczyzna nie pisze, a obietnicą podzbioru
    #  jest, że każde zdanie olskiego jest zdaniem polskim.
    found = verdict("Cena widać koszt.")
    assert found.status == "rejected", found.explain()


def test_predykatyw_orzeka_bez_podmiotu_i_nie_czyni_go_z_biernika():
    #  Usterka, którą to łapie: predykatyw wpuszczony jako `grupa_orzeczenia`, po którym
    #  `Programy trzeba czytać.` wychodzi zdaniem o podmiocie `Programy`
    #  (docs/konstrukcje-gramatyczne/orzeczenie.md#predykatyw-orzeka-bez-podmiotu-i-rządzi-ramą-czasownika).
    found = verdict("Trzeba czytać dokumenty.")
    assert role(found)[0][ORZECZENIE_BEZOSOBOWE] == "Trzeba", found.explain()
    wysunięte = verdict("Programy trzeba czytać.")
    assert wysunięte.status == "rejected", wysunięte.explain()


@pytest.mark.parametrize("lemat", sorted(PREDYKATYWY))
def test_każdy_predykatyw_z_listy_ma_czytanie_którego_gramatyka_sięga(lemat):
    #  Usterka, którą to łapie: lemat wpisany na listę, którego Morfeusz pod `pred`
    #  nie ma. `trudno` i `łatwo` są u niego przysłówkami, więc wpisane tutaj byłyby
    #  wierszem martwym, a martwego wiersza nie widać po żadnym zdaniu.
    [segment] = analyse(lemat)
    czytania = [(r.tag.pos, r.lemma, segment.lematy, r.tag.cechy) for r in segment.readings]
    brane = [c for c in czytania if c[0] == "pred" and GRAMMAR.licencjonuje(*c)]
    assert brane, (lemat, czytania)


def test_czasownik_nieosobowy_orzeka_bez_podmiotu_i_nie_czyni_go_z_biernika():
    #  Usterka, którą to łapie: forma `imps` wpuszczona pod symbolem `orzeczenie`.
    #  Zgodności ta forma nie niesie żadnej, a cechy, której konstytuent nie
    #  niesie, unifikacja nie sprawdza, więc pod tamtym symbolem `program`
    #  wychodzi podmiotem, choć jest tam biernikiem
    #  (docs/konstrukcje-gramatyczne/orzeczenie.md#czasownik-nieosobowy-rządzi-ramą-swojego-lematu).
    found = verdict("Zgłoszono program.")
    assert role(found)[0][ORZECZENIE_BEZOSOBOWE] == "Zgłoszono", found.explain()
    assert "podmiot" not in role(found)[0], found.explain()


def test_dopełnienie_wysunięte_przed_głowę_bez_podmiotu_zostawia_okolicznik_za_nią():
    #  Usterki, które to łapie: pozycja wpisana jednej z dwóch głów zamiast wzięta
    #  nazwą symbolu, po której wysunięcie ma predykatyw albo forma nieosobowa, a
    #  nie obie; oraz dopełnienie wpisane pod `wypełnienia`, po którym
    #  `Usterkę zgłoszono wczoraj.` nie ma gdzie postawić okolicznika, bo tamten
    #  symbol stoi w ciele za głową i tylko tam
    #  (docs/konstrukcje-gramatyczne/orzeczenie.md#dopełnienie-poprzedza-głowę-która-orzeka-bez-podmiotu).
    forma = verdict("Usterkę zgłoszono.")
    assert role(forma)[0]["dopełnienie"] == "Usterkę", forma.explain()
    predykatyw = verdict("Nic nie widać.")
    assert role(predykatyw)[0]["dopełnienie"] == "Nic", predykatyw.explain()
    #  Okolicznik jest tu przysłówkiem bez czytania rzeczownikowego: `wczoraj` ma
    #  u Morfeusza obok przysłówka rzeczownik nieodmienny, więc stanęłoby zarazem
    #  w okoliczniku narzędnikowym i pytanie o pozycję utonęłoby w tamtej parze.
    okolicznik = verdict("Usterkę zgłoszono szybko.")
    assert okolicznik.status == "valid", okolicznik.explain()
    #  Szyk odwrotny ma własne ciało, a nie przestawienie tego, więc jeden napis
    #  wychodzi jednym wyprowadzeniem, a nie dwoma.
    odwrotny = verdict("Zgłoszono usterkę.")
    assert odwrotny.status == "valid", odwrotny.explain()


def test_czasownik_nieosobowy_nie_bierze_orzecznika_zgodnego():
    #  Usterka, którą to łapie: rama leksykonu wzięta tej formie taka, jaka jest.
    #  Orzecznik zgodny zgadza się z podmiotem, więc zdanie bez podmiotu nie ma go
    #  z czym zgodzić, a zdanie niżej wychodzi wtedy przyjęte.
    found = verdict("Zgłoszono tania.")
    assert found.status == "rejected", found.explain()


def test_czasownik_nieosobowy_bierze_ramę_swojego_lematu_a_nie_jednej_konstrukcji():
    #  Usterka, którą to łapie: jedna rama wpisana tej konstrukcji obok listy
    #  lematów, tak jak ma ją predykatyw. Leksykon mówi, że `pomagać` biernika nie
    #  bierze, i forma nieosobowa tego lematu nie bierze go tak samo.
    biernik = verdict("Pomagano usterkę.")
    assert biernik.status == "rejected", biernik.explain()
    sama = verdict("Pomagano.")
    assert sama.status == "valid", sama.explain()


def test_forma_nieosobowa_z_cząstką_pyta_o_leksykon_zwrotny():
    #  Usterka, którą to łapie: pętla zwrotna pytająca o leksykon niezwrotny.
    #  `bawić` bierze biernik, a `bawić się` nie bierze, więc z tamtego leksykonu
    #  zdanie pierwsze wychodzi przyjęte.
    biernik = verdict("Bawiono się usterkę.")
    assert biernik.status == "rejected", biernik.explain()
    okolicznik = verdict("Bawiono się w parku.")
    assert okolicznik.status == "valid", okolicznik.explain()


def test_czasownik_nieosobowy_przeczy_dopełniaczem_tak_jak_forma_osobowa():
    #  Usterka, którą to łapie: ciało napisane bez cząstki przeczącej. Zdanie z nią
    #  wychodzi wtedy odrzucone, a `nie` czyta się jak brak licencji na formę.
    found = verdict("Nie zgłoszono usterki.")
    assert role(found)[0]["dopełnienie"] == "usterki", found.explain()
    biernik = verdict("Nie zgłoszono usterkę.")
    assert biernik.status == "rejected", biernik.explain()


# --------------------------------------------------------------------------- #
# Negacja i dopełniacz, którego ona żąda
# --------------------------------------------------------------------------- #


def test_przeczenie_żąda_od_dopełnienia_dopełniacza():
    #  Biernik pod przeczeniem to jest ta jedna rzecz, którą dopełniacz negacji
    #  zabrania, więc bez tego zakazu cała cecha jest ozdobą: zdanie przeczące
    #  wychodziłoby wtedy dwoma czytaniami zamiast jednego, po jednym na przypadek.
    dopełniacz = verdict("Program nie zapisuje ustawień.")
    assert dopełniacz.status == "valid", dopełniacz.explain()
    assert verdict("Program nie zapisuje plik konfiguracyjny.").status == "rejected"


def test_zdanie_bez_przeczenia_nie_bierze_dopełniacza_negacji():
    #  Druga strona tego samego: gdyby ciało bez cząstki nie ogłaszało `aff`,
    #  dopełniacz negacji stałby w każdym zdaniu, bo cechy, której konstytuent
    #  nie niesie, unifikacja nie sprawdza.
    assert verdict("Program zapisuje ustawień.").status == "rejected"


def test_dopełniacz_negacji_sięga_pod_bezokolicznik_nad_którym_stoi_cząstka():
    #  Rządzenie sięga tu dalej niż zgodność kiedykolwiek: cząstka stoi przy
    #  formie osobowej, a przypadek zmienia się dopełnieniu, które wisi pod
    #  bezokolicznikiem, i przez łańcuch dowolnej długości.
    found = verdict("Program nie pozwala zapisać ustawień.")
    assert found.status == "valid", found.explain()
    assert verdict("Program nie pozwala zapisać ustawienia i dane.").status == "rejected"


def test_przeczenie_przy_bezokoliczniku_zamyka_żądanie_z_góry():
    #  Fraza z własną cząstką nie wypuszcza tej cechy wcale, więc zdanie
    #  nadrzędne, które nie przeczy, nie żąda od niej biernika.
    found = verdict("Program ma nie zapisywać ustawień.")
    assert found.status == "valid", found.explain()


def test_orzecznik_narzędnikowy_stoi_pod_przeczeniem_tak_jak_bez_niego():
    #  Dopełniacz negacji sięga po biernik i po nic więcej, więc kopula pod
    #  przeczeniem bierze swój narzędnik nietknięty.
    found = verdict("Jan nie jest nauczycielem.")
    assert found.status == "valid", found.explain()


def test_zaimek_względny_w_dopełniaczu_przy_przeczącym_zdaniu_względnym():
    #  Przypadek wysuniętego zaimka rozstrzyga przeczenie stojące za resztą
    #  zdania składowego, czyli rządzenie przez cały konstytuent.
    #  Podmiot stoi za czasownikiem, bo rzeczownik zaraz za zaimkiem czyta się
    #  także jako głowa grupy wysuniętej i oba czytania polszczyzna ma.
    found = verdict("Polszczyzna, której nie napisał autor, jest podzbiorem.")
    assert found.status == "valid", found.explain()
    assert verdict("Polszczyzna, którą nie napisał autor, jest podzbiorem.").status == "rejected"


# --------------------------------------------------------------------------- #
# Dopełnienie bezokolicznika wysunięte przed formę osobową
# --------------------------------------------------------------------------- #


def test_dopełnienie_bezokolicznika_wysunięte_przed_formę_osobową_dostaje_swoją_rolę():
    #  Zdanie Składnicy, nad którym bank drzew czyta `premier` podmiotem, a
    #  `większości` dopełnieniem, które bierze `ruszyć`. Bez tej pozycji zostaje
    #  samo czytanie z grupą imienną, więc asercja jest o obu naraz: gramatyka ma
    #  oddać oba, a nie wymienić jedno na drugie.
    found = verdict("Premier większości nie może ruszyć.")
    assert found.result.ile == 2, found.explain()
    assert {streszczenie.get("dopełnienie") for streszczenie in role(found)} == {None, "większości"}


def test_dopełnienie_wysunięte_pyta_o_ramę_bezokolicznika_a_o_przeczenie_formę_osobową():
    #  Dwa kanały biegną tu w przeciwne strony i pomylenie każdego widać osobno.
    #
    #  Rama: celownik wpuszcza leksykon na lemat, `musieć` go nie ma, a `pomagać`
    #  ma, więc pozycja stoi wtedy i tylko wtedy, gdy licencjonuje ją bezokolicznik.
    assert verdict("Program autorowi musi pomagać.").status == "valid"
    assert verdict("Program autorowi musi znać.").status == "rejected"
    assert verdict("Program autorowi musi.").status == "rejected"
    #  Przeczenie czyta forma osobowa: dopełniacza żąda cząstka stojąca przy niej.
    assert verdict("Premier ustawień może zapisać.").result.ile == 1
    assert verdict("Premier ustawień nie może zapisać.").result.ile == 2


def test_dopełnienie_wysunięte_nie_daje_drugiego_wyprowadzenia_zdaniu_które_już_stoi():
    #  Dopełnienie za swoim bezokolicznikiem wyprowadza się przez `wypełnienia`
    #  bezokolicznika, a pozycja wysunięta ma szyk jeden, ten wypisany, więc napis
    #  ten zostaje przy jednym czytaniu.
    found = verdict("Premier nie może ruszyć większości.")
    assert found.status == "valid", found.explain()


def test_okolicznik_ma_przy_wysuniętym_dopełnieniu_tyle_gospodarzy_ile_bez_niego():
    #  Tor zwykły daje okolicznikowi za bezokolicznikiem dwóch gospodarzy, a przed
    #  nim jednego, bo `wypełnienia` bezokolicznika stoi za swoją głową i przed nią
    #  nie sięga.
    assert verdict("Premier nie może ruszyć szybko.").result.ile == 2
    assert verdict("Premier nie może szybko ruszyć.").result.ile == 1
    #  Wysunięcie dokłada każdemu z tych czytań drugie, z dopełnieniem, i nie dokłada
    #  nic ponad to, więc liczby się podwajają. Nierówność znaczy, że któreś z ciał
    #  wybiera gospodarza przez przeoczenie.
    assert verdict("Premier większości nie może ruszyć szybko.").result.ile == 4
    assert verdict("Premier większości nie może szybko ruszyć.").result.ile == 2


def test_okolicznik_przy_wysuniętym_dopełnieniu_nazywa_swojego_gospodarza():
    #  Bez wpisu w `gospodarze` (`DEKLARACJA`) dwa czytania różne samym miejscem
    #  okolicznika streszczają się jednym napisem, a werdykt milczy o wyborze,
    #  który to zdanie zostawia.
    found = verdict("Premier większości nie może ruszyć szybko.")
    assert len({tuple(sorted(s.items())) for s in role(found)}) == found.result.ile
