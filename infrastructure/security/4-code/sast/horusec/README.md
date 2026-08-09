[← SAST](../README.md)

# Horusec

<https://github.com/ZupIT/horusec>

---

## The problem it solves

A polyglot repository needs bandit for the Python, gosec for the Go, a JavaScript analyser, a
secret scanner, and something for the Dockerfiles. Each has its own installation, its own
configuration file and its own output format, and someone has to stitch the results together.

Horusec is an **orchestrator**. One CLI runs many underlying analysers — including gosec, bandit,
semgrep, gitleaks, npm/yarn audit and others — normalises their output into a single report, and
applies one severity policy across all of them:

```bash
# analyse the current directory with every applicable tool
horusec start -p .
```

The design points that follow:

| Property | Consequence |
|---|---|
| Language detection | it decides which analysers apply, so no per-language configuration |
| Tools run in containers | you do not install a dozen scanners; you need a Docker daemon |
| One unified report | one severity scale, one JSON/SARIF output, one exit code |
| One vulnerability management surface | its own dashboard and API, optionally self-hosted |
| Secret detection included | so the same run covers [`../../secret-scanner/README.md`](../../secret-scanner/README.md)'s question too |

It was built by **Zup Innovation** (a Brazilian engineering organisation) and is open source.

## When to use it

- **A polyglot monorepo where per-language tooling has become the problem** — Horusec's whole
  premise is removing that setup cost
- **You want one command and one report** without building the aggregation yourself
- **An easy first step.** For a team with no application security tooling at all, `horusec start`
  produces a broad picture quickly, which is useful for deciding where to invest properly
- **You want the underlying tools' findings without adopting each tool's workflow**

## When not to use it

- **Check the project's maintenance status first.** This is the decisive question and it should be
  answered before anything else. Horusec's development slowed considerably after its initial
  push, and an orchestrator that stops being updated is worse than the tools it wraps — it pins
  old versions of each analyser, so your Python checks are whatever bandit was two years ago,
  invisibly
- **You want control over each analyser.** Custom Semgrep rules, tuned bandit exclusions and
  gosec configuration are all easier to manage when you run the tools directly. An orchestrator
  abstracts exactly the configuration you eventually need
- **The false-positive problem is the problem.** Running five tools at once multiplies findings
  rather than curating them, which is the opposite of the advice in
  [`../README.md`](../README.md) section 3
- **You already run Semgrep.** Semgrep alone covers most languages with one configuration, which
  achieves the same goal with fewer moving parts
- **Aggregation is what you actually want.** For deduplicating and triaging findings from many
  tools across many repositories, a purpose-built ASPM platform is the right shape —
  [`../../aspm/defectdojo/README.md`](../../aspm/defectdojo/README.md)
- **CI without a Docker daemon.** Analysers run as containers, which is a hard requirement

## Notes

Original note recorded for this tool:

- <https://github.com/ZupIT/horusec> — the upstream project from ZupIT. The repository documents
  which analysers are wrapped per language, the `horusec-config.json` configuration (severity
  thresholds, false-positive and risk-accepted hashes, which tools to disable), the CLI flags,
  and the optional self-hosted web platform with its own services and database.

The one thing to verify before adopting it, restated because it governs everything else: **check
the last release and the currency of the wrapped analyser versions.** The value of an
orchestrator is entirely dependent on it keeping up with the tools it orchestrates.

---

[← SAST](../README.md)
