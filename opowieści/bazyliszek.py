"""Bazyliszek warszawski, opowiedziany drzewami zamiast zdaniami.

Legenda o potworze z piwnicy przy Krzywym Kole
i o czeladniku, który zszedł tam z lustrem,
stoi tu jako drzewa w kategoriach ``skład.składnia``,
a polski tekst jest tym, co z nich wychodzi.
Dwanaście zdań tej wersji trzyma ``tests/test_opowieść.py``,
znak w znak z tym, co ten moduł wypuszcza.

Legendę tę Warszawa opowiada w wielu wersjach
i żadna z nich nie stoi tu jako źródło:
opowieść jest wymyślona pod ten plik, bo mierzy się nią kompilator, a nie podanie.

Po co ten plik jest, mówi ``opowieści/__init__.py``,
a co widać z niego na kompilatorze, mówi
``docs/design-notes.md``.
"""

from skład import Akapit, Opowieść, Postać
from skład.słownik import A, D, Dokąd, Gdzie, R, Skąd, V, czym, nie, nowe, razem, temat

#: Postaciami są ci, do których opowieść wraca; reszta rzeczy jest wymieniana raz.
#: Tożsamość niesie sama zmienna, więc ``bazyliszek`` użyty niżej dwa razy
#: jest w obu miejscach jednym bazyliszkiem, a nie dwoma.
bazyliszek = Postać(R.bazyliszek)
mieszczanie = Postać(~R.mieszczanin)
czeladnik = Postać(A.odważny * R.czeladnik)

#: Poddrzewa, które stoją w opowieści więcej niż raz.
#: Zmienna oszczędza tu powtórzenie, a nie niesie tożsamość:
#: ciemna piwnica jest za każdym razem taką samą piwnicą, bo tyle znaczy opis.
ciemna_piwnica = A.ciemny * R.piwnica
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


def strach(kto):
    """Dwa zdania o tym, co mieszczanie robili ze strachu.

    Funkcja zwraca listę, więc jedno wywołanie dokłada do akapitu dwa zdania.
    Podmiot stoi w obu, a w tekście wyjdzie raz,
    bo o opuszczeniu rozstrzyga akapit, a nie ten, kto zdania pisze.
    """
    return [
        V.zamykać(kto, razem([~R.okno, ~R.drzwi])),
        nie(V.wychodzić(kto, Dokąd.na(R.ulica))),
    ]


OPOWIEŚĆ = Opowieść(
    Akapit(
        V.mieszkać(nowe(bazyliszek), temat(Gdzie.w(R.piwnica / (A.stary * R.kamienica)))),
        V.mieć(bazyliszek, razem([A.koguci * R.dziób, A.wężowy * R.ogon, ~(A.żabi * R.oko)])),
        zamienia_w_kamień(V.zamieniać, wzrok_potwora, ~R.człowiek),
        nie(V.wracać(R.nikt, Skąd.z(ciemna_piwnica))),
    ),
    Akapit(
        strach(mieszczanie),
        nie(V.mieć(R.miasto, R.obrońca)),
    ),
    Akapit(
        V.zejść(czeladnik, Dokąd.do(ciemna_piwnica)),
        V.zasłonić(czeladnik, R.twarz, czym(A.duży * R.lustro)),
        V.zobaczyć(bazyliszek, A.własny * R.odbicie),
        zamienia_w_kamień(V.zamienić, wzrok_potwora, bazyliszek),
        V.odzyskać(R.miasto, R.spokój, temat(D.wkrótce)),
    ),
)


if __name__ == "__main__":
    print(OPOWIEŚĆ.kompiluj())
