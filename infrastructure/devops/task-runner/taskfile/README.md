[← Task runners](../README.md)

# Task

<https://github.com/go-task/task>

---

## The problem it solves

Task defines commands in **YAML**, in a `Taskfile.yml`, and runs them with a single Go binary
that carries **its own shell interpreter**. That second detail is the one that distinguishes it:
recipes run identically on Linux, macOS and Windows without a POSIX shell being present, which
neither [Make](../makefile/README.md) nor [Just](../justfile/README.md) can claim.

It also keeps the useful half of Make's build-system behaviour, as an opt-in rather than a
default:

| Feature | What it does |
|---|---|
| `deps:` | tasks that run first, **in parallel** where the graph allows |
| `cmds:` | the commands, including `task:` references to other tasks |
| `sources:` / `generates:` | skip the task when its inputs are unchanged — Make's incremental rebuild, declared explicitly |
| `status:` | skip based on an arbitrary check succeeding |
| `task --watch` | rerun on file change |
| `includes:` | compose Taskfiles from subdirectories, which is how it handles monorepos |
| `vars:`, `env:`, `dotenv:` | variables, environment, `.env` loading — and variables whose value is the output of a command |
| `preconditions:` | fail early with a message when a required tool or file is missing |

`task --list` prints every task with its `desc:`, which is the same discoverability property Just
has.

## When to use it

- **When Windows is genuinely in scope.** The embedded shell is the reason to choose Task over
  Just, and it is a strong one.
- **When YAML is the preference** — consistent with the rest of a repository whose configuration
  is YAML already, and readable by anyone regardless of tooling background.
- **When file watching or input-based caching is wanted** without adopting Make's semantics
  wholesale.
- **Monorepos**, where `includes:` composes per-directory Taskfiles into one entry point.

## When not to use it

- **For a handful of short commands.** A one-line command becomes several lines of YAML, and the
  ceremony is visible immediately.
- **When nothing may be installed** — [Make](../makefile/README.md) is the only answer to that.
- **When the templating gets complicated.** Task uses Go templates inside YAML strings, which is
  a smaller dose of exactly the problem described in
  [manifest templating](../../templating/README.md#3-why-helms-string-templating-hurts):
  the tool is producing text, and quoting and escaping become the author's problem.

## Notes

The recorded link is [go-task/task](https://github.com/go-task/task).

Task sits between the other two rather than beside them. It is more capable than Just —
dependencies, caching, watching, includes — and more verbose than both. Whether that trade is
worth taking comes down to two questions, and neither is about the feature list:

- **Is anyone running these on Windows?** If yes, Task; the embedded shell settles it.
- **Is YAML a preference or an imposition?** A `Taskfile.yml` is longer than a `justfile` for the
  same commands, and the difference compounds.

Absent those, [Just](../justfile/README.md) does the common case with less typing and
[Make](../makefile/README.md) does it with nothing installed.

One caution worth recording: `includes:` makes it easy to build a deep tree of Taskfiles across a
monorepo, at which point resolving where a variable came from is a real exercise. The
discoverability that made a task runner worth having is the thing that erodes first.

---

[← Task runners](../README.md)
