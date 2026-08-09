[← Format](../README.md)

# Prettier

<https://github.com/prettier/prettier>

---

## The problem it solves

Prettier removes formatting from the set of things a team can disagree about. It parses the file
into an AST, throws the original formatting away, and prints it back out from scratch. The input's
whitespace is not adjusted — it is discarded.

That is the design decision that makes it work. A tool that *adjusts* formatting leaves room for
two files to be differently-but-acceptably formatted; a tool that reprints from the AST produces
exactly one output per program, so "correctly formatted" becomes a property that can be checked
with an exit code.

Its second advantage is breadth. One binary and one configuration file cover JavaScript,
TypeScript, JSX, CSS, SCSS, Less, HTML, JSON, YAML, GraphQL and Markdown. In a repository that
contains all of those — which most repositories that contain any of them do — the alternative is
five formatters with five configurations that disagree at the boundaries.

## When to use it

- Any repository with **JavaScript or TypeScript** in it. This is the settled default; there is no
  serious competitor for the same job.
- Repositories where the non-code files matter: **YAML manifests, JSON, Markdown documentation**.
  A GitOps repository is mostly YAML, and Prettier formats it consistently.
- Alongside ESLint, with `eslint-config-prettier` disabling every ESLint rule that touches
  layout. This is the standard pairing and the reason it is standard: without it the two tools
  produce an infinite fix loop.
- As a **pre-commit hook in write mode and a CI job in `--check` mode**. Both, not either.

## When not to use it

- For **Python**. Use Black or `ruff format` — see [`../../lint/`](../../lint/README.md). Prettier
  has no Python parser and there is no reason to want one.
- For **Go, Rust or Terraform**, where the toolchain already ships a formatter that everyone
  already uses. Adding Prettier there creates a second opinion where there was none.
- As a **linter**. Prettier has no opinion about unused variables, shadowed names or bad idioms,
  and configuring it as though it did produces frustration in both directions.
- If the plan is to configure it heavily. Prettier deliberately exposes few options; a team that
  wants many is a team that has not yet accepted the premise, and will spend more time on the
  configuration than the tool saves.
- On a large legacy codebase **without** a plan for the blame-destroying first commit. Reformat in
  one isolated commit and record its hash in `.git-blame-ignore-revs`.

## Notes

The only thing recorded in the original note for this folder is the repository itself:

- <https://github.com/prettier/prettier>

That reflects the status accurately — Prettier is catalogued here as the chosen formatter for the
non-Python parts of the stack, not deployed or configured. There is no Kubernetes surface to it:
it runs in the editor, in a pre-commit hook and in CI, and nothing about it belongs in the
cluster.

Two operational points worth carrying forward when it is actually adopted:

| Point | Detail |
|---|---|
| Pin the version | Prettier's output changes between major versions; an unpinned version reformats the world on a Monday |
| `.prettierignore` | vendored code, generated files and lockfiles should be excluded, or every regeneration produces a diff |

---

[← Format](../README.md)
