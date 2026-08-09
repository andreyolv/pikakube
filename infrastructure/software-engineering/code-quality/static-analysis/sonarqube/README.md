[← Static analysis](../README.md)

# SonarQube

<https://github.com/SonarSource/sonarqube>
<https://github.com/SonarSource/helm-chart-sonarqube>
<https://github.com/SonarSource/sonarqube-scan-action>

---

## The problem it solves

Every individual code-quality signal exists somewhere already — a linter reports rule violations,
a test run reports coverage, a reviewer notices duplication if they happen to have seen the other
copy. None of them are kept, and none of them are comparable between one week and the next or
between one repository and another.

SonarQube is the place those signals are stored and compared. It scans the project, keeps the
results, and answers the question no stateless tool can: **is this getting better or worse?**

Its more important feature is the **quality gate** — a pass/fail condition evaluated against
*new and changed code* rather than the whole codebase. That framing is what makes it usable on a
codebase that already exists: the pull request that adds untested, duplicated, over-complex code
fails, and the pull request that does not, passes, regardless of the state of the surrounding
file. Gating on the total instead is the standard way this tool gets installed, ignored and
switched off.

It covers a large number of languages from one server, which is the argument for it over
per-language tooling in a polyglot estate: one measure, one gate, every repository.

## When to use it

- Several repositories, several teams, and a need for a **comparable** measure across all of
  them. This is the case it is built for and the only one where the operational cost is clearly
  worth it.
- Where the quality gate is going to be **enforced** — blocking merges on new code. Enforcement is
  the whole product; without it this is a dashboard.
- Polyglot codebases. One scanner covering Python, Java, TypeScript, Go and the rest is worth more
  than the best individual tool per language, because it produces one number everyone reads the
  same way.
- When coverage needs to be tracked over time rather than printed at the end of a test run.

## When not to use it

- For a **single small repository**. It is a JVM application plus a database plus storage, and at
  that scale a linter finds most of the same things for the cost of a CI step. Start with
  [`../../lint/`](../../lint/README.md).
- As a **security scanner**. See the notes below — this is the important boundary and it is
  routinely collapsed.
- As a **substitute for review**. It measures properties of code, not whether the change is a good
  idea — see [`../../review/`](../../review/README.md).
- If nobody will own the server. Scan history grows without bound by default, and an instance
  nobody maintains fills its disk and stops mid-quarter.
- Gating on absolute totals against a legacy codebase. It will be red permanently and the gate will
  be removed.

## Notes

The original note for this folder records three repositories, and the split between them is the
useful part:

| Link | What it is |
|---|---|
| <https://github.com/SonarSource/sonarqube> | the server itself |
| <https://github.com/SonarSource/helm-chart-sonarqube> | the official Helm chart — **how it runs here** |
| <https://github.com/SonarSource/sonarqube-scan-action> | the GitHub Action that scans a repository and reports to the server |

**The two halves.** The chart deploys the server; the action is what actually sends it something
to analyse. A server without a scanner configured in CI is an empty dashboard, and that is the
current state — the manifests in this folder deploy the first half only.

**What is deployed.** Flux manifests exist here: a `HelmRepository` pointing at
`https://SonarSource.github.io/helm-chart-sonarqube`, a `HelmRelease` pinned to chart version
`2026.3.1` with an empty `values` block, and a `sonarqube` namespace. Pinning the chart version is
correct and worth keeping — a floating version on a stateful application means an unplanned
database migration.

**The overlap with security — the point to internalise.** This repository also holds
`infrastructure/security/4-code/sast/`, containing Semgrep, Bandit, CodeQL, gosec and Horusec.
That path is deliberately written as text and not linked: the directory exists, its README does
not yet, and this repository does not link to files that are not there.

SonarQube and Semgrep both analyse source code. They answer different questions:

| | SonarQube | Semgrep and the SAST set |
|---|---|---|
| Asks | **is this maintainable?** | **is this exploitable?** |
| Reports | duplication, complexity, dead code, coverage, code smells | injection, unsafe deserialisation, hardcoded secrets |
| A red build means | quality is degrading | a vulnerability is shipping |

SonarQube does ship security rules, and they are not worthless — but **"we run SonarQube" is not
an answer to "do you do SAST?"** The two tools are complementary, and the reason the folders are
separate is so that running one never looks like having done the other.

**Before this is useful here:** wire `sonarqube-scan-action` into CI, and configure the quality
gate on new code only. Neither is done.

---

[← Static analysis](../README.md)
