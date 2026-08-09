[← SAST](../README.md)

# gosec

<https://github.com/securego/gosec>

---

## The problem it solves

gosec is bandit's counterpart for **Go**: it inspects the Go AST (and, for some rules, the SSA
representation) and reports constructs known to be dangerous. Every rule has a `G` number.

The checks reflect Go's specific failure modes rather than generic security advice:

| Rule family | Examples |
|---|---|
| `G1xx` — crypto and credentials | hardcoded credentials, weak random (`math/rand` where `crypto/rand` is needed), weak ciphers, small RSA keys |
| `G2xx` — injection | SQL built by string concatenation, command execution with variable input, template injection |
| `G3xx` — file and permissions | world-writable files, `os.MkdirAll` with permissive modes, path traversal from user input, unsafe archive extraction (zip slip) |
| `G4xx` — crypto primitives | MD5, SHA1, DES, RC4 |
| `G5xx` — imports | importing packages with known problems |
| `G6xx` — misc | integer overflow in conversions, `unsafe` usage, unhandled errors |

Two checks are worth naming because they catch real bugs that a Go reviewer also misses:

- **`G104` — unhandled errors.** In Go this is a security check as much as a quality one, because
  an ignored error from a permission check or a crypto operation means the failure silently
  proceeds.
- **`G601` / implicit memory aliasing in a loop.** Historically a real source of subtle bugs
  before the Go 1.22 loop variable change.

It integrates as a `golangci-lint` linter, which is how most Go projects actually run it — and if
`golangci-lint` is already configured, enabling gosec there is one line rather than a new tool.

## When to use it

- **A Go codebase.** It is fast, needs only the module to compile, and its checks are idiomatic
- **Through `golangci-lint`**, next to the linters the project already runs — same configuration,
  same output, same CI step
- **Alongside a general tool.** gosec encodes Go-specific knowledge; Semgrep gives you custom
  rules and multi-language coverage. Both is cheap
- **Kubernetes operators and controllers**, which are Go and typically handle credentials, TLS
  configuration and file permissions — exactly gosec's strongest areas

## When not to use it

- **A polyglot repository** — one SAST tool per language does not scale;
  [`../semgrep/README.md`](../semgrep/README.md)
- **Expecting cross-package dataflow.** gosec is largely per-file AST analysis. It flags a
  `exec.Command` with a variable argument without knowing whether the variable is attacker
  controlled
- **Expecting dependency coverage.** Vulnerable Go modules are `govulncheck`'s and
  [`../../sca/README.md`](../../sca/README.md)'s territory, not gosec's. `govulncheck` is
  particularly worth knowing here because it does reachability analysis on Go modules — it
  reports only vulnerabilities in code your binary actually calls, which is exactly the filter
  [`../../sca/README.md`](../../sca/README.md) argues most scanners lack
- **Without tuning.** `G104` on every deferred `Close()` and `G304` on every file path built from
  a variable will dominate the first run. Decide which of those you care about before deciding
  the tool is noisy

## Notes

Original note recorded for this tool:

- <https://github.com/securego/gosec> — the upstream project. The repository lists every `G`
  rule with an explanation, and documents the configuration surface: `-include` / `-exclude` by
  rule id, `-severity` and `-confidence` filtering, the `#nosec` inline annotation (which accepts
  a rule id and, in recent versions, requires a justification when configured to), SARIF and JSON
  output, and the GitHub Action.

Practical notes worth keeping alongside it:

- **`#nosec` should always name the rule and a reason** — `//nolint:gosec // G304: path is a
  fixed constant`. A bare `#nosec` suppresses everything on the line, forever, with no record of
  why.
- **Prefer running it inside `golangci-lint`** if that is already present: one binary, one
  configuration file, one cache, and the exclusion rules you already maintain for tests apply.

---

[← SAST](../README.md)
