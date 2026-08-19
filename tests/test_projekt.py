"""Leksykon projektu, czyli polskie słowo odmienione, którego słownik nie ma.

Wpis wskazuje leksem, a nie wypisuje form, więc pilnować trzeba dwóch rzeczy
naraz: że z leksemu wychodzi odmiana naszego słowa, i że wzorzec dobrany źle
zgłasza się, zamiast wydać formę, której polszczyzna nie ma.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.morph import analyse
from olski.projekt import WPISY, Wpis, ZłyWpis, czytania, odmiana
from olski.subset import check, morphology


def formy(wpis):
    return {czytanie.form for czytanie in odmiana(wpis)}


def test_język_olski_umie_powiedzieć_sam_w_sobie_czym_jest():
    #  Kryterium wyjścia etapu 5 z docs/roadmap.md: zdanie o nazwie własnej tego
    #  języka wyprowadza się i wyprowadza raz. Bez leksykonu `olski` wracało jako
    #  `ign`, którego nie bierze ani jedna produkcja.
    werdykty = check("Język olski jest podzbiorem polszczyzny.")
    assert [werdykt.status for werdykt in werdykty] == ["valid"]


def test_wpis_wskazuje_leksem_a_formy_wydaje_słownik():
    #  Ani jednej formy nie ma w pliku, a paradygmat wychodzi cały.
    wpis = Wpis(lemat="olski", wzorzec="polski:A", świadek="olskim")
    assert {"olski", "olskiego", "olskim", "olską", "olscy"} <= formy(wpis)


def test_temat_wzorca_niesie_swoją_alternację():
    #  Granicę tematu wycina to, na czym formy wzorca przestają się zgadzać, więc
    #  `bacie` schodzi do tematu `ba`, a `commit` bierze stąd i miejscownik z
    #  alternacją, i liczbę mnogą bez niej.
    wpis = Wpis(lemat="commit", wzorzec="bat:Sm3~a", świadek="commita")
    assert {"commita", "commicie", "commitach", "commitów"} <= formy(wpis)


def test_przedrostek_wzorca_zostaje_przed_podmienionym_tematem():
    #  Podmiana idzie tam, gdzie temat stoi, a nie na początku formy, bo słownik
    #  trzyma formę zaprzeczoną w tym samym paradygmacie: gdyby podmiana czepiała
    #  się początku, `niemalowanie` nie dałoby ani jednej formy naszego słowa.
    wpis = Wpis(lemat="lintować", wzorzec="malować", świadek="lintuje")
    assert {"lintuje", "lintowanie", "nielintowanie"} <= formy(wpis)


def test_wzorzec_alternujący_inaczej_łapie_się_na_świadku():
    #  Cała cena wskazania leksemu zamiast wypisania form: `pies` daje temat `p`
    #  wraz z końcówką `ies`, więc `bies` dostałby z niego dopełniacz `bsa`.
    #  Świadek jest tym, co tę pomyłkę zgłasza, zamiast wydać ją jako polszczyznę.
    wpis = Wpis(lemat="bies", wzorzec="pies:Sm2", świadek="biesa")
    with pytest.raises(ZłyWpis, match="biesa"):
        odmiana(wpis)


def test_świadkiem_nie_jest_lemat():
    #  Lemat wydaje każdy wzorzec, który przeszedł warunek na końcówkę, więc
    #  świadek równy lematowi jest kolumną wypełnioną, a nie świadkiem.
    wpis = Wpis(lemat="olski", wzorzec="polski:A", świadek="olski")
    with pytest.raises(ZłyWpis, match="inna niż lemat"):
        odmiana(wpis)


def test_lemat_bez_końcówki_wzorca_zgłasza_się_zamiast_wziąć_temat_wzorca():
    #  `figura` daje końcówkę `a`, której `commit` nie ma, i bez tego warunku
    #  podmiana tematu wydałaby formy wzorca, a nie naszego słowa.
    wpis = Wpis(lemat="commit", wzorzec="figura", świadek="commity")
    with pytest.raises(ZłyWpis, match="końcówki"):
        odmiana(wpis)


def test_wzorcem_nie_jest_paradygmat_o_dwóch_tematach():
    #  Granica tematu jest tu granicą stosowania: `iść` odmienia się przez `szedł`,
    #  więc ani jedna litera lematu nie stoi w każdej jego formie i temat nie ma
    #  skąd wyjść. Zgłasza się to zamiast wydać formy wzorca nietknięte.
    wpis = Wpis(lemat="pójść", wzorzec="iść", świadek="pójdzie")
    with pytest.raises(ZłyWpis, match="wspólnego tematu"):
        odmiana(wpis)


def test_leksem_którego_słownik_nie_ma_zgłasza_się_zamiast_milczeć():
    #  Literówka w identyfikatorze nie ma jak wydać ani jednej formy, więc
    #  zgłasza się tutaj, a nie na zdaniu, w którym to słowo stanie.
    wpis = Wpis(lemat="olski", wzorzec="polski:X", świadek="olskiego")
    with pytest.raises(ZłyWpis, match="polski:X"):
        odmiana(wpis)


def test_każdy_wpis_leksykonu_wydaje_swojego_świadka():
    #  Świadka sprawdza sama odmiana, więc wpis zły zgłasza się przy pierwszym
    #  zdaniu, w którym to słowo stanie. Test woła go po kolei nad całym plikiem,
    #  bo inaczej zły wiersz czeka na zdanie, które ktoś kiedyś napisze.
    for wpis in WPISY:
        assert wpis.świadek in formy(wpis)


def test_dwa_wpisy_jednego_lematu_dokładają_komórkę_a_nie_drugi_paradygmat():
    #  `konstytuent` ma w tej prozie dwa dopełniacze, a jeden narzędnik, choćby
    #  stał w obu paradygmatach: czytania powtórzone schodzą, więc druga rama
    #  wpisu nie czyni wieloznacznym ani jednego zdania.
    assert len(czytania("konstytuentem")) == 1
    assert len(czytania("konstytuentu")) == 1
    assert len(czytania("konstytuenta")) == 1


def test_forma_wraca_taka_jak_stoi_w_tekście():
    #  Tak samo oddaje ją Morfeusz: `Program` wraca od niego z lematem `program`,
    #  a z formą pisaną wielką literą, bo zdanie się od niej zaczyna.
    assert {czytanie.form for czytanie in czytania("Olski")} == {"Olski"}
    assert {czytanie.lemma for czytanie in czytania("Olski")} == {"olski"}


def test_czytanie_nieznane_schodzi_z_krawędzi_którą_leksykon_nazwał():
    #  `ign` mówi, że tego słowa nie zna nikt, a leksykon właśnie je nazwał.
    czytania_formy = morphology("commitów")[0].readings
    assert [str(czytanie) for czytanie in czytania_formy] == ["commitów:commit:subst:pl:gen:m3"]


def test_żadnej_formy_leksykonu_słownik_nie_zna():
    #  Na tym stoi cena tej warstwy: czytania dochodzą tylko do form, których
    #  słownik nie czyta wcale, więc zdanie bez ani jednego słowa tego leksykonu
    #  wychodzi z werdyktem nietkniętym, a zdanie z takim słowem było przedtem
    #  odrzucone, bo `ign` nie bierze żadna produkcja. Wpis, który tę własność
    #  łamie, dokłada czytanie zdaniom, które już się wyprowadzają.
    for wpis in WPISY:
        for czytanie in odmiana(wpis):
            znane = [
                reading
                for segment in analyse(czytanie.form)
                for reading in segment.readings
                if reading.tag.known
            ]
            assert not znane, f"{czytanie.form}: słownik ma dla tej formy {znane}"


def test_każda_forma_leksykonu_jest_dla_morfeusza_jedną_krawędzią():
    #  Czytania dokłada się krawędzi, a nie rozpiętości, więc forma podzielona na
    #  kilka krawędzi zgubiłaby je w ciszy: wpisu nie widziałby żaden segment.
    for wpis in WPISY:
        for czytanie in odmiana(wpis):
            assert len(analyse(czytanie.form)) == 1, czytanie.form
