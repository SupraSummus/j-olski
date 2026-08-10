import pytest

pytest.importorskip("morfeusz2")

from opowieści.bazyliszek import OPOWIEŚĆ
from skład import Akapit, Kontekst, Opowieść, Postać, kompiluj
from skład.słownik import A, R, V, jest, opis

#: Tekst, który ma wyjść z drzew w ``opowieści/bazyliszek.py``, znak w znak.
#: Pierwszy powstał tekst, a drzewa są tym, co go wypuszcza,
#: więc różnica między jednym a drugim jest różnicą, którą ten kierunek mierzy.
BAZYLISZEK = """\
W piwnicy starej kamienicy mieszkał bazyliszek. \
Wzrok potwora zamieniał ludzi w kamień. \
Kamienne postaci, których nikt nie liczył, stały pod ścianą. \
Mieszczanie zabili okna i drzwi deskami.

W nocy córka krawca zapaliła świecę. \
Podniosła deskę. \
Zeszła po schodach. \
Świeca zgasła. \
Córka krawca nie wróciła.

Czeladnik, który znał córkę krawca, wziął z warsztatu duże lustro. \
Podniósł deskę. \
Zszedł po schodach. \
Zasłonił twarz lustrem. \
Bazyliszek otworzył oczy. \
Zobaczył własne odbicie. \
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


def test_orzeczenie_imienne_opuszcza_podmiot_tak_samo_jak_zdanie_o_czynności():
    """Dwa konstruktory zdania, jedna reguła, bo czytelnik nie widzi, który z nich stoi.

    Kopula niesie rodzaj i liczbę tak samo jak czasownik,
    więc podmiot jest przy niej równie zbędny,
    a zdanie, które go powtarza, wygląda na zdanie o kimś innym.
    """
    kot = Postać(R.kot)
    opowieść = Opowieść(Akapit(V.zamykać(kot, R.okno), jest(kot, R.potwór)))
    assert opowieść.kompiluj() == "Kot zamykał okno. Był potworem."
