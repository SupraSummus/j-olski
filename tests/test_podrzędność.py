"""Zdanie podrzędne, względne i pytanie wraz z wysunięciem roli na czoło.

Plik pyta o jedną warstwę, a nie o jedną konstrukcję,
i jest to ta warstwa, która ma swój plik w rejestrze konstrukcji
(docs/konstrukcje-gramatyczne/podrzędność.md);
kryterium przynależności podaje nagłówek tamtego rejestru.
Rodziny czoła sprawdza ten sam plik co zdania,
bo wypisane są obok tych produkcji i rozejść się mogą już tylko z nimi.

Czy zdanie jest olskim — dwa korpusy zdań i kształt odrzucenia —
pyta ``tests/test_subset.py``.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import Sym
from olski.subset import (
    GRAMMAR,
    GRUPA_PYTAJNA,
    OKOLICZNIK_ZDANIOWY,
    ORZECZENIE_RZECZOWNIKOWE,
    RODZINY,
)
from tests.test_werdykt import role, verdict


def _po_głowach(symbol: str, widziane: set[str] | None = None) -> set[str]:
    """Symbole, do których schodzi się od tego samymi głowami ciał."""
    widziane = set() if widziane is None else widziane
    for produkcja in GRAMMAR.for_head(symbol):
        if not produkcja.body:
            continue
        głowa = produkcja.body[produkcja.głowa]
        if isinstance(głowa, Sym) and głowa.name not in widziane:
            widziane.add(głowa.name)
            _po_głowach(głowa.name, widziane)
    return widziane


def test_symbol_opakowujący_rodzinę_czoła_ma_pod_głową_jej_rdzeń():
    """Rodzina wypisana ręką ma stać zgodnie z tym, co gramatyka wyprowadza.

    Cztery miejsca czytają dziś jedną :class:`Rodzina`, więc rozejść się może
    już tylko ona sama z gramatyką, i najciszej wtedy, gdy nazwa jest symbolem
    prawdziwym, tylko cudzym: symbol opakowujący wpisany do niewłaściwej rodziny
    zatrzymuje streszczenie tam, gdzie role są rolami zdania nad nim.

    Pytamy o łańcuch głów, a nie o córkę ani o dosięgnięcie w ogóle: zdanie
    pytające dochodzi do swojego rdzenia przez ciąg pytań, więc córką rdzeń nie
    jest, a dosięgnąć stąd można prawie każdego symbolu, bo zdanie podrzędne ma
    pod sobą całe zdanie.
    """
    rdzenie = {rodzina.rdzeń for rodzina in RODZINY}
    for rodzina in RODZINY:
        for symbol in rodzina.opakowujące:
            assert _po_głowach(symbol) & rdzenie == {rodzina.rdzeń}, symbol


def test_przyimek_pod_zaimkiem_pytajnym_dostaje_w_werdykcie_swojego_gospodarza():
    """Czoło pytania zatrzymuje zejście, bo przyimek pod nim określa sam zaimek.

    Czytań pominięcie takiego gospodarza nie rusza, więc nie widać go po ich
    liczbie: zejście mija wtedy czoło i oba czytania dostają jednego gospodarza,
    czyli orzeczenie, choć w pierwszym z nich przyimek stoi pod `Kto`.
    """
    found = verdict("Kto z posłów zapisuje ustawienia?")
    assert found.result.ile == 2, found.explain()
    [przyłączenie] = found.result.przyłączenia
    assert przyłączenie.modyfikator == "z posłów"
    assert przyłączenie.gospodarze == ("Kto", "zapisuje")


def test_zdanie_względne_bierze_okolicznik_między_podmiotem_a_czasownikiem():
    #  Miejsce, które gramatyka pisana ręką miała w dwóch ciałach z trzech i w
    #  trzecim je pominęła. Usterka jest niewidoczna po werdykcie: zdanie nie
    #  zostaje odrzucone, tylko wychodzi jednym czytaniem, w którym `w tym trybie`
    #  dochodzi do `organ`, bo czytanie z przyłączeniem do `wydaje` nie ma gdzie
    #  się wyprowadzić. Powrotem tamtego stanu jest `valid` nad tym zdaniem.
    found = verdict("Ustawa, którą organ w tym trybie wydaje, jest tania.")
    assert found.status == "ambiguous", found.explain()
    [przyłączenie] = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("wydaje", "organ"), found.explain()


def test_zdanie_podrzędne_z_że_wyprowadza_się_raz_mimo_przecinka_koordynacji():
    #  Przecinek koordynuje zdania, więc gramatyka, która bierze go na poziomie
    #  zdania i nie ma podrzędności, czyta zdanie podrzędne jako współrzędne.
    #  Rozdziela je miejsce przecinka: tutaj stoi on wewnątrz konstytuentu,
    #  który zdanie podrzędne tworzy, a nie nad dwoma zdaniami.
    found = verdict("Pomiar mówi, że gramatyka jest podzbiorem.")
    assert found.status == "valid", found.explain()


def test_pytanie_zależne_nie_wychodzi_zdaniem_współrzędnym():
    #  Morfeusz daje `które` ten sam znacznik co `nowe`, więc bez warunku
    #  ujemnego `które zadania własne gminy` jest grupą imienną i staje się
    #  podmiotem zdania po przecinku. Wychodzi z tego jedno czytanie, pewne
    #  siebie i błędne, czyli werdykt najgorszy z tych, jakie olski wydaje.
    #  Zdanie ma jedno czytanie i jest nim pytanie zależne, a nie tamto: role
    #  współrzędnego niosłyby znak sąsiedniego zdania składowego, a role pytania
    #  zależnego są rolami zdania nadrzędnego i tylko nimi.
    found = verdict("Ustawy określają, które zadania własne gminy mają charakter obowiązkowy.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"podmiot": "Ustawy", "orzeczenie": "określają"}]


def test_pytanie_zależne_z_kto_nie_wychodzi_zdaniem_współrzędnym():
    #  Zdanie to jest werdyktem najgorszym, jaki ten podzbiór wydaje: Morfeusz
    #  czyta `kto` jako zaimek rzeczowny, przecinek koordynuje zdania, więc bez
    #  wykluczenia zaimek staje podmiotem zdania po przecinku i zdanie wychodzi
    #  jednym czytaniem, które polszczyzny nie jest. Statusu to nie rusza — `valid`
    #  było przed wykluczeniem i jest po nim — więc rozdzielają je same role:
    #  ciąg współrzędny niesie dwa zdania składowe, a pytanie zależne jedno.
    found = verdict("Pyta, kto płaci.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"orzeczenie": "Pyta"}]


def test_zaimek_pytajny_o_jednym_słowie_daje_zdaniu_jedno_wyprowadzenie():
    #  Wykluczenie z pozycji rzeczownej i czoło pytania wchodzą razem, bo bez
    #  pierwszego drugie dokłada każdemu takiemu zdaniu drugie wyprowadzenie:
    #  pytanie oraz zdanie oznajmujące zamknięte pytajnikiem, w którym zaimek jest
    #  podmiotem. Oba czytania mają te same role, więc widać je po ich liczbie.
    found = verdict("Kto płaci?")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"podmiot": "Kto", "orzeczenie": "płaci", GRUPA_PYTAJNA: "Kto"}]


def test_przymiotnik_za_zaimkiem_pytajnym_nie_bierze_zaimka_wskazującego():
    #  Usterka, przed którą to stoi: symbol przydawki postawiony w tym ciele
    #  zamiast terminala z wykluczeniem. Morfeusz czyta `to` także jako przymiotnik
    #  od `ten`, więc `co to` wychodzi wtedy grupą pytajną, a polszczyzna ma tam
    #  dwa zaimki obok siebie: pytanie dostaje drugie czytanie, którego nie ma.
    pierwszy = verdict("Kto inny zapisuje ustawienia?")
    assert role(pierwszy) == [
        {
            "podmiot": "Kto inny",
            "dopełnienie": "ustawienia",
            "orzeczenie": "zapisuje",
            GRUPA_PYTAJNA: "Kto inny",
        }
    ], pierwszy.explain()
    #  Zdanie to jest odrzucone i było przyjęte na czytaniu, którego polszczyzna
    #  nie ma: `Co to` wychodziło wyrażeniem przyimkowym przy `jest`, bo kopula
    #  stała wtedy bez orzecznika (:data:`olski.subset.BEZ_KOPULI`). Pytanie tego
    #  testu jest jednak to samo: gdyby `co to` stało się grupą pytajną, zdanie
    #  wróciłoby do przyjętych.
    assert verdict("Co to jest?").status == "rejected"


def test_wykluczenie_zaimka_pytajnego_nie_tyka_pozostałych_zaimków_rzeczownych():
    #  Zawężenie stoi na dwóch lematach, a nie na całej liście zaimków rzeczownych:
    #  `to` i `nic` mają u Morfeusza tę samą klasę, a pytania nie zadaje nimi nikt,
    #  więc pozycję rzeczowną mają dalej.
    assert role(verdict("To jest tanie.")) == [
        {"podmiot": "To", "orzecznik": "tanie", "orzeczenie": "jest"}
    ]
    assert role(verdict("Nic nie rośnie.")) == [{"podmiot": "Nic", "orzeczenie": "nie rośnie"}]


def test_zaimek_pytajny_zastępuje_też_poprzednik():
    #  Ta sama forma, którą zdanie pyta, stoi na czele zdania względnego, a
    #  poprzednikiem jest przy niej zaimek rzeczowny. Bez tego ciała wykluczenie z
    #  pozycji rzeczownej odbiera zdaniu względnemu z `co` każde czytanie, a ten
    #  rejestr pisze je częściej niż pytanie.
    #
    #  Poprzednik stoi tu w podmiocie, bo za orzeczeniem to samo zdanie jest
    #  wieloznaczne: `co` niesie tam także zdanie względne o poprzedniku zdaniowym,
    #  i tę cenę trzyma test niżej razem z zakupem.
    found = verdict("To, co mogło się zepsuć, jest tanie.")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {"podmiot": "To, co mogło się zepsuć,", "orzecznik": "tanie", "orzeczenie": "jest"}
    ]


def test_zdanie_względne_bez_poprzednika_jest_podmiotem_a_nie_zdaniem_współrzędnym():
    #  `Kto` bez poprzednika nazywa sam to, o czym zdanie orzeka, więc zdanie z nim
    #  jest podmiotem zdania nadrzędnego. Bez tej pozycji wychodziło ono zdaniem
    #  współrzędnym, czyli czytaniem nieprawdziwym, a rozdzielają je role: orzeczenie
    #  zdania nadrzędnego jest jedno i stoi za przecinkiem.
    found = verdict("Kto wchodzi w środek, poprzedniego zdania nie przeczytał.")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {
            "podmiot": "Kto wchodzi w środek,",
            "dopełnienie": "poprzedniego zdania",
            "orzeczenie": "nie przeczytał",
        }
    ]


def test_poprzednikiem_zaimka_co_jest_zdanie_a_nie_rzeczownik_przed_przecinkiem():
    #  Usterka, którą to łapie: jedno czoło na oba poprzedniki. Wygląda ona
    #  poprawnie, bo zdanie dalej wychodzi `valid` z jednym czytaniem, a czytanie
    #  jest inne, niż mówi zdanie: zaimek doczepia się przydawką do rzeczownika,
    #  który parę cech ma przypadkiem, i całe zdanie podrzędne wpada w dopełnienie.
    #  Nad Składnicą łapał to jeden wiersz `disagrees` i nic poza nim.
    found = verdict("Sejm zaaprobował przekroczenie, co przekreśliło sens działań.")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {"podmiot": "Sejm", "dopełnienie": "przekroczenie", "orzeczenie": "zaaprobował"}
    ]

    #  Poprzednika rzeczownikowego zaimek `który` ma dalej, i to on rozdziela te dwa
    #  czoła: bez rozdzielenia oba zdania niżej wychodzą tym samym kształtem.
    zgodny = verdict("Sejm zaaprobował przekroczenie, które przekreśliło sens działań.")
    assert zgodny.status == "valid", zgodny.explain()
    assert role(zgodny) == [
        {
            "podmiot": "Sejm",
            "dopełnienie": "przekroczenie, które przekreśliło sens działań",
            "orzeczenie": "zaaprobował",
        }
    ]


def test_poprzednik_zdaniowy_bierze_zaimek_co_a_nie_kto():
    #  Rodzaj zaimka jest tu całym kryterium: pozycja żąda poprzednika nijakiego, bo
    #  tyle niesie `co`, a `kto` jest męskoosobowy. Cechy osobnej na to nie ma, więc
    #  para zdań niżej jest jedynym miejscem, które ten wybór pilnuje.
    #
    #  Przyimek przed zaimkiem wchodzi przez czoło
    #  (`wyrażenie_przyimkowe_względne_rzeczowne`), a nie przez tę pozycję,
    #  i pierwsze zdanie jest tym, co to pokazuje.
    found = verdict("Bierzemy ostry zakręt, dzięki czemu unikamy zderzenia.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"dopełnienie": "ostry zakręt", "orzeczenie": "Bierzemy"}]

    #  Para stoi w tej samej ramie i różni ją sam zaimek, więc mówi o rodzaju, a nie
    #  o czymś innym w zdaniu. Pierwszy wiersz jest ujemny rozmyślnie: `co` daje temu
    #  zdaniu dwa czytania szykiem wewnątrz zdania podrzędnego, czyli różnicą, o
    #  której ten test nie orzeka.
    assert verdict("Cena jest niska, co przekreśla sens działań.").status != "rejected"
    assert verdict("Cena jest niska, kto przekreśla sens działań.").status == "rejected"


def test_orzecznik_wysunięty_na_czoło_nie_wypełnia_szyku_zdania_oznajmującego():
    #  Usterka, którą to łapie: szyk zdania oznajmującego żądający orzecznika bez
    #  cechy `czoło`. Wygląda ona poprawnie, bo zdanie dalej się wyprowadza, a
    #  wyprowadza się dwoma drzewami o tych samych rolach: orzecznik wysunięty
    #  wypełnia wtedy i pytanie, i szyk zdania oznajmującego zamkniętego pytajnikiem.
    #  Żądań orzecznika są trzy, więc pominięcie w którymkolwiek widać dopiero po
    #  liczbie czytań.
    found = verdict("Czym jest parser?")
    assert found.status == "valid", found.explain()
    assert role(found) == [
        {"podmiot": "parser", "orzecznik": "Czym", "orzeczenie": "jest", GRUPA_PYTAJNA: "Czym"}
    ]


def test_ciąg_pytań_zależnych_stoi_pod_jednym_czasownikiem():
    #  Czasownik bierze jedno wypełnienie, więc ciąg pytań zajmuje tę pozycję cały.
    #  Znakiem ciągu jest spójnik: przecinek w tym miejscu zamyka zdanie podrzędne,
    #  więc zdanie z przecinkiem samym nie jest ciągiem i nie ma czytania.
    #
    #  Członem jest tu `kto`, a nie `co`, i pilnuje tego sam wiersz z odrzuceniem:
    #  `co` za zdaniem domkniętym niesie zdanie względne o poprzedniku zdaniowym
    #  (`zaimek_względny_rzeczowny` w `olski/subset/podrzędne.py`), więc napis bez spójnika
    #  wyprowadza się tamtędy i o ciągu nie mówi nic. `kto` jest męskoosobowe,
    #  a tamta pozycja żąda poprzednika nijakiego, więc go nie bierze.
    found = verdict("Drzewo mówi, kto jest tematem, a kto jest nowy.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"podmiot": "Drzewo", "orzeczenie": "mówi"}]
    assert verdict("Drzewo mówi, kto jest tematem, kto jest nowy.").status == "rejected"


def test_przecinek_za_pytaniem_zależnym_zamyka_je_i_nie_otwiera_ciągu():
    #  Zdanie nadrzędne biegnie dalej spójnikiem, a przecinek przed nim zamyka
    #  pytanie zależne (`_zamykane`). Ciało ciągu bierze ten sam spójnik, więc bez
    #  tej linii nie widać, że jeden napis nie dostał dwóch wyprowadzeń.
    #
    #  Pytaniem jest tu `kto`, a nie `co`, z tego samego powodu co w teście wyżej:
    #  drugie wyprowadzenie dałoby temu napisowi zdanie względne o poprzedniku
    #  zdaniowym, a nie ciało ciągu, czyli test mierzyłby nie to, co mówi.
    found = verdict("Drzewo mówi, kto jest tematem, i liczy cenę.")
    assert found.status == "valid", found.explain()
    assert found.readings == [
        (
            {"podmiot": "Drzewo", "orzeczenie": "mówi"},
            {"dopełnienie": "cenę", "orzeczenie": "liczy"},
        )
    ]


def test_pytanie_stawia_grupę_pytajną_w_podmiocie_i_w_dopełnieniu():
    #  Dwie role, bo tyle deklaruje `_wysunięta_rola`, i obie idą tą samą
    #  drogą co w zdaniu względnym. Werdykt nazywa grupę pytajną rolą, bo pytanie
    #  przyjęte bez niej nie mówiłoby, o co pyta.
    podmiot = verdict("Który aktor robi na tobie największe wrażenie?")
    assert podmiot.status == "valid", podmiot.explain()
    assert role(podmiot)[0][GRUPA_PYTAJNA] == "Który aktor"
    dopełnienie = verdict("Które zadania gmina wykonuje?")
    assert dopełnienie.status == "valid", dopełnienie.explain()
    assert role(dopełnienie)[0][GRUPA_PYTAJNA] == "Które zadania"


def test_zdanie_pytające_żąda_pytajnika():
    #  Znak jest tu warunkiem, a nie interpunkcją do pominięcia: ta sama forma
    #  zamknięta kropką nie jest polszczyzną, a `KONIEC_ZDANIA` wziąłby oba.
    found = verdict("Który aktor robi na tobie największe wrażenie.")
    assert found.status == "rejected", found.explain()


def test_grupa_pytajna_zgadza_się_ze_swoją_głową():
    #  Zaimek stoi przy rzeczowniku, a nie nad zdaniem, więc niezgodny w rodzaju
    #  nie ma wyprowadzenia. Bez tej zgodności grupa pytajna brałaby każdą formę
    #  zaimka do każdej grupy imiennej.
    found = verdict("Który zadania gmina wykonuje?")
    assert found.status == "rejected", found.explain()


def test_grupa_wysunięta_zgadza_się_z_poprzednikiem_swoim_zaimkiem_a_nie_głową():
    #  Usterka, którą to łapie: liczba i rodzaj wypuszczone z głowy grupy, a nie
    #  z zaimka. Wygląda ona poprawnie, bo grupa imienna wszędzie indziej w tej
    #  gramatyce wypuszcza cechy swojej głowy, i przechodzi każdym zdaniem, w
    #  którym głowa jest tego samego rodzaju co poprzednik — `na podstawie
    #  której` przy `ustawa` jest właśnie takim zdaniem. Rozdziela je głowa
    #  rodzaju innego niż poprzednik: `wyniku` jest męskie, `Reguła` żeńska, a
    #  zaimek zgadza się z poprzednikiem, więc stoi w rodzaju żeńskim.
    found = verdict("Reguła, w wyniku której program zapisuje ustawienia, jest tania.")
    assert found.status == "valid", found.explain()
    głowa = verdict("Reguła, w wyniku którego program zapisuje ustawienia, jest tania.")
    assert głowa.status == "rejected", głowa.explain()


def test_grupa_wysunięta_wchodzi_oboma_szykami_zaimka_i_głowy():
    #  Polszczyzna stawia zaimek w dopełniaczu za głową i przed nią, więc oba
    #  szyki są tu ciałami produkcji. Drugiego z nich nie pilnuje nic poza tą
    #  linią: rejestr ustaw niesie sam pierwszy, więc żaden przebieg nad korpusem
    #  nie zauważy, że ciało z zaimkiem przed głową wyszło z gramatyki.
    za = verdict("Reguła, na podstawie której program zapisuje ustawienia, jest tania.")
    assert za.status == "valid", za.explain()
    przed = verdict("Program, o którego pliku ustawa mówi, jest tani.")
    assert przed.status == "valid", przed.explain()


def test_przyimek_grupy_wysuniętej_rządzi_przypadkiem_głowy_a_nie_zaimka():
    #  Przypadek rozchodzi się w tej grupie w drugą stronę niż liczba i rodzaj:
    #  zaimek jest dopełniaczem przy głowie, a przyimek pyta o przypadek głowy.
    #  Rozdziela to przyimek rządzący dopełniaczem, czyli tym przypadkiem, który
    #  zaimek ma: `bez podstawy której` wyprowadza się, bo dopełniaczem jest tam
    #  głowa, a `bez podstawie której` nie, choć `której` dopełniaczem jest w obu.
    głowa = verdict("Reguła, bez podstawy której program zapisuje ustawienia, jest tania.")
    assert głowa.status == "valid", głowa.explain()
    zaimek = verdict("Reguła, bez podstawie której program zapisuje ustawienia, jest tania.")
    assert zaimek.status == "rejected", zaimek.explain()


def test_grupa_wysunięta_bez_przyimka_zgadza_orzeczenie_z_głową_a_poprzednik_z_zaimkiem():
    #  Obie pary cech czoła widać dopiero tutaj, bo tutaj są różne, i usterką jest
    #  każda z nich wzięta za obie. Para zaimka przyjmuje `której autorzy pisze`,
    #  bo `Ustawa` jest pojedyncza; para głowy przyjmuje `Ustawy, której autorzy
    #  piszą`, bo z `autorzy` zgadza się tam wszystko.
    #
    #  Głowa jest męskoosobowa, bo przy głowie o mianowniku równym biernikowi oba
    #  te napisy wyprowadza czoło w dopełnieniu z opuszczonym podmiotem, więc
    #  odrzucenie nie mówiłoby o parach cech nic.
    found = verdict("Ustawa, której autorzy piszą, jest tania.")
    assert found.status == "valid", found.explain()
    głowa = verdict("Ustawa, której autorzy pisze, jest tania.")
    assert głowa.status == "rejected", głowa.explain()
    zaimek = verdict("Ustawy, której autorzy piszą, są tanie.")
    assert zaimek.status == "rejected", zaimek.explain()


def test_grupa_wysunięta_bez_przyimka_staje_także_w_dopełnieniu():
    #  Drugą rolę deklaruje `_wysunięta_rola` osobno, więc podmiot wyżej o niej
    #  nie świadczy. Przypadka żąda tam czasownik, a nie sama pozycja, więc
    #  przeczenie za nim przestawia grupę na dopełniacz tak samo jak przestawia
    #  czoło o jednym słowie.
    dopełnienie = verdict("Ustawa, której przepisy urzędnik ogłasza, jest tania.")
    assert dopełnienie.status == "valid", dopełnienie.explain()
    przeczenie = verdict("Ustawa, której przepisów urzędnik nie ogłasza, jest tania.")
    assert przeczenie.status == "valid", przeczenie.explain()


@pytest.mark.parametrize(
    "zdanie",
    ["Dyrektor wymienia imprezy, które zorganizował.", "Które zadania wykonuje?"],
)
def test_czoło_w_dopełnieniu_wyprowadza_zdanie_z_opuszczonym_podmiotem(zdanie):
    """Podmiot polszczyzna tutaj opuszcza, więc deklaracje są dwie, jak w zdaniu głównym.

    Zdania są dwa, bo ciała pisze obu rodzinom czół jedna funkcja, a rozejście
    się tych rodzin widać dopiero na zdaniu, którego jedna z nich nie wyprowadza.
    """
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


@pytest.mark.parametrize(
    "zdanie",
    ["Przepisy, o których mowa, są nowe.", "O którym akcie mowa?"],
)
def test_wysunięte_wyrażenie_bierze_rzeczownik_orzekający_pod_oboma_czołami(zdanie):
    """Kopuła opuszczona wchodzi pod czoło zdania względnego i pod czoło pytania.

    Pierwsze zdanie jest tym, na którym stoi rejestr ustaw: `o których mowa` niesie
    co siódme jego zdanie i bez tego ciała nie przechodzi ani jedno
    (docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze). Drugie tego rejestru nie
    ma ani razu, więc pilnuje go sama ta linia: ciało wypisane poza pętlą, która
    obie rodziny czoła obsługuje, dałoby tę konstrukcję jednej z nich, a żaden
    przebieg nad korpusem tego nie zauważy.
    """
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


def test_rzeczownik_orzekający_żąda_tego_o_czym_orzeka():
    #  Kopuła opuszczona żąda tego, o czym ten rzeczownik orzeka, więc stoi on
    #  sam wyłącznie pod wysuniętym wyrażeniem przyimkowym, a w zdaniu składowym
    #  ma przy sobie okolicznik. Bez tego żądania olski przyjmuje `Mowa.` jako
    #  zdanie, czego polszczyzna w tej formie nie ma, a obietnicą podzbioru jest,
    #  że każde zdanie olskiego jest zdaniem polskim.
    samo = verdict("Mowa.")
    assert samo.status == "rejected", samo.explain()
    okolicznik = verdict("Mowa o zadaniach.")
    assert okolicznik.status == "valid", okolicznik.explain()


def test_rzeczownik_orzekający_niesie_etykietę_roli():
    #  Zdanie to nie ma ani podmiotu, ani czasownika, więc bez tej etykiety
    #  wychodzi `valid` bez ani jednej roli, czyli bez słowa o tym, co olski w nim
    #  przyjął. Pilnuje jej samo streszczenie, bo w zdanie względne ono nie
    #  zagląda i tam ta usterka jest niewidoczna (:data:`olski.subset.ORZECZENIE_RZECZOWNIKOWE`).
    found = verdict("Mowa o zadaniach.")
    assert found.status == "valid", found.explain()
    [(reading,)] = found.readings
    assert reading[ORZECZENIE_RZECZOWNIKOWE] == "Mowa", found.explain()


def test_kopuła_opuszczona_żąda_jednej_formy_i_żąda_lematu():
    #  Dwa warunki naraz i każdy jest osobną usterką do zrobienia. Bez lematu
    #  zdaniem wychodzi każda grupa imienna w mianowniku, więc `o których cisza`
    #  przechodzi razem ze zwrotem tego rejestru, a przecinek koordynacji czyta
    #  wtedy wyliczenie jako ciąg zdań
    #  (docs/konstrukcje-gramatyczne/podrzędność.md#kopułę-opuszczoną-wpuszcza-wpis-na-lemat).
    #  Bez liczby przechodzi `o których mowy`, i mianownik sam tego nie łapie:
    #  Morfeusz zna `mowy` i jako dopełniacz pojedynczy, i jako mianownik mnogi,
    #  więc warunek na sam przypadek bierze tę formę drugim czytaniem.
    forma = verdict("Przepisy, o których mowy, obowiązują.")
    assert forma.status == "rejected", forma.explain()
    lemat = verdict("Przepisy, o których cisza, obowiązują.")
    assert lemat.status == "rejected", lemat.explain()


def test_rzeczownik_orzekający_nie_jest_orzecznikiem_pod_kopulą():
    #  Rola stoi obok orzecznika, a nie jest nim, a to zdanie jest tym, co
    #  tamto wyjście przyjmuje: orzecznik przed kopulą ramy nie żąda, więc rzeczownik
    #  wpuszczony do orzecznika stanąłby tam i przyjął zdanie, w którym olski
    #  czyta orzecznik w mianowniku (:data:`olski.subset.ORZECZENIE_RZECZOWNIKOWE`).
    found = verdict("Mowa jest ustawa.")
    assert found.status == "rejected", found.explain()


def test_oba_ciała_kopuli_opuszczonej_dają_temu_zdaniu_po_jednym_przyłączeniu():
    #  Usterka, którą to łapie: jedno z dwóch ciał zdjęte. Zdania nie odrzuca ani
    #  jedno, bo każde wyprowadza je osobno, tylko każde z innym przyłączeniem
    #  `w ustawie` — pod czołem wychodzi ono do `określa`, a w zdaniu składowym
    #  zostaje przy `mowa` — więc olski wybiera przyłączenie, którego wybierać nie
    #  ma (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    found = verdict("Ustawa określa zadania, o których mowa w ustawie.")
    assert found.status == "ambiguous", found.explain()
    [przyłączenie] = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("określa", "mowa"), found.explain()


@pytest.mark.parametrize(
    ("zdanie", "rola", "czoło"),
    [
        ("Reguła, która rozstrzyga, jest tania.", "podmiot", "która"),
        ("Polszczyzna, którą napisał autor, jest tania.", "dopełnienie", "którą"),
        ("Ustawa, której autorzy piszą, jest tania.", "podmiot", "której autorzy"),
        ("Ustawa, której przepisy urzędnik ogłasza, jest tania.", "dopełnienie", "której przepisy"),
        ("Który aktor robi na tobie największe wrażenie?", "podmiot", "Który aktor"),
        ("Które zadania gmina wykonuje?", "dopełnienie", "Które zadania"),
    ],
)
def test_czoło_niesie_etykietę_roli_którą_zajmuje(zdanie, rola, czoło):
    """Wysunięty konstytuent jest podmiotem albo dopełnieniem i tak się nazywa.

    Bez tej etykiety olski wyprowadza te zdania dokładnie tak, jak czyta je bank
    drzew, a czytanie wychodzi o tę jedną rolę uboższe, więc porównanie ról nie
    ma go z czym zestawić i złote czytanie nie równa się żadnemu
    (docs/corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym).
    Pilnuje jej samo drzewo, bo w zdanie względne streszczenie nie zagląda.

    Sześć zdań, bo tyle jest par czoła i roli: sam zaimek, grupa, w której on
    stoi, i grupa pytajna, każde w podmiocie i w dopełnieniu. Grupa pytajna
    niesie tę etykietę obok własnej, a tamtej pilnuje
    :func:`test_pytanie_stawia_grupę_pytajną_w_podmiocie_i_w_dopełnieniu`.
    """
    werdykt = verdict(zdanie)
    assert werdykt.status == "valid", werdykt.explain()
    obsadzone = {" ".join(węzeł.forms()) for węzeł in werdykt.result.readings[0].find(rola)}
    assert czoło in obsadzone


def test_etykieta_roli_nie_wpuszcza_na_czoło_swoich_pozostałych_produkcji():
    """Podmiot na czole zdania względnego jest czołem, a nie każdą grupą imienną.

    Usterka, którą to łapie, jest ceną samej etykiety: `podmiot` wpisany do ciała
    czoła bez cechy rozdzielającej wpuszcza tam `podmiot → grupa_imienna`, więc `reguła, ta
    reguła rozstrzyga` staje się zdaniem względnym, a `Który aktor robi
    wrażenie.` zdaniem oznajmującym o takim podmiocie, czyli wraca czytanie,
    które zdjął warunek na lemat.
    """
    względne = verdict("Reguła, ta reguła rozstrzyga, jest tania.")
    assert względne.status == "rejected", względne.explain()
    oznajmujące = verdict("Który aktor robi wrażenie.")
    assert oznajmujące.status == "rejected", oznajmujące.explain()


def test_czoło_jednej_rodziny_nie_staje_na_czele_drugiej():
    """Zdanie względne bierze swoje czoła, a pytanie swoje.

    Obie rodziny noszą tę samą etykietę roli, więc wartość rozdzielająca jest
    nazwą czoła, a nie jednym „wysunięte”: wspólna zlałaby je i `ustawa, który
    przepis obowiązuje` wyszłoby zdaniem względnym z grupą pytajną na czole,
    a `Który zapisuje ustawienia?` pytaniem o sam zaimek.
    """
    pytajna = verdict("Ustawa, który przepis obowiązuje, jest nowa.")
    assert pytajna.status == "rejected", pytajna.explain()
    zaimek = verdict("Który zapisuje ustawienia?")
    assert zaimek.status == "rejected", zaimek.explain()


def test_pytanie_wysuwa_grupę_pytajną_razem_z_przyimkiem():
    #  Czoło pytania jest tu drugie i jest wyrażeniem przyimkowym, a nie nowym
    #  kształtem grupy: pod przyimkiem stoi ta sama grupa pytajna, którą pytanie
    #  stawia w podmiocie i w dopełnieniu, więc rolę werdykt nazywa tak samo.
    #
    #  Napis roli jest tu drugim żądaniem, a nie sprawdzeniem tego samego dwa
    #  razy. Ta pozycja wynosi grupę pytajną ponad zdanie składowe i jest jedyną,
    #  która robi to bez zdania składowego nad sobą: okolicznik na czele zdania
    #  wynosi rolę tak samo, ale stoi pod symbolem `zdanie_składowe`, a streszczenie bierze
    #  z gałęzi to najwyższe. Bez czoła pytania w `Deklaracja.składowe` pytanie o
    #  jednym zdaniu składowym dostaje więc wielokropek mówiący, że streszczenie
    #  milczy o drugim.
    found = verdict("W którym roku ustawa weszła?")
    assert found.status == "valid", found.explain()
    assert role(found)[0][GRUPA_PYTAJNA] == "którym roku"


def test_pytanie_nie_wysuwa_z_przyimkiem_samego_zaimka():
    #  Rzeczownika ta pozycja żąda, bo pytanie bez niego każe go domyślić z
    #  tego, co stoi obok, a konstrukcji do domyślenia olski nie ma. Wpuszczony
    #  zaimek sam dałby ponadto drugie czytanie każdemu pytaniu tego kształtu.
    found = verdict("W którym ustawa weszła?")
    assert found.status == "rejected", found.explain()


def test_zdanie_względne_zgadza_się_z_poprzednikiem_i_tym_odbiera_przyłączenie():
    #  Liczba i rodzaj zaimka mówią o poprzedniku, a przypadek o roli w zdaniu
    #  podrzędnym, więc `które` w liczbie mnogiej ma się do czego przyłączyć
    #  tylko raz. Gramatyka przyłączenia nie wybiera, tak samo jak przy
    #  wyrażeniu przyimkowym; odbiera je zgodność.
    jedno = verdict("Zbiór tekstów, które są polskie, jest podzbiorem.")
    assert jedno.status == "valid", jedno.explain()
    dwa = verdict("Zbiór tekstu, który jest polski, jest podzbiorem.")
    assert dwa.status == "ambiguous", dwa.explain()
    assert dwa.result.ile == 2


def test_zdanie_względne_nie_daje_dwóch_wyprowadzeń_jednej_struktury():
    #  Usterka, którą to łapie: produkcja rekurencyjna na poziomie członu.
    #  Zdanie względne dochodzi wtedy pod przymiotnikiem i nad nim, czyli
    #  `ci [ludzie, którzy stoją]` obok `[ci ludzie], którzy stoją`,
    #  a te dwa kształty są różne, więc liczą się jako dwa czytania.
    #
    #  Zaimek jest męskoosobowy, bo `które` jest zarazem mianownikiem i
    #  biernikiem, więc zdanie z nim wychodzi drugim czytaniem — z opuszczonym
    #  podmiotem — i to czytanie zasłoniłoby usterkę, o którą tu idzie.
    #
    #  Ten sam napis łapie drugą usterkę tego samego kształtu: ciało z
    #  dopełnieniem przed czasownikiem (:data:`GRUPA_ORZECZENIA_ODWRÓCONA`) biorące
    #  całe wypełnienie ramy zamiast samego dopełnienia. Wypełnienie niesie
    #  okolicznik w swoich ciałach, a przed czasownikiem stawia go także
    #  rozwinięcie szyku, więc `na niej` wychodzi wtedy dwoma wyprowadzeniami.
    found = verdict("Istnieją ci ludzie, którzy na niej stoją.")
    assert found.status == "valid", found.explain()


def test_dopełnienie_przed_czasownikiem_nie_dubluje_szyku_zdania_głównego():
    #  Usterka, którą to łapie: szyk z dopełnieniem przed czasownikiem dopisany
    #  do grupy orzeczenia zamiast do osobnego symbolu. Zdanie główne ma ten szyk już
    #  z deklaracji swoich córek, więc dopisany tam daje jednemu napisowi dwa
    #  wyprowadzenia tego samego kształtu, czyli drugie odczytanie.
    #
    #  Zdanie podrzędne i główne stoją tu obok siebie, bo dopisanie zdejmuje
    #  odrzucenie pierwszemu i wolno mu przy tym nie ruszyć drugiego.
    podrzędne = verdict("Reguła, która tekst sprawdza, jest tania.")
    assert podrzędne.status == "valid", podrzędne.explain()
    główne = verdict("Reguła tekst sprawdza.")
    assert główne.status == "valid", główne.explain()


def test_przysłówek_względny_nie_stoi_okolicznikiem_zdania_współrzędnego():
    #  Usterka, którą to łapie: `gdzie` zostawione w terminalu okolicznika obok
    #  własnego ciała. Zdanie za przecinkiem wyprowadza się wtedy członem
    #  współrzędnym, w którym ta forma jest okolicznikiem, i jest to czytanie,
    #  którego polszczyzna nie ma; drugie czytanie zdania jest tu całą usterką,
    #  bo werdykt bez wykluczenia niczego nie odrzuca.
    #
    #  Dopełnienie jest żeńskie, bo `tekst` jest zarazem mianownikiem i
    #  biernikiem, więc zdanie z nim wychodzi drugim czytaniem na synkretyzmie
    #  i to czytanie zasłoniłoby usterkę, o którą tu idzie.
    found = verdict("Wchodzi w roadmap.md, gdzie linter sprawdza regułę.")
    assert found.status == "valid", found.explain()


def test_przysłówek_względny_określa_drugi_przysłówek():
    #  Wykluczenie wyżej zabiera parę, w której ta forma zdania nie otwiera, więc
    #  para ma własne ciało. Bez niego wykluczenie odbiera zdania, które ta proza
    #  pisze, i jest to cena płacona za czytanie, o które szło tamtemu testowi.
    found = verdict("Cena jest gdzie indziej.")
    assert found.status == "valid", found.explain()


def test_pytanie_o_okoliczność_nazywa_przysłówek_którym_pyta():
    #  Bez etykiety nad przysłówkiem pytanie wychodzi `valid` i o tym, że jest
    #  pytaniem, nie mówi nic, bo role zdania pod nim są rolami zdania
    #  oznajmującego. Werdykt jest tu przez to całym sprawdzeniem, a nie sam status.
    proste = verdict("Dlaczego gramatyka rośnie?")
    assert proste.status == "valid", proste.explain()
    assert role(proste) == [
        {"podmiot": "gramatyka", "orzeczenie": "rośnie", "okolicznik_pytajny": "Dlaczego"}
    ]


def test_przysłówek_pytajny_nie_stoi_okolicznikiem_zdania_współrzędnego():
    #  Usterka, którą to łapie: `dlaczego` zostawione w terminalu okolicznika obok
    #  własnego ciała. Zdanie za przecinkiem wyprowadza się wtedy członem
    #  współrzędnym, w którym ten przysłówek określa czasownik, pytania zależnego
    #  nie ma w zdaniu wcale, a werdykt mówi `valid`, czyli nie odrzuca niczego.
    #
    #  Streszczenie w pytanie zależne nie zagląda (`podrzędne` w
    #  ``olski/subset/deklaracja.py``), więc czytanie prawdziwe poznaje się tu po
    #  tym, że zdanie ma jedno zdanie składowe, a czytanie współrzędne po dwóch.
    found = verdict("Pyta, dlaczego gramatyka rośnie.")
    assert found.status == "valid", found.explain()
    assert role(found) == [{"orzeczenie": "Pyta"}]


def test_pytanie_o_rozstrzygnięcie_nie_dubluje_się_z_koordynacją():
    #  `czy` bierze zarazem koordynacja bez przecinka, gdzie znaczy `albo`, więc
    #  usterką byłoby czoło pytania biorące człon zamiast zdania: jeden napis
    #  dostałby wtedy oba wyprowadzenia. Rozdziela je materiał pod spójnikiem i
    #  tego pilnuje ta para.
    pytanie = verdict("Pyta, czy go to dotyczy.")
    assert pytanie.status == "valid", pytanie.explain()
    #  Drugi człon ma podmiot rzeczownikowy, a nie `to`: łącznik `to` bierze
    #  rzeczownik za sobą (``olski/subset/zdanie.py``), więc `czy to działa`
    #  wychodzi dwoma czytaniami i mierzyłoby tu co innego niż czoło pytania.
    ciąg = verdict("Pyta, kto płaci i czy program działa.")
    assert ciąg.status == "valid", ciąg.explain()


def test_okolicznik_ze_zdania_względnego_zostaje_w_nim():
    #  Zdanie względne jest zdaniem, więc stoi wśród gospodarzy przyłączenia.
    #  Bez tego okolicznik z jego wnętrza wychodzi w górę do grupy imiennej,
    #  którą to zdanie określa, i werdykt nazywa poprzednik zamiast orzeczenia.
    #  Widać to po wpisie o przyłączeniu, bo ten chodzi po lesie i granicy zdania
    #  nie zna; streszczenie o tym okoliczniku milczy, jak o całym tym zdaniu.
    found = verdict("Reguła, która rozstrzyga o zdaniu w pliku, jest tania.")
    assert found.result.ile == 2, found.explain()
    (przyłączenie,) = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("rozstrzyga", "zdaniu")


def test_streszczenie_nazywa_czasownik_zdania_a_nie_zdania_względnego():
    #  Usterka, którą to łapie: zejście do pierwszego węzła roli, gdziekolwiek on
    #  stoi. Zdanie względne stoi tu w podmiocie, czyli przed czasownikiem
    #  zdania, więc zejście bez granicy nazywa czasownikiem `rozstrzyga`, a
    #  `jest` nie pada wtedy w wierszu wcale.
    roles = role(verdict("Reguła, która rozstrzyga o zdaniu, jest tania."))[0]
    assert roles["orzeczenie"] == "jest"
    assert "wyrażenie_przyimkowe" not in roles


def test_streszczenie_nie_nazywa_roli_wziętej_ze_zdania_dopełnieniowego():
    #  Druga granica, i tu widać ją mocniej: zdanie nadrzędne dopełnienia nie ma
    #  wcale, więc `dopełnienie` wzięty ze zdania podrzędnego nazywa rolę, której to
    #  zdanie nie ma. Wiersz werdyktu łapie przy tym drugie podsumowanie: bez tej
    #  samej granicy ogłasza niezgodę o rolę, której lista czytań nie nazywa.
    #  Wieloznaczność zostaje po tej stronie granicy nazwana konstytuentem, w
    #  którym leży, i tym wierszem, a nie rolą tamtego zdania.
    found = verdict("Ustawa mówi, że organ gminy wydaje przepis.")
    assert found.result.ile == 2, found.explain()
    assert all(
        "dopełnienie" not in składowe for czytanie in found.readings for składowe in czytanie
    )
    assert found.explain() == "2 odczytania; „organ gminy wydaje przepis” ma 2 odczytania"


@pytest.mark.parametrize(
    "zdanie",
    [
        "Program zapisuje ustawienia, ponieważ linter sprawdza dokumentację.",
        "Ponieważ linter sprawdza dokumentację, program zapisuje ustawienia.",
    ],
)
def test_zdanie_okolicznikowe_wyprowadza_się_raz_w_obu_pozycjach(zdanie):
    #  Polszczyzna stawia ten okolicznik przed swoim zdaniem i za nim, a szyku
    #  wewnątrz zdania nadrzędnego nie zmienia ani jedna pozycja, ani druga.
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Cztery zdania podrzędne, po jednym na wywołanie `_zamykane`, bo pozycja
        #  dopisana jednemu z nich nie mówi nic o pozostałych trzech.
        "Dokument mówi, że cena jest niska, i liczy cenę.",
        "Parser jest tani, bo cena jest niska, i gramatyka jest tania.",
        "Dokument mówi, który parser jest tani, i liczy cenę.",
        "Parser czyta regułę, która rozstrzyga, i liczy cenę.",
    ],
)
def test_zdanie_podrzędne_zamyka_się_przecinkiem_przed_spójnikiem(zdanie):
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


def test_przecinek_przed_spójnikiem_bez_zdania_podrzędnego_nie_wyprowadza_się():
    #  Usterka, którą to łapie: przecinek zamykający wpuszczony do koordynacji
    #  zamiast do zdania podrzędnego. Polszczyzna nie stawia go przed `i` między
    #  dwoma zdaniami, więc olski wyprowadzałby wtedy napis, którego ona nie ma.
    found = verdict("Parser jest tani, i gramatyka jest tania.")
    assert found.status == "rejected", found.explain()


@pytest.mark.parametrize(
    "zdanie",
    [
        "Program zapisuje ustawienia ponieważ linter sprawdza dokumentację.",
        "Ponieważ linter sprawdza dokumentację program zapisuje ustawienia.",
    ],
)
def test_zdanie_okolicznikowe_niesie_przecinek_po_stronie_zdania_nadrzędnego(zdanie):
    #  Usterka, którą to łapie: ciało bez cechy wiążącej przecinek z pozycją.
    #  Ciało z przecinkiem z przodu, wpuszczone na czoło zdania, wyprowadza napis
    #  zaczynający się przecinkiem, a ciało z przecinkiem z tyłu, wpuszczone na
    #  koniec, wyprowadza zdanie bez przecinka przed spójnikiem. Polszczyzna
    #  stawia ten znak zawsze, więc oba są zdaniami, których nie ma.
    found = verdict(zdanie)
    assert found.status == "rejected", found.explain()


@pytest.mark.parametrize(
    ("zdanie", "status"),
    [
        ("Program zapisuje ustawienia, gdyż linter sprawdza dokumentację.", "valid"),
        ("Gdyż linter sprawdza dokumentację, program zapisuje ustawienia.", "rejected"),
    ],
)
def test_spójnik_przyczyny_dopowiedzianej_nie_wysuwa_swojego_zdania(zdanie, status):
    #  Wysunięcie jest faktem o słowie, a nie o pozycji, więc ciała biorą dwie
    #  różne listy lematów. Bez tego podziału olski wyprowadza `Gdyż pada,
    #  zostaję w domu.`, czego polszczyzna nie ma, a `ponieważ` w tym samym
    #  miejscu ma i bierze je ciało wysunięte.
    found = verdict(zdanie)
    assert found.status == status, found.explain()


def test_spójnik_żądający_trybu_przypuszczającego_nie_otwiera_okolicznika():
    #  `aby` żąda zdania w trybie przypuszczającym, a cechy trybu żadna produkcja
    #  zdania nie niesie, więc spójnik nie ma czego żądać, choć samą cząstkę `by`
    #  forma czasownika bierze. Wpuszczone na listę spójników okolicznikowych
    #  wyprowadzałoby zdanie, którego polszczyzna nie ma, przeciwko obietnicy
    #  podzbioru.
    found = verdict("Program zapisuje ustawienia, aby linter sprawdza dokumentację.")
    assert found.status == "rejected", found.explain()


def test_streszczenie_nazywa_okolicznik_zdaniowy_a_wnętrza_jego_nie_otwiera():
    #  Usterka, którą to łapie: zejście po role do wnętrza tego okolicznika.
    #  Zdanie podrzędne stoi tu przed zdaniem nadrzędnym, więc zejście bez
    #  granicy nazywa podmiotem `linter`, czyli podmiot tamtego zdania, a nie
    #  tego. Rola jest przy tym nazwana całym napisem, bo symbol stoi i wśród
    #  ról, i wśród zdań podrzędnych.
    roles = verdict("Ponieważ linter sprawdza dokumentację, program zapisuje ustawienia.")
    [(streszczenie,)] = roles.readings
    assert streszczenie["podmiot"] == "program"
    assert (
        streszczenie["okolicznik_zdaniowy"] == "Ponieważ linter sprawdza dokumentację, → zapisuje"
    )


def test_okolicznik_zdaniowy_dochodzi_do_obu_zdań_i_werdykt_to_nazywa():
    #  Okolicznik za zdaniem dopełnieniowym dochodzi do niego i do zdania nad
    #  nim, i są to dwa czytania, które polszczyzna nad tym zdaniem ma. Widać je
    #  po roli, bo streszczenie nazywa ją wtedy, gdy okolicznik stoi w zdaniu
    #  streszczanym, a milczy, gdy stoi w tamtym.
    found = verdict("Pomiar mówi, że autor pisze, ponieważ tekst jest gotowy.")
    assert found.result.ile == 2, found.explain()
    assert found.result.różniące == ("okolicznik_zdaniowy",)
    assert {OKOLICZNIK_ZDANIOWY in reading for reading in role(found)} == {False, True}


def test_okolicznik_zdaniowy_dochodzi_do_całego_ciągu_współrzędnego():
    #  `aby rozwiązać problemy` mówi tu o obu członach naraz, a ciało stawiające
    #  ten okolicznik przy zdaniu składowym daje samo czytanie o członie drugim.
    #  Usterka, którą to łapie, nie jest odrzuceniem: zdanie wychodzi wtedy
    #  jednoznaczne i jednoznaczne jest w nim czytanie, którego czytelnik nie bierze.
    found = verdict("Dwoisz się i troisz, aby rozwiązać problemy.")
    assert found.result.ile == 2, found.explain()
    assert {drugie[OKOLICZNIK_ZDANIOWY] for _pierwsze, drugie in found.readings} == {
        ", aby rozwiązać problemy → troisz",
        ", aby rozwiązać problemy → Dwoisz",
    }


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Okolicznik za zdaniem i przed nim, każdy nad zdaniem o jednym członie.
        "Program zapisuje ustawienia, ponieważ tekst jest gotowy.",
        "Gdyby tekst był gotowy, program zapisałby ustawienia.",
    ],
)
def test_zdanie_o_jednym_członie_nie_bierze_okolicznika_nad_ciągiem(zdanie):
    #  Ciało nad ciągiem żąda ciągu cechą, bo nad zdaniem pojedynczym dawałoby ten
    #  sam napis drugim kształtem: raz z okolicznikiem przy członie, raz nad ciągiem
    #  o jednym członie. Powrotem tamtego stanu jest liczba czytań wyższa niż jeden.
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()
