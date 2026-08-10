import pytest

pytest.importorskip("morfeusz2")

import skład.składnia as składnia
from olski.subset import WALENCJA, check
from olski.walencja import bierze_biernik
from skład import (
    BrakFormy,
    Byt,
    Czyj,
    Jaki,
    Kontekst,
    Koordynacja,
    PozaRamą,
    Rzecz,
    byt,
    kompiluj,
    nie,
    odmień,
)
from skład.składnia import Jest, Robi
from skład.słownik import (
    A,
    D,
    Dokąd,
    Gdzie,
    Kiedy,
    R,
    Skąd,
    V,
    czym,
    jest,
    nowe,
    opis,
    razem,
    temat,
)


def test_zgodność_jest_liczona_a_nie_żądana_od_autora():
    """Przymiotnik dostaje rodzaj z rzeczownika, a przypadek z pozycji w zdaniu.

    Trzy rodzaje naraz, bo pomyłką, którą da się tu zrobić, jest wzięcie rodzaju
    z jednego miejsca dla wszystkich: przy jednym rzeczowniku taki błąd nie widać.
    """
    assert Jaki("dobry", Rzecz("kod")).linearyzuj("nom", "sg").napis == "dobry kod"
    dokumentacja = Jaki("dobry", Rzecz("dokumentacja"))
    assert dokumentacja.linearyzuj("nom", "sg").napis == "dobra dokumentacja"
    assert Jaki("dobry", Rzecz("narzędzie")).linearyzuj("nom", "sg").napis == "dobre narzędzie"


def test_ta_sama_rzecz_odmienia_się_wedle_pozycji_w_zdaniu():
    """Przypadek przychodzi od konstruktora zdania, a nie od autora grupy imiennej."""
    tekst = Jaki("polski", Rzecz("tekst"))
    assert Robi(byt(Rzecz("linter")), "sprawdzać", byt(tekst)).linearyzuj().napis == (
        "linter sprawdza polski tekst"
    )
    assert Jest(byt(tekst), byt(Rzecz("wejście"))).linearyzuj().napis == (
        "polski tekst jest wejściem"
    )


def test_kierunek_relacji_dopełniaczowej_jest_kształtem_drzewa():
    """Dwa drzewa, dwa zdania, znaczenia przeciwne.

    Nad workiem lematów te dwa zdania są nie do rozróżnienia, i to jest powód,
    dla którego ta kategoria stoi w drzewie zamiast w kolejności słów.
    """
    parser, podzbiór = Rzecz("parser"), Rzecz("podzbiór")
    assert kompiluj(Jest(byt(parser / podzbiór), byt(Rzecz("cel")))) == (
        "Parser podzbioru jest celem."
    )
    assert kompiluj(Jest(byt(podzbiór / parser), byt(Rzecz("cel")))) == (
        "Podzbiór parsera jest celem."
    )


def test_określenie_niesie_własną_liczbę_niezależnie_od_głowy():
    """Bez tego parser podzbiorów nie ma jak powstać, bo liczba głowy zjada obie."""
    parser = Rzecz("parser")
    assert Czyj(parser, Byt(Rzecz("podzbiór"), "pl")).linearyzuj("nom", "sg").napis == (
        "parser podzbiorów"
    )
    assert Czyj(parser, Byt(Rzecz("podzbiór"))).linearyzuj("nom", "pl").napis == (
        "parsery podzbioru"
    )


def test_forma_której_słownik_nie_ma_zgłasza_się_zamiast_zostać_zgadnięta():
    """Kompilator, który w tym miejscu zgaduje, wypuszcza polszczyznę nieistniejącą."""
    with pytest.raises(BrakFormy):
        odmień("podzbiór", "subst", case="nom", number="sg", gender="f")
    with pytest.raises(BrakFormy):
        odmień("zzznieistniejący", "subst", case="nom", number="sg")


def test_czasownik_któremu_leksykon_odmawia_biernika_nie_wypuszcza_dopełnienia():
    """Zdanie z roadmapy: `Linter pomaga dobry kod.` nie ma wyjść z tego drzewa.

    Zgłoszenie pada przy budowaniu drzewa, a nie przy linearyzacji,
    więc test niczego nie linearyzuje.
    """
    with pytest.raises(PozaRamą):
        V.pomagać(R.linter, A.dobry * R.kod)


def test_kopuli_biernik_odmówiony_jest_po_obu_stronach_tak_samo():
    """Kopula jest lematem, na którym kopia leksykonu rozjechałaby się najpierw.

    Czemu akurat ona, mówi ``olski/walencja.py``;
    tutaj stoi zdanie, które by z tego rozjazdu wyszło.
    """
    with pytest.raises(PozaRamą):
        V.być(R.program, ~R.ustawienie)


