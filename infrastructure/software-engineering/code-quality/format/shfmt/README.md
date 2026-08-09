[← Format](../README.md)

# shfmt — mvdan/sh

<https://github.com/mvdan/sh>

---

## The problem it solves

A formatter for shell — the one language where formatting arguments are most tedious and where
almost nobody had a tool.

`gofmt` settled the question for Go by removing the option to disagree.
[Prettier](../prettier/README.md) did it for the JavaScript world. Shell had neither, so every
script in a repository reflects whoever last touched it: two spaces or four, `then` on the same
line or the next, `$(...)` or backticks.

shfmt applies one consistent style, and it does it by **parsing** rather than by pattern-matching
text — which is what makes it safe.

## More than a formatter

`mvdan/sh` is a shell **parser** in Go, and shfmt is one thing built on it. The distinction
matters:

| Component | What it is |
|---|---|
| **The parser** | a real syntax tree for `bash`, `sh` (POSIX) and `mksh` |
| **`shfmt`** | the formatter — the part most people use |
| `gosh` | an interpreter, useful for embedding shell evaluation in Go |
| The library | usable directly, for tools that need to understand shell |

Because it parses, shfmt **refuses to format a script it cannot parse** rather than mangling it.
That is the property that makes it safe to run across a repository: a syntax error is reported, not
silently reformatted into something different.

It also means shfmt is a syntax check on its own. A script that shfmt parses is at least
structurally valid — which is a weaker guarantee than
[ShellCheck's](../../lint/shellcheck/README.md) and a free one.

## When to use it

- **any repository with more than one shell script**, especially with more than one author
- in CI with `-d` (diff) or `-l` (list), failing the build on unformatted files
- as a pre-commit hook, or on save in the editor
- alongside [ShellCheck](../../lint/shellcheck/README.md) — they do different jobs, see
  [`../README.md`](../README.md#2-formatting-is-not-linting)

## When not to use it

- there is no shell in the repository
- expecting it to find bugs — it formats; ShellCheck analyses
- on a language it does not parse. It covers `bash`, POSIX `sh` and `mksh`; **zsh and fish are
  not supported**, and that is the most common reason it does not fit

## The flags that matter

Unlike `gofmt`, shfmt has options — which slightly undermines the "no arguments" principle, and is
a concession to how much shell already exists in the world:

| Flag | Effect |
|---|---|
| `-i N` | indent with N spaces; **`-i 0` means tabs**, and is the default |
| `-bn` | binary operators (`&&`, `\|\|`) at the start of the next line |
| `-ci` | indent switch cases |
| `-sr` | a space after a redirect operator |
| **`-s`** | simplify — remove redundant quotes and brackets. This one **changes code**, not just layout |
| `-d` | print a diff and exit non-zero — the CI mode |
| `-w` | write in place |

Two things to decide once and record: **the indent setting**, because the default is tabs and most
people expect spaces, and whether **`-s`** is on. Simplification is genuinely useful and it edits
expressions rather than whitespace, so it belongs in a deliberate pass rather than in a save hook.

`.editorconfig` is honoured, which is the tidiest way to keep the setting with the repository rather
than in everyone's editor.

## Notes

Added to the catalogue from <https://github.com/mvdan/sh>. From Daniel Martí, who also maintains
parts of the Go toolchain — the parser quality reflects that.

The recorded position in [`../../lint/README.md`](../../lint/README.md) that **EditorConfig is
largely covered by linters** applies here with a caveat: shfmt *reads* `.editorconfig`, which makes
it one of the places where that file still earns its keep.

**Relevant to pikakube rather than theoretical.** The repository contains real shell —
[`init.sh`](../../../../../init.sh), [`finish.sh`](../../../../../finish.sh),
[`tools-update.sh`](../../../../../tools-update.sh),
[`convert.sh`](../../../../docs/authoring/pandoc/README.md), plus `build.sh`, `ssh-gen.sh` and `gen.sh`
across the tree — written at different times, and it shows.

The pairing worth setting up together, because each covers what the other does not:

| Tool | Job |
|---|---|
| **shfmt** | it looks the same everywhere, and it parses |
| [**ShellCheck**](../../lint/shellcheck/README.md) | the unquoted variable will not delete the wrong directory |

Neither of them tells you the script does the right thing. That is still a test.

---

[← Format](../README.md)
