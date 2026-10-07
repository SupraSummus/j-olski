"""Witryna oddaje werdykt, a odmawia tego, co zajęłoby dyno.

Aplikacja jest funkcją WSGI, więc test podaje jej słownik środowiska i czyta
odpowiedź: portu ani serwera tu nie ma, a gunicorn jest zależnością wdrożenia,
nie suity.
"""

from __future__ import annotations

import json
import re
from io import BytesIO
from pathlib import Path

import pytest

pytest.importorskip("morfeusz2")

from witryna.serwer import NAJWIĘCEJ_ZNAKÓW, PLIKI, TRASY, aplikacja

ROOT = Path(__file__).resolve().parent.parent.parent
STRONA = ROOT / "witryna" / "strona.html"
#: Adres, po który strona sięga sama: styl i skrypt. Adresu zewnętrznego ten
#: wzorzec nie bierze, bo trasą jest ścieżka zaczynająca się od ukośnika.
ADRES_STRONY = re.compile(r"(?:href|src)=\"(/[^\"]*)\"")


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
    """Bez tego tekstu wylosowanego raz nie da się zawołać drugi raz."""
    _, _, odpowiedź = wołaj("GET", "/makieta")
    dane = json.loads(odpowiedź)
    _, _, drugi = wołaj("GET", "/makieta", zapytanie=f"ziarno={dane['ziarno']}")
    assert json.loads(drugi)["tekst"] == dane["tekst"]
