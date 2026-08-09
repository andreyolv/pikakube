[← Lint](../README.md)

# typos

<https://github.com/crate-ci/typos>

---

## The problem it solves

Spell checking source code has a bad reputation, and it is deserved. A conventional spell checker
works by comparing every word against a dictionary and reporting what is missing — and a code
repository is almost entirely words that are missing from the dictionary. Identifiers, package
names, acronyms, flags, hostnames. The output is thousands of findings, the response is a
project-specific word list that nobody wants to maintain, and the check is abandoned.

**typos inverts the question.** It does not look for unknown words. It looks for *known
corrections* — a curated set of misspellings mapped to what they were meant to be. `recieve`,
`sucessful`, `paramter`, `enviroment`. If a word is not in that set, typos says nothing about it,
regardless of whether it is a real word.

| Approach | Reports | Cost |
|---|---|---|
| Dictionary spell checker | every word it does not recognise | a word list per project, maintained forever |
| **typos** | only words that are definitely wrong | **effectively none** |

The consequence is the point: **the false-positive rate is low enough that it can run on every
commit without curation.** A check that needs no allow-list is a check that never gets disabled.

It also understands code rather than treating a file as prose. Identifiers are split on case and
underscore boundaries before checking, so `recieveMessage` and `max_paramter_count` are both found,
and the correction is proposed for the word rather than the identifier.

And it corrects rather than merely reporting. Because every finding maps to a specific intended
word, it can rewrite the file — which turns the whole exercise into one command and one review
rather than a list of line numbers to work through by hand.

## When to use it

- **any repository with source code or documentation**, which is all of them
- as a pre-commit hook — it is fast enough that it is not noticed
- in CI, failing the build; see [`../README.md`](../README.md#1-what-a-linter-is-actually-for) on
  why a warning-only check is decoration
- on a large documentation set, where typos accumulate faster than anyone rereads
- when a spell checker was tried before and abandoned for noise

## When not to use it

- expecting it to find *all* misspellings; it finds the common ones, and unusual mistakes pass
- as a substitute for review — it checks spelling, not whether the sentence means anything
- for prose style, terminology or tone — that is
  [Vale](../../../../docs/authoring/vale/README.md)
- for grammar, which nothing in this folder does

## typos or codespell

They solve the same problem and the honest comparison is short. It lives here rather than in both
pages; see [`../codespell/`](../codespell/README.md) for the other tool's own page.

| | **typos** | **codespell** |
|---|---|---|
| Written in | Rust | Python |
| Speed | very fast — a large tree in well under a second | fast enough, and noticeably slower on a large tree |
| Dictionary | curated corrections, deliberately conservative | long-curated corrections list, larger and broader |
| False positives | **low by design** — unknown words are ignored | low, but broader coverage means more borderline calls |
| Identifier handling | **splits camelCase and snake_case before checking** | works on words; less code-aware |
| Installed base | growing, common in Rust and newer projects | **very large** — the Linux kernel and many long-standing projects |
| Fixing | proposes and applies the correction | proposes and applies the correction |
| Configuration | one file, plus per-word and regex exclusions | command-line flags and ignore files |

**The default recommendation here is typos**, for the same reason Ruff is the recommendation in
[`../README.md`](../README.md#2-the-python-set-and-how-it-collapsed): speed changes where a check
can run. A tool measured in milliseconds belongs in a pre-commit hook, and a hook that never
delays anybody is a hook that survives.

codespell remains the right answer in one situation, and it is not a small one: a project that
already uses it. Its dictionary is older and larger, its installed base is enormous, and switching
tools to gain a few hundred milliseconds is not a real improvement.

Neither is a substitute for the other in coverage terms, and running both is not unreasonable —
they are cheap, and the overlap is not complete. What neither replaces is somebody reading the
text.

## Notes

Written in Rust, from the crate-ci organisation, and distributed as a binary, a pre-commit hook
and a GitHub Action. Configuration is a single file, holding the words to ignore and the paths to
skip — needed mostly for generated files, vendored code, and the occasional identifier that is
spelled wrong on purpose because an upstream API spells it that way.

That last case is the one worth calling out. Exclusions here should be per-word and commented,
never a whole directory added because it was noisy once — the same rule
[`../shellcheck/`](../shellcheck/README.md) applies to per-line disables.

**Directly applicable to this repository, and cheaper than anything else catalogued here.** There
are 1204 `README.md` files under `infrastructure/`, written across many sessions, and prose
accumulates typos at a rate no amount of rereading catches. A repository whose entire product is
documentation has more to gain from a spell check than from most of the code linters on this page.

It is also the one check in this folder with **no adoption problem**. The advice in
[`../README.md`](../README.md#6-adopting-a-linter-on-code-that-already-exists) — ratchet, or gate
on new code only — exists because turning a linter on against an existing codebase produces
thousands of findings. typos does not: the first run finds a handful of real mistakes, they get
fixed in one commit, and the check is at zero from then on.

---

[← Lint](../README.md)
