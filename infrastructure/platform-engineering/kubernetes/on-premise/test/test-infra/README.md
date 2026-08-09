[← Test](../README.md)

# test-infra

<https://github.com/kubernetes/test-infra>

---

## The problem it solves

This is the Kubernetes project's **own CI infrastructure** — the machinery that tests Kubernetes
itself. It contains Prow, the Kubernetes-native CI system that runs on every pull request to the
project; the configuration for the thousands of jobs across the Kubernetes organisation; TestGrid,
which displays their results; and the tooling around release verification.

It is not something you install to test your cluster. It is what the project runs to test its own
code.

## When to use it

- Contributing to Kubernetes, where understanding Prow is necessary to read the bot comments on your PR
- As a reference for building CI at scale on Kubernetes — Prow is genuinely instructive
- Investigating whether an upstream failure is a real bug or a known flaky test, via TestGrid
- Running Prow independently, which some large organisations do

## When not to use it

- Testing **your** cluster — that is [Sonobuoy](../sonobuoy/README.md)
- As a general-purpose CI system; Prow is powerful and shaped tightly around the Kubernetes project's
  workflow
- Without a substantial reason; the operational weight is significant

## Notes

Recorded as a link only, and filed in `test/` next to
[Sonobuoy](../sonobuoy/README.md) — which is worth flagging, because the two answer completely
different questions:

| | Sonobuoy | test-infra |
|---|---|---|
| Tests | **your cluster** | **Kubernetes itself** |
| Audience | cluster operators | Kubernetes contributors |
| Question | is this a conformant cluster | did this pull request break anything |

Both are "testing Kubernetes" in a sentence and nothing alike in practice. The pairing presumably
comes from that phrase.

**What is genuinely useful in it for an operator**, rather than a contributor:

- **TestGrid** — when a Kubernetes release behaves unexpectedly, TestGrid shows whether the relevant
  upstream tests are failing or flaky. That converts "is this us or is this a known problem" from a
  guess into a lookup.
- **Prow as a reference design.** It is a CI system built as Kubernetes controllers, where jobs are
  pods and configuration is declarative. Reading how it handles job scheduling, artifact collection
  and merge automation is instructive even if you never run it.
- **The job configuration** shows, concretely, how a project tests Kubernetes across dozens of
  configurations — which is a useful model when deciding what your own cluster CI should cover.

Filed as a bookmark for the upstream project's machinery, not as a tool for this repository.

---

[← Test](../README.md)
