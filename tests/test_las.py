"""Co werdykt czyta z lasu: liczbę czytań, ich kolejność, streszczenie i gospodarza.

Las odpowiada na pytanie, na które lista czytań odpowiedzieć nie umie:
czytań bywa więcej, niż wydruk wypisuje
(``MAX_READINGS`` w ``olski/parse/las.py``),
więc liczba, numer czytania i to, czym czytania się różnią,
biorą się z lasu, a nie z tej listy
(docs/parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań).

Wydruk werdyktu stoi tu razem z lasem, a nie osobno w ``tests/test_werdykt.py``:
wiersz o przyłączeniu i wiersz o konstytuencie rozbieżnym są zapytaniem o las
wypisanym słowami, więc rozcięte na dwa pliki zostawiłyby w każdym pół zdania.
``tests/test_werdykt.py`` pyta o te odpowiedzi, które werdykt dokłada nad rozbiorem,
a ``tests/test_subset.py`` o to, które zdanie olski przyjmuje.
"""

import os
import subprocess
import sys
from dataclasses import replace

import pytest

pytest.importorskip("morfeusz2")

from olski.parse import MAX_READINGS, Leaf, Pozycja, las, parse
from olski.segmentacja import morphology
from olski.subset import DEKLARACJA, GRAMMAR
from tests.test_werdykt import role, verdict


@pytest.mark.parametrize(
    ("zdanie", "czytań"),
    [
        #  Pod jedną pozycją stoją tu dwie produkcje, a rodzic przyjmuje jedną,
        #  więc iloczyn liczony po samych pozycjach naliczyłby trzy czytania.
        #  Dwa, a nie jedno, bo notacja czyta się nieodmiennie, więc stoi także
        #  w okoliczniku narzędnikowym
        #  (``WIELOZNACZNE_PRZEZ_NARZĘDNIK`` w ``tests/test_subset.py``).
        ("Zobacz docs/subset.md.", 2),
        #  Tu jest odwrotnie: jeden kształt przechodzi na dwa sposoby, więc dwa
        #  naliczyłaby pozycja rozdzielona po cechach.
        ("Projekt jest dla przyjemności.", 1),
    ],
)
def test_czytania_liczy_się_po_kształtach_a_nie_po_wyprowadzeniach(zdanie: str, czytań: int):
    """Oba nadmiary są z przeciwnych stron, i las nie ma prawa na żaden z nich wpaść.

    Zdanie, które przestało pokazywać swój nadmiar, zabiera podstawę wywodowi z
    docs/parsowanie.md#co-się-pakuje-rozstrzyga-tożsamość-czytania, i nie widać
    tego po żadnej liczbie: test przechodziłby wtedy sam z siebie.
    """
    wynik = parse(GRAMMAR, morphology(zdanie))
    assert wynik.ile == len(wynik.readings) == czytań, wynik.status


def _liście(drzewo):
    return (
        [drzewo]
        if isinstance(drzewo, Leaf)
        else [liść for dziecko in drzewo.children for liść in _liście(dziecko)]
    )


def _po_liściach(liście, zamiast=None):
    """Segmenty zdania zawężone do odczytań, jakie te liście niosą.

    Zdanie zawężone tak wyprowadza się dokładnie tyle razy,
    ile razy te odczytania to drzewo licencjonują,
    i dlatego odczytania liści sprawdza sam parser,
    a nie unifikacja napisana w tym pliku drugi raz.

    ``zamiast`` podmienia odczytanie jednego liścia, bo pytanie o pojedyncze
    odczytanie jest pytaniem o jeden liść: reszta zdania idzie wtedy tym
    odczytaniem, którym ją drzewo pokazuje.
    """
    liść_podmieniany, odczytanie = zamiast or (None, None)
    return [
        replace(
            liść.segment,
            readings=(odczytanie if liść is liść_podmieniany else liść.reading,),
        )
        for liść in liście
    ]


