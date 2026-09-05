"""Czym forma stoi w odczytaniu, kiedy autor tego odczytania nie poznaje.

Wykaz morfologii ma jedno zadanie: pokazać odczytanie formy, z którego bierze
się odczytanie zdania niewidoczne w streszczeniu
(``Verdict.morfologia`` w ``olski/werdykt/zdanie.py``).
Testy stoją więc na zdaniach, które o to zadanie pytają, a nie na kształcie
wydruku: wiersze wklejone do dokumentów pilnuje ``tests/test_wydruki.py``.
"""

import pytest

pytest.importorskip("morfeusz2")

from olski.werdykt import check


def werdykt(zdanie: str):
    znalezione = check(zdanie)
    assert len(znalezione) == 1, f"zdań jest {len(znalezione)}, a nie jedno"
    return znalezione[0]


def wiersz(tabela, forma: str) -> tuple[str, ...]:
    """Odczytania tej formy w tym wpisie wykazu."""
    znalezione = [w for w in tabela if w.forma == forma]
    assert len(znalezione) == 1, f"form „{forma}” jest {len(znalezione)}, a nie jedna"
    return znalezione[0].odczytania


def test_odczytanie_z_dopełnieniem_zostawia_formie_samo_odczytanie_biernikowe():
    """Zdanie, o które to pytanie poszło: skąd bierze się `Janek` w dopełnieniu.

    Słownik zna `Janek` także jako rzeczownik żeński nieodmienny, więc forma stoi
    w każdym przypadku naraz i zdanie dostaje odczytanie z dopełnieniem `Janek`.
    Streszczenie nazywa tam rolę i formę, a nie odczytanie formy, więc bez tego
    wykazu autor nie ma czym tego odczytania sprawdzić
    (docs/pisanie-po-olsku.md#skąd-bierze-się-odczytanie-którego-autor-nie-widzi).
    """
    znalezione = werdykt("Janek lubi piwo.")
    podmiotem, dopełnieniem = znalezione.readings
    assert (podmiotem[0]["podmiot"], dopełnieniem[0]["dopełnienie"]) == ("Janek", "Janek")
    wykaz = znalezione.morfologia
    assert wiersz(wykaz[1], "Janek") == ("Janek subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:f",)
    #  W podmiocie stoją oba mianowniki, bo podmiot bierze każdy z nich, i to
    #  jest przesłanka testu: wykaz odsiewa odczytania, a nie wypisuje jednego.
    assert wiersz(wykaz[0], "Janek") == (
        "Janek subst:sg.pl:nom.gen.dat.acc.inst.loc.voc:f",
        "Janek subst:sg:nom:m1",
    )


def test_forma_pod_orzeczeniem_nie_niesie_odczytań_rzeczownikowych():
    """Odczytanie, którego to odczytanie zdania nie bierze, jest w wykazie usterką.

    `lubi` jest u Morfeusza także rzeczownikiem i przymiotnikiem `luby`, a pod
    orzeczeniem żadne z tych dwóch nie stoi; wypisane mówiłoby autorowi, że
    zdanie czyta się tam sposobem, którego gramatyka mu nie daje.
    """
    [tabela] = werdykt("Chłopiec lubi piwo.").morfologia
    assert wiersz(tabela, "lubi") == ("lubić fin:sg:ter:imperf",)


def test_wykaz_zbiera_odczytania_ze_wszystkich_ciał_jednego_kształtu():
    """Kształt wychodzący z dwóch ciał niesie odczytania obu, a nie ciała wybranego.

    `polecenie` jest u Morfeusza rzeczownikiem i odsłownikiem dwóch czasowników,
    a grupę imienną z jednej formy robi w tej gramatyce osobne ciało dla każdej z
    tych części mowy. Bez sumy po ciałach wykaz pokazuje stąd sam odsłownik
    `polecieć`, czyli czasownik, którego w tym zdaniu nie ma, a rzeczownik
    przemilcza (`Las._wsparte_kształtu` w olski/parse/las.py). Klasa nie jest rzadka:
    stoi w niej słownictwo, którym ten rejestr mówi o sobie samym
    (docs/subset.md#co-się-liczy-jako-jedno-odczytanie).
    """
    [tabela] = werdykt("Znam to polecenie.").morfologia
    assert wiersz(tabela, "polecenie") == (
        "polecieć ger:sg:nom.acc:n:perf:aff",
        "polecić ger:sg:nom.acc:n:perf:aff",
        "polecenie subst:sg:nom.acc.voc:n:ncol",
    )


def test_forma_czytana_jednym_sposobem_nie_dostaje_wiersza():
    """Wiersz o niej powtarzałby zdanie, w którym ta forma i tak stoi."""
    [tabela] = werdykt("Zapisz plik konfiguracyjny.").morfologia
    assert [w.forma for w in tabela] == ["plik", "konfiguracyjny"]


def test_zdanie_bez_odczytania_dostaje_odczytania_każdej_formy():
    """Kształtu nie ma, więc nie ma czym odsiewać, a autor pyta o formy tak samo.

    Wpis jest jeden, bo odczytania zdania nie ma ani jednego, i wypisuje też
    formę czytaną jednym sposobem: nad zdaniem odrzuconym wykaz jest tym, co
    weszło do rozbioru, a nie zawężeniem, którego to zdanie nie ma.
    """
    [tabela] = werdykt("Nowa program zapisuje ustawienia.").morfologia
    assert [w.forma for w in tabela] == ["Nowa", "program", "zapisuje", "ustawienia", "."]
    assert wiersz(tabela, "program") == ("program subst:sg:nom.acc:m3",)


def test_odczytanie_dwóch_leksemów_o_jednym_znaczniku_stoi_w_wierszu_raz():
    """Lemat traci przy analizie indeks homonimu (``analyse`` w ``olski/morph.py``).

    `Zamek` wychodzi z Morfeusza dwoma odczytaniami, które po tym odjęciu są
    jednym napisem, a wypisane oba czytają się jak pomyłka wydruku.
    Lemat `Zamek` zostaje w wierszu obok, bo różni się od `zamek` napisem,
    a nie samym indeksem.
    """
    tabela, _drugie = werdykt("Zamek stoi.").morfologia
    odczytania = wiersz(tabela, "Zamek")
    assert len(set(odczytania)) == len(odczytania)
    assert "zamek subst:sg:nom.acc:m3" in odczytania
