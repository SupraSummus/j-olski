"""Lematy, o które pyta więcej niż jedna warstwa.

Wpis należy tutaj wtedy, gdy o ten sam napis pyta gramatyka oraz warstwa poza nią:
terminal bierze lemat, a warunek gdzie indziej porównuje ten sam napis
z czytaniem formy albo z lematem gospodarza
(``olski/segmentacja.py``, ``olski/werdykt/``, ``olski/rozstrzyganie.py``).
Kopia druga rozjeżdża się po cichu, bo napisu z napisem nie porównuje żaden test.
Obok takiego lematu wpisujemy ten, który mu się przeciwstawia,
choćby pytała o niego jedna warstwa:
znaki cytowania spoza rejestru mówią, którą parę rejestr wybrał,
a rozdzielone z tą parą przestają to mówić.

Moduł ten leży poniżej gramatyki i nic z niej nie czyta.
``olski/subset/`` buduje ją przy imporcie,
więc kto sięgałby po lemat tam, płaciłby za całą gramatykę i za leksykon walencyjny.
Lemat, o który pyta sama gramatyka, zostaje przy swoim terminalu w tamtym module.
"""

from __future__ import annotations

#: Rozdzielające `a`, czyli to z `dwa bilety a pięć złotych`: Morfeusz daje mu
#: czytanie przyimka rządzącego mianownikiem, a wyrażenie przyimkowe olskiego tego
#: czytania nie bierze, bo bez tego warunku każde `, a` wychodzi okolicznikiem
#: wysuniętym zdania po przecinku, którego podmiot w mianowniku właśnie stoi.
#: Warunek pada na lemat, a nie na przypadek; czego kryterium na przypadek zabrałoby
#: razem z nim, wywodzi docs/subset.md, i ono trzyma też cenę.
PRZYIMEK_ROZDZIELAJĄCY = "a"

#: Znaki, którymi ten rejestr obejmuje tytuł i termin cytowany: `„Zasady
#: techniki prawodawczej”`. Znaki są dwa i są różne, bo polszczyzna otwiera
#: cudzysłów innym znakiem, niż go zamyka.
#: Pyta o nie terminal (``olski/subset/słowa.py``), warunek, którym cudzysłów
#: licencjonuje napis przytoczony (``olski/segmentacja.py``),
#: oraz poprawka, którą werdykt daje zdaniu cytującemu innymi (``olski/werdykt/odrzucone.py``).
ZNAK_CUDZYSŁOWU_OTWIERAJĄCY = "„"
ZNAK_CUDZYSŁOWU_ZAMYKAJĄCY = "”"

#: Znaki, którymi cytuje się poza tym rejestrem: cudzysłów maszynowy, pojedynczy,
#: angielski i ostrokątny. Gramatyka bierze samą parę wyżej, a zdanie cytujące
#: którymkolwiek z tych znaków werdykt przecytowuje nią i pyta o nie gramatykę
#: drugi raz (``_cudzysłów`` w ``olski/werdykt/odrzucone.py``).
ZAMIENNIKI_CUDZYSŁOWU = ('"', "'", "‘", "’", "‚", "“", "«", "»")

#: Znaki myślnika: pauza i półpauza. Polszczyzna rozdziela nimi zdanie, a łącznik
#: spaja jej wewnątrz wyrazu. Ten rejestr pisze przy tym myślnik także łącznikiem,
#: i rozstrzyga to warstwa morfologiczna, bo tylko ona widzi spacje wokół znaku
#: (``olski/segmentacja.py``); terminal pyta o sam lemat (``olski/subset/słowa.py``).
ZNAK_MYŚLNIKA = "—"
ZNAK_PÓŁPAUZY = "–"

#: Cząstka przecząca jako lemat, bo pyta o nią terminal, którym olski przeczy,
#: wykluczenie w klasie spójników bez przecinka (``olski/subset/słowa.py``)
#: oraz warstwa nad plikiem żądań: pod przeczeniem dopełnienie w bierniku staje
#: w dopełniaczu, więc przypadek wypełnienia nazywa wtedy dwie pozycje ramy naraz
#: (``olski/żądania.py``).
LEMAT_PRZECZENIA = "nie"

#: Lemat cząstki czasownika zwrotnego. Leksykon czyta tę cząstkę jako drugi wymiar
#: lematu, a nie jako określenie: `otwierać` bierze dopełnienie w bierniku,
#: a `otwierać się` go nie bierze.
#: Pyta o niego terminal cząstki wraz z klasami walencyjnymi (``olski/subset/słowa.py``),
#: warunek na pozycję tej cząstki (``olski/segmentacja.py``)
#: oraz warstwa nad plikiem żądań, bo czasownik z cząstką jest tam innym słowem
#: (``olski/żądania.py``).
LEMAT_ZWROTNY = "się"
