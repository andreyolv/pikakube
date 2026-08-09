[← Visualisation](../README.md)

# WrenAI

<https://github.com/Canner/WrenAI>

---

## What it is

Natural-language querying over a data warehouse: a question in plain language becomes SQL,
runs, and returns a result with a chart.

Its distinguishing choice is that it does **not** point an LLM at raw tables. It uses a
semantic model — table relationships, metric definitions, business meaning — and generates SQL
against that. Which addresses the obvious objection: a model guessing at schema produces
confident, wrong answers.

## When it is interesting

- business users ask questions faster than analysts can answer them
- a semantic model already exists, so the generated SQL has something correct to build on
- exploratory questions where the alternative is a ticket and a two-day wait

## When it is not

- **the answer has to be right.** Generated SQL is plausible by construction and correct by
  luck. For anything reported externally or used in a decision, a reviewed
  [dbt model](../../transform/dbt/README.md) is the answer
- there is no semantic layer — without one it is guessing at the schema
- data access is sensitive; the question and the schema go to a model

## Status

> No Helm chart yet — <https://github.com/Canner/WrenAI/issues/1753>

Which makes it awkward for a GitOps setup where everything else is a `HelmRelease`.

## The honest framing

This category is genuinely promising and genuinely unreliable. It works well for exploration —
"roughly how many orders last month" — and badly for anything where being wrong matters,
because it fails **confidently**.

The useful position: treat generated SQL as a **draft query**, not an answer. It saves the
blank page, and a human still verifies it before the number is used.

Related: the same trade-off appears in
[`observability/troubleshooting/`](../../../observability/troubleshooting/README.md), where
AI-assisted diagnosis is good at recurring cases and confidently wrong on novel ones.

---

[← Visualisation](../README.md)
