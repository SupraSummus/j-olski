# j-olski

Olski to parser i generator polszczyzny, z których budujemy kompilator.
Parser czyta zdanie gramatyką pisaną ręką nad Morfeuszem 2 i zwraca wszystkie rozbiory.
Generator, nazwany składem, składa polskie zdanie z drzewa tego, co ma zostać powiedziane.
Oba są deterministyczne: to samo wejście daje tę samą odpowiedź.

## Kierunek

Kompilator ma cztery etapy:

1. **Front-end**: Morfeusz i gramatyka dają wszystkie rozbiory zdania. Działa.
2. **Reprezentacja pośrednia**: kto, co, komu; rozbiory o tej samej strukturze dają jedną.
   Zalążek działa (`olski/reprezentacja.py`).
3. **Przebieg semantyczny**: typy z Walentego i model uczony na strukturach, nigdy na napisie.
   Do zbudowania.
4. **Back-end**: skład. Działa dla konstrukcji, które ma.

Uzasadnienie, otwarte decyzje i następny krok opisuje [docs/kierunek.md](docs/kierunek.md).

## Co działa

Zainstaluj pakiet z zależnościami deweloperskimi:

```sh
pip install -e '.[dev]'
```

**Rozbiór.**
Narzędzie wypisuje wszystkie czytania zdania.

```sh
python3 -m olski.check --readings -c "Program otwierający się psuje.
Operator ustala priorytet."
```

```text
<text>: Program otwierający się psuje.
        3 odczytania, różne w rolach: dopełnienie, orzeczenie, podmiot
        - podmiot: Program otwierający się, orzeczenie: psuje
        - podmiot: Program otwierający, orzeczenie: się psuje
        - dopełnienie: Program otwierający się, orzeczenie: psuje
<text>: Operator ustala priorytet.
        2 odczytania, różne w rolach: dopełnienie, podmiot
        - podmiot: Operator, dopełnienie: priorytet, orzeczenie: ustala
        - podmiot: priorytet, dopełnienie: Operator, orzeczenie: ustala
zdań: 2; wieloznaczne: 2; bez odczytania: 0
```

Drugie czytanie drugiego zdania jest składniowo możliwe,
bo polszczyzna zna szyk dopełnienie–orzeczenie–podmiot,
ale priorytet nie ustala operatora.
Odrzucić je ma przebieg semantyczny, a nie gramatyka.

**Zaimek wskazujący na dwie rzeczy.**

```sh
python3 -m olski.check -c "Narzędzie sprawdza zdania tekstu.
Autor poprawia je sam."
```

```text
<text>: Autor poprawia je sam.
        „je” wskazuje na „Narzędzie” albo „zdania”
zdań: 2; wieloznaczne: 0; bez odczytania: 0; niejasne odniesienia: 1
```

Morfologia dopuszcza oba odniesienia.
Autor poprawia zdania, a nie narzędzie, ale tego nie widać bez semantyki.

**Skład.**
Wchodzi drzewo tego, co ma zostać powiedziane, a wychodzi zdanie.

```python
from olski.skład import kompiluj
from olski.skład.słownik import A, R, V, jest

kompiluj(jest(R.parser / R.podzbiór, R.cel))     # Parser podzbioru jest celem.
kompiluj(V.sprawdzać(R.parser, ~(A.polski * R.tekst)))  # Parser sprawdza polskie teksty.
```

Ten sam skład losuje tekst do makiety:

```sh
python3 -m olski.skład.makieta --ziarno 1871 --akapity 1
```

```text
Czeladnik zapłakał w wąskiej piwnicy. Dziewczyna zgubiła glinianą skrzynię, ponieważ czeladnik zszedł. Zdążyła mieszkać przed ciężkim młynem. Córka dała dziewczynie koszyk. Zdążyła wrócić od młodej wdowy. Czeladnik zważył kufry gospodarza i sukno.
```

**Witryna.**
`python3 -m witryna` stawia lokalnie stronę z tym samym werdyktem.
Wdrożona stoi pod adresem [olski.pl](https://olski.pl).

## Repozytorium

- `olski/`: pakiet, czyli parser, gramatyka, werdykt i skład.
  Mapę modułów podaje [docs/kod.md](docs/kod.md).
- `harness/`: potoki danych i pomiar pokrycia, dla tego, kto olskiego rozwija.
- `próba/`: zdania z cudzego tekstu wraz z oceną, czyli materiał do ewaluacji.
- `witryna/`: strona i jej API.
- `tests/`: testy pakietu, potoków i witryny.

Skąd wziąć Morfeusza, Walentego, Składnicę i NKJP, mówi [docs/zasoby.md](docs/zasoby.md).
Dokumentacja wraz z referencją API stoi pod adresem
[dokumentacja.olski.pl](https://dokumentacja.olski.pl).

## Stan sprzed resetu

Do commita `d79da51` projekt miał inny kierunek:
sprawdzacz, który zgłasza usterki tekstu samą gramatyką podzbioru.
Tamte dokumenty, rejestr otwartej roboty i reguły pracy są w gicie
(`git show d79da51:docs/roadmap.md`).
Czemu ten kierunek porzuciliśmy, mówi [docs/kierunek.md](docs/kierunek.md#stan-sprzed-resetu).

## Licencja

Kod, testy i proza są na licencji MIT.
Dwa pliki danych podlegają warunkom swoich źródeł:
`olski/leksykon.txt` i `olski/żądania.txt` powstają z Walentego i są na CC BY-SA 4.0,
a `olski/skłonności.txt` powstaje ze Składnicy i jest na GPL v3.
Zdania w `próba/wybory*.txt` są cudze i to repozytorium ich nie licencjonuje,
a zdania w `próba/nkjp-*.txt` pochodzą z NKJP i są na CC BY 4.0.

Wszystko to deklaruje [REUSE.toml](REUSE.toml).
Teksty licencji są w katalogu `LICENSES/`, nazwane identyfikatorem SPDX.
