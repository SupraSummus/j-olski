"""To repozytorium powiedziane drzewami zamiast zdaniami.

Eksperyment stojący obok ``README.md``, a nie zamiast niego.
Treść, o której tamten plik mówi na wstępie —
dlaczego olski jest podzbiorem, kiedy zdanie jest w nim poprawne,
komu werdykt oddaje wybór i po co ten projekt jest —
stoi tu jako drzewa w kategoriach ``olski.skład.składnia``,
a polski tekst jest tym, co z nich wychodzi.
Wypisuje go ``python3 README.py``.
README repozytorium jest dalej tamten plik i nic tutaj tego nie zmienia.

Napisu tego nie trzyma żaden test, i jest to brak nazwany, a nie przeoczony.
Literał skopiowany z wyjścia zgadza się z nim zawsze i nie orzeka nic,
czego nie orzekł git, a maszyneria pod tymi drzewami ma w ``tests/test_skład.py``
własności nazwane po imieniu — ``opis`` nad postacią w liczbie mnogiej
pod przeczeniem stoi tam wraz z resztą.
Władzę nad napisem ma tekst napisany pierwszy, i tak stoi ``BAZYLISZEK``
w ``tests/test_opowieść.py``, gdzie literał jest celem, a drzewa próbą w niego trafienia.

**Kryterium wyjścia toru składu to nie jest.**
Tamto żąda, żeby każde zdanie ``README.md`` wyszło z drzewa znak w znak,
i trzyma je ``docs/roadmap.md``,
a ten plik oddaje tę samą treść innymi zdaniami, więc go nie zalicza
i nie wolno go za nie brać: porównania słabszego tamta sekcja odmawia z powodem.
Plik jest tym, czym jest ``opowieści/bazyliszek.py``, tylko o czym innym,
i po to samo, co mówi ``opowieści/__init__.py``:
tekst napisany ręcznie w tych kategoriach jest tym jedynym,
co mówi, czego kategoriom brakuje.
Kolejności, którą tamten plik deklaruje, ten nie dochował:
drzewa powstały przed tekstem, a nie po nim,
więc mierzy on, co skład powiedzieć umie, a nie co powiedzieć trzeba.
Odwrócenie tej kolejności, po którym napis dostanie właściciela, trzyma ``TODO.md``.

Brakuje trzech rzeczy i każdą widać w tym, co niżej wyszło inaczej,
niż wyszłoby w prozie.
Lematu ``olski`` Morfeusz nie zna wcale i czyta go jako ``ign``,
więc nazwa własna tego języka nie wyjdzie z drzewa w żadnej roli,
i podmiotem stoi tu gramatyka tam, gdzie ``README.md`` pisze o olskim.
Liczebnika skład nie ma, więc jedno czytanie mówi się tu przez brak drugiego.
Relacji przyczyny nie ma w ``olski/skład/przyimki.py`` ani pod jednym przyimkiem,
a ma ją ``olski/skład/spójniki.py``, więc wychodzi ona zdaniem i nie wychodzi frazą:
przyjemność jest tu orzecznikiem tam, gdzie ``README.md`` pisze ``dla przyjemności``.
Ruch przy każdej z tych trzech trzyma ``TODO.md``.

Część zdań, które stąd wychodzą, parser czyta dwojako,
i nie jest to usterka ani tego pliku, ani tamtego kierunku:
tekst z drzewa jest funkcją, a drzewo z tekstu relacją,
i tyle obiecuje obieg zamknięty w ``docs/design-notes.md``.
"""

from olski.skład import Akapit, Postać
from olski.skład.słownik import A, R, Skąd, V, jest, nie, opis, razem

#: Postaciami jest to, do czego tekst wraca; reszta rzeczy jest wymieniana raz.
#: Tożsamość niesie sama zmienna, więc ``parser`` użyty niżej trzy razy
#: jest w każdym z tych miejsc jednym parserem, a nie trzema.
gramatyka = Postać(R.gramatyka)
maszyna = Postać(R.maszyna)
parser = Postać(R.parser)
skład = Postać(R.skład)

#: Czytania, o których zdanie nie rozstrzyga.
#: Postacią są, bo zdanie opisujące stawia je drugi raz,
#: a ``opis`` rozpoznaje opisywaną rzecz po tożsamości, a nie po lemacie.
czytania = Postać(~R.czytanie)

AKAPITY = (
    #: Po co podzbiór: trudność jest po stronie maszyny, a nie polszczyzny.
    Akapit(
        nie(V.czytać(maszyna, R.polszczyzna)),
        V.opisywać(gramatyka, R.podzbiór / R.polszczyzna),
    ),
    #: Kiedy zdanie jest poprawne i co werdykt z wieloznacznością robi.
    #: Ostatnie zdanie jest tym, po co ten tor jest: wybiera czytelnik.
    Akapit(
        nie(V.mieć(A.poprawny * R.zdanie, A.drugi * R.czytanie)),
        V.nazywać(parser, opis(czytania, nie(V.rozstrzygać(R.zdanie, czytania)))),
        nie(V.wybierać(parser, R.czytanie)),
        V.wybierać(R.czytelnik, R.czytanie),
    ),
    #: Dwa tory i to, że nie napędza ich żadna aplikacja.
    Akapit(
        V.mierzyć(R.repozytorium, razem([gramatyka, skład])),
        V.pisać(skład, R.zdanie, Skąd.z(R.drzewo)),
        jest(R.projekt, R.przyjemność),
    ),
)

#: Czas jest tu teraźniejszy, bo README mówi o tym, co jest, a nie co było.
#: Konstruktora tekstu na ten czas skład nie ma — ``Opowieść`` niesie przeszły
#: i sama mówi, że tamten się doczeka osobnego — więc akapit składa się tu wprost.
CZAS = "teraz"


def kompiluj() -> str:
    """Polski tekst, który wychodzi z drzew tego modułu."""
    return "\n\n".join(akapit.kompiluj(CZAS) for akapit in AKAPITY)


if __name__ == "__main__":
    print(kompiluj())
