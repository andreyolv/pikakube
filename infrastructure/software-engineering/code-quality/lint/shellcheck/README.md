[← Lint](../README.md)

# ShellCheck

<https://github.com/koalaman/shellcheck>

---

## The problem it solves

Shell is the language every platform ends up writing and nobody claims to know well. It has no
compiler, no type checker, and a set of defaults that turn mistakes into silence rather than
errors — so a broken script does the wrong thing successfully.

ShellCheck is a static analyser for `sh`, `bash`, `dash` and `ksh`, and it is unusually good at
its job: it catches the specific traps that make shell hard, and it explains each finding with a
wiki page rather than a code.

| Trap | What actually happens |
|---|---|
| **Unquoted variable** | `rm -rf $DIR` with a space in `DIR` deletes something else entirely |
| **Unquoted `$@`** | arguments containing spaces are split into several |
| `cd` without checking | the script continues in the wrong directory and does its work there |
| Parsing `ls` output | breaks on any filename with a space or a newline |
| `[ ]` vs `[[ ]]` | different operators, different quoting rules, different failures |
| **A failing command ignored** | without `set -e`, the script carries on as though it succeeded |
| `$?` checked after the wrong command | a redirect or an echo has already overwritten it |

The first row is the one that has destroyed real systems. It is also invisible in review, because
the code looks correct until the variable is empty or contains a space.

## When to use it

- **any repository containing shell scripts**, which is nearly all of them
- in CI, failing the build — see [`../README.md`](../README.md#1-what-a-linter-is-actually-for) on
  why a warning-only linter is decoration
- as a pre-commit hook, which is where it costs least
- when inheriting scripts nobody wants to touch — it is a fast way to find out how bad they are

## When not to use it

- there is no shell in the repository
- as a substitute for testing what the script actually does; it checks the code, not the outcome
- on very large legacy scripts, all rules at once, on day one — see below
- for formatting — that is [shfmt](../../format/shfmt/README.md)

## Adopting it on scripts that already exist

The same problem every linter has, and shell is worse because the findings are dense.

`shellcheck` on an old script produces a wall of output, and the reliable outcome is that somebody
disables it. What works:

| Step | Detail |
|---|---|
| **Start at `-S error`** | severity filtering: errors only, then warnings, then info |
| Fix quoting first | `SC2086` and its relatives are most of the volume and most of the risk |
| **Disable per line, with a reason** | `# shellcheck disable=SC2086` — and a comment saying why |
| Then lower the threshold | once errors are clean, move to warnings |

Per-line disables are legitimate here in a way they are not in most linters: shell has genuine
cases where word-splitting is intended. What is not legitimate is disabling a rule globally
because it fires a lot.

## The three lines that prevent most of it

Worth knowing, because ShellCheck will suggest them and they matter more than any individual fix:

```bash
set -euo pipefail
```

- **`-e`** — stop on a failing command instead of continuing
- **`-u`** — treat an unset variable as an error rather than an empty string
- **`-o pipefail`** — a pipeline fails if *any* stage fails, not just the last

`-u` is the one that pairs with ShellCheck's quoting findings: together they turn "the variable was
empty and the command did something unexpected" into an immediate failure.

## Notes

Added to the catalogue from <https://github.com/koalaman/shellcheck>. Written in Haskell, GPLv3,
and available as a binary, a container image, a GitHub Action and an editor extension — the last is
where it is most useful, because the feedback arrives while the script is being written.

**This is directly relevant to pikakube rather than theoretical.** The repository contains real
shell in the path people actually run:

| Script | What it does |
|---|---|
| [`init.sh`](../../../../../init.sh) | brings up the cluster — the entry point of the whole repository |
| [`finish.sh`](../../../../../finish.sh) | tears it down |
| [`tools-update.sh`](../../../../../tools-update.sh) | updates tooling |
| [`pandoc/convert.sh`](../../../../docs/authoring/pandoc/README.md) | document conversion |
| plus `build.sh`, `ssh-gen.sh`, `gen.sh` and others across the tree | |

`init.sh` is the one that matters most: it is the first thing anyone runs, and a quoting bug there
fails in front of a new user. It is also the script that most deserves `set -euo pipefail`, because
a partially-completed cluster bootstrap is worse than a failed one.

Pairs with [shfmt](../../format/shfmt/README.md), which formats what this one checks — see the
lint/format split in [`../README.md`](../README.md#1-what-a-linter-is-actually-for).

---

[← Lint](../README.md)
