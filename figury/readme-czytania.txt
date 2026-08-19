#  Ten plik powstaje przebiegiem: python3 -m harness.figury readme-czytania
polecenie: python3 -m olski.check --readings -c Zapisz plik konfiguracyjny.\nKoszt samej szynki przewyższa koszt szynki z dodatkami.\nNowa program zapisuje ustawienia.
czyta: README.md#co-działa
ruszają:
  olski/subset.py: 290a30c351a9
  olski/grammar.py: 9077925971d9
  olski/parse.py: b0553f072e6c
  olski/morph.py: 68c6bc12d9f1
  olski/check.py: 268664a6f662
  olski/leksykon.txt: 00193493b3ea

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
