# Notes for AI agents

## Prose formatting

This repository uses [Semantic Line Breaks](https://sembr.org).
When you write or edit Markdown, plain text, commit messages,
or pull request descriptions:

- Break after each sentence.
- Break after independent clauses
  (those punctuated by a comma, semicolon, colon, or em dash).
- Never break in a way that changes the rendered meaning.
- Do not hard-wrap at a column,
  and do not put a whole paragraph on one line.
- Do not reflow lines you are not otherwise changing;
  keep diffs limited to the clauses you actually touched.
- Do not use two trailing spaces for a hard break
  (trailing whitespace is trimmed).

See `CONTRIBUTING.md` for the full convention.

## Rewriting history

Squashing has gone wrong here once,
in the way that is easy to miss,
so these are not general advice but the specific traps that were hit.

**`origin/main` can be stale, including in a fresh clone.**
The remote's `main` moved mid-session
while the remote-tracking ref still held the value
fetched when the container started.
Run `git fetch origin main`
before using main as a base, a diff target, or a squash point.
A fresh clone is not a guarantee that anything stayed still afterwards.

**Squash onto the parent of your own first commit,
not onto a branch name.**
Find that commit explicitly
and reset to `<your-first-commit>^`.
Resetting to `origin/main` or any other name
aims at a ref whose value you have not checked,
and if it turns out to sit further back than you thought
you will silently absorb commits somebody else wrote.

**Check what you are about to rewrite, before you rewrite it.**
`git log --oneline <base>..HEAD` should list your commits and nothing else.
If a diffstat contains files you never touched,
the base is wrong.

**Never rewrite a commit you did not author in this session.**
Its message and authorship are somebody's work.
Absorbing it into a squash destroys both,
and the loss is not visible in the resulting tree,
which is why it has to be caught before the push
rather than after.

**Verify the squash preserved the content.**
`git diff <squashed> <original-head>` must be empty.
