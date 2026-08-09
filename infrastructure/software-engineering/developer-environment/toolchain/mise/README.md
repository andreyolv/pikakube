[← Toolchain](../README.md)

# mise

<https://github.com/jdx/mise>

---

## The problem it solves

A repository depends on a set of CLI tools at specific versions — a language runtime, Terraform,
kubectl, a linter — and nothing in the repository says which versions. mise makes that declaration
a committed file: a `mise.toml` listing tools and versions, resolved onto `PATH` when you enter the
directory.

It is the successor to **asdf** and occupies the same slot, rewritten in Rust. The practical
consequences of that rewrite are speed and a single static binary instead of a shell-based plugin
system. It is **backward compatible with `.tool-versions`**, which means an existing asdf project
can adopt it without rewriting its configuration first.

Three jobs, one tool:

| Job | What it replaces |
|---|---|
| **Tool versions** | asdf, nvm, pyenv, rbenv, tfenv, and the rest of the `*env` family |
| **Environment variables per directory** | `direnv` |
| **Tasks** | a `Makefile` used only as a command list — see [`devops/task-runner/`](../../../../devops/task-runner/README.md) |

The property that defines its scope: **mise manages versions of tools, it does not build packages.**
It fetches or builds a named tool at a named version and puts it on `PATH`. It says nothing about
the system libraries that tool links against. That limit is why it is small and fast, and it is
also exactly where the [Nix-based tools](../README.md#32-nix-based-environments) offer more.

## When to use it

- **The problem is version drift on CLIs** — everyone on a different Terraform, and that is the
  whole complaint
- A project already using asdf or `.tool-versions`, where asdf's speed has become an irritation
- Several projects on one machine needing different versions of the same runtime
- The team will not adopt Nix, and asking them to would kill the initiative outright
- You want one definition read by both the laptop and CI
- Inside a [devcontainer](../../devcontainer/README.md), to pin tool versions the base image does
  not fix — the two compose, they do not compete
- Replacing a `Makefile` whose only real content is a list of shell commands

## When not to use it

- **The guarantee needed is the full dependency closure**, not the tool version — that is
  [devenv](../devenv/README.md), [flox](../flox/README.md) or
  [Devbox](../../../../platform-engineering/kubernetes/local/linux/virtual-enviroment/devbox/README.md)
- The environment needs **running services** — a database, a broker — which mise does not do;
  [devenv](../devenv/README.md) does
- The tool is not available for it, or needs building from source with specific compiler flags —
  see [spack](../spack/README.md) for the extreme end of that
- A working Nix-based setup already covers it, and adding a second mechanism only splits the
  declaration in two
- The dependency is a **daemon** on the host, which no tool in this folder manages

## Notes

**Shims and activation.** mise can put tools on `PATH` through shims — small executables that
dispatch to the right version — or by activating in the shell so `PATH` itself changes per
directory. Shims work in contexts that never load a shell profile, such as some editors and CI
runners, which is usually where a "works in my terminal, not in my IDE" report comes from.

**The task runner overlap is a real decision, not a bonus.** mise's tasks cover the same ground as
[`devops/task-runner/`](../../../../devops/task-runner/README.md). Adopting both means commands
live in two places and one of them goes stale. Either mise owns tasks, or a `justfile`/`Taskfile`
does — not both.

**The `direnv` overlap is the same story.** Per-directory environment variables in `mise.toml`
remove the reason to run `direnv` alongside it. Running both is workable and confusing.

**The migration path from asdf is unusually cheap** because of `.tool-versions` compatibility: the
existing file keeps working while the team decides whether to move to `mise.toml`. That is rare
enough among replacement tools to be worth stating.

**What it does not promise.** Two machines with identical `mise.toml` files can still behave
differently, because the OS underneath is not part of the declaration. For most repositories that
is an acceptable trade; for a regulated or long-lived build it is not, and that is the line
between this family and the Nix-based one.

Specific flags, subcommand names and the exact `mise.toml` schema are not recorded here and are
unverified in this repository — read the upstream documentation rather than trusting a summary.

---

[← Toolchain](../README.md)
