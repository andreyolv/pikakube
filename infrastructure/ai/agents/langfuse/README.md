[← Agents](../README.md)

# Langfuse

<https://github.com/langfuse/langfuse>
<https://github.com/langfuse/langfuse-k8s>

---

**This tool is filed in the wrong folder.** Langfuse is not an agent framework and does not
orchestrate anything. It is **LLM observability** — tracing, prompt management, evaluation and
cost tracking. It sits closer to [`observability/`](../../../observability/README.md) than to
anything else in `agents/`, and the natural home for it would be an `ai/observability/` folder
alongside `ai/llm/` and `ai/ai-gateway/`. Recorded as an observation about the taxonomy, not as
a change — the folder is left where it is.

---

## The problem it solves

An LLM application fails differently from ordinary software. There is no stack trace. The
request succeeded, returned 200, and the answer was wrong. Something in a chain of eight model
calls produced nonsense and the next step confidently built on it. The bill tripled last week
and nobody can say which feature caused it.

Ordinary observability does not reach any of that. A trace tells you the call took 4.2 seconds;
it does not tell you what the prompt was, what came back, how many tokens it cost, or whether
the answer was any good.

Langfuse covers four distinct jobs, and it is worth separating them because teams usually need
them in this order:

| Job | What it means | Why it matters |
|---|---|---|
| **Tracing** | every model call, tool call and nested step recorded with its inputs and outputs | the only way to debug a multi-step chain — you can read what the model actually saw |
| **Cost tracking** | tokens in, tokens out, priced per model, attributable per trace, user or feature | LLM cost is usage-driven and invisible until it is a line item |
| **Prompt management** | prompts stored, versioned and served from Langfuse rather than hardcoded | changing a prompt stops being a deploy, and you can see which version produced which output |
| **Evaluation** | scores attached to traces — from humans, from heuristics, or from a model acting as judge | the substitute for tests when the output is not deterministic |

The one that changes how a team works is **tracing with full inputs and outputs**. Everything
else in this list is possible without it and painful; debugging a chain without it is mostly
guesswork.

That capability comes with an obligation. A trace store holds every prompt and every response,
which means it holds whatever users typed — including whatever they should not have typed.
Treat it as a data store with the same sensitivity as application logs at their worst, and
decide retention deliberately.

## When to use it

| Situation | Why Langfuse fits |
|---|---|
| Any LLM feature that has real users | you will need to see what actually happened, and you will need it urgently |
| Cost per feature or per team is a question | per-trace token accounting answers it; provider invoices do not |
| Prompts change often | versioned prompts served at runtime, with the output tied to the version |
| You need a quality signal without deterministic tests | scores on traces, and comparison across prompt versions |
| Self-hosting is a requirement | the OSS core is self-hostable and there is a maintained Helm chart |

## When not to use it

| Situation | Use instead |
|---|---|
| You want ordinary application traces | [`observability/tracing/`](../../../observability/tracing/README.md) — Langfuse is not a replacement for it |
| One prompt, one call, low volume | provider-side logs and a dashboard; this is a system to operate |
| You cannot afford its dependencies | see the notes — the self-hosted stack is not a single container |
| The data must never be stored at all | then do not store it; no observability tool solves that requirement |

There is also an overlap worth being deliberate about: an [AI gateway](../../ai-gateway/README.md)
also sees every request and can produce token counts and per-team attribution. The gateway sees
*traffic*; Langfuse sees *application semantics* — which chain, which step, which prompt version,
what score. Running both is defensible. Running both without deciding which one is authoritative
for cost is how two dashboards end up disagreeing.

## Notes

Recorded in the original notes:

- <https://github.com/langfuse/langfuse> — the project.
- <https://github.com/langfuse/langfuse-k8s> — the Kubernetes/Helm repository, which is the
  source of the chart deployed here.

**What is deployed here.** The `langfuse` chart at version `1.5.12`, from the `HelmRepository`
at `https://langfuse.github.io/langfuse-k8s`, into the `langfuse` namespace, with **empty
values** — chart defaults. The manifest also records two pointers as comments, the ArtifactHub
page and the chart's `values.yaml`, which is where the configurable surface is documented.

**Empty values matters more here than elsewhere.** Langfuse is not a single service: recent
major versions add ClickHouse for analytical queries, a cache, and S3-compatible object storage
alongside PostgreSQL. Chart defaults will bring up bundled versions of whatever it needs, which
is convenient and is not how any of those should run long-term — this repository already has
operators for the real thing. Before this is more than an evaluation, read the chart's
`values.yaml` and decide each dependency explicitly, the way
[kagent](../kagent/README.md) already points at an external CloudNativePG cluster rather than a
bundled database.

**On the folder placement**, restated so it is not lost: nothing in Langfuse orchestrates an
agent. It observes one. Its neighbours here are frameworks and platforms for *running* LLM
workloads; Langfuse is what you point at them afterwards.

---

[← Agents](../README.md)
