"""Bazyliszek warszawski, opowiedziany drzewami zamiast zdaniami.

Legenda o potworze z piwnicy, o córce krawca, która zeszła tam ze świecą,
i o czeladniku, który zszedł tam z lustrem,
stoi tu jako drzewa w kategoriach ``skład.składnia``,
a polski tekst jest tym, co z nich wychodzi.
Dziewiętnaście zdań tej wersji trzyma ``tests/test_opowieść.py``,
znak w znak z tym, co ten moduł wypuszcza.

Legendę tę Warszawa opowiada w wielu wersjach
i żadna z nich nie stoi tu jako źródło:
opowieść jest wymyślona pod ten plik, bo mierzy się nią kompilator, a nie podanie.
Zakończenie, które nie mówi, o czym opowieść była, jest w niej wyborem,
a nie tym, co po skracaniu zostało,
i katalog, z którego ten wybór wyszedł, trzyma ``docs/fiction.md``.

Po co ten plik jest, mówi ``opowieści/__init__.py``,
a co z niego widać na kompilatorze i czego on od niego zażądał, mówi
``docs/design-notes.md``.
"""

from skład import Akapit, Opowieść, Postać
from skład.słownik import (
    A,
    Dokąd,
    Gdzie,
    Kiedy,
    Którędy,
    R,
    Skąd,
    V,
    czym,
    nie,
    nowe,
    opis,
    razem,
    temat,
)

#: Postaciami jest to, do czego opowieść wraca; reszta rzeczy jest wymieniana raz.
#: Tożsamość niesie sama zmienna, więc ``bazyliszek`` użyty niżej dwa razy
#: jest w obu miejscach jednym bazyliszkiem, a nie dwoma.
#: Człowiekiem być przy tym nie trzeba: świeca zapalona i świeca zgasła
#: są tą samą świecą, a kamienne postaci są jednym zbiorem widzianym dwa razy.
bazyliszek = Postać(R.bazyliszek)
mieszczanie = Postać(~R.mieszczanin)
córka_krawca = Postać(R.córka / R.krawiec)
czeladnik = Postać(R.czeladnik)
świeca = Postać(R.świeca)
kamienne_postaci = Postać(A.kamienny * ~R.postać)

#: Poddrzewo, które stoi w opowieści dwa razy.
#: Zmienna oszczędza tu powtórzenie, a nie niesie tożsamość:
#: wzrok potwora jest za każdym razem tym samym wzrokiem, bo tyle znaczy opis.
wzrok_potwora = R.wzrok / R.potwór


def zamienia_w_kamień(czyn, kto, kogo):
    """Zdanie o tym, co obraca w kamień, i o tym, kogo obraca.

    Funkcja stoi tu, bo to zdanie pada w opowieści dwa razy
    i za drugim razem jest jej puentą:
    zamienia ten sam wzrok, a zamienionym okazuje się ten, do kogo należał.
    Czasownik jest argumentem, bo aspekt jest znaczeniem, a nie formą:
    raz mowa o tym, co działo się stale, a raz o tym, co stało się raz.
    """
    return czyn(kto, kogo, Dokąd.w(R.kamień))


def schodzi_do_piwnicy(kto):
    """Dwa zdania o tym, jak się tam wchodzi, bo drzwi są zabite.

    Funkcja zwraca listę, więc jedno wywołanie dokłada do akapitu dwa zdania.
    Wywołań jest dwa i to one są tu treścią, a nie oszczędnością:
    czeladnik schodzi na dół tak samo jak dziewczyna, której szuka,
    i tyle wystarcza, żeby czytelnik wiedział, czym to się skończyło.
    Podmiot stoi w obu zdaniach, a w tekście wyjdzie raz,
    bo o opuszczeniu rozstrzyga akapit, a nie ten, kto zdania pisze.
    """
    return [
        V.podnieść(kto, R.deska),
        V.zejść(kto, Którędy.po(~R.schody)),
    ]


def zabijają_wejście(deski):
    """Zdanie o tym, co miasto robi z piwnicą, powiedziane dwa razy o różnych deskach.

    Deski są argumentem, bo to w nich jest cała różnica między początkiem a końcem:
    drugi raz są nowe, a poza tym nie stało się nic.
    """
    return V.zabić(mieszczanie, razem([~R.okno, ~R.drzwi]), czym(deski))


OPOWIEŚĆ = Opowieść(
    Akapit(
        V.mieszkać(nowe(bazyliszek), temat(Gdzie.w(R.piwnica / (A.stary * R.kamienica)))),
        zamienia_w_kamień(V.zamieniać, wzrok_potwora, ~R.człowiek),
        V.stać(
            opis(kamienne_postaci, nie(V.liczyć(R.nikt, kamienne_postaci))),
            Gdzie.pod(R.ściana),
        ),
        zabijają_wejście(~R.deska),
    ),
    Akapit(
        V.zapalić(córka_krawca, świeca, temat(Kiedy.w(R.noc))),
        schodzi_do_piwnicy(córka_krawca),
        V.zgasnąć(świeca),
        nie(V.wrócić(córka_krawca)),
    ),
    Akapit(
        V.wziąć(
            opis(czeladnik, V.znać(czeladnik, córka_krawca)),
            nowe(A.duży * R.lustro),
            Skąd.z(R.warsztat),
        ),
        schodzi_do_piwnicy(czeladnik),
        V.zasłonić(czeladnik, R.twarz, czym(R.lustro)),
        V.otworzyć(bazyliszek, ~R.oko),
        V.zobaczyć(bazyliszek, A.własny * R.odbicie),
        zamienia_w_kamień(V.zamienić, wzrok_potwora, bazyliszek),
    ),
    Akapit(
        V.poznać(czeladnik, córka_krawca, Gdzie.wśród(kamienne_postaci)),
        nie(V.wynieść(czeladnik, nowe(R.lustro), Skąd.z(R.piwnica))),
        zabijają_wejście(A.nowy * ~R.deska),
    ),
)


if __name__ == "__main__":
    print(OPOWIEŚĆ.kompiluj())
