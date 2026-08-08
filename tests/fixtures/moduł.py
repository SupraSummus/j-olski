"""Moduł próbny, po jednym z każdej konstrukcji, którą ekstrakcja rozstrzyga.

Akapit złamany w źródle na dwa wiersze,
bo tak pisze się w tym repozytorium.

Znaczniki reST w wierszu: ``kod``, `nazwa`, :func:`funkcja` i **wyróżnienie**,
a po nich pytajnik tuż za :data:`STAŁA`? Tak.

Lista, której pozycje są zdaniami:

1. Pierwsza pozycja listy, złamana w źródle,
   i ciągnąca się w drugim wierszu.
2. Druga pozycja listy.

Przykład, którego nikt nie czyta jako polszczyzny::

    python3 -m harness.python olski/ --into proza/

Ostatni akapit docstringa.
"""

#: Komentarz z dwukropkiem, którym dokumentujemy stałą,
#: złamany na dwa wiersze.
STAŁA = 1

#  Komentarz narracyjny, pisany od dwóch spacji,
#  i o dwa wiersze dłuższy niż stała pod nim.
#
#  Drugi akapit tego samego komentarza.
INNA = 2

TRZECIA = 3  #  Komentarz dopisany na końcu wiersza, czyli własny akapit.


def funkcja():
    """Docstring funkcji, bo jednostką jest docstring, a nie plik."""
    #  Komentarz w ciele funkcji, wcięty w źródle
    #  i przez to samo niebędący przykładem.
    return STAŁA
