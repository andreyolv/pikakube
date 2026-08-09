[← LLM](../README.md)

# llmkube

<https://github.com/defilantech/llmkube>

---

## The problem it solves

**Recorded as a pointer, not as an evaluation.** The original notes for this folder contain the
project URL and nothing else, there are no manifests here, and nothing in this repository uses
it. What follows is therefore about *how to place it*, not a description of features that have
not been verified.

From its name and where it was filed, llmkube belongs to the same category as
[KAITO](../kaito/README.md): running LLM inference on Kubernetes through an operator rather than
by assembling Deployments and node selectors by hand. That is a real and crowded category — it
is the natural thing to build once you have deployed a model twice.

The useful question about any entrant in it is not what it does, because they all describe
themselves similarly. It is:

| Question | Why it decides the answer |
|---|---|
| What is the inference runtime underneath? | if it is [vLLM](../vllm/README.md), the serving properties are vLLM's and the operator is packaging |
| Who maintains it, and how many of them are there? | this determines whether a bug is fixed or inherited |
| What happens at the edge of the abstraction? | every operator has one; the cost is whether you can escape it |
| Does it provision nodes, or assume them? | this is the main functional dividing line — KAITO does |

Applied to a small, early project the honest conclusion is that the abstraction is the risk. An
operator sits between you and the serving engine permanently, and if it stops being maintained
the migration is not a configuration change.

## When to use it

Nothing here has been evaluated, so the only defensible answer is: when you have read the
project, confirmed the four questions above, and it beats the alternatives on something specific.
The likely shapes of that would be a simpler model than KAITO's for a cluster that does not need
node provisioning, or better support for a runtime you are already committed to.

## When not to use it

| Situation | Use instead |
|---|---|
| Production serving, today | [vLLM](../vllm/README.md) — the default, and the thing most operators wrap |
| Declarative model deployment with node provisioning | [KAITO](../kaito/README.md), which is the mature comparison in this folder |
| Local development or a quick trial | [Ollama](../ollama/README.md) |
| Any case where "it is a small project" is a problem | the maturity gap against vLLM and KAITO is the whole consideration |

## Notes

The only thing recorded for llmkube in the original notes was the project URL:

- <https://github.com/defilantech/llmkube>

**Nothing is deployed, and nothing here evaluates it.** It is filed as a candidate to look at,
which is what a large part of this repository is for. Deliberately not asserted above: what it
runs underneath, what its CRDs look like, and how active it is. Those are the things to check
first, and inventing them here would be worse than leaving the gap visible.

---

[← LLM](../README.md)
