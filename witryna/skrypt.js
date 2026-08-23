//  Strona jest klientem API i niczym więcej: pyta o dane, a rysuje z nich to,
//  co ma pokazać. Ramy tu nie ma, bo widok jest listą zdań, a każde z nich
//  rysuje jedna funkcja. Napisy z odpowiedzi wchodzą przez `textContent`, więc
//  wklejony tekst zostaje tekstem, a nie znacznikiem.

//  Granicę znaków zna serwer i podaje ją w odpowiedzi, więc licznik pod polem
//  ma mianownik dopiero od pierwszej odpowiedzi. Wpisana tutaj byłaby drugą
//  kopią tej liczby i po zmianie na serwerze kłamałaby, nie mówiąc tego.
let granica = null;

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

function czytanie(role) {
  const wiersz = element("li");
  for (const [rola, wypełnienie] of Object.entries(role)) {
    wiersz.append(element("span", "rola", rola), document.createTextNode(` ${wypełnienie} `));
  }
  return wiersz;
}

//  Czytania stoją zwinięte, dopóki są dwa: zdanie olskie ma jedno, a zdanie
//  wieloznaczne ma ich tyle, że rozwinięte zasłaniają następne zdanie.
function czytania(lista, ile) {
  const zwój = element("details", "czytania");
  zwój.open = lista.length <= 2;
  const podpis = ile > lista.length
    ? `czytania: ${lista.length} z ${ile}`
    : `czytania: ${lista.length}`;
  zwój.append(element("summary", null, podpis));
  const spis = element("ol", "czytanie-lista");
  lista.forEach((role) => spis.append(czytanie(role)));
  zwój.append(spis);
  return zwój;
}

function domysły(lista) {
  const blok = element("div", "domysły");
  blok.append(element("span", "podpis", "? warstwa rozstrzygająca zgaduje, nie orzeka"));
  for (const domysł of lista) {
    const wiersz = element("p");
    wiersz.append(
      document.createTextNode(`„${domysł.modyfikator}” → „${domysł.gospodarz}” `),
      element("span", "powód", `${domysł.powód} (${domysł.świadek})`),
    );
    blok.append(wiersz);
  }
  return blok;
}

function zdanie(dane) {
  const blok = element("div", `zdanie ${dane.status}`);
  blok.append(element("span", `znaczek ${dane.status}`, dane.status));
  blok.append(element("p", "treść", dane.zdanie));
  const wyjaśnienie = element("p", "wyjaśnienie", dane.wyjaśnienie);
  for (const forma of dane.dalsze_zatrzymania) {
    wyjaśnienie.append(element("br"), document.createTextNode(`analiza staje też na „${forma}”`));
  }
  blok.append(wyjaśnienie);
  if (dane.czytania.length) blok.append(czytania(dane.czytania, dane.liczba_czytań));
  if (dane.domysły.length) blok.append(domysły(dane.domysły));
  return blok;
}

async function sprawdź() {
  wyślij.disabled = true;
  stan.classList.remove("pomyłka");
  stan.textContent = "sprawdzam…";
  try {
    const dane = await zapytaj("/werdykt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tekst: pole.value }),
    });
    werdykty.replaceChildren(...dane.zdania.map(zdanie));
    stan.textContent = dane.podsumowanie.wyjaśnienie;
    granica = dane.granica_znaków;
    odmierz();
  } catch (pomyłka) {
    stan.classList.add("pomyłka");
    stan.textContent = pomyłka.message;
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
