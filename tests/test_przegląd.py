import pytest

pytest.importorskip("morfeusz2")

from olski.subset import check
from olski.wieloznaczność import miejsca
from opowieści.bazyliszek import OPOWIEŚĆ
from skład import kompiluj
from skład.opowieść import Akapit, Postać
from skład.przegląd import przejrzyj
from skład.składnia import TERAZ, Kontekst, Rzecz, byt, nie
from skład.słownik import Dokąd, Kiedy, R, V, jest, opis, potem


def kolizje(drzewo, kontekst=TERAZ):
    return [x.formy for x in przejrzyj(drzewo, kontekst)]


def nad_akapitem(akapit, czas="kiedyś"):
    """Zgłoszenia przeglądu nad akapitem, czyli po kontekstach, którymi on się składa.

    Osobno od napisu, bo o opuszczonym podmiocie rozstrzyga akapit,
    więc test, który tego napisu nie pokaże obok, mierzy co innego, niż czyta.
    """
    return [
        kolizja
        for zdanie, kontekst in akapit.konteksty(czas)
        for kolizja in przejrzyj(zdanie, kontekst)
    ]


def test_dwie_role_nieodróżnialne_zgłaszają_się_choć_drzewo_jest_dobre():
    """Zdanie, przez które ten moduł powstał, i cała jego treść naraz.

    Drzewo mówi, co jest większe, a napis, który z niego wychodzi, nie mówi,
    i nie zgłasza tego ani rama, ani zgodność, ani słownik form.
    """
    drzewo = V.przewyższać(R.koszt / R.szynka, R.koszt / R.bułka)
    assert kompiluj(drzewo) == "Koszt szynki przewyższa koszt bułki."
    (kolizja,) = przejrzyj(drzewo)
    assert kolizja.formy == ("koszt szynki", "koszt bułki")
    #  Same formy nie wystarczą: zgłoszenie ma powiedzieć, czego autor nie widzi.
    assert "„koszt szynki” i „koszt bułki”" in kolizja.opisz()


@pytest.mark.parametrize(
    ("drzewo", "kontekst"),
    [
        #  Liczba: orzeczenie stoi w pojedynczej, więc grupa mnoga podmiotem nie stanie.
        (V.zapisywać(R.program, ~R.ustawienie), TERAZ),
        #  Rodzaj: czas przeszły go niesie, a teraźniejszy nie, i stąd ta sama
        #  para ról raz się zgłasza, a raz nie. Kufer jest męski, lustro nijakie.
        (V.zasłaniać(R.kufer, R.lustro), Kontekst(czas="kiedyś")),
        #  Przeczenie: dopełnienie idzie w dopełniaczu, więc z mianownikiem nie kolidu-
        #  je. Przypadek bierze się tu z jednego pola, o które pyta i linearyzacja.
        (nie(V.zasłaniać(R.kufer, R.lustro)), TERAZ),
        #  Narzędnik orzecznika: kopula nie stawia dwóch grup, które by się myliły.
        (jest(R.parser / R.podzbiór, R.cel), TERAZ),
        #  Żywotność: biernik rzeczownika męskoosobowego równa się dopełniaczowi,
        #  a nie mianownikowi, więc czeladnik dopełnieniem stanie i podmiotem nie.
        (V.zamykać(R.czeladnik, R.okno), TERAZ),
    ],
)
def test_zdanie_któremu_polszczyzna_role_przypina_nie_zgłasza_się(drzewo, kontekst):
    assert kolizje(drzewo, kontekst) == []


def test_rzecz_spod_przyimka_nie_staje_w_parze_z_podmiotem():
    """To jest ta różnica, dla której przegląd bierze drzewo, a nie napis.

    `Wzrok` i `kamień` stoją tu w formach nierozróżnialnych i przy jednym czasowniku,
    czyli tak samo jak para, którą przegląd zgłasza.
    Podmiotem `kamień` nie stanie, bo stoi pod przyimkiem,
    a to jest fakt o drzewie i po formach go nie widać.
    """
    drzewo = V.zamieniać(R.wzrok / R.potwór, R.człowiek, Dokąd.w(R.kamień))
    assert kompiluj(drzewo) == "Wzrok potwora zamienia człowieka w kamień."
    assert kolizje(drzewo) == []