@pytest.mark.parametrize(
    "zdanie",
    [
        #  szynki jest dopełniaczem szynki i mianownikiem szynk, a pozycja pod
        #  człon_imienny licencjonuje z tych dwóch sam dopełniacz. Poprawnym zdaniem
        #  to nie jest, więc czytelnik ogląda te drzewa, żeby zobaczyć różnicę.
        "Koszt szynki przewyższa koszt chleba.",
        #  Dobry jest przymiotnikiem zgodnym z kod i nazwiskiem rządzącym
        #  dopełniaczem, a kod ma obok mianownika dopełniacz kody, więc dwa
        #  czytania słownikowe wiążą się tu w ciele parami.
        "Dobry kod zapisuje ustawienia.",
        #  Zdanie poprawne, o jednym czytaniu: ustawienia jest dopełniaczem
        #  liczby pojedynczej i biernikiem mnogiej, a pozycja dopełnienia bierze
        #  drugie z nich.
        "Program zapisuje ustawienia.",
        #  Jeden kształt przechodzi tu na dwa sposoby, czyli w dwóch liczbach, i
        #  cechy liścia idą wtedy za tą, którą drzewo pokazuje.
        "Projekt jest dla przyjemności.",
        #  Zdanie względne, żeby żądanie cech schodziło głębiej niż o jedną córkę.
        "Program zapisuje ustawienia, które sprawdza linter.",
        #  Najkrótszy kształt wychodzący z dwóch ciał naraz, zaimkowego i
        #  rzeczownikowego, więc liść niesie odczytania obu
        #  (`Las._wsparte_kształtu` w olski/parse/las.py): tu ta suma może wyjść za szeroko.
        "Znam go.",
    ],
)
def test_liść_wyliczonego_drzewa_niesie_odczytania_licencjonujące_jego_pozycję(zdanie: str):
    """Drzewo pokazane czytelnikowi ma być tym, co gramatyka nad tymi odczytaniami wyprowadza.

    Pakowanie wyłącza z tożsamości odczytania lemat i część mowy
    (`Node.signature` w olski/parse/czytanie.py),
    więc wyprowadzenia różne samą morfologią są jedną klasą,
    a przedstawiciel klasy mógłby nieść odczytania liści wzięte spoza niej:
    dopełniacz pod pozycją dopełniacza jest wtedy w drzewie mianownikiem,
    i myli to jedynego czytelnika, jakiego drzewo ma —
    tego, kto je wypisuje, żeby zrozumieć wieloznaczność.

    Sprawdzane jest każde odczytanie liścia, a nie samo pierwsze, bo werdykt
    wypisuje je wszystkie (`Las._wsparte` w olski/parse/las.py): odczytanie wpisane
    tam bez licencji mówiłoby autorowi, że forma stoi w tym odczytaniu zdania
    czymś, czym gramatyka jej nie bierze.
    """
    for drzewo in parse(GRAMMAR, morphology(zdanie)).readings:
        liście = _liście(drzewo)
        for liść in liście:
            for odczytanie in liść.odczytania:
                zawężone = las(GRAMMAR, _po_liściach(liście, (liść, odczytanie)))
                sygnatury = {czytanie.signature() for czytanie in zawężone.czytania()}
                assert drzewo.signature() in sygnatury, (
                    f"{zdanie}: „{liść.segment.form}” jako {odczytanie}"
                )


def test_odczytanie_liścia_spoza_licencjonujących_zabiera_drzewu_wyprowadzenie():
    """Przesłanka testu wyżej: zawężenie do odczytań liści potrafi wyjść źle.

    Bez tego przechodziłby on sam z siebie,
    bo zawężenie, którego żadne odczytanie nie odrzuca, nie sprawdza niczego.
    Mianownik `szynk` pod pozycją dopełniacza jest dokładnie tym,
    co tamten test ma łapać, więc tutaj stoi wstawiony ręcznie.
    """
    for drzewo in parse(GRAMMAR, morphology("Koszt szynki przewyższa koszt chleba.")).readings:
        liście = _liście(drzewo)
        [szynki] = [liść for liść in liście if liść.segment.form == "szynki"]
        assert {c for odczytanie in szynki.odczytania for c in odczytanie.tag.get("case")} == {
            "gen"
        }
        [mianownik] = [
            odczytanie for odczytanie in szynki.segment.readings if odczytanie.lemma == "szynk"
        ]
        assert mianownik not in szynki.odczytania
        zawężone = las(GRAMMAR, _po_liściach(liście, (szynki, mianownik)))
        assert drzewo.signature() not in {
            czytanie.signature() for czytanie in zawężone.czytania()
        }


