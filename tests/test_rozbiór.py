import subprocess
import sys

import pytest

pytest.importorskip("morfeusz2")

from olski.skład import Kontekst, Postać, Robi, kompiluj
from olski.skład.rozbiór import obieg, rozbierz, sygnatura
from olski.skład.słownik import (
    A,
    Czym,
    D,
    Dlaczego,
    Dokąd,
    Gdzie,
    Kiedy,
    R,
    Treść,
    V,
    jest,
    nie,
    potem,
    razem,
)
from olski.subset import check


@pytest.mark.parametrize(
    "drzewo",
    [
        jest(A.zwykły * A.polski * R.tekst, R.wejście),
        jest(R.parser / R.podzbiór, R.cel),
        jest(R.parser / ~R.podzbiór, R.cel),
        V.zapisywać(R.program, ~R.ustawienie),
        V.sprawdzać(R.linter, ~(A.polski * R.tekst)),
        V.mieszkać(R.kot, Gdzie.w(R.piwnica)),
        V.mieszkać(R.kot, Gdzie.w(R.piwnica).temat),
        V.zapisywać(R.program.remat, (~R.ustawienie).temat),
        V.sprawdzać(R.linter, razem([~(A.polski * R.tekst), ~R.ustawienie])),
        potem(V.zapisywać(R.program, ~R.ustawienie), V.sprawdzać(R.linter, R.tekst)),
        nie(V.zapisywać(R.program, ~R.ustawienie)),
        nie(jest(A.zwykły * A.polski * R.tekst, R.wejście)),
        V.wiedzieć(R.linter, Treść(V.zapisywać(R.program, ~R.ustawienie))),
        V.mieszkać(R.kot, D.nagle),
        V.zapisywać(R.program, ~R.ustawienie, D.szybko),
    ],
)
def test_drzewo_wraca_z_napisu_który_z_niego_wyszedł(drzewo):
    """Niezmiennik obiegu na tych drzewach, których obejmują oba tory naraz.

    Lista jest listą przypadków, a nie gwarancją, i przecięciem dwóch pokryć:
    przymiotnik po rzeczowniku ma tylko gramatyka, a okoliczność wyrażoną
    zdarzeniem tylko skład, więc stoi tu to, co mówią oba.
    Przysłówek stoi w niej, odkąd mają go oba: gramatyka dostała go po składzie,
    a obieg zamknął się na nim dopiero razem z tą produkcją.
    """
    przebieg = obieg(drzewo)
    assert przebieg.wróciło, przebieg.opisz()


def test_czas_jest_własnością_opowiadania_i_obieg_zamyka_się_w_obu():
    """Czas jest w kontekście, a nie w drzewie, i to samo drzewo wraca z obu napisów.

    To drzewo stoi w liście wyżej, czyli w czasie teraźniejszym,
    a tutaj wraca z napisu, który dałaby mu opowieść.
    Jest to jedyne miejsce w tym pliku, w którym obieg biegnie poza ``TERAZ``.
    """
    drzewo = V.mieszkać(R.kot, Gdzie.w(R.piwnica))
    kiedyś = obieg(drzewo, Kontekst(czas="kiedyś"))
    assert kiedyś.napis == "Kot mieszkał w piwnicy."
    assert kiedyś.wróciło, kiedyś.opisz()


def test_wyróżnienie_wraca_z_szyku_bo_szyk_jest_tym_co_ono_niesie():
    """Temat i remat są jedyną kategorią tego zapisu, którą napis niesie kolejnością.

    Zdanie stoi tu w szyku, którego bez znaczników nie ma,
    więc drzewo, które wraca, musi je mieć, a nie tylko dać się wypisać.
    """
    bez_znaczników = jest(A.zwykły * A.polski * R.tekst, R.wejście)
    wyróżnione = jest((A.zwykły * A.polski * R.tekst).remat, R.wejście.temat)
    assert kompiluj(bez_znaczników) == "Zwykły polski tekst jest wejściem."
    przebieg = obieg(wyróżnione)
    assert przebieg.napis == "Wejściem jest zwykły polski tekst."
    assert przebieg.wróciło, przebieg.opisz()


