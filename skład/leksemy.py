"""Który leksem stoi pod nazwą: leksykon nazw nad identyfikatorami SGJP.

Lemat leksemu nie wskazuje, a słownik leksemy rozdziela.
Pod napisem ``oko`` stoją dwa i jeden z nich ma liczbę mnogą ``oczy``,
a drugi ``oka``.
Pod ``Włochy`` także dwa, a są nimi kraj wraz z miejscownikiem ``Włoszech``
oraz dzielnica Warszawy wraz z ``Włochach``.
Który z nich, jest pytaniem o rzecz, o której autor pisze,
więc odpowiedź stoi tutaj, a nie w kolejności, w jakiej słownik wydaje formy.
Identyfikatory, którymi słownik je rozdziela, stoją niżej w ``LEKSEMY``,
bo pisze się je do kodu, a nie do zdania.

Wpis robi dwie rzeczy, a jest to jedna rzecz widziana z dwóch stron.
Nazwa osobna daje osobnej rzeczy osobne miejsce w drzewie:
``oko_w_rosole`` odmienia się jak ``oko`` niezbiorowe,
więc autor pisze nim to, czego przez ``oko`` nie powie.
Nazwa goła rozstrzyga, czym samo ``oko`` jest w tym repozytorium,
i po to jest, żeby ``odmień`` nie wybierał w milczeniu.

Nazwy, której tu nie ma, ten plik nie zabrania.
Idzie ona do słownika jako lemat, tak jak szła przedtem,
a identyfikator wolno postawić wprost w konstruktorze ``Rzecz``,
bo słownik odmienia i po nim, choć przestrzeń nazw ``R`` dwukropka nie zapisze.
Wpisu żąda dokładnie jeden przypadek i pilnuje tego ``odmień``:
leksemy jednego lematu, które w żądanej komórce nie zgadzają się co do formy.

Świadka ma ten plik w słowniku i jest to świadek połowy wpisu.
Leksem, którego SGJP nie zna, nie ma ani jednej formy,
więc literówka w identyfikatorze zgłasza się w ``tests/test_leksemy.py``,
a nie na zdaniu, które z tego wpisu wyjdzie.
Czego świadek nie sprawdza, jest doborem, tak jak w ``skład/przyimki.py``:
że goła nazwa ``oko`` znaczy oko, a nie oczko w sieci,
rozstrzyga ten plik i nic poza nim.
"""

from __future__ import annotations

#: Leksem, o który idzie autorowi, gdy pisze tę nazwę.
#: Nazwa goła stoi tu wtedy, gdy leksemy jednego lematu nie zgadzają się
#: co do formy, bo tylko wtedy jest co rozstrzygać.
LEKSEMY: dict[str, str] = {
    "Włochy": "Włochy:Sn_pt~szech",
    "oko": "oko:Sn_col",
    "oko_w_rosole": "oko:Sn_ncol",
}


def leksem(nazwa: str) -> str:
    """Identyfikator leksemu, którym ta nazwa jest, albo nazwa nietknięta.

    Milczenie leksykonu jest tu zgodą na to, co słownik ma pod tym napisem,
    a nie brakiem wiedzy, i tym ten plik różni się od ``skład/przyimki.py``:
    tamten milczy o przyimku, którego nie zna, i milczenie zgłasza wyjątkiem,
    a tutaj większość nazw jest lematami o jednym leksemie
    i wpis byłby dla nich powtórzeniem napisu.
    """
    return LEKSEMY.get(nazwa, nazwa)
