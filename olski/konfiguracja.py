"""Konfiguracja projektu: jeden plik, w którym projekt deklaruje coś olskiemu.

Sekcje są trzy i każda mówi o jednym projekcie, a nie o polszczyźnie:
``leksykon`` deklaruje odmianę słowa, którego słownik nie ma
(``olski/projekt.py``), ``lematy`` mówi, których lematów projekt używa,
a których nie używa wcale (``olski/słownictwo.py``),
a ``osoby`` mówi, które z nich nazywają kogoś (``olski/osoby.py``).
Plik jest jeden, bo projekt jest jedną rzeczą i szukanie go jest jedną regułą;
leży w jego korzeniu, a nie w paczce, bo zainstalowany olski jest jeden dla
wszystkich projektów naraz. Braku nie zgłasza się (:func:`znajdź`).

Format jest TOML-em, bo czyta go biblioteka standardowa (``tomllib`` od 3.11),
więc ani składni, ani jej komunikatów o błędach nie pisze ten moduł.
Nazwy sekcji i kluczy nie mają znaków diakrytycznych i mieć ich nie mogą:
klucz nagi w TOML-u jest ASCII, a klucz cytowany zapraszałby do pomyłki.
Jest to jedyne miejsce, w którym reguła o polskich nazwach
ustępuje formatowi.

Ten moduł zna sam plik i podział na sekcje.
Co znaczy wpis w sekcji, wie ten, kto tę sekcję czyta,
i on zgłasza swoje usterki: struktura jest tutaj, znaczenie tam.
"""

from __future__ import annotations

import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Any

#: Nazwa pliku, w którym projekt deklaruje wszystko, co deklaruje.
NAZWA = "olski.toml"

#: Sekcja, w której projekt deklaruje odmianę słowa spoza słownika.
LEKSYKON = "leksykon"

#: Sekcja, w której projekt orzeka o lematach w obie strony.
LEMATY = "lematy"

#: Sekcja, w której projekt mówi, które lematy nazywają kogoś.
OSOBY = "osoby"

#: Sekcje, które olski czyta. Nazwa spoza tej listy zgłasza się, zamiast
#: przemilczeć deklarację, którą ktoś napisał i której nikt nie przeczytał.
SEKCJE = (LEKSYKON, LEMATY, OSOBY)


class ZłaKonfiguracja(Exception):
    """Konfiguracja, z której nie wychodzi deklaracja, którą obiecuje.

    Wyjątek, a nie wpis pominięty, bo plik pisze się ręką i każda przyczyna jest
    w nim usterką: sekcja nazwana inaczej, klucz nazwany inaczej, wartość o innym
    kształcie. Ruch po zgłoszeniu jest za każdym razem ten sam, czyli poprawiony
    plik, i dlatego klasa jest jedna.

    Od ``ZłyWpis`` w ``olski/projekt.py`` różni się pytaniem: tamten mówi, że
    z poprawnie napisanego wpisu nie wychodzi odmiana, którą on obiecuje.
    """


def znajdź(skąd: Path | None = None) -> Path | None:
    """Konfiguracja projektu, w którym olskiego uruchomiono; ``None``, gdy jej nie ma.

    Szuka się jej od katalogu roboczego w górę, bo projekt ma podkatalogi:
    kto woła olskiego spod ``docs/``, deklaruje wciąż to samo, co spod korzenia.
    """
    katalog = (skąd or Path.cwd()).resolve()
    for miejsce in (katalog, *katalog.parents):
        kandydat = miejsce / NAZWA
        if kandydat.is_file():
            return kandydat
    return None


def czytaj(path: Path) -> dict[str, Mapping[str, Any]]:
    """Konfiguracja z pliku, sprawdzona co do sekcji i niczego poza nimi."""
    with path.open("rb") as plik:
        wczytane = tomllib.load(plik)
    nieznane = sorted(set(wczytane) - set(SEKCJE))
    if nieznane:
        raise ZłaKonfiguracja(
            f"{path}: sekcjami są {', '.join(SEKCJE)}, a nie {', '.join(nieznane)}"
        )
    for nazwa, dane in wczytane.items():
        if not isinstance(dane, Mapping):
            raise ZłaKonfiguracja(f"{path}: sekcja {nazwa} ma być tablicą kluczy")
    return wczytane


def sekcja(
    nazwa: str,
    klucze: tuple[str, ...],
    konfiguracja: Mapping[str, Mapping[str, Any]] | None = None,
) -> Mapping[str, Any]:
    """Jedna sekcja konfiguracji, sprawdzona co do kluczy i niczego poza nimi.

    Klucz nazwany inaczej zgłasza się tutaj, a nie u tego, kto sekcję czyta,
    bo literówka w kluczu jest usterką tego samego rodzaju co literówka w nazwie
    sekcji i czytelnik ma dostać ten sam komunikat.
    """
    dane = (KONFIGURACJA if konfiguracja is None else konfiguracja).get(nazwa, {})
    nieznane = sorted(set(dane) - set(klucze))
    if nieznane:
        raise ZłaKonfiguracja(
            f"sekcja {nazwa}: kluczami są {', '.join(klucze)}, a nie {', '.join(nieznane)}"
        )
    return dane


def napisy(nazwa: str, klucz: str, dane: Mapping[str, Any]) -> frozenset[str]:
    """Wartość klucza jako zbiór napisów; kształt inny zgłasza się.

    Pytają o to dwa klucze sekcji ``lematy`` i pytałby każdy następny,
    więc warunek stoi tu raz.
    """
    wartość = dane.get(klucz, [])
    if not isinstance(wartość, list) or not all(isinstance(item, str) for item in wartość):
        raise ZłaKonfiguracja(f"sekcja {nazwa}: {klucz} ma być listą napisów")
    return frozenset(wartość)


#: Konfiguracja tego projektu, przeczytana przy imporcie.
#: Pusta znaczy projekt bez pliku i jest odpowiedzią zwykłą (:func:`znajdź`).
PLIK = znajdź()
KONFIGURACJA: dict[str, Mapping[str, Any]] = czytaj(PLIK) if PLIK else {}
