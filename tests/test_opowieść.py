import pytest

pytest.importorskip("morfeusz2")

from opowieści.bazyliszek import OPOWIEŚĆ
from skład import Akapit, Kontekst, Opowieść, Postać, PozaRamą, kompiluj
from skład.słownik import A, Dlaczego, Gdzie, Kiedy, R, Skutek, V, jest, nie, opis, potem, temat

#: Tekst, który ma wyjść z drzew w ``opowieści/bazyliszek.py``, znak w znak.
#: Pierwszy powstał tekst, a drzewa są tym, co go wypuszcza,
#: więc różnica między jednym a drugim jest różnicą, którą ten kierunek mierzy.
BAZYLISZEK = """\
W piwnicy starej kamienicy mieszkał bazyliszek. \
Wzrok potwora zamieniał ludzi w kamień, więc mieszczanie zabili okna i drzwi deskami. \
Pod ścianą stały kamienne postaci, których nikt nie liczył.

W nocy córka krawca zapaliła świecę, bo w piwnicy stał kufer ojca. \
Podniosła deskę i zeszła po schodach. \
Świeca zgasła. \
Córka krawca nie wróciła.

Czeladnik, który znał córkę krawca, wziął z warsztatu duże lustro. \
Podniósł deskę i zszedł po schodach. \
Gdy bazyliszek otworzył oczy, czeladnik zasłonił twarz lustrem. \
Bazyliszek zobaczył własne odbicie. \
Wzrok potwora zamienił bazyliszka w kamień.

Czeladnik poznał córkę krawca wśród kamiennych postaci. \
Nie wyniósł z piwnicy lustra. \
Mieszczanie zabili okna i drzwi nowymi deskami."""


def test_opowieść_o_bazyliszku_wychodzi_z_drzew_znak_w_znak():
    """Kryterium tego toru jest porównaniem tekstu z tekstem, a nie werdyktem parsera.

    Słabszego porównania nie ma czym zrobić: gramatyka podzbioru nie obejmuje
    czasu przeszłego, więc nad tym tekstem nie miałaby czego powiedzieć,
    a ``docs/roadmap.md`` wywodzi, dlaczego to jej zadaniem nie jest.
    """
    assert OPOWIEŚĆ.kompiluj() == BAZYLISZEK


def test_ten_sam_podmiot_znika_a_wraca_wraz_z_akapitem():
    """Opuszczenie podmiotu ma dwa warunki i oba są tu sprawdzone naraz.

    Drugie zdanie akapitu podmiot traci, bo mowa dalej o tym samym,
    a pierwsze zdanie akapitu następnego odzyskuje go,
    choć postać jest ta sama i stoi tuż obok.
    """
    kot = Postać(R.kot)
    opowieść = Opowieść(
        Akapit(V.zamykać(kot, R.okno), V.otwierać(kot, R.pudełko)),
        Akapit(V.otwierać(kot, R.okno)),
    )
    assert opowieść.kompiluj() == "Kot zamykał okno. Otwierał pudełko.\n\nKot otwierał okno."


def test_podmiot_wraca_gdy_między_zdaniami_stanął_inny():
    """Warunkiem opuszczenia jest zdanie poprzednie, a nie obecność wcześniej w akapicie.

    Bez tego zdanie o kocie czytałoby się jako zdanie o pudełku,
    bo podmiotu, który znika, czytelnik szuka w zdaniu tuż obok.
    """
    kot, pudełko = Postać(R.kot), Postać(R.pudełko)
    opowieść = Opowieść(
        Akapit(V.zamykać(kot, R.okno), V.stać(pudełko), V.otwierać(kot, R.pudełko))
    )
    assert opowieść.kompiluj() == "Kot zamykał okno. Pudełko stało. Kot otwierał pudełko."


def test_rzecz_opisana_zdaniem_zostaje_tą_samą_rzeczą_w_zdaniu_następnym():
    """Opis wskazuje rzecz, a nie robi z niej drugiej, więc podmiot dalej się opuszcza.

    Zdanie podrzędne ma własny podmiot i to ono jest tu pomyłką do zrobienia:
    gdyby tożsamość liczyła się z niego, opuszczał się dalej nie ten, o kim mowa.
    """
    kot = Postać(R.kot)
    opowieść = Opowieść(
        Akapit(
            V.zamykać(opis(kot, V.gonić(R.mysz, kot)), R.okno),
            V.otwierać(kot, R.pudełko),
        )
    )
    assert opowieść.kompiluj() == "Kot, którego mysz goniła, zamykał okno. Otwierał pudełko."