def test_lemat_i_liczba_biorą_się_z_formy_a_nie_z_wyprowadzenia_które_zostało():
    """Czytanie parsera jest kształtem, więc lemat w nim stojący jest przypadkowy.

    ``Kot`` jest w słowniku i kotem, i nazwiskiem rodzaju żeńskiego,
    a te dwa wyprowadzenia mają jeden kształt i stoją w wyniku jako jedno czytanie,
    więc rozbiór czytający lemat z liścia dostaje to, które przyszło pierwsze.
    Zdanie to wraca stąd oboma drzewami i żadne z nich nie jest wyborem tego pliku.
    """
    drzewa = [sygnatura(drzewo) for drzewo in rozbierz("Kot mieszka w piwnicy.").drzewa]
    assert sygnatura(V.mieszkać(R.kot, Gdzie.w(R.piwnica))) in drzewa
    assert sygnatura(V.mieszkać(R.Kot, Gdzie.w(R.piwnica))) in drzewa


def test_relacja_okolicznika_wraca_każda_którą_ta_forma_dopuszcza():
    """Relacja jest kategorią dziedziny, a napis niesie przyimek, więc drzew jest kilka.

    Rozdziela je forma, a nie cecha w drzewie parsera:
    miejscownik po ``w`` stoi w relacji czasu i miejsca naraz,
    a relacja celu żąda biernika, którego w tym zdaniu nie ma.
    """
    drzewa = [sygnatura(drzewo) for drzewo in rozbierz("Kot mieszka w piwnicy.").drzewa]
    assert sygnatura(V.mieszkać(R.kot, Kiedy.w(R.piwnica))) in drzewa
    assert sygnatura(V.mieszkać(R.kot, Dokąd.w(R.piwnica))) not in drzewa


def test_przeczenie_wraca_przy_tym_orzeczeniu_przy_którym_cząstka_stanęła():
    """Cząstka przecząca stoi w pozycji czasownika i przeczy jednemu orzeczeniu.

    Gramatyka stawia ją przed formą, więc czytana samą głową ta pozycja
    czasownika nie znajduje wcale, a czytana całym ciałem znajduje i jego,
    i przeczenie. Że przeczenie zostaje przy swoim orzeczeniu,
    mówi następstwo z jednym zdarzeniem zaprzeczonym:
    drugie drzewo wychodzi innym napisem i stąd nie wraca.
    """
    program = Postać(R.program)
    jedno = potem(V.zapisywać(program, ~R.ustawienie), nie(V.sprawdzać(program, R.tekst)))
    oba = potem(nie(V.zapisywać(program, ~R.ustawienie)), nie(V.sprawdzać(program, R.tekst)))
    przebieg = obieg(jedno)
    assert przebieg.napis == "Program zapisuje ustawienia i nie sprawdza tekstu."
    assert przebieg.wróciło, przebieg.opisz()
    assert sygnatura(oba) not in [sygnatura(drzewo) for drzewo in przebieg.odczyt.drzewa]


@pytest.fixture
def chcieć_sprawdzać():
    """Bezokolicznik o wykonawcy zdania nad nim, bo tego samego obiektu żąda ``Robi``."""
    linter = R.linter
    return V.chcieć(linter, V.sprawdzać(linter, A.dobry * R.kod))


def test_bezokolicznik_wraca_z_wykonawcą_wziętym_z_podmiotu_nad_nim(chcieć_sprawdzać):
    """O wykonawcy napis nie mówi nic, bo bezokolicznik nie niesie ani osoby, ani rodzaju.

    Drzewo pod tą pozycją powstaje więc po podmiocie, a nie przed nim,
    i tym różni się ona od treści, która podmiot ma wypisany.
    """
    przebieg = obieg(chcieć_sprawdzać)
    assert przebieg.napis == "Linter chce sprawdzać dobry kod."
    assert przebieg.wróciło, przebieg.opisz()


def test_dopełniacz_negacji_wraca_spod_bezokolicznika(chcieć_sprawdzać):
    """Przeczenie stoi przy formie osobowej, a przypadek zmienia się o piętro niżej.

    Dwie kategorie spotykają się tu w jednej pozycji i żadna z nich
    nie jest w napisie tam, gdzie jej skutek: cząstka wychodzi nad bezokolicznikiem,
    a dopełniacz pod nim, więc drzewo, które wraca, musi mieć obie.
    """
    przebieg = obieg(nie(chcieć_sprawdzać))
    assert przebieg.napis == "Linter nie chce sprawdzać dobrego kodu."
    assert przebieg.wróciło, przebieg.opisz()


def test_pozycja_bezokolicznika_wraca_ramą_a_nie_brakiem_kategorii():
    """Bezokolicznika gramatyka nie pyta o lemat, a skład pyta, i tu widać, ile to znaczy.

    `Linter pomaga pisać dobry kod.` wyprowadza się i nie składa,
    a mówi o tym powód, nie sama pustka: kategorię ten zapis ma,
    a leksykon jej temu czasownikowi nie daje.
    Tę różnicę między kierunkami opisuje `olski/walencja.py`,
    a co z niej wynika dla tego zdania, pyta `TODO.md`.
    """
    zdanie = "Linter pomaga pisać dobry kod."
    assert check(zdanie)[0].status in ("valid", "ambiguous")
    odczyt = rozbierz(zdanie)
    assert odczyt.drzewa == ()
    assert odczyt.powody == ("pomagać nie bierze bezokolicznika",)


