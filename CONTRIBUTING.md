# Contributing

## Semantic line breaks

All prose in this repository follows
[Semantic Line Breaks](https://sembr.org) (sembr).
Instead of hard-wrapping at a fixed column
or putting each paragraph on one long line,
break lines at boundaries of meaning.

The rules, in order of precedence:

1. A line break must not change the rendered meaning of the text.
2. Insert a line break after a sentence.
3. Insert a line break after an independent clause
   punctuated by a comma, semicolon, colon, or em dash.
4. Optionally insert a line break
   after a dependent clause,
   a long phrase,
   or a list item.

Markdown collapses a single newline into a space,
so the rendered output is identical either way.
What changes is the diff:
a reworded sentence touches only the lines that actually changed,
instead of reflowing an entire paragraph
or producing one unreadable single-line diff.

### What this applies to

- Markdown files (`*.md`)
- Plain text files (`*.txt`)
- Commit message bodies
- Pull request descriptions
- Long comments in source files

Code itself is unaffected;
format it however the language's usual tooling says.

### Practical notes

- Do not use two trailing spaces for a hard line break.
  Trailing whitespace is stripped in this repository
  (see `.editorconfig`).
  If you need a real `<br>`,
  end the line with a backslash
  or start a new paragraph.
- Do not reflow lines you are not otherwise editing.
  Gratuitous rewrapping makes diffs unreviewable,
  which is the exact problem sembr exists to solve.
- Line-length linting is disabled
  (see `.markdownlint.jsonc`),
  because sembr line lengths are meant to vary.
- Turn off automatic hard-wrap in your editor for Markdown.
  Soft wrap is fine and recommended.

### Converting existing prose

The [`sembr`](https://github.com/admk/sembr) tool
inserts breaks automatically using a fine-tuned model:

```sh
pip install sembr
sembr -i path/to/file.md
```

It is a convenience, not a requirement,
and its output still deserves a read-through before committing.
