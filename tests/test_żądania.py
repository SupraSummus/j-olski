"""Plik żądań z obu stron: jak się go pisze i co się z niego czyta.

Wydanie TEI wchodzi tu złączeniem trzech warstw (``harness/żądania.py``),
a wychodzi odpowiedzią o jedno słowo w jednej pozycji (``olski/żądania.py``).
Oba pytania stoją w jednym pliku, bo obracają się o jeden plik danych,
i żadne z nich nie dochodzi do analizatora morfologicznego:
o wiersz werdyktu, który tę odpowiedź niesie, pyta ``tests/test_werdykt.py``.

Słownika strona pisząca nie potrzebuje, tak samo jak ``tests/test_walenty.py``:
wpisy pisane tutaj mają kształt wpisu z wydania, przycięty do pól, o które to
czytanie pyta, a plik wejściowy nie stoi w repozytorium.

Złączenie jest tym, co ma tu czym się zepsuć. Wskazanie idzie w spięciu w obie
warstwy naraz, a każde z nich ma własny identyfikator, więc pomyłka o jedno
zagłębienie wiąże rolę z pozycją stojącą obok tej, którą argument obsadza — i
wychodzi z tego wiersz wyglądający jak każdy inny.

Strona czytająca pyta o gotowy ``olski/żądania.txt``, a nie o plik pisany tutaj,
bo o milczeniu rozstrzyga w niej to, co w tamtym pliku naprawdę stoi.
"""

from collections.abc import Iterable, Sequence

import pytest

from harness.żądania import Fraza, pozycja, żądania
from olski.walencja import (
    BEZOKOLICZNIK,
    BIERNIK,
    CELOWNIK,
    CZASOWNIK,
    CZASOWNIK_ZWROTNY,
    DOPEŁNIACZ,
    PODMIOT,
    PYTANIE_ZALEŻNE,
    ZDANIE_PODRZĘDNE,
)
from olski.żądania import SYNSETY, żądane


@pytest.mark.parametrize(
    ("fraza", "podmiotowa", "nazwa"),
    [
        #  Przypadek strukturalny jest w podmiocie mianownikiem, a poza nim
        #  biernikiem, więc ta sama fraza daje dwie różne pozycje.
        (Fraza("np", przypadek="str"), True, PODMIOT),
        (Fraza("np", przypadek="str"), False, BIERNIK),
        (Fraza("np", przypadek="dat"), False, CELOWNIK),
        #  Dopełniacz cząstkowy realizuje polszczyzna tą samą formą co żądany ramą.
        (Fraza("np", przypadek="part"), False, DOPEŁNIACZ),
        #  Narzędnik jest u olskiego pozycją orzecznika, więc argumentu
        #  narzędnikowego nie ma czym nazwać (``olski/walencja.py``).
        (Fraza("np", przypadek="inst"), False, None),
        #  Pozycja podmiotowa obsadzona czym innym niż grupa imienna: zdania w
        #  podmiocie olski nie ma.
        (Fraza("cp", spójnik="że"), True, None),
        (Fraza("np", przypadek="dat"), True, None),
        #  Przyimek zostaje w nazwie, a przypadek nie, bo świadek ramowy dopasowuje
        #  się samym przyimkiem (:data:`harness.walenty.PRZYIMKOWA`).
        (Fraza("prepnp", przyimek="od", przypadek="gen"), False, "prepnp(od)"),
        (Fraza("infp"), False, BEZOKOLICZNIK),
        (Fraza("cp", spójnik="że"), False, ZDANIE_PODRZĘDNE),
        (Fraza("cp", spójnik="int"), False, PYTANIE_ZALEŻNE),
        #  Zdanie spod innego spójnika olski nie ma czym wypisać.
        (Fraza("cp", spójnik="żeby"), False, None),
        #  Okolicznik: pozycji takiej olski nie ma, a przyimka ten kształt nie
        #  nazywa, więc żądanie miejsca zostaje poza plikiem (docstring modułu).
        (Fraza("xp"), False, None),
        (Fraza("lex"), False, None),
        (Fraza("refl"), False, None),
    ],
)
def test_pozycję_nazywa_kształt_frazy_wraz_z_funkcją_pozycji(fraza, podmiotowa, nazwa):
    assert pozycja(fraza, podmiotowa) == nazwa


