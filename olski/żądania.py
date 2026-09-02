"""Czego czasownik żąda od słowa stojącego w jego pozycji: leksykon nad plikiem żądań.

Leksykon walencyjny mówi, co czasownik bierze, a nie mówi, czego od tego żąda:
``zażądać`` bierze dopełnienie w dopełniaczu, a w podmiocie żąda człowieka.
To drugie stoi w ``olski/żądania.txt``, który wychodzi z wydania TEI Walentego
(``harness/żądania.py``), a czemu jest plikiem osobnym od leksykonu, mówi
docs/warstwa-leksykalna.md#żądanie-pozycji-jest-osobnym-plikiem-a-nie-kolumną-leksykonu.

Moduł ten czyta sam plik i odpowiada na pytanie o jedno słowo w jednej pozycji.
Które słowo w zdaniu jest czasownikiem i którą pozycję obsadza które wypełnienie,
rozstrzyga warstwa nad czytaniem (``Verdict.żądania`` w ``olski/werdykt.py``);
tam też stoi wiersz, którym werdykt to nazywa.
Podział jest ten sam co przy leksykonie walencyjnym: plik czyta moduł, który nie
ogląda ani gramatyki, ani rozbioru, więc czyta się go bez analizatora morfologicznego
i bez niego działa też przekład, który ten plik pisze.

**Odpowiedź jest połową pytania i drugiej połowy tu nie ma.**
Warstwa nazywa żądanie i nie pyta, czy słowo stojące w pozycji je spełnia;
orzekłby o tym wordnet, którego to repozytorium nie ma
(docs/open-questions.md#shared-questions).
Wyjątkiem są klasy osobowe (:data:`OSOBOWE`), bo tam odpowiada projekt sam,
deklaracją swoich osób (``olski/osoby.py``); żądanie i tam wychodzi stąd,
a spełnienie stamtąd.

**Milczenie jest odpowiedzią pełnoprawną**, tak samo jak w warstwie
rozstrzygającej (``olski/rozstrzyganie.py``), i jest odpowiedzią domyślną
(:func:`żądane`).
Główną jego przyczyną jest zasięg samego pliku: warstwę semantyczną ma w tym
wydaniu część czasowników leksykonu, i nie ma jej ani jeden z tych, którymi
ten rejestr orzeka najczęściej (docs/prior-art.md#polish-language-resources).
"""

from __future__ import annotations

import functools
from collections.abc import Iterable
from pathlib import Path

from olski.walencja import BIERNIK, CELOWNIK, DOPEŁNIACZ

#: Plik żądań, czytany przy pierwszym pytaniu.
PLIK = Path(__file__).parent / "żądania.txt"

#: Klasa, którą Walenty nazywa rzecz dowolną, czyli pozycję, która nie żąda niczego.
#: Kolumna klas jest alternatywą po wszystkich ramach lematu, więc ta nazwa obok
#: klasy nazwanej znosi całe żądanie: pozycja żądająca w jednym znaczeniu ludzi,
#: a w drugim czegokolwiek, nie żąda niczego.
DOWOLNA = "ALL"

#: Znaczniki żądania, którego plik nie umie nazwać klasą: pierwszy stoi tam, gdzie
#: Walenty żąda zbioru synsetów plWordNetu, drugi tam, gdzie żąda rzeczy stojącej
#: w relacji do argumentu obok. Czemu wychodzą z generatora zamiast milczenia,
#: mówi ``harness/żądania.py``; stoją po stronie czytającego z tego samego powodu,
#: co zdania leksykonu (``olski/walencja.py``). Pisane małymi literami, bo klasy
#: nazwane Walentego są wersalikami i nazwa dopisana tam nie ma tu w co wpaść.
SYNSETY = "synsety"
RELACJA = "relacja"
NIENAZWANE = frozenset({SYNSETY, RELACJA})

#: Klasy, które Walenty stawia tam, gdzie w pozycji ma stanąć ktoś: człowiek,
#: istota żywa oraz podmiot, czyli ten, kto działa jak człowiek, a człowiekiem
#: nie jest — organ, spółka, państwo. Trzy razem, bo pytanie, na które projekt
#: odpowiada deklaracją (``olski/osoby.py``), jest jedno: czy słowo stojące
#: w pozycji nazywa kogoś. Rozdzielenie ich żądałoby taksonomii, a ta jest
#: właśnie tym, czego bez wordnetu nie ma.
OSOBOWE = frozenset({"LUDZIE", "ISTOTY", "PODMIOTY"})

