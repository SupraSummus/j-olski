"""Dwa mianowniki wydruku tej sondy, bo jeden z nich mówiłby o zasięgu drugi raz.

Kryterium, o które sonda pyta, ma testy tam, gdzie stoi jego właściciel:
`przyimki` w `olski/walenty.py`, a więc w `tests/test_walenty.py`. Tutaj zostaje
to, co jest własnością samej sondy.

Test idzie po wydruku, a nie po przebiegu nad korpusem: Walenty i bank drzew nie
stoją w repozytorium, a odpowiedzi wpisane tutaj ręką są dokładnie tym, co sonda
liczy.
"""

from __future__ import annotations

from sonda.rama import Odpowiedź, render


def test_trafność_liczy_się_z_odpowiedzi_a_zasięg_z_populacji():
    """Dwa mianowniki, bo milczenie jest odpowiedzią o pozycji, a nie o gospodarzu.

    Trafność wzięta z populacji spadałaby wraz z milczeniem, którego świadek nie
    ma czym poprawić, i mówiłaby o zasięgu drugi raz zamiast o pomyłkach.
    """

    def odpowiedź(wskazany: str) -> Odpowiedź:
        return Odpowiedź(
            przyimek="o",
            czasownik="być",
            rzeczownik="informacja",
            wskazany=wskazany,
            wzorcowy="noun",
            fraza=None,
        )

    wydruk = render([odpowiedź("noun"), odpowiedź("clause"), odpowiedź(""), odpowiedź("")])
    assert "4 spornych przyłączeń" in wydruk
    assert "50.0% zasięg" in wydruk
    assert "50.0% trafność" in wydruk
