[← Toolchain](../README.md)

# devenv

<https://github.com/cachix/devenv>

---

## The problem it solves

devenv builds developer environments on **Nix**, which means the environment is pinned all the way
down — not just "Terraform 1.7" but the exact build of it, with its dependency closure, fetched
into `/nix/store`. That guarantee is stronger than anything a version manager like
[mise](../mise/README.md) can offer.

Its distinguishing feature against plain Nix, and against the other tools in this folder, is
narrower and more useful than the reproducibility argument: **devenv runs services.** Postgres,
Redis, a message broker and similar processes are declared as part of the environment definition
and started by `devenv up`. The environment stops being "tools on `PATH`" and becomes "the
application's local dependencies, running".

That is the point where it replaces something concrete:

| Before | With devenv |
|---|---|
| A `docker-compose.yaml` kept only to run Postgres locally | a service block in the environment definition |
| A README section on installing and starting the database | `devenv up` |
| Pre-commit hooks configured separately per machine | declared alongside the environment |
| Nix flakes written by hand | a higher-level layer over the same substrate |

It is built by **Cachix**, whose binary cache service it integrates with — which matters in
practice, because the difference between fetching a prebuilt closure and compiling one from source
is the difference between a fast first run and a very slow one.

## When to use it

- **The local environment needs running services**, and Docker Compose exists only to provide them
- The team is willing to work with Nix, or already does
- Reproducibility is a requirement rather than a preference — regulated work, long-lived builds, or
  a team that has been burned by an unpinned toolchain
- Pre-commit hooks should be part of the environment definition instead of a per-machine setup step
- You want the same definition to run on a laptop and in CI, with the closure identical in both
- A binary cache is available or can be set up, so first runs are fetches and not builds

## When not to use it

- **The problem is only CLI version drift** — [mise](../mise/README.md) solves that with none of
  the learning curve
- The team will not learn Nix, and honesty about that is more useful than optimism —
  [flox](../flox/README.md) makes the opposite bet for exactly this case
- A working Nix-based setup already exists, such as this repository's
  [Devbox](../../../../platform-engineering/kubernetes/local/linux/virtual-enviroment/devbox/README.md);
  a second one is a second declaration
- Disk is tight and nobody will garbage-collect `/nix/store`, which only ever grows
- The dependency is a **daemon on the host** — Docker and containerd are outside the boundary of
  every tool in this folder
- The services needed are complex enough that the real answer is a container stack, or a
  [devcontainer](../../devcontainer/README.md) built from Compose

## Notes

**The learning curve is the actual cost, and it is not small.** Nix is a functional language with
unusual evaluation semantics, and people who are competent everywhere else find it genuinely hard.
devenv reduces how much of it you write; it does not remove it. Any adoption plan that treats this
as a documentation problem is underestimating it.

**Services are the reason to pick this one.** Reproducibility is shared with flox and Devbox.
Running Postgres as part of the environment is not — it is the specific capability that makes
devenv the answer for an application team rather than a platform team.

**Cache or compile.** Nix either fetches a prebuilt closure or builds it. Without a working binary
cache, "reproducible" is bought with build time, and that cost lands hardest on the first person
to try it — which is also the person deciding whether the team adopts it.

**vs. Docker Compose for services.** Compose gives isolated services in containers; devenv gives
them as processes on the host, started from the same definition as the toolchain. Compose is more
faithful to production, devenv is lighter and needs no container runtime. Neither is strictly
better, and the choice usually follows whether a container runtime is available and licensed.

Exact configuration file names, option schemas and subcommand behaviour beyond `devenv up` are not
recorded here and are unverified in this repository — read the upstream documentation.

---

[← Toolchain](../README.md)
