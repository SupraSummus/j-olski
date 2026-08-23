"""Witryna oddaje werdykt, a odmawia tego, co zajęłoby dyno.

Aplikacja jest funkcją WSGI, więc test podaje jej słownik środowiska i czyta
odpowiedź: portu tu nie ma, serwera pod spodem nie ma, a gunicorn jest
zależnością wdrożenia, nie suity (``docs/witryna.md``).

Suita pilnuje tu tego, co psuje się bez śladu.
Blok JSON-a wklejony do dokumentu rozjeżdża się z każdą zmianą w werdykcie,
tak samo jak blok wydruku pilnowany przez ``tests/test_wydruki.py``.
Adres, o który pyta strona, przestaje istnieć razem z przemianowaną trasą,
a wtedy przeglądarka dostaje 404 i nie mówi tego nikomu poza swoją konsolą.
Ścieżka składana z żądania wypuszcza z dyna pliki, o których nikt nie pytał.
Odmowa bez powodu zostawia stronę z komunikatem, który nic nie mówi.
"""

from __future__ import annotations

import json
import re
import shlex
from io import BytesIO
from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

from witryna.serwer import NAJWIĘCEJ_ZNAKÓW, PLIKI, TRASY, aplikacja

ROOT = Path(__file__).resolve().parent.parent
DOKUMENT = ROOT / "docs" / "witryna.md"
STRONA = ROOT / "witryna" / "strona.html"
#: Adres, po który strona sięga sama: styl i skrypt. Adresu zewnętrznego ten
#: wzorzec nie bierze, bo trasą jest ścieżka zaczynająca się od ukośnika.
ADRES_STRONY = re.compile(r"(?:href|src)=\"(/[^\"]*)\"")
BLOK = re.compile(r"```(sh|json)\n(.*?)```", re.DOTALL)


def wołaj(metoda: str, ścieżka: str, zapytanie: str = "", ciało: str | None = None):
    """Jedno żądanie do aplikacji WSGI; wraca status i ciało odpowiedzi."""
    dane = b"" if ciało is None else ciało.encode("utf-8")
    środowisko = {
        "REQUEST_METHOD": metoda,
        "PATH_INFO": ścieżka,
        "QUERY_STRING": zapytanie,
        "CONTENT_LENGTH": "" if ciało is None else str(len(dane)),
        "wsgi.input": BytesIO(dane),
    }
    zebrane: dict[str, str] = {}

    def odpowiedz(status, nagłówki):
        zebrane["status"] = status
        zebrane["typ"] = dict(nagłówki)["Content-Type"]

    odpowiedź = b"".join(aplikacja(środowisko, odpowiedz))
    return zebrane["status"], zebrane["typ"], odpowiedź


def przez_curl(polecenie: str):
    """Żądanie wzięte z polecenia curla, tak jak stoi w dokumencie.

    Dokument pokazuje wywołanie, którym czytelnik dostanie ten blok JSON-a, więc
    test woła to samo wywołanie, a nie jego przepisanie na argumenty aplikacji.
    """
    tokeny = shlex.split(polecenie)
    adres = next(token for token in tokeny if token.startswith("localhost"))
    ścieżka, _, zapytanie = adres.removeprefix("localhost:8000").partition("?")
    ciało = tokeny[tokeny.index("-d") + 1] if "-d" in tokeny else None
    return wołaj("POST" if ciało else "GET", ścieżka, zapytanie, ciało)


def pary_z_dokumentu():
    """Bloki dokumentu parami: polecenie curla i odpowiedź, którą ma dać."""
    bloki = BLOK.findall(DOKUMENT.read_text(encoding="utf-8"))
    pary = [
        pytest.param(polecenie, odpowiedź, id=polecenie.split("\n")[0][:60])
        for (rodzaj, polecenie), (następny, odpowiedź) in zip(bloki, bloki[1:], strict=False)
        if rodzaj == "sh" and "curl" in polecenie and następny == "json"
    ]
    assert pary, "docs/witryna.md nie ma ani jednej pary polecenia i odpowiedzi"
    return pary


@pytest.mark.parametrize(("polecenie", "oczekiwana"), pary_z_dokumentu())
def test_blok_json_a_w_dokumencie_jest_tym_co_witryna_naprawdę_oddaje(polecenie, oczekiwana):
    status, typ, odpowiedź = przez_curl(polecenie)
    assert status == "200 OK"
    assert typ.startswith("application/json")
    assert json.loads(odpowiedź) == json.loads(oczekiwana)


