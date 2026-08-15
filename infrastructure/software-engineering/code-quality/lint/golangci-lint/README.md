[← Lint](../README.md)

# golangci-lint

<https://github.com/golangci/golangci-lint>

<https://golangci-lint.run>

The Go equivalent of what [Ruff](../README.md#2-the-python-set-and-how-it-collapsed) became for
Python — except it got there by aggregation rather than by rewriting.

---

## The problem it solves

Go's linting story is unusual: the language ships `go vet`, and everything beyond it is a separate
binary. `staticcheck`, `errcheck`, `ineffassign`, `revive`, `gosec`, `unused`, `gocritic` — each is
its own project, its own installation, its own output format, and its own pass over the source.
Running eight of them means eight tool versions to pin, eight configuration styles, eight parses of
the same packages, and eight different ways of saying "line 42".

golangci-lint runs them **as one process**: over a hundred bundled linters, a single
`.golangci.yml`, one output format, results deduplicated, the type-checking work shared between
linters rather than repeated, and a cache so an unchanged package is not re-analysed. On a large
repository that is not a marginal improvement — it is the difference between a linter that runs on
every commit and one that runs in a nightly job nobody reads.

The distinction from Python's collapse is worth being precise about, because it changes how you
configure it: **Ruff replaced its predecessors; golangci-lint aggregates them.** Every finding
belongs to a named upstream linter, and the fix for a false positive is usually that linter's
documentation, not golangci-lint's. It is a runner with a shared configuration file, and knowing
that is what makes the config file readable.

## What is actually in it

The bundled set spans four categories that would otherwise be four decisions:

| Category | Examples | What it catches |
|---|---|---|
| **Correctness** | `govet`, `staticcheck`, `errcheck`, `nilness` | ignored errors, impossible type assertions, nil dereferences |
| **Dead weight** | `unused`, `ineffassign`, `unparam` | unused code, assignments never read, parameters nobody passes |
| **Style and idiom** | `revive`, `gocritic`, `stylecheck` | naming, receiver consistency, non-idiomatic constructs |
| **Security** | `gosec` | hardcoded credentials, weak crypto, unchecked file permissions, `exec` with tainted input |

`errcheck` is the one that earns the tool on its own. Go's error handling is a convention, not a
compiler rule — `f()` with a discarded error compiles perfectly — and the linter is the only thing
between that convention and a silently swallowed failure.

The security row deserves a boundary: **`gosec` inside golangci-lint is not a SAST programme.** It
is a useful set of pattern checks running where developers already look. Real static application
security testing lives in [`security/4-code/sast/`](../../../../security/4-code/sast/README.md),
where [gosec](../../../../security/4-code/sast/gosec/README.md) is catalogued as its own tool
alongside [Semgrep](../../../../security/4-code/sast/semgrep/README.md) and
[CodeQL](../../../../security/4-code/sast/codeql/README.md). Enabling it here is worth doing and is
not the same control.

## When to use it

- **any repository containing Go**, from the first package — this is the default and there is no
  serious competitor
- **in CI as a gate**, not a warning. The rule from [§1](../README.md#1-what-a-linter-is-actually-for)
  applies unchanged: a linter that only warns is decoration
- in a **pre-commit hook** as well, so CI is rarely the first place a finding appears
- when adopting linting on **existing** Go code — see `--new-from-rev` in the notes, which is the
  mechanism that makes this survivable
- when the alternative being considered is "install four linters in the Makefile", which is the
  same job done worse

## When not to use it

- as a **replacement for tests or review**. It finds mistakes that are mechanically detectable; it
  has no opinion about whether the code does the right thing
- as a **formatter** — `gofmt` and `goimports` own that, and formatting is
  [`../../format/`](../../format/README.md). golangci-lint can run them, but the disagreement to
  avoid is two tools rewriting the same file
- as your **SAST**, for the reason above
- **with `enable-all: true`.** This is the specific failure mode of an aggregator: over a hundred
  linters includes several with directly contradictory opinions, and the result is thousands of
  findings, a team that stops reading them, and a tool that gets removed within a month
- on a repository with **no Go**, which is worth saying because a meta-linter like
  [MegaLinter](../README.md#4-meta-linters) will happily run it anyway and report nothing useful

## Notes

**Pin the version, and expect the rules to move.** New releases add linters and tighten existing
ones, so an unpinned linter makes unrelated pull requests fail for reasons nobody changed — the same
argument recorded for [TFLint](../../../../platform-engineering/iac/lint/tflint/README.md). Pin it
in CI, pin it in the pre-commit config, and bump it deliberately.

**v2 changed the configuration file, not just the version.** golangci-lint v2 (2025) restructured
`.golangci.yml` — a top-level `version:` key, formatters split out from linters, and a reorganised
`linters:` block. There is a `migrate` command for the transition. The practical consequence: most
configuration examples on the internet are v1 and will not load. Check which major version the file
you are copying was written for.

**`--new-from-rev` is how you adopt this on existing code.** Pointed at a base revision, it reports
only findings in code that changed — so the backlog is frozen rather than dumped into the first pull
request, and every new commit is clean. This is exactly the strategy argued in
[§6 *Adopting a linter on code that already exists*](../README.md#6-adopting-a-linter-on-code-that-already-exists),
and golangci-lint has the flag for it built in. The trap is forgetting to ever go back: freeze the
backlog deliberately, and enable a batch of the old findings on purpose later, not never.

**The official action is `golangci/golangci-lint-action`.** It handles the install and the caching,
which matter more here than for most linters — a cold cache turns a fifteen-second run into a
multi-minute one. Pin it to a SHA like any third-party action
([GitHub Actions §8](../../../../devops/cicd/github-actions/README.md#8-anti-patterns)), and set the
linter version explicitly in the action's `version` input rather than letting it track latest.

**One process, one memory footprint.** Running a hundred linters over a large module is genuinely
memory-hungry, and the usual symptom on a constrained runner is an OOM kill with no useful message.
It is a documented, configurable problem — concurrency and the enabled set are both knobs — but it
is the first thing to suspect when the job dies without output on
[self-hosted runners](../../../../devops/cicd/github-actions/actions-runner-controller/README.md).

**Licence.** golangci-lint itself is GPL-3.0. That is a licence on the *tool you run*, not on the
code it analyses, so it carries no obligation for your source — worth stating because the question
gets asked, and because it differs from the permissive licences most of this folder carries.

**Where this fits in pikakube.** There is no Go in this repository to lint — the custom actions here
are [TypeScript](../../../../devops/cicd/github-actions/custom-ts/README.md) and
[Python](../../../../devops/cicd/github-actions/custom-py/README.md), and everything else is YAML
and Markdown. It is catalogued because **nearly every tool this platform deploys is written in Go**,
and the first moment it becomes concrete is the first controller, operator or CLI written here:
[`software-engineering/language/golang/`](../../../language/golang/README.md) is where that decision
lands, and this is the linter that goes in with it — configured on day one, when the backlog is
still empty and `enable-all` is still tempting.

---

[← Lint](../README.md)
