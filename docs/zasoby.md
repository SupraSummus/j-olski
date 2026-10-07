# Zasoby

Olski stoi na zasobach Zespołu Inżynierii Lingwistycznej IPI PAN.
Repozytorium nie trzyma korpusów, bo są duże i mają własne licencje.
Ten dokument mówi, skąd je wziąć i które pliki repozytorium z nich powstają.

## Morfeusz 2

Analizator i generator morfologiczny polszczyzny, oparty na słowniku SGJP.
Instaluje się z PyPI jako zależność pakietu (`morfeusz2`),
więc `pip install -e '.[dev]'` przynosi go razem z resztą.
Strona projektu: <http://morfeusz.sgjp.pl/>.

## Walenty

Słownik walencyjny polszczyzny: co czasownik i rzeczownik bierze
oraz, w warstwie semantycznej, czego żąda od argumentu.
Z wydania z 18 kwietnia 2016 powstają dwa pliki pakietu.
Oba są na CC BY-SA 4.0, tak jak źródło.

Wydanie tekstowe daje leksykon walencyjny:

```sh
curl -L -o walenty.zip \
  'http://zil.ipipan.waw.pl/Walenty?action=AttachFile&do=get&target=walenty_20160418-text.zip'
unzip walenty.zip
python3 -m harness.walenty walenty_20160418-text/verbs/walenty_20160418_verbs_all.txt \
  --rzeczowniki walenty_20160418-text/nouns/walenty_20160418_nouns_all.txt \
  > olski/leksykon.txt
```

Wydanie TEI niesie warstwę semantyczną i daje plik żądań:

```sh
curl -L -o walenty-tei.zip \
  'http://zil.ipipan.waw.pl/Walenty?action=AttachFile&do=get&target=walenty_20160418-TEI.zip'
unzip walenty-tei.zip
python3 -m harness.żądania walenty_20160418-TEI/walenty_20160418.xml > olski/żądania.txt
```

Warstwa semantyczna obsadza pozycje rolami
i żąda od argumentu klasy rzeczy:
klasy nazwanej (na przykład `LUDZIE`, `MIEJSCE`, `KOMUNIKAT`)
albo zbioru synsetów Słowosieci.

## Składnica

Bank drzew składnikowych polszczyzny ze zdaniami z NKJP.
Wydanie z 23 lipca 2018 ma 13 035 zdań z pełnym złotym drzewem.
Jest na GPL, więc tabela przyłączeń zbudowana na nim, `olski/skłonności.txt`, też.

```sh
curl -L -o skladnica.tar.gz \
  'https://zil.ipipan.waw.pl/Sk%C5%82adnica?action=AttachFile&do=get&target=Sk%C5%82adnica-frazowa-180723.tar.gz'
tar xzf skladnica.tar.gz
python3 -m harness.pomiar Składnica-frazowa-180723/
python3 -m harness.skłonności Składnica-frazowa-180723/ --zbuduj olski/skłonności.txt
```

`harness.pomiar` mierzy pokrycie gramatyki, czyli ile zdań wychodzi z jednym czytaniem,
ile z kilkoma i ile bez żadnego.

## NKJP

Narodowy Korpus Języka Polskiego.
Podkorpus milionowy w wydaniu 1.2 jest na CC BY i niesie warstwy anotacji obok tekstu.
Z niego pochodzą zdania w `próba/nkjp-sądy.txt`.

```sh
curl -L -o nkjp1m.tar.gz \
  'http://clip.ipipan.waw.pl/NationalCorpusOfPolish?action=AttachFile&do=get&target=NKJP-PodkorpusMilionowy-1.2.tar.gz'
mkdir nkjp && tar xzf nkjp1m.tar.gz -C nkjp
python3 -m harness.nkjp nkjp/ --into proza/nkjp
```

## Słowosieć

Relacyjny słownik znaczeń polszczyzny (plWordNet).
Jest potrzebny, żeby sprawdzić, czy słowo w zdaniu należy do klasy, której żąda Walenty.
W październiku 2026 formularz pobierania przekierowuje na <https://slowosiec.pl/>,
a pełne zrzuty witryna udostępnia po zgłoszeniu.
Sprawy licencyjne idą na `plwordnet@clarin-pl.eu`.
Licencja pozwala używać i rozpowszechniać Słowosieć bez opłat,
pod warunkiem zachowania noty copyright na kopii.
