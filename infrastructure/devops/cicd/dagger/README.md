[← CI/CD](../README.md)

# Dagger

<https://github.com/dagger/dagger>

---

## The problem it solves

Every other tool in this folder has the same shape: **the pipeline is YAML, interpreted by a server
you do not control.** Three consequences follow, and they are the daily experience of anyone who
maintains CI:

| Consequence | What it costs |
|---|---|
| You cannot run it locally | every change is a commit, a push, a queue and a wait |
| It is not a program | no types, no functions, no tests, no debugger, no imports |
| It is locked to one CI system | migrating means rewriting every pipeline |

Dagger inverts it. **The pipeline is a program** — Go, Python, TypeScript, PHP, Java — that calls an
API to describe a DAG of container operations. A local engine executes that DAG with
content-addressed caching, on BuildKit. The CI system's only job is to run one command.

That produces three properties nothing else in this folder has together:

- **The same pipeline runs on a laptop and in CI.** Not a similar one — the same one, with the same
  container images and the same cache semantics. This is the difference from
  [`act`](../github-actions/act/README.md), which approximates a runner
- **It is code.** Functions, parameters, imports, unit tests, a type checker, and reuse across
  repositories through modules rather than copy-paste
- **It is portable.** GitHub Actions, GitLab CI, Jenkins, or a terminal — all of them just invoke
  Dagger. The CI system becomes a trigger and a log viewer

Caching is the part that makes it practical rather than merely elegant: every operation is
content-addressed, so unchanged steps are skipped, on any machine, without configuring a cache key.

## When to use it

- **Pipeline debugging is the bottleneck.** If the team's commit history contains `fix ci`,
  `fix ci 2`, `fix ci for real`, this is the tool that removes the loop
- Logic has outgrown YAML — conditionals, matrices, shared functions across many `run:` blocks
- **The same pipeline must run across several CI systems**, or a migration is planned and you do
  not want to rewrite it again
- A monorepo where many services need the same build steps with small variations — a function with
  parameters, not N copies of a workflow
- The team already writes Go, Python or TypeScript, so the pipeline can be reviewed and tested like
  any other code
- You want developers to reproduce a CI failure locally, exactly, without pushing

## When not to use it

- The pipeline is five steps and works. `checkout`, `setup`, `test` in GitHub Actions YAML is not a
  problem that needs solving, and Dagger is a real dependency
- **The team will not maintain a program.** Dagger trades YAML for code; if nobody wants to own the
  code, YAML that everyone can read is better
- You depend heavily on **Marketplace actions**. Dagger has modules, but the GitHub Actions
  ecosystem is far larger, and rewriting `configure-aws-credentials` yourself is not progress
- Everything must run **inside Kubernetes as CRDs**. That is [Tekton](../tekton/README.md) or
  [Argo Workflows](../argo-workflows/README.md); Dagger's engine is a container runtime, not a
  Kubernetes controller
- The build cannot run in containers — a macOS or Windows native build, code signing on specific
  hardware
- You need the CI system's UI to be the source of truth for step-level status. Dagger runs as one
  command, so the CI view is coarser (its own cloud UI covers this, which is another dependency)

## Notes

<https://github.com/dagger/dagger> — the only recorded link, and the only one needed. Nothing is
deployed in this folder: Dagger is a **mapped alternative**, not part of this platform.

What is worth writing down is why it is filed here at all, given nothing runs it. Dagger is the
only entry in `cicd/` that is **different in kind** rather than different in implementation.
Jenkins, GitHub Actions, Tekton and Argo Workflows all answer *"which server interprets my
pipeline YAML?"* Dagger answers *"why is the pipeline YAML?"* — and that reframing is the reason to
keep it in view even when it is not installed.

Two clarifications that avoid the usual misunderstandings:

**Dagger is not a CI system.** It does not have triggers, webhooks, a scheduler, secret storage or
a permissions model. It still needs GitHub Actions or Jenkins around it to react to a push and hold
credentials. It replaces the *contents* of the pipeline, not the thing that starts it.

**It is not a container build tool either.** It builds images, but so does BuildKit, which it uses.
The product is the programmable DAG with caching, of which image building is one operation.

The evolution worth knowing about: Dagger began around **CUE**, a configuration language, and moved
to SDKs in general-purpose languages. Older material describing CUE-based pipelines is obsolete.
The current model is **modules** — reusable pipeline components, published and consumed like
libraries, callable from the CLI or from another module. That is the mechanism that makes it a
credible answer to cross-repository pipeline reuse, and the closest thing it has to the Actions
Marketplace.

For this platform, the concrete trigger to revisit it: the reusable Docker pipeline in
[`github-actions/workflows/`](../github-actions/workflows/README.md) is already a hundred lines of
YAML with lint, scan, test and push stages, and it can only be tested by pushing a tag. That is
exactly the shape Dagger exists for — the same stages as a typed function, runnable locally, with
the GitHub Actions workflow reduced to `dagger call build-and-push`.

---

[← CI/CD](../README.md)
