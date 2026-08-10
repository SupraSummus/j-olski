"""Bazyliszek warszawski, opowiedziany drzewami zamiast zdaniami.

Legenda o potworze z piwnicy, o córce krawca, która zeszła tam po kufer,
i o czeladniku, który zszedł tam z lustrem,
stoi tu jako drzewa w kategoriach ``skład.składnia``,
a polski tekst jest tym, co z nich wychodzi.
Tekst ten trzyma ``tests/test_opowieść.py``,
znak w znak z tym, co ten moduł wypuszcza.

Legendę tę Warszawa opowiada w wielu wersjach
i żadna z nich nie stoi tu jako źródło:
opowieść jest wymyślona pod ten plik, bo mierzy się nią kompilator, a nie podanie.
Zakończenie, które nie mówi, o czym opowieść była, jest w niej wyborem,
a nie tym, co po skracaniu zostało,
i katalog, z którego ten wybór wyszedł, trzyma ``docs/fiction.md``.

Dwie rzeczy w tej wersji niesie sama wola, a nie zdanie o kimś.
Córka krawca chce wynieść kufer i to jest jej powód zejścia,
a czeladnik chce zejść tam, gdzie nie chce zejść nikt,
i to jest wszystko, co opowieść mówi o tym, jaki jest.
Czasownik ``wynieść`` domyka przy tym opowieść:
otwiera ją rzecz, którą ktoś chciał wynieść, a zamyka rzecz, której nikt nie wyniósł.

Po co ten plik jest, mówi ``opowieści/__init__.py``,
a co z niego widać na kompilatorze i czego on od niego zażądał, mówi
``docs/design-notes.md``.
"""

from skład import Akapit, Opowieść, Postać
from skład.słownik import (
    A,
    Czym,
    D,
    Dlaczego,
    Dokąd,
    Gdzie,
    Kiedy,
    Którędy,
    R,
    Skutek,
    Skąd,
    V,
    nie,
    opis,
    potem,
    razem,
    remat,
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

#: Nikt, czyli rzecz, którą opowieść wymienia dwa razy i o której nie mówi.
#: Postacią to nie jest i być nie może: postać jest kimś, do kogo tekst wraca,
#: a tu nie ma do kogo wracać.
#: Zmienna jest tu mimo to potrzebna, i to jest ta sama potrzeba,
#: którą ma ``opis``: bezokolicznik żąda tego samego obiektu w dwóch miejscach,
#: bo o wykonawcy rozstrzyga zmienna, a nie lemat.
nikt = R.nikt


def zamienia_w_kamień(czyn, kto, kogo, *reszta):
    """Zdanie o tym, co obraca w kamień, i o tym, kogo obraca.

    Funkcja stoi tu, bo to zdanie pada w opowieści dwa razy
    i za drugim razem jest jej puentą:
    zamienia ten sam wzrok, a zamienionym okazuje się ten, do kogo należał.
    Czasownik jest argumentem, bo aspekt jest znaczeniem, a nie formą:
    raz mowa o tym, co działo się stale, a raz o tym, co stało się raz.
    """
    return czyn(kto, kogo, Dokąd.w(R.kamień), *reszta)


def schodzi_do_piwnicy(kto):
    """Zdanie o tym, jak się tam wchodzi, bo drzwi są zabite.

    Wywołań jest dwa i to one są tu treścią, a nie oszczędnością:
    czeladnik schodzi na dół tak samo jak dziewczyna, której szuka,
    i tyle wystarcza, żeby czytelnik wiedział, czym to się skończyło.
    Podmiot stoi w obu zdarzeniach, a w tekście wyjdzie raz,
    bo o tym rozstrzyga ciąg, a nie ten, kto zdarzenia pisze.
    """
    return potem(
        V.podnieść(kto, R.deska),
        V.zejść(kto, Którędy.po(~R.schody)),
    )


def zabijają_wejście(deski):
    """Zdanie o tym, co miasto robi z piwnicą, powiedziane dwa razy o różnych deskach.

    Deski są argumentem, bo to w nich jest widoczna różnica między początkiem a końcem:
    drugi raz są nowe, a poza tym nie stało się nic.
    Za pierwszym razem to zdanie stoi jako skutek cudzego zdania, a za drugim samo,
    i to jest tu echo: miasto robi to samo, a nie mówi już, przed czym.
    """
    return V.zabić(mieszczanie, razem([~R.okno, ~R.drzwi]), Czym(deski))


def chce_zejść(kto):
    """Zdanie o woli, a nie o zejściu, powiedziane dwa razy o dwóch różnych ludziach.

    Wywołań jest dwa i to one są tu treścią, tak samo jak przy schodzeniu wyżej,
    tylko że tamte dwa są echem, a te dwa kontrastem:
    nikt nie chce zejść, a czeladnik chce, i tyle wystarcza,
    żeby o czeladniku nie trzeba było mówić, jaki jest.
    Wykonawca stoi w tym zdaniu dwa razy, a w tekście wyjdzie raz,
    bo bezokolicznik podmiotu nie ma i bierze go z czasownika nad sobą.
    """
    return V.chcieć(kto, V.zejść(kto, Dokąd.do(R.piwnica)))


OPOWIEŚĆ = Opowieść(
    Akapit(
        V.mieszkać(remat(bazyliszek), temat(Gdzie.w(R.piwnica / (A.stary * R.kamienica)))),
        zamienia_w_kamień(
            V.zamieniać,
            wzrok_potwora,
            ~R.człowiek,
            Skutek.więc(zabijają_wejście(~R.deska)),
        ),
        V.stać(
            remat(opis(kamienne_postaci, nie(V.liczyć(nikt, kamienne_postaci)))),
            temat(Gdzie.pod(R.ściana)),
        ),
    ),
    Akapit(
        V.chcieć(
            córka_krawca,
            V.wynieść(córka_krawca, remat(R.kufer / R.ojciec), Skąd.z(R.piwnica)),
        ),
        V.zapalić(córka_krawca, świeca, temat(Kiedy.w(R.noc))),
        schodzi_do_piwnicy(córka_krawca),
        V.zgasnąć(świeca),
        nie(V.wrócić(córka_krawca)),
        V.stać(
            mieszczanie,
            temat(D.rano),
            Gdzie.przed(R.kamienica),
            Dlaczego.bo(nie(chce_zejść(nikt))),
        ),
    ),
    Akapit(
        V.znać(czeladnik, córka_krawca),
        chce_zejść(czeladnik),
        V.wziąć(
            czeladnik,
            remat(A.duży * R.lustro),
            temat(Kiedy(R.wieczór)),
            Skąd.z(R.warsztat),
        ),
        schodzi_do_piwnicy(czeladnik),
        V.zasłonić(
            czeladnik,
            R.twarz,
            Czym(R.lustro),
            temat(Kiedy.gdy(V.otworzyć(bazyliszek, ~R.oko))),
        ),
        V.zobaczyć(bazyliszek, A.własny * R.odbicie),
        zamienia_w_kamień(V.zamienić, wzrok_potwora, bazyliszek),
    ),
    Akapit(
        V.poznać(czeladnik, córka_krawca, Gdzie.wśród(kamienne_postaci)),
        nie(V.wynieść(czeladnik, remat(R.lustro), Skąd.z(R.piwnica))),
        zabijają_wejście(A.nowy * ~R.deska),
    ),
)


if __name__ == "__main__":
    print(OPOWIEŚĆ.kompiluj())