def test_biernika_odmawiają_oba_kierunki_tym_samym_lematom():
    """Jedno źródło znaczy tyle, że nie ma dwóch odpowiedzi na jedno pytanie.

    Odmowy parsera liczone są z ram, a nie wypisane obok nich,
    żeby rama dopisana do gramatyki weszła do tego porównania sama.
    """
    odmawia_parser = {
        lemat
        for rama, lematy in WALENCJA.items()
        if "acc" not in rama.split(".")
        for lemat in lematy.split("|")
    }
    assert {lemat for lemat in odmawia_parser if bierze_biernik(lemat)} == set()
    #  Odmowa postawiona każdemu lematowi przeszłaby powyższe, więc świadek
    #  z drugiej strony: `zapisywać` bierze ramę domyślną po obu.
    assert "zapisywać" not in odmawia_parser
    assert bierze_biernik("zapisywać")


def test_przestrzenie_nazw_niczego_w_składni_nie_zmieniają():
    """Cukier jest zdejmowalny albo nim nie jest, a docstring tego nie rozstrzyga.

    Warstwa dopisująca operatory klasom składni zmieniałaby zachowanie modułu
    przez sam import, więc to samo drzewo znaczyłoby co innego zależnie od tego,
    co jeszcze zostało zaimportowane.
    """
    assert składnia.Rzecz.__truediv__ is składnia.Nominalne.__truediv__
    assert składnia.Rzecz.__invert__ is składnia.Nominalne.__invert__
    assert R.parser / R.podzbiór == Czyj(Rzecz("parser"), byt(Rzecz("podzbiór")))
    assert ~R.ustawienie == Byt(Rzecz("ustawienie"), "pl")
    assert A.dobry * R.kod == Jaki("dobry", Rzecz("kod"))


def test_dwa_przymiotniki_zagnieżdżają_się_w_kolejności_zapisu():
    """Mnożenie wiąże w lewo, więc bez klasy pośredniej wychodzi kolejność odwrotna."""
    assert A.zwykły * A.polski * R.tekst == Jaki("zwykły", Jaki("polski", Rzecz("tekst")))


@pytest.mark.parametrize(
    "drzewo",
    [
        jest(A.zwykły * A.polski * R.tekst, R.wejście),
        jest(R.parser / R.podzbiór, R.cel),
        jest(R.parser / ~R.podzbiór, R.cel),
        V.zapisywać(R.program, ~R.ustawienie),
        V.sprawdzać(R.linter, ~(A.polski * R.tekst)),
    ],
)
def test_to_co_skład_wypuszcza_czyta_się_w_olskim_raz(drzewo):
    """Sprzężenie obu torów jest tu całe i jest jednostronne.

    Skład olskiego nie potrzebuje, bo zgodność liczy, zamiast ją sprawdzać, więc
    ten check jest świadkiem, a nie zależnością: nad zdaniem, którego gramatyka
    nie obejmuje, nie ma czego powiedzieć i wtedy takiego przypadku tu nie ma.
    """
    werdykt = check(kompiluj(drzewo))[0]
    assert werdykt.status == "valid", werdykt.explain()


@pytest.mark.parametrize(
    ("podmiot", "oczekiwane"),
    [
        (R.kot, "kot mieszkał"),
        (R.mysz, "mysz mieszkała"),
        (R.zwierzę, "zwierzę mieszkało"),
        (~R.mieszkaniec, "mieszkańcy mieszkali"),
        (~R.mysz, "myszy mieszkały"),
    ],
)
def test_czas_przeszły_zgadza_się_z_podmiotem_rodzajem_wziętym_z_leksykonu(podmiot, oczekiwane):
    """Pięć form, bo pomyłką, którą tu widać, jest wzięcie rodzaju z jednego miejsca.

    Forma przeszła zgadza się rodzajem, a teraźniejsza osobą,
    więc czas jest tu żądaniem innym co do treści, a nie tylko co do wartości,
    i to jest cały powód, dla którego stoi w ``CZASY`` jako dane.
    Liczba mnoga rozdziela się przy tym na dwa rodzaje, a nie na pięć,
    i dlatego stoją tu obie.
    """
    assert V.mieszkać(podmiot).linearyzuj(Kontekst(czas="kiedyś")).napis == oczekiwane