@pytest.mark.parametrize("adres", sorted(set(ADRES_STRONY.findall(STRONA.read_text()))))
def test_każdy_adres_po_który_strona_sięga_sama_jest_trasą_serwera(adres):
    ścieżka = adres.partition("?")[0]
    assert ("GET", ścieżka) in TRASY, f"strona woła {adres}, a serwer tej trasy nie ma"


@pytest.mark.parametrize(("ścieżka", "typ"), [(k, v[1]) for k, v in PLIKI.items()])
def test_każdy_plik_strony_leży_tam_gdzie_go_serwer_szuka(ścieżka, typ):
    """Przemianowany plik strony daje 500 dopiero na dynie, bo trasa go nie widzi."""
    status, oddany, odpowiedź = wołaj("GET", ścieżka)
    assert (status, oddany) == ("200 OK", typ)
    assert odpowiedź


@pytest.mark.parametrize(
    "ścieżka", ["/../pyproject.toml", "/../../etc/passwd", "/witryna/serwer.py"]
)
def test_ścieżka_z_żądania_nie_wypuszcza_pliku_z_dyna(ścieżka):
    """Pliki są wymienione, a nie składane, i to jest jedyna obrona przed `..`.

    Test broni tej decyzji, a nie kodu: składanie ścieżki z ``PATH_INFO`` jest
    naprawą, na którą ktoś tu kiedyś wpadnie, i wtedy suita ma zrobić się czerwona.
    """
    status, _, odpowiedź = wołaj("GET", ścieżka)
    assert status == "404 Not Found"
    assert "powód" in json.loads(odpowiedź), "odpowiedzią jest odmowa, a nie treść pliku"


def test_tekst_dłuższy_niż_granica_odpada_zamiast_zająć_dyno():
    zdanie = "Zapisz plik konfiguracyjny. "
    tekst = zdanie * (NAJWIĘCEJ_ZNAKÓW // len(zdanie) + 1)
    status, _, odpowiedź = wołaj("POST", "/werdykt", ciało=json.dumps({"tekst": tekst}))
    assert status.startswith("413")
    assert str(NAJWIĘCEJ_ZNAKÓW) in json.loads(odpowiedź)["powód"]


def test_żądanie_bez_długości_odpada_przed_czytaniem_z_gniazda():
    """Czytanie bez granicy jest tym, co dyno zabija, więc brak nagłówka jest odmową."""
    status, _, odpowiedź = wołaj("POST", "/werdykt")
    assert status.startswith("411")
    assert json.loads(odpowiedź)["powód"]


@pytest.mark.parametrize(
    ("ciało", "czego_brakuje"),
    [("nie jest jasonem", "JSON"), ("[]", "tekst"), ('{"text": "Zapisz plik."}', "tekst")],
)
def test_żądanie_bez_tekstu_wraca_z_powodem_a_nie_z_pustką(ciało, czego_brakuje):
    """Powód pokazuje strona, więc odmowa bez powodu jest tu odmową milczącą."""
    status, _, odpowiedź = wołaj("POST", "/werdykt", ciało=ciało)
    assert status.startswith("400")
    assert czego_brakuje in json.loads(odpowiedź)["powód"]


def test_trasa_pytana_niewłaściwą_metodą_mówi_którą_bierze():
    status, _, odpowiedź = wołaj("GET", "/werdykt")
    assert status.startswith("405")
    assert "POST" in json.loads(odpowiedź)["powód"]


def test_makieta_bez_ziarna_oddaje_to_którym_wyszła():
    """Bez tego tekst wylosowany raz nie da się zawołać drugi raz.

    Że ziarno rozstrzyga o tekście, mówi już blok z dokumentu: gdyby losowanie go
    nie czytało, ten blok nie zgadzałby się dwa przebiegi pod rząd.
    """
    _, _, odpowiedź = wołaj("GET", "/makieta")
    dane = json.loads(odpowiedź)
    _, _, drugi = wołaj("GET", "/makieta", zapytanie=f"ziarno={dane['ziarno']}")
    assert json.loads(drugi)["tekst"] == dane["tekst"]