@pytest.mark.parametrize(
    "zdanie",
    [
        "Zwykły tekst polski jest wejściem.",
        "On zapisuje ustawienia.",
        "Zapisz plik.",
        "Ludzie są wolni.",
        "Program albo linter sprawdza tekst.",
        "Program, który zapisuje ustawienia, sprawdza tekst.",
    ],
)
def test_czytanie_którego_ten_zapis_nie_mówi_nie_wraca_żadnym_drzewem(zdanie):
    """Zdania olskiego, dla których ten kierunek kategorii nie ma.

    Werdykt gramatyki stoi w każdym z nich obok, bo bez niego pustka
    mówiłaby o zdaniu odrzuconym tyle samo, co o brakującej kategorii,
    a mierzy się tu tę drugą.
    """
    assert check(zdanie)[0].status in ("valid", "ambiguous")
    assert rozbierz(zdanie).drzewa == ()


@pytest.mark.parametrize(
    ("zdanie", "powód"),
    [
        ("Program, który zapisuje ustawienia, sprawdza tekst.", "RelativeClause"),
        ("Zapisz plik.", "w pozycji Verb"),
    ],
)
def test_zdanie_bez_drzewa_mówi_czego_temu_zapisowi_brakuje(zdanie, powód):
    """Dwa miejsca, w których pusta odpowiedź powstaje bez zgłoszenia po drodze.

    Zdanie względne jest ciałem produkcji, którego ten zapis nie czyta,
    a rozkaźnik nie ma lematu, którym ten zapis wypisuje czasownik,
    więc pierwsze wypada przy dopasowaniu ciała, a drugie na pustym iloczynie.
    Powód nazywa jedno i drugie, bo bez niego obie drogi wyglądają tak samo.
    """
    odczyt = rozbierz(zdanie)
    assert any(powód in mówi for mówi in odczyt.powody), odczyt.powody


@pytest.mark.parametrize(
    ("zdanie", "zbudowano_kandydata"),
    [
        ("Program, który zapisuje ustawienia, sprawdza tekst.", False),
        ("Zwykły tekst polski jest wejściem.", True),
    ],
)
def test_pusta_odpowiedź_mówi_liczbą_kandydatów_która_z_dwóch_pustek_padła(
    zdanie, zbudowano_kandydata
):
    """Dwie pustki, które powód rozdziela zdaniem, a pomiar musi rozdzielić liczbą.

    Zdanie względne nie ma tu kategorii, więc kandydat nie powstaje wcale,
    a przymiotnik po rzeczowniku kategorię ma i wraca z niej inny szyk,
    więc kandydat powstaje i przegrywa dopiero na porównaniu form.
    Pomiar nad rejestrem liczy te dwie rzeczy osobno, bo pierwsza mówi,
    o ile ten zapis musiałby urosnąć, a druga, że kierunki mówią co innego
    o jednym zdaniu (``sonda/znaczenia.py``).
    """
    odczyt = rozbierz(zdanie)
    assert odczyt.drzewa == ()
    assert (odczyt.kandydaci > 0) is zbudowano_kandydata


def test_zdanie_spoza_gramatyki_mówi_o_gramatyce_a_nie_o_brakującej_kategorii():
    """Dwie pustki mówią o czym innym i obieg ma je rozdzielać.

    Narzędzie stoi w napisie samym narzędnikiem, bez przyimka,
    a narzędnik bierze w tej gramatyce orzecznik kopuli i nikt poza nim,
    więc to zdanie nie ma ani jednego czytania,
    i wtedy pustka jest werdyktem olskiego, a nie zdaniem o tym zapisie.
    """
    przebieg = obieg(V.zapisywać(R.program, ~R.ustawienie, Czym(R.klucz)))
    assert przebieg.napis == "Program zapisuje ustawienia kluczem."
    assert not przebieg.wróciło
    assert "gramatyka olskiego nie wyprowadza" in przebieg.opisz()


