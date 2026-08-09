[← Language](../README.md)

# Go

<https://github.com/golang/go>

<https://github.com/golang-standards/project-layout>

<https://github.com/go-gorm/gorm>

<https://github.com/google/pprof>

<https://github.com/apache/casbin>

---

## The problem it solves

Go produces **a single static binary** with no runtime to install and no dependencies to resolve at
deploy time. For anything that ships to a machine you do not control — a container image, a CLI
handed to another team, a controller in a cluster — that removes an entire category of problem.

The rest of the language follows from the same instinct: a compiler fast enough that the edit
cycle feels interpreted, concurrency built into the language rather than bolted on, a formatter
with no options so nobody argues about it, and a standard library that covers HTTP and TLS without
a dependency.

It is also, in practice, the language of this platform. Kubernetes, Flux, Helm, Prometheus, Argo,
Terraform and etcd are all Go. Extending any of them means writing Go, because the client
libraries and code generators exist there and nowhere else.

## When to use it

| Situation | Why Go |
|---|---|
| **Kubernetes controllers, operators, webhooks** | client-go, controller-runtime and the codegen tooling are Go-only in any serious sense |
| **CLIs distributed to other people** | one binary, no runtime on the target machine, trivial cross-compilation |
| Services where latency or memory is the constraint | compiled, no GIL, small footprint |
| Anything with heavy concurrency | goroutines and channels are the language, not a library |
| Sidecars and agents | a small static binary next to every workload keeps overhead honest |

## When not to use it

| Situation | Use instead |
|---|---|
| A one-off script or piece of glue | Python — a build step for twenty lines is not a trade |
| Data work, notebooks, ML | Python — the ecosystem is not close to being matched |
| Rapid prototyping of an internal API | Python — Go's explicitness costs time you have not yet decided is worth spending |
| Complex generic data structures | Go's generics are recent and limited; the code fights you |
| A team with no Go experience and no Kubernetes work | the maintenance burden is real and the payoff is not |

The honest version: Go is verbose about errors on purpose. `if err != nil` on every line is
tedious and it is also why Go services fail predictably. That trade only pays off in code that has
to keep running.

## Notes

The references collected here, and what each is for.

**[golang/go](https://github.com/golang/go)** — the language itself. Worth having for the standard
library source, which is unusually readable and is frequently the fastest answer to "what does
this actually do".

**[golang-standards/project-layout](https://github.com/golang-standards/project-layout)** — the
widely-copied directory convention: `cmd/` for entry points, `internal/` for code the compiler
will refuse to let other modules import, `pkg/` for code intended to be imported. Two caveats
worth knowing before adopting it wholesale:

- It is **not official**, despite the organisation name. It is a community convention that became
  a default by repetition.
- `internal/` is the only part the toolchain actually enforces, and it is the most valuable part.
  A small project does not need the rest of the tree.

**[go-gorm/gorm](https://github.com/go-gorm/gorm)** — the dominant Go ORM: associations,
migrations, hooks, and a query builder. The Go community is more sceptical of ORMs than most, and
the alternatives (`sqlc`, which generates typed code from SQL, or the standard `database/sql`) are
genuinely competitive. GORM wins when the model is relational and CRUD-heavy; it loses when the
queries are the interesting part and the generated SQL becomes something you have to fight.

**[google/pprof](https://github.com/google/pprof)** — the profiler. This is the thing to reach for
before optimising anything: CPU, heap allocation, goroutine and blocking profiles, with a web UI
that renders flame graphs. Go exposes it over HTTP from the standard library
(`net/http/pprof`), which means a running service in a cluster can be profiled by port-forwarding
to it — no rebuild, no restart, no agent. That single property makes it the most useful debugging
tool the language ships.

The rule it enforces: **measure, then optimise.** A profile takes minutes and is almost always
surprising.

**[apache/casbin](https://github.com/apache/casbin)** — an authorisation library. It separates the
*policy* (who may do what, stored in a file or a database) from the *model* (the shape of the
rules — RBAC, ABAC, ACL — declared in a config file), so the enforcement code stays the same while
the authorisation scheme changes underneath it.

Two things make it worth noting here. It is not Go-only — there are ports to most languages, so
the same policy format can be shared across services in different languages. And it is the
library-shaped alternative to running a policy engine as a service: if the decision is simple and
in-process is acceptable, Casbin avoids deploying and operating another component.

Nothing in this repository is written in Go yet. These are the references that would be needed
first if that changes — most plausibly the day something here has to reconcile cluster state,
which is the point at which a Python script has become a controller written badly.

---

[← Language](../README.md)
