[← Python dependency management](../README.md)

# Poetry

<https://github.com/python-poetry/poetry>

---

## The problem it solves

Poetry was the first tool to make a Python project **one file and one lock file**. Before it, a
project meant `setup.py` for packaging, `requirements.txt` for runtime dependencies,
`requirements-dev.txt` for the rest, and a virtual environment created by hand.

It does four jobs together:

| Job | How |
|---|---|
| **Declaration** | dependencies and metadata in `pyproject.toml`, one file |
| **Resolution** | a real solver — it finds a version set that satisfies everything, or fails and says why |
| **Locking** | `poetry.lock`, committed, giving the same versions everywhere |
| **Environments** | creates and manages the virtual environment for you |

It also handles packaging and publishing, which is why libraries adopted it early. For an
application rather than a library, `package-mode = false` turns that half off — the
[`pyproject.toml`](pyproject.toml) in this folder is exactly that shape: Poetry manages the
dependencies, but the repository is not treated as an installable package.

## When to use it

| Situation | Why |
|---|---|
| **The project already uses it and works** | migrating buys speed, not capability — see [`../README.md`](../README.md) |
| Publishing a library to PyPI | packaging and publishing are built in and mature |
| A team already fluent in it | the workflow is well understood and the tooling integrates everywhere |
| Anywhere the ecosystem assumes it | plugins, CI actions and editor integrations for Poetry are everywhere |

## When not to use it

| Situation | Use instead |
|---|---|
| **A new project** | [uv](../uv/README.md) — faster, and it replaces pyenv and pipx as well |
| **You need to constrain a transitive dependency** | uv — Poetry cannot do this at all, see the notes below |
| **The project is being containerised** | uv, whose Docker guidance is documented rather than scattered |
| Managing Python versions themselves | Poetry does not; uv or pyenv do |
| CI where install time is measurable | uv resolves and installs an order of magnitude faster |

## Notes

### Installing it

```
sudo apt install pipx
pipx install poetry
```

Install Poetry with **pipx, not pip**. pipx puts it in its own isolated environment with its own
dependencies. Installing it with `pip install poetry` into a project's environment means Poetry's
dependencies and the project's dependencies have to resolve together — and a tool whose job is
resolving conflicts should not be able to cause one.

```
poetry config --list
```

Shows the effective configuration. The setting worth checking first is
`virtualenvs.in-project` — with it on, the environment is created as `.venv/` next to the project
instead of in a cache directory elsewhere, which most editors detect automatically.

### Project and dependencies

| Command | What it does |
|---|---|
| `poetry init` | starts a project interactively — only if there is no `pyproject.toml` yet |
| `poetry add <lib>` | adds a dependency, resolves, updates the lock, installs |
| `poetry add <lib> --group dev` | the same, into the dev group — test and lint tooling that must not ship |
| `poetry remove <lib>` | removes it, and its transitive dependencies if nothing else needs them |

The `--group dev` split is the point of the whole exercise: it is what lets a production image
install runtime dependencies only.

After editing `pyproject.toml` **by hand**, the CLI has not been involved and the lock file is
stale:

| Command | What it does |
|---|---|
| `poetry lock` | re-resolves and rewrites `poetry.lock` — no installation |
| `poetry install` | installs exactly what the lock file says |

The two-step matters. `poetry lock` is a decision (which versions), `poetry install` is a
consequence (put them on disk). In CI only the second should run, so a pipeline can never quietly
change the version set.

### The virtual environment

```
poetry env activate
```

This **prints** the activation command rather than running it — a shell command cannot change its
parent's environment, which is the constraint every tool of this kind runs into. So you either
evaluate it:

```
eval "$(poetry env activate)"
```

Or install the alias recorded in the original notes:

```
echo "alias venv='source \"\$(poetry env info --path)/bin/activate\"'" >> ~/.bashrc
```

The escaping in that line is the load-bearing part. Written into `~/.bashrc`, `$(poetry env info
--path)` must survive as literal text so it is evaluated **when `venv` is run**, inside whichever
project directory you are in — not once, at the moment the alias is written. Get the quoting wrong
and the alias permanently points at the environment of whatever project you happened to be in that
day. The original note escapes both the `$` and the inner quotes for exactly this reason.

The alternative that avoids the problem entirely:

```
poetry run <command>
```

Runs a single command inside the environment without activating anything. This is the form to use
in scripts, `Makefile`s and CI, where an interactive shell does not exist.

`exit` leaves an activated environment — the activation started a subshell, so leaving the shell
is how you leave the environment.

### Inspecting and cleaning up

| Command | What it does |
|---|---|
| `poetry show` | lists installed packages with versions and descriptions; `--tree` shows what depends on what |
| `poetry env list` | every environment Poetry has created for this project |
| `poetry env remove --all` | deletes them all — the reset when an environment is in a state nobody can explain |

`poetry env list` returning more than one entry is usually a sign the project has been used under
several interpreter versions; each gets its own environment.

### Docker: the gap

Poetry has no official multi-stage Docker guide. The community's accumulated best practice lives
in two places, both recorded in the original notes:

- [python-poetry/discussions#1879](https://github.com/orgs/python-poetry/discussions/1879) — the
  long-running discussion thread where the patterns were worked out
- [python-poetry/poetry#9542](https://github.com/python-poetry/poetry/pull/9542) — a pull request
  to document them

A discussion thread and an unmerged PR are not documentation. The pattern they converge on:
install with `--no-root --only main` in a builder stage using the lock file **before** copying
application source, then copy the resulting virtual environment into a slim runtime stage. It
works, but you have to reconstruct it from a thread.

This is the concrete reason [uv](../uv/README.md) wins for anything containerised — it publishes
[a proper Docker guide](https://docs.astral.sh/uv/guides/integration/docker/#installing-a-project),
and in this repository nearly every Python project ends up as an image.

### Constraints: the limitation

**Poetry does not support constraints files.**
[python-poetry/poetry#7051](https://github.com/python-poetry/poetry/issues/7051)

A constraint pins a **transitive** dependency — something you do not depend on directly, but that
arrives through something you do — without adding it to your project as a direct dependency. The
scenario is common: a sub-dependency ships a broken or vulnerable release and has to be held back
until upstream catches up.

Without constraints, the options are all bad:

| Workaround | Why it is worse |
|---|---|
| Add it as a direct dependency | the project now claims to depend on something it does not use, and nobody remembers why |
| Pin the parent package instead | blocks unrelated fixes in the parent |
| Wait for upstream | not an option during an active vulnerability |

uv supports constraints. This is the one place where the difference between the two tools is a
capability rather than a preference, and it is felt precisely when something is already going
wrong.

---

[← Python dependency management](../README.md)
