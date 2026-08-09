[← SAST](../README.md)

# Semgrep

<https://github.com/semgrep/semgrep>
<https://github.com/semgrep/semgrep-rules>

---

## The problem it solves

Static analysis engines have historically been either too crude (grep, which cannot tell a
comment from code) or too specialised (a query language and a code database, which nobody on the
team will learn). Semgrep sits deliberately in between.

Its central idea: **a rule looks like the code it matches.**

```yaml
rules:
  - id: dangerous-subprocess-shell
    pattern: subprocess.$FUNC(..., shell=True, ...)
    message: shell=True with untrusted input allows command injection
    languages: [python]
    severity: WARNING
```

That pattern is Python with metavariables. It matches regardless of formatting, whitespace,
argument order or the variable names used, because Semgrep parses to an AST rather than matching
text. The consequence is the one that matters organisationally: **a developer can read, review
and write these rules**, which is what makes a curated rule set achievable instead of aspirational.

What it brings:

| Capability | Detail |
|---|---|
| Multi-language | 30+ languages from one engine and one configuration |
| Community rules | `semgrep-rules` is a large, curated, open-source registry — OWASP categories, framework-specific rules, secret detection |
| Taint mode | source-to-sink dataflow, though not CodeQL's cross-file depth |
| Fast | seconds to a couple of minutes; no build required |
| Diff-aware | `--baseline-commit` scans only what changed, which is how you avoid drowning in a legacy backlog |
| Autofix | some rules carry a fix, applied with `--autofix` |
| SARIF output | integrates with GitHub code scanning and with aggregators |

Beyond security, the same engine is used for enforcing internal conventions — "never call this
deprecated helper", "every handler must go through this middleware". That secondary use is often
what gets it adopted.

## When to use it

- **As the default SAST tool for a polyglot repository.** One engine, one config, one output —
  the single strongest argument for it
- **When you need custom rules.** This is where it beats everything else in this folder. An
  organisation-specific rule takes minutes to write and can be reviewed by anyone
- **Diff-aware scanning on pull requests.** `--baseline-commit` turns an unbounded backlog into a
  per-PR problem
- **Enforcing conventions, not only security.** The rules mechanism is general
- **You want to stay open source.** The CLI and the community rules are; see the note about the
  hosted product below

## When not to use it

- **Deep cross-file dataflow is the requirement.** If the question is "can input from this HTTP
  handler reach this sink through four files and an interface", CodeQL does that properly and
  Semgrep does not — [`../codeql/README.md`](../codeql/README.md)
- **Single-language repositories where a specialist tool is enough.** bandit for Python, gosec
  for Go: less to configure and idiomatic knowledge already encoded
- **Expecting default rules to be low-noise.** They are better than most, but "enable everything"
  still produces a backlog. Curation is not optional
- **Confusing the CLI with the platform.** Semgrep AppSec Platform (formerly Semgrep Cloud) is a
  commercial hosted product; some rules and features live there rather than in the open-source
  registry. Know which side of that line you are relying on

## Notes

Original notes recorded for this tool:

- <https://github.com/semgrep/semgrep> — the engine and CLI. Documents the pattern syntax
  (metavariables, `...` ellipsis, `pattern-either`, `pattern-not`), taint mode, autofix, and the
  `--baseline-commit` flag for diff-aware scanning.
- <https://github.com/semgrep/semgrep-rules> — the open-source rule registry. This is the more
  useful repository day to day: it is the corpus to copy from when writing a rule, and reading a
  few rules in the language you use is the fastest way to learn the pattern syntax. Rules are
  organised by language and framework, so it is also how you decide *which* rule packs to enable
  rather than taking `p/default` wholesale.
- <https://semgrep.dev/docs/semgrep-ci/sample-ci-configs#sample-github-actions-configuration-file>
  — the official sample CI configurations, with the GitHub Actions example anchored directly.
  This is the reference for wiring it into a workflow: which container image to use, how to pass
  the rule configuration, and how to emit SARIF for GitHub code scanning.

One practical point from those sample configs worth carrying: they show scanning on pull requests
with a baseline, which is the configuration that makes adoption survivable — see
[`../README.md`](../README.md) section 3.

---

[← SAST](../README.md)
