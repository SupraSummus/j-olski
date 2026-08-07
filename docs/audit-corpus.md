# Repositories in the audit corpus

[corpora.md](corpora.md#the-audit-corpus-polish-documentation-in-version-control)
argues for an audit corpus that grows by admitting a repository
rather than by gathering words.
This is the list that argument asks for:
what a repository has to show to be admitted,
which ones are in, and the commit each figure below was taken at.

A repository named in a paragraph cannot be cloned by a command,
and a paragraph has nowhere to carry the reason the repository belongs in the corpus.
A section per member carries both,
so that a second person fetches the same bytes
and reads why that prose counts as Polish that was written in Polish.

## What a repository has to show

Four things.
Three are the demands
[corpora.md](corpora.md#what-a-corpus-has-to-say-about-itself) makes of a corpus,
narrowed to what one repository can answer for,
and the fourth is what the extraction needs.

- **Its documentation was written in Polish first.**
  No licence field records this and no metadata answers it,
  so somebody establishes it and the member's section below says how.
  What makes it answerable per repository at all
  is that a repository has one subject, the system it documents,
  where the same question asked of
  [NKJP](corpora.md#it-does-not-record-whether-a-text-is-a-translation)
  is 3,889 samples to trace one at a time.
- **It is documentation.**
  The pack is scoped to a register,
  and a hit read over a prospectus or over a page of links
  is a hit read outside the register the rule was built for.
- **Its prose is in version control, at a commit that can be named.**
  [What the survey settles](corpora.md#what-the-survey-settles) turns on this:
  a typographic rule can be audited only over text
  that reached its reader through no step that rewrote its characters,
  and a clone is the case where that is checkable rather than assumed.
  The pin is also what makes a figure here reproducible,
  since a repository goes on being written after it is admitted.
- **A format the extraction reads.**
  `harness/markdown.py` reads Markdown, and
  [roadmap.md](roadmap.md#the-two-pieces-are-not-the-same-size)
  makes admitting a repository the step that decides
  whether a second extraction gets written.
  The `Markdown files` column below is where that shows:
  a member in another format changes the column,
  and brings the extraction it needs with it.

Licence is recorded and is not a fifth demand.
[Milestone 1](roadmap.md#milestone-1-the-calibration-harness)
exits on numbers taken over a corpus anyone can fetch,
which a public repository satisfies whatever its terms say,
because this list ships no text: it ships a URL and a commit.
What a licence decides is the narrower question
of whether extracted prose can be published beside a figure taken over it.
So a repository with no licence file joins with the gap written down,
and its prose stays where it was cloned from.

## The list

| repository | Markdown files | words of prose | licence | authors |
| --- | --- | --- | --- | --- |
| [CIRFMF/ksef-docs](https://github.com/CIRFMF/ksef-docs) | 32 | 23,825 | MIT | 9 |
| [pot-gov-pl/rit-dokumentacja](https://github.com/pot-gov-pl/rit-dokumentacja) | 7 | 15,112 | none stated | 2 |

39 files and 38,937 words of prose.
Five of the 39 extract to nothing,
being files of tables and code blocks with no sentence in them.

One run fetches the corpus and builds its prose.
The commits sit in the command rather than in a column of their own,
so that the pin a figure was taken at
and the pin a rerun checks out cannot come apart:

```sh
git clone https://github.com/CIRFMF/ksef-docs
git -C ksef-docs checkout -q 1c34fe2
git clone https://github.com/pot-gov-pl/rit-dokumentacja
git -C rit-dokumentacja checkout -q 32f85cc
python3 -m harness.markdown ksef-docs --into proza/ksef
python3 -m harness.markdown rit-dokumentacja --into proza/rit
python3 -m olski proza --format report --packs harness/counts.py \
                                       --packs olski.packs.typography
```

`--depth 1` is not in the clone,
because a shallow clone cannot check out the commit that follows it.
The word counts are of extracted prose rather than of the files as they stand,
and [extraction.md](extraction.md) holds what that step costs.
The author counts are of the commits touching each repository's Markdown,
which is a proxy for who wrote the prose rather than a count of them.

## CIRFMF/ksef-docs

The API documentation of Krajowy System e-Faktur,
the Polish national e-invoicing system,
published by the Ministry of Finance.

**Polish first** for the reason
[corpora.md](corpora.md#polish-technical-documentation-original-and-translated) gives,
that the system, its law and its readers are Polish.
What the repository adds to that is an absence:
it holds no version of any of these files in another language
for the Polish to have been rendered from,
where a translated pool keeps the source beside the translation.

**MIT**, in `LICENSE.txt`, which reads `Copyright (c) 2025 Ministerstwo Finansów`.

**The caution beside it** is that nine authors are not nine hands on the prose.
394 commits touch its Markdown
between 2025-07-11 and the pinned commit of 2026-07-21,
and 320 of them are one person's.
Nine tenths of its straight quotation marks are in one file,
`api-changelog.md`, which quotes API error messages release by release
([corpora.md](corpora.md#polish-technical-documentation-original-and-translated)
has that count and what it is evidence of).

## pot-gov-pl/rit-dokumentacja

Documentation of Repozytorium Informacji Turystycznej,
the tourism information register of Polska Organizacja Turystyczna:
two descriptions of its REST API, a guide to its WSDL interfaces,
an annex written into a procurement specification,
and editorial guidelines for the register's own editors.

**Polish first** because every reader it addresses is Polish.
The guidelines instruct the register's editors on writing entries,
the annex is drafted to go into a Polish public tender,
and the API documents are written for the integrators of a Polish state system.
As with KSeF, no file in it has a counterpart in another language.

**No licence.** The repository carries no `LICENSE` file,
and the only mentions of licensing in its Markdown are its subject matter —
the terms under which the register may publish a photograph —
rather than its own terms.
Under [what a repository has to show](#what-a-repository-has-to-show)
that bars publishing its prose beside a figure and does not bar the figure.

**The caution beside it** is that four of the six documents beside the README
are marked *Wycofany z użytku*, withdrawn from use —
the editorial guidelines are marked current and one REST description carries no status —
and the last commit is 2022-11-09,
so this is documentation of a system as it was left rather than as it runs.
60 of its 61 Markdown commits are one person's,
so what it adds to the corpus is one writer rather than two.

## What a second repository buys

The prose extracted from the two carries 750 straight quotation marks,
279 of them in `api-changelog.md`.
Over one repository the largest file holds nine tenths of that statistic,
and over two it holds 37%,
which is what admitting a repository is for:
the corpus grows in authors, and in words only incidentally.

That share is the number to watch as the list grows,
because it says how far a rate over this corpus is still one person's habit.
Which repositories join beyond these two,
and how many it takes before the share stops mattering,
is [a question corpora.md keeps](corpora.md#not-yet-decided).

## Sources

- <https://github.com/CIRFMF/ksef-docs> — the KSeF API documentation, its history and its MIT licence
- <https://github.com/pot-gov-pl/rit-dokumentacja> — the RIT documentation and its history
- <https://github.com/gakowalski/foss-in-gov-pl> — a catalogue of open-source repositories of Polish state institutions, where a search for members can start
