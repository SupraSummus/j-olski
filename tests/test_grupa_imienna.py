"""Grupa imienna: koordynacja i jej zasięg, przydawka, liczebnik i zaimki.

Plik pyta o jedną warstwę, a nie o jedną konstrukcję,
i jest to ta warstwa, która ma swój plik w rejestrze konstrukcji
(docs/konstrukcje-gramatyczne/grupa-imienna.md);
kryterium przynależności podaje nagłówek tamtego rejestru.
Koordynacja należy tu tą stroną, którą spina człony wewnątrz grupy;
o tę, którą spina zdania, pyta ``tests/test_zdanie_złożone.py``.

Czy zdanie jest olskim — dwa korpusy zdań i kształt odrzucenia —
pyta ``tests/test_subset.py``.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.grammar import EMPTY, bierze, word
from olski.morph import analyse
from olski.subset.słowa import CZĄSTKI, CZĄSTKI_PRZY_LICZEBNIKU
from tests.test_werdykt import role, verdict


def test_termin_z_dopełniaczem_bierze_wyrażenie_przyimkowe_na_własną_głowę():
    #  Usterka, przed którą to broni: pozycja z przymiotnikiem i dopełniaczem
    #  dopisana bez swojej pozycji z okolicznikiem za nią. Zdanie zostaje wtedy
    #  wieloznaczne, więc po werdykcie nie widać, że w pliku nie dochodzi już do
    #  samych ustawień, choć polszczyzna to czytanie ma — i stąd liczba obok
    #  zbioru, bo dwa z trzech czytań mają to samo dopełnienie i różnią się
    #  wewnątrz niego, czyli tym, do czego w pliku doszło
    #  (docs/subset.md#przyjąć-koszt-to-znaczy-dać-oba-czytania-wszędzie).
    found = verdict("Program zapisuje ustawienia domyślne użytkownika w pliku.")
    assert found.status == "ambiguous", found.explain()
    assert len(found.readings) == 3
    assert {reading["dopełnienie"] for reading in role(found)} == {
        "ustawienia domyślne użytkownika w pliku",
        "ustawienia domyślne użytkownika",
    }


def test_coordination_does_not_loosen_agreement_inside_a_conjunct():
    #  The failure to guard against: an adjective scoping over the whole
    #  coordination, which would let a singular feminine one head two masculine
    #  plural nouns. An adjective attaches inside a conjunct, so nowe programy i
    #  pliki is [nowe programy] i [pliki] and the disagreement below has nowhere
    #  to hide.
    assert verdict("Nowa programy i pliki mają nazwy.").status == "rejected"


def test_koordynacja_przecinkiem_żąda_zgodności_tak_samo_jak_spójnik():
    #  Usterka, przed którą to stoi: produkcja z przecinkiem dopisana bez cech
    #  zgodności, która wygląda jak lustro produkcji ze spójnikiem i przyjmuje
    #  grupę przymiotnikową uzgodnioną z niczym.
    assert verdict("Pliki są nowe, duże.").status == "valid"
    assert verdict("Pliki są nowe, duży.").status == "rejected"


def test_ciąg_przydawki_zgadza_się_z_rzeczownikiem_każdym_członem():
    #  Usterka, przed którą to stoi: ogon ciągu dopisany bez cech zgodności,
    #  czyli produkcja, która wygląda jak koordynacja imienna, a wpuszcza pod
    #  jeden rzeczownik przymiotniki uzgodnione z niczym.
    assert verdict("Nowy i tani parser zapisuje ustawienia.").status == "valid"
    assert verdict("Nowy i tania parser zapisuje ustawienia.").status == "rejected"


def test_ciąg_przydawki_o_trzech_członach_wyprowadza_się_raz():
    #  Usterka, przed którą to stoi: przydawka koordynowana produkcją stojącą
    #  nad samą sobą, bez pary symboli. Zdanie wychodzi wtedy przyjęte tak samo,
    #  a czytań ma tyle, ile ten ciąg dopuszcza nawiasowań, więc widać ją po
    #  jednoznaczności, a nie po tym, czy zdanie się wyprowadza.
    found = verdict("Nowy, tani i szybki parser zapisuje ustawienia.")
    assert found.status == "valid", found.explain()


def test_ciąg_rozdzielny_stoi_za_rzeczownikiem_i_nie_stoi_przed_nim():
    #  Usterka, przed którą to stoi: ciało rozdzielne wpuszczone w oba szyki
    #  przydawki, czyli czytanie, w którym `Trzecia i czwarta` są dwiema
    #  warstwami stojącymi przed swoim rzeczownikiem, a polszczyzna go nie ma.
    #  Zdania to nie odrzuca, bo wyprowadza się ono ciągiem imiennym, więc bez
    #  cechy zatrzymującej ten szyk wychodzi ono wieloznaczne.
    assert verdict("Warstwy trzecia i czwarta pracują.").status == "valid"
    assert verdict("Trzecia i czwarta warstwy pracują.").status == "valid"


def test_ciąg_zgodny_nie_bierze_ogona_rozdzielnego():
    #  Usterka, przed którą to stoi: ogon ciągu zgodnego pytany o samą zgodność,
    #  bez cechy, czyli czytanie, w którym pierwsza przydawka orzeka o wszystkich
    #  warstwach, a dwie następne dzielą je między siebie. Zdanie zostaje przyjęte
    #  ciągiem imiennym, więc usterkę widać po jednoznaczności.
    assert verdict("Warstwy nowe i trzecia i czwarta pracują.").status == "valid"


def test_wyrażenie_przyimkowe_dochodzi_i_do_członu_ostatniego_i_do_całego_ciągu():
    #  Usterka, przed którą to stoi: pozycja nad ciągiem dopisana produkcją
    #  rekurencyjną `grupa_imienna → grupa_imienna wyrażenie_przyimkowe`,
    #  czyli bez spójnika w ciele. Zdania są dwa, bo każde pokazuje inną jej połowę.
    #  Nawias mówi, którego członu wyrażenie sięga, więc zasięgi są tu trzy i każdy
    #  da się nazwać; tamta produkcja zabiera nawias ostatniemu z nich, bo
    #  gospodarzem jest w nim cała grupa.
    found = verdict("Pliki i katalogi w tym drzewie rosną.")
    assert found.status == "ambiguous", found.explain()
    assert {reading["podmiot"] for reading in role(found)} == {
        "Pliki i katalogi",
        "Pliki i [katalogi w tym drzewie]",
        "Pliki i katalogi [w tym drzewie]",
    }
    #  Grupa bez koordynacji ma dwa czytania i tyle ma ich mieć: tamta produkcja
    #  dokłada trzecie, którego werdykt nie ma czym odróżnić od pierwszego, bo obu
    #  daje tego samego gospodarza.
    bez_ciągu = verdict("Katalogi w tym drzewie rosną.")
    assert len(bez_ciągu.readings) == 2, bez_ciągu.explain()


def test_grupa_liczebnikowa_zgadza_się_tym_czego_nie_ma_w_środku():
    #  Usterka, przed którą to stoi: liczba i rodzaj wypuszczone z liczebnika
    #  zmienną wspólną, tak jak wypuszcza je każda inna produkcja tej gramatyki.
    #  Wygląda to poprawnie i odwraca zgodność, bo `pięć` jest mnogie, a grupa,
    #  którą buduje, żąda czasownika w liczbie pojedynczej i rodzaju nijakim.
    #  Zdanie przyjęte tego nie łapie, bo cechy, której konstytuent nie niesie,
    #  unifikacja nie sprawdza, więc para zdań rozstrzyga o obu stronach naraz.
    assert verdict("Pięć kobiet przyszło.").status == "valid"
    assert verdict("Pięć kobiet przyszły.").status == "rejected"


def test_liczebnik_zgodny_zgadza_się_ze_swoim_rzeczownikiem():
    #  Ciało zgodne jest tu tym, czym przymiotnik przed rzeczownikiem, więc pilnuje
    #  go to samo, co tamtego: rodzaj złamany parą form, których polszczyzna obok
    #  siebie nie stawia.
    assert verdict("Dwie kobiety przyszły.").status == "valid"
    assert verdict("Dwa kobiety przyszły.").status == "rejected"


def test_liczebnik_rządzący_żąda_rodzaju_od_swojego_dopełniacza():
    #  Rodzaj przechodzi z liczebnika na dopełniacz, choć grupa nad nimi wychodzi
    #  nijaka, i bez tego warunku obie formy liczebnika biorą każdy rzeczownik:
    #  rodzaj męskoosobowy ma w polszczyźnie własną formę i to ona tu rozstrzyga.
    assert verdict("Pięciu mężczyzn przyszło.").status == "valid"
    assert verdict("Pięć mężczyzn przyszło.").status == "rejected"


def test_liczebnik_złożony_przyłącza_się_wedle_swojego_ostatniego_członu():
    #  Usterka, przed którą to stoi: łańcuch wypuszczający `accommodability` członu
    #  pierwszego albo zmienną wspólną wszystkim członom. Jedno i drugie wygląda
    #  poprawnie, bo `dwadzieścia` rządzi dopełniaczem, a przyłączenie rozstrzyga tu
    #  człon skrajnie prawy: `dwa` żąda mianownika mnogiego i czasownika mnogiego,
    #  `siedem` dopełniacza mnogiego i czasownika pojedynczego. Cechy, której
    #  konstytuent nie niesie, unifikacja nie sprawdza, więc każda strona żąda pary.
    #  Zdanie ostatnie stawia z przodu dwa człony naraz, bo łańcuch spłaszczony do
    #  dwóch członów przechodzi wszystkie pozostałe zdania.
    assert verdict("Dwadzieścia dwa chleby leżą.").status == "valid"
    assert verdict("Dwadzieścia dwa chleby leży.").status == "rejected"
    assert verdict("Dwadzieścia siedem chlebów leży.").status == "valid"
    assert verdict("Dwadzieścia siedem chlebów leżą.").status == "rejected"
    assert verdict("Sto dwadzieścia dwa chleby leżą.").status == "valid"


def test_łańcuch_liczebnikowy_żąda_jednego_przypadka_od_każdego_członu():
    #  Polszczyzna odmienia każdy człon, więc przypadek jest w łańcuchu zmienną
    #  wspólną. Bez niej `dwadzieścia dwóch` wyprowadza się tak samo jak
    #  `dwudziestu dwóch`, czyli mianownik miesza się z dopełniaczem.
    assert verdict("Dwadzieścia dwóch mężczyzn przyszło.").status == "rejected"


def test_cząstka_przybliżająca_przepuszcza_cechy_liczebnika_pod_sobą():
    #  Cząstka ma być przezroczysta, więc każde zdanie tu pyta o jedną cechę, którą
    #  ciało wypuszcza w górę, i pyta o nią zdaniem, które bez cząstki wychodzi tak
    #  samo. Pierwsza para pyta o zgodność: cechy wzięte z cząstki zamiast z
    #  liczebnika — znacznik głowy na cząstce albo :data:`AGREE` zdjęte z liczebnika
    #  — zostawiają grupę bez przypadka, liczby i rodzaju, a cechy, której
    #  konstytuent nie niesie, unifikacja nie sprawdza, więc zdanie drugie
    #  przechodzi. Zdanie trzecie pyta o przyłączenie zgodne, bo pierwsza para stoi
    #  na rządzącym. Czwarte pyta o samo `accommodability`: bez niego grupę bierze
    #  ciało rządzące nad ciałem zgodnym i `dwóch chlebów` czyta się dwojako,
    #  dokładnie tak, jak czyta się zagnieżdżony łańcuch wyżej.
    assert verdict("Przeszło pięć kobiet przyszło.").status == "valid"
    assert verdict("Przeszło pięć kobiet przyszły.").status == "rejected"
    assert verdict("Przeszło dwie kobiety przyszły.").status == "valid"
    assert verdict("Brakuje przeszło dwóch chlebów.").status == "valid"


def test_cząstka_przybliżająca_żąda_liczebnika_a_nie_grupy_imiennej():
    #  Ciało dopisane poziom wyżej, czyli przy grupie imiennej, przechodzi oba te
    #  zdania i przechodzi tak samo zgodność wyżej, więc bez tej pary nie widać, na
    #  którym poziomie pozycja stanęła. `setka` jest rzeczownikiem, a `tysiąc` czyta
    #  się i liczebnikiem, i rzeczownikiem, więc ciało żądające liczebnika czytanie
    #  rzeczownikowe zdejmuje, zamiast dołożyć swoje.
    assert verdict("Rejestr pisze przeszło setkę zdań.").status == "rejected"
    assert verdict("Wiersz ma przeszło tysiąc zdań.").result.ile < (
        verdict("Wiersz ma tysiąc zdań.").result.ile
    )


def test_cząstka_przy_liczebniku_nie_powtarza_lematu_cząstki_przy_zdaniu():
    #  Lemat postawiony na obu listach ma dwie drogi do jednej grupy — przez
    #  liczebnik i przez grupę imienną — więc `Kupuje niemal sto zdań.` wychodzi
    #  dwoma wyprowadzeniami jednego kształtu, a zdanie to jest wieloznaczne i bez
    #  nich, więc po statusie tego nie widać.
    assert not CZĄSTKI & CZĄSTKI_PRZY_LICZEBNIKU


def test_pięć_nie_jest_dopełniaczem_rzeczownika_odczasownikowego():
    #  Bez tego warunku `pięć` staje głową grupy imiennej w dopełniaczu mnogim,
    #  czyli dokładnie tam, gdzie ciało rządzące żąda dopełniacza, i każda liczba
    #  zakończona na pięć wychodzi dwoma czytaniami. Drugie zdanie jest ceną, którą
    #  ten warunek płaci, i stoi tu dlatego, że płaci ją rozmyślnie.
    assert verdict("Dwadzieścia pięć chlebów leży.").status == "valid"
    assert verdict("Pięcie jest trudne.").status == "rejected"


def test_cyfra_nie_jest_liczebnikiem_bo_nie_niesie_ani_przypadka_ani_liczby():
    #  Rejestr, o który olskiemu chodzi, pisze liczebnik cyfrą, a Morfeusz daje jej
    #  tag `dig` bez ani jednej cechy, więc oba ciała biorą ją naraz i `14 dni`
    #  wychodzi dwoma wyprowadzeniami o jednym streszczeniu. Odmowa jest przez to
    #  rozstrzygnięciem, a nie przeoczeniem, i docs/subset.md trzyma jej cenę.
    werdykt = verdict("Termin wynosi 14 dni.")
    assert werdykt.status == "rejected"
    assert werdykt.nielicencjonowane == ("14",)


def test_rzeczownik_odczasownikowy_stoi_w_każdej_pozycji_rzeczownika():
    #  Usterka, którą to łapie: pozycja dopisana rzeczownikowi i nie dopisana tej
    #  głowie. Ciała wypisuje jedna pętla, więc rozejście się dwóch kompletów nie
    #  daje ani jednego zdania odrzuconego, dopóki nikt nie zapyta o pozycję
    #  osobno, a zdania niżej są tymi pytaniami: głowa sama, z przymiotnikiem, z
    #  dopełniaczem i z wyrażeniem przyimkowym po sobie.
    #
    #  Ostatnie z nich wychodzi wieloznaczne i wychodzi tak słusznie: wyrażenie
    #  przyimkowe przyłącza się i do tej głowy, i do zdania, a olski między tymi
    #  dwoma czytaniami nie wybiera. Przyłączenie do głowy jest tu tym, o co pyta
    #  ten test, i widać je po tym, że czytania są dwa, a nie jedno.
    assert verdict("Przyłączenie jest tanie.").status == "valid"
    assert verdict("Nowe przyłączenie jest tanie.").status == "valid"
    assert verdict("Przyłączenie wyrażenia jest tanie.").status == "valid"
    przyimkowe = verdict("Przyłączenie do czasownika jest tanie.")
    assert przyimkowe.status == "ambiguous", przyimkowe.explain()
    [przyłączenie] = przyimkowe.result.przyłączenia
    assert przyłączenie.gospodarze == ("Przyłączenie", "jest"), przyimkowe.explain()


def test_rzeczownik_odczasownikowy_żąda_dopełniacza_a_nie_biernika():
    #  Ta głowa jest głową grupy imiennej, a nie pozycją przy czasowniku, i tyle
    #  właśnie znaczy: dopełnienia żąda w dopełniaczu, tak jak żąda go rzeczownik
    #  z dopełniaczem pod sobą. Bez tego warunku `przyłączenie wyrażenie`
    #  wyprowadza się jako grupa, której polszczyzna nie ma.
    assert verdict("Wyznaczenie granicy jest tanie.").status == "valid"
    assert verdict("Wyznaczenie granica jest tanie.").status == "rejected"


def test_dwa_czytania_tej_samej_głowy_są_jednym_czytaniem():
    #  Na tym stoi zerowa cena tej głowy: `czytanie` jest u Morfeusza i
    #  rzeczownikiem, i formą odczasownikową `czytać`, a ciała są dwa, więc zdanie
    #  ma dwa wyprowadzenia. Kształt mają jeden, a część mowy jest z tożsamości
    #  czytania wyłączona (`Node.signature` w `olski/parse/czytanie.py`), więc wpadają do
    #  jednej klasy i zdanie zostaje jednoznaczne.
    werdykt = verdict("Czytanie jest tanie.")
    assert werdykt.status == "valid", werdykt.explain()


def test_streszczenie_nie_wstawia_odstępu_przed_przecinkiem():
    #  Przecinek jest segmentem jak każde inne słowo, więc sklejenie form przez sam
    #  odstęp dawało `ustawienia , dane i pliki`, czyli napis, którego w tym zdaniu
    #  nikt nie napisał. Usterka jest widoczna w każdym zdaniu z koordynacją
    #  przecinkiem i w żadnym innym.
    roles = role(verdict("Program zapisuje ustawienia, dane i pliki."))[0]
    assert roles["dopełnienie"] == "ustawienia, dane i pliki"


def test_dwa_czytania_różne_granicą_członu_nie_wychodzą_jednym_napisem():
    #  Usterka, którą to łapie: streszczenie sklejone z samych form. Dwa z tych
    #  trzech czytań mają w każdej roli te same formy i różnią się granicą członu
    #  wewnątrz dopełnienia, więc bez nawiasu dawały znak w znak ten sam wiersz,
    #  co po werdykcie czyta się jak usterka narzędzia, a nie jak dwa czytania.
    #  Ciąg wpuszcza tu `sera` dlatego, że forma jest i dopełniaczem od `ser`,
    #  i biernikiem mnogim od `serum`, a biernika żąda pozycja dopełnienia.
    found = verdict("Koszt szynki i sera przewyższa koszt chleba.")
    streszczenia = [tuple(sorted(reading.items())) for reading in role(found)]
    assert len(set(streszczenia)) == len(streszczenia), found.explain()
    assert "[Koszt szynki] i sera" in {reading["dopełnienie"] for reading in role(found)}


def test_wykluczenie_leksykalne_mówi_o_czytaniu_a_nie_o_formie():
    #  Warunki ujemne są dwa i różni je zasięg, a nad Składnicą nie różni ich ani
    #  jedno zdanie (docs/konstrukcje-gramatyczne/grupa-imienna.md#zaimek-rzeczowny-nie-rządzi-dopełniaczem), więc
    #  jeden podstawiony za drugi nie wywraca ani suity, ani przebiegu nad korpusem.
    #  Pilnuje ich zatem to jedno miejsce. `nie` jest u Morfeusza cząstką `nie`
    #  i formą `on`: wykluczenie o czytaniu zostawia to drugie czytanie, a o formie
    #  zabiera oba, czyli zabiera czytanie, o którym nic nie mówi.
    [segment] = analyse("nie")
    zaimek = next(reading for reading in segment.readings if reading.lemma == "on")
    pytanie = (zaimek.tag.pos, zaimek.lemma, segment.lematy, zaimek.tag.cechy, EMPTY)
    o_czytaniu = word(zaimek.tag.pos, bez_lematu="nie")
    o_formie = word(zaimek.tag.pos, bez_lematu_formy="nie")
    assert bierze(o_czytaniu, *pytanie) is not None
    assert bierze(o_formie, *pytanie) is None


def test_zaimek_rzeczowny_nie_bierze_dopełniacza():
    #  tego jest dopełniaczem ten przy podzbioru i dopełniaczem to obok niego,
    #  czyli raz przymiotnikiem przy rzeczowniku, a raz zaimkiem rządzącym
    #  rzeczownikiem, więc bez warunku ujemnego zdanie wychodzi dwoma drzewami o
    #  różnym kształcie i o identycznym streszczeniu ról.
    found = verdict("Celem jest parser tego podzbioru.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["podmiot"] == "parser tego podzbioru"


def test_zaimek_bez_czytania_przymiotnikowego_też_nie_bierze_dopełniacza():
    #  Lista zawężona do paradygmatu ten zostawia to zdanie wieloznacznym: nikt ma
    #  u Morfeusza czytanie jedno i rzeczownikowe, więc czytania, w którym nikt nas
    #  jest grupą imienną, nie zdejmuje ani anotator, ani wykluczenie ze słownika.
    found = verdict("Wtedy nikt nas nie zauważy.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["podmiot"] == "nikt"


def test_zaimek_rzeczowny_nie_unosi_wysuniętego_zaimka_względnego():
    #  Drugie miejsce, w którym przydawką dopełniaczową jest zaimek: grupa
    #  wysuwana przed zdanie względne. Warunek postawiony w samej grupie imiennej
    #  zostawia to zdanie wieloznacznym, bo której nikt wychodzi taką grupą.
    found = verdict("Polszczyzna, której nikt nie napisał, jest podzbiorem.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["podmiot"] == "Polszczyzna, której nikt nie napisał,"


def test_rzeczownik_dalej_bierze_dopełniacz_po_sobie():
    #  Druga połowa warunku: wyłączona jest lista lematów, a nie produkcja, więc
    #  grupa imienna z dopełniaczem po głowie stoi tam, gdzie stała.
    found = verdict("Wejściem jest opis podzbioru.")
    assert found.status == "valid", found.explain()
    assert role(found)[0]["podmiot"] == "opis podzbioru"


def test_zaimek_rzeczowny_zostaje_wszędzie_indziej():
    #  Warunek stoi na jednej pozycji jednej produkcji, więc zaimek rzeczowny
    #  dalej jest tym, czym w polszczyźnie jest.
    assert verdict("To ma pomagać pisać dobrą polszczyznę.").status == "valid"


def test_zaimek_dzierżawczy_nie_zgadza_się_z_rzeczownikiem_przy_którym_stoi():
    #  Usterka, przed którą to stoi: zgodność wypuszczona zmienną wspólną, tak jak
    #  wypuszcza ją przymiotnik i liczebnik zgodny obok. Wygląda to poprawnie i
    #  odbiera polszczyźnie prawie każdą taką parę, bo zaimek zgadza się ze swoim
    #  poprzednikiem, który stoi w zdaniu obok. Para zdań łapie obie liczby.
    mnogi = verdict("Jego skutki są znane.")
    assert mnogi.status == "valid", mnogi.explain()
    assert role(mnogi)[0]["podmiot"] == "Jego skutki"
    assert verdict("Ich cena jest niska.").status == "valid"


def test_zaimek_dzierżawczy_bierze_formę_akcentowaną_i_nieprzyimkową():
    #  Enklityka stoi przy czasowniku, a forma przyimkowa po przyimku, więc bez tych
    #  dwóch warunków pozycja bierze `go` oraz `niego`, a zdanie z nimi wychodzi
    #  jednym czytaniem, czyli twierdzeniem. Warunek zbyt szeroki kosztuje z drugiej
    #  strony, dlatego pierwszy ma obok zdanie, które ma przejść.
    #
    #  Warunku drugiego nie sprawdza zdanie bez przyimka: formę przyimkową zdejmuje
    #  tam już morfologia (`po_przyimku`), więc `Znam niego cenę.` byłoby odrzucone
    #  i bez tego warunku. Sprawdza go grupa pod przyimkiem, gdzie ta forma czytanie
    #  zachowuje i gdzie ten warunek jest jedyną rzeczą, która ją odrzuca.
    assert verdict("Znam jego cenę.").status == "valid"
    assert verdict("Znam go cenę.").status == "rejected"
    assert verdict("Cena bez niego zapisu rośnie.").status == "rejected"


# --------------------------------------------------------------------------- #
# Przydawka imiesłowowa
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "zdanie",
    [
        #  Imiesłów bierny w obu szykach przydawki, tych samych, które ma przymiotnik.
        "Wymienione zadania są obowiązkowe.",
        "Zadania wymienione są obowiązkowe.",
        #  Imiesłów czynny wraz z dopełniaczem, którego żąda jego czasownik: ciało z
        #  przydawką i dopełniaczem stało w gramatyce przed nim i bierze go za darmo.
        "Reguła sięgająca znaku jest tania.",
    ],
)
def test_przydawka_imiesłowowa_stoi_tam_gdzie_przymiotnik(zdanie):
    found = verdict(zdanie)
    assert found.readings, found.explain()


def test_imiesłów_czynny_nie_dochodzi_do_orzecznika():
    #  Orzecznik bierze `ppas` i nie bierze `pact`, bo `Reguła jest sięgająca.` nie
    #  jest zdaniem tego rejestru. Usterka, którą to łapie: imiesłów wpuszczony
    #  jednym terminalem do obu symboli przymiotnikowych naraz.
    found = verdict("Reguła jest sięgająca.")
    assert found.status == "rejected", found.explain()


def test_ciąg_przyimkowy_o_trzech_członach_wyprowadza_się_raz():
    #  Usterka, którą to łapie: ciało `X → X spójnik X` zamiast członu i ciągu
    #  nad nim. Trzem członom daje ono dwa wyprowadzenia — `A i (B i C)` oraz
    #  `(A i B) i C` — a napis jest jeden i znaczy jedno.
    werdykt = verdict("Cena stoi w prozie i w kodzie i w pliku.")
    assert werdykt.status == "valid", werdykt.explain()


def test_ogon_ciągu_przyimkowego_nie_jest_osobnym_wyborem_przyłączenia():
    #  Usterka, którą to łapie: ciąg wpisany pod nazwą roli, czyli bez symbolu
    #  między nimi. Ogon jest wtedy drugim wyrażeniem przyimkowym w czytaniu,
    #  więc werdykt nazywa jego gospodarza obok gospodarza całego ciągu, a lista
    #  czytań pod spodem tego wyboru nie ma.
    werdykt = verdict("Program zapisuje ustawienia w pliku i w katalogu.")
    assert werdykt.status == "ambiguous", werdykt.explain()
    [przyłączenie] = werdykt.result.przyłączenia
    assert przyłączenie.modyfikator == "w pliku i w katalogu", werdykt.explain()


def test_człony_ciągu_przyimkowego_stoją_pod_różnymi_przyimkami():
    #  Usterka, którą to łapie: przypadek wypuszczony przez ciąg albo przez człon.
    #  Rządzi nim przyimek stojący w każdym członie z osobna, więc żądanie
    #  postawione nad ciągiem odbiera każdy ciąg o dwóch różnych przyimkach.
    werdykt = verdict("Program szyje ubrania w Belgii i na Malcie.")
    assert werdykt.readings, werdykt.explain()
