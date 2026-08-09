[← Task runners](../README.md)

# Make

<https://www.gnu.org/software/make/>

---

## The problem it solves

Make computes a **dependency graph over files** and runs only the work whose inputs changed. A
target depends on prerequisites; if the target is older than any of them, its recipe runs. That
is a genuinely good idea and still the correct answer for compiling artefacts from sources.

For task running specifically, its one overwhelming advantage is different: **it is already
installed.** Every Linux distribution, every CI image, every developer machine, every base
container. There is nothing to add to a README, nothing to install in a pipeline, and no argument
to have about adopting it. For a tool whose job is to be available the moment someone types a
command, that is worth more than any feature.

And everyone can read it. A `Makefile` with ten targets needs no explanation to anybody who has
worked on software.

## When to use it

- **Compiling things.** Sources to artefacts, with incremental rebuilds. This is what it is for
  and nothing else here does it as well.
- **When the runner has to work everywhere with nothing installed** — CI images you do not
  control, other people's machines, minimal containers.
- **Small repositories with a handful of commands**, where the friction below never gets large
  enough to matter.

## When not to use it

- **When most targets are not files.** `.PHONY` on every line is the tool telling you it is being
  used against its design.
- **When recipes need arguments.** Make has none. `make deploy ENV=prod` is a variable
  assignment, and positional arguments require pattern-rule tricks.
- **When recipes are multi-line shell.** One shell per line means `cd` does not persist, and
  every sequence needs `\` and `&&`.

## Notes

No links or commands were recorded with these notes — the folder existed as a placeholder in the
[task runner](../README.md) comparison. The canonical implementation is
[GNU Make](https://www.gnu.org/software/make/).

### The friction, precisely

| Behaviour | What happens |
|---|---|
| **Targets are files** | `make test` does nothing if a file or directory named `test` exists and is not older than its prerequisites. This is the surprise that costs people an afternoon |
| **`.PHONY`** | declares a target is not a file. Required on essentially every target in a task-runner Makefile, which is the clearest signal that Make is the wrong shape for the job |
| **Tabs, not spaces** | recipe lines must start with a literal tab character. A space gives `missing separator`, and any editor configured to expand tabs breaks the file silently |
| **One shell per line** | each recipe line is its own shell. `cd build` then `cmake ..` runs `cmake` in the original directory. Join with `\` and `&&`, or set `.ONESHELL` |
| **`$` belongs to Make** | to pass `$HOME` to the shell you write `$$HOME`. Forgetting produces an empty string, not an error |
| **No arguments** | only variables, which are global and untyped |

None of this is broken. It is a build system behaving like a build system, and every item above
follows from that.

### Making it tolerable

If Make is the choice, these three cover most of the pain:

```make
.DEFAULT_GOAL := help
.PHONY: help test
```

`.DEFAULT_GOAL := help` makes a bare `make` print what is available instead of running the first
target. `.PHONY` on every non-file target avoids the silent no-op. A `help` target that greps the
Makefile for `##` comments is the conventional way to get a listing — which the other two tools
have built in.

### The honest position

**Make is already there and it works.** For a small set of recipes that is a complete argument,
and swapping it for something else buys a nicer syntax at the cost of an installation step.

[Just](../justfile/README.md) is what you move to when the tab rule and the `.PHONY` noise stop
being cosmetic. [Task](../taskfile/README.md) is for YAML and Windows. Neither replaces Make for
actual builds.

---

[← Task runners](../README.md)
