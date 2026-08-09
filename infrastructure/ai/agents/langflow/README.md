[← Agents](../README.md)

# Langflow

<https://github.com/langflow-ai/langflow>
<https://github.com/langflow-ai/langflow-helm-charts>
<https://github.com/langflow-ai/langflow-embedded-chat>

---

## The problem it solves

Building an LLM flow in code means everyone who wants to change a prompt, swap a model or add a
retrieval step needs the repository, the toolchain and a review. For an application that is
mostly a chain of prompts, that is a lot of friction between the person with the domain
knowledge and the thing they want to adjust.

Langflow is a **visual builder**: drag nodes onto a canvas — model, prompt, vector store,
retriever, tool, agent — wire them together, run the flow, see the intermediate output at every
node. The flow is stored as JSON and can be exported, versioned and served as an API endpoint.

The part that makes it deployable rather than a toy is the split into two components, which is
exactly how the charts in this folder are laid out:

| Component | What it is | Who touches it |
|---|---|---|
| **langflow-ide** | the authoring UI plus its backend, where flows are built | builders, prompt authors |
| **langflow-runtime** | serves one exported flow as a headless API | nothing and nobody, at request time |

Running the IDE in production is the mistake this split exists to prevent. The runtime has no
canvas, no editing surface and no reason to hold the whole workspace — it executes a flow that
was already reviewed.

The **embedded chat** repository is a third piece: a web component you drop into a page to talk
to a deployed flow, so a working prototype can be put in front of users without building a
front end.

## When to use it

| Situation | Why Langflow fits |
|---|---|
| Non-engineers need to iterate on prompts and chains | the canvas is the interface, not the repository |
| Rapid prototyping of a RAG or tool-using flow | wiring is faster than writing, and intermediate output is visible |
| You need something demonstrable this week | the embedded chat closes the loop to a user |
| The flow is genuinely a chain, not a program | boxes and arrows describe it honestly |

## When not to use it

| Situation | Use instead |
|---|---|
| The logic has real branching, retries and error handling | [LangGraph](../langgraph/README.md) — a canvas hides control flow, it does not express it |
| The flow is part of an application's core path | code, in that application, tested like code |
| Flows must be reviewed as diffs | a JSON blob is a poor pull request; this is the main long-term cost |
| Strict latency or cost budgets | you cannot profile what you cannot read |
| It is business automation across SaaS systems | [n8n](../n8n/README.md) |

The honest failure pattern for visual builders is not that they fail — it is that they succeed,
and the prototype becomes production. What was six connected boxes becomes forty, nobody can
review the diff, and the thing that made it fast to build is what makes it impossible to change
safely. Decide up front whether a given flow is allowed to graduate, and if it is, plan the
rewrite into code rather than discovering it later.

## Notes

Recorded in the original notes:

- <https://github.com/langflow-ai/langflow> — the project.
- <https://github.com/langflow-ai/langflow-helm-charts> — the Helm charts, which is where the
  `langflow-ide` / `langflow-runtime` split comes from. The `HelmRelease` manifests in this
  folder point at the `values.yaml` of each chart as a comment, which is the pattern used across
  this repository for "the options are documented over there".
- <https://github.com/langflow-ai/langflow-embedded-chat> — the drop-in chat web component
  described above.

**What is deployed here.** Both charts, `langflow-ide` and `langflow-runtime`, at version
`0.1.1`, from the `HelmRepository` at `https://langflow-ai.github.io/langflow-helm-charts`, into
the `langflow` namespace. Both are running with **empty values** — chart defaults throughout.
That is fine for evaluation and not fine for anything else: chart defaults decide persistence,
authentication and resource limits, and none of those have been stated deliberately here.

Two things to look at before this is more than an evaluation: whether the IDE is exposed with
authentication in front of it, and whether flow storage is persistent — a builder that loses
work on a pod restart will not be used twice.

---

[← Agents](../README.md)
