"""Cztery odpowiedzi, które werdykt dokłada nad rozbiorem, i podsumowanie nad tekstem.

O zdaniu przyjętym i o odrzuconym rozstrzyga gramatyka,
więc pyta o nie ``tests/test_subset.py``.
Fragment jest napisem, którego nikt nie napisał jako zdania,
a niedomknięcie zdaniem bez ostatniego znaku;
czemu granica między nimi biegnie tędy, wywodzi ``docs/extraction.md``.
Zatrzymanie nazywa formę, na której stanęła analiza zdania odrzuconego,
a po co ta odpowiedź jest, mówi ``docs/pisanie-po-olsku.md``.
Wszystkie trzy mówią o napisie autora, a nie o grafie segmentacji.

Czwartą jest żądanie pozycji, czyli to, czego czasownik żąda od słowa,
które w jego pozycji stanęło; sam plik żądań sprawdza ``tests/test_żądania.py``,
a tutaj pyta się o to, którą pozycję czytanie obsadziło i którym słowem.
Tu też spotyka się ono z drugą połową pytania, czyli z deklaracją osób
projektu (``olski/osoby.py``), bo dopiero obie razem dają odpowiedź o zdaniu.

Piąte pytanie jest o podsumowanie tekstu,
bo od niego zależy, czego pomiar pokrycia nie liczy jako zdania.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.osoby import Osoby
from olski.segmentacja import morphology
from olski.werdykt import (
    FRAGMENT,
    NIEDOMKNIĘTE,
    WIELOZNACZNE,
    Naprawa,
    Podsumowanie,
    check,
    dalsze_zatrzymania,
    nad_tekstem,
    niespełnione_żądania,
    werdykt,
    zatrzymania,
)


#  Wołają je też pliki pytające o gramatykę, o las i o segmentację,
#  a kopia w każdym z nich rozjechałaby się po cichu.
#  Wyliczenia nie ma, bo plik warstwy dopisany do `tests/` wydłuża tę listę,
#  a nic o niej wtedy nie przypomina.
def verdict(text):
    found = check(text)
    assert len(found) == 1, f"expected one sentence, got {len(found)}"
    return found[0]


def role(werdykt):
    """Role czytań zdania o jednym zdaniu składowym, po słowniku na czytanie.

    Streszczeniem czytania jest krotka o słowniku na każde zdanie składowe
    (``describe`` w ``olski/parse/streszczenie.py``).
    Zdanie o dwóch składowych wywraca ten pomocnik,
    zamiast wyjść z niego samym składowym pierwszym.
    """
    return [jedno for (jedno,) in werdykt.readings]


def test_werdykt_niesie_zdanie_tak_jak_stoi_a_nie_graf_segmentacji():
    #  Morfeusz dzieli ktoś na kto i ś obok formy całej, więc jest to zdanie,
    #  które wypisywało się jako cztery słowa, choć stoją w nim trzy.
    assert verdict("Ktoś zapisał plik.").text == "Ktoś zapisał plik."


def test_fragment_bez_znaku_zamykajacego_nie_jest_zdaniem_odrzuconym():
    #  Nagłówek i pozycja listy dochodzą do olskiego jako akapity, a produkcja
    #  wypowiedzenie żąda na końcu kropki, więc odrzucone mierzyłyby ekstrakcję.
    assert verdict("Zapisywanie pliku").status == FRAGMENT
    assert verdict("Nowa program zapisuje ustawienia.").status == "rejected"


def test_napis_który_olski_czyta_po_domknięciu_nie_jest_fragmentem():
    """Fragment jest aparatem dokumentu, a to jest zdanie bez ostatniego znaku.

    Rozdział ten jest całym zyskiem z werdyktu `unclosed`: bez niego autor, który
    kropki nie postawił, dostawał odpowiedź, że nikt tego zdaniem nie napisał.
    """
    niedomknięte = verdict("Cena jest niska")
    assert niedomknięte.status == NIEDOMKNIĘTE
    assert niedomknięte.naprawa == Naprawa("kropka na końcu", 1)


def test_niedomknięte_pytanie_dostaje_pytajnik_a_nie_kropkę():
    #  Kropka stoi w DOMKNIĘCIA pierwsza, więc pytajnik wychodzi tylko tam, gdzie
    #  kropka czytania nie daje: PYTAJNIK bierze jeden znak, a KONIEC_ZDANIA trzy.
    assert verdict("Który program zapisuje ustawienia").naprawa == Naprawa("pytajnik na końcu", 1)


def test_domknięcie_wieloznaczne_też_jest_niedomknięciem_a_nie_fragmentem():
    """Warunkiem jest czytanie, a nie czytanie jedno.

    `Program zapisuje ustawienia w pliku.` wychodzi dwoma czytaniami, bo `w pliku`
    dochodzi raz do czasownika, a raz do dopełnienia. Brak kropki jest w tym
    napisie tym samym brakiem co wyżej, a warunek na jedno czytanie schowałby go
    pod odpowiedzią o wieloznaczności.
    """
    niedomknięte = verdict("Program zapisuje ustawienia w pliku")
    assert niedomknięte.status == NIEDOMKNIĘTE
    assert niedomknięte.naprawa.czytań > 1


# --------------------------------------------------------------------------- #
# Poprawka jednego znaku, czyli pierwsze ze znalezisk
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "zdanie",
    [
        'Przepisem "Zasad techniki prawodawczej" jest ustawa.',
        #  Cudzysłów pojedynczy Morfeusz scala ze słowem w jedną formę, więc
        #  warunek pytający o samą formę nie widzi go wcale.
        "Przepisem 'Zasad techniki prawodawczej' jest ustawa.",
    ],
)
def test_zdanie_cytujące_spoza_rejestru_jest_znaleziskiem_i_zostaje_odrzucone(zdanie):
    """Poprawka mówi autorowi, co zrobić, a status mówi, że gramatyka tego nie bierze."""
    naprawialne = verdict(zdanie)
    assert naprawialne.status == "rejected"
    assert naprawialne.zgłoszenie
    assert naprawialne.naprawa == Naprawa("cudzysłów „ i ” w miejsce tego, którym zdanie cytuje", 1)


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Łącznik: myślnik w jego miejsce dałby tu odczytanie, a poprawki na
        #  niego nie ma i cenę tego trzyma docs/subset.md.
        "Cena jest niska - gramatyka jest tania.",
        #  Apostrof w środku słowa: warunek pytający o samo zawieranie brał go za
        #  cytat nad kilkunastoma zdaniami prozy tego repozytorium.
        "Reguła nazywa document's own list.",
        #  Zdanie angielskie: reguła stojąca na samym znaku strzelała nad prozą
        #  tego repozytorium kilkadziesiąt razy i za każdym razem właśnie tak.
        'A reference with no antecedent, "this difference".',
    ],
)
def test_poprawki_nie_dostaje_zdanie_któremu_podmiana_znaku_odczytania_nie_daje(zdanie):
    assert verdict(zdanie).naprawa is None


def test_napis_któremu_brakuje_dwóch_znaków_zostaje_fragmentem_bez_poprawki():
    #  Usterka, którą to łapie: poprawka składana z dwóch znaków naraz. Napis
    #  jest tu bez kropki i cytuje spoza rejestru, więc po jednej poprawce dalej
    #  nie ma odczytania, a po obu naraz stałby się `unclosed` i wypadł z
    #  fragmentów, którymi mierzy się ekstrakcja (docs/extraction.md).
    napis = verdict('Przepisem "Zasad techniki prawodawczej" jest ustawa')
    assert napis.status == FRAGMENT
    assert napis.naprawa is None


def test_zdanie_naprawialne_liczy_się_i_do_znalezisk_i_do_milczenia():
    #  Dwa liczniki, bo mówią o czym innym: znalezisko o autorze, a milczenie o
    #  podzbiorze. Zdanie zliczone tylko w pierwszym podniosłoby pokrycie o
    #  konstrukcję, której gramatyka nie wyprowadza.
    tekst = 'Przepisem "Zasad techniki prawodawczej" jest ustawa.'
    podsumowanie = Podsumowanie.ze_zdań(nad_tekstem(tekst))
    assert (podsumowanie.naprawialne, podsumowanie.bez_odczytania) == (1, 1)
    assert podsumowanie.wieloznaczne == 0


# --------------------------------------------------------------------------- #
# Zatrzymania, czyli miejsca, na których staje analiza
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    ("zdanie", "oczekiwane"),
    [
        #  Werdykt nazywa jedno miejsce, bo jedno jest końcem przedrostka, który
        #  się analizuje, a zdanie o kilkunastu wyrazach ma ich kilka i pierwsze
        #  zasłania resztę.
        ("Dokument nazywa role, w jakich ktoś czyta, a dla każdej: pytanie.", ("czyta", "a", ":")),
        ("Zapisz plik konfiguracyjny.", ()),
    ],
)
def test_zatrzymania_nazywają_każde_miejsce_a_nie_samo_pierwsze(zdanie, oczekiwane):
    assert zatrzymania(morphology(zdanie)) == oczekiwane


def test_analiza_wznawia_się_za_formą_zatrzymania_a_nie_na_niej():
    #  Usterka, którą to łapie: przebieg wznowiony na formie zatrzymania. Formy,
    #  której nie wzięła żadna analiza częściowa, nie weźmie też analiza zaczęta
    #  od niej, więc taki przebieg nazywałby ją bez końca.
    #  Oba zatrzymania stoją tu na spójniku i biorą się z przecinka przed nim,
    #  którego polszczyzna tam nie stawia (docs/subset.md). Drugiego nie znajdzie
    #  przebieg wznowiony na formie pierwszego, bo tamta forma nie ruszy się z
    #  miejsca, więc para jest tu całym pytaniem: jedno zatrzymanie przechodziłoby
    #  i wznowieniu błędnemu.
    zdanie = "Cena rośnie, i linter sprawdza tekst, i parser czyta tekst."
    assert zatrzymania(morphology(zdanie)) == ("i", "i")


@pytest.mark.parametrize(
    ("zdanie", "wszystkie"),
    [
        #  Zdanie o dwóch zatrzymaniach, czyli jedyne z niepustą odpowiedzią.
        ("Czym milczenie z braku pokrycia różni się od wstrzymania się, wywodzi linter.md.", ("się", ",")),
        #  Zdanie o jednym: kawałek za nim rozbiera się i nie staje już nigdzie.
        ("Czego olski nie obiecuje, mówią dwie sekcje o tym, po jednej na tor.", ("na",)),
        #  Zdanie, które nie staje wcale, bo dochodzi do końca i nic go nie domyka.
        ("Nowa program zapisuje ustawienia.", ()),
    ],
)
def test_zatrzymania_dalsze_nazywają_to_samo_co_przebieg_od_początku_zdania(zdanie, wszystkie):
    #  Usterka, którą to łapie: ``Result.furthest`` przestaje nazywać ten węzeł,
    #  na którym staje rozbiór całości, bo na tej jednej przesłance stoi skrót.
    #  Krotka pełna stoi obok, żeby przypadek nie zszedł po cichu do pustej,
    #  w której porównanie nie może wypaść źle.
    assert zatrzymania(morphology(zdanie)) == wszystkie
    assert dalsze_zatrzymania(verdict(zdanie)) == wszystkie[1:]


def test_zatrzymania_dalsze_bez_pytania_o_zatrzymanie_odmawiają_zamiast_milczeć():
    #  Usterka, którą to łapie: krotka pusta oddana przebiegowi, który o pierwsze
    #  zatrzymanie nie pytał. Czyta się ona jak zdanie stające raz, a nie jak brak
    #  odpowiedzi, i tak samo odmawia ``Verdict.explain``.
    zdanie = "Dokument nazywa role, w jakich ktoś czyta, a dla każdej: pytanie."
    milczący = werdykt(zdanie, morphology(zdanie), zatrzymanie=False)
    assert milczący.result.rejected
    with pytest.raises(ValueError, match="o zatrzymanie nie pytał"):
        dalsze_zatrzymania(milczący)


def test_werdykt_bez_pytania_o_zatrzymanie_daje_ten_sam_status():
    #  Na tym stoi cała oszczędność: sonda różnicowa czyta z werdyktu sam status
    #  i po to o zatrzymanie nie pyta (``harness/ruch.py``).
    #  Zdanie odrzucone, bo tylko nad takim zatrzymanie w ogóle się liczy.
    zdanie = "Nowa program zapisuje ustawienia."
    segmenty = morphology(zdanie)
    pytany = werdykt(zdanie, segmenty)
    milczący = werdykt(zdanie, segmenty, zatrzymanie=False)
    assert (milczący.status, milczący.result.ile) == (pytany.status, pytany.result.ile)


def test_wyjaśnienie_odrzucenia_bez_zatrzymania_odmawia_zamiast_zmyślać():
    #  Usterka, którą to łapie: ``zatrzymanie`` jest ``None`` i wtedy, gdy analiza
    #  doszła do końca, i wtedy, gdy nikt nie pytał, więc wyjaśnienie czytające
    #  sam ten brak mówiłoby o zdaniu rzecz nieprawdziwą.
    zdanie = "Nowa program zapisuje ustawienia."
    milczący = werdykt(zdanie, morphology(zdanie), zatrzymanie=False)
    assert milczący.result.rejected
    with pytest.raises(ValueError, match="o zatrzymanie nie pytał"):
        milczący.explain()


def test_napis_bez_znaku_pyta_o_zatrzymanie_mimo_że_wołający_nie_prosił():
    #  Domknięcie stawia się nad analizą, która doszła do końca, a status napisu
    #  bez znaku od domknięcia zależy: flaga posłuchana tutaj dosłownie robi z
    #  niedomknięcia fragment.
    zdanie = "Cena jest niska"
    milczący = werdykt(zdanie, morphology(zdanie), zatrzymanie=False)
    assert milczący.status == NIEDOMKNIĘTE
    assert milczący.naprawa == Naprawa("kropka na końcu", 1)


# --------------------------------------------------------------------------- #
# Cały tekst, czyli werdykt na każde zdanie i podsumowanie nad nimi
# --------------------------------------------------------------------------- #


def test_niedomknięte_stoi_poza_mianownikiem_tak_samo_jak_fragment():
    """Domknięcia nie postawił nikt, więc zdaniem tekstu ten napis nie jest.

    Liczone w mianowniku podniosłoby go o nagłówek, który po domknięciu się
    wyprowadza, a `docs/extraction.md` mierzy tym mianownikiem podzbiór, a nie
    ekstrakcję.
    """
    podsumowanie = Podsumowanie.ze_zdań(nad_tekstem("Cena jest niska\n\nZapisz plik."))
    assert (podsumowanie.zdań, podsumowanie.bez_odczytania) == (1, 0)
    assert podsumowanie.fragmentów == 1


def test_every_sentence_of_a_text_is_checked():
    verdicts = check("Zapisz plik. Nowa program zapisuje ustawienia.")
    assert [found.status for found in verdicts] == ["valid", "rejected"]


def test_podsumowanie_nie_liczy_fragmentu_ani_w_liczniku_ani_w_mianowniku():
    """Fragment nie jest zdaniem, więc tekst z nagłówkiem nie ma gorszego wyniku.

    Reguła ta ma jednego właściciela dlatego, że pytają o nią wołający po obu
    stronach repozytorium — wiersz poleceń i witryna — a policzona u każdego z
    nich osobno daje mianownik większy o nagłówek i czyta się jak pomiar.
    """
    podsumowanie = Podsumowanie.ze_zdań(
        nad_tekstem("Co działa\n\nZapisz plik. Nowa program zapisuje ustawienia.")
    )
    assert (podsumowanie.zdań, podsumowanie.bez_odczytania) == (2, 1)
    assert (podsumowanie.wieloznaczne, podsumowanie.fragmentów) == (0, 1)


def test_niejasne_odniesienie_liczy_się_do_znalezisk_a_wieloznaczność_nie():
    """Usterka, którą to łapie: znalezisko policzone przez wydruk, a wydruki są dwa.

    Do kodu wyjścia idzie zaimek, a wieloznaczność zostaje w swoim liczniku
    (`ZNALEZISKA` w `olski/werdykt/tekst.py`), więc pytamy o obie liczby naraz.
    """
    podsumowanie = Podsumowanie.ze_zdań(nad_tekstem("Maki rosną w garnkach. Są one czerwone."))
    assert podsumowanie.niejasnych_odniesień == 1
    assert podsumowanie.znalezisk == 1


def test_zdanie_wieloznaczne_ma_zgłoszenie_a_nie_znalezisko():
    """Wiersz o odczytaniach pada, a kod wyjścia i licznik znalezisk go nie liczą."""
    (zdanie,) = nad_tekstem("Program otwierający się psuje.")
    assert zdanie.zgłoszenia == (WIELOZNACZNE,)
    assert zdanie.znaleziska == ()
    podsumowanie = Podsumowanie.ze_zdań([zdanie])
    assert (podsumowanie.wieloznaczne, podsumowanie.znalezisk) == (1, 0)


def _żądania(werdykt):
    """Żądania jedynego odczytania zdania, po jednym wpisie na obsadzoną pozycję."""
    (jedno,) = werdykt.żądania
    return [(w.rola, w.wypełnienie, w.klasy) for w in jedno]


def test_para_wypełnień_dostaje_wiersz_na_każdą_pozycję_a_nie_na_rolę():
    """Jedna rola obsadza tu dwie pozycje ramy, a czasownik żąda od nich czego innego.

    `dopełnienie` nie mówi, w którym przypadku stoi, więc wiersz wzięty raz na
    rolę nazwałby żądanie jednej z tych pozycji i przypisał je obu wypełnieniom.
    """
    assert _żądania(verdict("Autor doradza czytelnikowi poprawkę.")) == [
        ("podmiot", "Autor", ("PODMIOTY",)),
        ("dopełnienie", "czytelnikowi", ("LUDZIE",)),
        ("dopełnienie", "poprawkę", ("KOMUNIKAT", "SYTUACJA", "WYTWÓR")),
    ]


def test_czasownik_z_cząstką_zwrotną_pyta_o_własną_ramę():
    """Cząstka czyni z czasownika inne słowo, a plik żądań rozdziela je klasą słowa.

    `destabilizować` żąda w podmiocie podmiotu albo sytuacji, a `destabilizować
    się` samej sytuacji, więc wiersz wzięty bez cząstki mówiłby o zdaniu z nią
    to, co Walenty mówi o zdaniu bez niej.
    """
    assert _żądania(verdict("Rynek się destabilizuje.")) == [
        ("podmiot", "Rynek", ("SYTUACJA",))
    ]
    assert _żądania(verdict("Ustawa destabilizuje rynek."))[0] == (
        "podmiot",
        "Ustawa",
        ("PODMIOTY", "SYTUACJA"),
    )


def test_dopełniacz_pod_przeczeniem_czyta_się_jako_pozycja_biernikowa():
    """Przeczenie wymienia biernik dopełnienia na dopełniacz, a pozycja zostaje ta sama.

    Pozycję nazywa tu przypadek wypełnienia, więc bez tej wymiany zdanie
    zaprzeczone milczałoby o dopełnieniu, o którym zdanie twierdzące mówi.
    """
    assert _żądania(verdict("Autor nie edytuje dokumentu.")) == [
        ("podmiot", "Autor", ("PODMIOTY",)),
        ("dopełnienie", "dokumentu", ("KOMUNIKAT", "KONCEPCJA")),
    ]
    #  To samo żądanie, którym odpowiada zdanie twierdzące: różni je sama forma.
    assert _żądania(verdict("Autor edytuje dokument."))[1] == (
        "dopełnienie",
        "dokument",
        ("KOMUNIKAT", "KONCEPCJA"),
    )


def test_dopełnienie_bezokolicznika_nie_dostaje_żądania_formy_osobowej():
    """Pozycje pod bezokolicznikiem obsadzają jego ramę, a nie ramę formy nad nim.

    `dokument` stoi w bierniku `edytować`, a `zamierzyć` też biernika żąda,
    więc bez zatrzymania zejścia wychodzi stąd wiersz o żądaniu cudzego czasownika.
    """
    assert _żądania(verdict("Autor zamierzył edytować dokument.")) == [
        ("podmiot", "Autor", ("PODMIOTY",))
    ]


#: Projekt, który nikogo nie zadeklarował. Podaje go tu każde wywołanie, bo
#: domyślną jest deklaracja tego repozytorium, a te testy mówią o warstwie,
#: a nie o tym, kogo `olski.toml` w niej wypisał.
BEZ_OSÓB = Osoby()


def _osoby(werdykt, deklaracja=BEZ_OSÓB):
    """Pozycje, w których czasownik żąda kogoś, a stoi w nich rzecz."""
    return niespełnione_żądania(werdykt, deklaracja)


def test_deklaracja_zdejmuje_wiersz_temu_lematowi_o_który_prosi_i_żadnemu_obok():
    """Cała treść tej deklaracji: projekt mówi, kto w jego rejestrze jest kimś.

    Bez niej wiersz dostaje każde żądanie osoby, bo lemat spoza deklaracji
    nikogo nie nazywa, a projekt bez tej sekcji nie ma nikogo.
    """
    zdanie = verdict("Autor doradza czytelnikowi poprawkę.")
    assert [(w.rola, w.wypełnienie, w.lematy) for w in _osoby(zdanie)] == [
        ("podmiot", "Autor", frozenset({"autor"})),
        ("dopełnienie", "czytelnikowi", frozenset({"czytelnik"})),
    ]
    z_autorem = _osoby(zdanie, Osoby(lematy=frozenset({"autor"})))
    assert [w.wypełnienie for w in z_autorem] == ["czytelnikowi"]


def test_wiersz_o_pozycji_wychodzi_raz_na_zdanie_a_nie_raz_na_odczytanie():
    """Tym ten wykaz różni się od wykazu żądań, a różnicę widać na przyłączeniu.

    `w dokumencie` dochodzi raz do czasownika, raz do dopełnienia, więc zdanie
    ma dwa odczytania i te same dwie pozycje obsadzone w każdym z nich.
    Wykaz na odczytanie kazałby przeczytać cztery wiersze, żeby przeczytać dwa.
    """
    zdanie = verdict("Autor doradza czytelnikowi poprawkę w dokumencie.")
    assert len(zdanie.readings) == 2
    assert [w.wypełnienie for w in _osoby(zdanie)] == ["Autor", "czytelnikowi"]


def test_pozycja_obsadzona_w_każdym_odczytaniu_inaczej_daje_wiersz_na_każde_słowo():
    """Cena wykazu o zdaniu i granica zwijania wierszy powtórzonych.

    `Program drukuje werdykt.` czyta się dwojako, bo mianownik jest tu
    synkretyczny z biernikiem, więc podmiotem jest raz jedno słowo, raz drugie.
    Wiersz zwinięty do jednego zataiłby przed czytelnikiem to drugie czytanie.
    """
    assert [w.wypełnienie for w in _osoby(verdict("Program drukuje werdykt."))] == [
        "Program",
        "werdykt",
    ]


def test_pozycja_o_dwóch_głowach_wychodzi_raz_i_zbiera_oba_lematy():
    """Grupa `Wszystko to` ma głowę raz w jednym, raz w drugim ze swoich słów.

    Wiersz jest o pozycji, a nie o głowie, więc oba kształty dają go raz;
    bez tego `--żądania` wypisywało dwa wiersze o tym samym brzmieniu, bo
    głowy w nim nie widać. Lematy zbierają się przy tym oba, bo o cały ich
    zbiór pyta deklaracja osób.
    """
    wiersze = _osoby(verdict("Wszystko to deklaruje plik."))
    grupa = [w for w in wiersze if w.wypełnienie == "Wszystko to"]
    assert [w.lematy for w in grupa] == [frozenset({"to", "wszystko"})]
