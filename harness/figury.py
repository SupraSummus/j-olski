"""Figura ma jednego właściciela: plik, który wypisuje przebieg.

Reguła i jej powód są w ``CLAUDE.md#checks``, a tutaj jest to, czym ona działa.
``FIGURY`` niżej deklaruje na każdy przebieg polecenie, korpus, pliki, których
zmiana rusza liczby, oraz sekcję restytuującą figurę grubiej. Plik figury zapisuje
odciski tych plików z chwili przebiegu, więc pytanie o należność przeliczenia
porównuje dwa napisy i po korpus nie sięga.

Stąd dwie komendy zamiast jednej: raport odpowiada wszędzie, bo nie pobiera
niczego, a przeliczenie wymaga korpusu i wykonuje je ktoś, kto go ma.

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

#: Cztery odpowiedzi raportu. Są nazwane, bo drukuje je jedna funkcja, a odróżnia
#: druga, i literał powtórzony w obu rozjechałby się przy pierwszej zmianie słowa.
AKTUALNA = "aktualna"
NALEŻNA = "należna"
NIEZMIERZONA = "niezmierzona tutaj"
BEZ_PLIKU = "bez pliku"

#: Ile znaków odcisku zapisywać. Odcisk odpowiada na jedno pytanie — czy plik jest
#: ten sam — a nie na pytanie o podstawienie, więc reszta sześćdziesięciu czterech
#: znaków kosztowałaby czytelność nagłówka i nic nie kupiła.
ZNAKÓW = 12


@dataclass(frozen=True)
class Figura:
    """Jeden przebieg, jeden plik i lista tego, co ten plik rusza.

    Jednostką jest przebieg, a nie tabela w dokumencie: sonda różnicowa nad
    Składnicą i ta sama sonda nad prozą mają osobne korpusy i osobne wydruki, więc
    jedna należy się przeliczenia wtedy, gdy druga nie.
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
    #: Ścieżki korpusów, bez których polecenie nie ma czego czytać; puste, kiedy
    #: przebieg nie pobiera niczego. Rozstrzyga, czy przeliczenie wykonuje się
    #: tutaj, czy należy do kogoś z korpusem. Krotka, a nie jedna ścieżka, bo
    #: przebieg bywa porównaniem dwóch korpusów naraz i brak każdego z nich
    #: zatrzymuje go osobno.
    korpusy: tuple[str, ...] = ()

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
        ruszają=("olski/subset.py", "olski/parse.py", "sonda/negacja.py", "sonda/ruch.py"),
        czyta=("docs/subset.md#negacja-zmierzona-kupuje-przeszło-sto-zdań-i-nie-płaci-dopełniaczem",),
    ),
    Figura(
        nazwa="negacja-proza",
        polecenie=("python3", "-m", "sonda.negacja", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/parse.py",
            "sonda/negacja.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#negacja-zmierzona-kupuje-przeszło-sto-zdań-i-nie-płaci-dopełniaczem",),
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
        nazwa="przysłówek-proza",
        polecenie=("python3", "-m", "sonda.przysłówek", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/parse.py",
            "olski/grammar.py",
            "sonda/przysłówek.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#przysłówek-wchodzi-obu-gospodarzami-bo-drugi-zdejmuje-czytania-nieprawdziwe",
            "docs/roadmap.md#etap-6-reszta-konstrukcji",
        ),
    ),
    Figura(
        nazwa="płaski",
        polecenie=("python3", "-m", "sonda.płaski", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
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
            "olski/parse.py",
            "olski/grammar.py",
            "sonda/przysłówek.py",
            "sonda/ruch.py",
            "sonda/płaski.py",
        ),
        czyta=("docs/subset.md#płaska-lista-okoliczników-mówi-o-zdaniu-nieprawdę",),
    ),
    Figura(
        nazwa="płaski-proza",
        polecenie=("python3", "-m", "sonda.płaski", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
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
            "olski/parse.py",
            "sonda/przecinek.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania",),
    ),
    Figura(
        nazwa="przecinek-proza",
        polecenie=("python3", "-m", "sonda.przecinek", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/parse.py",
            "sonda/przecinek.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#przecinek-zmierzono-i-nie-odbiera-ani-jednego-zdania",
        ),
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
        nazwa="interpunkcja-proza",
        polecenie=("python3", "-m", "sonda.interpunkcja", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/parse.py",
            "olski/morph.py",
            "sonda/interpunkcja.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#interpunkcja-zdaniowa-zmierzona-kupuje-kilkadziesiąt-zdań-i-nie-odbiera-żadnego",
        ),
    ),
    Figura(
        nazwa="liczebnik",
        polecenie=("python3", "-m", "sonda.liczebnik", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/parse.py",
            "sonda/liczebnik.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#liczebnik-zmierzono-i-nie-odbiera-ani-jednego-zdania",),
    ),
    Figura(
        nazwa="liczebnik-proza",
        polecenie=("python3", "-m", "sonda.liczebnik", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/parse.py",
            "sonda/liczebnik.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#liczebnik-zmierzono-i-nie-odbiera-ani-jednego-zdania",
        ),
    ),
    Figura(
        nazwa="szyk",
        polecenie=("python3", "-m", "sonda.szyk", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/parse.py",
            "sonda/szyk.py",
            "sonda/ruch.py",
        ),
        czyta=("docs/subset.md#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka",),
    ),
    Figura(
        nazwa="szyk-proza",
        polecenie=("python3", "-m", "sonda.szyk", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/parse.py",
            "sonda/szyk.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#szyk-zmierzono-kupuje-kilkadziesiąt-zdań-i-odbiera-kilka",
        ),
    ),
    Figura(
        nazwa="okolicznikowe",
        polecenie=("python3", "-m", "sonda.okolicznikowe", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        ruszają=(
            "olski/subset.py",
            "olski/parse.py",
            "sonda/okolicznikowe.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie",
        ),
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
            "olski/parse.py",
            "sonda/okolicznikowe.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie",
        ),
    ),
    Figura(
        nazwa="okolicznikowe-proza",
        polecenie=("python3", "-m", "sonda.okolicznikowe", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/parse.py",
            "sonda/okolicznikowe.py",
            "sonda/ruch.py",
        ),
        czyta=(
            "docs/subset.md#zdanie-okolicznikowe-zmierzono-pod-złotą-morfologią-jest-darmowe-a-pod-żywą-nie",
        ),
    ),
    Figura(
        nazwa="czoło",
        polecenie=("python3", "-m", "sonda.czoło", "Składnica-frazowa-180723/"),
        korpusy=("Składnica-frazowa-180723",),
        #  Gramatyki tu nie ma, tak samo jak przy figurze niżej: liczone są cudze
        #  zdania, a rusza je lista, o którą sonda pyta, i nic poza nią.
        ruszają=("olski/subset.py", "sonda/czoło.py"),
        czyta=(
            "docs/subset.md#okolicznik-wyrażony-zdaniem-nie-jest-pozycją-ramy-i-dochodzi-do-zdania",
        ),
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
        ruszają=("sonda/rama.py", "olski/attachment.py"),
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
            "olski/parse.py",
            "olski/skład/rozbiór.py",
            "olski/skład/składnia.py",
            "sonda/znaczenia.py",
        ),
        czyta=("docs/architecture.md#werdykt-liczy-wyprowadzenia-bo-powstaje-pod-dwiema-warstwami-które-liczą-znaczenia",),
    ),
    Figura(
        nazwa="znaczenia-proza",
        polecenie=("python3", "-m", "sonda.znaczenia", "proza/README.txt"),
        ruszają=(
            "README.md",
            "harness/markdown.py",
            "olski/subset.py",
            "olski/parse.py",
            "olski/skład/rozbiór.py",
            "olski/skład/składnia.py",
            "sonda/znaczenia.py",
        ),
        czyta=("docs/architecture.md#werdykt-liczy-wyprowadzenia-bo-powstaje-pod-dwiema-warstwami-które-liczą-znaczenia",),
    ),
)