def test_czasownik_bez_dopełnienia_woła_się_tak_samo_jak_z_dopełnieniem():
    """O dopełnienie pyta rama z leksykonu, a nie kształt wywołania.

    ``mieszkać`` biernika nie bierze, więc zdanie z dopełnieniem się zgłasza,
    a bez dopełnienia wychodzi, i jest to jedno wywołanie o dwóch długościach.
    """
    assert kompiluj(V.mieszkać(R.kot)) == "Kot mieszka."
    with pytest.raises(PozaRamą):
        V.mieszkać(R.kot, R.dom)


def test_przeczenie_zabiera_dopełnieniu_biernik_na_rzecz_dopełniacza():
    """Dwie rzeczy naraz i dlatego jedna decyzja: ``nie`` przed czasownikiem i przypadek niżej.

    Dopełniacz negacji jest miejscem, w którym kompilator liczy coś,
    czego autor w drzewie nie napisał i nie miałby gdzie napisać.
    Orzeczenie imienne stoi obok, bo ``nie`` sięga obu orzeczeń tak samo,
    a przypadek traci tylko dopełnienie: narzędnika przeczenie nie rusza.
    """
    assert kompiluj(V.mieć(R.miasto, R.obrońca)) == "Miasto ma obrońcę."
    assert kompiluj(nie(V.mieć(R.miasto, R.obrońca))) == "Miasto nie ma obrońcy."
    assert kompiluj(nie(jest(R.kot, R.potwór))) == "Kot nie jest potworem."


def test_koordynacja_bierze_przypadek_z_pozycji_a_liczbę_od_każdego_członu_osobno():
    """Jedna pozycja, kilka rzeczy: przypadek wspólny, liczba własna.

    Interpunkcja tej listy jest polska: przecinek między członami,
    a spójnik dopiero przed ostatnim.
    """
    części = razem([A.koguci * R.dziób, A.wężowy * R.ogon, ~(A.żabi * R.oko)])
    assert kompiluj(V.mieć(R.bazyliszek, części)) == (
        "Bazyliszek ma koguci dziób, wężowy ogon i żabie oczy."
    )
    assert razem([R.kot, R.mysz]) == Koordynacja((byt(R.kot), byt(R.mysz)))


def test_rodzaj_koordynacji_jest_męskoosobowy_gdy_choć_jeden_człon_taki_jest():
    """Tyle mówi polska zgodność i tyle liczy ta właściwość, zamiast pytać autora."""
    assert (R.mysz & R.mieszkaniec).rodzaj == "m1"
    assert (R.mysz & R.zwierzę).rodzaj != "m1"


def test_ten_sam_przyimek_w_dwóch_relacjach_daje_dwa_przypadki():
    """Relacja stoi w drzewie, a przypadek wychodzi z leksykonu, i to jest cała mechanika.

    Nad samym przyimkiem tych dwóch zdań nie da się rozróżnić,
    więc jest to ta sama wieloznaczność, którą ``Czyj`` zdejmuje w grupie imiennej.
    """
    assert Gdzie.w(R.piwnica).linearyzuj().napis == "w piwnicy"
    assert Dokąd.w(R.kamień).linearyzuj().napis == "w kamień"
    assert Skąd.z(R.piwnica).linearyzuj().napis == "z piwnicy"
    assert czym(R.wzrok).linearyzuj().napis == "wzrokiem"


def test_przyimek_postawiony_w_relacji_której_leksykon_nie_ma_zgłasza_się_od_razu():
    """Zgłoszenie pada przy budowaniu drzewa, tak samo jak przy ramie czasownika."""
    with pytest.raises(PozaRamą):
        Skąd.do(R.piwnica)


def test_przysłówek_wychodzi_w_stopniu_równym_także_wtedy_gdy_stopnia_nie_ma():
    """Dwa przysłówki, bo o odmienności rozstrzyga leksem, a nie część mowy.

    ``nagle`` stopniuje się i pierwszą formą w słowniku nie musi być równa,
    a ``wkrótce`` stopnia nie ma wcale.
    """
    assert D.nagle.linearyzuj().napis == "nagle"
    assert D.wkrótce.linearyzuj().napis == "wkrótce"


def test_wyróżnienie_przestawia_konstytuenty_a_czasownik_zostaje_na_miejscu():
    """Szyk jest wnioskiem z tego, co drzewo mówi o temacie i o tym, co nowe.

    Trzy drzewa różnią się tu tylko wyróżnieniem,
    więc wychodzą z nich trzy zdania o jednym znaczeniu logicznym
    i trzech różnych rzeczach postawionych na czele.
    """
    gdzie = Gdzie.w(R.piwnica)
    assert kompiluj(V.mieszkać(R.bazyliszek, gdzie)) == "Bazyliszek mieszka w piwnicy."
    assert kompiluj(V.mieszkać(R.bazyliszek, temat(gdzie))) == "W piwnicy bazyliszek mieszka."
    assert kompiluj(V.mieszkać(nowe(R.bazyliszek), temat(gdzie))) == "W piwnicy mieszka bazyliszek."


