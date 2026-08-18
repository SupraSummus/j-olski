#  Ten plik powstaje przebiegiem: python3 -m harness.figury readme-czytania
polecenie: python3 -m olski.check --readings -c Zapisz plik konfiguracyjny.\nKoszt samej szynki przewyższa koszt szynki z dodatkami.\nNowa program zapisuje ustawienia.
czyta: README.md#co-działa
ruszają:
  olski/subset.py: ccaa0fcef11b
  olski/grammar.py: 9077925971d9
  olski/parse.py: 7b2184342e31
  olski/morph.py: 7490ae22fd17
  olski/check.py: 268664a6f662
  olski/leksykon.txt: 7bcf02ee5940

<text>: valid     Zapisz plik konfiguracyjny.
                  one reading
                  - Object: plik konfiguracyjny, Verb: Zapisz
<text>: ambiguous Koszt samej szynki przewyższa koszt szynki z dodatkami.
                  6 readings, differing in Object, Subject; „z dodatkami” → „przewyższa”, „koszt”, „szynki”
                  - Subject: Koszt samej szynki, Object: koszt szynki z dodatkami, Verb: przewyższa, Modifier: z dodatkami → szynki
                  - Subject: Koszt samej szynki, Object: koszt szynki z dodatkami, Verb: przewyższa, Modifier: z dodatkami → koszt
                  - Subject: Koszt samej szynki, Object: koszt szynki, Verb: przewyższa, Modifier: z dodatkami → przewyższa
                  - Subject: koszt szynki z dodatkami, Object: Koszt samej szynki, Verb: przewyższa, Modifier: z dodatkami → szynki
                  - Subject: koszt szynki z dodatkami, Object: Koszt samej szynki, Verb: przewyższa, Modifier: z dodatkami → koszt
                  - Subject: koszt szynki, Object: Koszt samej szynki, Verb: przewyższa, Modifier: z dodatkami → przewyższa
<text>: rejected  Nowa program zapisuje ustawienia.
                  no reading: nothing in olski derives this
1 of 3 sentences are olski
