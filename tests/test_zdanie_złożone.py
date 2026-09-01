"""Zdanie złożone: czym wypowiedzenie spina dwa zdania i co obejmuje znak.

Plik pyta o jedną warstwę, a nie o jedną konstrukcję,
i jest to ta warstwa, która ma swój plik w rejestrze konstrukcji
(docs/konstrukcje-gramatyczne/zdanie-złożone.md);
kryterium przynależności podaje nagłówek tamtego rejestru.
Interpunkcja należy tu obiema stronami:
zdaniowa, czyli ta, która zdania rozdziela,
oraz obejmująca, czyli cudzysłów i nawias.
Przecinek koordynujący na wszystkich trzech poziomach naraz
pyta się tutaj, a nie w grupie imiennej, bo najwyższy z nich jest zdaniem.

Czy zdanie jest olskim — dwa korpusy zdań i kształt odrzucenia —
pyta ``tests/test_subset.py``.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import EMPTY, Word, bierze
from olski.morph import analyse
from olski.subset import (
    GRAMMAR,
    SPÓJNIK_BEZ_PRZECINKA,
    SPÓJNIK_PRZECINKOWY,
    SPÓJNIK_PYTAJNY,
    SPÓJNIKI_PRZECINKOWE,
    SPÓJNIKI_SKORELOWANE,
    WTRĄCENIE,
    WTRĄCENIE_MYŚLNIKOWE,
    WYRAŻENIE_PRZYIMKOWE,
)
from tests.test_werdykt import role, verdict


@pytest.mark.parametrize(
    "zdanie",
    [
        "Wstaję, wyglądam przez okno.",
        "Kobiety muszą zakrywać włosy, ramiona, nogi.",
        "Plik jest nowy, duży.",
    ],
)
def test_przecinek_koordynuje_na_każdym_poziomie_i_wyprowadza_raz(zdanie: str):
    #  Trzy poziomy, bo przecinek dopisany do dwóch z nich zostawia trzeci na
    #  spójniku i nikt tego nie zobaczy po zdaniu odrzuconym gdzie indziej. Raz,
    #  a nie w ogóle: przecinek zdaniowy miał konkurować z przecinkiem w grupie
    #  imiennej, a docs/subset.md trzyma pomiar mówiący, ile tej konkurencji
    #  jest nad bankiem drzew.
    assert verdict(zdanie).status == "valid"


def test_czytanie_rozcinające_zdanie_nie_wychodzi_streszczeniem_całości():
    #  Usterka, którą to łapie: streszczenie czytające się jak streszczenie całości.
    #  Morfeusz zna `szczęśliwi` jako `szczęśliwić fin:sg:ter:imperf`, więc `i szczęśliwi`
    #  wychodzi drugim zdaniem składowym bez podmiotu. Streszczenie jedno na zdanie
    #  mówi `orzecznik: wolni, równi`, o reszcie zdania milczy i nie widać,
    #  że dwa czytania różni rozcięcie zdania na dwa, a nie żadna rola.
    found = verdict("Ludzie są wolni, równi i szczęśliwi.")
    assert found.readings == [
        ({"podmiot": "Ludzie", "orzecznik": "wolni, równi i szczęśliwi", "orzeczenie": "są"},),
        (
            {"podmiot": "Ludzie", "orzecznik": "wolni, równi", "orzeczenie": "są"},
            {"orzeczenie": "szczęśliwi"},
        ),
    ]
    #  Tę różnicę nazywa rolą samo pytanie o zdanie całe: każde zdanie składowe
    #  osobno niesie jeden orzecznik, bo stoi w jednym z tych dwóch czytań.
    assert found.result.różniące == ("orzecznik",)


def test_zdanie_współrzędne_dostaje_streszczenie_na_każde_zdanie_składowe():
    #  Zdanie jednoznaczne, więc streszczenia nie bierze się z żadnej wieloznaczności:
    #  dopełnienie jest w drugim zdaniu składowym, a podmiot i czasownik w pierwszym,
    #  i widać to po tym, w którym streszczeniu która rola stoi. Streszczenie jedno na
    #  zdanie nazywa pierwsze wystąpienie roli, więc wychodzi z niego werdykt `valid`
    #  o dopełnieniu i podmiocie z dwóch różnych zdań składowych.
    [streszczenie] = verdict("Autor działa i zapisuje ustawienia.").readings
    assert streszczenie == (
        {"podmiot": "Autor", "orzeczenie": "działa"},
        {"dopełnienie": "ustawienia", "orzeczenie": "zapisuje"},
    )


def _biorące(lemat):
    """Produkcje, w których ciele stoi ten znak."""
    return [
        produkcja
        for produkcja in GRAMMAR.productions
        if any(_znak(część, lemat) for część in produkcja.body)
    ]


def _znak(część, lemat):
    """Czy ta część ciała jest tym znakiem."""
    return (
        isinstance(część, Word)
        and bierze(część, "interp", lemat, frozenset({lemat}), {}, EMPTY) is not None
    )


def test_średnik_bierze_jedna_produkcja_więc_nie_ma_z_czym_konkurować():
    #  Na tej jedynce stoi zdanie, że średnik nie odbiera jednoznaczności ani
    #  jednemu zdaniu: znak wchodzący w jedno ciało albo wyprowadza zdanie tą
    #  produkcją, albo nie wyprowadza go wcale. Drugie ciało z tym znakiem czyni
    #  z tego zera liczbę do zmierzenia i ten test jest tym, co o tym powie.
    #  Myślnik tę jedynkę stracił, kiedy weszła para; jego cenę zmierzono i trzyma
    #  ją docs/konstrukcje-gramatyczne/zdanie-złożone.md.
    assert len(_biorące(";")) == 1, _biorące(";")


@pytest.mark.parametrize("lemat", ["—", "–"])
def test_para_myślników_żąda_w_środku_symboli_rozłącznych(lemat):
    #  Myślnik stoi w czterech ciałach, więc jedynki wyżej mieć nie może, a zdanie
    #  o jednoznaczności zostaje to samo i stoi na czym innym: para żąda w środku
    #  grupy imiennej, wyrażenia przyimkowego albo zdania składowego, a żaden z tych
    #  trzech napisów nie ma wyprowadzenia pozostałymi — wyrażenie przyimkowe
    #  zaczyna się przyimkiem, którego grupa imienna nie bierze, a zdanie składowe
    #  żąda czasownika albo rzeczownika orzekającego.
    #  Usterka, którą to łapie: symbol dopisany w środek pary tak, że dwa ciała
    #  biorą ten sam napis, czyli dokładają czytanie każdemu zdaniu z parą.
    w_środku = set()
    for produkcja in _biorące(lemat):
        if produkcja.head != WTRĄCENIE_MYŚLNIKOWE:
            continue
        [rdzeń] = [część for część in produkcja.body if not _znak(część, lemat)]
        w_środku.add(rdzeń.name)
    assert w_środku == {"grupa_imienna", "wyrażenie_przyimkowe", "zdanie_składowe"}


def test_ciała_dwukropka_żądają_za_nim_symboli_rozłącznych():
    #  Dwukropek stoi w kilku ciałach, więc jedynki wyżej mieć nie może, a zdanie
    #  o jednoznaczności zostaje to samo i stoi na czym innym: za dwukropkiem
    #  jedno ciało żąda zdania, drugie grupy imiennej, a trzecie ciągu pytań
    #  zależnych, i żaden z tych trzech napisów nie ma wyprowadzenia pozostałymi —
    #  grupa imienna zdaniem nie jest, a zdanie składowe nie zaczyna się ani `czy`
    #  (:data:`SPÓJNIK_NA_CZELE` tego lematu nie ma), ani zaimkiem, który pozycji
    #  rzeczownej nie dostał (:data:`ZAIMEK_PYTAJNO_RZECZOWNY`).
    #  Usterka, którą to łapie: symbol dopisany za dwukropkiem do któregoś z tych
    #  ciał tak, że dwa biorą ten sam napis.
    za_dwukropkiem = set()
    for produkcja in _biorące(":"):
        [gdzie] = [
            numer
            for numer, część in enumerate(produkcja.body)
            if _znak(część, ":")
        ]
        za_dwukropkiem.add(produkcja.body[gdzie + 1].name)
    assert za_dwukropkiem == {"zdanie", "grupa_imienna", "ciąg_pytajny"}


@pytest.mark.parametrize(
    "zdanie",
    [
        #  `czy` podporządkowuje u olskiego pytanie o rozstrzygnięcie.
        "Czy zmiana idzie w dobrą stronę?",
        #  `to` jest zaimkiem, a Morfeusz daje mu czytanie spójnikowe.
        "To samo wejście daje tę samą odpowiedź.",
    ],
)
def test_lemat_o_własnej_pozycji_nie_staje_na_czele_zdania_spójnikiem(zdanie: str):
    #  Usterka, przed którą to stoi: czoło zdania pisane wykluczeniem zamiast listy
    #  lematów. Oba te zdania mają wtedy dwa czytania, a polszczyzna czyta je raz;
    #  docs/subset.md trzyma pomiar, przy którym lista wygrała z wykluczeniem.
    assert verdict(zdanie).status == "valid"


def test_człon_bez_czasownika_nie_wchodzi_za_spójnikiem_dokładającym_skutek():
    #  Usterka, którą to łapie: SPÓJNIK_PRZECINKOWY postawiony przed tym członem
    #  zamiast węższej listy. Obie listy niosą `a` i `czyli`, więc zdanie przyjęte
    #  nie powie, którą wzięto; rozdziela je `więc`, za którym polszczyzna samej
    #  grupy imiennej nie stawia.
    assert role(verdict("Parser jest tani, a nie Morfeusz."))
    assert not role(verdict("Parser jest tani, więc Morfeusz."))


def test_człon_bez_czasownika_przepuszcza_zdanie_nadrzędne_za_przecinkiem():
    #  Usterka, którą to łapie: ciało bez przecinka zamykającego, czyli to samo
    #  przeoczenie, które zdaniom podrzędnym naprawia `_zamykane`. Zdanie
    #  nadrzędne biegnie za tym członem i biegnie spójnikiem bez przecinka, więc
    #  bez tego ciała `i pilnuje go test` nie ma się o co zaczepić.
    zamknięty = verdict(
        "Granica pakietu jest rozstrzygnięciem, a nie przypadkiem, i pilnuje go test."
    )
    assert zamknięty.readings, zamknięty.explain()


def test_ciąg_skorelowany_bierze_liczbę_z_członu_a_nie_wartością():
    #  Usterka, którą to łapie: `number="pl"` przepisane z dwóch ciał koordynacji
    #  obok. Ciąg z przeczeniem rozdziela człony, zamiast je sumować, więc orzeka
    #  w liczbie pojedynczej, a wartość `pl` odbiera temu zdaniu każde czytanie.
    assert verdict("Ani parser, ani linter nie rośnie.").status == "valid"
    assert verdict("Ani parsery, ani lintery nie rosną.").status == "valid"
    #  Zgodność zostaje przy tym zgodnością: człon w innej liczbie niż orzeczenie
    #  czytania nie ma.
    assert verdict("Ani parser, ani linter nie rosną.").status == "rejected"


def test_ciąg_skorelowany_nie_bierze_lematu_o_własnej_pozycji():
    #  Usterka, którą to łapie: `czy` dopisane do listy skorelowanych. Lemat ten
    #  podporządkowuje pytanie o rozstrzygnięcie, więc ciąg dawałby `Pyta, czy
    #  rośnie, czy maleje.` drugie wyprowadzenie tego samego kształtu, a werdykt
    #  zostawałby ten sam: zdanie jest wieloznaczne i bez tego czytania, więc
    #  pomiar różnicowy tej ceny nie pokaże (docs/subset.md).
    assert SPÓJNIK_PYTAJNY not in SPÓJNIKI_SKORELOWANE


def test_analiza_staje_na_spójniku_przed_którym_stoi_zbędny_przecinek():
    #  Usterka, którą to łapie: `i` dopisane do listy spójników skorelowanych.
    #  Terminal ciągu wpuszcza tę formę na czoło członu, czyli wszędzie tam, gdzie
    #  człon może się zacząć, więc analiza idzie przez nią dalej, niż napis na to
    #  pozwala: przecinka przed `i` polszczyzna nie stawia (docs/subset.md).
    stanęło = verdict("Cena rośnie, i linter sprawdza tekst.")
    assert stanęło.status == "rejected", stanęło.explain()
    assert stanęło.zatrzymanie == "i", stanęło.explain()


def test_spójnik_ma_czoło_całego_zdania_a_nie_czoło_zdania_składowego():
    #  Granica biegnie między dwoma poziomami, a jedno zdanie sprawdza oba.
    #  Usterka po stronie zdania składowego: SPÓJNIK dopisany do pętli, która
    #  daje cząstce i przysłówkowi czoło składowego, albo ciało czoła postawione
    #  przy symbolu `zdanie` zamiast przy `wypowiedzenie`. `więc` stoi wtedy w dwóch pozycjach
    #  naraz — na czele drugiego składowego i w jego liście okoliczników — więc
    #  zdanie spięte przecinkiem dostaje drugie czytanie tego samego kształtu.
    spięte = verdict("Cena jest niska, więc gramatyka jest tania.")
    assert spięte.status == "valid", spięte.explain()
    #  Ten sam spójnik między dwoma zdaniami bez przecinka, czyli druga z dwóch
    #  klas, na jakie gramatyka dzieli spójnik zdaniowy.
    assert verdict("Cena jest niska i gramatyka jest tania.").status == "valid"


def test_cząstka_przecząca_nie_spina_dwóch_zdań_w_ciąg_współrzędny():
    #  Morfeusz czyta `nie` także jako spójnik, a gramatyka ma dla tej formy
    #  pozycję przy czasowniku, więc bez wykluczenia w klasie spójników bez
    #  przecinka jeden napis ma dwa wyprowadzenia, a drugie jest czytaniem,
    #  którego polszczyzna nie ma. Usterka, którą to łapie: wykluczenie zdjęte
    #  przy okazji dopisywania lematu do listy spójników przecinkowych.
    assert not role(verdict("Program zapisuje ustawienia nie linter sprawdza tekst."))
    assert verdict("Program nie zapisuje ustawień.").status == "valid"


def test_rozdzielające_a_nie_licencjonuje_formy_przyimkowej_zaimka():
    #  `a` niesie u Morfeusza czytanie przyimka, którego wyrażenie przyimkowe nie
    #  bierze, więc licencji nie udziela też forma stojąca za nim. Usterka, którą
    #  to łapie: warunek w `po_przyimku` pytający o samą część mowy, przy którym
    #  `Cena jest niska, a nie.` wychodzi członem bez czasownika, a `nie` w nim
    #  biernikiem zaimka `on`.
    assert not role(verdict("Cena jest niska, a nie."))
    #  Przyimek, który gramatyka bierze, licencjonuje dalej.
    assert role(verdict("Program zapisuje ustawienia dla niego."))


def test_cudzysłów_przepuszcza_przypadek_grupy_którą_obejmuje():
    #  Usterka, którą to łapie: przypadek wypisany wartością zamiast zmiennej.
    #  Polszczyzna odmienia to, co cudzysłów obejmuje, wedle roli grupy, więc
    #  wartość wpisana w produkcję przyjmuje jeden z tych dwóch napisów i odrzuca
    #  drugi, a oba są zdaniami tej dokumentacji.
    mianownik = verdict("Same „Zasady techniki prawodawczej” są rozporządzeniem.")
    assert mianownik.status == "valid", mianownik.explain()
    orzecznik = verdict("Ustawa jest przepisem „Zasad techniki prawodawczej”.")
    assert orzecznik.status == "valid", orzecznik.explain()


def test_przytoczenie_bierze_licencję_od_cudzysłowu_a_nie_od_pisma_napisu():
    #  Usterka, którą to łapie: warunek pytający o samą formę. Litera jest u
    #  Morfeusza skrótem — `B` pod lematem `bajt` — i skrótów ta gramatyka nie ma,
    #  więc bez cudzysłowu napisowi nie zostaje ani jedno czytanie do wzięcia.
    #
    #  `nacisnąć`, a nie `wcisnąć`: drugie ma drugą pozycję ramy, a grupa w
    #  cudzysłowie idzie przez każdy przypadek, więc para dokłada temu zdaniu
    #  czytanie z `„B”` w celowniku i pytanie o cudzysłów tonie w nim.
    #  Pytanie jest tu o odczytanie, a nie o jednoznaczność: napis nieodmienny
    #  spełnia każde żądanie przypadku, więc stoi i w dopełnieniu, i w okoliczniku
    #  narzędnikowym (``WIELOZNACZNE_PRZEZ_NARZĘDNIK`` w ``tests/test_subset.py``),
    #  a licencji udziela mu
    #  jedno i drugie tak samo.
    przytoczony = verdict("Naciśnij klawisz „B” i zapisz plik konfiguracyjny.")
    assert przytoczony.readings, przytoczony.explain()
    assert not verdict("Naciśnij klawisz B i zapisz plik konfiguracyjny.").readings


def test_przytoczeniem_jest_napis_domknięty_i_jednosłowny():
    #  Usterka, którą to łapie: warunek pytający o jeden znak z dwóch albo o
    #  cudzysłów gdziekolwiek w zdaniu, zamiast o oba sąsiedztwa napisu. Wnętrzem
    #  dłuższym niż jedno słowo jest grupa imienna albo nic.
    assert not verdict("Wciśnij klawisz „B.").readings
    assert not verdict("Znam „to nie zdanie”.").readings


def test_przytoczenie_zostawia_tytuł_jednosłowny_grupie_imiennej():
    #  Usterka, którą to łapie: GRUPA_JEDNYM_SŁOWEM opróżniona albo zawężona do
    #  samego rzeczownika. Czytanie nieodmienne spełnia każdy przypadek i niesie
    #  rodzaj nijaki, więc zamiana daje takiemu napisowi drugie czytanie w roli
    #  podmiotu, a orzecznikowi żeńskiemu odbiera zgodność.
    dopełnienie = verdict("Program zapisuje „ustawienia”.")
    assert dopełnienie.status == "valid", dopełnienie.explain()
    orzecznik = verdict("„Reguła” jest tania.")
    assert orzecznik.status == "valid", orzecznik.explain()


def test_wtrącenie_nie_oddaje_zdaniu_ról_ze_swojego_wnętrza():
    #  Wtrącenie jest rolą całym napisem, więc zejście po role zatrzymuje się na
    #  nim (`Deklaracja.podrzędne`). Bez tego wyrażenie przyimkowe z jego wnętrza
    #  wychodzi rolą przyłączaną zdania, którego ono nie określa, i werdykt mówi o
    #  zdaniu nieprawdę, zamiast odrzucić.
    werdykt = verdict("Cena jest niska (koszt w pliku).")
    assert werdykt.status == "valid", werdykt.explain()
    [(czytanie,)] = werdykt.readings
    assert czytanie[WTRĄCENIE] == "( koszt w pliku ) → jest", czytanie
    assert WYRAŻENIE_PRZYIMKOWE not in czytanie, czytanie


def test_para_myślników_nie_oddaje_zdaniu_ról_ze_swojego_wnętrza():
    #  To samo, o co pyta test wyżej, na drugim znaku i na wypełnieniu, którego
    #  nawias nie bierze: para obejmuje całe zdanie składowe, a rolą jest ona sama.
    #  Bez wpisu w `MIJANE` i w `podrzędne` (`DEKLARACJA`) podmiot z jej wnętrza
    #  wychodzi podmiotem zdania, które go nie ma.
    werdykt = verdict("Cena — gramatyka rośnie — jest niska.")
    assert werdykt.status == "valid", werdykt.explain()
    [(czytanie,)] = werdykt.readings
    assert czytanie[WTRĄCENIE_MYŚLNIKOWE] == "— gramatyka rośnie — → jest", czytanie
    assert czytanie["podmiot"] == "Cena", czytanie


def test_para_myślników_staje_w_każdym_miejscu_okolicznika_i_wyprowadza_raz():
    #  Usterka, którą to łapie: para wpisana ciałem na jedno miejsce zamiast do
    #  listy okoliczników. Miejsce na okolicznik wylicza się za każdą córką
    #  (`olski/precedencja.py`), a te trzy napisy stawiają parę za każdą z nich
    #  po kolei; ciało wypisane bierze zwykle to miejsce, które autor zapamiętał.
    for zdanie in (
        "Program — w pliku — zapisuje ustawienia.",
        "Program zapisuje — w pliku — ustawienia.",
        "Program zapisuje ustawienia — w pliku — dotąd.",
    ):
        assert verdict(zdanie).status == "valid", verdict(zdanie).explain()


def test_myślnik_pojedynczy_rozdziela_dwa_zdania_mimo_pary():
    #  Usterka, którą to łapie: para wpuszczona tak, że bierze także jeden znak,
    #  czyli dwa ciała na jeden napis. Zdanie rozdzielone myślnikiem ma czytanie
    #  jedno i miało je przed parą.
    werdykt = verdict("Cena jest niska — parser rośnie.")
    assert werdykt.status == "valid", werdykt.explain()


def test_wtrącenie_w_zdaniu_względnym_wychodzi_jednym_czytaniem():
    #  Nawias przed przecinkiem zamykającym zdanie względne ma jednego gospodarza,
    #  bo przyłączony do zdania nadrzędnego stanąłby za tym przecinkiem, czyli
    #  dałby inny napis.
    werdykt = verdict("Reguła, która rozstrzyga (niżej), jest tania.")
    assert werdykt.status == "valid", werdykt.explain()


def test_zdanie_względne_na_końcu_zdania_bierze_nawias_od_zdania_nadrzędnego():
    #  Usterka, którą to łapie: ta sama pozycja dopisana przez symetrię do ciała
    #  zdania względnego bez przecinka. Ten napis obsługuje w całości pozycja przy
    #  zdaniu składowym, więc druga dołożyłaby mu drugiego gospodarza i drugie
    #  czytanie, nie kupując ani jednego zdania.
    werdykt = verdict("Program zapisuje regułę, która rozstrzyga (niżej).")
    assert werdykt.status == "valid", werdykt.explain()


def test_zdanie_bierze_jeden_znak_rozdzielający_a_nie_ciąg_takich_znaków():
    #  Produkcja stoi na poziomie zdania, a `zdanie` żadnego z tych znaków nie ma,
    #  więc rekurencji nie ma czym zbudować i drugi znak w zdaniu odrzuca je. Jest
    #  to granica wypowiedziana, a nie przeoczona: docs/subset.md trzyma ją wśród
    #  tego, czego olski nie bierze, i ten test jest jej świadkiem.
    assert verdict("Cena jest niska; gramatyka jest bezkontekstowa.").status == "valid"
    dwa = verdict("Cena jest niska; gramatyka jest bezkontekstowa; parser jest tani.")
    assert dwa.status == "rejected", dwa.explain()


@pytest.mark.parametrize(("znak", "status"), [("—", "valid"), ("–", "valid"), ("-", "rejected")])
def test_myślnik_rozdziela_zdanie_a_łącznik_nie(znak, status):
    #  Usterka, którą to łapie: łącznik dopisany do lematów myślnika. Polszczyzna
    #  spaja nim wewnątrz wyrazu — `UTF-8` — a rozdzielanie zdania należy do pauzy
    #  i półpauzy, więc znaki są trzy i tylko dwa z nich rozdzielają
    #  (:data:`olski.subset.MYŚLNIK`).
    found = verdict(f"Cena jest niska {znak} gramatyka jest bezkontekstowa.")
    assert found.status == status, found.explain()


@pytest.mark.parametrize("lemat", sorted(SPÓJNIKI_PRZECINKOWE))
def test_dwie_klasy_spójnika_zdaniowego_nie_zachodzą_na_siebie(lemat: str):
    #  Lemat wzięty obiema pozycjami dałby polszczyźnie i `A, ale B`, i `A ale B`,
    #  a pominięty na liście nie wszedłby do żadnej z nich. Literówka wygląda
    #  dokładnie tak jak pominięcie: pozycja z przecinkiem milczy wtedy o słowie
    #  i nie widać tego po żadnym zdaniu.
    [segment] = analyse(lemat)
    czytania = [(r.tag.pos, r.lemma, segment.lematy) for r in segment.readings]
    brane = [c for c in czytania if bierze(SPÓJNIK_PRZECINKOWY, *c, {}, EMPTY) is not None]
    assert brane, (lemat, czytania)
    assert not [c for c in czytania if bierze(SPÓJNIK_BEZ_PRZECINKA, *c, {}, EMPTY) is not None]
    #  Spójnik spoza listy idzie odwrotnie, więc klasy pokrywają ją całą.
    jedno = frozenset({"i"})
    assert bierze(SPÓJNIK_BEZ_PRZECINKA, "conj", "i", jedno, {}, EMPTY) is not None
    assert bierze(SPÓJNIK_PRZECINKOWY, "conj", "i", jedno, {}, EMPTY) is None


def test_rozdzielające_a_nie_wchodzi_do_wyrażenia_przyimkowego():
    #  Usterka, którą to łapie, jest usterką werdyktu, a nie pokrycia: `a` ma w
    #  słowniku czytanie przyimkowe rządzące mianownikiem, więc bez tego warunku
    #  każde czytanie tego zdania niesie okolicznik `a linter`, którego zdanie nie
    #  ma, i przecinek przed spójnikiem nie ma czego kupić.
    found = verdict("Program zapisuje ustawienia, a linter sprawdza polszczyznę.")
    assert found.status == "valid", found.explain()
    #  Żądanie idzie do każdego streszczenia, bo zdanie ma dwa składowe,
    #  a okolicznik z tego czytania stoi w drugim z nich.
    assert all(
        "wyrażenie_przyimkowe" not in składowe
        for czytanie in found.readings
        for składowe in czytanie
    )
