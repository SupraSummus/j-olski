"""API nad gramatyką i strona, która je woła: jedna aplikacja WSGI.

Ramy tu nie ma, bo cała warstwa HTTP mieści się w tablicy tras, w jednym typie
odpowiedzi i w jednym wyjątku na odmowę. Zależnością wykonawczą zostaje sam
serwer, który tę aplikację woła — gunicorn na dynie, ``wsgiref`` na klonie
(``witryna/__main__.py``) — a suita nie woła żadnego z nich, bo aplikacja WSGI
jest funkcją. Cały ten wywód wraz z warunkiem, który go odwraca, stoi w
``docs/witryna.md``, i tam też stoi powód, dla którego API oddaje dane, a nie
fragmenty HTML.

Granice są dwie i obie są granicami dyna:
tekst wchodzi przycięty do :data:`NAJWIĘCEJ_ZNAKÓW`, a ścieżka do pliku nie
wychodzi z żądania, bo pliki są wymienione w :data:`PLIKI`.
"""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs

from witryna.werdykty import makieta, zbadaj

#: Ile znaków bierze jedno żądanie. Dyno oddaje odpowiedź jednym procesem, więc
#: granica ta jest tym, co dzieli akapit do sprawdzenia od cudzego korpusu
#: wklejonego w to samo pole. Najgorsze zdania tej długości idą pod sekundę.
NAJWIĘCEJ_ZNAKÓW = 4000

#: Ile bajtów wolno przeczytać z gniazda. Znak polski waży w UTF-8 dwa bajty,
#: a cudzysłów w JSON-ie sześć, więc zapas jest tu na kopertę, a nie na tekst:
#: żądanie dłuższe odpada przed dekodowaniem, czyli przed przydzieleniem pamięci.
NAJWIĘCEJ_BAJTÓW = NAJWIĘCEJ_ZNAKÓW * 6 + 512

STRONA = Path(__file__).parent

#: Pliki, które przeglądarka bierze wprost, wraz z typem, którym się przedstawiają.
#: Ścieżki są wymienione, a nie składane z żądania, więc ``..`` nie ma tu czego
#: przejść: żądanie wybiera z tej tablicy albo nie wybiera niczego.
PLIKI = {
    "/": ("strona.html", "text/html; charset=utf-8"),
    "/styl.css": ("styl.css", "text/css; charset=utf-8"),
    "/skrypt.js": ("skrypt.js", "text/javascript; charset=utf-8"),
}


@dataclass(frozen=True)
class Odpowiedź:
    """Jedna odpowiedź HTTP, zanim WSGI rozłoży ją na wywołania."""

    status: str
    typ: str
    ciało: bytes


class Odmowa(Exception):
    """Żądanie, na które nie ma odpowiedzi, wraz ze statusem, który to mówi.

    Wyjątek, a nie wartość, bo odmowa wychodzi z głębi czytania żądania — z
    długości, z JSON-a, z liczby — a żadne z tych miejsc nie ma czym odpowiedzieć.
    """

    def __init__(self, status: str, powód: str) -> None:
        super().__init__(powód)
        self.status = status
        self.powód = powód


def aplikacja(środowisko: dict, odpowiedz: Callable) -> Iterable[bytes]:
    """Aplikacja WSGI, czyli to, co woła gunicorn na dynie."""
    odpowiedź = _odpowiedź(środowisko)
    odpowiedz(
        odpowiedź.status,
        [
            ("Content-Type", odpowiedź.typ),
            ("Content-Length", str(len(odpowiedź.ciało))),
            #  Strona i skrypt jadą pod stałymi adresami, więc przeglądarka
            #  trzymająca je bez pytania pokazywałaby po wdrożeniu wersję sprzed.
            ("Cache-Control", "no-cache"),
        ],
    )
    return [odpowiedź.ciało]


def _odpowiedź(środowisko: dict) -> Odpowiedź:
    ścieżka = środowisko.get("PATH_INFO") or "/"
    metoda = środowisko.get("REQUEST_METHOD", "GET")
    try:
        trasa = TRASY.get((metoda, ścieżka))
        if trasa is None:
            raise _nie_ta_trasa(metoda, ścieżka)
        return trasa(środowisko)
    except Odmowa as odmowa:
        return _json(odmowa.status, {"powód": odmowa.powód})