@pytest.mark.parametrize(
    "drzewo",
    [
        V.zapisywać(R.program, ~R.ustawienie, Dlaczego.bo(V.sprawdzać(R.linter, R.tekst))),
        V.zapisywać(R.program, ~R.ustawienie, Kiedy.gdy(V.sprawdzać(R.linter, R.tekst))),
        V.zapisywać(R.program, ~R.ustawienie, Kiedy.gdy(V.sprawdzać(R.linter, R.tekst)).temat),
    ],
)
def test_okoliczność_wyrażona_zdarzeniem_wraca_relacją_którą_niesie_spójnik(drzewo):
    """Obieg zamyka się na zdaniu okolicznikowym, a relację niesie przez spójnik.

    Relacja jest kategorią dziedziny i w napisie stoi tylko słowo,
    więc wraca ona stąd tak samo jak przy przyimku: z leksykonu czytanego wspak.
    Wysunięcie na czoło wraca osobno, bo o nim rozstrzyga autor,
    a leksykon mówi tylko, którym spójnikom polszczyzna na nie pozwala.
    """
    przebieg = obieg(drzewo)
    assert przebieg.wróciło, przebieg.opisz()


def test_z_dwóch_przyłączeń_wraca_to_jedno_które_ten_zapis_ma():
    """Przyłączenie olski oddaje czytelnikowi, a ten zapis rozstrzyga je w drzewie.

    Wyrażenie przyimkowe dochodzi tu do zdarzenia i nie ma czym dojść do rzeczy,
    więc z dwóch czytań tego zdania wraca jedno,
    i to jest ta połowa przyłączenia, której ten kierunek nie mówi.
    """
    zdanie = "Program zapisuje ustawienia w repozytorium."
    assert check(zdanie)[0].status == "ambiguous"
    drzewa = rozbierz(zdanie).drzewa
    assert drzewa
    assert all(isinstance(drzewo, Robi) and len(drzewo.okoliczniki) == 1 for drzewo in drzewa)


def test_tożsamość_wraca_stamtąd_gdzie_napis_ją_niesie():
    """Opuszczony podmiot jest jedynym śladem, jaki tożsamość zostawia w napisie.

    Dwa drzewa różnią się tu tylko tym, czy podmiot obu zdarzeń jest jedną rzeczą,
    a napisy różnią się tym, czy drugie zdarzenie go powtarza,
    więc oba wracają, każde ze swojego napisu.
    """
    program = Postać(R.program)
    jedna = obieg(potem(V.zapisywać(program, ~R.ustawienie), V.sprawdzać(program, R.tekst)))
    dwie = obieg(potem(V.zapisywać(R.program, ~R.ustawienie), V.sprawdzać(R.program, R.tekst)))
    assert jedna.napis == "Program zapisuje ustawienia i sprawdza tekst."
    assert dwie.napis == "Program zapisuje ustawienia i program sprawdza tekst."
    assert jedna.wróciło, jedna.opisz()
    assert dwie.wróciło, dwie.opisz()


def test_import_składu_nie_woła_parsera():
    """Parser jest tu świadkiem, a nie zależnością, i widać to na tym, co się importuje.

    ``olski/skład/rozbiór.py`` czyta gramatykę, więc dopisany do ``olski/skład/__init__.py``
    kazałby ją zbudować każdemu, kto sięga po sam kompilator.
    Import podpakietu przechodzi przez pakiet nadrzędny,
    więc ten test pyta o ``olski/__init__.py`` tak samo.
    Liczone jest to w osobnym procesie, bo w tym gramatykę zaimportowały
    testy stojące obok.
    """
    kod = "import olski.skład, sys; print('olski.subset' in sys.modules)"
    przebieg = subprocess.run([sys.executable, "-c", kod], capture_output=True, text=True)
    assert przebieg.stdout.strip() == "False", przebieg.stderr


def test_sygnatura_mówi_które_wystąpienia_są_jedną_rzeczą_a_nie_którą():
    """Bez tego niezmiennik obiegu nie miałby czego porównać.

    Tożsamość jest obiektem, bo tyle daje zmienna w Pythonie,
    a drzewo zbudowane z napisu nie ma jak dzielić obiektów z tym,
    z którego ten napis wyszedł, więc równość odpowiadałaby przecząco zawsze.
    """
    jeden, drugi = Postać(R.program), Postać(R.program)
    jedna = potem(V.zapisywać(jeden, ~R.ustawienie), V.sprawdzać(jeden, R.tekst))
    taka_sama = potem(V.zapisywać(drugi, ~R.ustawienie), V.sprawdzać(drugi, R.tekst))
    dwie = potem(V.zapisywać(jeden, ~R.ustawienie), V.sprawdzać(drugi, R.tekst))
    assert jedna != taka_sama
    assert sygnatura(jedna) == sygnatura(taka_sama)
    assert sygnatura(jedna) != sygnatura(dwie)
