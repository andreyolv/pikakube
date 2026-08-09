[← Image scanning](../README.md)

# Docker Scout

<https://github.com/docker/scout-cli>
<https://github.com/docker/scout-action>

---

## The problem it solves

Docker Scout is Docker's own supply-chain and vulnerability product, and its actual
differentiator is not detection — it is **advice about the base image**.

Where other scanners hand you a list of CVEs in packages you did not choose, Scout tells you
which of them come from the base image and **which base image tag would remove them**. That is
the recommendation that matches the argument in [`base-images/`](../../base-images/README.md):
most findings in a typical image are inherited, and changing the base fixes them all at once.

Its other genuine strengths:

| Capability | Why it is useful |
|---|---|
| Base image recommendations | the fix is usually "move to a newer or smaller base", and Scout names it |
| Image comparison (`docker scout compare`) | diff two tags and see which findings a change added or removed — much more useful in a pull request than an absolute count |
| Integrated into Docker Desktop and Docker Hub | zero setup for developers who already use Docker; the findings appear where they already are |
| SBOM and provenance surfacing | reads attestations produced by BuildKit |

The delivery shapes are `scout-cli` (a Docker CLI plugin) and `scout-action` (the GitHub Action).

## When to use it

- **Docker Desktop and Docker Hub are already the workflow.** Scout is right there, with no
  installation and no pipeline change. For developer-facing feedback that is a real advantage
- **You want base image recommendations specifically.** No other tool in this folder does this
  as well, and it is the highest-value form of vulnerability advice
- **Pull-request diffs of vulnerability posture** — "this change adds three findings" is
  actionable in a way that "this image has 412 findings" is not
- **Small teams already paying for Docker.** If the subscription exists, the marginal cost is
  zero

## When not to use it

- **You need open source.** Recorded plainly in the original note: **Docker Scout is not open
  source.** The CLI and Action wrappers are on GitHub, but the analysis is a hosted Docker
  service. That rules it out wherever the requirement is self-hosted, air-gapped or auditable
  tooling
- **It requires a Docker subscription** beyond a limited free allowance, and the terms are
  Docker's to change. Building a security gate on it is building on a commercial dependency
- **Images are not in Docker Hub.** Scout works against other registries, but the integrated
  experience — the part that makes it worth choosing — is Hub-centric
- **You want in-cluster continuous scanning.** That is not what this is; Trivy Operator or
  [`../kubeclarity/README.md`](../kubeclarity/README.md) is
- **You want one tool for IaC, Kubernetes and secrets too.** Scout is image-focused

## Notes

Original notes recorded for this tool:

- <https://github.com/docker/scout-cli> — the Docker CLI plugin. Note what this repository
  actually contains: the client, its releases and its documentation. The scanning itself happens
  in Docker's hosted service.
- <https://github.com/docker/scout-action> — the GitHub Action wrapper, for running Scout in a
  workflow and posting results (including the `compare` output) onto a pull request.
- **"not open source"** — this is the recorded judgement in the original note and it is the
  decisive point. The wrappers are public; the product is not. Anywhere the requirement is
  "tooling we can inspect, self-host or run air-gapped", Scout is disqualified regardless of how
  good the base image recommendations are.

---

[← Image scanning](../README.md)
