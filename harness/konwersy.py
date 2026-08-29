"""Ile czasowników czyta zdanie przechodnie w obie strony naraz, według Walentego.

``Wynajmę mieszkanie.`` olski przyjmuje i mówi o nim ``jedno odczytanie``, a czytelnik
ma dwa: raz mieszkanie wynajmuje właściciel, raz lokator. Jest to wieloznaczność,
której werdykt nie melduje, i ``docs/disambiguation.md`` opisuje ją wraz z tym,
co miałoby ją zdejmować. Ta sonda odpowiada na pytanie, które stoi przed tamtym:
ilu lematów to dotyczy.

**Konwersem jest tu para czytań, w której zamieniają się uczestnicy.** Wynajmować
komuś i wynajmować od kogoś to jedno zdarzenie opowiedziane z dwóch stron, a
zdanie o samym podmiocie i dopełnieniu nie mówi, z której. Pozycja, która by to
rozstrzygnęła, w takim zdaniu nie stoi.

Walenty nie nazywa ról, więc para taka nie jest w nim zapisana i trzeba ją zgadnąć
z kształtu pozycji. Kryterium jest stąd: lemat ma schemat z celownikiem i schemat
z frazą źródłową (``od`` albo ``u`` z dopełniaczem), oba o podmiocie i dopełnieniu,
i żaden jego schemat nie bierze obu tych pozycji naraz, bo pozycje, które stoją w
jednym zdaniu obok siebie, opowiadają je z jednej strony.

Liczba jest przez to górnym oszacowaniem i myli się w jedną stronę, mocno.
Celownik bywa posiadaczem albo tym, komu się przysłuży — ``ściągnąć komuś czapkę``
— i taki celownik stoi obok frazy źródłowej, nie naprzeciwko niej. Ile z tego
zostaje po przeczytaniu, mówi ``docs/disambiguation.md`` przy liczbie stąd; sonda
sądu o parze nie wydaje.

Plik wejściowy nie stoi w repozytorium: pobiera się go tak, jak bank drzew, a
polecenie trzyma docs/subset.md.

    python3 -m harness.konwersy walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from harness.próbka import rozrzucona
from harness.walenty import PODMIOT, pozycje, schematy

#: Etykieta pozycji dopełnienia. Sprawdza się ją dopiero po podmiocie, bo ``subj``
#: niesie ``obj`` w środku i pytanie zadane samym ``in`` czytałoby podmiot jako
#: dopełnienie.
DOPEŁNIENIE = "obj"

#: Pozycja, którą schemat nazywa odbiorcę. Celownik jest w polszczyźnie
#: przypadkiem tego, komu się daje, więc druga strona tej samej wymiany stoi pod
#: przyimkiem.
CELOWNIK = "np(dat)"

#: Pozycje, którymi schemat nazywa źródło, czyli tego, od kogo się bierze.
ŹRÓDŁO = ("prepnp(od,gen)", "prepnp(u,gen)")

#: Pozycja zleksykalizowana, czyli taka, w której Walenty żąda konkretnego słowa.
#: ``pożyczyć coś od kogoś dla siebie`` ma celownik i ma go zleksykalizowanego na
#: ``siebie``, więc uczestnikiem on nie jest i tej pary nie zamyka.
ZLEKSYKALIZOWANA = "lex("

#: Ile par wypisać do przeczytania. Sama liczba nie mówi, czy kryterium trafiło
#: w konwersy, czy w celownik posiadacza, a rozstrzyga to dopiero czytanie par;
#: lematy idą alfabetycznie, więc próbka jest rozrzucona po całej liście.
PRZYKŁADY = 12


@dataclass(frozen=True)
class Opis:
    """Co schemat mówi o wyborze, przed którym staje zdanie o samym podmiocie i dopełnieniu."""

    #: Czy schemat ma i podmiot, i dopełnienie, czyli czy takie zdanie w ogóle
    #: pod niego podchodzi.
    przechodni: bool
    #: Czy stoi w nim pozycja odbiorcy.
    celownik: bool
    #: Czy stoi w nim pozycja źródła.
    źródło: bool


@dataclass(frozen=True)
class Konwers:
    """Lemat wraz z parą schematów, między którymi zdanie przechodnie nie wybiera."""

    lemat: str
    #: Schemat z celownikiem, w postaci, w jakiej stoi w Walentym.
    odbiorca: str
    #: Schemat z frazą źródłową, tamże.
    źródło: str


def alternatywy(żądanie: str) -> list[str]:
    """Kształty, którymi pozycja może się wypełnić, bez tych zleksykalizowanych.

    Walenty rozdziela alternatywy średnikiem — ``obj{np(str);ncp(str,że)}`` — a
    średnik stoi też wewnątrz nawiasu pozycji zleksykalizowanej, gdzie rozdziela
    słowa: ``OR('twarz';'usta')``. Rozcięcie idzie więc po średnikach spoza
    nawiasów, tak jak :func:`harness.walenty.pozycje` idzie po plusach spoza nich.

    Klamry zdejmuje się z obu stron, choć :func:`harness.walenty.pozycje` wydaje
    żądanie bez otwierającej: żądanie jest tym, co stoi w klamrach, a kształt
    zależny od tego, która z nich została, byłby drugą umową do zapamiętania.
    """
    żądanie = żądanie.strip().removeprefix("{").removesuffix("}")
    poziom, bieżąca, zebrane = 0, "", []
    for znak in żądanie:
        if znak == "(":
            poziom += 1
        elif znak == ")":
            poziom -= 1
        if znak == ";" and poziom == 0:
            zebrane.append(bieżąca.strip())
            bieżąca = ""
        else:
            bieżąca += znak
    zebrane.append(bieżąca.strip())
    return [kształt for kształt in zebrane if not kształt.startswith(ZLEKSYKALIZOWANA)]


def opisz(schemat: str) -> Opis:
    """Podmiot, dopełnienie, odbiorca i źródło jednego schematu.

    Odbiorcy ani źródła nie szuka się w pozycji podmiotu, bo tam ta sama fraza
    mówi co innego: ``od`` z dopełniaczem stoi w podmiocie zdania o tym, co się
    od czegoś zaczyna, a nie o tym, że ktoś coś od kogoś wziął.
    """
    podmiot = dopełnienie = celownik = źródło = False
    for etykieta, żądanie in pozycje(schemat):
        if PODMIOT in etykieta:
            podmiot = True
            continue
        if DOPEŁNIENIE in etykieta:
            dopełnienie = True
        kształty = alternatywy(żądanie)
        celownik = celownik or CELOWNIK in kształty
        źródło = źródło or any(kształt in ŹRÓDŁO for kształt in kształty)
    return Opis(przechodni=podmiot and dopełnienie, celownik=celownik, źródło=źródło)


def konwersy(słownik: Mapping[str, Sequence[str]]) -> list[Konwers]:
    """Lematy, których dwa schematy przechodnie opowiadają zdarzenie z dwóch stron.

    Schemat nieprzechodni odpada, bo zdanie o podmiocie i dopełnieniu pod niego
    nie podchodzi, a lemat, którego jeden schemat bierze obie pozycje naraz,
    odpada cały: skoro odbiorca i źródło stoją w jednym zdaniu obok siebie, to
    nie są dwiema stronami jednej wymiany.
    """
    zebrane = []
    for lemat, ich_schematy in słownik.items():
        opisy = [(schemat, opisz(schemat)) for schemat in ich_schematy]
        przechodnie = [(schemat, opis) for schemat, opis in opisy if opis.przechodni]
        if any(opis.celownik and opis.źródło for _schemat, opis in przechodnie):
            continue
        odbiorca = next((schemat for schemat, opis in przechodnie if opis.celownik), None)
        źródło = next((schemat for schemat, opis in przechodnie if opis.źródło), None)
        if odbiorca and źródło:
            zebrane.append(Konwers(lemat=lemat, odbiorca=odbiorca, źródło=źródło))
    return sorted(zebrane, key=lambda konwers: konwers.lemat)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.konwersy",
        description="Policz czasowniki, których zdanie przechodnie nie wybiera strony wymiany.",
    )
    parser.add_argument("schematy", help="walenty_*_verbs_all.txt z wydania tekstowego")
    parser.add_argument(
        "--przykłady",
        type=int,
        default=PRZYKŁADY,
        dest="przykłady",
        help=f"ile par wypisać do przeczytania (domyślnie {PRZYKŁADY})",
    )
    args = parser.parse_args(argv)

    słownik = schematy(args.schematy)
    znalezione = konwersy(słownik)
    print(f"{len(znalezione)} z {len(słownik)} lematów czasownikowych")
    for konwers in rozrzucona(znalezione, args.przykłady):
        print(f"  {konwers.lemat}")
        print(f"    odbiorca: {konwers.odbiorca.strip()}")
        print(f"    źródło:   {konwers.źródło.strip()}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