def test_pozycja_odrzucona_przez_rodzica_zostaje_w_tablicy():
    #  To jest przesłanka pierwszego z tych dwóch zdań i nie widać jej po liczbie
    #  czytań: tablica domyka pozycję, gdy produkcja doszła do końca ciała, a o
    #  cechy pyta dopiero unifikacja po lesie. `zobacz` ma ramę domyślną, bez
    #  narzędnika, a notacja rejestru dostaje czytanie nieodmienne i przechodzi w
    #  każdym przypadku, więc `orzecznik` buduje się nad nią i ginie u rodzica.
    segments = morphology("Zobacz docs/subset.md.")
    assert not [
        węzeł
        for reading in parse(GRAMMAR, segments).readings
        for węzeł in reading.find("orzecznik")
    ]
    assert las(GRAMMAR, segments).wyprowadzenia(Pozycja("orzecznik", (1, 2)))


#: Siedem przyłączeń, czyli czytań więcej, niż lista wypisuje.
#: Oba testy pod spodem żądają od zdania tego samego, więc stoi tu raz.
SIEDEM_PRZYŁĄCZEŃ = (
    "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci "
    "w firmie w kraju w Polsce."
)


def test_liczba_czytań_nie_urywa_się_tam_gdzie_lista_czytań():
    """Werdykt nad zdaniem o siedmiu przyłączeniach ma być liczbą, a nie „64+”.

    Las liczy sumą po klasach korzenia, więc `MAX_READINGS` ogranicza wypisywanie
    drzew i nie ogranicza liczenia ich.
    """
    wynik = parse(GRAMMAR, morphology(SIEDEM_PRZYŁĄCZEŃ))
    assert wynik.ile == 128
    assert len(wynik.readings) == MAX_READINGS
    assert wynik.truncated


def test_lista_czytań_niesie_każde_streszczenie_raz():
    """Streszczenie wypisane drugi raz nie mówi nic ponad to, które stoi nad nim.

    Streszczenie nazywa pierwszy modyfikator zdania i jego gospodarza, więc nad
    zdaniem o siedmiu przyłączeniach po kilka czytań ma jeden napis. Liczbę
    czytań podaje las, a nie ta lista, więc skrócenie listy jej nie rusza.
    """
    napisy = [
        tuple(sorted(streszczenie.items()))
        for streszczenie in role(verdict(SIEDEM_PRZYŁĄCZEŃ))
    ]
    assert len(set(napisy)) == len(napisy)
    assert len(napisy) < MAX_READINGS


def test_wypisane_czytania_stoją_w_każdym_przebiegu_w_tej_samej_kolejności():
    """Urwana lista ma być za każdym razem tymi samymi streszczeniami.

    Kolejność ustala `wyprowadzenia` w `olski/parse/las.py` i tam stoi wywód;
    ten test pilnuje, żeby zbiór postawiony gdziekolwiek po drodze z lasu
    nie oddał jej z powrotem haszowaniu napisów.
    Po liczbie czytań tego nie widać, bo ta jest sumą po klasach,
    a ziarno haszowania jest jedno na proces, więc przebiegi są dwa i osobne.
    Drugie zdanie wchodzi po drugą taką listę, tę pod konstytuentem:
    kształty wybiera tam odsiew po zbiorze pozycji żywych.
    """
    tekst = f"{SIEDEM_PRZYŁĄCZEŃ} Ustawa mówi, że organ gminy wydaje przepis."
    kod = f"import olski.check; olski.check.main(['--readings', '-c', {tekst!r}])"
    przebiegi = [
        subprocess.run(
            [sys.executable, "-c", kod],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONHASHSEED": ziarno},
        )
        for ziarno in ("1", "2")
    ]
    for przebieg in przebiegi:
        assert przebieg.returncode == 0, przebieg.stderr
    wypisane = [w for w in przebiegi[0].stdout.splitlines() if w.lstrip().startswith("- ")]
    #  Wierszy jest kilka, a nie jeden, i są wśród nich oba rodzaje listy:
    #  inaczej nie ma tu kolejności, którą haszowanie mogłoby pomylić.
    assert len(wypisane) > 1
    assert "czyta się tak:" in przebiegi[0].stdout
    assert przebiegi[0].stdout == przebiegi[1].stdout