def _pole(nazwa: str, treść: str) -> str:
    return f'<f name="{nazwa}">{treść}</f>'


def _zbiór(dzieci: Iterable[str]) -> str:
    return f'<vColl org="set">{"".join(dzieci)}</vColl>'


def _fs(typ: str, treść: str = "", identyfikator: str = "") -> str:
    ident = f' xml:id="{identyfikator}"' if identyfikator else ""
    return f'<fs{ident} type="{typ}">{treść}</fs>'


def _symbol(nazwa: str, wartość: str) -> str:
    return _pole(nazwa, f'<symbol value="{wartość}"/>')


def _fraza_np(identyfikator: str, przypadek: str = "str") -> str:
    return _fs("np", _symbol("case", przypadek), identyfikator)


def _pozycja_xml(identyfikator: str, frazy: Sequence[str], podmiotowa: bool = False) -> str:
    funkcja = _symbol("function", PODMIOT) if podmiotowa else ""
    return _fs("position", funkcja + _pole("phrases", _zbiór(frazy)), identyfikator)


def _schemat(pozycje: Sequence[str], opinia: str = "cer", zwrotny: str = "false") -> str:
    return _fs(
        "schema",
        _symbol("opinion", opinia)
        + _pole("reflexive_mark", f'<binary value="{zwrotny}"/>')
        + _pole("positions", _zbiór(pozycje)),
    )


def _argument(
    identyfikator: str, rola: str, klasy: Sequence[str] = (), synsety: bool = False
) -> str:
    grupy = ""
    if klasy:
        grupy += _pole("predefs", _zbiór(f'<symbol value="{klasa}"/>' for klasa in klasy))
    if synsety:
        grupy += _pole("synsets", _zbiór(['<numeric value="1234"/>']))
    preferencje = _pole("sel_prefs", _fs("sel_prefs_groups", grupy)) if grupy else ""
    return _fs("argument", _symbol("role", rola) + preferencje, identyfikator)


def _rama(argumenty: Sequence[str]) -> str:
    return _fs("frame", _pole("arguments", _zbiór(argumenty)))


def _spięcie(argument: str, fraza: str) -> str:
    return _fs(
        "connection",
        _pole("argument", f'<fs sameAs="#{argument}" type="argument"/>')
        + _pole("phrases", _zbiór([f'<fs sameAs="#{fraza}" type="phrase"/>'])),
    )


def _wydanie(
    tmp_path,
    lemat: str,
    schematy: Sequence[str],
    ramy: Sequence[str],
    spięcia: Sequence[str],
    pos: str = "verb",
):
    """Plik wydania o jednym wpisie, złożony z podanych warstw.

    Warstwy chodzą w tym wydaniu razem, więc wpis dostaje wszystkie trzy albo
    żadnej z dwóch (``_wpisy_lematu`` w ``harness/żądania.py``).
    """
    warstwy = (
        _fs("syntactic_layer", _pole("schemata", _zbiór(schematy)))
        + _fs("semantic_layer", _pole("frames", _zbiór(ramy)))
        + _fs(
            "connections_layer",
            _pole(
                "alternations", _zbiór([_fs("alternation", _pole("connections", _zbiór(spięcia)))])
            ),
        )
    )
    plik = tmp_path / "walenty.xml"
    plik.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<TEI xml:lang="pl" xmlns="http://www.tei-c.org/ns/1.0"><text><body>'
        f'<entry xml:id="w1-ent"><form><orth>{lemat}</orth><pos>{pos}</pos></form>'
        f"{warstwy}</entry>"
        "</body></text></TEI>",
        encoding="utf-8",
    )
    return plik