def test_przegląd_widzi_parę_której_pomiar_nad_tekstem_nie_melduje():
    """Rozbieżność, na której stoi wpis w ``TODO.md``, więc trzymana testem.

    `mysz` niesie mianownik i biernik dwoma osobnymi wpisami słownika,
    a `_obojętny` w tamtym module żąda obu od jednego wpisu, więc tę parę mija.
    Porównanie napisów o wpisy nie pyta i dlatego jej nie mija,
    a olski czyta to zdanie dwojako, czyli rację ma tu skład.
    """
    drzewo = V.gonić(R.mysz, R.ogon)
    assert kompiluj(drzewo) == "Mysz goni ogon."
    assert check(kompiluj(drzewo))[0].status == "ambiguous"
    assert miejsca(kompiluj(drzewo)) == []
    assert kolizje(drzewo) == [("mysz", "ogon")]


def test_ciąg_zdarzeń_rozdziela_kolizje_po_orzeczeniach():
    """Uczestnicy stają przy orzeczeniu, a ciąg ma po jednym na zdarzenie.

    Zgłoszenia są więc dwa i każde o swojej parze,
    a `kufer` i `plik`, które przy jednym czasowniku nie stanęły, parą nie są.
    """
    drzewo = potem(V.zasłaniać(R.kufer, R.lustro), V.zapisywać(R.program, R.plik))
    assert kompiluj(drzewo) == "Kufer zasłania lustro i program zapisuje plik."
    assert kolizje(drzewo) == [("kufer", "lustro"), ("program", "plik")]


def test_kolizja_spod_okoliczności_wyrażonej_zdarzeniem_zgłasza_się_też():
    """Zdanie podrzędne ma własne orzeczenie, więc ma i własnych uczestników.

    Zgłoszenie jest tu jedno i przychodzi z dołu:
    w zdaniu nadrzędnym czeladnik jest męskoosobowy i dopełnieniem nie stanie,
    a w podrzędnym obie role stoją nieodróżnialne.
    """
    drzewo = V.zasłaniać(R.czeladnik, R.lustro, Kiedy.gdy(V.zapisywać(R.program, R.plik)))
    assert kompiluj(drzewo) == "Czeladnik zasłania lustro, gdy program zapisuje plik."
    assert kolizje(drzewo) == [("program", "plik")]


def test_zdanie_z_opuszczonym_podmiotem_zgłasza_się_samym_dopełnieniem():
    """Podmiot, którego w tekście nie ma, żadnej swojej formy czytelnikowi nie pokazuje.

    Zdanie stoi tu drugie w akapicie i mówi o tej samej postaci co pierwsze,
    więc podmiot z niego wypada, a zostaje `sień`, którą polszczyzna czyta
    i w mianowniku, i w bierniku; forma przeszła tych dwóch ról nie rozdziela,
    bo obie są żeńskie.
    Zgłoszenie niesie przez to jeden napis, a nie dwa: forma, której nie widać,
    nie jest tym, na co autor ma spojrzeć.
    """
    córka = Postać(R.córka)
    akapit = Akapit(V.wracać(córka), V.zamykać(córka, R.sień))
    assert akapit.kompiluj("kiedyś") == "Córka wracała. Zamykała sień."
    (kolizja,) = nad_akapitem(akapit)
    assert kolizja.formy == ("sień",)
    #  Zgłoszenie ma powiedzieć, czego autor nie widzi, a nie wypisać drugą formę
    #  za polszczyznę: podmiotu w tym zdaniu nie ma.
    assert "„sień” stoi w formie" in kolizja.opisz()
    assert "podmiotu to zdanie nie wypisuje" in kolizja.opisz()