def test_rola_różniąca_czytania_zostaje_nazwana_zza_granicy_wyliczania():
    """Werdykt liczony po streszczeniach milczałby o wyborze, który to zdanie zostawia.

    Zdanie jest przepisem z rejestru ustaw
    (docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem)
    i ma czytań więcej, niż `MAX_READINGS` wypisuje, a wypisane zgadzają się co
    do podmiotu. Ta zgoda jest przesłanką testu: gdy zniknie, zdanie przestaje
    pokazywać, o co tu idzie, a asercja niżej przechodzi sama z siebie.
    """
    werdykt = verdict(
        "Plan ochrony dóbr kultury na czas wojny zawiera wskazanie zadań "
        "ochrony dóbr kultury na czas wojny z określeniem niezbędnych priorytetów."
    )
    assert werdykt.result.truncated
    assert len({streszczenie.get("podmiot") for streszczenie in role(werdykt)}) == 1
    assert "podmiot" in werdykt.result.różniące


def test_rola_stojąca_w_czytaniu_dwa_razy_nie_jest_niezgodą_między_czytaniami():
    """Zdanie współrzędne ma własny podmiot, a to nie jest różnica między czytaniami.

    Pozycje o etykiecie `podmiot` mają w lesie tego zdania różne rozpiętości,
    więc porównanie ich wszystkich naliczyłoby niezgodę tam, gdzie oba czytania
    mówią to samo. Jednym wystąpieniem roli jest to, które nazywa streszczenie:
    pierwsze w tym zdaniu składowym. Zdanie jest wieloznaczne czytaniem
    słownikowym wewnątrz podmiotu drugiego składowego, o którym oba streszczenia
    mówią jeden napis, więc niezgody nie ma tu żadna rola i mówi to wiersz o
    konstytuencie.
    """
    werdykt = verdict(
        "Autor działa i dodatkowych przedstawicieli wyznacza zainteresowana rada gminy."
    )
    assert werdykt.result.ile == 2
    assert all(len(czytanie.find("podmiot")) == 2 for czytanie in werdykt.result.readings)
    assert werdykt.result.różniące == ()


def test_niezgoda_w_drugim_zdaniu_składowym_zostaje_nazwana_rolą():
    """Werdykt milczący o tej roli czyta się jak usterka narzędzia.

    Pierwsze wystąpienie każdej roli w tym zdaniu jest w składowym pierwszym i jest
    w obu czytaniach to samo, a różnica siedzi w drugim. Pytanie zadane samemu
    zdaniu całemu zostawia więc `2 odczytania` nad dwoma streszczeniami, które podmiot
    i dopełnienie rozdzielają, czyli werdykt nie mówi, czym te dwa czytania się różnią.
    """
    werdykt = verdict("Program zapisuje ustawienia i przepis wydaje organ.")
    assert werdykt.result.różniące == ("podmiot", "dopełnienie")
    assert [drugie for _pierwsze, drugie in werdykt.readings] == [
        {"podmiot": "przepis", "dopełnienie": "organ", "orzeczenie": "wydaje"},
        {"podmiot": "organ", "dopełnienie": "przepis", "orzeczenie": "wydaje"},
    ]


def _role_czytań(zbudowany):
    """Rozpiętości podmiotu i dopełnienia w kolejnych czytaniach, po jednej parze."""
    return [
        (
            frozenset(węzeł.span for węzeł in drzewo.find("podmiot")),
            frozenset(węzeł.span for węzeł in drzewo.find("dopełnienie")),
        )
        for drzewo in zbudowany.czytania()
    ]