def test_dwie_postaci_o_jednym_lemacie_są_dwiema_rzeczami():
    """Tożsamość niesie zmienna, a nie lemat, i to jest cała różnica.

    Bez tego opowieść o dwóch braciach opuszczałaby podmiot tam,
    gdzie czytelnik trafiłby na niewłaściwego.
    """
    jeden, drugi = Postać(R.brat), Postać(R.brat)
    opowieść = Opowieść(Akapit(V.zamykać(jeden, R.okno), V.otwierać(drugi, R.pudełko)))
    assert opowieść.kompiluj() == "Brat zamykał okno. Brat otwierał pudełko."


def test_podmiot_bez_tożsamości_nie_znika_nigdy():
    """Rzecz wymieniona dwa razy jest dwiema rzeczami, dopóki autor nie powie inaczej.

    Zdanie o drugim takim samym kocie ma podmiot wypisać,
    bo nie ma czym stwierdzić, że jest to ten sam kot.
    """
    opowieść = Opowieść(Akapit(V.zamykać(R.kot, R.okno), V.otwierać(R.kot, R.pudełko)))
    assert opowieść.kompiluj() == "Kot zamykał okno. Kot otwierał pudełko."


def test_funkcja_zwracająca_listę_dokłada_do_akapitu_kilka_zdań():
    """Wzorcem akapitu jest zwykła funkcja Pythona, a nie kategoria tej biblioteki."""

    def dwa_razy(kto):
        return [V.zamykać(kto, R.okno), V.otwierać(kto, R.pudełko)]

    kot = Postać(R.kot)
    assert Opowieść(Akapit(dwa_razy(kot))).kompiluj() == "Kot zamykał okno. Otwierał pudełko."


def test_to_samo_drzewo_stoi_w_dwóch_czasach_zależnie_od_tekstu():
    """Czas jest własnością opowiadania, a nie zdarzenia, i dlatego nie ma go w drzewie."""
    drzewo = V.zamykać(R.kot, R.okno)
    assert kompiluj(drzewo) == "Kot zamyka okno."
    assert kompiluj(drzewo, Kontekst(czas="kiedyś")) == "Kot zamykał okno."


def test_kopula_też_dostaje_czas_od_opowieści():
    """Orzeczenie imienne nie ma osobnej drogi do czasu, bo pyta o formę tak samo."""
    assert kompiluj(jest(A.stary * R.kot, R.potwór), Kontekst(czas="kiedyś")) == (
        "Stary kot był potworem."
    )


def test_ciąg_zdarzeń_wypisuje_podmiot_raz_a_czasownik_przy_każdym():
    """Kilka zdarzeń jednym zdaniem, bo tak polszczyzna mówi o tym, co po sobie idzie.

    Opuszczenie wewnątrz ciągu jest tym samym opuszczeniem, co między zdaniami,
    więc ciąg o dwóch podmiotach wypisuje oba,
    a ciąg o jednym wypisuje go raz i to jest cała różnica.
    """
    kot = Postać(R.kot)
    assert kompiluj(potem(V.zamykać(kot, R.okno), V.otwierać(kot, R.pudełko))) == (
        "Kot zamyka okno i otwiera pudełko."
    )
    assert kompiluj(potem(V.zamykać(kot, R.okno), V.spać(R.mysz))) == (
        "Kot zamyka okno i mysz śpi."
    )


def test_okoliczność_wyrażona_zdarzeniem_odpowiada_na_to_samo_pytanie_co_rzecz():
    """Relacja jest jedna, a pod nią stoi raz rzecz, a raz zdarzenie.

    Spójnik wychodzi z relacji tak samo jak przyimek,
    więc drzewo mówi, kiedy i dlaczego, a nie że stoi tam zdanie podrzędne.
    Wysunięcie jest przy tym zwykłym wyróżnieniem, a nie osobnym wariantem:
    to samo zdanie stoi raz z okolicznością na czele, a raz z nią na swoim miejscu.
    """
    gdy = Kiedy.gdy(V.zgasnąć(R.świeca))
    assert kompiluj(V.wrócić(R.czeladnik, temat(gdy)), Kontekst(czas="kiedyś")) == (
        "Gdy świeca zgasła, czeladnik wrócił."
    )
    assert kompiluj(V.wrócić(R.czeladnik, gdy), Kontekst(czas="kiedyś")) == (
        "Czeladnik wrócił, gdy świeca zgasła."
    )


