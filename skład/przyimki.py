"""Czym rządzi przyimek: mały leksykon czytany przez okolicznik.

Przypadek po przyimku jest faktem o przyimku, a nie o zdaniu, w którym stoi,
więc stoi w leksykonie, tak jak rama czasownika stoi w ``olski/walencja.py``.

Klucz jest parą, bo sam przyimek przypadka nie wyznacza:
``w piwnicy`` mówi, gdzie coś jest, a ``w kamień`` mówi, w co się coś zamienia.
Rozstrzyga między nimi relacja, którą autor postawił w drzewie,
a relacja jest kategorią dziedziny, a nie polszczyzny:
drzewo mówi, że coś jest celem, a nie że stoi tam biernik.
Para taka jest całym powodem, dla którego okolicznik niesie relację,
bo przyimek biorący jeden przypadek dałby się opisać samym napisem.

Relacji jest przy tym więcej niż przypadków, które one rozdzielają,
i widać to na tym samym przyimku: ``w nocy`` stoi w miejscowniku jak ``w piwnicy``,
a mówi, kiedy, a nie gdzie.
Wpis, który przypadka nie zmienia, jest tu wpisem mimo to,
bo relacja nazywa to, co autor powiedział, a nie to, w czym mu to wyjdzie.

Wpis pisany jest ręcznie, tak samo jak w ``skład/spójniki.py``,
czyli w tym pliku, który to samo mówi o okoliczności wyrażonej zdarzeniem.
Walenty opisuje czasowniki, a nie przyimki, więc nie ma stąd czego wygenerować.
Połowa wpisu ma jednak świadka w słowniku:
Morfeusz znakuje przyimek przypadkami, którymi ten przyimek rządzi,
więc przypadek wypisany tutaj przy przyimku, który go nie bierze,
zgłasza się w ``tests/test_przyimki.py``.
Czego ten świadek nie sprawdza, jest doborem:
który z przypadków należy się której relacji, rozstrzyga ten plik i nic poza nim.

Przyimka w postaci zgłoskotwórczej — ``we``, ``ze``, ``pode`` — ten leksykon nie ma,
więc ``we Wrocławiu`` z drzewa nie wyjdzie; trzyma to ``TODO.md``.
"""

from __future__ import annotations

#: Przypadek, którego żąda przyimek postawiony w danej relacji.
#: Pusty napis jest przyimkiem żadnym, bo narzędzie polszczyzna wyraża
#: samym narzędnikiem, a rola bez przyimka jest tu tym samym, co rola z nim.
PRZYIMKI: dict[tuple[str, str], str] = {
    ("", "narzędzie"): "inst",
    ("do", "cel"): "gen",
    ("na", "cel"): "acc",
    ("na", "miejsce"): "loc",
    ("od", "źródło"): "gen",
    ("po", "droga"): "loc",
    ("pod", "cel"): "acc",
    ("pod", "miejsce"): "inst",
    ("przed", "miejsce"): "inst",
    ("w", "cel"): "acc",
    ("w", "czas"): "loc",
    ("w", "miejsce"): "loc",
    ("wśród", "miejsce"): "gen",
    ("z", "źródło"): "gen",
}


def przypadek(przyimek: str, relacja: str) -> str | None:
    """Przypadek, w którym staje grupa imienna po tym przyimku w tej relacji.

    Milczenie leksykonu jest tu brakiem wiedzy, a nie ramą domyślną,
    i tym ten plik różni się od ``olski/leksykon.txt``:
    tamten wylicza wyjątki od ramy, którą ma większość czasowników,
    a przyimków jest tyle, że wyliczyć da się je wszystkie.
    Odpowiedzią na milczenie jest ``None``, a nie wyjątek,
    bo zgłasza je konstruktor okolicznika w ``skład/składnia.py``,
    czyli to samo miejsce, w którym zgłasza się rama czasownika,
    i po to, żeby drzewo błędne nie powstało zamiast zgłosić się przy wypisywaniu.
    """
    return PRZYIMKI.get((przyimek, relacja))
