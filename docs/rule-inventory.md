# Inwentarz kandydatów na reguły

Kolejka reguł do napisania.
Wywód, z którego te pozycje wyszły, stoi w [linter.md](linter.md):
po co jest ten linter, ile analizy wolno regule zażądać
i dlaczego próg bez kalibracji jest opinią z przecinkiem.

Grupuje je [poziom analizy](linter.md#how-deep-does-each-rule-have-to-see),
którego każda z nich potrzebuje.
Pozycja oznaczona *cited* ma za sobą źródło
z [similar-work.md](similar-work.md),
z [listy źródeł tamtego dokumentu](linter.md#sources)
albo z listy na końcu tego pliku;
reszta jest hipotezą do skalibrowania, a nie wnioskiem.
Regułę, która stąd wychodzi, deklaruje się tak, jak mówi [rules.md](rules.md),
a jej pole `sources` cytuje sekcję, z której pozycja wyszła.
Pozycja, która wyszła, zostaje tu bez znacznika:
co jest wysłane, mówi `python3 -m olski --list-rules`,
i tamta odpowiedź nie rozjedzie się z pakietem.
Pozycja, którą pomiar z pakietu usunął, niesie to przy sobie,
bo inaczej ktoś zbuduje ją drugi raz.

Prozy literackiej ta lista nie obejmuje.
[To, co w niej mimo wszystko da się lintować](linter.md#what-is-nevertheless-lintable-in-fiction),
jest taką samą listą kandydatów i zostaje przy swoim wywodzie,
bo z tamtej listy nikt następnej reguły nie bierze:
rejestr, którego dotyczy, [linter.md](linter.md#and-fiction)
trzyma jako życzenie, a nie jako milestone.

Rejestru ustaw ta lista nie obejmuje z tego samego powodu.
Czego „Zasady techniki prawodawczej” żądają od zdania w ustawie
i co z tego dałoby się zmierzyć,
trzyma [ustawy.md](ustawy.md#nierozstrzygnięte),
bo tamten rejestr jest osobnym zakresem i chciałby osobnej kalibracji.

## Typography, tier A

- Em dash frequency, and em dashes used where Polish would not use them *cited*
- Straight quotes where Polish takes „ and ”
- Single-letter words left at end of line.
  Zbudowana i usunięta,
  bo rejestrem, który tę regułę utrzymuje, jest tekst, który ktoś złoży,
  a nie dokumentacja;
  trafienia, na których to stanęło, trzyma
  [odczyt, który ją usunął](firing-rates.md#dwie-reguły-wyszły-z-pakietu-i-to-jest-ich-odczyt)
- Markdown emphasis left unreviewed in running prose *cited*
- Excess spacing and other generation artifacts *cited*

## Lexical, tier B

- Anglicisms and calques:
  `dedykowany`, `adresować` a problem, `w oparciu o`,
  `dostarczać wartość`, `holistyczny`, `synergia`
- Booster inflation:
  `kluczowy`, `istotny`, `przełomowy`, `fundamentalny`, `niezwykle`, `znacząco`
- Stock openers and closers:
  `W dzisiejszym szybko zmieniającym się świecie`,
  `Warto zauważyć, że`, `Podsumowując`
- Connector density:
  `Ponadto`, `Co więcej`, `Dodatkowo`, `Niemniej jednak`
- Repetitive evaluative vocabulary *cited*
- **Unconventional collocation** —
  a verb paired with an argument it is rarely paired with,
  as in `zaloguj się do bazy danych`,
  where what has an account to log into
  is the server serving the database.
  The defect is the elided step,
  which a reader restores or does not,
  and the wish behind the entry is that olski type-check prose:
  a slot expecting one kind of thing, filled by another.

  That framing is the wrong instrument,
  and the reason is worth keeping,
  because the mismatch is real and carries no verdict.
  The same mismatch stands in `kliknij w link`, `dysk padł`
  and `Warszawa zdecydowała`,
  which are Polish rather than faults in it.
  A check over selectional preferences is a metonymy detector.
  What separates a shorthand a reader restores
  from one that leaves them guessing
  is how established the pairing is, rather than what it pairs,
  and that is a count over a corpus.
  So the ontology the type framing reaches for drops out of the rule,
  and with it the layer over [Walenty](prior-art.md)
  that would have had to supply preferences
  on top of the frames that dictionary records.

  What is left is cheap to compute.
  The pairing is a verb lemma, a preposition,
  and the noun lemma heading the phrase after it,
  which wants lemmas and no parse,
  because the head of a prepositional phrase sits beside its preposition.
  That is [the suffix finding](linter.md#suffixes-buy-more-than-expected) again:
  a rule that reads as tier C turns out to want tier B.
  What is not cheap is deciding whether it may fire.
  Rare is not wrong,
  and in fiction a rare pairing is frequently the point,
  so this entry stands on the declared register or it does not stand —
  [register is how false positives get in](linter.md#limits-worth-stating-up-front).
  Its answer depends on the site rather than on the rate,
  so it owes
  [an audit](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule),
  and it is the expensive kind to read:
  every hit is a judgement about whether the missing step comes back,
  where a quotation mark is a quotation mark.

## Morphosyntactic, tier B

- Nominalization density: `-anie`, `-enie`, `-cie` per hundred words *cited*
- Impersonal `-no` and `-to` forms, and `się` passives *cited*
- Hedges `można`, `trzeba`, `należy`, `warto` *cited*
- Adjective stacking before a noun
- Participle chains: `będąc`, `mając` *cited*
- Comparative adjective frequency *cited*
- **Ambiguous pronoun antecedent** —
  a third-person pronoun that agrees with more than one antecedent.
  Article 1 of the Universal Declaration of Human Rights reads, in Polish,
  `Wszyscy ludzie rodzą się wolni i równi pod względem swej godności i swych praw.
  Są oni obdarzeni rozumem i sumieniem
  i powinni postępować wobec innych w duchu braterstwa.`,
  where `oni` reaches back across the sentence boundary to `Wszyscy ludzie`
  and reaches nothing else.
  What keeps the pointer single is agreement rather than position.
  `oni` is masculine personal and plural,
  and an antecedent answers it in whatever case it stood in,
  so every noun phrase in the first sentence is a candidate by position
  and exactly one survives agreement:
  Morfeusz reads `ludzie` as `subst:pl:nom.voc:m1`
  and `praw` as `subst:pl:gen:n:ncol`.
  Substitute `swych niewolników`, which it reads as `subst:pl:gen.acc:m1`,
  and the filter passes two phrases where it passed one.
  The nearer of the two is the substitute,
  and what follows the pronoun settles nothing,
  since reason and conscience are said of people and slaves are people,
  so a reader who takes the pointer the other way has misread the sentence
  and has no way to find that out.

  A rule for this need not resolve the pointer.
  Its finding is that agreement failed to pick one antecedent out,
  which is a count over candidates and not a choice between them,
  and the count wants number and gender per form and no parse.
  That inverts what
  [ambiguity as a confidence measure](glr-in-practice.md#ambiguity-as-a-confidence-measure)
  makes of the same observation,
  where more than one reading is the reason to say nothing;
  here it is the entire report.
  What the count cannot be is a verdict, and the same pair says why:
  what makes the substitution ambiguous rather than merely two-candidate
  is that reason and conscience fit slaves as well as people,
  which no tier here reads.
  So a hit is a site for a reader,
  and a rule ships only if something structural makes such sites rare.

  What the count runs over is where the difficulty sits.
  Counted over forms it goes wrong twice:
  `Wszyscy` and `ludzie` are one phrase counted as two,
  and the predicative `wolni` and `równi` carry the pronoun's own features
  while being no candidate for it at all.
  Over runs of adjacent forms
  that share number, gender and case and end in a noun,
  it returns `Wszyscy ludzie` for the article
  and `Wszyscy ludzie` beside `swych niewolników` for the substitution,
  which is the distinction the rule needs.
  A run of that kind is adjacency and agreement rather than a parse,
  so the pair is settled at tier B
  where resolving the pointer would be tier D.
  One kind of antecedent is above a run anyway:
  a coordination can be a plural no form inside it carries,
  `Jan i Maria` answering `oni` where neither noun is plural or masculine personal,
  and reaching that is chunking rather than adjacency.
  The analyser sets the noise floor, not the procedure:
  the same runs over the second sentence return `braterstwa`,
  which Morfeusz reads as a masculine personal plural,
  and that is [a reading Polish does not have](subset.md#the-dictionary-offers-readings-polish-does-not).
  The tags are Morfeusz's because it is the analyser this repository runs,
  and Morfologik, which
  [the linter track takes instead](open-questions.md#settled),
  marks number and gender in a tagset of its own.

  When such a rule may fire is the undecided half.
  Two agreeing candidates need not be a defect,
  since subjecthood, recency and topic continuity
  settle pointers that agreement leaves open,
  and a plural pronoun contributes one bit of gender to the filter,
  so how often the count reaches two in edited Polish
  decides whether it may fire on the count at all.
  The pair names the configuration to measure first —
  the intended antecedent is the subject, the competitor is the nearer one,
  so the two preferences disagree,
  which cannot happen where only one candidate survives, as in the article.
  Whether that configuration is the defect
  or a property of an example built by substitution
  is what [an audit](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
  settles rather than a rate.

## Structural and statistical, tier A with sentence splitting

- Sentence-length uniformity, measured as low variance *cited*
- Paragraph-length uniformity
- Three-item list frequency *cited*
- Bullet density inside prose
- `nie tylko X, ale także Y` and other parallel-negation frames.
  The frame's commonest Polish form is punctuated rather than lexical,
  so this entry and the em dash above are one construction:
  see [generated-polish.md](generated-polish.md#what-the-em-dashes-are-doing).
  The realization with `a` belongs here and is not among the rates measured there.
  What does not belong here is the negated relative,
  `czytanie, którego polszczyzna nie ma`,
  which defines a thing by an absence and pairs nothing against anything;
  it is tier A on the same machinery, a relative pronoun and a negated verb,
  and it wants a rate of its own before it is called one construction with this.
  [CLAUDE.md](../CLAUDE.md#a-phrase-that-arrived-ready-made-was-not-chosen)
  refuses both under a single convention,
  which is a demand on prose and settles nothing about the count
- Lemma type-token ratio *cited*
- Fact density: dates, numerals, proper nouns; low in generated text *cited*
- Absence of inversion and other emphatic reorderings *cited*,
  which the fronting entry below approaches from the other direction.
  Absence is the harder of the two sides to measure.
  A count at this tier reaches the clause-fronted variant that entry names
  and not the phrase-fronted one,
  so prose that inverts only in the ways a pattern cannot see
  reads here exactly like prose that does not invert,
  the way [lack of coverage reads like a clean document](rules.md#abstention-is-not-silence)

## Discourse, tier C or D

- Promotional inflation:
  `stanowi świadectwo`, `odgrywa kluczową rolę` *cited*
- Vague attribution:
  `badania pokazują`, `eksperci twierdzą` *cited*
- Subject-predicate distance and position *cited*
- **Fronting for gravity** *cited* —
  a bare complement or a whole subordinate clause
  set before the subject and the verb:
  `Trzech pozostałych wskaźników projekt nie ustala`,
  `Czego ochrona takiego terenu wymaga, nazywa uzasadnienie projektu`.
  Plain order says the same thing at once,
  instead of asking the reader to hold the opening in memory
  until the verb arrives.
  What is cited is the position:
  the plain-Polish norm asks for subject and predicate
  near the start of the sentence,
  and fronting pushes them away from it.
  The gravity the examples reach for is nobody's norm but this entry's.
  Subject-predicate distance above counts that position in words
  and owns the interpolation case;
  this entry names the construction,
  and [why it is tier C](linter.md#recognizing-a-phrase-by-what-it-is-not-costs-more)
  is argued there.
  The clause-fronted variant is the cheap half,
  reachable at tier A as an interrogative or relative pronoun
  opening a sentence whose clause closes on a comma.
  A fronted phrase carrying the sentence's link to the one before it
  is doing work, and nothing at these tiers tells work from decoration,
  so the finding is a share of sentences over a document
  rather than an accusation against one of them.
  The absence-of-inversion entry above counts the same construction
  and reads a low rate as the generated tell,
  which makes the two a floor and a ceiling on one measurement.
  These examples are official Polish rather than model output,
  and [the calibration harness](roadmap.md#milestone-1-the-calibration-harness)
  has to say whether both hold at once, and in which register.

## From the repository's own writing conventions

The conventions in [CLAUDE.md](../CLAUDE.md) name six patterns
the groups above do not reach.
They are defects of documentation specifically,
which is the declared target register,
and they are hypotheses in Polish like everything else here.

- **Temporal anchors** — `jeszcze`, `już`, `nadal`, `na razie`, `obecnie` —
  which pin a sentence to the moment it was written
  and let documentation rot rather than merely age.
  A word list is tier A,
  but the temporal and the logical sense share a form,
  so a rule that fires on the list alone
  will flag correct Polish more often than not.
  What has to be found first is a context test that separates the two.
- **Echo sentences** — two adjacent sentences carrying one thought,
  usually a plain version and a rhetorical one side by side.
  Lemma overlap between neighbouring sentences measures it, tier B,
  with no parse involved.
- **Ungrounded superlatives and exclusivity** —
  `naj-` forms, `jedyny`, `wyłącznie`.
  Distinct from booster inflation:
  the claim is checkable in principle and simply unchecked,
  so the flag asks for grounds rather than for a smaller word.
  The `naj-` prefix is tier A+, the rest tier B.
- **The placeholder pronoun** — `coś`, `pewne rzeczy`, `takie sprawy` —
  standing where the thing itself would be named.
  Distinct from the dangling reference the reader force warns of:
  that one points at an antecedent the reader cannot find,
  and this one points at nothing and was never meant to.
  The forms are few, so the pattern is tier A,
  and it fires on correct Polish wherever the indefiniteness *is* the content,
  as in `jeśli coś pójdzie nie tak`,
  which is the same shape of problem the temporal anchors have.
- **The modal that lends a will** —
  `umie`, `chce`, `stara się`, `potrafi` in front of an infinitive
  whose subject is a thing: `gramatyka umie żądać`, `dokument chce powiedzieć`.
  Two defects arrive together and either alone is weaker:
  the modal does the work of the plain verb in two words instead of one,
  and the personification claims a mechanism nobody meant to claim,
  which is what the word-choice force refuses in a worn metaphor.
  A modal beside an infinitive is tier A,
  and deciding whether the subject is a thing is tier B,
  so what has to be measured first is how much of the pattern
  the cheap half already separates.
- **A closed set of verbs carrying every predication** —
  `stoi`, `mówi`, `bierze`, `czyta`, `trzyma`, `kupuje`,
  each standing for a different relation in each place it appears.
  This is the worn metaphor with no metaphor on the surface:
  every one of those verbs is ordinary,
  so no word list separates the tenth use from the first,
  and what makes it a defect is the share of the text they carry.
  The statistic is therefore a concentration,
  the share of finite-verb lemmas taken by the commonest few,
  and its denominator is what
  [lemma type-token ratio](#structural-and-statistical-tier-a-with-sentence-splitting)
  above does not reach:
  measured over every lemma, the verbs are diluted
  by terminology a technical document repeats on purpose,
  so the two want separating before either is calibrated.
  Lemmas and a part of speech are tier B,
  and a concentration is a statistic no declaration produces,
  so what this entry needs first is a check kind, which is code:
  [rules.md](rules.md#check-kinds) owns what the kinds are
  and what adding one costs.
  Two things stand between the count and the defect.
  `stoi` is read as `stać` and as `stoa` both,
  so a rule taking one reading per form files this pattern under a portico,
  and choosing between readings is what `olski/morph.py` refuses to do.
  That reading is Morfeusz's, because it is the analyser this repository runs,
  and the linter track takes
  [Morfologik instead](open-questions.md#settled),
  whose ambiguities are its own.
  And a verb repeats where the relation repeats,
  so what a rate here means is
  [what an audit settles](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
  rather than what a distribution does.

## Sources

- <https://pl.wikisource.org/wiki/Powszechna_Deklaracja_Praw_Człowieka> — the Polish text of the Universal Declaration of Human Rights