def odcisk(ścieżka: Path) -> str:
    return hashlib.sha256(ścieżka.read_bytes()).hexdigest()[:ZNAKÓW]


def zapis(figura: Figura, odciski: dict[str, str], wydruk: str) -> str:
    """Plik figury: nagłówek mówiący, skąd te liczby są, i wydruk przebiegu.

    Nagłówek jest po to, żeby przebieg dał się powtórzyć i żeby raport orzekł, czy
    jest jeszcze potrzebny, więc podaje polecenie, korpus, sekcje restytuujące i
    odciski. Wydruk zostaje pod nim nietknięty: przepisany albo obcięty przestałby
    być tym, co komenda wypisuje.
    """
    wiersze = [
        f"#  Ten plik powstaje przebiegiem: python3 -m harness.figury {figura.nazwa}",
        f"polecenie: {' '.join(figura.polecenie)}",
    ]
    wiersze += [f"korpus: {korpus}" for korpus in figura.korpusy]
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
    powody = ["polecenie"] if polecenie != " ".join(figura.polecenie) else []
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
        print(f"figury: {figura.nazwa} wymaga korpusu, którego tu nie ma: {', '.join(brakujące)}")
        return 2
    poprzedni = figura.plik.read_text(encoding="utf-8") if figura.plik.exists() else ""
    odciski = {plik: NIEZNANY for plik in figura.ruszają} | odciski_drzewa(figura)
    przebieg = subprocess.run(
        figura.polecenie, cwd=KORZEŃ, capture_output=True, text=True, check=False
    )
    if przebieg.returncode != 0:
        sys.stderr.write(przebieg.stderr)
        print(f"figury: {' '.join(figura.polecenie)} wyszło z kodem {przebieg.returncode}")
        return 2
    KATALOG.mkdir(exist_ok=True)
    figura.plik.write_text(zapis(figura, odciski, przebieg.stdout), encoding="utf-8")
    print(f"figury: {figura.plik.relative_to(KORZEŃ)} przeliczona")
    if ciało(poprzedni) == przebieg.stdout.rstrip("\n"):
        return 0
    #  Prozy nikt za autora nie poprawi, a przeliczenie jest jedyną chwilą, w której
    #  widać, że liczby się ruszyły, więc raport nad figurą aktualną już tego nie powie.
    for sekcja in figura.czyta:
        print(f"figury: wydruk inny niż poprzednio, więc przeczytaj restytucję: {sekcja}")
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
    należne = 0
    for figura in FIGURY:
        odpowiedź, powody = należność(figura)
        powód = f" — {', '.join(powody)}" if powody else ""
        print(f"{figura.nazwa:<16} {odpowiedź}{powód}")
        if odpowiedź == AKTUALNA:
            continue
        należne += 1
        if brakujące := figura.brakujące:
            print(f"{'':<16} przeliczy ją ktoś z korpusem: {', '.join(brakujące)}")
        for sekcja in figura.czyta:
            print(f"{'':<16} restytucja w prozie: {sekcja}")
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