def test_oba_szyki_orzeczenia_imiennego_biorą_się_z_dwóch_drzew():
    """Zdanie z README w dwóch szykach, żaden z nich nie zaszyty w konstruktorze.

    Wysunięty orzecznik jest tu wyborem zapisanym w drzewie,
    więc oba zdania mają jedno znaczenie logiczne i dwie różne rzeczy na czele.
    Widać tu przy okazji dziurę, która została:
    README pisze `zwykły tekst polski`, a grupa imienna wypuszcza `zwykły polski tekst`,
    bo wyróżnienia wewnątrz niej ten zapis nie ma.
    """
    tekst = A.zwykły * A.polski * R.tekst
    assert kompiluj(jest(tekst, R.wejście)) == "Zwykły polski tekst jest wejściem."
    assert kompiluj(jest(nowe(tekst), temat(R.wejście))) == "Wejściem jest zwykły polski tekst."


def test_zaimek_względny_bierze_przypadek_z_pozycji_a_zgodność_z_rzeczy_opisywanej():
    """Zaimek jest tu policzony z dwóch miejsc naraz i to jest cały mechanizm opisu.

    Rodzaj i liczbę ma z rzeczy, która stoi w zdaniu nadrzędnym,
    a przypadek z pozycji, którą zajmuje w podrzędnym,
    więc dopełniacz negacji sięga go tak samo jak sięgnąłby rzeczy w tym miejscu.

    Dwa zdania, bo zmienna raz trzyma rolę, a raz samą rzecz:
    ``~R.postać`` jest rolą, a ``A.ciemny * R.piwnica`` nie,
    i bez zejścia pod rolę drugie z nich zgłasza się jako opis, który nie opisuje.
    """
    postaci = A.kamienny * ~R.postać
    stoją = V.stać(opis(postaci, nie(V.liczyć(R.nikt, postaci))), Gdzie.pod(R.ściana))
    assert kompiluj(stoją, Kontekst(czas="kiedyś")) == (
        "Kamienne postaci, których nikt nie liczył, stały pod ścianą."
    )
    piwnica = A.ciemny * R.piwnica
    mieszkał = opis(piwnica, V.mieszkać(nowe(R.bazyliszek), Gdzie.w(piwnica)))
    assert kompiluj(V.zejść(R.czeladnik, Dokąd.do(mieszkał)), Kontekst(czas="kiedyś")) == (
        "Czeladnik zszedł do ciemnej piwnicy, w której mieszkał bazyliszek."
    )


def test_zaimek_względny_otwiera_zdanie_podrzędne_z_każdej_roli():
    """Czoło zdania podrzędnego nie jest wyborem autora, bo tyle znaczy ten zaimek.

    Raz stoi on w podmiocie, a raz pod przyimkiem w okoliczniku,
    czyli w pozycjach, które bez opisu wypadają w zdaniu w dwóch różnych miejscach.
    """
    kot = R.kot
    assert kompiluj(V.spać(opis(kot, V.zamykać(kot, R.okno)))) == "Kot, który zamyka okno, śpi."
    assert kompiluj(V.spać(opis(kot, V.mieszkać(R.mysz, Gdzie.pod(kot))))) == (
        "Kot, pod którym mysz mieszka, śpi."
    )


def test_zdanie_które_opisywanej_rzeczy_nie_stawia_zgłasza_się_od_razu():
    """Opis, który nie wskazuje, jest błędem drzewa, a nie zdaniem podrzędnym o niczym.

    Trzy sposoby na to samo: zdanie o kimś innym, ta sama rzecz napisana
    drugi raz z osobna, bo tożsamością jest tu zmienna, a nie równość drzew,
    oraz rzecz postawiona pod grupą imienną, skąd zaimek nie wyszedłby na czoło.
    Trzecie jest granicą tej kategorii, a nie pomyłką autora,
    bo `kot, którego ogon goni mysz` jest zdaniem polskim.
    """
    kot = R.kot
    with pytest.raises(PozaRamą):
        opis(kot, V.zamykać(R.mysz, R.okno))
    with pytest.raises(PozaRamą):
        opis(A.stary * R.kot, V.zamykać(A.stary * R.kot, R.okno))
    with pytest.raises(PozaRamą):
        opis(kot, V.gonić(R.mysz, R.ogon / kot))