@pytest.mark.parametrize(
    ("dopełnienie", "tekst"),
    [
        #  Czasownik: lustro jest nijakie, więc forma przeszła rozdziela je od córki.
        (Rzecz("lustro"), "Córka wracała. Zamykała lustro."),
        #  Forma uczestnika: biernik różni się od mianownika, choć rodzaj jest wspólny.
        (Rzecz("skrzynia"), "Córka wracała. Zamykała skrzynię."),
    ],
)
def test_opuszczony_podmiot_nie_zdejmuje_dwóch_pozostałych_rozróżnień(dopełnienie, tekst):
    """Zostają dwa warunki i oba mierzą to, co w tekście widać.

    Bez nich każde zdanie o opuszczonym podmiocie byłoby trafieniem,
    a raport zgłaszający je wszystkie nie oddzielałby niczego od niczego.
    """
    córka = Postać(R.córka)
    akapit = Akapit(V.wracać(córka), V.zamykać(córka, dopełnienie))
    assert akapit.kompiluj("kiedyś") == tekst
    assert nad_akapitem(akapit) == []


def test_rzecz_wskazana_liczy_się_z_zaimka_którym_wyszła():
    """Zdanie podrzędne mówi o wskazanej rzeczy zaimkiem, a zaimek przypadek pokazuje.

    `sień` brzmi w mianowniku i w bierniku tak samo, a `którą` nie brzmi,
    więc czytelnik wie, która rola jest którą, i zgłoszenia tu nie ma.
    Liczone z samej grupy imiennej wyszłoby trafienie na zdaniu,
    które ról wcale nie miesza, czyli zarzut wobec napisu, którego autor nie dostał.
    """
    sień = byt(R.sień)
    drzewo = V.zasłaniać(R.czeladnik, opis(sień, V.zamykać(R.klucz, sień)))
    assert kompiluj(drzewo) == "Czeladnik zasłania sień, którą klucz zamyka."
    assert kolizje(drzewo) == []


def test_każde_mierzone_zdanie_wychodzi_takim_napisem_jakim_je_zmierzono():
    """Przegląd mierzy napis, więc mierzony napis ma stać w tekście, a nie obok niego.

    Rozjeżdża się to cicho i rozjechało się raz:
    pole dopisane do ``Kontekst`` przekazuje w dół linearyzacja,
    a ``Zdanie.konteksty`` obok niej przekazać go może zapomnieć,
    i wtedy przegląd czyta zdanie, którego autor nie dostał.
    Legenda jest tu materiałem, bo niesie wszystkie kategorie zapisu naraz,
    wraz z opuszczonym podmiotem i z rzeczą wskazaną zaimkiem.
    """
    for akapit in OPOWIEŚĆ.akapity:
        tekst = akapit.kompiluj(OPOWIEŚĆ.CZAS)
        for zdanie, kontekst in akapit.konteksty(OPOWIEŚĆ.CZAS):
            for niższe, jego in zdanie.konteksty(kontekst):
                #  Kompilacja podnosi pierwszą literę zdania, a pomiar jej nie podnosi.
                assert niższe.linearyzuj(jego).napis.lower() in tekst.lower()


def test_opowieść_o_bazyliszku_nie_niesie_ani_jednej_kolizji():
    """Zero zgłoszeń nad całą legendą, a przyczyną jest czas, w którym ona stoi.

    Opowieść mówi o tym, co było, więc każde jej orzeczenie niesie rodzaj,
    a rodzaj rozstrzyga tam, gdzie sam przypadek nie rozstrzyga.
    Test ten jest przez to pomiarem tego, ile przegląd zgłasza nad tekstem,
    którego nikt pod niego nie pisał, i dlatego stoi tu mimo swojej zerowej liczby.
    """
    assert [
        kolizja
        for akapit in OPOWIEŚĆ.akapity
        for zdanie, kontekst in akapit.konteksty(OPOWIEŚĆ.CZAS)
        for kolizja in przejrzyj(zdanie, kontekst)
    ] == []
