[← Lint](../README.md)

# codespell

<https://github.com/codespell-project/codespell>

---

## The problem it solves

The same problem [`typos`](../typos/README.md) solves, arrived at first and by a different route.

Spell checking a code repository with an ordinary dictionary does not work: nearly every
identifier, package name and acronym is an unknown word, so the output is noise and the check gets
removed. codespell avoids that by never consulting a dictionary of valid words at all. It carries
a **list of common misspellings and their corrections** — built up over more than a decade of
contributions — and reports only what appears in that list.

Everything else is left alone. An unrecognised identifier is not a finding, because
unrecognisability is not evidence of anything in a codebase.

The dictionary is the asset. It has been curated in the open for years, includes multiple
correction candidates for ambiguous cases, and is split into optional sets so a project can decide
how aggressive it wants to be — the rarer sets catch more and are more likely to argue with valid
words.

## When to use it

- **any repository**, as a pre-commit hook or a CI step — it is cheap in every sense
- a project that already uses it; there is no reason to switch away
- Python-first environments where a Python tool is one fewer toolchain to install
- when the broadest available correction list matters more than raw speed
- on documentation and comments in particular, where typos accumulate unread

## When not to use it

- expecting it to find every misspelling; it finds the common ones and nothing else
- with the most aggressive dictionary sets enabled by default — those are where the false
  positives are
- as a substitute for review, or for grammar and style — style is
  [Vale](../../../../docs/authoring/vale/README.md)
- as a reason to add a second tool if [`typos`](../typos/README.md) is already in place; the
  overlap is large

## Where it is used

Worth stating plainly, because installed base is a real argument for a tool whose value is its
dictionary. codespell runs in the **Linux kernel**'s checking scripts and in a large number of
long-standing open-source projects, which is both why the correction list is as good as it is and
why it keeps improving — every false positive somebody reports upstream is fixed for everyone.

That is the strongest thing about it, and it is not a technical property.

## Running it

It reports by default and fixes on request. Two operational details matter more than the rest:

| Concern | What to do |
|---|---|
| **Applying corrections** | it can rewrite files in place; do that in a **separate commit** from feature work, as [`../README.md`](../README.md#6-adopting-a-linter-on-code-that-already-exists) requires of every linter fix |
| **Ambiguous corrections** | where a misspelling has more than one plausible intended word, it reports rather than guesses — these need a human, and they are the reason not to apply fixes blindly |
| False positives | ignore per word rather than per file, and comment why |
| Generated and vendored files | skip by path; there is nothing to gain from spell-checking a lock file |

The ambiguous case is the one that catches people out. Automatic fixing across a large repository
will produce a diff nobody reads, and a wrong automatic correction in prose is worse than the
original typo because it looks deliberate.

## codespell or typos

The comparison table lives in one place rather than two — see
[`../typos/`](../typos/README.md#typos-or-codespell).

The summary: **codespell has the larger installed base and the longer-curated dictionary; typos is
substantially faster and has fewer false positives by design.** Both are cheap enough that the
choice barely matters, and neither replaces somebody reading the text. The default recommendation
in this folder is typos, on speed; codespell is the right answer for any project already running
it.

## Notes

Written in Python, distributed on PyPI, with a pre-commit hook and a GitHub Action. Configuration
can live in `setup.cfg` or `pyproject.toml`, which is convenient in a Python project and irrelevant
elsewhere.

**Not present in this repository, and it is a genuine gap — but the one that gets filled is
[`typos`](../typos/README.md).** Both would work; the tie-break is that this repository's Python
tooling recommendation is already Ruff, a Rust tool chosen for speed, and the same reasoning
applies here. Pre-commit hooks compete for the same few seconds of a developer's patience, and
every one that is slow makes the whole set more likely to be skipped.

codespell is catalogued anyway because it is the tool most external projects use, and knowing why
the two exist is more useful than knowing only the newer one.

---

[← Lint](../README.md)