def test_przecinek_między_konstytuentami_stoi_dokładnie_raz():
    """Przecinka żądają dwie konstrukcje i żadna nie wie, co obok niej stanie.

    Stanąć może pięć rzeczy i każda rozstrzyga inaczej:
    kropka żądania nie spełnia, dalszy konstytuent spełnia je raz,
    przecinek listy jest tym samym przecinkiem, a przed spójnikiem staje mimo to.
    Piąte jest tym, dla którego przecinek przestał być znakiem w napisie:
    dwa żądania spotkane naraz są jednym przecinkiem, a nie dwoma.
    """
    kot = R.kot
    opisany = opis(kot, V.spać(kot))
    gdy = Kiedy.gdy(V.gasnąć(R.świeca))
    assert kompiluj(V.gonić(opisany, R.mysz)) == "Kot, który śpi, goni mysz."
    assert kompiluj(V.gonić(R.mysz, opisany)) == "Mysz goni kota, który śpi."
    assert kompiluj(V.gonić(R.mysz, razem([opisany, R.okno, R.pudełko]))) == (
        "Mysz goni kota, który śpi, okno i pudełko."
    )
    assert kompiluj(V.gonić(R.mysz, razem([opisany, R.okno]))) == (
        "Mysz goni kota, który śpi, i okno."
    )
    assert kompiluj(V.gonić(R.mysz, opisany, gdy)) == (
        "Mysz goni kota, który śpi, gdy świeca gaśnie."
    )


def test_czas_opowiadania_dochodzi_do_zdania_podrzędnego():
    """Kontekst schodzi pod grupę imienną, bo inaczej gubi się dopiero tam.

    Zdanie podrzędne stojące w czasie teraźniejszym wewnątrz opowieści
    czyta się jako zdanie o tym, co jest, a nie o tym, co było,
    więc pomyłka tego rodzaju nie zgłasza się nigdzie i wychodzi tekstem.
    """
    kot = R.kot
    zdanie = V.gonić(R.mysz, R.ogon / opis(kot, V.zamykać(kot, R.okno)))
    assert kompiluj(zdanie, Kontekst(czas="kiedyś")) == (
        "Mysz goniła ogon kota, który zamykał okno."
    )


def test_forma_odesłana_kwalifikatorem_poza_rejestr_nie_wychodzi():
    """Wybór pierwszej z form jest wyborem dopiero po odsianiu tych spoza rejestru.

    Oba lematy pokazała ta opowieść, a nie plan:
    ``któren`` wychodził na każdym zaimku względnym rodzaju męskiego,
    a ``zgasnęła`` na świecy, i żaden z nich nie stoi w tym rejestrze.
    """
    assert odmień("który", "adj", case="nom", number="sg", gender="m1", degree="pos") == "który"
    assert odmień("zgasnąć", "praet", number="sg", gender="f") == "zgasła"


def test_kwalifikator_dziedzinowy_formy_nie_odsyła():
    """Kwalifikator mówi o formie dwie różne rzeczy i tylko jedna z nich jest rejestrem.

    ``oczy`` niosą kwalifikator anatomiczny i są zwykłą polszczyzną,
    więc odsianie po każdym kwalifikatorze naraz zabrałoby je,
    a zostawiłoby ``oka``, czyli oczka w sieci.
    """
    assert odmień("oko", "subst", case="nom", number="pl") == "oczy"


def test_relacja_która_przypadka_nie_zmienia_jest_osobną_relacją_mimo_to():
    """Relacja nazywa to, co autor powiedział, a nie to, w czym mu to wyjdzie.

    ``w nocy`` i ``w piwnicy`` stoją w jednym przypadku i odpowiadają na dwa pytania,
    więc wpis, po którym nic w tekście się nie zmienia, jest tu wpisem mimo to.
    """
    assert Kiedy.w(R.noc).linearyzuj().napis == "w nocy"
    assert Gdzie.w(R.piwnica).linearyzuj().napis == "w piwnicy"


def test_dwa_konstytuenty_wyróżnione_tak_samo_zgłaszają_się_zamiast_stanąć_obok_siebie():
    """Na czele stoi jedna rzecz, więc drugi temat jest drzewem błędnym.

    Bez tego zdanie wychodzi ciche i przestawione,
    a to jest gorszy koniec niż wyjątek, bo autor nie ma po czym poznać, co zrobił.
    """
    with pytest.raises(PozaRamą):
        kompiluj(V.mieszkać(temat(R.bazyliszek), temat(Gdzie.w(R.piwnica))))