@pytest.mark.parametrize(
    "zdanie",
    [
        "Koszt samej szynki przewyższa koszt szynki z dodatkami.",
        "Program zapisuje ustawienia w pliku w katalogu.",
        "Program zapisuje ustawienia i użytkownik czyta plik w katalogu.",
    ],
)
def test_las_numeruje_te_i_tylko_te_rozdania_ról_które_wychodzą_z_jego_drzew(zdanie: str):
    """Pytanie o czytanie nazwane rolami ma odpowiadać to, co daje wyliczenie.

    Sprawdzane w obie strony, bo osobno łatwo o obie pomyłki: rozdanie z drzewa
    nieznalezione i rozdanie znalezione bez drzewa, które by je dało. Drugie jest
    tym, co robi porównanie po jednej roli naraz — bierze podmiot z jednego
    czytania i dopełnienie z drugiego — więc iloczyn niżej sprawdza właśnie je.

    Sam numer sprawdza się przeciw miejscu w wyliczeniu, bo tym numer jest:
    numer liczony osobno byłby kolejnością czytań wypisaną drugi raz.
    """
    zbudowany = las(GRAMMAR, morphology(zdanie))
    z_drzew = _role_czytań(zbudowany)
    assert len(set(z_drzew)) > 1, "zdanie bez dwóch rozdań niczego tu nie rozstrzyga"
    for podmioty in {rozdanie[0] for rozdanie in z_drzew}:
        for dopełnienia in {rozdanie[1] for rozdanie in z_drzew}:
            role = {"podmiot": podmioty, "dopełnienie": dopełnienia}
            szukane = (podmioty, dopełnienia)
            oczekiwany = z_drzew.index(szukane) + 1 if szukane in z_drzew else None
            assert zbudowany.numer_czytania(role) == oczekiwany, role


def test_czytanie_nazwane_rolami_znajduje_się_zza_granicy_wyliczania():
    """Pytanie o cudze czytanie idzie do lasu, bo lista czytań urywa się przed nim.

    Zdanie o siedmiu przyłączeniach ma osiem rozdań ról, a ostatnie z nich stoi
    za granicą wypisywania: rozdanie liczone po liście wychodziłoby przepadłe.
    Wieloznaczne są zaś dokładnie te zdania, na których ta granica pada, czyli te,
    o które to pytanie w ogóle się zadaje.

    Numer wychodzi zza tej granicy razem z odpowiedzią, bo granica jest wydruku,
    a nie wyliczenia: gdyby wiązała także tu, tamto rozdanie nie miałoby numeru.
    """
    zbudowany = las(GRAMMAR, morphology(SIEDEM_PRZYŁĄCZEŃ))
    czytania = _role_czytań(zbudowany)
    poza_listą = set(czytania) - set(czytania[:MAX_READINGS])
    assert len(poza_listą) == 1
    for podmioty, dopełnienia in poza_listą:
        numer = zbudowany.numer_czytania({"podmiot": podmioty, "dopełnienie": dopełnienia})
        assert numer is not None and numer > MAX_READINGS


def test_pusty_zbiór_żąda_czytania_które_tej_roli_nigdzie_nie_obsadza():
    """Etykieta bez rozpiętości jest żądaniem, a nie pominięciem etykiety.

    Bez tego czytanie z dopełnieniem przechodziłoby jako cudze czytanie
    bez dopełnienia, czyli jako to samo czytanie zawężone,
    a `Outcome.agreement` w `harness/pomiar.py` liczy taką parę jako niezgodę.
    """
    zbudowany = las(GRAMMAR, morphology("Program zapisuje ustawienia."))
    podmiot = frozenset({(0, 1)})
    assert zbudowany.numer_czytania({"podmiot": podmiot, "dopełnienie": frozenset({(2, 3)})}) == 1
    assert zbudowany.numer_czytania({"podmiot": podmiot, "dopełnienie": frozenset()}) is None