def test_rola_dochodzi_do_tej_pozycji_którą_argument_obsadza(tmp_path):
    """Wiersz mówi o pozycji, więc pomyłka w złączeniu przestawia role między nimi.

    `wynająć` jest tu wpisem, na którym to widać: inicjator w celowniku jest tym,
    komu się wynajmuje, a inicjator pod `od` tym, od kogo, i rozdziela ich samo
    uszczegółowienie roli.
    """
    plik = _wydanie(
        tmp_path,
        "wynająć",
        [
            _schemat(
                [
                    _pozycja_xml("w1.1.1-psn", [_fraza_np("w1.1.1.1-phr")], podmiotowa=True),
                    _pozycja_xml("w1.1.2-psn", [_fraza_np("w1.1.2.1-phr", "dat")]),
                    _pozycja_xml(
                        "w1.1.3-psn",
                        [
                            _fs(
                                "prepnp",
                                _symbol("preposition", "od") + _symbol("case", "gen"),
                                "w1.1.3.1-phr",
                            )
                        ],
                    ),
                ]
            )
        ],
        [
            _rama(
                [
                    _argument("w1.2.1-arg", "Initiator", ["LUDZIE"]),
                    _argument("w1.2.2-arg", "Recipient", ["PODMIOTY"]),
                    _argument("w1.2.3-arg", "Initiator", ["ISTOTY"]),
                ]
            )
        ],
        [
            _spięcie("w1.2.1-arg", "w1.1.1.1-phr"),
            _spięcie("w1.2.2-arg", "w1.1.2.1-phr"),
            _spięcie("w1.2.3-arg", "w1.1.3.1-phr"),
        ],
    )
    assert żądania(plik) == [
        ("wynająć", CZASOWNIK, CELOWNIK, "Recipient", frozenset({"PODMIOTY"})),
        ("wynająć", CZASOWNIK, "prepnp(od)", "Initiator", frozenset({"ISTOTY"})),
        ("wynająć", CZASOWNIK, PODMIOT, "Initiator", frozenset({"LUDZIE"})),
    ]


def test_klasy_jednej_pozycji_zbierają_się_po_wszystkich_ramach_lematu(tmp_path):
    """Zbiór jest alternatywą, bo olski nie wie, w którym znaczeniu czasownik stoi.

    Żądanie synsetowe wchodzi do niego znacznikiem, a nie milczeniem: pozycja
    żądająca w jednym znaczeniu ludzi, a w drugim synsetów, wyglądałaby bez tego
    na żądającą samych ludzi.
    """
    plik = _wydanie(
        tmp_path,
        "znać",
        [_schemat([_pozycja_xml("w1.1.1-psn", [_fraza_np("w1.1.1.1-phr")], podmiotowa=True)])],
        [
            _rama([_argument("w1.2.1-arg", "Experiencer", ["LUDZIE"])]),
            _rama([_argument("w1.3.1-arg", "Experiencer", synsety=True)]),
        ],
        [_spięcie("w1.2.1-arg", "w1.1.1.1-phr"), _spięcie("w1.3.1-arg", "w1.1.1.1-phr")],
    )
    assert żądania(plik) == [
        ("znać", CZASOWNIK, PODMIOT, "Experiencer", frozenset({"LUDZIE", SYNSETY})),
    ]


def test_zwrotność_schematu_rozdziela_wpisy_o_jednym_lemacie(tmp_path):
    """Cząstka `się` czyni z lematu drugie słowo, tak samo jak w leksykonie.

    Wydanie tekstowe pisze ją przy lemacie, a TEI polem schematu, więc klasa
    słowa bierze się tu ze schematu, w którym stoi obsadzona pozycja.
    """
    plik = _wydanie(
        tmp_path,
        "wynająć",
        [
            _schemat([_pozycja_xml("w1.1.1-psn", [_fraza_np("w1.1.1.1-phr", "dat")])]),
            _schemat(
                [_pozycja_xml("w1.2.1-psn", [_fraza_np("w1.2.1.1-phr", "dat")])],
                zwrotny="true",
            ),
        ],
        [_rama([_argument("w1.3.1-arg", "Recipient", ["LUDZIE"])])],
        [_spięcie("w1.3.1-arg", "w1.1.1.1-phr"), _spięcie("w1.3.1-arg", "w1.2.1.1-phr")],
    )
    assert [(lemat, klasa) for lemat, klasa, *_reszta in żądania(plik)] == [
        ("wynająć", CZASOWNIK),
        ("wynająć", CZASOWNIK_ZWROTNY),
    ]


