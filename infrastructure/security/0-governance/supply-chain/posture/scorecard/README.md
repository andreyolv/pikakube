[← Posture](../README.md)

# OpenSSF Scorecard

<https://github.com/ossf/scorecard>
<https://github.com/ossf/scorecard-action>

---

## The problem it solves

"Is this project well run?" is asked constantly — about your own repositories during a security
review, and about every dependency you are about to adopt — and it is normally answered by
impression.

Scorecard automates it. It runs a set of checks against a repository and produces a score per
check plus an overall number: is branch protection enabled, are pull requests reviewed, are
GitHub Actions pinned to commit SHAs, are workflow token permissions scoped down, are there
dangerous workflow patterns, is there a security policy, are releases signed, is fuzzing set
up, has anyone committed recently, are there known vulnerabilities in dependencies.

Every check maps to a practice that correlates with catching problems. None of them looks at
what the code does — which is the correct way to read the output, and the subject of
[`../README.md`](../README.md#4-what-a-score-does-not-mean).

It is an OpenSSF project and is used at scale: results for a large number of public
repositories are published, and [deps.dev](https://deps.dev) surfaces Scorecard data alongside
dependency graphs, which makes it available as a dependency-selection signal without running
anything yourself.

## When to use it

- on **your own repositories**, as a checklist — the failing checks are usually configuration
  changes, not projects
- when choosing between dependencies that do the same job, as one comparative input
- to find the two specific things it is best at: **unpinned GitHub Actions** and
  **over-permissive workflow tokens**, both of which are real supply-chain exposure and both
  of which are easy to fix
- on a schedule, because practices drift — unpinned actions reappear as workflows are edited
- as a cheap first move in a repository with no supply-chain controls at all

## When not to use it

- as a security guarantee, or as evidence that code is safe. It measures habits
- as a hard acceptance gate with a minimum score — scores are not comparable across project
  types, and small, well-run, single-maintainer libraries routinely score poorly for reasons
  that do not matter
- as a substitute for SAST, SCA or dependency scanning; those live in `4-code/` and answer
  different questions
- when the goal has become raising the number. Several checks are satisfiable cosmetically
  without changing any security property

## Notes

Original notes recorded for this tool:

> <https://github.com/ossf/scorecard>
>
> # github action
> <https://github.com/ossf/scorecard-action>
>
> The Scorecards GitHub Action is free for all public repositories. Private repositories are
> supported if they have GitHub Advanced Security. Private repositories without GitHub
> Advanced Security can run Scorecards from the command line by following the standard
> installation instructions.

That licensing note is the practically important one and it is worth restating as a decision:

| Repository | Path |
|---|---|
| **Public** | `scorecard-action` — free, and results can be published to the OpenSSF API |
| **Private + GitHub Advanced Security** | `scorecard-action` is supported |
| **Private, no GHAS** | run the **CLI** — same checks, no Action; a step in CI or a scheduled job |

So there is no case where Scorecard is unavailable; there is only a case where the convenient
wrapper is not. That matters because the usual reason it goes unused in a private repository is
the assumption that it requires a paid feature, which is a misreading — the CLI is the same
tool.

Two operational points. The Action wants a repository token with enough scope to read branch
protection settings, and it uploads results as SARIF so findings appear in the security tab —
which is the difference between a report someone runs once and findings that show up where
people already look. And when reading results, treat the **pinned dependencies** and
**token permissions** checks as the ones with direct security content; the rest are health
indicators, valuable but softer.

---

[← Posture](../README.md)