def test_werdykt_nazywa_przyimek_i_głowy_a_nie_wylicza_iloczynu():
    """Wpisów jest tyle, ile nierozstrzygniętych wyborów, a nie ile czytań.

    Iloczyn rośnie tu z każdym wyrażeniem przyimkowym, a wyborów jest po jednym na
    wyrażenie, i to jest ta różnica, dla której werdykt pyta las, a nie listę
    czytań (docs/parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań).
    """
    zdanie = "Program zapisuje ustawienia w pliku w katalogu w systemie w sieci w firmie w kraju."
    wynik = parse(GRAMMAR, morphology(zdanie), deklaracja=DEKLARACJA)
    assert wynik.ile == 64
    przyłączenia = wynik.przyłączenia
    assert [p.modyfikator for p in przyłączenia] == [
        "w pliku",
        "w katalogu",
        "w systemie",
        "w sieci",
        "w firmie",
        "w kraju",
    ]
    assert przyłączenia[0].gospodarze == ("zapisuje", "ustawienia")
    assert przyłączenia[-1].gospodarze == ("zapisuje", "firmie")


@pytest.mark.parametrize(
    ("zdanie", "modyfikator", "gospodarze"),
    [
        (
            "Władza zwierzchnia w Rzeczypospolitej Polskiej należy do Narodu.",
            "w Rzeczypospolitej Polskiej",
            ("Władza", "należy"),
        ),
        (
            "Sejm sprawuje kontrolę nad działalnością Rady Ministrów.",
            "nad działalnością Rady Ministrów",
            ("sprawuje", "kontrolę"),
        ),
    ],
)
def test_gospodarza_nazywa_jego_głowa_a_nie_materiał_przed_modyfikatorem(
    zdanie: str, modyfikator: str, gospodarze: tuple[str, ...]
):
    """Głowa rozdziela gospodarzy, którym materiał przed modyfikatorem jest wspólny.

    Grupa imienna otwierająca pierwsze z tych zdań dzieli ten materiał z całym
    zdaniem, więc nazwa wzięta z materiału daje na oboje jeden napis; wywód
    mieści docs/parsowanie.md#werdykt-jest-zapytaniem-o-las-a-nie-listą-czytań.
    Oba zdania są wypisane razem z werdyktem w
    docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem.
    """
    found = verdict(zdanie)
    [przyłączenie] = found.result.przyłączenia
    assert przyłączenie.modyfikator == modyfikator
    assert przyłączenie.gospodarze == gospodarze


def test_werdykt_nazywa_konstytuent_gdy_dwa_czytania_mają_jedno_streszczenie():
    """Dwa czytania o jednym napisie mają zostać nazwane, a nie zostać samą liczbą.

    Różni je tu czytanie słownikowe: `zainteresowana` jest i rzeczownikiem, a
    `rada` formą `rad`, więc podmiotem jest w obu czytaniach ten sam napis i
    lista czytań niesie jeden wpis. Roli zdania grupa imienna nie nosi, więc oba
    jej kształty streszczają się pustym słownikiem i listy pod wierszem nie
    dostaje: wiersz jest tu całą odpowiedzią, a różnicę niesie głowa, której
    streszczenie nie nazywa (todo/). Zdanie jest z rejestru ustaw
    (docs/ustawy.md#co-gramatyka-z-tego-wyprowadza).
    """
    found = verdict("Dodatkowych przedstawicieli wyznacza zainteresowana rada gminy.")
    assert found.result.ile == 2, found.explain()
    assert len(found.readings) == 1
    [rozbieżność] = found.result.rozbieżności
    assert (rozbieżność.konstytuent, rozbieżność.ile) == ("zainteresowana rada gminy", 2)
    assert rozbieżność.czytania == (({},),)
    assert found.rozbieżne == []
    assert found.explain() == "2 odczytania; „zainteresowana rada gminy” ma 2 odczytania"