@pytest.mark.parametrize(("opinia", "wierszy"), [("potoczny", 1), ("archaiczny", 0)])
def test_schemat_spoza_tego_rejestru_nie_daje_żądania(tmp_path, opinia, wierszy):
    """Odsiew jest ten sam co w leksykonie i ma tam swojego właściciela.

    Kwalifikator nazywa się w tym wydaniu inaczej — `col` i `dat` w miejsce
    `potoczny` i `archaiczny` — a kryterium jest jedno (:data:`harness.walenty.BRANE`),
    więc przekład nazw stoi tutaj, a wybór nie.
    """
    kwalifikatory = {"potoczny": "col", "archaiczny": "dat"}
    plik = _wydanie(
        tmp_path,
        "abdykować",
        [
            _schemat(
                [_pozycja_xml("w1.1.1-psn", [_fraza_np("w1.1.1.1-phr")], podmiotowa=True)],
                opinia=kwalifikatory[opinia],
            )
        ],
        [_rama([_argument("w1.2.1-arg", "Initiator", ["LUDZIE"])])],
        [_spięcie("w1.2.1-arg", "w1.1.1.1-phr")],
    )
    assert len(żądania(plik)) == wierszy


def test_wpis_niebędący_czasownikiem_nie_wchodzi(tmp_path):
    """Warstwę semantyczną ma w tym wydaniu sam czasownik.

    Rzeczownik stoi w nim ze samą warstwą składniową, więc wpis rzeczownikowy z
    ramą byłby wydaniem innym niż to, o które ten moduł pyta.
    """
    plik = _wydanie(
        tmp_path,
        "informacja",
        [_schemat([_pozycja_xml("w1.1.1-psn", [_fraza_np("w1.1.1.1-phr")], podmiotowa=True)])],
        [_rama([_argument("w1.2.1-arg", "Theme", ["KOMUNIKAT"])])],
        [_spięcie("w1.2.1-arg", "w1.1.1.1-phr")],
        pos="noun",
    )
    assert żądania(plik) == []


# --------------------------------------------------------------------------- #
# Strona czytająca: co gotowy plik odpowiada o jedno słowo w jednej pozycji
# --------------------------------------------------------------------------- #


def test_klasa_nienazwana_zostaje_obok_nazwanej_zamiast_zniknąć():
    """Alternatywa przemilczana czyta się jak żądanie ostrzejsze, niż Walenty stawia.

    `absorbować` żąda w bierniku ludzi albo zbioru synsetów, więc odpowiedź
    o samych ludziach mówiłaby autorowi, że słowo spoza tej klasy stoi w tej
    pozycji błędnie, a Walenty tego o nim nie mówi.
    """
    assert żądane([("absorbować", CZASOWNIK)], BIERNIK) == frozenset({"LUDZIE", SYNSETY})


def test_pozycja_żądająca_samych_klas_nienazwanych_milczy():
    #  Wiersz o niej nie miałby czego powiedzieć: klasę orzeka dopiero wordnet.
    assert żądane([("abdykować", CZASOWNIK)], PODMIOT) == frozenset()


def test_pozycja_niczego_niebędąca_żądaniem_w_jednym_znaczeniu_milczy():
    """Klasa dowolna w jednym znaczeniu znosi żądanie postawione w drugim.

    `akompaniować` żąda w celowniku ludzi albo czegokolwiek, a zdanie o ludziach
    byłoby wtedy zdaniem o jednym ze znaczeń, którego olski nie umie wybrać.
    """
    assert żądane([("akompaniować", CZASOWNIK)], CELOWNIK) == frozenset()


def test_słowo_spoza_pliku_milczy_tak_samo_jak_pozycja_bez_żądania():
    #  Wydanie TEI ma warstwę semantyczną dla części czasowników leksykonu,
    #  i to ona jest głównym powodem milczenia tej warstwy.
    assert żądane([("zapisywać", CZASOWNIK)], PODMIOT) == frozenset()


def test_słowo_milczące_ucisza_żądanie_słowa_obok_siebie():
    """Forma bywa dwoma słowami naraz, a czytanie nie mówi, którym z nich stoi.

    Suma jest odpowiedzią tylko wtedy, gdy żąda każde z nich: przy słowie, o
    którym plik milczy, żądanie drugiego byłoby postawione pod monetę.
    """
    żądające = ("absorbować", CZASOWNIK)
    assert żądane([żądające], PODMIOT)
    assert żądane([żądające, ("zapisywać", CZASOWNIK)], PODMIOT) == frozenset()