def _nie_ta_trasa(metoda: str, ścieżka: str) -> Odmowa:
    """Odmowa nad ścieżką, której nie ma, albo nad metodą, której ta ścieżka nie bierze."""
    metody = sorted({inna for inna, znana in TRASY if znana == ścieżka})
    if metody:
        return Odmowa("405 Method Not Allowed", f"{ścieżka} bierze {' i '.join(metody)}")
    return Odmowa("404 Not Found", f"nie ma tu {ścieżka}")


def _plik(nazwa: str, typ: str) -> Callable[[dict], Odpowiedź]:
    """Trasa oddająca plik strony.

    Plik czyta się na żądanie, bo waży kilobajty, a wzięty przy imporcie kazałby
    restartować proces po każdej edycji strony.
    """
    return lambda _: Odpowiedź("200 OK", typ, (STRONA / nazwa).read_bytes())


def _werdykt(środowisko: dict) -> Odpowiedź:
    #  Granicę oddaje się razem z werdyktem, bo strona liczy przy niej znaki, a
    #  wpisana w skrypcie byłaby drugą kopią tej liczby i rozjechałaby się cicho.
    return _json("200 OK", zbadaj(_tekst(środowisko)) | {"granica_znaków": NAJWIĘCEJ_ZNAKÓW})


def _makieta(środowisko: dict) -> Odpowiedź:
    zapytanie = parse_qs(środowisko.get("QUERY_STRING", ""))
    return _json(
        "200 OK",
        makieta(_liczba(zapytanie, "ziarno", None), _liczba(zapytanie, "akapity", 1)),
    )


def _tekst(środowisko: dict) -> str:
    """Tekst do sprawdzenia, wyjęty z ciała żądania, albo odmowa z powodem."""
    surowa = środowisko.get("CONTENT_LENGTH") or ""
    if not surowa.isdigit():
        raise Odmowa("411 Length Required", "żądanie podaje się z Content-Length")
    długość = int(surowa)
    #  Dwa razy to samo pytanie, bo bajty odmawiają przed przydzieleniem pamięci,
    #  a znaki po dekodowaniu: nagłówek mówi o kopercie, a granica jest o tekście.
    if długość > NAJWIĘCEJ_BAJTÓW:
        raise _za_długie()
    try:
        żądanie = json.loads(środowisko["wsgi.input"].read(długość) or b"{}")
    except (UnicodeDecodeError, json.JSONDecodeError) as błąd:
        raise Odmowa("400 Bad Request", f"ciało nie jest JSON-em: {błąd}") from błąd
    tekst = żądanie.get("tekst") if isinstance(żądanie, dict) else None
    if not isinstance(tekst, str):
        raise Odmowa("400 Bad Request", "żądanie podaje tekst pod kluczem „tekst”")
    if len(tekst) > NAJWIĘCEJ_ZNAKÓW:
        raise _za_długie()
    return tekst


def _za_długie() -> Odmowa:
    """Odmowa nad tekstem ponad granicę; powód pokazuje strona, więc jest jeden."""
    return Odmowa("413 Content Too Large", f"witryna bierze {NAJWIĘCEJ_ZNAKÓW} znaków naraz")


def _liczba(zapytanie: dict[str, list[str]], nazwa: str, domyślna: int | None) -> int | None:
    """Liczba z zapytania, wraz z odmową nad tym, co liczbą nie jest."""
    wartości = zapytanie.get(nazwa)
    if not wartości or not wartości[0]:
        return domyślna
    try:
        return int(wartości[0])
    except ValueError as błąd:
        raise Odmowa("400 Bad Request", f"{nazwa} jest liczbą, a nie „{wartości[0]}”") from błąd


def _json(status: str, dane: dict) -> Odpowiedź:
    ciało = json.dumps(dane, ensure_ascii=False, indent=1).encode("utf-8")
    return Odpowiedź(status, "application/json; charset=utf-8", ciało)


#: Trasa na parę metody i ścieżki. Tablica zamiast drzewa warunków, bo pytanie o
#: metodę niedozwoloną czyta z niej odpowiedź, zamiast mieć na to własną gałąź.
TRASY: dict[tuple[str, str], Callable[[dict], Odpowiedź]] = {
    **{("GET", ścieżka): _plik(*plik) for ścieżka, plik in PLIKI.items()},
    ("POST", "/werdykt"): _werdykt,
    ("GET", "/makieta"): _makieta,
}
