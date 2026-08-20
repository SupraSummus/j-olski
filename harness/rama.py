"""Ile spornych przyłączeń rozstrzyga rama, i czy rozstrzyga je zgodnie z bankiem drzew.

``docs/disambiguation.md`` mówi, że część spornych wyrażeń przyimkowych
rozstrzyga się słownikiem, a nie rankingiem: fraza, której schemat jednej ze
stron żąda, przeczytana po drugiej stronie łamie ten schemat. Ten przebieg wycenił
świadka ramowego przed dopisaniem go, tak jak wyceniono przysłówek przed
wpuszczeniem go do gramatyki, i wycenia go dalej: świadek
wskazuje po stronie rzeczownika, a co byłby wart po drugiej, mówi ten przebieg.

**Wyceniane jest pytanie, a nie odpowiedź warstwy.** Sonda pyta bank drzew o to,
dokąd wyrażenie doszło u anotatora, i zestawia to z samym kryterium, a nie
z werdyktem: rozstrzygnięcie warstwy nad werdyktem mierzy ``harness/wskazania.py``.
Populacją jest tu wyrażenie, a nie zdanie, więc żadna produkcja tych liczb nie
rusza.

**Kryterium jest jedno i pyta o nie ta sonda oraz leksykon.** ``przyimki``
w ``olski/walenty.py`` mówi, że lemat żąda przyimka wtedy, gdy któryś jego
schemat ma pozycję niepodmiotową z ``prepnp`` o tym przyimku, i to samo pytanie
wypisuje kolumnę ``olski/leksykon.txt``, którą czyta świadek. Druga kopia
rozeszłaby się cicho, bo rozejście widać dopiero w liczbach, a nie w wydruku.

Odpowiedź pada tu, gdy żąda przyimka dokładnie jedna strona: czasownik przed
wyrażeniem albo rzeczownik kończący grupę przed nim. Żądanie obustronne jest
milczeniem, bo schematu nie łamie wtedy żadne czytanie, i milczeniem jest też
brak żądania po obu stronach. Świadek czyta to samo kryterium połową:
wskazuje sam rzeczownik, a żądanie czasownika jest u niego wetem.

Kryterium pyta o przyimek i nie pyta o przypadek, więc zasięg wychodzi z niego
zawyżony: Walenty pisze ``prepnp(o,loc)`` obok ``prepnp(o,acc)``, a
``Attachment`` niesie sam przyimek, więc ``informacja o błędzie`` pasuje tu do
obu wpisów naraz. Zwężenie żąda przypadka grupy pod przyimkiem, czyli pola,
którego ``olski/attachment.py`` nie wydaje.

Sonda czyta Walentego wprost, a nie leksykon, i to jest tu różnica: leksykon
niesie kolumnę o rzeczowniku wypisanym w pliku rzeczownikowym, a ta sonda pyta
o obie strony naraz, także o tę, po której świadka nie ma. Wariant
``--tylko-pewne`` stoi tu z tego samego powodu.

Pliki wejściowe nie stoją w repozytorium: pobiera się je tak, jak bank drzew, a
polecenia trzymają docs/subset.md oraz docs/corpus.md.

    python3 -m harness.rama Składnica-frazowa-180723/ \\
      --czasowniki walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt \\
      --rzeczowniki walenty_20160418-text/nouns/walenty_20160418_nouns_all.txt
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from olski.attachment import LUŹNA, WYMAGANA, attachments
from olski.corpus import pliki, read_forest
from olski.próbka import rozrzucona
from olski.walenty import PEWNY, przyimki, schematy

#: Gospodarz po stronie czasownika i po stronie rzeczownika, tak jak nazywa je
#: ``olski/attachment.py`` w polu ``host``.
CZASOWNIK, RZECZOWNIK = "clause", "noun"

#: Ile odpowiedzi wypisać do przeczytania. Sama trafność nie mówi, czy świadek
#: wskazuje gospodarza z powodu, który da się autorowi pokazać, a rozstrzyga to
#: dopiero czytanie odpowiedzi.
PRZYKŁADY = 12


@dataclass(frozen=True)
class Odpowiedź:
    """Jedno sporne przyłączenie wraz z tym, co o nim mówi rama i co bank drzew."""

    #: Przyimek, lemat czasownika i lemat rzeczownika, czyli trójka, na której to
    #: kryterium stoi.
    przyimek: str
    czasownik: str
    rzeczownik: str
    #: Gospodarz wskazany ramą: ``clause``, ``noun`` albo puste, gdy milczenie.
    wskazany: str
    #: Gospodarz wybrany przez anotatora.
    wzorcowy: str
    #: ``fw`` albo ``fl``, gdy wyrażenie stanęło pod jedną z tych fraz.
    fraza: str | None

    @property
    def trafna(self) -> bool:
        return bool(self.wskazany) and self.wskazany == self.wzorcowy


def odpowiedzi(
    paths: Sequence[Path],
    czasowniki: Mapping[str, Sequence[str]],
    rzeczowniki: Mapping[str, Sequence[str]],
    tylko_pewne: bool = False,
) -> list[Odpowiedź]:
    """Sporne przyłączenia banku drzew, każde wraz z odpowiedzią ramy albo z milczeniem.

    Populacją jest pozycja dwuznaczna, czyli ta, w której oba gospodarze stoją do
    wzięcia: to samo zwężenie, którym liczy ``Report`` w
    ``olski/attachment.py``. Wyrażenie, przed którym nie kończy się grupa imienna
    albo nie stoi forma czasownikowa, wyboru nie stawia, więc świadek nie ma tam
    czego rozstrzygać.
    """
    zebrane = []
    for path in paths:
        for przyłączenie in attachments(read_forest(path)):
            if not (przyłączenie.postverbal and przyłączenie.postnominal):
                continue
            if przyłączenie.host not in (CZASOWNIK, RZECZOWNIK):
                continue
            żąda_czasownik = przyłączenie.prep in przyimki(
                czasowniki.get(przyłączenie.verb, ()), tylko_pewne
            )
            żąda_rzeczownik = przyłączenie.prep in przyimki(
                rzeczowniki.get(przyłączenie.noun, ()), tylko_pewne
            )
            wskazany = ""
            if żąda_czasownik and not żąda_rzeczownik:
                wskazany = CZASOWNIK
            elif żąda_rzeczownik and not żąda_czasownik:
                wskazany = RZECZOWNIK
            zebrane.append(
                Odpowiedź(
                    przyimek=przyłączenie.prep,
                    czasownik=przyłączenie.verb,
                    rzeczownik=przyłączenie.noun,
                    wskazany=wskazany,
                    wzorcowy=przyłączenie.host,
                    fraza=przyłączenie.frame,
                )
            )
    return zebrane


def _udział(ile: int, z_ilu: int) -> str:
    return f"{100 * ile / z_ilu:5.1f}%" if z_ilu else "    —"


def render(wszystkie: Sequence[Odpowiedź], przykłady: int = PRZYKŁADY) -> str:
    """Zasięg i trafność, a pod nimi odpowiedzi do przeczytania.

    Kolejność wierszy jest napisana tutaj, a nie wzięta ze zbioru, bo zbiór
    wypisywałby je w każdym przebiegu inaczej (``CLAUDE.md``, o porządku
    wypisywanego wyjścia).
    """
    padłe = [o for o in wszystkie if o.wskazany]
    trafne = [o for o in padłe if o.trafna]

    def rozbicie(nazwa: str, stąd: Sequence[Odpowiedź]) -> str:
        dobrze = [o for o in stąd if o.trafna]
        return f"    {nazwa:11} {len(stąd):5}  {_udział(len(dobrze), len(stąd))} trafnych"

    wiersze = [
        f"{len(wszystkie)} spornych przyłączeń banku drzew",
        f"  {len(padłe):5}  {_udział(len(padłe), len(wszystkie))} zasięg,"
        " czyli rama żąda po jednej stronie",
        f"  {len(trafne):5}  {_udział(len(trafne), len(padłe))} trafność wśród tych odpowiedzi",
        "",
        "  czym odpowiedziała rama:",
        rozbicie("czasownik", [o for o in padłe if o.wskazany == CZASOWNIK]),
        rozbicie("rzeczownik", [o for o in padłe if o.wskazany == RZECZOWNIK]),
        "",
        "  co bank drzew mówi o odpowiedziach, po frazie, pod którą stanęły:",
        rozbicie("wymagana", [o for o in padłe if o.fraza == WYMAGANA]),
        rozbicie("luźna", [o for o in padłe if o.fraza == LUŹNA]),
        rozbicie("bez frazy", [o for o in padłe if o.fraza is None]),
        "",
        "  odpowiedzi do przeczytania:",
    ]
    for o in rozrzucona(padłe, przykłady):
        werdykt = "trafna " if o.trafna else "pomyłka"
        wiersze.append(
            f"    {werdykt}  „{o.przyimek}” → {o.wskazany:6}"
            f"  czasownik: {o.czasownik}, rzeczownik: {o.rzeczownik}"
        )
    return "\n".join(wiersze)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 -m harness.rama",
        description="Wyceń świadka ramowego: ile spornych przyłączeń rozstrzyga rama.",
    )
    parser.add_argument("korpus", help="katalog Składnicy")
    parser.add_argument(
        "--czasowniki", required=True, help="walenty_*_verbs_all.txt z wydania tekstowego"
    )
    parser.add_argument(
        "--rzeczowniki", required=True, help="walenty_*_nouns_all.txt z wydania tekstowego"
    )
    parser.add_argument(
        "--tylko-pewne",
        action="store_true",
        dest="tylko_pewne",
        help=f"bierz same schematy o kwalifikatorze `{PEWNY}`",
    )
    parser.add_argument(
        "--przykłady",
        type=int,
        default=PRZYKŁADY,
        dest="przykłady",
        help=f"ile odpowiedzi wypisać do przeczytania (domyślnie {PRZYKŁADY})",
    )
    args = parser.parse_args(argv)

    print(
        render(
            odpowiedzi(
                pliki(Path(args.korpus)),
                schematy(args.czasowniki),
                schematy(args.rzeczowniki),
                args.tylko_pewne,
            ),
            args.przykłady,
        )
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