def test_spójnik_postawiony_w_relacji_której_leksykon_nie_ma_zgłasza_się_od_razu():
    """Zgłoszenie pada przy budowaniu drzewa, tak samo jak przy przyimku.

    ``bo`` mówi, dlaczego, i nie mówi, kiedy,
    a przyimek stojący przed zdarzeniem nie mówi niczego,
    bo zdanie podrzędne nie ma przypadka, którym by mu odpowiedziało.
    """
    with pytest.raises(PozaRamą):
        Kiedy.bo(V.spać(R.kot))
    with pytest.raises(PozaRamą):
        Kiedy.w(V.spać(R.kot))


def test_o_czele_pary_zdań_rozstrzyga_spójnik_a_nie_autor():
    """Leksykon spójników mówi jedno o szyku i jest to jedyne, co o szyku mówi leksykon.

    Odpowiedź jest własnością słowa, a nie relacji, w której ono stoi,
    i widać to na dwóch spójnikach jednej relacji:
    zdanie z ``ponieważ`` na czele jest polskie, a z ``bo`` na czele nie jest.
    Skutek odpowiada tak samo jak przyczyna, bo zdanie z ``więc``
    stoi za tym, przy którym stoi, i nie ma go czym przestawić.
    """
    zgasła = V.zgasnąć(R.świeca)
    wróciła = nie(V.wrócić(R.córka, temat(Dlaczego.ponieważ(zgasła))))
    assert kompiluj(wróciła, Kontekst(czas="kiedyś")) == (
        "Ponieważ świeca zgasła, córka nie wróciła."
    )
    with pytest.raises(PozaRamą):
        kompiluj(nie(V.wrócić(R.córka, temat(Dlaczego.bo(zgasła)))))
    with pytest.raises(PozaRamą):
        kompiluj(V.zamykać(R.kot, R.okno, temat(Skutek.więc(V.spać(R.mysz)))))


def test_podmiot_wraca_gdy_ktoś_inny_wyciąga_z_czasownika_tę_samą_formę():
    """Po opuszczonym podmiocie zostaje forma czasownika i tylko ona.

    Dwa zdania różnią się rodzajem rzeczy, która stoi w zdaniu podrzędnym,
    i tylko tym: kufer nie odbiera córce niczego, bo rodzaj ma inny,
    a skrzynia odbiera jej formę żeńską, więc podmiot staje wypisany.
    """

    def zeszła(rzecz):
        córka = Postać(R.córka)
        return Opowieść(
            Akapit(
                V.zapalić(córka, R.świeca, Dlaczego.bo(V.stać(rzecz, Gdzie.w(R.piwnica)))),
                V.zejść(córka),
            )
        ).kompiluj()

    assert zeszła(R.kufer) == "Córka zapaliła świecę, bo kufer stał w piwnicy. Zeszła."
    assert zeszła(R.skrzynia) == (
        "Córka zapaliła świecę, bo skrzynia stała w piwnicy. Córka zeszła."
    )


def test_podmiot_opisany_zdaniem_nie_znika_wraz_z_opisem():
    """Opuszczenie zabrałoby to, co autor o tej rzeczy akurat powiedział.

    Rzecz jest ta sama i zdanie obok mówiło o niej,
    więc bez tego warunku zdanie podrzędne przepadłoby po cichu.
    """
    kot = Postać(R.kot)
    opowieść = Opowieść(
        Akapit(V.zamykać(kot, R.okno), V.otwierać(opis(kot, V.spać(kot)), R.pudełko))
    )
    assert opowieść.kompiluj() == "Kot zamykał okno. Kot, który spał, otwierał pudełko."


def test_orzeczenie_imienne_opuszcza_podmiot_tak_samo_jak_zdanie_o_czynności():
    """Dwa konstruktory zdania, jedna reguła, bo czytelnik nie widzi, który z nich stoi.

    Kopula niesie rodzaj i liczbę tak samo jak czasownik,
    więc podmiot jest przy niej równie zbędny,
    a zdanie, które go powtarza, wygląda na zdanie o kimś innym.
    """
    kot = Postać(R.kot)
    opowieść = Opowieść(Akapit(V.zamykać(kot, R.okno), jest(kot, R.potwór)))
    assert opowieść.kompiluj() == "Kot zamykał okno. Był potworem."
