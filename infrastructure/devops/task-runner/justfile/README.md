[← Task runners](../README.md)

# Just

<https://github.com/casey/just>

---

## The problem it solves

Just is what you get when you take Make's syntax, keep the parts people like, and delete the
build system underneath.

The premise is that most `Makefile`s in the wild are not building anything. They are a list of
named commands, and they are paying for a dependency-graph engine they never use — in `.PHONY`
declarations, tab characters and the absence of arguments.

Just removes each of those:

| Make problem | Just |
|---|---|
| Targets are files, so `.PHONY` everywhere | recipes always run. There is no file semantics and no `.PHONY` |
| Recipe lines must start with a tab | any consistent indentation |
| No arguments | `deploy env="dev":`, called as `just deploy prod`, with defaults and variadic parameters |
| One shell per recipe line | a shebang line makes the whole recipe one script, in any interpreter |
| Runs wherever you invoked it | runs from the justfile's directory by default, so recipes work from anywhere in the tree |
| Listing targets needs a `grep` trick | `just --list`, with doc comments as descriptions |
| `$$` for shell variables | `$` is the shell's; `{{ }}` is Just's |

It also loads `.env` files, supports `[private]` and `[confirm]` attributes on recipes, and
produces error messages that name the recipe and line rather than `missing separator`.

## When to use it

- **A repository whose commands are commands** — the common case, and what the tool was built
  for.
- **When recipes need parameters.** This is the single biggest practical gain over Make.
- **When a recipe is really a script.** The shebang form lets a recipe be Python or Bash with
  proper multi-line semantics, kept next to the other recipes instead of in a `scripts/` folder.
- **When discoverability matters.** `just --list` with doc comments is the cheapest self-updating
  index of what a repository can do.

## When not to use it

- **When nothing may be installed.** Just is one binary, but it is a binary — CI images and
  other people's machines may not have it, and [Make](../makefile/README.md) always does.
- **For actual builds.** There is no incremental rebuild and no dependency graph over files. That
  is deliberate; if you need it, that is Make's job.
- **On Windows without a shell.** Just needs one. [Task](../taskfile/README.md) embeds its own.

## Notes

The recorded link is [casey/just](https://github.com/casey/just).

Just is a **command runner, not a build system**, and that framing is the whole design rather
than a caveat. Everything it does better than Make follows from having dropped the file-target
model, and the one thing Make does that Just does not — skipping work whose inputs are unchanged —
follows from the same decision.

The practical adoption note: a `justfile` is close enough to a `Makefile` that anyone who can read
one can read the other, so the migration cost is a rename, a syntax pass and dropping every
`.PHONY` line. That is unusually cheap for a tool change, which is why "Just is what you use if
the tab rule and `.PHONY` noise bother you" is a complete and honest recommendation — there is no
larger commitment hiding behind it.

For this repository it is the best fit of the three, for the reason in
[`task-runner/`](../README.md#7-how-this-applies-to-pikakube): there is nothing to build here,
only commands worth naming.

---

[← Task runners](../README.md)