#: Pozycje, których nazwą jest przypadek wypełnienia, czyli te, o które pyta
#: rola nazywająca kilka pozycji naraz (:attr:`olski.parse.Obsada.przypadkowe`).
PRZYPADKI = (BIERNIK, CELOWNIK, DOPEŁNIACZ)


@functools.cache
def _wpisy() -> dict[tuple[str, str], dict[str, frozenset[str]]]:
    """Plik żądań jako klasy po słowie i pozycji.

    Przy pierwszym pytaniu, a nie przy imporcie, bo pyta o niego jedna flaga:
    gramatyka bez leksykonu nie wstaje, a bez tego pliku olski wstaje i milczy.

    Wiersze o jednej pozycji zbierają się w jeden zbiór, bo różni je rola,
    a olski nie ma czym powiedzieć, w którym znaczeniu czasownik stoi.
    Roli ta warstwa przez to nie czyta: nazywa ona pozycję wewnątrz ramy —
    ``Initiator.Source`` jest tym, kto wynajmuje — a autor działa na klasie.
    """
    wpisy: dict[tuple[str, str], dict[str, frozenset[str]]] = {}
    for wiersz in PLIK.read_text(encoding="utf-8").splitlines():
        if wiersz.startswith("#") or not wiersz.strip():
            continue
        lemat, klasa, pozycja, _rola, klasy = wiersz.split("\t")
        pozycje = wpisy.setdefault((lemat, klasa), {})
        pozycje[pozycja] = pozycje.get(pozycja, frozenset()) | _klasy(klasy)
    return wpisy


def _klasy(pole: str) -> frozenset[str]:
    """Kolumna klas jako zbiór; pusta znaczy tyle, co :data:`DOWOLNA`.

    Rama, która nazywa rolę i klasy nie żąda, żąda czegokolwiek,
    a zbiór pusty zniknąłby w sumie po ramach lematu.
    """
    return frozenset(pole.split(",")) if pole else frozenset({DOWOLNA})


def żądane(słowa: Iterable[tuple[str, str]], pozycja: str) -> frozenset[str]:
    """Klasy, których te słowa żądają w tej pozycji; zbiór pusty jest milczeniem.

    Powody milczenia są trzy i rozdzielać ich nie ma po co,
    bo autorowi mówią jedno: nie ma tu czego przeczytać.
    Plik o tym słowie w tej pozycji nie mówi nic;
    albo mówi, że w którymś znaczeniu nie żąda ono niczego (:data:`DOWOLNA`);
    albo żąda samych klas, których nie nazywa (:data:`NIENAZWANE`).

    Znacznik klasy nienazwanej zostaje w odpowiedzi obok klasy nazwanej i wychodzi
    stąd do wydruku, bo kolumna klas jest alternatywą: pozycja żądająca w jednym
    znaczeniu ludzi, a w drugim zbioru synsetów, ludzi nie żąda, więc przemilczana
    połowa tej alternatywy czytałaby się jak żądanie ostrzejsze, niż Walenty stawia.

    Słów jest kilka tam, gdzie formę licencjonuje w jednym kształcie kilka
    odczytań, a odpowiedź jest wtedy sumą i żąda milczenia od każdego z nich:
    czytanie nie mówi, którym z tych słów forma stoi
    (:meth:`olski.parse.Node.signature`),
    więc żądanie jednego z nich byłoby żądaniem postawionym pod monetę.
    """
    zebrane: set[str] = set()
    for słowo in słowa:
        klasy = _wpisy().get(słowo, {}).get(pozycja, frozenset())
        if DOWOLNA in klasy or not klasy - NIENAZWANE:
            return frozenset()
        zebrane |= klasy
    return frozenset(zebrane)


def żąda_osoby(klasy: Iterable[str]) -> bool:
    """Czy tej alternatywy nie spełnia nic poza kimś (:data:`OSOBOWE`).

    Odpowiedź jest połową pytania także tutaj: mówi ona o żądaniu, a o słowie
    stojącym w pozycji orzeka deklaracja projektu (``olski/osoby.py``).

    Klasa nienazwana znosi żądanie w całości, tak samo jak :data:`DOWOLNA`
    w :func:`żądane`, i tym ta odpowiedź jest węższa od wiersza, który klasy
    wypisuje: pozycja żądająca w jednym znaczeniu ludzi, a w drugim zbioru
    synsetów, bywa obsadzona rzeczą i o tej rzeczy plik nie mówi nic.
    """
    zbiór = frozenset(klasy)
    return bool(zbiór) and zbiór <= OSOBOWE
