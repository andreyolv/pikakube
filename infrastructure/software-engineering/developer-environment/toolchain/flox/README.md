[← Toolchain](../README.md)

# flox

<https://github.com/flox/flox>

---

## The problem it solves

flox is **Nix-based**, like [devenv](../devenv/README.md) and like this repository's
[Devbox](../../../../platform-engineering/kubernetes/local/linux/virtual-enviroment/devbox/README.md),
so the underlying guarantee is the same one: packages resolved from a catalog with their
dependency closure pinned, not just a version string.

Its bet is different from devenv's. devenv assumes you will accept Nix in exchange for its power.
**flox assumes you will not, and works to keep the language out of the way**: environments are
created, populated and shared through a CLI rather than by writing a Nix expression.

Two design choices follow from that, and both are the reason to look at it:

| Choice | Consequence |
|---|---|
| **Activate inside the existing shell** | your prompt, aliases, shell configuration and history survive — the environment is layered on, not substituted for |
| **Push and pull environments via FloxHub** | an environment becomes a thing you share with a teammate or pull onto a second machine, rather than a file each person builds locally |

It is cross-platform, including macOS, which matters for any team that is not uniformly on Linux.

## When to use it

- **Nix's guarantee is wanted and Nix's language is not** — this is the specific case flox exists
  for
- Environments should be **shared across a team and across machines**, and a git-committed file is
  not the sharing mechanism you want
- Developers have strongly customised shells and react badly to a tool that replaces them
- A mixed macOS/Linux team, where a Linux-only assumption would exclude people
- You want per-project environments layered onto a normal working shell rather than entered as a
  separate mode

## When not to use it

- **The environment needs to run services** — Postgres, Redis, a broker — which is
  [devenv](../devenv/README.md)'s distinguishing feature, not flox's
- The problem is only CLI version drift, where [mise](../mise/README.md) is far lighter
- The team is already fluent in Nix and wants the full expressive power rather than a layer over it
- A working Nix-based toolchain already exists — as it does in this repository — and a second one
  would only split the declaration
- Disk is tight and nobody will garbage-collect `/nix/store`
- The dependency is a **daemon on the host**, which is outside the boundary of every tool here

## Notes

**FloxHub is a dependency worth understanding before adopting.** Sharing environments through a
hosted service is the feature, and it also means asking who hosts it, what happens if it is
unreachable, and whether the environments involved are ones you are willing to push. Whether flox
is usable purely locally without FloxHub is not verified here — establish that before committing a
team to the workflow.

**Activation semantics are the ergonomic differentiator.** Tools that drop you into a new shell
break prompts, shell functions and history in small ways that people complain about for months.
Layering onto the current shell avoids that class of friction entirely, which sounds cosmetic and
is not — it is often what decides whether a team keeps using the tool.

**Compared to Devbox**, the two are close: both are Nix with the language removed. Devbox's
interface is a committed `devbox.json`; flox's is a CLI plus a shareable hosted environment. For a
repository that wants the environment definition living in version control alongside the code,
Devbox's model is the more conventional fit. For sharing an environment that is not tied to one
repository, flox's is.

**Compared to devenv**, the split is clean: choose devenv if you need services or want Nix's full
power, choose flox if the team's resistance to Nix is the binding constraint.

Specific commands, catalog behaviour and the exact environment file format are not recorded here
and are unverified in this repository — read the upstream documentation.

---

[← Toolchain](../README.md)
