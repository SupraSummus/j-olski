"""Figura ma jednego właściciela: plik, który wypisuje przebieg.

Reguła i jej powód są w ``CLAUDE.md#checks``, a tutaj jest to, czym ona działa.
``FIGURY`` niżej deklaruje na każdy przebieg polecenie,
pliki, bez których nie ma on czego czytać,
pliki, których zmiana rusza liczby,
sekcje restytuujące figurę grubiej,
to, co po przeliczeniu zostaje ręką,
oraz to, kto ten przebieg jeszcze powtórzy.
Figura, której nie powtórzy nikt, przeliczenia nie żąda,
bo liczba pod nią jest pomiarem datowanym, a nie stanem bieżącym,
a jej sonda jest odtwarzalna commitem podanym obok.
Plik figury zapisuje odciski tych plików z chwili przebiegu,
więc pytanie o należność przeliczenia porównuje dwa napisy i po korpus nie sięga.

Stąd dwie komendy zamiast jednej: raport odpowiada wszędzie, bo nie pobiera niczego,
a przeliczenie wymaga korpusu albo prozy z niego wyjętej
i wykonuje je ktoś, kto to ma.

    python3 -m harness.figury            # co jest należne przeliczenia
    python3 -m harness.figury negacja    # przelicz i zapisz
    python3 -m harness.figury --należne  # przelicz wszystko, co jest należne
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

KORZEŃ = Path(__file__).resolve().parent.parent
KATALOG = KORZEŃ / "figury"

#: Odcisk pliku, którego przebieg nie widział, bo liczby przeniesiono do pliku
#: figury z dokumentu, zamiast wziąć je przebiegiem. Figura wzięta kiedyś przez
#: kogoś nie ma daty, po której dałoby się orzec, czy coś ją od tamtej pory
#: ruszyło, więc raport mówi o niej tyle właśnie, zamiast liczyć ją za zgodną.
NIEZNANY = "nieznany"

#: Pięć odpowiedzi raportu. Są nazwane, bo drukuje je jedna funkcja, a odróżnia
#: druga, i literał powtórzony w obu rozjechałby się przy pierwszej zmianie słowa.
AKTUALNA = "aktualna"
NALEŻNA = "należna"
NIEZMIERZONA = "niezmierzona tutaj"
BEZ_PLIKU = "bez pliku"
ZAMKNIĘTA = "zamknięta"

#: Wartość ``Figura.powtórzy``, która mówi, że przebiegu nie powtórzy nikt. Pusty
#: napis, a nie ``None``, bo ``None`` znaczy tutaj coś innego: nikt jeszcze nie
#: orzekł, a orzeczenie i jego brak są dwoma różnymi stanami deklaracji.
NIKT = ""

#: Ile znaków odcisku zapisywać. Odcisk odpowiada na jedno pytanie — czy plik jest
#: ten sam — a nie na pytanie o podstawienie, więc reszta sześćdziesięciu czterech
#: znaków kosztowałaby czytelność nagłówka i nic nie kupiła.
ZNAKÓW = 12


@dataclass(frozen=True)
class Figura:
    """Jeden przebieg, jeden plik i lista tego, co ten plik rusza.

    Jednostką jest przebieg, a nie tabela w dokumencie: ta sama sonda pod złotą
    i pod żywą morfologią ma osobne wydruki, więc jedna należy się przeliczenia
    wtedy, gdy druga nie.
    """

    #: Nazwa pliku w ``figury/``, bez rozszerzenia, i nazwa dla komendy.
    nazwa: str
    #: Polecenie, którego wydruk jest figurą, słowo po słowie. Jest tu, a nie w
    #: dokumencie, bo dokument je drukujący byłby drugą kopią tego samego.
    polecenie: tuple[str, ...]
    #: Pliki, których zmiana rusza liczby, wymienione tak, jak mówi o tej figurze
    #: sekcja ``Checks`` w ``CLAUDE.md``: z parserem obok gramatyki, bo kolejność
    #: prób rusza blokery, choć werdyktu nie rusza.
    ruszają: tuple[str, ...]
    #: Sekcje restytuujące figurę grubiej. Raport je wypisuje nad figurą należną
    #: przeliczenia, bo przeliczenie ruszające rząd wielkości jest winne tej prozy.
    czyta: tuple[str, ...]
    #: Ścieżki, bez których polecenie nie ma czego czytać; puste, kiedy przebieg
    #: czyta samo repozytorium. Rozstrzyga, czy przeliczenie wykonuje się tutaj,
    #: czy należy do kogoś, kto te pliki ma. Krotka, a nie jedna ścieżka, bo
    #: przebieg bywa porównaniem dwóch korpusów naraz i brak każdego z nich
    #: zatrzymuje go osobno. Proza wyjęta z Markdownu stoi tu na równi z korpusem
    #: pobranym, bo jednego i drugiego w drzewie nie ma; polecenie, które ją robi,
    #: drukuje dokument nazwany w ``czyta``.
    korpusy: tuple[str, ...] = ()

    #: Kody wyjścia, które są pomiarem, a nie usterką przebiegu. ``olski-check``
    #: odpowiada 1, kiedy nie każde zdanie jest olskim, co nad każdą prawdziwą prozą
    #: jest właśnie tym, co się mierzy, a 2, kiedy nie miał czego przeczytać. Kod 1
    #: zderza się przy tym z kodem, którym Python kończy na wyjątku, więc przebieg
    #: kończący się kodem niezerowym musi mieć puste wyjście błędu, żeby uszło za
    #: pomiar; inaczej figurą stałby się ślad stosu.
    kody: tuple[int, ...] = (0,)

    #: Co przeliczenie zostawia człowiekowi, bo poprawiona liczba tego nie zaspokaja:
    #: odczyt próbki czytanej ręką, blok wydruku wklejony do dokumentu, arytmetyka
    #: pod takim blokiem. Raport wypisuje to nad figurą nieaktualną, a przeliczenie
    #: wtedy, gdy wydruk wyszedł inny, bo tam pada pytanie, czego jeszcze zmiana
    #: jest winna. Puste, kiedy przeliczenie i poprawiona restytucja to wszystko.
    ręką: tuple[str, ...] = ()

    #: Kto ten przebieg jeszcze powtórzy, jednym zdaniem. Trzy stany: ``None``
    #: znaczy, że nikt nie orzekał, i wtedy figura zachowuje się tak jak przed
    #: dopisaniem tego pola; napis nazywa czytelnika; ``NIKT`` znaczy, że nie
    #: powtórzy jej nikt, więc przeliczenie nie jest winne, a sonda idzie do gita.
    #: Odpowiedź stoi tu, a nie w docstringu sondy, bo kryterium zapisane samą
    #: prozą nie ma gdzie jej zapisać i pada drugi raz przy każdej sesji.
    powtórzy: str | None = None

    #: Commit, w którym leży program, kiedy nie ma go już w drzewie: bez niego
    #: polecenie wskazuje moduł, którego nikt nie wykona, i liczba przestaje być
    #: odtwarzalna w chwili, gdy sonda wychodzi. Wymaga go ``tests/test_figury.py``.
    w_gicie: str = ""

    @property
    def zamknięta(self) -> bool:
        """Czy przebiegu nie powtórzy nikt, czyli czy przeliczenie nie jest już winne."""
        return self.powtórzy == NIKT

    @property
    def brakujące(self) -> list[str]:
        """Korpusy zadeklarowane, których w drzewie nie ma."""
        return [korpus for korpus in self.korpusy if not (KORZEŃ / korpus).exists()]

    @property
    def plik(self) -> Path:
        return KATALOG / f"{self.nazwa}.txt"


#: Figury, które właściciela już mają. Lista rośnie zmianą dotykającą figury przy
#: innej robocie, a nie przebiegiem porządkowym nad wszystkimi — tak jak
#: ``CLAUDE.md#reguły-przyjmujemy-leniwie`` każe przyjmować resztę reguł.
FIGURY = (
    Figura(
        nazwa="negacja",
        polecenie=("python3", "-m", "sonda.negacja", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#negacja-zmierzona-kupuje-przeszło-sto-zdań-i-nie-płaci-dopełniaczem",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="przysłówek",
        polecenie=("python3", "-m", "sonda.przysłówek", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Formalizm stoi tu obok gramatyki, czego nie robi żadna figura wyżej, i
        #  jest to zapis tego, co tę figurę ruszyło: żądanie obecności cechy jest
        #  warunkiem w `olski/grammar.py`, a bez niego pozycja przy przymiotniku
        #  bierze przysłówek pierwotny i odbiera zdania, których nie odbiera z nim.
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "olski/grammar.py",
            "sonda/przysłówek.py",
            "sonda/ruch.py",
        ),
        #  Sekcje są trzy, bo tę figurę restytuuje więcej niż jedna, a ``czyta``
        #  jest listą właśnie na to. Pierwsza jest właścicielem restytucji, a dwie
        #  dalsze niosą twierdzenie z niej wyprowadzone — porównanie rejestrów i
        #  przelicznik kolejki blokerów — więc przeliczenie ruszające liczbę może
        #  je odwrócić, choć wskazują na pierwszą, a nie na ten plik.
        czyta=(
            "docs/subset.md#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe",
            "docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze",
            "docs/roadmap.md#etap-6-reszta-konstrukcji",
        ),
    ),
    Figura(
        nazwa="płaski",
        polecenie=("python3", "-m", "sonda.płaski", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "olski/grammar.py",
            "sonda/przysłówek.py",
            "sonda/ruch.py",
            "sonda/płaski.py",
        ),
        czyta=("docs/subset.md#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę",),
    ),
    Figura(
        nazwa="płaski-okolicznik",
        #  Ta sama sonda nad tym samym korpusem, a osobno od figury wyżej, bo pyta
        #  o co innego: tamta mówi, ile fałszywych czytań zostaje w olskim, a ta,
        #  ile dawałby pierwszy gospodarz bez drugiego, czyli po jakiej cenie
        #  drugiego wpuszczono.
        polecenie=(
            "python3",
            "-m",
            "sonda.płaski",
            "Składnica-frazowa-180723/",
            "--wariant",
            "okolicznik",
        ),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "olski/grammar.py",
            "sonda/przysłówek.py",
            "sonda/ruch.py",
            "sonda/płaski.py",
        ),
        czyta=("docs/subset.md#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę",),
    ),
    Figura(
        nazwa="przecinek",
        polecenie=("python3", "-m", "sonda.przecinek", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="interpunkcja",
        polecenie=("python3", "-m", "sonda.interpunkcja", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Morfologia stoi tu wśród tego, co rusza liczby, czego nie robi żadna
        #  figura wyżej, i jest to zapis tego, co tę sondę w ogóle wpuściło:
        #  lemat dwukropka wychodził z ``olski/morph.py`` pusty, bo obcięcie
        #  indeksu homonimu brało go za indeks, więc terminal dwukropka nie brał
        #  ani jednego czytania i produkcja stała martwa.
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "olski/morph.py",
            "sonda/interpunkcja.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego",
            "docs/roadmap.md#etap-4-zdanie-złożone",
        ),
    ),
    Figura(
        nazwa="liczebnik",
        polecenie=("python3", "-m", "sonda.liczebnik", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#liczebnik-zmierzono-i-nie-odbiera-ani-jednego-zdania",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="szyk",
        polecenie=("python3", "-m", "sonda.szyk", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="okolicznikowe",
        polecenie=("python3", "-m", "sonda.okolicznikowe", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie",
        ),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="okolicznikowe-żywa",
        #  Ta sama sonda po morfologii żywej, bo cena tej konstrukcji jest pod
        #  złotą niewidoczna: konkuruje ona z czytaniem przysłówkowym spójnika,
        #  a anotator wybrał w banku drzew jedno czytanie na token.
        polecenie=(
            "python3",
            "-m",
            "sonda.okolicznikowe",
            "Składnica-frazowa-180723/",
            "--morfologia",
            "live",
        ),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie",
        ),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="czoło",
        polecenie=("python3", "-m", "sonda.czoło", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Gramatyki tu nie ma, tak samo jak przy figurze niżej: liczone są cudze
        #  zdania, a rusza je lista, o którą sonda pyta, i nic poza nią.
        ruszają=("olski/subset.py",),
        czyta=(
            "docs/subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania",
        ),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="rama",
        polecenie=(
            "python3",
            "-m",
            "sonda.rama",
            "Składnica-frazowa-180723/",
            "--czasowniki",
            "walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt",
            "--rzeczowniki",
            "walenty_20160418-text/nouns/walenty_20160418_nouns_all.txt",
        ),
        korpusy=("Składnica-frazowa-180723", "walenty_20160418-text"),
        #  Gramatyki tu nie ma i to ją odróżnia od figur wyżej: kryterium czyta
        #  Walentego wprost, a wzorzec bierze z cudzych drzew, więc rusza je sonda
        #  i to, co `olski/attachment.py` uznaje za pozycję sporną — a nie produkcja.
        #  `olski/walenty.py` stoi tu, bo kryterium ma tam jednego właściciela:
        #  sonda i kolumna leksykonu pytają jednym `przyimki`.
        ruszają=("sonda/rama.py", "olski/walenty.py", "olski/attachment.py"),
        czyta=("docs/disambiguation.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie",),
    ),
    Figura(
        nazwa="znaczenia",
        polecenie=("python3", "-m", "sonda.znaczenia", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Rusza to i gramatyka, i zapis dziedziny, bo pomiar jest różnicą między
        #  nimi: produkcja dopisana rusza czytania, a kategoria dopisana w składni
        #  albo w rozbiorze rusza to, ile z nich wraca.
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "olski/skład/rozbiór.py",
            "olski/skład/składnia.py",
            "sonda/znaczenia.py",
        ),
        czyta=("docs/architecture.md#werdykt-liczy-wyprowadzenia-bo-powstaje-pod-dwiema-warstwami-które-liczą-znaczenia",),
    ),
    Figura(
        nazwa="znaczenia-live",
        #  Ta sama sonda nad tym samym korpusem, a osobno od figury wyżej, bo
        #  morfologia żywa jest tą, którą czyta się dokument, i daje pytaniu
        #  populację kilka razy większą niż czytania wybrane przez anotatorów.
        polecenie=(
            "python3",
            "-m",
            "sonda.znaczenia",
            "Składnica-frazowa-180723/",
            "--morfologia",
            "live",
        ),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "olski/skład/rozbiór.py",
            "olski/skład/składnia.py",
            "sonda/znaczenia.py",
        ),
        czyta=("docs/architecture.md#werdykt-liczy-wyprowadzenia-bo-powstaje-pod-dwiema-warstwami-które-liczą-znaczenia",),
    ),
    Figura(
        nazwa="pytanie",
        polecenie=("python3", "-m", "sonda.pytanie", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="pytanie-żywa",
        #  Ta sama sonda po morfologii żywej. Cena wyszła pod złotą zerowa, a zero
        #  wzięte pod morfologią, w której anotator wybrał jedno czytanie na token,
        #  nie mówi o cenie nad tekstem, który olski dostaje do sprawdzenia.
        polecenie=(
            "python3",
            "-m",
            "sonda.pytanie",
            "Składnica-frazowa-180723/",
            "--morfologia",
            "live",
        ),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="wysunięcie",
        polecenie=("python3", "-m", "sonda.wysunięcie", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/wysunięcie.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania",),
    ),
    Figura(
        nazwa="wysunięcie-żywa",
        #  Ta sama sonda po morfologii żywej, i tu jedyny zakup banku drzew stoi.
        #  Pod złotą nie rusza się nad tym korpusem nic, więc kolumna złota mówiłaby
        #  sama o konstrukcji, która nad bankiem drzew nie kupuje niczego.
        polecenie=(
            "python3",
            "-m",
            "sonda.wysunięcie",
            "Składnica-frazowa-180723/",
            "--morfologia",
            "live",
        ),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/wysunięcie.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania",),
    ),
    Figura(
        nazwa="wysunięcie-ustawy",
        polecenie=("python3", "-m", "sonda.wysunięcie", "proza/ustawy.txt"),
        korpusy=("proza/ustawy.txt",),
        ruszają=(
            "harness/ustawy.py",
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/wysunięcie.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania",),
    ),
    Figura(
        nazwa="wysunięcie-ztp",
        #  „Zasady techniki prawodawczej” stoją osobno od siedmiu ustaw, bo są
        #  rozporządzeniem, i to one dają tej konstrukcji zdanie, na którym stanęła:
        #  `ustawy, na podstawie której jest ono wydawane` jest ich przepisem.
        polecenie=("python3", "-m", "sonda.wysunięcie", "proza/ztp.txt"),
        korpusy=("proza/ztp.txt",),
        ruszają=(
            "harness/ustawy.py",
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/wysunięcie.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#grupę-wysuniętą-zmierzono-nie-kosztuje-nic-i-kupuje-pojedyncze-zdania",),
    ),
    Figura(
        nazwa="kopuła",
        polecenie=("python3", "-m", "sonda.kopuła", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#kopułę-opuszczoną-zmierzono-nie-kosztuje-nic-i-kupuje-mniej-niż-obiecywała-jej-częstość",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="kopuła-żywa",
        #  Ta sama sonda po morfologii żywej. Kolumna złota mówi tu zero i zero,
        #  a bank drzew nie ma tego zwrotu ani razu, więc żywa jest tym, co
        #  pokazuje, że zero po stronie ceny nie jest zerem anotatora.
        polecenie=(
            "python3",
            "-m",
            "sonda.kopuła",
            "Składnica-frazowa-180723/",
            "--morfologia",
            "live",
        ),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#kopułę-opuszczoną-zmierzono-nie-kosztuje-nic-i-kupuje-mniej-niż-obiecywała-jej-częstość",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="kopuła-ustawy",
        #  Siedem ustaw jest jedynym korpusem, w którym ta konstrukcja cokolwiek
        #  kupuje, bo jedynym, który tym zwrotem odsyła.
        polecenie=("python3", "-m", "sonda.kopuła", "proza/ustawy.txt"),
        korpusy=("proza/ustawy.txt",),
        ruszają=(
            "harness/ustawy.py",
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#kopułę-opuszczoną-zmierzono-nie-kosztuje-nic-i-kupuje-mniej-niż-obiecywała-jej-częstość",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="kopuła-ztp",
        polecenie=("python3", "-m", "sonda.kopuła", "proza/ztp.txt"),
        korpusy=("proza/ztp.txt",),
        ruszają=(
            "harness/ustawy.py",
            "olski/subset.py",
            "olski/precedencja.py",
            "olski/parse.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#kopułę-opuszczoną-zmierzono-nie-kosztuje-nic-i-kupuje-mniej-niż-obiecywała-jej-częstość",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="pytajne",
        polecenie=("python3", "-m", "sonda.pytajne", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Gramatyka rusza tu jedną kolumnę, a nie liczby: sonda pyta ją o lematy,
        #  które grupa pytajna bierze, a pytania w banku drzew liczy bez niej.
        ruszają=("olski/subset.py",),
        czyta=("docs/subset.md#pytanie-zmierzono-nie-odbiera-żadnego-zdania-i-oddaje-to-które-warunek-zabrał",),
        powtórzy=NIKT,
        w_gicie="474437f",
    ),
    Figura(
        nazwa="korpus",
        polecenie=("olski-corpus", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Lista jest tu najszersza w tej deklaracji, bo jeden przebieg przechodzi
        #  cały aparat: segmentacja, leksykon czytany przy imporcie i czytnik banku
        #  drzew ruszają werdykty tak samo jak produkcja. `signature` w
        #  `olski/parse.py` nie ma ani jednej produkcji i rusza każdy z nich, a
        #  `PORÓWNYWANE_ROLE` w `olski/coverage.py` rusza samą zgodność z bankiem.
        #  Kolejkę blokerów rusza przy tym przepisanie `olski/parse.py`, które nie
        #  rusza ani jednego werdyktu: gdzie stanęło zdanie odrzucone, jest faktem
        #  o tym, które produkcje próbowano, a nie o tym, które się udały, więc dwie
        #  gramatyki przyjmujące te same zdania układają blokery inaczej.
        #  Tam też stoi `ciała`, czyli kolejność, w jakiej las wydaje czytania:
        #  numer złotego czytania jest nią i niczym więcej, więc przepisanie jej
        #  rusza tę jedną tabelę, zostawiając każdy werdykt i każde ocalenie.
        ruszają=(
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/corpus.py",
            "olski/coverage.py",
            "olski/leksykon.txt",
        ),
        czyta=(
            "docs/corpus.md#the-measurement",
            "docs/corpus.md#where-the-analyses-stop",
            "docs/corpus.md#agreement-which-matters-more-than-acceptance",
            "docs/corpus.md#złote-czytanie-ocalało-w-niemal-każdym-zdaniu-wieloznacznym",
        ),
    ),
    Figura(
        nazwa="korpus-żywa",
        #  Ta sama komenda po morfologii żywej, osobno od figury wyżej, bo cena
        #  wieloznaczności morfologicznej jest pod złotą niewidoczna.
        polecenie=("olski-corpus", "Składnica-frazowa-180723/", "--morphology", "live"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/corpus.py",
            "olski/coverage.py",
            "olski/leksykon.txt",
        ),
        czyta=("docs/corpus.md#what-morphological-ambiguity-costs",),
    ),
    Figura(
        nazwa="readme",
        polecenie=("python3", "-m", "olski.check", "proza/README.txt"),
        #  Korpusem jest własna proza wyjęta z README, więc rusza figurę i kod, i
        #  samo README: akapit dopisany o nowej konstrukcji rusza tę liczbę tak
        #  samo jak produkcja. Ekstrakcję drukuje sekcja z `czyta`.
        korpusy=("proza/README.txt",),
        kody=(0, 1),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/check.py",
            "olski/document.py",
            "olski/leksykon.txt",
            #  Leksykon projektu rusza tę figurę, bo README pisze słowa, które on
            #  nazywa; nad korpusem, który żadnego z nich nie pisze, nie ruszy nic.
            "olski/projekt.py",
            "olski/projekt.txt",
        ),
        czyta=("docs/corpus.md#where-the-analyses-stop",),
        ręką=(
            "odczyt klas pod przebiegiem: czym różnią się czytania zdań wieloznacznych",
        ),
    ),
    Figura(
        nazwa="readme-czytania",
        #  Przebieg bez korpusu, bo zdania stoją w samym poleceniu: jest to blok
        #  wklejony do README, a nie pomiar nad tekstem.
        polecenie=(
            "python3",
            "-m",
            "olski.check",
            "--readings",
            "-c",
            "Zapisz plik konfiguracyjny.\n"
            "Koszt samej szynki przewyższa koszt szynki z dodatkami.\n"
            "Nowa program zapisuje ustawienia.",
        ),
        kody=(0, 1),
        ruszają=(
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/check.py",
            "olski/leksykon.txt",
        ),
        czyta=("README.md#co-działa",),
        ręką=("blok wydruku w README przepisać, wraz z arytmetyką pod nim",),
    ),
    Figura(
        nazwa="czytania",
        polecenie=("python3", "-m", "sonda.czytania", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Klasy bierze sonda, a nazywają je `różniące`, `przyłączenia` i
        #  `rozbieżności` w `olski/parse.py` oraz `gospodarze` w `DEKLARACJA`:
        #  gospodarz dopisany jest wyborem dopisanym, choć werdykt stoi.
        ruszają=(
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/coverage.py",
            "olski/corpus.py",
            "olski/leksykon.txt",
            "sonda/czytania.py",
        ),
        czyta=("docs/disambiguation.md#czym-różnią-się-czytania-które-olski-odrzuca",),
    ),
    Figura(
        nazwa="powtórzenie",
        polecenie=("python3", "-m", "sonda.powtórzenie", "proza/"),
        korpusy=("proza/ksef", "proza/rit"),
        #  Gramatyki tu nie ma: pozycje wyznacza `pytania` w
        #  `olski/wieloznaczność.py`, a nie werdykt, więc produkcja nie rusza ani
        #  jednej liczby tego przebiegu. Ekstrakcja rusza za to obie: udział zdań
        #  pierwszych w akapicie jest faktem o tym, co `harness/markdown.py`
        #  liczy za akapit.
        ruszają=(
            "harness/markdown.py",
            "olski/document.py",
            "olski/morph.py",
            "olski/wieloznaczność.py",
            "olski/rozstrzyganie.py",
            "sonda/powtórzenie.py",
        ),
        czyta=("docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek",),
        ręką=(
            "odczyt odpowiedzi świadka, bo pod figurą stoi odczyt, a nie stopa",
            "porównanie reguł, gdy przebieg rusza to, którą z nich wariant wycenia",
        ),
    ),
    Figura(
        nazwa="rozstrzyganie-proza",
        polecenie=(
            "sh",
            "-c",
            "python3 -m olski.check --rozstrzygaj proza/ksef/*.txt proza/rit/*.txt",
        ),
        #  Powłoka jest tu dlatego, że `olski-check` bierze pliki, a nie katalog,
        #  i tak samo drukuje to polecenie dokument z `czyta`.
        korpusy=("proza/ksef", "proza/rit"),
        kody=(0, 1),
        ruszają=(
            "harness/markdown.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/check.py",
            "olski/rozstrzyganie.py",
            "olski/skłonności.txt",
            "olski/leksykon.txt",
        ),
        czyta=("docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek",),
    ),
    Figura(
        nazwa="skłonności-ocena",
        polecenie=("python3", "-m", "olski.rozstrzyganie", "Składnica-frazowa-180723/", "--oceń"),
        korpusy=("Składnica-frazowa-180723",),
        #  Ocena buduje tabelę z połowy banku drzew i sprawdza ją na drugiej, więc
        #  `olski/skłonności.txt` jej nie rusza: ten plik powstaje z całości i jest
        #  tym, czego ta tabela nie mierzy. Leksykon rusza ją za to cały, bo
        #  świadek ramowy czyta z niego kolumnę przyimków.
        ruszają=(
            "olski/rozstrzyganie.py",
            "olski/attachment.py",
            "olski/corpus.py",
            "olski/leksykon.txt",
        ),
        czyta=(
            "docs/disambiguation.md#zalążek-stoi-obok-werdyktu-i-nazywa-swoją-częstość-pomyłek",
            "docs/disambiguation.md#rama-rozstrzyga-po-stronie-rzeczownika-a-po-stronie-czasownika-nie",
        ),
    ),
    Figura(
        nazwa="wskazania",
        polecenie=("python3", "-m", "sonda.wskazania", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Rusza to wszystko, co rusza werdykt, i cała warstwa nad nim, bo pomiar
        #  jest wskazaniem ocenianym wzorcem: wzorcem jest to, co
        #  `olski/attachment.py` czyta ze złotego drzewa.
        ruszają=(
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/corpus.py",
            "olski/coverage.py",
            "olski/attachment.py",
            "olski/rozstrzyganie.py",
            "olski/skłonności.txt",
            "olski/leksykon.txt",
            "sonda/wskazania.py",
        ),
        czyta=("docs/disambiguation.md#werdykt-pyta-warstwę-o-inny-wybór-niż-bank-drzew",),
    ),
    Figura(
        nazwa="wybory",
        polecenie=("python3", "-m", "sonda.wybory", "próba/wybory.txt"),
        #  Korpusu nie ma, bo wzorzec jest w repozytorium: wpisy są pisane ręką i
        #  stoją, więc rusza tę figurę sama warstwa. Gramatyka jej nie rusza,
        #  bo pozycje bierze `pytania` w `olski/wieloznaczność.py`, a nie werdykt.
        ruszają=(
            "próba/wybory.txt",
            "olski/wieloznaczność.py",
            "olski/rozstrzyganie.py",
            "olski/skłonności.txt",
            "olski/próbka.py",
            "sonda/wybory.py",
        ),
        czyta=("docs/disambiguation.md#wzorzec-dla-rejestru-czyta-się-ręką-i-jest-go-trzydzieści-wyborów",),
        ręką=("przebudowa próby jest osobnym aktem i winna jest odczyt każdego wpisu",),
    ),
    Figura(
        nazwa="wybory-z-odpowiedzią",
        polecenie=("python3", "-m", "sonda.wybory", "próba/wybory-z-odpowiedzią.txt"),
        #  Ta sama sonda i ten sam brak korpusu, a osobno od figury wyżej, bo próba
        #  jest inna: wpisy są losowane z pozycji, o których warstwa się odzywa,
        #  więc zmiana w niej rusza to, które pozycje do tej próby należą.
        ruszają=(
            "próba/wybory-z-odpowiedzią.txt",
            "olski/wieloznaczność.py",
            "olski/rozstrzyganie.py",
            "olski/skłonności.txt",
            "olski/próbka.py",
            "sonda/wybory.py",
        ),
        czyta=(
            "docs/disambiguation.md#częstość-nad-dokumentacją-myli-się-tam-gdzie-nie-rozstrzyga-żadne-słowo-zdania",
        ),
        ręką=(
            "podział pomyłek jest odczytem pól `powód`, a nie liczbą z wydruku",
            "zmiana ruszająca odpowiedzi jest winna nowe losowanie i odczyt jego wpisów",
        ),
    ),
    Figura(
        nazwa="konwersy",
        polecenie=(
            "python3",
            "-m",
            "sonda.konwersy",
            "walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt",
        ),
        korpusy=("walenty_20160418-text",),
        #  Gramatyki tu nie ma: liczone są schematy Walentego, więc jedynym
        #  ruszającym jest kryterium sondy, a `olski/próbka.py` wybiera pary,
        #  które pod figurą czyta się ręką.
        ruszają=("sonda/konwersy.py", "olski/walenty.py", "olski/próbka.py"),
        czyta=("docs/disambiguation.md#rozstrzygnąć-da-się-tylko-to-co-las-trzyma",),
        ręką=("dwanaście par przeczytać na nowo, bo kryterium ruszone to kryterium bez odczytu",),
    ),
    Figura(
        nazwa="przyłączenie",
        polecenie=("python3", "-m", "olski.attachment", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Liczone są cudze drzewa, więc produkcja nie rusza tu niczego, a rusza
        #  to, co ten moduł liczy za zdanie i za grupę imienną.
        ruszają=("olski/attachment.py", "olski/corpus.py"),
        czyta=("docs/subset.md#bank-drzew-nie-zna-domyślnego-przyłączenia",),
    ),
    Figura(
        nazwa="ustawy",
        polecenie=("sh", "-c", "python3 -m olski.check proza/ustawy/*.txt"),
        #  Korpusem są akty złożone w zdania przez `harness/ustawy.py`, więc rusza
        #  tę figurę i to, co ten krok składa. Adres ELI, pod którym akt stoi, nie
        #  rusza się nigdy: akt zmienia inny akt, pod własnym adresem.
        korpusy=("proza/ustawy",),
        kody=(0, 1),
        ruszają=(
            "harness/ustawy.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/check.py",
            "olski/document.py",
            "olski/leksykon.txt",
        ),
        czyta=(
            "docs/ustawy.md#co-gramatyka-z-tego-wyprowadza",
            "docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze",
        ),
        ręką=(
            "tabele w prozie powstają grepami nad tym wydrukiem, nie są jego wierszami",
            "bloki wydruku wklejone do dokumentu przepisać, wraz z arytmetyką pod nimi",
        ),
    ),
    Figura(
        nazwa="przysłówek-ustawy",
        polecenie=("python3", "-m", "sonda.przysłówek", "proza/ustawy.txt"),
        #  Ta sama sonda co nad bankiem drzew, a nad rejestrem, o który chodzi:
        #  cena konstrukcji jest tu inna niż nad prozą literacką.
        korpusy=("proza/ustawy.txt",),
        ruszają=(
            "harness/ustawy.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/leksykon.txt",
            "sonda/przysłówek.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze",),
    ),
    Figura(
        nazwa="płaski-ustawy",
        polecenie=("python3", "-m", "sonda.płaski", "proza/ustawy.txt"),
        korpusy=("proza/ustawy.txt",),
        ruszają=(
            "harness/ustawy.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/leksykon.txt",
            "sonda/przysłówek.py",
            "sonda/płaski.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze",),
    ),
    Figura(
        nazwa="interpunkcja-ustawy",
        polecenie=("python3", "-m", "sonda.interpunkcja", "proza/ustawy.txt"),
        korpusy=("proza/ustawy.txt",),
        ruszają=(
            "harness/ustawy.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/leksykon.txt",
            "sonda/interpunkcja.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/ustawy.md#gdzie-stają-analizy-w-tym-rejestrze",),
    ),
    Figura(
        nazwa="wieloznaczność",
        polecenie=(
            "sh",
            "-c",
            "python3 -m olski.wieloznaczność proza/ksef/*.txt proza/rit/*.txt",
        ),
        korpusy=("proza/ksef", "proza/rit"),
        #  Figura mierzy rejestr, a nie gramatykę, ale między tekstem a liczbą stoi
        #  to, co `admissible` w `olski/subset.py` zostawia z czytań morfologii,
        #  i leksykon pod nim. Stoi ona pod pytaniem otwartym, a nie pod regułą,
        #  więc przeliczenie, które ją rusza, rusza to, o co tamto pytanie pyta.
        ruszają=(
            "harness/markdown.py",
            "olski/wieloznaczność.py",
            "olski/subset.py",
            "olski/morph.py",
            "olski/walencja.py",
            "olski/leksykon.txt",
            "olski/próbka.py",
        ),
        czyta=("docs/open-questions.md#własność-jednoznaczności-żąda-jej-od-zdania-które-jej-nie-ma",),
        ręką=("zdania z próbki przeczytać na nowo, bo `rozrzucona` wybiera je od nowa",),
    ),
    Figura(
        nazwa="sonda-readme",
        polecenie=("python3", "-m", "sonda", "proza/README.txt"),
        korpusy=("proza/README.txt",),
        #  Pomiar jest różnicą dwóch formalizmów nad jedną prozą, więc rusza go
        #  każda ze stron osobno, a README rusza obie naraz. `tests/test_sonda.py`
        #  łapie grubą połowę tego dryfu, czyli werdykt, który przestał się zgadzać,
        #  i nie łapie żadnej z liczb.
        kody=(0, 1),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/leksykon.txt",
            "olski/projekt.py",
            "olski/projekt.txt",
            "sonda/__main__.py",
            "sonda/polszczyzna.py",
            "sonda/wiezy.py",
        ),
        czyta=("docs/design-notes.md#podłoże-więzowe-zmierzone-sondą",),
        ręką=("rozejścia wypisane pod figurą przeczytać zdanie po zdaniu",),
    ),
    Figura(
        nazwa="końcówki",
        polecenie=(
            "python3",
            "-m",
            "harness.endings",
            "proza",
            "--probe",
            "nominalization",
            "--probe",
            "impersonal",
        ),
        korpusy=("proza/ksef", "proza/rit"),
        #  Klasy deklaruje sonda, a nie korpus, więc rusza tę figurę i ekstrakcja,
        #  i lista klas: pierwsza rusza liczby, druga potrafi ruszyć klasę.
        ruszają=("harness/endings.py", "harness/markdown.py", "olski/morph.py"),
        czyta=(
            "docs/linter.md#what-the-nominalization-endings-match",
            "docs/linter.md#the-impersonal-endings-come-out-the-other-way",
        ),
    ),
    Figura(
        nazwa="ekstrakcja-ksef",
        polecenie=("sh", "-c", "python3 -m olski.check $(find proza/ksef -name '*.txt')"),
        korpusy=("proza/ksef",),
        #  Figurą jest ostatni wiersz wydruku, czyli liczba fragmentów, i rusza ją
        #  to, co ekstrakcja zostawia, oraz to, co liczy się za zdanie.
        kody=(0, 1),
        ruszają=(
            "harness/markdown.py",
            "olski/document.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/check.py",
            "olski/leksykon.txt",
        ),
        czyta=("docs/extraction.md#what-the-numbers-here-were-run-over",),
    ),
    Figura(
        nazwa="ekstrakcja-rit",
        polecenie=("sh", "-c", "python3 -m olski.check $(find proza/rit -name '*.txt')"),
        korpusy=("proza/rit",),
        kody=(0, 1),
        ruszają=(
            "harness/markdown.py",
            "olski/document.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/check.py",
            "olski/leksykon.txt",
        ),
        czyta=("docs/extraction.md#what-the-numbers-here-were-run-over",),
    ),
    Figura(
        nazwa="ekstrakcja-notes",
        polecenie=("sh", "-c", "python3 -m olski.check $(find proza/notes -name '*.txt')"),
        #  Korpus jest cudzym repozytorium klonowanym płasko, więc przebieg, który
        #  się nie zgadza, potrafi mówić o korpusie ruszonym, a nie o kodzie;
        #  dokument z `czyta` podaje commit, na którym te liczby wzięto.
        korpusy=("proza/notes",),
        kody=(0, 1),
        ruszają=(
            "harness/markdown.py",
            "olski/document.py",
            "olski/subset.py",
            "olski/grammar.py",
            "olski/parse.py",
            "olski/morph.py",
            "olski/check.py",
            "olski/leksykon.txt",
        ),
        czyta=("docs/extraction.md#what-the-numbers-here-were-run-over",),
    ),
)


def odcisk(ścieżka: Path) -> str:
    return hashlib.sha256(ścieżka.read_bytes()).hexdigest()[:ZNAKÓW]


def wiersz_polecenia(polecenie: Sequence[str]) -> str:
    """Polecenie jednym wierszem, bo nagłówek pliku figury jest wierszowy.

    Zdanie podane po ``-c`` bywa wielowierszowe, a nagłówek czyta się do pierwszego
    wiersza pustego, więc nowa linia w argumencie urwałaby polecenie w połowie i
    figura wychodziłaby z raportu jako należna po wieki. Pisze i czyta to jedna
    funkcja, żeby zapis i porównanie nie rozjechały się na tym znaku.
    """
    return " ".join(polecenie).replace("\n", "\\n")


def zapis(figura: Figura, odciski: dict[str, str], wydruk: str) -> str:
    """Plik figury: nagłówek mówiący, skąd te liczby są, i wydruk przebiegu.

    Nagłówek jest po to, żeby przebieg dał się powtórzyć i żeby raport orzekł, czy
    jest jeszcze potrzebny, więc podaje polecenie, korpus, sekcje restytuujące i
    odciski. Wydruk zostaje pod nim nietknięty: przepisany albo obcięty przestałby
    być tym, co komenda wypisuje.
    """
    wiersze = [
        f"#  Ten plik powstaje przebiegiem: python3 -m harness.figury {figura.nazwa}",
        f"polecenie: {wiersz_polecenia(figura.polecenie)}",
    ]
    wiersze += [f"korpus: {korpus}" for korpus in figura.korpusy]
    #  Commit wchodzi do nagłówka, a nie tylko do deklaracji, bo plik figury czyta
    #  ten, kto szuka liczby, a polecenie nad skasowaną sondą jest bez niego ślepe.
    wiersze += [f"w gicie: {figura.w_gicie}"] if figura.w_gicie else []
    wiersze += [f"czyta: {sekcja}" for sekcja in figura.czyta]
    wiersze.append("ruszają:")
    wiersze += [f"  {plik}: {odciski[plik]}" for plik in figura.ruszają]
    return "\n".join(wiersze) + "\n\n" + wydruk.rstrip("\n") + "\n"


def nagłówek(zapisane: str) -> tuple[str, dict[str, str]]:
    """Polecenie i odciski z treści pliku figury.

    Polecenie czyta się razem z odciskami, bo zmiana samego polecenia — inny
    korpus, dopisana flaga — nie rusza ani jednego z nich, a wydruk pod nią
    odpowiada już na inne pytanie.

    Bierze napis, a nie ścieżkę, tak jak ``zapis`` wyżej napis oddaje, więc obie
    funkcje opisują jeden format i sprawdzają się bez pliku.
    """
    polecenie, odciski, w_bloku = "", {}, False
    for wiersz in zapisane.splitlines():
        if not wiersz.strip():
            break
        if wiersz.startswith("polecenie: "):
            polecenie = wiersz.removeprefix("polecenie: ")
        elif wiersz == "ruszają:":
            w_bloku = True
        elif w_bloku and wiersz.startswith("  "):
            plik, _, wartość = wiersz.strip().partition(": ")
            odciski[plik] = wartość
    return polecenie, odciski


def ciało(zapisane: str) -> str:
    """Sam wydruk przebiegu z treści pliku figury, czyli wszystko pod nagłówkiem."""
    _, _, wydruk = zapisane.partition("\n\n")
    return wydruk.rstrip("\n")


def stan(figura: Figura, zapisane: str, teraz: dict[str, str]) -> tuple[str, list[str]]:
    """Odpowiedź o jednej figurze i powody, dla których tak wypadła.

    Powodem jest nazwa pliku albo słowo ``polecenie``, bo należność bierze się i z
    tego, że przebieg czytał inny korpus, a nie tylko z tego, że kod się ruszył.

    Rozstrzyga się to z treści pliku i ze słownika odcisków, żeby dało się
    sprawdzić bez pliku i bez przebiegu; czytanie z dysku jest w ``należność``.
    """
    polecenie, odciski = nagłówek(zapisane)
    powody = ["polecenie"] if polecenie != wiersz_polecenia(figura.polecenie) else []
    powody += [plik for plik in figura.ruszają if odciski.get(plik) != teraz.get(plik)]
    niezmierzone = [plik for plik in figura.ruszają if odciski.get(plik) == NIEZNANY]
    if niezmierzone:
        return NIEZMIERZONA, niezmierzone + [p for p in powody if p not in niezmierzone]
    return (NALEŻNA, powody) if powody else (AKTUALNA, [])


def odciski_drzewa(figura: Figura) -> dict[str, str]:
    """Odciski tego, co rusza figurę, w drzewie takim, jakie jest teraz.

    Plik wymieniony w ``ruszają``, którego nie ma, zostaje bez odcisku i wychodzi
    z raportu jako należność. Że jest to usterka deklaracji, a nie stan figury,
    orzeka ``tests/test_figury.py``.
    """
    return {plik: odcisk(KORZEŃ / plik) for plik in figura.ruszają if (KORZEŃ / plik).exists()}


def należność(figura: Figura) -> tuple[str, list[str]]:
    #  Figura zamknięta odpowiada przed odciskami, bo pytanie o nie jest już
    #  bezprzedmiotowe: przebiegu, którego nikt nie powtórzy, nie ma po co liczyć
    #  za nieaktualny, a liczba pod nim jest pomiarem datowanym commitem, więc
    #  gramatyka ruszona potem czyni ją starszą od siebie, a nie fałszywą.
    if figura.zamknięta:
        return ZAMKNIĘTA, []
    if not figura.plik.exists():
        return BEZ_PLIKU, []
    return stan(figura, figura.plik.read_text(encoding="utf-8"), odciski_drzewa(figura))


def przelicz(figura: Figura) -> int:
    """Wykonuje przebieg i zapisuje jego wydruk wraz z odciskami.

    Odciski bierze się przed przebiegiem, a nie po nim: kod czyta się raz przy
    imporcie, więc to jego przebieg zmierzył, a plik ruszony w trakcie zapisałby
    się jako zmierzony, choć nie był (``CLAUDE.md#checks`` mówi to o samym
    przeliczaniu).
    """
    if brakujące := figura.brakujące:
        print(f"figury: {figura.nazwa} wymaga tego, czego tu nie ma: {', '.join(brakujące)}")
        return 2
    poprzedni = figura.plik.read_text(encoding="utf-8") if figura.plik.exists() else ""
    odciski = {plik: NIEZNANY for plik in figura.ruszają} | odciski_drzewa(figura)
    przebieg = subprocess.run(
        figura.polecenie, cwd=KORZEŃ, capture_output=True, text=True, check=False
    )
    if przebieg.returncode not in figura.kody or (przebieg.returncode and przebieg.stderr):
        sys.stderr.write(przebieg.stderr)
        print(f"figury: {' '.join(figura.polecenie)} wyszło z kodem {przebieg.returncode}")
        return 2
    KATALOG.mkdir(exist_ok=True)
    figura.plik.write_text(zapis(figura, odciski, przebieg.stdout), encoding="utf-8")
    print(f"figury: {figura.plik.relative_to(KORZEŃ)} przeliczona")
    if not poprzedni or ciało(poprzedni) == przebieg.stdout.rstrip("\n"):
        return 0
    #  Prozy nikt za autora nie poprawi, a przeliczenie jest jedyną chwilą, w której
    #  widać, że liczby się ruszyły, więc raport nad figurą aktualną już tego nie powie.
    for sekcja in figura.czyta:
        print(f"figury: wydruk inny niż poprzednio, więc przeczytaj restytucję: {sekcja}")
    for robota in figura.ręką:
        print(f"figury: wydruk inny niż poprzednio, więc zostaje ręką: {robota}")
    return 0


def przelicz_należne() -> int:
    """Przelicz każdą figurę, którą raport nazywa należną.

    Jedna zmiana w parserze czyni należnymi kilkanaście figur naraz,
    a przepisywanie ich nazw z raportu do wiersza poleceń jest krokiem,
    w którym gubi się jedna, i to bez śladu:
    figura pominięta czyta się potem tak samo jak figura przeliczona,
    bo różni je jeden odcisk w nagłówku.

    Każda idzie tą samą drogą, co przeliczenie z nazwą,
    więc o figurze bez korpusu mówi to samo i tym samym kodem wyjścia.
    Figury niezmierzonej tutaj ta komenda nie rusza,
    bo raport nie nazywa jej należną,
    a pierwszy przebieg nad nią jest decyzją, a nie krokiem porządkowym.
    """
    należne = [figura for figura in FIGURY if należność(figura)[0] == NALEŻNA]
    if not należne:
        print("figury: nic nie jest należne przeliczenia")
    return max((przelicz(figura) for figura in należne), default=0)


def raport() -> int:
    """Wypisuje odpowiedź o każdej figurze; kod 1, gdy któraś nie jest aktualna.

    Nie pobiera niczego i nie wykonuje żadnej sondy, więc odpowiada tam, gdzie
    korpusu nie ma, w sesji z pustym kontenerem włącznie.
    """
    #  Szerokość bierze się z najdłuższej nazwy, a nie z liczby wpisanej tutaj:
    #  wpisana rozjeżdża kolumny przy pierwszej figurze o nazwie dłuższej,
    #  a raport czyta się właśnie kolumnami.
    szerokość = max(len(figura.nazwa) for figura in FIGURY)
    należne = 0
    for figura in FIGURY:
        odpowiedź, powody = należność(figura)
        powód = f" — {', '.join(powody)}" if powody else ""
        print(f"{figura.nazwa:<{szerokość}} {odpowiedź}{powód}")
        if odpowiedź in (AKTUALNA, ZAMKNIĘTA):
            continue
        należne += 1
        if brakujące := figura.brakujące:
            print(f"{'':<{szerokość}} wymaga tego, czego tu nie ma: {', '.join(brakujące)}")
        for sekcja in figura.czyta:
            print(f"{'':<{szerokość}} restytucja w prozie: {sekcja}")
        for robota in figura.ręką:
            print(f"{'':<{szerokość}} ręką: {robota}")
    #  Jeden wiersz, a nie wiersz przy każdej figurze: nieorzeczonych jest dziś
    #  tyle, ile figur, więc adnotacja przy każdej z osobna byłaby raportem o sobie
    #  samym. Orzeczenie zapada przy zmianie, która i tak figurę rusza, tak jak
    #  ``CLAUDE.md#reguły-przyjmujemy-leniwie`` każe przyjmować resztę reguł.
    if nieorzeczone := sum(1 for figura in FIGURY if figura.powtórzy is None):
        print(f"bez orzeczenia, kto ten przebieg jeszcze powtórzy: {nieorzeczone}")
    return 1 if należne else 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.figury",
        description="Figury: raport o należnych przeliczeniach, a z nazwą — przeliczenie.",
    )
    parser.add_argument(
        "nazwy",
        nargs="*",
        help="figury do przeliczenia; bez nazwy sam raport, który nic nie pobiera",
    )
    parser.add_argument(
        "--należne",
        action="store_true",
        help="przelicz wszystkie figury należne przeliczenia, które są tu do policzenia",
    )
    args = parser.parse_args(argv)
    if args.należne and args.nazwy:
        parser.error("--należne wybiera figury samo, więc nazwy są przy nim zbędne")
    if args.należne:
        return przelicz_należne()
    if not args.nazwy:
        return raport()
    znane = {figura.nazwa: figura for figura in FIGURY}
    nieznane = [nazwa for nazwa in args.nazwy if nazwa not in znane]
    for nazwa in nieznane:
        print(f"figury: nie ma takiej figury: {nazwa}", file=sys.stderr)
    if nieznane:
        print(f"figury: zadeklarowane są {', '.join(znane)}", file=sys.stderr)
        return 2
    return max(przelicz(znane[nazwa]) for nazwa in args.nazwy)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
