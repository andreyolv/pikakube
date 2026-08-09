[← Secret scanning](../README.md)

# Gitleaks

<https://github.com/gitleaks/gitleaks>

---

## The problem it solves

Gitleaks is the default secret scanner: a single Go binary that scans Git history, working
directories, or a diff, using a rule set of regular expressions with optional entropy checks.

The modes matter, because they map onto the three placements in
[`../README.md`](../README.md) section 2:

```bash
# the whole history — run this once, at adoption
gitleaks detect --source . --report-format sarif --report-path leaks.sarif

# only what is staged — the pre-commit case
gitleaks protect --staged

# a directory, ignoring Git entirely — useful for artefacts and untracked files
gitleaks dir .
```

Why it is the default rather than merely one option:

| Property | Detail |
|---|---|
| **Fast full-history scanning** | it walks Git objects efficiently; scanning years of history is minutes, not hours |
| A good default rule set | 150+ patterns for the credential formats that matter, maintained upstream |
| Extensible rules | `.gitleaks.toml` adds your own patterns — internal token formats, which no default rule set knows |
| Allowlisting that survives review | by path, by regex, by commit, or inline with `gitleaks:allow`, plus `.gitleaksignore` keyed on a finding fingerprint |
| SARIF output | lands in GitHub code scanning and in aggregators |
| Pre-commit and Action integrations | official, first-class |

The allowlisting design is worth calling out because it is what stops a scanner being abandoned.
`.gitleaksignore` records a **fingerprint** of a specific finding, so suppressing one false
positive does not blind you to a real secret in the same file later.

## When to use it

- **As the continuous scanner**, in pre-commit and in CI. This is its primary role and it is very
  good at it
- **For the initial full-history scan**, if you want one tool rather than two — though for that
  specific job TruffleHog's verification makes triage far easier
  ([`../trufflehog/README.md`](../trufflehog/README.md))
- **When custom credential formats exist.** Internal service tokens follow a format only you know,
  and a `.gitleaks.toml` rule is a few lines
- **Where the scan must be offline.** Gitleaks makes no network calls, so it runs in air-gapped CI
  and never sends a candidate secret anywhere. That is a real advantage over verification-based
  scanning in sensitive environments
- **In pre-commit specifically** — `gitleaks protect --staged` is the only placement that can stop
  a secret from entering history at all

## When not to use it

- **When you need to know which findings are live.** Gitleaks reports pattern matches; it does
  not check whether a credential still works. On a first scan of an old repository that is the
  difference between 200 candidates and 3 incidents
- **As your only control.** Pattern matching misses formats nobody wrote a rule for, and entropy
  detection is noisy enough that most people turn it down
- **Instead of prevention.** A scanner that finds a secret in CI has already lost — the value is
  in the remote. See [`../README.md`](../README.md) section 5
- **Without tuning on a large legacy repository.** The first full-history run on an old repository
  produces a backlog. Triage it once, fingerprint the false positives, then it stays quiet

## Notes

Original note recorded for this tool:

- <https://github.com/gitleaks/gitleaks> — the upstream project. The repository documents the
  `detect` / `protect` / `dir` commands, the `.gitleaks.toml` configuration format (rules,
  allowlists, entropy thresholds, `extend` for building on the default rules rather than replacing
  them), the `.gitleaksignore` fingerprint file, the inline `gitleaks:allow` comment, exit codes
  for CI, and the official pre-commit hook and GitHub Action.

Two configuration points that decide whether it is kept:

- **Use `extend` rather than replacing the default rules.** A custom `.gitleaks.toml` that does
  not extend the defaults silently discards 150 useful patterns, and it is not obvious that it has
  happened.
- **Fingerprint-based ignores, not path-based.** `.gitleaksignore` entries keyed on a finding
  fingerprint suppress *that* finding; a path allowlist suppresses the file forever, including the
  real secret someone adds to it next year.

Licensing note worth knowing: gitleaks is MIT-licensed, and the author also offers a commercial
product built on it. The open-source scanner is complete and unrestricted for this use.

---

[← Secret scanning](../README.md)
