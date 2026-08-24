//  Strona jest klientem API i niczym więcej: pyta o dane, a rysuje z nich to,
//  co ma pokazać. Ramy tu nie ma, bo widok jest listą zdań, a każde z nich
//  rysuje jedna funkcja. Napisy z odpowiedzi wchodzą przez `textContent`, więc
//  wklejony tekst zostaje tekstem, a nie znacznikiem.

//  Granicę znaków zna serwer i podaje ją w odpowiedzi, więc licznik pod polem
//  ma mianownik dopiero od pierwszej odpowiedzi. Wpisana tutaj byłaby drugą
//  kopią tej liczby i po zmianie na serwerze kłamałaby, nie mówiąc tego.
let granica = null;

//  Etykieta przycisku schowka jest stałą, bo przycisk wraca do niej po pokazaniu,
//  że skopiował.
const KOPIUJ = "Kopiuj";

const pytanie = document.getElementById("pytanie");
const pole = document.getElementById("tekst");
const wyślij = document.getElementById("wyślij");
const miara = document.getElementById("miara");
const stan = document.getElementById("stan");
const werdykty = document.getElementById("werdykty");
const pytanieMakiety = document.getElementById("pytanie-makiety");
const wyślijMakietę = document.getElementById("wyślij-makietę");
const makieta = document.getElementById("makieta");

function element(nazwa, klasa, napis) {
  const węzeł = document.createElement(nazwa);
  if (klasa) węzeł.className = klasa;
  if (napis !== undefined) węzeł.textContent = napis;
  return węzeł;
}

//  Wiersz stanu mówi, co wyszło albo czemu nie wyszło, a klasę pomyłki trzeba
//  zdjąć tak samo jak założyć, więc jedno miejsce robi oba.
function powiedz(napis, pomyłka = false) {
  stan.classList.toggle("pomyłka", pomyłka);
  stan.textContent = napis;
}

function odmierz() {
  const znaków = pole.value.length;
  miara.textContent = granica === null ? `${znaków} znaków` : `${znaków} / ${granica}`;
  miara.classList.toggle("pełna", granica !== null && znaków > granica);
}

//  Odpowiedź z powodem przychodzi także wtedy, gdy status mówi o odmowie, więc
//  jedno miejsce czyta JSON, a wołający dostaje albo dane, albo wyjątek z powodem.
async function zapytaj(adres, opcje) {
  const odpowiedź = await fetch(adres, opcje);
  const dane = await odpowiedź.json();
  if (!odpowiedź.ok) throw new Error(dane.powód || odpowiedź.statusText);
  return dane;
}

//  Napis, którego strona jest właścicielem, ma dwa widoki: węzeł na stronie i
//  wiersz w tekście dla schowka. Dwie kopie rozjechałyby się po cichu, więc
//  każdy taki napis powstaje w jednej funkcji.
//  Podpis liczy streszczenia, a nie odczytania: streszczenie stoi pod zwojem raz,
//  choć bywa napisem kilku odczytań (`Verdict.readings` w `olski/subset.py`). Ile
//  odczytań zdanie ma, mówi wyjaśnienie nad zwojem, więc drugiej kopii tej liczby
//  tutaj nie ma.
function podpisOdczytań(streszczeń, urwane) {
  const podpis = `streszczenia odczytań: ${streszczeń}`;
  return urwane ? `${podpis}, lista urwana` : podpis;
}

function podpisZatrzymania(forma) {
  return `analiza staje też na „${forma}”`;
}

function podpisDomysłu(domysł) {
  return `„${domysł.modyfikator}” → „${domysł.gospodarz}”`;
}

function podpisRozbieżności(konstytuent) {
  return `„${konstytuent}” czyta się tak:`;
}

//  Streszczenie czytania jest listą streszczeń zdań składowych, po jednym na
//  składowe (`describe` w `olski/parse.py`), więc każde stoi w osobnym wierszu
//  jednej pozycji spisu: pozycji jest tyle, ile czytań.
function czytanie(streszczenie) {
  const wiersz = element("li");
  for (const składowe of streszczenie) {
    const część = element("div");
    for (const [rola, wypełnienie] of Object.entries(składowe)) {
      część.append(element("span", "rola", rola), document.createTextNode(` ${wypełnienie} `));
    }
    wiersz.append(część);
  }
  return wiersz;
}

function spisCzytań(lista) {
  const spis = element("ol", "czytanie-lista");
  lista.forEach((streszczenie) => spis.append(czytanie(streszczenie)));
  return spis;
}

//  Czytania stoją zwinięte, dopóki są dwa: zdanie olskie ma jedno, a zdanie
//  wieloznaczne ma ich tyle, że rozwinięte zasłaniają następne zdanie.
//  Konstytuent rozbieżny dostaje własny spis pod tym samym zwojem, bo mówi o
//  czytaniach tego samego zdania.
function czytania(dane) {
  const zwój = element("details", "czytania");
  zwój.open = dane.czytania.length <= 2;
  zwój.append(element("summary", null, podpisOdczytań(dane.czytania.length, dane.urwane)));
  zwój.append(spisCzytań(dane.czytania));
  for (const wpis of dane.rozbieżne) {
    const blok = element("div", "rozbieżny");
    blok.append(element("span", "podpis", podpisRozbieżności(wpis.konstytuent)));
    blok.append(spisCzytań(wpis.czytania));
    zwój.append(blok);
  }
  return zwój;
}

