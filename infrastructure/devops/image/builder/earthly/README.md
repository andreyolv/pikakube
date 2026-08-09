[← Builders](../README.md)

# Earthly

<https://github.com/earthly/earthly>

---

## The problem it solves

**One build definition that runs identically locally and in CI.** Earthly's premise is that CI
configuration and build scripts are the same thing written twice — a `Makefile` for the laptop and
a pipeline YAML for the server, which drift until "works locally" stops meaning anything.

An `Earthfile` looks like a Dockerfile with targets:

```
build:
    FROM golang:1.22
    COPY . .
    RUN go build -o app
    SAVE ARTIFACT app

test:
    FROM +build
    RUN go test ./...
```

Everything runs in containers, so the build is reproducible and hermetic wherever it is invoked.
Targets can depend on one another, run in parallel, and export artefacts or images. BuildKit does
the execution underneath, so the caching is BuildKit's.

| Property | Detail |
|---|---|
| Same command locally and in CI | `earthly +test` — no separate pipeline definition |
| Containerised steps | dependencies are declared, not assumed to exist on the runner |
| Parallel target execution | independent targets run at once |
| Monorepo-friendly | targets across directories with explicit dependencies |
| CI-agnostic | the CI system's only job is to invoke `earthly` |

## When to use it

- **a monorepo with several languages**, where a shared build definition is worth real effort
- when "works on my machine" is a recurring, expensive problem
- when CI configuration has grown into a build system nobody can run locally
- with the caveat below firmly in mind

## When not to use it

- **as a new dependency for a long-lived platform** — see the note on the project's status
- for a single-service repository where a Dockerfile plus a few CI steps is already clear
- where the team has no appetite for another build language to learn and maintain
- where the CI system's native features — caching, matrices, artefacts — already work well

## Notes

Recorded link:

- <https://github.com/earthly/earthly> — the tool.

**Project status, stated plainly because it changes the recommendation.** Earthly the company
wound down its commercial products — Earthly Cloud and Earthly Satellites — and the open-source
project's development slowed markedly as a result. The repository is still there and the tool
still works, but it is no longer a project with a company driving it forward.

That does not make the ideas wrong; the "one build definition, containerised, runs anywhere"
argument is a good one and it is why the tool is documented here. It does mean **checking the
repository's current activity before adopting it**, and weighing that against alternatives that
have not lost their sponsor: [Dagger](https://github.com/dagger/dagger) occupies much the same
space with pipelines written in a general-purpose language, and a plain
[BuildKit](../buildkit/README.md) or Dockerfile-based build with well-organised CI covers most of
the benefit with no extra tool.

The `dagger/` folder under `infrastructure/devops/cicd/` in this repository is the closest
mapped alternative.

## Where it fits here

Documented as an evaluated alternative rather than a candidate. The pattern worth taking from it —
**the build definition is code, containerised, and runs the same way everywhere** — is the durable
part; the specific tool is the part with a question mark over it.

---

[← Builders](../README.md)
