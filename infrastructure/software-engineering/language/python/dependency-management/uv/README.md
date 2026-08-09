[← Python dependency management](../README.md)

# uv

<https://github.com/astral-sh/uv>

---

## The problem it solves

uv is a Python package and project manager written in Rust by Astral. It does two things that
matter, and the second is the one that lasts.

**It is fast.** Resolution and installation are an order of magnitude quicker than pip or Poetry.
On a laptop that is pleasant; in CI, on every build, it is measurable.

**It collapses the tool count.** This is the real argument:

| Job | Before | With uv |
|---|---|---|
| Virtual environments | `virtualenv` / `venv` | `uv venv` |
| Installing | `pip` | `uv pip` |
| Locking | `pip-tools` / Poetry | `uv lock` |
| **Python versions** | `pyenv` | **`uv python`** |
| Running CLI tools | `pipx` | `uv tool` |
| Project management | Poetry | `uv add` / `uv remove` |

That right-hand column is one binary, with no Python installation required to bootstrap it. A
project that used Poetry for dependencies, pyenv for interpreters and pipx for tooling had three
tools to install, three to keep current, and three places for a new developer's setup to go wrong.

## When to use it

| Situation | Why |
|---|---|
| **Any new Python project** | the default; there is no longer a good reason to start elsewhere |
| **Anything being containerised** | multi-stage builds are documented properly — see the notes |
| **You need to constrain a transitive dependency** | supported here, and impossible in [Poetry](../poetry/README.md) |
| CI pipelines | install time drops enough to notice on every run |
| Replacing a stack of pyenv + pipx + pip-tools | one binary covers all three |
| Migrating off unpinned `requirements.txt` | it reads `requirements.txt` and produces a real lock file |

## When not to use it

| Situation | Use instead |
|---|---|
| **A working Poetry project** | leave it — the gain is speed, and the migration is risk for little return |
| A team with deep Poetry-specific tooling | the switching cost is in the surrounding automation, not the tool |
| Complex packaging requiring a specific build backend | check the backend is supported before committing |

The exception to the first row, recorded in [`../README.md`](../README.md): a project *being
containerised* is worth migrating on its own, because the documented multi-stage pattern is worth
more than the speed.

## Notes

### Commands

| Command | What it does |
|---|---|
| `uv init` | starts a project — only if there is no `pyproject.toml` yet |
| `uv add <package>` | adds a dependency, resolves, updates `uv.lock`, syncs the environment |
| `uv remove <package>` | removes it and anything transitively orphaned |
| `uv lock` | re-resolves and rewrites the lock file, without installing |
| `uv pip install -r pyproject.toml` | installs from `pyproject.toml` using the pip-compatible interface |
| `uv venv` | creates the virtual environment and prints the command to activate it |
| `uv run <command>` | runs a command in the project environment, syncing it first if needed |

Two things about that list are worth drawing out.

**`uv pip` is a deliberate compatibility surface.** It accepts pip's flags and arguments, which
means it can be dropped into an existing script or Dockerfile without rewriting the workflow.
That is the migration path: swap `pip` for `uv pip`, get the speed, and adopt `uv add` / `uv lock`
later.

**`uv run` is the command that removes activation entirely.** It ensures the environment matches
the lock file and then runs the command inside it. In scripts, `Makefile`s and CI — anywhere an
interactive shell does not exist — this is the form to use, and it makes the "did I activate the
right environment?" class of mistake impossible.

`uv venv` has the same constraint every tool of this kind has: a subprocess cannot modify its
parent shell, so it prints the activation command rather than performing it.

### Docker

The judgement recorded in the original notes, stated plainly: **uv's Docker documentation is good,
and Poetry's is not.** uv publishes
[a proper integration guide](https://docs.astral.sh/uv/guides/integration/docker/#installing-a-project);
Poetry's equivalent guidance lives in
[a discussion thread](https://github.com/orgs/python-poetry/discussions/1879) and
[an unmerged pull request](https://github.com/python-poetry/poetry/pull/9542).

For a platform that builds container images constantly, having the vendor document the multi-stage
pattern rather than leaving it to be reconstructed from a forum thread is not a small difference.

The [`Dockerfile`](Dockerfile) in this folder is that pattern, and each piece of it is doing
something:

| Element | Why |
|---|---|
| `COPY --from=ghcr.io/astral-sh/uv:${UV_VERSION} /uv /uvx /bin/` | takes uv from its official image at a **pinned version** — no install script, no network fetch of "latest" |
| `UV_COMPILE_BYTECODE=1` | compiles `.pyc` files at build time, so the first request does not pay for it |
| `UV_LINK_MODE=copy` | copies instead of hardlinking, which is what you want when the cache and the target are different mounts |
| `COPY pyproject.toml uv.lock ./` **before** the source | the dependency layer is invalidated only when dependencies change, not on every code edit |
| `--mount=type=cache,target=/root/.cache/uv` | BuildKit cache mount — the package cache survives between builds without ending up in a layer |
| `uv sync --locked --no-dev --no-install-project` | installs dependencies only: `--locked` fails if the lock is stale, `--no-dev` keeps test tooling out, `--no-install-project` defers the project itself |
| `uv sync --frozen --no-dev` after `COPY src/` | installs the project on top, once the source is present |
| Second stage copies only `/app/.venv` | uv itself, the cache and the build tooling never reach the runtime image |
| `ENV PATH=$APP_DIR/.venv/bin:$PATH` | the environment is "activated" by `PATH` alone — no activation script in a container |

The `--locked` flag deserves its own line: it makes a stale lock file a **build failure** rather
than a silent re-resolution. Without it, a build can quietly install a different version set than
the one that was tested.

### CI

The [`workflow.yaml`](workflow.yaml) in this folder is the GitHub Actions shape:
`astral-sh/setup-uv@v6` with the version pinned to the same `0.7.20` as the Dockerfile, then
`uv python install` to provision the interpreter — no `setup-python` step needed, because uv
manages interpreters too — and `uv lock --no-dev`.

Pinning the uv version in both the workflow and the Dockerfile is the detail that keeps CI and the
image resolving identically.

### Constraints

uv supports constraint files; Poetry does not
([python-poetry/poetry#7051](https://github.com/python-poetry/poetry/issues/7051)). Being able to
hold back a **transitive** dependency without declaring it as a direct one is the difference
between a two-line change and a false dependency nobody can later explain. It is the one place
where the gap between the two tools is a capability rather than a preference.

---

[← Python dependency management](../README.md)
