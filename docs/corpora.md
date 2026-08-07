# Sourcing the human half

[linter.md](linter.md#the-thing-that-makes-or-breaks-it-calibration)
needs a paired corpus,
and [milestone 1](roadmap.md#milestone-1-the-calibration-harness)
calls the human half the blocking one.
This document is the survey behind that half:
what Polish is obtainable, and what each body of it can and cannot support.

The answer it arrives at is that no existing corpus serves.
The register olski is scoped to is nearly absent from the corpora that exist,
the corpus that would say whether a text is a translation does not record it,
and the typography a linter measures
has been normalized out of the largest one.
So the good side is assembled from named parts rather than chosen,
and it is two corpora rather than one,
because a rule reporting a rate wants prose an editor worked on
and a rule whose hits get read wants prose nobody touched after the author.

## What a corpus has to say about itself

Five things, each demanded by something already decided.

- **Licence.**
  Milestone 1 exits on numbers taken
  over a corpus anyone can fetch and a run anyone can redo,
  so a corpus that cannot be redistributed or downloaded
  can produce a number nobody can check.
- **Size.**
  A threshold is a point in a distribution,
  and a distribution needs enough text to have a shape.
  A rule whose hits get read instead of counted needs no shape,
  so what is a starved corpus for one demand is a working one for the other.
- **Register.**
  A pack is scoped to a register,
  and a threshold read off a different one accuses the writing it was built to protect.
- **Provenance.**
  The rules against anglicisms and calques
  need Polish that was written in Polish.
  A baseline translated from English licenses exactly what they flag.
- **Stage of production.**
  [linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
  argues a typographic rule measured against typeset prose is measured against nothing,
  because the corpus could not have held what the rule looks for.

Stage of production is the column that splits the answer in two,
because no body of Polish is both worked on by an editor
and untouched since its author,
and the two shapes of rule want one each.

## How the counts here were taken

Every figure below that is not attributed to somebody else
was taken on 2026-08-07,
over the files as they stand,
by fetching a corpus with the command printed beside it
and counting words and characters over what came down.
Each count says which files it ran over and which selection of them,
so that a second person picks the same text;
what it does not come with is the program that did the counting,
which was written for this survey and is not in this repository.

That is the defect [TODO.md](../TODO.md) already records
against the rates in
[generated-polish.md](generated-polish.md#what-was-measured),
and it closes the same way.
`olski --format report` prints a per-rule rate over a corpus,
which is the run the typographic counts here approximate by hand,
and what stands between the two is the extraction that entry asks for.
Until it lands, a figure here is checkable by rewriting the count,
which the stated selection makes possible and does not make free.

These are counts of characters and words rather than rule firings either way,
and they are here to characterize a corpus rather than to calibrate anything.

The crude extraction they use has the price
[generated-polish.md](generated-polish.md#the-extraction-has-a-price-of-its-own)
already names.
Removing fenced and inline code from one of the Markdown corpora below
leaves 280 runs of two or more spaces,
and every one of them is padding inside a Markdown table.
That figure is therefore not reported as a finding,
which is the shape of correction an unaccounted extraction needs
everywhere else as well.

## The National Corpus of Polish

Narodowy Korpus Języka Polskiego is the reference corpus of contemporary Polish,
built 2007–2011 by IPI PAN, the Institute of Polish Language, PWN and Łódź.
It holds 1.5 billion words,
of which a 250-million-word subcorpus is balanced by readership
and a 1-million-word subcorpus of that is manually annotated.

Only the 1-million-word subcorpus is downloadable.
It carries CC BY, and the rest is reachable through
the Poliqarp and PELCRA search interfaces and not otherwise.

```sh
curl -L -o nkjp1m.tar.gz \
  'http://clip.ipipan.waw.pl/NationalCorpusOfPolish?action=AttachFile&do=get&target=NKJP-PodkorpusMilionowy-1.2.tar.gz'
tar xzf nkjp1m.tar.gz
```

### Its register composition, from the file it ships

`statystyki.txt` inside the archive gives the breakdown by text type,
over 1,003,956 words in 3,889 samples,
and the taxonomy that names each type is in `NKJP_1M_header.xml`:

| type | words | | |
| --- | --- | --- | --- |
| `typ_publ` | 495,662 | 49.4% | journalism |
| `typ_lit` | 164,543 | 16.4% | fiction |
| `typ_konwers` | 58,459 | 5.8% | conversational |
| `typ_inf-por` | 54,284 | 5.4% | informative and instructive writing |
| `typ_fakt` | 52,600 | 5.2% | non-fiction novel |
| `typ_net_interakt` | 50,510 | 5.0% | interactive internet |
| `typ_urzed` | 30,539 | 3.0% | legal and official |
| `typ_qmow` | 25,212 | 2.5% | quasi-spoken |
| `typ_media` | 23,408 | 2.3% | spoken from the media |
| `typ_nd` | 19,438 | 1.9% | academic writing |
| `typ_net_nieinterakt` | 18,937 | 1.9% | non-interactive internet |
| `typ_nklas` | 9,890 | 1.0% | unclassified non-fiction book |
| `typ_listy` | 411 | 0.04% | letters |
| `typ_lit_poezja` | 63 | 0.006% | poetry |

Two of those rows could hold olski's register, and neither does.
Reading the titles of the 56 `typ_inf-por` samples in their headers
gives dream dictionaries, travel guides, astrology, cookery and self-help:
*Sny – klucz* at 3,577 words is the largest,
then *Wielkopolska : przewodnik*, *Przewodnik po Polsce*, *Wielki sennik współczesny*.
One sample out of the 56 is documentation of a computer system,
*TAG 3.1 dla opornych*, and it runs to 974 words.
The 19,438 words of academic writing are university textbooks —
*Meteorologia dla geografów*, *Glacjologia*, *Podstawy bankowości* —
and those are the closest thing in the corpus
to the expository Polish a pack for technical documentation is scoped to.

So the register is present at 7.3% of the subcorpus if textbooks count,
and at about a thousand words if only documentation does.

### It does not record whether a text is a translation

Each sample's `header.xml` carries a title, an author, a publisher,
a publication date and the text class above.
Across all 3,889 of them, no header names a translator,
an editor or a responsibility statement:

```sh
grep -l 'respStmt\|<editor\|translat' */header.xml | wc -l   # 0
```

The question the calque rules ask cannot be answered from this metadata,
and answering it by hand means identifying the source of each of 3,889 samples.

### Its text layer has been character-normalized

Concatenating the `<ab>` paragraphs of every `text.xml`
gives 985,308 words carrying 10,055 straight `"` against 530 `„`,
and 9,535 en dashes against 241 em dashes.
The straight marks are in the running text of 1,088 of the 3,889 samples,
books and dailies alike,
and they are ordinary quotations: *autor "Krótkich dni"*, *W "Babim lecie"*.

Whatever produced that — the source digitizations or the corpus build —
it settles what NKJP can be used for:
a `quote-straight` rate measured here measures the encoding.
It is also why
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
asks these rules for prose that reached its reader
through no step that rewrote its characters,
rather than for prose from before a typesetter.

Two smaller limits.
Of the 349,370 words whose header carries a publication date,
the median falls in 2000, and the range runs 1957 to 2008,
so the corpus predates the prose olski is aimed at by a generation.
And the manually annotated subcorpus is the balanced one,
so its 49.4% journalism is a design target met
rather than an accident to be sampled around.

## Wolne Lektury

A library of Polish literary works,
in the public domain or under CC BY-SA 3.0 or the Free Art Licence 1.3,
with a JSON API and per-work text, XML, EPUB and audio exports.
The catalogue holds 7,651 works.

```sh
curl -s 'https://wolnelektury.pl/api/books/?format=json'
```

Three properties of it are in the catalogue's own metadata.

**It is mostly verse.**
5,275 of the 7,651 works are `Liryka`, 2,032 `Epika` and 342 `Dramat`.
A corpus of Polish prose extracted from it is a quarter of what the count suggests.

**It is period-marked.**
By epoch the catalogue runs
Współczesność 2,614, Romantyzm 1,056, Modernizm 960, Pozytywizm 817,
Dwudziestolecie międzywojenne 726, Renesans 510, Oświecenie 305,
Barok 166, Starożytność 137, Średniowiecze 15.
That is the trap [fiction.md](fiction.md#what-this-means-for-olski)
names for cliché mining, and its cause is the licence:
a library of public-domain Polish is a library of what copyright has released.

**A seventh of it is translated.**
1,148 of the 7,651 detail records name a translator, which is 15.0%.
The library commissions translations as well as hosting old ones,
so this is a standing property rather than a legacy of digitization.

Typographically it is the opposite of NKJP.
The first forty `Epika` entries the catalogue returns
— thirty-eight of them, the other two being collections with no text export —
are 1,434,945 words carrying 5,591 `„` and 5,562 `”` against 12 straight `"`.
They also carry 32,782 em dashes, which is 22.8 per thousand words,
against the 10 per thousand `em-dash-density` allows.
Polish prose introduces dialogue with a dash,
so a literary corpus measures dialogue punctuation on that statistic
and not the construction the rule is aimed at —
the same confusion as the link lists in
[generated-polish.md](generated-polish.md#the-apparatus-biases-a-rate-by-an-amount-the-corpus-decides),
with an editorial convention rather than markup doing it.

Wolne Lektury is therefore not the human side for a technical pack,
on register, on provenance and on period at once.
It would be the obvious corpus for a fiction pack,
which [linter.md](linter.md#and-fiction) files as a wish.

## PolEval, and the one dataset in it that pairs

PolEval is an evaluation campaign for Polish
running task editions from 2017 onward,
each releasing its own data under its own terms —
the DiaBiz sample used for punctuation prediction in 2022, for instance,
is CC BY-SA-NC-ND, and prose pulled out of a corpus is a derivative of it,
so a no-derivatives task set can be measured and cannot be shipped.
The campaign is a source of task data rather than of a register-balanced corpus,
with one exception, and the exception is aimed at olski's problem.

**Śmigiel** is the dataset of PolEval 2025's first task,
machine-generated text detection for Polish.
It is CC BY 4.0, published on Zenodo,
and it holds 64,000 postprocessed fragments,
32,000 human-written and 32,000 machine-generated,
with a raw corpus of over 462,000 generations behind them.

Its human side is drawn from six domains,
each from a named dataset with a permissive licence:
literature (the Polish Library of Science Corpus,
open Polish coursebooks, and the public-domain texts of Wikiźródła),
reviews (PolEmo, Allegro Reviews, Filmweb),
social media (TwitterEmo, BAN-PL),
Polish Wikipedia, Polish Wikinews, and ParlaMint parliamentary transcripts.
Its machine side comes from eight open-weight models
in three size tiers, from Bielik-7B to Llama-3.3-70B,
each prompted with a prefix taken from a human fragment.

Two things about it matter here, and they pull in opposite directions.

**The machine half was generated for the purpose.**
That is the condition
[generated-polish.md](generated-polish.md#what-this-corpus-cannot-support)
sets on the generated half and the corpus it measures fails.
The pipeline the paper describes is prompting, filtering
— about a third of the generations were discarded —
and length normalization,
with no editing pass in it,
so what shaped the surviving fragments was a filter rather than a writer.

**Neither half is in the register, and neither half is a document.**
The six domains do not include technical documentation.
The fragments are passages, length-normalized,
and every machine fragment continues a human prefix
rather than answering a brief, which is not how the prose olski checks is written.

The typographic state of the training split says the same thing with numbers.
Over 35,763 fragments, split by the released label file:

| | fragments | words | `"` | `„` | `—` | em dashes per 1000 |
| --- | --- | --- | --- | --- | --- | --- |
| human | 17,873 | 1,809,311 | 13,631 | 3,176 | 1,308 | 0.72 |
| machine | 17,890 | 1,739,720 | 18,472 | 1,358 | 587 | 0.34 |

Both sit two orders of magnitude below the threshold `em-dash-density` sets,
and the machine half sits below the human one,
which is the reverse of the direction
[generated-polish.md](generated-polish.md#the-em-dash-rate-has-room-above-the-threshold)
found at 35.9 per thousand
over generated Polish written as whole notes
rather than as continuations of somebody else's sentence.
One of the thirteen human source labels reaches the threshold's neighbourhood:
the fragments marked `classics` run 1,035 em dashes over 105,643 words,
or 9.80 per thousand,
for the dialogue reason Wolne Lektury gives above.
A rate is a property of a register, a writer and a task at once,
and a corpus assembled for detection holds none of the three olski is aimed at.

The state also varies by source inside one half:
human Wikipedia carries 2,072 `„` and 2,045 `”` over 678,486 words,
which is Polish quotation used correctly,
while human Filmweb reviews carry 5,672 straight `"` against 38 `„`.
Stage of production is a property of each source and not of the corpus.

## Polish technical documentation, original and translated

This is the register the linter is scoped to,
and it is the hardest of the five to satisfy,
because the bodies of it that are easiest to fetch are translations.

**The translated pool announces itself.**
`python/python-docs-pl`, the Polish translation of the Python documentation,
is 501 PO files holding 1,999,845 words of English source
against 169,936 Polish words in 11,589 of 86,735 strings.
Every Polish word in it sits in a `msgstr` beside the `msgid` it came from,
so the storage format records the provenance
that NKJP's headers do not.
The Kubernetes documentation localizes into Polish the same way,
contributor guide and terminology glossary included,
so the arrangement is a convention rather than one project's choice.
A corpus built from these would be the baseline
[open-questions.md](open-questions.md#linter-questions) warns about:
a rule against `w oparciu o` measured against prose
produced by rendering *based on* into Polish
reports the translator's habit as the norm.

**The original pool has to be gathered repository by repository.**
The largest single item found is the API documentation
of the Polish national e-invoicing system,
published by the Ministry of Finance under the MIT licence:

```sh
git clone --depth 1 https://github.com/CIRFMF/ksef-docs
```

32 Markdown files, 31,286 words once fenced and inline code are removed.
It is written in Polish because the system, its law and its readers are Polish,
which is the property that makes a repository worth adding
and the one no licence field records.
Beyond it the pool thins quickly.
`pot-gov-pl/rit-dokumentacja` is a handful of files,
and the catalogue of open-source repositories of Polish state institutions
covers 21 institutions across 25 GitHub accounts
without describing a single one of their repositories as documentation.

Its typographic state is the reason this material is worth the gathering.
Straight quotation marks outnumber `„` by 332 to 13,
en dashes outnumber em dashes by 148 to 12,
and the straight marks are around Polish phrases in running prose —
*"Uwierzytelnianie zakończone niepowodzeniem z powodu błędnego tokenu"*,
*"Profil Zaufany"*, *"Certyfikat zawieszony"*.
This is prose caught at the stage the linter runs at,
holding what NKJP and Wolne Lektury cannot hold.

The distribution of those hits is the caution that goes with the finding.
279 of the 332 are in `api-changelog.md`,
which quotes the wording of API error messages release by release,
so one document with one habit supplies five sixths of them.
A pack audited against this repository alone
would be audited against a handful of authors,
which is the argument for the corpus being a list of repositories
rather than a repository.

## The expository Polish that is obtainable

Between the register that barely exists
and the corpora that are the wrong register
sits edited expository Polish, and this is what there is of it.

**PLSC**, the Polish Library of Science Corpus,
is 159,767 records of title, abstract, journal and discipline
from Polish scientific journals, 194 MB of them, under CC0.
It is the only body in this survey
whose licence asks nothing of whoever redistributes it.
Two things it is not.
An abstract is a paragraph written to a house convention, not running documentation.
And a Polish journal publishing in English still carries a Polish abstract,
which is then a translation, so the pool is Polish-first in part and not throughout.

**Polish Wikipedia** is 1,703,870 articles and 561,399,817 article words
under CC BY-SA 4.0, with dumps and an API.

```sh
curl -s 'https://pl.wikipedia.org/w/api.php?action=query&meta=siteinfo&siprop=statistics&format=json'
```

It is expository and edited by more than one person,
and the per-article provenance is not recorded any more than NKJP's is.
An article's interlanguage links and its own edit history
are where an answer for one article would come from,
and neither has been read here for any of them.

**Polish Wikibooks** is 7,216 articles and 5,802,842 words under CC BY-SA 4.0,
by the same query against `pl.wikibooks.org`.
That is a hundredth of Wikipedia,
in the instructive register documentation is nearest to.

**Open Polish coursebooks**, the `open-coursebooks-pl` dataset,
is 1,528 chapters of Polish coursebook material, 4.8 MB, under CC BY-SA 4.0,
written in Polish rather than translated into it.

**SpeakLeash** aggregates Polish text with a per-source manifest
recording licence, category and size for each dataset it holds,
which makes it the place to look for slices of the above rather than a corpus itself.
Which of its datasets are in this register, and under what terms,
is not checked here.

## What the survey settles

**The target register is nearly absent from the corpora that exist.**
Seven percent of NKJP's downloadable subcorpus is instructive or academic writing,
one sample of it is documentation of a computer system,
and Śmigiel's six domains do not include the register at all.
Anyone wanting a distribution over Polish technical documentation
assembles it; nobody has assembled it already.

**Provenance is recorded in the data only where the data is translated.**
NKJP names no translator, and Wikipedia names no source article,
while a PO file keeps the English beside every Polish string it holds.
A rule against calques therefore needs material
whose Polish-first origin somebody established when they gathered it,
which makes provenance a property of the gathering rather than of the corpus,
and makes it something this repository has to write down
rather than something a corpus can be asked for.

**Stage of production is a property of the corpus build, not of the typesetter.**
NKJP's text layer and Wolne Lektury's prose disagree
by a factor of three and a half thousand
on how often a Polish quotation opens with `„` rather than with `"`,
which is one statistic over one language,
so at most one of them describes Polish practice
and nothing in either says which.
A typographic rule can be audited only over text
that reached its reader through no step that rewrote its characters,
and a repository cloned from version control is the case
where that can be checked rather than assumed.

## The composition this argues for

Two corpora, because the two shapes of rule in
[linter.md](linter.md#what-a-rate-on-human-polish-means-depends-on-the-rule)
want different prose, and one corpus cannot be both.

### The audit corpus: Polish documentation in version control

Original Polish technical documentation, cloned from a list of repositories
kept in this repository, prose extracted from Markdown and AsciiDoc,
fenced code dropped.
Every rule whose answer depends on the site rather than on the rate audits here:
the whole typography pack, and any later rule with the same property.

It is small on purpose, and it is a list rather than a body.
An audit reads its hits, so tens of thousands of words is a working corpus,
and one repository of that size supplies more hits than an afternoon settles.
What one repository cannot supply is authors:
five sixths of KSeF's straight quotation marks are in one of its files.
So the corpus grows by adding repositories rather than by adding words,
and the list is where the admission test is written down —
a repository joins if its documentation was written in Polish first,
with the reason it was recorded beside it.

### The distribution corpus: edited original expository Polish

For every rule reporting a rate against a norm.
Proportions by words, with the reason each is capped where it is:

| share | source | why it is capped there |
| --- | --- | --- |
| 50% | PLSC abstracts, CC0 | the largest, and the only licence that asks nothing; abstracts rather than running prose, and Polish-first only in part |
| 25% | Polish Wikipedia, technical and scientific categories, CC BY-SA 4.0 | supplies the running prose abstracts cannot; per-article provenance unread |
| 15% | Polish Wikibooks and open coursebooks, CC BY-SA 4.0 | the instructive register, which is the nearest one to documentation; between them a few million words |
| 10% | NKJP `typ_nd` and `typ_inf-por`, 73,722 words, CC BY | printed-book prose an editor worked on, in a balance somebody else designed; a median dated text from 2000, and an instructive half that is dream books and travel guides |

The principle behind the numbers is that each source's share
is bounded by the defect it is known to carry,
so that no single defect can set a threshold on its own.
The numbers themselves are a starting point rather than a result,
and the run that corrects them is cheap:
recompute every threshold with each source dropped in turn,
and a threshold that moves when one source leaves
is a threshold measuring that source.

Wolne Lektury is in neither corpus.
It is verse, it is period-marked, a seventh of it is translated,
and on the one statistic a shipped rule measures
it sits at twice the rule's threshold for a reason that is Polish orthography.

### The generated half

Śmigiel is the only generated Polish in this survey
that is openly licensed and describes a pipeline with no editing pass in it,
and it cannot be the only generated half.
It meets the condition
[generated-polish.md](generated-polish.md#what-this-corpus-cannot-support)
sets, and it fails the register and the task,
being fragments continuing human prefixes in six domains that exclude documentation.
So it enters as the second opinion,
the corpus that says whether a rate belongs to the register or to the model,
and the primary generated half remains one produced in the register, from briefs.

One overlap has to be kept in view when it is used that way.
PLSC and the open coursebooks are in the distribution corpus above
and in Śmigiel's human half both,
so the two human sides are not independent samples of anything,
and a difference between them understates by however much they share.

That also answers what
[generated-polish.md](generated-polish.md#not-yet-decided) asks about the corpus
it measures.
With an unedited generated half obtainable,
a body edited against style detectors is not needed as the generated half,
and stays what that document calls it: a floor, and the harder case.

## Not yet decided

- Whether a Wikipedia article's provenance can be established at scale.
  Interlanguage links and the article's own history are the obvious places to look,
  and neither has been checked.
- Whether PLSC's abstracts are Polish-first.
  A Polish journal publishing in English carries a translated Polish abstract,
  and the dataset records the journal, which is where the answer starts.
- Which repositories join the audit corpus beyond the two named here,
  and how many authors it takes before a hit rate in it
  stops describing whoever wrote the largest file.
- Whether SpeakLeash's manifests hold a slice of this register
  that would be cheaper than gathering one.

## Sources

- <http://clip.ipipan.waw.pl/NationalCorpusOfPolish> — the downloadable NKJP subcorpus and its licence
- <https://nkjp.pl/index.php?page=14&lang=1> — NKJP's own list of what it publishes and under what terms
- <https://www.uni-goettingen.de/de/document/download/cbcf2e9ded91b3c41d0c460c31d1d9bb.pdf/nkjp.pdf> — Przepiórkowski on the corpus's design and its readership-balanced targets
- <https://wolnelektury.pl/info/o-projekcie/> — Wolne Lektury on its own licences and commissioned translations
- <https://wolnelektury.pl/api/> — the API the catalogue figures come from
- <https://poleval.pl/> — the PolEval campaign and its editions
- <https://aclanthology.org/2025.poleval-main.2/> — the Śmigiel shared task, its subsets and its results
- <https://zenodo.org/records/18919631> — the Śmigiel dataset, its sources, its generators and its licence
- <https://github.com/CIRFMF/ksef-docs> — the KSeF API documentation, MIT
- <https://github.com/python/python-docs-pl> — the Polish translation of the Python documentation
- <https://kubernetes.io/pl/docs/contribute/localization-pl/> — the Kubernetes Polish localization and its glossary
- <https://github.com/gakowalski/foss-in-gov-pl> — a catalogue of open-source repositories of Polish state institutions
- <https://huggingface.co/datasets/rafalposwiata/plsc> — the Polish Library of Science Corpus
- <https://huggingface.co/datasets/rafalposwiata/open-coursebooks-pl> — open Polish coursebooks
- <https://speakleash.org/> — SpeakLeash, and the manifests it publishes beside each dataset