function domysły(lista) {
  const blok = element("div", "domysły");
  blok.append(element("span", "podpis", "? warstwa rozstrzygająca zgaduje, nie orzeka"));
  for (const domysł of lista) {
    const wiersz = element("p");
    wiersz.append(
      document.createTextNode(`${podpisDomysłu(domysł)} `),
      element("span", "powód", `${domysł.powód} (${domysł.świadek})`),
    );
    blok.append(wiersz);
  }
  return blok;
}

//  Wiersze jednego czytania, po jednym na zdanie składowe, w tym samym układzie,
//  jaki pisze `_czytanie` w `olski/check.py`, i po co on taki, mówi tamten plik.
function wierszeCzytania(streszczenie, wcięcie) {
  return streszczenie.map((składowe, numer) => {
    const role = Object.entries(składowe)
      .map(([rola, wypełnienie]) => `${rola}: ${wypełnienie}`)
      .join(", ");
    return `${wcięcie}${numer === 0 ? "- " : "  "}${role}`;
  });
}

//  Tekst dla schowka jest drugim widokiem tych samych danych: wierszami, a nie
//  węzłami. Czytania wchodzą wszystkie, także zwinięte pod zwojem, bo tekstu nie
//  ma czym rozwinąć.
function tekstWerdyktu(dane) {
  const wiersze = [`${dane.status}  ${dane.zdanie}`, dane.wyjaśnienie];
  for (const forma of dane.dalsze_zatrzymania) wiersze.push(podpisZatrzymania(forma));
  if (dane.czytania.length) {
    wiersze.push(podpisOdczytań(dane.czytania.length, dane.urwane));
    for (const streszczenie of dane.czytania) wiersze.push(...wierszeCzytania(streszczenie, ""));
  }
  for (const wpis of dane.rozbieżne) {
    wiersze.push(podpisRozbieżności(wpis.konstytuent));
    for (const streszczenie of wpis.czytania) wiersze.push(...wierszeCzytania(streszczenie, "  "));
  }
  for (const domysł of dane.domysły) {
    wiersze.push(`? ${podpisDomysłu(domysł)}: ${domysł.powód} (${domysł.świadek})`);
  }
  return `${wiersze.join("\n")}\n`;
}

//  Odmowa idzie do wiersza stanu, a nie na przycisk, bo przycisk przepisany na
//  komunikat zostaje bez etykiety do kliknięcia.
function kopiowanie(dane) {
  const przycisk = element("button", "kopiuj", KOPIUJ);
  przycisk.type = "button";
  przycisk.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(tekstWerdyktu(dane));
      przycisk.textContent = "skopiowane";
      setTimeout(() => { przycisk.textContent = KOPIUJ; }, 1500);
    } catch (pomyłka) {
      powiedz(`nie udało się skopiować: ${pomyłka.message}`, true);
    }
  });
  return przycisk;
}

function zdanie(dane) {
  const blok = element("div", `zdanie ${dane.status}`);
  const nagłówek = element("div", "nagłówek");
  nagłówek.append(element("span", `znaczek ${dane.status}`, dane.status));
  //  Schowka nie ma bez kontekstu bezpiecznego, czyli pod http poza localhostem,
  //  a przycisk, który zawsze odmawia, jest gorszy niż jego brak.
  if (navigator.clipboard) nagłówek.append(kopiowanie(dane));
  blok.append(nagłówek, element("p", "treść", dane.zdanie));
  const wyjaśnienie = element("p", "wyjaśnienie", dane.wyjaśnienie);
  for (const forma of dane.dalsze_zatrzymania) {
    wyjaśnienie.append(element("br"), document.createTextNode(podpisZatrzymania(forma)));
  }
  blok.append(wyjaśnienie);
  if (dane.czytania.length) blok.append(czytania(dane));
  if (dane.domysły.length) blok.append(domysły(dane.domysły));
  return blok;
}

async function sprawdź() {
  wyślij.disabled = true;
  powiedz("sprawdzam…");
  try {
    const dane = await zapytaj("/werdykt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tekst: pole.value }),
    });
    werdykty.replaceChildren(...dane.zdania.map(zdanie));
    powiedz(dane.podsumowanie.wyjaśnienie);
    granica = dane.granica_znaków;
    odmierz();
  } catch (pomyłka) {
    powiedz(pomyłka.message, true);
  } finally {
    wyślij.disabled = false;
  }
}

async function losuj() {
  wyślijMakietę.disabled = true;
  try {
    const ziarno = document.getElementById("ziarno").value;
    const akapity = document.getElementById("akapity").value;
    const zapytanie = new URLSearchParams({ akapity });
    if (ziarno) zapytanie.set("ziarno", ziarno);
    const dane = await zapytaj(`/makieta?${zapytanie}`);
    const blok = element("div", "makieta-tekst");
    dane.tekst.split("\n\n").forEach((akapit) => blok.append(element("p", null, akapit)));
    makieta.replaceChildren(blok, element("p", "ziarno", `ziarno: ${dane.ziarno}`));
  } catch (pomyłka) {
    makieta.replaceChildren(element("p", "stan pomyłka", pomyłka.message));
  } finally {
    wyślijMakietę.disabled = false;
  }
}

pytanie.addEventListener("submit", (zdarzenie) => {
  zdarzenie.preventDefault();
  sprawdź();
});
pytanieMakiety.addEventListener("submit", (zdarzenie) => {
  zdarzenie.preventDefault();
  losuj();
});
pole.addEventListener("input", odmierz);
pole.addEventListener("keydown", (zdarzenie) => {
  if (zdarzenie.key === "Enter" && (zdarzenie.ctrlKey || zdarzenie.metaKey)) sprawdź();
});

odmierz();
sprawdź();
