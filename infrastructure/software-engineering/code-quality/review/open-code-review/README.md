[← Review](../README.md)

# Open Code Review

<https://github.com/alibaba/open-code-review>

---

## The problem it solves

The same problem as [PR-Agent](../pr-agent/README.md): a diff arrives, and the first pass over it
is mechanical work that a model can do faster than a person. Open Code Review is Alibaba's
open-source take on putting an LLM into that step and having it comment on the change
automatically.

It belongs in the same category and answers the same question — *can a machine do the first read?*
— which is why it is catalogued next to PR-Agent rather than next to
[reviewdog](../reviewdog/README.md). reviewdog forwards findings from tools that already exist;
these two generate the findings themselves.

## When to use it

- When an **open-source, self-hostable** LLM reviewer is a requirement and the alternatives are
  commercial or hosted.
- As an **alternative to evaluate against PR-Agent**, not alongside it. Two LLM reviewers on the
  same pull request produce two sets of overlapping comments and double the noise.
- Under the same rule that applies to the whole category: configured to **comment, never to
  block**, with a person still approving the merge.

## When not to use it

- As the only reviewer, or as a merge gate. The reasoning is identical to
  [PR-Agent](../pr-agent/README.md): no context outside the diff, and no accountability.
- Before the cheap checks exist. Formatting and lint findings belong to
  [`../../format/`](../../format/README.md) and [`../../lint/`](../../lint/README.md), where they
  cost nothing per run.
- Where the diff cannot be sent to a model and none can be self-hosted.
- **On the strength of this page.** Nothing here is from use — see the notes below.

## Notes

The original note for this folder records exactly one thing, the upstream repository:

- <https://github.com/alibaba/open-code-review>

No trial, no configuration, no manifest and no recorded opinion. This is the thinnest entry in
[`../`](../README.md), and the honest summary is: **it was seen, it was filed, it has not been
evaluated.**

That matters for how the page should be read. Everything above describes the category the tool
belongs to, not measured behaviour of this tool. The concrete questions still open — which models
it supports, whether it can run fully self-hosted, which forges it integrates with, how noisy its
default output is — are exactly the ones that would decide it against
[PR-Agent](../pr-agent/README.md), and none of them have been answered here.

If an LLM reviewer is ever adopted for this repository, the first step is to answer those
questions for both tools. The step before that is
[reviewdog](../reviewdog/README.md) plus a linter, which delivers most of the value with none of
the data-egress question.

---

[← Review](../README.md)
