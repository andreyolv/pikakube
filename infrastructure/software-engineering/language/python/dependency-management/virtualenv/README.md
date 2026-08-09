[← Python dependency management](../README.md)

# virtualenv

<https://github.com/pypa/virtualenv>

<https://github.com/pypa/pip>

<https://github.com/jazzband/pip-tools>

---

## The problem it solves

**Isolation.** One interpreter on a machine, many projects, and two of them needing different
versions of the same library. A virtual environment is a directory containing its own
`site-packages` and its own `bin/`, so `pip install` writes there instead of into the interpreter
the operating system depends on.

That is the whole idea, and it is the foundation everything else in this folder is built on. uv
and Poetry both create virtual environments; they just do more on top.

Since Python 3.3 the standard library has shipped `venv`, which covers the common case.
`pypa/virtualenv` — the original project — is still faster, works on older interpreters, and
supports more configuration, but for a modern project `python3 -m venv` is what you use.

## When to use it

| Situation | Why |
|---|---|
| **A script or a throwaway environment** | no project to initialise, no lock file to maintain |
| Reproducing a bug in a clean environment | thirty seconds, no tooling to install |
| A machine where you cannot install anything | `venv` is in the standard library; it is always there |
| **Understanding what the other tools do** | uv and Poetry create exactly this; knowing it makes their behaviour legible rather than magical |
| An existing project already on `requirements.txt` | leave it working, and reach for a real lock file when it next hurts |

## When not to use it

| Situation | Use instead |
|---|---|
| **Any project with more than a handful of dependencies** | uv — resolution and a real lock file |
| Anything that has to be reproducible | uv or Poetry; `pip freeze` is not locking |
| Separating dev and runtime dependencies | dependency groups, which `requirements.txt` does not have |
| A container image built repeatedly | a lock file, or the layer cache is guesswork |

The specific limitation: `pip` installs, it does not resolve. It walks the requirements in order
and takes the first version that fits, which means the result depends on ordering and can differ
between machines. That is the gap [pip-tools](https://github.com/jazzband/pip-tools) and then uv
were built to close.

## Notes

The commands recorded from use.

**Creating and using an environment**

| Command | What it does |
|---|---|
| `python3 -m venv <name>` | creates the environment in a directory called `<name>` |
| `source <name>/bin/activate` | puts its `bin/` at the front of `PATH` — `python` and `pip` now mean the environment's |
| `pip install <package>` | installs into the active environment |
| `deactivate` | restores the previous `PATH` |

Activation is only a `PATH` change. Nothing is installed globally and nothing persists after
`deactivate`; deleting the directory removes the environment completely. The convention is to name
it `.venv` and add it to `.gitignore` — never commit it, because it contains platform-specific
binaries.

**Capturing what is installed**

```
pip freeze > requirements.txt
```

This writes every package in the environment with its exact version. It is the closest thing plain
pip has to a lock file, and the difference matters:

| | What it records |
|---|---|
| `pip freeze` output | the **state** of an environment — every package, direct and transitive, flattened together |
| A real lock file | the **intent** (what you asked for) *and* the resolved result, with the two kept distinct |

With a frozen `requirements.txt` there is no way to tell which entries you actually depend on and
which arrived as somebody else's dependency, so removing a package leaves its transitive
dependencies behind forever. It also captures anything installed by accident during debugging.

**The references**

**[pypa/pip](https://github.com/pypa/pip)** — the installer itself, and the thing every other tool
in this folder either wraps or replaces. Worth reading its resolver documentation once: modern pip
does backtrack, but it is slow enough that large dependency trees are where uv's speed advantage
becomes obvious.

**[jazzband/pip-tools](https://github.com/jazzband/pip-tools)** — the missing layer, and the
intermediate step between plain pip and uv. You write direct dependencies in `requirements.in`,
run `pip-compile`, and get a fully-pinned `requirements.txt` with comments recording *why* each
transitive package is present. `pip-sync` then makes the environment match exactly, removing
anything that should not be there.

This is the two-file split that Poetry and uv adopted (`pyproject.toml` plus a lock file), and it
is why pip-tools is worth understanding even if you never adopt it: it is the same idea without
the project management. `uv pip compile` is a drop-in, much faster replacement for it.

---

[← Python dependency management](../README.md)
