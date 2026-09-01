"""Okolicznik: przysłówek, cząstka i narzędnik bez przyimka wraz z gospodarzem.

Plik pyta o jedną warstwę, a nie o jedną konstrukcję,
i jest to ta warstwa, która ma swój plik w rejestrze konstrukcji
(docs/konstrukcje-gramatyczne/okolicznik.md);
kryterium przynależności podaje nagłówek tamtego rejestru.
Okolicznik pozycji ramy nie zajmuje, a wybór między dwoma gospodarzami
jest całą jego ceną, więc o gospodarza pyta tu większość testów.

Czy zdanie jest olskim — dwa korpusy zdań i kształt odrzucenia —
pyta ``tests/test_subset.py``.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.morph import analyse
from olski.subset import CZĄSTKA_ZDANIA, CZĄSTKI, GRAMMAR, OKOLICZNIK_PRZYSŁÓWKOWY
from tests.test_werdykt import role, verdict


def test_a_fronted_modifier_belongs_to_the_clause_and_not_to_the_subject():
    #  Nothing but the clause rule can take it there, and the failure to guard
    #  against is the subject swallowing it: człon_imienny → subst wyrażenie_przyimkowe makes
    #  the same phrase between the subject and the verb come out valid and wrong.
    roles = role(verdict("Pod względem smaku chałka przewyższa zwykłą bułkę."))[0]
    assert roles["podmiot"] == "chałka"
    #  Streszczenie nazywa konstytuent, do którego przyłączenie doszło, jego
    #  głową, więc zdanie z nazwy tego testu stoi w samym napisie, a nie tylko w
    #  podmiocie obok: gospodarzem jest tu czasownik, a nie `chałka`.
    assert roles["wyrażenie_przyimkowe"] == "Pod względem smaku → przewyższa"


@pytest.mark.parametrize(
    ("text", "rola", "modyfikator"),
    [
        ("Począł myśleć gorączkowo.", "okolicznik_przysłówkowy", "gorączkowo"),
        ("Począł myśleć już.", "cząstka_zdania", "już"),
    ],
)
def test_okolicznik_bez_przyimka_nazywa_gospodarza_tak_jak_wyrażenie_przyimkowe(
    text, rola, modyfikator
):
    #  Gospodarz jest tu całą różnicą między dwoma czytaniami:
    #  `począł (myśleć gorączkowo)` i `(począł myśleć) gorączkowo`.
    #  Usterka, którą to łapie: rola przyłączana bez nazwy gospodarza,
    #  po której werdykt drukuje jeden wiersz dwa razy
    #  i nie mówi o zdaniu nic poza liczbą czytań.
    found = verdict(text)
    assert found.status == "ambiguous", found.explain()
    assert {reading[rola] for reading in role(found)} == {
        f"{modyfikator} → myśleć",
        f"{modyfikator} → Począł",
    }


def test_streszczenie_wiąże_okolicznik_ze_zdaniem_a_nie_z_dopełnieniem():
    #  `okoliczniki` stoją w drzewie pod `wypełnienia`, czyli tuż obok dopełnienia,
    #  więc przyłączenie wzięte z najbliższego węzła z materiałem obok
    #  nazwałoby okolicznik zdania określeniem dopełnienia —
    #  i byłoby to akurat to drugie czytanie, od którego olski to pierwsze odróżnia.
    found = verdict("Program zapisuje ustawienia w pliku w katalogu.")
    zdaniowe = [reading for reading in role(found) if reading["dopełnienie"] == "ustawienia"]
    assert {reading["wyrażenie_przyimkowe"] for reading in zdaniowe} == {
        "w pliku → zapisuje",
        "w pliku w katalogu → zapisuje",
    }


def test_okolicznik_na_czele_zdania_nie_wychodzi_drugim_zdaniem_składowym():
    #  Usterka, którą to łapie: zdanie składowe policzone dwa razy. Okolicznik
    #  zdania dokłada nad składowym drugi węzeł o tej samej etykiecie
    #  (`zdanie_składowe → wyrażenie_przyimkowe zdanie_składowe`), więc zbieranie wszystkich
    #  takich węzłów zamiast najwyższego w gałęzi widzi tu ciąg dwóch zdań
    #  i rozcina streszczenie na dwa, choć zdanie składowe jest jedno.
    [streszczenie] = verdict("Pod względem smaku chałka przewyższa zwykłą bułkę.").readings
    assert len(streszczenie) == 1, streszczenie


@pytest.mark.parametrize(
    "text",
    [
        #  Po podmiocie w szyku SVO, i po dopełnieniu w szyku OVS.
        "Program w tym trybie zapisuje ustawienia.",
        "Ustawienia w pliku zapisuje program.",
        #  Po podmiocie w szykach z czasownikiem na czele, przed orzecznikiem i za nim.
        "Trwa dochodzenie w tej sprawie.",
        "Są ludzie w tej sprawie wolni.",
        #  Po orzeczniku wysuniętym przed kopulę.
        "Wejściem w tym trybie jest zwykły tekst.",
        #  Przed dopełnieniem, wewnątrz orzeczenia.
        "Program zapisuje w pliku ustawienia.",
        #  Za bezokolicznikiem, gdzie dochodzi i do niego, i do formy osobowej.
        "Muszę jechać do domu.",
        #  Po rzeczowniku, który ma już przy sobie przymiotnik albo dopełniacz,
        #  i po imiesłowie.
        "Trwa akcja zbrojna w Strefie Gazy.",
        "Rozmieszczenie ogrodów w Polsce jest nierównomierne.",
        "Ludzie są powiązani z interesami.",
    ],
)
def test_żadna_pozycja_okolicznika_nie_daje_jednego_czytania(text):
    #  Cena decyzji z docs/subset.md o przyłączaniu wyrażeń przyimkowych, i to ta
    #  jej połowa, której nie widać po zdaniach odrzuconych. Gdy gramatyka ma
    #  regułę na jedno z dwóch przyłączeń, zdanie wychodzi jednoznaczne i olski
    #  wybiera po cichu to, czego wybierać nie miał. Każde zdanie tutaj stoi na
    #  innej pozycji okolicznika i żadne nie ma wychodzić jednym czytaniem.
    assert verdict(text).status == "ambiguous", verdict(text).explain()


def test_pozycje_okolicznika_w_orzeczeniu_nie_zachodzą_na_siebie():
    #  Cztery ciała `wypełnienia` stawiają okolicznik przed dopełnieniem i za nim,
    #  a `okoliczniki` nawraca samo na siebie, więc dwie pozycje łatwo tu wypisać tak,
    #  żeby jedno zdanie wychodziło dwoma kształtami drzewa. Nie widać tego po
    #  werdykcie, bo zdanie jest wieloznaczne w jedną i w drugą stronę, i nie widać
    #  po rolach, bo obie pary przyłączeń zostają te same; widać po liczbie czytań.
    #  Werdykt nazywa tu jedno przyłączenie z dwóch, i to jest ta ostrość, którą
    #  las kupuje: `w pliku` dochodzi do zdania w obu czytaniach.
    found = verdict("Autor zapisuje w pliku w katalogu.")
    assert found.explain() == '2 odczytania; „w katalogu” → „zapisuje”, „pliku”'


def test_forma_poprzyimkowa_nie_stoi_okolicznikiem_bez_przyimka_przed_sobą():
    #  `adjp` jest u Morfeusza formą, która poza przyimkiem nie stoi, i cała ta
    #  pozycja jest ciałem o dwóch córkach właśnie dlatego. Usterka, którą to
    #  łapie: `adjp` dopisane do części mowy terminala okolicznika zamiast do
    #  osobnego ciała — wtedy każde zdanie z taką formą samą dostaje czytanie,
    #  którego polszczyzna nie ma, a werdykt drugiego zdania mówi `valid`.
    assert verdict("Reguła działa po polsku.").status == "valid"
    assert verdict("Reguła działa polsku.").status == "rejected"


def test_dwóch_gospodarzy_przysłówka_rozdziela_w_streszczeniu_rola():
    """Para gospodarzy jest tym, czym przysłówek atakuje jednoznaczność.

    Zdanie z przysłówkiem stopniowanym przed przymiotnikiem ma dwa czytania i oba
    są polszczyzną w tym sensie, w jakim liczy je ta gramatyka: raz przysłówek
    określa przymiotnik, a raz całe zdanie. Streszczenie ma je rozdzielać, i
    rozdziela je rolą, bo określenie przymiotnika stoi wewnątrz orzecznika, a
    okolicznik zdania niesie własną rolę; docs/subset.md wycenia tę parę.
    """
    found = verdict("Plik jest bardzo duży.")
    assert found.status == "ambiguous", found.explain()
    assert {czytanie.get("orzecznik") for czytanie in role(found)} == {
        "bardzo duży",
        "duży",
    }
    assert {czytanie.get("okolicznik_przysłówkowy") for czytanie in role(found)} == {
        None,
        "bardzo → jest",
    }


def test_okolicznik_staje_po_czasowniku_i_daje_zdaniu_czytanie_z_podmiotem():
    """Pozycja okolicznika po córce czasownikowej, wzięta z obu stron naraz.

    Zdania są dwa, bo brak tej pozycji płacił w dwóch walutach: pierwsze było
    odrzucone, a drugie wychodziło jednym czytaniem, w którym `program
    ustawienia` jest dopełnieniem, czyli werdyktem `valid` mówiącym o zdaniu
    nieprawdę.
    """
    trwa = verdict("Trwa w tej sprawie dochodzenie.")
    assert trwa.status == "valid", trwa.explain()
    assert role(trwa)[0]["podmiot"] == "dochodzenie"
    zapisuje = verdict("Zapisuje w pliku program ustawienia.")
    assert ("program", "ustawienia") in {
        (czytanie.get("podmiot"), czytanie.get("dopełnienie")) for czytanie in role(zapisuje)
    }, zapisuje.explain()


def test_przysłówek_przed_przysłówkiem_dochodzi_do_niego_a_nie_do_zdania():
    """Gospodarz trzeci, czyli ten, który zdejmuje ostatnią klasę płaskich czytań.

    Bez niego zdanie wychodziło jednym czytaniem, w którym `bardzo` jest
    okolicznikiem zdania na równi z `szybko`, czyli werdyktem `valid` mówiącym o
    zdaniu nieprawdę; kurs, po którym ta pozycja weszła, trzyma docs/subset.md.
    Czytania są odtąd dwa i rozdziela je rola, tak samo jak przy przymiotniku:
    pod trzecim gospodarzem cały `bardzo szybko` jest jednym okolicznikiem.
    """
    found = verdict("Program zapisuje ustawienia bardzo szybko.")
    assert found.status == "ambiguous", found.explain()
    assert {czytanie.get("okolicznik_przysłówkowy") for czytanie in role(found)} == {
        "bardzo szybko → zapisuje",
        "bardzo → zapisuje",
    }


def test_przysłówek_okolicznikowy_dostaje_rolę_a_nie_samo_wyprowadzenie():
    #  Pozycja dopisana bez roli daje `valid` bez słowa o tym, co olski w zdaniu
    #  przyjął, a rola jest tym, po co werdykt stoi (docs/roadmap.md).
    found = verdict("Program zapisuje ustawienia szybko.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["okolicznik_przysłówkowy"] == "szybko → zapisuje"


def test_cząstka_dostaje_rolę_osobną_od_przysłówka_w_obu_pozycjach():
    #  Rola jest osobna, bo cząstka przysłówkiem nie jest: `okolicznik_przysłówkowy: już` mówiłoby o
    #  zdaniu, że ma okolicznik przysłówkowy, którego ono nie ma. Pozycje przy zdaniu
    #  są dwie i pisze je jedna pętla razem z przysłówkiem, więc zdania są dwa:
    #  rozejście się tych dwóch kompletów widać dopiero na tym, którego jedna z nich
    #  nie bierze. Zdanie drugie cząstkę wpuszcza także do podmiotu, więc pytamy o
    #  rolę wśród czytań, a nie o pierwsze z nich.
    okolicznik = verdict("Program już zapisuje ustawienia.")
    assert role(okolicznik)[0][CZĄSTKA_ZDANIA] == "już → zapisuje", okolicznik.explain()
    assert OKOLICZNIK_PRZYSŁÓWKOWY not in role(okolicznik)[0], okolicznik.explain()
    czoło = verdict("Już program zapisuje ustawienia.")
    assert "Już → zapisuje" in {
        czytanie.get(CZĄSTKA_ZDANIA) for czytanie in role(czoło)
    }, czoło.explain()


def test_cząstka_w_grupie_imiennej_wchodzi_w_zasięg_roli_a_nie_obok_niej():
    """Gospodarz drugi, czyli ten, po którym podmiotem jest cała `Nawet ptaki`.

    Bez niego zdanie wychodziło jednym czytaniem, w którym podmiotem jest samo
    `ptaki`, choć bank drzew czyta tam grupę razem z cząstką; cenę tej pozycji
    trzyma docs/subset.md. Czytania są dwa, bo o gospodarzu nie rozstrzyga ani
    cecha, ani lemat, a rozdziela je zasięg podmiotu wraz z listą ról: cząstka
    obejmująca grupę etykiety nie nosi.
    """
    found = verdict("Nawet ptaki przestały śpiewać.")
    assert found.status == "ambiguous", found.explain()
    assert {
        (czytanie.get("podmiot"), czytanie.get(CZĄSTKA_ZDANIA)) for czytanie in role(found)
    } == {("Nawet ptaki", None), ("ptaki", "Nawet → przestały")}, found.explain()


def test_cząstka_w_grupie_imiennej_przepuszcza_osobę_zaimka():
    #  Przymiotnik i zaimek dzierżawczy ogłaszają trzecią osobę, a cząstka ją
    #  przepuszcza, bo staje i przed zaimkiem. Z `ter` w tym ciele grupa nie zgodziłaby
    #  się z czasownikiem osobą i to czytanie by nie wyszło.
    found = verdict("Nawet ja zapisuję ustawienia.")
    assert "Nawet ja" in {czytanie.get("podmiot") for czytanie in role(found)}, found.explain()


@pytest.mark.parametrize("lemat", sorted(CZĄSTKI))
def test_cząstka_z_listy_nie_ma_czytania_branego_gdzie_indziej(lemat):
    #  Kryterium na wejście do tej listy, postawione lemat po lemacie: cząstka,
    #  której inne czytanie gramatyka bierze, daje jednemu napisowi dwa
    #  wyprowadzenia. `tylko` jest u Morfeusza także spójnikiem, więc dopisane tu
    #  kosztowałoby czytanie każdego zdania, w którym stoi, i tego ten test pilnuje
    #  po stronie listy, a nie po stronie zdania.
    [segment] = analyse(lemat)
    czytania = [(r.tag.pos, r.lemma, segment.lematy, r.tag.cechy) for r in segment.readings]
    brane = [c for c in czytania if GRAMMAR.licencjonuje(*c)]
    assert brane, (lemat, czytania)
    assert {pos for pos, *_ in brane} == {"part"}, (lemat, brane)


@pytest.mark.parametrize(
    ("zdanie", "status"),
    [
        ("Koszt bardzo dużego pliku jest niski.", "valid"),
        ("Koszt tu dużego pliku jest niski.", "rejected"),
    ],
)
def test_do_przymiotnika_dochodzi_przysłówek_stopniowany_a_do_zdania_każdy(zdanie, status):
    """Terminale są dwa, bo warunek należy do jednego gospodarza, a nie do obu.

    Bez tego podziału pozycja przy przymiotniku bierze `tu` tak samo jak `bardzo`,
    a przysłówek bez stopnia stoi wtedy w dwóch trzecich zdań, które ta pozycja
    czyta wbrew drzewu wzorcowemu (docs/subset.md). Zdania są dwa i różni je sam
    przysłówek, bo o różnicę między dwiema jego klasami tu chodzi: pozycji w
    grupie imiennej `tu` nie ma, a okolicznik zdania w tym miejscu nie stoi.
    """
    assert verdict(zdanie).status == status


def test_gospodarzem_przyłączenia_zostaje_przymiotnik_a_nie_przysłówek_przed_nim():
    """Głowa jest numerem pozycji w ciele, więc stoi na przymiotniku, a nie przed nim.

    Bez tego werdykt nazywa gospodarzem przyłączenia przysłówek —
    `z interesami → bardzo` — czyli mówi o zdaniu coś, czego polszczyzna nie ma,
    a liczba czytań zostaje przy tym ta sama, więc żadna tabela tego nie pokaże.

    Gospodarze wchodzą tu zbiorem, bo żądanie jest o to, którzy nimi są, a nie o
    kolejność, w jakiej las wydaje czytania.
    """
    found = verdict("Program jest bardzo powiązany z interesami.")
    assert {czytanie.get("wyrażenie_przyimkowe") for czytanie in role(found)} == {
        "z interesami → powiązany",
        "z interesami → jest",
    }


def test_okolicznik_przy_bezokoliczniku_ma_dwóch_gospodarzy():
    #  Fraza bezokolicznikowa bierze okolicznik przez to samo `wypełnienia`,
    #  którym bierze go forma osobowa nad nią, więc stoi wśród gospodarzy
    #  przyłączenia. Bez niej okolicznik wychodzi do zdania w obu czytaniach,
    #  oba streszczają się jednym napisem, a werdykt mówi samo `2 odczytania`.
    found = verdict("Syn usiłował wejść na ołtarz.")
    assert found.result.ile == 2, found.explain()
    (przyłączenie,) = found.result.przyłączenia
    assert przyłączenie.gospodarze == ("usiłował", "wejść")


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Wysunięty modyfikator z okolicznikiem wyrażonym zdaniem, czyli to zdanie,
        #  na którym tę parę kształtów zauważono, oraz z wtrąceniem.
        "Na stole leży sto dwadzieścia chlebów, bo piekarz je tam położył.",
        "Na stole leży chleb (docs/subset.md).",
    ],
)
def test_określenie_z_obu_stron_zdania_nie_daje_dwóch_kształtów(zdanie):
    #  Niezmiennik o zapisanym porządku par (``tests/test_subset.py``) mówi
    #  o produkcjach, a to zdanie o werdykcie, bo cecha zapisana w ciałach
    #  i zdanie wychodzące jednym czytaniem to dwie rzeczy.
    found = verdict(zdanie)
    assert found.status == "valid", found.explain()


# --------------------------------------------------------------------------- #
# Imiesłów przysłówkowy
# --------------------------------------------------------------------------- #


def test_imiesłów_przysłówkowy_bierze_ramę_swojego_lematu():
    #  Rama idzie z głowy cechą, tak samo jak przy formie nieosobowej, więc lemat,
    #  o którym leksykon mówi, że biernika nie bierze, nie bierze go i tutaj.
    #  Usterka, którą to łapie: rama wypisana przy tych ciałach ręką, po której
    #  imiesłów bierze wszystko, co bierze czasownik dowolny.
    assert verdict("Program zapisuje ustawienia, pomagając linterowi.").status == "valid"
    odrzucone = verdict("Program zapisuje ustawienia, pomagając zgodność.")
    assert odrzucone.status == "rejected", odrzucone.explain()


@pytest.mark.parametrize(
    ("zdanie", "gospodarz"),
    [
        #  Imiesłów nie ma pod sobą zdania składowego, więc bez wpisu wśród
        #  gospodarzy zejście mija cały ten okolicznik i nazywa orzeczenie zdania
        #  nadrzędnego. Usterka, którą to łapie: oba czytania mówią wtedy
        #  `→ zapisuje`, więc wychodzą z werdyktu jednym napisem.
        ("Program zapisuje ustawienia, sprawdzając zgodność z dokumentem.", "sprawdzając"),
        #  Drugiej głowy tego symbolu ten sam wpis ruszyć nie ma: pod zdaniem
        #  podrzędnym stoi `zdanie_składowe`, na którym zejście staje wcześniej.
        ("Program zapisuje ustawienia, gdy linter sprawdza zgodność z dokumentem.", "sprawdza"),
    ],
)
def test_gospodarzem_pod_okolicznikiem_jest_jego_własna_głowa(zdanie: str, gospodarz: str):
    found = verdict(zdanie)
    assert f"„z dokumentem” → „{gospodarz}”" in found.explain(), found.explain()