def test_konstytuent_będący_zdaniem_streszcza_się_swoimi_rolami():
    """Wiersz nazywa konstytuent, a lista pod nim ma powiedzieć, czym te czytania się różnią.

    Zdanie podrzędne role ma, tyle że własne, więc streszczone osobno mówi to,
    czego streszczenie zdania nad nim nie mówi: podmiot i dopełnienie są w tych
    dwóch czytaniach zamienione.
    """
    found = verdict("Ustawa mówi, że organ gminy wydaje przepis.")
    assert len(found.readings) == 1
    [rozbieżność] = found.rozbieżne
    assert [
        (składowe["podmiot"], składowe["dopełnienie"])
        for (składowe,) in rozbieżność.czytania
    ] == [("organ gminy", "przepis"), ("przepis", "organ gminy")]


def test_wiersz_o_konstytuencie_nie_powtarza_wyboru_nazwanego_przyłączeniem():
    """Wpisów ma być tyle, ile wyborów, więc wybór nazwany raz nie wraca drugim wierszem.

    Dwadzieścia cztery czytania tego zdania składają się z trzech gospodarzy
    jednego wyrażenia przyimkowego, dwóch drugiego, dwóch kształtów `ulicy
    Pomorskiej` i dwóch miejsc, w których kończy się drugie z tych wyrażeń:
    `zapewnić` ma drugą pozycję ramy, więc `połowie bieżącego roku` czyta się
    także jej celownikiem, a przed nim zostaje samo `w pierwszej`.
    Wieloznaczność zamknięta w zdaniu podrzędnym jest poza zasięgiem
    streszczenia: wiersz o przyłączeniu granicy tego zdania nie zna, więc gdyby
    ten wiersz szedł po samej granicy, wypisałby te same dwa wybory jeszcze raz,
    konstytuentem długim na całe zdanie podrzędne. Zdanie jest ze Składnicy.
    """
    found = verdict(
        "Władze miasta zapewniają, że remont kapitalny torowiska na ulicy Pomorskiej "
        "rozpocznie się w pierwszej połowie bieżącego roku."
    )
    assert found.result.ile == 24, found.explain()
    assert [p.modyfikator for p in found.result.przyłączenia] == [
        "na ulicy Pomorskiej",
        "w pierwszej",
    ]
    [rozbieżność] = found.result.rozbieżności
    assert (rozbieżność.konstytuent, rozbieżność.ile) == ("ulicy Pomorskiej", 2)


@pytest.mark.parametrize(
    ("zdanie", "ile", "konstytuent"),
    [
        (
            "Podręczniki powinny uwzględniać zasadę równych praw kobiet i mężczyzn.",
            7,
            "równych praw kobiet",
        ),
        (
            "Po upływie kadencji rady gminy zarząd działa do dnia wyboru nowego zarządu.",
            6,
            "nowego zarządu",
        ),
    ],
)
def test_wiersz_o_konstytuencie_nazywa_najwęższy_z_nich(zdanie: str, ile: int, konstytuent: str):
    """Jeden wybór to jeden wiersz, choć wieloznaczność jednego słowa wychodzi w górę.

    W pierwszym zdaniu `równych` jest przymiotnikiem albo rzeczownikiem, i przez
    to czyta się dwoma sposobami `równych praw kobiet`, a trzema `równych praw
    kobiet i mężczyzn`, czyli człon ciągu z drugiego czytania; sam ciąg wiersza
    nie dostaje, bo granicę członu pokazuje nawias w napisie roli. W drugim
    dwoma sposobami czyta się `nowego zarządu`, a przez to i `wyboru nowego
    zarządu`, czyli konstytuent o innym początku. Naprawić trzeba w obu wypadkach
    jedno słowo, więc wiersz jest jeden i nazywa napis najkrótszy. Pierwsze
    zdanie jest ze Składnicy, drugie z ustawy o samorządzie gminnym
    (docs/ustawy.md#wieloznaczność-jest-tu-odczytem-z-6-ale-nie-jest-zarzutem).
    """
    found = verdict(zdanie)
    assert found.result.ile == ile, found.explain()
    assert [r.konstytuent for r in found.result.rozbieżności] == [konstytuent]

